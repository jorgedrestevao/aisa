# -*- coding: utf-8 -*-
"""Coordenador de operações e recuperação — contrato B (WRITES_AND_RECOVERY).

    python library/kernel/tools/operation.py status --engagement <slug> [--json]
    python library/kernel/tools/operation.py recover --engagement <slug>

Stdlib apenas (ADR-001). Sem serviço, sem base de dados, sem framework transaccional.

O QUE ISTO GARANTE, E O QUE NÃO GARANTE

Garante (B1): uma falha pode deixar bytes parcialmente publicados, mas NUNCA produz uma
leitura operacional de sucesso sobre esse estado. É atomicidade observável pelos leitores
suportados — não promessa de transacção do sistema de ficheiros.

Não garante: leitores externos arbitrários. Quem lê os ficheiros por fora da barreira está
explicitamente fora da garantia; o que se faz é DETECTAR que mudaram, antes da operação
seguinte.

DISPOSIÇÃO EM DISCO

    <engagement>/_ops/pending.json         marcador — presença bloqueia mutação e gate
    <engagement>/_ops/staging/<op>/…       bytes preparados, antes de publicar
    <engagement>/_ops/receipts/<op>.json   recibo idempotente

    $TMP/aisa-op-<hash>.json               exclusão (lock)

O lock vive FORA do engagement, como o do dashboard e pela mesma razão: a pasta do
engagement é material de cliente e um ficheiro de runtime não tem que ser versionado com
ela. O marcador de pendência é o contrário — tem de sobreviver a tudo, e fica no engagement.

EXCLUSÃO (B2.2)

Quem exclui é o kernel, por `flock` sobre o ficheiro de lock — não a existência do
ficheiro. A diferença não é de estilo. Medido com processos reais barrados no mesmo
instante sobre um lock abandonado, a exclusão por existência dava **seis donos do mesmo
engagement em seis processos, doze corridas em doze**: todos liam o mesmo dono morto,
todos o davam por recuperável, todos escreviam o seu por cima. A jusante, isso custava
escrita confirmada e perdida em sete de oito corridas — quatro recibos `committed`, o
ficheiro com um, e `BASE_CHANGED` calado porque todos tinham lido a mesma base.

Com `flock` não há recuperação a decidir: um lock deixado por um processo morto não tem
lock nenhum agarrado, e o próximo a chegar entra sem corrida. O `pid` + instante de
arranque fica — mas como REGISTO de quem tem (o que `status` mostra) e como recusa
conservadora perante um lock escrito por uma versão sem `flock`, não como o mecanismo.

Lock abandonado continua a não ser removido por timeout cego, e um lock ilegível não é
removido de todo.

O limite, declarado: `flock` é do sistema de ficheiros local. Em NFS antigo ou num
sistema sem `fcntl`, cai-se na criação exclusiva — e aí a recuperação de um lock morto
volta a não ser exclusiva. `status()` diz qual dos dois está em uso (`exclusion`).

ORDEM (B2)

    intenção -> marcador visível -> publicação individual temp+rename -> verificação
    -> recibo + revisão de commit -> retirar pendência -> responder sucesso

O marcador é escrito ANTES de qualquer publicação e retirado DEPOIS do recibo. Entre os
dois, qualquer leitor vê pendência e recusa-se a declarar sucesso.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

try:
    import fcntl
except ImportError:                                # pragma: no cover — não-POSIX
    fcntl = None

# Qual dos dois mecanismos está em uso. `status()` publica-o: quem lê um resultado tem de
# poder saber sob que garantia ele foi produzido.
EXCLUSION = "flock" if fcntl else "create-exclusive"
LOCK_TRIES = 5

OPS_DIR = "_ops"
PENDING = "pending.json"
STAGING = "staging"
RECEIPTS = "receipts"
INTENT_VERSION = 1

# Estados devolvidos por `status()`. Cada um é distinto — B4 proíbe mascarar uns nos outros.
CLEAN = "clean"
PENDING_OPERATION = "pending_operation"
LOCKED = "active_lock"
CONFLICT = "conflict"


class OperationError(Exception):
    def __init__(self, message: str, code: str, detail: dict | None = None):
        super().__init__(message)
        self.code = code
        self.detail = detail or {}

    def as_dict(self) -> dict:
        return {"error": str(self), "code": self.code, "detail": self.detail}


# ------------------------------------------------------------------ identidade

def _proc_started(pid: int) -> str:
    """Instante de arranque do processo, para distinguir um pid reutilizado.

    Em Linux vem do campo 22 de `/proc/<pid>/stat` (jiffies desde o boot). Onde não
    existe, devolve "" — e a ausência é tratada como identidade fraca: um lock sem
    instante de arranque nunca é considerado abandonado com certeza."""
    try:
        with open("/proc/{}/stat".format(pid), "r", encoding="utf-8") as fh:
            raw = fh.read()
        return raw.rsplit(")", 1)[1].split()[19]
    except (OSError, IndexError, ValueError):
        return ""


def _alive(pid: int, started: str) -> bool | None:
    """True vivo, False morto, None não determinável (e aí não se assume nada)."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True          # existe, é de outro utilizador
    except OSError:
        return None
    if started:
        now = _proc_started(pid)
        if now and now != started:
            return False     # pid reutilizado: o dono do lock morreu
        if not now:
            return None
    return True


# fds com `flock` agarrado, por caminho de lock. Vive em memória de propósito: um fd não
# se herda por um ficheiro, e um lock que sobrevivesse ao processo seria o bug de origem.
_HELD: dict = {}


def _identity() -> dict:
    return {"pid": os.getpid(), "started": _proc_started(os.getpid()),
            "host": os.uname().nodename if hasattr(os, "uname") else "",
            "at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


# ----------------------------------------------------------------------- disco

def ops_dir(eng: Path) -> Path:
    return Path(eng) / OPS_DIR


def _lock_path(eng: Path) -> Path:
    key = hashlib.sha1(str(Path(eng).resolve()).encode("utf-8")).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / "aisa-op-{}.json".format(key)


def _read_json(p: Path):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _atomic_write(p: Path, text: str) -> None:
    """tmp com pid -> os.replace. O pid no nome evita que dois escritores se pisem."""
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".{}.tmp".format(os.getpid()))
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, p)


def digest(p: Path) -> str:
    """Hash dos bytes, ou "" se o ficheiro não existe. Ausência é um estado, não um erro."""
    try:
        return hashlib.sha256(Path(p).read_bytes()).hexdigest()
    except OSError:
        return ""


# ----------------------------------------------------------------------- lock

def _flock_fd(lp: Path) -> int:
    """fd com `flock` exclusivo E a certeza de que o caminho ainda aponta para ele.

    A segunda metade não é zelo a mais. Quem liberta o lock apaga o ficheiro, e entre o
    `unlink` de um e o `open` de outro o inode pode já não ser o mesmo: sem a comparação,
    ficava-se com um lock agarrado a um inode órfão enquanto um terceiro criava o ficheiro
    novo e o trancava também. Dois donos outra vez, por outro caminho.
    """
    for _ in range(LOCK_TRIES):
        fd = os.open(str(lp), os.O_CREAT | os.O_RDWR, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            os.close(fd)
            return -1                      # ocupado por um vivo, sem ambiguidade
        try:
            mesmo = os.fstat(fd).st_ino == os.stat(str(lp)).st_ino
        except OSError:
            mesmo = False
        if mesmo:
            return fd
        _unlock(fd)                        # o caminho trocou de inode: recomeçar
    raise OperationError(
        "o ficheiro de lock trocou de inode {} vezes seguidas".format(LOCK_TRIES),
        "LOCK_CONTENDED", {"lock": str(lp)})


def _unlock(fd: int) -> None:
    try:
        if fcntl:
            fcntl.flock(fd, fcntl.LOCK_UN)
    except OSError:
        pass
    try:
        os.close(fd)
    except OSError:
        pass


def _held_by(lp: Path):
    """O que o ficheiro de lock diz. `None` se está vazio — recém-criado não é ilegível."""
    try:
        bruto = lp.read_text(encoding="utf-8")
    except OSError:
        return None
    if not bruto.strip():
        return None
    try:
        return json.loads(bruto)
    except ValueError:
        raise OperationError("lock ilegível — não removido às cegas", "LOCK_UNREADABLE",
                             {"lock": str(lp)})


def _refuse_if_foreign(held, lp: Path) -> dict | None:
    """Recusa conservadora sobre o REGISTO, para lá do que o kernel já garantiu.

    Ter o `flock` prova que nenhum escritor desta versão está lá dentro. Não prova que não
    está lá um de uma versão anterior, que nunca chamou `flock`. Por isso, se o registo diz
    um dono vivo, recusa-se na mesma — e devolve-se o que ele era, para o recuperar ficar
    registado em vez de silencioso.
    """
    if not held:
        return None
    alive = _alive(int(held.get("pid") or -1), str(held.get("started") or ""))
    if alive is True:
        raise OperationError(
            "outro escritor tem o engagement (pid {})".format(held.get("pid")),
            "LOCK_ACTIVE", {"holder": held})
    if alive is None:
        raise OperationError(
            "lock de posse indeterminada (pid {}) — não removido por timeout cego".format(
                held.get("pid")),
            "LOCK_UNDETERMINED", {"holder": held})
    return held


def acquire(eng: Path) -> dict:
    """Exclusão por engagement. Decide o kernel; o ficheiro só regista quem tem (B2.2)."""
    lp = _lock_path(eng)
    ident = _identity()
    ident["engagement"] = str(Path(eng).resolve())
    if not fcntl:                                  # pragma: no cover — não-POSIX
        return _acquire_by_create(lp, ident)

    fd = _flock_fd(lp)
    if fd < 0:
        held = None
        try:
            held = _held_by(lp)
        except OperationError:
            pass
        raise OperationError(
            "outro escritor tem o engagement (pid {})".format(
                (held or {}).get("pid", "?")),
            "LOCK_ACTIVE", {"holder": held})
    try:
        morto = _refuse_if_foreign(_held_by(lp), lp)
        if morto:
            # dono morto: a recuperação é registada, não silenciosa
            ident["recovered_from"] = morto
        # Escrita PELO fd, nunca `_atomic_write`: um `os.replace` trocava o inode por baixo
        # do lock que estamos a segurar, e o lock deixava de valer para quem abrisse a
        # seguir pelo caminho.
        os.lseek(fd, 0, os.SEEK_SET)
        os.ftruncate(fd, 0)
        os.write(fd, json.dumps(ident).encode("utf-8"))
        os.fsync(fd)
    except BaseException:
        _unlock(fd)
        raise
    _HELD[str(lp)] = fd
    return ident


def _acquire_by_create(lp: Path, ident: dict) -> dict:   # pragma: no cover — não-POSIX
    """Sem `fcntl`: criação exclusiva. Declaradamente mais fraca — ver a docstring."""
    try:
        fd = os.open(str(lp), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(ident, fh)
        return ident
    except FileExistsError:
        pass
    held = _held_by(lp)
    if not held:
        raise OperationError("lock ilegível — não removido às cegas", "LOCK_UNREADABLE",
                             {"lock": str(lp)})
    morto = _refuse_if_foreign(held, lp)
    ident["recovered_from"] = morto
    _atomic_write(lp, json.dumps(ident))
    return ident


def release(eng: Path, ident: dict) -> None:
    """Só o dono liberta. Um lock de outro nunca é apagado por engano."""
    lp = _lock_path(eng)
    held = _read_json(lp)
    if not (held and held.get("pid") == ident.get("pid")
            and held.get("started") == ident.get("started")):
        return
    fd = _HELD.pop(str(lp), None)
    try:
        lp.unlink()
    except OSError:
        pass
    if fd is not None:
        _unlock(fd)          # o unlock vem DEPOIS do unlink: o caminho já não é este


# -------------------------------------------------------------------- pendência

def pending_path(eng: Path) -> Path:
    return ops_dir(eng) / PENDING


def read_pending(eng: Path) -> dict | None:
    return _read_json(pending_path(eng))


def status(eng: Path) -> dict:
    """O que um leitor vê ANTES de decidir seja o que for (B3)."""
    eng = Path(eng)
    p = read_pending(eng)
    lp = _lock_path(eng)
    held = _read_json(lp) if lp.exists() else None
    alive = None
    if held:
        alive = _alive(int(held.get("pid") or -1), str(held.get("started") or ""))
    if p:
        return {"state": PENDING_OPERATION, "exclusion": EXCLUSION,
                "operation_id": p.get("operation_id"),
                "write_set": list(p.get("after", {})),
                "detail": "operação pendente — mutação e gate bloqueados até recuperar",
                "recovery": "python library/kernel/tools/operation.py recover --engagement <slug>",
                "lock_held_by": held if alive else None}
    if held and alive is True:
        return {"state": LOCKED, "exclusion": EXCLUSION,
                "detail": "escritor activo (pid {})".format(held.get("pid")),
                "lock_held_by": held}
    return {"state": CLEAN, "exclusion": EXCLUSION, "detail": ""}


def gate_open(eng: Path) -> bool:
    """Um gate NUNCA passa sobre pendência (B4)."""
    return status(eng)["state"] == CLEAN


# -------------------------------------------------------------------- recibos

def receipt_path(eng: Path, op_id: str) -> Path:
    return ops_dir(eng) / RECEIPTS / "{}.json".format(op_id)


def read_receipt(eng: Path, op_id: str) -> dict | None:
    return _read_json(receipt_path(eng, op_id))


def request_hash(write_set: dict) -> str:
    """Identidade do PEDIDO. Mesmo id com payload diferente é erro (B2)."""
    body = json.dumps({k: hashlib.sha256(v.encode("utf-8")).hexdigest()
                       for k, v in sorted(write_set.items())},
                      ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------- operação

def run(eng: Path, operation_id: str, write_set: dict, expected: dict | None = None) -> dict:
    """Publica um conjunto de escrita como UMA operação.

    `write_set`: `{caminho relativo ao engagement: conteúdo}`.
    `expected`  : `{caminho relativo: digest esperado}` — a base sobre a qual se calculou.
                  `""` significa «não existia». Base diferente = recusa (B2.3).

    Devolve o recibo. Repetir o mesmo `operation_id` com o mesmo pedido devolve o recibo
    existente sem repetir efeitos (B2, W03)."""
    eng = Path(eng)
    rq = request_hash(write_set)

    prior = read_receipt(eng, operation_id)
    if prior:
        if prior.get("request_hash") != rq:
            raise OperationError(
                "mesmo operation_id com pedido diferente", "RECEIPT_MISMATCH",
                {"operation_id": operation_id, "have": prior.get("request_hash"), "got": rq})
        # Um recibo diz que a operacao aconteceu; NAO diz que os efeitos sobreviveram. Um
        # `restore` a montante apaga os ficheiros e deixa o recibo para tras — e repetir a
        # operacao passava a devolver sucesso sem escrever nada. Quem chama tem de poder
        # distinguir «ja feito» de «ja feito e desfeito», entao a resposta di-lo.
        gravado = prior.get("revision") or {}
        agora = {rel: digest(eng / rel) for rel in gravado}
        return dict(prior, replayed=True, effects_present=(agora == gravado))

    ident = acquire(eng)
    try:
        existing = read_pending(eng)
        if existing:
            raise OperationError(
                "existe operação pendente ({}) — recuperar antes de mutar".format(
                    existing.get("operation_id")),
                "PENDING_EXISTS", {"pending": existing})

        # --- 3. base esperada, sob exclusão
        before = {rel: digest(eng / rel) for rel in write_set}
        if expected is not None:
            for rel, want in expected.items():
                if before.get(rel, "") != want:
                    raise OperationError(
                        "base mudou em `{}` — reavaliar, não sobrescrever".format(rel),
                        "BASE_CHANGED",
                        {"path": rel, "expected": want, "actual": before.get(rel, "")})

        # --- 4/5. staging + intenção, ANTES de publicar
        stg = ops_dir(eng) / STAGING / operation_id
        if stg.exists():
            shutil.rmtree(stg)
        stg.mkdir(parents=True)
        after = {}
        for rel, content in sorted(write_set.items()):
            sp = stg / rel.replace("/", "__")
            sp.write_text(content, encoding="utf-8", newline="\n")
            after[rel] = hashlib.sha256(content.encode("utf-8")).hexdigest()

        intent = {"intent_version": INTENT_VERSION, "operation_id": operation_id,
                  "request_hash": rq, "owner": ident,
                  "before": before, "after": after,
                  "staging": str(stg.relative_to(eng)),
                  "opened_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        _atomic_write(pending_path(eng), json.dumps(intent, ensure_ascii=False, indent=2))

        # --- 6. publicação individual, ordem determinada
        published = _publish(eng, intent)

        # --- 7. verificação + recibo, antes de retirar a pendência
        receipt = _finish(eng, intent, published)
        return receipt
    finally:
        release(eng, ident)


def _publish(eng: Path, intent: dict) -> list[str]:
    stg = Path(eng) / intent["staging"]
    done = []
    for rel in sorted(intent["after"]):
        src = stg / rel.replace("/", "__")
        dst = Path(eng) / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        _atomic_write(dst, src.read_text(encoding="utf-8"))
        done.append(rel)
    return done


def _finish(eng: Path, intent: dict, published: list[str]) -> dict:
    """Verifica, escreve o recibo, e SÓ DEPOIS retira a pendência."""
    for rel, want in intent["after"].items():
        got = digest(Path(eng) / rel)
        if got != want:
            raise OperationError(
                "verificação falhou em `{}` — pendência mantida".format(rel),
                "VERIFY_FAILED", {"path": rel, "expected": want, "actual": got})
    receipt = {"operation_id": intent["operation_id"], "request_hash": intent["request_hash"],
               "result": "committed", "revision": intent["after"],
               "published": published,
               "committed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    _atomic_write(receipt_path(eng, intent["operation_id"]),
                  json.dumps(receipt, ensure_ascii=False, indent=2))
    try:
        pending_path(eng).unlink()
    except OSError:
        pass
    try:
        shutil.rmtree(Path(eng) / intent["staging"])
    except OSError:
        pass
    return receipt


# ----------------------------------------------------------------- recuperação

def recover(eng: Path) -> dict:
    """Completa ou reporta uma operação interrompida. Repetir NÃO muda o resultado (B4, W06)."""
    eng = Path(eng)
    intent = read_pending(eng)
    if not intent:
        return {"result": "nothing_pending"}
    if intent.get("intent_version") != INTENT_VERSION:
        raise OperationError("versão de intenção não suportada", "INTENT_VERSION",
                             {"have": intent.get("intent_version")})

    ident = acquire(eng)
    try:
        third = []
        for rel in intent["after"]:
            got = digest(eng / rel)
            if got not in (intent["before"].get(rel, ""), intent["after"][rel]):
                third.append({"path": rel, "actual": got,
                              "before": intent["before"].get(rel, ""),
                              "after": intent["after"][rel]})
        if third:
            # B4: terceiro estado NÃO se sobrescreve. Preserva-se e reporta-se.
            raise OperationError(
                "bytes de terceiro estado — recuperação recusada sem sobrescrever",
                "THIRD_STATE", {"paths": third,
                                "detail": "ficheiro alterado por fora durante a pendência"})

        stg = eng / intent["staging"]
        missing = [rel for rel in intent["after"]
                   if not (stg / rel.replace("/", "__")).is_file()
                   and digest(eng / rel) != intent["after"][rel]]
        if missing:
            raise OperationError(
                "staging incompleto e alvo por publicar", "STAGING_INCOMPLETE",
                {"paths": missing})

        for rel in sorted(intent["after"]):
            if digest(eng / rel) == intent["after"][rel]:
                continue                      # já publicado: roll-forward é no-op
            src = stg / rel.replace("/", "__")
            dst = eng / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            _atomic_write(dst, src.read_text(encoding="utf-8"))

        receipt = _finish(eng, intent, sorted(intent["after"]))
        return dict(receipt, result="rolled_forward")
    finally:
        release(eng, ident)


# --------------------------------------------------------------------------- CLI

def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description="coordenador de operações")
    ap.add_argument("command", choices=["status", "recover"])
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    eng = Path(a.engagement)
    if not eng.is_dir():
        eng = Path("projects") / a.engagement
    if not eng.is_dir():
        print("engagement não encontrado: {}".format(a.engagement), file=sys.stderr)
        return 2
    try:
        out = status(eng) if a.command == "status" else recover(eng)
    except OperationError as exc:
        out = exc.as_dict()
        print(json.dumps(out, ensure_ascii=False, indent=2) if a.json else out["error"],
              file=sys.stderr)
        return 1
    print(json.dumps(out, ensure_ascii=False, indent=2) if a.json
          else "\n".join("{:18} {}".format(k, v) for k, v in out.items()))
    return 0 if out.get("state", CLEAN) == CLEAN or a.command == "recover" else 1


if __name__ == "__main__":
    sys.exit(main())
