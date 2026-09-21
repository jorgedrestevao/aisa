#!/usr/bin/env python3
"""text_extract.py — aisa process-capture: capture-lite (deterministic text extraction).

Kernel asset (library/kernel/tools/). Read + executed at runtime, never edited at runtime.
Dependencies: Python 3.10+, python-docx (.docx), pypdf (.pdf), stdlib (.vtt).
No LLM, no network, no writes outside the given output paths.

Usage:
  extract : python text_extract.py <input> <out.text.md> <out.extraction.json> [--force] [--log <capture-log.md>]
  index   : python text_extract.py --index <engagement-root> [--log <capture-log.md>]

Contract (library/kernel/orchestration.md -> Evidence contract):
- Loss-minimizing extraction with provenance. NEVER summarization, interpretation,
  requirement extraction, risk classification or architectural inference.
- Everything the source said, plus where it said it.
- Caches on SHA-256 like xlsx_extract.py: unchanged input -> "cache-hit", no rewrite (unless --force).
- Degradation is visible, never silent: status in {ok, empty, failed, skipped}; a failure artefact
  is always written, the raw source always stays available and authoritative.
- Exit codes: 0 ok/cache-hit/empty/failed-artefact-written, 2 usage error or unsupported format.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import sys

TOOL_VERSION = "1.0.1"
ARTEFACT_ID = "aisa.capture.text-extraction"
XLSX_ARTEFACT_ID = "aisa.capture.extraction"

TEXT_FORMATS = (".docx", ".pdf", ".vtt")
XLSX_FORMATS = (".xlsx", ".xlsm")

CITE = {
    ".docx": "<file> · §<heading> ¶NN",
    ".pdf": "<file> · p.N",
    ".vtt": "<file> · [HH:MM:SS] <speaker>",
}


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


def short(value, limit: int = 120) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 1] + "…"


def append_log(log_path: str | None, layer: str, filename: str, event: str, detail: str) -> None:
    if not log_path:
        return
    new = not os.path.exists(log_path)
    os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# Capture log\n\n| timestamp | layer | file | event | detail |\n|---|---|---|---|---|\n")
        fh.write(f"| {now_iso()} | {layer} | {filename} | {event} | {detail} |\n")


def write_atomic(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    os.replace(tmp, path)


def write_json(path: str, doc: dict) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(doc, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    os.replace(tmp, path)


def md_escape_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>").strip()


def collapse_blanks(lines: list[str]) -> list[str]:
    """Drop trailing whitespace and collapse consecutive blank lines. Transport noise only."""
    out: list[str] = []
    blank = 0
    for line in lines:
        line = line.rstrip()
        if line:
            blank = 0
            out.append(line)
        else:
            blank += 1
            if blank == 1:
                out.append("")
    while out and not out[-1]:
        out.pop()
    return out


class ExtractionError(Exception):
    """Deterministic extraction could not run (status: failed / skipped)."""

    def __init__(self, reason: str, status: str = "failed"):
        super().__init__(reason)
        self.reason = reason
        self.status = status


# ---------------------------------------------------------------- .docx

def extract_docx(path: str) -> tuple[list[str], dict, str, str]:
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError:
        raise ExtractionError("python-docx not installed (pip install python-docx)", status="skipped")

    try:
        document = Document(path)
    except Exception as exc:
        raise ExtractionError(f"{type(exc).__name__}: {exc}")

    body: list[str] = []
    n_par = n_head = n_tab = 0

    for child in document.element.body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            para = Paragraph(child, document)
            text = para.text.strip()
            if not text:
                continue
            style = (para.style.name or "") if para.style is not None else ""
            level = None
            if style == "Title":
                level = 1
            else:
                m = re.match(r"^Heading (\d+)$", style)
                if m:
                    level = min(int(m.group(1)), 6)
            if level is not None:
                n_head += 1
                body.append("")
                body.append("#" * (level + 1) + " " + text)
                body.append("")
            else:
                n_par += 1
                body.append(f"[¶{n_par}] {text}")
                body.append("")
        elif tag == "tbl":
            table = Table(child, document)
            rows = [[md_escape_cell(cell.text) for cell in row.cells] for row in table.rows]
            if not rows:
                continue
            n_tab += 1
            width = max(len(r) for r in rows)
            rows = [r + [""] * (width - len(r)) for r in rows]
            body.append("")
            body.append(f"[table {n_tab}]")
            body.append("")
            body.append("| " + " | ".join(rows[0]) + " |")
            body.append("|" + "---|" * width)
            for row in rows[1:]:
                body.append("| " + " | ".join(row) + " |")
            body.append("")

    units = {"unit": "paragraph", "paragraphs": n_par, "headings": n_head, "tables": n_tab}
    if n_par == 0 and n_tab == 0:
        return collapse_blanks(body), units, "empty", "document contains no non-empty paragraph or table"
    return collapse_blanks(body), units, "ok", ""


# ---------------------------------------------------------------- .pdf

def extract_pdf(path: str) -> tuple[list[str], dict, str, str]:
    try:
        from pypdf import PdfReader
    except ImportError:
        raise ExtractionError("pypdf not installed (pip install pypdf)", status="skipped")

    try:
        reader = PdfReader(path)
        if reader.is_encrypted:
            try:
                opened = reader.decrypt("")
            except Exception as exc:
                raise ExtractionError(f"PDF is encrypted and could not be opened: {exc}")
            if not opened:
                raise ExtractionError("PDF is encrypted; no password available")
        pages = list(reader.pages)
    except ExtractionError:
        raise
    except Exception as exc:
        raise ExtractionError(f"{type(exc).__name__}: {exc}")

    if not pages:
        raise ExtractionError("PDF has 0 pages")

    body: list[str] = []
    empty_pages = 0
    chars = 0
    for i, page in enumerate(pages, start=1):
        body.append("")
        body.append(f"## [p.{i}]")
        body.append("")
        try:
            text = page.extract_text() or ""
        except Exception as exc:
            body.append(f"_extraction failed on this page: {type(exc).__name__}: {short(exc, 80)}_")
            empty_pages += 1
            continue
        lines = collapse_blanks(text.splitlines())
        if lines:
            chars += sum(len(line) for line in lines)
            body.extend(lines)
        else:
            empty_pages += 1
            body.append("_no extractable text on this page_")

    units = {"unit": "page", "pages": len(pages), "pages_without_text": empty_pages, "chars": chars}
    if empty_pages == len(pages):
        raise ExtractionError(
            f"no extractable text in any of {len(pages)} pages "
            "(image-only or scanned); no OCR in this tier — read the raw source")
    return collapse_blanks(body), units, "ok", ""


# ---------------------------------------------------------------- .vtt

TIMING_RE = re.compile(
    r"^\s*(?P<start>(?:\d+:)?\d{1,2}:\d{2}(?:[.,]\d{1,3})?)\s*-->\s*"
    r"(?P<end>(?:\d+:)?\d{1,2}:\d{2}(?:[.,]\d{1,3})?)")
VOICE_RE = re.compile(r"<v(?:\.[^\s>]+)*\s+(?P<name>[^>]*)>", re.IGNORECASE)
TAG_RE = re.compile(r"</?[^>]{0,200}>")


def _hhmmss(stamp: str) -> str:
    stamp = stamp.replace(",", ".").split(".")[0]
    parts = stamp.split(":")
    if len(parts) == 2:
        parts = ["0"] + parts
    return ":".join(f"{int(p):02d}" for p in parts)


def extract_vtt(path: str) -> tuple[list[str], dict, str, str]:
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as fh:
            raw = fh.read()
    except Exception as exc:
        raise ExtractionError(f"{type(exc).__name__}: {exc}")

    if "WEBVTT" not in raw[:64]:
        raise ExtractionError("not a WebVTT file (missing WEBVTT signature)")

    blocks = re.split(r"\n\s*\n", raw.replace("\r\n", "\n").replace("\r", "\n"))
    cues: list[dict] = []
    for block in blocks:
        lines = [ln for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue
        head = lines[0].strip().upper()
        if head.startswith(("WEBVTT", "NOTE", "STYLE", "REGION")):
            continue
        timing_i = next((i for i, ln in enumerate(lines) if TIMING_RE.match(ln)), None)
        if timing_i is None:
            continue
        m = TIMING_RE.match(lines[timing_i])
        payload_lines = lines[timing_i + 1:]
        if not payload_lines:
            continue
        payload = " ".join(ln.strip() for ln in payload_lines)
        speaker = None
        voice = VOICE_RE.search(payload)
        if voice:
            speaker = html.unescape(voice.group("name")).strip() or None
        text = html.unescape(TAG_RE.sub("", payload))
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        cues.append({"start": _hhmmss(m.group("start")), "end": _hhmmss(m.group("end")),
                     "speaker": speaker, "text": text})

    if not cues:
        return [], {"unit": "cue", "cues": 0, "passages": 0, "speakers": 0}, "empty", \
            "WebVTT file contains 0 cues"

    # Merge consecutive cues from the SAME named speaker; never merge unattributed cues.
    merged: list[dict] = []
    for cue in cues:
        prev = merged[-1] if merged else None
        if prev and cue["speaker"] and prev["speaker"] == cue["speaker"]:
            prev["end"] = cue["end"]
            prev["text"] = prev["text"] + " " + cue["text"]
        else:
            merged.append(dict(cue))

    body: list[str] = []
    for passage in merged:
        stamp = passage["start"] if passage["start"] == passage["end"] \
            else f"{passage['start']}–{passage['end']}"
        if passage["speaker"]:
            body.append(f"[{stamp}] **{passage['speaker']}:** {passage['text']}")
        else:
            body.append(f"[{stamp}] {passage['text']}")
        body.append("")

    speakers = sorted({c["speaker"] for c in cues if c["speaker"]})
    units = {"unit": "cue", "cues": len(cues), "passages": len(merged),
             "speakers": len(speakers), "speaker_names": speakers}
    return collapse_blanks(body), units, "ok", ""


EXTRACTORS = {".docx": extract_docx, ".pdf": extract_pdf, ".vtt": extract_vtt}
LIBRARIES = {".docx": "python-docx", ".pdf": "pypdf", ".vtt": "stdlib"}


# ---------------------------------------------------------------- extract driver

def render_md(identity: dict, status: str, reason: str, body: list[str]) -> str:
    fmt = identity["format"]
    head = [
        f"<!-- {ARTEFACT_ID} | text_extract.py {TOOL_VERSION} | deterministic extraction, no interpretation -->",
        f"# Source: {identity['filename']}",
        "",
        f"- format: `{fmt}` · size: {identity['size_bytes']} B · modified: {identity['modified']}",
        f"- sha256: `{identity['sha256'][:16]}`",
        f"- status: **{status}**" + (f" — {reason}" if reason else ""),
        f"- cite as: `{CITE[fmt]}`",
        f"- raw source stays authoritative on conflict: `inputs/{identity['filename']}`",
        "",
        "---",
        "",
    ]
    if status in {"failed", "skipped"}:
        head.append(f"_No extraction. {reason}. Read the raw source with the format table in "
                    "`library/kernel/orchestration.md` → Evidence contract._")
        head.append("")
        return "\n".join(head)
    if status == "empty":
        head.append(f"_Extraction ran and found nothing: {reason}. Absence is evidence — "
                    "the source is not silently omitted._")
        head.append("")
        return "\n".join(head)
    return "\n".join(head + body) + "\n"


def extract(path: str, md_out: str, json_out: str, force: bool, log_path: str | None) -> int:
    filename = os.path.basename(path)
    if not os.path.exists(path):
        print(f"input not found: {path}", file=sys.stderr)
        return 2
    fmt = os.path.splitext(filename)[1].lower()
    if fmt not in EXTRACTORS:
        print(f"unsupported format for capture-lite: {fmt} (supported: {', '.join(TEXT_FORMATS)})",
              file=sys.stderr)
        return 2

    sha = sha256_file(path)
    if not force and os.path.exists(json_out) and os.path.exists(md_out):
        try:
            with open(json_out, encoding="utf-8") as fh:
                previous = json.load(fh)
            reusable = (previous.get("artefact") == ARTEFACT_ID
                        and previous.get("identity", {}).get("sha256") == sha
                        and previous.get("tool", {}).get("version") == TOOL_VERSION)
            # A cached artefact is only an extraction when it HOLDS one. `failed` and
            # `skipped` record why nothing came out -- a missing library, a transient
            # read error -- and the cause usually lives outside this file, so the hash
            # that keyed it says nothing about whether it is still true. Reusing them
            # froze a fixed environment's failure forever (F11, adversarial review
            # 2026-09-08). `xlsx_extract.py` already required `status == "ok"`; this is
            # the same rule, and `--force` stays what it was: a way to redo an OK one.
            prev_status = previous.get("status")
            if reusable and prev_status == "ok":
                print(f"cache-hit: {filename} unchanged (sha256 {sha[:8]}), extraction kept")
                append_log(log_path, "LT", filename, "cache-hit", f"sha256 {sha[:8]}")
                return 0
            if reusable:
                reason = short(previous.get("reason") or "sem motivo registado")
                print(f"retry: {filename} unchanged (sha256 {sha[:8]}) but the cached "
                      f"extraction is {prev_status} ({reason}) -- extracting again")
                append_log(log_path, "LT", filename, "cache-retry",
                           f"{prev_status}: {reason}")
        except Exception:
            pass  # unreadable previous artefact -> re-extract

    stat = os.stat(path)
    identity = {
        "filename": filename,
        "source_path": path,
        "format": fmt,
        "size_bytes": stat.st_size,
        "sha256": sha,
        "modified": dt.datetime.fromtimestamp(stat.st_mtime).isoformat(timespec="seconds"),
    }

    try:
        body, units, status, reason = EXTRACTORS[fmt](path)
    except ExtractionError as exc:
        body, units, status, reason = [], {"unit": CITE[fmt]}, exc.status, exc.reason

    doc = {
        "artefact": ARTEFACT_ID,
        "tool": {"name": "text_extract.py", "version": TOOL_VERSION,
                 "library": LIBRARIES[fmt],
                 "python": ".".join(map(str, sys.version_info[:3]))},
        "extracted_at": now_iso(),
        "identity": identity,
        "status": status,
        "reason": reason or None,
        "units": units,
        "provenance": {"cite_as": CITE[fmt]},
        "output": {"text_md": os.path.basename(md_out)},
    }
    write_atomic(md_out, render_md(identity, status, reason, body))
    write_json(json_out, doc)

    detail = ", ".join(f"{k} {v}" for k, v in units.items()
                       if k != "unit" and isinstance(v, int)) or "—"
    if status == "ok":
        print(f"extracted: {filename} -> {md_out} ({detail}, sha256 {sha[:8]})")
        append_log(log_path, "LT", filename, "extracted", f"{detail}, sha256 {sha[:8]}")
    else:
        print(f"extraction {status.upper()} for {filename}: {reason} -> artefact written "
              f"({md_out}); raw source stays available")
        append_log(log_path, "LT", filename, status, short(reason))
    return 0


# ---------------------------------------------------------------- evidence index

def _declined_calls(replay_md_path: str) -> int:
    """How many formula calls the L3 replay declined, read from its own report.

    No new artefact and no re-derivation: `xlsx_extract.py` writes the line, this reads
    it. A missing or older replay report simply contributes nothing."""
    try:
        with open(replay_md_path, encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"\*\*Out of scope: (\d+) formula call", line)
                if m:
                    return int(m.group(1))
    except OSError:
        pass
    return 0


INDEX_HEADER = """# Evidence index

Shared evidence surface for this engagement — **parse once, reason many**
(`library/kernel/orchestration.md` → *Evidence contract*).

Normalized evidence below is the normal reading surface. Raw sources stay in `inputs/`,
are always openable, and are **authoritative on conflict**. Inspect the raw source when
material to confidence — not to satisfy a quota.

| source | format | normalized evidence | status | cite as |
|---|---|---|---|---|
"""

INDEX_FOOTER = """
**Status vocabulary** — `ok` extracted · `empty` extraction ran, the source has no content
(absence is evidence) · `failed` deterministic extraction could not run, read the raw source ·
`skipped` extraction library unavailable, read the raw source · `not captured` format outside
the capture tiers (not a failure) — read the raw source with the format table in
`library/kernel/orchestration.md` → *Evidence contract*.

Regenerate with `python library/kernel/tools/text_extract.py --index <engagement>`.
"""


def _read_json(path: str) -> dict | None:
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except Exception:
        return None


def build_index(root: str, log_path: str | None) -> int:
    inputs_dir = os.path.join(root, "inputs")
    capture_dir = os.path.join(root, "_capture")
    if not os.path.isdir(inputs_dir):
        print(f"no inputs/ directory under {root}", file=sys.stderr)
        return 2

    names = sorted(n for n in os.listdir(inputs_dir)
                   if os.path.isfile(os.path.join(inputs_dir, n)) and not n.startswith("."))
    rows = []
    counts: dict[str, int] = {}
    for name in names:
        fmt = os.path.splitext(name)[1].lower()
        doc = _read_json(os.path.join(capture_dir, f"{name}.extraction.json"))
        if fmt in XLSX_FORMATS and doc and doc.get("artefact") == XLSX_ARTEFACT_ID:
            status = doc.get("status", "failed")
            declined = _declined_calls(os.path.join(capture_dir, f"{name}.replay.md"))
            normalized = f"`process-model.md` (PM ids) + `{name}.replay.md`"
            if declined:
                # What the replay DECLINED belongs next to what it checked: a reader who
                # sees "0 findings" must be able to tell a clean workbook from one whose
                # formulas were mostly out of the battery's scope (P-17).
                normalized += f" — {declined} chamada(s) fora do alcance do replay"
            cite = "`PM-NNN → <sheet>!<cell>`"
        elif fmt in TEXT_FORMATS and doc and doc.get("artefact") == ARTEFACT_ID:
            status = doc.get("status", "failed")
            normalized = f"`{name}.text.md`"
            cite = f"`{doc.get('provenance', {}).get('cite_as', CITE[fmt])}`"
        else:
            status, normalized, cite = "not captured", "—", f"raw (`inputs/{name}`)"
        counts[status] = counts.get(status, 0) + 1
        rows.append(f"| `{name}` | `{fmt or '—'}` | {normalized} | `{status}` | {cite} |")

    out_path = os.path.join(capture_dir, "evidence-index.md")
    write_atomic(out_path, INDEX_HEADER + "\n".join(rows) + "\n" + INDEX_FOOTER)
    summary = ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) or "no sources"
    print(f"evidence index: {out_path} ({len(rows)} sources — {summary})")
    append_log(log_path, "LT", "evidence-index.md", "indexed", f"{len(rows)} sources — {summary}")
    return 0


# ---------------------------------------------------------------- cli

def main(argv=None) -> int:
    utf8_console()
    parser = argparse.ArgumentParser(
        description="aisa process-capture: capture-lite deterministic text extraction (.docx/.pdf/.vtt)")
    parser.add_argument("--index", action="store_true",
                        help="rebuild <engagement>/_capture/evidence-index.md")
    parser.add_argument("--force", action="store_true", help="ignore the extraction cache")
    parser.add_argument("--log", default=None, help="append events to this capture log file")
    parser.add_argument("--version", action="version", version=f"text_extract.py {TOOL_VERSION}")
    parser.add_argument("paths", nargs="+",
                        help="extract: <input> <out.text.md> <out.extraction.json> | "
                             "index: <engagement-root>")
    args = parser.parse_args(argv)

    if args.index:
        if len(args.paths) != 1:
            parser.error("--index takes exactly one path: <engagement-root>")
        return build_index(args.paths[0], args.log)
    if len(args.paths) != 3:
        parser.error("extract takes three paths: <input> <out.text.md> <out.extraction.json>")
    return extract(args.paths[0], args.paths[1], args.paths[2], args.force, args.log)


if __name__ == "__main__":
    sys.exit(main())
