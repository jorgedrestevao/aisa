# Step 6A — Deliverable Projection Model & Authoring Design

<!--
provenance: AUTHORING (design document) · class: DESIGN
authored: 2026-09-04 (Step 6A) · design authority: this file
Predecessors: step-5a-architecture-template-model.md (frozen), step-5b (closed),
step-5c-architecture-semantic-gate-report.md (PASS + class-6 addendum + §27 freeze marker).
DESIGN ONLY. No deliverable template, synthesis template, render runtime, pack.yaml, Step 3,
Step 4 or Step 5 architecture runtime file was modified by this step. The only non-report
modification made in Step 6A is the documentation-only Step 5 freeze marker appended as §27 of
the Step 5C report.
-->

---

## 1. Purpose and doctrine

Step 6A defines **how each canonical deliverable projects the same engagement truth** at a different
audience, altitude and level of detail — without creating a second reasoning layer.

### 1.1 The binding chain

```text
Shared Understanding
        ↓
Decision
        ↓
Architecture
        ↓
Deliverable projections
```

### 1.2 The forbidden chain

```text
deliverable template
→ re-reason evidence
→ choose interpretation
→ create a new decision
```

### 1.3 What a deliverable template is

A **projection contract**: it names its authorities, selects a subset of what they hold, and states the
transformations it may and may not apply.

It is **not** a decision model, an architecture model, a Domain Knowledge unit, a research summary, or an
independent synthesis agent.

### 1.4 The three operative rules

| Rule | Statement |
|---|---|
| **R1 — closest authority** | A deliverable reads the closest authoritative upstream artefact for each fact. Never raw evidence for something already settled upstream. |
| **R2 — compression without reinterpretation** | A projection may compress, reorder, re-word for audience, and change table↔prose. It may not change epistemic state, decision meaning, scope, architecture ownership, risk acceptance, proof level or comparator status. |
| **R3 — no truth by repetition** | A statement appearing in two deliverables has one authority. The second occurrence is a projection, not a competing claim. |

### 1.5 Relationship to Step 5

Step 5 is frozen (Step 5C §27). Step 6 consumes the frozen Architecture Layer — the `architecture:`
block, `architecture-core.md`, the experience fragments, the boundary fragment, the reachability ×
architectability gate and the four render-gap classes — and **adds no architecture reasoning of its own.**

---

## 2. Current deliverable inventory

Source: `library/packs/pp/deliverable-templates/` (6 files) + `library/packs/pp/pack.yaml` (manifest) +
`library/kernel/synthesis-templates/` (5 templates) + `library/kernel/render-contract.md` +
`.claude/skills/aisa-render/SKILL.md` + `.claude/skills/aisa-synthesize/SKILL.md`.
`library/packs/pp-backup/` is a pre-Step-3 snapshot, **not runtime**, and is excluded from every count and
every migration disposition in this report.

### 2.1 Per-file record

#### 2.1.1 `discovery-report.template.md` (54 lines)

| Field | Value |
|---|---|
| Canonical deliverable | **1 — Discovery Report** |
| Audience declared | `client` |
| Source inputs | `_synthesis/business-story.md`, `_synthesis/as-is.md`, `_synthesis/risks-and-assumptions.md`, `shared-understanding.md# lens=data (Confirmed + Assumed)`, `context.json# requester`, `inputs/*` |
| Render path | `aisa-render` → `_render/<slug>_discovery-report_v<NN>.md` (+ `--html` interrogable projection, v3.0 scope) |
| Sections | 8: business context · current state · processes · data inventory · friction · stakeholders · sources · pending validation |
| Embedded reasoning instructions | none |
| Branch / chosen-architecture references | **none** |
| Duplicated decision logic | none |
| Duplicated architecture knowledge | none |
| Duplicated Domain Knowledge | none |
| Hardcoded PP facts | none |
| Volatile facts | none |
| Prices | none |
| CRAFT leakage | none |
| Epistemic handling | **partial** — Confirmed + Assumed only. No Unknown section of its own, no Conflicted, no Risky. `open_assumptions_list` carries Assumed + Critical Unknowns via the risks synthesis |
| Render-gap handling | inherited from the render contract; nothing template-local |
| Survives | **yes** |
| Class | **REWRITE** (epistemic completeness + materiality selection) |

#### 2.1.2 `executive-report.template.md` (60 lines)

| Field | Value |
|---|---|
| Canonical deliverable | **2 — Executive Report** |
| Audience declared | `sponsor` |
| Source inputs | `_synthesis/business-story.md`, `_synthesis/architecture-story.md`, `_synthesis/financial-story.md`, `_synthesis/risks-and-assumptions.md`, `decisions.md# Justification / Alternatives / Tripwires`, `options.md` (whole file) |
| Render path | `aisa-render` → `_render/<slug>_executive-report_v<NN>.md` |
| Sections | 9: business case · chosen solution · timeline · investment · decision context · options evaluated · alternatives · risks · pending validation |
| Embedded reasoning instructions | none explicit; `decision_options: options.md` (unsectioned whole-file slot) implicitly invites re-presentation of the option set at executive altitude |
| Branch / chosen-architecture references | none directly; inherits the branch vocabulary through `options.md` (`chairman.md` still writes `Branch (if technology)` there) |
| Duplicated decision logic | **risk** — `decision_options` + `alternatives_summary` together re-stage the comparison |
| Duplicated architecture knowledge | `chosen_solution_summary` ← architecture-story `# Chosen architecture, Platform and components` — architecture detail at executive altitude |
| Duplicated Domain Knowledge | none |
| Hardcoded PP facts / volatile facts / prices | none |
| CRAFT leakage | none |
| Epistemic handling | `open_assumptions_list` **optional** — Assumed + Critical Unknown may be omitted entirely. No Conflicted, no Risky-as-accepted-risk identity beyond the risks slot |
| Render-gap handling | inherited |
| **Missing authorities** | `decisions.md# Conditions`, `# Proof obligations`, `# Preconditions`, `# (Scope, outcome) pairs — UNCOLLAPSED` are **all unread** |
| Survives | **yes** |
| Class | **REWRITE** |

#### 2.1.3 `solution-blueprint.template.md` (55 lines)

| Field | Value |
|---|---|
| Canonical deliverable | **3 — Architecture Blueprint** (id/file alias: `solution-blueprint`) |
| Audience declared | `technical` |
| Source inputs | `_synthesis/architecture-story.md` (4 sections), `_synthesis/financial-story.md# Build effort`, `decisions.md# Alternatives considered`, `decisions.md# D-NNN — Branch (if technology)`, `_synthesis/risks-and-assumptions.md` (whole file), `architecture-templates/{{chosen_architecture}}.md` |
| Render path | `aisa-render` → `_render/<slug>_solution-blueprint_v<NN>.md`; `applies_to: [technology]` |
| Sections | 8: executive summary · chosen architecture (sub-template) · data model · security/RBAC · integrations · estimate · alternatives · pending validation |
| Embedded reasoning instructions | none |
| Branch / chosen-architecture references | **`chosen_architecture` required slot · `Branch (if technology)` slot source · `{{>> architecture-templates/{{chosen_architecture}}.md}}` dynamic include** — all three dead |
| Duplicated decision logic | `alternatives_considered` at architecture altitude |
| Duplicated architecture knowledge | the whole file re-shapes A3/A5/A7 as its own sections instead of projecting `architecture-core.md`'s A-sections |
| Duplicated Domain Knowledge | none |
| Hardcoded PP facts / volatile facts / prices | none |
| CRAFT leakage | none |
| Epistemic handling | `open_assumptions_list` optional, whole-file slot. Proof obligations, open architecture choices, volatile stamps: **unread** |
| Render-gap handling | inherited |
| Survives | **yes, as the projection of the frozen architecture layer** |
| Class | **REWRITE** |

#### 2.1.4 `implementation-spec.template.md` (77 lines)

| Field | Value |
|---|---|
| Canonical deliverable | **4 — Implementation Specification** |
| Audience declared | `developer` |
| Source inputs | `decisions.md# Branch (if technology)`, `_synthesis/architecture-story.md` (Data, Platform and components, Security model, Integrations), `_blueprint/ux-blueprint_v<approved>.yaml# screens`, `_synthesis/as-is.md# Top friction points, Exceptions…`, `_synthesis/financial-story.md# Build effort`, `shared-understanding.md# lens=data (Risky rows about historical data / migration)`, `_synthesis/risks-and-assumptions.md` |
| Render path | `aisa-render` → `_render/<slug>_implementation-spec_v<NN>.md`; `applies_to: [technology]` |
| Sections | 10: architecture · entities · screens/components · flows · security & roles · integrations · test scenarios · sequencing · migration notes · pending validation |
| Embedded reasoning instructions | **yes, and legitimate in kind** — each section carries a shape instruction (`> One row per entity: …`). These are formatting contracts, not reasoning |
| Branch / chosen-architecture references | `chosen_architecture` required slot + `Branch (if technology)` source (dead) |
| Duplicated decision logic | none |
| Duplicated architecture knowledge | re-derives the architecture shape through narrative synthesis rather than the `architecture:` block |
| Duplicated Domain Knowledge | none (the DK it needs is not pulled at all) |
| Hardcoded PP facts | none |
| Volatile facts | none |
| Prices | none |
| CRAFT leakage | none — and **CRAFT is legitimately needed here and absent** |
| Epistemic handling | `open_assumptions_list` optional. Proof obligations (V1–V4) **unread**; `test_scenarios` derived from discovery friction instead |
| Render-gap handling | inherited; the template's own "if a section is thin, loop back" note is a completeness heuristic that predates the four gap classes |
| Survives | **yes** |
| Class | **REWRITE** |

#### 2.1.5 `claude-design-brief.template.md` (67 lines)

| Field | Value |
|---|---|
| Canonical deliverable | **5 — Claude Design Brief** |
| Audience declared | `claude-design` |
| Source inputs | `decisions.md# Branch (if technology)`, `decisions.md# Blueprint bp-v<NN> aprovado`, `_blueprint/ux-blueprint_v<approved>.yaml` (screens · navigation · personas · ui_states · excluded_from_ui), `context.json# brand_guidance`, `shared-understanding.md# lens=user`, `architecture-templates/{{chosen_architecture}}.md` |
| Render path | `aisa-render` → `_render/<slug>_claude-design-brief_v<NN>.md`; `applies_to: [technology]` |
| Sections | 8: context & architecture (sub-template) · personas · pages · navigation · UX requirements · brand · accessibility · **Domain Knowledge cross-references (6-row table + 2 explanatory paragraphs)** |
| Embedded reasoning instructions | the citation convention (legitimate); the DK table's framing ("carries the dense technical context Claude Design downstream needs") is a **preload instruction** |
| Branch / chosen-architecture references | `chosen_architecture` slot + `Branch (if technology)` source + dynamic include (dead) |
| Duplicated decision logic | none |
| Duplicated architecture knowledge | **the whole architecture** is included as §1 |
| Duplicated Domain Knowledge | **yes — 6 units named and characterised inline** (`craft/powerfx.md`, `craft/screen-patterns.md`, `craft/security-craft.md`, `craft/screen-consolidation-rules.md`, `craft/excel-translation.md`, `data/query-and-delegation.md`) |
| Hardcoded PP facts | vendor/product vocabulary throughout ("Canvas App", "Power FX") — legitimate post-Options, but it hardcodes an **experience-mode assumption** |
| Volatile facts / prices | none |
| CRAFT leakage | **yes, by design and over-broad** — 5 CRAFT units preloaded; the `craft/` vs `RESEARCH` boundary is stated correctly but the carriage is indiscriminate |
| Epistemic handling | **none** — no Assumed/Unknown/Conflicted/Risky carriage at all |
| Render-gap handling | inherited; the template notes the missing-blueprint case explicitly (good) |
| **Applicability gate** | **absent** — `canvas_app_pages`, `page_navigation_map`, `persona_users`, `ux_requirements` are all **required**, so `experience.mode: none` produces four required-slot gaps |
| Survives | **yes, narrowed** |
| Class | **REWRITE** |

#### 2.1.6 `estimate.template.md` (63 lines)

| Field | Value |
|---|---|
| Canonical deliverable | **6 — Estimate** |
| Audience declared | `client` |
| Source inputs | `_synthesis/financial-story.md` (8 of 9 slots), `_synthesis/risks-and-assumptions.md` (2 slots) |
| Render path | `aisa-render` → `_render/<slug>_estimate_v<NN>.md`; `applies_to: all`, `mandatory: false` |
| Sections | 10: summary · phases · timeline · detailed per phase · effort summary · team · risks · operational impact · assumptions · recommendations |
| Embedded reasoning instructions | **none — and that is the defect.** The template owns no estimation logic; the calculation happens in `financial-story.template.md` |
| Branch / chosen-architecture references | none |
| Duplicated decision logic | inherits decision economics through `financial-story` (budget envelope, payback/ROI, do-nothing cost) |
| Duplicated architecture knowledge | none |
| Duplicated Domain Knowledge | none — `craft/estimation-model.md` is **not referenced by any runtime deliverable template** |
| Hardcoded PP facts | none |
| Volatile facts | none stamped |
| Prices | no literal prices in the template; the `financial-story` slots it consumes are explicitly monetary ("indicative cost", "investment") — the **price surface is one hop upstream and unstamped** |
| CRAFT leakage | none |
| Epistemic handling | `assumptions` + `risks_table` present; "cost and effort figures are Assumed unless documented" lives in the synthesis prompt, not the template |
| Render-gap handling | inherited |
| Survives | **yes** |
| Class | **REWRITE** |

### 2.2 Kernel-side consumers inspected (not deliverable templates)

| File | Role | Step 6 relevance |
|---|---|---|
| `library/kernel/render-contract.md` | pipeline, slot resolution order, versioning, applicability, architecture discriminator, **4 render-gap classes** | reused unchanged in substance; one label generalization proposed (§32) |
| `library/kernel/synthesis-templates/business-story.template.md` | neutral business narrative | KEEP |
| `…/as-is.template.md` | neutral as-is narrative | KEEP |
| `…/architecture-story.template.md` | architecture narrative | **REWRITE (bounded)** — carries I-1 and I-2 |
| `…/risks-and-assumptions.template.md` | Assumed / Risky / Critical Unknown / Conflicted / watch-list | **REWRITE (bounded)** — add conditions, proof obligations, expired-validity rows |
| `…/financial-story.template.md` | **decision economics *and* the whole implementation estimate calculation** | **SPLIT (semantic, not necessarily file-level)** — see §17, §18 |
| `.claude/skills/aisa-render/SKILL.md` | slot resolution, architecture include, iteration, gap classes | UPDATE in 6B (deliverable ids, applicability, gap-owner label) |
| `.claude/skills/aisa-synthesize/SKILL.md` | 5 topic packs | UPDATE in 6B (financial split, epistemic carriage) |
| `library/packs/pp/pack.yaml` | deliverable manifest + `applies_to` | UPDATE in 6B (discriminator, `canonical_deliverable`) |

### 2.3 Classification summary

| File | Class | One-line reason |
|---|---|---|
| `discovery-report.template.md` | **REWRITE** | epistemically incomplete; no materiality rule |
| `executive-report.template.md` | **REWRITE** | conditions, proof obligations and scope pairs unread; comparison re-staged |
| `solution-blueprint.template.md` | **REWRITE** | dead branch include; does not project the frozen architecture layer |
| `implementation-spec.template.md` | **REWRITE** | dead branch slot; acceptance work derived from discovery instead of proof obligations |
| `claude-design-brief.template.md` | **REWRITE** | full-architecture copy + DK preload + no headless gate |
| `estimate.template.md` | **REWRITE** | owns no calculation; economics conflated upstream |
| — | **MERGE: none** | the six audiences are materially distinct (`docs/ARCHITECTURE.md §5.4`) |
| — | **SPLIT: none (deliverables)** | one semantic split at the **synthesis** layer only (financial) |
| — | **RETIRE: none** | |
| — | **REPLACE: none** | |

**No canonical deliverable is added, renamed or removed.** Six in, six out.

---

## 3. Current source-of-truth defects

Read: raw evidence (`inputs/*`, capture) · **SU** · **decisions** · **architecture** (`architecture:`
block / `architecture-core.md`) · **synthesis** · **other deliverables**.

| # | Deliverable | Reads | Defect |
|---|---|---|---|
| **D-1** | blueprint · impl-spec · design-brief | decisions (removed field) | `chosen_architecture` ← `decisions.md# D-NNN — Branch (if technology)`. `/decide` **removed** that field (`aisa-decide` §"What this skill serializes"). Three required slots resolve to nothing |
| **D-2** | blueprint · design-brief | pack file (retired) | `{{>> architecture-templates/{{chosen_architecture}}.md}}` — the three branch templates were retired in Step 5B. A dynamic include over a dead value |
| **D-3** | **all six** | — | **No deliverable reads the `architecture:` block.** Authorization, experience mode, `record_authority[]`, `compositions[]`, `relocated_responsibilities[]`, `proof_obligations[]`, `open_architecture_choices[]` are unreachable at render time; architecture reaches deliverables only as narrative |
| **D-4** | executive | decisions (partial) | `decisions.md# Conditions`, `# Proof obligations`, `# Preconditions` and `# (Scope, outcome) pairs — UNCOLLAPSED` are **unread by every deliverable**. A condition that qualifies the recommendation can disappear (violates §21) |
| **D-5** | executive | options.md (whole file) | Re-presenting the option set plus per-alternative "why not" at executive altitude invites a **fresh comparison**; and `options.md` still carries `Branch (if technology)` from `chairman.md` |
| **D-6** | discovery | SU (partial) | Conflicted (`X-NNN`) and Risky (`R-NNN`) have **no path into the Discovery Report**. Only Confirmed + Assumed (+ Critical Unknown via risks synthesis) reach it |
| **D-7** | impl-spec | **synthesis of raw discovery** | `test_scenarios` ← `as-is.md# Top friction points, Exceptions…`. Acceptance work is derived from **discovery evidence** while `proof_obligations[]` (V1–V4, method, owner, funded) is unread. This is the clearest downstream re-reasoning of upstream-settled material |
| **D-8** | impl-spec | financial synthesis | `sequencing` ← `financial-story.md# Build effort and indicative cost`. Build order is an **architecture-dependency** fact; the financial narrative is the wrong authority |
| **D-9** | impl-spec | **raw SU rows** | `migration_notes` ← `shared-understanding.md# lens=data (Risky rows about historical data / migration)`. Bypasses the class-14 outcome and A9's *replacement of an existing artefact* conditional; re-reads evidence for something the decision/architecture already settled |
| **D-10** | design-brief | architecture (whole) + DK (preloaded) | The full architecture as §1 + six named Domain Knowledge units characterised inline. Violates *selective DK* (§29) and the Blueprint→Design altitude boundary (§37) |
| **D-11** | design-brief | — | **No applicability gate.** Four surface slots are `required`, so `experience.mode: none` manufactures four gaps for an architecture that correctly has no surface (violates §22) |
| **D-12** | impl-spec | blueprint (approved) | `screens_to_build` is `required` with a fallback to architecture narrative — a headless architecture yields either a gap or an invented surface |
| **D-13** | estimate | financial synthesis (only) | The Estimate owns **no** calculation. Work breakdown, phase tables, day counts, Gantt, team mix and operational-impact deltas are all produced inside `financial-story.template.md` |
| **D-14** | estimate + executive | financial synthesis (merged) | `financial-story.md` **merges decision economics** (as-is cost, do-nothing cost, budget envelope, payback/ROI) **with implementation effort** (phases, days, timeline, team). §18 requires these to stay distinct; today one artefact owns both and both deliverables inherit the merge |
| **D-15** | estimate | — | `craft/estimation-model.md` — the pack's estimation method, with its explicit *not valid as comparative economics* banner — is referenced by **no runtime deliverable template** |
| **D-16** | blueprint | financial synthesis | `estimation_summary` pulls effort/cost into the architecture deliverable, and `executive_summary` duplicates the Executive Report's job. Repetition without ownership |
| **D-17** | pack.yaml | — | `applies_to: [technology]` is the wrong discriminator (Step 5A §3 defect 6). The real discriminator — *does an architecture authorization exist for at least one scope?* — lives in `render-contract.md` and is not reflected in the manifest |
| **D-18** | synthesis | decisions | `architecture-story.template.md` §*Chosen architecture* asks for *"why it won over alternatives"* — **observation I-2** |
| **D-19** | — | — | **`not-authorized` has no structured durable home** — **observation I-1** |
| **D-20** | docs | — | `docs/ARCHITECTURE.md` §5.3 and `docs/PACK_AUTHORING.md` §113 still describe `architecture-templates/<chosen>.md` and `{{chosen_architecture}}` as the mechanism. Documentation-only |

### 3.1 The three cases of genuine downstream re-reasoning

Flagged explicitly, per the Step 6A commission:

1. **D-7** — Implementation Specification reads raw discovery friction to invent acceptance work, while
   the decision's proof obligations sit unread.
2. **D-9** — Implementation Specification reads raw SU `lens=data` Risky rows to write migration notes,
   while the class-14 outcome and A9 sit unread.
3. **D-10** — Claude Design Brief pulls six Domain Knowledge units directly, at a point where the
   architecture layer has already consumed the knowledge those units hold.

Everything else is a *missing* authority (D-3, D-4, D-6, D-15) or a *wrong* authority
(D-8, D-13, D-14, D-16), not an independent re-reading of evidence.

### 3.2 One benign raw-evidence read — kept

`discovery-report`'s `sources_analysed: inputs/*` lists the artefacts analysed. That is an **inventory**,
not a reinterpretation, and `_capture/evidence-index.md` is its natural entry point. **KEEP**, re-sourced
to the capture index where one exists.

---

## 4. Canonical deliverable mapping

| # | Canonical deliverable | Runtime file | Manifest id | Alias needed |
|---:|---|---|---|---|
| 1 | Discovery Report | `discovery-report.template.md` | `discovery-report` | — |
| 2 | Executive Report | `executive-report.template.md` | `executive-report` | — |
| 3 | **Architecture Blueprint** | `solution-blueprint.template.md` | `solution-blueprint` | **yes** |
| 4 | Implementation Specification | `implementation-spec.template.md` | `implementation-spec` | — |
| 5 | Claude Design Brief | `claude-design-brief.template.md` | `claude-design-brief` | — |
| 6 | Estimate | `estimate.template.md` | `estimate` | — |

**6/6 accounted for. No repository contradiction requires escalation.**

**On #3's name.** `docs/ARCHITECTURE.md §5` already calls it *Architecture Blueprint*; the file and
manifest id say `solution-blueprint`. This is an **alias, not a contradiction**, so §2 of the commission
forbids renaming it here. Step 6B adds one frontmatter field —
`canonical_deliverable: architecture-blueprint` — and the id/file/CLI argument stay `solution-blueprint`.

**Recorded observation (no action).** The engagement now has two artefacts called "blueprint": the
**UX blueprint** (`_blueprint/ux-blueprint_v<NN>.yaml`, an *input*, produced by `/blueprint` in the
Decision phase) and the **Architecture Blueprint** (a *deliverable*, rendered from `_render/`). Step 6B
must never let a template or slot source conflate them; the test set covers it (**T-D14**, §29).

---

## 5. Primary-authority table

One primary authority per information class. Binding in Step 6B.

| Information class | **Primary authority** | Permitted projections (read-only, compress-only) | Forbidden |
|---|---|---|---|
| **engagement fact** | `shared-understanding.md` row (`C/A/U/X/R-NNN`) | every deliverable, by id | restating a fact without its id; re-deriving it from `inputs/*` |
| **epistemic state** | `shared-understanding.md` row state + `library/kernel/states.md` vocabulary; `verificado_em` / `validade` on the row | every deliverable must preserve the state where the fact is material | promotion, silent expiry, "assumed" → "confirmed" |
| **decision** | `decisions.md` `D-NNN` | executive (full) · blueprint (basis only) · impl-spec (as constraint) · discovery (not at all) | re-deciding; re-wording an emitted outcome sentence |
| **(scope, outcome) pair** | `decisions.md` `# (Scope, outcome) pairs — UNCOLLAPSED` (verbatim from `options.md`) | executive · blueprint · impl-spec · estimate | collapsing two scopes; re-wording; dropping a marker |
| **condition / precondition** | `decisions.md` `# Conditions` / `# Preconditions` | executive (required where it qualifies the recommendation) · blueprint · impl-spec (required where it gates build) | converting *condition* → *satisfied*; omitting from Executive |
| **risk acceptance** | `decisions.md` `# Accepted risks` + the SU `R-NNN` rows it points at | executive · blueprint · impl-spec · estimate (as uncertainty) | dropping the accepted-risk identity; re-grading impact |
| **option comparison** | `options.md` (+ frozen `_simulation/counterfactuals/<O-NNN>.md`) | executive: the decision's own recorded *why not* lines only | any fresh comparison, ranking or score in any deliverable |
| **comparator status** | the emitted outcome sentence's own markers (`COMPARATIVE FIT UNEVALUATED`, `INCUMBENT FIT UNEVALUATED`, class 9's "evidenced on this axis alone") | every deliverable that names the far side | removing a marker; inferring fit from silence |
| **architecture authorization** — `authorized` / `authorized-bounded` | **primary authority and carrier**: the `architecture:` block — `authorization` + `authorization_basis` + `architectability_basis` (initialized once at blueprint entry) | blueprint · impl-spec · design-brief · estimate · executive (one sentence) | deriving, upgrading or downgrading it |
| **architecture authorization** — `not-authorized` | **semantic authority**: outcome reachability × the architecture-entry architectability evaluation (selected solution × the frozen active-pack architectability boundary). **Durable sources**: outcome basis → `decisions.md`; architectability basis → `_synthesis/architecture-story.md` **as durable carrier** (§21, §40.3) | executive (both reasons, distinct) · estimate (as the reason for its own applicability) | labelling the synthesis file the source of architectural truth; any deliverable re-evaluating pack architectability |
| **architecture component** | `architecture:` block — `compositions[]`, `record_authority[]`, `relocated_responsibilities[]` | blueprint (all) · impl-spec (build-relevant) · design-brief (surface-touching only) · estimate (as work units) | adding a component; renaming one; merging two |
| **pattern import** | the boundary fragment instance (six channels, derived per component by the architecture layer) | blueprint (all six channels) · impl-spec (operational channels) · estimate (cost/monitoring/recovery channels as work) | declaring an import satisfied; collapsing channels |
| **proof obligation** | `decisions.md# Proof obligations` → carried into `architecture:` `proof_obligations[]` | executive (decision-changing only) · blueprint (all) · impl-spec (translated to work packages + acceptance) · design-brief (UX validations only) · estimate (effort for the work) | re-grading V1–V4; substituting a different method |
| **open architecture choice** | `architecture:` `open_architecture_choices[]` (+ the `U-NNN` it references) | blueprint (all, with `structural?`) · impl-spec (as open work item) · estimate (as uncertainty) | resolving it; hiding it in contingency |
| **implementation task** | **Implementation Specification** (owns its derivation from architecture + approved UX blueprint) | estimate (inventory only, see §26) | architecture-changing tasks; tasks with no architecture or blueprint anchor |
| **UX design constraint** | `_blueprint/ux-blueprint_v<NN>.yaml` (**approved** version) — screens, personas, navigation, `ui_states`, `excluded_from_ui`, `validation` | design-brief (primary) · impl-spec (`screens_to_build`) | inventing a screen, persona or state; re-consolidating screens |
| **effort estimate** | **Estimate** (owns the mapping and the arithmetic; method from `craft/estimation-model.md`) | executive (one investment paragraph at decision altitude) | any other deliverable computing effort |
| **decision economics** | `options.md` S8 + `decisions.md` (+ `_synthesis/` narrative) | executive (attractiveness / funding) · discovery (as-is cost baseline only) | the Estimate deciding attractiveness; merging with implementation effort |
| **volatile value** | the SU row carrying `value · verificado_em · validade`, with its `volatility-register` trigger | every deliverable, stamped | rendering an unstamped or expired value as fact |
| **scope-ownership projection category** | derived render category (§12) — from the `(scope, outcome)` pairs × the `architecture:` block | blueprint (table) · executive (prose) · impl-spec (scope statement) · estimate (priced/not-priced) | inventing a fifth category; turning a category into a state |
| **Domain Knowledge fact** | the owning `RESEARCH` unit under `library/packs/pp/domain-knowledge/` | impl-spec (selective) · design-brief (selective, UX-relevant) | any deliverable pulling DK for richer prose |
| **delivery convention** | the owning `CRAFT` unit | impl-spec · design-brief · estimate (method only) | CRAFT asserting a platform limit or overriding architecture |

---

## 6. Dependency graph

### 6.1 The proposed graph, evaluated

The commission's candidate graph is **not adopted as a read graph**. Two of its edges fail against actual
repository semantics:

| Proposed edge | Verdict | Why |
|---|---|---|
| `Implementation Specification → Claude Design Brief` | **rejected as a read edge** | The authority for screens/personas/navigation/UX states is the **approved UX blueprint**, which is produced in the Decision phase *upstream of both*. Routing the Design Brief through the rendered spec would put a versioned, hand-editable `_render/` file between the brief and its authority (R1 violation) |
| `Implementation Specification → Estimate` | **adopted, narrowed** | *Implementation obligations* are exactly what the spec owns (§5, §17). The Estimate reads its **inventory** — components, obligations, proof work, migration steps, open work items — and nothing else |
| `Decision Model → Architecture Layer` | **adopted** | matches `blueprint-contract.md`'s entry gate |
| `Shared Understanding → Discovery Report` | **adopted** | |
| `Decision Model → Executive Report` | **adopted** | |
| `Architecture Layer → {Blueprint, Impl Spec}` | **adopted** | |

### 6.2 The adopted graph

```text
inputs/ + _capture/            (evidence — never a deliverable's reasoning source)
        ↓
shared-understanding.md        ── AUTHORITY: facts + epistemic states
        ├────────────────────────────────────────────→ (1) Discovery Report
        ↓
options.md                     ── AUTHORITY: option set + emitted outcomes + S8 economics
        ↓
decisions.md  D-NNN            ── AUTHORITY: decision · pairs · conditions · risks ·
        │                                     proof obligations · tripwires
        ├────────────────────────────────────────────→ (2) Executive Report
        ↓
architecture: block            ── AUTHORITY: authorization · experience · components ·
   (approved ux-blueprint)                    imports · proof · open choices
        ├────────────────────────────────────────────→ (3) Architecture Blueprint
        ├────────────────────────────────────────────→ (4) Implementation Specification
        │                                                        │  (inventory only)
ux-blueprint screens/personas  ── AUTHORITY: UX design            ↓
        ├────────────────────────────────────────────→ (5) Claude Design Brief
        └────────────────────────────────────────────→ (6) Estimate ←────────┘

_synthesis/*  — a BOUNDED NARRATIVE PROJECTION of the artefacts above (§25).
                Deliverables may read it for prose. In the `not-authorized` case,
                architecture-story is the DURABLE CARRIER for exactly one
                architecture-entry result whose SEMANTIC AUTHORITY remains the
                architecture-entry gate (§21, §40.3). It is NOT architecture
                authority.
```

**Read edges: 1 deliverable → deliverable** (`(4) → (6)`, inventory-only, same render run).
**Cycles: 0.** Every other edge points strictly downstream.

### 6.3 Two orderings, deliberately distinct

- **Altitude order** (semantic): Architecture Blueprint → Implementation Specification → Claude Design
  Brief. A Design Brief statement may not contradict an architecture-derived implementation obligation.
- **Read order** (mechanical): both the spec and the brief read the architecture and UX blueprint
  directly. Altitude is a **constraint on content**, not a file dependency.

### 6.4 Forbidden edges (binding)

```text
Estimate                  → changes architecture               FORBIDDEN
Estimate                  → settles economic attractiveness    FORBIDDEN
Design Brief              → changes requirements               FORBIDDEN
Design Brief              → selects store / composition        FORBIDDEN
Implementation Spec       → changes architecture                FORBIDDEN
Implementation Spec       → reopens Options                     FORBIDDEN
Executive Report          → source of implementation truth      FORBIDDEN
Any deliverable           → raw evidence to re-settle an upstream fact   FORBIDDEN
Any deliverable           → another deliverable's narrative as authority FORBIDDEN
Discovery Report          → decision, recommendation or architecture     FORBIDDEN
```

### 6.5 The one permitted deliverable→deliverable edge, specified

| Aspect | Rule |
|---|---|
| Direction | Implementation Specification → Estimate |
| Payload | **inventory only**: components to build/configure · implementation obligations · proof work packages · migration/cutover steps · open implementation work items |
| Excluded payload | narrative, rationale, architecture description, acceptance text |
| Additions | **when an Implementation Specification exists**, the Estimate **may not add** a work unit absent from it. A needed-but-absent unit is an **open work item** logged against the spec, not an estimate line. (**Corrected** — the mode-conditional form of this rule is §40.6) |
| Absent spec | where the spec is `not applicable` (§17/§23), **blocked** (§40.5) or not rendered, the Estimate takes **mode B** (§40.6) or is itself not applicable. It never estimates work whose authority it cannot name |
| Ordering | `--all` renders (4) before (6). A lone `/render estimate` with no spec present is legal and resolves its input mode per §40.6 |

---

## 7. Projection contract

For every deliverable: **authority · selection · transformation · forbidden transformation.**

### 7.1 The common forbidden set (all six)

| May not change | Meaning |
|---|---|
| epistemic state | Assumed stays assumed; Unknown stays unknown; Conflicted keeps both sides or neither; Risky keeps its accepted-risk identity; an expired Confirmed renders as a re-verification obligation |
| decision meaning | the emitted outcome sentence is verbatim; the selected solution is as recorded |
| scope | no scope added, dropped, widened or collapsed |
| architecture ownership | who owns what is the architecture's answer, not the deliverable's |
| risk acceptance | an accepted risk is not a mitigated risk |
| proof level | V1–V4 as recorded |
| comparator status | every marker survives |

### 7.2 The common permitted set (all six)

wording · level of detail · ordering · audience language · table↔prose · omission of non-material
content **subject to the deliverable's own survival test** (§35–§38).

---

## 8. Discovery Report model

**Audience**: sponsor + stakeholders. **Altitude**: detailed discovery state. **Phase truth**: pre-decision
by construction, even though it renders after `/decide`.

| Aspect | Definition |
|---|---|
| **Authority** | `shared-understanding.md` (facts + states, all five) · `_capture/evidence-index.md` (sources) · `context.json` (requester, literal request) · `frame.md` / `D-001` (scope framing) · `lens-outputs/*` **only** through `_synthesis/{business-story, as-is}.md` |
| **Selection** | engagement context · **material** Confirmed facts · **material** Assumed with basis and validity · open Unknowns with criticality and who can answer · Conflicts with both sides · accepted/observed Risks · per-perspective findings · surviving tensions · evidence still required · scope framing |
| **Transformation** | narrative reconstruction of the as-is; tables for the data inventory; prose for perspectives; audience language = engagement language; id citations inline; `--html` provenance projection |
| **Forbidden** | the common set (§7.1) **plus**: no Options conclusion · no technology recommendation · **no vendor/product naming** (`.claude/rules/no-tech-mention-before-options.md` — this deliverable is neutral by construction) · no Unknown converted to a finding · no mechanical copy of all SU rows · no transcript |

### 8.1 Materiality rule — which rows survive

A row reaches the Discovery Report if **any** of:

1. it anchors a claim in `business-story.md` or `as-is.md`;
2. it is `Unknown` with `criticidade = Critical`, **or** any `Unknown` that a blocking-set entry needs;
3. it is `Conflicted` and unresolved;
4. it is `Risky`;
5. it is `Assumed` and load-bearing for the problem statement, a volume, a cost baseline or a control;
6. it is `Confirmed` and **expired** (renders as a re-verification obligation, never dropped);
7. a stakeholder concern the council recorded that no other row carries.

Rows failing all seven are **omitted, not summarized**. Omission is silent for Confirmed rows and
**never** silent for the other four states: an omitted `Unknown`/`Conflicted`/`Risky` is a **counted
residual** ("+ N further open items, see `shared-understanding.md`"), so the reader can see that
compression happened.

### 8.2 Sections (target)

context · as-is · processes · data inventory · friction · perspectives & tensions · **open questions
(Unknown)** · **conflicts (Conflicted)** · **risks observed (Risky)** · assumptions in play (Assumed) ·
evidence still required (incl. open blocking criteria) · stakeholders · sources · scope framing.

### 8.3 Completeness

Complete when every surviving row of the seven materiality classes appears **in its own state**, the
residual counts are stated, and no section asserts anything the SU does not carry. **Not** "every section
populated": an engagement with no Conflicted rows renders that section as `nenhum` — a fact, not a gap.

---

## 9. Executive Report model

**Audience**: sponsor / C-level. **Altitude**: decision. **Reads in ~10 minutes.**

| Aspect | Definition |
|---|---|
| **Authority** | `decisions.md` `D-NNN` (**primary**) · `_synthesis/business-story.md` (problem/value) · the `architecture:` block A1/A2/A9 **only** · `_synthesis/financial-story.md` decision-economics half + the Estimate's headline · `_synthesis/risks-and-assumptions.md` |
| **Selection** | what problem/opportunity matters · what we learned that changed the picture · the decision (chosen option, selected solution in plain language, the uncollapsed `(scope, outcome)` pairs) · **why — the justification the decision recorded** · what remains conditional (conditions · preconditions · decision-changing proof obligations · structural open choices) · major architecture **shape** where authorized (2–5 sentences, A1 + A2 + A9 irreversibles) · major risks and obligations · economics at decision altitude · what happens next (tripwires + next actions) |
| **Transformation** | compression to sponsor language; prose over tables except the pairs and the tripwires; one investment paragraph, not a phase table; architecture named, not described |
| **Forbidden** | the common set **plus**: not a shorter Discovery Report (no as-is reconstruction, no data inventory, no perspective-by-perspective walk) · not an Architecture Blueprint (no A3 table, no A5 store detail, no import channels) · not a technical appendix · **no new option comparison** — project the decision's own recorded *why not* lines and nothing else · never converts a condition into a satisfied state |

### 9.1 The rationale rule (I-2 at executive altitude)

The Executive Report reproduces **the justification the decision recorded** (`decisions.md# Justification`
plus the per-alternative *why not* lines). It does **not** explain why an architecture "won". Where the
decision recorded no comparison, the report records none — the absence is honest, not a gap.

### 9.2 Non-omissible content

Conditions · preconditions · the uncollapsed pairs · accepted risks · decision-changing proof obligations
· structural open architecture choices · tripwires. Each is `required` **subject to existence**: absent
upstream ⇒ *not applicable* skip; present upstream ⇒ it renders (§21, **T-D6**).

### 9.3 Completeness

Complete when a sponsor can state, from this document alone: the decision, its scope boundaries, what it
is conditional on, what it costs at decision altitude, what would force a revisit, and what happens next.
An Executive Report with **no architecture section** is complete where no architecture is authorized.

---

## 10. Architecture Blueprint model

**Audience**: solution architect / lead developer / tech lead. **Altitude**: architecture.
**Nature**: the human-readable projection of the **frozen** Step 5 Architecture Layer.

| Aspect | Definition |
|---|---|
| **Authority** | the `architecture:` block (**primary**) · `architecture-templates/architecture-core.md` + the resolved fragments (the **shape**) · `_synthesis/architecture-story.md` (narrative) · `decisions.md` (basis, conditions, proof obligations) · `shared-understanding.md` (validity/state display of the rows the architecture rests on) |
| **Selection** | **all** of A1–A12 as engaged, plus the engaged conditionals, plus one boundary-fragment instance per qualifying component with all six channels. This is the one deliverable that does not compress the architecture |
| **Transformation** | A-section order and headings; tables and (degradable) diagrams per the core's own conditionals; architect-facing precision; the narrative paragraphs from `architecture-story.md` woven around the structured sections |
| **Forbidden** | the common set **plus**: **may not choose** architecture authorization · experience mode · store / record authority · pattern · composition · far-side solution — all six belong to the frozen layer. No scoring. No selection among candidate architectures. No far-side design |

### 10.1 Projection map

| Architecture-layer output | Blueprint projection |
|---|---|
| A1 authorization & scope | §1 — pairs uncollapsed, `authorization`, both bases, PP-owned vs not-designed-here |
| A2 intent | §2 — the requirement each structural choice answers; `forced_by` per escalation |
| A3 context & boundaries | §3 — the mandatory boundary table (every component exactly once) + conditional context picture + conditional sequence |
| A4 surface | §4 — **rendered by the matching experience fragment**; where `experience.mode: none`, `not applicable` with reason. No empty A4, no gap |
| A5 data authority | §5 — per domain; an affirmative empty set renders its rationale verbatim |
| A6 automation & integration | §6 — per stream: mechanism class, guarantee, failure semantics, idempotency basis |
| A7 identity & enforcement | §7 — always in full, headless included |
| A8 environments & release | §8 |
| A9 irreversible & exit | §9 — incl. the conditional *replacement of an existing artefact* (§24) |
| A10 operability | §10 — named operator; an `UNKNOWN` operator is a **structural** open choice, not a risk row |
| A11 economics | §11 — **drivers only**; no prices, no SKUs, no quotas |
| A12 proof & epistemic ledger | §12 — proof obligations (five-part shape, never re-graded) · the Assumed/Unknown/Conflicted/Risky rows the architecture rests on · every volatile value with its stamp · `open_architecture_choices[]` with `structural?` |
| candidate architectures (conditional) | §13 — both rendered, neither chosen, what would settle it (§20) |
| scope ownership (conditional) | §14 — the **four** projection categories (§12) |
| boundary fragments | §15 — N+M instances, six channels each, nothing collapsed |

### 10.2 What the Blueprint sheds

`executive_summary` (→ Executive Report) and `estimation_summary` (→ Estimate) are **removed** as slots
(D-16). The Blueprint may carry a two-sentence orientation paragraph; it does not carry an executive
summary or an effort figure.

### 10.3 Completeness

Complete when every engaged A-section is populated from the recorded architecture, every non-engaged one
carries `not applicable — <reason>`, the N+M fragment invariant holds, and every open architecture choice
is visible with its `structural?` flag. **Open items do not make it incomplete** — they make it honest.

---

## 11. Implementation Specification model

**Audience**: implementation team. **Altitude**: build. **Nature**: *architecture → build obligations and
implementation contracts.*

| Aspect | Definition |
|---|---|
| **Authority** | the `architecture:` block (**primary** — A5/A6/A7/A8/A9/A10/A12 + fragments) · the **approved** `ux-blueprint` (`screens`, `entities`, `personas`, `excluded_from_ui`, `validation`) · `decisions.md` (conditions, preconditions, proof obligations) · **selective** `RESEARCH` units for implementation-grade detail · **selective** `CRAFT` units for delivery conventions |
| **Selection** | components to build/configure · responsibilities per component · interfaces and contracts · data structures at implementation altitude · environment/deployment obligations · security implementation obligations · monitoring · recovery · migration/cutover where applicable · test & proof work packages · acceptance conditions · open implementation questions |
| **Transformation** | architecture facts → build obligations; per-section shape contracts (one row per entity, one block per flow, …); operational language; sequencing constraints expressed as dependencies |
| **Forbidden** | the common set **plus**: **may not re-decide architecture** · may not reopen Options · no pixel-level detail unless the downstream consumer uses it · **may not fabricate implementation detail for an unresolved architecture choice** — that renders as an open work item with its owner and what would settle it |

### 11.1 Derivation rules (replacing D-7, D-8, D-9, D-12)

| Slot | New authority | Replaces |
|---|---|---|
| architecture constraints | the `architecture:` block + `architecture-core.md` sections, **projected not re-derived** | `chosen_architecture` ← removed decision field (D-1) |
| entities / data structures | `architecture:` `record_authority[]` + the approved blueprint's `entities` | architecture narrative alone |
| screens/components | the approved blueprint's `screens` — **conditional on `experience.mode != none`** | required slot with narrative fallback (D-12) |
| flows / integrations | `architecture:` A6 streams + boundary fragments | architecture narrative alone |
| security implementation | A7 + `CRAFT security-craft.md` for artefact **form** only | — |
| **test & proof work** | `proof_obligations[]` (**claim · V-level · method · owner · funded**) → one work package each, plus acceptance conditions; discovery friction may add **scenarios**, never the proof level | `as-is.md# Top friction points` as the source of acceptance work (D-7) |
| **sequencing** | architecture dependencies (A3 boundaries · A8 release routes · A9 fixed-at points · fragment cross-boundary release owner) — **constraints only, no durations** | `financial-story# Build effort` (D-8) |
| **migration & cutover** | A9 *replacement of an existing artefact* + the class-14 outcome sentence + `access_mode` transitions — **conditional** | raw SU `lens=data` Risky rows (D-9) |
| open implementation questions | `open_architecture_choices[]` (non-structural) + implementation-local unknowns | — |

### 11.2 Completeness

**Complete enough for handoff** — not *fully specified*. It is complete when: every architecture-derived
obligation appears; every proof obligation has a work package and an acceptance condition; every open item
names an owner and what would settle it; and nothing is invented for an unresolved choice. Explicit open
work items are **compatible with completeness**.

### 11.3 Structural blocking

The spec's primary authority is the **approved** architecture. A `structural: true` open architecture
choice blocks blueprint **approval** (`blueprint-contract.md` hard rule 5) — therefore the spec is
**blocked**, mechanically, with no new machinery (§20, §41).

---

## 12. Scope-ownership projection semantics (I-3 target)

Four **render/projection categories**. Not states. Not outcome classes. Not epistemic values.

| # | Category | Rendered as | Engaged when | Architecture consequence |
|---:|---|---|---|---|
| **1** | **architected here** | `sim — A4…A12` | the scope carries `authorized` or `authorized-bounded` and the responsibility is PP-owned | full A-sections |
| **2** | **relocated — boundary represented** | `não — uma instância do fragmento de fronteira` | a `relocated_responsibilities[]` entry with a **named owner** (class 3 / class 4) | one boundary fragment instance, six channels; **no far-side design**; markers verbatim |
| **3** | **excluded — destination unevaluated** | `não — sem arquitectura e sem fragmento de fronteira; destino/contraparte não selecionado` | class 6 (or 5/7/14) followed by class 8, where the destination is an **emitted candidate set** | **nothing** — no design, no boundary component, no owner, no inferred fit. `COMPARATIVE FIT UNEVALUATED` verbatim |
| **4** | **not applicable — no architecture authorization** | `não aplicável — sem autorização de arquitectura` | `authorization: not-authorized` for every scope | no architecture at all; the outcome basis + architectability basis carry the meaning (§21) |

**Category 3 is the I-3 resolution.** It is the honest third value C6-B already rendered.

**Where the enumeration lives.** In the **deliverable projection contract** (the Architecture Blueprint
template's scope-ownership section, plus the Executive/Impl-Spec/Estimate scope statements). It is a
render category, so the deliverable layer is its natural home — and `architecture-core.md` stays frozen
and untouched. Adding the third value to that file's angle-bracket column hint remains an **optional**
documentation-only follow-up requiring explicit authorization to touch a frozen file; C6-B proves it is
not needed for correct behaviour.

**Rendering rules.** The table renders where more than one `(scope, outcome)` pair exists. One row per
responsibility. Category 3 rows carry the emitted outcome sentence and **no** owner column value other
than the candidate set as emitted. No category may be inferred from another.

---

## 13. Claude Design Brief model

**Consumer inspected first**, per the commission.

### 13.1 Who reads it, when, and what it must generate

| Question | Answer (from the repository) |
|---|---|
| Who reads it | Claude Design (or a replaceable equivalent) — `audience: claude-design`; `blueprint-contract.md` §*Downstream consumers*; `docs/ARCHITECTURE.md §5.4` |
| At what phase | after `/decide` → `/blueprint` (approved) → `/synthesize` → `/render` |
| What it must generate | high-fidelity mockups of the **already-designed** application: screens, navigation, states, RBAC-conditioned UI, validated platform expressions |
| Does it receive an architecture or an implementation spec | **neither, today** — it receives the *retired branch architecture template* (dead) plus the approved UX blueprint |
| Does it currently include `architecture-core` | **no** — it includes `{{>> architecture-templates/{{chosen_architecture}}.md}}`, a dead dynamic include |

### 13.2 Resolution of Step 5A open question (i)

> Does the Claude Design Brief consume the full architecture core, or a narrower implementation-facing
> projection?

**A narrower projection.** Not the core, and not the whole rendered Implementation Specification either.

Tested against §37's survival test — *could the generated design violate an approved UX / business /
control requirement if this fact disappears?*

| Architecture content | In the brief? | Survival-test verdict |
|---|---|---|
| A1 authorization + authorized scope | **yes** (one paragraph) | YES — a design outside the authorized scope is a violation |
| A3 boundary-table rows a surface **touches** | **yes** (filtered) | YES — a screen reading a component outside platform governance changes trust and error handling |
| A5 `access_mode` consequences that reach the UI (delegation/truncation limits, freshness, virtualized/replicated staleness) | **yes** | YES — a gallery that silently truncates is a control failure |
| A7 identity class + enforcement point + role/permission model | **yes** | YES — RBAC-conditioned UI is a control requirement |
| A12 items that are **design-relevant** (design-blocking Unknowns, accessibility proof obligations, UX-relevant Conflicted rows) | **yes** | YES |
| A2 architecture intent | no | NO — rationale, not a design constraint |
| A6 stream internals (idempotency basis, failure semantics) | **no**, except where a UI state must reflect async status | mostly NO |
| A8 environments / release topology | no | NO |
| A9 irreversible choices / exit cost | no | NO |
| A10 operability / named operator | no | NO |
| A11 economics | no | NO |
| boundary-fragment six channels | no | NO |

**The `architecture_constraints_digest` is a selection, not a new artefact**: named A-sections, filtered
to surface-touching rows, addressed by heading. No new template, no new file, no router.

### 13.3 Contract

| Aspect | Definition |
|---|---|
| **Authority** | the **approved** `ux-blueprint` (**primary**: screens, personas, navigation, `ui_states`, `excluded_from_ui`, `validation`) · `decisions.md# Blueprint bp-v<NN> aprovado` (the approval id) · the `architecture_constraints_digest` (§13.2) · `context.json# brand_guidance` · SU `lens=user` accessibility/language rows · **selective** CRAFT |
| **Selection** | design objective · target users/roles · screen/surface inventory · key journeys · data displayed/edited (with `excluded_from_ui` and its reasons) · state & interaction requirements · permissions affecting UX · validation/error behaviour · loading/empty/success/failure states · responsive & accessibility constraints · design-system / CRAFT inputs · **material** architecture constraints |
| **Transformation** | generator-oriented phrasing; per-screen blocks; inline citations to the owning CRAFT/RESEARCH unit where an expression or control convention is needed |
| **Forbidden** | the common set **plus**: **may not select store, composition, pattern or experience mode** · may not re-consolidate screens (`craft/screen-consolidation-rules.md` ran in `/blueprint`) · may not add a persona, screen or state absent from the approved blueprint · may not change requirements · may not become an Architecture Blueprint copy · **may not preload the Domain Knowledge catalogue** |

### 13.4 Domain Knowledge and CRAFT carriage (replacing D-10)

Today: six units named and characterised inline. Target: **cite on demand, at the point of need.**

| Unit | Legitimate use in the brief |
|---|---|
| `craft/screen-patterns.md` | the screen type and density convention for a screen the blueprint already assigned |
| `craft/powerfx.md` | where the brief must emit or constrain an expression |
| `craft/security-craft.md` | the **form** of the RBAC matrix; never the control's existence or reach |
| `craft/excel-translation.md` | only where an Excel anchor is in the approved blueprint |
| `craft/screen-consolidation-rules.md` | **reference only** (the named contract of `blueprint-contract.md`); its rules already ran |
| `data/query-and-delegation.md` | **RESEARCH** — the authority for what an access path returns; cited where A5's consequence reaches the UI |

The brief carries a short **"where to verify"** pointer list (unit + section) instead of a
characterised catalogue. Fresh pulls are legitimate **only** for a design decision the brief must itself
express (an expression, a control convention, a UI-visible access-path limit) — never for richer prose.

### 13.5 Applicability gate

```text
experience.mode == none                  → Claude Design Brief: NOT APPLICABLE
                                           (deliverable-level skip, logged with reason; NOT a gap)
authorization == not-authorized (all)    → NOT APPLICABLE
no approved ux-blueprint                 → BLOCKED (with the reason: run /blueprint, or a
                                           structural open choice blocks approval)
experience.mode == inherited              → CONDITIONAL — the brief covers only what the
                                           inherited surface lets the solution shape; it never
                                           designs the host's surface
experience.mode in {owned-internal, owned-external} → REQUIRED
```

**No persona list, screen inventory, navigation map or UX state is ever a required slot where
`experience.mode: none`.** All four become conditional on the mode.

### 13.6 Completeness

Complete when every screen in the approved blueprint has its data, actions, states, RBAC visibility and
exclusions; every material architecture constraint that could be violated is present; and nothing is
invented. **`not applicable` is a complete Design Brief** for a headless architecture.

---

## 14. Estimate model

**Audience**: sponsor + procurement. **Nature**: *a calculation and projection over decided scope and
implementation work.*

### 14.1 Inputs owned elsewhere

> **Two input modes.** §14.1 describes **mode A** (implementation estimate). **Mode B** (candidate
> planning estimate) is defined in §40.6 and applies only where architecture approval is blocked by an
> unresolved structural choice. There is no third mode.

| Input | Owner |
|---|---|
| scope | `decisions.md` `(scope, outcome)` pairs |
| components | `architecture:` block, via the Implementation Specification's inventory (mode A) or via the candidate architecture record (mode B) |
| implementation obligations | Implementation Specification |
| proof work | `proof_obligations[]` → the spec's work packages |
| migration effort | the spec's migration & cutover section (authority: A9 + class 14) |
| risk / uncertainty | `decisions.md# Accepted risks` + `open_architecture_choices[]` + SU `Risky`/`Assumed`/`Unknown` |
| entitlement & cost **drivers** | A11 (drivers only) + `economics/licensing-and-cost-drivers.md` |

### 14.2 Estimate-owned logic

work-breakdown mapping (spec inventory → work units) · the effort model
(`craft/estimation-model.md`, **method only**, person-days) · estimate-specific assumptions ·
ranges · contingency treatment · confidence statement.

### 14.3 Contract

| Aspect | Definition |
|---|---|
| **Authority** | itself, for the calculation — it is the **semantic owner**; `aisa-render` is only the **executor** (§40.2, §40.4). The §14.1 owners, for every input |
| **Selection** | only work that materially changes effort, uncertainty or contingency (§38) |
| **Transformation** | inventory → work breakdown → effort bands → phases → range + contingency + confidence; tables |
| **Forbidden** | the common set **plus**: **may not decide whether PP is cheaper** or more attractive · **no live licence prices, SKUs or quotas** · may not substitute `craft/estimation-model.md` for Step 3 S8 comparative economics · **may not hide an architectural Unknown inside contingency** — an `open_architecture_choices[]` entry renders as a named uncertainty line with what would settle it · may not estimate far-side delivery (§18, §19) · may not add a work unit the spec does not carry |

### 14.4 The contingency-honesty rule

Every structural open choice and every decision-changing Unknown that affects effort appears as a
**named** uncertainty line: *the open item · the effort it swings · what would settle it · its `U-NNN`*.
Contingency is a number **over** the named items, never a substitute for them (**T-D4**, **T-D10**).

### 14.5 Completeness

Complete when every work unit in the spec's inventory is either estimated or explicitly excluded with a
reason; every named uncertainty is visible; the confidence statement matches the epistemic state of the
inputs; and no price appears. An Estimate that covers only part of the engagement scope is complete when
it **says which part** (§19).

---

## 15. Epistemic projection

| State | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| **Confirmed** (within validity) | stated as fact, with id | stated as fact | fact + `verificado_em`/`validade` | fact | fact | fact; basis of the band |
| **Confirmed (expired)** | **re-verification obligation** | only if decision-changing | re-verification obligation (A12) | obligation + work item | only if UX-material | uncertainty line |
| **Assumed** | assumed, with basis, validity, validator | **assumed where material to the decision** | assumed, never promoted (A12) | assumed + validation work | assumed where UX-material | assumed; feeds the range |
| **Unknown** | own section, with criticality + who answers | **decision-changing ones only, as open** | `open_architecture_choices[]` entry; never filled | open work item; no fabricated detail | design-blocking ones only | **named uncertainty line** |
| **Conflicted** | conflict rendered, both sides, neither chosen | only if decision-changing; render the conflict | conflict rendered, neither figure carried | no value chosen; proof obligation instead | render the conflict, design no side | no figure; range + named uncertainty |
| **Risky** | risk observed, with consequence | accepted-risk identity + consequence | accepted-risk id (A12) | risk + mitigation obligation | only if UX-material | uncertainty / contingency input, identified |

### 15.1 The binding rule

> **Deliverable brevity cannot upgrade epistemics.**

Three corollaries:
1. An `Unknown` may be **omitted** from a deliverable only where it is immaterial *for that audience*,
   and its omission is counted in a residual line — never rewritten as a fact or an assumption.
2. `Conflicted` renders the conflict **or** omits the value. Choosing a side is prohibited in every
   deliverable, at every altitude, with or without a caveat.
3. An expired `Confirmed` never renders as fact anywhere, including the Executive Report.

---

## 16. Proof-obligation projection

| Deliverable | Carries | Form |
|---|---|---|
| **Discovery Report** | material evidence gaps | question · who can answer · criticality · what resolution would change |
| **Executive Report** | **decision-changing / high-level** obligations only | claim · why it qualifies the decision · owner · funded? |
| **Architecture Blueprint** | **all** architecture proof obligations | the five-part shape: claim · level (V1–V4) · method · owner · funded? |
| **Implementation Specification** | **all**, translated | work package + acceptance condition, one per obligation |
| **Claude Design Brief** | UX/design validations only (accessibility attestation, usability check) | what must be validated · against what |
| **Estimate** | the **effort** for the proof work | work unit + effort + uncertainty |

**No deliverable re-grades V1–V4.** The level is recorded at the decision and carried into the
architecture block; every projection quotes it. Nor may a deliverable change `method`, `owner` or
`funded?`, or mark an obligation satisfied (**T-D11**).

---

## 17. Conditions and preconditions projection

| Condition kind | First authoritative appearance | Must reproduce | May omit if non-material |
|---|---|---|---|
| Outcome condition (class 2's *provided that*) | `options.md` emitted sentence → `decisions.md# Conditions` (verbatim, with owner/funded/by-when) | **Executive** (always where it qualifies the recommendation) · **Arch Blueprint** (A1/A2) · **Impl Spec** (where it gates build) | Discovery · Design Brief · Estimate (unless it changes effort) |
| Precondition (must be true before work starts) | `decisions.md# Preconditions` | **Impl Spec** (always) · **Executive** (as "what must happen first") | Discovery · Design Brief |
| Entitlement / funding condition | `decisions.md# Conditions` + A11 drivers | **Executive** · **Estimate** (as a named input, no price) | Design Brief |
| Control / compliance condition | `decisions.md# Conditions` + A7/A8 | **Executive** · **Arch Blueprint** · **Impl Spec** | Estimate (unless it changes effort) |
| Architecture gate (operator, support, skills, cross-boundary release owner, maturity) | `relocated_responsibilities[].gates_recorded` | **Arch Blueprint** (fragment) · **Impl Spec** | Executive, unless a gate is unsatisfied — then **required** |

### 17.1 Two non-negotiables

- A condition required for the **recommendation** never disappears from the **Executive Report**.
- A condition required to **build** never disappears from the **Implementation Specification**.

### 17.2 The satisfaction rule

No template may convert *condition* into *already satisfied*. A condition becomes satisfied only through
engagement evidence — a `Confirmed` SU row or an `/answer` transition that says so. Absent that, it
renders as a condition with its owner and funding state, `not named` included (**T-D6**).

---

## 18. Economics distinction

```text
Step 3 S8 economics          →  decision economics / option attractiveness
Estimate                     →  implementation effort / delivery projection
```

**Not the same, and not merged.** An implementation estimate can be low while an option is economically
unattractive (licensing, control population, operating tier) — and the reverse.

| Aspect | Decision economics (S8) | Implementation estimate |
|---|---|---|
| Owner | `options.md` S8 + `decisions.md` (+ outcome class 7's mandatory reason) | the Estimate deliverable |
| Question | *is this option worth choosing?* | *how much work is the chosen path?* |
| Denomination | drivers, entitlement classes, funding state, attractiveness | person-days, phases, team mix |
| Method authority | the decision spine + `economics/licensing-and-cost-drivers.md` (drivers) | `craft/estimation-model.md` (**method only**, and explicitly *not valid as comparative economics*) |
| Deliverable home | **Executive Report** | **Estimate** |
| Prohibited | the Estimate asserting attractiveness | the Executive Report deriving a phase plan |

### 18.1 The required synthesis split (D-14)

`financial-story.template.md` currently holds both halves in one artefact and generates the estimate
tables inside a narrative synthesis prompt. Step 6B **splits the content semantically**:

| Content | Target home |
|---|---|
| as-is cost baseline · cost of doing nothing · budget envelope & funding · payback/ROI · financial revision triggers | **decision economics** — synthesis narrative, projected by the **Executive Report** |
| phased build plan · detailed per-phase effort · timeline · effort summary · team by profile · operational impact · recommendations | **implementation estimate** — **semantically owned** by the **Estimate** deliverable and **executed by `aisa-render`** under the estimate template's projection contract, from the spec inventory (mode A) or the candidate architecture record (mode B) + `craft/estimation-model.md` |

**Corrected (§40.5).** The earlier wording left a "one file, two owned halves" option open. It is
withdrawn. Target:

```text
financial synthesis   → decision economics narrative ONLY
Estimate deliverable  → implementation effort calculation and projection
```

**Remove the implementation-estimate calculation from synthesis entirely.** No second synthesis file is
created for implementation effort. Any implementation-effort prose that remains in synthesis after
Step 6B may only be a **reference or projection of an already-produced Estimate** — never the calculation
source, and never the place a figure first appears.

---

## 19. Scope pairs

For `authorized-bounded`, **every** relevant deliverable preserves the split.

| Deliverable | How the split renders |
|---|---|
| **Executive Report** | the uncollapsed pairs, each with its outcome sentence verbatim; one sentence naming what is **not** in PP scope and its category (§12); markers preserved |
| **Architecture Blueprint** | A1 states both sides; the scope-ownership table (§12) carries one row per responsibility; category-2 rows get exactly one boundary fragment with six channels; category-3 rows get **nothing** |
| **Implementation Specification** | PP-owned scope only, stated as such; the far side appears as an **interface/contract obligation** where a boundary component exists, and as **nothing** where the destination is unevaluated |
| **Claude Design Brief** | designs only PP-owned surfaces; a far-side surface is out of scope and named as such |
| **Estimate** | prices **only** PP-owned work. Category-2 far-side work: excluded with the reason (its owner is external); estimated only where the pack's estimation authority explicitly covers it **and** evidence exists. Category-3: **never estimated** |

### 19.1 Rendering and pricing by category

| Category (§12) | Rendered | Estimated |
|---|---|---|
| 1 — architected here | full architecture + spec + design | **yes** |
| 2 — relocated, boundary represented | boundary, owner, imports, gates | **no** for far-side delivery (unless in estimation authority **and** evidenced); **yes** for the PP-side integration obligation |
| 3 — excluded, destination unevaluated | the emitted outcome sentence + the candidate set, verbatim | **no** — and the exclusion is stated, not silent |
| 4 — no authorization | outcome basis + architectability basis | only if the selected implementation is inside this pack's estimation authority (normally **no**) |

**The far side never silently enters PP implementation scope** (**T-D5**).

---

## 20. Class-6 behaviour (mandatory design case)

Case, from the Step 5C class-6 addendum (C6-B):

```text
S → class 2 → PP architecture authorized (independently emitted pair)
R → class 6 → class 8, destination UNEVALUATED
```

| Deliverable | Required behaviour |
|---|---|
| **Discovery Report** | unaffected — the evidence for both scopes, in its own states |
| **Executive Report** | states that PP is **excluded for R** (sentence verbatim, including *"It may remain the correct answer for `<the surrounding scope>`"*), that R's destination is an **emitted candidate set with comparative fit UNEVALUATED**, and that S proceeds. **No** inference about which candidate is better; **no** implication that R's exclusion weakens S |
| **Architecture Blueprint** | architects **S only**. R appears **once**, in the scope-ownership table, as **category 3**: no boundary component, no owner, no imports, no gates. Zero far-side design |
| **Implementation Specification** | **does not specify R's external implementation** — no interface, no contract, no migration, no cutover to an unnamed counterparty. S's spec is complete on its own; where S must eventually exchange with R's destination, that is an **open item** naming the unselected destination |
| **Claude Design Brief** | designs **S only**. No screen, persona or journey for R |
| **Estimate** | estimates **S only**. R is listed as **excluded from this estimate — destination unevaluated**. **No** allowance, no placeholder, no contingency band for an unknown external implementation |

**No reverse inference in any direction**: R's exclusion authorizes nothing about S (C6-A proved the
converse — class 6 alone does **not** authorize the surrounding scope), and S's architecture says nothing
about R's fit. Both directions are exercised in the fixture set (§30: C6-B, plus a C6-A-shaped case).

---

## 21. I-1 resolution — durable carriage of `not-authorized`

### 21.1 The problem

`architecture.authorization: not-authorized` is a legal contract value, but `blueprint-contract.md`'s
entry gate produces **no blueprint artefact** in that case, so the authoritative pair —

```text
outcome basis            (the emitted outcome sentence, verbatim)
+
architectability basis   (why this pack cannot architect the selected solution)
```

— has no structured durable home. Step 5C found it surviving in `_synthesis/architecture-story.md`,
`render-log.md` and skill output, read correctly and never re-derived, and classified it as a
documentation-level observation.

### 21.2 Candidate owners evaluated

| Candidate | Verdict |
|---|---|
| a new `architecture:` artefact / empty blueprint | **rejected** — the commission forbids it, and it would be an artefact whose only content is the absence of content |
| `decisions.md` | **partial** — it already owns the **outcome basis** verbatim and durably. It must **never** own the architectability basis: `/decide` is explicitly forbidden from emitting `architectability_basis` |
| `_blueprint/blueprint-log.md` | structurally attractive (append-only, written by the gate that computes the pair) but requires editing `aisa-blueprint` — **frozen Step 5 runtime**. Rejected on the freeze |
| `render-log.md` | **rejected** — per-run audit, not a durable engagement record |
| `_synthesis/architecture-story.md` | **adopted as durable carrier only** — never as semantic authority; see §21.3 and §40.3 |

### 21.3 The adopted ownership model (smallest) — **corrected, §40.3**

**Semantic authority and durable carriage are different things, and this resolution separates them.**

| Half | **Semantic owner** | **Durable carrier** | Change required |
|---|---|---|---|
| **outcome basis** | the Options layer that emitted the outcome sentence | `decisions.md# (Scope, outcome) pairs — UNCOLLAPSED` — verbatim, already durable | **none** |
| **architectability basis** | **the architecture-entry gate rule**: selected solution × the frozen active-pack architectability boundary (`architecture-templates/README.md`) | `_synthesis/architecture-story.md` §*Authorized scope and outcome basis* — **durable carrier only** | two documentation sentences (§21.4) |

**`_synthesis/architecture-story.md` is not the semantic authority for `architectability_basis`.** It is
the durable carrier of an architecture-entry **result** in the one case where no architecture artefact
exists to hold it. Concretely, the carrier:

- does **not** own the rule;
- may **not** change the wording's meaning;
- may **not** widen or narrow the active pack's architecture authority;
- may **not** introduce a new basis;
- must produce a result **reproducible** from the already-recorded selected solution × the frozen
  architectability boundary.

Downstream deliverables read it **as the durable carrier of an architecture-entry result**, not as a
source of architectural truth. **This is the only such carriage exception, and it does not generalize to
any other architecture field.**

### 21.4 The two documentation changes (Step 6B)

1. **`library/kernel/blueprint-contract.md`** — §*Entry gate*, one sentence: *where the entry gate yields
   `not-authorized`, no blueprint version is produced; the outcome basis remains in `decisions.md`, and
   the architectability basis — whose semantic owner is this entry gate's own rule — is durably carried in
   `_synthesis/architecture-story.md` §Authorized scope and outcome basis, which downstream deliverables
   read as that carrier.* This is exactly the bounded repair Step 5C §25 item 3 recommended, and it
   modifies no Step 5 architecture runtime.
2. **`library/kernel/synthesis-templates/architecture-story.template.md`** — mark that section as the
   **durable carrier** (never the semantic owner), and state that the architectability basis is a
   reproducible evaluation of the pack's frozen architectability boundary against the recorded selected
   solution, never a fresh judgement and never re-scoped.

**No new artefact. No new state machine. No new field vocabulary. No empty blueprint. `aisa-blueprint`
untouched.**

### 21.5 Downstream reading

| Deliverable | Reads | Renders |
|---|---|---|
| Executive Report | both halves | the decision **plus** why no PP architecture exists, two reasons distinct, neither labelled *Decision Blocked* |
| Architecture Blueprint | — | **not produced** (`not applicable`, logged as a skip) |
| Implementation Specification | — | **not produced**, unless another scope carries a PP authorization |
| Claude Design Brief | — | **not produced** |
| Estimate | both halves | either the work inside this pack's estimation authority, or `not applicable` with the reason |

---

## 22. I-2 resolution — remove the comparative invitation

### 22.1 Target semantics

| Remove | Replace with |
|---|---|
| *"why it won over alternatives"* | *"the justification the decision recorded"* |
| any instruction inviting a fresh comparison, ranking or superiority claim in any template | project existing comparison **evidence** only — the decision's own justification and its per-alternative *why not* lines, and the frozen `_simulation/counterfactuals/` where cited |

**Deliverables may project existing comparison evidence. They may not create a fresh comparison.**

### 22.2 Exact locations to change in Step 6B

| File | Location | Current | Target |
|---|---|---|---|
| `library/kernel/synthesis-templates/architecture-story.template.md` | §*Chosen architecture*, line 34 | *"and why it won over alternatives"* | *"and the justification the decision recorded (`decisions.md# D-NNN — Justification`), reproduced verbatim in substance. Create no new comparison."* |
| `library/packs/pp/deliverable-templates/executive-report.template.md` | `alternatives_summary` slot + §7 | `decisions.md# D-NNN — Alternatives considered` (unconstrained) | same source, plus the explicit constraint: *project the recorded per-alternative "why not" lines; add no new comparison and no ranking* |
| `library/packs/pp/deliverable-templates/executive-report.template.md` | `decision_options: options.md` (whole file) + §6 | whole-file slot | **narrow** to the option **names + classes** as recorded, or drop the section in favour of §7; a whole-file read of `options.md` at executive altitude invites re-staging the comparison |
| `library/packs/pp/deliverable-templates/solution-blueprint.template.md` | `alternatives_considered` + §7 | architecture-altitude alternatives section | **remove** — the comparison is the Executive Report's projection, at decision altitude. The Blueprint keeps only A1's authorization basis |
| `library/packs/pp/deliverable-templates/estimate.template.md` | §10 *Recommendations* | free-form strategic recommendations from the risks story | constrain: delivery recommendations only; **no** option or economic-attractiveness claim |

### 22.3 Non-goal

Nothing in this resolution removes the ability to state a comparator's **status** (`COMPARATIVE FIT
UNEVALUATED`, `INCUMBENT FIT UNEVALUATED`, class 9's single-axis evidence). Those are recorded facts and
they render verbatim.

---

## 23. Non-authorized architecture behaviour

Case: **a decision exists** and **PP architecture is not authorized for any scope**.

| Deliverable | Behaviour |
|---|---|
| **Discovery Report** | **required, unchanged.** Discovery state is independent of the architecture outcome |
| **Executive Report** | **required.** Communicates the decision, the selected solution in plain language, the pairs, conditions, risks, economics at decision altitude, and next actions — **plus** the two distinct reasons no PP architecture exists (§21). Never labels a positive non-PP outcome as a failure or as *Decision Blocked* |
| **Architecture Blueprint** | **not applicable.** Not produced. Logged as a skip with the reason. **No empty architecture deliverable, no placeholder A-sections, no "architecture: none" document** |
| **Implementation Specification** | **not applicable**, unless another scope carries a PP authorization — then produced for that scope only |
| **Claude Design Brief** | **not applicable.** Not produced |
| **Estimate** | **conditional.** Produced only where the selected implementation is inside this pack's estimation authority **and** evidence exists (`craft/estimation-model.md` carries bands for building on **this** platform only). Otherwise `not applicable` with the reason — *this pack has no estimation basis for the selected solution class*. **Never** a comparative or placeholder number |

**Anti-requirement**: no deliverable may infer anything about the selected non-PP solution's quality,
cost or fit from the absence of a PP architecture (Step 5C N1–N3 hold at the deliverable boundary too).

---

## 24. Architecture replacement / migration boundary

Resolves Step 5A open question (ii). **Both** — split by altitude. **No separate migration deliverable.**

| Owner | Content |
|---|---|
| **Architecture Blueprint** (A9 *replacement of an existing artefact*, conditional) | which existing authority/component is replaced · the coexistence boundary (what runs in parallel, and which side holds authority while both exist) · the transition architecture (dual-write, read-through, freeze, shadow) · the cutover dependency **where it is architectural** (an irreversible graduation, a residency binding, a release-route dependency) |
| **Implementation Specification** (migration & cutover, conditional) | migration steps · conversion procedure · sequencing and tasks · data cleanup · detailed cutover execution · rollback procedure |

### 24.1 The boundary test

> Would a different implementation choice here **change the architecture**, or only change **how the
> transition is executed**?

Changes the architecture ⇒ Blueprint (A9). Changes only execution ⇒ Implementation Specification.

### 24.2 Consequences

- `architecture-core.md`'s A9 conditional stays exactly as frozen. **No Step 5 change.**
- `implementation-spec`'s `migration_notes` slot is **re-sourced** (D-9): from A9 + the class-14 outcome
  sentence + `record_authority[].access_mode` transitions — **not** from raw SU `lens=data` Risky rows.
- The Estimate reads migration effort from the spec's migration section (§14.1), never from A9 directly.
- Engagement risk rows about historical data remain visible through the normal epistemic projection
  (§15), not as the source of the migration plan.

---

## 25. Template, synthesis and render responsibilities

### 25.1 Target principle

```text
synthesis            → creates bounded narrative from authoritative artefacts
deliverable template → determines projection structure AND declares the permitted transformations
render               → assembles validated slots AND executes the declared transformations
```

> **Render executes a projection contract; it does not reason beyond that contract.**

### 25.2 The boundary, per layer — **corrected, §40.1–§40.2**

| Layer | Owns | May do | May **not** do |
|---|---|---|---|
| **Synthesis** (`library/kernel/synthesis-templates/`, `aisa-synthesize`) | bounded narrative per topic, from named authoritative sources | narrate · compress · order · cite ids · produce bounded narrative projections · refuse to write where sources are thin | decide · compare afresh · select an interpretation · re-grade epistemics · pull Domain Knowledge for richer prose · **compute the implementation estimate** (§18.1, §40.5) |
| **Deliverable template** (`library/packs/pp/deliverable-templates/`) | projection semantics · allowed transformations · source contract · selection/materiality · structure · applicability | declare what to select, how to shape it, and **which projection transformations are permitted** | **execute** anything itself · reason · settle an upstream value · re-source a fact from raw evidence · include another deliverable's narrative |
| **Render / deliverable execution** (`library/kernel/render-contract.md`, `aisa-render`) | slot resolution order · the fixed architecture include · fragment iteration (0..1 experience, N+M boundary) · versioning · gap classification · applicability skips · **execution of the transformations the active contract declares** | assemble · validate · log · fail loud · **execute ONLY the projection transformations explicitly declared by the active deliverable contract** — including the deterministic, bounded derivations required by the Implementation Specification, the Claude Design Brief and the Estimate | create new upstream facts · choose an option · choose architecture · change scope · resolve an Unknown · promote epistemics · invent work · re-source evidence · create a comparator claim |

**No new engine and no new skill.** The executor is the existing `aisa-render`.

### 25.3 Where transformation belongs — the one deliberate relocation

Today the **implementation estimate calculation** lives in the synthesis layer
(`financial-story.template.md`), and the Estimate template is a passthrough (D-13). Target: the
**Estimate deliverable becomes the semantic owner** of the calculation, and **`aisa-render` executes it**
under the estimate template's declared projection contract (§40.4). Synthesis keeps the
**decision-economics narrative** and computes no effort figure.

This is the only transformation relocation Step 6B makes. Everything else stays in its current layer.

### 25.4 Not three reasoners

Exactly one layer is the **semantic owner** of a bounded derivation per information class: synthesis
narrates; the Implementation Specification owns the derivation of build obligations; the Estimate owns the
derivation of effort; the Claude Design Brief owns the derivation of generator-oriented screen blocks. In
all three deliverable cases the **executor** is `aisa-render`, acting strictly inside the declared
contract. **No layer derives what another already derived** (R3), and no derivation settles or changes
upstream meaning (§40.1).

---

## 26. Legacy-vocabulary migration disposition

Sweep executed over all deliverable templates, synthesis templates, kernel contracts, render/synthesis
skills, `pack.yaml` and the docs. `library/packs/pp-backup/` (pre-Step-3 snapshot) and
`.claude/tests/*` (which assert the vocabulary's **absence**) are excluded.

| Token | Location | Disposition |
|---|---|---|
| `chosen_architecture` (required slot) | `solution-blueprint`, `implementation-spec`, `claude-design-brief` | **REMOVE.** Replace with the fixed `architecture-core.md` include + `architecture_block` (blueprint), the projected constraint sections (spec), and `architecture_constraints_digest` (design brief) |
| `chosen_architecture` (slot source `decisions.md# D-NNN — Branch (if technology)`) | same three | **REMOVE.** The field no longer exists in `/decide` |
| `{{>> architecture-templates/{{chosen_architecture}}.md}}` (dynamic include) | `solution-blueprint` §2, `claude-design-brief` §1 | **REPLACE** with the fixed include `{{>> architecture-templates/architecture-core.md}}` (blueprint) / **REMOVE** entirely (design brief — it receives the narrow digest, §13) |
| `sub_templates: architecture-templates/{{chosen_architecture}}.md` (frontmatter) | `solution-blueprint`, `claude-design-brief` | **REPLACE** / **REMOVE**, as above |
| `sharepoint-first` · `dataverse-first` · `hybrid` (as branch ids) | **zero occurrences** in any runtime deliverable or synthesis template | **no action.** Present only in `architecture-templates/README.md` (deliberate retirement record), `pp-backup/`, tests (absence assertions) and domain knowledge (where `hybrid` is an **outcome-class / composition** term, not a branch id — **do not touch**) |
| old scored-tree terminology (`R0`–`R6`, branch scoring, top-N) | **zero occurrences** in runtime deliverable/synthesis templates | no action |
| architecture **outcome-selection** language | none in deliverable templates | no action |
| *"why it won over alternatives"* | `architecture-story.template.md` line 34 | **REWORD** (§22.2) |
| implicit mandatory surface — `canvas_app_pages`, `page_navigation_map`, `persona_users`, `ux_requirements` as `required` | `claude-design-brief` | **MAKE CONDITIONAL** on `experience.mode != none` (§13.5) |
| implicit mandatory surface — `screens_to_build` as `required` with narrative fallback | `implementation-spec` | **MAKE CONDITIONAL** on `experience.mode != none`; source = approved UX blueprint only |
| implicit mandatory surface — "Canvas App" in the design brief's own prose | `claude-design-brief` header + §3 | **RE-WORD** to the surface the architecture actually recorded (`experience.primary_surface`); vendor naming stays legitimate, the **assumption** does not |
| `applies_to: [technology]` | `pack.yaml` (3 deliverables) | **REPLACE** with the authorization discriminator (§28) |
| `Branch (if technology)` in the **options artefact** | `.claude/agents/chairman.md` §*Options → options.md* | **OUT OF STEP 6B SCOPE** — it is a council-artefact field, owned by the Options line. Recorded here because `executive-report` reads `options.md`. Disposition: **flag for the owning line**; Step 6B mitigates by narrowing the executive's `options.md` read (§22.2) so the field is never projected |
| `{{chosen_architecture}}` / `architecture-templates/<chosen>.md` in prose | `docs/ARCHITECTURE.md` §5.3 + §5 table + `docs/PACK_AUTHORING.md` §113 | **UPDATE (documentation)** in Step 6B's doc pass; no runtime effect |
| `chosen_architecture` in the docs' slot lists | `docs/ARCHITECTURE.md` §5 table, §378 | **UPDATE (documentation)** |

**Runtime tokens to remove: 9 occurrences across 3 deliverable templates + 1 synthesis phrase +
1 manifest discriminator.** No edit performed in Step 6A.

---

## 27. Deliverable-specific architecture applicability

`required` · `conditional` · `not applicable` · `blocked`.

| Situation | Discovery | Executive | Architecture Blueprint | Implementation Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| **PP authorized** | required | required | required | required | **conditional** ¹ | **conditional** ² |
| **PP authorized-bounded** | required | required | required (PP side only) | required (PP side only) | **conditional** ¹ | **conditional** ² ³ |
| **PP not-authorized** | required | required | not applicable | **conditional** ⁴ | not applicable | **conditional** ⁵ |
| **Decision blocked** | required | required | not applicable | not applicable | not applicable | not applicable ⁶ |
| **Headless PP** | required | required | required | required | **not applicable** | **conditional** ² |
| **Multiple architectures open** | required | required | **required** — candidate architectures rendered, neither chosen ⁷ | **blocked** ⁸ | **blocked** ⁸ ⁹ — **no exception** | **conditional** ¹⁰ — under the candidate-estimate rule (§40.6) |

**Ambiguous cells explained**

1. **Design Brief, authorized/bounded** — `required` where `experience.mode ∈ {owned-internal,
   owned-external}`; `conditional` (narrowed to what the solution shapes) where `inherited`;
   `not applicable` where `none`. Also `blocked` where no **approved** UX blueprint exists.
2. **Estimate, authorized** — `mandatory: false` in the manifest today. It is `required` in practice once
   an authorized PP scope exists and the spec has an inventory; `conditional` because the pack's
   estimation authority is platform-scoped: work outside it is excluded with a reason, never guessed.
3. **Estimate, bounded** — PP side only. Far-side delivery is excluded unless explicitly inside estimation
   authority **and** evidenced (§19.1).
4. **Impl Spec, not-authorized** — `not applicable` for the non-authorized scope; **produced** for any
   other scope that does carry a PP authorization. With no such scope: not produced.
5. **Estimate, not-authorized** — produced only if the selected implementation is inside this pack's
   estimation authority; otherwise `not applicable` with the reason (§23).
6. **Estimate, decision blocked** — `not applicable`. There is no decided scope to calculate over. The
   **evidence task** (its owner, form and cost of not resolving) belongs to the Executive Report's *what
   happens next* and the Discovery Report's *evidence still required* — not to the Estimate.
7. **Blueprint, multiple architectures** — renders **both** candidates via A12's *candidate architectures*
   conditional, states what would settle the choice, and chooses neither. No scoring.
8. **Blocked, mechanically** — a `structural: true` open architecture choice blocks blueprint
   **approval** (`blueprint-contract.md` hard rule 5), and both the spec and the brief require the
   **approved** blueprint. **No new mechanism is introduced**; the block is a consequence of existing rules.
9. **Design Brief, multiple architectures — BLOCKED, with no exception** (**corrected, §40.5**). The
   earlier materiality exception is **withdrawn**. The chain is mechanical and frozen:
   `structural: true` → blueprint approval blocked → no approved UX blueprint → the Design Brief's
   required source is absent → **blocked**. No partial approval, no UX-only approval, no materiality
   override — each would be new workflow semantics. If future evidence shows partial approval is needed,
   that is a separate design question, not Step 6A.
10. **Estimate, multiple architectures** — `conditional` under the **mode B candidate planning estimate**
    rule (§40.6): either not produced, or one **separately labelled** estimate per candidate. **Never**
    one blended figure, **never** a selected candidate, **never** spec-level detail. Each candidate's
    figure is labelled with its candidate id and its lower-confidence marker.

---

## 28. Template source contract

Per deliverable: **required** upstream · **conditional** upstream · **forbidden** direct sources.
Binding for Step 6B frontmatter.

### 28.1 Discovery Report

```text
required:
  shared-understanding.md            (all five states, materiality-filtered)
  context.json                       (requester, literal request)
  _synthesis/business-story.md
  _synthesis/as-is.md
conditional:
  _synthesis/risks-and-assumptions.md   (assumptions / risks / critical unknowns)
  _capture/evidence-index.md            (sources analysed, where capture ran)
  frame.md · decisions.md# D-001        (scope framing, where framing happened)
forbidden:
  decisions.md# D-NNN (decision, recommendation, architecture)   — post-decision content
  the architecture: block · architecture-templates/*             — no architecture at all
  any Domain Knowledge unit                                      — and no vendor/product naming
  options.md                                                     — no option conclusions
```

### 28.2 Executive Report

```text
required:
  decisions.md# D-NNN   (pairs UNCOLLAPSED · selected solution · conditions ·
                         preconditions · proof obligations · accepted risks ·
                         justification · alternatives "why not" · tripwires ·
                         sponsor confirmation)
  _synthesis/business-story.md
  _synthesis/risks-and-assumptions.md
conditional:
  architecture: block A1/A2/A9        (where an authorization exists — shape only)
  _synthesis/architecture-story.md    (narrative; and the I-1 carriage where not-authorized)
  decision-economics narrative        (attractiveness, envelope, funding, payback)
  the Estimate's headline             (one investment paragraph, where an estimate exists)
  shared-understanding.md             (validity/state display of decision-changing rows)
forbidden:
  options.md as a whole-file read     (invites re-staged comparison — §22.2)
  raw evidence / inputs / _capture    (nothing is re-settled here)
  Domain Knowledge units              (none, at any altitude)
  CRAFT units                         (none)
  architecture-core.md A3–A8, A10–A12 (architecture detail below decision altitude)
```

### 28.3 Architecture Blueprint

```text
required:
  architecture: block                              (the record)
  architecture-templates/architecture-core.md      (the fixed shape)
  the resolved fragments                            (0..1 experience · N+M boundary)
  _synthesis/architecture-story.md                 (narrative)
conditional:
  decisions.md# D-NNN                (basis · conditions · proof obligations · tripwires)
  shared-understanding.md            (validity / state display, volatile stamps)
forbidden:
  raw evidence for re-reasoning      (anything already settled upstream)
  all Domain Knowledge preloaded     (the architecture layer already pulled selectively;
                                      the Blueprint cites, it does not re-pull)
  _synthesis/financial-story.md      (no effort or cost figure here — §10.2)
  another deliverable's narrative
```

### 28.4 Implementation Specification

```text
required:
  architecture: block                (record_authority · compositions ·
                                      relocated_responsibilities · proof_obligations ·
                                      open_architecture_choices)
  architecture-templates/architecture-core.md + fragments   (A5–A10 projection targets)
  decisions.md# D-NNN               (conditions · preconditions · proof obligations)
conditional:
  _blueprint/ux-blueprint_v<approved>.yaml   (screens/entities — where experience.mode != none)
  A9 replacement conditional + class-14 outcome (migration & cutover)
  selective RESEARCH units          (implementation-grade detail, at the point of need)
  selective CRAFT units             (delivery conventions, artefact form)
  _synthesis/architecture-story.md  (narrative glue)
forbidden:
  raw SU rows as the source of a migration plan       (D-9)
  _synthesis/as-is.md as the source of acceptance work (D-7 — scenarios only, never proof level)
  _synthesis/financial-story.md as the source of sequencing (D-8)
  options.md                                           (Options is closed)
  the whole Domain Knowledge catalogue
```

### 28.5 Claude Design Brief

```text
required:
  _blueprint/ux-blueprint_v<approved>.yaml   (screens · personas · navigation ·
                                              ui_states · excluded_from_ui · validation)
  decisions.md# Blueprint bp-v<NN> aprovado  (the approval id)
conditional:
  architecture_constraints_digest    (A1 scope · A3 rows a surface touches ·
                                      A5 UI-visible access-mode consequences ·
                                      A7 identity/enforcement/roles ·
                                      A12 design-relevant items)      — §13.2
  context.json# brand_guidance
  shared-understanding.md# lens=user (accessibility / language rows)
  selective CRAFT                    (screen-patterns · powerfx · security-craft form ·
                                      excel-translation where an anchor exists)
  data/query-and-delegation.md       (RESEARCH — cited where A5 reaches the UI)
forbidden:
  architecture-templates/architecture-core.md in full       (§13.2)
  the characterised Domain Knowledge table                  (D-10 — cite on demand instead)
  decisions.md architecture/economic content
  _synthesis/financial-story.md
  raw evidence
  any invented persona, screen, journey or state
```

### 28.6 Estimate

**Two input modes, and no third** (**corrected, §40.6**):

```text
MODE A — implementation estimate
required:
  the Implementation Specification's inventory   (components · obligations ·
                                                  proof work · migration steps ·
                                                  open work items)          — §6.5

MODE B — candidate planning estimate
required:
  candidate architecture record(s)               (per candidate, from A12's
                                                  candidate-architectures conditional)
  candidate-specific KNOWN obligations           (configuration/build · proof ·
                                                  migration already known)

BOTH modes require:
  craft/estimation-model.md                      (METHOD only, person-days)
  decisions.md# D-NNN                            (scope · pairs · accepted risks ·
                                                  conditions that change effort)

Neither basis present ⇒ the Estimate is blocked or not applicable, as appropriate.
```

```text
conditional:
  architecture: block                (mode B's component authority;
                                      open_architecture_choices as named uncertainty)
  A11 drivers + economics/licensing-and-cost-drivers.md   (DRIVERS only, no prices)
  _synthesis/risks-and-assumptions.md
forbidden:
  live licence prices · SKUs · quotas as cost facts · platform rate cards
  S8 comparative economics as an estimate input or output   (§18)
  craft/estimation-model.md used comparatively              (its own §0 banner)
  raw evidence
  mode A: adding a work unit absent from the Specification              (§40.6)
  mode B: adding a work unit absent from the candidate architecture's
          known components/obligations                                  (§40.6)
  mode B: fabricating implementation tasks, screen-level work, or an
          unevaluated far side                                          (§40.6)
  blending candidates into one figure                                   (§40.6)
  any architecture change                                   (§6.4)
```

---

## 29. Selective Domain Knowledge and CRAFT in deliverables

### 29.1 Domain Knowledge

**Most deliverables need none.** The architecture layer already consumed it (median 1 pull per material
section, max 2, zero catalogue scans — Step 5C).

| Deliverable | Fresh DK pull legitimate? | When |
|---|---|---|
| Discovery Report | **never** | it is technology-neutral by construction |
| Executive Report | **never** | decision altitude; the decision already carries what matters |
| Architecture Blueprint | **no fresh pulls** | it cites the units the architecture already used; it does not re-open them |
| Implementation Specification | **yes, selectively** | for implementation-grade detail the architecture correctly left at architecture altitude: a mechanism's configuration surface, an access path's implementation consequence, a control's implementation form. One unit per obligation, at the point of need |
| Claude Design Brief | **yes, narrowly** | where a UI-visible platform boundary must be expressed (`data/query-and-delegation.md`) |
| Estimate | **drivers only** | `economics/licensing-and-cost-drivers.md` for cost **drivers**; never for prices |

**Prohibited in every deliverable**: pulling a unit to make prose richer; preloading a bundle; naming and
characterising units the deliverable does not use (D-10); a catalogue scan.

**Prefer upstream derived facts.** If the architecture already stated the consequence, project it.

### 29.2 CRAFT

| Deliverable | CRAFT |
|---|---|
| **Discovery Report** | **none** |
| **Executive Report** | **none** |
| **Architecture Blueprint** | only already-shaped architecture detail; **no new CRAFT pulls** |
| **Implementation Specification** | **yes, selectively** — `delivery-conventions.md`, `flow-craft.md`, `sql-delivery-conventions.md`, `security-craft.md` (artefact form), `anonymization.md` where a masking obligation exists |
| **Claude Design Brief** | **yes, selectively** — `screen-patterns.md`, `powerfx.md`, `security-craft.md` (matrix form), `excel-translation.md` where an anchor exists; `screen-consolidation-rules.md` **by reference only** |
| **Estimate** | `craft/estimation-model.md` **as estimation method only** |

**CRAFT never overrides RESEARCH or architecture.** It shapes the *form* of an artefact, never the
existence or reach of a platform capability or control. Where a limit is needed, the owning RESEARCH unit
is cited.

---

## 30. Render-gap behaviour

### 30.1 Reuse, do not duplicate

The four Step 5 classes are **reused unchanged in semantics**. No second taxonomy.

| Class | Trigger (deliverable layer) | Behaviour |
|---|---|---|
| **not applicable** | the section's or the **deliverable's** trigger does not hold | omit / do not produce; log a **skip** with the reason to `render-log.md`. **Not a gap** |
| **optional** | an optional section with no content | omit |
| **open work item** *(label generalized)* | a required section that **owned work** can still resolve | render the open item with **its owner** and what would settle it; log to `render-gaps.md`. **Not** decision-blocking |
| **decision-blocking** | no architecture authorization for any scope, or the decision itself forbids one | render nothing architectural; render the emitted outcome sentence (+ the architectability basis) instead |

### 30.2 The one change: a label, not a class

Class 3 is currently labelled *architecture work item*. Step 6B generalizes the **label** to **open work
item** and relies on the `owner` value the class already requires:

```text
owner ∈ { architecture | implementation | design | estimate | evidence }
```

Semantics, trigger and behaviour are unchanged. **No fifth class. No parallel taxonomy.**

### 30.3 Worked mappings

| Case | Class | Owner |
|---|---|---|
| Headless Design Brief | **not applicable** (deliverable-level) | — |
| Missing optional appendix | **optional** | — |
| Unresolved implementation naming (entity, flow, connection) | **open work item** | implementation |
| Unresolved decision-critical requirement | **decision-blocking** | — |
| Structural open architecture choice | **open work item** (architecture) **and** blueprint approval blocked ⇒ spec/brief **blocked** | architecture |
| `experience.mode: none` ⇒ A4 | **not applicable** | — |
| Class-6 destination unevaluated in the Estimate | **not applicable**, with the exclusion stated | — |
| A required Executive condition present upstream but unresolved in the render | **open work item** (never omitted) | evidence |

### 30.4 Deliverable-level skips

A deliverable that is `not applicable` for the situation (§27) is a **skip**, logged in `render-log.md`
with the reason, and **never** written to `render-gaps.md`. `render-gaps.md` remains the file that
screams; skips must not dilute it.

---

## 31. Deliverable completeness

Completeness is defined **independently per deliverable**, and never as *every section populated*.

> **Completeness = the correct projection for the current epistemic and architecture state.**
> Not visual fullness.

| Deliverable | Complete when |
|---|---|
| **Discovery Report** | every surviving materiality-class row appears **in its own state**; residual counts stated; nothing asserted that the SU does not carry. Empty Conflicted section = `nenhum`, not a gap |
| **Executive Report** | the decision, its scope boundaries, its conditions, its material risks, its decision-altitude economics, and the next actions are all present and correct. **No architecture section, where none is authorized** |
| **Architecture Blueprint** | every engaged A-section populated from the record; every non-engaged one `not applicable` with a reason; N+M fragment invariant holds; every open architecture choice visible with `structural?`. **Open choices do not make it incomplete** |
| **Implementation Specification** | **complete enough for handoff**: every architecture-derived obligation present; every proof obligation has a work package + acceptance condition; every open item has an owner and a resolver. **Explicit implementation work items are compatible with completeness** |
| **Claude Design Brief** | every approved screen fully specified; every material architecture constraint present; nothing invented. **`not applicable` is complete** for headless |
| **Estimate** | every spec inventory unit estimated or explicitly excluded with a reason; every named uncertainty visible; confidence matches the inputs' epistemic state; no price present. **Partial scope is complete when it says which part** |

---

## 32. No copy-all strategy — materiality and survival tests

Rejected:

```text
SU            → copy everything into Discovery
decision      → copy everything into Executive
architecture  → copy A1–A12 verbatim into every downstream deliverable
```

**Compress repetition. Never compress decision coverage.**

### 32.1 Executive compression survival test

> Could an executive misunderstand **the decision**, **its conditions**, **its material risk** or **its
> required next action** if this fact disappears?

**YES ⇒ keep.** **NO ⇒ omit, or push to a technical deliverable.**

Always fails the test (therefore always kept): the uncollapsed pairs · conditions · preconditions ·
accepted risks · decision-changing proof obligations · structural open choices · tripwires · the
architectability basis where no architecture exists.

Always passes (therefore omitted): A3 boundary table · A5 store internals · A6 idempotency basis ·
A8 release routes · import channels · screen inventories · effort per task.

### 32.2 Implementation compression survival test

> Could implementation make a **materially different choice that violates the architecture** if this fact
> disappears?

**YES ⇒ keep.** This is the Blueprint → Implementation boundary.

Kept: `access_mode` and its forfeits · `forced_by` per composition · guarantee and failure semantics ·
idempotency basis · enforcement point · trust boundary · irreversible/fixed-at points · release route ·
named operator and reconciler · every proof obligation with its level.

Omitted: A2 rationale prose · A11 economics · executive framing · comparator status (except where it
scopes what may be built).

### 32.3 Design Brief survival test

> Could the generated design **violate an approved UX / business / control requirement** if this fact
> disappears?

**YES ⇒ include. Otherwise leave it upstream.** Applied in full in §13.2. The brief is not an
Architecture Blueprint copy.

### 32.4 Estimate survival test

> Could excluding this work item **materially change effort, uncertainty or contingency**?

**YES ⇒ estimate it.** Informational detail is not estimated merely because it exists. A work unit
excluded for a reason (external owner, unevaluated destination, outside estimation authority) is
**named as excluded**, never silently dropped.

---

## 33. Language and audience

| Aspect | Rule |
|---|---|
| Prose language | the **engagement language** (`pack.yaml language: pt` for this pack). Deliverable prose is `pt` |
| Decision-layer literals | **verbatim, in their recorded form**: emitted outcome sentences · class markers (`COMPARATIVE FIT UNEVALUATED`, `INCUMBENT FIT UNEVALUATED`) · ids (`C/A/U/X/R/D/O/TW-NNN`) · V1–V4 · authorization values · experience modes · composition/pattern names · `access_mode` values. **Never translated, never paraphrased** (authoring-map Q-02) |
| Vendor/product terms | never awkwardly translated. Product names stay as the vendor writes them; the surrounding sentence is in the engagement language |
| Executive language | concise, sponsor-facing, no kernel jargon, no lens names |
| Architecture language | precise, architect-facing, A-section vocabulary |
| Implementation language | operational and imperative; shape contracts per section |
| Design Brief language | consumer-oriented; schema keys in English where they are keys, prose in the engagement language |
| Template copies | **no parallel PT/EN template set.** One template per deliverable; language follows the engagement |

---

## 34. Proposed Step 6B taxonomy

```text
library/packs/pp/deliverable-templates/
├── discovery-report.template.md
├── executive-report.template.md
├── solution-blueprint.template.md        # canonical: Architecture Blueprint (alias, §4)
├── implementation-spec.template.md
├── claude-design-brief.template.md
└── estimate.template.md
```

**Six files. No fragments. No includes framework. No inheritance. No router.**

| File | Canonical | Audience | Activation | Authority sources | Conditional sections | Forbidden sources | Downstream consumers |
|---|---|---|---|---|---|---|---|
| `discovery-report.template.md` | 1 Discovery Report | sponsor + stakeholders | always | SU · context · capture index · business-story · as-is · risks | conflicts · risks observed · open blocking criteria · capture sources · scope framing | decision · architecture · DK · options · vendor naming | sponsor; `--html` provenance projection |
| `executive-report.template.md` | 2 Executive Report | sponsor / C-level | always | `decisions.md` · business-story · risks · A1/A2/A9 · decision economics · estimate headline | architecture shape · investment · I-1 carriage · tripwires | `options.md` whole-file · raw evidence · DK · CRAFT · A3–A8/A10–A12 | sponsor, board |
| `solution-blueprint.template.md` | 3 Architecture Blueprint | architect / tech lead | an architecture authorization exists for ≥1 scope | `architecture:` block · `architecture-core.md` + fragments · architecture-story · decisions · SU | A4 (experience) · context picture · sequence · analytical responsibility · replacement · candidate architectures · scope ownership · boundary fragments | raw evidence · preloaded DK · financial story · other deliverables | architect; input to review/approval |
| `implementation-spec.template.md` | 4 Implementation Specification | implementation team | an architecture authorization exists **and** the blueprint is approved | `architecture:` block · core + fragments · decisions · approved UX blueprint · selective RESEARCH/CRAFT | screens (mode ≠ none) · migration & cutover · integrations · analytical work · open items | raw SU for migration · as-is for proof level · financial for sequencing · options | dev team; **Estimate** (inventory only) |
| `claude-design-brief.template.md` | 5 Claude Design Brief | Claude Design (or equivalent) | `experience.mode ∈ {owned-internal, owned-external, inherited}` **and** an approved UX blueprint | approved UX blueprint · approval id · `architecture_constraints_digest` · brand · user-lens rows · selective CRAFT | brand · accessibility · Excel anchors · async UI states · inherited-surface limits | full architecture core · DK table · financial · raw evidence | design generation |
| `estimate.template.md` | 6 Estimate | sponsor + procurement | decided scope exists **and** work is inside this pack's estimation authority **and** one of the two input modes resolves (§40.6) | **mode A**: spec inventory · **mode B**: candidate architecture record(s) + known obligations · both: `craft/estimation-model.md` (method) · decisions · A11 drivers · risks | migration effort · proof-work effort · per-candidate labelled estimates · excluded-scope statement | prices/SKUs/quotas · S8 economics · comparative use of the model · raw evidence · blended candidate figures | sponsor, procurement |

### 34.1 Why no fragments

- The one genuinely repeated block (the architecture) is **already** an include of the frozen
  architecture layer, and the iteration (0..1 experience, N+M boundary) is **already** owned by
  `aisa-render` + `architecture-core.md`. Adding deliverable-side fragments would duplicate it.
- A shared "epistemics appendix" fragment was considered and **rejected**: each deliverable projects
  epistemics differently (§15), so a shared fragment would either be wrong for five of six or become a
  parameterized template — an inheritance framework, which is out of scope by construction.
- Per-scenario templates (headless, bounded, not-authorized, class-6) were **rejected** for the same
  reason Step 5 rejected them: applicability gates and conditional sections cover all six situations
  without multiplying files.

### 34.2 Frontmatter additions (Step 6B)

`canonical_deliverable` · `activation` (the applicability expression) · `authority_sources` /
`conditional_sources` / `forbidden_sources` · per-slot `condition:` · `materiality` (Discovery) ·
`permitted_transformations` (the transformations `aisa-render` may execute for this contract, §40.2) ·
`input_modes` (Estimate only — exactly the two of §40.6) · `owns_calculation: true` (Estimate only,
meaning per §40.4). All declarative. **No router.**

---

## 35. Step 6B implementation scope

**In scope**

1. Rewrite the six deliverable templates against §28's source contracts and §34's frontmatter.
2. Remove the 9 legacy runtime occurrences (§26): `chosen_architecture` ×3 slots, its ×3 slot sources,
   the ×2 dynamic includes, and the `sub_templates` entries.
3. Point the architecture-consuming deliverables at the **fixed** `architecture-core.md` +
   `architecture_block`, and the Design Brief at the narrow `architecture_constraints_digest`.
4. Add applicability gates and conditional slots (§13.5, §27) — kills the implicit mandatory surface.
5. Add the missing decision authorities to the Executive Report: pairs · conditions · preconditions ·
   proof obligations · comparator status · tripwires (D-4, D-7 of the executive kind).
6. Add the missing epistemic sections to the Discovery Report (Unknown · Conflicted · Risky · expired
   Confirmed) plus the materiality rule and residual counts (D-6).
7. Re-source the Implementation Specification: proof obligations → test/acceptance work; architecture
   dependencies → sequencing; A9 + class 14 → migration & cutover (D-7, D-8, D-9).
8. Make the Estimate the **semantic owner** of the calculation and `aisa-render` its **executor**: declare
   `owns_calculation`, `permitted_transformations`, the two `input_modes` (§40.6), the method authority
   (`craft/estimation-model.md`) and the named-uncertainty rule (D-13, D-15, §14.4, §40.4).
9. **Remove** the implementation-estimate calculation from the synthesis layer entirely (§18.1, §40.5).
   Financial synthesis keeps the decision-economics narrative only; no second synthesis file is created.
10. Apply **I-2**: reword `architecture-story.template.md` and constrain the four comparison-adjacent
    deliverable slots (§22.2).
11. Apply **I-1**: two documentation sentences — `blueprint-contract.md` entry gate +
    `architecture-story.template.md` carriage (§21.4).
12. Apply **I-3**: the four scope-ownership projection categories in the deliverable layer (§12).
13. Add the epistemic and proof-obligation carriage rules per deliverable (§15, §16).
14. Generalize the render-gap class-3 **label** to *open work item* with `owner` (§30.2) in
    `render-contract.md` + `aisa-render`, and state the execution boundary in both:
    *render executes a projection contract; it does not reason beyond that contract* (§40.2).
15. Replace `pack.yaml`'s `applies_to: [technology]` with the authorization discriminator, and add
    `canonical_deliverable` (D-17).
16. Update `aisa-render` and `aisa-synthesize` for the new source contracts and the financial split.
17. Documentation pass: `docs/ARCHITECTURE.md` §5/§5.3, `docs/PACK_AUTHORING.md` §113.
18. Add `.claude/tests/test_pp_deliverable_templates.py` (§36).
19. Bump `pack_version` (1.7.0 → 1.8.0) with the rationale comment the pack's convention requires.

**Out of scope for Step 6B**

Step 3 registers · Step 4 knowledge units · **Step 5 architecture runtime** (`architecture-core.md`, the
four fragments, `README.md`, `aisa-blueprint`) · new research · the `chairman.md` options-artefact field
(§26, flagged to its owning line) · `library/packs/pp-backup/` · any new deliverable · any renamed
canonical deliverable · any template inheritance framework · any projection router.

**Explicitly not authorized**: touching `architecture-core.md`'s scope-ownership column hint. The
deliverable-side enumeration (§12) makes it unnecessary; C6-B proves behaviour is already correct.

---

## 36. Structural test design (Step 6B) — design only, not run

Target module: `.claude/tests/test_pp_deliverable_templates.py`. Mechanical/structural assertions only —
semantic defensibility is Step 6C. Pattern follows `test_pp_architecture_templates.py`.

| Id | Test | Mechanical assertion |
|---|---|---|
| **T-D1** | No branch / chosen-architecture vocabulary | no deliverable or synthesis template contains `chosen_architecture`, `Branch (if technology)`, `{{chosen_architecture}}`, `sharepoint-first`, `dataverse-first` or a `hybrid` **branch id**; the only architecture include is the fixed `architecture-templates/architecture-core.md` |
| **T-D2** | Headless produces no fake Design Brief or screen section | every surface slot (`canvas_app_pages`, `page_navigation_map`, `persona_users`, `ux_requirements`, `screens_to_build`) is **conditional** on `experience.mode != none`, never `required`; `claude-design-brief` declares a `not applicable` activation for `mode: none`; no template contains an unconditional persona/screen/navigation heading |
| **T-D3** | Not-authorized produces no Architecture Blueprint | `solution-blueprint`'s activation requires an authorization for ≥1 scope; the render skill's not-authorized path produces a **skip**, not a gap; no template emits an empty A-section set |
| **T-D4** | Class-6 destination unevaluated is not estimated or designed | `estimate` declares the excluded-scope statement and forbids an allowance for an unevaluated destination; `claude-design-brief` and `implementation-spec` forbid far-side content; the scope-ownership enumeration contains **category 3** |
| **T-D5** | Authorized-bounded preserves scope ownership | executive · blueprint · impl-spec · estimate each declare the uncollapsed pairs (or the scope-ownership projection) as a required/conditional source; no template collapses pairs into a single scope slot |
| **T-D6** | Executive conditions cannot disappear | `executive-report` declares `conditions`, `preconditions`, `proof_obligations` (decision-changing) and `revision_tripwires` as **required subject to existence**; no template contains a "satisfied" transformation for a condition |
| **T-D7** | Implementation cannot change architecture | `implementation-spec` lists the `architecture:` block as required, declares architecture as read-only, and contains no store/pattern/composition/experience selection vocabulary |
| **T-D8** | Design Brief cannot re-select store or composition | `claude-design-brief` contains no `record_authority`, `compositions`, `pattern` or `experience.mode` **selection** vocabulary; its architecture source is the **digest**, and `architecture-core.md` is in its forbidden list |
| **T-D9** | Estimate cannot settle economic attractiveness | `estimate` contains no comparative-economics vocabulary, no price/SKU/quota token, cites `craft/estimation-model.md` as **method**, and lists S8 economics as forbidden |
| **T-D10** | Assumed / Unknown / Conflicted never promoted | every deliverable template carries an epistemic-projection block consistent with §15; the Estimate declares the named-uncertainty rule; no template instructs "resolve", "assume confirmed" or "pick the more likely value" |
| **T-D11** | Proof levels not re-graded | every proof-carrying template quotes the five-part shape and declares V1–V4 read-only; no template contains re-grading or satisfaction vocabulary |
| **T-D12** | Multiple architectures remain multiple | `solution-blueprint` declares the candidate-architectures conditional with *choose neither, no scoring*; `implementation-spec` and `claude-design-brief` declare **blocked** on a structural open choice; `estimate` forbids a blended single figure |
| **T-D13** | No deliverable becomes source authority for another upstream concern | for every information class in §5, exactly one template declares ownership; the only deliverable→deliverable source edge is `implementation-spec → estimate`, inventory-only; the read graph is acyclic |
| **T-D14** | The two "blueprints" are never conflated | no template sources UX-blueprint content from `_render/*solution-blueprint*` or vice versa; every UX slot names `_blueprint/ux-blueprint_v<approved>.yaml` |
| **T-D15** | Selective DK and CRAFT | no deliverable template names more than **2** Domain Knowledge units without a point-of-need condition; the Design Brief's characterised 6-row table is gone; `discovery-report` and `executive-report` name **zero** DK/CRAFT units |
| **T-D16** | Manifest coherence | `pack.yaml` lists exactly 6 deliverables; every `template:` path exists; every template's `canonical_deliverable` is one of the 6; `applies_to: [technology]` is gone |
| **T-D17** | Gap-class integrity | exactly **4** render-gap classes in `render-contract.md` and `aisa-render`; class 3 carries an `owner`; deliverable-level skips are logged to `render-log.md` and never to `render-gaps.md` |
| **T-D18** | Discovery neutrality survives | `discovery-report` names no vendor/product term from the neutrality denylist and declares decision/architecture/options as forbidden sources |
| **T-D19** | **Deliverable-owned derivation executor** | `estimate` declares `owns_calculation: true` **and** all four of: input-inventory authority · method authority · permitted outputs · forbidden semantic changes. `aisa-render` is permitted to execute **only** template-declared transformations (its contract names `permitted_transformations`). `financial-story.template.md` computes **no** implementation effort figure. **No second estimate authority exists** anywhere (no synthesis file, no skill, no other template computes effort) |
| **T-D20** | **Not-authorized authority / carriage split** | `decisions.md` is declared the **outcome-basis authority**; the **architecture-entry rule** is declared the **architectability-basis semantic owner**; `_synthesis/architecture-story.md` is declared **durable carrier, not semantic authority** (the words appear, distinctly). No deliverable template declares a source or transformation that **re-evaluates pack architectability**; the carriage exception is stated as applying to this one basis only |
| **T-D21** | **Structural choice blocks the Design Brief** | the chain `structural: true` → blueprint not approved → Implementation Specification **blocked** → Claude Design Brief **blocked** is declared in the applicability contract; **no materiality override, no partial approval and no UX-only approval token** appears in any template, skill or contract |
| **T-D22** | **Estimate input modes** | `estimate` declares **exactly two** input modes (Specification inventory; candidate architecture planning inventory) — no third. Mode B declares its label (`Candidate planning estimate — pre-Implementation-Specification; lower-confidence; architecture choice unresolved`), per-candidate isolation, and the prohibition on fabricating implementation tasks. **No blended candidate figure** is permitted by any slot or transformation |

**22 structural tests. Not run in Step 6A.**

---

## 37. Step 6C semantic fixture design — design only, not run

Behavioural corpus. Frozen Step 5 scenarios are **reused, not redesigned**; one new discovery-heavy
engagement is added.

| Id | Reused from | Scenario | Deliverables that must exist | Must **not** invent |
|---|---|---|---|---|
| **DF-1** | F-3 | Record-centric governed internal application; class 1; `owned-internal`; row + column security + audit | all 6 | no price in Estimate or A11; no fresh comparison in Executive; no re-graded proof level in the spec |
| **DF-2** | F-10 | Scope pair — PP application + relocated responsibility (class 3/4), `authorized-bounded` | all 6, **each preserving the split** | no far-side design; no far-side estimate; no collapsed pair; no inferred incumbent fit |
| **DF-3** | F-12 | Two materially distinct defensible architectures inside one authorized scope; structural open choice; approval blocked | Discovery · Executive · **Blueprint (both candidates, neither chosen)**; Implementation Spec **blocked**; Design Brief **blocked (no exception)**; Estimate **either not produced, or one separately labelled candidate planning estimate per candidate** (§40.6) | no selection; no score; **no blended figure**; no spec-level task detail; no fabricated entity/flow/screen for either candidate; **no Design Brief on a "not UX-material" judgement** |
| **DF-4** | F-13 | Decision Blocked (class 12) | Discovery · Executive only | no architecture; no spec; no brief; **no estimate**; no implied outcome |
| **DF-5** | F-15 | Headless — `experience.mode: none`; A6/A7 carry the architecture | Discovery · Executive · Blueprint · Spec · Estimate; **Design Brief `not applicable`** | no persona, screen, navigation or UX state anywhere; no "application" language in Executive; no A4 |
| **DF-6** | F-17 | Positive outcome over a solution this pack cannot architect (`not-authorized`) | Discovery · Executive (decision + **both** reasons); Estimate only if inside estimation authority | no empty Blueprint; no spec; no brief; no inference about the selected solution's fit or cost; no *Decision Blocked* relabel |
| **DF-7** | C6-B | S → class 2 (PP architecture authorized, independently emitted); R → class 6 → class 8, destination **UNEVALUATED** | all 6, **S only** | no design, boundary component, owner, interface, migration or estimate for R; no reverse inference in either direction; category-3 row rendered exactly once |
| **DF-8** | **new** | Discovery-heavy engagement with **material unresolved evidence**: 3 Critical Unknowns (one in the blocking set), 1 unresolved Conflicted on a decision-critical volume, 2 accepted Risks, 1 expired Confirmed | Discovery Report (full epistemic projection) · Executive (only if a decision exists; otherwise Discovery + evidence plan) | no Unknown converted to a finding; no side chosen on the Conflicted volume; no expired Confirmed as fact; no assumption manufactured to complete a section; no transcript |

### 37.1 Cross-fixture assertions

1. Every deliverable that exists names its authorities and re-derives nothing settled upstream.
2. Every deliverable that does **not** exist is a logged **skip** with a reason — never an empty file and
   never a gap.
3. Across all eight, every information class in §5 has exactly one authority; a second occurrence is a
   projection.
4. No fixture output contains a fresh comparison, a re-graded proof level, a promoted epistemic state, a
   price, or a far-side design.
5. DF-3 and DF-7 are the two hardest negatives: **do not choose**, and **do not design or price the
   unevaluated destination**.
6. **DF-3 adversarial check (mandatory).** Run the fixture with an evaluator asserting *"the unresolved
   structural choice is not UX-material, so the Design Brief can proceed"*. The correct behaviour is
   **BLOCKED**: the brief's required source (an **approved** UX blueprint) does not exist, and no
   materiality judgement, partial approval or UX-only approval may substitute for it. A run that produces
   a Design Brief here **fails DF-3**, regardless of how good the brief is.
7. **DF-3 candidate-estimate check.** Where estimates are produced, assert: one labelled block per
   candidate (`Candidate A → its own estimate`, `Candidate B → its own estimate`), each with its own
   inventory, uncertainty and confidence; the mode-B label present; **zero** blended figures; **zero**
   spec-level tasks; **zero** screen-level work.

---

## 38. Complexity test

| Question | Answer |
|---|---|
| Do deliverables re-reason upstream evidence? | **NO** — the three current cases (D-7, D-9, D-10) are re-sourced in §11.1, §24.2 and §13.4 |
| Does each information class have one primary authority? | **YES** — §5, 21 classes, one authority each |
| Can a deliverable compress without changing semantics? | **YES** — §7.2 permitted set + the four survival tests (§32) |
| Do downstream deliverables depend on upstream deliverables as truth where a more authoritative artefact exists? | **NO** — exactly one deliverable→deliverable edge (`impl-spec → estimate`, inventory-only), and the spec **is** the authority for implementation obligations (§6.5) |
| Does headless remain headless? | **YES** — §22-behaviour in §13.5, §27, T-D2, DF-5; no surface slot is ever unconditionally required |
| Can the Architecture Blueprint be not applicable? | **YES** — §23, §27, T-D3, DF-6 |
| Can the Design Brief be not applicable? | **YES** — §13.5, §27, T-D2, DF-5 |
| Does the Estimate remain distinct from S8 economics? | **YES** — §18, and the ownership split in §18.1 |
| Does the Implementation Specification preserve architecture choices? | **YES** — §11 forbidden set, §32.2 survival test, T-D7 |
| Do class-6 unevaluated destinations remain undesigned and unestimated? | **YES** — §12 category 3, §19.1, §20, T-D4, DF-7 |
| Is a new state machine introduced? | **NO** — the four scope-ownership values are render categories; blocking reuses `structural: true` + blueprint approval; gap classes stay at four |
| Is a projection router introduced? | **NO** — activation is a declarative frontmatter condition per template; the render skill resolves slots as it already does |

### 38.1 Net complexity delta

| Added | Removed |
|---|---|
| declarative frontmatter fields (activation, source contracts, per-slot conditions, materiality) | 3 dead `chosen_architecture` slots + 3 dead slot sources + 2 dynamic includes |
| 4 scope-ownership render categories (documentation) | 1 dynamic-include mechanism |
| 1 deliverable→deliverable inventory edge | 1 comparative phrase |
| 1 gap-class label generalization (`owner`) | 1 characterised 6-unit DK table |
| 1 owned calculation in the Estimate | 1 calculation misplaced in the synthesis layer |
| 18 structural tests + 8 fixtures | `applies_to: [technology]` wrong discriminator |

**No new file in `deliverable-templates/`. No new artefact type. No new state. No new phase.**

---

## 39. Result

Step 6A defines a projection model in which the Shared Understanding, the decision, and the frozen
Architecture Layer remain the only reasoning layers; the six deliverables select, compress and re-voice
what those artefacts already hold; each information class has exactly one authority; and the four hard
negatives — headless, not-authorized, scope pairs, class-6 unevaluated destinations — are answered by
applicability gates and render categories rather than by new machinery.

Three carried Step 5C observations are resolved in the target model (I-1 §21, I-2 §22, I-3 §12) and both
carried Step 5A open questions are answered (Design Brief scope §13.2, replacement/migration boundary
§24). No deliverable template, synthesis template, render runtime, `pack.yaml`, Step 3, Step 4 or Step 5
architecture runtime file was modified.

---

`STEP 6A — DELIVERABLE PROJECTION MODEL: PASS`
`CANONICAL DELIVERABLES ACCOUNTED FOR: 6/6`
`ONE PRIMARY AUTHORITY PER INFORMATION CLASS: YES`
`DELIVERABLES MAY RE-DECIDE OPTIONS: NO`
`DELIVERABLES MAY RE-DERIVE ARCHITECTURE: NO`
`HEADLESS DESIGN BRIEF MAY BE NOT APPLICABLE: YES`
`ARCHITECTURE BLUEPRINT MAY BE NOT APPLICABLE: YES`
`NOT-AUTHORIZED DURABLE CARRIAGE DEFINED: YES`
`CLASS-6 UNEVALUATED DESTINATION REMAINS UNDESIGNED: YES`
`CLASS-6 UNEVALUATED DESTINATION REMAINS UNESTIMATED: YES`
`SCOPE-PAIR PROJECTION DEFINED: YES`
`MULTIPLE-ARCHITECTURE PROJECTION DEFINED: YES`
`ESTIMATE DISTINCT FROM S8 ECONOMICS: YES`
`IMPLEMENTATION SPEC CAN CHANGE ARCHITECTURE: NO`
`CLAUDE DESIGN BRIEF CAN SELECT STORE/COMPOSITION: NO`
`I-1 RESOLVED IN TARGET MODEL: YES`
`I-2 RESOLVED IN TARGET MODEL: YES`
`I-3 RESOLVED IN TARGET MODEL: YES`
`OLD BRANCH / CHOSEN_ARCHITECTURE MODEL SURVIVES: NO`
`NEW PROJECTION ROUTER INTRODUCED: NO`
`NEW STATE MACHINE INTRODUCED: NO`
`PP RUNTIME FILES MODIFIED: 0`
`STEP 5 — ARCHITECTURE TEMPLATES FROZEN: YES`
`READY FOR STEP 6A REVIEW: YES`

---

# 40. Final bounded contract correction (appended 2026-09-04)

**The Step 6A direction is approved.** This section applies **three bounded contract corrections** and is
**normative**: where it and an earlier section differ, §40 governs. Earlier passages were edited in place
to point here; nothing else in §1–§39 is reopened.

**Corrections applied**

| # | Concern | Sections corrected |
|---:|---|---|
| **1** | execution of deliverable-owned derivations | §25.1–§25.4 · §34.2 · §35 items 8/14 · §40.1, §40.2, §40.4, §40.5 |
| **2** | authority **vs** durable carriage for `not-authorized` | §5 · §21.2–§21.4 · §40.3 |
| **3** | multiple-architecture applicability / estimate fallback | §6.5 · §14.1 · §27 (cell + notes 9, 10) · §28.6 · §34 · §40.5, §40.6, §40.7 |

**Preserved unchanged**: the doctrine chain (SU → Decision → Architecture → Deliverable projections) ·
closest authority · compression without reinterpretation · no truth by repetition · six canonical
deliverables · one authority per information class · no projection router · no state machine · headless
behaviour · class-6 behaviour · scope-pair projection · Estimate ≠ S8 economics · the Design Brief's
narrow architecture digest · **I-2** · **I-3**.

---

## 40.1 Reasoning vs projection transformation

The §25 contract as first written left **no executor** for legitimate deliverable-owned derivations. The
binding distinction:

```text
REASONING
→ settles or changes upstream meaning

PROJECTION TRANSFORMATION
→ deterministically derives a downstream representation
   from already-authoritative inputs
   under a deliverable-owned contract
```

**Permitted projection transformations** (none of these is upstream reasoning):

```text
architecture obligation        → implementation work package
proof obligation               → acceptance work package
implementation inventory       → estimate work unit
work units + estimation method → effort range / arithmetic
approved UX blueprint          → generator-oriented screen block
```

A projection transformation is legitimate exactly when it is **deterministic**, **bounded**, **declared by
the active deliverable contract**, and **traceable to already-authoritative inputs**. Fail any of the four
and it is reasoning, and therefore prohibited.

---

## 40.2 The corrected layer execution contract

| Layer | May | May **not** |
|---|---|---|
| **Synthesis** | narrate · compress · order · cite · produce bounded narrative projections | decide · compare afresh · select an interpretation · re-grade epistemics · **compute the implementation estimate** |
| **Deliverable template** | own projection semantics · allowed transformations · source contract · selection/materiality · structure · applicability | **execute anything itself** |
| **Render / deliverable execution** (`aisa-render`) | execute **only** the projection transformations explicitly declared by the active deliverable contract — including the deterministic, bounded derivations required by the **Implementation Specification**, the **Claude Design Brief** and the **Estimate** | create new upstream facts · choose an option · choose architecture · change scope · resolve an Unknown · promote epistemics · invent work · re-source evidence · create a comparator claim |

> **Render executes a projection contract; it does not reason beyond that contract.**

**No new engine and no new skill.** The executor is the existing `aisa-render`. The template declares;
the renderer executes; neither reasons.

---

## 40.3 I-1 — semantic authority separated from durable carriage

```text
outcome basis
→ semantic owner:   the Options layer that emitted the sentence
→ durable source:   decisions.md

architectability basis
→ semantic owner:   the architecture-entry gate rule
                    (selected solution × frozen active-pack architectability boundary)
→ durable carrier:  _synthesis/architecture-story.md
                    (only where no architecture artefact exists)
```

`_synthesis/architecture-story.md` is **not** the semantic authority for `architectability_basis`. As
**durable carrier** it:

- does **not** own the rule;
- may **not** change the wording's meaning;
- may **not** widen or narrow the active pack's architecture authority;
- may **not** introduce a new basis;
- must carry a result **reproducible** from *the already-recorded selected solution* × *the frozen
  active-pack architectability boundary*.

Downstream deliverables read it as **the durable carrier of an architecture-entry result**, never as the
source of architectural truth. **This is the only carriage exception in the model, and it does not
generalize to any other architecture field.**

**Primary-authority table correction** (applied at §5):

| Case | Semantic authority | Durable source / carrier |
|---|---|---|
| `authorized` / `authorized-bounded` | the architecture-entry gate; recorded in the `architecture:` block | the `architecture:` block (authority **and** carrier) |
| `not-authorized` | outcome reachability **×** the architecture-entry architectability evaluation | outcome basis → `decisions.md`; architectability basis → `architecture-story.md` **as carrier** |

**Step 5 remains frozen.** `aisa-blueprint`, `architecture-core.md`, the four fragments,
`architecture-templates/README.md` and every Step 5 contract are untouched. I-1 is resolved by
projection and carriage semantics only: **no new architecture artefact, no empty blueprint, no new
field.** The two Step 6B changes remain exactly the two documentation sentences of §21.4.

---

## 40.4 The Estimate execution path

```text
authoritative work inventory
+
craft/estimation-model.md            (method authority — person-days)
+
named estimate assumptions
        ↓
aisa-render executing estimate.template's projection contract
        ↓
work breakdown + effort bands + ranges + contingency + confidence
```

| Role | Holder |
|---|---|
| **Semantic owner** of mapping · calculation · arithmetic · estimate assumptions · confidence | **the Estimate deliverable** |
| **Executor** | **`aisa-render`** — and nothing else |
| Method authority | `craft/estimation-model.md` (method only; explicitly not valid comparatively) |
| Input inventory authority | mode A: the Implementation Specification · mode B: the candidate architecture record(s) (§40.6) |

**Synthesis must not compute these values.** No new estimation skill and no new engine is introduced.

### `owns_calculation` — meaning

```yaml
owns_calculation: true    # Estimate only
```

**Means**: this deliverable contract **authorizes `aisa-render` to execute the bounded calculation defined
by the template, using the named method authority.**

**Does not mean**: the Markdown template itself reasons.

**Structural obligation** — a calculation-owning deliverable **must declare** all four of:

1. **input inventory authority** (which artefact supplies the work units);
2. **method authority** (which unit supplies the effort model);
3. **permitted outputs** (work breakdown · bands · ranges · contingency · confidence);
4. **forbidden semantic changes** (no scope change, no epistemic promotion, no comparator claim, no
   invented work unit, no price).

Asserted by **T-D19** (§36).

---

## 40.5 Two withdrawals

**(a) Financial synthesis keeps no implementation-estimate calculation.**

```text
financial synthesis   → decision economics narrative ONLY
Estimate deliverable  → implementation effort calculation and projection
```

The earlier "one file, two owned halves" option is **withdrawn**. No second synthesis file is created for
implementation effort. Any implementation-effort prose surviving in synthesis after Step 6B may only be a
**reference or projection of an already-produced Estimate** — never the calculation source, and never
where a figure first appears. **Preferred outcome: the calculation leaves synthesis entirely.**

**(b) The Design Brief materiality exception is withdrawn.**

Frozen runtime rule:

```text
structural: true
→ blueprint approval blocked
```

Design Brief contract: **an approved UX blueprint is required.** Therefore:

```text
structural: true
→ no approved blueprint
→ Claude Design Brief BLOCKED
```

**No exception.** No partial approval, no UX-only approval, no materiality override — each would be new
workflow semantics, and none is introduced here. If future evidence shows partial approval is needed,
that is a separate design question, not Step 6A. Asserted by **T-D21** and by DF-3's adversarial check
(§37.1 item 6).

---

## 40.6 Estimate input modes — the spec/candidate contradiction resolved

The model previously held both *"the Estimate requires the Specification inventory"* and *"with multiple
architectures open the Specification is blocked yet the Estimate may estimate candidates"*. **Two
legitimate input modes, and no third.**

### Mode A — implementation estimate (the authoritative path)

```text
approved architecture
+
Implementation Specification inventory
→ implementation estimate
```

**Invariant preserved**: *when a Specification exists, the Estimate may not add a work unit absent from
that Specification.* A needed-but-absent unit is an open work item logged against the spec.

### Mode B — candidate planning estimate

Available **only** where all three hold:

```text
architecture candidates exist
+ architecture approval is blocked by the unresolved structural choice
+ a sponsor materially needs comparative delivery magnitude
```

**Authority**: candidate architecture components · candidate-specific obligations · proof obligations ·
migration obligations **already known** · `craft/estimation-model.md`.

**Mandatory label**, verbatim:

> Candidate planning estimate — pre-Implementation-Specification; lower-confidence; architecture choice
> unresolved.

**Per candidate**: its own work inventory · its own estimate · its own uncertainty · its own confidence.
**Never blend candidates. Never choose.**

**May estimate**: architecture components · known configuration/build obligations · known proof work ·
known migration work.

**May not estimate**: detailed implementation tasks not yet derivable · screen-level work while the UX
blueprint is unapproved · an unevaluated far side · work whose existence depends on the unresolved choice
without being assigned to the candidate it belongs to.

```text
no spec  ≠  permission to invent a spec
```

### The scope-control rule, restated per mode

| Mode | The Estimate may not add a work unit absent from … |
|---|---|
| **A** | the Implementation Specification |
| **B** | the candidate architecture's known components / obligations |

This removes the contradiction without weakening scope control.

### Neither basis present

The Estimate is **blocked** or **not applicable**, as appropriate — never a placeholder, never a guess.

---

## 40.7 Monetary boundary preserved

This correction changes nothing about money. Still prohibited as invented or live values: **licence
prices · SKU prices · platform rate cards · quotas presented as cost facts.**

**Person-days remain the canonical estimate denominator** where no valid delivery rate exists. If a future
engagement supplies an internal approved delivery-labour rate, it is an **engagement input with
provenance** — not Domain Knowledge, and not a pack fact. **No such rate is introduced in Step 6A.**

---

## 40.8 Complexity re-test

```text
new reasoning layer introduced                                → NO
new estimation skill introduced                               → NO
renderer becomes unrestricted reasoner                        → NO
renderer may execute bounded deliverable-owned transformation  → YES
synthesis owns architectability                               → NO
synthesis durably carries one not-authorized basis            → YES
partial UX approval introduced                                → NO
Design Brief can bypass blocked blueprint approval            → NO
candidate estimate possible without inventing a spec          → YES
candidate estimates can be blended                            → NO
new state machine                                             → NO
projection router                                             → NO
```

## 40.9 Correction footprint

| Aspect | Value |
|---|---|
| Report sections corrected in place | 16 (§5 · §6.5 · §14.1 · §14.3 · §18.1 · §21.2 · §21.3 · §21.4 · §25.1 · §25.2 · §25.3 · §25.4 · §27 · §28.6 · §34 · §35 · §36 · §37) |
| New normative section | 1 (§40) |
| Structural tests added | 4 (**T-D19** … **T-D22**) — total **22** |
| Fixtures added | 0 (DF-3 tightened; 2 new cross-fixture checks, incl. the adversarial Design Brief check) |
| New artefacts · engines · skills · states · routers | **0** |
| Runtime files modified | **0** |
| Step 5 files modified | **0** |

---

`STEP 6A FINAL BOUNDED CONTRACT CORRECTION: PASS`
`DELIVERABLE-OWNED DERIVATION EXECUTOR DEFINED: YES`
`ESTIMATE CALCULATION SEMANTIC OWNER: ESTIMATE`
`ESTIMATE CALCULATION EXECUTOR: AISA-RENDER`
`SYNTHESIS COMPUTES IMPLEMENTATION ESTIMATE: NO`
`RENDER MAY EXECUTE BOUNDED PROJECTION TRANSFORMATIONS: YES`
`ARCHITECTABILITY BASIS SEMANTIC OWNER: ARCHITECTURE-ENTRY GATE (SELECTED SOLUTION × FROZEN ACTIVE-PACK ARCHITECTABILITY BOUNDARY)`
`ARCHITECTURE-STORY IS DURABLE CARRIER ONLY: YES`
`SYNTHESIS IS ARCHITECTURE AUTHORITY: NO`
`STRUCTURAL OPEN CHOICE CAN BYPASS BLUEPRINT APPROVAL FOR DESIGN BRIEF: NO`
`MULTIPLE-ARCHITECTURE DESIGN BRIEF: BLOCKED`
`ESTIMATE INPUT MODES: 2`
`CANDIDATE PLANNING ESTIMATE DEFINED: YES`
`CANDIDATE ESTIMATES MAY BE BLENDED: NO`
`CANDIDATE MODE MAY INVENT SPEC TASKS: NO`
`NEW ESTIMATION SKILL INTRODUCED: NO`
`NEW STATE MACHINE INTRODUCED: NO`
`PP RUNTIME FILES MODIFIED: 0`
`STEP 5 REMAINS FROZEN: YES`
`STEP 6A MODEL READY TO FREEZE: YES`
`READY FOR STEP 6B IMPLEMENTATION: YES`


```text
STEP 6A — DELIVERABLE PROJECTION MODEL: FROZEN

FINAL BOUNDED CONTRACT CORRECTION: PASS
CANONICAL DELIVERABLES: 6/6
ONE PRIMARY SEMANTIC AUTHORITY PER INFORMATION CLASS: YES
DELIVERABLE-OWNED DERIVATION EXECUTOR: AISA-RENDER
ESTIMATE SEMANTIC OWNER: ESTIMATE
SYNTHESIS COMPUTES IMPLEMENTATION ESTIMATE: NO
ARCHITECTABILITY BASIS SEMANTIC OWNER: ARCHITECTURE-ENTRY GATE
ARCHITECTURE-STORY: DURABLE CARRIER ONLY
MULTIPLE-ARCHITECTURE DESIGN BRIEF: BLOCKED
ESTIMATE INPUT MODES: 2
CANDIDATE ESTIMATES MAY BE BLENDED: NO
NEW REASONING LAYER: NO
NEW STATE MACHINE: NO
NEW ROUTER: NO
STEP 5 REMAINS FROZEN: YES

STEP 6A: FROZEN
```
