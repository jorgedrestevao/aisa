---
template_id: architecture-fragment-experience-inherited
category: architecture
scope: experience-fragment        # NOT an option class, NOT an architecture shape
activates_on: architecture.experience.mode == inherited
renders: [A4, A7-human-user-specialization, A8-inherited-form]
required_slots:
  - host
  - graduation_trigger
optional_slots:
  - verified_ceiling
  - replacement_of_existing_artefact
output_format: md
---

<!--
EXPERIENCE FRAGMENT — inherited. Surface access, lifecycle and capacity are inherited from a host.
Embedded surfaces (a customised list form, a report visual, a chat tab) belong here.

BOUNDARIES (binding):
- This fragment must NOT claim that this platform is excluded. It is not. An inherited capability is a
  documented-sufficiency answer, and the platform stays available.
- It must NOT decide WHEN graduation occurs, nor whether the capability is architectable here. Both are
  recorded facts read into this fragment.
- It does not own store choice (A5) and does not own security truth (A7).
- It owns no platform number. The capacity ceiling is an ENGAGEMENT-VERIFIED value with `verificado_em`
  and `validade`, or a verification obligation — never a figure stated by this template.
- Domain Knowledge: `application/application-surfaces.md` for the host surface and its forfeits, and the
  relevant store unit for the host's own limits. One pull per responsibility.
-->

#### A4.1 — Host e acesso herdado

**Host**: {{host}}

<what the host is, and precisely what is inherited from it: who can reach the surface, how access is
granted and revoked, and what the host's own audience boundary is. Access is **not** administered by this
solution — state who administers it, by role.>

#### A4.2 — Ciclo de vida herdado

<the solution has **no independent lifecycle**: it lives and dies with the host artefact. State what that
means concretely — how a change is released, what happens when the host is moved, renamed, archived or
deleted, and who is able to do each of those without consulting the owner of this workflow.>

#### A4.3 — Tecto de capacidade (valor verificado no engagement)

<!-- The ceiling is engagement evidence, never a template number. -->

<where engagement evidence exists, render:
`<valor verificado> · verificado_em <data> · validade <prazo> · re-verificar quando <gatilho>`,
citing the SU row. Where no verified row exists, render the **verification obligation** instead: what
must be measured, by whom, at what fidelity, and by when. Never substitute a remembered or documented
figure for a verified one.>

#### A4.4 — Gatilho de graduação (obrigatório)

**Gatilho**: {{graduation_trigger}}

<This section is **mandatory**; without it the output is malformed. State the measurable condition under
which the inherited capability stops being sufficient and the workflow must move to an owned surface —
and state it as a tripwire with its metric, its source in the SU, and who watches it.

State plainly that growth past this trigger is a **one-way graduation**: what is carried over, what is
rebuilt, and what the move costs. **When** to graduate is not decided here — the trigger is recorded, and
the tripwire mechanism fires it.>

#### A4.5 — Forfeits do modelo herdado

<what the inherited model forfeits, each as an accepted consequence with its id and the unit that
documents it: interface-level access, extensibility, audit depth, field-level security, offline
capability, and portability of the solution as a deployable unit. State the consequence, not the
mechanism.>

#### A4.6 — Substituição de um artefacto existente

<!-- CONDITIONAL. Otherwise `not applicable — <reason>`. -->

<where this inherited surface replaces an existing artefact: what is replaced, what is migrated, what is
abandoned, and who confirms the replacement is complete.>

#### A7 (especialização) — utilizador humano no host

<the human-user role model **as the host expresses it**, and the gap between it and the model the
workflow actually needs. Where the host cannot express a needed separation of duties, that gap is an
accepted forfeit with an id, or an open architecture item — never silently closed. The enforcement plane
and the controls themselves stay in **A7 of the core**.>

#### A8 (forma herdada) — sem topologia independente

<State explicitly: **no independent environment, policy plane or release topology exists** for this
solution, and that this is a **choice** with consequences — not an omission and not a gap. Name what is
consequently unavailable: environment separation, a governed release route, policy application at the
solution's own boundary, and independent recovery. Name who accepts each consequence.>
