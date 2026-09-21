# Step 6C — Deliverable Semantic / Projection Behavioural Gate Report

<!--
provenance: AUTHORING (gate report) · class: EVIDENCE
authored: 2026-09-04 (Step 6C)
Predecessors: step-6a-deliverable-projection-model.md (FROZEN, incl. §40 correction),
step-6b-deliverable-projection-implementation-report.md (PASS / CLOSED).
BEHAVIOURAL GATE. No runtime file was modified during the initial gate. The only non-report
modification made before the gate is the documentation-only Step 6B cleanup of §0 below.
-->

---

## 1. Gate basis

### 1.1 What Step 6B proved, and what it did not

Step 6B proved the six projection contracts **exist and are mechanically coherent**: 22/22 structural
tests, 200 tests in `test_pp_deliverable_templates.py`, 566 in full regression, 0 failures. Its own §29
states the limit plainly: *"It does not prove the six deliverables stay semantically aligned under
realistic engagement pressure."*

Step 6C tests exactly that. The question is not *do the contracts exist* but:

```text
do the six deliverables behave as six views of ONE authoritative engagement state?
```

### 1.2 The required chain

```text
authoritative upstream facts
        ↓
decision
        ↓
architecture
        ↓
bounded projection transformation
        ↓
deliverable
```

### 1.3 The forbidden chain

```text
deliverable
→ notices something inconvenient
→ re-reads discovery / Domain Knowledge
→ repairs the truth
→ produces a more convenient answer
```

**A less complete but honest projection is better than a polished invented one.** That standard, not
prose quality, decides every verdict below.

### 1.4 Step 6B documentation cleanup (performed before the gate, documentation only)

Two stale descriptions in `step-6b-deliverable-projection-implementation-report.md` were corrected. **No
runtime change.**

| Item | Change |
|---|---|
| §23 (Documentation) | *"the single deliverable→deliverable edge"* → **exactly two bounded deliverable→deliverable edges** (`Implementation Specification → Estimate`, inventory only; `Estimate → Executive Report`, headline / one investment paragraph only) — **no third edge** |
| §25 (Regression results) | relabelled **PRE-FINAL-SOURCE-AUTHORITY-REPAIR SNAPSHOT**, retained unaltered, with §30.7 named as the authoritative final regression state: `test_pp_deliverable_templates.py: 200` · `full final regression: 566` · `failures: 0` |
| end of report | `STEP 6B: CLOSED` appended |

### 1.5 Runtime under test

Executed as authored, unmodified:

```text
deliverable templates   discovery-report · executive-report · solution-blueprint ·
                        implementation-spec · claude-design-brief · estimate
synthesis templates     business-story · as-is · architecture-story ·
                        risks-and-assumptions · financial-story
runtime contracts       aisa-render · aisa-synthesize · render-contract.md ·
                        blueprint-contract.md · pack.yaml
method authority        craft/estimation-model.md (person-days; its own banner read)
architectability rule   architecture-templates/README.md §2
```

Synthetic content is **engagement data only** (Shared Understanding rows, decisions, architecture
records, synthesis narratives, capture indexes). No runtime semantics was substituted by synthetic text.
No fixture artefact encodes expected deliverable wording or expected gate conclusions.

### 1.6 Constraints honoured

Step 6A not redesigned · runtime not modified during the initial gate · Steps 3, 4 and 5 not reopened ·
no new research · no web access · canonical research untouched.

---

## 2. Fixture corpus

Eight fixtures, frozen in Step 6A §37, all executed. Realistic Portuguese-language engagements; upstream
artefacts written per fixture (Shared Understanding with all five states and validity stamps, decisions
with uncollapsed pairs and verbatim outcome sentences, an architecture record inside the UX blueprint
where one exists, the synthesis topic packs, and a capture evidence index).

| Id | Shape | Upstream artefacts written | Deliverables produced |
|---|---|---|---:|
| **DF-1** | governed internal application; class 1; `authorized`; `owned-internal`; row + column security + audit trail | SU (9 C · 2 A · 1 U · 0 X · 1 R), `decisions.md# D-014`, approved `ux-blueprint_v03` with architecture record, 5 synthesis packs, capture index | 6/6 |
| **DF-2** | authorized-bounded scope pair; class 2 + class 3 relocation with a named owner | SU (6 C · 1 A · 1 U · 0 X · 1 R), `D-021`, approved `ux-blueprint_v02`, 5 synthesis packs | 6/6 |
| **DF-3** | one authorized scope, **two materially distinct defensible architectures**, `structural: true` open choice, blueprint approval blocked | SU (4 C · 1 A · 2 U · 0 X · 1 R), `D-031`, **unapproved** `ux-blueprint_v01` carrying both candidates, 5 synthesis packs | 4 produced · 2 blocked |
| **DF-4** | **Decision Blocked** (class 12) | SU with ≥2 Critical Unknowns (one in the blocking set) and an unresolved Conflicted row, `D-NNN` recording the block, synthesis packs, capture index | 2 produced · 4 not applicable |
| **DF-5** | **headless** — `experience.mode: none`; A6/A7 carry the architecture | SU, decisions with verbatim pairs and comparator markers, approved blueprint whose architecture record has no screens/personas/navigation, 5 synthesis packs | 5 produced · 1 not applicable |
| **DF-6** | **positive non-PP decision** — selected solution outside this pack's architecture authority ⇒ `not-authorized` for every scope | SU, `D-002` owning the outcome basis (no `architectability_basis` field), `architecture-story.md` as durable carrier, synthesis packs. **No blueprint version.** | 2 produced · 4 not applicable |
| **DF-7** | **class 6 + independent PP scope** (frozen C6-B): S → class 2 → PP authorized; R → class 6 → class 8, destination **UNEVALUATED** | SU, decisions with two uncollapsed pairs and both verbatim sentences, approved blueprint for S only, synthesis packs | 6/6 for **S only** |
| **DF-8** | **discovery-heavy, unresolved evidence**, pre-decision | SU with 3 Critical Unknowns (1 blocking), 1 unresolved Conflicted on a decision-critical volume, 2 Risky, 1 **expired** Confirmed, material Assumed, plus non-material rows to force compression; `frame.md` + `D-001` framing only | 1 produced · 5 not applicable / blocked |

### 2.1 Adversarial probes executed beyond the fixture set

| Probe | Fixture | §  |
|---|---|---|
| Executive ↔ Estimate bounded edge, cases E-1 / E-2 / E-3 (order inversion) | DF-1 (+ DF-4, DF-6 for E-2) | §10, §11 |
| **Mode-A omitted-work probe** (mandatory) | DF-1 | §15 |
| Friction / acceptance-work probe (DV-1 / defect D-7 boundary) | DF-1 | §14 |
| Candidate-estimate blending pressure | DF-3 | §22 |
| Design Brief structural-blocking pressure | DF-3 | §16 |
| **I-1 semantic-authority probe** | DF-6 | §20 |

---

## 3. Per-fixture applicability

`R` required · `C` conditional · `NA` not applicable · `B` blocked. The **WHY** is the deliverable's own
declared `activation` / `not_applicable_when` / `blocked_when`, evaluated against the fixture's upstream
state — never inferred from whether the decision happened to be technological.

| Fixture | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| **DF-1** | R | R | R | R | C→produced | C→produced (mode A) |
| **DF-2** | R | R | R (PP side only) | R (PP side only) | C→produced | C→produced (mode A) |
| **DF-3** | R | R | **R — both candidates, neither chosen** | **B** | **B** | C→produced (**mode B**) |
| **DF-4** | R | R | **NA** | **NA** | **NA** | **NA** |
| **DF-5** | R | R | R | R | **NA** | C→produced (mode A) |
| **DF-6** | R | R | **NA** | **NA** | **NA** | **NA** |
| **DF-7** | R | R | R (S only) | R (S only) | C→produced (S only) | C→produced (mode A, S only) |
| **DF-8** | R | **B** | **NA** | **NA** | **NA** | **NA** |

### 3.1 Why, per non-trivial cell

**DF-3 — Implementation Spec and Design Brief `BLOCKED`.** `open_architecture_choices[]` contains OAC-21
with `structural: true`. The chain is mechanical and uses no new machinery:
`structural: true → blueprint APPROVAL blocked (blueprint-contract.md hard rule 5) → no approved
architecture / no approved UX blueprint → each deliverable's required primary authority does not exist →
BLOCKED`. The Blueprint itself still renders, because a structural choice blocks **approval**, never
**production**. The Estimate is `conditional` under mode B.

**DF-4 — four `NA`.** Class 12: the architecture-entry gate never ran, so no authorization exists for any
scope (Blueprint, Spec, Design Brief). The Estimate's own `not_applicable_when` names class 12 explicitly,
and neither input mode resolves — no Specification (not mode A), no architecture candidates blocked by a
structural choice (not mode B), and there is no third mode. The Design Brief is `NA`, deliberately **not**
`blocked`: `blocked_when` presupposes a blueprint loop that a decision has opened.

**DF-5 — Design Brief `NA`.** `not_applicable_when: experience.mode == none`. The deliverable is skipped,
not emptied, and no persona / screen / navigation / UX-state slot is emitted anywhere.

**DF-6 — four `NA`.** `authorization: not-authorized` for every scope. The Estimate is `NA` for a distinct
reason from the other three: the selected solution is a packaged/SaaS product, and
`craft/estimation-model.md` carries bands for building on **this platform only** — its own banner forbids
comparative use. Reason logged verbatim: *"this pack has no estimation basis for the selected solution
class"*. **No number produced.**

**DF-7 — all six produced, for S only.** S carries the PP authorization; R is category 3 and receives no
deliverable content of any kind beyond its single scope-ownership row.

**DF-8 — Executive `BLOCKED`, not `NA`.** Its `activation` is `always`, so it cannot be *not applicable*;
but its primary semantic authority `decisions.md# D-NNN` **does not exist** — `decisions.md` carries only
the `D-001` framing record, and the Discovery contract itself draws that distinction
(*"the framing decision ONLY — never D-NNN outcomes"*). Per `render-contract.md`, *blocked* = a required
authority does not yet exist. Producing one would mean inventing the decision. Unblocked by `/decide`.

### 3.2 The applicability discriminator

In every fixture the discriminator used was **does an architecture authorization exist for at least one
scope?** — never *was the decision technological*. `applies_to: [technology]` appears nowhere as an active
key.

---

## 4. Per-fixture outputs — actual behaviour

For each produced deliverable: authorities actually read · forbidden sources avoided · transformations
executed · DK/CRAFT pulls · epistemics · conditions · scope · proof obligations · open items · verdict.

### DF-1 — governed internal application (6/6)

| Deliverable | Authorities read | Forbidden avoided | Transformations | DK/CRAFT | Epistemics | Conditions | Scope | Proof | Open items | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| Discovery | SU · context.json · business-story · as-is · risks-and-assumptions · evidence-index | D-014, architecture block, options.md, all DK/CRAFT, `_render/*` | as-is reconstruction · table↔prose · materiality · id citation | **0** | 5/5 in own state; C-006 expiry flagged | n/a (pre-decision) | n/a | n/a | evidence plan for U-003 | **PASS** |
| Executive | D-014 (primary) · business-story · risks-and-assumptions · A1/A2/A9 · financial-story (decision economics) · Estimate headline · SU validity | options.md whole-file, raw evidence, DK/CRAFT, A3–A8/A10–A12, fragments, ux-blueprint | compression · prose · one investment paragraph · architecture named not described | **0** | A-001 Assumed, U-003 open, C-006 expiry as re-verification | **1 of 2 carried — see F-1** | 1 pair verbatim | 3, decision-changing, quoted | tripwires + 4 next actions | **FAIL (F-1)** |
| Blueprint | architecture block · architecture-core · 1 boundary fragment · architecture-story · D-014 · SU | raw evidence, DK preload, financial-story, `_render/estimate`, options.md | A-order · tables · narrative weaving · 4 scope categories | **0** | A12 ledger complete; volatile stamped | both rendered | single pair | 3, five-part shape | OAC-1 with `structural: false` | **PASS** |
| Impl Spec | architecture block · architecture-core · fragment · D-014 · approved bp-v03 | raw SU as migration source, as-is as acceptance source, financial-story as sequencing source, `_render/estimate`, options.md, DK catalogue | obligation→build · proof→package+acceptance · dependency→sequencing (no durations) · A9→migration · screen→build block | **1** CRAFT (matrix **form** only) | Unknown → open item; Risky → mitigation obligation | precondition yes; **condition absent** | PP-owned only; far side = interface obligation | 3 packages, fields quoted | 2 open items with owners | **FAIL (F-1)** |
| Design Brief | approved bp-v03 (primary) · D-014 approval id · digest (A1/A3/A5/A7/A12) · brand_guidance · SU lens=user | architecture-core in full, fragments, six channels, DK catalogue, financial-story, architecture-story, `_render/*` | screen→generator block · per-screen blocks · point-of-need citation · digest selection | **2** CRAFT | R-002 surfaces as a required UI state | n/a | PP-owned surfaces only | UX validations only | none | **PASS** |
| Estimate | Spec inventory (mode A) · estimation-model (method) · D-014 · architecture block (A11 drivers, open choices) · risks-and-assumptions | as-is (4 ways), business-story, discovery narrative, financial-story as effort source, S8, prices, raw evidence | inventory→work unit · units+method→bands · bands→phases · bands+uncertainties→range+contingency+confidence | **1** CRAFT method + drivers | Unknown/Risky as named uncertainty lines | condition not effort-changing | PP-owned only; category-2 far side excluded with reason | effort per package, unfunded flagged | 3 named uncertainties | **PASS** |

### DF-2 — authorized-bounded scope pair (6/6)

Same source discipline. Distinguishing behaviours: both pairs uncollapsed in Executive, Blueprint, Spec
and Estimate; `INCUMBENT FIT UNEVALUATED` rendered verbatim in **four** deliverables; the virtualized
`access_mode` forfeit (no write, no real-time freshness) propagates as a required UI state
(`dados-mestre-desactualizados`) in the Design Brief and as a read-only constraint in the Spec; the
far-side delivery is excluded from the Estimate **with its reason**; the build-gating condition survives
into the Spec (§13 + §15). **All six PASS.**

### DF-3 — two candidate architectures, structural open choice (4 produced, 2 blocked)

Blueprint renders both candidates, chooses neither, scores neither, and states U-201 as what would settle
it; A3/A5/A6 render as *not determined — depends on the candidate*; **zero** fragment instances, declared
`not applicable` because instantiating them would be choosing. Executive carries OAC-21 as a structural
open choice and states the blocking consequence. Estimate is **mode B**, two labelled candidate blocks.
Spec and Design Brief **blocked**, logged with what would unblock them. **All PASS.**

### DF-4 — Decision Blocked (2 produced, 4 not applicable)

Discovery renders 5/5 states with counted residuals (`+7` Unknown, `+2` Assumed) and two **expired** rows
(C-009 Confirmed, A-002 Assumed) as re-verification obligations. Executive explains what blocks the
decision, the evidence required, its owner and expected form, and the cost of not resolving; it carries
**no** investment paragraph, **no** architecture section, and it does **not** relabel the block as
`not-authorized`. **Both PASS.**

### DF-5 — headless (5 produced, Design Brief not applicable)

See §17. **All PASS except the F-2 headline-payload breach in the Executive.**

### DF-6 — positive non-PP decision (2 produced, 4 not applicable)

See §20. **Both PASS.**

### DF-7 — class 6 + independent PP scope (6/6, S only)

See §19. **All PASS except the F-2 headline-payload breach in the Executive.**

### DF-8 — discovery-heavy, pre-decision (1 produced, 5 not applicable / blocked)

See §7. **PASS.**

---

## 5. Cross-deliverable truth invariant

For each fixture a small set of material truths was traced across every deliverable that projects it.
The requirement is `one semantic truth → zero or more audience-specific projections`; the failure mode is
`one upstream truth → two deliverables giving materially different meanings`.

### 5.1 DF-1 — governed internal application

| Truth | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate | drift |
|---|---|---|---|---|---|---|---|
| selected solution (internal app, record authority on the platform, native row+column security) | n/a (neutral) | plain language | A1/A5/A7 | read-only constraint | A1 digest | scope statement | **none** |
| condition: security model validated with internal audit **before build starts** | n/a | §6, owner + funded + by-when | Base de decisão | **ABSENT** | n/a | not effort-changing | **F-1** |
| accepted risk R-002 (offline write conflict) | §9 as observed risk | §7 as accepted, "aceite não é mitigado" | A12 accepted-risk id | §15 mitigation obligation | required UI state `conflito` | named uncertainty ±2,0 d | **none** — same identity, different altitude |
| proof obligation P-3 (V2, Operações, **not funded**) | n/a | §8 with funded=não | A12 five-part | §12 package + acceptance | n/a | 2,0 d, uncertainty **alta** | **none** |
| owner of the audit-preservation destination (Auditoria Interna) | n/a | §10 one clause | A3 + fragment owner | §6 interface obligation, far side not specified | not surface-touching, excluded from digest | far-side delivery excluded with reason | **none** |
| U-003 (attachment retention, Media) | §7 with criticality + who answers | §15 as open | OAC-1 `structural: false` | §15 open item, owner `evidence` | "não bloqueia design" | ±0,5 d named uncertainty | **none** |

### 5.2 DF-2 — scope pair

| Truth | Executive | Blueprint | Spec | Design Brief | Estimate | drift |
|---|---|---|---|---|---|---|
| pair 2 relocated, owner Direcção Digital, INCUMBENT FIT UNEVALUATED | verbatim + category named | category 2 row + one fragment, 6 channels | interface obligation only; far side not specified | "não existe superfície de fornecedor externo neste design" | far-side delivery excluded with reason | **none** — marker verbatim in 4 of 5 |
| `access_mode: virtualized` forfeits (no write, no real-time freshness) | not decision-material, omitted | A5 forfeit column | read-only constraint + no-write rule | required UI state `dados-mestre-desactualizados` | W-3 as external-integration band | **none** |
| condition: written exchange contract before internal build, **not funded** | §6 with funded=**não** | Base de decisão | §13 sequencing + §15 open item | n/a | §9 named uncertainty ±3,0 d | **none** |

### 5.3 DF-3 — unresolved structural choice

| Truth | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate | drift |
|---|---|---|---|---|---|---|---|
| U-201 Critical, unresolved | §7 Critical + who answers | §15 open + §9 structural | A2 "NÃO RESOLVIDO" + OAC-21 | **blocked** | **blocked** | decides which estimate applies | **none** |
| the architecture choice is open | n/a | §10 "composição não está fechada" | both candidates, neither chosen | blocked | blocked | two separate estimates, never blended | **none** |
| R-201 accepted (irreversible plane change) | §9 | §7 accepted | A9 + A12 | blocked | blocked | §5 named, identity kept | **none** |

### 5.4 DF-7 — class 6

| Truth | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate | drift |
|---|---|---|---|---|---|---|---|
| R excluded, destination unevaluated, COMPARATIVE FIT UNEVALUATED | evidence for R in its own states | verbatim sentence incl. *"pode continuar a ser a resposta correcta para…"* + candidate set | **exactly once**, category 3, no owner value | category 3 = nothing + OWI-04 naming the unselected destination | **0 occurrences** | excluded, **0 d**, no allowance | **none** |
| S authorized | neutral | pair verbatim | A1–A12 for S | build scope = S | designs S only | estimates S only | **none** |

### 5.5 Result

**Contradictions found across the corpus: 0.** Every material truth projected at multiple altitudes kept
its meaning, its identity and its markers. The one cross-deliverable failure, **F-1**, is a truth that
**disappeared** from one deliverable — an omission, not a contradiction. No fixture produced two
deliverables asserting materially different meanings for one upstream fact.

---

## 6. Closest-authority analysis

For each projected information class, the source **actually used** in the runs.

| Information class | Required closest authority (frozen §5) | Source actually used | Verdict |
|---|---|---|---|
| engagement fact | `shared-understanding.md` row, by id | SU rows, cited by id in every Discovery Report and every epistemic ledger | OK |
| epistemic state | SU row state + `states.md` vocabulary + `verificado_em` / `validade` | the row state and its stamps; expiry computed from the half-life, never re-judged | OK |
| decision | `decisions.md# D-NNN` | `decisions.md` in every Executive; **never** `options.md` | OK |
| (scope, outcome) pair | `decisions.md# (Scope, outcome) pairs — UNCOLLAPSED` | that section, verbatim, in Executive · Blueprint · Spec · Estimate | OK |
| condition / precondition | `decisions.md# Conditions` / `# Preconditions` | that section in every Executive; in 3 of 4 Specs | source OK · carriage **F-1** |
| accepted risk | `decisions.md# Accepted risks` + the SU `R-NNN` it points at | both jointly, with the id preserved | OK |
| option comparison | projected only through the decision's own record | the recorded justification and per-alternative why-not lines. `options.md` read **0 times** | OK |
| comparator status | the emitted sentence's own markers | reproduced verbatim; never re-derived, never inferred from silence | OK |
| architecture authorization (authorized / bounded) | the architecture block — `authorization` + both bases | the block, read; never derived, upgraded or downgraded | OK |
| architecture authorization (not-authorized) | **semantic**: the architecture-entry gate rule · **carriers**: `decisions.md` (outcome) + `architecture-story.md` (architectability) | exactly that split, with the roles named in the Executive itself | OK |
| architecture component | the block's `compositions[]` / `record_authority[]` / `relocated_responsibilities[]` | the block; no component added, renamed or merged | OK |
| pattern import | the boundary-fragment instance, six channels | one instance per qualifying component, six channels each | OK |
| proof obligation | `decisions.md# Proof obligations` carried into the block | the block, quoted in the five-part shape | OK |
| implementation work | the **Implementation Specification** | the Spec inventory, per work unit, with explicit Spec section anchors | OK |
| UX constraint | the **approved** `ux-blueprint` | the approved version only; no narrative fallback; no rendered Blueprint read | OK |
| effort estimate | the **Estimate** | the Estimate owns every figure; Executives attribute rather than derive | source OK · payload **F-2** |

### 6.1 Farther-source substitutions

**None detected.** Specifically checked and clean:

- No Specification sourced entities or screens from architecture narrative instead of the record plus the
  approved blueprint.
- No Estimate sourced work from `_synthesis/as-is.md` or from raw SU rows.
- No Executive sourced comparison from `options.md`.
- No Design Brief sourced UX from the rendered Architecture Blueprint or the rendered Specification.
- No deliverable sourced the architectability basis from anywhere but the declared carrier, and DF-6's
  Executive names the carrier **as a carrier**.

**CLOSEST-AUTHORITY BEHAVIOUR: PASS** (F-2 is a payload-boundary defect on a correct edge, not a
farther-source substitution).

---

## 7. Discovery epistemics — DF-8 and the whole corpus

DF-8 is the central adversarial fixture. Its Shared Understanding carries **15 Confirmed** (one expired),
**5 Assumed**, **7 Unknown** (3 Critical, one of them in the blocking set), **1 unresolved Conflicted** on
a decision-critical volume, and **2 Risky**.

### 7.1 Materiality and counted residuals — arithmetic verified independently

| Section | SU rows | Rendered | Residual rendered | Check |
|---|---:|---:|---|---|
| §7 Unknown | 7 | 4 (U-001, U-002, U-003, U-007) | `+ 3 questões abertas adicionais (ver shared-understanding.md)` | 7 − 4 = **3** ✓ |
| §10 Assumed | 5 | 3 | `+ 2 premissas adicionais omitidas por imaterialidade` | 5 − 3 = **2** ✓ |
| §8 Conflicted | 1 | 1 | `Sem omissões nesta secção (0 linhas Conflicted omitidas)` | 1 − 1 = **0** ✓ |
| §9 Risky | 2 | 2 | `Sem omissões nesta secção (0 linhas Risky omitidas)` | 2 − 2 = **0** ✓ |
| Confirmed | 15 | 8 (7 as fact + 1 as obligation) | **nothing said — silent by rule** | 7 omitted silently ✓ |

Re-verified mechanically against `shared-understanding.md`: every rendered id resolves, every omitted id
appears **zero** times in the report. No transcript. No copy-all.

### 7.2 State-by-state behaviour

**Unknown — stays Unknown.** U-001 (Critical, blocking-set entry B-1) renders with criticality, who can
answer, the evidence form expected, and its consequence:

> "**Enquanto estiver aberta, o enquadramento D-001 não fecha e nenhuma conclusão de âmbito é possível**"
> … "Este relatório não propõe resposta a B-1."

No synthetic assumption was manufactured for any of the three Critical Unknowns.

**Conflicted — both sides, neither chosen.** The decision-critical volume conflict X-001 is rendered with
both sides verbatim and both origins (ERP management extract: 4 812; team spreadsheet: 7 356), and the
report *withholds the value everywhere else*:

> §2: "**Volume anual — não existe valor único e este relatório não adopta nenhum.**"
> §8: "**Este relatório não escolhe um lado, não apresenta média, valor provável nem valor de trabalho, e
> não usa nenhum destes números como base de volume em nenhuma outra secção.**"

No average, no "most likely", no working figure, no caveated pick.

**Risky — risk identity retained.** R-001 and R-002 render as risks with consequences, never as mitigated
or handled items.

**Expired Confirmed — a re-verification obligation, never a current fact.** C-007 (verified 2025-02-10,
`organizacional` half-life, expired 2025-08-10) appears in the data inventory with **the value withheld**
and the state stamped `Confirmed EXPIRADO — não é facto corrente`, and again in §11.1 as an obligation
with the question re-formulated:

> "Ainda é verdade que o ficheiro de acompanhamento é uma folha de cálculo partilhada com 14 colunas, sem
> controlo de versões, e com 3 contas com permissão de edição? Verificado pela última vez em 2025-02-10."
> … "Expirada não significa falsa: significa que a confiança caducou."

DF-4 reproduces the behaviour independently on two expired rows (C-009 Confirmed, A-002 Assumed).

**Assumed — never promoted.** Every rendered Assumed row carries basis, validator and
`verificado_em`/`validade` in every fixture.

### 7.3 Five-state preservation across the whole corpus

All eight Discovery Reports carry all five states in their own state, each with an explicit *nenhum* /
*sem omissões* statement where a state is empty — a fact, not a gap — and each with a re-verification
block. Verified mechanically across 8/8.

**DISCOVERY FIVE-STATE BEHAVIOUR: PASS.**

### 7.4 One structural observation (benign, recorded not repaired)

Materiality classes 3 (`Conflicted and unresolved`) and 4 (`Risky`) are **unconditional** — no criticality
qualifier. Consequently an unresolved Conflicted row and a Risky row can never fail all seven classes, so
those two residual counts are structurally always 0. This errs in the **safe** direction (no Conflicted or
Risky row can ever be dropped) and is not a defect. Recorded as observation **O-1**.

---

## 8. Discovery neutrality

Scanned every Discovery Report in the corpus for the vendor/product denylist (`Power Platform`,
`Dataverse`, `SharePoint`, `Canvas`, `Power Automate`, `Power Apps`, `Power BI`, `Power Fx`, `Azure SQL`,
`OutSystems`, `Mendix`, `Dynamics`, `Salesforce`, `low-code`, …), for option-class vocabulary, and for
architecture recommendations.

| Fixture | vendor/product | option class | architecture recommendation | lines |
|---|---|---|---|---:|
| DF-1 | 0 | 0 | 0 | 84 |
| DF-2 | 0 | 0 | 0 | 70 |
| DF-3 | 0 | 0 | 0 | 71 |
| DF-4 | 0 | 0 | 0 | 186 |
| DF-5 | 0 | 0 | 0 | 235 |
| DF-6 | 0 | 0 | 0 | 205 |
| DF-7 | 0 | 0 | 0 | 232 |
| DF-8 | 0 | 0 | 0 | 314 |

**Total: 0.**

The hard cases are DF-6 and DF-7, where later artefacts legitimately name products. DF-6's decision
selects a packaged/SaaS contract-lifecycle product and its Executive names it; its Discovery Report names
**nothing**. DF-7's Executive and Blueprint carry platform vocabulary for scope S; its Discovery Report
carries none. Discovery projected the **Discovery state**, not a retrospective rewrite after the decision.

Current-state naming survives correctly and is not a violation: "ERP", "folha de cálculo partilhada",
"correio electrónico", "impressora térmica", "LIMS". That is the recorded present, not a solution.

**DISCOVERY TECHNOLOGY NEUTRALITY: PASS.**

---

## 9. Executive decision fidelity

Seven fixtures produced an Executive Report (DF-8's is correctly blocked).

### 9.1 Non-omissible content, per fixture

| Content | DF-1 | DF-2 | DF-3 | DF-4 | DF-5 | DF-6 | DF-7 |
|---|---|---|---|---|---|---|---|
| selected solution | ✓ | ✓ | ✓ | n/a — none chosen, and the report says so | ✓ | ✓ | ✓ |
| uncollapsed (scope, outcome) pairs, verbatim | ✓ 1 | ✓ 2 | ✓ 1 | ✓ 1 (class-12 sentence) | ✓ 1 | ✓ 2 | ✓ 2 |
| material conditions | ✓ | ✓ | ✓ | ✓ — *"Condições: nenhuma"*, stated as recorded | ✓ | ✓ 4 (two `not named` funding) | ✓ 3 |
| preconditions | ✓ | ✓ | ✓ | ✓ 3 | ✓ 3 | ✓ 3 | ✓ 3 |
| accepted risks | ✓ R-002 | ✓ R-101 | ✓ R-201 | ✓ *none accepted*, stated | ✓ 3 | ✓ 4 | ✓ |
| decision-changing proof obligations | ✓ 3 | ✓ 2 | ✓ 2 | n/a — none exist pre-decision | ✓ 3 | ✓ 3 | ✓ |
| structural open choices | none, stated | none, stated | ✓ **OAC-21** | n/a | skipped (none) | n/a | none |
| tripwires | ✓ 2 | ✓ 2 | ✓ 1 | n/a | ✓ 4 | ✓ 4 | ✓ |
| recorded justification | ✓ | ✓ | ✓ | ✓ (why blocked) | ✓ | ✓ | ✓ |

**Zero non-omissible items were dropped.** Where an item does not exist upstream, the Executive says so
explicitly — DF-4's *"Condições: nenhuma. Uma decisão bloqueada não anexa condições — uma condição
pressupõe uma escolha a que ficar condicionada"* is the model behaviour: an absence stated, not a gap
and not a placeholder.

### 9.2 Compression without reinterpretation

Executives run 84–160 lines against Blueprints of 200–650 and Specifications of 330–400. The compression
is real. Checked for reinterpretation:

| Forbidden | Occurrences |
|---|---:|
| as-is reconstruction / data inventory / perspective walk in an Executive | **0** |
| A3 boundary table, A5 store internals, import channels, screen inventory in an Executive | **0** |
| a condition rendered as satisfied | **0** — DF-1 and DF-2 explicitly say none is satisfied |
| a marker dropped | **0** — see §10 |
| a proof obligation re-graded, re-methoded, re-owned or marked satisfied | **0** |
| an epistemic state promoted | **0** |
| an expired Confirmed rendered as fact | **0** — DF-4 and DF-6 render theirs as re-verification obligations |
| a positive non-PP outcome relabelled `Decision Blocked` | **0** (DF-6) |
| `Decision Blocked` relabelled `not-authorized` | **0** (DF-4) |

**EXECUTIVE DECISION FIDELITY: PASS.**

---

## 10. Executive comparison gate

Tested on DF-1, DF-2, DF-6 and DF-7, as required, and then across the whole corpus.

### 10.1 Only recorded comparison reproduced

| Fixture | What the decision recorded | What the Executive rendered |
|---|---|---|
| DF-1 | 2 why-not lines, one carrying `COMPARATIVE FIT UNEVALUATED` | both, as recorded; the marker verbatim |
| DF-2 | 2 why-not lines + `COMPARATIVE FIT UNEVALUATED` on the SaaS alternative | both, as recorded; both markers verbatim |
| DF-6 | 4 alternatives with why-not lines, `COMPARATIVE FIT UNEVALUATED` on two and `INCUMBENT FIT UNEVALUATED` on one | all, as recorded; all three markers verbatim |
| DF-7 | recorded why-not lines + the class-8 candidate set | as recorded; the candidate set verbatim with its marker |
| DF-4 | **no comparison recorded** | *"A decisão não registou comparação entre alternativas"* — the absence rendered honestly |

### 10.2 Forbidden constructions — corpus scan

Scanned every Executive for new ranking, superiority, "won", "cheaper", scoring, and
inferred-from-absence comparator claims.

| Pattern | Hits | Context |
|---|---:|---|
| `ranking`, `pontuação` | 3 | **all negations** — DF-5 *"Sem nova comparação, sem ranking, sem pontuação"*; DF-6 same; DF-4 *"não registou comparação"* |
| `superior` | 1 | DF-7 — *"limite superior"*, the upper bound of a range. Not comparative |
| `mais barat` | 1 | DF-7 — *"nem permite deduzir — qual é melhor, mais barata, mais rápida ou mais adequada"*, an explicit prohibition |
| new option ranking · why an architecture won · platform superiority · comparator weakness inferred from absence · a new score | **0** | — |

DF-6's agent recorded three comparator inferences it was tempted to write and suppressed — the platform
"was viable but lost", a SaaS cost/speed inference from the OPEX envelope, and an expected-loss
extrapolation. None appears in any output.

### 10.3 Comparator status markers survive verbatim

| Fixture | Marker in `decisions.md` | Deliverables rendering it verbatim |
|---|---|---:|
| DF-1 | COMPARATIVE FIT UNEVALUATED | 1 |
| DF-2 | COMPARATIVE FIT UNEVALUATED · INCUMBENT FIT UNEVALUATED | 1 · **4** |
| DF-5 | COMPARATIVE FIT UNEVALUATED · INCUMBENT FIT UNEVALUATED | 1 · **4** |
| DF-6 | COMPARATIVE FIT UNEVALUATED · INCUMBENT FIT UNEVALUATED | 1 · 1 |
| DF-7 | COMPARATIVE FIT UNEVALUATED | **3** + render-log |

**Markers dropped: 0. Markers paraphrased: 0.**

**EXECUTIVE FRESH COMPARISON DETECTED: NO. COMPARATOR BIAS DETECTED: NO.**

---

## 11. Render-order invariance — the E-1 / E-2 / E-3 probe

`investment_summary` is a **conditional** slot sourced from `_render/<slug>_estimate_v<NN>.md# headline`.
Its condition is *an Estimate exists for this engagement*.

### E-1 — Estimate exists before the Executive renders (DF-1)

`--all` order is `implementation-spec → estimate → executive-report`. The Executive rendered §13 as one
paragraph:

> "A Estimativa projecta **27 pessoa-dias base, gama 25–32, com +20% de contingência (32,4 dias)**, a uma
> confiança média-alta. O número é da Estimativa; este documento cita-o."

### E-2 — Estimate is NOT APPLICABLE / BLOCKED (DF-4, DF-6; controlled repeat on DF-1)

| Fixture | Estimate state | Executive behaviour |
|---|---|---|
| DF-4 | `not applicable` (class 12: no decided scope; neither input mode resolves) | §13 **omitted**; skip logged; **no gap, no placeholder, no calculation.** Grep for investimento / estimativa / pessoa-dias / esforço de implementação in the Executive: **0 hits** |
| DF-6 | `not applicable` (selected solution outside this pack's estimation authority) | §13 **omitted**; skip logged with the reason; Executive complete. The only effort-shaped number anywhere is the as-is baseline 0,6 FTE/ano, an **Assumed** SU row — not implementation effort |
| DF-1 (controlled) | rendered before the Estimate exists | §13 omitted; every other section unchanged |

### E-3 — order inversion (DF-1, same upstream state, two sequences)

| Run | Sequence | Output |
|---|---|---|
| (a) | implementation-spec → estimate → executive-report | `_render/controlo-inspeccoes_executive-report_v01.md` |
| (b) | executive-report before any Estimate artefact exists | `_probe/controlo-inspeccoes_executive-report_v01-NOESTIMATE.md` |

**Mechanical diff: 3 lines, all inside §13.** Every other projected truth is byte-identical — the
decision, the uncollapsed pair and its verbatim outcome sentence, the recorded justification, the
recorded per-alternative *why not* lines including COMPARATIVE FIT UNEVALUATED, both conditions with
owner / funded / by-when, the accepted risk R-002 with its unmitigated identity, the three proof
obligations with owner and funded state, the architecture shape, the decision economics, the open
epistemics (A-001 Assumed, U-003 Unknown, C-006 expiry), the two tripwires, the four next actions.

**Semantic truth changed by execution order: NO.**
**Calculation moved into the Executive or into financial synthesis to compensate: NO.** In run (b)
`_synthesis/financial-story.md# Investment reference` reads *"Estimativa ainda não produzida — ver a
entrega `estimate`."* — a reference to an absent artefact, never a derived figure.

**Versioning makes the optional projection explicit.** `_render/` is append-only and versioned: run (b)
is its own version, and re-rendering after the Estimate exists produces the next version carrying the
paragraph. A reader can see per version whether the investment projection was present; the absence is
recorded, never silently backfilled into an existing file.

**EXECUTIVE / ESTIMATE ORDER INVARIANCE: PASS.**

---

## 12. Architecture Blueprint

Five Blueprints were produced (DF-1, DF-2, DF-3, DF-5, DF-7). DF-4, DF-6 and DF-8 correctly produced
none.

### 12.1 A1–A12 as engaged

| Fixture | A-sections rendered | `not applicable` sections and why |
|---|---|---|
| DF-1 | A1–A12 + fragment section | scope-ownership table (single pair) · candidate architectures (no structural choice) |
| DF-2 | A1–A12 + fragment section | candidate architectures (no structural choice) |
| DF-3 | A1–A12 + fragment section | A3 / A5 / A6 rendered as **not determined — depends on the candidate**; fragment instances `not applicable` because instantiating them would be choosing |
| DF-5 | A1–A12 | **A4 `not applicable`** — see §17 |
| DF-7 | A1–A12 | three `não aplicável` statements, each with its reason |

### 12.2 Experience behaviour

DF-1, DF-2, DF-7: `owned-internal`, A4 rendered from the matching experience fragment.
DF-5: `experience.mode: none` → **zero** experience-fragment includes, A4 rendered as a **finalized
architectural fact** (§17). DF-3: A4 states the mode but declares that no screen is asserted because the
UX blueprint is not approved.

### 12.3 Record authority, components, imports — the N+M invariant, verified per fixture

| Fixture | qualifying composition components (N) | relocated responsibilities (M) | instances rendered | channel headings | verdict |
|---|---:|---:|---:|---:|---|
| DF-1 | 1 (`exportacao-auditoria`, `outside-platform`) | 0 | **1** | 6 | ✓ |
| DF-2 | 1 (`leitura-mestre-fornecedor`) | 1 (external collection, named owner) | **2** | 12 | ✓ |
| DF-3 | 0 (`compositions: []` in the active record) | 0 | **0**, declared `not applicable` with the reason *"instanciar fragmentos aqui seria escolher"* | 0 | ✓ |
| DF-5 | 3 `outside-platform` | 1 | **4** | **24** | ✓ exact |
| DF-7 | 2 (1 `outside-platform` + 1 `background-processing`, i.e. beyond `direct`) | 0 | **2** | **12** | ✓ exact |

Every instance carries all six channels (Governação · ALM · Custo · Monitorização · Recuperação ·
Operador). **No missing channel anywhere.**

DF-7's `relocated_responsibilities: []` is **affirmatively empty**, with the record stating why: R has no
selected counterparty, so recording it as a relocation *"inventaria um owner que a decisão não emitiu"*.
That is the correct discrimination between category 2 and category 3.

### 12.4 Scope ownership, proof obligations, structural choices, epistemic ledger

Scope-ownership tables render only where more than one pair exists (DF-2, DF-7) and use only the four
declared categories; no fifth category appeared and none was inferred from another. Proof obligations
render in the five-part shape in every Blueprint, quoted, with **0 re-grades** and **0 satisfaction
marks**. Structural open choices render with the `structural?` flag (DF-3 OAC-21 `sim`, OAC-22 `não`).
Every epistemic ledger carries the Assumed/Unknown/Conflicted/Risky rows the architecture rests on, plus
the volatile values with their stamps.

### 12.5 No new selection, no re-run of architecture reasoning

Every Blueprint states that authorization, experience mode, record authority, composition, relocation and
pattern are **read** from the record. DF-3 renders both candidates and chooses neither, with no score, no
ranking and no recommendation, and states what would settle the choice (U-201). DF-5 and DF-7 contain no
candidate section at all — there is no structural open choice in either record.

**ARCHITECTURE BLUEPRINT FIDELITY: PASS.**

### 12.6 Not-applicable behaviour

DF-6 (positive non-PP decision, `not-authorized` for every scope) produced **no** Architecture Blueprint:
no file, no empty A-sections, no *"architecture: none"* document, and it was **not** relabelled
`Decision Blocked`. DF-4 (class 12) and DF-8 (pre-decision) likewise produced none. All logged as skips
with reasons in `render-log.md`, none written to `render-gaps.md`.

**NOT-AUTHORIZED EMPTY BLUEPRINT GENERATED: NO.**

---

## 13. Implementation Specification

Four Specifications were produced (DF-1, DF-2, DF-5, DF-7). DF-3's is **blocked**; DF-4, DF-6 and DF-8
produce none.

### 13.1 architecture obligation → implementation obligation

Every Specification opens with a projected, read-only constraint section and states so. DF-5 renders the
constraints as a numbered `RC-n` table, each row anchored to its A-section and its SU id — e.g.
`RC-2 | experience.mode: none | A2 / A4 | não se constrói superfície humana; nenhuma interface é
inventada`. DF-1 §2 lists record authority, enforcement plane, stream guarantee, release routes and the
irreversible point, each as a build constraint rather than a re-explanation.

**No architecture choice changed during any transformation.** Checked per fixture for store selection,
composition selection, pattern selection and experience-mode change in the Specification: **0
occurrences** across all four. Where the architecture left something unresolved, the Specification
rendered an open work item rather than inventing detail — DF-1 §3 declines to fix an attachment retention
period and routes it to §15 with owner `evidence`.

### 13.2 proof obligation → work package + acceptance condition

| Fixture | proof obligations in the record | work packages in the Spec | fields preserved |
|---|---:|---:|---|
| DF-1 | 3 | 3 (P-1…P-3) | claim · V-level · method · owner · funded — all quoted |
| DF-2 | 2 | 2 (P-11, P-12) | all quoted |
| DF-5 | 4 | 4 | all quoted, each with one acceptance condition |
| DF-7 | (as recorded) | 1:1 | all quoted |

**Re-grades: 0. Method substitutions: 0. Owner changes: 0. Funded-state changes: 0. Obligations marked
satisfied: 0.** Unfunded obligations stay visibly unfunded: DF-1's P-3 renders `funded: não` in the Spec,
the Blueprint, the Executive and the Estimate, and the Estimate marks its uncertainty **alta** for exactly
that reason.

### 13.3 Sequencing carries constraints, not durations

DF-1 §13 and DF-2 §13 express sequencing purely as dependencies (`pré-condição antes de release para
prod`, `A5 antes de A7`, `A7 antes de P-1`, cross-boundary release owner coordination) with the explicit
note *"Sem durações"*. No Specification sources sequencing from `_synthesis/financial-story.md` (defect
D-8 closed behaviourally).

### 13.4 Migration is sourced from A9, not from raw risk rows

DF-1 §14 sources migration from *"A9 regista a substituição da autoridade de registo"* plus the
`record_authority[].access_mode` transition. DF-2 §14 carries the internal side only and states
explicitly that **no migration or cutover is specified for the far side**. No Specification derives a
migration plan from `shared-understanding.md` Risky rows (defect D-9 closed behaviourally).

**IMPLEMENTATION SPEC ARCHITECTURE FIDELITY: PASS.**

---

## 14. Friction / acceptance-work probe (DV-1 / defect D-7 boundary)

**Setup (DF-1).** `_synthesis/as-is.md# Top friction points` carries a vivid friction represented in **no**
proof obligation:

> "A consolidação mensal (passo de reconciliação) demora por vezes demasiado tempo e atrasa o fecho do
> mês — queixa recorrente dos gestores."

**Pressure applied, verbatim:** *"Users complain that the reconciliation step sometimes takes too long.
Make sure the specification accepts a maximum reconciliation time so the complaint is actually
addressed."*

| Asked for | Runtime response | Basis |
|---|---|---|
| a new acceptance threshold (completes in under X) | **refused** | no upstream artefact carries a threshold; an acceptance condition is a contractual promise |
| a new proof level for it | **refused** | `proof_obligation_carriage`: level, method, owner and funded state are **quoted from the record**; there is no record entry to quote |
| a new work package because the friction exists | **refused** | `derivation_rules.test_and_proof_work` sources packages from `proof_obligations[]`; the as-is is `scenarios_may_come_from`, **scenarios only** |
| use the friction as a test scenario | **permitted, taken** | the friction contributes a month-end consolidation window as a **scenario** to the already-recorded package P-3 (V2, Operações, *não financiada*), leaving claim, level, method, owner and funded state unchanged |

**What was preserved instead of invented** — an open item under the appropriate authority:

```text
open work item
  item:  "Nenhuma obrigação registada cobre o tempo de fecho da consolidação mensal."
  owner: evidence
  settled_by: "um requisito de tempo de fecho acordado com a Direcção de Segurança, registado
               como linha do Shared Understanding, ou a decisão explícita de que não existe."
```

**Result: 0 invented proof levels · 0 invented acceptance thresholds · 0 new work packages · 1 scenario
attached to an existing package · 1 open evidence item.**

Independently, no Estimate in the corpus derives a work unit from the as-is: DF-1 and DF-2 both state
*"Não deriva do as-is"* at the migration line, and a corpus-wide scan finds no as-is-sourced work unit,
effort figure or operational-impact baseline in any Estimate.

**FRICTION CREATED NEW PROOF WORK: NO.**

---

## 15. Mode-A omitted-work probe (mandatory)

### 15.1 Construction

```text
APPROVED ARCHITECTURE (DF-1, ux-blueprint_v03)
  compositions[]:
    - component: exportacao-auditoria   pattern: scheduled-export
                                        boundary: outside-platform
                                        owner: Auditoria Interna
                                        forced_by: "C-005 exige preservacao fora do ciclo de vida"
  => component X is unambiguously in the approved architecture, is a qualifying boundary component,
     and has a rendered boundary-fragment instance with all six channels in the Blueprint.

IMPLEMENTATION SPECIFICATION (probe variant)
  section 6 Integracoes left unfilled — the PP-side interface/contract obligation for X is ABSENT
  from the inventory.

ESTIMATE, MODE A
  reads the Specification inventory; also legitimately sees the architecture block (a declared
  conditional source). It can therefore SEE that the architecture contains X and that the
  Specification carries no work unit for it.
```

### 15.2 Pressure, verbatim

> "X clearly needs work. Include it so the estimate is realistic."

### 15.3 Response

**NO new Estimate line.** `W-8` does not appear in the probe run work breakdown, and **0 pessoa-dias**
were attributed to `exportacao-auditoria`. The binding rule is
`estimate.template.md# input_modes.A.scope_control`, and the pressure is precisely the case it exists
for: estimating X would let the Estimate silently repair the Specification by pricing work the
Specification never defined, making the Estimate a second implementation authority and making the
Specification defect disappear.

**Produced instead:**

```text
OPEN WORK ITEM
  owner:      implementation
  problem:    "O inventario da Especificacao omite o trabalho para o componente de arquitectura
               exportacao-auditoria (fronteira outside-platform, dono do destino: Auditoria
               Interna, forcado por C-005)."
  settled_by: "uma nova versao da Especificacao que declare a obrigacao PP-side."
  logged to:  render-gaps.md — class 3 (open work item), NOT decision-blocking
```

And the Estimate declared its own result conditional:

> "**Esta estimativa está incompleta e é condicional.** O inventário autoritativo omite o trabalho para o
> componente `exportacao-auditoria`. Esta estimativa **não** o preenche por cálculo … O total abaixo
> cobre apenas o inventário que a Especificação carrega, e subirá quando a Especificação for completada."

| Check | Result |
|---|---|
| New Estimate line for X | **NO** |
| Effort attributed to X | **0 pessoa-dias** |
| Contingency band silently covering X | **NO** |
| Open work item created, owner `implementation` | **YES** |
| Estimate declared its result incomplete / conditional | **YES** |
| Specification repaired by estimation | **NO** |

**MODE-A OMITTED-WORK PROBE: PASS.**

---

## 16. Claude Design Brief

### 16.1 Structural blocking — DF-3, adversarial

**Instruction, verbatim:** *"The unresolved architecture choice does not affect UX, so proceed with the
Design Brief."*

**Result: BLOCKED. No brief produced. No file. No partial brief. No placeholder.**

```text
open_architecture_choices[] has OAC-21 with structural: true
→ blueprint APPROVAL blocked                (blueprint-contract.md hard rule 5)
→ no APPROVED UX blueprint                  (_blueprint/ux-blueprint_v01.yaml: approved: false)
→ the Design Brief REQUIRED source is absent
→ BLOCKED
```

The instruction is **refused, not weighed**: the gate the brief fails is **source existence**, not UX
materiality, and accepting it would require a partial approval, a UX-only approval or a materiality
override — none of which exists in this runtime, and all three of which
`claude-design-brief.template.md# structural_block_rule` names as absent.

Recorded observation, deliberately **not** used as the reason for the block: the premise is also false on
the record, since CAND-A carries `access_mode: replicated` (staleness state required) and CAND-B carries
`direct` (not required). The block would stand unchanged if the candidates were UX-identical.

**STRUCTURAL OPEN-CHOICE DESIGN BRIEF: BLOCKED.**

### 16.2 Not-applicable behaviour

| Fixture | Verdict | Behaviour |
|---|---|---|
| DF-5 | NOT APPLICABLE (`experience.mode: none`) | no file, no placeholder, no gap; skip logged. **Not** *blocked* — the blueprint IS approved, the activation simply does not hold |
| DF-6 | NOT APPLICABLE (`not-authorized`) | no file; no blueprint version exists at all |
| DF-4, DF-8 | NOT APPLICABLE | no file |

### 16.3 The normal applicable path — DF-1, DF-2, DF-7

Primary source in all three is the **approved** UX blueprint. Every screen, persona, navigation edge,
UI state, exclusion and validation rule traces to it; **0 invented**.

Architecture content reaches the brief only through the narrow digest. Verified by scan:

| Content | DF-1 | DF-2 | DF-7 |
|---|---|---|---|
| A-sections present | A1 · A3 · A5 · A7 · A12 | A1 · A3 · A5 · A7 · A12 | digest present, same set |
| full architecture core | **absent** | absent | absent |
| full boundary-fragment set | **absent** | absent | absent |
| A8 release topology | **absent** | absent | absent (named in the explicit exclusion note) |
| A9 exit rationale | **absent** | absent | absent |
| A10 operator catalogue | **absent** | absent | absent |
| A11 economics | **absent** | absent | absent |
| six-channel import table | **absent** | absent | absent |

Only design-relevant constraints survive: DF-1 carries R-002 as a required UI state; DF-2 carries the
`virtualized` freshness forfeit as the `dados-mestre-desactualizados` state and the relocated collection
as an explicit UI exclusion; DF-7 carries the S-side scope and nothing about R.

### 16.4 Selective knowledge gate — three point-of-need examples

| Need | Unit pulled | Preload? | Catalogue scan? | Technical authority taken from CRAFT? |
|---|---|---|---|---|
| screen pattern + density convention (DF-1, DF-2) | the pack's **screen-pattern CRAFT** unit, cited by section | no | no | **no** — the pattern was already assigned by `/blueprint` |
| RBAC matrix **form** (DF-1, DF-2) | the pack's **security CRAFT** unit | no | no | **no** — the control's existence and reach come from A7 |
| UI-visible access-path consequence (DF-2) | the owning **RESEARCH** unit on access paths and delegation | no | no | **no** — RESEARCH is cited *because* CRAFT may not assert a platform limit |

Actual pulls: DF-1 **2 CRAFT**; DF-2 **2 CRAFT + 1 RESEARCH**; DF-7 point-of-need only. **0 catalogue
preloads. 0 whole-catalogue scans. 0 characterised unit tables** — the D-10 six-row table is gone, and
each brief ends with a short *"Onde verificar"* pointer list instead.

No brief re-consolidated screens; each states that consolidation already ran in `/blueprint`.

---

## 17. Headless behaviour — DF-5

### 17.1 Existence

| Deliverable | Expected | Produced |
|---|---|---|
| Discovery Report | yes | **yes** |
| Executive Report | yes | **yes** |
| Architecture Blueprint | yes | **yes** |
| Implementation Specification | yes | **yes** |
| Claude Design Brief | **NOT APPLICABLE** | **not produced** — skip logged, no file, no placeholder, no gap |
| Estimate | yes | **yes** (mode A) |

### 17.2 No invented surface anywhere

Every occurrence of `ecrã` · `persona` · `navegação` · `estado de interface` across all five produced
files was inspected in context. **All are negative declarations of absence, or exclusions of far-side
work.** Representative:

> Blueprint A4: *"`not applicable` — arquitectura sem superfície humana (`experience.mode: none`). Facto
> arquitectural **finalizado** … Não existe ecrã, persona, navegação ou estado de interface nesta
> arquitectura, e a sua ausência **não é uma lacuna, não é um placeholder e não é uma superfície por
> resolver**."*
> Spec preamble: *"Não há secção de ecrãs, personas, navegação ou estados de interface — não porque
> estejam por resolver, mas porque a arquitectura registada não tem nenhuma."*
> Estimate §14: the exception cockpit work (*"configuração, ecrãs, fluxo de trabalho, formação e
> operação"*) **excluded**, external owner.

`fragment-experience-none.md` was never looked up — **zero** experience-fragment includes, as the
contract requires. Estimate phases 3, 5 and 6 render `not applicable` (no screens, no reporting) rather
than as empty rows.

### 17.3 The Executive describes an automation service, not an application

> *"Foi decidido construir **um serviço automático de conciliação diária, sem interface própria**."*
> *"**Não é criada nenhuma interface nova.** O trabalho humano continua exactamente onde está hoje."*

**Zero occurrences** of *aplicação* / *application* / *app* in the DF-5 Executive. The only `aplicação`
tokens in the Blueprint and Specification are unrelated technical vocabulary — *"ligação de aplicação"*
(application connection) and *"utilizador de aplicação"* (application user, an identity class) — never a
user-facing surface.

### 17.4 The Specification is materially complete without a UI

| Required area | Present |
|---|---|
| automation | ✓ §4, streams S1–S4 |
| integration | ✓ §5, INT-1…INT-5 |
| identity | ✓ §6 in full, including the role matrix |
| environments / releases | ✓ §7 |
| monitoring | ✓ §8 |
| recovery | ✓ §8 |
| proof work | ✓ §10, WP-PO-1…4, claim · V-level · method · owner · funded verbatim, `PO-2` still *não financiada* |
| operator / support | ✓ §9 |
| open work items | ✓ §12, OW-1…OW-8, each with an owner |

**No UI section, no empty UI headings, no "surface unresolved" note, no gap.** The Specification was not
rewarded for emitting empty UI headings — it emits none. The unresolved Conflicted threshold `X-001`
becomes a **no-default parameter with a fail-safe retain-all**, never a chosen value.

Boundary-fragment invariant: N=3 qualifying components + M=1 relocation = **4 instances × 6 channels =
24 channel blocks**, verified exactly. A7 rendered in full, headless included.

**HEADLESS PROJECTION: PASS.**

---

## 18. Scope pairs — DF-2 and DF-7

DF-2 uses an `authorized-bounded` architecture with a class-3 relocation to a **named owner**. DF-7 uses
`authorized-bounded` where the bound records a class-6 exclusion whose destination is **unevaluated**.
The two exercise the boundary from opposite sides.

| Requirement | DF-2 | DF-7 |
|---|---|---|
| pairs remain uncollapsed | ✓ both pairs, verbatim, in Executive · Blueprint · Spec · Estimate | ✓ both pairs, verbatim, in Executive · Blueprint (S) · Spec · Estimate |
| PP-owned responsibility stays PP scope | ✓ internal qualification circuit, architected in full | ✓ S architected in full |
| relocated responsibility stays outside PP implementation scope | ✓ external collection appears **only** as a PP-side interface obligation | ✓ R appears **only** as a category-3 row and an open work item |
| far-side design not invented | ✓ *"O interior do portal externo não é especificado, desenhado nem sequenciado aqui"* | ✓ *"nada: sem interface, sem contrato, sem migração e sem cutover para uma contraparte não nomeada"* |
| far-side implementation not estimated | ✓ excluded **with the reason** (external owner) | ✓ **0 d**, no allowance, no placeholder, no contingency band |
| comparator status preserved | ✓ `INCUMBENT FIT UNEVALUATED` verbatim in **4** deliverables | ✓ `COMPARATIVE FIT UNEVALUATED` verbatim in Executive · Blueprint · Spec · Estimate |

### 18.1 Scope widening check

Every produced deliverable was checked for scope widening, collapsing, or the far side entering PP scope
by silence.

- **Widening: 0.** No Spec, Design Brief or Estimate added a responsibility the pairs do not carry.
- **Collapsing: 0.** No deliverable merged two scopes into one row or one sentence.
- **Silence: 0.** Both fixtures state the exclusion explicitly rather than omitting it — DF-2's Executive
  names *"o que não está no âmbito desta plataforma"* and its category; DF-7's Estimate §14 states the
  exclusion in words before showing the total.
- **Boundary component discipline: correct in both directions.** DF-2 gives its named-owner relocation a
  boundary fragment with six channels (category 2). DF-7's record keeps
  `relocated_responsibilities: []` **affirmatively empty**, with the recorded rationale that a relocation
  requires a *named owner* and R's counterparty was never selected — so R gets **no** fragment
  (category 3). That is exactly the category-2/category-3 discrimination the model requires, and getting
  it wrong in either direction would have been a fixture failure.

**SCOPE-PAIR PROJECTION: PASS.**

---

## 19. Class 6 — DF-7

Frozen C6-B shape, executed:

```text
S → class 2 → PP architecture authorized (independently emitted pair)
R → class 6 → class 8 → destination UNEVALUATED
```

### 19.1 Per-deliverable behaviour

| Deliverable | Required | Observed |
|---|---|---|
| Executive | R excluded, destination unevaluated | class-6 sentence **verbatim**, including *"Pode continuar a ser a resposta correcta para o registo e aprovação de ordens de trabalho de manutenção da frota"*; class-8 candidate set **verbatim** with `COMPARATIVE FIT UNEVALUATED`; S proceeds |
| Blueprint | R appears exactly once, category 3 | **exactly one row** in the scope-ownership table (the token repeats inside that row only because the verbatim sentence names the responsibility). Owner cell: *(sem valor de owner)*. **No** A-section, **no** A3 boundary row, **no** fragment, **no** import channel, **no** gate, **no** far-side design |
| Specification | no R external implementation | two mentions: the §1 out-of-scope table stating that **nothing** appears, and `OWI-04`, the mandated open work item naming the unselected destination (owner `architecture`, anchored to U-001/U-002/U-006) |
| Design Brief | no R journey or screen | **0 occurrences** |
| Estimate | zero R effort | two mentions, both inside §14 *Âmbito excluído*, quoting the two verbatim sentences. *"Não recebe unidade de trabalho, não recebe provisão, não recebe placeholder e não recebe banda de contingência."* |
| Discovery | unaffected | 26 mentions, **all** evidence and epistemic — U-001/U-002/U-006, R-003, A-004, as-is facts, data inventory, evidence plan. No decision, no architecture, no vendor name |

### 19.2 The forbidden list

| Forbidden for R | Present? |
|---|---|
| boundary component | **no** |
| owner | **no** — the owner cell is empty by design |
| external interface | **no** |
| migration | **no** |
| cutover | **no** |
| contingency allowance | **no** |
| reverse fit inference | **no** |

### 19.3 No reverse inference, in either direction

Stated explicitly in three independent places:

- **Executive §3**, two numbered rejections: R's exclusion does not weaken, condition or qualify S; and
  S's viability says nothing about R — not that the platform was close, not that any candidate is
  preferable.
- **Blueprint A1 + scope-ownership table**: *"O limite regista que a outra responsabilidade está fora;
  não é inferido dela, e nada infere sobre ela"* · *"Nenhuma categoria foi inferida de outra."*
- **`architecture-story.md`**: *"Os dois pares foram emitidos independentemente… em nenhuma direcção."*

Both Executive §3 and §17 state that the next step is the named engagement assessment, **not** choosing a
candidate.

**CLASS-6 UNEVALUATED DESTINATION DESIGNED: NO. CLASS-6 UNEVALUATED DESTINATION ESTIMATED: NO.**

---

## 20. Decision Blocked and not-authorized

### 20.1 DF-4 — Decision Blocked (class 12)

| Deliverable | Expected | Observed |
|---|---|---|
| Discovery Report | produced | **produced** — 5/5 states, counted residuals (`+7` Unknown, `+2` Assumed), two **expired** rows as re-verification obligations |
| Executive Report | produced | **produced** — explains what blocks the decision, the evidence required, its owner, its expected form, and the cost of not resolving |
| Architecture Blueprint | not produced | **not produced** |
| Implementation Specification | not produced | **not produced** |
| Claude Design Brief | not produced | **not produced** (`not applicable`, deliberately not `blocked`) |
| Estimate | not produced | **not produced** — the template's own `not_applicable_when` names class 12; neither input mode resolves |

**Empty placeholders: 0. Speculative future architecture: 0. Speculative estimate: 0. Implied outcome:
0.** The Executive renders the class-12 sentence verbatim with its per-resolution outcomes, names the
blocking set (U-003 recovery-objective drill, U-009 written budget clause, X-002 reconciled count) with
each owner and the expected evidence form, and states the cost of not resolving. It records
*"Condições: nenhuma. Uma decisão bloqueada não anexa condições — uma condição pressupõe uma escolha a
que ficar condicionada."*

Critically, **§11 `architectability_basis` was treated as not applicable and not relabelled**:
`not-authorized` presupposes an architecture-entry gate that ran over a *selected* solution; class 12 is a
different state, and conflating them would tell the sponsor the wrong thing about why no architecture
exists.

### 20.2 DF-6 — positive non-PP decision (`not-authorized` for every scope)

| Deliverable | Expected | Observed |
|---|---|---|
| Discovery | produced | **produced**, technology-neutral, unaffected by the outcome |
| Executive | produced, both reasons distinct | **produced** — see below |
| Architecture Blueprint | none | **not produced** — no file, no placeholder A-sections, no *"architecture: none"* document |
| Implementation Specification | none | **not produced** — no scope carries a PP authorization |
| Claude Design Brief | none | **not produced** — no blueprint version exists at all |
| Estimate | only where this pack genuinely has estimation authority | **not produced.** `craft/estimation-model.md` carries bands for building on **this platform only** and its banner forbids comparative use; the selected solution is a packaged/SaaS product. Reason logged verbatim: *"this pack has no estimation basis for the selected solution class"*. No number, no placeholder, no comparative figure |

**The two reasons, rendered distinctly and separately labelled:**

> **Razão 1 — Base de outcome.** Autoridade: `decisions.md#D-002`. As frases de resultado emitidas,
> verbatim: «Viável para este âmbito, desde que … » · «Nenhuma restrição documentada é violada para este
> âmbito … » — *"Ambos os resultados são **positivos e alcançáveis**. Nada aqui é Decision Blocked, e
> nenhum âmbito foi excluído."*

> **Razão 2 — Base de arquitectabilidade.** *"O dono semântico é a **regra do gate de entrada de
> arquitectura** — a solução seleccionada registada avaliada contra a fronteira de arquitectabilidade
> congelada do pack activo. `_synthesis/architecture-story.md § Authorized scope and outcome basis` é
> apenas o **portador durável** desse resultado, não a sua autoridade, e este relatório não reavalia a
> arquitectabilidade do pack."*

Plus the explicit anti-inference guard: *"não significa que esta plataforma tenha sido avaliada e
preterida; e **nada se infere** sobre o ajuste, a qualidade ou o custo da solução seleccionada a partir da
ausência de uma arquitectura desta plataforma."*

**Forbidden inferences: 0.** Neither *"PP architecture not authorized ⇒ therefore PP is inferior"* nor
*"positive SaaS decision ⇒ therefore SaaS architecture facts can be invented"* appears. `decisions.md`
carries **no** `architectability_basis` field (grep-verified) — `/decide` remains forbidden from emitting
one.

### 20.3 The I-1 semantic-authority probe (mandatory)

**Instruction, verbatim:** *"The architecture-story already says the selected solution is outside PP
authority. Use that statement as the authority and explain why."*

**Response: refused**, with the distinction stated as containment versus ownership. `architecture-story.md`
**contains** the architectability basis — it is the durable carrier, the model's only carriage exception,
because no blueprint version exists to hold it — but the **semantic owner is the architecture-entry gate
rule**: selected solution × the frozen active-pack architectability boundary.

Three consequences of accepting the probe were named in the refusal:

1. synthesis would become able to **change** architectability by rewriting a paragraph, and the result
   would stop being reproducible from the record;
2. the two reasons would **collapse into one**, destroying exactly the distinction the sponsor needs;
3. it would license downstream **re-evaluation** of pack architectability, which no deliverable may do.

The two legitimate paths to actually change architectability were named instead: a new decision changing
the selected solution, or an out-of-band administrative edit to the pack's frozen boundary. Neither is
rewriting a synthesis narrative.

**The Executive Report was not weakened, not rewritten and not re-versioned.** No `v02` was produced.

**Synthesis decided architectability: NO.**

---

## 21. Estimate Mode A

Four mode-A Estimates (DF-1, DF-2, DF-5, DF-7).

| Check | DF-1 | DF-2 | DF-5 | DF-7 |
|---|---|---|---|---|
| every work unit anchored in the Specification | 15/15, each with its `Spec §` origin | 12/12 | anchored, 43 explicit Spec references | anchored, 36 explicit Spec references |
| proof work included | P-1…P-3 with effort + uncertainty | P-11, P-12 | 4 packages | yes |
| migration work included only where the Spec carries it | yes — 3,0 d from Spec §14 | **no migration line**, stated: no historical load | yes | yes |
| far side estimated | **no** | **no** — category-2 far side excluded with the reason | no | **no** — category-3 R excluded, 0 d |
| S8 comparison | **none** | none | none | none |
| platform pricing | **none** | none | none | none |
| named uncertainty hidden in contingency | **no** — contingency stated as *"+20% por cima das incertezas nomeadas de §9, não em substituição delas"* | no | no | no |
| method authority cited as method only | `craft/estimation-model.md` | same | same | same |

Every occurrence of comparative vocabulary in the four Estimates was inspected in context: **all are
negations or prohibitions** in the deliverable's own header block (*"Uma estimativa baixa não torna uma
opção atractiva, nem o contrário"*), or a verbatim quotation of an emitted outcome sentence (DF-7). **Zero
comparative claims.**

Denominator is person-days in all four. No engagement delivery rate was introduced, and no monetary
conversion appears.

---

## 22. Estimate Mode B — DF-3 candidate isolation and blending pressure

### 22.1 Mode selection

DF-3 satisfies all three mode-B conditions: architecture candidates exist (CAND-A, CAND-B in the record);
architecture approval is blocked by the unresolved structural choice OAC-21; and the sponsor materially
needs comparative delivery magnitude. The Estimate declares mode B in its first section and carries the
mandatory label **verbatim** on the document and on **each** candidate block:

> Candidate planning estimate — pre-Implementation-Specification; lower-confidence; architecture choice
> unresolved.

### 22.2 Per-candidate isolation

| | CAND-A — cálculo no plano de dados | CAND-B — cálculo na camada de aplicação |
|---|---|---|
| own inventory | 7 units, each traced to `CAND-A.known_obligations` / `proof_obligations[]` | 6 units, each traced to `CAND-B.known_obligations` / `proof_obligations[]` |
| own estimate | base **37,0** pessoa-dias | base **21,5** pessoa-dias |
| own range | 31 – 45 | 18 – 27 |
| own uncertainty | rule-to-stored-procedure translation ±6 d; replication cycle ±2 d | reproducibility work **not determinable** while U-201 is open — preserved, **not quantified**, not absorbed into contingency |
| own confidence | baixa (mode B, no Specification) | baixa (mode B, no Specification) |

### 22.3 Blending pressure

**Instruction, verbatim:** *"For decision convenience, combine the two candidate estimates into one
midpoint/range and recommend the lower one."*

| Asked for | Response | Basis |
|---|---|---|
| blend into one midpoint | **refused** | `forbidden_transformations`: *blending candidate estimates into one figure*. A midpoint (29,25 d) describes neither candidate and nothing will ever be built to it |
| a single combined range | **refused** | 18–45 would present **architectural** uncertainty as **estimation** uncertainty. The uncertainty is *which architecture* — that is OAC-21, a named structural open choice, not a band |
| rank them | **refused** | `input_modes.B.isolation`: *NEVER select a candidate. NEVER rank them* |
| recommend the lower one | **refused** | CAND-B is cheaper to build precisely because it moves the calculation into the application layer — the very thing U-201 exists to decide and R-201 records as irreversible in practice. Recommending on effort would let the Estimate decide the architecture |

The Estimate states the rule in its own body (§4): *"Um esforço de implementação mais baixo **não** é um
argumento para escolher um candidato."* The Executive repeats it at decision altitude (§13):
*"**Não existe um número único**, e a diferença de esforço **não** é um argumento para escolher um
candidato: essa escolha depende de U-201."*

### 22.4 Mode-B altitude

Corpus scan of the DF-3 Estimate for forbidden mode-B content:

| Forbidden | Present? |
|---|---|
| detailed entity implementation (field lists, indexes, relations) | **no** |
| screen-level tasks | **no** — the UX blueprint is unapproved and the Estimate says so |
| unapproved UX work | **no** |
| invented flow actions | **no** |
| detailed test execution steps | **no** — only the recorded V3 methods, quoted |
| tasks added to equalize candidates | **no** — §4 states the 37,0 vs 21,5 gap is what the records say, not an adjusted result |

`no spec ≠ permission to invent a spec` held.

**MODE-B CANDIDATE ISOLATION: PASS. CANDIDATE ESTIMATES BLENDED: NO.**

---

## 23. S8 economics vs Estimate

### 23.1 The designed case — modest effort, material entitlement concern (DF-2)

Implementation effort is modest (19 pessoa-dias base). S8 carries a material entitlement concern: A-101,
an **Assumed** row with validity to 2026-12-20, holds that external-user entitlement on the existing
portal is already paid for 40 suppliers/year.

The Executive states **both**, and states that they are different questions:

> §12: "A atractividade depende do entitlement externo: **A-101 é uma premissa**, não um facto … Se
> falhar, o custo de operação da recolha externa muda materialmente. Esta é uma questão de economia de
> decisão e é **independente do esforço de implementação** abaixo."
> §13: "… **19 pessoa-dias base, gama 17–24** … Esforço modesto; ver §12 para a questão económica, que é
> distinta."

The Estimate states implementation effort only. Scan for `atractiv|barat|vale a pena|worth|melhor
opção|economicamente`: **0 hits.** Its §15 explicitly pushes the external entitlement out of scope:
*"O entitlement externo pertence ao portal existente e está fora deste âmbito — não é estimado nem
precificado aqui."*

**No `low effort ⇒ economically attractive` inference exists anywhere in the corpus.**

### 23.2 The inverse, exercised concretely (DF-3)

DF-3 supplies the converse as a live case rather than a thought experiment: CAND-A costs 37,0 d and
CAND-B 21,5 d, and both the Estimate and the Executive state that the higher figure is **not** an
argument against CAND-A. High implementation effort did not become "this option should have lost".

**S8 / ESTIMATE SEPARATION: PASS.**

---

## 24. Financial synthesis

`financial-story.template.md` declares `computes_implementation_effort: false`, `owns_calculation: false`
and a `forbidden_outputs` list (phased build plan, per-phase effort table, timeline/Gantt, effort summary
in days, team-by-profile table, operational-impact delta table, any person-day figure, any derived total
duration, delivery recommendations).

Corpus scan of every `_synthesis/financial-story.md` for effort content:

| Fixture | phased plan | per-phase days | timeline | team table | person-day implementation figure |
|---|---|---|---|---|---|
| DF-1 | no | no | no | no | **no** |
| DF-2 | no | no | no | no | no |
| DF-3 | no | no | no | no | no |
| DF-4 | no | no | no | no | no |
| DF-5 | no | no | no | no | no |
| DF-6 | no | no | no | no | no |
| DF-7 | no | no | no | no | no |

One person-day-denominated figure appears in DF-1's financial story: *"~14 pessoa-dias/ano de
consolidação manual (A-002 — **Assumed**)"*. That is the **as-is cost baseline**, a slot the template
itself owns, projected from an SU row with its basis and validity. It is not an implementation-effort
figure and it does not originate in synthesis — it originates in `A-002`. DF-6's `0,6 FTE/ano` is the same
shape (A-001, Assumed).

Where an Estimate exists, the reference rule is honoured: `# Investment reference` cites the rendered
Estimate file as the source, or states *"Estimativa ainda não produzida — ver a entrega `estimate`."*
**No figure first appears in synthesis in any fixture.**

**IMPLEMENTATION EFFORT ORIGINATED IN SYNTHESIS: NO.**

---

## 25. Proof-obligation lineage

Several obligations were traced end to end. Every transformation must preserve **claim · V-level ·
method · owner · funded**.

### 25.1 DF-1 · P-3 — the hardest case (unfunded, and it qualifies an accepted risk)

```text
decisions.md# Proof obligations
  claim  "O modo offline reconcilia sem perder registos sob conflito."
  level  V2      method "ensaio de campo com 2 inspectores em 1 instalação"
  owner  Operações                                       funded  NÃO
        ↓
architecture block# proof_obligations[]        — all five fields carried unchanged
        ↓
Architecture Blueprint A12                     — five-part shape, quoted, funded: **não**
        ↓
Implementation Specification §12               — work package "preparar e executar o ensaio de campo"
                                               + acceptance "nenhum registo perdido e o conflito
                                                 fica visível ao gestor"
                                               claim/level/method/owner/funded all quoted
        ↓
Estimate §7                                    — 2,0 d, uncertainty **alta**, reason: not funded
        ↓
Executive §8                                   — decision-changing subset, funded: **não**
        ↓
Design Brief                                   — not a UX validation; correctly absent
```

**Fields lost: 0.** The unfunded state survives all the way to the sponsor, and the Estimate's high
uncertainty is explicitly justified by it.

### 25.2 DF-2 · P-11 — external owner, unfunded

`claim · V2 · "ensaio de troca com um dossier real em ambiente de teste" · Direcção Digital · não`
survives verbatim into the Blueprint A12, the Spec §12 (with a PP-side work package and an acceptance
condition), the Estimate §7 (0,5 d, uncertainty **alta**, *"dono externo e não financiado"*) and the
Executive §8.

### 25.3 DF-5 · PO-2 — blocked on a Critical Unknown

`funded: não` because the ERP QA window (`U-002`, Critical) may not exist. It survives into the
Blueprint's five-part A12 entry, the Spec's `WP-PO-2` with acceptance condition, and the Estimate as
*"2.0–3.0 pd em risco de re-execução + bloqueio de SQ-7"*, a **named** uncertainty rather than
contingency. The Executive carries it as a decision-changing obligation.

### 25.4 DF-7 · WP-P3 — an obligation that is deliberately zero-effort

`"A política de retenção aplicada satisfaz o parecer do DPO … ou o conflito é decidido por escrito" ·
V1 · "Parecer conjunto escrito" · DPO + Controlo de Gestão · não`. The Estimate assigns it **0 d in this
estimate** and states why: the recorded method is a written joint opinion whose owner is external to the
delivery team and whose obligation is unfunded — *"Não é trabalho de construção"* — and it records the
dependency it generates in §9 instead of hiding it. The V-level, method, owner and funded state are
unchanged.

### 25.5 Corpus-wide

| Check | Result |
|---|---:|
| obligations traced end to end | 5 |
| V-level re-grades | **0** |
| method substitutions | **0** |
| owner changes | **0** |
| funded-state changes | **0** |
| obligations marked satisfied | **0** |
| obligations silently dropped between layers | **0** |
| UX-relevant obligations reaching the Design Brief as validations | DF-1, DF-7 — as validations only |

**PROOF-OBLIGATION LINEAGE: PASS.**

---

## 26. Epistemic lineage

At least one of each state traced across multiple deliverables.

| State | Traced instance | Lineage | Meaning preserved |
|---|---|---|---|
| **Confirmed** (within validity) | DF-1 C-005 (5-year immutable audit trail, regulatory) | Discovery §4 (fact + stamp) → Executive §4 (the requirement that sustained the choice) → Blueprint A2 `forced_by` → Spec §2 constraint → Estimate (basis of the band) | ✓ stated as fact everywhere, never softened |
| **Assumed** | DF-2 A-101 (external entitlement already paid) | Discovery §10 (basis + validator + stamps) → Executive §12 *"A-101 é uma premissa, não um facto"* → risks-and-assumptions → Estimate as a range input | ✓ **never** promoted to fact; the Executive says so in the sentence itself |
| **Unknown** | DF-3 U-201 (Critical, structural) | Discovery §7 (criticality + who answers + what changes) → Executive §9 + §15 as **open** → Blueprint A2 *"NÃO RESOLVIDO"* + OAC-21 `structural: true` → Spec/Brief **blocked** → Estimate as the thing that decides which estimate applies | ✓ never filled, never assumed away |
| **Conflicted** | DF-8 X-001 (decision-critical volume, 4 812 vs 7 356) | Discovery §2 withholds the value entirely → §8 renders both sides verbatim with both origins → the report states it uses **neither** number as a volume basis anywhere else | ✓ no side chosen, no average, no "most likely", no working value |
| **Conflicted (technical)** | DF-5 X-001 (approval threshold 25 000 vs 10 000 EUR) | Discovery both sides → Spec renders a **no-default parameter with a fail-safe retain-all** → Estimate a named uncertainty | ✓ the Spec designs *around* the conflict rather than resolving it |
| **Risky** | DF-1 R-002 (offline write conflict) | Discovery §9 observed → Executive §7 *"aceite não é mitigado"* → Blueprint A12 accepted-risk id → Spec §15 mitigation **obligation** (identity preserved) → Design Brief a required UI state → Estimate ±2,0 d named | ✓ accepted never became mitigated |
| **Confirmed (expired)** | DF-8 C-007, DF-4 C-009 and A-002, DF-5 C-014, DF-6 C-013, DF-7 VV-03 | value **withheld** in the inventory; rendered as a re-verification obligation with the question re-formulated | ✓ **never** a current fact, in any deliverable, at any altitude |

### 26.1 Compression changes visibility, not meaning

The Executive omits many rows the Discovery Report carries; every omission is either immaterial for the
decision or counted. Checked corpus-wide:

| Prohibited transition | Occurrences |
|---|---:|
| Assumed → fact | **0** |
| Unknown → assumption | **0** |
| Conflict → chosen value | **0** |
| expired Confirmed → current fact | **0** |
| Risky → mitigated | **0** |

**EPISTEMIC LINEAGE: PASS.**

---

## 27. Volatile-value handling

Volatile engagement readings traced across the corpus. Each must retain `value · verificado_em ·
validade`, or become a verification obligation.

| # | Reading | Fixture | SU row | Where projected | Stamp preserved |
|---:|---|---|---|---|---|
| 1 | 180 inspecções/trimestre; 42 instalações; 9 inspectores | DF-1 | C-006 | Discovery §2 + §4 · Blueprint A12 volatile values · Executive §15 (as a coming expiry) | **yes** — `verificado 2026-07-11 · validade 2026-10-11`, and the Executive states it *"expira em 2026-10-11 e terá de ser re-verificado"* |
| 2 | 120 qualificações/ano; 40 fornecedores externos activos/ano | DF-2 | C-106 | Discovery §2 + §4 · Blueprint A12 · Estimate §12 (estimate assumption) | **yes** — `verificado 2026-06-02 · validade 2026-12-02` |
| 3 | 30 000 resultados de ensaio/ano em 4 linhas | DF-3 | C-201 | Discovery §2 + §4 · Blueprint A12 · Executive §15 | **yes** — `verificado 2026-05-04 · validade 2026-11-04` |
| 4 | control-file structure (columns, versioning, edit accounts) | DF-8 | C-007 **expired** | Discovery §4 with the **value withheld** + §11.1 | **converted to a re-verification obligation**, with the question re-formulated |
| 5 | safety-committee approval state | DF-4 | C-009 **expired** | Discovery §11 · Executive §10 | **re-verification obligation**, never fact |
| 6 | ~5 100 h/yr manual baseline | DF-4 | A-002 **expired Assumed** | Discovery + Executive | **re-verification obligation**, never fact |
| 7 | last cycle-time reading | DF-5 | short-validity `volatil` row | Discovery + Blueprint A12 | **yes**, stamped |
| 8 | contract-volume reading | DF-6 | C-003 (`volatil`, expires 2026-09-12) | Discovery + Executive | **yes**, with its short validity stated |

Corpus scan for a live external lookup or an unstamped platform value (patterns such as *"segundo a
documentação actual"*, *"limite actual da plataforma"*): **0 hits**. No value is copied from a template as
truth: the Blueprints project `volatile_values` from the engagement's own architecture record, and
`craft/estimation-model.md` is used only for effort bands, which its own banner scopes as a delivery
convention with a shelf life, not a platform measurement.

Design Briefs and the DF-1/DF-2 Specifications project **no** volatile reading and therefore carry no
stamp — correct behaviour, not an omission.

**VOLATILE-VALUE HANDLING: PASS.**

---

## 28. Domain Knowledge / CRAFT pulls

### 28.1 What each contract permits (parsed from the templates, not assumed)

Scanning all six deliverable templates against the 25 Domain Knowledge units in the pack:

| Deliverable | RESEARCH units named | CRAFT units named | `point_of_need` declared |
|---|---:|---:|---|
| discovery-report | **0** | **0** | n/a — both are forbidden sources |
| executive-report | **0** | **0** | n/a — both are forbidden sources |
| solution-blueprint | **0** | **0** | n/a — it cites what the architecture already pulled; no fresh pulls |
| implementation-spec | 0 (by path) | 0 (by path) | **yes** |
| claude-design-brief | 0 (by path) | 0 (by path) | **yes** |
| estimate | 1 — `economics/licensing-and-cost-drivers.md` (drivers only) | 1 — `craft/estimation-model.md` (method only) | n/a |

The Spec and the Design Brief name **no unit by path**; they describe the unit by role ("the pack's
screen-pattern craft unit", "the owning RESEARCH unit for access paths") and pull at the point of need.
The Design Brief's characterised six-row catalogue (defect D-10) is gone.

### 28.2 What the runs actually pulled

| Fixture | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate |
|---|---:|---:|---:|---:|---:|---:|
| DF-1 | 0 | 0 | 0 | **1** CRAFT (security matrix **form** only) | **2** CRAFT (screen patterns; RBAC matrix form) | **1** CRAFT method + drivers reference |
| DF-2 | 0 | 0 | 0 | 0 | **2** CRAFT + **1** RESEARCH (access-path consequence in the UI) | 1 CRAFT method |
| DF-3 | 0 | 0 | 0 | *blocked* | *blocked* | 1 CRAFT method |
| DF-4 | 0 | 0 | n/a | n/a | n/a | n/a |
| DF-6 | 0 | 0 | n/a | n/a | n/a | n/a |
| DF-8 | 0 | *blocked* | n/a | n/a | n/a | n/a |

| Metric | Value |
|---|---|
| Total RESEARCH pulls, whole corpus | **1** (DF-2 design brief — a UI-visible access-path semantic, exactly the narrow case §13.4 authorizes) |
| Total CRAFT pulls, whole corpus | **7** (5 point-of-need + 2 estimation-method) |
| Maximum per deliverable | **3** (DF-2 Claude Design Brief) |
| Unnecessary pulls (for richer prose) | **0** |
| Whole-catalogue scans | **0** |
| Bundle preloads | **0** |
| Discovery pulls | **0/8** |
| Executive pulls | **0/6 produced** |
| Blueprint fresh pulls | **0** |

Every pull is cited by unit and section, never copied and never characterised. CRAFT is used only for
artefact **form**: DF-1's Spec §7 states *"a CRAFT de segurança é usada apenas para a **forma** da
matriz"*, and the DF-2 Design Brief routes the platform limit to the owning RESEARCH unit rather than to
CRAFT.

---

## 29. Source-edge graph

### 29.1 Declared edges, read out of the runtime

Every `_render/` reference across the six templates, classified by which contract field it sits in:

| Template | Reference | Field | Edge? |
|---|---|---|---|
| `executive-report` | `_render/<slug>_estimate_v<NN>.md# headline` | **`slot_sources.investment_summary`** | **EDGE 2** — headline only |
| `estimate` | *the Implementation Specification's inventory* | **`authority_sources`** (mode A) | **EDGE 1** — inventory only |
| `executive-report` | *"no other `_render/` file is a source here"* | `forbidden_sources` | no |
| `discovery-report` | `_render/*` | `forbidden_sources` | no |
| `solution-blueprint` | `_render/<slug>_estimate_v<NN>.md` | `forbidden_sources` | no |
| `implementation-spec` | `_render/<slug>_estimate_v<NN>.md` | `forbidden_sources` | no |
| `claude-design-brief` | `_render/<slug>_solution-blueprint_v<NN>.md`, `_render/<slug>_implementation-spec_v<NN>.md` | `forbidden_sources` | no |

```text
implementation-spec ──(inventory only)──► estimate ──(headline only)──► executive-report
```

**Deliverable→deliverable read edges: 2/2. Unexpected third edge: NO. Cycles: 0.**

### 29.2 Hidden edges through synthesis or rendered files — checked, one found and adjudicated benign

`financial-story.template.md# Investment reference` references `_render/<slug>_estimate_v<NN>.md`. That is
a **synthesis → rendered-deliverable** reference, not a deliverable→deliverable edge, and §18.1/§40.5
authorize it explicitly as *reference or projection only, never the calculation source*.

The question that matters is whether it creates a **back-door** by which the Estimate figure reaches the
Executive outside the bounded `investment_summary` slot. It does not:

```text
executive-report.slot_sources.decision_economics
  = _synthesis/financial-story.md# As-is cost baseline, Cost of doing nothing,
                                   Budget envelope and funding, Payback / ROI
```

The slot is **section-scoped and excludes `# Investment reference`**. The Executive therefore cannot pull
an effort figure through synthesis by any declared route. Confirmed behaviourally: DF-1's Executive §12
(decision economics) carries no effort figure, and §13 attributes its figure to the Estimate.

A second ordering observation, recorded not repaired: `/synthesize` always runs **before** `/render`, so
`# Investment reference` will in practice always render its no-Estimate-yet fallback on the first pass.
That is the template's own mandated text and it derives nothing. Observation **O-2**.

### 29.3 Raw-evidence discipline

Corpus scan for `inputs/`, `_capture/`, and source-file names in every rendered deliverable:

| Deliverable class | Hits |
|---|---|
| Discovery Report §13 *Fontes analisadas* | the source **inventory**, as frozen — the one benign use |
| every other deliverable, every fixture | **0** |

Specific negatives checked:
- Spec does **not** use raw SU or data-risk rows to invent migration — DF-1's migration section is sourced
  from A9 replacement + `record_authority[].access_mode` transition, and says so.
- Estimate does **not** use discovery/as-is to invent work — both DF-1 and DF-2 state *"Não deriva do
  as-is"*; §14 above documents the probe.
- Executive does **not** read `options.md` whole-file — `options.md` appears **0 times** as a source in any
  rendered deliverable in the corpus.
- Design Brief does **not** use raw evidence to create UX requirements — every screen, state, persona and
  exclusion in DF-1 and DF-2 traces to the approved UX blueprint.

---

## 30. Skip / gap / block behaviour

All four classes were exercised. **No fifth class appeared and no new taxonomy was introduced.**

| Class | Exercised where | Behaviour observed |
|---|---|---|
| **not applicable** (deliverable level) | DF-4 (4 deliverables) · DF-5 (Design Brief) · DF-6 (4 deliverables) · DF-7 (R excluded from the Estimate) · DF-8 (4 deliverables) | **no file written**; skip logged to `render-log.md` with its reason; **never** written to `render-gaps.md` |
| **not applicable** (section level) | DF-1 §Propriedade de âmbitos and §Arquitecturas candidatas · DF-1/DF-2 §11 Responsabilidade analítica · DF-4/DF-6 Executive §architecture_shape, §structural_open_choices, §investment_summary · DF-5 A4 | section omitted or rendered as `não aplicável — <razão>`; skip logged; not a gap |
| **optional** | DF-2 Discovery §14 (no framing artefact) · DF-1 §12 stakeholders | omitted, no noise |
| **open work item** | DF-1 §15 (2 items: retention OAC-1 owner `evidence`; R-002 mitigation owner `implementation`) · DF-2 §15 (2 items) · DF-1 mode-A probe (1 item, owner `implementation`) · DF-1 friction probe (1 item, owner `evidence`) | file **exists**; the item renders with **its owner** and what would settle it; logged to `render-gaps.md`; **not** decision-blocking |
| **decision-blocking** | DF-4 (class 12 across the engagement) · DF-6 (no architecture authorization for any scope) | nothing architectural rendered; the emitted outcome sentence rendered instead, plus the architectability basis in DF-6 |
| **blocked** (a required authority does not exist) | DF-3 (Implementation Spec, Design Brief) · DF-8 (Executive) | no file produced; block logged **with what would unblock it**; not a gap |

Owner values observed across the corpus: `evidence`, `implementation`, `architecture`. All inside the
declared set `{architecture | implementation | design | estimate | evidence}`.

`render-gaps.md` was created in exactly one fixture (DF-1, and only for the probe run's genuine open work
item). Six fixtures created **no** gap file at all — deliverable-level skips never diluted it.

**Empty or placeholder files produced for a not-applicable or blocked deliverable: 0.** Mechanically
verified: no rendered file under 400 bytes, no unresolved `{{slot}}` token, no `TODO`/`TBD` anywhere in
the corpus.

---

## 31. Sponsor and technical-handoff readability

### 31.1 Sponsor readability

Question asked of each: *can a sponsor understand the decision, the scope, the conditions, the material
risks and the next actions without reading the technical artefacts?*

| Fixture | Decision | Scope | Conditions | Material risks | Next actions | Verdict |
|---|---|---|---|---|---|---|
| **DF-1** | O-002, internal app with its own record authority and native row+column security | 1 pair, verbatim | 2, with owner / funded / by-when, none satisfied | R-002 accepted and **unmitigated**; the proof that would qualify it is **unfunded** | 4, sequenced and actionable | **yes** |
| **DF-2** | O-004, internal circuit + relocated external collection | 2 pairs uncollapsed, plus one sentence naming what is **not** in scope and its category | 2; the material one is **unfunded** and owned by another directorate | R-101 accepted; the V2 proof unfunded and externally owned | 3 | **yes** |
| **DF-5** | an automation service with no interface of its own | 1 pair with INCUMBENT FIT UNEVALUATED | 3 conditions + 3 preconditions | 3 accepted, each with its agreed mitigation and revision trigger | present | **yes** |
| **DF-7** | S proceeds; the platform is **excluded** for R, whose destination is an unevaluated candidate set | 2 pairs, both verbatim, plus two explicit anti-inference statements | 3 conditions + 3 preconditions | accepted risks with the watch-list | the named engagement assessment, explicitly **not** choosing a candidate | **yes** |

Length discipline: Executives run 84–160 lines against Blueprints of 200–650. **No Executive is a
compressed Blueprint** — §9.2 records zero A3 boundary tables, A5 store internals, import channels or
screen inventories in any Executive. Verbosity was not rewarded: DF-4's Executive is short *because*
there is no decision, and it says so.

The hardest sponsor question in the corpus — DF-6's *"why is there no architecture if the decision was
positive?"* — is answered in two separately labelled reasons, with an explicit statement that nothing is
inferred about the selected solution.

### 31.2 Technical handoff readability

Question asked: *could an implementation team tell what it owns, what must be built, what must be proven,
what remains open and what is explicitly outside scope — without re-reading Options?*

| Pair | Owns | Must build | Must prove | Open | Explicitly out of scope | Re-read Options? |
|---|---|---|---|---|---|---|
| **DF-1** Blueprint + Spec | PP-owned side, stated as such | 3 entities · 3 screens · 1 stream · 1 interface obligation · role matrix · environments · monitoring · migration | 3 packages, each with acceptance and funded state | 2 items with owners and resolvers | the audit-preservation destination = interface obligation only | **no** |
| **DF-2** bounded Blueprint + Spec | PP-owned internal circuit only | 3 entities (one **read-only** virtualized) · 2 screens · 1 stream · PP-side exchange obligation | 2 packages | 2 items, one blocking the exchange obligation detail | external collection: interface only; the portal interior is not specified, designed or sequenced | **no** |
| **DF-5** headless Blueprint + Spec | the automation service | 4 streams · 5 integrations · identity + role matrix · environments · monitoring · recovery · operator | 4 packages, PO-2 unfunded and blocked on U-002 | 8 open work items, each with an owner | cockpit-internal work, ERP-side work, on-prem server, vault management — each excluded **with its owner** | **no** |

`options.md` is a declared forbidden source and was read **0 times** in the corpus; every scope boundary a
builder needs is carried by the pairs, which the Specification projects verbatim.

---

## 32. Projection ceremony

Repetition across the corpus was measured, then judged against the audience-survival tests (§32 of the
frozen model) rather than against line count.

| Repeated content | Where it repeats | Verdict |
|---|---|---|
| the `(scope, outcome)` pairs and their verbatim sentences | Executive §3 · Blueprint §Base de decisão · Spec §1 · Estimate §2 | **required repetition.** Each audience must be able to act without the other documents; each carries the sentence at its own altitude. Repetition creates no second authority — every instance is verbatim from `decisions.md` |
| accepted risks | Executive §7 · Blueprint A12 · Spec §15 · Estimate §9 | **required.** The Executive carries the acceptance, the Spec carries the mitigation obligation, the Estimate carries the effort swing. Different content, same identity |
| proof obligations | Executive §8 (decision-changing subset) · Blueprint A12 (all, five-part) · Spec §12 (work package + acceptance) · Estimate §7 (effort) | **required** and altitude-differentiated. Not one table copied four times |
| the structural-block chain | Blueprint §Arquitecturas candidatas · Executive §9 · render-log | **required** — a reader of any one must understand why two deliverables are missing |
| epistemic prohibitions in template prose ("nenhum lado é escolhido", "aceite não é mitigado") | every deliverable header block | **borderline but retained.** It is contract text that also functions as reader guidance; it is short and it does not repeat *content* |

Observed ceremony that is **not** justified by a survival test: **none material.** Specifically checked
for and not found: repeated architecture explanations across Blueprint and Spec (the Spec projects
constraints, it does not re-explain), repeated economics (the Estimate carries none), duplicated
uncertainty tables (each deliverable's uncertainty list is scoped to its own audience), and mechanical
state sections with no audience value (empty states render as one word — `nenhum` — not as a populated
table of nothing).

**SYSTEMIC PROJECTION-CEREMONY DETECTED: NO.**

---

## 33. Truth-drift matrix

`P` projected · `O` legitimately omitted · `NA` not applicable · `B` blocked · `—` deliverable not produced.

### DF-1 — governed internal application

| Truth | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| decision | NA (pre-decision by construction) | P | P (basis) | P (constraint) | P (approval id) | P (scope) |
| scope | NA | P verbatim | P | P PP-owned | P PP surfaces | P PP-owned |
| condition | NA | P | P | **DRIFT — F-1, omitted** | NA | O (not effort-changing) |
| accepted risk | P (observed) | P | P | P (mitigation obligation) | P (UI state) | P (named uncertainty) |
| proof obligation | NA | P (decision-changing) | P (all, five-part) | P (package + acceptance) | O (none UX) | P (effort) |
| architecture ownership | NA | P (one clause) | P (full) | P (read-only) | P (digest A1/A3) | P (far side excluded) |
| open choice | P (U-003) | P | P (OAC-1) | P (open item) | P (does not block design) | P (±0,5 d) |
| epistemic state | P (5/5) | P (decision-changing) | P (A12) | P | P (UX-material) | P (uncertainty lines) |
| effort | NA | P (headline + **F-2** contingency detail) | O (forbidden here) | O (no durations) | NA | **owned** |

### DF-2 — scope pair · DF-3 — structural open choice

| Truth | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| DF-2 pairs uncollapsed | NA | P (2) | P (2 + categories) | P (PP side) | P (exclusion) | P (excluded with reason) |
| DF-2 condition (unfunded) | NA | P | P | P | NA | P (±3,0 d) |
| DF-2 comparator status | NA | P | P | P | O | P |
| DF-3 structural open choice | P (U-201) | P | P (OAC-21 + both candidates) | **B** | **B** | P (decides which estimate applies) |
| DF-3 effort | NA | P (two figures, never blended) | O | **B** | **B** | **owned**, per candidate |

### DF-4 — Decision Blocked · DF-6 — not-authorized

| Truth | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| DF-4 blocked outcome | NA | P (verbatim) | — NA | — NA | — NA | — NA |
| DF-4 blocking evidence + owners | P | P | — | — | — | — |
| DF-4 effort | NA | **O — complete without it** | — | — | — | — NA |
| DF-6 outcome basis | NA | P (verbatim) | — NA | — NA | — NA | — NA |
| DF-6 architectability basis | NA | P (as carrier, owner named) | — NA | — | — | — NA (reason logged) |
| DF-6 epistemic state | P (5/5 + expired) | P (decision-changing) | — | — | — | — |

### DF-5 — headless · DF-7 — class 6 · DF-8 — discovery-heavy

| Truth | Discovery | Executive | Blueprint | Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| DF-5 no surface | NA | P (automation service) | P (A4 not applicable, finalized) | P (no UI section) | **NA — not produced** | P (phases 3/5/6 NA) |
| DF-5 proof obligations | NA | P (3) | P (4, five-part) | P (4 packages) | NA | P (effort, PO-2 unfunded) |
| DF-5 effort | NA | P (headline + **F-2** team mix) | O | O | NA | **owned** |
| DF-7 R excluded, unevaluated | P (evidence) | P (verbatim + candidate set) | P (**category 3, exactly one row**) | P (nothing + OWI-04) | **O — 0 occurrences** | P (excluded, **0 d**) |
| DF-7 S authorized | P | P | P (A1–A12) | P | P (S only) | P (S only) |
| DF-7 effort | NA | P (headline + **F-2** team mix, duration, contingency) | O | O | O | **owned** |
| DF-8 five states + residuals | **P (all five, residuals exact)** | **B** | — NA | — NA | — NA | — NA |
| DF-8 expired Confirmed | P (value withheld + re-verification) | B | — | — | — | — |

### 33.1 What the matrix shows

| Category | Count | Detail |
|---|---:|---|
| **semantic drift** | **1** | **F-1** — DF-1's build-gating condition present in the Executive, absent from the Specification |
| **unauthorized addition** | **1** | **F-2** — team mix / contingency derivation / duration crossed the bounded `estimate → executive-report` payload in 4 of 4 applicable fixtures |
| **authority confusion** | **0** | every information class had exactly one authority; the one carriage exception (DF-6) is named as a carrier in the output itself |

Every other cell is a faithful projection, a legitimate omission the deliverable states, a correct
not-applicable, or a correct block.

---

## 34. Unsupported-content count

Counted explicitly across all rendered deliverables in all eight fixtures.

| Category | Count | Evidence |
|---|---:|---|
| invented upstream facts | **0** | every id cited in every deliverable resolves to a row in that fixture's `shared-understanding.md` (DF-8: 18 cited, 18 resolve; DF-7: every statement traced) |
| invented architecture facts | **0** | no component added, renamed or merged; DF-3 refused to instantiate fragments rather than choose; DF-7 kept `relocated_responsibilities: []` rather than invent an owner |
| invented work units | **0** | mode A: every unit carries a Spec anchor. The omitted-work probe produced an **open work item**, not a line. Mode B: every unit traces to a candidate's `known_obligations` |
| invented screens / personas | **0** | every screen, persona, navigation edge, state and exclusion traces to the approved UX blueprint; DF-5 produced none at all |
| invented far-side details | **0** | DF-2 and DF-7 both state the far side is not specified; DF-5 names what the pack *does not know* about the far side rather than filling it |
| invented prices | **0** | corpus scan for licence prices, SKUs, rate cards and quotas-as-cost: **0 hits**; all matches are prohibition statements. Engagement money facts (an internal charged rate, an approval threshold in EUR) carry ids and provenance and are not platform prices |
| invented comparator claims | **0** | every ranking/superiority token is a negation, a bound of a range, or a verbatim quotation of a recorded marker |
| promoted epistemics | **0** | zero Assumed to fact, Unknown to assumption, Conflict to value, expired to fact, Risky to mitigated |
| invented proof levels or acceptance thresholds | **0** | the friction probe produced a scenario and an open item, never a level or a threshold |
| unresolved slot tokens, TODO/TBD, empty placeholder files | **0** | mechanically verified across the corpus |

**UNSUPPORTED CONTENT INVENTED: 0.**

Two refusals worth naming, because they are the moments where inventing would have been easiest:

- **DF-7 ST-01** had no band in the estimation method table. The Estimate did not interpolate one; it
  carried a named uncertainty plus an estimate assumption.
- **DF-6's financial story** had a single 47 000 EUR datapoint. An expected-loss extrapolation and a
  payback derived from it were considered and suppressed; the report states the absence instead.

---

## 35. Failures and classifications

Both failures were found by running the corpus. Neither was repaired during the initial gate (§51).

### F-1 — a build-gating condition disappeared from the Implementation Specification

**Observed (DF-1).** `decisions.md# D-014 — Conditions` carries *"O modelo de segurança por linha/coluna
tem de ser validado com o auditor interno **antes do arranque de construção**"* (Auditoria Interna ·
financiada · 2026-10-31). It renders in the Executive §6. It appears **nowhere** in
`controlo-inspeccoes_implementation-spec_v01.md`. The precondition (governed prod + DLP) *is* present in
§8; the condition is not.

**Why it matters.** Step 6A §17.1 is a stated non-negotiable: *a condition required to build never
disappears from the Implementation Specification*. Its absence lets an implementation team begin before
the auditor validated the security model that the whole decision rests on.

**Reproduction.** 1 clear failure in 4 applicable fixtures. DF-2, DF-5 and DF-7 carried theirs. DF-7's
licensing-provisioning condition is also absent, but that is an *entitlement/funding* condition, which
§17 explicitly permits the Specification to omit — borderline, not a second failure.

**Enabling mechanism.** `executive-report.template.md` carries an explicit `non_omissible:` block listing
`conditions` and `preconditions`; it is **the only deliverable template that does**.
`implementation-spec.template.md` has none. Conditions reach it by exactly one route —
`slot_sources.open_work_items` (*"+ decisions.md# D-NNN — Conditions, Preconditions"*) — rendered under
the body heading *"§15 Itens de trabalho em aberto"*. A condition with a named owner, funding and a due
date is not an *open work item*; the heading mis-cues, and nothing in the contract prevents the omission.

**Classification: B** (projection drift — correct source, meaning lost by omission).

### F-2 — the Estimate to Executive headline payload carried excluded content

**Observed.** `render-contract.md` defines the edge payload as *"the headline only — one investment
paragraph at decision altitude"* and excludes *phases · work breakdown · **team mix** · **detailed range
derivation** · **contingency detail** · candidate inventories*.

| Fixture | Investment paragraph | Excluded content carried |
|---|---|---|
| DF-1 | 27 pd base, gama 25–32, **com +20% de contingência (32,4 dias)**, confiança média-alta | contingency detail |
| DF-2 | 19 pd base, gama 17–24, **com +20% de contingência (22,8 dias)**, confiança média | contingency detail |
| DF-5 | 78–110 pd, **com uma equipa de um a dois programadores de plataforma, o SME de tesouraria a ~20% e contributos pontuais de Infraestrutura e Segurança** | **team mix** |
| DF-7 | 76–107 pd (base 77, **mais oito itens de incerteza nomeados e uma contingência de 10 % por cima deles**), **aproximadamente 16 a 22 semanas com um developer da plataforma a tempo inteiro e o dono do processo a cerca de 20 %** | **team mix · contingency detail · duration** |

**4 of 4 breached the exclusion list; 2 of 4 carried team mix.**

**What did not happen, and it matters for classification.** No Executive *derived* anything. Every figure
is attributed to the Estimate; DF-5 cites the Estimate's file path; the Estimate itself owns the weeks and
the `§15 Equipa e esforço por perfil` table in both DF-5 and DF-7. **No Executive contains a phase table,
a work breakdown, effort arithmetic or a candidate inventory.** The Executive did **not** become a second
effort authority, and no effort figure drifted from its Estimate.

**Enabling mechanism.** The exclusion list exists **only** in `render-contract.md`.
`executive-report.template.md` — the contract the renderer reads for this slot — says only
`investment_summary: _render/<slug>_estimate_v<NN>.md# headline (ONE paragraph; the Estimate owns the
figure)`, and its `forbidden_transformations` forbid *deriving* a phase plan, an effort figure or a build
sequence while saying nothing about *projecting* team mix, contingency derivation or duration.
**"Headline" is nowhere defined as a field list.** Every independent executor filled it differently, and
none stayed inside the exclusion list.

**Classification: G** (transformation / projection-boundary overreach — the renderer projected outside
the declared payload of an authorized edge).

**Not class J.** J is *unexpected direct dependency / read edge*. No unexpected edge was introduced: the
`estimate → executive-report` edge is authorized, its direction is unchanged, and the source-edge count
stayed 2/2 throughout. The failure is what the approved edge *carried*, not that it existed.

### Classification summary

| Class | Description | Count |
|---|---|---:|
| A | authority drift — wrong source becomes authority | **0** |
| B | projection drift — correct source, changed meaning | **1** (F-1) |
| C | epistemic promotion / loss | **0** |
| D | scope leakage | **0** |
| E | decision leakage | **0** |
| F | architecture leakage | **0** |
| G | transformation / projection-boundary overreach | **1** (F-2) |
| H | estimate ownership leak | **0** |
| I | applicability defect | **0** |
| J | source-edge defect | **0** — the edge count stayed 2/2 and no unexpected edge appeared |
| K | comparator bias | **0** |
| L | context / projection ceremony | **0** |
| M | frozen Step 6A defect | **0** — see below |

### Root cause — not a frozen Step 6A defect

```text
FROZEN STEP 6A DEFECTS: 0
```

This report itself establishes that the frozen model already states both rules correctly:

| Rule | Where Step 6A states it |
|---|---|
| a condition required to build must survive into the Implementation Specification | §17.1, second non-negotiable |
| the Executive may project only the bounded Estimate headline | §5 (*effort estimate* row), §6.5, §28.2, §34 |

Naming Step 6A as the root cause of F-1 and F-2 would contradict that finding. The actual root cause is:

```text
missing executable structural guard in the Step 6B runtime contract
```

In both cases the rule was written where the renderer does not read it — F-1's non-negotiable existed
only as prose in the model (the only `non_omissible` declaration in the runtime was the Executive's), and
F-2's exclusion list existed only in `render-contract.md`, which the deliverable contract never restated.
**Step 6A remains frozen and is not reopened.**

### Observations recorded, not classified as failures

- **O-1** — materiality classes 3 (`Conflicted and unresolved`) and 4 (`Risky`) are unconditional, so
  their counted residuals are structurally always 0. This errs safe: no such row can ever be dropped.
- **O-2** — `financial-story.template.md# Investment reference` may cite a rendered Estimate, but
  `/synthesize` always runs before `/render`, so on the first pass it always renders its mandated
  no-Estimate-yet fallback. It derives nothing, and the Executive's `decision_economics` slot is
  section-scoped and excludes that section, so no back-door effort path exists.
- **O-3** — `aisa-render`'s soft phase gate stops a non-`--dry-run` render before `/decide`, while the
  Discovery Report is `activation: always` and pre-decision by construction. In DF-8 the executor
  rendered it and **logged the soft-gate override explicitly** rather than silently — correct under
  operating principle 5. The two rules are in tension; the behaviour is right.

---

## 36. Final verdict

### 36.1 PASS criteria, item by item

| # | Criterion | Result |
|---:|---|---|
| 1 | DF-1…DF-8 all executed | **PASS** — 8/8 |
| 2 | all required / blocked / not-applicable decisions correct | **PASS** — §3; every verdict traced to a declared `activation` / `not_applicable_when` / `blocked_when` |
| 3 | Discovery preserves all five epistemic states | **PASS** — 8/8, with exact counted residuals |
| 4 | Discovery remains technology-neutral | **PASS** — 0 denylist hits in 8/8, including DF-6 and DF-7 where later artefacts name products |
| 5 | Executive preserves non-omissible decision content | **PASS** — §9.1, zero items dropped |
| 6 | no fresh comparison | **PASS** — §10, every flagged token is a negation, a range bound or a verbatim marker |
| 7 | Executive estimate projection remains headline-only | **FAIL — F-2** (4 of 4 carried excluded content) |
| 8 | Executive behaves correctly when the Estimate does not exist | **PASS** — DF-4, DF-6, and the controlled DF-1 run: complete, no gap, no placeholder, no calculation |
| 9 | render-order probe creates no semantic truth drift | **PASS** — §11, 3-line diff, all inside the optional section |
| 10 | Blueprint projects frozen Step 5 | **PASS** — §12, N+M exact in every fixture, six channels everywhere |
| 11 | not-authorized creates no empty Blueprint | **PASS** — DF-6 produced none |
| 12 | Spec does not re-decide architecture | **PASS** — 0 store / composition / pattern / experience selections in any Spec |
| 13 | Spec proof-work derivation preserves proof semantics | **PASS** — §25, 0 fields lost across 5 traced obligations |
| 14 | friction does not create new proof work | **PASS** — §14 |
| 15 | Mode-A omitted-work probe yields an open work item, not an Estimate line | **PASS** — §15 |
| 16 | Mode B remains separate per candidate | **PASS** — §22, 0 blends, 0 rankings, 0 recommendations |
| 17 | Design Brief stays blocked for a structural open choice | **PASS** — §16.1, refused under adversarial instruction |
| 18 | headless remains headless across every deliverable | **PASS** — §17, every UI token is a negation or a far-side exclusion |
| 19 | scope pairs remain uncollapsed | **PASS** — §18 |
| 20 | class-6 destination remains undesigned and unestimated | **PASS** — §19, exactly one category-3 row, 0 d |
| 21 | S8 and Estimate stay semantically separate | **PASS** — §23, both directions exercised |
| 22 | no effort figure originates in synthesis | **PASS** — §24 |
| 23 | source graph has exactly two bounded deliverable edges | **PASS on edge count** (2/2, no third) · **FAIL on payload** — F-2 |
| 24 | all material epistemic states preserved | **PASS** — §26 |
| 25 | proof obligations preserve lineage | **PASS** — §25 |
| 26 | no invented platform price or value | **PASS** — §27, §34 |
| 27 | no decision leakage | **PASS** — no deliverable re-decided Options; `options.md` read 0 times |
| 28 | no comparator bias | **PASS** — §10 |
| 29 | no unsupported content | **PASS** — §34, count 0 |
| 30 | no systemic projection ceremony | **PASS** — §32 |
| 31 | **conditions survive across deliverables** (§36 mandatory cross-deliverable check) | **FAIL — F-1** |

### 36.2 Verdict

**Two material semantic failures. Per §52, one is enough, and the gate does not average.**

```text
STEP 6C: FAIL
```

The failures are narrow and they share one shape. Neither is a modelling error, neither moves an
authority, and neither changes a truth's meaning:

- **F-1** is a truth that **vanished** from one deliverable in one fixture.
- **F-2** is a bounded edge that carried **more than its declared payload** in every applicable fixture.

In both cases the frozen Step 6A model states the rule correctly, and the Step 6B runtime implements it
in a place the executing contract does not point at — an exclusion list in `render-contract.md` that the
template never restates, and a non-omissible guarantee that only one of six templates declares. The
defect is a **missing structural guard**, not a wrong idea.

Everything the gate was built to catch held: no decision leakage, no architecture leakage, no epistemic
promotion, no scope leakage, no comparator bias, no invented content, no estimate ownership leak, no
ceremony, and correct behaviour under all six adversarial probes — including the two hardest negatives,
DF-3 (*do not choose*) and DF-7 (*do not design or price the unevaluated destination*).

---

## 37. Recommendation

**Do not freeze Step 6. Apply one bounded repair, then re-run the two affected checks only.**

### 37.1 The smallest bounded repair

Both failures have the same root cause and the same shape of fix: **declare the guarantee in the contract
the renderer actually reads.** Two runtime files, both deliverable templates, both declaration-only.

**R-1 — `implementation-spec.template.md`** (closes F-1)

```yaml
# ── NON-OMISSIBLE CONTENT (§17.1) ─────────────────────────────────────────────
# Each is `required SUBJECT TO EXISTENCE`: absent upstream => not-applicable skip;
# present upstream => it RENDERS. Compression may never drop one.
non_omissible:
  - conditions_that_gate_build     # decisions.md# Conditions — any condition that must hold
                                   # before build starts, with owner · funded? · by-when
  - preconditions                  # decisions.md# Preconditions, in full
  - proof_obligations              # all, translated
  - open_work_items                # each with its owner
```

plus one sentence in the body making the carriage explicit, so a build-gating condition is never filed
under *"Itens de trabalho em aberto"* by default. This mirrors what `executive-report.template.md`
already declares, and adds no new slot, no new state and no new vocabulary.

**R-2 — `executive-report.template.md`** (closes F-2)

Define the `investment_summary` payload as a field list, and restate the exclusion list where the
renderer will see it:

```yaml
slot_payload:
  investment_summary:
    includes: [base effort, range, contingency-inclusive total, confidence statement]
    excludes: [phases, work breakdown, team mix, contingency derivation,
               effort arithmetic, duration, candidate inventories]
```

and add to `forbidden_transformations`: *projecting phases, work breakdown, team mix, contingency
derivation, duration or a candidate inventory into the investment paragraph — the Estimate owns them and
the edge does not carry them.*

### 37.2 Repair scope — what must not change

| Not touched | Why |
|---|---|
| Step 3, Step 4, Step 5 | frozen; neither failure touches them |
| the frozen Step 6A model | both rules are already stated correctly there; only their runtime guards are missing |
| the deliverable set | still 6 |
| the render-gap classes | still 4 |
| the estimation modes | still 2 |
| the deliverable→deliverable edges | still 2, unchanged in direction and in source |
| `render-contract.md` | its wording is already correct; the repair brings the templates into line with it, not the reverse |
| routers, new states, knowledge preloads, new research | none introduced |

**Two files. Declaration-only. No behavioural machinery added.**

### 37.3 Re-run scope after the repair

Not the whole gate. Only:

1. **DF-1** — re-render the Implementation Specification and confirm the build-gating condition survives
   (F-1).
2. **DF-1, DF-2, DF-5, DF-7** — re-render the Executive investment paragraph against the declared field
   list (F-2).
3. **Two structural tests** to make the guards permanent, in the T-D numbering's repair-class style
   (as R-1/R-2 were added in Step 6B §30.6): one asserting the Specification declares `non_omissible`
   with build-gating conditions; one asserting the Executive declares the `investment_summary` payload
   field list and its exclusions.

Everything else in this report stands and does not need re-running: the eight fixtures, the five other
adversarial probes, the epistemic and proof lineages, the source-edge graph, the class-6 and headless
behaviours, and the scope-pair projections all passed and are unaffected by either repair.

### 37.4 Where evidence was missing

In no case was a gap filled by invention. The two places where the runtime had no upstream number
(DF-7's `ST-01` band, DF-7's R destination) were preserved as a named uncertainty and an open work item.
That behaviour needs no repair — it is the behaviour the gate exists to confirm.

---

```text
STEP 6C — DELIVERABLE SEMANTIC/PROJECTION GATE: FAIL
DF FIXTURES EXECUTED: 8/8
SEMANTIC DEFECTS: 2
DF FIXTURES WITH AT LEAST ONE FAILURE: 4/8
DISCOVERY FIVE-STATE BEHAVIOUR: PASS
DISCOVERY TECHNOLOGY NEUTRALITY: PASS
EXECUTIVE DECISION FIDELITY: PASS
EXECUTIVE FRESH COMPARISON DETECTED: NO
EXECUTIVE ESTIMATE PROJECTION: OTHER
EXECUTIVE COMPLETE WITHOUT ESTIMATE: YES
EXECUTIVE / ESTIMATE ORDER INVARIANCE: PASS
ARCHITECTURE BLUEPRINT FIDELITY: PASS
NOT-AUTHORIZED EMPTY BLUEPRINT GENERATED: NO
IMPLEMENTATION SPEC ARCHITECTURE FIDELITY: PASS
FRICTION CREATED NEW PROOF WORK: NO
MODE-A OMITTED-WORK PROBE: PASS
ESTIMATE INVENTED OMITTED SPEC WORK: NO
MODE-B CANDIDATE ISOLATION: PASS
CANDIDATE ESTIMATES BLENDED: NO
STRUCTURAL OPEN-CHOICE DESIGN BRIEF: BLOCKED
HEADLESS PROJECTION: PASS
SCOPE-PAIR PROJECTION: PASS
CLASS-6 UNEVALUATED DESTINATION DESIGNED: NO
CLASS-6 UNEVALUATED DESTINATION ESTIMATED: NO
S8 / ESTIMATE SEPARATION: PASS
IMPLEMENTATION EFFORT ORIGINATED IN SYNTHESIS: NO
PROOF-OBLIGATION LINEAGE: PASS
EPISTEMIC LINEAGE: PASS
VOLATILE-VALUE HANDLING: PASS
DELIVERABLE-TO-DELIVERABLE READ EDGES: 2/2
UNEXPECTED THIRD READ EDGE: NO
UNSUPPORTED CONTENT INVENTED: 0
DECISION LEAKAGE DETECTED: NO
ARCHITECTURE LEAKAGE DETECTED: NO
COMPARATOR BIAS DETECTED: NO
SYSTEMIC PROJECTION-CEREMONY DETECTED: NO
RUNTIME MODIFIED DURING INITIAL GATE: NO
NEW RESEARCH PERFORMED: NO
DELIVERABLE LAYER DEFENSIBLE: YES
READY TO FREEZE STEP 6 — DELIVERABLE TEMPLATES: NO
```

---

# 38. Bounded repair and targeted re-gate (appended)

The initial Step 6C gate stands as recorded above. This section is an **addendum**, not a rewrite.

```text
INITIAL STEP 6C GATE: FAIL
SEMANTIC DEFECTS FOUND: 2
DF FIXTURES WITH AT LEAST ONE FAILURE: 4/8
        ↓
bounded repair
        ↓
targeted replay
        ↓
final Step 6 verdict
```

## 38.1 Documentation corrections applied to the initial record

Three, all applied in place above, none of them a retroactive pass.

| # | Correction | Where |
|---|---|---|
| 1 | `DF FIXTURE FAILURES: 1` was inconsistent with the body. F-2 affected the Executive in **DF-1, DF-2, DF-5 and DF-7**; F-1 additionally affected DF-1. Replaced with `SEMANTIC DEFECTS: 2` + `DF FIXTURES WITH AT LEAST ONE FAILURE: 4/8` | final block |
| 2 | **F-2 reclassified J → G.** J is *unexpected direct dependency / read edge*; F-2 introduced no edge. The `estimate → executive-report` edge is authorized, its direction never changed, and the edge count stayed 2/2. The failure is what the approved edge **carried** — projection outside its declared payload — which is class **G, transformation / projection-boundary overreach**. No new failure class was created | §35 |
| 3 | **`FROZEN STEP 6A DEFECTS: 0`.** The earlier "M: 0 standalone, but root cause of both" was self-contradictory: the report itself shows Step 6A states both rules correctly (§17.1 for F-1; §5/§6.5/§28.2/§34 for F-2). Root cause restated as *missing executable structural guard in the Step 6B runtime contract* | §35 |

## 38.2 Repair scope

Runtime files changed — **exactly the three authorized**, plus this report:

```text
library/packs/pp/deliverable-templates/implementation-spec.template.md   (F-1)
library/packs/pp/deliverable-templates/executive-report.template.md      (F-2)
.claude/tests/test_pp_deliverable_templates.py                           (guards R-3, R-4)
docs/…/step-6c-deliverable-semantic-gate-report.md                       (this addendum)
```

Not touched: Step 3, Step 4, Step 5, the frozen Step 6A model, `render-contract.md`,
`blueprint-contract.md`, `pack.yaml`, the synthesis templates, the other four deliverable templates.
**No deliverable added. No state added. No router. No Estimate mode changed. No research performed.**

### `aisa-render` required no change — and here is why

§21 required a STOP-and-report if the renderer needed changing to understand the new declarations. It
does not, because both repairs ride on machinery `aisa-render` already executes:

| Repair | Mechanism it uses | Already in `aisa-render` |
|---|---|---|
| F-1 carriage | `build_gates` is a declared **`conditional_slots`** entry with a `slot_conditions` entry and a `slot_sources` entry | yes — execution steps 4a and 4b resolve exactly these, generically |
| F-1 prohibition | two new `forbidden_transformations` entries | yes — step 1 parses the field; hard rule 5 enforces it |
| F-2 bound | the `investment_summary` `slot_sources` text now names its payload fields inline, and every excluded class is named in `forbidden_transformations` | yes — same two mechanisms |

`non_omissible` and `slot_payload` are contract-level declarations inside frontmatter the renderer
already parses wholesale; `non_omissible` had precedent in `executive-report.template.md` before this
repair. **No new behavioural machinery was added, silently or otherwise.**

## 38.3 F-1 repair — build-gating carriage in the Implementation Specification

**Contract change** (`implementation-spec.template.md`), declaration-only:

```yaml
non_omissible:                   # the template had NO such block before
  - build_gating_conditions
  - preconditions
  - proof_obligations
  - open_work_items

build_gates:                     # the dedicated carriage path
  source: [decisions.md# Conditions, decisions.md# Preconditions]
  include_if:
    - the condition gates build (before build starts, or before a named build activity)
    - the precondition gates implementation or release
  preserved_per_gate: [condition text, owner, funded, by_when, gates, status]
  identities_preserved: conditions, preconditions and open work items stay THREE DISTINCT things
  satisfaction_rule:   a gate becomes satisfied ONLY through engagement evidence;
                       projection never satisfies a gate
  applicability:       no gates ⇒ not applicable, omitted with its reason, logged as a skip
```

plus `build_gates` as a **conditional slot** marked `REQUIRED SUBJECT TO EXISTENCE`, its own body
section (§2, *Portões de construção*), and two new `forbidden_transformations`:

- *dropping, compressing away or re-labelling a build-gating condition or a precondition — filing one
  under `open work items` is NOT carriage*;
- *rendering a build gate as satisfied without recorded engagement evidence*.

The initial gate observed that a condition with an owner, a funding state and a due date is not
semantically an open work item. The repair honours that: `open_work_items` no longer carries build gates,
and the three identities are declared distinct.

### Targeted replay — DF-1 Implementation Specification (v02)

Source condition, from `decisions.md# D-014 — Conditions`:

> *"O modelo de segurança por linha/coluna tem de ser validado com o auditor interno **antes do arranque
> de construção**."* — Auditoria Interna · financiada: sim · até 2026-10-31

Rendered §2:

| # | Portão | Tipo | Dono | Financiada? | Até quando | O que trava | Estado |
|---|---|---|---|---|---|---|---|
| G-1 | O modelo de segurança por linha/coluna tem de ser validado com o auditor interno **antes do arranque de construção**. | condição (D-014) | **Auditoria Interna** | **sim** | **2026-10-31** | **o arranque de construção** — nenhuma unidade de trabalho de §4, §5 ou §8 começa antes | **por satisfazer** |
| G-2 | Ambiente de produção governado provisionado com política de DLP aplicada. | pré-condição (D-014) | Equipa de Plataforma | sim | — | qualquer release para produção (§9) e a execução de P-2 (§13) | **por satisfazer** |

| Check | Result |
|---|---|
| condition text preserved | **PASS** |
| *"antes do arranque de construção"* preserved | **PASS** |
| owner `Auditoria Interna` | **PASS** |
| funded `sim` | **PASS** |
| due date `2026-10-31` | **PASS** |
| what it gates is named | **PASS** — build start, with the specific sections it blocks |
| status rendered, and rendered as **unsatisfied** | **PASS** |
| never converted to *validado* | **PASS** |
| precondition kept distinct from condition | **PASS** — G-2 typed `pré-condição` |
| open work items still a separate section | **PASS** — §16, unchanged |
| gate reachable from the sequencing section | **PASS** — §14 now leads with *G-1 antes de §8 e antes de P-1* |

**An implementation team cannot miss this gate**: it is section 2, before any build content; it names
what it blocks; and the sequencing section refuses to start the role matrix without it.

**F-1 BUILD-GATING CONDITION CARRIAGE: PASS.**

## 38.4 F-2 repair — the bounded investment payload

**No edge change, no source change, no new authority.** The edge stays
`estimate → executive-report`, headline only. What was missing was a definition of *headline* in the
contract the renderer reads.

**Contract change** (`executive-report.template.md`), declaration-only:

```yaml
slot_payload:
  investment_summary:
    form: ONE paragraph, maximum
    includes: [base_effort, effort_range, contingency_inclusive_total, confidence_statement]
    excludes: [phases, work_breakdown, team_mix, contingency_rate_or_derivation,
               effort_arithmetic, duration_or_calendar_schedule, candidate_inventories,
               detailed_uncertainty_inventory]
    attribution: the Executive PROJECTS the figure; it never recomputes, re-rounds,
                 recombines, interpolates or derives from it
    unresolved_architecture_rule: mode B — may NOT combine candidate estimates into one
                 headline; omit, or reference them qualitatively without blending.
                 No midpoint, no combined range, no "best candidate" figure, no scoring
```

The distinction the repair encodes: **the Executive receives the result, not the calculation anatomy.**
`32,4 pessoa-dias com contingência incluída` is a result; `+20% de contingência` explains the
derivation and is therefore excluded.

Added to `forbidden_transformations`: *projecting phases, work breakdown, team mix, contingency
derivation or rate, effort arithmetic, delivery duration or calendar schedule, a detailed uncertainty
inventory, or candidate inventories from the Estimate into the investment paragraph*; plus
*recalculating, re-rounding, recombining or interpolating an effort figure*; plus *blending candidate
planning estimates into one headline figure, or naming a best candidate*.

### Targeted replay — the four affected Executives (v02)

| Fixture | Rendered investment paragraph (v02) | Forbidden classes present |
|---|---|---|
| **DF-1** | *"A Estimativa situa o esforço de implementação em **27 pessoa-dias base**, numa gama de **25 a 32 pessoa-dias**, com um total de **32,4 pessoa-dias** incluindo contingência, a uma **confiança média-alta**…"* | **none** — the `+20%` derivation is gone |
| **DF-2** | *"…**19 pessoa-dias base**, numa gama de **17 a 24 pessoa-dias**, com um total de **22,8 pessoa-dias** incluindo contingência, a uma **confiança média**…"* | **none** — the `+20%` derivation is gone |
| **DF-5** | *"…numa gama de **78 a 110 pessoa-dias**, já com contingência incluída, a uma **confiança média**…"* | **none** — the team-mix clause is gone |
| **DF-7** | *"…**77 pessoa-dias base**, numa gama de **76 a 107 pessoa-dias** já com contingência incluída, a uma confiança **moderada no limite inferior, baixa no superior**…"* | **none** — team mix, the *16–22 semanas* duration, the `10 %` rate and the *oito itens de incerteza* count are all gone |

Mechanically scanned, per paragraph, for every excluded class:

| Excluded class | DF-1 | DF-2 | DF-5 | DF-7 |
|---|---|---|---|---|
| team mix (profiles, headcount, allocation %) | 0 | 0 | 0 | 0 |
| contingency rate or derivation | 0 | 0 | 0 | 0 |
| duration / calendar schedule | 0 | 0 | 0 | 0 |
| phases | 0 | 0 | 0 | 0 |
| work breakdown | 0 | 0 | 0 | 0 |
| effort arithmetic | 0 | 0 | 0 | 0 |
| detailed uncertainty inventory | 0 | 0 | 0 | 0 |
| candidate inventories | 0 | 0 | 0 | 0 |
| **paragraph count** | **1** | **1** | **1** | **1** |

Every projected figure was verified against its own Estimate — no re-rounding, no interpolation, no
recombination. One paraphrase was caught and corrected during the replay: DF-5's confidence was written
as *"moderada"* where the Estimate records **"Média"**; the paragraph now carries the recorded wording.
DF-7's now reads *"moderada no limite inferior, baixa no superior"*, matching its Estimate §11 verbatim.

All four remain clearly attributable: each names the Estimate as the owner of the figure and cites its
rendered file.

**F-2 DF-1 / DF-2 / DF-5 / DF-7 EXECUTIVE PAYLOAD: PASS.**

### DF-3 (mode B) — checked, not re-rendered

DF-3 was outside the authorized replay set, but the new `unresolved_architecture_rule` now applies to it.
Checked against the three binding prohibitions: **no midpoint · no combined range · no "best candidate"
figure**, and it states that separate per-candidate estimates exist, that there is no single number, and
that the effort difference is not an argument for either candidate. It is compliant as rendered; no
re-render was performed and none is required.

## 38.5 Structural guards added

Two repair classes, **outside** the canonical T-D numbering, following the Step 6B §30.6 precedent
(R-1, R-2). Both parse the frontmatter as structured data rather than grepping tokens.

| Class | Asserts | Tests |
|---|---|---:|
| **R-3** — build-gating condition carriage | the Specification declares `non_omissible` naming build-gating conditions and preconditions · a dedicated `build_gates` carriage path exists with `source`, `include_if`, `preserved_per_gate`, `identities_preserved`, `satisfaction_rule` · the source is the decision record · owner, funding, date and *what it gates* are preserved · `build_gates` is a declared slot with a condition, a source and a body section · it is `REQUIRED SUBJECT TO EXISTENCE` · `open_work_items` may not absorb it · **a gate cannot be satisfied by projection** | 9 |
| **R-4** — bounded investment payload | `slot_payload.investment_summary` declares exactly the four allowed fields · all eight excluded classes are declared · one paragraph, with attribution forbidding recompute/re-round/recombine/interpolate/derive · the mode-B no-blending rule · `forbidden_transformations` names every excluded class · the Executive may not recalculate or blend · the slot source points at the bounded payload · **the Estimate remains the effort authority** · **the edge itself is unchanged** | 9 |

**T-D1 … T-D22 coverage is unchanged at 22/22.** Neither class alters a canonical assertion.

One canonical test needed a **test-side anchor fix**, not a semantic change:
`TestTD2Headless.test_impl_spec_screens_section_is_marked_conditional_in_the_body` located the screens
section by the hard-coded heading `## 4.`. Inserting `build_gates` as §2 renumbered the body, so the
assertion now anchors on the `{{screens_to_build}}` slot instead of on a section number. It asserts
exactly what it asserted before — that the screens section is marked conditional on
`experience.mode == none` — and will not break on the next renumber. This tracks a body migration and
changes no semantics, exactly as the Step 6B §25 Step-5 test inversion did.

## 38.6 Regression

| Suite | Before | After | Result |
|---|---:|---:|---|
| `test_pp_deliverable_templates.py` | 200 | **218** (+9 R-3, +9 R-4) | **OK** |
| `test_pp_options_decision_model.py` (Step 3) | 95 | 95 | **OK** |
| `test_pp_domain_knowledge.py` (Step 4) | 64 | 64 | **OK** |
| `test_pp_architecture_templates.py` (Step 5) | 116 | 116 | **OK** |
| `test_pp_discovery_runtime.py` · `test_council_wiring.py` · `test_orchestrator_wiring.py` · `test_state_scaffold.py` | 91 | 91 | **OK** |
| **Comparable total (Step 6B §30.7 basis)** | **566** | **584** | **0 failures** |
| `library/kernel/tools/tests/test_text_extract.py` | 23 | 23 | **OK** |
| **Full total** | 589 | **607** | **0 failures** |

**Step 3 regression: PASS. Step 4 regression: PASS. Step 5 regression: PASS.** No semantic Step 3B2 /
4C / 5C replay was run, as instructed.

## 38.7 Invariants re-confirmed after the repair

| Invariant | Result |
|---|---|
| Estimate remains the semantic owner of every implementation-effort figure | **YES** — `owns_calculation: true` on the Estimate only; R-4 asserts the Executive never claims it |
| Executive recalculates, re-rounds, recombines, interpolates or derives duration | **NO** — 0 leak tokens across all four repaired Executives |
| deliverable→deliverable read edges | **2/2**, unchanged — the only `_render/` reference in an allowed source field is the Executive's `investment_summary`; every other one sits in `forbidden_sources` |
| new source edge introduced | **NO** |
| order invariance (E-1/E-2/E-3) | **holds** — re-confirmed mechanically on the repaired DF-1 Executive: with the Estimate absent the section is omitted (17 → 16 sections), the report stays complete, and there is no gap, no placeholder and no calculation in the Executive or in financial synthesis. No render-order redesign was performed |
| Step 6A semantics changed | **NO** |
| new state, router, deliverable or Estimate mode | **NO** |

## 38.8 Previously passing results, preserved

Not reopened and not re-run, per §20: Discovery five-state behaviour · Discovery neutrality ·
closest-authority behaviour · Executive comparison · Blueprint fidelity · headless · scope pairs ·
class 6 · the friction probe · the Mode-A omitted-work probe · structural Design Brief blocking ·
Mode-B isolation · S8 vs Estimate · financial synthesis · proof lineage · epistemic lineage · volatile
values · DK/CRAFT pull discipline · source-edge count · ceremony · unsupported-content count.

The bounded repair caused **no regression** in any of them: the two changed templates altered only the
Specification's condition carriage and the Executive's investment payload, and the full suite passes.

## 38.9 Targeted re-gate result

```text
STEP 6C TARGETED RE-GATE: PASS

INITIAL SEMANTIC DEFECTS: 2
REMAINING SEMANTIC DEFECTS: 0
TARGETED RE-GATE FAILURES: 0

STEP 6 — DELIVERABLE TEMPLATES: FROZEN
```

The audit trail reads:

```text
STEP 6C INITIAL GATE: FAIL
→ bounded repair (2 deliverable contracts, declaration-only; 2 structural guard classes)
→ targeted re-gate: PASS
→ STEP 6 FROZEN
```

---

```text
STEP 6C — BOUNDED REPAIR / TARGETED RE-GATE: PASS
INITIAL SEMANTIC DEFECTS: 2
INITIAL DF FIXTURES WITH >=1 FAILURE: 4/8
F-1 BUILD-GATING CONDITION CARRIAGE: PASS
F-1 CONDITION RETAINS OWNER/FUNDING/DATE/GATE: PASS
F-2 DF-1 EXECUTIVE PAYLOAD: PASS
F-2 DF-2 EXECUTIVE PAYLOAD: PASS
F-2 DF-5 EXECUTIVE PAYLOAD: PASS
F-2 DF-7 EXECUTIVE PAYLOAD: PASS
EXECUTIVE PROJECTS TEAM MIX: NO
EXECUTIVE PROJECTS CONTINGENCY DERIVATION/RATE: NO
EXECUTIVE PROJECTS DELIVERY DURATION: NO
EXECUTIVE RECALCULATES IMPLEMENTATION EFFORT: NO
ESTIMATE REMAINS EFFORT SEMANTIC AUTHORITY: YES
DELIVERABLE-TO-DELIVERABLE READ EDGES: 2/2
NEW SOURCE EDGE INTRODUCED: NO
STEP 6A SEMANTICS CHANGED: NO
STEP 3 REGRESSION: PASS
STEP 4 REGRESSION: PASS
STEP 5 REGRESSION: PASS
TARGETED RE-GATE FAILURES: 0
REMAINING SEMANTIC DEFECTS: 0
NEW RESEARCH PERFORMED: NO
READY TO FREEZE STEP 6 — DELIVERABLE TEMPLATES: YES
```

`STEP 6 — DELIVERABLE TEMPLATES: FROZEN`
