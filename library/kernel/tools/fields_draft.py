#!/usr/bin/env python3
"""fields_draft.py — L1 column inventory → fields / access-contract DRAFT (aisa, P-6).

Deterministic motor of frente D. Reads one `<file>.extraction.json` produced by
`xlsx_extract.py` and writes `<file>.fields-draft.json` next to it in `_capture/`:
for every populated column, a candidate field or contract line — name, type, required,
key, role (write / computed / no-data), lineage, rules — each with its L1 locator and
the epistemic state `Assumed` (or `Unknown` where the L1 gives no name or no type).

What it carries and what it never does (docs/pp-pack-authoring/pilot/step-9a-onda-0-desenho-a5.md):

  D4  the draft is a CAPTURE artefact (locator class 1); this tool never writes into a
      blueprint YAML and never decides which record_authority domain a column belongs to.
  D6  name resolution: named_range → formula_ref → header → none. Headers are the LAST
      resort: pilot-1's `Inputs` has values where the extractor saw a header row, and
      `Outputs` has 4 headers in 76 columns.
  D7  type vocabulary text | number | date | datetime | boolean | choice | identifier |
      unknown; `mixed(...)` and `empty` are `unknown` with the reason; a validation list
      on the column makes a `choice` with its values; `default` is never inferred.
  D8  class → role: manual/input → write (someone types it), derived → computed with its
      lineage, empty-with-a-name → dictionary entry without data. The SHEET's role
      (register / report / reference) is the process model's judgement, not this tool's:
      only a `shape_hint` is emitted.
  D12 `disposition` is left null. ADOPT / MAP / DISMISS is the skill's judgement, per
      column, never the motor's.

Items are per COLUMN with `aliases[]` (pilot-1: 291 named ranges → 83 columns). Named
ranges that point at columns without data are listed apart — they are dictionary entries
the artefact carries but never filled, and the skill must dispose of them too.

Usage:
  python fields_draft.py <file.extraction.json> <out.fields-draft.json> [--force] [--log <capture-log>]
  python fields_draft.py --engagement <slug|path> [--file <name.xlsx>] [--force] [--log]

Idempotent: an existing draft with the same source sha256 and tool version is kept.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

TOOL_VERSION = "0.1.0"
ARTEFACT = "aisa.capture.fields-draft"
SOURCE_ARTEFACT = "aisa.capture.extraction"

TYPE_MAP = {"str": "text", "string": "text", "number": "number", "int": "number",
            "float": "number", "datetime": "datetime", "date": "date", "bool": "boolean",
            "boolean": "boolean"}
NAME_TYPES = ("text", "identifier", "choice")

# `Sheet!$C$9:$C$1469` · `'My Sheet'!$A$1:$J$5` · `Outputs!$C$6`
TARGET_RE = re.compile(
    r"^(?:'(?P<q>[^']+)'|(?P<u>[^'!]+))!\$?(?P<c1>[A-Z]{1,3})\$?(?P<r1>\d+)"
    r"(?::\$?(?P<c2>[A-Z]{1,3})\$?(?P<r2>\d+))?$")
# a named-range identifier inside a formula: has an underscore, is not an Excel
# function prefix (`_xlfn.`), not an R1C1 token and not a sheet reference
NAMED_REF_RE = re.compile(r"(?<![\w.!'])([A-Za-zÀ-ÿ][\w.À-ÿ]*_[\w.À-ÿ]+)(?![\w.]*\s*[!(])")
NUMERIC_RE = re.compile(r"^[-+]?\d+([.,]\d+)?([eE][-+]?\d+)?$")
DATEISH_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([ T]\d{2}:\d{2}(:\d{2})?)?$")
RANGE_RE = re.compile(r"^\$?([A-Z]{1,3})\$?(\d+)(?::\$?([A-Z]{1,3})\$?(\d+))?$")


def utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass


def now_iso() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat()


def col_index(letters: str) -> int:
    n = 0
    for ch in letters:
        n = n * 26 + (ord(ch) - 64)
    return n


def parse_target(target: str) -> dict | None:
    m = TARGET_RE.match((target or "").strip())
    if not m:
        return None
    sheet = m.group("q") or m.group("u")
    c1, r1 = m.group("c1"), int(m.group("r1"))
    c2, r2 = m.group("c2") or c1, int(m.group("r2") or r1)
    return {"sheet": sheet, "c1": c1, "r1": r1, "c2": c2, "r2": r2,
            "single_column": c1 == c2 and r2 > r1, "single_cell": c1 == c2 and r1 == r2}


def header_is_a_name(header) -> bool:
    if not isinstance(header, str):
        return False
    h = header.strip()
    if not h or h in ("*", "None", "-", "—"):
        return False
    if NUMERIC_RE.match(h) or DATEISH_RE.match(h):
        return False
    return True


def named_refs(pattern: str, sheet_names: set[str] | None = None) -> list[str]:
    """Named-range identifiers a formula references. A sheet name with an underscore
    (`Dayly_extraction!A1`) and a function (`_xlfn.XLOOKUP(`) are not names."""
    out: list[str] = []
    for tok in NAMED_REF_RE.findall(pattern or ""):
        if tok.startswith("_") or tok.lower().startswith("_xl"):
            continue
        if sheet_names and tok in sheet_names:
            continue
        if re.fullmatch(r"R\[?-?\d*\]?C\[?-?\d*\]?", tok):
            continue
        if tok not in out:
            out.append(tok)
    return out


def validation_covers(v: dict, sheet_col: str) -> bool:
    for part in re.split(r"[ ,]+", (v.get("range") or "").strip()):
        m = RANGE_RE.match(part)
        if not m:
            continue
        a, b = col_index(m.group(1)), col_index(m.group(3) or m.group(1))
        if a <= col_index(sheet_col) <= b:
            return True
    return False


def list_values(formula1: str) -> list[str]:
    f = (formula1 or "").strip()
    if f.startswith('"') and f.endswith('"') and len(f) >= 2:
        return [x.strip() for x in f[1:-1].split(",") if x.strip()]
    return []


# ---------------------------------------------------------------- the draft

def build_draft(extraction: dict, extraction_name: str, draft_name: str,
                generated_at: str | None = None) -> dict:
    if extraction.get("artefact") != SOURCE_ARTEFACT:
        raise ValueError("not an aisa L1 extraction: artefact={!r}".format(
            extraction.get("artefact")))
    identity = extraction.get("identity") or {}
    wb = extraction.get("workbook") or {}
    ranges = wb.get("named_ranges") or []
    sheets = extraction.get("sheets") or []
    populated = {s["name"]: {c["column"] for c in (s.get("columns") or [])} for s in sheets}
    sheet_names = set(populated)

    # --- named-range index -------------------------------------------------------
    by_col: dict[tuple[str, str], list[str]] = {}
    without_data: list[dict] = []
    non_column: list[dict] = []
    seen_names: set[tuple[str, str]] = set()
    for nr in ranges:
        name, target = nr.get("name") or "", nr.get("target") or ""
        key = (name, target)
        if key in seen_names:           # the same name repeated across scopes
            continue
        seen_names.add(key)
        t = parse_target(target)
        if t is None or not t["single_column"]:
            non_column.append({"name": name, "target": target,
                               "kind": "cell" if (t and t["single_cell"]) else
                                       "external" if target.startswith("[") or target.startswith('"') else
                                       "broken" if "#REF" in target else "range"})
            continue
        if t["sheet"] in populated and t["c1"] not in populated[t["sheet"]]:
            without_data.append({"name": name, "target": target, "sheet": t["sheet"],
                                 "column": t["c1"]})
            continue
        if t["sheet"] not in populated:
            non_column.append({"name": name, "target": target, "kind": "unknown-sheet"})
            continue
        by_col.setdefault((t["sheet"], t["c1"]), [])
        if name not in by_col[(t["sheet"], t["c1"])]:
            by_col[(t["sheet"], t["c1"])].append(name)

    # formula references to named ranges, workbook-wide (key candidates)
    ref_count: dict[str, int] = {}

    # --- dimensions of the `A_B_C` convention --------------------------------------
    # Only over names that point at a COLUMN (with or without data): a broken `#REF!`
    # name or a cell anchor is not a dictionary entry and must not invent a dimension.
    dims: dict[int, set[str]] = {1: set(), 2: set(), 3: set()}
    three = 0
    column_names = {n for names in by_col.values() for n in names} | {e["name"] for e in without_data}
    for name in sorted(column_names):
        parts = name.split("_")
        if len(parts) == 3 and all(parts):
            three += 1
            for i, p in enumerate(parts, 1):
                dims[i].add(p)

    out_sheets: list[dict] = []
    totals = {"columns": 0, "named": 0, "unnamed": 0, "computed": 0, "write": 0,
              "choice": 0, "identifier": 0, "unknown_type": 0}
    for si, s in enumerate(sheets):
        cols = s.get("columns") or []
        validations = s.get("validations") or []
        profile: dict[str, int] = {}
        for c in cols:
            profile[c.get("class") or "?"] = profile.get(c.get("class") or "?", 0) + 1
        if not cols:
            hint = "empty"
        elif set(profile) <= {"derived", "empty"}:
            hint = "report"
        elif profile.get("derived") and profile.get("manual"):
            hint = "register"
        elif set(profile) <= {"input", "empty"}:
            hint = "input-extract"
        else:
            hint = "mixed"
        out_cols: list[dict] = []
        for ci, c in enumerate(cols):
            col = c.get("column") or ""
            klass = c.get("class") or ""
            aliases = list(by_col.get((s["name"], col), []))
            formula = c.get("formula") or {}
            patterns = [p.get("pattern", "") for p in (formula.get("patterns") or [])]
            if formula.get("dominant_pattern") and formula["dominant_pattern"] not in patterns:
                patterns.insert(0, formula["dominant_pattern"])
            refs: list[str] = []
            for p in patterns:
                for r in named_refs(p, sheet_names):
                    if r not in refs:
                        refs.append(r)
                    ref_count[r] = ref_count.get(r, 0) + 1
            # -- name (D6) --
            if aliases:
                name, basis = sorted(aliases, key=lambda x: (len(x), x))[0], "named_range"
            elif klass == "derived" and refs:
                name, basis = refs[0], "formula_ref"
            elif header_is_a_name(c.get("header")):
                name, basis = c["header"].strip(), "header"
            else:
                name, basis = "{}!{}".format(s["name"], col), "none"
            # -- type (D7) --
            inferred = (c.get("inferred_type") or "").strip()
            rules: list[str] = []
            if inferred in TYPE_MAP:
                ftype, tbasis = TYPE_MAP[inferred], "inferred_type={}".format(inferred)
            elif inferred.startswith("mixed"):
                ftype, tbasis = "unknown", "tipos mistos na origem: {}".format(inferred)
                rules.append("tipos mistos na origem ({}) — a origem não fixa o tipo".format(inferred))
            elif inferred == "empty" or not inferred:
                ftype, tbasis = "unknown", "sem valores na origem (header only)"
            else:
                ftype, tbasis = "unknown", "inferred_type={} sem mapa".format(inferred)
            values: list[str] = []
            for v in validations:
                if not validation_covers(v, col):
                    continue
                if (v.get("type") or "") == "list":
                    vals = list_values(v.get("formula1") or "")
                    if vals:
                        values = vals
                        rules.append("lista ({}): {}".format(v.get("range"), ", ".join(vals)))
                    else:
                        rules.append("lista ({}): {}".format(v.get("range"), v.get("formula1")))
                else:
                    rules.append("{}: {} {} {}".format(v.get("type"), v.get("operator") or "",
                                                       v.get("formula1") or "",
                                                       v.get("formula2") or "").strip())
            if values and ftype in ("text", "unknown"):
                ftype, tbasis = "choice", "validação list na coluna ({})".format(
                    "; ".join(r for r in rules if r.startswith("lista")))
            key_like = bool(c.get("key_like"))
            if key_like and ftype in ("text", "unknown"):
                ftype = "identifier"
                tbasis += " + key_like"
            nonempty = int(c.get("rows_nonempty") or 0)
            nulls = int(c.get("nulls") or 0)
            distinct = int(c.get("distinct") or 0)
            required = bool(nonempty and nulls == 0)
            if key_like and required and distinct == nonempty:
                index = "primary"
            elif key_like:
                index = "candidate"
            else:
                index = "none"
            # -- role (D8) --
            if klass == "derived":
                role = "computed"
            elif klass in ("manual", "input"):
                role = "write"
            elif klass == "empty":
                role = "no-data"
            else:
                role = "unknown"
            lineage = list(refs)
            for r in (c.get("reads") or []):
                if "!" in r and r not in lineage:
                    lineage.append(r.split("!")[0] + "!" + r.split("!", 1)[1])
            state = "Unknown" if (basis == "none" or ftype == "unknown") else "Assumed"
            item = {
                "column": col, "name": name, "name_basis": basis, "aliases": aliases,
                "header": c.get("header"),
                "type": ftype, "type_basis": tbasis, "values": values,
                "required": required,
                "required_basis": "nulls={} em {} linhas com valor".format(nulls, nonempty),
                "default": None,
                "index": index, "key_like": key_like,
                "class": klass, "class_basis": c.get("class_basis") or "",
                "role": role, "computed": klass == "derived",
                "lineage": lineage[:40], "rules": rules,
                "cardinality": {"rows_nonempty": nonempty, "nulls": nulls, "distinct": distinct},
                "state": state,
                "source": "_capture/{}#{}/{}".format(draft_name, s["name"], col),
                "locator": "{}#sheets[{}].columns[{}]".format(extraction_name, si, ci),
                "disposition": None,
            }
            out_cols.append(item)
            totals["columns"] += 1
            totals["named" if basis != "none" else "unnamed"] += 1
            if role == "computed":
                totals["computed"] += 1
            if role == "write":
                totals["write"] += 1
            if ftype == "choice":
                totals["choice"] += 1
            if ftype == "identifier":
                totals["identifier"] += 1
            if ftype == "unknown":
                totals["unknown_type"] += 1
        out_sheets.append({
            "name": s["name"], "state": s.get("state"), "dimensions": s.get("dimensions"),
            "header_row": s.get("header_row"), "header_basis": s.get("header_basis"),
            "data_rows": [s.get("data_start_row"), s.get("data_end_row")],
            "class_profile": profile, "shape_hint": hint,
            "shape_hint_basis": "perfil de classes das colunas; o papel da folha (registo, "
                                "relatório, referência) é julgamento do process-model.md §1",
            "columns": out_cols,
        })

    key_candidates = sorted(ref_count.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
    dimensions = [{"position": i, "cardinality": len(v), "values": sorted(v)}
                  for i, v in dims.items() if v]
    covered = len(by_col)
    return {
        "artefact": ARTEFACT,
        "tool": {"name": "fields_draft.py", "version": TOOL_VERSION},
        "generated_at": generated_at or now_iso(),
        "source": {
            "extraction": extraction_name,
            "extraction_tool": extraction.get("tool") or {},
            "filename": identity.get("filename"),
            "sha256": identity.get("sha256"),
        },
        "status": "ok",
        "dictionary": {
            "named_ranges": len(ranges),
            "distinct_name_target_pairs": len(seen_names),
            "columns_covered": covered,
            "max_aliases_per_column": max((len(v) for v in by_col.values()), default=0),
            "three_segment_names": three,
            "dimensions": dimensions,
            "entries_without_data": sorted(without_data, key=lambda x: x["name"]),
            "non_column_targets": non_column,
            "key_candidates": [{"name": n, "formula_references": k} for n, k in key_candidates],
        },
        "totals": totals,
        "sheets": out_sheets,
        "julgamento": (
            "Rascunho determinístico do inventário L1. Nenhuma linha é campo, leitura ou escrita "
            "de um domínio até a skill (aisa-blueprint step 4) lhe dar disposição ADOPT / MAP / "
            "DISMISS e a copiar para record_authority[].fields[] ou access_contract; o estado "
            "por linha é Assumed (ou Unknown sem nome/tipo) até confirmação do dono. `default` "
            "nunca é inferido; a separação métrica/porto e contraparte/prefixo técnico nas "
            "dimensões é julgamento."),
    }


# ---------------------------------------------------------------- I/O

def _atomic_write(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)


def summary_line(draft: dict) -> str:
    t, d = draft["totals"], draft["dictionary"]
    return ("{} sheets, {} columns — named {} · unnamed {} · write {} · computed {} · choice {} "
            "· identifier {} · unknown type {} · named ranges {} → {} columns, {} without data"
            ).format(len(draft["sheets"]), t["columns"], t["named"], t["unnamed"], t["write"],
                     t["computed"], t["choice"], t["identifier"], t["unknown_type"],
                     d["named_ranges"], d["columns_covered"], len(d["entries_without_data"]))


def draft_one(extraction_path: Path, out_path: Path, force: bool = False,
              log_path: Path | None = None) -> tuple[int, str]:
    if not extraction_path.is_file():
        return 2, "extraction not found: {}".format(extraction_path)
    try:
        extraction = json.loads(extraction_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return 2, "unreadable extraction {}: {}".format(extraction_path.name, exc)
    if extraction.get("status") not in (None, "ok"):
        return 2, "extraction status={} — no draft (fix the extraction first)".format(
            extraction.get("status"))
    sha = (extraction.get("identity") or {}).get("sha256")
    if out_path.is_file() and not force:
        try:
            prev = json.loads(out_path.read_text(encoding="utf-8"))
            if (prev.get("source", {}).get("sha256") == sha
                    and (prev.get("tool") or {}).get("version") == TOOL_VERSION):
                return 0, "unchanged (same source sha256 and tool version): {}".format(out_path.name)
        except (OSError, json.JSONDecodeError):
            pass
    try:
        draft = build_draft(extraction, extraction_path.name, out_path.name)
    except ValueError as exc:
        return 2, str(exc)
    _atomic_write(out_path, draft)
    line = summary_line(draft)
    if log_path is not None:
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with log_path.open("a", encoding="utf-8") as fh:
                fh.write("| {} | L1b | {} | fields-draft | {} · sha256 {} |\n".format(
                    now_iso(), draft["source"].get("filename") or extraction_path.name,
                    line, (sha or "")[:8]))
        except OSError:
            pass
    return 0, "{}: {}".format(out_path.name, line)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def resolve_engagement(arg: str) -> Path | None:
    p = Path(arg)
    if p.is_dir():
        return p
    root = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    base = Path(root) if root else (repo_root() / "projects")
    cand = base / arg
    return cand if cand.is_dir() else None


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    ap = argparse.ArgumentParser(
        prog="fields_draft.py",
        description="aisa P-6: L1 column inventory -> fields / access-contract draft (Assumed per line)")
    ap.add_argument("paths", nargs="*", help="<file.extraction.json> <out.fields-draft.json>")
    ap.add_argument("--engagement", help="slug or path: draft every xlsx extraction in _capture/")
    ap.add_argument("--file", help="with --engagement: only this workbook (file name)")
    ap.add_argument("--force", action="store_true", help="rewrite even if the source is unchanged")
    ap.add_argument("--log", nargs="?", const="", default=None, metavar="PATH",
                    help="append a line to the capture log (default: <engagement>/_capture/_capture-log.md)")
    ap.add_argument("--version", action="version", version="fields_draft.py " + TOOL_VERSION)
    args = ap.parse_args(argv)

    jobs: list[tuple[Path, Path, Path | None]] = []
    if args.engagement:
        eng = resolve_engagement(args.engagement)
        if eng is None:
            print("[fields_draft] engagement não resolvido: {}".format(args.engagement), file=sys.stderr)
            return 3
        cap = eng / "_capture"
        log = None
        if args.log is not None:
            log = Path(args.log) if args.log else (cap / "_capture-log.md")
        for p in sorted(cap.glob("*.extraction.json")):
            if not re.search(r"\.xls[xm]\.extraction\.json$", p.name, re.I):
                continue
            if args.file and not p.name.startswith(args.file):
                continue
            jobs.append((p, cap / p.name.replace(".extraction.json", ".fields-draft.json"), log))
        if not jobs:
            print("[fields_draft] nenhuma extracção xlsx em {}".format(cap), file=sys.stderr)
            return 3
    else:
        if len(args.paths) != 2:
            ap.error("needs <file.extraction.json> <out.fields-draft.json>, or --engagement <slug>")
        log = Path(args.log) if args.log else None
        jobs.append((Path(args.paths[0]), Path(args.paths[1]), log))

    rc = 0
    for src, dst, log in jobs:
        code, msg = draft_one(src, dst, args.force, log)
        print(("[fields_draft] " if code else "") + msg, file=sys.stderr if code else sys.stdout)
        rc = max(rc, code)
    return rc


if __name__ == "__main__":
    sys.exit(main())
