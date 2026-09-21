Review Status: COMPLETE
Reviewer: independent senior enterprise-architecture review (fresh pass)
Review date: **2026-09-03**
Block under review: **D — Decision Intelligence (Areas 13, 14, 15 + Decision Intelligence Matrix)**
Scope: review only. **No Block D file was modified. No pack authoring performed. `library/packs/pp/` untouched.**

# Block D Review

Inputs read in full: `anti-patterns.md` (2,391 lines), `alternatives.md` (796), `decision-criteria.md` (3,438), `decision-intelligence-matrix.md` (598), `canonical-manifest.md`, `source-policy.md`, `research-prompt.md`, `research-areas.md`.
Canonical Areas 1–12 consulted for lineage verification and for the spot-checks recorded in §10.
External research used: **none**. Every claim tested in this review was testable against the canonical corpus or against Block D's own internal consistency. `anti-patterns.md` §6's four external checks (V-D-01…V-D-04) were reviewed as evidence, not re-run.

---

## 1. Review Status

| | |
|---|---|
| Files reviewed | 4 of 4 |
| Criteria examined | 115 of 115 |
| Anti-patterns examined | 67 of 67 |
| Alternative classes examined | 11 of 11 |
| Matrix rows examined | 115 criterion rows + 10 composed disqualifiers + 8 volatility rows |
| Adversarial scenarios independently re-run | 15 of 15 (§13) |
| Mechanical lineage references resolved | **1,582** file-qualified id references across the three files |
| Mechanical lineage failures | **2** (both explained by a recorded manifest reservation — L-02) |
| Internal dangling references (`AP-D-`, `ALT-`, `DC-D-`) | **0** |
| Findings raised | 22 — CRITICAL 0 · HIGH 4 · MEDIUM 11 · LOW 7 |

---

## 2. Overall Confidence

**MEDIUM-HIGH in the evidence layer. MEDIUM in the decision layer. MEDIUM-LOW in the counting and labelling layer.**

The three layers are worth separating because they failed differently.

- **Evidence layer (high).** Lineage integrity is the strongest I have seen in this corpus. 1,582 file-qualified references were resolved mechanically; two failed, and both are the manifest's own recorded artefact-history reservation rather than a Block D error. Spot-checks against `platform-suitability.md` PS-47, `performance-scale.md` PF-17, `data-architecture.md` DA-03, `application-architecture.md` AA-40/AA-46 and `licensing-cost.md` LC-28 found no overstatement, no silent generalisation and — in the DA-03 case, which is the corpus's own trap — correct preservation of a *revised, narrowed* boundary (aggregation, not report size). `UNKNOWN`, `CONFLICTED`, `VOLATILE VALUE` and `INF` semantics are preserved throughout, including where preservation is inconvenient.
- **Decision layer (medium).** The ordered, non-commutative model in `decision-intelligence-matrix.md` §5 is the right shape, and the refusal to score (`decision-criteria.md` §2.4) is correctly argued from evidence rather than from instruction. But the apparatus is **one-sided**: only Power Platform has per-criterion states→signals. Alternatives have triggers and consequences but no per-criterion evaluation, so the model is strong at *"is this in or out of Power Platform"* and weak at *"which of the survivors"* (H-04). Its terminal outputs assert more than the evidence supports (H-02).
- **Counting and labelling layer (medium-low).** The headline arithmetic is wrong in a way that matters downstream. Three files report three different exit-signal counts for the same 115 criteria (36 / 46 / 48 — H-01), and the outcome-class vocabulary is inconsistent across the three files (M-07). These are cheap to fix and expensive to inherit.

---

## 3. Executive Assessment

**Block D does convert canonical architectural research into a coherent, technology-neutral decision-support model. It is not a Power Platform recommendation engine.** I tested that claim hard and it holds:

- 46 of 115 matrix rows carry a substantive exit signal; 69 carry `—`, and the `—` is treated as information rather than as a gap.
- Eleven outcome classes exist, **three of which are not technology decisions at all** (extend the incumbent, process change, do nothing).
- Of my 15 independent scenario re-runs, Power Platform was **rejected or displaced in 6** and **blocked pending evidence in 5**.
- The anti-pattern set carries both failure directions — under-engineering *and* over-engineering — with the over-engineering half explicitly marked as resting on weaker evidence and flagged for a reviewer to attack (`anti-patterns.md` §7 item 2). That is unusual and correct.
- The three classic false-positive traps are avoided. Direct integration is explicitly defended (`AP-D-022` Exceptions: *"the correct answer far more often than architects trained on enterprise integration expect"*), a document/list store is explicitly defended for document-centric work (`AP-D-008` Exceptions), and `AP-D-023` exists as the symmetric counterweight to `AP-D-022`. I found **no anti-pattern that condemns a normal architecture unconditionally**.
- The symmetry rule in `alternatives.md` §2.2 is genuinely enforced. I checked all five forbidden universals against the finished text of all four files; none is asserted. `ALT-004`'s weaknesses field is the longest in that file.

Four things stop this being a PASS.

1. **The model's arithmetic contradicts itself on its own headline finding.** The claim that 36 of 115 criteria carry an exit signal — used in `decision-criteria.md` §2.5 and §9 item 5 to argue that exit asymmetry is evidential rather than constructed — is contradicted by the criteria bodies (48) and by the matrix (46). Twelve criteria carry a written exit and no `X` flag. Several are consequential: *"the platform is not the integration layer for that stream"* (DC-D-036), *"the integration responsibility leaves the platform"* (DC-D-039), *"out of the platform for the coordination"* (DC-D-054), *"the option is infeasible"* (DC-D-092). A pack generated from the register rather than from the bodies silently loses them.
2. **The terminal outputs overstate the evidence on every non-Power-Platform branch.** `CUSTOM DEVELOPMENT PREFERRED` and `EXISTING ENTERPRISE PLATFORM PREFERRED` are preference claims. The corpus holds no comparative TCO, no comparative benchmark and no evaluation of any incumbent — and says so, repeatedly and honestly, in `alternatives.md` §5.3 and §6. The outcome labels are the one place where that honesty does not survive into the user-visible output.
3. **A whole requirement class has no home.** Conversational and agent-shaped requirements are absent from the criteria set. The stated reason (`decision-criteria.md` §8.5) covers only *consumption economics* — but the canonical corpus carries substantive agent evidence in governance, security and operations, none of which is carried forward. The precedent for how to handle exactly this situation already exists in Block D: `DC-D-113` is carried with an empty evidence base and flagged decision-blocking. Agents were dropped instead.
4. **The evaluation apparatus is asymmetric by construction.** Every criterion is expressed as *"what does this state mean for Power Platform"*. That is defensible for a Power Platform pack, but it means the model cannot discriminate among the alternatives it redirects to. This is the same defect T-14 exposed from the cost side, and it is structural rather than evidential.

None of the four produces an unsafe recommendation on its own, which is why there are no CRITICAL findings. All four will produce a defective pack if carried into authoring unchanged.

---

## 4. Decision Criteria Findings

### 4.1 Technology neutrality — PASS

All 115 criterion **names** and **definitions** are stated as requirements or constraints, not as products. The worked examples in §2.2 are the correct discriminations (*"Needs Dataverse"* → *"a governed relational operational data store with row- and column-level authorization and field-level audit"*). I found **no criterion that encodes a technology choice inside the question**.

The four current-state criteria (DC-D-109, DC-D-110, DC-D-111, DC-D-114) are correctly identified as such and are permitted by `.claude/rules/no-tech-mention-before-options.md` (*"Data lives in SharePoint today ✓"*). They describe the estate, not the solution.

One residual, recorded as L-05 rather than as a neutrality failure: the `Decision impact` and signal fields are written in a consistent **pack-local circumlocution** — *"the governed relational store"*, *"the task-focused surface"*, *"the record-centric surface"*, *"the external-site surface"*, *"the document/list store"*. The vocabulary is used consistently across all four files and never slips into product names, which is disciplined. But it is nowhere **declared**, and `data-architecture.md` DQ-03/U-14 explicitly instructs that a pack *"must declare its own vocabulary as pack-local"*. A glossary is a prerequisite for using this material, and Block D correctly does not author one — but it should name the requirement.

### 4.2 Decision relevance — PASS with fragmentation

The inclusion test in §2.1 is the right test and is applied. I found no criterion that is purely informational and none that is an implementation detail. The organisational criteria (DC-D-006, DC-D-070, DC-D-104, DC-D-110, DC-D-114) earn their place: the corpus's own evidence makes them *availability* conditions, not preferences (*"if there is no operator, the pattern is unavailable, not merely expensive"*).

Fragmentation is the real coverage defect, not omission. See M-03 and M-04.

### 4.3 Semantic precision — PASS with exceptions

The corpus's dangerous words are handled well:

| Term | Handling | Verdict |
|---|---|---|
| "real-time" | Banned; DC-D-018 requires a number and a source of change | ✅ |
| "high volume" | Refused; *"scale anxiety without a number"* is named as a failure | ✅ |
| "critical" | DC-D-001 states four classes by observable consequence, not by tier name | ✅ |
| "enterprise" | Defined as a criticality class with named obligations | ✅ |
| "complex" | DC-D-022 `DEEP` = *"traversal beyond two levels"* — measurable | ✅ |
| "external" | DC-D-009 decomposes into five identity classes | ✅ |
| "regulated" | DC-D-059 requires the named regime and the clause verbatim | ✅ |
| "mission-critical" | DC-D-001 / DC-D-104 pair separates *required* from *demonstrated* | ✅ |
| "scalable" | Excluded as an adjective, per `integration-architecture.md` C-04 | ✅ |

The exceptions are M-05: three criteria carry ordinal states with no semantic anchor at all.

### 4.4 State quality — PASS with exceptions

States are mostly categorical-where-categorical and ordinal-where-ordinal, as §2.3 claims. `UNKNOWN` is a first-class state on all 115. Where the corpus publishes a figure, it stays in `Decision impact` rather than becoming a state name — a deliberate design choice that I agree with, because it localises revalidation.

Exceptions in M-05. One further observation, not a finding: several states are *decision-shaped* rather than *evidence-shaped* — DC-D-040's `EXCEEDS, PARTITIONABLE` versus `EXCEEDS, NOT PARTITIONABLE` requires an architectural judgement to classify. That is correct here (the partitioning question genuinely is the decision) but a downstream question bank will need a two-step elicitation, not one question.

### 4.5 Positive / caution / exit signals — PASS on structure, FAIL on counting

§2.5's refusal to force an exit onto every criterion is correct and is the single best structural decision in the file. Governance and ALM producing **zero** exits is defensible and correctly explained (§9 item 5): those areas' findings are about obligations and cost, not capability absence.

But the counting is wrong — H-01 — and the taxonomy behind it is applied inconsistently. DC-D-040's exit (*"the integration responsibility leaves the platform"*) carries an `X`; DC-D-039's structurally identical exit (*"the integration responsibility leaves the platform"*) does not. The distinction between a *platform* exit and a *responsibility* exit is real and useful, but it is not applied consistently, and neither the register nor the matrix names it as a distinction.

### 4.6 Hidden vendor bias in the signals — NOT FOUND, with one leak

I looked specifically for a positive-signal tilt and found the opposite: the signal language is disciplined (*"no documented constraint violated"*, never *"Microsoft endorses"*), and the `PP positive` fields are consistently narrower than the criteria they sit under.

One leak: **DC-D-055** (M-06). It inherits a comparative claim — *"no equivalent in the alternatives"* — from `automation-architecture.md` §4.1 row 12, presents it as *"a comparative capability fact rather than a preference"*, and states an unqualified rule: *"Any human decision within 30 days → **keep this leg in the platform even if other legs move**."* The corpus cannot know this: `automation-architecture.md` §3.B row 19 states plainly that *"no Microsoft or independent source evaluates incumbent BPM/ESB platforms; treat as reasoning, not evidence"*, and `alternatives.md` ALT-007 repeats it. In an organisation running a BPM engine that already owns the process class, DC-D-055's rule and DC-D-111/DC-D-036/ALT-007's redirect point in opposite directions. The hedge exists (DC-D-055's `Related alternatives` names ALT-007) but not in the rule itself, and the matrix row carries the bolded superlative with no comparator caveat.

### 4.7 Decision-blocking unknowns — PASS

The 28-criterion blocking set (§5.2) is the correct set and is mechanically consistent with the register (I verified: exactly 28 `B` flags). It covers every category the brief names — throughput (DC-D-040, DC-D-037), criticality (DC-D-001), availability (DC-D-091, DC-D-100), regulatory (DC-D-059), system of record (DC-D-021), external identity (DC-D-061), transaction semantics (DC-D-054, DC-D-052), budget/licensing (DC-D-092, DC-D-093) — plus deployment model (DC-D-108), which is the sharpest and is correctly placed first in the evaluation order.

§5.3's counterweight is as important as §5.2 and is well argued: *"a pack that treats every unknown as blocking will never produce a recommendation, and one that treats none as blocking will produce confident nonsense."*

`DECISION BLOCKED — MORE EVIDENCE REQUIRED` is a first-class outcome, it is reached in 5 of my 15 scenario re-runs, and — critically — §6's rule that a blocked outcome *"names the outcome it would produce under each resolution of the unknown"* is what makes the block actionable rather than evasive. That is the single best decision-model feature in Block D.

---

## 5. Anti-Pattern Findings

### 5.1 Structural quality — PASS

All 67 entries carry `Trigger conditions`, a named `Why it fails` mechanism, `Consequences` landed on a named party, `Decision impact` and `Evidence`. I verified this mechanically. 66 of 67 carry an `Exceptions` field (the 67th, AP-D-036, carries one in a different bold span — not a defect).

The §2 inclusion test is the right test and the §3 ledger is the right artefact: 101 candidates evaluated, with 20 rejected explicitly as *"Areas 1–12 altitude"* and 3 as misclassified. Publishing the rejections is what makes the accept boundary auditable, and I used it: the rejected list (nested loops, `OnStart` overloading, leading-wildcard filters, multiple publishers, patches-as-hotfix, alerts-to-a-mailbox) is correctly bounded. None of them belongs at decision altitude.

### 5.2 False-positive test — PASS

Explicitly tested, both of the brief's cases and three more:

| Normal pattern | Correctly conditioned? |
|---|---|
| Direct point-to-point integration | ✅ AP-D-022's Exceptions defend it; AP-D-023 is its symmetric counterpart; `integration-architecture.md` §4.1's seven conditions are cited |
| Document/list store as a data store | ✅ AP-D-008's Exceptions state the positive cases in detail (*"the document is the record"*, small flat trackers, form-over-a-list) |
| Data virtualization | ✅ AP-D-012 names a documented sweet spot (narrow, positively-filtered, read-mostly reference reads) |
| Replication | ✅ AP-D-010 permits a scoped one-way replica where a named platform data feature requires it |
| UI/robotic automation | ✅ AP-D-020 names the three conditions under which it is justified, and records that the fragility framing is *not* a Microsoft statement (`automation-architecture.md` U-07) |

No unconditional condemnation of a normal architecture was found.

### 5.3 Exception quality — PASS with a classification issue (M-08)

Six entries state `None`: AP-D-026, AP-D-031, AP-D-044, AP-D-051, AP-D-059, AP-D-067. Each supplies a scope boundary instead of an exception (*"the depth scales with class"*, *"a measured value is not invention"*, *"non-secret configuration is a different thing"*). That is honest, but by Block D's own §2 test — *"A structure that is always wrong is a constraint, not an anti-pattern"* — these six are constraints or reasoning rules, not context-conditional anti-patterns. Block D half-recognises this (§8 marks three as *"gates rather than risks"*) without following it through in the classification field.

### 5.4 Lineage — PASS

719 file-qualified references in the `Evidence` fields; 717 resolved mechanically; the 2 failures are the manifest-qualified `IA-U-14` / `IA-C-01` forms discussed in L-02. Origin tags (`MS`, `MS-V`, `INF`, `T3/T4`) are applied per entry and the 17 `INF`-framed entries are enumerated in §7 item 3 rather than buried. `T3/T4` sources are confined to frequency and incident-class claims and never carry a limit — I checked all four cases named in §7 item 4.

`AP-D-059` is correctly identified as the file's most consequential addition. It is the mechanism that prevents the whole model from degenerating into per-dimension favourability, and it is well evidenced from `architecture-patterns.md` §13, which I read in full and against which Block D's transcription is faithful (8 rows, correctly generalised — including the connector-conflict row, where Block D correctly replaces the two specific figures with *"either side of the open conflict, unmeasured"*).

### 5.5 Weak entries

Two entries I would challenge: AP-D-004 (M-09) and, less strongly, AP-D-039 — which Block D itself flags for exactly this scrutiny (§7 item 2: *"A reviewer should test these four hardest"*). Having tested them: AP-D-005, AP-D-006 and AP-D-023 survive on Microsoft's own *"not suitable when"* statements, which I verified in `architecture-patterns.md` §8. AP-D-039 survives more weakly, on the class definition plus the cost statements, and its confidence (MEDIUM) and `INF` framing are honestly stated. AP-D-004 is the one I would fold.

---

## 6. Alternatives Findings

### 6.1 Class coverage — PASS

All the classes the brief requires are present, under different names:

| Brief's class | Block D |
|---|---|
| existing system / no new platform | ALT-001 |
| process redesign | ALT-002 |
| Microsoft 365 native | ALT-003 |
| Power Platform | ALT-004 |
| custom development | ALT-005 |
| Azure / cloud-native | ALT-006 |
| existing enterprise platform | ALT-007 |
| other low-code platforms | ALT-008 |
| hybrid architecture | ALT-009 |
| — (Block D additions) | ALT-010 do nothing/defer, ALT-011 buy |

The ordering note (least-to-most new technology, *"a reading aid, not a preference ranking"*, with an explicit statement that arriving at ALT-005/006/008 quickly *"is not a failure"*) is the right guard against the ordering being read as a ladder.

### 6.2 Symmetry test — PASS, and this is the file's strongest section

`alternatives.md` §2 is written before anything else, which is the correct structure for a file that could easily become advocacy. I tested all five forbidden universals against the finished text of all four Block D files:

| Forbidden claim | Asserted anywhere? |
|---|---|
| "custom development is more expensive" | No. ALT-005's cost section states *"No universal direction"* and cites LC-U-04 (no comparative TCO study exists) |
| "low-code is faster" | No. §2.2 rejects it as a marketing claim by the source policy's own test; DC-D-003 explicitly *"never asserts that low-code is faster"* |
| "Power Platform scales / does not scale" | No. Both adjectives excluded per `integration-architecture.md` C-04 |
| "Azure is the answer for anything hard" | No — and AP-D-002/ALT-007 actively counter it; `architecture-patterns.md` AP-10 is described as *"the corpus's antidote to 'Azure is automatically the answer'"* |
| "building it yourself gives you control" | No. Countered with the vendor's own cost caution |

`ALT-004` is written to the same field structure as the other ten, and its weaknesses field is the longest in the file — 14 bulleted items against 1 paragraph of strengths. I checked whether that is theatre: it is not. Every weakness is a real decision-changing boundary with a canonical anchor.

The remaining asymmetry is **evidential, acknowledged, and unavoidable** — and Block D handles it by naming it (§5.3 "What is symmetrically unknown", §6's eight comparative gaps) rather than resolving it. That is the correct handling. The defect is not the asymmetry; it is that the outcome labels do not carry it (H-02).

### 6.3 Trigger quality — PASS

ALT-005's trigger table is the model for the rest: **thirteen rows, every one framed as a documented platform absence with a canonical citation**, not as a claim about custom development's merits. I verified four of the thirteen against `platform-suitability.md` and `application-architecture.md` (PS-47, PS-51, AA-40/AA-46, PS-45); all check out. The economic trigger (*"per-user licensing uneconomic at the audience's scale"*) is correctly labelled as economic rather than technical.

ALT-008's trigger table is the honest one: **one row EVIDENCE-BACKED, five rows CANDIDATE/`UNKNOWN`**, with the early-access caveat carried on the second comparator. `anti-patterns.md` §6.2's scoping statement — that V-D-04 establishes a *materially relevant distinction*, not a comparison — is exactly the right narrow conclusion to draw from that evidence.

### 6.4 Hybrid as a first-class option — PASS

ALT-009 is not framed as "Power Platform plus something else when it fails". It is framed as responsibility decomposition, opens with *"This is a first-class option, not a compromise"*, and carries eleven documented trigger shapes. Crucially, it also carries nine documented **weaknesses of hybrid as a shape** (two ALM models, two RBAC models, two monitoring surfaces, two retention windows, no cross-boundary correlation unless designed, availability profile conversion, two supply chains, governance non-extension, the private-egress/eventing collision). A file that only listed hybrid's virtues would fail this review; this one does not.

Responsibility decomposition is explicit for: UX, workflow, integration, API/mediation, data, compute, identity, orchestration, event processing and analytics. All ten of the brief's decomposition dimensions have a named owner-selection rule somewhere in ALT-009's trigger table or in `architecture-patterns.md`'s composition set. The gate (`AP-D-026`: no operator → *unavailable, not merely expensive*) is enforced consistently and appears in the matrix, in ALT-009, in DC-D-070 and in AP-D-059.

### 6.5 What is missing

Nothing structural. The gaps are evidential and are already reported in `alternatives.md` §6 — I re-derived them independently and reached the same eight, plus one the corpus does not name: **document generation and templating is absent from the entire corpus** (0 hits across all twelve canonical files). That is an Area 1–12 gap, not a Block D defect, and it is recorded in §19.

---

## 7. Decision Intelligence Matrix Findings

### 7.1 Linkage — PASS, mechanically verified

I re-ran the §8.1 cross-linking audit rather than trusting it:

| Claim | Independent result |
|---|---|
| 115 criteria → ≥1 anti-pattern | ✅ verified, 115/115 |
| 115 criteria → ≥1 alternative | ✅ verified, 115/115 |
| 115 criteria → lineage field | ✅ verified, 115/115 |
| Matrix anti-pattern column == criteria `Related anti-patterns` | ✅ verified — **identical sets on all 115 rows** |
| No dangling `AP-D-` / `ALT-` / `DC-D-` references anywhere in Block D | ✅ verified, 0 dangling |

Set-level agreement between two independently authored representations of 115 rows is a strong signal. This part of the work is sound.

### 7.2 Orphans — PASS

Zero unreachable items. The three "deliberately weakly linked" items (§8.2) are correctly handled: AP-D-059 belongs to combinations rather than to any criterion; ALT-008 has one strong trigger and six weak ones, and padding it would be invention; DC-D-113's evidence base is genuinely empty and is recorded as such rather than filled.

### 7.3 Contradictory and overstated rows

- **H-01** — the exit-column count contradicts both peer files.
- **M-07** — outcome-class vocabulary drift between §6 of `decision-criteria.md`, AP-D-059's decision impact and T-14's outcome.
- **L-01** — two id transpositions in §6's scenarios (`AP-D-053` used for a trigger-concurrency failure in T-05; `DC-D-047` used for solution-awareness in T-10). Both are silent failures: the transposed ids exist, so no mechanical check catches them. This is the cost of running `AP-D-NNN` and `DC-D-NNN` over the same numeric range, and two instances surfaced in a 15-scenario spot check.
- Two rows disagree with their own criterion body on whether an exit exists: DC-D-093 and DC-D-104 (subsumed in H-01).

### 7.4 Evaluation order — PASS, and it is the best part of the matrix

§5's nine-step order is correct, and §5's justification (*"an option that is unavailable cannot be made available by being cheap"*) is the right reason for putting economics after the gates. T-09 demonstrates the non-commutativity concretely — evaluating offline capture (a platform strength) before cross-region recovery (a platform absence) yields an optimistic answer that Steps 0–1 prevent. That the model **exposes** its own order dependency instead of hiding it is a mark of quality.

The order is, however, the single most fragile thing to carry into a pack: it is stated in prose in one file and is not enforced by anything. §18 records the correction.

---

## 8. Technology Neutrality Assessment

**PASS.**

| Test | Result |
|---|---|
| Criterion names free of vendor/product | ✅ 115/115 |
| Criterion definitions free of vendor/product | ✅ 115/115 |
| Criteria elicitable in a Discovery phase forbidding product names | ✅ — the `Discovery evidence` fields are requirement-shaped throughout |
| Current-state criteria identified as such | ✅ 4 identified (DC-D-109, 110, 111, 114); permitted by the project's own rule |
| Technology choice encoded inside a question | ❌ none found |
| Anti-pattern `Detection signals` neutral | ✅ with the stated exception for estate-describing signals |
| Alternative classes named as capability classes, not products | ✅ — no vendor is named in any ALT title |

The one qualification is L-05: the pack-local circumlocution is consistent and disciplined but undeclared. A pack cannot be authored from this material until the mapping from *"the governed relational store"* to its product name is written down — and the Options phase is where that mapping is permitted to exist.

---

## 9. Power Platform Bias Assessment

**No vendor-favouring bias found. A structural asymmetry found instead.**

Rejection capability, tested against the brief's required outcome list:

| Required outcome | Producible? | Where demonstrated |
|---|---|---|
| Power Platform strong fit | ✅ | §6 class 1; T-01, T-06 |
| Power Platform conditional fit | ✅ | §6 class 2; T-02, T-06 |
| Power Platform + Azure hybrid | ✅ | §6 class 3; T-05, T-11 |
| Power Platform + enterprise-system hybrid | ✅ | §6 class 4; T-03 |
| Existing platform preferred | ✅ | §6 class 6; T-12 |
| Custom development preferred | ✅ | §6 class 5; T-07, T-13 |
| Another low-code should be evaluated | ✅ | §6 class 8; DC-D-108 exit, evidence-backed on one axis |
| Process redesign / no new technology | ✅ | §6 class 9; T-14 |
| Insufficient evidence | ✅ | §6 class 11; T-03, T-04, T-08, T-09, T-15 |
| **Power Platform rejected** | ⚠️ **producible in substance, absent as a label** | T-04, T-07, T-13 reject it; but §6 has no `POWER PLATFORM — POOR FIT` class, while AP-D-059 and T-14 emit classes §6 never defines (M-07) |

**Does Power Platform almost always survive?** No. In my 15 independent re-runs it survived unconditionally in 2, survived with constraints in 3, survived only as a partial-scope component in 4, was displaced or rejected in 4, and was blocked pending evidence in 2 with rejection live in both. On the requirement classes the corpus can evidence — deployment model, cross-system atomicity, real compute, contractual availability, product-grade experience with native distribution and push, a public third-party interface, frozen behaviour, administrator-excluded confidentiality — rejection is clean, over-determined and correctly reasoned.

**The asymmetry that does exist is not pro-vendor.** It is that Power Platform is the only class with a full per-criterion evaluation. Everything else has triggers and consequences. The consequences are two, and they point in opposite directions:

- The model can reject Power Platform on evidence but cannot *choose* between the survivors on evidence (H-04). T-14 is the clearest instance and Block D itself rates it HIGH.
- The model's non-Power-Platform outcome labels therefore assert a preference the evidence does not support (H-02).

`alternatives.md` §9 states this precisely and correctly: *"A decision model built on this must be strong on disqualification and modest on preference."* The finding is that the labels are not modest.

---

## 10. Evidence Lineage Assessment

**PASS — strongest dimension of Block D.**

| Test | Result |
|---|---|
| File-qualified references resolved, `decision-criteria.md` | **732 / 732** |
| File-qualified references resolved, `anti-patterns.md` | **717 / 719** |
| File-qualified references resolved, `alternatives.md` | **131 / 131** |
| Canonical-only sourcing (Areas 1–12 + declared external checks) | ✅ |
| Canonical ids renamed? | ❌ none — manifest §4 respected; new namespaces (`DC-D-`, `AP-D-`, `ALT-`) verified collision-free |
| `UNKNOWN` preserved | ✅ — NB-01, NB-04, NB-05, NB-07, LC-U-05, PF-U-07, the unpublished concurrency and amplification figures, the polling intervals |
| `CONFLICTED` preserved | ✅ — NB-02 preserved *and re-verified as still open* rather than closed |
| `VOLATILE VALUE` preserved | ⚠️ partial — see M-01 |
| `INF` preserved | ✅ — 17 entries enumerated; NB-06 carried into AP-D-027, ALT-007 and DC-D-036 with the "not vendor-endorsed" warning intact |
| Inference presented as fact | ❌ one instance found (M-06, DC-D-055) |
| Thresholds invented | ❌ none found. AP-D-051 institutionalises the prohibition |

Content spot-checks against the canonical text (not just id existence):

| Claim | Canonical source | Verdict |
|---|---|---|
| SaaS-only, no on-premises/customer-hosted deployment | `platform-suitability.md` PS-47 | ✅ faithful, including the sovereign-cloud parity exceptions |
| External-site 15-minute cache, non-reducible | `performance-scale.md` PF-17 (*"No. SLA for cache refresh remains 15 minutes"*) | ✅ faithful — and Block D correctly preserves the on-site-change carve-out |
| 50,000 aggregate ceiling is scope-specific, not a report-size ceiling | `data-architecture.md` DA-03 (REVISED) | ✅ faithful — Block D carries the *revision*, which is the trap; a careless extraction would have re-broadened it |
| Branded native distribution excludes push and consumer audiences | `application-architecture.md` AA-40, AA-46 | ✅ faithful |
| Options must always carry process change, incumbent, PP, alternatives, do-nothing | `licensing-cost.md` LC-28 | ✅ faithful, including *"No Microsoft source frames this — the absence is the point"* |
| `architecture-patterns.md` §13's eight composed disqualifiers | read in full | ✅ faithful transcription; the conflicted-figures row correctly generalised |
| Duplicate `DC-14` in `licensing-cost.md` | verified: two rows at lines 357–358 | ✅ Block D's §1.4 observation is **correct**; the manifest's `DUPLICATE CANONICAL IDS: 0` is wrong |

That last row deserves emphasis. Block D found a defect in the manifest's own mechanical-validation claim, recorded it in two files with the disambiguation rule (*"disambiguate by question text, never by number"*), mapped both senses separately in its lineage map (§8.2 DC-14 (a)/(b)), and **did not repair it**, because repairing Areas 1–12 is out of scope. That is exactly the right behaviour and it is worth stating as a positive finding.

---

## 11. Combinatorial Decision Assessment

**PARTIAL — the mechanism is right, the register is under-populated.**

The mechanism is correct and is the model's best idea. `decision-criteria.md` §2.4 argues from evidence — not from instruction — that a score would pass options the corpus documents as *unavailable*, because *"three of the eight conclude the option is unavailable, not worse"*. AP-D-059 turns that into a detectable failure. The matrix §3 turns it into a runnable test placed at Step 4, before economics. This is materially better than a scoring model and the reasoning survives scrutiny.

Against the brief's eight named combinations:

| Combination | Covered as a composed rule? |
|---|---|
| scale + strict latency | ⚠️ narratively (DC-D-042/084 exits + DC-D-089); no composed row |
| external users + security sensitivity | ⚠️ inside DC-D-009's exit text; no composed row |
| mission criticality + operational immaturity | ✅ Block D addition, matrix §3 |
| low budget + premium/security requirements | ✅ `architecture-patterns.md` §13 row 3 |
| high integration complexity + weak API ownership | ⚠️ narratively (DC-D-035 + DC-D-036 + AP-D-022/027); no composed row |
| citizen development + business criticality | ❌ no composed row — handled only by AP-D-036/AP-D-065/AP-D-047 |
| bidirectional sync + strict consistency | ✅ substantially (row 8 + NB-01 + AP-D-011) |
| high change frequency + weak ALM maturity | ❌ no composed row |

Four of eight are enumerated. The two that are entirely absent both sit in **Governance and ALM** — the two domains Block D correctly identifies as producing zero exit signals. That is the structural cause: a domain that cannot produce a single-criterion exit also, in this design, contributes no composed row, so its combinations are invisible to the one test that is supposed to catch exactly this. T-10 reaches the right answer, but by narrative reasoning over four anti-patterns rather than by a rule.

Compounding it: the two combinations Block D *does* add live only in the matrix. AP-D-059's own trigger table — the enforcement mechanism — still lists eight (M-02).

No numerical scoring model was introduced anywhere. Verified across all four files.

---

## 12. Volatility Assessment

**PARTIAL.**

What is handled correctly:

- A dedicated volatility register (`decision-criteria.md` §7, matrix §4) with 10 criteria, each naming *what* is volatile and *when* to re-verify.
- The NB-02 20× conflict is **not resolved**, is re-verified as live in currently-maintained pages, and both figures are explicitly barred from encoding. DC-D-039 is decision-blocking as a consequence. This is exactly right, and it is the corpus's single most consequential open item.
- §2.3's rule that a published figure never becomes a **state name**, so revalidation changes one sentence rather than a taxonomy. Verified across all 115 criteria — no state name contains a number except the anchored population bands (`TENS`, `HUNDREDS`, `THOUSANDS`), which are semantic rather than product limits.
- AP-D-055 makes building on transition-period or preview terms an anti-pattern in its own right.
- DC-D-115 treats preview and general-availability state as a criterion, with the corpus's own two-facts-already-changed warning carried forward.

What is not (M-01): the register covers **commercial and licensing** volatility and excludes **service-limit** volatility, which manifest §5's `VOLATILE VALUE` definition explicitly includes (*"quota, limit, feature-state"*). Service limits are embedded in `Decision impact` fields and in matrix exit cells as timeless rules — the 15-minute cache floor, the 30-day run ceiling, the 50,000 aggregate ceiling, the 500/2,000 delegation ceiling, the ~5,000 list threshold, the 12-column ceiling, the 500-action ceiling, the 7/28-day backup window, the two-minute server-side ceiling. `decision-criteria.md` §7 claims a mitigation — *"where a static criterion's decision impact quotes a figure, the figure carries its own source and date in the lineage"* — but the `Lineage` fields carry file and id only; **no date appears in any lineage field**. The mitigation is stated and not implemented.

The practical damage today is limited, because most matrix exit cells are phrased qualitatively (*"beyond 30 days as a single run"*, *"sub-15-minute freshness"*) and the figures behind them are current as of 2026-09-03. The damage is downstream: a pack authored from these fields will encode a service limit as a permanent decision rule, which is precisely the brief's `BAD` example.

---

## 13. Adversarial Scenario Results

I re-ran all fifteen independently against the criteria, anti-pattern and alternatives files, without reading the matrix's own §6 conclusions first, then compared.

| # | Scenario | Key criteria activated | Anti-patterns | Alternative classes | Expected direction | Block D sensible? | Weakness exposed |
|---|---|---|---|---|---|---|---|
| 1 | Simple departmental app | DC-D-001, 008, 010, 022, 023, 074, 104 | AP-D-039, 005, 065 (as over-correction risks) | ALT-002, 003, 004, 010 | Strong fit **or** collaboration-native, with a graduation trigger | ✅ | none |
| 2 | Excel replacement | DC-D-023, 026, 030, 022, 031, 093 | AP-D-008, 050, 009, 061 | ALT-004; ALT-003 excluded by DC-D-026/030 | Fit with constraints; premium priced | ✅ | none — best-evidenced scenario in both directions |
| 3 | Business-critical internal app | DC-D-001, 021, 036, 091, 100, 097, 104 | AP-D-047, 053, 056, 010, 066 | ALT-001, 004, 007, 009 | Blocked on 036/100/091 → enterprise-system hybrid | ✅ | blocking condition is organisational (needs another team) — M-11 process risk |
| 4 | External customer portal | DC-D-009, 018, 061, 010, 058, 094, 085 | AP-D-034, 024, 009, 032 | ALT-004, 005, 011 | Blocked on the freshness number → 15-minute constraint or custom web | ✅ | exit is clean; the replacement's adequacy is unevidenced (NB-07) |
| 5 | High-volume integration | DC-D-040, 037, 039, 041, 052, 086, 021 | AP-D-016, 049, 015, 017 | ALT-006, 007, 009 | Cloud-native hybrid, gated on DC-D-070/110; blocked if a custom connector is on the path | ✅ | **L-01: the matrix cites AP-D-053 for a trigger-concurrency failure; that is AP-D-015 / DC-D-053** |
| 6 | Complex enterprise data app | DC-D-022, 026, 027, 032, 031, 021, 058 | AP-D-029, 009, 012, 063, 011 | ALT-004 (documented STRONG), 011, 009 | Fit with constraints + hybrid analytics; buy-check first | ✅ | none |
| 7 | Strict low-latency | DC-D-084, 042, 050, 091, 057 | AP-D-003, 019, 048 | ALT-005, 006, 007 | Custom or enterprise platform preferred | ✅ | symmetry correctly preserved — no claim that custom achieves 200 ms either |
| 8 | Regulated / security-sensitive | DC-D-058, 059, 062, 064, 027, 033, 107 | AP-D-029, 033, 064, 057, 058 | ALT-005, 007, 008, 011 | Blocked on clause reading → hybrid with the excluded attribute outside, or buy/custom | ✅ | model correctly **refuses** to resolve the key-vs-audit conflict |
| 9 | Mission-critical | DC-D-001, 100, 091, 016, 089, 104, 097 | AP-D-056, 054, 052, 059 | ALT-005, 006, 007, 009, 011 | Blocked on 100/091 → restated objective or custom/enterprise core | ✅ | best demonstration of order dependency; hybrid correctly noted to *worsen* 091 |
| 10 | Citizen app → enterprise | DC-D-006, 074, 001, 071, 104, 093, 033 | AP-D-036, 040, 047, 066, 065, 053 | ALT-011, 001, 004, 002 | Blocked on ownership → buy or extend; migration not remediation | ✅ | **L-01: "DC-D-047 solution-awareness" — DC-D-047 is consumer count**. Also **M-02: no composed row for citizen-dev + criticality** |
| 11 | Platform + cloud-native hybrid | DC-D-057, 025, 037, 054, 070, 110, 083, 096, 055 | none fatal; latent AP-D-046, 026, 017, 006 | ALT-009 (is ALT-009), 005, 006 | Hybrid, gates satisfied | ✅ | the "gates pass" case is correctly identified as a finding in itself |
| 12 | Enterprise system should own it | DC-D-111, 036, 021, 002, 109, 003 | AP-D-027, 007, 022, 002 | ALT-007, 001, 011, 004 | Existing enterprise platform preferred | ✅ | rests on NB-06 (`INF`) with no incumbent evaluated — honestly labelled |
| 13 | Custom clearly preferable | DC-D-020, 009, 016, 012, 010, 045 | AP-D-003, 005 (in reverse) | ALT-005, 009 | Custom for the consumer surface; PP legitimate behind it | ✅ | over-determined rejection (4 independent exits) — usefully distinguished from a single-exit case |
| 14 | Economically unattractive | DC-D-010, 094, 093, 063, 092, 008, 002 | AP-D-062, 064, 061, 060 | ALT-001, 011, 002, 005, 006, 010 | Economically unattractive → extend / buy / redesign | ⚠️ | **the model can say "this is expensive for this shape"; it cannot say "that one is cheaper"** — H-02's root |
| 15 | Insufficient evidence | most of §5.2 as `UNKNOWN` | AP-D-001, 051 | all eleven remain open | `DECISION BLOCKED`, with the four highest-value questions named | ✅ | none — the value-of-information ranking is the model at its best |

**My independent scoring: 13 pass, 2 expose gaps (T-14 materially, T-04 partially) — identical to Block D's own §7.** I found no scenario where Block D's stated conclusion was wrong, and no evidence of tuning. T-14's gap in particular would have been trivially concealable by inventing a "cost efficiency" criterion with comparative states; Block D declines and says why. That restraint is the strongest single indicator that this work is not an advocacy document.

Two additional weaknesses my re-runs exposed that Block D's own §7 does not record:

- **T-05 and T-10 both contain an id transposition** (L-01), invisible to mechanical checking.
- **T-10's correct answer is reached without a rule.** Citizen-development-becoming-critical is arguably the single most common real engagement in this domain, and it has no composed disqualifier row — only four separately-detected anti-patterns whose conjunction the model does not formally test (M-02).

---

## 14. Coverage Matrix

Legend: ✅ sufficient · ⚠️ partial · ❌ missing · ⚠️C conflicting

| Domain | Criteria | Anti-patterns | Alternatives | Lineage | Decision usefulness |
|---|---|---|---|---|---|
| Business | ✅ 8 | ✅ 7 (selection + architecture) | ✅ ALT-001/002/010/011 | ✅ | ✅ — DC-D-008 carries the "build nothing" exit |
| User / UX | ✅ 12 | ⚠️ effectively 1 dedicated (AP-D-003) | ✅ ALT-004/005/003 | ✅ | ✅ — highest exit density (7); detection thin (M-11) |
| Data | ✅ 14 | ✅ 7 | ✅ ALT-003/004/005/006/007 | ✅ | ✅ — best-evidenced domain overall |
| Integration | ✅ 13 | ✅ 7 | ✅ ALT-006/007/009 | ✅ | ⚠️C — DC-D-039 exit present in body, absent from the register (H-01) |
| Automation | ✅ 10 | ✅ 7 | ✅ ALT-004/006/009 | ✅ | ⚠️ — DC-D-055's unqualified rule conflicts with ALT-007 (M-06) |
| Security | ✅ 11 | ✅ 7 | ✅ ALT-001/005/007 | ✅ | ✅ — DC-D-062 is the cleanest single-criterion exit in the corpus |
| Governance | ✅ 7 | ✅ 5 | ⚠️ ALT-004/011 only | ✅ | ⚠️ — 0 exits (correct); but also 0 composed rows (M-02) |
| ALM | ✅ 8 | ✅ 7 | ⚠️ ALT-004/005 only | ✅ | ⚠️ — 0 exits (correct); change-frequency × ALM-maturity has no rule (M-02) |
| Performance / Scale | ✅ 8 | ✅ 5 | ✅ ALT-005/006/009 | ✅ | ✅ — NB-07 correctly makes limits exclusion-only |
| Cost | ✅ 8 | ✅ 8 | ✅ ALT-002/010/001/003/005/006 | ✅ | ⚠️ — mechanism strong, comparison absent (H-02, T-14) |
| Operations | ✅ 5 | ✅ 6 | ✅ ALT-011/001/007/009 | ✅ | ✅ |
| Strategic / Platform | ✅ 11 | ⚠️ 4 (AP-D-002/057/058/065) | ⚠️ ALT-005 ✅ / ALT-008 evidence-thin by admission | ✅ | ✅ — DC-D-108 is the model's sharpest exit |
| **Agent / conversational** | ❌ **absent** | ❌ absent | ❌ absent | n/a | ❌ **H-03** |

---

## 15. Critical Findings

**None.**

I looked specifically for findings that could produce an unsafe or materially wrong platform decision. The candidates I tested and rejected as CRITICAL:

- *Could the model recommend Power Platform for a workload it cannot serve?* No — the absolutes are evaluated at Step 0, the exits are over-determined in the clear cases (T-13 needs four independent exits before it concludes), and AP-D-059 catches the composed cases.
- *Could the model invent a threshold?* No — AP-D-051 makes it an anti-pattern, §7's volatility register flags the date-sensitive figures, and I found no invented number in 115 criteria.
- *Could the model resolve a live conflict silently?* No — NB-02 is preserved as decision-blocking and re-verified as open; T-08 explicitly refuses to resolve the key-versus-audit conflict.
- *Could the model quietly hide the "do not build" answer?* No — DC-D-008's exit is *"do not build on any platform"*, ALT-002 and ALT-010 are first-class classes, and `licensing-cost.md` LC-28's five-option requirement is enforced.

The HIGH findings below are gate-blocking because they will corrupt the pack built from this material, not because they produce a wrong answer today.

---

## 16. High Findings

### H-01

**Finding.** Three Block D files report three different totals for the same quantity — how many of the 115 criteria carry an evidence-backed exit signal. `decision-criteria.md` §3, §3.1 (register `X` flags), §2.5 and §11 say **36**. The criteria bodies contain **48** criteria whose `PP negative/exit` field states a substantive exit rather than a form of "none". The matrix's own exit column carries a substantive exit on **46** rows. Twelve criteria carry a written exit and no `X` flag, and are excluded from every published count.

**Severity.** HIGH

**Type.** CONTRADICTION

**Affected Items.** DC-D-010, DC-D-031, DC-D-036, DC-D-039, DC-D-043, DC-D-054, DC-D-068, DC-D-092, DC-D-093, DC-D-103, DC-D-104, DC-D-106. Also `decision-criteria.md` §3 domain table (per-domain exit counts), §2.5, §11 summary; `decision-intelligence-matrix.md` §9. Secondary: DC-D-093 and DC-D-104 disagree between their own body (exit present) and their matrix row (`—`).

**Evidence.** Mechanical: 115 `PP negative/exit` fields; 67 begin with a "none…" formulation, 48 do not; the register carries exactly 36 `X` flags and exactly 28 `B` flags (the `B` count is correct and matches §5.2). Examples of excluded exits, quoted from the criteria bodies: DC-D-036 — *"`CAPABILITY EXISTS, CONTRACT PUBLISHED` → the platform is **not** the integration layer for that stream (ALT-007)"*; DC-D-039 — *"`EXCEEDS` with no partitioning available → the integration responsibility leaves the platform"*; DC-D-054 — *"`MUST NOT PARTIALLY COMPLETE` across systems → out of the platform for the coordination responsibility"*; DC-D-092 — *"Budget inadequate for the mandated controls or the required audience → the option is infeasible"*. Each is bolded as an exit in its matrix row.

**Why It Matters.** Two reasons, both downstream. First, the register is the machine-readable summary — a pack authoring signals or a decision tree from §3.1 rather than from 115 prose entries loses twelve documented exits, four of which are among the corpus's most consequential negative findings. Second, the number 36 is load-bearing in an *argument*: §2.5 and §9 item 5 use the 36/79 split to establish that the exit distribution is evidential rather than constructed. An argument that rests on a miscount is easy to dismiss at the moment it most needs to hold.

The underlying cause is a taxonomy applied inconsistently: Block D distinguishes a *platform* exit from a *responsibility* or *pattern* exit, which is a genuine and useful distinction, but DC-D-040's responsibility exit carries `X` while DC-D-039's structurally identical one does not, and the distinction is never named as a distinction.

**Required Correction.** Name the two exit classes explicitly (for example `X` = platform exit, `Xr` = responsibility/pattern exit). Re-flag all 115 criteria against the named classes. Recompute the register, the §3 domain table, §2.5, §11 and matrix §9 from the flags. Reconcile DC-D-093 and DC-D-104 between body and matrix. State the corrected totals in all three files. *(Not performed — this review does not modify Block D.)*

---

### H-02

**Finding.** The outcome classes assert comparative preference on every non-Power-Platform branch — `CUSTOM DEVELOPMENT PREFERRED`, `EXISTING ENTERPRISE PLATFORM PREFERRED`, `BUY — PACKAGED PRODUCT OR SERVICE` — while the corpus holds no comparative TCO, no comparative benchmark, and no evaluation of any incumbent platform or product. The evidence supports *"Power Platform is excluded for this scope; the candidate classes are X and Y, neither evaluated"*. The labels claim more.

**Severity.** HIGH

**Type.** ALTERNATIVE ASYMMETRY

**Affected Items.** `decision-criteria.md` §6 outcome classes 5, 6, 7, 8; `decision-intelligence-matrix.md` §6 T-07, T-12, T-13, T-14 outcome lines; `alternatives.md` §9 (which states the correct position but does not govern the labels).

**Evidence.** `alternatives.md` §6 item 1: *"No like-for-like pricing was fetched for custom development, cloud-native services, other low-code platforms or packaged products, and no independent comparative study was found."* §6 item 3: *"The corpus evaluates none [no incumbent enterprise platform], and says so."* §5.3: *"Neither 'the platform will be fast enough' nor 'custom will be fast enough' is evidenced."* ALT-005 Confidence: *"The comparative claims are deliberately absent, because the corpus holds no comparative TCO or benchmark evidence."* ALT-007 Confidence: *"LOW on any specific incumbent's fit, which the corpus explicitly cannot assess."* T-14 records the consequence exactly: *"the model can say 'this is expensive for this shape' and cannot say 'that one is cheaper'."*

**Why It Matters.** The outcome class is the model's user-visible output — the sentence that lands in a decision record and a sponsor deck. Every internal caveat in four files is discarded at that boundary. An architect handed `CUSTOM DEVELOPMENT PREFERRED` will reasonably read it as *the research recommends custom development*, when the research recommends nothing of the sort: it excludes Power Platform for a named scope and hands over an unevaluated candidate set. This is the one place where Block D's otherwise exemplary evidential honesty does not survive into the output, and it is the place where it matters most.

It also interacts with H-04: because alternatives have no per-criterion evaluation, the "preferred" class is not merely unevidenced — there is no apparatus that could evidence it.

**Required Correction.** Rename the non-Power-Platform outcome classes to state exclusion plus a candidate set plus an evidence obligation (for example `POWER PLATFORM EXCLUDED FOR THIS SCOPE → CANDIDATES: ALT-005, ALT-006 — comparative fit UNEVALUATED, engagement assessment required`). Where a class genuinely is evidence-backed for a specific requirement, scope the label to it (ALT-008 on the deployment-model axis is the only such case). Carry `alternatives.md` §9's sentence into `decision-criteria.md` §6 as a governing rule on the class names. *(Not performed.)*

---

### H-03

**Finding.** No criterion, anti-pattern or alternative class addresses conversational or agent-shaped requirements. The stated justification (`decision-criteria.md` §8.5) covers only *consumption economics*, but the canonical corpus carries substantive agent evidence in governance, security and operations that is not economic and is not carried forward.

**Severity.** HIGH

**Type.** MISSING CRITERION

**Affected Items.** `decision-criteria.md` §4.2 (Users, 12 criteria — none conversational), §4.5 (Automation, DC-D-048's four shapes — none agentic), §8.5, §9 item 6; `alternatives.md` (0 mentions); `decision-intelligence-matrix.md` §8.3.

**Evidence.** Block D's justification cites: no published per-operation consumption figure, per-interaction consumption an open unknown making *"agent economics unmodellable in advance"*, a bundled allocation with a dated removal, and governance *"preview; not researched here"*. All true, and all economic or governance-maturity claims. What the canonical corpus *does* carry: `governance.md` treats agents as first-class governed artefacts with policy scope (*"prevent agents, apps, and flows from calling any service"*), records that Copilot Studio virtual connectors are *"evolving into their own dedicated governance rules"*, and lists agents in the tenant inventory scope; `security.md` §9 names *"agent authentication/channels"* among the surfaces that changed in the research window, records that vault-backed secrets are consumable by *"cloud flows, Copilot Studio agents and custom connectors only"*, and documents that Copilot Studio items using Graph connectors *"might access the information in these items even if you block guest access"*; `operations-support.md` records agent runtime as **not covered** by regional resilience.

The inconsistency is internal: **DC-D-113** (multi-tenancy and resale) is carried as a full criterion with `LOW` confidence, an explicitly empty evidence base, a `V` flag and a decision-blocking status on the commercial model. That is the correct pattern for a decision-relevant requirement whose evidence is absent. Agents received the opposite treatment for the same situation.

**Why It Matters.** *"Users need a conversational assistant over our enterprise data"* is a requirement an architect will meet in 2026 engagements, and it materially changes architecture, governance scope, security posture and economics. Block D's model has nowhere to put it: it would be forced into DC-D-012 (`FORM AND LIST SHAPED` … `PRODUCT-GRADE`) or DC-D-048 (`WORKFLOW` … `DISTRIBUTED PROCESSING`), neither of which can express it. The failure mode is silent — the model returns a confident answer to the wrong question. The Graph-connector guest-access bypass makes this a security-relevant gap, not only a coverage one.

**Required Correction.** Add a criterion in the Users domain for conversational/agentic interaction requirement (states along the lines of `NONE` / `ASSISTED SEARCH AND SUMMARY` / `TASK-COMPLETING AGENT` / `AUTONOMOUS AGENT` / `UNKNOWN`), with evidence drawn from the governance, security and operations material that exists, `UNKNOWN` economics preserved, and a decision-blocking flag on the commercial model — the DC-D-113 pattern applied consistently. Consider a companion criterion in Automation for agent-as-actor. Record the residual economic gap as a research follow-up rather than as grounds for omission. *(Not performed.)*

---

### H-04

**Finding.** The decision apparatus evaluates one class. All 115 criteria carry `PP positive` / `PP caution` / `PP negative-exit` signals; no alternative class has per-criterion states or signals. Alternatives carry triggers (which classes come into scope) and consequences (what each class costs), but nothing that discriminates between them under a given requirement state. The model can therefore determine whether Power Platform is in or out, and cannot determine which of the survivors fits.

**Severity.** HIGH

**Type.** BIAS (structural asymmetry — not vendor-favouring)

**Affected Items.** All 115 criteria's signal fields; `decision-intelligence-matrix.md` §2 (columns 2–4); §6 T-14; `alternatives.md` §5.1 (which produces candidate sets, correctly, but is the only cross-class instrument).

**Evidence.** The matrix's own column definitions name only Power Platform states. `alternatives.md` §5.1 is explicitly *"candidate set, not verdict"*. §8 warns that *"a pack that renders §5.1 as a lookup table will produce confident wrong answers"* — correct, and it leaves nothing else to render. T-14 is the exposed instance and Block D rates it HIGH itself. Symmetric evidence exists in places and is not used structurally: DC-D-110 `LOW-CODE ONLY` is a documented *disqualifier for ALT-005/ALT-006* (`architecture-patterns.md` §13: *"Hybrid architecture required + no pro-dev/enterprise platform capability available → POOR FIT"*), and DC-D-070 `NONE`/`EMERGING` makes ALT-006/ALT-009 *unavailable* — both are recorded as prose gates rather than as per-criterion negative signals against those classes.

**Why It Matters.** It is the direct answer to this review's primary question. The brief asks whether Block D can help an architect move *from requirements and constraints to viable solution directions*. It reliably delivers the first half — requirement → constraint → Power Platform in/out. The second half — direction among the viable alternatives — has no apparatus. In every engagement where Power Platform is excluded (4 of my 15 re-runs, plus 2 of the 5 blocked ones on likely resolution), the model hands the architect an unstructured candidate set at exactly the moment the decision becomes hardest.

Note carefully what this finding is **not**. It is not a claim that the model favours Power Platform: it rejects it readily and on evidence. It is a claim that the *evaluation is one-sided in shape*, which produces an unevidenced hand-off rather than a biased recommendation.

**Required Correction.** For the criteria where the corpus holds symmetric evidence — capability gates (DC-D-070, DC-D-110, DC-D-104, DC-D-073, DC-D-114), operating-model gates (DC-D-083, DC-D-096) and the documented alternative-side limits already collected in ALT-005's and ALT-006's weaknesses fields — add per-class caution and exclusion signals so that alternatives can be constrained by the same criteria. Where the corpus holds no symmetric evidence, add an explicit `COMPARATOR EVIDENCE ABSENT` marker rather than silence, so the hand-off is visibly incomplete. Do not manufacture comparator signals; mark the absence. *(Not performed.)*

---

## 17. Medium / Low Findings

### M-01 — Service-limit volatility not registered; §7's stated mitigation not implemented

**Type.** VOLATILITY ERROR · **Affected.** `decision-criteria.md` §7 (10 volatile criteria), all `Lineage` fields; matrix §4. Concretely: DC-D-018 (15 minutes), DC-D-049 (30 days), DC-D-031 (50,000), DC-D-023 (500/2,000), DC-D-022 (12 columns, 2 lookup levels), DC-D-032 (7/28 days), DC-D-028 (two minutes), DC-D-088 (~5,000 list threshold).
**Evidence.** Manifest §5 defines `VOLATILE VALUE` to include *"quota, limit, feature-state"*. §7 registers only the ten commercial/licensing criteria and asserts of the other 105: *"Where a static criterion's decision impact quotes a figure, the figure carries its own source and date in the lineage."* No `Lineage` field in any of the 115 criteria contains a date — verified mechanically.
**Why it matters.** These figures sit inside `Decision impact` fields and matrix exit cells, which is where a pack will read decision rules from. The brief's own `BAD` example is exactly this: *"If calls exceed X, use Azure"* where X is a volatile service limit. Damage today is limited because most exit cells are phrased qualitatively; damage downstream is a pack that treats a 2026 service limit as timeless.
**Required correction.** Either extend the volatility register to service-limit-bearing criteria with a re-verification trigger, or implement §7's claimed mitigation by carrying `ms.date` alongside each quoted figure. Do not do neither.

### M-02 — Composed-disqualifier register under-populated, and its enforcement mechanism is out of step

**Type.** COMBINATORIAL GAP · **Affected.** `decision-intelligence-matrix.md` §3 (10 rows); `anti-patterns.md` AP-D-059 trigger table (8 rows); `decision-criteria.md` §2.4 ("eight combinations").
**Evidence.** Eight rows are inherited wholesale from `architecture-patterns.md` §13; Block D adds two, and they appear **only in the matrix**. AP-D-059 — the entry that makes the composed test detectable and enforceable — still carries eight. §2.4 still says eight. No composed row is drawn from Governance or ALM, so *citizen development + business criticality* and *high change frequency + weak ALM maturity* have no rule. T-10 reaches the right answer by conjoining four separately-detected anti-patterns, which is precisely the reasoning AP-D-059 exists to formalise.
**Why it matters.** The composed test is the load-bearing substitute for the scoring model Block D correctly refuses. A pack generated from `anti-patterns.md` alone loses Block D's two additions; a pack that trusts the composed set as complete will miss the two most common low-code governance failure combinations.
**Required correction.** Reconcile the three counts. Add composed rows for the two named Governance/ALM combinations if the evidence supports them, or state explicitly why a zero-exit domain also contributes no composed row.

### M-03 — DC-D-023 and DC-D-088 are the same criterion

**Type.** DUPLICATE CRITERION · **Affected.** DC-D-023 (Queried volume per interactive access path), DC-D-088 (Record count per access path at horizon).
**Evidence.** DC-D-023's definition: *"For each interactive screen or query, the number of records the query must consider… projected to the investment horizon."* DC-D-088's: *"For each access path — screen, query, view, retrieval — the number of records it must reason over at year three."* DC-D-088 claims to be *"the operational form of DC-D-023, expressed per path rather than per store"* — but DC-D-023 is already expressed per path. Their lineages share the same roots (`performance-scale.md` PF-01/PF-02, DC-01/DC-02; `data-architecture.md` DA-39/DA-40), and their matrix anti-pattern sets are near-identical (AP-D-050, AP-D-008 ± AP-D-012).
**Why it matters.** A question bank generated from both asks the same question twice with different state vocabularies (`BELOW CEILING`/`ABOVE CEILING…` versus `SHALLOW AND SMALL`/`DEEP AND LARGE`), which is how conflicting answers to the same fact enter a Shared Understanding.
**Required correction.** Merge into one criterion with two dimensions (volume per path, traversal depth per path), or restate DC-D-088 as depth-only and remove the volume overlap.

### M-04 — Near-duplicate clusters: portability/exit, peak/growth, environment count

**Type.** DUPLICATE CRITERION · **Affected.** DC-D-098 / DC-D-105 / DC-D-106; DC-D-037 / DC-D-087; DC-D-071 / DC-D-082.
**Evidence.** DC-D-106 is described in its own text as *"DC-D-105 expressed as an obligation rather than a preference"*, and DC-D-098 is the cost of the same axis; the three share `platform-suitability.md` PS-51 and `licensing-cost.md` §6 as their common root. DC-D-037 (frequency distribution and peak shape) and DC-D-087 (peak load shape and growth horizon) both elicit peak-versus-average and both are decision-blocking. DC-D-071 and DC-D-082 both produce an environment topology and both enumerate the same four cost axes.
**Why it matters.** The brief warns specifically against splitting one well-defined criterion into near-identical ones. Three clusters is not fatal, but each multiplies discovery effort and creates reconciliation work between answers that cannot disagree.
**Required correction.** Collapse DC-D-098/105/106 into one portability-and-exit criterion with cost as a field. Merge DC-D-037 into DC-D-087 or scope DC-D-037 explicitly to per-stream arrival only. State the DC-D-071/082 distinction as one criterion with two drivers.

### M-05 — Unanchored ordinal states

**Type.** WEAK CRITERION · **Affected.** DC-D-024 (`SMALL` · `MODERATE` · `LARGE` · `VERY LARGE OR HIGH-GROWTH`), DC-D-025 (`NONE` · `LOW` · `MODERATE` · `HIGH` · `LARGE FILES`), DC-D-096 (`NONE` · `MINOR` · `MATERIAL` · `DOMINANT`).
**Evidence.** None of the three states carries a semantic or measurable anchor. Compare with the criteria that get this right: DC-D-010/DC-D-085 use population bands that are self-anchoring; DC-D-022 defines `DEEP` as *"traversal beyond two levels"*; DC-D-035 anchors at `2–5 STREAMS`. In all three flagged cases the actual decision comes from the modelled figure in `Decision impact` (year-three volume, bytes per window, priced TCO line), so the state contributes no information.
**Why it matters.** This is the brief's *"arbitrary LOW/MEDIUM/HIGH with no semantic basis"* case, and it is the kind of state that acquires false authority once a pack renders it as a dropdown.
**Required correction.** Anchor relatively rather than absolutely — DC-D-024 against purchased entitlement and the redesign trigger, DC-D-025 against the content-throughput window and the payload ceilings, DC-D-096 against the option's total cost. Relative anchors do not require inventing a threshold.

### M-06 — DC-D-055 asserts a comparative claim the corpus forbids, and its rule is unqualified

**Type.** CONTRADICTION / BIAS · **Affected.** DC-D-055; matrix §2.5 row DC-D-055; `alternatives.md` §2.2, §5.3; ALT-007.
**Evidence.** DC-D-055 states the approvals capability is *"stated as a comparative capability fact rather than a preference"* and quotes *"no equivalent in the alternatives"*, sourced to `automation-architecture.md` §4.1 row 12. That row is tagged `AT2-23, AT2-24, AT2-25` — findings which establish that approvals *exist* and what they do, not what alternatives lack. The same canonical file states at §3.B row 19: *"no Microsoft or independent source evaluates incumbent BPM/ESB platforms; treat as reasoning, not evidence"*, and ALT-007 repeats it. DC-D-055's decision impact is unqualified: *"Any human decision within 30 days → **keep this leg in the platform even if other legs move**."* The matrix row carries the superlative (*"the platform's strongest documented differentiator here"*) with no comparator caveat.
**Why it matters.** It is the one positive comparative claim that survives into the model's signal layer, in a file that opens by forbidding exactly this class of claim. In an organisation running a BPM or service-management engine that already owns the process class, DC-D-055's rule and DC-D-111/DC-D-036/ALT-007's redirect give opposite instructions, and DC-D-055's is stated as a rule while the redirect is stated as a consideration.
**Required correction.** Restate the claim as scoped and inherited: approvals are a first-class construct on standard entitlement, *no equivalent was found in the code-first alternatives the corpus examined*, and comparator capability in incumbent process engines is `UNKNOWN`. Qualify the decision impact with DC-D-111's precondition.

### M-07 — Outcome-class vocabulary drift

**Type.** SEMANTIC DRIFT · **Affected.** `decision-criteria.md` §6 (11 defined classes); `anti-patterns.md` AP-D-059 decision impact (emits `POWER PLATFORM POOR FIT`); AP-D-061 decision impact and matrix T-14 (both emit `POWER PLATFORM IS ECONOMICALLY UNATTRACTIVE`).
**Evidence.** §6 defines neither `POOR FIT` nor `ECONOMICALLY UNATTRACTIVE`, and has no explicit rejection class at all — rejection is expressed only indirectly through the preference classes (H-02). `platform-suitability.md`'s own classification model does carry `POOR`.
**Why it matters.** The terminal set of a decision tree must be closed and consistent. Three files emitting three overlapping vocabularies guarantees that a pack's decision tree and its rendered deliverables will disagree about what the engagement concluded.
**Required correction.** Define the closed outcome set once, in `decision-criteria.md` §6, including an explicit `POWER PLATFORM — POOR FIT / EXCLUDED` class and an economic-infeasibility class. Make every emitting site reference it.

### M-08 — Six anti-patterns are constraints by Block D's own inclusion test

**Type.** WEAK ANTI-PATTERN · **Affected.** AP-D-026, AP-D-031, AP-D-044, AP-D-051, AP-D-059, AP-D-067.
**Evidence.** All six state `Exceptions: None` and supply a scope boundary in place of an exception. `anti-patterns.md` §2's own test: *"A structure that is always wrong is a constraint, not an anti-pattern."* §8 half-corrects this by marking AP-D-026, AP-D-059 and AP-D-013 as *"gates rather than risks"*, without changing the `Classification` field of any entry.
**Why it matters.** A pack renders a constraint as a hard check and an anti-pattern as a contextual warning. Six items rendered in the weaker form include the hybrid operator gate (AP-D-026) and the composed-disqualifier test (AP-D-059) — the two items Block D itself identifies as making options *unavailable*.
**Required correction.** Reclassify the six as `CONSTRAINT` or introduce a `GATE` classification, and align §8's "gates rather than risks" list with the `Classification` field.

### M-09 — AP-D-004 has no distinct failure mechanism

**Type.** WEAK ANTI-PATTERN · **Affected.** AP-D-004 (One platform for every workload class).
**Evidence.** Its mechanism decomposes into AP-D-015 (shape mismatch), AP-D-009 (analytics on the operational store), AP-D-039/AP-D-036 (simultaneous over- and under-governance) plus shared-capacity contention already carried by AP-D-063. Its trigger conditions are estate-level (*"an estate in which workloads of visibly different shapes all run on the same platform"*), which is not observable within a single engagement — the altitude at which every other entry operates. Its own Confidence is MEDIUM with the estate-level framing marked `INF`.
**Why it matters.** It is the one entry whose detection signals a Discovery process cannot produce, so it will either never fire or fire on judgement rather than evidence.
**Required correction.** Merge into AP-D-015 + AP-D-063, or restate as a portfolio-level governance finding explicitly outside the engagement-altitude set.

### M-10 — Missing anti-pattern: agent surface bypassing the data access model

**Type.** MISSING ANTI-PATTERN · **Affected.** `anti-patterns.md` §5.5 (Security).
**Evidence.** `security.md` records that Copilot Studio items using Graph connectors *"might access the information in these items even if you block guest access"*, and `governance.md` records that agent virtual connectors are *"evolving into their own dedicated governance rules"* — i.e. current policy coverage is incomplete. That is a documented mechanism by which an authorization decision made at one plane is bypassed at another, which is the same failure family as AP-D-030 and AP-D-033 and is derivable from canonical evidence.
**Why it matters.** It is a security-relevant, evidenced failure mechanism that the accepted set does not carry. It is also the concrete instance that makes H-03 more than a coverage gap.
**Required correction.** Add the entry, or record explicitly in §3's ledger that agent-surface anti-patterns were considered and rejected with a stated reason. Currently the ledger does not mention agents at all.

### M-11 — User/UX domain has the highest exit density and the thinnest detection

**Type.** MISSING ANTI-PATTERN · **Affected.** `decision-criteria.md` §4.2 (12 criteria, 7 flagged exits); `anti-patterns.md` (one UX-specific entry, AP-D-003).
**Evidence.** The UX domain produces more exit signals than any other except Data, and several are absolute (branded distribution with push; offline in a browser; mandated design system on record-centric core pages; product-grade consumer experience). Detection rests almost entirely on the criteria themselves; AP-D-003 is the only anti-pattern whose triggers are UX-shaped, and its trigger table is cross-domain rather than UX-specific.
**Why it matters.** Exits without detection signals fire only if the right question was asked. `application-architecture.md` carries AP-17…AP-35, most correctly rejected as implementation altitude — but the rejection appears to have been applied uniformly rather than tested per entry for decision impact.
**Required correction.** Re-examine `application-architecture.md` AP-17…AP-35 specifically against the four-element test, and record in the §3 ledger which UX candidates were considered. Currently §3.1–§3.11 contains no UX section.

---

### Low findings

**L-01 — Two id transpositions in the adversarial scenarios.** `decision-intelligence-matrix.md` §6 T-05 cites *"AP-D-053 ordering by trigger concurrency, which is irreversible and lossy"* — AP-D-053 is *Business-critical application with no monitoring and no incident owner*; the described failure is DC-D-053 / AP-D-015. §6 T-10 cites *"DC-D-047 solution-awareness"* — DC-D-047 is *Consumer count for a backend capability*; solution-awareness is AP-D-047 / DC-D-001. Both are silent failures because `AP-D-NNN` and `DC-D-NNN` share a numeric range, so both ids resolve. Two instances surfaced in a 15-scenario check, which suggests the class is worth a systematic pass. *Type: SEMANTIC DRIFT.*

**L-02 — `IA-U-14` / `IA-C-01` cited against a file that carries `U-14` / `C-01`.** The only two mechanical lineage failures out of 1,582 references. Both forms are defensible (the manifest §4 declares the qualified forms canonical; the mounted `integration-architecture.md` carries the unqualified ones), and the manifest's own lineage reservation covers the mismatch. Block D uses both forms in different entries. *Type: LINEAGE GAP.* Correction: cite as `manifest NB-01 / IA-U-14 (= integration-architecture.md U-14)`.

**L-03 — The V1–V4 validation model is cited to a section that does not exist.** AP-D-052's evidence line reads *"`integration-architecture.md` §15.8 as cited by peers (four-level model)"*. That file has fourteen sections. The model is actually defined in `alm-devops.md` (V1 documentation/limits, V2 bounded pilot with monitoring, V3 pro-dev automated harness, V4 managed-test fidelity), and `architecture-patterns.md` and `performance-scale.md` carry the same dangling citation — so this is an inherited Area 1–12 defect, correctly hedged by Block D but propagated. *Type: LINEAGE GAP.* Correction: re-anchor to `alm-devops.md`; raise the dangling citation as an Areas 1–12 repair item (§19).

**L-04 — Register ordering.** AP-D-055 appears in §5.11 after AP-D-066; AP-D-067 appears in §5.9 before AP-D-059. The §4 register is authoritative and correct, so this is cosmetic — but it makes a sequential read look like an omission. *Type: SEMANTIC DRIFT.*

**L-05 — Pack-local vocabulary undeclared.** *"The governed relational store"*, *"the task-focused surface"*, *"the record-centric surface"*, *"the external-site surface"*, *"the document/list store"*, *"the team-hosted surface"* are used consistently across four files and never declared. `data-architecture.md` DQ-03/U-14 explicitly requires a pack to *"declare its own vocabulary as pack-local"*. *Type: SEMANTIC DRIFT.* Correction: record the glossary requirement as a named prerequisite for pack authoring (Block D correctly does not author it).

**L-06 — §3.12 ledger arithmetic needs its footnote.** 101 candidate topics against 67 + 21 + 20 + 3 = 111 verdict rows. The reconciliation (ten accepted topics split into two entries each) is stated immediately below the table, so this is not an error — but the table alone does not balance, and a reader checking the audit trail will stop at the table. *Type: SEMANTIC DRIFT.*

**L-07 — DC-D-093 and DC-D-104 disagree between body and matrix on whether an exit exists.** Subsumed in H-01; recorded separately because the correction is per-row rather than per-taxonomy.

---

## 18. Required Corrections

Ordered by gate impact. **None has been performed.**

| # | Correction | Finding | Gate-blocking? |
|---|---|---|---|
| 1 | Name the two exit classes (platform vs responsibility), re-flag all 115 criteria, recompute every published exit count in three files, reconcile DC-D-093/DC-D-104 | H-01 | **Yes** |
| 2 | Rename non-Power-Platform outcome classes to state exclusion + candidate set + evidence obligation; carry `alternatives.md` §9's rule into `decision-criteria.md` §6 | H-02 | **Yes** |
| 3 | Add a conversational/agent criterion using the DC-D-113 pattern (evidence where it exists, `UNKNOWN` economics, decision-blocking commercial model) | H-03 | **Yes** |
| 4 | Add per-class caution/exclusion signals where symmetric evidence exists; add an explicit `COMPARATOR EVIDENCE ABSENT` marker where it does not | H-04 | **Yes** |
| 5 | Extend the volatility register to service-limit-bearing criteria, or implement §7's claimed date-carrying mitigation | M-01 | Yes |
| 6 | Reconcile the composed-disqualifier count across three files; add or explicitly decline Governance/ALM composed rows | M-02 | Yes |
| 7 | Define the closed outcome-class set once; align AP-D-059 and T-14 to it; add an explicit rejection class | M-07 | Yes |
| 8 | Merge DC-D-023 / DC-D-088; collapse the DC-D-098/105/106 cluster; resolve DC-D-037/087 and DC-D-071/082 | M-03, M-04 | No |
| 9 | Anchor the ordinal states on DC-D-024, DC-D-025, DC-D-096 relatively | M-05 | No |
| 10 | Re-scope DC-D-055's comparative claim and qualify its decision impact with DC-D-111 | M-06 | No |
| 11 | Reclassify the six no-exception anti-patterns as constraints or gates; align §8's gate list with the `Classification` field | M-08 | No |
| 12 | Merge or re-scope AP-D-004 | M-09 | No |
| 13 | Add the agent/data-access-bypass anti-pattern, or record its consideration in the §3 ledger | M-10 | No |
| 14 | Re-test `application-architecture.md` AP-17…AP-35 for UX decision impact; add a UX section to the §3 ledger | M-11 | No |
| 15 | Fix the two id transpositions; run a systematic `AP-D-NNN` ↔ `DC-D-NNN` transposition pass over all prose | L-01 | No |
| 16 | Normalise `IA-U-14`/`IA-C-01` citation form; re-anchor the V1–V4 model to `alm-devops.md` | L-02, L-03 | No |
| 17 | Record the pack-local glossary as a named prerequisite; fix register ordering; footnote the §3.12 arithmetic | L-04, L-05, L-06 | No |

---

## 19. Research Follow-Ups

Items outside Block D's remit, surfaced by this review.

1. **`licensing-cost.md` duplicate `DC-14` — confirmed, and the manifest is wrong.** Two distinct criteria share the id at lines 357–358. `canonical-manifest.md` §4 records `DUPLICATE CANONICAL IDS: 0` and cites a *"Licensing/Cost `DC-14…DC-18` repair"* that is incomplete in the mounted snapshot. Block D recorded it correctly and did not repair it. **A bounded Areas 1–12 repair is required, and the manifest's mechanical-validation claim must be corrected**, because downstream extraction is now entitled to trust a guarantee that does not hold.
2. **`integration-architecture.md` §15.8 does not exist.** Three canonical files (`architecture-patterns.md`, `performance-scale.md`, and Block D by inheritance) cite it as the home of the V1–V4 validation model, which is actually defined in `alm-devops.md`. Either restore the section or re-anchor all citations. This is the manifest's "canonical lineage reservation" made concrete.
3. **NB-02 remains open and live.** Re-verified 2026-09-03 in currently-maintained pages, 20× apart. It is not a stale-page artefact. Every engagement touching a high-frequency custom connector must re-check and measure. Consider commissioning a definitive vendor clarification.
4. **Comparative TCO commission.** `alternatives.md` §6 item 1, confirmed by T-14. This is the single most commonly expected output and the least supported. Without it, no pack can answer "which alternative is cheaper" — only "this one is expensive for this shape".
5. **Other low-code platform comparison commission.** `alternatives.md` §6 item 2. One axis (deployment model) is evidenced; everything else is `UNKNOWN`, and Area 1 placed the topic out of scope. If the pack needs a real comparison, it is a separate research area.
6. **Agent / Copilot Studio research area.** The corpus carries agent evidence in governance, security, operations and licensing but has no fit assessment (`platform-suitability.md`: zero mentions). Recommend an Area 16 covering agent fit boundaries, governance scope, security posture (including the Graph-connector guest-access bypass) and economics. H-03 is the Block D consequence; the root gap is upstream.
7. **Document generation and templating is absent from the entire corpus.** Zero mentions across all twelve canonical files. Document output at volume is a recurring architecture-changing requirement in this domain. Recorded as a discovered Areas 1–12 scoping gap, not a Block D defect.
8. **Incumbent-platform assessment method.** ALT-001, ALT-007 and ALT-011 are decision-logic classes whose fit is always a per-engagement assessment the corpus cannot make. A structured assessment method (what to ask an incumbent, what evidence closes the gap) would convert three `UNKNOWN` classes into usable ones without any comparative claim.
9. **Broker and streaming capacity envelopes.** Two of the three services recommended for guaranteed-delivery and streaming requirements were never sized (`automation-architecture.md` U-13, `integration-architecture.md` U-03). ALT-006 can be triggered but not sized for those two.

---

## 20. Final Review Verdict

Block D is a serious piece of work. Its lineage integrity is measurably excellent — 1,582 file-qualified references, two failures, both explained by a pre-existing manifest reservation. It preserves every canonical `UNKNOWN`, `CONFLICTED`, `VOLATILE VALUE` and `INF` semantic I tested, including the ones that would have been easier to resolve than to carry. It refuses to score, and argues the refusal from evidence rather than from instruction. It publishes its own rejections so the accept boundary is auditable. It found a defect in the manifest's own validation claim and recorded it without overstepping its scope. Its adversarial tests were, as far as I can determine, not tuned: T-14 exposes a HIGH gap that would have been trivial to conceal by inventing one criterion, and Block D declines and explains why.

It is not, on this evidence, a Power Platform recommendation engine, a product chooser, a checklist, a scoring model, a catalogue of generic best practice, a list of things Microsoft dislikes, or a competitor comparison table. It rejects the platform readily, on evidence, across a bounded and enumerable set of requirement classes, and it can conclude "build nothing", "buy", "extend the incumbent" and "not enough evidence".

The corrections are real and four of them are gate-blocking. The exit-signal arithmetic contradicts itself on the file's own headline argument. The terminal outputs assert preference on every non-Power-Platform branch where the corpus explicitly holds no comparative evidence. A whole requirement class — conversational and agent-shaped work — has no home, on a justification narrower than the omission. And the evaluation apparatus is one-sided in shape, so the model answers the first half of the primary review question well and hands the second half over unstructured.

None of that makes the current material unsafe. All of it will make the pack built from it defective.

**PASS WITH CORRECTIONS**

`BLOCK D REVIEW: PASS WITH CORRECTIONS`

`READY FOR BLOCK D GATE: NO`

Corrections 1–7 in §18 must be applied and re-checked before the formal Block D gate. Corrections 8–17 should be applied before pack authoring begins. **No correction has been performed by this review.**

---
