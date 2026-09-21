# PP Pack Authoring — Step 2 Discovery Layer — Independent Gate Review

**Step:** PP PACK AUTHORING — STEP 2 GATE (independent adversarial review)
**Date:** 2026-09-03
**Reviewer role:** independent adversarial reviewer. Did not author the Discovery layer. Did not edit any file under review, any canonical research file, or the Authoring Map.
**Path resolution:** the repository has no top-level `research/`. Per the Authoring Map's own §-header convention, the requested `research/pp/authoring/gates/step-2-discovery-layer-gate.md` resolves to `docs/pp-pack-authoring/research/pp/authoring/gates/step-2-discovery-layer-gate.md`, alongside `docs/pp-pack-authoring/research/pp/authoring/pp-pack-authoring-map.md` and `step-2-discovery-layer-report.md`.
**Method:** 14 independent adversarial reviewer agents (6 per-lens + 8 cross-cutting), each with Read/Grep access to the full canonical corpus and the authored files, followed by adversarial verification: every candidate gate-blocking finding (CRITICAL/HIGH, or MEDIUM self-flagged as gate-blocking) was independently re-examined by 3 skeptic agents instructed to try to refute it. A finding is reported below as **CONFIRMED** only if a majority of skeptics (≥2/3) did not refute it after independently re-reading the cited files themselves. 28 candidates were adversarially verified; 22 survived (CONFIRMED), 6 were refuted and dropped.

---

## 1. Verdict

**FAIL.** The authors' self-reported gate line (`READY FOR STEP 2 AUTHORING GATE: YES`, zero contamination, zero broken references, full canonical grounding) does not survive independent verification.

The actual Discovery-round content (the questions and signals a participant would be asked) is **technology-neutral and largely well-grounded** — no confirmed finding shows a vendor/product leak into live Discovery conversation, and the five-outcome bias check independently holds. The gate fails on a narrower, but real and repeated, set of defects: **citation/traceability breaks** (a canonical id cited as a signal's basis with no actual eliciting question — most seriously `DC-D-071`, found independently by 5 of the 14 review agents), **cross-lens signal fragmentation** (a signal declared in one lens's `pack.yaml` block but only ever answerable from a different lens's question), **two missing decision-blocking evidence items** the canonical corpus itself flags as blocking at scale (`DC-D-085` concurrency, `DC-D-089` capacity-proof), and **a stale, partly vendor-tagged signal catalog** left in `lens-governance/SKILL.md` that the Step-2 rewrite never reconciled. None of these are structural — all 18 confirmed gate-blocking findings are fixable by editing the existing three files (plus, in one case, a SKILL.md line) with no new research required.

## 2. Evidence inspected

**Authoring contract:** `docs/pp-pack-authoring/research/pp/authoring/pp-pack-authoring-map.md` (§3.1, §4.1, §5, §6, §8), `docs/pp-pack-authoring/research/pp/authoring/step-2-discovery-layer-report.md` (authors' self-report, treated as a claim to verify, not evidence).
**Canonical manifest:** `docs/pp-pack-authoring/research/pp/evidence/canonical-manifest.md`.
**Canonical Areas 1–12:** `platform-suitability.md`, `application-architecture.md`, `data-architecture.md`, `automation-architecture.md`, `integration-architecture.md`, `security.md`, `governance.md`, `alm-devops.md`, `performance-scale.md`, `licensing-cost.md`, `operations-support.md`, `architecture-patterns.md` (all under `docs/pp-pack-authoring/research/pp/evidence/`).
**Block D:** `decision-criteria.md` (116 `DC-D-*`), `anti-patterns.md` (68 `AP-D-*`), `alternatives.md` (11 `ALT-*`), `decision-intelligence-matrix.md`.
**Authored files under review:** `library/packs/pp/glossary.md`, `library/packs/pp/question-bank.md`, `library/packs/pp/pack.yaml`.
**Kernel contracts:** `library/kernel/phases.md`, `library/kernel/states.md`, `library/kernel/orchestration.md`, `library/kernel/glossary.md`.
**Pack authoring guide:** `docs/PACK_AUTHORING.md`. **Rule:** `.claude/rules/no-tech-mention-before-options.md`.
**Lens contracts consulted for grounding (not primary review targets):** `.claude/skills/lens-{business,operations,user,data,governance,financial}/SKILL.md`.

No web research was performed. No file was edited.

## 3. Canonical grounding review

Representative-but-adversarial sampling across all six lenses (all Core questions, ≥half the Probes per lens, every `extra_signal`, every glossary section) traced backward to canonical evidence. Overall: the large majority of citations hold up — ids exist, sit in the right file/area, and their content genuinely supports the authored claim. Confirmed semantic-citation-laundering instances (a real id attached to a question/signal it does not actually support) survived adversarial verification in four places:

- **Business** — `requester_vs_sponsor_authority` (pack.yaml) cites `DC-D-006`, but `DC-D-006` is entirely about accountable-ownership *acceptance*; the word "requester" does not occur anywhere in the checked canonical corpus (GATE-12).
- **Operations** — `Q-OPS-03` and `P-OPS-10` both cite `operations-support.md §2.4`, which is entirely Power-Platform backup/restore/pipeline content with no bearing on business-process queue depth or exception counting; neither `DC-D-049` nor `DC-D-054`'s own canonical Lineage line cites that file at all (GATE-01).
- **Operations** — the `as_is_variant_count` signal cites `DC-D-005` ("how many variants exist and why"), but no Core or Probe question asks about process variants, and `question-bank.md` Appendix B falsely labels `Q-OPS-07` as producing that evidence (GATE-02).
- **User** — `frontline_versus_reported_reality` cites `AP-D-001`, which is entirely about premature vendor/technology naming and has zero content on performer-vs-manager perspective divergence (GATE-14).

One candidate in this category (`BUS-01`, `Q-BUS-08`'s citation of `AP-D-036`) was **refuted 3/3** on adversarial verification: while `AP-D-036` is indeed unrelated to prior-attempt evidence, the two skeptic agents that dug deepest judged the loose fit bounded enough (the question is still well-grounded by its other two citations) not to independently gate the review — see §15.

No case was found, anywhere, of a canonical `VOLATILE`/`CONFLICTED`/`UNKNOWN` marker being silently resolved into an unconditional Discovery claim, or of a qualified/conditional finding being restated as a timeless rule. `DC-D-021`'s `CONTESTED` state is correctly routed to a Conflicted SU row (`P-DAT-01`); `DC-D-072`'s `VOLATILE` tag is correctly preserved in `Q-GOV-05`'s citation; `DC-D-113`/`115`/`116`'s `B*` scoping is preserved verbatim.

## 4. Technology-neutrality attack

`DISCOVERY TECHNOLOGY NEUTRALITY: PASS` (confirmed independently).

A from-scratch literal sweep (Power Platform, Power Apps, Canvas Apps, Model-driven Apps, Dataverse, Power Automate, Power Fx, SharePoint, Microsoft Lists, Power Pages, Copilot, connector(s), premium licensing, environment(s), solution(s), ALM — plus tenant/DLP/Excel/Outlook/Teams/Azure/gateway/citizen-developer/low-code/plugin/security-role) over `glossary.md` Part A, `question-bank.md` Parts 1–2 + Appendix A/B, and `pack.yaml`'s Discovery `lenses_config` found **zero VIOLATION classifications**. Every literal hit is either the pack's own self-identifying metadata (title, `display_name`, description), inside Part B's explicitly quarantined (`options+`) translation table, or inside `question-bank.md` Appendix C / `pack.yaml`'s `technology:`/`domain_knowledge:` blocks — all explicitly out of Step-2/Discovery scope by the files' own comments.

Semantic-contamination hunting (disguised Dataverse-shaped questions, assumed-automation, assumed-app-exists, disguised product-selection signals, MS-tenant-shaped governance questions, MS-licensing-framed financial questions) found **no confirmed violation**. One naming-only nit survived: the governance signal `maker_and_delivery_model` retains "maker" (low-code vernacular), inconsistent with the authors' own demonstrated discipline of stripping "connector" from `service_permissibility_posture` — LOW, non-gate-blocking (`NEUT-01`).

**Caveat that does affect the verdict at the boundary of scope (GATE-03):** the Discovery round is not fully governed by the 3 files Step 2 authored — the compliance-officer agent's actual runtime instructions are `lens-governance/SKILL.md`, which still lists `DLP_policies` and `sensitivity_labels` as "pp pack additions" in its signal catalog. Both are literal Microsoft product/feature nomenclature (Power Platform DLP policies; Microsoft Purview/Information Protection sensitivity labels), sitting in a file that governs a live Discovery round, and neither matches any of the 20 signals the Step-2 rewrite actually declared. This is a real, confirmed neutrality/traceability gap at the edge of what "the Discovery layer" functionally means — flagged as gate-blocking because it means the authors' zero-contamination claim is true only for the 3 files they touched, not for the mechanism that actually executes the round.

## 5. Outcome-neutrality regression

`DISCOVERY OUTCOME NEUTRALITY: PASS` (confirmed independently, via freshly-constructed scenarios, not by co-signing the authors' own Appendix B).

One scenario was built per outcome and walked through the actual Core/Probe/signal set:

| Outcome | Reachable without off-script questions? | Load-bearing Core questions |
|---|---|---|
| 1. Platform fits | Yes (default/null state) | — |
| 2. Fits with material constraints | Yes | Q-GOV-02, Q-GOV-06, Q-GOV-08, P-FIN-01 |
| 3. Another technology preferable | Yes (3 independent sub-paths: compute, atomicity, deployment) | Q-GOV-02, Q-DAT-08 (Core, not buried) |
| 4. Process change, no new technology | Yes | Q-BUS-07, Q-OPS-07 |
| 5. Do nothing / defer | Yes (most robustly Core-anchored) | Q-FIN-02, Q-FIN-03, Q-BUS-04 |

No structural bias was found favoring platform-fits answers: disqualifying/redirecting evidence is not confined to buried probes (outcomes 2–5 each have ≥2 unconditional Core questions), and there is no separate "confirming register" phrased more strongly than the disqualifying one. One non-blocking defect: the authored Appendix B self-check omits the bank's single strongest platform-exit pair (`Q-DAT-03`/`P-DAT-09`, tracing to `DC-D-023`/`DC-D-040`) from its own outcome-3 justification — the underlying questions work correctly, only the self-check's bookkeeping is incomplete (`GRD-NEUT-01`, MEDIUM, non-gate-blocking).

## 6. Lens coverage review

All six lenses cover their required topic checklist substantially, mostly through a mix of Core questions, Probes, signals and glossary terms (per the gate's own rule, not every topic needs a Core Question). Genuine, confirmed gaps:

- **User** — *adoption/training* is entirely uncovered by both the universal lens-user baseline and the pack's additions (`USR-04`, MEDIUM, non-gate-blocking — the canonical corpus itself is nearly silent here, so this is as much a corpus gap as an authoring one; flagged per the task's explicit checklist).
- **Operations** — *ownership* is intentionally out of scope (owned by Business), consistent with the universal lens contract — not a defect.
- **Governance** — *environment/isolation-domain topology* (`DC-D-071`) has a glossary term and a signal but **no eliciting question anywhere** — see §11 (GATE-08, HIGH).
- **Financial** — *operating-cost sensitivity* (`DC-D-097`, support/monitoring/on-call cost tier) is only asked when an external party builds the solution — the majority "built internally" case reaches Options with this cost line unasked (GATE-05, HIGH).

Full per-lens coverage tables are preserved in the review's working data; condensed to the confirmed gaps above for this report per the bounded-gate rule (a topic answered by *some* mechanism is not reported as a gap).

## 7. Question economics and usability

Whole-bank and per-lens attacks found the bank operationally usable, with five candidate defects raised and **four refuted on adversarial verification**:

- `QB-ECON-01` (Q-BUS-07/Q-FIN-01 cross-lens duplicate cost elicitation) — refuted 2/3: skeptics judged the two questions distinct enough in framing (and the corpus's own §3.2 near-duplicate-cluster mechanism not intended to be exhaustive) not to independently gate.
- `QB-ECON-02` (frequency asked in 3 lenses) — refuted 2/3, same reasoning (the three questions operate at genuinely different granularities: group cadence / instance volume / per-actor rate).
- `QB-ECON-03` (Q-BUS-03's "does a product category exist" as an opinion question) — refuted 3/3: the clause is a near-verbatim, deliberate lift of `DC-D-002`'s own Discovery-evidence field, not an invented ask.
- `QB-ECON-04` (P-GOV-14 four-part compound probe) — refuted 2/3: the three canonical ids it bundles are confirmed thematically coherent (all ALM-precondition facts elicited together is defensible), though 1/3 still flagged partial-capture risk as real.

One proportionality observation survives as non-blocking: the Probe tier (up to 14 for Governance, 12 for Data) sits outside `docs/PACK_AUTHORING.md`'s stated "5–8 per lens" norm, which never anticipated a Core/Probe split (`QB-ECON-05`, MEDIUM, non-gate-blocking — the weight is substantively defensible given Governance's concentration of decision-blocking criteria, but the governing doc was not updated to say so).

No true duplicate, no vague/unanswerable question, no stakeholder-collapsing question, and no undetectable probe trigger were confirmed anywhere in the bank.

## 8. Five-state compatibility

Confirmed compatible overall. The bank is demonstrably not confirmatory-only: ~20 items are explicitly tagged "decision-blocking when unknown," 5 are tagged `VOLATILE`, `P-DAT-01` explicitly instructs recording a cross-team figure disagreement as **Conflicted, not resolved by the lens**, and the glossary's own A11 vocabulary (`Contested authority`, `Provability gap`, `Decision-blocking unknown`) routes directly into the kernel's 5-state model. Every lens agent found a plausible path to Confirmed, Assumed, Unknown and Risky from its own question set.

One bounded asymmetry, non-gate-blocking: the Financial lens has no analogue to Data's `P-DAT-01` for surfacing a stakeholder disagreement on a cost/budget figure as Conflicted (`GRD-FIN-03`, MEDIUM, non-gate-blocking — a lens operator can still record it from inline judgment, and cross-lens Conflicted rows still arise at Framing).

## 9. Cross-lens contradiction capability

`PASS`, confirmed. All 9 required tension pairs (business urgency vs governance constraints; user need vs security/privacy; operational convenience vs SoD; data freshness vs integration reality; process volume vs operational capacity; expected benefit vs cost envelope; frontline vs management workflow; availability/continuity vs support ownership; growth vs current operational model) have a plausible discovery path through named questions/signals on both sides, and the combined evidence model is explicitly engineered — not incidental — to expose tension: `lens-governance/SKILL.md`'s "Conflict scan" step, `chairman-synthesis`'s "surface contradictions as Conflicted, never silently pick a winner," and Appendix B's outcome-reachability guard all actively push the bank away from confirmation-only design.

One non-blocking observation: the explicit "Conflict scan" instruction exists only in `lens-governance/SKILL.md`, not the other five lens contracts, so Discovery-phase (as opposed to Framing-phase) detection of the 5 non-governance-adjacent pairs depends on ad hoc judgment — fully backstopped by `chairman-synthesis` at Framing, and this predates Step 2 (kernel/lens-contract characteristic, not introduced by this authoring step) (`GRD-XLENS-01`, MEDIUM, non-gate-blocking). A second, LOW observation: the "data freshness vs integration reality" pair has no dedicated supply-side signal (`GRD-XLENS-02`).

## 10. Downstream Decision sufficiency

`DOWNSTREAM DECISION SUFFICIENCY: FAIL` (confirmed).

34 `DC-D-*` criteria were sampled across Business/Integration/Automation/Security/Governance/ALM/Performance-Scale (exceeding the required 25), each independently traced from its canonical "Discovery evidence" field to whichever question/signal/glossary term claims to elicit it. ~27 of 34 are genuinely, often elegantly, covered. Two confirmed HIGH gaps sit exactly where the canonical corpus itself marks its own decision-blocking thresholds:

- **`DC-D-085` (User concurrency)** — explicitly "Blocking. UNKNOWN is decision-blocking at THOUSANDS and above." No question anywhere asks for simultaneous/concurrent users at peak; the closest candidates (`Q-USR-04` per-person frequency, `Q-OPS-06`/`P-DAT-09` instance/message volume) are different quantities (GATE-06).
- **`DC-D-089` (Provability of capacity before commitment)** — the criterion the corpus uses to convert "scale anxiety without a number" into a documented exit (`Xr`). No question asks whether a sponsor/contract requires proof of capacity, or whether a bounded pilot is fundable (GATE-07).

A third, already covered under Traceability (§11/GATE-08): `DC-D-071` (environment strategy). A fourth, meta-level finding: the authors' own §6/§8 traceability-validation claim ("113 cited by exact string; the remaining 3 ... by range header") is arithmetically wrong on independent re-extraction — **7** ids (`DC-D-039, 046, 071, 082, 085, 086, 089`), not 3, are range-only, and the 4 undisclosed ones are exactly where the real gaps above live (GATE-17). Four further, non-gate-blocking missing-evidence items were also confirmed but judged bounded in effect: `DC-D-046` contract volatility (no cadence/breaking-change question), `DC-D-086` request-rate identity concentration, and a partial evidence gap on `DC-D-060`/`Q-GOV-03` (identity-provider/PIM/conditional-access facts) and `DC-D-077`/`Q-GOV-07` (release cadence/window) — see §15.

No case of semantic laundering was found in this pass beyond what is already reported in §3/§11 — qualified/`VOLATILE`/`CONFLICTED` markers were consistently preserved.

## 11. Traceability integrity

`TRACEABILITY INTEGRITY: FAIL` (confirmed).

`BROKEN CANONICAL REFERENCES: 0`. Across an exhaustive sweep of `glossary.md` (186 references/ids checked, full ranges expanded) and `question-bank.md`+`pack.yaml` (152 unique canonical ids, ~350+ citing occurrences), **no id or section reference was found that does not exist, or that resolves to the wrong canonical file/area.** The authors' `BROKEN CANONICAL REFERENCES: 0` claim is independently confirmed accurate as literally stated.

`SEMANTICALLY UNSUPPORTED REFERENCES: 6` (confirmed), by two distinct sub-patterns:

1. **Citation does not support the claim it is attached to** (4 instances): `BUS-03` (DC-D-006 ↛ "requester"), `OPS-01` (operations-support.md §2.4 ↛ queue/exception evidence, cited twice), `USR-01` (AP-D-001 ↛ frontline-reality), and Appendix B's mislabeling of `Q-OPS-07` as producing variant evidence it does not ask for (part of `OPS-02`/GATE-02).
2. **Shared "decision-blocking" status over-attributed to a co-cited id that does not itself carry it** (2 instances, found by the dedicated question-bank traceability sweep, non-independently-gating): `Q-GOV-06` attributes blocking status to both `DC-D-073` and `DC-D-102`, but only `DC-D-073` is in the canonical §5.2 blocking set; `P-GOV-03` does the same for `DC-D-044`/`DC-D-063`. The authors demonstrate elsewhere (`Q-DAT-08`, `P-GOV-07`) that they know how to scope this precisely, making these two inconsistent with the pack's own established discipline rather than a format limitation.

**The pack's own self-policing traceability convention** ("the same id appears on the matching question — grep it to find signal, question and evidence together, no separate index," `question-bank.md` Appendix A / `pack.yaml`:46-47) **fails outright for one signal, independently discovered and confirmed by 5 of the 14 review agents** (lens-governance, neutrality-resweep, downstream-sufficiency, traceability-questionbank, internal-consistency): **`DC-D-071` / `environment_isolation_requirement`** is declared as a governance signal and has a glossary term, but is cited by **zero** Core questions, Probes, or Appendix A entries — the only signal-id pair (out of ~83 checked) with this property (GATE-08, merged from `GRD-GOV-02`/`TRACE-01`/`GRD-DEC-03`/`TRC-01`/`CONS-02`). Three further, independently confirmed instances of the same convention breaking across a lens boundary (not id-nonexistence, but the id's *only* eliciting question sitting in a different lens than the signal declares):

- **`DC-D-061`** (external identity requirement) — declared as a **governance** signal; only elicited by `Q-USR-02`/`P-USR-02` in the **User** lens (GATE-09/CONS-01).
- **`DC-D-045`** (interface availability) — declared as both an **operations** and a **data** signal; only `P-OPS-04` (operations) actually cites it (GATE-10/CONS-03).
- **`DC-D-024`** (total data volume/growth) — declared as a **data** signal; the only citing question (`Q-FIN-08`, financial) asks a different framing and omits retention/history-in-scope/attachment-counting, which `DC-D-024`'s own Discovery-evidence field names (GATE-11/CONS-04).

## 12. Internal consistency

Confirmed defects beyond §11's cross-lens fragmentation:

- **`CONS-05`/GATE-18**: the Authoring Map's own rule **N-06** names six "Step-0 absolutes" that "can terminate the platform question" and warns that deferring them "wastes the engagement." Four (`DC-D-108`, `DC-D-033`, `DC-D-059`, `DC-D-062`) are correctly placed as unconditional Core questions; the other two (`DC-D-028` atomicity, `DC-D-057` compute-intensity) are demoted to trigger-gated Probes — contradicting N-06's own stated rationale for exactly these six ids, and `question-bank.md`'s own Structure section, which reserves Probe for trigger-gated content and Core for "almost every engagement."
- The §6.2 contamination-inventory table (spot-checked 10+ rows) and the Part B "two deprecated tools" factual claim (`GOV-12`/`ALM-22`) are both faithfully implemented — no defects found there.
- No case was found of the same concept receiving two genuinely different names across lenses in a way that would fragment the Shared Understanding **beyond** the three cross-lens-fragmentation cases already reported in §11 (which are a naming/ownership mismatch, not a definitional contradiction).

## 13. Findings table

52 raw findings were produced; 28 were selected as gate-blocking candidates and adversarially verified (22 CONFIRMED, 6 REFUTED); the remaining 24 were LOW or self-flagged non-gate-blocking MEDIUM and are reported in §15 without independent verification (per the gate's own proportionality rule — verification effort was concentrated on candidate gate-blocking findings). After merging 5 independently-discovered reports of the identical `DC-D-071` defect into one, and folding one repeated Appendix-B mislabeling into its parent finding, **18 distinct findings are gate-blocking** (11 HIGH, 7 MEDIUM; 0 CRITICAL).

| ID (report) | Source finding id(s) | Severity | Category | Verdict |
|---|---|---|---|---|
| GATE-01 | OPS-01 | HIGH | evidence-integrity | CONFIRMED (0/3 refuted) |
| GATE-02 | OPS-02 | HIGH | coverage-gap / citation-laundering | CONFIRMED (0/3 refuted) |
| GATE-03 | GRD-GOV-01 (+ OPS-06, BUS-04 as related, unverified LOW instances) | HIGH | technology-neutrality / traceability | CONFIRMED (0/3 refuted) |
| GATE-04 | GRD-FIN-01 | HIGH | unsupported-specificity | CONFIRMED (0/3 refuted) |
| GATE-05 | GRD-FIN-02 | HIGH | coverage-gap | CONFIRMED (1/3 refuted, majority holds) |
| GATE-06 | GRD-DEC-01 | HIGH | missing-discovery-evidence | CONFIRMED (0/3 refuted) |
| GATE-07 | GRD-DEC-02 | HIGH | missing-discovery-evidence | CONFIRMED (0/3 refuted) |
| GATE-08 | GRD-GOV-02, TRACE-01, GRD-DEC-03, TRC-01, CONS-02 (merged, 5 independent reports) | HIGH | traceability / downstream-sufficiency | CONFIRMED (0/15 skeptic votes refuted) |
| GATE-09 | CONS-01 | HIGH | cross-lens-fragmentation | CONFIRMED (1/3 refuted, majority holds) |
| GATE-10 | CONS-03 | HIGH | cross-lens-fragmentation | CONFIRMED (0/3 refuted) |
| GATE-11 | CONS-04 | HIGH | unbacked-signal | CONFIRMED (1/3 refuted, majority holds) |
| GATE-12 | BUS-03 | MEDIUM | citation-laundering | CONFIRMED (0/3 refuted) |
| GATE-13 | OPS-03 | MEDIUM | evidence-integrity | CONFIRMED (0/3 refuted) |
| GATE-14 | USR-01 | MEDIUM | semantic-citation-laundering | CONFIRMED (0/3 refuted) |
| GATE-15 | DAT-01 | MEDIUM | question-design | CONFIRMED (0/3 refuted) |
| GATE-16 | DAT-02 | MEDIUM | coverage-gap | CONFIRMED (0/3 refuted) |
| GATE-17 | GRD-DEC-08 | MEDIUM | self-audit-accuracy | CONFIRMED (0/3 refuted) |
| GATE-18 | CONS-05 | MEDIUM | internal-contradiction | CONFIRMED (1/3 refuted, majority holds) |
| — | BUS-01 | MEDIUM | citation-laundering | **REFUTED** (3/3) — dropped |
| — | GRD-GOV-03 | MEDIUM | question-economics | **REFUTED** (2/3) — dropped |
| — | QB-ECON-01 | HIGH | cross-lens-duplicate | **REFUTED** (2/3) — dropped |
| — | QB-ECON-02 | MEDIUM | cross-lens-duplicate | **REFUTED** (2/3) — dropped |
| — | QB-ECON-03 | MEDIUM | opinion-not-evidence | **REFUTED** (3/3) — dropped |
| — | QB-ECON-04 | MEDIUM | compound-question | **REFUTED** (2/3) — dropped |

24 further LOW / self-flagged-non-blocking findings (`BUS-02,04,05`; `OPS-04,05,06`; `USR-02,03,04,05`; `DAT-03`; `GRD-GOV-04`; `GRD-FIN-03,04`; `NEUT-01`; `GRD-NEUT-01`; `GRD-DEC-04,05,06,07`; `GRD-XLENS-01,02`; `CONS-06`; `QB-ECON-05`) were not independently adversarially verified and are listed in §15.

## 14. Gate-blocking findings

### GATE-01 — HIGH — wrong canonical section repeatedly cited (Operations)
**Artifact:** `library/packs/pp/question-bank.md:70` (Q-OPS-03) and `:279` (P-OPS-10).
**Canonical evidence:** `operations-support.md` §2.4 (lines 179-251, OP-14..OP-23) — entirely Power-Platform backup/restore/pipeline/capacity content. Neither `DC-D-049`'s nor `DC-D-054`'s own canonical Lineage line cites `operations-support.md` at all; the Authoring Map's own table names `operations-support.md §11` as the intended anchor.
**Defect:** Both questions append "operations-support.md §2.4" as canonical support for business-process queue depth (Q-OPS-03) and exception-path counting (P-OPS-10). §2.4's actual content has no bearing on either claim — confirmed by 3/3 independent skeptics reading the section directly.
**Why it matters downstream:** Grepping the cited section, exactly as the pack's own stated convention instructs, leads a maintainer to content that does not support the claim — repeated identically across two questions, not a one-off typo, which undermines the specific self-audit mechanism the pack designed for itself.
**Minimum bounded repair:** Replace "operations-support.md §2.4" with "§11" (or drop the file-level citation and keep `DC-D-049`/`DC-D-054`+`AP-D-018`, which already support the questions alone) in both locations.
**New research required:** No.

### GATE-02 — HIGH — orphaned variant-count signal + false Appendix B label (Operations)
**Artifact:** `library/packs/pp/pack.yaml:65` (`as_is_variant_count`); `library/packs/pp/question-bank.md:479` (Appendix B row).
**Canonical evidence:** `DC-D-005` (decision-criteria.md:470-491) — Discovery evidence explicitly asks "how many variants exist and why"; Decision impact: VARIABLE → standardisation before automation (`ALT-002`).
**Defect:** No Core or Probe question in the Operations set asks about process variants across teams/sites. Appendix B nonetheless labels `Q-OPS-07` as producing "(unjustified variants)" evidence for the "process change, not technology" outcome — `Q-OPS-07`'s actual text is about judgement-dependency, not variants. Confirmed by 3/3 independent skeptics reading `DC-D-005` and `Q-OPS-07` directly.
**Why it matters downstream:** `DC-D-005`'s VARIABLE state is a documented decision-impact branch; if no question elicits it, an engagement can silently skip the evidence for that branch while the pack's own outcome-reachability guard falsely reports it as covered.
**Minimum bounded repair:** Add an explicit variant-count question/sub-ask (Core, or a Probe triggered on "more than one team/site performs this"), citing `DC-D-005`; correct the Appendix B row once it exists.
**New research required:** No.

### GATE-03 — HIGH — stale, partly vendor-tagged signal catalog in the runtime lens contract (Governance)
**Artifact:** `.claude/skills/lens-governance/SKILL.md:48` (Signal catalog section). Related, unverified LOW-severity instances of the same pattern: `.claude/skills/lens-operations/SKILL.md:48` (`sharepoint_lists_anchors` — literal vendor name), `.claude/skills/lens-business/SKILL.md:46` (three stale, non-vendor-tagged names).
**Canonical evidence:** `docs/PACK_AUTHORING.md`:87-89 confirms `pack.yaml`'s `extra_signals` is the mechanism the lens actually consults; `library/packs/pp/pack.yaml` lines 127-148 (governance, the artifact actually authored in Step 2) lists 20 signals, none matching SKILL.md's four.
**Defect:** `lens-governance/SKILL.md` still states "pp pack additions: `DLP_policies`, `environment_strategy`, `sensitivity_labels`, `RBAC_complexity`" — none of the 4 match any of the 20 signals `pack.yaml` actually declares, and two (`DLP_policies`, `sensitivity_labels`) are literal Microsoft product/feature nomenclature. Confirmed verbatim by 3/3 independent skeptics.
**Why it matters downstream:** The compliance-officer agent reads `SKILL.md` verbatim as its runtime instructions. The authoring effort's "zero contamination" claim is true only for the 3 files it changed — the mechanism that actually executes a governance-lens Discovery round still carries a stale, partly vendor-tagged signal list.
**Minimum bounded repair:** Update the "pp pack additions" line in `lens-governance/SKILL.md` (and, as a related cleanup, `lens-operations/SKILL.md` and `lens-business/SKILL.md`) to reference the current `pack.yaml` signal names, or make the line generic ("see the active pack's `lenses_config`").
**New research required:** No.

### GATE-04 — HIGH — invented 12-month horizon (Financial)
**Artifact:** `library/packs/pp/question-bank.md:178-179` (Q-FIN-02).
**Canonical evidence:** `licensing-cost.md` LC-28, `alternatives.md` ALT-010 (neither states any horizon); `DC-D-008` ("over the expected lifespan"), `DC-D-004` (states run 1-3yr/3-5yr/>5yr/INDEFINITE); the pack's own glossary A9 "Cost of doing nothing" term ("over a stated horizon").
**Defect:** Q-FIN-02 hardcodes "the next twelve months" as the cost-of-doing-nothing horizon. No cited source states or implies a 12-month window. Confirmed by 3/3 independent skeptics reading LC-28 and ALT-010 directly.
**Why it matters downstream:** A fixed 1-year anchor systematically understates the priced cost of inaction for any multi-year problem (the common case per `DC-D-004`'s own state distribution), biasing the SU row toward "doing nothing looks cheap" — and is internally inconsistent with the pack's own glossary definition of the same term and with Q-FIN-07/Q-FIN-08, which correctly leave the horizon open.
**Minimum bounded repair:** Replace "the next twelve months" with an open-horizon framing, e.g. "What does leaving the situation unchanged cost, over the horizon this decision needs to cover?"
**New research required:** No.

### GATE-05 — HIGH — operational/support cost tier unasked for internal builds (Financial)
**Artifact:** `library/packs/pp/question-bank.md:441-443` (P-FIN-05, only trigger); `pack.yaml` financial `extra_signals` (no `DC-D-097` signal).
**Canonical evidence:** `DC-D-097` (support tier, monitoring, on-call, drills); `AP-D-060` ("licence line treated as TCO"), `AP-D-064` ("operational/security prerequisites omitted from the cost model... often a larger line than the platform licences themselves") — both already cited in the pack's own glossary A9 header as load-bearing.
**Defect:** `DC-D-097` is cited exactly once, gated on "an external party would build it." No Core question, unconditional Probe, or signal surfaces this cost line for internally-built engagements — the majority case this pack targets.
**Why it matters downstream:** `AP-D-060`/`AP-D-064` name this exact omission as the corpus's most consequential, most commonly-observed cost-modelling failure. The current design reproduces it inside the tool meant to prevent it, for every internally-built engagement.
**Minimum bounded repair:** Add a Core question or an unconditionally-checked Probe (e.g. trigger "this will run in production after go-live," true for almost every engagement) mirroring `DC-D-097`'s Discovery-evidence field.
**New research required:** No.

### GATE-06 — HIGH — user concurrency never elicited
**Artifact:** no Q/P entry anywhere; `library/packs/pp/glossary.md` A6 "Concurrency" is definition-only.
**Canonical evidence:** `DC-D-085` (decision-criteria.md:2554) — "Expected simultaneous users at peak... whether all users hit the same records... whether a load test is feasible." Explicitly "Blocking. UNKNOWN is decision-blocking at THOUSANDS and above."
**Defect:** No question asks for simultaneous/concurrent users at peak. `Q-USR-04` (per-person frequency), `Q-OPS-06`/`P-DAT-09` (instance/message volume) are different quantities. Confirmed by 3/3 independent skeptics who checked all three candidate questions directly.
**Why it matters downstream:** This is an explicitly decision-blocking criterion at scale, feeding Options-phase architecture/scale reasoning (`DC-D-089`, `DC-D-086`); Discovery currently never asks for the number.
**Minimum bounded repair:** Add one Core or Probe question, e.g. "At the busiest moment, roughly how many people are using this at the same time — and do they tend to hit the same records?", citing `DC-D-085, DC-D-010, DC-D-030`.
**New research required:** No.

### GATE-07 — HIGH — capacity-proof requirement never elicited
**Artifact:** no Q/P entry anywhere; glossary A6 "Proof requirement" is definition-only.
**Canonical evidence:** `DC-D-089` (decision-criteria.md:2657) — whether a contract/sponsor requires proof of capacity, whether a bounded pilot is fundable, whether a degradation plan is acceptable. Decision impact names a documented exit (`Xr`): "FULL LOAD PROOF REQUIRED where testing against the service is constrained → host the peak-bearing component where load testing is permitted."
**Defect:** No question anywhere asks this. Confirmed by 3/3 independent skeptics.
**Why it matters downstream:** This is the criterion the corpus uses to convert "scale anxiety without a number" into an actual documented exit condition; without it, Options inherits an unknown default and cannot apply the criterion's own exit test.
**Minimum bounded repair:** Add a Probe, e.g. "Trigger: a contract, regulator or sponsor requires proof of capacity before go-live. What evidence would satisfy them, and would a bounded pilot in a representative environment be fundable?", citing `DC-D-089, DC-D-085`.
**New research required:** No.

### GATE-08 — HIGH — `DC-D-071` orphaned across the entire pack (independently found 5 times)
**Artifact:** `library/packs/pp/pack.yaml:142` (`environment_isolation_requirement # DC-D-071`); `library/packs/pp/glossary.md` A7 "Isolation domain" term (line 180) and A8 header (line 184); `question-bank.md` Appendix A (claims completeness).
**Canonical evidence:** `DC-D-071` (decision-criteria.md:2199-2220) — "Discovery evidence: isolation domains required; regions required; lifecycle stages required; whether external audiences need separation; whether the default environment currently holds anything that matters; whether creation is restricted" — plus four independent cost axes. Cross-referenced by `DC-D-001, DC-D-033, DC-D-063, DC-D-074, DC-D-093, DC-D-099`.
**Defect:** `DC-D-071` is declared as a governance signal and cited in the glossary, but appears **zero times** in `question-bank.md` — no Core question, Probe, or Appendix A entry. This is the only orphan among ~83 checked signal-id pairs. Independently discovered by 5 of the 14 review agents (lens-governance, neutrality-resweep, downstream-sufficiency, traceability-questionbank, internal-consistency) via 5 different attack angles, and confirmed by all 15 adversarial-verification skeptic votes across the 3 candidates that went through formal verification (`TRACE-01`, `TRC-01`, `CONS-02`) — the single most independently-corroborated finding in this review. A secondary detail: the glossary citation itself sits under A8's header, not A7's (where the matching term lives), which is a harmless cross-domain overlap per the dedicated glossary-traceability sweep, not a separate defect.
**Why it matters downstream:** Environment topology is a first-order Options/ALM cost and governance driver on four independent cost axes; `DC-D-099` (cost attribution) explicitly depends on it. The authors' own report defers `DC-D-082` as "a near-duplicate of `DC-D-071`, fully covered" — that deferral's justification is itself unsound, since `DC-D-071` is not in fact covered.
**Minimum bounded repair:** Add a Governance (or Operations) Core/Probe question eliciting isolation-domain/region/lifecycle-stage requirements, citing `DC-D-071` directly — e.g. "How many separate isolation domains does this need — by lifecycle stage, by business unit, by region — and is environment creation restricted today?"
**New research required:** No.

### GATE-09 — HIGH — `DC-D-061` cross-lens fragmentation (external identity)
**Artifact:** `library/packs/pp/pack.yaml:132` (governance `external_identity_requirement`) vs `question-bank.md:95, 289` (Q-USR-02, P-USR-02, User lens).
**Canonical evidence:** `DC-D-061` (decision-criteria.md:1944).
**Defect:** `DC-D-061` is declared as a **governance** signal, but every question that elicits it lives in the **User** lens. No governance question anywhere carries it. Confirmed by 2/3 skeptics (1/3 argued the mismatch is real but judged it non-independently-gating; majority held it as gate-blocking given the council-independent-mode consequence below).
**Why it matters downstream:** In council-independent mode (Framing/Options), each persona writes SU rows from its own lens's signals — the governance persona has a signal it can never answer from its own elicitation.
**Minimum bounded repair:** Move `external_identity_requirement` to the User lens's signal list (matching where it is actually elicited), or add an independent governance-lens question, and update Appendix A's "no-owning-criterion" exception table if it stays cross-lens by design.
**New research required:** No.

### GATE-10 — HIGH — `DC-D-045` declared in two lenses, elicited in only one
**Artifact:** `library/packs/pp/pack.yaml:75` (operations `interface_absent_target_present`, DC-D-045/056) and `:116` (data `interface_availability_per_system`, DC-D-045) vs `question-bank.md:255` (P-OPS-04 only).
**Canonical evidence:** `DC-D-045` ("Interface availability and protocol requirement").
**Defect:** `DC-D-045` is cited as the basis for signals in **both** operations and data, but only `P-OPS-04` (operations) actually carries it; the nearest data question (`Q-DAT-08`) is tagged with different ids entirely. Confirmed by 3/3 independent skeptics.
**Why it matters downstream:** The same underlying fact is declared twice under two names in two lenses, but only one lens can actually derive it — risking either a silent gap in the data-lens row, or a duplicate row if a data question citing `DC-D-045` is added later without merging.
**Minimum bounded repair:** Give the data-lens signal its own elicitation, or explicitly document the shared ownership the way Appendix A already does for its two no-owning-criterion signals.
**New research required:** No.

### GATE-11 — HIGH — `DC-D-024` data signal only weakly covered by an unrelated financial question
**Artifact:** `library/packs/pp/pack.yaml:101` (data `total_volume_and_growth`, DC-D-024) vs `question-bank.md:197` (Q-FIN-08, Financial lens).
**Canonical evidence:** `DC-D-024` (decision-criteria.md:998) — Discovery evidence: current volume, records added per period, growth rate/seasonality, whether history is in scope, retention, whether attachments are counted separately.
**Defect:** The only question carrying `DC-D-024` is `Q-FIN-08`, framed around people/volume/machine-work growth for cost planning — it omits retention, history-in-scope, and attachment-counting, all named by `DC-D-024`'s own Discovery-evidence field. The glossary's own A10 table lists "Data volume vs audit volume" as a pair that must not be collapsed, implicitly conceding this is a distinct concept `Q-DAT-03` (tagged `DC-D-023`/`DC-D-088`) does not cover. Confirmed by 2/3 skeptics (1/3 argued the fit was defensibly close; majority held the gap material).
**Why it matters downstream:** The data lens carries a named signal for total-store-volume-and-growth (needed for capacity/entitlement reasoning in Options) that nothing on the data lens's own initiative elicits, and what does get asked omits three of six named evidence items.
**Minimum bounded repair:** Add a data-lens Core question (or extend `Q-DAT-03`) covering total volume/growth/history-in-scope/retention/attachment-counting, citing `DC-D-024`, with its own Part-A glossary term distinct from "Volume."
**New research required:** No.

### GATE-12 — MEDIUM — `requester_vs_sponsor_authority` signal citation unsupported
**Artifact:** `library/packs/pp/pack.yaml:57` (business `requester_vs_sponsor_authority # DC-D-006`).
**Canonical evidence:** `DC-D-006` (decision-criteria.md:495-517) — entirely about accountable-ownership acceptance (NAMED AND ACCEPTED/NOMINAL/NONE). Corpus-wide grep for "requester" returns zero hits.
**Defect:** The signal's sole cited basis does not discuss a requester role or requester-vs-sponsor split at all. Confirmed by 3/3 independent skeptics reading `DC-D-006` in full.
**Why it matters downstream:** Overstates canonical grounding for one signal; the concept is aisa's own kernel-level vocabulary (universal `requester_motivation` signal, glossary A2), not something `DC-D-006` evidences. Low practical harm since `Q-BUS-05`/`P-BUS-03` (which do implement the distinction) are otherwise sound.
**Minimum bounded repair:** Drop the `DC-D-006` citation for this signal and mark it `Provenance: CRAFT`/kernel-derived, or narrow the signal to only the ownership-acceptance half `DC-D-006` actually supports.
**New research required:** No.

### GATE-13 — MEDIUM — `event_frequency_floor` not actually elicited
**Artifact:** `library/packs/pp/pack.yaml:73` (`event_frequency_floor # DC-D-051`) vs `question-bank.md:66-67` (Q-OPS-02, the only question the grep-convention leads to).
**Canonical evidence:** `DC-D-051` (VOLATILE VALUE) — Discovery evidence: "shortest interval between real events; detection latency...".
**Defect:** `Q-OPS-02` asks about the trigger mechanism, not an interval/frequency figure. Confirmed by 3/3 independent skeptics.
**Why it matters downstream:** `DC-D-051`'s states (HOURLY OR SLOWER/MINUTES/SUB-MINUTE/CONTINUOUS STREAM) drive a documented Options-phase mechanism choice with an exit class at CONTINUOUS STREAM; if the cited question never produces the figure, that evidence can be silently missing.
**Minimum bounded repair:** Move the `DC-D-051` citation onto `Q-OPS-06` (closest functional fit) with an added interval sub-clause, or add a dedicated Probe.
**New research required:** No.

### GATE-14 — MEDIUM — `frontline_versus_reported_reality` cites an unrelated anti-pattern
**Artifact:** `library/packs/pp/question-bank.md` Q-USR-05/Q-USR-08; `pack.yaml` user `extra_signals` (`# DC-D-005, AP-D-001`).
**Canonical evidence:** `AP-D-001` (anti-patterns.md:447-478) — entirely about premature vendor/technology naming.
**Defect:** `AP-D-001` never discusses performer-vs-manager perspective divergence. `DC-D-005` gives genuine partial support; `AP-D-001` does not. Confirmed by 3/3 independent skeptics reading the full entry.
**Why it matters downstream:** Breaks the traceability convention's own stated purpose (grep an id, find its evidentiary basis); a maintainer auditing "why ask the performer, not the manager" finds an unrelated technology-selection anti-pattern.
**Minimum bounded repair:** Cite only `DC-D-005`; note in the pack's authoring notes that no canonical anti-pattern currently covers frontline-vs-reported-reality, rather than attaching `AP-D-001`.
**New research required:** No.

### GATE-15 — MEDIUM — `Q-DAT-08` collapses per-stream evidence into per-system-pair
**Artifact:** `library/packs/pp/question-bank.md:140-141` (Q-DAT-08).
**Canonical evidence:** `AP-D-028` ("one integration decision per system pair instead of per stream"); the pack's own A5 glossary: "Exchange stream ... the unit of analysis — one decision per stream, not per system pair."
**Defect:** Q-DAT-08's grammar ("Which other systems... For each: ...") binds "for each" to *systems*, not *streams* — collecting one composite answer per system pair, exactly the shape `AP-D-028` names as an anti-pattern and the opposite of the pack's own glossary definition. Confirmed by 3/3 independent skeptics who checked the pack's own parallel idiom (`Q-DAT-01`'s identical "List X. For each:" construction, correctly bound to the enumerated noun).
**Why it matters downstream:** `DC-D-035, DC-D-036, DC-D-047` (stream count, ownership, consumer count) are per-stream decision criteria driving the Options-phase integration topology choice; if Discovery's own evidence collapses streams into systems, Options inherits an undercount with no downstream re-decomposition step.
**Minimum bounded repair:** Rephrase to bind "for each" to *exchange stream* explicitly, e.g. "List each exchange stream (not just each system) this work depends on. For each stream: who starts it, what triggers it, what moves, who owns it today?"
**New research required:** No.

### GATE-16 — MEDIUM — `Q-DAT-02` misses DC-D-022's decisive relational sub-dimensions
**Artifact:** `library/packs/pp/question-bank.md:122-123` (Q-DAT-02, the sole Core operationalization of `DC-D-022`).
**Canonical evidence:** `DC-D-022` Discovery evidence: "how many related entities appear on one screen; whether cascade delete or restrict-delete semantics are required; whether traversal depth exceeds two levels."
**Defect:** Q-DAT-02 asks only about relationship existence and cross-change consistency — none of the three named decisive sub-dimensions. No Data probe covers them either. Confirmed by 3/3 independent skeptics reading `DC-D-022`'s full Discovery-evidence field directly.
**Why it matters downstream:** `DC-D-022`'s Decision impact ties deep relational structures to a store/surface change; `AP-D-050`/`AP-D-008` name this exact gap as a documented failure mode producing silently wrong answers, not slow ones.
**Minimum bounded repair:** Extend `Q-DAT-02` or add a Data probe asking traversal depth, entities-per-screen count, and cascade-vs-restrict-delete expectation, citing `DC-D-022`.
**New research required:** No.

### GATE-17 — MEDIUM — self-report's own coverage-matrix arithmetic is wrong
**Artifact:** `docs/pp-pack-authoring/research/pp/authoring/step-2-discovery-layer-report.md` §6 (line 105) and §8 (line 138).
**Canonical evidence:** independent extraction of every `DC-D-NNN` exact string in `glossary.md`+`question-bank.md` against the full 116-id canonical namespace.
**Defect:** The report claims "113 cited by exact string; the remaining 3 (`DC-D-039, 082, 093`) are cited via... section's explicit id-range header." Independent re-extraction (confirmed by 3/3 skeptics, two of whom reproduced the count from scratch) finds **7** range-only ids, not 3: `DC-D-039, 046, 071, 082, 085, 086, 089` (a third skeptic's slightly different regex found 9, including boundary ids `047`/`083`, but all three independently agree the true count materially exceeds 3). The 4 undisclosed ones are exactly where GATE-06/07/08/10/11 live.
**Why it matters downstream:** This self-certified count is the artefact the pipeline is meant to trust for merge decisions, and the report's own §11 recommends automating this exact check going forward — an inaccurate manual count, if scripted as-is, silently propagates an undercount of real gaps into every future re-run.
**Minimum bounded repair:** Re-run the id-extraction with full range-expansion (not substring containment) against both files; correct the coverage table to list all range-only ids; re-examine each (not just 3 of them) for whether the enclosing section actually produces its Discovery-evidence content.
**New research required:** No.

### GATE-18 — MEDIUM — N-06's own Step-0-absolutes rule contradicted by its Core/Probe classification
**Artifact:** `pp-pack-authoring-map.md` §6.3 rule N-06 vs `question-bank.md:249-251` (P-OPS-03) and `:321-323` (P-DAT-02).
**Canonical evidence:** N-06 groups six ids together as ids that "can terminate the platform question" and warns deferring them "wastes the engagement" because "Steps 0-1 are cheap."
**Defect:** Four of the six (`DC-D-108, DC-D-033, DC-D-059, DC-D-062`) are correctly Core; the other two (`DC-D-028` atomicity, `DC-D-057` compute-intensity) are demoted to trigger-gated Probes — contradicting N-06's own stated rationale for exactly these six ids, and the bank's own Structure section (Core = "almost every engagement," Probe = trigger-gated). Confirmed by 2/3 skeptics reading N-06's text directly (1/3 argued N-06 only requires the six be *somewhere* in Discovery, not necessarily Core, and that reading is plausible — but the majority held that N-06's own "wastes the engagement"/"cheap" language specifically argues for unconditional asking).
**Why it matters downstream:** If nobody spontaneously volunteers a cross-system atomicity requirement or a heavy compute step, the round never surfaces `DC-D-028`/`DC-D-057` — the exact failure N-06 exists to prevent for these ids, while the other four Step-0 absolutes are protected by being Core.
**Minimum bounded repair:** Promote `DC-D-028` and `DC-D-057` to Core questions, or explicitly amend N-06 to state these two are probe-gated by design with a stated justification for why that is safe.
**New research required:** No.

## 15. Non-blocking improvements

Considered, but refuted on adversarial verification (majority of skeptics found the finding did not hold up as gate-blocking after independent re-reading — not asserted as false, only as non-material or explainable within the bounded-gate philosophy):

- `BUS-01` — `Q-BUS-08`'s loose `AP-D-036` citation (3/3 refuted; the question remains grounded by its other two citations).
- `GRD-GOV-03` — `P-GOV-14`'s 4-in-1 bundling (2/3 refuted; the bundled ids were judged thematically coherent enough as one ALM-precondition question).
- `QB-ECON-01`, `QB-ECON-02` — cross-lens frequency/cost duplication (2/3 refuted each time; the questions were judged distinct enough in framing/granularity).
- `QB-ECON-03` — Q-BUS-03's "product category" clause (3/3 refuted; it is a verbatim, deliberate lift of `DC-D-002`'s own field, not an invented ask).
- `QB-ECON-04` — same P-GOV-14 bundling as `GRD-GOV-03` (2/3 refuted).

Not independently adversarially verified (self-flagged LOW or non-gate-blocking MEDIUM by the originating agent; reviewed for plausibility, judgment not independently re-tested):

- `BUS-02` — `Q-BUS-05`'s `AP-D-014` parenthetical attributed to the wrong id (should be `DC-D-006`'s own vocabulary).
- `BUS-04` / `OPS-06` — stale/vendor-tagged SKILL.md signal catalogs in `lens-business` and `lens-operations` (see GATE-03; same systemic pattern, lower individually-observed severity).
- `BUS-05` — `process_maturity_and_variants` has no dedicated Business anchor (elicited only via Operations/User).
- `OPS-04` — `Q-OPS-07`'s `DC-D-006` add-on citation is unsupported (DC-D-005 alone suffices).
- `OPS-05` — `Q-OPS-04` bundles elapsed-duration and human-wait into one question.
- `USR-02` — "frontline" used with two unrelated canonical meanings in the same lens (naming collision, no functional harm).
- `USR-03` — `Q-USR-05`/`Q-USR-08` near-duplicate on performer-vs-manager perspective.
- `USR-04` — end-user adoption/training is entirely uncovered (canonical corpus itself is nearly silent here — flagging is per the task's explicit checklist, not an invented requirement; **new research required if pursued**).
- `USR-05` — `Q-USR-01` bundles three distinct asks.
- `DAT-03` — `DC-D-021`'s lifecycle-split state is reachable only via a glossary aside, not an eliciting question.
- `GRD-GOV-04` — the `maker_and_delivery_model` signal name retains low-code vernacular (same as `NEUT-01`).
- `GRD-FIN-03` — Financial lens has no `P-DAT-01`-equivalent Conflicted-forcing construct.
- `GRD-FIN-04` — `P-FIN-07`'s `DC-D-096` co-citation is a loose/padding fit.
- `NEUT-01` — `maker_and_delivery_model` naming (duplicate of `GRD-GOV-04`).
- `GRD-NEUT-01` — Appendix B's outcome-3 row omits its own strongest evidence pair (`Q-DAT-03`/`P-DAT-09`); the underlying bank works correctly regardless.
- `GRD-DEC-04` — `DC-D-046` (contract volatility/cadence) not operationalized beyond ownership.
- `GRD-DEC-05` — `DC-D-086` (identity concentration) not asked.
- `GRD-DEC-06` — `Q-GOV-03`'s partial coverage of `DC-D-060` (identity-provider/PIM/conditional-access facts missing).
- `GRD-DEC-07` — `Q-GOV-07`'s partial coverage of `DC-D-077` (release cadence/window not asked).
- `GRD-XLENS-01` — the "Conflict scan" instruction exists only in `lens-governance/SKILL.md`, not the other five lens contracts (kernel-level, predates Step 2; backstopped at Framing).
- `GRD-XLENS-02` — "data freshness vs integration reality" pair lacks a dedicated supply-side signal.
- `CONS-06` — `Q-GOV-03`'s citation precision issue (same underlying fact as `GRD-DEC-06`).
- `QB-ECON-05` — Probe-tier size (up to 14/lens) exceeds `docs/PACK_AUTHORING.md`'s stated "5–8 per lens" norm, which never anticipated a Core/Probe split; substantively defensible for Governance given its decision-blocking density, but the governing doc was not updated to say so.

## 16. Required bounded repair, if any

All 18 gate-blocking findings are fixable by editing the existing authored files (plus, for GATE-03, 1–3 `SKILL.md` files outside Step 2's original file set) — no redesign, no new canonical research. Condensed action list:

1. Fix two mis-cited canonical sections/ids (`GATE-01` operations-support.md §2.4→§11; `GATE-14` drop AP-D-001).
2. Fix or add three unsupported/orphaned signal citations (`GATE-02` variant-count question + Appendix B label; `GATE-12` requester_vs_sponsor_authority; `GATE-13` event_frequency_floor anchor).
3. Reconcile 1–3 lens `SKILL.md` signal catalogs with the Step-2 `pack.yaml` rewrite, prioritizing the two literal vendor terms in `lens-governance/SKILL.md` (`GATE-03`).
4. Rewrite `Q-FIN-02` to an open horizon (`GATE-04`).
5. Add one Financial question/probe for the internal-build support/ops cost tier (`GATE-05`).
6. Add one question each for user concurrency (`GATE-06`) and capacity-proof requirement (`GATE-07`).
7. Add a Governance (or Operations) question for `DC-D-071` (`GATE-08`) — this single fix also resolves GATE-08's 5 independent reports at once.
8. Resolve 3 cross-lens signal/question mismatches — move or duplicate the eliciting question so signal and question agree on lens (`GATE-09` DC-D-061, `GATE-10` DC-D-045, `GATE-11` DC-D-024).
9. Rephrase `Q-DAT-08` to bind per-stream, not per-system (`GATE-15`); extend `Q-DAT-02` for relational sub-dimensions (`GATE-16`).
10. Re-run and correct the self-report's own coverage-matrix arithmetic (`GATE-17`).
11. Resolve N-06's own internal contradiction by promoting `DC-D-028`/`DC-D-057` to Core, or amending N-06 (`GATE-18`).

None of these require new canonical research (`new_research_required: False` on all 18). One non-blocking item (`USR-04`, end-user adoption/training) would require new research if the team chooses to pursue it, since the canonical corpus itself is silent there.

---

`STEP 2 DISCOVERY GATE: FAIL`
`CRITICAL FINDINGS: 0`
`HIGH FINDINGS: 11`
`GATE-BLOCKING MEDIUM FINDINGS: 7`
`DISCOVERY TECHNOLOGY NEUTRALITY: PASS`
`DISCOVERY OUTCOME NEUTRALITY: PASS`
`DOWNSTREAM DECISION SUFFICIENCY: FAIL`
`TRACEABILITY INTEGRITY: FAIL`
`BROKEN CANONICAL REFERENCES: 0`
`SEMANTICALLY UNSUPPORTED REFERENCES: 6`
`NEW RESEARCH REQUIRED: NO`
`READY TO FREEZE DISCOVERY LAYER: NO`
