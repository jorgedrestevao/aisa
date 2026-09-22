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

MODO LEGACY
    Só um grafo GENUINAMENTE ausente autoriza modo legacy, e é declarado. Grafo corrompido,
    par incoerente, schema não suportado ou ilegível NÃO autorizam fallback silencioso —
    é a distinção que o B07 exige e que `graph.read()` já produz.

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


def items_from_graph(nodes: list[dict]) -> list[dict]:
    """Itens de contexto a partir do grafo. Em P3 o grafo ainda não tem conhecimento real."""
    out = []
    for n in nodes:
        props = n.get("props") or {}
        prov = n.get("provenance") or {}
        out.append({"id": n.get("id"), "text": props.get("text", ""),
                    "criticality": "critical" if props.get("state") in ("Unknown", "Conflicted",
                                                                        "Risky") else "noncritical",
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
        limitations.append({"code": "LEGACY_MODE",
                            "detail": "projecto sem grafo — modo legacy DECLARADO, "
                                      "não apresentado como migrado"})
    elif not usable:
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
    """Um gate exige bootstrap pronto E contexto completo (B6).

    Contexto parcial NUNCA autoriza declarar que não há bloqueios — é a razão de esta
    função não olhar só para `ready`."""
    return bool(boot.get("ready")) and bool(boot.get("context", {}).get("complete"))


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
