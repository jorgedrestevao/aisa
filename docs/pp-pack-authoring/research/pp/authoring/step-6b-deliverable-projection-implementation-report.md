# Step 6B — Deliverable Projection Runtime Implementation Report

<!--
provenance: AUTHORING (implementation report) · class: IMPLEMENTATION
authored: 2026-09-04 (Step 6B)
design authority: step-6a-deliverable-projection-model.md (FROZEN, incl. §40)
This report records what was BUILT. It changes no Step 6A semantics, reopens no Step 3,
Step 4 or Step 5 decision, performs no research and consults no external source.
-->

---

## 1. Implementation basis

| Aspect | Value |
|---|---|
| Authoritative design | `step-6a-deliverable-projection-model.md`, **FROZEN**, including the final bounded contract correction in **§40** |
| Step 6A cleanup applied | 1 (the stale dependency-graph statement, §6.2) + the freeze block appended |
| Design decisions re-opened | **0** |
| Step 3 / Step 4 / Step 5 reopened | **no** |
| New research performed | **no** |
| Web consulted | **no** |
| Canonical research modified | **no** |

**Step 6A §6.2 correction (documentation only).** The graph's `_synthesis/*` note said the layer
*"is authority for exactly one derived sentence"*. Replaced with the §40.3-consistent semantics:

> `_synthesis/*` is a bounded narrative projection. In the `not-authorized` case, architecture-story is
> the **durable carrier** for exactly one architecture-entry result whose **semantic authority** remains
> the architecture-entry gate. It is **not** architecture authority.

The graph is otherwise untouched. The freeze block was appended verbatim as specified.

---

## 2. Files modified

**17 runtime + documentation files, 1 new test module, 1 new report.** Line counts and change notes below reflect the state AFTER the final bounded source-authority repair (§30).

| # | File | Change |
|---:|---|---|
| 1 | `library/packs/pp/deliverable-templates/discovery-report.template.md` | REWRITE — 54 → 219 lines |
| 2 | `…/executive-report.template.md` | REWRITE — 60 → 277 lines |
| 3 | `…/solution-blueprint.template.md` | REWRITE — 55 → 228 lines |
| 4 | `…/implementation-spec.template.md` | REWRITE — 77 → 333 lines |
| 5 | `…/claude-design-brief.template.md` | REWRITE — 71 → 325 lines |
| 6 | `…/estimate.template.md` | REWRITE — 63 → 404 lines |
| 7 | `library/kernel/synthesis-templates/financial-story.template.md` | SPLIT — decision economics only |
| 8 | `…/architecture-story.template.md` | BOUNDED REWRITE — I-1 carriage + I-2 |
| 9 | `…/risks-and-assumptions.template.md` | BOUNDED REWRITE — epistemic carriage |
| 10 | `…/as-is.template.md` | consumer-contract correction only, narrative untouched (§27 → repaired §30) |
| 11 | `library/kernel/render-contract.md` | doctrine, layer contract, 6 contracts, applicability, gap label |
| 12 | `library/kernel/blueprint-contract.md` | I-1 entry-gate sentence (documentation) |
| 13 | `library/packs/pp/pack.yaml` | manifest: `activation`, `canonical_deliverable`, 1.7.0 → **1.8.0** |
| 14 | `.claude/skills/aisa-render/SKILL.md` | the executor: activation, transformations, estimate modes, skips |
| 15 | `.claude/skills/aisa-synthesize/SKILL.md` | financial split, I-1 carriage, I-2, epistemic carriage |
| 16 | `docs/ARCHITECTURE.md` | 14 replacements (documentation) |
| 17 | `docs/PACK_AUTHORING.md` | 2 replacements (documentation) |
| 18 | `.claude/tests/test_pp_deliverable_templates.py` | **NEW** — 200 tests: T-D1…T-D22 (181) + R-1/R-2 bounded repair (18) + 1 T-D13 phrase update |
| 19 | `.claude/tests/test_pp_architecture_templates.py` | 1 carry-forward test inverted + 1 added (§25) |
| 20 | `research/…/step-6a-deliverable-projection-model.md` | §6.2 cleanup + freeze block |
| 21 | `research/…/step-6b-…-implementation-report.md` | **NEW** — this file |

**Not modified, deliberately**: Step 3 registers · Step 4 knowledge units · **all Step 5 architecture
runtime** (`architecture-core.md`, the four fragments, `README.md`, `aisa-blueprint`) ·
`.claude/agents/chairman.md` (§26) · `library/packs/pp-backup/`.

**Authoring mechanics note.** `library/` is read-only at runtime (`pre-write-guard.py` fail-closed +
`settings.json` deny). All `library/` edits went through the sanctioned out-of-band path. One incident:
an inline shell-quoted edit YAML-round-tripped `claude-design-brief.template.md`, stripping its comment
blocks (39 → 17) and rewriting `activation: |` as `|-`. Detected by the test run, re-staged from source
and re-verified (39 comments, parses, slots correct). No other file was affected.

---

## 3. Six-template taxonomy

```text
library/packs/pp/deliverable-templates/
├── discovery-report.template.md
├── executive-report.template.md
├── solution-blueprint.template.md        # canonical: architecture-blueprint (alias)
├── implementation-spec.template.md
├── claude-design-brief.template.md
└── estimate.template.md
```

**Six files. No new deliverable. No fragment system. No inheritance. No router.** Asserted by
`test_exactly_six_deliverable_templates_exist`, `test_canonical_deliverable_values_are_the_six` and
`test_no_new_deliverable_no_fragment_no_inheritance_framework`.

| Runtime id / file | `canonical_deliverable` |
|---|---|
| `discovery-report` | `discovery-report` |
| `executive-report` | `executive-report` |
| `solution-blueprint` | **`architecture-blueprint`** (alias preserved, not renamed) |
| `implementation-spec` | `implementation-specification` |
| `claude-design-brief` | `claude-design-brief` |
| `estimate` | `estimate` |

---

## 4. Authority-source implementation

Every template declares the projection contract declaratively. All eleven affected templates parse as
**structured YAML**, so the tests assert on parsed fields, not greps.

Common fields implemented: `canonical_deliverable` · `activation` · `authority_sources` ·
`conditional_sources` · `forbidden_sources` · `permitted_transformations` ·
`forbidden_transformations` · `slot_conditions` · `epistemic_projection`.
Where applicable: `blocked_when` · `not_applicable_when` · `materiality` (Discovery) ·
`proof_obligation_carriage` · `selective_pulls` · `scope_rule` · `owns_calculation` +
`input_modes` (Estimate only).

**No routing logic is encoded.** No concern→deliverable map, no outcome→template map, no product map,
no load order. Asserted by `test_no_projection_router_is_introduced` and
`test_manifest_introduces_no_router`.

| Deliverable | Primary semantic authority |
|---|---|
| Discovery Report | `shared-understanding.md` (all five states) |
| Executive Report | `decisions.md` `D-NNN` |
| Architecture Blueprint | the `architecture:` block + the fixed architecture shape |
| Implementation Specification | the `architecture:` block + the **approved** UX blueprint |
| Claude Design Brief | the **approved** UX blueprint |
| Estimate | **itself**, for the calculation |

---

## 5. Projection transformation execution

The §40.1 distinction is implemented in `render-contract.md` and `aisa-render`:

```text
REASONING              → settles or changes upstream meaning        FORBIDDEN downstream
PROJECTION TRANSFORM.  → deterministically derives a downstream
                         representation from already-authoritative
                         inputs under the active contract           PERMITTED where declared
```

A transformation executes only when **deterministic**, **bounded**, **declared**, and **traceable**.
Fail any of the four and `aisa-render` refuses it and logs an open work item.

Implemented permitted transformations:

```text
architecture obligation        → implementation work package
proof obligation               → acceptance work package
implementation inventory       → estimate work unit
work units + estimation method → effort bands / ranges / arithmetic
approved UX blueprint          → generator-oriented screen block
```

**Layer roles**: synthesis narrates · the template declares · `aisa-render` executes. `aisa-render`
carries the boundary sentence verbatim — *Render executes a projection contract; it does not reason
beyond that contract* — plus an explicit "This skill is not an inference engine." **No new engine, no
new skill, no new state machine, no new router.**

---

## 6. Discovery rewrite

Projects, each in **its own state**: material Confirmed · material Assumed (basis, validity,
validator) · **Unknown** (own section, criticality, who answers) · **Conflicted** (both sides, neither
chosen) · **Risky** (risk + consequence) · **expired Confirmed as re-verification obligations** ·
perspective/tension findings · evidence still required · scope framing · analysed-source inventory.

**Materiality (§8.1)** implemented as a declared 7-class `survives_if_any` list plus the
`omission_rule`: omission is silent for Confirmed and **never** silent for Unknown / Conflicted /
Risky / Assumed — those carry a **counted residual**. No copy-all.

**Neutrality by construction**: zero vendor/product terms (13-term denylist asserted), zero Domain
Knowledge / CRAFT unit paths, and `decisions.md# D-NNN`, the architecture block and `options.md`
declared **forbidden sources**. `frame.md` / `D-001` is read for scope framing only.

The one benign raw-evidence read is **kept** and re-sourced to `_capture/evidence-index.md`, declared
as an *inventory, never a reinterpretation* (§3.2).

---

## 7. Executive rewrite

Primary authority: **`decisions.md`**. Projects: the decision + selected solution in plain language ·
**uncollapsed `(scope, outcome)` pairs** (verbatim, every marker) · conditions · preconditions ·
accepted risks · decision-changing proof obligations · structural open choices · tripwires · the
**recorded** justification · the **recorded** per-alternative *why not* lines · decision economics ·
one investment paragraph · major architecture shape where authorized.

**`options.md` whole-file read removed** and declared forbidden (I-2). The comparison invitation is
gone: the `rationale_rule` states the report reproduces *the justification the decision recorded* and
never explains why an architecture "won"; where the decision recorded no comparison, none is recorded.

**Non-omissible set** declared as a frontmatter list of 8 items, each `required subject to existence`:
three are `required` slots, five are `conditional` with an **existence** condition — so absent upstream
⇒ skip, present upstream ⇒ renders. `converting a condition into a satisfied state` is an explicit
forbidden transformation.

---

## 8. Architecture Blueprint rewrite

The direct human-readable projection of the **frozen** Step 5 Architecture Layer. Consumes the
`architecture:` block, the **fixed** `architecture-core.md` include (which itself resolves the 0..1
experience fragment and the N+M boundary instances), architecture-story narrative, decision basis, and
SU state/validity for display.

**Re-derives nothing**: authorization, experience, record authority, composition, scope relocation and
pattern are all in `forbidden_transformations`, as are scoring and selecting among candidates.

**Sheds duplicated altitudes** (D-16): `executive_summary` and `estimation_summary` removed as slots;
`_synthesis/financial-story.md` and the rendered Estimate are **forbidden sources**; the
architecture-level alternatives section is removed. A two-sentence `orientation` slot remains, declared
as *never an executive summary*.

**Scope ownership (I-3)** implemented as the four **render/projection categories** in the deliverable
layer — `architected here` · `relocated — boundary represented` · **`excluded — destination
unevaluated`** · `not applicable — no architecture authorization`. Declared as
`scope_ownership_categories` (exactly 4, asserted) with per-category `architecture_consequence`.
`architecture-core.md` was **not touched** — C6-B already proved behaviour correct.

---

## 9. Implementation Specification rewrite

*Architecture → build obligations and implementation contracts.* Architecture is declared
**READ-ONLY**, per section (A5, A3/A6, A4 marked read-only individually).

**Derivation rules implemented**, replacing the four defects:

| Slot | New authority | Replaced |
|---|---|---|
| test & proof work | `proof_obligations[]` → **one work package + one acceptance condition each**; friction may add *scenarios only, never the proof level* | D-7 |
| sequencing | architecture dependencies only (A3 · A8 · A9 · fragment cross-boundary release owner), **constraints only, no durations** | D-8 |
| migration & cutover | A9 replacement conditional + the class-14 outcome sentence + `access_mode` transitions | D-9 |
| screens | the **approved** UX blueprint only, **conditional** on `experience.mode != none`, no narrative fallback | D-12 |

All four old authorities are declared **forbidden sources** by name.

Preserved verbatim per proof obligation: *claim · V1–V4 · method · owner · funded?*. No re-grading, no
method substitution, no satisfaction marking.

**Migration boundary (§24)**: the Blueprint owns what is replaced, coexistence, the transition
architecture and architectural cutover dependencies; the Specification owns migration steps,
conversion, detailed cutover, sequencing/tasks, cleanup and rollback. **No separate migration
deliverable** — asserted.

**Headless (§16)**: `headless_behaviour` declares no required screens, no persona section, no
navigation, no UX placeholder — while still projecting automation, integration, identity,
environment/release, monitoring, recovery, proof work and operator obligations **in full**. *No fake
application surface.*

---

## 10. Claude Design Brief rewrite

Materially narrowed. Primary source: `_blueprint/ux-blueprint_v<approved>.yaml` + the approval id +
the **architecture constraints digest** + brand guidance + material user/accessibility rows +
selective CRAFT + one selective RESEARCH unit where UI-visible access-path semantics require it.

**The digest is a runtime selection, not an artefact**: declared as `architecture_constraints_digest`
with explicit `includes` (A1 scope · only the A3 rows a surface touches · UI-visible A5 access-mode
consequences · A7 identity/enforcement/roles · design-relevant A12 · A6 only where async state reaches
the UX) and `excludes` (A2, A6 internals, A8, A9, A10, A11, the six channels, the full A3 table, full
A5 detail). Declared *NOT a new artefact, NOT a new file, NOT a router, NOT an architecture reasoning
layer*; the test also asserts no such file exists.

**`architecture-core.md` in full is a forbidden source.** The six-unit characterised Domain Knowledge
table is **gone** — replaced by a `where_to_verify` pointer list and `selective_pulls` with
`point_of_need: true`. The test asserts no markdown table row begins with a knowledge-unit path.

**Applicability implemented exactly as §13.5** — and **no surface slot is `required`**: all seven live
in `conditional_slots`, each gated on `experience.mode`. Emitting a headless placeholder is an explicit
forbidden transformation. The "Canvas App" prose assumption was replaced by the recorded
`experience.primary_surface`.

---

## 11. Estimate rewrite

Declares `owns_calculation: true`, `semantic_owner: estimate`, `calculation_executor: aisa-render`,
and all four §40.4 structural obligations: `input_inventory_authority` · `method_authority`
(`craft/estimation-model.md`, method only, person-days) · `permitted_outputs` (work breakdown, bands,
ranges, contingency, confidence) · `forbidden_semantic_changes` (no scope change, no epistemic
promotion, no comparator claim, no invented work unit, no price).

`no_second_estimate_authority` states there is exactly one implementation-effort authority in the
runtime. `contingency_honesty` implements §14.4: every structural open choice and decision-changing
Unknown renders as a **named** uncertainty line — *item · effort it swings · what would settle it ·
`U-NNN`* — with contingency a number **over** the named items. Hiding an Unknown in contingency is a
forbidden transformation.

---

## 12. Estimate modes A / B

`input_modes_count: 2`, `input_modes: {A, B}`, plus `no_third_mode`. Asserted to be exactly `{A, B}`.

**Mode A — implementation estimate.** Approved architecture + the Specification's inventory
(components, obligations, proof work, migration steps, open work items — **INVENTORY ONLY**: no
narrative, no rationale, no architecture description, no acceptance text). Scope control: *when a
Specification exists, no work unit absent from it may be added*; a needed-but-absent unit is an **open
work item** against the Specification (owner `implementation`).

**Mode B — candidate planning estimate.** Available only where all three hold: candidates exist AND
approval is blocked by the unresolved structural choice AND the sponsor materially needs comparative
delivery magnitude. Mandatory label declared **verbatim** (and asserted verbatim in both the
frontmatter and the rendered body):

> Candidate planning estimate — pre-Implementation-Specification; lower-confidence; architecture choice
> unresolved.

Per-candidate isolation: own inventory, own estimate, own uncertainty, own confidence. *NEVER blend
candidates. NEVER select a candidate. NEVER rank them.* `may_not_estimate` names the four
prohibitions, and `scope_control` carries `no spec != permission to invent a spec`.

**Neither basis present** ⇒ blocked or not applicable. Never a placeholder, never a guess.

---

## 13. Financial synthesis split

`financial-story.template.md` now carries **decision-economics narrative only**. Declared
`computes_implementation_effort: false` and `owns_calculation: false`, with a `forbidden_outputs` list
naming the phased build plan, per-phase effort table, timeline/Gantt, effort summary in days,
team-by-profile table, operational-impact delta, any person-day figure, any derived total duration and
delivery recommendations.

**The six calculation sections were physically removed** — `## Phased build plan`,
`## Detailed estimate by phase`, `## Timeline`, `## Effort summary by phase`,
`## Team and effort by profile`, `## Estimate headline` — asserted absent. **No second synthesis file
was created.** The surviving `## Investment reference` section may only cite an already-produced
Estimate and states *never derive a figure here*.

`aisa-synthesize` carries a matching "Synthesis computes no implementation estimate" section.

---

## 14. I-1 — authority / carriage split

```text
outcome basis           semantic owner: the Options layer that emitted the sentence
                        durable source: decisions.md

architectability basis  semantic owner: THE ARCHITECTURE-ENTRY GATE RULE
                        durable carrier: _synthesis/architecture-story.md
```

Implemented in four places:

1. **`architecture-story.template.md`** — `is_architecture_authority: false`; a `carriage` block with
   `role: durable carrier`, `is_semantic_authority: false`, `semantic_owner: the architecture-entry
   gate rule`, `exception_scope: this one basis only`; the section header says **DURABLE CARRIER — NOT
   SEMANTIC AUTHORITY**; the five carrier limits are stated; *only carriage exception* is stated.
2. **`blueprint-contract.md`** — the §21.4 entry-gate sentence, ending *no new artefact, no empty
   blueprint, no new field*.
3. **`executive-report.template.md`** — a `not_authorized_carriage` block with both halves' semantic
   owner and durable source/carrier, and a note reading *DURABLE CARRIER, NOT SEMANTIC AUTHORITY …
   never re-evaluates pack architectability*.
4. **`aisa-render` + `aisa-synthesize`** — both state the split and both forbid re-evaluating pack
   architectability.

**Positive non-PP decision**: the decision and the architectability reason are preserved; relabelling
it `Decision Blocked` is a forbidden transformation; implying the platform "lost" and inferring the
selected solution's fit or cost are both forbidden. **Step 5 untouched** — no new artefact, no empty
blueprint, no new field, `aisa-blueprint` unmodified.

---

## 15. I-2 — comparison invitation removed

| Location | Change |
|---|---|
| `architecture-story.template.md` §*Chosen architecture* | *"and why it won over alternatives"* → *"and the justification the decision recorded (`decisions.md# D-NNN — Justification`), reproduced verbatim in substance. Create no new comparison."* |
| `executive-report` alternatives | source constrained to the **recorded** per-alternative *why not* lines; "creating any new option comparison, ranking, score or superiority claim" is a forbidden transformation |
| `executive-report` `decision_options` | the whole-file `options.md` slot is **removed**; `options.md` as a whole-file read is a declared forbidden source |
| `solution-blueprint` `alternatives_considered` | **removed** — comparison lives at decision altitude |
| `estimate` §Recommendations | constrained to **delivery** recommendations only; no option or economic-attractiveness claim |

Comparator **status** markers (`COMPARATIVE FIT UNEVALUATED`, `INCUMBENT FIT UNEVALUATED`, class 9's
single-axis evidence) are preserved verbatim as recorded facts — explicitly not a comparison.

---

## 16. I-3 — scope-ownership projection categories

Four render categories implemented in the deliverable layer (§8 above). Declared as
`scope_ownership_categories` on the Architecture Blueprint and mirrored as
`pricing_by_scope_category` on the Estimate (4 entries) and `scope_rule` on the Implementation
Specification. They are **projection categories** — not states, not outcome classes, not epistemic
values — and the tests assert exactly four, no fifth, and none inferred from another.

`architecture-core.md`'s angle-bracket column hint was **not** touched (explicitly unauthorized).

---

## 17. Epistemic carriage

Every deliverable declares an `epistemic_projection` block covering all five states, asserted
per-deliverable. Tests additionally assert that:

- **expired Confirmed** is never projected as fact by any deliverable;
- **Conflicted** is projected as *neither side chosen* by every deliverable;
- no template instructs a promotion — the phrase scan is **negation-aware**, so a template may state
  the prohibition without tripping it;
- Discovery carries all five states in their own required sections, with counted residuals;
- `aisa-render` states the binding rule *Deliverable brevity cannot upgrade epistemics*.

**Volatile values**: `aisa-render` requires `value · verificado_em · validade`, or a verification
obligation where invalid/expired, and forbids introducing a live platform fact or using a template as
a fact store.

`risks-and-assumptions.template.md` gained *Expired validity — re-verification obligations*,
*Conditions and preconditions the decision recorded* and *Proof obligations*, declared
`is_authority: false` with `always_retain: [id, state, verificado_em/validade]`.

---

## 18. Proof-obligation carriage

Implemented per §16 as a declared `proof_obligation_carriage` block on the five obligation-carrying
deliverables (Discovery carries **evidence gaps** instead, as designed):

| Deliverable | Scope | Form |
|---|---|---|
| Executive | decision-changing only | claim · why it qualifies · owner · funded? |
| Architecture Blueprint | **all** architecture obligations | the five-part shape |
| Implementation Spec | **all, translated** | one work package + one acceptance condition each |
| Claude Design Brief | UX / design validations only | what must be validated · against what |
| Estimate | the **effort** for the proof work | work unit + effort + uncertainty |

No deliverable changes the V-level, method, owner or funded state, and none marks an obligation
satisfied — asserted both positively (the prohibition is declared) and negatively (no re-grading
instruction exists).

---

## 19. Scope pairs and class 6

Pairs are preserved **uncollapsed** across Executive, Blueprint, Implementation Spec and Estimate;
`collapsing or re-wording a (scope, outcome) pair` is a forbidden transformation on the Executive.

For the mandatory class-6 case (`S → class 2 → PP authorized`; `R → class 6 → class 8, destination
UNEVALUATED`):

| Deliverable | Implemented behaviour |
|---|---|
| Executive | states the exclusion + the UNEVALUATED candidate status; markers verbatim |
| Blueprint | R appears **exactly once**, as scope-ownership **category 3** — no owner, no boundary component, no imports, no gates, no far-side design |
| Implementation Spec | no external R implementation — *no interface, no contract, no migration, no cutover to an unnamed counterparty*; the exchange point is an open work item naming the unselected destination |
| Design Brief | no R screen or journey — a forbidden transformation |
| Estimate | **never estimated**: no allowance, no placeholder, no contingency band; the exclusion is **stated** |

`render-contract.md` and `aisa-render` both carry *The far side never enters PP scope by silence.* No
reverse inference in either direction.

---

## 20. Applicability, skips and blocks

Declarative `activation` / `blocked_when` / `not_applicable_when` per template, mirrored in
`pack.yaml`. `aisa-render` reads them; it does not dispatch on them.

- **Headless Design Brief** → `not applicable`, logged as a skip. No persona/screen/navigation/UX slot
  emitted, no gap.
- **Not-authorized Architecture Blueprint** → `not applicable`, skip. *No empty architecture
  deliverable, no placeholder A-sections, no "architecture: none" document.*
- **Not-authorized Implementation Spec** → `not applicable` for that scope; produced for any other
  scope that carries a PP authorization.
- **Structural open choice** → Blueprint renders both candidates (approval blocked); Implementation
  Spec **BLOCKED**; Design Brief **BLOCKED, no exception**.
- **Decision blocked (class 12)** → Discovery + Executive only; the other four `not applicable`; no
  future implementation work invented.
- **Estimate outside estimation authority** → `not applicable` with the reason.

A `not applicable` deliverable is **never** written and **never** produces a `render-gaps.md` entry —
asserted in both the contract and the skill.

---

## 21. Render-gap terminology

**Four classes, unchanged in semantics.** Class 3's label generalized:

```text
architecture work item  →  open work item
owner ∈ { architecture | implementation | design | estimate | evidence }
```

Applied in `render-contract.md` and `aisa-render`; both state *No fifth class. No parallel taxonomy.*
The old label survives only inside the relabel note (*"the former architecture work item"*), which the
negation-aware test permits while forbidding a class row carrying it. The Implementation
Specification's `open_work_items` section renders the owner enumeration.

---

## 22. `pack.yaml`

| Change | Value |
|---|---|
| `pack_version` | **1.7.0 → 1.8.0**, with the rationale comment the pack's convention requires |
| Deliverables | 6, all template paths verified to exist |
| Added | `canonical_deliverable` per deliverable; `activation` per deliverable; `owns_calculation: true` on `estimate` |
| Removed | **`applies_to`** on all six (including the three `[technology]` values) |
| Router | none — the comment states no outcome→template map, no concern→deliverable map, no product map, no load order, no state machine |

`applies_to: [technology]` survives **only** inside the 1.8.0 rationale comment explaining why it was
the wrong discriminator; the test asserts every line mentioning it is a comment, and that no active key
declares routing.

---

## 23. Documentation

**`docs/ARCHITECTURE.md`** — 14 replacements: the `applies_to` bullet → declarative `activation` +
the authorization discriminator; the deliverable slot table rows 3–6 → the new contracts; the
`_synthesis/` rationale; the three synthesis-source rows (architecture-story as **durable carrier**,
risks expanded, financial **decision economics only**); the DK cross-refs bullet → selective,
point-of-need; the branch sub-template bullet → **six** bullets covering the fixed include, projection
contracts, the transformation test, the **exactly two bounded deliverable→deliverable edges**
(Implementation Specification → Estimate, **inventory only**; Estimate → Executive Report,
**headline / one investment paragraph only**) — **no third edge** — and the gap-class label;
the repo tree; the checklist; the migration table.

**`docs/PACK_AUTHORING.md`** — 2 replacements: the `architecture-templates/` tree comment, and §113's
branch-lookup paragraph → the fixed-include explanation plus a new *"Deliverable templates are
projection contracts"* section documenting all eleven frontmatter fields and the
deterministic/bounded/declared/traceable test.

`chosen_architecture`, `{{chosen_architecture}}` and `<chosen>.md` are gone from both, except inside
explicit removal notes (negation-asserted).

---

## 24. T-D1 … T-D22

`.claude/tests/test_pp_deliverable_templates.py` — **181 tests**, all passing. Structural where
meaningful: frontmatter is **parsed** and asserted as data whenever the claim is about a declared
contract field; phrase assertions normalize markdown emphasis and blockquote wrapping; banned-token
scans are **negation-aware** so a contract may state its own prohibitions.

| Id | Tests | Result |
|---|---:|---|
| baseline (six contracts well-formed) | 5 | PASS |
| **T-D1** no branch vocabulary | 7 | PASS |
| **T-D2** headless | 8 | PASS |
| **T-D3** not-authorized → no Blueprint | 6 | PASS |
| **T-D4** class-6 undesigned / unestimated | 7 | PASS |
| **T-D5** scope pairs preserved | 7 | PASS |
| **T-D6** Executive conditions cannot disappear | 5 | PASS |
| **T-D7** Spec cannot change architecture | 11 | PASS |
| **T-D8** Design Brief cannot re-select | 7 | PASS |
| **T-D9** Estimate ≠ economics | 7 | PASS |
| **T-D10** epistemics never promoted | 9 | PASS |
| **T-D11** proof levels not re-graded | 8 | PASS |
| **T-D12** multiple architectures stay multiple | 4 | PASS |
| **T-D13** read graph | 6 | PASS |
| **T-D14** the two blueprints | 4 | PASS |
| **T-D15** selective DK / CRAFT | 8 | PASS |
| **T-D16** manifest coherence | 6 | PASS |
| **T-D17** gap-class integrity | 6 | PASS |
| **T-D18** Discovery neutrality | 6 | PASS |
| **T-D19** calculation ownership *(mandatory)* | 13 | PASS |
| **T-D20** carriage split *(mandatory)* | 7 | PASS |
| **T-D21** structural block *(mandatory)* | 7 | PASS |
| **T-D22** two input modes *(mandatory)* | 11 | PASS |
| complexity guard (no router / state machine / docs) | 6 | PASS |
| **Total (canonical)** | **181** | **PASS** |
| R-1 · R-2 bounded repair classes (§30, outside the T-D numbering) | 18 | PASS |
| **Total (suite)** | **200** | **PASS** |

**Coverage: 22/22.** The four mandatory tests prove exactly what §45–§48 require, including: the
Estimate's four structural declarations; `aisa-render` as sole executor and its refusal of undeclared
computations; zero implementation-effort figures in synthesis and no second authority anywhere; the
three-way authority/carrier split with the words appearing distinctly; the full structural-block chain
with no override token outside a prohibition; and exactly two input modes with the mode-B label
verbatim in both frontmatter and body.

---

## 25. Regression results — **PRE-FINAL-SOURCE-AUTHORITY-REPAIR SNAPSHOT**

> **This section is a historical snapshot**, recorded **before** the final source-authority
> bounded repair of §30. It is retained deliberately, unaltered, so the audit trail shows the
> state at the first-pass close. **It is not the authoritative regression state.**
>
> **§30.7 is the authoritative final regression state:**
>
> ```text
> test_pp_deliverable_templates.py: 200
> full final regression: 566
> failures: 0
> ```


| Suite | Tests | Result |
|---|---:|---|
| `test_pp_deliverable_templates.py` (**new**) | 181 | **OK** |
| `test_pp_options_decision_model.py` (Step 3) | 95 | **OK** |
| `test_pp_domain_knowledge.py` (Step 4) | 64 | **OK** |
| `test_pp_architecture_templates.py` (Step 5) | 116 | **OK** |
| `test_pp_discovery_runtime.py` (Step 2) | 22 | **OK** |
| `test_council_wiring.py` | 31 | **OK** |
| `test_orchestrator_wiring.py` | 23 | **OK** |
| `test_state_scaffold.py` | 15 | **OK** |
| `library/kernel/tools/tests/test_text_extract.py` | 23 | **OK** |
| **Total** | **570** | **0 failures** |

**Step 3: PASS** — no decision semantics changed. **Step 4: PASS** — no knowledge unit touched; pull
boundaries tightened, never widened. **Step 5: PASS** — after two repairs, both traceable to Step 6B
and neither a semantic regression:

1. `test_authorization_read_never_derived_or_upgraded` required *"never derived, upgraded or
   downgraded"* in `aisa-render`. The rewrite had dropped the sentence. **Runtime restored** — the
   Step 5 contract wins; the phrase is back at the architecture-include step.
2. `test_step6_carry_forwards_are_known_and_bounded` **pinned** the three deliverable templates as
   still carrying the branch contract — a deliberate Step 5B carry-forward marker (its own docstring
   said *"Step 6, not a 5B failure"*). Step 6B resolved it, so the assertion was **inverted** to
   require the set be empty, and a second test was added asserting the replacement is exactly one
   fixed include. This tracks a migration; it changes no Step 5 semantics.

Per §49, the full semantic T01–T18, Step 4C and Step 5C replays were **not** run — no semantic
regression appeared.

---

## 26. Carry-forwards

| # | Item | Disposition |
|---:|---|---|
| **CF-1** | `Branch (if technology)` in `.claude/agents/chairman.md` §*Options → options.md* | **OUT OF STEP 6B SCOPE**, per §43. **Not modified.** Mitigated structurally: the Executive Report no longer reads `options.md` whole-file (it is a declared forbidden source), and **no deliverable projects that field**. Recorded as an **owning-line carry-forward** for the Options line. Step 3 remains frozen. |
| **CF-2** | `architecture-core.md`'s scope-ownership angle-bracket column hint | Deliberately **not** touched — explicitly unauthorized. The deliverable-side enumeration makes it unnecessary; C6-B proved behaviour already correct. Optional documentation-only follow-up. |
| **CF-3** | `--html` interrogable projection for the other five deliverables | Unchanged v3.1 scope; Discovery only in v3.0. |
| **CF-4** | `pack.yaml` `epistemics.half_lives_override: {}` | Untouched Step 4B open item. |

---

## 27. Deviations

Three, all bounded and recorded rather than silent:

**DV-1 — `as-is.template.md` received a one-line change. → REPAIRED, see §30.** Step 6A §2.2 classified it **KEEP**, and its
content is unchanged. But its `synthesis_prompt` named the *Solution Blueprint* as a consumer, and in
the target model `_synthesis/as-is.md` is a **forbidden source** for the Architecture Blueprint and
forbidden as the source of acceptance work in the Implementation Specification (D-7). The stale
consumer line was corrected to name its real consumers (Discovery Report as authority; the Estimate's
operational-impact **timings only**) and to state the two prohibitions. Source-contract coherence, not
a content rewrite. `business-story.template.md` needed nothing and was not touched.

> **DEFECT — and its repair.** The second half of that correction was **wrong**: naming the Estimate a
> consumer of `_synthesis/as-is.md` created a source edge the frozen Step 6A Estimate contract
> (§28.6, §14.1, §18.1) does not authorize, and the Estimate template carried it as a live
> `slot_sources` entry. Repaired in the final bounded pass — **§30**. The first half (Discovery
> Report) was also mis-worded as *authority*; corrected to *consumer / projection*. This entry stays
> as written so the audit trail shows both the deviation and its closure.

**DV-2 — two deliverable→deliverable read edges exist, not one. → CLARIFIED, not a defect; see §30.** §6.2/§6.5 count one
(`impl-spec → estimate`, inventory only). But §5's *effort estimate* row, §28.2 and §34 all
independently authorize the Executive Report to project **the Estimate's headline** as one investment
paragraph. Both were implemented; the Executive's forbidden-source line states the Estimate headline is
the **only** exception. T-D13 asserts the edge set is exactly those two and that the graph is
**acyclic** (verified by traversal). No cycle exists, and no other deliverable reads a `_render/` file.

> **Adjudicated: NOT a semantic defect.** The frozen model independently authorized both edges. The
> discrepancy was a **documentation count**, corrected in §30: `render-contract.md` and
> `docs/ARCHITECTURE.md` now state *exactly two bounded deliverable→deliverable edges, and no third*,
> each with its bounded payload. No runtime was altered for the count. Behavioural confirmation
> (including render-order invariance) remains a Step 6C probe.

**DV-3 — Executive `proof_obligation_carriage` was added during the repair pass.** §16 requires the
Executive to carry decision-changing obligations; the first pass declared the slot but not the carriage
contract. Added. Classification **B** (projection authority defect), repaired without touching frozen
semantics.

---

## 28. Failures and classification

First full run: **181 tests, 23 failures.** Classified per §51, repaired smallest-defect-first, with no
fixture-driven redesign and no frozen-semantics change.

| Class | Count | Nature | Repair |
|---|---:|---|---|
| **A** — deliverable implementation defect | 5 | Contract facts sat in **YAML comments**, so they were not part of the declared contract a renderer or test can read (impl-spec `PRIMARY`; blueprint no-re-pull; design-brief two-blueprints warning; estimate mode-A inventory payload; design-brief CRAFT boundary) | Moved into declared values |
| **B** — projection authority defect | 2 | Executive lacked `proof_obligation_carriage`; Discovery/Executive/Estimate did not forbid another deliverable's narrative as authority | Declared both |
| **C** — epistemic projection defect | 0 | — | — |
| **D** — transformation-boundary defect | 0 | — | — |
| **E** — applicability defect | 1 | Design Brief surface slots were `required`, violating §13.5 / T-D2 | Moved to `conditional_slots` |
| **F** — estimate ownership defect | 0 | — | — |
| **G** — Step 3 regression | 0 | — | — |
| **H** — Step 4 regression | 0 | — | — |
| **I** — Step 5 regression | 0 | 2 Step 5 test failures, both Step 6B consequences, neither a semantic regression (§25) | 1 runtime sentence restored; 1 migration-tracking test inverted |
| **J** — frozen Step 6A ambiguity | 0 | DV-2 is a **count** discrepancy inside §6 vs §5/§28.2/§34, resolved by implementing what three sections authorize and asserting acyclicity. No semantic ambiguity blocked implementation | recorded, not escalated |
| **Test-side defects** | 15 | Assertions that did not match authored wording, or were not negation-aware (a contract legitimately contains the token it forbids); plus markdown emphasis / blockquote wrapping breaking phrase matches | `flat()` now normalizes emphasis + nested blockquotes; a shared `only_in_prohibition()` helper replaces four ad-hoc window checks; 12 phrase corrections |

One infrastructure incident (not a test failure): the YAML round-trip that stripped the Design Brief's
comments, detected by the test run and repaired by re-staging (§2).

**No blocker (G/H/I) and no §51-J stop condition arose.**

---

## 29. Recommendation for Step 6C

**Proceed to Step 6C.** Step 6B proves the projection model is **mechanically implemented**: six
contracts, one primary semantic authority per information class, no legacy branch lookup, the
calculation owned by the Estimate and executed only by `aisa-render`, synthesis computing no effort,
two input modes, the authority/carrier split, and the four hard negatives answered by applicability
gates and render categories rather than new machinery.

It does **not** prove the six deliverables stay semantically aligned under realistic engagement
pressure. **Step 6 is not frozen by these mechanical tests.**

Step 6C should run the eight designed fixtures (DF-1 … DF-8) with the §37.1 cross-fixture assertions,
and priority attention on:

1. **DF-3 adversarial Design Brief check** (§37.1 item 6) — an evaluator asserting *"the unresolved
   structural choice is not UX-material, so the brief can proceed"*. Correct behaviour is **BLOCKED**;
   a run that produces a brief fails DF-3 regardless of quality. The structural implementation forbids
   it, but only a behavioural run proves the reasoner honours it.
2. **DF-3 candidate-estimate check** (§37.1 item 7) — one labelled block per candidate, zero blended
   figures, zero spec-level tasks, zero screen-level work.
3. **DF-7 / C6-B** — category 3 rendered exactly once, and no reverse inference in either direction.
4. **DF-8** — the new discovery-heavy fixture: three Critical Unknowns, one unresolved Conflicted on a
   decision-critical volume, two accepted Risks, one expired Confirmed. Residual counting and
   non-promotion are structurally declared but behaviourally unproven.
5. **DV-2** — confirm the Executive's Estimate-headline projection stays a one-paragraph projection and
   never becomes a second effort authority.
6. **DV-1** — confirm the corrected `as-is` consumer boundary holds behaviourally (no acceptance work
   derived from friction).

Recommended additional adversarial probe, beyond the frozen fixture set: pressure the **mode-A scope
control** with an engagement whose architecture plainly implies a work unit the Specification omitted.
The correct output is an **open work item against the Specification**, not an Estimate line — the one
place where "helpfulness" most plausibly breaks the contract.

---

## 30. Final source-authority bounded repair (appended)

One bounded semantic repair plus a documentation-consistency correction. **No Step 6A semantics
changed. No Step 3 / Step 4 / Step 5 change. No deliverable model, Estimate mode, calculation
ownership, architecture-story carriage, class-6 behaviour, headless applicability, render-gap class,
pack version or chairman carry-forward touched.**

### 30.1 The defect

DV-1 had given the Estimate a read edge to `_synthesis/as-is.md`. The frozen Estimate source contract
authorizes only:

```text
MODE A   Implementation Specification inventory + craft/estimation-model.md + decision scope/conditions
MODE B   candidate architecture record + candidate-specific KNOWN obligations
         + craft/estimation-model.md + decision scope/conditions
```

`_synthesis/as-is.md` is **not** an Estimate authority, required source or conditional source. The
defect was live in three places in `estimate.template.md` (a `slot_sources` entry, a `slot_conditions`
precondition and a body anchor) and asserted as legitimate in one place in `as-is.template.md`.

### 30.2 What was changed

| File | Change |
|---|---|
| `estimate.template.md` | `slot_sources.operational_impact` re-sourced to the **active mode's authoritative inventory** (mode A: the Specification's inventory; mode B: the candidate's KNOWN obligations); `slot_conditions.operational_impact` no longer preconditions on as-is timings; `forbidden_sources` now names `_synthesis/as-is.md` as **NOT required, NOT conditional, NOT fallback, NOT point-of-need**, plus `_synthesis/business-story.md` and any discovery narrative; `forbidden_transformations` prohibits *as-is friction / timing / exception / discovery narrative → a new Estimate work unit*; body §16 rewritten with no as-is anchor |
| `as-is.template.md` | consumer contract only. The **Estimate is removed as a consumer** and declared a forbidden consumer in all four ways; the authorized effort path is stated (Specification inventory → mode A, or candidate-specific KNOWN obligation → mode B). Narrative content untouched |
| `aisa-render` | a *No discovery re-read* hard rule in the Estimate execution section, with the per-mode escape hatch |
| `render-contract.md` · `docs/ARCHITECTURE.md` | DV-2: *one* → **exactly two bounded** deliverable→deliverable edges, each with its payload and its exclusions |

**No replacement source edge was added.** `operational_impact` remains a **conditional** slot; where
the authoritative inventory carries no operating-path change, it is `not applicable`. The Estimate's
allowed-source fields now contain **zero** occurrences of `as-is` — the token appears only inside
`forbidden_sources` and `forbidden_transformations`.

### 30.3 The authorized path for operational-impact effort

```text
authoritative engagement fact / architecture obligation
        ↓
Implementation Specification work inventory
        ↓
Estimate Mode A
```

or, while architecture approval remains open:

```text
candidate-specific KNOWN architecture obligation
        ↓
Estimate Mode B
```

A discovery fact that should alter implementation work but is absent from the authoritative inventory
becomes — **mode A** — an **open work item against the Implementation Specification** (owner
`implementation`), never an Estimate line; **mode B** — usable only if already a candidate-specific
**KNOWN** architecture obligation, otherwise the **uncertainty is preserved**.
`no spec ≠ permission to invent a spec` is intact.

### 30.4 Discovery wording corrected

`as-is.template.md` said *"the Discovery Report reads this as an authority source"*. Corrected: the
Discovery Report is a **consumer** that **projects** this narrative, and **neither** the synthesis file
nor the Discovery Report is source authority. Authority stays upstream with the artefacts Step 6A
names — the **Shared Understanding** rows, the **capture / evidence index**, and the **framing**
record. A new test also asserts no deliverable or synthesis template labels the Discovery Report as
source authority.

### 30.5 Executive → Estimate semantics preserved

Unchanged and unexpanded: **one Estimate headline / one investment paragraph**. The Executive does not
read phases, work breakdown, team mix, detailed range derivation, contingency detail or candidate
inventories — each named as excluded in `render-contract.md` and asserted absent from the Executive's
`investment_summary` source. `investment_summary` stays **conditional**, so where the Estimate is
`not applicable`, blocked or not produced the Executive is **complete without an implementation-effort
paragraph** — no gap, no placeholder, no calculation in the Executive or in synthesis.

### 30.6 Tests

Two repair classes added **outside** the canonical numbering — **R-1** (Estimate does not consume the
as-is synthesis, 12 tests) and **R-2** (two bounded read edges, 6 tests). Suite: 181 → **200 tests**.
`T-D1…T-D22` remain **22/22**, unchanged in meaning and count; the only T-D edit was the phrase T-D13
quotes from `render-contract.md`, moved to the corrected two-edge wording.

R-1 proves: the Estimate names as-is in no allowed source field; it declares as-is forbidden four ways;
it forbids the discovery-narrative → work-unit transformation; the missing-fact path is an open work
item, not an Estimate line; `operational_impact` is sourced from the active mode's inventory only and
no new source edge was added; `aisa-render` does not use as-is as an Estimate input; `as-is.template.md`
names only the Discovery Report as consumer and carries no estimate content; and the as-is narrative
sections are intact.

Three test-side defects surfaced during the repair and were fixed: two blunt `assertOnlyProhibited`
checks that tripped on the as-is template's legitimate *statement of the authorized effort path*, and
T-D13's stale quoted phrase.

### 30.7 Regression

| Suite | Tests | Result |
|---|---:|---|
| `test_pp_deliverable_templates.py` | **200** | **OK** |
| `test_pp_options_decision_model.py` (Step 3) | 95 | **OK** |
| `test_pp_domain_knowledge.py` (Step 4) | 64 | **OK** |
| `test_pp_architecture_templates.py` (Step 5) | 116 | **OK** |
| `test_pp_discovery_runtime.py` · `test_council_wiring.py` · `test_orchestrator_wiring.py` · `test_state_scaffold.py` | 91 | **OK** |
| **Total** | **566** | **0 failures** |

Semantic Steps 3B2 / 4C / 5C were **not** replayed, as instructed.

### 30.8 Recorded for Step 6C

Render order was **not** redesigned — no mechanical test proves it broken. Recorded as a Step 6C
behavioural probe:

1. Where an Estimate exists, the Executive may project its **headline** only.
2. Where the Estimate is `not applicable` / blocked / not produced, the Executive must be **complete**
   without an implementation-effort paragraph — no gap, no placeholder, no calculation in the Executive
   or in synthesis.
3. **Order invariance** — where both are produced, `--all` and individual render sequencing must not
   produce two different Executive truths merely because the Estimate rendered earlier or later.
4. **Mode-A scope control under pressure** (carried from §29): an engagement whose architecture plainly
   implies a work unit the Specification omitted must yield an **open work item**, not an Estimate line.

---

`STEP 6B — DELIVERABLE PROJECTION IMPLEMENTATION: PASS`
`CANONICAL DELIVERABLE TEMPLATES: 6/6`
`LEGACY CHOSEN-ARCHITECTURE RUNTIME REFERENCES: 0`
`PROJECTION CONTRACTS IMPLEMENTED: 6/6`
`DISCOVERY FIVE-STATE PROJECTION: PASS`
`EXECUTIVE NON-OMISSIBLE DECISION CONTENT: PASS`
`ARCHITECTURE BLUEPRINT PROJECTS FROZEN STEP 5: PASS`
`IMPLEMENTATION SPEC MAY CHANGE ARCHITECTURE: NO`
`HEADLESS DESIGN BRIEF: NOT-APPLICABLE`
`STRUCTURAL OPEN CHOICE DESIGN BRIEF: BLOCKED`
`DESIGN BRIEF DOMAIN-KNOWLEDGE PRELOAD PRESENT: NO`
`ESTIMATE SEMANTIC OWNER: ESTIMATE`
`ESTIMATE CALCULATION EXECUTOR: AISA-RENDER`
`SYNTHESIS COMPUTES IMPLEMENTATION ESTIMATE: NO`
`ESTIMATE INPUT MODES: 2`
`CANDIDATE ESTIMATES MAY BE BLENDED: NO`
`CANDIDATE MODE MAY INVENT SPEC TASKS: NO`
`S8 ECONOMICS AND ESTIMATE MERGED: NO`
`ARCHITECTURE-STORY IS SEMANTIC AUTHORITY FOR ARCHITECTABILITY: NO`
`ARCHITECTURE-STORY DURABLE CARRIER IMPLEMENTED: YES`
`SCOPE PAIRS PRESERVED: YES`
`CLASS-6 UNEVALUATED DESTINATION DESIGNED: NO`
`CLASS-6 UNEVALUATED DESTINATION ESTIMATED: NO`
`RENDER-GAP CLASSES: 4/4`
`T-D1...T-D22 STRUCTURAL COVERAGE: 22/22`
`STEP 3 REGRESSION: PASS`
`STEP 4 REGRESSION: PASS`
`STEP 5 REGRESSION: PASS`
`NEW RESEARCH PERFORMED: NO`
`NEW PROJECTION ROUTER INTRODUCED: NO`
`NEW STATE MACHINE INTRODUCED: NO`
`READY FOR STEP 6B REVIEW: YES`

---

`STEP 6B: CLOSED`
