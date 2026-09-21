# Step 7 — Final Pack Integrity / Consistency Gate

> Report path note: this repository's authoring root is `docs/pp-pack-authoring/`, so the
> canonical `research/pp/authoring/` location resolves to
> `docs/pp-pack-authoring/research/pp/authoring/`. Same tree as every prior step report.

**Verdict: `STEP 7 — FINAL PACK INTEGRITY / CONSISTENCY GATE: FAIL`**

One material defect class survives: the runtime still **actively manufactures** retired
decision/architecture vocabulary through the Options artefact writer and the standing memory of
the Options evaluator. Everything else in §63 passes. The defect is bounded, its repair is
serialization-only, and no frozen semantic layer is implicated.

---

## 1. Gate basis

| | |
|---|---|
| Gate scope | `.claude/`, `library/kernel/`, `library/packs/pp/`, `docs/` |
| Historical / audit evidence (not swept for stale vocabulary) | `docs/pp-pack-authoring/**` |
| Runtime modified during the initial gate | **NO** — one new test module + this report only |
| New research performed | **NO** |
| Web access used | **NO** |
| Canonical research modified | **NO** |
| Model knowledge used to fill a gap | **NO** |
| Steps 3–6 reopened | **NO** |

### 1.1 Step 6 freeze — recorded, not rewritten

The Step 6C audit trail already reads, and stands unaltered:

```text
STEP 6C INITIAL GATE: FAIL
→ bounded repair
→ targeted re-gate: PASS
→ STEP 6 FROZEN
```

Authoritative final repair state:

```text
INITIAL SEMANTIC DEFECTS: 2
REMAINING SEMANTIC DEFECTS: 0
TARGETED RE-GATE FAILURES: 0
STEP 6 — DELIVERABLE TEMPLATES: FROZEN
```

No runtime modification belongs to that marker.

### 1.2 Governing integrity chain under test

```text
ENGAGEMENT EVIDENCE → SHARED UNDERSTANDING → OPTIONS / DECISION → ARCHITECTURE ENTRY
  → DOMAIN KNOWLEDGE (pulled only where needed) → ARCHITECTURE → DELIVERABLE PROJECTIONS
```

Allowed feedback: *downstream unresolved material issue → open work / evidence obligation →
upstream authority resolves it.* Forbidden: *downstream layer silently re-reasons upstream and
replaces its authority.*

---

## 2. Frozen-state inventory

| Layer | Frozen at | Filesystem evidence |
|---|---|---|
| Step 2 — Discovery | complete | `glossary.md` 165 L · `question-bank.md` 246 L · `pack.yaml lenses_config` |
| Simplification A–G | complete | phase reports 2026-09-03 23:41 → 2026-09-04 01:32 |
| Step 3 — Options | frozen | `decision-model/` written 2026-09-04 02:30 |
| Step 4 — Domain Knowledge | frozen | **all 26 units share mtime 2026-09-04 10:18:07** |
| Step 5 — Architecture | frozen | `architecture-templates/` 12:14 → 12:23 |
| Step 6 — Deliverables | frozen | `deliverable-templates/` 16:10 → 17:33 (incl. 6C repair) |

---

## 3. Active runtime inventory

### 3.1 PP pack — 47 files (excluding `.gitkeep`)

| Group | Count | Files |
|---|---:|---|
| Manifest | 1 | `pack.yaml` (`pack_version: 1.8.0`) |
| Discovery | 2 | `glossary.md`, `question-bank.md` |
| Options / Decision | 6 | `decision-tree.md` + `decision-model/{alternatives-register, blocking-set, composed-disqualifiers, outcome-classes, volatility-register}.md` |
| Domain Knowledge | 26 | 1 README + **15 RESEARCH** + **10 CRAFT** |
| Architecture | 6 | **5 runtime units** + 1 positioning README |
| Deliverables | 6 | the six canonical projection contracts |

### 3.2 Counts against the expected frozen taxonomy

| Expected | Actual | |
|---|---:|:--:|
| RESEARCH units | 15 | ✅ |
| CRAFT units | 10 | ✅ |
| Domain-knowledge README | 1 | ✅ |
| Architecture runtime units | 5 | ✅ |
| Architecture README positioning | 1 | ✅ |
| Canonical deliverable contracts | 6 | ✅ |
| ALT option classes | 11 | ✅ |
| Outcome classes | 14 | ✅ |
| Material decision concerns | 12 | ✅ |
| Ordered stages S0–S9 | 10 | ✅ |
| Volatility rows | 39 `VS` + 10 `VC` = 49 | ✅ |

Counts taken from the filesystem and the parsed manifest, not from prior reports.

### 3.3 Kernel / runtime surfaces

`orchestration.md` · `phases.md` · `states.md` · `render-contract.md` · `blueprint-contract.md` ·
`glossary.md` · 5 synthesis templates · 1 capture template · 4 tool modules.
`.claude/`: 23 skills · 8 agents · 17 commands · 8 hooks · 4 rules · 21 agent-memory files ·
9 test modules.

---

## 4. Manifest integrity

```text
MANIFEST TARGETS: 40
RESOLVED:         40
MISSING:           0
DUPLICATE PATHS:   0
ORPHAN TARGETS:    0
pack_version:  1.8.0   (NOT bumped during the initial gate)
```

| Check | Result |
|---|---|
| Every referenced file exists | ✅ 40/40 |
| Every required runtime unit reachable | ✅ (see note) |
| Retired file referenced | ✅ none |
| Duplicate path | ✅ none |
| Dynamic branch mapping | ✅ none — every `template:` is a literal path |
| Outcome → template router | ✅ none |
| Product → template router | ✅ none |
| Hidden domain-knowledge preload list | ✅ none — `domain_knowledge:` is declared "a MANIFEST … NOT a load order, NOT a routing table, NOT a concern map" |
| Deliverable metadata matches the six contracts | ✅ `canonical_deliverable` in manifest == template frontmatter, 6/6 |

**Note — architecture templates are deliberately unmanifested.** The 6 files under
`architecture-templates/` are the only pack files no manifest key names. This is by design and is
recorded in `pack.yaml` (1.7.0 note): the entry point is **fixed**, so there is nothing to select
and nothing to route. They are reached by literal path from `aisa-blueprint`, `aisa-render`,
`aisa-synthesize`, `render-contract.md` and `architecture-story.template.md` — all four paths
resolve. Classified **legitimate pull-only asset**, not an orphan.

`applies_to` no longer exists as a key on any deliverable; it survives only in the manifest's own
prose recording that it was *replaced* by `activation`.

---

## 5. Stale-vocabulary sweep

### 5.1 Retired architecture model (§5)

Tokens swept: `sharepoint-first`, `dataverse-first`, `chosen_architecture`,
`architecture-templates/<branch>`, `architecture-templates/{{chosen_architecture}}`,
`Branch (if technology)`, `technology branch`, `branch score`, `three-branch`.
Plain-English "branch" was deliberately excluded — the runtime legitimately says *"no branch"*.

| Location | Reading | Verdict |
|---|---|---|
| `.claude/tests/*` | negative assertions | legitimate guard |
| `library/packs/pp/architecture-templates/README.md` §11 | documents the retirement + read-compatibility mapping | legitimate |
| `library/packs/pp/decision-tree.md:21` | *"It replaces the scored three-branch tree"* | legitimate negation |
| `.claude/skills/aisa-decide/SKILL.md:158` | *"is **removed**"* | legitimate negation |
| **`.claude/agents/chairman.md:82`** | **emits `Branch (if technology)` into `options.md`** | **DEFECT — see §6** |
| **`.claude/agent-memory/_universal/solution-architect/universal-constraints.md`** | **instructs "branch shortlisting"** | **DEFECT** |
| **`.claude/agent-memory/_universal/solution-architect/diary.md`** | **narrates `sharepoint-first` / `dataverse-first` / `R0–R6`** | **DEFECT** |
| `docs/{ARCHITECTURE,GAP_ANALYSIS,IMPLEMENTATION_PLAN,LIVE_VALIDATION_REPORT,MIGRATION_FROM_AISA,UX_BLUEPRINT_PROPOSAL,DELIVERABLE_AUTHORING}.md` | historical planning / analysis records | documentation-only (§23) |

```text
ACTIVE RETIRED ARCHITECTURE MODEL REFERENCES: 3
```

### 5.2 No stale vocabulary in the frozen layers

Zero retired tokens in `library/packs/pp/` (outside the README's retirement section), zero in
`library/kernel/`, zero in the six deliverable contracts, zero in the five architecture units,
zero in the 26 domain-knowledge units.

---

## 6. Chairman carry-forward — adjudication (§6)

### 6.1 The finding

`.claude/agents/chairman.md` §"Phase artefact specifications → Options" carries a **complete
second copy** of the `options.md` artefact spec:

```markdown
### O-001 — <option name>
- **Branch (if technology)**: <from decision-tree.md, or "non-technology" / "do-nothing">
- **Pros**: … - **Cons**: … - **Constraints checked**: …
- **Reversibility**: <Low|Medium|High>  - **Indicative effort band**: <Small|Medium|Large>
```

The current, Step-3-aligned spec for the **same artefact** lives in
`.claude/skills/chairman-synthesis/SKILL.md` §"Options → `options.md`" and is clean:

```markdown
### O-001 — <option name> · <option class> · scope: <whole solution | named responsibility>
- **Viability**: viable | viable with preconditions | disqualified (settled) | …
- **Outcome**: <render template from the pack's outcome register>
- **Disqualifiers** / **Preconditions** / **Proof requirement** / …
## Concern coverage — round O-<NN>      ## Comparator status
```

### 6.2 Case A or Case B

**Case B — ACTIVE serialization.** Three reasons:

1. The chairman agent is the writer of `options.md` in council-independent mode
   (`aisa-options` §6 → `chairman.md` mandate: *"Write the phase artefact … Options → `options.md`"*).
   The stale template is inside its own agent definition, i.e. its system prompt.
2. The field is not inert: it names a **source** — `<from decision-tree.md>` — for a value
   `decision-tree.md` no longer defines. A new engagement asked to populate it must invent one.
3. The stale copy is not merely one extra field; it **omits** the entire Step 3 option shape —
   option class, scope, viability, outcome class, disqualifier evidence grade, preconditions,
   proof requirement, concern coverage and comparator status. An Options round serialized through
   it would emit no `(scope, outcome)` pairs, which is precisely what `/decide`, `/blueprint`
   and the Executive Report read.

This is therefore a **Step 7 defect**, and additionally a **duplicate-authority defect**: two
active runtime files specify the same artefact, and they disagree.

```text
CHAIRMAN LEGACY BRANCH SERIALIZATION: ACTIVE
```

### 6.3 Bounded repair recommended (NOT applied during the gate)

Replace `.claude/agents/chairman.md` §"Phase artefact specifications" with a **pointer** to
`.claude/skills/chairman-synthesis/SKILL.md`, so exactly one file specifies each artefact.
Serialization-only. Touches no Step 3 semantics, no decision logic, no register, no stage.
`test_pp_pack_integrity.P02.test_chairman_carry_forward_is_pinned_and_isolated` currently pins the
defect and inverts the moment the repair lands.

---

## 7. Discovery integrity

| Check | Result |
|---|---|
| 6 Discovery lenses technology-neutral | ✅ zero vendor/product tokens in the six lens SKILL files |
| PP product/service signals in `extra_signals` | ✅ none — all 34 cues are neutral (`work_shape_class`, `authorization_enforcement_point`, …) |
| Architecture pattern prompts in Discovery | ✅ none |
| Option-class leakage | ✅ none |
| Domain-knowledge preload in Discovery | ✅ none — `aisa-round` §38 forbids dumping `pack.yaml`, `question-bank.md` or DK into a lens invocation |
| `lens-technology` Options-only, pull-based | ✅ declared in the skill, the agent, `pack.yaml` and `decision-tree.md` §1 |
| Question bank | ✅ **one** consumer: `aisa-status` step 6 (`aisa-round` §54: *"Its single consumer is `aisa-status` step 6"*; `orchestration.md:105` concurs) |
| Signals = attention cues | ✅ no coverage score, no completion %, no per-signal question rule; `orchestration.md:80` explicitly forbids converting signals into checklist coverage |

`library/packs/pp/glossary.md` and `question-bank.md` carry "Power Platform Pack" in their titles.
Neither is injected into a lens; the glossary excludes product definitions by rule (§133: *"Product
definitions … belong to the Options vocabulary and are not authored here"*).

```text
DISCOVERY TECHNOLOGY NEUTRALITY: PASS
```

---

## 8. Decision integrity

### 8.1 Structural invariants (§13)

| Invariant | Verified |
|---|---|
| 11 canonical ALT classes | ✅ `ALT-001…ALT-011` |
| 14 outcome classes | ✅ §1 "The fourteen classes" |
| 12 canonical concerns | ✅ `C1…C12` |
| 10 ordered stages | ✅ `S0…S9`, order declared non-commutative |
| No scoring | ✅ *"States, not scores… no numeric fit score, no weight, no aggregated verdict, no ordinal ladder … at any point"* |
| `ALT-002` / `ALT-010` baseline rule | ✅ *"members of every candidate set … never eliminated by a platform disqualifier"* |
| Hard-disqualifier evidence semantics | ✅ §4 binding rule + the five-row evidence-grade table |
| `Assumed` never settles exclusion | ✅ §4 + `outcome-classes.md` §1.1 (classes 5, 6, 7, 9, 14) |
| Class 12 semantics | ✅ per-resolution outcome mandatory |
| Class 13(a) semantics | ✅ two forms that never merge; comparative clause scoped to the entitlement fact; graduation trigger mandatory in both |
| Class 6 scope-pair semantics | ✅ *"may remain the correct answer for the surrounding scope — and the outcome **must say so**"* |
| Technology lens = evaluator, not decider | ✅ `/decide` is user-driven; no council runs in Decision |

T01–T18 not replayed: no structural contradiction was found (§57).

### 8.2 Old Options-model vocabulary (§7)

Swept: `R0…R6`, scored PP tree, deleted thresholds as decision rules, scored recommendation
language, architecture product choice encoded in Options.

Every hit in `library/`, `.claude/skills/` and `.claude/agents/` is a **prohibition**
(`no scoring`, `never a score`, `no ranking engine`, `replaces the scored three-branch tree`).

Two active semantic uses, both in the standing memory of the Options evaluator:

- `solution-architect/universal-constraints.md`: *"`decision-tree.md` is the gating logic for
  **branch shortlisting**. Skipping it lets vibes pick a **branch**."* — instructs a procedure
  the spine no longer has. Also *"walk every constraint and produce a verdict: pass / risky /
  blocker"*, a parallel ordinal vocabulary that maps onto none of the seven §3 decision-semantics
  terms, while `pack.yaml` declares `constraints_to_check` a *"standing-attention floor … never
  the coverage object"*.
- `solution-architect/diary.md`: *"sharepoint-first caiu no gate **R0** … dataverse-first venceu
  **R0–R6**"* — the retired scored-gate model presented to the persona as its own experience, and
  the agent is instructed to cite diary patterns (`solution-architect.md:34`).

```text
ACTIVE OLD SCORED/BRANCH DECISION SEMANTICS: 3
```

---

## 9. Domain Knowledge integrity

### 9.1 Taxonomy (§19)

Filesystem == manifest, exactly. 15 RESEARCH · 10 CRAFT · 1 README · **0 unexpected files**.
No resurrected flat legacy unit (`azure-sql-reference.md`, `delegation-matrix.md`,
`powerfx-patterns.md`, … all absent). No `azure-sql-first`-style decision file. No
alternative/vendor comparator file. No anti-pattern encyclopedia. No agent file.

### 9.2 Decision-leakage (§20)

Zero option-winner, selected-option, outcome-assignment, stage-exit, scoring, comparator-preference
or "should choose" semantics in any of the 25 units. The README states the boundary structurally:

```text
decision model   → decides what question needs answering   (decision-tree.md + decision-model/)
domain knowledge → provides the technical knowledge to answer it   (this directory)
```

### 9.3 CRAFT authority (§21)

All 10 CRAFT units carry, verbatim: `class: CRAFT` · *"No independent research authority"* ·
*"must not state a platform limit, threshold or comparative claim as fact; where one is required it
refers to the RESEARCH unit that owns it"* · *"Not an Options D3 pull target"*.
`aisa-blueprint` reinforces it at the consumer: *"`data/query-and-delegation.md` … is the platform
authority for what delegates and what silently truncates; the `craft/` files never restate it."*

```text
CRAFT AUTHORITY LEAK DETECTED: NO
```

### 9.4 Pull integrity (§22)

Actual active consumer graph:

| Consumer | Pull discipline declared |
|---|---|
| `lens-technology` / `solution-architect` | selective; *"Never load the domain-knowledge base by default; never preload a register"* |
| `aisa-blueprint` | *"Median 1 unit per section, maximum 2"*; forbids knowledge bundles and surveying `patterns.md` §5 in full |
| `architecture-core.md` | *"Never preload the units, never assemble an architecture knowledge bundle, never survey all ten"* |
| `aisa-render` | *"at its point of need (never a preload, never a catalogue scan)"* |
| `aisa-synthesize` | *"No Domain Knowledge pulls for prose"* |
| Deliverable contracts | 4 of 6 name the catalogue in `forbidden_sources`; the other 2 declare *selective* units only |

No preload, no concern matrix, no architecture bundle, no whole-catalogue scan.

```text
DOMAIN KNOWLEDGE PRELOAD DETECTED: NO
```

### 9.5 Research-gap annex (§25) and agent/conversational gaps (§26)

`G001…G120` have **zero active runtime consumers** — the only references are inside
`test_pp_domain_knowledge.py`, which reads the *authoring* annex to assert it stays authoring-side.
The gap annex is not a routing table, a research queue, a default blocker or a runtime checklist.

G118 / G119 remain authoring-side research candidates, and the runtime handles the shape they
cover correctly rather than inventing knowledge — `alternatives-register.md` row 29:

> *Conversational or agent-shaped interaction* → **none evaluable.** Fit is `UNKNOWN` in **every**
> class, `ALT-004` included. The correct output is **decision blocked**, not a candidate set.

No fabricated entitlement, security or licensing semantics were found.

```text
RUNTIME RESEARCH-GAP ANNEX CONSUMER EXISTS: NO
```

---

## 10. Volatility and provenance

### 10.1 Volatility (§23)

`decision-model/volatility-register.md` remains the volatility authority: **49 rows**
(39 `VS` + 10 `VC`), consulted on demand only, *"NOT loaded at the start of Options and NEVER read
as a standing checklist"*, and it **supplies no figures** — it supplies re-verification triggers.
The governing rule is intact:

```text
stable decision principle → decision logic     (decision-tree.md)
volatile platform fact    → evidence           (domain knowledge + the engagement's own row)
```

No current fact was converted into a stable principle: every numeric platform reading in the
RESEARCH units is stamped and pointed at its row —
`Documented reading · read 2026-09-04 · re-verify: VS-03 (design time, and on any licence change)`.
Rows unchanged by this gate.

### 10.2 Provenance (§24)

Git cannot prove byte identity here: the whole Step 1–7 body of work is uncommitted working tree
(`git status`: 97 entries, `HEAD` predates Step 3). The evidence that **does** prove the Step 4
freeze survived Steps 5 and 6:

1. **Filesystem mtimes.** All 26 domain-knowledge units carry the identical write timestamp
   `2026-09-04 10:18:07` — a single Step 4B write. The architecture layer was written at
   12:14–12:23, the deliverables at 16:10–17:33. No Step 5 or Step 6 write touched a knowledge unit.
2. **Step 6B's own declaration**: *"Not modified, deliberately: Step 3 registers · Step 4 knowledge
   units · all Step 5 architecture runtime."*
3. **Step 4 regression**: 64 tests green, including the provenance-header and taxonomy assertions.

No later change created a new decision-grade factual claim inside Domain Knowledge.

**One provenance observation.** `decision-tree.md` carries mtime `15:41`, after the Step 5C gate
(14:59) and inside the Step 6A window — while Step 6B's file list declares Step 3 registers
untouched. mtime alone cannot distinguish a content change from a re-save, and no commit boundary
exists to diff against. What *is* provable: every Step 3 structural invariant in §8.1 holds, and
the 95-test Step 3 suite passes. Recorded as an evidence limitation, not a defect.

```text
VOLATILITY / PROVENANCE INTEGRITY: PASS
```

---

## 11. Architecture integrity

### 11.1 Decision → Architecture entry (§14)

```text
architecture authorization = outcome reachability × active-pack architectability
```

Single home: `architecture-templates/README.md` §2–§4. `aisa-blueprint` step 1 runs both factors
mechanically (1a read pairs → 1b reachability → 1c architectability → 1d initialize), and states
*"Reachability alone is **never sufficient**"*. `render-contract.md` carries the discriminator in
the same shape: *"A positive outcome over a solution the active pack cannot architect authorizes no
architecture."*

Searched for the bypass shape *positive outcome → render PP architecture* without architectability:

```text
ARCHITECTURE AUTHORIZATION BYPASS FOUND: NO   (0 instances)
```

### 11.2 Authority ownership (§15)

`aisa-decide` **Must NEVER emit**: `architecture.authorization`, `architectability_basis`,
experience mode / primary surface, composition selection, record authority, architecture-template
selection. `/blueprint` owns the mechanical entry initialization; after it, the value is *"read,
never derived, upgraded or downgraded"*. No Step 3 semantic drift.

### 11.3 Composition (§17)

```text
architecture-core + 0..1 experience fragment + 0..N boundary/import fragments
```

No product-specific template, no pattern-specific template, no hidden headless template, no
whole-architecture shape enum. Component identity `<scope>::component::<component>` with
`component` unique within scope; responsibility identity is the responsibility name, unique within
scope — collision-safe.

### 11.4 Headless (§16)

`experience.mode: none` is a first-class **finalized architectural fact**: zero experience
fragments, `primary_surface: null`, no A4, no `surface unresolved`, no missing-template warning,
no render gap — logged as a `not applicable` skip with its reason. `fragment-experience-none.md`
intentionally does not exist and both `aisa-blueprint` and `architecture-core.md` say so. The
Specification forbids *"inventing a user surface where experience.mode == none"* while still
projecting automation, integration, identity, environments, monitoring, recovery, proof work and
operator obligations **in full**. No architecture/application synonym assumption survives.

```text
HEADLESS END-TO-END INTEGRITY: PASS
```

### 11.5 Imported obligations (§18)

`fragment-boundary-and-imports.md` retains all six channels — Governance · ALM · Cost ·
Monitoring · Recovery · Operator — instantiated once per qualifying component and once per
relocated responsibility (N + M instances). No Step 6 change caused a consumer to bypass or drop
them; architecture owns them and no deliverable is required to repeat them.

---

## 12. Deliverable integrity

### 12.1 The six projection contracts (§28)

| # | Canonical | Runtime id | Template |
|---:|---|---|---|
| 1 | discovery-report | `discovery-report` | `discovery-report.template.md` |
| 2 | executive-report | `executive-report` | `executive-report.template.md` |
| 3 | architecture-blueprint | `solution-blueprint` (alias) | `solution-blueprint.template.md` |
| 4 | implementation-specification | `implementation-spec` | `implementation-spec.template.md` |
| 5 | claude-design-brief | `claude-design-brief` | `claude-design-brief.template.md` |
| 6 | estimate | `estimate` | `estimate.template.md` |

No seventh deliverable · no duplicate canonical name · no obsolete dynamic sub-template.

### 12.2 Applicability (§29)

`aisa-render` declares a six-row applicability **table**, not a router or a state machine, and it
matches the expected chain exactly for PP authorized · authorized-bounded · not-authorized ·
Decision Blocked · headless · structural open choice (Blueprint producible but unapproved; Spec +
Design Brief blocked; candidate Estimate only under Mode B).

### 12.3 Architecture → Deliverable (§27)

No deliverable independently selects experience, store or composition, infers the far side, or
derives authorization. Blueprint / Spec / Design Brief / Estimate all take the **recorded**
architecture block as authority; `solution-blueprint.template.md` states *"lidos do registo —
nunca derivados, escolhidos, pontuados"*.

### 12.4 Build gates — F-1 repair survived (§30)

`non_omissible:` block present, carrying build-gating conditions, preconditions, proof obligations
and open work items. The three are declared **THREE DISTINCT THINGS**; *"A condition with an owner,
a funding state and a due date is NOT an open work item"*. Forbidden transformations include
*"dropping, compressing away or re-labelling a build-gating condition or a precondition"*,
*"rendering a build gate as satisfied without recorded engagement evidence"* and
*"marking a proof obligation satisfied"*.

```text
BUILD-GATE GUARD PRESENT: YES
```

### 12.5 Estimate → Executive payload — F-2 repair survived (§31)

Allowed: base effort · range · contingency-inclusive **total** · confidence.
Explicitly forbidden and named in the contract: `phases` · work breakdown · `team_mix` ·
`contingency_rate_or_derivation` · effort arithmetic · `duration_or_calendar_schedule` ·
candidate inventories · detailed uncertainty inventory · blending candidates into one headline.
`render-contract.md`: *"The Executive Report never becomes a second Estimate authority."*

```text
ESTIMATE→EXECUTIVE PAYLOAD GUARD PRESENT: YES
```

### 12.6 Estimate ownership (§32) and the S8 boundary (§33)

Exactly two input modes. Mode A: Specification inventory, *"MAY NOT ADD A WORK UNIT ABSENT FROM
THAT SPECIFICATION"* — an absent unit is an OPEN WORK ITEM against the Spec. Mode B: candidate
planning, *"no spec != permission to invent a spec"*, per-candidate isolation, *"NEVER blend …
NEVER select … NEVER rank"*. `owns_calculation: true` on the Estimate and on nothing else;
`aisa-render` executes; synthesis computes zero implementation effort (`financial-story.template.md`:
*"NO effort figure, NO phase plan, NO duration derived here"*).

S8 ↔ Estimate separation holds in **both** directions: the Estimate forbids *"settling economic
attractiveness (that is S8, at decision altitude)"* and forbids `options.md` S8 as an input or
output; `aisa-render`: *"The Estimate never decides whether this platform is cheaper or more
attractive."* Reverse inferences searched (`low person-days → attractive`, `high → should have
lost`): **0**.

### 12.7 Synthesis boundary (§34)

`architecture-story` carries the `not-authorized` architectability basis as **durable carrier
only** — never authority. `financial-story` is decision economics only, split from implementation
effort in Step 6B. `as-is` is named in the Estimate's `forbidden_sources` with the explicit note
*"NOT required, NOT conditional, NOT fallback, NOT point-of-need"*. `risks-and-assumptions` is a
carrier that does not alter epistemics. No topic pack may create a comparison, ranking, score or
superiority claim.

```text
DELIVERABLE PROJECTION INTEGRITY: PASS
```

---

## 13. Cross-layer source-owner graph (§36)

| Information class | Semantic owner | Durable carrier (where different) | Permitted downstream projection |
|---|---|---|---|
| Engagement fact | `shared-understanding.md` | `_capture/` normalized evidence | Discovery Report; cited by any layer |
| Epistemic state (5 states) | `shared-understanding.md` (`library/kernel/states.md`) | — | display only; never re-graded |
| Decision | `decisions.md# D-NNN` | — | Executive; architecture entry inputs |
| Condition / precondition | `decisions.md# Conditions/Preconditions` | Implementation Spec *Build gates* | rendered with owner · funded? · by when · what it gates; never as satisfied |
| Risk acceptance | `decisions.md# Accepted risks` | `_synthesis/risks-and-assumptions.md` | Executive; Estimate uncertainty naming |
| Option comparison | `options.md` (S9) | `_synthesis/` narratives | Executive — **as recorded**; no new comparison |
| Comparator marker | `decision-model/outcome-classes.md` §4 | the outcome sentence itself | carried verbatim; never closed downstream |
| Architecture authorization | `/blueprint` entry gate (reachability × architectability) | the `architecture:` block | read; never derived, upgraded, downgraded |
| Architectability basis | `/blueprint` step 1d | `architecture-story.md`; Executive | one sentence, carried |
| Architecture component | the `architecture:` block | `architecture-core.md` + fragments | Blueprint; Spec work packages |
| Imported obligation | `fragment-boundary-and-imports.md` (6 channels) | the architecture record | Spec; Blueprint |
| Proof obligation | `decision-tree.md` §12 → the `architecture:` block | Spec work package + acceptance condition | never re-graded (V1–V4, method, owner, funded) |
| Implementation work | Implementation Specification | — | Estimate — **inventory only** |
| UX constraint | approved `ux-blueprint_v<NN>.yaml` | — | Claude Design Brief |
| Effort estimate | Estimate (`owns_calculation: true`) | — | Executive — bounded headline only |

Exactly one semantic owner per class.

---

## 14. Deliverable read-edge graph (§35)

```text
Implementation Specification ──inventory only──▶ Estimate
Estimate ──bounded headline only──▶ Executive Report
```

No third edge exists. Every other cross-deliverable read is declared **forbidden**:

- Discovery Report forbids `_render/*` and *"another deliverable's narrative as authority"*.
- Architecture Blueprint forbids `_render/<slug>_estimate_v<NN>.md`.
- Implementation Spec forbids `_render/<slug>_estimate_v<NN>.md` — *"the Estimate reads THIS, not the reverse"*.
- Claude Design Brief forbids **both** rendered Blueprint and rendered Spec as UX authority.
- Executive forbids every `_render/` file **except** the Estimate headline.

```text
DELIVERABLE-TO-DELIVERABLE READ EDGES: 2/2
```

---

## 15. Cycle detection (§37)

Active authority graph (edges taken from declared source contracts, not inferred), DFS-verified
acyclic in `P16NoAuthorityCycles`:

```text
shared-understanding ─▶ options ─▶ decision ─▶ architecture ─▶ synthesis
                                                    │              │
                                                    ├─▶ ux-blueprint ─▶ claude-design-brief
                                                    ├─▶ architecture-blueprint
                                                    └─▶ implementation-specification ─▶ estimate ─▶ executive-report
                        shared-understanding ─────────────────────────▶ discovery-report
```

None of the forbidden inversions exists: `Executive → Decision`, `Estimate → Specification`,
`Design Brief → Architecture`, `Blueprint → Options`. A downstream artefact exposing an open item
upstream (Spec → OPEN WORK ITEM) is present and is **not** authority inversion.

```text
SEMANTIC AUTHORITY CYCLES: 0
```

---

## 16. Semantic bypass matrix (§38)

| Consumer | Required authority | Possible bypass found? |
|---|---|---|
| Options | SU / decision inputs | **No** — the spine reasons over SU rows; evidence grade governs settlement |
| Architecture | frozen decision + architectability | **No** — both factors mechanical at `/blueprint` step 1; no alternate entry |
| Blueprint | architecture record | **No** — `authority_sources` = the block + core + fragments + architecture-story |
| Spec | architecture | **No** — block is PRIMARY; raw SU rows forbidden as migration-plan source |
| Design Brief | approved UX blueprint | **No** — rendered Blueprint/Spec both forbidden; structural open choice blocks with NO EXCEPTION |
| Estimate A | Spec inventory | **No** — may not add a work unit absent from the Spec |
| Executive | decision | **No** — `options.md` whole-file forbidden; only the Estimate headline crosses |

```text
SEMANTIC BYPASSES FOUND: 0
```

---

## 17. Source-denylist checks (§39)

| Layer | Forbidden read | Declared? |
|---|---|---|
| Discovery | decision / architecture / DK to reinterpret discovery | ✅ Discovery Report forbids `decisions.md# D-NNN`, the architecture block, `architecture-templates/*`, `options.md`, any DK unit, any CRAFT unit, `architecture-story`, `financial-story`, `_render/*` |
| Executive | `options.md` whole-file | ✅ `forbidden_sources[0]`: *"options.md as a whole-file read"* |
| Specification | raw evidence / as-is to invent build obligations | ✅ forbids raw SU rows as migration source, `as-is.md` as acceptance-work source, `inputs/*`/`_capture/*` to re-settle a fact |
| Design Brief | rendered Blueprint / Spec as UX authority | ✅ both named, with the *"never confuse it with the UX blueprint"* clause |
| Estimate | as-is / discovery narrative / financial-story as effort source | ✅ all three named, plus *"any discovery narrative as the source of a work unit"* and SU rows as work-unit source |
| Architecture | CRAFT as technical authority | ✅ `aisa-blueprint`: query/delegation is the platform authority, *"the `craft/` files never restate it"*; every CRAFT unit disclaims it |

---

## 18. Epistemic and proof lineage

### 18.1 Epistemics (§41)

Five kernel states remain the single home (`decision-tree.md`: *"No new state machine. The five
kernel states (`library/kernel/states.md`) carry all epistemics"*). The Specification's epistemic
carriage block reads:

```text
Confirmed_expired: re-verification obligation + an open work item
Unknown:           OPEN WORK ITEM; no fabricated detail
Conflicted:        NO value chosen; a proof obligation instead
```

`render-contract.md` lists *"promote epistemics"* among what render may never do. No deliverable
declares a permitted transformation that promotes, upgrades or resolves a state. Discovery Report
projects **all five** states plus expired Confirmed rows as re-verification obligations.

### 18.2 Proof lineage (§42)

```text
decision proof obligation (decision-tree.md §12, V1–V4)
  → architecture carriage (the block# proof_obligations[])
  → implementation work package + acceptance condition (Spec, preserved verbatim)
  → estimate work unit (Mode A inventory)
  → [UX-relevant] Design Brief validation
```

Required fields survive end to end: **claim · level (V1–V4) · method · owner · funded?**
Re-grading the level, method, owner or funded state is an explicit forbidden transformation.

---

## 19. Scope and comparator neutrality

### 19.1 Scope (§43)

Uncollapsed `(scope, outcome)` pairs are normative in `decision-tree.md` §3 and
`outcome-classes.md` §1.2, carried by `relocated_responsibilities[]` in the architecture block,
and rendered as *"PP side only"* in `aisa-render`'s `authorized-bounded` row. *"The far side of a
scope pair is never architectable here"*, and `architectability_basis` records why in one sentence
so no reader reconstructs it. Class 6 explicitly forbids inferring the surrounding scope's
authorization from the exclusion. No far-side implementation, design or estimate can enter PP
scope by silence.

```text
SCOPE LEAKAGE DETECTED: NO
```

### 19.2 Comparator neutrality (§44)

`COMPARATIVE FIT UNEVALUATED`, `INCUMBENT FIT UNEVALUATED` and `COMPARATOR EVIDENCE ABSENT` are
preserved across **13 active runtime files** (26 occurrences), from the registers through the
architecture fragments to the Executive and Blueprint contracts. No downstream artefact may close
them. The knowledge asymmetry is stated *as* an asymmetry rather than resolved:

> *"The pack's negative evidence is richer for this platform than for any alternative, while its
> coverage of fit runs the other way. The countermeasure is that `COMPARATOR EVIDENCE ABSENT` is
> part of the outcome string, so a reader cannot mistake unevaluated for evaluated-and-lost."*

Zero instructions anywhere that rich PP knowledge may be treated as evidence PP is better.

```text
COMPARATOR BIAS PATH FOUND: NO
```

---

## 20. Numeric and price sweep

### 20.1 Prices (§46)

Zero monetary amounts in `library/packs/pp/` and zero in `library/kernel/`. Every occurrence of
*price* / *SKU* / *rate card* in the pack sits inside a `forbidden_sources` or
`forbidden_transformations` list — the vocabulary appears only as the thing being banned.

```text
ACTIVE RUNTIME PLATFORM PRICES: 0
```

### 20.2 Numbers (§45)

| Class | Finding |
|---|---|
| Structural | 11 ALT · 14 outcomes · 12 concerns · 10 stages · 6 deliverables · 5 architecture units · 4 ALM rungs (0–3) · 6 import channels — all structural, all correct |
| Engagement-owned | volatile values require `verificado_em` + `validade` on the engagement's own row; deliverables retain the verification metadata |
| Canonical documented reading | every quota, threshold, limit and retention period in the RESEARCH units carries the Step 4 stamp `Documented reading · read 2026-09-04 · re-verify: VS-NN`. Scripted check across all 15 RESEARCH units: **0 unstamped material numbers** (the 5 hits are ALM rung ordinals and a documented test procedure "set the row limit to 1") |
| **Suspicious fossil** | **1** — `.claude/agent-memory/_universal/cfo-lens/universal-constraints.md:4`: *"fully-loaded internal rate sits at ~40-60€/hr … ~60-90€/hr for a specialist"*. Undated, no provenance, no validity, in an active consumer path. It is a **labour rate, not a platform price**, and the file does instruct *"Use a documented HR rate if available; otherwise mark the figure as Assumed"* — which limits the damage but does not stamp the number |

```text
SUSPICIOUS NUMERIC FOSSILS: 1
```

---

## 21. Orphan and broken-reference audit

### 21.1 Broken references (§48, §49)

510 path tokens resolved across the active runtime.

```text
BROKEN ACTIVE RUNTIME REFERENCES: 0        (.claude/ + library/)
```

Seven unresolved tokens exist, **all** in historical `docs/` planning records:
`.claude/skills/contradiction-scan/SKILL.md` (`ARCHITECTURE.md`), `library/foo.md` (an
illustrative example), and five references to retired flat domain-knowledge files in
`MIGRATION_FROM_AISA.md` / `IMPLEMENTATION_PLAN.md`. Documentation-only.

Case consistency: no path referenced under two casings; no duplicate conceptual file under
different casing; no stale rename target. Verified programmatically (`P15`).

### 21.2 Orphan runtime assets (§47)

| Asset | Classification |
|---|---|
| `architecture-templates/` (6 files) | **legitimate pull-only** — no manifest key by design; four literal-path consumers, all resolving |
| `library/packs/pp/glossary.md` | **documentation-only** — manifested (`glossary: glossary.md`) but no active runtime consumer resolves that key. Required by `docs/PACK_AUTHORING.md` as a pack contract asset and asserted by two test modules. Not material |
| **`library/packs/pp-backup/`** (27 files) | **MATERIAL ORPHAN** — a complete, self-contained pack at `pack_version: 1.2.0` declaring `pack_id: pp`, containing the retired `sharepoint-first` / `dataverse-first` / `hybrid` architecture templates, the flat legacy domain-knowledge set, the old scored `decision-tree.md` and `applies_to:` deliverable metadata. It sits **inside the runtime pack directory**, so `aisa-start` step 3 (*"If not, list available packs and stop"*) and `aisa-status --check` (*"Verify at least one pack exists under `library/packs/`"*) will enumerate it as a selectable pack. Step 6B lists it under "not modified, deliberately", so its retention is deliberate — but its **location** is not defensible for a pilot |

```text
MATERIAL ORPHAN RUNTIME ASSETS: 1
```

Not deleted during the initial gate (§47).

---

## 22. Kernel / pack boundary (§51, §52)

### 22.1 PP-specific tokens in the kernel — adjudicated

| Token | Location | Adjudication |
|---|---|---|
| `architecture.experience.mode`, value `none` | `render-contract.md:154` | **Legitimate generic contract.** The kernel owns the architecture-block mechanic and the fragment-resolution arithmetic; it names no PP mode enum |
| "DLP policy classification" | `architecture-story.template.md:119` | **Legitimate.** Data-loss-prevention is cross-platform security vocabulary, not a PP product name |
| "prices, SKUs, platform rate cards" | `financial-story.template.md:57,84` | **Legitimate prohibition**, generic |

Zero PP option classes, experience-mode enums, pattern names, service names, product limitations
or entitlement rules in `library/kernel/`.

### 22.2 Generic mechanics duplicated in the pack

One reference only, and it is a **pointer, not a duplication**: `decision-tree.md:56` —
*"No new state machine. The five kernel states (`library/kernel/states.md`) carry all epistemics."*
No generic state definitions, phase mechanics, renderer loop or approval engine is reimplemented
inside the pack.

```text
KERNEL / PACK BOUNDARY: PASS
```

---

## 23. Documentation integrity (§50)

| Document | Currency |
|---|---|
| `docs/ARCHITECTURE.md` | **Current** on the material points — fixed architecture include (§403), the six projection contracts with `owns_calculation` (§356–359), pull-based DK, `experience.mode: none` → zero includes, pack-agnostic Discovery lenses. Two legacy sections are stale: §183 still says a pack declares only *"glossary, question-bank, lenses-config, deliverable-templates"* (the manifest now also declares `decision_tree`, `decision_model`, `domain_knowledge`); §343 shows an example row *"branch dataverse-first"*. Also references `.claude/skills/contradiction-scan/SKILL.md`, which does not exist |
| `docs/PACK_AUTHORING.md` | **Current** — fixed entry point, no per-branch sub-template, projection contracts with `activation`/`owns_calculation`, pull-based DK, question-bank runtime role |
| `library/packs/pp/architecture-templates/README.md` | **Current** — retirement documented, reachability table, architectability boundary, headless semantics |
| `library/packs/pp/domain-knowledge/README.md` | **Current** — pull rule, RESEARCH/CRAFT boundary |
| **`docs/DELIVERABLE_AUTHORING.md`** | **STALE.** Teaches the retired dynamic-include model as the current authoring contract: `sub_templates` with `{{slot}}` resolution, `{{>> architecture-templates/{{chosen_architecture}}.md}}`, and *"they MUST source it from the same place — usually `decisions.md# D-NNN — Branch (if technology)`"*. It was not in Step 6B's modified list and carries no historical marker |

No runtime consumer reads any `docs/` file except `aisa-decide`'s one citation of
`ARCHITECTURE.md §4.5` (a section reference, unaffected). Classified documentation-only.

---

## 24. Context footprint (§53)

| Layer | Files | Lines | Largest units |
|---|---:|---:|---|
| PP discovery (glossary + question bank) | 2 | 411 | question-bank (246) |
| PP manifest | 1 | 240 | pack.yaml |
| PP options / decision | 6 | 1 209 | decision-tree (438), volatility-register (202) |
| **PP domain knowledge** | **26** | **10 910** | patterns (924), release-and-lifecycle (618) |
| PP architecture | 6 | 901 | README (246), architecture-core (245) |
| PP deliverables | 6 | 1 948 | estimate (430), implementation-spec (406) |
| Kernel contracts + templates | 12 | 1 113 | render-contract (199) |
| `.claude` skills | 23 | 2 477 | largest SKILL 312 |
| `.claude` agents | 8 | 342 | chairman (133) |
| `.claude` commands / hooks / rules / memory | 50 | 1 395 | phase-completeness (260) |

### 24.1 Mandatory preload per phase

| Phase | Mandatory | Pull-only |
|---|---|---|
| Discovery | one lens SKILL (~100 L) + ~6 verbatim cue tokens from `pack.yaml` | question bank · DK · decision-tree · registers |
| Options | `decision-tree.md` (438 L) | the stage's own register · 1–2 DK units at D3 |
| Decision | `aisa-decide` | — |
| Architecture | `architecture-templates/README.md` + `architecture-core.md` (491 L) + 0..1 fragment + `craft/screen-consolidation-rules.md` | 1 unit per section, max 2 |
| Render | `render-contract.md` + one deliverable template at a time | units cited at point of need |

**70 % of the pack (10 910 of 15 619 lines) is domain knowledge that is never preloaded.** No file
is permanently loaded despite point-of-need semantics. No duplicate repeated instruction block was
found; each cross-cutting rule has one home and is referenced, not restated (the pull rule lives in
the DK README; the architecture include rule in `render-contract.md`; the question-bank role in
`orchestration.md`).

> *Is any material context present because the framework requires ceremony rather than because the
> engagement requires reasoning?* — **No.** The only permanently-resident pack surface is the cue
> token list (~6 tokens per lens) and, in Options, the 438-line spine.

```text
SYSTEMIC CONTEXT CEREMONY: NO
```

---

## 25. Evidence-heavy authoring / evidence-light runtime (§54)

| Should be authoring-side | Present in runtime? |
|---|---|
| Full research evidence trails | **No** — every unit points to the Step 4B authoring report for traceability |
| Source catalogues | **No** — `docs/pp-pack-authoring/research/pp/evidence/` only |
| Broad comparator evidence | **No** — the runtime carries markers, not comparator corpora |
| Authoring gap annexes (`G001…G120`) | **No** — zero runtime consumers |
| Canonical research ids | **No** — `pack.yaml`: *"No canonical research ids here"* |

| Should be runtime-side | Present? |
|---|---|
| Decision shapes | ✅ 11 classes · 14 outcomes · 12 concerns · 10 stages |
| Technical mechanism knowledge | ✅ 15 RESEARCH units, pull-based |
| Boundaries | ✅ architectability · CRAFT · comparator · scope · S8/Estimate · kernel/pack |
| Projection contracts | ✅ 6, declarative |

**PASS.** No violation.

---

## 26. Light framework / complete reasoning (§55)

**Not simplified away.** Coverage is unchanged: 12 concerns are the coverage object, every serious
option × every material concern, plus the emergent-concern obligation (§7.3) so a material concern
outside the declared list is evaluated anyway. Depth is proportional (D0–D3), not reduced.

**Ceremony not reintroduced.** No 12×N matrix (§7.5 forbids rendering one; concern coverage is
twelve prose lines). No router. No coverage table. No duplicate state layer — the five kernel
states are the only epistemics. No duplicate decision model.

Both sides **PASS**.

---

## 27. Integration smoke traces (§56)

Each deliverable's state resolved by evaluating the declared `activation` / `blocked_when` /
`not_applicable_when` conditions from the six template frontmatters against a synthetic engagement
state, then cross-checked against the applicability matrix in `aisa-render/SKILL.md`.

### S-1 — normal governed internal PP application

Authority transitions: SU → options (S0–S9, class 1) → `D-NNN` → `/blueprint` entry
(reachable × architectable → `authorized`, `experience.mode: owned-internal`) → architecture record
→ approved `ux-blueprint_v<NN>` → deliverables.
Files read: SU · `decisions.md` · `architecture-templates/{README, architecture-core,
fragment-experience-internal, fragment-boundary-and-imports}.md` · `craft/screen-consolidation-rules.md`
· `_synthesis/*` · the six templates. DK pulls: point-of-need only.

| | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| resolved | required | required | required | required | required | conditional (mode A) |

Bypasses: 0 · unexpected preloads: 0 · **PASS**

### S-2 — headless PP

`experience.mode: none` → zero experience fragments, `primary_surface: null`, no A4, no gap.
Blueprint still produced and approved (the architecture record); A6/A7 carry the architecture.

| | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| resolved | required | required | required | required | **not applicable** | conditional (mode A) |

No fake human surface anywhere; Design Brief NA is a logged skip, not a gap.
Bypasses: 0 · **PASS**

### S-3 — positive non-PP decision

Outcome reachable, selected solution **not architectable** by this pack →
`authorization: not-authorized` for every scope. Experience mode of the chosen non-PP solution is
`owned-internal`, so the Design Brief's NA rests on the **absent authorization**, not on headlessness.

| | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| resolved | required | required | **not applicable** | **not applicable** | **not applicable** | **not applicable** |

Executive carries the outcome basis **and** the architectability basis as two distinct reasons;
neither relabelled *decision blocked*. No PP architecture, Spec or Brief produced. **PASS**

### S-4 — Decision Blocked (class 12)

| | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| resolved | required | required | **not applicable** | **not applicable** | **not applicable** | **not applicable** |

Executive is `required` (activation `always`), never NA. No speculative downstream work; the
evidence task lands in the Executive's *what happens next* and the Discovery Report's *evidence
still required*. **PASS**

```text
SMOKE TRACES FAILED: 0
```

No trace contradicted a frozen gate; T01–T18, Step 4C, Step 5C and DF-1…DF-8 were not re-run (§57).

---

## 28. P-1 … P-18 integrity tests (§59)

New module `.claude/tests/test_pp_pack_integrity.py` — **96 tests, 0 failures**. Structural
assertions against parsed manifests and frontmatter, not token greps alone.

| | Coverage | |
|---|---|:--:|
| P-1 | Manifest targets resolve · no duplicate · no routing key · no dynamic template slot | ✅ |
| P-2 | No active retired architecture paths (+ the two pins, §29.1) | ✅ |
| P-3 | Exactly 15 RESEARCH + 10 CRAFT; filesystem == manifest; no legacy resurrection | ✅ |
| P-4 | Exactly 5 architecture runtime units; no headless fragment; no product template | ✅ |
| P-5 | Exactly 6 contracts; canonical names; manifest/template agreement | ✅ |
| P-6 | No architecture authorization bypass; read-never-derived | ✅ |
| P-7 | Exactly two deliverable read edges; reverse edges forbidden | ✅ |
| P-8 | No DK preload — manifest, README, all 26 units, 4 consumers | ✅ |
| P-9 | CRAFT non-authoritative; never a D3 pull target | ✅ |
| P-10 | Headless has no mandatory surface dependency | ✅ |
| P-11 | Build-gating condition guard (F-1) | ✅ |
| P-12 | Estimate→Executive payload guard (F-2) | ✅ |
| P-13 | Estimate modes == exactly two | ✅ |
| P-14 | No monetary amount in pack or kernel; price vocabulary never on a source edge | ✅ |
| P-15 | No broken active runtime reference; case consistency | ✅ |
| P-16 | No semantic authority cycles (DFS); no forbidden inversion | ✅ |
| P-17 | Scope-pair representation remains possible; far side never architectable | ✅ |
| P-18 | No deliverable owns epistemic state | ✅ |

```text
P-1...P-18 INTEGRITY COVERAGE: 18/18
```

Two tests deliberately **pin known defects** rather than hiding them
(`test_chairman_carry_forward_is_pinned_and_isolated`,
`test_agent_memory_retired_vocabulary_set_is_pinned`): they assert the defect's exact boundary, so
the contamination cannot grow silently, and they invert the moment the bounded repair lands.

---

## 29. Full regression (§58)

| Module | Before | After |
|---|---:|---:|
| `test_council_wiring.py` | 31 | 31 |
| `test_orchestrator_wiring.py` | 23 | 23 |
| `test_pp_architecture_templates.py` | 116 | 116 |
| `test_pp_deliverable_templates.py` | 218 | 218 |
| `test_pp_discovery_runtime.py` | 22 | 22 |
| `test_pp_domain_knowledge.py` | 64 | 64 |
| `test_pp_options_decision_model.py` | 95 | 95 |
| `test_state_scaffold.py` | 15 | 15 |
| **`test_pp_pack_integrity.py`** | — | **96** |
| pack/kernel subtotal | 584 | **680** |
| kernel text-extract | 23 | 23 |
| **total** | **607** | **703** |

```text
ADDITIONS: 96
FAILURES:   0
```

---

## 30. Findings and classification (§61)

| # | Finding | Class | Material? |
|---|---|:--:|:--:|
| **B-3** | `.claude/agents/chairman.md` carries a second, pre-Step-3 `options.md` spec that **actively emits** `Branch (if technology)` sourced `<from decision-tree.md>`, and omits option class, scope, viability, outcome class, disqualifier evidence grade, preconditions, proof requirement, concern coverage and comparator status. Duplicate authority with `chairman-synthesis/SKILL.md` | **B** (+ duplicate authority) | **YES** |
| **B-2** | `agent-memory/_universal/solution-architect/universal-constraints.md` instructs *"branch shortlisting"* and calls `decision-tree.md` *"the gating logic"* for it; also prescribes a `pass/risky/blocker` per-constraint verdict ladder that maps onto none of the seven §3 decision-semantics terms | **B** | **YES** |
| **B-1** | `agent-memory/_universal/solution-architect/diary.md` narrates a retired-model engagement (`sharepoint-first` excluded at gate `R0`; `dataverse-first` *"venceu R0–R6"*) and the agent is instructed to cite diary patterns | **B** | **YES** |
| **M-1** | `library/packs/pp-backup/` — a complete retired pack (`pack_id: pp`, v1.2.0, branch templates, flat legacy DK, scored decision tree) inside the runtime pack directory, selectable by `aisa-start` / listed by `aisa-status --check` | **M** | **YES** |
| **J-1** | `agent-memory/_universal/cfo-lens/universal-constraints.md:4` — undated hourly labour rates (`~40-60€/hr`, `~60-90€/hr`) with no provenance or validity, in an active consumer path | **J** | No (bounded by the file's own *"mark as Assumed"* instruction) |
| **L-1** | `docs/DELIVERABLE_AUTHORING.md` teaches the retired dynamic-include / `{{chosen_architecture}}` / `Branch (if technology)` authoring model as current, with no historical marker | **L** | No (no runtime consumer) |
| **L-2** | `docs/ARCHITECTURE.md` §183 stale pack-declaration list; §343 stale `dataverse-first` example; dangling `.claude/skills/contradiction-scan/SKILL.md` | **L** | No |
| **O-1** | `decision-tree.md` mtime falls inside the Step 6A window while Step 6B declares Step 3 registers untouched; no commit boundary exists to prove byte identity. All Step 3 invariants hold and the 95-test suite passes | observation | No |
| **O-2** | `library/packs/pp/glossary.md` is manifested but has no active runtime consumer | observation | No |

Classes with **zero** findings: A (manifest/path) · C (semantic authority bypass) · D
(source-edge/consumer) · E (frozen-layer regression) · F (kernel/pack boundary leak) · G (DK
loading/authority) · H (epistemic/proof lineage) · I (scope/comparator neutrality) · K
(context/framework ceremony) · N (test-only).

---

## 31. Final verdict

§63 requires every condition to hold. All hold **except one**:

> *"no active scored/branch decision model survives"*

B-3 defeats it directly: the writer of `options.md` is still instructed to serialize a retired
branch field from an authority that no longer defines it, using an option shape that predates the
frozen Step 3 model. B-1 and B-2 compound it inside the standing memory of the Options evaluator.
Per §63, one material semantic/runtime failure means FAIL. Not averaged.

```text
STEP 7 — FINAL PACK INTEGRITY / CONSISTENCY GATE: FAIL
```

Everything else — manifest, paths, architecture entry, headless, DK pull discipline, CRAFT
boundary, volatility, provenance, the six projections, both Step 6C repairs, the two read edges,
zero cycles, zero bypasses, zero scope leakage, zero comparator bias, zero prices, zero broken
references, kernel/pack boundary, context footprint, four smoke traces, 703 tests green — passes.

### 31.1 Recommended bounded repair set (§62) — NOT applied

Smallest set that closes the material findings. All four are **serialization / asset placement**;
none touches Steps 3–6 semantics, adds a stage, a template, a deliverable, a knowledge unit, a
router or a state machine.

| # | Repair | Scope |
|---|---|---|
| **R-1** | Replace `.claude/agents/chairman.md` §"Phase artefact specifications" with a pointer to `.claude/skills/chairman-synthesis/SKILL.md`, leaving exactly one specification per artefact | 1 file, documentation-shaped |
| **R-2** | Rewrite the two `solution-architect` memory sections in the current vocabulary: *branch shortlisting* → *option-class generation at S1 + material-concern evaluation at S5*; *pass/risky/blocker* → the §3 decision-semantics terms. Preserve the underlying advice (read data before proposing; constraints are a floor) | 1 file, 2 sections |
| **R-3** | Re-anonymise `solution-architect/diary.md` entry (a) / (c) into the current model, or mark it explicitly as a pre-Step-3 record so the persona does not reason from retired gates. Note the entry is already flagged in-file as a simulated validation fixture *"substituir/remover na primeira curadoria real"* — removing it is the cheaper option and is sanctioned by `aisa-retro`'s human-curation rule | 1 file |
| **R-4** | Move `library/packs/pp-backup/` out of `library/packs/` (e.g. to an archive path outside the pack-resolution root) so no retired pack is selectable at engagement start | directory move |

Optional, documentation-only: **R-5** mark `docs/DELIVERABLE_AUTHORING.md` superseded or update it
to the fixed-include model; **R-6** correct `ARCHITECTURE.md` §183 / §343 and the dangling
`contradiction-scan` reference; **R-7** stamp or externalise the cfo-lens hourly rates.

After R-1…R-4, the two pinning tests in `test_pp_pack_integrity.py` invert (they will FAIL on the
now-absent tokens), the retired-vocabulary sweep exclusions are removed, and a targeted re-gate of
§5, §6, §7 and §47 is sufficient — no full replay.

`PP PACK AUTHORING: NOT COMPLETE` · `STEP 1–6: CLOSED` · `STEP 7: OPEN pending R-1…R-4`

---

## 32. Recommendation for Step 8

**Do not start the real engagement pilot yet.** Not because the pack is weak — the frozen layers
are in good order and the chain of authority holds end to end — but because B-3 would corrupt the
**first artefact the pilot produces**. `options.md` is the input to `/decide`, `/blueprint` and the
Executive Report; serialized through the stale chairman spec it would carry no `(scope, outcome)`
pairs, no outcome class and no comparator status, and the pilot would then be exercising a decision
chain fed by the wrong shape. Every subsequent observation would be uninterpretable.

Sequence:

1. Apply **R-1…R-4** (bounded, serialization/placement only).
2. Targeted re-gate: §5 stale-vocabulary sweep · §6 chairman adjudication · §7 old-Options sweep ·
   §47 orphans · full regression. Expect the two pins to invert and the exclusions to be removed.
3. On PASS, record `PP PACK AUTHORING: COMPLETE` / `STEP 1–7: CLOSED`, freeze
   `library/packs/pp/`, bump `pack_version` to `1.8.1` (repair, not semantics), and **commit** —
   the entire Step 1–7 body of work is currently uncommitted working tree, which is the single
   largest operational risk carried into a pilot and the reason §24 provenance had to fall back on
   mtimes.
4. Then Step 8. It may discover empirical and usability defects; it is not permission to redesign.

Two things to watch in the pilot, carried forward as observations rather than defects: whether the
438-line Options spine is the right resident size in a live round, and whether the `half_lives_override: {}`
question `pack.yaml` deliberately left OPEN can be calibrated from real engagement decay rather
than invented.

---

```text
STEP 7 — FINAL PACK INTEGRITY / CONSISTENCY GATE: FAIL
ACTIVE PP PACK FILES: 47
MANIFEST TARGETS RESOLVED: 40/40
BROKEN ACTIVE RUNTIME REFERENCES: 0
RESEARCH UNITS: 15/15
CRAFT UNITS: 10/10
ARCHITECTURE RUNTIME UNITS: 5/5
CANONICAL DELIVERABLE CONTRACTS: 6/6
ACTIVE RETIRED ARCHITECTURE MODEL REFERENCES: 3
ACTIVE OLD SCORED/BRANCH DECISION SEMANTICS: 3
CHAIRMAN LEGACY BRANCH SERIALIZATION: ACTIVE
DISCOVERY TECHNOLOGY NEUTRALITY: PASS
SHARED UNDERSTANDING REMAINS EPISTEMIC AUTHORITY: YES
DECISION MODEL STRUCTURAL INTEGRITY: PASS
ARCHITECTURE AUTHORIZATION BYPASS FOUND: NO
HEADLESS END-TO-END INTEGRITY: PASS
DOMAIN KNOWLEDGE PRELOAD DETECTED: NO
CRAFT AUTHORITY LEAK DETECTED: NO
VOLATILITY / PROVENANCE INTEGRITY: PASS
RUNTIME RESEARCH-GAP ANNEX CONSUMER EXISTS: NO
DELIVERABLE PROJECTION INTEGRITY: PASS
BUILD-GATE GUARD PRESENT: YES
ESTIMATE→EXECUTIVE PAYLOAD GUARD PRESENT: YES
ESTIMATE INPUT MODES: 2/2
DELIVERABLE-TO-DELIVERABLE READ EDGES: 2/2
SEMANTIC AUTHORITY CYCLES: 0
SEMANTIC BYPASSES FOUND: 0
SCOPE LEAKAGE DETECTED: NO
COMPARATOR BIAS PATH FOUND: NO
ACTIVE RUNTIME PLATFORM PRICES: 0
SUSPICIOUS NUMERIC FOSSILS: 1
MATERIAL ORPHAN RUNTIME ASSETS: 1
KERNEL / PACK BOUNDARY: PASS
SYSTEMIC CONTEXT CEREMONY: NO
S-1 NORMAL PP TRACE: PASS
S-2 HEADLESS TRACE: PASS
S-3 NON-PP TRACE: PASS
S-4 DECISION-BLOCKED TRACE: PASS
P-1...P-18 INTEGRITY COVERAGE: 18/18
FULL REGRESSION TESTS: 703
FULL REGRESSION FAILURES: 0
RUNTIME MODIFIED DURING INITIAL GATE: NO
NEW RESEARCH PERFORMED: NO
PP PACK AUTHORING COMPLETE: NO
READY FOR STEP 8 — REAL ENGAGEMENT PILOT: NO
```

---
---

# Step 7 Addendum — Bounded Runtime Cleanup / Targeted Re-Gate

> **The initial gate's `FAIL` above is the record and is not rewritten.** This addendum is what
> happened next. Audit trail:
>
> ```text
> STEP 7 INITIAL GATE: FAIL
> → bounded runtime cleanup
> → targeted integrity re-gate
> → STEP 7 PASS
> → PP PACK AUTHORING COMPLETE
> ```

## A1. Correction to the initial verdict description

§31 of the initial report said *"one material defect class survives"*. **That was wrong, and the
correction matters for what the repair had to cover.** The initial gate found **two independently
material runtime problem families**, not one, plus a third required for pilot readiness:

| Family | Findings | Why independently material |
|---|---|---|
| **B — active retired decision/architecture vocabulary** | B-3 chairman duplicate Options serialization · B-2 solution-architect retired branch procedure · B-1 solution-architect retired scored-gate diary | Three separate active runtime files, three separate consumers. Repairing the chairman alone would have left the Options *evaluator* still reasoning in the retired model |
| **M — selectable retired pack** | M-1 `library/packs/pp-backup/` | Independent of B: a complete v1.2.0 pack selectable at `/start`, reachable with no B-family involvement at all |
| **J — unsupported standing numeric anchor** | J-1 CFO-lens hourly-rate ranges (and, found during this pass, four more monetary anchors the initial sweep missed) | Not a semantic defect, but a pilot would anchor real money on an undated, unsourced number |

The initial report's framing under-counted the exposure by collapsing B and M into one "defect class".
The finding table (§30) listed them correctly; the prose summary did not.

**Steps 3–6 semantics were not defective and are not defective now.** Every finding in every family was
runtime residue *around* the frozen model — a stale copy, a stale memory, a misplaced asset, an
unsourced number. No stage, concern, option class, outcome class, register row, knowledge unit,
architecture unit, deliverable contract, activation rule, source edge or estimate mode was wrong, and
none was changed.

## A2. Files and assets changed

| # | Path | Change | Class |
|---:|---|---|---|
| 1 | `.claude/agents/chairman.md` | 133 → 67 lines. Duplicate artefact schema removed, replaced by a pointer | R-1 |
| 2 | `.claude/agent-memory/_universal/solution-architect/universal-constraints.md` | 3 sections re-expressed against the frozen model | R-2 |
| 3 | `.claude/agent-memory/_universal/solution-architect/diary.md` | Simulated retired-model fixture removed; 2 general lessons retained, re-expressed | R-3 |
| 4 | `library/packs/pp-backup/` → `docs/pp-pack-authoring/archive/pp-backup-v1.2.0/` | 27 files relocated intact, out of the pack-resolution root | R-4 |
| 5 | `.claude/agent-memory/_universal/cfo-lens/universal-constraints.md` | Rewritten: all unsourced monetary anchors removed | R-5 |
| 6 | `.claude/agent-memory/_universal/business-analyst/universal-constraints.md` | 1 line — approval-authority figure removed | R-5 |
| 7 | `.claude/agent-memory/_universal/compliance-officer/universal-constraints.md` | 1 line — sign-off threshold figure removed | R-5 |
| 8 | `.claude/skills/aisa-simulate/SKILL.md` | 2 lines — retired verdict ladder → the frozen model's vocabulary | R-2 family |
| 9 | `library/kernel/synthesis-templates/architecture-story.template.md` | 2 slot descriptions — same ladder, plus a retired knowledge-unit citation | R-2 family |
| 10 | `docs/DELIVERABLE_AUTHORING.md` | Rewritten to the fixed-Architecture-Layer / projection-contract model | D-1 |
| 11 | `docs/ARCHITECTURE.md` | 3 identified stale items only | D-2 |
| 12 | `library/packs/pp/pack.yaml` | `pack_version` 1.8.0 → 1.8.1 + rationale block | §23 |
| 13 | `.claude/tests/test_pp_pack_integrity.py` | 3 pinning tests → 4 clean-state assertions (96 → 97) | §14 |
| 14 | `.claude/tests/test_pp_deliverable_templates.py` | 1 test: exact version pin → minor-line pin | Class N |

**Not touched:** `decision-tree.md` · `decision-model/*` · all 26 domain-knowledge units · all 6
architecture units · all 6 deliverable templates · `render-contract.md` · `blueprint-contract.md` ·
`orchestration.md` · `states.md` · `phases.md` · the six Discovery lenses · `question-bank.md` ·
`glossary.md`.

**`library/` write mechanics.** Items 4, 9 and 12 are under the read-only guard. They went through the
sanctioned out-of-band administrative path with explicit per-operation authorization, exactly as Steps
5B and 6B did. The pp-backup relocation was verified by comparing a sorted SHA-256 manifest of both
trees **before** deleting the source — identical (`fc9f19a9…7754f`), 27 files each.

## A3. R-1 — duplicate Options artefact authority removed

`.claude/agents/chairman.md` carried its own `## Phase artefact specifications` block: a pre-Step-3
`options.md` schema with `Branch (if technology)` sourced `<from decision-tree.md>`, plus
Pros/Cons/Constraints-checked/Reversibility/Indicative-effort-band, and a second copy of the
`chairman-synthesis-<round>.md` audit-trail schema. Removed in full and replaced by:

> **Canonical phase artefact serialization is owned by `.claude/skills/chairman-synthesis/SKILL.md`.
> Follow that contract exactly; this agent does not maintain a second copy.**
>
> ```text
> one artefact
>   → one serialization authority
> ```
>
> This agent owns its mandate, its role and its behavioural principles. It owns no artefact schema.

Three consequential inconsistencies in the same file were corrected with it, all of the same family —
the agent implying it writes a Decision artefact, which its own mandate and `chairman-synthesis`
both deny: the `D-<NN>` round suffix in its write list, *"or the draft decision block"* in execution
step 6, and `aisa-decide` listed as a calling orchestrator in step 9.

**No new schema was invented.** `chairman-synthesis/SKILL.md` was not modified.

### A3.1 Chairman repair validation (§3)

```text
chairman.md emits `Branch (if technology)`        → NO   (0 occurrences)
chairman.md owns an Options field schema          → NO   (0 of the 5 legacy field lines)
chairman-synthesis/SKILL.md owns Options          → YES  (sole definer, asserted by test)
```

A new Options round serializes, per the unchanged canonical contract: option class · scope · viability ·
outcome (from the outcome register's render template) · disqualifiers with evidence status ·
preconditions · material trade-offs · material risks · economic implications · decision-changing
uncertainties · proof requirement · twelve-line concern coverage · comparator status.

## A4. R-2 — solution-architect standing constraints

Two sections carried the retired procedure; both were re-expressed, keeping the underlying lesson:

| Was | Now |
|---|---|
| *"the right architectural **branch**"* determined by data | *"the strongest determinant of what a solution can be is the data"* — same lesson, no branch |
| *"`decision-tree.md` is the gating logic for **branch shortlisting**"* | *"the ordered evaluation procedure… candidate option classes at **S1**, every serious option × every material concern at **S5**, outcome at **S9**"* |
| — (absent) | added: a settled hard disqualifier requires decision-grade evidence; `Assumed` never settles a hard exclusion |
| *"walk every constraint and produce a verdict: **pass / risky / blocker**"* | *"a **standing-attention floor**, never a ceiling and never the coverage object"* — coverage is the twelve concerns + the emergent-concern obligation |
| *"the exact band-to-hour conversion lives in `cfo-lens/universal-constraints.md`"* | *"there is no band-to-hour conversion to carry here"* — effort is calculated once, by the Estimate |

Decision-status vocabulary is now a **pointer**, not a copied list: `decision-tree.md` §3 and the
outcome register own it.

### A4.1 No parallel verdict system (§5) — and two more instances found

The re-gate sweep caught the same `pass / risky / blocker` ladder in **two active runtime files the
initial gate had not surfaced** — its §7 sweep grepped for `R0…R6` and scoring vocabulary but not for
that phrase:

- `.claude/skills/aisa-simulate/SKILL.md` §3 — *"the decision-tree constraint verdicts (pass / risky /
  blocker)"*, attributing to `decision-tree.md` a ladder it does not define.
- `library/kernel/synthesis-templates/architecture-story.template.md` §Watch-list constraints — *"the
  per-constraint state (pass / risky / blocker)"*.

Both were repaired **vocabulary-only**: each section keeps exactly what it carried (which constraints,
what was found, what would force a re-think) and now states it in the round's own vocabulary —
*disqualifier at its scope · precondition · trade-off · risk · uncertainty* — with an explicit
instruction to project the recorded finding rather than re-grade it. The same edit removed a citation
to `security-patterns`, a domain-knowledge file retired in Step 4; the template now points at the
manifest instead of a dead filename. The 218-test Step 6 suite passes unchanged.

## A5. R-3 — retired-model diary fixture removed

The simulated `galp-adv-val` entry taught the agent through the retired model and the agent is
instructed to cite diary patterns; a historical label would not have been protection. Removed entirely,
per the entry's own in-file instruction (*"substituir/remover na primeira curadoria real"*) and
`aisa-retro`'s human-curation rule.

Two general lessons survived, re-expressed in current semantics and explicitly labelled *not diary
entries*: (i) a deadline without a document is an `Unknown` with an owner, never an `Assumed`;
(ii) infrastructure uncertainties arrive open at Options and close in one conversation — S5/S7 input.
No fictional historical result was rewritten to look as though the current model produced it.

### A5.1 Solution-architect memory invariant (§7)

```text
sharepoint-first              0
dataverse-first               0
branch shortlisting           0
architectural branch          0
branch winner / branch loser  0
R0–R6 retired gate semantics  0
pass / risky / blocker        0
```

Absence, not prohibition wording — the removal note itself was rewritten so it names no retired token.

## A6. R-4 — pp-backup out of the pack-resolution root

```text
library/packs/pp-backup/  →  docs/pp-pack-authoring/archive/pp-backup-v1.2.0/
```

27 files, byte-identical, verified before the source was removed. **Not** relocated to
`library/packs/archive/`, `_backup/` or `legacy/` — all of those remain inside the resolution root.
Contents untouched: it is preserved as historical evidence, not made to look current.

### A6.1 Backup invariants (§9)

```text
directories under library/packs/ claiming pack_id: pp   → 1   (library/packs/pp/)
runtime-selectable PP pack                              → library/packs/pp/
retired v1.2.0 pack selectable                          → NO
retired branch templates under library/packs/           → 0
packs under library/packs/                              → generic · mendix · outsystems · pp
library/packs/pp/ file count                            → 47 (unchanged)
```

## A7. R-5 — standing numeric anchors removed

The initial gate counted **one** fossil. A proper currency sweep over all standing memory during this
pass found **five**, in three files — the initial regex required a digit adjacent to `€` and so missed
every `k€` form:

| File | Removed | Replaced by |
|---|---|---|
| `cfo-lens/universal-constraints.md` | `~40-60€/hr`, `~60-90€/hr` | the engagement's own rate, carrying provenance; `Unknown` / measurement obligation where unavailable; `Assumed` only with explicit basis **and** explicit validator |
| `cfo-lens/universal-constraints.md` | `~5-20k€`, `~10-30k€`, `~20-80k€`, `~80k€+` build bands | duration bands only (Small/Medium/Large in weeks), carrying no money and no hour conversion |
| `cfo-lens/universal-constraints.md` | `~50k€` / `~250k€` approval thresholds | *"ask for the actual thresholds and record them with their source"* + the structural rule that survives |
| `business-analyst/universal-constraints.md` | `~50-100k€` director authority | same treatment; the `Unknown`-raising rule is unchanged |
| `compliance-officer/universal-constraints.md` | `> 10k€` sign-off step | same treatment |

**No replacement rates were invented.** The binding rule now reads:

```text
delivery or as-is labour rate needed
  → engagement-provided / approved internal rate, with provenance
  → unavailable and material  → Unknown (custo · swing · owner), or a measurement obligation
  → assumption permitted      → Assumed, explicit basis, explicit validator, never market truth
```

### A7.1 Economics invariant (§11)

The CFO lens still reasons about labour cost categories, FTE and opportunity cost, entitlement,
implementation effort, operating burden, uncertainty and cost drivers — it simply supplies no number.
Full sweep of standing constraints (`universal-constraints.md` + `anti-patterns.md`, 14 files):

```text
ACTIVE UNSOURCED LABOUR RATE FALLBACKS: 0
standing currency anchors of any kind:  0
```

**Classified and deliberately left:** currency figures in four persona *diaries*
(`business-analyst`, `cfo-lens`, `data-steward`, `operations-lead`). Each is an engagement observation
carrying its SU id (`C-014`, `X-001`, `C-009`, `C-012`) — a diary is a **record**, a constraints file is
an **instruction**, and §18 exempts engagement-provenanced values. They originate from the same v3.0
simulated fixture and carry no retired vocabulary; the first real `/retro` curation should replace them.
Recorded as a Step 8 item, not a fossil. Structural numbers (ALM rungs, stage/class counts, band
durations, ROI-month heuristics) were not touched.

## A8. Documentation cleanup (§12) — performed

**D-1 `docs/DELIVERABLE_AUTHORING.md` — updated, not just marked superseded.** It presented itself as
current authoring guidance while teaching the retired model. Now states: the six canonical deliverables
as a **closed** set; templates as **projection contracts** (`authority_sources` / `conditional_sources` /
`forbidden_sources` / `permitted_` and `forbidden_transformations`); `activation` as declarative
applicability, explicitly *not* routing; the **fixed** architecture include with zero-or-one experience
fragment and N+M boundary fragments; the four render-gap classes; non-omissible build gates as distinct
from open work items; the two-edge deliverable read graph with the bounded Executive payload. *"Adding
a new deliverable"* became *"Don't"*, with the reason. Anti-patterns rewritten to the real ones —
widening a source edge for better prose, re-parsing raw evidence, promoting epistemics, manufacturing a
surface under `experience.mode: none`, manufacturing a comparison.

**D-2 `docs/ARCHITECTURE.md` — the three identified items only.** §183 pack-declaration list corrected
to what the manifest actually declares (adding `decision_tree`, `decision_model`, pull-based
`domain_knowledge`, and noting architecture-templates are *not* declared because the entry point is
fixed). §343 example row de-branched. The dangling `.claude/skills/contradiction-scan/SKILL.md`
checklist entry struck through and annotated: never built, deliberately — the chairman records
contradictions as `Conflicted` rows and lenses raise `Unknown`. The rest of the document was not
rewritten.

## A9. Integrity-test inversion (§14)

The three tests whose passing condition was *"the known defect still exists exactly here"* are gone.
Replaced by four clean-state assertions:

| Was (pinned defect) | Now (clean state) |
|---|---|
| `test_chairman_carry_forward_is_pinned_and_isolated` — asserted the retired field was **present** | `test_no_agent_definition_owns_an_artefact_schema` — asserts it is absent, the pointer exists, none of the 5 legacy field lines survives, and no agent definition carries a retired token |
| `test_chairman_synthesis_skill_is_the_clean_options_authority` | `test_exactly_one_options_serialization_authority` — same checks **plus** it counts the files defining the `options.md` shape and requires exactly one |
| `test_agent_memory_retired_vocabulary_set_is_pinned` — pinned a known-contaminated set | `test_standing_agent_memory_is_free_of_retired_semantics` — requires the set to be empty |
| — | `test_solution_architect_memory_uses_the_current_model` — new: asserts the lessons survived, anchored to S1/S5/S9, the evidence-grade rules and the attention floor |

The sweep in `P-2` no longer excludes `.claude/agent-memory/` or `chairman.md`: **standing memory is
runtime**, and it is now swept like everything else. `P-1…P-18` semantics are unchanged.

One test outside the integrity suite needed a bounded correction (Class N):
`test_pp_deliverable_templates.TestTD16Manifest.test_pack_version_bumped` pinned the **exact** string
`1.8.0`, which would fail on any later patch. Its intent — *Step 6B put the manifest on the 1.8 line* —
is preserved by asserting the minor line `^1\.8\.\d+$`; a move off 1.8.x still fails, which is what the
test exists to catch. The rationale-comment assertion is unchanged.

## A10. Targeted sweeps

### A10.1 Stale vocabulary (§15)

```text
ACTIVE RETIRED ARCHITECTURE MODEL REFERENCES: 0
ACTIVE OLD SCORED/BRANCH DECISION SEMANTICS:  0
```

Not counted, per §15: negative assertions in the guard suites · the retirement documentation in
`architecture-templates/README.md` §11 · historical authoring and archive material outside runtime
(`docs/pp-pack-authoring/**`). **Standing agent memory was counted as runtime.**

Two remaining occurrences in active runtime are negations that state the retirement, not uses of it:
`aisa-decide/SKILL.md:158` (*"is **removed**"*) and `decision-tree.md:21` (*"replaces the scored
three-branch tree"*). Both were already in the guard's allow-list with their negation asserted.

Also verified zero: retired flat domain-knowledge filenames cited anywhere in active runtime prose
(`security-patterns`, `powerfx-patterns`, `delegation-matrix`, `excel-patterns`, `flows-patterns`,
`*-reference`).

### A10.2 Chairman (§16)

```text
CHAIRMAN LEGACY BRANCH SERIALIZATION: ABSENT
DUPLICATE OPTIONS SERIALIZATION AUTHORITIES: 0
```

Council-independent Options writing resolves through `chairman-synthesis/SKILL.md` and nothing else —
`aisa-options` §6 hands off to it, and it is now the sole file defining the artefact shape.

### A10.3 Pack root / orphans (§17)

```text
MATERIAL ORPHAN RUNTIME ASSETS: 0
SELECTABLE RETIRED PP PACKS:    0
```

`architecture-templates/` (6 files) remain **legitimate pull-only assets** — unmanifested by design,
reached by literal path from four consumers, all resolving. `library/packs/pp/glossary.md` remains
manifested-but-unread: a **non-material documentation asset**, unchanged by this repair, still required
by `docs/PACK_AUTHORING.md` as a pack contract asset.

### A10.4 Numeric fossils (§18)

```text
SUSPICIOUS NUMERIC FOSSILS:              0
ACTIVE UNSOURCED LABOUR RATE FALLBACKS:  0
ACTIVE RUNTIME PLATFORM PRICES:          0
```

Structural enum/count numbers, engagement-provenanced values and authoring research evidence outside
runtime were not flagged and not touched.

## A11. Smoke traces (§19) — wiring re-check only

Re-run unchanged against the repaired runtime; no scenario was recreated.

| | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate | |
|---|---|---|---|---|---|---|---|
| **S-1** normal PP | required | required | required | required | required | conditional (mode A) | **PASS** |
| **S-2** headless | required | required | required | required | **not applicable** | conditional (mode A) | **PASS** |
| **S-3** positive non-PP | required | required | **not applicable** | **not applicable** | **not applicable** | **not applicable** | **PASS** |
| **S-4** Decision Blocked | required | required | **not applicable** | **not applicable** | **not applicable** | **not applicable** | **PASS** |

```text
SMOKE TRACES FAILED: 0
```

S-1's Options serialization now resolves through the frozen Step-3-aligned shape: the chairman has no
competing schema to fall back on, so `(scope, outcome)` pairs, outcome class, disqualifier evidence
status, preconditions, proof requirement, concern coverage and comparator status all reach `/decide`,
`/blueprint` and the Executive — which was exactly the exposure the initial gate found.

## A12. Full regression (§20)

| Module | Before (initial gate) | After |
|---|---:|---:|
| `test_council_wiring.py` | 31 | 31 |
| `test_orchestrator_wiring.py` | 23 | 23 |
| `test_pp_architecture_templates.py` | 116 | 116 |
| `test_pp_deliverable_templates.py` | 218 | 218 |
| `test_pp_discovery_runtime.py` | 22 | 22 |
| `test_pp_domain_knowledge.py` | 64 | 64 |
| `test_pp_options_decision_model.py` | 95 | 95 |
| **`test_pp_pack_integrity.py`** | **96** | **97** |
| `test_state_scaffold.py` | 15 | 15 |
| pack/kernel subtotal | 680 | **681** |
| kernel text-extract | 23 | 23 |
| **total** | **703** | **704** |

```text
INTEGRITY TESTS: 96 → 97   (3 pinning tests removed, 4 clean-state tests added)
ADDITIONS:       +1
FAILURES:        0
```

Not replayed, and not needed — no frozen semantic layer changed: T01–T18 · Step 4C · Step 5C ·
the Step 6C DF corpus. The Step 3 (95), Step 4 (64), Step 5 (116) and Step 6 (218) suites all pass
unchanged, which is the evidence that the cleanup stayed outside the model.

## A13. Remaining findings

| # | Finding | Class | Material? | Disposition |
|---|---|:--:|:--:|---|
| **O-2** | `library/packs/pp/glossary.md` is manifested but has no active runtime consumer | observation | No | Pack contract asset per `PACK_AUTHORING.md`; leave |
| **O-3** | Six persona diaries remain simulated v3.0 fixtures (the solution-architect's was removed as it carried retired semantics; the others do not) | observation | No | Replace at the first real `/retro` curation — Step 8 item |
| **O-1** | `decision-tree.md` mtime falls inside the Step 6A window; no commit boundary existed to prove byte identity | observation | No | **Closed by the checkpoint** (§A15) — from now on git proves it |

Zero findings in classes A · C · D · E · F · G · H · I · K · N.

## A14. Final verdict

Every §22 PASS criterion is met:

```text
chairman obsolete serialization        → absent
duplicate Options artefact authority   → absent
solution-architect retired semantics   → absent
selectable retired PP pack             → absent
unsupported standing labour-rate nums  → absent
active retired architecture refs       → 0
active old scored/branch semantics     → 0
material orphan runtime assets         → 0
semantic bypasses                      → 0
authority cycles                       → 0
smoke traces                           → 4/4 PASS
full regression failures               → 0
```

```text
STEP 7 TARGETED RE-GATE: PASS

ACTIVE RETIRED ARCHITECTURE MODEL REFERENCES: 0
ACTIVE OLD SCORED/BRANCH DECISION SEMANTICS: 0
CHAIRMAN LEGACY BRANCH SERIALIZATION: ABSENT
DUPLICATE OPTIONS SERIALIZATION AUTHORITIES: 0
SELECTABLE RETIRED PP PACKS: 0
SUSPICIOUS NUMERIC FOSSILS: 0
MATERIAL ORPHAN RUNTIME ASSETS: 0
SEMANTIC BYPASSES FOUND: 0
SEMANTIC AUTHORITY CYCLES: 0

PP PACK AUTHORING: COMPLETE
STEP 1–7: CLOSED
STEP 7: FROZEN
PACK VERSION: 1.8.1
```

`library/packs/pp/` is frozen for the pilot.

## A15. Commit boundary and Step 8

The initial gate recorded that the entire Step 1–7 body of work was an uncommitted working tree — the
single largest operational risk into a pilot, and the reason §24 provenance had to fall back on file
mtimes instead of byte identity. That is resolved at this checkpoint: Step 8 starts from a frozen,
recoverable Step-7 baseline, and from here git — not mtimes — proves what changed.

**Step 8 — Real Engagement Pilot** is next and is **not** executed in this pass. It tests empirical
usability and runtime behaviour. It is not another authoring redesign phase. Two things to watch,
carried forward as observations rather than defects: whether the 438-line Options spine is the right
resident size in a live round, and whether the `half_lives_override: {}` question the manifest
deliberately left OPEN can be calibrated from real engagement decay rather than invented.

---

```text
STEP 7 — BOUNDED CLEANUP / TARGETED RE-GATE: PASS
INITIAL STEP 7 VERDICT: FAIL
CHAIRMAN LEGACY BRANCH SERIALIZATION: ABSENT
DUPLICATE OPTIONS SERIALIZATION AUTHORITIES: 0
ACTIVE RETIRED ARCHITECTURE MODEL REFERENCES: 0
ACTIVE OLD SCORED/BRANCH DECISION SEMANTICS: 0
SOLUTION-ARCHITECT RETIRED MEMORY TOKENS: 0
SELECTABLE RETIRED PP PACKS: 0
MATERIAL ORPHAN RUNTIME ASSETS: 0
SUSPICIOUS NUMERIC FOSSILS: 0
ACTIVE UNSOURCED LABOUR RATE FALLBACKS: 0
DOCUMENTATION CLEANUP PERFORMED: YES
SEMANTIC AUTHORITY CYCLES: 0
SEMANTIC BYPASSES FOUND: 0
S-1 NORMAL PP TRACE: PASS
S-2 HEADLESS TRACE: PASS
S-3 NON-PP TRACE: PASS
S-4 DECISION-BLOCKED TRACE: PASS
P-1...P-18 INTEGRITY COVERAGE: 18/18
FULL REGRESSION TESTS: 704
FULL REGRESSION FAILURES: 0
STEP 3 SEMANTICS CHANGED: NO
STEP 4 SEMANTICS CHANGED: NO
STEP 5 SEMANTICS CHANGED: NO
STEP 6 SEMANTICS CHANGED: NO
PACK VERSION: 1.8.1
PP PACK AUTHORING COMPLETE: YES
STEP 1–7 CLOSED: YES
READY FOR STEP 8 — REAL ENGAGEMENT PILOT: YES
```
