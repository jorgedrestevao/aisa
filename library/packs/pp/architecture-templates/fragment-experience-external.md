---
template_id: architecture-fragment-experience-external
category: architecture
scope: experience-fragment        # NOT an option class, NOT an architecture shape
activates_on: architecture.experience.mode == owned-external
renders: [A4, A7-human-user-specialization]
required_slots:
  - primary_surface
  - external_identity_provider
optional_slots:
  - anonymous_exposure
  - localization
  - offline_read
output_format: md
---

<!--
EXPERIENCE FRAGMENT — owned-external. The solution owns a surface whose audience is, at least in part,
outside the directory.

BOUNDARIES (binding):
- This fragment does NOT decide whether an external audience is required. That is a recorded fact from
  the engagement; this fragment renders its consequences.
- It does not own store choice (A5) and does not own security truth (A7) — it may specialize the
  human-user authorization form only.
- It owns no platform number: no price, quota, retention window or capacity figure. Where a volatile
  value is needed it resolves an engagement-verified SU value with `verificado_em` and `validade`, or
  renders the verification obligation.
- Domain Knowledge: `application/application-surfaces.md` for the surface and build model,
  `governance/governance-and-environments.md` for the exposure and policy plane,
  `security/security-controls.md` for what each control does. One pull per responsibility.
-->

#### A4.1 — Pré-requisito: audiência externa

<the recorded fact that part of the audience is outside the directory, with its `su_refs`, and which
audience segments those are. This is the **prerequisite** that engages this fragment — it is not decided
here.>

#### A4.2 — Provedor de identidade externa (pré-requisito, não detalhe)

**Provedor**: {{external_identity_provider}}

<the external identity provider is a **prerequisite with its own consequences**, not a configuration
detail: it is a tenant or directory the organization must own, it carries its own cost, and it carries
its own operating burden with an **owning role**. State all three, and state the role that operates it,
with the mechanism it operates through. Where no role is designated to operate it, or the funding is
absent, that is an open architecture item — `structural: true` where it decides whether the audience can be
served at all. An operating role with nobody named against it yet is not that: it is complete.>

#### A4.3 — Superfície e modelo de construção

**Superfície primária**: {{primary_surface}} — <the recorded value and its build model (low-code or
code-first).>

<what the build model forfeits relative to the alternative: what becomes harder to change, what tooling
and skills it requires, and what portability it gives up. Cite the surface unit for each forfeit; state
no limit of your own.>

#### A4.4 — Autorização do utilizador humano (forma)

<the deny-by-default authorization form for an external audience: the permission model over records
crossed with the audience's web-facing roles. State the default posture explicitly — nothing is reachable
until a permission grants it — and which grants are required for each audience segment. The control's
existence and reach come from the security unit (core A7); this section carries only the form.>

#### A4.5 — Exposição pública e auto-registo

<!-- CONDITIONAL — engaged only where anonymous or self-registering access is in scope. Otherwise
     `not applicable — sem exposição anónima em âmbito`. -->

<what is reachable without authentication, what the default posture is, and what self-registration
admits. Every anonymous path is stated as a deliberate decision with an id, never as an inherited
default.>

#### A4.6 — Cache e semântica de frescura

<the freshness semantics the surface presents. **A write made outside the site is never guaranteed to be
immediately visible on it** — state what the design does about that: which reads tolerate staleness,
which do not, and what the user is shown while the two disagree. This is an architectural commitment, not
an implementation detail.>

#### A4.7 — Base de conformidade de acessibilidade

<the accessibility conformance basis: the standard being conformed to, who attests it, and when. An
unattested claim is an open architecture item with an owner — never an assumption promoted to fact.>

#### A4.8 — Localização

<!-- CONDITIONAL. Otherwise `not applicable — <reason>`. -->

<the languages and locales in scope, what is translated (interface, content, data), and who owns each.>

#### A4.9 — Leitura offline

<!-- CONDITIONAL. Otherwise `not applicable — <reason>`. -->

<what, if anything, is readable without connectivity, and what that forfeits.>
