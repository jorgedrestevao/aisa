---
name: aisa-simulate
description: Simulate the candidate options BEFORE /decide — for each option, project the concrete future (draft screen architecture, effort band, risk profile, constraint verdicts) and produce a side-by-side comparison plus the value-of-information list (which open Unknowns would flip the ranking). Advisory; never decides.
---

# aisa-simulate

## Usage

`/simulate [O-NNN ...]`

- No argument: simulate every option in `options.md`.
- `O-NNN ...`: simulate only the named subset.

Requires `phase ∈ {options, decision}` and `options.md` to exist. The sponsor stops choosing between paragraphs and starts choosing between concretized futures — at near-zero marginal cost, because projection reuses the deterministic layers (blueprint rules, estimation model, decision-tree verdicts).

## Inputs (read)

- `<engagement>/options.md`, `frame.md`, `shared-understanding.md`, `_state.json`, `lens-outputs/*.md`.
- Pack: `decision-tree.md` (verdicts per branch), `domain-knowledge/estimation-model.md`, `screen-consolidation-rules.md`, `delegation-matrix.md`.

## Execution steps — per option

1. **Shape**: for technology options, run `aisa-blueprint --option O-NNN` (draft mode) or reuse an existing draft for this option — yielding screen count, patterns, entities touched. For non-technology / do-nothing options: describe the intervention shape (process steps changed, roles affected) — no blueprint.
2. **Effort band**: apply the pack's `estimation-model.md` to the shape (screens × complexity, entities, flows, integrations); output a band (P50/P80), never a point. Every multiplier applied is named (e.g., "SAP integration ×1.4 per estimation-model §…").
3. **Risk profile**: SU `Risky` rows touching this option + the option's cons + the decision-tree constraint verdicts (pass / risky / blocker) for its branch.
4. **Dependencies on the unknown**: list the SU `Unknown` rows whose answer changes THIS option's viability, effort band, or constraint verdicts — with the direction of the swing ("if SAP latency > 2s, O-003's mobile case dies").

## Execution steps — after all options

5. **Comparison artefact**: write `<engagement>/_simulation/options-comparison_v<NN>.md` (versioned, append-only, mirrors `_render/`):
   - Side-by-side table: option · shape (screens/intervention) · effort band · licensing/run cost signal · top-3 risks · reversibility · constraint blockers.
   - One-pager per option: the projected future in 5-8 lines, every claim citing SU/option/tree ids.
   - **Value of information**: the Unknowns that are *decision-flipping* — resolving them changes the ranking or kills an option — ranked by swing size, each with `quem responde`. These are the answers worth chasing before `/decide`; Unknowns that flip nothing are explicitly listed as "não vale a pena esperar por".
6. Append one line to `council-log.md`. Output the comparison table inline + the VOI list + "Next: `/answer` the decision-flipping Unknowns, or proceed to `/decide`."

## Hard rules

1. **Advisory only.** The simulation never picks a winner; it sharpens the user's choice. No recommendation language beyond the factual verdicts.
2. **No invention**: every number traces to the estimation model, the decision tree, or an SU id; missing inputs surface as Unknowns (consistent with the tree's missing-inputs protocol).
3. **Draft blueprints stay drafts** (`draft: true`); the approved-blueprint flow only exists after `/decide`.
4. Versioned output; a re-run after new answers produces `v<NN+1>` — the comparison history shows how the picture changed as Unknowns resolved.
