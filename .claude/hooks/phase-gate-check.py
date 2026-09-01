"""phase-gate-check.py — log-only PostToolUse stub.

Fires after a phase-transition skill ran (aisa-frame, aisa-options, aisa-decide).
MVP behaviour is log-only; v0.2.0 will validate _state.json + SU counts against
phases.md exit criteria.
"""

from __future__ import annotations

import json
import sys

TRANSITION_SKILLS = {"aisa-frame", "aisa-options", "aisa-decide"}


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

    skill = (tool.get("tool_input") or {}).get("skill") or ""
    if skill in TRANSITION_SKILLS:
        print(
            f"[phase-gate-check] {skill} ran — soft gate logged. "
            f"v0.2.0 will validate state + SU counts against exit criteria.",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
