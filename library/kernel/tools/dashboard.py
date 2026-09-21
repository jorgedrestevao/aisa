#!/usr/bin/env python3
"""dashboard.py -- aisa living dashboard: deterministic HTML projection of an engagement.

Kernel asset (library/kernel/tools/). Read + EXECUTED at runtime, never edited at runtime.
Dependencies: Python 3.10+ stdlib only. No LLM, no network, no writes outside
<engagement>/dashboard.html (or --out / --json).

Two consumers share one model: the HTML page below, and the `/status` view via
`--json` (see docs/STATUS_IMPROVEMENT_PLAN.md, step A0). The model carries FACTS;
every semantic verdict -- a tripwire that fired, a structural choice that closed,
whether a condition is evaluable -- belongs to the aisa-status skill, never here.

Usage:
  python library/kernel/tools/dashboard.py [--engagement <slug|path>] [--out <path>]
         [--json <path>] [--open] [--reload <sec>] [--today <ISO>] [--quiet]
         [--force] [--version]

Exit codes: 0 ok/no-op | 1 build failed (error page written) | 2 usage | 3 engagement unresolvable
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import html as _html
import http.server
import socketserver
import json
import os
import re
import sys
import tempfile
import threading
import time
import traceback
import unicodedata
import urllib.parse
import urllib.request
import webbrowser
from datetime import date, datetime
from pathlib import Path

TOOL_VERSION = "1.14.0"
ARTEFACT_ID = "aisa.dashboard"
# Schema 2 unchanged throughout: every bump only ADDS keys.
#   1.2.0  `round_delta` (P-2) · `confirmed_locator` (P-12) · `enquadramento` (P-0) ·
#          `arbiter` (P-1) · `facets.lens_producao`.
#   1.3.0  `funding_gate` (P-4, was living in the comparison script -- one rule, one
#          home); `arbiter` gains the third declaration of P-1
#          (`decisivo_sem_referente`) and `sem_citacao_m`; every deterministic block
#          now publishes its own `regex`, its `falsos_negativos` posture and what it
#          leaves to `julgamento`, so an empty list can no longer be read as approval.
#   1.4.0  fifth locator class `extraccao-directa` (states.md rule 1): a direct
#          extraction over the raw source, PERSISTED in `_capture/` under its own
#          name. Appended at the END of LOCATOR_PATTERNS (positions 5/6 are indexed).
#   1.5.0  P-13 (frente C): every label a person reads -- tabs, headings, table
#          headers, swing/custo/phase labels -- speaks the business language of
#          `glossary.md` (column *Como se diz ao utilizador*); the kernel term
#          moves to the tooltip. `round_delta.por_ronda[].novas` counts the rows
#          each round created per state (the `/status` block *desde a ultima
#          passagem*). Model shape otherwise unchanged.
#   1.8.0  `engagement.lentes_ronda_aberta` -- which Discovery lenses stamped the
#          open passagem and which are missing (`lens_wrote_round`, header match,
#          never substring). Read by `/round`, `/status`, `/frame` and the
#          lens-order guard; `/round <lens>` runs any lens in isolation.
#  1.10.0  P-26: admission of a question is a CONJUNCTION. The `M-n` waiver dies
#          here too -- it lived in this file as `if cita_m or duas: continue`, so
#          fixing the skill alone would have left the old rule reporting from the
#          motor. `arbiter.sem_declaracao` now lists a row missing ANY of the three
#          declarations; `sem_eixo` is the new third one (which of the eight
#          technical axes moves). `arbiter_declarations` takes `has_enq`: with no
#          `enquadramento.md` the `M-n` half is not owed. Reading change, not a
#          gate: the list grows on old engagements by construction, and the
#          judgement stays the arbiter's.
#  1.11.0  Owner's ruling of 2026-09-10 on declaration (i): a narrow framing must
#          not price a legitimate technical question at zero, so (i) now has TWO
#          admissible forms -- cite an `M-n`, or carry the closed-set marker
#          `TO-BE DIVERGENCE`. Verified by PRESENCE of the marker, never by whether
#          the divergence it announces is real: that reading is the arbiter's.
#          `has_enq` keeps its meaning -- with no `enquadramento.md`, (i) was never
#          owed to the motor and still is not, so no old engagement gains a finding.
SCHEMA_VERSION = 2
DEFAULT_RELOAD_SECS = 5

# ---------------------------------------------------------------- utilities


def utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except Exception:
            pass


def now_iso() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


def _read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None


def _read_json(path: Path) -> dict:
    raw = _read(path)
    if not raw:
        return {}
    # tolerate a UTF-8 BOM written by PowerShell
    for i, ch in enumerate(raw):
        if ch in "{[":
            raw = raw[i:]
            break
    try:
        out = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return out if isinstance(out, dict) else {}


def _write_text(out_path: str | Path, text: str) -> None:
    """Atomic write. The tmp name carries the pid: the hook spawns detached and two
    generators may overlap; a fixed tmp name would let one clobber the other's file."""
    out_path = str(out_path)
    parent = os.path.dirname(os.path.abspath(out_path))
    if parent:
        os.makedirs(parent, exist_ok=True)
    tmp = f"{out_path}.{os.getpid()}.tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    os.replace(tmp, out_path)


def esc(s: object) -> str:
    return _html.escape("" if s is None else str(s), quote=True)


def deaccent(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_key(s: str) -> str:
    return re.sub(r"\s+", " ", deaccent(s or "").strip().casefold())


def href_for(rel: str) -> str:
    return urllib.parse.quote(rel.replace("\\", "/"), safe="/()")


def human_size(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 * 1024:
        return f"{n / 1024:.0f} KB"
    return f"{n / (1024 * 1024):.1f} MB"


# ------------------------------------------------------- engagement resolution


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def engagements_root() -> Path:
    raw = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (repo_root() / p)
    return repo_root() / "projects"


def _activity_mtime(eng: Path) -> float:
    """Most recent touch across the engagement's live files (same idiom as
    .claude/hooks/pre-lens-order-check.py)."""
    stamps = [0.0]
    for rel in ("_state.json", "shared-understanding.md", "decisions.md", "council-log.md"):
        f = eng / rel
        if f.exists():
            try:
                stamps.append(f.stat().st_mtime)
            except OSError:
                pass
    lens_dir = eng / "lens-outputs"
    if lens_dir.is_dir():
        for f in lens_dir.glob("*.md"):
            try:
                stamps.append(f.stat().st_mtime)
            except OSError:
                pass
    return max(stamps)


def engagement_from_path(file_path: str) -> Path | None:
    """Walk up from a written file to the engagement folder holding _state.json."""
    try:
        p = Path(file_path).resolve()
    except Exception:
        return None
    for parent in [p] + list(p.parents):
        if (parent / "_state.json").is_file():
            return parent
    return None


def find_engagement(base: Path, slug: str | None = None) -> Path | None:
    if slug:
        cand = Path(slug)
        if not cand.is_absolute():
            cand = base / slug
        return cand if (cand / "_state.json").is_file() else None
    if not base.is_dir():
        return None
    engs = [d for d in base.iterdir() if d.is_dir() and (d / "_state.json").is_file()]
    if not engs:
        return None
    return max(engs, key=_activity_mtime)


# ------------------------------------------------------------- GFM table parser

SEP_RE = re.compile(r"^\s*\|?[\s:\-|]+\|?\s*$")
# A fenced block holds EXAMPLES, not data: templates and docs carry SU-shaped tables
# inside ``` fences, and a reader that continues a table across a blank line (see
# parse_tables) would otherwise absorb them as rows of the real section.
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
# A record of the Shared Understanding opens the line with a pipe. Measured over the
# 27 SUs on disk: 5224 rows, ZERO without it -- so a note that merely CONTAINS a pipe
# ("o dono decide entre A | B") is prose, and prose is not a record.
ROW_RE = re.compile(r"^\s*\|")
# The first cell of a row is an id (`U-012`, `C-022 was A-007`, `M-1`).
ROW_ID_RE = re.compile(r"^\s*\*{0,2}`?[A-Z]{1,3}-\d{1,4}\b")


def split_row(line: str) -> list[str]:
    """One GFM row -> stripped cells. Honours \\| escapes and backtick code spans.
    Never raises."""
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|") and not s.endswith("\\|"):
        s = s[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_code = False
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == "\\" and i + 1 < n and s[i + 1] == "|":
            buf.append("|")
            i += 2
            continue
        if ch == "`":
            run = 1
            while i + run < n and s[i + run] == "`":
                run += 1
            in_code = not in_code
            buf.append("`" * run)
            i += run
            continue
        if ch == "|" and not in_code:
            cells.append("".join(buf).strip())
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def fit_row(cells: list[str], n_cols: int, payload_idx: int = 2) -> tuple[list[str], bool]:
    """Reconcile a row to the header width. Surplus cells are re-joined into
    payload_idx with ' | '; deficit is right-padded. Returns (cells, malformed).

    Real case: cae-automation/shared-understanding.md U-035 carries unescaped pipes
    BETWEEN code spans -> 8 cells against a 6-column header. A naive split shifts every
    column right and `criticidade` ends up reading a swing phrase."""
    if len(cells) == n_cols:
        return cells, False
    if len(cells) < n_cols:
        return cells + [""] * (n_cols - len(cells)), True
    surplus = len(cells) - n_cols
    head = cells[:payload_idx]
    merged = " | ".join(cells[payload_idx : payload_idx + surplus + 1])
    tail = cells[payload_idx + surplus + 1 :]
    return head + [merged] + tail, True


class Table:
    __slots__ = ("heading", "headers", "rows", "line_no", "malformed_lines",
                 "gaps", "bare_lines")

    def __init__(self, heading: str, headers: list[str], line_no: int):
        self.heading = heading
        self.headers = headers
        self.rows: list[tuple[int, list[str]]] = []
        self.line_no = line_no
        self.malformed_lines: list[int] = []
        # Interruptions found INSIDE the body, as (kind, first_line, last_line) with
        # 1-based line numbers; kind is "branco" or "texto". The rows after them are
        # read (DEF-P1-04); the caller turns each gap into a diagnostic.
        self.gaps: list[tuple[str, int, int]] = []
        # Rows read WITHOUT the leading pipe: legal GFM, absent from all 27 SUs on
        # disk, and read here rather than dropped -- with a diagnostic, never silently.
        self.bare_lines: list[int] = []


def parse_tables(md: str) -> list[Table]:
    """Every GFM table in the document, tagged with the nearest preceding heading.

    Neither a blank line NOR a line of prose closes a table (DEF-P1-04). The Shared
    Understanding is a markdown table appended to by six lenses over many rounds; an
    interruption between blocks is the likeliest lapse there is, and the reader used
    to stop counting at it -- eleven open questions vanished from the dashboard, from
    the exit gate and from the epistemic health with `0 diagnostics`. The body now
    resumes at the next line that is still a row of the SAME table, and the
    interruption is recorded so the caller can emit a diagnostic.

    What is a row is decided by SHAPE, not by the mere presence of a pipe: a record
    opens the line with `|` (0 of the 5224 rows on disk do otherwise), so a note that
    happens to contain one stays prose. To resume ACROSS an interruption the evidence
    has to be stronger still -- the line opens with `|` and either carries an id in
    its first cell or matches the header width. The body ends for good at the next
    heading, at a fence, at the header of a new table and at the end of the file --
    it never absorbs another section's table nor an example inside a code block."""
    lines = md.splitlines()
    tables: list[Table] = []
    heading = ""
    fence: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        m_fence = FENCE_RE.match(line)
        if m_fence:
            marker = m_fence.group(1)
            if fence is None:
                fence = marker
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                fence = None
            i += 1
            continue
        if fence is not None:
            i += 1
            continue
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
            i += 1
            continue
        if "|" in line and i + 1 < len(lines) and SEP_RE.match(lines[i + 1]) and "|" in lines[i + 1]:
            headers = split_row(line)
            tbl = Table(heading, headers, i + 1)
            j = i + 2
            while j < len(lines):
                cur = lines[j]
                shape = _row_shape(cur, len(headers))
                if shape:
                    cells, bad = fit_row(split_row(cur), len(headers))
                    tbl.rows.append((j + 1, cells))
                    if bad:
                        tbl.malformed_lines.append(j + 1)
                    if shape == "sem-pipe":
                        tbl.bare_lines.append(j + 1)
                    j += 1
                    continue
                if _ends_body(cur):
                    break
                k = j
                while (k < len(lines) and not _row_shape(lines[k], len(headers))
                       and not _ends_body(lines[k])):
                    k += 1
                if k >= len(lines) or not _row_resumes(lines, k, len(headers)):
                    break
                kind = "branco" if all(not lines[x].strip() for x in range(j, k)) else "texto"
                tbl.gaps.append((kind, j + 1, k))
                j = k
            tables.append(tbl)
            i = j
            continue
        i += 1
    return tables


def _row_shape(line: str, n_cols: int) -> str:
    """`pipe`, `sem-pipe` or "" -- is this line a record of the table, and in what form?

    A record normally opens the line with `|`. GFM also allows `U-001 | data | ...`
    without it: legal, absent from all 27 SUs on disk, and read all the same -- but
    only on strong evidence, so that a note carrying a pipe ("o dono decide entre A |
    B") stays prose. The evidence is an id in the first cell or the header's exact
    width; the caller turns the pipeless form into a diagnostic."""
    if not line.strip() or SEP_RE.match(line):
        return ""
    if ROW_RE.match(line):
        return "pipe"
    if "|" not in line:
        return ""
    cells = split_row(line)
    first = cells[0] if cells else ""
    return "sem-pipe" if (ROW_ID_RE.match(first) or len(cells) == n_cols) else ""


def _ends_body(line: str) -> bool:
    """A heading or a fence closes the table for good -- nothing resumes across them."""
    return line.startswith("#") or bool(FENCE_RE.match(line))


def _row_resumes(lines: list[str], k: int, n_cols: int) -> bool:
    """After an interruption, does line `k` still belong to the SAME table body?

    Stronger than the in-body test on purpose: the line opens with a pipe AND either
    names an id in its first cell or matches the header width. The header+separator
    pair of a NEW table never resumes -- it starts one."""
    if not _row_shape(lines[k], n_cols):
        return False
    if (k + 1 < len(lines) and lines[k + 1].strip() and "|" in lines[k + 1]
            and SEP_RE.match(lines[k + 1])):
        return False          # header of a new table under the same heading
    cells = split_row(lines[k])
    first = cells[0] if cells else ""
    return bool(ROW_ID_RE.match(first)) or len(cells) == n_cols


# ------------------------------------------------------------------- SU model

SECTIONS = ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky")

COLUMN_ALIASES = {
    "id": "id",
    "lens": "lens",
    "claim": "claim",
    "pergunta": "claim",
    "conflito": "claim",
    "risco": "claim",
    "evidencia": "support",
    "base da assumption": "support",
    "quem responde": "support",
    "partes": "support",
    "impacto": "support",
    "mitigacao proposta": "extra",
    "criticidade": "criticidade",
    "criticidade (low/med/critical)": "criticidade",
    "verificado_em": "verificado_em",
    "validade": "validade",
    "custo": "custo",
    "swing": "swing",
    "ronda": "ronda",
}

CRIT_MAP = {
    "critical": "Critical", "critica": "Critical", "alta": "Critical", "high": "Critical",
    "med": "Med", "medium": "Med", "media": "Med",
    "low": "Low", "baixa": "Low",
}
CRIT_RANK = {"Critical": 0, "Med": 1, "Low": 2, "": 3}

RESOLVED_RE = re.compile(r"resolved\s*(?:\u2192|->)\s*(.+)$", re.I)
# P-21, the fourth sanctioned edit: a question the process does not ask leaves by this
# marker. It is not a closure -- nothing was answered -- so it counts in no round balance.
# The reason may itself carry parentheses ("substituida por U-096 (perfis ...)"), so the
# capture runs greedily to the LAST `)` of the cell -- the marker always closes the cell.
RETIRED_RE = re.compile(r"\bretirada\b\s*(?:P-\d+)?\s*\((.*)\)\s*$", re.I)
STRIKE_RES_RE = re.compile(r"~~[^~]*resolvid[oa][^~]*~~|~~[^~]+~~\s*resolvid[oa]", re.I)
WAS_RE = re.compile(r"\bwas\s+([A-Z]{1,3}-\d{2,4})")
ID_RE = re.compile(r"\b((?:C|A|U|X|CF|R|RI|D|TW|PM)-\d{2,4})\b")

DEFAULT_VALIDADE = "organizacional"
DEFAULT_CUSTO = "email"
DEFAULT_SWING = "dimensionante"


def canon_header(h: str) -> str:
    return COLUMN_ALIASES.get(norm_key(h), norm_key(h))


def parse_su_header(md: str) -> dict:
    """The leading blockquote block. Values contain colons -> split on the FIRST one."""
    out: dict[str, str] = {}
    for line in md.splitlines():
        s = line.strip()
        if not s.startswith(">"):
            if s.startswith("##"):
                break
            continue
        body = s.lstrip(">").strip()
        if ":" not in body:
            continue
        k, v = body.split(":", 1)
        out[norm_key(k)] = v.strip()
    return out


def norm_criticidade(raw: str) -> tuple[str, str]:
    txt = re.sub(r"~~[^~]*~~", " ", raw or "")
    key = norm_key(re.sub(r"[*`]", "", txt))
    for token in re.split(r"[\s/(),]+", key):
        if token in CRIT_MAP:
            return CRIT_MAP[token], (raw or "").strip()
    return "", (raw or "").strip()


def detect_resolution(cells: list[str]) -> tuple[bool, list[str]]:
    """Three conventions coexist across live engagements:
      kernel marker  '... - resolved -> C-072 + U-059'  (pricing-marinha)
      strikethrough  '~~RESOLVIDO - ver C-036~~' / '~~Alta~~ Resolvido'  (dpt-galp-jp)
      none at all    (kam-onboarding, cae-automation)"""
    last = cells[-1] if cells else ""
    m = RESOLVED_RE.search(last)
    if m:
        return True, ID_RE.findall(m.group(1))
    joined = " | ".join(cells)
    if STRIKE_RES_RE.search(joined):
        targets = ID_RE.findall(" ".join(re.findall(r"~~([^~]*)~~", joined)))
        return True, targets
    return False, []


def detect_retirement(cells: list[str]) -> tuple[bool, str]:
    """P-21 withdrawal for scope: `- retirada P-21 (<reason>)` in the last column.

    A withdrawn question stops counting as open but is NOT a closure: nothing was
    answered, so it belongs to no round balance and never to `fechadas`. The reason
    travels with the row so the page can say why the question left."""
    last = cells[-1] if cells else ""
    m = RETIRED_RE.search(last)
    return (True, (m.group(1) or "").strip()) if m else (False, "")


SWING_CLASSES = ("decisivo", "dimensionante", "cosmetico")
# `classe: frase` (states.md:128). The class is the FIRST token and one of three; the
# separator that follows it may be the canonical colon, a dash the lens wrote instead,
# or nothing at all. Anything else is not a class and is not split off (DEF-P4-01).
SWING_HEAD_RE = re.compile(
    r"^[\s*_`~]*(decisivo|dimensionante|cosmetico|cosmético)[\s*_`~]*"
    r"(?P<sep>:|\u2014|\u2013|-|$|\s)\s*(?P<rest>.*)$",
    re.I | re.S)


# The sanctioned annotations of P-26 (states.md -> "The arbiter's two effects"): the
# arbiter appends them to the cell it just reclassified. They are METADATA ABOUT the
# row -- and the first of them quotes the very declaration it says is missing ("nao
# cita `M-n` nem declara TO-BE DIVERGENCE"), so a presence match over the whole cell
# reads the audit note as the declaration (DEF-P2-01). Everything from the marker on
# is annotation; the body is what comes before.
ARB_ANNOT_RE = re.compile(
    r"\s*(?:\u2014|\u2013|--|-)?\s*"
    r"(?:reclassificad[oa]|criticidade\s+baixada)\s+P-26\s*"
    r"\(\s*[A-Z]{1,2}-\d{1,3}\s*\)\s*:",
    re.I | re.U)


def split_annotation(raw: str) -> tuple[str, str]:
    """`corpo, anotacao` -- the sanctioned P-26 suffix is cut off at its FIRST marker
    (a row reclassified in two rounds carries two). Both halves are preserved: the file
    is never touched, `swing_text` keeps the cell as written, and only the evaluation
    reads the body.

    The suffix is recognised WHOLE -- verb, `P-26`, the round in parentheses and the
    colon (states.md -> "The arbiter's two effects"). Two words were not enough: a
    sentence of the body that merely mentions the rule ("o campo reclassificado P-26
    integra o historico. Serve M-1 ...") was being cut there, and the legitimate `M-n`
    stopped counting."""
    raw = raw or ""
    m = ARB_ANNOT_RE.search(raw)
    if not m:
        return raw, ""
    return raw[:m.start()].rstrip(), raw[m.start():].strip()


def parse_swing(raw: str) -> tuple[str, str, str]:
    """`classe: frase` -> (classe, frase, forma).

    DEF-P4-01: this used to split on the FIRST colon wherever it stood and never
    checked what came before it. A cell written `decisivo - serve M-1 (...). Duas
    respostas: (a) ...` was cut at `respostas:`, so the class became the whole
    50-character prefix glued together and the phrase kept only the tail. With the
    prefix went `serve M-1` and the marker `TO-BE DIVERGENCE` -- the two forms of
    P-26's first declaration -- and 20 of 20 rows were reported as citing neither,
    with `decisivas = 0` and no diagnostic (P4 R-01).

    The class is now separated only when the cell OPENS with one of the three known
    classes. `forma` says how it was read, and the caller turns the two anomalous
    values into a diagnostic:

      `canonica`      `classe: frase` -- as states.md:128 specifies
      `separador`     class recovered, separator not the canonical colon
      `nao-lida`      the cell does not open with a class: NOTHING is split off,
                      the text is preserved whole, the class is left empty. Not
                      evaluated -- never fabricated, and never counted as proof
                      that the row cites no `M-n`.
      `vazia`         empty cell (the pre-v2.3 compatibility path, states.md:171)
    """
    raw = (raw or "").strip()
    if not raw:
        return "", "", "vazia"
    m = SWING_HEAD_RE.match(raw)
    if not m:
        return "", raw, "nao-lida"
    cls = norm_key(m.group(1)).replace(" ", "")
    rest = (m.group("rest") or "").strip()
    forma = "canonica" if m.group("sep") == ":" else "separador"
    if m.group("sep") in ("", None) and not rest:
        forma = "canonica"          # the bare class token, nothing lost
    return cls, rest, forma


def parse_su(md: str) -> tuple[dict, list[dict], dict, list[dict]]:
    """-> (header_fields, rows, sections_meta, diagnostics)"""
    header = parse_su_header(md)
    diagnostics: list[dict] = []
    rows: list[dict] = []
    sections: dict[str, dict] = {}
    seen_columns: set[str] = set()
    swing_anomalies: dict[str, list[tuple[str, int]]] = {}

    for tbl in parse_tables(md):
        state = None
        for s in SECTIONS:
            if norm_key(tbl.heading) == norm_key(s):
                state = s
                break
        if state is None:
            continue
        canon = [canon_header(h) for h in tbl.headers]
        seen_columns.update(canon)
        meta = sections.setdefault(
            state,
            {"open": 0, "resolved": 0, "retirada": 0, "columns": tbl.headers, "prefixes": []},
        )
        for line_no, cells in tbl.rows:
            rec = {k: "" for k in ("id", "lens", "claim", "support", "extra",
                                   "criticidade", "verificado_em", "validade",
                                   "custo", "swing", "ronda")}
            raw_map: dict[str, str] = {}
            for key, head, cell in zip(canon, tbl.headers, cells):
                raw_map[head] = cell
                if key in rec and not rec[key]:
                    rec[key] = cell
            if not rec["id"]:
                continue
            row_id = rec["id"].strip().strip("*` ")
            resolved, targets = detect_resolution(cells)
            retired, retired_reason = detect_retirement(cells)
            if retired:
                # Withdrawal is for open questions only: a Confirmed/Assumed/Risky row
                # asserts something and leaves by transition or not at all (states.md).
                if state in ("Unknown", "Conflicted"):
                    resolved = True
                else:
                    retired, retired_reason = False, ""
            crit, crit_raw = norm_criticidade(rec["criticidade"])
            swing_class, swing_text, swing_form = parse_swing(rec["swing"])
            if swing_form in ("separador", "nao-lida"):
                swing_anomalies.setdefault(swing_form, []).append((row_id, line_no))
            prefix = row_id.split("-", 1)[0]
            if prefix not in meta["prefixes"]:
                meta["prefixes"].append(prefix)
            meta["resolved" if resolved else "open"] += 1
            if retired:
                meta["retirada"] += 1
            rows.append({
                "id": row_id,
                "state": state,
                "lens": rec["lens"].strip(),
                "claim": rec["claim"],
                "support": rec["support"],
                "extra": rec["extra"],
                "criticidade": crit,
                "criticidade_raw": crit_raw,
                "verificado_em": rec["verificado_em"].strip(),
                "verificado_em_inferred": not rec["verificado_em"].strip(),
                "verificado_em_source": "declarado" if rec["verificado_em"].strip() else "",
                "validade": rec["validade"].strip() or DEFAULT_VALIDADE,
                "validade_inferred": not rec["validade"].strip(),
                "custo": norm_key(rec["custo"]) or DEFAULT_CUSTO,
                "custo_inferred": not rec["custo"].strip(),
                # `nao-lida` keeps the class EMPTY on purpose: not evaluated is not
                # `dimensionante`. The compatibility default belongs to the empty cell
                # alone (states.md:171).
                "swing_class": swing_class or (DEFAULT_SWING if swing_form == "vazia" else ""),
                "swing_text": swing_text,
                # DEF-P2-01: what the row itself DECLARES, without the arbiter's audit
                # note. `swing_text` stays verbatim -- the page shows the whole cell.
                "swing_body": split_annotation(swing_text)[0],
                "swing_annot": split_annotation(swing_text)[1],
                "swing_form": swing_form,
                "swing_inferred": not rec["swing"].strip(),
                "ronda": rec["ronda"].strip().split(" ")[0].strip("*` ") if rec["ronda"] else "",
                "resolved": resolved,
                "resolved_to": targets,
                "retired": retired,
                "retired_reason": retired_reason,
                "was": WAS_RE.findall(rec["claim"] or ""),
                "expired": False,
                "expires_on": "",
                "days_overdue": 0,
                "line": line_no,
                "malformed": line_no in tbl.malformed_lines,
            "duplicate_id": False,
                "raw": raw_map,
            })
        for bad in tbl.malformed_lines:
            diagnostics.append({
                "level": "warn", "where": "shared-understanding.md", "line": bad,
                "message": "linha com contagem de celulas != header ({} colunas) -- "
                           "excedente fundido na coluna de payload".format(len(tbl.headers)),
            })
        # DEF-P1-04: the rows after the interruption ARE read now; the file is still
        # anomalous and says so with section and line, instead of failing in silence.
        # A legal-but-unusual form is read, never dropped -- and it is said out loud,
        # because a SU where half the rows carry no leading pipe is a file worth
        # looking at before its numbers are trusted.
        if tbl.bare_lines:
            shown = ", ".join(str(n) for n in tbl.bare_lines[:8])
            diagnostics.append({
                "level": "warn", "where": "shared-understanding.md",
                "line": tbl.bare_lines[0],
                "message": "linha sem `|` inicial na seccao {} ({} linha{}: {}{}) -- "
                           "lida como registo pela forma (id ou largura do cabecalho); "
                           "acrescentar o `|` inicial".format(
                               state, len(tbl.bare_lines),
                               "s" if len(tbl.bare_lines) > 1 else "", shown,
                               ", ..." if len(tbl.bare_lines) > 8 else ""),
            })
        for kind, first, last in tbl.gaps:
            span = str(first) if first == last else "{}-{}".format(first, last)
            what = ("linha em branco" if kind == "branco" else "texto entre linhas")
            diagnostics.append({
                "level": "warn", "where": "shared-understanding.md", "line": first,
                "message": "{} dentro da tabela da seccao {} (linha {}) -- a tabela "
                           "continua e as linhas seguintes foram lidas; separar o {} "
                           "da tabela".format(what, state, span,
                                              "espaco" if kind == "branco" else "texto"),
            })

    for s in SECTIONS:
        sections.setdefault(
            s, {"open": 0, "resolved": 0, "retirada": 0, "columns": [], "prefixes": []}
        )

    # An id is the engagement's unit of reference: a deliverable, a decision, a
    # tripwire and every other row cite it. Two rows under one id make that citation
    # ambiguous, and the consumer used to keep whichever came last -- the review saw
    # `parsed_rows=2, drawer_entries=1, diagnostics=[]` (F01, 2026-09-08). The motor
    # cannot pick the right one and must not: it reports both and lets a human fix
    # the SU. `aisa-round` 3.6c recomputes the next free id before EACH lens so the
    # collision stops happening upstream.
    by_id: dict[str, list[dict]] = {}
    for r in rows:
        by_id.setdefault(r["id"], []).append(r)
    for row_id, dups in by_id.items():
        if len(dups) < 2:
            continue
        lines = ", ".join(str(d["line"]) for d in dups)
        states = " / ".join(dict.fromkeys(d["state"] for d in dups))
        for d in dups:
            d["duplicate_id"] = True
        diagnostics.append({
            "level": "error", "where": "shared-understanding.md", "line": dups[0]["line"],
            "message": "id duplicado: {} ({} linhas: {}) -- estados {}; uma citacao de {} "
                       "nao identifica a sua evidencia. Renomear uma das linhas "
                       "(o id novo herda `was {}`).".format(
                           row_id, len(dups), lines, states, row_id, row_id),
        })

    # DEF-P4-01. Aggregated, not one per row: a round writes the same deviation in
    # every line it produces, and a channel that prints 200 identical warnings stops
    # being read. Ids and lines stay in the message so the fix is locatable.
    SWING_DIAG = {
        "separador": ("warn", "swing fora da forma `classe: frase` (states.md:128) -- a classe "
                              "foi recuperada e o texto preservado; corrigir o separador"),
        "nao-lida": ("warn", "swing nao abre por `decisivo`/`dimensionante`/`cosmetico` -- "
                             "classificacao NAO avaliada (nao foi inventada) e o texto ficou "
                             "inteiro; as declaracoes P-26 continuam a ser lidas do texto"),
    }
    for forma, hits in swing_anomalies.items():
        level, msg = SWING_DIAG[forma]
        shown = ", ".join(rid for rid, _ln in hits[:8])
        diagnostics.append({
            "level": level, "where": "shared-understanding.md", "line": hits[0][1],
            "message": "{} ({} linha{}: {}{})".format(
                msg, len(hits), "s" if len(hits) > 1 else "", shown,
                ", ..." if len(hits) > 8 else ""),
        })

    flavour = "v2.3" if {"verificado_em", "validade", "custo", "swing"} & seen_columns else "legacy"
    return header, rows, {"sections": sections, "schema_flavour": flavour}, diagnostics


# ------------------------------------------------------------------ epistemics
# library/kernel/states.md -> "Epistemic half-lives" (normative).

HALF_LIVES = {
    "legal-regulatorio": 24,
    "plataforma-tecnica": 12,
    "organizacional": 6,
    "financeiro": 6,
    "pessoas-disponibilidade": 3,
    "volatil": 1,
}
DATE_RE = re.compile(r"(\d{4})-(\d{2})-(\d{2})")
ROUND_RE = re.compile(r"\b([RFOD]-\d{2})\b")
PHASE_ORDER = {"R": 0, "F": 1, "O": 2, "D": 3}


def load_half_lives(pack: str) -> tuple[dict, list[dict]]:
    """pack.yaml -> epistemics.half_lives_override. An indentation-based mini-reader for
    that one nested scalar map -- deliberately NOT a YAML parser."""
    out = dict(HALF_LIVES)
    diags: list[dict] = []
    if not pack:
        return out, diags
    pf = repo_root() / "library" / "packs" / pack / "pack.yaml"
    txt = _read(pf)
    if txt is None:
        diags.append({"level": "info", "where": "pack.yaml", "line": 0,
                      "message": "pack '{}' nao encontrado -- meias-vidas do kernel".format(pack)})
        return out, diags
    lines = txt.splitlines()
    in_epi = False
    in_ovr = False
    ovr_indent = 0
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip())
        stripped = line.strip()
        if indent == 0:
            in_epi = stripped.startswith("epistemics:")
            in_ovr = False
            continue
        if not in_epi:
            continue
        if stripped.startswith("half_lives_override:"):
            rest = stripped.split(":", 1)[1].strip()
            if rest and rest != "{}":
                inner = rest.strip("{} ")
                for part in inner.split(","):
                    if ":" in part:
                        k, v = part.split(":", 1)
                        try:
                            out[norm_key(k)] = int(re.sub(r"[^0-9]", "", v) or 0)
                        except ValueError:
                            pass
            in_ovr = not rest
            ovr_indent = indent
            continue
        if in_ovr:
            if indent <= ovr_indent:
                in_ovr = False
                continue
            if ":" in stripped:
                k, v = stripped.split(":", 1)
                digits = re.sub(r"[^0-9]", "", v)
                if digits:
                    out[norm_key(k)] = int(digits)
    return out, diags


def parse_round_dates(eng: Path, state: dict, su_header: dict) -> dict:
    """round-id -> (ISO date, source). Heading formats diverge across engagements:
      '## R-01 | 2026-05-28' | '## R-01 - 2026-05-29' | '## R-01 - Discovery' (no date)
      '## Framing F-01 - ...' | '## Options O-01 - ...'
    -> extract the round token and the ISO date independently, in any order."""
    out: dict[str, tuple[str, str]] = {}
    cl = _read(eng / "council-log.md") or ""
    for line in cl.splitlines():
        if not line.startswith("#"):
            continue
        rm = ROUND_RE.search(line)
        dm = DATE_RE.search(line)
        if rm and dm and rm.group(1) not in out:
            out[rm.group(1)] = (dm.group(0), "council-log.md")
    dec = _read(eng / "decisions.md") or ""
    cur_round = ""
    for line in dec.splitlines():
        s = line.strip()
        rm = re.search(r"\*\*Decided in round\*\*:\s*(\S+)", s) or \
             re.search(r"\*\*Agreed in round\*\*:\s*(\S+)", s)
        if rm:
            cur_round = rm.group(1).strip("*` ")
            continue
        if cur_round and s.startswith("- **Timestamp**"):
            dm = DATE_RE.search(s)
            if dm and cur_round not in out:
                out[cur_round] = (dm.group(0), "decisions.md")
            cur_round = ""
    fallback = ""
    for cand in (state.get("created", ""), su_header.get("iniciado", "")):
        dm = DATE_RE.search(str(cand))
        if dm:
            fallback = dm.group(0)
            break
    if fallback:
        out.setdefault("_fallback", (fallback, "_state.json/Iniciado"))
    return out


def add_months(d: date, months: int) -> date:
    total = (d.year * 12 + (d.month - 1)) + months
    y, m = divmod(total, 12)
    m += 1
    day = d.day
    while True:
        try:
            return date(y, m, day)
        except ValueError:
            day -= 1


def _as_date(s: str) -> date | None:
    m = DATE_RE.search(s or "")
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


def compute_expiry(row: dict, half_lives: dict, today: date, round_dates: dict) -> None:
    """Mutates the row. Compatibility (states.md): absent verificado_em => the round's
    date; absent validade => organizacional. Applied ON READ, never migrated."""
    if row["state"] not in ("Confirmed", "Assumed"):
        return
    d = _as_date(row["verificado_em"])
    if d is None:
        rd = round_dates.get(row["ronda"]) or round_dates.get("_fallback")
        if rd:
            row["verificado_em"] = rd[0]
            row["verificado_em_source"] = "inferido: {} {}".format(row["ronda"] or "-", rd[1])
            d = _as_date(rd[0])
    if d is None:
        return
    months = half_lives.get(norm_key(row["validade"]), half_lives["organizacional"])
    exp = add_months(d, months)
    row["expires_on"] = exp.isoformat()
    if exp < today:
        row["expired"] = True
        row["days_overdue"] = (today - exp).days


def epistemic_health(rows: list[dict]) -> dict:
    live = expired = 0
    by_validade: dict[str, dict] = {}
    for r in rows:
        if r["state"] not in ("Confirmed", "Assumed") or r["resolved"] or not r["expires_on"]:
            continue
        bucket = by_validade.setdefault(r["validade"], {"live": 0, "expired": 0})
        if r["expired"]:
            expired += 1
            bucket["expired"] += 1
        else:
            live += 1
            bucket["live"] += 1
    total = live + expired
    return {
        "pct": round(live * 100 / total) if total else 100,
        "live": live, "expired": expired, "total": total, "by_validade": by_validade,
    }


def rewrite_question(row: dict) -> str:
    claim = re.sub(r"\s+", " ", row["claim"]).strip()
    return "Ainda e verdade que {}? Verificado pela ultima vez em {}.".format(
        claim, row["verificado_em"] or "?")


def revalidation_list(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        if r["state"] in ("Confirmed", "Assumed") and not r["resolved"] and r["expired"]:
            out.append({
                "id": r["id"], "state": r["state"], "lens": r["lens"], "claim": r["claim"],
                "validade": r["validade"], "verificado_em": r["verificado_em"],
                "verificado_em_source": r["verificado_em_source"],
                "expires_on": r["expires_on"], "days_overdue": r["days_overdue"],
                "question": rewrite_question(r),
                "cmd": "/answer --revalidate {}".format(r["id"]),
            })
    out.sort(key=lambda x: (-x["days_overdue"], x["id"]))
    return out


# -------------------------------------------------- computed views (aisa-status)

SWING_ORDER = {"decisivo": 0, "dimensionante": 1, "cosmetico": 2}
CANAL = {"email", "documento", "spike"}


def _agenda_key(r: dict) -> tuple:
    return (SWING_ORDER.get(r["swing_class"], 1), CRIT_RANK.get(r["criticidade"], 3), r["id"])


def meeting_agenda(rows: list[dict]) -> dict:
    reuniao, canal, nao = [], [], []
    for r in rows:
        if r["state"] != "Unknown" or r["resolved"]:
            continue
        item = {
            "id": r["id"], "lens": r["lens"], "pergunta": r["claim"],
            "quem": r["support"], "criticidade": r["criticidade"],
            "criticidade_raw": r["criticidade_raw"],
            "custo": r["custo"], "custo_inferred": r["custo_inferred"],
            "swing_class": r["swing_class"], "swing_text": r["swing_text"],
            "swing_inferred": r["swing_inferred"],
        }
        if r["swing_class"] == "cosmetico":
            nao.append(item)
        elif r["custo"] == "reuniao":
            reuniao.append(item)
        elif r["custo"] in CANAL:
            canal.append(item)
        else:
            canal.append(item)
    for bucket in (reuniao, canal, nao):
        bucket.sort(key=_agenda_key)
    return {"reuniao": reuniao, "outro_canal": canal, "nao_gastar": nao}


def critical_open(rows: list[dict]) -> list[dict]:
    out = [
        {"id": r["id"], "state": r["state"], "lens": r["lens"], "claim": r["claim"],
         "criticidade": r["criticidade"], "criticidade_raw": r["criticidade_raw"]}
        for r in rows
        if r["state"] in ("Unknown", "Conflicted") and not r["resolved"]
        and r["criticidade"] == "Critical"
    ]
    out.sort(key=lambda x: (x["state"], x["id"]))
    return out


# ------------------------------------------------ Confirmed locator (P-12)
# One implementation, two consumers: the `sem locator` facet below and the
# .claude/hooks/su-confirmed-guard.py hook, which imports this module. The regex
# lives here and nowhere else.
#
# The five classes are `library/kernel/states.md` -> *Confirmed threshold* rule 1
# (the fifth -- a persisted direct extraction -- was added after the R-05 validation).
# Each class accepts the canonical form AND the capture-lite form the same rule
# names, because that is what live engagements write (`kickoff · [00:52:17]`,
# `'Outputs BIOS'!M` -- one workbook family, sheet!cell without the file prefix).
# This is a PRESENCE check, never a judgement: it says whether an anchor is there
# and whether its target exists, never whether the claim matches the evidence.

_SHEET = r"(?:'[^'|]{1,60}'|[0-9A-Za-z_À-ɏ][0-9A-Za-z_ À-ɏ]{0,40})"
_FILE = r"[^\s`|]+"

LOCATOR_PATTERNS: tuple[tuple[str, "re.Pattern[str]"], ...] = (
    # 1a. workbook cell / column -- with the file prefix, or bare sheet!cell
    ("xlsx-celula", re.compile(
        r"\.(?:xlsx|xlsm)#[^\s`|!]+!\$?[A-Z]{1,3}\$?\d*"
        r"|" + _SHEET + r"!\$?[A-Z]{1,3}\$?\d*(?![0-9A-Za-z])", re.U)),
    # 1b. extractor output -- counts and structure
    ("extraction-json", re.compile(r"\.extraction\.json#\S", re.U)),
    ("replay", re.compile(r"\.replay\.md#\d+|\breplay\s*#\s*\d+", re.U)),
    # 2. transcript passage
    ("transcricao", re.compile(
        r"\.vtt#\s*\[?\d{1,2}:\d{2}:\d{2}"
        r"|[·•]\s*`?\[\d{1,2}:\d{2}:\d{2}\]", re.U)),
    # 3. document passage
    ("documento", re.compile(
        r"\.(?:docx|pdf)#\s*¶?\s*\d+"
        r"|[·•]\s*§[^|]{0,80}¶\s*\d+"
        r"|[·•]\s*p\.\s*\d+", re.U)),
    # 4. dated owner declaration
    ("answers", re.compile(r"answers\.md#([0-9A-Za-zÀ-ɏ._-]+)", re.U)),
    ("enquadramento", re.compile(r"enquadramento\.md#(M-\d+)", re.U)),
    # 5. direct extraction over the raw source, PERSISTED under its own name in
    #    `_capture/` (states.md rule 1, fifth class). `<source>.<ext>.<what>.(json|md)`
    #    where <what> is not a pipeline artefact -- those are class 1.
    ("extraccao-directa", re.compile(
        r"[^\s`|]+\.(?:xlsx|xlsm|vtt|docx|pdf)\."
        r"(?!extraction\.json|replay\.md|text\.md)[A-Za-z0-9_-]+\.(?:json|md)(?:#\S+)?",
        re.I | re.U)),
    # 6. what the FRAMEWORK itself writes at the start of the engagement (DEF-P1-01).
    #    `aisa-start` opens `enquadramento.md` with the themes T1..T7 and `context.json`
    #    with the requester, the literal request and the funding gate. A Confirmed row
    #    resting on the owner's declaration cites exactly those anchors -- and they used
    #    to match no class at all, so the guard reported "sem locator" on evidence the
    #    framework had produced itself. Appended at the END: positions 5/6 of this tuple
    #    were indexed by the resolver (they are looked up by name now, and a test holds
    #    both ends of that).
    ("enquadramento-tema", re.compile(r"enquadramento\.md#(T\d+)\b", re.U)),
    ("contexto", re.compile(r"context\.json[.#]([A-Za-z_][A-Za-z0-9_]*"
                            r"(?:\.[A-Za-z_][A-Za-z0-9_]*)*)", re.U)),
)

LOCATOR_BY_NAME = {name: rx for name, rx in LOCATOR_PATTERNS}

LOCATOR_EXCEPTION = re.compile(r"context\.json[.#]literal_request", re.U)

NAMED_FILE_RE = re.compile(
    r"[`'\"]?([^\s`'\"|]+\.(?:xlsx|xlsm|vtt|docx|pdf)"
    r"(?:\.(?:extraction\.json|replay\.md|text\.md|[A-Za-z0-9_-]+\.(?:json|md)))?)",
    re.I | re.U)


def locator_classes(text: str) -> list[str]:
    """The locator classes present in an evidence cell. Presence only."""
    txt = text or ""
    return [name for name, rx in LOCATOR_PATTERNS if rx.search(txt)]


def evidence_targets(eng: Path) -> dict:
    """What the engagement actually holds, so a locator can be resolved and not just
    matched. `inputs/` and `_capture/` by file name; `answers.md` by section anchor
    (states.md rule 1: first segment of the heading before ' - ', spaces as hyphens);
    `enquadramento.md` by `M-n`."""
    names: set[str] = set()
    for sub in ("inputs", "_capture"):
        d = eng / sub
        if not d.is_dir():
            continue
        for p in d.rglob("*"):
            if p.is_file():
                names.add(p.name.lower())
                names.add(deaccent(p.name).lower())
    anchors: set[str] = set()
    for line in (_read(eng / "answers.md") or "").splitlines():
        if not line.startswith("#"):
            continue
        head = line.lstrip("#").strip().strip("*` ")
        head = re.split(r"\s+—\s+|\s+--\s+", head)[0].strip()
        if head:
            a = head.replace(" ", "-")
            anchors.add(a.lower())
            anchors.add(deaccent(a).lower())
    enq = _read(eng / "enquadramento.md") or ""
    # The theme anchors `aisa-start` writes: `## T1 · actors` answers both `#T1` and
    # the full slug. Same rule as answers.md -- the first segment of the heading.
    enq_anchors: set[str] = set()
    for line in enq.splitlines():
        if not line.startswith("#"):
            continue
        head = line.lstrip("#").strip().strip("*` ")
        first = re.split(r"\s+[·•—-]\s+|\s+--\s+", head)[0].strip()
        for form in (head, first):
            if form:
                a = form.replace(" ", "-")
                enq_anchors.add(a.lower())
                enq_anchors.add(deaccent(a).lower())
    ctx_path = eng / "context.json"
    ctx_raw = _read(ctx_path)
    ctx = _read_json(ctx_path)
    return {
        "files": names,
        "answers_anchors": anchors,
        "has_answers": (eng / "answers.md").is_file(),
        "enq_ids": set(re.findall(r"\bM-\d+\b", enq)),
        "enq_anchors": enq_anchors,
        "has_enq": (eng / "enquadramento.md").is_file(),
        "context": ctx,
        "has_context": ctx_path.is_file(),
        # a file that exists and does not parse is NOT the same as a missing one: the
        # locator points somewhere real that nothing can be read from.
        "context_broken": bool(ctx_raw) and not ctx,
        "has_workbook": any(n.endswith((".xlsx", ".xlsm")) or ".extraction.json" in n
                            or ".replay.md" in n for n in names),
        "has_transcript": any(".vtt" in n for n in names),
        "has_document": any(n.endswith((".docx", ".pdf")) for n in names),
    }


def _dig(data: dict, dotted: str) -> tuple[object, bool]:
    """`a.b.c` sobre um dicionario -> (valor, existe). Nunca levanta."""
    cur: object = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None, False
        cur = cur[part]
    return cur, True


def locator_target_gaps(text: str, classes: list[str], tgt: dict) -> list[str]:
    """Why a present locator does not resolve. Empty list = it resolves.

    A file name is only checked when it belongs to a locator's OWN span (extended
    left to the token boundary, because the name sits immediately before the `#`).
    A path quoted inside prose -- an `external_links` target, a system someone
    named -- is evidence content, not a locator, and is never checked. The lite
    forms name no file, so their target is checked by class.
    """
    txt = text or ""
    gaps: list[str] = []

    def add(g: str) -> None:
        if g not in gaps:
            gaps.append(g)

    for name, rx in LOCATOR_PATTERNS:
        if name in ("answers", "enquadramento", "enquadramento-tema", "contexto"):
            continue
        for m in rx.finditer(txt):
            start = m.start()
            while start > 0 and txt[start - 1] not in " `\"'|(\t\n":
                start -= 1
            fm = NAMED_FILE_RE.search(txt[start:m.end()])
            if not fm:
                continue
            nm = fm.group(1).lower()
            nmd = deaccent(fm.group(1)).lower()
            if any(f.endswith(nm) or f.endswith(nmd) for f in tgt["files"]):
                continue
            add("ficheiro nao esta em inputs/ nem _capture/: {}".format(fm.group(1)))

    for m in LOCATOR_BY_NAME["answers"].finditer(txt):      # answers.md#<seccao>
        a = m.group(1)
        if not tgt["has_answers"]:
            add("answers.md nao existe")
        elif a.lower() not in tgt["answers_anchors"] and \
                deaccent(a).lower() not in tgt["answers_anchors"]:
            add("answers.md sem a seccao #{}".format(a))
    for m in LOCATOR_BY_NAME["enquadramento"].finditer(txt):    # enquadramento.md#M-n
        if not tgt["has_enq"]:
            add("enquadramento.md nao existe")
        elif m.group(1) not in tgt["enq_ids"]:
            add("enquadramento.md sem {}".format(m.group(1)))
    # DEF-P1-01: the theme anchors of the enquadramento, and the startup fields of
    # context.json. Recognised as locators -- and RESOLVED, not waved through: the
    # section has to be in the file and the key has to be in the JSON.
    for m in LOCATOR_BY_NAME["enquadramento-tema"].finditer(txt):
        a = m.group(1)
        # O enquadramento tem SETE temas (states.md / aisa-start). `#T8` nao e um tema
        # -- e isso nao depende de haver, ou nao, um cabecalho com esse nome no
        # ficheiro: um cabecalho fora do contrato nao cria um tema novo.
        num = int(a[1:]) if a[1:].isdigit() else 0
        if not 1 <= num <= 7:
            add("enquadramento.md: {} fora dos sete temas (T1..T7)".format(a))
            continue
        if not tgt["has_enq"]:
            add("enquadramento.md nao existe")
        elif a.lower() not in tgt.get("enq_anchors", set()):
            add("enquadramento.md sem a seccao #{}".format(a))
    for m in LOCATOR_BY_NAME["contexto"].finditer(txt):
        key = m.group(1)
        if not tgt.get("has_context"):
            add("context.json nao existe")
            continue
        if tgt.get("context_broken"):
            add("context.json nao e JSON valido")
            continue
        val, found = _dig(tgt.get("context") or {}, key)
        if not found:
            add("context.json sem a chave {}".format(key))
        elif val is None or (isinstance(val, str) and not val.strip()) \
                or (isinstance(val, (list, dict, tuple)) and len(val) == 0):
            # `false` and `0` ARE values -- a funding gate that is closed is a fact.
            # An empty string is not: the locator points at a key that says nothing.
            add("context.json#{} esta vazio".format(key))

    if "xlsx-celula" in classes and not tgt["has_workbook"]:
        add("celula citada e o engagement nao tem folha de calculo")
    if "transcricao" in classes and not tgt["has_transcript"]:
        add("timestamp citado e o engagement nao tem transcricao")
    if "documento" in classes and not tgt["has_document"]:
        add("passagem citada e o engagement nao tem documento")
    return gaps


def audit_confirmed_locators(rows: list[dict], eng: Path,
                             only_ids: set[str] | None = None) -> dict:
    """P-12 deterministic half. Open `Confirmed` rows without a resolvable locator.
    `only_ids` narrows it to the rows a single write touched (the hook's use)."""
    tgt = evidence_targets(eng)
    sem: list[dict] = []
    alvo: list[dict] = []
    excepcao: list[str] = []
    por_classe: dict[str, int] = {}
    total = ok = 0
    for r in rows:
        if r["state"] != "Confirmed" or r["resolved"]:
            continue
        if only_ids is not None and r["id"] not in only_ids:
            continue
        total += 1
        text = " ".join((r.get("support") or "", r.get("extra") or ""))
        classes = locator_classes(text)
        if not classes:
            if LOCATOR_EXCEPTION.search(text):
                excepcao.append(r["id"])
                ok += 1
                continue
            sem.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"],
                        "motivo": "evidencia sem locator das cinco classes"})
            continue
        for c in classes:
            por_classe[c] = por_classe.get(c, 0) + 1
        gaps = locator_target_gaps(text, classes, tgt)
        if gaps:
            alvo.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"],
                         "classes": classes, "motivo": "; ".join(gaps)})
        else:
            ok += 1
    return {
        "total": total,
        "com_locator": ok,
        "sem_locator": sem,
        "alvo_ausente": alvo,
        "excepcao_literal_request": excepcao,
        "por_classe": por_classe,
        "ids": [x["id"] for x in sem] + [x["id"] for x in alvo],
        "regex": {name: rx.pattern for name, rx in LOCATOR_PATTERNS},
        "regex_excepcao": LOCATOR_EXCEPTION.pattern,
        "falsos_negativos": ("ACEITES: uma evidencia que aponte a fonte numa forma que "
                             "estes regex nao conhecem passa por boa. Falsos POSITIVOS "
                             "nao sao aceites -- o alvo so e verificado quando o nome do "
                             "ficheiro pertence ao span do proprio locator"),
        "julgamento": ("o motor verifica PRESENCA de locator e EXISTENCIA do alvo. Se a "
                       "afirmacao diz mais do que a evidencia -- a regra 2 do limiar -- e "
                       "julgamento da segunda leitura do arbitro (aisa-round step 5f) e das "
                       "Hard rules das lentes. Lista vazia significa 'toda a evidencia "
                       "aponta a algo que existe', nunca 'os factos estao certos'"),
        "calibracao": list(CALIBRACAO),
    }


ENQ_ROUND = "R-00"
ENQ_LENS = "enquadramento"


# --------------------------------------------------- round arbiter (P-1)
# Presence check ONLY. It never reclassifies, never rewrites a question, never
# judges materiality: it lists the open `Unknown` rows that carry NO declaration
# of why they exist. The arbiter (aisa-round step 5f) decides what to do with the
# list; the lens wrote the row. False negatives are accepted by design -- a row
# that declares its divergence in words this regex does not know is left alone.

# Engagements de calibração: todo o regex determinístico desta secção desenvolve-se
# contra estes três -- dois vivos sob a regra e um anterior a ela -- e nunca só contra o
# template. Foi a ausência desta disciplina que produziu os quatro defeitos que a
# validação de R-05 apanhou (step-9c §5.2.1).
CALIBRACAO = ("pricing-marinha-pilot-3", "dpt-galp-jp", "cae-automation")

ARB_M_RE = re.compile(r"\bM-\d+\b")
# P-1, terceira declaração: um `decisivo` nomeia o referente que a resposta elimina ou
# mantém vivo. Vivia no script de comparação -- duas casas para a mesma regra divergem.
ARB_REF_RE = re.compile(
    r"\bO-\d{2,4}\b|\bframe\b|\bbranch\b|\bramo\b|\bop[çc][ãa]o\b"
    r"|\bdo nothing\b|\bn[ãa]o fazer\b|\belimina\b|\bmant[ée]m vivo\b",
    re.I | re.U)
# P-4: com `funding_gate = false` a lente financeira não constrói envelope. Idem, vinha
# do script.
#
# DEF-P3-01: `tecto`, `limiar` e `envelope` sao polissemicos. Um TECTO DE VOLUME
# (quantos pedidos por mes a solucao aguenta) nao e um TECTO DE VERBA; um LIMIAR DE
# TOLERANCIA a erros nao e um limiar de aprovacao orcamental; um ENVELOPE DE TEMPO nao
# e um envelope de orcamento. A verificacao assinalava os tres pares por igual. Os
# termos inequivocos continuam a valer sozinhos; os polissemicos passam a exigir um
# qualificador financeiro a distancia curta -- e `custo` no eixo do swing continua a
# nao ser prova de nada, porque o eixo diz o que MUDA, nao de que a pergunta trata.
# `aprovacao` NAO e qualificador: aprova-se conteudo, classificacao e acesso tanto
# como verba. `aprovacao orcamental` continua a contar -- pelo `orcament`, que e
# inequivoco, nao pela aprovacao.
FUNDING_TERM_RE = re.compile(
    r"\borcament|\bcapex\b|\bopex\b|\bimputa|\bchargeback\b|\bpayback\b"
    r"|\broi\b|\bfunding\b|\bverba\b|\bcabimento\b|\bdotacao\b", re.I)
FUNDING_POLY_RE = re.compile(
    r"\b(te[ct]to|limiar|envelope|plafond)\b[^.;|]{0,40}?"
    r"\b(verba|orcament\w*|custo\w*|gasto\w*|despesa\w*|investiment\w*"
    r"|financeir\w*|monetari\w*|euros?|eur|budget|capex|opex)\b", re.I)
# Publicado no resultado para se poder contestar o que foi assinalado.
FUNDING_RE = re.compile(
    FUNDING_TERM_RE.pattern + r"|(?:" + FUNDING_POLY_RE.pattern + r")", re.I)


def funding_term(text: str) -> str | None:
    """O termo financeiro presente, ou None. Compara sem acentos e devolve o trecho tal
    como esta escrito -- e o que vai no resultado para alguem contestar."""
    raw = text or ""
    flat = deaccent(raw)
    m = FUNDING_TERM_RE.search(flat) or FUNDING_POLY_RE.search(flat)
    if not m:
        return None
    # deaccent preserva o comprimento nos acentos latinos, logo o span mapeia de volta
    return raw[m.start():m.end()] if len(flat) == len(raw) else m.group(0)
# P-26, terceira declaracao: qual dos OITO eixos tecnicos muda com cada resposta.
# Generoso por desenho -- aqui um falso positivo seria assinalar uma linha que declara
# o eixo por palavras que o regex nao conhece, e essa e a troca que este ficheiro nao
# aceita (ver `falsos_negativos`). Le-se so a frase do `swing`: e ai que a regra poe a
# declaracao.
ARB_AXIS_RE = re.compile(
    r"\btecnologia\b|\bplataforma\b|\bproduto\b"                     # tecnologia
    r"|\bpadr[ãa]o\b|\barquitec?tura\b|\bdesenho da solu"           # padrão arquitetural
    r"|\bcomponente|\bconector|\bm[óo]dulo|\bintegra[çc][ãa]o\b"      # componentes
    r"|\bmodelo de dados\b|\bentidade|\besquema\b|\bschema\b|\btabela"
    r"|\bcampo|\bchave\b"                                            # modelo de dados
    r"|\bpermiss|\bRBAC\b|\bacesso|\bautoriza|\bperfil"                # imposição de
    r"|\bimposi[çc][ãa]o\b|\bpartilha\b"                             # permissões
    r"|\besfor[çc]o|\bdimension|\bordem de grandeza\b|\btamanho\b"     # esforço de
    r"|\b[âa]mbito\b"                                                # alto nível
    r"|\bcusto|\blicen[çc]|\bpre[çc]o|\bor[çc]ament"              # custo
    r"|\brisco",                                                      # risco técnico
    re.I | re.U)
# ">= 2 named answers" -- the three shapes the swing phrase uses in live SUs
ARB_ALT_RE = re.compile(
    r"\(\s*a\s*\)[^|]{2,400}?\(\s*b\s*\)"       # "(a) ... (b)" -- what live SUs write
    r"|\bou\b"                                  # "A ou B"
    r"|\bvs\.?\b|\bversus\b"                    # "A vs B"
    # "se ..., se ...": a janela era `[^|;]{2,80}` -- um ponto-e-virgula entre os dois
    # ramos, ou um ramo com mais de 80 caracteres, dava FALSO POSITIVO. Aconteceu 7 vezes
    # em pricing-bunkers R-01 (council-log) e voltou em pilot-3 R-05 com P-26, onde a
    # conjuncao o torna consequente: sob a regra antiga a linha passava por citar `M-n`.
    # A janela larga alinha com a do "(a) ... (b)" e troca falsos positivos por falsos
    # negativos -- a troca que este ficheiro aceita.
    r"|\bse\b[^|]{2,400}?\bse\b"
    r"|\bcontra\b"
    r"|\bentre\b[^|;]{2,60}?\be\b",
    re.I | re.U | re.S)


# P-26 declaracao (i), segunda forma admissivel (veredicto do dono, 2026-09-10).
# Marcador de CONJUNTO FECHADO e NAO TRADUZIDO, pela mesma razao que os quatro de G1:
# a SU sai na lingua do pacote e uma frase traduzida faz o teste passar em falso.
# Presenca, nunca verdade -- o que o marcador anuncia le-se, nao se verifica aqui.
ARB_TOBE_RE = re.compile(r"TO-BE DIVERGENCE")

# P-26, segunda declaracao: as formas do portugues real que ARB_ALT_RE nao cobria.
#
# DEF-P1-03: as 8 perguntas de P1 R-01 nomeiam duas respostas em ORACOES PARALELAS
# separadas por ponto-e-virgula -- "traducao implica conteudo com variantes de lingua;
# percurso proprio implica conteudo versionado por geografia" -- e as 8 foram
# assinaladas como nao nomeando duas. A regra universal `tem ; => duas alternativas`
# nao serve: o mesmo ponto-e-virgula separa, noutras linhas, duas consequencias da
# MESMA resposta ("acrescenta relogio, alerta e medicao; move `modelo de dados`"), e
# ja tinha dado 7 falsos positivos em pricing-bunkers R-01.
#
# O que se reconhece e a ESTRUTURA, nao o sentido: dois ramos, cada um com o seu
# antecedente. Um ramo vale quando abre por uma condicao (`sem ...`, `se ...`, `com
# ...`, `caso ...`, `quando ...`) ou quando nomeia um sujeito ANTES do verbo de
# consequencia. "move X" nao tem sujeito antes do verbo e nao e um ramo -- e a
# consequencia da linha inteira.
ARB_CONSEQ_RE = re.compile(
    r"\b(implica|implicam|exige|exigem|obriga|obrigam|dispensa|dispensam"
    r"|elimina|eliminam|permite|permitem|custa|custam|traz|trazem"
    r"|mant[ée]m|acrescenta|acrescentam|basta|bastam|cabe|cabem"
    r"|reduz|reduzem|aumenta|aumentam|evita|evitam|for[çc]a|for[çc]am"
    r"|deixa de|passa a|passam a|chega|chegam)\b", re.I | re.U)
# A condicao abre o RAMO, e o ramo pode vir depois do preambulo `serve M-n -`: o
# marcador vale no inicio do segmento ou logo a seguir a um travessao/dois-pontos.
ARB_COND_RE = re.compile(
    r"(?:^|[\u2014\u2013:-]\s*)\b(sem|se|com|caso|quando|havendo|existindo)\b",
    re.I | re.U)
# O caso comparativo (U-021 de P1): "sete modulos ... custam varias vezes o que custa
# um percurso com a Fase 2". Compara dois ambitos, mas nomear duas COISAS comparadas
# nao e o mesmo que nomear duas RESPOSTAS -- e as duas respostas de U-021 estao na
# pergunta, nao no swing. Forma ambigua: declara-se NAO AVALIADA, nunca em falta.
ARB_COMPAR_RE = re.compile(
    r"\b(v[\u00e1a]rias vezes|o dobro|o triplo|metade|muito mais|muito menos)\b"
    r"[^|;]{0,60}?\b(o que|do que|que custa|que custam)\b"
    r"|\b(mais|menos|maior|menor)\b[^|;]{0,60}?\bdo que\b",
    re.I | re.U)


# Palavras que nao distinguem um ramo do outro: artigos, demonstrativos e
# preposicoes de ligacao. Os QUALIFICADORES ficam de fora desta lista de proposito,
# porque sao eles que separam os ramos: `nao` ("mostrar" contra "nao mostrar"),
# `com`/`sem` ("com validacao" contra "sem validacao"), `mais`/`menos`, `so`,
# `apenas`, `outro`, `cada`, `todo`. Foi assim que "com validacao exige aprovacao;
# sem validacao permite publicacao imediata" aparecia como um so antecedente.
ARB_STOP = frozenset("""
a o as os um uma uns umas de do da dos das em no na nos nas ao aos que e ou por para
ja isto isso aquilo este esta esse essa aquele aquela seu sua seus suas lhe lhes
serve entao ainda
""".split())


def _antecedente(seg: str) -> str | None:
    """O que o ramo supoe, antes da consequencia. `None` = nao se identifica."""
    seg = seg.strip()
    if not seg:
        return None
    m_cond = ARB_COND_RE.search(seg)
    m_verb = ARB_CONSEQ_RE.search(seg)
    if m_cond and (not m_verb or m_cond.start() <= m_verb.start()):
        # `sem essa lista o modulo 7 ...` -> da condicao ate a virgula / ao verbo
        resto = seg[m_cond.start():]
        corte = m_verb.start() - m_cond.start() if m_verb else len(resto)
        pedaco = resto[:corte]
        return pedaco.split(",")[0]
    if m_verb:
        return seg[:m_verb.start()]
    return None


def _chave(texto: str) -> frozenset:
    """As palavras com que o antecedente se distingue de outro."""
    limpo = re.sub(r"`[^`]*`", " ", texto or "")
    limpo = re.sub(r"\bM-\d+\b", " ", limpo)
    limpo = re.sub(r"[^\w\s]", " ", deaccent(limpo).lower(), flags=re.U)
    return frozenset(w for w in limpo.split() if w and w not in ARB_STOP and len(w) > 1)


def _ramos_distintos(segs: list[str]) -> str:
    """`sim` | `nao` | `nao-avaliado` -- ha dois ramos com antecedentes DIFERENTES?

    DEF-P1-03, segunda volta: "a automatizacao reduz erros; a automatizacao aumenta a
    rastreabilidade" tem dois verbos de consequencia e um so antecedente -- sao duas
    consequencias da MESMA resposta. Dois ramos so contam como duas respostas quando
    cada um traz pelo menos uma palavra que o outro nao tem ("confirmacao em
    mobilidade" contra "confirmacao ao computador"). Onde um dos lados nao acrescenta
    nada ao outro, o motor nao decide: `nao-avaliado`."""
    chaves = []
    for seg in segs:
        ant = _antecedente(seg)
        if ant is None:
            continue
        k = _chave(ant)
        if k:
            chaves.append(k)
    if len(chaves) < 2:
        return "nao"
    for i in range(len(chaves)):
        for j in range(i + 1, len(chaves)):
            a, b = chaves[i], chaves[j]
            if a == b:
                continue                      # mesmo antecedente: mesma resposta
            if (a - b) and (b - a):
                return "sim"                  # cada ramo traz o que o outro nao tem
    if any(chaves[0] != k for k in chaves[1:]):
        return "nao-avaliado"                 # diferentes, mas um contem o outro
    return "nao"


def declara_alternativas(texto: str) -> str:
    """`sim` | `nao` | `nao-avaliado` -- a linha nomeia >= 2 respostas?

    `nao-avaliado` existe porque a alternativa honesta a um falso positivo nao e um
    falso negativo: onde a forma e ambigua o motor diz que nao avaliou, em vez de
    afirmar que a declaracao falta (plano R4)."""
    texto = texto or ""
    if ARB_ALT_RE.search(texto):
        return "sim"
    ramos = [s for s in re.split(r";", texto) if s.strip()]
    if len(ramos) >= 2:
        v = _ramos_distintos(ramos)
        if v != "nao":
            return v
    if ARB_COMPAR_RE.search(texto):
        return "nao-avaliado"
    return "nao"


def arbiter_declarations(rows: list[dict], ronda: str | None = None,
                        has_enq: bool = True) -> dict:
    """P-1 + P-26 support. Per open `Unknown`, the THREE declarations the row owes,
    as a conjunction: does it cite an `M-n` (only owed where `enquadramento.md`
    exists), does its `swing` phrase name >= 2 answers, and does that phrase name
    which technical axis moves? `ronda` narrows it to the round just run.

    Declaration (i) has two admissible forms: cite an `M-n`, or carry the marker
    `TO-BE DIVERGENCE`. The `M-n` waiver over declaration (iii) is gone (P-26):
    citing an invariant is the context half and never the consequence half. Presence
    only -- whether the axis named is the right one is the arbiter's reading, not
    this function's."""
    sem: list[dict] = []
    sem_ref: list[dict] = []
    sem_m: list[dict] = []
    sem_eixo: list[dict] = []
    sem_classe: list[dict] = []
    sem_alt_aval: list[dict] = []
    decisivas = 0
    total = 0
    for r in rows:
        if r["state"] != "Unknown" or r["resolved"]:
            continue
        if ronda and r["ronda"] != ronda:
            continue
        total += 1
        # DEF-P2-01: the metadata of a reclassification never sustains the declaration
        # it audits. Body only -- the annotation is preserved on the row and in the
        # file, and is simply not evidence of anything the row declares.
        body = r.get("swing_body", r.get("swing_text") or "")
        text = " ".join((split_annotation(r.get("claim") or "")[0], body,
                         split_annotation(r.get("support") or "")[0]))
        cita_m = bool(ARB_M_RE.search(text))
        tobe = bool(ARB_TOBE_RE.search(text))
        alt = declara_alternativas(body)
        duas = alt == "sim"
        if alt == "nao-avaliado":
            sem_alt_aval.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"],
                                 "motivo": "forma comparativa -- >= 2 respostas nao avaliado"})
        eixo = bool(ARB_AXIS_RE.search(body))
        if r.get("swing_form") == "nao-lida":
            # DEF-P4-01: the class could not be read. It is not `decisivo` and it is
            # not `cosmetico` either -- it is unknown, and says so in its own list
            # instead of silently joining a count.
            sem_classe.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"],
                               "motivo": "classe do swing nao avaliada (forma nao suportada)"})
        if r["swing_class"] == "decisivo":
            decisivas += 1
            if not ARB_REF_RE.search(text):
                sem_ref.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"],
                                "motivo": "`decisivo` sem referente nomeado"})
        if not cita_m and not tobe:
            sem_m.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"]})
        if not eixo:
            sem_eixo.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"],
                             "swing_class": r["swing_class"],
                             "swing_inferred": r["swing_inferred"],
                             "motivo": "o swing nao nomeia o eixo tecnico que muda"})
        # P-26: conjuncao. A declaracao (i) so e devida ao motor quando ha
        # enquadramento declarado, e satisfaz-se por qualquer das duas formas.
        em_falta = []
        if has_enq and not (cita_m or tobe):
            em_falta.append("nao cita M-n nem declara TO-BE DIVERGENCE")
        # `nao-avaliado` nao entra em falta: nao se prova ausencia com uma forma que
        # o motor admite nao saber ler.
        if alt == "nao":
            em_falta.append("o swing nao nomeia >= 2 respostas")
        if not eixo:
            em_falta.append("o swing nao nomeia o eixo tecnico que muda")
        if not em_falta:
            continue
        sem.append({"id": r["id"], "lens": r["lens"], "ronda": r["ronda"],
                    "swing_class": r["swing_class"],
                    "swing_inferred": r["swing_inferred"],
                    "motivo": " + ".join(em_falta)})
    return {
        "avaliadas": total,
        # a pre-v2.3 SU has no `swing` column at all: every row lands here for a
        # reason the arbiter cannot act on. Say how many, so nobody reads it as a
        # finding (states.md -> Compatibility).
        "sem_coluna_swing": sum(1 for x in sem if x["swing_inferred"]),
        "sem_declaracao": sem,
        "decisivas": decisivas,
        # DEF-P4-01: rows whose swing class the motor could not read. `decisivas` is a
        # count of rows READ as decisive, so these are neither in it nor against it.
        "classe_nao_avaliada": sem_classe,
        # DEF-P1-03: formas em que o motor nao decide se ha duas respostas. Nem contam
        # como declaradas, nem como em falta -- contam como por ler.
        "alternativas_nao_avaliadas": sem_alt_aval,
        "decisivo_sem_referente": sem_ref,
        # P-0: quais nao satisfazem (i) por nenhuma das duas formas. Nao e falha por
        # si onde nao ha enquadramento -- e a lista existe para alguem LER se alguma
        # pergunta o porque que um `M-n` ja responde.
        "sem_citacao_m": sem_m,
        # P-26, terceira declaracao isolada: uteis separadas porque e a que quase
        # nenhuma linha anterior a regra carrega, e misturada com as outras duas
        # deixaria de se ver quantas mudaram de estado por causa DESTA.
        "sem_eixo": sem_eixo,
        # Mesma razao que `sem_coluna_swing`: numa SU pre-v2.3 nao ha coluna `swing`,
        # logo NENHUMA linha pode nomear o eixo -- contar isso como falta de declaracao
        # seria ler como achado o que e ausencia de esquema. Diz-se quantas sao.
        "sem_eixo_sem_coluna": sum(1 for x in sem_eixo if x["swing_inferred"]),
        "conjuncao": ("P-26: as tres declaracoes sao devidas em conjunto; citar `M-n` "
                      "nao dispensa nomear o eixo tecnico. A (i) satisfaz-se por `M-n` "
                      "ou pelo marcador `TO-BE DIVERGENCE` (veredicto do dono, 2026-09-10)"),
        "enquadramento_declarado": has_enq,
        "ids": [x["id"] for x in sem] + [x["id"] for x in sem_ref],
        "regex": {
            "m_n": ARB_M_RE.pattern,
            "to_be": ARB_TOBE_RE.pattern,
            "alternativas": ARB_ALT_RE.pattern,
            "referente": ARB_REF_RE.pattern,
            "eixo": ARB_AXIS_RE.pattern,
        },
        "falsos_negativos": ("ACEITES por desenho -- uma row que declare a divergencia "
                             "em palavras que estes regex nao conhecem passa em silencio. "
                             "Falsos POSITIVOS nao sao aceites: um motor que avisa a torto "
                             "deixa de ser lido"),
        "julgamento": ("o motor verifica PRESENCA de declaracao; se a pergunta e material, "
                       "se o referente e o certo e se a classe do swing esta bem sao "
                       "julgamento do arbitro (aisa-round step 5f). Lista vazia significa "
                       "'nada em falta que este regex saiba ver', nunca 'aprovado'"),
        "calibracao": list(CALIBRACAO),
    }


def funding_gate_audit(rows: list[dict], context: dict,
                       ronda: str | None = None) -> dict:
    """P-4. Com `context.json.funding_gate = false` a decisao de avancar nao depende de
    aprovacao orcamental de terceiros, e a lente financeira nao constroi envelope: nenhuma
    `Unknown` de envelope, limiar, CAPEX/OPEX ou imputacao. Ausente = `true` (comportamento
    anterior), e entao nao ha nada a verificar.

    Presenca por regex, nunca julgamento: nao decide se a pergunta de custo era util.
    """
    gate = context.get("funding_gate", True)
    fin = [r for r in rows
           if r["state"] == "Unknown" and not r["resolved"]
           and "financial" in r["lens"].lower()
           and (ronda is None or r["ronda"] == ronda)]
    infra = []
    if gate is False:
        for r in fin:
            text = " ".join((r.get("claim") or "", r.get("swing_body") or "",
                             r.get("support") or ""))
            termo = funding_term(text)
            if termo:
                infra.append({"id": r["id"], "ronda": r["ronda"],
                              "termo": termo,
                              "motivo": "envelope/limiar/imputacao com funding_gate=false"})
    return {
        "funding_gate": gate,
        "aplicavel": gate is False,
        "financeiras_abertas": len(fin),
        "infracoes": infra,
        "ids": [x["id"] for x in infra],
        "regex": FUNDING_RE.pattern,
        "falsos_negativos": ("ACEITES: uma pergunta de envelope escrita sem nenhum destes "
                             "termos passa. Falsos POSITIVOS nao sao aceites -- o termo "
                             "encontrado vai no resultado para se poder contestar, e um "
                             "termo polissemico (tecto, limiar, envelope) so conta com "
                             "qualificador financeiro por perto (DEF-P3-01)"),
        "julgamento": ("com `funding_gate=true` nao ha nada a verificar e a lista vem vazia "
                       "por isso, nao por aprovacao. O mandato permanente da lente "
                       "(custo as-is, custo de nao fazer, custo de atraso) e julgamento da "
                       "lente, nao deste motor"),
        "calibracao": list(CALIBRACAO),
    }


def enquadramento_state(eng: Path, rows: list[dict]) -> dict:
    """P-0 -- the owner's declared business mechanism. `R-00` is not a round of
    lenses and the `M-n` rows are not a lens's output: they are the hypothesis the
    owner declared before anyone looked. Exposed apart so /status and the page can
    say `enquadramento (dono)` instead of counting a seventh lens and a fifth round.
    """
    md = _read(eng / "enquadramento.md") or ""
    invar: list[dict] = []
    for tbl in parse_tables(md):
        if not tbl.headers or norm_key(tbl.headers[0]) != "id":
            continue
        for _line, cells in tbl.rows:
            mid = (cells[0] if cells else "").strip().strip("*` ")
            if not re.fullmatch(r"M-\d+", mid):
                continue
            invar.append({
                "id": mid,
                "invariante": cells[1].strip() if len(cells) > 1 else "",
                "orienta": cells[2].strip() if len(cells) > 2 else "",
                "fonte": cells[3].strip() if len(cells) > 3 else "",
            })
    su_rows = [r for r in rows
               if r["ronda"] == ENQ_ROUND or norm_key(r["lens"]) == ENQ_LENS]
    ligados = {}
    for r in su_rows:
        for mid in re.findall(r"\benquadramento\.md#(M-\d+)", r.get("support") or ""):
            ligados.setdefault(mid, []).append(r["id"])
    for inv in invar:
        inv["rows"] = ligados.get(inv["id"], [])
    return {
        "presente": (eng / "enquadramento.md").is_file(),
        "ficheiro": "enquadramento.md",
        "ronda": ENQ_ROUND,
        "lens": ENQ_LENS,
        "rotulo": "enquadramento (dono)",
        "invariantes": invar,
        "rows": [r["id"] for r in su_rows],
        "nota": ("R-00 e a declaracao do dono, nao uma ronda de lentes; as rows M-n "
                 "nao contam como producao de uma lente"),
    }


def round_delta(rows: list[dict], round_dates: dict) -> dict:
    """P-2 -- convergence per round, read from the SU, never estimated.

    criadas   `Unknown` rows whose `ronda` is R-NN (still open or resolved later).
    fechadas  `Unknown` rows carrying a `resolved ->` marker whose CLOSURE round is
              R-NN. The closure round is resolved in order: (1) the `ronda` of the
              destination row the marker names -- the round in which the answer was
              written, which is what the council-log records; (2) the destination's
              `verificado_em`, when that date matches exactly one round in
              `round_dates`. Neither -> the row goes to `indeterminadas`, is counted
              in no round, and says so. Nothing is estimated.

    novas     per round, the rows created in R-NN per state (all five) -- P-13.
    `abertas` / `critical_abertas` are the engagement's CURRENT snapshot -- the two
    numbers /round and /status print next to the round they just ran -- not history.
    """
    ids = {r["id"]: r for r in rows}
    date_to_round: dict[str, list[str]] = {}
    for rid, val in round_dates.items():
        if rid.startswith("_"):
            continue
        date_to_round.setdefault(val[0], []).append(rid)

    unknowns = [r for r in rows if r["state"] == "Unknown"]
    criadas: dict[str, int] = {}
    fechadas: dict[str, int] = {}
    sem_ronda = 0
    retiradas = 0
    fonte = {"destino.ronda": 0, "destino.verificado_em": 0, "indeterminado": 0}
    indet: list[dict] = []

    for r in unknowns:
        if r["ronda"]:
            criadas[r["ronda"]] = criadas.get(r["ronda"], 0) + 1
        else:
            sem_ronda += 1
        if not r["resolved"]:
            continue
        if r.get("retired"):
            # Withdrawn for scope: not an answer, so not a closure of any round (P-21).
            retiradas += 1
            continue
        rnd = src_label = ""
        for tid in r["resolved_to"]:
            dst = ids.get(tid)
            if dst is None:
                continue
            if dst["ronda"]:
                rnd, src_label = dst["ronda"], "destino.ronda"
                break
            cands = date_to_round.get(dst["verificado_em"], [])
            if len(cands) == 1:
                rnd, src_label = cands[0], "destino.verificado_em"
                break
        if rnd:
            fechadas[rnd] = fechadas.get(rnd, 0) + 1
            fonte[src_label] += 1
        else:
            fonte["indeterminado"] += 1
            indet.append({
                "id": r["id"], "ronda": r["ronda"], "resolved_to": r["resolved_to"],
                "motivo": ("destino sem ronda e sem data que identifique uma ronda unica"
                           if r["resolved_to"] else
                           "marcador de resolucao sem id de destino"),
            })

    determinavel = not indet and sem_ronda == 0
    # P-13: what each round ADDED, per state -- the `/status` block "desde a ultima
    # passagem" reads it. Presence of `ronda` on the row, never a date.
    novas: dict[str, dict[str, int]] = {}
    for r in rows:
        if r["ronda"] and r["state"] in SECTIONS:
            novas.setdefault(r["ronda"], {st: 0 for st in SECTIONS})[r["state"]] += 1

    ordered = sorted(set(criadas) | set(fechadas) | set(novas), key=lambda x: _round_sort(x, ""))
    por_ronda = []
    acc_c = acc_f = 0
    for rid in ordered:
        c, f = criadas.get(rid, 0), fechadas.get(rid, 0)
        acc_c += c
        acc_f += f
        por_ronda.append({
            "ronda": rid, "criadas": c, "fechadas": f, "sem_convergencia": c > f,
            "abertas_no_fim": (acc_c - acc_f) if determinavel else None,
            "novas": novas.get(rid, {st: 0 for st in SECTIONS}),
        })
    nota = ("fecho datado pela ronda do destino, ou pela data do destino quando ela "
            "identifica uma ronda unica")
    if indet:
        nota += "; {} row(s) sem fecho determinavel -- listadas em `indeterminadas`, " \
                "contadas em nenhuma ronda".format(len(indet))
    if sem_ronda:
        nota += "; {} Unknown sem `ronda`".format(sem_ronda)
    if not determinavel:
        nota += "; `abertas_no_fim` fica a null (a serie cumulativa nao fecha)"
    return {
        "por_ronda": por_ronda,
        "retiradas": retiradas,
        "abertas": sum(1 for r in unknowns if not r["resolved"]),
        "critical_abertas": sum(1 for r in unknowns
                                if not r["resolved"] and r["criticidade"] == "Critical"),
        "criadas_sem_ronda": sem_ronda,
        "indeterminadas": indet,
        "fonte_fecho": fonte,
        "nota": nota,
    }


TW_HEAD_RE = re.compile(r"^-\s*\*\*(Revision conditions[^*]*|Tripwires[^*]*)\*\*", re.I)


def parse_tripwires(decisions_md: str) -> list[dict]:
    """Bullets under '**Tripwires**' OR '**Revision conditions**' of the LAST D-NNN block.
    No live engagement uses the kernel's 'Tripwires' label -- both use the older one."""
    if not decisions_md:
        return []
    blocks = re.split(r"^## ", decisions_md, flags=re.M)
    block = ""
    for b in blocks:
        if re.match(r"D-\d+", b.strip()):
            block = b
    if not block:
        return []
    lines = block.splitlines()
    out: list[dict] = []
    collecting = False
    for line in lines:
        if TW_HEAD_RE.match(line.strip()):
            collecting = True
            continue
        if collecting:
            s = line.strip()
            if s.startswith("- **") or (s.startswith("## ")):
                break
            if s.startswith("-") or s.startswith("*"):
                text = s.lstrip("-* ").strip()
                if not text:
                    continue
                m = re.match(r"(TW-\d+)\s*:\s*(.*)$", text, re.I)
                label = m.group(1).upper() if m else "TW-{}".format(len(out) + 1)
                body = m.group(2) if m else text
                out.append({"tw": label, "text": body, "cited_ids": ID_RE.findall(body),
                            "status": "quiet", "evidence": []})
    return out


def scan_tripwires(tws: list[dict], rows: list[dict]) -> list[dict]:
    """status in {quiet, watch}. NEVER 'fired' -- deciding that a free-prose condition
    actually fired is a semantic judgement; a deterministic script must not invent it.
    The verdict belongs to /status."""
    index = {r["id"]: r for r in rows}
    for tw in tws:
        ev = []
        for rid in tw["cited_ids"]:
            r = index.get(rid)
            if not r:
                continue
            if not r["resolved"] and (r["criticidade"] == "Critical" or r["expired"]):
                ev.append({"id": rid, "state": r["state"], "expired": r["expired"],
                           "criticidade": r["criticidade"]})
        if ev:
            tw["status"] = "watch"
            tw["evidence"] = ev
    return tws


def next_action(state: dict, rows: list[dict], health: dict, agenda: dict,
                critical: list[dict], artefacts: list[dict]) -> dict:
    """SUPERSEDED by milestone() (A0): a fixed phase -> command map sent a Decision
    engagement to `/render --all` while its blueprint sat unapproved with four
    structural choices open. Kept only so an external caller does not break."""
    phase = norm_key(state.get("phase", ""))
    missing = [a["name"] for a in artefacts if not a["exists"]]
    if missing:
        return {"text": "Artefacto esperado em falta nesta fase: {}. Retomar a fase antes "
                        "de avancar.".format(", ".join(missing[:3])),
                "command": "/resume"}
    if critical:
        cmds = " ".join('/answer {} "..."'.format(c["id"]) for c in critical[:2])
        return {"text": "{} itens Critical abertos (Unknown/Conflicted). Resolver com o "
                        "sponsor antes de avancar de fase.".format(len(critical)),
                "command": cmds}
    if health["expired"]:
        return {"text": "{} rows Confirmed/Assumed expiradas ({}% de saúde epistémica). "
                        "Revalidar antes de decidir.".format(health["expired"], health["pct"]),
                "command": "/status"}
    nxt = {"discovery": "/frame", "framing": "/options", "options": "/simulate -> /premortem -> /decide",
           "decision": "/render --all"}.get(phase, "/status")
    return {"text": "Sem bloqueios criticos abertos na fase {}.".format(phase or "?"),
            "command": nxt}


# ------------------------------------------------------------ markdown -> html

CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
ITAL_RE = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
ITAL2_RE = re.compile(r"(?<![\w_])_([^_\n]+)_(?![\w_])")
STRIKE_RE = re.compile(r"~~([^~]+)~~")


def prov_title(row: dict) -> str:
    bits = [row["state"], row["lens"] or "-"]
    if row["verificado_em"]:
        v = "verificado {}".format(row["verificado_em"])
        if row["validade"]:
            v += " ({})".format(row["validade"])
        if row["verificado_em_source"].startswith("inferido"):
            v += " [inferido]"
        bits.append(v)
    elif row["criticidade"]:
        bits.append(row["criticidade"])
    if row["ronda"]:
        bits.append(row["ronda"])
    if row["expired"]:
        bits.append("EXPIRADA ha {}d".format(row["days_overdue"]))
    if row["resolved"]:
        bits.append("resolvida" + (" -> " + ", ".join(row["resolved_to"]) if row["resolved_to"] else ""))
    return " · ".join(bits)


def prov_span(row_id: str, row: dict | None) -> str:
    if not row:
        return esc(row_id)
    cls = "prov" + (" prov-exp" if row["expired"] else "") + (" prov-res" if row["resolved"] else "")
    return '<span class="{}" data-id="{}" title="{}" tabindex="0">{}</span>'.format(
        cls, esc(row_id), esc(prov_title(row)), esc(row_id))


SAFE_SCHEMES = {"http", "https", "mailto"}
SCHEME_RE = re.compile(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):")


def safe_href(url: str) -> str | None:
    """The URL when it is safe to put in an `href`, None when it is not.

    Engagement content is client material: a source, a transcript or an artefact
    can carry `[Abrir fonte](javascript:alert(1))`, and escaping the TEXT of the
    URL does not stop the browser executing the SCHEME (F12, adversarial review
    2026-09-08). Allow-list, never deny-list: `http(s)`, `mailto`, and relative
    targets (including `#anchor`). Everything else -- `javascript:`, `data:`,
    `vbscript:`, `file:`, and any scheme invented tomorrow -- renders as text.
    Whitespace and control characters are stripped first: `java	script:` is one
    of the oldest ways past a scheme check.
    """
    if not url:
        return None
    cleaned = "".join(ch for ch in url if ord(ch) > 32 and ch != "")
    if not cleaned:
        return None
    m = SCHEME_RE.match(cleaned)
    if m:
        return cleaned if m.group(1).lower() in SAFE_SCHEMES else None
    # No scheme: relative target. `//host/path` is scheme-relative, not relative.
    return None if cleaned.startswith("//") else cleaned


def _render_link(m: re.Match) -> str:
    """`[text](url)` -> anchor when the scheme is safe, plain text when it is not.

    The rejected URL stays VISIBLE (as text, escaped) instead of disappearing: a
    reader must be able to see what the source actually wrote."""
    href = safe_href(m.group(2))
    if href is None:
        return "{} ({})".format(m.group(1), esc(m.group(2)))
    return '<a href="{}">{}</a>'.format(esc(href), m.group(1))


def inline_md(text: str, ids: dict | None = None) -> str:
    """Escape first, then apply emphasis; code spans are lifted out beforehand so a
    mega-regex cannot mangle **bold with `code`**."""
    if not text:
        return ""
    spans: list[str] = []

    def _stash(m: re.Match) -> str:
        spans.append(m.group(1))
        return "\x00{}\x00".format(len(spans) - 1)

    s = CODE_RE.sub(_stash, text)
    s = esc(s)
    s = LINK_RE.sub(_render_link, s)
    s = BOLD_RE.sub(r"<strong>\1</strong>", s)
    s = STRIKE_RE.sub(r"<del>\1</del>", s)
    s = ITAL_RE.sub(r"<em>\1</em>", s)
    s = ITAL2_RE.sub(r"<em>\1</em>", s)
    if ids:
        # Only link ids that exist in the parsed index: 'R-01' is a round label in every
        # ronda cell and throughout the prose, and 'R-' is also the Risky prefix.
        s = ID_RE.sub(lambda m: prov_span(m.group(1), ids[m.group(1)])
                      if m.group(1) in ids else m.group(0), s)
    s = re.sub(r"\x00(\d+)\x00", lambda m: "<code>{}</code>".format(esc(spans[int(m.group(1))])), s)
    return s


def block_md(md: str, ids: dict | None = None, max_lines: int | None = None) -> str:
    if not md:
        return ""
    lines = md.splitlines()
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines] + ["", "*(truncado)*"]
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s:
            i += 1
            continue
        if s.startswith("```"):
            j = i + 1
            buf = []
            while j < n and not lines[j].strip().startswith("```"):
                buf.append(lines[j])
                j += 1
            out.append("<pre><code>{}</code></pre>".format(esc("\n".join(buf))))
            i = j + 1
            continue
        if re.match(r"^(-{3,}|\*{3,})$", s):
            out.append("<hr>")
            i += 1
            continue
        if s.startswith("#"):
            lvl = min(len(s) - len(s.lstrip("#")), 4)
            out.append("<h{0} class=\"md-h\">{1}</h{0}>".format(
                lvl + 2 if lvl < 4 else 6, inline_md(s.lstrip("#").strip(), ids)))
            i += 1
            continue
        if "|" in line and i + 1 < n and SEP_RE.match(lines[i + 1]) and "|" in lines[i + 1]:
            headers = split_row(line)
            body = []
            j = i + 2
            while j < n and "|" in lines[j] and lines[j].strip():
                cells, _ = fit_row(split_row(lines[j]), len(headers))
                body.append(cells)
                j += 1
            out.append('<div class="tw"><table><thead><tr>{}</tr></thead><tbody>{}</tbody>'
                       "</table></div>".format(
                           "".join("<th>{}</th>".format(inline_md(h, ids)) for h in headers),
                           "".join("<tr>{}</tr>".format(
                               "".join("<td>{}</td>".format(inline_md(c, ids)) for c in row))
                               for row in body)))
            i = j
            continue
        if s.startswith(">"):
            buf = []
            while i < n and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            out.append("<blockquote>{}</blockquote>".format(inline_md(" ".join(buf), ids)))
            continue
        m_li = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", line)
        if m_li:
            ordered = not m_li.group(2) in ("-", "*")
            tag = "ol" if ordered else "ul"
            items = []
            while i < n:
                mm = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", lines[i])
                if not mm:
                    break
                indent = len(mm.group(1))
                items.append((indent, mm.group(3)))
                i += 1
            html_items = []
            depth = 0
            for indent, txt in items:
                lvl = 1 if indent >= 2 else 0
                while depth < lvl:
                    html_items.append("<ul>")
                    depth += 1
                while depth > lvl:
                    html_items.append("</ul>")
                    depth -= 1
                html_items.append("<li>{}</li>".format(inline_md(txt, ids)))
            while depth > 0:
                html_items.append("</ul>")
                depth -= 1
            out.append("<{0}>{1}</{0}>".format(tag, "".join(html_items)))
            continue
        buf = []
        while i < n and lines[i].strip() and not lines[i].strip().startswith(("#", ">", "```", "|")) \
                and not re.match(r"^(\s*)([-*]|\d+[.)])\s+", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if not buf:
            # PROGRESS GUARANTEE. Reachable only for a line starting with "|" that the
            # table branch above declined: a table whose separator row is missing, a
            # table at end of file, an orphan pipe line, or a table header left
            # dangling by the `max_lines` cut. Consuming nothing here spun `while i < n`
            # forever, appending an empty paragraph each pass until the process died of
            # MemoryError -- whose message is empty, so the tool reported exactly
            # "[dashboard] build falhou: " and overwrote the page with an error page.
            # Render the line as text and advance; every other branch already advances.
            buf.append(s)
            i += 1
        out.append("<p>{}</p>".format(inline_md(" ".join(buf), ids)))
    return "".join(out)


# ------------------------------------------------------------ narrative / timeline


def _round_sort(round_id: str, date_str: str) -> tuple:
    m = re.match(r"([RFOD])-(\d+)", round_id or "")
    if m:
        return (PHASE_ORDER.get(m.group(1), 9), int(m.group(2)), date_str or "")
    return (9, 99, date_str or "")


def parse_story(md: str) -> list[dict]:
    if not md:
        return []
    out = []
    for chunk in re.split(r"^##\s+", md, flags=re.M)[1:]:
        head, _, body = chunk.partition("\n")
        dm = DATE_RE.search(head)
        rm = ROUND_RE.search(head)
        out.append({"kind": "story", "title": head.strip(), "when": dm.group(0) if dm else "",
                    "round": rm.group(1) if rm else "", "body": body.strip()})
    return out


def parse_council_log(md: str) -> list[dict]:
    if not md:
        return []
    out = []
    for chunk in re.split(r"^##\s+", md, flags=re.M)[1:]:
        head, _, body = chunk.partition("\n")
        dm = DATE_RE.search(head)
        rm = ROUND_RE.search(head)
        out.append({"kind": "council", "title": head.strip(), "when": dm.group(0) if dm else "",
                    "round": rm.group(1) if rm else "", "body": body.strip()})
    return out


def parse_decisions(md: str) -> list[dict]:
    if not md:
        return []
    out = []
    for chunk in re.split(r"^##\s+", md, flags=re.M)[1:]:
        head, _, body = chunk.partition("\n")
        if not re.match(r"D-\d+", head.strip()):
            continue
        dm = DATE_RE.search(body)
        rm = re.search(r"\*\*(?:Decided|Agreed) in round\*\*:\s*(\S+)", body)
        out.append({"kind": "decision", "title": head.strip(), "when": dm.group(0) if dm else "",
                    "round": rm.group(1).strip("*` ") if rm else "", "body": body.strip()})
    return out


def build_timeline(story, council, decisions, round_dates: dict, ids: dict,
                   docs: list[dict] | None = None) -> list[dict]:
    events = []
    for d in (docs or []):
        # A phase artefact IS an event in the engagement's story. The full text lives in
        # the Fase tab; the timeline carries the marker so the narrative is not a hole.
        body = ("`{}` -- {} caracteres, {} ids do SU citados. "
                "Texto integral no separador **Outputs**.").format(
                    d["rel"], d["chars"], len(d["ids"]))
        events.append({
            "kind": "artefacto", "when": "", "round": d["round"],
            "title": d["title"], "html": block_md(body, ids), "ids": d["ids"],
        })
    for ev in story + council + decisions:
        when = ev["when"]
        if not when and ev["round"] and ev["round"] in round_dates:
            when = round_dates[ev["round"]][0]
        events.append({
            "kind": ev["kind"], "when": when, "round": ev["round"],
            "title": ev["title"],
            "html": block_md(ev["body"], ids, max_lines=None),
            "ids": sorted({i for i in ID_RE.findall(ev["body"]) if i in ids}),
        })
    kind_rank = {"story": 0, "council": 1, "artefacto": 2, "decision": 3}
    dated_rounds = sorted(
        ((k, v[0]) for k, v in round_dates.items() if k != "_fallback" and v[0]),
        key=lambda kv: _round_sort(kv[0], ""))

    def sort_key(e):
        rank = kind_rank.get(e["kind"], 9)
        if e["round"]:
            return _round_sort(e["round"], e["when"]) + (rank,)
        if e["when"]:
            owner = ""
            for r, d in dated_rounds:
                if d <= e["when"]:
                    owner = r
            if owner:
                return _round_sort(owner, e["when"]) + (rank + 0.5,)
        return (-1, 0, e["when"] or "", rank)  # undated: the opening of the story

    events.sort(key=sort_key)
    return events


# ---------------------------------------------------------------- artefact index

INDEX_DIRS = ["inputs", "_capture", "lens-outputs", "_simulation", "_synthesis",
              "_blueprint", "_coverage", "_retro", "_render"]
# `_coverage` is here for TWO reasons, and the second is the one that bites: this list
# is also what `_needs_rebuild` scans. Left out of it, publishing a review changed the
# model (`status.coverage`) while the page kept its old mtime verdict and never
# regenerated -- and `on-su-change.py` spawns the generator WITHOUT `--force`, so a
# trigger alone would not have fixed it. No cycle: the generator writes only
# `dashboard.html`, which sits at the engagement root and is skipped here and there.
# What a person reads for each folder of the Ficheiros tab (P-13); the folder name stays
# in the heading's tooltip.
GROUP_LABEL = {
    "em falta": "Em falta", "raiz": "Raiz do projecto", "inputs": "Ficheiros de entrada",
    "_capture": "Leitura dos ficheiros", "lens-outputs": "Leituras das perspectivas",
    "_simulation": "Ensaio das alternativas", "_synthesis": "Resumos por tema",
    "_blueprint": "Desenho dos ecrãs", "_coverage": "Conferência do que foi pedido",
    "_retro": "Lições do fim", "_render": "Documentos finais",
}
INDEX_FILES = ["context.json", "shared-understanding.md", "story.md", "answers.md",
               "council-log.md", "frame.md", "options.md", "premortem.md", "decisions.md"]
SKIP_PREFIX = ("~$",)
SKIP_NAMES = {"dashboard.html"}
SKIP_SUFFIX = (".tmp",)

EXPECTED_BY_PHASE = {
    "discovery": [],
    "framing": ["frame.md"],
    "options": ["frame.md", "options.md"],
    "decision": ["frame.md", "options.md", "decisions.md", "_synthesis/business-story.md"],
}


def expected_for_phase(phase: str) -> list[str]:
    return EXPECTED_BY_PHASE.get(norm_key(phase), [])


def _skip(name: str) -> bool:
    return (name in SKIP_NAMES or name.startswith(SKIP_PREFIX)
            or name.endswith(SKIP_SUFFIX) or name == "__pycache__")


def _entry(eng: Path, p: Path, group: str) -> dict:
    rel = p.relative_to(eng).as_posix()
    try:
        st = p.stat()
        size, mtime = st.st_size, datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M")
    except OSError:
        size, mtime = 0, ""
    return {"group": group, "name": rel, "rel": rel, "href": href_for(rel),
            "size": size, "size_h": human_size(size), "mtime": mtime,
            "exists": True, "note": ""}


def artefact_index(eng: Path, state: dict) -> list[dict]:
    out: list[dict] = []
    for name in INDEX_FILES:
        p = eng / name
        if p.is_file():
            out.append(_entry(eng, p, "raiz"))
    for d in INDEX_DIRS:
        base = eng / d
        if not base.is_dir():
            continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or _skip(p.name):
                continue
            if any(part.startswith(".") for part in p.relative_to(eng).parts):
                continue
            out.append(_entry(eng, p, d))
    have = {a["rel"] for a in out}
    for exp in expected_for_phase(state.get("phase", "")):
        if exp not in have:
            out.append({"group": "em falta", "name": exp, "rel": exp, "href": "",
                        "size": 0, "size_h": "-", "mtime": "", "exists": False,
                        "note": "esperado na fase '{}' e ausente".format(state.get("phase", ""))})
    return out


# The narrative artefacts each phase produces. Until now the dashboard listed these as
# filenames in the artefact index and rendered none of them -- so the whole output of a
# /frame or /options round was invisible on a page whose job is to show where things are.
PHASE_DOC_SPECS = [
    ("process-model", "_capture/process-model.md", "Modelo de processo", "discovery"),
    ("frame", "frame.md", "Frame \u2014 a frase única", "framing"),
    ("options", "options.md", "Opções na mesa", "options"),
    ("simulation", "_simulation/options-comparison_v*.md", "Simulação das opções", "options"),
    ("premortem", "premortem.md", "Pré-mortem", "options"),
    ("decisions", "decisions.md", "Decisões", "decision"),
    ("synthesis", "_synthesis/*.md", "Topic packs", "decision"),
    ("blueprint", "_blueprint/ux-blueprint_v*.yaml", "Blueprint UX", "decision"),
]
PHASE_RANK = {"discovery": 0, "framing": 1, "options": 2, "decision": 3}
PHASE_FIRST_ROUND = {"discovery": "R-01", "framing": "F-01", "options": "O-01",
                     "decision": "D-01"}
# What a person reads for each phase (glossary.md, *Como se diz ao utilizador*); the
# kernel name stays in the tooltip wherever the label is rendered.
PHASE_LABEL = {"discovery": "Ouvir e perguntar", "framing": "A frase do problema",
               "options": "As alternativas", "decision": "A escolha"}


def _latest(eng: Path, pattern: str) -> list[Path]:
    """Versioned artefacts: newest only. Plain globs: all of them, sorted."""
    hits = sorted(eng.glob(pattern))
    if not hits:
        return []
    if "_v*" in pattern:
        return [hits[-1]]
    return [h for h in hits if not h.name.startswith("_")]


def frame_sentence(md: str) -> str:
    """The single problem sentence -- the whole point of Framing, and the thing an
    approval is an approval OF.

    It lives under '## Single problem sentence', written either as a blockquote or in
    bold: `pricing-marinha-pilot-1`, `kam-onboarding` and `cae-automation` all use bold,
    and the blockquote-only reader returned "" for all three -- no sentence on the page,
    and nothing to approve. Normalisation is deliberate and narrow, because this output
    is hashed (P-18/F05): quote markers, bold wrappers, horizontal rules and whitespace
    are presentation and must not change the identity; the words are the identity.
    """
    # Three real headings across the engagements: `## Single problem sentence`
    # (kernel template), `### Frame sentence` (dpt-galp-jp). Reading only the first
    # would call a framed engagement "no frame" and make its approval unverifiable.
    m = re.search(r"^#{2,4}\s+(?:Single problem sentence|Frame sentence)\s*$"
                  r"(.*?)(?=^#{1,4}\s|\Z)", md, re.M | re.S)
    if not m:
        return ""
    lines = []
    for raw in m.group(1).splitlines():
        line = raw.strip()
        if line.startswith(">"):
            line = line.lstrip(">").strip()
        if not line or re.fullmatch(r"[-*_]{3,}", line):   # blank or horizontal rule
            continue
        lines.append(line)
    text = re.sub(r"\s+", " ", " ".join(lines)).strip()
    text = re.sub(r"^(?:\*\*|__)(.+?)(?:\*\*|__)$", r"\g<1>", text).strip()
    return unicodedata.normalize("NFC", text)


def frame_sha256(sentence: str) -> str:
    """Fingerprint of the sentence, or "" when there is no sentence.

    Never the hash of the empty string: "no sentence" and "a sentence that happens to
    normalise to nothing" must not be able to match an approval."""
    if not sentence:
        return ""
    return hashlib.sha256(sentence.encode("utf-8")).hexdigest()


def collect_phase_docs(eng: Path, ids: dict) -> list[dict]:
    out: list[dict] = []
    for key, pattern, title, phase in PHASE_DOC_SPECS:
        paths = _latest(eng, pattern) if "*" in pattern else (
            [eng / pattern] if (eng / pattern).is_file() else [])
        for path in paths:
            raw = _read(path)
            if raw is None or not raw.strip():
                continue
            rel = path.relative_to(eng).as_posix()
            body = raw
            # Drop the H1: the card already carries the title.
            body = re.sub(r"\A#\s+[^\n]*\n", "", body)
            # A 40k-character process model in the DOM costs more than it gives. Cap the
            # inline render; the file link in the summary is always the full text.
            cap = 220 if len(body) > 14000 else None
            if path.suffix in (".yaml", ".yml"):
                html = "<pre><code>{}</code></pre>".format(esc(body))
                if BP_FILE_RE.match(path.name):
                    st = _read_json(eng / "_state.json")
                    iss = bp_validate(raw, path.name, bp_pack_cfg(st.get("pack", "")),
                                      set(ids), bp_loader(eng))
                    nb = sum(1 for i in iss if i["severity"] == "block")
                    nw = len(iss) - nb
                    if nb:
                        badge = ("<p class=\"bp-check bad\">Estrutura: <strong>{} falha(s) que impedem a "
                                 "aprovação</strong> · {} aviso(s) — {}</p>").format(
                            nb, nw, esc(", ".join(sorted({i["code"] for i in iss if i["severity"] == "block"}))))
                    elif nw:
                        badge = "<p class=\"bp-check warn\">Estrutura: sem falhas · {} aviso(s)</p>".format(nw)
                    else:
                        badge = "<p class=\"bp-check ok\">Estrutura: verificada, sem falhas</p>"
                    html = badge + html
            else:
                html = block_md(body, ids, max_lines=cap)
            truncated = cap is not None
            if not body.strip():
                continue  # header-only file: /frame writes decisions.md's D-001 on validation
            rm = ROUND_RE.search(raw[:400])
            cited = sorted({i for i in ID_RE.findall(raw) if i in ids})
            out.append({
                "key": key,
                "title": title if len(paths) == 1 else "{} \u2014 {}".format(title, path.stem),
                "rel": rel, "href": href_for(rel), "phase": phase,
                "round": rm.group(1) if rm else PHASE_FIRST_ROUND[phase],
                "html": html, "ids": cited, "chars": len(body),
                "truncated": truncated,
            })
    out.sort(key=lambda d: (PHASE_RANK.get(d["phase"], 9), d["rel"]))
    return out


RENDER_RE = re.compile(r"^(?P<slug>.+)_(?P<deliv>[a-z0-9-]+)_v(?P<ver>\d{2})\.(md|html|docx)$")


def render_versions(eng: Path) -> dict:
    out: dict[str, list[str]] = {}
    rd = eng / "_render"
    if not rd.is_dir():
        return out
    for p in sorted(rd.iterdir()):
        if not p.is_file():
            continue
        m = RENDER_RE.match(p.name)
        if not m:
            continue
        out.setdefault(m.group("deliv"), [])
        tag = "v" + m.group("ver")
        if tag not in out[m.group("deliv")]:
            out[m.group("deliv")].append(tag)
    for k in out:
        out[k].sort()
    return out


def parse_render_gaps(eng: Path) -> list[dict]:
    txt = _read(eng / "_render" / "render-gaps.md")
    if not txt:
        return []
    gaps = []
    for tbl in parse_tables(txt):
        heads = [h.strip() for h in tbl.headers]
        for _, cells in tbl.rows:
            gaps.append(dict(zip(heads, cells)))
    return gaps


# =============================================================== status layer
# Step A0 of docs/STATUS_IMPROVEMENT_PLAN.md: the deterministic facts `/status`
# needs and this tool did not carry. Everything below is FACT EXTRACTION only.
#
# Boundary (normative, do not weaken):
#   * no function here emits a tripwire verdict of "fired", declares a structural
#     choice resolved, or judges whether a condition is evaluable -- those are
#     semantic judgements and belong to the aisa-status skill;
#   * "no evidence in the SU" is reported as exactly that, never as "OK";
#   * nothing here invents an owner, a criterion, a duration or a date.


# ---------------------------------------------------- tolerant YAML extraction
# A blueprint is authored by an LLM and is not guaranteed to be well-formed:
# `pricing-marinha` v05 (an APPROVED version) fails yaml.safe_load at
# irreversible_choices. A strict parse would therefore lose the whole record for
# the sections that ARE well-formed. So: no PyYAML, stdlib only, and a targeted
# indentation walk that reads the keys the status view needs and skips the rest.

_YL_TRUE = {"true", "yes", "on"}
_YL_FALSE = {"false", "no", "off"}
_YL_NULL = {"", "null", "~"}


def yl_scalar(raw: str):
    """One YAML scalar -> python. Quotes stripped, booleans/ints coerced, `[..]` -> list
    (Y2), `{..}` -> dict (Y5, one level). Null is `null` / `~` / empty ONLY -- `none` is
    text (blueprint-contract.md -> Validação estrutural). Anchors, aliases, tags and
    nested flow mappings come back as YlUnsupported (a str) and are signalled upstream."""
    s = (raw or "").strip()
    if s.startswith("#"):
        return ""
    # strip a trailing comment only where it cannot be inside a quoted string
    if not (s[:1] and s[:1] in "\"'[{"):
        s = re.sub(r"\s+#.*$", "", s).strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    if s[:1] and s[:1] in "&*!":
        return YlUnsupported(s)
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [yl_scalar(x) for x in _yl_split_flow(inner)]
    if s.startswith("{") and s.endswith("}"):
        return _yl_flow_map(s)
    if s[:1] and s[:1] in "[{":
        return YlUnsupported(s)
    low = s.lower()
    if low in _YL_TRUE:
        return True
    if low in _YL_FALSE:
        return False
    if low in _YL_NULL:
        return None
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    return s


def _yl_lines(text: str) -> list[tuple[int, str]]:
    """(indent, stripped content) for every line with content. Comments dropped."""
    out = []
    for line in (text or "").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        out.append((len(line) - len(line.lstrip(" ")), line.strip()))
    return out


def _yl_scope(lines: list[tuple[int, str]], parent: str | None):
    """Index range of `parent:`'s children, or the whole file when parent is None."""
    if not parent:
        return 0, len(lines)
    for i, (ind, content) in enumerate(lines):
        if re.match(r"^" + re.escape(parent) + r"\s*:", content):
            for j in range(i + 1, len(lines)):
                if lines[j][0] <= ind:
                    return i + 1, j
            return i + 1, len(lines)
    return None, None


def yl_find_block(text: str, key: str, parent: str | None = None) -> list[tuple[int, str]]:
    """Child lines of `key:` (optionally nested under `parent:`), by indentation.

    Tolerant by construction: it never parses what it was not asked for, so a
    malformed sibling section cannot destroy this one.
    """
    lines = _yl_lines(text)
    lo, hi = _yl_scope(lines, parent)
    if lo is None:
        return []
    start = base = None
    for i in range(lo, hi):
        ind, content = lines[i]
        if re.match(r"^" + re.escape(key) + r"\s*:", content):
            start, base = i, ind
            break
    if start is None:
        return []
    out = []
    for i in range(start + 1, hi):
        ind, content = lines[i]
        if ind <= base:
            break
        out.append((ind, content))
    return out


def yl_scalar_at(text: str, key: str, parent: str | None = None):
    """Value of `key:` where it is a scalar on the key line. None when absent."""
    lines = _yl_lines(text)
    lo, hi = _yl_scope(lines, parent)
    if lo is None:
        return None
    for i in range(lo, hi):
        m = re.match(r"^" + re.escape(key) + r"\s*:\s*(.*)$", lines[i][1])
        if m:
            return yl_scalar(m.group(1))
    return None


# ------------------------------------------------ YAML subset parser (Y1-Y7)
# The blueprint is authored by an LLM and read without PyYAML (stdlib only, by
# design: requirements-dev.txt). The subset the kernel reads is DECLARED here and
# in blueprint-contract.md → "Validação estrutural"; a form outside it is
# signalled (BP-YAML-UNSUPPORTED), never read in silence.
#
#   Y1 scalar `k: v`            Y5 flow mapping `k: {a: 1, b: [x]}` — one level of braces
#   Y2 flow list `k: [a, b]`    Y6 block mapping `k:` + deeper `k2: v2`, any depth
#   Y3 block list `k:` + `- a`  Y7 block scalar `>` / `|` (folded to one line, as before)
#   Y4 list of maps `- k: v` + siblings at the same indent
#
# Scalars follow YAML 1.2 for null (`null`, `~`, empty) — `none` is TEXT: it is the
# headless value of `experience.mode`. Booleans keep YAML 1.1 (`yes`/`no`) because
# the blueprint template writes `funded: yes|no`.


class YlUnsupported(str):
    """A flow form the subset does not read (anchor, alias, tag, nested `{{}}`).
    A str subclass so tolerant consumers keep the raw text; validators detect it."""


def _yl_split_flow(inner: str) -> list[str]:
    """Split a flow collection body on top-level commas (quotes and brackets aware)."""
    parts, buf, depth, quote = [], [], 0, None
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote = ch
            buf.append(ch)
            continue
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    tail = "".join(buf)
    if tail.strip() or parts:
        parts.append(tail)
    return [p.strip() for p in parts if p.strip()]


_YL_KEY_RE = re.compile(r"^(\"[^\"]*\"|'[^']*'|[^\s:#\-\[\]{},][^:]*?)\s*:(?:\s+(.*)|$)")


def _yl_flow_map(s: str):
    """`{a: 1, b: x}` -> dict (Y5). Nested braces are outside the subset."""
    inner = s[1:-1].strip()
    if "{" in inner or "}" in inner:
        return YlUnsupported(s)
    out: dict = {}
    if not inner:
        return out
    for part in _yl_split_flow(inner):
        m = _yl_KEY_RE_match(part)
        if m:
            k, v = m
            out[k] = yl_scalar(v) if v is not None else None
        else:
            out[part.strip("\"'")] = None
    return out


def _yl_KEY_RE_match(part: str):
    m = _YL_KEY_RE.match(part)
    if not m:
        return None
    key = m.group(1).strip().strip("\"'")
    rest = m.group(2)
    rest = rest.strip() if rest is not None else None
    if rest is not None and rest.startswith("#"):
        rest = ""          # `key:   # comment` — the value is the nested block, not the comment
    return key, rest


def _yl_lines_n(text: str) -> tuple[list[tuple[int, str, int]], list[dict]]:
    """(indent, stripped content, 1-based line) for every content line; tab-indented
    lines are reported as malformed and skipped."""
    out: list[tuple[int, str, int]] = []
    issues: list[dict] = []
    for n, line in enumerate((text or "").replace("\r\n", "\n").split("\n"), start=1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        lead = line[: len(line) - len(line.lstrip())]
        if "\t" in lead:
            issues.append({"kind": "malformed", "line": n, "message": "tab na indentação"})
            continue
        if line.strip() == "---" and not out:
            continue
        if line.strip() == "---" and out:
            issues.append({"kind": "unsupported", "line": n, "message": "segundo documento (`---`)"})
            break
        out.append((len(lead), line.strip(), n))
    return out, issues


def _yl_children(lines, i: int, hi: int, base: int) -> tuple[int, int]:
    j = i + 1
    while j < hi and lines[j][0] > base:
        j += 1
    return i + 1, j


def _yl_fold(lines, lo: int, hi: int, head: str = "") -> str:
    parts = ([head] if head else []) + [lines[k][1] for k in range(lo, hi)]
    return " ".join(p.strip() for p in parts).strip()


def _yl_scalar_checked(rest: str, ln: int, issues: list[dict]):
    if rest[:1] in "&*!" or rest.startswith("? "):
        issues.append({"kind": "unsupported", "line": ln,
                       "message": "âncora/alias/tag/chave explícita: " + rest[:30]})
        return YlUnsupported(rest)
    v = yl_scalar(rest)
    if isinstance(v, YlUnsupported):
        issues.append({"kind": "unsupported", "line": ln,
                       "message": "forma de fluxo fora do subconjunto: " + rest[:40]})
    return v


def _yl_block(lines, lo: int, hi: int, issues: list[dict]):
    if lo >= hi:
        return None
    base = lines[lo][0]
    if lines[lo][1] == "-" or lines[lo][1].startswith("- "):
        return _yl_seq(lines, lo, hi, base, issues)
    return _yl_map(lines, lo, hi, base, issues)


def _yl_map(lines, lo: int, hi: int, base: int, issues: list[dict]) -> dict:
    out: dict = {}
    i = lo
    while i < hi:
        ind, content, ln = lines[i]
        if ind != base:
            issues.append({"kind": "malformed", "line": ln,
                           "message": "indentação inesperada ({} vs {})".format(ind, base)})
            i += 1
            continue
        if content == "-" or content.startswith("- "):
            issues.append({"kind": "malformed", "line": ln, "message": "item de lista dentro de mapa"})
            c_lo, c_hi = _yl_children(lines, i, hi, base)
            i = c_hi
            continue
        km = _yl_KEY_RE_match(content)
        if km is None:
            if content[:1] in "&*!" or content.startswith("? "):
                issues.append({"kind": "unsupported", "line": ln, "message": content[:40]})
            else:
                issues.append({"kind": "malformed", "line": ln, "message": "linha sem `chave:`"})
            c_lo, c_hi = _yl_children(lines, i, hi, base)
            i = c_hi
            continue
        key, rest = km
        c_lo, c_hi = _yl_children(lines, i, hi, base)
        if rest is None or rest == "":
            out[key] = _yl_block(lines, c_lo, c_hi, issues) if c_lo < c_hi else None
        elif rest in (">", "|", ">-", "|-", ">+", "|+"):
            out[key] = _yl_fold(lines, c_lo, c_hi)
        else:
            if c_lo < c_hi:
                # a plain/quoted scalar continued on deeper lines: folded text, as before
                out[key] = _yl_fold(lines, c_lo, c_hi, rest)
            else:
                out[key] = _yl_scalar_checked(rest, ln, issues)
        i = c_hi
    return out


def _yl_seq(lines, lo: int, hi: int, base: int, issues: list[dict]) -> list:
    out: list = []
    i = lo
    while i < hi:
        ind, content, ln = lines[i]
        if ind != base or not (content == "-" or content.startswith("- ")):
            issues.append({"kind": "malformed", "line": ln,
                           "message": "esperado item `- ` na indentação {}".format(base)})
            c_lo, c_hi = _yl_children(lines, i, hi, ind)
            i = c_hi
            continue
        rest = content[1:].strip()
        c_lo, c_hi = _yl_children(lines, i, hi, base)
        if rest == "":
            out.append(_yl_block(lines, c_lo, c_hi, issues) if c_lo < c_hi else None)
        else:
            km = _yl_KEY_RE_match(rest) if rest[:1] not in "[{\"'" else None
            if km is not None:
                # The item's mapping sits where its first key sits (`- key` -> base+2). A
                # block scalar / empty first value owns every deeper line. A SCALAR first
                # value cannot own key-shaped children, so when the following lines are
                # all key-shaped at one deeper indent (an LLM's misindented siblings) that
                # indent is the mapping's -- what the old reader did, now by rule.
                off = len(content) - len(content[1:].lstrip()) if content[1:].strip() else 2
                child_ind = base + off
                first_rest = km[1]
                if c_lo < c_hi and first_rest not in (None, "", ">", "|", ">-", "|-", ">+", "|+"):
                    mn = min(lines[k][0] for k in range(c_lo, c_hi))
                    top = [lines[k] for k in range(c_lo, c_hi) if lines[k][0] == mn]
                    if mn > child_ind and all(_yl_KEY_RE_match(t[1]) for t in top):
                        child_ind = mn
                virtual = [(child_ind, rest, ln)] + [lines[k] for k in range(c_lo, c_hi)]
                out.append(_yl_map(virtual, 0, len(virtual), child_ind, issues))
            elif rest in (">", "|", ">-", "|-"):
                out.append(_yl_fold(lines, c_lo, c_hi))
            elif c_lo < c_hi:
                out.append(_yl_fold(lines, c_lo, c_hi, rest))
            else:
                out.append(_yl_scalar_checked(rest, ln, issues))
        i = c_hi
    return out


def yl_parse(text: str) -> tuple[object, list[dict]]:
    """Whole document -> python value + parse issues ({kind: malformed|unsupported,
    line, message}). Tolerant: a malformed line is reported and skipped, the rest is
    still read — an approved version that PyYAML rejects keeps its readable sections."""
    lines, issues = _yl_lines_n(text)
    if not lines:
        return None, issues
    return _yl_block(lines, 0, len(lines), issues), issues


def yl_list_of_maps(block: list[tuple[int, str]]) -> list[dict]:
    """`- k: v` sequence items -> dicts, nested lists/maps included (Y3/Y5/Y6 inside
    Y4). Scalar items become {"_value": x}. Block scalars are folded to one line."""
    if not block:
        return []
    lines = [(ind, content, 0) for ind, content in block]
    val = _yl_block(lines, 0, len(lines), [])
    if not isinstance(val, list):
        return []
    items: list[dict] = []
    for it in val:
        if isinstance(it, dict):
            if it:
                items.append(it)
        elif it is not None and it != "":
            items.append({"_value": it})
    return items


# ------------------------------------------------------ decisions: kind by role
# The kernel gives a solution decision and a blueprint approval the same D-NNN
# shape. They are not interchangeable: tripwires live on the SOLUTION decision,
# and reading them off the latest block -- what parse_tripwires does -- silently
# returns none for every engagement that approved a blueprint afterwards.

BP_APPROVAL_RE = re.compile(r"blueprint\s+bp-v(\d{1,3})\s+aprovad", re.I)
ADOPT_RE = re.compile(r"\b(?:adopt|adopta|adota|chosen option|op[cç][aã]o escolhida)\b", re.I)
OPTION_RE = re.compile(r"\b(O-\d{2,4})\b")
TS_PAT = r"(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2})?Z?)?)"
TS_RE = re.compile(TS_PAT)
DECISION_ID_RE = re.compile(r"^(D-\d{2,4})")


def _tw_bullets(body: str) -> tuple[list[dict], list[str]]:
    """(declared tripwires, unlabelled notes under the same heading).

    A bullet is a tripwire ONLY where it declares `TW-<n>:`. Auto-numbering the
    rest fabricates tripwires: `pricing-marinha` D-002 carries a note saying the
    other premortem candidates were considered and deliberately NOT adopted, and
    numbering it TW-2 made the view announce a tripwire the decision declined.
    Notes are returned, never dropped -- they are just not tripwires."""
    tws: list[dict] = []
    notes: list[str] = []
    collecting = False
    for line in body.splitlines():
        s = line.strip()
        if TW_HEAD_RE.match(s):
            collecting = True
            continue
        if collecting:
            if s.startswith("- **") or s.startswith("## "):
                break
            if s.startswith("-") or s.startswith("*"):
                text = s.lstrip("-* ").strip()
                if not text:
                    continue
                m = re.match(r"(TW-\d+)\s*:\s*(.*)$", text, re.I)
                if m:
                    tws.append({"tw": m.group(1).upper(), "text": m.group(2)})
                else:
                    notes.append(text)
    return tws, notes


def classify_decisions(md: str) -> list[dict]:
    """Every D-NNN block with the role it plays. File order preserved."""
    if not md:
        return []
    out: list[dict] = []
    for chunk in re.split(r"^##\s+", md, flags=re.M)[1:]:
        head, _, body = chunk.partition("\n")
        head = head.strip()
        dm = DECISION_ID_RE.match(head)
        if not dm:
            continue
        did = dm.group(1)
        approval = BP_APPROVAL_RE.search(head) or BP_APPROVAL_RE.search(body)
        opts = OPTION_RE.findall(head) + OPTION_RE.findall(body)
        tws, tw_notes = _tw_bullets(body)
        m = re.search(r"\*\*Timestamp\*\*\s*:\s*" + TS_PAT, body) or TS_RE.search(body)
        ts = m.group(1) if m else ""
        if approval:
            kind = "blueprint-approval"
        elif re.search(r"\bframe\b", head, re.I) and not opts:
            kind = "frame"
        elif opts and (ADOPT_RE.search(head) or ADOPT_RE.search(body)):
            kind = "solution"
        elif tws and opts:
            kind = "solution"
        else:
            kind = "other"
        for t in tws:
            t["decision"] = did
        # P-18/F05+F07: what an approval is an approval OF, and what replaced it.
        # `Supersedes` is the ONLY pointer written into the file (forward, in the new
        # block); `superseded_by` is derived below. Old blocks are never edited --
        # decisions.md is append-only, and a decision keeps its counterfactual.
        rm = re.search(r"\*\*(?:Agreed|Decided) in round\*\*\s*:\s*`?([A-Z]-\d+)", body)
        hm = re.search(r"\*\*Frame sha256\*\*\s*:\s*`?([0-9a-fA-F]{64})`?", body)
        sm = re.search(r"\*\*Supersedes\*\*\s*:\s*`?(D-\d{2,4})", body)
        out.append({
            "id": did, "title": head, "kind": kind, "when": ts,
            "round": rm.group(1) if rm else "",
            "sha256": (hm.group(1).lower() if hm else ""),
            "supersedes": sm.group(1) if sm else "",
            "superseded_by": "",
            # A frame approval written before the fingerprint rule cannot be compared,
            # only re-confirmed by the owner. Saying so beats guessing either way.
            "legacy": kind == "frame" and not hm,
            "blueprint_version": ("v" + approval.group(1).zfill(2)) if approval else "",
            "options_cited": sorted(set(opts)),
            "tripwires": tws,
            "tripwire_notes": tw_notes,
        })
    index = {b["id"]: b for b in out}
    for b in out:
        target = index.get(b["supersedes"])
        if target is not None and target is not b:
            target["superseded_by"] = b["id"]
    return out


def solution_decision(blocks: list[dict]) -> dict | None:
    """The decision that chose the solution -- the one tripwires belong to.

    A superseded decision is history, not the decision in force: after a reopen
    (P-18/F07) its tripwires belong to the block that replaced it, and reading them
    as live would keep watching the conditions of a choice nobody is making."""
    live = [b for b in blocks if not b.get("superseded_by")]
    sol = [b for b in live if b["kind"] == "solution"]
    if sol:
        return sol[-1]
    carrying = [b for b in live if b["tripwires"]]
    return carrying[-1] if carrying else None


def tripwire_facts(blocks: list[dict], rows: list[dict]) -> dict:
    """Tripwires of the SOLUTION decision + the SU evidence each one can see.

    `status` is limited to two values, neither of which is a verdict:
      watch        -- a cited SU id is open Critical or expired
      no-evidence  -- no cited id in the SU is open Critical or expired
    "fired" is never emitted here, and `no-evidence` is NOT "OK": whether a
    condition is evaluable at all in the current phase is the skill's call.
    """
    src = solution_decision(blocks)
    index = {r["id"]: r for r in rows}
    tws: list[dict] = []
    for t in (src or {}).get("tripwires", []):
        cited = ID_RE.findall(t["text"])
        resolvable, unresolvable, evidence = [], [], []
        for rid in cited:
            r = index.get(rid)
            if r is None:
                unresolvable.append(rid)
                continue
            resolvable.append(rid)
            if not r["resolved"] and (r["criticidade"] == "Critical" or r["expired"]):
                evidence.append({"id": rid, "state": r["state"], "expired": r["expired"],
                                 "criticidade": r["criticidade"]})
        tws.append({
            "tw": t["tw"], "text": t["text"], "decision": t.get("decision", ""),
            "cited_ids": cited, "resolvable_ids": resolvable,
            "unresolvable_ids": unresolvable, "evidence": evidence,
            "status": "watch" if evidence else "no-evidence",
        })
    return {
        "source_decision": (src or {}).get("id", ""),
        "source_kind": (src or {}).get("kind", ""),
        "unlabelled_notes": list((src or {}).get("tripwire_notes") or []),
        "approvals_after": [b["id"] for b in blocks if b["kind"] == "blueprint-approval"],
        "total": len(tws),
        "watch": sum(1 for t in tws if t["status"] == "watch"),
        "no_evidence": sum(1 for t in tws if t["status"] == "no-evidence"),
        "items": tws,
        "verdict_owner": "skill",
        "note": ("sem decisão-solução identificada — nenhuma fonte de tripwires; "
                 "verificação incompleta, nunca 'OK'") if not src else
                ("disparado / não-avaliável é veredicto do skill; 'no-evidence' significa "
                 "sem evidência na SU, nunca 'OK'"),
    }


# ------------------------------------------------------------------- blueprint

BP_FILE_RE = re.compile(r"^ux-blueprint_v(?P<ver>\d{2,3})\.ya?ml$", re.I)


def _bp_refs(raw) -> list[str]:
    if isinstance(raw, list):
        return [str(x) for x in raw if x]
    if isinstance(raw, str) and raw.strip():
        return ID_RE.findall(raw) or [raw.strip()]
    return []


def bp_decision_id(text: str) -> str:
    """O `D-NNN` que a versao concretiza, venha da chave que vier (F16).

    `bp_validate` aceita `decision_ref` OU `concretizes_decision`
    (blueprint-contract.md -> Codigos, BP-REQ-KEY); o leitor tem de aceitar as duas, ou
    uma ligacao documental existente desaparece da projeccao. Normaliza as duas formas
    reais -- `decisions.md#D-002` e `D-002` -- para o id, e devolve "" quando nao ha id
    nenhum a ler (nunca inventa)."""
    raw = yl_scalar_at(text, "decision_ref") or yl_scalar_at(text, "concretizes_decision")
    m = re.search(r"\bD-\d{2,4}\b", str(raw or ""))
    return m.group(0) if m else ""


def bp_read(p: Path) -> dict:
    text = _read(p) or ""
    oac = yl_find_block(text, "open_architecture_choices", "architecture") \
        or yl_find_block(text, "open_architecture_choices")
    po = yl_find_block(text, "proof_obligations", "architecture") \
        or yl_find_block(text, "proof_obligations")
    choices = []
    for c in yl_list_of_maps(oac):
        choices.append({
            "choice": c.get("choice") or c.get("id") or c.get("_value") or "",
            "structural": bool(c.get("structural")),
            "su_refs": _bp_refs(c.get("su_refs") or c.get("su_ref")),
            "would_be_settled_by": c.get("would_be_settled_by") or "",
            "owner": c.get("owner") or "",
            "resolved": bool(c.get("resolved")),
            "closure_basis": c.get("closure_basis") or c.get("basis") or "",
        })
    proofs = [{
        "claim": q.get("claim") or q.get("_value") or "",
        "level": q.get("level") or "",
        "method": q.get("method") or "",
        "owner": q.get("owner") or "",
        "funded": q.get("funded"),
    } for q in yl_list_of_maps(po)]
    ver = "v" + BP_FILE_RE.match(p.name).group("ver").zfill(2)
    return {
        "version": ver, "file": p.name, "rel": "_blueprint/" + p.name,
        "draft": bool(yl_scalar_at(text, "draft")),
        "option": yl_scalar_at(text, "option") or yl_scalar_at(text, "option_ref") or "",
        # F16: o alias entra aqui, num sitio so. `decision_ref` conserva o valor CRU
        # do ficheiro (ha fixtures e snapshots que o leem tal e qual); `decision_id` e a
        # forma normalizada, que e o que qualquer consumidor deve comparar.
        "decision_ref": (yl_scalar_at(text, "decision_ref")
                         or yl_scalar_at(text, "concretizes_decision") or ""),
        "decision_id": bp_decision_id(text),
        "authorization": yl_scalar_at(text, "authorization", "architecture") or "",
        "experience_mode": yl_scalar_at(text, "mode", "experience") or "",
        "open_choices": choices,
        "structural_open": [c for c in choices if c["structural"] and not c["resolved"]],
        "proof_obligations": proofs,
        "readable": bool(text.strip()),
    }


# --------------------------------------------------- blueprint: structural check
# bp_validate reads presence, type and form against blueprint-contract.md →
# "Validação estrutural" and the aisa-blueprint step-2 template. It never decides
# what is structural, whether a closure basis suffices, or whether a su_ref points
# at the right row — those are the pack's and the skill's. Severity lives in one
# table so the owner can recalibrate without touching the rules.

BP_SEE_RE = re.compile(r"SEE_V(\d{1,3})", re.I)   # search, not fullmatch: real versions write
                                                  # `screens: SEE_V01 + export_features (ver v04)`,
                                                  # and render-validate.py already follows that shape
BP_ENUMS = {
    "authorization": ("authorized", "authorized-bounded", "not-authorized"),
    "experience.mode": ("none", "owned-internal", "owned-external", "inherited"),
    "record_authority[].access_mode": ("owned", "virtualized", "replicated", "keep-in-place"),
    "compositions[].boundary": ("in-platform", "outside-platform"),
    "proof_obligations[].level": ("V1", "V2", "V3", "V4"),
}
BP_TOP_REQUIRED = ("version", "architecture", "personas", "entities", "screens",
                   "excluded_from_ui", "validation")
BP_TOP_ADVISED = ("open_questions", "navigation", "app")          # warn when absent
BP_TOP_LISTS = ("personas", "entities", "screens", "excluded_from_ui", "open_questions")
BP_ARCH_SCALARS = ("scope", "authorization", "authorization_basis", "architectability_basis")
BP_ARCH_LISTS = ("record_authority", "compositions", "relocated_responsibilities",
                 "proof_obligations", "open_architecture_choices")
BP_DEAD_PREFIXES = ("C", "A", "U", "X", "R", "RI", "CF", "D")     # PM-/TW- live elsewhere
BP_SEVERITY = {
    "BP-YAML-UNSUPPORTED": "block", "BP-YAML-MALFORMED": "block",
    "BP-REQ-KEY": "block", "BP-TYPE": "block", "BP-ARCH-REQ": "block", "BP-ENUM": "block",
    "BP-SURFACE": "block", "BP-COMP-REQ": "block", "BP-RA-REQ": "block", "BP-AC-KEY": "block",
    "BP-RR-REQ": "block", "BP-NO-SUREFS": "block", "BP-LEAF-NO-SUREF": "warn",
    "BP-ITEM-TYPE": "block",
    "BP-BAD-ID": "warn", "BP-DEAD-ID": "warn", "BP-STRUCT-TYPE": "block",
    "BP-STRUCT-MISSING": "block", "BP-STRUCT-NO-SETTLE": "block", "BP-RESOLVED-TYPE": "block",
    "BP-RESOLVED-NO-BASIS": "block", "BP-PO-REQ": "warn", "BP-DRAFT": "block",
    "BP-VERSION": "block", "BP-NESTED-SPLIT": "warn",
}
BP_ADVISED_SEVERITY = "warn"   # BP-REQ-KEY for BP_TOP_ADVISED keys


def _bp_iss(out: list[dict], code: str, path: str, message: str, line: int = 0,
            severity: str | None = None) -> None:
    out.append({"code": code, "severity": severity or BP_SEVERITY.get(code, "warn"),
                "path": path, "line": int(line or 0), "message": message})


def _bp_refs_of(node: dict):
    """(present?, refs list) — `su_refs` or `su_ref`, list or scalar."""
    if not isinstance(node, dict):
        return False, []
    for k in ("su_refs", "su_ref"):
        if k in node:
            v = node[k]
            if isinstance(v, list):
                return True, [str(x) for x in v if x not in (None, "")]
            if isinstance(v, str) and v.strip():
                return True, ID_RE.findall(v) or [v.strip()]
            return True, []
    return False, []


def _bp_container(node, kind: str) -> str:
    """list|map|ref|delta|missing|bad for a container the contract wants as `kind`."""
    if node is None:
        return "missing"
    if isinstance(node, str) and BP_SEE_RE.match(node.strip()):
        return "ref"
    if kind == "list":
        if isinstance(node, list):
            return "list"
        if isinstance(node, dict) and any(isinstance(v, str) and BP_SEE_RE.match(v.strip())
                                          for k, v in node.items() if k == "baseline"):
            return "delta"
        return "bad"
    return "map" if isinstance(node, dict) else "bad"


def _bp_delta_items(node: dict) -> list:
    items: list = []
    for k, v in node.items():
        if k.startswith("changes") and isinstance(v, list):
            items.extend(x for x in v if isinstance(x, dict))
    return items


def _bp_list_items(node) -> list:
    if isinstance(node, list):
        return node
    if isinstance(node, dict):
        return _bp_delta_items(node)
    return []


def _bp_map_items(node, path: str, out: list[dict]) -> list[dict]:
    """Items of a contract list that MUST be mappings. A scalar item is a structural
    defect, not something to skip: skipping is how `open_architecture_choices:
    ["missing classification"]` passed as valid."""
    items = []
    for i, it in enumerate(_bp_list_items(node)):
        p = "{}[{}]".format(path, i)
        if isinstance(it, dict):
            items.append((p, it))
            continue
        if it is None:
            _bp_iss(out, "BP-ITEM-TYPE", p, "item nulo — mapa esperado")
            continue
        _bp_iss(out, "BP-ITEM-TYPE", p,
                "item escalar ({!r}) — mapa esperado com os campos do contrato".format(
                    str(it)[:60]))
        if isinstance(it, str) and ID_RE.fullmatch(it.strip()):
            _bp_iss(out, "BP-NESTED-SPLIT", p,
                    "item escalar com id ({}) — sintoma de lista aninhada lida como item".format(it))
    return items


def _bp_enum(out: list[dict], value, path: str, key: str) -> None:
    """Enumerated field: a wrong TYPE is a wrong value. `authorization: true` used to
    slip through because the check only ran when the value was already text."""
    if value is None or value == "":
        return
    allowed = BP_ENUMS[key]
    raw = value.strip() if isinstance(value, str) else value
    if isinstance(raw, str) and raw in allowed:
        return
    if key == "proof_obligations[].level" and isinstance(raw, str) and raw.upper() in allowed:
        return
    _bp_iss(out, "BP-ENUM", path, "valor {!r} fora de {}".format(raw, allowed))


def _bp_walk_leaves(node, path: str, out: list[dict]) -> None:
    """BP-LEAF-NO-SUREF: a `{value, state: Assumed|Confirmed}` leaf without su_ref(s)
    or `source`. Unknown leaves are excused (they point at `open:`)."""
    if isinstance(node, dict):
        st = node.get("state")
        if isinstance(st, str) and st.strip().lower() in ("assumed", "confirmed"):
            present, refs = _bp_refs_of(node)
            if not refs and not node.get("source"):
                _bp_iss(out, "BP-LEAF-NO-SUREF", path,
                        "folha com state={} sem su_ref/su_refs nem source".format(st))
        for k, v in node.items():
            _bp_walk_leaves(v, path + "." + str(k), out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _bp_walk_leaves(v, "{}[{}]".format(path, i), out)


def _bp_provenance(items: list, path: str, out: list[dict], su_ids: set | None,
                   check_nested: bool = True) -> None:
    """`items` is a list of (path, mapping) pairs from _bp_map_items, or raw mappings."""
    for entry in items:
        p, it = entry if isinstance(entry, tuple) else (path, entry)
        if not isinstance(it, dict):
            continue
        present, refs = _bp_refs_of(it)
        if not refs:
            _bp_iss(out, "BP-NO-SUREFS", p, "nó sem su_refs/su_ref não vazio (regra 1)")
        for r in refs:
            if not ID_RE.fullmatch(r.strip()):
                _bp_iss(out, "BP-BAD-ID", p + ".su_refs", "token não é id: {}".format(r))
            elif su_ids is not None and r.split("-")[0] in BP_DEAD_PREFIXES and r not in su_ids:
                _bp_iss(out, "BP-DEAD-ID", p + ".su_refs", "id sem linha na SU: {}".format(r))
        if check_nested:
            for sub in ("actions", "data"):
                v = it.get(sub)
                if isinstance(v, list) and any(isinstance(x, dict) for x in v):
                    _bp_provenance([x for x in v if isinstance(x, dict)], p + "." + sub, out,
                                   su_ids, check_nested=False)
                elif isinstance(v, dict) and any(isinstance(x, dict) for x in v.values()):
                    groups = [x for x in v.values() if isinstance(x, dict)]
                    _bp_provenance(groups, p + "." + sub, out, su_ids, check_nested=False)


def bp_validate(text: str, filename: str = "", pack_cfg: dict | None = None,
                su_ids: set | None = None, loader=None) -> list[dict]:
    """Structural issues of one blueprint file. Empty list == valid (no `block`, no
    `warn`). `su_ids` enables BP-DEAD-ID; `loader(vNN) -> text` resolves SEE_Vnn."""
    out: list[dict] = []
    tree, yiss = yl_parse(text or "")
    for y in yiss:
        _bp_iss(out, "BP-YAML-UNSUPPORTED" if y["kind"] == "unsupported" else "BP-YAML-MALFORMED",
                "$", y["message"], y.get("line", 0))
    if not isinstance(tree, dict):
        _bp_iss(out, "BP-YAML-MALFORMED", "$", "documento não é um mapa — versão ilegível")
        return out
    pack_cfg = pack_cfg or {}

    # --- top level ---------------------------------------------------------
    required = list(BP_TOP_REQUIRED) + [k for k in (pack_cfg.get("required_keys") or []) if k]
    for k in required:
        if k not in tree:
            _bp_iss(out, "BP-REQ-KEY", k, "chave de topo obrigatória ausente")
    for k in BP_TOP_ADVISED:
        if k not in tree:
            _bp_iss(out, "BP-REQ-KEY", k, "chave de topo esperada ausente", severity=BP_ADVISED_SEVERITY)
    if not any(k in tree for k in ("engagement", "blueprint_id")):
        _bp_iss(out, "BP-REQ-KEY", "engagement|blueprint_id", "identidade do engagement ausente")
    draft = tree.get("draft") is True
    if draft:
        _bp_iss(out, "BP-DRAFT", "draft", "versão draft — nunca aprovável (regra 4)")
    elif not any(k in tree for k in ("decision_ref", "concretizes_decision")):
        _bp_iss(out, "BP-REQ-KEY", "decision_ref|concretizes_decision",
                "versão não-draft sem referência à decisão")

    # version vs filename
    fm = BP_FILE_RE.match(filename or "")
    if fm and "version" in tree:
        v = tree.get("version")
        vs = re.sub(r"\D", "", str(v)) if v is not None else ""
        if not vs or int(vs) != int(fm.group("ver")):
            _bp_iss(out, "BP-VERSION", "version",
                    "version no ficheiro ({}) ≠ v{} do nome".format(v, fm.group("ver")))

    # container types
    for k in BP_TOP_LISTS:
        if k in tree:
            kind = _bp_container(tree[k], "list")
            if kind == "missing":
                _bp_iss(out, "BP-TYPE", k, "lista esperada, valor nulo (ausente ≠ vazio ≠ inválido)")
            elif kind == "bad":
                _bp_iss(out, "BP-TYPE", k, "lista esperada, valor {}".format(type(tree[k]).__name__))
            elif kind == "ref" and loader is not None:
                m = BP_SEE_RE.match(str(tree[k]).strip())
                if not loader("v" + m.group(1).zfill(2)):
                    _bp_iss(out, "BP-TYPE", k, "referência {} a versão inexistente".format(tree[k]))
    for k in ("architecture", "validation", "app", "navigation"):
        if k in tree and _bp_container(tree[k], "map") not in ("map", "ref"):
            _bp_iss(out, "BP-TYPE", k, "mapa esperado, valor {}".format(
                "nulo" if tree[k] is None else type(tree[k]).__name__))

    # provenance on top-level nodes (regra 1)
    for k in ("personas", "entities", "screens", "excluded_from_ui"):
        node = tree.get(k)
        if isinstance(node, (list, dict)):
            _bp_provenance(_bp_map_items(node, k, out), k, out, su_ids)

    # --- architecture --------------------------------------------------------
    arch = tree.get("architecture")
    if isinstance(arch, str) and BP_SEE_RE.search(arch):
        # `architecture: SEE_Vnn` -- follow it, exactly as render-validate.py follows the
        # other blocks. An unresolvable reference is a blocking defect: returning "no
        # issues" for a version whose architecture was never read is how an unverified
        # version passed as valid.
        m = BP_SEE_RE.search(arch)
        other = loader("v" + m.group(1).zfill(2)) if loader is not None else ""
        if not other:
            _bp_iss(out, "BP-TYPE", "architecture",
                    "referência {} não resolúvel{} — a arquitectura não foi verificada".format(
                        arch.strip(),
                        "" if loader is not None else " (sem engagement para a resolver)"))
            return _bp_sorted(out)
        sub, subiss = yl_parse(other)
        arch = (sub or {}).get("architecture") if isinstance(sub, dict) else None
        if not isinstance(arch, dict):
            _bp_iss(out, "BP-TYPE", "architecture",
                    "referência {} aponta para uma versão sem bloco architecture legível".format(
                        arch if isinstance(arch, str) else m.group(0)))
            return _bp_sorted(out)
    if not isinstance(arch, dict):
        if "architecture" in tree:
            _bp_iss(out, "BP-TYPE", "architecture",
                    "mapa esperado, valor {}".format(
                        "nulo" if arch is None else type(arch).__name__))
        return _bp_sorted(out)
    for k in BP_ARCH_SCALARS:
        if k not in arch or arch.get(k) in (None, ""):
            _bp_iss(out, "BP-ARCH-REQ", "architecture." + k, "campo obrigatório ausente ou vazio")
    _bp_enum(out, arch.get("authorization"), "architecture.authorization", "authorization")
    exp = arch.get("experience")
    if "experience" not in arch:
        _bp_iss(out, "BP-ARCH-REQ", "architecture.experience", "mapa obrigatório ausente")
    elif not isinstance(exp, dict):
        _bp_iss(out, "BP-TYPE", "architecture.experience", "mapa esperado")
    else:
        mode = exp.get("mode")
        if mode in (None, ""):
            _bp_iss(out, "BP-ARCH-REQ", "architecture.experience.mode", "campo obrigatório ausente ou vazio")
        elif not (isinstance(mode, str) and mode.strip() in BP_ENUMS["experience.mode"]):
            _bp_enum(out, mode, "architecture.experience.mode", "experience.mode")
        else:
            surf = exp.get("primary_surface")
            if str(mode) == "none" and surf not in (None, ""):
                _bp_iss(out, "BP-SURFACE", "architecture.experience.primary_surface",
                        "mode: none exige primary_surface: null")
            if str(mode) != "none" and (not isinstance(surf, str) or not surf.strip()):
                _bp_iss(out, "BP-SURFACE", "architecture.experience.primary_surface",
                        "mode: {} exige primary_surface nomeada".format(mode))
    for k in BP_ARCH_LISTS:
        if k not in arch:
            _bp_iss(out, "BP-ARCH-REQ", "architecture." + k, "lista obrigatória ausente (vazia é válida)")
        elif _bp_container(arch[k], "list") == "missing":
            _bp_iss(out, "BP-TYPE", "architecture." + k, "lista esperada, valor nulo")
        elif _bp_container(arch[k], "list") not in ("list", "ref", "delta"):
            _bp_iss(out, "BP-TYPE", "architecture." + k,
                    "lista esperada, valor {}".format(type(arch[k]).__name__))

    # compositions
    seen: set = set()
    for p, it in _bp_map_items(arch.get("compositions"), "architecture.compositions", out):
        for k in ("component", "pattern", "forced_by", "boundary"):
            if it.get(k) in (None, ""):
                _bp_iss(out, "BP-COMP-REQ", p + "." + k, "campo obrigatório ausente")
        _bp_enum(out, it.get("boundary"), p + ".boundary", "compositions[].boundary")
        c = str(it.get("component") or "").strip()
        if c and c in seen:
            _bp_iss(out, "BP-COMP-REQ", p + ".component", "component duplicado: {}".format(c))
        seen.add(c)

    # record_authority
    seen = set()
    ra_items = _bp_map_items(arch.get("record_authority"), "architecture.record_authority", out)
    _bp_provenance(ra_items, "architecture.record_authority", out, su_ids, check_nested=False)
    for p, it in ra_items:
        for k in ("domain", "authority", "access_mode", "key"):
            if it.get(k) in (None, ""):
                _bp_iss(out, "BP-RA-REQ", p + "." + k, "campo obrigatório ausente")
        _bp_enum(out, it.get("access_mode"), p + ".access_mode", "record_authority[].access_mode")
        raw_mode = it.get("access_mode")
        mode = raw_mode.strip() if isinstance(raw_mode, str) else ""
        has_fields = isinstance(it.get("fields"), list)
        ac = it.get("access_contract")
        has_ac = isinstance(ac, dict)
        if mode == "owned" and not has_fields and not has_ac:
            _bp_iss(out, "BP-RA-REQ", p + ".fields", "owned sem fields nem access_contract")
        if mode in ("keep-in-place", "virtualized") and not has_ac:
            _bp_iss(out, "BP-RA-REQ", p + ".access_contract", "{} sem access_contract".format(mode))
        if has_ac:
            key = ac.get("key")
            empty = key is None or key == [] or key == ""
            if empty and not ac.get("open") and not re.search(r"\bopen:\s*U-\d+", json.dumps(ac, ensure_ascii=False, default=str)):
                _bp_iss(out, "BP-AC-KEY", p + ".access_contract.key", "key vazio sem open: U-nnn")
        k = str(it.get("key") or "").strip()
        if k and k in seen:
            _bp_iss(out, "BP-RA-REQ", p + ".key", "key duplicado: {}".format(k))
        seen.add(k)

    # relocated_responsibilities
    seen = set()
    for p, it in _bp_map_items(arch.get("relocated_responsibilities"),
                               "architecture.relocated_responsibilities", out):
        for k in ("responsibility", "owner", "outcome_basis"):
            if it.get(k) in (None, ""):
                _bp_iss(out, "BP-RR-REQ", p + "." + k, "campo obrigatório ausente")
        r = str(it.get("responsibility") or "").strip()
        if r and r in seen:
            _bp_iss(out, "BP-RR-REQ", p + ".responsibility", "responsibility duplicada: {}".format(r))
        seen.add(r)

    # proof_obligations
    for p, it in _bp_map_items(arch.get("proof_obligations"),
                               "architecture.proof_obligations", out):
        for k in ("claim", "level", "method", "owner", "funded"):
            if k not in it or it.get(k) in (None, ""):
                _bp_iss(out, "BP-PO-REQ", p + "." + k, "campo ausente")
        _bp_enum(out, it.get("level"), p + ".level", "proof_obligations[].level")

    # open_architecture_choices
    oac = _bp_map_items(arch.get("open_architecture_choices"),
                        "architecture.open_architecture_choices", out)
    _bp_provenance(oac, "architecture.open_architecture_choices", out, su_ids, check_nested=False)
    for p, it in oac:
        if "structural" not in it:
            _bp_iss(out, "BP-STRUCT-MISSING", p + ".structural",
                    "classificação estrutural ausente — sem ela não há aprovação (regra 5)")
        elif not isinstance(it.get("structural"), bool):
            _bp_iss(out, "BP-STRUCT-TYPE", p + ".structural",
                    "structural deve ser true|false, é {!r}".format(it.get("structural")))
        structural = it.get("structural") is True
        if structural and it.get("would_be_settled_by") in (None, ""):
            _bp_iss(out, "BP-STRUCT-NO-SETTLE", p + ".would_be_settled_by",
                    "escolha estrutural sem o que a resolveria (regra 5)")
        if "resolved" in it and not isinstance(it.get("resolved"), bool):
            _bp_iss(out, "BP-RESOLVED-TYPE", p + ".resolved",
                    "resolved deve ser true|false, é {!r}".format(it.get("resolved")))
        if structural and it.get("resolved") is True and not (it.get("closure_basis") or it.get("basis")):
            _bp_iss(out, "BP-RESOLVED-NO-BASIS", p + ".closure_basis",
                    "escolha estrutural resolvida sem closure_basis (fact ≠ fit)")

    _bp_walk_leaves(arch, "architecture", out)
    return _bp_sorted(out)


def _bp_sorted(out: list[dict]) -> list[dict]:
    rank = {"block": 0, "warn": 1}
    return sorted(out, key=lambda i: (rank.get(i["severity"], 2), i["line"], i["path"], i["code"]))


def bp_pack_cfg(pack: str) -> dict:
    """`blueprint:` block of the active pack's pack.yaml (stdlib read). Absent → {}."""
    if not pack:
        return {}
    p = repo_root() / "library" / "packs" / pack / "pack.yaml"
    text = _read(p) or ""
    if not text:
        return {}
    block = yl_find_block(text, "blueprint")
    if not block:
        return {}
    val = _yl_block([(i, c, 0) for i, c in block], 0, len(block), [])
    return val if isinstance(val, dict) else {}


def bp_loader(eng: Path):
    def loader(ver: str) -> str:
        f = _bp_file(eng, ver)
        return (_read(f) or "") if f else ""
    return loader


def frame_identity(eng: Path, blocks: list[dict]) -> dict:
    """Does the approval on file approve the sentence on file? (P-18 / F05)

    An approval used to be found by existence alone: `/options` looked for a D-NNN
    saying "Frame agreed" and proceeded. So F-02 could rewrite the sentence, the
    session die, and the old approval wave the NEW sentence through. The approval now
    carries the fingerprint of the sentence it approved, and this function compares it
    with the sentence on file. It reports; the skill decides (soft gate).

    Verdicts:
      no-frame            no frame.md, or no sentence in it -- nothing to approve yet
      none                a sentence, no frame approval at all
      legacy              the latest approval predates the fingerprint rule
      match               same fingerprint, approved in the current framing round
      match-other-round   same fingerprint, approved in an earlier round (anchors were
                          redone, the sentence was not) -- still approved
      mismatch            the sentence changed since the latest approval
    """
    md = _read(eng / "frame.md") or ""
    sentence = frame_sentence(md)
    sha = frame_sha256(sentence)
    rm = re.search(r"^##\s*Round:\s*([A-Z]-\d+)", md, re.M) or ROUND_RE.search(md[:400])
    frame_round = rm.group(1) if rm else ""
    approvals = [
        {"id": b["id"], "round": b["round"], "sha256": b["sha256"], "when": b["when"],
         "legacy": b["legacy"], "superseded_by": b["superseded_by"]}
        for b in blocks if b["kind"] == "frame"
    ]
    live = [a for a in approvals if not a["superseded_by"]]
    latest = live[-1] if live else (approvals[-1] if approvals else None)
    if not sentence:
        verdict = "no-frame"
    elif latest is None:
        verdict = "none"
    elif latest["legacy"] or not latest["sha256"]:
        verdict = "legacy"
    elif latest["sha256"] == sha:
        verdict = "match" if (not frame_round or latest["round"] == frame_round)             else "match-other-round"
    else:
        verdict = "mismatch"
    return {"present": bool(md), "round": frame_round, "sentence": sentence,
            "sha256": sha, "approvals": approvals, "latest": latest, "verdict": verdict}


def options_round_history(eng: Path, state: dict) -> dict:
    """The highest O- round this engagement ever ran, and the next one.

    Read from history, never from `_state.json` alone: after a decision the state says
    `D-01`, so a reopen that trusted it would restart at O-01 and overwrite the round
    that produced the decision being revisited (P-18 / F07). Sources, in order of
    trust: one chairman synthesis file per Options round (never rewritten), the
    `## O-NN` headings of the council log, and the state when it still holds an O-.
    `options.md` is not a source -- it is rewritten in place.
    """
    seen: set[int] = set()
    sources: list[str] = []
    for f in sorted((eng / "lens-outputs").glob("chairman-synthesis-O-*.md")):
        m = re.search(r"O-(\d+)", f.name)
        if m:
            seen.add(int(m.group(1)))
            sources.append(f.name)
    log = _read(eng / "council-log.md") or ""
    for m in re.finditer(r"^##\s*(O-\d+)", log, re.M):
        seen.add(int(m.group(1).split("-")[1]))
        if "council-log.md" not in sources:
            sources.append("council-log.md")
    sm = re.match(r"O-(\d+)", (state.get("round") or "").strip())
    if sm:
        seen.add(int(sm.group(1)))
        sources.append("_state.json")
    top = max(seen) if seen else 0
    return {"max": "O-{:02d}".format(top) if top else "",
            "next": "O-{:02d}".format(top + 1), "sources": sources}


REVISIT_FIELD_RE = {
    "decision": re.compile(r"^-?\s*\*\*Decision\*\*\s*:\s*`?(D-\d{2,4})", re.M),
    "target": re.compile(r"^-?\s*\*\*Target\*\*\s*:\s*`?([A-Z]+-\d+)", re.M),
    "verdict": re.compile(r"^-?\s*\*\*Recomenda[çc][ãa]o\*\*\s*:\s*\*{0,2}"
                          r"(MANTER|ADAPTAR|REABRIR)", re.M | re.I),
    "when": re.compile(r"^-?\s*\*\*Timestamp\*\*\s*:\s*`?" + TS_PAT, re.M),
}


def revisit_state(eng: Path) -> dict:
    """The latest `/revisit` verdict, read from a fixed header -- never from prose.

    `/options` needs a deterministic answer to "may this decision be reopened?"
    (P-18 / F07). A verdict inferred from free prose would be the motor judging;
    a header the skill writes is the motor reading. No header, no verdict:
    `unknown`, and the skill asks the owner instead of assuming.
    """
    files = sorted((eng / "_simulation").glob("revisit_*.md"))
    if not files:
        return {"present": False, "file": "", "decision": "", "target": "",
                "verdict": "", "when": ""}
    parsed = []
    for f in files:
        body = _read(f) or ""
        rec = {"present": True, "file": f.name,
               "decision": "", "target": "", "verdict": "unknown", "when": ""}
        for key, rx in REVISIT_FIELD_RE.items():
            m = rx.search(body)
            if m:
                rec[key] = m.group(1).upper() if key == "verdict" else m.group(1)
        parsed.append(rec)
    # Newest by declared timestamp; filename (which carries the date) breaks ties.
    parsed.sort(key=lambda r: (r["when"], r["file"]))
    return parsed[-1]


def blueprint_state(eng: Path, blocks: list[dict], rows: list[dict] | None = None,
                    pack: str = "") -> dict:
    """Versions, which one the business approved, and whether it covers the current one.

    Approval is read from `decisions.md` (blueprint-contract.md: approval IS a
    D-NNN block), never from an `approved:` field -- live blueprints leave it null.
    """
    d = eng / "_blueprint"
    diags: list[dict] = []
    empty = {"present": False, "versions": [], "current": None, "approved": None,
             "approved_valid": None, "latest_authorized": None,
             "approved_by": "", "approval_covers_current": None, "structural_open": [],
             "structural_open_count": 0, "proof_obligations": [], "diagnostics": diags}
    if not d.is_dir():
        return empty
    versions = []
    cfg = bp_pack_cfg(pack or _read_json(eng / "_state.json").get("pack", ""))
    su_ids = None if rows is None else {r["id"] for r in rows if r.get("id")}
    loader = bp_loader(eng)
    for p in sorted(d.iterdir()):
        if not (p.is_file() and BP_FILE_RE.match(p.name)):
            continue
        try:
            v = bp_read(p)
            # A3/A4 (runtime hardening): structure checked by code; a `block` issue makes
            # the version non-approvable and an existing approval of it non-consumable.
            v["issues"] = bp_validate(_read(p) or "", p.name, cfg, su_ids, loader)
            v["blocking"] = [i for i in v["issues"] if i["severity"] == "block"]
            v["valid"] = not v["blocking"]
            if any(i["code"] == "BP-YAML-MALFORMED" and i["path"] == "$"
                   and "ilegível" in i["message"] for i in v["issues"]):
                v["readable"] = False
            versions.append(v)
        except Exception as exc:                                      # noqa: BLE001
            diags.append({"level": "warn", "where": "_blueprint/" + p.name, "line": 0,
                          "message": "versão ilegível ({}) — verificação "
                                     "incompleta".format(type(exc).__name__)})
    if not versions:
        return empty | {"present": True, "diagnostics": diags}
    versions.sort(key=lambda v: v["version"])
    non_draft = [v for v in versions if not v["draft"]]
    current = non_draft[-1] if non_draft else versions[-1]
    approvals = [b for b in blocks if b["kind"] == "blueprint-approval"]
    approved, approved_by = None, ""
    if approvals:
        last = approvals[-1]
        want = last["blueprint_version"]
        for v in versions:
            if v["version"] == want:
                approved, approved_by = v, last["id"]
        if approved is None and want:
            diags.append({"level": "warn", "where": "decisions.md", "line": 0,
                          "message": "{} aprova {} e o ficheiro não existe em "
                                     "_blueprint/ — verificação incompleta".format(
                                         last["id"], want)})
    struct = list(current.get("structural_open") or [])
    # P-18 / F08: the Architecture Blueprint deliverable reads the latest AUTHORIZED
    # version and declares its approval state; approval stays the gate of the
    # Implementation Specification and the Claude Design Brief. Authorization and
    # human approval are distinct concepts and the model names both.
    authorized = [v for v in non_draft
                  if (v.get("authorization") or "").strip().lower()
                  in ("authorized", "authorized-bounded")]
    latest_auth = None
    if authorized:
        la = authorized[-1]
        n_struct = len(la.get("structural_open") or [])
        if approved and approved["version"] == la["version"]:
            la_state = "approved ({})".format(approved_by)
        elif n_struct:
            la_state = "not approved — {} structural choice(s) open".format(n_struct)
        else:
            la_state = "not approved — awaiting business approval"
        if not la.get("valid", True):
            la_state += " — invalid structure ({} blocking issue(s))".format(len(la.get("blocking") or []))
        latest_auth = {"version": la["version"], "rel": la["rel"],
                       "valid": la.get("valid", True),
                       "blocking": len(la.get("blocking") or []),
                       "approved": bool(approved and approved["version"] == la["version"]),
                       "approved_by": approved_by if (approved and approved["version"] == la["version"]) else "",
                       "structural_open_count": n_struct, "state": la_state}
    return {
        "present": True,
        "latest_authorized": latest_auth,
        "versions": [{"version": v["version"], "rel": v["rel"], "draft": v["draft"],
                      "authorization": v["authorization"],
                      "experience_mode": v["experience_mode"],
                      "open_choices": len(v["open_choices"]),
                      "structural_open": len(v["structural_open"]),
                      "valid": v.get("valid", True), "readable": v.get("readable", True),
                      "issues": len(v.get("issues") or []),
                      "blocking": len(v.get("blocking") or []),
                      "issue_codes": sorted({i["code"] for i in (v.get("issues") or [])})}
                     for v in versions],
        "current": current,
        "approved": approved,
        "approved_valid": (approved or {}).get("valid") if approved else None,
        "approved_by": approved_by,
        "approval_covers_current": bool(approved and
                                        approved["version"] == current["version"]),
        "structural_open": struct,
        "structural_open_count": len(struct),
        "proof_obligations": list(current.get("proof_obligations") or []),
        "diagnostics": diags,
    }


# ------------------------------------------------------- synthesis / render age
# Fixed 2026-09-07: approving a blueprint re-runs /synthesize, because
# architecture-story.md projects the APPROVED blueprint's architecture block
# (aisa-synthesize) and the auto-synthesis of /decide predates the blueprint.
# Timestamps come from the artefacts' own logs and from decisions.md -- never
# from file mtimes, which a copy or a checkout destroys.
#
# P-18 / F04 (2026-09-09): freshness is judged PER TOPIC, against the authorities
# that topic consumes (the kernel synthesis templates' `sources:`), never by the
# newest date of any topic. A fresh business-story cannot validate an old
# architecture-story. The architecture-story also carries the IDENTITY of the
# blueprint version it projected (`authority: _blueprint/ux-blueprint_vNN.yaml#
# architecture @ sha256:<block>`); a stamp -- or the version cited in the log line --
# that names another version than the approved one is stale whatever the clock says.
# A pack with no log entry is `desconhecido`: an absent log is never a positive claim.

SYNTH_TOPICS = ("business-story", "as-is", "architecture-story",
                "risks-and-assumptions", "financial-story")

# Mirror of library/kernel/synthesis-templates/<topic>.template.md `sources:` -- used
# ONLY when the template cannot be read (a diagnostic says so). The template is the
# contract; this keeps the motor from going blind when the library is not mounted.
SYNTH_SOURCES_FALLBACK = {
    "business-story": [
        "shared-understanding.md# lens=business (Confirmed + Assumed)",
        "lens-outputs/business.md", "frame.md", "decisions.md# D-001 (frame agreed)"],
    "as-is": [
        "shared-understanding.md# lens IN (operations, user)",
        "lens-outputs/operations.md", "lens-outputs/user.md"],
    "architecture-story": [
        "decisions.md# chosen option + selected solution + (scope, outcome) pairs",
        "_blueprint/ux-blueprint_v<NN>.yaml# architecture",
        "shared-understanding.md# lens IN (technology, data)",
        "lens-outputs/technology.md", "lens-outputs/data.md",
        "library/packs/<pack>/architecture-templates/architecture-core.md"],
    "risks-and-assumptions": [
        "shared-understanding.md# Risky (all) + Assumed (all) + Unknown (criticidade=Critical) + Conflicted (unresolved)",
        "shared-understanding.md# Confirmed (rows whose validade has EXPIRED)",
        "decisions.md# Accepted risks + Conditions + Preconditions + Proof obligations + Revision conditions from D-NNN"],
    "financial-story": [
        "shared-understanding.md# lens=financial", "lens-outputs/financial.md",
        "decisions.md# D-NNN — Conditions, Accepted risks, Revision conditions (economic anchors)"],
}

SYNTH_STAMP_RE = re.compile(
    r"authority:\s*_blueprint/ux-blueprint_v(\d{1,3})\.ya?ml#\s*architecture"
    r"(?:\s*@\s*(?:sha256:)?([0-9a-fA-F]{64}))?", re.I)
SYNTH_STATES = ("Confirmed", "Assumed", "Unknown", "Conflicted", "Risky")


def _iso_key(s: str) -> str:
    return (s or "").strip().replace(" ", "T")[:19]


def _after(a: str, b: str) -> bool:
    """Is `a` strictly after `b`? Both ISO. Where either side is a bare date the
    comparison is made on the day (the SU carries dates, not timestamps)."""
    a, b = _iso_key(a), _iso_key(b)
    if not a or not b:
        return False
    if len(a) <= 10 or len(b) <= 10:
        return a[:10] > b[:10]
    return a > b


def synthesis_template_sources(topic: str) -> tuple[list[str], str]:
    """The `sources:` list of the kernel synthesis template, read as text (no PyYAML).
    Returns (sources, basis) with basis `template` or `fallback`."""
    p = repo_root() / "library" / "kernel" / "synthesis-templates" / (topic + ".template.md")
    text = _read(p) or ""
    m = re.search(r"^sources:\s*\n((?:[ \t]+-[^\n]*\n)+)", text, re.M)
    if not m:
        return list(SYNTH_SOURCES_FALLBACK.get(topic, [])), "fallback"
    items = [re.sub(r"^\s*-\s*", "", ln).strip() for ln in m.group(1).splitlines()
             if ln.strip()]
    return items, "template"


def _synth_cited_version(text: str) -> str:
    m = re.search(r"ux-blueprint_v(\d{1,3})", text or "")
    return ("v" + m.group(1).zfill(2)) if m else ""


def synthesis_entries(log: str) -> list[dict]:
    """Every run recorded in _synthesis-log.md. Two shapes exist in real engagements:
    one line per topic (`<ts> — <topic> — ...`, the kernel's) and a `## Run N — <ts>`
    heading followed by a `| topic | ... |` table (dpt-galp-jp). Both are read; a
    topic token tolerates a suffix (`architecture-story (re-síntese, manual)`)."""
    entries: list[dict] = []
    run_ts = ""
    for raw in (log or "").splitlines():
        line = raw.strip()
        if not line:
            continue
        hm = re.match(r"^##\s+.*?" + TS_PAT, line)
        if hm:
            run_ts = hm.group(1)
            continue
        m = re.match(r"^" + TS_PAT + r"\s*[—–-]\s*(.+)$", line)
        if m:
            rest = m.group(2)
            tm = re.match(r"([a-z][a-z-]*)", rest)
            entries.append({"when": m.group(1), "topic": tm.group(1) if tm else "",
                            "detail": rest, "cited_version": _synth_cited_version(rest)})
            continue
        tm = re.match(r"^\|\s*([a-z][a-z-]*)\s*\|(.*)$", line)
        if tm and run_ts and tm.group(1) in SYNTH_TOPICS:
            entries.append({"when": run_ts, "topic": tm.group(1), "detail": tm.group(2),
                            "cited_version": _synth_cited_version(tm.group(2))})
    return entries


def synthesis_stamp(text: str) -> dict | None:
    """`authority: _blueprint/ux-blueprint_vNN.yaml#architecture @ sha256:<hex>` in the
    head of a topic pack (aisa-synthesize writes it; the sha is optional)."""
    m = SYNTH_STAMP_RE.search((text or "")[:6000])
    if not m:
        return None
    return {"version": "v" + m.group(1).zfill(2), "sha256": (m.group(2) or "").lower()}


def architecture_block_text(text: str) -> str:
    """The raw `architecture:` block of a blueprint file, presentation-normalised
    (CRLF, trailing spaces, trailing blank lines). Text, not YAML: an APPROVED
    version of pilot-1 does not parse, and identity must not depend on parsing."""
    lines = (text or "").replace("\r\n", "\n").split("\n")
    out: list[str] = []
    inside = False
    for ln in lines:
        if re.match(r"^architecture:\s*(#.*)?$", ln):
            inside = True
            out.append("architecture:")
            continue
        if inside:
            if ln.strip() and not ln[:1] in (" ", "\t"):
                break
            out.append(ln.rstrip())
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out)


def architecture_block_sha256(text: str) -> str:
    blk = architecture_block_text(text)
    return hashlib.sha256(blk.encode("utf-8")).hexdigest() if blk else ""


def _bp_file(eng: Path, version: str) -> Path | None:
    for ext in ("yaml", "yml"):
        p = eng / "_blueprint" / ("ux-blueprint_{}.{}".format(version, ext))
        if p.is_file():
            return p
    return None


def _su_authority(spec: str, rows: list[dict]) -> str:
    """Newest `verificado_em` among the SU rows a source clause names
    (`lens=business (Confirmed + Assumed)`, `lens IN (operations, user)`,
    `Risky (all) + Assumed (all) ...`). Day granularity -- the SU carries dates."""
    lenses: set[str] = set()
    m = re.search(r"lens\s*=\s*([A-Za-z]+)", spec)
    if m:
        lenses.add(m.group(1).lower())
    m = re.search(r"lens\s+IN\s*\(([^)]*)\)", spec, re.I)
    if m:
        lenses |= {t.strip().lower() for t in m.group(1).split(",") if t.strip()}
    states = {s for s in SYNTH_STATES if re.search(r"\b" + s + r"\b", spec)}
    best = ""
    for r in rows or []:
        if lenses and (r.get("lens") or "").strip().lower() not in lenses:
            continue
        if states and (r.get("state") or "").strip() not in states:
            continue
        v = (r.get("verificado_em") or "").strip()
        if v and v > best:
            best = v
    return best


def synthesis_state(eng: Path, blocks: list[dict], rows: list[dict] | None = None,
                    pack: str = "") -> dict:
    log = _read(eng / "_synthesis" / "_synthesis-log.md") or ""
    entries = synthesis_entries(log)
    sd = eng / "_synthesis"
    packs = sorted(p.name for p in sd.glob("*.md")
                   if p.is_file() and not p.name.startswith("_")) if sd.is_dir() else []
    last_any = max((_iso_key(e["when"]) for e in entries), default="")
    approvals = [b for b in blocks if b["kind"] == "blueprint-approval"]
    appr = approvals[-1] if approvals else None
    appr_ts = _iso_key((appr or {}).get("when", ""))
    appr_v = (appr or {}).get("blueprint_version", "")
    appr_file = _bp_file(eng, appr_v) if appr_v else None
    appr_sha = architecture_block_sha256(_read(appr_file) or "") if appr_file else ""
    appr_bp = blueprint_state(eng, blocks, rows) if appr_v else {}
    appr_valid = (appr_bp.get("approved") or {}).get("valid", True) if appr_v else True
    appr_blocking = len((appr_bp.get("approved") or {}).get("blocking") or []) if appr_v else 0
    dec_ts = max((_iso_key(b.get("when", "")) for b in blocks if b.get("when")), default="")
    diags: list[dict] = []
    topics: dict[str, dict] = {}
    for topic in SYNTH_TOPICS:
        sources, basis = synthesis_template_sources(topic)
        if basis == "fallback":
            diags.append({"level": "info", "where": "library/kernel/synthesis-templates",
                          "line": 0,
                          "message": "{}.template.md ilegível — autoridades lidas do espelho "
                                     "interno do motor".format(topic)})
        runs = [e for e in entries if e["topic"] == topic]
        last_entry = max(runs, key=lambda e: _iso_key(e["when"])) if runs else None
        last = _iso_key(last_entry["when"]) if last_entry else ""
        present = (topic + ".md") in packs
        text = (_read(sd / (topic + ".md")) or "") if present else ""
        stamp = synthesis_stamp(text) if present else None
        authorities: list[dict] = []
        reasons: list[str] = []
        comparable = 0
        for spec in sources:
            s = spec.strip()
            if s.startswith("_blueprint/"):
                kind, when = "blueprint-approval", appr_ts
            elif s.startswith("shared-understanding.md"):
                kind, when = "su", _su_authority(s, rows or [])
            elif s.startswith("decisions.md"):
                kind, when = "decisions", dec_ts
            else:
                kind, when = "sem carimbo", ""
            authorities.append({"source": s, "kind": kind, "when": when})
            if kind == "sem carimbo" or not when:
                continue
            comparable += 1
            if last and _after(when, last):
                reasons.append("{}: autoridade {} posterior à síntese {}".format(kind, when, last))
        identity = "n/a"
        if topic == "architecture-story" and appr_v:
            cited = (stamp or {}).get("version") or (last_entry or {}).get("cited_version", "")
            if appr_valid is False:
                identity = "invalid"
                reasons.append("identidade: a versão aprovada {} falha a estrutura ({} bloqueio(s)) "
                               "— a aprovação não é consumível (blueprint-contract.md → "
                               "Validação estrutural)".format(appr_v, appr_blocking))
            elif not cited:
                identity = "sem carimbo"
            elif cited != appr_v:
                identity = "mismatch"
                reasons.append("identidade: sintetizado de {}, aprovada {}".format(cited, appr_v))
            elif stamp and stamp.get("sha256") and appr_sha and stamp["sha256"] != appr_sha:
                identity = "mismatch"
                reasons.append("identidade: o bloco architecture de {} mudou desde a síntese "
                               "(sha256 difere)".format(appr_v))
            else:
                identity = "match"
        if not present:
            verdict = "missing"
        elif not last:
            verdict = "desconhecido"
        elif reasons:
            verdict = "stale"
        else:
            verdict = "fresh"
        topics[topic] = {
            "present": present, "last_run": last, "runs": len(runs),
            "sources_basis": basis, "authorities": authorities, "comparable": comparable,
            "stamp": stamp, "identity": identity, "reasons": reasons, "verdict": verdict,
            "julgamento": ("sem registo em _synthesis-log.md: nada se afirma" if present and not last
                           else "ficheiro ausente" if not present
                           else "nenhuma autoridade com carimbo posterior à síntese" if not reasons and comparable
                           else "nenhuma autoridade com carimbo para comparar — fresco por ausência de "
                                "contra-evidência, não por verificação" if not reasons
                           else "; ".join(reasons)),
        }
    stale_topics = [t for t in SYNTH_TOPICS if topics[t]["verdict"] == "stale"]
    unknown_topics = [t for t in SYNTH_TOPICS if topics[t]["verdict"] in ("desconhecido", "missing")]
    arch = topics["architecture-story"]
    if appr and arch["last_run"]:
        stale_vs_approval = any(r.startswith(("blueprint-approval", "identidade")) for r in arch["reasons"])
    else:
        stale_vs_approval = None
    verdict = "stale" if stale_topics else ("desconhecido" if unknown_topics else
                                             ("fresh" if packs else "ausente"))
    return {
        "present": bool(packs),
        "packs": packs,
        "log_entries": entries,
        "last_run": last_any,
        "approval_id": (appr or {}).get("id", ""),
        "approval_when": appr_ts,
        "approval_version": appr_v,
        "approval_block_sha256": appr_sha,
        "topics": topics,
        "stale_topics": stale_topics,
        "unknown_topics": unknown_topics,
        "verdict": verdict,
        # architecture-story vs the blueprint approval (time OR identity); None without an
        # approval or without a logged run. Kept for consumers written against 1.6.x.
        "stale_vs_approval": stale_vs_approval,
        "diagnostics": diags,
        "note": ("frescura por tópico, contra as autoridades que cada tópico consome "
                 "(synthesis-templates sources) — um tópico fresco não valida outro; "
                 "architecture-story compara também a identidade da versão aprovada"),
    }


def render_state(eng: Path, bp: dict, syn: dict) -> dict:
    log = _read(eng / "_render" / "render-log.md") or ""
    runs = [{"when": m.group(1), "label": m.group(2).strip()} for m in
            re.finditer(r"^##\s+" + TS_PAT + r"\s*[—–-]\s*(.+)$", log, flags=re.M)]
    last_run = max((_iso_key(r["when"]) for r in runs), default="")
    appr_ts = syn.get("approval_when") or ""
    cur = (bp.get("current") or {}).get("version") or ""
    appr_v = (bp.get("approved") or {}).get("version") or ""
    return {
        "versions": render_versions(eng),
        "gaps": parse_render_gaps(eng),
        "gap_count": len(parse_render_gaps(eng)),
        "runs": runs, "last_run": last_run,
        "skip_mentions": len(re.findall(r"\bskip\b", log, flags=re.I)),
        "stale_vs_approval": (last_run < appr_ts) if (last_run and appr_ts) else None,
        "renders_blueprint_version": appr_v,
        "current_blueprint_version": cur,
        "behind_current_blueprint": bool(cur and appr_v and cur != appr_v),
    }


# ------------------------------------------------------- cobertura (coverage-contract.md)
# The coverage engine lives next door in `coverage.py`, and it reads THIS module through its
# ReaderAdapter. Importing it at the top of this file would recurse; loading it on demand and
# handing it our own globals as the reader module does not. Everything below is READ-ONLY: the
# model never finalizes a review, never writes a record, and never records an approval.
#
# Cost: a full inventory is ~0.3-1 s. An engagement with no record in `_coverage/` pays none of
# it -- with nothing to compare the denominator against, `not_evaluated` IS the whole answer
# (coverage-contract.md §10). That is also what keeps the on-su-change hook cheap.

_COVERAGE_MOD: dict | None = None
_COVERAGE_ERR = ""


def coverage_module() -> dict | None:
    """`coverage.py`'s globals, loaded once; None with the reason in `_COVERAGE_ERR`."""
    global _COVERAGE_MOD, _COVERAGE_ERR
    if _COVERAGE_MOD is None and not _COVERAGE_ERR:
        import runpy
        path = Path(__file__).resolve().parent / "coverage.py"
        if not path.is_file():
            _COVERAGE_ERR = "coverage.py não está em library/kernel/tools/"
            return None
        try:
            _COVERAGE_MOD = runpy.run_path(str(path))
        except Exception as exc:                                        # noqa: BLE001
            _COVERAGE_ERR = "{}: {}".format(type(exc).__name__, exc)
            return None
    return _COVERAGE_MOD


COVERAGE_UNEVALUATED = {
    "contract_validity": "not_evaluated", "freshness": "not_evaluated",
    "source_review": "not_evaluated", "semantic_review": "not_evaluated",
    "coverage": "not_evaluated", "eligible": False,
}


def _coverage_stage(C, eng: Path, stage: str, target: dict | None, readers,
                    inventory: dict | None = None) -> dict:
    """One stage's verdicts, trimmed for the model.

    Never raises, and never returns a pass it did not compute: an engine failure comes back
    as `not_evaluated` with its reason (coverage-contract.md §8, `COV-UNEXPECTED`) -- a check
    that did not run is not a check that passed."""
    out = {"stage": stage, "target": (target or {}).get("file", ""), "record": None,
           "record_version": "", "error": "", "reasons": [], "gaps": [], "gap_count": 0,
           "codes": [], "diagnostics": [], "limitations": [], "superseded": [],
           "action": ""}
    out.update(COVERAGE_UNEVALUATED)
    try:
        res = C["coverage_state"](eng, stage, target, readers, inventory=inventory)
    except Exception as exc:                                            # noqa: BLE001
        out["error"] = "{}: {}".format(type(exc).__name__, exc)
        out["reasons"] = ["verificação incompleta — o motor de cobertura falhou: "
                          + out["error"]]
        return out
    for k in ("contract_validity", "freshness", "source_review", "semantic_review",
              "coverage", "eligible", "action"):
        if k in res:
            out[k] = res[k]
    rec = res.get("record") or {}
    out["record"] = rec.get("file") or None
    out["record_version"] = rec.get("version") or ""
    out["reasons"] = list(res.get("reasons") or [])
    out["gaps"] = list(res.get("gaps") or [])
    out["gap_count"] = len(out["gaps"])
    out["limitations"] = list(res.get("limitations") or [])
    out["superseded"] = list(res.get("superseded") or [])
    out["diagnostics"] = [{"code": d.get("code", ""), "severity": d.get("severity", ""),
                           "message": d.get("message", ""), "item": d.get("item", ""),
                           "file": d.get("file", ""), "resolves": d.get("resolves", "")}
                          for d in (res.get("diagnostics") or [])]
    out["codes"] = sorted({d["code"] for d in out["diagnostics"] if d["code"]})
    return out


def coverage_status(eng: Path, bp: dict, pack: str = "") -> dict:
    """`status.coverage` — the fourth dimension, beside blueprint, synthesis and render.

    It answers FOUR questions separately and never mixes them (coverage-contract.md §1):

      structure — does the version parse and satisfy the blueprint contract? (`bp_validate`)
      coverage  — did a declared review treat every obligation, and is that review current?
      approval  — did the business approve THIS version? (a `D-NNN` block, nothing else)
      e2e       — was the solution proved end to end? Never from here: `not_evaluated`.

    A valid structure never meant a covered design — that is the whole finding this dimension
    carries — and a complete coverage never meant an approval.
    """
    out = {
        "present": False, "records": [], "engine": "ok", "engine_error": "",
        "stages": {}, "readiness": {"structure": "not_evaluated",
                                    "coverage": "not_evaluated",
                                    "approval": "absent", "e2e": "not_evaluated"},
        "approve_eligible": None, "produce_eligible": None, "blockers": [],
        "limitations": [], "diagnostics": [], "julgamento": "",
    }
    C = coverage_module()
    if C is None:
        out["engine"] = "absent"
        out["engine_error"] = _COVERAGE_ERR
        out["julgamento"] = ("motor de cobertura indisponível ({}) — verificação "
                             "incompleta, nunca «sem lacunas»".format(_COVERAGE_ERR))
        return out

    # --- the answers that do not need the engine -----------------------------------
    cur = bp.get("current") or {}
    appr = bp.get("approved") or {}
    if cur:
        out["readiness"]["structure"] = ("invalid" if cur.get("valid") is False
                                         else "valid" if cur.get("valid") else
                                         "not_evaluated")
        out["readiness"]["current_version"] = cur.get("version", "")
    if appr:
        same = appr.get("version") == cur.get("version")
        out["readiness"]["approval"] = "approved" if same else "approved-other-version"
        out["readiness"]["approved_version"] = appr.get("version", "")
        out["readiness"]["approved_by"] = bp.get("approved_by", "")

    try:
        records = C["load_records"](eng, pack or None)
    except Exception as exc:                                            # noqa: BLE001
        out["engine"] = "error"
        out["engine_error"] = "{}: {}".format(type(exc).__name__, exc)
        out["julgamento"] = ("não foi possível ler `_coverage/` ({}) — verificação "
                             "incompleta".format(out["engine_error"]))
        return out

    out["records"] = [{"file": e["file"], "version": e["version"], "state": e["state"],
                       "stage": ((e["record"] or {}).get("stage") or ""),
                       "target": (((e["record"] or {}).get("target") or {}).get("file", "")
                                  if isinstance((e["record"] or {}).get("target"), dict)
                                  else "")}
                      for e in records]
    out["present"] = bool(records)
    if not records:
        # coverage-contract.md §10: no record is `not_evaluated` — never "complete", never
        # "retroactively failed". A historical approval keeps standing, and says so.
        out["julgamento"] = ("sem revisão de cobertura registada — não avaliado; não é "
                             "aprovação nem reprovação, e não revoga aprovação nenhuma")
        return out

    readers = C["ReaderAdapter"](module=globals())
    # One denominator for both stages: `build_inventory` does not depend on the stage
    # (the stage only shapes the basis), and building it twice doubled the cost of every
    # dashboard regeneration for nothing.
    try:
        inv = C["build_inventory"](eng, readers)
    except Exception as exc:                                            # noqa: BLE001
        # Each stage then builds (and fails on) its own, and reports the reason. The flag
        # is set here so the model never reads "engine ok" beside an engine error.
        inv = None
        out["engine"] = "error"
        out["engine_error"] = "{}: {}".format(type(exc).__name__, exc)
    out["stages"]["reconciliation"] = _coverage_stage(C, eng, "reconciliation", None,
                                                      readers, inv)
    rel = cur.get("rel") or ""
    if rel:
        try:
            target = {"file": rel, "identity": C["target_identity"](eng, "blueprint", rel)}
        except Exception:                                               # noqa: BLE001
            target = {"file": rel}
        st = _coverage_stage(C, eng, "blueprint", target, readers, inv)
        st["version"] = cur.get("version", "")
        out["stages"]["blueprint"] = st

    bpst = out["stages"].get("blueprint") or {}
    recon = out["stages"].get("reconciliation") or {}
    if bpst:
        out["readiness"]["coverage"] = (
            "stale" if bpst["freshness"] == "stale"
            else bpst["contract_validity"]
            if bpst["contract_validity"] in ("invalid", "unsupported")
            else bpst["coverage"])
        # The engine already refuses a version whose structure fails (§8.1.4). Recombining
        # the two here would hide which of them said no, so the blocker is named, not merged.
        out["approve_eligible"] = bool(bpst["eligible"]) and \
            out["readiness"]["structure"] != "invalid"
        # Each blocker says WHICH of the two stages raised it. Without the prefix the
        # same sentence appeared twice, from two stages, and named neither.
        if not bpst["eligible"]:
            out["blockers"] += ["revisão do desenho: " + r for r in bpst["reasons"]]
    if out["readiness"]["structure"] == "invalid":
        out["blockers"].append("A estrutura desta versão do desenho falha a verificação do "
                               "contrato — por si só já impede a aprovação "
                               "(blueprint-contract.md → Validação estrutural).")
    if recon:
        out["produce_eligible"] = bool(recon["eligible"])
        if not recon["eligible"]:
            out["blockers"] += ["reconciliação das fontes: " + r for r in recon["reasons"]]
    for st in out["stages"].values():
        out["limitations"] += [l for l in st["limitations"] if l not in out["limitations"]]
        out["diagnostics"] += st["diagnostics"]

    out["julgamento"] = (
        "cobertura revista é uma declaração do revisor verificada na forma, nunca correcção "
        "garantida por código; estrutura, cobertura, aprovação e ponta-a-ponta são quatro "
        "perguntas separadas e esta responde só à segunda. `approve_eligible` diz que a "
        "versão PODE ser levada ao negócio, nunca que o negócio aprovou")
    if out["engine"] != "ok":
        out["julgamento"] = ("verificação incompleta — {} ({}); o que está abaixo é o que se "
                             "conseguiu calcular, e não é «sem lacunas»"
                             .format(out["engine"], out["engine_error"]))
    return out


def simulation_coherence(eng: Path, rows: list[dict]) -> list[dict]:
    """Mechanical staleness of each simulation: the SU ids it cites that have
    since been resolved, expired or disappeared. Not a judgement about value."""
    d = eng / "_simulation"
    if not d.is_dir():
        return []
    index = {r["id"]: r for r in rows}
    out = []
    for p in sorted(d.glob("options-comparison_v*.md")):
        cited = sorted(set(ID_RE.findall(_read(p) or "")))
        resolved = [i for i in cited if i in index and index[i]["resolved"]]
        expired = [i for i in cited if i in index and index[i]["expired"]]
        absent = [i for i in cited if i not in index]
        out.append({"file": p.name, "rel": "_simulation/" + p.name, "cited": cited,
                    "cited_resolved": resolved, "cited_expired": expired,
                    "cited_absent": absent,
                    "stale": bool(resolved or expired or absent)})
    return out


# ------------------------------------------------------------- who answers this
# `quem responde` mixes real people with council persona names. A persona is a
# lens, not somebody who can be asked -- surfacing one as the owner would invent
# a responsible party. Split; never guess.
#
# F1.1/F1.2: what a lens writes there now carries a PREFIX -- `role: <role>` or
# `fonte: <artefact/system>`. This function reads the prefix and nothing else. It
# does NOT decide whether unprefixed free text names a role, a source or a person:
# that is judgement, and the adversarial review rejected asking code for it. A part
# with no prefix goes where it always went and is reported verbatim in `raw`.

PERSONA_NAMES = {"business-analyst", "operations-lead", "user-advocate", "data-steward",
                 "compliance-officer", "cfo-lens", "solution-architect", "chairman",
                 "chair", "council"}
UNASSIGNED_TOKENS = {"", "-", "n/a", "na", "tbd", "por atribuir", "not named",
                     "not recorded", "not specified", "unknown", "?"}
_PERSONA_KEYS = {norm_key(x) for x in PERSONA_NAMES}
_UNASSIGNED_KEYS = {norm_key(x) for x in UNASSIGNED_TOKENS}

# The closed set of prefixes, exactly as F1.1 fixed them: `role:` for the role that owes
# the answer, `fonte:` for the artefact or system to consult. Adding a spelling is a
# semantic decision this file may not take -- every writer is pointed at
# `library/kernel/states.md` for the single spelling of each.
OWNER_ROLE_KINDS = {"role"}
OWNER_PREFIX_RE = re.compile(r"^(?P<kind>role|fonte)\s*:\s*(?P<value>.+)$", re.I)
# Used ONLY to find prefixes inside a compound cell (see `split_owner`). Never used to
# build `humans`, so widening it cannot change what an older row parsed to.
OWNER_SPLIT_RE = re.compile(r"\s*(?:·|/|\+|,|;| e | and )\s*")


def split_owner(raw: str) -> dict:
    """`quem responde` / `owner` -> {raw, humans, personas, unassigned, role, source}.

    `role` and `source` are filled FROM THE PREFIX and from nothing else. `humans` and
    `unassigned` keep their old meaning to the byte, so an engagement written before the
    prefix produces exactly the `/status` it produced before (F3): `humans` is every part
    that is not a council persona -- a prefixed part included, because it is still a party
    that owes the answer -- and `unassigned` still means nobody owes it.
    """
    s = (raw or "").strip()
    if norm_key(s) in _UNASSIGNED_KEYS:
        return {"raw": s, "humans": [], "personas": [], "unassigned": True,
                "role": [], "source": []}
    parts = [p.strip() for p in re.split(r"\s*(?:/|\+|,|;| e | and )\s*", s) if p.strip()]
    humans, personas = [], []
    for p in parts:
        (personas if norm_key(p) in _PERSONA_KEYS else humans).append(p)

    # Prefix extraction is a SECOND pass over the same cell, deliberately separate from
    # the split above. A compound cell separates its parts with the pack's own list
    # separator (`·`) as often as with `/`, and adding `·` to the split would change
    # `humans` on rows written before any of this -- so it stays out of the split and
    # enters only here, where it can add a `role`/`source` and can subtract nothing.
    roles, sources = [], []
    for p in re.split(OWNER_SPLIT_RE, s):
        m = OWNER_PREFIX_RE.match(p.strip())
        if not m:
            continue
        value = m.group("value").strip()
        if value:
            (roles if m.group("kind").lower() in OWNER_ROLE_KINDS
             else sources).append(value)
    return {"raw": s, "humans": humans, "personas": personas,
            "unassigned": not humans, "role": roles, "source": sources}


# ------------------------------------------------------------ one item per SU id
# STATUS_IMPROVEMENT_PLAN section 3: the grouping key is the SU id, decided here
# so the skill never has to judge what counts as "the same subject".

def su_items(rows: list[dict], agenda: dict, bp: dict, tw: dict,
             options_md: str, decisions_md: str) -> list[dict]:
    index = {r["id"]: r for r in rows}
    hits: dict[str, dict] = {}

    def touch(rid: str) -> dict | None:
        r = index.get(rid)
        if r is None or r["resolved"]:
            return None
        return hits.setdefault(rid, {
            "id": rid, "state": r["state"], "lens": r["lens"],
            "criticidade": r["criticidade"], "custo": r["custo"],
            "swing_class": r["swing_class"], "swing_text": r["swing_text"],
            "expired": r["expired"], "claim": r["claim"],
            # `quem responde` (Unknown) and `partes` (Conflicted) both alias to
            # `support`; on Confirmed/Assumed/Risky that column is evidence, not an
            # owner, so it must never be read as one.
            "owner": (split_owner(r["support"])
                      if r["state"] in ("Unknown", "Conflicted")
                      else {"raw": "", "humans": [], "personas": [],
                            "unassigned": True, "role": [], "source": []}),
            "obligations": [], "agenda": "", "blocks_approval": False, "cited_by": [],
        })

    # Seed from EVERY material open row, not from agenda placement: meeting_agenda()
    # is built from Unknowns alone, so seeding from it silently dropped every open
    # Critical `Conflicted` row -- a material blocker the view must never lose.
    # Same definition of "material" that read_to_resume() uses.
    for r in rows:
        if r["resolved"]:
            continue
        if r["criticidade"] == "Critical" or r["expired"] or r["state"] == "Risky":
            touch(r["id"])

    for bucket, items in (agenda or {}).items():
        for a in items:
            it = touch(a["id"])
            if it:
                it["agenda"] = bucket

    cur_rel = (bp.get("current") or {}).get("rel", "_blueprint")
    for c in (bp.get("structural_open") or []):
        for rid in c["su_refs"]:
            it = touch(rid)
            if it is None:
                continue
            it["blocks_approval"] = True
            it["obligations"].append({
                "kind": "structural-choice", "what": c["choice"],
                "closes_when": c["would_be_settled_by"],
                "owner": split_owner(c["owner"]),
                "source": cur_rel + "#architecture.open_architecture_choices",
                "rule": "blueprint-contract.md regra 5 — bloqueia aprovação, nunca a "
                        "produção da versão",
            })

    for q in (bp.get("proof_obligations") or []):
        # `claim` and `method` say what the proof settles; `owner` cites ids only
        # to identify a team ("IT centralizado (C-063)"). Scanning owner pulled
        # Confirmed evidence rows in as if they were open work.
        blob = " ".join(str(q.get(k) or "") for k in ("claim", "method"))
        for rid in sorted(set(ID_RE.findall(blob))):
            # A free-text scan seeds only a row that can still be acted on. A
            # proof cites Confirmed facts as the SPEC of what to prove; those are
            # not open work. A declared `su_ref` above is different -- it is the
            # anchor the choice hangs on, whatever its state.
            r0 = index.get(rid)
            if r0 is None or (rid not in hits and r0["state"] not in
                              ("Unknown", "Conflicted", "Risky") and not r0["expired"]):
                continue
            it = touch(rid)
            if it is None:
                continue
            it["obligations"].append({
                "kind": "proof-obligation", "what": q["claim"], "closes_when": q["method"],
                "owner": split_owner(q["owner"]), "level": q["level"],
                "funded": q["funded"],
                "source": cur_rel + "#architecture.proof_obligations",
            })

    for t in (tw.get("items") or []):
        for rid in t["resolvable_ids"]:
            it = touch(rid)
            if it:
                it["cited_by"].append("{} ({})".format(t["tw"], t["decision"]))

    # A row the current phase artefact cites is material (plan section 4), so a
    # citation seeds too -- but only for a state that can still block: a Confirmed
    # row cited in a justification is not something that "falls to advance", and
    # decisions.md cites dozens of them. Expired Confirmed/Assumed already seeded.
    for label, md in (("options.md", options_md), ("decisions.md", decisions_md)):
        for rid in sorted(set(ID_RE.findall(md or ""))):
            r = index.get(rid)
            if r is None or r["resolved"]:
                continue
            if rid not in hits and r["state"] not in ("Unknown", "Conflicted", "Risky"):
                continue
            it = touch(rid)
            if it:
                it["cited_by"].append(label)

    for it in hits.values():
        it["cited_by"] = sorted(set(it["cited_by"]))
        # section 3: pre-blueprint the SU carries no closure-criterion column.
        # Say so with the swing phrase instead of inventing a criterion.
        obl = next((o for o in it["obligations"] if o.get("closes_when")), None)
        if obl:
            it["closes_when"] = obl["closes_when"]
            it["closes_when_substitute"] = ""
            it["closes_when_source"] = obl["source"]
        elif it["swing_text"]:
            it["closes_when"] = ""
            it["closes_when_substitute"] = "{}: {}".format(it["swing_class"],
                                                           it["swing_text"])
            it["closes_when_source"] = "swing (critério formal por definir)"
        else:
            # A pre-v2.3 SU has no swing column, so there is no substitute either.
            # Blank would read as "nothing to close"; name the absence instead.
            it["closes_when"] = ""
            it["closes_when_substitute"] = ""
            it["closes_when_source"] = ("critério por definir — sem critério registado "
                                        "e sem swing na SU")

    order = {"Critical": 0, "Med": 1, "Low": 2, "": 3}
    return sorted(hits.values(), key=lambda i: (
        not i["blocks_approval"], order.get(i["criticidade"], 3),
        SWING_ORDER.get(i["swing_class"], 3), i["id"]))


# ------------------------------------------------------------ milestone + action
# STATUS_IMPROVEMENT_PLAN section 5.1, as a table. Replaces the fixed
# phase -> command map, which sent a Decision engagement to `/render --all`
# while its blueprint sat unapproved with four structural choices open.

# Which command produces each artefact a phase expects. Naming `/resume` here
# would send the user back to this same view -- a loop, not a next step.
PRODUCED_BY = {
    "frame.md": "/frame",
    "options.md": "/options",
    "decisions.md": "/decide",
    "_synthesis/business-story.md": "/synthesize",
}


def milestone(eng: Path, state: dict, health: dict, critical: list[dict],
              artefacts: list[dict], bp: dict, syn: dict, decisions: list[dict],
              items: list[dict], frame_id: dict | None = None) -> dict:
    phase = norm_key(state.get("phase", ""))
    missing = [a["name"] for a in artefacts if not a["exists"]]
    kinds = {b["kind"] for b in decisions}
    # su_items() is already ordered by blocks-approval -> criticidade -> swing, so
    # the ids named here are the ones priority picked, not the head of an id sort.
    crit_ids = ([i["id"] for i in items if i["criticidade"] == "Critical"]
                or [c["id"] for c in critical])

    def out(marco, text, command, blocking=None):
        return {"phase": phase, "marco": marco, "text": text, "command": command,
                "blocking": blocking or [], "critical_open": len(critical)}

    if missing:
        cmd = " → ".join(dict.fromkeys(PRODUCED_BY.get(n, "/resume") for n in missing))
        return out("completar a fase {} — artefacto esperado em falta".format(phase or "?"),
                   "A fase está marcada em `_state.json` mas {} não existe: a ronda não "
                   "produziu o seu artefacto.".format(", ".join(missing[:3])),
                   cmd, missing[:3])

    if phase == "discovery":
        if critical:
            cmd = " ".join('/answer {} "..."'.format(i) for i in crit_ids[:2])
            return out("critérios de saída de Discovery (phases.md)",
                       "{} itens Critical abertos (Unknown/Conflicted). Resolver com o "
                       "sponsor antes de /frame.".format(len(critical)), cmd, crit_ids)
        return out("critérios de saída de Discovery (phases.md)",
                   "Sem itens Critical abertos.", "/frame")

    if phase == "framing":
        # P-18: "an approval exists" is not "this sentence is approved". The verdict
        # carries which of the two it is; the id is no longer assumed to be D-001.
        verdict = (frame_id or {}).get("verdict", "")
        latest_id = ((frame_id or {}).get("latest") or {}).get("id", "")
        if verdict == "no-frame" or "frame" not in kinds and verdict in ("", "none"):
            return out("frase do problema confirmada pelo dono do processo",
                       "A frase do problema ainda não foi aprovada — a aprovação "
                       "fica registada como uma decisão própria (D-NNN).",
                       "validar a frase do problema e registar a aprovação (D-NNN)")
        if verdict == "mismatch":
            return out("aprovar a frase do problema actual",
                       "A frase mudou desde a última aprovação ({}): a versão actual "
                       "ainda não foi aprovada.".format(latest_id or "—"),
                       "aprovar a frase actual (novo D-NNN) ou refazer com `/frame`")
        if verdict == "legacy":
            return out("confirmar a frase aprovada",
                       "A aprovação existente ({}) é anterior à regra da impressão "
                       "digital: não é possível verificar que aprova esta "
                       "frase.".format(latest_id or "—"),
                       "confirmar a frase com o dono e registar a aprovação (D-NNN)")
        return out("passagem a Options", "Frase do problema aprovada.", "/options")

    if phase == "options":
        return out("decisão registada",
                   "Opções na mesa. {} itens Critical abertos.".format(len(critical)),
                   "/simulate → /premortem → /decide", crit_ids)

    if phase == "decision":
        if "solution" not in kinds:
            return out("decisão registada",
                       "Fase decision sem decisão-solução em decisions.md.", "/decide")
        if not bp.get("present"):
            txt = _read(eng / "_synthesis" / "architecture-story.md") or ""
            if re.search(r"not-authorized|n[ãa]o autorizad", txt, re.I):
                return out("entregas aplicáveis",
                           "Arquitectura não autorizada (portadora: "
                           "_synthesis/architecture-story.md). Ausência de blueprint é "
                           "o resultado por contrato, não uma falha.", "/render --all")
            return out("primeira versão do blueprint",
                       "Arquitectura autorizada e sem blueprint produzido.", "/blueprint")
        cur = (bp.get("current") or {}).get("version", "")
        struct = bp.get("structural_open") or []
        if not bp.get("approval_covers_current"):
            appr = (bp.get("approved") or {}).get("version", "")
            marco = "aprovar blueprint {}".format(cur)
            if appr:
                marco += " — {} aprovada em {} não cobre {}".format(
                    appr, bp.get("approved_by", ""), cur)
            if struct:
                want = {r for c in struct for r in c["su_refs"]}
                ids = ([i["id"] for i in items if i["id"] in want]
                       or sorted(want))
                cmd = " ".join('/answer {} "..."'.format(i) for i in ids[:2])
                return out(marco,
                           "{} escolha(s) estrutural(is) aberta(s) bloqueiam a aprovação "
                           "(blueprint-contract.md regra 5); a revisão da versão não "
                           "está bloqueada.".format(len(struct)),
                           cmd + " → /blueprint --refresh", ids)
            return out(marco, "Sem escolhas estruturais abertas — falta a aprovação do "
                              "negócio.", "registar aprovação de " + cur)
        # P-18 / F04: per topic. One fresh topic never validates the others; a pack
        # without a log entry is unknown, and unknown is never "posterior à aprovação".
        stale = list(syn.get("stale_topics") or [])
        unknown = [t for t in (syn.get("unknown_topics") or []) if t not in stale]
        if stale or unknown:
            names = stale + unknown
            cmd = "/synthesize" if len(names) > 1 else "/synthesize " + names[0]
            if stale:
                why = "; ".join("{} — {}".format(
                    t, ((syn.get("topics") or {}).get(t) or {}).get("reasons", ["?"])[0])
                    for t in stale[:3])
                txt = "Resumos anteriores à autoridade que consomem: " + why
                if unknown:
                    txt += ". Sem registo de produção: " + ", ".join(unknown)
                return out("re-síntese dos resumos desactualizados", txt + ".", cmd, names)
            return out("verificação incompleta — resumos sem registo de produção",
                       "Sem entrada em _synthesis-log.md para: {}. Não se afirma que a "
                       "síntese é posterior à aprovação.".format(", ".join(unknown)),
                       cmd, unknown)
        return out("entregas", "Blueprint {} aprovado ({}); os {} resumos por tema são "
                               "posteriores às autoridades que consomem.".format(
                                   cur, bp.get("approved_by", ""),
                                   len(syn.get("topics") or {}) or 5),
                   "/render --all")

    if health.get("expired"):
        return out("revalidação",
                   "{} rows Confirmed/Assumed expiradas ({}% de saúde epistémica)."
                   .format(health["expired"], health["pct"]), "/status")
    return out("?", "Fase '{}' não reconhecida.".format(phase or "?"), "/status")


# ------------------------------------------------------------- read to resume
# aisa-status step 8b, computed here so `/status` and `/resume` cannot drift.
# The decision/architecture line gains options.md and answers.md: the Step 8D
# revisit needed both to revalidate a Decision basis and neither was listed.

READ_TO_RESUME = {
    "discovery": [
        ("_state.json", "etapa, passagem, tipo de solução"),
        ("context.json", "pedido literal e requerente"),
        ("shared-understanding.md", "linhas em aberto, as graves primeiro"),
        ("_capture/evidence-index.md", "o que falhou ao ler os ficheiros"),
        ("_capture/process-model.md", "§4 síntese do processo + §6 perguntas que os ficheiros levantaram"),
    ],
    "framing": [
        ("_state.json", "etapa, passagem"),
        ("shared-understanding.md", "linhas materiais"),
        ("_capture/process-model.md", "§4 síntese do processo"),
        ("frame.md", "a frase do problema, se já houve passagem"),
        ("decisions.md", "a frase acordada (D-001), se já registada"),
    ],
    "options": [
        ("_state.json", "etapa, passagem"),
        ("frame.md", "a frase e o que tem de sobreviver até às alternativas"),
        ("shared-understanding.md", "linhas materiais"),
        ("options.md", "as alternativas, se já houve passagem"),
    ],
    "decision-pre-blueprint": [
        ("_state.json", "etapa, passagem"),
        ("decisions.md", "a escolha, as suas condições e as condições de revisão"),
        ("options.md", "a alternativa escolhida e os pontos fortes que a escolha cita"),
        ("shared-understanding.md", "linhas materiais"),
        ("_synthesis/", "os resumos por tema"),
    ],
    "decision-architecture": [
        ("_state.json", "etapa, passagem"),
        ("decisions.md", "a escolha e as aprovações do desenho dos ecrãs"),
        ("_blueprint/", "versão actual (+ as versões que ela referencia)"),
        ("_blueprint/blueprint-log.md", "última entrada e o que foi revisto"),
        ("options.md", "pontos fortes da alternativa escolhida — o que se revê quando a base da escolha muda"),
        ("answers.md", "resposta tal e qual, por pergunta — o registo guarda o facto extraído, não a resposta"),
        ("_synthesis/architecture-story.md", "o que sustenta a arquitectura autorizada"),
        ("shared-understanding.md", "linhas materiais"),
    ],
    "deliverables": [
        ("library/kernel/render-contract.md", "autoridades mais próximas"),
        ("_render/render-gaps.md", "lacunas por fechar"),
        ("_render/render-log.md", "execuções, não aplicáveis e bloqueios"),
    ],
}


def read_to_resume(state: dict, bp: dict, rows: list[dict]) -> dict:
    phase = norm_key(state.get("phase", ""))
    key = phase
    if phase == "decision":
        key = "decision-architecture" if bp.get("present") else "decision-pre-blueprint"
    entries = READ_TO_RESUME.get(key, READ_TO_RESUME["discovery"])
    material = sorted({r["id"] for r in rows if not r["resolved"] and (
        r["criticidade"] == "Critical" or r["expired"] or r["state"] == "Risky")})
    return {
        "key": key,
        "entries": [{"path": p, "why": w} for p, w in entries],
        "material_rows": material,
        "targeted_only": ["_capture/process-model.md §2–§3/§5", "*.text.md",
                          "inputs/ em bruto",
                          "Domain Knowledge (pelas regras do blueprint, nunca por defeito)"],
        "note": "derivado, nunca persistido — fase ≠ sessão; uma sessão nova não depende "
                "do transcript anterior",
    }


# --------------------------------------------------------------- model builder


def _facets(rows: list[dict]) -> dict:
    lenses: set[str] = set()
    rondas: set[str] = set()
    crits: set[str] = set()
    for r in rows:
        # lens is NOT an enum in live data: 'data + governance', 'operations + architect',
        # 'chair', 'architect' all occur. Derive from the data, token-split.
        for tok in re.split(r"[+,/&]| e ", r["lens"]):
            tok = tok.strip()
            if tok:
                lenses.add(tok)
        if r["ronda"]:
            rondas.add(r["ronda"])
        if r["criticidade"]:
            crits.add(r["criticidade"])
    return {
        "lens": sorted(lenses),
        # `enquadramento` is a legitimate `lens` value but not a lens: whoever counts
        # "por lente" reads this list, not the one above (states.md -> schema).
        "lens_producao": sorted(l for l in lenses if norm_key(l) != ENQ_LENS),
        "state": list(SECTIONS),
        "criticidade": sorted(crits, key=lambda c: CRIT_RANK.get(c, 3)),
        "ronda": sorted(rondas, key=lambda r: _round_sort(r, "")),
    }



# ------------------------------------------------- synthesis: contract checks
# The contract of `aisa-synthesize` (step 7 + rules 2 and 3), evaluated by code.
#
# TWO things this deliberately does NOT do:
#
#   1. It does not write in `_synthesis-log.md`. `synthesis_entries()` matches any
#      `<ISO> — <token>` line and `synthesis_state()` takes the newest of them as the
#      moment the topic was synthesised -- so a validation line dated today would make a
#      stale pack look fresh. The record lives in `_synthesis-checks.md`, which no
#      freshness code reads.
#
#   2. It does not trust its own record. The checks depend on the topic text AND on
#      sources outside it (the SU and decisions.md for the cited ids, the pack for the
#      vendor terms, the approved blueprint for the stamp). A sha of the text alone would
#      go on saying `ok` after the SU lost the row the topic cites. So the verdict is
#      RECOMPUTED whenever it is read; the log line is history -- what the hook saw, with
#      the sha of the text and of the dependencies it saw it against.

SYN_CHECK_SEVERITY = {
    "SYN-PARAS": "warn", "SYN-NO-IDS": "warn", "SYN-DEAD-ID": "warn",
    "SYN-VENDOR": "warn", "SYN-TEMPLATE": "warn", "SYN-STAMP": "warn",
}
SYN_NEUTRAL_TOPICS = ("business-story", "as-is", "risks-and-assumptions", "financial-story")
SYN_MIN_PARAS = 3


def pack_vendor_terms(pack: str) -> list[str]:
    """`vendor_terms.solution` of the active pack -- terms that NAME A SOLUTION.

    Not the same list as the Discovery vendor grep: that one includes `sharepoint`,
    `microsoft`, `azure`, which name the CURRENT STATE legitimately in an as-is narrative.
    A pack that declares none makes SYN-VENDOR `not evaluated`, never `ok`.
    """
    if not pack:
        return []
    text = _read(repo_root() / "library" / "packs" / pack / "pack.yaml") or ""
    if not text:
        return []
    block = yl_find_block(text, "solution", "vendor_terms")
    if not block:
        block = yl_find_block(text, "vendor_terms")
    val = _yl_block([(i, c, 0) for i, c in block], 0, len(block), []) if block else None
    if isinstance(val, dict):
        val = val.get("solution")
    if isinstance(val, str):
        val = [val]
    return [str(t).strip().lower() for t in (val or []) if str(t).strip()]


def _syn_paragraphs(text: str) -> int:
    """Non-empty paragraphs, excluding the H1, HTML comments (the authority stamp) and
    fenced code."""
    body = re.sub(r"\A#\s+[^\n]*\n", "", text or "")
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    body = re.sub(r"```.*?```", "", body, flags=re.S)
    return sum(1 for chunk in re.split(r"\n\s*\n", body) if chunk.strip())


def synthesis_check(eng: Path, topic: str, pack: str = "",
                    text: str | None = None) -> dict:
    """The contract verdict for ONE topic pack, computed against what is on disk NOW.

    -> {topic, present, sha, deps, codes: [{code, severity, detail}], evaluated: [...],
        not_evaluated: [...]}
    """
    f = eng / "_synthesis" / (topic + ".md")
    body = text if text is not None else (_read(f) or "")
    pack = pack or _read_json(eng / "_state.json").get("pack", "")
    out: list[dict] = []
    not_eval: list[str] = []
    notes: list[str] = []

    def add(code, detail=""):
        out.append({"code": code, "severity": SYN_CHECK_SEVERITY.get(code, "warn"),
                    "detail": detail})

    if topic not in SYNTH_TOPICS:
        add("SYN-TEMPLATE", "tópico fora dos cinco do kernel")
    if not body.strip():
        return {"topic": topic, "present": False, "sha": "", "deps": "",
                "codes": out, "evaluated": [], "not_evaluated": ["ficheiro ausente"],
                "notes": []}

    n = _syn_paragraphs(body)
    if n < SYN_MIN_PARAS:
        add("SYN-PARAS", "{} parágrafo(s), o contrato pede >= {}".format(n, SYN_MIN_PARAS))

    ids = sorted(set(ID_RE.findall(body)))
    if not ids:
        add("SYN-NO-IDS", "nenhum id citado (regra 2)")
    else:
        su_md = _read(eng / "shared-understanding.md") or ""
        _h, rows, _s, _d = parse_su(su_md)
        known = {r["id"] for r in rows if r.get("id")}
        known |= {b["id"] for b in classify_decisions(_read(eng / "decisions.md") or "")}
        dead = [i for i in ids if i not in known]
        if dead:
            add("SYN-DEAD-ID", "id citado sem linha na SU nem bloco em decisions.md: "
                               + ", ".join(dead[:8]))

    terms = pack_vendor_terms(pack)
    if not terms:
        not_eval.append("SYN-VENDOR (o pacote {} não declara vendor_terms.solution)".format(
            pack or "-"))
    else:
        neutral = topic in SYN_NEUTRAL_TOPICS
        if not neutral and topic == "architecture-story":
            # Rule 3 is conditional for this topic: naming products is legitimate only
            # where an architecture was AUTHORIZED. With no authorization the no-vendor
            # rule applies here too (aisa-synthesize, "No architecture authorization").
            blocks = classify_decisions(_read(eng / "decisions.md") or "")
            bp = blueprint_state(eng, blocks, None, pack)
            src = bp.get("approved") or bp.get("latest_authorized") or {}
            auth = (src.get("authorization") or "").strip().lower()
            if not auth:
                ver = src.get("version")
                match = next((v for v in bp.get("versions", []) if v["version"] == ver), None)
                auth = ((match or {}).get("authorization") or "").strip().lower()
            neutral = auth not in ("authorized", "authorized-bounded")
        if neutral:
            low = body.lower()
            hits = sorted({t for t in terms if t in low})
            if hits:
                add("SYN-VENDOR", "termo de solução num tópico neutro: " + ", ".join(hits[:6]))

    if topic == "architecture-story":
        stamp_issues, stamp_not_eval, stamp_notes = _syn_stamp_issues(eng, body, pack)
        for issue in stamp_issues:
            add("SYN-STAMP", issue)
        not_eval.extend(stamp_not_eval)
        notes.extend(stamp_notes)

    return {"topic": topic, "present": True, "sha": _sha_text(body),
            "deps": _syn_deps_sha(eng, pack), "codes": out,
            "evaluated": [c for c in SYN_CHECK_SEVERITY
                          if not any(n.startswith(c) for n in not_eval)],
            "not_evaluated": not_eval, "notes": notes}


SYN_PAIRS_HEAD_RE = re.compile(r"\(\s*scope\s*,\s*outcome\s*\)\s*pairs", re.I)
SYN_SELECTED_RE = re.compile(
    r"^\s*[-*]\s*\*{0,2}Selected solution\s*/\s*composition\*{0,2}\s*:\s*(?P<v>.+)$",
    re.I | re.M)
# Separador do par: travessao (o que `aisa-decide` escreve), meia-risca, `--` ou um
# hifen entre espacos. Divide-se na PRIMEIRA ocorrencia -- o ambito e curto, e a frase
# de outcome, essa sim, costuma trazer hifens pelo meio.
SYN_PAIR_SPLIT_RE = re.compile(r"\s(?:\u2014|\u2013|--|-)\s")


def decision_block_span(decisions_md: str, did: str) -> str:
    """The text of one `## D-NNN ...` block, up to the next `## ` heading."""
    text = decisions_md or ""
    m = re.search(r"^##\s+" + re.escape(did) + r"\b.*$", text, re.M)
    if not m:
        return ""
    nxt = re.search(r"^##\s+", text[m.end():], re.M)
    return text[m.start():m.end() + (nxt.start() if nxt else len(text))]


def live_solution_decision(decisions_md: str) -> dict | None:
    """The solution decision IN FORCE, never a superseded one.

    Same notion of `live` the rest of the motor uses (`superseded_by`): after a reopen the
    old block is history. Reading its pairs would validate a stamp against a choice nobody
    is making -- and the defect this fixes is exactly that: a D-003 with malformed pairs
    was accepted because D-002's older, well-formed pairs were still in the file.
    """
    blocks = classify_decisions(decisions_md or "")
    live = [b for b in blocks if not b.get("superseded_by") and b.get("kind") == "solution"]
    return live[-1] if live else None


def decision_scope_outcome_pairs(decisions_md: str) -> dict:
    """The `(Scope, outcome) pairs -- UNCOLLAPSED` block of the decision IN FORCE, by SHAPE.

    -> {present, decision, lines, pairs, malformed, selected_solution}

      present   the block header exists inside the live solution decision
      lines     every `- ...` line under it, verbatim
      pairs     those that split into a non-empty scope AND a non-empty outcome sentence
      malformed the ones that do not

    Both fields are read from the SAME block: scanning the whole file would let a
    superseded decision supply the evidence for the current one.

    `aisa-decide` writes one line per emitted pair, `<scope> - <outcome sentence, verbatim>`,
    and forbids merging two scopes into one line. This reads that shape and nothing else: it
    never interprets the sentence, because what a sentence MEANS for architecture needs the
    pack's architectability boundary, which today is prose.
    """
    out = {"present": False, "decision": "", "lines": [], "pairs": [], "malformed": [],
           "selected_solution": ""}
    live = live_solution_decision(decisions_md)
    if live is None:
        return out
    out["decision"] = live["id"]
    text = decision_block_span(decisions_md or "", live["id"])
    if not text:
        return out
    lines = text.splitlines()
    m = SYN_SELECTED_RE.search(text)
    if m:
        val = m.group("v").strip().strip("*` ")
        if val and val.lower() not in ("<none>", "none", "n/a", "-", "nao aplicavel"):
            out["selected_solution"] = val
    start_i = None
    for i, ln in enumerate(lines):
        if SYN_PAIRS_HEAD_RE.search(ln):
            start_i = i
            break
    if start_i is None:
        return out
    out["present"] = True
    base_indent = len(lines[start_i]) - len(lines[start_i].lstrip())
    for ln in lines[start_i + 1:]:
        if not ln.strip():
            continue
        indent = len(ln) - len(ln.lstrip())
        stripped = ln.lstrip()
        if indent <= base_indent:
            break
        if not stripped.startswith(("-", "*")):
            continue
        item = stripped[1:].strip()
        out["lines"].append(item)
        parts = SYN_PAIR_SPLIT_RE.split(item, 1)
        if len(parts) == 2 and parts[0].strip() and parts[1].strip():
            out["pairs"].append({"scope": parts[0].strip(), "outcome": parts[1].strip()})
        else:
            out["malformed"].append(item)
    return out


SYN_NONE_STAMP_RE = re.compile(
    r"authority:\s*none\s*(?:\u2014|\u2013|-{1,2})\s*(?P<reason>[A-Za-z][\w-]*)", re.I)
SYN_NONE_REASONS = ("outcome-forbade", "outside-pack-authority")


def _syn_stamp_issues(eng: Path, body: str, pack: str) -> tuple:
    """Does the stamp on `architecture-story.md` correspond to an authority that EXISTS?

    Recognising the SHAPE of a stamp is not verifying it. A stamp naming a version that is
    not in `_blueprint/`, one naming a version other than the authority this engagement
    actually has, or `authority: none` claimed while an authorized version sits on disk --
    all passed silently, and the topic then carried a provenance nobody could follow.

    The motor checks existence, authorization, correspondence and the reason token. WHICH
    of the two reasons applies (the outcome forbade an architecture, or the selected
    solution is outside this pack's authority) stays the skill's to state: both are
    legitimate and the difference is semantic.
    """
    stamp = synthesis_stamp(body)
    none_stamp = SYN_NONE_STAMP_RE.search(body[:6000])
    blocks = classify_decisions(_read(eng / "decisions.md") or "")
    bp = blueprint_state(eng, blocks, None, pack)
    versions = {v["version"]: v for v in bp.get("versions", [])}
    approved = bp.get("approved") or {}
    latest_auth = bp.get("latest_authorized") or {}
    expected = approved.get("version") or latest_auth.get("version") or ""
    out: list = []
    not_eval: list = []
    notes: list = []

    if stamp:
        ver = stamp.get("version") or ""
        if ver not in versions:
            out.append("carimba {}, que nao existe em _blueprint/ -- a autoridade citada "
                       "nao e verificavel".format(ver or "(sem versao)"))
            return out, not_eval, notes
        v = versions[ver]
        if approved and approved.get("valid") is False and ver == approved.get("version"):
            out.append("carimba {}, que falha a verificacao estrutural".format(ver))
        if expected and ver != expected:
            out.append("carimba {} e a autoridade deste engagement e {} ({})".format(
                ver, expected,
                "aprovada" if approved.get("version") == expected else "ultima autorizada"))
        auth = (v.get("authorization") or "").strip().lower()
        if auth and auth not in ("authorized", "authorized-bounded"):
            out.append("carimba {}, cuja autorizacao e `{}` -- uma versao nao autorizada "
                       "nao e autoridade de arquitectura".format(ver, auth))
        sha = (stamp.get("sha256") or "").lower()
        if sha:
            f = _bp_file(eng, ver)
            real = architecture_block_sha256(_read(f) or "") if f else ""
            if real and sha != real:
                out.append("o bloco architecture de {} mudou desde o carimbo "
                           "(sha256 difere)".format(ver))
        elif re.search(r"sha256\s*:", body[:6000], re.I):
            # `SYNTH_STAMP_RE` only captures a full 64-hex digest, so a truncated or
            # invented one leaves the group empty and used to read as "stamp without a
            # sha" -- i.e. as the tolerated case. A digest that is not a digest is not a
            # missing digest: nothing can be compared against it.
            out.append("carimba {} com um sha256 que nao e um sha256 (64 hex) -- a "
                       "identidade citada nao e verificavel".format(ver))
        return out, not_eval, notes

    if none_stamp:
        reason = (none_stamp.group("reason") or "").strip().lower()
        if reason not in SYN_NONE_REASONS:
            out.append("`authority: none -- {}` nao e uma razao reconhecida (esperado: "
                       "{})".format(reason or "(vazia)", " | ".join(SYN_NONE_REASONS)))
        # CONTRADICAO VERIFICAVEL -- nunca convertida em "nao avaliado".
        authorized = [ver for ver, v in versions.items()
                      if (v.get("authorization") or "").strip().lower()
                      in ("authorized", "authorized-bounded")]
        if authorized:
            out.append("declara `authority: none` e o engagement tem arquitectura "
                       "autorizada ({}) -- a razao nao se sustenta no estado registado"
                       .format(", ".join(sorted(authorized))))
            return out, not_eval, notes

        # A BASE DOCUMENTAL sao os pares (scope, outcome) que `aisa-decide` serializa.
        # FALTA DE INFORMACAO e uma coisa, INCONSISTENCIA VERIFICAVEL e outra, e o motor
        # nao as junta: sem pares nada se afirma (nem limpo, nem falha); com pares, a
        # ESTRUTURA valida-se. O SIGNIFICADO da razao continua por avaliar em ambos os
        # casos -- separar `outcome-forbade` de `outside-pack-authority` exige ler a frase
        # emitida contra a fronteira de architectabilidade do pacote, que hoje e prosa.
        sol = [b for b in blocks if b.get("kind") == "solution"]
        pairs = decision_scope_outcome_pairs(_read(eng / "decisions.md") or "")
        if not sol:
            not_eval.append("SYN-STAMP: `authority: none -- {}` nao foi verificada -- nao ha "
                            "decisao de solucao registada em decisions.md, logo nao ha pares "
                            "(scope, outcome) contra que a validar".format(
                                reason or "(sem razao)"))
            return out, not_eval, notes
        if not pairs["present"]:
            not_eval.append("SYN-STAMP: `authority: none -- {}` nao foi verificada -- a "
                            "decisao de solucao nao regista pares (scope, outcome)".format(
                                reason or "(sem razao)"))
            return out, not_eval, notes
        if not pairs["pairs"]:
            out.append("o bloco (scope, outcome) existe e nao tem um unico par completo "
                       "(<ambito> -- <frase de outcome>){} -- dados malformados, nao "
                       "ausentes".format(
                           ": " + "; ".join(x[:40] for x in pairs["malformed"][:3])
                           if pairs["malformed"] else ""))
            return out, not_eval, notes
        if pairs["malformed"]:
            out.append("{} linha(s) do bloco (scope, outcome) nao sao pares completos: "
                       "{}".format(len(pairs["malformed"]),
                                   "; ".join(x[:40] for x in pairs["malformed"][:3])))
        if reason == "outside-pack-authority" and not pairs["selected_solution"]:
            out.append("`authority: none -- outside-pack-authority` fala da solucao "
                       "seleccionada e decisions.md nao a regista (`Selected solution / "
                       "composition`)")
            return out, not_eval, notes
        if not out:
            notes.append("`authority: none -- {}`: a base documental existe ({} par(es) "
                         "(scope, outcome){}); o SIGNIFICADO da razao nao foi avaliado -- "
                         "separa-la exige a fronteira de architectabilidade do pacote "
                         "legivel pelo motor".format(
                             reason, len(pairs["pairs"]),
                             " + solucao seleccionada" if pairs["selected_solution"] else ""))
        return out, not_eval, notes

    out.append("sem carimbo `authority:` (nem `authority: none -- <razao>`)")
    return out, not_eval, notes


def _syn_deps_sha(eng: Path, pack: str) -> str:
    """Fingerprint of what the checks depend on BESIDES the topic text: the SU, the
    decisions, the pack's term list, the approved blueprint. It goes in the log line so
    the history says what the verdict was computed against."""
    parts = [
        _sha_text(_read(eng / "shared-understanding.md") or ""),
        _sha_text(_read(eng / "decisions.md") or ""),
        _sha_text("|".join(pack_vendor_terms(pack))),
    ]
    blocks = classify_decisions(_read(eng / "decisions.md") or "")
    bp = blueprint_state(eng, blocks, None, pack)
    appr = bp.get("approved") or {}
    parts.append("{}:{}".format(appr.get("version", "-"), appr.get("valid", "-")))
    return hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:12]


SYN_CHECK_LINE_RE = re.compile(
    r"^check\s*·\s*(?P<when>\S+)\s*·\s*(?P<topic>[a-z][a-z-]*)\s*·\s*sha:(?P<sha>[0-9a-f]+)"
    r"(?:\s*·\s*deps:(?P<deps>[0-9a-f]+))?\s*·\s*(?P<result>.+)$")


def synthesis_check_log(eng: Path) -> dict:
    """The LAST recorded line per topic in `_synthesis-checks.md`. History, not verdict."""
    out: dict[str, dict] = {}
    for raw in (_read(eng / "_synthesis" / "_synthesis-checks.md") or "").splitlines():
        m = SYN_CHECK_LINE_RE.match(raw.strip())
        if m:
            out[m.group("topic")] = {"when": m.group("when"), "sha": m.group("sha"),
                                     "deps": m.group("deps") or "",
                                     "result": m.group("result").strip()}
    return out


def synthesis_checks(eng: Path, pack: str = "") -> dict:
    """Per topic: the verdict RECOMPUTED now, plus the last line the hook wrote.

    `stale_record` is true when the recorded line was computed against a different text or
    different dependencies -- the record is then history and nothing more. There is no
    inherited `ok`.
    """
    pack = pack or _read_json(eng / "_state.json").get("pack", "")
    recorded = synthesis_check_log(eng)
    topics = {}
    for topic in SYNTH_TOPICS:
        now = synthesis_check(eng, topic, pack)
        rec = recorded.get(topic)
        topics[topic] = {
            "present": now["present"],
            "codes": [c["code"] for c in now["codes"]],
            "detail": now["codes"],
            "not_evaluated": now["not_evaluated"],
            "notes": now.get("notes") or [],
            "verdict": ("ausente" if not now["present"]
                        else ("avisos" if now["codes"]
                              else ("nao avaliado" if now["not_evaluated"] else "ok"))),
            "recorded": rec,
            "stale_record": bool(rec) and (rec["sha"] != now["sha"]
                                           or (rec["deps"] and rec["deps"] != now["deps"])),
        }
    codes = sorted({c for t in topics.values() for c in t["codes"]})
    return {"topics": topics, "codes": codes,
            "verdict_owner": "motor (presença, forma, termos); o que a prosa diz é da skill",
            "note": "recalculado na consulta — o log é o que o hook viu, nunca o veredicto"}


# ------------------------------------------------------------------- phase gates
# `phases.md` -> "Exit criteria (soft)" of each phase, evaluated by CODE where the
# criterion is a count, a presence or a marker, and DECLARED as `juizo` or `n/a`
# where it is not. Runtime-hardening bloco C: a gate that says it was evaluated was
# evaluated, and a criterion nobody can measure is never reported as OK.
#
# The motor carries the facts. Whether an override is justified, whether comprehension
# is sufficient, whether the named form is the RIGHT form -- all skill.

GATE_TRANSITIONS = {
    "aisa-frame": "discovery→framing",
    "aisa-options": "framing→options",
    "aisa-decide": "options→decision",
}
OM_MARKERS = ("SIMULATED", "PACK MODEL", "ANALOGY", "ORDER OF MAGNITUDE UNAVAILABLE")
LENSES_6 = ("business", "operations", "user", "data", "governance", "financial")


def _g(criterion: str, mode: str, ok, value="", threshold="", note="") -> dict:
    """One criterion. `ok` is None whenever the mode is not `codigo`: a judgement and a
    non-evaluable criterion have no machine verdict, and pretending otherwise is the
    defect this function exists to remove."""
    return {"criterion": criterion, "mode": mode,
            "ok": (bool(ok) if mode == "codigo" else None),
            "value": str(value), "threshold": str(threshold), "note": note}


def _open_rows(rows: list[dict], state: str) -> list[dict]:
    return [r for r in rows or [] if r.get("state") == state
            and not r.get("resolved") and not r.get("retired")]


def _critical(rows: list[dict], state: str) -> list[dict]:
    out = []
    for r in _open_rows(rows, state):
        crit = (r.get("criticidade") or "").strip().lower()
        if crit.startswith("crit") or crit in ("alta", "high"):
            out.append(r)
    return out


def _lens_files(eng: Path) -> dict:
    """A lens counts as having written when its file exists AND carries at least one SU
    id. Presence of an empty file is presence, not content, and the report says so."""
    out = {}
    for lens in LENSES_6:
        f = eng / "lens-outputs" / (lens + ".md")
        text = _read(f) or ""
        out[lens] = bool(text.strip()) and bool(ID_RE.search(text))
    return out


def _capture_pending(eng: Path) -> list[str]:
    src = eng / "inputs"
    cap = eng / "_capture"
    if not src.is_dir():
        return []
    pending = []
    for p in sorted(src.iterdir()):
        if p.is_file() and p.suffix.lower() in (".xlsx", ".xlsm"):
            if not cap.is_dir() or not list(cap.glob(p.name + ".*")):
                pending.append(p.name)
    return pending


def _options_blocks(options_md: str) -> list[str]:
    return re.findall(r"^###\s+(O-\d+)", options_md or "", re.M)


def _gate_discovery(eng: Path, model_bits: dict) -> list[dict]:
    rows = model_bits["rows"]
    confirmed = len(_open_rows(rows, "Confirmed"))
    unk = _critical(rows, "Unknown")
    con = _critical(rows, "Conflicted")
    lenses = _lens_files(eng)
    missing_lens = [k for k, v in lenses.items() if not v]
    delta = model_bits["round_delta"].get("por_ronda") or []
    last = [d for d in delta if str(d.get("ronda", "")).startswith("R-")]
    last = last[-1] if last else None
    pending = _capture_pending(eng)
    return [
        _g("Confirmed >= 10", "codigo", confirmed >= 10, confirmed, ">= 10"),
        _g("Unknown Critical = 0", "codigo", not unk,
           "{} ({})".format(len(unk), ", ".join(r["id"] for r in unk[:6]) or "-"), "0",
           "uma pergunta descida a cosmético leva a criticidade com ela (states.md)"),
        _g("Conflicted Critical = 0", "codigo", not con,
           "{} ({})".format(len(con), ", ".join(r["id"] for r in con[:6]) or "-"), "0"),
        _g("6 lentes escreveram em lens-outputs/", "codigo", not missing_lens,
           "{}/6".format(6 - len(missing_lens)), "6/6",
           "presença de conteúdo mínimo (ficheiro com >= 1 id da SU), nunca qualidade"),
        _g("a última passagem convergiu", "codigo",
           (last is None) or not last.get("sem_convergencia"),
           "-" if last is None else "{}: criadas {} · fechadas {}".format(
               last["ronda"], last["criadas"], last["fechadas"]),
           "criadas <= fechadas"),
        _g("_capture/ para cada .xlsx/.xlsm em inputs/", "codigo", not pending,
           ", ".join(pending) or "nenhum em falta", "0 em falta"),
        _g("teste de compreensão", "juizo", None, "",
           "", "aisa-frame passo 2 — a skill lê a SU e julga; o motor não"),
    ]


def _gate_framing(eng: Path, model_bits: dict) -> list[dict]:
    frame = model_bits["frame_identity"]
    verdict = (frame or {}).get("verdict", "")
    decisions_md = model_bits["decisions_md"]
    validated = bool(re.search(r"(?mi)^-?\s*\*{0,2}(Validated by|Validado por)\*{0,2}\s*:",
                               decisions_md))
    frame_md = _read(eng / "frame.md") or ""
    enq = _read(eng / "enquadramento.md") or ""
    declared = sorted(set(re.findall(r"\bM-(\d{1,2})\b", enq)))
    addressed = sorted(set(re.findall(r"\bM-(\d{1,2})\b", frame_md)))
    missing_m = [m for m in declared if m not in addressed]
    return [
        _g("a frase corrente está aprovada", "codigo",
           verdict in ("match", "match-other-round"), verdict or "sem frase", "match"),
        _g("`Validated by` registado", "codigo", validated,
           "sim" if validated else "não", "presente"),
        _g("cada M-n confirmado ou corrigido no frame", "codigo", not missing_m,
           "{}/{} tratados{}".format(len(addressed), len(declared),
                                     "" if not missing_m else
                                     " — falta M-" + ", M-".join(missing_m)),
           "todos",
           "presença do id no frame.md; se a correcção está certa é juízo"),
    ]


def _option_table(body: str) -> tuple[dict, dict]:
    """The decision table of `options.md` -> ({O-NNN: {header: cell}}, {header: index}).

    Read by SHAPE (a header row naming the columns, then `| O-NNN | ...` rows), never by
    looking for a word in the prose: a technology cell reads `canvas app + Azure SQL`, and
    searching the section for the word "tecnologia" answers a different question.
    """
    lines = (body or "").splitlines()
    header, cols = None, {}
    for i, ln in enumerate(lines):
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        low = [c.lower() for c in cells]
        if any(re.search(r"tecnolog|technolog", c) for c in low) and len(cells) >= 3:
            header, cols = i, {c: n for n, c in enumerate(low)}
            break
    if header is None:
        return {}, {}
    rows = {}
    for ln in lines[header + 1:]:
        if not ln.strip().startswith("|"):
            continue
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        m = re.match(r"^\**\s*(O-\d+)", cells[0]) if cells else None
        if m:
            rows[m.group(1)] = cells
    return rows, cols


def _cell(rows: dict, cols: dict, oid: str, *needles: str) -> str:
    cells = rows.get(oid) or []
    for name, idx in cols.items():
        if any(n in name for n in needles) and idx < len(cells):
            return cells[idx]
    return ""


def _filled(value: str) -> bool:
    v = (value or "").strip().strip("*` ").lower()
    return bool(v) and v not in ("-", "—", "–", "n/a", "na", "?", "tbd")


def _gate_options(eng: Path, model_bits: dict) -> list[dict]:
    options_md = model_bits["options_md"]
    body = options_md or ""
    blocks = _options_blocks(body)
    table, cols = _option_table(body)
    ids = sorted(set(blocks) | set(table))
    hist = model_bits["options_history"]
    rnd = (hist or {}).get("max") or ""
    log = (_read(eng / "lens-outputs" / "chairman-synthesis-{}.md".format(rnd)) or "") if rnd else ""

    def per_option(check_label, predicate, threshold, note=""):
        """A per-option criterion with NO options is not satisfied -- it is unevaluable.
        Reporting 0/0 as `ok` is the vacuous truth this front exists to remove."""
        if not ids:
            return _g(check_label, "n/a", None, "sem opções para avaliar", threshold,
                      note or "nada a avaliar enquanto options.md não tiver opções")
        missing = [oid for oid in ids if not predicate(oid)]
        return _g(check_label, "codigo", not missing,
                  "{}/{}{}".format(len(ids) - len(missing), len(ids),
                                   "" if not missing else " — falta " + ", ".join(missing)),
                  threshold, note)

    def has_om(oid):
        seg = _option_segment(body, oid) + " " + " ".join(table.get(oid) or [])
        return any(m in seg for m in OM_MARKERS)

    def names_tech(oid):
        return _filled(_cell(table, cols, oid, "tecnolog", "technolog"))

    tech_note = ("célula da coluna Tecnologia preenchida (uma alternativa sem construção "
                 "declara-o na célula); se a forma nomeada é a certa é juízo")
    if not cols:
        tech = _g("cada opção nomeia a tecnologia (plataforma nomeia a forma)", "n/a", None,
                  "sem tabela de decisão em options.md", "coluna Tecnologia",
                  "não avaliável sem a tabela — nunca 'OK'")
    else:
        tech = per_option("cada opção nomeia a tecnologia (plataforma nomeia a forma)",
                          names_tech, "todas", tech_note)

    rule_rows = re.findall(r"(?i)vi[aá]vel se a regra for alterada|viable if the rule is changed",
                           body)
    rec = bool(re.search(r"(?mi)^##+\s+(recomenda|recommendation)", body))
    no_rec = "no recommendation" in body.lower() or "sem recomendação" in body.lower()
    return [
        _g(">= 3 opções", "codigo", len(ids) >= 3,
           "{} ({})".format(len(ids), ", ".join(ids) or "-"), ">= 3"),
        _g("cobertura DO-NOTHING declarada", "codigo", "DO-NOTHING" in log,
           "no log da ronda {}".format(rnd or "-"), "marcador presente"),
        _g("cobertura PROCESS-CHANGE declarada", "codigo", "PROCESS-CHANGE" in log,
           "no log da ronda {}".format(rnd or "-"), "marcador presente"),
        per_option("cada opção com ordem de grandeza e fonte", has_om,
                   "um dos 4 marcadores por opção"),
        _g("regra organizacional não apaga a opção", "codigo", True,
           "{} opção(ões) com o veredicto".format(len(rule_rows)), "-",
           "presença do veredicto quando usado; se a regra devia ter sido invocada é juízo"),
        _g("a ronda fecha com recomendação", "codigo", rec or no_rec,
           "secção presente" if rec else ("`no recommendation`" if no_rec else "ausente"),
           "recomendação ou `no recommendation`"),
        tech,
        _g("decision-tree.md do pacote consultado", "n/a", None, "", "",
           "não há registo mecânico da consulta — não avaliável, nunca 'OK'"),
    ]


def _option_segment(body: str, oid: str) -> str:
    m = re.search(r"^###\s+" + re.escape(oid) + r"\b", body or "", re.M)
    if not m:
        return ""
    nxt = re.search(r"^###\s+O-\d+", body[m.end():], re.M)
    seg = body[m.start():m.end() + (nxt.start() if nxt else len(body))]
    table = "\n".join(l for l in (body or "").splitlines() if oid in l)
    return seg + "\n" + table


def gates(eng: Path, transition: str, model_bits: dict) -> dict:
    """Every exit criterion of the phase that is ENDING, with its mode. Cobertura is
    declared: `n de m por código`, never `gate OK`."""
    phase = transition.split("→")[0] if "→" in transition else transition
    fn = {"discovery": _gate_discovery, "framing": _gate_framing,
          "options": _gate_options}.get(phase)
    if fn is None:
        return {"transition": transition, "phase": phase, "criteria": [],
                "evaluated": 0, "total": 0, "red": [], "judgement": [], "na": [],
                "fingerprint": "", "id": "",
                "note": "transição desconhecida — nada avaliado"}
    crit = fn(eng, model_bits)
    code = [c for c in crit if c["mode"] == "codigo"]
    red = [c["criterion"] for c in code if not c["ok"]]
    return {
        "transition": transition, "phase": phase, "criteria": crit,
        "evaluated": sum(1 for c in code if c["ok"]), "total": len(code),
        "declared": len(crit),
        "red": red,
        "judgement": [c["criterion"] for c in crit if c["mode"] == "juizo"],
        "na": [c["criterion"] for c in crit if c["mode"] == "n/a"],
        "fingerprint": "", "id": "",
        "note": "{} de {} por código · {} por juízo · {} não avaliável".format(
            len(code), len(crit), sum(1 for c in crit if c["mode"] == "juizo"),
            sum(1 for c in crit if c["mode"] == "n/a")),
    }


def gate_fingerprint(eng: Path, transition: str, model_bits: dict,
                     criteria: list[dict]) -> str:
    """Identity of the STATE that was evaluated -- contents and identities, not counts.

    Counts alone collide: swapping U-001 for U-002 leaves every number where it was and
    the gate result with it, so a second run under a different reality would reuse the
    first run's id. Adding a frame approval to decisions.md changes the verdict without
    touching the SU, so decisions.md is in here too, and so is each criterion's own
    normalized result.
    """
    rows = model_bits["rows"]
    parts = [transition]
    for state in ("Unknown", "Conflicted", "Risky"):
        parts += sorted("{}:{}:{}:{}".format(state, r.get("id"), r.get("criticidade"),
                                             r.get("ronda"))
                        for r in _open_rows(rows, state))
    parts += sorted("Confirmed:" + str(r.get("id")) for r in _open_rows(rows, "Confirmed"))
    parts += sorted("Assumed:" + str(r.get("id")) for r in _open_rows(rows, "Assumed"))
    for rel in ("decisions.md", "options.md", "frame.md", "enquadramento.md"):
        parts.append("{}:{}".format(rel, _sha_text(_read(eng / rel) or "")))
    lens_dir = eng / "lens-outputs"
    if lens_dir.is_dir():
        for f in sorted(lens_dir.glob("*.md")):
            parts.append("lens:{}:{}".format(f.name, _sha_text(_read(f) or "")))
    st = _read_json(eng / "_state.json")
    parts.append("state:{}:{}:{}".format(st.get("phase", ""), st.get("round", ""),
                                         st.get("round_in_progress", "")))
    for c in criteria:
        parts.append("crit:{}={}".format(
            c["criterion"], c["ok"] if c["mode"] == "codigo" else c["mode"]))
    return hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()


def _sha_text(text: str) -> str:
    return hashlib.sha256((text or "").replace("\r\n", "\n").encode("utf-8")).hexdigest()[:12]


def gate_state(eng: Path, transition: str) -> dict:
    """Public entry: evaluate `transition` against what is on disk, with its identity."""
    su_md = _read(eng / "shared-understanding.md") or ""
    _h, rows, _sec, _d = parse_su(su_md)
    st = _read_json(eng / "_state.json")
    bits = {
        "rows": rows,
        "decisions_md": _read(eng / "decisions.md") or "",
        "options_md": _read(eng / "options.md") or "",
        "round_delta": round_delta(rows, parse_round_dates(eng, st, _h)),
        "frame_identity": frame_identity(eng, classify_decisions(_read(eng / "decisions.md") or "")),
        "options_history": options_round_history(eng, st),
    }
    g = gates(eng, transition, bits)
    fp = gate_fingerprint(eng, transition, bits, g["criteria"])
    g["fingerprint"] = fp
    g["id"] = "G-{}-{}".format(transition.replace("→", "-"), fp[:10])
    return g


def build_model(eng: Path, today: date) -> dict:
    state = _read_json(eng / "_state.json")
    context = _read_json(eng / "context.json")
    su_md = _read(eng / "shared-understanding.md") or ""
    su_header, rows, su_meta, diagnostics = parse_su(su_md)

    half_lives, hl_diags = load_half_lives(state.get("pack", ""))
    diagnostics.extend(hl_diags)
    round_dates = parse_round_dates(eng, state, su_header)
    for r in rows:
        compute_expiry(r, half_lives, today, round_dates)

    ids = {r["id"]: r for r in rows}
    health = epistemic_health(rows)
    agenda = meeting_agenda(rows)
    critical = critical_open(rows)
    decisions_md = _read(eng / "decisions.md") or ""
    options_md = _read(eng / "options.md") or ""
    tws = scan_tripwires(parse_tripwires(decisions_md), rows)
    artefacts = artefact_index(eng, state)

    # --- status layer (A0): facts the /status view needs -----------------
    dec_blocks = classify_decisions(decisions_md)
    frame_id = frame_identity(eng, dec_blocks)
    opts_history = options_round_history(eng, state)
    reopen = revisit_state(eng)
    tw_facts = tripwire_facts(dec_blocks, rows)
    bp = blueprint_state(eng, dec_blocks, rows, state.get("pack", ""))
    syn = synthesis_state(eng, dec_blocks, rows, state.get("pack", ""))
    syn_checks = synthesis_checks(eng, state.get("pack", ""))
    # Bloco C: the gate of the transition this phase would take, evaluated by code with
    # each criterion's mode declared. `/status` and the dashboard read it; the hook writes
    # its own line. A phase with no outgoing gate (decision) simply has none.
    gate = gate_state(eng, {"discovery": "discovery→framing",
                            "framing": "framing→options",
                            "options": "options→decision"}.get(state.get("phase", ""), ""))         if state.get("phase") in ("discovery", "framing", "options") else None
    rnd = render_state(eng, bp, syn)
    # The fourth dimension (coverage-contract.md): structure, coverage, approval and
    # end-to-end are four separate questions, and `bp.valid` only ever answered the
    # first. Read-only, and free for an engagement with no record in `_coverage/`.
    cov = coverage_status(eng, bp, state.get("pack", ""))
    sims = simulation_coherence(eng, rows)
    items = su_items(rows, agenda, bp, tw_facts, options_md, decisions_md)
    marco = milestone(eng, state, health, critical, artefacts, bp, syn, dec_blocks,
                      items, frame_id)
    resume = read_to_resume(state, bp, rows)
    diagnostics.extend(bp["diagnostics"])
    diagnostics.extend(syn.get("diagnostics") or [])
    # Before the decision phase there is no solution decision to find, so its
    # absence is the expected state, not a finding. Warning about it in Options
    # made a normal engagement look broken.
    if (not tw_facts["source_decision"] and dec_blocks
            and norm_key(state.get("phase", "")) == "decision"):
        diagnostics.append({
            "level": "warn", "where": "decisions.md", "line": 0,
            "message": "fase decision e nenhuma decisão-solução identificada entre {} "
                       "blocos D-NNN — os tripwires não têm fonte; verificação "
                       "incompleta, não 'OK'".format(len(dec_blocks))})
    if cov.get("engine") not in ("ok",):
        diagnostics.append({
            "level": "warn", "where": "library/kernel/tools/coverage.py", "line": 0,
            "message": "cobertura não avaliada — {} ({}); verificação incompleta, "
                       "não «sem lacunas»".format(cov.get("engine"),
                                                  cov.get("engine_error", ""))})
    for _st in (cov.get("stages") or {}).values():
        if _st.get("error"):
            diagnostics.append({
                "level": "warn", "where": "_coverage/", "line": 0,
                "message": "revisão de cobertura da etapa {} não avaliada: {}".format(
                    _st.get("stage", ""), _st["error"])})
    docs = collect_phase_docs(eng, ids)
    timeline = build_timeline(
        parse_story(_read(eng / "story.md") or ""),
        parse_council_log(_read(eng / "council-log.md") or ""),
        parse_decisions(_read(eng / "decisions.md") or ""),
        round_dates, ids, docs)

    if not su_md:
        diagnostics.append({"level": "error", "where": "shared-understanding.md", "line": 0,
                            "message": "ficheiro ausente ou vazio"})
    if su_meta["schema_flavour"] == "legacy":
        diagnostics.append({
            "level": "info", "where": "shared-understanding.md", "line": 0,
            "message": "SU pre-v2.2: sem verificado_em/validade/custo/swing -- datas inferidas "
                       "da ronda, validade assumida 'organizacional', custo 'email', "
                       "swing 'dimensionante' (states.md, aplicado na leitura)"})

    requester = context.get("requester") or {}
    model = {
        "artefact": ARTEFACT_ID,
        "schema": SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "generated": now_iso(),
        "today": today.isoformat(),
        "engagement": {
            "slug": state.get("engagement") or eng.name,
            "pack": state.get("pack", ""),
            "phase": state.get("phase", ""),
            "round": state.get("round", ""),
            # `round` is the last COMPLETED round; a passagem opened by `/round <lens>` and not
            # yet closed lives in `round_in_progress` (phases.md -> Rounds). Reporting the first
            # as "where we are" while lenses stamp the second is how a half-run round looked
            # finished. Empty string = no round open. Stale values (not ahead of `round`) are
            # dropped here so no consumer has to re-derive the rule.
            "round_in_progress": _open_round(state),
            # Which perspectives already stamped the open passagem (header match, 1.8.0).
            # Empty lists when no passagem is open.
            "lentes_ronda_aberta": lenses_for_round(eng, _open_round(state)),
            "created": state.get("created", ""),
            "aisa_version": state.get("aisa_version", ""),
            "capture_run": state.get("capture_run", 0),
            "path": str(eng),
            "sponsor": su_header.get("sponsor", "") or (requester.get("name") or ""),
            "requester_role": requester.get("role", ""),
            "iniciado": su_header.get("iniciado", ""),
            "fase_actual": su_header.get("fase actual", ""),
            "ultima_actualizacao": su_header.get("ultima actualizacao", ""),
            "literal_request": context.get("literal_request", ""),
        },
        "su": {
            "header_health_raw": su_header.get("saude epistemica", ""),
            "schema_flavour": su_meta["schema_flavour"],
            "sections": su_meta["sections"],
            "rows": rows,
        },
        "health": health,
        "revalidate": revalidation_list(rows),
        "agenda": agenda,
        "critical": critical,
        "tripwires": tws,
        "next_action": {"text": marco["text"], "command": marco["command"]},
        "status": {
            "milestone": marco,
            "decisions": dec_blocks,
            "tripwires": tw_facts,
            "blueprint": bp,
            "gates": gate,
            "synthesis_checks": syn_checks,
            "synthesis": syn,
            "render": rnd,
            "coverage": cov,
            "simulations": sims,
            "items": items,
            "read_to_resume": resume,
        },
        "timeline": timeline,
        "artefacts": artefacts,
        "phase_docs": docs,
        "frame_sentence": frame_id["sentence"],
        # P-18: the sentence, its fingerprint, and whether the approval on file
        # approves THIS sentence. `/options` reads `frame.verdict` in its pre-flight.
        "frame": frame_id,
        "options_history": opts_history,
        "reopen": reopen,
        "render": {"versions": render_versions(eng), "gaps": parse_render_gaps(eng)},
        "facets": _facets(rows),
        "round_dates": {k: list(v) for k, v in round_dates.items()},
        "round_delta": round_delta(rows, round_dates),
        "confirmed_locator": audit_confirmed_locators(rows, eng),
        "enquadramento": enquadramento_state(eng, rows),
        "arbiter": arbiter_declarations(
            rows, has_enq=(eng / "enquadramento.md").is_file()),
        "funding_gate": funding_gate_audit(rows, context),
        "diagnostics": diagnostics,
    }
    stable = {k: v for k, v in model.items() if k != "generated"}
    model["build"] = hashlib.sha1(
        json.dumps(stable, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    ).hexdigest()[:12]
    return model


# ------------------------------------------------------------------- CSS / JS
# Self-contained: no <link>, no src=, no @import, no webfonts, no images. The type
# stack asks for Montserrat / Roboto / Roboto Mono and falls back to the system faces
# where they are not installed -- a webfont would break the file:// case the dashboard
# has to survive.
# Palette: GALP standard (Pure Orange FF5A00, Dark Orange 7A1400, Pure Grey EDE9DF,
# Dark Grey 39383A) so the page, the report and the Word handoff read as one system.
# Every colour is a custom property on :root -- zero hard-coded hex below it.

CSS = """
:root{
  --bg:#EDE9DF; --panel:#FFFFFF; --surface:#F5F2EC; --hover:#EDE9DF; --hover-warm:#F9F6F1;
  --line:#D7CEC5; --line-soft:#E7E3DB; --deco:#B5AEA4;
  --ink:#39383A; --ink2:#6B635B; --ink3:#7A736B; --ink-strong:#5C554D;
  --accent:#FF5A00; --a-soft:#FFD6BC; --a-tint:#FFE7D8; --a-tint2:#FFF1E8; --a-mid:#FFB183;
  --brand:#7A1400; --brand-press:#5C0F00; --on-a:#2B1200; --on-brand:#FFFFFF;
  --hero:#39383A; --hero-ink:#FFFFFF; --hero-dim:rgba(255,255,255,.55);
  --hero-txt:rgba(255,255,255,.7); --hero-rule:rgba(255,255,255,.16);
  --hero-track:rgba(255,255,255,.12); --hero-zero:rgba(255,255,255,.35);
  --bad:#7A1400; --warn:#8F3200;
  --f-ui:'Montserrat','Segoe UI',system-ui,-apple-system,Arial,sans-serif;
  --f-txt:'Roboto','Segoe UI',system-ui,-apple-system,Arial,sans-serif;
  --f-mono:'Roboto Mono',ui-monospace,Consolas,'Courier New',monospace;
  --st-Confirmed-fg:#7A1400; --st-Confirmed-bg:#FFD6BC; --st-Confirmed-dot:#FF5A00;
  --st-Assumed-fg:#8F3200; --st-Assumed-bg:#FFE7D8; --st-Assumed-dot:#FFB183;
  --st-Unknown-fg:#7A1400; --st-Unknown-bg:#FFF1E8; --st-Unknown-dot:#FFD6BC;
  --st-Conflicted-fg:#7A1400; --st-Conflicted-bg:#F6E2DB; --st-Conflicted-dot:#7A1400;
  --st-Risky-fg:#5C554D; --st-Risky-bg:#E7E3DB; --st-Risky-dot:#D7CEC5;
  --rowpad:11px 16px; --fs:13px; --clamp:3;
  --shadow:0 1px 3px rgba(0,0,0,.05); --shadow-lift:0 2px 8px rgba(122,20,0,.14);
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#191A1C; --panel:#232427; --surface:#2B2C30; --hover:#2E2F33; --hover-warm:#2E2F33;
    --line:#3B3C42; --line-soft:#313237; --deco:#6B635B;
    --ink:#EDE9DF; --ink2:#B5AEA4; --ink3:#9C958C; --ink-strong:#D7CEC5;
    --a-soft:#5A2000; --a-tint:#431800; --a-tint2:#341200; --a-mid:#B85A20;
    --brand:#FFB183; --brand-press:#FFD6BC; --on-brand:#2B1200;
    --hero:#101113;
    --bad:#FF8A5C; --warn:#E0A33A;
    --st-Confirmed-fg:#FFD6BC; --st-Confirmed-bg:#5A2000; --st-Confirmed-dot:#FF5A00;
    --st-Assumed-fg:#FFC9A5; --st-Assumed-bg:#431800; --st-Assumed-dot:#FFB183;
    --st-Unknown-fg:#FFD6BC; --st-Unknown-bg:#341200; --st-Unknown-dot:#FFD6BC;
    --st-Conflicted-fg:#FFC0AE; --st-Conflicted-bg:#4A1A10; --st-Conflicted-dot:#FF8A5C;
    --st-Risky-fg:#D7CEC5; --st-Risky-bg:#33343A; --st-Risky-dot:#6B635B;
    --shadow:0 1px 3px rgba(0,0,0,.5);
  }
}
:root[data-theme="dark"]{
  --bg:#191A1C; --panel:#232427; --surface:#2B2C30; --hover:#2E2F33; --hover-warm:#2E2F33;
  --line:#3B3C42; --line-soft:#313237; --deco:#6B635B;
  --ink:#EDE9DF; --ink2:#B5AEA4; --ink3:#9C958C; --ink-strong:#D7CEC5;
  --a-soft:#5A2000; --a-tint:#431800; --a-tint2:#341200; --a-mid:#B85A20;
  --brand:#FFB183; --brand-press:#FFD6BC; --on-brand:#2B1200;
  --hero:#101113;
  --bad:#FF8A5C; --warn:#E0A33A;
  --st-Confirmed-fg:#FFD6BC; --st-Confirmed-bg:#5A2000; --st-Confirmed-dot:#FF5A00;
  --st-Assumed-fg:#FFC9A5; --st-Assumed-bg:#431800; --st-Assumed-dot:#FFB183;
  --st-Unknown-fg:#FFD6BC; --st-Unknown-bg:#341200; --st-Unknown-dot:#FFD6BC;
  --st-Conflicted-fg:#FFC0AE; --st-Conflicted-bg:#4A1A10; --st-Conflicted-dot:#FF8A5C;
  --st-Risky-fg:#D7CEC5; --st-Risky-bg:#33343A; --st-Risky-dot:#6B635B;
  --shadow:0 1px 3px rgba(0,0,0,.5);
}
:root[data-density="compact"]{ --rowpad:6px 16px; --fs:12.5px; --clamp:2 }

*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font:400 14px/1.55 var(--f-ui);
     -webkit-font-smoothing:antialiased}
a{color:var(--brand);text-underline-offset:2px}
::selection{background:var(--brand);color:var(--on-brand)}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:var(--line);border-radius:6px;border:3px solid var(--bg)}
::-webkit-scrollbar-thumb:hover{background:var(--deco)}
[hidden]{display:none!important}
:where(a,button,summary,input,[tabindex]):focus-visible{outline:2px solid var(--accent);
   outline-offset:2px;border-radius:5px}
tr[data-id]:focus-visible{outline:2px solid var(--accent);outline-offset:-2px}
@media (prefers-reduced-motion: reduce){*,*::before,*::after{transition-duration:.01ms!important}}
.sr{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
    clip:rect(0 0 0 0);white-space:nowrap;border:0}

/* ---------- shell */
.app{height:100vh;display:flex;flex-direction:column;overflow:hidden}
header.top{flex:none;min-height:64px;background:var(--panel);border-bottom:1px solid var(--line);
   display:flex;align-items:center;gap:14px;padding:0 24px;flex-wrap:wrap}
.wordmark{font:700 18px/1 var(--f-ui);color:var(--ink);white-space:nowrap}
.wordmark span{font-weight:400;color:var(--ink2);margin-left:6px}
.idblock{display:flex;align-items:center;gap:10px;padding-left:24px;
   border-left:1px solid var(--line);margin-left:4px;flex-wrap:wrap}
.slug{font:500 13px/1 var(--f-mono);color:var(--ink)}
.dot4{width:4px;height:4px;border-radius:50%;background:var(--deco);flex:none}
.phasepill{display:inline-flex;align-items:center;gap:8px;padding:7px 12px;
   border:1px solid var(--line);border-radius:6px;font:500 13px/1 var(--f-ui);color:var(--ink)}
.spacer{flex:1}
.hpill{display:inline-flex;align-items:center;gap:6px;font:700 12px/16px var(--f-txt);
   background:var(--line-soft);color:var(--ink);padding:3px 10px;border-radius:999px;
   border:0;white-space:nowrap}
.hpill i{width:6px;height:6px;border-radius:50%;background:var(--ink);display:inline-block}
.hpill.hot{background:var(--a-soft);color:var(--brand);cursor:pointer}
.hpill.hot:hover{background:var(--brand);color:var(--on-brand)}
.stamp{font:400 12px/1 var(--f-txt);color:var(--ink2);white-space:nowrap;
   font-variant-numeric:tabular-nums}
.btn{font:600 12px/1 var(--f-ui);color:var(--brand);background:var(--panel);
   border:1px solid var(--brand);border-radius:5px;padding:8px 14px;cursor:pointer;
   white-space:nowrap}
.btn:hover{background:var(--a-tint)}
.btn.solid{background:var(--brand);color:var(--on-brand)}
.btn.solid:hover{background:var(--brand-press)}
.btn.quiet{border-color:var(--line);color:var(--ink2)}
.btn.quiet:hover{background:var(--surface);color:var(--ink)}
.btn.mini{font-size:11px;padding:6px 10px;background:var(--a-soft);color:var(--brand);border:0}
.btn.mini:hover{background:var(--brand);color:var(--on-brand)}
.btn[aria-pressed="true"]{background:var(--a-tint);color:var(--brand);border-color:var(--brand)}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:5px;overflow:hidden}
.seg .btn{border:0;border-radius:0;padding:8px 11px;color:var(--ink2)}
.seg .btn+.btn{border-left:1px solid var(--line)}
.seg .btn[aria-pressed="true"]{background:var(--brand);color:var(--on-brand)}

.mid{flex:1;display:flex;min-height:0}
nav.side{flex:none;width:240px;background:var(--panel);border-right:1px solid var(--line);
   display:flex;flex-direction:column;padding:16px 10px;gap:2px;overflow:auto}
.navhead{font:600 10px/16px var(--f-ui);letter-spacing:.09em;text-transform:uppercase;
   color:var(--ink2);padding:6px 10px 8px}
.nav{display:flex;align-items:center;gap:8px;width:100%;text-align:left;border:0;
   cursor:pointer;padding:10px 12px;border-radius:6px;font:500 14px/20px var(--f-ui);
   background:transparent;color:var(--ink)}
.nav:hover{background:var(--surface)}
.nav[aria-selected="true"]{background:var(--brand);color:var(--on-brand);font-weight:600}
.nav .cnt{margin-left:auto;font:700 11px/16px var(--f-txt);padding:1px 7px;border-radius:999px;
   background:var(--line-soft);color:var(--ink-strong);font-variant-numeric:tabular-nums}
.nav[aria-selected="true"] .cnt{background:rgba(255,255,255,.22);color:var(--on-brand)}
.navfoot{border-top:1px solid var(--line);padding:14px 10px 4px;display:flex;
   flex-direction:column;gap:8px;margin-top:auto}
.navfoot .lg{display:flex;align-items:center;gap:8px}
.navfoot .lg b{font:700 13px/1 var(--f-txt);min-width:26px;font-variant-numeric:tabular-nums}
.navfoot .lg span{font:400 12px/1 var(--f-ui);color:var(--ink2)}
.build{font:400 10px/14px var(--f-txt);color:var(--ink2);margin-top:4px}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block;flex:none;background:var(--deco)}
.sq{width:10px;height:10px;border-radius:3px;display:inline-block;flex:none;background:var(--deco)}
main.pane{flex:1;min-width:0;overflow:auto}
.panel{padding:28px 32px 56px;max-width:1500px;display:flex;flex-direction:column;gap:20px}
.panel.reg{padding:0;max-width:none;gap:0;min-height:100%}
@media (max-width:900px){
  nav.side{width:180px}
  .panel{padding:20px 18px 48px}
}

/* ---------- headings */
.eyebrow{font:600 10px/16px var(--f-ui);letter-spacing:.09em;text-transform:uppercase;
   color:var(--ink2)}
h1.pt{font:700 26px/1.2 var(--f-ui);letter-spacing:-.02em;margin:0;color:var(--ink)}
.panel h1.big{font-size:32px;line-height:40px;margin:2px 0 6px}
p.lead{font:400 15px/1.6 var(--f-txt);color:var(--ink2);margin:0;max-width:70ch}
p.sub{font:400 13px/1.6 var(--f-txt);color:var(--ink2);margin:0;max-width:80ch}
h2.sec{font:700 13px/1 var(--f-ui);color:var(--ink);margin:0;display:flex;
   align-items:baseline;gap:10px;flex-wrap:wrap}
h2.sec .n{font:700 13px/1 var(--f-txt);color:var(--ink2);font-variant-numeric:tabular-nums}
h2.sec .x{font:400 11px/1 var(--f-ui);color:var(--ink2)}
.blk{display:flex;flex-direction:column;gap:8px}

/* ---------- cards */
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;
   box-shadow:var(--shadow)}
.card>.hd{padding:16px 20px;border-bottom:1px solid var(--line);display:flex;
   align-items:center;justify-content:space-between;gap:10px}
.card>.bd{padding:16px 20px}
.pad{padding:20px}

/* ---------- panorama */
.pantop{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;flex-wrap:wrap}
.stepper{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.step{font:500 12px/1 var(--f-ui);padding:8px 14px;border-radius:999px;background:var(--panel);
   color:var(--ink2);border:1px solid var(--line)}
.step.on{background:var(--accent);color:var(--on-a);border-color:var(--accent);font-weight:700}
.hero{background:var(--hero);border-radius:10px;padding:26px 28px;display:grid;
   grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:28px;align-items:center}
.hero .eyebrow{color:var(--hero-dim)}
.hero .col{display:flex;flex-direction:column;gap:14px}
.bar{display:flex;height:18px;border-radius:9px;overflow:hidden;background:var(--hero-track)}
.bar span{display:block}
.stats{display:flex;gap:26px;flex-wrap:wrap}
.stats>div{display:flex;flex-direction:column;gap:2px}
.stats .v{font:700 26px/1 var(--f-ui);letter-spacing:-.02em;color:var(--hero-ink);
   font-variant-numeric:tabular-nums}
.stats .v.zero{color:var(--hero-zero)}
.stats .l{display:flex;align-items:center;gap:6px;font:500 11px/16px var(--f-ui);
   color:var(--hero-txt)}
.metrics{display:flex;flex-direction:column;gap:16px;min-width:260px}
.metric{display:flex;align-items:center;gap:16px}
.metric+.metric{border-top:1px solid var(--hero-rule);padding-top:16px}
.metric .v{font:700 44px/1 var(--f-ui);letter-spacing:-.03em;color:var(--hero-ink);
   font-variant-numeric:tabular-nums}
.metric .v.hi{color:var(--a-soft)}
.metric .u{font:400 12px/1.5 var(--f-txt);color:var(--hero-txt);max-width:38ch}
.cards2{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:20px;
   align-items:start}
.todo{list-style:none;margin:0;padding:6px 20px 18px;counter-reset:t}
.todo li{counter-increment:t;padding:14px 0;border-bottom:1px solid var(--line-soft);
   display:flex;gap:14px;align-items:flex-start}
.todo li:last-child{border-bottom:0}
.todo li::before{content:counter(t,decimal-leading-zero);font:700 12px/20px var(--f-mono);
   color:var(--ink2);min-width:18px}
.todo .t{font:400 14px/22px var(--f-txt)}
.todo .m{font:400 12px/18px var(--f-txt);color:var(--ink2);margin-top:6px}
.quote{border-left:3px solid var(--a-soft);padding-left:16px;font:400 14px/1.7 var(--f-txt);
   color:var(--ink)}
.quote .src{display:block;margin-top:10px;font:400 11px/1 var(--f-ui);color:var(--ink3)}
.sentence{font:400 15px/1.65 var(--f-txt);max-width:80ch}
.sentence strong{color:var(--brand);background:var(--a-tint);padding:0 3px;border-radius:3px}
.caret{display:inline-block;font-size:11px;color:var(--ink3);
   transition:transform 180ms cubic-bezier(.4,0,.2,1)}
[aria-expanded="true"]>.caret,details[open]>summary .caret{transform:rotate(90deg)}
.gloss{padding:0 20px 22px;display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
   gap:18px}
.gloss>div{display:flex;flex-direction:column;gap:4px}
.gloss .k{font:700 11px/16px var(--f-ui);letter-spacing:.06em;text-transform:uppercase;
   color:var(--brand)}
.gloss .v{font:400 13px/1.6 var(--f-txt);color:var(--ink)}
.rowbtn{width:100%;display:flex;align-items:center;gap:10px;background:transparent;border:0;
   padding:16px 20px;cursor:pointer;text-align:left;color:inherit;font:inherit}
.rowbtn h3,.rowbtn .ttl{margin:0;font:700 14px/24px var(--f-ui);color:var(--ink)}
.rowbtn .m{font:400 12px/24px var(--f-txt);color:var(--ink2)}

/* ---------- toolbar (registo) */
.toolbar{position:sticky;top:0;z-index:5;background:var(--panel);
   border-bottom:1px solid var(--line);padding:16px 32px 12px;display:flex;
   flex-direction:column;gap:10px}
.trow{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
.trow.r1{gap:14px}
.counts{font:400 12px/1 var(--f-txt);color:var(--ink2);font-variant-numeric:tabular-nums}
.hint{font:400 12px/1 var(--f-txt);color:var(--brand)}
.flabel{font:600 10px/16px var(--f-ui);letter-spacing:.08em;text-transform:uppercase;
   color:var(--ink2);margin-right:2px}
.vr{width:1px;height:18px;background:var(--line);margin:0 4px}
input[type=search]{font:400 13px/1 var(--f-txt);color:var(--ink);background:var(--panel);
   border:1px solid var(--line);border-radius:6px;padding:9px 12px;min-width:260px;outline:none}
input[type=search]:focus{border-color:var(--brand);box-shadow:0 0 0 3px rgba(255,90,0,.28)}
.chip{font:600 12px/1 var(--f-ui);padding:7px 12px;border-radius:999px;cursor:pointer;
   border:1px solid var(--line);background:var(--panel);color:var(--ink2)}
.chip:hover{border-color:var(--brand);color:var(--brand)}
.chip[aria-pressed="true"]{background:var(--brand);color:var(--on-brand);border-color:var(--brand)}
.chip[aria-pressed="true"][data-tint="accent"]{background:var(--accent);color:var(--on-a);
   border-color:var(--accent)}
.regbody{padding:20px 32px 60px;display:flex;flex-direction:column;gap:26px}

/* ---------- tables */
.tw{background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.tw.scroll{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:var(--fs);font-family:var(--f-txt)}
thead th{text-align:left;background:var(--surface);border-bottom:1px solid var(--line);
   padding:6px 16px;font:600 11px/16px var(--f-ui);letter-spacing:.04em;text-transform:uppercase;
   color:var(--ink2);white-space:nowrap}
tbody td{padding:var(--rowpad);border-bottom:1px solid var(--line-soft);vertical-align:top;
   text-align:left}
tbody tr:last-child td{border-bottom:0}
tbody tr[data-id]{cursor:pointer}
tbody tr[data-id]:hover{background:var(--hover)}
tbody tr.res .prov.idchip{text-decoration:line-through;opacity:.6}
tbody tr.hit{background:var(--a-tint)!important;transition:background .3s}
table.reg{table-layout:fixed}
table.reg th.c-id,table.reg td.c-id{width:96px}
table.reg th.c-crit,table.reg td.c-crit{width:104px}
table.reg th.c-lens,table.reg td.c-lens{width:124px}
table.reg th.c-verif,table.reg td.c-verif{width:116px}
table.reg th.c-ronda,table.reg td.c-ronda{width:74px}
td.c-lens,td.c-verif,td.c-meta{font:400 13px/20px var(--f-txt);color:var(--ink2)}
td.c-ronda{font:400 13px/20px var(--f-mono);color:var(--ink2)}
td.c-claim{overflow-wrap:anywhere}
td.c-claim>div{font:400 13px/20px var(--f-txt);color:var(--ink);padding-right:16px}
.sortb{display:flex;align-items:center;gap:5px;background:transparent;border:0;padding:0;
   cursor:pointer;font:600 11px/16px var(--f-ui);letter-spacing:.04em;text-transform:uppercase;
   color:var(--ink2)}
.sortb:hover{color:var(--brand)}
th[aria-sort] .sortb{font-weight:700;color:var(--brand)}
h2.sec.hasdot::before{content:"";width:10px;height:10px;border-radius:3px;flex:none;
   align-self:center;display:inline-block;background:var(--st-dot,var(--deco))}
td.c-file{font:400 13px/20px var(--f-mono);overflow-wrap:anywhere}
.s-Confirmed{--st-fg:var(--st-Confirmed-fg);--st-bg:var(--st-Confirmed-bg);--st-dot:var(--st-Confirmed-dot)}
.s-Assumed{--st-fg:var(--st-Assumed-fg);--st-bg:var(--st-Assumed-bg);--st-dot:var(--st-Assumed-dot)}
.s-Unknown{--st-fg:var(--st-Unknown-fg);--st-bg:var(--st-Unknown-bg);--st-dot:var(--st-Unknown-dot)}
.s-Conflicted{--st-fg:var(--st-Conflicted-fg);--st-bg:var(--st-Conflicted-bg);--st-dot:var(--st-Conflicted-dot)}
.s-Risky{--st-fg:var(--st-Risky-fg);--st-bg:var(--st-Risky-bg);--st-dot:var(--st-Risky-dot)}
.s-Confirmed .dot,.s-Confirmed .sq,.s-Confirmed.dot,.s-Confirmed.sq{background:var(--st-Confirmed-dot)}
.s-Assumed .dot,.s-Assumed .sq,.s-Assumed.dot,.s-Assumed.sq{background:var(--st-Assumed-dot)}
.s-Unknown .dot,.s-Unknown .sq,.s-Unknown.dot,.s-Unknown.sq{background:var(--st-Unknown-dot)}
.s-Conflicted .dot,.s-Conflicted .sq,.s-Conflicted.dot,.s-Conflicted.sq{background:var(--st-Conflicted-dot)}
.s-Risky .dot,.s-Risky .sq,.s-Risky.dot,.s-Risky.sq{background:var(--st-Risky-dot)}
.critpill{font:700 11px/16px var(--f-txt);border-radius:999px;padding:2px 8px;
   display:inline-block;color:var(--ink3);background:transparent}
.critpill.k-Critical{color:var(--brand);background:var(--a-soft)}
.critpill.k-Med{color:var(--ink-strong);background:var(--line-soft)}
.statepill{font:700 12px/16px var(--f-txt);color:var(--st-fg,var(--brand));
   background:var(--st-bg,var(--a-tint));border-radius:999px;padding:3px 10px;
   display:inline-block;white-space:nowrap}
.clamp{display:-webkit-box;-webkit-line-clamp:var(--clamp);-webkit-box-orient:vertical;
   overflow:hidden}
.empty{font:400 13px/20px var(--f-txt);color:var(--ink2);padding:14px 16px}
.emptycard{background:var(--panel);border:1px dashed var(--line);border-radius:8px;
   padding:40px 24px;text-align:center;display:flex;flex-direction:column;gap:10px;
   align-items:center}
.emptycard .t{font:700 16px/24px var(--f-ui);color:var(--ink)}
.emptycard .m{font:400 13px/20px var(--f-txt);color:var(--ink2)}
.badge{font:400 10px/16px var(--f-ui);letter-spacing:.02em;border:1px solid var(--line);
   border-radius:5px;padding:0 5px;color:var(--ink2);margin-left:5px;white-space:nowrap}
.badge.exp{color:var(--bad);border-color:var(--bad)}
.badge.inf,.badge.mal{color:var(--warn);border-color:var(--warn)}
.tag{font:600 11px/16px var(--f-txt);color:var(--ink2);background:var(--line-soft);
   padding:1px 8px;border-radius:999px;white-space:nowrap}
.sw{font:600 11px/16px var(--f-txt);color:var(--brand);background:var(--a-tint2);
   padding:1px 8px;border-radius:999px;white-space:nowrap}
.sw.decisivo{background:var(--a-soft);color:var(--brand)}
.sw.cosmetico{background:transparent;color:var(--ink3);font-weight:400}
.cmd{font:400 12px/1.6 var(--f-mono);background:var(--hero);color:var(--a-soft);
   padding:2px 8px;border-radius:4px;display:inline-block}
.prov{font:500 11.5px/1.6 var(--f-mono);background:var(--a-soft);color:var(--brand);
   padding:1px 6px;border-radius:4px;cursor:pointer;white-space:nowrap}
.prov:hover{background:var(--brand);color:var(--on-brand)}
.prov.idchip{font-size:12px;line-height:20px;background:var(--st-bg,var(--a-soft));
   color:var(--st-fg,var(--brand))}
.prov.idchip:hover{background:var(--brand);color:var(--on-brand)}
.prov-exp{box-shadow:inset 0 -2px 0 var(--bad)}
.prov-res{background:var(--line-soft);color:var(--ink3);text-decoration:line-through}

/* ---------- notes / agenda */
.note{background:var(--a-soft);border:1px solid var(--a-mid);border-radius:8px;
   padding:16px 20px;display:flex;flex-direction:column;gap:6px;max-width:90ch}
.note .eyebrow{color:var(--brand)}
.note .bdy{font:400 14px/22px var(--f-txt);color:var(--ink)}
.note.quiet{background:var(--panel);border-color:var(--line)}
.note.watch{background:var(--a-tint);border-color:var(--a-mid)}
.tally{display:flex;background:var(--panel);border:1px solid var(--line);border-radius:8px;
   overflow:hidden;flex-wrap:wrap}
.tally>div{flex:1;min-width:150px;padding:16px 18px;display:flex;flex-direction:column;gap:2px}
.tally>div+div{border-left:1px solid var(--line)}
.tally .v{font:700 30px/1.1 var(--f-ui);letter-spacing:-.02em;color:var(--ink);
   font-variant-numeric:tabular-nums}
.tally .l{font:500 11px/16px var(--f-ui);color:var(--ink2)}
.tally .hot{background:var(--a-tint)}
.tally .hot .v{color:var(--brand)}
.qgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(340px,1fr));gap:12px}
.q{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:14px 16px;
   display:flex;flex-direction:column;gap:8px;cursor:pointer;text-align:left;font:inherit;
   color:inherit}
.q:hover{border-color:var(--brand);box-shadow:var(--shadow-lift)}
.q .qh{display:flex;align-items:center;gap:7px;flex-wrap:wrap}
.q .qt{font:500 13px/1.5 var(--f-ui);color:var(--ink)}
.q .qm{display:flex;gap:8px;font:400 12px/1.5 var(--f-txt);color:var(--ink2)}
.q .qm b{font:700 10px/18px var(--f-ui);letter-spacing:.06em;text-transform:uppercase;
   color:var(--ink2);min-width:42px;flex:none}
tbody tr.agrow:hover{background:var(--hover-warm)}

/* ---------- narrativa */
.ev{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--line);
   border-radius:8px;padding:20px 24px}
.ev.story{border-left-color:var(--accent)}
.ev.council{border-left-color:var(--hero)}
.ev.decision{border-left-color:var(--brand)}
.ev .k{font:700 10px/16px var(--f-ui);letter-spacing:.08em;text-transform:uppercase;
   padding:2px 8px;border-radius:999px;background:var(--line-soft);color:var(--ink-strong)}
.ev.story .k{background:var(--a-soft);color:var(--brand)}
.ev.council .k{background:var(--line-soft);color:var(--ink)}
.ev .meta{font:400 11px/16px var(--f-txt);color:var(--ink2)}
.ev h2{font:700 18px/26px var(--f-ui);margin:0 0 10px;color:var(--ink)}
.ev .top{display:flex;align-items:center;gap:10px;margin-bottom:6px;flex-wrap:wrap}

/* ---------- etapas (phase documents) */
.doc{background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.doc>summary{list-style:none;cursor:pointer;padding:16px 20px;display:flex;
   flex-direction:column;gap:4px;border-bottom:1px solid var(--line-soft)}
.doc>summary::-webkit-details-marker{display:none}
.doc>summary:hover{background:var(--surface)}
.doc>summary .t{display:flex;align-items:center;gap:10px}
.doc>summary h3{margin:0;font:700 16px/24px var(--f-ui);color:var(--ink)}
.doc>summary .m{font:400 11px/18px var(--f-txt);color:var(--ink3);padding-left:22px}
.docbody{padding:18px 24px 24px}
.trunc{margin-top:18px;background:var(--a-tint);border:1px solid var(--a-mid);border-radius:6px;
   padding:12px 16px;font:400 13px/1.6 var(--f-txt);color:var(--brand)}

/* ---------- rich text (markdown bodies) */
.rich{font:400 14px/1.65 var(--f-txt);color:var(--ink)}
.rich p{margin:0 0 12px}
.rich h3.md-h,.rich h4.md-h,.rich h5.md-h{font-family:var(--f-ui);margin:22px 0 8px;
   color:var(--ink2);font-size:12px;letter-spacing:.07em;text-transform:uppercase;font-weight:700}
.rich code{font:400 12px/1.5 var(--f-mono);background:var(--line-soft);padding:1px 5px;
   border-radius:4px}
.rich pre{background:var(--line-soft);padding:12px;border-radius:6px;overflow-x:auto;
   font:400 12px/1.5 var(--f-mono)}
.rich blockquote{margin:12px 0;padding:12px 16px;background:var(--a-tint);
   border-left:3px solid var(--brand);border-radius:0 6px 6px 0;font-size:13px}
.rich hr{border:0;border-top:1px solid var(--line);margin:18px 0}
.rich ul,.rich ol{margin:0 0 12px;padding-left:20px}
.rich li{margin:3px 0}
.rich table{margin:10px 0;font-size:13px;border:1px solid var(--line);border-radius:6px}
.rich th{background:var(--surface);white-space:normal;vertical-align:bottom}
.rich td{border-bottom:1px solid var(--line-soft);padding:6px 10px;vertical-align:top;
   overflow-wrap:anywhere}
.rich .tw{margin:10px 0}
.rich>p,.rich>ul,.rich>ol,.rich>blockquote{max-width:82ch}
del{opacity:.55}

/* ---------- drawer / popover / blocker */
#dwbg{position:fixed;inset:0;z-index:40;background:rgba(0,0,0,.4);opacity:0;
   pointer-events:none;transition:opacity .18s ease-out}
#dwbg.on{opacity:1;pointer-events:auto}
#dw{position:fixed;top:0;right:0;bottom:0;width:min(560px,92vw);background:var(--panel);
   border-left:1px solid var(--line);box-shadow:-20px 0 40px rgba(0,0,0,.15);z-index:41;
   display:flex;flex-direction:column;transform:translateX(102%);visibility:hidden;
   transition:transform .18s ease-out}
#dw.on{transform:none;visibility:visible}
#dw .dwh{flex:none;padding:18px 24px;border-bottom:1px solid var(--line);display:flex;
   align-items:center;gap:12px;flex-wrap:wrap}
#dw .dwh .did{font:500 14px/22px var(--f-mono);color:var(--ink)}
#dw .dwh .lens{font:400 12px/1 var(--f-ui);color:var(--ink2)}
#dw .dwb{flex:1;overflow:auto;padding:22px 24px 40px;display:flex;flex-direction:column;gap:20px}
#dw .claim{font:400 15px/1.65 var(--f-txt);color:var(--ink)}
#dw .lbl{font:600 10px/16px var(--f-ui);letter-spacing:.09em;text-transform:uppercase;
   color:var(--ink2);margin-bottom:6px}
#dw .prosev{font:400 13px/1.6 var(--f-txt);color:var(--ink2)}
#dw .tiles{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
#dw .tile{background:var(--surface);border:1px solid var(--line);border-radius:6px;
   padding:10px 12px}
#dw .tile .k{font:600 10px/16px var(--f-ui);letter-spacing:.06em;text-transform:uppercase;
   color:var(--ink2)}
#dw .tile .v{font:500 13px/20px var(--f-txt);color:var(--ink);overflow-wrap:anywhere}
#dw .alert{background:var(--a-tint);border:1px solid var(--a-mid);border-radius:6px;
   padding:12px 14px;font:400 13px/1.6 var(--f-txt);color:var(--brand)}
#pop{position:fixed;z-index:60;max-width:440px;background:var(--panel);border:1px solid var(--line);
   border-radius:8px;padding:10px 13px;box-shadow:var(--shadow);font:400 12.5px/1.5 var(--f-txt);
   display:none;color:var(--ink)}
#pop b{display:block;margin-bottom:3px}
#blk{position:fixed;left:0;right:0;bottom:0;z-index:80;background:var(--brand);
   color:var(--on-brand);padding:9px 16px;font:400 13px/1.5 var(--f-txt);display:none;
   text-align:center}

/* ---------- error page shell (error_page reuses .wrap/.note/.foot) */
.wrap{max-width:1000px;margin:0 auto;padding:24px 22px 80px}
.foot{font:400 11.5px/1.6 var(--f-txt);color:var(--ink2);margin-top:34px;
   border-top:1px solid var(--line);padding-top:12px;max-width:90ch;
   font-variant-numeric:tabular-nums}
pre{background:var(--line-soft);padding:12px;border-radius:8px;overflow-x:auto;
    font:400 12px/1.5 var(--f-mono)}

@media print{
  .noprint{display:none!important}
  html,body{background:#fff}
  .app{height:auto!important;overflow:visible!important;display:block!important}
  .mid{display:block!important}
  main.pane{overflow:visible!important;height:auto!important}
  .panel{padding:0 0 12px!important;max-width:none!important;display:block!important}
  .panel::before{content:attr(data-title);display:block;font:700 20px/1.3 var(--f-ui);
     margin:16px 0 10px}
  .toolbar{position:static!important}
  .clamp{display:block;-webkit-line-clamp:none;overflow:visible}
  .card,.tw,.q,.ev,.doc{box-shadow:none;break-inside:avoid}
  tr,.ev,.q{break-inside:avoid}
  .hero{background:#fff;color:#000;border:1px solid var(--line)}
  .hero .eyebrow,.hero .u,.hero .l{color:#333}
  .hero .v{color:#000}
  a[href]::after{content:""}
}
"""

JS = """
(function(){
  var D = JSON.parse(document.getElementById("aisa-data").textContent);
  var KEY = "aisa.dash." + D.slug;
  var TABS = D.tabs || ["panorama"];
  // The URL carries what is worth sharing -- the open separator and the open row.
  // Everything else (filters, sort, theme, density) is a per-reader preference and
  // lives in localStorage, so a pasted link never arrives pre-filtered by accident.
  var S = {tab:TABS[0], drawer:null, q:"", states:[], lenses:[], crits:[], rondas:[],
           resolved:false, exponly:false, sortKey:null, sortDir:"asc", narr:"todos",
           theme:"auto", density:"cosy", paused:false, gloss:false, scroll:0};
  var PREFS = ["q","states","lenses","crits","rondas","resolved","exponly","sortKey",
               "sortDir","narr","theme","density","paused","gloss","scroll"];

  function $(s,r){ return (r||document).querySelector(s); }
  function $$(s,r){ return Array.prototype.slice.call((r||document).querySelectorAll(s)); }
  function esc(s){ var d=document.createElement("i"); d.textContent = s==null?"":String(s); return d.innerHTML; }
  var pane = $("#pane");

  function loadPrefs(){
    var raw = null;
    // file:// partitions localStorage to the opaque null origin: it can be missing, and
    // where it exists it is shared by every local dashboard -> key per slug.
    try{ raw = JSON.parse(localStorage.getItem(KEY) || "null"); }catch(e){}
    if(raw) PREFS.forEach(function(k){ if(k in raw) S[k] = raw[k]; });
  }
  function savePrefs(){
    var blob = {};
    PREFS.forEach(function(k){ blob[k] = S[k]; });
    try{ localStorage.setItem(KEY, JSON.stringify(blob)); }catch(e){}
  }
  function readHash(){
    var h = (location.hash || "").replace(/^#/, "").split("/");
    if(h[0] && TABS.indexOf(h[0]) >= 0) S.tab = h[0];
    if(h[1] && D.ids[h[1]]) S.drawer = h[1];
  }
  function writeHash(){
    var h = "#" + S.tab + (S.drawer ? "/" + S.drawer : "");
    if(location.hash !== h){ try{ history.replaceState(null, "", h); }catch(e){} }
  }
  function save(){ savePrefs(); writeHash(); }

  // ---- chrome
  function applyTheme(){
    var el = document.documentElement;
    if(S.theme === "auto") el.removeAttribute("data-theme"); else el.setAttribute("data-theme", S.theme);
    var b = $("#theme"); if(b) b.textContent = {auto:"tema auto",light:"claro",dark:"escuro"}[S.theme];
    el.setAttribute("data-density", S.density);
    $$("[data-dens]").forEach(function(x){
      x.setAttribute("aria-pressed", x.dataset.dens === S.density ? "true" : "false"); });
  }
  function applyTab(){
    $$(".nav").forEach(function(n){
      var on = n.dataset.tab === S.tab;
      n.setAttribute("aria-selected", on ? "true" : "false");
      n.tabIndex = on ? 0 : -1;
    });
    $$(".panel").forEach(function(p){ p.hidden = p.dataset.tab !== S.tab; });
  }

  // ---- registo: filter, sort, count
  function tokens(v){ return (v||"").split(/[+,\\/&]| e /).map(function(s){return s.trim();}).filter(Boolean); }
  var CRIT_RANK = {Critical:0, Med:1, Low:2, "":3};
  function rowMatch(tr, q){
    if(S.states.length && S.states.indexOf(tr.dataset.state) < 0) return false;
    if(S.lenses.length && !tokens(tr.dataset.lens).some(function(l){ return S.lenses.indexOf(l) >= 0; })) return false;
    if(S.crits.length && S.crits.indexOf(tr.dataset.crit || "\\u2014") < 0) return false;
    if(S.rondas.length && S.rondas.indexOf(tr.dataset.ronda) < 0) return false;
    if(!S.resolved && tr.dataset.resolved === "1") return false;
    if(S.exponly && tr.dataset.expired !== "1") return false;
    if(q && (tr.dataset.text || "").indexOf(q) < 0) return false;
    return true;
  }
  function sortVal(tr){
    if(S.sortKey === "crit") return CRIT_RANK[tr.dataset.crit || ""];
    if(S.sortKey === "lens") return tr.dataset.lens || "";
    if(S.sortKey === "claim") return tr.dataset.text || "";
    if(S.sortKey === "verif") return tr.dataset.verif || "";
    if(S.sortKey === "ronda") return tr.dataset.ronda || "";
    return tr.dataset.id || "";
  }
  function applySort(){
    var dir = S.sortDir === "desc" ? -1 : 1;
    $$("table.reg tbody").forEach(function(tb){
      if(!tb._orig) tb._orig = $$("tr", tb);
      var rows = tb._orig.slice();
      if(S.sortKey){
        rows.sort(function(a,b){ var x=sortVal(a), y=sortVal(b);
          return (x>y?1:x<y?-1:0) * dir || (a.dataset.id > b.dataset.id ? 1 : -1); });
      }
      rows.forEach(function(r){ tb.appendChild(r); });
    });
    $$(".sortb").forEach(function(sb){
      var on = sb.dataset.sort === S.sortKey, th = sb.closest("th");
      if(th){
        if(on) th.setAttribute("aria-sort", S.sortDir === "desc" ? "descending" : "ascending");
        else th.removeAttribute("aria-sort");
      }
      var ar = $(".ar", sb);
      if(ar) ar.textContent = on ? (S.sortDir === "desc" ? "\\u2193" : "\\u2191") : "";
    });
  }
  function applyFilters(){
    var q = S.q.trim().toLowerCase();
    $$("tr[data-id]").forEach(function(tr){ tr.hidden = !rowMatch(tr, q); });
    var shown = 0;
    $$(".regblock").forEach(function(b){
      var vis = $$("tr[data-id]", b).filter(function(r){ return !r.hidden; }).length;
      // .aux blocks (the reconfirm list) repeat ids that already live in a state block --
      // counting them would inflate "visiveis" and export the same row twice.
      if(!b.classList.contains("aux")) shown += vis;
      b.hidden = vis === 0;
      var c = $("[data-count-state]", b);
      if(c) c.textContent = vis;
    });
    var reg = $("#regempty"); if(reg) reg.hidden = shown > 0;
    var cnt = $("#regcount");
    if(cnt) cnt.textContent = shown + " vis\\u00edveis \\u00b7 " + D.counts.live + " vivos \\u00b7 "
        + D.counts.resolved + " resolvidos \\u00b7 " + D.counts.total + " no total";
    // the agenda cards carry the same ids, so the same filters apply there
    $$(".q[data-id]").forEach(function(el){
      var r = D.ids[el.dataset.id] || {}, ok = true;
      if(S.lenses.length) ok = tokens(r.l).some(function(l){ return S.lenses.indexOf(l) >= 0; });
      if(ok && S.crits.length && S.crits.indexOf(r.k || "\\u2014") < 0) ok = false;
      if(ok && S.rondas.length && S.rondas.indexOf(r.r || "") < 0) ok = false;
      if(ok && q && (el.dataset.text || "").indexOf(q) < 0) ok = false;
      el.hidden = !ok;
    });
  }
  function syncControls(){
    $$(".chip[data-facet]").forEach(function(c){
      c.setAttribute("aria-pressed", (S[c.dataset.facet] || []).indexOf(c.dataset.value) >= 0 ? "true":"false"); });
    var x;
    if((x = $("#f-res"))) x.setAttribute("aria-pressed", S.resolved ? "true":"false");
    if((x = $("#f-exp"))) x.setAttribute("aria-pressed", S.exponly ? "true":"false");
    if((x = $("#f-q"))) x.value = S.q;
    $$(".chip[data-narr]").forEach(function(c){
      c.setAttribute("aria-pressed", c.dataset.narr === S.narr ? "true":"false"); });
    $$(".ev").forEach(function(e){
      e.hidden = !(S.narr === "todos"
        || (S.narr === "story" ? e.dataset.kind === "story" : e.dataset.kind !== "story")); });
    var g = $("#gloss"), gb = $("#glossbtn");
    if(g){ g.hidden = !S.gloss; gb.setAttribute("aria-expanded", S.gloss ? "true":"false"); }
  }
  function clearFilters(){
    S.states=[]; S.lenses=[]; S.crits=[]; S.rondas=[]; S.q=""; S.resolved=false; S.exponly=false;
    syncControls(); applyFilters(); save();
  }

  // ---- CSV of exactly what is on screen, in the order it is on screen
  function exportCsv(){
    var head = ["id","estado","criticidade","perspectiva","afirmacao","verificado","ronda","resolvida"];
    var lines = [head.join(",")];
    $$("table.reg tbody tr[data-id]").forEach(function(tr){
      if(tr.hidden) return;
      var r = D.ids[tr.dataset.id] || {};
      var claim = (r.c || "").replace(/\\s+/g, " ").trim();
      var cells = [tr.dataset.id, D.stlabel[tr.dataset.state] || tr.dataset.state,
                   tr.dataset.crit || "", tr.dataset.lens || "", claim, r.v || "",
                   tr.dataset.ronda || "", tr.dataset.resolved === "1" ? "sim" : "nao"];
      lines.push(cells.map(function(c){ return '"' + String(c).replace(/"/g, '""') + '"'; }).join(","));
    });
    var blob = new Blob(["\\ufeff" + lines.join("\\r\\n")], {type:"text/csv;charset=utf-8"});
    var a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = D.slug + "-registo.csv";
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 2000);
  }

  // ---- drawer + hover popover
  var pop = $("#pop"), dw = $("#dw"), dwbg = $("#dwbg"), lastFocus = null;
  function md(t){
    return esc(t == null ? "" : t)
      .replace(/\\*\\*(.+?)\\*\\*/g, "<strong>$1</strong>")
      .replace(/`([^`]+)`/g, "<code>$1</code>");
  }
  function tile(k, v){
    return '<div class="tile"><div class="k">' + k + '</div><div class="v">' + v + "</div></div>";
  }
  function drawerHtml(id){
    var r = D.ids[id]; if(!r) return null;
    var o = [];
    o.push('<div class="dwh s-' + esc(r.s) + '"><span class="did">' + esc(id) + "</span>"
      + '<span class="statepill">' + esc(D.stlabel[r.s] || r.s) + "</span>"
      + '<span class="lens">' + esc(r.l || "-") + "</span><span class=\\"spacer\\"></span>"
      + '<button class="btn quiet" id="dw-x">Fechar</button></div>');
    o.push('<div class="dwb">');
    o.push('<div class="claim">' + md(r.c) + "</div>");
    if(r.e){
      o.push('<div class="alert">Esta linha precisa de reconfirmar \\u2014 passou o prazo h\\u00e1 '
        + r.d + ' dias. <span class="cmd">/answer --revalidate ' + esc(id) + "</span></div>");
    }
    if(r.dp){
      var extra = (r.dups || []).map(function(x){
        return "linha " + x.ln + " \\u00b7 " + esc(D.stlabel[x.s] || x.s) + " \\u00b7 "
             + esc(x.l || "-") + ": " + esc(x.c); }).join("<br>");
      o.push('<div class="alert"><b>Este identificador aparece em mais do que uma linha.</b>'
        + (extra ? "<br>" + extra : "")
        + "<br>Renomear uma delas no shared-understanding.md \\u2014 at\\u00e9 l\\u00e1, citar este "
        + "identificador \\u00e9 amb\\u00edguo.</div>");
    }
    if(r.su){
      o.push('<div><div class="lbl">' + esc(D.support[r.s] || "proveni\\u00eancia")
        + '</div><div class="prosev">' + md(r.su) + "</div></div>");
    }
    if(r.ex){
      o.push('<div><div class="lbl">mitiga\\u00e7\\u00e3o proposta</div><div class="prosev">'
        + md(r.ex) + "</div></div>");
    }
    var tiles = [];
    tiles.push(tile("passagem", esc(r.r || "\\u2014")));
    tiles.push(tile("verificado", esc(r.v || "\\u2014") + (r.vi ? ' <span class="badge inf">da passagem</span>' : "")));
    tiles.push(tile("validade", esc(r.va || "\\u2014")));
    tiles.push(tile("expira", esc(r.x || "\\u2014")));
    if(r.k) tiles.push(tile("gravidade", '<span class="critpill k-' + esc(r.k) + '">' + esc(r.k) + "</span>"
        + (r.kr && r.kr !== r.k ? ' <span class="badge">no registo: ' + esc(r.kr) + "</span>" : "")));
    if(r.cu) tiles.push(tile("custo da resposta", esc(D.custo[r.cu] || r.cu)
        + (r.ci ? ' <span class="badge inf">por omiss\\u00e3o</span>' : "")));
    if(r.sc) tiles.push(tile("o que muda", '<span class="sw ' + esc(r.sc) + '">'
        + esc(D.swing[r.sc] || r.sc) + "</span>"));
    tiles.push(tile("linha no ficheiro", esc(r.ln) + (r.ml ? ' <span class="badge mal">reparada</span>' : "")));
    if(r.w && r.w.length) tiles.push(tile("veio de", r.w.map(esc).join(", ")));
    if(r.rt && r.rt.length) tiles.push(tile("resolvida para", r.rt.map(esc).join(", ")));
    o.push('<div class="tiles">' + tiles.join("") + "</div>");
    o.push('<div class="prosev">Fonte de verdade: <code>shared-understanding.md</code>, linha '
      + esc(r.ln) + ".</div>");
    o.push("</div>");
    return o.join("");
  }
  function focusables(){
    return $$('button,[href],input,select,textarea,[tabindex]:not([tabindex="-1"])', dw)
      .filter(function(el){ return !el.disabled && el.offsetParent !== null; });
  }
  function openDrawer(id){
    var html = drawerHtml(id); if(!html) return;
    dw.innerHTML = html;
    if(document.activeElement && document.activeElement !== document.body
       && !dw.contains(document.activeElement)) lastFocus = document.activeElement;
    dwbg.hidden = false; dwbg.classList.add("on"); dw.classList.add("on");
    S.drawer = id; writeHash();
    var f = focusables();
    (f[0] || dw).focus();
    hidePop();
  }
  function closeDrawer(){
    if(!dw.classList.contains("on")) return;
    dw.classList.remove("on"); dwbg.classList.remove("on");
    setTimeout(function(){ if(!dw.classList.contains("on")) dwbg.hidden = true; }, 220);
    S.drawer = null; writeHash();
    if(lastFocus && lastFocus.focus){ lastFocus.focus(); lastFocus = null; }
  }
  function showPop(el){
    var r = D.ids[el.dataset.id]; if(!r) return;
    var b = ["<b>" + esc(el.dataset.id) + " \\u00b7 " + esc(D.stlabel[r.s] || r.s) + "</b>", esc(r.c)];
    if(r.v) b.push("verificado " + esc(r.v) + (r.va ? " (" + esc(r.va) + ")" : ""));
    if(r.e) b.push("<b>precisa de reconfirmar</b> \\u2014 h\\u00e1 " + r.d + " dias");
    if(r.dp) b.push("<b>identificador repetido</b> \\u2014 " + (1 + (r.dups ? r.dups.length : 0)) + " linhas");
    b.push("clicar para ver o detalhe");
    pop.innerHTML = b.join("<br>");
    pop.style.display = "block";
    var q = el.getBoundingClientRect();
    pop.style.top = Math.min(q.bottom + 7, window.innerHeight - pop.offsetHeight - 10) + "px";
    pop.style.left = Math.max(8, Math.min(q.left, window.innerWidth - pop.offsetWidth - 16)) + "px";
  }
  function hidePop(){ pop.style.display = "none"; }

  function goTab(tab){
    S.tab = tab; applyTab(); if(pane) pane.scrollTop = 0; save();
  }

  // ---- refresh. Served over HTTP the page asks /__build whether anything changed and
  // reloads only then. Opened as file:// it cannot fetch, so it falls back to the blind
  // timed reload and says so when even that is refused.
  var served = location.protocol.indexOf("http") === 0;
  var secs = D.reload|0, left = secs, checking = false, wrongServer = false;

  function doReload(){ S.scroll = pane ? pane.scrollTop : 0; savePrefs(); location.reload(); }

  // The server answers with its identity, not only a build hash. A port is not an
  // identity: server A can die, B take its port, and a reattach then serve B's
  // engagement under A's URL. If page and server disagree, stop polling and say so.
  function checkBuild(){
    if(checking || wrongServer) return;
    checking = true;
    fetch("__build", {cache:"no-store"})
      .then(function(r){ return r.ok ? r.text() : null; })
      .then(function(t){
        checking = false;
        if(!t || !t.trim()) return;
        var doc = null;
        try{ doc = JSON.parse(t); }catch(e){ doc = null; }
        if(!doc || typeof doc !== "object") return;      // pre-1.5.2 server: do nothing
        if(doc.slug && D.slug && doc.slug !== D.slug){
          wrongServer = true;
          var el = $("#cd");
          if(el) el.textContent = "servidor de outro projecto (" + doc.slug + ")";
          var b = $("#blk");
          if(b){
            b.textContent = "Esta p\\u00e1gina \\u00e9 do projecto " + D.slug + ", mas quem responde"
              + " neste endere\\u00e7o serve " + doc.slug + ". Nada foi actualizado. Fechar o"
              + " servidor e correr /dashboard --serve no projecto certo.";
            b.style.display = "block";
          }
          return;
        }
        if(doc.build && doc.build !== D.build) doReload();
      })
      .catch(function(){ checking = false; });
  }
  function maybeRefresh(){
    var ae = document.activeElement;
    if(dw.classList.contains("on")
       || (ae && (ae.tagName === "INPUT" || ae.tagName === "TEXTAREA"))) return;
    if(served){ checkBuild(); return; }
    if(document.hidden) return;
    doReload();
    setTimeout(function(){ var b = $("#blk"); if(b) b.style.display = "block"; }, 1200);
  }
  function tick(){
    var el = $("#cd");
    if(wrongServer) return;
    if(S.paused){ if(el) el.textContent = "em pausa"; return; }
    left--;
    if(el) el.textContent = served ? "a vigiar" : (Math.max(0, left) + "s");
    if(left > 0) return;
    left = secs;
    maybeRefresh();
  }
  document.addEventListener("visibilitychange", function(){
    if(!document.hidden && !S.paused){ left = secs; maybeRefresh(); }
  });

  // ---- boot
  loadPrefs(); readHash(); applyTheme(); applyTab(); syncControls(); applySort(); applyFilters();
  if(pane && S.scroll) pane.scrollTop = S.scroll;
  if(S.drawer) openDrawer(S.drawer);
  writeHash();

  document.addEventListener("click", function(e){
    var t = e.target, b = t.closest ? t.closest("button,a,.q,tr[data-id],.prov") : null;
    if(t.closest && t.closest(".prov")){
      var p = t.closest(".prov");
      e.preventDefault(); e.stopPropagation(); openDrawer(p.dataset.id); return;
    }
    if(!b) { if(!t.closest || !t.closest("#dw")){ hidePop(); closeDrawer(); } return; }
    if(b.id === "dw-x"){ closeDrawer(); return; }
    if(b.dataset && b.dataset.tab){ goTab(b.dataset.tab); return; }
    if(b.classList.contains("chip") && b.dataset.facet){
      var arr = S[b.dataset.facet], i = arr.indexOf(b.dataset.value);
      if(i < 0) arr.push(b.dataset.value); else arr.splice(i, 1);
      syncControls(); applyFilters(); save(); return;
    }
    if(b.dataset && b.dataset.narr){ S.narr = b.dataset.narr; syncControls(); save(); return; }
    if(b.id === "f-res"){ S.resolved = !S.resolved; syncControls(); applyFilters(); save(); return; }
    if(b.id === "f-exp"){ S.exponly = !S.exponly; syncControls(); applyFilters(); save(); return; }
    if(b.id === "f-clear" || (b.dataset && b.dataset.clear)){ clearFilters(); return; }
    if(b.id === "csv"){ exportCsv(); return; }
    if(b.id === "glossbtn"){ S.gloss = !S.gloss; syncControls(); save(); return; }
    if(b.id === "theme"){ S.theme = {auto:"light",light:"dark",dark:"auto"}[S.theme]; applyTheme(); save(); return; }
    if(b.dataset && b.dataset.dens){ S.density = b.dataset.dens; applyTheme(); save(); return; }
    if(b.id === "pause"){
      S.paused = !S.paused;
      b.setAttribute("aria-pressed", S.paused ? "true":"false");
      b.textContent = S.paused ? "retomar" : "pausar";
      left = secs; save(); return;
    }
    if(b.id === "printtab"){ window.print(); return; }
    if(b.id === "printall"){
      $$(".panel").forEach(function(p){ p.hidden = false; });
      window.print(); return;
    }
    if(b.dataset && b.dataset.sort){
      S.sortDir = (S.sortKey === b.dataset.sort && S.sortDir === "asc") ? "desc" : "asc";
      S.sortKey = b.dataset.sort;
      applySort(); save(); return;
    }
    if(b.classList.contains("q") && b.dataset.id){ openDrawer(b.dataset.id); return; }
    var row = t.closest && t.closest("tr[data-id]");
    if(row){ openDrawer(row.dataset.id); return; }
  });

  document.addEventListener("keydown", function(e){
    if(e.key === "Escape"){ closeDrawer(); hidePop(); return; }
    var ae = document.activeElement;
    var typing = ae && (ae.tagName === "INPUT" || ae.tagName === "TEXTAREA");
    if(dw.classList.contains("on") && e.key === "Tab"){
      var f = focusables(); if(!f.length) return;
      var first = f[0], last = f[f.length-1];
      if(e.shiftKey && (ae === first || !dw.contains(ae))){ e.preventDefault(); last.focus(); }
      else if(!e.shiftKey && ae === last){ e.preventDefault(); first.focus(); }
      return;
    }
    if(e.key === "/" && !typing){
      e.preventDefault();
      if(S.tab !== "estado") goTab("estado");
      var q = $("#f-q"); if(q) q.focus();
      return;
    }
    if((e.key === "Enter" || e.key === " ") && ae && ae.matches
       && (ae.matches("tr[data-id]") || ae.matches(".prov")
           || ae.matches(".q[data-id]"))){
      e.preventDefault(); openDrawer(ae.dataset.id); return;
    }
    if(ae && ae.classList && ae.classList.contains("nav")){
      var navs = $$(".nav"), i = navs.indexOf(ae), d = 0;
      if(e.key === "ArrowDown" || e.key === "ArrowRight") d = 1;
      else if(e.key === "ArrowUp" || e.key === "ArrowLeft") d = -1;
      else if(e.key === "Home") d = -i;
      else if(e.key === "End") d = navs.length - 1 - i;
      else return;
      e.preventDefault();
      var n = navs[(i + d + navs.length) % navs.length];
      goTab(n.dataset.tab); n.focus();
    }
  });

  document.addEventListener("mouseover", function(e){
    if(e.target.classList && e.target.classList.contains("prov")) showPop(e.target); });
  document.addEventListener("mouseout", function(e){
    if(e.target.classList && e.target.classList.contains("prov")) hidePop(); });
  window.addEventListener("afterprint", applyTab);
  window.addEventListener("hashchange", function(){
    readHash(); applyTab();
    if(S.drawer) openDrawer(S.drawer); else closeDrawer();
  });
  var qd, qi = $("#f-q");
  if(qi) qi.addEventListener("input", function(e){
    S.q = e.target.value;
    clearTimeout(qd); qd = setTimeout(function(){ applyFilters(); save(); }, 120);
  });
  if(pane) pane.addEventListener("scroll", function(){
    clearTimeout(pane._t);
    pane._t = setTimeout(function(){ S.scroll = pane.scrollTop; savePrefs(); }, 400);
  });
  var pb = $("#pause");
  if(pb){ pb.setAttribute("aria-pressed", S.paused ? "true":"false");
          pb.textContent = S.paused ? "retomar" : "pausar"; }
  if(secs > 0) setInterval(tick, 1000);
})();
"""


# ------------------------------------------------------------------- renderer

STATE_LABEL = {
    "Confirmed": "Confirmado", "Assumed": "Assumido", "Unknown": "Por saber",
    "Conflicted": "Em conflito", "Risky": "Risco",
}
# `enquadramento` and `R-00` are the owner's declaration, not a lens and not a round
# of lenses -- the chips say so (P-0).
FACET_LABEL = {
    "lenses": {"enquadramento": "enquadramento (dono)"},
    "rondas": {"R-00": "R-00 · enquadramento"},
    "crits": {"—": "sem classificação"},
}
SUPPORT_LABEL = {
    "Confirmed": "evidência", "Assumed": "base do que assumimos", "Unknown": "quem responde",
    "Conflicted": "partes", "Risky": "impacto",
}
CUSTO_LABEL = {"email": "email", "documento": "documento", "reuniao": "reunião",
               "spike": "trabalho técnico"}
# The class is the machine value (also a CSS class); the label is what a human reads
# (glossary.md, *Como se diz ao utilizador*): what the answer changes, not the class name.
SWING_LABEL = {"decisivo": "muda o caminho", "dimensionante": "muda o tamanho",
               "cosmetico": "não muda nada"}


def swing_label(cls: str) -> str:
    """Business wording for the class chip. An unread class says so (DEF-P4-01):
    an empty chip would read as `nada a assinalar`, which is the opposite."""
    return SWING_LABEL.get(cls, cls or "peso por classificar")
CRIT_LABEL = {"Critical": "grave", "Med": "média", "Low": "baixa"}
# The chip for rows with no classification. The JS reads the same em dash from
# `data-crit || "\u2014"`, so the two sides cannot drift.
CRIT_NONE = "—"
PHASES = [(k, PHASE_LABEL[k]) for k in ("discovery", "framing", "options", "decision")]

# One grid for every state: id, how bad it is, which perspective saw it, the claim, when
# it was verified, which passagem wrote it. The full SU schema is never lost -- every
# column that leaves the grid reappears in the row drawer, and shared-understanding.md
# stays the source of truth.
REG_COLS = [("id", "id", "c-id"), ("crit", "gravidade", "c-crit"),
            ("lens", "perspectiva", "c-lens"), ("claim", "afirmação", "c-claim"),
            ("verif", "verificado em", "c-verif"), ("ronda", "passagem", "c-ronda")]

TAB_SPEC = [
    ("panorama", "Panorama", ""),
    ("outputs", "Etapas", "Outputs de fase: frame.md, options.md, premortem, síntese, blueprint"),
    ("agenda", "Agenda", "Meeting agenda: Unknown por custo e swing"),
    ("estado", "Registo", "Shared Understanding: Confirmed · Assumed · Unknown · Conflicted · Risky"),
    ("narrativa", "Narrativa", "story.md, council-log.md, decisions.md"),
    ("artefactos", "Ficheiros", "Artefactos do engagement"),
]


def _ids_payload(rows: list[dict]) -> dict:
    """Everything the drawer needs. What leaves the grid must land here."""
    out = {}
    for r in rows:
        rec = {
            "s": r["state"], "l": r["lens"], "c": re.sub(r"\s+", " ", r["claim"]).strip(),
            "r": r["ronda"], "ln": r["line"],
        }
        if r["support"]:
            rec["su"] = re.sub(r"\s+", " ", r["support"]).strip()
        if r["extra"]:
            rec["ex"] = re.sub(r"\s+", " ", r["extra"]).strip()
        if r["criticidade"]:
            rec["k"] = r["criticidade"]
            rec["kr"] = r["criticidade_raw"]
        if r["state"] == "Unknown":
            rec["cu"] = r["custo"]
            rec["ci"] = bool(r["custo_inferred"])
            rec["sc"] = r["swing_class"]
            rec["st"] = r["swing_text"]
        if r["verificado_em"]:
            rec["v"] = r["verificado_em"]
            rec["va"] = r["validade"]
            rec["vi"] = bool(r["verificado_em_source"].startswith("inferido"))
            rec["x"] = r["expires_on"]
        if r["expired"]:
            rec["e"] = True
            rec["d"] = r["days_overdue"]
        if r["was"]:
            rec["w"] = r["was"]
        if r["resolved"]:
            rec["re"] = True
            if r["resolved_to"]:
                rec["rt"] = r["resolved_to"]
        if r["malformed"]:
            rec["ml"] = True
        if r.get("duplicate_id"):
            rec["dp"] = True
        if r["id"] in out:
            # Do not overwrite: the drawer shows the first row and lists the others,
            # so a duplicated id reads as the defect it is instead of silently
            # resolving to whichever row the parser happened to see last (F01).
            out[r["id"]].setdefault("dups", []).append(
                {"s": rec["s"], "l": rec["l"], "ln": rec["ln"], "c": rec["c"]})
            continue
        out[r["id"]] = rec
    return out


def _age(iso: str, today: date) -> str:
    d = _as_date(iso)
    if d is None:
        return ""
    days = (today - d).days
    if days < 45:
        return "ha {}d".format(max(days, 0))
    months = round(days / 30.44)
    if months < 24:
        return "ha {}m".format(months)
    return "ha {}a".format(round(months / 12))


def _chips(facet: str, values: list[str], label: str, tint: str = "") -> str:
    if not values:
        return ""
    labels = FACET_LABEL.get(facet, {})
    inner = "".join(
        '<button class="chip" data-facet="{}" data-value="{}"{} aria-pressed="false">{}</button>'.format(
            facet, esc(v), ' data-tint="{}"'.format(tint) if tint else "",
            esc(labels.get(v) or STATE_LABEL.get(v) or CRIT_LABEL.get(v) or v))
        for v in values)
    return '<span class="flabel">{}</span>{}'.format(esc(label), inner)


def _row_attrs(r: dict, su: bool = False) -> str:
    """su=True marks the canonical SU-section row. The reconfirm and critical tables
    repeat the same ids, so only the canonical rows feed the per-state counters."""
    text = " ".join([r["id"], r["lens"], r["claim"], r["support"], r["extra"]]).lower()
    return (' data-id="{}" data-lens="{}" data-state="{}" data-crit="{}" data-ronda="{}"'
            ' data-verif="{}" data-resolved="{}" data-expired="{}"{} data-text="{}"').format(
        esc(r["id"]), esc(r["lens"]), esc(r["state"]), esc(r["criticidade"]),
        esc(r["ronda"]), esc(r["verificado_em"]),
        "1" if r["resolved"] else "0", "1" if r["expired"] else "0",
        ' data-su="1"' if su else "",
        esc(re.sub(r"\s+", " ", text)[:1200]))


def _id_chip(r: dict, state_tone: bool = True) -> str:
    cls = "prov idchip" if state_tone else "prov"
    cls += " prov-exp" if r["expired"] else ""
    cls += " prov-res" if r["resolved"] else ""
    return '<span class="{}" data-id="{}" title="{}" tabindex="0">{}</span>'.format(
        cls, esc(r["id"]), esc(prov_title(r)), esc(r["id"]))


def _id_cell(r: dict) -> str:
    marks = ""
    if r["expired"]:
        marks += '<span class="badge exp" title="expirada ha {} dias">reconf.</span>'.format(
            r["days_overdue"])
    if r["verificado_em_source"].startswith("inferido"):
        marks += '<span class="badge inf" title="{}">inf</span>'.format(esc(r["verificado_em_source"]))
    if r["malformed"]:
        marks += '<span class="badge mal" title="linha reparada pelo parser (linha {})">!</span>'.format(r["line"])
    return '<td class="c-id">{}{}</td>'.format(_id_chip(r), marks)


def _crit_cell(r: dict) -> str:
    k = r["criticidade"]
    if not k:
        return '<td class="c-crit"><span class="critpill">&mdash;</span></td>'
    return ('<td class="c-crit"><span class="critpill k-{}" title="{}">{}</span></td>'.format(
        esc(k), esc(r["criticidade_raw"] or k), esc(CRIT_LABEL.get(k, k))))


def _reg_head() -> str:
    cells = []
    for key, label, cls in REG_COLS:
        cells.append('<th class="{}" scope="col"><button class="sortb" data-sort="{}">{}'
                     '<span class="ar" aria-hidden="true"></span></button></th>'.format(
                         cls, key, esc(label)))
    return "<thead><tr>{}</tr></thead>".format("".join(cells))


def _su_table(state: str, rows: list[dict], ids: dict, today: date) -> str:
    mine = [r for r in rows if r["state"] == state]
    if not mine:
        return '<div class="tw"><div class="empty">Sem linhas nesta secção.</div></div>'
    body = []
    for r in mine:
        cells = [_id_cell(r), _crit_cell(r),
                 '<td class="c-lens">{}</td>'.format(esc(r["lens"] or "-")),
                 '<td class="c-claim"><div>{}</div></td>'.format(inline_md(r["claim"], None)),
                 '<td class="c-verif" title="validade {} &middot; {}">{}</td>'.format(
                     esc(r["validade"]), esc(_age(r["verificado_em"], today) or "-"),
                     esc(r["verificado_em"] or "-")),
                 '<td class="c-ronda">{}</td>'.format(esc(r["ronda"] or "-"))]
        body.append('<tr tabindex="0" role="button" class="s-{}{}"{}>{}</tr>'.format(
            esc(state), " res" if r["resolved"] else "", _row_attrs(r, su=True), "".join(cells)))
    return ('<div class="tw"><table class="reg">{}<tbody>{}</tbody></table></div>'.format(
        _reg_head(), "".join(body)))


def _agenda_bucket(title: str, why: str, items: list[dict], ids: dict) -> str:
    head = ('<div class="blk"><h2 class="sec">{} <span class="n">{}</span>'
            '<span class="x">{}</span></h2>'.format(esc(title), len(items), esc(why)))
    if not items:
        return head + '<div class="tw"><div class="empty">Nada aqui.</div></div></div>'
    qs = []
    for it in items:
        r = ids.get(it["id"])
        badge = ('<span class="critpill k-Critical" title="Critical">grave</span>'
                 if it["criticidade"] == "Critical" else "")
        meta = '<div class="qm"><b>quem</b><span>{}</span></div>'.format(
            inline_md(it["quem"] or "-", None))
        if it["swing_text"]:
            meta += '<div class="qm"><b>muda</b><span>{}</span></div>'.format(
                inline_md(it["swing_text"], None))
        qs.append(
            '<div class="q s-{st}" role="button" tabindex="0" data-id="{id}" data-text="{txt}">'
            '<div class="qh">{chip}<span class="sw {sw}">{swl}</span>{badge}'
            '<span class="tag">{custo}</span></div>'
            '<div class="qt">{perg}</div>{meta}</div>'.format(
                st=esc(r["state"] if r else "Unknown"), id=esc(it["id"]),
                txt=esc(re.sub(r"\s+", " ", (it["id"] + " " + it["pergunta"] + " " + it["quem"]).lower())[:600]),
                chip=_id_chip(r) if r else esc(it["id"]), sw=esc(it["swing_class"]),
                swl=esc(swing_label(it["swing_class"])), badge=badge,
                custo=esc(CUSTO_LABEL.get(it["custo"], it["custo"])),
                perg=inline_md(it["pergunta"], None), meta=meta))
    return head + '<div class="qgrid">{}</div></div>'.format("".join(qs))


# ------------------------------------------------------------------ panorama


def _stepper(phase: str) -> str:
    cur = norm_key(phase)
    return '<div class="stepper">{}</div>'.format("".join(
        '<span class="step{}" title="{}">{}</span>'.format(
            " on" if key == cur else "", esc(key), esc(label)) for key, label in PHASES))


def _next_phase_label(phase: str) -> str:
    cur = norm_key(phase)
    keys = [k for k, _ in PHASES]
    if cur in keys and keys.index(cur) + 1 < len(keys):
        return PHASE_LABEL[keys[keys.index(cur) + 1]]
    return ""


def _pano_lead(model: dict) -> str:
    e, su = model["engagement"], model["su"]
    live = sum(su["sections"][s]["open"] for s in SECTIONS)
    crit = len(model["critical"])
    rondas = model["facets"]["ronda"]
    bits = []
    opening = {
        "discovery": "Estamos a ouvir e a perguntar.",
        "framing": "Estamos a fixar a frase do problema.",
        "options": "Estamos a comparar alternativas.",
        "decision": "Estamos na escolha e no que vem depois.",
    }.get(norm_key(e["phase"]))
    if opening:
        bits.append(opening)
    if rondas:
        n = len(rondas)
        bits.append("{} até agora ({}{}).".format(
            "1 passagem" if n == 1 else "{} passagens".format(n), esc(rondas[0]),
            " a " + esc(rondas[-1]) if n > 1 else ""))
    tail = "O registo tem {} afirmações vivas".format(live)
    if crit:
        tail += " e {} tema{} grave{} por fechar".format(
            crit, "" if crit == 1 else "s", "" if crit == 1 else "s")
        nxt = _next_phase_label(e["phase"])
        tail += " antes de passar a «{}».".format(esc(nxt)) if nxt else " antes das entregas."
    else:
        tail += " e nenhum tema grave em aberto."
    bits.append(tail)
    return " ".join(bits)


def _hero(model: dict) -> str:
    su, h = model["su"], model["health"]
    crit = len(model["critical"])
    total = sum(su["sections"][s]["open"] for s in SECTIONS) or 1
    segs = "".join(
        '<span class="s-{}" style="width:{:.3f}%;background:var(--st-{}-dot)" title="{}: {}"></span>'
        .format(s, su["sections"][s]["open"] * 100 / total, s,
                STATE_LABEL[s], su["sections"][s]["open"])
        for s in SECTIONS if su["sections"][s]["open"])
    stats = "".join(
        '<div><span class="v{}">{}</span><span class="l"><span class="dot s-{}"></span>{}</span></div>'
        .format(" zero" if not su["sections"][s]["open"] else "", su["sections"][s]["open"],
                s, esc(STATE_LABEL[s].lower()))
        for s in SECTIONS)

    notes = []
    if su["header_health_raw"]:
        notes.append("no registo: {}".format(esc(su["header_health_raw"])))
    if su["schema_flavour"] == "legacy":
        notes.append("registo anterior à v2.2: datas inferidas da passagem")
    fresh = "{} em prazo &middot; {} por reconfirmar, de {}".format(h["live"], h["expired"], h["total"])
    if notes:
        fresh += "<br>" + " &middot; ".join(notes)

    nxt = _next_phase_label(model["engagement"]["phase"])
    crit_note = ("Bloqueiam a passagem a «{}».".format(esc(nxt)) if nxt
                 else "Bloqueiam o fecho das entregas.") if crit else \
                "Nada grave em aberto neste momento."

    return (
        '<div class="hero">'
        '<div class="col">'
        '<div class="eyebrow">O registo do que sabemos &middot; linhas vivas</div>'
        '<div class="bar">{segs}</div>'
        '<div class="stats">{stats}</div>'
        "</div>"
        '<div class="metrics">'
        '<div class="metric"><div class="v hi">{crit}</div><div>'
        '<div class="eyebrow">Graves em aberto</div>'
        '<div class="u">{crit_note}</div></div></div>'
        '<div class="metric" title="Percentagem de linhas dentro do prazo de revalidação '
        '(saúde epistémica) — não é uma medida de saúde do projecto">'
        '<div class="v">{pct}%</div><div>'
        '<div class="eyebrow">Frescura do registo</div>'
        '<div class="u">{fresh}</div></div></div>'
        "</div></div>"
    ).format(segs=segs, stats=stats, crit=crit, crit_note=crit_note, pct=h["pct"], fresh=fresh)


def _todo_items(model: dict, ids: dict) -> list[tuple[str, str]]:
    items: list[tuple[str, str]] = []
    ag = model["agenda"]["reuniao"] + model["agenda"]["outro_canal"]
    if ag:
        it = ag[0]
        r = ids.get(it["id"])
        items.append((
            "{} &middot; <span class=\"sw {}\">{}</span> {}".format(
                _id_chip(r, False) if r else esc(it["id"]), esc(it["swing_class"]),
                esc(swing_label(it["swing_class"])),
                inline_md(it["pergunta"], None)),
            "obter a resposta: {} &middot; quem: {}".format(
                esc(CUSTO_LABEL.get(it["custo"], it["custo"])), esc(it["quem"] or "-"))))
    elif model["critical"]:
        c = model["critical"][0]
        r = ids.get(c["id"])
        items.append(((_id_chip(r, False) if r else esc(c["id"])) + " &middot; "
                      + inline_md(c["claim"], None),
                      "grave, em aberto ({})".format(esc(STATE_LABEL.get(c["state"], c["state"])))))
    if model["revalidate"]:
        rv = model["revalidate"][0]
        r = ids.get(rv["id"])
        items.append((
            "{} passou o prazo há {} dias &mdash; ainda é verdade?".format(
                _id_chip(r, False) if r else esc(rv["id"]), rv["days_overdue"]),
            '<span class="cmd">{}</span> &middot; mais {} a reconfirmar'.format(
                esc(rv["cmd"]), len(model["revalidate"]) - 1)))
    watching = [t for t in model["tripwires"] if t["status"] == "watch"]
    if watching:
        t = watching[0]
        items.append(("{} a vigiar &mdash; {}".format(esc(t["tw"]), inline_md(t["text"], None)),
                      '<span class="cmd">/revisit {}</span>'.format(esc(t["tw"]))))
    elif model["tripwires"]:
        items.append(("{} condições de revisão registadas, nenhuma a vigiar".format(len(model["tripwires"])),
                      "o veredicto de disparo pertence ao <span class='cmd'>/status</span>"))
    na = model["next_action"]
    items.append((inline_md(na["text"], None), '<span class="cmd">{}</span>'.format(esc(na["command"]))))
    return items[:4]


def _first_para(html_body: str, limit: int = 420) -> tuple[str, bool]:
    """First <p> of a rendered episode, trimmed at a word boundary. The Panorama shows a
    taste in the sponsor's voice; the full text lives in Narrativa."""
    m = re.search(r"<p>(.*?)</p>", html_body, re.S)
    para = m.group(1) if m else html_body
    more = len(re.findall(r"<p>", html_body)) > 1
    plain = re.sub(r"<[^>]+>", "", para)
    if len(plain) > limit:
        cut = plain[:limit].rsplit(" ", 1)[0]
        return esc(cut) + "&hellip;", True
    return para, more


def _glossary(model: dict) -> list[tuple[str, str]]:
    su = model["su"]
    total = len(su["rows"])
    resolved = sum(su["sections"][s]["resolved"] for s in SECTIONS)
    live = sum(su["sections"][s]["open"] for s in SECTIONS)
    rondas = model["facets"]["ronda"]
    lentes = model["facets"]["lens"]
    n_ag = len(model["agenda"]["reuniao"]) + len(model["agenda"]["outro_canal"])
    return [
        ("Registo (shared understanding)",
         "A lista de tudo o que se sabe sobre o processo. Cada linha é uma afirmação com "
         "identificador, evidência e data de verificação. A fonte de verdade é "
         "<code>shared-understanding.md</code>."),
        ("Confirmado",
         "Afirmação verificada com evidência citada (ficheiro, passagem de reunião ou "
         "declaração do dono do processo)."),
        ("Assumido", "Hipótese aceite para avançar, ainda sem evidência que a feche."),
        ("Por saber",
         "Pergunta em aberto. É o que a Agenda organiza por custo de obter a resposta."),
        ("Em conflito",
         "Duas evidências dizem coisas diferentes; precisa de arbitragem antes de ser usada."),
        ("Risco",
         "Afirmação que, a confirmar-se, muda o custo ou a viabilidade do que se está a desenhar."),
        ("Passagem ({})".format(esc(" … ".join([rondas[0], rondas[-1]])) if len(rondas) > 1
                                else esc(rondas[0]) if rondas else "R-01"),
         "Cada passagem das perspectivas pelo material. A primeira (R-00) é o enquadramento "
         "declarado pelo dono do processo."),
        ("Perspectiva",
         "O ângulo com que a passagem olhou: {}.".format(esc(", ".join(lentes)) or "-")),
        ("Grave",
         "Item por saber ou em conflito que bloqueia a passagem à etapa seguinte."),
        ("Contagens",
         "O registo tem {} linhas no total: as {} vivas contam para os números do topo, as {} "
         "resolvidas ficam escondidas até activares «mostrar resolvidas». As contagens da "
         "Agenda sobrepõem-se — o mesmo item pode ser grave e pedir reunião; o separador "
         "conta {} perguntas em aberto.".format(total, live, resolved, n_ag)),
        ("<code>/answer</code>, <code>/frame</code>",
         "Comandos do processo: <code>/answer</code> registra a resposta a uma pergunta em "
         "aberto, <code>/frame</code> fecha o enquadramento e passa à etapa seguinte."),
        ("Frescura do registo",
         "Percentagem de afirmações dentro do prazo de revalidação. Não é uma medida de "
         "saúde do projecto: {} afirmações vivas e {} temas graves em aberto podem coexistir "
         "com 100%.".format(live, len(model["critical"]))),
    ]


def _panorama(model: dict, ids: dict) -> str:
    e = model["engagement"]
    o = []

    o.append('<div class="pantop"><div>'
             '<div class="eyebrow">Panorama</div>'
             '<h1 class="pt big">Onde estamos</h1>'
             '<p class="lead">{}</p></div>{}</div>'.format(_pano_lead(model), _stepper(e["phase"])))
    o.append(_hero(model))

    if model.get("frame_sentence"):
        o.append('<div class="card pad"><h3 title="frame.md">A frase do problema (passagem {})</h3>'
                 '<div class="sentence">{}</div>'
                 '<button class="btn quiet" data-tab="outputs" style="margin-top:14px">'
                 "âncoras, correcções e conflitos</button></div>".format(
                     esc(e["round"] if e["round"].startswith("F") else "F-01"),
                     inline_md(model["frame_sentence"], None)))

    todo = ['<div class="card"><div class="hd">'
            '<span class="eyebrow">A fazer a seguir</span>'
            '<button class="btn mini" data-tab="agenda">Ver agenda</button></div>'
            '<ol class="todo">']
    for t, m in _todo_items(model, ids):
        todo.append('<li><div><div class="t">{}</div><div class="m">{}</div></div></li>'.format(t, m))
    todo.append("</ol></div>")

    chapter = ""
    story = [ev for ev in model["timeline"] if ev["kind"] == "story"]
    if story:
        last = story[-1]
        para, more = _first_para(last["html"])
        tail = ('<button class="btn quiet" data-tab="narrativa" style="margin-top:16px">'
                "Ler o resto na Narrativa</button>") if more else ""
        chapter = ('<div class="card pad"><div class="eyebrow" style="margin-bottom:12px">'
                   'Último capítulo &middot; {}</div>'
                   '<div class="quote">{}<span class="src">{}</span></div>{}</div>'.format(
                       esc(last["when"] or last["round"] or "-"), para, esc(last["title"]), tail))
    elif e["literal_request"]:
        chapter = ('<div class="card pad"><div class="eyebrow" style="margin-bottom:12px">'
                   "O pedido original</div>"
                   '<div class="quote">{}<span class="src">{}{}</span></div></div>'.format(
                       _first_para(inline_md(e["literal_request"], None))[0],
                       esc(e["sponsor"] or "-"),
                       ", " + esc(e["requester_role"]) if e["requester_role"] else ""))
    o.append('<div class="cards2">{}{}</div>'.format("".join(todo), chapter))

    o.append('<div class="card"><button class="rowbtn" id="glossbtn" aria-expanded="false"'
             ' aria-controls="gloss"><span class="caret" aria-hidden="true">&#9656;</span>'
             '<span class="ttl">Como ler este relatório</span>'
             '<span class="m">termos, estados e contagens</span></button>'
             '<div class="gloss" id="gloss" hidden>{}</div></div>'.format(
                 "".join('<div><span class="k">{}</span><span class="v">{}</span></div>'.format(k, v)
                         for k, v in _glossary(model))))
    return "".join(o)


# --------------------------------------------------------------------- page


def render_html(model: dict, reload_secs: int) -> str:
    e = model["engagement"]
    su = model["su"]
    ids = {r["id"]: r for r in su["rows"]}
    h = model["health"]
    today = _as_date(model["today"]) or date.today()

    n_ag = len(model["agenda"]["reuniao"]) + len(model["agenda"]["outro_canal"])
    n_open = sum(su["sections"][s]["open"] for s in SECTIONS)
    n_res = sum(su["sections"][s]["resolved"] for s in SECTIONS)
    n_crit = len(model["critical"])
    counts = {
        "panorama": "", "outputs": len(model["phase_docs"]), "agenda": n_ag,
        "estado": n_open, "narrativa": len(model["timeline"]),
        "artefactos": len([x for x in model["artefacts"] if x["exists"]]),
    }

    payload = {
        "slug": e["slug"], "reload": reload_secs, "build": model["build"],
        "tabs": [k for k, _, _ in TAB_SPEC],
        "counts": {"live": n_open, "resolved": n_res, "total": len(su["rows"])},
        "stlabel": STATE_LABEL, "support": SUPPORT_LABEL,
        "custo": CUSTO_LABEL, "swing": SWING_LABEL,
        "ids": _ids_payload(su["rows"]),
    }
    payload_json = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

    o: list[str] = []
    a = o.append
    a('<!doctype html><html lang="pt-PT"><head><meta charset="utf-8">')
    a('<meta name="viewport" content="width=device-width,initial-scale=1">')
    a("<title>aisa &middot; {}</title>".format(esc(e["slug"])))
    a("<style>" + CSS + "</style></head><body>")
    a("<!-- aisa-dashboard v{} build {} {} -->".format(TOOL_VERSION, model["build"], model["generated"]))
    a('<div class="app">')

    # ---------------- header
    a('<header class="top">')
    a('<span class="wordmark">aisa<span>discovery</span></span>')
    a('<span class="idblock"><span class="slug">{}</span><span class="dot4"></span>'
      '<span class="phasepill" title="phase {} · round {}">{}{}</span></span>'.format(
          esc(e["slug"]), esc(e["phase"] or "-"), esc(e["round"] or "-"),
          esc(PHASE_LABEL.get(norm_key(e["phase"]), e["phase"] or "-")),
          " ({})".format(esc(e["round_in_progress"] or e["round"])) if (e["round"] or e["round_in_progress"]) else ""))
    a('<span class="spacer"></span>')
    a('<span class="hpill" title="Percentagem de linhas dentro do prazo de revalidação">'
      '<i></i>registo fresco {}%</span>'.format(h["pct"]))
    a('<button class="hpill hot" data-tab="agenda">{} graves em aberto</button>'.format(n_crit))
    a('<span class="stamp">{} &middot; <b id="cd">{}s</b></span>'.format(
        esc(model["generated"].replace("T", " ")[:16]), reload_secs))
    a('<button class="btn quiet noprint" id="pause">pausar</button>')
    a('<span class="seg noprint" title="Densidade da página">'
      '<button class="btn" data-dens="cosy">confortável</button>'
      '<button class="btn" data-dens="compact">compacto</button></span>')
    a('<button class="btn quiet noprint" id="theme">tema auto</button>')
    a('<button class="btn noprint" id="printtab">Imprimir separador</button>')
    a('<button class="btn quiet noprint" id="printall">tudo</button>')
    a("</header>")

    # ---------------- nav + main
    a('<div class="mid">')
    a('<nav class="side noprint" role="tablist" aria-orientation="vertical"'
      ' aria-label="Separadores do relatório">')
    a('<div class="navhead">O projecto</div>')
    for i, (key, label, tip) in enumerate(TAB_SPEC):
        cnt = counts[key]
        # the tooltip carries the kernel vocabulary; the accessible name must stay the
        # business label, so it is spelled out instead of left to the tooltip
        a('<button class="nav" role="tab" id="tab-{k}" data-tab="{k}" aria-controls="panel-{k}"'
          ' aria-selected="{sel}" aria-label="{aria}"{tip}>{lbl}{cnt}</button>'.format(
              k=key, sel="true" if i == 0 else "false",
              aria=esc("{}{}".format(label, ", {} linhas".format(cnt) if cnt != "" else "")),
              tip=' title="{}"'.format(esc(tip)) if tip else "", lbl=esc(label),
              cnt=' <span class="cnt">{}</span>'.format(cnt) if cnt != "" else ""))
    a('<div class="navfoot">')
    a('<div class="navhead" style="padding:0">Registo por estado</div>')
    for s in SECTIONS:
        a('<div class="lg s-{}"><span class="dot"></span><b>{}</b><span>{}</span></div>'.format(
            s, su["sections"][s]["open"], esc(STATE_LABEL[s].lower())))
    a('<div class="build">build {}</div>'.format(esc(model["build"])))
    a("</div></nav>")
    a('<main class="pane" id="pane">')

    # ---------------- panel: panorama
    a('<section class="panel" role="tabpanel" id="panel-panorama" aria-labelledby="tab-panorama"'
      ' tabindex="0" data-tab="panorama" data-title="Panorama">')
    a(_panorama(model, ids))
    a("</section>")

    # ---------------- panel: etapas (what each phase actually produced)
    a('<section class="panel" role="tabpanel" id="panel-outputs" aria-labelledby="tab-outputs"'
      ' tabindex="0" data-tab="outputs" data-title="Etapas" hidden>')
    a('<div><div class="eyebrow">O que cada etapa produziu</div><h1 class="pt">Etapas</h1></div>')
    docs = model["phase_docs"]
    if not docs:
        a('<p class="sub">Nenhuma etapa produziu ainda o seu documento. '
          "Aparecem aqui a partir de <span class=\"cmd\">/capture</span>, "
          '<span class="cmd">/frame</span>, <span class="cmd">/options</span>, '
          '<span class="cmd">/premortem</span>, <span class="cmd">/decide</span> '
          "e <span class=\"cmd\">/blueprint</span>.</p>")
    else:
        a('<p class="sub">Por extenso. Os documentos da etapa actual abrem expandidos; os '
          "anteriores ficam recolhidos. Os identificadores do registo são clicáveis.</p>")
        cur = norm_key(e["phase"])
        last_phase = None
        for d in docs:
            if d["phase"] != last_phase:
                a('<div class="eyebrow" style="margin-top:14px">{}</div>'.format(
                    esc(PHASE_LABEL.get(d["phase"], d["phase"]))))
                last_phase = d["phase"]
            trunc = ""
            if d.get("truncated"):
                trunc = ('<div class="trunc">O que está acima é um render parcial do documento '
                         "({} caracteres no total). O texto integral está em "
                         '<a href="{}">{}</a>.</div>'.format(d["chars"], d["href"], esc(d["rel"])))
            a('<details class="doc"{open}><summary><div class="t">'
              '<span class="caret" aria-hidden="true">&#9656;</span><h3>{title}</h3></div>'
              '<div class="m">{round}{chars} &middot; {nids} identificadores do registo '
              '&middot; <a href="{href}">{rel}</a></div></summary>'
              '<div class="docbody rich">{body}{trunc}</div></details>'.format(
                  open=" open" if d["phase"] == cur else "", title=esc(d["title"]),
                  round=(esc(d["round"]) + " &middot; ") if d["round"] else "",
                  chars="{} caracteres{}".format(
                      d["chars"], " &middot; render truncado" if d.get("truncated") else ""),
                  nids=len(d["ids"]), href=d["href"], rel=esc(d["rel"]),
                  body=d["html"], trunc=trunc))
    a("</section>")

    # ---------------- panel: agenda
    a('<section class="panel" role="tabpanel" id="panel-agenda" aria-labelledby="tab-agenda"'
      ' tabindex="0" data-tab="agenda" data-title="Agenda" hidden>')
    a('<div><div class="eyebrow">O que vale o tempo de uma reunião</div>'
      '<h1 class="pt">Agenda</h1></div>')
    na = model["next_action"]
    a('<div class="note"><span class="eyebrow">Próxima acção</span>'
      '<div class="bdy">{} <span class="cmd">{}</span></div></div>'.format(
          inline_md(na["text"], None), esc(na["command"])))

    ag = model["agenda"]
    decisivos = sum(1 for b in ("reuniao", "outro_canal")
                    for it in ag[b] if it["swing_class"] == "decisivo")
    crits = sum(1 for b in ("reuniao", "outro_canal")
                for it in ag[b] if it["criticidade"] == "Critical")
    a('<div class="tally">'
      '<div class="hot"><span class="v">{}</span><span class="l">mudam o caminho</span></div>'
      '<div><span class="v">{}</span><span class="l">graves</span></div>'
      '<div><span class="v">{}</span><span class="l">pedem reunião</span></div>'
      '<div><span class="v">{}</span><span class="l">por outro canal</span></div>'
      '<div><span class="v">{}</span><span class="l">não mudam nada</span></div></div>'.format(
          decisivos, crits, len(ag["reuniao"]), len(ag["outro_canal"]), len(ag["nao_gastar"])))
    a('<p class="sub">As contagens acima sobrepõem-se: o mesmo item pode ser grave e pedir '
      "reunião. O separador conta {} perguntas em aberto.</p>".format(n_ag))

    if model["critical"]:
        a('<div class="blk"><h2 class="sec" title="Critical">Graves em aberto '
          '<span class="n">{}</span></h2>'.format(n_crit))
        a('<div class="tw"><table><thead><tr><th scope="col">id</th><th scope="col">estado</th>'
          '<th scope="col">perspectiva</th><th scope="col">item</th></tr></thead><tbody>')
        for c in model["critical"]:
            r = ids.get(c["id"])
            a('<tr class="agrow s-{st}"{attrs} tabindex="0" role="button">'
              '<td class="c-id">{chip}</td>'
              '<td class="c-meta"><span class="statepill">{state}</span></td>'
              '<td class="c-lens">{lens}</td>'
              '<td class="c-claim"><div class="clamp">{claim}</div></td></tr>'.format(
                  st=esc(c["state"]), attrs=_row_attrs(r) if r else "",
                  chip=_id_chip(r) if r else esc(c["id"]),
                  state=esc(STATE_LABEL.get(c["state"], c["state"])),
                  lens=esc(c["lens"]), claim=inline_md(c["claim"], None)))
        a("</tbody></table></div></div>")

    a('<p class="sub">Cada pergunta em aberto diz <b>o que custa obter a resposta</b> '
      "e <b>o que muda quando ela chega</b>. Ordenadas pelo que muda: primeiro as que "
      "mudam o caminho.</p>")
    a(_agenda_bucket("Reunião", "Justificam a hora síncrona do sponsor.",
                     model["agenda"]["reuniao"], ids))
    a(_agenda_bucket("Por outro canal",
                     "Email, documento ou trabalho técnico. Não ocupam a reunião.",
                     model["agenda"]["outro_canal"], ids))
    a(_agenda_bucket("Não gastes tempo com isto",
                     "Não mudam nada material: legítimas, mas não valem reunião.",
                     model["agenda"]["nao_gastar"], ids))

    a('<div class="blk"><h2 class="sec" title="tripwires">Condições de revisão '
      '<span class="n">{}</span></h2>'.format(len(model["tripwires"])))
    if not model["tripwires"]:
        a('<div class="tw"><div class="empty">Sem escolha final registada, ou sem condições '
          "de revisão na decisão.</div></div>")
    else:
        a('<p class="sub">Estado <b>a vigiar</b> = um identificador citado está em aberto e '
          "grave, ou passou o prazo. Este gerador nunca declara uma condição disparada: essa "
          'leitura pertence ao <span class="cmd">/status</span>.</p>')
        for tw in model["tripwires"]:
            ev = ""
            if tw["evidence"]:
                ev = '<br><span class="stamp">a vigiar: {}</span>'.format(", ".join(
                    "{} ({}{})".format(x["id"], STATE_LABEL.get(x["state"], x["state"]),
                                       ", por reconfirmar" if x["expired"] else "")
                    for x in tw["evidence"]))
            a('<div class="note {}"><span class="eyebrow">{}{}</span><div class="bdy">{}{}<br>'
              '<span class="cmd">/revisit {}</span></div></div>'.format(
                  "watch" if tw["status"] == "watch" else "quiet", esc(tw["tw"]),
                  " &middot; a vigiar" if tw["status"] == "watch" else "",
                  inline_md(tw["text"], None), ev, esc(tw["tw"])))
    a("</div>")
    a("</section>")

    # ---------------- panel: registo (the SU itself)
    a('<section class="panel reg" role="tabpanel" id="panel-estado" aria-labelledby="tab-estado"'
      ' tabindex="0" data-tab="estado" data-title="Registo" hidden>')
    a('<div class="toolbar noprint"><div class="trow r1">')
    # the kernel vocabulary is not deleted, it moves to the tooltip (P-13 mechanic 5)
    a('<h1 class="pt" style="font-size:20px" title="Shared Understanding: Confirmed \u00b7 Assumed \u00b7 Unknown \u00b7 Conflicted \u00b7 Risky">Registo</h1>')
    a('<span class="counts" id="regcount" aria-live="polite">{} visíveis &middot; {} vivos '
      "&middot; {} resolvidos &middot; {} no total</span>".format(
          n_open, n_open, n_res, len(su["rows"])))
    a('<span class="hint">Clicar numa linha abre o detalhe</span>')
    a('<span class="spacer"></span>')
    a('<input type="search" id="f-q" placeholder="Procurar identificador ou texto…    /"'
      ' aria-label="Procurar no registo">')
    a('<button class="btn" id="csv">Exportar CSV</button>')
    a("</div>")
    a('<div class="trow">')
    a(_chips("states", model["facets"]["state"], "estado"))
    a('<span class="vr"></span>')
    a(_chips("crits", model["facets"]["criticidade"] + [CRIT_NONE], "gravidade"))
    a('<span class="vr"></span>')
    a('<button class="chip" id="f-exp" aria-pressed="false">só a reconfirmar</button>'
      '<button class="chip" id="f-res" aria-pressed="false">mostrar resolvidas</button>'
      '<button class="chip" id="f-clear">limpar filtros</button>')
    a("</div>")
    a('<div class="trow">')
    a(_chips("lenses", model["facets"]["lens"], "perspectiva", tint="accent"))
    a('<span class="vr"></span>')
    a(_chips("rondas", model["facets"]["ronda"], "passagem", tint="accent"))
    a("</div></div>")

    a('<div class="regbody">')
    a('<p class="sub">O registo completo. Clicar numa linha abre o detalhe: texto integral, '
      "evidência, proveniência e transições. O preço e o impacto de cada pergunta em aberto "
      "estão na Agenda. A fonte de verdade continua a ser <code>shared-understanding.md</code>.</p>")

    if model["revalidate"]:
        a('<section class="regblock aux blk" title="revalidate (expired half-life)">'
          '<h2 class="sec">A reconfirmar <span class="n">{}</span>'
          '<span class="x">passou o prazo — não significa falso</span></h2>'.format(
              len(model["revalidate"])))
        a('<div class="tw"><table><thead><tr><th scope="col">id</th>'
          '<th scope="col">afirmação</th><th scope="col">validade</th>'
          '<th scope="col">verificado em</th><th scope="col">vencida há</th>'
          "</tr></thead><tbody>")
        for it in model["revalidate"]:
            r = ids.get(it["id"])
            a('<tr class="s-{st}"{attrs} tabindex="0" role="button"><td class="c-id">{chip}</td>'
              '<td class="c-claim"><div class="clamp">{claim}</div></td>'
              '<td class="c-meta">{val}</td><td class="c-verif">{v}</td>'
              '<td class="c-meta">{d}d</td></tr>'.format(
                  st=esc(it["state"]), attrs=_row_attrs(r) if r else "",
                  chip=_id_chip(r) if r else esc(it["id"]),
                  claim=inline_md(it["claim"], None), val=esc(it["validade"]),
                  v=esc(it["verificado_em"]), d=it["days_overdue"]))
        a("</tbody></table></div></section>")

    for s in SECTIONS:
        meta = su["sections"][s]
        a('<section class="regblock blk" data-state="{s}">'
          '<h2 class="sec hasdot s-{s}" title="{s}">{lbl} '
          '<span class="n" data-count-state="{s}">{open}</span>'
          '<span class="x">visíveis{res}</span></h2>{table}</section>'.format(
              s=esc(s), lbl=esc(STATE_LABEL[s]), open=meta["open"],
              res=" +{} resolvidas".format(meta["resolved"]) if meta["resolved"] else "",
              table=_su_table(s, su["rows"], ids, today)))

    a('<div class="emptycard" id="regempty" hidden>'
      '<span class="t">Nenhum registo corresponde aos filtros</span>'
      '<span class="m">Há {} linhas vivas. Tenta remover um filtro ou limpar a pesquisa.</span>'
      '<button class="btn solid" data-clear="1">Limpar filtros</button></div>'.format(n_open))
    a("</div></section>")

    # ---------------- panel: narrativa
    a('<section class="panel" role="tabpanel" id="panel-narrativa" aria-labelledby="tab-narrativa"'
      ' tabindex="0" data-tab="narrativa" data-title="Narrativa" hidden>')
    a('<div><div class="eyebrow">A leitura corrida do que aconteceu</div>'
      '<h1 class="pt">Narrativa</h1></div>')
    if not model["timeline"]:
        a('<p class="sub">Sem <code>story.md</code>, <code>council-log.md</code> ou '
          "<code>decisions.md</code> com conteúdo.</p>")
    else:
        a('<p class="sub">Os episódios são a leitura corrida do que aconteceu. Os registos '
          "técnicos de cada passagem trazem as transições de cada identificador.</p>")
        a('<div class="trow noprint"><button class="chip" data-narr="todos" aria-pressed="true">'
          'Tudo</button><button class="chip" data-narr="story" aria-pressed="false">Episódios'
          '</button><button class="chip" data-narr="council" aria-pressed="false">'
          "Registos técnicos</button></div>")
        kind_label = {"story": "episódio &middot; voz do sponsor",
                      "council": "registo técnico da passagem",
                      "artefacto": "documento de etapa", "decision": "decisão"}
        for ev in model["timeline"]:
            a('<div class="ev {k}" data-kind="{k}"><div class="top"><span class="k">{kl}</span>'
              '<span class="meta">{when}{rnd}</span></div><h2>{title}</h2>'
              '<div class="rich">{body}</div></div>'.format(
                  k=esc(ev["kind"]), kl=kind_label.get(ev["kind"], esc(ev["kind"])),
                  when=esc(ev["when"] or "sem data"),
                  rnd=" &middot; " + esc(ev["round"]) if ev["round"] else "",
                  title=inline_md(ev["title"], None), body=ev["html"]))
    a("</section>")

    # ---------------- panel: ficheiros
    a('<section class="panel" role="tabpanel" id="panel-artefactos"'
      ' aria-labelledby="tab-artefactos" tabindex="0" data-tab="artefactos"'
      ' data-title="Ficheiros" hidden>')
    a('<div><div class="eyebrow">O que existe em disco</div><h1 class="pt">Ficheiros</h1></div>')
    groups: dict[str, list[dict]] = {}
    for art in model["artefacts"]:
        groups.setdefault(art["group"], []).append(art)
    for g in ["em falta", "raiz"] + INDEX_DIRS:
        items = groups.get(g)
        if not items:
            continue
        a('<div class="blk"><h2 class="sec" title="{}">{} <span class="n">{}</span></h2>'.format(
            esc(g), esc(GROUP_LABEL.get(g, g)), len(items)))
        a('<div class="tw"><table><thead><tr><th scope="col">ficheiro</th>'
          '<th scope="col">tamanho</th><th scope="col">alterado</th><th scope="col">nota</th>'
          "</tr></thead><tbody>")
        for it in items:
            name = ('<a href="{}">{}</a>'.format(it["href"], esc(it["name"]))
                    if it["exists"] else '<span class="stamp">{}</span>'.format(esc(it["name"])))
            a('<tr><td class="c-file">{}</td><td class="c-meta">{}</td>'
              '<td class="c-meta">{}</td><td class="c-meta">{}</td></tr>'.format(
                  name, esc(it["size_h"]), esc(it["mtime"]),
                  '<span class="badge mal">{}</span>'.format(esc(it["note"])) if it["note"] else ""))
        a("</tbody></table></div></div>")

    if model["render"]["versions"]:
        a('<div class="blk"><h2 class="sec" title="deliverables (_render/)">'
          "Documentos finais produzidos</h2>")
        a('<div class="tw"><table><thead><tr><th scope="col">documento</th>'
          '<th scope="col">versões</th></tr></thead><tbody>')
        for k in sorted(model["render"]["versions"]):
            a('<tr><td>{}</td><td class="c-meta">{}</td></tr>'.format(
                esc(k), esc(", ".join(model["render"]["versions"][k]))))
        a("</tbody></table></div></div>")
    if model["render"]["gaps"]:
        a('<div class="blk"><h2 class="sec" title="render-gaps.md">O que falta para os '
          'documentos finais <span class="n">{}</span></h2>'.format(len(model["render"]["gaps"])))
        heads = list(model["render"]["gaps"][0].keys())
        a('<div class="tw scroll"><table><thead><tr>{}</tr></thead><tbody>'.format(
            "".join('<th scope="col">{}</th>'.format(esc(x)) for x in heads)))
        for row in model["render"]["gaps"]:
            a("<tr>{}</tr>".format("".join("<td>{}</td>".format(
                inline_md(row.get(x, ""), None)) for x in heads)))
        a("</tbody></table></div></div>")

    a('<div class="blk"><h2 class="sec" title="parser diagnostics">Avisos de leitura do '
      'registo <span class="n">{}</span></h2>'.format(len(model["diagnostics"])))
    if not model["diagnostics"]:
        a('<div class="tw"><div class="empty">Nenhum.</div></div>')
    else:
        a('<div class="tw"><table><thead><tr><th scope="col">nível</th><th scope="col">onde</th>'
          '<th scope="col">linha</th><th scope="col">mensagem</th></tr></thead><tbody>')
        for d in model["diagnostics"]:
            a('<tr><td class="c-meta">{}</td><td class="c-meta">{}</td><td class="c-meta">{}</td>'
              "<td>{}</td></tr>".format(
                  esc(d["level"]), esc(d["where"]), d["line"] or "-", esc(d["message"])))
        a("</tbody></table></div>")
    a("</div>")
    a("</section>")

    a("</main></div></div>")
    a('<div id="pop" role="tooltip"></div>')
    a('<div id="dwbg" class="noprint" hidden></div>')
    a('<div id="blk" role="status">O browser recusou o auto-reload neste contexto '
      '(<code>file://</code> em sandbox, ou preview embebido). O ficheiro em disco '
      '<b>está actualizado</b> &mdash; carrega <b>F5</b> para ver o build novo.</div>')
    a('<aside id="dw" class="noprint" role="dialog" aria-modal="true" '
      'aria-label="Detalhe da linha do registo" tabindex="-1"></aside>')
    a('<script type="application/json" id="aisa-data">' + payload_json + "</script>")
    a("<script>" + JS + "</script>")
    a("</body></html>")
    return "".join(o)


def error_page(eng: Path, exc: BaseException, reload_secs: int) -> str:
    tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    return (
        '<!doctype html><html lang="pt-PT"><head><meta charset="utf-8">'
        "<title>aisa &middot; build falhou</title><style>" + CSS + "</style></head><body>"
        '<div class="wrap"><h1>dashboard build falhou</h1>'
        '<div class="note bad">Engagement: <code>' + esc(str(eng)) + "</code><br>"
        "Gerado: " + esc(now_iso()) + " &middot; tool v" + TOOL_VERSION + "</div>"
        "<pre>" + esc(tb) + "</pre>"
        '<p class="foot">A pagina recarrega sozinha; corrige e volta a correr '
        "<code>/dashboard</code>.</p></div>"
        "<script>setTimeout(function(){location.reload();}," + str(max(5, reload_secs) * 1000)
        + ");</script></body></html>"
    )


# -------------------------------------------------------------------- CLI


def _needs_rebuild(eng: Path, out: Path, debounce: float) -> bool:
    if not out.exists():
        return True
    try:
        out_m = out.stat().st_mtime
    except OSError:
        return True
    newest = _activity_mtime(eng)
    for extra in ("story.md", "context.json", "options.md", "frame.md", "premortem.md", "answers.md"):
        f = eng / extra
        if f.exists():
            try:
                newest = max(newest, f.stat().st_mtime)
            except OSError:
                pass
    for d in INDEX_DIRS:
        base = eng / d
        if base.is_dir():
            for f in base.rglob("*"):
                if f.is_file():
                    try:
                        newest = max(newest, f.stat().st_mtime)
                    except OSError:
                        pass
    return newest > out_m


DEFAULT_PORT = 8787


class _Handler(http.server.SimpleHTTPRequestHandler):
    """Serves the engagement folder. Two extras over the stock handler:

    * `/` maps to dashboard.html;
    * `/__build` returns the current build hash, so the page can ask "did anything
      change?" instead of reloading blindly on a timer. That endpoint is same-origin and
      only exists while serving -- the generated file stays self-contained and keeps
      working over file:// with the timed fallback.
    """

    # Identity travels with the build hash. A port is not an identity: the review
    # killed server A, let B take its port and reattached A's lock to B's server
    # (F02, 2026-09-08). `slug` + `engagement` + `pid` + `started` are what the lock
    # holds, so the reattach can compare all four before showing anything.
    build_holder: dict = {"build": "", "slug": "", "engagement": "",
                          "pid": os.getpid(), "started": ""}

    def log_message(self, fmt, *args):  # quiet: the watcher already reports rebuilds
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def do_GET(self):
        if self.path.split("?")[0] in ("/__build", "__build"):
            body = json.dumps(self.build_holder, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path in ("/", ""):
            self.path = "/dashboard.html"
        super().do_GET()


def _lock_path(eng: Path) -> Path:
    """Outside the engagement folder on purpose: that folder is client material and a
    runtime lock file has no business being versioned with it."""
    key = hashlib.sha1(str(eng.resolve()).encode("utf-8")).hexdigest()[:12]
    return Path(tempfile.gettempdir()) / "aisa-dashboard-{}.json".format(key)


def probe(port: int, timeout: float = 0.7) -> dict | None:
    """Identity + build hash of a server listening on this port, or None.

    A server older than 1.5.2 answers the bare build hash; it is returned with an
    empty identity, which no lock can match, so reattaching to it is refused rather
    than guessed."""
    try:
        with urllib.request.urlopen(
                "http://127.0.0.1:{}/__build".format(port), timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace").strip()
    except Exception:
        return None
    try:
        doc = json.loads(raw)
    except (ValueError, TypeError):
        return {"build": raw, "slug": "", "engagement": "", "pid": None, "started": ""}
    return doc if isinstance(doc, dict) else None


def _same_server(lock: dict, ident: dict, eng: Path) -> bool:
    """Is the process answering on that port the one this lock was written for?

    Path + pid + started must all agree: the resolved engagement path (the same
    slug lives in two checkouts, and a folder name is not an identity), the pid,
    and the start timestamp (a pid is reused after a crash). The slug is NOT part
    of this test -- it is what the page compares, and it comes from
    `_state.json.engagement`, which a copied engagement keeps. An empty identity
    -- an older server, or something else on that port -- never matches."""
    try:
        wanted_eng = str(eng.resolve())
    except OSError:
        wanted_eng = str(eng)
    return bool(
        ident.get("engagement")
        and ident.get("engagement") == lock.get("engagement") == wanted_eng
        and ident.get("pid") is not None
        and ident.get("pid") == lock.get("pid")
        and ident.get("started")
        and ident.get("started") == lock.get("started")
    )


def running_server(eng: Path) -> tuple[int, dict] | None:
    """A live server for THIS engagement, if one is already up. Two watchers on one
    engagement race on the output file and an older build can win, so the default is to
    reattach and hand back the URL rather than start a second one."""
    lock = _lock_path(eng)
    info = _read_json(lock)
    port = info.get("port")
    if isinstance(port, int):
        ident = probe(port)
        if ident is not None and _same_server(info, ident, eng):
            return port, info
        if ident is not None:
            print("[dashboard] a porta {} esta ocupada por outro servidor ({}) -- "
                  "o lock de `{}` foi descartado".format(
                      port, ident.get("slug") or "identidade desconhecida", eng.name),
                  file=sys.stderr)
    if lock.exists():
        try:
            lock.unlink()
        except OSError:
            pass
    return None


def write_lock(eng: Path, port: int) -> dict:
    """Write the lock AND return it, so the served identity is the same record."""
    info = {"engagement": str(eng.resolve()), "slug": eng.name, "port": port,
            "pid": os.getpid(), "started": now_iso(), "tool_version": TOOL_VERSION}
    _write_text(_lock_path(eng), json.dumps(info, ensure_ascii=False, indent=2))
    return info


def clear_lock(eng: Path) -> None:
    try:
        _lock_path(eng).unlink()
    except OSError:
        pass


def serve(eng: Path, port: int) -> tuple[socketserver.BaseServer, int]:
    """Bind 127.0.0.1 only -- an engagement holds client material and must never be
    reachable from the network. Walks forward if the port is taken."""
    handler = functools.partial(_Handler, directory=str(eng))
    last: OSError | None = None
    for candidate in range(port, port + 12):
        try:
            httpd = socketserver.ThreadingTCPServer(("127.0.0.1", candidate), handler)
        except OSError as exc:
            last = exc
            continue
        httpd.daemon_threads = True
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        info = write_lock(eng, candidate)
        _Handler.build_holder.update({
            "engagement": info["engagement"],
            "pid": info["pid"], "started": info["started"]})
        return httpd, candidate
    raise SystemExit("[dashboard] nenhuma porta livre em {}-{}: {}".format(port, port + 11, last))


def build_once(eng: Path, out: Path, today: date, reload_secs: int,
               json_out: str | None = None) -> tuple[int, dict | None]:
    """Render one dashboard. On an internal failure the page shows the traceback rather
    than going silently stale. Returns (exit_code, model|None)."""
    try:
        model = build_model(eng, today)
    except Exception as exc:  # noqa: BLE001
        _write_text(out, error_page(eng, exc, reload_secs))
        print("[dashboard] build falhou: {} -> pagina de erro em {}".format(exc, out),
              file=sys.stderr)
        return 1, None
    _write_text(out, render_html(model, max(0, reload_secs)))
    _Handler.build_holder["build"] = model["build"]
    # Same source as the page's own payload, so "is this my server?" compares like
    # with like -- the folder name would not (a copy keeps the declared slug).
    _Handler.build_holder["slug"] = model["engagement"]["slug"]
    if json_out:
        _write_text(json_out, json.dumps(model, ensure_ascii=False, indent=2, default=str))
    return 0, model


DISCOVERY_LENSES = ["business", "operations", "user", "data", "governance", "financial"]


def lens_wrote_round(path: Path, round_id: str) -> bool:
    """True when `lens-outputs/<lens>.md` carries a section HEADER for `round_id`.

    A lens appends `## R-NN — <lens>` (legacy files: `## R-NN (date)`,
    `## R-NN — date`). The match is on the heading line, never a substring of
    the body: prose that says "vs R-02" is not R-02's output. One rule, read
    by the guard (`pre-lens-order-check.py`), the round close test
    (`aisa-round` 5a) and the model below."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    pat = re.compile(r"^##\s+" + re.escape(round_id) + r"(?![\w-])", re.MULTILINE)
    return bool(pat.search(text))


def lenses_for_round(eng: Path, round_id: str) -> dict:
    """Discovery lenses that stamped `round_id` vs the ones still missing.

    `{"ronda": "R-02", "corridas": [...], "em_falta": [...]}`; empty lists and
    `ronda == ""` when no round is given. Order is the habitual one of
    `phases.md`, purely for display -- `/round <lens>` may run any lens alone."""
    if not round_id:
        return {"ronda": "", "corridas": [], "em_falta": []}
    ran = [l for l in DISCOVERY_LENSES
           if lens_wrote_round(eng / "lens-outputs" / f"{l}.md", round_id)]
    return {"ronda": round_id, "corridas": ran,
            "em_falta": [l for l in DISCOVERY_LENSES if l not in ran]}


def _open_round(state: dict) -> str:
    """The round an open `/round` is filling, "" when none is.

    Mirrors `.claude/hooks/pre-lens-order-check.py::in_progress_round`: a
    `round_in_progress` equal to or behind `round` is a leftover from a closed
    round (phase transition, hand edit) and is not an open round."""
    open_round = (state.get("round_in_progress") or "").strip()
    if not open_round:
        return ""
    om = re.search(r"(\d+)", open_round)
    lm = re.search(r"(\d+)", state.get("round") or "R-00")
    if not om or not lm:
        return ""
    return open_round if int(om.group(1)) > int(lm.group(1)) else ""


def summary_line(model: dict, out: Path) -> str:
    s = model["su"]["sections"]
    e = model["engagement"]
    ronda = e["round"] + (" (+{} em curso)".format(e["round_in_progress"])
                          if e["round_in_progress"] else "")
    return ("[dashboard] {} | fase {} ronda {} | C{} A{} U{} X{} R{} | saude {}% "
            "({} expiradas) | {} diagnostics -> {}").format(
        e["slug"], e["phase"], ronda,
        s["Confirmed"]["open"], s["Assumed"]["open"], s["Unknown"]["open"],
        s["Conflicted"]["open"], s["Risky"]["open"],
        model["health"]["pct"], model["health"]["expired"], len(model["diagnostics"]), out)


def watch(eng: Path, out: Path, args, poll: float) -> int:
    """Poll the engagement's mtimes and rebuild on change.

    The PostToolUse hook only sees the AGENT'S Write/Edit calls. Anything else that
    touches the engagement -- a human in an editor, a script, another session, a git
    checkout -- is invisible to it, and the browser then reloads a stale page forever.
    This loop is what makes the page live for those writers. Stdlib only: mtime polling,
    no watchdog, no inotify."""
    print("[dashboard] watch a cada {:g}s em {} -- Ctrl+C para sair".format(poll, eng),
          file=sys.stderr)
    builds = 0
    try:
        while True:
            if _needs_rebuild(eng, out, 0.0):
                today = _as_date(args.today) or date.today()
                code, model = build_once(eng, out, today, args.reload)
                builds += 1
                if model is not None and not args.quiet:
                    print(summary_line(model, out))
                elif code:
                    print("[dashboard] rebuild #{} falhou".format(builds), file=sys.stderr)
            time.sleep(poll)
    except KeyboardInterrupt:
        print("[dashboard] watch terminado apos {} rebuilds".format(builds), file=sys.stderr)
        return 0
    finally:
        clear_lock(eng)


def blueprint_check_cli(path: Path, slug: str | None, base: Path) -> int:
    """`--blueprint-check FILE`: structural issues of one blueprint file, one per line."""
    if not path.is_file():
        print("[dashboard] ficheiro não existe: {}".format(path), file=sys.stderr)
        return 3
    eng = None
    if slug:
        eng = find_engagement(base, slug)
    if eng is None and path.resolve().parent.name == "_blueprint" \
            and (path.resolve().parent.parent / "_state.json").is_file():
        eng = path.resolve().parent.parent
    su_ids = None
    cfg: dict = {}
    loader = None
    if eng is not None:
        _h, rows, _m, _d = parse_su(_read(eng / "shared-understanding.md") or "")
        su_ids = {r["id"] for r in rows if r.get("id")}
        cfg = bp_pack_cfg(_read_json(eng / "_state.json").get("pack", ""))
        loader = bp_loader(eng)
    issues = bp_validate(_read(path) or "", path.name, cfg, su_ids, loader)
    for i in issues:
        print("{code} · {severity} · {path} · L{line} · {message}".format(**i))
    nb = sum(1 for i in issues if i["severity"] == "block")
    nw = len(issues) - nb
    print("valid: {} ({} block, {} warn){}".format(
        "yes" if not nb else "no", nb, nw,
        "" if su_ids is not None else " · BP-DEAD-ID not evaluated (no engagement)"))
    return 0 if not nb else 4


def main(argv: list[str] | None = None) -> int:
    utf8_console()
    ap = argparse.ArgumentParser(
        prog="dashboard.py",
        description="aisa living dashboard -- deterministic HTML projection of an engagement.")
    ap.add_argument("--engagement", help="slug or path; default = most recently touched")
    ap.add_argument("--out", help="output HTML path; default <engagement>/dashboard.html")
    ap.add_argument("--json", dest="json_out", help="also dump the intermediate model as JSON")
    ap.add_argument("--open", dest="do_open", action="store_true", help="open in the default browser")
    ap.add_argument("--reload", type=int,
                    default=int(os.environ.get("AISA_DASHBOARD_RELOAD", DEFAULT_RELOAD_SECS)),
                    help="browser auto-reload seconds (0 disables)")
    ap.add_argument("--today", help="ISO date to evaluate expiry against (testing)")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--force", action="store_true", help="ignore the mtime debounce")
    ap.add_argument("--serve", nargs="?", type=int, const=DEFAULT_PORT, default=None,
                    metavar="PORT",
                    help="serve the engagement over http://127.0.0.1:PORT (default "
                         + str(DEFAULT_PORT) + "). Implies --watch. Over HTTP the page polls "
                         "/__build and reloads only when the build actually changes, instead "
                         "of the blind timer file:// forces on it.")
    ap.add_argument("--url", action="store_true",
                    help="print where this engagement's dashboard can be opened (a running "
                         "server's URL, else the file:// path) and exit. Nothing is built.")
    ap.add_argument("--watch", nargs="?", type=float, const=2.0, default=None,
                    metavar="SECS",
                    help="stay running and rebuild whenever the engagement changes "
                         "(default poll: 2s). Covers writers the PostToolUse hook cannot "
                         "see -- editors, scripts, other sessions.")
    ap.add_argument("--which-engagement", action="store_true",
                    help="print the slug of the engagement this invocation resolves to and "
                         "exit. Exit 0 with the slug; exit 4 listing the candidates when "
                         "several are mounted and no --engagement was given (the caller must "
                         "ask, never guess); exit 3 when none is mounted. Used by /frame, "
                         "/options and /decide to pass `--engagement <slug>` to the skill, so "
                         "the gate hook records its verdict against the right project.")
    ap.add_argument("--blueprint-check", metavar="FILE",
                    help="structural check of one ux-blueprint_vNN.yaml against "
                         "blueprint-contract.md -> Validação estrutural. Prints one line per "
                         "issue and a verdict; exit 0 valid, 4 when a `block` issue exists. "
                         "Resolves the engagement from the file's folder when --engagement "
                         "is absent. Nothing is built.")
    ap.add_argument("--authority-stamp", nargs="?", const="", default=None, metavar="vNN",
                    help="print the authority stamp aisa-synthesize writes at the head of "
                         "architecture-story.md -- `authority: _blueprint/ux-blueprint_vNN."
                         "yaml#architecture @ sha256:<hex>` -- for the given version, else "
                         "the approved one, else the latest authorized. Nothing is built.")
    ap.add_argument("--version", action="version", version="dashboard.py " + TOOL_VERSION)
    args = ap.parse_args(argv)

    base = engagements_root()
    if args.which_engagement:
        if args.engagement:
            eng = find_engagement(base, args.engagement)
            if eng is None:
                print("[dashboard] engagement nao resolvido: {}".format(args.engagement),
                      file=sys.stderr)
                return 3
            print(eng.name)
            return 0
        mounted = sorted(d for d in base.iterdir()
                         if d.is_dir() and (d / "_state.json").is_file())             if base.is_dir() else []
        if not mounted:
            print("[dashboard] nenhum engagement montado em {}".format(base), file=sys.stderr)
            return 3
        if len(mounted) > 1:
            print("[dashboard] varios engagements montados — passa --engagement <slug>:",
                  file=sys.stderr)
            for m in mounted:
                print("  " + m.name, file=sys.stderr)
            return 4
        print(mounted[0].name)
        return 0
    if args.blueprint_check:
        return blueprint_check_cli(Path(args.blueprint_check), args.engagement, base)
    eng = find_engagement(base, args.engagement)
    if eng is None:
        print("[dashboard] engagement nao resolvido em {} (--engagement <slug>)".format(base),
              file=sys.stderr)
        return 3

    today = date.today()
    if args.today:
        d = _as_date(args.today)
        if d is None:
            print("[dashboard] --today invalido: {}".format(args.today), file=sys.stderr)
            return 2
        today = d

    out = Path(args.out) if args.out else (eng / "dashboard.html")

    if args.authority_stamp is not None:
        blocks = classify_decisions(_read(eng / "decisions.md") or "")
        bp = blueprint_state(eng, blocks)
        want = args.authority_stamp.strip()
        if want:
            m = re.search(r"(\d{1,3})", want)
            ver = ("v" + m.group(1).zfill(2)) if m else ""
        else:
            ver = ((bp.get("approved") or {}).get("version")
                   or (bp.get("latest_authorized") or {}).get("version") or "")
        f = _bp_file(eng, ver) if ver else None
        sha = architecture_block_sha256(_read(f) or "") if f else ""
        if not sha:
            print("[dashboard] sem bloco architecture legível para {} em {}/_blueprint"
                  .format(ver or "(nenhuma versão aprovada ou autorizada)", eng.name),
                  file=sys.stderr)
            return 3
        vinfo = next((v for v in bp.get("versions", []) if v["version"] == ver), None)
        if vinfo is not None and not vinfo.get("valid", True):
            # A4.5: the stamp names an approved/authorized version whose structure fails —
            # the skill must stop; nothing downstream consumes an invalid version.
            print("authority: _blueprint/{}#architecture @ sha256:{} INVALID".format(f.name, sha))
            print("[dashboard] {} falha a verificação estrutural ({} bloqueio(s): {}) — não usar; "
                  "refazer o desenho (/blueprint) antes de sintetizar ou renderizar".format(
                      ver, vinfo.get("blocking", 0), ", ".join(vinfo.get("issue_codes") or [])),
                  file=sys.stderr)
            return 5
        print("authority: _blueprint/{}#architecture @ sha256:{}".format(f.name, sha))
        return 0

    if args.url:
        live = running_server(eng)
        if live:
            url = "http://127.0.0.1:{}/".format(live[0])
            print("{}  (servidor vivo, pid {}, desde {})".format(
                url, live[1].get("pid", "?"), live[1].get("started", "?")))
        elif out.exists():
            url = out.resolve().as_uri()
            print("{}  (ficheiro; sem servidor -- '/dashboard --serve' para o modo vivo)".format(url))
        else:
            print("[dashboard] {} ainda nao tem dashboard -- correr '/dashboard --serve --open'"
                  .format(eng.name), file=sys.stderr)
            return 3
        if args.do_open:
            try:
                webbrowser.open(url)
            except Exception:
                pass
        return 0

    if args.serve is not None and not args.force:
        # Check BEFORE building: the running watcher owns dashboard.html, and a second
        # process writing it is exactly the race this reattach exists to prevent.
        live = running_server(eng)
        if live:
            url = "http://127.0.0.1:{}/".format(live[0])
            print("[dashboard] ja esta a servir {} em {} (pid {}, desde {}) -- reaproveitado, "
                  "nada reconstruido. --force arranca um segundo (nao recomendado: dois "
                  "watchers competem pelo mesmo ficheiro).".format(
                      eng.name, url, live[1].get("pid", "?"), live[1].get("started", "?")),
                  file=sys.stderr)
            print(url)
            if args.do_open:
                try:
                    webbrowser.open(url)
                except Exception:
                    pass
            return 0

    debounce = float(os.environ.get("AISA_DASHBOARD_DEBOUNCE", "2"))
    stale = _needs_rebuild(eng, out, debounce)
    if args.serve is not None and not args.watch:
        args.watch = 2.0

    if not args.force and not args.json_out and not args.do_open and not args.watch and not stale:
        if not args.quiet:
            print("[dashboard] sem alteracoes desde o ultimo build -> {}".format(out))
        return 0

    code, model = build_once(eng, out, today, args.reload, args.json_out)
    if model is not None and not args.quiet:
        print(summary_line(model, out))

    url = out.resolve().as_uri()
    if args.serve is not None:
        _, port = serve(eng, args.serve)
        url = "http://127.0.0.1:{}/".format(port)
        print("[dashboard] a servir {} em {} (so 127.0.0.1)".format(eng.name, url),
              file=sys.stderr)

    if args.do_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    if args.watch:
        return watch(eng, out, args, args.watch)
    return code


if __name__ == "__main__":
    sys.exit(main())
