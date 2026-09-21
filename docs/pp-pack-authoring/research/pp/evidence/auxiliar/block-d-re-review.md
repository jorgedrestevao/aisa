Re-Review Status: COMPLETE
Reviewer: independent bounded re-review (fresh pass over the repaired files)
Re-review date: **2026-09-03**
Scope: **verification only.** No Block D file was modified. No pack authoring performed. `library/packs/pp/` untouched. Areas 1–12 read only.
Authority: `research/pp/evidence/block-d-review.md` (verdict `PASS WITH CORRECTIONS`) and `research/pp/evidence/block-d-repair-report.md` (verdict `READY FOR BLOCK D RE-REVIEW: YES`).

# Block D Bounded Re-Review

Inputs read in full: `block-d-review.md` (693 lines) · `block-d-repair-report.md` (485) · `decision-criteria.md` (3,750) · `anti-patterns.md` (2,505) · `alternatives.md` (804) · `decision-intelligence-matrix.md` (687).
Canonical Areas 1–12 consulted only where a repair's evidence lineage or a repaired claim needed verification (§5). No new broad research. No external research.

**Method note.** Every count in this document was recomputed from the files themselves, from the criterion bodies and register tables upward. **No assertion in `block-d-repair-report.md` was accepted as evidence.** Where my recount agrees with the repair report I say so and give the derivation; where it does not, the derivation is stated so a third reader can repeat it.

---

## 1. Re-Review Status

| | |
|---|---|
| Files re-read in full | 6 of 6 |
| Criteria re-examined | 116 of 116 |
| Anti-patterns re-examined | 68 of 68 |
| Alternative classes re-examined | 11 of 11 |
| Matrix rows re-examined | 116 criterion rows · 12 composed rows · 11 volatility rows · 16 scenarios |
| Canonical id references resolved mechanically | **3,066 occurrences / 1,520 distinct (file, id) pairs** |
| Unresolved canonical references | **0** (one scanner false positive: `SUB-15`, from the state name `SUB-15-MINUTE`) |
| Internal dangling `DC-D-` / `AP-D-` / `ALT-` references | **0 / 0 / 0** |
| HIGH findings from the original review re-tested | 4 of 4 |
| MEDIUM findings from the original review re-tested | 11 of 11 |
| Adversarial scenarios re-run | 16 (all 12 the brief names) |
| New findings raised | 14 — CRITICAL 0 · **HIGH 1** · MEDIUM 3 · LOW 10 |

---

## 2. Headline verdict

**Three of the four HIGH findings are genuinely resolved. One — H-01, the exit taxonomy and its counts — is resolved at the level the repair measured and unresolved at the level the review actually asked about.**

The repair's mechanical claims are true and I reproduced them all. The taxonomy exists, is named before any count changed, and the three representations of it (criterion body tag, §3.1 register flag, matrix exit cell) are **byte-for-byte in agreement on all 116 criteria** — I generated all three independently and diffed them. The per-domain table in §3 matches a fresh recount on all 12 rows × 7 columns. `B` is exactly 28 and `§5.2` lists exactly those 28. `G` is exactly 28 and §4A.2 contains exactly those 28 in both directions. Composed disqualifiers are 12 in all three homes. Anti-pattern classifications are 61/3/4 = 68. That is a materially better state than the 36/46/48 contradiction the review found, and the work behind it is real.

What the repair did not do is test whether the **classification is sound**, as distinct from consistent. Two things fail:

- **Four criteria were promoted into an exit class on fields that name nothing leaving the platform.** DC-D-025, DC-D-030, DC-D-032 and DC-D-088 read *"none evidenced; the answer is a store change"* / *"an archival store"* / *"a store, model or surface change"* / *"a store and pattern change, **not a platform change**"*. §2.5's own `Xr` test is *"The field names **what** leaves"*. These name nothing. On the file's own test the direct-exit count is **50, not 54**, and the dash count is **42, not 38**. Their matrix cells are now **bare `[Xr]` markers with no exit text at all** — strictly less information than the pre-repair `—`, which this file itself calls *"load-bearing"*.
- **The exit-class → outcome-class mapping is wrong for that subset, and the matrix's own worked scenario contradicts it.** Matrix §1 states that an `Xr` *"produces a **hybrid or partial-scope** outcome (`decision-criteria.md` §6.2 classes 3, 4, 6), never a whole-solution rejection"*, and §6.2 class 6's trigger is *"An `Xr` exit fires and no in-scope hybrid shape is available"*. T-02 (Excel replacement) fires **four** `Xr` criteria at their exit states with hybrid scoped to reporting only, and correctly emits class 2 `POWER PLATFORM — FIT WITH CONSTRAINTS`. The rule says class 6; the instance says class 2. A pack built from the rule emits `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` for a within-platform store change.

A third defect sits in the seam between H-01's repair and M-02's: **`Xc`'s declared home does not contain 18 of the 24 things pointed at it.** §2.5 defines `Xc` as *"An exit exists only in combination with named criteria — its home is `decision-intelligence-matrix.md` §3 and `anti-patterns.md` AP-D-059."* Eighteen of the 24 `Xc` criteria appear in no §3 row. Step 4 of the evaluation order therefore has no rule to run for them, so 18 declared exits are undetectable by the mechanism declared to detect them. M-02 reconciled the register to 12 in three files while H-01 created 24 pointers into it; each repair is locally correct and they are mutually inconsistent.

Separately, one MEDIUM is gate-blocking in its own right: **the "closed" outcome set is not closed, and its gap leans toward Power Platform.** §6.2 declares twelve classes and states *"The set is **closed**: `anti-patterns.md` and `decision-intelligence-matrix.md` emit from this list and no other."* T-01 emits `COLLABORATION-PLATFORM NATIVE` and T-05 emits `single platform + a tripwire`; neither is in the set. The underlying cause is worse than two stray labels: **the set has no class for "an alternative is sufficient and Power Platform is not excluded"** — which is ALT-003's own outcome and the most common departmental engagement shape. Class 8 is defined as *"the terminal form for classes 5, 6 and 7"*, so it cannot carry a non-exclusion. A pack authoring a decision tree from §6.2 must either drop T-01's alternative branch — biasing systematically toward Power Platform on the commonest case — or invent a class.

**Evidence integrity is the strongest part of the repair and it passes without qualification.** I re-resolved 3,066 canonical id references across the four files; all resolve. The two failures the original review recorded (`IA-U-14` / `IA-C-01`) now resolve because both forms are named. I read every one of the fifteen facts DC-D-116 asserts against the canonical file it cites, and all fifteen are present verbatim; the same for AP-D-068's three mechanisms. Nothing was invented for agents, for custom development, for Azure, for incumbents, for other low-code platforms or for packaged products. `UNKNOWN`, `CONFLICTED`, `VOLATILE VALUE`, `INF` and comparator absence are preserved everywhere I tested, including where preserving them is inconvenient.

**H-02 is resolved cleanly and I tested it hard.** An exhaustive search for `PREFERRED`, `BETTER`, `CHEAPER`, `FASTER`, `BEST` and equivalents across all four files returns **no surviving comparative recommendation about an unevaluated class**. Every occurrence of `PREFERRED` is either a state name (`ORDER PREFERRED`, `CORPORATE NETWORK PREFERRED`), a repair note explaining a retirement, or a before/after table row. No scenario converts `Power Platform excluded` into `Alternative X preferred`. Scenarios 7, 8 and 9 of the brief (T-12, T-13, T-14) — the three the brief flags — are the cleanest cases in the file.

---

## 3. H-01 — Exit taxonomy and counts

**Original finding.** Three files reported 36 / 46 / 48 for the same quantity; twelve criteria carried a written exit and no flag; the platform-vs-responsibility distinction was used and never named.

**Repair claim.** RESOLVED. Five classes; all 116 re-flagged; every derived count regenerated; DC-D-093/DC-D-104 reconciled; DC-D-039/DC-D-040 parity fixed.

**Re-review verdict: NOT RESOLVED.** See finding **R-01** (HIGH). What follows is the evidence, positive parts first.

### 3.1 What I verified as correct

The taxonomy is **explicitly defined** (`decision-criteria.md` §2.5) with five mutually exclusive classes, a per-class classification test, a stated precedence rule for multi-consequence fields, and an explicit statement that `B`, `B*`, `G` and `V` are orthogonal flags and not exits. Matrix §1 reproduces the classes with a warning that `Xr` is *"not a weaker `Xp`"*. That is the named distinction the review asked for.

**Three representations, independently extracted, in exact agreement.** I parsed (a) the inline `[`class`]` tag at the head of each of the 116 `PP negative/exit` fields, (b) the flag column of the §3.1 register, and (c) the exit cell of each of the 116 matrix §2 rows, then diffed all three:

| Comparison | Result |
|---|---|
| Criterion body tag present on every criterion | **116 / 116** |
| Register row per criterion, exactly one | **116 / 116**, 0 duplicate ids |
| Matrix row per criterion, exactly one | **116 / 116**, 0 duplicates |
| Body tag == register flag | **116 / 116**, 0 mismatches |
| Body tag == matrix exit class | **116 / 116**, 0 mismatches |
| Register rows carrying more than one exit class | **0** |

**The distribution I recount matches every published home** (§2.5's table, §3's domain table, §9 item 5, §11, matrix §1's legend, matrix §9):

| Class | My recount | Published |
|---|---|---|
| `Xp` | 15 | 15 |
| `Xr` | 34 | 34 |
| `Xe` | 5 | 5 |
| `Xc` | 24 | 24 |
| `—` | 38 | 38 |
| Direct (`Xp`+`Xr`+`Xe`) | 54 | 54 |
| Total | 116 | 116 |

**The §3 domain table is correct on every cell.** I recomputed all 12 domains × (count, `Xp`, `Xr`, `Xe`, `Xc`, `—`, `B`, `G`) from the criterion bodies' own `Domain` fields plus the DC-D-116 → Users assignment the file declares, and every one of the 96 cells and the totals row matches. Governance produces 0/0/0/0 and 7 dashes; ALM produces 0/0/0/1 and 7 dashes — so the claim that **Governance and ALM produce zero direct exits between them survives the recount**, and the load-bearing argument in §9 item 5 stands on the corrected numbers rather than on the old 36.

**Blocking counts are correct.** `B` = 28 exactly; §5.2's table lists exactly those 28 ids, no more and no fewer. `B*` = 3 exactly (DC-D-113, DC-D-115, DC-D-116), carried in a separate table so §5.2's set stays 28. This is the cleanest mechanical result in the repair.

**The review's named pair is fixed.** DC-D-039 and DC-D-040 both read `Xr` in body, register and matrix. Their consequences are structurally identical (*"the integration responsibility leaves the platform"* / *"a documented exit for the integration responsibility"*), so identical classification is correct.

**DC-D-093 and DC-D-104 are reconciled.** DC-D-093's body states an economic exit and its matrix cell now reads `[Xe] Premium plus external prerequisites across an unfunded population → economically infeasible`. DC-D-104's body and cell both read `[Xc]`. L-07 is closed.

**The nine reclassified fields are the ones the repair says they are.** I extracted, without reference to the repair report, every `Xr` field whose text opens with a form of *"none"*: exactly DC-D-006, 021, 025, 030, 032, 046, 053, 056, 088 — the nine named. So the repair's derivation `45 + 9 = 54` is reproducible.

### 3.2 What fails

**(a) Four of the nine reclassifications do not meet §2.5's own test.**

| Criterion | `PP negative/exit` field, verbatim | What leaves the platform |
|---|---|---|
| DC-D-025 | *"none evidenced; the answer is a store and pattern change, **not a platform change**."* | nothing |
| DC-D-030 | *"none evidenced; the answer is a store change."* | nothing |
| DC-D-032 | *"none evidenced; the answer is an archival store."* | unstated |
| DC-D-088 | *"none evidenced; the answer is a store, model or surface change."* | nothing |

§2.5's `Xr` test: *"The field names **what** leaves (`the integration responsibility`, `the affected attribute`, `the run mechanism`, `the interactive read surface`)."* §2.5's `—` test: *"The field says `none evidenced` with no combination and no delegation."* All four match the `—` test literally and fail the `Xr` test. The class *definition*'s second limb (*"or an in-platform pattern becomes unavailable"*) can be stretched to admit them, but that limb is exactly what makes the class unsound (see (b)) — and DC-D-025 explicitly rules itself out by saying *"not a platform change"*.

The five other reclassifications survive: DC-D-006 and DC-D-021 name specific in-platform patterns that become unavailable and say so; DC-D-053 and DC-D-056 name the mechanism the responsibility moves to; DC-D-046 is ambiguous by its own admission (*"may or may not be outside the platform"*).

**Corrected counts on the file's own test:** `Xr` **30**, `—` **42**, direct exits **50** of 116, not 54 / 38. Every published home carries the uncorrected pair.

**(b) The `Xr` → outcome-class mapping is contradicted by the matrix's own scenario.**

- Matrix §1: *"an `Xr` produces a **hybrid or partial-scope** outcome (`decision-criteria.md` §6.2 classes 3, 4, 6), never a whole-solution rejection."*
- §6.2 class 3's trigger requires *"a bounded, nameable excess (compute, guarantee, duration, protocol, network reach, secret-free identity)"* — a store change is none of these.
- §6.2 class 4's trigger requires *"the integration or authority responsibility"* — not this either.
- §6.2 class 6's trigger: *"An `Xr` exit fires and no in-scope hybrid shape is available, or the responsibility is the whole deliverable."* That is satisfied, and it emits **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`**.
- **T-02 fires four `Xr` criteria at their exit states** (DC-D-023 `ABOVE CEILING`, DC-D-030 `ROUTINE`, DC-D-026 `FIELD`, DC-D-031 aggregation) with hybrid scoped to reporting only, and emits **class 2 `POWER PLATFORM — FIT WITH CONSTRAINTS`** — which is the right answer.

The rule and the worked instance give different answers on the corpus's own best-evidenced scenario. The scenarios are prose read by a human; the rule is what a pack implements. Result: a pack that follows matrix §1 and §6.2 class 6 emits a false exclusion of Power Platform for routine concurrent-edit, attachment-volume, retention and records-per-path findings.

**(c) Five matrix exit cells assert a class and state nothing.**

`DC-D-025`, `DC-D-030`, `DC-D-032`, `DC-D-046`, `DC-D-088` carry a bare **`[Xr]`** with no exit sentence. Five more carry a bare **`[Xc]`** with no combination named: `DC-D-011`, `DC-D-022`, `DC-D-037`, `DC-D-038`, `DC-D-080`. (Their criterion bodies do name the combinations; the matrix cells do not.) Both classes' §2.5 tests require the field to say what leaves or what it combines with. Pre-repair these ten cells carried `—`, which the matrix's own §1 calls *"load-bearing"* information; they now carry a class marker with no content, which is a net loss for the representation a pack reads.

**(d) `Xc`'s declared home does not hold 18 of the 24 things pointed at it.**

§2.5: *"`Xc` — Composed-only exit. No exit from this criterion alone. An exit exists only in combination with named criteria — **its home is `decision-intelligence-matrix.md` §3 and `anti-patterns.md` AP-D-059**."*

I expanded every criterion id named in matrix §3's twelve rows (including the compressed `DC-D-028, 029, 021` forms) and intersected with the 24 `Xc` criteria. Eighteen are named in no row:

`DC-D-004` · `DC-D-011` · `DC-D-022` · `DC-D-024` · `DC-D-027` · `DC-D-035` · `DC-D-038` · `DC-D-047` · `DC-D-048` · `DC-D-058` · `DC-D-061` · `DC-D-080` · `DC-D-085` · `DC-D-086` · `DC-D-087` · `DC-D-090` · `DC-D-098` · `DC-D-112`

Their bodies name real combinations that the register does not contain — DC-D-011 *"combines with DC-D-012 and DC-D-013"*, DC-D-022 *"combines with DC-D-023 and DC-D-088 to disqualify specific stores rather than the platform"*, DC-D-038 *"combines with DC-D-044"*, DC-D-080 *"an unrehearsed reversibility claim is a documented composed risk"*. None is a §3 row. Step 4 of the evaluation order (*"COMPOSED DISQUALIFIERS — §3 above → run explicitly"*) has nothing to run for eighteen of the twenty-four criteria whose only exit is supposed to live there.

This is the structural cost of repairing H-01 and M-02 independently: M-02 correctly reconciled the register to **12** in three files, H-01 correctly created **24** `Xc` flags, and nobody checked that the second points into the first.

**(e) One stale derived count survives inside the regenerated file.**

`decision-intelligence-matrix.md` §9's closing paragraph: *"The most important thing this matrix says is in its **79 dashes** and its §5 ordering."* The table immediately above it says 38. 79 is the pre-repair figure.

---

## 4. H-02 — Unsupported preference outcomes

**Re-review verdict: RESOLVED.** This is the best-executed of the four repairs and I could not break it.

### 4.1 The four terminal statements are separated by rule, not by convention

`decision-criteria.md` §6.1 states the governing rule and derives two enforceable prohibitions from `alternatives.md` §9. §4A.4 states the four parts a pack must not collapse. Matrix §5 adds **Step 7a**, positioned immediately before the terminal sentence is written — the boundary where the review found the caveats being discarded. §4A.4 and §6.1 both state the availability honestly: steps 1–2 almost always, step 3 on 28 criteria, **step 4 on exactly one axis** (DC-D-108).

| Statement the brief requires distinguished | Where it now lives | Verified |
|---|---|---|
| Power Platform exclusion, and at what scope | §6.2 classes 5 / 6 / 7, keyed to `Xp` / `Xr` / `Xe` / `Xc` | ✅ |
| candidate alternatives | §6.2 class 8; `alternatives.md` §5.1 relabelled *"Evidence (that these classes come into scope)"* | ✅ |
| comparator evidence status | §4A.1's default; `COMPARATOR EVIDENCE ABSENT` present in all three decision files | ✅ |
| actual evidence-backed preference, if any | §6.2 class 9, scoped to DC-D-108 alone, with the Early-Access caveat on the second comparator | ✅ |

### 4.2 Residual comparative language — exhaustive search

I searched all four files for `PREFERRED`, `BETTER`, `CHEAPER`, `FASTER`, `BEST`, *more scalable*, *more reliable*, *more productive*, *superior*, *outperform*, and classified every hit.

| Class of hit | Count | Verdict |
|---|---|---|
| State names (`ORDER PREFERRED`, `CORPORATE NETWORK PREFERRED`) | 4 | not claims |
| Repair notes naming a retired label in order to retire it | 6 | correct — the retirement must be legible |
| Matrix §7's before/after table rows | 8 | correct — the audit trail of the rename |
| The prohibition itself (§6.1 rule 1, §4A.3, `alternatives.md` §2.2) | 5 | correct |
| Evidence-quality adjectives (*"best-evidenced"*, *"best-documented composition"*) | 6 | claims about the corpus, not about a class's fitness |
| **Surviving comparative recommendation about an unevaluated class** | **0** | — |

The four retired labels — `CUSTOM DEVELOPMENT PREFERRED`, `EXISTING ENTERPRISE PLATFORM PREFERRED`, `BUY — PACKAGED PRODUCT OR SERVICE`, `ANOTHER LOW-CODE PLATFORM SHOULD BE EVALUATED` — survive **only** inside §6.3's retirement table and matrix §7's before/after table. The two drifted labels the review found (`POWER PLATFORM POOR FIT`, `POWER PLATFORM IS ECONOMICALLY UNATTRACTIVE`) survive only in repair notes. Verified by locating every occurrence.

Two soft residuals, both pre-existing and neither an outcome claim, recorded as **R-11** (LOW): `alternatives.md` ALT-008's *"ALT-009 is cheaper than a platform change"* is an uncited cost comparison, and ALT-004's *"the dominant and often best composition"* is a shape claim cited to `architecture-patterns.md` AP-06/AP-03.

### 4.3 Rejection was not softened

Tested directly, because a rename in one direction is the obvious way to weaken rejection accidentally.

- §6.2 now contains **class 5 `POWER PLATFORM — POOR FIT`**, an explicit rejection class the pre-repair §6 did not contain at all, anchored to `platform-suitability.md` §1's own `POOR`.
- T-07 and T-13 emit class 5. T-13 still rests on four independent `Xp` exits plus an `Xe`, and I verified the arithmetic: DC-D-020, DC-D-009, DC-D-016, DC-D-012 are all `Xp`; DC-D-010 is `Xe`.
- T-14 emits class 7 on `Xe` exits at DC-D-010, DC-D-093, DC-D-092 — all three genuinely `Xe` in the register.
- T-12 emits class 6 on DC-D-036's `Xr` and carries `INCUMBENT FIT UNEVALUATED` explicitly.
- Power Platform is rejected, displaced or blocked in **12 of 16** scenarios. I re-derived the list from the scenario outcomes rather than from §7's table and reached the same twelve.

**No scenario converts exclusion into preference.** Scenarios 7–9 of the brief:

| Brief scenario | Terminal | Comparative claim? |
|---|---|---|
| 7 — incumbent enterprise platform ownership (T-12) | class 6 → class 8: ALT-007, ALT-001, ALT-011, `INCUMBENT FIT UNEVALUATED`, per-requirement gap analysis | none. NB-06's `INF` status stated |
| 8 — custom application case (T-13) | class 5 → class 8: ALT-005, described as *"scope narrowing, not evaluation"* | none |
| 9 — economically unattractive (T-14) | class 7 → class 8: six candidates, *"none priced"* | none — *"It states nothing whatever about what the others cost"* |

---

## 5. H-03 — Agent / conversational requirements

**Re-review verdict: RESOLVED for coverage, blocking behaviour and evidence integrity. The residual research gap is correctly preserved and escalated, not closed.**

### 5.1 Coverage

| Requirement of the brief | Where it lands | Verified |
|---|---|---|
| Users coverage | `DC-D-116`, Users and experience domain, four states plus `UNKNOWN`, matrix row §2.2 | ✅ |
| Automation coverage where appropriate | `DC-D-116` links DC-D-052 (idempotency of the actor's writes) and DC-D-048's shape question; an autonomous-agent *modality* entry was **rejected as evidence-absent** in the §3.5 ledger, on `automation-architecture.md` U-14's own statement | ✅ — the refusal is the correct call |
| governance implications | tenant inventory, managed-environment sharing with editor/viewer granularity, default-environment policy, ACP virtual-connector non-coverage, GOV-U-06 preview gap | ✅ |
| security implications | Graph-connector guest-access bypass, per-workload design-time enforcement, Key Vault consumability, `security.md` §9 re-verify flag; **AP-D-068** added | ✅ |
| operations implications | no Copilot Studio maker monitoring page, admin Monitor coverage public preview, **agent conversation runtime excluded from self-service DR** | ✅ |
| economics uncertainty | `UNKNOWN` preserved; consumption *"dependent on the complexity of the task"*; dated removal of the bundled allocation; monthly peak enforcement; instruction is a **pilot**, not an estimate | ✅ |
| decision-blocking unknowns | `B*` on commercial and governance model at `TASK-COMPLETING AGENT`+, plus the modality question at `AUTONOMOUS AGENT`; §5.2's unconditional set stays exactly 28 | ✅ |

The DC-D-113 precedent the review named is applied consistently: `LOW` confidence, evidence base stated honestly, `V` flag, and a block on the part the corpus cannot answer. §8.5 records the original error in its own words (*"Every one of those statements is true, and none of them justified the omission"*) and **Local criteria deliberately not carried: 0** is now true.

### 5.2 No fabricated capability, economics, limits or architecture

This was the specific risk the brief named, so I read every asserted fact against the canonical file it cites rather than checking that the id resolves.

| DC-D-116 / AP-D-068 claim | Canonical source | Present verbatim? |
|---|---|---|
| *"view and govern all apps, flows, and **agents** created across your tenant"* | `governance.md` GOV-16 (G-09) | ✅ |
| *"prevent **agents**, apps, and flows from calling any service"* | `governance.md` GOV-03 (G-03) | ✅ |
| *"**Virtual connectors**: ACP doesn't support virtual connectors and won't support them in the future"* | `security.md` SEC-24 (S-29) | ✅ |
| virtual connectors *"evolving into their own dedicated governance rules"* | `governance.md` GOV-11b (G-13, G-17) | ✅ |
| *"might access the information in these items **even if you block guest access**"* | `security.md` SEC-04 (S-25) | ✅ |
| design-time enforcement rolling out Power Automate → Copilot Studio → Power Apps; runtime-only until then | `security.md` SEC-24 (S-29) | ✅ |
| secrets consumable by *"cloud flows, Copilot Studio agents and custom connectors only"* | `security.md` SEC-07/SEC-06 (S-28) | ✅ |
| *Block unmanaged customizations* breaks **Copilot Studio agent publishing**; *"Either forgo that control or forgo those features"* | `alm-devops.md` ALM-15, §4 row 15 | ✅ |
| *"Power Automate and Copilot Studio don't have a monitoring page in their respective maker portals"*; agent coverage public preview | `operations-support.md` OP-06 (O-08) | ✅ |
| *"Copilot Studio conversation runtime requests fail until Microsoft restores the service in the primary region"* | `operations-support.md` OP-19 (O-19); `performance-scale.md` P-27 | ✅ |
| *"250,000"* per 24 h for *"Copilot Studio base and add-on"* | `automation-architecture.md` AT2-03 (V-01, V-02) | ✅ |
| Copilot Credits at $0.01; *"dependent on the complexity of the task"*; AI Builder 5,000 removed 2026-11-01; *"Purchase capacity for the peak utilization monthly period"* | `licensing-cost.md` LC-15 (L-03, L-04, L-05) | ✅ |
| agent authentication and channel controls *"preview; not researched here"* | `governance.md` GOV-U-06 | ✅ |
| *"cannot answer 'should this be an agent instead of a flow?'"*; *"This deferral has no owner"* | `automation-architecture.md` U-14, §12 | ✅ |
| no fit assessment exists: `platform-suitability.md` / `application-architecture.md` carry zero mentions of the surface | grep both files | ✅ — 0 hits for *copilot studio* / *agent* / *agentic* in `platform-suitability.md`; the three `Copilot` hits in `application-architecture.md` are a canvas control and Copilot Service workspace, not an agent surface |

**Fabrication check: nothing found.** No capacity envelope, no latency figure, no accuracy claim, no cost model, no architecture pattern and no fit verdict is synthesised. The criterion states the request bucket is *"a licensing meter, not a performance envelope"* and that **no throughput, latency, concurrency or accuracy figure exists**. `AUTONOMOUS AGENT` is declared unanswerable from this corpus with the unowned deferral quoted. AP-D-068's confidence note records that GOV-U-06 makes the entry *"incomplete by construction"* for the surface. AP-D-068 carries two real `Exceptions`, so it is context-conditional rather than a constraint — correct under §2's own test.

The one place a comparator could have been invented — *"which class does agents better"* — is instead recorded as the corpus's one **total** rather than asymmetric gap (`alternatives.md` §6 item 9): *"no class — including ALT-004 — can be assessed for fit"*.

### 5.3 The block is real

T-16 terminates at `DECISION BLOCKED — MORE EVIDENCE REQUIRED` on three separable, separately closable grounds, each anchored in a quoted MS statement, with the outcome each resolution would produce. Its sharpest sentence is the one that makes the model safe: *"a `—` on DC-D-018 means the corpus looked and found no exit; a `—` on DC-D-116 means the corpus **never looked**."* That distinction is not encoded in the taxonomy's five classes — a `—` is a `—` — but it is stated in the criterion, in the matrix row and in the scenario, which is the honest handling available without inventing a sixth class. Recorded as **R-12** (LOW) because a pack reading only the register cannot see it.

---

## 6. H-04 — Alternative evaluation asymmetry

**Re-review verdict: PARTIALLY RESOLVED, and this is the correct outcome.** The finding asked for two things — encode the evidence that exists, mark the absence where it does not — and both were done without manufacturing symmetry.

### 6.1 The four states the brief requires distinguished

| State | Instrument | Verified |
|---|---|---|
| evidence-backed alternative **constraints** | §4A.2 `CONSTRAINED` / `CAUTION` rows on ALT-005 and ALT-006 | ✅ |
| evidence-backed alternative **exclusions** | §4A.2 `UNAVAILABLE` rows (DC-D-006, 070, 073, 104, 110) — *"unavailable, not merely expensive"* | ✅ |
| **candidate** alternatives | §4A.2 `CANDIDATE`; `alternatives.md` §5.1 relabelled as candidate generation | ✅ |
| **missing comparator evidence** | `COMPARATOR EVIDENCE ABSENT`, §4A.1, stated as the **default on every criterion** | ✅ |

**Mechanically verified both directions:** the register carries exactly **28** `G` flags; §4A.2 carries **42 rows over exactly those 28 distinct criteria**; no `G` criterion lacks a row and no row belongs to a non-`G` criterion. The 88 / 28 split in §4A.1, §9 item 5a, §11, matrix §1 and matrix §9 is arithmetically correct against 116.

`COMPARATOR EVIDENCE ABSENT` (or an explicit equivalent) is present in `decision-criteria.md`, `anti-patterns.md` and `decision-intelligence-matrix.md`, and the matrix's Alternatives column carries the warning in its own legend. Where the absence is total rather than default, it says so absolutely — DC-D-116's *"`COMPARATOR EVIDENCE ABSENT` … and here it is absolute rather than default"*.

### 6.2 No fake symmetry

The specific risk the brief named. Spot-checked the load-bearing §4A.2 rows against canonical text:

| §4A.2 claim | Source | Verdict |
|---|---|---|
| *"unavailable, not merely expensive"* gate | `architecture-patterns.md` §13 row 2 | ✅ documented, quoted |
| *"Hybrid architecture required + no pro-dev/enterprise platform capability available → POOR FIT"* | `architecture-patterns.md` §13 row 7 | ✅ |
| ALT-006 has the **identical** 500-action/8-nesting ceiling; *"'Move to Logic Apps' does not relieve it"* | `automation-architecture.md` §8.2 | ✅ — a limit *on the alternative*, not a claim about Power Platform |
| ALT-005's 230-second maximum HTTP response on every plan | `automation-architecture.md` §8.3 | ✅ |
| event service *"guarantees neither ordering nor exactly-once"*; streaming service *"no dead-lettering"* | `automation-architecture.md` §8.4 | ✅ |
| broker/streaming capacity for two of three services **never sized** → `UNKNOWN` | `automation-architecture.md` U-13; `integration-architecture.md` U-03 | ✅ preserved as `UNKNOWN` |
| DC-D-110 `FULL ENGINEERING CAPABILITY` → **POSITIVE** for ALT-005/006 | `alternatives.md` ALT-005 | ✅ — recorded precisely because refusing a signal pointing *toward* an alternative would itself be bias |
| DC-D-100: *"Custom will recover in time"* is exactly as unevidenced as the platform claim | manifest NB-07; `automation-architecture.md` §8.7, §3.B row 19 | ✅ symmetric |

Every row is a documented limit, a documented unavailability, a documented absent capability, an explicit `UNKNOWN`, or the single documented positive. **No row asserts that any class is faster, cheaper, more scalable, more productive or more reliable than any other.** §4A.3 states this and I could not falsify it. No comparative TCO, benchmark, incumbent evaluation or comparator-low-code claim was invented for custom development, Azure/cloud-native, incumbent platforms, other low-code platforms or packaged products.

The residual — that no comparative evaluation exists — is unchanged, correctly attributed to upstream research commissions (`alternatives.md` §6 items 1, 2, 3, 5, 8), and now visible in the output rather than only in an internal caveat. That is the right shape for a finding the corpus cannot close.

---

## 7. Regression re-tests on the MEDIUM findings

| Finding | Repair claim | Re-review verdict |
|---|---|---|
| **M-01** service-limit volatility | RESOLVED — unimplemented mitigation withdrawn; 20-criterion register added | **RESOLVED.** §7.2 lists exactly 20 ids; matrix §4's service-limit group lists 17, and the other three (DC-D-039, 051, 116) have their own rows above it — 17 + 3 = 20, coherent. The two excluded false positives are named. §7.3's rule (*encode the boundary shape, not the number*) is the right inheritance rule, and §2.3's property that **no published figure is a state name** I re-verified across all 116 state lists — the only numerals are the population bands and DC-D-035's `2–5 STREAMS`. Residual `ms.date` gap is recorded, not hidden. One count slip: **R-06** |
| **M-02** composed disqualifiers | RESOLVED — 12 in all three homes | **PARTIALLY RESOLVED.** The count is right: matrix §3 carries 8 + 4 = 12, AP-D-059 carries 8 + 4 = 12, §2.4 and §11 say 12. Both new rows (Governance, ALM) are evidenced and I traced them: `governance.md` G-03, `operations-support.md` O-05/O-10, `alm-devops.md` ALM-14 for the citizen row; `alm-devops.md` ALM-06/17/23, §4 rows 3 and 11, `application-architecture.md` AA-06 for the ALM row. Both compositions are marked `INF`, matching AP-D-059's origin. **But 18 of 24 `Xc` criteria are in none of the 12 rows** — see R-01(d). Also **R-08**: the same two rows list three criteria in AP-D-059 and four in matrix §3 |
| **M-03 / M-04** duplicate clusters | PARTIALLY RESOLVED by design — binding elicitation rule instead of merging | **ACCEPTED as a defensible design choice.** §3.2 states, per cluster, the one fact to elicit, which member owns which dimension, and a tie-break (*"DC-D-023 is authoritative on volume and DC-D-088 on depth"*). The trade is recorded so a re-reviewer can disagree; I do not, because merging would delete ids three peer files cite and the review rated both findings non-gate-blocking. The elicitation rule does what a question bank needs |
| **M-05** unanchored ordinals | RESOLVED | **RESOLVED.** All three anchored relatively with no invented threshold: DC-D-024 against purchased entitlement and the redesign trigger, DC-D-025 against the content-throughput window and payload ceilings, DC-D-096 against the option's own TCO — and `DOMINANT` now carries a decision consequence (evaluate as ALT-006, not ALT-009). Each anchor's basis is stated, including *why* an absolute anchor would be invention |
| **M-06** DC-D-055 comparative claim | RESOLVED | **PARTIALLY RESOLVED — the matrix row was not repaired.** See **R-03** (MEDIUM). The criterion body is fixed correctly and thoroughly; the matrix row the review explicitly named still carries the superlative |
| **M-07** outcome vocabulary | RESOLVED — closed set of 12 | **PARTIALLY RESOLVED.** The set is defined once, is genuinely closed on paper, contains the two classes the other files were emitting undefined (class 5 `POOR FIT`, class 7 `ECONOMICALLY UNATTRACTIVE OR INFEASIBLE`), and AP-D-003/AP-D-035/AP-D-059/AP-D-061 now name the class **and its number** — I read all four. **But the matrix emits two labels outside the set and the set has no class for a non-exclusion alternative outcome** — see **R-02** (MEDIUM, gate-blocking) |
| **M-08** six constraints | RESOLVED | **RESOLVED.** `Classification` now takes three values with stated enforcement strength. Recounted from the entry blocks: **61 `ANTI-PATTERN` · 3 `GATE` (AP-D-013, 026, 059) · 4 `CONSTRAINT` (AP-D-031, 044, 051, 067) = 68**, matching §2's published split. All six the review named are reclassified, plus AP-D-013 which §8 had already called a gate. §5's header carries the legend. One stray artefact: **R-07** |
| **M-09** AP-D-004 | RESOLVED by re-scoping | **RESOLVED.** Retained, retitled *(portfolio altitude)*, classification carries *"portfolio altitude, explicitly outside the engagement-altitude set"*, and §8 instructs a pack not to surface it as an engagement finding. Re-scoping rather than merging is defensible: the estate-level finding is real and MS-evidenced, and the entry records that its mechanism decomposes without residue |
| **M-10** agent anti-pattern | RESOLVED | **RESOLVED.** AP-D-068 added with all nine contract fields, three MS-quoted mechanisms, two real exceptions, and an honest incompleteness note. The §3.5 ledger, which previously did not mention agents at all, now carries four candidates — one accepted, two merged, **one rejected as evidence-absent** on `automation-architecture.md` U-14's own statement. The refusal is the strongest signal here |
| **M-11** UX detection | RESOLVED with a corrected finding | **RESOLVED, and this is the most honest repair in the set.** §3.11b re-tests `application-architecture.md` AP-17…AP-35 **individually**, quoting each by its own id and summary. I verified the verdict arithmetic: 9 MERGED + 5 CONFIRMED HOME + 5 REJECTED = 19, matching the published split, and the §3.12 totals absorb them correctly (124 candidates = 101 + 4 + 19; 37 merged/confirmed = 21 + 2 + 14; 25 rejected = 20 + 5). The conclusion — *the thin UX coverage was correct, and what was missing was the mapping* — is better than manufacturing entries. The note recording that a first draft was written from plausible-sounding names and discarded is exactly the disclosure a re-reviewer needs. One imprecision: **R-13** |
| **L-01 … L-07** | RESOLVED | **RESOLVED, all seven.** T-05's `AP-D-053` → `AP-D-015` with DC-D-053 named; T-10's `DC-D-047` → `DC-D-001` with AP-D-047 named; both state the original error and why it was silent. `IA-U-14` / `IA-C-01` now name both forms, with a §1 citation-form note — and this is why my mechanical lineage pass found **0** unresolved where the review found 2. AP-D-052 re-anchored to `alm-devops.md` with the four levels named and the upstream defect recorded not repaired. Ordering note added. §9 item 7a records the glossary prerequisite in the strongest available terms (*"this material is not usable until it is written"*). §3.12's footnote now states that the table does not balance and why |

---

## 8. Mechanical validation (independent)

Everything in this section was computed from the four files. Nothing was taken from the repair report.

| Check                                                                             | Result                                                                  |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Duplicate `DC-D-*` definitions                                                    | **0** (116 defined)                                                     |
| Duplicate `AP-D-*` definitions                                                    | **0** (68 defined)                                                      |
| Duplicate `ALT-*` definitions                                                     | **0** (11 defined: ALT-001 … ALT-011)                                   |
| Dangling `DC-D-*` references, all four files                                      | **0**                                                                   |
| Dangling `AP-D-*` references                                                      | **0**                                                                   |
| Dangling `ALT-*` references                                                       | **0** (`ALT-00X` in matrix §7 is an explicit placeholder)               |
| §3.1 register: exactly one row per criterion, ids == body ids as sets             | ✅ 116                                                                   |
| Exit-class tag on every criterion body                                            | ✅ 116                                                                   |
| **body tag == register flag == matrix cell class, all 116**                       | ✅ 0 mismatches                                                          |
| Exit-class distribution vs all published homes                                    | ✅ `Xp` 15 · `Xr` 34 · `Xe` 5 · `Xc` 24 · `—` 38 · direct 54 · total 116 |
| §3 domain table, all 96 cells + totals row                                        | ✅ exact                                                                 |
| Blocking: `B` == 28 · `B*` == 3 · §5.2 lists exactly the 28                       | ✅                                                                       |
| Alternative-side: `G` == 28 · §4A.2 == same 28, both directions                   | ✅                                                                       |
| §4A.1's 88 / 28 split against 116                                                 | ✅                                                                       |
| Composed disqualifiers: matrix §3 == 12 · AP-D-059 == 12 · §2.4 == 12 · §11 == 12 | ✅                                                                       |
| **`Xc` criteria named in a matrix §3 row**                                        | ❌ **6 of 24** — R-01(d)                                                 |
| Anti-pattern classifications: 61 / 3 / 4 == 68 entries                            | ✅                                                                       |
| Anti-pattern register rows == 68, distinct                                        | ✅                                                                       |
| All nine contract fields present on every anti-pattern                            | ✅ 68                                                                    |
| Criterion → ≥1 anti-pattern · ≥1 alternative · file-qualified `Lineage`           | ✅ 116 / 116 / 116                                                       |
| Every anti-pattern reachable from ≥1 criterion · every alternative reachable      | ✅ 68 · ✅ 11                                                             |
| **Matrix anti-pattern column == criterion `Related anti-patterns`**               | ⚠️ **115 of 116** — DC-D-055 diverges (R-03)                            |
| Matrix alternatives column == criterion `Related alternatives`                    | ⚠️ 114 of 116 — DC-D-002, DC-D-116 (R-09)                               |
| Canonical id references resolved                                                  | ✅ **3,066 occurrences / 1,520 distinct pairs, 0 unresolved**            |
| Retired preference labels confined to repair notes                                | ✅                                                                       |
| `COMPARATOR EVIDENCE ABSENT` present in all three decision files                  | ✅                                                                       |
| Adversarial scenarios present                                                     | ✅ 16                                                                    |
| Criterion `Confidence` distribution vs §9 item 8                                  | ❌ actual 68 / 46 / 2 vs published 57 / 56 / 3 — R-04                    |
| `V` flags in register vs §7.1's "ten"                                             | ❌ 11 vs 10 — R-06                                                       |
| Matrix §8.2's reference counts                                                    | ❌ AP-D-059 7–8 not 11; ALT-008 10–13 not 7 — R-05                       |
| Matrix exit cells carrying a class marker and no content                          | ❌ 10 (5 `Xr`, 5 `Xc`) — R-01(c)                                         |

---

## 9. Adversarial regression

All sixteen re-run against the repaired files, including the twelve the brief names. I ran each against the criteria, anti-pattern and alternatives files first and compared with the matrix's stated conclusion afterwards.

| # | Brief scenario | Matrix test | Terminal produced | Correct? |
|---|---|---|---|---|
| 1 | simple departmental app | T-01 | class 1 `STRONG FIT` **or** `COLLABORATION-PLATFORM NATIVE` + graduation trigger | direction ✅ · **label off the closed set — R-02** |
| 2 | Excel replacement | T-02 | class 2 `FIT WITH CONSTRAINTS` | ✅ substantively — **and it contradicts the `Xr` mapping rule, R-01(b)** |
| 3 | high-volume integration | T-05 | class 3 `+ CLOUD-NATIVE HYBRID`, conditional on DC-D-070/110; else `single platform + a tripwire` or the responsibility to ALT-007 | direction ✅ · fallback label off-set — R-02 |
| 4 | strict low-latency | T-07 | class 5 `POOR FIT` → class 8, three candidates, none evaluated | ✅ |
| 5 | citizen app → enterprise-critical | T-10 | `DECISION BLOCKED` on DC-D-006 → composed row 3 fires **explicitly** → class 8, migration not remediation | direction ✅ · **class 8 emitted unaccompanied, against its own definition — R-02** |
| 6 | mission-critical | T-09 | `DECISION BLOCKED` on DC-D-100/091 → class 2 restated, or class 6 → class 8 with NB-07 stated on the candidates too | ✅ |
| 7 | incumbent enterprise platform ownership | T-12 | class 6 → class 8: ALT-007/001/011 with `INCUMBENT FIT UNEVALUATED`; or class 4 where authority stays | ✅ **no preference asserted** |
| 8 | custom application case | T-13 | class 5 → class 8: ALT-005, *"scope narrowing, not evaluation"*; four `Xp` + one `Xe` | ✅ **no preference asserted** |
| 9 | economically unattractive | T-14 | class 7 → class 8: six candidates, *"none priced"*; *"It states nothing whatever about what the others cost"* | ✅ **no preference asserted** |
| 10 | insufficient evidence | T-15 | class 12 `DECISION BLOCKED` + the four highest-value questions and what each resolution would produce | ✅ |
| 11 | conversational assistant over enterprise data | T-16 | class 12 on three separable grounds; *"no class evaluable"* | ✅ |
| 12 | task-completing agent with sensitive data | T-16 + DC-D-116 `TASK-COMPLETING AGENT` + AP-D-068 | class 12; guest-access bypass named as the gating question | ✅ |

**All six required outcome shapes are producible:** Power Platform viable (T-01, T-02 direction), viable with constraints (T-02, T-06), partial/hybrid responsibility (T-05, T-09, T-11, T-12), Power Platform excluded (T-07, T-13), alternatives requiring evaluation (class 8, reached in seven scenarios), decision blocked pending evidence (T-03, T-04, T-08, T-09, T-15, T-16).

**The critical test the brief names — `Power Platform excluded` must not become `Alternative X preferred` without comparative evidence — passes on every scenario.** Every exclusion terminal is followed by class 8 with `COMPARATIVE FIT UNEVALUATED`, and T-12 additionally carries `INCUMBENT FIT UNEVALUATED`. T-04's note that *"the replacement's adequacy is unevidenced"* and T-09's note that NB-07 applies to the candidates too were **added**, not removed — I verified both are present.

**Two regressions the scenarios expose rather than cause.** T-02 is the counter-example that falsifies matrix §1's `Xr` mapping rule (R-01(b)). T-01, T-05 and T-10 are the three places where the closed outcome set cannot express the answer the model correctly reaches (R-02). In both cases the *scenarios* are right and the *rules* are wrong — which is the dangerous direction, because a pack implements the rules.

---

## 10. Evidence integrity

**PASS.** This is the dimension where the repair is strongest, and it improved on an already-strong baseline.

| Test | Result |
|---|---|
| Canonical id references resolved, all four files | **3,066 occurrences / 1,520 distinct (file, id) pairs — 0 unresolved** |
| The review's two lineage failures (`IA-U-14`, `IA-C-01`) | **now resolve** — both forms named, with a §1 citation-form note stating that this is the manifest's reservation *recorded, not repaired* |
| Canonical identifiers renamed | **none** — manifest §4 respected; `DC-D-`, `AP-D-`, `ALT-` remain collision-free |
| New criterion (DC-D-116) — every asserted fact | **15 of 15 verified verbatim** against the cited canonical file (§5.2) |
| New anti-pattern (AP-D-068) — every mechanism | **3 of 3 verified verbatim** |
| New composed rows (2) | both traced to MS-stated facts; composition marked `INF`, matching AP-D-059's origin |
| `UNKNOWN` preserved | ✅ agent economics, capacity, latency, concurrency, accuracy; broker/streaming sizing (U-13, U-03); comparator portability; incumbent fit; polling intervals; concurrency and amplification figures; GOV-U-06 governance maturity |
| `CONFLICTED` preserved | ✅ NB-02 still open, still 20×, still re-verified as live, still barred from encoding, DC-D-039 still decision-blocking |
| `VOLATILE VALUE` preserved | ✅ **improved** — §7.2's 20-criterion service-limit register closes the review's M-01 gap; §7.3 states the inheritance rule |
| `INF` preserved | ✅ NB-06 carried with the *"not vendor-endorsed"* warning into DC-D-036, DC-D-111, ALT-007 and T-12; AP-D-059's composition marked `INF`; DC-D-116's `INF` scoped to *framing only* |
| comparator evidence absence preserved | ✅ 88 criteria by default, absolutely on DC-D-116, and `alternatives.md` §6 item 9 records it as the corpus's one **total** rather than asymmetric gap |
| A repaired field silently upgrading one of these states into fact | **none found** |
| Invented threshold | **none found.** No published figure is a state name — re-verified across all 116 state lists |
| Areas 1–12 modified | **no.** Duplicate `licensing-cost.md DC-14` and the `integration-architecture.md §15.8` dangling citation are both still recorded and not repaired, correctly |

The repair also declined the four things it would have been easiest to fabricate — an agent fit verdict, an agent capacity envelope, a comparative TCO, and comparator low-code capability beyond the deployment-model axis — and says so explicitly in §4 of the repair report. I looked for each and found none.

---

## 11. Findings

### R-01 — HIGH · CONTRADICTION / TAXONOMY · gate-blocking

**Finding.** H-01 is resolved as a *consistency* problem and unresolved as a *classification* problem. The taxonomy is named and its three representations agree exactly on all 116 criteria, but (a) four criteria are classed `Xr` on fields that name nothing leaving the platform, (b) the `Xr` → outcome-class mapping produces a false exclusion for that subset and is contradicted by the matrix's own T-02, (c) ten matrix exit cells assert a class and carry no content, (d) 18 of the 24 `Xc` criteria are absent from the register §2.5 declares to be their exit's home, and (e) one pre-repair count survives in the regenerated file.

**Affected.** `decision-criteria.md` §2.5 (class definitions and tests), §3 domain table, §3.1 register, §9 item 5, §11; DC-D-025, DC-D-030, DC-D-032, DC-D-088 (and DC-D-046, ambiguous); the 18 `Xc` criteria listed in §3.2(d); `decision-intelligence-matrix.md` §1 (`Xr` mapping rule and legend), §2 rows for DC-D-011/022/025/030/032/037/038/046/080/088, §3, §9; `decision-criteria.md` §6.2 classes 3, 4, 6.

**Evidence.** §3.2 above. Reproducible: extract the 116 `PP negative/exit` fields; apply §2.5's two tests literally; intersect the `Xc` set with the criterion ids named in matrix §3's twelve rows; read matrix §1's mapping sentence against T-02's criteria list and terminal.

**Why it matters.** The review's stated reason for raising H-01 was that *"a pack authoring signals or a decision tree from §3.1 rather than from 115 prose entries loses twelve documented exits"*. The repair fixed the loss and introduced the mirror-image defect: the register now carries four exits that are not exits and 18 combination-pointers that resolve to nothing, and the rule a pack would implement to turn an `Xr` into an outcome emits `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` where the corpus's own best-evidenced scenario emits `FIT WITH CONSTRAINTS`. The direction of the error is *anti*-platform, not pro-, which does not make it safe: a false exclusion on routine data findings (concurrent editing, attachment volume, retention, records per path) is a wrong architecture recommendation on common engagements. And the 18 undetectable `Xc` exits sit exactly where the model claims its greatest advantage over a score.

**Required correction.** Re-apply §2.5's `Xr` test to the four (five, with DC-D-046) criteria whose remedy is entirely in-platform; either return them to `—` and republish the derived counts (direct exits 50, dashes 42) or split `Xr` into *leaves-the-platform* and *in-platform-pattern-unavailable* sub-classes with distinct outcome mappings. Correct matrix §1's mapping sentence and §6.2 class 6's trigger so an in-platform pattern change routes to class 2, and align them with T-02. Give every `[Xr]` and `[Xc]` matrix cell the content its class test requires. Reconcile the 24 `Xc` flags against the 12-row composed register — either add the missing rows or downgrade the criteria whose combination is not registered. Fix matrix §9's *"79 dashes"*.

### R-02 — MEDIUM · SEMANTIC DRIFT / CLOSED-SET GAP · **gate-blocking**

**Finding.** §6.2 declares the twelve-class outcome set closed and states that the other two files *"emit from this list and no other"*. Two matrix scenarios emit labels outside it, and the set has no class for the case where an alternative is sufficient and Power Platform is **not** excluded.

**Affected.** `decision-criteria.md` §6.2 (class 8's definition); `decision-intelligence-matrix.md` T-01 (`COLLABORATION-PLATFORM NATIVE`), T-05 (`single platform + a tripwire`), T-10 (class 8 emitted unaccompanied), §2.8 header.

**Evidence.** T-01: *"`POWER PLATFORM — STRONG FIT` **or** `COLLABORATION-PLATFORM NATIVE`"*. T-05: *"If not, the outcome is `single platform + a tripwire`"*. Neither string appears in §6.2. §6.2 class 8 is defined as *"The terminal form for classes 5, 6 and 7"*, so it cannot carry a non-exclusion — yet T-10's terminal is class 8 alone, correctly, because its composed row concludes *"cannot be brought to the required class in place → migration, not remediation"*, which is not *"the option is unavailable"* and therefore does not trigger class 5. `alternatives.md` ALT-003 is *"Collaboration-platform native capability"* and is a first-class class with `HIGH` confidence, but has no outcome class of its own.

**Why it matters.** The review's reason for rating M-07 gate-blocking was that *"the terminal set of a decision tree must be closed and consistent"*. It still is not. The gap is not cosmetic: a pack implementing §6.2 literally must either drop T-01's alternative branch — which systematically biases toward Power Platform on the **most common departmental engagement shape**, the one the corpus is most explicit about (*over-engineering it is a real cost*) — or invent a class the research does not define. T-10 is the brief's scenario 5 and the corpus's own *"most common real engagement in this domain"*; its terminal is unreachable under the class definitions as written.

**Required correction.** Add the missing classes: an *alternative-sufficient, platform not excluded* class (ALT-003 / ALT-001 / ALT-011 direction with `COMPARATIVE FIT UNEVALUATED`), and a *cannot-be-remediated-in-place → migration* class for the composed citizen-development row. Relax class 8's antecedent to include them. Map T-01's and T-05's labels onto the set or define them in it. Then re-run the mechanical check the repair's own §5.1 table implies but did not perform: **every emitted outcome string appears in §6.2**.

### R-03 — MEDIUM · CONTRADICTION / CROSS-FILE · not gate-blocking

**Finding.** M-06 is reported RESOLVED but only the criterion body was repaired. The matrix row the review explicitly named still carries the comparative superlative, still lacks the DC-D-111 precondition, and now diverges from the criterion on anti-patterns.

**Affected.** `decision-intelligence-matrix.md` §2.5 row DC-D-055.

**Evidence.** The row's Positive PP signal cell reads: *"Simple to delegated/escalated approval within 30 days — **the platform's strongest documented differentiator here**"*. §4A.3 states that no row asserts a class is better than another; §4A.2's DC-D-055 rows correctly scope the claim to *"the code-first alternatives the corpus examined"* with ALT-007 and ALT-008 `UNKNOWN`; the criterion body's `PP positive` was repaired to *"Not a differentiator against incumbent process engines, which the corpus does not evaluate."* The matrix row was not. The review's M-06 affected list named *"matrix §2.5 row DC-D-055"* explicitly. The repair report's M-06 file list omits `decision-intelligence-matrix.md`.

Separately: the repair added AP-D-027 to DC-D-055's `Related anti-patterns`; the matrix row's anti-pattern cell still reads `AP-D-015`. This is the **only** criterion↔matrix anti-pattern-set divergence in 116 rows — the review had verified *"identical sets on all 115 rows"*, so it is a repair-introduced regression in a previously clean invariant.

**Why it matters.** The matrix is the machine-readable summary; a pack rendering the row emits a comparative claim about classes the corpus does not evaluate, in the one column matrix §1 governs with an explicit phrasing rule. The DC-D-111 precondition — the whole substance of the M-06 repair — is invisible to a matrix reader.

**Required correction.** Scope the row's positive cell as the criterion body does; add the DC-D-111 precondition; add AP-D-027 to the row.

### R-04 — MEDIUM · CONTRADICTION / COUNT · not gate-blocking

**Finding.** `decision-criteria.md` §9 item 8 publishes a confidence distribution of **HIGH 57 · MEDIUM 56 · LOW 3**. Recounted from the 116 `**Confidence:**` fields: **HIGH 68 · MEDIUM 46 · LOW 2** (LOW = DC-D-113, DC-D-116). Every field is a single unqualified token, so there is no compound-value ambiguity. The published triple sums to 116, which is why it reads as plausible.

**Why it matters.** It is a published derived count in the same section whose item 5 was regenerated, and it is wrong by 11 on two of three values. The H-01 re-test asks whether *all* derived counts agree; this one does not. No decision behaviour depends on it, which is why it is MEDIUM rather than HIGH — but the claim *"every derived count was regenerated, not patched"* is falsified by it.

**Required correction.** Recount and republish, and add the confidence distribution to whatever check regenerates the other counts.

### Low findings

**R-05 — Matrix §8.2's reference counts are wrong.** *"`AP-D-059` … Referenced from 11 criteria"* — actual 7 by `Related anti-patterns` field, 8 anywhere in a criterion body. *"`ALT-008` … Reachable from 7 criteria"* — actual 10 by field, 13 anywhere. Reachability itself holds and orphans are genuinely **0**, so the section's conclusion survives; the numbers do not. *Type: SEMANTIC DRIFT.*

**R-06 — The `V` flag count disagrees with the volatility register in three places.** The §3.1 register carries **11** `V` flags (the §7.1 ten plus DC-D-116). §7.1's header says *"Ten criteria"* and its table lists ten. §9 item 4 says *"the ten criteria whose figures are date-sensitive"*. §7.2's DC-D-116 row says *"(already `V` — §7.1)"*, which is false — DC-D-116 is not in §7.1's table. The criterion is not lost (matrix §4 carries its own row), so this is labelling, not coverage. *Type: SEMANTIC DRIFT.*

**R-07 — Stray `Classification` field in `anti-patterns.md` §1.4.** Line 66 carries *"- **Classification:** CONSTRAINT · **Origin:** INF (mechanical inspection of the canonical corpus) · **Confidence:** HIGH"* inside the *lineage defects observed, not repaired* section, belonging to no entry. The file therefore has **69** `**Classification:**` fields for **68** entries. My per-entry count is unaffected (61/3/4), but a checker counting fields rather than entries gets 69. *Type: MECHANICAL.*

**R-08 — The two new composed rows carry different criteria sets in their two homes.** Matrix §3 lists the citizen row as `DC-D-006, 001, 074, 093` and the ALM row as `DC-D-007, 078, 110, 081`; AP-D-059's *"Derived from"* column lists `DC-D-006 × DC-D-001 × DC-D-074` and `DC-D-007 × DC-D-078 × DC-D-110`. Same rule, two triggers. M-02's whole point was that the two homes must not diverge. *Type: CROSS-FILE INCONSISTENCY.*

**R-09 — Two criterion→alternative set divergences between criteria and matrix.** DC-D-002's body names ALT-004; its matrix row does not. DC-D-116's body names ALT-003/004/007/011 *"all `UNKNOWN` on this axis"*; its matrix cell says *"none evaluable"*. The second is a defensible deliberate difference; the first is pre-existing drift. The anti-pattern column was verified identical on 115 of 116 (R-03 is the exception), so this column is the weaker of the two invariants. *Type: SEMANTIC DRIFT.*

**R-10 — Matrix §2.8's header overstates.** *"### 2.8 ALM and delivery (DC-D-076 … 083) — no exit signals evidenced"* while DC-D-080 carries `[Xc]`. The accurate claim, used correctly everywhere else, is *zero **direct** exits*. §2.7 Governance's identical header is accurate (7 dashes, nothing else). *Type: SEMANTIC DRIFT.*

**R-11 — Two soft comparatives survive in `alternatives.md`, both pre-existing.** ALT-008's *"When Power Platform is preferable"* ends *"in which case ALT-009 is cheaper than a platform change"* — an uncited cost comparison between two options, in the direction of Power Platform. ALT-001's *"the dominant and often best composition"* is a shape claim, cited. Neither is an outcome class, so neither breaches §6.1's rule as written; both breach §4A.3's spirit. The `When X is preferable` / `When Power Platform is preferable` field pair is otherwise correctly conditioned throughout — every entry states conditions with a canonical anchor rather than a verdict, and ALT-007's is explicit that fit is *"recorded **per requirement**, not asserted"*. *Type: BIAS (minor, symmetric field structure).*

**R-12 — The taxonomy cannot express "the corpus never looked".** DC-D-116's `—` and DC-D-018's `—` mean different things, and the criterion, the matrix row and T-16 all say so in prose (*"a `—` on DC-D-018 means the corpus looked and found no exit; a `—` on DC-D-116 means the corpus never looked"*). The five-class taxonomy has no marker for it, so a pack reading the register alone cannot distinguish *no exit evidenced* from *no evidence at all*. Not a defect of the repair — inventing a sixth class was not in scope — but a named prerequisite alongside the glossary. *Type: MISSING DISTINCTION.*

**R-13 — Two small imprecisions in otherwise correct repair prose.** §3.11b states that *"DC-D-012, DC-D-013, DC-D-015, DC-D-016, DC-D-018, DC-D-020 carry seven exits between them"*; those six carry six class tags (one of which is `Xc`), and the Users domain's seventh direct exit is DC-D-010's `Xe`. `decision-criteria.md` §9 item 1 states *"Four criteria additionally rest on the external checks"* and names three (DC-D-039, DC-D-108, DC-D-105). Matrix §7 says *"the five scenarios that terminate at `DECISION BLOCKED`"* while matrix §9 says **6** blocked; T-04 also opens with a block. *Type: SEMANTIC DRIFT.*

**R-14 — The repair report's own validation table overstates two checks.** *"Register flag == body tag == classification map, all 116 ✓"* and *"Matrix exit class == criterion body class, all 116 ✓"* are both true and I reproduced them — but the table also claims *"44 checks, 44 PASS, 0 FAIL"* while carrying no check that any emitted outcome string is in §6.2 (R-02), no check that a `Xc` criterion appears in the composed register (R-01(d)), no check of the confidence distribution (R-04), no check of the `V` count (R-06), and no re-check of the criterion↔matrix anti-pattern invariant after AP-D-027 was added (R-03). The checks that were run were run correctly; the suite has holes where the repair's own changes created new invariants. Recorded because a future repair should extend the suite, not re-run it. *Type: PROCESS.*

---

## 12. What the repair got right, stated plainly

Because the verdict below is a FAIL on one finding, the balance is worth recording.

1. **The taxonomy exists and was established before any count moved**, with a written classification test and a written precedence rule — which is what makes R-01 diagnosable at all. A repair that had simply renumbered to 46 would have been undetectable.
2. **Three independently authored representations of 116 rows agree exactly.** That is a strong signal about the care taken, and it is rare.
3. **H-02 is fully resolved and survives an exhaustive adversarial search.** The four preference labels are retired, the retirement is documented, the replacement vocabulary distinguishes exclusion from candidacy from comparator status from preference, and Step 7a makes the check ordered rather than optional. Rejection was not softened — the explicit `POOR FIT` class did not previously exist.
4. **H-03 added a whole requirement class without inventing a single fact.** Fifteen facts, fifteen verified verbatim, and the four things it would have been easiest to fabricate are explicitly declined. The criterion **blocks** rather than guesses, and §8.5 records the original error in the file rather than in a changelog.
5. **H-04 refused to manufacture symmetry** and encoded 28 real alternative-side constraints that were already in the corpus and unused, with `COMPARATOR EVIDENCE ABSENT` as the stated default on the other 88.
6. **M-11's repair corrected the finding rather than complying with it** — nineteen candidates re-tested individually, zero new entries, and an honest conclusion that the thin coverage was right and the missing thing was the mapping. The disclosure that a first draft was written from invented candidate names and discarded is the single most reviewer-useful sentence in the repair report.
7. **Lineage went from 2 unresolved references to 0**, and the fix was to name both forms rather than to pick one and hide the reservation.
8. **M-01's unimplemented mitigation was withdrawn rather than quietly left standing**, and replaced with a register that makes re-verification a trigger.

---

## 13. Required corrections before the gate

| # | Correction | Finding | Gate-blocking? |
|---|---|---|---|
| 1 | Re-apply §2.5's `Xr` test to DC-D-025/030/032/088 (+046); republish direct-exit and dash counts; or split `Xr` by scope with distinct outcome mappings | R-01(a) | **Yes** |
| 2 | Correct matrix §1's `Xr` → outcome mapping and §6.2 class 6's trigger so an in-platform pattern change routes to class 2; align with T-02 | R-01(b) | **Yes** |
| 3 | Give all ten bare `[Xr]` / `[Xc]` matrix cells the content their class test requires | R-01(c) | **Yes** |
| 4 | Reconcile the 24 `Xc` flags against the 12-row composed register — add the missing rows or downgrade the unregistered criteria | R-01(d) | **Yes** |
| 5 | Fix matrix §9's *"79 dashes"* | R-01(e) | **Yes** |
| 6 | Add an *alternative-sufficient, platform not excluded* class and a *migration-not-remediation* class; relax class 8's antecedent; map T-01's and T-05's labels into the set; add a mechanical check that every emitted outcome string is in §6.2 | R-02 | **Yes** |
| 7 | Repair the DC-D-055 matrix row (scope the superlative, add the DC-D-111 precondition, add AP-D-027) | R-03 | No |
| 8 | Recount and republish §9 item 8's confidence distribution | R-04 | No |
| 9 | Reconcile the `V` count across §3.1, §7.1, §7.2 and §9 item 4 | R-06 | No |
| 10 | Fix matrix §8.2's two reference counts | R-05 | No |
| 11 | Remove the stray `Classification` field at `anti-patterns.md` §1.4 | R-07 | No |
| 12 | Align the two new composed rows' criteria sets across matrix §3 and AP-D-059 | R-08 | No |
| 13 | Fix matrix §2.8's header; the §9 item 1 count; the §7-vs-§9 blocked count; §3.11b's "seven exits" | R-10, R-13 | No |
| 14 | Extend the validation suite to cover the invariants the repair created (outcome-string closure, `Xc` → §3 membership, confidence distribution, `V` count, criterion↔matrix AP sets) | R-14 | No |

Corrections 1–6 are the gate. None has been performed by this re-review.

---

## 14. Research follow-ups — unchanged and confirmed

The review's §19 items 1–9 all survive this pass and none was closed by the repair, correctly. Two are worth restating because the repair made them load-bearing:

1. **The agent / Copilot Studio research area** (`alternatives.md` §6 item 9). DC-D-116 and AP-D-068 now hold real evidence and a real block, but no canonical file assesses agent fit in any class, and `automation-architecture.md` U-14's deferral is still **unowned**. Until the commission lands, every `TASK-COMPLETING AGENT` engagement terminates at `DECISION BLOCKED`. That is correct behaviour and a poor answer to give a sponsor twice.
2. **Comparative TCO and comparator low-code capability** (§6 items 1 and 2). §4A.1 now makes `COMPARATOR EVIDENCE ABSENT` a governing default on 88 criteria. The model is honest and, on the question sponsors ask most, silent.

Also unchanged: `licensing-cost.md`'s duplicate `DC-14` and the manifest's incorrect `DUPLICATE CANONICAL IDS: 0`; `integration-architecture.md` §15.8's non-existence; NB-02's live 20× conflict; document generation and templating absent from the entire corpus.

---

## 15. Final verdict

The repair is substantial, largely competent, and honest about its own residuals in a way that made this re-review possible rather than adversarial. Three of four HIGH findings are closed on the evidence. H-02's closure is thorough and survives an exhaustive search for the specific language the brief named. H-03 added a requirement class without inventing a fact and made the model block where it previously would have answered confidently and wrongly. H-04 declined to manufacture symmetry and encoded the twenty-eight real alternative-side constraints that were sitting unused in the corpus. Evidence integrity improved: 3,066 canonical references, zero unresolved, every preserved-state semantic intact, and four separate opportunities to fabricate declined and documented.

H-01 is the one that does not close. The repair named the distinction the review asked it to name and made three representations agree exactly — real work, and the reason its remaining defects are findable. But it then classified four criteria into an exit class on fields that say *"none evidenced"*, mapped that class to outcome classes that emit a false exclusion, emptied ten matrix cells that previously carried information, and pointed twenty-four composed-only flags at a twelve-row register that holds six of them. The counts now agree with each other and not with the criteria they describe. And the outcome set the M-07 repair declared closed is emitting two labels it does not contain, because it has no class for the answer the model correctly reaches on the most common engagement shape there is.

Neither defect makes the material unsafe to read. Both will make the pack built from it wrong in specific, predictable ways — a false `EXCLUDED FOR THIS RESPONSIBILITY` on routine data findings, eighteen undetectable composed exits, and a decision tree that cannot terminate where T-01, T-05 and T-10 terminate. That is the same class of consequence the original review gave for holding the gate, and it holds again.

`BLOCK D RE-REVIEW: FAIL`
`CRITICAL FINDINGS: 0`
`HIGH FINDINGS: 1`
`GATE-BLOCKING MEDIUM FINDINGS: 1`
`EVIDENCE INTEGRITY: PASS`
`DECISION MODEL REGRESSION: FAIL`
`READY FOR BLOCK D GATE: NO`

---

**Not performed, by instruction:** any modification to a Block D file · any repair of the findings above · the Block D gate · canonicalisation · PP pack authoring · any external or new broad research.
