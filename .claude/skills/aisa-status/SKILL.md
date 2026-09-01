---
name: aisa-status
description: Show the current phase, round, Shared Understanding summary (counts per state), epistemic health (expired Confirmed/Assumed rows to revalidate, with the re-question formulated), open critical gaps, and the suggested next action. With --check, validates the aisa install.
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
5. **Compute epistemic health** (per `library/kernel/states.md` → *Epistemic half-lives*):
   a. For every OPEN Confirmed/Assumed row (rows with a `resolved →` marker are out), read `verificado_em` + `validade`. Absent columns (pre-v2.2 SUs) ⇒ `verificado_em` = the row's round date, `validade` = `organizacional` — never migrate the SU.
   b. Half-lives: kernel decay table, overridden by the pack's `epistemics.half_lives_override` (`pack.yaml`) when present.
   c. A row is **expirada** when `verificado_em + meia-vida(validade) < hoje`. Health = `vivas / (vivas + expiradas)` as a percentage.
   d. Update the SU header line `> Saúde epistémica: NN% (X expiradas) — <date>` (create the line if the SU predates it).
6. **Build the meeting agenda** from OPEN Unknowns (`custo`/`swing` columns; absent ⇒ `email`/`dimensionante`):
   a. **Agenda da próxima reunião**: `custo = reuniao`, ordered `decisivo` → `dimensionante`, each with its swing phrase.
   b. **Por outro canal**: `custo ∈ {email, documento, spike}`, same ordering (spikes flagged with their cost in days).
   c. **Não gastes tempo com**: every `cosmético`, listed explicitly — protecting the sponsor's hour is the point.
7. **Check tripwires** (engagements with a final D-NNN): read the `Tripwires` list from the latest decision block; for each TW, scan the OPEN SU rows for evidence that the condition fired (a row satisfying the metric/condition). Fired → highlighted alert with the associated counterfactual + suggest `/revisit TW-n`.
8. Suggest the next action based on phase + gaps, e.g.:
   - Critical Unknown/Conflicted open → "Resolve N critical items with the sponsor before /frame."
   - Discovery exit criteria met → "Ready for /frame."
   - Expired rows underpin the current phase's artefact → "Revalidate before deciding."
9. Output a readable summary:
   ```
   Engagement: <slug>   Pack: <pack>
   Phase: <phase>       Round: <round>

   Shared Understanding:
     Confirmed: N   Assumed: N   Unknown: N (C critical)   Conflicted: N (C critical)   Risky: N
     Saúde epistémica: NN% (X expiradas)

   A revalidar (top-5, mais vencidas primeiro):
     C-00x (<validade>, verificado <data>) — "Ainda é verdade que <claim>? Verificado pela última vez em <data>."
       → /answer --revalidate C-00x   (ou /answer C-00x "..." se o facto mudou)
     …

   Agenda da próxima reunião (custo=reuniao, por swing):
     U-00x [decisivo: <o que muda>] — <pergunta> → quem: <role>
   Por outro canal: U-00y (email), U-00z (spike: <dias>)
   Não gastes tempo com: U-00w (cosmético)

   Open critical items:
     U-00x — <question> (lens)
     X-00x — <conflict> (lens)

   Tripwires: <OK | TW-n DISPAROU → evidência <id>; counterfactual O-NNN → /revisit TW-n>

   Next suggested action:
     → <suggestion>
   ```
   Omit the "A revalidar" block when nothing is expired (health 100%). Sort by how far past expiry; list at most 5 and say how many more there are.

## Execution steps (--check)

1. Verify `library/kernel/` has the 6 expected files (phases, states, orchestration, render-contract, blueprint-contract, glossary) + `synthesis-templates/` with 5 templates.
2. Verify at least one pack exists under `library/packs/` with a `pack.yaml`.
3. Verify the engagements root is resolvable: `$AISA_ENGAGEMENTS_ROOT` is set, or `projects/` exists and is writable.
4. Verify `.claude/hooks/pre-write-guard.py` exists and that `python`/`python3` is on PATH (all hooks are Python 3).
5. Output green/red per check, e.g.:
   ```
   ✓ kernel: 5/5 files
   ✓ packs: pp (+ scaffolds)
   ✓ engagements root: projects/ (or $AISA_ENGAGEMENTS_ROOT)
   ✓ pre-write-guard hook present (Python)
   ✓ ready.
   ```
