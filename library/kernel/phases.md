# Phases — Kernel v0.2.0

The aisa engagement progresses through 4 phases. Each phase declares its mode of orchestration, the lenses active, and soft entry/exit criteria. Phases are defined here; the 5 knowledge states are in [`states.md`](states.md); orchestration modes in [`orchestration.md`](orchestration.md).

## Enquadramento (P-0) — before Phase 1

> Not a phase: the intake that precedes Discovery. The engagement still has four
> phases, and `_state.json.phase` never takes this value.

Before any lens runs, the process owner says **in their own words** how the business works at
the point the request touches. This is the owner's HYPOTHESIS, not verified fact: `/frame`
confirms or corrects each `M-n` with evidence.

**Seven themes, fixed order, one `AskUserQuestion` each, answer kept verbatim.** The ids are
stable and are the anchors of `enquadramento.md` (`## T4 · outcomes`). They describe A
PROCESS — any process — and none of them presumes what the process produces:

| # | id | como se diz ao utilizador |
|---|---|---|
| T1 | `actors` | quem faz parte disto — que papéis intervêm, e quem manda no processo |
| T2 | `trigger` | o que faz o processo começar, e com que frequência |
| T3 | `activities` | o que se faz, por ordem, e onde se decide algo |
| T4 | `outcomes` | o que sai no fim, para quem, e como se sabe que correu bem |
| T5 | `invariants` | o que tem de se manter sempre verdadeiro — as regras que ninguém pode quebrar |
| T6 | `failure_today` | o que corre mal hoje, quanto custa quando corre mal |
| T7 | `change_requested` | o que o pedido quer mudar nisto |

`T5` is where the `M-n` invariants come from, verbatim, one sentence each.

### The `pricing` conditional set

Immediately after `T4`, **one** explicit question, asked in every engagement:

> A saída deste processo é um preço, cotação, margem ou valorização?  —  *Sim* / *Não*

**Sim** activates five further themes; **Não** skips them entirely. The activation is never
inferred from the narrative, from the slug, or from what the request seems to be about — a
process that mentions money is not a pricing process, and a pricing process that never says
so still gets asked.

| id | como se diz ao utilizador |
|---|---|
| `P1 sold_what_when` | o que se vende, e quando |
| `P2 price_fixing_moment` | quando o preço se fixa e quando a venda acontece |
| `P3 cost_driver` | o que determina o custo |
| `P4 valuation_driver` | o que determina a valorização |
| `P5 uncertainty_shape` | de onde vem a incerteza e como evolui no tempo |

These live in the kernel, not in a pack: pricing is a shape a process can have, not a
property of a digitalization platform. A pack may ADD themes of its own through
`pack.yaml: enquadramento.extra_themes[]` (`{id, question_pt, when}`), and today every pack
declares that list empty.

After the themes, in this order and unchanged: the invariants read back from `T5`, who
besides the owner may confirm facts about this process (`states.md` → *Confirmed threshold*,
rule 3), and the funding gate.

**Output**: `enquadramento.md` with one `## Tn · <id>` section per theme, in order. The
`## pricing` section exists **only** when the set was activated, and carries the marker
`<!-- INTAKE-SET: pricing -->` so the activation is readable, never guessed. Engagements
written before this contract have no `Tn` sections and are read as they are — the presence
of the data is the criterion, and the generation is never inferred from a date or a version.

---

## Phase 1: Discovery

**Goal**: Map operational context, shadow stakeholders, as-is process, constraints. Do not name vendor/product.

**Lenses active (habitual order)**: business → operations → user → data → governance → financial — **mandatory when the six run as one full round** (`/round`, enforced by `pre-lens-order-check`); **free when a lens runs alone** (`/round <lens>`: any lens, no prerequisite, in any order — `/round` records it in `_state.json.round_lenses` = `{ronda, modo, lentes}`, which is what the guard reads; the record is scoped to the round and the lens, so a leftover authorises nothing, and its absence means the order is policed). A lens run alone before `business` still has a denominator: the owner's `M-n` (R-00) and earlier rounds are already in the SU.

**Mode**: `inline` (each lens sees the Shared Understanding accumulated by previous lenses)

**Rounds — in progress vs completed**: `_state.json.round` is the last **completed** round; `_state.json.round_in_progress` is the round an open `/round` is filling (empty or absent → none open). `/round` with no argument opens and closes a round in the same call. `/round <lens>` runs inside the round already open, or opens one; the round closes when **all six lenses have stamped it** (a section header `## R-NN …` in each `lens-outputs/<lens>.md` — header match, never a substring; `dashboard.py::lenses_for_round`, published as `engagement.lentes_ronda_aberta`), in one call or across several, in any order — or on `/round --close`. "`financial` wrote" is not a close signal: alone, it may be the first to run. A lens is never re-run in the same open round without the user saying so (`aisa-round` step 3.7). Everything that asks *what is done* — the exit criteria below, `/frame`, `/status` — reads `round`; everything that asks *which round are the lenses stamping now* — the lens-order guard, the lenses' `ronda` column — reads `round_in_progress` when it is ahead of `round`. A round in progress is not a completed round.

**Entry criteria**:
- `_state.json` exists with `phase: discovery`.
- `context.json` has at minimum: literal request, requester role.
- `enquadramento.md` exists — the process owner's declaration of the business mechanism, as `M-n` invariants, written by `/start` (soft — warn if missing or *"não declarado"*; the lenses then work without a denominator for their questions). Its `M-n` enter the SU as `Confirmed`, `lens = enquadramento`, `ronda = R-00`: the owner's hypothesis, not verified fact.
- Capture run for supported inputs — `_capture/` artefacts exist for every `.xlsx`/`.xlsm` in `inputs/` (soft — warn if missing; `/capture` fixes it).

**Exit criteria** (soft, advisory):
- `## Confirmed` has ≥10 rows.
- `## Unknown` Critical = 0. A question the round arbiter lowered to `cosmético` for want of a declared technical consequence carries its `criticidade` down with it (`states.md` → *Admission of a question*), so it stops pressing this gate: what remains `Critical` here moves one of the eight technical axes.
- `## Conflicted` Critical = 0.
- All 6 lenses have written to `lens-outputs/`.
- The last round converged: `Unknown` created in that round ≤ `Unknown` closed in it (any origin). A round with `criadas > fechadas` is labelled `sem convergência` by `/round` and `/status` — visible, not blocking, no new state. Counts come from the motor (`dashboard.py --json`), never by hand. The label is per **closed** round, not per calendar span: a round filled lens by lens over days, with `/answer` in between, is balanced only when it closes.

**Outputs**:
- `shared-understanding.md` populated.
- `lens-outputs/<lens>.md` per lens.

---

## Phase 2: Framing

**Goal**: Synthesize a single sentence: "The problem is X, felt by Y, costs Z today, evidence is W." Along the way, **confirm or correct each `M-n`** of `enquadramento.md` with evidence — a corrected invariant is a normal transition (`was C-nnn`), never an edit of the R-00 row.

**Lenses active**: subset of the 6 Discovery lenses (chairman picks the 3-4 most relevant given the Shared Understanding).

**Mode**: `council-independent` (parallel Task subagents; only the chairman writes to the Shared Understanding).

**Entry criteria**:
- Exit criteria of Discovery met (overrideable with justification).

**Exit criteria** (soft):
- The **current** frame sentence approved in `decisions.md` — an approval record whose
  `Frame sha256` matches the sentence in `frame.md` (see *Frame approval record*).
  Any free `D-NNN` id; the old habit of assuming `D-001` is what let an approval of
  one sentence stand for another.
- Sponsor explicitly confirmed (`Validated by`).

**Outputs**:
- `frame.md` in the project root.
- New rows in `## Confirmed` from chairman synthesis.

---

### Frame approval record (normative)

An approval approves a **sentence**, not a file and not a round. The record in
`decisions.md` therefore carries the fingerprint of the sentence it approved, so that a
regenerated frame stops matching it (F05, `docs/ADVERSARIAL_REVIEW_2026-09-08.md`: an
F-01 approval waved through an F-02 sentence nobody had approved).

```markdown
## D-NNN — Frame agreed (F-NN)

- **Frame sentence**: <verbatim, as it stands in frame.md>
- **Agreed in round**: F-NN
- **Frame sha256**: <64 hex of the normalised sentence>
- **Supersedes**: D-00x (frame F-0y) | —
- **Anchors**: …
- **Override used at /frame**: <reason | —>
- **Validated by**: owner (<name/role>, via AskUserQuestion) | executor [ÂMBITO AUTORIZADO]
- **Timestamp**: <ISO-8601>
```

- The id is the **next free `D-NNN`**, never a fixed `D-001`: frame, solution and
  blueprint approvals share one monotonic counter, and the motor derives what each
  block IS (`kind`) from its content.
- The fingerprint is always computed from `frame.md` by the motor
  (`dashboard.py --json` → `frame.sha256`), never from the text of the decision block
  and never by hand: `pricing-marinha-pilot-1` holds an English sentence in `frame.md`
  and a Portuguese one in `D-001`, which is exactly the drift this rule closes.
- **The sentence unchanged in a later round is not a new approval**: no new block, no
  new id — one line in `council-log.md` (`frame unchanged since D-00x (sha256 match)`).
  Same doctrine as revalidation in `states.md`: the fact did not change, so the check
  is renewed, not the record.
- `Supersedes` is the **only pointer ever written** (forward, in the new block). Nothing
  edits an existing block: `decisions.md` is append-only and a decision keeps its
  counterfactual. The reverse pointer (`superseded_by`) is derived by the motor.
- Approvals written before this rule carry no fingerprint. They are `legacy`: they can
  be re-confirmed by the owner (a new block with the fingerprint, superseding the old),
  never silently trusted.

---

## Phase 3: Options

**Goal**: Generate 3-5 applicable options — technologies and implementation patterns — each with its high-level architecture, order of magnitude, cost drivers, risks and reversibility; close with the aisa's reasoned recommendation, which is not the decision. **The technology lens enters here for the first time.**

**Lenses active**: technology (new) + business + operations + financial (others read-only).

**Mode**: `council-independent`.

**Entry criteria**:
- Phase 2 frame validated by sponsor **for the sentence currently on file** —
  `dashboard.py --json` → `frame.verdict` is `match` or `match-other-round`.
  `mismatch`, `legacy` and `none` are soft: `/options` shows both sentences and asks
  the owner to approve, redo, or proceed without approval with a justification.
- Or a reopening: `phase=decision` with a REABRIR verdict from `/revisit`, or
  `/options --reopen "<justification>"` (see *Transition rules*).

**Exit criteria** (soft):
- ≥3 options recorded. **Doing nothing and changing the process are conditional members**:
  each enters when discovery showed it plausible, and where one does not, the round's log
  declares why with ids (`DO-NOTHING` / `PROCESS-CHANGE` class coverage). A silent absence is
  the defect; a reasoned one is a finding.
- **Every option carries an order of magnitude with its source declared** — the band from
  `/simulate`, from the pack's estimation model, or from a named analogy — or the field written
  as unavailable with what is missing. A number with no source is invented
  (`.claude/skills/chairman-synthesis/SKILL.md` owns the method and its four markers).
- **An organisational rule blocks an option; it never deletes it.** The option stays in the set
  with the verdict *viable if the rule is changed* and its seven fields. Where the technology is
  imposed, the set is generated **inside** that boundary and no option proposes changing platform.
- **The round closes with the aisa's reasoned recommendation**, separate from the decision: the
  option, what separates it from its siblings, what it rests on, what would flip it — or
  `no recommendation` with what would produce one.
- **Every option names its technology**, and a platform option names the *form* — surface *and*
  store, in products, one option per form (the pack's option-class register owns the forms; for
  `pp` that is `decision-model/alternatives-register.md` §1.2). An option rendered as *"the
  platform"* has withheld the choice the phase exists to present.
- `decision-tree.md` from the pack consulted (if applicable).

**Outputs**:
- `options.md` — the decision as a table (option · technology · verdict · order of magnitude ·
  reversibility · what blocks it), then one short entry per option, then the recommendation. **Budgeted: ~1 500 words of prose (the table is not prose), ≤120 per option.**
  The complete per-option field set and the twelve-line concern coverage live in
  `lens-outputs/chairman-synthesis-O-<NN>.md`, which the artefact projects and never replaces
  (`.claude/skills/chairman-synthesis/SKILL.md` owns both shapes).
- Optional: `_simulation/options-comparison_v<NN>.md` (via `/simulate`) — a per-option projection (screens, effort band, risks, constraints) plus the value-of-information list of decision-flipping Unknowns.

---

## Phase 4: Decision

**Goal**: Capture choice + justification + alternatives + risks + revision conditions. Auto-trigger synthesis.

**Lenses active**: none by default — the decision is the **user's**. `lens-technology` (via the solution-architect agent) may be consulted ad-hoc with `/decide --consult` for an advisory review of the chosen option.

**Mode**: `interactive` (user-driven). No council synthesis runs in Decision — the council's work ended at Options; here the user chooses and justifies.

**Entry criteria**:
- Phase 3 options reviewed by sponsor.

**Exit criteria** (soft):
- `decisions.md` has the chosen option with justification + alternatives + risks + revision conditions.
- `/synthesize` auto-ran successfully (5 topic packs in `_synthesis/`).

**Outputs**:
- `decisions.md` (D-NNN entries) + the matching `D-NNN` row in the SU `## Confirmed`.
- `_synthesis/{business-story, as-is, architecture-story, risks-and-assumptions, financial-story}.md`.
- For engagements with a UI component: `_blueprint/ux-blueprint_v<NN>.yaml` (via `/blueprint`, per `blueprint-contract.md`) — iterated with the business until approved (its approval is itself a D-NNN).
- `_coverage/coverage_v<NN>.json` (+ its Markdown projection) — the recorded coverage reviews, per `coverage-contract.md`: the reconciliation the design was produced against, and the review of each concrete version. Written by the coverage motor's `finalize`, never by hand, and immutable once published.
- Render-ready state.

---

## Transition rules

- Transitions are user-triggered (`/frame`, `/options`, `/decide`).
- Soft gates are **evaluated** by the `phase-gate-check.py` hook (`PreToolUse` on the
  transition skill) and do not block. Each criterion above carries a **mode**: evaluated by
  code, left to the skill's judgement, or not evaluable at all. The verdict is written to
  `<engagement>/gate-log.md` with the fingerprint of the state judged; a later override
  refers back to it. Coverage is declared (*n of m by code*) — a criterion nobody can
  measure is never reported as OK, and a per-option criterion with zero options is not
  vacuously satisfied.
- **Readiness is not approval, and neither is a green check.** The Decision phase answers four
  separate questions about a design version — is the artefact well formed (`blueprint-contract.md`
  → *Validação estrutural*), does it carry what the sources asked for (`coverage-contract.md`),
  did the business approve **this** version (a `D-NNN` block), and was the solution proved
  end to end (nothing in aisa proves this). No check answers another's question, and no
  motor records an approval: the request goes to the business explicitly, and silence is not
  a yes. This integrates into the existing Decision phase — **no fifth phase, no new state,
  no new approval state machine**, and the soft gates between phases stay soft.

- Override syntax: `/frame --override "reason"` — logged in `decisions.md`.
- Phase regression is allowed (`/round` from Framing returns to Discovery scope if needed).
- **`decision → options` (reopening the alternatives)** is an explicit transition, not a
  regression. `/revisit` recommending REABRIR used to end in a dead end: `/options`
  refused `phase=decision` and so did `/frame` (F07). It runs when the latest
  `_simulation/revisit_*.md` declares `Recomendação: REABRIR`, or when the owner passes
  `/options --reopen "<justification>"` — the decision is the owner's, and forcing them
  to invent a tripwire would make the record worse, not better. It:
  - writes `phase = options`, `round = <next O-NN from HISTORY>`, `round_in_progress = ""`;
  - **never touches the previous decision**: the new decision block (written later by
    `/decide`) carries `Supersedes: D-00x — reaberta em O-NN por <TW-n | decisão do dono>`;
  - logs the reopening in `council-log.md` with what triggered it.
- **Round counters come from history, never from `_state.json` alone.** After a decision
  the state holds `D-01`, so an Options round derived from it would restart at `O-01` and
  overwrite the round that produced the decision being revisited. The `O-` counter is the
  highest of `lens-outputs/chairman-synthesis-O-NN.md` (one per round, never rewritten),
  the `## O-NN` headings of `council-log.md`, and the state when it still holds an `O-`.
  `options.md` is not a source: it is rewritten in place.

See [`render-contract.md`](render-contract.md) for what happens after Decision (synthesize → render).
