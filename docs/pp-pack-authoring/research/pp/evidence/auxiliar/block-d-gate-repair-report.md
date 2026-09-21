Repair Status: COMPLETE
Repair date: **2026-09-03**
Scope: **bounded gate-failure repair — the two gate-blocking findings of `research/pp/evidence/block-d-gate.md`, and the one dependent finding forced by repairing the first.** Not a new Block D review. No new research. No canonicalisation. No PP pack authoring. Areas 1–12 read for verification only, not reopened, not modified.
Authority repaired against: `research/pp/evidence/block-d-gate.md` (`BLOCK D GATE: FAIL` — HIGH 1, gate-blocking MEDIUM 1).

# Block D Gate-Failure Bounded Repair

## 1. Gate Failure Summary

`block-d-gate.md` independently re-derived both findings from the artifacts rather than trusting the review chain's summaries, and found:

| | Gate result |
|---|---|
| `BLOCK D GATE` | `FAIL` |
| `CRITICAL FINDINGS` | 0 |
| `HIGH FINDINGS` | 1 |
| `GATE-BLOCKING MEDIUM FINDINGS` | 1 |
| `EVIDENCE INTEGRITY` | PASS |
| `TECHNOLOGY NEUTRALITY` | **FAIL** |
| `MECHANICAL INTEGRITY` | PASS |
| `DECISION MODEL REGRESSION` | **FAIL** |
| `DOWNSTREAM AUTHORING SAFETY` | **FAIL** |
| `READY FOR BLOCK D CANONICALIZATION` | NO |

**Why Technology Neutrality failed (gate §5).** Not on the exclusion paths, which the gate verified hold on every scenario. It failed because `decision-criteria.md` §6.2 class 13's render template carried an unconditioned comparative clause — *"and is the cheaper or lighter option"* — outside its `ALT-NNN` substitution slot, so it fired a cost claim for ALT-001 and ALT-011, two classes the corpus prices nowhere. This is `alternatives.md` §2.2's forbidden-claim list re-entering the corpus one layer down, exactly as H-02 first found it and one scope narrower.

**Why Decision Model Regression failed (gate §9).** The gate applied `decision-criteria.md` §2.5's own one-limb `Xr` test to all 28 `Xr` criteria — not to the subset a prior review had named — and constructed two adjacent scenarios (its A-01, A-02) that no existing test exercised. Both found a false platform exclusion: **DC-D-049** (a multi-month approval process) and **DC-D-068** (per-user authorization through a mediation tier) were classed `Xr` on fields naming nothing leaving the platform, and both routed through §2.5's mapping to §6.2 class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` where the corpus documents an in-platform answer.

**Why Downstream Authoring Safety failed (gate §10).** Both defects sit in the machine-readable artefacts a pack author copies most directly — a render template string and a criterion's exit-class tag — so both would be encoded verbatim rather than caught by a consistency check.

## 2. HIGH Finding

**Finding ID:** G-H-01 (= V2-H-01 in the review chain)
**Severity:** HIGH
**Type:** Taxonomy / classification — root-cause membership defect, inherited across two repairs
**Affected artifacts:** `decision-criteria.md` §2.5 (distribution, class → outcome mapping), §3 (domain table, Automation and Security rows), §3.1 (register), §9 items 5/5b, §11 · `decision-intelligence-matrix.md` §1 (legend), §2.5/§2.6 rows, §3 (registration rule), §5 Step 7, §9
**Affected IDs:** DC-D-049 (Automation, process elapsed duration), DC-D-068 (Security, authorization enforcement point)
**Root cause.** `decision-criteria.md` §2.5's `Xr` test reads: *"The field names what leaves the platform. If nothing leaves the platform, this class does not apply."* Repair V2 wrote this test correctly but applied it only to the criteria the prior re-review had named by pattern-matching fields whose text *"opens with a form of 'none'"* — a search method the prior re-review itself disclosed. DC-D-049's field opens with *"`BEYOND 30 DAYS` held as a single run **is a documented exit**"* and DC-D-068's opens with *"the pattern is unsuitable"* — neither matches that pattern, so neither was re-examined, even though neither field names an off-platform destination.
**Why Repair V2 did not eliminate it.** V2 fixed the **definition** (removed the two-limb `Xr` and made the outcome mapping explicit) but never re-derived the **membership** of `Xr` from the repaired definition over the whole class. It patched the six criteria a prior review named (DC-D-006, 021, 025, 030, 046, 088) and stopped. Re-Review V2 confirmed the definition was sound and did not itself run the converse check — *"every `Xr` field claims something leaves"* — over all 28 criteria; the gate ran it and found the two survivors.
**Decision behaviour affected.** A pack authoring its decision tree from §2.5's register would emit `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` for (a) a business process that simply runs longer than 30 days, whose own documented answer is an in-platform business record with a re-triggering automation, and (b) an in-platform authorization design constraint (propagate identity through an intermediary) with no off-platform destination named anywhere in the criterion. In case (a) the classification additionally pointed the decision at alternatives (ALT-005, ALT-006) the corpus's own §4A.2 rows record as *more* constrained on the triggering axis than the platform.

**Resolved: YES.**

## 3. Gate-Blocking MEDIUM Finding

**Finding ID:** G-M-01 (= V2-M-01 in the review chain)
**Severity:** MEDIUM, gate-blocking
**Type:** Unsupported preference / cross-file contradiction
**Affected artifacts:** `decision-criteria.md` §6.1 (exception paragraph), §6.2 (class 13 render template) · `alternatives.md` §8 (pack-implication bullet)
**Affected IDs:** class 13 `ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED`, referencing ALT-001, ALT-003, ALT-011
**Root cause.** Class 13's render template was written as one string covering two semantically different situations — *the corpus states an alternative's sufficiency* (true only of ALT-003, on four named shapes) and *an alternative is merely a candidate* (true of ALT-001, ALT-011, and anything else class 13's trigger admits) — and the comparative clause *"is the cheaper or lighter option"* sat outside the `ALT-NNN` substitution slot, so it was emitted regardless of which situation applied.
**Why Repair V2 did not eliminate it.** V2's own repair introduced class 13 to close R-02 (the missing terminal for the ALT-003 case) and, in doing so, wrote the render template broadly enough to admit ALT-001 and ALT-011 as substitutable classes without narrowing the comparative clause to the one class the corpus actually documents as sufficient. The prose paragraphs around class 13 (§6.1's exception rule, ALT-003's own note) were written correctly and disclaim the overreach — but the machine-readable string itself, which is what a pack encodes, did not match its own prose.
**Decision behaviour affected.** For any engagement where class 13 fires with ALT-001 or ALT-011 as the documented answer rather than ALT-003, the rendered terminal sentence would assert a cost preference the corpus's own `licensing-cost.md` LC-U-04 records as absent.

**Resolved: YES.**

## 4. Root-Cause Analysis

Both findings share a shape: **a correctly stated rule whose application was scoped too narrowly** — G-H-01 to a named subset of criteria, G-M-01 to a single render string covering two cases it should have distinguished. The repair addresses the mechanism in both cases, not the symptom:

- **G-H-01.** §2.5's decisive test was re-applied to **all 28** `Xr` criteria, not re-run against the same named subset. This is the only way to close a "the rule is right but was never fully applied" defect — narrowing the search again would reproduce exactly the failure mode the gate found.
- **G-M-01.** The render template was split into **two named forms**, selected by which class is substituted, so the comparative clause is now structurally incapable of firing for a class the corpus has not evaluated — it exists only inside form (a), scoped to ALT-003.

**A third, forced repair.** Reclassifying DC-D-068 from `Xr` to `Xc` makes it the criterion at matrix §3 row 6, and row 6's own consequence (`DECISION CRITERION`) does not fit the single global `Xc` → outcome mapping {5, 12, 14} that §2.5 previously stated. Inspecting all twelve registered rows found that **three others** already had the same problem or worse: row 3 (`CONSTRAINT`, an unfunded mandated control — an economic finding, not a capability one), row 4 (`RISK`, an unevidenced production commitment — a validation gap, not an exclusion), and Block D row 1 (`SPONSOR DECISION`, a maturity-funding gap that recurs on every platform and previously had **no Class column at all**). This is finding **G-M-02**, non-blocking per the gate but explicitly flagged there as forced by the G-H-01 repair. It is fixed in the same pass: `decision-criteria.md` §2.5's `Xc` mapping now reads *"2, 5, 7, 11, 12 or 14 — named per registered row"*, and `decision-intelligence-matrix.md` §3 gained a **Class column** on all twelve rows (the four Block-D-added rows previously had none) stating the reachable `decision-criteria.md` §6.2 class for each, with the reasoning for the three non-obvious ones (rows 3, 4, 9) stated inline.

## 5. Technology-Neutrality Repair

The seven-way distinction the brief requires — requirement, PP viability, PP scope exclusion, candidate classes, alternative constraints, comparator evidence status, evidence-backed preference — was already structurally present in §4A.4's four-part render contract and §6.1's governing rule. The defect was that one render string violated its own governing rule. The repair does not add new machinery; it makes the existing rule's enforcement complete.

**Before (§6.2 class 13, one form, unconditioned):**
> *"No documented constraint excludes Power Platform. ALT-NNN is \<the documented answer for this shape / a candidate\> and is the cheaper or lighter option. Graduation trigger: …"*

**After (two forms, selected by the substituted class, never merged):**
> **(a) ALT-003 substituted:** *"No documented constraint excludes Power Platform. ALT-003 is the documented answer for this shape, and is the lighter option on the seeded-entitlement fact alone (DC-D-093) — no comparative TCO is asserted. Graduation trigger: …"*
> **(b) any other candidate substituted (ALT-001, ALT-011, …):** *"No documented constraint excludes Power Platform. ALT-NNN is a candidate for this shape. `COMPARATOR EVIDENCE ABSENT` — engagement-level evaluation required. Graduation trigger: …"*

The same correction was applied to `alternatives.md` §8's parallel bullet, which carried the identical unscoped clause (*"is the lighter answer"*).

**Verification against the gate's own critical test — `Power Platform excluded` must never imply `Alternative X preferred`.** This test was already passing on every exclusion path (classes 5, 6, 7, 14 all route through class 8, comparative fit `UNEVALUATED`); the defect sat in the one **non-exclusion** class, where "not excluded" was being paired with an unearned comparative claim about a *different* class than the one the corpus actually evaluated. Form (b) now states `COMPARATOR EVIDENCE ABSENT` explicitly and asserts nothing else. The repair does not touch class 8's own template, the four exclusion classes, or any scenario's exclusion logic — it narrows exactly one clause to the one class it was ever evidenced for.

**§6.1's exception paragraph** (the prose that was already correct) was tightened to point at the string-level fix, so the paragraph and the render template now make the identical claim in both places: *"§6.2's render template carries this scoping in the string itself, not only in this paragraph."*

## 6. Decision-Regression Repair

**DC-D-049 — Process elapsed duration.** Reclassified `Xr` → `Ri`. The `PP negative/exit` field and `Decision impact` field were rewritten to state the in-platform redirect explicitly, mirroring the already-correct DC-D-025 pattern the gate cited as the template: the run mechanism becomes unavailable at `BEYOND 30 DAYS`, and the documented answer — a business record with a re-triggering automation — is a different in-platform choice. The durable-orchestrator limb is now stated as a design option for the same redirect, not the exit. `Related alternatives` was trimmed from `ALT-004, ALT-006, ALT-009` to `ALT-006, ALT-009` (ALT-004 is Power Platform itself and does not belong in a "design option" list, matching DC-D-025's own convention).

**DC-D-068 — Authorization enforcement point.** Reclassified `Xr` → `Xc`. The field now states that no exit exists from this criterion alone; the disqualifier lives in the already-registered matrix §3 row 6 (DC-D-068, 036, 060), whose class is `DECISION CRITERION`, not an exclusion — satisfying V2's own `Xc` registration requirement, which this criterion had met without ever being classed to use it.

**Cascading updates, all independently recomputed after the edit (not copied from the plan):**

| Figure | Before Repair V3 | After Repair V3 |
|---|---|---|
| `Xr` | 28 | **26** |
| `Ri` | 6 | **7** |
| `Xc` | 7 | **8** |
| Direct exits (`Xp`+`Xr`+`Xe`) | 48 | **46** |
| Rows that cannot reject the platform (`—`+`Ri`+`Cf`) | 61 | **62** |
| Automation domain (`Xr`/`Ri`) | 7 / 0 | **6 / 1** |
| Security domain (`Xr`/`Xc`) | 3 / 2 | **2 / 3** |

Republished at every site the gate named: `decision-criteria.md` §2.5 (distribution table, class→outcome mapping), §3 (domain table, "exactly what moved" paragraph), §3.1 (register flags), §9 items 5/5b, §11 · `decision-intelligence-matrix.md` §1 (legend counts), §2.5/§2.6 (row content), §9 (summary table) · `anti-patterns.md` AP-D-059 (registration count, decision-impact mapping).

**Two new adversarial scenarios added, not merely re-run.** Because neither DC-D-049 nor DC-D-068 appeared in any of the sixteen existing scenarios — which is how the defect survived three review generations — the gate's A-01 and A-02 were added to the corpus as permanent scenarios **T-17** and **T-18** (`decision-intelligence-matrix.md` §6), in the same style and rigour as the existing sixteen, so the repaired rule is now under standing test rather than only under one-off audit. See §12 below for full results.

## 7. Downstream-Authoring Safety Repair

Both fixes were tested against the gate's own question: *could this wording become a deterministic rule stronger than the underlying evidence?*

- **G-H-01's fix removes a false rule**, it does not add one. A pack authoring from the repaired register now correctly reads DC-D-049 and DC-D-068 as non-exits, with their in-platform conditions stated as conditions — exactly the shape §4A.4's render contract requires.
- **G-M-01's fix removes an unconditioned assertion and replaces it with two conditioned ones**, one of which is `COMPARATOR EVIDENCE ABSENT` — the correct output when evidence is missing, per the brief's own instruction. No new certainty was manufactured on either side.
- **G-M-02's fix (forced) prevents a new failure mode from being introduced by the first fix.** Without it, DC-D-068's move to `Xc` would have made matrix §3 row 6 simultaneously *registered* and *unmapped to any valid outcome* — a pack encountering that state would have had nowhere correct to route the decision. The per-row Class column closes that gap for row 6 and, since the same defect existed latently in three other rows, for all twelve.
- **No volatile threshold was hard-coded.** DC-D-049's `BEYOND 30 DAYS` and the run-duration figures remain governed by `decision-criteria.md` §7.2's service-limit register and §7.3's rule (*"a pack encodes the question and the boundary shape, not the number"*) — unchanged by this repair.
- **No silent inference across an evidence gap was introduced.** Where DC-D-068's identity-propagation feasibility is `UNKNOWN`, the repaired mapping routes to class 12 `DECISION BLOCKED`, not to a guessed class 2 or a guessed exclusion.

## 8. Files Modified

| File | Sections changed |
|---|---|
| `research/pp/evidence/decision-criteria.md` | §2.5 (Repair note V3, distribution table, class→outcome mapping table, closing paragraph) · §3 (domain table, "exactly what V3 moved" paragraph) · §3.1 (DC-D-049, DC-D-068 register rows) · §4.5 DC-D-049 body (Decision impact, PP negative/exit, Related alternatives) · §4.6 DC-D-068 body (Decision impact, PP negative/exit) · §6.1 (exception-paragraph bullet) · §6.2 (class 13 row) · §9 (items 5, 5b) · §11 (summary table, closing sentence) · status footer |
| `research/pp/evidence/decision-intelligence-matrix.md` | §1 (Repair note V3, legend counts, "62 of 116" sentence) · §2.5 DC-D-049 row · §2.6 DC-D-068 row · §3 (Class column added to all twelve rows, registration-rule paragraph, new closing paragraph) · §5 Step 7 (mapping restatement) · §6 (new scenarios T-17, T-18) · §7 (passing/gap counts, new V3 re-run table and bias check) · §9 (summary table) · status footer |
| `research/pp/evidence/anti-patterns.md` | AP-D-059 (Decision impact paragraph, registration-count sentence) · status footer |
| `research/pp/evidence/alternatives.md` | §8 (pack-implication bullet) · status footer |

No file under `library/` was touched. No file outside `research/pp/evidence/` was touched. Areas 1–12 (the twelve canonical files) were read for verification and not modified.

## 9. Evidence Used

All evidence was already canonical and already cited by Block D; no new source was consulted.

- **DC-D-049's own field** — the exit statement's own parenthetical, *"not necessarily for the platform, since the state-record pattern stays in-platform,"* is the field arguing against its own class.
- **DC-D-025's already-repaired `Ri` field** — used as the template for DC-D-049's rewrite, since both are "an in-platform mechanism becomes unavailable, with an off-platform limb present but undocumented as an exit" pairs.
- **`decision-intelligence-matrix.md` §3 row 6** — DC-D-068's own registration, already present, whose Class (`DECISION CRITERION`) is what the criterion's field itself already implied.
- **`decision-criteria.md` §4A.2's DC-D-049 rows** (ALT-005 `CONSTRAINED` at 230 seconds; ALT-006 `CONSTRAINED` at 5 minutes) — used to state, in the new T-17 scenario, why the pre-repair classification pointed at alternatives the corpus records as *worse* on the triggering axis.
- **`alternatives.md` LC-U-04 and §6 item 3** — re-cited (not re-derived) to justify form (b)'s `COMPARATOR EVIDENCE ABSENT` for ALT-001/ALT-011.
- **`architecture-patterns.md` §13's own row consequences** (already quoted in matrix §3) — used unchanged to derive each row's §6.2 class in the new Class column; no canonical file was re-read for new facts.

No claim in this repair rests on anything not already present in the four Block D artifacts or the canonical files they already cited.

## 10. Uncertainty Preserved

| State | Status after repair |
|---|---|
| `UNKNOWN` | Unaffected. DC-D-068's identity-propagation feasibility, where `UNKNOWN`, still routes to class 12 (§2.5 mapping, matrix §3 row 6), not to an inferred class |
| `CONFLICTED` | Unaffected. DC-D-039's 20× conflict (NB-02) is untouched by this repair — a different row (row 5) than the ones repaired |
| `VOLATILE VALUE` | Unaffected. §7.2's service-limit register still carries DC-D-049's run-duration figures with the same re-verify instruction; the reclassification changes DC-D-049's **exit class**, not its **volatility status** |
| `INF` | Unaffected. AP-D-059's composition is still stated as `INF` synthesis (Confidence: MEDIUM), and the new Class column does not change that classification's basis |
| `COMPARATOR EVIDENCE ABSENT` | **Strengthened, not weakened.** Form (b) of class 13's render template now states this marker explicitly where it was previously silent, closing a gap rather than opening one |

No state was converted from a weaker to a stronger claim anywhere in this repair. Where a new class assignment was made (DC-D-049 → `Ri`, DC-D-068 → `Xc`; three composed rows given an explicit Class), each is a **narrower, more accurate** statement than what it replaced (an unconditioned exit, or no stated outcome at all), never a more certain one.

## 11. Mechanical Regression Check

All figures independently recomputed from the repaired files, not copied from this report's own narrative.

| Check | Result |
|---|---|
| Duplicate `DC-D-*` ids | **0** (116 definitions) |
| Duplicate `AP-D-*` ids | **0** (68 definitions) |
| Duplicate `ALT-*` ids | **0** (11 definitions) |
| Dangling `DC-D-*` / `AP-D-*` / `ALT-*` references, all four files | **0 / 0 / 0** |
| Body class distribution (recomputed from all 116 `PP negative/exit` fields) | `Xp` 15 · `Xr` **26** · `Xe` 5 · `Xc` **8** · `Ri` **7** · `Cf` 17 · `—` 38 — sum 116 |
| Body class == register class == matrix class | **116 / 116, 0 mismatches** |
| Domain table recomputed from criterion ids, matched against published table | **exact match**, all 12 domains, all 9 class columns |
| `Xc` set == criteria named in a registered matrix §3 row, both directions | **8 == 8, 0 divergence** (DC-D-001, 015, 037, 063, 064, 068, 080, 104) |
| Matrix §3 tables — pipe count per row (structural validity) | **7 pipes / 6 columns, all 12 rows, both tables — consistent** |
| ALT-004 / AP-D-* orphans introduced by trimming DC-D-049's `Related alternatives` | **0** — ALT-004 remains cited by other criteria; no alternative or anti-pattern class lost its last reference |
| Every criterion still names ≥1 anti-pattern, ≥1 alternative, a `Lineage` field | **116 / 116 / 116** |

**No mechanical check regressed.** The repair reduced the direct-exit count (48 → 46) and increased the non-exit-consequence count (61 → 62 rows that cannot reject the platform) — both in the same direction the review chain has moved in every prior repair, and both independently reproduced from the edited files rather than asserted.

## 12. Adversarial Regression Results

### 12.1 The two scenarios that caused the gate's regression failure — re-run, using the required format

**A-01 / T-17 — Multi-month approval process**

```
REQUIREMENTS        → Capital-expenditure approval, 90–120 days end to end, human-review
                       dominated, single-department ownership, no external component.
CRITERIA             → DC-D-049 `BEYOND 30 DAYS` · DC-D-103 (audit retention) ·
                       DC-D-006 (ownership) · DC-D-070/073 (no operator needed).
PP VIABILITY         → Viable. The run mechanism becomes unavailable at the 30-day
                       ceiling; the documented answer is a business record with a
                       re-triggering automation, entirely in-platform.
EXCLUSIONS           → None. DC-D-049 is `Ri`, not an exit.
CANDIDATE SET        → None required. ALT-005/ALT-006 remain candidates only for a
                       future requirement genuinely needing external orchestration.
COMPARATOR EVIDENCE  → N/A — no exit fires, so no candidate set is generated.
                       (Where cited, ALT-005/006 are `CONSTRAINED` on this exact axis,
                       per §4A.2 — worse, not better, than the in-platform answer.)
OUTCOME              → PP_VIABLE_WITH_CONSTRAINTS (class 2) — the business-record
                       pattern is the named condition.
```

**Before Repair V3, had this scenario been run:** `Xr` → §2.5's mapping → classes 3/4/6; no operator and no hybrid shape available → class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` → class 8, naming ALT-005/ALT-006 as unranked candidates the corpus itself records as constrained on the triggering axis. **Corrected.**

**A-02 / T-18 — Per-user authorization through a mediation tier**

```
REQUIREMENTS        → Expense-reimbursement workflow; downstream finance system
                       enforces per-user authorization; a facade calls it as a shared
                       service identity; propagation feasibility not yet known.
CRITERIA             → DC-D-068 `TARGET ENFORCES PER USER` (shared-identity
                       intermediary) · DC-D-036 (integration ownership) ·
                       DC-D-060 (registered in the same row).
PP VIABILITY         → Undetermined pending the propagation question — not excluded
                       either way.
EXCLUSIONS           → None on this criterion alone, and none in combination unless
                       identity propagation is confirmed impossible AND no
                       compensating authorization design exists (neither is
                       established here).
CANDIDATE SET        → None named. No off-platform destination anywhere in the
                       criterion's own field.
COMPARATOR EVIDENCE  → N/A — no exit fires, so no candidate set is generated.
OUTCOME              → DECISION_BLOCKED (class 12) on the propagation question →
                       PP_VIABLE_WITH_CONSTRAINTS (class 2, explicit delegated
                       identity as the condition) once resolved yes, or class 12
                       continuing pending a compensating-authorization design if no.
```

**Before Repair V3, had this scenario been run:** `Xr` → same mapping → class 6 reachable for an in-platform authorization design constraint naming no off-platform destination anywhere in the criterion. **Corrected.**

**Verified especially: excluding Power Platform does not select an unevaluated alternative.** Neither repaired scenario excludes Power Platform at all, which is the stronger form of the test — the pre-repair defect was not a bad *choice* of alternative on exclusion, it was a *false exclusion* that then reached for alternatives the corpus documents as worse. Both are now closed at the source: no exit fires, so no candidate set is generated, so no alternative-preference question can arise.

### 12.2 Adjacent scenarios sharing the repaired rule — re-checked, not merely re-run

All eighteen scenarios' `**Criteria triggering**` lines were scanned for DC-D-049 and DC-D-068.

- **T-16** is the only existing scenario citing DC-D-068 (*"whose identity the assistant reads as"*). Re-checked: T-16's `DECISION BLOCKED` outcome rests on the agent-governance, commercial and modality grounds already stated there (DC-D-116, U-14's unowned deferral) — not on DC-D-068's exit class. **Unchanged.**
- **No existing scenario cites DC-D-049.** T-17 is its first exercise.
- **T-04, T-07, T-08, T-09, T-12, T-13, T-14** (the scenarios that reject, displace or block Power Platform on other grounds) were confirmed to rest on `Xp`, `Xe`, or `Xr` criteria this repair did not touch. **None softened, none changed.**
- **T-01 through T-15** (all sixteen pre-existing scenarios): re-read in full against the repaired files. **Zero substantive-conclusion changes.**

### 12.3 The twelve composed disqualifier rows — spot-checked against their new Class column

Each row's new `§6.2 outcome` was tested against its own stated consequence text (not merely asserted): rows concluding an unavailable pattern (1, 2, 7, 8, 10, 12) → class 5; the unfunded-control row (3) → class 7, matching class 7's own trigger wording (*"infeasible where a mandated control is unfunded"*) rather than class 5's capability wording; the unevidenced-commitment row (4) → class 12, because three of its four criteria (DC-D-001, 080, 100) are themselves in `decision-criteria.md` §5.2's blocking set; the sizing-conflict row (5) → class 12, because DC-D-039 is itself `CONFLICTED` and `B`; the authorization row (6, DC-D-068's own) → class 2 or 12 per the propagation condition; the migration row (11) → class 14, unchanged from V2; the sponsor-decision row (9) → class 11 or 12, explicitly **never** a Power Platform exclusion class, because the maturity gap recurs on every platform.

### 12.4 Full scenario count after repair

| | Before Repair V3 | After Repair V3 |
|---|---|---|
| Scenarios tested | 16 | **18** |
| Passing | 14 | **16** |
| Exposing gaps (unchanged, out of this repair's scope) | 2 (T-14, T-04) | 2 (T-14, T-04) |
| Rejecting, displacing or blocking Power Platform | 12 of 16 | **13 of 18** |

**`FAILED GATE REGRESSION SCENARIOS NOW PASS: YES`** — both A-01/T-17 and A-02/T-18 now produce the class the corpus's own evidence supports, and both are permanent, standing tests rather than one-off audit findings.

## 13. Remaining Open Issues

None of the following are gate-blocking, and none was in scope for this bounded repair. Listed so they are not lost, exactly as they were listed in `block-d-gate.md` §11.

| Id | Severity | Status |
|---|---|---|
| R-03 | MEDIUM, non-blocking | Still open. `decision-intelligence-matrix.md` DC-D-055's row still reads *"the platform's strongest documented differentiator here,"* still carries `AP-D-015` against the body's `AP-D-015, AP-D-027`, and still omits the DC-D-111 precondition. Untouched by this repair — DC-D-055's class is `—` and neither G-H-01 nor G-M-01 involves it |
| R-04 | MEDIUM, non-blocking | Still open. `decision-criteria.md` §9 item 8 still publishes `HIGH 57 · MEDIUM 56 · LOW 3` against a recount of `HIGH 68 · MEDIUM 46 · LOW 2`. No decision behaviour reads this figure |
| R-06 | LOW–MEDIUM, non-blocking | Still open. `V` = 11 in the register against §7.1's *"ten"* and §9 item 4. DC-D-116 is `V`-flagged and absent from §7.1's table |
| V2-M-02 | MEDIUM, non-blocking | Still open, still disclosed. DC-D-046 → `Ri` is contestable on its own evidence (the documented remedy reads as an external-component gate). Mitigated because §3 row 2's operator gate runs independently |
| V2-L-01 | LOW | Still open. DC-D-013 and DC-D-023's exit fields name only in-platform changes while their `Xr` class rests on an off-platform limb stated only in `Decision impact` |
| V2-L-02 | LOW | Still open. Abbreviated outcome labels (`DECISION BLOCKED`, `FIT WITH CONSTRAINTS`) are emitted without the class number; matrix §9's *"verbatim"* claim is technically overstated |
| G-L-01 | LOW | Still open. DC-D-002's matrix row omits ALT-004 (present in the body); DC-D-116's matrix cell and body enumerate the same classes with compatible but non-identical set notation |
| Areas 1–12 lineage defects | recorded, not repaired | `licensing-cost.md`'s duplicate `DC-14` and `integration-architecture.md` §15.8's dangling citation remain, correctly recorded and correctly not repaired by Block D |

**Nothing above requires new research.** All are readable, bounded corrections against material already in the four artifacts, in the same category as this repair's own three fixes — just not gate-blocking, so out of this pass's scope by the task's own instruction.

`NEW RESEARCH REQUIRED: NO` — every finding this repair addressed, and every finding it left open, is resolvable (or already correctly left as a stated evidence gap, e.g. `alternatives.md` §6 items 9–10) from the canonical corpus Block D already cites.

## 14. Final Repair Verdict

Both gate-blocking findings are resolved at the root cause, not patched at the surface:

- **G-H-01** — the `Xr` membership was re-derived from §2.5's own test over the whole class, not re-patched for a named subset. **RESOLVED.**
- **G-M-01** — the render template's comparative clause was structurally confined to the one class it was ever evidenced for, not merely re-worded in place. **RESOLVED.**
- **G-M-02** (forced dependency, non-blocking but necessary for G-H-01's fix to be coherent) — the `Xc` outcome mapping was made per-row rather than global, closing the gap the gate flagged and three latent instances of the same gap elsewhere in the register. **RESOLVED.**

All four cross-file invariants hold after the repair: `decision-criteria.md`'s criteria remain technology-neutral (no vendor/product name entered any Discovery-phase artefact; Block D is the sanctioned Options-phase location); `anti-patterns.md`'s AP-D-059 failure mechanism and triggers are unchanged in substance, only its outcome-routing text was corrected; `alternatives.md`'s eleven classes remain symmetrical and conditional (§2.1–§2.3 untouched); `decision-intelligence-matrix.md` no longer overstates the decision beyond evidence at the one point the gate found it did. The same semantic rule now produces the same output in all four files — verified mechanically (§11) rather than asserted.

This repair did not reopen R-01…R-14 beyond the two the gate named, did not touch Areas 1–12, did not canonicalise, and did not begin PP pack authoring.

`GATE HIGH FINDING RESOLVED: YES`
`GATE-BLOCKING MEDIUM FINDING RESOLVED: YES`
`TECHNOLOGY NEUTRALITY REPAIRED: YES`
`FAILED GATE REGRESSION SCENARIOS NOW PASS: YES`
`DOWNSTREAM AUTHORING SAFETY REPAIRED: YES`
`NEW RESEARCH REQUIRED: NO`
`READY FOR FINAL BOUNDED GATE RECHECK: YES`

---

**Not performed, by instruction:** the Block D gate recheck · canonicalisation of Block D · PP pack authoring · any new research · any reopening of R-03, R-04, R-06, V2-M-02, V2-L-01, V2-L-02 or G-L-01 beyond recording their status · any modification of Areas 1–12 · any modification of files outside `research/pp/evidence/`.
