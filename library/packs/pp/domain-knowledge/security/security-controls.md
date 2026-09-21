# Security controls — which plane enforces what

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Is this mandated control available at all — and if it is, on which plane is it enforced, and over what
  population?*
- *Does this design change who the backend sees, and whose authorization the backend therefore enforces?*
- *Which of these security choices cannot be reversed after provisioning?*
- *Which control is only partially satisfiable, and what must the residual-risk statement say?*

This file states **which enforcement plane can actually hold a given security requirement, what each plane
does not cover, and which of those choices are irreversible**. It does not decide which option wins —
that belongs to the decision model (`decision-tree.md` S4–S6). A control's absence stated here is a
capability fact, never a verdict.

---

## 1. What this is for · `decision-grade`

Power Platform security is not one model. It is **five planes**, enforced by different services,
configured by different roles, and failing independently of one another. Almost every security
disappointment in delivery comes from a requirement having been placed on the wrong plane — usually a
plane too high, where it looks satisfied and is not.

So the unit of analysis here is not "the control" but **requirement → plane → grain → what still gets
through**. A security requirement is only answered when all three are named.

## 2. When it becomes material · `decision-grade`

- A population must be **unable to see** data that another population sees — at table, row or column grain.
- Confidentiality is claimed **against administrators**, or against the people who operate the automation.
- An **external, guest or anonymous** audience is in scope.
- A **network posture** is mandated: corporate-network-only access, or no public egress to a back end.
- **Key custody** is mandated, or vendor engineer access must be approved per incident.
- A regulator or auditor requires **who-saw-what**, with a retention period.
- Automation must **survive the departure** of the person who built it.
- **Separation of duties** between who builds and who releases is mandated.
- A **residency** boundary applies to the data.
- The mandated control set is written as a checklist someone expects to tick — that is the moment the
  partial controls (§10) and the residual-risk obligation (§13) become load-bearing.

## 3. The five enforcement planes · `decision-grade`

Read a row as: *who enforces · at what grain · what fails independently of the other planes.*

| # | Plane | Enforced by | Grain | Fails independently as |
|---:|---|---|---|---|
| 1 | **Tenant / identity** | Microsoft Entra ID — authentication, Conditional Access, continuous access evaluation, Privileged Identity Management, B2B guest | User · group · device · location · session | A Conditional Access policy that misses a first-party application id (Power Automate's service is **not** inside the Office 365 application target); standing administrative access with no just-in-time gate |
| 2 | **Environment** | Power Platform — environment security group, environment roles, IP firewall, cookie binding, guest restriction, VNet support, customer-managed key, Customer Lockbox | The environment | Everything in one environment, so blast radius equals the estate; platform administrators and **application users (service principals)** are outside the security group by design |
| 3 | **Data store** | The store itself — Dataverse roles/business units/teams/sharing/column security/masking/audit; SharePoint permissions; Azure SQL row-level security and column grants | Table · row · column (per store — §7) | Additive grants over-issued and not subtractable; per-record sharing used as the access model |
| 4 | **Connection / connector** | Connectors, data policies (classic DLP, advanced connector policies, endpoint filtering) **and the target system's own authorization** | Connector · action · endpoint · connection credential | A connection whose identity is not the user's, so the store's per-user rules resolve to one principal |
| 5 | **Application surface** | Each surface's own model — canvas app sharing, model-driven security roles, Power Pages web roles + table permissions, flow ownership and co-ownership | App · page · record set · flow | Nothing at all against a caller who holds plane-4 credentials (§4) |

**Configuration ownership differs per plane, and that is a delivery fact, not a detail.** Plane 1 belongs
to the identity team; plane 2 to the tenant/environment administrator (and, where environment groups are
used, the group rule **locks** the setting read-only inside the environment); plane 3 to whoever owns the
store's model; plane 4 splits between tenant policy (which an environment policy **cannot override**) and
the connection's owner; plane 5 to the maker. A requirement that crosses planes crosses teams.

## 4. The lowest-plane rule · `decision-grade`

> **A security requirement must be satisfied on the lowest plane that can actually enforce it.**

This is supported synthesis over the vendor's own documented behaviour, not a vendor-endorsed maxim — but
the behaviour it rests on is stated plainly by the vendor, and the negative case is the vendor's own
worked example.

**The worked negative case — the application as the authorization layer.** A canvas app over a SharePoint
list surfaces only the `Name` column. The salary column exists on the list but never appears in the app,
and the design records "salary is restricted". It is not. A user who holds list permissions can author a
new app on the same list, or open the list in the Lists UI, in Excel, or through the Graph API, and read
salary. The vendor's own statement is that *the permissions granted through an app's user interface do not
deny the data-source permissions the user already has*, and that the platform grants no access to data
assets the user did not already have.

Three consequences follow, and they are architectural:

1. **A plane-5 control is not a control.** Hiding a control, screen, navigation item or column changes what
   the app shows; it changes nothing about what the store permits. Any other client bypasses it entirely.
2. **If the store cannot express the requirement, the platform cannot add it.** The choice is then to move
   the data to a store that can express it, or to re-permission the source. There is no third option
   inside the application.
3. **Client-side filtering is not a security boundary either.** A filter applied after retrieval means the
   data was retrieved. Where per-row confidentiality is required, the predicate has to live in the store.

The same rule read upwards: a requirement satisfied at plane 3 is also satisfied for every plane-5 surface
over that store, and for the API, and for the export. That is the reason to push down.

## 5. Trust boundary and data egress · `decision-grade`

**The environment is the platform's security boundary.** It is a logical container and a unit of
governance, and cross-environment data access is not a platform capability: an app can connect only to
data sources deployed in its own environment. The environment is also bound to a geography, and its
resources are reachable only by identities in its tenant. This makes environment count and shape the
primary security lever — and simultaneously the primary governance, residency and cost lever.

**What may cross, and who decides:**

| Crossing | Governed by | Decided by | Documented gap |
|---|---|---|---|
| Which connectors an artifact may use | Data policies (classic DLP / advanced connector policies) | Tenant policy first; an environment policy **cannot override** it; where several apply, the most restrictive wins and blocked always wins | Policies are connector-aware, not connection-aware (§9) |
| Which **endpoint** a supported connector may reach | Endpoint filtering | Tenant / environment administrator | Not enforced for environment variables, custom inputs or any endpoint computed at runtime |
| Whether a connection may reach another tenant | Tenant isolation | Tenant administrator | Covers Entra-authenticated connectors only; a named connector gap; propagation latency measured in hours |
| Whether traffic leaves over the public internet | VNet support (subnet delegation) — **outbound only** | Power Platform administrator **plus** the Azure subscription owner | Internet-bound access from a delegated subnet remains available by default; a NAT gateway is the documented way to control it. The event-publishing path from Dataverse does not support VNet at all, so "private egress" and "outbound platform events" cannot both be met through that mechanism |
| Whether an on-premises source is reachable | On-premises data gateway — an **outbound-only** relay | Whoever installs it (controllable tenant-wide, **not** per environment) | The gateway reaches everything the supplied credential reaches; scoping happens at the source, not on the platform |
| Whether an external component is governed at all | Nothing in Power Platform | The Azure / on-premises owner | API Management, Service Bus, Functions and gateway hosts sit outside platform data policies — a **second enforcement plane** with its own identities, RBAC, network exposure and secret custody, and it needs a designated owning role |

**Consequence for the trust boundary statement.** "It is inside our tenant" is not a boundary claim.
"It is inside environment X, whose membership is Y, whose policies are Z, whose egress is W, and whose
administrators are population V" is.

## 6. Identity propagation · `decision-grade`

Connecting and authenticating to a **data source** is a separate question from authenticating to a
**platform service**. The design decision is: whose identity arrives at the back end.

**The fork, per stream:**

- **Delegated (explicit) identity** — the caller's own credentials reach the source, so the source's
  per-user authorization is still in force, audit at the source shows the actual person, and throughput is
  spread across users. This is the only shape in which store-side row-level security means anything.
- **Service or shared identity** — one principal reaches the source. Authorization is uniform, audit shows
  one actor, and the whole population's traffic lands in one throughput budget.

### 6.1 The shared-identity failure

> When a shared, implicit or service connection is used, **per-user authorization collapses to a single
> principal**. Store-side row-level security does not fail loudly; it resolves to *one set of rights,
> identical for everyone*.

Concretely: with implicit authentication the app runs on the credentials the maker supplied when creating
the connection, for every user, every time. A relational store's row-level predicate written against the
session's user name therefore evaluates once, for the shared principal — the reference architecture's own
wording is that a shareable service identity means all users have the same database access rights. Only an
explicit per-user database identity (or a mediation tier that sets a per-request user context on every
connection) restores the per-user predicate; a canvas app on the store's connector has neither hook.
Two further collapses ride along: **attribution** (the audit record captures the acting identity, so a
shared identity destroys who-did-what) and **throughput** (service protection is per identity, so one
account is one budget regardless of user count).

Secured shared connections narrow one specific hole — end users can no longer take a shared connection and
build their own app on it. They are hygiene, not an authorization model: column names are not hidden, the
action limitation is coarse (write permission implies more than the named action), and apps published
before the platform's secured-connection cutover remain on the old behaviour **until republished** — which
makes it an inventory action, not a design action.

### 6.2 The invisible elevation in automation

> **An automation's default acting identity is the connection owner, not the triggering user.**

A flow runs with the permissions of whoever owns its connections; the user who triggered it may have none
of those rights. Nothing in the run signals this. Three consequences:

- **It is an elevation path.** A trigger reachable by a broad population executes with the owner's rights.
  The authorization decision therefore belongs to the flow's design, not to the trigger's audience.
- **It is a continuity risk.** Ownership tied to a person ends when the person leaves. Automation intended
  to outlive its author needs a service principal or a controlled service identity **designed in** —
  retrofitting means re-authoring connection references, and a connection reference's ownership cannot be
  transferred from the solutions area.
- **Co-ownership is near-total control** — edit, delete, change credentials, add further owners. And
  environment administrators have full access to edit workflows and to see all data that flows through
  them, which puts the administrator population inside the data-access population for any sensitive
  payload.

### 6.3 Two propagation boundaries worth naming early

- **Virtual (read-through) tables cannot carry row-level authorization.** Only organization-owned tables
  are supported, and source-side user validation is not possible. Where backend row-level authorization is
  a compliance requirement, that mechanism is excluded and replication is the documented alternative —
  with its own security work, because security does not travel to a copy.
- **Revocation latency differs by component.** Continuous access evaluation shortens the revocation window
  from the access token's remaining lifetime to near real time, but it is documented for Dataverse only.
  "Access must be revocable immediately" is therefore an identity-plane requirement plus a component
  scope — it is not satisfiable by removing a security role.

## 7. Authorization grain per store · `decision-grade`

The grain a store can enforce is the ceiling on what any surface over it can promise. The stores' own
units carry the mechanics and the scale boundaries — this table exists only to place the grain on a plane.

| Store | Table | Row | Column | Where the detail lives |
|---|---|---|---|---|
| **Dataverse** | Yes — security-role privileges per table | Yes — role depth + business unit + team membership + shares, **summed** | Yes — column-level security, the only store here with column security enforced at the API | `data/dataverse.md` |
| **SharePoint** | List-level, and per-item unique permissions up to a published scale boundary above which inheritance can no longer be broken | Coarse; per-item ACL automation is documented as significant operational overhead and not suitable where strict file-level security is a compliance requirement | **None** | `data/sharepoint.md` |
| **Azure SQL** | Yes — database grants | Yes — row-level security in the database tier, applied on every access path **provided a trustworthy identity arrives** (§6.1) | Yes — column grants / DENY / views | `data/azure-sql.md` |

Two properties of the Dataverse model are decision-shaping and belong here rather than in the store unit:

- **Privileges are cumulative and cannot be subtracted.** A broad organization-level read grant cannot be
  walked back to hide one record. Retrofitting least privilege onto an over-granted environment means
  rebuilding roles, not editing them.
- **Column-level security never applies to the system administrator**, and cannot secure lookup, formula,
  primary-name, system or virtual-table columns; it leaks through calculated and composite columns unless
  every constituent column is secured too. So *"confidential even from administrators"* is not achievable
  in that store: the attribute is modelled into a separately secured table, kept out of the platform, or
  the administrator population is reduced to an auditable, just-in-time set. Administrator count is a
  security **design** variable, because it caps what column security and flow confidentiality can promise.

## 8. Key, certificate and secret custody · `decision-grade`

Only the decision-material parts. Rotation mechanics, vault wiring and per-artifact conventions are
implementation and live in `craft/security-craft.md`.

**Customer-managed keys.** Available as an environment-plane control, gated on a managed environment plus
a higher-tier compliance entitlement for the users of that environment. Three decision-material
properties:

1. **It is scoped, not total.** Connector connection settings, environment settings, and app display
   names, descriptions and connection metadata remain encrypted with the vendor's key. It is an at-rest
   key-custody control for the store's content — not a tenant-wide encryption control.
2. **It rewrites the recovery topology.** The environment is disabled while encryption runs; restore is
   restricted to the same environment or to another encrypted with the same key; a reset deletes the
   environment's encrypted data **including backups**; audit retention configuration is unavailable in a
   customer-key environment.
3. **It creates a tier-0 availability dependency.** The vendor documents the scenario itself: an
   administrator with key control can lock environments, and *locked environments cannot be accessed by
   anyone, including vendor support — they become disabled and data loss can occur*. The key vault becomes
   a single point of failure for the workload, and the documented mitigation is **separation of duties**
   between the key-vault administrator and the platform administrator. Adopting customer-managed keys
   without that separation converts a compliance control into an availability risk.

**Vendor-access approval.** Customer Lockbox exists as an environment-plane control to gate vendor
engineer access to environment data per request. It is a managed-environment capability with documented
exclusions, so it is an explicit per-environment decision — not a tenant default.

**Vault-backed secrets.** Environment variables of type Secret, backed by Azure Key Vault, are the
sanctioned path, and their reach is narrow: consumable by **cloud flows, Copilot Studio agents and custom
connectors only** — the vendor states the secrets are not available to other customizations or generally
through the API. Canvas apps have **no** sanctioned way to hold or read a secret. So "the app must call an
API with a key" is not an app requirement: it becomes a flow, a custom connector, or a Dataverse plug-in —
which changes the topology, the latency profile and the entitlement conversation. Where a secret lands in
an automation action input instead, it becomes readable from run history.

**Credential-free authentication is narrower still.** Platform managed identity is generally available for
**Dataverse plug-ins only**. There is no credential-free path for connectors, flows or apps. A "no stored
credentials anywhere" requirement therefore forces the integration into plug-in code, or out of the
platform to a host that supports managed identity. Where connectors must be used, the mitigation is a
service-principal or certificate connection with the secret in a vault — reduction of exposure, **not**
elimination of the secret.

**Certificates and keys on an external surface are dated obligations with an accountable role and a
rotation mechanism.** Public-facing
site certificates and authentication keys expire; expiry is an operating-model item, not a build item.
Note also that a target endpoint must present a TLS certificate chaining to a well-known root — a custom
root certificate authority cannot be added — which excludes some internal endpoints from private paths.

## 9. Data-policy enforcement semantics · `decision-grade`

**What a data policy enforces:** which **connectors** — and, in the newer allowlist mechanism, which
actions and which static endpoints — an artifact may talk to. It shapes *what a maker can build and run*.

**What a data policy does not enforce:** it does not govern **data**. Policies are connector-aware but not
connection-aware: a policy cannot tell whether a connector is reaching development, test or production.
Environment separation, not the policy, is what keeps production data away from a development artifact.
Policies also cannot be applied per user — only per environment or per tenant.

**Enforcement is asynchronous and it is disruptive.** The chain is: policy saved → cascaded to
environments → resources check periodically → a violating app or flow is put into a suspended or
quarantined state → its connections are disabled → anything running fails at run time. The latency to full
enforcement is documented in **hours, not seconds**, with a worst case measured in a day. Two things follow:
a policy change is a change event that can present as an integration outage, and a control claimed as
"enforced" is enforced only after the propagation window.

**Composition is a real cost.** Where several policies apply to one environment, the most restrictive
combination wins and *blocked* always wins — and each additional policy fragments the connector space
combinatorially. The number of policies is itself an architectural decision; the vendor's own guidance is a
minimal set, tenant-level baseline, environment policies as exceptions. See
`governance/governance-and-environments.md` for who owns which policy and what a group rule locks.

## 10. Controls that are partial by design · `decision-grade`

Not immature — **partial**, in a documented respect. Do not round any of these up to "available".

| Control | Partial in what respect |
|---|---|
| **Data policies (DLP)** | Scoped by the vendor to reducing *unintentional* exposure. Guardrails, not an exfiltration control. Independent (non-vendor, unreproduced) evidence describes deliberate cross-environment bypass through a ubiquitous connector — a signal to validate, not authority. Also: the default tenant state is **no policy at all** |
| **Advanced connector policies** | Default-deny allowlist, but **certified connectors only** — custom and HTTP connectors, the usual route to a bespoke back end, are not covered and stay on the older mechanism; virtual connectors are stated as never in scope. Design-time enforcement rolls out per maker portal, and until it lands for a workload the policy is run-time only there |
| **Endpoint filtering** | Preview, a handful of connectors, and **not enforced for environment variables, custom inputs, or any endpoint created at runtime**. Only static endpoints are evaluated — so a design whose only enforcement is endpoint filtering has no enforcement |
| **Tenant isolation** | Entra-authenticated connectors only; a named connector for which the policy is documented as **not enforced**; guest-to-own-host-tenant connections are not evaluated; propagation measured in hours. A reduction of one vector, never containment |
| **Guest restriction** | Restricts guest access to **Dataverse only**. Guests are not restricted from apps in the same environment that do not use Dataverse; tenant-level guest policy is not overridden; its general-availability state is itself unresolved in the baseline |
| **Environment security group** | A membership control, not a perimeter. Platform administrators show as active and can sign in regardless; **all application users can run in any group-secured environment without being a member**. Not assignable to default or developer environments |
| **IP firewall** | Dataverse only, managed environment only, **audit-only mode enabled by default** (requests allowed regardless of address), and *allow all application users* and *allow trusted services* on by default. Its own audit logs are unsupported under customer-key encryption |
| **Customer-managed keys** | A published exclusion list (§8), and the list grew during the research window |
| **Sharing limits** | Enforced when someone tries to share. Already-shared assets are untouched; once out of compliance, only *unsharing* is permitted. Oversharing remediation is a separate workstream, not a setting |
| **Purview integration** | Discovery and classification over the store's metadata. **Not** an enforcement control on rows or columns — classification is an input to the design, not a runtime gate |
| **Security posture score** | Preview, and the vendor states it is for evaluation purposes only and that it is not receiving further investment in its current form; recommendations are actionable only on managed environments. A backlog generator, not an assurance artifact |
| **Column-level security** | Never applies to the system administrator; cannot secure lookup, formula, primary-name, system or virtual-table columns; leaks through calculated and composite columns |
| **Masking rules · app access control** | Managed-environment capabilities; app access control is preview and its bypasses and interaction with sharing limits are unverified in the baseline |

## 11. The irreversible security decisions · `decision-grade`

These cannot be reversed after provisioning, or can be reversed only by rebuild-and-migrate. They belong
in Discovery, not in Options.

| Decision | Why it cannot be reversed |
|---|---|
| **Residency / region** | The environment is bound to a geography at creation. Multi-region means multi-environment. Where private networking is used, the environment is additionally pinned to an Azure region pair |
| **Table ownership type** (organization vs user/team owned) | Fixed at table creation. A late discovery that rows must be scoped per organizational unit on an organization-owned table means deleting and recreating the table, with migration |
| **The owning business unit on a row** | Immutable unless the matrix-access feature is on. And turning that feature **off** rewrites the owning unit on existing rows to the owner's unit — a data mutation, not a setting |
| **The root business unit** | Unchangeable for the life of the environment |
| **A broad privilege grant** | Grants are additive and cannot be subtracted. The grant made "to unblock the project" is not walked back; roles are rebuilt |
| **Delegated subnet range and DNS** | Immutable while delegated; changing them breaks the delegation and the environment stops working. A subnet cannot be reused across enterprise policies |
| **Customer-key adoption** | Restore is locked to environments encrypted with the same key; a reset deletes encrypted data including backups; audit retention configuration becomes unavailable |
| **Audit retention already written** | Each audit record is stamped with the retention period active at write time. Changing the setting does not change records already written |
| **The default environment** | Cannot be deleted, cannot take a security group, and every licensed user holds the maker role in it. It is not a place a solution with a real security requirement can live; securing it is its own governance workstream |
| **Read-through (virtual) table choice** | Cannot be converted to a standard table; its authorization exclusions are structural (§6.3) |

## 12. Controls whose licence dependency sits outside the platform · `decision-grade`

This is the sharpest security→economics landing in the corpus, and it is the one most often missed:
**satisfying a control can oblige an entitlement for a population that is not the app's own users.**

- **Managed environments gate nearly every strong control** — IP firewall, cookie binding, customer-managed
  keys, Lockbox, sharing limits, app access control, masking rules, VNet support, extended backup. Making
  an environment managed puts **every active user of that environment** in scope for a premium
  entitlement, *including users of standard apps* — not only the users of the app that needed the control.
- **The enforcement is dated.** Users without an appropriate entitlement are blocked from opening apps in a
  managed environment from February 2027.

  > Documented reading · read 2026-09-04 · re-verify: TW-V3 (dated tripwire)

- **The IP firewall and customer-managed keys add a second, higher-tier compliance entitlement** for users
  in the governed environment — an entitlement bought from the productivity/compliance stack, not from
  Power Platform.
- **Conditional Access** on the identity plane carries its own directory-tier prerequisite, and risk-based
  policy a higher one still.
- **Read and export auditing** requires activity logging into Purview, whose availability is entitlement-
  gated — and the option to turn it on is not even visible below the minimum productivity licensing.
- **Private networking** adds an Azure subscription relationship and address-space planning across a
  region pair, which is a dependency on another team's budget as much as on its network.

The obligation this creates: evaluate **control → external entitlement prerequisite → affected population
→ meter** *before* selecting the control. Where the control is mandated and its population is unfunded,
the correct response is not to weaken the requirement silently — it is to select another control or
topology, or to escalate the cost decision. `economics/licensing-and-cost-drivers.md` carries the meters,
populations and growth mechanisms; this file carries only the obligation to look.

## 13. The residual-risk statement obligation · `decision-grade`

Where a mandated control is only partially satisfiable (§10), a binary *"control in place"* is not an
acceptable output. What must be recorded, per control:

1. **The plane on which it is actually enforced**, and its grain.
2. **The documented respect in which it is partial** — in the source's terms, not softened.
3. **Who or what is outside it** — the named bypass population (platform administrators, application
   users), the uncovered connector class, the dynamic-endpoint case, the non-Dataverse app in the same
   environment.
4. **The compensating control**, and on which plane *it* sits — with the honest note where the compensation
   is detection rather than prevention, and therefore inherits detection's cadence and scope.
5. **The residual vector that remains open**, stated as a vector, with an owner who has accepted it.
6. **The re-verification date**, because several of these controls changed state during the baseline's own
   research window.

A design that states its residuals explicitly is defensible. A design that presents any partial control as
containment is not — and the specific failure is presenting *reduction of one vector* as *containment*.

## 14. Failure modes · `decision-grade`

> **The application as the authorization layer.** Access is decided by the connection identity and the
> store's own rules, not by the interface. Hidden controls and post-retrieval filters change the view, not
> the permission; any other client — a second app, the store's own UI, a spreadsheet, the API — reads what
> the app concealed. Consequence: the store choice was wrong, and no amount of app-side work fixes it.

> **Shared identity as the access or integration model.** One principal reaches the source, so per-user
> predicates resolve to one set of rights, attribution collapses (audit records the acting identity), and
> the whole population's traffic lands in one throughput budget. Consequence: three separate requirements —
> authorization, auditability, capacity — fail from one decision, and licence multiplexing to save cost is
> a contractual exposure rather than a trade-off.

> **Authorization model deferred past an irreversible decision.** Tables are created before the access
> model exists. Ownership type is then fixed, grants already issued cannot be subtracted, and the matrix
> case needs a migration programme. Consequence: a confidentiality requirement the built model cannot
> meet, closed only by rebuild-and-migrate.

> **One control treated as the whole control.** Environment separation, or a connector policy, or tenant
> isolation is presented as satisfying a requirement it partially addresses (§10). Consequence: assurance
> built outside the control's stated scope — and the discovery usually arrives as an audit finding, not as
> a defect.

> **Secrets held in makers' assets.** A key lands in an app formula, an automation action input or a
> connector definition, because the sanctioned vault path does not reach the surface that needs it.
> Consequence: credential disclosure to anyone with run-history or maker access, and rotation becomes a
> manual hunt across artifacts.

> **External or anonymous surface published with unreviewed permissions.** Web-role access is cumulative,
> an anonymous role's table permission means visible to anyone, the broadest access type means all rows,
> and the private-site access list itself lives in an environment variable that any role able to edit it
> can change. Consequence: mass exposure — the highest-severity outcome in this domain — plus a lifecycle
> (certificates, keys, visibility) with no owner.

> **A security control lost in transit.** A secured shared connection imported through a connection
> reference is documented as not having its security set properly in the target environment. Consequence:
> the control that protects production is established by the **deployment**, not by the app, so
> post-deployment verification belongs in the release checklist.

> **Network and key constraints discovered after the platform is chosen.** Private egress, on-premises
> reach, residency and key custody carry preconditions that pin regions, freeze network settings, break
> public calls by default, and oblige entitlements across a population. Consequence: a security
> architecture that is economically infeasible rather than merely complex — discovered after commitment.

## 15. Consequences elsewhere · `decision-grade`

- **`economics/licensing-and-cost-drivers.md`** — the control-obliged population (§12). A control gated on
  a managed environment prices *every active user of that environment*, standard-app users included, with
  a dated enforcement milestone; the firewall and key-custody controls add a second, higher-tier
  compliance entitlement; read/export auditing and Conditional Access each add their own. This is the
  landing that turns a security requirement into a budget decision.
- **`governance/governance-and-environments.md`** — who configures the lever and what it prevents
  estate-wide: environment-creation restriction is a *security prerequisite* (an unrestricted tenant lets
  a licensed user create an environment outside every control, and the restriction is not retroactive);
  environment-group rules lock security settings read-only with no per-environment exception; policy
  scope, composition and the tenant-over-environment precedence; and the detection cadence that a
  detection-based posture inherits.
- **`integration/integration-mechanisms.md`** — the network boundary and the mediation tier: outbound-only
  private egress with its preconditions, the outbound-only gateway whose blast radius is its credential,
  the collision between private egress and platform event publishing, and the second enforcement plane
  that external components create.
- **`data/dataverse.md` · `data/sharepoint.md` · `data/azure-sql.md`** — the grain each store can enforce
  (§7), the mechanics behind it, and the scale boundaries on per-item access in the list store.
- **`performance/performance-and-scale.md`** — security-model complexity has a runtime cost with **no
  published curve** (§16), and per-record sharing writes access rows that sit on the access hot path.
- **`operations/operability-and-support.md`** — evidence retention: what auditing captures, what it never
  sees (retrieve and export operations are not covered; read/export evidence requires activity logging),
  that retention is stamped at write time, that audit consumes log capacity, and that audit-log export is
  not a supported operation. An audit requirement is an entitlement + capacity + retention design decision
  taken before go-live, not a switch flipped after.
- **`alm/release-and-lifecycle.md`** — separation of duties between build and release; deployment as a
  privileged operation with the deploying identity owning what it deploys (and therefore becoming the
  runtime identity of deployed automation); security roles and column-security profiles travel in
  solutions while **business units and teams must be created in each environment**; and the connection-
  security control that can be lost at import.
- **`application/application-surfaces.md`** — each surface authorizes differently (§3, plane 5), so a
  multi-surface solution needs a **per-surface** security statement; "we secured the app" is not a
  statement until the surface is named.
- **`architecture/patterns.md`** — a pattern involving an external component is not production-ready until
  the second plane's owner exists.

## 16. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Control propagation and enforcement latency — the window in which a configured control is not yet enforcing | `VS-21` |
| The revocation window: how long an already-issued credential or session keeps working after access is removed | `VS-22` |
| Customer-managed-key operational windows — time to denial, time to inaccessible, absence of automatic healing past it, previous-key-version retention | `VS-35` |
| Connector and service permissibility posture — a policy check is valid on its date only | `VC-03` |
| Audit retention and log-availability windows | `VS-05` · `VS-19` |
| List-store unique-permission scope ceilings, and the item count above which inheritance can no longer be broken | `VS-29` |
| Backup / restore windows underpinning the recovery objective, including the key-version retention that keeps restore possible | `VS-07` · `VS-17` |
| Entitlement fit of the required capability set, and whether one premium capability obliges premium entitlement for **every** user of an artifact | `VC-05` |
| Preview / general-availability state of any control relied on — several controls in this domain changed state during the baseline's own research window | `VC-10` |
| Managed-environment licence enforcement milestone | `TW-V3` |

**Not established in the baseline** — do not fill from general knowledge:

- **No universal numeric curve exists relating security-model complexity — business-unit depth, team and
  share cardinality, column-security breadth — to runtime performance.** The baseline documents that
  overhead exists and that excessive use is detrimental; it publishes no figure. Do **not** invent a
  threshold. The only closure is a **representative pilot at target workload and target model complexity**,
  with realistic principals, record volumes and access patterns. Absence of a published figure must not be
  converted into an arbitrary "safe" number.
- **Per-record sharing has a data and storage consequence, not only a performance one.** Every share,
  access-team grant and cascading reparent writes access rows; those rows **cannot be deleted directly**,
  and they grow on the storage meter. The documented remedy is to change the security model, not to clean
  the table. This is a data/performance consequence of a *security* choice — treat it as such in sizing.
- Whether the allowlist connector policy has reached general availability per maker portal, and whether
  custom and HTTP connector rule types have shipped.
- Whether endpoint filtering has left preview and whether the dynamic-endpoint gap has closed.
- The general-availability state of the guest-access restriction — the baseline's two sources disagree.
- Current status of the two documented connection-security known issues (secured shared connection via a
  connection reference; service-principal solution import) — both are security-control-defeating.
- Hierarchy security's mechanics and its interaction with matrix business units and column security.
- Depth of any label-driven enforcement over store rows or columns (discovery and classification are
  documented; enforcement is not).
- Masking-rule mechanics and limits; app access control's scope and bypasses.
- Whether any platform control can restrict spreadsheet export or direct analytical-endpoint reads beyond
  privacy privileges and the IP firewall.
- Whether managed identity will extend beyond Dataverse plug-ins to connectors or flows.

## 17. What not to infer · `decision-grade`

- **A capability absence is not a verdict.** *"Column security never hides data from the system
  administrator"* is domain knowledge. *"Therefore unsuitable"* is a selection verdict and belongs to
  `decision-tree.md`.
- **A documented boundary here is not evidence that another option class performs better.** The baseline
  holds no like-for-like security comparison against SaaS products, custom/pro-code stacks, incumbent
  platforms or other low-code platforms. Where such a comparison is material it is *unevaluated*, and the
  comparator semantics in `decision-model/outcome-classes.md` stand.
- **Do not read the plane table as a maturity ladder.** Plane 5 is not a weaker version of plane 3; it
  answers a different question (what this surface presents) and is simply not an authorization mechanism.
- **Do not restate a scoped control as a general one.** "Firewall enabled" without *Dataverse only,
  managed environment only, audit mode by default, application users allowed by default* is a false claim,
  not a summary.
- **Do not convert a partial control into a satisfied requirement** (§10), and do not convert an unresolved
  preview state into availability.
- **Do not treat an entitlement prerequisite as an implementation detail.** It changes who pays and how
  many, and it can make a mandated control economically infeasible — which is a decision input, not a
  procurement footnote.
- **Do not infer a performance threshold for the security model** (§16). There is none.

## 18. Where the implementation material lives · `implementation-grade`

Deliberately **not** in this file. All of the following is craft, and craft is never an Options pull
target and may never state a platform limit — it lives in `craft/security-craft.md`:

- role-inference signal sources and priority order, scope-classification and approval-authority signals,
  and inheritance-detection heuristics;
- permission matrices (role × screen, role × entity × CRUD, sensitive fields, approval permissions) and
  their symbol conventions;
- conflict types, conflict-resolution rules and the conflict-log format;
- Power Fx security blocks — app-start security initialisation, screen-access, gallery row-filter, button-
  access and field-visibility patterns;
- audit blocks for Approve / Delete / Export actions and the mandatory audit-trail columns;
- artifact formats — Dataverse security-role definitions, column-security profiles, SharePoint group
  definitions, and role-specific column views for relational row-level security.

**Rotation mechanics** — cadence, vault wiring, connection re-authorisation steps — are implementation and
belong there too. What belongs *here* is only that custody has an owner, that rotation is an operational
process someone must own, and that the surfaces which cannot consume a vault-backed secret change the
topology (§8).
