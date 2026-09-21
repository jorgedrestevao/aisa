Re-Review Status: COMPLETE
Re-review date: **2026-09-03**
Scope: **bounded re-review V2 — the remaining HIGH finding, the remaining gate-blocking MEDIUM finding, the regression they caused, and the cross-file invariants and derived counts those two touch.** Not a new full Block D review. No new research. No Block D file modified. No gate. No canonicalisation. No pack authoring.
Authority reviewed: `research/pp/evidence/block-d-repair-v2-report.md` (verdict `READY FOR BLOCK D RE-REVIEW V2: YES`).
Prior failed review: `research/pp/evidence/block-d-re-review.md` (verdict `FAIL` — HIGH 1, gate-blocking MEDIUM 1, `DECISION MODEL REGRESSION: FAIL`).

# Block D Bounded Re-Review V2

## 1. Method and independence

The repair report's conclusions were **not accepted**. Every count, classification and closure claim below was regenerated from the repaired files by an independently written extractor, then read semantically against §2.5's own tests and against the canonical Areas 1–12 text each repair cites.

| Step | What was done |
|---|---|
| Classification | Extracted the class tag from all 116 `**PP negative/exit.**` fields, all 116 §3.1 register rows and all 116 matrix §2 rows, independently, and compared three ways |
| Semantic test | Read all 28 `Xr`, all 6 `Ri` and the 7 `Xc` fields in full, and applied §2.5's repaired tests literally, **to the whole class and not only to the criteria the prior re-review named** |
| Registration | Expanded every criterion id in matrix §3's twelve rows (including compressed `DC-D-028, 029, 021` forms) and intersected with the `Xc` set, both directions |
| Closure | Extracted every outcome-shaped string emitted in `decision-intelligence-matrix.md`, `anti-patterns.md` and `alternatives.md`, subtracted the 433 harvested criterion state names, and tested membership in §6.2 |
| Regression | Re-ran T-01, T-02, T-05, T-06, T-10 and the adjacent scenarios; then constructed the two adjacent cases the repaired rule newly governs and no existing scenario exercises |
| Evidence | Verified DC-D-032's restated evidence and class 13's comparative-scope claim verbatim against `data-architecture.md` DA-17/DA-18, `application-architecture.md` AA-50, `licensing-cost.md` LC-U-04, `alternatives.md` ALT-003 |
| Mechanical | Recomputed only the values Repair V2 affected: class distribution, direct exits, domain table, `B` / `B*` / `G`, composed-register size, duplicate ids, dangling references |

**What was deliberately not reopened.** R-03 … R-14 from the prior re-review, except where a V2 edit made one moot. Findings already closed at V1 were not re-litigated unless V2 changed their underlying semantics.

---

## 2. Verification of the remaining HIGH — R-01, exit taxonomy classification unsound

**Verdict: PARTIALLY RESOLVED. The root cause was removed from the definition and not from the membership. Gate-blocking.**

### 2.1 What is genuinely repaired

Five of R-01's five sub-parts were addressed, and four are fully closed.

| Sub-part | Independent result |
|---|---|
| **(a)** four/five criteria classed `Xr` on fields naming nothing leaving | **Closed for the named set.** All six criteria V2 moved (DC-D-006, 021, 025, 030, 046, 088) now read `Ri` in body, register and matrix, and every one of the six fields states explicitly that nothing leaves — *"a store change, not a platform change"*, *"not a platform change"*, *"a store, model or surface change, not a platform change"*. Verified by reading all six fields in full |
| **(b)** the `Xr` → outcome mapping contradicted by T-02 | **Closed.** §2.5 now carries an explicit class → outcome mapping table; `Ri` → class 2 or 13, and **never** classes 3, 4, 5, 6, 7. Matrix §1 and §5 Step 7 reference that table rather than restating it (Step 7 reproduces it exactly: `Xp`→5 · `Xr`→3/4/6 · `Xe`→7 · `Xc`→5/12/14 via its registered row · `Ri`→2 or 13 · `Cf`→none alone · `—`→1 or 2). T-02 and the rule now agree |
| **(c)** ten matrix cells asserting a class with no content | **Closed. Independently recounted: 0 bare cells** (was 10). Matrix §1 now states the requirement as a rule, and a bare `—` is correctly exempt |
| **(d)** 18 of 24 `Xc` criteria absent from the register their class cites | **Closed. 7 of 7 `Xc` criteria are named in a matrix §3 row** — DC-D-001, 015, 037, 063, 064, 080, 104 — verified by expanding all twelve rows independently. The registration requirement is stated in three places with compatible wording (§2.5, matrix §3, AP-D-059). The register stayed at 12 rather than growing to 30, which is the correct refusal |
| **(e)** the stale *"79 dashes"* | **Closed.** Matrix §9 now reads 38, with 61 of 116 as the rows that cannot reject the platform, and carries the correction note |

**Three-way agreement, recomputed independently:**

```
body class == register class == matrix class    116 / 116, 0 mismatches
Xp 15 · Xr 28 · Xe 5 · Xc 7 · Ri 6 · Cf 17 · — 38   = 116
direct exits (Xp+Xr+Xe) = 48
rows that cannot reject the platform (— + Ri + Cf) = 61
bare matrix cells = 0 · duplicate DC-D ids = 0 · register rows = 116 · matrix rows = 116
```

Every published home of these figures agrees: §2.5's distribution table, §3's domain table (all 12 rows × 9 class columns and the totals row recounted cell by cell), §3.1, §9 items 5 and 5b, §11, matrix §1's legend, matrix §9. **No count was found patched.**

### 2.2 What is not repaired — the root cause survives in the membership

R-01's root cause, in the repair report's own words, was *"one class carrying two opposite decision consequences"*. V2 removed the second limb from the **definition**. It did not re-derive the **membership** of `Xr` from the repaired definition. Instead it repaired exactly the set the prior re-review named plus the criteria matching that review's search pattern — `Xr` fields *"whose text opens with a form of 'none'"*. The prior re-review states that method explicitly (§3.1), so the blind spot was inherited rather than introduced.

Applying §2.5's repaired test — *"The field names what leaves the platform. **If nothing leaves the platform, this class does not apply**"* — to all 28 surviving `Xr` criteria returns two that fail it.

#### DC-D-049 — Process elapsed duration · classed `Xr`

| | |
|---|---|
| Exit field | *"[`Xr`] **`BEYOND 30 DAYS` held as a single run is a documented exit** for the run mechanism (**not necessarily for the platform, since the state-record pattern stays in-platform**)."* |
| Matrix cell | *"**[`Xr`]** Beyond 30 days as a single run → **state in a business record**, or a durable orchestrator"* |
| `Decision impact` | *"`BEYOND 30 DAYS` → the state must live in a **business record** with a re-triggering automation (**a legitimate in-platform pattern**), or move to a durable orchestrator."* |

The criterion's own field says nothing necessarily leaves. Its documented primary answer is an in-platform pattern the corpus calls *legitimate*. That is `Ri` by the repaired test — an in-platform mechanism becoming unavailable with a different in-platform choice as the answer.

**The pair test is decisive, and it is the same pair test that created this taxonomy.** Compare DC-D-025, which V2 moved to `Ri`:

| | DC-D-025 → `Ri` | DC-D-049 → `Xr` |
|---|---|---|
| At a named state | the in-platform store becomes unavailable | the in-platform run mechanism becomes unavailable |
| Documented answer | file storage or the document store with a reference | a business record with a re-triggering automation |
| Off-platform limb also present | **yes** — *"An external object store is a design option for the same redirect"* | **yes** — *"or move to a durable orchestrator"* |
| V2's treatment of that limb | *"a design option … **not a documented exit**"* → `Ri` | treated as the exit → `Xr` |

Structurally identical criteria, classed differently on the same reasoning applied in opposite directions. This is precisely the DC-D-039 / DC-D-040 defect that §2.5 was written to eliminate, reproduced one generation later by the repair itself.

**The consequence is the R-01(b) failure mode, unremoved.** §2.5's mapping and matrix §5 Step 7 both send `Xr` → classes 3, 4 or 6. Class 3's trigger names *duration* as a qualifying bounded excess, **and** requires DC-D-070 / DC-D-110 / DC-D-073 / DC-D-083 / DC-D-104 all satisfied. Where no operator exists — the ordinary departmental case — class 3 is unavailable, and class 6's trigger fires by its own words: *"An `Xr` exit fires and no in-scope hybrid shape is available"*. A pack therefore emits **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`** for a process running beyond 30 days whose documented answer is an in-platform business record needing no operator at all.

It is worse than a neutral misclassification, because §4A.2's own DC-D-049 rows record that the off-platform candidates are **CONSTRAINED on this very axis** — ALT-005 at *"a 230-second maximum HTTP response on every plan"*, ALT-006 at *"a stateless choice silently shrinks the envelope to a 5-minute run duration"*. The classification points the decision at alternatives the corpus documents as worse on the axis that triggered it, and away from the in-platform pattern it documents as legitimate.

#### DC-D-068 — Authorization enforcement point · classed `Xr`

| | |
|---|---|
| Exit field | *"[`Xr`] Per-user target authorization **through a shared-identity intermediary** → the pattern is unsuitable unless identity is propagated; where propagation is impossible, **the option changes**."* |
| Matrix cell | *"**[`Xr`]** Per-user target authorization through a shared-identity intermediary → unsuitable unless identity is propagated"* |
| `Decision impact` | *"`TARGET ENFORCES PER USER` → explicit delegated identity, **no shared connection**, and virtualized tables excluded; where a mediation tier is present, identity must be propagated through it."* |

I read the whole body. **No off-platform destination is named anywhere in the criterion** — not in the exit field, not in `Decision impact`, not in `Why it matters`. Every documented consequence is an in-platform design constraint. *"The option changes"* names nothing that leaves.

And DC-D-068 **is a registered composed criterion** — matrix §3 row 6, *"Per-user backend authorization + a facade or worker calling downstream as a shared identity | DC-D-068, 036, 060"*, whose Class is **`DECISION CRITERION`**, not an exclusion. Its own body calls it *"one of the corpus's composed disqualifiers unless identity is propagated"*. That is §2.5's `Xc` definition verbatim — *"No exit from this criterion alone. An exit exists only in a **registered** combination"* — and DC-D-068 satisfies V2's new registration requirement. The class V2 built is the one this criterion needs, and V2 did not apply it here.

As `Xr` the criterion routes to classes 3/4/6 and can emit a platform exclusion; as `Xc` it would route to 5/12/14 **only via row 6**, whose consequence is neither an exclusion nor a block. The correct emission is class 2 with identity propagation as the named condition, or class 12 where propagation feasibility is `UNKNOWN`.

### 2.3 Answers to the five required questions on R-01

| Question | Answer |
|---|---|
| Was the root cause actually removed? | **No — half of it.** The two-limb definition is gone and the class → outcome mapping is now explicit and authoritative. The membership of `Xr` was not re-derived from the repaired definition; it was patched for the criteria the prior review named. Two criteria still carry `Xr` on fields that name nothing leaving the platform |
| Is the correction evidence-backed? | **Yes, for everything it covers.** All six `Ri` reclassifications are readings of Block D's own fields, no canonical claim was re-interpreted, and DC-D-032 — the one criterion whose evidence was restated — is verbatim-traceable (§5.1) |
| Are uncertainty states preserved? | **Yes.** See §5. DC-D-046's tier location is recorded as an open design choice rather than resolved |
| Did it remain technology-neutral? | **Not applicable and not violated** — Block D is the Options-phase layer where naming vendors and products is sanctioned. No first-party product name was introduced into a Discovery-phase artefact |
| Did it create any new contradiction? | **Yes, one, and it is inherited rather than created:** DC-D-025 (`Ri`) against DC-D-049 (`Xr`) on identical structure. The `Xc` registration rule is internally consistent across §2.5, matrix §3 and AP-D-059 |
| Did it alter another decision path unexpectedly? | **One, disclosed:** DC-D-046 → `Ri` forecloses the class-3 hybrid its own evidence documents (§4.3, finding V2-M-02). No `Xp` or `Xe` moved, no criterion moved *into* an exit class, and no scenario's substantive conclusion changed |

**Finding V2-H-01 — HIGH · TAXONOMY / CLASSIFICATION · gate-blocking.** §2.5's repaired one-limb `Xr` test was not applied to the whole `Xr` class. DC-D-049 and DC-D-068 remain `Xr` on fields that name nothing leaving the platform; both consequently route through §2.5's mapping and matrix §5 Step 7 to §6.2 class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`, where the corpus documents an in-platform answer. DC-D-049 against DC-D-025 is a structurally identical pair classed differently — the exact defect shape the taxonomy exists to prevent. Affected: `decision-criteria.md` §2.5 distribution, §3 domain table (Automation and Security rows), §3.1, §9 items 5 and 5b, §11 · `decision-intelligence-matrix.md` §1 legend, §2.5 and §2.6 rows, §9. Correct classification returns `Xr` **26**, `Ri` **7**, `Xc` **8**, direct exits **46**. **Not repaired here, by instruction.**

---

## 3. Verification of the remaining gate-blocking MEDIUM — R-02, outcome set not closed

**Verdict: RESOLVED. The closed set is now genuinely closed, and the two missing terminal shapes exist.**

### 3.1 The classes

Independently extracted from §6.2: **14 classes defined**, numbered 1–14, the twelve V1 numbers unchanged. Class 13 `ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED` and class 14 `IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED` are appended, and the lineage reason for appending rather than inserting is stated and correct — AP-D-003, AP-D-035, AP-D-059, AP-D-061 and eight matrix scenarios cite the twelve by number.

Class 8's antecedent was widened to *"classes 5, 6, 7 and 14, and for class 13 where the alternative's sufficiency is not documented"*. That is exactly what T-10 needed and could not have under the V1 definition. Verified in the class-8 cell itself, not only in the repair report.

### 3.2 Closure, tested rather than read

§6.2 now states closure as a check: *"every outcome string emitted anywhere in `anti-patterns.md` or `decision-intelligence-matrix.md` must appear verbatim in the table below."* Matrix §5 Step 7 carries the same instruction at the point of writing. AP-D-059 carries *"and from nowhere else"*.

I ran the check independently. Every outcome-shaped string in the three emitting files was extracted, 433 harvested criterion state names subtracted, and the remainder tested for §6.2 membership.

| Emitted string not in §6.2 | Sites | Verdict |
|---|---|---|
| `COLLABORATION-PLATFORM NATIVE` | matrix 381, 629 | **Legitimate** — both are withdrawal/correction context, verified by reading both lines |
| `CUSTOM DEVELOPMENT PREFERRED`, `EXISTING ENTERPRISE PLATFORM PREFERRED`, `CUSTOM/ENTERPRISE PLATFORM PREFERRED`, `POWER PLATFORM IS ECONOMICALLY UNATTRACTIVE` | matrix 466, 536, 614–621 | **Legitimate** — every site is a *"Renamed 2026-09-03 from …"* retirement note or a §7 before/after row. Verified by reading 466, 536 and 550 in full: each emits a defined class and names the retired label only as the thing it replaced |
| `single platform + a tripwire` | matrix 438 (T-05), §6.2 note, §6.3 withdrawal row | **Legitimate** — retained as class 2's *condition wording*, sourced to `automation-architecture.md` AT2-53, never as a terminal |
| `INCUMBENT FIT UNEVALUATED`, `COMPARATOR EVIDENCE ABSENT` | several | **Legitimate** — markers, not outcome classes; defined in §4A.1 and carried into classes 4 and 8 |
| `POOR FIT` | `anti-patterns.md` 497 | **Legitimate** — a citation of `architecture-patterns.md` §13's own consequence vocabulary, not an emission |
| `DECISION BLOCKED` (short), `FIT WITH CONSTRAINTS` (short), `POWER PLATFORM + … HYBRID`, `DEPLOYMENT MODEL EXCLUDES THIS PLATFORM` (short) | matrix 46, 91, 410, 424, 480, 494 and others; `anti-patterns.md` 539, 1498 | **Abbreviated forms of defined classes** — finding V2-L-02 below. Not off-set semantically; each maps to exactly one class, and the `anti-patterns.md` sites carry the class number |

**No emitted label sits outside the set.** The two labels that caused R-02 appear only in explanatory and withdrawal context. §6.3 gained the two withdrawal rows, and the second correctly records that *"single platform + a tripwire"* was **not** replaced by a class because it is a condition on a fit.

### 3.3 §6.4's per-scope rule

*"One outcome per scope, not one per engagement"* is now stated, with T-06, T-12 and T-13 named as the instances. This is load-bearing: class 8's widened antecedent depends on it, and it is the rule that stops a bounded `Xr` collapsing into a whole-solution rejection. It was the matrix's actual behaviour and had never been written down. Verified present in §6.4 and exercised in T-06 (class 2 for the application scope **plus** class 3 for the analytical responsibility).

### 3.4 Answers to the five required questions on R-02

| Question | Answer |
|---|---|
| Was the root cause actually removed? | **Yes.** The root cause was the two missing terminal shapes, not the two stray labels. Class 13 carries *"an alternative is the documented answer and Power Platform is not excluded"*; class 14 carries *"cannot be brought to the required class in place, while the same platform rebuilt remains a candidate"*. Both were reachable conclusions with no class |
| Is the correction evidence-backed? | **Yes.** Class 13's anchors verified: AA-50's one-way upgrade *"then premium licences for all users"* read verbatim; `data-architecture.md` §6 and AP-D-008's Exceptions state the four shapes positively; LC-U-04 confirms comparative TCO absent. Class 14's anchors are the evidence already under matrix §3's Block D row 3 — no new claim |
| Are uncertainty states preserved? | **Yes**, and class 13's scope is deliberately narrowed to one class on four shapes, with the widening recorded as an open commission |
| Did it remain technology-neutral? | **Not applicable and not violated** — as above |
| Did it create any new contradiction? | **Yes, one:** class 13's render template contains an unconditioned comparative clause that contradicts §6.1 rule 1, its own closing sentence, `alternatives.md` ALT-003's note, and §11's *"1 evidenced comparative axis"* — finding V2-M-01 |
| Did it alter another decision path unexpectedly? | **No.** T-07, T-12, T-13 and T-14 still reject or displace on the same evidence; class 8 is still reached in the same scenarios; the twelve V1 numbers are unmoved |

**R-02 is closed.** The finding below is a defect in the new class's rendering rule, not a failure to close R-02.

**Finding V2-M-01 — MEDIUM · UNSUPPORTED PREFERENCE / CROSS-FILE · gate-blocking.** §6.2 class 13's render template reads: *"No documented constraint excludes Power Platform. **ALT-NNN** is \<the documented answer for this shape / a candidate\> **and is the cheaper or lighter option**. Graduation trigger: …"*. The comparative clause sits **outside** the substitution slot, so it is emitted for whatever class is substituted — and §6.2's own evidence anchor and `alternatives.md` §8 both permit ALT-001 and ALT-011 in class 13 as candidates. For those two classes the corpus prices nothing (LC-U-04; `alternatives.md` §6 item 3 records that no incumbent and no product is evaluated), so the template emits a cost preference on no evidence. It contradicts four things at once:

- **§6.1 rule 1** — *"No outcome class may contain the word 'preferred', 'better', 'cheaper' or 'faster' about a class the corpus has not evaluated."*
- **class 13's own closing sentence** — *"It asserts no comparison the corpus has not made."*
- **`alternatives.md` ALT-003's V2-added note** — class 13 *"asserts **nothing comparative** about cost, speed, scale or reliability."* ALT-003's own cost section is sharper still: *"**Not** automatically lowest TCO … cheapest where the fit is genuine, most expensive where it is a workaround."*
- **`decision-criteria.md` §11 and matrix §9** — *"Axes on which a preference between candidate classes is evidenced: **1** — DC-D-108 deployment model."*

The intent is documented and correct everywhere it is argued — §6.1's exception rule, T-01's explicit disclaimer, ALT-003's note — and the defect is confined to the one string a pack actually encodes. That is what makes it gate-blocking rather than cosmetic: a render template is the machine-readable artefact, and the brief's named critical test is that a preference must not reach the outcome string. Affected: `decision-criteria.md` §6.2 class 13 · `alternatives.md` §8 (*"is the lighter answer"*, same shape, applied to ALT-001/ALT-011). **Not repaired here, by instruction.**

---

## 4. Regression results

### 4.1 The scenarios that caused `DECISION MODEL REGRESSION: FAIL`

Identified independently from the prior re-review §9 and §11: **T-02** (the counter-example falsifying V1's `Xr` mapping rule, R-01(b)) and **T-01, T-05, T-10** (the closed-set violations, R-02). **T-06** was found by the repair's own adjacency pass and carries both defects. All five re-run against the repaired files, reading the criteria, anti-pattern and alternatives files first and the matrix's stated conclusion afterwards.

| Scenario | Emission now | Independently correct? |
|---|---|---|
| **T-02** Excel replacement | class 2 `FIT WITH CONSTRAINTS`, with the class arithmetic stated — one live `Xr` (DC-D-031, scoped to reporting), one `Ri` (DC-D-030), one `Cf` (DC-D-022), DC-D-023 and DC-D-026 not reaching their exit states | **Yes.** The rule and the scenario now agree, which is the whole point of the repair. Verified against the criterion bodies: DC-D-026's exit is at `ADMINISTRATOR-EXCLUDED` and this scenario is `FIELD`; DC-D-023's is *"with no server-side shaping option"* and shaping is available |
| **T-01** simple departmental app | class 1 **or** class 13 naming ALT-003, graduation trigger mandatory, non-exclusion explicit | **Yes.** Same two branches, same evidence, and the alternative branch now has a terminal a pack cannot be forced to drop |
| **T-05** high-volume integration | class 3, falling back to **class 2** whose named condition is the corpus's *"single platform + a tripwire, not a paper hybrid"*, with the forcing metric recorded as the tripwire | **Yes.** The fallback was always a conditioned fit, never a terminal class |
| **T-06** complex data-centric app | class 2 for the application scope **plus** class 3 for the analytical responsibility (DC-D-031's `Xr`); DC-D-022 stated as `Cf` feeding DC-D-088's `Ri` | **Yes.** §6.4's per-scope rule now licenses the two-class emission. DC-D-032 is listed as triggering but its exit requires `MULTI-YEAR, QUERYABLE` **at volume**, which 12,000 contracts does not reach — correctly not fired |
| **T-10** citizen app → enterprise-owned | class 12 → **class 14** → class 8, with the row's documented mechanisms named, and *"strongest candidate means first to assess, not chosen"* | **Yes.** Same migration-not-remediation conclusion, class 8 no longer unaccompanied, and Power Platform *rebuilt* stays in the candidate set |

**Previously failing scenarios now pass: YES (5 of 5).**

### 4.2 Adjacent scenarios re-checked

T-03, T-04, T-07, T-08, T-09, T-11, T-12, T-13, T-14, T-15, T-16 — **unchanged, verified mechanically.** Every exit these rest on is `Xp`, `Xe` or an `Xr` V2 did not reclassify. The reclassified criteria appear in only two of them, and in both as a `B` blocking flag (T-10's DC-D-006, T-15's DC-D-021), which V2 did not change. All sixteen `**Outcome:**` lines were extracted and read.

### 4.3 Adjacent scenarios the repaired rule newly governs — and which no existing scenario exercises

The brief requires running *"directly adjacent scenarios where the repaired semantic rule could produce a different outcome."* Two such cases follow from V2-H-01. **Neither DC-D-049 nor DC-D-068 appears in any of the sixteen scenarios** — verified by scanning every `Criteria triggering` line — which is exactly how the defect survived.

**A-01 — a multi-month approval process.** Capital-expenditure approval that routinely runs 90–120 days with human waits; departmental ownership; no named operator for an external component.

- DC-D-049 at `BEYOND 30 DAYS`, classed `Xr`.
- §2.5's mapping and matrix §5 Step 7 both send `Xr` → classes 3, 4 or 6.
- Class 3's trigger names *duration* as a qualifying bounded excess **and** requires DC-D-070 / DC-D-110 / DC-D-073 / DC-D-083 / DC-D-104 satisfied. No operator → class 3 unavailable.
- Class 6's trigger then fires by its own words: *"An `Xr` exit fires and no in-scope hybrid shape is available."*
- **Emitted: `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` → class 8.**
- **Documented answer:** *"the state must live in a business record with a re-triggering automation (a legitimate in-platform pattern)"* — needing no operator and no external component.
- **Correct emission under the repaired test:** DC-D-049 as `Ri` → class 2 `FIT WITH CONSTRAINTS`, the state-record pattern as the named constraint.
- This is the R-01(b) failure mode verbatim, on a common engagement shape, in the operator-poor case where the in-platform answer matters most.

**A-02 — per-user backend authorization through a mediation tier.** A workload whose target system enforces per-user rules; a facade tier is on the path; identity propagation through it is not available.

- DC-D-068 at `TARGET ENFORCES PER USER`, classed `Xr` → classes 3/4/6, so class 6 is reachable.
- Nothing in the criterion leaves the platform, and its registered composed row 6's consequence is `DECISION CRITERION` — neither an exclusion nor a block.
- **Correct emission:** class 2 with identity propagation as the named condition, or class 12 where propagation feasibility is `UNKNOWN`.
- As written, the model can emit a platform exclusion for an in-platform authorization design constraint.

### 4.4 The six outcome shapes the brief requires distinguished

All six remain producible and distinct. Verified by reading all sixteen `**Outcome:**` lines.

| Required shape | Class | Scenarios |
|---|---|---|
| viable | 1 | T-01 |
| viable with constraints | 2 | T-02, T-06, T-05 fallback, T-04, T-09 |
| partial / hybrid responsibility | 3, 4, 6 | T-05, T-06, T-08, T-11, T-12, T-04 |
| platform excluded | 5, 6, 7 | T-07, T-13 (5) · T-12 (6) · T-14 (7) |
| alternatives require evaluation | 8 | T-07, T-10, T-12, T-13, T-14 |
| decision blocked pending evidence | 12 | T-03, T-04, T-08, T-09, T-10, T-15, T-16 |
| *(new)* alternative sufficient, platform not excluded | 13 | T-01 |
| *(new)* in-place remediation unavailable | 14 | T-10 |

### 4.5 The critical test — `Power Platform excluded` must not imply `Alternative X preferred`

**Holds on every exclusion terminal.** Every one of the four exclusion emissions is followed by class 8 `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`:

- T-07 → class 5 → class 8: ALT-005, ALT-006, ALT-007, with the retired preference labels named only as what was replaced.
- T-12 → class 6 → class 8: ALT-007, ALT-001, ALT-011, with `INCUMBENT FIT UNEVALUATED` carried explicitly.
- T-13 → class 5 → class 8: ALT-005, *"realistically the only class in scope, which is scope narrowing, not evaluation"*.
- T-14 → class 7 → class 8: six candidates, none priced.
- T-10 → class 14 → class 8, with *"strongest candidate means first to assess, not chosen"*.
- AP-D-059 states the discipline directly: *"the composed test can say the option is unavailable, and it cannot say which surviving class is better."*

**Class 13 does not violate the test in its firing condition.** It fires only where **no exit of any class fires**, which is the opposite configuration from exclusion — `Power Platform excluded` was not converted into `Alternative X preferred` anywhere. The violation is narrower and lives in the render string, not the trigger: see V2-M-01. That is why the critical test passes on the scenarios and the finding is still raised.

### 4.6 Bias check, run in both directions

- **Pro-platform direction.** V2 reduces exits 54 → 48. Every rejecting or displacing scenario was re-tested against the reclassification: T-04, T-07, T-08, T-09, T-12, T-13 and T-14 all rest on exits V2 did not touch, and none softened. T-13 still carries four independent `Xp` exits plus an `Xe`. Power Platform is still rejected, displaced or blocked in the same twelve of sixteen scenarios.
- **Anti-platform direction.** Class 13 removes a structural bias toward the platform that had been arrived at by omission. V2-H-01 leaves an *anti*-platform bias in place on two criteria (§2.2), which is the direction the prior re-review correctly noted is no safer.
- **Artificial comparators.** No scenario gained a claim about an alternative's fitness. T-04's *"the replacement's adequacy is unevidenced"* and T-09's NB-07 note on the candidates are both intact.

**`DECISION MODEL REGRESSION: FAIL`** — not on the scenarios, which all pass, but on the rule the scenarios do not reach. This applies the prior re-review's own standard: T-02 passed substantively while the rule contradicted it, and the regression was rated FAIL because *"the scenarios are right and the rules are wrong — which is the dangerous direction, because a pack implements the rules."* The same condition holds for DC-D-049 and DC-D-068, and no scenario covers either.

---

## 5. Evidence integrity

**PASS.** No uncertainty state was converted into a stronger factual state, silently or otherwise.

### 5.1 The one evidence restatement V2 made — DC-D-032, verified verbatim

V2 restated DC-D-032's exit field on the grounds that its V1 text *"none evidenced; the answer is an archival store"* **understated** its own evidence. I checked every clause of the restatement against `data-architecture.md`.

| DC-D-032's restated claim | Canonical text |
|---|---|
| in-platform long-term retention is `CONDITIONAL` only — managed environment | DA-17: *"must be a Managed Environment … policies are disabled"* otherwise |
| irreversible | DA-17: *"Once data is retained … it can't be moved back to the Dataverse live (active) application state"*; DAP-15 *"irreversible"* |
| no capacity saving for files | DA-17: *"For file and image attachments, Dataverse long term retention doesn't reduce capacity consumed"* |
| retained data no longer surfaced to the analytical shortcuts | DA-17: *"shortcuts include live data only. Retained data is no longer surfaced"* |
| backups are not a retention mechanism | DA-18 / §2 row 12: *"Backups as archive → ≤ 28 days, same region, not downloadable → not a retention mechanism"* |
| the archival responsibility leaves to a lake or archive store; the active record stays | DA-17 Decision impact: *"Managed Env + read-only history … or external archive for attachments-heavy history … take the lake copy before retention"*, against *"M months active"* |

**Every clause traces verbatim. Nothing was moved beyond the canonical text, and the class is correct** — the archival responsibility leaves and the active record stays, which is `Xr` and not `Xp`, exactly as the field now says.

### 5.2 The five states the brief names

| State | Verified after V2 |
|---|---|
| `UNKNOWN` | **Preserved.** Agent economics, capacity, latency and accuracy; broker and streaming sizing (U-13, U-03); comparator portability; incumbent fit; polling intervals; concurrency and amplification figures; GOV-U-06. DC-D-046's tier location is recorded as an open design choice, **not resolved** |
| `CONFLICTED` | **Preserved.** NB-02 intact in the manifest, still 20×, still *"must not be treated as stable sizing limits"*, still *"Do not encode either value"*. DC-D-039 still carries `B V Xr G` in the register and is still decision-blocking; matrix §4 re-verifies both pages by date. DC-D-037 stays `Xc` because it is named in matrix §3 row 5 |
| `VOLATILE VALUE` | **Preserved.** §7.1 and §7.2 untouched; the 20-criterion service-limit register intact, DC-D-049 and DC-D-032 both still in it; `V` count 11 unchanged (R-06, out of scope, confirmed still open against §7.1's *"ten"*) |
| `INF` | **Preserved.** NB-06 intact in the manifest with *"Preserve INF"*; carried in DC-D-036, DC-D-111, ALT-007 and T-12; AP-D-059's composition still MEDIUM confidence with *"the composition is the corpus's own INF synthesis"*; the two Block D composed rows still marked derived |
| `COMPARATOR EVIDENCE ABSENT` | **Preserved as a state.** §4A.1's default on 88 criteria unchanged and reproduced independently (`G` = 28, matched against §4A.2 in **both** directions, 0 divergence); the marker present in all three decision files; LC-U-04 verified still recording comparative TCO as absent; `alternatives.md` §6 item 3 still records that no incumbent and no product is evaluated. **Class 13's exception is argued explicitly at §6.1, bounded to one class on four shapes, and disclaimed in T-01 and in ALT-003's own note — so there is no *silent* conversion.** The overreach is in one render string and is raised as V2-M-01 |
| Manufactured comparator evidence | **None.** No comparative TCO, benchmark, incumbent evaluation or comparator low-code claim was created. Class 13 fires only where nothing is excluded; class 14 keeps ALT-004 in the candidate set |
| Areas 1–12 modified | **No.** Read only. The duplicate `licensing-cost.md` DC-14 and the `integration-architecture.md` §15.8 dangling citation remain recorded and unrepaired, correctly |

---

## 6. Cross-file consistency

The four V2-changed concepts checked across all four files for compatible ids, meanings, exit semantics, blocking semantics, alternative mappings and outcome vocabulary.

| Concept | `decision-criteria.md` | `decision-intelligence-matrix.md` | `anti-patterns.md` | `alternatives.md` | Compatible? |
|---|---|---|---|---|---|
| `Ri` / `Cf` are **not exits** | §2.5 definitions + mapping table; §3.1 legend with the explicit pack instruction; §9 item 5b | §1 legend (`Ri` no, `Cf` no), the three-way misreading warning, §5 Step 4 and Step 7 | — | — | **Yes.** Counts, tests and outcome bars identical in both files |
| `Xr` one-limb meaning | §2.5 *"If nothing leaves the platform, this class does not apply"* | §1 *"leaves the platform"* | — | — | **Wording yes; membership no** — V2-H-01 |
| Class → outcome mapping | §2.5 table (authority) | §5 Step 7 reproduces it exactly; §1 states the `Xr` and `Ri` rules | — | — | **Yes.** Byte-for-byte compatible on all seven classes |
| `Xc` registration requirement | §2.5 | §3 registration rule, seven ids named | AP-D-059 *"§2.5's `Xc` class depends on it"*, same seven ids | — | **Yes.** Same rule, same seven ids, same refusal to extend the register |
| Composed register = 12 | §2.4, §11 | §3 (12 rows counted mechanically), §9 | AP-D-059, §12 summary | — | **Yes.** Four sites, all 12 |
| Class 13 | §6.1 exception rule, §6.2 class 13, §6.3 withdrawal row | T-01, §5 Step 7, §7 before/after | — | ALT-003 outcome-class note, §8 bullet | **Id, trigger, non-exclusion and graduation trigger: yes. Comparative content: no** — V2-M-01 |
| Class 14 | §6.2 class 14, §6.3 | T-10, §7 | AP-D-059 class 5 / class 14 boundary | — | **Yes.** Same trigger (a registered row concluding *cannot be repaired in place*), same *migration not remediation* consequence, same class-8 follow-on |
| Closure as a test | §6.2 | §5 Step 7, §9 | AP-D-059 *"and from nowhere else"* | — | **Yes** in rule; §9's *"verbatim"* claim is overstated — V2-L-02 |
| One outcome per scope | §6.4 | T-06, T-12, T-13 | — | — | **Yes** |

**Outcome vocabulary.** AP-D-059 emits classes 5, 12, 14 and 8 by number and full label, all four in §6.2. Class 8's *"can say the option is unavailable, and cannot say which surviving class is better"* matches §6.1's governing rule and `alternatives.md` §9. No divergent vocabulary found.

**R-03 verified still open, as the repair report states.** Matrix §2.5's DC-D-055 row still reads *"the platform's strongest documented differentiator here"*, still carries only `AP-D-015` against the body's `AP-D-015, AP-D-027`, and still omits the DC-D-111 precondition. It remains the only criterion↔matrix anti-pattern-set divergence in 116 rows. Caused by the M-06 repair, not by R-01 or R-02; DC-D-055's class is `—` and V2 did not touch it. Out of V2's scope and correctly reported as such.

---

## 7. Mechanical checks

Only the values Repair V2 affected were recomputed. **No number was taken from the repair report.**

| Check | Independent result |
|---|---|
| Criterion bodies · **duplicate `DC-D-*` ids** | 116 · **0** |
| Every body carries a class tag | **116 / 116** |
| §3.1 register rows · register ids == body ids | 116 · **identical** |
| Register rows carrying more than one class | **0** |
| Matrix §2 rows, one per criterion · duplicates | 116 · **0** |
| **body class == register class == matrix class** | **116 / 116 · 0 mismatches** |
| Class distribution, regenerated | `Xp` **15** · `Xr` **28** · `Xe` **5** · `Xc` **7** · `Ri` **6** · `Cf` **17** · `—` **38** · sum **116** |
| Distribution == published in §2.5, §3, §3.1, §9, §11, matrix §1, matrix §9 | **all seven sites agree** |
| **Direct exits** | **48** (as published) — **46** under the corrected classification of V2-H-01 |
| Rows that cannot reject the platform | **61** (as published) |
| §3 domain table — 12 rows × 9 class columns + totals | **every cell recounted, all correct** |
| **Affected mappings: every `Xc` criterion named in a matrix §3 row** | **7 / 7** (was 6 of 24) |
| `Xc` set == the seven registered | **DC-D-001, 015, 037, 063, 064, 080, 104** |
| DC-D-080 present in §3 row 4's criteria list | **yes** — row 4 reads DC-D-001, 080, 082, 089, 100 |
| Matrix cells carrying a class marker and no content | **0** (was 10) |
| **Affected blocking counts:** `B` · `B*` | **28** · **3** (DC-D-113, 115, 116) |
| §5.2's set == the `B` set, both directions | **identical, 0 divergence** |
| `G` == §4A.2's criteria, both directions | **28 == 28, 0 divergence** |
| **Affected composed-disqualifier counts** | **12** in matrix §3 (rows counted), AP-D-059, §2.4, §11, matrix §9 |
| Outcome classes defined in §6.2 | **14**, numbered 1–14, no gaps, no duplicates |
| **Dangling affected references** `DC-D-*` / `AP-D-*` / `ALT-*` | **0 / 0 / 0** across all four files |
| Definition counts | `DC-D` **116** · `AP-D` **68** · `ALT` **11**, no duplicates |
| Every criterion names ≥1 anti-pattern, ≥1 alternative, a file-qualified `Lineage` | **116 / 116 / 116** |
| Matrix §9's *"79 dashes"* | **repaired** to 38 / 61, with the correction note |
| §9 items 5 and 5b | **regenerated consistently** (48 / 7 / 6 / 17 / 38) |

**Two repair-report claims that do not reproduce as stated.** Neither changes a published figure.

1. *"37 checks, 37 PASS"* on closure — the check *"every outcome-shaped string emitted in the matrix appears in §6.2"* passes only if abbreviated forms are excluded, which the report's own count of *"34 candidate strings"* implies it did. My extraction finds abbreviated emissions the check did not count (V2-L-02).
2. The report's §4.1 line *"No `Ri`/`Cf` field claims anything leaves the platform"* is correct and reproduces — but the converse check, *every `Xr` field claims something leaves*, was never run, and is where V2-H-01 sits.

---

## 8. Newly introduced defects and findings

| Id | Severity | Gate-blocking | Finding |
|---|---|---|---|
| **V2-H-01** | **HIGH** | **Yes** | R-01's root cause removed from the `Xr` definition but not from its membership. DC-D-049 and DC-D-068 remain `Xr` on fields naming nothing that leaves the platform, and both route to §6.2 class 6 where the corpus documents an in-platform answer. DC-D-049 against DC-D-025 is a structurally identical pair classed differently. Inherited from the prior re-review's search method, not created by V2 — but unresolved. Correct classification: `Xr` 26, `Ri` 7, `Xc` 8, direct exits 46 |
| **V2-M-01** | **MEDIUM** | **Yes** | Class 13's render template carries an unconditioned comparative clause *"and is the cheaper or lighter option"*, emitted for whatever `ALT-NNN` is substituted — including ALT-001 and ALT-011, which the corpus prices nowhere. Contradicts §6.1 rule 1, class 13's own closing sentence, `alternatives.md` ALT-003's note, and §11 / matrix §9's *"1 evidenced comparative axis"*. `alternatives.md` §8's *"is the lighter answer"* has the same shape |
| **V2-M-02** | MEDIUM | No | DC-D-046 → `Ri` is contestable on its own evidence: the documented remedy is a gateway *"acting as a facade to the backend services"* that *"adds an extra service that you must manage and maintain"*, which reads as the external component matrix §3 row 2 and AP-D-026 gate. `Ri`'s mapping bars classes 3 and 4, foreclosing the class-3 hybrid the criterion's own evidence documents. **Disclosed** by the repair at §1.4 with its counterfactual (direct exits 49), and mitigated because §3 row 2's operator gate runs from its own criteria under §5 Step 4, so the gate is not bypassed |
| **V2-L-01** | LOW | No | DC-D-013 and DC-D-023 exit fields name only in-platform changes (*"surface change or requirement change"*, *"surface/store change"*) while their `Xr` class rests on an off-platform limb stated only in `Decision impact` (*"custom web"*, *"a custom-application trigger"*). The class is supportable under §2.5's broadest-scope rule; the field text fails §2.5's decisive test and matrix §1's requirement that *"an `Xp` / `Xr` / `Xe` names what leaves"* |
| **V2-L-02** | LOW | No | Closure claim overstated. Matrix §9 asserts *"every label emitted in this file appears there verbatim"*, but abbreviated forms are emitted — `DECISION BLOCKED` (T-03, T-04, T-08, T-09) and `FIT WITH CONSTRAINTS` (§1) without the class number or full label, and `POWER PLATFORM + … HYBRID` / `DEPLOYMENT MODEL EXCLUDES THIS PLATFORM` in AP-D-059. Each maps to exactly one class and the AP-D-059 sites carry the class number, so nothing is semantically off-set |

**Findings the prior re-review left open and V2 correctly did not touch** — confirmed still open, none gate-blocking, none made worse: R-03 (DC-D-055 matrix row, verified in §6 above), R-04 (confidence distribution), R-05 (matrix §8.2 reference counts), R-06 (`V` = 11 against §7.1's *"ten"*, independently confirmed), R-07 … R-14, and the H-03 / H-04 upstream commissions.

---

## 9. What the repair got right, stated plainly

Recorded because a FAIL verdict on two findings should not obscure the scale of what closed.

- **It repaired the model, not the wording.** `Ri` and `Cf` are real classes with tests, an explicit outcome mapping and a bar on what they may never emit. The `Xc` registration requirement is a *testable* rule in three files, and it closed R-01(d) by refusing to invent eighteen composed rows — the correct choice, stated as such.
- **The exit count went down.** 54 → 48, by declining to call an in-platform redirect an exit. A taxonomy that shrinks under scrutiny is behaving correctly, and §9 item 5 now carries all three generations with the test that produced each.
- **Closure became a test.** §6.2, matrix §5 Step 7 and AP-D-059 all now say that an off-set label is a defect in the emitting file. That is the check whose absence caused R-02.
- **Class 13 fixed a bias arrived at by omission** — the commonest departmental shape in the domain had no terminal, and a pack implementing §6.2 literally would have had to reach for ALT-004.
- **DC-D-032 was restated by strengthening its evidence, not by weakening its class**, and every clause traces verbatim to DA-17 and DA-18.
- **All ten bare matrix cells were filled**, and matrix §1 made it a rule.
- **The boundary was kept.** R-03 … R-14 were not quietly repaired, `library/packs/pp/` is untouched, Areas 1–12 were read and not modified, and the two out-of-scope findings were named rather than left silent.

---

## 10. Required corrections before the gate

Two, both narrow. **Neither was performed here, by instruction.**

1. **V2-H-01.** Re-derive the `Xr` membership from §2.5's repaired one-limb test over all 28 criteria rather than over the criteria the prior review named. On the evidence read here that reclassifies **DC-D-049 → `Ri`** (its documented answer is the in-platform state-record pattern; the durable-orchestrator limb is a design option, which is exactly how V2 treated DC-D-025's external object store) and **DC-D-068 → `Xc`** (no off-platform destination anywhere in the criterion, and it is named in matrix §3 row 6, so it satisfies V2's own registration requirement). Then republish the derived counts — `Xr` **26**, `Ri` **7**, `Xc` **8**, **direct exits 46** — in all seven homes, and re-run the pair test on the whole class so DC-D-025 / DC-D-049 cannot recur. Optionally tighten §2.5's classification rule to say which limb governs when a field reaches both an in-platform answer and an off-platform option, since that ambiguity is what produced the split.
2. **V2-M-01.** Move class 13's comparative clause inside the substitution slot, or scope it to ALT-003 explicitly, so the emitted string cannot assert a cost preference about ALT-001 or ALT-011. Align `alternatives.md` §8's *"is the lighter answer"* the same way. Then re-run the check §6.1 rule 1 implies: **no outcome class or render template contains a comparative word about a class the corpus has not evaluated.**

Optional, not gate-blocking: V2-L-01 (give DC-D-013 and DC-D-023 exit fields the off-platform destination their class rests on) and V2-L-02 (emit outcome labels in full, or drop matrix §9's *"verbatim"* claim).

---

## 11. Verdict

The re-review's two gate-blocking findings did not both close. **R-02 is fully resolved** — the outcome set is genuinely closed, closure is a test rather than a claim, the two missing terminal shapes exist and are evidence-backed, and all five previously failing scenarios pass on defined classes without any substantive conclusion changing. **R-01 is resolved as a definition and unresolved as a membership**: the two-limb `Xr` was replaced by a sound one-limb class with an explicit outcome mapping, and the class's membership was patched for the criteria the prior review happened to name rather than re-derived from the repaired test. Two criteria still carry `Xr` on fields that name nothing leaving the platform, and both reach `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` where the corpus documents an in-platform answer.

The direction of the surviving error is *anti*-platform, which does not make it safe: a false exclusion on a multi-month approval process is a wrong architecture recommendation on a common engagement, and no scenario covers it. Evidence integrity is strong throughout — the one restated evidence claim traces verbatim, and every uncertainty state the brief names survives intact.

`BLOCK D RE-REVIEW V2: FAIL`
`CRITICAL FINDINGS: 0`
`HIGH FINDINGS: 1`
`GATE-BLOCKING MEDIUM FINDINGS: 1`
`EVIDENCE INTEGRITY: PASS`
`DECISION MODEL REGRESSION: FAIL`
`READY FOR BLOCK D GATE: NO`

---

**Not performed, by instruction:** the Block D Gate · canonicalisation of Block D · PP pack authoring · any new research · any modification of Block D files · any repair of the findings above · any reopening of findings closed at V1 whose semantics V2 did not change.
