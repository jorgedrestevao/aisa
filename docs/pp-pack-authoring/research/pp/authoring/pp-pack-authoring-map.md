# PP Pack Authoring Map

**Step:** PP PACK AUTHORING — STEP 1 (authoring map only)
**Date:** 2026-09-03
**Status:** authoring plan. Contains **no pack content** and modifies **nothing** under `library/packs/pp/`.
**Path resolution:** the repository has no top-level `research/`. The canonical research root is `docs/pp-pack-authoring/research/pp/`, so the requested `research/pp/authoring/pp-pack-authoring-map.md` resolves to `docs/pp-pack-authoring/research/pp/authoring/pp-pack-authoring-map.md`, alongside the existing `research/pp/evidence/`.

---

## 1. Baseline consumed

### 1.1 Canonical corpus (read-only, frozen)

Manifest: `research/pp/evidence/canonical-manifest.md` — §3 (Areas 1–12), §5 (semantic handling rules), §6 (non-blocking reservations), §7 (downstream extraction rules), §11–§13 (Block D, frozen).

| Layer | Area | File | Confidence | Primary id namespace |
|---|---:|---|---|---|
| Evidence | 1 Platform Suitability | `platform-suitability.md` | MEDIUM | `PS-NN` |
| Evidence | 2 Application Architecture | `application-architecture.md` | MEDIUM | `AA-NN`, sources `A-/B-/C-/D-/E-/V-` |
| Evidence | 3 Data Architecture | `data-architecture.md` | HIGH | `DA-NN`; sub-registers `DV:Sxx`, `SQ:Sx`, `SP:S-xx`, `EX:Sxx`, `XC:Sxx`, `VT:Sxx`, `SY:S-xx`, `SQ2:Sxx`, `SC:Sxx`, `DQ:Sxx` |
| Evidence | 4 Automation Architecture | `automation-architecture.md` | MEDIUM | `AT2-NN` |
| Evidence | 5 Integration | `integration-architecture.md` | MEDIUM-HIGH | `IA-NN`, `IA-C-*`, `IA-U-*` (mounted file uses local `C-01` form) |
| Evidence | 6 Security | `security.md` | MEDIUM | `SEC-*`, `S-NN`, `SEC-XB-0N` |
| Evidence | 7 Governance | `governance.md` | MEDIUM | `GOV-*`, `G-NN`, `GOV-XB-0N` |
| Evidence | 8 ALM / DevOps | `alm-devops.md` | MEDIUM | `ALM-NN`, `D-NN` |
| Evidence | 9 Performance and Scale | `performance-scale.md` | MEDIUM | `PF-NN` |
| Evidence | 10 Licensing and Cost | `licensing-cost.md` | MEDIUM | `LC-NN`, file-local `DC-01…DC-18` |
| Evidence | 11 Operations and Support | `operations-support.md` | MEDIUM | `OP-NN`, file-local `DC-01…DC-20` |
| Evidence | 12 Architecture Patterns | `architecture-patterns.md` | MEDIUM | `APR-*`, `AP-01…AP-10`, `Y-01…Y-14` |
| Decision | 15 Decision Criteria | `decision-criteria.md` | MEDIUM | `DC-D-001…116` |
| Decision | 13 Anti-Patterns | `anti-patterns.md` | MEDIUM | `AP-D-001…068` |
| Decision | 14 Alternatives | `alternatives.md` | MEDIUM | `ALT-001…011` |
| Decision | — Decision Intelligence Matrix | `decision-intelligence-matrix.md` | MEDIUM | consumes the three above; 12 composed rows, 8 evaluation steps, 18 scenarios |

### 1.2 Baseline verification performed in this step (read-only, mechanical)

| Check | Result |
|---|---|
| `DC-D-001…116` present and contiguous | 116 / 116, no gaps |
| `AP-D-001…068` present and contiguous, register vs entries | 68 ids · 68 register rows · 68 `####` entries |
| `ALT-001…011` present | 11 / 11 |
| Manifest §11 counts vs files | Criteria and alternatives match; anti-patterns match at 68 |
| Internal count line `anti-patterns.md` §4 "Count: 67" | **Disagrees** with §3.12 (68), §9 (68), the register (68) and manifest §11 (68). Stale pre-`AP-D-068` line. **Not repaired** — recorded as open question **Q-01** (§12) |

### 1.3 Binding rules inherited by authoring

Non-negotiable, from the manifest and Block D:

1. Manifest §5 semantic states — `UNKNOWN`, `CONFLICTED`, `VOLATILE VALUE`, `INF` — survive into the pack unchanged.
2. Manifest §6 reservations `NB-01`…`NB-08` are evidence, not defects. Authoring may not "clean them up".
3. Manifest §7 extraction rules bind: no invented thresholds, no `INF`/`T3`/`T4` restated as Microsoft recommendation, documented limit ≠ measured performance, Power Platform rejection is a valid outcome.
4. Block D §12.1 adds `COMPARATOR EVIDENCE ABSENT`, the exit taxonomy `Xp/Xr/Xe/Xc`, the non-exit classes `Ri/Cf`, the `GATE`/`CONSTRAINT`/`ANTI-PATTERN` enforcement classes, the closed 14-member outcome set, and the **non-commutative** evaluation order.
5. Block D ids are canonical and closed: pack ids **reference**, never replace or renumber.

### 1.4 aisa-side contracts consumed

`library/kernel/phases.md` · `states.md` (5 states, epistemic half-lives, question economics `custo`/`swing`) · `render-contract.md` (synthesis → render, slot resolution, `applies_to`) · `blueprint-contract.md` (screen catalogues and hard caps come from the pack) · `orchestration.md` · `library/kernel/glossary.md`.
Repo rules: `.claude/rules/no-tech-mention-before-options.md` · `library-readonly.md` · `render-on-decision-only.md` · `shared-understanding-as-source-of-truth.md`.
Guides: `docs/PACK_AUTHORING.md` · `docs/DELIVERABLE_AUTHORING.md` · `docs/LENS_AUTHORING.md`.

### 1.5 Authoring principles (binding from Step 3)

Governing principle: **evidence-heavy authoring, evidence-light runtime**. Evidence-light runtime does not mean decision-light reasoning.

1. **Light framework, not lightweight reasoning.** Framework mechanics shrink; analysis does not.
2. **Compress repetition, not decision coverage.** A concern is never dropped merely to reduce context size.
3. **Broad coverage, selective depth.** Material concerns are considered; how deeply is proportional to relevance, risk, uncertainty and consequence.
4. **Minimum sufficient complexity** — the least framework complexity that still preserves materially complete, balanced and defensible reasoning. *Not* the smallest number of rules, stages or criteria.
5. **Research completeness is authoring input, not runtime payload.** The corpus is exhaustive so the pack need not be.
6. **Materiality determines depth.**
7. **Domain knowledge deepens a concrete decision question; it does not flood context pre-emptively.** Pull-based, never push-based.
8. **Neutrality means the active technology pack must remain capable of concluding that its own technology is not the best option.** `Xp/Xr/Xe/Xc`, `DECISION BLOCKED` and the `ALT` classes are real outcomes, not escape hatches.

**Survival test for authoring compression.** A concern survives — it may not be compressed away — when its omission could materially change: viability · option class · architecture · security/control posture · governance · lifecycle/ALM · scale/performance · operability · cost/economics · risk · reversibility · preference · decision confidence.

**Discovery vs Options.** Discovery stays exploratory and evidence-led: no fixed checklist to traverse, but material concerns exposed by evidence must be followed. Options requires **broad systematic decision coverage** — every serious option is considered against every *material* decision concern, with depth varying by relevance, risk, uncertainty and consequence. Identical depth per option is not required; silent omission of a material concern is not permitted.

**Signals do not bound reasoning.** Discovery signals (universal or `extra_signals`) and the question bank are attention cues. Absence of a cue never authorises ignoring a material concern. This does **not** license inflating signal counts, the question bank or the glossary: the principle protects reasoning depth, not framework size.


---

## 2. Existing PP pack inventory

`library/packs/pp/` — pack_version `1.2.0`, 26 files, 4,961 lines. Consumers outside the pack are listed because renames have a blast radius (§12 Q-05).

| File | Lines | What it is today | External consumers |
|---|---:|---|---|
| `pack.yaml` | 92 | Manifest: 6 deliverables, 7 lens configs, 13 domain-knowledge files, empty `epistemics.half_lives_override` | `aisa-start`, `aisa-options`, `lens-*`, `aisa-render` |
| `glossary.md` | 95 | ~55 vendor terms + a 6-axis "Discovery fit criteria" rating vocabulary | lenses, deliverables |
| `question-bank.md` | 137 | 45 lens questions + 4 "quality gate" blocks (D1–D8, S1–S9, P1–P10, E1–E7, M1–M9) | all lenses |
| `decision-tree.md` | 157 | 3 branches (`sharepoint-first`, `dataverse-first`, `hybrid`), R0 hard gates + R1–R6 scored rules, hybrid trigger, exclusion side-effects | `lens-technology`, `solution-architect`, `aisa-simulate` |
| `architecture-templates/sharepoint-first.md` | 34 | Slot template for branch A | `solution-blueprint`, `claude-design-brief` |
| `architecture-templates/dataverse-first.md` | 38 | Slot template for branch B | idem |
| `architecture-templates/hybrid.md` | 38 | Slot template for branch C | idem |
| `deliverable-templates/discovery-report.template.md` | 54 | client, 7 required slots | `aisa-render` |
| `deliverable-templates/executive-report.template.md` | 60 | sponsor, 6 required slots | `aisa-render` |
| `deliverable-templates/solution-blueprint.template.md` | 55 | technical, 7 required slots + arch sub-template | `aisa-render` |
| `deliverable-templates/implementation-spec.template.md` | 77 | developer, 9 required slots | `aisa-render` |
| `deliverable-templates/claude-design-brief.template.md` | 67 | claude-design, 7 required slots, cross-refs 4 domain-knowledge files | `aisa-render` |
| `deliverable-templates/estimate.template.md` | 63 | client, 9 required slots | `aisa-render` |
| `domain-knowledge/powerfx-patterns.md` | 566 | Delegation, traps, validation sequence, standard Power Fx patterns | `lens-technology`, design brief |
| `domain-knowledge/flows-patterns.md` | 514 | Connector reference, flow templates, expressions, adaptive cards | `lens-technology` |
| `domain-knowledge/azure-sql-reference.md` | 554 | Types, mandatory audit columns, medallion, SP template, DAG, RLS, CTE, MERGE, temporal, indexes | `lens-technology`, `decision-tree` |
| `domain-knowledge/dataverse-reference.md` | 437 | Types, reserved names, flags, relationships, calc tiers, roles, limits, plugin choice matrix | idem |
| `domain-knowledge/security-patterns.md` | 392 | Role inference, permission matrices, conflict resolution, Power Fx security blocks | design brief |
| `domain-knowledge/sharepoint-reference.md` | 379 | Column types, hard limits, indexing, groups, no-RLS/CLS workarounds, delegation specifics | `lens-technology`, `decision-tree` |
| `domain-knowledge/screen-patterns.md` | 269 | 5 screen types, density, badge colours, navigation, states | `aisa-blueprint`, design brief |
| `domain-knowledge/estimation-model.md` | 260 | Effort tables, multipliers, phases, risk register, **indicative licence prices** | `aisa-simulate`, `estimate` |
| `domain-knowledge/anonymization.md` | 205 | Anonymisation + synthetic-data rules | design brief |
| `domain-knowledge/excel-patterns.md` | 203 | Excel → Power Fx / T-SQL translation catalogue | `lens-technology`, capture |
| `domain-knowledge/delegation-matrix.md` | 77 | Delegable operations, Dataverse vs SharePoint | `lens-technology`, `aisa-simulate`, agent memory |
| `domain-knowledge/screen-consolidation-rules.md` | 76 | Field-count → screen-type tree, naming, hard caps | `aisa-blueprint` (**named contract**) |
| `domain-knowledge/delivery-conventions.md` | 62 | Naming, traceability stamping, environments, go-live checklist | `lens-technology` |

### 2.1 Structural findings against the canonical baseline

Recorded here because they drive §3's verdicts.

- **F-01 — the decision tree is a scoring model.** R1–R6 emit graded verdicts (`forte`/`adequada`/`inadequada`) that the architect "aggregates and scores". `decision-criteria.md` §2.3 and §2.4 state the corpus supports **states, not scores**, and explains why a scoring model is the specific construct that loses the composed disqualifiers (`AP-D-059`, matrix §3).
- **F-02 — the decision tree contains invented numbers.** `30,000` rows for SharePoint, `formula_count > 100`, `external_integrations_count > 3`, "sub-second" as a Dataverse exclusion, and the 5,000/100,000 volume bands carry no canonical source. The canonical SharePoint figures are `5,000` LVT / `30M` items / 12 joins (`DA-39`, `DA-40`); no concurrent-user ceiling and no standard-table row ceiling are published anywhere (`SC-16`, `SC-18`). This is `AP-D-051` — classification **`CONSTRAINT`**, i.e. always wrong within scope.
- **F-03 — the option space is three branches wide.** The corpus requires **11** alternative classes (`ALT-001…011`, including three that are not technology decisions) and a **closed 14-class** outcome set (`decision-criteria.md` §6.2). The current tree cannot emit `DECISION BLOCKED`, `ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED`, `IN-PLACE REMEDIATION UNAVAILABLE`, an `Xr` partial-scope exit, or `COMPARATOR EVIDENCE ABSENT`.
- **F-04 — evaluation order is absent.** Matrix §5 is explicit that order is non-commutative (absolutes → blocking unknowns → shape → envelope → composed → gates → economics → direction → comparator check → validation level). The current tree runs R0 then R1–R6 in register order.
- **F-05 — Discovery contamination in the question bank.** `question-bank.md`'s quality-gate blocks name Dataverse, Azure SQL, SharePoint, Power Fx and Power Automate (`D3`, `S1`–`S9`, `P1`–`P10`, partly `E6`) inside a file every Discovery lens reads. §6 handles this.
- **F-06 — the glossary is a Discovery-visible vendor dictionary.** It is loaded by lenses in Discovery and is almost entirely product vocabulary, plus a rating scale that is a scoring model (F-01).
- **F-07 — prices in the pack.** `estimation-model.md § LICENSE COST ESTIMATES` quotes indicative per-user figures. `licensing-cost.md` §12: *"The pack must never quote a price."*
- **F-08 — no provenance anywhere.** No pack file carries a research reference, a volatility stamp or a provenance class. §8 fixes this.
- **F-09 — genuine, valuable, non-corpus content exists.** Power Fx craft, screen patterns, consolidation rules, anonymisation, delivery conventions and the estimation method are engagement-proven practice the corpus never evaluated. They must be **kept and labelled**, not deleted and not laundered into research-backed rules.

---

## 3. Target artifact inventory

Verdicts: **KEEP** · **UPDATE** · **REWRITE** · **SPLIT** · **MERGE** · **CREATE** · **DEPRECATE**.
Every row states the canonical basis for the verdict. Nothing here is executed in Step 1.

### 3.1 Pack root

| Artifact | Verdict | Why (canonical basis) |
|---|---|---|
| `pack.yaml` | **UPDATE** | Add: `decision_model` block pointing at the new registers; expanded `technology.constraints_to_check` derived from the 12 `DC-D` domains; `epistemics.half_lives_override` populated (`plataforma-tecnica` is the dominant class for this pack — `licensing-cost.md` §0.3, `decision-criteria.md` §7, matrix §4 service-limit group); `discovery_vocabulary` and `options_vocabulary` split; `provenance_classes` declared. No deliverable set change. |
| `glossary.md` | **SPLIT** | Into `discovery-vocabulary.md` (Discovery-visible, technology-neutral) and `options-glossary.md` (vendor vocabulary, Options-gated). Basis: `no-tech-mention-before-options.md`; `decision-criteria.md` §2.2 (technology neutrality of criteria); `block-d-final-gate-recheck.md` §12 names a pack-local vocabulary glossary as an **authoring** deliverable. The 6-axis "Discovery fit criteria" rating table is **DEPRECATED** (F-01; `decision-criteria.md` §2.3, §2.4). |
| `question-bank.md` | **SPLIT + REWRITE** | Into `question-bank.md` (Discovery, neutral, derived from the `Discovery evidence` field of all 116 `DC-D` criteria and the twelve areas' *"technology-neutral Discovery signals"* bullets) and `options-checks.md` (Options-phase verification). Quality-gate blocks re-homed per §6.4. Basis: `decision-criteria.md` §4 field model + §10; `platform-suitability.md` §9; `performance-scale.md` §13; `licensing-cost.md` §12; `operations-support.md` §11; F-05. |
| `decision-tree.md` | **REWRITE** | Becomes the **ordered evaluation procedure** (matrix §5 Steps 0–8 + Step 7a), not a scored branch tree. Keeps the filename because `lens-technology`, `solution-architect` and `aisa-simulate` reference it by name and `pack.yaml.decision_tree.source` declares it. Basis: F-01…F-04; matrix §5; `decision-criteria.md` §2.4, §6.2. |

### 3.2 Decision model (new layer, class B)

New directory `decision-model/`. Rationale: `decision-tree.md` must stay a readable procedure; the registers it runs against are large, separately versioned and separately volatile.

| Artifact | Verdict | Purpose | Canonical sources |
|---|---|---|---|
| `decision-model/criteria-register.md` | **CREATE** | The 116 criteria as pack rows: id, domain, states, exit class, flags `B`/`B*`/`G`/`V`, elicitation signal, decision impact, related `AP-D`/`ALT`. Not a copy of the research prose — the operational subset. | `decision-criteria.md` §3.1, §4 |
| `decision-model/exit-classes.md` | **CREATE** | `Xp`/`Xr`/`Xe`/`Xc` and the non-exits `Ri`/`Cf`/`—`, with the class → outcome mapping. Prevents the V1 defect where an in-platform redirect rendered as an exclusion. | `decision-criteria.md` §2.5; matrix §1 |
| `decision-model/outcome-classes.md` | **CREATE** | The closed 14-class terminal set with its render templates, including class 13's two non-mergeable forms and the `COMPARATOR EVIDENCE ABSENT` marker. Closure is testable: any label not here is a defect in the emitter. | `decision-criteria.md` §6.1–§6.4 |
| `decision-model/blocking-set.md` | **CREATE** | The 28 `B` criteria + the 3 `B*` scopes, each with its closing evidence task, owner and the outcome each resolution would produce. Drives SU `Unknown` rows with `custo`/`swing`. | `decision-criteria.md` §5.2, §5.3; kernel `states.md` question economics |
| `decision-model/composed-disqualifiers.md` | **CREATE** | The 12 registered rows with criteria, consequence, class and reachable outcome. Step 4 of the evaluation order has nothing to run without it. | matrix §3; `anti-patterns.md` `AP-D-059` |
| `decision-model/alternatives-register.md` | **CREATE** | `ALT-001…011`, the trigger-to-class map as **candidate generation**, the symmetry rule and the five forbidden universals as prohibited output. | `alternatives.md` §2.2, §4, §5.1, §5.3, §6 |
| `decision-model/anti-pattern-register.md` | **CREATE** | `AP-D-001…068` with `GATE` (3) / `CONSTRAINT` (4) / `ANTI-PATTERN` (61) enforcement strength, detection signals, exceptions, and the altitude note on `AP-D-004`. | `anti-patterns.md` §4, §5, §8 |
| `decision-model/comparator-rules.md` | **CREATE** | §4A: the 28 `G` criteria with evidenced alternative-side signals, the single evidenced comparative axis (`DC-D-108`), and the default `COMPARATOR EVIDENCE ABSENT`. Step 7a. | `decision-criteria.md` §4A.1–§4A.4; `alternatives.md` §5.2, §6 |
| `decision-model/volatility-register.md` | **CREATE** | Commercial/licensing volatility, the service-limit group, dated tripwires (Feb 2026 pipeline-target conversion; Feb 2027 managed-environment licence enforcement; 1 Nov 2026 AI credits), and the revalidation trigger for each. Feeds `/decide` tripwires and kernel half-lives. | `decision-criteria.md` §7.1, §7.2; matrix §4; `governance.md` §10; `alm-devops.md` §10; `licensing-cost.md` §14.4 |
| `decision-model/validation-levels.md` | **CREATE** | V1 limits · V2 bounded pilot · V3 pro-code harness · V4 managed-test fidelity, and which commitment requires which. Step 8 of the evaluation order. | `anti-patterns.md` `AP-D-048`, `AP-D-051`, `AP-D-052`; `decision-criteria.md` §10; `alm-devops.md` §14.3 |

### 3.3 Discovery layer (class A)

| Artifact | Verdict | Why |
|---|---|---|
| `discovery-signals.md` | **CREATE** | The pack's technology-neutral signal catalogue, per lens, each signal traced to the `DC-D` criteria it feeds. It is the join between the decision model and `pack.yaml.lenses_config.*.extra_signals`, and the artefact gate G2 polices. Basis: the twelve areas' *"technology-neutral Discovery signals"* bullets + `decision-criteria.md` §4 `Discovery evidence` fields + `integration-architecture.md` §13.2, `security.md` §10, `governance.md` §10, `performance-scale.md` §13, `licensing-cost.md` §12, `operations-support.md` §11. |
| `discovery-vocabulary.md` | **CREATE** (from the `glossary.md` split) | Neutral vocabulary Discovery participants and lenses share: criticality classes, identity tiers, freshness classes, ownership vocabulary, operational maturity classes, validation levels. Basis: `operations-support.md` §1.1; `decision-criteria.md` `DC-D-001`, `DC-D-009`, `DC-D-021`; `data-architecture.md` §4.11 (ownership/quality vocabulary). |
| `question-bank.md` | **REWRITE** | See §3.1. |
| `options-glossary.md` | **CREATE** (from the split) | Vendor vocabulary, explicitly Options-gated. |

### 3.4 Domain knowledge (class C) — see §7 for the full taxonomy

| Artifact | Verdict | Why |
|---|---|---|
| `domain-knowledge/delegation-matrix.md` | **UPDATE + MERGE** into `domain-knowledge/data/query-and-delegation.md` | Corpus separates *delegation-safe* (correctness, `PF-01`) from *fast* (latency) and the current file conflates them. Add `DA-02` truncation, `PS-13`, SharePoint `DA-39`/`DA-40`, SQL connector `DA-32`. |
| `domain-knowledge/dataverse-reference.md` | **REWRITE** → `domain-knowledge/data/dataverse.md` | Keep the useful schema craft; re-source every limit to `DA-*`/`DV:*`; remove any figure the corpus does not publish; add ownership immutability (`DA-12`), capacity borrowing (`DA-04`), audit/LTR (`DA-17`, `DA-18`), virtual-table forfeits (`DA-45`, `VT-06`, `VT-09`). |
| `domain-knowledge/sharepoint-reference.md` | **REWRITE** → `domain-knowledge/data/sharepoint.md` | Same treatment; the canonical figures are `5,000` LVT, `30M` items, 12 joins, 8,000 bytes, 600 calls/min (`DA-39`, `DA-40`, §13 summary). Add the "start on SharePoint, move later" corrected boundary (`DA-44`). |
| `domain-knowledge/azure-sql-reference.md` | **SPLIT** → `domain-knowledge/data/azure-sql.md` (research-backed store facts) + `domain-knowledge/craft/sql-delivery-conventions.md` (medallion, SP wrapper, DAG, temporal, CTE, MERGE — team convention) | The store-choice evidence is canonical (`data-architecture.md` §4.3, §4.9, `SQ2-05`, `SQ2-07`); the build conventions are craft with no research basis and must be labelled as such rather than read as platform truth. |
| `domain-knowledge/powerfx-patterns.md` | **KEEP + UPDATE** → `domain-knowledge/craft/powerfx.md` | High-value craft (F-09). Update only where it asserts a platform boundary; provenance class `CRAFT`. |
| `domain-knowledge/flows-patterns.md` | **SPLIT** → `domain-knowledge/automation/automation-engineering.md` (limits, metering, idempotency, retry, HITL, RPA — `AT2-*`) + `domain-knowledge/craft/flow-craft.md` (templates, expressions, adaptive cards) | The corpus has substantial, decision-bearing automation evidence the current file lacks (three independent meters `AT2-02`; 500 actions / 8 nesting / 30-day run `AT2-01`, `AT2-06`, `AT2-13`; retry duplicates non-idempotent effects `AT2-16`; the nine corrected myths in `automation-architecture.md` §14). |
| `domain-knowledge/security-patterns.md` | **SPLIT** → `domain-knowledge/security/security-engineering.md` (five enforcement planes, `SEC-*`) + `domain-knowledge/craft/security-craft.md` (role inference, permission matrices, Power Fx blocks) | `security.md` §1 organises security by **plane**; the current file organises by artefact. The plane determines which lever moves (`security.md` §10). Irreversible decisions (`SEC-09` ownership type, publisher, region, D365 apps) must reach Discovery. |
| `domain-knowledge/screen-patterns.md` | **KEEP** → `domain-knowledge/craft/screen-patterns.md` | Craft; `aisa-blueprint` and the design brief depend on it. |
| `domain-knowledge/screen-consolidation-rules.md` | **KEEP** → `domain-knowledge/craft/screen-consolidation-rules.md` | Named contract of `blueprint-contract.md` ("screen catalogues, naming conventions and hard caps come from the pack"). Rename only with the consumer update in §12 Q-05. |
| `domain-knowledge/excel-patterns.md` | **KEEP** → `domain-knowledge/craft/excel-translation.md` | Craft; consumed by `/capture` and Options translation work. |
| `domain-knowledge/anonymization.md` | **KEEP** → `domain-knowledge/craft/anonymization.md` | Craft, entirely outside corpus scope. Label, do not source. |
| `domain-knowledge/estimation-model.md` | **UPDATE + partial DEPRECATE** → `domain-knowledge/craft/estimation-model.md` | Method kept as craft. `§ LICENSE COST ESTIMATES` **deprecated** (F-07, `licensing-cost.md` §12: never quote a price; carry units, ratios, drivers and route figures to the Licensing Guide and the customer's agreement). |
| `domain-knowledge/delivery-conventions.md` | **UPDATE** → `domain-knowledge/alm/delivery-conventions.md` | Add the ALM ladder rungs and entry conditions (`alm-devops.md` §1, §10), `ALM-18` (no rollback), the two dated tripwires, and the deprecation pair (ALM Accelerator, CoE Starter Kit — `GOV-12`). |
| new class-C files | **CREATE** | `application-surfaces.md`, `data/store-selection.md`, `integration/integration-engineering.md`, `architecture/patterns.md`, `governance/preconditions.md`, `alm/alm-engineering.md`, `performance/performance-and-scale.md`, `cost/licensing-economics.md`, `operations/operations-and-support.md` — see §7. |

### 3.5 Architecture templates

| Artifact | Verdict | Why |
|---|---|---|
| `architecture-templates/sharepoint-first.md` | **REWRITE** → `collaboration-surface.md` | The corpus's own framing is that this is the **documented answer** for four named shapes (`ALT-003`, outcome class 13 form (a), `AP-D-008` Exceptions), not the "cheap branch". The template must carry the mandatory graduation trigger (one-way upgrade — `AA-50`). |
| `architecture-templates/dataverse-first.md` | **REWRITE** → `dataverse-application.md` | Keep the shape; re-source; add the irreversible-decision block (ownership type, publisher, region, D365 apps) and the managed-environment / licence chain. |
| `architecture-templates/hybrid.md` | **SPLIT** | The corpus has two structurally different hybrids: outcome class 3 (`ALT-009`, cloud-native, gated on an operator — `AP-D-026`) and class 4 (`ALT-007`, enterprise system keeps authority, carries `INCUMBENT FIT UNEVALUATED`). One template cannot carry both. |
| new templates | **CREATE** | `model-driven-application.md`, `canvas-application.md`, `external-audience-site.md`, `hybrid-cloud-native.md`, `hybrid-enterprise-boundary.md`, `non-technology-intervention.md` (classes 10/11), `candidate-set.md` (class 8 render, `COMPARATOR EVIDENCE ABSENT`). Basis: `application-architecture.md` §1, §10; `architecture-patterns.md` `AP-01…AP-10`, §3.2; `decision-criteria.md` §6.2; `alternatives.md` §4. |

Every architecture template must be reachable from an outcome class, and every outcome class that names an architecture must have a template. Gate G5 checks both directions.

### 3.6 Deliverable templates

| Artifact | Verdict | Why |
|---|---|---|
| `discovery-report.template.md` | **UPDATE** | Add `open_blocking_criteria` (the `B` criteria still `UNKNOWN`) as a required slot. Basis: `decision-criteria.md` §5.1 — `DECISION BLOCKED` is a legitimate, fundable output. Neutrality: this deliverable stays technology-neutral (gate G2 scope). |
| `executive-report.template.md` | **UPDATE** | Add `outcome_class` (one of the closed 14, verbatim), `scope_outcome_pairs` (one outcome per **scope**, never collapsed — `decision-criteria.md` §6.4), `comparator_status`, and promote `revision_tripwires` to required where the volatility register fires. |
| `solution-blueprint.template.md` | **UPDATE** | Add `validation_level_required` (V1–V4), `accepted_unknowns`, `volatile_facts_with_dates`. Basis: `AP-D-052`, `decision-criteria.md` §7. |
| `implementation-spec.template.md` | **UPDATE** | Add `irreversible_decisions` (ownership type, publisher, region, D365 apps, residency), `idempotency_keys`, `failure_semantics`, `reconciliation_owner`. Basis: `security.md` §10; `DC-D-052`, `DC-D-054`; `NB-01`. |
| `claude-design-brief.template.md` | **UPDATE** | Re-point the domain-knowledge cross-reference table at the new taxonomy paths; keep the inline-citation convention (it is already a provenance mechanism and generalises into §8). |
| `estimate.template.md` | **UPDATE** | Add `cost_drivers` and `entitlement_exposure` slots; forbid absolute prices in the template's own guidance. Basis: `licensing-cost.md` §12; `AP-D-060`, `AP-D-062`, `AP-D-064`. |

### 3.7 Cross-cutting new artifacts

| Artifact | Verdict | Purpose |
|---|---|---|
| `PROVENANCE.md` | **CREATE** | The pack-local statement of the traceability convention (§8): id grammar, provenance classes, volatility stamping, semantic markers. Authored **before** any content file. |
| `neutrality-denylist.md` | **CREATE** | The machine-checkable vendor/product term list plus the Discovery-visible file list, consumed by gate G2. |
| `CHANGELOG.md` | **CREATE** | Pack-level change log keyed to `pack_version`; each entry names the canonical ids that moved. `docs/PACK_AUTHORING.md` requires a version bump per change but the pack has no log. |

---

## 4. Evidence → artifact mapping

Canonical ids only; no research prose is copied.

### 4.1 Discovery layer

| Pack artifact | Canonical evidence | Notes |
|---|---|---|
| `discovery-signals.md` — business | `DC-D-001…008`; `PS-04`, `PS-41`; `LC-28`; `platform-suitability.md` §9 | `DC-D-001` criticality is the highest-leverage signal in the corpus; four states, never a tier label |
| `discovery-signals.md` — user | `DC-D-009…020`, `DC-D-116`; `application-architecture.md` §10 | Identity tier, device mix, offline depth/surface, a11y regime, language + RTL, deep-link inventory |
| `discovery-signals.md` — operations | `DC-D-048…057`, `DC-D-100…104`; `automation-architecture.md` §14; `operations-support.md` §11 | Four automation shapes; who notices / who acts / with what evidence / what they bought |
| `discovery-signals.md` — data | `DC-D-021…034`; `data-architecture.md` §11; `SC-14`, `SC-21`, `SY-18`, `DQ-*` | Per **entity**, not per solution; peak (not average) business-event volume |
| `discovery-signals.md` — governance | `DC-D-069…075`; `governance.md` §10 | Governance findings are mostly **tenant preconditions**, not solution decisions |
| `discovery-signals.md` — financial | `DC-D-092…099`; `licensing-cost.md` §12 | Signals that must not be collapsed: users vs (user, app) pairs; data vs audit volume; unique people vs billable visitors |
| `discovery-signals.md` — cross-cutting absolutes | `DC-D-108`, `DC-D-033`, `DC-D-059`, `DC-D-062`, `DC-D-028`, `DC-D-057` | Step 0 of the evaluation order. Neutral by construction and therefore Discovery-legal (§6 rule N-06) |
| `question-bank.md` | the `Discovery evidence` field of all 116 `DC-D` criteria | One question per elicitable signal; near-duplicate clusters collapsed per `decision-criteria.md` §3.2 |
| `discovery-vocabulary.md` | `DC-D-001` states; `operations-support.md` §1.1 maturity classes; `DC-D-009` identity tiers; `data-architecture.md` §4.11 ownership/quality vocabulary; validation levels V1–V4 | Shared language, zero product nouns |
| `question-bank.md` — Unknown pricing | kernel `states.md` question economics + `decision-criteria.md` §5.2 | Every `B` criterion is `swing: decisivo` by construction |

### 4.2 Options / decision layer

| Pack artifact | Canonical evidence |
|---|---|
| `decision-tree.md` (ordered procedure) | matrix §5 Steps 0–8 + Step 7a; `decision-criteria.md` §10 (order is not commutative) |
| `decision-model/criteria-register.md` | `decision-criteria.md` §3.1 register, §4 bodies |
| `decision-model/exit-classes.md` | `decision-criteria.md` §2.5; matrix §1 |
| `decision-model/outcome-classes.md` | `decision-criteria.md` §6.2 (14 classes), §6.1 governing rule, §6.4 scope-pairs rule |
| `decision-model/blocking-set.md` | `decision-criteria.md` §5.2 (28) + `B*` (`DC-D-113`, `115`, `116`) |
| `decision-model/composed-disqualifiers.md` | matrix §3 rows 1–12; `AP-D-059` |
| `decision-model/alternatives-register.md` | `alternatives.md` §4 (`ALT-001…011`), §5.1 trigger map, §2.2 forbidden universals |
| `decision-model/anti-pattern-register.md` | `anti-patterns.md` §4 register, §5 entries, §8 (GATE/CONSTRAINT strength; `AP-D-004` altitude) |
| `decision-model/comparator-rules.md` | `decision-criteria.md` §4A; `alternatives.md` §5.2, §5.3, §6 |
| `decision-model/volatility-register.md` | `decision-criteria.md` §7.1, §7.2; matrix §4; `LC-09`, `LC-15`, `LC-19`; `GOV-11`; `ALM-10` |
| `decision-model/validation-levels.md` | `AP-D-048`, `AP-D-051`, `AP-D-052`; `NB-07`; `alm-devops.md` §14.3 |
| `pack.yaml` `technology.constraints_to_check` | the 12 `DC-D` domains; the existing five keys re-derived and extended (network boundary `DC-D-044`, residency `DC-D-033`, deployment model `DC-D-108`, entitlement fit `DC-D-093`, observability `DC-D-101`, reversibility `DC-D-080`, operator availability `DC-D-070`/`073`/`110`) |
| architecture templates | `architecture-patterns.md` `AP-01…AP-10`, §3.2 escalation ladder, §5 selection matrix; `application-architecture.md` §1; `alternatives.md` §4 |

### 4.3 Implementation layer

| Pack artifact | Canonical evidence |
|---|---|
| `application/application-surfaces.md` | `application-architecture.md` §1, §3.1–§3.7, §4, §10; `platform-suitability.md` §2 rows 1–19 |
| `data/store-selection.md` | `data-architecture.md` §2 store fit matrix, §3 decision boundaries, §6 |
| `data/dataverse.md` | `data-architecture.md` §4.2, §4.7; `DV:*`; `VT:*` |
| `data/sharepoint.md` | `data-architecture.md` §4.4; `SP:S-*`; `DA-39`, `DA-40`, `DA-44` |
| `data/azure-sql.md` | `data-architecture.md` §4.3, §4.9; `SQ:*`, `SQ2:*` |
| `data/query-and-delegation.md` | `DA-02`; `PS-13`; `PF-01`; `performance-scale.md` §5.4; `AP-D-050` |
| `automation/automation-engineering.md` | `automation-architecture.md` §2, §5.1–§5.15, §7, §8; `AT2-*` |
| `integration/integration-engineering.md` | `integration-architecture.md` §3, §4, §5, §8, §12; `IA-*` |
| `architecture/patterns.md` | `architecture-patterns.md` §4 catalogue, §5, §6, §7 (`Y-01…Y-14`) |
| `security/security-engineering.md` | `security.md` §1–§3.6, §4, §5, §12; `SEC-XB-01…04` |
| `governance/preconditions.md` | `governance.md` §1–§3.6, §4, §5, §12; `GOV-XB-01…04` |
| `alm/alm-engineering.md` | `alm-devops.md` §1–§3.4, §4, §5, §12, §14 |
| `performance/performance-and-scale.md` | `performance-scale.md` §1–§5.7, §6, §8; `NB-04`, `NB-07` |
| `cost/licensing-economics.md` | `licensing-cost.md` §1–§2.6, §3, §5, §7 (units, drivers, ratios — never prices) |
| `operations/operations-and-support.md` | `operations-support.md` §1–§2.6, §3, §5, §6 |

### 4.4 Deliverable composition layer

| Pack artifact | Canonical evidence |
|---|---|
| `executive-report` outcome slots | `decision-criteria.md` §6.2 render templates; §6.4 scope-pairs |
| `discovery-report` blocking slot | `decision-criteria.md` §5.1, §5.2 |
| `solution-blueprint` validation slot | `validation-levels.md` ← `AP-D-052` |
| `implementation-spec` irreversibility slot | `security.md` §10; `alm-devops.md` §10; `DC-D-033`, `DC-D-044` |
| `estimate` cost slots | `licensing-cost.md` §2.3 cost drivers, §2.5 TCO, §12 |
| synthesis mapping (`architecture-story`, `risks-and-assumptions`) | `anti-patterns.md` `Consequences` → Risky rows; `alternatives.md` `*Consequences` → trade-offs; `decision-criteria.md` §10 |

---

## 5. Knowledge classification (A/B/C/D)

**Class definitions** as given in the brief: **A** Discovery (pre-Options, technology-neutral) · **B** Options/decision (Power Platform-specific allowed) · **C** Implementation engineering · **D** Deliverable composition.

### 5.1 Classification by canonical source

| Canonical source | A | B | C | D | Why more than one class (where applicable) |
|---|:-:|:-:|:-:|:-:|---|
| `platform-suitability.md` §9 signal list | ✔ | | | | Written by the corpus as technology-neutral signals |
| `platform-suitability.md` §1, §2, §3 fit matrix and boundaries | | ✔ | ✔ | | The **fit verdict** is B; the **boundary mechanics** (why the limit exists) are C for the build team |
| `application-architecture.md` §1, §2 | | ✔ | ✔ | | Surface selection is B; surface construction limits are C |
| `application-architecture.md` §10 signal list | ✔ | | | | |
| `data-architecture.md` §2, §3 | | ✔ | ✔ | | Store selection is B; store engineering is C |
| `data-architecture.md` §11 signal list, §4.11 vocabulary | ✔ | | | | Ownership and quality vocabulary is neutral and must be shared with the business |
| `automation-architecture.md` §2 shape test | ✔ | ✔ | | | The **four-shape classification** is neutral and belongs in Discovery; the shape → product mapping is B |
| `automation-architecture.md` §5, §7, §8; `AT2-*` limits | | ✔ | ✔ | | Limits exclude designs (B) and constrain implementations (C) |
| `integration-architecture.md` §9 (28 variables), §13.2 signals | ✔ | ✔ | | | §13.2 states the signals are elicitable **without naming a vendor**; the same variables drive the B topology test |
| `integration-architecture.md` §5, §12 | | ✔ | ✔ | | |
| `security.md` §10 plane-named signals | ✔ | | | | The **plane** names a requirement, not a product |
| `security.md` §1–§4, `SEC-*` | | ✔ | ✔ | | Irreversible items (`SEC-09`) additionally force an A-side question in Discovery |
| `governance.md` §10 signals | ✔ | | | | |
| `governance.md` §1–§5 preconditions | | ✔ | ✔ | ✔ | Preconditions are B gates, C setup work, and D deliverable line-items with an owner and a cost |
| `alm-devops.md` §10 signals | ✔ | | | | Team size, change velocity, reversibility, compliance evidence — all neutral |
| `alm-devops.md` §1 ladder, §3, §5 | | ✔ | ✔ | | Rung selection B; rung construction C |
| `performance-scale.md` §13 signals | ✔ | | | | |
| `performance-scale.md` §2–§6, §8 | | ✔ | ✔ | | Limits exclude (B); envelopes size the build (C) |
| `licensing-cost.md` §12 signals | ✔ | | | | Population, frequency, capability count, growth — neutral cost drivers |
| `licensing-cost.md` §2, §3, §5, §6 | | ✔ | | ✔ | Economics decide (B) and populate the estimate and executive report (D) |
| `operations-support.md` §11 signals, §0 central question | ✔ | | | | *"Who will notice, who will act, with what evidence, and what have they bought"* — four neutral questions |
| `operations-support.md` §2, §3, §5, §6 | | ✔ | ✔ | ✔ | Operating model is a B gate, a C runbook, and a D deliverable commitment |
| `architecture-patterns.md` §4, §5 | | ✔ | ✔ | | Pattern shortlist is B; pattern construction is C |
| `architecture-patterns.md` §7 (`Y-*`) | | ✔ | | | Pattern-**selection** anti-patterns, distinct from `integration-architecture.md`'s `X-*` implementation anti-patterns — the two sets must not be merged (`architecture-patterns.md` §11.2) |
| `decision-criteria.md` §4 `Discovery evidence` fields | ✔ | | | | The single richest A-class source in the corpus |
| `decision-criteria.md` §2.5, §5, §6, §7, §4A | | ✔ | | ✔ | Outcome classes are B logic and D render strings; §6.2's templates are literally deliverable text |
| `anti-patterns.md` `Detection Signals` fields | ✔ | | | | Neutral by construction wherever the evidence allowed; each entry says so when it could not be |
| `anti-patterns.md` entries (`GATE`/`CONSTRAINT`) | | ✔ | ✔ | | GATE makes an option unavailable (B); each entry's `Better alternatives` is build guidance (C) |
| `alternatives.md` §4, §5.1 | | ✔ | | ✔ | Candidate generation B; the class-8 render string D |
| `alternatives.md` §2.2 forbidden universals | | ✔ | | ✔ | Prohibited **output** — enforced at the deliverable boundary, which is where the caveats were being lost |
| `decision-intelligence-matrix.md` §3, §5 | | ✔ | | | The composed rows and the order are pure B |
| `decision-intelligence-matrix.md` §6 (T-01…T-18) | | ✔ | | | Not pack content — the **regression suite** for gate G5 |

### 5.2 The three multi-class patterns, stated once

1. **Signal → limit → build rule.** One finding can be an A signal (*"largest queried table row count at year 3"*), a B exclusion (*"non-delegable access path over a growing dataset excludes this design"*), and a C build rule (*"page size, index, and the delegation-safe operator set"*). The A form must never carry the number; the B form carries the boundary **shape**; only the C form carries a figure, stamped and dated.
2. **Precondition → gate → deliverable line-item.** Governance and operations findings are preconditions (B gate), setup work (C), and a costed, owned item in the estimate and executive report (D). Dropping the D leg is how an unfunded mandated control becomes a surprise (`AP-D-064`, outcome class 7).
3. **Outcome class → render string.** `decision-criteria.md` §6.2 is simultaneously the decision terminal set (B) and the exact sentence that lands in `decisions.md` and the executive report (D). It is deliberately authored once and consumed twice, because the corpus's own recorded failure is that the caveats survived every internal step and were discarded at the writing boundary (matrix §5 Step 7a).

---

## 6. Discovery neutrality boundaries

### 6.1 The principle

> Discovery elicits the **requirement**, the **current state** and the **constraint**. It never elicits the mechanism.
> Test: *could a competent architect answer this question unchanged for a custom build, another low-code platform, or "no new technology"?* If not, it is Options.

Basis: `.claude/rules/no-tech-mention-before-options.md`; `decision-criteria.md` §2.2; `anti-patterns.md` §8 (*"detection signals are technology-neutral by construction wherever the underlying evidence allowed it, so they are usable in a Discovery phase that forbids naming vendors and products"*); `integration-architecture.md` §13.2 (its 16 signals are explicitly stated as satisfying the repo rule).

### 6.2 Contamination inventory — canonical material that must NOT reach Discovery

Systematic pass over the corpus's decision-bearing vendor facts. Left column: the fact. Right column: what Discovery asks instead. The fact still reaches the engagement — in Options, through the criteria register.

| Vendor-bound canonical fact | Canonical ids | Discovery must ask instead |
|---|---|---|
| Dataverse delegation truncation, 500/2,000 | `DA-02`, `PS-13` | Expected rows and growth **per queried table** at year 3; query shape (filters, negations, sorts, free-text, aggregates) |
| Aggregate/chart 50k ceiling; no published row ceiling | `DA-03`, `SC-18` | Reporting scope: per-user/time-boxed vs org-wide/historical; must reports respect record security |
| SharePoint LVT 5,000 / 30M items / 12 joins | `DA-39`, `DA-40` | Where structured records live today; how many; relationship count and cascade expectations |
| Dataverse security model (BU, teams, FLS), no numeric curve | `SEC-*`, `NB-04`, `PF-U-07` | Data-access granularity (row/column), who may see which records and columns, read-audit obligation, separation of duties |
| Premium connector / entitlement chain | `LC-04`, `LC-10`, `DC-D-093` | Which systems must be reached; user population; interaction frequency; distinct capabilities per user; existing licence baseline (current state, allowed) |
| Managed Environments ↔ premium for all active users | `PS-33`, `DA-55`, `GOV-11` | Enforced-control requirement; telemetry requirement; criticality class; who funds the control |
| Power Pages / external identity / billable visitors | `PS-36`, `PS-56`, `LC-20` | Audience identity tier: employee / known partner / authenticated customer / anonymous; population predictability |
| Offline never in browser; offline vs FLS mutual exclusion | `AA-42`…`AA-44`, `PS-35` | Connectivity pattern, device class, offline **depth** and **surface**, what must be doable disconnected |
| Flow limits: 500 actions, 8 nesting, 30-day run, 120 s sync | `AT2-01`, `AT2-06`, `AT2-12`, `AT2-13` | Longest human wait; maximum process instance duration; is there a step whose result a caller must wait for, and for how long |
| Three independent automation meters | `AT2-02`, `AT2-04` | Expected event rate; actions per event; peak shape per minute; single-identity funnels |
| No cross-connector transaction | `PS-45`, `AT2-19`, `DA-07` | Which writes must be all-or-nothing, across which systems; tolerance to temporary inconsistency; acceptable compensation window |
| Custom-connector throughput `CONFLICTED` by 20× | `NB-02`, `IA-C-01`, `DC-D-039` | Required sustained and peak throughput per stream — **elicit the requirement; never quote either figure** |
| Gateway 2 MB/8 MB; VNet constraints | `DA-34`, `integration-architecture.md` §5.6 | Is any source on-premises; is private-network execution mandated; may data transit a public cloud |
| DLP / connector classification | `GOV-*`, `DC-D-072` | Data-handling policy: where may this data travel, and who owns that policy |
| EUDB dual condition; global metadata replication | `DA-57`, `DA-58`, `DC-D-033` | Residency and sovereignty regime, verbatim from the regulation or contract clause |
| SaaS-only deployment model | `PS-47`, `DC-D-108` | **Where must the runtime execute?** (neutral, and a Step-0 absolute — see N-06) |
| No rollback; pipelines; solutions | `ALM-18`, `alm-devops.md` D-06 | Reversibility expectation; change frequency; change-window constraints; what release evidence is required |
| Mandatory release waves | `PS-50` | Tolerance to vendor-driven change; is behaviour required to be frozen per release |
| CoE Starter Kit deprecation; ALM Accelerator | `GOV-12`, `alm-devops.md` §10 | What governance tooling exists today (current state); who operates it |
| Backups ≤ 28 d; restore is a procedure | `DA-18`, `OP-14` | RPO/RTO per business flow; has a restore ever been rehearsed; who would run it |
| Dataverse 99.9% ≠ end-to-end SLA | `NB-03`, `OP-19`, `DC-D-091` | Contractual availability commitment per business flow; every dependency and its own commitment |

### 6.3 Authoring rules (normative for Step 2 onward)

- **N-01 — Requirement, not mechanism.** Every Discovery-visible question and signal passes the §6.1 test.
- **N-02 — No vendor or product nouns** in Discovery-visible artefacts. Existing systems may be named **only as current state**, and only where the criterion's own `Discovery evidence` field is estate-bound.
- **N-03 — Never ask the comparison.** No Discovery question may embed a canonical threshold (*"more than 2,000 rows?"*, *"more than 500 actions?"*). Ask the quantity; the comparison happens in Options. Violating this both leaks the platform and biases the answer.
- **N-04 — Discovery asserts no numbers.** Platform limits never appear in Discovery artefacts, not even as background. Numbers in Discovery are **elicited from the customer**, and they enter the SU with `verificado_em` and `validade`.
- **N-05 — Current-state questions are legal and bounded.** For the estate-bound criteria (`DC-D-111` platform estate, `DC-D-072` policy posture, `DC-D-093` licence baseline, `DC-D-110` team capability) the permitted form is *"what do you already have / own / license / operate"* — never *"do you need X"*.
- **N-06 — Step-0 absolutes are elicited in Discovery.** `DC-D-108`, `DC-D-033`, `DC-D-059`, `DC-D-062`, `DC-D-028`, `DC-D-057` are neutral by construction and can terminate the platform question. Deferring them to Options wastes the engagement (matrix §5: *"Steps 0–1 are cheap and can terminate the analysis"*).
- **N-07 — Two vocabularies.** `discovery-vocabulary.md` (Discovery-visible, zero product nouns) and `options-glossary.md` (Options-gated). No file serves both.
- **N-08 — Framing inherits the boundary.** `frame.md`, `business-story.md` and `as-is.md` are Discovery-visible for neutrality purposes.
- **N-09 — No exit signal in Discovery.** Exit classes, outcome classes and anti-pattern verdicts are Options artefacts. Discovery may raise a **Risky** row from a neutral detection signal, never a platform verdict.
- **N-10 — Neutrality is checked mechanically**, not by review alone (gate G2, `neutrality-denylist.md`).

### 6.4 Re-homing the existing quality gates (F-05)

| Block | Today | Target |
|---|---|---|
| `D1`–`D2`, `D4`–`D7` | Discovery question bank | **KEEP** in Discovery — data-integrity checks, already neutral |
| `D3`, `D8` | Discovery ("Power Fx, SP, Power Automate, Business Rule") | **REWRITE** neutral: *"every discovered calculation has an owner and a stated implementation intent"* — mechanism named in Options |
| `S1`–`S9` | Discovery question bank | **MOVE** to `domain-knowledge/data/*` build checklists (class C) |
| `P1`–`P10` | Discovery question bank | **MOVE** to `domain-knowledge/craft/powerfx.md` (class C) |
| `E1`–`E5`, `E7` | Discovery question bank | **KEEP** neutral in Discovery (permission-matrix completeness, least privilege) |
| `E6` | Discovery ("Audit Power Fx mandatory") | **SPLIT**: the neutral obligation (*"approve / delete / export must be auditable"*) stays in Discovery; the Power Fx implementation moves to class C |
| `M1`–`M9` | Discovery question bank | **MOVE** to `domain-knowledge/craft/estimation-model.md` (class C/D) |

All re-homed gates carry `Provenance: CRAFT` (§8) — they are engagement experience, not research findings, and must not acquire a false research basis.

---

## 7. Proposed domain-knowledge taxonomy

The existing flat 13-file structure is **not** accepted. It mixes decision logic, platform facts and craft in one namespace, has no provenance, and its store-reference files predate the corpus.

### 7.1 The separation test

A body of knowledge earns its own file when it satisfies **at least two** of:
(a) a distinct consumer (a named skill, agent or deliverable reads it and not the rest);
(b) a distinct volatility class (it decays at a different rate and revalidates on a different trigger);
(c) a distinct provenance class (`RESEARCH` vs `CRAFT` — mixing them is how craft acquires false authority);
(d) it is large enough that loading it whole would crowd the reader's working context for an unrelated task.

Pack files are organised by **consumer need**, not one-per-research-area. Two areas can merge into one file, and one area can fan out into three.

### 7.2 Target structure

```
library/packs/pp/
├── PROVENANCE.md
├── CHANGELOG.md
├── pack.yaml
├── discovery-vocabulary.md
├── options-glossary.md
├── question-bank.md
├── options-checks.md
├── discovery-signals.md
├── neutrality-denylist.md
├── decision-tree.md                      # ordered evaluation procedure (Steps 0–8 + 7a)
├── decision-model/
│   ├── criteria-register.md
│   ├── exit-classes.md
│   ├── outcome-classes.md
│   ├── blocking-set.md
│   ├── composed-disqualifiers.md
│   ├── alternatives-register.md
│   ├── anti-pattern-register.md
│   ├── comparator-rules.md
│   ├── volatility-register.md
│   └── validation-levels.md
├── architecture-templates/               # one per reachable outcome/architecture shape
└── domain-knowledge/
    ├── application/application-surfaces.md
    ├── data/store-selection.md
    ├── data/dataverse.md
    ├── data/sharepoint.md
    ├── data/azure-sql.md
    ├── data/query-and-delegation.md
    ├── automation/automation-engineering.md
    ├── integration/integration-engineering.md
    ├── architecture/patterns.md
    ├── security/security-engineering.md
    ├── governance/preconditions.md
    ├── alm/alm-engineering.md
    ├── alm/delivery-conventions.md
    ├── performance/performance-and-scale.md
    ├── cost/licensing-economics.md
    ├── operations/operations-and-support.md
    └── craft/
        ├── powerfx.md
        ├── screen-patterns.md
        ├── screen-consolidation-rules.md
        ├── excel-translation.md
        ├── flow-craft.md
        ├── security-craft.md
        ├── sql-delivery-conventions.md
        ├── anonymization.md
        └── estimation-model.md
```

### 7.3 Per-artifact justification (class C files)

| File | Purpose | Canonical sources | Downstream consumers | Why separate |
|---|---|---|---|---|
| `application/application-surfaces.md` | Which surface can carry which experience, and the documented boundary of each (canvas, model-driven, Pages, custom pages, code apps, Teams-hosted, Wrap, offline, mobile, a11y, l10n) | Area 2 §1–§3.7, §4, §9; Area 1 §2 rows 1–19 | `lens-technology`, `aisa-blueprint`, `solution-blueprint`, `claude-design-brief` | (a) blueprint is its principal consumer and reads nothing else here; (b) short half-life — modern controls, code apps and SPA sites all changed during the research window (`application-architecture.md` §9 item 6) |
| `data/store-selection.md` | Requirement → default store fit, and the boundaries that move it | Area 3 §2, §3, §6 | `lens-technology`, `solution-architect`, `decision-tree` | (a) the only data file the decision procedure reads; (d) keeps the selection logic out of three engineering files |
| `data/dataverse.md` | Dataverse engineering: modelling, ownership immutability, keys, audit/LTR, capacity, virtual tables | Area 3 §4.2, §4.7; `DV:*`, `VT:*` | `implementation-spec`, design brief, `lens-technology` | (a)(d) largest single store body; distinct from selection |
| `data/sharepoint.md` | SharePoint/Lists/Excel engineering and its documented ceilings and absences (no RLS, no CLS) | Area 3 §4.4; `SP:S-*` | idem | (a)(c) also the home of outcome class 13's four documented shapes |
| `data/azure-sql.md` | Azure SQL as a store: tiers, log-rate ceiling, connector envelope, cold-storage absence | Area 3 §4.3, §4.9; `SQ2:*` | idem | (c) separates research-backed store facts from the team's SQL build conventions |
| `data/query-and-delegation.md` | Delegation-safe (correctness) vs fast (latency) — the corpus's most-collapsed distinction | `DA-02`, `PS-13`, `PF-01`, Area 9 §5.4, `AP-D-050` | `lens-technology`, `aisa-simulate`, design brief, `craft/powerfx.md` | (a) the most frequently consulted rule set at build time; (b) explicitly warned against collapsing (`performance-scale.md` §13) |
| `automation/automation-engineering.md` | Four shapes, three meters, limits, idempotency, retry, ordering, HITL, RPA, the nine corrected myths | Area 4 §2, §5, §7, §8 | `lens-technology`, `implementation-spec` | (a)(d); the myth corrections are content the pack must actively teach (`automation-architecture.md` §14) |
| `integration/integration-engineering.md` | Mechanism envelope, topology test, network boundary, sync risk register, when the platform is not the integration layer | Area 5 §3, §4, §5, §8, §12 | `lens-technology`, `solution-architect`, `implementation-spec` | (a)(d); §12's nine conditions are a principal source of non-PP options |
| `architecture/patterns.md` | `AP-01…AP-10` with strengths, weaknesses, risks, escalation ladder, and the `Y-*` selection anti-patterns | Area 12 §3.2, §4, §5, §6, §7 | `solution-architect`, architecture templates | (a) the templates are generated from it; (c) heavy `INF` content requiring the lineage marker |
| `security/security-engineering.md` | Five enforcement planes; irreversible decisions; partial-by-design controls; licence dependencies outside the platform | Area 6 §1–§4, §12, §14 | `compliance-officer`, `lens-technology`, `implementation-spec` | (a)(c); `security.md` §10 requires forcing an explicit residual-risk statement rather than a binary "control in place" |
| `governance/preconditions.md` | Tenant preconditions vs solution decisions; environment/DLP/managed-environment levers; dated commitments | Area 7 §1–§5, §12, §14 | `compliance-officer`, `estimate` (unfunded preconditions are costs) | (b) two dated tripwires; (a) governance is the only area whose findings are mostly **not** design choices |
| `alm/alm-engineering.md` | The ALM ladder with entry conditions and prices; `ALM-18` no rollback; pipelines; environment variables and connection references | Area 8 §1–§3, §5, §14 | `implementation-spec`, `delivery-conventions` | (b) fast-moving (`alm-devops.md` §9 lists eight items expected to churn) |
| `alm/delivery-conventions.md` | The team's naming, stamping, environment and go-live conventions | existing pack file + Area 8 | `lens-technology`, `implementation-spec` | (c) `CRAFT` provenance, but sits next to the research it must stay consistent with |
| `performance/performance-and-scale.md` | Meter map, scale envelopes per layer, the limit-vs-measurement rule, validation levels | Area 9 §2–§5, §6, §8; `NB-07` | `solution-architect`, `aisa-simulate`, `solution-blueprint` | (a)(c) the single place `AP-D-051` is enforced at build altitude |
| `cost/licensing-economics.md` | Billing **units**, cost **drivers**, cost **ratios**, TCO structure, licence-avoidance trap. **No prices.** | Area 10 §1–§2.6, §3, §5, §7 | `cfo-lens`, `estimate`, `executive-report` | (b) the most volatile body in the corpus; (c) the file where the no-price rule is enforced |
| `operations/operations-and-support.md` | Who notices / who acts / with what evidence / what they bought; monitoring limits; backup vs recovery; support boundaries | Area 11 §1–§2.6, §3, §5, §6 | `operations-lead`, `implementation-spec`, `executive-report` | (a)(c); the operating-model question is a decision input, not a post-deployment concern |
| `craft/*` (9 files) | Engagement-proven practice the corpus never evaluated: Power Fx, screens, consolidation, Excel translation, flow craft, security craft, SQL conventions, anonymisation, estimation | none — `Provenance: CRAFT` | `aisa-blueprint`, design brief, `aisa-simulate`, `estimate` | (c) is decisive: keeping craft in its own namespace is what stops it being read as research, and stops research being diluted into style guidance |

### 7.4 What deliberately does **not** get its own file

- **Copilot / agent surfaces.** `DC-D-116` and `AP-D-068` exist, but `alternatives.md` §5.1 records *"none evaluable — `UNKNOWN` in every class"* and the correct output is `DECISION BLOCKED`. A pack file would be an invitation to invent. It is one criterion row plus one anti-pattern row until research exists (§12 Q-06).
- **Power BI.** Present only as constraints inside Areas 2 and 3 (`AA-51`, `DA-22`); folded into `application-surfaces.md` and `data/store-selection.md`.
- **Accessibility/UX as a research file.** Area 2 carries the a11y and l10n boundaries; the practice lives in `craft/screen-patterns.md`. Two files, no third.
- **"Architecture selection" as domain knowledge.** It is class B and lives in `decision-tree.md` + `decision-model/`, not in `domain-knowledge/`. Putting selection logic in domain knowledge is how the current pack ended up with thresholds in a reference file.

---

## 8. Traceability convention

Lightweight, greppable, no ledger. One line per authored rule; no separate database; no per-claim identifiers of our own.

### 8.1 The reference line

Placed immediately after the rule, table or section it justifies:

```
> Research basis: DC-D-039, AP-D-051 · NB-02 · CONFLICTED — do not encode a figure
```

Grammar:

1. Literal prefix `Research basis:`.
2. Canonical ids, comma-separated, **most specific first**: Block D (`DC-D-NNN`, `AP-D-NNN`, `ALT-NNN`) → Area ids (`PS-NN`, `AA-NN`, `DA-NN`, `AT2-NN`, `IA-NN`, `SEC-*`, `GOV-*`, `ALM-NN`, `PF-NN`, `LC-NN`, `OP-NN`, `APR-*`) → reservations (`NB-0N`).
3. Optional ` · ` separated semantic markers, taken **verbatim** from the canonical vocabulary: `UNKNOWN` · `CONFLICTED` · `VOLATILE` · `INF` · `T3` / `T4` · `MS-V` · `COMPARATOR EVIDENCE ABSENT` · `NUMBER ABSENT` · `DECISION BLOCKING`.
4. Optional short imperative after an em dash, where the marker implies an action (*"do not encode a figure"*, *"measure before commitment"*).

### 8.2 Disambiguation rule (mandatory)

Area-local ids are overloaded across the corpus and **must be file-qualified** when cited: `AP-NN` (Areas 1, 2, 12), `DC-NN` (Areas 9, 10, 11), `D-NN` (Area 8), `C-01` (Area 5), `S-NN` (Area 6), `G-NN` (Area 7).

```
Research basis: architecture-patterns.md AP-05, licensing-cost.md DC-10
```

Block D ids (`DC-D-*`, `AP-D-*`, `ALT-*`) are globally unique and are **never** qualified. Prefer them: `decision-criteria.md` §8 already maps the file-local criteria into the canonical namespace.

### 8.3 Provenance class (mandatory in every file's frontmatter)

```yaml
provenance: RESEARCH | CRAFT | MIXED
```

- `RESEARCH` — every material rule carries a `Research basis:` line. Gate G1 enforces resolution; gate G3 enforces presence.
- `CRAFT` — engagement practice with no research basis. The file header states it in one sentence. It may **not** state a platform limit, a threshold or a comparative claim; where it needs one, it cites the `RESEARCH` file that owns it.
- `MIXED` — permitted only where a `CRAFT` section is explicitly delimited inside a `RESEARCH` file, and the section header says so.

### 8.4 Volatility stamping

Any rule resting on a platform value, limit, entitlement, feature state or commercial term carries the kernel's own epistemic columns, so pack rules decay exactly like Shared Understanding rows:

```
> Research basis: LC-09 · VOLATILE · verificado_em: 2026-09-03 · validade: plataforma-tecnica
> Revalidation trigger: contract renewal · PPR reporting reaching GA
```

`validade` classes come from `library/kernel/states.md`; `pack.yaml.epistemics.half_lives_override` declares the pack's overrides. The service-limit group of matrix §4 and the commercial register of `decision-criteria.md` §7.1 are the two lists that must be stamped exhaustively.

### 8.5 Scope — what must be traced

**Mandatory** (gate G3): any rule that materially influences architecture, governance, security, ALM, scale, cost or implementation. Concretely: every threshold, every exclusion, every gate, every outcome string, every constraint check, and every "must"/"never" in a `RESEARCH` file.

**Not required**: prose framing, examples, formatting guidance, and everything in `craft/` (which instead carries the `CRAFT` class once, at file level).

### 8.6 Explicit non-goals

No claim ledger. No per-sentence ids. No bidirectional index file. No confidence scores of our own — the corpus's confidence is inherited by reference, never restated as a new number. The convention must survive a maintainer with `grep` and no tooling.

---

## 9. Authoring sequence

Derived from actual dependencies, not from `docs/PACK_AUTHORING.md`'s greenfield order.

**Why the order changed.** That guide prescribes glossary → question bank → decision tree → deliverables → domain knowledge last. With a canonical decision layer in hand the dependency reverses: **the decision model determines what must be elicited**, so criteria precede questions; the glossary is a by-product of the vocabulary the criteria and questions already use, not the anchor; and domain knowledge cannot be last because architecture templates, the blueprint contract and the design brief all resolve against it. The guide's order was correct for a pack with no research behind it.

| # | Stage | Must already exist | Produces | Exit gate |
|---:|---|---|---|---|
| S0 | Baseline freeze | — | Canonical baseline (done) | manifest §13 |
| S1 | Authoring map | S0 | this document | G0 |
| S2 | Conventions | S1 | `PROVENANCE.md`, `neutrality-denylist.md`, `CHANGELOG.md` | G0 |
| S3 | Decision spine | S2 | `outcome-classes.md` → `exit-classes.md` → `blocking-set.md` → `composed-disqualifiers.md` → `comparator-rules.md` → `decision-tree.md` (ordered procedure) | G1, G4, G6 |
| S4 | Criteria register | S3 (a criterion's class is meaningless without the outcome set) | `criteria-register.md`, `volatility-register.md`, `validation-levels.md` | G1, G3, G7 |
| S5 | Registers | S4 | `anti-pattern-register.md`, `alternatives-register.md` | G1, G6 |
| S6 | Decision-logic regression | S3–S5 | replay of `T-01`…`T-18` against the authored model | **G5** |
| S7 | Discovery layer | S4 (questions derive from `Discovery evidence` fields) + S2 (denylist) | `discovery-signals.md`, `question-bank.md`, `discovery-vocabulary.md`, `options-glossary.md`, `options-checks.md` | **G2**, G1, G8 |
| S8 | Lens + manifest wiring | S7 | `pack.yaml` `lenses_config`, `technology.constraints_to_check`, `epistemics` | G2, G8 |
| S9 | Domain knowledge (class C) | S3 (boundary shapes) — independent of S7 | the 16 `RESEARCH` files + the 9 `craft/` files | G1, G3, G4, G6, G7 |
| S10 | Architecture templates | S3 (outcome classes) + S9 | one template per reachable shape | G5 (reachability both directions) |
| S11 | Blueprint alignment | S9, S10 | screen catalogue, naming and hard caps reconciled with `blueprint-contract.md` | G6 |
| S12 | Deliverables + synthesis mapping | S3 (render strings), S10 | 6 updated templates + slot sources | G3, G6 |
| S13 | Manifest close-out | S1–S12 | `pack.yaml` final, `pack_version` bump, `CHANGELOG.md` entry | G0–G8 full sweep |
| S14 | Pack validation | S13 | fixture engagement `--dry-run`, `/simulate`, `/render --dry-run`; consumer-reference sweep (§12 Q-05) | all gates + `docs/PACK_AUTHORING.md` checklist |

S7 and S9 are independent after S4 and may run in parallel by different authors. S6 is a hard checkpoint: no Discovery or domain-knowledge authoring is worth doing against a decision spine that fails the corpus's own scenarios.

---

## 10. Authoring gates

Proportional by design: seven of the nine are mechanical (`grep`/script), and the two review gates are scenario replays with a fixed pass criterion. No governance board, no sign-off ceremony, no ledger. Gates run **at stage boundaries** (§9), never only at the end.

| Gate | Detects | Method | Pass criterion |
|---|---|---|---|
| **G0 — structural** | Missing declared files; manifest/file drift; broken intra-pack links | Script over `pack.yaml` + filesystem + relative links | 0 missing, 0 broken |
| **G1 — canonical reference resolution** | Broken canonical references; ambiguous unqualified ids | Extract every id from every `Research basis:` line; resolve against the 16 canonical files; flag any `AP-NN`/`DC-NN`/`D-NN`/`C-01`/`S-NN`/`G-NN` that is not file-qualified | `UNRESOLVED CANONICAL REFERENCES: 0`, `AMBIGUOUS REFERENCES: 0` |
| **G2 — Discovery neutrality** | Technology contamination in Discovery | Denylist regex (`neutrality-denylist.md`) over the Discovery-visible set: `question-bank.md`, `discovery-signals.md`, `discovery-vocabulary.md`, `pack.yaml` Discovery `extra_signals`, `discovery-report` + `executive-report` templates | 0 hits, or each hit annotated `# current-state` and passing the N-05 form |
| **G3 — unsupported assertion** | Recommendations with no basis; invented numbers; forbidden comparatives; price quotes | Regex sweep in `RESEARCH` files for: numerals in a rule without a `Research basis:` line; `preferred`/`better`/`cheaper`/`faster` near an `ALT-` mention; currency symbols; SLA/availability percentages | 0 unbasis'd numerals · 0 forbidden comparatives (`alternatives.md` §2.2, `decision-criteria.md` §6.1) · 0 prices (`licensing-cost.md` §12) |
| **G4 — contradiction with canonical** | A pack rule disagreeing with the corpus | Targeted review of every rule citing an id in matrix §4 (volatile/conflicted) or a `NB-0N` reservation; plus a diff of every numeric threshold against its cited source | 0 contradictions; every `CONFLICTED` id renders the conflict, never a value |
| **G5 — decision-logic regression** | Wrong or unreachable outcomes; lost composed disqualifiers; `Ri` rendered as an exclusion | Replay `T-01`…`T-18` (matrix §6) against the authored decision model; check outcome-set closure and template reachability in both directions | 18/18 reproduce the canonical outcome · every emitted label appears verbatim in the closed 14-set · every outcome naming an architecture has a template and vice versa |
| **G6 — duplication and conflict** | The same rule in two files; two files stating one threshold differently | Cross-file index of cited ids and of numeric thresholds; any id justifying a *rule* in two `RESEARCH` files is a finding (cross-references are fine) | 1 rule → 1 home; 0 divergent restatements |
| **G7 — volatility** | A dated or volatile fact presented as stable | Every id in `decision-criteria.md` §7.1/§7.2 and matrix §4 that appears in the pack must carry `VOLATILE` + `verificado_em` + `validade` + a revalidation trigger | 100% stamped |
| **G8 — coverage** | Silent loss of canonical content | Coverage report: each of the 116 `DC-D` has an elicitation home or a recorded exclusion reason; each of the 68 `AP-D` is reachable; all 11 `ALT` are emittable; all 14 outcome classes are reachable; all 12 composed rows are runnable | 100%, or an explicit and reasoned exclusion list |

Gate output is a short block of counters appended to `CHANGELOG.md` — the same shape as the research gates, deliberately, so the two halves of the project read alike.

---

## 11. Deprecated / redundant existing content

| Item | Verdict | Reason |
|---|---|---|
| `decision-tree.md` R1–R6 scored verdicts and the aggregation instruction | **DEPRECATE** | Scoring model; `decision-criteria.md` §2.3, §2.4 — states, not scores; scoring is the construct that loses `AP-D-059` |
| `decision-tree.md` R0 thresholds: `30,000` rows, `formula_count > 100`, `external_integrations_count > 3`, "sub-second", the 5,000/100,000 bands | **DEPRECATE** | Invented numbers — `AP-D-051`, classification `CONSTRAINT`; canonical SharePoint figures are `DA-39`/`DA-40`; `SC-16`/`SC-18` record that no user-concurrency and no standard-table row ceiling are published |
| `decision-tree.md` three-branch option space | **DEPRECATE** | 11 `ALT` classes and a closed 14-class outcome set cannot be expressed in it (F-03) |
| `glossary.md § Discovery fit criteria` (6 rating axes) | **DEPRECATE** | Scoring vocabulary; same basis as row 1. Replaced by outcome classes + exit classes |
| `glossary.md` as a Discovery-loaded vendor dictionary | **DEPRECATE in that role** | Content survives in `options-glossary.md`; Discovery gets `discovery-vocabulary.md` (rule N-07) |
| `question-bank.md § S1–S9`, `§ P1–P10`, `M1–M9`, `D3` as written | **DEPRECATE in Discovery** | Technology contamination (F-05, §6.4); content survives in class C |
| `estimation-model.md § LICENSE COST ESTIMATES` | **DEPRECATE** | `licensing-cost.md` §12 — the pack must never quote a price |
| `azure-sql-reference.md` build-convention sections presented as platform reference | **DEPRECATE in that framing** | `CRAFT` content in a file read as authoritative; survives in `craft/sql-delivery-conventions.md` with the correct provenance class |
| `dataverse-reference.md` / `sharepoint-reference.md` limit tables as authored | **DEPRECATE in that form** | Predate the corpus and carry no provenance or dates; rewritten against `DA-*` with `VOLATILE` stamps |
| Any pack content citing the **CoE Starter Kit** or **ALM Accelerator** | **REVIEW then DEPRECATE** | `GOV-12` deprecation; `governance.md` §10 and `alm-devops.md` §10 both require explicit review of prior art citing them |
| `agent-memory` note asserting the SharePoint 2,000-record failure rule | **UPDATE** (outside the pack) | `.claude/agent-memory/_universal/solution-architect/anti-patterns.md` restates a threshold; must point at `data/query-and-delegation.md` instead. Tracked as Q-05 |

Nothing is deleted at Step 1. Deprecation is executed inside the stage that replaces it, and recorded in `CHANGELOG.md` with the canonical id that justified it.

---

## 12. Open authoring questions

| # | Question | Impact if unresolved | Proposed default |
|---|---|---|---|
| **Q-01** | `anti-patterns.md` §4 states `Count: 67` while its own register, §3.12, §9 and manifest §11 state 68. Research is frozen — repair requires a new research → review → gate cycle. | Cosmetic for authoring; the register and entries are complete and unambiguous. | Author against **68**; record the discrepancy in `CHANGELOG.md`; raise a bounded research-side correction separately. Do not touch the canonical file. |
| **Q-02** | Pack language. `pack.yaml` declares `language: pt`; the entire canonical corpus and its terminology are English. | Mixed-language rules risk mistranslating outcome-class strings that must be emitted verbatim. | **Decision layer in English** (outcome strings, class markers and ids quoted verbatim); Discovery-facing prose and deliverables stay `pt`. Needs owner sign-off. |
| **Q-03** | `library/` is read-only at runtime and `pre-write-guard.py` fails closed. Authoring writes into `library/packs/pp/`. | Every stage is blocked without an authoring path. | Author out-of-band via the sanctioned git path (`.claude/rules/library-readonly.md`), on a branch, with the hook active for runtime only. Confirm the mechanics before S2. |
| **Q-04** | Does the pack keep `decision-tree.md` as the filename for what is now an evaluation procedure? | Renaming breaks `pack.yaml.decision_tree.source`, `lens-technology`, `solution-architect`, `aisa-simulate`. | **Keep the filename**, change the content. Revisit only if the kernel contract changes. |
| **Q-05** | Domain-knowledge renames have consumers outside the pack: `aisa-blueprint` (`screen-consolidation-rules.md`), `lens-technology`, `solution-architect`, `aisa-simulate`, `claude-design-brief.template.md`, `docs/ARCHITECTURE.md`, two agent-memory files. | Silent breakage of skills at runtime. | Treat consumer updates as part of S9/S14, not as a follow-up. Gate G0 extended to sweep `.claude/` and `docs/` for stale pack paths. |
| **Q-06** | Agent/Copilot surfaces: `DC-D-116` and `AP-D-068` exist but `alternatives.md` §5.1 records no evaluable class and `DECISION BLOCKED` as the correct output. | A pack file here would be invention. | Carry as **one criterion row + one anti-pattern row + a `DECISION BLOCKED` path**. No domain-knowledge file until research exists. |
| **Q-07** | Craft content (Power Fx, screens, estimation, anonymisation, SQL conventions) has no research basis and the corpus never evaluated it. | Either it is silently laundered into research-backed rules, or it is lost. | `Provenance: CRAFT`, own namespace, may not state platform limits or comparatives (§8.3). Confirm the team accepts the label. |
| **Q-08** | Half-life overrides. `pack.yaml.epistemics.half_lives_override` is empty with a TODO to calibrate at the pilot retro. The corpus shows platform facts changing **within the research window**. | Pack rules and SU rows decay slower than the facts. | Propose `plataforma-tecnica: 9 meses` and `financeiro: 3 meses` for this pack at S8; validate at the first retro. |
| **Q-09** | Where do the two evidenced **upstream** lineage defects (duplicate `DC-14` in `licensing-cost.md`; `IA-C-01` vs mounted `C-01`) land in pack references? | G1 could flag legitimate citations as ambiguous. | Cite the Block D canonical form and, where the Area file must be cited, use both forms as Block D does: `IA-C-01 (C-01)`. Encode as a G1 exception list. |
| **Q-10** | `decision-criteria.md` §9 records `R-03` (the `DC-D-055` matrix row) as **open and out of the last repair's scope**. | A criterion row may be authored against an unsettled matrix row. | Author `DC-D-055` from `decision-criteria.md` §4 only; mark the matrix row `OPEN` in `criteria-register.md`; do not synthesise the missing join. |
| **Q-11** | **Options material-coverage.** Today the Options layer bounds constraint evaluation to `lenses_config.technology.constraints_to_check` (5 entries for `pp`) plus the technology lens's 9-token signal catalog, and `lens-technology` execution step 2 emits *a verdict per constraint*. A material concern outside that fixed list (governance, operability, reversibility beyond the listed five) can be silently omitted. | An option could be chosen without a material concern having been considered. | **Deferred to Step 3A by design** — Options is being re-authored there. Fix in the decision model (§9 S3/S8), not by patching the lens: the constraint set must become materiality-driven, with the fixed list as a floor, not a ceiling. Principle 3 governs. |

---

`AUTHORING MAP CREATED: YES`
`CANONICAL BASELINE FULLY MAPPED: YES`
`DISCOVERY NEUTRALITY BOUNDARY DEFINED: YES`
`DOMAIN-KNOWLEDGE TAXONOMY DEFINED: YES`
`TRACEABILITY CONTRACT DEFINED: YES`
`AUTHORING SEQUENCE DEFINED: YES`
`AUTHORING GATES DEFINED: YES`
`READY FOR PP PACK AUTHORING STEP 2: YES`
`AUTHORING PRINCIPLES (§1.5) BINDING FROM STEP 3: YES`
