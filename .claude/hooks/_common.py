"""_common.py -- what more than one aisa hook needs, in one place.

Created for the runtime-hardening front (bloco C): `phase-gate-check.py` and
`phase-completeness.py` were both resolving the engagement, and the gate hook cannot
afford the completeness hook's tolerance -- writing a gate verdict into the wrong
project is worse than not writing one. So the resolution is shared and its ambiguity
policy is a parameter, not a copy.

Nothing here writes. Nothing here blocks.
"""

from __future__ import annotations

import json
import os
import re
import runpy
import sys
from pathlib import Path


def utf8_stderr() -> None:
    """Claude Code surfaces hook stderr verbatim; on Windows it defaults to cp1252 and
    mangles arrows and accents."""
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def engagements_root() -> Path:
    raw = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (repo_root() / p)
    return repo_root() / "projects"


def load_dashboard() -> dict:
    """The kernel motor as a namespace. Executing is not writing: the read-only rule
    covers runtime edits of `library/`."""
    return runpy.run_path(str(repo_root() / "library" / "kernel" / "tools" / "dashboard.py"))


def _activity_mtime(eng: Path) -> float:
    stamps = [0.0]
    for rel in ("_state.json", "shared-understanding.md", "decisions.md", "council-log.md"):
        f = eng / rel
        if f.exists():
            try:
                stamps.append(f.stat().st_mtime)
            except OSError:
                pass
    return max(stamps)


def mounted_engagements(base: Path | None = None) -> list[Path]:
    base = base or engagements_root()
    if not base.is_dir():
        return []
    return sorted(d for d in base.iterdir() if d.is_dir() and (d / "_state.json").is_file())


def find_engagement(slug: str | None = None, *, allow_ambiguous: bool = True,
                    base: Path | None = None) -> tuple[Path | None, str]:
    """-> (engagement, how) where `how` is one of:

        "explicit"   the slug was given and resolved
        "only"       no slug, exactly one engagement mounted
        "recent"     no slug, several mounted, most recently active picked
        "ambiguous"  no slug, several mounted, and the caller refuses to guess
        "none"       nothing resolvable

    `allow_ambiguous=False` is for a caller that WRITES into the engagement it picks:
    guessing there records a verdict against the wrong project. A caller that only
    reports (phase-completeness) keeps the tolerant default.
    """
    base = base or engagements_root()
    if slug:
        cand = base / slug
        if (cand / "_state.json").is_file():
            return cand, "explicit"
        p = Path(slug)
        if (p / "_state.json").is_file():
            return p, "explicit"
        return None, "none"
    engs = mounted_engagements(base)
    if not engs:
        return None, "none"
    if len(engs) == 1:
        return engs[0], "only"
    if not allow_ambiguous:
        return None, "ambiguous"
    return max(engs, key=_activity_mtime), "recent"


def read_text(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def read_state(eng: Path) -> dict:
    try:
        return json.loads(read_text(eng / "_state.json") or "{}")
    except json.JSONDecodeError:
        return {}


def tool_payload(raw: str) -> dict:
    """The hook's stdin JSON, tolerant of a leading banner."""
    for i, ch in enumerate(raw or ""):
        if ch in "{[":
            raw = raw[i:]
            break
    try:
        return json.loads(raw) if (raw or "").strip() else {}
    except json.JSONDecodeError:
        return {}


ARG_SLUG_RE = re.compile(r"--engagement[= ]+\"?([A-Za-z0-9._\-]+)\"?")
ARG_FLAG_RE = re.compile(r"--override[= ]+(\"([^\"]*)\"|'([^']*)'|(\S+))")


def arg_slug(args: str) -> str:
    m = ARG_SLUG_RE.search(args or "")
    return m.group(1) if m else ""


def arg_override(args: str) -> tuple[bool, str]:
    """-> (present, reason). `--override` with no reason is still an override; the
    reason is what the skill logs, and an empty one is reported as empty, not invented."""
    m = ARG_FLAG_RE.search(args or "")
    if not m:
        return ("--override" in (args or "")), ""
    return True, (m.group(2) or m.group(3) or m.group(4) or "").strip()
