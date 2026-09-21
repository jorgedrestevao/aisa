Repair Status: COMPLETE
Repair date: **2026-09-03**
Scope: **bounded repair V2 — the remaining HIGH finding, the remaining gate-blocking MEDIUM finding, and the regression they caused.** No Block D redesign. No re-review. No gate. No canonicalisation. No pack authoring. `library/packs/pp/` untouched. Areas 1–12 read, **not modified**. No external or new broad research.
Authority: `research/pp/evidence/block-d-re-review.md` (independent re-review, verdict `FAIL` — HIGH 1, gate-blocking MEDIUM 1, `DECISION MODEL REGRESSION: FAIL`).

# Block D Bounded Repair V2 Report

Files modified: `decision-criteria.md` · `anti-patterns.md` · `alternatives.md` · `decision-intelligence-matrix.md`.

**What V2 repaired, in one sentence each.** The exit taxonomy V1 introduced was internally consistent and **semantically wrong**: one class carried two opposite decision consequences and another pointed at a register that did not contain it. The "closed" outcome set was **not closed**, because it had no class for two outcomes the model reaches. Both defects have been repaired at the level of the model — new classes with an explicit class → outcome mapping, and a registration requirement that is now testable — not at the level of the wording or the derived counts.

---

## 0. Identification

The re-review left exactly two gate-blocking findings. Both are repaired here. Nothing else in Block D was reopened.

### 0.1 R-01 — HIGH · exit taxonomy classification unsound

| | |
|---|---|
| **Finding ID** | `R-01` (`block-d-re-review.md` §11), five sub-parts (a)–(e) |
| **Affected files** | `decision-criteria.md` §2.5, §3, §3.1, §4 (26 criterion bodies), §4A.4, §9 item 5, §11 · `decision-intelligence-matrix.md` §1, §2 (26 rows), §3, §5 Steps 4 and 7, §9 · `anti-patterns.md` AP-D-059 |
| **Affected criteria** | **`Xr` → `Ri` (6):** DC-D-006, 021, 025, 030, 046, 088. **`Xc` → `Cf` (17):** DC-D-004, 011, 022, 024, 027, 035, 038, 047, 048, 058, 061, 085, 086, 087, 090, 098, 112. **Restated, class unchanged (1):** DC-D-032 (`Xr`). **Registration added (1):** DC-D-080 to matrix §3 row 4 |
| **Affected anti-patterns** | AP-D-059 (the composed test; `Xc`'s registration authority) |
| **Affected alternatives** | none directly |
| **Affected matrix rows** | the 26 criterion rows above, of which **10 were bare class markers** (5 `Xr`: DC-D-025, 030, 032, 046, 088 · 5 `Xc`: DC-D-011, 022, 037, 038, 080); plus §3 row 4, §5, §9 |
| **Root cause** | **One class carrying two opposite decision consequences.** §2.5's `Xr` definition read *"a bounded responsibility … **leaves the platform**, **or** an in-platform pattern becomes unavailable"*. Those two limbs terminate in different outcome classes, and V1 mapped the whole class to the exclusion outcomes. Six criteria whose documented answer is a **different in-platform store, pattern or surface** were therefore filed as exits that route to exclusion. The second root cause is the same shape: `Xc` **asserted** its exit *"lives in §3"* without any rule **requiring** it to, so 24 criteria pointed at a 12-row register that named 6 of them |
| **Canonical evidence involved** | `architecture-patterns.md` §13 (the twelve-row register's source; it carries **no criteria column**, which is where the mapping gap sat) · `data-architecture.md` §2 rows 7 and 12, §6, DA-17, DA-18, DA-44, DA-59 (the in-platform store redirects and the archival exit) · `application-architecture.md` AA-06 · `automation-architecture.md` AT2-53, §4 row 22 · manifest NB-01 |
| **Why Repair V1 was insufficient** | V1 was asked to *name the distinction the file was using and never named*, and it did — then measured its own success with the wrong test. Its 44-check suite verified that the three representations **agreed** (they did, exactly, on all 116) and never verified that the classification was **sound**: no check asked whether an `Xr` field names something leaving the platform, and no check asked whether an `Xc` criterion appears in the register its own definition cites. Consistency was proved; correctness was assumed. V1 also derived its headline `54` from that unsound classification, so the count was a symptom rather than the defect |

### 0.2 R-02 — MEDIUM, gate-blocking · outcome set not closed

| | |
|---|---|
| **Finding ID** | `R-02` (`block-d-re-review.md` §11) |
| **Affected files** | `decision-criteria.md` §6.1, §6.2, §6.3, §6.4, §11 · `decision-intelligence-matrix.md` T-01, T-05, T-06, T-10, §5 Step 7, §7, §9 · `anti-patterns.md` AP-D-059 · `alternatives.md` ALT-003, §8 |
| **Affected matrix rows / scenarios** | **T-01** (emitted `COLLABORATION-PLATFORM NATIVE`) · **T-05** (emitted `single platform + a tripwire`) · **T-06** (emitted `HYBRID`) · **T-10** (emitted class 8 with no antecedent class) |
| **Root cause** | **Not the two stray labels — the missing classes underneath them.** The V1 set had twelve classes covering two terminal shapes: *Power Platform in, with or without conditions* and *Power Platform out → candidates*. It had **no class for an outcome in which Power Platform is not excluded and an alternative is nonetheless the documented answer** (ALT-003's own outcome, and the commonest departmental shape), and **no class for a composed row concluding the workload cannot be brought to the required class *in place*** while the same platform rebuilt stays a candidate. Class 8 is defined as the terminal form *for exclusions*, so it could carry neither. The labels leaked because the model kept reaching conclusions the set could not express |
| **Canonical evidence involved** | **Class 13:** `application-architecture.md` AA-36 rung 0, AA-20, AA-50 (the one-way upgrade) · `data-architecture.md` §2 row 7, §6 (the four shapes stated positively) · `licensing-cost.md` LC-28 · `operations-support.md` §1.1 · `anti-patterns.md` AP-D-008 Exceptions, AP-D-005, AP-D-039, AP-D-065. **Class 14:** `governance.md` G-03 · `operations-support.md` O-05, O-10 · `alm-devops.md` ALM-14. **T-05's condition:** `automation-architecture.md` AT2-53, §4 row 22 |
| **Why Repair V1 was insufficient** | V1 executed the review's correction #7 literally and completely — *define the set once, add an explicit rejection class, align AP-D-059 and T-14* — and then **asserted** closure (*"the set is closed: the other files emit from this list and no other"*) instead of **testing** it. A one-line check over the emitted labels would have found all three violations. And because the check was never run, the deeper gap it would have exposed — that the set was missing two terminal shapes, one of them on the commonest engagement in the domain — stayed invisible |

### 0.3 The regression, and what was deliberately left alone

`DECISION MODEL REGRESSION: FAIL` was caused by **R-01(a)/(b)** and **R-02**, in four scenarios: **T-02** (the counter-example that falsified V1's `Xr` mapping rule), and **T-01, T-05, T-10** (the closed-set violations). **T-06** was found during this repair's own adjacency pass and carries both defects. All five are repaired and re-run in §3.

Two findings the re-review raised are **not** in V2's scope and are **not** repaired, stated here so the boundary is explicit rather than silent:

| Finding | Why out of scope |
|---|---|
| **R-03** (MEDIUM, not gate-blocking) — the DC-D-055 matrix row still carries *"the platform's strongest documented differentiator here"*, lacks the DC-D-111 precondition, and omits AP-D-027 | Caused by the **M-06** repair, not by R-01 or R-02. DC-D-055's class is `—` and V2 did not touch it, so it is not a regression of these defects. **Verified still open** by this repair's mechanical pass (§4): it remains the only criterion↔matrix anti-pattern-set divergence in 116 rows |
| **R-04 … R-14** (MEDIUM/LOW) — confidence distribution, `V` count, §8.2 reference counts, the stray `Classification` field, the two new composed rows' criteria sets, §2.8's header, and the rest | Not gate-blocking, not caused by R-01 or R-02, and repairing them would be reopening Block D. **Except** where a V2 edit made one moot: §9 item 5's counts and matrix §9's *"79 dashes"* are both R-01(e) and are repaired |

---

## 1. R-01 — Exit taxonomy classification unsound

**Status: RESOLVED.**

### 1.1 Exact repair

**1. `Xr` lost its second limb.** The class now means one thing: *at a named state a bounded responsibility **leaves the platform***. Its test is unchanged in wording and now decisive in effect — *"The field names what leaves the platform. **If nothing leaves the platform, this class does not apply.**"*

**2. Two consequence classes were added, and neither is an exit.** This is the model repair. The consequences V1 was smuggling into the exit taxonomy are real and decision-changing; they simply do not take anything off the platform.

| New class | Definition | Outcome it may produce | Outcome it may **never** produce |
|---|---|---|---|
| **`Ri`** in-platform redirect | At a named state a documented in-platform pattern, store, mechanism or surface becomes **unavailable**, and the documented answer is a **different in-platform choice**. Nothing leaves. | §6.2 class 2, or class 13 where the redirect's destination is a class the corpus documents as sufficient | classes 3, 4, 5, 6, 7 — **any exclusion** |
| **`Cf`** combination input | No exit and no redirect of its own. The value is a required **input** to another criterion's exit or to a registered composed row, and the field names which. | none on its own | everything — a pack must resolve the criterion it feeds |

**3. `Xc` gained a registration requirement.** *"A criterion may carry `Xc` only if it is named in a row of `decision-intelligence-matrix.md` §3 / `anti-patterns.md` AP-D-059. An unregistered combination is not an exit — it is `Cf`."* Seven criteria qualify (DC-D-001, 015, 037, 063, 064, 080, 104); the other seventeen became `Cf`.

**The alternative to this was invention, and it was refused.** The other way to make 24 `Xc` flags resolve is to add eighteen rows to the composed register. That would have asserted eighteen combinations as *disqualifiers* which the corpus never states as such. `architecture-patterns.md` §13 registers eight; Block D derives four from the same corpus and marks them derived. The register stays at twelve. **The criteria that feed those rows are inputs, and V2 says so.**

**4. §2.5 now carries an explicit class → outcome mapping table.** This is the sentence V1 was missing rather than getting wrong: it named the classes and left the mapping implicit, which is exactly how an in-platform store change acquired an exclusion outcome. `decision-intelligence-matrix.md` §1 and §5 Step 7 now reference the table rather than restating it, so there is one authority.

**5. DC-D-080 was added to matrix §3 row 4's criteria list** — *business- or mission-critical + no representative managed test environment + **no recovery drill***. Reversibility is the leg that condition tests. This changes **no consequence, no class and no canonical content**: `architecture-patterns.md` §13 carries no criteria column, so the row → `DC-D-NNN` mapping is Block D's own, and the omission sat there.

**6. DC-D-032 was restated and kept as `Xr`.** Its V1 field said *"none evidenced; the answer is an archival store"* and **understated its own evidence**. The corpus is explicit that in-platform long-term retention is `CONDITIONAL` only — managed environment, irreversible, no capacity saving for files, retained data no longer surfaced to the analytical shortcuts — and that *"backups as archive → ≤ 28 days, same region, not downloadable → **not a retention mechanism**"*. At `MULTI-YEAR, QUERYABLE` at volume the **archival responsibility genuinely leaves** to a lake or archive store, while the active record stays. That is `Xr` by the repaired test, and the field now states it.

**7. All ten bare matrix cells were filled** from the criterion bodies. Matrix §1 now makes it a rule: *"Every cell states its content… A bare class marker is a defect — V1 left ten cells bare, which is how a `—` carrying information became a class carrying none."*

**8. Every derived count was regenerated from the classification**, not patched: §2.5's distribution table, §3's domain table (now nine class columns), §9 items 5 and the new 5b, §11, matrix §1's legend, matrix §9, and the stale *"79 dashes"* in matrix §9's closing paragraph.

### 1.2 Headline arithmetic — three generations

| Quantity | V0 | V1 | **V2** | Why |
|---|---|---|---|---|
| `Xp` platform exits | — | 15 | **15** | unchanged |
| `Xr` responsibility exits | — | 34 | **28** | six in-platform redirects removed |
| `Xe` economic exits | — | 5 | **5** | unchanged |
| `Xc` composed-only | — | 24 | **7** | registration required; 17 were unregistered |
| `Ri` in-platform redirect | — | — | **6** | new, **not an exit** |
| `Cf` combination input | — | — | **17** | new, **not an exit** |
| `—` no exit | 79 | 38 | **38** | unchanged |
| **Direct exits** | 36 *(published)* | 54 | **48** | |
| Rows that cannot reject the platform | — | 38 | **61** | `—` + `Ri` + `Cf` |
| Composed disqualifiers | 8 / 10 / 8 | 12 | **12** | unchanged, now with a registration rule |
| Outcome classes | 11, open | 12, asserted closed | **14, closure testable** | R-02 |

**The exit count went down, and that is the point.** V0 published 36 against bodies containing 48 statements. V1 reached 54 by admitting six in-platform redirects and eighteen unregistered combinations into exit classes. V2 reached **48** by refusing both. An exit taxonomy that shrinks under scrutiny is behaving correctly; §9 item 5 now carries all three generations and the test that produced each, because that history is the strongest evidence in the file that the counting is driven by classification rather than the reverse.

**The load-bearing argument survives both corrections.** Governance and ALM still produce **zero direct exits** between them. The 38 dashes are still 33% of the register. And the honesty ratio in §11 is now `48` direct exits against `1` evidenced comparative axis.

### 1.3 Canonical evidence used

`architecture-patterns.md` §13 (all twelve rows; the absent criteria column) · `data-architecture.md` §2 row 7 (*"SharePoint / Lists is preferable when: the document is the record… small flat trackers"*), §2 row 12 and DA-17 (long-term retention `CONDITIONAL`, irreversible, *"doesn't reduce capacity consumed"* for files, *"retained data is no longer surfaced"*), DA-18 (*"backups… not a retention mechanism"*), §6, DA-44, DA-59 · `application-architecture.md` AA-06, AA-50 · `automation-architecture.md` AT2-53, §4 row 22 · manifest NB-01 · `alm-devops.md` ALM-06, ALM-17, ALM-23. **No canonical claim was re-interpreted and no figure was moved.** The reclassification is a reading of Block D's own 116 exit fields against §2.5's own test; DC-D-032 is the one criterion whose *evidence* was restated, and it was restated **from** the canonical text rather than beyond it.

### 1.4 Remaining uncertainty

- **DC-D-046 is the one judgement a re-reviewer may contest.** Its field says the mediation tier *"may or may not be outside the platform"*. It is classed `Ri`, because the location is a design choice driven by DC-D-045 and DC-D-047 rather than a documented consequence of *this* criterion — and because classing an ambiguous case as an exit is the error V2 exists to correct. If a re-reviewer holds that the tier is documented as external, DC-D-046 becomes `Xr` and direct exits become 49.
- **DC-D-080's addition to §3 row 4** is a mapping refinement, not a canonical change. A re-reviewer could instead argue DC-D-080 should be `Cf` feeding DC-D-089/DC-D-100. Recorded so the choice is visible.
- **`Ri` and `Cf` are Block D's own vocabulary**, like the exit classes themselves, and inherit the undeclared-pack-local-vocabulary prerequisite already recorded at §9 item 7a.

**External research required?** No. This finding is entirely about Block D's internal consistency and its reading of evidence already mounted.

**Status: RESOLVED.**

---

## 2. R-02 — Outcome set not closed

**Status: RESOLVED.**

### 2.1 Exact repair

**1. Two classes were added, appended rather than inserted.**

| # | Class | Fires when | Mandatory parts |
|---|---|---|---|
| **13** | **ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED** | **No exit of any class fires**, and a class other than ALT-004 is the documented answer for the requirement shape — either stated positively by the corpus, or as an `Ri` redirect's destination | (a) it must state that **Power Platform is not excluded**, so it can never be read as a rejection; (b) it must carry a **graduation trigger**, because the documented path off the collaboration and team-hosted surfaces is a **one-way upgrade** converting every user to premium (`application-architecture.md` AA-50) |
| **14** | **IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED** | A **registered** composed row concludes the existing artefact cannot be brought to the required class **in place**, while the same platform **rebuilt** remains a candidate | names the documented mechanisms; followed by class 8. It exists because *the remediation estimate a sponsor is usually given is for the wrong work* |

The twelve V1 numbers are unchanged, because `anti-patterns.md` AP-D-003, AP-D-035, AP-D-059 and AP-D-061 and eight matrix scenarios cite them **by number**. Renumbering would break the lineage discipline manifest §4 protects — the same reason DC-D-116 sits outside its domain's range. §6.2 states this and §6.4 restates that numeric order carries no preference.

**2. Closure became a test instead of an assertion.** §6.2 now reads: *"The set is **closed**, and closure is a testable property, not a claim: **every outcome string emitted anywhere in `anti-patterns.md` or `decision-intelligence-matrix.md` must appear verbatim in the table below.** A label that does not appear here is a defect in the emitting file, not a new class."* Matrix §5 Step 7 carries the same instruction at the point of writing: *"if the label you are about to write is not in §6.2, the label is wrong, not the set."*

**3. Class 8's antecedent was widened** to *"classes 5, 6, 7 and 14, and class 13 where the alternative's sufficiency is not documented"* — which is what T-10 needed and could not have.

**4. §6.3 gained two withdrawal rows** recording `COLLABORATION-PLATFORM NATIVE` and `single platform + a tripwire`, what each was carrying, and where it went. The second is **not** replaced by a class: it is the corpus's own phrase for a **condition on a fit** (`automation-architecture.md` AT2-53 — *"single platform + a tripwire, not a paper hybrid"*), so it is retained as class 2's condition wording, with the metric that would force the move recorded as the tripwire.

**5. §6.4 gained the per-scope rule.** *"One outcome per scope, not one per engagement."* An `Xr` takes a named responsibility off the platform and leaves the rest, so an engagement legitimately terminates in more than one *(scope, class)* pair — class 2 for the application and class 3 for analytics (T-06); class 5 for a consumer surface and class 1 for the operations behind it (T-13). The matrix's scenarios already behaved this way; it was never stated, and class 8's antecedent depends on it.

### 2.2 The one thing V2 had to get right: class 13 is not a preference

Class 13 names a specific alternative **without** class 8 in exactly one situation — where the corpus states that alternative's sufficiency **for a named requirement shape in its own words**. Today that is ALT-003 on the four shapes `data-architecture.md` §6 and `anti-patterns.md` AP-D-008's Exceptions state positively: the document is the record; a small flat tracker with one or two lookups, list-level security and low write concurrency; a form whose audience is the list's audience; team scope matching seeded entitlement. `alternatives.md` ALT-003 already carried the corpus's framing — *"In these cases it is not a compromise — it is the documented recommendation."*

§6.1 now states, as a governing rule, why this is **not** the comparative claim rule 1 forbids:

- It is a statement about **one class's documented sufficiency for a named shape**, sourced to the vendor's own guidance. It is not a ranking and it does not survive outside those four shapes.
- It asserts **nothing** about cost, speed, scale or reliability relative to any other class. Class 13's *"cheaper or lighter"* is scoped to the entitlement fact the corpus does state — the collaboration surface runs on seeded licences already held (DC-D-093) — and **never** to a comparative TCO, which `licensing-cost.md` LC-U-04 records as absent for every class.
- **Power Platform is not excluded**, which class 13 must say. Where the requirement crosses any of AP-D-008's triggers, class 13 does not apply and ALT-004 is the answer.
- For every class other than ALT-003, class 13 is followed by class 8 and carries `COMPARATOR EVIDENCE ABSENT` like everything else. **The exception is one class on four documented shapes, not a general licence.**

`Power Platform excluded` was **not** converted into `Alternative X preferred` anywhere. Class 13 fires only where **nothing is excluded**, which is the opposite configuration.

### 2.3 Canonical evidence used

**Class 13:** `application-architecture.md` AA-36 rung 0 (*"configure or buy before any app type"*), AA-20, AA-50 (*"Growth beyond limits → one-way upgrade… then premium licences for all users"*) · `data-architecture.md` §2 row 7, §6 · `licensing-cost.md` LC-28, DC-15 (*"Always carry process change, existing capability and do-nothing as priced options"*), LC-U-04 · `operations-support.md` §1.1 · `anti-patterns.md` AP-D-008 Exceptions (*"`data-architecture.md` §6 states these positively — this anti-pattern is not 'never use it'"*), AP-D-005, AP-D-039, AP-D-065 · `alternatives.md` ALT-003.
**Class 14:** `governance.md` G-03 · `operations-support.md` O-05, O-10 · `alm-devops.md` ALM-14 — the same evidence already under matrix §3's Block D row 3, no new claim.
**T-05's condition:** `automation-architecture.md` AT2-53, §4 row 22.
**Class 5 / class 14 boundary:** `architecture-patterns.md` §13, `platform-suitability.md` §1's `POOR`.

### 2.4 Remaining uncertainty

- **Class 13's evidenced scope is exactly four shapes and one class.** Whether ALT-001 or ALT-011 can ever stand in class 13 without class 8 is `UNKNOWN` and deliberately left so: the corpus evaluates no incumbent and no product (`alternatives.md` §6 item 3), so for those classes class 13 is always followed by class 8. Should the comparative commissions in `alternatives.md` §6 land, this is where they would widen the class — and until then the narrow scope is the finding.
- **Fourteen classes is more than a decision tree wants.** Classes 10, 11 and 13 are adjacent in practice (*don't build*, *defer*, *something lighter is enough*), and a pack may want to render them as one question with three answers. That is a pack-design decision and is out of Block D's remit.
- **Class 14 currently has exactly one trigger** — matrix §3's Block D row 3. If the register never grows, class 14 has one route in. That is honest rather than tidy: it is the class for a conclusion the corpus reaches once.

**External research required?** No, to close the finding — both classes are built from evidence already mounted. **Yes, to widen class 13 beyond ALT-003**, which is the existing comparative-TCO and incumbent-assessment commission (`alternatives.md` §6 items 1 and 3), unchanged and not attempted here.

**Status: RESOLVED.**

---

## 3. Regression scenarios re-run

**Scenarios that caused `DECISION MODEL REGRESSION: FAIL`:** T-02 (R-01's counter-example), T-01, T-05, T-10 (R-02's closed-set violations). **Found during V2's own adjacency pass:** T-06 (both defects). **Directly adjacent scenarios capable of being affected, re-checked:** T-03, T-04, T-08, T-09, T-11, T-12, T-13, T-14, T-15, T-16. The complete Block D review was **not** re-run.

| Scenario | V1 | V2 | Substantive conclusion changed? |
|---|---|---|---|
| **T-02** Excel replacement — *the falsifying case* | class 2 `FIT WITH CONSTRAINTS` — correct, **and contradicted by matrix §1's own `Xr` → classes 3/4/6 rule**, which would have emitted class 6 for a store change | class 2, with the class arithmetic stated: **one scoped `Xr`** (DC-D-031, analytics), **one `Ri`** (DC-D-030), **one `Cf`** (DC-D-022), and DC-D-023/DC-D-026 not reaching their exit states | **No.** The rule now agrees with the scenario. This is the scenario that falsified V1 and it is the one the repair is measured against |
| **T-01** simple departmental app | class 1 **or** `COLLABORATION-PLATFORM NATIVE` — undefined label | class 1 **or** **class 13** naming ALT-003, graduation trigger mandatory; rejection line restated (DC-D-022 `Cf`, DC-D-030 `Ri` inert at `RARE`) | **No.** Same two branches, same evidence. The alternative branch now has a class, so a pack can no longer be forced to drop it |
| **T-05** high-volume integration | class 3, falling back to `single platform + a tripwire` — undefined label | class 3, falling back to **class 2** whose named condition is the corpus's *"single platform + a tripwire, not a paper hybrid"*, with the forcing metric recorded | **No.** The fallback was always a conditioned fit, not a terminal class |
| **T-06** complex data-centric app | class 2 **plus** `HYBRID` — undefined label; DC-D-022's traversal depth readable as a platform rejection | class 2 for the application scope **plus** class 3 for the analytical responsibility (DC-D-031's `Xr`); DC-D-022 stated as `Cf` feeding **DC-D-088's `Ri`** | **No.** Two scopes, two classes — §6.4 now states that rule |
| **T-10** citizen app → enterprise-owned | class 12 → class 8 **unaccompanied**, against class 8's own definition | class 12 → **class 14** → class 8, with the row's documented mechanisms named | **No.** Same migration-not-remediation conclusion, and class 14 keeps Power Platform *rebuilt* in the candidate set rather than rejecting it |
| T-03, T-04, T-08, T-09, T-11, T-12, T-13, T-14, T-15, T-16 | — | **untouched** | **No.** Verified mechanically: every exit these rest on is `Xp`, `Xe` or an `Xr` V2 did not reclassify — DC-D-018, 036, 059, 062, 084, 042, 091, 100, 020, 009, 016, 012, 010, 093, 092, 116. The three that name a reclassified criterion (T-10 DC-D-006, T-15 DC-D-021) name it as a **`B` blocking** criterion, which is a flag V2 did not change |

**Mechanical check on the repair's own risk.** No scenario drives an exclusion class from an `Ri` or `Cf` criterion. Verified by scanning every `**Outcome:**` line for reclassified ids: three hits, all legitimate — T-02's correction note (historical), T-10's DC-D-006 as a `B` block, T-15's DC-D-021 as an evidence task.

**V2 bias check — run in both directions, because the repair moves both ways.**

- **Pro-platform direction:** V2 **reduces** the exit count from 54 to 48. Every scenario that rejects or displaces was re-tested against the reclassification: **T-04, T-07, T-08, T-09, T-12, T-13 and T-14 all rest on exits V2 did not touch**, and not one softened. T-13 still carries four independent `Xp` exits plus an `Xe`; T-07 and T-13 still emit class 5 `POWER PLATFORM — POOR FIT`.
- **Anti-platform direction:** class 13 stops a pack dropping the alternative branch on the commonest departmental shape — which, left unfixed, would have been a structural bias *toward* the platform arrived at by omission.
- **Net:** Power Platform is rejected, displaced or blocked in **12 of 16** scenarios — the same twelve as before V2.
- **Artificial-comparator check:** no scenario gained a claim about an alternative's fitness. Class 13's only named comparator is ALT-003 on the four shapes the corpus states positively; class 14 keeps ALT-004 in scope rather than excluding it. T-04's *"the replacement's adequacy is unevidenced"* and T-09's NB-07 note are intact.

**Failed regression scenarios now pass: YES** (T-01, T-02, T-05, T-06, T-10).

---

## 4. Cross-file consistency and mechanical validation

A checker was written and run over all four files. **37 checks, 37 PASS**, plus three known-open items reported rather than silently passed.

### 4.1 Taxonomy and counts

| Check | Result |
|---|---|
| Criterion bodies · duplicate `DC-D-*` ids | 116 · **0** |
| Every body carries a class tag | ✅ 116 |
| §3.1 register rows · register ids == body ids | 116 · ✅ |
| Register rows carrying more than one class | **0** |
| Matrix rows, one per criterion | ✅ 116 |
| **body class == register class == matrix class, all 116** | ✅ **0 mismatches** |
| Distribution == published everywhere | ✅ `Xp` 15 · `Xr` 28 · `Xe` 5 · `Xc` 7 · `Ri` 6 · `Cf` 17 · `—` 38 |
| Direct exits == 48 · classes sum to 116 | ✅ · ✅ |
| §3 domain table — all 12 rows × 9 columns + totals, recounted | ✅ **every cell** |
| **Every `Xc` criterion named in a matrix §3 row** | ✅ **7 of 7** (was 6 of 24) |
| `Xc` set == the seven registered | ✅ DC-D-001, 015, 037, 063, 064, 080, 104 |
| `Ri` == 6 · `Cf` == 17 | ✅ |
| **No `Ri`/`Cf` field claims anything leaves the platform** | ✅ |
| Matrix cells carrying a class marker and no content | **0** (was 10; bare `—` correctly exempt — a dash is its own content) |

### 4.2 Blocking, alternative-side, composed

| Check | Result |
|---|---|
| `B` == 28 · `B*` == 3 (DC-D-113, 115, 116) | ✅ · ✅ |
| §5.2 lists exactly the 28 `B` plus the 3 `B*` in its footnote table | ✅ |
| `G` == 28 · §4A.2 criteria == the `G` set, **both directions** | ✅ · ✅ |
| Composed disqualifiers == 12 in matrix §3, AP-D-059, §2.4 and §11 | ✅ all four |
| `COMPARATOR EVIDENCE ABSENT` present in all three decision files | ✅ |

### 4.3 Outcome set

| Check | Result |
|---|---|
| All **14** labels defined in §6.2 | ✅ |
| Every outcome-shaped string emitted in the matrix appears in §6.2 | ✅ — 34 candidate strings extracted from §6's scenarios; 32 are criterion **state names**, and the only two outcome labels not in §6.2 are `CUSTOM DEVELOPMENT PREFERRED` and `EXISTING ENTERPRISE PLATFORM PREFERRED`, both appearing **only** in §7's before/after table as retired labels |
| Withdrawn labels appear only in withdrawal/correction context | ✅ — `COLLABORATION-PLATFORM NATIVE` (2 sites, both explanatory); `single platform + a tripwire` (3 sites: DC-D-070's *"Why it matters"* quoting the corpus as reasoning, the §6.2 V2 note, the §6.3 withdrawal row) |
| No surviving comparative recommendation about an unevaluated class | ✅ — every `PREFERRED` / `CHEAPER` / `FASTER` / `BETTER` / `BEST` occurrence is a state name (`ORDER PREFERRED`, `CORPORATE NETWORK PREFERRED`, `BEST EFFORT`), a retirement note, a before/after row, the prohibition itself, or T-14's statement of the gap |

### 4.4 Ids, references, lineage

| Check | Result |
|---|---|
| `AP-D-*` definitions, unique | **68** |
| `ALT-*` definitions, unique | **11** |
| Dangling `DC-D-*` / `AP-D-*` / `ALT-*` | **0 / 0 / 0** |
| Every criterion names ≥ 1 anti-pattern · ≥ 1 alternative · a file-qualified `Lineage` | ✅ 116 / 116 / 116 |
| **Canonical id references resolved** | **3,083 occurrences / 1,524 distinct (file, id) pairs — 0 unresolved** (one scanner false positive: `SUB-15`, from the state name `SUB-15-MINUTE`) |
| Criterion → matrix **anti-pattern** set identity | **115 of 116** — `DC-D-055` diverges (**R-03, out of V2 scope, verified still open**) |
| Criterion → matrix **alternative** set identity | 114 of 116 — `DC-D-002` (pre-existing) and `DC-D-116` (deliberate: the matrix cell says *"none evaluable"*, the body lists candidates *"all `UNKNOWN` on this axis"*). **R-09, out of V2 scope** |

**No headline count was manually patched.** Every published figure in this repair was regenerated by the checker from the criterion bodies and then written into the files; the checker was re-run afterwards and reproduces all of them.

### 4.5 Semantic consistency across the four files

| Concept | `decision-criteria.md` | `decision-intelligence-matrix.md` | `anti-patterns.md` | `alternatives.md` |
|---|---|---|---|---|
| `Ri` / `Cf` are not exits | §2.5 definitions + mapping table; §3.1 legend; §4A.4 step 1 | §1 legend and the three-way misreading warning; §5 Step 7 | — | — |
| `Xc` registration requirement | §2.5 | §3 registration rule | AP-D-059 closing paragraph | — |
| Class 13 | §6.1 exception rule, §6.2 class 13, §6.3 withdrawal | T-01; §5 Step 7; §7 | — | ALT-003 outcome-class note; §8 |
| Class 14 | §6.2 class 14, §6.3 | T-10; §7 | AP-D-059 class 5 / class 14 boundary | — |
| Closure as a test | §6.2 | §5 Step 7; §9 | AP-D-059 (*"and from nowhere else"*) | — |
| One outcome per scope | §6.4 | T-06, T-12, T-13 | — | — |

---

## 5. Preserved knowledge states

| State | Verified after V2 |
|---|---|
| `UNKNOWN` | ✅ agent economics/capacity/latency/accuracy; broker and streaming sizing (U-13, U-03); comparator portability; incumbent fit; polling intervals; concurrency and amplification figures; GOV-U-06. **DC-D-046's tier location is recorded as a design choice, not resolved** |
| `CONFLICTED` | ✅ NB-02 unchanged, still 20×, still barred from encoding, DC-D-039 still `Xr` + `B` + `V`. Matrix §3 row 5 still the registered composed row, and DC-D-037 stays `Xc` because it is named in it |
| `VOLATILE VALUE` | ✅ §7.1 and §7.2 untouched; the 20-criterion service-limit register intact; **no figure became a state name** |
| `INF` | ✅ NB-06 carried in DC-D-036, DC-D-111, ALT-007, T-12; AP-D-059's composition still `INF`; the two Block D composed rows still marked derived |
| `COMPARATOR EVIDENCE ABSENT` | ✅ §4A.1's default on 88 criteria unchanged; the marker still in all three decision files; **class 13's one exception is bounded to ALT-003 on four documented shapes and stated as a rule in §6.1** |
| Manufactured comparator evidence | **none.** No comparative TCO, benchmark, incumbent evaluation or comparator low-code claim was created. Class 13 fires only where nothing is excluded; class 14 keeps ALT-004 in the candidate set |

---

## 6. Files modified

| File | Before | After | Nature of change |
|---|---|---|---|
| `decision-criteria.md` | 3,750 | **3,806** | §2.5 rewritten (seven classes, registration rule, class → outcome mapping) · §3 domain table regenerated with nine class columns + reclassification note · §3.1 legend · 26 criterion bodies re-tagged, 8 exit fields rewritten · §4A.4 step 1 · §6.1 class-13 exception rule · §6.2 V2 note + classes 13 and 14 + closure-as-test · §6.3 two withdrawal rows · §6.4 per-scope rule · §9 items 5 and 5b · §11 |
| `decision-intelligence-matrix.md` | 687 | **725** | §1 V2 note, seven-marker legend, three-way misreading warning, exit-cell content rule · 26 §2 rows re-tagged and **10 bare cells filled** · §3 DC-D-080 added to row 4 + registration rule + *"the register is not a wish list"* · §5 Step 4 `Cf` note, Step 7 mapping and closure instruction · T-01, T-02, T-05, T-06, T-10 · §7 V2 before/after table + V2 bias check · §9 |
| `anti-patterns.md` | 2,505 | **2,509** | AP-D-059 decision impact: class 14 added, class 5 / class 14 boundary stated, `Xc` registration authority stated |
| `alternatives.md` | 804 | **807** | ALT-003 outcome-class note (class 13, its three non-negotiable properties) · §8 pack-implication bullet |
| `block-d-repair-v2-report.md` | — | this report | |

`library/packs/pp/` — **untouched.** Areas 1–12 canonical files — **read only, not modified.**

---

## 7. Findings this repair leaves open

| Finding | Status | Gate-blocking? |
|---|---|---|
| **R-03** DC-D-055 matrix row (superlative, missing DC-D-111 precondition, missing AP-D-027) | **Open, verified still open.** Caused by the M-06 repair, not by R-01 or R-02; DC-D-055's class is `—` and V2 did not touch it | No — the re-review rated it MEDIUM, not gate-blocking |
| **R-04** §9 item 8 confidence distribution (published 57/56/3; actual 68/46/2) | Open | No |
| **R-05** matrix §8.2 reference counts (AP-D-059 "11", ALT-008 "7") | Open | No |
| **R-06** `V` count 11 vs §7.1's "ten" | Open | No |
| **R-07** stray `Classification` field at `anti-patterns.md` §1.4 | Open | No |
| **R-08** the two new composed rows list 3 criteria in AP-D-059 and 4 in matrix §3 | Open | No |
| **R-09 … R-14** | Open | No |
| **H-04 residual** — no comparative evaluation exists in the corpus | Unchanged; `COMPARATOR EVIDENCE ABSENT` on 88 criteria | No — upstream commission |
| **H-03 residual** — no agent fit assessment exists in any canonical file | Unchanged; DC-D-116 blocks | No — upstream commission |
| **Areas 1–12** duplicate `licensing-cost.md DC-14`; `integration-architecture.md` §15.8 | Unchanged, recorded not repaired | Not for Block D |

**Unresolved gate-blocking findings: 0.**

---

## 8. Verdict

`BLOCK D V2 HIGH FINDINGS RESOLVED: YES`
`BLOCK D V2 GATE-BLOCKING MEDIUM FINDINGS RESOLVED: YES`
`FAILED REGRESSION SCENARIOS NOW PASS: YES`
`NEW RESEARCH REQUIRED: NO`
`READY FOR BLOCK D RE-REVIEW V2: YES`

---

**Not performed, by instruction:** the re-review · the Block D gate · canonicalisation · PP pack authoring · any external or new broad research · any repair of R-03 … R-14 · any reopening of Block D beyond the two gate-blocking findings and the regression they caused.
