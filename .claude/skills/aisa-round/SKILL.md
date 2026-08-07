---
name: aisa-round
description: Run a round of lenses in the current phase. In Discovery, runs the lenses sequentially (inline) in the fixed order, or a single named lens.
---

# aisa-round

## Usage

`/round [lens]`

- No argument: in Discovery, runs the lenses in the fixed order defined in `library/kernel/phases.md`: `business → operations → user → data → governance → financial`. In other phases → stop with: "/round is for Discovery; use /frame, /options, /decide for later phases."
- `[lens]`: a lens name (e.g., `business`) — runs only that lens.

## Execution steps

1. Read `_state.json` (resolve the engagement root as in `aisa-start`). Read `phase` and `round`.
2. If `phase != discovery` → stop with the message above.
3. **Determine the round to run**: increment `_state.json.round` by one (`R-00`→`R-01`, `R-01`→`R-02`, ...). The lenses stamp **this** round on their rows. `aisa-start` seeds `R-00` (no round run yet), so the first `/round` runs `R-01`.
3.5. **Capture freshness check**: for each supported file (`.xlsx`/`.xlsm`) in `inputs/`, compare its SHA-256 with `identity.sha256` in `_capture/<file>.extraction.json`. Missing or mismatched → invoke the `aisa-capture` skill for the stale/missing file(s) BEFORE any lens runs (the L1 script self-caches, so up-to-date files cost one hash check). Capture failure is soft: warn and let lenses fall back to raw reading.
4. For each lens to run (the full Discovery order, or just the named lens):
   a. If `.claude/skills/lens-<name>/SKILL.md` does not exist yet → skip it and note "lens `<name>` not yet implemented" (lenses data/governance/financial arrive in a later build phase).
   b. Otherwise invoke the lens skill (e.g., `Skill: lens-business`) in **inline mode** — it reads `context.json` + the accumulated `shared-understanding.md` + previous lenses' `lens-outputs/` from this round.
      > **MUST:** Call the `Skill` tool with `skill="lens-{name}"` for each lens. Never read `SKILL.md` files directly and run the analysis yourself — doing so bypasses the `pre-lens-order-check` hook that enforces sequential ordering.
   c. Confirm the lens wrote rows to the SU and a paragraph to `lens-outputs/<lens>.md`.
5. After all lenses (or the single lens) finish:
   a. Persist `_state.json.round` = the round just run (atomically, tmp → rename). It therefore always holds the most recent completed round = the engagement's current round.
   b. Update the SU header `Última actualização` timestamp.
   c. Append a round summary to `council-log.md`.
6. Output: "Round `R-NN` complete (lenses run: …). Run `/status` for the summary."

## Notes

- Each `/round` starts a NEW round; the counter only moves forward. Lenses append and never rewrite prior rows, so re-running is safe — it adds the next round rather than duplicating.
- The fixed inline order exists for predictability and debuggability (see `library/kernel/orchestration.md`).
