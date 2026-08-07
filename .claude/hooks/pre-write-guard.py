"""pre-write-guard.py — PreToolUse guard for Write/Edit.

Blocks writes to library/* when AISA_GUARD_MODE=enforce; otherwise logs a
warning. Cross-platform Python replacement for the original .sh.
"""

from __future__ import annotations

import json
import os
import sys


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

    normalised = file_path.replace("\\", "/")
    in_library = "/library/" in normalised or normalised.startswith("library/")
    if not in_library:
        return 0

    mode = os.environ.get("AISA_GUARD_MODE", "log")
    if mode == "enforce":
        block("library/ is read-only at runtime")
    else:
        print(
            f"[pre-write-guard] WARN: write to library/ — would be denied in enforce mode: {file_path}",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
