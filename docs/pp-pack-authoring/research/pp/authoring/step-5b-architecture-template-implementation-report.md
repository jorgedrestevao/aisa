# Step 5B — Architecture Template Runtime Implementation Report

<!--
provenance: AUTHORING (implementation report) · Step 5B
authored: 2026-09-04 · basis: step-5a-architecture-template-model.md (FROZEN, incl. §27, §28)
No new research. No web access. No canonical research modified. No Step 6 deliverable template authored.
-->

## 1. Implementation basis

The authoritative design is `step-5a-architecture-template-model.md`, frozen at the start of this step
(its §29 freeze marker, documentation only). Implemented as specified, including the **§27 bounded
correction** (reachability × architectability · headless first-class · repeatable-fragment execution) and
the **§28 component-identity micro-correction** (`component` field · collision-safe identity · N+M
invariant · `experience.mode: none` execution).

Step 5A was **not** redesigned. Step 3 was not reopened. Step 4 was not reopened. No research was
performed and no canonical research file was modified.

## 2. Files created / retired / modified

**Created (6 — 5 runtime units + positioning):**

| File | Role |
|---|---|
| `library/packs/pp/architecture-templates/README.md` | rewritten — positioning authority |
| `.../architecture-core.md` | runtime unit 1 — the fixed entry point |
| `.../fragment-experience-internal.md` | runtime unit 2 |
| `.../fragment-experience-external.md` | runtime unit 3 |
| `.../fragment-experience-inherited.md` | runtime unit 4 |
| `.../fragment-boundary-and-imports.md` | runtime unit 5 — repeatable |

**Retired (3):** `sharepoint-first.md`, `dataverse-first.md`, `hybrid.md` — removed via `git rm -f`. Their
only uncommitted delta was the Step 3B1 re-scope note, which Step 5A verdicts as RETIRE; prior content
remains in git history and in `library/packs/pp-backup/`.

**Modified (10 + 2 test files):**

| File | Change |
|---|---|
| `.claude/skills/aisa-blueprint/SKILL.md` | rewritten to the §20 contract |
| `.claude/skills/aisa-decide/SKILL.md` | bounded serialization cleanup only |
| `.claude/skills/aisa-render/SKILL.md` | fixed entry point · fragment iteration · four gap classes |
| `.claude/skills/aisa-synthesize/SKILL.md` | fixed architecture source · no branch language |
| `.claude/skills/aisa-options/SKILL.md` | rendering vocabulary only |
| `.claude/skills/aisa-simulate/SKILL.md` | rendering vocabulary only |
| `library/kernel/blueprint-contract.md` | three generic edits (§21) |
| `library/kernel/render-contract.md` | two generic edits (§21) |
| `library/kernel/synthesis-templates/architecture-story.template.md` | fixed source · reworded prompt |
| `library/packs/pp/pack.yaml` | version 1.6.0 → 1.7.0 + manifest comment |
| `.claude/tests/test_pp_architecture_templates.py` | **new** — 115 tests |
| `.claude/tests/test_pp_options_decision_model.py` | `TestArchitectureTemplatesRescoped` rewritten |

## 3. Architecture-template taxonomy

```text
library/packs/pp/architecture-templates/
  README.md                          positioning — NOT a runtime template unit
  architecture-core.md               A1…A3 + A5…A12 + 8 conditional sections
  fragment-experience-internal.md    owned-internal
  fragment-experience-external.md    owned-external
  fragment-experience-inherited.md   inherited
  fragment-boundary-and-imports.md   one instance per qualifying component
```

**Runtime template units: 5.** Pattern-specific templates: **0**. Product-named templates: **0**.
Headless-specific template: **none** (and none needed). One fixed entry point; one include driven by one
recorded field; no router, no loop primitive, no inheritance framework.

## 4. Authorization implementation

```text
architecture authorization = outcome reachability × active-pack architectability
```

Outcome reachability alone is never sufficient. The full 14-class reachability table has **one home** —
`README.md` §3 — and no template file lists an outcome class (asserted). Three authorization values only:
`authorized` · `authorized-bounded` · `not-authorized`, each requiring **both** factors.

Authorization is **read, never derived**: the layer cannot compute one from evidence, cannot upgrade
`authorized-bounded` to `authorized`, and cannot emit *decision blocked* — only repeat one Options
emitted. Outcome classes were not modified.

## 5. Architectability implementation

Implemented as §27.2's single question with two lists (README §4). Architectable: a PP application in any
experience mode · a PP automation or integration composition · the **PP side** of a composed solution · a
capability the pack explicitly covers. Not architectable: custom-only · packaged / SaaS ·
cloud-native-only · incumbent internals · another platform's internals · a candidate set with no selected
architecture. The far side of a scope pair is never architectable here.

Where no scope is both reachable and architectable, **no PP architecture is produced**, and the two
failure reasons are reported **separately** — never merged, and neither relabelled `Decision Blocked`.
`architectability_basis` records the reason in one sentence.

## 6. Architecture contract

The Step 5A §6 `architecture:` block replaces `branch`, written into
`_blueprint/ux-blueprint_v<NN>.yaml`: `scope` · `authorization` · `authorization_basis` ·
`architectability_basis` · `experience{mode, primary_surface}` · `record_authority[]` ·
`compositions[]` (with `component`, `pattern`, `forced_by`, `boundary`, `owner`, `enclosing`) ·
`relocated_responsibilities[]` · `proof_obligations[]` · `open_architecture_choices[]`.

No additional architecture state was introduced. `imports` is deliberately **not** a field — imports are
derived per component and carried structurally, so they cannot be declared satisfied by fiat.

## 7. Ownership of authorization

`aisa-decide` **serializes already-decided facts only**: uncollapsed `(scope, outcome)` pairs · selected
solution / composition in plain language · conditions · proof obligations · accepted risks ·
preconditions · tripwires. A new section enumerates what it must **never** emit
(`architecture.authorization`, `architectability_basis`, experience mode, composition selection, record
authority, template selection).

`/blueprint` initializes `authorization` + `architectability_basis` at entry, from the frozen outcome and
the frozen selected solution against the active pack's architecture scope — a **mechanical
architecture-entry gate, not a new decision**.

## 8. Headless implementation

`experience.mode: none` is a **finalized architectural condition**, not an Unknown:
`primary_surface: null` · **zero** experience-fragment includes · **no A4** · no attempt to resolve
`fragment-experience-none.md` (which intentionally does not exist) · no placeholder · no missing-template
warning · no render gap · no *surface unresolved*. It is logged as a `not applicable` skip with a reason.

A headless architecture remains complete: A1–A3, A5–A12 plus zero or more boundary fragments. A7 stays
**common** and can never be owned by an experience fragment. "Do not fabricate a user surface" is stated
in both the README and the skill.

## 9. Experience fragments

Three fragments, each declaring `activates_on`. `owned-internal`: A4 body, screen handoff,
delegation-safe access paths, distribution, offline/device, surface forfeits, human-user A7
specialization, owned lifecycle. `owned-external`: external-audience prerequisite, external identity
provider as prerequisite with cost and operating burden, deny-by-default authorization form, public /
anonymous exposure, cache and freshness semantics, accessibility basis, localization, build-model
forfeits. `inherited`: host, inherited access and lifecycle, verified ceiling, **mandatory graduation
trigger**, forfeits, and the explicit statement that no independent topology exists.

Each fragment states that it does **not** own store choice or security truth, and that it does not decide
whether a surface exists, whether an external audience is required, or when graduation occurs. The
inherited fragment must not claim the platform is excluded.

## 10. Record-authority handling

`0..N`. An empty set is legitimate **only** with the affirmative rationale (*"No persisted record
authority introduced; the workflow acts on external authorities and retains only operational execution
state."*). **Missing evidence is never an empty set** — undetermined authority becomes an
`open_architecture_choices` entry, `structural: true` where it decides the store.

## 11. Boundary/import fragment

One instance per qualifying component. Qualifying = `boundary: outside-platform`, any composition beyond
`direct`, or any `relocated_responsibilities[]` entry. Every instance carries **all six channels**
(Governance · ALM · Cost · Monitoring · Recovery · Operator), each populated or `not engaged — <reason>`;
six independent escapes are present, and a missing channel is stated as a defect in all five binding
places. Conditionals: `INCUMBENT FIT UNEVALUATED`, status resource, reconciliation owner, enclosing
boundary. `owner: UNKNOWN` is a structural open choice, not a risk row.

## 12. Component identity

`component` is required on every composition: human-readable, local to the scope, unique within it, not
globally stable, not canonical vocabulary, not a registry id. No UUIDs, no identifier subsystem.
`responsibility` is the identity for a relocation — no second field was created. Duplicate identity in one
scope is a **contract defect**: fail, never merge, auto-suffix, overwrite or collapse imports.

## 13. Fragment iteration and invariant

```text
composition fragment key             → <scope>::component::<component>
relocated responsibility fragment key → <scope>::responsibility::<responsibility>

N unique qualifying composition components + M unique relocated responsibilities
  ⇒ exactly N + M boundary/import fragment instances
```

No loop syntax or template-engine functionality was added. The skill performs the iteration; the **core
carries the repeat instruction exactly once** (asserted by count). The scope prefix is structure only and
is never rendered as engagement vocabulary.

## 14. Scope-pair implementation

`(scope, outcome)` pairs stay uncollapsed in A1, `aisa-decide` serialization and the conditional *scope
ownership* table. A relocated responsibility receives responsibility · owner · outcome basis · boundary ·
gates and imports — and **never a PP design for the far side** (asserted in all four binding files).
`INCUMBENT FIT UNEVALUATED` is preserved verbatim and comparator fit is never inferred. The fragment
carries an explicit *"what this pack does not know about the other side"* section.

## 15. Epistemic and render-gap handling

The kernel's five states survive unchanged: `Confirmed` renders with `verificado_em` / `validade` (expired
⇒ re-verification obligation); `Assumed` never promoted; `Unknown` never filled (becomes an open choice);
`Conflicted` renders the conflict and carries neither figure; `Risky` carries its accepted-risk id.

Four gap classes implemented in both `render-contract.md` and `aisa-render`: **not applicable** (skip with
a reason, never a gap) · **optional** · **architecture work item** (not decision-blocking) ·
**decision-blocking**. A structural open architecture choice blocks **approval**, not **production**, via
the existing open-question and SU mechanisms — no new state, outcome class, phase or approval state
machine.

## 16. Domain Knowledge pull behaviour

Step 4C discipline preserved verbatim in `aisa-blueprint`: one relevant unit per architecture
responsibility, decision-grade + architecture-grade sections, a second pull only where the first exposes a
material dependency. Median 1, **maximum 2**. Explicitly forbidden and asserted: preloading the units, an
architecture knowledge bundle, surveying all ten patterns, a routing table keyed by section. For an
engaged composition the pull is `architecture/patterns.md` §3 + **the one** engaged pattern, plus a
mechanism file only if necessary. No knowledge unit was modified; no knowledge was duplicated into a
template.

## 17. CRAFT boundary

CRAFT may shape screen consolidation, screen patterns and density, the **form** of the security matrix,
relational layering and naming, delivery conventions, and masking where an obligation exists. CRAFT may
**not** select architecture, set authorization, set record authority, establish platform capability,
establish a technical limit, or choose a proof level. `craft/estimation-model.md` is excluded from the
architecture blueprint. RESEARCH wins on conflict, and the CRAFT statement is a defect to report.

## 18. Diagram and boundary-table implementation

No diagram tooling added. The **required** boundary table is implemented with its six columns
(Component · Role · Platform governance · Trust boundary crossed · Owner · Data classification); every
component in `compositions[]`, `record_authority[]` and `relocated_responsibilities[]` appears **exactly
once**. Optional context picture and sequence sketch are fenced blocks, must degrade to readable text, and
**no diagram-only fact is authoritative**.

## 19. No platform numbers

No architecture template owns a service limit, price, quota, retention window, threshold or SKU value —
asserted by a regex scan over all five units. Volatile values resolve to an engagement-verified SU row
(`value · verificado_em · validade · re-verify trigger`) or render the verification obligation.

## 20. Consumer updates

`aisa-blueprint` (entry gate · authorization initialization · architecture-block authoring · headless
handling · component identity · fragment iteration · structural-open-choice handling · selective pulls ·
CRAFT boundary). `aisa-decide` (serialization only). `aisa-render` (fixed entry point · zero/one
experience fragment · zero/many boundary instances · identity uniqueness · N+M invariant · four gap
classes). `aisa-synthesize` + `architecture-story.template.md` (fixed source; states authorized scope,
outcome basis, architecture intent, composition, boundaries, imported obligations). `aisa-options` and
`aisa-simulate` (rendered vocabulary only). No router was added anywhere.

## 21. Kernel contract updates

`blueprint-contract.md`: `branch` → a generic `architecture` block (with the explicit note that
experience-mode, surface and pattern vocabulary belongs to the pack, never the kernel); an entry-gate
section (authorization for at least one scope, initialized at entry, never re-derived; a blueprint need
not have a human-facing surface); and a new approval rule for structural open choices.

`render-contract.md`: architecture-containing output renders only where an authorization exists for at
least one scope (replacing `applies_to: [technology]` as the architecture discriminator); plus the four
render-gap classes. **No PP taxonomy entered the kernel** (asserted), no router, no loop primitive, no new
state.

## 22. pack.yaml changes

`pack.yaml` **never manifested architecture-template paths**, so no path required updating — manifest
maintenance only. Version bumped minimally `1.6.0 → 1.7.0` per the repository's minor-bump convention for
pack content changes, with a comment recording why. No architecture routing, outcome→template map, product
map, concern map or load order was added. The `applies_to: [technology]` values are **unchanged**: the
architecture discriminator lives in `render-contract.md`, not in a pack vocabulary value. Step 3 semantic
config was not modified.

## 23. Legacy compatibility

Already-rendered artefacts are preserved and not regenerated; two engagements
(`projects/cae-automation`, `projects/dpt-galp-jp`) carry a recorded legacy branch value and frozen
renders. README §11 records the read interpretation for `sharepoint-first`, `dataverse-first` and
`hybrid`, and states that a **new** render must construct a proper `architecture:` block. **Read
compatibility only** — no shim, no router, no permanent dual model, and the mapping supplies no
authorization.

## 24. Step 6 carry-forwards

Deliberately **not** migrated (Step 6 owns them). All three still reference the old contract
(`chosen_architecture` and/or `Branch (if technology)`):

- `library/packs/pp/deliverable-templates/solution-blueprint.template.md`
- `library/packs/pp/deliverable-templates/implementation-spec.template.md`
- `library/packs/pp/deliverable-templates/claude-design-brief.template.md`

Recorded as **STEP 6 CARRY-FORWARD**, not a Step 5B failure, and pinned by a test that fails if the set
changes without updating this report. No partial deliverable-template migration was performed.
**Step 5B therefore does not claim complete end-to-end deliverable rendering**; the Architecture Layer was
tested directly instead.

Step 5A's two carried open questions remain open for Step 6: whether `claude-design-brief` includes the
core or receives a narrower entry, and whether *replacement of an existing artefact* is better owned by
`implementation-spec`.

## 25. F-1…F-19 mechanical coverage

**19/19 represented and mechanically enforceable.** `TestFixtureRepresentability` covers F-1…F-19;
`TestF19CollisionMechanics` executes the identity rules as data.

| Fixture | Proven mechanically |
|---|---|
| F-1 | inherited activation · graduation trigger · no independent topology |
| F-2, F-3 | owned-internal over either store role · A5/A9 present |
| F-4 | relational-via-connector expressible · delegation-safe paths · A7/A3 |
| F-5 | owned-external · external identity · cache/freshness · accessibility |
| F-6 | `data-replication` · `access_mode: replicated` · reconciliation owner mandatory |
| F-7 | `api-mediated` · second release route · contract compatibility |
| F-8 | `owner: UNKNOWN` ⇒ structural, not a risk row · tripwire cross-reference |
| F-9 | `data-virtualization` · `virtualized` · A9 |
| F-10, F-11 | relocations · both owners · `INCUMBENT FIT UNEVALUATED` · scope-ownership section |
| F-12 | candidate architectures · choose neither · no scoring |
| F-13 | render nothing architectural · class 12 present in the one reachability table |
| F-14 | classes 5 and 8 · skip is not a gap |
| F-15 | zero experience fragments · A6 · no A4 · no fabricated surface |
| F-16 | queue/pro-code compositions · zero/many boundary fragments · service identity |
| F-17 | class 1/2 over non-PP ⇒ no PP architecture authorization |
| F-18 | 13(a) outside authority ⇒ sufficiency, non-exclusion and graduation trigger preserved |
| F-19 | 2 components, same pattern + owner ⇒ **2** fragments; duplicate name ⇒ **fail** |

Step 5B proves the runtime can **represent and enforce** these. It is **not** the semantic gate — Step 5C
replays them behaviourally.

## 26. Tests and regressions

| Suite | Result |
|---|---|
| `test_pp_architecture_templates.py` (**new**) | **115 passed** |
| `test_pp_options_decision_model.py` | **95 passed** (was 94; `TestArchitectureTemplatesRescoped` rewritten) |
| `test_pp_domain_knowledge.py` | **64 passed** — Step 4 regression PASS |
| `test_pp_discovery_runtime.py` | 22 passed |
| `test_council_wiring.py` | 31 passed |
| `test_orchestrator_wiring.py` | 23 passed |
| `test_state_scaffold.py` | 15 passed |
| **Total** | **365 passed, 0 failed** |

**Step 3 regression: PASS.** The only two failures encountered were the obsolete assertions Step 5A §25
item 15 named in advance (`TestArchitectureTemplatesRescoped` asserting exactly three shapes and the old
README wording). They were rewritten to assert the Options-side guarantee that survives — no architecture
template claims to be an option class, and no architecture vocabulary leaks upward into `aisa-options` /
`aisa-simulate`. **No Step 3 register was modified to make a test pass**, and the T-01…T-18 semantic gate
was not re-run: rendering-vocabulary removal alone does not warrant reopening 3B2.

**Step 4 regression: PASS.** No knowledge unit was modified; pull behaviour is unchanged; the architecture
layer does not preload knowledge; CRAFT remains non-authoritative (all asserted).

## 27. Deviations from Step 5A

**None semantic.** Two additive clarifications were made inside the runtime files during test repair, both
restating a Step 5A rule rather than changing one:

1. `architecture-core.md` now names the six channels inline and states *"a missing channel is a defect"*
   explicitly in its render contract (Step 5A §10 rule 1).
2. `fragment-boundary-and-imports.md` uses the canonical phrasing *"never a PP design for the far side"*
   (Step 5A §12), replacing an equivalent paraphrase.

One documented exemption: the three retired branch names survive **only** in README §11's legacy
read-compatibility paragraph, as §36 of the commission requires. The obsolete-vocabulary test is scoped to
the branch *model* tokens and treats that paragraph as the single documented exemption.

## 28. Failures and classification

| Class | Count | Disposition |
|---|---:|---|
| **A — implementation/wiring defect** | 15 | All repaired. 13 were assertion brittleness across markdown line wraps (fixed with the repo's existing `flat()` normalizer idiom); 2 were genuine missing sentences in runtime files, added per §27 above |
| **B — frozen Step 5A ambiguity** | 0 | None found. Nothing required reporting before redesign, and no redesign occurred |
| **C — Step 3 regression** | 0 | The 2 test failures were the sanctioned rewrite named by Step 5A §25 item 15, not a behaviour change |
| **D — Step 4 regression** | 0 | 64/64 pass; no unit touched |
| **E — Step 6 carry-forward** | 3 | The three deliverable templates. Correctly bounded, pinned by a test, and not a 5B blocker — the Architecture Layer itself is functional |
| **F — legacy compatibility** | 0 | Read compatibility only; no artefact regenerated |

Per §44, the complete scope was implemented before any individual failure was repaired; failures were
collected, classified, then fixed at the smallest implementation defect. No Step 5A semantics were altered
in response to a fixture.

## 29. Recommendation for Step 5C

**Proceed to Step 5C — the semantic architecture gate.** Step 5B proves the model was faithfully
implemented and that the runtime can represent and mechanically enforce F-1…F-19. It does **not** prove
that a generated architecture is semantically defensible under realistic engagement pressure. **Step 5 must
not be frozen on structural tests alone.**

Step 5C should prioritise: (i) behavioural replay of all 19 fixtures against real engagement material,
with Domain Knowledge pull counting per fixture (median ≤ 1 per section, max 2) exactly as 4C did;
(ii) whether an authored architecture actually resists the temptation to design the far side of a scope
pair; (iii) whether the six import channels are populated with decision-bearing content rather than
`not engaged` boilerplate; (iv) whether a headless architecture reads as complete to a sponsor;
(v) whether the two authorization-failure reasons stay legible and distinct in real output.

Step 6 should then migrate the three carry-forward deliverable templates onto the fixed
`architecture-core.md` entry point and the `architecture:` block.

---

## 30. Step 5B final marker

```text
STEP 5B — ARCHITECTURE TEMPLATE IMPLEMENTATION: PASS
RUNTIME TEMPLATE UNITS: 5/5
OLD BRANCH TEMPLATES RETIRED: 3/3
OLD THREE-BRANCH MODEL PRESENT IN STEP-5 RUNTIME: NO
PRODUCT-DRIVEN TEMPLATE TAXONOMY: NO
PATTERN-SPECIFIC TEMPLATES: 0
OUTCOME ALONE AUTHORIZES PP ARCHITECTURE: NO
PACK ARCHITECTABILITY GATE IMPLEMENTED: YES
AISA-DECIDE OWNS ARCHITECTURE AUTHORIZATION: NO
HEADLESS PP ARCHITECTURE IMPLEMENTED: YES
EXPERIENCE=NONE OPENS EXPERIENCE FRAGMENT: NO
EMPTY RECORD AUTHORITY WITH RATIONALE SUPPORTED: YES
COMPOSITION COMPONENT IDENTITY IMPLEMENTED: YES
DUPLICATE COMPONENT IDENTITY FAILS: YES
F-19 SAME-PATTERN COLLISION: PASS
N+M FRAGMENT COUNT INVARIANT: PASS
SIX IMPORT CHANNELS ENFORCED: YES
SCOPE PAIRS PRESERVED: YES
FAR-SIDE PP DESIGN GENERATED: NO
PLATFORM NUMBERS HARDCODED IN TEMPLATES: NO
DOMAIN KNOWLEDGE DUPLICATED INTO TEMPLATES: NO
CRAFT USED AS TECHNICAL AUTHORITY: NO
F-1...F-19 MECHANICAL COVERAGE: 19/19
STEP 3 DECISION SEMANTICS CHANGED: NO
STEP 3 REGRESSION: PASS
STEP 4 REGRESSION: PASS
STEP 6 CARRY-FORWARDS RECORDED: YES
NEW RESEARCH PERFORMED: NO
READY FOR STEP 5B REVIEW: YES
```

`STEP 5B: CLOSED`
