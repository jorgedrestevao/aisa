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


def read_base(eng: Path, rels=()):
    """O conteudo E o digest de cada ficheiro, da MESMA leitura.

    O plano lia os ficheiros no principio e tirava os digests no fim, e entre as duas coisas
    cabia uma escrita: ela ficava registada como a base — `expected` batia certo com o disco
    — enquanto o conteudo preparado era o de antes dela. O coordenador publicava, e a
    alteracao desaparecia com recibo `committed` e sem uma unica recusa.

    `BASE_CHANGED` existia e nunca disparava, porque o que lhe era declarado ja era o estado
    novo. Nao e um problema de que ficheiros se declaram (isso foi o F04) — e de QUANDO se
    tira o digest: do texto que se leu, nao do ficheiro que la esta quando o plano acaba.
    """
    eng = Path(eng)
    fora = {}
    for rel in rels:
        caminho = eng / rel
        try:
            bruto = caminho.read_bytes()
        except OSError:
            fora[rel] = {"text": "", "digest": ""}
            continue
        fora[rel] = {"text": bruto.decode("utf-8"),
                     "digest": hashlib.sha256(bruto).hexdigest()}
    return fora


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


# Forca do estado, do mais forte ao mais fraco. Serve para UMA coisa: decidir se um
# `--to` pedido pelo operador desce (legitimo) ou sobe (proibido).
FORCA = {"Confirmed": 3, "Assumed": 2, "Risky": 1}


def force_state(verdict: dict, pedido: str) -> dict:
    """Aplica um `--to`. Desce sempre; sobe nunca.

    `states.md` proibe promover em silencio, e a regra dura 3 do `/answer` diz o mesmo:
    uma resposta de terceiro ou sem locator nao vira `Confirmed` porque quem a escreveu
    estava confiante. Descer e o contrario disso — e quem responde declarar que as provas
    dao mais do que ele quer afirmar."""
    if not pedido:
        return verdict
    alvo = pedido.strip().capitalize()
    if alvo not in FORCA:
        raise ResolveError("estado desconhecido: {!r}".format(pedido), "UNKNOWN_STATE",
                           {"aceites": sorted(FORCA)})
    actual = verdict["state"]
    if FORCA[alvo] > FORCA[actual]:
        raise ResolveError(
            "`--to {}` promovia sobre {} — states.md proibe promocao silenciosa".format(
                alvo, actual),
            "SILENT_UPGRADE",
            {"decidido": actual, "pedido": alvo, "porque": verdict["reason"]})
    if alvo == actual:
        return verdict
    return dict(verdict, state=alvo, forced_from=actual,
                reason="{} — descido para {} por declaracao do operador".format(
                    verdict["reason"], alvo))


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
         settles=SETTLES_FACT, claim="", today="", to=""):
    """Calcula TUDO sem publicar (contrato B2.4)."""
    eng = Path(eng)
    when = today or date.today().isoformat()
    # UMA leitura: o texto que se usa e o digest que se declara saem daqui, do mesmo
    # instante. Ver `read_base`.
    lido = read_base(eng, (SU_FILE, ANSWERS_FILE))
    md = lido[SU_FILE]["text"]
    _h, rows, _s, _d = _D["parse_su"](md)
    row = find_row(rows, row_id)

    verdict = force_state(decide_state(row, answered_by, locator, inference), to)
    struct = structural_verdict(row, settles)
    state = verdict["state"]
    new_id = next_id(rows, state)

    who = answered_by.get("role") or answered_by.get("source") or answered_by.get("other") or "—"
    # A ancora `answers.md#<id>` entra sempre. Se o chamador passou exactamente essa como
    # `--locator` — e e o locator que o limiar de `Confirmed` pede — escreve-la outra vez
    # dava `…, answers.md#U-001 (was U-001), answers.md#U-001` na mesma celula.
    ancora = "{}#{}".format(ANSWERS_FILE, row_id)
    loc_extra = (locator or "").strip()
    if loc_extra in ("", ancora):
        loc_extra = ""
    basis = "USER_ANSWER {w} — {who}{loc} (was {old}), {anc}".format(
        w=when, who=who, loc=", {}".format(loc_extra) if loc_extra else "",
        old=row_id, anc=ancora)
    lens, ronda = row.get("lens") or "", row.get("ronda") or ""
    claim_text = claim or (answer_text.strip().splitlines() or [""])[0]
    cells = [new_id, lens, claim_text, basis, when, "organizacional", ronda]

    su_new = append_row(mark_resolved(md, row_id, [new_id]), state, cells)

    ans_old = lido[ANSWERS_FILE]["text"] or "# Respostas\n"
    ans_new = ans_old.rstrip("\n") + "\n" + answers_section(row_id, answer_text, answered_by, when)

    # O que o escritor sabe e a SU nao diz: a linha original como pergunta, o sucessor com
    # a proveniencia de quem respondeu, e a ligacao `was` entre os dois. Os campos
    # espelhados vem todos da SU publicada — `mirror_write_set` trata disso.
    extra_nodes = [
        {"id": row_id, "type": "question", "props": {},
         "provenance": {"lens": lens, "ronda": ronda, "mirror_of": "SU:" + row_id}},
        {"id": new_id, "type": "claim",
         "props": {"structural_choice_open": struct["choice_open"]},
         "provenance": {"lens": lens, "ronda": ronda, "answered_by": who,
                        "locator": locator, "mirror_of": "SU:" + new_id}},
    ]
    extra_edges = [{"src": new_id, "rel": "was", "dst": row_id, "props": {},
                    "provenance": {"ronda": ronda}}]

    write_set = {SU_FILE: su_new, ANSWERS_FILE: ans_new}
    write_set.update(mirror_write_set(eng, su_new, extra_nodes, extra_edges))

    return {"operation_id": operation_id(row_id, answer_text), "row": row_id,
            "new_id": new_id, "state": state, "verdict": verdict, "structural": struct,
            "write_set": write_set,
            "expected": _expected_for(eng, write_set, lido),
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
    ap.add_argument("--answer", default="")
    ap.add_argument("--op", default="answer",
                    choices=["answer", "revalidate", "withdraw", "accept-risk",
                             "resolve-conflict"],
                    help="a operacao; `answer` por defeito, para nao mudar o que ja existia")
    ap.add_argument("--note", default="", help="revalidate: a nota de confirmacao")
    ap.add_argument("--changed", action="store_true",
                    help="revalidate: o facto MUDOU — recusa, porque isso e transicao")
    ap.add_argument("--reason", default="", help="withdraw: a razao da retirada")
    ap.add_argument("--basis", default="", help="accept-risk: a base da aceitacao")
    ap.add_argument("--side", action="append", default=[],
                    help="resolve-conflict: um lado; repetir por cada lado")
    ap.add_argument("--by-owner", action="store_true",
                    help="resolve-conflict: o dono decidiu (senao resolve por evidencia interna)")
    ap.add_argument("--by", default="")
    ap.add_argument("--locator", default="")
    ap.add_argument("--inference", action="store_true")
    ap.add_argument("--settles", choices=[SETTLES_FACT, SETTLES_FIT], default=SETTLES_FACT)
    ap.add_argument("--claim", default="",
                    help="o facto extraido para a linha da SU; sem isto usa a 1a linha da resposta")
    ap.add_argument("--to", default="", choices=["", "confirmed", "assumed", "risky"],
                    help="forcar o estado — so DESCE; subir e recusado (promocao silenciosa)")
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
    def _exige(nome, valor):
        if not valor:
            raise ResolveError(
                "`--op {}` exige `--{}`".format(a.op, nome), "MISSING_ARG",
                {"op": a.op, "falta": nome})
        return valor

    try:
        if a.op == "answer":
            _exige("answer", a.answer)
            fn = plan if a.dry_run else apply
            out = fn(eng, row_id=a.row, answer_text=a.answer, answered_by=by,
                     locator=a.locator, inference=a.inference, settles=a.settles,
                     claim=a.claim, to=a.to)
        elif a.op == "revalidate":
            fn = plan_revalidate if a.dry_run else apply_revalidate
            out = fn(eng, row_id=a.row, still_holds=not a.changed, note=a.note, by=a.by)
        elif a.op == "withdraw":
            fn = plan_withdraw if a.dry_run else apply_withdraw
            out = fn(eng, row_id=a.row, reason=_exige("reason", a.reason))
        elif a.op == "accept-risk":
            fn = plan_accept_risk if a.dry_run else apply_accept_risk
            out = fn(eng, row_id=a.row, basis=_exige("basis", a.basis))
        else:
            if len(a.side) < 2:
                raise ResolveError("`--op resolve-conflict` exige pelo menos dois `--side`",
                                   "TOO_FEW_SIDES", {"lados": len(a.side)})
            fn = plan_resolve_conflict if a.dry_run else apply_resolve_conflict
            out = fn(eng, row_id=a.row, sides=a.side, by_owner=a.by_owner, by=by)
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
        if "structural" in out:
            print("{:16} {}".format("estrutural", out["structural"]["note"]))
    return 0


# ============================================================================
# Ciclo do conhecimento (L06-L10) — as transicoes que nao partem de `Unknown`.
# Todas por `library/kernel/states.md` -> *Transitions*.
# ============================================================================

RETIRADA_MARK = "— retirada P-21"


def revalidate(row, still_holds, note="", today=""):
    """Confirmed/Assumed expirado (L09).

    `states.md` distingue DOIS caminhos, e a diferenca importa:
      still_holds=True  -> **edicao sancionada**: renova `verificado_em` NA PROPRIA LINHA,
                           sem linha nova. Nao ha claim nova porque nao ha facto novo.
      still_holds=False -> o facto mudou -> cai no fluxo NORMAL (`was <id>`), e a correccao
                           exige transicao. «Never renew a changed fact.»"""
    when = today or date.today().isoformat()
    rid = (row.get("id") or "").strip()
    if still_holds:
        return {"mode": "sanctioned_edit", "row": rid, "new_id": "",
                "verificado_em": when, "creates_row": False,
                "reason": "o facto mantem-se — `states.md`: renovar `verificado_em` na "
                          "propria linha, sem linha nova",
                "note": note}
    return {"mode": "transition", "row": rid, "creates_row": True,
            "reason": "o facto mudou — `states.md`: «Never renew a changed fact»; aplica-se "
                      "o fluxo normal com `was {}`".format(rid),
            "note": note}


def withdraw(row, reason):
    """Retirada por ambito (P-21, a quarta edicao sancionada) (L08).

    Sai «por um marcador na ultima coluna e por mais nada». Nao vira facto, nao apaga
    historia, nao cria linha nova."""
    if not (reason or "").strip():
        raise ResolveError("retirada exige razao — a base fica registada", "NO_BASIS",
                           {"row": row.get("id")})
    return {"mode": "withdrawal", "row": (row.get("id") or "").strip(),
            "marker": "{} ({})".format(RETIRADA_MARK, reason.strip()),
            "creates_row": False, "becomes_fact": False,
            "reason": "retirada por ambito — marcador na ultima coluna, e mais nada"}


def resolve_conflict(row, sides, by_owner, today=""):
    """Conflicted -> Confirmed (xN) ou Assumed (L07).

    Os DOIS lados sobrevivem. `states.md`: com decisao do dono, N linhas Confirmed; sem ela,
    uma Assumed com `was X-nnn`. Nunca se escolhe por recencia — nao ha ordenacao temporal
    nesta funcao, de proposito."""
    rid = (row.get("id") or "").strip()
    if len(sides) < 2:
        raise ResolveError("um conflito tem pelo menos dois lados", "TOO_FEW_SIDES",
                           {"row": rid, "sides": len(sides)})
    if by_owner:
        return {"mode": "owner_decision", "row": rid, "state": "Confirmed",
                "successors": len(sides), "sides_preserved": list(sides),
                "reason": "o dono decidiu — `states.md`: Conflicted -> Confirmed (xN)",
                "chose_by_recency": False}
    return {"mode": "internal_evidence", "row": rid, "state": "Assumed",
            "successors": 1, "sides_preserved": list(sides),
            "reason": "sem resposta do dono — `states.md`: Conflicted -> Assumed, base = as "
                      "linhas e locators usados",
            "chose_by_recency": False}


def accept_risk(row, basis):
    """Risky com risco aceite (L08). A base EXIGIDA fica registada; nao vira facto."""
    if not (basis or "").strip():
        raise ResolveError("aceitar risco exige base registada", "NO_BASIS",
                           {"row": row.get("id")})
    return {"mode": "risk_accepted", "row": (row.get("id") or "").strip(),
            "basis": basis.strip(), "becomes_fact": False, "creates_row": False,
            "reason": "risco aceite com base registada — continua Risky, nao vira Confirmed"}


def finding(fid, behaviour, evidence, criticality, action):
    """Um finding de comportamento manual (L06).

    Distincao, evidencia, criticidade e accao sao os quatro campos que tem de sobreviver
    ao reinicio — por isso viajam como props do no, nao como prosa."""
    missing = [k for k, v in (("behaviour", behaviour), ("evidence", evidence),
                              ("criticality", criticality), ("action", action)) if not v]
    if missing:
        raise ResolveError("finding incompleto: {}".format(", ".join(missing)),
                           "INCOMPLETE_FINDING", {"missing": missing})
    return {"id": fid, "type": "finding",
            "props": {"behaviour": behaviour, "evidence": evidence,
                      "criticality": criticality, "action": action, "disposed": False},
            "provenance": {"kind": "manual-behaviour"}}


def dispose_finding(node, disposition, basis):
    """Dispor ou reabrir um finding (L06). A historia fica; o estado muda."""
    if disposition not in ("disposed", "reopened"):
        raise ResolveError("disposicao invalida: {}".format(disposition), "BAD_DISPOSITION",
                           {"got": disposition})
    if not (basis or "").strip():
        raise ResolveError("dispor/reabrir exige base", "NO_BASIS", {"id": node.get("id")})
    props = dict(node.get("props") or {})
    props["disposed"] = disposition == "disposed"
    props.setdefault("history", [])
    props["history"] = list(props["history"]) + [{"disposition": disposition,
                                                  "basis": basis.strip()}]
    return dict(node, props=props)


def dependents_of(nodes, edges, changed_ids):
    """Quem depende do que mudou — revalidacao DIRECCIONADA (L10).

    Segue `depends_on` e `was` a partir dos ids alterados. Quem nao esta na cadeia nao e
    tocado: revalidar tudo seria o mesmo que nao revalidar nada."""
    changed = set(changed_ids or ())
    by_src = {}
    for e in edges:
        if e.get("rel") in ("depends_on", "was"):
            by_src.setdefault(e.get("dst"), set()).add(e.get("src"))
    out, frontier = set(), set(changed)
    while frontier:
        nxt = set()
        for cid in frontier:
            for dep in by_src.get(cid, ()):
                if dep not in out and dep not in changed:
                    out.add(dep)
                    nxt.add(dep)
        frontier = nxt
    return sorted(out)


def decision_rewritten_by(answer_targets, decision_ids):
    """Uma resposta NUNCA reescreve uma decisao (L10).

    `states.md` da a `/answer` transicoes de linhas da SU. Uma decisao muda por `/decide`,
    nao por resposta. Esta funcao existe para que a regra seja verificavel."""
    hit = sorted(set(answer_targets or ()) & set(decision_ids or ()))
    return {"would_rewrite": bool(hit), "decisions": hit,
            "reason": ("uma resposta nao reescreve uma decisao — isso e `/decide`"
                       if hit else "")}


# ============================================================================
# W4 — as operacoes de ciclo de vida passam pelo coordenador.
#
# Cada uma tem `plan_*` (compoe o conjunto de escrita, publica nada) e `apply_*`
# (publica por `_O["run"]`, com recibo). A DECISAO fica nas funcoes de parecer acima —
# `revalidate`, `withdraw`, `resolve_conflict`, `accept_risk` — que estes chamam. A regra
# vive num sitio so; o que muda e passar a haver quem a escreva.
# ============================================================================

SECTION_RE = re.compile(r"^##\s+(\w[\w \-]*)\s*$")


def _section_of(md, row_id):
    """`(estado, cabecalhos, indice da linha)` da seccao onde a linha vive.

    A coluna e encontrada pelo NOME no cabecalho da seccao, nao por indice fixo: as cinco
    seccoes da SU tem colunas diferentes (`Risky` nao tem `verificado_em`, `Unknown` nao tem
    `validade`), e um indice contado a olho parte na primeira seccao que nao for a esperada.
    """
    estado, headers = "", []
    linhas = md.splitlines()
    for i, linha in enumerate(linhas):
        m = SECTION_RE.match(linha.strip())
        if m:
            estado, headers = m.group(1), []
            continue
        if linha.lstrip().startswith("|") and not headers and estado:
            headers = [c.strip() for c in linha.strip().strip("|").split("|")]
            continue
        if re.match(r"^\|\s*" + re.escape(row_id) + r"\s*\|", linha):
            return estado, headers, i
    raise ResolveError("nao encontrei a linha `{}` no texto da SU".format(row_id),
                       "ROW_LINE_NOT_FOUND", {"row": row_id})


def set_cell(md, row_id, coluna, valor):
    """Substitui UMA celula, identificada pelo nome da coluna na sua seccao."""
    estado, headers, i = _section_of(md, row_id)
    if coluna not in headers:
        raise ResolveError(
            "a seccao `{}` nao tem coluna `{}`".format(estado, coluna),
            "COLUMN_MISSING", {"row": row_id, "section": estado, "headers": headers})
    k = headers.index(coluna)
    linhas = md.splitlines()
    cells = linhas[i].rstrip().rstrip("|").split("|")
    # `split("|")` sobre `| a | b |` da um primeiro elemento vazio: o indice da coluna k
    # esta em k+1.
    cells[k + 1] = " {} ".format(valor)
    linhas[i] = "|".join(cells) + "|"
    return "\n".join(linhas) + ("\n" if md.endswith("\n") else "")


def append_cell(md, row_id, coluna, sufixo):
    """Acrescenta a uma celula sem apagar o que la esta. Idempotente sobre o mesmo sufixo."""
    estado, headers, i = _section_of(md, row_id)
    if coluna not in headers:
        raise ResolveError(
            "a seccao `{}` nao tem coluna `{}`".format(estado, coluna),
            "COLUMN_MISSING", {"row": row_id, "section": estado, "headers": headers})
    k = headers.index(coluna)
    linhas = md.splitlines()
    cells = linhas[i].rstrip().rstrip("|").split("|")
    actual = cells[k + 1].strip()
    if sufixo in actual:
        return md                      # ja la esta: repetir nao acrescenta informacao
    cells[k + 1] = " {} {} ".format(actual, sufixo).replace("  ", " ")
    linhas[i] = "|".join(cells) + "|"
    return "\n".join(linhas) + ("\n" if md.endswith("\n") else "")


def _revalidation_section(row, note, by, when):
    return (
        "\n## {rid} — {w} (revalidacao)\n"
        "- **Claim**: {claim}\n"
        "- **Confirmacao**: mantem-se — {note}\n"
        "- **Fonte**: {by}\n"
        "- **verificado_em**: {old} -> {w}\n"
    ).format(rid=row.get("id", ""), w=when, claim=row.get("claim", ""),
             note=(note or "").strip() or "(sem nota)", by=by or "—",
             old=row.get("verificado_em") or "—")


def _answers_with(eng, seccao):
    ap = eng / ANSWERS_FILE
    antigo = ap.read_text(encoding="utf-8") if ap.exists() else "# Respostas\n"
    return antigo.rstrip("\n") + "\n" + seccao


def _expected(eng, *rels):
    return {rel: _O["digest"](eng / rel) for rel in rels}


def mirror_write_set(eng, su_new, extra_nodes=(), extra_edges=()):
    """O grafo que acompanha uma SU nova — os campos espelhados postos ao que ela diz.

    **Quem escreve a autoridade escreve o espelho dela.** Nao uma versao sua, e nao noutra
    transaccao: desde que o bootstrap BLOQUEIA sobre desvio, um escritor que deixe o grafo
    para tras nao produz uma inconsistencia tolerada — inutiliza o engagement. Medido antes
    de existir esta funcao: `apply_resolve_conflict` levava `ready` de True a False.

    Isto e a CLASSE, nao o caso. A primeira correccao (F06) fechou o `/answer` e deixou os
    outros escritores a depender de sorte: `withdraw` e `accept_risk` passaram porque tocam
    colunas que nao sao espelhadas, e `resolve_conflict` nao passou. Um escritor novo nao
    pode depender disso.

    `extra_nodes`/`extra_edges` sao o que o escritor sabe e a SU nao diz — a ligacao `was`
    de um sucessor, a proveniencia de quem respondeu. Os campos do contrato do espelho
    (`state`, `criticidade`, `resolved`, `text`) vem SEMPRE da SU publicada, nunca do que o
    chamador achar.
    """
    eng = Path(eng)
    st = _G["read"](eng)
    nodes = list(st.get("nodes", []))
    edges = list(st.get("edges", []))
    have = {n.get("id") for n in nodes}
    for n in extra_nodes:
        if n.get("id") not in have:
            nodes.append(n)
            have.add(n.get("id"))
    for e in extra_edges:
        if not any(x.get("src") == e.get("src") and x.get("rel") == e.get("rel")
                   and x.get("dst") == e.get("dst") for x in edges):
            edges.append(e)

    _h, linhas, _s, _d = _D["parse_su"](su_new)
    autoridade = _G["authority_from_rows"](linhas)

    # Uma linha da SU sem no nenhum bloqueia a reconstrucao (F08, segunda metade). Quem a
    # criou tem de a espelhar — senao a operacao bem sucedida bloqueia a seguinte.
    espelhadas = {(n.get("provenance") or {}).get("mirror_of") for n in nodes}
    por_id = {("SU:" + str(r.get("id") or "").strip()): r for r in linhas if r.get("id")}
    for chave in sorted(set(autoridade) - espelhadas):
        r = por_id[chave]
        nodes.append({"id": r["id"], "type": "su-row", "props": {},
                      "provenance": {"lens": r.get("lens") or "",
                                     "ronda": r.get("ronda") or "",
                                     "mirror_of": chave}})

    nodes = [
        dict(n, props=_G["mirror_props"](
            n.get("props"), autoridade.get((n.get("provenance") or {}).get("mirror_of") or "",
                                           {})))
        if (n.get("provenance") or {}).get("mirror_of") in autoridade else n
        for n in nodes
    ]
    ws = _G["write_set"](nodes, edges)
    # Um espelho que nao muda nao se publica. A REGRA e que todo o escritor de autoridade
    # chame isto — nao que toda a escrita carregue o grafo atras. `revalidate` mexe em
    # `verificado_em`, que nao e campo espelhado: chamar e obrigatorio, publicar seria ruido
    # (e um recibo a dizer que o grafo mudou quando nao mudou).
    if all(_O["digest"](eng / rel) == hashlib.sha256(corpo.encode("utf-8")).hexdigest()
           for rel, corpo in ws.items()):
        return {}
    return ws


def _expected_for(eng, write_set, base=None):
    """A precondicao cobre TUDO o que o plano escreve — nao uma lista escrita a mao.

    O plano de uma resposta escreve o grafo INTEIRO (`_G["write_set"]` serializa todos os
    nos e arestas), e a precondicao so exigia os digests da SU e do answers. Quem
    escrevesse no grafo entre o planeamento e a publicacao desaparecia, com recibo
    `committed` e sem uma recusa — `BASE_CHANGED` existe e nunca era consultado para os
    ficheiros do grafo, porque nunca lhe foram declarados.

    Derivar do `write_set` em vez de enumerar fecha a classe, nao o caso: um escritor novo
    nao pode esquecer-se de acrescentar um ficheiro aqui.
    """
    lida = base or {}
    return {rel: (lida[rel]["digest"] if rel in lida else _O["digest"](Path(eng) / rel))
            for rel in write_set}


def plan_revalidate(eng, row_id, still_holds, note="", by="", today=""):
    """L09. Facto mantem-se -> edicao sancionada. Facto mudou -> NAO e revalidacao."""
    eng = Path(eng)
    when = today or date.today().isoformat()
    lido = read_base(eng, (SU_FILE, ANSWERS_FILE))  # uma leitura: texto e digest
    md = lido[SU_FILE]["text"]
    _h, rows, _s, _d = _D["parse_su"](md)
    row = find_row(rows, row_id)
    parecer = revalidate(row, still_holds, note=note, today=when)

    if parecer["mode"] == "transition":
        raise ResolveError(
            "o facto mudou — `states.md`: «Never renew a changed fact». Isto e uma "
            "transicao normal (`was {}`), nao uma revalidacao".format(row_id),
            "FACT_CHANGED", {"row": row_id, "proximo": "resolve.plan(...)"})

    su_new = set_cell(md, row_id, "verificado_em", when)
    ans_new = _answers_with(eng, _revalidation_section(row, note, by, when))
    write_set = {SU_FILE: su_new, ANSWERS_FILE: ans_new}
    write_set.update(mirror_write_set(eng, su_new))
    return {"operation_id": "revalidate-{}-{}".format(row_id, when),
            "row": row_id, "mode": parecer["mode"], "verificado_em": when,
            "creates_row": False, "verdict": parecer,
            "write_set": write_set,
            "expected": _expected_for(eng, write_set, lido),
            "summary": {"o que mudou": "{} revalidado — verificado_em {}".format(row_id, when),
                        "estado": "sem linha nova: o facto e o mesmo",
                        "proximo passo": "nada; a linha volta a estar dentro da validade"}}


def plan_withdraw(eng, row_id, reason):
    """L08/P-21. Sai por um marcador na ultima coluna e por mais nada."""
    eng = Path(eng)
    lido = read_base(eng, (SU_FILE, ANSWERS_FILE))  # uma leitura: texto e digest
    md = lido[SU_FILE]["text"]
    _h, rows, _s, _d = _D["parse_su"](md)
    row = find_row(rows, row_id)
    parecer = withdraw(row, reason)
    _estado, headers, _i = _section_of(md, row_id)
    su_new = append_cell(md, row_id, headers[-1], parecer["marker"])
    write_set = {SU_FILE: su_new}
    write_set.update(mirror_write_set(eng, su_new))
    return {"operation_id": "withdraw-{}".format(row_id),
            "row": row_id, "mode": parecer["mode"], "creates_row": False,
            "becomes_fact": False, "verdict": parecer,
            "write_set": write_set,
            "expected": _expected_for(eng, write_set, lido),
            "summary": {"o que mudou": "{} retirada por ambito".format(row_id),
                        "estado": "nao virou facto; a linha fica para historia",
                        "proximo passo": "nada — retirar nao abre nada"}}


def plan_accept_risk(eng, row_id, basis):
    """L08. O risco continua Risky; o que muda e a base ficar registada."""
    eng = Path(eng)
    lido = read_base(eng, (SU_FILE, ANSWERS_FILE))  # uma leitura: texto e digest
    md = lido[SU_FILE]["text"]
    _h, rows, _s, _d = _D["parse_su"](md)
    row = find_row(rows, row_id)
    parecer = accept_risk(row, basis)
    estado, headers, _i = _section_of(md, row_id)
    coluna = "mitigação proposta" if "mitigação proposta" in headers else headers[-2]
    su_new = append_cell(md, row_id, coluna,
                         "— risco aceite: {}".format(parecer["basis"]))
    write_set = {SU_FILE: su_new}
    write_set.update(mirror_write_set(eng, su_new))
    return {"operation_id": "accept-risk-{}".format(row_id),
            "row": row_id, "mode": parecer["mode"], "becomes_fact": False,
            "creates_row": False, "verdict": parecer,
            "write_set": write_set,
            "expected": _expected_for(eng, write_set, lido),
            "summary": {"o que mudou": "{} — risco aceite com base registada".format(row_id),
                        "estado": "continua {}; aceitar nao e resolver".format(estado),
                        "proximo passo": "nada; a base fica auditavel"}}


def plan_resolve_conflict(eng, row_id, sides, by_owner, by=None, today=""):
    """L07. Os DOIS lados sobrevivem: N linhas com decisao do dono, 1 Assumed sem ela."""
    eng = Path(eng)
    when = today or date.today().isoformat()
    lido = read_base(eng, (SU_FILE, ANSWERS_FILE))  # uma leitura: texto e digest
    md = lido[SU_FILE]["text"]
    _h, rows, _s, _d = _D["parse_su"](md)
    row = find_row(rows, row_id)
    parecer = resolve_conflict(row, sides, by_owner, today=when)
    by = by or {}
    quem = by.get("role") or by.get("source") or by.get("other") or "—"

    estado_alvo = parecer["state"]
    lens, ronda = row.get("lens") or "", row.get("ronda") or ""
    novos, su_new = [], md
    lados = list(sides) if by_owner else [" · ".join(str(x) for x in sides)]
    for lado in lados:
        # cada linha recebe o id livre SEGUINTE, calculado sobre a SU ja com as anteriores
        _h, rows_agora, _s, _d = _D["parse_su"](su_new)
        novo_id = next_id(rows_agora, estado_alvo)
        base = "RESOLUCAO {w} — {q} (was {old}), {af}#{old}".format(
            w=when, q=quem, old=row_id, af=ANSWERS_FILE)
        cells = [novo_id, lens, str(lado), base, when, "organizacional", ronda]
        su_new = append_row(su_new, estado_alvo, cells)
        novos.append(novo_id)
    su_new = mark_resolved(su_new, row_id, novos)

    seccao = (
        "\n## {rid} — {w} (conflito resolvido)\n"
        "- **Conflito**: {claim}\n"
        "- **Lados preservados**: {lados}\n"
        "- **Resolucao**: {modo}\n"
        "- **Fonte**: {q}\n"
    ).format(rid=row_id, w=when, claim=row.get("claim", ""),
             lados=" | ".join(str(x) for x in sides), modo=parecer["reason"], q=quem)

    # Os sucessores ligam-se ao conflito original; os campos espelhados vem da SU publicada.
    ronda = row.get("ronda") or ""
    lens = row.get("lens") or ""
    extra_nodes = [{"id": nid, "type": "claim", "props": {},
                    "provenance": {"lens": lens, "ronda": ronda, "answered_by": quem,
                                   "mirror_of": "SU:" + nid}} for nid in novos]
    extra_edges = [{"src": nid, "rel": "was", "dst": row_id, "props": {},
                    "provenance": {"ronda": ronda}} for nid in novos]
    write_set = {SU_FILE: su_new, ANSWERS_FILE: _answers_with(eng, seccao)}
    write_set.update(mirror_write_set(eng, su_new, extra_nodes, extra_edges))
    return {"operation_id": "resolve-conflict-{}-{}".format(row_id, operation_id(
                row_id, "|".join(str(x) for x in sides))[-12:]),
            "row": row_id, "new_ids": novos, "state": estado_alvo,
            "mode": parecer["mode"], "verdict": parecer,
            "write_set": write_set,
            "expected": _expected_for(eng, write_set, lido),
            "summary": {"o que mudou": "{} -> {} {}".format(
                            row_id, estado_alvo, ", ".join(novos)),
                        "estado": "os dois lados sobrevivem; nao se escolheu por recencia",
                        "proximo passo": "nada" if by_owner else
                                         "confirmar com o dono para passar a Confirmed"}}


def _apply_plan(eng, p):
    """Publica um plano de ciclo de vida. O MESMO caminho do `/answer`: gate, operacao, recibo.

    «Mesmo caminho» era o que a docstring dizia e nao era verdade: `apply` consultava o
    bootstrap e isto nao. A pendencia era apanhada na mesma — o coordenador tem a sua
    verificacao —, mas desvio de autoridade e ausencia de grafo sao do bootstrap, e por ai
    as quatro operacoes de ciclo de vida passavam sobre estado que o `/answer` recusava.
    Medido: sobre `AUTHORITY_DRIFT`, `/answer` recusado e `revalidate`/`accept_risk`
    publicados.
    """
    eng = Path(eng)
    boot = _B["bootstrap"](eng)
    if not boot["ready"]:
        raise ResolveError("bootstrap nao pronto — operacao recusada", "NOT_READY",
                           {"limitations": boot["limitations"]})
    recibo = _O["run"](eng, p["operation_id"], p["write_set"], expected=p["expected"])
    return dict(p, receipt=recibo, published=recibo.get("published", []))


def apply_revalidate(eng, **kw):
    return _apply_plan(eng, plan_revalidate(eng, **kw))


def apply_withdraw(eng, **kw):
    return _apply_plan(eng, plan_withdraw(eng, **kw))


def apply_accept_risk(eng, **kw):
    return _apply_plan(eng, plan_accept_risk(eng, **kw))


def apply_resolve_conflict(eng, **kw):
    return _apply_plan(eng, plan_resolve_conflict(eng, **kw))


# ============================================================================
# W6 — o indice inverso das citacoes. Calculado a pedido, guardado em lado nenhum.
# ============================================================================

# Os derivados que `aisa-answer` passo 7 manda percorrer. A SU NAO esta aqui de proposito:
# uma linha citar-se a si propria nao e dependencia, e inclui-la dava 100% de cobertura
# falsa.
DERIVED_GLOBS = (
    "frame.md",
    "options.md",
    "decisions.md",
    "story.md",
    "_synthesis/*.md",
    "_blueprint/*.yaml",
    "_simulation/**/*.md",
    "_render/**/*.md",
)


def derived_files(eng) -> list:
    """Os artefactos derivados que existem, por ordem estavel."""
    eng = Path(eng)
    fora = []
    for padrao in DERIVED_GLOBS:
        fora += [f for f in sorted(eng.glob(padrao)) if f.is_file()]
    return fora


def cited_by(eng, row_ids=None) -> dict:
    """`{id: [caminhos relativos]}` — quem cita cada linha da SU.

    Os ids procurados vem da SU, nunca de um padrao inventado: medido nos pilotos, um
    padrao generico apanhava `F-01`, `O-005`, `D-002` e `PM-003`, que sao rondas, opcoes,
    decisoes e passos do modelo de processo — nao linhas da SU.

    A fronteira da procura importa tanto como o alvo: `C-01` nao pode casar dentro de
    `C-010`, e um id seguido de `)` ou `,` tem de casar na mesma.
    """
    eng = Path(eng)
    if row_ids is None:
        _md, rows = read_su(eng)
        row_ids = [(r.get("id") or "").strip() for r in rows if (r.get("id") or "").strip()]

    textos = []
    for f in derived_files(eng):
        try:
            textos.append((str(f.relative_to(eng)), f.read_text(encoding="utf-8",
                                                                errors="replace")))
        except OSError:
            continue

    fora = {}
    for rid in sorted(set(row_ids)):
        padrao = re.compile(r"(?<![\w-])" + re.escape(rid) + r"(?![\w-])")
        ficheiros = {rel for rel, texto in textos if padrao.search(texto)}
        fora[rid] = sorted(ficheiros)
    return fora


def _G_dependents(eng, changed_ids) -> list:
    """Os sucessores no grafo — a outra metade do impacto, que ja existia."""
    st = _G["read"](Path(eng))
    if st.get("status") != _G["OK"]:
        return []
    return dependents_of(st.get("nodes", []), st.get("edges", []), changed_ids)


def impact_of(eng, changed_ids) -> dict:
    """O que uma alteracao toca: os derivados que a citam e os sucessores no grafo.

    Devolve CANDIDATOS, nunca um veredicto. Um derivado citar uma linha que mudou nao prova
    que ele e anterior a mudanca — nenhum derivado regista contra que valores foi escrito.
    Quem le decide, uma linha por dependente, e e isso que `aisa-answer` passo 7 ja pede.
    """
    eng = Path(eng)
    alterados = [i for i in (changed_ids or []) if i]
    indice = cited_by(eng, alterados)
    por_id = {rid: fs for rid, fs in indice.items() if fs}
    todos = sorted({f for fs in por_id.values() for f in fs})
    return {
        "changed": sorted(set(alterados)),
        "cited_by": por_id,
        "not_cited": sorted(set(alterados) - set(por_id)),
        "files": todos,
        "successors": _G_dependents(eng, alterados),
        "verdict": "candidatos — citar nao prova anterioridade; o julgamento e de quem le",
    }


# O guard fica no FIM, e so no fim: tudo o que vier depois dele existe para quem
# importa o modulo e NAO existe para quem o corre. As funcoes de ciclo de vida
# viveram ai, e por isso a CLI nunca lhes chegou.
if __name__ == "__main__":
    sys.exit(main())
