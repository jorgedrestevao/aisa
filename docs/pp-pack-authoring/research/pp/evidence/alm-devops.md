Research Status: CANONICAL
Research Confidence: MEDIUM
Gate: PASS — Cross-Block Gate Recheck
Canonicalization Basis: Cross-Block Gate Recheck
Canonicalized: 2026-09-03

# ALM / DevOps — Research Evidence

Research area: **08 — ALM / DevOps** (`../research-areas.md`). Block B, area 3 of 3.
Draft date: **2026-09-03**. Sibling documents of the same block: `security.md` (area 06), `governance.md` (area 07). Cross-references to the validated foundational Areas 1–4 use the canonical files `platform-suitability.md` (**PS-nn**), `application-architecture.md` (**AA-nn**), `automation-architecture.md`, `data-architecture.md`.
Source policy: `../source-policy.md`.

**Purpose.** Answer: *"What delivery lifecycle does this solution require, what does the platform provide natively, where does it stop, and which requirements force the step up from basic ALM to enterprise ALM?"* Not a tooling tour: a capability appears only where it changes the delivery plan, the environment topology, the identity model, or the recoverability of production.

**Provenance rule.** Sources are **fetched** (retrieved 2026-09-03, `ms.date` read from page metadata — the default), **search-verified**, or **T3/T4 signals**. Findings that rely solely on a search-verified or T3/T4 source are capped at MEDIUM and LOW respectively.

**Origin tags.** **Origin:** MS / INF / T3 / T4 / UNKNOWN. Cross-Block V2 uses **VOLATILE VALUE** alongside the source-policy classifications for date-sensitive ALM capability states, pipeline behaviour, deprecations and licence prerequisites.

**Overall confidence MEDIUM (self-assessed, no gate).** The cap reflects: (a) two of the three community ALM assets are now deprecated (ALM Accelerator, CoE Starter Kit), which invalidates a large body of circulating guidance; (b) the automated-testing story has no supported first-party low-code option after the Test Engine deprecation (cross-referenced from Block A) — the gap is documented but the replacement practice is not; (c) pipelines are evolving quickly and several documented limitations are explicitly temporary ("Not currently", "but planned"); (d) no adversarial review or gate has been run.

**Volatility.** Pipelines, Dataverse Git integration, delegated deployments, block-unmanaged-customizations and solution-checker enforcement all changed within the research window; the February 2026 automatic conversion of pipeline targets to managed environments is a dated commitment. Re-verify §9 before encoding.

---

## 1. The ALM ladder (what each rung buys and costs)

Power Platform does not have one ALM model; it has four rungs that differ in who can operate them, what they guarantee, and what they cost. Almost every ALM decision is a choice of rung.

| Rung | Mechanism | Guarantees | Prerequisites | Does **not** give you | Findings |
|---|---|---|---|---|---|
| 0 | **No solutions** — build in the default solution, edit in place | Nothing | None | Portability, layering, rollback, audit | ALM-02, ALM-05 |
| 1 | **Manual solution export/import**, managed to test/prod | Layering, portability, a managed production estate | Discipline; a publisher; separate environments | Automation, traceability, approvals, gate enforcement | ALM-01..ALM-08 |
| 2 | **Pipelines in Power Platform** | Automated promotion, artefact immutability across stages, connection/environment-variable handling, run history, optional approvals and delegated identity | Managed environments for targets; a host environment; premium licences | Source control (unless combined with Git), multi-solution deploys, cross-tenant, per-developer isolation, choice of import behaviour | ALM-10, ALM-11 |
| 3 | **Source-controlled ALM** — Dataverse Git integration and/or Build Tools / GitHub Actions | Version history, branching, pull requests, code review, code-first components, rehydratable environments, full pipeline control | Git provider; developer environments per maker/branch; pro-dev capability | Automated functional testing (no supported first-party low-code framework) | ALM-09, ALM-12, ALM-17, ALM-22 |

**Consequence (INF):** rungs 2 and 3 are not alternatives — Microsoft's documented position is that Git integration belongs in *developer* environments and pipelines belong in *deployment* ("Use Git integration with developer environments, not in your test or production environments. Use builds to create solution artifacts and pipelines in Power Platform to deploy", D-08). The enterprise pattern is 3-for-source + 2-or-3-for-deploy, not one or the other.

---

## 2. Decision boundaries (requirement → ALM constraint → architectural / delivery consequence)

- Anything that must survive its author → assets must be in a **custom solution with a deliberate publisher**; the publisher owns the component and cannot be changed after a managed import without deleting the component and losing its data → **choose one publisher for the tenant, before the first managed deployment** (ALM-05).
- Production must be protected from ad-hoc change → managed solutions only outside development, plus **block unmanaged customizations** → accept the documented break-list (Field Service, Omnichannel, SLAs, journeys, Copilot Studio publish, and more) and the dataflow exemption (ALM-02, ALM-15).
- More than one person builds at once → unmanaged solutions give **no isolation** ("Every modification is applied directly to the environment, regardless of which solution is being edited") and canvas co-authoring was removed (`application-architecture.md` AA-06) → **one development environment per developer/branch**, which requires source control to reconcile (ALM-06, ALM-09, ALM-23).
- Changes must be reviewable before they reach test → pipelines have approvals but no diff; Git integration provides pull requests and code review → **source control is the requirement that forces rung 3**, not automation (ALM-09, ALM-21).
- Deployments must not be performed by the maker → **delegated deployments** with a service principal, which requires System Administrator in each target ("Lower permission security roles can't deploy plug-ins and other code components") → the deploying identity becomes a governed asset and owns the deployed objects (ALM-11, ALM-20).
- Configuration differs per environment → **environment variables** (definition in the solution, value supplied at deployment) and **connection references** → values must be excluded from the solution; secrets go to Key Vault and are consumable only by flows/agents/custom connectors (ALM-13, ALM-14, `security.md` SEC-07).
- A release must be reversible → **there is no solution rollback**. The options are redeploy a previous solution version (pipelines, if enabled), restore a backup (7 or 28 days, only to sandbox/developer/Teams targets, never directly over production), or fix forward → **rollback strategy must be designed, and the restore path has documented side effects on flows, connections and canvas app IDs** (ALM-18).
- Emergency fix in production → patches are documented but "Using patches isn't recommended"; pipelines deploy the same artefact through the same stages and cannot bypass a stage → **the hotfix path is a normal release with a compressed schedule, or an explicitly governed exception** (ALM-04, ALM-10, ALM-21).
- Multiple applications share components → cross-solution dependencies enforce import order and create upgrade/delete failures → **either one solution, or a base-plus-app layering built with dedicated development environments** (ALM-06).
- Deployment must be tested before production → solution checker is static analysis and "doesn't guarantee that a solution import will be successful"; there is no supported first-party low-code functional test framework after the Test Engine deprecation → **a UAT environment and a manual or Playwright-based regression approach must be budgeted** (ALM-16, ALM-17).
- Environments span regions → solutions cannot be reliably imported into an environment on an *older* service-update station → **development environments must sit in the same or an earlier station than production** (ALM-08).
- The environment might need Dynamics 365 apps later → "It's important to determine at that time if these apps are required or not because **they can't be uninstalled or installed later**" → an irreversible decision at environment creation (ALM-24).

---

## 3. Findings

Ids ALM-nn are stable. Sources in §11.

### 3.1 Foundations

#### ALM-01 — Healthy ALM = separate environments + managed solutions everywhere except development + source control as the source of truth
- **Classification:** RECOMMENDATION (foundational)
- **Origin:** MS
- **Evidence:** "Managed solutions are used to deploy to any environment that isn't a development environment for that solution. This includes test, user acceptance testing (UAT), system integration testing (SIT), and production environments"; "As an ALM best practice, managed solutions should be generated by a build server and considered a build artifact"; "A source control system helps organizations achieve healthy ALM because the assets maintained in the source control system are the '**single source of truth**'" (D-01). Access model by environment purpose, verbatim (D-01): Development — "App users shouldn't have access. Developers require at least the Environment Maker security role"; Test — "App makers, developers, and production app users shouldn't have access"; Production — "**App makers and developers shouldn't have access, or should only have user-level privileges**"; Default — "We strongly recommend that you create environments for a specific purpose". "Except for your development environment, you should only have managed solutions in your environments" (D-04).
- **Decision impact:** the environment topology and the role matrix are ALM artefacts, not infrastructure details. This is also the concrete definition of separation of duties in Power Platform.
- **Confidence:** HIGH.
- **Sources:** D-01, D-04.

#### ALM-02 — Managed vs unmanaged: five consequences that decide production posture
- **Classification:** FACT + RISK
- **Origin:** MS
- **Evidence (D-02):** "You can't edit components directly within a managed solution. To edit managed components, first add them to an unmanaged solution" — and doing so "create[s] a dependency between your unmanaged customizations and the managed solution… the managed solution can't be uninstalled until you remove the dependency". "You can't export a managed solution. But you can export an unmanaged solution as managed." "**You can't import a managed solution into the same environment that contains the originating unmanaged solution.** To test a managed solution, you need a separate environment." "When a managed solution is deleted (uninstalled), all the customizations and extensions included with it are removed." And the critical data warning: "**When you delete a managed solution, the following data is lost: data stored in custom tables that are part of the managed solution and data stored in custom columns that are part of the managed solution on other tables**". Unmanaged deletion is the mirror: "only the solution container… is deleted. All the unmanaged customizations remain in effect and belong to the default solution".
- **Decision impact:** uninstalling a managed solution is a **data-destructive** operation, which makes solution boundaries a data-lifecycle decision. And a managed solution cannot be validated in its own development environment — a test environment is structurally required, not a nicety.
- **Confidence:** HIGH.
- **Sources:** D-02.

#### ALM-03 — Layering: one unmanaged layer sits above everything and defines runtime behaviour
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence (D-03):** "**Unmanaged layer** All imported unmanaged solutions and ad-hoc customizations exist at this layer. **All unmanaged solutions share a single unmanaged layer.**" Managed layers stack in install order, "the last one installed is above the managed solution installed previously"; uninstalling one exposes the layer below; the system layer is at the base. Merge behaviour: "**only model-driven app, form, and site map component types are merged. All other components use 'top level wins' behavior**." Within a managed solution: base → patches → pending upgrade. "**Using patches isn't recommended.**" (D-12): "Unmanaged customizations reside at the top layer for a component and subsequently define the runtime behavior of the component. In most situations, you don't want unmanaged customizations determining the behavior of your components."
- **Decision impact:** an unmanaged layer created by a single production edit permanently overrides every future managed update to that component until it is explicitly removed. This is the mechanism behind environment drift (ALM-19).
- **Confidence:** HIGH.
- **Sources:** D-03, D-12.

#### ALM-04 — Update vs upgrade vs patch have different deletion semantics
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** "Updates to a managed solution are deployed to the previous version… This doesn't create an additional solution layer. **You can't delete components by using an update.**" "A patch contains only the changes for a parent managed solution… **You can't delete components by using a patch.**" "Upgrading a solution installs a new solution layer immediately above the base layer and any existing patches. Applying solution upgrades involves deleting all existing patches and the base layer. **Solution upgrades delete components that existed but are no longer included in the upgraded version**" (D-01, D-02). Staged upgrade ("stage for upgrade") allows actions before completing (D-02, D-03).
- **Decision impact:** removing a component from production requires an *upgrade*, and an upgrade deletes anything absent from the new version — including anything a well-meaning admin added to that solution in the target. Pipelines default to "Upgrade without Overwrite customizations" (ALM-10).
- **Confidence:** HIGH.
- **Sources:** D-01, D-02, D-03.

#### ALM-05 — The publisher is an irreversible ownership decision
- **Classification:** CONSTRAINT (irreversible)
- **Origin:** MS
- **Evidence:** "The publisher of a solution where a component is created is considered the owner of that component… It's possible to move the ownership of a component from one solution to another within the same publisher, but not across publishers. **Once you introduce a publisher for a component in a managed solution, you can't change the publisher for the component.** Because of this restriction, it's best to define a single publisher" (D-02). "When you change a solution publisher prefix, you should do it **before** you create any new apps or metadata items because you can't change the names of metadata items after they're created" (D-02). The cost of getting it wrong, verbatim: "if a custom table is imported as managed through Solution A with Publisher X, you can't later move that table to Solution B with Publisher Y. The only option is to delete the table, upgrade Solution A to remove the table from the target system, then recreate the table in Solution B with Publisher Y and import Solution B. **This process results in loss of all data stored in the custom table unless it's migrated beforehand**" (D-05). Migration warning: "It's important to carefully select the publisher for this unmanaged solution… If you have multiple publishers, now is the time to decide which publisher to use moving forward" (D-04).
- **Decision impact:** publisher choice belongs in the first week of an engagement and is a tenant-level standard, not a project choice.
- **Confidence:** HIGH.
- **Sources:** D-02, D-04, D-05.

#### ALM-06 — Solution organisation: three documented strategies with explicit rules
- **Classification:** PATTERN + DECISION CRITERION
- **Origin:** MS
- **Evidence (D-05):** Strategy A — **single solution**: recommended for "Small-medium scale implementations… where future modularization is unlikely"; downside "When multiple developers work in the same development environment, they risk overwriting each other's changes". Strategy B — **multiple solutions in one development environment**: only for "distinct and independent functional areas that don't share components"; downside "you might encounter a situation where Solution A can't be imported because it depends on Solution B, while Solution B can't be imported because it depends on Solution A"; and "Working in an unmanaged solution doesn't provide isolation. **Every modification is applied directly to the environment, regardless of which solution is being edited.**" Strategy C — **multiple solutions with dedicated development environments**: for "Large-scale enterprise projects… Teams with multiple developers or partners… strict governance and CI/CD"; base managed solution imported into each app development environment; downsides "Higher infrastructure and maintenance overhead… Requires robust environment strategy and governance… More complex deployment". Hard rules: "Don't include the same unmanaged component in more than one solution"; "**Have only one solution that includes all your tables**"; "Use only one solution publisher"; "**Avoid creating dependencies between solutions**", with the worked failure — a flow solution imports successfully but "the flow itself doesn't work" because the dependency on a custom column was not recognised. Documented dependency sources: application ribbons/site maps, plug-ins and cloud flows triggering on custom columns, security roles depending on custom tables.
- **Decision impact:** the number of solutions and the number of development environments are a single coupled decision, driven by team size, release independence and modularity — and the "one solution with tables" rule constrains any modular design.
- **Confidence:** HIGH.
- **Sources:** D-05.

#### ALM-07 — Solutions carry metadata, not data — and not all metadata
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "They include metadata and certain tables with configuration data. **Solutions don't contain any business data.**" "Notice that not all tables can be included in a solution. For example, the Application User, Custom API, and Organization Setting system tables can't be added" (D-01). "A solution can be up to **95 MB** in size" (D-02, repeated in D-15 for environment variables). Pipelines: "Pipelines, or solutions in general, don't contain data stored within Dataverse tables" (D-06).
- **Decision impact:** reference/configuration data needs its own migration mechanism (configuration migration tooling or a data pipeline); application users and org settings must be provisioned per environment outside the solution — as must business units and teams (`security.md` SEC-10, S-02).
- **Confidence:** HIGH.
- **Sources:** D-01, D-02, D-06, D-15.

#### ALM-08 — Environment topology and the service-update station trap
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS
- **Evidence:** "you'll need separate environments for app development and production. Although you can perform basic ALM with only separate development and production environments, we recommend that you also maintain at least one test environment… at a minimum, any healthy ALM practice should include using a test environment prior to deploying anything to the production environment. This ensures that you have a place to test your app, but also ensures that **the deployment itself can be tested**" (D-11). "Separate development environments can be helpful to help isolate changes from one work effort being checked in before it's completed" (D-11). Region/version: "There are six stations in total that are primarily defined by geographical location… **You can import a solution into an environment that is a newer version than the environment where the solution was exported. You can't reliably import a solution into an environment that's an older version**"; worked example — with production in Canada and the US, "your development environments should be in North America (station 5) and not in Canada (station 2)" (D-11).
- **Decision impact:** multi-geography estates must choose development regions deliberately, or accept intermittent import failures that look like product defects.
- **Confidence:** HIGH.
- **Sources:** D-11.

### 3.2 Source control

#### ALM-09 — Dataverse Git integration: native source control, for developer environments only
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence (D-08):** "Source control integration enables development teams to sync solutions and solution objects across one or more Microsoft Dataverse environments by using a supported Git provider, such as Azure DevOps or GitHub"; "**Use Git integration with developer environments, not in your test or production environments. Use builds to create solution artifacts and pipelines in Power Platform to deploy.**" "solutions stored in source control come from unmanaged solutions in a maker's environment… Managed solutions are built from source control and deployed into downstream environments". Benefits claimed: source control as source of truth; SDLC practices (version control, code reviews, static analysis); "**Short-lived dev environments**… you can rehydrate development environments from source control quickly"; fusion teams; recovery "to a previous state or version". Code-first caveat: deploying built artefacts directly into a maker environment and committing them means "you end up with two copies of the object in source control—one represented by the built version and the other represented by the source code… **This practice isn't recommended**"; the recommended approach is to build code-first objects through a solution build process. File format is designed to be human-readable and de-duplicated across solutions in the same folder.
- **Decision impact:** Git integration is the mechanism that makes multi-maker parallel work and environment rehydration possible — and it is explicitly *not* a deployment mechanism.
- **Conditions:** canvas-specific caveats live in the validated foundational Area 2 (`application-architecture.md`): Git version control inside the canvas editor "has been removed and is no longer supported"; commits happen only on publish; `.pa.yaml` cannot be edited directly when the app contains code components; one maker per app/custom page (AA-05, AA-06).
- **Confidence:** HIGH.
- **Sources:** D-08; `application-architecture.md` AA-05, AA-06.

#### ALM-12 — Build Tools and GitHub Actions: the pro-dev pipeline, with identity as the main design point
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence:** Build Tools task categories: helper, quality check, solution, environment management; typical pipelines "Initiate, Export from Dev, Build, and Release"; "Microsoft Power Platform Build Tools are supported only for a Microsoft Dataverse environment with a database"; "available for use in **GCC** and **GCC High**"; v2.0 is CLI-based and is "the version that Microsoft services and adds newer features to", while v1.0 is PowerShell-based and receives "critical security updates as needed"; "**You can't mix and match task versions**". Connection types: "Service Principal via Workload Identity Federation (**recommended**)… Service principal and client secret… Username/password: **Does not support users requiring multi-factor authentication**". Service-principal setup via `pac admin create-service-principal`, default role System Administrator, with "Keep the client secret safe and secure. Once the command prompt is cleared, you can't retrieve the same client secret again" (D-09). GitHub Actions provide the same four task categories, run on Windows and Linux runners, require a Dataverse environment with a database, and offer the same two connection types (D-10). Checker output is SARIF (D-09).
- **Decision impact:** the deployment identity is the first design decision of a pro-dev pipeline, and username/password service connections are incompatible with an MFA-enforced tenant — which most enterprise tenants are.
- **Confidence:** HIGH.
- **Sources:** D-09, D-10.

### 3.3 Deployment

#### ALM-10 — Pipelines in Power Platform: what they guarantee, and fourteen documented limits
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence — capability (D-06):** "Pipelines deploy solutions as well as configuration for the target environment such as connections, connection references, and environment variables"; prevalidation against the target "to prevent mistakes and improve success rates… missing dependencies and other issues are detected before deployment"; "Both managed and unmanaged solutions are automatically exported and stored in the pipelines host for every deployment"; artefact integrity — "Solutions are exported as soon as a deployment request is submitted… **the same solution artifact must pass through pipeline stages in sequential order. The system also prevents any tampering or modification to the exported solution artifact. This ensures customization can't bypass QA environments or your approval processes**"; layer diffs are visible in the target, with XML diffs for model-driven apps, site maps and forms; CLI support via `pac pipeline`; extensibility hooks.
- **Evidence — limits (D-06 unless noted):** (1) "All other environments used in pipelines must be enabled as managed environments. Licenses granting premium use rights are required for all managed environments"; the host "should be a production environment, but… doesn't have to be a managed environment"; development environments may be Developer-plan. (2) "**Starting February 2026, Microsoft will start enabling managed environments for any pipeline target environments that aren't already enabled.**" (3) "Power BI Dashboards (preview) and Power BI Datasets (preview) are not currently supported". (4) "Can pipelines deploy to a different tenant? **No.**" (5) Cross-geo only if "Cross-Geo Solution Deployments" is enabled in the host. (6) "Can I deploy unmanaged solutions? **No.**" (7) "Can I deploy multiple solutions at once? **Not currently.**" (8) "Can I specify advanced solution import behaviors such as update versus upgrade? **Not currently. Pipelines default import behavior is *Upgrade* without *Overwrite customizations*.**" (9) "Do pipelines publish unmanaged customizations before exporting the solution? **Not currently.**" (10) "**The current implementation uses a single development environment for a given solution**" — i.e. no isolated multi-developer flow. (11) "Currently, connection references without a value in the solution or targeted environment can't be updated during deployment." (12) "Pipelines can't be viewed or run from the default solution, managed solutions, or in target environments." (13) "Can an environment be associated with multiple hosts? **No.**" (14) "Can I customize or extend the first-party deployment pipeline app and tables? **Not currently**", though extension hooks exist. Rollback: "If the pipeline setting is enabled, you can redeploy previous solution versions… If the setting is disabled, only higher solution versions can be deployed"; the workaround is downloading the artefact, incrementing `solution.xml` and importing manually. Ownership: "**Who owns deployed solution objects? The deploying identity.**"
- **Decision impact:** pipelines give the two things manual promotion cannot — artefact immutability across stages and prevalidated configuration — at the price of managed environments everywhere downstream and a fixed import behaviour. The single-development-environment constraint is the reason enterprises still combine pipelines with Git.
- **Confidence:** HIGH.
- **Sources:** D-06.

#### ALM-11 — Delegated deployments are the platform's separation-of-duties mechanism
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence (D-07):** "When you enable this feature, the pipeline stage deploys as the delegate (service principal or pipeline stage owner) **instead of the requesting maker**." Service-principal prerequisites: Cloud Application Administrator or Application Administrator in Entra; "**You must be an owner of the enterprise application (service principal) in Microsoft Entra ID**"; the SPN is added as an S2S user in the host and each target; "Assign the Deployment Pipeline Administrator security role… within the pipelines host, and **System Administrator security role within target environments. Lower permission security roles can't deploy plug-ins and other code components.**" Approvals: an `OnApprovalStarted` cloud flow in the host calls the Dataverse unbound action `UpdateApprovalStatus` (20 = approved, 30 = rejected) using the delegate's own connection; "All delegated deployments are pending until approved." Sharing during deployment: "Pipelines assign the minimum privileges required to run apps and flows"; "**Sharing is available the first time an object is deployed… You can't update sharing when new versions are deployed**"; "Can makers share with individual users? **Not currently.**" Stage-owner delegation: "you **can't** deploy solutions containing connection references for OAuth connections"; "For security reasons, you must sign in as the user that you set as the pipeline stage owner." Warning to approvers: "Deployment approvers are responsible for carefully reviewing sharing and security role information. When a deployment is approved, pipelines automatically assigns permissions using the deploying service principal's identity."
- **Decision impact:** a real separation of duties is achievable in-product, but it *requires* granting System Administrator to a service principal in production. The control is therefore "no human has standing production rights", not "nothing has production rights".
- **Confidence:** HIGH.
- **Sources:** D-07.

#### ALM-13 — Environment variables: the sanctioned configuration mechanism, with six limits
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence (D-15):** Types: Decimal number, Text, JSON, Two options, Data source, Secret. Definition vs value: "**A value can't exist without a definition**"; default value lives on the definition, current value on the value record; "A defined value is used even if a default value is also present". ALM guidance verbatim: "**Should I include the value in my solution? No.** Environment variables are intended to be used by applications that need to have different values in different environments… the values should be provided for the target environment during deployment." Import experience prompts for variables without a value. Limits: "Environment variables are limited to a maximum of **2,000 characters**"; "**Power Platform Build Tools tasks aren't yet available for managing data source environment variables**"; "Validation of environment variable values happens within the user interfaces and within the components that use them, **but not within Dataverse**"; "Interacting with environment variables via custom code requires an API call to fetch the values; there isn't a cache exposed"; "It might take up to an **hour** to fully publish updated environment variables because the value is pushed into the apps and flows asynchronously"; "If the environment variable is in a managed solution, you won't be able to see the value unless you look inside of the **Default solution**… since the environment variable value is an unmanaged customization". SharePoint caveat: display and logical names must match, and "SharePoint has internal identifiers that might not match between target environments". Names `$authentication` and `$connection` are reserved and block flow save. Security: the definition table is user/team owned and included in Environment Maker and Basic User roles by default.
- **Decision impact:** configuration externalisation works, but the propagation delay, the absence of Dataverse-side validation and the SharePoint identifier mismatch are all live sources of "it worked in dev" incidents.
- **Confidence:** HIGH.
- **Sources:** D-15.

#### ALM-14 — Connection references: the deployment-time binding, with four documented failure modes
- **Classification:** CONSTRAINT + RISK
- **Origin:** MS
- **Evidence (D-16):** "During solution import into a target environment, a connection is provided for all the connection references so any referencing flows can be turned on automatically." Asymmetry: "**Flows use connection references for all connectors, whereas canvas apps only use them for implicitly shared (non-OAuth) connections**"; "Canvas apps and flows added from outside solutions will not automatically be upgraded to use connection references"; "Connection references get associated with canvas apps only at the time a data source is added to the app." Failure modes: (1) "**Canvas apps don't recognize connection references on custom connectors.** To work around this limitation, after a solution is imported… the app must be edited to remove and then readd the custom connector connection. Note, if this app is in a managed solution, proceeding to edit the app will create an unmanaged layer." (2) "**Copy environment breaks connection references for custom connectors**" — a new connection reference must be created. (3) "**Custom connectors need to be imported in a separate solution from their connection references**", before connection references or flows. (4) Flow enablement requires connection ownership or explicit sharing; `ConnectionAuthorizationFailed` otherwise. Ownership of a connection reference cannot be transferred from the modern Solutions area.
- **Decision impact:** custom connectors materially complicate ALM; the documented workaround for canvas apps deliberately creates an unmanaged layer in a managed solution — i.e. the fix breaks the production-integrity rule (ALM-03, ALM-15).
- **Confidence:** HIGH.
- **Sources:** D-16.

#### ALM-15 — Block unmanaged customizations: the strongest production-integrity control, with a real break-list
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS
- **Evidence (D-12, ms.date 2026-09-02):** Blocked when enabled: "Import of unmanaged solutions into the environment is blocked"; "Creation of new solution components like apps, tables, and forms are blocked"; "Adding unmanaged changes to existing managed components are blocked"; the user-facing error is quoted. Still allowed: changing environment variables; enabling/disabling components (turning flows on/off, assigning ownership, sharing records); removing an unmanaged layer; creating and exporting unmanaged solutions; reviewing flow run history; running a flow to test it. Exemption: "**Dataflows require unmanaged customizations, so they're allowed… Dataflows will continue to create unmanaged layers in the environment even with the setting enabled.**" Default is disabled. Known limitations (each breaks with the same error): Dynamics 365 Resource Scheduling Optimization install/upgrade; automatic record creation; legacy workflows enable/disable; Field Service enhanced autonumbering; Connected Field Service install; Field Service Mobile geofencing; Resource Scheduling table enablement; Sales Accelerator configuration; **Customer Insights - Journeys** (journeys, triggers, emails, forms, SMS, push cannot be created or published); Omnichannel install/upgrade; SLA activation/deactivation/editing; file attachments to appointments or emails via `activitymimeattachment`; work-queue items; **Copilot Studio agent publishing**. Microsoft's guidance: "If you must use one of the below apps or features… we recommend you disable the setting."
- **Decision impact:** for a pure Power Platform workload this is close to free and highly valuable. For a Dynamics 365 or Copilot Studio workload it may be unusable — which is itself a fit signal.
- **Confidence:** HIGH.
- **Sources:** D-12.

### 3.4 Quality, testing and release governance

#### ALM-16 — Solution checker: static analysis with an explicitly limited promise
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "Solution checker works with unmanaged solutions that can be exported from an environment." Analysed components: "Dataverse custom workflow activities; Dataverse web resources (HTML and JavaScript); Dataverse configurations, such as SDK message steps; Power Automate flows (via flow checker); Power Fx expressions (via app checker)". Limit, verbatim: "**Use of solution checker doesn't guarantee that a solution import will be successful. The static analysis checks performed against the solution don't know the configured state of the destination environment**". Severities Critical/High/Medium/Low/Informational; categories include Performance, Maintainability, Usage, Supportability, Design, Security, Accessibility, Upgrade readiness, Licensing. Managed and non-Microsoft managed solutions cannot be analysed ("Checked by Microsoft"/"Checked by Publisher"). Rules can be run locally for web resources via `@microsoft/eslint-plugin-power-apps` (D-14). Enforcement: None/Warn/Block; "**only critical severity rules block a solution from being imported**"; rule exclusions supported; unavailable in Administration mode; emails to Power Platform/Dynamics 365 admins and weekly-digest recipients (D-13).
- **Decision impact:** solution checker is a code-quality gate, not a test. Treating a green check as release evidence is a category error.
- **Confidence:** HIGH.
- **Sources:** D-13, D-14.

#### ALM-17 — Automated testing is the weakest link in the platform's lifecycle story
- **Classification:** RISK (negative evidence)
- **Origin:** MS (deprecation) + INF (consequence)
- **Evidence:** From validated foundational Area 2 (`application-architecture.md` AA-08, source V-07, 2026-05-22 upd. 2026-08-14): "**Effective April 2026, Test Engine is deprecated. The documentation and GitHub repository are no longer maintained by Microsoft**"; reason given: "near-zero usage and failed to meet customer needs… The Power Fx implementation created unnecessary limitations that are avoided if using Playwright directly"; the stated migration path is "the Power Platform Playwright samples". Within this block: solution checker is explicitly not a test (ALM-16); pipelines provide prevalidation of dependencies and configuration but no functional testing (ALM-10); Build Tools/GitHub Actions expose a "quality check" task category that is the checker, not tests (D-09, D-10); the documented ALM environment guidance requires a test environment for "end-to-end validation that includes solution deployment and application testing" (D-11), i.e. manual by default.
- **Decision impact:** any requirement for automated regression testing forces pro-dev capability (Playwright, custom harnesses) and a budget line. For a citizen-developed estate the honest position is: manual UAT plus static analysis, with regression risk rising with change velocity — which is itself an argument for smaller solutions and shorter release cycles.
- **Conditions:** unit testing of plug-ins/custom code follows normal .NET practice and is out of scope of the platform's own tooling; not researched here (ALM-U-04).
- **Confidence:** HIGH (deprecation) / MEDIUM (consequence framing).
- **Sources:** D-09, D-10, D-11, D-13, D-14; `application-architecture.md` AA-08.

#### ALM-18 — There is no rollback; there are three imperfect recovery paths
- **Classification:** RISK + DECISION CRITERION
- **Origin:** MS
- **Evidence:** Path 1 — redeploy a previous solution version through pipelines, only "if the pipeline setting is enabled"; otherwise "only higher solution versions can be deployed or imported", with the manual `solution.xml` workaround (D-06). Path 2 — restore a backup (D-17): system backups are continuous with **7-day** default retention (production managed environments up to **28**); "**You can't directly restore backups to production environments.** To restore a backup to a production environment, first change the environment type to sandbox, perform the restore, and then switch the environment type back"; source→target matrix (Production→Sandbox; Sandbox→Sandbox; Developer→Sandbox/Developer; Teams→Teams; Default→Developer); "You must restore an environment in the same region"; "**You can restore a managed environment only to another managed environment**"; CMK and enterprise-policy (VNet) parity required; restore needs 1 GB free capacity; "**Backup and restore operations include only apps… and flows… in a Dataverse solution**". Documented post-restore effects: "existing solution flows are deleted, but existing nonsolution flows remain… **Solution flows are turned off**"; "**Connection references require new connections**"; "Review custom connectors and, as required, **delete and reinstall them**"; "**apps shared with Everyone aren't shared with Everyone in the restored environment**"; "the app ID for a canvas app in a restored environment differs"; the environment lands in administration mode. Path 3 — fix forward, constrained by ALM-04 (only an upgrade can delete components) and by pipelines' fixed import behaviour (ALM-10). Additional: "You can't get a copy of your database backup"; deleted environments recoverable within 7 days (28 for production with Dynamics 365 apps).
- **Decision impact:** "we can roll back" is false unless a specific mechanism has been designed and rehearsed. Restore is an environment-level, disruptive, side-effect-laden operation — not a release-level undo. This should be stated to sponsors before go-live, not during an incident.
- **Confidence:** HIGH.
- **Sources:** D-06, D-17.

#### ALM-19 — Environment drift: how it happens, how it is detected, how it is prevented
- **Classification:** ANTI-PATTERN + PATTERN
- **Origin:** MS
- **Evidence:** Mechanism — any ad-hoc change creates an unmanaged layer that defines runtime behaviour and shadows future managed updates (ALM-03, D-12). Detection — "**Check if there are any components with an active layer.** If you find any, it might be because you missed including them in the unmanaged solution in your development environment" (D-04); "To see if a managed component has been customized, look for an unmanaged layer that appears above the base managed layer" (D-04); pipelines expose layer diffs in the target (D-06). Prevention — block unmanaged customizations (D-12); environment group rules that lock settings and "prevent issues such as **configuration drift**" (D-21); managed-solutions-only downstream (D-04). Configuration drift also arises outside solutions: business units and teams "must be created and managed in each environment" (`security.md` S-02), and modernised-BU owning-BU values must exist in the target or synchronisation fails with a foreign-key violation (`security.md` SEC-10).
- **Decision impact:** drift control is two workstreams — solution-layer discipline (ALM) and environment-configuration discipline (governance). Neither alone is sufficient.
- **Confidence:** HIGH.
- **Sources:** D-04, D-06, D-12, D-21; `security.md` SEC-10.

#### ALM-20 — Deployment creates ownership; ownership creates the runtime identity
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "Who owns deployed solution objects? **The deploying identity.** For standard deployments, the owner is the requesting maker. For delegated deployments, the owner is the delegated service principal or user" (D-06, repeated in D-07). Flows run under their connection owner and can only be enabled by someone owning or permitted on every connection (`security.md` SEC-21); OAuth connections can be explicitly shared only with a user representing a service principal (`security.md` SEC-21).
- **Decision impact:** without delegated deployment, production automations end up owned by whichever maker pressed Deploy — the precise condition that later produces ownerless applications (`governance.md` GOV-14).
- **Confidence:** HIGH.
- **Sources:** D-06, D-07.

#### ALM-21 — Release governance: what is auditable in-product, and what must be built
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence:** In-product: pipeline run history and analytics ("Customizations and audit log saved automatically and are easily accessible"; out-of-the-box Power BI reports), artefact immutability and sequential stages, approvals via the `OnApprovalStarted` extension point, delegated identity, and retention control through Dataverse bulk-delete jobs in the host (D-06, D-07). Not in-product: change advisory records, release notes, links to work items, emergency-change procedure, and any approval taxonomy beyond what the extension flow implements. Azure DevOps/GitHub supply those natively when rung 3 is used (D-09, D-10). WAF operational excellence frames the expectations: "**Build a workload supply chain that drives proposed changes through predictable, automated pipelines**" (OE:05); "**Clearly define your workload's safe deployment practices**… Account for routine deployments and emergency, or hotfix, deployments" (OE:10); "**Implement a deployment failure mitigation strategy**… Combine multiple approaches, such as rollback, feature disablement, or using your deployment pattern's native capabilities" (OE:11) (D-20).
- **Decision impact:** traceability from requirement → change → release exists only if the team runs rung 3 or builds it around pipelines. OE:11 is the checklist item that ALM-18 shows is hardest to satisfy on this platform.
- **Confidence:** HIGH.
- **Sources:** D-06, D-07, D-09, D-10, D-20.

#### ALM-22 — Tooling choice: pipelines vs Build Tools/GitHub vs ALM Accelerator (deprecated)
- **Classification:** DECISION CRITERION + FACT
- **Origin:** MS
- **Evidence:** Deprecation, verbatim: "**The ALM Accelerator is deprecated and no new features are being added. Issues are no longer reviewed or addressed.** … Use Pipelines in Power Platform to bring ALM automation capabilities… Pipelines can be used with source code integration or extended to integrate with Azure DevOps, GitHub, and other providers" (D-19). The comparison table from the same (now-deprecated) page remains the clearest published framing: *IT/developer involvement* — Pipelines: not required; Accelerator: up-front setup; DevOps/GitHub: required for every project. *Source code integration* — Pipelines: "No, but planned"; the other two: yes. *Maker requires elevated privileges in target* — all three: no, service principal supported. *Democratized for citizen development* — Pipelines yes; Accelerator yes; DevOps/GitHub no. *Support* — Pipelines and DevOps/GitHub Microsoft-supported; Accelerator "Power CAT-supported through GitHub issues". *Code-first development* — Pipelines "No, but planned"; others yes. Positioning: "Generally, you would choose Pipelines if your organization doesn't need to control your solutions' source code files and wants to get started with ALM quickly"; "you would choose Build Tools if your organization has DevOps or GitHub and developer resources available and requires granular control" (D-19). Pipelines' own guidance: "We encourage customers to use pipelines for core deployment functionality, and when needed, extend pipelines to integrate with other CI/CD tools" (D-06).
- **Decision impact:** the decision is between rung 2 (pipelines), rung 3 (Build Tools/GitHub, optionally with native Git integration), and the hybrid Microsoft now recommends. The Accelerator is no longer a valid recommendation. Note the table predates native Dataverse Git integration, which partially closes the "source code integration: No, but planned" row (D-08).
- **Conditions:** table `ms.date` 2024-04-09 (page updated 2026-07-13) — the capability comparison is stale in at least that one row.
- **Confidence:** HIGH (deprecation) / MEDIUM (comparison rows).
- **Sources:** D-06, D-08, D-19.

#### ALM-23 — Multi-developer isolation is achievable only at rung 3
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** Pipelines: "The current implementation uses a single development environment for a given solution" (D-06). Unmanaged solutions in a shared development environment: "Working in an unmanaged solution doesn't provide isolation. Every modification is applied directly to the environment" (D-05). Canvas apps: real-time co-authoring "has been removed and is no longer supported"; "one maker can edit one custom page at a time" (`application-architecture.md` AA-06). Git integration explicitly enables "Fusion development teams… build independently in separate environments and collaborate with others by syncing with a common source control repository" and "short-lived dev environments" (D-08). Solution-organisation strategy C pairs dedicated development environments with a base/app layering (D-05). Team-development guidance: "**We recommend that you avoid situations where multiple people make changes to complex components—such as forms, flows, and canvas apps—at the same time**" (D-01).
- **Decision impact:** team size is a direct input to the ALM rung. Two or more makers on the same artefact requires environment-per-developer plus Git; anything less is a serialisation agreement enforced by humans.
- **Confidence:** HIGH.
- **Sources:** D-01, D-05, D-06, D-08; `application-architecture.md` AA-06.

#### ALM-24 — Two environment-creation choices are irreversible and belong to the ALM plan
- **Classification:** CONSTRAINT (irreversible)
- **Origin:** MS
- **Evidence:** "When you create an environment, you can choose to install Dynamics 365 apps… **It's important to determine at that time if these apps are required or not because they can't be uninstalled or installed later.** If you aren't building on these apps and will not require them in the future, we recommend that you not install them in your environments. This helps avoid dependency complications when you distribute solutions between environments" (D-01). Also: the environment's region is set at creation and constrains service-update station alignment (ALM-08), CMK enterprise-policy region matching (`security.md` SEC-29) and VNet region pairing (`security.md` SEC-30).
- **Decision impact:** environment provisioning is a design act with permanent consequences; it should be scripted and reviewed, not performed ad hoc (which is also why environment-creation control is a governance prerequisite — `governance.md` GOV-09).
- **Confidence:** HIGH.
- **Sources:** D-01.

#### ALM-25 — Licensing shapes the pipeline topology
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** Pipelines' own worked example (D-06): Host — Production, standalone licence **not** required; Development — Developer, not required; QA — Developer, not required; Production — Production, **required**. But: "All other environments used in pipelines must be enabled as managed environments. Licenses granting premium use rights are required for all managed environments" (D-06), and "Managed environment isn't included as an entitlement in the Developer Plan when users run their assets" (D-18, D-22). Managed-environment licence enforcement blocks app opening from February 2027 (D-22).
- **Decision impact:** the cheap topology (Developer-plan dev and QA environments) works only while those environments are used for building and testing by their owners; the moment real users run apps there, the licence rules bite.
- **Conditions:** the interaction between "pipeline targets must be managed" and "Developer-plan QA is licence-free" is documented as a worked example but is easy to over-read; verify before encoding (ALM-U-05).
- **Confidence:** MEDIUM.
- **Sources:** D-06, D-18, D-22.

---

## 4. ALM decision criteria (REQUIREMENT → ALM CONSTRAINT → ARCHITECTURAL / DELIVERY CONSEQUENCE)

| # | Requirement | ALM constraint (evidence) | Consequence — and the rung it forces |
|---|---|---|---|
| 1 | Anything beyond a personal tool | Unmanaged/default-solution work is not portable and is data-destructive to unwind (ALM-02, ALM-05) | Custom solution + single publisher from day one → **rung 1 minimum** |
| 2 | Protect production from ad-hoc edits | Unmanaged layer overrides managed behaviour permanently (ALM-03) | Managed-only downstream + block unmanaged customizations, accepting the break-list → rung 1–2 |
| 3 | Two or more makers | No isolation inside an environment; canvas co-authoring removed (ALM-23) | Environment per developer/branch + Git → **rung 3** |
| 4 | Reviewed changes / pull requests | Pipelines have approvals but no code review (ALM-10, ALM-21) | Dataverse Git integration or Build Tools/GitHub → **rung 3** |
| 5 | Automated promotion with an audit trail | Manual export/import has no traceability or artefact integrity (ALM-10) | Pipelines (targets must be managed) → **rung 2** |
| 6 | Makers must not deploy | Delegated deployments; SPN needs System Administrator in targets (ALM-11) | Governed service principal + approval flow → rung 2/3 |
| 7 | Different configuration per environment | Values must not travel in the solution; secrets are Key Vault-only and consumable by three component types (ALM-13; `security.md` SEC-07) | Environment variables + connection references designed in; deployment settings per environment |
| 8 | Custom connectors in the solution | Separate solution, import order, canvas apps don't recognise connection references, copy breaks them (ALM-14) | Extra solution + a documented post-deployment step; expect an unmanaged layer in the canvas workaround |
| 8a | Custom connector used by AP-02/AP-05/AP-08/AP-10 | The seam crosses into an external API lifecycle and the documented canvas workaround can create an unmanaged layer | Treat connector + API contract as one release boundary. If `block unmanaged customizations` is mandatory and the consumer needs the workaround, redesign the seam rather than waive production integrity silently |
| 9 | Reversible releases | No rollback; restore is disruptive and side-effect-laden (ALM-18) | Explicit strategy: version redeploy, restore drill, or fix-forward — rehearsed before go-live |
| 10 | Emergency fixes | Patches discouraged; pipelines cannot bypass stages (ALM-04, ALM-10) | A compressed but identical release path, or a governed exception with a named approver |
| 11 | Automated regression testing | No supported first-party low-code framework after Test Engine deprecation (ALM-17) | Playwright/pro-dev harness budgeted, or manual UAT with an explicit regression risk statement |
| 12 | Multiple modules / release independence | Cross-solution dependencies enforce import order and break upgrades; one solution must hold the tables (ALM-06) | Base + app layering with dedicated development environments → rung 3 |
| 13 | Multi-geography estate | Cannot reliably import into an older service-update station (ALM-08) | Development region chosen to be at or behind production's station |
| 14 | Compliance evidence for releases | Pipelines store artefacts and run history; work-item traceability is not in-product (ALM-21) | Azure DevOps/GitHub for traceability, or a documented manual record |
| 15 | Dynamics 365 or Copilot Studio workload | Block unmanaged customizations breaks a documented list including journeys, SLAs and agent publishing (ALM-15) | Either forgo that control or forgo those features — record the decision |
| 16 | Cross-tenant delivery (ISV, M&A) | Pipelines cannot deploy across tenants (ALM-10) | Azure DevOps/GitHub → **rung 3** |

---

## 5. ALM anti-patterns (evidence-backed)

- **ALM-A1 — Editing production directly.** Creates an unmanaged layer that permanently shadows managed updates (ALM-03); the countermeasure is documented (ALM-15).
- **ALM-A2 — Unmanaged solutions in production.** Microsoft's position is unambiguous: "Except for your development environment, you should only have managed solutions in your environments" (ALM-01); the conversion procedure exists precisely because this is common (D-04).
- **ALM-A3 — Working in the default solution.** Assets become indistinguishable and cannot be promoted selectively; the documented remedy is a custom solution set as the preferred solution (D-24, ALM-05).
- **ALM-A4 — Multiple publishers.** Irreversible component ownership; the only fix is delete-and-recreate with data loss (ALM-05).
- **ALM-A5 — Shared development environment for a team.** No isolation; overwriting is the documented outcome (ALM-06, ALM-23).
- **ALM-A6 — Manual deployment as the steady state.** No artefact integrity, no prevalidation, no run history, and the deployer owns the objects (ALM-10, ALM-20).
- **ALM-A7 — No source control.** Loses version history, review, rehydration and recovery-to-a-previous-state — all named benefits of Git integration (ALM-09).
- **ALM-A8 — Assuming rollback exists.** Contradicted by ALM-18; the restore path alone deletes solution flows, invalidates connection references and changes canvas app IDs.
- **ALM-A9 — Patches as the hotfix mechanism.** "Using patches isn't recommended" (ALM-03/ALM-04).
- **ALM-A10 — Ignoring dependency management.** Cross-solution dependencies produce import-order deadlocks and silently non-functional flows (ALM-06).
- **ALM-A11 — Values shipped inside the solution.** Contradicted verbatim by ALM-13; produces production pointing at development data sources.
- **ALM-A12 — Treating solution checker as a test gate.** Explicitly not a guarantee of import success and not a functional test (ALM-16, ALM-17).
- **ALM-A13 — Building new ALM on the ALM Accelerator.** Deprecated, unmaintained, issues not reviewed (ALM-22).
- **ALM-A14 — Unclear ownership of deployed objects.** Standard deployments make the requesting maker the owner (ALM-20), which is the upstream cause of ownerless applications (`governance.md` GOV-14).

---

## 6. Unknowns (UNKNOWN)

- **ALM-U-01** — Whether pipelines gained source-code integration, multi-solution deployment, update-vs-upgrade choice, or multi-developer support (all documented as "Not currently"/"No, but planned", D-06).
- **ALM-U-02** — Whether the February 2026 automatic conversion of pipeline targets to managed environments completed as announced, and what it did to tenants that had not planned for the licence impact.
- **ALM-U-03** — Practical maturity of Dataverse Git integration for canvas apps specifically (`application-architecture.md` records that in-editor Git version control was removed and that commits occur only on publish; the interaction with native solution-level Git integration was not verified).
- **ALM-U-04** — Plug-in/custom-code unit-testing practice and any first-party support (out of scope of the pages fetched).
- **ALM-U-05** — Exact licence position of Developer-plan QA environments used as pipeline targets (ALM-25).
- **ALM-U-06** — Whether the pipelines "redeploy previous solution versions" setting is on by default and whether it has retention limits.
- **ALM-U-07** — Deployment settings file (`DeploymentSettings.json`) capabilities and its interaction with delegated deployments (documented as unsupported in the maker experience for stage-owner delegation, D-07; the file itself was not researched).
- **ALM-U-08** — Catalog in Power Platform as a component-distribution mechanism (mentioned in D-24; not researched).

---

## 7. Conflicts (CONFLICTED)

- **ALM-C1 — Pipelines' capability table vs current product.** D-19's comparison lists Pipelines as "Source code integration: No, but planned" and "Code-first development: No, but planned" (table `ms.date` 2024-04-09). D-08 (2025-04-21) documents native Dataverse Git integration used alongside pipelines, and D-06 documents CLI-driven pipeline runs for developers. **Resolution:** the table is stale; the deprecation notice on the same page is current. Use D-06/D-08 for capability, D-19 only for the decision framing.
- **ALM-C2 — "Use pipelines" vs "targets must be managed".** D-06 positions pipelines as democratised ALM for all makers, while requiring every target environment to be a managed environment with premium licences for all users (D-06, D-22). For small teams this makes the "approachable" option the expensive one. **Resolution:** not a documentation contradiction — a genuine cost/capability trade-off that must be stated, mirroring `governance.md` GOV-C2.
- **ALM-C3 — Test environment necessity.** D-11 says basic ALM is possible with only development and production, then states that "at a minimum, any healthy ALM practice should include using a test environment". D-02 makes a test environment *structurally* necessary, because a managed solution cannot be imported into the environment that holds its originating unmanaged solution. **Resolution:** treat the test environment as mandatory; D-11's "you can" describes a possibility, not a recommendation.

---

## 8. Deferred to other areas

- Licensing arithmetic for managed environments, Developer Plan, per-app and pay-as-you-go → **Area 10 (Licensing and Cost)**.
- Monitoring, run history retention, Application Insights export, incident management and DR beyond backup/restore → **Area 11 (Operations and Support)**.
- Environment strategy as a governance construct, environment groups, environment creation control → `governance.md` (GOV-02, GOV-07, GOV-09).
- Deployment identity, connection security and separation of duties from the security side → `security.md` (SEC-05, SEC-19, SEC-21, SEC-36).
- Canvas-specific source-control and co-authoring constraints → Area 02 `application-architecture.md` (AA-05, AA-06, AA-08).
- Data and configuration migration (reference data, Dataverse rows) → Area 03 `data-architecture.md`.

---

## 9. Verification list before pack encoding (mandatory)

1. Pipelines "Not currently" list (D-06) — at least four items are candidates for change: source-code integration, multi-solution deployment, import-behaviour choice, multi-developer support.
2. February 2026 automatic managed-environment conversion for pipeline targets — outcome and current default (D-06).
3. Dataverse Git integration GA state and canvas-app coverage (D-08 + `application-architecture.md` AA-05/AA-06).
4. Whether a supported first-party functional-test option has replaced Test Engine (ALM-17).
5. Block-unmanaged-customizations break-list (D-12, `ms.date` 2026-09-02 — updated during the research window; expect churn).
6. Backup retention values and the production-managed-environment condition (D-17).
7. Build Tools task version (v1 vs v2) and whether username/password service connections are still supported (D-09).
8. Delegated-deployment sharing limitations — "first deployment only" and "no individual users" are both flagged "currently" (D-07).

---

## 10. Implications for the aisa knowledge model (pointers, not pack content)

- ALM is best modelled as a **ladder with entry conditions**, not as a set of features. The pack should map requirement signals (team size, change velocity, reversibility, compliance evidence, cross-tenant, code-first content) to a rung, and price the rung.
- Several ALM decisions are **irreversible** and belong to Discovery: publisher, table ownership type (`security.md` SEC-09), Dynamics 365 apps at environment creation, environment region.
- Two findings should be represented as **tripwires** rather than static rules: the February 2026 pipeline-target conversion and the February 2027 managed-environment licence enforcement (`governance.md` GOV-11).
- **ALM-18 (no rollback)** deserves explicit treatment in the pack's risk model: it is the single most commonly assumed capability that does not exist, and its absence changes release planning, cutover design and sponsor expectations.
- The deprecation pair (ALM Accelerator, CoE Starter Kit) means any pack content or engagement artefact citing them must be reviewed.

---

## 11. Source register

Kind: fetched (retrieved 2026-09-03, `ms.date` shown) / search-verified / signals (T3/T4).

| Id | Tier | Kind | Title | URL | ms.date |
|---|---|---|---|---|---|
| D-01 | T1 | fetched | ALM basics with Microsoft Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/basics-alm | 2025-01-04 |
| D-02 | T1 | fetched | Solution concepts with Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm | 2025-01-29 |
| D-03 | T1 | fetched | Solution layers and merge behavior | https://learn.microsoft.com/en-us/power-platform/alm/solution-layers-alm | 2025-01-30 |
| D-04 | T1 | fetched | Move from unmanaged to managed solutions | https://learn.microsoft.com/en-us/power-platform/alm/move-from-unmanaged-managed-alm | 2025-07-03 |
| D-05 | T1 | fetched | Organize your solutions in Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/organize-solutions | 2025-11-04 |
| D-06 | T1 | fetched | Overview of pipelines in Power Platform (incl. FAQ limits) | https://learn.microsoft.com/en-us/power-platform/alm/pipelines | 2026-01-12 |
| D-07 | T1 | fetched | Deploy pipelines as a service principal or pipeline owner | https://learn.microsoft.com/en-us/power-platform/alm/delegated-deployments-setup | 2026-08-19 |
| D-08 | T1 | fetched | Overview of Dataverse Git integration | https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview | 2025-04-21 |
| D-09 | T1 | fetched | Microsoft Power Platform Build Tools for Azure DevOps | https://learn.microsoft.com/en-us/power-platform/alm/devops-build-tools | 2026-08-19 |
| D-10 | T1 | fetched | GitHub Actions for Microsoft Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/devops-github-actions | 2026-08-19 |
| D-11 | T1 | fetched | ALM environment strategy considerations | https://learn.microsoft.com/en-us/power-platform/alm/environment-strategy-alm | 2024-05-23 |
| D-12 | T1 | fetched | Block unmanaged customizations in Dataverse environments | https://learn.microsoft.com/en-us/power-platform/alm/block-unmanaged-customizations | 2026-09-02 |
| D-13 | T1 | fetched | Solution checker enforcement in managed environments | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-solution-checker | 2025-11-24 |
| D-14 | T1 | fetched | Improve component performance… with solution checker | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/use-powerapps-checker | 2026-08-03 |
| D-15 | T1 | fetched | Use environment variables in Power Platform solutions | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables | 2026-01-09 |
| D-16 | T1 | fetched | Use a connection reference in a solution | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference | 2026-01-09 |
| D-17 | T1 | fetched | Back up and restore environments | https://learn.microsoft.com/en-us/power-platform/admin/backup-restore-environments | 2026-06-23 |
| D-18 | T1 | fetched | Managed environments overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview | 2026-02-23 |
| D-19 | T1 | fetched | ALM Accelerator for Power Platform (**Deprecated**) | https://learn.microsoft.com/en-us/power-platform/guidance/alm-accelerator/overview | 2024-04-09 (page updated 2026-07-13) |
| D-20 | T1 | fetched | WAF — Operational Excellence checklist (OE:01–OE:11) | https://learn.microsoft.com/en-us/power-platform/well-architected/operational-excellence/checklist | 2025-08-15 |
| D-21 | T1 | fetched | Environment groups | https://learn.microsoft.com/en-us/power-platform/admin/environment-groups | 2025-07-28 |
| D-22 | T1 | fetched | Licensing requirements for managed environments | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-licensing | 2026-08-31 |
| D-23 | T1 | fetched | Manage application users in the PPAC | https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users | 2026-04-03 |
| D-24 | T1 | fetched | Develop a tenant environment strategy (Dataverse, preferred solutions, pipelines, solution checker, catalog) | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/environment-strategy | 2026-05-04 |
| D-25 | T1 | cited from validated foundational Area 2 (`application-architecture.md`) | Test Engine deprecation (April 2026) — see `application-architecture.md` AA-08 / V-07 | (per `application-architecture.md` register) | 2026-05-22 (upd. 2026-08-14) |
| D-26 | T3/T4 | search-verified (signal) | Independent commentary on pipelines' limitations vs Build Tools / ALM Accelerator | various | 2025–2026 |

---

## 12. Cross-area analysis (from the ALM side)

### 12.1 ALM ↔ GOVERNANCE

1. **Governance owns the environments that ALM runs on.** The dev/test/prod topology is the same object as the environment strategy (`governance.md` GOV-02), so a governance decision to consolidate environments directly removes ALM capability — and a decision to add environments adds licence and administration cost.
2. **ALM tooling now requires a governance state.** Pipeline targets must be managed environments, with automatic conversion beginning February 2026 (ALM-10). Adopting in-product ALM therefore triggers the managed-environment licence conversation (`governance.md` GOV-11) — an ALM decision with an organisation-wide budget consequence.
3. **The release gates are governance settings, not pipeline settings.** Solution-checker enforcement (Warn/Block, critical-only) and block-unmanaged-customizations are configured per environment or per environment group (ALM-15, ALM-16; `governance.md` GOV-20). A project cannot weaken them inside its own pipeline, and an environment group can impose them centrally.
4. **Drift is fought on two fronts.** Solution-layer discipline is ALM's (ALM-19); environment-configuration consistency is governance's, through group rules that lock settings (`governance.md` GOV-07). Business units, teams and application users fall in the gap — they travel in neither solutions nor group rules and must be provisioned per environment (ALM-07).
5. **Deployment creates the ownership record governance audits.** Standard deployments assign ownership to the requesting maker (ALM-20); delegated deployments assign it to a governed identity. The ownerless-application backlog that governance later detects (`governance.md` GOV-14) is largely manufactured at deployment time.
6. **Both areas lost their community backbone at once.** The ALM Accelerator (ALM-22) and the CoE Starter Kit (`governance.md` GOV-12) are both unmaintained; an organisation running both is carrying debt in delivery *and* in governance, with in-product replacements that are not proven equivalent.

### 12.2 ALM ↔ SECURITY

1. **Deployment is privileged.** A service principal that deploys plug-ins needs System Administrator in every target (ALM-11). The least-privilege story is therefore "no standing human privilege in production", enforced by delegated deployment plus approval — not "nothing has privilege".
2. **The runtime identity is set by ALM.** Flows execute under the connection owner (`security.md` SEC-21); the deployed object is owned by the deploying identity (ALM-20). Service-principal ownership of production automations is achieved by the deployment mechanism, not by a security setting.
3. **A security control can be lost in transit.** The documented issue where an implicitly shared *secure* connection imported via a connection reference has "the security… not set properly in the target environment" (`security.md` SEC-19) means production security depends on post-deployment verification, which belongs on the release checklist.
4. **Secrets and configuration are an ALM/security joint design.** Values must not ship in the solution (ALM-13); secrets live in Key Vault and are consumable only by flows, agents and custom connectors (`security.md` SEC-07). Every target environment therefore needs its own Key Vault permission model and its own environment-variable values — provisioning that must be automated or it will be forgotten.
5. **The security model does not travel intact.** Security roles and column-security profiles are solution components; **business units and teams are not** and "must be created and managed in each environment" (`security.md` S-02) — and modernised-BU owning-BU values must match across environments or synchronisation fails with a foreign-key violation (`security.md` SEC-10). Any BU-dependent security model needs an explicit environment-provisioning step.
6. **Security configuration constrains recovery.** Restore requires matching CMK, matching enterprise policies (VNet) and matching managed-environment status (ALM-18; `security.md` SEC-29, SEC-30); audit retention is unavailable under CMK (`security.md` SEC-34). The security posture therefore determines which of the three recovery paths remain open — a fact that must be established before a security control is switched on, not after an incident.
7. **Production integrity is a security control implemented in ALM.** Block unmanaged customizations prevents changes that would otherwise silently override managed behaviour (ALM-15) and is what makes read-only production support possible (`governance.md` GOV-15). Its break-list is therefore a security/feature trade-off, not just an ALM inconvenience.

---

## 13. Summary

Power Platform has a complete, first-party application lifecycle — solutions, layering, environment variables, connection references, native Git integration, in-product pipelines with artefact immutability and delegated deployment identities, and a static-analysis gate that can block imports. What it does not have is equally decisive: **no rollback**, **no supported first-party functional test framework** after the Test Engine deprecation, **no multi-developer isolation inside an environment**, and **no cross-tenant deployment**.

Four properties drive every ALM decision. **(1)** Several choices are irreversible — the publisher, the table ownership type, Dynamics 365 apps at environment creation, the environment region — and all of them are made in the first days of an engagement. **(2)** Managed solutions are the only defensible production posture, but uninstalling one destroys the data in its custom tables and columns, so solution boundaries are data-lifecycle boundaries. **(3)** The ALM rung is set by team size, change velocity and reversibility requirements, not by preference: two makers on one artefact means environment-per-developer plus Git; a "we can roll it back" commitment means a rehearsed restore or version-redeploy path, because neither exists by default. **(4)** In-product ALM now has a governance and licensing prerequisite — pipeline targets must be managed environments — so the decision to automate delivery is also a decision about the tenant's licence position.

Finally, the ground has moved: the ALM Accelerator and the CoE Starter Kit are both unmaintained, and Microsoft's direction is pipelines plus native Git integration, extended into Azure DevOps or GitHub where source control, code review, work-item traceability and cross-tenant delivery are required. Guidance predating that shift — including some still-published Microsoft pages — should be treated as historical.

---

## 14. Cross-Block V2 reconciliation

### 14.1 Custom connectors are an architectural seam with ALM cost

`architecture-patterns.md` AP-02, AP-05, AP-08 and AP-10 now cite **ALM-14** as a precondition when instantiated through a custom connector. The reciprocal decision boundary is:

- connector definition, connection references and consuming solution must have an explicit import/deployment order;
- backend API and connector schema are a versioned contract;
- canvas-app connector rebinding/workaround that creates an unmanaged layer directly conflicts with a production policy that blocks unmanaged customizations;
- if that workaround is required, **do not silently disable the integrity control**. Redesign the consumer/seam, use another supported binding approach, or document a governance exception with owner and expiry.

This is not a claim that custom connectors are inherently bad. It is the condition under which their ALM cost changes the pattern choice.

### 14.2 Hybrid patterns require two coordinated supply chains
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS + INF
- **Evidence:** Azure Functions documentation recommends IaC, source control and CI/CD; Azure Well-Architected Operational Excellence requires predictable automated pipelines with testing/quality gates.
- **Decision impact:** AP-05/AP-10 and Azure-backed AP-02/AP-04/AP-08 require a Power Platform solution pipeline **and** an Azure/API/broker infrastructure/code pipeline. The release unit must declare contract compatibility and sequencing. Deploying only one side is allowed only where backward/forward compatibility is proven.
- **Sources:** `https://learn.microsoft.com/en-us/azure/azure-functions/functions-infrastructure-as-code`; `https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/checklist`.

### 14.3 Validation model — functional testing and performance validation are not contradictory
Use the shared model in `integration-architecture.md` §15.8:

1. **V1 documentation/limits** for hard support/limit boundaries;
2. **V2 bounded pilot with monitoring** for latency, throttling, security-model cost and recovery behaviour;
3. **V3 pro-dev automated harness** for repeatable functional/API/performance regression;
4. **V4 managed-test fidelity** when behaviour depends on managed-environment/network/security controls.

ALM-17 remains true: no supported first-party low-code functional-test framework is assumed after Test Engine deprecation. That does not prohibit Playwright/API/load tooling or a monitored pilot. A business-critical release must state which validation level is required and budget it.

### 14.4 Recovery crosses ALM and integration
ALM-18's “no rollback” finding now has an integration consequence: restoring one environment can rewind one participant while external systems, queues and replicated copies retain later state. Therefore the release/recovery plan must contain a post-restore integration step: pause affected writers, establish the restore time boundary, reconcile/replay/re-seed as appropriate, validate, then reopen traffic. See `integration-architecture.md` §8/§15.7 and `operations-support.md` OP-14/OP-18.

### 14.5 Compensation/reconciliation are versioned release artefacts
Idempotency keys, mapping rules, compensating actions and reconciliation schemas are part of the contract. They require code review/change control equal to the forward write path. The identity allowed to execute them is governed by `security.md` SEC-XB-04; the business owner of unresolved items is governed by `governance.md` GOV-XB-04.

