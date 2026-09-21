"""pre-write-guard.py — PreToolUse guard for Write/Edit.

Enforces library/ read-only at runtime (the one hard guard). Fails CLOSED:
blocks writes to library/* unless AISA_GUARD_MODE=log is set as an explicit
administrative override. .claude/settings.json sets the mode in env, and the
permissions.deny rules are a second layer whose matching semantics belong to the
harness, not to this file — so this guard never relies on them.

Path matching is on the CANONICAL path, not on the string as typed. The review of
2026-09-08 wrote `LIBRARY/kernel/states.md` on Windows: same file, guard returned
0, because the check was a case-sensitive substring test (P-R13). Anything that
resolves inside `<repo>/library` is library, however it was spelled — `./library`,
`a/../library`, an absolute path, a different case on a case-insensitive
filesystem. The literal `/library/` test is kept as a net for paths that resolve
outside this repository (another checkout's library, a symlinked mount).

Cross-platform Python replacement for the original .sh.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# <repo>/.claude/hooks/pre-write-guard.py -> <repo>
REPO_ROOT = Path(__file__).resolve().parents[2]
LIBRARY_ROOT = REPO_ROOT / "library"


def block(reason: str) -> None:
    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(payload), file=sys.stderr)
    sys.exit(2)


def _case_insensitive_fs(root: Path) -> bool:
    """Ask the filesystem instead of assuming from the platform name.

    Windows is the case the review hit, but a macOS APFS volume and a mounted
    share behave the same way and a Linux checkout must stay case-sensitive."""
    if os.name == "nt":
        return True
    try:
        swapped = Path(str(root).swapcase())
        return root.exists() and swapped.exists() and os.path.samefile(root, swapped)
    except OSError:
        return False


def targets_library(file_path: str) -> bool:
    """True when the write lands inside library/, however the path was spelled."""
    normalised = file_path.replace("\\", "/")
    try:
        target = Path(os.path.abspath(os.path.normpath(file_path)))
    except (OSError, ValueError):
        target = None

    if target is not None:
        lib = LIBRARY_ROOT
        candidates = [str(target)]
        try:
            candidates.append(str(target.resolve()))  # follow symlinks too
        except OSError:
            pass
        for cand in candidates:
            prefix = str(lib) + os.sep
            if _case_insensitive_fs(lib):
                if (cand + os.sep).lower().startswith(prefix.lower()):
                    return True
            elif (cand + os.sep).startswith(prefix):
                return True

    # Net for paths that resolve outside this repository.
    lowered = normalised.lower() if _case_insensitive_fs(LIBRARY_ROOT) else normalised
    return "/library/" in lowered or lowered.startswith("library/")


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

    file_path = (tool.get("tool_input") or {}).get("file_path") or ""
    if not file_path:
        return 0

    if not targets_library(file_path):
        return 0

    # Fail closed: anything other than an explicit "log" enforces.
    mode = os.environ.get("AISA_GUARD_MODE", "enforce").strip().lower()
    if mode != "log":
        block(
            "library/ is read-only at runtime (rule: .claude/rules/library-readonly.md). "
            "Administrative edits go out-of-band via git, or set AISA_GUARD_MODE=log "
            f"temporarily: {file_path}"
        )
    print(
        f"[pre-write-guard] WARN: write to library/ — would be denied in enforce mode: {file_path}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
