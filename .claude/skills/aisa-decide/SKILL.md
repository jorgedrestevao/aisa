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
2. Verify `<engagement>/options.md` exists. If not → stop and ask the user to run `/options` first, or supply `--override "..."`.
3. **Pre-mortem check (soft)**: if `<engagement>/premortem.md` does not exist, or is older than the latest Options-round artefact (`options.md` / newest `_simulation/*`), suggest `/premortem` first — its mitigations feed the accepted risks and revision conditions below. Free override: if the user says "proceed", proceed (no `--override` needed); note the skip in the D-NNN block's justification context.
4. Parse `options.md` and list the available options.

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

### 2b. Optional consult (`--consult`)

If `--consult` was passed (or the user asks for a technical review mid-flow), launch ONE Task subagent: `subagent_type: solution-architect`, prompt = review the chosen `<O-NNN>` against the SU, the pack's `decision-tree.md` and `domain-knowledge/` — return newly visible risks, constraint re-checks, and revision triggers per its output schema. Present the review to the user before step 3. Any new risks the user accepts become `R-NNN` rows in step 4. The review is advisory: it never changes the choice by itself.

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

### 4b. Append the decision row to the Shared Understanding

The SU stays complete (understanding + commitments). Append ONE row to `## Confirmed`:

```
| D-NNN | <dominant lens, or `chair`> | <decision title>; ver decisions.md#D-NNN | decisions.md#D-NNN | <current round> |
```

Update the SU header `Última actualização`. (Per `docs/ARCHITECTURE.md §4.5` — the decision is citable from the SU like any other id.)

### 5. Auto-invoke aisa-synthesize

Immediately invoke the `aisa-synthesize` skill. Wait for it to return; it produces the 5 topic packs in `_synthesis/`. If any topic-pack synthesis fails → record the failure in `council-log.md` but do NOT roll back the decision (the synthesis can be retried manually).

### 5c. Story

Append one narrative episode to `<engagement>/story.md` (`## Episódio <N> — <data> — a decisão (e porquê)`): 4-8 frases na voz do sponsor, sem jargão de kernel, máx. 2 ids citados. Create the file with `# Story — <slug>` if missing (pre-v2.3 engagements).

### 6. Wrap-up output

"Decision D-<NN> registered. Synthesis produced <N>/5 topic packs in `_synthesis/`. Next: `/render --all` to produce the 6 deliverables, or `/render <id>` for one."

If a topic pack failed:
"Decision D-<NN> registered. Synthesis produced <N>/5 topic packs in `_synthesis/`; FAILED: <list>. Run `/synthesize` to retry, then `/render --all`."

## Notes

- The decision is the only point where the *user* (not the council) must say a sentence. Everything else has been council + chairman.
- **Append-only** on `decisions.md` and the SU — D-NNN ids monotonically increase across re-decisions.
- No council runs in Decision. `chairman-synthesis` is invoked by `aisa-frame` and `aisa-options` only; the decision block is written fresh by this skill from the user's answers (plus the optional `--consult` review).
