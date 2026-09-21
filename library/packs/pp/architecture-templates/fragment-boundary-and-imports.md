---
template_id: architecture-fragment-boundary-and-imports
category: architecture
scope: boundary-fragment          # NOT an option class, NOT an architecture shape
repeatable: true                  # ONE instance per qualifying component — the skill iterates
activates_on: >
  one instance for each compositions[] entry with boundary: outside-platform, or any composition beyond
  `direct`, and one instance for each relocated_responsibilities[] entry
required_slots:
  - component_or_responsibility
  - pattern_or_owner
  - forced_by
  - boundary
  - owner
optional_slots:
  - incumbent_fit_unevaluated
  - status_resource
  - reconciliation_owner
  - enclosing_boundary
output_format: md
---

<!--
BOUNDARY / IMPORT FRAGMENT — one instance per qualifying architecture component.

IDENTITY (binding):
    composition fragment key             → <scope>::component::<component>
    relocated responsibility fragment key → <scope>::responsibility::<responsibility>

`component` is the uniqueness-bearing field for a composition; `responsibility` is the identity for a
relocation. Two components may legitimately share the same pattern, the same owner, the same boundary and
even the same forcing requirement, and still render as SEPARATE instances. `component` is
human-readable, local to the architecture scope, unique within it, not globally stable, not canonical
vocabulary and not a registry id. No UUIDs; no identifier subsystem.

Two entries in one scope declaring the same `component` name — or two relocations sharing a
`responsibility` — is an ARCHITECTURE CONTRACT DEFECT. Fail. Never merge, never auto-suffix, never
overwrite, never collapse imports.

INVARIANT:
    N unique qualifying composition components + M unique relocated responsibilities
    ⇒ exactly N + M instances of this fragment

Per instance: the key appears exactly once; all SIX channels appear; each channel is either populated or
carries `not engaged — <reason>`. A MISSING CHANNEL IS A DEFECT.

The scope prefix exists only for deterministic uniqueness across a multi-scope blueprint. It is
structure, never rendered as engagement vocabulary.

WHAT THIS FRAGMENT DOES NOT DO:
- It does not decide whether the composition is justified. `forced_by` is a recorded requirement.
- It does not judge whether the far side is a good design, and draws no comparator claim about it.
- It does not restate pattern strengths, pattern weaknesses, the risk catalogue, mechanism descriptions,
  service limits or volatile readings. It STRUCTURES the obligations the engaged pattern imports.
  `../domain-knowledge/architecture/patterns.md` §3 plus THE ONE engaged composition in §5 is the pull;
  the mechanism unit behind it is a second pull only where a material dependency is exposed.
- It owns no platform number. A volatile value resolves to an engagement-verified SU row with
  `verificado_em` and `validade`, or to a verification obligation.
-->

#### Componente: {{component_or_responsibility}}

| Campo | Valor |
|---|---|
| Identidade (chave de fragmento) | `<scope>::component::<component>` \| `<scope>::responsibility::<responsibility>` |
| Composição / owner externo | {{pattern_or_owner}} |
| Forçado por | {{forced_by}} — <the named requirement; never a preference> |
| Fronteira | {{boundary}} |
| Owner | {{owner}} |

<!--
`owner` here is the **role, team or organisation** that owns the far side of the boundary — what the
composition needs in order to be described at all. It is never a person, and `owner: <role> — not named`
is a complete value.

`owner: UNKNOWN` does **not** make the composition unavailable, and this template emits no availability
verdict (`decision-model/blocking-set.md`, `composed-disqualifiers.md`: a missing name or a missing
maturity produces a requirement, a condition, a cost or a risk — never an exclusion). What an unknown
owner means depends on which of two things is missing: if no side of the boundary has an **operating
model** — no role authorised to intervene, no diagnostic or recovery interface — that is a structural
open architecture choice in A12 (blocking approval, per A10); if the model exists and only the holder is
unnamed, nothing is open. Where the organisation has not yet decided who owns the far side, that is a
**requirement of the to-be**, carried with the simpler composition and a tripwire on the metric that
would force the move — the honest output the pattern unit already prescribes.
-->

**Marcadores**: <`INCUMBENT FIT UNEVALUATED` where the owner is the incumbent — preserved verbatim, and
comparator fit never inferred; otherwise `(none)`.>

**Gates registados** (relocations): <operator · support · skills · cross-boundary release owner ·
maturity — the recorded gate values, or `not recorded` per gate.>

**Conditional — recurso de estado**: engaged for a background or asynchronous composition. A status
resource is then a **mandatory obligation**: state what it is, who reads it, and how a caller learns the
outcome. Otherwise `not applicable — <reason>`.

**Conditional — reconciliação**: engaged where the composition replicates or copies data. What is then
mandatory is the **mechanism**: the role authorised to reconcile, the identity and permission it uses, how
a divergence is detected, where that fact is sent, and the procedure that closes it. The role is required;
a name is not, and `not named` against a stated role satisfies this. Otherwise
`not applicable — <reason>`.

**Conditional — fronteira envolvente**: engaged where `enclosing: true`. This component **encloses** the
others rather than replacing them — state what it encloses and what the enclosure changes for each
enclosed component. Otherwise `not applicable — <reason>`.

##### Obrigações importadas — seis canais (nenhum pode faltar)

**1. Governação**
<the new controlled asset; who may create and change it; who classifies its data; and **which platform
controls stop applying at its edge**.>
<!-- or: not engaged — <reason> -->

**2. ALM**
<how many release routes now exist; which contract must stay version-compatible; what is rebound after
each deployment.>
<!-- or: not engaged — <reason> -->

**3. Custo**
<the new meters and the population each is charged against. **Drivers only — no prices.**>
<!-- or: not engaged — <reason> -->

**4. Monitorização**
<the new health signal; where its failures land; and the correlation the design must generate itself.>
<!-- or: not engaged — <reason> -->

**5. Recuperação**
<what happens, in what order, after a restore of any participant — and **who reconciles**.>
<!-- or: not engaged — <reason> -->

**6. Operador**
<the role paged, the destination the alert reaches, and the permission that role needs to act. A role, never
a person.>
<!-- or: not engaged — <reason> -->

##### O que este pack não sabe sobre o outro lado

<For a relocated responsibility: state explicitly what this pack has **no** evidence about — the far
side's internals, its fit, its cost and its roadmap. A boundary and an owner are described here — **never
a PP design for the far side**, and no comparator claim is drawn. For an in-platform component,
`not applicable`.>
