# Step 8 — Real Engagement Pilot Report — pricing-marinha

## 1. Frozen baseline

```
STEP 7 BASELINE COMMIT: 78391d7ea00cc59c45b23ec65b384de8c812ab39
BRANCH: pp-pack-authoring/step-2-discovery-layer
PACK VERSION: 1.8.1
WORKING TREE AT PILOT START: clean (3 untracked non-pack files, unrelated to library/kernel/pack)
```
No `library/`, `.claude/skills/`, `.claude/agents/`, `.claude/agent-memory/`, or `library/kernel/` edits during the pilot. Verified at start and throughout — every P-OBS logged in `step-8-pilot-observation-log.md` records observation only, zero repair.

## 2. Engagement profile

- **Engagement**: `projects/pricing-marinha`, pack=pp
- **Requester**: Pedro O. (role/authority not recorded — real gap, never filled)
- **Literal request** (verbatim, unedited): daily Marinha bunker pricing runs on a fragile, single-owner Excel workbook; Pedro repairs it including during his own leave; needs a way to estimate Monday/Tuesday pricing with few known quotes; wants an alternative to the Excel file to streamline the process
- **Real stakeholders**: sponsor (Pedro O.), pricing committee, ~200 KAM (never directly consulted during Discovery/Framing — consultation authorized in Framing, not run before Decision)
- **Complexity**: moderate — 291 named ranges, 6-sheet calculation duplication, 2 external integrations (SAP, X-Author — the latter's name was itself corrected mid-engagement), 1 shared SQL Server dependency discovered mid-Options
- **Not a fixture**: this was not chosen or shaped to stress the pack; complexity, ambiguity, and stakeholder gaps emerged from real material (2 recordings, 2 process docs, 1 xlsx)

## 3. Evidence/source profile

5 inputs: `Fluxograma do Processo Atual de Pricing – Marinha.docx`, `Inputs, cálculos e outputs relevantes...docx`, `PREÇO BANCAS_30_01_26.xlsx`, `Pricing Marinha – Kick-off.vtt`, `Processos Pricing - Marinha...vtt`. Process-capture (`/capture`) ran once at engagement start; no stale-hash re-runs were needed.

## 4. Phase timeline

| Phase/round | Started | Key output |
|---|---|---|
| Discovery R-01 | 2026-09-04T18:00Z | 6 lenses sequential inline; 4 `/answer` batches to close all 14 Critical items |
| Framing F-01 | 2026-09-04T19:20Z | 7-persona parallel council (6 lenses, no solution-architect yet); frame.md; D-001 |
| Options O-01 | 2026-09-04T21:00Z | 7-persona parallel (adds solution-architect); options.md; 6 options; post-round `/answer` for X-002/U-017 |
| Premortem | 2026-09-04T22:30Z, re-run 23:00Z | 5 causes of death on O-004; re-run after unsolicited scope clarification |
| Decision D-01 | 2026-09-04T23:15Z | D-002 (adopt O-004); auto-`/synthesize` |
| Blueprint | 2026-09-04T23:40Z → 2026-09-05T02:15Z | v01→v05 across 4 iterations + 1 gap-closing revision; D-003 (v04 approved), D-004 (v05 approved) |
| Render | 2026-09-05T02:00Z (5 gaps) → 02:30Z (0 gaps) | 6/6 deliverables, v01 each |

Elapsed real time from `/start` to a clean 6-deliverable render: ~9h45m (16:47Z day 1 capture → 02:30Z day 2 final render), across Discovery/Framing/Options/Decision/Blueprint/Render in one continuous session with the sponsor answering in batches.

## 5. Discovery observations

- 6 lenses ran inline, sequential, correct fixed order.
- Financial lens correctly refused to invent as-is cost/budget absent evidence (§9, §15) — left Unknown until sponsor closed it.
- Governance vs Operations: SoD conflict (X-001) correctly surfaced, not auto-reconciled; resolved by sponsor, but the underlying continuity risk (R-001) was explicitly kept open as a separate row rather than folded into the SoD answer.
- One answer (U-010→A-006) correctly held at Assumed rather than promoted to Confirmed, because the sponsor's answer was an impression ("provavelmente boa"), not a verification.

## 6. Question metrics

Best available count across the full engagement (Discovery + all subsequent phases), from `council-log.md`:

```
Discovery R-01 (4 batches): 14 items (13 Unknown + 1 Conflicted, all Critical)
Framing F-01 (1 batch):     12 items (11 resolved, 1 — U-007 — refused a transition, stayed Unknown)
Options O-01 (1 batch):      2 items (X-002, U-017)
Pre-render gap closure:       3 items (solution_name, A8, A9)
U-025 (blueprint):            2 attempts, both refused a transition — correctly held Unknown twice
────────────────────────────────────────────
TOTAL QUESTIONS ASKED:       33
QUESTIONS REFUSED A CLOSING ANSWER (correctly): 3 (U-007 once, U-025 twice)
QUESTIONS LATER JUDGED UNNECESSARY: 0 observed
DUPLICATE QUESTIONS: 0 (U-025's 2 asks were a deliberate re-attempt at a different moment, not a redundant repeat)
QUESTIONS ANSWERABLE FROM EXISTING EVIDENCE: 0 identified
```

No question in this engagement was flagged, on review, as avoidable — every one either changed a decision, closed a real evidence gap, or (correctly) failed to close and stayed Unknown.

## 7. Shared Understanding epistemic quality

Final SU state (spot-checked, not independently re-audited row-by-row beyond this pilot's live observations):

- **Confirmed**: 67 · **Assumed**: 10 · **Risky**: rows spanning R-001..R-012 · **Conflicted**: 6 total raised (X-001..X-006), 4 resolved (X-001, X-002, X-004, and X-005 addressed at design-assumption level in blueprint) — **X-003 and X-006 remain open** at engagement's stopping point.
- **Unknown**: 31 rows in the table (includes resolved-and-superseded history); confirmed still-open at report time: **U-007** (Med — pricing-team throughput concentration, never closed, "não sei"), **U-025** (Critical — prior veto reason, asked twice, never closed), **U-028** (Critical — reference-app capacity, not closed before Decision — O-003 was never definitively ruled out or in), **U-030** (Med — business criticality classification, never asked).
- No incorrect state assignment observed in any row this pilot inspected directly (spot-checked ~15 rows across phases via the P-OBS entries above).
- No unnecessary row fragmentation observed; no row judged too vague to support later reasoning.

**Notable**: U-028 (whether the reference-app reuse option, O-003, is viable) was never closed. The sponsor picked O-004 (build from scratch) without formally ruling O-003 in or out — this is a **live gap in the decision's comparator basis** (`options.md`'s own "COMPARATOR EVIDENCE ABSENT" flag never got resolved before `/decide`). This is not a pack defect — the pack correctly flagged the gap in `options.md` — but it is a real engagement-quality finding: the decision proceeded past an explicitly-flagged comparator gap. Worth a P-OBS-style note even though it was not caught live during this pilot's real-time instrumentation; recorded here for completeness in this report per §35's non-optimization rule (no fix attempted; documentation only).

## 8. Options / context footprint

Not separately instrumented at the token/section level during this pilot (§11 mandates observing footprint, not measuring it precisely without invasive tooling this pilot didn't build). Qualitative observation: the Options round produced deep, non-mechanical reasoning (option-class generation, disqualifiers, `COMPARATOR EVIDENCE ABSENT` used honestly twice, O-004/O-005 correctly treated as non-comparators, O-006 correctly treated as a "finding" not a candidate) without any sign of the spine being either under- or over-loaded. No repeated-section reads or unused-context waste was observed in the artefacts produced. This pilot cannot report a footprint number — only an absence of visible friction.

## 9. Decision depth (D0–D3)

Not formally tagged with D0/D1/D2/D3 labels in this engagement's artefacts (the pack's escalation-depth mechanism was not directly observable as discrete tags in the outputs reviewed). Qualitatively: solution-architect's 2 domain-knowledge pulls (dataverse.md §8-9, patterns.md §5) were both material and directly cited in the strongest option's (O-004) preconditions/strengths — consistent with proportionate, not excessive, depth. No sign of over-analysis (no unused pulls) or under-analysis (the decision's justification directly engages every material concern raised by the 7 personas).

## 10. Domain Knowledge pulls

```
OPTIONS DK PULLS: 2 (both used, both cited with section — dataverse.md §8-9, architecture/patterns.md §5)
ARCHITECTURE DK PULLS: not separately itemized in blueprint-log.md beyond architecture-core.md anchor citations (used as template/contract reference, not a "pull" event distinct from the Options-round pulls)
DELIVERABLE DK PULLS: none observed
UNNECESSARY KNOWLEDGE PULLS: 0 observed
```

Consistent with, not enforcing, the Step 4C median≈1/max2 observation — this pilot's data point: 2 pulls total across the whole engagement, both material.

## 11. Missing-knowledge behaviour

No instance of the runtime guessing, using model knowledge, or inventing a platform capability/entitlement/limit was observed. Every missing-knowledge moment (financial exposure, retention floor, legal confirmation, DK gaps) resulted in a preserved Unknown, a Confirmed fact sourced to a real answer, or an explicit Assumed with a stated reason — never a silent fill.

## 12. Volatility behaviour

`half_lives_override: {}` was never populated and never needed — no material volatile platform fact was encountered that required deviation from default validity behaviour in this engagement. No re-verification trigger fired (engagement ran start-to-finish in under 24h, well inside any plausible half-life).

## 13. Decision quality

- Justification is defensible: O-004 closes every clause of the frame, explicitly cross-referenced to D-001's anchors.
- What was NOT evaluated is visible: 5 Critical Unknowns (U-025..029) surfaced explicitly as preconditions/proof obligations in D-002, not hidden.
- Conditions/preconditions are explicit and owned where known (Pedro O./governance for data ownership; "not named" honestly stated where no owner exists yet).
- A human reviewer can distinguish "O-003 excluded" from "O-003 proven fit" — it is neither: U-028 never closed, and the decision record does not claim O-003 was ruled out, only that O-004 was chosen. This is honest but leaves a live gap (see §7 above).

## 14. Architecture quality

Blueprint structured the frozen decision rather than re-deciding it across all 5 versions:

- v01: initial structure, 4 structural blockers, all traced to real Unknowns, none defaulted.
- v02: a genuinely new fact (shared SQL Server) changed 3 domains' record authority and correctly opened a *new* tension (A-009) instead of silently keeping the old surface choice.
- v03: caught a real terminology/identity error (X-ALT → X-Author) mid-architecture, flagged (not asserted or dismissed) a suspected link to a previously-vetoed integration.
- v04: legitimately dissolved the last structural blocker via a genuine scope-boundary relocation (owner = other initiative), with the underlying Unknown (U-025) explicitly kept open in the SU rather than closed by the relocation.
- v05: closed 3 real render-identified gaps (name, A8, A9) additively, without touching any already-approved content; explicitly refused to force-close `replacement_of_existing_artefact` just to make the earlier dry-run gap disappear.

No re-decision of D-002 occurred at any point in the blueprint layer.

## 15. Deliverable consumer feedback

**Not collected this pilot.** No real consumer (sponsor, architect, implementer, delivery lead) reviewed the 6 rendered deliverables as part of this run — the engagement was stopped, by the user's choice, immediately after achieving a gap-free render. §21-25 (deliverable consumer test, Executive Report test, implementation handoff test) are **not exercised** in this pilot. This is a material completeness gap in this specific pilot run, not a pack defect — recorded honestly rather than fabricating consumer feedback.

## 16. Estimate comparison

Estimate rendered via Mode A (from the just-produced Implementation Specification): 44–51 person-days, medium confidence (per render-log.md). No independent developer/lead estimate was collected for comparison — not available in this pilot run.

## 17. Human intervention log

```
H1 — expected judgement:      ~20 events (14 Discovery + 12 Framing[11 closed] + 2 Options + decision itself + 2 blueprint-approval events D-003/D-004 + 3 pre-render gap closures) — sponsor accepted/decided at every gate
H2 — engagement clarification: 2 unsolicited (scope clarification re: KAM/app interface → C-056; scope clarification re: X-Author handled elsewhere → C-065) — both correctly triggered re-runs (premortem, blueprint v04) rather than being absorbed silently
H3 — usability friction:      0 observed
H4 — framework repair:        0 observed
```

## 18. Rework / iteration

```
Premortem re-run: 1 — new evidence (C-056), correctly reclassified cause-of-death #3, not deleted
Blueprint v01→v05: 5 versions, each with a distinct, evidenced trigger (new fact, terminology correction, scope relocation, gap closure) — none cosmetic, none a repeat of the same unresolved issue
Render re-run: 1 — human decision (v05 approval, D-004), 0 gaps reopened
RUNTIME-DEFECT REWORK: 0
```

## 19. Context ceremony

No instance of mechanically-populated boilerplate, duplicated state summaries, or unused-but-loaded context was observed in the artefacts reviewed. `options.md`'s concern-coverage section explicitly marks several dimensions "não avaliado" / "não material" rather than forcing verdicts on all 12 — read as necessary defensibility, not ceremony. No systemic context ceremony detected in this pilot.

## 20. P-OBS register

29 observations logged in `step-8-pilot-observation-log.md` (P-OBS-001 through P-OBS-029). **This report was originally compiled at P-OBS-026 with a PASS verdict; a human reviewer (post-compilation) identified 3 structural problems the live instrumentation missed, added as P-OBS-027/028/029.** Corrected totals below.

## 21. Defect classification / severity

```
S0 (observation, no consequence): 4
S1 (nuisance, safe workaround):   1  — solution_name missing across all 6 deliverables (P-OBS-019)
S2 (material usability defect):   0
S3 (semantic/decision risk):      2  — NEW, reviewer-identified:
    · P-OBS-027 — Discovery/Options/Architecture reasoning did not demonstrably re-engage the captured process model (`_capture/process-model.md`) at the depth this highly customized process required; SU-level summary facts substituted for the real calculation chain
    · P-OBS-028 — experience-surface choice (Record-centric/model-driven) was never reconsidered against the process's own customization signal (6-sheet duplication, per-counterparty heuristics), even though that signal was present in the SU from Discovery onward
S4 (integrity failure):           1  — NEW, reviewer-identified:
    · P-OBS-029 — A-009 (the correct question: does a model-driven surface fit an externally-authoritative SQL Server data store?) was closed via C-062, an unverified technical claim ("conectividade nativa já configurada, confirma Record-centric app"). C-062 asserted that existing/native connectivity was sufficient to confirm the record-centric/model-driven surface. That conclusion was not supported by an identified connectivity mechanism or by evidence that the mechanism satisfies the engagement's material data, security, audit, query and operability requirements. *(Step 8B correction: the earlier wording "model-driven apps do not natively run against an external SQL Server as primary record authority" is withdrawn as a factual assertion — external SQL authority is not an automatic model-driven disqualifier; see `step-8b-post-pilot-adjudication-report.md` §7.)* This claim was accepted as Confirmed and became load-bearing for the entire downstream architecture, blueprint, implementation-spec, and 44-51 person-day estimate. **The pilot's own live instrumentation (P-OBS-014) logged this same event as a positive example and failed to independently verify the technical claim — a review-quality failure, not only an engagement one.**
```

**This is no longer a defect-free pilot.** One S4 integrity failure means the recommended architecture, as currently specified, rests on an unverified load-bearing technical premise and should not proceed to build until Step 8B adjudicates the data-access mechanism and its fit against the engagement's material requirements.

## 22. Recurring vs engagement-specific

29 observations total — each a **single data point** — this is the first real-engagement pilot, so nothing here can yet be classified as "recurring" per §32. Two items are flagged as worth watching across future pilots without recommending action now:
- Whether `solution_name` is commonly missing at render time across engagements (would suggest an earlier prompt point, e.g. at `/start` or `/decide`).
- Whether A8 (environment/release) and A9 (irreversible choices) are commonly absent from a first-pass blueprint (would suggest they deserve more prominence in the blueprint authoring flow, not necessarily a new gate).
Neither is recommended as a repair from this single pilot.

## 23. Overall verdict — REVISED after reviewer correction

The frozen pack (1.8.1) held approval-gate and epistemic discipline well on *procedural* dimensions: no fabricated fact was accepted as such by the mechanism's own checks, gates were not bypassed, and the render/synthesis layers correctly refused to reach for unapproved-but-convenient content twice. **However**, a human reviewer identified that this procedural discipline was not enough: an unverified, load-bearing *technical* claim (C-062) was accepted as Confirmed by the answer/blueprint process and never checked against an identified connectivity mechanism or that mechanism's fit with the engagement's material requirements, and it became load-bearing for the whole architecture. Separately, the engagement's reasoning did not visibly re-engage the captured process detail (§P-OBS-027) at the depth a highly customized calculation process demanded, and the experience-surface choice was never reconsidered against the process's own customization signal (§P-OBS-028) even though that signal was present from Discovery onward.

The one open item flagged in the original compilation (U-028, O-003 vs O-004 comparator gap) still stands and is now compounded by these findings: the decision and architecture, as currently rendered, are **not fully defensible as specified** — they should be revisited before any build proceeds.

## 24. Recommended post-pilot actions

- **BOUNDED RUNTIME REPAIR (candidate, for post-pilot review — not actioned in this pilot)**: technical claims about platform/connector capability that a persona or blueprint asserts (e.g. "native connectivity confirms surface X fits data store Y") should require either a citable, checkable source (a domain-knowledge pull with a real section reference) or must remain Unknown — never Confirmed on the strength of the persona's own assertion. This is the single most important candidate to come out of this pilot.
- **ENGAGEMENT PRACTICE CHANGE**: re-engage `_capture/process-model.md` directly (not just its SU-level summary) during Options and Architecture reasoning for any engagement with a highly customized as-is process; treat process-customization level as an explicit, revisited input to the experience-surface choice, not a one-time decision at v01.
- **RESEARCH COMMISSION**: verify, with real platform documentation, what connectivity model-driven (Dataverse) apps and Canvas apps genuinely support against an external SQL Server system of record, and reconsider `pricing-marinha`'s experience-surface choice on that basis before any build proceeds.
- **MEASUREMENT / MORE PILOTS**: still valid — watch whether `solution_name`/A8/A9 gaps recur; also now watch, across future pilots, whether unverified technical claims from personas get accepted as Confirmed elsewhere.
- A second real pilot, run to completion including §21-25 deliverable-consumer testing (not exercised here) and with the technical-claim-verification gap specifically watched for, is recommended.
- **This specific engagement's blueprint/implementation-spec/estimate should not be treated as final** until the experience-surface choice is re-examined with real technical verification.

---

## Final evaluation questions (§38)

1. **Did the framework improve reasoning quality?** Yes — options.md and the blueprint iterations show reasoning that engages real trade-offs (comparator-absent flags, non-comparator scoping) rather than mechanical form-filling.
2. **Did it preserve uncertainty honestly?** Yes — U-007/U-025 held Unknown under repeated pressure; A-006/A-008 held at Assumed rather than promoted; `replacement_of_existing_artefact` left open rather than force-closed.
3. **Did it avoid inventing technical knowledge?** No. C-062 was accepted as Confirmed without sufficient technical verification and became architecture-significant. Whether its underlying mechanism is ultimately viable is subject to Step 8B technical adjudication.
4. **Did it ask the right stakeholder questions?** Largely yes — 33 questions, all judged necessary on review; but KAM (the actual daily consumers) were authorized for consultation in Framing (C-045) and never actually consulted before Decision — a real engagement-practice gap, not a pack defect.
5. **Did it avoid unnecessary questions?** Yes — 0 identified as unnecessary or duplicate.
6. **Was context loading selective?** Qualitatively yes; not independently measured at the token level this pilot.
7. **Did Domain Knowledge pull behave naturally?** Yes — 2 pulls total, both material, both cited.
8. **Did Options feel like reasoning or form-filling?** Reasoning — comparator-absent flags used honestly, non-comparator scoping correctly identified.
9. **Did Architecture structure rather than re-decide?** Yes across all 5 blueprint versions — no re-decision of D-002 observed.
10. **Were deliverables genuinely useful to their consumers?** **Not tested** — no real consumer reviewed them in this pilot run (§15).
11. **Did any layer create a second truth?** No — render correctly preferred the approved architecture record over a more-complete-but-unapproved version, twice (synthesis and render).
12. **Was framework ceremony proportionate?** Yes, qualitatively — no ceremony flagged in artefacts reviewed.
13. **What failed because this was real rather than synthetic?** A genuine terminology error (X-ALT/X-Author) surfaced only because real evidence was messy; a genuine comparator gap (U-028) was flagged but not resolved because real engagement pressure (time, stopping point) intervened — exactly the kind of finding a synthetic fixture would not produce.
14. **Which observations are generic enough to justify post-pilot repair?** P-OBS-029 identifies a potentially generic runtime-control defect — architecture-significant platform claims may be settled without cited technical authority. Genericity and repair scope are being adjudicated in Step 8B. P-OBS-027/028 remain separate candidates.
15. **Should pack 1.8.1 proceed to another pilot unchanged?** No — not until Step 8B determines whether P-OBS-029 requires a bounded runtime repair.

---

## FINAL OUTPUT — REVISED after human reviewer correction (2026-09-05)

> The pilot was first compiled as PASS at P-OBS-026. A human reviewer then identified 3 structural problems the live instrumentation missed (P-OBS-027/028/029), including one S4 integrity failure (an unverified technical claim accepted as Confirmed and used to justify the chosen architecture). This is the corrected, final output.
>
> **Step 8B consistency corrections applied 2026-09-05** (documentation only — observation count 26→29; Final Evaluation Q3/Q14/Q15; P-OBS-029 technical wording; unsupported-fact wording). The historical pilot verdict (FAIL) is unchanged. Adjudication: `step-8b-post-pilot-adjudication-report.md`.

```
STEP 8 — REAL ENGAGEMENT PILOT: FAIL
BASELINE COMMIT: 78391d7ea00cc59c45b23ec65b384de8c812ab39
PACK VERSION: 1.8.1
ENGAGEMENT REACHED LEGITIMATE STOPPING POINT: YES (clean 6/6 deliverable render reached; but the underlying architecture is now known to rest on an incorrect technical premise — §21-25 consumer test also not exercised)
CRITICAL UNKNOWNS IDENTIFIED: 18 (13 Discovery + 5 Options-round; 3 remain open at stopping point: U-025, U-028, plus Med-severity U-007/U-030 non-critical)
UNSUPPORTED FACTS INVENTED: 1 (C-062 — "conectividade nativa já configurada, confirma Record-centric app" — accepted as Confirmed without technical verification: no connectivity mechanism identified, no evidence that the mechanism satisfies the engagement's material data, security, audit, query and operability requirements; mechanism viability adjudicated in Step 8B)
EPISTEMIC PROMOTIONS: 1 (C-062, incorrectly promoted to Confirmed) — separately, 2 correct non-promotions were also observed elsewhere (A-006, A-008)
SEMANTIC AUTHORITY BYPASSES: 0
SCOPE LEAKAGE EVENTS: 0
QUESTIONS ASKED: 33
UNNECESSARY QUESTIONS: 0
DUPLICATE QUESTIONS: 0
DOMAIN KNOWLEDGE PULLS: 2
UNNECESSARY DOMAIN KNOWLEDGE PULLS: 0
H3 USABILITY-FRICTION INTERVENTIONS: 0
H4 FRAMEWORK-REPAIR INTERVENTIONS: 1 (this reviewer correction itself — a human had to catch what the runtime and the pilot's own live instrumentation both missed)
RUNTIME-DEFECT RE-RUNS: 0
S0 OBSERVATIONS: 4
S1 OBSERVATIONS: 1
S2 OBSERVATIONS: 0
S3 OBSERVATIONS: 2 (P-OBS-027 process-model under-engagement; P-OBS-028 surface choice never reconsidered against customization signal)
S4 OBSERVATIONS: 1 (P-OBS-029 — unverified technical claim promoted to Confirmed, load-bearing for the entire architecture)
SYSTEMIC CONTEXT CEREMONY DETECTED: NO
DELIVERABLE CONSUMER USEFULNESS: NOT TESTED (no real consumer reviewed deliverables this run)
DECISION REMAINS DEFENSIBLE: NO — the chosen architecture (model-driven surface over an externally-authoritative SQL Server) rests on an unverified load-bearing technical claim (C-062); the data-access mechanism and experience-surface choice must be re-examined (Step 8B) before this blueprint/implementation-spec/estimate is treated as final
PACK MODIFIED DURING PILOT: NO
NEW RESEARCH PERFORMED DURING PILOT: NO
PACK 1.8.1 READY FOR ANOTHER PILOT UNCHANGED: NO — recommend the bounded-runtime-repair candidate in §24 (require citable verification for platform/connector technical claims) be reviewed before the next pilot, though the pilot process itself (evidence-first, no live optimization) worked as intended in surfacing this once a human reviewer looked
POST-PILOT REVIEW REQUIRED: YES
```
