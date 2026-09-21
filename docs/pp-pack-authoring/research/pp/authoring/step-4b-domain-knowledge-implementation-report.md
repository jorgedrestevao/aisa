# Step 4B — Domain Knowledge Runtime Implementation (report)

<!--
provenance: AUTHORING REPORT
date: 2026-09-04
scope: PP PACK AUTHORING — STEP 4B. Implementation of the approved Step 4A design.
design authority (read, not reopened, not modified): step-4a-domain-knowledge-model.md (final)
read (not reopened, not modified): step-3a-options-decision-model.md · step-3b1/3b2 reports (FROZEN) ·
    pp-pack-authoring-map.md · library/packs/pp/decision-tree.md + the five decision-model registers ·
    canonical Areas 1–12 + Block D (canonical-manifest.md §3, §5, §6, §11–§13) ·
    the 13 pre-existing library/packs/pp/domain-knowledge/* files (migration source only)
no research reopened · no web access · no canonical evidence file modified · Step 3 runtime unmodified
path note: `research/pp/authoring/` resolves to `docs/pp-pack-authoring/research/pp/authoring/`
-->

---

## 1. Implementation summary

The domain-knowledge layer was rebuilt from a flat, unprovenanced namespace of 13 files into the approved
pull-based taxonomy of **26 files — 15 RESEARCH units, 10 CRAFT units and a README use contract**.

| | Before | After |
|---|---|---|
| Files | 13 | 26 |
| Structure | flat | 12 subject directories + `craft/` |
| Lines | ~4,000 | ~10,850 |
| Provenance headers | 0 | 26 |
| Volatility stamps | 0 | 47 across 15 units |
| Class labelling (RESEARCH / CRAFT) | none | explicit on every file |
| Prices | 2 files, 9 figures | **0** |
| Obsolete architecture-branch vocabulary | 4 files | **0** |
| Restated deleted disqualification gates | 1 file | **0** |
| Delegation authority | 3 divergent copies | **1** |
| Subjects the layer could not answer at all | 19 | 0 (all authored; gaps recorded, not filled) |

**What was actually gained.** The layer previously could not answer a question about the four automation
shapes, the five metering systems, idempotency and retry duplication, the five security enforcement
planes, trust boundary, egress or key custody, the eight governance levers, managed environments and
their licence chain, the four-rung ALM ladder, no-rollback, environment topology, the five economic
mechanisms, the four operational maturity classes, monitoring and telemetry limits, backup ≠ recovery,
integration mechanism envelopes, the network boundary, identity propagation, or the ten architecture
patterns. **Every one of those is now a D3 pull target with decision-grade content.**

**What was removed rather than migrated.** All prices; the `azure-sql-first` architecture branch the
decision tree never had (a recorded live engagement defect); the restated R0 disqualification gates and
their invented numbers; the three-branch vocabulary in four files; comparative selection verdicts
(*"therefore inappropriate"*); two duplicate delegation tables; and every craft body that was presenting
itself as platform reference.

**Method note.** The 12 remaining RESEARCH units and the 10 CRAFT migrations were authored by parallel
subagents against a single written authoring contract (its rules are the prohibitions listed in §1 and
asserted in §19.1), each returning a
provenance table, a research-gap table, a number adjudication and a compliance confirmation. Those
returns are the raw material for §9, §10, §11 and §12 of this report. Every unit was then re-verified
mechanically by the orchestrator against the landed files (§17).

---

## 2. Old → new migration map

| # | Old file (lines) | Step 4A verdict | Landed as | Notes |
|---:|---|---|---|---|
| 1 | `powerfx-patterns.md` (566) | SPLIT | `craft/powerfx.md` (531) + platform boundary → `data/query-and-delegation.md` | §1–§2 (both delegation matrices, the client-record ceiling, the workaround catalogue) **deleted** from craft; craft now cites the owner and states *"delegation is not owned here"* |
| 2 | `flows-patterns.md` (514) | SPLIT + REWRITE | `craft/flow-craft.md` (554) + **new** `automation/automation-mechanisms.md` (405) | The decision-bearing content (shapes, meters, idempotency, retry, ordering, waits) did not exist and was authored from Area 4; connector limit column, child-flow limits, card expiry and Power BI comparatives removed from craft |
| 3 | `azure-sql-reference.md` (554) | SPLIT | `craft/sql-delivery-conventions.md` (601) + `data/azure-sql.md` (481) | ~85 % was team convention. The declared `azure-sql-first` branch and the performance-limits table **deleted** |
| 4 | `dataverse-reference.md` (437) | REWRITE | `data/dataverse.md` (541) | Price row **deleted**; verdict matrix re-expressed as capability boundaries; schema-rigor matrix → craft |
| 5 | `sharepoint-reference.md` (379) | REWRITE | `data/sharepoint.md` (340) | **Deleted R0 gate restatement** (`>30,000` rows, `formula_count > 100`) and *"makes SharePoint inappropriate"*; the customer-key correction carried |
| 6 | `security-patterns.md` (392) | SPLIT + REWRITE | `craft/security-craft.md` (425) + **new** `security/security-controls.md` (522) | Re-organised from artifact type to the five enforcement planes; currency example removed |
| 7 | `screen-patterns.md` (269) | KEEP | `craft/screen-patterns.md` (282) | Substance unchanged; two surface-fit verdicts removed |
| 8 | `estimation-model.md` (260) | KEEP + partial DEPRECATE | `craft/estimation-model.md` (288) | Licence-cost section **deleted, not migrated**; comparative-economics bar stated prominently |
| 9 | `anonymization.md` (205) | KEEP | `craft/anonymization.md` (226) | Substance unchanged |
| 10 | `excel-patterns.md` (203) | KEEP | `craft/excel-translation.md` (220) | Delegation verdict cells converted to check-prompts |
| 11 | `delegation-matrix.md` (77) | MERGE | `data/query-and-delegation.md` (350) | Three copies collapsed to one authority; divergences adjudicated (§4.1) |
| 12 | `screen-consolidation-rules.md` (76) | KEEP (filename) | `craft/screen-consolidation-rules.md` (91) | **Rules byte-identical.** Only the dead branch sentence and one cross-reference changed |
| 13 | `delivery-conventions.md` (62) | UPDATE + RETAXONOMIZE | `craft/delivery-conventions.md` (97) | Portuguese preserved; `TODO(team)` markers preserved; platform assertions now cite their RESEARCH owners |

**New units with no migration source (11):** `application/application-surfaces.md`,
`data/store-boundaries.md`, `automation/automation-mechanisms.md`,
`integration/integration-mechanisms.md`, `governance/governance-and-environments.md`,
`alm/release-and-lifecycle.md`, `performance/performance-and-scale.md`,
`economics/licensing-and-cost-drivers.md`, `operations/operability-and-support.md`,
`architecture/patterns.md`, `security/security-controls.md` — authored from the canonical baseline.

**Retired outright: 0 files.** Thirteen retired *paths*; every file's salvageable content survives.

---

## 3. Number-adjudication summary

Every numeral in the 13 source files was classified. Full per-file tables are in the subagent returns;
this is the consolidated disposition.

| Class | Count (approx.) | Disposition |
|---|---:|---|
| `stable-retain` | ~20 | Structural counts and non-volatile facts (four shapes, five planes, five meters, four rungs, three capacity meters, one-directional borrowing, national data formats). Carried unstamped |
| `volatile-retain-stamped` | **47** | Carried as a documented reading naming an existing register row (§8) |
| `register-owned` (row exists, figure deferred) | ~55 | Boundary shape carried, figure left to be read at the decision date |
| `register-owned` (**no owning row**) | ~60 | Boundary shape carried, figure dropped. **This is the largest structural finding of Step 4B — §8.2** |
| `implementation-trivia` | ~120 | Retained in `craft/` where it is build guidance (hex palettes, pixel densities, ms timings, T-SQL types, checksum weights); dropped from RESEARCH units |
| `unsupported-remove` | **14** | See below |
| **Conflicted — carried on neither side** | 5 | §11 |

### 3.1 The 14 `unsupported-remove` figures

| Figure | Was in | Why removed |
|---|---|---|
| `> 30,000` rows as a disqualifier | `sharepoint-reference.md` l.42 | A deleted R0 gate with an invented number |
| `formula_count > 100` | `sharepoint-reference.md` l.42 | Same |
| The `2,000 / 5,000 / 20,000 / 100,000+ → migrate` ladder | `sharepoint-reference.md` | Invented threshold ladder **and** a selection verdict |
| `"peak load + 30 % buffer"` | `azure-sql-reference.md` | Invented sizing rule |
| Fragmentation `> 30 %` | `azure-sql-reference.md` | Invented threshold |
| `screen count > 15 → evaluate model-driven` | `screen-patterns.md` | Surface-fit verdict |
| Six per-user licence prices + two tier prices | `estimation-model.md` | Prices |
| `€/day × days` cost column | `estimation-model.md` | Price |
| Per-user and per-app price row | `dataverse-reference.md` | Prices |
| `"quotes under €10k"`, `€` in a format mask | `security-patterns.md` | Currency |
| Canvas vendor claim (`50+` screens, `100` tables) as a scale ceiling | Area 2 (source) | Source policy forbids treating a vendor scale adjective as evidence |
| Third-tier `30–40` screen / `500` control heuristics | Area 2 (source) | Gate condition 3 forbids encoding them |
| Practitioner scale figures (concurrent users, row counts) | Area 9 (source) | Explicitly unverified in the baseline |
| Security-score hygiene triggers (`>10` env admins, `>20` sys admins) | Area 6 (source) | Preview-tool hygiene, would read as invented thresholds |

**The adjudication is authoring-side only. None of it is reproduced in runtime.**

---

## 4. Files created / retired / moved

**Created (26).** `README.md` · `application/application-surfaces.md` ·
`data/{store-boundaries,dataverse,sharepoint,azure-sql,query-and-delegation}.md` ·
`automation/automation-mechanisms.md` · `integration/integration-mechanisms.md` ·
`security/security-controls.md` · `governance/governance-and-environments.md` ·
`alm/release-and-lifecycle.md` · `performance/performance-and-scale.md` ·
`economics/licensing-and-cost-drivers.md` · `operations/operability-and-support.md` ·
`architecture/patterns.md` ·
`craft/{powerfx,screen-patterns,screen-consolidation-rules,excel-translation,flow-craft,security-craft,sql-delivery-conventions,anonymization,estimation-model,delivery-conventions}.md`

**Retired (13 paths).** The flat files in §2. Verified absent by `test_no_retired_flat_file_survives`.

**Landing mechanics.** `library/**` is deny-listed for `Write`/`Edit` and guarded by `pre-write-guard.py`.
All files were authored in the session scratchpad and copied in by an idempotent script that **refuses to
run unless all 26 expected files are present** and verifies the landed set equals the expected set
exactly. Nothing is committed.

### 4.1 The delegation-divergence adjudication

Collapsing three copies into one authority required resolving disagreements the copies already carried.
Resolved against the canonical baseline only:

| Subject | The three copies said | Resolution |
|---|---|---|
| Client retrieval ceiling | *"limited to 500 records"* / *"default 500, max 2000"* / *"500-item client-side limit"* + a separate *"max 2000 per call even with delegation"* | Default **and** maximum, a **client** non-delegable retrieval ceiling, **per query**. The third copy was wrong twice. Carried stamped under `VS-02` |
| `CountRows` on the list store | all three said delegable | **All three wrong** — the vendor states the function is not supported and not delegated |
| `CountIf` on the list store | *"partial, indexed column"* ×2 / *"no"* | Not delegated; the *indexed-column* qualifier is unsupported |
| Lookup/sort delegation gated on *"if the FK column is indexed"* | asserted ×2 | Contradicted — indexes on the governed store are platform-managed; maker-controlled-index framing dropped for that store |
| Growth ladder + *"no longer appropriate… migrate"* | one copy | Invented thresholds **and** a selection verdict — not carried in any form |
| Maintenance instruction (*"bump `pack_version` when the matrix changes"*) | one copy | Superseded by the volatility register |

---

## 5. The 15 RESEARCH units

| Unit | Lines | Answers | Decision-grade core |
|---|---:|---|---|
| `application/application-surfaces.md` | 380 | Which surface carries which experience, and what it forfeits | Rung-0 test · 12-surface boundary inventory · identity class as the first hard fork · five-depth offline ladder ending in the offline × field-confidentiality mutual exclusion · device · accessibility · localization · distribution · deep links · one-way graduations |
| `data/store-boundaries.md` | 279 | Which store can support this requirement; does reporting force a second store | 12 dimensions · cross-store capability map · *view or data?* · what a copy obliges (reconciliation owner, drift detection that is not row counts, resync, rebuilt authorization, capacity, erasure, schema owner) · replication vs virtualization vs keep-in-place |
| `data/dataverse.md` | 541 | Transactional and authorization semantics; what cannot be undone | Relationship semantics · irreversibility table · alternate keys as the uniqueness *and* upsert *and* idempotency mechanism · extension-mechanism boundary as capability, not verdict · authorization grain · audit and retention · three capacity meters · standard vs elastic consistency · virtual-table forfeits |
| `data/sharepoint.md` | 340 | What the store does not enforce; its ceiling on this access path | Documented ceilings · the absences (no column security, no transaction, last-writer-wins) · indexing and view mechanics · calculated-column boundary · binary and label behaviour · the shapes for which it *is* the answer · nine graduation triggers stated as capability conditions |
| `data/azure-sql.md` | 481 | Connector envelope and identity model when the store is external | Connector envelope incl. shared-connection budget · why implicit connections collapse per-user authorization · row-level-security prerequisites · schema-conformance gate · log rate as the real ceiling · retention and cold-storage reality · bulk-load path · customer-key with its tier-0 dependency · private-network path · **what leaves platform governance** |
| `data/query-and-delegation.md` | 350 | Is this path delegation-safe — and is delegation-safe fast enough | **delegation-safe ≠ fast** · truncation semantics and the all-or-nothing rule · the two traps that produce no warning · per-connector-class behaviour · client cache and cached-count · list-view threshold · throttled query shapes |
| `automation/automation-mechanisms.md` | 405 | Which mechanism carries this shape, what fails first | Four shapes + ordered classification test · five meters · mechanism envelopes · long-running waits · **retry duplicates non-idempotent effects** · ordering, dedup, no-rollback, atomicity · approvals · RPA queue · nine corrected myths |
| `integration/integration-mechanisms.md` | 471 | Which mechanism supports this guarantee, payload and boundary | 12 dimensions · ordered topology test (ownership first) · 16-mechanism envelope table · five justifications for mediation and when it is unnecessary · guarantees are the transport's · synchronization risk register · atomicity and identity propagation · nine ownership conditions · the conflicted ceiling · network mutual exclusions |
| `security/security-controls.md` | 522 | Is the control available, on which plane, over what population | **Five enforcement planes** · lowest-plane rule with its worked negative case · trust boundary and egress · identity propagation and the shared-identity collapse · key/secret custody where decision-material · policy semantics · 13 partial-by-design controls · 10 irreversible decisions · control-obliged population · residual-risk obligation |
| `governance/governance-and-environments.md` | 551 | What preconditions does this control level require, and what does it cost the estate | Eight levers by what they prevent · preconditions vs solution design · preventive/detective/boundary · environment as five boundaries · **Managed Environments (sole home) and its licence chain** · estate policies · sharing · solution checker · external-estate boundary · ownership and retirement · matched over/under-governance pairs |
| `alm/release-and-lifecycle.md` | 617 | Which rung does this reach; can it be reversed | Four rungs with what each does **not** give · solution-awareness as prerequisite · pipelines · source-controlled ALM · environment variables and connection references · **no rollback** · named *Reversibility and exit* section · cross-boundary release as a second supply chain · four irreversible week-one choices |
| `performance/performance-and-scale.md` | 511 | Which meter binds first; what must be validated | Workload classification before sizing · five meters, smallest binds · **the seven-way separation** · quota vs throttle vs hard boundary · **limits exclude but never prove** · measurement obligations and fidelity · the benchmark absence as evidence |
| `economics/licensing-and-cost-drivers.md` | 480 | Which meter moves with this shape; which population is obliged | Five mechanisms and their units · cost moves between them without falling · affected-population concepts · capacity meters and what silently consumes them · control-obliged entitlement chain · demand shape · growth at horizon · licence-avoidance trap · sunk capability · exit cost. **Zero prices** |
| `operations/operability-and-support.md` | 581 | Can this organisation run it; is recovery evidenced | Four maturity classes with architectural deltas · operator and support ownership and what *accepted* means as evidence · monitoring, telemetry, correlation · **backup ≠ recovery** and restore reality · objectives, drills, DR · dependency and deployment ownership · skills as availability · four evidence-retention classes |
| `architecture/patterns.md` | 924 | Which composition fits, and what does it import | Ten compositions × (intent, prerequisites, mechanisms, strengths, weaknesses, risks, **imported obligations**, escalation cost, lineage marker) · six import channels · escalation ladder with de-escalation as legitimate · composition rules · 14 selection failure modes |

---

## 6. The 10 CRAFT units

All carry `class: CRAFT`, *"Not an Options D3 pull target"*, and the non-authority statement. None states
a platform limit; each cites the RESEARCH unit that owns any it needs.

| Unit | Lines | Kept | Stripped |
|---|---:|---|---|
| `craft/powerfx.md` | 531 | Validation sequence, 8 traps, standard patterns, context-variable conventions, control-property reference | **All of §1–§2** (two delegation matrices, workarounds), the client-record ceiling in four places, the chunk-size recipe, stale token-tier metadata |
| `craft/screen-patterns.md` | 282 | 5 screen types, density, palette, approval state machine, navigation, journeys, validation UX, layout, states, tabs, responsive, per-screen template, Excel anchors | Two surface-fit verdicts; token-tier metadata |
| `craft/screen-consolidation-rules.md` | 91 | **Every rule byte-identical** — field-count tree, naming, hard caps, Conflicted-row-on-violation | The dead branch sentence; one cross-reference repointed. Marked as the named hard contract with *do not renumber or relax* |
| `craft/excel-translation.md` | 220 | Translation catalogue, financial-function gap (strengthened) | Delegation verdict cells → check-prompts; *"NEVER in Power Fx"* → *"no equivalent"* |
| `craft/flow-craft.md` | 554 | Error-handling patterns, three templates, expression catalogue, adaptive cards, child-flow contract, decomposition heuristics, reporting patterns | Connector limits column, child-flow limits, card expiry, throughput figure, Power BI comparatives, *"authoritative reference"* |
| `craft/security-craft.md` | 425 | 4 matrices, 5 conflict types, log format, all Power Fx blocks, 3 audit blocks, 4 artifact formats | Currency example and symbol; role-stacking control semantics; enforcement-plane phrasing (now owned by the RESEARCH unit) |
| `craft/sql-delivery-conventions.md` | 601 | Medallion layering, audit columns, SP wrapper, DAG, views, RLS scaffold, financial T-SQL, CTE/MERGE/temporal, index strategy, reserved words | **The whole performance-limits table**, type-range annotations, connector query/result limits, hardcoded page size, the fragmentation threshold, the branch sentence |
| `craft/anonymization.md` | 226 | 11 sensitivity types, methods, generators, distributions, log format | Stale cross-reference; the real bank-code map (replaced by the unallocated-range rule) |
| `craft/estimation-model.md` | 288 | Effort tables, multipliers, buffer, phases, overlap, team composition, risk register, output format, quick-win criteria, worked example | **Licence-cost section deleted, not migrated**; the cost column; price front-matter. **Comparative-economics bar stated prominently** |
| `craft/delivery-conventions.md` | 97 | Naming, `su:` stamping, environments/ALM, security/data, go-live and post-go-live checklists, all `TODO(team)` markers (**+2 new**) | Platform assertions now cite `alm/` and `governance/`; three references repointed. **Portuguese preserved** |

---

## 7. Stable / volatile implementation

Ownership is unchanged from the frozen Step 3 model and was implemented, not redefined:

| Responsibility | Owner | Implemented as |
|---|---|---|
| The boundary **question** | `decision-tree.md` | untouched |
| The stable **explanation** | the knowledge unit | 15 RESEARCH units |
| That a fact **is volatile**, and when to re-verify | `decision-model/volatility-register.md` | untouched; **no row added, none copied wholesale** |
| The **current value** used | the engagement's SU row | untouched |

**47 stamped readings across 15 units**, in the mandated form
`> Documented reading · read 2026-09-04 · re-verify: VS-NN (<trigger>)`. Every stamp resolves to an
existing row (mechanically asserted). The heaviest user is `performance/performance-and-scale.md`, which
*names* 20 of the 30 rows — correct for the meter unit — while carrying few figures; the anti-copy test
therefore bounds **stamped figures**, not row references, because naming a row in a *what must be
verified* table is the sanctioned pattern.

---

## 8. Register-coverage finding — the principal structural output of Step 4B

### 8.1 What happened

Step 4A §5.2 permits a figure only when **all four** hold, the third being *it names the
volatility-register row owning its re-verify trigger*. Applying that literally: **~60 decision-relevant
figures had no owning row**, so per the rule the number was dropped and the **boundary shape** carried
instead. This is compliant, and in several cases it produced *better* runtime content — the
myth-correction *"the action-count ceiling is identical on both platforms"* is stronger than either
number. But it is a coverage gap in the register, not in the knowledge.

### 8.2 Subjects with decision-relevant volatile figures and no owning register row

| Domain | Uncovered subject |
|---|---|
| Automation / performance | Structural definition ceilings (action count, nesting depth, array items, switch cases) · the **synchronous response window** · in-run parallelism default and maximum · trigger-concurrency range and de-batching collapse · retry attempt counts by profile · runtime-endpoint inbound concurrency |
| Data | Alternate-key budgets · derived-column budgets and recurrence floor · extension-mechanism per-table ceilings · the search budget · elastic partition sizing · filterable-text index threshold · relationship-traversal depth · join-count per view · row-byte budgets · per-list item ceiling · connector call-rate/concurrency/timeout envelope · log-rate and per-tier storage ceilings |
| Security / governance | **Control enforcement and propagation latency** (flagged independently by three units) · token lifetime as the revocation window · key-inaccessibility and healing windows · per-vault association ceilings · recommendation cadence and warm-up · developer-environment disuse window · sharing-limit enforcement latency |
| ALM / operations | Solution size ceiling · environment-variable length and propagation · free capacity required for restore · service-update station directionality · support effort cap and severity response windows · capacity notification threshold · reported percentile · cross-region enablement duration · RPO/RTO pair |
| Application / economics | Offline record-set ceiling · custom-page and connector-per-app ceilings · team-scoped store ceiling · report-visual row ceiling · wrap bundle-size · storage-rate and run-cost ratios · per-environment storage floor · free-tier ceiling · site minimum assignments |

Also: **`VS-04` is currently doing double duty** — the list-store *access-granularity* threshold and the
*unique-permission scope* ceiling are different facts under one row.

### 8.3 Recommendation

This is **authoring feedback on the frozen Step 3 register**, not a Step 4B defect, and Step 4B did not
add rows (the register is out of scope per Step 4A §21.2). The recommendation for Step 4C or a bounded
Step 3 amendment: add rows for the recurring, decision-material families above — in priority order
**(1) control enforcement and propagation latency, (2) the synchronous response window, (3) structural
definition ceilings, (4) the connector envelope, (5) split `VS-04`.** Until then the affected knowledge
is carried as boundary shape, which is defensible but loses the ability to test a real requirement
against a figure.

---

## 9. Anti-pattern single-home table

All **68** canonical entries (61 `ANTI-PATTERN` + 3 `GATE` + 4 `CONSTRAINT`) were dispositioned; the full
behaviour → primary-home → secondary-reference table is reproduced verbatim below from the
authoring-side sweep.

**Precedence applied** (Step 4A §11.1): decision model → failure-mode note in the owning unit →
architecture-composition concern → authoring-only. **No id appears in any runtime file.**

| Layer | Entries | Result |
|---|---:|---|
| **Decision model only** — `GATE` ×3, the reasoning `CONSTRAINT` ×1, plus behaviours already owned by a blocking entry or composed row | 11 | Not restated in domain knowledge. Lower levels carry the *mechanism* and cross-reference, never the availability verdict |
| **Failure-mode note in the owning unit** | ~48 | Landed as ~30 mechanism-level blockquotes (several entries fold — §9.1) |
| **Architecture-composition concern** | 3 | `architecture/patterns.md` (escalation, de-escalation, composition failures) |
| **Authoring-only** | 6 | Incl. the **1 portfolio-altitude entry**, which must never surface as an engagement finding — its mechanisms fire through five other entries |

**Duplication control result: no behaviour has two primary homes.** Verified by hand at the three known
seams (data policies, managed environments, environment topology) and at the two adjudicated collisions:

- **The limit-vs-proof rule** is stated **once**, in `performance/performance-and-scale.md` §7. The
  *inventing-thresholds* half stays decision-model-only. `automation/` originally restated it; that line
  was rewritten to a cross-reference during verification.
- **Platform-vs-solution commitment** is owned by `performance/` (the distinction); `operations/` carries
  only *what evidence underwrites a commitment*.

### 9.1 One adjudicated fold, recorded rather than improvised

Step 4A §11.3 states the automation family *"is largely one error … so it becomes **one**
decision-sensitive distinction, not N notes."* Applied literally, three entries fold into that single
distinction (shape mismatch · workflow engine as high-volume transaction engine · hand-built transaction
semantics). The remaining four automation entries were **kept as separate notes** because each names a
mechanism the shape distinction does not imply — retry duplication, heterogeneous-availability coupling,
the UI-automation interface test, and the throttling-owner requirement. Recorded as an adjudication.

The full 68-row behaviour table is annexed as **`step-4b-antipattern-single-home.md`**. It is
authoring-side only and deliberately not copied into runtime.

---

## 10. Runtime provenance

**Convention followed: the frozen Step 3 one.** Zero canonical research ids at runtime; the authoring
report carries traceability. This is a documented departure from authoring-map §8 (which specified a
`Research basis:` line per runtime file) — running two provenance conventions in one pack would be worse
than either, and Step 3B1 already resolved it deliberately.

| Layer | Carries |
|---|---|
| **This report** | Per-unit provenance tables: every material decision-grade rule → its canonical file and finding id → stable/volatile → register row |
| **Runtime file** | Factual wording · an HTML-comment header · grade markers · volatility stamps naming a **runtime** row |
| **Engagement** | The reading actually used, with `verificado_em` + `validade` |

**Per-unit provenance tables.** Each of the 15 RESEARCH units has one, covering every material
decision-grade statement. They are now **persisted durably** in
`step-4b-runtime-provenance.md` (created in the pre-4C repair — §23) rather than living only in the
authoring returns, and they are the object gates G1/G3/G7 run against.

**Count correction:** this report originally estimated ≈330 rows *(historical value)*. Enumerated, the
current authoritative figure is **619**.

**Mechanically verified:** 0 research ids in any of the 26 runtime files; 0 in `pack.yaml`.

---

## 11. Conflicted and unknown facts — preserved, not resolved

**Five conflicted quantitative facts. None carried numerically on either side.**

| Conflict | Rendered as | Owner |
|---|---|---|
| **Per-mechanism (custom-connector) throughput ceiling** — two maintained vendor pages disagree by 20× | *conflicted · decision-blocked until measured*, **symmetric across option classes, never a penalty against this platform**. Carried identically in `integration/`, `performance/` and `architecture/` | `VC-01`/`VS-08`, `B-08`, `CD-05` |
| Tenant default database capacity — internally inconsistent in one source | conflicted; confirm in the administration centre | — |
| Elastic-table GA status | unresolved; carried as a maturity risk | `VC-10` |
| Elastic-table alternate-key support | contradicted between sources | — |
| Platform scale positioning vs the published envelopes | both adjectives dropped; capability rows used | — |

**All eight canonical non-blocking reservations survive as unknowns.** Notably: the corpus is
limits-based not benchmark-based (no empirical throughput/latency/concurrency figure exists anywhere);
no security-model performance curve; write-through virtualization has weak production evidence; one
enterprise-boundary pattern is supported synthesis, not vendor-endorsed; prolonged far-side failure in
dual-write is unknown; and platform availability ≠ contractual composite availability.

**The vendor's own self-contradiction on server-side business-rule execution is preserved unresolved**,
carried as *`Assumed`, never `Confirmed`, until tested in the target environment*, with the named
empirical test. It is the single highest-value unresolved contradiction in the whole baseline.

---

*(The full canonical coverage accounting, re-run against the files actually authored, is annexed as
**`step-4b-canonical-coverage-accounting.md`** — every Area 1–12 family plus Block D, with its runtime
RESEARCH home, Step 3 home, CRAFT/downstream home, authoring-only residue, volatile handling, intentional
exclusions and research gaps.)*

---

## 12. Research gaps found

**Research gaps recorded across the 15 units.** None was filled from model knowledge; none was authored
as fact. Where a gap narrowed a unit, the unit states the boundary explicitly.

**Count correction:** this report originally estimated **63** *(historical value)*. Enumerated and
de-duplicated in `step-4b-research-gaps.md` (created in the pre-4C repair — §23), the current authoritative
figure is **120**. All 120 are persisted there, not only the fourteen headline gaps below.

### 12.1 Fourteen priority gaps identified during Step 4B

These are the decision-material, recurring gaps — **not** a list of research commissions. Their closure
mechanisms differ (`commission`, `empirical-test`, `measurement`), and each keeps the `Class` recorded in
`step-4b-research-gaps.md`. **A priority knowledge gap is not automatically a research commission.**
Commission only where the gap is *material* **+** *recurring/general* **+** *not adequately closed by
engagement measurement or a bounded empirical test*. Notably `G-001` is `empirical-test`, `G-006` and
`G-013` are `measurement` — none of the three is a commission candidate.

| # | Gap | Affected units | Why it recurs |
|---:|---|---|---|
| 1 | Whether table-scoped business rules fire on API/integration writes | `data/dataverse.md`, `data/store-boundaries.md` | Every engagement asks *"will this rule hold whichever client writes"*. **An empirical test, not a documentation gap** |
| 2 | Whether one premium capability obliges premium entitlement for **every** user of an artefact | `economics/`, `governance/` | The largest single cost finding in the domain, and still not verbatim-confirmed |
| 3 | Per-operation delegation table per connector | `data/query-and-delegation.md` | Class-level boundaries answer the architecture question; a named screen filter needs the operation level |
| 4 | Control enforcement and propagation latency | `security/`, `governance/` | Decision-material in three separate places; volatility ownership now exists (`VS-21` / `VS-22`); the actual control-enforcement / propagation latency remains a knowledge/evidence gap requiring verification (§8.2) |
| 5 | Whether the previous-version-redeployment mechanism is on by default, and its retention | `alm/` | **The** reversibility mechanism most often assumed rather than enabled |
| 6 | Per-operation AI / agent consumption | `economics/`, `automation/` | Highest-volatility sub-area, and a dated tripwire removes its bundled basis |
| 7 | Gateway throughput and at-scale cost | `integration/`, `economics/` | Every hybrid option's economics |
| 8 | Broker quota envelopes for two of the three services | `integration/`, `automation/` | Selection evidence exists; sizing evidence does not |
| 9 | Entitlement treatment of five newer application surfaces | `application/`, `economics/` | Five cost cells unquantified |
| 10 | Managed-identity reach beyond in-database plug-ins | `security/`, `integration/` | Gates every *"no stored secrets"* requirement |
| 11 | Whether any in-platform dead-letter or circuit-breaker construct is documented | `integration/`, `architecture/` | Determines which composition must carry the guarantee |
| 12 | Composite availability across platform services for a business flow | `operations/`, `performance/` | Every availability commitment. Needs contractual parsing, not search |
| 13 | Measured restore duration at representative volume | `operations/` | Every recovery objective |
| 14 | Multi-tenancy / resale licensing | `economics/` | Unclosed gap, already a scope-blocker |

### 12.2 Permanently open — closed by measurement, not research

No empirical benchmark of any kind · concurrent-user ceiling for any surface · write-amplification
multiplier · standard-table size envelope · audit request cost · replica resynchronisation cost ·
security-model performance curve. Each is carried in its unit as a **measurement obligation** with the
fidelity required, which is the correct runtime treatment.

### 12.3 Agent / conversational surfaces — gap confirmed

Step 4B confirms the canonical position: **no evaluable class, `UNKNOWN` in every dimension.** No domain
file was created (Step 4A §7.5). The Step 3 behaviour is preserved — where the question is material the
output is `UNKNOWN` / decision blocked via scope-blocker `BS-03` and row `VS-20`, with the dated
entitlement tripwire. **Recorded as a future research-commission candidate.** Nothing was invented.

---

## 13. Pull-question fixture results

The 27 Step 4A pull questions were run as an authoring retrieval gate. For each: does exactly one obvious
first pull exist, does that unit exist, and is there enough **decision-grade** content to begin answering
(probed against the portion of the file before its first architecture-grade heading)?

**Result: 27/27.** Every fixture resolves to a single existing first pull whose decision-grade portion
carries the concepts the question turns on. Distribution of first pulls: `automation/` 3 ·
`integration/` 3 · `security/` 3 · `operations/` 3 · `application/` 3 · `performance/` 2 · `economics/` 2 ·
`alm/` 2 · `data/dataverse` 1 · `data/sharepoint` 1 · `data/query-and-delegation` 1 ·
`data/store-boundaries` 1 · `governance/` 1 · `architecture/` 1.

Second pulls occur only where the first exposes a dependency (e.g. residency: `security/` →
`governance/`), which is the designed behaviour. **Options never needs `craft/` to answer a decision
question**, and **no unit returns an option-selection verdict** — asserted mechanically.

---

## 14. Discoverability results

For each of the 15 RESEARCH units: given only a concrete material question, can a reasoner infer from the
directory name, the filename and §0 that this is the correct first pull?

**15/15 YES.** No router was added. Every unit carries **3–4** concrete pull questions (within the design's
two-to-four band) and the mandated boundary line. One unit was trimmed from five questions to four during
verification to hold the band.

The mechanism is exactly three things — directory name (subject boundary), filename (question domain), §0
(the questions). Where the Step 4A design renamed a file for discoverability
(`store-selection` → `store-boundaries`, `*-engineering` → `*-mechanisms`, `preconditions` →
`governance-and-environments`, `alm-engineering` → `release-and-lifecycle`, `cost/` → `economics/`), the
rename was implemented as specified.

---

## 15. Depth-gate results

| Area | Question | Verdict | Where |
|---|---|---|---|
| **Data** | Transactional, authority, integrity, delegation and query boundaries reachable at D3? | **YES** | 5 units. Transactional scope and where atomicity stops · authority per entity/field/phase · integrity that holds on every write path (with the vendor contradiction preserved) · delegation and truncation · access-path and index design |
| **Automation** | Shape, state, unit of failure, wait, retries, idempotency, ordering, limits? | **YES** | Four shapes by *where state lives* and *what the unit of failure is* · ordered classification test · five meters · waits and shape escalation · retry duplication · ordering and dedup as transport properties · envelopes |
| **Integration** | Ownership, guarantee, payload, topology, network, identity? | **YES** | Ownership test **first** · guarantees are the transport's, with the five-answer completeness rule · payload ceilings · four-class topology test · network mutual exclusions · delegated vs service identity fork |
| **Security** | Enforcement plane, trust, egress, identity, key/secret custody, control population? | **YES** | Five planes with enforcer/grain/independent failure · lowest-plane rule + worked negative case · trust boundary and egress · identity propagation and shared-identity collapse · custody where decision-material · control-obliged population |
| **Governance** | Estate preconditions, environments, ownership, managed-control implications? | **YES** | Eight levers by what they prevent · preconditions vs solution design · environment as five boundaries and blast radius · Managed Environments and the licence chain · ownership, detection, retirement |
| **ALM** | Isolation, deployment, source control, reversibility, cross-boundary release? | **YES** | Four rungs incl. what each withholds · pipelines and their dependency · source-controlled ALM · named *Reversibility and exit* section with the enable-in-advance rule · second supply chain |
| **Performance** | Meters, hard boundaries, throttling, proof obligations? | **YES** | Workload classification first · five meters, smallest binds · seven-way separation · quota vs throttle vs hard boundary · limits exclude but never prove · measurement and fidelity |
| **Economics** | Entitlement units, populations, capacity, growth — without prices? | **YES** | Five mechanisms with billing units · affected-population concepts and counting hazards · capacity meters and silent consumers · control-obliged populations · growth at horizon · exit cost. **Zero prices** |
| **Operability** | Operator, support, telemetry, backup/recovery, drills? | **YES** | Four maturity classes with architectural deltas · operator and support ownership with *accepted* as evidence · telemetry depth and its gate · backup ≠ recovery, restore reality, objectives, drills, DR |
| **Architecture** | Compositions and imported obligations, without treating patterns as Options? | **YES** | Ten compositions with intent/prerequisites/mechanisms/strengths/weaknesses/risks/**imports**/escalation/lineage · six import channels · three explicit statements that it never selects and is not the option space |

**No `NO`.** Where a sub-question is not answerable, it is an explicit **research gap** (§12), not silent
shallowness.

### 15.1 Cross-domain consequence coverage

All six required interactions have a stated local home under each unit's *consequences elsewhere*
heading. **No cross-domain matrix file was created.**

| Interaction | Stated in |
|---|---|
| security → economics | `security/` (control-obliged population) · `economics/` |
| data → performance / cost | `data/store-boundaries.md`, `data/dataverse.md` (audit capacity) · `performance/` |
| governance → ALM / operations | `governance/` (managed environments unlock the controls **and** gate pipelines) |
| user / offline → architecture / control / support | `application/` (offline forfeits) → `security/`, `operations/` |
| integration → resilience / operations | `integration/` (sync risk register, reconciliation owner) |
| scale → architecture / economics | `performance/` (the meter that binds moves the design; the meter that bills) |

---

## 16. Consumer updates

Every consumer identified in Step 4A §21 step 9 was inspected and updated. **Path/boundary corrections
only — no consumer behaviour was changed.**

| Consumer | Change |
|---|---|
| `.claude/skills/aisa-blueprint/SKILL.md` | Four paths repointed (`craft/screen-consolidation-rules.md` — the **hard contract** — `craft/screen-patterns.md`, `craft/security-craft.md`, `data/query-and-delegation.md`), in both the inputs list and the execution steps. Added the note that `craft/` never restates the delegation authority |
| `.claude/skills/aisa-simulate/SKILL.md` | Three paths repointed; **added the comparative-economics bar** on `craft/estimation-model.md` with the requirement that its output carry the asymmetry statement |
| `.claude/agent-memory/_universal/solution-architect/anti-patterns.md` | **Restated threshold removed** (`>2000 records`, the store-and-operation verdict) and repointed at `data/query-and-delegation.md`; now states the *mechanism* (silent truncation is a correctness failure) and *delegation-safe ≠ fast* |
| `.claude/agent-memory/_universal/compliance-officer/anti-patterns.md` | Repointed to `craft/security-craft.md`; added that control availability and enforcement plane are owned by `security/security-controls.md` |
| `library/packs/pp/deliverable-templates/claude-design-brief.template.md` | Cross-reference table rebuilt to six rows on the new paths, plus an explicit `craft/` vs `RESEARCH` boundary paragraph; the stale citation-convention example fixed |
| `library/kernel/blueprint-contract.md` | Generic `domain-knowledge/` reference now names the `craft/` units, and states that platform boundaries come from `RESEARCH` units, never from `craft/` |
| `docs/ARCHITECTURE.md` | Deliverable cross-refs, the repository tree (full new taxonomy) and the illustrative `pack.yaml` block updated; the historical v1→v2 migration table annotated with current paths so **no dead path stands alone** |
| `docs/PACK_AUTHORING.md` | Pack-layout comment rewritten to describe the pull-based layer and the RESEARCH/CRAFT split; the manifest example marked *manifest only* |
| `docs/ONBOARDING.md` | One row split into three — the use contract, the 15 RESEARCH units, the 10 CRAFT units with their non-pull-target status |

**Deliberately not changed.** `aisa-blueprint`'s `architecture-templates/<branch>.md` reference and its
*"technology branch"* wording: that is Step 5 territory (architecture templates), not a Step 4B
domain-knowledge path. Flagged in §19 as pre-existing and owned by Step 5.
`.claude/skills/lens-technology/`, `solution-architect.md`, `aisa-options`, `chairman-synthesis` and
`library/kernel/orchestration.md` reference `domain-knowledge/*.md` generically and correctly — the
pull-based, never-preload wording they carry is exactly right and was left untouched.
`docs/IMPLEMENTATION_PLAN.md`, `MIGRATION_FROM_AISA.md`, `REFERENCES_ANALYSIS.md`,
`NEXT_LEVEL_PLAN.md` and `UX_BLUEPRINT_PROPOSAL.md` are historical planning records outside the Step 4A
consumer list and were left as history.

---

## 17. `pack.yaml` updates

- `domain_knowledge` replaced with the **26 new paths**, ordered README → 15 RESEARCH → 10 CRAFT, with
  comments stating it is a **manifest** and explicitly not a load order, routing table, concern map or
  priority list. **No canonical research ids.**
- `pack_version` **1.5.0 → 1.6.0** (minor: a new runtime layer, no consumer contract broken).
- `epistemics.half_lives_override` — see §18.

Asserted mechanically: every declared path exists; every existing unit is declared; the two sets are
equal; no research id; no routing semantics in the data lines.

---

## 18. Epistemic half-life override (Q4-05) — NOT adopted

Step 4A carried a **proposal** for `plataforma-tecnica: 9 meses` and `financeiro: 3 meses`. Step 4B
inspected `library/kernel/states.md`, `pack.yaml.epistemics`, authoring-map Q-08 and the canonical
freshness model, and **did not adopt it**.

**Finding.** The canonical baseline supports the *direction* — it flags several facts as short-half-life
and records two that changed **during the research window itself** — but it names **no duration
anywhere**. Its freshness model is **trigger-based, not duration-based**: re-verify on a named event
(*"the reporting GA announcement"*, *"before any freshness commitment"*), which is precisely what
`volatility-register.md` implements. The kernel defaults (`plataforma-tecnica: 12 meses`,
`financeiro: 6 meses`) carry their own `TODO(team): validate at the pilot retro`, and authoring-map Q-08
itself says *"propose … validate at the first retro"*.

`9` and `3` are round halvings of the kernel defaults with no canonical basis. Adopting them would be
**inventing decay periods**, which the step's own rules forbid.

**Verdict: `half_lives_override: {}` left unchanged. `DEFERRED TO PILOT — non-blocking for Step 4C`.**
The rationale is written into `pack.yaml` at the setting so the next reader does not re-litigate it.

The deeper point, and the reason this is a deferral rather than an open decision: **for this pack the
freshness model is trigger-based, and a duration is only the fallback.**

```text
named volatility / decision trigger   →  primary re-verification mechanism   (volatility-register.md)
generic kernel half-life              →  fallback                            (library/kernel/states.md)
pack-specific duration calibration    →  real engagement pilot
```

The bounded pre-4C repair strengthened exactly the primary mechanism — 19 new ownership rows and a split
(§23) — which makes the duration question **less** load-bearing, not more. Kernel defaults were not
altered.

---

## 19. Tests and regressions

### 19.1 New suite — `.claude/tests/test_pp_domain_knowledge.py` (34 tests, all passing)

Taxonomy (exact 26-file set · counts · no retired flat file survives) · RESEARCH contract (runtime header
and class · §0 with 2–4 pull questions · boundary line · **decision-grade section first** · alternatives-
symmetry statement) · CRAFT contract (class header · non-authority statement, matched in **either
language** · no volatility stamp · no delegation figure in `craft/powerfx.md` and it must defer to the
owner · the estimation-model comparative bar · screen-consolidation caps preserved) · hygiene (no price
token in prose · **no canonical research id** · no obsolete branch vocabulary · no router/load-order
semantics unless negated · **no deleted R0 threshold restated** · no asserted selection verdict) ·
volatility (every stamp names an existing row · every referenced row exists · **the conflicted ceiling is
not carried numerically** · no unit reads as a current-facts database) · manifest (paths exist ·
bidirectional completeness · no research id · manifest-only · version bumped) · consumers (**no dead path
stands alone** · the blueprint hard contract resolves · the architect memory no longer restates a
threshold · design-brief cross-references resolve) · README contract.

### 19.2 Regressions

| Suite | Tests | Result |
|---|---:|---|
| `test_pp_domain_knowledge` (new) | 34 | **OK** |
| `test_pp_options_decision_model` (Step 3) | 94 | **OK** |
| `test_pp_discovery_runtime` (Step 2 / Phase G) | 22 | **OK** |
| `test_council_wiring` | 31 | **OK** |
| `test_orchestrator_wiring` | 23 | **OK** |
| `test_state_scaffold` | 15 | **OK** |
| **Total** | **219** | **all passing** |

*Post-repair state (§23.8):* `test_pp_domain_knowledge` was extended from 34 to **46** tests and the
five regression suites above were re-run and green — **231** tests across the six suites. The 219 figure
is the historical total at first issue of this report.

**One pre-existing test assertion was loosened, and it is worth flagging.**
`test_pp_options_decision_model.test_pack_yaml_is_valid_and_bumped` pinned `pack_version` to *exactly*
`1.5.0`. Pinned that way it asserted *"no later authoring step has run"*, which is not what it was for —
and §17 of this step's own brief mandates a bump. It is now a **floor** (`>= 1.5.0`, i.e. the Step 3 line
landed) with the reasoning in its docstring. **No Step 3 runtime file was touched.**

Test-precision fixes made during verification (six), each because the assertion was wrong rather than the
file: line-wrapped sentences needed whitespace-normalising before substring matching; the CRAFT boundary
statement is legitimately Portuguese in one file; sample T-SQL contains the phrase *"price per category"*
which is a domain column, not a platform price, so the price scan now skips fenced code; the manifest's
own comments negate the words the routing check looks for; the register-copy bound belongs on stamped
figures rather than row references; and *"therefore inappropriate"* legitimately appears where a unit
names it as forbidden.

---

## 20. Deviations from Step 4A

| # | Deviation | Rationale |
|---:|---|---|
| 1 | **~60 decision-relevant figures dropped for want of an owning register row** (§8) | Step 4A §5.2 condition 3 applied literally. Compliant, and often better content — but it is the step's principal finding and needs a decision |
| 2 | Three units exceed the *typical* 150–320-line guidance: `architecture/patterns.md` (924), `alm/` (617), `operations/` (581) | Step 4A §45 forbids size as a hard gate and asks for semantic cohesion. Each answers one coherent question family; the length is mandated content — ten compositions × nine fields incl. the imports block named as the most decision-bearing content; four rungs + a dedicated reversibility section; ten required operational depths. **Reviewed and accepted, not trimmed** |
| 3 | The automation anti-pattern family folds to **one** classification distinction **plus four** mechanism-distinct notes, not one note total (§9.1) | Each of the four names a mechanism the shape distinction does not imply. Recorded as an adjudication |
| 4 | Products are **named plainly** in domain knowledge (Dataverse, SharePoint, Power Automate, …) while the frozen Step 3 spine is entirely de-vendored | The approved taxonomy itself names three stores in filenames, domain knowledge is Options-only, and Options is the one phase where naming vendors is allowed. De-vendoring would have hurt discoverability and matched no approved filename |
| 5 | `architecture/patterns.md` §0 boundary line reads *"does not decide which composition wins, and never selects or renders a blueprint"* | The mandated *"does not decide"* form plus the file-specific selection/rendering prohibition, which the design also requires |
| 6 | One unit trimmed from five §0 pull questions to four | Step 4A §4.2 specifies two to four |

**No deviation changes an approved contract.** Nothing in Step 3 was reopened; no decision logic moved
into domain knowledge; no canonical evidence file was modified.

---

## 21. Unresolved open questions

| # | Question | Status |
|---|---|---|
| **Q4-01** | Does the team accept `provenance: CRAFT` on ten files, including the estimation model used commercially? | **Implemented as designed.** Needs team confirmation; the label costs the craft files nothing and protects the research files' authority |
| **Q4-02** | Language | **Resolved as designed** — RESEARCH English; CRAFT keeps its consumers' language (`craft/delivery-conventions.md` stays Portuguese) |
| **Q4-03** | `screen-consolidation-rules.md` moves path but keeps its filename | **Resolved** — consumers updated in the same step; rules byte-identical |
| **Q4-04** | Does the S8 bar on `craft/estimation-model.md` need to be machine-checkable? | **Stated rule + a test asserting the bar is documented in the file.** A hard block would need a loader the pack does not have |
| **Q4-05** | Half-life overrides | **DEFERRED TO PILOT — non-blocking for Step 4C.** Not adopted (§18). The canonical PP freshness model is primarily **trigger-based**: a named volatility or decision trigger is the primary re-verification mechanism, the generic kernel half-life is the fallback, and pack-specific duration calibration belongs to the **real engagement pilot**. No canonical evidence supports the proposed durations, so there is nothing to decide before Step 4C |
| **Q4-06** *(new)* | **Register coverage (§8).** ~60 decision-relevant volatile subjects have no owning row, and `VS-04` is doing double duty | **RESOLVED** — bounded pre-4C volatility-register amendment (§23.1). 19 family rows added, `VS-04` split, uncovered subjects re-adjudicated. No Step 3 decision semantic changed. *(Historical status at first issue of this report: OPEN.)* |
| **Q4-07** *(new)* | The vendor's self-contradiction on server-side business-rule execution | **OPEN by design** — carried as `Assumed` with a named empirical test. Highest-value single test in the baseline |
| **Q4-08** *(new)* | `aisa-blueprint` still requires *"a final D-NNN with a technology branch"* and embeds `architecture-templates/<branch>.md` | **OPEN — Step 5 scope.** Pre-existing; deliberately untouched here |
| **Q4-09** *(new)* | 14 priority knowledge gaps (§12.1) | **OPEN.** Fourteen priority gaps with **different closure mechanisms** (`commission`, `empirical-test`, `measurement`). Only those classified `commission` are candidates for a commissioned extension of the canonical baseline; e.g. `G-001` is an `empirical-test`, `G-006` and `G-013` are `measurement` |

---

## 22. Recommendation for the Domain Knowledge gate

**Step 4B does not close Step 4.** It proves the layer was authored faithfully against the approved
design: the taxonomy is exact, the contracts hold mechanically, provenance is traceable authoring-side,
coverage is accounted for, and the suites pass (**231** tests post-repair — the domain-knowledge suite at
**46** plus the five green regression suites; 219 was the pre-repair total). It does **not** prove the layer *behaves* correctly under
real decision pressure.

**A bounded Step 4C semantic/pull gate is required**, and should test what §13–§15 could only approximate:

1. **Concrete D3 questions run end-to-end** — not keyword probes. Give a reasoner a real engagement
   fragment and a material concern, and check what it actually pulls and concludes.
2. **Pull discoverability under ambiguity** — questions that *look* like they belong to two units
   (offline × confidentiality; reporting × store choice; hybrid cost × operator availability).
3. **Sufficient technical depth** — can the answer survive an adversarial *"how do you know?"*
4. **Research-gap behaviour** — does the reasoner correctly emit `UNKNOWN` / decision-blocked at a gap
   instead of filling it? The agent-surface question is the sharpest fixture.
5. **Volatility handling** — does it re-read rather than quote a stamped figure, and does it refuse to
   settle the conflicted ceiling?
6. **No decision leakage** — does any pull produce a verdict the decision model did not ask for?
7. **No comparator bias** — does platform depth quietly become preference, especially at the economics
   stage where `craft/estimation-model.md` is barred?

**One item was settled before 4C**, because it changed runtime content: **Q4-06**, the register-coverage
gap — closed by the bounded pre-4C repair recorded in §23. **Q4-05** (half-lives) is **deferred to the
pilot** and is **not** a Step 4C blocker: the freshness model is trigger-based, the triggers are in the
register, and a duration override is a calibration question a real engagement answers.

`STEP 4C SCOPE PROPOSED: semantic / pull gate only — no re-authoring, no re-taxonomy`

---

---

## 23. Bounded pre-4C repair — appended 2026-09-04

**The Step 4B implementation above is unchanged and remains approved.** This is an append-only note. The
15 RESEARCH units, 10 CRAFT units, README contract, directory taxonomy, pull semantics, RESEARCH/CRAFT
boundary, grade ordering, anti-pattern dispositions, no-price rule, no-router rule, comparator neutrality,
the agent/conversational `UNKNOWN` boundary and Step 3 decision semantics were **not** reopened.

### 23.1 Volatility-register amendment

The repair closed the register-coverage gap this report named as its principal structural finding (§8) —
a **volatility-ownership** gap, not a research gap: the knowledge existed and the figure had to be dropped
only because no row could own its re-verification trigger.

`library/packs/pp/decision-model/volatility-register.md` gained a **§2A ownership amendment**:

| | Count |
|---|---:|
| Family rows added (`VS-21` … `VS-39`) | **19** |
| Rows split (`VS-04` → `VS-04` + `VS-29`) | **1** |
| Existing rows whose scope was clarified | 7 (`VS-05`, `VS-06`, `VS-17`, `VC-05`, `VC-06`, `VC-07`, `VC-10`) |
| Register rows before → after | 33 → **52** |

The five mandatory priority families were adjudicated to **minimum sufficient granularity** rather than to
one row per number, and were **split** wherever subject, mechanism, trigger and consequence diverged:

| Priority | Outcome | Why not one row |
|---|---|---|
| **V1** control enforcement / propagation timing | **two** rows — `VS-21` propagation, `VS-22` revocation | Propagation is not credential lifetime: different mechanism, different consequence (*not yet enforcing* versus *a removed user still has access*) |
| **V2** synchronous execution / response windows | **one** row — `VS-23` | Every member is a wait a caller experiences, and the long asynchronous window is the same decision's other half |
| **V3** structural definition ceilings | **three** rows — `VS-24` orchestration, `VS-25` application artefact, `VS-26` release artefact | Three different service families with three different remedies. *All are limits* is not a reason to merge |
| **V4** connector / integration execution envelope | **two** rows — `VS-27` envelope, `VS-28` estate currency | A design ceiling and a standing operating obligation are different things. **`VS-27` explicitly excludes the conflicted custom-connector ceiling** so a family row could not absorb it into a settled value |
| **V5** split `VS-04` | **done** — `VS-04` keeps the access-path threshold, `VS-29` takes the unique-permission scope ceiling | Same store, different fact, different decision |

Remaining §8.2 subjects were classified **A** (added to an existing coherent owner) · **B** (new family
row) · **C** (figure left out of runtime) · **D** (research gap) · **E** (measurement-owned). Full
adjudication in `step-4b-number-adjudication.md` §3, §4.

**Reference migration.** The one `VS-04` use that was an *authorization* fact was repointed to `VS-29`
(`security/security-controls.md`); the access-path uses stayed on `VS-04`; `data/sharepoint.md` and
`data/store-boundaries.md` had their combined rows split. Nineteen *what must be verified* rows were added
across nine units so that **all 52 register rows are now referenced by at least one unit, and no unit
references a non-existent row** — both asserted mechanically.

**Nothing in the amendment changed a decision semantic.** No stage, concern, blocking entry, option class,
outcome, composed row or comparator rule was touched, and the register still supplies no figures.

### 23.2 Quantitative readings restored — selectively

The ~60 dropped figures were re-adjudicated against all four Step 4A conditions **plus** the survival test
*would knowing this reading materially help test a real requirement?*

| | Count |
|---|---:|
| Dropped figure subjects re-adjudicated | **60** |
| **Restored** to runtime — figure families | **15** |
| **Restored** to runtime — individual numeric readings | **65** (14 carriers, 8 units) |
| Left as boundary shape, now with a named owner | 14 subjects |
| **Deliberately left out** entirely (shape suffices, or price-adjacent) | 14 subjects |
| Measurement-owned — no published figure would settle the requirement | 2 subjects |

Volatility stamps across the layer: **47 → 53**. The other restorations were appended to stamps
that already existed, which is why the carrier count (14) is lower than the family count (15).

Restored where a requirement is *literally compared against* the figure: synchronous response windows ·
orchestration structural ceilings (which also makes the *identical on both platforms* correction
verifiable) · run-duration ceilings · retry defaults by profile · disablement countdowns · content
throughput by profile · the interface-automation queue envelope · the connector execution envelope ·
payload, truncation and batch ceilings · the alternate-key budget · the list-store join ceiling · the
list-store permission scopes · the aggregation ceiling and replication floors · the team-scoped ceiling ·
backup retention by environment class.

Deliberately **not** restored, and the two most instructive cases:

- **The per-identity service-protection triple** — its effective value is the published figure multiplied
  by an undisclosed, licence-dependent server count. Carrying it invites exactly the arithmetic the
  baseline forbids. The design must be **tolerant, not sized**.
- **The entitlement request sets** — the *instruction to size against official limits* is the content; the
  numbers are mid-transition with an unannounced enforcement date.

Also left out: storage-rate and run-cost **ratios** (price-adjacent — ordinal ordering carried instead) and
the bundled-credit quantity.

### 23.3 Conflicted evidence — unchanged

**No conflicted fact became a settled reading.** All five survive: the custom-connector throughput ceiling
(symmetric, decision-blocked, `VC-01`/`VS-08`, `B-08`, `CD-05`) · tenant default database capacity ·
elastic-table maturity state · elastic-table alternate-key support · the platform scale positioning. The
register now owns the **re-verification** of the elastic maturity state (`VS-32`) without supplying an
answer.

### 23.4 Durable authoring evidence

Three annexes created, so the authoring evidence no longer lives only in the authoring returns — a
**provenance annex**, a **number-adjudication annex** and a **research-gap annex**:

| Annex | Content |
|---|---|
| `step-4b-runtime-provenance.md` | **619** material decision-grade rules → canonical file and finding id → stable/volatile → volatility row → research-gap marker, across all 15 units |
| `step-4b-number-adjudication.md` | Every source numeral classified, per source file, **updated to reflect this repair** |
| `step-4b-research-gaps.md` | **All 120** research gaps with materiality, runtime treatment, classification, blocking status and next action |

Two authoring-side tables written during Step 4B were also promoted to annexes:
`step-4b-antipattern-single-home.md` and `step-4b-canonical-coverage-accounting.md`.

**All five annexes are authoring-side.** No runtime gap registry, no runtime provenance subsystem, and no
canonical research id entered any runtime file.

### 23.5 Report count corrections

| Location | Was | Is |
|---|---|---|
| §2 *new units with no migration source* | 7 | **11** (the enumerated list) |
| §10 provenance rows | ≈330 *(estimated)* | **619** *(enumerated — authoritative)* |
| §12 research gaps | 63 *(estimated)* | **120** *(enumerated — authoritative)* |

The first was the correction this repair was asked to make; the other two were found while persisting the
annexes and are corrected on the same principle — the report had estimated rather than counted.

### 23.6 Research commissions

**None executed.** The fourteen §12.1 items are recorded as **priority gaps** in
`step-4b-research-gaps.md` §2, each keeping its own `Class` — `commission`, `empirical-test` or
`measurement`. Only the `commission` ones are commission candidates. Commission later only where
**material + recurring/general + not adequately closed by engagement measurement or a bounded empirical
test**. Agent / conversational capability remains a candidate for a
**dedicated** commission (`G-118`, `G-119`).

### 23.7 What did not change

- No new research, no web access, no canonical evidence file touched.
- No decision semantics: `decision-tree.md` and the other four registers are byte-identical.
- No domain-knowledge unit was re-taxonomized, renamed, split or merged.
- `pack.yaml.epistemics.half_lives_override` stays `{}` — **deferred to pilot**, non-blocking for Step 4C.
- Kernel defaults in `library/kernel/states.md` untouched.
- `pack_version` unchanged at `1.6.0`: the register amendment and the figure restorations are the same
  authoring cycle as Step 4B, not a new one.

### 23.8 Tests

`.claude/tests/test_pp_domain_knowledge.py` extended to **46** tests. Step 3 regressions re-run and green;
the T-01…T-18 semantic replay was **not** re-run, because no Step 3 decision semantic was modified.

`STEP 4B PRE-4C BOUNDED REPAIR: PASS` · `READY FOR STEP 4C — SEMANTIC/PULL GATE: YES`

---

`STEP 4B — DOMAIN KNOWLEDGE IMPLEMENTATION: PASS`
`RESEARCH UNITS AUTHORED: 15/15`
`CRAFT UNITS AUTHORED: 10/10`
`TOTAL DOMAIN FILES: 26`
`CANONICAL RESEARCH MATERIAL ACCOUNTED FOR: YES`
`UNSUPPORTED MATERIAL CLAIMS AUTHORED: 0`
`RESEARCH GAPS RECORDED: 120`
`NEW RESEARCH PERFORMED: NO`
`MODEL KNOWLEDGE USED TO FILL RESEARCH GAPS: NO`
`DOMAIN KNOWLEDGE PRELOADED: NO`
`ROUTER INTRODUCED: NO`
`PRICES PRESENT IN DOMAIN KNOWLEDGE: NO`
`CONFLICTED VALUES CARRIED AS SETTLED NUMBERS: NO`
`VOLATILE FIGURES STAMPED: YES`
`RESEARCH IDS PRESENT IN RUNTIME DOMAIN FILES: NO`
`OBSOLETE OPTIONS BRANCH MODEL PRESENT: NO`
`CRAFT STATES PLATFORM LIMITS INDEPENDENTLY: NO`
`PULL QUESTIONS WITH CLEAR FIRST TARGET: 27/27`
`MATERIAL DEPTH GATE: PASS`
`DOMAIN KNOWLEDGE CAN SELECT WINNING OPTION: NO`
`PP KNOWLEDGE CREATES COMPARATOR PREFERENCE: NO`
`STEP 3 REGRESSION: PASS`
`READY FOR STEP 4B REVIEW: YES`
