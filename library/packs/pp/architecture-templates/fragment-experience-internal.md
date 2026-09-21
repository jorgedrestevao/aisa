---
template_id: architecture-fragment-experience-internal
category: architecture
scope: experience-fragment        # NOT an option class, NOT an architecture shape
activates_on: architecture.experience.mode == owned-internal
renders: [A4, A7-human-user-specialization, A8-owned-lifecycle]
required_slots:
  - primary_surface
  - personas
optional_slots:
  - offline_and_device
  - distribution
output_format: md
---

<!--
EXPERIENCE FRAGMENT — owned-internal. The solution owns its surface and access lifecycle; the audience
is internal directory identity.

BOUNDARIES (binding):
- This fragment carries ONLY the human-facing specialization. It does NOT own store choice (A5) and does
  NOT own security truth (A7) — it may specialize the human-user part of A7 and never replace it.
- It does not decide whether a surface exists, which surface is chosen, or which store holds the records.
  `primary_surface` is a recorded value, read here.
- It owns no platform number. Density, field counts and screen caps come from the pack's CRAFT
  screen units as the FORM of the screen architecture; every platform limit is cited from the owning
  RESEARCH unit. Where CRAFT and RESEARCH disagree, RESEARCH wins and the CRAFT statement is a defect
  to report.
- Domain Knowledge: one pull per responsibility — `application/application-surfaces.md` for the surface
  and its forfeits, `data/query-and-delegation.md` for access-path behaviour. A second pull only where
  the first exposes a material dependency.
-->

#### A4.1 — Superfície e audiência interna

**Superfície primária**: {{primary_surface}} — <the recorded value, with the responsibility it carries.>

<the internal audience and what the surface is responsible for: which tasks it owns, which it hands off,
and which it explicitly does not serve. Personas map to their access groups. Cite `su_refs` for every
persona and every responsibility.>

#### A4.2 — Arquitectura de ecrãs (handoff)

<the screen architecture handoff: screen types and patterns from the pack catalogue, sections and tabs,
role visibility, approval-as-action, and the naming convention. This is a HANDOFF to the approved UX
blueprint, not a re-derivation of it — the blueprint owns the screens; this section states what the
architecture commits to.

Pixel-level UX, component trees and expressions are downstream (implementation altitude), not here.>

#### A4.3 — Caminhos de acesso delegation-safe

<per surface: which access paths the design depends on, and which of them are delegation-safe against the
selected store. State the consequence of each non-delegable path — what silently truncates and what the
design does instead. `data/query-and-delegation.md` is the authority for what delegates; this section
states the architectural consequence, and repeats no limit of its own.>

#### A4.4 — Distribuição

<!-- CONDITIONAL. Otherwise `not applicable — <reason>`. -->

<how the surface reaches its audience: sharing model, who may grant access, what the audience must
already have, and what happens to access when a person changes role or leaves.>

#### A4.5 — Offline e capacidade de dispositivo

<!-- CONDITIONAL — engaged only where a named offline depth is required. Otherwise
     `not applicable — sem requisito de offline registado`. -->

<the required offline depth, the device capability it assumes, and what the selected surface and store
forfeit to provide it. Any capacity or sizing figure is an engagement-verified SU value with
`verificado_em` and `validade`, or a verification obligation — never a number owned here.>

#### A4.6 — Forfeits da superfície escolhida

<what the chosen surface gives up relative to the responsibilities the architecture asks of it, stated as
accepted consequences with their ids — not as risks to be resolved later. Cite the surface unit for each
forfeit.>

#### A7 (especialização) — modelo de papéis do utilizador humano

<the human-user role and permission model: groups, separation of duties, and the visibility matrix in the
FORM the pack's CRAFT security unit prescribes. The enforcement plane, the trust boundary, the control
that exists and where it takes effect stay in **A7 of the core** — this section never restates them and
never contradicts them.>

#### A8 (especialização) — ciclo de vida próprio

<where the solution owns its own lifecycle: which environments it occupies, its release route, and what
that ownership obliges the team to operate. Topology capability comes from the governance and ALM units;
naming and solution conventions may follow the pack's CRAFT delivery unit.>
