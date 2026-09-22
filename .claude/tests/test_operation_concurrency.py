# -*- coding: utf-8 -*-
"""W09-W12 — a exclusão exercida, não simulada (P7.5, W7).

`test_operation_recovery.py` já cobre W01-W08, e passava. Passava porque nunca corria a
corrida: escrevia um lock com um pid morto e chamava `acquire` **uma vez**. Isso exerce o
ramo, não a concorrência.

Medido com processos reais barrados no mesmo instante sobre um lock abandonado, a exclusão
por existência do ficheiro dava **seis donos do mesmo engagement em seis processos, doze
corridas em doze** — todos liam o mesmo dono morto, todos o davam por recuperável, todos
escreviam o seu por cima. A jusante custava escrita confirmada e perdida em sete de oito
corridas: quatro recibos `committed`, o ficheiro com um, e `BASE_CHANGED` calado porque
todos tinham lido a mesma base dentro de um lock que não excluía.

Por isso estes casos usam processos a sério, com barreira. Um teste de exclusão num só
processo prova o ramo e não prova a exclusão.

Mutantes escritos antes destes testes, como no W5 e no W6."""
import json
import multiprocessing as mp
import os
import runpy
import tempfile
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OP_PY = ROOT / "library" / "kernel" / "tools" / "operation.py"
O = runpy.run_path(str(OP_PY))

ALVO = "shared-understanding.md"
PROCESSOS = 5


def _eng(tmp, dono_morto=True, conteudo=None):
    eng = Path(tmp) / "eng"
    (eng / "_ops").mkdir(parents=True, exist_ok=True)
    if conteudo is not None:
        (eng / ALVO).write_text(conteudo, encoding="utf-8", newline="\n")
    if dono_morto:
        O["_lock_path"](eng).write_text(
            json.dumps({"pid": 999_999, "started": "", "engagement": str(eng.resolve())}),
            encoding="utf-8")
    return eng


# --- os trabalhadores correm noutro processo: têm de ser de topo, para o fork os achar ---

def _so_agarra(eng, barreira, fila):
    op = runpy.run_path(str(OP_PY))
    while not Path(barreira).exists():
        time.sleep(0.001)
    try:
        ident = op["acquire"](Path(eng))
        fila.put(("dono", os.getpid(), bool(ident.get("recovered_from"))))
    except Exception as exc:                                        # noqa: BLE001
        fila.put(("recusado", os.getpid(), getattr(exc, "code", type(exc).__name__)))


def _escreve(eng, barreira, marca, fila):
    op = runpy.run_path(str(OP_PY))
    eng = Path(eng)
    base = op["digest"](eng / ALVO)
    while not Path(barreira).exists():
        time.sleep(0.001)
    try:
        op["run"](eng, "op-" + marca, {ALVO: "linha de " + marca + "\n"},
                  expected={ALVO: base})
        fila.put(("commit", marca, ""))
    except Exception as exc:                                        # noqa: BLE001
        fila.put(("recusado", marca, getattr(exc, "code", type(exc).__name__)))


def _corrida(alvo, eng, extra=lambda i: ()):
    """Lança `PROCESSOS` barrados no mesmo instante e devolve o que cada um disse."""
    ctx = mp.get_context("fork")
    barreira = Path(eng).parent / "go"
    fila = ctx.Queue()
    ps = [ctx.Process(target=alvo, args=(str(eng), str(barreira)) + extra(i) + (fila,))
          for i in range(PROCESSOS)]
    for p in ps:
        p.start()
    time.sleep(0.2)
    barreira.write_text("go", encoding="utf-8")
    for p in ps:
        p.join(60)
    return [fila.get() for _ in range(PROCESSOS)]


class _OsQueTrocaOInode:
    """`os` com um degrau: a primeira abertura do lock é seguida da troca do ficheiro.

    É a interleaving que a verificação de inode existe para apanhar, e que nenhuma barreira
    entre processos consegue marcar: quem largou apaga o ficheiro e um terceiro cria o seu,
    entre o `os.open` e o `os.fstat` de quem está a chegar. Aqui é forçada.
    """

    def __init__(self, real, lp):
        self._real, self._lp, self.usado = real, str(lp), False

    def __getattr__(self, nome):
        return getattr(self._real, nome)

    def open(self, caminho, *a, **k):
        fd = self._real.open(caminho, *a, **k)
        if str(caminho) == self._lp and not self.usado:
            self.usado = True
            self._real.unlink(caminho)                  # quem largou apagou o ficheiro
            outro = self._real.open(caminho, self._real.O_CREAT | self._real.O_RDWR, 0o600)
            self._real.close(outro)                     # outro chegou e criou o seu
        return fd


class W09_ExclusaoComProcessosASerio(unittest.TestCase):
    """O caso que os W01-W08 não corriam: N processos sobre o MESMO lock abandonado."""

    def test_only_one_process_ends_up_owning_a_stale_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = _corrida(_so_agarra, _eng(tmp))
        donos = [o for o in out if o[0] == "dono"]
        self.assertEqual(len(donos), 1,
                         "%d processos ficaram donos do mesmo engagement" % len(donos))

    def test_the_losers_are_refused_with_a_reason_never_in_silence(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = _corrida(_so_agarra, _eng(tmp))
        recusas = [o[2] for o in out if o[0] == "recusado"]
        self.assertEqual(len(recusas), PROCESSOS - 1)
        for c in recusas:
            self.assertIn(c, ("LOCK_ACTIVE", "LOCK_UNDETERMINED", "LOCK_CONTENDED"),
                          "recusa sem código de exclusão: " + c)

    def test_the_one_owner_records_that_it_recovered_a_dead_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = _corrida(_so_agarra, _eng(tmp))
        donos = [o for o in out if o[0] == "dono"]
        self.assertTrue(donos[0][2],
                        "tomou um lock abandonado sem deixar registo de o ter feito")


class W10_EscritaConfirmadaEPerdida(unittest.TestCase):
    """O dano a jusante. `BASE_CHANGED` só vale se a base for lida sob exclusão real."""

    def test_a_confirmed_write_is_never_overwritten_by_another_confirmed_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, conteudo="base comum\n")
            out = _corrida(_escreve, eng, extra=lambda i: ("w%d" % i,))
            final = (eng / ALVO).read_text(encoding="utf-8").strip()
        commits = [o[1] for o in out if o[0] == "commit"]
        vencedor = final.replace("linha de ", "")
        perdidas = [c for c in commits if c != vencedor]
        self.assertEqual(perdidas, [],
                         "declarou sucesso a %s e o ficheiro ficou com %r"
                         % (perdidas, final))

    def test_the_writers_that_lost_the_race_are_told_the_base_moved(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = _corrida(_escreve, _eng(tmp, conteudo="base comum\n"),
                           extra=lambda i: ("w%d" % i,))
        codigos = {o[2] for o in out if o[0] == "recusado"}
        self.assertEqual(len([o for o in out if o[0] == "commit"]), 1)
        self.assertTrue(codigos <= {"BASE_CHANGED", "LOCK_ACTIVE", "LOCK_UNDETERMINED",
                                    "LOCK_CONTENDED", "PENDING_EXISTS"},
                        "recusa por um motivo que não é o da corrida: " + str(codigos))

    def test_one_receipt_per_write_that_actually_happened(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, conteudo="base comum\n")
            out = _corrida(_escreve, eng, extra=lambda i: ("w%d" % i,))
            recibos = sorted(p.stem for p in (eng / "_ops" / "receipts").glob("*.json"))
        commits = sorted("op-" + o[1] for o in out if o[0] == "commit")
        self.assertEqual(recibos, commits,
                         "há recibos a mais ou a menos para as escritas que aconteceram")


class W11_OLockEOInode(unittest.TestCase):
    """Quem liberta apaga o ficheiro. Entre o `unlink` de um e o `open` de outro, o
    caminho pode já não ser o mesmo inode — e um lock agarrado a um órfão não exclui nada."""

    def test_the_path_still_points_at_the_inode_the_lock_is_held_on(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            ident = O["acquire"](eng)
            try:
                lp = O["_lock_path"](eng)
                fd = O["_HELD"].get(str(lp))
                self.assertIsNotNone(fd, "o descritor do lock não ficou guardado")
                self.assertEqual(os.fstat(fd).st_ino, os.stat(str(lp)).st_ino,
                                 "o ficheiro de lock já não é o inode que está trancado")
            finally:
                O["release"](eng, ident)

    def test_releasing_removes_the_file_and_drops_the_descriptor(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            lp = O["_lock_path"](eng)
            ident = O["acquire"](eng)
            O["release"](eng, ident)
            self.assertFalse(lp.exists())
            self.assertNotIn(str(lp), O["_HELD"], "o descritor ficou agarrado depois de largar")

    def test_the_file_is_gone_before_the_lock_is_let_go(self):
        """A ordem importa: largar primeiro deixava outro entrar e depois apagava-lhe o
        ficheiro por baixo."""
        fonte = OP_PY.read_text(encoding="utf-8")
        corpo = fonte[fonte.index("def release(eng: Path, ident: dict)"):]
        corpo = corpo[:corpo.index("\n\n\n")]
        self.assertLess(corpo.index("lp.unlink()"), corpo.index("_unlock(fd)"),
                        "`release` larga o lock antes de apagar o ficheiro")

    def test_a_lock_held_on_an_orphan_inode_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            lp = O["_lock_path"](eng)
            g = O["_flock_fd"].__globals__
            real = g["os"]
            degrau = _OsQueTrocaOInode(real, lp)
            g["os"] = degrau
            try:
                ident = O["acquire"](eng)
            finally:
                g["os"] = real
            try:
                self.assertTrue(degrau.usado, "o degrau não chegou a ser exercido")
                fd = O["_HELD"][str(lp)]
                self.assertEqual(os.fstat(fd).st_ino, os.stat(str(lp)).st_ino,
                                 "ficou com o lock agarrado a um inode órfão: o ficheiro "
                                 "que o próximo a chegar abre já é outro, e tranca-o também")
            finally:
                O["release"](eng, ident)

    def test_a_second_acquire_in_the_same_process_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            ident = O["acquire"](eng)
            try:
                with self.assertRaises(O["OperationError"]) as ctx:
                    O["acquire"](eng)
                self.assertEqual(ctx.exception.code, "LOCK_ACTIVE")
            finally:
                O["release"](eng, ident)


class W12_ORegistoDeQuemTem(unittest.TestCase):
    """Ter o `flock` prova que nenhum escritor desta versão lá está. Não prova que não lá
    está um de uma versão anterior, que nunca chamou `flock`."""

    def test_a_live_owner_in_the_record_is_refused_even_with_the_kernel_lock_free(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            vivo = {"pid": os.getpid(), "started": O["_proc_started"](os.getpid()),
                    "engagement": str(eng.resolve())}
            O["_lock_path"](eng).write_text(json.dumps(vivo), encoding="utf-8")
            with self.assertRaises(O["OperationError"]) as ctx:
                O["acquire"](eng)
        self.assertEqual(ctx.exception.code, "LOCK_ACTIVE")
        self.assertEqual(ctx.exception.detail["holder"]["pid"], os.getpid())

    def test_a_dead_owner_is_recovered_and_the_record_says_who_it_was(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp)
            ident = O["acquire"](eng)
            try:
                self.assertEqual(ident["recovered_from"]["pid"], 999_999)
            finally:
                O["release"](eng, ident)

    def test_an_undetermined_owner_is_not_removed_by_a_blind_timeout(self):
        alvo = O["_refuse_if_foreign"].__globals__
        antes = alvo["_alive"]
        alvo["_alive"] = lambda pid, started: None
        try:
            with tempfile.TemporaryDirectory() as tmp:
                eng = _eng(tmp)
                lp = O["_lock_path"](eng)
                with self.assertRaises(O["OperationError"]) as ctx:
                    O["acquire"](eng)
                self.assertEqual(ctx.exception.code, "LOCK_UNDETERMINED")
                self.assertTrue(lp.exists(), "removeu um lock de posse indeterminada")
        finally:
            alvo["_alive"] = antes

    def test_an_unreadable_lock_is_refused_and_kept(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            lp = O["_lock_path"](eng)
            lp.write_text("isto não é json", encoding="utf-8")
            with self.assertRaises(O["OperationError"]) as ctx:
                O["acquire"](eng)
            self.assertEqual(ctx.exception.code, "LOCK_UNREADABLE")
            self.assertTrue(lp.exists(), "removeu um lock que não leu")

    def test_an_empty_lock_file_is_not_an_unreadable_one(self):
        """Recém-criado é vazio. Vazio não é ilegível, e não é um dono morto."""
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            ident = O["acquire"](eng)
            try:
                self.assertNotIn("recovered_from", ident,
                                 "um lock vazio foi contado como dono abandonado")
            finally:
                O["release"](eng, ident)


class W13_OQueOEstadoDeclara(unittest.TestCase):
    """Quem lê um estado tem de poder saber sob que garantia ele foi produzido."""

    def test_a_clean_state_names_the_exclusion_in_use(self):
        with tempfile.TemporaryDirectory() as tmp:
            st = O["status"](_eng(tmp, dono_morto=False))
        self.assertEqual(st["state"], O["CLEAN"])
        self.assertIn(st.get("exclusion"), ("flock", "create-exclusive"))

    def test_the_exclusion_matches_what_the_platform_actually_offers(self):
        esperado = "flock" if O["fcntl"] else "create-exclusive"
        self.assertEqual(O["EXCLUSION"], esperado)

    def test_a_pending_state_names_it_too(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False, conteudo="x\n")
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-1", "request_hash": "h",
                 "owner": {}, "before": {}, "after": {ALVO: "f" * 64},
                 "staging": "_ops/staging/op-1"}))
            st = O["status"](eng)
        self.assertEqual(st["state"], O["PENDING_OPERATION"])
        self.assertEqual(st["exclusion"], O["EXCLUSION"])

    def test_the_new_field_does_not_open_or_close_a_gate_by_itself(self):
        with tempfile.TemporaryDirectory() as tmp:
            eng = _eng(tmp, dono_morto=False)
            self.assertTrue(O["gate_open"](eng))
            O["_atomic_write"](O["pending_path"](eng), json.dumps(
                {"intent_version": 1, "operation_id": "op-1", "request_hash": "h",
                 "owner": {}, "before": {}, "after": {}, "staging": "_ops/staging/op-1"}))
            self.assertFalse(O["gate_open"](eng))


if __name__ == "__main__":
    unittest.main(verbosity=1)
