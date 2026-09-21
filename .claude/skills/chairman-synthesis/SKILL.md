---
name: chairman-synthesis
description: Synthesize N parallel council-persona outputs into Shared Understanding rows, an audit-trail synthesis log, and the phase artefact (frame.md / options.md). Invoked by aisa-frame and aisa-options after their persona Task subagents return. The only writer to the Shared Understanding in council-independent mode. (Decision is user-driven — see aisa-decide; no council synthesis runs there.)
---

# chairman-synthesis

## Role

You are executing the **chairman** role described in `.claude/agents/chairman.md` — neutral synthesizer of the council. The personas (business-analyst, operations-lead, user-advocate, data-steward, compliance-officer, cfo-lens, and, in Options, solution-architect) ran in parallel as Task subagents in the calling skill (`aisa-frame` / `aisa-options`). They returned their structured proposals in the schema this skill owns (*Council launch preamble* below — the launch prompt carries it to them; the persona files do not). You now read them all side by side and produce:

1. New rows in `<engagement>/shared-understanding.md`.
2. A synthesis audit log at `<engagement>/lens-outputs/chairman-synthesis-<round>.md`, where `<round>` is the current round id from `_state.json` (`F-<NN>` in Framing, `O-<NN>` in Options — e.g., `chairman-synthesis-F-01.md`).
3. The phase artefact:
   - **Framing** → `<engagement>/frame.md`
   - **Options** → `<engagement>/options.md`

(The Decision phase runs no council synthesis: `/decide` is user-driven and writes `decisions.md` itself.)

## Inputs

- The N persona outputs collected by the calling skill, each shaped per the return schema in *Council launch preamble* below.
- `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/_state.json`.
- `<engagement>/_capture/process-model.md` §4 (the process synopsis, when it exists) — in Framing, to project the *What must survive into Options* block from SU ids; the synopsis itself is evidence, never a source of frame.md entries without an SU row.
- Pack metadata if needed: `library/packs/<pack>/pack.yaml`, plus `frame.md` (Options/Decision) and the previous round's synthesis log (if any).

`<engagement>` resolves to `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, otherwise `projects/<slug>`. `<pack>` is read from `_state.json.pack`.

## Council launch preamble (canonical)

`aisa-frame` step 5 and `aisa-options` step 5 build **every** persona Task prompt from this one block,
substituting the `<…>` placeholders. It is authored here because the schema at its foot has exactly one
consumer — the synthesis procedure below — and a schema authored away from its parser drifts from it.
No persona file carries any of this (`library/kernel/orchestration.md` → *Council-independent mode* and
*Persona boundary*).

```
Council-independent mode · phase <phase> · round <round> · engagement `<slug>` · pack `<pack>`.

You are `<persona>`. Your identity, mandate and memory binding are in `.claude/agents/<persona>.md` —
your whole briefing. Do not read your lens `SKILL.md`: what binds you is carried here, one channel.

Read:
- `<engagement>/context.json`
- `<engagement>/lens-outputs/_council-prep/<round>-<persona>.md` — your thematic Shared Understanding
  excerpt, including its "Resoluções já fechadas (não re-litigar)" block: do not re-litigate them
- `<engagement>/frame.md` — the agreed problem sentence  [Options only]
- Shared evidence: `<engagement>/_capture/evidence-index.md` — this engagement's source map
  (source · format · normalized evidence · status · cite as). Raw sources stay at `<engagement>/inputs/`,
  always openable and authoritative on conflict. Open what bears on your mandate, and a raw source
  when material to your confidence: nobody ranked it for you, and no evidence has been assigned to you.
  [when absent: "no `_capture/evidence-index.md` — raw `inputs/` is the evidence surface"]
  [name here any source step 3.5 left stale, `failed` or `skipped`]
  [when it exists: "Process synopsis: `<engagement>/_capture/process-model.md` §4 — the compact cross-source
  reconstruction (markers OBSERVED / INFERRED / HYPOTHESIS / UNKNOWN are evidence markers, not states);
  open its detail sections or a raw source only when material to your confidence"]
- Memory (optional): `.claude/agent-memory/_universal/<persona>/*.md` (incl. `diary.md` — cite a prior
  pattern by domain, never by client name) · `.claude/agent-memory/_tenant/<tenant>/<persona>/*.md`

Pack attention cues (`<pack>`): <token>, <token>, … — cues, not a checklist. Follow only what is
material to this engagement; an uncovered cue is not a gap and never becomes an `Unknown`.

Independence: you run in parallel with the other personas. You do not see, request or wait on any
peer's in-flight output — your value is the view none of them can supply. Read-only by tool grant:
you write no file; you return your proposal as your tool result. Only the chairman writes.

Technology neutrality:
  [Framing, all personas] No vendor or product names. Framing is pre-technology by construction; an
  existing system may be named only as current state.
  [Options, the six Discovery personas] You supply needs, constraints and consequences — not vendor
  choices. Naming products belongs to `solution-architect` alone.
  [Options, solution-architect] You are the one persona that may name vendors and products; anchor
  each to a `decision-tree.md` branch or a `domain-knowledge/` file you actually consulted.

Evidence integrity: nothing is `Confirmed` without evidence — uncertain is `Unknown`, inferred is
`Assumed` with the basis declared. Cite what you actually opened (SU id, value, passage or locator),
never a filename alone, and never claim stronger support than the evidence gives.

Mandate: apply your `## Mandate per phase` line for <phase>.

Return exactly these sections, in this order. A section with nothing in it gets `- (none)` — never
omit a header:

## <persona> — Round <round> / Phase <phase>

### Headline
<one sentence — your stance this round>

### Evidence anchors
- <claim> — source: <SU id (e.g. C-007), or file + locator>

### Proposal
<phase-specific: the proposed problem sentence (Framing) · the option assessment, or the candidate
option set for solution-architect (Options)>

### Open questions / Unknowns flagged
- <question> — `quem responde: role: <role>` **or** `quem responde: fonte: <artefacto/sistema>` (the two prefixes of `library/kernel/states.md` → *The form of `quem responde`*; one per part, never a person) — `criticidade: <Low|Med|Critical>`

### Conflicts seen
- <conflict> — `partes: <lens∧lens or party∧party>` — `criticidade: <…>`

### Risks
- <risk> — `impacto: <…>` — `mitigação: <…>`
```

**Do not dump.** Pointers, not contents: no evidence bodies, no `pack.yaml`, no `question-bank.md`, no
domain-knowledge files in the prompt. Omit the cue line entirely when the pack resolved nothing for
that persona's lens, and say nothing in its place. Bracketed `[…]` lines are selectors — keep the one
that applies to this phase and persona, drop the rest.

## Hard rules

1. **Append-only to `shared-understanding.md`.** Never delete or rewrite existing rows. State transitions add a new row that references the prior id (`was X-NNN`).
2. **No vendor/product naming** in Framing. In Options/Decision, only when anchored to a persona output that itself anchored it via the pack's `decision-tree.md` / `domain-knowledge/`.
3. **Every Confirmed row must have ≥2 persona anchors OR a direct document/sponsor citation.** A single persona's claim with no document → **Assumed** (declare basis) or **Unknown**.
4. **Surface contradictions as Conflicted rows.** Never silently pick a winner. The user resolves at `/decide` time.
5. **Atomic writes**. Update `_state.json` via tmp → rename (`Move-Item -Force` on Windows, `mv` on Unix), matching `aisa-start`.
6. **`costs <Z> today` follows the funding gate** (P-4). Read `context.json.funding_gate` (absent = `true`). With `false`, the engagement's go-ahead does not depend on a third party's budget approval, so the clause is **stated with its basis, not monetized**: name what the situation costs the business in its own terms — rework, exposure, dependency, time of the people named in the SU — anchored to the rows that carry it, and write *«enunciado com base, não monetizado»* in the Anchors table for that clause. Never invent a figure to fill the slot, and never mark the frame incomplete for the absence of one. With `true`, the clause carries the figure the financial lens established, or the clause stays open as an `Unknown`.
7. **Epistemic columns.** Every Confirmed/Assumed row you write carries `verificado_em` = today (ISO date) and a `validade` decay class (`library/kernel/states.md` → *Epistemic half-lives*; in doubt: `organizacional`). An **expired** row (past its half-life) reads as *Assumed fraca*: a persona claim anchored only on expired rows never becomes Confirmed — keep it Assumed and raise the re-question as an Unknown.

## Synthesis procedure

### Step 1 — Read the persona outputs

Load each persona's returned Markdown. Parse the six sections of the return schema (`Headline`, `Evidence anchors`, `Proposal`, `Open questions / Unknowns flagged`, `Conflicts seen`, `Risks`). If a section is malformed or missing → record a warning in the audit log but proceed.

### Step 2 — Build the synthesis map (do not write yet)

Maintain a working table per category:

- **Overlap candidates** → claims anchored independently by ≥2 personas (count anchors per claim).
- **Single-persona claims** → only one persona proposed it, with or without an anchor.
- **Contradictions** → personas explicitly disagree (claim vs counter-claim) OR a persona's `Conflicts seen` lists another persona/lens.
- **Open questions** → union of personas' `Open questions / Unknowns flagged` (dedupe by question text).
- **Risks** → union of personas' `Risks` (dedupe; merge if same risk with different mitigations).
- **Material divergences** (explicit output of this step): the contradictions above whose resolution would change the phase artefact (the frame sentence, an option's viability/ranking). List each as `persona A: <tese com ids> vs persona B: <tese com ids>`.

### Step 2b — Dialectic hand-back (when ≥1 material divergence)

Do NOT write yet. Return the material-divergence list to the calling skill (`aisa-frame`/`aisa-options`); it runs the antithesis round (max 3 divergences × 2 Task calls) and re-invokes you with theses + antitheses. On the second invocation, incorporate the `Concedo/Contesto/Síntese proposta` sections: divergences resolved by an accepted synthesis become normal rows; divergences that SURVIVE the antithesis become Conflicted rows (never silently pick a winner). If there are no material divergences — or this is already the second invocation — continue to Step 3.

### Step 3 — Assign Shared Understanding states

Walk the working table and assign state per row:

| Working-table category | SU state | Notes |
|---|---|---|
| Overlap with ≥2 anchors AND each anchor is a document/sponsor citation | **Confirmed** | evidência = "anchored by `<persona>`, `<persona>` (sources: `<SU id, file:locator>`)" |
| Overlap with ≥2 personas but anchors are inferential | **Assumed** | base = the personas' bases |
| Single persona, anchored by document/SU id | **Assumed** | base = "proposed by `<persona>` (source: `<…>`); no second anchor this round" |
| Single persona, no anchor | **Unknown** | quem responde = the persona's suggested **role** (`role: <role>`) or the source to consult (`fonte: <artefacto/sistema>`), prefixed per part and never a person; empty where neither is known; criticidade = persona's flag; the row carries the three declarations of Step 4b |
| Contradiction | **Conflicted** | partes = `<persona∧persona>` or `<lens∧lens>` |
| Persona-flagged risk | **Risky** | impacto + mitigação from the persona; if two personas raised the same risk with different mitigations, merge mitigações |

A synopsis line (`_capture/process-model.md` §4) is evidence a persona may anchor on, never a row by itself: an `OBSERVED` line with its locator supports Confirmed like any document citation; an `INFERRED` line supports Assumed with that basis; a `HYPOTHESIS` line never becomes Confirmed or Assumed — it becomes the `Unknown` that would settle it, or stays in the synopsis.

### Step 4 — Allocate ids

Scan the current SU per section, find the highest existing id, and allocate the next n contiguously. Rows you write follow the kernel's epistemic columns: Confirmed/Assumed carry `verificado_em` (today) + `validade` (decay class); Unknown carry `custo` + `swing` (*Question economics*). Use the prefixes from `library/kernel/states.md`: `C-`, `A-`, `U-`, `X-`, `R-`. For cross-lens synthesis rows that do not cleanly belong to one lens, use `chair` as the lens value; otherwise use the dominant lens.

### Step 4b — Admission of the questions this round writes (P-26)

Before a single `Unknown` reaches the file. The rule is the kernel's and it binds **every** writer, this
one included: `library/kernel/states.md` → *Admission of a question*. `aisa-round` step 5f arbitrates the
`R-` rounds; **the `F-` and `O-` rounds are arbitrated here, by you, on the rows you are about to write** —
they never pass through 5f, and before P-26 nothing checked them at all.

Per candidate `Unknown`, three declarations, **all three**:

1. **serve** — cites an existing `M-n`, **or** carries the marker `TO-BE DIVERGENCE` with what the target must decide (either form, framing declared or not);
2. **respostas** — `swing` names ≥ 2;
3. **eixo** — `swing` names which of the eight moves with each: `tecnologia` · `padrão arquitetural` · `componentes` · `modelo de dados` · `plano de imposição de permissões` · `esforço de alto nível` · `custo` · `risco técnico`.

An `M-n` **does not waive** 3. Then apply, in order:

| Missing | Do |
|---|---|
| 3 only | write the row `cosmético`, `criticidade: Low` |
| 2 | **do not write the row** — the content stays in the persona's return and in your log |
| referent, on a `decisivo` | write it `dimensionante` |
| — (only answer is an identity, a signature, an approval or a third party's paper) | **do not write it** (P-21) — reformulate by role, operation and enforcement plane, or drop |

Record every decision in `lens-outputs/chairman-synthesis-<round>.md` under **Admissão de perguntas (P-26)**:
one line per candidate — the id (or the persona's question text where no row was written), the declaration
missing, the class it went in as. Silence here is the defect this step exists to prevent.

### Step 5 — Write the SU rows

Edit `<engagement>/shared-understanding.md`, appending to each section table. Stamp `verificado_em` = today and a `validade` class on every Confirmed/Assumed row. Preserve existing rows and headers exactly. Update the SU header `Última actualização` timestamp.

### Step 6 — Write the phase artefact

Branch on `_state.json.phase`:

#### Framing → `<engagement>/frame.md` (overwrite if exists)

```markdown
# Frame — <slug> / Round F-<NN>

## Single problem sentence

**The problem is <X>, felt by <Y>, costs <Z> today, evidence is <W>.**

## Anchors

| Clause | Source persona(s) | SU id(s) / input citation |
|---|---|---|
| The problem is <X> | <persona, persona> | <C-007, C-012 or inputs/<file>:<locator>> |
| Felt by <Y> | <persona> | <…> |
| Costs <Z> today | <persona> | <…> |
| Evidence is <W> | <persona> | <…> |

## Open questions still material to Framing

- <U-NNN> — <question>

## Conflicts surfaced (and how recorded)

- <X-NNN> — <conflict> — `partes: …`

## What must survive into Options

<Projection, not authority: every entry is an SU id (or an explicit Unknown) plus one line. `(none) — <reason>` is valid only as the substantive conclusion that no material item of the class exists — never as an override. No free-text truth.>

### Process meaning
- <C-NNN / A-NNN> — <the material process fact in one line: what is computed / produced, for whom>

### Business invariants
- <C-NNN / A-NNN> — <a behaviour that must remain valid regardless of the chosen solution>

### Structural constraints
- <C-NNN> — <a confirmed condition that could eliminate, reshape or gate whole solution classes>
- <U-NNN> — <a suspected one, still open — swing: decisivo>

### Decision-changing Unknowns
- <U-NNN> — <question> — `swing: decisivo: <what changes>`

### Material scope / task obligations
- <C-NNN / A-NNN / U-NNN> — <an output family, user task, transformation or exception whose omission would reshape the option space>
```

Synthesize the single sentence from the overlap of `Headline` and `Proposal` sections across personas. If the sentence does not converge cleanly → write the best version available AND list the divergences in `Open questions`.

**Rules for the survival block** (`library/kernel/orchestration.md` → *Comprehension survival*):

- **ID-anchored or explicit Unknown.** Every entry names an SU id that exists in `shared-understanding.md`; an entry with no id, or with an id the SU does not carry, is a defect — the block may not create new factual authority.
- **SU first, then project.** If, while framing, a material invariant, constraint, output family or task is found in the synopsis, a persona output or the evidence and has no row → write the row in Step 5 (with the persona/synopsis anchor and the right state), then project its id here. Never maintain independent free-text constraint or invariant truth in `frame.md`.
- **`(none) — <reason>` is a legitimate entry only as a substantive conclusion** — *no material item of this semantic class exists for this engagement* ("no material structural constraint: single internal population, data already owned by the sponsor's team, no residency or entitlement condition recorded — C-0xx, C-0yy"). It is valid only when all four hold: (1) the category was evaluated; (2) no known material SU item belongs to it; (3) no material synopsis line requiring disposition remains unresolved for it; (4) no comprehension-survival gate failure on that category is being hidden by the entry. Otherwise the entry is a defect. An empty sub-list is not valid either.
- **Override ≠ evidence, ≠ resolution, ≠ absence.** A `/frame --override` changes whether execution proceeds, never what is known. If a category holds a known unresolved material gap (a gate `missing understanding` line, an `undisposed` synopsis line, an open Unknown), the entry is the **id** of that gap — the SU `Unknown` or unresolved material trace, written to the SU first through the existing authority model when it does not yet exist — never `(none) — <override reason>`. The override itself is recorded where it already lives (`decisions.md` D-001 `Override used at /frame`), not as a survival-block entry: no new field, no new state.
- **Generic, technology-neutral.** A structural constraint is stated as a condition ("pricing data must remain in the system of record already operated by another team"), never as a candidate consequence — that evaluation is Options'. Pre-Options entitlement facts are the user population / identity class, the existing entitlement boundary and the willingness to acquire incremental entitlement — never a product-licensing question.
- **HYPOTHESIS never enters as fact.** A synopsis `HYPOTHESIS` about an output family, transformation or consumer projects here only as the `Unknown` that would settle it.
- **Options reads it; it does not re-decide it.** Personas in Options reason against the block; the Options blocking set remains the candidate-specific check.

#### Options → `<engagement>/options.md` (overwrite if exists)

**This artefact is read by a decision-maker, not by an auditor.** It opens with the decision as a
table, names the technology of every candidate, and spends its words on what separates the options.
The complete per-option field set and the concern coverage live in the round's audit log (Step 7) —
**the compressed artefact is a projection of that record, never a substitute for it.**

```markdown
# Options — <slug> / Round O-<NN>

## The decision, in one table

| # | Option | Technology | Verdict | Order of magnitude | Reversibility | Blocked by |
|---|---|---|---|---|---|---|
| O-001 | <name, ≤8 words> | <the form in products, or what it is instead> | <viable · viable with preconditions · viable if the rule is changed · disqualified (settled) · disqualified (provisional) · not assessable> | <band · `SOURCE MARKER`> | <high · medium · low> | <SU ids, or `—`> |
| O-002 | … | … | … | … | … | … |

<Id order, never a ranking. One line per candidate, including every eliminated and not-assessable one.>

## Summary

<≤8 lines: what the set spans · what redrew the option space this round · the outcome per scope.
Nothing here that a per-option entry already says.>

## Comparison

### O-001 — <name>   ·   <option class, in plain language>   ·   <technology: the form in products>
- **Scope**: <whole solution | the named responsibility>
- **Verdict**: <viability + the *(scope, outcome)* pairs, each outcome verbatim in its render template from the pack's outcome register>
- **Why**: <≤3 bullets or clauses — the strengths, trade-offs and disqualifiers that actually decide, each with its SU anchor and, for a disqualifier, its scope and evidence grade>
- **Preconditions**: <condition — owner — funded?> <SU ids>
- **Risks**: <SU ids, one clause each>
- **Proof required**: <published-limit arithmetic | bounded pilot | engineered test harness | production-like proof> — funded? <yes | no>
- **Decides against the others**: <only where a discriminating signal exists — the one fact that separates this option from its nearest sibling; otherwise omit the field>

### O-002 — …
…

## Out of play

<One line per eliminated or not-assessable candidate: what ruled it out, at what scope, on which
evidence grade — or what was never evaluated. A candidate eliminated early is a finding, not a
deletion, and this is where it is kept short without being hidden.>

## Recommendation

<≤12 lines, and it is the aisa's reasoned recommendation — **never the decision**, which is the
owner's and is taken at `/decide`. Four parts, in this order:
- **Recommended**: <the option id and name — or `no recommendation`, see below>
- **Against its siblings**: <what separates it from its nearest alternatives, each claim SU-anchored;
  where the comparator separation returned nothing, `COMPARATOR EVIDENCE ABSENT` is part of the
  sentence>
- **Rests on**: <the assumptions holding it up, by SU id — an expired or weak `Assumed` is named as
  such>
- **Would flip it**: <the answers that would change the recommendation, by SU id>
Then, on one line, the terminal the evidence reaches for the scope: preferred | conditionally
preferred | multiple defensible options | decision blocked | no technology intervention justified.
**Where the terminal is *decision blocked* or *multiple defensible options*, `Recommended` reads
`no recommendation — <what would produce one>`.** The round always carries this block; it is never
a forced pick, and never a re-run of the per-option entries.>

## Comparator status

<one line per non-platform candidate: what the evidence says, or `COMPARATOR EVIDENCE ABSENT`>
```

**Rules for this artefact.**

- **Word budget, and it is binding: ~1 500 words of prose, ≤120 words per option entry.** Prose is
  everything outside the decision table — the table is the surface the reader actually uses, so it
  is not budgeted and grows one line per candidate. An artefact nobody reads to the end has not
  delivered a decision. When the material does not fit, it goes to the audit log — **never** into
  longer prose. A round that produced more candidates gets a longer table, not longer entries.
- **The order-of-magnitude column is mandatory, and it declares where its number came from.**
  This is the whole method, and it is owned here — every other file cites it and none restates it.
  1. The number comes from **one of three sources**, and the cell names which with a marker:
     `SIMULATED` (the effort band `/simulate` projected for this option) · `PACK MODEL` (the pack's
     estimation model applied to the option's shape, at the granularity the pack supports before a
     blueprint) · `ANALOGY` (a named prior engagement, with what is alike and why).
  2. **With none of the three, the cell reads `ORDER OF MAGNITUDE UNAVAILABLE — <what is missing to
     produce it>`.** A declared empty field is worth more than a number with no basis, and inventing
     one breaks the hard rule the whole framework rests on.
  3. **It is a band, never a point**, and never a quantile — the sources carry rates and buffers, not
     a distribution. A band does not become a delivery commitment by crossing into `estimate`.
  4. **`PACK MODEL` carries its asymmetry statement**: the pack's model is platform-side only, so the
     band exists for that candidate and no equivalent was computed for the others. The absence of a
     comparator number is not evidence that an alternative is cheaper or dearer, and a number beside a
     blank must not be read as the better option.
  These four markers are a closed set and are written **verbatim, never translated** — like
  `COMPARATOR EVIDENCE ABSENT`. A translated marker makes a check pass on a broken file.
- **The technology column is mandatory and is never empty.** A platform candidate names its **form
  in products** — surface *and* store, per the pack's alternatives register (`ALT-004` §1.2, e.g.
  *record-centric app + governed store* · *canvas app + the existing relational database*). *"This
  platform"* alone, or a store with no surface named, is **malformed**: the phase exists to put the
  named choice on the table. A non-technology candidate writes what it is instead (*process change*,
  *do nothing*); a class nobody evaluated writes *not assessed*.
- **One option per form.** Two platform forms differing in surface or in store are **two rows and
  two entries**, with their own verdicts, effort drivers and reversibility. Collapsing them is the
  same defect as collapsing two scopes into one outcome.
- **Do-nothing and process change are conditional, and their absence is declared — never silent.**
  Each enters the set when discovery showed it plausible, generated with the candidate set and never
  appended here. Where one did not enter, the round's log records why, with ids (`Class coverage`,
  Step 7). An unexplained absence is the defect; a reasoned absence is a finding.
  Plus the platform forms the solution-architect generated. If the architect returned no form-level
  candidate for a platform class it put on the table → say so in `Summary` and raise it as an open
  question; do not name a form the architect did not name.
- **A declared imposed technology is the boundary the set is generated inside, not a candidate to
  argue with.** Where the engagement records the platform as a fixed constraint, every option is a
  pattern compatible with it — plus, where the organisation permits the boundary, external components.
  **No option proposes changing platform, and no recommendation does.** The imposition is itself an
  organisational rule, so a platform alternative may appear **only** as *viable if the rule is changed*
  with that verdict's full field set — never as a plain candidate and never as the recommendation.
- **An organisational rule blocks an option; it never deletes it.** Where an existing rule of the
  organisation makes an option unavailable, the option stays in the set with the verdict *viable if
  the rule is changed* and its seven fields (rule with id · condition · impact · cost · risk · who can
  change it · status). Whether to change the rule is the owner's decision at `/decide`, and it cannot
  be taken about an option nobody was shown.
- **One outcome per scope, not per engagement.** Render *(scope, outcome)* pairs and never collapse
  them — collapsing is how a bounded exclusion becomes a whole-solution rejection.
- **`(none)` is not written here; the field is omitted.** The explicit `(none)` obligation lives in
  the audit log's long form, which is what makes an empty field distinguishable from an unevaluated
  one. Omitting a field in the artefact is legitimate **only** because the log carries it — if the
  log does not, the field belongs here.
- **No score, no weight, no ordinal ladder** (`forte`/`adequada`/…) anywhere in this file, and the
  table's order is the id order.
- **No internal framework vocabulary.** Exit-class codes, outcome class numbers, depth codes,
  subtype codes and register ids stay in the pack. Plain language only — **and that rule governs the
  framework's vocabulary, never the product's.** Vendor and product names are *mandatory* in this
  artefact: paraphrasing a form into *"this platform over the store that already runs"* is not plain
  language, it is the option withholding its identity. Name the products; keep the codes out.
- **No unsupported comparative claim** — *better*, *cheaper*, *faster*, *easier*, *more scalable*,
  *lower TCO* — about any candidate.
  Being able to exclude one option does not prove another is superior. Where no comparative evidence
  exists, `COMPARATOR EVIDENCE ABSENT` is part of the sentence, not a footnote. The *Decides against
  the others* field exists **only** where the comparator separation returned a discriminating
  signal, and is omitted otherwise.
- Where the round terminates in *decision blocked*, name the evidence, its expected form, the likely
  role type, and **what each resolution would produce** — in `Recommendation`, once.

### Step 7 — Write the synthesis audit log

Write `<engagement>/lens-outputs/chairman-synthesis-<round>.md` (e.g., `chairman-synthesis-F-01.md`):

```markdown
# Chairman Synthesis — Round <round> / Phase <phase>

## Personas heard
- <comma-separated list of persona names that returned>

## Overlaps → strengthened
- "<claim>" — anchored by <personas> → <SU id> (<state>)

## Gaps → carried as Assumed/Unknown
- "<claim>" — proposed by <persona> only → <SU id> (<state>)

## Contradictions → Conflicted
- "<conflict>" — <persona∧persona> → <X-NNN>

## Admissão de perguntas (P-26)
<One line per candidate `Unknown` this round — written, downgraded or not written (Step 4b). Empty only
when no persona raised an open question at all; "none missing" is written as such, never by omission.>
- <U-NNN | "<persona question text>"> — <admitida | `cosmético`: sem eixo técnico declarado | não escrita: sem 2ª resposta | não escrita: pergunta de pessoa ou de papel (P-21)> — eixo: <o eixo técnico, ou —>

## Risks captured
- <R-NNN> — <one-line>

## SU rows written this round
- <SU id> — <one-line>
- …

## Phase artefact written
- `<frame.md | options.md | decisions.md draft>` — <one-line summary>

## Class coverage — round <round>   [Options only]
<Exactly two lines, one per conditional option class. The marker is verbatim and never translated —
it is what a check can read on an artefact written in the pack's language.>
- `DO-NOTHING` — <O-NNN, the candidate that carries it | `NOT PLAUSIBLE`: <why, with SU ids>>
- `PROCESS-CHANGE` — <O-NNN, the candidate that carries it | `NOT PLAUSIBLE`: <why, with SU ids>>

## Concern coverage — round <round>   [Options only]
<One line per material decision concern: the depth used per option, or "not material — <the evidence
that makes it so>". Twelve lines. This is what makes coverage auditable without a matrix —
do NOT render a 12×N grid, and do NOT put these lines in `options.md`.>

## Per-option long form   [Options only]
<The complete `decision-tree.md` §14.1 field set for every candidate — anchored by · viability ·
outcome · material strengths · disqualifiers with scope and evidence grade · preconditions
(condition — owner — funded? — by when) · material trade-offs · material risks · economic
implications · decision-changing uncertainties · proof requirement · concern notes. **`(none)` is
written explicitly here** — this is the record that makes an omitted field in `options.md` mean
*evaluated and empty* rather than *never evaluated*. For a platform candidate, the entry is headed
by its **form in products** (surface + store), one entry per form.>

### <O-NNN> — <name>   ·   <option class>   ·   <technology: the form in products>
- **Anchored by**: <personas — solution-architect always for technology options>
- **Scope**: <whole solution | the named responsibility>   ·   renders as `scope: <…>`
- **Viability**: viable | viable with preconditions | disqualified (settled) | disqualified (provisional — rests on assumption <SU id>) | not assessable (evidence)
- **Outcome**: <the outcome, in its render template from the pack's outcome register. An economic outcome states explicitly whether it is economically **infeasible** or economically **unattractive** — never the disjunction where the evidence supports one.>
- **High-level architecture**: <the main components, and per component whether it falls inside or outside the responsibility boundary — what this team builds and operates versus what another team, the platform or a third party does. High level only: the detailed architecture belongs to the chosen option, after the decision.> | (none)
- **Assumptions**: <what the option rests on that is not Confirmed, by SU id — an expired or weak `Assumed` named as such> | (none)
- **Order of magnitude**: <band · `SIMULATED` | `PACK MODEL` | `ANALOGY` — or `ORDER OF MAGNITUDE UNAVAILABLE — <what is missing>`. Never a point, never a quantile; `PACK MODEL` carries its asymmetry statement. The method is in the artefact template above and is not restated here.>
- **Material strengths**: <evidence-anchored; no comparative adjectives> | (none)
- **Disqualifiers**: <what it fails, at what scope, plus the SU anchor and whether the evidence is confirmed-and-current or an unverified assumption> | (none)
- **Preconditions**: <condition — role or source — funded? — by when. A precondition is a role, an operation, a mechanism or a piece of evidence — **never a person** (P-21).> | (none)
- **Material trade-offs**: <consciously acceptable disadvantages> | (none)
- **Material risks**: <impact + proposed mitigation → SU Risky rows> | (none)
- **Cost drivers**: <which of the pack's cost dimensions move for this option, and in which direction> | (none)
- **Reversibility**: <high · medium · low — and what makes it so: migration cost, lock-in, data export> 
- **Revision condition**: <what would make this option worth reopening after a decision — the metric, the date or the event, as a tripwire candidate> | (none)
- **Decision-changing uncertainties**: <SU id — what it would change — cost to close> | (none)
- **Proof requirement**: <published-limit arithmetic | bounded pilot | engineered test harness | production-like proof> — funded? | (none)
- **Concern notes**: <the assessment that decided something> | (none)

## Parser warnings (if any)
- <persona> output: <what was malformed>
```

**The log is written before the artefact is compressed, not after.** `options.md` is a projection of
this record: every claim it carries traces to a field here, and nothing material is dropped on the way
— it is relocated. `/simulate`, `/premortem` and `/decide` read the table and the entries in
`options.md`; where one of them needs a field the artefact omitted, it reads this log.

### Step 8 — Update state and log

1. Update `_state.json.round` to the current round (atomically). For Framing rounds use the `F-NN` form, Options `O-NN`; the calling skill (`aisa-frame` / `aisa-options`) is responsible for the prefix, but if you find the prefix already correct in `_state.json`, leave it alone.
2. Append a one-line summary to `<engagement>/council-log.md`: round, `agent: chairman`, what was produced.
3. Return control to the calling skill with: "Chairman synthesis complete for `<phase>` round `<round>`. Wrote `<N>` SU rows; phase artefact `<frame.md | options.md | decisions.md draft>`."
