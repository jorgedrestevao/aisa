"""synthesis-validate.py — log-only PostToolUse stub.

Fires after any Write to <engagement>/_synthesis/*.md. v0.2.0 will validate
paragraph count, SU citations, and vendor-neutrality per topic pack.
"""

from __future__ import annotations

import json
import re
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
    if re.search(r"_synthesis[\\/].+\.md$", file_path.replace("\\", "/")):
        print(
            f"[synthesis-validate] Topic pack written: {file_path} — "
            f"v0.2.0 will validate paragraph count + SU citations + vendor-neutrality.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
