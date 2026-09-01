"""pre-lens-order-check.py — PreToolUse guard: enforces sequential lens order in Discovery.

Blocks invocation of lens-N if lens-(N-1) has not written output for the round
currently in progress. The in-progress round is computed as
_state.json.round + 1 (the next round to run).

When more than one engagement is in `phase: discovery`, the active one is the
most recently touched (see find_discovery_engagement) — stale fixtures parked
in discovery no longer shadow the live engagement.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

LENS_ORDER = ["business", "operations", "user", "data", "governance", "financial"]


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


def _activity_mtime(eng: Path) -> float:
    """Most recent mtime across the files a round writes.

    Tracks "the engagement currently being worked on" better than creation
    time: running a lens rewrites the Shared Understanding and a lens-outputs
    file, so the active engagement bubbles to the top during a round.
    """
    candidates = [eng / "_state.json", eng / "shared-understanding.md"]
    lens_out = eng / "lens-outputs"
    if lens_out.is_dir():
        candidates.extend(lens_out.glob("*.md"))
    mtimes = []
    for p in candidates:
        try:
            mtimes.append(p.stat().st_mtime)
        except OSError:
            continue
    return max(mtimes) if mtimes else 0.0


def find_discovery_engagement(base: Path) -> Path | None:
    """Resolve the active Discovery engagement.

    The lens-order rule targets the engagement the current /round operates on,
    but the Skill call carries no engagement id. When several engagements sit in
    ``phase: discovery`` (e.g. stale fixtures alongside a live one), pick the one
    most recently touched — its SU / lens-outputs were just written by the round
    in progress. With a single discovery engagement this is identical to the
    original "first match" behaviour.
    """
    if not base.is_dir():
        return None
    discovery = []
    for child in base.iterdir():
        state_file = child / "_state.json"
        if not state_file.is_file():
            continue
        try:
            state = json.loads(state_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if state.get("phase") == "discovery":
            discovery.append(child)
    if not discovery:
        return None
    if len(discovery) == 1:
        return discovery[0]
    return max(discovery, key=_activity_mtime)


def main() -> int:
    raw = sys.stdin.read()
    # Tolerate stray leading bytes (UTF-8 BOM, mis-decoded BOM bytes, whitespace).
    for i, ch in enumerate(raw):
        if ch in "{[":
            raw = raw[i:]
            break
    try:
        tool = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        return 0

    if tool.get("tool_name") != "Skill":
        return 0

    skill = (tool.get("tool_input") or {}).get("skill") or ""
    match = re.match(r"^lens-(.+)$", skill)
    if not match:
        return 0

    lens_name = match.group(1)
    if lens_name not in LENS_ORDER:
        return 0

    idx = LENS_ORDER.index(lens_name)
    if idx == 0:
        return 0  # business is always allowed

    base = Path(os.environ.get("AISA_ENGAGEMENTS_ROOT") or "projects")
    eng = find_discovery_engagement(base)
    if eng is None:
        return 0  # no active Discovery engagement → nothing to enforce

    try:
        state = json.loads((eng / "_state.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0

    last_round = state.get("round") or "R-00"
    m = re.search(r"(\d+)", last_round)
    if not m:
        return 0
    in_progress_round = f"R-{int(m.group(1)) + 1:02d}"

    for prev in LENS_ORDER[:idx]:
        output_file = eng / "lens-outputs" / f"{prev}.md"
        if not output_file.is_file():
            block(
                f"Cannot run lens-{lens_name}: lens-{prev} has not run yet. "
                f"Invoke 'Skill: lens-{prev}' first (round {in_progress_round})."
            )
        content = output_file.read_text(encoding="utf-8", errors="replace")
        if in_progress_round not in content:
            block(
                f"Cannot run lens-{lens_name}: lens-{prev} has not written output for round "
                f"{in_progress_round} yet. Invoke 'Skill: lens-{prev}' first."
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
