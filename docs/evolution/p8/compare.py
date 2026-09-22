#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""P8 — comparador determinístico de sessões reais (E01/E02/E03).

Porque é que isto existe
------------------------
`ACCEPTANCE.md` §1 é explícita: «Não basta criar um ficheiro com o mesmo nome ou imprimir
PASS.» E §5: «Não gerar a referência a partir das conclusões do candidato que será testado.»

Quem constrói o mecanismo não pode ser quem julga o resultado em prosa. Então o veredicto
sai daqui: um programa que compara o que a sessão reabriu (`report`) com o que os ficheiros
do engagement dizem (`truth`), e com o oráculo congelado antes de existir candidato.

O que este programa NÃO faz
---------------------------
- Não lê a sessão. O operador cola o que a sessão devolveu; isto compara.
- Não compara texto. Compara proposições, estados e locators, por id (§6).
- Não emite GO. Emite números. O GO é a leitura dos limiares que o próprio oráculo declara.
- Não inventa correspondência entre um item do oráculo e uma linha da SU. Essa
  correspondência é declarada pelo CANDIDATO; o que aqui se mede é se ela se sustenta.

Uso
---
    # antes de fechar a sessão, congelar a verdade daquele momento
    compare.py truth --engagement <slug> --checkpoint <nome> --out runs/<slug>/

    # depois de reabrir e colar a resposta da sessão
    compare.py check --truth runs/<slug>/<checkpoint>.truth.json \\
                     --report runs/<slug>/<checkpoint>.report.json

    # fuga entre engagements (§6: trocar entre dois e verificar que nada passa)
    compare.py leak --truth-other runs/<outro>/<cp>.truth.json \\
                    --report runs/<slug>/<cp>.report.json

    # extracção contra o oráculo independente (E02/E03)
    compare.py oracle --engagement <slug> --oracle docs/evolution/oracles/<slug>.oracle.json \\
                      --mapping runs/<slug>/mapping.json

    # o agregado de tudo o que está em runs/
    compare.py summary --runs runs/
"""
from __future__ import annotations

import argparse
import json
import runpy
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TOOLS = ROOT / "library" / "kernel" / "tools"

_P = runpy.run_path(str(TOOLS / "projection.py"))
_D = runpy.run_path(str(TOOLS / "dashboard.py"))
_B = runpy.run_path(str(TOOLS / "bootstrap.py"))
_G = runpy.run_path(str(TOOLS / "graph.py"))

# Severidades. Só as críticas fecham o gate de P8 — são as de `ACCEPTANCE.md` §2.
CRITICO = "critical"
AVISO = "warning"

CAMPOS_OBRIGATORIOS = ("engagement", "checkpoint", "phase", "facts", "open_questions",
                       "decisions", "coverage", "blockers", "next_step")

# Mecanismos que contam como reconstrucao pelo kernel. `ACCEPTANCE.md` §6 exige «apenas
# mecanismos oficiais do projeto»; com o grafo obrigatorio, ler `shared-understanding.md`
# a olho deixou de ser um deles.
MECANISMOS_KERNEL = ("bootstrap", "graph", "resume", "projection", "operation")


# ----------------------------------------------------------------- verdade do momento

def truth(eng_path: Path) -> dict:
    """Congela o que os ficheiros do engagement dizem AGORA.

    A autoridade é a SU, como sempre. Isto não a interpreta: copia ids, estados e o que o
    gate diz, para que a comparação mais tarde seja contra um alvo imóvel.
    """
    eng_path = Path(eng_path)          # `build_model` quer Path; um str rebenta lá dentro
    estado = _P["operational_state"](eng_path)
    modelo = _D["build_model"](eng_path, date.today()) if estado.get("ready") else {}
    linhas = (modelo.get("su") or {}).get("rows") or []

    por_estado: dict[str, list] = {}
    for r in linhas:
        if str(r.get("retired")) == "True":
            continue
        por_estado.setdefault(str(r.get("state") or ""), []).append({
            "id": r.get("id"),
            "state": r.get("state"),
            "criticidade": r.get("criticidade", ""),
            "swing_class": r.get("swing_class", ""),
            "resolved": str(r.get("resolved")) == "True",
            "resolved_to": r.get("resolved_to") or [],
            "support": (r.get("support") or "")[:200],
        })

    # As decisoes vivem em `status.decisions`, NAO no topo do modelo. Verificado contra a
    # saida real: `modelo.get("decisions")` devolve [] em silencio num engagement que tem
    # D-001 e D-002 escritas — um zero que se le como "nao ha decisoes" sem se queixar.
    decisoes = [d.get("id") for d in ((modelo.get("status") or {}).get("decisions") or [])
                if d.get("id")]

    # Por que caminho e que este engagement se reconstroi HOJE. Sem isto o comparador mede
    # ids recuperados e da GO — mesmo quando a recuperacao veio de ler a SU a moda antiga,
    # que e exactamente o que E01 nao pode dar por provado.
    boot = _B["bootstrap"](eng_path)
    codigos = [l.get("code") for l in boot.get("limitations", [])]
    itens = len((boot.get("context") or {}).get("items") or [])
    if not boot.get("ready"):
        modo = "blocked"
    elif "LEGACY_MODE" in codigos:
        modo = "legacy"
    else:
        modo = "graph"
    kernel = {"mode": modo, "context_items": itens, "limitations": codigos,
              "graph_status": _G["read"](eng_path).get("status", ""),
              "detail": {"legacy": "o grafo esta ausente: o bootstrap nao devolve contexto, "
                                   "logo nada do que a sessao recuperar veio por ele",
                         "blocked": "o bootstrap nao esta pronto",
                         "graph": ""}[modo]}
    return {
        "engagement": Path(eng_path).name,
        "phase": estado.get("phase", ""),
        "ready": estado.get("ready", False),
        "gate": {"open": (estado.get("gate") or {}).get("open", False),
                 "transition": (estado.get("gate") or {}).get("transition", "")},
        "by_state": por_estado,
        "all_ids": sorted({r.get("id") for r in linhas if r.get("id")}),
        "critical_open": [b for b in estado.get("blockers", [])
                          if b.get("kind") == "CRITICAL_OPEN"],
        "decisions": sorted(decisoes),
        "next_action": estado.get("next_action", {}),
        "kernel": kernel,
    }


def _index(t: dict) -> dict:
    """id -> registo, a partir de qualquer estado."""
    fora = {}
    for linhas in t.get("by_state", {}).values():
        for r in linhas:
            if r.get("id"):
                fora[r["id"]] = r
    return fora


# -------------------------------------------------------------- E01: continuidade

def _achado(code, sev, detail, **extra):
    return dict({"code": code, "severity": sev, "detail": detail}, **extra)


def check(t: dict, report: dict) -> dict:
    """O que a sessão reaberta disse vs o que os ficheiros dizem.

    Perder é crítico quando a linha perdida é dimensionante ou crítica: é disso que fala
    «Zero perda de IDs, estados, resoluções, decisões». Inventar é SEMPRE crítico — não há
    gravidade menor para um id que não existe.
    """
    achados = []

    em_falta = [c for c in CAMPOS_OBRIGATORIOS if c not in report]
    if em_falta:
        achados.append(_achado("REPORT_INCOMPLETE", CRITICO,
                               "a resposta não traz os campos pedidos: " + ", ".join(em_falta),
                               missing=em_falta))

    if report.get("phase") and t.get("phase") and report["phase"] != t["phase"]:
        achados.append(_achado("PHASE_MISMATCH", CRITICO,
                               "fase reportada {!r} != fase nos ficheiros {!r}".format(
                                   report["phase"], t["phase"])))

    idx = _index(t)
    reportados: dict[str, str] = {}
    for campo in ("facts", "open_questions", "blockers"):
        for item in (report.get(campo) or []):
            rid = item.get("id") if isinstance(item, dict) else str(item)
            if not rid:
                continue
            estado = item.get("state", "") if isinstance(item, dict) else ""
            reportados[rid] = estado

    # inventado: id que não existe em lado nenhum
    for rid, estado in sorted(reportados.items()):
        if rid not in idx:
            achados.append(_achado("INVENTED", CRITICO,
                                   "id reportado que não existe na SU", id=rid, claimed=estado))
            continue
        real = idx[rid].get("state") or ""
        if estado and estado != real:
            falso_confirmado = (estado == "Confirmed" and real != "Confirmed")
            achados.append(_achado(
                "FALSE_CONFIRMED" if falso_confirmado else "STATE_DRIFT",
                CRITICO if falso_confirmado else AVISO,
                "estado reportado {!r} != estado real {!r}".format(estado, real), id=rid))

    # perdido: o que a verdade tem e a sessão não devolveu
    for rid, r in sorted(idx.items()):
        if rid in reportados or r.get("resolved"):
            continue
        if (r.get("state") or "") not in ("Unknown", "Conflicted", "Risky", "Confirmed", "Assumed"):
            continue
        material = (str(r.get("swing_class", "")).lower() == "dimensionante"
                    or str(r.get("criticidade", "")).lower() in ("critical", "critica", "crítica"))
        if material:
            achados.append(_achado("LOST_CRITICAL", CRITICO,
                                   "linha material não recuperada pela sessão",
                                   id=rid, state=r.get("state")))
        elif (r.get("state") or "") in ("Unknown", "Conflicted"):
            achados.append(_achado("LOST", AVISO, "pergunta em aberto não recuperada",
                                   id=rid, state=r.get("state")))

    # decisões
    reportadas = {d.get("id") if isinstance(d, dict) else str(d)
                  for d in (report.get("decisions") or [])}
    for did in t.get("decisions", []):
        if did not in reportadas:
            achados.append(_achado("LOST_DECISION", CRITICO,
                                   "decisão tomada e não recuperada", id=did))
    for did in sorted(reportadas - set(t.get("decisions", []))):
        if did:
            achados.append(_achado("INVENTED_DECISION", CRITICO,
                                   "decisão reportada que não está em decisions.md", id=did))

    # proveniencia: por que mecanismo e que a sessao diz ter reconstruido, e se esse
    # mecanismo estava sequer disponivel. Sem isto o comparador da GO a uma recuperacao que
    # leu `shared-understanding.md` a moda antiga — que e o fluxo que E01 existe para NAO
    # dar por provado.
    kernel = t.get("kernel") or {}
    modo = kernel.get("mode", "")
    declarados = [str(x).strip().lower() for x in (report.get("recovered_via") or [])]
    pelo_kernel = [x for x in declarados if any(m in x for m in MECANISMOS_KERNEL)]

    if modo == "legacy":
        achados.append(_achado(
            "LEGACY_PATH", CRITICO,
            "o bootstrap correu em modo legacy ({} itens de contexto): o que a sessao "
            "recuperou NAO veio pelo kernel".format(kernel.get("context_items", 0)),
            graph_status=kernel.get("graph_status", "")))
    elif modo == "blocked":
        achados.append(_achado("KERNEL_BLOCKED", CRITICO,
                               "o bootstrap nao ficou pronto; nao ha recuperacao a medir"))

    if "recovered_via" not in report:
        achados.append(_achado("PROVENANCE_UNDECLARED", AVISO,
                               "a resposta nao diz por que mecanismo reconstruiu"))
    elif pelo_kernel and modo != "graph":
        achados.append(_achado(
            "PROVENANCE_MISMATCH", CRITICO,
            "a sessao diz ter usado {} mas o bootstrap estava em modo {!r}".format(
                pelo_kernel, modo or "desconhecido")))
    elif declarados and not pelo_kernel:
        achados.append(_achado(
            "PROVENANCE_OUTSIDE_KERNEL", AVISO,
            "reconstrucao declarada sem nenhum mecanismo do kernel: {}".format(declarados)))

    # avanço indevido: propor o passo seguinte com o gate fechado
    passo = str(report.get("next_step") or "")
    avanca = any(passo.strip().startswith(c) for c in
                 ("/frame", "/options", "/decide", "/blueprint", "/render", "/synthesize"))
    if avanca and not t.get("gate", {}).get("open", False):
        achados.append(_achado("UNDUE_ADVANCE", CRITICO,
                               "propõe {!r} com o gate fechado".format(passo.strip())))

    return _veredicto(t.get("engagement", ""), report.get("checkpoint", ""), "E01", achados)


def leak(t_outro: dict, report: dict) -> dict:
    """§6: trocar entre dois engagements e verificar que nada do primeiro entra no segundo."""
    idx_outro = set(_index(t_outro)) | set(t_outro.get("decisions", []))
    achados = []
    for campo in ("facts", "open_questions", "blockers", "decisions"):
        for item in (report.get(campo) or []):
            rid = item.get("id") if isinstance(item, dict) else str(item)
            if rid and rid in idx_outro:
                achados.append(_achado("LEAK", CRITICO,
                                       "id do engagement {!r} apareceu neste".format(
                                           t_outro.get("engagement", "")), id=rid, field=campo))
    return _veredicto(report.get("engagement", ""), report.get("checkpoint", ""),
                      "E01-leak", achados)


# ------------------------------------------------------- E02/E03: contra o oráculo

def oracle(eng_path: Path, oracle_doc: dict, mapping: dict) -> dict:
    """Mede os três números que o próprio oráculo declara em `acceptance`.

    `mapping` é `{<id do oráculo>: <id da SU ou null>}` e é declarado pelo CANDIDATO. Não
    se adivinha aqui: adivinhar seria construir a referência a partir do candidato, que é
    exactamente o que §5 proíbe.
    """
    t = truth(eng_path)
    idx = _index(t)
    itens = oracle_doc.get("items") or []
    criticos = [i for i in itens if i.get("criticality") == CRITICO]

    achados, recuperados, falsos = [], 0, 0
    for item in itens:
        oid = item.get("id")
        esperado = item.get("epistemic_state") or ""
        critico = item.get("criticality") == CRITICO
        alvo = (mapping or {}).get(oid)

        if not alvo:
            if critico:
                achados.append(_achado("CRITICAL_MISS", CRITICO,
                                       "item crítico do oráculo sem correspondência na SU",
                                       oracle_id=oid, expected_state=esperado))
            else:
                achados.append(_achado("MISS", AVISO, "item não crítico sem correspondência",
                                       oracle_id=oid))
            continue

        if alvo not in idx:
            achados.append(_achado("MAPPED_TO_NOTHING", CRITICO,
                                   "a correspondência aponta a uma linha inexistente",
                                   oracle_id=oid, su_id=alvo))
            continue

        real = idx[alvo].get("state") or ""
        if critico:
            recuperados += 1
        if esperado != "Confirmed" and real == "Confirmed":
            falsos += 1
            achados.append(_achado("FALSE_CONFIRMED", CRITICO,
                                   "o oráculo diz {!r}; a SU afirma Confirmed".format(esperado),
                                   oracle_id=oid, su_id=alvo))
        elif esperado != real:
            achados.append(_achado("STATE_DRIFT", AVISO,
                                   "oráculo {!r} vs SU {!r}".format(esperado, real),
                                   oracle_id=oid, su_id=alvo))

    avancos = 0 if t.get("ready") and not t.get("critical_open") else len(t.get("critical_open", []))
    if t.get("gate", {}).get("open") and t.get("critical_open"):
        achados.append(_achado("UNDUE_ADVANCE", CRITICO,
                               "gate aberto com {} crítico(s) por resolver".format(
                                   len(t["critical_open"]))))

    aceitacao = oracle_doc.get("acceptance") or {}
    medido = {
        "critical_recall": (recuperados / len(criticos)) if criticos else 1.0,
        "critical_false_confirmed": falsos,
        "improper_gate_advances": 1 if (t.get("gate", {}).get("open")
                                        and t.get("critical_open")) else 0,
    }
    v = _veredicto(t.get("engagement", ""), "oracle", "E02/E03", achados)
    v["measured"] = medido
    v["thresholds"] = aceitacao
    v["meets_thresholds"] = (
        medido["critical_recall"] >= float(aceitacao.get("critical_recall", 1.0))
        and medido["critical_false_confirmed"] <= int(aceitacao.get("critical_false_confirmed", 0))
        and medido["improper_gate_advances"] <= int(aceitacao.get("improper_gate_advances", 0)))
    v["critical_total"] = len(criticos)
    v["critical_recovered"] = recuperados
    if not v["meets_thresholds"]:
        v["verdict"] = "NO-GO"
    _ = avancos
    return v


# ------------------------------------------------------------------------- veredicto

def _veredicto(engagement, checkpoint, caso, achados) -> dict:
    criticos = [a for a in achados if a["severity"] == CRITICO]
    return {"engagement": engagement, "checkpoint": checkpoint, "case": caso,
            "findings": achados, "critical": len(criticos), "warnings": len(achados) - len(criticos),
            "verdict": "NO-GO" if criticos else "GO"}


def summary(runs: Path) -> dict:
    """Agrega o que estiver em `runs/`. Sem ficheiros, sem veredicto — não se conclui do vazio."""
    veredictos = [json.loads(p.read_text(encoding="utf-8"))
                  for p in sorted(runs.rglob("*.verdict.json"))]
    if not veredictos:
        return {"verdict": "SEM EXECUÇÃO", "runs": 0,
                "detail": "nenhum veredicto em {} — P8 não corre sozinho".format(runs)}
    criticos = sum(v.get("critical", 0) for v in veredictos)
    return {"runs": len(veredictos), "critical": criticos,
            "warnings": sum(v.get("warnings", 0) for v in veredictos),
            "by_case": sorted({v.get("case", "") for v in veredictos}),
            "no_go": [v["engagement"] + "/" + str(v.get("checkpoint"))
                      for v in veredictos if v.get("verdict") == "NO-GO"],
            "verdict": "NO-GO" if criticos else "GO"}


# ------------------------------------------------------------------------------ CLI

def _ler(p) -> dict:
    return json.loads(Path(p).read_text(encoding="utf-8"))


def _eng(slug) -> Path:
    p = Path(slug)
    if p.is_dir():
        return p
    p = ROOT / "projects" / slug
    if not p.is_dir():
        raise SystemExit("engagement não encontrado: {}".format(slug))
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("truth", help="congelar a verdade do engagement agora")
    t.add_argument("--engagement", required=True)
    t.add_argument("--checkpoint", required=True)
    t.add_argument("--out", required=True)

    c = sub.add_parser("check", help="comparar a resposta da sessão com a verdade")
    c.add_argument("--truth", required=True)
    c.add_argument("--report", required=True)
    c.add_argument("--out")

    l = sub.add_parser("leak", help="procurar contaminação do outro engagement")
    l.add_argument("--truth-other", required=True)
    l.add_argument("--report", required=True)
    l.add_argument("--out")

    o = sub.add_parser("oracle", help="medir a SU contra o oráculo independente")
    o.add_argument("--engagement", required=True)
    o.add_argument("--oracle", required=True)
    o.add_argument("--mapping", required=True)
    o.add_argument("--out")

    s = sub.add_parser("summary", help="agregar os veredictos de runs/")
    s.add_argument("--runs", required=True)

    a = ap.parse_args(argv)

    if a.cmd == "truth":
        doc = truth(_eng(a.engagement))
        destino = Path(a.out)
        destino.mkdir(parents=True, exist_ok=True)
        alvo = destino / "{}.truth.json".format(a.checkpoint)
        alvo.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("verdade congelada: {}".format(alvo))
        return 0

    if a.cmd == "summary":
        out = summary(Path(a.runs))
    elif a.cmd == "check":
        out = check(_ler(a.truth), _ler(a.report))
    elif a.cmd == "leak":
        out = leak(_ler(a.truth_other), _ler(a.report))
    else:
        out = oracle(_eng(a.engagement), _ler(a.oracle), _ler(a.mapping))

    texto = json.dumps(out, ensure_ascii=False, indent=2)
    if getattr(a, "out", None):
        Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        Path(a.out).write_text(texto + "\n", encoding="utf-8")
    print(texto)
    return 1 if out.get("verdict") == "NO-GO" else 0


if __name__ == "__main__":
    sys.exit(main())
