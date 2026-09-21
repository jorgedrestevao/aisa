---
name: aisa-decide
description: Interactive Decision phase. User picks an option from options.md, gives justification + alternatives + accepted risks + revision conditions; the skill writes D-NNN to decisions.md and auto-invokes aisa-synthesize to produce the 5 topic packs in _synthesis/. Flips _state.json to phase=decision/round=D-01.
---

# aisa-decide

## Usage

`/decide [--option <O-NNN>] [--consult] [--override "<reason>"]`

- No `--option`: the skill reads `options.md` and asks the user to choose interactively.
- `--option <O-NNN>`: pre-select an option from `options.md`.
- `--consult`: before finalizing, launch ONE `solution-architect` Task subagent to review the chosen option (constraints re-check, watch-list, newly visible risks). Advisory — the user still decides.
- `--override "<reason>"`: bypass soft gates (e.g., options.md missing); the reason is logged.

## Phase model

- **From**: `phase: options`.
- **To**: `phase: decision`, `round: D-01`.
- **Mode**: interactive (user-driven), with automatic chained `aisa-synthesize` at the end. This is deliberate: the decision is the one point in the engagement where the *user* must say a sentence — no council runs here by default. `--consult` adds a single advisory solution-architect review; see `library/kernel/phases.md` (Phase 4).

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/council-log.md`.
- `<engagement>/frame.md`, `<engagement>/options.md`.
- `<engagement>/premortem.md` (if present — tripwire candidates and requirements for the D-NNN block).
- `<engagement>/lens-outputs/*.md` (incl. all chairman-synthesis logs).

## Outputs (written)

- `<engagement>/_state.json` (atomic, this skill).
- A new `D-NNN` block appended to `<engagement>/decisions.md` (this skill).
- `<engagement>/_synthesis/{business-story,as-is,architecture-story,risks-and-assumptions,financial-story}.md` (chained `aisa-synthesize`).
- `<engagement>/council-log.md` summary lines.

## Execution steps

### 1. Pre-flight

1. Resolve the engagement root and read `_state.json`. If `phase != options` AND `phase != decision` → stop with: "/decide transitions Options → Decision; current phase is `<phase>`. Use /options first." If `phase == decision`, treat as a re-decision (a new D-NNN, the next number).
2. **Read the gate verdict** in `<engagement>/gate-log.md` (id `G-options-decision-...`, written by `phase-gate-check.py` before this skill loaded): repeat it to the user, with its declared coverage, and never re-state a `n/a` criterion as OK.
2b. Verify `<engagement>/options.md` exists. If not → stop and ask the user to run `/options` first, or supply `--override "..."`.
3. **Pre-mortem check (soft)**: if `<engagement>/premortem.md` does not exist, or is older than the latest Options-round artefact (`options.md` / newest `_simulation/*`), suggest `/premortem` first — its mitigations feed the accepted risks and revision conditions below. Free override: if the user says "proceed", proceed (no `--override` needed); note the skip in the D-NNN block's justification context.
4. Parse `options.md` — its decision table is the option list — and read
   `lens-outputs/chairman-synthesis-O-<NN>.md` for any field the artefact omitted (it is the long
   form the artefact projects; an omitted field there means *evaluated and empty*).

### 2. Interactive capture

If `--option` was not supplied, present the parsed option list:

```
Options on the table (from options.md):

  O-001 — <name>   (<option class> · <technology: the form in products, or "sem tecnologia"> · effort <…> · reversibility <…>)
  O-002 — …
  …

Pick one (e.g., "O-002") or type "more rounds" to return to /options.
```

Once the user picks an option `<O-NNN>`, ask in sequence (one question at a time; do not invent answers):

1. **Justification** — "Why this option, anchored on what evidence in the SU? Cite ids (e.g., C-007, A-005, X-001).":
2. **Alternatives considered** — "Which other options were on the table, and why not each (one line per O-NNN)?"
3. **Accepted assumptions** — "The recommendation rests on these assumptions: <list them from the round's `Recommendation` section, `Assumed` rows cited by the chosen option, one line each>. Which do you accept as the basis of the decision, and which do you want tested first?" Present the list; do not ask an open question with nothing in it. An assumption the owner does **not** accept becomes either a proof obligation or a revision condition below — never a silently carried premise.
4. **Accepted risks** — "Which open R-NNN risks are you accepting with this choice? Add any new ones you accept now."
5. **Revision conditions** — "What measurable triggers would force a revisit of this decision? (e.g., 'monthly volume > 200', 'compliance review fails')"
6. **Sponsor confirmation** — "Has the sponsor confirmed this choice? (yes / pending / no)"

If a sponsor confirmation is `no` → warn the user but allow `--override "..."` to proceed; record the override in the D-NNN block.

### 2b. Optional consult (`--consult`)

If `--consult` was passed (or the user asks for a technical review mid-flow), launch ONE Task subagent: `subagent_type: solution-architect`, prompt = review the chosen `<O-NNN>` against the SU, the pack's `decision-tree.md` and `domain-knowledge/` — return newly visible risks, constraint re-checks, and revision triggers per its output schema. Present the review to the user before step 3. Any new risks the user accepts become `R-NNN` rows in step 4. The review is advisory: it never changes the choice by itself.

### 3. Flip state to Decision (atomic)

1. Update `_state.json`: `phase = decision`, `round = D-<NN>` (D-01 for the first decision in the engagement; if a prior D-NN exists in `_state.json`, increment).
2. Update SU header `Fase actual: Decision`.

### 4. Append the decision to decisions.md

```markdown

## D-<NNN> — <decision title; default "Adopt <O-NNN> — <option name>">

- **The aisa recommended**: <O-NNN — name, copied verbatim from the round's `Recommendation` section, or `no recommendation — <the reason that round gave>`>
- **Chosen option**: <O-NNN — name>
- **Recommendation followed?**: <yes | no — <why the owner chose otherwise>>. Two distinct facts kept as two fields: the recommendation is the aisa's reasoning, the choice is the owner's authority. Neither is evidence for the other, and a divergence is a legitimate outcome, not a defect to reconcile.
- **Rule change decided**: <— | the option carried the verdict *viable if the rule is changed*: which rule (with id), whether the owner chose to pursue changing it, who can change it, and the status the decision leaves it in (not requested · requested · refused). A rule the owner declines to change turns the option's condition into a `Risky` row, not a deletion.>
- **Selected solution / composition**: <the decided option class and what it consists of, in PLAIN LANGUAGE — e.g. "a platform-containing application for the intake scope", "extend the incumbent system", "custom development", "cloud-native assembly", "buy a packaged product", "process redesign", "do nothing". Serialization of an already-decided fact; no architecture verdict.>
- **(Scope, outcome) pairs — UNCOLLAPSED**: one line per emitted pair, each carrying the outcome sentence VERBATIM as `options.md` emitted it. Never merge two scopes into one line; never re-word or re-derive an outcome. Preserve every marker the pair carries (e.g. `INCUMBENT FIT UNEVALUATED`, documented sufficiency, "this platform is not excluded", the graduation trigger).
  - <scope> — <emitted outcome sentence, verbatim>
- **Conditions**: <the technical conditions the emitted outcome attached, each as *condition — owner as a ROLE — funded? — by when*; `not named` where the source did not name one, and never a person: a condition owed by a role is complete without one>
- **Proof obligations**: <carried from the Options proof requirement, each as *claim — level (V1–V4) — method — owner — funded?*; never re-derived here>
- **Preconditions**: <what must be true before work starts>
- **Justification**: <user-supplied paragraph; quote the cited SU ids inline>
- **Alternatives considered**:
  - <O-NNN> — <one-line "why not">
  - …
- **Accepted assumptions**: <the assumptions the decision rests on, each as *assumption — its `A-NNN`/`C-NNN` id where it has one — accepted | to be tested*. Carried from the round's `Recommendation` section (the assumptions it declared) plus the `Assumed` rows the chosen option cites; never re-derived here and never widened. An assumption marked *to be tested* appears below as a proof obligation or a revision condition, and this field says which. Empty is a legitimate value only where the round declared none — `—` with that stated, never a blank.>
- **Accepted risks**: <list pointing to R-NNN ids; add new R-NNN rows in the SU if any are new>
- **Revision conditions / Tripwires (estruturados)**:
  - TW-1: <condição mensurável, com fonte no SU> → se disparar, comparar com `_simulation/counterfactuals/<O-NNN>.md`
  - TW-2: …
  (Fontes: as respostas do utilizador + os TRIPWIRE candidatos do `premortem.md`, se existir — propõe-os explicitamente.)
- **Sponsor confirmation**: <yes | pending | no (with --override reason)>
- **Supersedes**: <D-00x — reaberta em O-NN por TW-n (_simulation/<revisit file>) | D-00x — reaberta em O-NN por decisão do dono: "<justificação>" | —>
- **Decided in round**: D-<NN>
- **Timestamp**: <ISO-8601>
```

**`Supersedes` is filled only when this decision replaces an earlier one** (a reopening —
`library/kernel/phases.md` → *Transition rules*). Detecting it needs no new state: the motor
(`--json`) reports `phase = options` while `status.tripwires.source_decision` still names a
solution decision with no `superseded_by` — that combination IS the reopening, and it survives
a session that died mid-way. The superseded block is **never edited**: it keeps its tripwires,
its alternatives and its counterfactual; the motor derives the reverse pointer and stops
treating it as the decision in force.

**Counters come from history, not from `_state.json`**: `D-<NN>` is the highest `Decided in
round` in `decisions.md` plus one, and the block id is the highest `D-NNN` plus one (frame,
solution and blueprint approvals share the counter).

If the user introduced **new** accepted risks not yet in the SU, add them as `R-NNN` rows (lens = the dominant lens, or `chair` for cross-lens) and reference them from the D-NNN block.

### 4b. Append the decision row to the Shared Understanding

The SU stays complete (understanding + commitments). Append ONE row to `## Confirmed`:

```
| D-NNN | <dominant lens, or `chair`> | <decision title>; ver decisions.md#D-NNN | decisions.md#D-NNN | <current round> |
```

Update the SU header `Última actualização`. (Per `docs/ARCHITECTURE.md §4.5` — the decision is citable from the SU like any other id.)

### 4c. Freeze the counterfactuals (multiverse)

For every option NOT chosen that has a projection in the latest `_simulation/options-comparison_v<NN>.md`, write `_simulation/counterfactuals/<O-NNN>.md` — **never overwriting one that already exists**: after a reopening the previously chosen option becomes a rejected branch, and its counterfactual goes to `_simulation/counterfactuals/<O-NNN>@D-00y.md` (`D-00y` = the decision that rejected it), so the frozen branch of the first decision stays frozen. Content: the frozen projection (shape, effort band, risks, constraint verdicts) + a final section **"Condições em que este ramo ganharia"** derived from the decision-tree verdicts and the VOI (e.g., "se o volume confirmado cair para <20/mês, o caso de eficiência de O-002 passa à frente"). Frozen = never edited afterwards; `/revisit` compares against them and writes NEW artefacts.

### 5. Auto-invoke aisa-synthesize

Immediately invoke the `aisa-synthesize` skill. Wait for it to return; it produces the 5 topic packs in `_synthesis/`. If any topic-pack synthesis fails → record the failure in `council-log.md` but do NOT roll back the decision (the synthesis can be retried manually).

### 5c. Story

Append one narrative episode to `<engagement>/story.md` (`## Episódio <N> — <data> — a decisão (e porquê)`): 4-8 frases na voz do sponsor, sem jargão de kernel, máx. 2 ids citados. Create the file with `# Story — <slug>` if missing (pre-v2.3 engagements).

### 6. Wrap-up output

Business language (`CLAUDE.md` → *Duas línguas*); kernel labels and ids only between parentheses:

```user-output
Escolha registada: <a alternativa escolhida, em palavras> (D-NN) — com as razões, as alternativas rejeitadas, os riscos aceites e as condições que obrigam a rever.
Resumos por tema: <N>/5 produzidos em `_synthesis/` <| falharam: <lista> — repete com `/synthesize`>.
A seguir: desenhar os ecrãs e iterar com o negócio até aprovar → `/blueprint`; depois os documentos finais → `/render --all`.
```

## What this skill serializes — and what it must never emit

This skill **serializes already-decided facts**. It performs no architecture reasoning, and its Step 5B
change was a bounded serialization cleanup only: stage execution, candidate evaluation, outcome logic,
comparator semantics, evidence semantics and class selection are **unchanged**.

**May serialize** (all already decided upstream): uncollapsed `(scope, outcome)` pairs · the selected
option / composition in plain language · conditions · proof obligations · accepted risks ·
preconditions · tripwires.

**Must NEVER emit** — these belong to `/blueprint`'s mechanical architecture-entry gate, which
initializes them from the frozen outcome and the frozen selected solution against the active pack's
architecture scope:

- `architecture.authorization` (`authorized` / `authorized-bounded` / `not-authorized`)
- `architectability_basis`
- experience mode or primary surface
- composition selection
- record authority
- architecture-template selection

The obsolete `Branch (if technology)` field is **removed**: it named a three-value decision-tree branch
whose own authority no longer defines it. Nothing here replaces it with another architecture verdict —
downstream reads the `(scope, outcome)` pairs and the selected solution instead.

## Notes

- The decision is the only point where the *user* (not the council) must say a sentence. Everything else has been council + chairman.
- **Append-only** on `decisions.md` and the SU — D-NNN ids monotonically increase across re-decisions.
- No council runs in Decision. `chairman-synthesis` is invoked by `aisa-frame` and `aisa-options` only; the decision block is written fresh by this skill from the user's answers (plus the optional `--consult` review).
