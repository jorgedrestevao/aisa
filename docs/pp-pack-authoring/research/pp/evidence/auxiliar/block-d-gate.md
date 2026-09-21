Gate Status: COMPLETE
Gate date: **2026-09-03**
Scope: **final Block D research gate — a strict promotion decision.** No Block D file was modified. No repair performed. No canonicalisation. No PP pack authoring. No new research. Areas 1–12 read for lineage verification only, not reopened.
Artifacts under gate: `decision-criteria.md` · `anti-patterns.md` · `alternatives.md` · `decision-intelligence-matrix.md`
Review history read in full: `block-d-review.md` · `block-d-repair-report.md` · `block-d-re-review.md` · `block-d-repair-v2-report.md` · `block-d-re-review-v2.md`

# Block D Research Gate

## 1. Executive gate verdict

**FAIL.**

Block D is a strong decision-intelligence layer with two unresolved gate-blocking defects. Its epistemic discipline, mechanical integrity and technology-neutrality *architecture* all pass independent verification. What fails is narrower and specific: the two findings raised by Re-Review V2 remain in the files exactly as reported, and **no Repair V3 exists**.

The artifacts were last modified at **17:56** on 2026-09-03; `block-d-re-review-v2.md` was written at **18:50**. The mounted state is therefore precisely the state Re-Review V2 judged, and its verdict — `HIGH 1`, `GATE-BLOCKING MEDIUM 1`, `READY FOR BLOCK D GATE: NO` — has not been acted on.

**This gate did not accept that verdict on trust.** Both findings were independently re-derived from the artifacts:

| Finding | Independently confirmed? | Method |
|---|---|---|
| **V2-H-01** — `Xr` membership not re-derived from §2.5's repaired one-limb test | **Yes** | Extracted all 116 `PP negative/exit` fields, isolated the 28 `Xr` fields, applied §2.5's decisive test (*"If nothing leaves the platform, this class does not apply"*) to every one. Exactly two fail: **DC-D-049** and **DC-D-068**. Both route to §6.2 class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` where the corpus documents an in-platform answer |
| **V2-M-01** — class 13's render template carries an unconditioned comparative clause | **Yes** | Read `decision-criteria.md` §6.2 class 13 and `alternatives.md` §8 verbatim. Both present, both unrepaired. The clause *"and is the cheaper or lighter option"* sits outside the `ALT-NNN` substitution slot; class 13's own trigger and §6.2's evidence anchor both admit ALT-001 and ALT-011, which the corpus prices nowhere |

Neither is a reviewer over-reading. Both are readable directly off the files, and both would be encoded verbatim by an authoring process consuming these artifacts.

**Counts.** `CRITICAL 0` · `HIGH 1` · `GATE-BLOCKING MEDIUM 1`.

**What passes.** Evidence integrity, decision-model completeness, and mechanical integrity all pass on independent recomputation — including the full three-way class agreement (116/116, 0 mismatches), 0 duplicate ids, 0 dangling references across 2,793 canonical id references, and every published headline number derived from the underlying classifications rather than maintained by hand.

---

## 2. Review-history closure

Traced `review → repair → re-review → repair v2 → re-review v2` for every gate-blocking finding.

| Generation | Gate-blocking findings raised | Disposition | Verified how |
|---|---|---|---|
| **Original review** (`block-d-review.md`) | CRITICAL 0 · HIGH 4 (H-01…H-04) · MEDIUM 11 (M-07 rated gate-blocking) · LOW 7 | H-02, H-03, H-04 **closed**. H-01 **superseded** by R-01. M-07 **superseded** by R-02 | §3 below |
| **Repair V1** (`block-d-repair-report.md`) | claimed `UNRESOLVED GATE-BLOCKING FINDINGS: 0` | claim **falsified** by Re-Review V1 | Re-Review V1 §3, §11 |
| **Re-Review V1** (`block-d-re-review.md`) | HIGH 1 (R-01) · gate-blocking MEDIUM 1 (R-02) · MEDIUM 2 non-blocking (R-03, R-04) · LOW | R-02 **closed** at V2. R-01 **partially closed** → V2-H-01. R-03, R-04 **still open**, non-blocking | §3, §11 below |
| **Repair V2** (`block-d-repair-v2-report.md`) | claimed `READY FOR BLOCK D RE-REVIEW V2: YES` | R-02's closure claim **holds**; R-01's does not | §3 below |
| **Re-Review V2** (`block-d-re-review-v2.md`) | HIGH 1 (V2-H-01) · gate-blocking MEDIUM 1 (V2-M-01) · MEDIUM 1 non-blocking (V2-M-02) · LOW 2 | **both gate-blocking findings unrepaired** — no Repair V3 exists | file mtimes; direct re-derivation |

**The review chain is honest and improving.** Each generation closed real defects and each re-review caught the previous repair's blind spot rather than rubber-stamping it. The exit-class count moved `36 → 48 → 54 → 48` and each move is documented with the test that produced it — a taxonomy that shrinks under scrutiny is behaving correctly. The chain has simply not been allowed to finish: it stopped one repair short of the gate.

### 2.1 Closure of the original HIGH findings

| Finding | Status | Verified in the artifacts |
|---|---|---|
| **H-01** — three files reported three different exit totals (36 / 48 / 46) | **Superseded, partially open.** Consistency fully closed; classification soundness not. Now V2-H-01 | Three-way agreement recomputed: body class == register class == matrix class, **116 / 116, 0 mismatches**. All seven published homes of the distribution agree. But two `Xr` memberships remain wrong (§4) |
| **H-02** — unsupported comparative preference in terminal outcomes | **Closed, with one residue.** The four preference labels (`CUSTOM DEVELOPMENT PREFERRED`, `EXISTING ENTERPRISE PLATFORM PREFERRED`, `BUY — PACKAGED PRODUCT OR SERVICE`, `ANOTHER LOW-CODE PLATFORM SHOULD BE EVALUATED`) are withdrawn in §6.3 and replaced by class 5/6/7 + class 8. Residue is V2-M-01 | §6.3's withdrawal table read in full; every surviving mention of a retired label verified as a *"Renamed 2026-09-03 from …"* note, not an emission |
| **H-03** — missing conversational / agentic coverage | **Closed.** DC-D-116 exists (Users and experience domain, `B*` blocking on the commercial and governance model), AP-D-068 exists (`anti-patterns.md` line 1511), T-16 exercises it, and `alternatives.md` §6 item 9 records the residual gap as a research commission | Read DC-D-116, AP-D-068, T-16 and §6 item 9 in full. No fabricated agent capability, economics, limit or architecture found — the criterion **blocks** rather than guesses |
| **H-04** — asymmetric evaluation of alternative classes | **Closed.** §4A exists with `COMPARATOR EVIDENCE ABSENT` as the default on all 116 criteria, an evidenced-signal table on 28, and §4A.3 stating explicitly what the section does not contain | `G` set recomputed = **28**, matched against §4A.2 in both directions, 0 divergence. 116 − 28 = **88** marked `COMPARATOR EVIDENCE ABSENT`, matching §4A.1's published figure |

### 2.2 Closure of Re-Review V1's gate-blocking findings

**R-02 — outcome set not closed. CLOSED.** Independently verified: §6.2 defines **14 classes**, numbered 1–14 with no gaps and no duplicates. The twelve V1 numbers are unmoved (correct, since AP-D-003/035/059/061 and eight matrix scenarios cite them by number). Class 13 `ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED` and class 14 `IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED` exist and fill the two shapes that were reachable with no terminal. Class 8's antecedent is widened to *"classes 5, 6, 7 and 14, and for class 13 where the alternative's sufficiency is not documented"*. §6.2 states closure as a **testable property** rather than an assertion, and matrix §5 Step 7 and AP-D-059 carry the same rule. §6.4's *"one outcome per scope, not one per engagement"* is now written down — it was always the matrix's behaviour and had never been stated.

**R-01 — exit taxonomy classification unsound. PARTIALLY CLOSED. Gate-blocking.** Sub-parts (b), (c), (d) and (e) are fully closed and independently verified: the class → outcome mapping table exists and is reproduced byte-compatibly in matrix §5 Step 7; **0 bare matrix cells** (was 10); **7 of 7** `Xc` criteria named in a matrix §3 row (was 6 of 24); matrix §9's stale *"79 dashes"* is repaired to 38 / 61. Sub-part (a) is not closed — see §4.

**R-03 and R-04 — still open, non-blocking, independently confirmed.** §11 below.

---

## 3. Gate 1 — Review closure

**FAIL.**

**Evidence inspected.** All five review-history documents in full. File modification times for all four artifacts and all five review documents. Direct re-derivation of both surviving findings from the artifacts.

**Reasoning.** Gate 1 requires 0 unresolved CRITICAL, 0 unresolved HIGH and 0 unresolved gate-blocking MEDIUM. The artifacts carry **1 unresolved HIGH** and **1 unresolved gate-blocking MEDIUM**, both raised by Re-Review V2 and neither repaired. The mtime evidence is unambiguous: the artifacts predate the re-review that found the defects, and no repair report for a third generation exists in `research/pp/evidence/`.

The instruction not to trust summary statements alone was applied in both directions. Repair V1's `UNRESOLVED GATE-BLOCKING FINDINGS: 0` and Repair V2's `READY FOR BLOCK D RE-REVIEW V2: YES` were both checked rather than accepted, and Repair V2's claims about R-02 were found to **hold** on independent test while its claim on R-01 does not. Two of Repair V2's own validation claims also fail to reproduce, as Re-Review V2 reported: its *"37 checks, 37 PASS"* on closure passes only if abbreviated outcome forms are excluded, and its §4.1 line *"No `Ri`/`Cf` field claims anything leaves the platform"* reproduces while the converse check — *every `Xr` field claims something leaves* — was never run. That converse check is exactly where V2-H-01 sits, and this gate ran it (§4).

**Blocking findings.**

- **G-H-01** (= V2-H-01) — HIGH, unresolved.
- **G-M-01** (= V2-M-01) — MEDIUM gate-blocking, unresolved.

---

## 4. Gate 2 — Evidence integrity

**PASS.**

**Evidence inspected.** `decision-criteria.md` §2.3, §4A.1, §4A.2, §4A.3, §4A.4, §5.1–§5.3, §6.1, §7.1–§7.3, §9 items 1–5a; `alternatives.md` §2.1–§2.3, §5.2, §5.3, §6, §7; `anti-patterns.md` §1.4, §6, AP-D-059; `canonical-manifest.md` NB-01…NB-08. Canonical cross-checks against `data-architecture.md` DA-17/DA-18, `licensing-cost.md` LC-U-04, `application-architecture.md` AA-50, `automation-architecture.md` §8.3/§8.4/U-14.

**Reasoning.** Block D does not silently upgrade any of the five states the gate names. Verified state by state:

| State | Verified |
|---|---|
| `UNKNOWN` | **Preserved.** Agent economics, capacity, latency and accuracy; broker and streaming sizing; comparator portability; incumbent fit; polling intervals; the unpublished concurrency figure (DC-D-085) and amplification multiplier (DC-D-086); GOV-U-06. DC-D-085's and DC-D-086's criteria carry a **measurement obligation** in place of a figure, which is the correct handling |
| `CONFLICTED` | **Preserved.** NB-02's 20× custom-connector conflict is live in DC-D-039, which carries `B V Xr G` in the register — decision-blocking, volatile and re-verified by date in matrix §4 with the instruction *"Do not encode either figure"* |
| `VOLATILE VALUE` | **Preserved and extended.** §7.1 registers commercial volatility; §7.2 adds the service-limit register the original omitted (20 criteria, derived mechanically, with two false positives excluded and stated). §7.2 also **withdraws** a mitigation the file had claimed and never implemented — *"the figure carries its own source and date in the lineage"* — on the stated grounds that a stated-but-unimplemented mitigation is worse than a named gap. That is the right call and it is the kind of self-correction this gate looks for |
| `INF` | **Preserved.** NB-06 carried in DC-D-036, DC-D-111, ALT-007 and T-12; ALT-002, ALT-007 and ALT-010 are `INF`-framed with the framing stated; AP-D-059's composition is declared as the corpus's own INF synthesis with the two Block D-derived rows marked as derived |
| `COMPARATOR EVIDENCE ABSENT` | **Preserved as a governing default.** §4A.1 makes it the default on every criterion; `G` = **28** recomputed and matched to §4A.2 in both directions with 0 divergence; **88** criteria carry it. §4A.3 states plainly that on the four questions most often asked of a decision model — cheaper, faster, scales further, more reliable — *"Block D's answer is `COMPARATOR EVIDENCE ABSENT`, in every direction, for every class"* |

**Traceability.** 2,793 file-qualified canonical id references were resolved mechanically across the four artifacts. **0 are truly dangling.** Forty-eight apparent misses all resolve to a documented namespace rather than a defect: manifest `NB-01…NB-08`; `anti-patterns.md` §6's own `V-D-01…V-D-04`; the cross-file `AP-1…AP-16` (`platform-suitability.md` §5) and `AP-17…AP-35` (`application-architecture.md` §11) namespaces declared in `anti-patterns.md` §1.3; the several canonical files each carrying their own local `DC-NN` series; and the qualified forms `IA-C-01` / `IA-U-14`, which AP-D-059's own Evidence field states are canonical per `pre-canonicalization-repair.md` while the mounted snapshot carries the unqualified `C-01` / `U-14`. Every one is an attribution artefact of the checker, not a broken reference.

**Where evidence is insufficient the model blocks.** 28 criteria block the decision unconditionally when `UNKNOWN` (§5.2, recomputed `B` = 28, matching §5.2's set in both directions with 0 divergence); 3 more block a named narrower scope (`B*` = DC-D-113, DC-D-115, DC-D-116, recomputed). §5.3 correctly declines to make the remaining 88 blocking, with the reasoning stated: *"a pack that treats every unknown as blocking will never produce a recommendation, and one that treats none as blocking will produce confident nonsense."*

**On G-M-01 and this gate.** Class 13's comparative clause does exceed the corpus's evidence. It is recorded against Gates 3, 5 and 8 rather than here because the overreach is **argued, not silent** — §6.1 states the exception explicitly and bounds it, class 13's own closing sentence disclaims it, T-01 disclaims it, and `alternatives.md` ALT-003's note disclaims it. Gate 2's test is silent upgrading of epistemic status; that test passes. The defect is that the emitted string contradicts its own four disclaimers, which is a neutrality and downstream-safety failure.

**Blocking findings.** None.

---

## 5. Gate 3 — Technology neutrality

**FAIL.**

**Evidence inspected.** `decision-criteria.md` §2.2, §4A, §6.1, §6.2 (all 14 classes), §6.3, §6.4, §9 item 7; `alternatives.md` §2.1, §2.2, §2.3, §5.1, §5.3, §6, §9; `anti-patterns.md` AP-D-001, AP-D-002, AP-D-004, AP-D-059, §2.1; matrix §5 Step 7a, all sixteen `**Outcome:**` lines.

**Reasoning.** The neutrality *architecture* is genuinely strong, and stronger than most decision frameworks of this kind. Specifically:

- **§2.2's five forbidden universal claims** — *"custom development is more expensive"*, *"low-code is faster"*, *"Power Platform scales / does not scale"*, *"Azure is the answer for anything hard"*, *"building it yourself gives you control"* — are each named with the canonical reason they are excluded, and each is checked absent from the finished text.
- **§2.3 is the neutrality test run in the pro-platform direction**, which is the direction most such documents omit: four MS-sourced reasons that are *not* reasons to leave Power Platform (scale anxiety without a number, a preference for code, one difficult step, resemblance to a reference architecture), plus two more from elsewhere in the corpus.
- **§5.3 records what is symmetrically unknown**, so a reader cannot over-conclude in whichever direction they were already leaning. NB-07 — no empirical benchmark for *any* technology — is applied to all eleven classes.
- **ALT-004 (Power Platform) is written to the same standard as the others**, and its weaknesses field is the longest in the file. §7 item 3 states this is deliberate.
- **§6.1's governing rule** separates exclusion, candidate generation, comparative evaluation and preference as four different statements, and matrix §5 Step 7a enforces the separation at the point the terminal sentence is written — the step the review chain identified as the one that had been missing.

**All seven required outcomes are producible and distinct.** Verified by reading all fourteen class definitions and all sixteen scenario outcomes:

| Required outcome | Class | Exercised by |
|---|---|---|
| Power Platform viable | 1 | T-01 |
| viable with constraints | 2 | T-02, T-04, T-05 fallback, T-06, T-09 |
| partial / hybrid responsibility | 3, 4, 6 | T-04, T-05, T-06, T-08, T-11, T-12 |
| capability owned by another existing platform | 4, 6 + 8 with `INCUMBENT FIT UNEVALUATED` | T-12 |
| Power Platform excluded | 5, 6, 7 | T-07, T-13 (5) · T-12 (6) · T-14 (7) |
| alternatives requiring evaluation | 8 | T-07, T-10, T-12, T-13, T-14 |
| decision blocked pending evidence | 12 | T-03, T-04, T-08, T-09, T-10, T-15, T-16 |
| *(also)* alternative sufficient, platform not excluded | 13 | T-01 |
| *(also)* in-place remediation unavailable | 14 | T-10 |

**The critical test holds on every exclusion path.** `Power Platform excluded` does **not** imply any alternative preference. Every one of the exclusion terminals is followed by class 8 `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: T-07 → 5 → 8; T-12 → 6 → 8; T-13 → 5 → 8; T-14 → 7 → 8; T-10 → 14 → 8. T-13 states the discipline sharply — ALT-005 is *"realistically the only class in scope, which is scope narrowing, not evaluation"*. T-14 states it sharper still: *"The model states that this option is expensive for this demand shape. It states nothing whatever about what the others cost."* AP-D-059 makes it a rule: *"the composed test can say the option is unavailable, and it cannot say which surviving class is better."* Candidate generation is not preference, and exclusion is not comparison, throughout.

**Why this gate nonetheless fails.** Gate 3 fails not on the exclusion paths but on the clause *"FAIL if material Power Platform advocacy or **unsupported alternative preference** remains encoded."* An unsupported alternative preference is encoded — in a terminal render template, which is the most consequential place for one to sit.

`decision-criteria.md` §6.2 class 13 renders as:

> *"No documented constraint excludes Power Platform. **ALT-NNN** is \<the documented answer for this shape / a candidate\> **and is the cheaper or lighter option**. Graduation trigger: \<the named DC-D-074 / DC-D-001 condition\>."*

The comparative clause sits **outside** the substitution slot, so it is emitted for whatever class is substituted. Class 13's own trigger admits *"a class other than ALT-004"*, and §6.2's evidence anchor names ALT-003, **ALT-001 and ALT-011**; `alternatives.md` §8 says the same. For ALT-001 and ALT-011 the corpus prices nothing — `licensing-cost.md` LC-U-04 records comparative TCO as absent, and `alternatives.md` §6 item 3 records that no incumbent and no product is evaluated. The template therefore emits a cost preference about two classes the corpus has never evaluated, in the sentence that lands in a decision record.

`alternatives.md` §8 carries the same shape: *"ALT-003 — or, as a candidate, ALT-001 or ALT-011 — **is the lighter answer** for the requirement shape."*

This is the identical defect shape as H-02, one generation later and one scope narrower. H-02's finding was that *"every internal caveat in four files was discarded at the one boundary where it matters most — the sentence that lands in a decision record."* That is exactly what class 13's render string does, and §6.1's own rule 1 forbids it in terms: *"No outcome class may contain the word 'preferred', 'better', 'cheaper' or 'faster' about a class the corpus has not evaluated."*

**Bias check run in both directions.** In the pro-platform direction, nothing softened: Power Platform is still rejected, displaced or blocked in twelve of sixteen scenarios, T-13 still carries four independent `Xp` exits plus an `Xe`, and no scenario gained a claim about an alternative's fitness. In the anti-platform direction, G-H-01 leaves a **false exclusion** in place on two criteria (§9), which is a neutrality defect in the opposite direction and no safer.

**Blocking findings.** **G-M-01** — unsupported alternative preference encoded in §6.2 class 13's render template and in `alternatives.md` §8.

---

## 6. Gate 4 — Decision-model completeness

**PASS.**

**Evidence inspected.** `decision-criteria.md` §3 domain table (all 12 rows × 9 class columns), §3.1 register (all 116 rows), §3.2 near-duplicate clusters, §4.1–§4.12, §5.2, §8 lineage map; matrix §2.1–§2.12, §3, §5; `alternatives.md` §3, §4, §5.1.

**Reasoning.** Every dimension the gate names has explicit coverage, and the two domains that cannot reject the platform on any single criterion are named as such rather than left to look like coverage.

| Dimension | Coverage | Verified |
|---|---|---|
| application architecture | Users and experience (13), Strategic and platform (11); AP-D-005 structural altitude, AP-D-004 portfolio altitude | §4.2, §4.12 read |
| data architecture | Data (14) | §4.3 read |
| integration | Integration (13) | §4.4 read |
| automation | Automation (10) | §4.5 read |
| security | Security (11) | §4.6 read |
| governance | Governance (7) — **0 direct exits, stated and explained** | §4.7, §9 item 5 |
| ALM | ALM and delivery (8) — **0 direct exits, stated and explained** | §4.8, §9 item 5 |
| scale · performance | Performance and scale (8) + envelope criteria at matrix §5 Step 3 | §4.9 read |
| licensing / economics | Cost (8), 5 `Xe` economic exits, §7.1 commercial volatility register | §4.10, §7.1 |
| operations / supportability | Operations (5), DC-D-100…104 | §4.11 read |
| ownership | DC-D-006 accountable ownership, DC-D-021 system of record, DC-D-036 integration ownership — all three in §5.2's blocking set | §5.2 read |
| lifecycle | DC-D-004 lifespan, DC-D-112 platform-change tracking, AP-D-067 no retirement lifecycle | §4.1, §4.12 |
| enterprise criticality | DC-D-001, `Xc`, `B`, cited in 3 composed rows | §4.1, matrix §3 |
| user experience | Users and experience domain, second-densest exit domain (4 `Xp`, 2 `Xr`, 1 `Xe`); `anti-patterns.md` §3.11b added a UX section that was previously absent | §4.2, `anti-patterns.md` §3.11b |
| conversational / agentic | DC-D-116 + AP-D-068 + T-16 + `alternatives.md` §6 item 9 | all four read |

**The governance and ALM zero-exit result is a finding, not a gap.** §9 item 5 explains it — the corpus's governance and lifecycle evidence is about *obligations and cost*, not capability absence — and warns that *"a pack that expects every domain to be able to reject the platform will invent thresholds in those two."* Both domains nonetheless contribute to the one test designed to catch that situation: Block D rows 3 and 4 of the composed register are the only rows drawn from Governance and ALM, and were added precisely because those domains were otherwise invisible to the composed test.

**Material gaps are explicit unknowns, not invisible assumptions.** `alternatives.md` §6 enumerates ten comparative evidence gaps with the decision consequence of each. Two are notable for their honesty: item 9 records conversational/agent capability as **evaluable in no class including ALT-004** — *"not asymmetric; it is total, so the honest output is `DECISION BLOCKED`, not a candidate set"* — and item 10 records document generation and templating as absent from all twelve canonical files, correctly classified as an **Areas 1–12 scoping gap rather than a Block D defect**.

**Elicitation-collapse risk is handled without lineage damage.** §3.2 identifies four near-duplicate clusters that a naive question bank would ask twice with different state vocabularies, and resolves them with a binding elicitation rule and a stated authority per dimension rather than by merging ids that three peer files already cite.

**Blocking findings.** None. No missing dimension was found that could materially corrupt pack authoring or platform-fit decisions.

---

## 7. Gate 5 — Cross-file semantic consistency

**FAIL.**

**Evidence inspected.** All four artifacts. Mechanical cross-checks on ids, class tags, anti-pattern sets, alternative sets and lineage fields (§8 below). Semantic reads of §2.5 against matrix §1 and §5 Step 7; §6.2 against AP-D-059 and all sixteen scenario outcomes; §6.1 against `alternatives.md` §9; the `Xc` registration rule across its three homes.

**Reasoning.** Most invariants hold, and several hold unusually tightly.

| Concept | Consistent across files? | Verified |
|---|---|---|
| Ids | **Yes.** `DC-D` 116 · `AP-D` 68 · `ALT` 11, no duplicates in any namespace, 0 dangling internal references in any of the four files | recomputed |
| `Ri` / `Cf` are **not exits** | **Yes.** §2.5 definitions and mapping, §3.1 legend with an explicit pack instruction, §9 item 5b, matrix §1 legend, matrix §5 Steps 4 and 7. Counts and outcome bars identical in both files | read and recomputed |
| Class → outcome mapping | **Yes.** §2.5's table is the authority; matrix §5 Step 7 reproduces it exactly on all seven classes | compared field by field |
| `Xc` registration requirement | **Yes.** Stated in §2.5, matrix §3 and AP-D-059 with compatible wording and the **same seven ids** (DC-D-001, 015, 037, 063, 064, 080, 104), and the same refusal to extend the register to make flags resolve | recomputed both directions |
| Composed register = 12 | **Yes.** Four sites agree — §2.4, §11, matrix §3 (12 rows counted), AP-D-059 | rows counted |
| Class 14 | **Yes.** Same trigger, same *migration not remediation* consequence, same class-8 follow-on in §6.2, matrix T-10 and AP-D-059 | read |
| Outcome vocabulary | **Yes.** Closed set of 14; AP-D-059 emits classes 5, 12, 14 and 8 by number and full label, all four defined in §6.2 | extracted and tested |
| Evidence lineage | **Yes.** 116/116 criteria carry ≥1 anti-pattern, ≥1 alternative and a file-qualified `Lineage` field | recomputed |
| `Xr` one-limb meaning | **Wording yes, membership no** — G-H-01 | §9 |
| **Class 13** | **Id, trigger, non-exclusion and graduation trigger: yes. Comparative content: no** — G-M-01 | §5 |

**Why this gate fails.** Gate 5's standard is *"FAIL for semantic contradictions capable of changing a decision."* G-M-01 is such a contradiction, and it contradicts four things simultaneously:

- **§6.1 rule 1** — *"No outcome class may contain the word 'preferred', 'better', 'cheaper' or 'faster' about a class the corpus has not evaluated."*
- **Class 13's own closing sentence** — *"It asserts no comparison the corpus has not made."*
- **`alternatives.md` ALT-003's note** — class 13 *"asserts nothing comparative about cost, speed, scale or reliability."* ALT-003's own cost section is sharper: *"Not automatically lowest TCO … cheapest where the fit is genuine, most expensive where it is a workaround."*
- **`decision-criteria.md` §11 and matrix §9** — *"Axes on which a preference between candidate classes is evidenced: 1 — DC-D-108 deployment model."*

It changes a decision because it changes what the pack writes down: a candidacy statement becomes a cost preference. On T-01's ALT-001 / ALT-011 branch the emitted sentence recommends a class on grounds the corpus explicitly does not hold.

G-H-01 also sits partly in this gate: §2.5's `Xr` **wording** agrees across `decision-criteria.md` and the matrix, while the **membership** the wording is meant to define does not follow from it, and the divergence propagates into matrix §2.5 and §2.6 rows. It is recorded against Gates 1, 7 and 9 as its primary homes.

**Non-material divergences found and cleared.** Three, none capable of changing a decision:

- **DC-D-055** — the matrix row carries `AP-D-015` against the body's `AP-D-015, AP-D-027`, still reads *"the platform's strongest documented differentiator here"*, and still omits the DC-D-111 precondition. This is R-03, already recorded as open and non-blocking. Independently confirmed as the **only** criterion↔matrix anti-pattern-set divergence in 116 rows.
- **DC-D-002** — the matrix row's alternatives cell omits ALT-004, which the body carries. The criterion's class is `—`; consequence negligible. **New, LOW.**
- **DC-D-116** — the matrix cell states *"none evaluable — `UNKNOWN` in every class including ALT-004"* while the body enumerates ALT-003, 004, 007, 011 with the same `UNKNOWN` qualifier. Compatible in meaning: the cell states the semantics, the body names the classes it applies to. **New, LOW.**

**Blocking findings.** **G-M-01** — decision-changing cross-file contradiction between §6.2 class 13's render template (and `alternatives.md` §8) and §6.1 rule 1, class 13's own closing sentence, ALT-003's note, and §11 / matrix §9's single-evidenced-axis claim.

---

## 8. Gate 6 — Mechanical integrity

**PASS.**

**Evidence inspected.** All four artifacts, parsed programmatically. Every figure below was regenerated from the artifacts by independently written extractors. **No number was taken from any review or repair report.**

| Check | Independent result | Required |
|---|---|---|
| Duplicate `DC-D-*` ids | **0** (116 definitions) | 0 ✓ |
| Duplicate `AP-D-*` ids | **0** (68 definitions) | 0 ✓ |
| Duplicate `ALT-*` ids | **0** (11 definitions) | 0 ✓ |
| Dangling internal `DC-D-*` / `AP-D-*` / `ALT-*` references, all four files | **0 / 0 / 0** | 0 ✓ |
| Dangling canonical references (2,793 resolved) | **0** | 0 ✓ |
| Unresolved ambiguous references | **0** — all 48 apparent misses resolve to a namespace documented in `anti-patterns.md` §1.3, manifest `NB-*`, `anti-patterns.md` §6's `V-D-*`, or the `IA-` qualified forms declared canonical in AP-D-059's Evidence field | 0 ✓ |
| Every criterion body carries a class tag | **116 / 116** | ✓ |
| §3.1 register rows; register ids == body ids | **116**; identical | ✓ |
| Register rows carrying more than one class | **0** | ✓ |
| Matrix §2 rows, one per criterion; duplicates | **116**; **0** | ✓ |
| **body class == register class == matrix class** | **116 / 116 · 0 mismatches** | ✓ |
| Matrix cells asserting a class with no content | **0** | ✓ |
| Class distribution, regenerated from the 116 `PP negative/exit` fields | `Xp` **15** · `Xr` **28** · `Xe` **5** · `Xc` **7** · `Ri` **6** · `Cf` **17** · `—` **38** · sum **116** | ✓ |
| Distribution == published at §2.5, §3, §3.1, §9 items 5/5b, §11, matrix §1, matrix §9 | **all seven sites agree** | ✓ |
| Direct exits (`Xp` + `Xr` + `Xe`) | **48** as published | ✓ |
| Rows that cannot reject the platform (`—` + `Ri` + `Cf`) | **61** as published | ✓ |
| §3 domain table — 12 rows × 9 class columns + totals | **every cell recounted, all correct** | ✓ |
| Blocking classifications `B` · `B*` | **28** · **3** (DC-D-113, 115, 116) | ✓ |
| §5.2's set == the `B` set, both directions | **identical, 0 divergence** | ✓ |
| `G` == §4A.2's criteria, both directions | **28 == 28, 0 divergence**; 116 − 28 = **88** as §4A.1 publishes | ✓ |
| Composed-disqualifier register | **12** rows counted in matrix §3; **12** at §2.4, §11, AP-D-059, matrix §9 | ✓ |
| **`Xc` ↔ register mapping: every `Xc` criterion named in a matrix §3 row** | **7 / 7** | ✓ |
| Outcome classes defined in §6.2 | **14**, numbered 1–14, no gaps, no duplicates | ✓ |
| Criterion ↔ anti-pattern mappings valid; ≥1 per criterion | **116 / 116**; **1** body↔matrix set divergence (DC-D-055 — R-03) | ✓ |
| Criterion ↔ alternative mappings valid; ≥1 per criterion | **116 / 116**; **2** body↔matrix set divergences (DC-D-002, DC-D-116 — both LOW) | ✓ |
| Anti-pattern orphans (defined, cited by no criterion) | **0** | ✓ |
| Alternative orphans | **0** | ✓ |
| Volatility flags `V` | **11** | see §11 |
| Service-limit register (§7.2) | **20** rows, matching its published figure; matrix §4's group of 17 + the 3 separately-listed volatile rows = 20, consistent | ✓ |

**Headline numbers derive from the classifications.** This was the specific thing to test, because it is what H-01 and R-01 were both about. Every published distribution figure was regenerated from the 116 exit fields and matched at all seven of its homes; the domain table was recounted cell by cell; the blocking, alternative-side and composed counts were regenerated and matched in both directions. **No count was found patched.** The exit history `36 → 48 → 54 → 48` is published in §9 item 5 with the test that produced each generation, which is the audit trail that makes the current figure checkable.

**Two published derived counts do not reproduce.** Both are recorded as non-blocking in §11, because no decision behaviour reads them:

- §9 item 8's confidence distribution publishes `HIGH 57 · MEDIUM 56 · LOW 3`. Recounted from the 116 `**Confidence:**` fields: **`HIGH 68 · MEDIUM 46 · LOW 2`**. (R-04, confirmed still open.)
- §7.1 and §9 item 4 say *"ten"* volatile criteria; the register carries `V` on **11** (DC-D-116 is flagged `V` and is absent from §7.1's table, while §7.2 describes it as *"already `V` — §7.1"*). (R-06, confirmed still open.)

**Reasoning.** Gate 6's standard is *"FAIL if mechanical defects can materially corrupt interpretation or downstream authoring."* Every invariant a pack would actually read — ids, class tags, the three-way class agreement, the blocking set, the `Xc` register, the criterion↔anti-pattern↔alternative mappings, the closed outcome set — is clean. The two count discrepancies are prose figures that no mapping or emission depends on. G-H-01 is a defect in a *classification*, not in the mechanics that carry it; the mechanics faithfully propagate the wrong class to all three representations, which is why it had to be caught semantically.

**Blocking findings.** None.

---

## 9. Gate 7 — Decision-behaviour regression

**FAIL.**

**Evidence inspected.** Matrix §5's eight-step evaluation order including Step 7 and Step 7a; all sixteen scenarios read in full including every `Criteria triggering` and `**Outcome:**` line; `decision-criteria.md` §6.2's fourteen class triggers; all 28 `Xr` exit fields; matrix §3's twelve composed rows; §4A.2's rows for the criteria under test.

**Reasoning.** Ten of the twelve required scenarios reason correctly from the evidence and produce an appropriate outcome class without fabricating certainty. Two carry material defects.

| # | Required scenario | Model behaviour | Correct? |
|---|---|---|---|
| 1 | simple departmental application | T-01 → class 1 **or** class 13 naming ALT-003, graduation trigger mandatory, non-exclusion explicit | **Defective** — the class-13 branch emits G-M-01's comparative clause. Correct on the ALT-003 entitlement fact; **unsupported on the ALT-001 / ALT-011 branch the same class admits** |
| 2 | Excel replacement, straightforward workflow | T-02 → class 2, with the class arithmetic stated: one live `Xr` scoped to reporting, one `Ri`, one `Cf`, two criteria not reaching their exit states | **Yes.** Verified against the criterion bodies — DC-D-026's exit is at `ADMINISTRATOR-EXCLUDED` and this scenario is `FIELD`; DC-D-023's requires *"no server-side shaping option"* and shaping is available |
| 3 | high-volume integration | T-05 → class 3, falling back to class 2 whose named condition is the corpus's *"single platform + a tripwire, not a paper hybrid"*, with the forcing metric recorded as the tripwire | **Yes.** The fallback is correctly a conditioned fit, not a terminal |
| 4 | strict low-latency workload | T-07 → class 5 on `Xp` exits at DC-D-084 / DC-D-042, over-determined → class 8 naming ALT-005, 006, 007, unranked | **Yes** |
| 5 | citizen-developed → enterprise-critical | T-10 → class 12 → class 14 → class 8, with the composed row's own mechanisms named and *"strongest candidate means first to assess, not chosen"* | **Yes.** Power Platform *rebuilt* correctly stays in the candidate set |
| 6 | mission-critical workload | T-09 → class 12 on DC-D-100 and DC-D-091 → then class 2 for the dispatch experience or class 6 for the recovery commitment → class 8, with NB-07 carried so *"the candidate set is a set of things to assess, not a ranking"* | **Yes** |
| 7 | capability owned by an incumbent platform | T-12 → class 6 → class 8 naming ALT-007, 001, 011 with `INCUMBENT FIT UNEVALUATED` carried explicitly; class 4 where the incumbent keeps authority | **Yes.** The platform team's lead time is recorded as a constraint, explicitly not as a justification for bypassing them (AP-D-027) |
| 8 | custom development may be a candidate | T-13 → class 5 for the consumer surface on four independent `Xp` exits plus an `Xe` → class 8 naming ALT-005 as *"realistically the only class in scope, which is scope narrowing, not evaluation"* | **Yes.** Power Platform remains a legitimate candidate for the internal operations behind it |
| 9 | Power Platform economics unattractive | T-14 → class 7 on `Xe` exits → class 8 with six candidates, none priced | **Yes.** *"The model states that this option is expensive for this demand shape. It states nothing whatever about what the others cost."* |
| 10 | insufficient evidence to decide | T-15 → class 12, with a named evidence task per blocking criterion, an owner, and the outcome each resolution would produce | **Yes.** The highest-value four questions are ranked by decision impact, which is what makes the evidence task fundable |
| 11 | conversational assistant over enterprise data | T-16 → class 12 on the commercial and governance model | **Yes.** And the distinction the model must hold is stated: *"a `—` on DC-D-018 means the corpus looked and found no exit; a `—` on DC-D-116 means the corpus never looked."* Absence of an exit is correctly not treated as evidence of fit |
| 12 | task-completing agent handling sensitive data | DC-D-116 at `TASK-COMPLETING AGENT` → `B*` blocks the commercial and governance model; DC-D-058 sensitivity, DC-D-068 identity, DC-D-093 entitlement, DC-D-095 consumption all engaged; T-16 covers this shape | **Yes.** Blocks rather than guesses, on three separable grounds |

**Specific behaviours the gate asked to be tested.** Exclusions: sound and over-determined in the clear cases. Partial responsibility: §6.4's per-scope rule licenses the two-class emission T-06 needs (class 2 for the application, class 3 for the analytical responsibility). Decision blocking: reachable from seven scenarios, and correctly names the outcome each resolution would produce. Comparator-evidence absence: carried into every class-8 terminal. Volatile limits: §7.2's register plus §7.3's rule — *"a figure inside a `Decision impact` field is exclusion evidence with a shelf life, never a permanent decision rule"* — and §2.3's verified property that **no published figure is a state name**. Security/governance interactions: matrix §3 rows 3 and 6 and Block D row 3. Cost/scale interactions: T-14, DC-D-010's `Xe`, matrix §5 Step 6's rule that *"an option that is unavailable cannot be made available by being cheap."*

**Where the model regresses.** The failure is not in the scenarios — all sixteen are substantively right — but in the **rule the scenarios do not reach**. That is the dangerous direction, because a pack implements the rules, not the worked examples. This gate applied §2.5's own decisive test to all 28 `Xr` criteria and constructed the two adjacent cases the rule governs and no scenario exercises.

**A-01 — a multi-month approval process** (capital-expenditure approval routinely running 90–120 days with human waits; departmental ownership; no named operator).

- DC-D-049 at `BEYOND 30 DAYS`, classed **`Xr`**.
- §2.5's mapping and matrix §5 Step 7 both send `Xr` → classes **3, 4 or 6**.
- Class 3's trigger names *duration* as a qualifying bounded excess **and** requires DC-D-070 / DC-D-110 / DC-D-073 / DC-D-083 / DC-D-104 all satisfied. No operator → class 3 unavailable. Class 4 needs an integration or authority responsibility → not this.
- Class 6's trigger then fires by its own words: *"An `Xr` exit fires and no in-scope hybrid shape is available."*
- **Emitted: `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` → class 8.**
- **The criterion's own documented answer:** *"the state must live in a business record with a re-triggering automation (**a legitimate in-platform pattern**), or move to a durable orchestrator"* — needing no operator and no external component.
- **Correct emission under §2.5's own test:** DC-D-049 as `Ri` → class 2 `FIT WITH CONSTRAINTS`, the state-record pattern as the named constraint.

It is worse than a neutral misclassification. DC-D-049's own §4A.2 rows record the off-platform candidates as **`CONSTRAINED` on the very axis that triggered the exit** — ALT-005 at *"a 230-second maximum HTTP response on every plan"*, ALT-006 at *"a stateless choice silently shrinks the envelope to a 5-minute run duration"*. The classification points the decision at alternatives the corpus documents as worse on the triggering axis, and away from the in-platform pattern it documents as legitimate. Multi-month approval processes are a common engagement shape, and the operator-poor case is where the in-platform answer matters most.

**A-02 — per-user backend authorization through a mediation tier** (the target system enforces per-user rules; a facade tier is on the path; identity propagation through it is unavailable).

- DC-D-068 at `TARGET ENFORCES PER USER`, classed **`Xr`** → classes 3/4/6, so class 6 is reachable.
- The exit field reads: *"the pattern is unsuitable unless identity is propagated; where propagation is impossible, **the option changes**."* **No off-platform destination is named anywhere in the criterion** — not in the exit field, not in `Decision impact`, not in `Why it matters`. Every documented consequence is an in-platform design constraint.
- DC-D-068 **is** a registered composed criterion: matrix §3 row 6, *"Per-user backend authorization + a facade or worker calling downstream as a shared identity | DC-D-068, 036, 060"*, whose Class is **`DECISION CRITERION`** — neither an exclusion nor a block. Its own body calls it *"one of the corpus's composed disqualifiers unless identity is propagated"*, which is §2.5's `Xc` definition verbatim, and it satisfies V2's registration requirement.
- **Correct emission:** class 2 with identity propagation as the named condition, or class 12 where propagation feasibility is `UNKNOWN`.

**The pair test is decisive, and it is the test that created this taxonomy.** DC-D-025, which Repair V2 moved to `Ri`, and DC-D-049, which it left at `Xr`, are structurally identical and classed in opposite directions on the same reasoning:

| | DC-D-025 → `Ri` | DC-D-049 → `Xr` |
|---|---|---|
| At a named state | the in-platform store becomes unavailable | the in-platform run mechanism becomes unavailable |
| Documented answer | file storage or the document store with a reference | a business record with a re-triggering automation |
| Off-platform limb also present | **yes** — *"An external object store is a design option for the same redirect"* | **yes** — *"or move to a durable orchestrator"* |
| Treatment of that limb | *"a design option … not a documented exit"* → `Ri` | treated as the exit → `Xr` |

This is precisely the DC-D-039 / DC-D-040 defect that §2.5 was written to eliminate, reproduced one generation later by the repair itself. DC-D-049's field states the case against its own class in terms: *"**not necessarily for the platform**, since the state-record pattern stays in-platform."*

**Neither DC-D-049 nor DC-D-068 appears in any of the sixteen scenarios** — confirmed by scanning every `Criteria triggering` line — which is how the defect survived three review generations.

**Correct classification returns `Xr` 26, `Ri` 7, `Xc` 8, direct exits 46.**

**Blocking findings.** **G-H-01** — false platform exclusion reachable on two criteria whose documented answer is in-platform.

---

## 10. Gate 8 — Downstream authoring safety

**FAIL.**

**Evidence inspected.** All four artifacts read as authoring inputs. `decision-criteria.md` §10 and §9 item 7a; `alternatives.md` §8; `anti-patterns.md` §8; matrix §8 and §9 — the three *"implications for the aisa knowledge model"* sections, which are where each file states what a pack should take from it.

**Reasoning.** The question is whether a defect in Block D could systematically teach the pack the wrong behaviour. Checking each named risk:

| Risk | Verdict |
|---|---|
| vendor advocacy disguised as criteria | **Absent.** §2.2 makes neutrality an inclusion test; §9 item 7 identifies the only four criteria naming estate (DC-D-109, 110, 111, 114) and correctly classifies them as current-state statements the Discovery rule permits. All other 112 are expressible without naming a vendor or product |
| hard-coded volatile limits | **Handled, and this is one of Block D's better repairs.** §7.2's 20-criterion service-limit register plus §7.3's rule that a pack encodes *"the question and the boundary shape, not the number"*. §2.3's verified property that **no published figure is a state name** is what makes it survivable: revalidating a limit changes one sentence, not a taxonomy |
| unsupported architectural preferences | **Absent from the exclusion paths.** Every exclusion terminal routes to class 8 with comparative fit `UNEVALUATED`. **Present in class 13's render template** — G-M-01 |
| licensing claims treated as permanent | **Absent.** §7.1's commercial register with per-criterion re-verify triggers; DC-D-093's own note that general documentation is not authoritative on licensing; DC-D-113 and DC-D-115 blocking on named scopes |
| missing governance / security coupling | **Present and explicit.** Matrix §3 row 3 couples private-network and key-control requirements to unfunded licence populations; row 6 couples per-user authorization to shared-identity intermediaries; Block D row 3 couples citizen artefacts to criticality and entitlement. Both zero-exit domains contribute registered composed rows |
| missing operational consequences | **Present.** Operations domain; DC-D-070 / 073 / 104 as availability gates that make options *unavailable rather than worse*; AP-D-026's operator gate; every anti-pattern carries a `Consequences` field spanning business, architecture, cost and governance |
| **false comparator certainty** | **PRESENT — G-M-01.** The one place it reaches a machine-readable string |
| criteria collapsing independent decisions into one unsafe rule | **Handled** by §3.2's four near-duplicate clusters with a binding elicitation rule and a stated authority per dimension, and by §2.4's refusal to build a scoring model — *"a weighted average of eight CONDITIONALs would pass an option the corpus says is unavailable"* |

**Why this gate fails.** Both gate-blocking findings would be encoded, and each teaches a different wrong behaviour:

1. **G-M-01 teaches false comparator certainty at the output boundary.** A render template is the artefact an authoring process copies most directly into a decision tree's terminal. The clause is unconditioned, so every ALT-001 and ALT-011 emission of class 13 would carry a cost preference the corpus does not hold. The pack would then contain, in its own terminal vocabulary, exactly the claim `alternatives.md` §2.2 lists as forbidden and §8 warns is *"exactly the sentences a pack most easily reintroduces"*. That warning is being borne out inside Block D itself.

2. **G-H-01 teaches a false platform exclusion.** A pack authoring its decision tree from §2.5's register and mapping — which §10 and matrix §1 both direct it to do — would inherit `Xr` for DC-D-049 and DC-D-068 and route both to class 6. The result is a pack that recommends leaving the platform for a multi-month approval process and for an in-platform authorization design constraint, in both cases against the corpus's own documented answer, and in DC-D-049's case toward alternatives the corpus documents as constrained on the triggering axis. Because the mechanics are clean, the wrong class propagates consistently to all three representations — the register, the domain table and the matrix rows — so no consistency check downstream would catch it.

**One prerequisite is correctly identified and must not be lost.** §9 item 7a records that Block D's pack-local vocabulary — *"the governed relational store"*, *"the task-focused surface"*, *"the record-centric surface"*, *"the external-site surface"*, *"the document/list store"*, *"the team-hosted surface"* — is used consistently across all four files and never slips into product names, but that **the mapping to product names is nowhere written down**. Block D correctly declines to author that glossary, since the Options phase is where the mapping is permitted to exist. It is a **prerequisite for authoring, not an optional extra**: this material is not usable until the glossary is written. That is not a Block D defect and does not affect this verdict, but it is the first thing authoring will need.

**Blocking findings.** **G-H-01** and **G-M-01**.

---

## 11. Remaining non-blocking findings

Recorded as technical debt for later authoring or refinement. None of these caused the FAIL, and none should be treated as a reason to delay a Repair V3 focused on the two blocking findings.

### New findings raised by this gate

| Id | Severity | Gate-blocking | Finding |
|---|---|---|---|
| **G-M-02** | MEDIUM | **No** | **§2.5's `Xc` → outcome mapping is indeterminate, and in one case wrong, for 3 of the 12 registered composed rows.** §2.5 maps `Xc` to *"5 or 12, only via its registered §3 row; 14 where the row concludes in-place remediation is unavailable"*, and AP-D-059 restates the same three. But matrix §3's rows carry their own consequence vocabulary inherited from `architecture-patterns.md` §13, and three rows containing `Xc` criteria do not map onto {5, 12, 14}: **row 3** (`CONSTRAINT` — *"incompatible"*; DC-D-063, DC-D-064), **row 4** (`RISK` — *"cannot be evidenced"*; DC-D-001, DC-D-080), and **Block D row 1** (DC-D-001 vs DC-D-104), whose consequence is *"**The commitment cannot be delivered in any architecture**; the gap is a sponsor decision, not a design one"*. The last is the material one: that finding is **platform-independent**, and the nearest available class under the mapping — class 5 `POWER PLATFORM — POOR FIT` — would render a platform-specific rejection for a conclusion that rejects no platform. Class 10 or 11 (the non-technology outcomes) or class 12 pending a funded plan is the honest reading, and neither is reachable under §2.5's mapping. Rated non-blocking because the row's own text (*"not a design one"*, AP-D-053/054's remediation-flavoured decision impacts) steers a careful reader toward class 12, so the unsafe branch is plausible rather than confirmed. **It must nonetheless be settled in the same repair pass as G-H-01**, because reclassifying DC-D-068 → `Xc` makes row 6 (`DECISION CRITERION`) live and forces exactly this mapping decision |
| **G-L-01** | LOW | No | Two body↔matrix alternative-set divergences. DC-D-002's matrix row omits ALT-004, which the body carries (class `—`, consequence negligible). DC-D-116's matrix cell states *"none evaluable — `UNKNOWN` in every class including ALT-004"* while the body enumerates the four classes with the same qualifier — compatible in meaning, divergent as sets. Neither can change a decision |
| **G-L-02** | LOW | No | Stale status footers. `decision-criteria.md` §11 and `alternatives.md` §9 both close with *"**Re-review V2 not yet performed.**"* Re-Review V2 was completed 2026-09-03. A canonicalisation candidate should carry an accurate review-status line |

### Findings confirmed still open from prior generations

All independently re-verified against the artifacts rather than accepted from the reports.

| Id | Severity | Confirmed how | Status |
|---|---|---|---|
| **R-03** | MEDIUM, non-blocking | Recomputed: **1** criterion↔matrix anti-pattern-set divergence in 116 rows, at DC-D-055. The matrix row still reads *"the platform's strongest documented differentiator here"*, still carries `AP-D-015` against the body's `AP-D-015, AP-D-027`, and still omits the DC-D-111 precondition that was the substance of the M-06 repair | Open. DC-D-055's class is `—`; no outcome depends on it. Worth fixing in the same pass — it is a comparative superlative in the column matrix §1 governs with an explicit phrasing rule |
| **R-04** | MEDIUM, non-blocking | Recounted from all 116 `**Confidence:**` fields: **HIGH 68 · MEDIUM 46 · LOW 2** against §9 item 8's published `HIGH 57 · MEDIUM 56 · LOW 3`. Item 8's parenthetical also names three LOW criteria while describing DC-D-102 as MEDIUM-HIGH | Open. No decision behaviour reads the confidence distribution. It does falsify the claim that *every* derived count was regenerated |
| **R-06** | LOW–MEDIUM, non-blocking | Recomputed `V` = **11**; §7.1's table carries **10** rows and §9 item 4 says *"ten"*. DC-D-116 is flagged `V` in the register, is absent from §7.1's table, and §7.2 describes it as *"already `V` — §7.1"* | Open. The register is authoritative and correct; the prose count is off by one |
| **V2-M-02** | MEDIUM, non-blocking | DC-D-046 → `Ri` is contestable on its own evidence: the documented remedy is a gateway *"acting as a facade to the backend services"* that *"adds an extra service that you must manage and maintain"*, which reads as the external component matrix §3 row 2 and AP-D-026 gate. `Ri`'s mapping bars classes 3 and 4, foreclosing the class-3 hybrid the criterion's own evidence documents | Open, and **correctly disclosed** by Repair V2 at §1.4 with its counterfactual (direct exits 49). Mitigated because §3 row 2's operator gate runs from its own criteria under Step 4, so the gate is not bypassed |
| **V2-L-01** | LOW | Confirmed by reading all 28 `Xr` fields: DC-D-013 (*"either change surface or change the requirement"*) and DC-D-023 (*"the interactive read surface must move"*) name only in-platform changes in the exit field, while their class rests on an off-platform limb stated only in `Decision impact`. Supportable under §2.5's broadest-scope rule; the field text fails §2.5's decisive test. Marginally, DC-D-057 and DC-D-062 name no destination either, though §2.5's own example list was drawn from them | Open |
| **V2-L-02** | LOW | Confirmed: abbreviated outcome forms are emitted (`DECISION BLOCKED`, `FIT WITH CONSTRAINTS` without class number or full label) against matrix §9's claim that *"every label emitted in this file appears there verbatim"*. Each maps to exactly one class, so nothing is semantically off-set | Open. Either emit labels in full or drop the *"verbatim"* claim |
| Areas 1–12 lineage defects | recorded, not repaired | `licensing-cost.md`'s duplicate `DC-14` and `integration-architecture.md` §15.8's dangling citation remain, correctly recorded at `anti-patterns.md` §1.4 and `decision-criteria.md` §1.1 / §8.2 and correctly **not** repaired by Block D | Open by design. Downstream must disambiguate `licensing-cost.md DC-14` by its question text, never by its number |
| Research commissions | not defects | `alternatives.md` §6's ten comparative evidence gaps, of which item 9 (agent/Copilot Studio fit — evaluable in no class) and item 10 (document generation — absent from all twelve canonical files) are the two that bound what a pack can conclude | Correctly scoped as upstream commissions, not Block D defects |

---

## 12. Final promotion decision

**FAIL. Block D may not proceed to canonicalisation.**

Two gate-blocking findings remain in the artifacts, both independently confirmed by this gate rather than inherited from the review chain:

- **G-H-01 — HIGH.** §2.5's repaired one-limb `Xr` test was not applied to the whole `Xr` class. DC-D-049 and DC-D-068 remain `Xr` on fields that name nothing leaving the platform, and both route through §2.5's mapping and matrix §5 Step 7 to §6.2 class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` where the corpus documents an in-platform answer. DC-D-049 against DC-D-025 is a structurally identical pair classed in opposite directions — the exact defect shape the taxonomy exists to prevent. No scenario covers either criterion.

- **G-M-01 — MEDIUM, gate-blocking.** §6.2 class 13's render template carries the unconditioned clause *"and is the cheaper or lighter option"* outside its `ALT-NNN` substitution slot, emitting a cost preference for ALT-001 and ALT-011, which the corpus prices nowhere. It contradicts §6.1 rule 1, class 13's own closing sentence, `alternatives.md` ALT-003's note, and §11 / matrix §9's single-evidenced-axis claim. `alternatives.md` §8's *"is the lighter answer"* has the same shape.

**Both errors are narrow, and they point in opposite directions.** G-H-01 is *anti*-platform — a false exclusion on a common engagement shape. G-M-01 is *pro*-alternative — an unsupported preference on the commonest departmental shape. Neither direction is safe, and both land in the machine-readable artefacts an authoring process consumes most directly.

**What this verdict is not.** It is not a judgement on the quality of the work. Block D's evidence discipline is the strongest part of this corpus: `COMPARATOR EVIDENCE ABSENT` as a governing default on 88 criteria against 28 with evidence and exactly **1** axis supporting a preference; a `CONFLICTED` value held open at 20× and marked decision-blocking rather than resolved; an exit taxonomy that **shrank** under scrutiny from 54 to 48 by refusing to call an in-platform redirect an exit; a mitigation withdrawn rather than left claimed-and-unimplemented; and 116 criteria whose classes agree three ways with zero mismatches. Evidence integrity, decision-model completeness and mechanical integrity all pass on independent recomputation.

The material is one bounded repair away from promotion, and it has been for one generation.

### Smallest bounded repair scope required

**Repair V3 — three items. This gate performed none of them.**

1. **G-H-01.** Re-derive the `Xr` membership from §2.5's repaired one-limb test over **all 28** criteria rather than over the criteria a prior review named. On the evidence read here that reclassifies **DC-D-049 → `Ri`** (its documented answer is the in-platform state-record pattern; the durable-orchestrator limb is a design option, which is exactly how Repair V2 treated DC-D-025's external object store) and **DC-D-068 → `Xc`** (no off-platform destination anywhere in the criterion, and it is named in matrix §3 row 6, satisfying V2's own registration requirement). Then republish the derived counts — `Xr` **26**, `Ri` **7**, `Xc` **8**, **direct exits 46** — in all seven homes (§2.5 distribution, §3 domain table Automation and Security rows, §3.1, §9 items 5 and 5b, §11, matrix §1 legend, matrix §2.5/§2.6 rows, matrix §9), and **re-run the pair test across the whole class** so a DC-D-025 / DC-D-049 split cannot recur. Tighten §2.5's classification rule to state which limb governs when a field reaches both an in-platform answer and an off-platform option — that ambiguity is what produced the split.

2. **G-M-01.** Move class 13's comparative clause **inside** the substitution slot, or scope it explicitly to ALT-003, so the emitted string cannot assert a cost preference about ALT-001 or ALT-011. Align `alternatives.md` §8's *"is the lighter answer"* the same way. Then run the check §6.1 rule 1 implies and no generation has yet run: **no outcome class and no render template contains a comparative word about a class the corpus has not evaluated.**

3. **G-M-02, forced by item 1.** State the `Xc` → outcome mapping per registered row rather than as a global {5, 12, 14}. Reclassifying DC-D-068 to `Xc` makes matrix §3 row 6 (`DECISION CRITERION`) the first live row with no mapped class, and rows 3 (`CONSTRAINT`), 4 (`RISK`) and Block D row 1 are already in that position. Block D row 1 additionally needs a class outside {5, 12, 14}, because *"cannot be delivered in any architecture"* is not a platform exclusion.

**Recommended to fold in, cheap and already diagnosed:** R-03 (scope DC-D-055's matrix positive cell as the body does, add the DC-D-111 precondition, add AP-D-027 to the row), R-04 (republish the confidence distribution as 68 / 46 / 2 and add it to whatever check regenerates the other counts), R-06 (reconcile `V` = 11 against §7.1's *"ten"*, either by adding DC-D-116's row to §7.1 or by correcting the prose), and G-L-02 (update both status footers).

**Then re-review V3 against this gate's two blocking findings only**, and re-run the gate. Nothing in Gates 2, 4 or 6 needs re-establishing unless Repair V3 changes what they measured — and item 1 does change the class distribution, so Gate 6's distribution checks and Gate 7's A-01 / A-02 must both be re-run.

---

`BLOCK D GATE: FAIL`
`CRITICAL FINDINGS: 0`
`HIGH FINDINGS: 1`
`GATE-BLOCKING MEDIUM FINDINGS: 1`
`EVIDENCE INTEGRITY: PASS`
`TECHNOLOGY NEUTRALITY: FAIL`
`MECHANICAL INTEGRITY: PASS`
`DECISION MODEL REGRESSION: FAIL`
`DOWNSTREAM AUTHORING SAFETY: FAIL`
`READY FOR BLOCK D CANONICALIZATION: NO`

---

**Not performed, by instruction:** any repair of Block D · canonicalisation of Block D · PP pack authoring · any new research · any modification of any Block D file · any modification of Areas 1–12 · any reopening of Areas 1–12 for general review.
