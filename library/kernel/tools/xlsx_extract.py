#!/usr/bin/env python3
"""xlsx_extract.py — aisa process-capture: Layer 1 (deterministic extraction) + Layer 3 (replay).

Kernel asset (library/kernel/tools/). Read + executed at runtime, never edited at runtime.
Dependencies: Python 3.10+, openpyxl. No LLM, no network, no writes outside the given output paths.

Usage:
  L1 extract : python xlsx_extract.py <input.xlsx> <out.extraction.json> [--force] [--log <capture-log.md>]
  L3 replay  : python xlsx_extract.py --replay <input.xlsx> <extraction.json> <out.replay.md> [--log <capture-log.md>]

Contract (PROCESS_CAPTURE_SPEC.md):
- L1 extracts structure/logic only from what the file proves. Unreadable file -> status:"failed" JSON, never guessed.
- L1 caches on SHA-256: same hash as stored in an existing extraction JSON -> "cache-hit", no rewrite (unless --force).
- L3 is a fixed battery of checks, NOT a formula engine. No check = no claim; unsupported formulas -> "not replayable".
- Exit codes: 0 ok/cache-hit/failed-artefact-written, 2 usage error, 3 stale extraction on replay.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import gc
import re
import sys
import zipfile
from collections import Counter, defaultdict

try:
    import openpyxl
    from openpyxl import load_workbook
    from openpyxl.utils import get_column_letter, column_index_from_string
    from openpyxl.worksheet.formula import ArrayFormula
except ImportError:  # pragma: no cover
    print("xlsx_extract.py requires openpyxl (pip install openpyxl)", file=sys.stderr)
    sys.exit(2)

TOOL_VERSION = "1.6.0"
ARTEFACT_ID = "aisa.capture.extraction"

MAX_TOP_VALUES = 5
MAX_PATTERNS_PER_COLUMN = 5
MAX_EXCEPTION_CELLS = 20
MAX_DUP_VALUES = 20
MAX_CELLS_PER_DUP = 10
MAX_WHITESPACE_CELLS = 30
MAX_COMMENTS = 100
MAX_MISS_EXAMPLES = 5
MAX_OLDEST_ROWS = 5
MAX_SCAN_ROWS = 5_000           # per-sheet row cap for cell-level scans (owner's ruling 2026-09-16:
                                # calculation logic repeats — a table computing past this row carries
                                # the same formulas as the rows above it)
MAX_DISTINCT = 10_000           # per-column cap on the distinct-value counter (counts stay true)
BIG_SHEET_CELLS = 400_000
VALUE_TRUNC = 80

FIXED_AGE_BANDS = (30, 60, 90, 120, 180)
STALE_FILE_DAYS = 30

KEY_HEADER_RE = re.compile(r"(?i)(?:^|[^a-z])(id|key|code|ref|ticket|chave|c[oó]digo|n[ºo°]|num(?:ber|ero)?)(?:$|[^a-z])")
ARCHIVE_NAME_RE = re.compile(r"(?i)(closed|conclus|arquiv|hist[oó]r|archive|done|fechad)")
VOLATILE_RE = re.compile(r"(?i)\b(TODAY|NOW|RAND|RANDBETWEEN|RANDARRAY)\s*\(")
NOT_REPLAYABLE_RE = re.compile(r"(?i)\b(INDIRECT|OFFSET)\s*\(|\[\d+\]")  # dynamic refs / external workbook markers

_SHEETNAME = r"(?:'(?:[^']|'')+'|[A-Za-z_\u00C0-\u024F][\w.\u00C0-\u024F]{0,30})"
REF_RE = re.compile(
    rf"(?<![\w$:!.])(?:(?P<sheet>{_SHEETNAME})!)?"
    r"(?P<body>\$?[A-Z]{1,3}\$?\d+(?::\$?[A-Z]{1,3}\$?\d+)?|\$?[A-Z]{1,3}:\$?[A-Z]{1,3}|\$?\d+:\$?\d+)"
    r"(?![\w(])"
)
STRING_SEG_RE = re.compile(r'"(?:[^"]|"")*"')
MAX_COL = 16384
MAX_ROW = 1048576


# ---------------------------------------------------------------- utilities

def utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def now_iso() -> str:
    return dt.datetime.now().isoformat(timespec="seconds")


def json_default(value):
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return value.isoformat()
    return str(value)


def short(value, limit: int = VALUE_TRUNC) -> str:
    text = value.isoformat() if isinstance(value, (dt.datetime, dt.date, dt.time)) else str(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def append_log(log_path: str | None, layer: str, filename: str, event: str, detail: str) -> None:
    if not log_path:
        return
    new = not os.path.exists(log_path)
    with open(log_path, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Capture log\n\n| timestamp | layer | file | event | detail |\n|---|---|---|---|---|\n")
        fh.write(f"| {now_iso()} | {layer} | {filename} | {event} | {detail} |\n")


def cell_kind(value) -> str:
    if value is None or value == "":
        return "empty"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, (dt.datetime, dt.date, dt.time)):
        return "datetime"
    if isinstance(value, str):
        return "str"
    return "other"


def formula_text(cell) -> str | None:
    """Raw formula string of a cell in a formulas-workbook, or None."""
    if cell.data_type != "f":
        return None
    v = cell.value
    if isinstance(v, ArrayFormula):
        return v.text or ""
    return v if isinstance(v, str) else None


# ------------------------------------------------- A1 -> R1C1 normalization

def _split_strings(formula: str):
    """Yield (is_string, segment) pairs so refs inside string literals are never touched."""
    pos = 0
    for m in STRING_SEG_RE.finditer(formula):
        if m.start() > pos:
            yield False, formula[pos:m.start()]
        yield True, m.group(0)
        pos = m.end()
    if pos < len(formula):
        yield False, formula[pos:]


def _endpoint_r1c1(col: str | None, col_abs: bool, row: str | None, row_abs: bool,
                   base_row: int, base_col: int) -> str:
    parts = []
    if row is not None:
        r = int(row)
        if row_abs:
            parts.append(f"R{r}")
        else:
            d = r - base_row
            parts.append(f"R[{d}]" if d else "R")
    if col is not None:
        c = column_index_from_string(col)
        if col_abs:
            parts.append(f"C{c}")
        else:
            d = c - base_col
            parts.append(f"C[{d}]" if d else "C")
    return "".join(parts)


_ENDPOINT_RE = re.compile(r"(\$?)([A-Z]{1,3})?(\$?)(\d+)?")


def _ref_body_to_r1c1(body: str, base_row: int, base_col: int) -> str | None:
    """Convert one A1 ref body ('A2', '$A$1:$F$9', '$A:$F', '2:4') to relative R1C1. None = leave as-is."""
    out = []
    for endpoint in body.split(":"):
        m = _ENDPOINT_RE.fullmatch(endpoint)
        if not m:
            return None
        d1, col, d2, row = m.groups()
        if col is None and row is None:
            return None
        if col is not None and column_index_from_string(col) > MAX_COL:
            return None
        if row is not None and int(row) > MAX_ROW:
            return None
        # '$A' -> d1 before col; for row-only '$2' the '$' lands in d1 as well
        col_abs = bool(d1) if col is not None else False
        row_abs = bool(d2) if col is not None else bool(d1)
        out.append(_endpoint_r1c1(col, col_abs, row, row_abs, base_row, base_col))
    return ":".join(out)


def normalize_formula(formula: str, base_row: int, base_col: int) -> str:
    """Normalize every A1 reference to R1C1 relative form -> fill-down copies collapse to one pattern."""
    result = []
    for is_string, seg in _split_strings(formula):
        if is_string:
            result.append(seg)
            continue

        def repl(m: re.Match) -> str:
            converted = _ref_body_to_r1c1(m.group("body"), base_row, base_col)
            if converted is None:
                return m.group(0)
            sheet = m.group("sheet")
            return f"{sheet}!{converted}" if sheet else converted

        result.append(REF_RE.sub(repl, seg))
    return "".join(result)


def iter_refs(formula: str):
    """Yield (sheet_or_None, body) for every A1 reference outside string literals."""
    for is_string, seg in _split_strings(formula):
        if is_string:
            continue
        for m in REF_RE.finditer(seg):
            body = m.group("body")
            if _ref_body_to_r1c1(body, 1, 1) is None:
                continue
            sheet = m.group("sheet")
            if sheet and sheet.startswith("'"):
                sheet = sheet[1:-1].replace("''", "'")
            yield sheet, body


# ------------------------------------------------------------ L1 extraction

def content_rows(path: str) -> dict[str, int]:
    """Last row carrying a value or a formula, per sheet, read from the package XML in streaming.

    A sheet whose columns were formatted whole declares every row of the grid — the workbook that
    forced this declares `A1:AE1048576` for 1.1M cells, and one of its sheets declares 63 461 rows
    for NINE with values. Asking the XML first costs seconds and constant memory, and it separates
    the empty grid (drop it, no loss) from a genuinely long table (cap it, and say so).

    Returns {} on any parsing trouble: the caller then falls back to the declared dimension.
    """
    import xml.etree.ElementTree as ET
    R_NS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    out: dict[str, int] = {}
    try:
        with zipfile.ZipFile(path) as zf:
            names = set(zf.namelist())
            # attribute ORDER differs between writers (Excel: Id Type Target; openpyxl: Type Target Id),
            # so this parses the XML instead of matching its text
            target = {}
            for rel in ET.fromstring(zf.read("xl/_rels/workbook.xml.rels")):
                if rel.get("Id"):
                    target[rel.get("Id")] = rel.get("Target") or ""
            for sheet in ET.fromstring(zf.read("xl/workbook.xml")).iter():
                if sheet.tag.rsplit("}", 1)[-1] != "sheet":
                    continue
                name, rid = sheet.get("name"), sheet.get(R_NS + "id")
                if not name or not rid:
                    continue
                tgt = target.get(rid, "")
                member = tgt.lstrip("/") if tgt.startswith("/") else "xl/" + tgt
                if member not in names:
                    continue
                last = cur = 0
                with zf.open(member) as fh:
                    for event, el in ET.iterparse(fh, events=("start", "end")):
                        tag = el.tag.rsplit("}", 1)[-1]
                        if event == "start":
                            if tag == "row":
                                cur = int(el.get("r") or 0)
                        else:
                            # `v` covers numbers and shared strings (Excel), `is` covers inline
                            # strings (openpyxl and some exporters), `f` covers formula-only cells
                            if tag in ("v", "f", "is") and cur > last:
                                last = cur
                            if tag == "row":
                                el.clear()
                out[name] = last
    except Exception:
        return {}
    return out


def scan_bounds(ws, data_start: int, content_end: int | None = None) -> tuple[int, int, int, bool]:
    """(effective_end, declared_end, content_end, truncated) for every cell-level scan of this sheet.

    Three numbers, because they answer different questions: what the file DECLARES (grid, inflated
    by whole-column formatting), where its CONTENT actually ends (`content_rows`), and how far this
    pass went. `ws.cell(r, c)` CREATES the cell when it does not exist, so scanning the declared
    grid cost 16.3 GB of peak and a MemoryError when the machine had no slack.

    `truncated` is true only when real content was cut — never for dropping an empty grid.
    """
    declared = ws.max_row or data_start
    content = declared if content_end is None else max(content_end, data_start)
    end = min(content, data_start + MAX_SCAN_ROWS - 1)
    return end, declared, content, end < content


def sheet_scan_end(extraction: dict, name: str, ws=None) -> int:
    """The last row any downstream pass may touch on this sheet: the effective end the L1 recorded,
    or the same cap computed live when there is no record."""
    for s in extraction.get("sheets", []):
        if s["name"] == name:
            return s.get("data_end_row") or 1
    if ws is None:
        return MAX_SCAN_ROWS
    return min(ws.max_row or 1, MAX_SCAN_ROWS)


def detect_header(ws) -> tuple[int, int, str]:
    """Return (header_row, data_start_row, basis). Deterministic heuristic, basis recorded."""
    fp = ws.freeze_panes
    if fp:
        m = re.match(r"[A-Z]+(\d+)$", str(fp))
        if m and int(m.group(1)) >= 2:
            frozen_row = int(m.group(1))
            return frozen_row - 1, frozen_row, "frozen-pane"
    for r in range(1, min(ws.max_row or 1, 10) + 1):
        values = [c.value for c in ws[r]]
        nonempty = [v for v in values if v not in (None, "")]
        if len(nonempty) >= 2 and sum(isinstance(v, str) for v in nonempty) / len(nonempty) >= 0.6:
            return r, r + 1, "string-density"
    return 1, 2, "fallback-row-1"


def scan_columns(ws_data, ws_formula, header_row: int, data_start: int, data_end: int,
                 truncated: bool = False):
    """Per-column stats + formula patterns. Single pass over data rows on both workbook views.

    When the sheet was truncated (`scan_bounds`), every count and range below describes the SAMPLE
    that was scanned, never the column: a `max_date` read from the first rows of a series would
    otherwise pass for the end of the series. Each record says which of the two it is.
    """
    max_col = ws_data.max_column or 0
    columns = []
    for col_idx in range(1, max_col + 1):
        letter = get_column_letter(col_idx)
        header_val = ws_data.cell(row=header_row, column=col_idx).value
        header = str(header_val).strip() if header_val not in (None, "") else None

        kinds = Counter()
        values = Counter()
        values_capped = False
        num_min = num_max = None          # running min/max: keeping every number only to compare
        date_min = date_max = None        # two of them is what turned a wide sheet into gigabytes
        nulls = 0
        formulas: list[tuple[str, str]] = []          # (coord, raw formula)
        typed_cells: list[tuple[str, object]] = []    # (coord, value)

        for r in range(data_start, data_end + 1):
            dcell = ws_data.cell(row=r, column=col_idx)
            v = dcell.value
            kind = cell_kind(v)
            if kind == "empty":
                nulls += 1
            else:
                kinds[kind] += 1
                key = short(v)
                if key in values or len(values) < MAX_DISTINCT:
                    values[key] += 1
                else:
                    values_capped = True   # the counter stops growing; `rows_nonempty` stays true
                if kind == "number":
                    num_min = v if num_min is None or v < num_min else num_min
                    num_max = v if num_max is None or v > num_max else num_max
                elif kind == "datetime" and isinstance(v, (dt.datetime, dt.date)):
                    date_min = v if date_min is None or v < date_min else date_min
                    date_max = v if date_max is None or v > date_max else date_max
            raw = formula_text(ws_formula.cell(row=r, column=col_idx))
            if raw is not None:
                formulas.append((f"{letter}{r}", raw))
            elif kind != "empty":
                typed_cells.append((f"{letter}{r}", v))

        nonempty = sum(kinds.values())
        if header is None and nonempty == 0 and not formulas:
            continue

        if nonempty:
            ranked = kinds.most_common()
            inferred = ranked[0][0]
            mixed = len(ranked) > 1 and ranked[1][1] >= max(1, round(0.10 * nonempty))
            if mixed:
                inferred = f"mixed({ranked[0][0]},{ranked[1][0]})"
        else:
            inferred, mixed = "empty", False

        record = {
            "column": letter,
            "stats_scope": "sample" if truncated else "column",
            "header": header,
            "inferred_type": inferred,
            "rows_nonempty": nonempty,
            "nulls": nulls,
            "distinct": len(values),
            "top_values": [{"value": v, "count": n} for v, n in values.most_common(MAX_TOP_VALUES)],
            "formula_count": len(formulas),
            "typed_count": len(typed_cells),
        }
        if values_capped:
            record["distinct_capped"] = MAX_DISTINCT   # distinct counted up to here, not beyond
        if num_min is not None:
            record["min"], record["max"] = num_min, num_max
        if date_min is not None:
            record["min_date"], record["max_date"] = short(date_min), short(date_max)
        record["_formulas"] = formulas
        record["_typed"] = typed_cells
        record["_mixed"] = mixed
        columns.append(record)
    return columns


def analyse_formulas(columns, data_start: int) -> None:
    """Group per-column formulas by R1C1 pattern; exceptions = manual overrides / divergent logic."""
    for col in columns:
        formulas = col.pop("_formulas")
        typed = col.pop("_typed")
        if not formulas:
            if typed:
                col["formula"] = None
            continue

        patterns = Counter()
        norm_by_cell = []
        for coord, raw in formulas:
            row = int(re.sub(r"[A-Z]+", "", coord))
            base_col = column_index_from_string(re.sub(r"\d+", "", coord))
            norm = normalize_formula(raw, row, base_col)
            patterns[norm] += 1
            norm_by_cell.append((coord, raw, norm))

        dominant, dom_count = patterns.most_common(1)[0]
        derived = len(formulas) >= max(1, len(typed))
        divergent = [
            {"cell": coord, "formula": short(raw, 160)}
            for coord, raw, norm in norm_by_cell if norm != dominant
        ][:MAX_EXCEPTION_CELLS]
        overrides = (
            [{"cell": coord, "value": short(v)} for coord, v in typed][:MAX_EXCEPTION_CELLS]
            if derived and typed else []
        )
        stray = (
            [{"cell": coord, "formula": short(raw, 160)} for coord, raw in formulas][:MAX_EXCEPTION_CELLS]
            if not derived else []
        )
        col["formula"] = {
            "count": len(formulas),
            "dominant_pattern": dominant,
            "dominant_count": dom_count,
            "coverage_of_formulas": round(dom_count / len(formulas), 4),
            "coverage_of_nonempty": round(dom_count / max(1, len(formulas) + len(typed)), 4),
            "patterns": [
                {"pattern": p, "count": n}
                for p, n in patterns.most_common(MAX_PATTERNS_PER_COLUMN)
            ],
            "other_pattern_count": max(0, len(patterns) - MAX_PATTERNS_PER_COLUMN),
            "exceptions": {
                "divergent_formulas": divergent,
                "typed_overrides": overrides,
                "formula_in_manual_column": stray,
            },
        }
        col["reads"] = sorted({
            (f"{sheet}!{body}" if sheet else body)
            for _, raw, _ in norm_by_cell
            for sheet, body in iter_refs(raw)
        })


def classify_columns(columns) -> None:
    """input / derived / manual per spec §4. Basis recorded so L2 can reason about it."""
    sheet_has_derived = any(
        c["formula_count"] >= max(1, c["typed_count"]) and c["formula_count"] > 0 for c in columns
    )
    for col in columns:
        if col["formula_count"] == 0 and col["rows_nonempty"] == 0:
            col["class"], col["class_basis"] = "empty", "no values, no formulas"
        elif col["formula_count"] >= max(1, col["typed_count"]):
            col["class"] = "derived"
            col["class_basis"] = f"{col['formula_count']} formula cells vs {col['typed_count']} typed"
        elif sheet_has_derived:
            col["class"] = "manual"
            col["class_basis"] = "typed values on a sheet with derived columns = human-maintained field"
        else:
            col["class"] = "input"
            col["class_basis"] = "typed values on a formula-free sheet = raw input/extract"


def is_key_like(col) -> bool:
    if col["class"] in ("derived", "empty"):
        return False
    if col["header"] and KEY_HEADER_RE.search(col["header"]):
        return True
    base = col["inferred_type"].startswith("str") or col["inferred_type"].startswith("mixed(str")
    return base and col["rows_nonempty"] >= 10 and col["distinct"] / col["rows_nonempty"] >= 0.95


def scan_anomalies(ws_data, columns, data_start: int, data_end: int):
    """Whitespace on key-like columns, mixed types, duplicate candidate keys."""
    anomalies = {"whitespace": [], "mixed_types": [], "duplicate_keys": []}
    for col in columns:
        col["key_like"] = is_key_like(col)
        if col["_mixed"]:
            anomalies["mixed_types"].append({
                "column": col["column"], "header": col["header"], "type": col["inferred_type"],
            })
        col.pop("_mixed", None)
        if not col["key_like"]:
            continue
        col_idx = column_index_from_string(col["column"])
        seen: dict[str, list[str]] = defaultdict(list)
        ws_cells = []
        for r in range(data_start, data_end + 1):
            v = ws_data.cell(row=r, column=col_idx).value
            if v in (None, ""):
                continue
            coord = f"{col['column']}{r}"
            if isinstance(v, str) and v != v.strip():
                ws_cells.append({"cell": coord, "value": repr(v)})
            seen[short(v, 200)].append(coord)
        if ws_cells:
            anomalies["whitespace"].append({
                "column": col["column"], "header": col["header"],
                "cells": ws_cells[:MAX_WHITESPACE_CELLS],
                "count": len(ws_cells),
            })
        dups = {v: cells for v, cells in seen.items() if len(cells) > 1}
        if dups:
            anomalies["duplicate_keys"].append({
                "column": col["column"], "header": col["header"],
                "values": [
                    {"value": v, "count": len(cells), "cells": cells[:MAX_CELLS_PER_DUP]}
                    for v, cells in sorted(dups.items())[:MAX_DUP_VALUES]
                ],
                "distinct_duplicated": len(dups),
            })
    return anomalies


def extract_validations(ws):
    out = []
    try:
        for dv in ws.data_validations.dataValidation:
            out.append({
                "range": str(dv.sqref),
                "type": dv.type,
                "operator": dv.operator,
                "formula1": dv.formula1,
                "formula2": dv.formula2,
                "allow_blank": dv.allowBlank,
            })
    except Exception as exc:  # never abort extraction on one group
        out.append({"error": f"validation read failed: {exc}"})
    return out


def extract_conditional_formatting(ws):
    out = []
    try:
        for cf in ws.conditional_formatting:
            for rule in cf.rules:
                fill_rgb = None
                try:
                    if rule.dxf is not None and rule.dxf.fill is not None:
                        color = rule.dxf.fill.bgColor or rule.dxf.fill.fgColor
                        fill_rgb = getattr(color, "rgb", None)
                        fill_rgb = fill_rgb if isinstance(fill_rgb, str) else None
                except Exception:
                    pass
                out.append({
                    "range": str(cf.sqref),
                    "type": rule.type,
                    "operator": rule.operator,
                    "formulas": list(rule.formula or []),
                    "priority": rule.priority,
                    "fill_rgb": fill_rgb,
                })
    except Exception as exc:
        out.append({"error": f"conditional formatting read failed: {exc}"})
    return out


CF_RANGE_START = re.compile(r"([A-Z]{1,3})(\d+)")
MAX_CF_RANGES = 20


def _cf_base(sqref: str) -> tuple[int, int]:
    """(linha, coluna) da celula superior-esquerda do primeiro intervalo da regra.

    E a base a que as referencias da formula sao relativas — a mesma nocao que
    `normalize_formula` usa para as formulas de coluna."""
    primeiro = (sqref or "").split()[0].split(":")[0] if (sqref or "").strip() else ""
    m = CF_RANGE_START.search(primeiro)
    if not m:
        return (1, 1)
    try:
        return (int(m.group(2)), column_index_from_string(m.group(1)))
    except Exception:
        return (1, 1)


def group_cf_rules(rules: list) -> list:
    """Regras de formatacao condicional agrupadas pelo seu padrao R1C1.

    O Excel escreve uma INSTANCIA por linha quando alguem copia linhas com formatacao
    condicional. Medido no piloto de pricing: 21 982 regras numa folha, 3,3 MB — 77% do
    ficheiro de extraccao inteiro — a dizer **duas** coisas («e hoje» e «e fim-de-semana»)
    repetidas dez mil vezes cada. A L2 da captura e mandada ler todos os JSONs contra um
    orcamento declarado de ~200 KB; a 6,3 MB o passo demora 15+ minutos, e quase tudo o
    que le e a mesma regra outra vez.

    Normalizar para R1C1 e exactamente o que `analyse_formulas` ja faz as formulas de
    coluna, pela mesma razao: um fill-down colapsa num padrao. Aqui colapsa em SETE.

    Agrupar **nao e amostrar**. Cada padrao leva quantas instancias tem, os intervalos
    onde se aplica (ate `MAX_CF_RANGES`, com a truncagem declarada), a cor, e uma formula
    em A1 — `_cf_thresholds` colhe limiares dela (`$I5>=30`) e `extract_fills` precisa do
    conjunto de `fill_rgb`. Um literal diferente (`>=30` vs `>=60`) e outro padrao, porque
    `normalize_formula` so toca em referencias.

    Um registo de erro nao e uma regra: passa intacto, e nunca e agrupado.
    """
    saida: list = []
    indice: dict = {}
    for regra in rules:
        if not isinstance(regra, dict) or regra.get("error"):
            saida.append(regra)
            continue
        base_row, base_col = _cf_base(regra.get("range"))
        try:
            padrao = tuple(normalize_formula(str(f), base_row, base_col)
                           for f in (regra.get("formulas") or []))
        except Exception:
            padrao = tuple(str(f) for f in (regra.get("formulas") or []))
        chave = (regra.get("type"), regra.get("operator"), padrao, regra.get("fill_rgb"))
        alvo = indice.get(chave)
        if alvo is None:
            alvo = {
                "range": regra.get("range"),
                "type": regra.get("type"),
                "operator": regra.get("operator"),
                "formulas": list(regra.get("formulas") or []),
                "priority": regra.get("priority"),
                "fill_rgb": regra.get("fill_rgb"),
                "pattern": " ; ".join(padrao),
                "instances": 0,
                "ranges": [],
                "ranges_truncated": False,
            }
            indice[chave] = alvo
            saida.append(alvo)
        alvo["instances"] += 1
        if len(alvo["ranges"]) < MAX_CF_RANGES:
            alvo["ranges"].append(regra.get("range"))
        else:
            alvo["ranges_truncated"] = True
    return saida


def extract_fills(ws_data, columns, data_start: int, data_end: int, cf_rules):
    """Static cell fills per column (CF output is dynamic and never stored in cell.fill,
    so every static fill is a manual paint = candidate state encoding)."""
    cf_fill_rgbs = {r.get("fill_rgb") for r in cf_rules if isinstance(r, dict) and r.get("fill_rgb")}
    col_letters = {c["column"] for c in columns}
    fills: dict[str, Counter] = defaultdict(Counter)
    truncated = data_end - data_start + 1 > MAX_SCAN_ROWS
    end = min(data_end, data_start + MAX_SCAN_ROWS - 1)
    for row in ws_data.iter_rows(min_row=data_start, max_row=end):
        for cell in row:
            letter = get_column_letter(cell.column)   # MergedCell has no column_letter
            if letter not in col_letters:
                continue
            fill = cell.fill
            if fill is None or fill.patternType is None:
                continue
            rgb = getattr(fill.fgColor, "rgb", None)
            key = rgb if isinstance(rgb, str) else f"theme:{getattr(fill.fgColor, 'theme', '?')}"
            fills[letter][key] += 1
    out = []
    rows_by_letter = {c["column"]: max(1, c["rows_nonempty"]) for c in columns}
    for letter in sorted(fills):
        for rgb, count in fills[letter].most_common():
            out.append({
                "column": letter,
                "rgb": rgb,
                "count": count,
                "uniform": count >= 0.9 * rows_by_letter.get(letter, count),
                "matches_cf_output": rgb in cf_fill_rgbs,
            })
    return out, truncated


def extract_comments(ws, max_row: int | None = None):
    out = []
    for row in ws.iter_rows(max_row=min(max_row or ws.max_row or 1, ws.max_row or 1)):
        for cell in row:
            if cell.comment is not None:
                out.append({
                    "cell": cell.coordinate,
                    "author": cell.comment.author,
                    "text": short(cell.comment.text or "", 500),
                })
                if len(out) >= MAX_COMMENTS:
                    return out
    return out


def extract_named_ranges(wb):
    out = []
    try:
        for name, defn in wb.defined_names.items():
            out.append({"name": name, "target": defn.attr_text, "scope": "workbook"})
    except Exception as exc:
        out.append({"error": f"defined names read failed: {exc}"})
    for ws in wb.worksheets:
        try:
            for name, defn in getattr(ws, "defined_names", {}).items():
                out.append({"name": name, "target": defn.attr_text, "scope": ws.title})
        except Exception:
            continue
    return out


def extract_tables(wb):
    """As tabelas (ListObjects) do livro: nome, folha e intervalo.

    Uma referencia estruturada — `Galp_Marinha_v2[quotation_dt]` — nomeia uma tabela, e
    sem esta lista nao ha como dizer ONDE ela vive. No piloto de pricing e a diferenca
    entre «2 698 chamadas recusadas» e «ler `UlyssesQuotes!A1:J525`»."""
    out = []
    for ws in wb.worksheets:
        try:
            tabelas = getattr(ws, "tables", None) or {}
            for nome in tabelas:
                alvo = tabelas[nome]
                ref = alvo if isinstance(alvo, str) else getattr(alvo, "ref", None)
                out.append({"name": str(nome), "sheet": ws.title, "ref": ref})
        except Exception:
            continue
    return out


INDIRECT_LITERAL_RE = re.compile(r'(?i)\bINDIRECT\s*\(\s*"([^"]*)"')
STRUCTURED_REF_RE = re.compile(r"([A-Za-z_\u00C0-\u024F][\w.\u00C0-\u024F]{0,60})\s*\[")
BARE_NAME_RE = re.compile(r"(?<![\w.!$])([A-Za-z_\u00C0-\u024F][\w.\u00C0-\u024F]{2,60})(?![\w(\[])")
MAX_READ_TARGETS = 8


def _external_target(target: str) -> bool:
    """`[1]folha!A1` = outro ficheiro. Ler ESTE Excel nao resolve isso."""
    return bool(re.match(r"\s*\[\d+\]", str(target or "")))


def read_targets(formula: str, workbook: dict, sheetnames=()) -> list[dict]:
    """O que ha a LER para resolver esta chamada — o alvo, nao a formula.

    Uma chamada recusada ja dizia ONDE esta (a celula). Nao dizia o que abrir. Medido no
    piloto de pricing: 10 262 recusas que sao TRES alvos — uma folha, uma tabela de 525
    linhas, e uma familia de 82 intervalos nomeados de que basta ler UM.

    Deriva-se do texto, dos nomes e das tabelas do proprio livro. Nada se computa e nada
    se infere: um prefixo que nao casa com nome nenhum nao produz alvo, e um alvo noutro
    ficheiro sai marcado `external` — o relatorio nunca pode sugerir que se resolve a ler
    este Excel (e o caso do canal Apttus/X-Author).
    """
    texto = str(formula or "")
    nomes = [n for n in ((workbook or {}).get("named_ranges") or [])
             if isinstance(n, dict) and n.get("name")]
    por_nome = {}
    for n in nomes:
        por_nome.setdefault(str(n["name"]), str(n.get("target") or ""))
    tabelas = {str(t["name"]): t for t in ((workbook or {}).get("tables") or [])
               if isinstance(t, dict) and t.get("name")}

    saida: list[dict] = []
    vistos: set = set()

    def add(alvo: dict) -> None:
        chave = (alvo["kind"], alvo["name"])
        if chave in vistos or len(saida) >= MAX_READ_TARGETS:
            return
        vistos.add(chave)
        saida.append(alvo)

    # 1. o literal de um INDIRECT: nome exacto, ou o prefixo de uma familia de nomes
    for literal in INDIRECT_LITERAL_RE.findall(texto):
        if not literal:
            continue
        raiz = literal.split("[")[0]
        if raiz in tabelas:
            t = tabelas[raiz]
            add({"kind": "table", "name": raiz,
                 "where": "{}!{}".format(t.get("sheet") or "?", t.get("ref") or "?")})
            continue
        if raiz in por_nome:
            add({"kind": "named", "name": raiz, "where": por_nome[raiz],
                 "external": _external_target(por_nome[raiz])})
            continue
        familia = sorted(k for k in por_nome if k.startswith(raiz))
        if familia:
            add({"kind": "named-family", "name": raiz + "*", "count": len(familia),
                 "where": por_nome[familia[0]], "example": familia[0],
                 "external": _external_target(por_nome[familia[0]])})

    # 2. referencias estruturadas: `Tabela[coluna]`
    for nome in STRUCTURED_REF_RE.findall(texto):
        if nome in tabelas:
            t = tabelas[nome]
            add({"kind": "table", "name": nome,
                 "where": "{}!{}".format(t.get("sheet") or "?", t.get("ref") or "?")})

    # 3. folhas citadas explicitamente
    sem_strings = STRING_SEG_RE.sub('""', texto)
    for m in REF_RE.finditer(sem_strings):
        folha = _unquote_sheet(m.group("sheet"))
        if folha and folha in set(sheetnames or ()):
            add({"kind": "sheet", "name": folha, "where": folha})

    # 4. nomes usados directamente
    for nome in BARE_NAME_RE.findall(sem_strings):
        if nome in por_nome:
            add({"kind": "named", "name": nome, "where": por_nome[nome],
                 "external": _external_target(por_nome[nome])})
    return saida


def extract_flags(path: str, wb, wb_data):
    flags = {"vba_present": False, "vba_modules": [], "external_links": [],
             "pivot_tables": [], "protected_sheets": []}
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            flags["vba_present"] = any(n.lower().endswith("vbaproject.bin") for n in names)
            for rel in (n for n in names if n.startswith("xl/externalLinks/_rels/")):
                for target in re.findall(rb'Target="([^"]+)"', zf.read(rel)):
                    flags["external_links"].append(target.decode("utf-8", "replace"))
    except Exception:
        pass
    for ws in wb_data.worksheets:
        try:
            if ws.protection and ws.protection.sheet:
                flags["protected_sheets"].append(ws.title)
        except Exception:
            continue
        try:
            for pivot in getattr(ws, "_pivots", []):
                src = pivot.cache.cacheSource.worksheetSource
                flags["pivot_tables"].append({
                    "sheet": ws.title,
                    "source": f"{getattr(src, 'sheet', '?')}!{getattr(src, 'ref', '?')}",
                })
        except Exception:
            continue
    return flags


def _fail_extraction(doc: dict, out_path: str, filename: str, exc: BaseException,
                     log_path: str | None) -> int:
    """Write the failure artefact and return 0 — the degradation has to CLOSE.

    Measured on a 37 MB workbook: the first MemoryError was caught, the artefact was written, and a
    second MemoryError raised while handling the first killed the process with rc=1 anyway. So this
    drops the big references first, collects, and keeps every step allocation-free: no f-string over
    `exc`, no traceback formatting, and the whole tail guarded.
    """
    for key in ("sheets", "workbook"):
        doc.pop(key, None)
    gc.collect()
    name = type(exc).__name__
    doc["status"] = "failed"
    doc["reason"] = name + ": " + (str(exc)[:200] if not isinstance(exc, MemoryError) else "")
    doc["capability_boundary"] = {"extraction_failed": {
        "present": True, "detail": name, "locator": filename}}
    try:
        _write_json(out_path, doc)
    except BaseException:
        pass
    try:
        print("extraction FAILED for " + filename + " (" + name + ") -> failure artefact written",
              file=sys.stderr)
        append_log(log_path, "L1", filename, "failed", name)
    except BaseException:
        pass
    return 0


def extract(path: str, out_path: str, force: bool, log_path: str | None) -> int:
    filename = os.path.basename(path)
    if not os.path.exists(path):
        print(f"input not found: {path}", file=sys.stderr)
        return 2

    sha = sha256_file(path)
    if not force and os.path.exists(out_path):
        try:
            with open(out_path, encoding="utf-8") as fh:
                previous = json.load(fh)
            if previous.get("identity", {}).get("sha256") == sha and previous.get("status") == "ok":
                print(f"cache-hit: {filename} unchanged (sha256 {sha[:8]}), extraction kept")
                append_log(log_path, "L1", filename, "cache-hit", f"sha256 {sha[:8]}")
                return 0
        except Exception:
            pass  # unreadable previous artefact -> re-extract

    stat = os.stat(path)
    identity = {
        "filename": filename,
        "source_path": path,
        "size_bytes": stat.st_size,
        "sha256": sha,
        "modified": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
    }
    doc = {
        "artefact": ARTEFACT_ID,
        "tool": {"name": "xlsx_extract.py", "version": TOOL_VERSION,
                 "openpyxl": openpyxl.__version__,
                 "python": ".".join(map(str, sys.version_info[:3]))},
        "extracted_at": now_iso(),
        "identity": identity,
    }

    try:
        wb_formula = load_workbook(path, data_only=False)
        wb_data = load_workbook(path, data_only=True)
    except BaseException as exc:            # MemoryError included: the artefact is the deliverable
        return _fail_extraction(doc, out_path, filename, exc, log_path)

    doc["status"] = "ok"
    doc["workbook"] = {
        "named_ranges": extract_named_ranges(wb_formula),
        "tables": extract_tables(wb_formula),
        "flags": extract_flags(path, wb_formula, wb_data),
    }

    sheets = []
    content_end = content_rows(path)          # where each sheet's content really ends (streaming XML)
    if content_end:
        doc["workbook"]["content_rows"] = content_end
    known_sheets = set(wb_data.sheetnames)
    for ws_data, ws_formula in zip(wb_data.worksheets, wb_formula.worksheets):
        errors = []
        header_row, data_start, basis = detect_header(ws_data)
        data_end, data_end_declared, data_end_content, scan_truncated = scan_bounds(
            ws_data, data_start, content_end.get(ws_data.title))
        sheet = {
            "name": ws_data.title,
            "state": ws_data.sheet_state,
            "dimensions": ws_data.dimensions,
            "max_row": ws_data.max_row,
            "max_col": ws_data.max_column,
            "frozen_panes": str(ws_data.freeze_panes) if ws_data.freeze_panes else None,
            "header_row": header_row,
            "data_start_row": data_start,
            "data_end_row": data_end,
            "data_end_declared": data_end_declared,
            "data_end_content": data_end_content,
            "header_basis": basis,
        }
        try:
            columns = scan_columns(ws_data, ws_formula, header_row, data_start, data_end, scan_truncated)
            analyse_formulas(columns, data_start)
            classify_columns(columns)
            sheet["anomalies"] = scan_anomalies(ws_data, columns, data_start, data_end)
        except Exception as exc:
            columns = []
            sheet["anomalies"] = {}
            errors.append(f"column scan failed: {type(exc).__name__}: {exc}")
        sheet["validations"] = extract_validations(ws_formula)
        sheet["conditional_formatting"] = group_cf_rules(
            extract_conditional_formatting(ws_formula))
        try:
            sheet["fills"], truncated = extract_fills(
                ws_data, columns, data_start, data_end, sheet["conditional_formatting"])
            if truncated:
                sheet["fills_truncated_at_rows"] = MAX_SCAN_ROWS
        except Exception as exc:
            sheet["fills"] = []
            errors.append(f"fill scan failed: {type(exc).__name__}: {exc}")
        if scan_truncated:
            sheet["scan_truncated"] = True
            sheet["scan_truncated_reason"] = (
                f"content runs to row {data_end_content} (grid declares {data_end_declared}); "
                f"cell-level scans stop at MAX_SCAN_ROWS={MAX_SCAN_ROWS} (rows {data_start}-{data_end})")
        sheet["comments"] = extract_comments(ws_formula, data_end)
        sheet["columns"] = columns
        unknown = sorted({
            ref.split("!")[0]
            for col in columns for ref in col.get("reads", [])
            if "!" in ref and ref.split("!")[0] not in known_sheets
        })
        if unknown:
            sheet["unknown_sheet_refs"] = unknown
        if errors:
            sheet["errors"] = errors
        sheets.append(sheet)
    doc["sheets"] = sheets
    doc["capability_boundary"] = capability_boundary(path, wb_formula, doc)   # P3b-1, additive key

    _write_json(out_path, doc)
    n_cols = sum(len(s["columns"]) for s in sheets)
    print(f"extracted: {filename} -> {out_path} ({len(sheets)} sheets, {n_cols} columns, sha256 {sha[:8]})")
    append_log(log_path, "L1", filename, "extracted", f"{len(sheets)} sheets, {n_cols} columns, sha256 {sha[:8]}")
    return 0


def _write_json(out_path: str, doc: dict) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1, default=json_default)
    os.replace(tmp, out_path)


# --------------------------------------------------------------- L3 replay

class Finding:
    __slots__ = ("check", "location", "expected", "found", "severity")
    ORDER = {"high": 0, "medium": 1, "low": 2, "info": 3}

    def __init__(self, check, location, expected, found, severity):
        self.check, self.location = check, location
        self.expected, self.found, self.severity = expected, found, severity


def find_calls(text: str, fname: str) -> list[str]:
    """Balanced-paren extraction of every `FNAME(...)` call, string-literal aware."""
    out = []
    upper = text.upper()
    i = 0
    while True:
        j = upper.find(fname + "(", i)
        if j == -1:
            return out
        if j > 0 and (text[j - 1].isalnum() or text[j - 1] in "_.$"):
            i = j + 1
            continue
        depth, in_str = 0, False
        for k in range(j + len(fname), len(text)):
            ch = text[k]
            if in_str:
                if ch == '"':
                    in_str = False
            elif ch == '"':
                in_str = True
            elif ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    out.append(text[j:k + 1])
                    break
        i = j + 1


def split_args(call: str) -> list[str]:
    inner = call[call.index("(") + 1:-1]
    args, depth, in_str, start = [], 0, False, 0
    for k, ch in enumerate(inner):
        if in_str:
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        elif ch == "," and depth == 0:
            args.append(inner[start:k].strip())
            start = k + 1
    args.append(inner[start:].strip())
    return args


SINGLE_CELL_RE = re.compile(rf"^(?:(?P<sheet>{_SHEETNAME})!)?\$?(?P<col>[A-Z]{{1,3}})\$?(?P<row>\d+)$")
RANGE_ARG_RE = re.compile(
    rf"^(?:(?P<sheet>{_SHEETNAME})!)?"
    r"(?:\$?(?P<c1>[A-Z]{1,3})\$?(?P<r1>\d+)?:\$?(?P<c2>[A-Z]{1,3})\$?(?P<r2>\d+)?)$"
)


def _unquote_sheet(sheet: str | None) -> str | None:
    if sheet and sheet.startswith("'"):
        return sheet[1:-1].replace("''", "'")
    return sheet


# Excel treats `*` and `?` in a text criterion as wildcards, and `~` as the escape that
# makes the next one literal (COUNTIF, VLOOKUP/XLOOKUP with exact match, MATCH). The
# replay compares literally, so `"key*"` against `key`/`key2` reported "no match" where
# Excel counts two (F03, adversarial review 2026-09-08). Declaring the limit is the fix:
# a battery that invents anomalies is worse than one that says what it cannot check.
# Implementing the semantics waits for a real case -- none of the three pilots has one.
def has_wildcards(value) -> bool:
    """True when a criterion carries Excel wildcard syntax (`*`, `?`, or the `~` escape)."""
    return isinstance(value, str) and any(ch in value for ch in ("*", "?", "~"))


class Replayer:
    """Fixed check battery over one workbook + its extraction JSON. No general evaluation."""

    # a column only has a policeable fill-down convention above these:
    CONVENTION_MIN_FORMULAS = 8
    CONVENTION_MIN_COVERAGE = 0.6

    def __init__(self, wb_data, extraction: dict):
        self.wb = wb_data
        self.x = extraction
        self.range_cache: dict[tuple, list[tuple[int, object]]] = {}
        self.findings: list[Finding] = []
        self.not_replayable: Counter = Counter()
        self.nr_example: dict[str, str] = {}
        self.nr_cells: dict[str, set] = defaultdict(set)   # pattern -> {(sheet, coord)} (P9: TO-READ ranges)
        # pattern -> {(kind, name): alvo} -- o que ha a LER, nao onde a recusa esta
        self.nr_targets: dict[str, dict] = defaultdict(dict)
        self.lookup_targets: set[tuple[str, str]] = set()   # (sheet, col letter) used as match column
        self.criterion_cols: set[tuple[str, str]] = set()   # (sheet, col letter) feeding lookup values
        self.checked_cells = 0
        self.skipped_empty = 0
        # simple named ranges ('Sheet'!$A$1:$B$9 style) resolved for lookup replay;
        # ambiguous names (same name, several targets) are dropped, never guessed
        self.names: dict[str, str] = {}
        seen: dict[str, set] = defaultdict(set)
        for nr in (extraction.get("workbook", {}) or {}).get("named_ranges", []):
            if not isinstance(nr, dict) or not nr.get("name") or not nr.get("target"):
                continue
            seen[str(nr["name"]).casefold()].add(str(nr["target"]))
        for name, targets in seen.items():
            if len(targets) == 1:
                target = next(iter(targets))
                if "#REF!" not in target and (RANGE_ARG_RE.fullmatch(target) or SINGLE_CELL_RE.fullmatch(target)):
                    self.names[name] = target

    def _deref_name(self, arg: str) -> str:
        return self.names.get(arg.strip().casefold(), arg)

    # -- resolution helpers ------------------------------------------------
    def sheet_meta(self, name: str) -> dict | None:
        for s in self.x["sheets"]:
            if s["name"] == name:
                return s
        return None

    def resolve_cell(self, default_sheet: str, arg: str):
        m = SINGLE_CELL_RE.fullmatch(self._deref_name(arg))
        if not m:
            return None, None
        sheet = _unquote_sheet(m.group("sheet")) or default_sheet
        if sheet not in self.wb.sheetnames:
            return None, None
        coord = (sheet, m.group("col"), int(m.group("row")))
        ws = self.wb[sheet]
        return coord, ws.cell(row=coord[2], column=column_index_from_string(coord[1])).value

    def materialize(self, default_sheet: str, arg: str):
        """Range arg -> (sheet, first_col_idx, width, [(row, first_col_value)...]) or None."""
        arg = self._deref_name(arg)
        m = RANGE_ARG_RE.fullmatch(arg)
        if not m:
            sc = SINGLE_CELL_RE.fullmatch(arg)
            if sc:  # single-cell "range"
                sheet = _unquote_sheet(sc.group("sheet")) or default_sheet
                if sheet not in self.wb.sheetnames:
                    return None
                c = column_index_from_string(sc.group("col"))
                r = int(sc.group("row"))
                return sheet, c, 1, [(r, self.wb[sheet].cell(row=r, column=c).value)]
            return None
        sheet = _unquote_sheet(m.group("sheet")) or default_sheet
        if sheet not in self.wb.sheetnames:
            return None
        ws = self.wb[sheet]
        c1 = column_index_from_string(m.group("c1"))
        c2 = column_index_from_string(m.group("c2"))
        if c2 < c1:
            c1, c2 = c2, c1
        r1 = int(m.group("r1")) if m.group("r1") else 1
        r2 = int(m.group("r2")) if m.group("r2") else (ws.max_row or 1)
        r2 = min(r2, ws.max_row or 1)
        key = (sheet, c1, r1, r2)
        if key not in self.range_cache:
            self.range_cache[key] = [
                (r, ws.cell(row=r, column=c1).value) for r in range(r1, r2 + 1)
            ]
        return sheet, c1, c2 - c1 + 1, self.range_cache[key]

    @staticmethod
    def _eq(a, b, trim: bool) -> bool:
        if isinstance(a, str) and isinstance(b, str):
            if trim:
                a, b = a.strip(), b.strip()
            return a.casefold() == b.casefold()   # Excel text matching is case-insensitive
        if isinstance(a, bool) or isinstance(b, bool):
            return a is b
        if isinstance(a, (int, float)) and isinstance(b, (int, float)):
            return abs(a - b) < 1e-9
        return a == b

    def match_row(self, rows, needle, trim: bool):
        for r, v in rows:
            if v in (None, ""):
                continue
            if self._eq(v, needle, trim):
                return r
        return None

    @staticmethod
    def values_equal(a, b) -> bool:
        empties = (None, "")
        if a in empties and b in empties:
            return True
        # Excel: a reference to an empty cell evaluates to 0 — indistinguishable on replay
        for x, y in ((a, b), (b, a)):
            if x in empties and isinstance(y, (int, float)) and not isinstance(y, bool) and y == 0:
                return True
        if isinstance(a, (int, float)) and isinstance(b, (int, float)) \
                and not isinstance(a, bool) and not isinstance(b, bool):
            return abs(a - b) < 1e-6
        if isinstance(a, (dt.datetime, dt.date)) and isinstance(b, (dt.datetime, dt.date)):
            return str(a) == str(b)
        return a == b

    @staticmethod
    def _covers_whole_formula(formula: str, call: str) -> bool:
        """True when the lookup call IS the formula (allowing IFERROR/IFNA wrappers and
        leading +). Multi-call formulas (=INDEX(a)+INDEX(b)) cannot be compared against
        the stored total — stored-vs-recomputed is claimed only for whole-formula calls."""
        f = formula.strip().lstrip("=").lstrip("+").strip()
        for _ in range(3):
            if f.upper().startswith(("IFERROR(", "IFNA(")) and f.endswith(")"):
                args = split_args("X(" + f[f.index("(") + 1:])
                if args:
                    f = args[0].strip().lstrip("+").strip()
                    continue
            break
        return f == call.strip()

    # -- battery checks ----------------------------------------------------
    def run(self) -> None:
        self.check_lookups()
        self.check_duplicates()
        self.check_whitespace_casing()
        self.check_staleness()
        self.check_pattern_exceptions()
        self.check_clone_divergence()
        self.check_orphans()

    def _mark_not_replayable(self, sheet_name, coord, raw, reason) -> bool:
        generic = re.sub(r"\$?[A-Z]{1,3}\$?\d+", "<ref>", short(raw, 100))  # collapse per-cell variants
        pattern = f"{reason}: {generic}"
        self.not_replayable[pattern] += 1
        self.nr_example.setdefault(pattern, f"{sheet_name}!{coord}")
        self.nr_cells[pattern].add((sheet_name, coord))
        try:
            for alvo in read_targets(raw, self.x.get("workbook") or {}, self.wb.sheetnames):
                self.nr_targets[pattern].setdefault((alvo["kind"], alvo["name"]), alvo)
        except Exception:
            pass          # o alvo e um extra de leitura; nunca pode derrubar o replay
        return True

    def to_read_targets(self) -> list[dict]:
        """Os alvos distintos de TODAS as chamadas recusadas, do maior para o menor.

        E a resposta a «por onde comeco»: no piloto de pricing, 10 262 recusas dao TRES
        alvos. A contagem de cada um e quantas chamadas o citam — e por isso a ordem
        util, nao a alfabetica."""
        juntos: dict = {}
        for pattern, alvos in self.nr_targets.items():
            chamadas = self.not_replayable.get(pattern, 0)
            for chave, alvo in alvos.items():
                acc = juntos.setdefault(chave, dict(alvo, calls=0))
                acc["calls"] += chamadas
        return sorted(juntos.values(), key=lambda a: (-a["calls"], a["kind"], a["name"]))

    def to_read_ranges(self) -> dict[str, list[str]]:
        """P9: per not-replayable pattern, the compact ranges to READ — `Sheet!F9:F1469` — one per
        (sheet, column). 2045 declined calls in the real workbook collapse to a short, finite list."""
        out: dict[str, list[str]] = {}
        for pattern, cells in self.nr_cells.items():
            by_col: dict[tuple[str, str], list[int]] = defaultdict(list)
            for sheet, coord in cells:
                m = re.match(r"^([A-Z]{1,3})(\d+)$", coord)
                if m:
                    by_col[(sheet, m.group(1))].append(int(m.group(2)))
            ranges = []
            for (sheet, col), rows in sorted(by_col.items()):
                lo, hi = min(rows), max(rows)
                ranges.append(f"{sheet}!{col}{lo}" if lo == hi else f"{sheet}!{col}{lo}:{col}{hi}")
            out[pattern] = ranges
        return out

    def to_read_rectangles(self) -> list[str]:
        """All not-replayable cells, merged across patterns: per sheet, adjacent columns with the same
        row span collapse into one rectangle (`Outputs!AJ14:AK31`). The number that goes to the log."""
        # a clone sheet repeats the representative's ranges: reading them twice reads nothing new
        clone_of = {c for cs in clone_groups(self.x).values() for c in cs}
        by_col: dict[tuple[str, str], set[int]] = defaultdict(set)
        for cells in self.nr_cells.values():
            for sheet, coord in cells:
                if sheet in clone_of:
                    continue
                m = re.match(r"^([A-Z]{1,3})(\d+)$", coord)
                if m:
                    by_col[(sheet, m.group(1))].add(int(m.group(2)))
        cols = sorted(by_col.items(), key=lambda kv: (kv[0][0], column_index_from_string(kv[0][1])))
        rects: list[str] = []
        i = 0
        while i < len(cols):
            (sheet, c1), rows = cols[i]
            lo, hi = min(rows), max(rows)
            j = i
            while (j + 1 < len(cols) and cols[j + 1][0][0] == sheet
                   and column_index_from_string(cols[j + 1][0][1]) == column_index_from_string(cols[j][0][1]) + 1
                   and (min(cols[j + 1][1]), max(cols[j + 1][1])) == (lo, hi)):
                j += 1
            c2 = cols[j][0][1]
            if c1 == c2:
                rects.append(f"{sheet}!{c1}{lo}" if lo == hi else f"{sheet}!{c1}{lo}:{c1}{hi}")
            else:
                rects.append(f"{sheet}!{c1}{lo}:{c2}{hi}")
            i = j + 1
        return rects

    def to_read_count(self) -> int:
        return len(self.to_read_rectangles())

    def check_lookups(self) -> None:
        misses_by_col: dict[str, list] = defaultdict(list)
        stale_by_col: dict[str, list] = defaultdict(list)
        for sheet in self.x["sheets"]:
            name = sheet["name"]
            if name not in self.wb.sheetnames:
                continue
            ws = self.wb[name]
            for col in sheet["columns"]:
                if not col.get("formula"):
                    continue
                pattern = col["formula"]["dominant_pattern"]
                has_lookup = any(t in pattern.upper() for t in ("VLOOKUP(", "XLOOKUP(", "COUNTIF(", "INDEX("))
                if not has_lookup:
                    continue
                for r in range(sheet["data_start_row"], sheet["data_end_row"] + 1):
                    coord = f"{col['column']}{r}"
                    fcell = self._formula_at(name, coord)
                    if fcell is None:
                        continue
                    if NOT_REPLAYABLE_RE.search(fcell):
                        self._mark_not_replayable(name, coord, fcell, "dynamic/external reference")
                        continue
                    stored = ws[coord].value
                    volatile = bool(VOLATILE_RE.search(fcell))
                    self._replay_cell(name, coord, fcell, stored, volatile, misses_by_col, stale_by_col)
        for key, misses in sorted(misses_by_col.items()):
            examples = ", ".join(f"{short(v, 30)} @{c}" for c, v in misses[:MAX_MISS_EXAMPLES])
            self.findings.append(Finding(
                "lookup integrity", key,
                "every lookup value resolvable in its target range",
                f"{len(misses)} lookup value(s) with no match in target (e.g. {examples})",
                "medium"))
        for key, stales in sorted(stale_by_col.items()):
            examples = "; ".join(f"{c}: stored {short(s, 24)} vs recomputed {short(rc, 24)}"
                                 for c, s, rc in stales[:MAX_MISS_EXAMPLES])
            self.findings.append(Finding(
                "lookup integrity", key,
                "stored result equals recomputed lookup result",
                f"{len(stales)} cell(s) diverge ({examples})",
                "medium"))

    def _formula_at(self, sheet_name: str, coord: str) -> str | None:
        cache = getattr(self, "_fwb", None)
        if cache is None:
            return None
        try:
            return formula_text(cache[sheet_name][coord])
        except Exception:
            return None

    def _replay_cell(self, sheet_name, coord, formula, stored, volatile, misses_by_col, stale_by_col):
        col_letter = re.sub(r"[0-9]+$", "", coord)
        col_key = f"{sheet_name}!{col_letter} (VLOOKUP)"
        handled = False
        for call in find_calls(formula, "VLOOKUP"):
            args = split_args(call)
            if len(args) < 4 or args[3].upper().rstrip(")") not in ("0", "FALSE"):
                self._mark_not_replayable(sheet_name, coord, call, "approximate-match VLOOKUP")
                continue
            needle = self._resolve_scalar(sheet_name, args[0], coord)
            if needle is _UNSUPPORTED:
                self._mark_not_replayable(sheet_name, coord, call, "unsupported lookup value")
                continue
            table = self.materialize(sheet_name, args[1])
            if table is None:
                self._mark_not_replayable(sheet_name, coord, call, "unsupported table range")
                continue
            t_sheet, t_first, width, rows = table
            try:
                idx = int(args[2])
            except ValueError:
                self._mark_not_replayable(sheet_name, coord, call, "non-literal column index")
                continue
            self.lookup_targets.add((t_sheet, get_column_letter(t_first)))
            self._note_criterion(sheet_name, args[0])
            if idx > width:
                self.findings.append(Finding(
                    "orphan references", f"{sheet_name}!{coord}",
                    f"VLOOKUP column index within range width {width}",
                    f"index {idx} exceeds {args[1]}", "high"))
                continue
            if has_wildcards(needle):
                self._mark_not_replayable(sheet_name, coord, call, "wildcard VLOOKUP lookup value")
                continue
            handled = True
            if needle in (None, ""):
                self.skipped_empty += 1
                continue
            self.checked_cells += 1
            raw_row = self.match_row(rows, needle, trim=False)
            if raw_row is None:
                norm_row = self.match_row(rows, needle, trim=True) if isinstance(needle, str) else None
                if norm_row is not None:
                    tcell = f"{t_sheet}!{get_column_letter(t_first)}{norm_row}"
                    tval = self.wb[t_sheet].cell(row=norm_row, column=t_first).value
                    self.findings.append(Finding(
                        "whitespace/casing", f"{sheet_name}!{coord}",
                        f"lookup of {short(needle, 40)!r} matches {tcell}",
                        f"raw match fails; succeeds only after TRIM ({tcell} holds {short(tval, 40)!r}) "
                        "— silent lookup failure", "high"))
                else:
                    misses_by_col[col_key].append((coord, needle))
            elif not volatile and self._covers_whole_formula(formula, call):
                target_val = self.wb[t_sheet].cell(row=raw_row, column=t_first + idx - 1).value
                if not self.values_equal(stored, target_val):
                    stale_by_col[col_key].append((coord, stored, target_val))
        for call in find_calls(formula, "COUNTIF"):
            args = split_args(call)
            if len(args) != 2:
                self._mark_not_replayable(sheet_name, coord, call, "unsupported COUNTIF arity")
                continue
            needle = self._resolve_scalar(sheet_name, args[1], coord)
            if needle is _UNSUPPORTED or (isinstance(needle, str) and needle.startswith(("<", ">", "="))):
                self._mark_not_replayable(sheet_name, coord, call, "unsupported COUNTIF criterion")
                continue
            if has_wildcards(needle):
                self._mark_not_replayable(sheet_name, coord, call, "wildcard COUNTIF criterion")
                continue
            rng = self.materialize(sheet_name, args[0])
            if rng is None:
                self._mark_not_replayable(sheet_name, coord, call, "unsupported COUNTIF range")
                continue
            t_sheet, t_first, _, rows = rng
            self.lookup_targets.add((t_sheet, get_column_letter(t_first)))
            self._note_criterion(sheet_name, args[1])
            handled = True
            if needle in (None, ""):
                self.skipped_empty += 1
                continue
            self.checked_cells += 1
            raw_n = sum(1 for _, v in rows if v not in (None, "") and self._eq(v, needle, trim=False))
            if raw_n == 0 and isinstance(needle, str):
                norm_n = sum(1 for _, v in rows if v not in (None, "") and self._eq(v, needle, trim=True))
                if norm_n > 0:
                    self.findings.append(Finding(
                        "whitespace/casing", f"{sheet_name}!{coord}",
                        f"membership of {short(needle, 40)!r} in {args[0]}",
                        "raw COUNTIF = 0 but > 0 after TRIM — whitespace breaks the match", "high"))
                else:
                    misses_by_col[f"{sheet_name}!{col_letter} (COUNTIF membership)"].append((coord, needle))
        for fname in ("XLOOKUP", "INDEX"):
            for call in find_calls(formula, fname):
                if fname == "INDEX" and "MATCH(" not in call.upper():
                    continue
                whole = self._covers_whole_formula(formula, call)
                handled_x = self._replay_xlookup(sheet_name, coord, call, stored, volatile, whole, stale_by_col, misses_by_col) \
                    if fname == "XLOOKUP" else \
                    self._replay_index_match(sheet_name, coord, call, stored, volatile, whole, stale_by_col, misses_by_col)
                handled = handled or handled_x
        if not handled and not find_calls(formula, "VLOOKUP") and not find_calls(formula, "COUNTIF"):
            pass  # column matched lookup keywords only via dominant pattern; nothing claimable per-cell

    def _note_criterion(self, default_sheet: str, arg: str) -> None:
        m = SINGLE_CELL_RE.fullmatch(arg)
        if m:
            sheet = _unquote_sheet(m.group("sheet")) or default_sheet
            self.criterion_cols.add((sheet, m.group("col")))

    def _resolve_scalar(self, default_sheet: str, arg: str, coord: str):
        arg = arg.strip()
        if arg.startswith('"') and arg.endswith('"'):
            return arg[1:-1].replace('""', '"')
        try:
            return float(arg) if "." in arg else int(arg)
        except ValueError:
            pass
        ref, val = self.resolve_cell(default_sheet, arg)
        if ref is not None:
            return val
        return _UNSUPPORTED

    def _replay_xlookup(self, sheet_name, coord, call, stored, volatile, whole, stale_by_col, misses_by_col) -> bool:
        args = split_args(call)
        if len(args) < 3:
            return self._mark_not_replayable(sheet_name, coord, call, "unsupported XLOOKUP arity") and False
        if len(args) >= 5 and args[4] not in ("0", ""):
            return self._mark_not_replayable(sheet_name, coord, call, "non-exact XLOOKUP mode") and False
        # search_mode: 1 = first-to-last (what match_row does), -1 = last-to-first,
        # 2/-2 = binary search over sorted data. With duplicate keys, -1 returns the
        # OTHER row, and the replay then called a correct cached value stale (F03).
        if len(args) >= 6 and args[5].strip() not in ("1", ""):
            return self._mark_not_replayable(
                sheet_name, coord, call, "unsupported XLOOKUP search_mode") and False
        needle = self._resolve_scalar(sheet_name, args[0], coord)
        if has_wildcards(needle):
            return self._mark_not_replayable(
                sheet_name, coord, call, "wildcard XLOOKUP lookup value") and False
        lookup_rng = self.materialize(sheet_name, args[1])
        return_rng = self.materialize(sheet_name, args[2])
        if needle is _UNSUPPORTED or lookup_rng is None or return_rng is None:
            return self._mark_not_replayable(sheet_name, coord, call, "unsupported XLOOKUP args") and False
        l_sheet, l_first, _, rows = lookup_rng
        r_sheet, r_first, _, _ = return_rng
        self.lookup_targets.add((l_sheet, get_column_letter(l_first)))
        self._note_criterion(sheet_name, args[0])
        if needle in (None, ""):
            self.skipped_empty += 1
            return True
        self.checked_cells += 1
        raw_row = self.match_row(rows, needle, trim=False)
        col_key = f"{sheet_name}!{re.sub(r'[0-9]+$', '', coord)} (XLOOKUP)"
        if raw_row is None:
            norm_row = self.match_row(rows, needle, trim=True) if isinstance(needle, str) else None
            if norm_row is not None:
                self.findings.append(Finding(
                    "whitespace/casing", f"{sheet_name}!{coord}",
                    f"XLOOKUP of {short(needle, 40)!r} matches row {norm_row}",
                    "raw match fails; succeeds only after TRIM — silent lookup failure", "high"))
            else:
                misses_by_col[col_key].append((coord, needle))
        elif not volatile and whole:
            got = self.wb[r_sheet].cell(row=raw_row, column=r_first).value
            if not self.values_equal(stored, got):
                stale_by_col[col_key].append((coord, stored, got))
        return True

    def _replay_index_match(self, sheet_name, coord, call, stored, volatile, whole, stale_by_col, misses_by_col) -> bool:
        args = split_args(call)
        if len(args) < 2:
            return False
        matches = find_calls(args[1], "MATCH")
        if not matches:
            return self._mark_not_replayable(sheet_name, coord, call, "INDEX without literal MATCH") and False
        margs = split_args(matches[0])
        if len(margs) < 3 or margs[2] not in ("0",):
            return self._mark_not_replayable(sheet_name, coord, call, "non-exact MATCH") and False
        needle = self._resolve_scalar(sheet_name, margs[0], coord)
        match_rng = self.materialize(sheet_name, margs[1])
        index_rng = self.materialize(sheet_name, args[0])
        if needle is _UNSUPPORTED or match_rng is None or index_rng is None:
            return self._mark_not_replayable(sheet_name, coord, call, "unsupported INDEX/MATCH args") and False
        if has_wildcards(needle):
            return self._mark_not_replayable(
                sheet_name, coord, call, "wildcard MATCH lookup value") and False
        m_sheet, m_first, _, rows = match_rng
        i_sheet, i_first, _, _ = index_rng
        self.lookup_targets.add((m_sheet, get_column_letter(m_first)))
        self._note_criterion(sheet_name, margs[0])
        if needle in (None, ""):
            self.skipped_empty += 1
            return True
        self.checked_cells += 1
        raw_row = self.match_row(rows, needle, trim=False)
        col_key = f"{sheet_name}!{re.sub(r'[0-9]+$', '', coord)} (INDEX+MATCH)"
        if raw_row is None:
            norm_row = self.match_row(rows, needle, trim=True) if isinstance(needle, str) else None
            if norm_row is not None:
                self.findings.append(Finding(
                    "whitespace/casing", f"{sheet_name}!{coord}",
                    f"MATCH of {short(needle, 40)!r} finds row {norm_row}",
                    "raw match fails; succeeds only after TRIM — silent lookup failure", "high"))
            else:
                misses_by_col[col_key].append((coord, needle))
        elif not volatile and whole:
            offset = raw_row - rows[0][0]
            got = self.wb[i_sheet].cell(row=index_rng[3][0][0] + offset, column=i_first).value
            if not self.values_equal(stored, got):
                stale_by_col[col_key].append((coord, stored, got))
        return True

    def check_duplicates(self) -> None:
        for sheet in self.x["sheets"]:
            for dup_col in sheet.get("anomalies", {}).get("duplicate_keys", []):
                col_letter = dup_col["column"]
                is_target = (sheet["name"], col_letter) in self.lookup_targets
                for entry in dup_col["values"]:
                    diff_note = self._duplicate_row_diff(sheet, col_letter, entry["cells"])
                    self.findings.append(Finding(
                        "key uniqueness",
                        f"{sheet['name']}!{', '.join(entry['cells'])}",
                        f"'{entry['value']}' unique in {sheet['name']}!{col_letter} "
                        f"({dup_col.get('header') or 'key column'}"
                        f"{'; lookup/COUNTIF target — first match wins' if is_target else ''})",
                        f"{entry['count']}x present{diff_note}",
                        "high" if is_target else "medium"))

    def _duplicate_row_diff(self, sheet, col_letter, cells) -> str:
        if sheet["name"] not in self.wb.sheetnames or len(cells) < 2:
            return ""
        ws = self.wb[sheet["name"]]
        rows = [int(re.sub(r"[A-Z]+", "", c)) for c in cells[:2]]
        differing = []
        for col in sheet["columns"]:
            if col["column"] == col_letter:
                continue
            idx = column_index_from_string(col["column"])
            a = ws.cell(row=rows[0], column=idx).value
            b = ws.cell(row=rows[1], column=idx).value
            if not self.values_equal(a, b):
                differing.append(col.get("header") or col["column"])
        if differing:
            return f"; rows differ in: {', '.join(differing[:6])} — conflicting records"
        return "; rows identical — redundant record"

    def check_whitespace_casing(self) -> None:
        for sheet in self.x["sheets"]:
            for ws_col in sheet.get("anomalies", {}).get("whitespace", []):
                key = (sheet["name"], ws_col["column"])
                in_lookups = key in self.lookup_targets or key in self.criterion_cols
                for cell in ws_col["cells"]:
                    self.findings.append(Finding(
                        "whitespace/casing",
                        f"{sheet['name']}!{cell['cell']}",
                        f"key without leading/trailing whitespace in "
                        f"'{ws_col.get('header') or ws_col['column']}'",
                        f"{cell['value']}"
                        + (" — column feeds lookups/COUNTIF: raw matching against this key is impossible"
                           if in_lookups else ""),
                        "high" if in_lookups else "low"))
            # casefold collisions on key-like columns
            if sheet["name"] not in self.wb.sheetnames:
                continue
            ws = self.wb[sheet["name"]]
            for col in sheet["columns"]:
                if not col.get("key_like"):
                    continue
                idx = column_index_from_string(col["column"])
                groups: dict[str, set] = defaultdict(set)
                for r in range(sheet["data_start_row"], sheet["data_end_row"] + 1):
                    v = ws.cell(row=r, column=idx).value
                    if isinstance(v, str) and v.strip():
                        groups[v.strip().casefold()].add(v.strip())
                for folded, variants in sorted(groups.items()):
                    if len(variants) > 1:
                        self.findings.append(Finding(
                            "whitespace/casing",
                            f"{sheet['name']}!{col['column']} "
                            f"({col.get('header') or 'key column'})",
                            "one canonical casing per key",
                            f"case variants coexist: {sorted(variants)}",
                            "low"))

    def _cf_thresholds(self) -> dict[tuple[str, str], set[int]]:
        """Day thresholds per (sheet, column), taken ONLY from direct comparisons
        against a cell of that same column (e.g. 'I5>=30' -> ('Sheet','I'): {30})."""
        out: dict[tuple[str, str], set[int]] = defaultdict(set)
        for sheet in self.x["sheets"]:
            for rule in sheet.get("conditional_formatting", []):
                if not isinstance(rule, dict) or rule.get("error"):
                    continue
                for f in rule.get("formulas", []):
                    for m in re.finditer(r"\$?([A-Z]{1,3})\$?\d+\s*[<>]=?\s*(\d+)\b", str(f)):
                        n = int(m.group(2))
                        if 0 < n <= 400:
                            out[(sheet["name"], m.group(1))].add(n)
        return out

    @staticmethod
    def _is_series(ages: list) -> bool:
        """Monotonic date column with volume = a time-series/log axis, not a register."""
        if len(ages) < 30:
            return False
        vals = [a for a, _, _ in ages]
        up = sum(1 for i in range(1, len(vals)) if vals[i] <= vals[i - 1])
        down = sum(1 for i in range(1, len(vals)) if vals[i] >= vals[i - 1])
        return max(up, down) >= 0.95 * (len(vals) - 1)

    def check_staleness(self) -> None:
        today = dt.date.today()
        cf_thresholds = self._cf_thresholds()
        clone_of = self._clone_of()
        for sheet in self.x["sheets"]:
            if sheet["name"] not in self.wb.sheetnames:
                continue
            if sheet["name"] in clone_of:
                continue   # P6: a clone repeats the representative's staleness cell by cell
            ws = self.wb[sheet["name"]]
            archive_like = bool(ARCHIVE_NAME_RE.search(sheet["name"]))
            key_col_idx = next(
                (column_index_from_string(c["column"]) for c in sheet["columns"] if c.get("key_like")),
                None)
            for col in sheet["columns"]:
                if "datetime" not in col["inferred_type"]:
                    continue
                header = col.get("header") or col["column"]
                closing_like = bool(re.search(r"(?i)(conclus|clos|fecho|fim|end)", header))
                idx = column_index_from_string(col["column"])
                ages = []
                for r in range(sheet["data_start_row"], sheet["data_end_row"] + 1):
                    v = ws.cell(row=r, column=idx).value
                    if isinstance(v, (dt.datetime, dt.date)):
                        d = v.date() if isinstance(v, dt.datetime) else v
                        key_val = (ws.cell(row=r, column=key_col_idx).value
                                   if key_col_idx else None)
                        ages.append(((today - d).days, f"{col['column']}{r}", key_val))
                if not ages:
                    continue
                own_days = sorted(d for d in cf_thresholds.get((sheet["name"], col["column"]), set()))
                # thresholds on a derived aging column also apply to the date column feeding it —
                # only the direct case is claimed; indirect feeds stay unclaimed (no check = no claim)
                bands = sorted(set(FIXED_AGE_BANDS) | set(own_days))
                dist = {f">={b}d": sum(1 for a, _, _ in ages if a >= b) for b in bands}
                future = sum(1 for a, _, _ in ages if a < 0)
                future_ratio = future / len(ages)
                is_series = self._is_series(ages)
                oldest = sorted(ages, reverse=True)[:MAX_OLDEST_ROWS]
                oldest_txt = "; ".join(
                    f"{a}d @{c}" + (f" ({short(k, 24)})" if k not in (None, "") else "")
                    for a, c, k in oldest)
                max_cf = max(own_days) if own_days else None
                beyond_cf = dist.get(f">={max_cf}d") if max_cf else None
                severity = "info"
                if (not archive_like and not closing_like and len(ages) >= 5
                        and future_ratio <= 0.2 and not is_series):
                    if beyond_cf or dist.get(">=120d"):
                        severity = "medium"
                notes = []
                if future:
                    notes.append(f"{future} in the future" + (" (forward/curve column)" if future_ratio > 0.2 else ""))
                if is_series:
                    notes.append("monotonic dates (time-series axis, not a register)")
                found = (f"{len(ages)} dated rows; distribution {dist}"
                         + ("; " + "; ".join(notes) if notes else "")
                         + f"; oldest: {oldest_txt}")
                expected = (f"rows within this column's conditional-formatting thresholds (max {max_cf}d)"
                            if max_cf else "recent activity")
                self.findings.append(Finding(
                    "staleness",
                    f"{sheet['name']}!{col['column']} ({header})",
                    expected, found, severity))
        # file-level staleness
        try:
            mtime = dt.datetime.fromisoformat(self.x["identity"]["modified"]).date()
            age = (dt.date.today() - mtime).days
            if age > STALE_FILE_DAYS:
                self.findings.append(Finding(
                    "staleness", self.x["identity"]["filename"],
                    f"file touched within {STALE_FILE_DAYS} days",
                    f"last modified {mtime.isoformat()} ({age} days ago) — stored TODAY()-based "
                    "values are frozen at an older date", "info"))
        except Exception:
            pass

    @staticmethod
    def _cell_span(cells: list[str]) -> str:
        rows = sorted(int(re.sub(r"[A-Z]+", "", c)) for c in cells)
        letter = re.sub(r"[0-9]+", "", cells[0])
        if len(rows) == 1:
            return f"{letter}{rows[0]}"
        return f"{letter}{rows[0]}:{letter}{rows[-1]} ({len(cells)} cells)"

    def _has_convention(self, f: dict) -> bool:
        """True when the column provably follows one fill-down pattern worth policing."""
        return (f.get("count", 0) >= self.CONVENTION_MIN_FORMULAS
                and f.get("dominant_count", 0) / max(1, f.get("count", 1)) >= self.CONVENTION_MIN_COVERAGE)

    # ------------------------------------------------ clones, labels, live overrides (P6, P7, P8)
    _LIVE_OVERRIDE_RE = re.compile(r"^=\+?\$?([A-Z]{1,3})\$?(\d+)(\s*[+-]\s*\d+(?:\.\d+)?)?$")
    _PLACEHOLDER_RE = re.compile(r"^[\s\-\u2014\u2013_.\u00b7/*xX]*$")

    def _clone_groups(self) -> dict[str, list[str]]:
        """P6: sheets that replicate one another (module-level `clone_groups`, shared with CalcChain)."""
        return clone_groups(self.x)

    def _clone_of(self) -> dict[str, str]:
        return {c: rep for rep, cs in self._clone_groups().items() for c in cs}

    def _label_rows(self, sheet_name: str) -> set[int]:
        """P7-B: rows inside the data range whose non-empty cells are ALL text (no number, no
        formula) — label bands. Text there is layout, never an override of logic."""
        cache = getattr(self, "_label_rows_cache", None)
        if cache is None:
            self._label_rows_cache = cache = {}
        if sheet_name in cache:
            return cache[sheet_name]
        fwb = getattr(self, "_fwb", None)
        ws = fwb[sheet_name] if fwb is not None and sheet_name in fwb.sheetnames else None
        rows: set[int] = set()
        sheet = next((s for s in self.x["sheets"] if s["name"] == sheet_name), None)
        if ws is not None and sheet:
            last = min(max(sheet.get("data_end_row") or 0, 1) + 2, ws.max_row or 1, MAX_SCAN_ROWS)
            for r in range(1, last + 1):
                vals = [c.value for c in ws[r] if c.value not in (None, "")]
                texts = [v for v in vals if isinstance(v, str) and not v.startswith("=")]
                numbers = [v for v in vals if isinstance(v, (int, float)) and not isinstance(v, bool)]
                if len(texts) >= 2 and len(numbers) <= max(1, len(texts) // 5):
                    rows.add(r)   # labels (and formulas) dominate; a numeric grade used as a label is tolerated
        cache[sheet_name] = rows
        return rows

    @staticmethod
    def _feed_fed(f: dict) -> bool:
        """A column whose dominant pattern reads another sheet, an add-in or another workbook."""
        pat = f.get("dominant_pattern") or ""
        return "!" in pat or "_xll." in pat.lower() or bool(_CALC_EXTERNAL_RE.search(pat))

    def check_pattern_exceptions(self) -> None:
        groups = self._clone_groups()
        clone_of = self._clone_of()
        for sheet in self.x["sheets"]:
            name = sheet["name"]
            if name in clone_of:
                continue   # P6: policed once, on the representative
            tag = ""
            if name in groups:
                cs = groups[name]
                tag = f" (+{len(cs)} clone{'s' if len(cs) > 1 else ''}: {', '.join(cs[:4])}{'…' if len(cs) > 4 else ''})"
            label_rows = self._label_rows(name)
            typed_numbers: set[tuple[int, int]] = set()   # (row, col_idx) of numeric typed overrides on this sheet
            for col in sheet["columns"]:
                for e in ((col.get("formula") or {}).get("exceptions", {}) or {}).get("typed_overrides", []):
                    if not isinstance(e["value"], str) or re.fullmatch(r"-?\d+(?:[.,]\d+)?", str(e["value"]).strip()):
                        typed_numbers.add((int(re.sub(r"\D", "", str(e["cell"])) or 0), column_index_from_string(re.sub(r"\d", "", str(e["cell"])))))
            no_convention_cols = []
            label_hits: list[str] = []
            for col in sheet["columns"]:
                f = col.get("formula")
                if not f:
                    continue
                if not self._has_convention(f):
                    # model-style column (each row its own formula): no provable
                    # convention -> no per-cell exception claims (no check = no claim)
                    if f.get("count", 0) > 0 and col["class"] == "derived":
                        no_convention_cols.append(col["column"])
                    continue
                exc = f.get("exceptions", {})
                loc = f"{name}!{col['column']}"
                # P7: a text in a label band, or a placeholder (`-`), is layout — not an override
                real, labels = [], []
                for e in exc.get("typed_overrides", []):
                    row = int(re.sub(r"\D", "", str(e["cell"])) or 0)
                    v = e["value"]
                    cidx = column_index_from_string(col["column"])
                    beside_number = any((row, cidx + d) in typed_numbers for d in (-1, 1))
                    if isinstance(v, str) and not re.fullmatch(r"-?\d+(?:[.,]\d+)?", v.strip()) and (
                            row in label_rows or self._PLACEHOLDER_RE.match(v) or beside_number):
                        labels.append(e)
                    else:
                        real.append(e)
                label_hits.extend(f"{e['cell']}={e['value']!r}" for e in labels)
                if real:
                    examples = "; ".join(f"{e['cell']}={e['value']!r}" for e in real[:3])
                    self.findings.append(Finding(
                        "pattern exceptions",
                        f"{name}!{self._cell_span([e['cell'] for e in real])}{tag}",
                        f"formula column ({short(f['dominant_pattern'], 60)})",
                        f"{len(real)} typed value(s) replace the formula — manual override "
                        f"of automated logic ({examples})", "medium"))
                # P8: a self-column reference in a feed-fed column is a live-data override → high, per cell
                live, rest = [], []
                for e in exc.get("divergent_formulas", []):
                    mm = self._LIVE_OVERRIDE_RE.match(str(e["formula"]).replace(" ", ""))
                    row = int(re.sub(r"\D", "", str(e["cell"])) or 0)
                    if (mm and self._feed_fed(f) and mm.group(1) == col["column"]
                            and 1 <= abs(int(mm.group(2)) - row) <= 5):
                        live.append((e, mm))
                    else:
                        rest.append(e)
                for e, mm in live:
                    src = f"{mm.group(1)}{mm.group(2)}"
                    op = (" " + mm.group(3).replace(" ", "")) if mm.group(3) else ""
                    self.findings.append(Finding(
                        "pattern exceptions", f"{name}!{e['cell']}{tag}",
                        f"feed-fed column ({short(f['dominant_pattern'], 60)})",
                        f"cell overrides the feed with a reference to its own column "
                        f"({short(e['formula'], 40)} → {src}{op}) — live-data override: a human value "
                        f"replacing the day's quote", "high"))
                if rest:
                    families = len({e["formula"] for e in rest})
                    examples = "; ".join(f"{e['cell']}: {short(e['formula'], 60)}" for e in rest[:2])
                    self.findings.append(Finding(
                        "pattern exceptions",
                        f"{name}!{self._cell_span([e['cell'] for e in rest])}{tag}",
                        f"one fill-down pattern for the whole column "
                        f"({short(f['dominant_pattern'], 60)})",
                        f"{len(rest)} cell(s) carry {families} divergent formula variant(s) — "
                        f"manually re-anchored copies can misalign rows ({examples})", "medium"))
                stray = exc.get("formula_in_manual_column", [])
                if stray:
                    examples = "; ".join(f"{e['cell']}: {short(e['formula'], 60)}" for e in stray[:2])
                    self.findings.append(Finding(
                        "pattern exceptions",
                        f"{name}!{self._cell_span([e['cell'] for e in stray])}{tag}",
                        f"typed column {loc}",
                        f"{len(stray)} stray formula(s) in a manual column ({examples})", "low"))
            if no_convention_cols:
                cols = ", ".join(no_convention_cols[:12]) + ("…" if len(no_convention_cols) > 12 else "")
                self.findings.append(Finding(
                    "pattern exceptions", f"{name} (columns {cols}){tag}",
                    "columns follow a fill-down convention",
                    f"{len(no_convention_cols)} derived column(s) have no dominant pattern "
                    "(model-style sheet: each row its own formula) — per-cell exception "
                    "checks suppressed for them", "info"))
            if label_hits:
                rows = sorted({int(re.sub(r"\D", "", h.split("=")[0]) or 0) for h in label_hits})
                self.findings.append(Finding(
                    "layout labels", f"{name} (rows {', '.join(map(str, rows[:8]))}{'…' if len(rows) > 8 else ''}){tag}",
                    "data range free of text bands",
                    f"{len(label_hits)} label/placeholder text(s) inside formula columns — layout, "
                    f"not overrides of logic ({'; '.join(label_hits[:4])})", "info"))

    @staticmethod
    def _cell_text(cell):
        f = formula_text(cell)
        return f if f is not None else cell.value

    @staticmethod
    def _diff_kind(a, bs: list) -> tuple[str, str]:
        def kind(v):
            if v is None or v == "":
                return "empty"
            if isinstance(v, str):
                return "formula" if v.startswith("=") else "text"
            return "number"
        ka = kind(a)
        kbs = {kind(b) for b in bs}
        kinds = {ka} | kbs
        if kinds == {"formula"}:
            return "formula differs", "high"
        if kinds == {"number"}:
            return "typed value differs", "high"
        if kinds <= {"formula", "number"}:
            return "formula vs typed value", "high"
        if "text" in kinds:
            return "text differs", "medium"
        return "presence differs", "medium"

    def check_clone_divergence(self) -> None:
        """P6: cells that differ between a representative sheet and its clones — the rule that
        changed in one place and not in the other. One finding per run of adjacent cells of the
        same column and kind; the values of both sides are named."""
        fwb = getattr(self, "_fwb", None)
        if fwb is None:
            return
        for rep, clones in self._clone_groups().items():
            if rep not in fwb.sheetnames:
                continue
            rws = fwb[rep]
            diffs: dict[str, list[tuple[str, object]]] = defaultdict(list)
            for cname in clones:
                if cname not in fwb.sheetnames:
                    continue
                cws = fwb[cname]
                last_row = min(max(rws.max_row or 1, cws.max_row or 1), MAX_SCAN_ROWS)
                for r in range(1, last_row + 1):
                    for c in range(1, max(rws.max_column or 1, cws.max_column or 1) + 1):
                        a = self._cell_text(rws.cell(r, c))
                        b = self._cell_text(cws.cell(r, c))
                        if a != b:
                            diffs[rws.cell(r, c).coordinate].append((cname, b))
            by_col_kind: dict[tuple[str, str], list[tuple[int, str, object, list]]] = defaultdict(list)
            for coord, lst in diffs.items():
                a = self._cell_text(rws[coord])
                kind, sev = self._diff_kind(a, [b for _, b in lst])
                col = re.sub(r"\d", "", coord)
                by_col_kind[(col, kind + "|" + sev)].append((int(re.sub(r"\D", "", coord)), coord, a, lst))
            for (col, kindsev), items in by_col_kind.items():
                kind, sev = kindsev.split("|")
                items.sort()
                run = [items[0]]
                for it in items[1:]:
                    if it[0] == run[-1][0] + 1:
                        run.append(it)
                    else:
                        self._emit_divergence(rep, kind, sev, run)
                        run = [it]
                self._emit_divergence(rep, kind, sev, run)

    def _emit_divergence(self, rep: str, kind: str, sev: str, run: list) -> None:
        first = run[0]
        coords = [it[1] for it in run]
        loc = coords[0] if len(coords) == 1 else f"{coords[0]}:{coords[-1]} ({len(coords)} cells)"
        clones = sorted({cname for it in run for cname, _ in it[3]})
        found = "; ".join(f"{cname} = {short(b, 40)!s}" for cname, b in first[3][:4])
        self.findings.append(Finding(
            "clone divergence", f"{rep}!{loc} vs {', '.join(clones[:4])}",
            f"{rep}!{first[1]} = {short(first[2], 50)!s}" + (f" (and {len(run) - 1} adjacent)" if len(run) > 1 else ""),
            f"{found} — {kind}", sev))

    def check_orphans(self) -> None:
        known = set(self.wb.sheetnames)
        for sheet in self.x["sheets"]:
            for unknown in sheet.get("unknown_sheet_refs", []):
                self.findings.append(Finding(
                    "orphan references", f"{sheet['name']} (formulas)",
                    "formula references resolve to sheets in this workbook",
                    f"referenced sheet '{unknown}' does not exist", "high"))
        seen_broken: set[tuple] = set()
        for nr in self.x.get("workbook", {}).get("named_ranges", []):
            if isinstance(nr, dict) and "#REF!" in str(nr.get("target", "")):
                key = (nr.get("name"), nr.get("target"))
                if key in seen_broken:
                    continue
                seen_broken.add(key)
                scopes = [str(o.get("scope")) for o in self.x["workbook"]["named_ranges"]
                          if isinstance(o, dict) and (o.get("name"), o.get("target")) == key]
                self.findings.append(Finding(
                    "orphan references",
                    f"named range '{nr.get('name')}' (scope: {', '.join(scopes)})",
                    "named range points at a live range",
                    f"target is broken: {nr.get('target')}", "medium"))
        for (t_sheet, t_col) in sorted(self.lookup_targets):
            if t_sheet not in known:
                continue
            meta = self.sheet_meta(t_sheet)
            if not meta:
                continue
            col = next((c for c in meta["columns"] if c["column"] == t_col), None)
            if col is None or col["rows_nonempty"] == 0:
                self.findings.append(Finding(
                    "orphan references", f"{t_sheet}!{t_col}",
                    "lookup target column holds data",
                    "lookups point at an empty column — every lookup fails", "medium"))


_UNSUPPORTED = object()

CHECK_ORDER = ["lookup integrity", "key uniqueness", "whitespace/casing",
               "staleness", "pattern exceptions", "clone divergence", "layout labels", "orphan references"]


def _target_label(alvo: dict) -> str:
    """O alvo numa celula de tabela — sem partir o markdown."""
    nome = str(alvo.get("name") or "?").replace("|", "\\|")
    marca = " (outside this file)" if alvo.get("external") else ""
    return f"`{nome}`{marca}"


def render_replay_md(extraction: dict, rep: Replayer, out_path: str) -> tuple[int, dict]:
    sev_rank = Finding.ORDER
    findings = sorted(rep.findings, key=lambda f: (sev_rank[f.severity], CHECK_ORDER.index(f.check), f.location))
    by_check = {c: Counter() for c in CHECK_ORDER}
    for f in findings:
        by_check[f.check][f.severity] += 1

    lines = []
    ident = extraction["identity"]
    lines.append(f"# Replay report — {ident['filename']}")
    lines.append("")
    lines.append(f"> Source sha256: `{ident['sha256'][:12]}` | Replayed: {now_iso()} | "
                 f"Tool: xlsx_extract.py v{TOOL_VERSION} | Cells checked: {rep.checked_cells} "
                 f"(skipped {rep.skipped_empty} empty lookups)")
    lines.append("> Rule: **no check = no claim.** Every row below is a mechanical recomputation; "
                 "anything the battery cannot replay is listed under *Not replayable*.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("| check | findings | high | medium | low | info |")
    lines.append("|---|---|---|---|---|---|")
    for check in CHECK_ORDER:
        c = by_check[check]
        total = sum(c.values())
        lines.append(f"| {check} | {total} | {c['high']} | {c['medium']} | {c['low']} | {c['info']} |")
    lines.append("")

    lines.append("## Findings")
    lines.append("")
    if findings:
        lines.append("| # | check | location | expected | found | severity |")
        lines.append("|---|---|---|---|---|---|")
        for i, f in enumerate(findings, 1):
            def esc(s: str) -> str:
                return str(s).replace("|", "\\|").replace("\n", " ")
            lines.append(f"| {i} | {f.check} | `{esc(f.location)}` | {esc(f.expected)} | "
                         f"{esc(f.found)} | **{f.severity}** |")
    else:
        lines.append("**0 findings.** The battery ran and found nothing — absence of findings is "
                     "itself evidence (checked cells: " + str(rep.checked_cells) + ").")
    lines.append("")
    nr_total = sum(rep.not_replayable.values())
    lines.append(f"**Out of scope: {nr_total} formula call(s) declined as not replayable** "
                 "(see below). A declined call produces no finding in either direction: it is "
                 "neither a defect nor a clean check.")
    lines.append("")

    lines.append("## Not replayable")
    lines.append("")
    if rep.not_replayable:
        ranges = rep.to_read_ranges()
        lines.append("| formula / reason | cells | example | to_read | what to read |")
        lines.append("|---|---|---|---|---|")
        for pattern, count in rep.not_replayable.most_common():
            safe = pattern.replace("|", "\\|")
            rs = ranges.get(pattern, [])
            shown = ", ".join(f"`{r}`" for r in rs[:6]) + (f" (+{len(rs) - 6})" if len(rs) > 6 else "")
            alvos_p = ", ".join(_target_label(a) for a in rep.nr_targets.get(pattern, {}).values())
            lines.append(f"| {safe} | {count} | `{rep.nr_example[pattern]}` | {shown} | {alvos_p} |")
        lines.append("")
        alvos = rep.to_read_targets()
        if alvos:
            lines.append("**What to read** — the declined calls point at a short, finite set of "
                         "targets. Reading the target resolves the whole family; the cells above "
                         "are where the calls sit, not what has to be opened.")
            lines.append("")
            lines.append("| target | kind | where | calls |")
            lines.append("|---|---|---|---|")
            for a in alvos:
                nota = " — **outside this file**" if a.get("external") else ""
                extra = (f" (one of {a['count']}, e.g. `{a.get('example')}`)"
                         if a.get("count") else "")
                lines.append("| `{}` | {} | `{}`{}{} | {} |".format(
                    a["name"], a["kind"], a.get("where") or "?", extra, nota, a["calls"]))
            lines.append("")
        lines.append(f"These are **TO-READ** for the process model — {rep.to_read_count()} range(s) to read, "
                     "never inferred. A declined call is not an Unknown: the formula is legible, it was "
                     "not recomputed (`states.md` → *Confirmed threshold*, rule 2).")
    else:
        lines.append("None — every formula family found was inside the supported battery.")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append(f"- Staleness ages are computed against the replay date ({dt.date.today().isoformat()}); "
                 "re-running on another day shifts day counts, not conclusions.")
    lines.append("- Text matching mirrors Excel: case-insensitive; the TRIM pass isolates "
                 "whitespace-only defects.")
    lines.append("- Declared limits of the battery: lookups are replayed first-to-last and "
                 "literally. `XLOOKUP` with `search_mode` other than 1, and any criterion "
                 "carrying Excel wildcards (`*`, `?`, `~`), are declined as not replayable "
                 "instead of being compared under the wrong semantics — those formulas are "
                 "correct in Excel and a literal comparison would report anomalies that do "
                 "not exist.")
    lines.append("")

    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    tmp = out_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    os.replace(tmp, out_path)
    return len(findings), {c: sum(by_check[c].values()) for c in CHECK_ORDER}


def replay(path: str, extraction_path: str, out_path: str, log_path: str | None) -> int:
    filename = os.path.basename(path)
    for p in (path, extraction_path):
        if not os.path.exists(p):
            print(f"not found: {p}", file=sys.stderr)
            return 2
    with open(extraction_path, encoding="utf-8") as fh:
        extraction = json.load(fh)
    if extraction.get("status") != "ok":
        print(f"extraction status is '{extraction.get('status')}' — nothing to replay "
              f"(reason: {extraction.get('reason')})", file=sys.stderr)
        return 3
    sha = sha256_file(path)
    if extraction.get("identity", {}).get("sha256") != sha:
        print("extraction is STALE (file sha256 changed) — re-run L1 extraction first", file=sys.stderr)
        append_log(log_path, "L3", filename, "stale-extraction", f"file sha256 {sha[:8]}")
        return 3

    try:
        wb_data = load_workbook(path, data_only=True)
        wb_formula = load_workbook(path, data_only=False)
    except Exception as exc:
        print(f"replay failed to open workbook: {exc}", file=sys.stderr)
        append_log(log_path, "L3", filename, "failed", short(str(exc), 120))
        return 3

    rep = Replayer(wb_data, extraction)
    rep._fwb = wb_formula
    rep.run()
    n, per_check = render_replay_md(extraction, rep, out_path)
    nr_total = sum(rep.not_replayable.values())
    if nr_total:
        print(f"not replayable: {nr_total} call(s) declined — "
              + ", ".join(f"{r} x{c}" for r, c in rep.not_replayable.most_common(4)))
    print(f"replayed: {filename} -> {out_path} ({n} findings; "
          + ", ".join(f"{k}: {v}" for k, v in per_check.items() if v) + (")" if any(per_check.values()) else "0 across all checks)"))
    append_log(log_path, "L3", filename, "replayed",
               f"{n} findings, {nr_total} not replayable")
    if nr_total:
        append_log(log_path, "L3", filename, "not replayable",
                   f"{nr_total} calls -> {rep.to_read_count()} ranges TO-READ")
    # P3/P3b: the calc chain rides on the same open workbook — <file>.calc-chain.json + .md beside the replay
    chain_json = re.sub(r"\.replay\.md$", ".calc-chain.json", out_path)
    if chain_json == out_path:
        chain_json = out_path + ".calc-chain.json"
    try:
        boundary = extraction.get("capability_boundary") or capability_boundary(path, wb_formula, extraction)
        chain = CalcChain(wb_formula, extraction, boundary=boundary).run()
        write_calc_chain(chain, chain_json, filename, log_path)
    except Exception as exc:  # the chain never blocks the replay it rides on
        print(f"calc-chain failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        append_log(log_path, "L3", filename, "calc-chain: absent", short(f"{type(exc).__name__}: {exc}", 120))
    return 0


# ------------------------------------------------------------ calc chain (P3, P9, P3b, P3d)
#
# The replay recomputes values. The calc chain reads formulas. They are different
# operations on the same cell (states.md → Confirmed threshold, rule 2): a formula the
# battery cannot recompute — INDIRECT built from text, INDEX/MATCH outside the supported
# argument shapes — still says what the artefact calculates, cell by cell. This pass
# reconstructs, for each labelled output cell of a visible non-clone sheet, the chain of
# precedents back to typed values, feeds and named ranges, and annotates by SHAPE only:
# aggregation (SUM/AVERAGE*), selection (MIN/MAX), lookup (INDEX/MATCH/…), rounding,
# conversion factors (a literal 0<k<2 used multiplicatively), unlabelled additive
# constants (`+10`, `-10`), and dynamic INDIRECT prefixes as TO-READ targets. No business
# meaning is attached: naming what `+10` is belongs to the L2 pass and to the owner.
#
# P3b — capability boundary. Calculation that does not live in cells (Power Query, data
# model, add-in functions, RTD, external workbooks, VBA) is declared by the PRESENCE of
# its OOXML part or formula signature, never inferred; every branch of a chain ends in one
# of five terminal classes, or the block is `invalid`.
# P3d — traversal budget. A candidate above the budget never disappears: it is grouped
# (same normalized pattern, name dimension and absolute row collapsed) or listed TO-READ.
# `rendered + grouped + absorbed + to_read == candidates`, checked by code.

CHAIN_BUDGET = {"max_blocks": 60, "max_depth": 12, "max_nodes": 240, "max_steps_rendered": 4}
CALC_MAX_DEPTH = CHAIN_BUDGET["max_depth"]
CALC_MAX_NODES = CHAIN_BUDGET["max_nodes"]
CALC_MAX_BLOCKS = CHAIN_BUDGET["max_blocks"]
CALC_RANGE_EXPAND = 64          # a range this small is walked cell by cell
CALC_RANGE_SCAN = 400           # a larger range is scanned this far for one representative formula
CALC_LABEL_REACH = 3            # cells to the left / rows above searched for a label
CALC_NAMED_COLUMN_MIN_ROWS = 8  # a name spanning this many rows declares an input column
CLONE_MIN_SHARED = 0.9          # sheets with this share of identical column patterns replicate one another
TERMINAL_CLASSES = ("typed", "feed", "named_static", "to_read", "boundary")

_CALC_AGG = ("SUM(", "SUMIF(", "SUMIFS(", "AVERAGE(", "AVERAGEIF(", "AVERAGEIFS(", "SUMPRODUCT(", "COUNT(", "COUNTIF(", "COUNTIFS(")
_CALC_SEL = ("MIN(", "MAX(", "LARGE(", "SMALL(")
_CALC_LOOKUP = ("INDEX(", "MATCH(", "VLOOKUP(", "HLOOKUP(", "XLOOKUP(", "INDIRECT(", "OFFSET(", "LOOKUP(")
_CALC_ROUND = ("ROUND(", "ROUNDUP(", "ROUNDDOWN(", "INT(", "TRUNC(", "MROUND(", "CEILING(", "FLOOR(")
# literals inside these calls are arguments (indexes, offsets, digits), never price constants
_CALC_ARG_FUNCS = {"INDEX", "MATCH", "OFFSET", "ROUND", "ROUNDUP", "ROUNDDOWN", "MROUND", "CEILING", "FLOOR",
                   "WEEKDAY", "DATE", "EDATE", "EOMONTH", "TEXT", "LEFT", "RIGHT", "MID", "SUMIFS", "SUMIF",
                   "COUNTIF", "COUNTIFS", "AVERAGEIF", "AVERAGEIFS", "LARGE", "SMALL", "CHOOSE", "XLOOKUP",
                   "VLOOKUP", "HLOOKUP", "ADDRESS", "ROW", "COLUMN", "SUBSTITUTE", "REPT", "MOD", "POWER"}
_CALC_NAME_RE = re.compile(r"(?<![\w.$!'\"])([A-Za-z_\\À-ɏ][\w.À-ɏ]*)(?![\w(!])")
_CALC_DATE_RE = re.compile(r"(?i)(?<![A-Z_.])(WEEKDAY|TODAY|NOW|DATE|DATEVALUE|EDATE|EOMONTH|WORKDAY|NETWORKDAYS)\(")
_CALC_LABEL_MIN_ALNUM = 2
_CALC_DATEFMT_RE = re.compile(r"(?i)(?<![\\\[])[dmy]{1,4}[-/. ][dmy]{1,4}|yyyy|dd/mm|mm/dd")
_CALC_NUM_RE = re.compile(r"(?<![\w.$:])(\d+(?:\.\d+)?)(?![\d.:\w])")
_CALC_EXTERNAL_RE = re.compile(r"\[\d+\]|'\[[^\]]+\]")            # `[1]Sheet!A1` / `'[book.xlsx]Sheet'!A1`
_CALC_ABS_ROW_RE = re.compile(r"R(\d+)C")                          # absolute row in R1C1 → collapsed
_CALC_MODERN_RE = re.compile(r"(?i)(?<![A-Z_.])(LAMBDA|LET|BYROW|BYCOL|MAP|REDUCE|SCAN|MAKEARRAY)\(")
_CALC_RTD_RE = re.compile(r"(?i)(?<![A-Z_.])(RTD|WEBSERVICE|FILTERXML)\(")


def clone_groups(extraction: dict) -> dict[str, list[str]]:
    """Sheets with the same dimensions, the same column set and ≥ CLONE_MIN_SHARED of identical
    dominant formula patterns replicate one another (the four moeda×unidade snapshots, the
    Simulador). The first in workbook order represents the group; the others are listed under it."""
    def profile(sheet):
        return {c["column"]: (c.get("formula") or {}).get("dominant_pattern") for c in sheet.get("columns", [])}
    reps: list[tuple[str, str, dict]] = []   # (dimensions, name, profile)
    groups: dict[str, list[str]] = {}
    for sheet in extraction.get("sheets", []):
        prof = profile(sheet)
        if not any(v for v in prof.values()):
            continue   # a sheet without formulas is data, never a clone of a calculation sheet
        placed = False
        for dims, rep, rprof in reps:
            if dims != sheet.get("dimensions") or set(rprof) != set(prof):
                continue
            same = sum(1 for k in rprof if rprof[k] == prof[k])
            if same >= CLONE_MIN_SHARED * len(rprof):
                groups.setdefault(rep, []).append(sheet["name"])
                placed = True
                break
        if not placed:
            reps.append((sheet.get("dimensions"), sheet["name"], prof))
    return groups


def capability_boundary(path: str | None, wb_formula, extraction: dict) -> dict:
    """P3b-1. What this workbook computes OUTSIDE cells, declared by presence of an OOXML part
    or of a formula signature — never by inference. `present: False` means the part is not in
    the package, not that the calculation does not exist elsewhere."""
    def entry(present, detail="", locator=""):
        return {"present": bool(present), "detail": detail, "locator": locator}
    out = {k: entry(False) for k in ("power_query", "data_model", "vba", "addin_functions", "external_links",
                                      "rtd", "dynamic_names", "iterative", "merged_scan_fail", "pivot_caches",
                                      "modern_functions")}
    names: list[str] = []
    if path and os.path.exists(path):
        try:
            with zipfile.ZipFile(path) as zf:
                names = zf.namelist()
                custom = [n for n in names if n.lower().startswith("customxml/") and n.lower().endswith(".xml")]
                mashup = [n for n in custom if b"DataMashup" in zf.read(n)[:4096]]
                conns = [n for n in names if n.lower() == "xl/connections.xml"]
                conn_detail = ""
                if conns:
                    raw = zf.read(conns[0])
                    kinds = sorted(set(re.findall(rb'<connection [^>]*?type="(\d+)"', raw)))
                    conn_detail = f"xl/connections.xml types={[k.decode() for k in kinds]}"
                if mashup or conns:
                    out["power_query"] = entry(True, "; ".join(filter(None, [f"DataMashup in {mashup[0]}" if mashup else "", conn_detail])),
                                               mashup[0] if mashup else (conns[0] if conns else ""))
                model = [n for n in names if n.lower().startswith("xl/model/")]
                if model:
                    out["data_model"] = entry(True, f"{len(model)} part(s) under xl/model/", model[0])
                vba = [n for n in names if n.lower().endswith("vbaproject.bin")]
                if vba:
                    out["vba"] = entry(True, "vbaProject.bin present (modules not decompiled)", vba[0])
                ext = []
                for rel in (n for n in names if n.startswith("xl/externalLinks/_rels/")):
                    ext += [t.decode("utf-8", "replace") for t in re.findall(rb'Target="([^"]+)"', zf.read(rel))]
                if ext:
                    out["external_links"] = entry(True, "; ".join(ext[:4]) + (f" (+{len(ext) - 4})" if len(ext) > 4 else ""), "xl/externalLinks/")
                piv = [n for n in names if n.lower().startswith("xl/pivotcache/")]
                if piv:
                    out["pivot_caches"] = entry(True, f"{len(piv)} pivot cache part(s)", piv[0])
                if "xl/workbook.xml" in names:
                    wbxml = zf.read("xl/workbook.xml")
                    m = re.search(rb'<calcPr[^>]*iterate="(1|true)"', wbxml)
                    if m:
                        out["iterative"] = entry(True, "calcPr iterate=1 (intentional circular references)", "xl/workbook.xml#calcPr")
        except Exception as exc:
            out["_error"] = f"{type(exc).__name__}: {exc}"
    # formula signatures
    addins: Counter = Counter()
    ext_formula: list[str] = []
    dyn: list[str] = []
    rtd: list[str] = []
    modern: list[str] = []
    if wb_formula is not None:
        for ws in wb_formula.worksheets:
            # a formula signature repeats: a sheet that calls an add-in calls it in its first rows.
            # Walking the declared grid cost 5.8 GB and 93 s on a sheet declaring 1 048 576 rows.
            for row in ws.iter_rows(max_row=sheet_scan_end(extraction, ws.title, ws)):
                for cell in row:
                    f = formula_text(cell)
                    if not f:
                        continue
                    for m in re.finditer(r"_xll\.([A-Za-z_][\w.]*?)\.", f):
                        addins[m.group(1)] += 1
                    if _CALC_EXTERNAL_RE.search(f) and len(ext_formula) < 6:
                        ext_formula.append(f"{ws.title}!{cell.coordinate}")
                    if "INDIRECT(" in f.upper():
                        for call in find_calls(f, "INDIRECT"):
                            arg = split_args(call)[0] if "(" in call else ""
                            if not STRING_SEG_RE.search(arg) and len(dyn) < 6:
                                dyn.append(f"{ws.title}!{cell.coordinate}")
                    if _CALC_RTD_RE.search(f) and len(rtd) < 6:
                        rtd.append(f"{ws.title}!{cell.coordinate}")
                    if _CALC_MODERN_RE.search(f) and len(modern) < 6:
                        modern.append(f"{ws.title}!{cell.coordinate}")
    if addins:
        out["addin_functions"] = entry(True, ", ".join(f"_xll.{k} ×{v}" for k, v in addins.most_common(4)), "formula signature `_xll.`")
    if ext_formula and not out["external_links"]["present"]:
        out["external_links"] = entry(True, "external workbook reference by formula; no xl/externalLinks part", ext_formula[0])
    elif ext_formula:
        out["external_links"]["detail"] += f"; referenced from {ext_formula[0]}"
    if dyn:
        out["dynamic_names"] = entry(True, f"INDIRECT with no string literal ×{len(dyn)}+", dyn[0])
    if rtd:
        out["rtd"] = entry(True, "RTD/WEBSERVICE call", rtd[0])
    if modern:
        out["modern_functions"] = entry(True, "LAMBDA/LET-family call (outside the replay battery)", modern[0])
    failed = [s["name"] for s in extraction.get("sheets", []) if any("fill scan failed" in e for e in s.get("errors", []))]
    if failed:
        out["merged_scan_fail"] = entry(True, "fill scan failed (merged cells / layout)", ", ".join(failed[:6]))
    return out


def _calc_strip_strings(formula: str) -> str:
    return "".join(seg if not is_str else '""' for is_str, seg in _split_strings(formula))


def _calc_enclosing_funcs(text: str) -> list[str | None]:
    """For every character position, the innermost enclosing function name (or None)."""
    out: list[str | None] = [None] * len(text)
    stack: list[str | None] = []
    upper = text.upper()
    for i, ch in enumerate(text):
        if ch == "(":
            m = re.search(r"([A-Z_][A-Z0-9_.]*)$", upper[:i])
            stack.append(m.group(1) if m else None)
        elif ch == ")":
            if stack:
                stack.pop()
        out[i] = stack[-1] if stack else None
    return out


class CalcChain:
    """Static precedent walk from labelled output cells, annotated by shape only."""

    def __init__(self, wb_formula, extraction: dict, boundary: dict | None = None, budget: dict | None = None):
        self.wb = wb_formula
        self.x = extraction
        self.boundary = boundary or extraction.get("capability_boundary") or capability_boundary(None, wb_formula, extraction)
        self.budget = dict(CHAIN_BUDGET, **(budget or {}))
        self.sheets = {ws.title: ws for ws in wb_formula.worksheets}
        self.names: dict[str, tuple[str, str] | None] = {}
        self.name_case: dict[str, str] = {}
        self.name_family: dict[str, str] = {}          # name(lower) -> family prefix (≥ 2 names share it)
        self.families: dict[str, list[str]] = {}       # prefix -> suffixes
        self.clones = clone_groups(extraction)
        self.clone_of = {c: rep for rep, cs in self.clones.items() for c in cs}
        self.indegree: Counter = Counter()
        self.named_columns: set[tuple[str, str, int, int]] = set()
        self.to_read: dict[str, dict] = {}
        self.blocks: list[dict] = []
        self.dimensions: list[dict] = []
        self.skipped: Counter = Counter()
        self._formula_cache: dict[tuple[str, str], str | None] = {}
        self._empty_cache: dict[tuple[str, str], bool] = {}

    # ---------------------------------------------------------------- setup
    def _load_names(self) -> None:
        entries = (self.x.get("workbook") or {}).get("named_ranges") or []
        if not entries:
            try:
                entries = [{"name": n, "target": d.attr_text, "scope": "workbook"}
                           for n, d in self.wb.defined_names.items()]
            except Exception:
                entries = []
        for e in entries:
            name, target = e.get("name"), e.get("target")
            if not name or not isinstance(target, str):
                continue
            key = name.lower()
            if key in self.names and e.get("scope") not in (None, "workbook"):
                continue  # workbook scope wins over sheet scope on collision
            self.name_case[key] = name
            m = REF_RE.search(target)
            if "#REF" in target or not m:
                self.names[key] = None
                continue
            sheet = _unquote_sheet(m.group("sheet")) or ""
            body = m.group("body").replace("$", "")
            self.names[key] = (sheet, body)
            span = self._range_bounds(body)
            if span and span[3] - span[1] + 1 >= CALC_NAMED_COLUMN_MIN_ROWS:
                for c in range(span[0], span[2] + 1):
                    self.named_columns.add((sheet, get_column_letter(c), span[1], span[3]))
        fam: dict[str, list[str]] = defaultdict(list)
        for key, name in self.name_case.items():
            m = re.match(r"^(.+)_([^_]+)$", name)
            if m:
                fam[m.group(1)].append(m.group(2))
        self.families = {p: sorted(s) for p, s in fam.items() if len(s) >= 2}
        for key, name in self.name_case.items():
            m = re.match(r"^(.+)_([^_]+)$", name)
            if m and m.group(1) in self.families:
                self.name_family[key] = m.group(1)

    @staticmethod
    def _range_bounds(body: str) -> tuple[int, int, int, int] | None:
        """(col1, row1, col2, row2) as ints; whole columns/rows are clamped to the sheet max."""
        body = body.replace("$", "")
        m = re.match(r"^([A-Z]{1,3})(\d+)(?::([A-Z]{1,3})(\d+))?$", body)
        if m:
            c1, r1 = column_index_from_string(m.group(1)), int(m.group(2))
            c2 = column_index_from_string(m.group(3)) if m.group(3) else c1
            r2 = int(m.group(4)) if m.group(4) else r1
            return (min(c1, c2), min(r1, r2), max(c1, c2), max(r1, r2))
        m = re.match(r"^([A-Z]{1,3}):([A-Z]{1,3})$", body)
        if m:
            return (column_index_from_string(m.group(1)), 1, column_index_from_string(m.group(2)), MAX_ROW)
        m = re.match(r"^(\d+):(\d+)$", body)
        if m:
            return (1, int(m.group(1)), MAX_COL, int(m.group(2)))
        return None

    def _scan_end(self, title: str, ws) -> int:
        """Last row this pass may touch on that sheet — the effective end the L1 recorded."""
        return sheet_scan_end(self.x, title, ws)

    def _formula(self, sheet: str, coord: str) -> str | None:
        key = (sheet, coord)
        if key not in self._formula_cache:
            ws = self.sheets.get(sheet)
            f = None
            if ws is not None:
                try:
                    f = formula_text(ws[coord])
                except Exception:
                    f = None
            self._formula_cache[key] = f
        return self._formula_cache[key]

    def _value(self, sheet: str, coord: str):
        ws = self.sheets.get(sheet)
        if ws is None:
            return None
        try:
            return ws[coord].value
        except Exception:
            return None

    def _range_is_empty(self, sheet: str, body: str) -> bool:
        key = (sheet, body)
        if key in self._empty_cache:
            return self._empty_cache[key]
        ws = self.sheets.get(sheet)
        b = self._range_bounds(body)
        empty = False
        if ws is not None and b:
            c1, r1, c2, r2 = b
            r2 = min(r2, ws.max_row or r2)
            c2 = min(c2, ws.max_column or c2)
            empty = True
            for row in ws.iter_rows(min_row=r1, max_row=r2, min_col=c1, max_col=c2):
                if any(c.value not in (None, "") for c in row):
                    empty = False
                    break
        self._empty_cache[key] = empty
        return empty

    def _range_representative(self, sheet: str, body: str) -> str | None:
        """First formula cell of a range too large to expand (scanned up to CALC_RANGE_SCAN cells)."""
        ws = self.sheets.get(sheet)
        b = self._range_bounds(body)
        if ws is None or not b:
            return None
        c1, r1, c2, r2 = b
        r2 = min(r2, ws.max_row or r2)
        c2 = min(c2, ws.max_column or c2)
        seen = 0
        for row in ws.iter_rows(min_row=r1, max_row=r2, min_col=c1, max_col=c2):
            for cell in row:
                if formula_text(cell):
                    return cell.coordinate
                seen += 1
                if seen >= CALC_RANGE_SCAN:
                    return None
        return None

    def _build_indegree(self) -> None:
        for title, ws in self.sheets.items():
            if title in self.clone_of:
                continue
            for row in ws.iter_rows(max_row=self._scan_end(title, ws)):
                for cell in row:
                    f = formula_text(cell)
                    if not f:
                        continue
                    for tsheet, body in self._direct_refs(title, f):
                        b = self._range_bounds(body)
                        if not b:
                            continue
                        c1, r1, c2, r2 = b
                        if (c2 - c1 + 1) * (r2 - r1 + 1) > CALC_RANGE_EXPAND:
                            continue
                        for c in range(c1, c2 + 1):
                            for r in range(r1, r2 + 1):
                                self.indegree[(tsheet, f"{get_column_letter(c)}{r}")] += 1

    # -------------------------------------------------------------- parsing
    def _direct_refs(self, sheet: str, formula: str, names_out: list | None = None):
        """(sheet, body) for every A1 ref and every resolvable defined name in the formula."""
        for s, body in iter_refs(formula):
            yield (s or sheet), body.replace("$", "")
        stripped = _calc_strip_strings(formula)
        for m in _CALC_NAME_RE.finditer(stripped):
            tok = m.group(1)
            key = tok.lower()
            if key in ("true", "false") or key not in self.names:
                continue
            if names_out is not None:
                names_out.append(self.name_case[key])
            target = self.names[key]
            if target is None:
                continue
            yield target

    @staticmethod
    def _kind(formula: str) -> str:
        u = _calc_strip_strings(formula).upper()
        if any(t in u for t in _CALC_AGG):
            return "aggregation"
        if any(t in u for t in _CALC_SEL):
            return "selection"
        if any(t in u for t in _CALC_LOOKUP):
            return "lookup"
        if any(t in u for t in _CALC_ROUND):
            return "rounding"
        if "_XLL." in u or _CALC_EXTERNAL_RE.search(u):
            return "feed"
        if "*" in u or "/" in u:
            return "conversion"
        return "arith"

    def _is_sequence_cell(self, sheet: str, coord: str, formula: str) -> bool:
        """A date cell, or a counter (`=B15-1`, `=+A9+1`: one reference to its own column, 1-3 rows
        away): its literal is a step of a sequence, never a price offset."""
        ws = self.sheets.get(sheet)
        if ws is None:
            return False
        try:
            cell = ws[coord]
        except Exception:
            return False
        if _CALC_DATEFMT_RE.search(str(cell.number_format or "")):
            return True
        refs = list(iter_refs(formula))
        if len(refs) != 1:
            return False
        rsheet, body = refs[0]
        if rsheet and rsheet != sheet:
            return False
        m = re.match(r"^\$?([A-Z]{1,3})\$?(\d+)$", body)
        if not m:
            return False
        return column_index_from_string(m.group(1)) == cell.column and 1 <= abs(int(m.group(2)) - cell.row) <= 3

    def _literals(self, formula: str) -> tuple[list[dict], list[dict]]:
        """(conversions, unlabelled_constants) found by shape, outside argument-taking calls."""
        text = _calc_strip_strings(formula)
        enclosing = _calc_enclosing_funcs(text)
        conversions, constants = [], []
        for m in _CALC_NUM_RE.finditer(text):
            start = m.start()
            fn = enclosing[start] if start < len(enclosing) else None
            if fn in _CALC_ARG_FUNCS:
                continue
            value = float(m.group(1))
            before = text[:start].rstrip()
            after = text[m.end():].lstrip()
            prev = before[-1] if before else ""
            nxt = after[0] if after else ""
            if (prev and prev in "*/") or nxt == "*":
                if 0 < value < 2 and value != 1:
                    conversions.append({"value": value, "op": prev or nxt})
                continue
            if prev and prev in "+-":
                sign_pos = len(before) - 1
                before_sign = before[:sign_pos].rstrip()
                if before_sign and before_sign[-1] in ",(=<>":
                    continue  # signed argument, not an offset
                if nxt and nxt in "*/":
                    continue
                if _CALC_DATE_RE.search(text):
                    continue  # calendar arithmetic is not a price offset
                constants.append({"value": -value if prev == "-" else value})
        return conversions, constants

    @staticmethod
    def _indirect_prefixes(formula: str) -> list[str]:
        out = []
        for call in find_calls(formula, "INDIRECT"):
            arg = split_args(call)[0] if "(" in call else ""
            m = STRING_SEG_RE.search(arg)
            if m:
                lit = m.group(0)[1:-1].replace('""', '"')
                out.append(lit if lit.strip() else "<dynamic>")
            else:
                out.append("<dynamic>")
        return out

    # --------------------------------------------------------------- labels
    @staticmethod
    def _is_label(v) -> bool:
        return isinstance(v, str) and not v.startswith("=") and sum(ch.isalnum() for ch in v) >= _CALC_LABEL_MIN_ALNUM

    def _label(self, ws, cell) -> str | None:
        r, c = cell.row, cell.column
        for dc in range(1, CALC_LABEL_REACH + 1):
            if c - dc < 1:
                break
            v = ws.cell(r, c - dc).value
            if self._is_label(v):
                return " ".join(v.split())
        for dr in range(1, CALC_LABEL_REACH + 1):
            if r - dr < 1:
                break
            v = ws.cell(r - dr, c).value
            if self._is_label(v):
                return " ".join(v.split())
        return None

    def _row_label(self, ws, row: int, col: int) -> str | None:
        for dc in range(1, CALC_LABEL_REACH + 1):
            if col - dc < 1:
                break
            v = ws.cell(row, col - dc).value
            if self._is_label(v):
                return " ".join(v.split())
        return None

    def _in_named_column(self, sheet: str, cell) -> bool:
        col = get_column_letter(cell.column)
        return any(s == sheet and c == col and r1 <= cell.row <= r2 for s, c, r1, r2 in self.named_columns)

    def _continues_run(self, ws, cell, f: str) -> bool:
        pat = normalize_formula(f, cell.row, cell.column)
        if cell.row > 1:
            up = formula_text(ws.cell(cell.row - 1, cell.column))
            if up and normalize_formula(up, cell.row - 1, cell.column) == pat:
                return True
        return False

    def _run_members(self, ws, cell, f: str) -> list[dict]:
        """Rows below the anchor carrying the same normalized pattern — the members of a fill-down
        run — with the row label of each (P3d-3: a labelled run IS a dimension of the output)."""
        pat = normalize_formula(f, cell.row, cell.column)
        members = [{"cell": cell.coordinate, "label": self._row_label(ws, cell.row, cell.column)}]
        r = cell.row + 1
        while r <= (ws.max_row or r):
            other = formula_text(ws.cell(r, cell.column))
            if not other or normalize_formula(other, r, cell.column) != pat:
                break
            members.append({"cell": f"{get_column_letter(cell.column)}{r}", "label": self._row_label(ws, r, cell.column)})
            r += 1
        return members

    def _group_key(self, sheet: str, f: str, cell) -> str:
        """P3d-2: normalized pattern with the name dimension and the absolute row collapsed —
        `CustosLogísticos_FUEL_Aveiro` → `CustosLogísticos_FUEL_<dim>`, `$W$21` ≈ `$W$22`."""
        norm = normalize_formula(f, cell.row, cell.column)
        norm = _CALC_ABS_ROW_RE.sub("R?C", norm)
        stripped = _calc_strip_strings(norm)

        def repl(m):
            key = m.group(1).lower()
            fam = self.name_family.get(key)
            return f"{fam}_<dim>" if fam else m.group(1)
        return f"{sheet}|" + _CALC_NAME_RE.sub(repl, stripped)

    # ------------------------------------------------------------------ walk
    def _classify_leaf(self, tsheet: str, body: str, formula_of_consumer: str) -> str:
        """P3b-3: the terminal class of a reference that was not walked further."""
        if _CALC_EXTERNAL_RE.search(formula_of_consumer):
            return "boundary"
        if tsheet not in self.sheets:
            return "boundary" if self.boundary.get("external_links", {}).get("present") else "invalid"
        b = self._range_bounds(body)
        if not b:
            return "invalid"
        c1, r1, c2, r2 = b
        size = (c2 - c1 + 1) * (r2 - r1 + 1)
        if size <= CALC_RANGE_EXPAND:
            has_formula = any(self._formula(tsheet, f"{get_column_letter(cc)}{rr}")
                              for cc in range(c1, c2 + 1) for rr in range(r1, r2 + 1))
            return "to_read" if has_formula else "typed"
        return "typed" if self._range_representative(tsheet, body) is None else "to_read"

    def _walk(self, sheet: str, coord: str) -> dict:
        steps: list[dict] = []
        seen: set[tuple[str, str]] = set()
        reaches: set[str] = set()
        conversions: list[dict] = []
        constants: list[dict] = []
        prefixes: list[tuple[str, str]] = []
        terminals: Counter = Counter()
        invalid_reasons: list[str] = []
        truncated_at: list[str] = []
        queue: list[tuple[str, str, int]] = [(sheet, coord, 0)]
        while queue:
            s, c, depth = queue.pop(0)
            if (s, c) in seen:
                continue
            if len(steps) >= self.budget["max_nodes"]:
                truncated_at.append(f"{s}!{c}")
                continue
            seen.add((s, c))
            f = self._formula(s, c)
            if not f:
                terminals["typed"] += 1
                continue
            names: list[str] = []
            refs: list[str] = []
            source_empty = False
            upper = f.upper()
            if "_XLL." in upper or _CALC_RTD_RE.search(f):
                terminals["feed"] += 1
                reaches.add("feed")
            if _CALC_EXTERNAL_RE.search(f):
                terminals["boundary"] += 1
                reaches.add("boundary:external_links")
            for tsheet, body in self._direct_refs(s, f, names):
                refs.append(f"{tsheet}!{body}")
                if tsheet != s:
                    reaches.add(tsheet)
                if tsheet not in self.sheets:
                    cls = self._classify_leaf(tsheet, body, f)
                    terminals[cls] += 1
                    if cls == "invalid":
                        invalid_reasons.append(f"{s}!{c} → {tsheet}!{body} (folha inexistente)")
                    continue
                b = self._range_bounds(body)
                if not b:
                    terminals["invalid"] += 1
                    invalid_reasons.append(f"{s}!{c} → {tsheet}!{body} (referência ilegível)")
                    continue
                c1, r1, c2, r2 = b
                if self._range_is_empty(tsheet, body):
                    source_empty = True
                size = (c2 - c1 + 1) * (r2 - r1 + 1)
                if depth >= self.budget["max_depth"]:
                    truncated_at.append(f"{tsheet}!{body}")
                    continue
                if size > CALC_RANGE_EXPAND:
                    rep = self._range_representative(tsheet, body)
                    if rep is None:
                        terminals["typed"] += 1        # a large range with no formula = input data
                    elif (tsheet, rep) not in seen:
                        queue.append((tsheet, rep, depth + 1))
                    continue
                for cc in range(c1, c2 + 1):
                    for rr in range(r1, r2 + 1):
                        tgt = f"{get_column_letter(cc)}{rr}"
                        if (tsheet, tgt) in seen:
                            continue
                        if self._formula(tsheet, tgt):
                            queue.append((tsheet, tgt, depth + 1))
                        else:
                            terminals["typed"] += 1
            for nm in names:
                reaches.add(f"name:{nm}")
                if self.names.get(nm.lower()) is None:
                    terminals["boundary"] += 1
                    reaches.add("boundary:broken_name")
            conv, const = self._literals(f)
            if const and self._is_sequence_cell(s, c, f):
                const = []
            for item in conv:
                conversions.append({"cell": c, "sheet": s, **item})
            for item in const:
                constants.append({"cell": c, "sheet": s, **item})
            step = {"sheet": s, "cell": c, "depth": depth, "formula": short(f, 160),
                    "kind": self._kind(f), "refs": sorted(set(refs)), "names": sorted(set(names))}
            if source_empty:
                step["source_empty"] = True
            pfx = self._indirect_prefixes(f)
            if pfx:
                step["to_read_prefix"] = pfx
                terminals["to_read"] += len(pfx)
                for p in pfx:
                    prefixes.append((p, f"{s}!{c}"))
                    reaches.add(f"to_read:{p}")
            steps.append(step)
        if truncated_at:
            terminals["to_read"] += len(truncated_at)   # R3: budget truncation is a TO-READ, never silence
        return {"steps": steps, "reaches": reaches, "conversions": conversions,
                "unlabelled_constants": constants, "prefixes": prefixes,
                "terminals": dict(terminals), "invalid_reasons": invalid_reasons[:6],
                "truncated_at": sorted(set(truncated_at))[:12]}

    # ------------------------------------------------------------------- run
    def run(self) -> dict:
        self._load_names()
        self._build_indegree()
        order = {ws.title: i for i, ws in enumerate(self.wb.worksheets)}
        candidates: list[tuple[int, int, int, int, str, str, str, object]] = []
        for title, ws in self.sheets.items():
            if title in self.clone_of:
                self.skipped["clone sheet"] += 1
                continue
            if ws.sheet_state != "visible":
                self.skipped["hidden sheet"] += 1
                continue
            for row in ws.iter_rows(max_row=self._scan_end(title, ws)):
                for cell in row:
                    f = formula_text(cell)
                    if not f:
                        continue
                    if self._in_named_column(title, cell):
                        self.skipped["cell inside a named input range"] += 1
                        continue
                    if self._continues_run(ws, cell, f):
                        self.skipped["fill-down continuation"] += 1
                        continue
                    label = self._label(ws, cell)
                    if not label:
                        self.skipped["formula without label"] += 1
                        continue
                    candidates.append((self.indegree[(title, cell.coordinate)], order[title],
                                       cell.row, cell.column, title, cell.coordinate, label, cell))
        candidates.sort(key=lambda t: t[:4])
        walked: list[dict] = []
        for indeg, o, r, c, title, coord, label, cell in candidates:
            f = self._formula(title, coord) or ""
            walk = self._walk(title, coord)
            if not walk["reaches"]:
                self.skipped["reaches no other sheet, name or feed"] += 1
                continue
            walked.append({"indeg": indeg, "order": o, "row": r, "col": c, "sheet": title, "anchor": coord,
                           "label": label, "walk": walk, "key": self._group_key(title, f, cell),
                           "run": self._run_members(self.sheets[title], cell, f)})
        total = len(walked)
        # terminal outputs first, then the longest chains: the price grid before the day counters
        walked.sort(key=lambda w: (w["indeg"] != 0, -len(w["walk"]["steps"]), w["order"], w["row"], w["col"]))
        covered: set[tuple[str, str]] = set()
        groups: dict[str, dict] = {}
        absorbed = 0
        for w in walked:
            if (w["sheet"], w["anchor"]) in covered:
                absorbed += 1
                self.skipped["absorbed as a step of a larger block"] += 1
                continue
            for st in w["walk"]["steps"]:
                covered.add((st["sheet"], st["cell"]))
            g = groups.get(w["key"])
            if g is None:
                groups[w["key"]] = {"lead": w, "members": []}
            else:
                g["members"].append(w)
        ordered = sorted(groups.values(), key=lambda g: (g["lead"]["indeg"] != 0, -len(g["lead"]["walk"]["steps"]),
                                                          g["lead"]["order"], g["lead"]["row"], g["lead"]["col"]))
        rendered = grouped = 0
        over_budget: list[dict] = []
        for g in ordered:
            lead, members = g["lead"], g["members"]
            if len(self.blocks) >= self.budget["max_blocks"]:
                over_budget.append(g)
                continue
            walk = lead["walk"]
            for p, where in walk["prefixes"]:
                entry = self.to_read.setdefault(p, {"prefix": p, "cells": [], "candidates": [], "reason": "INDIRECT dinâmico"})
                if where not in entry["cells"]:
                    entry["cells"].append(where)
            for t in walk["truncated_at"]:
                entry = self.to_read.setdefault("<orçamento de travessia>", {"prefix": "<orçamento de travessia>", "cells": [], "candidates": [],
                                                                            "reason": f"ramo cortado em max_depth={self.budget['max_depth']} / max_nodes={self.budget['max_nodes']}"})
                if t not in entry["cells"]:
                    entry["cells"].append(t)
            terminals = walk["terminals"]
            valid = terminals.get("invalid", 0) == 0 and all(k in TERMINAL_CLASSES or k == "invalid" for k in terminals)
            run_labels = [m["label"] for m in lead["run"] if m.get("label")]
            self.blocks.append({
                "sheet": lead["sheet"], "anchor": lead["anchor"], "label": lead["label"], "terminal": lead["indeg"] == 0,
                "steps": walk["steps"], "reaches": sorted(walk["reaches"]),
                "conversions": walk["conversions"], "unlabelled_constants": walk["unlabelled_constants"],
                "terminals": terminals, "valid": valid, "invalid_reasons": walk["invalid_reasons"],
                "truncated_at": walk["truncated_at"],
                "group_members": [{"sheet": m["sheet"], "anchor": m["anchor"], "label": m["label"]} for m in members],
                "run_members": lead["run"] if len(lead["run"]) > 1 else [],
            })
            rendered += 1
            grouped += len(members)
            if len(run_labels) >= 2 and len(set(run_labels)) >= 2:
                self.dimensions.append({"basis": "linhas rotuladas de um run", "block": None, "sheet": lead["sheet"],
                                        "anchor": lead["anchor"],
                                        "label": self._row_label(self.sheets[lead["sheet"]], lead["row"] - 1, lead["col"]),
                                        "members": run_labels, "locators": [f"{lead['sheet']}!{m['cell']}" for m in lead["run"]]})
        # P3d-1: over-budget groups never disappear — they go to TO-READ with their ranges
        to_read_budget = 0
        for g in over_budget:
            cells = [f"{g['lead']['sheet']}!{g['lead']['anchor']}"] + [f"{m['sheet']}!{m['anchor']}" for m in g["members"]]
            entry = self.to_read.setdefault("<acima do orçamento de blocos>", {"prefix": "<acima do orçamento de blocos>", "cells": [], "candidates": [],
                                                                              "reason": f"max_blocks={self.budget['max_blocks']} atingido; cada célula é um bloco por ler"})
            entry["cells"].extend(c for c in cells if c not in entry["cells"])
            to_read_budget += 1 + len(g["members"])
        assert rendered + grouped + absorbed + to_read_budget == total, (rendered, grouped, absorbed, to_read_budget, total)
        # ids in workbook order
        self.blocks.sort(key=lambda b: (order[b["sheet"]], int(re.sub(r"\D", "", b["anchor"]) or 0),
                                        column_index_from_string(re.sub(r"\d", "", b["anchor"]))))
        for i, b in enumerate(self.blocks, start=1):
            b["id"] = f"CALC-{i:03d}"
        # dimensions: INDIRECT families, clone groups, aggregation windows (P3d-3)
        for entry in self.to_read.values():
            p = entry["prefix"].lower()
            if p.startswith("<"):
                continue
            entry["candidates"] = sorted(self.name_case[k] for k in self.names if k.startswith(p))[:60]
            fams = sorted({self.name_family[k] for k in self.names if k.startswith(p) and k in self.name_family})
            for fam in fams:
                self.dimensions.append({"basis": f"intervalos nomeados `{fam}_*`", "members": self.families.get(fam, []),
                                        "locators": entry["cells"][:8], "label": None,
                                        "key_cells": sorted({r for c in entry["cells"] for r in (self._indirect_key_refs(c))})[:8]})
            entry["cells"].sort()
        for rep, cs in self.clones.items():
            self.dimensions.append({"basis": "folhas-clone (uma variante por folha)", "members": [rep] + cs,
                                    "locators": [f"{s}!A1" for s in [rep] + cs], "label": None})
        seen_windows: dict[tuple, dict] = {}
        for b in self.blocks:
            by_col: dict[tuple[str, str], list[dict]] = defaultdict(list)
            for s in b["steps"]:
                if s["kind"] == "aggregation":
                    by_col[(s["sheet"], re.sub(r"\d", "", s["cell"]))].append(s)
            for (sh, col), ss in by_col.items():
                rngs = tuple(sorted({r for s in ss for r in s["refs"] if ":" in r}))
                if len(ss) >= 2 and len(rngs) >= 2:
                    key = (sh, col, rngs)
                    if key in seen_windows:
                        seen_windows[key]["blocks"].append(b["id"])
                        continue
                    d = {"basis": "janelas de agregação (mesma coluna, intervalos distintos)", "block": b["id"], "blocks": [b["id"]],
                         "members": list(rngs), "locators": sorted({f"{s['sheet']}!{s['cell']}" for s in ss}), "label": None}
                    seen_windows[key] = d
                    self.dimensions.append(d)
        for d in self.dimensions:
            for b in self.blocks:
                if d.get("anchor") == b["anchor"] and d.get("sheet") == b["sheet"]:
                    d["block"] = b["id"]
        # coverage: blocks whose every branch ended in a terminal class other than to_read
        complete = sum(1 for b in self.blocks if b["valid"] and not b["terminals"].get("to_read"))
        with_to_read = sum(1 for b in self.blocks if b["terminals"].get("to_read"))
        invalid = sum(1 for b in self.blocks if not b["valid"])
        return {
            "tool": {"name": "xlsx_extract.py", "version": TOOL_VERSION, "pass": "calc-chain"},
            "generated_at": now_iso(),
            "budget": self.budget,
            "totals": {"candidates": total, "rendered": rendered, "grouped": grouped, "absorbed": absorbed,
                       "to_read": to_read_budget},
            "coverage": {"traced_to_terminal": complete, "with_to_read": with_to_read, "invalid": invalid,
                         "rendered": len(self.blocks)},
            "capability_boundary": self.boundary,
            "blocks": self.blocks,
            "to_read": sorted(self.to_read.values(), key=lambda e: e["prefix"]),
            "dimensions": self.dimensions,
            "clone_groups": self.clones,
            "skipped": dict(self.skipped),
        }

    def _indirect_key_refs(self, where: str) -> list[str]:
        sheet, _, coord = where.partition("!")
        f = self._formula(sheet, coord) or ""
        out = []
        for call in find_calls(f, "INDIRECT"):
            arg = split_args(call)[0] if "(" in call else ""
            for s, body in iter_refs(arg):
                out.append(f"{s or sheet}!{body.replace('$', '')}")
        return out


def render_calc_chain_md(chain: dict) -> str:
    """§4bis fragment for the process model — boundary first, then coverage, then one row per block."""
    L = ["## 4bis. Cadeia de cálculo (por saída)", ""]
    L.append(f"> Gerado por `xlsx_extract.py` v{TOOL_VERSION} (calc-chain) em {chain.get('generated_at', '')}. "
             "Anotação por **forma** (agregação / selecção / lookup / conversão / constante), nunca por "
             "significado: o que cada passo *é* para o negócio fica para §3 e para o dono.")
    L.append("")
    # --- P3b-2: boundary first
    L.append("**Fronteira de capacidade** — o que este livro calcula fora das células, declarado pela presença da "
             "parte OOXML ou da assinatura de fórmula. `presente: não` = a parte não está no pacote, nunca «o cálculo não existe».")
    L.append("")
    L.append("| mecanismo | presente | detalhe | consequência para §4bis |")
    L.append("|---|---|---|---|")
    consequence = {"power_query": "ramos que chegam a uma tabela carregada terminam em fronteira", "data_model": "medidas DAX invisíveis à cadeia",
                   "vba": "lógica em macros não lida (TO-READ manual)", "addin_functions": "terminal `feed externo`; a cadeia a jusante é válida",
                   "external_links": "terminal `fronteira`; o precedente vive noutro ficheiro", "rtd": "valor vivo, sem fórmula a ler",
                   "dynamic_names": "INDIRECT sem literal → TO-READ `<dynamic>`", "iterative": "referência circular intencional; paragem por ciclo",
                   "merged_scan_fail": "colunas dessas folhas sem estatística L1", "pivot_caches": "agregações fora da grelha",
                   "modern_functions": "LAMBDA/LET fora da bateria de replay"}
    for k, v in chain.get("capability_boundary", {}).items():
        if k.startswith("_") or not isinstance(v, dict):
            continue
        L.append(f"| `{k}` | {'**sim**' if v.get('present') else 'não'} | {v.get('detail') or '—'}{(' · `' + v['locator'] + '`') if v.get('locator') else ''} | {consequence.get(k, '—') if v.get('present') else '—'} |")
    L.append("")
    cov, tot, bud = chain.get("coverage", {}), chain.get("totals", {}), chain.get("budget", {})
    L.append(f"**Cobertura declarada** — {cov.get('traced_to_terminal', 0)} de {cov.get('rendered', 0)} blocos traçados até input terminal · "
             f"{cov.get('with_to_read', 0)} com `TO-READ` · {cov.get('invalid', 0)} inválidos. Candidatos: {tot.get('candidates', 0)} = "
             f"{tot.get('rendered', 0)} renderizados + {tot.get('grouped', 0)} agrupados + {tot.get('absorbed', 0)} absorvidos como passo + "
             f"{tot.get('to_read', 0)} TO-READ (orçamento `max_blocks={bud.get('max_blocks')}`, `max_depth={bud.get('max_depth')}`, `max_nodes={bud.get('max_nodes')}`).")
    L.append("")
    blocks = chain.get("blocks", [])
    if not blocks:
        L.append("Nenhum bloco de saída com rótulo encontrado — `calc-chain: absent`.")
        return "\n".join(L) + "\n"
    L.append("| output | pseudo-código | locators | por confirmar |")
    L.append("|---|---|---|---|")
    n_show = bud.get("max_steps_rendered", 8)
    for b in blocks:
        head = f"{b['id']} · {b['label']} (`{b['sheet']}!{b['anchor']}`)"
        if b.get("group_members"):
            names = ", ".join(f"`{m['anchor']}`" for m in b["group_members"][:3]) + (f" (+{len(b['group_members']) - 3})" if len(b["group_members"]) > 3 else "")
            head += f" (+{len(b['group_members'])} membros: {names})"
        if b.get("run_members"):
            head += f" · run de {len(b['run_members'])} linhas"
        if not b.get("terminal"):
            head += " · intermédio"
        if not b.get("valid", True):
            head += " · **invalid**: " + "; ".join(b.get("invalid_reasons", [])[:2])
        head_step = b["steps"][0] if b["steps"] else None
        ftxt = short(head_step["formula"], 64).replace("|", "\|") if head_step else ""
        kinds = Counter(s["kind"] for s in b["steps"])
        hist = " ".join(f"{k[:4]}×{v}" for k, v in sorted(kinds.items(), key=lambda kv: -kv[1]))
        empties = sum(1 for s in b["steps"] if s.get("source_empty"))
        pseudo = (f"`{ftxt}`<br>{hist}" if head_step else "—") + (f" · {empties} fonte(s) vazia(s)" if empties else "")
        keys = [f"{s['sheet']}!{s['cell']}" for s in b["steps"] if s["kind"] in ("selection", "aggregation") or s.get("to_read_prefix")]
        keys = list(dict.fromkeys(keys))[:4]
        locs = f"{b['sheet']}!{b['anchor']} → {len(b['steps'])} passos" + (f"; chave: {', '.join(keys)}" if keys else "")
        confirm = []
        for c in b.get("unlabelled_constants", []):
            confirm.append(f"`{'+' if c['value'] >= 0 else ''}{c['value']:g}` em {c['sheet']}!{c['cell']}")
        seen_conv = set()
        for c in b.get("conversions", []):
            k = (c["sheet"], c["cell"], round(c["value"], 6))
            if k not in seen_conv:
                seen_conv.add(k)
                confirm.append(f"`×{c['value']:g}` em {c['sheet']}!{c['cell']}")
        for s in b["steps"]:
            for p in s.get("to_read_prefix", []):
                confirm.append(f"`INDIRECT(\"{p}…\")` em {s['sheet']}!{s['cell']} → TO-READ")
        if b.get("truncated_at"):
            confirm.append(f"{len(b['truncated_at'])} ramo(s) cortado(s) pelo orçamento → TO-READ")
        term = " ".join(f"{k[:5]}:{v}" for k, v in sorted(b.get("terminals", {}).items()) if k != "typed") or "só valores tipados"
        L.append(f"| {head}<br>term. {term or '—'} | {pseudo} | {locs} | {' · '.join(confirm[:4]) or '—'}{' · …' if len(confirm) > 4 else ''} |")
    L.append("")
    consts = [(b, c) for b in blocks for c in b.get("unlabelled_constants", [])]
    L.append("**Constantes sem racional** — literais numéricos somados ou subtraídos numa expressão de saída, "
             "sem rótulo na folha. Não se infere significado; lista-se para perguntar.")
    L.append("")
    if consts:
        agg: dict[tuple, list[str]] = defaultdict(list)
        for b, c in consts:
            step = next((s for s in b["steps"] if s["cell"] == c["cell"] and s["sheet"] == c["sheet"]), None)
            agg[(c["value"], short(step["formula"], 70) if step else "")].append(f"{c['sheet']}!{c['cell']}")
        for (v, ftxt), where in sorted(agg.items(), key=lambda kv: (-len(kv[1]), kv[0][0])):
            L.append(f"- `{'+' if v >= 0 else ''}{v:g}` em {', '.join(where[:6])}{f' (+{len(where) - 6})' if len(where) > 6 else ''} — `{ftxt}`")
    else:
        L.append("- nenhuma")
    L.append("")
    dims = chain.get("dimensions", [])
    L.append("**Dimensões da saída** — detectadas por forma (run rotulado, família de nomes, folhas-clone, janelas de agregação). "
             "O nome de negócio de cada dimensão é da L2; aqui ficam os membros e onde se lêem.")
    L.append("")
    if dims:
        L.append("| base | membros | locators |")
        L.append("|---|---|---|")
        for d in dims:
            mem = ", ".join(f"`{m}`" for m in d.get("members", [])[:10]) + (f" (+{len(d['members']) - 10})" if len(d.get("members", [])) > 10 else "")
            locs = ", ".join(d.get("locators", [])[:3]) + (f" (+{len(d['locators']) - 3})" if len(d.get("locators", [])) > 3 else "")
            base = d["basis"] + (f" · {d['block']}" if d.get("block") else "") + (f" · chave {', '.join(d['key_cells'][:3])}" if d.get("key_cells") else "")
            L.append(f"| {base} | {mem} | {locs} |")
    else:
        L.append("- nenhuma detectada")
    L.append("")
    to_read = chain.get("to_read", [])
    L.append("**Por ler (`TO-READ`)** — o que o motor não seguiu: `INDIRECT` construído a partir de texto, ramos cortados pelo orçamento, "
             "blocos acima do tecto. Finito, com locator; nunca `Unknown` por defeito.")
    L.append("")
    if to_read:
        L.append("| motivo | células | intervalos nomeados candidatos |")
        L.append("|---|---|---|")
        for e in to_read:
            cells = ", ".join(e["cells"][:8]) + (f" (+{len(e['cells']) - 8})" if len(e["cells"]) > 8 else "")
            cands = ", ".join(f"`{n}`" for n in e.get("candidates", [])[:6]) + (f" (+{len(e['candidates']) - 6})" if len(e.get("candidates", [])) > 6 else "")
            L.append(f"| `{e['prefix']}` — {e.get('reason', '')} | {cells} | {cands or '—'} |")
    else:
        L.append("- nenhum")
    L.append("")
    if chain.get("clone_groups"):
        L.append("Folhas-clone (não recontadas): " + "; ".join(
            f"`{rep}` ← {', '.join(f'`{c}`' for c in cs)}" for rep, cs in chain["clone_groups"].items()) + ".")
        L.append("")
    return "\n".join(L) + "\n"


def calc_chain(path: str, extraction_path: str, out_json: str, log_path: str | None) -> int:
    """Standalone entry: <input.xlsx> <extraction.json> <out.calc-chain.json> (+ .md beside it)."""
    filename = os.path.basename(path)
    for p in (path, extraction_path):
        if not os.path.exists(p):
            print(f"not found: {p}", file=sys.stderr)
            return 2
    with open(extraction_path, encoding="utf-8") as fh:
        extraction = json.load(fh)
    try:
        wb_formula = load_workbook(path, data_only=False)
    except Exception as exc:
        print(f"calc-chain failed to open workbook: {exc}", file=sys.stderr)
        append_log(log_path, "L3", filename, "calc-chain: absent", short(str(exc), 120))
        return 3
    boundary = extraction.get("capability_boundary") or capability_boundary(path, wb_formula, extraction)
    chain = CalcChain(wb_formula, extraction, boundary=boundary).run()
    write_calc_chain(chain, out_json, filename, log_path)
    return 0


def write_calc_chain(chain: dict, out_json: str, filename: str, log_path: str | None) -> None:
    _write_json(out_json, chain)
    md_path = re.sub(r"\.json$", ".md", out_json)
    tmp = md_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(render_calc_chain_md(chain))
    os.replace(tmp, md_path)
    tot, cov = chain["totals"], chain["coverage"]
    present = [k for k, v in chain.get("capability_boundary", {}).items() if isinstance(v, dict) and v.get("present")]
    print(f"calc-chain: {tot['rendered']} rendered · {tot['grouped']} grouped · {tot['absorbed']} absorbed · "
          f"{tot['to_read']} to-read of {tot['candidates']} candidates -> {out_json}")
    append_log(log_path, "L3", filename, "calc-chain",
               (f"coverage {cov['traced_to_terminal']}/{cov['rendered']} · {tot['rendered']} rendered · {tot['grouped']} grouped · "
                f"{tot['absorbed']} absorbed · {tot['to_read']} to-read · budget max_blocks={chain['budget']['max_blocks']} · "
                f"boundary: {', '.join(present) or 'none'}") if chain["blocks"] else "absent (no labelled output formula)")


# --------------------------------------------------------------------- main

def main(argv=None) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(description="aisa process-capture: L1 xlsx extraction + L3 replay")
    parser.add_argument("--replay", action="store_true", help="run the L3 replay battery")
    parser.add_argument("--calc-chain", action="store_true",
                        help="reconstruct the calc chain only: <input.xlsx> <extraction.json> <out.calc-chain.json>")
    parser.add_argument("--force", action="store_true", help="ignore extraction cache")
    parser.add_argument("--log", default=None, help="append events to this capture log file")
    parser.add_argument("--version", action="version", version=f"xlsx_extract.py {TOOL_VERSION}")
    parser.add_argument("paths", nargs="+", help="extract: <input.xlsx> <out.json> | "
                                                 "replay: <input.xlsx> <extraction.json> <out.md>")
    args = parser.parse_args(argv)

    if args.calc_chain:
        if len(args.paths) != 3:
            parser.error("--calc-chain needs: <input.xlsx> <extraction.json> <out.calc-chain.json>")
        return calc_chain(args.paths[0], args.paths[1], args.paths[2], args.log)
    if args.replay:
        if len(args.paths) != 3:
            parser.error("--replay needs: <input.xlsx> <extraction.json> <out.replay.md>")
        return replay(args.paths[0], args.paths[1], args.paths[2], args.log)
    if len(args.paths) != 2:
        parser.error("extraction needs: <input.xlsx> <out.extraction.json>")
    return extract(args.paths[0], args.paths[1], args.force, args.log)


if __name__ == "__main__":
    sys.exit(main())
