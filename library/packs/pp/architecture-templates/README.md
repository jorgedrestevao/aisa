# Architecture templates — positioning

<!--
provenance: RUNTIME · rewritten 2026-09-04 (Step 5B, implementing the frozen Step 5A model)
This file is the SINGLE home of the outcome-class reachability table and the architectability
boundary. No template file lists an outcome class. No file here owns a platform number.
-->

**An architecture template is a reusable output shape for an architecture that is already justified.
It is not an option, not an option class, and not an architecture shape you choose between.**

```text
OPTIONS DECISION MODEL   → whether and where architecture is defensible
DOMAIN KNOWLEDGE         → mechanisms, constraints, boundaries and obligations
ARCHITECTURE PATTERN     → reusable composition and what it imports
ARCHITECTURE TEMPLATE    → reusable output shape for an architecture already justified
```

The dependency runs downward only. A template never selects an option, assigns an outcome, determines
materiality, compares vendors or options, re-runs the Options spine (S0–S9), scores an architecture,
re-decides a Step 3 finding, or becomes a technical truth source.

## 1. Architecture Template ≠ Option

The Options procedure (`../decision-tree.md`) generates candidates from the option-class trigger map
(`../decision-model/alternatives-register.md`) and terminates in an outcome from the closed set
(`../decision-model/outcome-classes.md`). A comparison whose top level is *"one store-first shape versus
another store-first shape versus a split"* shows a sponsor **one option class presented as the whole
choice** — the defect the Options decision model exists to remove. Compare option classes first;
describe an architecture only for a scope where one is authorized.

## 2. Outcome reachability ≠ pack architectability

These are two independent factors, and each fails for its own reason. A sponsor reading *"no architecture
was produced"* must be able to tell *"the decision forbids one"* from *"this pack cannot author one"*.
**The two reasons are never merged.**

```text
architecture authorization = outcome reachability × active-pack architectability
```

**Outcome reachability alone is never sufficient.**

| Outcome | Selected solution | Result |
|---|---|---|
| class 1 or 2 | PP-containing | may authorize a PP architecture |
| class 1 or 2 | custom-only · packaged / SaaS · cloud-native-only · incumbent · another low-code platform | **no PP architecture authorization** |
| class 3 or 4 | PP keeps the near side | `authorized-bounded` for the PP side only |
| class 13(a) | the sufficient capability is inside this pack's architectable scope | may authorize; `experience.mode: inherited` |
| class 13(a) | the sufficient capability is outside it | **no PP architecture.** Documented sufficiency, *this platform is not excluded* and the graduation trigger are preserved in the decision and deliverable layers |
| any unreachable class | anything | not authorized, for the outcome's own reason |

## 3. Outcome-class reachability — this table's single home

Derived from `../decision-model/outcome-classes.md`. **Outcome → permission and scope to architect.
Never outcome → template.** The *reachable* column states **outcome reachability only**; every
"reachable" row still requires architectability (§4).

| # | Class | Architecture reachable? | Scope | Mandatory consequence |
|---:|---|---|---|---|
| 1 | Strong fit | reachable — authorized only if the selected option is PP-containing and architectable | the named scope | Render the class's *no documented constraint violated* sentence as the decision basis; never as endorsement |
| 2 | Fit with constraints | reachable — same architectability condition | the named scope | Every condition carried as *condition — owner — funded? — by when*; an unowned or unfunded condition is an open architecture item, never a silent assumption |
| 3 | Hybrid with cloud-native services | yes, bounded | the application scope only | The named responsibility gets a **boundary fragment**, never a PP design. The S7 gate record is required content |
| 4 | Hybrid with the incumbent system | yes, bounded | the experience / human-workflow scope only | Boundary fragment carrying `INCUMBENT FIT UNEVALUATED`. The incumbent's internals are not designed here |
| 5 | Poor fit — excluded for this scope | no for that scope | — | No PP architecture. Architect another scope only where it carries an emitted pair |
| 6 | Excluded for this responsibility | no for the named responsibility | surrounding scope only where a pair was **emitted** | Never infer the surrounding scope's authorization from the exclusion |
| 7 | Economically infeasible / unattractive | no | — | The subtype's discriminator is repeated verbatim. Funding a mandated control is an Options re-run, never a template-layer lift |
| 8 | Candidate set — comparative fit unevaluated | no | — | The terminal render of 5/6/7/14/13(b); belongs to the executive / discovery deliverables |
| 9 | Deployment model excludes this platform | no | — | The one class that may name a comparator; both halves of the sentence are repeated |
| 10 | Process redesign / no new application | no | — | No application exists to architect |
| 11 | Do nothing / defer | no | — | Revisit condition recorded; no architecture |
| 12 | Decision blocked | no | — | Architecture is **prohibited**, not deferred-with-a-draft. Draft mode (`/blueprint --option`) stays pre-decision only |
| 13(a) | Alternative sufficient — documented sufficiency | reachable, never automatic | the named shape | Where authorized: `experience.mode: inherited`. Where not architectable: no PP architecture; sufficiency, non-exclusion and the **graduation trigger** are preserved elsewhere. The trigger is mandatory either way |
| 13(b) | Alternative sufficient — candidate | no | — | The answer is another class, followed by class 8 |
| 15 | Viable if the rule is changed | no while the rule stands | — | The option is conditional, not excluded: no architecture until the rule changes and a new 1/2 pair is emitted. The rule, its cost and the role that can change it are carried into `/decide`; `status: refused` closes it for this engagement with a `Risky` row |
| 14 | In-place remediation unavailable — migration required | no on its own | — | Terminates in class 8. A rebuilt PP solution must arrive as a newly emitted 1/2 pair; then the core's *replacement of an existing artefact* section is engaged |

**Authorization vocabulary — three values, not fifteen.** Each requires **both** factors.

```text
authorized          ← an emitted class 1, 2 or 13(a) pair for this scope
                      AND the selected solution for that scope is architectable by this pack
authorized-bounded  ← an emitted class 3 or 4 pair, or class 6's surrounding scope
                      AND the PP-owned side is architectable; the far side never is
not-authorized      ← the outcome is unreachable, OR the selected solution is not architectable here.
                      Carries the emitted outcome sentence, plus the architectability reason where that
                      is what failed — the two reasons are never merged
```

**Two rules that keep this a gate and not a router.** No template file lists an outcome class — the table
above lives here and only here, and the *value* lives in the engagement's `architecture:` block. And
**authorization is read, never derived**: the template layer cannot compute an authorization from
evidence, cannot upgrade `authorized-bounded` to `authorized`, and cannot emit *decision blocked* — only
repeat one that Options emitted.

## 4. Active-pack architectability boundary

One question, answered from facts already recorded. No routing table, no new stage, no scoring, no
comparator logic, no pattern selection.

> **Is the selected solution for this scope something this pack has the authority and the knowledge to
> architect?**

| Architectable | Not architectable |
|---|---|
| A PP application (any experience mode) | A custom-only implementation |
| A PP automation or integration composition | A packaged-product / SaaS architecture |
| A PP solution composed with external components — **the PP side** | A cloud-native-only architecture |
| An inherited or native capability this pack explicitly covers | Incumbent-system internals |
| | Another platform's internals |
| | A candidate set with no selected architecture |

**The far side of a scope pair is never architectable here.** And the test states its own answer:
`architecture.architectability_basis` records why, in one sentence, so a reader never reconstructs it.

Where no scope is both outcome-reachable and architectable, **no PP architecture is produced**. That is
not automatically *Decision Blocked* — preserve the actual reason (outcome unreachable, or selected
solution outside this pack's architecture authority) and keep the two distinct.

## 5. Experience-mode semantics

Experience is **one optional architectural dimension** — not a shape, not a branch, not an option class.
It affects only experience-facing blueprint content and **selects no architecture**.

```text
Is there a human-facing surface in this architecture at all?
  no  → experience.mode: none          (headless — zero experience fragments)
  yes → does the solution own its own access model, lifecycle and capacity?
          no  → experience.mode: inherited
          yes → is any part of the audience outside the directory?
                  yes → experience.mode: owned-external
                  no  → experience.mode: owned-internal
```

| `experience.mode` | Meaning | `primary_surface` | Experience fragment |
|---|---|---|---|
| `none` | No human-facing surface is part of this architecture. A **finalized** value, not an Unknown | `null` | none |
| `owned-internal` | The solution owns its surface and access lifecycle; internal directory audience | required | `fragment-experience-internal.md` |
| `owned-external` | The solution owns a surface with an audience outside the directory | required | `fragment-experience-external.md` |
| `inherited` | Surface access, lifecycle and capacity inherited from a host | required | `fragment-experience-inherited.md` |

Embedded surfaces (a customised list form, a report visual, a chat tab) fold into `inherited`. Branded
native wrapping and code apps fold into `owned-internal` as `primary_surface` values with their own
forfeits.

## 6. Headless architecture semantics

A PP-containing architecture may legitimately have **no human-facing surface**: automation-only,
integration-only, scheduled machine work, event-driven processing, queue plus worker, background
processing, API-mediated orchestration, data movement and reconciliation.

```text
headless architecture = architecture-core
                      + ZERO experience fragments
                      + ZERO or more boundary/import fragment instances
```

**No headless-specific template exists and none is needed.** Where `experience.mode: none`:
`primary_surface` is `null`; **A4 is not engaged**; the render skill performs **zero** experience-fragment
includes and must **not** attempt to resolve `fragment-experience-none.md` (that file intentionally does
not exist); there is no placeholder, no missing-template warning, no render gap and no *surface
unresolved*. This is a finalized **not applicable** condition — a skip with a reason.

A headless architecture still carries A5 where a data authority exists, A6 automation and integration,
A7 service / managed / connection identity, A8 environments and release, A9 irreversible choices,
A10 operator and support, A11 economics and A12 proof obligations. **Do not fabricate a user surface.**

## 7. Pattern / composition relationship

**Ten canonical patterns → zero pattern-specific templates.** Patterns are entries in
`architecture.compositions[]`, named from `../domain-knowledge/architecture/patterns.md` §5, and rendered
through `fragment-boundary-and-imports.md` where qualifying. Composition of patterns is *N fragment
instances*, and their imports **accumulate rather than merge**.

Architecture composition and experience are **orthogonal dimensions**: `background-processing` with
`experience.mode: none` is as valid as `api-mediated` with `experience.mode: owned-internal`. Neither
dimension constrains the other, and neither is an option class.

No file in this directory is named after a product, a store or a vendor surface. *Same architectural
responsibilities + different store or mechanism implementation ⇒ same output shape, different resolved
content.*

## 8. Scope-pair rule

`(scope, outcome)` pairs stay **uncollapsed**. `A1` renders the pairs; the conditional *scope ownership*
section renders the ownership table. A relocated responsibility receives a responsibility name, an owner,
its outcome basis, a boundary and the relevant gates and imports — **never a PP design for the far side**.
This pack has no comparator evidence about the far side and must not draw one; where class 4 applies,
`INCUMBENT FIT UNEVALUATED` is preserved verbatim and comparator fit is never inferred.

Collapsing the pairs into a single template name is the failure mode this model replaces. No `hybrid`
shape exists, so it cannot recur.

## 9. Imported-obligation rule

A composition's **imports** are its most decision-bearing content. Carriage is structural, not editorial:

```text
for every compositions[] entry with boundary: outside-platform, or any composition beyond `direct`,
and for every relocated_responsibilities[] entry
  → exactly one instance of fragment-boundary-and-imports.md
  → each instance carries all SIX channels: Governance · ALM · Cost · Monitoring · Recovery · Operator
  → a channel is either populated, or marked `not engaged — <reason>`
```

**A missing channel is a defect.** The fragment structures and renders the obligations derived from the
engaged pattern; it does **not** restate pattern strengths, pattern weaknesses, the risk catalogue,
mechanism descriptions, service limits or volatile readings.
`../domain-knowledge/architecture/patterns.md` and the mechanism units remain the authority, and are cited
rather than copied.

## 10. Runtime taxonomy

```text
library/packs/pp/architecture-templates/
  README.md                          positioning — NOT a runtime template unit
  architecture-core.md               the entry point — A1…A3 + A5…A12 + conditional sections
  fragment-experience-internal.md    experience.mode: owned-internal
  fragment-experience-external.md    experience.mode: owned-external
  fragment-experience-inherited.md   experience.mode: inherited
  fragment-boundary-and-imports.md   one instance per qualifying architecture component
```

**Runtime template units: 5** (1 core + 3 experience fragments + 1 boundary fragment). There is one fixed
entry point — `architecture-core.md` — and one include driven by one recorded field. No router, no loop
primitive, no template-inheritance framework, no product-named template, no pattern-specific template and
no headless-specific template.

## 11. Legacy read compatibility

Three retired files — `sharepoint-first.md`, `dataverse-first.md`, `hybrid.md` — and the obsolete
`Branch (if technology)` decision field predate this model. Already-rendered artefacts are **immutable and
are not regenerated**; two engagements (`projects/cae-automation`, `projects/dpt-galp-jp`) carry a recorded
legacy branch value and a frozen rendered blueprint.

For **reading** a legacy artefact, interpret the recorded branch value as:

| Legacy branch value | Reads as |
|---|---|
| `sharepoint-first` | `experience.mode: owned-internal` with one `record_authority` entry whose authority is the list / library store |
| `dataverse-first` | `experience.mode: owned-internal` with one `record_authority` entry whose authority is the governed relational store |
| `hybrid` | `experience.mode: owned-internal` with **two** `record_authority` entries (governed relational + list / library). It was never a scope pair, and it is not one now |

This is **read compatibility only**. A *new* render must construct a proper `architecture:` block rather
than rely on this mapping. There is no shim, no router and no permanent dual architecture model, and the
mapping supplies no authorization: authorization is initialized at `/blueprint` entry from the frozen
outcome and the frozen selected solution against this pack's architecture scope.
