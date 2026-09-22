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

O QUE ESTE MÓDULO NÃO FAZ
    Não lê a Shared Understanding. O contexto é construído a partir do grafo, que em P3
    ainda não tem conhecimento real — ligar as autoridades de negócio é P4/P6. As funções
    de orçamento são puras e testadas por si; o que falta é a fonte, não o mecanismo.
"""
from __future__ import annotations

import hashlib
import json
import runpy
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_G = runpy.run_path(str(_HERE / "graph.py"))
_O = runpy.run_path(str(_HERE / "operation.py"))

# Autoridades cujo digest entra no snapshot. Ausência é um estado, não um erro.
AUTHORITIES = ("_state.json", "shared-understanding.md", "answers.md", "decisions.md",
               "context.json", "enquadramento.md")

DEFAULT_BUDGET = 40


# ------------------------------------------------------------------- snapshot

def snapshot(eng: Path) -> dict:
    """Digests das autoridades + revisão do conjunto. É a base que a mutação recompara."""
    eng = Path(eng)
    digests = {rel: _O["digest"](eng / rel) for rel in AUTHORITIES}
    body = json.dumps(digests, sort_keys=True, ensure_ascii=False)
    return {"authorities": digests,
            "revision": hashlib.sha256(body.encode("utf-8")).hexdigest()}


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

    # 2. recuperação pendente — antes de qualquer leitura de conteúdo
    op = _O["status"](eng)
    if op["state"] != _O["CLEAN"]:
        limitations.append({"code": op["state"].upper(), "detail": op["detail"],
                            "recovery": op.get("recovery", "")})
        return {"ready": False, "engagement": identity, "operation": op,
                "graph": {}, "snapshot": {}, "context": {},
                "limitations": limitations,
                "detail": "bootstrap parou no passo 2: recuperação é acção separada"}

    # 3. snapshot
    snap = snapshot(eng)

    # 4. autoridades / grafo
    st = _G["read"](eng)
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

def main(argv=None) -> int:
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
