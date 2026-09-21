"""on-su-change.py -- PostToolUse trigger for the living dashboard.

Fires after any Write/Edit inside an engagement folder and regenerates
<engagement>/dashboard.html via library/kernel/tools/dashboard.py.

Design notes:
  * No loop. PostToolUse fires on the AGENT'S Write/Edit tool calls; the generator
    writes with open() + os.replace() in a subprocess, which is filesystem I/O, not a
    tool invocation. Two cheap guards below cover a future model hand-editing the page.
  * Detached spawn, never waited on -- a /round writes 7 files back to back; a
    synchronous run would add ~250 ms to each of them and any generator bug would
    become a user-facing hang.
  * Never blocks. Everything is wrapped; the hook always exits 0.

Env: AISA_ENGAGEMENTS_ROOT, AISA_DASHBOARD_RELOAD, AISA_DASHBOARD_DEBOUNCE.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOL_REL = Path("library") / "kernel" / "tools" / "dashboard.py"

TRIGGER_FILES = {
    "shared-understanding.md", "_state.json", "decisions.md", "story.md",
    "council-log.md", "answers.md", "options.md", "frame.md", "context.json",
    "premortem.md",
}
TRIGGER_DIRS = ("_capture/", "_synthesis/", "_render/", "_blueprint/",
                "_simulation/", "_retro/", "lens-outputs/", "_coverage/")
# `_coverage/` joins the list because `status.coverage` is part of the model the page
# projects, and a published review changes it (coverage phase 4). It cannot loop: the
# engine's `finalize` writes with open() + os.replace() in a subprocess, which is
# filesystem I/O and not a tool call, so PostToolUse never fires on it; and the dashboard
# reads `_coverage/` and writes only `dashboard.html`, which is excluded below.


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def engagements_root() -> Path:
    raw = os.environ.get("AISA_ENGAGEMENTS_ROOT")
    if raw:
        p = Path(raw)
        return p if p.is_absolute() else (repo_root() / p)
    return repo_root() / "projects"


def engagement_from_path(file_path: str) -> Path | None:
    """Walk up from the written file to the folder holding _state.json. The hook knows
    the path, so it never has to guess which engagement is active."""
    try:
        p = Path(file_path).resolve()
    except Exception:
        return None
    root = engagements_root().resolve()
    for parent in [p] + list(p.parents):
        if (parent / "_state.json").is_file():
            try:
                if parent.parent.resolve() == root:
                    return parent
            except Exception:
                return parent
            return parent
    return None


def should_trigger(rel: str) -> bool:
    name = rel.rsplit("/", 1)[-1]
    if name in TRIGGER_FILES:
        return True
    return any(seg in rel for seg in TRIGGER_DIRS)


def debounced(eng: Path) -> bool:
    """Skip when dashboard.html was written moments ago -- a single /round writes SU +
    6 lens files in a burst."""
    out = eng / "dashboard.html"
    if not out.exists():
        return False
    try:
        window = float(os.environ.get("AISA_DASHBOARD_DEBOUNCE", "2"))
        return (time.time() - out.stat().st_mtime) < window
    except Exception:
        return False


def spawn(eng: Path) -> None:
    tool = repo_root() / TOOL_REL
    if not tool.is_file():
        return
    env = dict(os.environ)
    env["AISA_DASHBOARD_RUNNING"] = "1"
    env.setdefault("PYTHONIOENCODING", "utf-8")
    kw: dict = {
        "stdin": subprocess.DEVNULL,
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "cwd": str(repo_root()),
        "env": env,
    }
    if os.name == "nt":
        kw["creationflags"] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
    else:
        kw["start_new_session"] = True
    subprocess.Popen(
        [sys.executable, str(tool), "--engagement", str(eng), "--quiet"], **kw
    )


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

    if tool.get("tool_name") not in {"Write", "Edit"}:
        return 0
    if os.environ.get("AISA_DASHBOARD_RUNNING"):
        return 0

    file_path = (tool.get("tool_input") or {}).get("file_path") or ""
    rel = file_path.replace("\\", "/")
    if not rel or rel.endswith("dashboard.html"):
        return 0
    if not should_trigger(rel):
        return 0

    eng = engagement_from_path(file_path)
    if eng is None:
        return 0
    if debounced(eng):
        return 0

    spawn(eng)
    print(f"[on-su-change] dashboard a regenerar: {eng / 'dashboard.html'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # never block the user's write
        print(f"[on-su-change] ignorado: {exc}", file=sys.stderr)
        sys.exit(0)
