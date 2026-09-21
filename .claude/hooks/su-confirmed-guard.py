"""su-confirmed-guard.py -- PostToolUse guard for the Confirmed threshold (P-12).

Fires after a Write/Edit on an engagement's shared-understanding.md and checks the
deterministic half of `library/kernel/states.md` -> *Confirmed threshold*: does every
new or changed `C-` row carry a locator of the five classes, and does that locator's
target exist?

Design notes:
  * One implementation of the rule, two consumers. The regex lives in
    library/kernel/tools/dashboard.py (`locator_classes`, `evidence_targets`,
    `audit_confirmed_locators`); this hook imports it and never restates it.
  * Only the rows the write TOUCHED. An Edit names them: the `C-` ids in
    `new_string`. A Write replaces the whole file and there is no previous version
    to diff against, so the audit covers every open `Confirmed` -- and the message
    says so, rather than pretending the write created them.
  * Judgement is not here. Whether a claim says more than its evidence is the
    arbiter's reading (aisa-round step 5f) and the lenses' Hard rules. This hook
    checks presence and existence.
  * Never blocks. Warns on stderr, appends one idempotent line per id to
    council-log.md, always exits 0.

Env: AISA_ENGAGEMENTS_ROOT (shared with on-su-change.py).
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

TOOL_REL = Path("library") / "kernel" / "tools" / "dashboard.py"
LOG_LINE = "Confirmed sem locator: {}"
ROW_ID_RE = re.compile(r"^\s*\|\s*\**\s*(C-\d{2,4})\b", re.M)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def engagements_root() -> Path:
    raw = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (repo_root() / p)
    return repo_root() / "projects"


def engagement_from_path(file_path: str) -> Path | None:
    try:
        p = Path(file_path).resolve()
    except Exception:
        return None
    for parent in [p] + list(p.parents):
        if (parent / "_state.json").is_file():
            return parent
    return None


def load_motor():
    """Import the kernel motor as a module -- the rule has one home."""
    tool = repo_root() / TOOL_REL
    if not tool.is_file():
        return None
    spec = importlib.util.spec_from_file_location("aisa_dashboard", tool)
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def touched_ids(tool_input: dict, tool_name: str) -> set[str] | None:
    """The `C-` rows this write touched, or None when the write gives no way to tell."""
    if tool_name == "Edit":
        return set(ROW_ID_RE.findall(tool_input.get("new_string") or ""))
    if tool_name == "MultiEdit":
        out: set[str] = set()
        for e in tool_input.get("edits") or []:
            out.update(ROW_ID_RE.findall(e.get("new_string") or ""))
        return out
    return None


def log_new(eng: Path, findings: list[dict]) -> list[str]:
    """Append one line per id that the log does not already carry. Idempotent."""
    log = eng / "council-log.md"
    body = ""
    if log.is_file():
        try:
            body = log.read_text(encoding="utf-8")
        except Exception:
            return []
    novos = [f for f in findings if LOG_LINE.format(f["id"]) not in body]
    if not novos:
        return []
    today = date.today().isoformat()
    head = "## Confirmed sem locator — {} (su-confirmed-guard)".format(today)
    chunk = "" if head in body else "\n" + head + "\n\n"
    for f in novos:
        chunk += "- {} — {}\n".format(LOG_LINE.format(f["id"]), f.get("motivo", ""))
    try:
        with open(log, "a", encoding="utf-8") as fh:
            fh.write(chunk)
    except Exception:
        return []
    return [f["id"] for f in novos]


def main() -> int:
    raw = sys.stdin.read()
    for i, ch in enumerate(raw):
        if ch in "{[":
            raw = raw[i:]
            break
    try:
        tool = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    tool_name = tool.get("tool_name") or ""
    if tool_name not in {"Write", "Edit", "MultiEdit"}:
        return 0
    tool_input = tool.get("tool_input") or {}
    file_path = tool_input.get("file_path") or ""
    if not file_path.replace("\\", "/").endswith("shared-understanding.md"):
        return 0

    eng = engagement_from_path(file_path)
    if eng is None:
        return 0
    motor = load_motor()
    if motor is None:
        return 0

    su = motor._read(eng / "shared-understanding.md") or ""
    if not su:
        return 0
    _header, rows, _meta, _diag = motor.parse_su(su)

    ids = touched_ids(tool_input, tool_name)
    if ids is not None and not ids:
        return 0
    audit = motor.audit_confirmed_locators(rows, eng, only_ids=ids)
    findings = audit["sem_locator"] + audit["alvo_ausente"]
    if not findings:
        return 0

    escopo = ("rows desta escrita" if ids is not None else
              "todas as Confirmed abertas (a escrita substituiu o ficheiro: sem versão "
              "anterior para comparar)")
    logged = log_new(eng, findings)
    print("[su-confirmed-guard] {} facto(s) Confirmed sem prova localizável — {}:"
          .format(len(findings), escopo), file=sys.stderr)
    for f in findings[:10]:
        print("  {} — {}".format(LOG_LINE.format(f["id"]), f.get("motivo", "")),
              file=sys.stderr)
    if len(findings) > 10:
        print("  … e mais {}".format(len(findings) - 10), file=sys.stderr)
    print("  regra: library/kernel/states.md → Confirmed threshold, regra 1. "
          "Aviso, não bloqueio.", file=sys.stderr)
    if logged:
        print("  registado em council-log.md: {}".format(", ".join(logged)),
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never block the user's write
        print("[su-confirmed-guard] ignorado: {}".format(exc), file=sys.stderr)
        sys.exit(0)
