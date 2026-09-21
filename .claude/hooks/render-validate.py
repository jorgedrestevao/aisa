#!/usr/bin/env python3
"""render-validate.py — sufficiency of a rendered deliverable, checked BY CONTENT (P-7).

Two entry points, one motor:

  PostToolUse hook (stdin JSON, `Write`/`Edit` to <engagement>/_render/*.md)
      -> validates the deliverable just written, appends a `## Validação …` block to
         <engagement>/_render/render-gaps.md when a rule fails, prints one line to stderr.
         Fail-open: any error is reported, never blocks the write (exit 0).
  CLI  python .claude/hooks/render-validate.py --engagement <slug> [--deliverable implementation-spec]
                                               [--version vNN] [--dry-run] [--json]
      -> the same checks over the newest (or given) rendered version; --dry-run writes nothing.

What "by content" means (docs/CONSOLIDATED_PLAN.md P-7; deliverable template `sufficiency:`):
presence of a section is not sufficiency. The rules the template declares are executed here,
deterministically, against the APPROVED blueprint's architecture record and the rendered text:

  entities_to_create   every approved entity resolves `authority` to a `record_authority[].key`
                       (or the section carries its ⚠️ lacuna row); an `owned` domain has ≥ 1 typed
                       field and a primary index; an external domain has reads[], writes[] (or
                       readonly), key[] (or open) and a schema_owner; every dictionary line has
                       state + source.
  flows_to_implement   `(none)` is a defect while an approved entity carries a state machine or an
                       approval step.
  security_implementation  a Papel × (Ecrã | Entidade) table exists in the section.
  integrations         authentication + secret custody are present per integration, or the gap is
                       named in the section.

A failed rule is a `required` gap (owner: architecture or implementation). The motor never fills a
slot, never edits the deliverable, never reads `_capture/` or the SU to repair anything.

Coverage is reported BESIDE this, never instead of it (`library/kernel/coverage-contract.md` §8.2):
the `coverage` block of the result carries the five verdicts of the stage-`render` review of the
same file, read through the coverage motor — the rules are not duplicated here, and the finding is
never written to `render-gaps.md` by this hook: the owner of a coverage gap is the review, and
`aisa-render` step 9b is where it is recorded. Sufficiency says the document is well formed;
coverage says it carried what was asked. Two questions, two lines, and neither answers the other.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import os
import re
import sys
import unicodedata
from pathlib import Path

TOOL_VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
DELIVERABLE_RE = re.compile(
    r"^(?P<slug>.+?)_(?P<deliverable>discovery-report|executive-report|solution-blueprint|"
    r"implementation-spec|claude-design-brief|estimate)_v(?P<ver>\d{2,3})\.md$")
SECTION_KEYS = {
    "entities_to_create": ("entidade",),
    "flows_to_implement": ("fluxo",),
    "integrations": ("integra",),
    "security_implementation": ("seguran",),
}


def _load_dashboard():
    p = REPO / "library" / "kernel" / "tools" / "dashboard.py"
    spec = importlib.util.spec_from_file_location("aisa_dashboard_for_validate", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_coverage():
    """O motor de cobertura, carregado sob procura. Falhar aqui não pode partir a
    suficiência: quem chama trata `None` como «não avaliado»."""
    p = REPO / "library" / "kernel" / "tools" / "coverage.py"
    if not p.is_file():
        return None
    spec = importlib.util.spec_from_file_location("aisa_coverage_for_validate", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def coverage_report(eng: Path, rendered: Path) -> dict:
    """Os veredictos da revisão de projecção deste ficheiro (read-only).

    Não duplica uma única regra: chama `coverage_state` e mostra o que ele devolve. Sem
    registo, `not_evaluated` — que não é «completo» nem «reprovado» (§10)."""
    out = {"evaluated": False, "state": "", "contract_validity": "not_evaluated",
           "freshness": "not_evaluated", "source_review": "not_evaluated",
           "semantic_review": "not_evaluated", "coverage": "not_evaluated",
           "eligible": False, "record": "", "findings": 0}
    try:
        C = _load_coverage()
        if C is None:
            out["state"] = "motor ausente"
            return out
        rel = rendered.resolve().relative_to(eng.resolve()).as_posix()
        target = {"file": rel, "identity": C.target_identity(eng, "render", rel)}
        res = C.coverage_state(eng, "render", target)
    except Exception as exc:                              # noqa: BLE001 — fail-open
        out["state"] = "{}: {}".format(type(exc).__name__, exc)
        return out
    out.update({
        "evaluated": True, "state": "ok",
        "contract_validity": res["contract_validity"], "freshness": res["freshness"],
        "source_review": res["source_review"], "semantic_review": res["semantic_review"],
        "coverage": res["coverage"], "eligible": bool(res["eligible"]),
        "record": (res.get("record") or {}).get("file", ""),
        "findings": len([d for d in res.get("diagnostics", [])
                         if d.get("severity") == "error"]),
    })
    return out


def _fold(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s or "") if unicodedata.category(c) != "Mn").lower()


def now_iso() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat()


# ------------------------------------------------------------- tolerant YAML items

def yl_items(block: list[tuple[int, str]]) -> list[list[tuple[int, str]]]:
    """Split a `- …` sequence block into items (each a list of (indent, content) lines),
    by the indentation of the item markers. Nested lists stay inside their item."""
    if not block:
        return []
    base = min(ind for ind, c in block if c.startswith("- "))
    items: list[list[tuple[int, str]]] = []
    for ind, content in block:
        if ind == base and content.startswith("- "):
            items.append([(ind + 2, content[2:].strip())])
        elif items:
            items[-1].append((ind, content))
    return items


def item_scalar(item: list[tuple[int, str]], key: str):
    base = item[0][0]
    for ind, content in item:
        if ind == base:
            m = re.match(r"^" + re.escape(key) + r"\s*:\s*(.*)$", content)
            if m:
                return m.group(1).strip()
    return None


def item_children(item: list[tuple[int, str]], key: str) -> list[tuple[int, str]]:
    base = item[0][0]
    out: list[tuple[int, str]] = []
    grab = False
    for ind, content in item:
        if ind == base:
            if grab:
                break
            if re.match(r"^" + re.escape(key) + r"\s*:", content):
                grab = True
            continue
        if grab:
            out.append((ind, content))
    return out


def _scalar_list_nonempty(value: str | None) -> bool | None:
    """`[a, b]` -> True; `[]` -> False; None/other -> None (not a scalar list)."""
    if value is None:
        return None
    v = value.strip()
    if v.startswith("[") and v.endswith("]"):
        return bool(v[1:-1].strip())
    return None


def _truthy(value: str | None) -> bool:
    return (value or "").strip().strip('"\'').lower() in ("true", "yes", "on", "sim")


def _unq(value: str | None) -> str:
    v = (value or "").strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return re.sub(r"\s+#.*$", "", v).strip()


# ------------------------------------------------------------- the record

SEE_RE = re.compile(r"SEE_V(\d{1,3})", re.I)


def _follow(D, text: str, key: str, loader, parent: str | None = None, depth: int = 0) -> list[tuple[int, str]]:
    """A top-level block, following `key: SEE_Vnn` back-references (a version that changed
    only the architecture says `entities: SEE_V01`; the entities still live in v01)."""
    scalar = D.yl_scalar_at(text, key, parent)
    m = SEE_RE.search(str(scalar or ""))
    if m and loader is not None and depth < 8:
        other = loader("v" + m.group(1).zfill(2))
        if other:
            return _follow(D, other, key, loader, parent, depth + 1)
        return []
    return D.yl_find_block(text, key, parent)


def read_record(D, text: str, loader=None) -> dict:
    ra_block = (_follow(D, text, "record_authority", loader, "architecture")
                or _follow(D, text, "record_authority", loader))
    domains = []
    for it in yl_items(ra_block):
        mode = _unq(item_scalar(it, "access_mode"))
        fields = yl_items(item_children(it, "fields"))
        ac = item_children(it, "access_contract")
        # reuse the item_* helpers on the contract body: its keys sit at the contract's own indent
        ac_item = ([(min(ind for ind, _ in ac), "_")] + [(ind, c) for ind, c in ac]) if ac else []
        reads = yl_items(item_children(ac_item, "reads")) if ac else []
        writes = yl_items(item_children(ac_item, "writes")) if ac else []
        key_scalar = item_scalar(ac_item, "key") if ac else None
        key_children = item_children(ac_item, "key") if ac else []
        domains.append({
            "domain": _unq(item_scalar(it, "domain")),
            "key": _unq(item_scalar(it, "key")),
            "access_mode": mode,
            "fields": fields,
            "has_access_contract": bool(ac),
            "reads": reads, "writes": writes,
            "readonly": _truthy(item_scalar(ac_item, "readonly")) if ac else False,
            "key_nonempty": (_scalar_list_nonempty(key_scalar) if key_scalar is not None else bool(key_children)),
            "key_open": bool(ac and (item_scalar(ac_item, "open") or re.search(r"open:\s*U-\d+", " ".join(c for _, c in ac)))),
            "schema_owner": bool(item_scalar(it, "schema_owner") is not None or item_children(it, "schema_owner")),
        })
    entities = []
    for it in yl_items(_follow(D, text, "entities", loader)):
        entities.append({
            "name": _unq(item_scalar(it, "name")),
            "label": _unq(item_scalar(it, "label")),
            "authority": _unq(item_scalar(it, "authority")),
            "state_machine": bool(item_children(it, "state_machine")) or bool(_scalar_list_nonempty(item_scalar(it, "state_machine"))),
            "approval": _truthy(item_scalar(it, "approval")),
        })
    return {"domains": domains, "entities": entities}


def _lines_missing_state_source(items: list[list[tuple[int, str]]]) -> int:
    n = 0
    for it in items:
        if item_scalar(it, "state") is None or item_scalar(it, "source") is None:
            n += 1
    return n


# ------------------------------------------------------------- rendered text

def sections(md: str) -> dict[str, str]:
    """Rendered `## …` sections keyed by the folded heading text."""
    out: dict[str, str] = {}
    parts = re.split(r"^##\s+", md, flags=re.M)
    for chunk in parts[1:]:
        head, _, body = chunk.partition("\n")
        out[_fold(head.strip())] = body
    return out


def section_for(secs: dict[str, str], slot: str) -> str | None:
    for head, body in secs.items():
        if any(k in head for k in SECTION_KEYS.get(slot, ())):
            return body
    return None


def has_role_matrix(body: str) -> bool:
    """A table whose header names the role axis (papel / role / persona) and carries at
    least two more columns — the Papel × (Ecrã | Entidade) matrix, whatever the columns are
    called (a legacy render names the entities and screens directly)."""
    for line in (body or "").splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or set("".join(cells)) <= set("-: "):
            continue
        head = _fold(cells[0])
        if any(k in head for k in ("papel", "role", "persona", "perfil")) and len(cells) >= 3:
            return True
    return False


# ------------------------------------------------------------- template sufficiency

def sufficiency_slots(template_text: str) -> list[str]:
    m = re.search(r"^sufficiency:\s*\n((?:[ \t]+.*\n)+)", template_text, re.M)
    if not m:
        return []
    return [ln.strip().rstrip(":") for ln in m.group(1).splitlines()
            if re.match(r"^\s{2}[a-z_]+:\s*$", ln)]


# ------------------------------------------------------------- checks

def gap(slot, rule, detail, owner="architecture", resolves=""):
    return {"slot": slot, "rule": rule, "detail": detail, "owner": owner, "resolves": resolves}


def check_entities(record: dict, sec: str | None) -> list[dict]:
    gaps: list[dict] = []
    text = sec or ""
    keys = {d["key"] for d in record["domains"] if d["key"]}
    for e in record["entities"]:
        auth = e["authority"]
        declared = "lacuna" in _fold(text) and (_fold(e["name"]) in _fold(text) or (e["label"] and _fold(e["label"]) in _fold(text)))
        if not auth or auth.lower().startswith("none"):
            if not declared:
                gaps.append(gap("entities_to_create", "entities[].authority",
                                "entidade `{}` sem autoridade de registo e sem linha ⚠️ lacuna na secção".format(e["name"]),
                                resolves="`authority: <record_authority[].key>` ou `none — <razão>` + linha de lacuna"))
        elif keys and auth not in keys:
            gaps.append(gap("entities_to_create", "entities[].authority",
                            "entidade `{}` aponta para `{}`, que não é `key` de nenhum domínio".format(e["name"], auth),
                            resolves="corrigir `authority` ou criar o domínio"))
    for d in record["domains"]:
        name = d["key"] or d["domain"] or "?"
        if not d["key"]:
            gaps.append(gap("entities_to_create", "record_authority[].key",
                            "domínio `{}` sem `key` (P-6) — nenhuma entidade lhe pode apontar".format(name),
                            resolves="`key: <slug>` no registo"))
        mode = d["access_mode"]
        if mode in ("owned", "replicated"):
            typed = [f for f in d["fields"] if (item_scalar(f, "type") or "unknown").strip().lower() not in ("unknown", "")]
            if not typed:
                gaps.append(gap("entities_to_create", "owned: fields[] typed",
                                "domínio `{}` ({}) sem `fields[]` com tipo".format(name, mode),
                                resolves="`fields[]` do rascunho L1 ou de design, com `type` ≠ unknown"))
            if d["fields"] and not any((item_scalar(f, "index") or "").strip() == "primary" for f in d["fields"]):
                gaps.append(gap("entities_to_create", "owned: index primary",
                                "domínio `{}` sem campo `index: primary`".format(name),
                                resolves="um `index: primary` em `fields[]`"))
        if mode in ("keep-in-place", "virtualized", "replicated"):
            if not d["has_access_contract"]:
                gaps.append(gap("entities_to_create", "external: access_contract",
                                "domínio `{}` ({}) sem `access_contract`".format(name, mode),
                                resolves="`access_contract { reads[] · writes[] · key[] · schema_owner }` (P-6)"))
            else:
                if not d["reads"]:
                    gaps.append(gap("entities_to_create", "external: reads[]",
                                    "domínio `{}` com `reads: []`".format(name), resolves="colunas lidas do L1"))
                if not d["writes"] and not d["readonly"]:
                    gaps.append(gap("entities_to_create", "external: writes[] | readonly",
                                    "domínio `{}` sem `writes[]` e sem `readonly: true`".format(name),
                                    resolves="`writes[]` ou `readonly: true` afirmativo"))
                if not d["key_nonempty"] and not d["key_open"]:
                    gaps.append(gap("entities_to_create", "external: key[]",
                                    "domínio `{}` sem `key[]` e sem `open: U-nnn`".format(name),
                                    resolves="chave de linha ou a Unknown que a bloqueia"))
        if mode in ("keep-in-place", "virtualized", "replicated", "owned") and not d["schema_owner"]:
            gaps.append(gap("entities_to_create", "schema_owner",
                            "domínio `{}` sem `schema_owner` com estado".format(name),
                            resolves="`schema_owner: {value, state, su_ref, open}`"))
        missing = _lines_missing_state_source(d["fields"] + d["reads"] + d["writes"])
        if missing:
            gaps.append(gap("entities_to_create", "line: state + source",
                            "domínio `{}`: {} linha(s) do dicionário sem `state` ou `source`".format(name, missing),
                            resolves="`state` (Assumed · Confirmed · Unknown) + locator por linha"))
    if sec is None:
        gaps.append(gap("entities_to_create", "section", "secção de entidades ausente do documento",
                        owner="implementation", resolves="renderizar a §4 a partir do registo"))
    return gaps


def check_flows(record: dict, sec: str | None) -> list[dict]:
    if sec is None:
        return []
    carriers = [e["name"] for e in record["entities"] if e["state_machine"] or e["approval"]]
    if carriers and re.search(r"\(none\)|\(nenhum\)", sec, re.I):
        return [gap("flows_to_implement", "(none) with state machines",
                    "secção diz `(none)` e {} entidade(s) aprovada(s) carregam máquina de estados ou aprovação: {}".format(
                        len(carriers), ", ".join(carriers[:4])),
                    owner="implementation",
                    resolves="por entidade: quem transiciona · o que valida · o que notifica · o que dispara (`not named` onde A7 não nomeia)")]
    return []


def check_security(sec: str | None) -> list[dict]:
    if sec is None:
        return []
    if has_role_matrix(sec):
        return []
    return [gap("security_implementation", "Papel × (Ecrã | Entidade) table",
                "secção sem tabela Papel × (Ecrã | Entidade) — a citação do craft não conta",
                owner="implementation", resolves="a matriz, com existência e alcance dos controlos lidos de A7")]


def check_integrations(sec: str | None) -> list[dict]:
    if sec is None:
        return []
    f = _fold(sec)
    has_auth = "autentic" in f or "authentic" in f
    has_secret = any(w in f for w in ("segredo", "custodia", "secret", "credenci", "armazenad", "stored",
                                      "vault", "cofre", "connection reference", "certificad"))
    named_gap = any(w in f for w in ("lacuna", "item aberto", "nao especificad", "not named", "unknown", "por nomear", "gap"))
    if (has_auth and has_secret) or named_gap:
        return []
    return [gap("integrations", "authentication + secret custody",
                "secção sem mecanismo de autenticação e custódia de segredos, e sem lacuna nomeada",
                owner="implementation", resolves="por integração: autenticação · custódia; ou a lacuna com dono")]


# ------------------------------------------------------------- orchestration

def validate(eng: Path, deliverable: str, rendered: Path, version_override: str | None = None) -> dict:
    D = _load_dashboard()
    state = json.loads((eng / "_state.json").read_text(encoding="utf-8")) if (eng / "_state.json").is_file() else {}
    pack = state.get("pack") or "pp"
    tpl = REPO / "library" / "packs" / pack / "deliverable-templates" / (deliverable + ".template.md")
    tpl_text = tpl.read_text(encoding="utf-8") if tpl.is_file() else ""
    slots = sufficiency_slots(tpl_text)
    result = {"tool": "render-validate.py " + TOOL_VERSION, "engagement": eng.name, "deliverable": deliverable,
              "file": rendered.name, "template": tpl.name if tpl.is_file() else None,
              "sufficiency_slots": slots, "blueprint": None, "gaps": [], "notes": []}
    if not slots:
        result["notes"].append("template sem bloco `sufficiency:` — nada a verificar por conteúdo")
        result["coverage"] = coverage_report(eng, rendered)
        return result
    md = rendered.read_text(encoding="utf-8") if rendered.is_file() else ""
    secs = sections(md)
    blocks = D.classify_decisions(D._read(eng / "decisions.md") or "")
    bp = D.blueprint_state(eng, blocks)
    chosen = None
    if version_override:
        m = re.search(r"(\d{1,3})", version_override)
        want = "v" + m.group(1).zfill(2) if m else ""
        chosen = next((v for v in bp.get("versions", []) if v["version"] == want), None)
        chosen = {"version": want, "rel": chosen["rel"]} if chosen else None
    elif bp.get("approved"):
        chosen = {"version": bp["approved"]["version"], "rel": bp["approved"]["rel"]}
    if chosen is None:
        result["notes"].append("sem blueprint aprovado — as regras de §4/§6 não têm registo contra que verificar (a spec está bloqueada por contrato)")
        record = {"domains": [], "entities": []}
    else:
        def loader(ver: str) -> str:
            for ext in ("yaml", "yml"):
                p = eng / "_blueprint" / "ux-blueprint_{}.{}".format(ver, ext)
                if p.is_file():
                    return D._read(p) or ""
            return ""
        record = read_record(D, D._read(eng / chosen["rel"]) or "", loader)
        result["blueprint"] = chosen["version"]
    gaps: list[dict] = []
    approved_invalid = (chosen is not None and bp.get("approved")
                        and bp["approved"]["version"] == chosen["version"]
                        and bp["approved"].get("valid", True) is False)
    if approved_invalid:
        # A4.5 (runtime hardening): an approval recorded over a structurally invalid version
        # is history, not a licence. The content rules still run -- collapsing the two
        # signals into "no approved blueprint" would HIDE the content gaps -- and the
        # structural failure is added as its own required gap, which is what blocks.
        blocking = bp["approved"].get("blocking") or []
        result["approved_invalid"] = {
            "version": bp["approved"]["version"],
            "codes": sorted({i["code"] for i in blocking}),
            "count": len(blocking)}
        gaps.append(gap(
            "blueprint", "blueprint aprovado: estrutura válida",
            "a versão aprovada {} falha a verificação estrutural ({} bloqueio(s): {}) — "
            "blueprint-contract.md → Validação estrutural".format(
                bp["approved"]["version"], len(blocking),
                ", ".join(sorted({i["code"] for i in blocking}))),
            resolves="refazer o desenho (/blueprint) e aprovar a nova versão"))

    if "entities_to_create" in slots and chosen is not None:
        gaps += check_entities(record, section_for(secs, "entities_to_create"))
    if "flows_to_implement" in slots:
        gaps += check_flows(record, section_for(secs, "flows_to_implement"))
    if "security_implementation" in slots:
        gaps += check_security(section_for(secs, "security_implementation"))
    if "integrations" in slots:
        gaps += check_integrations(section_for(secs, "integrations"))
    result["gaps"] = gaps
    result["record"] = {"domains": len(record["domains"]), "entities": len(record["entities"])}
    result["coverage"] = coverage_report(eng, rendered)
    return result


def coverage_line(result: dict) -> str:
    """Uma linha, separada da suficiência, e que nunca fala pela aprovação."""
    cov = result.get("coverage") or {}
    if not cov.get("evaluated"):
        return "[render-validate] cobertura: não avaliada ({})".format(
            cov.get("state") or "sem motor")
    if cov["contract_validity"] == "not_evaluated":
        return ("[render-validate] cobertura: sem revisão para este ficheiro — "
                "`not_evaluated`, que não é aprovação nem reprovação")
    return ("[render-validate] cobertura: {} · fontes {} · leitura nos dois sentidos {} · "
            "{} achado(s) — {} ({})".format(
                cov["coverage"], cov["source_review"], cov["semantic_review"],
                cov["findings"],
                "pode declarar-se completo" if cov["eligible"] else "não é completo",
                cov["record"] or "sem registo"))


def append_gaps(eng: Path, result: dict) -> Path | None:
    if not result["gaps"]:
        return None
    path = eng / "_render" / "render-gaps.md"
    header = "" if path.is_file() else "# Render Gaps — {}\n\n".format(eng.name)
    lines = [header, "\n## Validação {} — `render-validate.py` {} por conteúdo — `{}` (blueprint {})\n\n".format(
        now_iso(), TOOL_VERSION, result["file"], result.get("blueprint") or "—"),
        "| Deliverable | Slot / secção | Regra | Detalhe | Owner | O que resolveria |\n",
        "|---|---|---|---|---|---|\n"]
    for g in result["gaps"]:
        lines.append("| {} | `{}` | {} | {} | `{}` | {} |\n".format(
            result["deliverable"], g["slot"], g["rule"], g["detail"].replace("|", "\\|"), g["owner"], g["resolves"]))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write("".join(lines))
    return path


def resolve_target(file_path: str) -> tuple[Path, str, Path] | None:
    p = Path(file_path)
    m = DELIVERABLE_RE.match(p.name)
    if not m or p.parent.name != "_render":
        return None
    return p.parent.parent, m.group("deliverable"), p


def hook_main(raw: str) -> int:
    for i, ch in enumerate(raw):
        if ch in "{[":
            raw = raw[i:]
            break
    try:
        tool = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0
    if tool.get("tool_name") not in {"Write", "Edit"}:
        return 0
    file_path = (tool.get("tool_input") or {}).get("file_path") or ""
    target = resolve_target(file_path.replace("\\", "/"))
    if target is None:
        if re.search(r"_render[\\/].+\.md$", file_path.replace("\\", "/")):
            print("[render-validate] escrito: {} — não é um deliverable versionado, nada a validar".format(file_path), file=sys.stderr)
        return 0
    eng, deliverable, rendered = target
    try:
        result = validate(eng, deliverable, rendered)
        path = append_gaps(eng, result)
        n = len(result["gaps"])
        if n:
            print("[render-validate] {}: {} lacuna(s) por conteúdo ({}) → {}".format(
                rendered.name, n, ", ".join(sorted({g["slot"] for g in result["gaps"]})), path), file=sys.stderr)
        else:
            print("[render-validate] {}: 0 lacunas por conteúdo nas regras de `sufficiency:` ({})".format(
                rendered.name, ", ".join(result["sufficiency_slots"]) or "sem regras"), file=sys.stderr)
        print(coverage_line(result), file=sys.stderr)
    except Exception as exc:  # noqa: BLE001 — fail-open, never block a write
        print("[render-validate] verificação incompleta — {}: {}".format(type(exc).__name__, exc), file=sys.stderr)
    return 0


def cli_main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="render-validate.py",
                                 description="P-7: sufficiency of a rendered deliverable, checked by content")
    ap.add_argument("--engagement", required=True, help="slug or path")
    ap.add_argument("--deliverable", default="implementation-spec")
    ap.add_argument("--file", help="a specific rendered file (default: newest version)")
    ap.add_argument("--version", dest="bp_version", help="blueprint version to validate against (default: approved)")
    ap.add_argument("--dry-run", action="store_true", help="print, write nothing")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    args = ap.parse_args(argv)
    eng = Path(args.engagement)
    if not eng.is_dir():
        root = os.environ.get("AISA_ENGAGEMENTS_ROOT")
        eng = (Path(root) if root else REPO / "projects") / args.engagement
    if not eng.is_dir():
        print("[render-validate] engagement não resolvido: {}".format(args.engagement), file=sys.stderr)
        return 3
    if args.file:
        rendered = Path(args.file)
    else:
        cands = sorted(p for p in (eng / "_render").glob("*_{}_v*.md".format(args.deliverable))) if (eng / "_render").is_dir() else []
        if not cands:
            print("[render-validate] nenhum render de {} em {}/_render".format(args.deliverable, eng.name), file=sys.stderr)
            return 3
        rendered = cands[-1]
    result = validate(eng, args.deliverable, rendered, args.bp_version)
    if not args.dry_run:
        append_gaps(eng, result)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print("{} — {} — blueprint {} — {} lacuna(s)".format(eng.name, rendered.name, result.get("blueprint") or "—", len(result["gaps"])))
        for g in result["gaps"]:
            print("  - [{}] {}: {}".format(g["slot"], g["rule"], g["detail"]))
        for n in result["notes"]:
            print("  · " + n)
        print(coverage_line(result))
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if argv:
        return cli_main(argv)
    return hook_main(sys.stdin.read())


if __name__ == "__main__":
    sys.exit(main())
