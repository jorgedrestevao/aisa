# Governance and environments — what each lever prevents, and what it obliges

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *What tenant or estate preconditions does this control level require, who owns them, and are they funded?*
- *What does this control cost the whole environment population, not just this app's users?*
- *What does this lever mechanically prevent — and does it prevent, or only detect?*
- *Can this control reach what already exists, or only what happens next?*

This file states **what Power Platform's governance levers mechanically prevent, what each one requires of
the tenant before a project can rely on it, and what it obliges across an environment's entire user
population**. It does not decide which option wins — that belongs to the decision model
(`decision-tree.md` S4–S6).

---

## 1. What this is for · `decision-grade`

Governance in Power Platform is not a policy document. It is a set of platform configurations that
mechanically constrain what makers can do — and almost all of them are configured **above the project**,
at the tenant, the environment or the environment group.

**Binding framing: organisational governance is not platform disqualification.** A governance finding is
one of four things, and none of them is an exit:

| Finding shape | What it means | What the engagement produces |
|---|---|---|
| **Precondition** | Something that must already be true in the tenant for the design to rely on a control | The precondition named, the role accountable for it, and whether it exists today |
| **Obligation** | Something the platform does not do, so the organisation must | A deliverable, the role accountable for it, and a cadence |
| **Economic consequence** | An entitlement obligation across a population, not across an app | An affected-population count handed to `economics/licensing-and-cost-drivers.md` |
| **Operating requirement** | A recurring activity (attestation, review, remediation campaign) | A staffed operating step, dated |

A tenant at an early governance maturity cannot be *assumed* to have data policies, environment routing,
promotion paths or an ownership process. That absence does not make the platform wrong; it makes those
things **project deliverables with owners and funding questions**. Where a precondition is missing and
unfunded, the honest output is a precondition and a cost decision escalated to whoever owns it — never a
verdict about the platform.

## 2. When it becomes material · `decision-grade`

- A control must be **enforced** rather than advised — because someone will be asked to evidence it.
- The estate has more than a handful of environments, so per-environment configuration will drift.
- Makers **outside** the delivery team will build, or already have.
- Residency, regional or business-unit separation is a requirement.
- There is an **external** (non-employee) audience.
- Ownership, support or retirement responsibility for the artefact is unclear.
- The existing estate is unknown — nobody can state the count of environments, apps, automations, owners
  and connectors.
- The design's critical path runs through a connector whose permissibility has not been checked in the
  **target** environment.

## 3. Tenant/estate preconditions vs solution design · `decision-grade`

This distinction is why most governance findings are **not design choices**. Almost every enforceable
lever is configured outside the solution, by someone who is not on the project.

| Control | Configured at | In the project's gift? |
|---|---|---|
| Environment topology and creation restriction | Tenant settings | No — tenant-owned |
| Managed-environment activation | Per environment / per group | No — tenant- or platform-team-owned, with a population-wide entitlement consequence |
| Environment groups and their rules | Tenant | No |
| Tenant-level data policies | Tenant | No |
| Environment-level data policies | Per environment | Sometimes — as a requested exception |
| Environment routing, licence auto-claim, weekly digest, Lockbox | Tenant settings | No |
| Sharing limits, solution-checker enforcement, backup retention | Per environment / locked by group rule | No, where a group rule is published |
| Which environment the solution lands in | Design + platform team | Shared |
| Which connectors the design needs, and its own sharing posture | Design | Yes, within the limits above |
| Solution and publisher discipline | Design | Yes |

Two mechanical properties of this boundary decide sequencing:

- **Preventive levers are forward-only.** Restricting environment creation does not reach environments that
  already exist — their creators keep managing them. Sharing limits apply only to future sharing; existing
  shares keep working. So governance must be established **before** adoption scales; in a tenant that
  already has sprawl, remediation is a discovery-and-migration exercise, not a setting.
- **The promotion path must exist before makers are enabled.** Otherwise successful maker-built tools become
  ungoverned production dependencies, and the platform's response to abandonment is detection, not repair.

## 4. The eight levers, and what each mechanically prevents · `decision-grade`

Read the middle column, not the lever's name. A control's value is what it makes impossible.

| # | Lever | Configured at | What it mechanically prevents | What it obliges |
|---|---|---|---|---|
| 1 | **Environment topology** | Tenant creation control + per environment | Wrong data in the wrong place; blast radius across workloads; residency violations | An entitlement and administration cost per environment; ALM overhead; a taxonomy |
| 2 | **Managed environments** | Per environment / per group | **Nothing on its own — it unlocks the other controls** | An entitling licence for *every active user* of that environment (§8) |
| 3 | **Environment groups + rules** | Tenant | Configuration drift; local admin override of ruled settings | No per-environment exceptions; local admin autonomy removed in the ruled dimensions |
| 4 | **Data policies** | Tenant + environment | Connector combinations; specific connectors, actions and endpoints | Maker friction; connector-space fragmentation if over-applied; an exception process |
| 5 | **Sharing limits and the org-wide group** | Per environment / group | Oversharing **going forward** | Existing shares untouched; a separate remediation campaign |
| 6 | **Solution-checker enforcement + block unmanaged customizations** | Per environment / group | Non-compliant imports; ad-hoc production edits | A documented break-list of first-party features (`alm/release-and-lifecycle.md`) |
| 7 | **Ownership, inventory and reactive action** | Tenant (inventory / recommendations) | **Nothing preventively — it detects** | A periodic review cadence; full detail only for managed environments |
| 8 | **External-estate governance** | Azure / enterprise platform / on-premises ownership domain | Ungoverned APIs, brokers, workers or gateways becoming shadow infrastructure | A second RBAC, policy, CI/CD, monitoring and cost model, with its own operating role and diagnostic path |

## 5. Preventive vs detective, and what works retroactively · `decision-grade`

- **Levers 1–6 are preventive**, and most of them require a managed environment (§8).
- **Lever 7 is detective and inherently lagging.** Recommendations refresh on a documented periodic cadence
  measured in days rather than in real time, full detail covers managed environments only, and there is a
  documented warm-up delay after enabling a managed environment before the detail appears. The vendor's own
  comparison is explicit that the in-product preventive controls enforce a sharing limit *before* it is
  passed, whereas a reactive model can only react after — possibly leaving non-compliant assets in place.
- **Lever 8 is a boundary condition**, not a control (§13).

Two consequences:

1. **A governance model resting on detection alone is a reporting exercise.** Detection latency and scope set
   the floor for any control described as "monitored, not prevented" — including ownerless artefacts,
   oversharing, inactive resources and expiring site certificates or authentication keys.
2. **Detection is the only lever that works retroactively.** Preventive levers do not reach the existing
   estate. So an engagement in a tenant with an unknown estate needs a *measurement* step (count of
   environments, apps, automations, owners, connectors) before it can state which controls are real.

## 6. The environment is five boundaries at once · `decision-grade`

The environment is simultaneously the **security boundary**, the **governance unit**, the **data-policy
scope**, the **residency unit** and the **licence unit**. That single fact makes environment topology the
most consequential governance decision, and it is why cross-environment data access is not a platform
feature: separation between development data and production data is *environment* separation, never policy.

Environment types carry governance-relevant, non-obvious behaviour:

- **Default environment.** Every employee has access. It cannot be deleted. A security group cannot be
  applied. It carries no backup guarantee and cannot be manually backed up. Every licensed user holds maker
  rights. A system backup cannot be restored over it — the documented restore target is a developer
  environment. And it fills up **by construction**: a custom list form creates its app there, and automations
  created from that surface always use it. So any tenant with the productivity suite has a de facto
  ungoverned application estate until the documented controls are applied. Securing it is a workstream with
  user-visible impact (it breaks existing apps), which is why it is sequenced with communication, not flipped.
- **Developer environments.** Cheap, capped per maker, not counted against tenant capacity, no security group,
  and **automatically turned off and removed after a documented period of disuse** if the owner does not
  respond — so they are not a place for anything that must survive. Routing-created developer environments
  are managed by default, and the maker, though environment admin, cannot change settings that a group rule
  governs.
- **Trial environments.** One per user, removed after a short documented period, and **not backed up at all**.
- **Sandbox environments.** Support copy and reset. Creation can be restricted to admins, but **converting a
  production environment to sandbox cannot be blocked** — so "production environments are protected" is not
  enforceable by creation controls alone.
- **Team-scoped Dataverse environments.** Created automatically when an app is created in the collaboration
  surface. The security model follows team membership; **no security-role customisation or assignment is
  available**; no security group applies; location is the tenant home. Growth beyond their limits is a
  **one-way** upgrade. Anything created this way starts outside the environment strategy and cannot be
  re-secured in place — the governance response is detection plus a migration path.

**Guest and external users.** Guest access to Dataverse is restricted by default on new environments and is a
per-environment toggle. It does not override tenant-level guest policy, and it does not restrict guests from
apps in the environment that do not use Dataverse — a documented residual. The org-wide "Everyone" group
contains every user who has ever signed in, **including guests**, and its membership can be neither viewed
nor edited.

**Backup retention is a governance rule with a type condition.** The default retention applies to production
and non-production environments alike; extension is available **only for production managed environments**,
and where a group rule sets retention the individual environment cannot override it. A retention requirement
beyond the extended ceiling cannot be met by platform backup at all — it becomes a data-level archival
requirement.

> Documented reading · read 2026-09-04 · re-verify: VS-07 (Options and renewal)
> Default retention seven days for production and non-production environments; extension up to 28 days for
> production **managed** environments only; trial environments not backed up.

## 7. Residency is fixed at environment creation · `decision-grade`

The region is chosen at creation and binds Dataverse, apps, connections and gateways. It is **irreversible**:
the remedy is a new environment plus a migration.

- Macro-region data-boundary scope requires **both** the tenant and *all* environments in the correct macro
  region **and** a matching billing address — the vendor's wording is that meeting only one condition does
  not place the environments inside the boundary. A single out-of-region environment (a forgotten sandbox)
  takes the estate out of scope.
- Without the advanced-residency add-on across the productivity seats, the datacentre *within* the macro
  region is vendor-chosen, and placement can shift — which affects network alignment, private-networking
  design and latency expectations.
- Some things replicate globally regardless of region: table and column **names**, app names and descriptions,
  and external site names/URLs. Content stays in geo; identifiers do not. So a naming convention that keeps
  sensitive semantics out of schema and app names is a residency control.
- Restore and customer-managed-key operations are same-region.
- Tax rules restrict creating a database in some geographies where the tenant is elsewhere.

**Consequence:** residency resolves to an *environment-creation policy* covering development and test as
well as production, plus an owner who enforces it — not to a solution setting.

## 8. Managed Environments and the licence chain they create · `decision-grade`

**This file is the sole home for Managed Environments.** Every other unit that touches them refers here.

A managed environment prevents nothing by itself. It is the **delivery vehicle** for nearly every enforceable
control, and the documented capability set it gates includes: environment groups; sharing limits; usage
insights; data policies (including desktop-flow data policies); deployment pipelines; maker welcome content;
solution-checker enforcement; IP firewall; IP-address cookie binding; customer-managed key; Lockbox; extended
backup retention; export of telemetry to Application Insights; catalog administration; default-environment
routing; virtual-network support; conditional access on individual apps; app access control; and masking
rules.

**The chain, in the order it actually runs:**

```text
a control requirement        →  the control is managed-environment-gated
                             →  the environment must be enabled as managed
                             →  every ACTIVE USER of that environment needs an entitling licence
                             →  the affected population is the ENVIRONMENT's population,
                                not the application's users
```

- **Entitlement shape.** Managed environments are included as an entitlement with the standalone Power Apps,
  Power Automate, Copilot Studio, Power Pages and Dynamics 365 licence families; qualifying consumption meters
  also count. Trial licences count but expire. **The Developer Plan does not entitle managed environments when
  users run their assets** — which closes the obvious workaround.
- **Scope, and the part teams get wrong.** Only environments actually enabled as managed are in scope — but
  within one, *every user who runs an app is in scope, including users who run standard (non-premium) apps*.
  A "standard-connectors-only" design does not escape the obligation.
- **Diagnostics exist, with a blind spot.** The admin centre publishes a report of users requiring licences in
  managed environments. It lists only users who actually launched an app in a managed environment in the
  period, so it under-reports the population that would be affected by enforcement.
- **Licence auto-claim.** Where auto-claim is configured, a user without a standalone licence who launches an
  app in a managed environment is automatically assigned one. The vendor recommends it precisely because it
  removes friction and consumes only for active users. Mechanically, it **converts an access decision into a
  consumption decision taken by an end user's click** — so it must be a deliberate choice, paired with sharing
  limits (which then act as a consumption control as well as a security control) and with a consumption view.
  Tenant capacity must be sufficient.

**The dated commitments.** Two are live and belong in an option's revision conditions, not in a static rule.

> Documented reading · read 2026-09-04 · re-verify: TW-V3 (dated commitment — confirm before costing)
> Managed-environment licence enforcement: from **February 2027**, users without an appropriate licence are
> blocked from opening apps in a managed environment. Administrator notification and staged in-app
> notification precede it. Row `TW-V3` owns this subject; on firing, re-price the whole environment
> population, not the app's own users.

> Documented reading · read 2026-09-04 · re-verify: TW-V1 (dated commitment — verify the outcome)
> Automatic conversion of deployment-pipeline **target** environments to managed environments began
> **February 2026**. Row `TW-V1` owns this subject; whether it completed as announced, and what it did to
> tenants that had not planned for the entitlement impact, is an open question in the baseline. Confirm the
> current default with the platform-owning team before costing an in-product ALM path
> (`alm/release-and-lifecycle.md`).

**The genuine tension, stated rather than absorbed.** The vendor recommends enabling managed environments
broadly — including on the default environment, which in most tenants is used by everyone — while also
documenting that every active user of a managed environment needs an entitling licence, enforced from the
dated milestone above. For a tenant whose default environment serves all employees these two recommendations
are in direct economic tension. This is not a documentation error; it is a real trade-off whose resolution is
organisation-specific and must be surfaced as a funded decision, with the role that can take it. The economic modelling
itself belongs to `economics/licensing-and-cost-drivers.md`.

## 9. Environment groups — the drift lever, and its five hard edges · `decision-grade`

Groups are the mechanism that makes governance scale, and they make local admin autonomy impossible in the
dimensions they rule.

- **Managed environments only.** A group cannot contain a non-managed environment.
- **One group per environment.** No overlap, no nesting. Groups may span regions and types.
- **No per-environment exceptions.** Therefore the group taxonomy must be designed around the *exception*
  cases, not the common ones.
- **A published rule locks the setting read-only** in each member environment; a local system administrator
  cannot override it. Removing an environment from the group leaves the last applied configuration in place
  but unlocked.
- **Joining overrides pre-existing environment-level values** in the ruled dimensions — sharing limits, maker
  welcome content, solution-checker enforcement, usage insights, backup retention and generative-AI settings
  are reset to the group's values on join. This is a known limitation, not a bug, and it is a live source of
  "who changed my environment" incidents.

Rules available at group level include sharing controls, usage insights, maker welcome content,
solution-checker enforcement, backup retention, AI-generated descriptions, and — at group scope — advanced
connector policies, IP firewall and cookie binding.

**Environment routing** creates or redirects makers into personal developer environments, optionally directly
inside a designated group, and those environments are managed by default. Routing is what makes guardrailed
maker enablement real. Two separate actions are still required: restricting *manual* developer-environment
creation is a distinct tenant setting (routing does not do it), and a security group in the routing policy
limits who gets an environment created. Changing the routing group later does **not** move existing developer
environments.

## 10. Data policies at estate level · `decision-grade`

- **The starting state is permissive.** By default no data policies exist in the tenant, and newly added
  connectors land in the default group over time — so the permissive surface grows on its own.
- **Scoping and precedence.** Policies are scoped at environment and tenant level. An environment policy
  **cannot override** a tenant policy. Where several policies apply to one environment, the **most
  restrictive** result applies to the combination, and blocked always wins. There is no user-level scope and
  no strict hierarchy between tenant and environment policies.
- **They are connector-aware, not connection-aware.** A policy shapes *what a maker can build*, not *which
  instance a connection reaches*. It does not control the connections made using a connector.
- **Policy count is an architectural variable.** Multiple policies fragment the connector space
  combinatorially in the number of policies (2ⁿ groups, some of them empty), producing maker-visible failures
  that are hard to diagnose. The documented strategy is a tenant baseline plus a **minimal** number of
  environment policies used only to categorise custom connectors or as genuine exceptions. A project that
  requests "its own policy" adds a dimension of fragmentation to every environment it touches.
- **Connector governance is mid-migration, so any rule must name its enforcing system.** The classic
  classification model has a documented set of connectors that cannot be blocked at all. The
  advanced/allowlist model inverts to default-deny for certified connectors and can block otherwise
  non-blockable ones on a managed environment — but it does **not yet cover custom or HTTP connectors**, and
  never covers virtual connectors. Endpoint filtering is preview, covers few connectors, and — the most
  consequential gap in this plane — **does not apply to values created dynamically at runtime**. So the
  custom-connector and bespoke-API path stays governed by the older model plus target-side control, and no
  control should have endpoint filtering as its only enforcement.
- **Retrofitting a policy is an availability event.** A violation puts the app or automation into a suspended
  or quarantined state, and full enforcement is not immediate — so a governance action can present as an
  integration outage arriving later, with no obvious cause.
- **A policy check is valid on its date only** (`VC-03`). Verify the required connector set against the
  **target** environment's policy before committing the design, and name who approves an exception — the
  approver for a line-of-business connector is often the owner of that system, not the platform team.

## 11. Sharing constraints and the external audience · `decision-grade`

- **Sharing limits are forward-only.** Applying a limit to an environment whose resources are already shared
  more widely leaves those shares working. Non-compliant resources permit *only* unsharing until they comply,
  and enforcement has a documented latency. Remediating pre-existing oversharing is therefore a separate
  campaign with its own owner, and makers must be told before the limit lands.
- The rules cover canvas apps, solution-aware cloud flows and agents. In team-scoped environments, publishing
  to the team is **outside** the sharing rules.
- **The org-wide group is not a control surface.** It includes guests and every user who has ever signed in,
  and its membership cannot be viewed or edited — so "shared with everyone" is an unbounded, unauditable
  audience.
- **An external audience adds its own governance surface.** Whether makers may make non-production external
  sites public is a tenant-level control; a site that was already public before the restriction **stays
  public**. Who may change site visibility is itself a tenant setting, with a designated security group as the
  alternative path. And external-facing sites carry dated operational obligations — web-application-firewall
  posture, certificate and authentication-key expiry — surfaced as recommendations, managed environments only.
  An accountable role for the site's lifecycle is a requirement, not a nicety. A gap in the organisation's
  global inventory is not this project's work: what the design owes is the lifecycle of what it builds.

## 12. Solution-checker enforcement — a release gate configured by governance · `decision-grade`

Enforcement modes are none, warn and block, set per environment or locked by a group rule. In block mode an
import carrying highly-critical findings is cancelled **before** the import, so the target is unchanged. Only
**critical**-severity rules block; rule exclusions are supported; notification goes to platform and
application administrators plus digest recipients; and enforcement is unavailable while the environment is in
administration mode.

Three properties decide how it is used:

1. **It is static analysis, not a test.** The vendor states plainly that using it does not guarantee a
   successful import, because the static checks do not know the configured state of the destination
   environment. A green result is not release evidence.
2. **It analyses exportable unmanaged solutions.** Managed and third-party managed solutions are not analysed.
3. **The project inherits it and cannot weaken it.** Because it is an environment or group setting rather than
   a pipeline setting, a delivery team cannot opt out inside its own pipeline — and an environment group can
   impose it centrally with no per-environment exception.

Its companion production-integrity control, **block unmanaged customizations**, is what makes read-only
production support possible; its mechanics and its documented break-list live in
`alm/release-and-lifecycle.md`.

## 13. The external-estate boundary · `decision-grade`

**Power Platform governance does not govern the external estate.** Where a design reaches into Azure, an
enterprise integration platform, or an on-premises ownership domain, the responsibilities that Power Platform
levers cover inside the platform — inventory, RBAC and privileged access, policy baseline, CI/CD, monitoring
and alerting, backup and recovery position, cost ownership, incident route — exist there too and are **not**
covered by data policies or environment groups.

The mechanical consequence: those responsibilities need a **named owning team** before the external component
is production-ready. Where no team accepts them, the component has no operator — which is a resourcing and
ownership fact to record, with the delivery-side form of the same fact (two coordinated supply chains) in
`alm/release-and-lifecycle.md`.

A related governance question comes before any product question: where the organisation **already** has an
API, event or integration platform with a published contract and an owning team, a project-local equivalent
duplicates governance and splits ownership. Ask whether the existing capability meets the required protocol,
security, reliability, latency and ownership model. Reuse is not automatic, and neither is replacement — this
file records the question and the ownership consequence, not the answer.

## 14. Control ownership, detection and retirement · `decision-grade`

- **Ownership is not enforced by the platform.** Ownerless artefacts are detected periodically and only in
  managed environments, and — the decisive detail — **reassigning an owner does not automatically grant the
  new owner permissions to the environment or the data sources**. An ownership *record* is not an ownership
  *capability*. A support model must state who holds the connections, who holds the environment role, and who
  is accountable; the platform only flags absence. When a maker leaves, their apps and automations are in
  effect ownerless.
- **Inventory is not a service catalogue.** The admin centre supplies inventory, usage, monitoring and
  recommendation surfaces plus APIs and admin connectors. Ownership, criticality, support tier and data
  classification are attributes the organisation must add. Naming and grouping conventions are organisational
  deliverables.
- **Production support without production edit rights has a documented answer — and it depends on an ALM
  setting.** With block unmanaged customizations enabled, a responsible user can be a co-owner on a managed
  automation in test or production: they can review run history, understand errors, turn it on and off, run it
  for testing, change environment variables and assign ownership, while the managed component itself stays
  effectively read-only to them.
- **Retirement is a process with platform support, not a platform feature.** Available mechanisms: quarantine
  (a maker can still edit, users cannot run, and only an admin can change the state), orphan and inactivity
  detection, automatic removal of unused developer environments, and a documented multi-step move-out
  procedure (solution with dependencies → export/import → security roles → configuration and data migration →
  test → notify → remove access → delete, without deleting shared assets). The data-migration step is usually
  the real work, and restoring a backup can bring back artefacts that a clean-up removed.
- **Evidence for audit is a cadence, not a feature.** Detection is periodic; recommendation history and audit
  logs are the artefacts. The reporting cadence and evidence-retention window are agreed with the auditor,
  not assumed.
- **Deprecation of prior governance tooling — recorded as a deprecation, not a recommendation.** The
  community governance starter kit is **no longer actively maintained**: issues are not reviewed or addressed
  and no new capability will be added, and its core scenarios have moved into the product (inventory, usage,
  monitoring, recommendations, plus CLI/APIs and admin connectors). Existing deployments remain available and
  should be treated as technical debt with a migration path. The consequence that matters for reading any
  advice: a large body of circulating governance guidance — including some still-published vendor pages —
  presumes that kit, and is historical. Functional parity between the kit and the in-product replacements is
  **not** established in the baseline. Building new governance capability on the kit is not a recommendation
  this file makes.

## 15. Failure modes · `decision-grade`

Governance failures come in **matched pairs**. Encoding only one half of a pair systematically pushes
engagements into the other, so both directions are carried here.

> **No environment strategy.** Adoption lands in the default environment, where no security group applies,
> backups are not guaranteed and every licensed user is a maker — and list-form and collaboration-surface
> artefacts land there automatically. Consequence: an ungoverned production estate that nobody chose.

> **Uncontrolled environment proliferation.** *(The mirror.)* Creation left open means environments outside
> every group, policy and control — and the restriction does not reach the ones already created.
> Consequence: an estate that cannot be described, policed or inventoried, plus per-environment cost axes
> nobody owns.

> **Under-governance of connectors.** The default state is no policy at all, and new connectors accrue to the
> default group over time. Consequence: the permissive surface grows without anyone deciding it should.

> **A policy per project.** *(The mirror.)* Policy count fragments the connector space combinatorially, with
> empty groups and maker-visible failures that are hard to diagnose, and the composite behaviour is emergent
> rather than designed. Consequence: a control layer that is unmaintainable in exactly the estates that need
> it most.

> **Excessive centralisation.** Group rules remove local administrative control in the ruled dimensions and
> support **no exceptions**, while the vendor's own delivery-model guidance offers centralised, decentralised
> and hybrid. Over-centralising drives shadow adoption into the collaboration and list surfaces — both of
> which land *outside* the strategy by construction. Consequence: over-governance manufactures the ungoverned
> estate it was meant to prevent.

> **Excessive decentralisation.** *(The mirror.)* Every business unit sets its own policies and topology.
> Consequence: the fragmentation above, plus an estate whose size is routinely larger than leadership
> believes.

> **Enterprise controls imposed on a trivial workload.** Managed environments oblige an entitling licence for
> every active user of the environment, and the whole operational feature set sits behind that gate.
> Consequence: a population-wide entitlement funded for no risk reduction — and a lead time that pushes
> makers off-platform. Classify criticality first; let the class select the obligations.

> **Ownership recorded but not capable.** An owner is assigned and the artefact still cannot be operated,
> because reassignment grants no environment or data-source permission. Consequence: an incident with a named
> owner who cannot act.

> **Detection mistaken for assurance.** Recommendation pages and posture scores refresh periodically, cover
> managed environments only, and some are preview. Consequence: an assurance claim built on a backlog
> generator. Assurance artefacts are built from configuration state plus audit, never from a score.

> **Auto-claim without sharing limits.** Auto-claim grants an entitlement on first app launch; permissive
> sharing then turns access into a self-service consumption event. Consequence: an unplanned population
> increase, discovered on a report rather than at a decision.

## 16. Consequences elsewhere · `decision-grade`

- **→ ALM and release.** The dev/test/prod topology *is* the environment strategy — a governance decision to
  consolidate environments directly removes delivery capability, and one to add them adds administration and
  entitlement obligations. The release gates (solution-checker enforcement, block unmanaged customizations)
  are governance settings, not pipeline settings, so a project inherits them. In-product pipelines require
  their target environments to be managed, which makes adopting in-product ALM a **tenant entitlement
  decision** (§8, `TW-V1`). See `alm/release-and-lifecycle.md`.
- **→ operations and support.** Detection cadence caps mean time to detect for anything that is monitored
  rather than prevented. Extended backup retention, telemetry export, cross-region recovery and the
  monitoring recommendation surfaces are managed-environment-gated, so **operational maturity is bought, not
  configured**. Ownership and support rota, retirement, and the reporting cadence are governance-owned
  operating requirements. See `operations/operability-and-support.md`.
- **→ economics.** *The licence chain in §8 is the largest cross-domain fact in this corpus.* A control
  requirement resolves to a managed environment, which resolves to an entitling licence for every active user
  of that environment — including users of standard apps — with a dated enforcement milestone (`TW-V3`).
  Auto-claim makes consumption a user-initiated event. Environment count is a cost driver on several
  independent axes. All monetary modelling, unit and meter treatment belongs to
  `economics/licensing-and-cost-drivers.md`; this file supplies the *affected population* and the
  *entitlement shape*.
- **→ security.** Governance is the **delivery mechanism** for the security controls: IP firewall, cookie
  binding, customer-managed key, Lockbox, virtual-network support, app access control, masking rules and
  sharing limits are all managed-environment features. A security requirement therefore arrives as a
  governance change request with a population-wide entitlement consequence — and conversely, a tenant already
  running managed environments absorbs new security requirements far more cheaply. Governance also decides
  the blast radius that security must contain, and can *create* an exposure (auto-claim plus permissive
  sharing). See `security/security-controls.md`.
- **→ data.** Residency, retention, customer-managed keys, vendor-access approval, masking and private
  networking are all environment-level and mostly managed-environment-gated, and residency is fixed at
  creation. **Data requirements therefore decide the licensing model and the environment topology**, not only
  the store. Compensation, replay and restore need a named business owner: who may replay or compensate, who
  approves manual conflict resolution, and who signs off reconciliation after a restore. See
  `data/store-boundaries.md`.
- **→ integration and automation.** Connector permissibility is a per-environment, per-date fact; the
  custom-connector and HTTP gap in the allowlist model is why target-side control matters; and the
  external-estate boundary (§13) means an integration component needs an owning team before it is
  production-ready. See `integration/integration-mechanisms.md` and `automation/automation-mechanisms.md`.

## 17. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Control propagation and enforcement latency — policy, isolation, sharing limits and group rules do not bind instantly | `VS-21` |
| Managed-environment licence enforcement milestone and any de-scoping guidance | `TW-V3` |
| Automatic conversion of pipeline target environments to managed — outcome and current default | `TW-V1` |
| Backup retention windows by environment class | `VS-07` |
| Connector and service permissibility posture, per environment, on its date | `VC-03` |
| Entitlement fit of the required control set for the affected population | `VC-05` |
| Preview / general-availability state of any lever the design leans on | `VC-10` |
| Audit and diagnostic retention windows underpinning an evidence obligation | `VS-05`, `VS-19` |

**Not established in the baseline** — do not fill from general knowledge:

- **Functional parity** between the deprecated community governance kit and the in-product replacements. The
  scenario mapping is stated; parity is not.
- Whether environment-group rules will gain **per-environment exceptions**, or a group hierarchy. Neither
  exists today; the vendor's own wording is "not yet".
- Whether **group membership automation** through the admin connector has shipped; moving environments between
  groups is documented as a manual action.
- The practical impact of the dated licence enforcement on tenants that enabled managed environments broadly
  for governance reasons — **no de-scoping guidance was seen**.
- The current **allowlist-model rollout state**, and whether custom-connector or HTTP rule types shipped.
- The **recommendation catalogue** itself — it grows, and one category changed within the research window.
- Whether tenant-level analytics (a prerequisite for the posture score) carries any residency or retention
  implication.
- Governance of agent surfaces beyond data policies, virtual connectors and sharing limits (agent
  authentication and channel controls are preview and were not researched).
- Whether inventory and API coverage includes external sites and desktop automations at the same fidelity as
  apps and cloud automations.
- **Any figure for the periodic detection cadence, the post-enablement warm-up, the policy-enforcement lag,
  the developer-environment disuse window or the per-maker developer-environment cap.** The *shapes* are
  documented and carried above; no volatility row owns those numbers, so they are read at the decision date
  and recorded on the engagement's own row.

## 18. What not to infer · `decision-grade`

- **A control's absence in the tenant is not a verdict.** "This tenant has no data policies and no promotion
  path" is domain knowledge. "Therefore the platform is inappropriate" is a selection verdict and belongs to
  `decision-tree.md`. The governance output is a precondition, an owner and a funding question.
- **Organisational governance immaturity is not platform disqualification.** Most findings here are
  preconditions, obligations, economic consequences or operating requirements. Treat an unfunded precondition
  as a cost decision to escalate, never as an exit.
- **A documented boundary here is not evidence that another option class performs better.** The baseline holds
  no like-for-like governance comparison against SaaS, custom/pro-code, incumbent platforms or other low-code
  estates; where such a comparison is material, the decision model's comparator semantics stand.
- **Do not read the vendor's reference topology as a verdict.** A reference environment topology is a position
  to be measured against; deviations are recorded as accepted risks with owners, not silently adopted and not
  treated as failure.
- **Do not treat a managed environment as a security control.** It gates controls; it enforces nothing by
  itself.
- **Do not present partial controls as containment.** Cross-tenant isolation covers only some connector
  families and has a documented enforcement hole; endpoint filtering does not survive dynamic values; the
  environment security group does not constrain platform administrators or service principals. State the
  vector each control reduces.
- **Do not quote sprawl statistics.** The direction is corroborated by the vendor's own product response; the
  figures come from material with no published methodology. Measure this estate instead.
- **Do not recommend deprecated tooling.** The community governance kit is recorded above as a deprecation and
  as existing technical debt — nothing more.
- Naming conventions for environments, groups and solutions, traceability stamping, go-live and post-go-live
  checklists are **delivery practice**, not platform governance — `craft/delivery-conventions.md`, which is
  never an Options pull target.
