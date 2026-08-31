---
name: aisa-status
description: Show the current phase, round, Shared Understanding summary (counts per state), open critical gaps, and the suggested next action. With --check, validates the aisa install.
---

# aisa-status

## Usage

`/status [--check]`

- No argument: shows status for the current engagement.
- `--check`: validates the aisa install (paths, kernel, pack, hook); no engagement needed.

## Execution steps (no argument)

1. Resolve the engagement. If the engagement is unclear, scan the engagements root (`$AISA_ENGAGEMENTS_ROOT` or `projects/`) for folders containing `_state.json` and ask which one (or use the only one).
2. Read `_state.json` → engagement, pack, phase, round (the most recent completed round; `R-00` = no round has run yet).
3. Read `shared-understanding.md` and count rows in each section: Confirmed, Assumed, Unknown, Conflicted, Risky. Rows carrying a `resolved → <id>` marker count as **resolved**, not open — report them separately (e.g., "Unknown: 4 open (+6 resolved)").
4. Identify **Critical** Unknown and Conflicted rows (criticidade column).
5. Suggest the next action based on phase + gaps, e.g.:
   - Critical Unknown/Conflicted open → "Resolve N critical items with the sponsor before /frame."
   - Discovery exit criteria met → "Ready for /frame."
6. Output a readable summary:
   ```
   Engagement: <slug>   Pack: <pack>
   Phase: <phase>       Round: <round>

   Shared Understanding:
     Confirmed: N   Assumed: N   Unknown: N (C critical)   Conflicted: N (C critical)   Risky: N

   Open critical items:
     U-00x — <question> (lens)
     X-00x — <conflict> (lens)

   Next suggested action:
     → <suggestion>
   ```

## Execution steps (--check)

1. Verify `library/kernel/` has the 6 expected files (phases, states, orchestration, render-contract, blueprint-contract, glossary) + `synthesis-templates/` with 5 templates.
2. Verify at least one pack exists under `library/packs/` with a `pack.yaml`.
3. Verify the engagements root is resolvable: `$AISA_ENGAGEMENTS_ROOT` is set, or `projects/` exists and is writable.
4. Verify `.claude/hooks/pre-write-guard.sh` exists (and is executable on Unix).
5. Output green/red per check, e.g.:
   ```
   ✓ kernel: 5/5 files
   ✓ packs: pp (+ scaffolds)
   ✓ engagements root: projects/ (or $AISA_ENGAGEMENTS_ROOT)
   ✓ pre-write-guard hook present
   ✓ ready.
   ```
