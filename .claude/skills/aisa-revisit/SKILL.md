---
name: aisa-revisit
description: Compare the present against a frozen counterfactual when a decision tripwire fires (or on demand) — what the rejected branch would look like now, what switching would cost, and a recommendation (keep / adapt / reopen Options). Advisory only; it never changes the decision — reopening goes through the normal /options round.
---

# aisa-revisit

## Usage

`/revisit <TW-n | O-NNN>` — requires a final decision (`D-NNN` in `decisions.md`) and frozen counterfactuals in `_simulation/counterfactuals/`.

- `TW-n`: a tripwire from the latest decision block (typically flagged by `/status`).
- `O-NNN`: revisit a rejected option directly (curiosity or an unstructured trigger).

## Inputs (read)

- `decisions.md` (the D-NNN with its tripwires), `shared-understanding.md` (current, with validades), `_simulation/counterfactuals/<O-NNN>.md` (frozen), `_simulation/options-comparison_v*.md` (context), `story.md`.

## Execution

1. Resolve the target: a `TW-n` maps to its associated counterfactual (per the tripwire line); an `O-NNN` maps directly. Missing counterfactual → stop and say which options were frozen.
2. Answer **four questions**, each anchored to ids:
   a. **Disparou mesmo?** — the evidence in the SU that satisfies (or not) the tripwire condition; if it did not actually fire, say so and stop (false alarm is a legitimate outcome).
   b. **Como estaria o ramo rejeitado HOJE?** — update the frozen projection with what is now known (new Confirmed rows, resolved Unknowns, expired assumptions). The frozen file is NEVER edited; the update lives in this artefact.
   c. **Custo de mudar agora vs custo de ficar** — migração/retrabalho/moral vs o dano acumulado de manter o ramo atual.
   d. **Recomendação** — `MANTER` (o tripwire disparou mas o ramo atual continua superior — dizer porquê) / `ADAPTAR` (a decisão sobrevive com um ajuste concreto — dizer qual) / `REABRIR` (justifica nova ronda de Options).
3. Write `_simulation/revisit_<data>_<alvo>.md` with the four answers + the tripwire evidence. Append an episode to `story.md` ("um alarme tocou — fomos ver") + a line to `council-log.md`.
4. If `REABRIR`: suggest `/options` (a new O-NN round) — NEVER alter `decisions.md` or the SU yourself. If `ADAPTAR`: the adjustment enters the SU by the normal path (`/answer`, new rows), not by editing the decision.

## Hard rules

1. **Advisory absoluto.** Revising a decision is a human decision, through the same path as the original (`/options` → `/decide`).
2. **The frozen counterfactual is never edited** — comparisons write new artefacts.
3. Every claim in the four answers carries ids; a revisit without provenance is an opinion, not an analysis.
