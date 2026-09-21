Recheck Status: COMPLETE
Recheck date: **2026-09-03**
Scope: **final bounded gate recheck — verification of `block-d-gate-repair-report.md`'s seven closure claims, and nothing else.** Not a new Block D gate. No new research. No repair. No canonicalisation. No PP pack authoring. No file modified except this report. Areas 1–12 consulted for lineage verification on the repaired rules only.
Authority rechecked against: `research/pp/evidence/block-d-gate.md` (`BLOCK D GATE: FAIL`) and `research/pp/evidence/block-d-gate-repair-report.md` (`READY FOR FINAL BOUNDED GATE RECHECK: YES`).

# Block D Final Bounded Gate Recheck

## 1. Recheck scope

**PASS.** Every claim in the repair report was re-derived from the artifacts. No number below is quoted from the repair report, the gate, or any review document.

### 1.1 What was verified

| Bounded check | In scope |
|---|---|
| Closure of the previous HIGH (**G-H-01** = V2-H-01) | yes |
| Closure of the previous gate-blocking MEDIUM (**G-M-01** = V2-M-01) | yes |
| Technology neutrality | yes — re-tested |
| Terminal outcome contract | yes — re-tested |
| Comparator evidence absence | yes — re-tested |
| Decision-model regression on the failed scenarios and their adjacents | yes |
| Downstream authoring safety | yes |
| Evidence-integrity regression (previously PASS) | bounded spot-check only |
| Mechanical-integrity regression (previously PASS) | bounded check only |
| Everything else the gate passed | **not reopened** — no repair edit touched it |

### 1.2 Repair actually landed

The repair is real, not asserted. Modification times place every artifact edit **after** the gate and **before** the repair report:

| File | mtime |
|---|---|
| `block-d-gate.md` | 20:05:13 |
| `decision-criteria.md` | 20:13:13 |
| `decision-intelligence-matrix.md` | 20:17:17 |
| `anti-patterns.md` | 20:18:12 |
| `alternatives.md` | 20:18:42 |
| `block-d-gate-repair-report.md` | 20:22:54 |

This is the failure mode the gate itself caught one generation ago — a repair report written against files that were never edited. It does not recur here.

### 1.3 Verdict summary

| Check | Result |
|---|---|
| 1 — Previous HIGH closure | **RESOLVED** |
| 1 — Previous gate-blocking MEDIUM closure | **RESOLVED** |
| 2 — Technology neutrality | **PASS** |
| 3 — Terminal outcome contract | **PASS** |
| 4 — Comparator evidence absence | **PASS** |
| 5 — Decision-model regression | **PASS** |
| 6 — Downstream authoring safety | **PASS** (one non-blocking MEDIUM recorded) |
| 7 — Evidence-integrity regression | **PASS** |
| 8 — Mechanical-integrity regression | **PASS** |

`CRITICAL 0` · `HIGH 0` · `GATE-BLOCKING MEDIUM 0` · new non-blocking: 1 MEDIUM, 2 LOW.

---

## 2. Previous HIGH closure — G-H-01

**RESOLVED.**

### 2.1 The original defect

`decision-criteria.md` §2.5's one-limb `Xr` test — *"The field names what leaves the platform. If nothing leaves the platform, this class does not apply"* — was written correctly at Repair V2 and applied only to a named subset. Two criteria survived in `Xr` whose fields name nothing leaving the platform, and both routed through §2.5's mapping and matrix §5 Step 7 to §6.2 class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` where the corpus documents an in-platform answer:

- **DC-D-049** (Automation, process elapsed duration) — a multi-month approval process.
- **DC-D-068** (Security, authorization enforcement point) — per-user backend authorization through a mediation tier.

### 2.2 The repaired rule, inspected

**DC-D-049 → `Ri`.** Body field now reads:

> **PP negative/exit.** [`Ri`] none evidenced. **In-platform redirect:** at `BEYOND 30 DAYS` held as a single run, the run mechanism becomes unavailable and the documented answer is a **business record with a re-triggering automation** — a mechanism change, not a platform change […]. A durable orchestrator is a design option for the same redirect (Decision impact), not a documented exit.

This is the same shape as **DC-D-025**, the criterion the gate named as the correct template:

> [`Ri`] none evidenced. **In-platform redirect:** at `HIGH` or `LARGE FILES` the binaries leave the database meter for file storage or the document store with a reference — a store and pattern change, not a platform change. An external object store is a design option for the same redirect (Decision impact), not a documented exit.

**The pair test that created the defect now passes.** DC-D-025 and DC-D-049 are structurally identical and are now classed identically. `Related alternatives` was trimmed to `ALT-006, ALT-009 — design options for the redirect, not exit destinations`, matching DC-D-025's convention; ALT-004 was removed and is **not orphaned** (verified — 0 `ALT` orphans corpus-wide).

**DC-D-068 → `Xc`.** Body field now reads *"none from authorization enforcement point alone"* and delegates to matrix §3 row 6 (DC-D-068, 036, 060). Verified that row 6 exists, names DC-D-068 in its Criteria column, and carries Class `DECISION CRITERION` — satisfying §2.5's own registration requirement, which this criterion had met without ever being classed to use it.

### 2.3 Independent re-derivation — the converse check, run over the whole class

This recheck did **not** verify only the two named criteria. All 116 `PP negative/exit` fields were extracted programmatically, the 26 surviving `Xr` fields isolated, and §2.5's decisive test applied to every one.

**Result: 24 of 26 name an off-platform destination explicitly** — *"the attribute leaves the governed store"* (DC-D-026), *"out of the platform for the coordination responsibility"* (DC-D-029, DC-D-054), *"the archival responsibility leaves the platform"* (DC-D-032), *"the platform is not the integration layer for that stream"* (DC-D-036), *"the integration responsibility leaves the platform"* (DC-D-039, DC-D-040), *"a transport outside the platform"* (DC-D-041, DC-D-053), *"a durable log outside the platform"* (DC-D-101, DC-D-103), and so on. Each passes.

**Two are marginal, and both are the gate's own pre-existing LOW finding V2-L-01**, unchanged and correctly still disclosed: **DC-D-013** (*"either change surface or change the requirement"*) and **DC-D-023** (*"the interactive read surface must move; at the extreme this becomes a custom-application trigger"*) name only in-platform changes in the exit field, resting their class on an off-platform limb stated in `Decision impact`. §2.5's escalation rule names DC-D-023 explicitly and defends it. **No new `Xr` member fails the test.** The gate rated these LOW; nothing about the repair changed them in either direction.

**All 7 `Ri` fields were checked in the converse direction** — none names anything leaving the platform. DC-D-006's closing sentence is the sharpest instance of the discipline holding: *"ALT-011's vendor-operated model or ALT-001's incumbent ownership may be the only viable classes — a **candidate** statement, not an exit."*

**All 8 `Xc` fields delegate to a combination**, and all 8 are named in a registered matrix §3 row (**8 == 8, 0 divergence, both directions**).

### 2.4 No stronger claim introduced

Both moves are **de-escalations**: an exit became a non-exit (DC-D-049) and a standalone exit became a registered composed-only exit (DC-D-068). The exit count fell 48 → 46 and the cannot-reject count rose 61 → 62. Nothing moved *into* an exit class; no `Xp` and no `Xe` changed. Verified by recomputation, not read from §3's claim.

**Closure verdict: `RESOLVED`.**

---

## 3. Previous gate-blocking MEDIUM closure — G-M-01

**RESOLVED.**

### 3.1 The original defect

§6.2 class 13's render template carried the clause *"and is the cheaper or lighter option"* **outside** the `ALT-NNN` substitution slot, so it fired for every substituted class. Class 13's own trigger and evidence anchor admit ALT-001 and ALT-011, which the corpus prices nowhere (`licensing-cost.md` LC-U-04). `alternatives.md` §8 carried the identical unscoped shape (*"is the lighter answer"*).

### 3.2 The repaired rule, inspected

Class 13 now renders as **two forms, selected by the substituted class, with an explicit prohibition on merging them**:

> **(a) Where the substituted class is ALT-003** […]: *"No documented constraint excludes Power Platform. ALT-003 is the documented answer for this shape, and is the lighter option **on the seeded-entitlement fact alone (DC-D-093)** — no comparative TCO is asserted. Graduation trigger: …"*
>
> **(b) Where the substituted class is a candidate rather than a documented sufficiency** (ALT-001, ALT-011, or any other class §6.1 admits here): *"No documented constraint excludes Power Platform. ALT-NNN is a candidate for this shape. `COMPARATOR EVIDENCE ABSENT` — engagement-level evaluation required. Graduation trigger: …"*
>
> **The comparative clause exists only in form (a), scoped to the DC-D-093 entitlement fact, and never in form (b).**

This is a **structural** fix, not a rewording: the clause is now inside the branch, so it is incapable of firing for a class the corpus has not evaluated. Both mandatory parts survive in both forms — the non-exclusion statement and the graduation trigger.

`alternatives.md` §8 is aligned and goes further, converting the defect into a standing prohibition: *"a pack must not call either 'the lighter answer' on no evidence."* The string *"is the lighter answer"* is **absent from all four artifacts** (verified by search).

### 3.3 Does form (a) still overstate?

No. The surviving comparative word carries three bounds, all present in the emitted string itself rather than only in surrounding prose:

1. it is scoped to **one named criterion** (DC-D-093, the seeded-entitlement fact the corpus does state);
2. it **disclaims TCO in the same sentence** (*"no comparative TCO is asserted"*);
3. it applies only to **ALT-003 on the four shapes** `data-architecture.md` §6 and `anti-patterns.md` AP-D-008's Exceptions state positively — where the corpus's own words are *"it is not a compromise — it is the documented recommendation."*

§6.1's exception paragraph now points at the string-level fix rather than standing alone as prose: *"§6.2's render template carries this scoping in the string itself, not only in this paragraph."* That is the specific gap the gate identified — prose that disclaimed what the machine-readable string asserted — and it is closed in the direction the gate required.

**Closure verdict: `RESOLVED`.**

---

## 4. Technology neutrality verification

**PASS.**

### 4.1 The six-way distinction, tested in the model rather than in prose

| Distinction | Where it is **enforced** |
|---|---|
| REQUIREMENT / CONSTRAINT | §3.1 register states, per-criterion `States` lists; §5.2's 28 `B` + 3 `B*` |
| PP VIABILITY | §6.2 classes 1, 2 — reachable only from `—`, `Ri` and satisfied conditions |
| PP EXCLUSION | §6.2 classes 5, 6, 7 — reachable **only** from `Xp`, `Xr`, `Xe` and from a registered row whose own §6.2 outcome names them |
| CANDIDATE ALTERNATIVES | §6.2 class 8; matrix §1's Alternatives-column rule (*"candidate generation, not evaluation"*) |
| COMPARATOR EVIDENCE | §4A.1's governing default; §4A.2's 28-criterion evidenced set |
| EVIDENCE-BACKED ALTERNATIVE DIRECTION | §6.2 class 9 **only** — DC-D-108, the single axis §4A.2 discriminates on |

The separation is **mechanised at the emission point**, not merely explained. Matrix §5 **Step 7a** runs immediately before any terminal sentence is written and forces the four statements apart:

> *(1) exclusion and at what scope · (2) which ALT classes come into scope · (3) what §4A.2 says about them, or `COMPARATOR EVIDENCE ABSENT` · (4) preference — permitted ONLY where (3) discriminates. → on current evidence (4) is available on ONE axis: DC-D-108 deployment model.*

And **Step 7** reproduces §2.5's class → outcome mapping byte-compatibly, including the repaired per-row `Xc` mapping and the `Ri` prohibition:

> `Xp→5 · Xr→3/4/6 · Xe→7 · Xc→2/5/7/11/12/14, NAMED PER REGISTERED ROW at §3's Class column, never one class for every Xc criterion · Ri→2 or 13 · Cf→none alone · —→1 or 2.`
> *"an `Ri` may NEVER produce 3, 4, 5, 6 or 7."*

### 4.2 The critical test — `PP EXCLUDED` → `ALTERNATIVE X PREFERRED`

**No branch performs it.** Every exclusion terminal in the repaired model routes to class 8 `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`. Verified on every exclusion path in all 18 scenarios: T-04 → 6 → 8 · T-07 → 5 → 8 · T-08 → 5 → 8 · T-09 → 6 → 8 · T-10 → 12 → 14 → 8 · T-12 → 6 → 8 · T-13 → 5 → 8 · T-14 → 7 → 8.

Class 7's own definition carries the prohibition inline: ***"Never** implies another class is cheaper."* AP-D-059 makes it a rule: *"the composed test can say the option is unavailable, and it cannot say which surviving class is better."*

The repair **strengthened** this rather than weakening it: the two repaired criteria no longer produce an exclusion at all, so the alternative-preference question cannot arise on either path.

### 4.3 Residual-semantics search

All four artifacts were searched for `preferred`, `is better`, `is cheaper`, `is faster`, `cheapest`, `superior`, `recommended alternative`, `obvious replacement`, `best option`, `lighter option`, `lighter answer`. **Every hit is one of:**

- an **explicit prohibition** (§2.2's five forbidden universals; §6.1 rule 1; §4A.3's *"on the four questions most often asked […] Block D's answer is `COMPARATOR EVIDENCE ABSENT`, in every direction, for every class"*; matrix §9's *"it cannot say with evidence which alternative is faster, cheaper or better"*);
- a **withdrawal note** recording a retired label (§6.3's four rows; matrix T-04/T-07's *"Renamed 2026-09-03 from `CUSTOM DEVELOPMENT PREFERRED`"*);
- a **disclaimer** on an alternative's own entry (`alternatives.md` ALT-001: *"Not automatically the cheapest"*);
- an **in-platform design-shape** statement attributed to the corpus (*"the corpus's preferred shape"* — single-writer-per-phase, DC-D-021/DC-D-028), which asserts nothing across technologies;
- the **scoped form (a)** clause verified in §3.3 above.

**No unsupported preference survives anywhere in the four artifacts.**

### 4.4 Bias check, both directions

- **Anti-platform direction:** the repair removed two false exclusions. No scenario that rejects, displaces or blocks Power Platform rests on DC-D-049 or DC-D-068 — verified by scanning all 18 `Criteria triggering` lines. T-16 is the only prior scenario citing DC-D-068, and its `DECISION BLOCKED` rests on DC-D-116's agent-governance and commercial grounds, not on DC-D-068's class. **Nothing softened.** Power Platform is still rejected, displaced or blocked in 13 of 18 scenarios.
- **Pro-platform direction:** both repair moves are *pro*-platform, so this is the direction that needed checking hardest. The corpus's own V3 bias check runs it and this recheck reproduced it: T-04, T-07, T-08, T-09, T-12, T-13 and T-14 all rest on `Xp`, `Xe` or untouched `Xr` exits. T-13 still carries four independent `Xp` exits plus an `Xe`. Class 5 `POWER PLATFORM — POOR FIT` remains an explicit rejection class. **No exclusion was traded away for the correction.**

---

## 5. Terminal outcome contract verification

**PASS.**

All fourteen classes and all eighteen scenario terminals were read. Every required semantic distinction is preserved by a distinct, reachable class:

| Required outcome | Class | Exercised by | Overstates the evidence? |
|---|---|---|---|
| PP viable | 1 | T-01 | No — phrased *"no documented constraint violated"*, never as endorsement |
| PP viable with constraints | 2 | T-02, T-04, T-05 fallback, T-06, T-09, **T-17**, T-18 resolved-yes | No — conditions stated as conditions |
| hybrid / partial responsibility | 3, 4, 6 | T-04, T-05, T-06, T-08, T-11, T-12 | No — class 3 gated on DC-D-070/110/073/083/104; class 6 must name the responsibility |
| PP excluded for a named scope | 5, 6, 7 | T-07, T-13 (5) · T-04, T-09, T-12 (6) · T-14 (7) | No |
| alternatives require evaluation | 8 | T-04, T-07, T-08, T-09, T-10, T-12, T-13, T-14 | No — `COMPARATIVE FIT UNEVALUATED` is in the class name |
| evidence-backed alternative direction | 9 | DC-D-108 only | No — *"Evidenced on **this axis alone** — every other comparative dimension stays `UNKNOWN`"* |
| decision blocked pending evidence | 12 | T-03, T-04, T-08, T-09, T-10, T-15, T-16, **T-18** | No |
| process / no-new-technology direction | 10, 11 | T-14's candidate set (ALT-002, ALT-010); matrix §3 row 9 → 11 | No — both marked *"Not a technology decision"* |
| *(also)* alternative sufficient, PP not excluded | 13 | T-01 | **No — repaired.** Form (b) asserts candidacy only |
| *(also)* in-place remediation unavailable | 14 | T-10 | No — keeps ALT-004 *rebuilt* in the candidate set |

**The alternative-oriented terminals, tested one by one against "does this state more than the evidence proves?":**

- **Class 8** — states exclusion + candidate set + `UNEVALUATED`. Nothing more. ✓
- **Class 9** — the only comparator claim in the model, on the only axis §4A.2 discriminates on, with the limit stated in the class body. ✓
- **Class 13 form (a)** — one class, four documented shapes, one named entitlement fact, TCO disclaimed in-string. ✓
- **Class 13 form (b)** — candidacy + `COMPARATOR EVIDENCE ABSENT`. Nothing more. ✓ **This is the repair.**
- **Class 14** — migration not remediation, followed by class 8; explicitly does not exclude the platform. ✓

**§6.4's per-scope rule is intact** — *"one outcome per scope, not one per engagement"* — which is what stops a bounded `Xr` collapsing into a whole-solution rejection. Verified live in T-06 (class 2 + class 3), T-12 (class 6 + class 4) and T-13 (class 5 + class 1/2).

---

## 6. Comparator evidence verification

**PASS.**

### 6.1 The absence is an explicit, defaulted state

§4A.1 states it as a governing default, not a footnote:

> **`COMPARATOR EVIDENCE ABSENT` is the default on every criterion.** […] where §4A.2 does not carry a row for a criterion, the model's output for that criterion is `POWER PLATFORM <exit class> → CANDIDATES: ALT-NNN… — COMPARATOR EVIDENCE ABSENT`, and a pack must render that phrase rather than a preference.

### 6.2 Independently recomputed

| Quantity | Recomputed | Published | Match |
|---|---|---|---|
| `G` (evidenced alternative-side signal) in §3.1 register | **28** | 28 | ✓ |
| §4A.2's row-leading criteria | **28** | 28 | ✓ |
| `G` set == §4A.2 set, **both directions** | **0 divergence** | — | ✓ |
| Criteria carrying `COMPARATOR EVIDENCE ABSENT` | **88** (116 − 28) | 88 | ✓ |
| Axes supporting a preference between candidates | **1** (DC-D-108) | 1 | ✓ |

### 6.3 Propagation — criterion → matrix → terminal

The absence survives every hop, and this is where the repair improved it:

- **criterion:** §4A.1 default; DC-D-116 carries the absolute form (*"`COMPARATOR EVIDENCE ABSENT` […] here it is absolute rather than default"*).
- **matrix:** §1's Alternatives-column rule — *"Read as a candidate set carrying `COMPARATOR EVIDENCE ABSENT` by default"*; §5 Step 7a's statement (3).
- **terminal:** class 8 carries `UNEVALUATED` in its own name; **class 13 form (b) now carries `COMPARATOR EVIDENCE ABSENT` explicitly where it previously carried a cost preference.**

**The consumer can distinguish "candidate" from "recommended".** The two words are separated by class: class 8 and class 13 form (b) emit *candidate*; class 9 alone emits a comparator-evidenced direction; class 13 form (a) emits a documented sufficiency for one class on four named shapes with TCO disclaimed. There is no path on which a candidate is rendered as a recommendation.

**The repair strengthened this state rather than weakening it** — form (b) closes a place where the marker was previously silent.

---

## 7. Decision regression results

**PASS.**

### 7.1 The two scenarios that failed the previous gate — re-run independently

Both were re-derived from the repaired register and mapping, not read from the repair report or from T-17/T-18's own narratives.

**A-01 / T-17 — multi-month approval process** (capex approval, 90–120 days, human-wait dominated, departmental ownership, no operator).

```
REQUIREMENTS        → process instance open 90–120 days; audit evidence beyond 30 days;
                      single-department ownership; nothing external proposed.
CRITERIA            → DC-D-049 `BEYOND 30 DAYS` · DC-D-103 · DC-D-006 · DC-D-070/073.
PP VIABILITY        → VIABLE. Run mechanism unavailable at the 30-day ceiling; documented
                      answer is a business record with a re-triggering automation, in-platform.
PP EXCLUSIONS       → NONE. DC-D-049 is `Ri`; §2.5 and Step 7 both bar `Ri` from 3/4/5/6/7.
CANDIDATE SET       → NONE GENERATED. No exit fires.
COMPARATOR STATUS   → N/A — no candidate set exists. (Where ALT-005/006 are cited at all,
                      §4A.2 records them `CONSTRAINED` on the triggering axis itself:
                      230-second HTTP ceiling; 5-minute stateless envelope. Verified present.)
TERMINAL OUTCOME    → class 2 POWER PLATFORM — FIT WITH CONSTRAINTS, business-record pattern
                      named as the condition, DC-D-103 retention as a design input.
```

Pre-repair this routed `Xr` → 3/4/6; with no operator, class 3 unavailable and class 4 inapplicable, so class 6's trigger fired by its own words. **Corrected at the source: no exit fires, so no exclusion and no candidate set can be produced.**

**A-02 / T-18 — per-user backend authorization through a mediation tier.**

```
REQUIREMENTS        → downstream finance system enforces per user; facade calls it as a
                      shared service identity; propagation feasibility UNKNOWN.
CRITERIA            → DC-D-068 `TARGET ENFORCES PER USER` · DC-D-036 · DC-D-060.
PP VIABILITY        → UNDETERMINED pending the propagation question.
PP EXCLUSIONS       → NONE, and none reachable. `Xc` routes only via matrix §3 row 6,
                      whose §6.2 outcome is 2 or 12 and which states "Never 5, 6 or 7".
CANDIDATE SET       → NONE NAMED. No off-platform destination in the criterion.
COMPARATOR STATUS   → N/A — no candidate set exists.
TERMINAL OUTCOME    → class 12 DECISION BLOCKED on propagation feasibility; on yes → class 2
                      with explicit delegated identity as the named condition; on no →
                      class 12 continuing, pending a compensating-authorization design.
```

**Corrected.** The `UNKNOWN` is preserved as a block rather than resolved into a guess in either direction.

### 7.2 Adjacent scenarios sharing the repaired rule

All 18 `Criteria triggering` lines were scanned independently.

- **T-16** is the only pre-existing scenario citing DC-D-068. Its `DECISION BLOCKED` rests on DC-D-116's commercial and governance model and on `automation-architecture.md` U-14's unowned deferral. **Outcome unchanged**, correctly.
- **No pre-existing scenario cites DC-D-049.** T-17 is its first exercise — which is precisely why the defect survived three review generations, and why adding it as a standing scenario rather than an audit note is the right closure.
- **T-02** is the adjacent case for the `Ri` rule generally (it fires four non-exit consequence rows and concludes class 2). Re-read: unchanged and still consistent with the mapping.
- **T-05** is the adjacent case for the class-3 operator gate (which A-01 fails). Re-read: its fallback to class 2 when the gate fails is intact, so a failed hybrid gate does not become an exclusion anywhere in the model.
- **T-04, T-07, T-08, T-09, T-12, T-13, T-14** — all rest on `Xp`, `Xe` or untouched `Xr` exits. None softened.

### 7.3 The four regression prohibitions

| Prohibition | Result |
|---|---|
| No unsupported alternative preference | **Held.** §4.3's residual search returns zero live instances |
| No hidden Power Platform advocacy | **Held.** Both repair moves are pro-platform and were checked against every rejecting scenario; none softened. 13 of 18 still reject, displace or block |
| No loss of decision-blocking uncertainty | **Held.** `B` = 28 and `B*` = 3 recomputed and matched to §5.2 in both directions. T-18 blocks rather than guessing; DC-D-068's `UNKNOWN` routes to class 12 |
| No alternative exclusion invented without evidence | **Held.** The repair removed exclusions; it created none. T-17's alternatives cell records ALT-005/006 as `CONSTRAINED` — the corpus's own evidence — rather than as excluded |

---

## 8. Downstream authoring safety verification

**PASS**, with one non-blocking finding recorded at §11.

Block D was read as an authoring input — question-bank logic, discovery signals, technology constraints, decision-tree branches, architecture recommendations — against the gate's own named risks.

| Risk the gate named | Verdict after repair |
|---|---|
| `PP excluded` → replacement recommendation | **Closed.** Every exclusion terminal routes to class 8 with `UNEVALUATED` in the class name. Class 7 carries *"**Never** implies another class is cheaper"* inline |
| candidate alternatives → ranking | **Closed.** Class 8 emits an unranked set; T-13 states the discipline (*"scope narrowing, not evaluation"*); AP-D-059 makes it a rule |
| comparator absence dropped | **Closed, and improved.** Class 13 form (b) now carries the marker where it was previously silent — the one place it was being dropped |
| `UNKNOWN` becoming a default | **Closed.** 28 `B` + 3 `B*` recomputed; DC-D-085/086 still carry a measurement obligation in place of a figure; DC-D-068's `UNKNOWN` routes to class 12, not to a guessed class 2 |
| `INF` becoming vendor guidance | **Closed.** NB-06 still carried in DC-D-036's exit field verbatim; AP-D-059 still declared `Origin: INF over MS facts` |
| `VOLATILE VALUE` becoming a permanent threshold | **Closed.** §7.2's 20-row service-limit register still carries DC-D-049 with its re-verify trigger; §7.3's rule (*"encode the question and the boundary shape, not the number"*) unchanged; the reclassification changed DC-D-049's **exit class**, not its **volatility status** |
| responsibility-level exits → whole-platform exits | **Closed.** §6.4's per-scope rule intact; class 6 must name the responsibility; matrix §1's *"`Xr` is not a weaker `Xp`, and `Ri` is not a quieter `Xr`"* paragraph is the legend a pack reads first |
| hybrid triggers → mandatory architecture | **Closed.** Class 3's trigger requires DC-D-070/110/073/083/104 all satisfied; T-05 demonstrates the fallback to class 2 when the operator gate fails, so hybrid is conditional evidence producing a conditional outcome |

**The repair's own two moves were tested as authoring inputs.** G-H-01's fix **removes** a false rule rather than adding one — a pack reading the repaired register now sees DC-D-049 and DC-D-068 as non-exits with their conditions stated as conditions. G-M-01's fix replaces one unconditioned assertion with two conditioned ones, one of which is the correct output when evidence is missing. Neither manufactures certainty in either direction.

**One residual is recorded as RC-M-01 (§11), non-blocking.** `anti-patterns.md` AP-D-059's Block-D-added row for *criticality two or more levels above operating maturity* still carries Class **`POOR FIT`** in its trigger table, while `decision-intelligence-matrix.md` §3 row 9 — the authority the same entry points to — states **`SPONSOR DECISION` → class 11 or 12, "Never a Power Platform exclusion class (5, 6, 7)"**. `POOR FIT` collides with §6.2 class 5's label verbatim. It is rated non-blocking, and the reasoning is stated in full at §11.1: AP-D-059's own **Decision impact** field — the field that says what decision follows — explicitly routes per-row, names class 11 among the reachable set, and defers to matrix §3. Reaching the unsafe reading requires ignoring the entry's own explicit rule, which this recheck is instructed not to fail on. It is strictly narrower than G-M-02, which the gate itself rated non-blocking.

**The prerequisite the gate identified is still correctly identified and still open by design.** §9 item 7a records that Block D's pack-local vocabulary (*"the governed relational store"*, *"the task-focused surface"*, …) never slips into product names and that the mapping to product names is deliberately not written down, because the Options phase is where it is permitted to exist. Unchanged by the repair. It remains **the first thing authoring will need**, and it is not a Block D defect.

---

## 9. Evidence integrity regression check

**PASS.** Bounded spot-check of the five states across the artifacts the repair touched.

| State | Result |
|---|---|
| `UNKNOWN` | **Preserved.** `B` = **28** recomputed, `§5.2` set identical both directions, 0 divergence. `B*` = **3** (DC-D-113, DC-D-115, DC-D-116) recomputed. DC-D-068's `UNKNOWN` state survives in its `States` list and routes to class 12 |
| `CONFLICTED` | **Preserved.** DC-D-039's 20× custom-connector conflict (NB-02) live in the criterion, in §3.1 as `B V Xr G`, and in matrix §4 with *"Do not encode either figure"* and both re-verification dates. Untouched by the repair |
| `VOLATILE VALUE` | **Preserved.** §7.2's register recounted at **20** rows, DC-D-049 among them with its re-verify trigger intact. §7.1's withdrawal of the unimplemented mitigation still stands. `V` = **11** in the register (unchanged; §7.1's prose still says *"ten"* — R-06, still open, non-blocking) |
| `INF` | **Preserved.** NB-06 carried verbatim in DC-D-036's exit field; AP-D-059's `Origin: INF over MS facts` and its Block-D-derived row markings unchanged; the new per-row outcome mapping does not alter that basis |
| `COMPARATOR EVIDENCE ABSENT` | **Strengthened.** `G` = 28 == §4A.2 both directions, 0 divergence; 88 criteria carry the default; §4A.3's four-question statement intact — **and class 13 form (b) now emits the marker where the pre-repair template emitted a cost preference** |

**No state was silently strengthened anywhere.** Both class reassignments are narrower claims than what they replaced (an unconditioned exit → an in-platform redirect; a standalone exit → a registered composed-only exit). The three composed rows that gained an explicit outcome went from *no stated outcome* to a **named, bounded** one — an increase in specificity, not in certainty, and in row 9's case an explicit **prohibition** on the strongest available reading.

---

## 10. Mechanical regression check

**PASS.** Bounded to what the repair touched, plus the invariants those edits could have broken. Every figure regenerated from the artifacts by independently written extractors.

| Check | Independent result | Required |
|---|---|---|
| Duplicate `DC-D-*` ids | **0** (116 definitions) | 0 ✓ |
| Duplicate `AP-D-*` ids | **0** (68 definitions) | 0 ✓ |
| Duplicate `ALT-*` ids | **0** (11 definitions) | 0 ✓ |
| Duplicate §3.1 register rows | **0** | 0 ✓ |
| Duplicate matrix §2 rows | **0** (116 rows, 116 unique) | 0 ✓ |
| Dangling `DC-D-*` / `AP-D-*` / `ALT-*` refs, all four files | **0 / 0 / 0** | 0 ✓ |
| Register rows carrying more than one class | **0** | 0 ✓ |
| **body class == register class == matrix class** | **116 / 116 · 0 mismatches** | ✓ |
| Class distribution, regenerated from the 116 `PP negative/exit` fields | `Xp` **15** · `Xr` **26** · `Xe` **5** · `Xc` **8** · `Ri` **7** · `Cf` **17** · `—` **38** · sum **116** | ✓ |
| Distribution agrees at every published home (§2.5 table, §2.5 prose, §3 domain table, §9 item 5, §11 summary, matrix §1 legend, matrix §9) | **all seven agree** | ✓ |
| Direct exits (`Xp`+`Xr`+`Xe`) | **46**, as published at all four of its homes | ✓ |
| Rows that cannot reject (`—`+`Ri`+`Cf`) | **62**, as published at §2.5, matrix §1, matrix §9 | ✓ |
| §3 domain table — 12 rows × 9 class columns + `B` + `G` + totals | **every cell recounted from the register, exact match** | ✓ |
| Automation row `Xr`/`Ri` after the move | **6 / 1** as published | ✓ |
| Security row `Xr`/`Xc` after the move | **2 / 3** as published | ✓ |
| `B` · `B*` | **28** · **3** | ✓ |
| §5.2 set == `B` set, both directions | **0 divergence** | ✓ |
| `G` == §4A.2 set, both directions | **28 == 28, 0 divergence**; 116 − 28 = **88** | ✓ |
| Matrix §3 rows | **12**, numbered 1–12, no gaps | ✓ |
| Matrix §3 structural validity (columns per row, both tables) | **6 columns, all 12 rows, consistent** | ✓ |
| **Every §3 row carries a non-empty Class column** | **12 / 12** (was 8 / 12 — four Block-D rows had none) | ✓ |
| **Every §3 row carries a non-empty §6.2-outcome column** | **12 / 12** | ✓ |
| `Xc` set == criteria named in a registered §3 row, both directions | **8 == 8, 0 divergence** (DC-D-001, 015, 037, 063, 064, 068, 080, 104) | ✓ |
| AP-D-059's registration list == the `Xc` set | **identical, 8 ids** | ✓ |
| Composed-register count agreement (§2.4, §11, matrix §3, matrix §9, AP-D-059) | **12 at all five sites** | ✓ |
| Anti-pattern orphans (defined, cited by no criterion) | **0** | ✓ |
| Alternative orphans — including after DC-D-049's `ALT-004` trim | **0** | ✓ |
| Every criterion names ≥1 anti-pattern, ≥1 alternative, a `Lineage` field | **116 / 116 / 116** | ✓ |
| Repaired matrix rows state content rather than a bare marker | **DC-D-049 and DC-D-068 both fully stated**; anti-pattern and alternative sets match their bodies exactly | ✓ |
| Outcome classes defined in §6.2 | **14**, numbered 1–14, no gaps | ✓ |
| Status footers accurate (G-L-02) | **4 / 4 repaired** — all now read *"Gate recheck not yet performed"* | ✓ |

**No mechanical check regressed, and one previously-failing structural invariant is now satisfied:** the four Block-D-added composed rows previously carried no Class column at all, and all twelve now name a reachable §6.2 class or class pair.

**Two derived counts still do not reproduce** — both pre-existing, both confirmed still open, neither read by any decision behaviour:

- §9 item 8 publishes `HIGH 57 · MEDIUM 56 · LOW 3`; recounted from all 116 `**Confidence:**` fields: **`HIGH 68 · MEDIUM 46 · LOW 2`**. (R-04.)
- §7.1 and §9 item 4 say *"ten"* volatile criteria; the register carries `V` on **11** (DC-D-116). (R-06.)

---

## 11. New findings

`CRITICAL 0` · `HIGH 0` · `GATE-BLOCKING MEDIUM 0`.

### 11.1 New non-blocking findings raised by this recheck

| Id | Severity | Gate-blocking | Finding |
|---|---|---|---|
| **RC-M-01** | MEDIUM | **No** | **G-M-02's closure is partial across files.** The repair added a per-row Class and §6.2-outcome column to `decision-intelligence-matrix.md` §3 — a real and well-executed fix, verified at §10 — but `anti-patterns.md` AP-D-059's own trigger table was not brought into line for one row. Its Block-D-added row *"Criticality class two or more levels above the demonstrated operating maturity, with no funded plan"* still carries Class **`POOR FIT`**, which is `decision-criteria.md` §6.2 class 5's label (`POWER PLATFORM — POOR FIT`) verbatim — while matrix §3 row 9, describing the identical combination, now states `SPONSOR DECISION` → class **11 or 12** and adds *"**Never a Power Platform exclusion class (5, 6, 7)** — the gap recurs on every platform, so naming Power Platform would misattribute a sponsor-side finding as a capability one."* Secondarily, AP-D-059's Decision impact directs the reader to *"`decision-intelligence-matrix.md` §3's **Class** column"* as the authority, when the authoritative column for a §6.2 outcome is §3's **§6.2 outcome** column; §3's Class column is `architecture-patterns.md` §13's consequence vocabulary. **Why non-blocking.** Five of the eight values in that column (`ANTI-PATTERN`, `CONSTRAINT`, `RISK`, `VOLATILE VALUE / CONFLICTED`, `DECISION CRITERION`) are not §6.2 labels at all, so the column plainly is not a §6.2 outcome column; the row's own consequence text says *"cannot be delivered in any architecture […] a sponsor decision, not a design one"*; and AP-D-059's Decision impact — the field that states what decision follows — explicitly routes per-row and names class 11 among the reachable set. Reaching the unsafe reading requires ignoring the entry's own explicit rule, which this recheck is instructed not to fail on. It is strictly narrower than G-M-02, which the gate itself rated MEDIUM non-blocking. **Recommended fix (one cell + one word):** change AP-D-059's row-9 Class cell to `SPONSOR DECISION` and point the Decision impact at §3's *§6.2 outcome* column |
| **RC-L-01** | LOW | No | **A withdrawn template string survives in one quotation.** `decision-intelligence-matrix.md` T-01's *"Evidence supports it?"* line still reads *"Its **'cheaper or lighter'** is the seeded-entitlement fact of DC-D-093, not a TCO comparison"* — quoting the pre-repair class-13 clause. The word *"cheaper"* no longer appears in any render template. The sentence **disclaims** rather than asserts, and its substantive claim (*"it makes no comparative claim about cost, speed or scale"*) is correct and conservative, so nothing is emitted wrongly. It is a stale quotation left behind when §6.2 changed and T-01's prose did not |
| **RC-L-02** | LOW | No | **§2.5's classification rule was not tightened as the gate's repair item 1 recommended.** The gate asked the repair to *"state which limb governs when a field reaches both an in-platform answer and an off-platform option — that ambiguity is what produced the split."* §2.5's standing rule still reads *"the class is the **broadest scope the field reaches** at a named state without further conditions"*, with the design-option principle stated **by example** (DC-D-025's and DC-D-049's field text now carry the identical *"a design option for the same redirect … not a documented exit"* phrasing) rather than as a general rule. In practice the ambiguity is now resolved at the point that matters — the field texts disambiguate themselves and the whole class was re-derived — so no criterion is currently misclassified. The exposure is to a **future** criterion or a future reviewer re-splitting the pair, which is the failure mode that produced G-H-01 in the first place. Recommended as one sentence in §2.5 |

### 11.2 Findings confirmed still open from prior generations — unchanged, non-blocking

All independently re-verified against the artifacts, not accepted from the repair report's §13.

| Id | Severity | Status |
|---|---|---|
| **R-03** | MEDIUM, non-blocking | Still open, correctly disclosed. DC-D-055's matrix row still reads *"the platform's strongest documented differentiator here"*, still carries `AP-D-015` against the body's `AP-D-015, AP-D-027`, still omits the DC-D-111 precondition. Class `—`; no outcome depends on it |
| **R-04** | MEDIUM, non-blocking | Still open. §9 item 8 publishes `HIGH 57 · MEDIUM 56 · LOW 3` against a recount of **`HIGH 68 · MEDIUM 46 · LOW 2`**. No decision behaviour reads it |
| **R-06** | LOW–MEDIUM, non-blocking | Still open. `V` = **11** recomputed against §7.1's *"ten"*. The register is authoritative and correct; the prose is off by one |
| **V2-M-02** | MEDIUM, non-blocking | Still open, still correctly disclosed. DC-D-046 → `Ri` remains contestable on its own evidence. Mitigated because matrix §3 row 2's operator gate runs from its own criteria under Step 4 |
| **V2-L-01** | LOW | Still open, independently re-confirmed at §2.3. DC-D-013 and DC-D-023's exit fields name only in-platform changes; §2.5's escalation rule names and defends DC-D-023 |
| **V2-L-02** | LOW | **Effectively addressed** — matrix §9's claim now reads *"appears there verbatim **or as a stated abbreviation of one**"*, which is the honest form the gate asked for (*"either emit labels in full or drop the 'verbatim' claim"*). A weakening in the safe direction |
| **G-L-01** | LOW | Still open. DC-D-002's matrix row omits ALT-004; DC-D-116's matrix cell and body use compatible but non-identical set notation. Neither can change a decision |
| **G-L-02** | LOW | **Closed.** All four status footers now accurately read *"Gate recheck not yet performed."* Verified in all four files |
| Areas 1–12 lineage defects | recorded, not repaired | `licensing-cost.md`'s duplicate `DC-14` and `integration-architecture.md` §15.8's dangling citation remain, correctly recorded and correctly not repaired by Block D |
| Research commissions | not defects | `alternatives.md` §6's ten comparative evidence gaps, items 9 and 10 in particular, remain correctly scoped as upstream commissions |

### 11.3 Regressions introduced by the bounded repair

**One, at LOW severity: RC-L-01.** Every other new finding is either a *partial* closure of a finding the gate itself rated non-blocking (RC-M-01) or an omission from the gate's own recommended scope (RC-L-02). No previously-passing dimension regressed: evidence integrity, decision-model completeness and mechanical integrity all re-verify, and the two counts that did not reproduce before still do not reproduce in exactly the same way.

---

## 12. Final promotion recommendation

**PASS. Block D is ready for canonicalisation.**

Both gate-blocking findings are closed at the root cause, and the closure was verified independently rather than accepted:

- **G-H-01 — RESOLVED.** The `Xr` membership was re-derived from §2.5's own decisive test over the whole class, not re-patched for a named subset. This recheck ran the converse check itself over all 26 surviving `Xr` fields and all 7 `Ri` fields, and found no member failing the test beyond the two the gate had already rated LOW (V2-L-01) and which the repair correctly left alone. The DC-D-025 / DC-D-049 pair — the structurally identical criteria classed in opposite directions that were the defect's signature — are now classed identically, in identical language. Both criteria are now under **standing test** as T-17 and T-18 rather than under one-off audit, which is what stops the defect recurring a fourth time.

- **G-M-01 — RESOLVED.** The comparative clause is now structurally confined to the one class the corpus ever evidenced it for. Form (b) emits `COMPARATOR EVIDENCE ABSENT` where the pre-repair template emitted a cost preference about two classes the corpus prices nowhere. The string *"is the lighter answer"* is absent from all four artifacts, and `alternatives.md` §8 converted the defect into a standing prohibition against reintroducing it.

- **G-M-02 — substantially resolved, forced by the first.** All twelve registered composed rows now name a reachable §6.2 class or class pair, where four previously had no Class column at all and a global {5, 12, 14} mapping was routing row 6 to no valid outcome. Row 9's explicit *"Never a Power Platform exclusion class"* is the sharpest instance of the model refusing to misattribute a sponsor-side finding as a capability one. One cell in `anti-patterns.md` was not brought into line — **RC-M-01**, non-blocking.

**The three gates that failed now pass.** Technology neutrality passes because the distinction is enforced in the decision model itself — §6.1's governing rule, §2.5's class → outcome mapping, matrix §5 Steps 7 and 7a — and not merely explained in prose; the one place a render string contradicted that enforcement is repaired. Decision-model regression passes on independent re-derivation of both failed scenarios and on all their adjacents. Downstream authoring safety passes on all eight of the gate's named risks.

**Both directions of bias were checked.** The repair's two moves are both *pro*-platform, which is the direction that needed the harder check; every scenario that rejects, displaces or blocks Power Platform was re-verified to rest on criteria the repair did not touch, and none softened. Power Platform is still rejected, displaced or blocked in 13 of 18 scenarios. In the anti-platform direction the false exclusions are gone, and no new exclusion was invented anywhere.

**What the recheck did not find.** No new CRITICAL. No new HIGH. No new gate-blocking MEDIUM. No silently strengthened epistemic state. No duplicate id, no dangling reference, no orphan, no three-way class disagreement. The exit taxonomy has now shrunk under scrutiny three times — 54 → 48 → 46 — each time by refusing to call an in-platform consequence an exit, and each step is published with the test that produced it. That is a corpus behaving correctly under review.

**Recommended before authoring consumes Block D — none blocking:**

1. **RC-M-01** — one cell and one word in `anti-patterns.md` AP-D-059. Worth doing first, because AP-D-059 is the entry an authoring process reads for composed-disqualifier logic, and it is the last place in the corpus where a `POOR FIT` label sits against a conclusion that rejects no platform.
2. **RC-L-02** — one sentence in §2.5 stating which limb governs, so the DC-D-025 / DC-D-049 principle is a rule rather than a pair of examples.
3. **RC-L-01, R-03, R-04, R-06, G-L-01** — cheap, already diagnosed, none read by any decision behaviour.
4. **The pack-local vocabulary glossary** (§9 item 7a) remains a **prerequisite for authoring, not an optional extra**, and is correctly not a Block D deliverable. It is the first thing authoring will need.

---

`FINAL BOUNDED GATE RECHECK: PASS`
`PREVIOUS HIGH FINDING VERIFIED RESOLVED: YES`
`PREVIOUS GATE-BLOCKING MEDIUM VERIFIED RESOLVED: YES`
`TECHNOLOGY NEUTRALITY: PASS`
`DECISION MODEL REGRESSION: PASS`
`DOWNSTREAM AUTHORING SAFETY: PASS`
`EVIDENCE INTEGRITY REGRESSION: PASS`
`MECHANICAL INTEGRITY REGRESSION: PASS`
`NEW GATE-BLOCKING FINDINGS: 0`
`READY FOR BLOCK D CANONICALIZATION: YES`

---

**Not performed, by instruction:** any repair of Block D · canonicalisation of Block D · PP pack authoring · any new research · any broad Block D review · any modification of any Block D artifact · any modification of Areas 1–12 · any reopening of dimensions that passed the previous gate and that the repair did not touch.
