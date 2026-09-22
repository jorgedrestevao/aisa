# -*- coding: utf-8 -*-
"""Resolução de uma linha da Shared Understanding — o motor por trás de `/answer`.

Stdlib apenas (ADR-001). Reutiliza `dashboard.py` para ler a SU: um segundo parser seria
uma segunda verdade.

O QUE DECIDE, E O QUE NÃO DECIDE
    Decide o ESTADO para onde a linha transita, por `library/kernel/states.md` →
    *Transitions*, a partir de factos verificáveis: há locator? quem respondeu bate com a
    autoridade que a própria linha declarou? é inferência assumida?

    Não redige prosa nem escolhe a claim. `aisa-answer/SKILL.md` continua a redigir; o que
    muda é que a regra deixa de ser só texto e passa a ter motor que a recusa quando violada.

AS TRÊS REGRAS QUE IMPÕE
    1. Autoridade não se presume (L03). `Unknown → Confirmed` exige locator E correspondência
       com a autoridade declarada. Resposta de terceiro resolve para `Assumed`, com razão
       escrita — textual em `states.md`: «an answer from someone other than the owner or a
       named authority».
    2. Facto não fecha adequação (L05). Resposta que estabelece conectividade/capacidade
       regista o facto e deixa a escolha estrutural ABERTA. Prosa em `aisa-answer` §46-48;
       aqui é veredicto calculado.
    3. Repetir não duplica (L04). O `operation_id` deriva da linha e da resposta.

CONVENÇÃO DE ESCRITA — lida de engagements reais, não inventada
    linha nova      evidência: `USER_ANSWER <data> — <quem> (was U-NNN), answers.md#U-NNN`
    linha original  última coluna: `<ronda> — resolved → C-014, A-006`
"""
from __future__ import annotations

import hashlib
import json
import re
import runpy
import sys
from datetime import date
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_D = runpy.run_path(str(_HERE / "dashboard.py"))
_G = runpy.run_path(str(_HERE / "graph.py"))
_O = runpy.run_path(str(_HERE / "operation.py"))
_B = runpy.run_path(str(_HERE / "bootstrap.py"))

SU_FILE = "shared-understanding.md"
ANSWERS_FILE = "answers.md"
PREFIX_FOR = {"Confirmed": "C", "Assumed": "A", "Unknown": "U",
              "Conflicted": "X", "Risky": "R"}
SETTLES_FACT = "fact"
SETTLES_FIT = "fit"


class ResolveError(Exception):
    def __init__(self, message: str, code: str, detail: dict | None = None):
        super().__init__(message)
        self.code = code
        self.detail = detail or {}

    def as_dict(self) -> dict:
        return {"error": str(self), "code": self.code, "detail": self.detail}


def read_su(eng: Path):
    md = (Path(eng) / SU_FILE).read_text(encoding="utf-8")
    _h, rows, _s, _d = _D["parse_su"](md)
    return md, rows


def find_row(rows, row_id):
    for r in rows:
        if (r.get("id") or "").strip() == row_id:
            return r
    raise ResolveError("linha `{}` nao existe na SU".format(row_id), "ROW_NOT_FOUND",
                       {"row": row_id})


def next_id(rows, state):
    pref = PREFIX_FOR[state]
    used = [int(m.group(1)) for r in rows
            for m in [re.match(r"^" + pref + r"-(\d+)$", (r.get("id") or "").strip())] if m]
    return "{}-{:03d}".format(pref, (max(used) + 1) if used else 1)


# -------------------------------------------------------------- autoridade (L03)

def declared_authority(row):
    """A autoridade que a PROPRIA linha declarou. `split_owner` so interpreta prefixos."""
    # `parse_su` normaliza `quem responde` / `partes` para `support`.
    raw = row.get("support") or ""
    o = _D["split_owner"](raw)
    return {"raw": raw, "role": o.get("role") or [], "source": o.get("source") or [],
            "unassigned": bool(o.get("unassigned"))}


def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def authority_match(row, answered_by):
    decl = declared_authority(row)
    got_role, got_source = _norm(answered_by.get("role", "")), _norm(answered_by.get("source", ""))
    if decl["unassigned"] or (not decl["role"] and not decl["source"]):
        return {"matched": False, "declared": decl,
                "reason": "a linha nao declara autoridade — nada a que corresponder"}
    for r in decl["role"]:
        if got_role and (_norm(r) == got_role or got_role in _norm(r) or _norm(r) in got_role):
            return {"matched": True, "declared": decl, "matched_on": "role", "value": r}
    for s in decl["source"]:
        if got_source and (_norm(s) == got_source or got_source in _norm(s)
                           or _norm(s) in got_source):
            return {"matched": True, "declared": decl, "matched_on": "fonte", "value": s}
    return {"matched": False, "declared": decl,
            "reason": "quem respondeu nao corresponde a autoridade declarada"}


def decide_state(row, answered_by, locator="", inference=False):
    """O estado de destino, por `states.md`. NUNCA promove em silencio."""
    if inference:
        return {"state": "Assumed", "authority": authority_match(row, answered_by),
                "reason": "inferencia declarada — states.md: «reasonable inference accepted "
                          "(must declare)»"}
    auth = authority_match(row, answered_by)
    if not locator:
        return {"state": "Assumed", "authority": auth,
                "reason": "sem locator — states.md exige locator para Confirmed"}
    if not auth["matched"]:
        return {"state": "Assumed", "authority": auth,
                "reason": "resposta de terceiro — states.md: «an answer from someone other than "
                          "the owner or a named authority» resolve para Assumed"}
    return {"state": "Confirmed", "authority": auth,
            "reason": "locator presente e autoridade declarada correspondida"}


# ------------------------------------------------- facto versus adequacao (L05)

def structural_verdict(row, settles):
    """Estrutural ou nao — pela classificacao que `parse_su` JA computa.

    `swing_class == "dimensionante"` e o veredicto do motor sobre se a pergunta muda um
    eixo tecnico. Fazer regex sobre a prosa seria uma segunda classificacao, a divergir da
    primeira ao primeiro caso estranho."""
    if str(row.get("swing_class", "")).strip().lower() != "dimensionante":
        return {"structural": False, "choice_open": False,
                "note": "nao se aplica — a pergunta nao decide um eixo estrutural"}
    if settles == SETTLES_FIT:
        return {"structural": True, "choice_open": False,
                "note": "a resposta estabelece adequacao ao requisito — a escolha pode fechar"}
    return {"structural": True, "choice_open": True,
            "note": "escolha estrutural continua em aberto — a resposta estabelece "
                    "conectividade/capacidade, nao o mecanismo nem a sua adequacao"}


# ------------------------------------------------------------------- escrita

def mark_resolved(md, row_id, successors):
    """Append a ultima coluna. NUNCA apaga a linha."""
    out, hit = [], False
    for line in md.splitlines():
        if re.match(r"^\|\s*" + re.escape(row_id) + r"\s*\|", line):
            cells = line.rstrip().rstrip("|").split("|")
            last = cells[-1].strip()
            if "resolved" not in last:
                cells[-1] = " {} — resolved -> {} ".format(last, ", ".join(successors))
                line = "|".join(cells) + "|"
            hit = True
        out.append(line)
    if not hit:
        raise ResolveError("nao encontrei a linha `{}` no texto da SU".format(row_id),
                           "ROW_LINE_NOT_FOUND", {"row": row_id})
    return "\n".join(out) + ("\n" if md.endswith("\n") else "")


def append_row(md, state, cells):
    lines = md.splitlines()
    heading = "## " + state
    start = next((i for i, l in enumerate(lines) if l.strip() == heading), -1)
    if start < 0:
        raise ResolveError("a SU nao tem seccao `{}`".format(heading), "SECTION_MISSING",
                           {"state": state})
    i, last_row = start + 1, -1
    while i < len(lines) and not lines[i].startswith("## "):
        if lines[i].lstrip().startswith("|"):
            last_row = i
        i += 1
    if last_row < 0:
        raise ResolveError("seccao `{}` sem tabela".format(heading), "SECTION_NO_TABLE",
                           {"state": state})
    lines.insert(last_row + 1, "| " + " | ".join(cells) + " |")
    return "\n".join(lines) + "\n"


def answers_section(row_id, answer_text, answered_by, when):
    who = answered_by.get("role") or answered_by.get("source") or answered_by.get("other") or "—"
    return ("\n## {rid}\n\n- **Respondido por:** {who}\n- **Data:** {when}\n\n> {v}\n").format(
        rid=row_id, who=who, when=when, v=answer_text.replace("\n", "\n> "))


def operation_id(row_id, answer_text):
    """Deriva da linha e do conteudo: repetir a mesma resolucao e a MESMA operacao (L04)."""
    h = hashlib.sha256((row_id + "\x00" + answer_text).encode("utf-8")).hexdigest()[:16]
    return "resolve-{}-{}".format(row_id, h)


def plan(eng, row_id, answer_text, answered_by, locator="", inference=False,
         settles=SETTLES_FACT, claim="", today=""):
    """Calcula TUDO sem publicar (contrato B2.4)."""
    eng = Path(eng)
    when = today or date.today().isoformat()
    md, rows = read_su(eng)
    row = find_row(rows, row_id)

    verdict = decide_state(row, answered_by, locator, inference)
    struct = structural_verdict(row, settles)
    state = verdict["state"]
    new_id = next_id(rows, state)

    who = answered_by.get("role") or answered_by.get("source") or answered_by.get("other") or "—"
    basis = "USER_ANSWER {w} — {who}{loc} (was {old}), {af}#{old}".format(
        w=when, who=who, loc=", {}".format(locator) if locator else "",
        old=row_id, af=ANSWERS_FILE)
    lens, ronda = row.get("lens") or "", row.get("ronda") or ""
    claim_text = claim or (answer_text.strip().splitlines() or [""])[0]
    cells = [new_id, lens, claim_text, basis, when, "organizacional", ronda]

    su_new = append_row(mark_resolved(md, row_id, [new_id]), state, cells)

    ap = eng / ANSWERS_FILE
    ans_old = ap.read_text(encoding="utf-8") if ap.exists() else "# Respostas\n"
    ans_new = ans_old.rstrip("\n") + "\n" + answers_section(row_id, answer_text, answered_by, when)

    st = _G["read"](eng)
    nodes, edges = list(st.get("nodes", [])), list(st.get("edges", []))
    have = {n.get("id") for n in nodes}
    if row_id not in have:
        nodes.append({"id": row_id, "type": "question",
                      "props": {"state": "Unknown", "text": row.get("claim", "")},
                      "provenance": {"lens": lens, "ronda": ronda, "mirror_of": "SU:" + row_id}})
    if new_id not in have:
        nodes.append({"id": new_id, "type": "claim",
                      "props": {"state": state, "text": claim_text,
                                "structural_choice_open": struct["choice_open"]},
                      "provenance": {"lens": lens, "ronda": ronda, "answered_by": who,
                                     "locator": locator, "mirror_of": "SU:" + new_id}})
    if not any(e.get("src") == new_id and e.get("rel") == "was" for e in edges):
        edges.append({"src": new_id, "rel": "was", "dst": row_id, "props": {},
                      "provenance": {"ronda": ronda}})

    write_set = {SU_FILE: su_new, ANSWERS_FILE: ans_new}
    write_set.update(_G["write_set"](nodes, edges))

    return {"operation_id": operation_id(row_id, answer_text), "row": row_id,
            "new_id": new_id, "state": state, "verdict": verdict, "structural": struct,
            "write_set": write_set,
            "expected": {SU_FILE: _O["digest"](eng / SU_FILE),
                         ANSWERS_FILE: _O["digest"](eng / ANSWERS_FILE)},
            "summary": {
                "o que mudou": "{} -> {} {}".format(row_id, state, new_id),
                "estado": ("escolha estrutural em aberto" if struct["choice_open"]
                           else "sem escolha estrutural pendente"),
                "proximo passo": ("resolver a adequacao da escolha estrutural"
                                  if struct["choice_open"] else "/status")}}


def apply(eng, **kw):
    """Planeia e publica como UMA operacao. Bootstrap primeiro — nunca sobre pendencia."""
    eng = Path(eng)
    boot = _B["bootstrap"](eng)
    if not boot["ready"]:
        raise ResolveError("bootstrap nao pronto — operacao recusada", "NOT_READY",
                           {"limitations": boot["limitations"]})

    # Idempotencia ANTES de planear (L04). Replanear sobre uma SU ja resolvida produz um
    # payload diferente com o mesmo `operation_id`, e o coordenador recusa-o — com razao.
    # Quem sabe que a operacao ja correu e este nivel: o id deriva da linha e da resposta,
    # nao do estado do mundo.
    op_id = operation_id(kw["row_id"], kw["answer_text"])
    done = _O["read_receipt"](eng, op_id)
    if done:
        return {"operation_id": op_id, "row": kw["row_id"],
                "new_id": "", "state": "", "verdict": {}, "structural": {},
                "receipt": dict(done, replayed=True), "replayed": True,
                "summary": {"o que mudou": "nada — esta resolucao ja tinha corrido",
                            "estado": "inalterado",
                            "proximo passo": "/status"}}

    p = plan(eng, **kw)
    receipt = _O["run"](eng, p["operation_id"], p["write_set"], expected=p["expected"])
    return dict(p, receipt=receipt, replayed=bool(receipt.get("replayed")))


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="resolver uma linha da SU")
    ap.add_argument("--engagement", required=True)
    ap.add_argument("--row", required=True)
    ap.add_argument("--answer", required=True)
    ap.add_argument("--by", default="")
    ap.add_argument("--locator", default="")
    ap.add_argument("--inference", action="store_true")
    ap.add_argument("--settles", choices=[SETTLES_FACT, SETTLES_FIT], default=SETTLES_FACT)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    eng = Path(a.engagement)
    if not eng.is_dir():
        eng = Path("projects") / a.engagement
    by = {}
    low = a.by.lower()
    if low.startswith("role:"):
        by = {"role": a.by.split(":", 1)[1].strip()}
    elif low.startswith(("fonte:", "source:")):
        by = {"source": a.by.split(":", 1)[1].strip()}
    elif a.by:
        by = {"other": a.by}
    try:
        fn = plan if a.dry_run else apply
        out = fn(eng, row_id=a.row, answer_text=a.answer, answered_by=by,
                 locator=a.locator, inference=a.inference, settles=a.settles)
    except (ResolveError, _O["OperationError"], _G["GraphError"]) as exc:
        print(json.dumps(exc.as_dict(), ensure_ascii=False, indent=2), file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps({k: v for k, v in out.items() if k != "write_set"},
                         ensure_ascii=False, indent=2))
    else:
        for k, v in out["summary"].items():
            print("{:16} {}".format(k, v))
        print("{:16} {}".format("porque", out["verdict"]["reason"]))
        print("{:16} {}".format("estrutural", out["structural"]["note"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
