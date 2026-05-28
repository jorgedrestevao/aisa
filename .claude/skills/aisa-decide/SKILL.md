---
name: aisa-decide
description: Interactive Decision phase. User picks an option from options.md, gives justification + alternatives + accepted risks + revision conditions; the skill writes D-NNN to decisions.md and auto-invokes aisa-synthesize to produce the 5 topic packs in _synthesis/. Flips _state.json to phase=decision/round=D-01.
---

# aisa-decide

## Usage

`/decide [--option <O-NNN>] [--override "<reason>"]`

- No `--option`: the skill reads `options.md` and asks the user to choose interactively.
- `--option <O-NNN>`: pre-select an option from `options.md`.
- `--override "<reason>"`: bypass soft gates (e.g., options.md missing); the reason is logged.

## Phase model

- **From**: `phase: options`.
- **To**: `phase: decision`, `round: D-01`.
- **Mode**: interactive (user-driven), with automatic chained `aisa-synthesize` at the end.

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/council-log.md`.
- `<engagement>/frame.md`, `<engagement>/options.md`.
- `<engagement>/lens-outputs/*.md` (incl. all chairman-synthesis logs).

## Outputs (written)

- `<engagement>/_state.json` (atomic, this skill).
- A new `D-NNN` block appended to `<engagement>/decisions.md` (this skill).
- `<engagement>/_synthesis/{business-story,as-is,architecture-story,risks-and-assumptions,financial-story}.md` (chained `aisa-synthesize`).
- `<engagement>/council-log.md` summary lines.

## Execution steps

### 1. Pre-flight

1. Resolve the engagement root and read `_state.json`. If `phase != options` AND `phase != decision` → stop with: "/decide transitions Options → Decision; current phase is `<phase>`. Use /options first." If `phase == decision`, treat as a re-decision (a new D-NNN, the next number).
2. Verify `<engagement>/options.md` exists. If not → stop and ask the user to run `/options` first, or supply `--override "..."`.
3. Parse `options.md` and list the available options.

### 2. Interactive capture

If `--option` was not supplied, present the parsed option list:

```
Options on the table (from options.md):

  O-001 — <name>   (<branch> · effort <…> · reversibility <…>)
  O-002 — …
  …

Pick one (e.g., "O-002") or type "more rounds" to return to /options.
```

Once the user picks an option `<O-NNN>`, ask in sequence (one question at a time; do not invent answers):

1. **Justification** — "Why this option, anchored on what evidence in the SU? Cite ids (e.g., C-007, A-005, X-001).":
2. **Alternatives considered** — "Which other options were on the table, and why not each (one line per O-NNN)?"
3. **Accepted risks** — "Which open R-NNN risks are you accepting with this choice? Add any new ones you accept now."
4. **Revision conditions** — "What measurable triggers would force a revisit of this decision? (e.g., 'monthly volume > 200', 'compliance review fails')"
5. **Sponsor confirmation** — "Has the sponsor confirmed this choice? (yes / pending / no)"

If a sponsor confirmation is `no` → warn the user but allow `--override "..."` to proceed; record the override in the D-NNN block.

### 3. Flip state to Decision (atomic)

1. Update `_state.json`: `phase = decision`, `round = D-<NN>` (D-01 for the first decision in the engagement; if a prior D-NN exists in `_state.json`, increment).
2. Update SU header `Fase actual: Decision`.

### 4. Append the decision to decisions.md

```markdown

## D-<NNN> — <decision title; default "Adopt <O-NNN> — <option name>">

- **Chosen option**: <O-NNN — name>
- **Branch (if technology)**: <decision-tree branch> or "non-technology" / "do-nothing"
- **Justification**: <user-supplied paragraph; quote the cited SU ids inline>
- **Alternatives considered**:
  - <O-NNN> — <one-line "why not">
  - …
- **Accepted risks**: <list pointing to R-NNN ids; add new R-NNN rows in the SU if any are new>
- **Revision conditions**:
  - <measurable trigger>
  - …
- **Sponsor confirmation**: <yes | pending | no (with --override reason)>
- **Decided in round**: D-<NN>
- **Timestamp**: <ISO-8601>
```

If the user introduced **new** accepted risks not yet in the SU, add them as `R-NNN` rows (lens = the dominant lens, or `chair` for cross-lens) and reference them from the D-NNN block.

### 5. Auto-invoke aisa-synthesize

Immediately invoke the `aisa-synthesize` skill. Wait for it to return; it produces the 5 topic packs in `_synthesis/`. If any topic-pack synthesis fails → record the failure in `council-log.md` but do NOT roll back the decision (the synthesis can be retried manually).

### 6. Wrap-up output

"Decision D-<NN> registered. Synthesis produced <N>/5 topic packs in `_synthesis/`. Next: `/render --all` to produce the 6 deliverables, or `/render <id>` for one."

If a topic pack failed:
"Decision D-<NN> registered. Synthesis produced <N>/5 topic packs in `_synthesis/`; FAILED: <list>. Run `/synthesize` to retry, then `/render --all`."

## Notes

- The decision is the only point where the *user* (not the council) must say a sentence. Everything else has been council + chairman.
- **Append-only** on `decisions.md` and the SU — D-NNN ids monotonically increase across re-decisions.
- The chairman drafted a `D-<NNN> (draft)` block at the end of Options (if it did). The `/decide` skill removes the `(draft)` marker and overwrites with the final D-NNN. If the draft is absent, the skill writes a fresh D-NNN block.
