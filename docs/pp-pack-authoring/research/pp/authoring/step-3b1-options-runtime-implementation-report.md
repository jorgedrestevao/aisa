# Step 3B1 — Options Runtime Implementation (report)

<!--
provenance: AUTHORING REPORT
date: 2026-09-04
scope: PP PACK AUTHORING — STEP 3B1. Implementation of the approved Step 3A design into the runtime pack.
design authority: step-3a-options-decision-model.md (final, incl. bounded correction record + micro-correction)
canonical Block D read (not reopened, not modified): decision-criteria.md §2.5, §4A, §5.2, §6.1–§6.4, §7.1–§7.3 ·
       decision-intelligence-matrix.md §3, §4, §5 · alternatives.md §2, §3, §5.1, §5.2, §5.3, §6
no research reopened · no web access · no canonical file modified
path note: `research/pp/authoring/` resolves to `docs/pp-pack-authoring/research/pp/authoring/`
NOT the G5 decision gate. This step proves implementation fidelity; Step 3B2 proves decision behaviour.
-->

---

## 1. Files created and modified

**Created — 7.**

| Path | What |
|---|---|
| `library/packs/pp/decision-model/alternatives-register.md` | 11 option classes · 29-row trigger→candidate map · symmetry rules · 5 forbidden universals · 10 symmetric unknowns |
| `library/packs/pp/decision-model/blocking-set.md` | 28 blocking entries + 3 scope-blockers, each with closure pattern, expected evidence form, role type, `custo` default and per-resolution outcome |
| `library/packs/pp/decision-model/composed-disqualifiers.md` | The 12 registered composed rows + the emergent-combination rule |
| `library/packs/pp/decision-model/outcome-classes.md` | The closed 14 with render templates · class 7 reason discriminator · class 13's two forms · scope pairs · comparator separation · recommendation semantics |
| `library/packs/pp/decision-model/volatility-register.md` | 10 commercial + 20 service-limit entries with per-row re-verify triggers · the live conflict · 3 dated tripwires |
| `library/packs/pp/architecture-templates/README.md` | Positioning only: shapes reachable **after** an outcome, never the option space |
| `.claude/tests/test_pp_options_decision_model.py` | 93 structural/mechanical tests |

**Modified — 8.**

| Path | Change |
|---|---|
| `library/packs/pp/decision-tree.md` | **REWRITTEN** as the Options spine (filename kept — four consumers reference it) |
| `library/packs/pp/pack.yaml` | `constraints_to_check` → the approved 10 with the non-limiting comment · new `decision_model:` block · `decision_tree` comment · `pack_version` 1.4.0 → **1.5.0** |
| `.claude/skills/lens-technology/SKILL.md` | Execution step 2 (the two Q-11 clauses) + three consequential wording fixes. Net line delta **0** |
| `.claude/agents/solution-architect.md` | Options mandate re-pointed at the option-class model; pull clause extended to the registers. 3,565 → **3,193 chars**, inside the Phase E budget |
| `.claude/skills/chairman-synthesis/SKILL.md` | `options.md` template → the approved per-option and round-level structure + 8 output rules |
| `library/packs/pp/glossary.md` | **Part C** added — 4 new Options terms + 2 reuse notes |
| `library/packs/pp/question-bank.md` | *Reachable outcomes* block rewritten against the closed set. No question added, changed or removed |
| `library/packs/pp/architecture-templates/{sharepoint-first,dataverse-first,hybrid}.md` | Front-matter `scope: architecture-shape` + `available_after_outcome` + one positioning line each. **No architecture content touched** |

**Deliberately not created**, per Step 3A §24: `criteria-register.md` · `exit-classes.md` · `comparator-rules.md` ·
`validation-levels.md` · `anti-pattern-register.md`. A test asserts each is absent.

**Untouched**: `library/kernel/**` · `domain-knowledge/**` · `deliverable-templates/**` · the six Discovery
lens skills · the six Discovery personas · `aisa-options` · `aisa-simulate` · `aisa-frame` · every hook ·
`settings.json` · all canonical research · everything under `projects/`.

**Landing mechanics.** `library/**` is deny-listed for `Write`/`Edit` and guarded by `pre-write-guard.py`;
files were authored in the session scratchpad and copied in via `Bash` on branch
`pp-pack-authoring/step-2-discovery-layer`. Nothing committed — presented for review.

---

## 2. Spine implementation

`decision-tree.md`: 157 lines of scored branches → **436 lines of procedure**, carrying exactly the
sixteen required sections and nothing else.

| # | Section | Where |
|---:|---|---|
| 1 | Purpose / Options-only phase gate | §1 |
| 2 | Governing decision doctrine | §2 |
| 3 | Decision semantics | §3 |
| 4 | Evidence-grade rule for disqualifiers | §4 |
| 5 | 12 material decision concerns | §5 |
| 6 | 10 ordered stages S0–S9 | §6 |
| 7 | Broad coverage / selective depth | §7, §7.1 |
| 8 | D0–D3 semantics | §7.2 |
| 9 | Emergent-concern obligation | §7.3 |
| 10 | Stage-local register references | §8 |
| 11 | Domain-knowledge pull rule | §9 |
| 12 | Cross-domain / composed reasoning | §10 |
| 13 | Volatile-fact boundary | §11 |
| 14 | Validation levels | §12 |
| 15 | Comparator discipline | §13 |
| 16 | Outcome / render handoff | §14 |

**What was removed and stayed removed.** The `branches:` front-matter · the 15-slot `inputs_used:`
signature · the aggregated-score sentence · every R0 threshold (30,000 rows · `formula_count > 100` ·
`external_integrations_count > 3` · sub-second · 2-decimal currency · >3 approval states) · the R1–R6
ordinal ladders · the R4 licensing rules · the hybrid entity-count arithmetic · the stale changelog.
A test greps the whole spine for any figure carrying a unit and asserts the result is empty.

**What was kept.** The Options-only phase gate · the disqualification-before-direction order · the
missing-inputs protocol (upgraded into S3) · the do-nothing + non-technology floor (promoted from a
chairman appendix to a mandatory S1 member).

**Concerns and stages stay distinct.** §5 is coverage, §6 is order; the spine states that several
concerns are evaluated at more than one stage and vice versa. Neither was collapsed into a checklist.

**Also implemented in the spine, not in a separate file** (per Step 3A's merge decisions): the exit-scope
semantics and the not-an-exit classes (§3), the four validation levels (§12), the comparator separation
(§13). The S8 ten cost dimensions and the two standing rules — the S3 re-check after S8 and the
reachability floor — are in §6.

---

## 3. Register implementation and counts

| Register | Content implemented | Count | Verified by |
|---|---|---:|---|
| `alternatives-register.md` | Option classes `ALT-001…011` with plain-language renderings | **11** | `test_eleven_option_classes` |
| | Trigger→candidate rows | **29** | `test_trigger_rows_present` |
| | Forbidden universal claims | 5 | `test_forbidden_universals_registered` |
| | Symmetric unknowns | 10 | `test_symmetric_unknowns_registered` |
| `blocking-set.md` | Blocking entries `B-01…B-28` | **28** | `test_twenty_eight_blocking_entries` |
| | Scope-blockers `BS-01…BS-03` | **3** | `test_three_scope_blockers` |
| `composed-disqualifiers.md` | Registered rows `CD-01…CD-12` | **12** | `test_exactly_twelve_registered_rows` |
| `outcome-classes.md` | Closed outcome set | **14** | `test_closed_set_of_fourteen` |
| `volatility-register.md` | Commercial `VC-01…VC-10` | **10** | `test_ten_commercial_entries` |
| | Service-limit `VS-01…VS-20` | **20** | `test_twenty_service_entries` |
| | Dated tripwires `TW-V1…TW-V3` | 3 | `test_dated_tripwires_present` |

**`alternatives-register.md`.** Opens with the one governing rule — *a trigger generates a candidate, it
never produces a verdict*. `ALT-002` and `ALT-010` are declared **mandatory members of every candidate
set, generated at S1**, always serious, never eliminated by a finding about `ALT-004`; `ALT-004` is
declared **not the default candidate**. The agent-surface row renders **decision blocked, not a candidate
set** — fit is `UNKNOWN` in every class including `ALT-004`. The comparator marker is carried on every
row except the deployment-model row. §3.2 states the capability gates cut hardest against `ALT-005`,
`ALT-006` and `ALT-009` and requires the output to say that this is **a documented gap in those classes,
never an advantage of `ALT-004`**.

**`blocking-set.md`.** Opens with the pack-authored ÷ engagement-resolved split table. Every entry
carries: what must be known · why proceeding is unsafe · the closure **pattern** → the expected **form** ·
the likely **role type** · a `custo` default from the kernel vocabulary · and **what each resolution
produces**. `swing: decisivo` is declared by construction rather than repeated 31 times. The file states
in its own header that it is **not a questionnaire** and is consulted at S3 only. §3 records the two ways
this register is misread: membership is not the only route to *decision blocked*, and non-membership is
not permission to skip a concern.

**`composed-disqualifiers.md`.** The 12 rows carry participating conditions, scope, consequence and
reachable outcome. Rows `CD-06` and `CD-09` keep their **conditional** mappings verbatim in substance —
`CD-06` reaches *fit with constraints* on the named condition or *decision blocked* on unknown
propagation and **never** an exclusion; `CD-09` is **sponsor-side** and reaches *do nothing / defer* or
*decision blocked* and **never** a platform exclusion. `CD-11` is *migration required*, not an exclusion.
The register declares itself **closed at twelve**; §2 makes emergent combinations evaluable as `Risky`
rows and explicitly forbids promoting one into the register at runtime.

**`outcome-classes.md`.** The closed 14 with a render template each, the settled-exclusion list
(5, 6, 7, 9, 14) bound to the evidence-grade rule, the scope-pair rule, what redirects and combination
inputs may and may not reach, class 7's discriminator (§4 below), class 13's two forms (§3 of that file),
the four-part comparator separation, and the recommendation semantics. Closure is stated as a **testable
property**: any label not in the table is a defect in the emitter.

**`volatility-register.md`.** Thirty entries, each with its own re-verify trigger; the live 20× conflict
with its symmetry statement; three dated tripwires with what each changes and what to do when it fires.
§5 states what the register does **not** do — it supplies no figures, is not a checklist, and creates no
exclusions.

---

## 4. Stage-local loading

Implemented in three places that must agree, and a test asserts they do.

| Stage | Register | Declared in the spine | Declared in `pack.yaml` |
|---|---|:--:|:--:|
| S1 | `alternatives-register.md` | ✅ §8 | ✅ `decision_model.alternatives.stage: S1` |
| S3 | `blocking-set.md` | ✅ §8 | ✅ `decision_model.blocking.stage: S3` |
| S6 | `composed-disqualifiers.md` | ✅ §8 | ✅ `decision_model.composed.stage: S6` |
| S9 | `outcome-classes.md` | ✅ §8 | ✅ `decision_model.outcomes.stage: S9` |
| — | `volatility-register.md` | ✅ §8, on-demand only | ✅ `decision_model.volatility.loading: on-demand`, **no `stage` key** |
| S0, S2, S4, S5, S7, S8 | **none** | ✅ §8 explicit row | — |

Each register's own header repeats its consuming stage, so a file opened on its own still declares its
loading rule. The spine carries *"No preloading, and no router"* verbatim and notes the two consequences
Step 3A required: a register may be **re-consulted** at a later stage, and **S5 — the widest stage —
reads no register at all**. `pack.yaml`'s block comment states the same. No routing file exists; a test
asserts no filename under `decision-model/` contains `rout`.

`lens-technology` and `solution-architect` were both updated to name *the stage you are executing and the
register that stage names*, and both keep *never preload*. `aisa-options`'s *"never place
`decision-tree.md` or `domain-knowledge/` contents in the prompt"* was **not** modified — it was correct
and is what Principle 7 rests on.

---

## 5. Evidence semantics

Implemented verbatim in spine §4, with the responsibilities kept apart:

```text
evidence grade      → determines whether an exclusion can be SETTLED
materiality / swing → determines whether unresolved uncertainty BLOCKS the decision
```

| Evidence state | Settles a hard exclusion | Implemented consequence |
|---|:--:|---|
| `Confirmed` + current | **YES** | Render the exclusion at its scope |
| `Assumed`, not decision-changing | **NO** | Provisional disqualifier, carried with its basis; **does not** block merely for being `Assumed`; where an independent `Confirmed` + current disqualifier exists, the settled exclusion rests on **that** and the assumption is corroboration only |
| `Assumed`, decision-changing | **NO** | Provisional + evidence obligation (expose · name the evidence and its form · `Unknown` with `swing: decisivo`) → **decision blocked** where the recommendation could change |
| `Unknown` | **NO** | Evidence obligation; blocked where decision-changing |
| `Conflicted` | **NO** | Evidence obligation naming both readings; blocked where decision-changing |
| Materially expired | **NO** | Reads as **weak `Assumed`**; may never be cited as `Confirmed`; revalidate |

**Settled exclusions.** Spine §4 and `outcome-classes.md` §1.1 both state that classes **5, 6, 7, 9 and
14 cannot be emitted from `Assumed` evidence alone**, decision-changing or not. Class 7's rules add the
specific case: an unfunded mandate asserted from an `Assumed` budget row is provisional, and escalates to
*decision blocked* naming the budget confirmation where it is decision-changing.

**Symmetry** is stated in both the spine and the alternatives register: an `Assumed` claim about a custom
build is held to exactly the same standard as one about the platform.

**D0.** Spine §7.2 carries the affirmative-rationale definition, the worked negative example (*"nothing in
the SU mentions offline"* is **not** a rationale), the gap path (D1 + a priced `Unknown`), the explicit
warning **not** to force every gap to become decision-blocking, and the auditability consequence.

**No second state machine.** The five kernel states carry all epistemics; the seven semantic terms are
option verdicts living in `options.md`. `custo` and `swing` are used with their existing kernel meanings,
and `custo` defaults in `blocking-set.md` come from the kernel's four-value vocabulary.

---

## 6. Constraint-floor implementation

`lenses_config.technology.constraints_to_check` replaced, 5 → the approved 10, each technology-neutral:

`deployment_model_and_residency` · `regulatory_and_control_mandates` · `service_permissibility_and_egress` ·
`entitlement_fit` · `throughput_and_capacity_envelope` · `environment_and_release_topology` ·
`reversibility_mechanism` · `operator_and_support_availability` · `observability_and_evidence_retention` ·
`authorization_enforcement_point`.

The five it replaces were merged or relocated as designed: `premium_licensing` → `entitlement_fit` ·
`dataflow_capacity` → `throughput_and_capacity_envelope` · `ALM_environments` →
`environment_and_release_topology` · `DLP_policy_compatibility` → `service_permissibility_and_egress` ·
`dataverse_storage_quota` → **removed from the floor**, reached by domain pull at D3 when a candidate
proposes that store.

**Declared non-limiting in three places**: `pack.yaml`'s own comment (*"STANDING-ATTENTION FLOOR, never a
ceiling … Coverage is set by the twelve material decision concerns and the emergent-concern obligation …
NOT by this list"*), spine §7.4, and the lens's signal-catalog note. No research id appears in
`pack.yaml`; the entries are neutral tokens.

---

## 7. Technology lens and persona changes

**`lens-technology/SKILL.md` — five edits, net line delta 0.**

1. Execution step 2, clause A: *"a constraint verdict per constraint (pass / risky / blocker)"* → **"a
   verdict per material concern, at proportional depth"**, with *floor, never the ceiling* and *classify
   each disqualifying finding by its exit scope*.
2. Execution step 2, clause B: *"identify the candidate branches"* → **"generate the candidate option
   classes"**.
3. Inputs pull clause: *"the branch of `decision-tree.md` you are evaluating"* → the **stage** you are
   executing plus the register that stage names, with *never preload the registers* added.
4. Hard rule 1: anchoring moved from *"a pack decision-tree branch"* to a **candidate option class and
   the stage that reached it** — the old wording named an object the spine no longer has.
5. Signal catalog: one sentence added stating the declared constraint list is a **floor, never a ceiling**
   and not the coverage object.

**Preserved unchanged**: the Options-only phase gate · the Role and its five questions · signals as cues
with *"Cues, not coverage"* · pull-based domain knowledge · the do-nothing + non-technology floor ·
hard rules 2 and 4–6 · outputs · size (a test asserts the file stays under 90 lines). **The twelve
concerns were not copied into the lens** — it points at the spine, which owns them.

**`solution-architect.md` — two edits, and it shrank.** The Options mandate now says candidates come from
the **option-class trigger map, never from architecture branches**, that process change and do-nothing are
members of the set, and lists the per-option fields; the pull clause names the stage and its register.
Phase E's conciseness is preserved and improved: **3,565 → 3,193 characters**, under the 3,200 budget the
council suite enforces. A test asserts the persona contains **no stage id, no concern id and no option-class
id** — the procedure is referenced, never duplicated.

---

## 8. Chairman / `options.md` output

The Pros / Cons / Constraints-checked / Reversibility / Effort block is gone. The template now supports,
per serious option: option name and **class in plain language** · scope · viability (five values including
**disqualified — provisional, naming the assumption**) · the outcome in its render template · material
strengths · disqualifiers with scope **and evidence grade** · preconditions (condition — owner — funded? —
by when) · material trade-offs · material risks · economic implications · decision-changing uncertainties ·
proof requirement and whether it is funded · concern notes **only where non-obvious**.

Round level: `Summary` · **`Concern coverage`** (one line per concern) · `Comparison` ·
`What the evidence supports` (the five recommendation semantics) · `Comparator status`.

Eight rules were added under the template: `(none)` written explicitly · *(scope, outcome)* pairs never
collapsed · an eliminated candidate still appears with its disqualifier · **no score, no weight, no
ordinal ladder** · **no internal framework vocabulary** · **no unsupported comparative claim**, with
*being able to exclude one option does not prove another is superior* stated in the artefact's own rules ·
the do-nothing + non-technology floor kept and re-stated as *generated with the candidate set, never
appended here* · a *decision blocked* round must name the evidence, its form, the role type and what each
resolution would produce.

**No 12×N matrix.** The template says so explicitly (*"do NOT render a 12×N grid"*) — the twelve-line
coverage summary is the audit surface.

---

## 9. Vocabulary and question-bank changes

**Glossary — Part C added, 4 new terms** (Step 3A's arithmetic: 6 shared − 2 already in Part A):
**Option class** · **Disqualifier** (with the hard ÷ provisional distinction) · **Comparator evidence
absent** · **Graduation trigger**.

**The naming duplication is resolved in favour of `proof requirement`** — the term already in Part A (A5).
Part C states in terms: *"**Validation level** is not a second term for the same thing — the four levels
are the values of the proof requirement."* Choosing the existing Discovery word means **no Part A edit was
needed** and no second vocabulary was created. Spine §12 is titled and worded accordingly.
**Precondition** is likewise reused from A5 with one addition (*it must also be dated*), not restated.

Part C exposes **no internal code** — a test greps it for exit-scope codes, `Ri`/`Cf`, `D0`–`D3`, class
numbers, subtype codes and every id namespace, and asserts none appears. The Discovery glossary did not
grow: Part A and Part B are byte-identical to their Phase G state.

**`question-bank.md` — the closing *Reachable outcomes* block only.** No `Q-TEC`/`P-TEC` namespace was
created and no existing question was added, changed, removed or re-anchored; a test asserts the six
Discovery lens codes are still the complete set. The block gained the **two terminals it was missing** —
*decision blocked* and *an alternative is sufficient and this platform is not excluded* — plus the scope
distinction on exclusion (whole scope · one responsibility · economics) and a closing sentence that
outcomes bind to scopes and must not be collapsed. The three phrases the Phase G neutrality guard tests
for survived verbatim.

---

## 10. Architecture-template re-scope

**Semantic positioning only. No architecture content was designed, renamed or removed.** The three
shapes — `sharepoint-first`, `dataverse-first`, `hybrid` — all survive.

Each template gained two front-matter keys (`scope: architecture-shape` and `available_after_outcome`) and
one line under its heading: *"Architecture shape, not an option class. Chosen after the Options procedure
has established that a platform-containing solution stays viable for this scope."* `hybrid` additionally
states that it is an **in-platform** split across two stores, **not** the cross-boundary hybrid outcome —
a distinction the old tree blurred.

`architecture-templates/README.md` states the positioning once, with a table of which outcomes make a
shape relevant (*strong fit* · *fit with constraints* · the **platform side** of a hybrid scope pair) and
which make **none** relevant (every exclusion, process redesign, do nothing, decision blocked, migration
required, and *alternative sufficient*). It closes with the consequence that matters: a comparison whose
top level is *"one store-first shape versus another versus a split"* shows a sponsor **one option class
presented as the whole choice**.

`applies_to_branch` was **left in place**: it is a self-declaration, resolution is by filename
(`{{chosen_architecture}}`), and renaming it would touch `aisa-render`, `aisa-blueprint`,
`aisa-synthesize` and the kernel synthesis template for no decision-model gain. Detailed architecture
authoring stays with the later Architecture Templates step.

---

## 11. C10 status

**No Discovery signal was added. `extra_signals` remains 36** — a test asserts the exact total, and the
Phase G suite still passes unchanged.

Step 3A's three obligations are implemented:

1. **S7 evaluates C10 for every serious option.** Spine §6 binds S7 to C7 and C10, and states these gates
   make options **unavailable, not worse**; §5 records that C10 is evaluated at S5 **and** S7.
2. **Absent decision-material evidence becomes the appropriate `Unknown`.** Five blocking entries carry it
   — `B-02` accountable ownership (named *and accepted*) · `B-16` governance maturity · `B-17` support and
   operational ownership · `B-26` operational maturity class · `B-28` skills and pro-code capacity — each
   with `swing: decisivo` by construction, so the terminal is *decision blocked*. `operator_and_support_availability`
   is entry 8 of the standing constraint floor, which forces the question in every engagement.
3. **Existing questions and probes are used, none added.** `Q-GOV-06`, `P-GOV-07` and `P-FIN-05` are
   unchanged, and `glossary.md` A2/A6 already carry *operational ownership*, *operational maturity class*
   and *pro-code capacity*.

Composed rows `CD-02` and `CD-09` are the two places C10 becomes decisive in combination; both are
implemented with their non-exclusion semantics intact. **A new C10 cue remains a pilot-calibration
decision** requiring real evidence that this route is insufficient.

---

## 12. Mechanical and regression tests

**New — `.claude/tests/test_pp_options_decision_model.py`, 93 tests, all passing.**

| Group | Tests | What it proves |
|---|---:|---|
| `TestSpine` | 12 | 12 concerns · 10 stages in order · all sixteen sections · phase gate · **no scoring token outside its own prohibition** · **no figure carrying a unit anywhere in the spine** · evidence-grade rule · D0 affirmative rationale · emergent obligation · floor-not-ceiling · no `branches:`/`inputs_used:` · no second state machine · V1–V4 |
| `TestRegisterInventory` | 3 | **Exactly 5** registers · the 5 deferred artifacts absent · no router file |
| `TestAlternativesRegister` | 6 | 11 classes · trigger-not-verdict · mandatory members · platform not default · ≥29 trigger rows · forbidden universals · symmetric unknowns |
| `TestBlockingSet` | 6 | 28 + 3 · engagement-neutral (no owner, date or duration) · every entry carries a `custo` default · `swing: decisivo` · not a questionnaire |
| `TestComposedDisqualifiers` | 6 | Exactly 12 · no 13th · rows 6 and 9 conditional · migration ≠ exclusion · emergent never registered · every row names a reachable outcome |
| `TestOutcomeClasses` | 9 | Closed 14 · closure testable · class 7 discriminator and its four rules · class 13's two non-merging forms · scope pairs · settled exclusions need decision-grade evidence · comparator default · preference on one axis |
| `TestVolatilityRegister` | 6 | 10 + 20 · every entry states a trigger · live conflict with its symmetry · 3 dated tripwires · not a checklist |
| `TestStageLocalLoading` | 6 | Spine binds each register to its stage · volatility on-demand · six stages load nothing · no preload/no router · `pack.yaml` agrees · every declared path resolves |
| `TestPackContract` | 6 | Valid YAML · version bumped · floor = the approved 10 in order · documented non-limiting · Options-gated · **`extra_signals` = 36** · technology lens has no Discovery cues |
| `TestLensAndPersona` | 8 | Verdict per material concern · old clause gone · floor not ceiling · option classes not branches · everything Step 3A said to keep · lens size · persona size · **persona restates no stage, concern or class id** |
| `TestChairmanOutput` | 7 | Every approved per-option field · round-level headings · no giant matrix · old Pros/Cons gone · comparator discipline · no scoring · do-nothing floor |
| `TestInternalVocabularyStaysInternal` | 5 | 4 new terms present · **Part C exposes no internal code** · one shared proof-requirement term · precondition reused · spine forbids rendering internals |
| `TestQuestionBank` | 4 | **No `Q-TEC`/`P-TEC` namespace**, six lens codes only · the two missing terminals added · the three Phase G reachability guards survived · scope pairing stated |
| `TestArchitectureTemplatesRescoped` | 2 | README positioning · all three shapes declare they are not option classes |
| `TestNeutrality` | 4 | Every non-platform outcome reachable · reachability floor enforced · gates symmetric and stated as such · no silent comparator claim |

**Regression — every existing suite re-run, all green.**

| Suite | Result |
|---|---|
| `test_pp_discovery_runtime.py` (Phase G, 22 tests) | **OK** |
| `test_council_wiring.py` (Phase E, 31 tests) | **OK** — after the persona was trimmed back inside the 3,200-char budget it enforces |
| `test_orchestrator_wiring.py` (Phase D, 23 tests) | **OK** |
| `test_state_scaffold.py` (15 tests) | **OK** |
| `library/kernel/tools/tests/test_text_extract.py` (23 tests) | **OK** |

**Leak checks (manual, clean).** No `DC-D-`, `AP-D-`, `PS-`, `LC-`, `AA-`, `DA-`, `AT2-`, `IA-`, `NB-` or
`T-NN` id appears in **any** runtime pack file. `ALT-` appears in exactly one file —
`decision-model/alternatives-register.md` — and nowhere else in the pack.

**One regression was found and fixed rather than waived.** The first persona edit pushed
`solution-architect.md` to 3,565 characters and broke Phase E's `test_personas_shrank`. The mandate was
compressed to a single bullet referencing the procedure instead of describing it — which is what Step 3A
asked for in the first place — and the file now sits at 3,193.

---

## 13. Deviations from Step 3A

Seven, all recorded, none silent. **No decision-model choice was reopened.**

| # | Deviation | Justification |
|---:|---|---|
| 1 | **29 trigger rows, not 30.** Step 3A §7's complexity ledger says *"11 classes, 30 triggers"* | The canonical trigger→class map registers **29** rows. The register implements the canonical table exactly. Implementing a 30th would be invention; the ledger figure is an authoring-side count, not a design decision. **No behaviour changes** |
| 2 | **Registers carry local ids, not canonical ids.** `B-NN`, `BS-NN`, `CD-NN`, `VC-NN`, `VS-NN`, `TW-VN` plus plain-language criterion names | Step 3A §23 test A states *"no `DC-D-NNN` id appears in any runtime file"*, while §17.1 files ids under *"authoring / registers"*. Resolved to the stricter reading: **zero canonical research ids at runtime**, local anchors so the rows stay unambiguous and testable. **`ALT-NNN` is the exception** — §24 artifact 5 specifies `ALT-001…011` as the register's content and the class id *is* the option-class identity. It is declared internal and never rendered |
| 3 | **Shared term = `proof requirement`**, not *validation level* | Step 3A §17.2 required one word and left the choice open. Picking the term already in `glossary.md` A5 means the Discovery vocabulary needs **no edit** and no second vocabulary is created. *Validation level* survives only as the internal name of the V1–V4 scale |
| 4 | **Options vocabulary placed as `glossary.md` Part C**, not a separate `options-glossary.md` | Step 3A §17.2 explicitly left this as *"Step 3B's call"*. One file keeps the two-vocabularies defect impossible by construction and keeps `pack.yaml.glossary` resolving to one path |
| 5 | **`architecture-templates/README.md` created** — one file beyond Step 3A's runtime list | §24 requires the re-scope; stating the positioning once beats repeating it in three templates. It is **not** a decision register — `decision-model/` still holds exactly five files, and a test asserts it |
| 6 | **Five wording fixes in `lens-technology`, not two clauses** | Step 3A named two clauses. Three more sentences named *"a pack decision-tree branch"* — an object the rewritten spine no longer has — so leaving them would have left the lens pointing at nothing. Net line delta is **0** and no behaviour beyond the approved semantics changed |
| 7 | **`applies_to_branch` retained in the architecture templates** | Renaming it would touch `aisa-render`, `aisa-blueprint`, `aisa-synthesize` and a kernel synthesis template for no decision-model gain. The positioning is carried by the new keys and the README instead. Out-of-scope renames are a later Architecture Templates concern |

**Not deviations, recorded to pre-empt the question.** The spine says *"this platform"* rather than the
product name in neutrality-bearing sentences — the file is Options-gated so naming is permitted, but the
symmetry statements read as rules rather than as advocacy when the class is referred to by role. The
volatility register **does** carry the `20×` magnitude of the live conflict and the three tripwire dates:
those are the volatile facts themselves, which is exactly what a volatility register is for. No figure
from either side of the conflict is encoded anywhere.

---

## 14. Exact inputs for Step 3B2

**What Step 3B2 must replay.** The full `T-01`…`T-18` canonical scenario set against the authored
runtime, proving **decision behaviour** — Step 3B1 proved only implementation fidelity.

**Runtime under test (7 files).**

```text
library/packs/pp/decision-tree.md
library/packs/pp/decision-model/alternatives-register.md
library/packs/pp/decision-model/blocking-set.md
library/packs/pp/decision-model/composed-disqualifiers.md
library/packs/pp/decision-model/outcome-classes.md
library/packs/pp/decision-model/volatility-register.md
library/packs/pp/pack.yaml            (decision_model + constraints_to_check)
```

**Design and expectation authority.**

- `step-3a-options-decision-model.md` §20 — the 16 regression scenarios with their expected terminals,
  the 18-row canonical scenario-id audit, and the four G5 carry-forwards.
- `decision-intelligence-matrix.md` §6 — the `T-01`…`T-18` bodies (read, not reopened).
- This report §13 — the seven deviations, each of which must be shown not to change a terminal.

**The four carry-forwards Step 3A promoted to the gate**, because they exercise mechanisms the sixteen
scenarios touch only in passing:

| Scenario | Must reach | Mechanism under test |
|---|---|---|
| `T-10` | outcome 14 → 8 | migration, not remediation — `CD-11` |
| `T-16` | outcome 12 in **every** class including `ALT-004` | the agent-surface row must produce a **block**, not a candidate set |
| `T-17` | outcome **2** | the in-platform redirect must not render as an exclusion |
| `T-18` | outcome **12 → 2** | `CD-06` must never reach 5, 6 or 7 |

**Additional assertions Step 3B2 should carry**, arising from this implementation:

1. **Evidence-grade replay.** `T-04`, `T-08`, `T-09`, `T-10` must reach **decision blocked first**, then
   their exclusion class — never a settled exclusion emitted directly from an assumption.
2. **Scope-pair replay.** `T-06` and `T-12` must render **two** *(scope, outcome)* pairs, uncollapsed.
3. **Class 7 subtype replay.** `T-14` must render **one** of *economically infeasible* /
   *economically unattractive*, chosen from the trigger, never the disjunction, and never implying another
   class is cheaper.
4. **Comparator replay.** `T-13` and `T-14` must carry `COMPARATOR EVIDENCE ABSENT` **inside the outcome
   string**; `T-13` must not assert that a custom build is better.
5. **Reachability-floor replay.** No scenario may terminate with a candidate set containing only forms of
   `ALT-004`.
6. **Class 13 form replay.** `T-01`'s collaboration-surface branch must render form (a) with its
   graduation trigger and stand alone; any other substituted class must render form (b) followed by class 8.
7. **Depth replay.** At least one scenario must exercise a defensible **D0** and one an **evidence gap at
   D1**, to show the two are distinguishable in output.

**Two authoring items carried forward, unchanged and not fixed here.** (a) **C10 Discovery thinness** —
a new cue remains a pilot-calibration decision requiring real evidence; `extra_signals` stays 36.
(b) **Concerns with no pack basis** (document generation at volume is the recorded instance) — the model
evaluates and logs them; accumulation is the input to a future research commission.

**Not in Step 3B2 scope**: `domain-knowledge/*` re-taxonomy (Step 4) · deliverable templates · detailed
architecture-template authoring · `epistemics.half_lives_override` · Discovery `extra_signals` · kernel
files.

---

`STEP 3B1 — OPTIONS RUNTIME IMPLEMENTATION: PASS`
`DECISION SPINE IMPLEMENTED: YES`
`MATERIAL DECISION CONCERNS: 12`
`ORDERED DECISION STAGES: 10`
`ALT OPTION CLASSES: 11`
`BLOCKING ENTRIES: 31 (28 unconditional + 3 scope-blockers)`
`COMPOSED DISQUALIFIERS: 12`
`OUTCOME CLASSES: 14`
`VOLATILITY COMMERCIAL ENTRIES: 10`
`VOLATILITY SERVICE ENTRIES: 20`
`SETTLED EXCLUSION FROM ASSUMED ALONE POSSIBLE: NO`
`D0 FROM MISSING EVIDENCE POSSIBLE: NO`
`DECISION REGISTERS PRELOADED: NO`
`CONSTRAINTS_TO_CHECK IS COVERAGE CEILING: NO`
`INTERNAL CODES EXPOSED AS USER VOCABULARY: NO`
`TECHNOLOGY QUESTIONNAIRE INTRODUCED: NO`
`DISCOVERY EXTRA SIGNALS: 36`
`WEIGHTED SCORING PRESENT: NO`
`PP RUNTIME IMPLEMENTATION MATCHES STEP 3A: YES`
`READY FOR STEP 3B2 — T01-T18 RUNTIME GATE: YES`
