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
  `options.md` is budgeted and omits fields the round evaluated as empty: the per-option long form and
  the concern coverage are in `lens-outputs/chairman-synthesis-O-<NN>.md`. Read that log for any field
  the artefact does not carry, and **never treat an omitted field as unevaluated** without checking it.
  A platform option's **form** (surface + store, in products) is part of its identity — carry it into
  the comparison table and into every projection, because two forms over the same store project
  differently.
- Pack: `decision-tree.md`, `domain-knowledge/craft/estimation-model.md`, `domain-knowledge/craft/screen-consolidation-rules.md`, `domain-knowledge/data/query-and-delegation.md`.
  - `craft/estimation-model.md` is a **platform-side** effort model with no comparator-side basis. It is available here to project a platform candidate, and its output **must carry that asymmetry statement**. It is barred from comparative economics between option classes.

## Execution steps — per option

1. **Shape**: for technology options, run `aisa-blueprint --option O-NNN` (draft mode) or reuse an existing draft for this option — yielding screen count, patterns, entities touched. For non-technology / do-nothing options: describe the intervention shape (process steps changed, roles affected) — no blueprint.
2. **Planning interval**: apply the pack's `craft/estimation-model.md` to the shape (screens × complexity, entities, flows, integrations); output a **planning interval (min–max)** over the method's own bands, never a point. **This interval is source (a) of the Options order-of-magnitude method** (`chairman-synthesis`, which owns the method and the markers): an option whose band came from here carries the marker `SIMULATED`, and a later Options round may read it back rather than re-deriving one. **Not a quantile** — the method carries per-component rates, complexity factors and a buffer, and carries no distribution: `P50`, `P80` or any other quantile may not be claimed here until a probabilistic method is documented and calibrated in the pack. Every factor applied is cited to the section of `craft/estimation-model.md` that states it; a factor with no such section is not applied. The interval carries the platform-side-only asymmetry statement.
3. **Risk profile**: SU `Risky` rows touching this option + the option's recorded material trade-offs + the findings the Options round already recorded against it, **in the vocabulary that round used** (`decision-tree.md` §3: disqualifier at its scope · precondition · trade-off · risk · uncertainty). Read them; do not re-classify them, and do not run a second per-constraint verdict ladder alongside the model.
4. **Dependencies on the unknown**: list the SU `Unknown` rows whose answer changes THIS option's viability, effort band, or recorded findings — with the direction of the swing ("if SAP latency > 2s, O-003's mobile case dies").

## Execution steps — after all options

5. **Comparison artefact**: write `<engagement>/_simulation/options-comparison_v<NN>.md` (versioned, append-only, mirrors `_render/`):
   - Side-by-side table: option · shape (screens/intervention) · effort band · licensing/run cost signal · top-3 risks · reversibility · constraint blockers.
   - One-pager per option: the projected future in 5-8 lines, every claim citing SU/option/tree ids.
   - **Value of information**: the Unknowns that are *decision-flipping* — resolving them changes the ranking or kills an option — ranked by swing size, each with `quem responde` and `custo`. Start from the rows' own `swing` classes (kernel *Question economics*); when the simulation's evidence disagrees with a row's class (a `cosmético` that flips an option, a `decisivo` that flips nothing), CORRECT the row's `swing` (sanctioned metadata edit) and note the correction in the output. **Coverage rule (emenda F10 → P-1):** a correction **downwards** (`decisivo` → `dimensionante`, `dimensionante` → `cosmético`) is allowed **only when this simulation covered every option the question touches** — a partial `/simulate O-001 O-002` that saw the question flip nothing has not seen the options it did not simulate. With partial coverage, write the local impact in the output (`sem oscilação nas opções simuladas: <O-…>; classe mantida — cobertura parcial`) and **do not touch the SU**. A correction **upwards** may rest on one sufficient piece of evidence (one option flipped is enough to make a question decision-flipping) — but the evidence has to be **the flip itself**: name the option or the pattern that changes with each answer, and how. A question is `decisivo` because a candidate leaves the set, changes class, or changes its shape; it is never `decisivo` because the answer feels important. Organisational maturity, a missing name, an unconfirmed funding line and an absent policy move no option by themselves: where they change nothing in the comparison, the class stays and the output says so. If the flip cannot be named, the correction is not made. These are the answers worth chasing before `/decide`; Unknowns that flip nothing are explicitly listed as "não vale a pena esperar por".
6. Append one line to `council-log.md`. Output the comparison table inline, then (business language — `CLAUDE.md` → *Duas línguas*; kernel labels and ids only between parentheses):
   ```user-output
   Ensaio das alternativas — versão <NN>: a tabela acima compara ecrãs, intervalo de esforço, riscos e restrições (ficheiro `_simulation/options-comparison_v<NN>.md`). O esforço é só o lado da plataforma — não compara classes de alternativa entre si.
   Vale a pena responder antes de escolher (a resposta muda a ordem ou mata uma alternativa): <pergunta curta> (U-nnn) — quem responde · como se obtém a resposta …
   Não vale a pena esperar por: <pergunta curta> (U-nnn) …
   Classificações corrigidas pelo ensaio: <nenhuma | <pergunta curta> (U-nnn): <de → para>> …
   A seguir: responde às que mudam a ordem → `/answer <id> "…"`; ou escolhe → `/decide`.
   ```

## Hard rules

1. **Advisory only.** The simulation never picks a winner; it sharpens the user's choice. No recommendation language beyond the factual verdicts.
2. **No invention**: every number traces to the estimation model, the decision tree, or an SU id; missing inputs surface as Unknowns (consistent with the tree's missing-inputs protocol).
3. **Draft blueprints stay drafts** (`draft: true`); the approved-blueprint flow only exists after `/decide`.
4. Versioned output; a re-run after new answers produces `v<NN+1>` — the comparison history shows how the picture changed as Unknowns resolved.
5. **High-level only, and comparative only.** Before the decision every option is projected at the same high level — enough to compare, never a design. Detailed architecture and an implementation plan are produced for the **chosen** option alone, after `/decide`. Projecting one option deeper than its siblings is not extra rigour: it manufactures the preference it appears to find.
