# -*- coding: utf-8 -*-
"""Bootstrap técnico — a leitura que precede qualquer efeito (contrato B5).

    python library/kernel/tools/bootstrap.py --engagement <slug> [--json]

Stdlib apenas (ADR-001).

READ-ONLY, SEM EXCEPÇÃO
    Não cria grafo, não renova timestamps, não marca nada resolvido, não repara prosa.
    Inicialização e migração são operações explícitas, de outra via. Um bootstrap que
    reparasse tornaria impossível distinguir «estava bem» de «foi consertado».

ORDEM (B5) — e a ordem é a garantia
    1. identificar engagement
    2. detectar necessidade de recuperação
    3. snapshot consistente
    4. validar autoridades / grafo
    5. construir contexto
    6. devolver revisão, digests e LIMITAÇÕES
    7. só então iniciar operação

    Pendência detectada no passo 2 fecha tudo o que vem a seguir: `ready` é falso e o
    chamador não tem por onde avançar um gate. A recuperação é acção separada
    (`operation.py recover`), registada, nunca um efeito lateral de ler.

MODO LEGACY — DEIXOU DE SER UM CAMINHO (P7.5 §2)
    Ausência de grafo era declarada e seguia: `ready=True` com uma limitação escrita. Desde
    a decisão de tornar o grafo obrigatório, BLOQUEIA, com a acção que a desbloqueia
    nomeada. A limitação continua declarada e continua a não se apresentar como migrada; o
    que deixou de existir é o seguir em frente.

    Um engagement novo não é legado: nasce com grafo (`migrate.py init`, corrido pelo
    `/start`). Ausência passou a significar uma coisa só — legado por migrar.

    A distinção do B07 mantém-se intacta e continua a importar: grafo corrompido, par
    incoerente, schema não suportado ou ilegível NÃO são ausência, e o bloqueio que
    produzem diz outra coisa — `migrate` não é a acção que os resolve.

AUTORIDADE — LÊ-SE A SU, E LÊ-SE PARA COMPARAR (F05/F08, auditoria de 212cdc6)

    Este módulo declarava que NÃO lia a Shared Understanding: em P3 o grafo ainda não
    tinha conhecimento real e o contexto saía só dele. Isso deixou de poder ser verdade
    quando o grafo passou a espelhar a SU.

    O defeito medido: a projecção bloqueava sobre `MIRROR_DRIFT` e o bootstrap devolvia
    `ready` sem uma única limitação, para o MESMO estado. E quem confia no bootstrap —
    `resolve.apply`, o guarda de escrita, os gates — ficava com a resposta que não aplica
    a regra. Duas respostas incompatíveis não são uma tolerância: são um sítio por onde
    passa o que o outro recusa.

    Por isso lê-se a SU aqui, e lê-se para uma coisa só: comparar o espelho com a
    autoridade, com a MESMA regra que a projecção aplica — `state`, `criticidade` e
    `resolved` divergentes bloqueiam; texto divergente informa. O contexto continua a
    construir-se a partir do grafo.

    E uma linha da autoridade SEM nó nenhum também bloqueia. Reconstruir a partir do grafo
    não vê o que a SU tem a mais, e um contexto que não sabe o que lhe falta dá-se por
    completo. Medido nos dois pilotos antes de o tornar bloqueante: 117/117 e 108/108
    espelhadas, zero desvio.
"""
from __future__ import annotations

import hashlib
import json
import runpy
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_D = runpy.run_path(str(_HERE / "dashboard.py"))
_G = runpy.run_path(str(_HERE / "graph.py"))
_O = runpy.run_path(str(_HERE / "operation.py"))

# Autoridades cujo digest entra no snapshot. Ausência é um estado, não um erro.
SU_FILE = "shared-understanding.md"
AUTHORITIES = ("_state.json", "shared-understanding.md", "answers.md", "decisions.md",
               "context.json", "enquadramento.md")

DEFAULT_BUDGET = 40


# ------------------------------------------------------------------- snapshot

def snapshot(eng: Path) -> dict:
    """Digests das autoridades, revisão do conjunto, E as linhas da SU dessa leitura.

    As linhas vêm aqui de propósito. A validação da revisão (`consistent_read`) cobria
    pendência, snapshot e grafo — e depois a comparação autoridade/espelho reabria a SU por
    sua conta, fora da janela validada. Validar uma parte da leitura e concluir sobre o todo
    é a mesma falha que o F02 fechou um nível acima.

    Quem já leu não obriga o próximo a reabrir: as linhas saem com o digest que as
    acompanha, e quem as consome está, por construção, na revisão que foi validada.
    """
    eng = Path(eng)
    digests, linhas = {}, []
    for rel in AUTHORITIES:
        caminho = eng / rel
        try:
            bruto = caminho.read_bytes()
        except OSError:
            digests[rel] = ""
            continue
        digests[rel] = hashlib.sha256(bruto).hexdigest()
        if rel == SU_FILE:
            try:
                _h, linhas, _s, _d = _D["parse_su"](bruto.decode("utf-8"))
            except Exception:                                   # noqa: BLE001
                linhas = []
    body = json.dumps(digests, sort_keys=True, ensure_ascii=False)
    return {"authorities": digests, "rows": linhas,
            "revision": hashlib.sha256(body.encode("utf-8")).hexdigest()}


def authority_check(rows, nodes: list) -> tuple:
    """`(autoridade, linhas sem nó, desvio)` — a comparação, sem decidir nada.

    Recebe as LINHAS, não o caminho: reabrir a SU aqui punha a comparação fora da revisão
    que `consistent_read` validou, e era possível comparar o espelho contra uma SU e
    concluir sobre outra. Quem chama passa o que leu dentro da janela.

    Separada de propósito: quem decide o que cada caso vale é o `bootstrap`, e quem quiser
    ver o mesmo sem bloquear (a projecção, um relatório) chama isto.
    """
    linhas = rows or []
    autoridade = _G["authority_from_rows"](linhas)
    espelhadas = {(n.get("provenance") or {}).get("mirror_of") for n in nodes}
    sem_no = sorted(k for k in autoridade if k not in espelhadas)
    return autoridade, sem_no, _G["drift"](nodes, autoridade)


# -------------------------------------------------------------------- contexto

def build_context(items: list[dict], budget: int = DEFAULT_BUDGET) -> dict:
    """Contexto com orçamento, proveniência e parcialidade DECLARADA (B5, B6).

    `items`: `{id, criticality, text, provenance, depends_on}`.

    Duas regras que não se negoceiam:
      - **Truncar nunca é silencioso** (B05). O que não cabe sai nomeado em `omitted`, e
        `complete` fica falso. Um excerto não autoriza concluir que não há bloqueios.
      - **Premissa quebrada limita a conclusão** (B06). Um item cuja dependência não está
        no conjunto entra com `premise_broken`; quem o consome não pode concluir sobre ele.

    Ordem de prioridade: críticos primeiro, depois por id. NÃO por recência — o contrato
    diz expressamente que a prioridade não depende só de recência."""
    known = {i.get("id") for i in items}
    ranked = sorted(items, key=lambda i: (0 if i.get("criticality") == "critical" else 1,
                                          str(i.get("id", ""))))
    kept, omitted = ranked[:budget], ranked[budget:]

    included = []
    for i in kept:
        entry = {"id": i.get("id"), "criticality": i.get("criticality", "noncritical"),
                 "text": i.get("text", ""), "provenance": i.get("provenance", {})}
        broken = [d for d in (i.get("depends_on") or []) if d not in known]
        if broken:
            entry["premise_broken"] = broken
            entry["conclusion"] = "limitada — dependência material em falta"
        elif any(d not in {k.get("id") for k in kept} for d in (i.get("depends_on") or [])):
            entry["premise_omitted"] = [d for d in i["depends_on"]
                                        if d not in {k.get("id") for k in kept}]
            entry["conclusion"] = "limitada — dependência fora do orçamento"
        included.append(entry)

    return {"included": included,
            "omitted": [{"id": i.get("id"), "criticality": i.get("criticality", "noncritical")}
                        for i in omitted],
            "omitted_critical": [i.get("id") for i in omitted
                                 if i.get("criticality") == "critical"],
            "complete": not omitted,
            "budget": budget,
            "note": ("contexto parcial — NÃO permite concluir que não há bloqueios"
                     if omitted else "")}


# Grafias aceites da coluna `criticidade` da SU para «isto bloqueia».
CRITICAS_DECLARADAS = {"critical", "critica", "crítica", "alta", "high"}


def items_from_graph(nodes: list[dict]) -> list[dict]:
    """Itens de contexto a partir do grafo.

    `criticality` decide a prioridade no orçamento, e uma linha **já resolvida** não é um
    bloqueio: a pergunta foi respondida e a resposta vive na linha sucessora. Ordená-la como
    crítica gastava orçamento a repetir história e empurrava para fora do contexto perguntas
    que continuam abertas — medido no piloto de tickets: 4 dos 40 lugares ocupados por
    `CF-001`, `CF-002`, `U-006` e `U-013`, todas resolvidas.

    A linha resolvida NÃO é descartada: continua no conjunto, como não-crítica. Descartá-la
    apagaria proveniência, e o grafo é aditivo por contrato."""
    out = []
    for n in nodes:
        props = n.get("props") or {}
        prov = n.get("provenance") or {}
        aberta = props.get("state") in ("Unknown", "Conflicted", "Risky")
        resolvida = bool(props.get("resolved"))
        # `criticidade` vem da coluna que a SU declara; sem ela, uma linha aberta conta
        # como critica, que e o lado seguro da duvida. Com ela, o que bloqueia e o que o
        # engagement DIZ que bloqueia — no piloto de tickets, 15 e nao 50.
        declarada = str(props.get("criticidade") or "").strip().lower()
        if declarada:
            critica = aberta and not resolvida and declarada in CRITICAS_DECLARADAS
        else:
            critica = aberta and not resolvida
        out.append({"id": n.get("id"), "text": props.get("text", ""),
                    "criticality": "critical" if critica else "noncritical",
                    "criticidade": props.get("criticidade", ""),
                    "resolved": resolvida,
                    "provenance": prov,
                    "depends_on": [e for e in (props.get("depends_on") or [])]})
    return out


READ_TRIES = 3


def _state_marker(eng: Path) -> tuple:
    """O que tem de estar igual no fim da leitura e no princípio.

    Pendência sozinha não chega, e é essa a armadilha: uma escrita que COMEÇA e ACABA
    durante a leitura não deixa pendência nenhuma para a segunda consulta encontrar. O que
    a apanha é o snapshot das autoridades — que muda — e a revisão do grafo.
    """
    op = _O["status"](eng)
    snap = snapshot(eng)
    st = _G["read"](eng)
    return op, snap, st


def consistent_read(eng: Path, tries: int = READ_TRIES):
    """`(op, snapshot, grafo, tentativas)` de UMA revisão — ou o que impediu.

    O bootstrap verificava a pendência e só depois lia o conteúdo, sem exclusão. Entre as
    duas coisas cabia uma publicação inteira, e o resultado saía com autoridades de
    revisões diferentes a dizer `ready`. A exclusão dos escritores não protege este leitor:
    ela impede dois escritores, não um escritor e um leitor.

    Aqui não se toma o lock — um leitor que bloqueia escritores serializa o sistema inteiro,
    e `resolve.apply` chama isto antes de escrever. Lê-se de forma optimista e valida-se: o
    marcador de estado antes e depois. Diferentes, repete-se; ao fim de `tries`, declara-se
    — nunca se declara pronto sobre um alvo em movimento.
    """
    ultimo = None
    for tentativa in range(1, tries + 1):
        antes = _state_marker(eng)
        op, snap, st = antes
        depois = _state_marker(eng)
        ultimo = (op, snap, st)
        if (antes[0]["state"] == depois[0]["state"]
                and antes[1].get("revision") == depois[1].get("revision")
                and antes[2].get("revision", "") == depois[2].get("revision", "")):
            return ultimo[0], ultimo[1], ultimo[2], tentativa, None
        # Uma escrita aconteceu durante a leitura. O que se leu vale para nada; repete-se.
    return ultimo[0], ultimo[1], ultimo[2], tries, {
        "code": "CONCURRENT_WRITE", "blocking": True,
        "detail": "o estado mudou durante a leitura, {} vez(es) seguidas".format(tries),
        "recovery": "repetir quando o escritor terminar; se persistir, `operation.py "
                    "status --engagement <slug>` diz quem está a escrever",
        "note": "ler sobre uma publicação a meio decide sobre estado misto"}


# ------------------------------------------------------------------- bootstrap

def bootstrap(eng: Path, budget: int = DEFAULT_BUDGET) -> dict:
    """A leitura completa, pela ordem do contrato. NÃO escreve nada."""
    eng = Path(eng)
    limitations: list[dict] = []

    # 1. identidade
    try:
        resolved = str(eng.resolve())
    except OSError as exc:
        return {"ready": False, "engagement": {"path": str(eng)},
                "limitations": [{"code": "ENGAGEMENT_UNRESOLVABLE", "detail": str(exc)}]}
    if not eng.is_dir():
        return {"ready": False, "engagement": {"path": str(eng), "resolved": resolved},
                "limitations": [{"code": "ENGAGEMENT_MISSING",
                                 "detail": "não existe: {}".format(resolved)}]}
    identity = {"path": str(eng), "resolved": resolved, "slug": eng.name}

    # 2-4. pendência, snapshot e grafo, TODOS da mesma revisão (F02)
    op, snap, st, tentativas, instavel = consistent_read(eng)
    if instavel:
        limitations.append(instavel)
        return {"ready": False, "engagement": identity, "operation": op,
                "graph": {"status": st.get("status", ""),
                          "revision": st.get("revision", "")},
                "snapshot": snap, "context": {}, "limitations": limitations,
                "read_attempts": tentativas,
                "detail": "bootstrap parou: o estado mexeu-se debaixo da leitura"}
    if op["state"] != _O["CLEAN"]:
        limitations.append({"code": op["state"].upper(), "detail": op["detail"],
                            "recovery": op.get("recovery", "")})
        return {"ready": False, "engagement": identity, "operation": op,
                "graph": {}, "snapshot": {}, "context": {},
                "limitations": limitations,
                "detail": "bootstrap parou no passo 2: recuperação é acção separada"}

    legacy = st["status"] == _G["ABSENT"]
    graph_info = {"status": st["status"], "legacy_mode": legacy,
                  "revision": st.get("revision", ""),
                  "nodes": len(st.get("nodes", [])), "edges": len(st.get("edges", []))}
    usable = st["status"] == _G["OK"]

    if legacy:
        # P7.5 §2: ausência de grafo bloqueia. A limitação continua DECLARADA e continua a
        # não se apresentar como migrada — o que deixou de existir é o seguir em frente.
        limitations.append({"code": "LEGACY_MODE", "blocking": True,
                            "detail": "projecto sem grafo — modo legacy DECLARADO, "
                                      "não apresentado como migrado",
                            "recovery": "python library/kernel/tools/migrate.py apply "
                                        "--engagement <slug>  (engagement acabado de "
                                        "criar: `migrate.py init`)"})
        return {"ready": False, "engagement": identity, "operation": op,
                "graph": graph_info, "snapshot": snap, "context": {},
                "limitations": limitations}
    if not usable:
        # B07: corrupção não autoriza fallback silencioso
        limitations.append({"code": st["status"].upper(), "detail": st["detail"],
                            "blocking": True,
                            "note": "grafo inutilizável — NÃO é modo legacy"})
        return {"ready": False, "engagement": identity, "operation": op,
                "graph": graph_info, "snapshot": snap, "context": {},
                "limitations": limitations}
    else:
        problems = _G["validate"](st["nodes"], st["edges"])
        if problems:
            limitations.append({"code": "GRAPH_INTEGRITY", "blocking": True,
                                "detail": "{} problema(s) de integridade".format(len(problems)),
                                "problems": problems})
            return {"ready": False, "engagement": identity, "operation": op,
                    "graph": graph_info, "snapshot": snap, "context": {},
                    "limitations": limitations}

    # 4b. autoridade vs espelho — a MESMA regra, no mesmo sítio para toda a gente
    autoridade, sem_no, desvio = authority_check(snap.get("rows"), st.get("nodes", []))
    bloqueante = [d for d in desvio
                  if d["code"] in ("MIRROR_DRIFT", "MIRROR_SOURCE_MISSING")]
    if bloqueante:
        primeiro = bloqueante[0]
        limitations.append({
            "code": "AUTHORITY_DRIFT", "blocking": True,
            "detail": "{} linha(s) em que o grafo e a autoridade discordam".format(
                len(bloqueante)),
            "first": primeiro,
            "recovery": "reconciliar o grafo com a SU — a SU prevalece",
            "note": "campos materiais; divergência só de texto não bloqueia"})
        return {"ready": False, "engagement": identity, "operation": op,
                "graph": graph_info, "snapshot": snap, "context": {},
                "limitations": limitations, "drift": desvio}
    if sem_no:
        limitations.append({
            "code": "AUTHORITY_UNMIRRORED", "blocking": True,
            "detail": "{} linha(s) da autoridade sem representação no grafo".format(
                len(sem_no)),
            "rows": [k.split(":", 1)[-1] for k in sem_no[:20]],
            "recovery": "python library/kernel/tools/migrate.py apply --engagement <slug>",
            "note": "o contexto vem do grafo; o que não está lá não se declara completo"})
        return {"ready": False, "engagement": identity, "operation": op,
                "graph": graph_info, "snapshot": snap, "context": {},
                "limitations": limitations, "drift": desvio}

    # 5. contexto
    ctx = build_context(items_from_graph(st.get("nodes", [])), budget)
    if not ctx["complete"]:
        limitations.append({"code": "CONTEXT_TRUNCATED",
                            "detail": "{} item(ns) omitido(s); {} crítico(s)".format(
                                len(ctx["omitted"]), len(ctx["omitted_critical"])),
                            "omitted_critical": ctx["omitted_critical"]})
    broken = [e["id"] for e in ctx["included"] if e.get("premise_broken")]
    if broken:
        limitations.append({"code": "PREMISE_BROKEN", "ids": broken,
                            "detail": "conclusões dependentes ficam limitadas"})

    # 6. revisão, digests e limitações
    return {"ready": True, "engagement": identity, "operation": op, "graph": graph_info,
            "snapshot": snap, "context": ctx, "limitations": limitations}


def gate_open(boot: dict) -> bool:
    """Um gate exige bootstrap pronto E nenhum item crítico fora do contexto (B6).

    MUDANÇA DE CONTRATO (2026-09-22, autorizada pelo operador; `ACCEPTANCE.md` §3).

      antes: `ready AND context.complete` — qualquer omissão fechava o gate.
      agora: `ready AND context.omitted_critical == []`.

    Porquê. B05 diz que um excerto não autoriza declarar que **não há bloqueios**. Se
    nenhum item crítico ficou de fora, essa conclusão é legítima: o que bloqueia está
    todo no contexto, e o que ficou de fora não bloqueia. Exigir contexto completo era
    mais estrito do que o contrato pede, e tornava o gate impossível de abrir num
    engagement real — `DEFAULT_BUDGET` é 40 e os pilotos têm 117 e 108 linhas, logo
    `complete` seria sempre falso e nenhum comando avançaria de fase.

    O que NÃO muda, e é a garantia que se preserva: a truncagem continua declarada
    (`complete` falso, `omitted` nomeado, `CONTEXT_TRUNCATED` nas limitações), e **um
    crítico omitido continua a fechar o gate**. O que se deixou de fazer foi confundir
    «o contexto não traz tudo» com «o contexto não traz o que decide»."""
    if not boot.get("ready"):
        return False
    ctx = boot.get("context") or {}
    return not (ctx.get("omitted_critical") or [])


def switched(previous: dict | None, current: dict) -> bool:
    """Trocar de engagement invalida o contexto anterior (B03)."""
    if not previous:
        return False
    return (previous.get("engagement", {}).get("resolved")
            != current.get("engagement", {}).get("resolved"))


# --------------------------------------------------------------------------- CLI

def utf8_console() -> None:
    """A consola em UTF-8, venha ela como vier.

    Uma consola Windows fala cp1252 e este motor imprime portugues, setas e aspas
    angulares. Medido numa sessao real: `bootstrap.py --json` rebentou com
    UnicodeEncodeError em '\\u2192' — e o `migrate.py apply` que o guarda manda correr
    para recuperar rebentaria da mesma forma. `errors="replace"` porque um caracter
    perdido na consola e ruido; um processo morto a meio de uma recuperacao nao e."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main(argv=None) -> int:
    utf8_console()
    import argparse
    ap = argparse.ArgumentParser(description="bootstrap técnico (read-only)")
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--budget", type=int, default=DEFAULT_BUDGET)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    eng = Path(a.engagement)
    if not eng.is_dir():
        eng = Path("projects") / a.engagement
    boot = bootstrap(eng, a.budget)
    if a.json:
        print(json.dumps(boot, ensure_ascii=False, indent=2))
    else:
        print("ready              {}".format(boot["ready"]))
        print("engagement         {}".format(boot["engagement"].get("slug", "?")))
        print("graph              {} (legacy={})".format(
            boot.get("graph", {}).get("status", "?"),
            boot.get("graph", {}).get("legacy_mode", "?")))
        print("snapshot revision  {}".format(boot.get("snapshot", {}).get("revision", "")[:16]))
        print("context complete   {}".format(boot.get("context", {}).get("complete", "-")))
        for lim in boot["limitations"]:
            print("  ! {:22} {}".format(lim["code"], lim.get("detail", "")))
    return 0 if boot["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
