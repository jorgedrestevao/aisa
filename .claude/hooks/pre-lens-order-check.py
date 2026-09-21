"""pre-lens-order-check.py — PreToolUse guard: the habitual lens order in a FULL Discovery round.

Blocks invocation of lens-N if lens-(N-1) has not written output for the round
currently in progress — but only inside a full `/round`. A lens run in
isolation (`/round <lens>`) is never policed: any lens may run alone, in any
order.

The isolation signal is DETERMINISTIC, not prose. `aisa-round` step 3c persists,
in the same atomic write as `round_in_progress`:

    "round_lenses": {"ronda": "R-03", "modo": "single", "lentes": ["data"]}

The guard stands aside when that record names the round in progress, says
`single`, and lists the lens being invoked. Scoping it to the round AND the lens
is what makes staleness harmless: a leftover from another round or another lens
matches nothing and the order is policed as usual. A free-text ``round mode:
single`` in the invocation is accepted as a secondary signal, for the case where
the state write landed in a different engagement copy — but the state is the
authority, because a marker the model must remember to type is exactly what
failed in operation (2026-09-09, `pricing-bunkers` R-03).

Fail-closed: no recognisable signal → policed as a full round.

"Has written output" means a section HEADER for the round in
`lens-outputs/<lens>.md` (`## R-NN …`), never a substring of the body — the
rule lives once, in `library/kernel/tools/dashboard.py::lens_wrote_round`,
imported here; a local copy of the same regex is the fallback when the motor
cannot be imported.

The in-progress round is read from `_state.json.round_in_progress` when it is
present and ahead of `_state.json.round` (the last COMPLETED round); otherwise it
falls back to `round + 1`, the round the next `/round` will open. Without this
distinction a single-lens `/round business` that closed R-01 made the following
`/round operations` look for output of R-02 and dead-end (P-R6 of the 2026-09-08
adversarial review). A `round_in_progress` that is not ahead of `round` is stale
(a phase transition, a hand edit) and is ignored rather than trusted.

The engagement is taken from the lens invocation itself — `aisa-round` step 4b
carries ``engagement root `<path>``` on its first line. Only when that is absent
does the guard fall back to "the most recently touched engagement in discovery"
(see find_discovery_engagement), which picks the wrong copy when two engagements
run a round at the same time.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

LENS_ORDER = ["business", "operations", "user", "data", "governance", "financial"]
SINGLE_MODE_RE = re.compile(r"round mode\s*[:=]\s*`?single`?", re.IGNORECASE)
TOOL_REL = Path("library") / "kernel" / "tools" / "dashboard.py"


def _local_lens_wrote_round(path: Path, round_id: str) -> bool:
    """Fallback copy of dashboard.py::lens_wrote_round (header match, not substring)."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return False
    pat = re.compile(r"^##\s+" + re.escape(round_id) + r"(?![\w-])", re.MULTILINE)
    return bool(pat.search(text))


def lens_wrote_round(path: Path, round_id: str) -> bool:
    tool = Path(__file__).resolve().parents[2] / TOOL_REL
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("aisa_dashboard", tool)
        mod = importlib.util.module_from_spec(spec)  # type: ignore[arg-type]
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return bool(mod.lens_wrote_round(path, round_id))
    except Exception:
        return _local_lens_wrote_round(path, round_id)


def single_by_state(state: dict, round_id: str, lens_name: str) -> bool:
    """`_state.json.round_lenses` authorises this lens to run alone in this round.

    Requires all three to line up — round, mode, lens — so a record left behind
    by another round or another lens authorises nothing."""
    record = state.get("round_lenses")
    if not isinstance(record, dict):
        return False
    if (record.get("ronda") or "").strip() != round_id:
        return False
    if (record.get("modo") or "").strip().lower() != "single":
        return False
    lenses = record.get("lentes")
    if not isinstance(lenses, list):
        return False
    return lens_name in [str(x).strip().lower() for x in lenses]


def single_by_marker(tool_input: dict) -> bool:
    """Secondary signal: ``round mode: single`` in the invocation text."""
    blob = json.dumps(tool_input, ensure_ascii=False) if tool_input else ""
    return bool(SINGLE_MODE_RE.search(blob))


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


def engagement_from_invocation(tool_input: dict, base: Path) -> Path | None:
    """The engagement the lens was invoked for, read from the invocation text.

    `aisa-round` step 4b opens the round context with ``engagement root `<path>```.
    Two `/round` calls on two copies at the same time make "most recently touched"
    a coin flip, so the declared root wins whenever it is present and real. A root
    that carries no `_state.json` is not an engagement — fall back rather than
    block on it.
    """
    blob = json.dumps(tool_input, ensure_ascii=False) if tool_input else ""
    match = re.search(r"engagement root[^`\w]*`([^`]+)`", blob)
    if not match:
        return None
    raw = match.group(1).strip().replace("\\\\", "\\")
    candidate = Path(raw)
    for path in (candidate, base / candidate.name):
        try:
            if (path / "_state.json").is_file():
                return path
        except OSError:
            continue
    return None


def in_progress_round(state: dict) -> str | None:
    """The round the lenses are stamping right now.

    `round` is the last COMPLETED round; `round_in_progress` is the one an open
    `/round` is filling. Prefer the latter when it is genuinely ahead — equal or
    behind means a leftover from a closed round.
    """
    last = re.search(r"(\d+)", state.get("round") or "R-00")
    if not last:
        return None
    last_n = int(last.group(1))
    open_round = (state.get("round_in_progress") or "").strip()
    if open_round:
        m = re.search(r"(\d+)", open_round)
        if m and int(m.group(1)) > last_n:
            return f"R-{int(m.group(1)):02d}"
    return f"R-{last_n + 1:02d}"


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

    tool_input = tool.get("tool_input") or {}
    skill = tool_input.get("skill") or ""
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
    eng = engagement_from_invocation(tool_input, base) or find_discovery_engagement(base)
    if eng is None:
        return 0  # no active Discovery engagement → nothing to enforce

    try:
        state = json.loads((eng / "_state.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return 0

    if state.get("phase") != "discovery":
        return 0  # the order rule is Discovery's; council phases run in parallel

    in_progress_round_id = in_progress_round(state)
    if in_progress_round_id is None:
        return 0

    # `/round <lens>`: any lens, alone, in any order (phases.md -> Rounds).
    if single_by_state(state, in_progress_round_id, lens_name) or single_by_marker(tool_input):
        return 0

    for prev in LENS_ORDER[:idx]:
        output_file = eng / "lens-outputs" / f"{prev}.md"
        if not output_file.is_file():
            block(
                f"Cannot run lens-{lens_name}: lens-{prev} has not run yet. "
                f"Invoke 'Skill: lens-{prev}' first (round {in_progress_round_id})."
            )
        if not lens_wrote_round(output_file, in_progress_round_id):
            block(
                f"Cannot run lens-{lens_name}: lens-{prev} has not written output for round "
                f"{in_progress_round_id} yet. Invoke 'Skill: lens-{prev}' first."
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
