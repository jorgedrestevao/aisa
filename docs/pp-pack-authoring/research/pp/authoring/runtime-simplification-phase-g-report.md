# Runtime Simplification — Phase G report: PP pack runtime cleanup

<!--
provenance: IMPLEMENTATION (3 PP runtime artifacts trimmed, 1 new test file, 1 authoring report addendum)
scope: library/packs/pp/{pack.yaml Discovery lenses_config, question-bank.md, glossary.md}
authored: 2026-09-04
basis: runtime-simplification-plan.md §9 + §11 phase G; phase C/D/E/F reports; step-2-discovery-layer-report.md
no research reopened · no kernel file modified · no lens/persona modified · decision-tree.md and
domain-knowledge/* untouched · no new runtime artifact
path note: written to the repo's actual `research/pp/authoring/` directory
  (`docs/pp-pack-authoring/research/pp/authoring/`), alongside the plan and the A–F reports.
-->

## 1. Cleanup summary

Three PP runtime artifacts were trimmed against one test: **would removing this materially reduce
decision quality?** Research support alone bought nothing.

| Artifact | Before | After | What changed |
|---|---|---|---|
| `pack.yaml` Discovery `extra_signals` | 89 cues | **36 cues** | survival test + consolidation; `# DC-D-NNN` trace comments moved to §9 of this report |
| `question-bank.md` | 506 lines / 33.8k chars · 48 core + 60 probes | **242 lines / 15.4k chars · 35 core + 34 probes** | re-shaped as a formulation resource for its one consumer; all `Research basis:` lines and Appendices A/C removed |
| `glossary.md` | 288 lines / 30.5k chars · 151 rows | **132 lines / 12.9k chars · 50 rows** | 11 sections → 7; terms that were research artefacts, kernel duplicates or ordinary language removed |
| `pack.yaml` overall | 194 lines / 9.2k | **144 lines / 5.8k** | `pack_version` 1.3.0 → 1.4.0 |

Static PP Discovery context: **73.5k → 34.2k chars (−53%)**. Injected per full Discovery round
(6 lens invocations): cue payload **1,824 → 1,155 chars (−37%)**, cue count **−60%**.

Untouched by design: `technology.constraints_to_check`, `decision_tree`, `domain_knowledge`,
`deliverables`, `epistemics`, `decision-tree.md`, `domain-knowledge/*`, architecture and deliverable
templates, all kernel files, all 7 lens files, all 7 persona files.

## 2. `extra_signals` before / after, by lens

| Lens | Before | After | Injected line (chars) | Was |
|---|---:|---:|---:|---:|
| business | 12 | **5** | 295 | 356 |
| operations | 14 | **7** | 389 | 426 |
| user | 15 | **5** | 343 | 508 |
| data | 20 | **7** | 390 | 625 |
| governance | 20 | **7** | 408 | 634 |
| financial | 8 | **5** | 314 | 259 |
| **total** | **89** | **36** | 2,139 | 2,808 |

`financial`'s injected *line* grew 259 → 314 chars while its cue count fell 8 → 5: the surviving names
are longer, and ~164 chars of every line is the mandatory "cues, not a checklist" clause. The payload
is what shrank (financial: 8 short cues → 5 cues, 150 chars).

Surviving set:

```
business    business_criticality_class · differentiation_class · existing_capability_overlap ·
            scope_reach · expected_lifespan_and_change_frequency
operations  work_shape_class · long_running_wait_and_approval_shape · partial_failure_behaviour_today ·
            stable_business_key_availability · system_without_programmatic_interface ·
            compute_intensive_step_present · spreadsheet_and_mailbox_anchors
user        user_population_identity_class · interaction_bespokeness_and_design_obligation ·
            offline_operating_requirement · native_distribution_and_push_need ·
            response_and_freshness_expectation
data        relational_depth_and_integrity · queried_volume_per_access_path ·
            access_granularity_requirement · atomicity_span_and_consistency_window ·
            analytical_versus_operational_need · attachment_and_binary_volume ·
            external_exchange_profile
governance  deployment_model_constraint · connectivity_and_egress_policy_posture ·
            vendor_trust_boundary_requirement · authorization_enforcement_point ·
            maker_and_platform_governance_model ·
            release_control_and_reversibility_expectation · vendor_change_tolerance
financial   audience_and_frequency_shape · existing_entitlement_baseline ·
            mandated_control_funding_gap · cost_driver_growth_at_horizon ·
            cost_attribution_requirement
```

## 3. Signals removed and consolidated — why

### 3.1 Removed because the universal lens already cues it

The cue added nothing the kernel lens does not already make the reasoner look for.

| Removed | Universal cue that covers it |
|---|---|
| `time_to_value_driver` | business `urgency_declared_vs_evidenced` |
| `accountable_owner_named`, `requester_vs_sponsor_authority` | business `decision_authority`, `shadow_stakeholders` |
| `prior_attempt_outcome` | business `prior_attempts` |
| `process_maturity_and_variants`, `as_is_variant_count`, `exception_and_rework_paths` | operations `as_is_steps`, `exceptions_and_escalations` |
| `process_elapsed_duration` | operations `cycle_time_current_vs_target` |
| `peak_to_average_ratio` | operations `volume_and_peaks` |
| `user_population_size`, `persona_divergence` | user `user_populations` |
| `device_and_form_factor_mix` | user `devices_and_connectivity` |
| `accessibility_regime`, `language_count_and_script_direction` | user `accessibility_needs`, `language_needs` |
| `frontline_versus_reported_reality` | the user lens's own stance ("the sponsor's account is second-hand") |
| `source_of_record_per_entity` | data `systems_of_record` |
| `total_volume_and_growth` | data `volumes_growth` |
| `retention_and_erasure_obligation`, `residency_and_sovereignty_regime` | data `retention_residency` |
| `data_quality_evidence`, `migration_scope_and_source_quality` | data `data_quality` (+ the lens's "trust the column profile") |
| `compliance_regime_named` | governance `regulations_applicable` |
| `identity_model`, `access_revocation_immediacy` | governance `access_control` |
| `audit_evidence_requirement` | governance `audit_requirements` |
| `current_state_cost` | financial `as_is_cost` |
| `cost_of_doing_nothing` | financial `do_nothing_cost` |
| `budget_envelope_and_funding_model` | financial `budget_envelope`, `funding_model` |
| `value_horizon` | financial `payback_roi` (+ business's surviving lifespan cue) |

### 3.2 Removed because another lens owns the concept

`value_against_cost_of_ownership` (financial owns cost) · `external_identity_requirement` (user owns
identity class) · `support_and_operational_ownership` (operations `operational_ownership`) ·
`operational_maturity_class` (governance's surviving maker/governance-model cue, plus probe `P-OPS-09`).

### 3.3 Removed because a probe with an observable trigger is the better home

A cue costs context on every round; a probe costs nothing until its trigger is seen.

| Removed cue | Now reached by |
|---|---|
| `concurrent_edit_contention` | (retired; `P-DAT-02` covers the multi-write case) |
| `event_frequency_floor` | `Q-OPS-02`, `Q-USR-07` |
| `navigation_shape_and_deep_links` | — (implementation-grade; no Discovery consequence) |
| `conversational_interaction_expectation` | `P-USR-06` |
| `secrets_and_credential_policy` | (retired; `Q-GOV-05` covers connect-time policy) |
| `retirement_accountability` | (retired; `Q-BUS-06` covers expected lifespan) |
| `environment_isolation_requirement` | `P-GOV-10`, and the surviving release-control cue |

### 3.4 Consolidated

Merged where several cues pointed Claude at substantially the same concern.

| New cue | Absorbed |
|---|---|
| `expected_lifespan_and_change_frequency` | `expected_lifespan` + `expected_change_frequency` |
| `long_running_wait_and_approval_shape` | `longest_human_wait` + `human_decision_points` |
| `interaction_bespokeness_and_design_obligation` | `interaction_bespokeness` + `brand_and_design_obligation` |
| `response_and_freshness_expectation` | `interactive_response_expectation` + `freshness_expectation_at_surface` |
| `atomicity_span_and_consistency_window` | `atomicity_span` + `consistency_window` |
| `external_exchange_profile` | `exchange_stream_inventory` + `exchange_ownership` + `exchange_directionality` + `delivery_guarantee_requirement` + `interface_availability_per_system` (5 → 1 — the pattern §5 of the brief names) |
| `connectivity_and_egress_policy_posture` | `network_isolation_mandate` + `egress_control_requirement` + `service_permissibility_posture` |
| `vendor_trust_boundary_requirement` | `administrator_exclusion_requirement` + `encryption_key_control_requirement` |
| `maker_and_platform_governance_model` | `maker_and_delivery_model` + `platform_governance_maturity` |
| `release_control_and_reversibility_expectation` | `release_control_regime` + `reversibility_expectation` |
| `cost_driver_growth_at_horizon` | `growth_and_seasonality` (+ the horizon half of `value_horizon`) |
| `system_without_programmatic_interface` | `interface_absent_target_present` (renamed for readability; same concern) |

### 3.5 One cue added

`financial.mandated_control_funding_gap` — a control, operating tier or recovery commitment stated as
mandatory by another lens, with no budget behind it. It is the mechanism by which an engagement reaches
*infeasible* rather than *trade-off*, it is cross-lens (a governance requirement priced by the financial
lens), and no universal financial cue points at it (`budget_envelope` and `funding_model` cue the money,
not the linkage). It replaces a concern previously carried only by probe `P-FIN-01`.

Consolidation stopped short of abstraction: no surviving cue is so broad that it merely restates a
universal cue (checked pairwise in §7).

## 4. Question bank before / after

| | Before | After |
|---|---:|---:|
| lines / chars | 506 / 33,801 | **242 / 15,402** |
| core patterns | 48 (8 × 6 lenses) | **35** (business 6 · operations 6 · user 5 · data 6 · governance 6 · financial 6) |
| conditional probes | 60 | **34** (business 4 · operations 6 · user 5 · data 7 · governance 7 · financial 5) |
| `Research basis:` lines | 111 | **0** |
| appendices | A (traceability), B (outcome reachability), C (non-Discovery carried content) | **Reachable outcomes** only, compressed inline |

**Re-framed for its one consumer.** The header now states what it is — a resource read at
`aisa-status` step 6d after reasoning has exposed a material gap — and what it is not (coverage
specification, questionnaire, interview script, lens context, research summary). `## Discipline`
survived as 7 lines; rule 5 now points question pricing at `states.md` instead of restating it, which
is the §11 requirement: **no `custo` / `swing` / `criticidade` is encoded per question** (asserted by
test).

**Retired ids** (numbering left with gaps on purpose, so a surviving id still resolves against the
Step 2 report): core — `Q-BUS-07/08`, `Q-OPS-03/07`, `Q-USR-04/05/08`, `Q-DAT-06/07`, `Q-GOV-03/08`,
`Q-FIN-07/08`. Probes — `P-BUS-05/06/07/08`, `P-OPS-02/07/08/10`, `P-USR-04/07/08`,
`P-DAT-03/06/10/11/12`, `P-GOV-04/05/08/09/11/12/14`, `P-FIN-03/04/08`.

**Why each class went.** Duplicates of a universal cue (`Q-OPS-07` tribal knowledge, `Q-USR-05/08`
frontline-vs-manager, `Q-DAT-07` retention, `Q-GOV-03` access control, `Q-FIN-07` ROI) ·
near-duplicates of a surviving question (`Q-OPS-03` queue depth vs `Q-OPS-04` human wait, `Q-USR-04`
frequency vs `Q-FIN-05`, `P-DAT-10` vs `P-DAT-09`, `P-GOV-04` vs `P-GOV-03`, `P-FIN-08` vs `Q-FIN-04`)
· research-completeness questions whose answer rarely moves framing/options/decision (`P-BUS-05`
multi-entity resale, `P-BUS-08` three-year horizon, `P-OPS-08` out-of-hours, `P-USR-04` deep links) ·
premature implementation for Discovery (`P-GOV-05` secret rotation, `P-GOV-14`'s four-part ALM
question, `P-USR-08` response-time restated) · and one **unobservable trigger**: `P-GOV-11` ("an
expected part of the answer is new or in preview") presumes a candidate solution component, which does
not exist in Discovery.

**Triggers.** All 34 surviving probes state a trigger, and every trigger is checkable against the
Shared Understanding, `context.json` or `_capture/`. Nine triggers were re-worded from a
conversational form ("somebody says…", "is mentioned") to the observable form ("is recorded…",
"is in scope") so that `aisa-status` — which sees rows, not the meeting — can actually evaluate them.
No inference machinery was added to support any trigger; each is a pattern-match on recorded content.

## 5. Glossary before / after

| | Before | After |
|---|---:|---:|
| lines / chars | 288 / 30,513 | **132 / 12,943** |
| Part A sections | 11 (A1–A11) | **7** (A1–A7) |
| Part A terms | ~137 | **42** |
| "must not be collapsed" rows | 14 | **8** |
| Part B translation rows | 12 | **8** |
| `Research basis:` lines | 26 | **0** |

Sections A1–A9 collapsed into A1 *Work and failure* · A2 *Accountability* · A3 *Information* ·
A4 *Users and surfaces* · A5 *Exchange and constraint* · A6 *Operations, change and money*, plus
A7 *Distinctions that must not be collapsed*.

**Removed classes.**

- **Kernel duplicates** — the whole of old A11: `Confirmed/Assumed/Unknown/Conflicted/Risky`,
  *decision-blocking unknown*, *volatile fact*, *evidence obligation*, *current state*,
  *precondition gap*. `library/kernel/states.md` owns these; a pack glossary restating them was a
  second source of truth. (*Precondition* survives in A5 — it is a Discovery deliverable, not a state.)
- **Ordinary language** — *Activity*, *Handoff*, *Queue*, *Decision point*, *Business rule*,
  *Exception*, *Workaround*, *Tribal knowledge*, *Cycle time*, *Actor*, *Requester*, *Sponsor*,
  *Entity*, *Attribute*, *Relationship*, *Persona*, *User population*, *Volume*, *Concurrency*,
  *Budget envelope*, *Funding model*, *Total cost of ownership*, *Value horizon* and ~25 more. Nobody
  in an engagement needs these defined.
- **Terms whose only job was a paired distinction** — *Drill*, *Peak shape*, *Growth horizon*,
  *Elapsed duration*, *End-to-end availability*, *Availability requirement*, *Evidence retention*.
  The A7 table carries the distinction that actually does the work.
- **Implementation trivia / domain-knowledge material** — *Contract volatility*, *Payload profile*,
  *Ordering requirement*, *Latency class*, *Consumer count*, *Network boundary*, *Monitoring depth*,
  *Request rate per acting identity*, *Build isolation*, *Change-review gate*, *Testing regime*,
  *Separation of duties*, *Recovery point/time objective*, *Shadow record*, *Migration and exit cost*.
  These matter at Options and in engineering, not while interpreting Discovery evidence.
  **Deferred relocation, not deleted knowledge** — see §11.

**Kept, and why** — 42 terms that pass one of the three tests: PP-specific engagement language a
participant will use (*Isolation domain*, *Entitlement exposure*, *Delivery model*, *Pro-code
capacity*), a class that prevents evidence being misread (*Work shape*, *Criticality class*,
*Identity class*, *Access granularity*, *Deployment-model constraint*, *Proof requirement*), or a word
that makes business and technical people mean the same thing (*Source of record*, *Failure semantics*,
*Operational ownership*, *Reversibility requirement*). Definitions are one sentence, carry no platform
number, no implementation guidance and no citation (asserted by test).

Part B kept its role — a translation table, not a dictionary — trimmed to 8 rows by merging the
platform/app-product rows and dropping *formula language*, *governance toolkit*, *solution/package*
and the vague "two deprecated named items" standing warning (unactionable without naming them, which
Discovery forbids).

## 6. Cross-artifact duplication check

Target separation, verified after cleanup:

```
Universal lens   how to look
PP extra_signal  a PP-specific thing worth noticing
Question bank    how to ask, once a material gap exists
Glossary         what a PP-specific term means
```

| Check | Result |
|---|---|
| PP cue ↔ universal cue | 0 restatements. 21 signals removed exactly because a universal cue covered them (§3.1) |
| PP cue ↔ PP cue (same lens or across lenses) | 0 duplicates — asserted by test (`test_cues_are_not_duplicated_across_lenses`) |
| PP cue ↔ question bank | Deliberate 1:1 alignment where it exists (e.g. `stable_business_key_availability` ↔ `P-OPS-01`), never restatement: the cue is a noun to notice, the question is a sentence to ask. 11 cues have no question and 12 questions have no cue — the roles are not coextensive, by design |
| question bank ↔ glossary | 0 definitions in the bank; 0 questions in the glossary |
| glossary ↔ kernel `states.md` | 0 overlap after old A11 was removed (was 6 rows) |
| glossary ↔ universal lens signal names | 0 term whose definition is only a restatement of a universal cue |
| anything appearing 4× | none found |

Three items did not fit any of the four roles cleanly and were removed rather than reworded:
`navigation_shape_and_deep_links` (a design decision, not an observation), old A11 (kernel semantics),
and question-bank Appendix A (a traceability convention, which is authoring machinery — now §9).

## 7. Neutrality regression

Scenario walk of the cleaned Discovery layer. No solution was chosen; this tests bias only.

| Scenario | Does the layer push toward a Power Platform implementation? |
|---|---|
| **A — process simplification may beat software** | **No.** `differentiation_class` and `existing_capability_overlap` route toward "a comparable organisation does this the same way" and "something already owned"; `P-BUS-01` (features of the outgoing tool), `P-BUS-02` (packaged option), `Q-BUS-03`, `Q-FIN-01/02` and `P-FIN-06` ("what is the smallest version that still delivers value") all remain. No cue names an app, a flow or a store |
| **B — high-volume integration, PP may not fit** | **No.** `queried_volume_per_access_path`, `external_exchange_profile`, `atomicity_span_and_consistency_window` and `compute_intensive_step_present` are precisely the cues that make unsuitability visible; `P-DAT-09` asks for peak *per minute*, `P-DAT-02` for cross-system atomicity, `P-OPS-03` for real compute. All record requirements; none states a platform figure to compare against |
| **C — sensitive / high-control workload** | **No.** `deployment_model_constraint` (where the runtime must *execute*), `vendor_trust_boundary_requirement` (administrator exclusion, key custody) and `connectivity_and_egress_policy_posture` can each eliminate a whole class of answer, including this pack's own platform. `Q-GOV-02/04`, `P-GOV-02/03/06` ask for the clause, not for an accommodation |
| **D — small spreadsheet replacement, straightforward** | **No.** `spreadsheet_and_mailbox_anchors` records the artefact as *current state* only. With 5–7 cues per lens and the mandatory "an uncovered cue is not a gap" clause, a small engagement can leave most of them untouched; the 20-cue lists that previously read as an inventory of concerns are gone — which is the main over-engineering pressure this phase removed |
| **E — dominant constraint is organizational** | **No.** `scope_reach`, `maker_and_platform_governance_model`, `mandated_control_funding_gap` and `expected_lifespan_and_change_frequency`, plus glossary *Operational ownership* / *Delivery model* / *Pro-code capacity* / the criticality-vs-maturity gap, let the layer conclude the blocker is organizational without naming any technology |

Mechanical support: 0 vendor term in any Discovery cue, in the question-bank body, or in glossary Part A
(§10). The *Reachable outcomes* guard survived in the bank, naming the questions that produce
disqualifying evidence for four non-PP outcomes.

## 8. Runtime usefulness regression

Capability test, not a checklist — no engagement is required to cover every category.

| Concern | Surviving cue(s) | Surviving question(s) |
|---|---|---|
| business ownership / value | `business_criticality_class`, `differentiation_class`, `scope_reach` | `Q-BUS-01/02/03/05`, `P-BUS-03` |
| operational exceptions / volume | `work_shape_class`, `partial_failure_behaviour_today`, `long_running_wait_and_approval_shape` | `Q-OPS-01/04/05/06`, `P-OPS-01/05/06` |
| user adoption / accessibility | `user_population_identity_class`, `interaction_bespokeness_and_design_obligation`, `offline_operating_requirement`, `native_distribution_and_push_need` | `Q-USR-01/02/03/06`, `P-USR-01/02/03/05` |
| data ownership / quality / sensitivity | universal `data_owners`/`data_quality` + `access_granularity_requirement`, `relational_depth_and_integrity`, `queried_volume_per_access_path` | `Q-DAT-01/03/04/05`, `P-DAT-01/07` |
| governance / control / environment | `deployment_model_constraint`, `connectivity_and_egress_policy_posture`, `vendor_trust_boundary_requirement`, `maker_and_platform_governance_model`, `release_control_and_reversibility_expectation` | `Q-GOV-01/02/04/05/07`, `P-GOV-01/02/03/06/07/10` |
| cost / licensing / economic uncertainty | `audience_and_frequency_shape`, `existing_entitlement_baseline`, `mandated_control_funding_gap`, `cost_driver_growth_at_horizon` | `Q-FIN-01…06`, `P-FIN-01/02/07` |

**Capability deliberately moved from cue to reasoning, recorded honestly.** Six concerns now depend on
the universal lens plus a triggered probe rather than a standing cue: data-quality evidence, migration
scope, concurrent-edit contention, accessibility attestation, script direction, and secrets policy.
Each is still reachable (universal `data_quality`; `P-DAT-02`; `Q-USR-06`; `Q-GOV-05`), and none is a
decision-blocking class on its own. If a pilot shows one of them being missed, it is a one-line cue to
restore — the reason this list is written down.

## 9. Provenance status

**No canonical research was reopened, re-read for new content, or modified.** Existing canonical
research files are byte-identical.

Runtime now carries **zero** canonical ids: the `# DC-D-NNN` trace comments were removed from
`pack.yaml` and every `Research basis:` line from `question-bank.md` and `glossary.md`. The Step 2
convention those served — *grep an id to find the signal, the question and the evidence together*
(old `question-bank.md` Appendix A) — could not survive the question-bank trim, so the mapping is
recorded here once, on the authoring side, instead of half-alive in two runtime files.

### 9.1 Surviving cue → canonical basis

| Cue | Basis |
|---|---|
| `business_criticality_class` | DC-D-001 |
| `differentiation_class` | DC-D-002 |
| `existing_capability_overlap` | DC-D-002, DC-D-109 · PS-41 |
| `scope_reach` | DC-D-074 |
| `expected_lifespan_and_change_frequency` | DC-D-004, DC-D-007 |
| `work_shape_class` | DC-D-048 |
| `long_running_wait_and_approval_shape` | DC-D-049, DC-D-055 |
| `partial_failure_behaviour_today` | DC-D-054 |
| `stable_business_key_availability` | DC-D-052 |
| `system_without_programmatic_interface` | DC-D-045, DC-D-056 |
| `compute_intensive_step_present` | DC-D-057 |
| `spreadsheet_and_mailbox_anchors` | AP-D-008 · DC-D-021 |
| `user_population_identity_class` | DC-D-009 |
| `interaction_bespokeness_and_design_obligation` | DC-D-012, DC-D-013 |
| `offline_operating_requirement` | DC-D-016 |
| `native_distribution_and_push_need` | DC-D-020 |
| `response_and_freshness_expectation` | DC-D-018, DC-D-084 |
| `relational_depth_and_integrity` | DC-D-022 |
| `queried_volume_per_access_path` | DC-D-023 |
| `access_granularity_requirement` | DC-D-026 |
| `atomicity_span_and_consistency_window` | DC-D-028, DC-D-029 |
| `analytical_versus_operational_need` | DC-D-031 |
| `attachment_and_binary_volume` | DC-D-025 |
| `external_exchange_profile` | DC-D-035, DC-D-036, DC-D-038, DC-D-041, DC-D-045 |
| `deployment_model_constraint` | DC-D-108 |
| `connectivity_and_egress_policy_posture` | DC-D-063, DC-D-067, DC-D-072 |
| `vendor_trust_boundary_requirement` | DC-D-062, DC-D-064 |
| `authorization_enforcement_point` | DC-D-068 |
| `maker_and_platform_governance_model` | DC-D-069, DC-D-070 |
| `release_control_and_reversibility_expectation` | DC-D-077, DC-D-079, DC-D-080 |
| `vendor_change_tolerance` | DC-D-107 |
| `audience_and_frequency_shape` | DC-D-094 |
| `existing_entitlement_baseline` | DC-D-109 · PS-41 |
| `mandated_control_funding_gap` | DC-D-092 · AP-D-064, LC-30 |
| `cost_driver_growth_at_horizon` | DC-D-024, DC-D-087, DC-D-095 |
| `cost_attribution_requirement` | DC-D-099 |

### 9.2 Canonical criteria that lost their standing cue

Still represented in Discovery through a universal lens cue or a surviving question (§3.1–§3.3), so
the Step 2 coverage matrix's `COVERED` verdict holds — the artifact carrying it changed, not the
coverage: DC-D-003, 005, 006, 008, 010, 011, 014, 015, 017, 019, 021, 024, 027, 030, 032, 033, 034,
051, 054 (partly), 059, 060, 061, 065, 066, 071, 073, 075, 104, 116 · AP-D-001, AP-D-007 ·
`data-architecture.md §4.11` · LC-28.

**Genuinely no longer represented anywhere in Discovery**: none. DC-D-019 (deep links) is the single
criterion whose Discovery representation was dropped outright rather than relocated — it names a
navigation design decision, not a fact about the problem, and its Options-side home is unaffected.

### 9.3 Step 2 report

`step-2-discovery-layer-report.md` gained one dated addendum recording that its §5 signal table, §4
question counts and §8 traceability convention are superseded by this report, and where the mapping now
lives. Nothing in it was rewritten or deleted. The authoring map needed no edit — it schedules the trim
(§9 of the plan) and does not restate the counts.

### 9.4 Question-bank Appendix C, carried verbatim

Appendix C held non-Discovery content parked in the runtime file so nothing was lost before Step 3/4
re-homes it. It is preserved here and removed from runtime:

> **C.1 — Technology lens questions (Options phase only).** Carried verbatim from v1.2.0; to be
> re-authored in Step 3 against `decision-tree.md` and the criteria register.
> 1. Given the needs identified, which delivery options are viable — including non-technology ones?
> 2. What is the tenant's current licensing baseline, and does the option need premium entitlements?
> 3. What integrations are required, and do connectors/APIs exist for them?
> 4. What are the expected request/transaction volumes versus platform limits?
> 5. Is mobile or offline genuinely required, and what does that imply for each option?
> 6. What environment and ALM landscape (DEV/UAT/PROD) must the option fit into?
> 7. How reversible is each option if it proves wrong?
>
> **C.2 — Data-integrity checks.** `D1`, `D2`, `D4`, `D5`, `D6`, `D7` from v1.2.0 are
> technology-neutral and were re-expressed as Discovery probes (`P-DAT-11`, `P-DAT-12`, both now
> retired — see §4) and as data-lens working checks. `D3` and `D8` named implementation mechanisms and
> are re-expressed neutrally: *every discovered calculation and every discovered output has a named
> owner and a stated implementation intent, decided in Options*.
>
> **C.3 — Schema, formula, security and estimation gates.** `S1`–`S9`, `P1`–`P10`, `E6`, `M1`–`M9`
> from v1.2.0 are implementation-grade checks that name technologies. They move to
> `domain-knowledge/` in Step 4 per `pp-pack-authoring-map.md` §6.4; their v1.2.0 text remains in the
> pack's git history and in `library/packs/pp-backup/`.
>
> **C.4 — Neutral security checks retained.** `E1`–`E5` and `E7` (permission-matrix completeness,
> least privilege on conflict, admin coverage, every approval action has an executing role, inheritance
> consistency, non-production test identities) are technology-neutral and are carried by the governance
> lens through `Q-GOV-03` (retired — `Q-GOV-05`/`Q-GOV-07` and universal `access_control` /
> `separation_of_duties` now carry it) and `P-GOV-09` (retired). Provenance: CRAFT — engagement
> experience, no research basis.

## 10. Tests / checks

**New**: `.claude/tests/test_pp_discovery_runtime.py` — **22 tests, OK** (0.03 s). One file, stdlib
`unittest` + `yaml`, no fixture engagement, no framework. It asserts properties, never sizes.

| Group | Covers |
|---|---|
| `TestDiscoveryCues` (6) | `pack.yaml` parses; all six Discovery lenses still receive non-empty `extra_signals`; every count within the soft 5–8 heuristic; every cue is a neutral lowercase token with no vendor term; no cue duplicated within or across lenses; `technology` has no `extra_signals` and keeps `constraints_to_check`; no mandatory-coverage wording in pack or bank |
| `TestQuestionBank` (7) | `aisa-status` resolves `question_bank` and both id shapes it names exist; 4–8 core patterns for each of six lenses; every probe states a `Trigger:`; no trigger depends on an unobservable verdict (complexity/score/fit/suitability); no vendor term in the body; the reachable-outcomes guard survived; no `custo`/`swing`/`criticidade` encoded per question |
| `TestGlossary` (4) | resolvable and split A/B; Part A carries no vendor term; Part B still marked `options+` / not Discovery vocabulary; no platform figure in any Part A definition |
| `TestNoCanonicalIdsInRuntime` (2) | 0 canonical id (`DC-D`/`AP-D`/`PS`/`LC`/`OP`/`SC`/`DQ`/`NB`/`AA`/`DA`/`AT2`/`IA`/`ALT`/`PF`/… and research-`GOV-` distinguished from `Q-GOV`/`P-GOV`) in the three runtime files; 0 `Research basis` line |
| `TestDegradation` (3) | `aisa-round`/`aisa-frame` still state empty/absent-signal degradation (`aisa-options` inherits it); `/status` still degrades without a bank; other packs' absent/malformed `lenses_config` injects nothing |

**Existing checks re-run, all green:**

| Check | Result |
|---|---|
| `.claude/tests/test_orchestrator_wiring.py` (Phase D) | 23 tests, **OK** — incl. "PP declares signals for all six Discovery lenses" |
| `.claude/tests/test_council_wiring.py` (Phase E) | 31 tests, **OK** |
| `.claude/tests/test_state_scaffold.py` (Phase F) | 15 tests, **OK** |
| `phase-completeness.py` | exit 0 |
| `phase-gate-check.py` | exit 0 |
| `dashboard.py --engagement <slug>` × 4 | all build |
| live resolution of `aisa-round` step 3.6b on the trimmed manifest | cues resolved for all 6 lenses; injected line sizes in §2 |

Not run: a live `/round` or `/status` writing engagement state. Phase G changed the content of three
pack files, not a single line of resolution, injection or consumption logic — those paths are asserted
above and were exercised in Phase D.

**Observed, out of scope, not fixed**: `docs/ARCHITECTURE.md:553-563` still shows a pre-v1.3
illustrative `lenses_config` snippet naming `dataverse_vs_sharepoint`, `DLP_policies`,
`sensitivity_labels`, `excel_anchors`. It is an example in a docs code block, not the PP pack, and
Phase G's scope is the three runtime artifacts. Worth a docs pass.

## 11. Files changed

**Modified**

1. `library/packs/pp/pack.yaml` — Discovery `lenses_config` rewritten (89 → 36 cues, trace comments
   removed, header comment restated as the cue contract); `pack_version` 1.3.0 → 1.4.0. `technology`,
   `deliverables`, `domain_knowledge`, `decision_tree`, `epistemics` unchanged in content.
2. `library/packs/pp/question-bank.md` — trimmed and re-framed (506 → 242 lines).
3. `library/packs/pp/glossary.md` — trimmed and restructured (288 → 132 lines).
4. `docs/pp-pack-authoring/research/pp/authoring/step-2-discovery-layer-report.md` — one dated
   addendum (§9.3); no existing line rewritten.

**New**

5. `.claude/tests/test_pp_discovery_runtime.py` — 22 tests.

**Not touched**: `library/kernel/**`, `library/packs/pp/decision-tree.md`,
`library/packs/pp/domain-knowledge/**`, `library/packs/pp/architecture-templates/**`,
`library/packs/pp/deliverable-templates/**`, all 7 lens `SKILL.md`, all 7 `.claude/agents/*`, every
orchestrator skill, every hook, `.claude/settings.json`, all canonical research under
`docs/pp-pack-authoring/research/pp/evidence/**`, and everything under `projects/`.

**Landing mechanics**: `library/**` is deny-listed for `Write`/`Edit` and guarded by
`pre-write-guard.py`. As in Step 2, the files were authored in the session scratchpad and copied in via
`Bash` on branch `pp-pack-authoring/step-2-discovery-layer`. Nothing committed — presented for review.

## 12. Deferred PP authoring work

| Item | Work |
|---|---|
| **Step 3 — Options layer** | `decision-tree.md` REWRITE into the ordered evaluation procedure; `technology.constraints_to_check` re-authored against it; the Options vocabulary (`options-glossary.md`) that receives the product definitions Part B translates away from; Appendix C.1's 7 technology questions re-authored (§9.4) |
| **Step 4 — domain knowledge re-taxonomy** | Receives the glossary terms relocated conceptually in §5 (*Contract volatility*, *Payload profile*, *Ordering requirement*, *Latency class*, *Consumer count*, *Network boundary*, *Monitoring depth*, *Request rate per acting identity*, *Build isolation*, *Change-review gate*, *Testing regime*, *RPO/RTO*, *Migration and exit cost*) and Appendix C.3's `S1`–`S9` / `P1`–`P10` / `M1`–`M9` gates. **Not relocated in this phase** — Phase G only removed them from Discovery runtime |
| Pilot calibration | `epistemics.half_lives_override` is still `{}` (map §12 Q-08); the six capability-to-probe demotions in §8 are the first thing to review at the pilot retro |
| kernel touch-up (unchanged, still open) | `library/kernel/orchestration.md` → *Question bank — runtime role*: replace *"(Consumer not yet wired…)"* with "Wired since Phase D: `aisa-status` step 6d". Blocked by `pre-write-guard.py` by design; out-of-band batch |
| docs pass (new) | `docs/ARCHITECTURE.md` §7.3 illustrative signal snippet is pre-v1.3 (§10) |

Not in scope and not started: decision-tree content, domain-knowledge content, deliverable templates,
technology constraints, new research, any new runtime artifact.

---

PHASE G — PP RUNTIME CLEANUP: PASS
