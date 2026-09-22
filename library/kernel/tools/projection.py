# -*- coding: utf-8 -*-
"""Projeccao operacional — o que o operador ve, e o que o gate usa (P7).

    python library/kernel/tools/projection.py --engagement <slug> [--json]

Stdlib apenas (ADR-001).

NAO E UM MODELO NOVO
    `dashboard.build_model` ja projecta fase, saude epistemica, agenda, criticos, tripwires,
    marco e o gate da transicao com o modo de cada criterio. Este modulo COMPOE isso com o
    que P2 e P3 trouxeram — pendencia de operacao e estado do grafo — porque o gate tem de
    avaliar o snapshot COMPLETO e nao um excerto.

O QUE ACRESCENTA, E SO ISTO
    1. O gate passa a consultar pendencia e drift, alem dos criterios que ja consultava.
       Um gate que ignorasse uma recuperacao pendente estaria a decidir sobre estado misto.
    2. Bloqueio com quatro campos: o que falta, porque importa, que evidencia fecha, que
       accao tomar. Um bloqueio que so diz «falta X» nao e accionavel.
    3. Incerteza NAO bloqueante continua visivel. Avancar nao e varrer para debaixo do tapete.
    4. Deteccao de projeccao desactualizada: `dashboard.html` gerado antes da ultima escrita
       das autoridades e reportado como stale, e stale NAO e verdade de gate.

O QUE NAO FAZ
    Nao inventa percentagens. Nao duplica `/resolve` nem `/advance` por existirem no doador.
    Nao decide nada: projecta.
"""
from __future__ import annotations

import json
import runpy
import sys
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_D = runpy.run_path(str(_HERE / "dashboard.py"))
_G = runpy.run_path(str(_HERE / "graph.py"))
_O = runpy.run_path(str(_HERE / "operation.py"))
_B = runpy.run_path(str(_HERE / "bootstrap.py"))

DASHBOARD = "dashboard.html"


def _blocker(what, why, evidence, action, kind):
    """Um bloqueio accionavel tem QUATRO campos. Tres nao chegam."""
    return {"what": what, "why_it_matters": why, "evidence_needed": evidence,
            "action": action, "kind": kind}


def projection_freshness(eng):
    """A projeccao esta a par das autoridades? (U05)

    Compara o mtime do `dashboard.html` com o da autoridade mais recente. Uma escrita por
    subprocesso nao dispara `PostToolUse`, por isso a projeccao pode ficar para tras sem
    que nenhum hook saiba — e a resposta certa e DIZE-LO, nao esconder."""
    eng = Path(eng)
    page = eng / DASHBOARD
    if not page.exists():
        return {"exists": False, "stale": False,
                "detail": "sem projeccao gerada — `/dashboard` cria-a"}
    newest, who = 0.0, ""
    for rel in _B["AUTHORITIES"]:
        p = eng / rel
        if p.exists() and p.stat().st_mtime > newest:
            newest, who = p.stat().st_mtime, rel
    stale = newest > page.stat().st_mtime
    return {"exists": True, "stale": stale, "newer_authority": who if stale else "",
            "detail": ("a projeccao e anterior a ultima escrita de `{}` — regenerar com "
                       "`/dashboard`; ate la NAO e verdade de gate".format(who) if stale
                       else "a projeccao esta a par das autoridades")}


# A forma do mapa de autoridade vive em `graph.py`, ao lado do `drift` que a consome.
# Aqui fica so o nome, para nao mudar quem ja o chama por este modulo.
authority_from_rows = _G["authority_from_rows"]


def drift_blocker(blocking_drift: list) -> dict:
    """O bloqueio de desvio, numa forma so.

    Desde que o bootstrap tambem bloqueia sobre desvio (F05), este bloqueio nasce em dois
    sitios: na saida antecipada, quando o bootstrap ja recusou, e aqui em baixo, quando
    chegou ate ao fim. Duas construcoes davam duas formas — e o que o caso guarda e que o
    bloqueio NOMEIA o campo que diverge e a linha onde diverge, nao o codigo generico.
    """
    primeiro = blocking_drift[0]
    campos = sorted({d.get("field") for d in blocking_drift if d.get("field")})
    faltam = [d for d in blocking_drift if d["code"] == "MIRROR_SOURCE_MISSING"]
    return _blocker(
        what="espelho do grafo divergente da autoridade — {} linha(s){}{}".format(
            len(blocking_drift),
            ", campos: " + ", ".join(campos) if campos else "",
            ", {} sem linha na SU".format(len(faltam)) if faltam else ""),
        why="o grafo nao prevalece sobre a SU; avancar assim decide sobre duas verdades",
        evidence="{} ({}): grafo={!r} autoridade={!r}".format(
            primeiro.get("id"), primeiro.get("field") or primeiro["code"],
            primeiro.get("graph"), primeiro.get("authority"))
        if primeiro.get("field") else
        "{}: o grafo espelha `{}`, que a SU ja nao tem".format(
            primeiro.get("id"), primeiro.get("mirror_of")),
        action="/status", kind=primeiro["code"])


def operational_state(eng, today=None):
    """Fase, bloqueios, incerteza visivel e proxima accao — de autoridades verificadas."""
    eng = Path(eng)
    boot = _B["bootstrap"](eng)
    out = {"engagement": boot.get("engagement", {}),
           "ready": boot.get("ready", False),
           "blockers": [], "visible_uncertainty": [], "gate": {},
           "projection": projection_freshness(eng)}

    # 1. pendencia fecha tudo — antes de ler conteudo (contrato B5)
    if not boot["ready"]:
        desvio_bloqueante = [d for d in (boot.get("drift") or [])
                             if d["code"] in ("MIRROR_DRIFT", "MIRROR_SOURCE_MISSING")]
        for lim in boot["limitations"]:
            if lim["code"] == "AUTHORITY_DRIFT" and desvio_bloqueante:
                out["blockers"].append(drift_blocker(desvio_bloqueante))
                continue
            out["blockers"].append(_blocker(
                what=lim.get("detail", lim["code"]),
                why="enquanto durar, qualquer avanco decide sobre estado misto",
                evidence="o estado tem de ficar consistente antes de se ler o conteudo",
                action=lim.get("recovery") or "resolver antes de continuar",
                kind=lim["code"]))
        out["phase"] = ""
        out["next_action"] = {"text": "Recuperar antes de qualquer outra coisa.",
                              "command": out["blockers"][0]["action"]}
        out["gate"] = {"open": False, "reason": "bootstrap nao pronto"}
        # A divergencia que o bootstrap ja calculou vem com ele: desde que ela BLOQUEIA
        # (F05), esta saida antecipada e o caminho normal para um engagement divergente, e
        # devolver a vista sem `drift` escondia exactamente a razao do bloqueio.
        out["drift"] = boot.get("drift", [])
        return out

    model = _D["build_model"](eng, today or date.today())
    # As chaves sao as de `build_model`, verificadas contra a saida real: a fase vive em
    # `engagement`, as linhas em `su.rows`, e o gate e o marco em `status`. Assumir nomes
    # aqui daria uma projeccao que le o vazio sem se queixar.
    eng_block = model.get("engagement") or {}
    status_block = model.get("status") or {}
    rows = (model.get("su") or {}).get("rows") or []
    out["phase"] = eng_block.get("phase", "")
    out["milestone"] = status_block.get("milestone", {})
    out["health"] = model.get("health", {})

    # 2. criticos abertos — bloqueiam, e dizem porque
    for c in (model.get("critical") or []):
        out["blockers"].append(_blocker(
            what="{} ({})".format(c.get("claim", "")[:110], c.get("id", "")),
            why="e material: muda um eixo tecnico da decisao",
            evidence=c.get("support") or "por atribuir",
            action='/answer {} "..."'.format(c.get("id", "")),
            kind="CRITICAL_OPEN"))

    # 3. incerteza NAO bloqueante continua visivel (U03)
    crit_ids = {c.get("id") for c in (model.get("critical") or [])}
    for r in rows:
        if r.get("state") not in ("Unknown", "Conflicted"):
            continue
        if r.get("id") in crit_ids or str(r.get("resolved")) == "True":
            continue
        out["visible_uncertainty"].append(
            {"id": r.get("id"), "claim": (r.get("claim") or "")[:110],
             "criticidade": r.get("criticidade", ""),
             "note": "nao bloqueia — continua visivel"})

    # 4. o gate avalia o SNAPSHOT COMPLETO, nao um excerto
    gates = status_block.get("gates") or {}
    g = gates if isinstance(gates, dict) else {}
    # A autoridade e a SU. Passar `{}` aqui nao era so nao detectar desvio: com o mapa
    # vazio, TODOS os nos espelhados saiam como `MIRROR_SOURCE_MISSING` — 225 nos dois
    # pilotos — e a linha seguinte filtrava-os fora. Um falso positivo sobre a populacao
    # inteira, calculado e deitado ao lixo.
    drift = _G["drift"](_G["read"](eng).get("nodes", []), authority_from_rows(rows))
    blocking_drift = [d for d in drift
                      if d["code"] in ("MIRROR_DRIFT", "MIRROR_SOURCE_MISSING")]
    out["drift"] = drift
    out["gate"] = {
        "transition": g.get("transition", ""),
        "criteria": g.get("criteria", []),
        "open": bool(g.get("passes")) and not out["blockers"] and not blocking_drift,
        "reason": ("criterios da transicao" if g else "sem transicao a sair desta fase"),
        "consulted": ["criterios de fase", "operacao pendente", "espelho do grafo"],
    }
    if blocking_drift:
        out["blockers"].append(drift_blocker(blocking_drift))

    out["next_action"] = (status_block.get("milestone") or {}).get("next") or {
        "text": "Sem accao pendente identificada.", "command": "/status"}
    return out


def explain(eng, today=None):
    """A explicacao para quem NAO tem de saber ids internos nem schema (U01).

    Regra P-13 do `CLAUDE.md`: o utilizador le linguagem de negocio; o id do kernel vai
    entre parenteses, depois da frase, nunca como sujeito."""
    st = operational_state(eng, today)
    lines = []
    lines.append("Onde estamos: {}".format(st.get("phase") or "por determinar"))
    if st["blockers"]:
        b = st["blockers"][0]
        lines.append("O que falta: {}".format(b["what"]))
        lines.append("Porque importa: {}".format(b["why_it_matters"]))
        lines.append("O que fecha isto: {}".format(b["evidence_needed"]))
    else:
        lines.append("O que falta: nada que impeca o proximo passo.")
    if st["visible_uncertainty"]:
        lines.append("Continua em aberto, sem bloquear: {} tema(s).".format(
            len(st["visible_uncertainty"])))
    if st["projection"]["stale"]:
        lines.append("Aviso: a pagina de acompanhamento esta desactualizada — "
                     "o que vale e o que esta nos ficheiros.")
    na = st["next_action"]
    lines.append("A seguir: {} -> {}".format(na.get("text", ""), na.get("command", "")))
    return {"text": "\n".join(lines), "state": st}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="projeccao operacional")
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    eng = Path(a.engagement)
    if not eng.is_dir():
        eng = Path("projects") / a.engagement
    if not eng.is_dir():
        print("engagement nao encontrado", file=sys.stderr)
        return 2
    out = explain(eng)
    print(json.dumps(out["state"], ensure_ascii=False, indent=2) if a.json else out["text"])
    return 0 if out["state"]["ready"] else 1


if __name__ == "__main__":
    sys.exit(main())
