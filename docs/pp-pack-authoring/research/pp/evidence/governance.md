Research Status: CANONICAL
Research Confidence: MEDIUM
Gate: PASS — Cross-Block Gate Recheck
Canonicalization Basis: Cross-Block Gate Recheck
Canonicalized: 2026-09-03

# Governance — Research Evidence

Research area: **07 — Governance** (`../research-areas.md`). Block B, area 2 of 3.
Draft date: **2026-09-03**. Sibling documents of the same block: `security.md` (area 06), `alm-devops.md` (area 08). Cross-references to the validated foundational Areas 1–4 use the canonical files `platform-suitability.md` (**PS-nn**), `application-architecture.md` (**AA-nn**).
Source policy: `../source-policy.md`.

**Purpose.** Answer: *"What must be true about the organisation's governance of Power Platform for this solution to be deliverable, operable and defensible — and how do those governance requirements change the architecture and the delivery plan?"* Not a governance checklist: a control appears only where it changes what can be built, where it must live, who can change it, or what it costs.

**Provenance rule.** Sources are **fetched** (retrieved 2026-09-03, `ms.date` read from page metadata — the default), **search-verified** (snippet only; a finding relying solely on such a source is capped at MEDIUM), or **T3/T4 signals** (non-Microsoft; never admissible as capability evidence).

**Origin tags.** **Origin:** MS / INF / T3 / T4 / UNKNOWN, as in the sibling documents. Cross-Block V2 uses **VOLATILE VALUE** alongside the source-policy classifications for date-sensitive governance features, licensing prerequisites and rollout/enforcement milestones.

**Overall confidence MEDIUM (self-assessed, no gate).** The cap reflects: (a) Microsoft's governance guidance changed materially during the research window — the CoE Starter Kit is "no longer actively maintained" (GOV-12) and the ALM Accelerator is deprecated (`alm-devops.md` ALM-22) — so a large body of widely circulated third-party governance advice is now built on unmaintained foundations; (b) managed-environment licence enforcement has a dated future milestone (February 2027) that changes the economics of almost every control; (c) quantitative claims about sprawl come only from T3/T4 vendor material; (d) no adversarial review or gate has been run.

**Volatility.** Environment groups and rules, the Actions page, advanced connector policies, inventory/monitor experiences, environment routing, licence auto-claim and the security hub are all 2024–2026 features still expanding. Re-verify §9 before encoding.

---

## 1. What "governance" actually decides (eight levers after Cross-Block V2)

Governance in Power Platform is not a policy document; it is a set of platform configurations that mechanically constrain what makers can do. Seven levers carry essentially all the architectural consequence.

| # | Lever | Configured at | What it mechanically prevents | Cost / friction | Findings |
|---|---|---|---|---|---|
| 1 | **Environment topology** | Tenant (creation control) + per environment | Wrong data in the wrong place; blast radius; residency violations | Licence per environment population; ALM overhead; sprawl | GOV-02..GOV-05, GOV-09 |
| 2 | **Managed environments** | Per environment / per group | Nothing by itself — it *unlocks* the controls | Premium licence for **every active user**; enforcement from Feb 2027 | GOV-06, GOV-11 |
| 3 | **Environment groups + rules** | Tenant | Configuration drift; local admin override | No per-environment exceptions | GOV-07 |
| 4 | **Data policies (DLP → ACP)** | Tenant + environment | Connector combinations; specific connectors/actions/endpoints | Maker friction; fragmentation if over-applied | GOV-10, GOV-11b |
| 5 | **Sharing limits + "Everyone"** | Per environment / group | Oversharing going forward | Existing shares unaffected | GOV-19 |
| 6 | **Solution checker enforcement + block unmanaged customizations** | Per environment / group | Non-compliant imports; ad-hoc production edits | Breaks a documented list of first-party features | GOV-20, GOV-15 |
| 7 | **Ownership, inventory and reactive action** | Tenant (Actions/Inventory) | Nothing preventively — it detects | Weekly cadence; managed environments only for full detail | GOV-13, GOV-14, GOV-17 |
| 8 | **External-estate governance** | Azure / enterprise platform / on-premises ownership domain | Ungoverned APIs, brokers, Functions/workers or gateways becoming shadow infrastructure | Second RBAC/policy/CI-CD/monitoring/cost model and named operator | GOV-XB-01 |

**Consequence (INF):** levers 1–6 are *preventive* and mostly require managed environments; lever 7 is *detective*; lever 8 is a **boundary condition**: Power Platform governance does not govern the external estate and is the only one that works retroactively. A governance model that relies on lever 7 alone is a reporting exercise; Microsoft's own comparison makes the point about the CoE Starter Kit: "The CoE can only react after the limit is exceeded, possibly resulting in noncompliant assets. On the other hand, managed environments uses private APIs, built into the product, that enforce sharing limits before they're passed" (G-07).

---

## 2. Decision boundaries (requirement → governance constraint → architectural consequence)

- Solution has business-critical or confidential data → the default environment is disqualified (no security group, no backup guarantee, everyone is a maker) → **dedicated environment**, with the licence and ALM overhead that implies (GOV-04, `security.md` SEC-17).
- Solution needs any of IP firewall, CMK, Lockbox, sharing limits, pipelines, solution-checker enforcement, extended backup, VNet, app access control → **managed environment**, therefore **premium licences for every active user of that environment**, with app-open enforcement from February 2027 (GOV-06, GOV-11).
- Organisation has more than a handful of environments → per-environment configuration will drift → **environment groups** (managed environments only, one group per environment, no nesting, no per-environment exceptions) (GOV-07).
- Makers must be able to build without endangering production → **environment routing** to personal developer environments inside a governed group, plus restriction of manual environment creation (GOV-08, GOV-09).
- Regulator/audit asks "who owns this application and who supports it" → ownership is not enforced by the platform; ownerless apps are detected weekly and only in managed environments; reassigning an owner "**doesn't** automatically" grant them environment or data-source permissions → **an ownership and support model must be defined and operated outside the platform**, with the platform providing detection (GOV-14, GOV-13).
- Multiple business units / regions with different data rules → environments are geography-bound at creation and DLP is scoped per environment/tenant → **environment-per-region/BU**, grouped, with tenant-level baseline policies and minimal per-environment exceptions (GOV-02, GOV-10).
- Business wants "citizen development" while IT owns risk → the documented model is *managed makers*: personal developer environments, restricted sharing, restrictive default-environment policy, promotion path via pipelines → **the promotion path must exist before makers are unleashed**, otherwise successful apps become ungoverned production (GOV-02, GOV-05, GOV-08, `alm-devops.md` ALM-10).
- Organisation intends to build its own governance tooling → Microsoft's current direction is in-product (Inventory, Usage, Monitor, Actions, APIs), and the CoE Starter Kit is "no longer actively maintained" → **do not design new governance on the Starter Kit**; treat existing kit deployments as technical debt with a migration path (GOV-12).
- Cost of the platform must be predictable → licence auto-claim assigns a premium licence when a user launches an app in a managed environment → **the managed-environment decision is also a licence-consumption decision**; auto-claim must be a deliberate choice, not a default (GOV-18, GOV-06).
- Production support must be possible without production edit rights → block unmanaged customizations makes managed components effectively read-only while still allowing co-owners to read run history, turn flows on/off and run them → **a support model exists, but it depends on an ALM setting** (GOV-15, `alm-devops.md` ALM-15).
- Applications must be retired in a controlled way → the platform gives quarantine (admin-only), inactivity/orphan detection, developer-environment auto-deletion after 90 days, and a documented "move out of default" procedure → **retirement is a process with platform support, not a platform feature** (GOV-17).

---

## 3. Findings

Ids GOV-nn are stable. Sources in §11.

### 3.1 Governance model and operating model

#### GOV-01 — Microsoft frames governance as a maturity progression with three delivery models
- **Classification:** PATTERN
- **Origin:** MS
- **Evidence:** Adoption maturity stages: Initial ("Governance practices are minimal"), Repeatable, Defined, Capable, Efficient; "As organizations progress through these stages, their governance practices must evolve to address increasing complexity and scale" (G-06). Delivery models: "Centralized administration involves a dedicated team managing all environments, while decentralized administration allows individual departments to manage their own environments. Hybrid models combine elements of both" (G-06). Roles named: Power Platform admins (framework, policy, compliance), environment admins (operations of specific environments, escalation path), makers (build within the framework) (G-06). The governance overview enumerates six practices: designate a Power Platform admin; support management at scale; establish an environment strategy; implement reactive governance controls; manage Dataverse for Teams environments; manage the default environment (G-05).
- **Decision impact:** the *governance model* an organisation is in determines what a project may assume. A project in an "Initial" tenant cannot assume DLP, environment routing, pipelines or ownership processes exist; those become project deliverables.
- **Confidence:** HIGH.
- **Sources:** G-05, G-06.

#### GOV-02 — Microsoft's current environment-strategy vision: default environment for M365 productivity only, makers routed to personal developer environments, environments grouped, promotion via pipelines
- **Classification:** RECOMMENDATION + PATTERN
- **Origin:** MS
- **Evidence:** "Many organizations start their Power Platform journey with personal productivity apps and automations built and running in a shared central environment called the *default environment*… As this initial adoption accelerates, Microsoft provides organizations with an on-ramp to an environment strategy for enterprise scale adoption"; "This strategy can result in lack of isolation and makers encroaching on each other. **Imagine if everyone in the company shared a single OneDrive folder for all their documents.** Instead, use environment features to guide makers to their own, personal environment"; "**Prioritize the built-in features of the platform for managing environments when possible, instead of building your own tools**" (G-01). Worked reference topology: default environment for M365 customisations with data policies and sharing limits; only admins create trial/sandbox/production; four environment groups — Development, Shared Development, UAT, Production — plus a pipeline host environment and two pipelines (G-01).
- **Decision impact:** this is the reference architecture a project should be positioned against. Deviations (e.g. shared development environments, no UAT, no pipelines) should be recorded as accepted risks, not silently adopted.
- **Confidence:** HIGH.
- **Sources:** G-01.

#### GOV-03 — Environment types have governance-relevant, non-obvious behaviours
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence (G-01 unless noted):** Developer environments — "Makers can have up to three developer environments. They don't count against your tenant capacity. **Developer environments that haven't been used for 90 days are automatically turned off and then removed from your tenant** if the owner doesn't respond to notifications. Dynamics 365 apps aren't available in developer environments." Trial — "limited to one per user", "automatically removed… after a short period" (30 days, G-21). Sandbox — supports copy/reset, "best used for testing and ALM build environments"; "Provisioning sandbox environments can be restricted to admins… but **converting from a production to a sandbox environment can't be blocked**" (G-21). Dataverse for Teams — "The security model for these environments aligns with the team they're associated with"; "No customizations of security role or assignments are available" (G-21). Support environments — created by Microsoft Support, don't count against capacity (G-01). Default — see GOV-04.
- **Decision impact:** developer environments are cheap and self-cleaning but are *not* a place for anything that must survive; the production→sandbox conversion gap means "production environments are protected" is not enforceable purely by creation controls.
- **Confidence:** HIGH.
- **Sources:** G-01, G-21.

#### GOV-04 — The default environment is the tenant's structural governance problem
- **Classification:** RISK
- **Origin:** MS
- **Evidence:** "Every employee in an organization that uses the Power Platform has access to the default environment" (G-02). "The default environment doesn't provide any backup guarantees and shouldn't be used for production workloads"; "You can't delete the default environment. You can't manually back up the default environment"; 1 TB cap with 3 GB database / 3 GB file / 1 GB log included; all licensed users hold Environment Maker (G-21). Security groups cannot be assigned to default or developer environments (G-29). Restore: "You can't restore a system backup over the default environment… Power Platform admins can use the Power Platform admin center to restore a default environment system backup to a developer environment" (G-23). "When a maker creates a custom SharePoint form in SharePoint, it creates a canvas app in the default environment"; "Power Automate flows created from SharePoint always use the default environment" (G-02).
- **Decision impact:** SharePoint-form-driven and Teams-driven adoption *lands in the default environment by construction*. Any tenant with M365 has a de facto ungoverned application estate unless the documented controls are applied.
- **Confidence:** HIGH.
- **Sources:** G-02, G-21, G-23, G-29.

#### GOV-05 — The documented control set for the default environment, and its trade-offs
- **Classification:** RECOMMENDATION
- **Origin:** MS
- **Evidence (G-03 unless noted):** rename it ("*Personal Productivity Environment*"); configure maker welcome content; enable managed environments; configure sharing limits; keep "Share with Everyone" disabled (default) — "The **Everyone** group for your organization contains all users who have ever logged in to your tenant, **which includes guests and internal members**… the membership… can't be edited nor viewed"; establish a data policy — "If the default environment is a managed environment, **prevent agents, apps, and flows from calling any service**: Scope: Default environment only; Business: Empty; Non-Business: Empty; Blocked: All connectors" via ACP; if managed environments are not possible, "block new connectors" (set the default group to Blocked), "limit makers to prebuilt connectors", "limit custom connectors" (block all URL patterns); secure Exchange integration with server-side rules using the documented SMTP headers (`x-ms-mail-application`, `x-ms-mail-operation-type`, `x-ms-mail-environment-id`); apply tenant isolation. Additionally: designate a SharePoint-form environment via `Set-AdminPowerAppSharepointFormEnvironment` — with the warnings "Existing SharePoint forms aren't migrated"; "If you delete the SharePoint form environment after setting it, **the custom SharePoint forms are lost**" (G-02). Recommended default-environment managed settings: sharing "Exclude sharing with security groups" + limit 20; solution checker "Block and send emails" (G-01, G-07).
- **Decision impact:** securing the default environment is a project in itself with user-visible impact (breaking existing apps), which is why it must be sequenced with communication and a data-policy governance message.
- **Confidence:** HIGH.
- **Sources:** G-01, G-02, G-03, G-07.

### 3.2 Managed environments: the governance/licensing coupling

#### GOV-06 — Managed environments are the delivery vehicle for nearly every governance control
- **Classification:** FACT + TRADE-OFF
- **Origin:** MS
- **Evidence:** Feature list: environment groups, limit sharing, weekly usage insights, data policies, pipelines, maker welcome content, solution checker, IP firewall, IP cookie binding, CMK, Lockbox, extended backup, desktop-flow data policies, App Insights export, catalog administration, default environment routing, Copilot app descriptions, VNet support, conditional access on individual apps, app access control, masking rules (G-10). Grouped by Microsoft as more visibility / more control / less effort (G-01). "Managed environments are included as an entitlement with standalone Power Apps, Power Automate, Microsoft Copilot Studio, Power Pages, and Dynamics 365 licenses"; "**Managed environment isn't included as an entitlement in the Developer Plan when users run their assets**" (G-10).
- **Decision impact:** the question "should this environment be managed?" is answered by the control requirements, and the answer immediately produces a licence bill for the whole user population of that environment.
- **Confidence:** HIGH.
- **Sources:** G-01, G-10.

#### GOV-07 — Environment groups: the scale mechanism, with five hard constraints
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence (G-04 unless noted):** "Environment groups can only contain managed environments"; "Each environment can belong to only one group, and groups can't overlap or be nested"; "Environments in a group can span different regions and types as long as each is managed"; "**Per-environment exceptions aren't currently supported**"; "When a rule is published at the environment group level, it's enforced across every environment within that group… the corresponding setting or policy becomes **locked (read-only)** within individual environments, ensuring that local system administrators can't modify or override these centrally defined rules"; on removal, "the environment retains the last applied configuration… but becomes unlocked". Known limitation: publishing sharing limits, maker welcome content, solution checker, usage insights, backup retention or generative-AI settings **overrides** any existing environment-level values on join — "if you've published sharing limits in your environment group, but already had maker welcome content and sharing limits set at the environment level, upon adding the environment to the group, the sharing limits are updated to match the group's… and the maker welcome content is reset". Rules available: sharing controls for canvas apps, usage insights, maker welcome content, solution-checker enforcement, backup retention, AI-generated descriptions (G-01), plus advanced connector policies, IP firewall and cookie binding at group level (G-17, S-01 of `security.md`). Environment routing can create new developer environments directly inside a designated group (G-04).
- **Decision impact:** groups make governance scalable and make local admin autonomy impossible in the ruled dimensions. The absence of per-environment exceptions means the group taxonomy must be designed around the *exception cases*, not the common ones.
- **Confidence:** HIGH.
- **Sources:** G-01, G-04, G-17.

#### GOV-08 — Environment routing moves makers out of the default environment automatically
- **Classification:** PATTERN
- **Origin:** MS
- **Evidence:** Routing "redirects makers into their personal development environment and creates new developer environments, as needed"; "The developer environments that are created by routing are managed by default"; "Makers are automatically assigned a security role that makes them an environment admin of their developer environment. When the environment is a part of an environment group, the maker—as the environment admin—**can't change the environment settings** because they're managed by the environment group rules"; two extra controls — disallow manual creation of developer environments in tenant settings, and "specify a security group, in the routing policy, to limit who can automatically get an environment created"; "If an environment group is selected for routing but later you decide to change it… **Existing developer environments remain in whichever group they were originally placed, unless moved manually**" (G-01, G-04).
- **Decision impact:** this is the mechanism that makes "citizen development with guardrails" real. Without it, the maker population defaults into the tenant's least-governed environment (GOV-04).
- **Confidence:** HIGH.
- **Sources:** G-01, G-04.

#### GOV-09 — Environment creation control is a tenant setting, is not retroactive, and has a documented gap
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** Restrict via tenant settings for **Developer environment assignments**, **Production environment assignments**, **Trial environment assignments** → "Only specific admins"; after restriction only Global, Dynamics 365 and Power Platform admins can create environments. "**Environments created before the restriction remain manageable by their creators even after the restriction is applied.** Restriction prevents any new environments being created and managed" (G-08). PowerShell equivalents: `DisableEnvironmentCreationByNonAdminUsers`, `DisableTrialEnvironmentCreationByNonAdminUsers`, `disableDeveloperEnvironmentCreationByNonAdminUsers` (G-08). Gap: "converting from a production to a sandbox environment can't be blocked" (G-21). Default posture without restriction: "users with the correct licenses can create an environment as long as 1 GB of capacity is available" (G-08); "By default, anyone who has a Power Platform Premium license, a Developer Plan license, or a Power Platform tenant admin role can create a developer environment from the admin portal" (G-01).
- **Decision impact:** governance must be established *before* adoption scales, because the tenant setting does not reach environments already created. In a tenant with existing sprawl, remediation is a discovery-and-migration exercise.
- **Confidence:** HIGH.
- **Sources:** G-01, G-08, G-21.

### 3.3 Data policies as governance

#### GOV-10 — The documented data-policy strategy: tenant-level baseline, minimal policies, environment policies as exceptions
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS
- **Evidence (G-15 unless noted):** Quick facts verbatim: "Data policies can be scoped at the environment level and tenant level"; "**Environment data policies can't override tenant-wide data policies**"; "If multiple policies are configured for one environment, **the most restrictive policy applies** to the combination of connectors"; "**By default, no data policies are implemented in the tenant**"; "Policies can't be applied at the user level, only at the environment or tenant level"; "**Data policies are connector aware, but they don't control connections made using the connector**". Recommended starting point: one policy spanning all environments except selected production ones, limited to Microsoft 365 and standard microservices with everything else blocked (this also covers the default environment and every newly created environment); more permissive policies for shared productivity environments; production environments excluded and given their own tenant-level policy. "**Create a minimal number of policies per environment. There's no strict hierarchy between tenant and environment policies**… Multiple data policies applied to one environment will fragment your connector space in complicated ways"; "Centrally manage data policies using tenant level policies, and use environment policies only to categorize custom connectors or in exception cases." Fragmentation is quantified: three policies over ten connectors produce 2³ = 8 groups, three of them empty (G-16). Blocked always wins across policies (G-16).
- **Decision impact:** the number of policies is itself an architectural decision. A project that requests "its own DLP policy" adds a dimension of fragmentation to every environment it touches.
- **Confidence:** HIGH.
- **Sources:** G-15, G-16.

#### GOV-11b — Connector governance is mid-migration: classic DLP, ACP, endpoint filtering, virtual connectors
- **Classification:** CONSTRAINT + TRADE-OFF
- **Origin:** MS
- **Evidence:** Classic classification: three groups; new connectors land in the default group (initially Non-Business), and Microsoft says "You can [change the default data group]… but don't" for general policies while recommending Blocked as the default group specifically for the default environment (G-14, G-03). Non-blockable list includes SharePoint, Microsoft 365 Outlook, Teams, OneDrive for Business, Power BI, Excel Online (Business), Planner, Approvals, Notifications, Dataverse (G-14). ACP: default-deny allowlist, certified connectors only, custom and HTTP "not yet supported", virtual connectors never; on managed environments ACP can block otherwise non-blockable connectors (G-17). Endpoint filtering: preview, eight connectors, "rules don't apply to environment variables, custom inputs, or any endpoint dynamically created at runtime" (`security.md` SEC-25). Copilot Studio virtual connectors are "evolving into their own dedicated governance rules"; desktop-flow virtual connectors are "transitioning to certified connectors" (G-13, G-17).
- **Decision impact:** for the next planning horizon the tenant must run **two** connector-governance systems in parallel (mixed mode), and the custom-connector/HTTP gap has to be covered by the older one. Any pack rule that says "block connector X" must state which system enforces it.
- **Confidence:** HIGH.
- **Sources:** G-03, G-13, G-14, G-17.

### 3.4 Governance at scale, inventory and ownership

#### GOV-12 — Microsoft's governance tooling has moved in-product; the CoE Starter Kit is no longer maintained
- **Classification:** FACT (high impact)
- **Origin:** MS
- **Evidence:** "**The Power Platform CoE Starter Kit is no longer actively maintained.** Its core capabilities are part of the Power Platform admin center. **Issues are no longer reviewed or addressed.** If you identify a potential security issue, please report it to the Microsoft Security Response Center." "The CoE Starter Kit remains available for existing and new deployments, but it will not be enhanced with new capabilities." Mapping of kit scenarios to product: **Inventory** (apps, flows, agents across the tenant), **Usage** (adoption, top resources and owners), **Monitor** (operational health), **Actions** (risks, best practices, governance insights); plus Power Platform CLI, Power Platform API, inventory API and the Power Platform for Admins V2 connector (G-09). Older guidance still recommends the kit for specific gaps (G-06, G-07, G-01) and was written before the deprecation.
- **Decision impact:** three consequences. (1) New governance capability should be designed on PPAC + APIs. (2) Existing kit deployments are technical debt with a monthly-update burden that no longer buys new features. (3) A significant share of publicly available governance guidance (including Microsoft's own older pages) presumes the kit; treat those recommendations as historical.
- **Conditions:** CONFLICTED with G-06/G-07 which still direct readers to kit components (see GOV-C1).
- **Confidence:** HIGH (deprecation statement) / MEDIUM (functional parity of the in-product replacements — not verified).
- **Sources:** G-01, G-06, G-07, G-09.

#### GOV-13 — Reactive governance: what the platform detects, at what cadence, and for which environments
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence:** Categories: business-continuity risks (ownerless resources; high-value resources in the default environment), tenant hygiene (overshared resources; inactive resources), licences (pending requests; intelligent recommendations), change requests and approvals (new environments; data-policy changes; user management; governance settings) (G-07). Actions page: "It analyzes **all managed environments** and the apps in these environments"; "The actions page shows a summary of recommendations for non-managed environments… Admins can turn on managed environments from the actions page to view the affected resources and act on them"; "When you turn on managed environments, it might take up to **72 hours** for the actions page to show full details"; recommendations refresh weekly (some daily/real time); snooze (non-security, up to two months), dismiss (security), delegate/share via Teams, action history, trends; automation via the Power Platform for Admins V2 connector actions *Get recommendations*, *Get recommendation resources*, *Execute recommendation action* (G-19). Category list: Security, Operational efficiency, Licensing and capacity, Performance (G-19).
- **Decision impact:** detection latency (weekly, 72 h after enabling) and scope (managed environments) set the floor for any control that is "monitored, not prevented". Automated remediation is possible but must be built.
- **Confidence:** HIGH.
- **Sources:** G-07, G-19.

#### GOV-14 — Ownership is not enforced by the platform, and reassignment does not carry permissions
- **Classification:** RISK + CONSTRAINT
- **Origin:** MS
- **Evidence:** Recommendation "Assign valid owners to apps to mitigate business continuity risks" lists "apps in all the managed environments… that don't have a valid owner. Currently, this list contains apps active in the last 90 days"; severity High, weekly refresh, managed environments only. Critically: "**New owners don't automatically get permissions to the environment or data sources used in the app. Admins must manually give owners permission.**" Also "New owner information isn't updated in the list. The app is shown in the list until the next planned scan." Promote-co-owner-to-owner is available (G-20). Flow ownership: SPN ownership recommended for critical flows precisely because "your flows continue to run smoothly even if employees leave the company" (`security.md` SEC-22). "When a maker leaves an organization, the maker's apps and flows are in effect owner-less" (G-02).
- **Decision impact:** an ownership *record* is not an ownership *capability*. A support model must define who holds the connections, who holds the environment role, and who is on the hook — the platform only flags absence.
- **Confidence:** HIGH.
- **Sources:** G-02, G-20.

#### GOV-15 — A production support model exists, and it depends on an ALM setting
- **Classification:** PATTERN
- **Origin:** MS
- **Evidence:** With **block unmanaged customizations** enabled: "responsible users can be made a co-owner on a managed flow in a test or production environment. Co-owners can review flow run history… to watch for errors and understand those errors. **Those users won't be able to make changes to the managed component, so it's effectively read-only to them.** They're able to turn the flow on and off if needed, as well as to run the flow for use or testing purposes"; allowed operations also include changing environment variables, assigning ownership and sharing records (D-12).
- **Decision impact:** "who can investigate a production incident without being able to change production" has a documented answer, but only in an environment that blocks unmanaged customizations — an ALM configuration with its own break-list (`alm-devops.md` ALM-15).
- **Confidence:** HIGH.
- **Sources:** D-12.

#### GOV-16 — Inventory, naming and documentation are the organisation's job, with platform assistance
- **Classification:** RECOMMENDATION
- **Origin:** MS
- **Evidence:** PPAC Inventory "view and govern all apps, flows, and agents created across your tenant", Usage, Monitor, Actions, plus the inventory API and admin connectors (G-09). Environment-strategy guidance includes explicit sections on naming environments and groups and on naming conventions (G-01 §"Naming environments and groups"). Governance framework guidance requires assessing current policies, defining objectives (security, compliance, efficiency, scalability), developing policies (connector management, environment management, solution development, security protocols), establishing roles, and defining a delivery model (G-06). Automation of "new environment requests" and "new connector requests" with approval workflows is recommended, including the question of who approves — "if a maker requests the SAP connector… does the Power Platform or SAP service owner approve this request?" (G-06).
- **Decision impact:** an engagement that expects "the platform will tell us what we have" gets an inventory, not a service catalogue. Ownership, criticality, support tier and data classification are attributes the organisation must add.
- **Confidence:** HIGH.
- **Sources:** G-01, G-06, G-09.

#### GOV-17 — Retirement and clean-up: quarantine, orphan/inactivity detection, auto-deletion, and a documented migration procedure
- **Classification:** PATTERN
- **Origin:** MS
- **Evidence:** Quarantine: "Makers can edit a quarantined app, but users can't play it… **Only admins can change an app's quarantine state**" (`Set-AppAsQuarantined` / `Set-AppAsUnquarantined` / `Get-AppQuarantineState`) (G-02). Detection: "recommendations for apps without valid owners and apps that haven't been used in the last 60 days" (G-02); inactive-resource recommendations on the Actions page (G-07, G-19). Developer environments unused for 90 days are turned off and removed (G-01). Documented move-out-of-default procedure: create a solution with the app and dependencies → export/import to the target environment → ensure security roles → migrate configuration and data → test → notify → remove access in default → delete the solution, "Make sure that you don't delete any shared assets" (G-02). Backup caveat: "restoring the default environment might also restore unused or orphaned apps and flows removed during cleanup" (G-02).
- **Decision impact:** retirement is executable but manual and multi-step; it needs an owner and a checklist, and the data migration step is often the real work.
- **Confidence:** HIGH.
- **Sources:** G-01, G-02, G-07, G-19.

### 3.5 Licensing and cost as governance constraints

#### GOV-11 — Managed-environment licensing: entitlement, enforcement dates, and the report that exposes exposure
- **Classification:** CONSTRAINT (high impact) + RISK
- **Origin:** MS
- **Evidence (G-11):** Entitling licences: "Power Apps Premium, Power Automate Premium, Microsoft Copilot Studio, Copilot Studio for Microsoft 365 Copilot…, Power Pages, Dynamics 365 Premium, Enterprise, Team Members, and Dynamics 365 Customer Insights. Pay-as-you-go meters for Power Apps per app, Power Pages, and Copilot Studio also qualify. **When you activate managed environments in an environment, all active usage requires one of these standalone licenses or pay-as-you-go meters.**" Enforcement timeline: administrator notifications from March 2026; end-user in-app notifications from June 2026 (informational → warning after 7 days → error after a further 7 days); "**Starting February 2027, users who don't have an appropriate license are blocked from opening apps in the managed environment**". Scope: "Only environments that you enable as managed environments are in scope"; "Every user who runs an app in a managed environment is in scope, **including users who run standard apps**." Diagnostics: the "Users requiring licenses in Managed Environments" report in PPAC, with the caveats that it "lists users who accessed at least one app in any managed environment without an appropriate license" and excludes users who didn't launch an app that month. Trial licences count but expire in 30 days; the Developer Plan does not entitle managed environments (G-10).
- **Decision impact:** the governance-security-ALM control set has a hard, dated price. Any architecture that assumes managed environments must include a licence census of the user population — and standard (non-premium) apps do not escape it.
- **Confidence:** HIGH.
- **Sources:** G-10, G-11.

#### GOV-18 — Licence auto-claim reduces friction and increases consumption
- **Classification:** TRADE-OFF
- **Origin:** MS
- **Evidence:** "If a user without a standalone Power Apps license **launches an app in a managed environment**, the system automatically assigns the user a Power Apps per user license"; similarly for premium flows/RPA; "We recommend configuring license auto-claim if your environment strategy includes managed environments. Users of apps and flows encounter the least amount of licensing friction, and you only consume licenses for users who are actively running apps" (G-01). Auto-claim policies are tenant settings (G-18); "Ensure you have sufficient license capacity in the tenant" (G-11).
- **Decision impact:** auto-claim converts an access decision into a spend decision made by an end user's click. It must be paired with the licence-consumption view and with sharing limits.
- **Confidence:** HIGH.
- **Sources:** G-01, G-11, G-18.

### 3.6 Standard governance settings by environment type

#### GOV-19 — Sharing limits: documented per-environment-type recommendations, and the retroactivity gap
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS
- **Evidence:** "**The limit only applies to future sharing.** If you apply a sharing limit of 20 to an environment with resources that are already shared with more than 20 users, those resources continue to work for all users the resources were shared with. Create a process to inform makers… In some cases, you might decide to move the solution to another environment." Common limits by type: Default — exclude security groups, limit 20; Developer — exclude security groups, limit 5; Sandbox — exclude security groups, no individual limit (or no limits if the team manages testers); Production — no limits by default, or exclude security groups when access is via an IT-managed group (G-01). Rules cover canvas apps, solution-aware cloud flows and agents, with agent editor/viewer granularity (G-12). Enforcement latency "up to an hour"; non-compliant resources allow "only unsharing" until compliant (G-12). "Sharing rules in Dataverse for Teams environments don't impact sharing to a Team when you select **Publish to Teams**" (G-12).
- **Decision impact:** the sharing posture is a per-environment-type standard, and remediating pre-existing oversharing is a separate campaign.
- **Confidence:** HIGH.
- **Sources:** G-01, G-12.

#### GOV-20 — Solution checker enforcement: documented per-environment-type standard, blocking only on critical
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS
- **Evidence:** Modes None / Warn / Block; in Block, "When a solution has highly-critical issues, the import process is canceled… This happens before the actual import, so there aren't any changes to the environment"; "**only critical severity rules block a solution from being imported**"; rule exclusions are supported; emails go to Power Platform and Dynamics 365 admins plus weekly-digest recipients; "Solution checker enforcement is not available when the environment is in the Administration mode" (G-22). Recommended settings: Default — Block + send emails; Developer — Warn, no emails; Sandbox — Warn, no emails; Production — Block + send emails; Teams — Block + send emails (G-01, G-07).
- **Decision impact:** enforcement is a *release gate configured by governance* — which is why it appears in this document and in `alm-devops.md` (ALM-16). It does not validate functionality, and does not guarantee import success.
- **Confidence:** HIGH.
- **Sources:** G-01, G-07, G-22.

#### GOV-21 — Backup retention is a governance rule with a production-managed-environment condition
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "By default, the system retains backups of all production and nonproduction environments for **seven days**. However, for production managed environments, you can extend the retention period **up to 28 days**"; retention values 7/14/21/28; "If a backup retention rule is already set at the environment group level, **you can't override the setting at the individual environment level**"; "You can extend the backup retention period only for production managed environments. For all other nonproduction environments, the default… of seven days is used, regardless of the setting's value"; trial environments are not backed up; the default environment cannot be manually backed up (G-23).
- **Decision impact:** RPO/retention requirements above 28 days cannot be met by platform backup at all — they require data-level archival (deferred to Area 11).
- **Confidence:** HIGH.
- **Sources:** G-23.

#### GOV-22 — Tenant settings are the outer ring of governance
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** Governance-relevant tenant settings include: Add-on capacity assignments; Analytics (tenant-level); Auto-claim policies for Power Apps and Power Automate; Catalog assignments; **Developer / Production / Trial environment assignments** (creation control); Environment routing (managed environments only); Customer Lockbox (managed environments only); Weekly digest (managed environments only); Power Automate flow run resubmission; Desktop-flow actions in data policies; tenant capacity and licensing summary visibility; Copilot/AI settings; support-request visibility. Access requires Global, Power Platform or Dynamics 365 administrator (G-18). Power Pages adds `enableSystemAdminsToChangeSiteVisibility` and a non-production public-site restriction (G-26).
- **Decision impact:** a project cannot assume any of these; each is a tenant-wide decision owned by someone outside the project.
- **Confidence:** HIGH.
- **Sources:** G-18, G-26.

#### GOV-23 — Power Pages carries its own governance surface
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** "Your tenant admin can control whether makers are allowed to make **non-production** sites public"; when blocked, private→public is unavailable and an "Access restricted" message appears; "If a non-production site was already **Public** before the restriction was applied, the site remains public." Who may change visibility: Power Platform / Dynamics 365 administrators always; System Administrators only when the tenant setting `enableSystemAdminsToChangeSiteVisibility` is true (null behaves as true), otherwise only through a designated Entra security group managed in PPAC (G-26). Site-level governance recommendations (WAF, SSL and authentication-key expiry within 90 days) appear as Actions-page items, managed environments only (G-20).
- **Decision impact:** external-facing workloads need a named owner for visibility, certificates and authentication keys — an operational commitment with hard expiry dates.
- **Confidence:** HIGH.
- **Sources:** G-20, G-26.

#### GOV-24 — Dataverse for Teams is a governance category of its own
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** Environments are "automatically created for the selected team when you create an app in Teams"; "Limited control. Admins have limited settings available for Teams environments. **No customizations of security role or assignments are available.** Teams members are automatically mapped to their Teams membership type — owners, members, and guests — with a corresponding security role assigned by the system"; location is the tenant home; security groups cannot be applied (G-21). Managing them is one of the six governance practices (G-05). Sharing rules do not affect Publish-to-Teams (G-12). Backups are supported with 7-day retention and self-restore only (G-23). Recommended managed settings: solution checker Block + emails (G-07). Growth beyond the Teams limits is a one-way upgrade to full Dataverse with premium licences for all users (`application-architecture.md` AA-50).
- **Decision impact:** anything created through Teams starts outside the environment strategy and cannot be re-secured in place; the governance response is detection plus a migration path.
- **Confidence:** HIGH.
- **Sources:** G-05, G-07, G-12, G-21, G-23; `application-architecture.md` AA-50.

#### GOV-25 — Guest and external-user governance is per environment and defaults to restricted
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** "By default, guest access to Dataverse is restricted for all new environments"; per-environment toggle; "Doesn't override tenant-level guest access policies set in Microsoft Entra ID"; "Guests aren't restricted from accessing apps in the environment that aren't using Dataverse" (G-28). The Everyone group includes guests and is not enumerable (G-03).
- **Decision impact:** external collaboration is an explicit per-environment governance decision with a documented residual (non-Dataverse apps).
- **Confidence:** HIGH.
- **Sources:** G-03, G-28.

#### GOV-26 — Independent evidence of the failure mode: sprawl, unknown estate, ownership gaps
- **Classification:** RISK (signal only)
- **Origin:** T3/T4 — **not admissible as capability evidence**
- **Evidence (search-verified snippets, G-27):** claims that organisations are found with "400+ apps scattered across dozens of environments, over 1,000 flows with unclear ownership, and no central registry"; that "Enterprise environments typically contain 40–60% more Power Platform solutions than IT leadership initially estimates"; that "DLP policy alignment efforts typically identify 20–30% of existing flows violating enterprise data handling requirements"; and that organisations without formal governance experience "application sprawl, security violations, and compliance breaches at rates 3-4x higher". None of these figures is sourced to a published methodology.
- **Why it is recorded:** the *direction* is corroborated by Microsoft's own product response — inventory, ownerless-app recommendations, inactivity detection, environment routing and sharing limits all exist because this failure mode is common (G-07, G-19, G-20).
- **Decision impact:** use as a prompt to measure the actual estate at engagement start (count of environments, apps, flows, owners, connectors), never as a benchmark to quote.
- **Confidence:** LOW (figures) / MEDIUM (direction, corroborated by MS product behaviour).
- **Sources:** G-07, G-19, G-20, G-27.

---

## 4. Governance decision criteria (REQUIREMENT → GOVERNANCE CONSTRAINT → ARCHITECTURAL CONSEQUENCE)

| # | Requirement | Governance constraint (evidence) | Architectural / delivery consequence |
|---|---|---|---|
| 1 | Business-critical availability | Default environment has no backup guarantee and cannot be manually backed up (GOV-04) | Dedicated production environment; 7-day default retention, 28 only if production + managed (GOV-21) |
| 2 | Enforced (not advisory) controls | Nearly all preventive controls require managed environments (GOV-06) | Premium licence for every active user; Feb 2027 app-open enforcement (GOV-11) |
| 3 | Consistency across many environments | Group rules lock settings; no per-environment exceptions (GOV-07) | Group taxonomy designed around exceptions; local admin autonomy removed in ruled dimensions |
| 4 | Makers must build safely | Routing creates managed developer environments in a group; manual creation must be disabled separately (GOV-08, GOV-09) | Personal developer environments + restricted creation + a promotion path that exists on day one |
| 5 | Only approved data flows | Tenant baseline policy + minimal environment exceptions; most restrictive wins; fragmentation 2^n (GOV-10) | Connector catalogue and an exception process; policy count is an architectural variable |
| 6 | Bespoke API integration | ACP does not cover custom or HTTP connectors (GOV-11b) | Custom-connector governance stays on classic policy + endpoint filtering + target-side control |
| 7 | Known owner and support path | Platform detects absence weekly, only in managed environments; reassignment grants no permissions (GOV-13, GOV-14) | Ownership/support model defined in the engagement; connections owned by an SPN |
| 8 | Production changes must be reviewable | Solution checker enforcement (critical only) + block unmanaged customizations (GOV-20, GOV-15) | Release gate configured at environment/group level; production support via co-ownership on managed components |
| 9 | Predictable cost | Auto-claim assigns licences on app launch in managed environments (GOV-18) | Auto-claim is a deliberate decision; sharing limits become cost controls |
| 10 | Regional/BU separation | Environments are geography-bound at creation; groups may span regions (GOV-03, GOV-07) | Environment-per-region/BU; naming convention and group taxonomy up front |
| 11 | Teams-based collaboration apps | Dataverse for Teams: no role customisation, no security group, one-way upgrade (GOV-24) | Treat as personal/team productivity only; plan the migration trigger |
| 12 | External audience | Public/non-production site visibility governed at tenant level; certificate and auth-key expiry are dated obligations (GOV-23) | Named owner for the site's lifecycle; environment separation for the external workload |
| 13 | Central governance capability | CoE Starter Kit no longer maintained; capability moved in-product (GOV-12) | Build on PPAC + APIs; treat existing kit deployments as debt |
| 14 | Retire an application | Quarantine + orphan/inactivity detection + manual migration procedure (GOV-17) | Retirement checklist with a data-migration step and an owner |
| 15 | Evidence for audit | Detection is weekly; Actions history and audit logs are the artefacts (GOV-13) | Reporting cadence and evidence retention agreed with the auditor, not assumed |

---

## 5. Governance anti-patterns (evidence-backed)

- **GOV-A1 — No environment strategy.** The documented consequence is that all adoption lands in the default environment (GOV-04) where no security group can be applied, backups are not guaranteed and everyone is a maker.
- **GOV-A2 — Uncontrolled environment creation.** Without the tenant settings (GOV-09), any licensed user creates environments outside every group, policy and control — and the restriction does not reach environments already created.
- **GOV-A3 — Production workloads in the default environment.** Contradicted verbatim: "shouldn't be used for production workloads" (GOV-04). The documented remedy is the move-out procedure (GOV-17).
- **GOV-A4 — Uncontrolled connectors / no data policy.** "By default, no data policies are implemented in the tenant" (GOV-10) — the starting state is permissive, and new connectors are added to the default group over time (GOV-11b).
- **GOV-A5 — A policy per project.** Documented outcome: 2^n fragmentation of the connector space with empty groups, and maker-visible failures that are hard to diagnose (GOV-10).
- **GOV-A6 — Unmanaged production changes.** Countered by block unmanaged customizations (GOV-15) and by managed-solution discipline (`alm-devops.md` ALM-02, ALM-15).
- **GOV-A7 — Orphaned applications.** Detected but not prevented; and reassigning ownership does not grant the new owner access (GOV-14).
- **GOV-A8 — No support model.** The platform supplies detection and a read-only support mechanism; the rota, SLA and escalation path are organisational (GOV-13, GOV-15).
- **GOV-A9 — Excessive centralisation.** Group rules remove local admin control in ruled dimensions and support no exceptions (GOV-07); Microsoft's own delivery-model guidance offers centralised, decentralised and hybrid (GOV-01). Over-centralising drives shadow adoption in Teams and SharePoint, both of which default *outside* the strategy (GOV-04, GOV-24).
- **GOV-A10 — Excessive decentralisation.** The mirror failure: every business unit sets its own policies, producing the fragmentation of GOV-10 and the estate described in GOV-26.
- **GOV-A11 — Building governance tooling that duplicates the product.** "Prioritize the built-in features of the platform for managing environments when possible, instead of building your own tools… You should evaluate any custom tooling against new features as they become available" (GOV-02); reinforced by the kit deprecation (GOV-12).
- **GOV-A12 — Treating the security score or the Actions page as assurance.** Preview, 24 h refresh, managed environments only (`security.md` SEC-35, GOV-13).

---

## 6. Unknowns (UNKNOWN)

- **GOV-U-01** — Functional parity between the deprecated CoE Starter Kit components and the in-product Inventory/Usage/Monitor/Actions experiences (the mapping is stated, the parity is not).
- **GOV-U-02** — Whether environment-group rules will gain per-environment exceptions, and whether a group hierarchy will exist ("Although you can't configure the group hierarchy yet…", G-01).
- **GOV-U-03** — Whether automation of environment-group membership through the admin connector shipped ("Moving environments is a manual action today, but you'll be able to automate it when the Power Platform admin connector supports the group feature in a future update", G-01).
- **GOV-U-04** — Practical impact of the February 2027 licence enforcement on tenants that enabled managed environments broadly for governance reasons (no Microsoft guidance seen on de-scoping).
- **GOV-U-05** — Whether tenant-level analytics (prerequisite for the security score) has any data-residency or retention implication.
- **GOV-U-06** — Governance of Copilot Studio agents beyond DLP/virtual connectors and sharing limits (agent authentication and channel controls are preview; not researched here).
- **GOV-U-07** — Whether Power Platform inventory/API coverage includes Power Pages sites and desktop flows at the same fidelity as apps and flows.

---

## 7. Conflicts (CONFLICTED)

- **GOV-C1 — Is the CoE Starter Kit part of the recommended governance model?** G-09 (ms.date 2026-05-07): "no longer actively maintained… Issues are no longer reviewed or addressed." G-06 (2025-09-02) and G-07 (2025-08-18) still direct readers to kit components for automation, environment requests and pulse surveys; G-01 (2026-05-04) references the kit's environment-request component. **More authoritative:** the dedicated kit page, which is also the most recent. **Resolution:** treat kit recommendations in older pages as historical. Record as a live conflict because much third-party governance material has not caught up.
- **GOV-C2 — Managed environments as a governance default vs their licence cost.** Microsoft recommends enabling managed environments broadly, including for the default environment (G-02, G-03, G-01), while also documenting that every active user in a managed environment needs a premium licence, enforced from February 2027 (G-11). For a tenant whose default environment is used by all employees, these two recommendations are in direct economic tension. **Resolution:** not a documentation error — it is a genuine trade-off that must be surfaced as a cost decision, not absorbed silently. Confidence HIGH that the tension exists; the resolution is organisation-specific.
- **GOV-C3 — "Environment groups only contain managed environments" vs ACP on non-managed environments.** G-04 restricts group membership to managed environments; G-17 states ACP can be configured on a single non-managed environment ("so that all customers using classic data policies can migrate to ACP without extra cost"), with non-blockable connectors remaining non-blockable there. **Resolution:** consistent — group-level governance is managed-only; single-environment ACP is not. Recorded because it is easy to mis-state.

---

## 8. Deferred to other areas

- Licence pricing, capacity add-ons, pay-as-you-go and total cost of ownership → **Area 10 (Licensing and Cost)**. This document records only the *existence and shape* of the dependencies (GOV-11, GOV-18).
- Monitoring, alerting, incident management, business continuity and DR beyond backup retention → **Area 11 (Operations and Support)**.
- Solution structure, pipelines, source control and release mechanics → `alm-devops.md`.
- Identity, Dataverse authorization, connector and network controls → `security.md`.
- Capacity/performance implications of many environments → **Area 09**.

---

## 9. Verification list before pack encoding (mandatory)

1. Managed-environment licence enforcement (February 2027) — status, and any de-scoping guidance (G-11).
2. Environment-group roadmap: per-environment exceptions, group hierarchy, connector-based automation (GOV-U-02, GOV-U-03).
3. Whether the in-product Inventory/Actions experiences have absorbed the remaining CoE Starter Kit scenarios (GOV-U-01).
4. ACP rollout state and whether custom/HTTP connector rule types shipped (GOV-11b).
5. Actions-page recommendation catalogue (it grows; the security list alone changed within the window).
6. Default-environment guidance — the "block all connectors via ACP" recommendation is new and depends on ACP availability (G-03).
7. Developer-environment auto-deletion window (90 days) and the three-per-maker limit (G-01).
8. Backup retention options and any change to the production-managed-environment condition (G-23).

---

## 10. Implications for the aisa knowledge model (pointers, not pack content)

- Governance findings are mostly **preconditions**, not design choices: they describe what must already be true in the tenant. The pack should distinguish *solution decisions* from *tenant preconditions*, and should treat a missing precondition as a project deliverable with an owner and a cost.
- Useful technology-neutral signals for Discovery: `dedicated_environment_required`, `enforced_controls_required`, `maker_population_size`, `ownership_model_unclear`, `support_model_unclear`, `external_audience`, `regional_separation_required`, `existing_estate_unknown`.
- Two findings are **dated commitments** and belong in a tripwire, not a static rule: the February 2027 licence enforcement (GOV-11) and the February 2026 automatic conversion of pipeline targets to managed environments (`alm-devops.md` ALM-10).
- One finding invalidates prior art: the CoE Starter Kit deprecation (GOV-12). Any pack content or engagement recommendation citing the kit needs an explicit review.

---

## 11. Source register

Kind: fetched (retrieved 2026-09-03, `ms.date` shown) / search-verified / signals (T3/T4).

| Id | Tier | Kind | Title | URL | ms.date |
|---|---|---|---|---|---|
| G-01 | T1 | fetched | Develop a tenant environment strategy to adopt Power Platform at scale | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/environment-strategy | 2026-05-04 |
| G-02 | T1 | fetched | Manage and govern the default Power Platform environment | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/manage-default-environment | 2026-06-23 |
| G-03 | T1 | fetched | Secure the default environment | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/secure-default-environment | 2026-08-26 |
| G-04 | T1 | fetched | Environment groups | https://learn.microsoft.com/en-us/power-platform/admin/environment-groups | 2025-07-28 |
| G-05 | T1 | fetched | Power Platform governance overview and strategy | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/admin-best-practices | 2026-08-22 |
| G-06 | T1 | fetched | Manage Power Platform adoption at scale (govern at scale) | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/govern-at-scale | 2025-09-02 |
| G-07 | T1 | fetched | Implement reactive governance controls (incl. ME vs CoE comparison) | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/reactive-governance | 2025-08-18 |
| G-08 | T1 | fetched | Control environment creation and management | https://learn.microsoft.com/en-us/power-platform/admin/control-environment-creation | 2024-04-17 |
| G-09 | T1 | fetched | CoE Starter Kit transition to Power Platform admin center (deprecation) | https://learn.microsoft.com/en-us/power-platform/guidance/coe/starter-kit | 2026-05-07 |
| G-10 | T1 | fetched | Managed environments overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview | 2026-02-23 |
| G-11 | T1 | fetched | Licensing requirements for managed environments | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-licensing | 2026-08-31 |
| G-12 | T1 | fetched | Limit sharing (managed environments) | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-sharing-limits | 2026-03-02 |
| G-13 | T1 | fetched | Data policies | https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention | 2026-04-07 |
| G-14 | T1 | fetched | Connector classification | https://learn.microsoft.com/en-us/power-platform/admin/dlp-connector-classification | 2026-04-07 |
| G-15 | T1 | fetched | Implement a data policy strategy | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/dlp-strategy | 2025-08-29 |
| G-16 | T1 | fetched | Combined effect of multiple data policies | https://learn.microsoft.com/en-us/power-platform/admin/dlp-combined-effect-multiple-policies | 2024-05-03 |
| G-17 | T1 | fetched | Advanced connector policies | https://learn.microsoft.com/en-us/power-platform/admin/advanced-connector-policies | 2026-07-15 |
| G-18 | T1 | fetched | Tenant settings | https://learn.microsoft.com/en-us/power-platform/admin/tenant-settings | 2026-06-23 |
| G-19 | T1 | fetched | Actions overview (Power Platform advisor) | https://learn.microsoft.com/en-us/power-platform/admin/power-platform-advisor | 2025-05-28 |
| G-20 | T1 | fetched | View security recommendations | https://learn.microsoft.com/en-us/power-platform/admin/security-recommendations | 2025-05-28 |
| G-21 | T1 | fetched | Power Platform environments overview | https://learn.microsoft.com/en-us/power-platform/admin/environments-overview | 2026-05-28 |
| G-22 | T1 | fetched | Solution checker enforcement in managed environments | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-solution-checker | 2025-11-24 |
| G-23 | T1 | fetched | Back up and restore environments | https://learn.microsoft.com/en-us/power-platform/admin/backup-restore-environments | 2026-06-23 |
| G-24 | T1 | fetched | Security and governance considerations in Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/governance-considerations | 2026-04-07 |
| G-25 | T1 | fetched | WAF — Operational Excellence checklist (OE:01–OE:11) | https://learn.microsoft.com/en-us/power-platform/well-architected/operational-excellence/checklist | 2025-08-15 |
| G-26 | T1 | fetched | Site visibility in Power Pages (tenant governance controls) | https://learn.microsoft.com/en-us/power-pages/security/site-visibility | 2026-03-17 |
| G-27 | T3/T4 | search-verified (signal) | Independent sprawl/governance cluster (i3solutions; Valorem Reply; vBeyond Digital; ERP Software Blog) | various | 2025–2026 |
| G-28 | T1 | fetched | Control guest access to Power Platform environments | https://learn.microsoft.com/en-us/power-platform/admin/security/guest-access | 2026-03-09 |
| G-29 | T1 | fetched | Control user access to environments with security groups and licenses | https://learn.microsoft.com/en-us/power-platform/admin/control-user-access | 2026-08-26 |

Sibling-file sources cited by their register id: **D-12** (block unmanaged customizations), **S-01/S-35** (security score and recommendations), **SEC-nn** findings in `security.md`, **ALM-nn** findings in `alm-devops.md`.

---

## 12. Cross-area analysis (from the governance side)

### 12.1 GOVERNANCE ↔ SECURITY

1. **Governance is the delivery mechanism for security controls.** IP firewall, CMK, cookie binding, sharing limits, app access control, masking rules and VNet are all managed-environment features (GOV-06). A security requirement therefore arrives as a governance change request with a licence consequence (GOV-11) — and the reverse is also true: a tenant that already runs managed environments can absorb new security requirements cheaply.
2. **Governance decides the blast radius that security must contain.** The environment count and shape (GOV-02) determine what a compromised identity reaches. Environment groups then guarantee that the containment settings are actually applied and cannot be locally overridden (GOV-07).
3. **The default environment is where the two areas collide hardest.** It cannot take a security group, cannot be deleted, has no backup guarantee, and receives every SharePoint-form and Teams-driven artefact by construction (GOV-04, GOV-24). Every documented control for it is a governance action with security intent (GOV-05).
4. **Detection cadence caps security response.** Ownerless apps, oversharing, missing WAF and expiring certificates surface weekly and only for managed environments (GOV-13, GOV-20 of `security.md` numbering SEC-35). A security model that relies on these signals inherits a weekly MTTD.
5. **Governance can create a security gap.** Auto-claim (GOV-18) grants a licence on first app launch; combined with permissive sharing, it converts an access-control question into a self-service action. Sharing limits are the compensating control — and they are forward-looking only (GOV-19).

### 12.2 GOVERNANCE ↔ ALM

1. **Governance sets the release gates that ALM must pass.** Solution-checker enforcement (None/Warn/Block, critical-only blocking) and block-unmanaged-customizations are environment/group settings, not pipeline settings (GOV-20, GOV-15). The pipeline inherits them; a project cannot opt out inside its own pipeline.
2. **Environment strategy *is* the ALM topology.** Development, Shared Development, UAT, Production groups plus a pipeline host is Microsoft's reference (GOV-02) — the same objects that `alm-devops.md` treats as dev/test/prod. Any governance decision about environment count directly changes the promotion path.
3. **ALM tooling now carries a governance prerequisite.** Pipeline target environments must be managed, and from February 2026 Microsoft begins enabling managed environments on pipeline targets automatically (`alm-devops.md` ALM-10). Adopting in-product ALM therefore triggers the managed-environment licence discussion (GOV-11).
4. **Governance supplies the identity that ALM deploys with.** Delegated deployments (service principal or stage owner) with approvals are how separation of duties is enforced (`alm-devops.md` ALM-11) — but who owns that service principal, who approves, and who may configure the stage is a governance decision.
5. **The two deprecations move together.** The CoE Starter Kit (GOV-12) and the ALM Accelerator (`alm-devops.md` ALM-22) were the community answer to governance and ALM gaps; both are now unmaintained, and both point at in-product replacements (PPAC; pipelines + Git integration). An organisation running either is carrying debt in both areas simultaneously.
6. **Ownership crosses both.** Deployed objects are owned by the deploying identity (`alm-devops.md` ALM-20), which is exactly the ownership record the governance layer later audits (GOV-14). Getting the deployment identity right is what prevents the ownerless-app backlog.

---

## 13. Summary

Power Platform governance is enforced by seven configurable levers, six of them preventive and mostly gated behind managed environments, and one detective and inherently lagging. The controlling facts for architecture are: **(1)** the environment is simultaneously the security boundary, the governance unit, the DLP scope, the residency unit and the licence unit — so environment topology is the single most consequential governance decision; **(2)** nearly every enforceable control requires managed environments, which requires a premium licence for every active user of that environment, with app-open enforcement dated February 2027 — governance capability has a hard, quantifiable price; **(3)** the default environment is ungovernable by design (no security group, no backup guarantee, everyone a maker) and receives Teams- and SharePoint-driven artefacts automatically, so securing it is a workstream, not a setting; **(4)** data policies must be few and centrally managed, because multiple policies fragment the connector space combinatorially and environment policies cannot override tenant policies; **(5)** ownership, support and retirement are organisational processes with platform *detection* only — the platform will tell you an app has no owner, weekly, and only in managed environments.

Two changes during the research window matter more than any single control: Microsoft's governance capability has moved in-product (Inventory, Usage, Monitor, Actions, APIs) and the CoE Starter Kit is no longer maintained. Any governance design — and any pack content — that assumes the Starter Kit as its backbone is now building on an unmaintained foundation.

---

## 14. Cross-Block V2 reconciliation

### GOV-XB-01 — Hybrid and enterprise-boundary patterns require governance outside Power Platform
- **Classification:** DECISION CRITERION + PATTERN
- **Origin:** MS + INF
- **Evidence:** Azure Architecture Center defines management/governance as including monitoring, auditing, security/business compliance, backup/DR, sensitive-data protection and efficient operations; Azure Well-Architected service guidance for API Management and Functions adds RBAC, Azure Policy, pipeline protection, observability and safe deployment. These responsibilities are outside Power Platform DLP/environment groups.
- **Decision impact:** AP-02/AP-04/AP-05/AP-08/AP-10 are not production-ready until the external resources have: a named owning team; inventory/tags; RBAC and privileged-access model; policy/security baseline; budget/cost owner; CI/CD/IaC owner; monitoring/alert ownership; backup/DR position; and incident route. If no team accepts these responsibilities, the pattern is unavailable (`architecture-patterns.md` Y-13).
- **Sources:** `integration-architecture.md` §15; `https://learn.microsoft.com/en-us/azure/architecture/guide/management-governance/management-governance-get-started`; `https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-api-management`; `https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-functions`.

### GOV-XB-02 — Existing enterprise integration capability is a governance decision before a product decision
- **Classification:** DECISION CRITERION
- **Origin:** INF, supported by enterprise-governance guidance
- **Finding:** if an organisation already has an API/event/integration platform with a published contract and owning team, a project-local APIM/broker/worker stack duplicates governance and creates split ownership.
- **Decision impact:** ask whether the enterprise capability already satisfies the required protocol, security, reliability, latency and ownership model before creating a new boundary. Reuse is not automatic: an incumbent that cannot meet the requirements remains unsuitable.
- **Links:** `integration-architecture.md` §12.1; `architecture-patterns.md` Y-12/Y-13 and AP-10.

### GOV-XB-03 — Security controls and managed environments are also cost-governance decisions
- **Classification:** TRADE-OFF + VOLATILE VALUE
- **Origin:** MS / MS-L
- **Finding:** managed-environment controls and advanced security features can change the licence population materially. `licensing-cost.md` LC-30 now owns the economic model; governance owns the policy decision and must not recommend broad enablement without identifying affected populations and funding.
- **Decision impact:** environment grouping, default-environment hardening, IP firewall/CMK/VNet and managed-environment rollout require an explicit cost owner and revalidation of licensing at implementation/renewal.

### GOV-XB-04 — Compensation, replay and restore need governance ownership
- **Classification:** RECOMMENDATION
- **Origin:** INF over IA/OP evidence
- **Finding:** synchronization failures and restore-induced divergence create business decisions, not merely technical queues.
- **Decision impact:** name (1) system/field authority, (2) who may replay/compensate, (3) who approves manual conflict resolution, and (4) who signs off reconciliation after restore. A replicated or dual-write design without those owners is not governed enough for business-critical use.

