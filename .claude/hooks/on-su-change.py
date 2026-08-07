"""on-su-change.py — log-only PostToolUse stub.

Fires after any Write/Edit to <engagement>/shared-understanding.md.
v0.2.0 will trigger a background contradiction scan.
"""

from __future__ import annotations

import json
import sys


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
    if file_path.replace("\\", "/").endswith("shared-understanding.md"):
        print(
            f"[on-su-change] SU written: {file_path} — "
            f"v0.2.0 will scan for contradictions in background.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
