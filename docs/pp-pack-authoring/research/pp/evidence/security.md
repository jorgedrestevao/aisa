Research Status: CANONICAL
Research Confidence: MEDIUM
Gate: PASS — Cross-Block Gate Recheck
Canonicalization Basis: Cross-Block Gate Recheck
Canonicalized: 2026-09-03

# Security — Research Evidence

Research area: **06 — Security** (`../research-areas.md`). Block B, area 1 of 3.
Draft date: **2026-09-03**. Sibling documents of the same block: `governance.md` (area 07), `alm-devops.md` (area 08). Cross-references to the validated foundational Areas 1–4 use the canonical files `platform-suitability.md` (**PS-nn**), `application-architecture.md` (**AA-nn**), `data-architecture.md`, `automation-architecture.md`.
Source policy: `../source-policy.md`.

**Purpose.** Answer: *"Given these security requirements, what changes in the architecture — environment topology, data model, identity model, connectivity, application type, and who is allowed to do what — and at what point does Power Platform stop being able to satisfy them?"* Not a settings catalogue: a setting appears only where it moves an architectural boundary.

**Provenance rule.** Sources are **fetched** (page retrieved 2026-09-03, `ms.date` read from page metadata — the default), **search-verified** (snippet only; a finding relying solely on such a source is capped at MEDIUM), or **T3/T4 signals** (non-Microsoft; never admissible as capability evidence, only as a prompt to verify).

**Origin tags.** Every finding carries **Origin:** MS (Microsoft statement) / INF (analyst inference from documented limits) / T3 / T4 / UNKNOWN. Cross-Block V2 uses **VOLATILE VALUE** alongside the source-policy classifications where a security control's availability, licensing prerequisite or rollout state is date-sensitive. An INF-derived prohibition is phrased "treat as unsupported until verified", never as a Microsoft statement.

**Overall confidence MEDIUM (self-assessed, no gate).** Individual findings keep their own grade. The overall cap reflects: (a) several controls are preview or explicitly "rolling out" (ACP design-time enforcement, endpoint filtering, security score, app access control, administrator privileges, guest access GA state); (b) the most consequential negative evidence about DLP as an exfiltration control comes from a T4 source and from reading Microsoft's own scoping language, not from a Microsoft statement; (c) no adversarial review or gate has been run on this document; (d) hierarchy security and Purview/sensitivity-label enforcement depth were not fetched (§6).

**Volatility.** Security is the fastest-moving Power Platform surface in 2025–2026. Advanced connector policies, the Security Hub/score, app access control, masking rules, administrator privileges, agent authentication/channels, guest-access defaults, and VNet connector coverage all changed within the research window. Re-verify §9 items before encoding anything into the pack.

---

## 1. The five enforcement planes

Power Platform security is not one model. It is five planes that are enforced by different services, configured by different roles, and fail independently. Almost every architectural consequence in this document comes from a requirement landing on the *wrong* plane.

| # | Plane | Enforced by | Grain | Typical failure mode | Findings |
|---|---|---|---|---|---|
| 1 | **Tenant / identity** | Microsoft Entra ID (authN, Conditional Access, CAE, PIM, B2B) | User, group, device, location, session | CA policy misses a first-party app id; standing admin access | SEC-01..SEC-06, SEC-36 |
| 2 | **Environment** | Power Platform (security group, environment roles, IP firewall, cookie binding, guest restriction, VNet, CMK, Lockbox) | Environment | Everything in one environment; admins and app users bypass the group | SEC-15..SEC-17, SEC-27..SEC-31 |
| 3 | **Data (Dataverse)** | Dataverse (roles, business units, teams, sharing, column security, masking, audit) | Table, row, column | Additive privileges over-granted and unrecoverable; sharing used as the model | SEC-08..SEC-14, SEC-34, SEC-39 |
| 4 | **Connection / connector** | Connectors + data policies (DLP/ACP/endpoint filtering) + the *target system's own* authorization | Connector, action, endpoint, connection credential | App UI mistaken for an authorization layer; implicit connections; service accounts | SEC-18..SEC-26 |
| 5 | **Application surface** | Each app type's own model (canvas sharing, model-driven roles, Pages web roles + table permissions, flow ownership) | App, page, record set, flow | Attack surface assumed uniform across app types | SEC-32, SEC-33, SEC-38, SEC-40 |

**Rule that follows from the table (INF):** a security requirement must be satisfied on the *lowest* plane that can enforce it. A requirement satisfied only in plane 5 (the app) is not enforced at all against a user who has plane-4 credentials — see SEC-18.

---

## 2. Decision boundaries (requirement → security constraint → architectural consequence)

Each row is derived from findings in §3; the finding id is the warrant.

- Data must be invisible to a population that has a licence and a tenant identity → environment membership + Dataverse role are both required, and neither is implied by the licence → **separate environment with a security group** is the only reliable isolation unit; do not model it as "a different app" (SEC-01, SEC-15, SEC-16).
- Some users must see a table but not certain rows → row access is the *sum* of role depth + business unit + team membership + shares, and grants cannot be subtracted → **the business-unit/ownership model must be designed before the first table is created**; the table's ownership type (organization vs user/team) is fixed at creation (SEC-08, SEC-09).
- Users work across organisational units (matrix organisation) → classic BU hierarchy cannot express it without owner-team workarounds → **modernised business units**, with a documented migration (impact analysis, RACI per BU, forms updated to carry *Owning Business Unit*) and a one-way-ish switch whose disablement rewrites ownership on existing rows (SEC-10).
- Certain columns must be hidden from otherwise-authorised users → column-level security exists but **never applies to System Administrator**, cannot secure lookups/formula/primary-name/system columns, and leaks through calculated and composite columns → **model sensitive attributes into a separate table with its own row security**, or accept the exclusions (SEC-13).
- External *organisations* must use the solution → B2B guests into canvas/model-driven; guest access to Dataverse is **restricted by default on new environments** and the restriction covers Dataverse only → decide per environment, and note guests still reach non-Dataverse apps in that environment (SEC-04; app-type fit in AA-52).
- External *customers or the public* must use the solution → Power Pages with web roles + table permissions; **without a table permission there is no access, and a table permission without a web role has no effect**; Global access type means all rows → treat Pages as an internet-facing application requiring WAF, security scan, certificate/auth-key lifecycle, and an explicit anonymous-access review (SEC-32, SEC-35).
- The app must not become a way to reach data the user could not otherwise reach → **it already cannot be**: with explicit auth the user's own rights govern; with implicit auth the maker's credentials govern → for sensitive sources use explicit (Entra) authentication; if implicit is unavoidable, the data source itself must be scoped to what the app legitimately needs (SEC-18, SEC-20).
- A production automation must not stop when its author leaves → flows run with the connection owner's credentials → **service-principal-owned flows and connections**; OAuth connections can be explicitly shared only with a user representing a service principal (SEC-21, SEC-22).
- Access to Dataverse must be restricted to corporate networks → IP firewall is **managed-environment only**, protects Dataverse only, defaults to audit-only mode, and by default still allows *all* application users and Microsoft trusted services → budget the managed-environment licence, plan the E5-class licence requirement, and treat non-Dataverse connectors as out of scope (SEC-27).
- Back-end systems must never be exposed to the public internet → VNet support (subnet delegation) for Dataverse plug-ins and a fixed connector list, or the on-premises gateway → **environment becomes region-pinned to an Azure region pair, trial/Teams environments are excluded, subnet range and DNS become immutable while delegated, and restore requires the same enterprise policy** (SEC-30, SEC-31).
- Encryption keys must be customer-controlled → CMK is managed-environment only, requires E5-class licences, covers a *listed* set of services and explicitly excludes connection settings, environment settings, app display names/descriptions and connection metadata → **CMK is a data-at-rest control for Dataverse content, not a tenant-wide control**; key revocation disables environments and "data loss can occur" (SEC-29).
- Regulator requires who-saw-what → Dataverse auditing covers changes and access, **not** retrieve/export unless activity logging (Purview, licence-gated) is on; retention is stamped at write time; audit is not available with CMK; audit consumes log capacity → **audit is a capacity and licensing decision made before go-live, not a switch flipped after** (SEC-34).
- Data must not leave the tenant through connectors → tenant isolation covers **Entra-authenticated connectors only**, has a documented Azure DevOps gap, and takes ~1 hour to propagate → combine with data policies; do not present it as a complete exfiltration control (SEC-26).
- Only an approved set of services may be reachable → classic DLP cannot block a fixed list of connectors; **ACP** gives a default-deny allowlist but currently covers certified connectors only and does not cover custom or HTTP connectors → hybrid policy posture, and the custom-connector/HTTP gap must be closed by classic policy + endpoint filtering (SEC-23, SEC-24, SEC-25).
- A specific endpoint must be unreachable (a particular SQL server, a particular URL) → endpoint filtering is preview, covers 8 connectors, and is **not enforced for environment variables, custom inputs or any runtime-computed endpoint** → do not design a control that depends on it; put the control on the target system (SEC-25).
- Secrets must never live in the solution → environment variables of type Secret (Azure Key Vault only), consumable by **cloud flows, Copilot Studio agents and custom connectors only** — "the secrets aren't available for use in other customizations or generally via the API" → canvas apps and most components cannot consume a secret; any requirement to do so pushes logic into a flow, a plug-in (managed identity) or Azure (SEC-07, SEC-06).
- Separation of duties between build and run → makers must not hold maker rights in test/production; deployment must be performed by a delegated identity → this is an **ALM** consequence (see `alm-devops.md` ALM-11, ALM-20) enforced by environment roles and delegated deployments (SEC-22, SEC-36).
- Board-level assurance that the tenant is secure → the PPAC security score is **preview**, "for evaluation purposes only at this time", refreshes every 24 h, and its recommendations are actionable only on managed environments → do not use the score as the assurance artefact (SEC-35).

---

## 3. Findings

Ids SEC-nn are stable. Sources are listed in §11.

### 3.1 Identity and authentication

#### SEC-01 — A licence and a tenant identity grant nothing; access needs environment membership *and* a Dataverse security role
- **Classification:** FACT + DECISION CRITERION
- **Origin:** MS
- **Evidence:** "Simply having a license and an identity at tenant level isn't enough to grant access to an environment unless it's the [default environment]" (S-33). "All licensed users, whether or not they're members of the security groups, must be assigned security roles to access data in the environments… Users can't access environments until they're assigned at least one security role for that environment" (S-26). "Users or groups assigned to these environment roles aren't automatically given access to the environment's database (if it exists) and must be given access separately" (S-08).
- **Why it matters:** the most common "why can't they see it / why can they see it" defect class is a mismatch between the three layers.
- **Decision impact:** every access requirement must be resolved into a triple (environment membership, security role, resource share). Isolation requirements resolve to *environments*, not to app-level filtering.
- **Confidence:** HIGH.
- **Sources:** S-08, S-26, S-33.

#### SEC-02 — Conditional Access applies, but Power Automate is not inside the Office 365 app target
- **Classification:** CONSTRAINT + RISK
- **Origin:** MS
- **Evidence:** "**Microsoft Flow Service** (Application ID: `7df0a125-d3be-4c96-aa54-591f83ff541c`) isn't included in the **Office 365** application target… users who access Power Automate flows from SharePoint, Teams, or Excel might see authentication errors because the token exchange between the host application and Power Automate fails. To prevent this issue, either target **All cloud apps** or explicitly add Microsoft Flow Service to your policy" (S-33). Location/device/user-based CA for Power Apps and Power Automate requires Entra ID P1/P2 (S-07).
- **Decision impact:** if the design depends on embedded flows (SharePoint, Teams, Excel), the CA policy design is part of the solution design, not an infrastructure detail. Licensing dependency (P1/P2) is an architectural cost.
- **Confidence:** HIGH.
- **Sources:** S-07, S-33.

#### SEC-03 — Continuous access evaluation shortens the revocation window from ~1 hour to near real time
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** "Users whose access rights are terminated keep access to resources until the access token expires—for Power Platform, as long as an hour, by default. With continuous access evaluation, however, Power Platform services such as Dataverse continuously evaluate a user's critical events and network location changes" (S-33).
- **Decision impact:** an "access must be revocable immediately" requirement is satisfiable, but only with CAE plus the identity plane; it is not satisfiable by Dataverse role removal alone.
- **Confidence:** HIGH.
- **Sources:** S-33.

#### SEC-04 — Guest access to Dataverse is restricted by default on new environments, and the restriction covers Dataverse only
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** "By default, guest access to Dataverse is restricted for all new environments. You must manually enable Dataverse access in existing environments." When restricted: "Existing guest connections disabled: Previously created guest-owned connections to Dataverse are disabled but not removed." Documented limitations: "Not available for environments without Dataverse"; "Doesn't override tenant-level guest access policies set in Microsoft Entra ID or through Conditional Access"; "**Guests aren't restricted from accessing apps in the environment that aren't using Dataverse.**"; Copilot Studio items using Microsoft Graph connectors "might access the information in these items even if you block guest access" (S-25).
- **Decision impact:** partner-facing scenarios need an explicit per-environment decision. A "no external access" requirement is *not* met by this control alone in an environment that also hosts non-Dataverse apps.
- **Conditions:** GA state unclear — the adoption guidance links this feature as "guest access (preview)" (S-33) while the feature page carries no preview banner (S-25). See SEC-C1.
- **Confidence:** HIGH (behaviour) / MEDIUM (GA state).
- **Sources:** S-25, S-33.

#### SEC-05 — Application users (service principals) are a parallel, unlicensed identity plane that bypasses two environment controls
- **Classification:** FACT + RISK
- **Origin:** MS
- **Evidence:** "You can create an unlicensed application user in your environment"; "In an environment, you can only have one application user for each Microsoft Entra–registered application"; "**All your application users can run in any environments that are secured with a security group without being a member of the security group**" (S-14, repeated in S-26). IP firewall: "**Allow access for all application users**: This setting allows all application users third-party and first-party access to Dataverse APIs. Enabled by default" (S-12). Deletion requires deactivation first and reassignment of owned records (S-14).
- **Why it matters:** the two controls most often presented as the environment perimeter — security group and IP firewall — do not, by default, constrain service principals.
- **Decision impact:** any design using service principals must state (a) which roles they hold, (b) whether SPN filtering on the IP firewall is enabled, (c) who owns the app registration and its secret rotation. Excessive SPN privilege is a top threat-model item (SEC-37).
- **Confidence:** HIGH.
- **Sources:** S-12, S-14, S-26.

#### SEC-06 — Managed identity is GA for Dataverse plug-ins only; there is no credential-free path for flows or connectors
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** Supported services table lists only "Dataverse plug-ins" and "Dependent, assembly plug-ins" as GA; "Power Platform managed identity allows enterprises to securely connect with Azure resources that support Azure managed identity **from Dataverse plug-ins** without the need for managing the credentials"; built on workload identities and federated identity credentials (S-31).
- **Decision impact:** a "no stored credentials anywhere" requirement forces the integration into plug-in code (pro-dev, Dataverse-bound) or into Azure. Low-code flows still authenticate through connections or Key Vault secrets.
- **Confidence:** HIGH.
- **Sources:** S-31.

#### SEC-07 — Key Vault secrets are consumable by three component types only
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "These secrets are then made available for use within Power Automate flows and custom connectors. Notice that **the secrets aren't available for use in other customizations or generally via the API**"; "Environment variables referencing Azure Key Vault secrets are currently limited for use with Power Automate flows, Copilot Studio agents, and custom connectors"; "Environment variables referencing secrets aren't currently available from the dynamic content selector"; requires `Microsoft.PowerPlatform` resource provider registration, **Key Vault Secrets User** for both the creating user and the Dataverse service principal (app id `00000007-0000-0000-c000-000000000000`), the vault "must be in the same tenant", and if the Key Vault firewall is on, "Power Platform isn't included in the 'Trusted Services Only' option" — the Power Platform IP ranges must be allowed (S-28). Private-link integration requires VNet support and same-tenant subscription (S-28, S-16).
- **Decision impact:** canvas apps cannot hold or read a secret. Any "the app must call an API with a key" requirement becomes a flow, a custom connector, or a plug-in — which changes the architecture, latency profile and licensing.
- **Confidence:** HIGH.
- **Sources:** S-16, S-28.

### 3.2 Dataverse authorization model

#### SEC-08 — Privileges are cumulative and cannot be subtracted; the model must be built least-privilege from the start
- **Classification:** FACT + DECISION CRITERION
- **Origin:** MS
- **Evidence:** "A key concept of Dataverse security to understand is **all privilege grants are accumulative with the greatest amount of access prevailing. If you gave broad organization level read access to all contact records, you can't go back and hide a single record**" (S-02). "A user can have multiple security roles. Security role privileges are cumulative" (S-03). "one of the most common administrative mistakes is getting frustrated with permissions and just over granting access. Very quickly a well-crafted security model starts looking like Swiss cheese (full of holes!)" (S-02).
- **Decision impact:** the security model is an *early* design artefact with an irreversible failure mode. Retrofitting least privilege onto an over-granted environment means rebuilding roles, not editing them.
- **Confidence:** HIGH.
- **Sources:** S-02, S-03.

#### SEC-09 — Two irreversible choices: table ownership type, and (without the matrix feature) the owning business unit
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "Dataverse supports two types of record ownership. Organization owned, and User or Team owned. **This is a choice that happens at the time the table is created and can't be changed.**" For organization-owned tables the only access levels are "can" or "can't"; user/team-owned tables get the tiered Organization / Parent:Child BU / BU / User depths (S-02, S-03). "Each record has an **Owning Business Unit** column… This column defaults to the user's business unit when the record is created **and can't be changed except when the feature switch is turned ON**" (S-02). Every environment has a single root business unit "that is unchangeable" (S-02).
- **Decision impact:** the row-security requirement decides the table's ownership type before the data model is built. A late discovery that rows must be scoped per unit on an organization-owned table means recreating the table.
- **Confidence:** HIGH.
- **Sources:** S-02, S-03.

#### SEC-10 — Modernised business units solve matrix access but carry migration and reversal risk
- **Classification:** PATTERN + RISK
- **Origin:** MS
- **Evidence:** With the feature on, "the user's business unit is no longer relevant in determining the user's access to records"; a role from each BU is assigned to the user; the user chooses the owning BU at record creation (S-04). Enablement prerequisites: "Before you enable this feature, you must publish all your customizations"; `RecomputeOwnershipAcrossBusinessUnits` set to true locks the system "up to 5 minutes"; `AlwaysMoveRecordToOwnerBusinessUnit` must be set to false (S-02). Reversal: "If you turn off either the **Record ownership across business units** feature or set the **RecomputeOwnershipAcrossBusinessUnits** setting to false… **all records where the Owning Business Unit field is different from the owner's business unit will be updated to the owner's business unit**" (S-02). Integration risk: "If you have a job/process to sync data between environments and the **Owning Business Unit** is included as part of the schema, your job fails with a **Foreign KEY** constraint violation if the target environment doesn't have the same **Owning Business Unit** value" (S-02). Microsoft's recommended migration for existing multi-BU environments: impact analysis, a user RACI at BU-record level, one BU at a time, "removing record ownership through Teams", and modifying all input forms to include and default the Owning Business Unit column (S-04).
- **Decision impact:** matrix access is available but is a programme of work, and it couples the security model to ALM (BU values must exist identically in every environment — see `alm-devops.md` ALM-19).
- **Confidence:** HIGH.
- **Sources:** S-02, S-04.

#### SEC-11 — Teams: owner teams carry roles; access teams carry shares; group teams bind Entra groups to Dataverse
- **Classification:** PATTERN
- **Origin:** MS
- **Evidence:** "Owning Teams can own records… Access teams are more performant because they don't allow owning records by the team or having security roles assigned to the team. Users get access because the record is shared with the team" (S-02). Every BU has an auto-managed default team whose membership "can't manually add or remove members" (S-02). Recommended pattern: one Entra security group per business unit → a Dataverse group team per group → the BU's role assigned to the team; "The user… will be created in the root business unit when the user accesses the environment. It's fine to have the user and the Dataverse group teams to be in the root business unit. They only have access to data in the business unit where the security role is assigned" (S-02). Sharing a canvas app with an Entra group and selecting roles auto-creates the team (S-34).
- **Decision impact:** identity governance (who is in which Entra group) becomes the operational control for Dataverse access — which is what makes the model auditable and JML-safe. Direct user-role assignment is the anti-pattern (SEC-A5).
- **Confidence:** HIGH.
- **Sources:** S-02, S-34.

#### SEC-12 — Record sharing is an exception mechanism, not an access model
- **Classification:** ANTI-PATTERN (when used as the model) + CONSTRAINT
- **Origin:** MS
- **Evidence:** "It should be an exception, though, because it's a less performant way of controlling access. **Sharing is tougher to troubleshoot because it's not a consistently implemented access control.** Sharing with a team is a more efficient way of sharing" (S-02). Record-level access is "the combination of all their security roles, the business unit they're associated with, the teams they're members of and the records that are shared with them" (S-02).
- **Decision impact:** if the requirement is "access depends on a per-record relationship", model it (BU, owner team, access team template, or a relationship + Pages table permission) rather than granting Share privilege broadly.
- **Confidence:** HIGH.
- **Sources:** S-02.

#### SEC-13 — Column-level security has five documented exclusions and never applies to System Administrator
- **Classification:** CONSTRAINT + RISK
- **Origin:** MS
- **Evidence:** "Column-level security configurations are organization-wide and apply to all data access requests." "**Column-level security doesn't apply for users who have the system administrator role. Data is never hidden from system administrators.**" "Unless one or more security profiles are assigned to a column with security, only users with the system administrator security role can access the column." Columns that can't be secured: "Columns in virtual tables; Lookup columns; Formula columns; Primary name columns; System columns like `createdon`, `modifiedon`, `statecode`, and `statuscode`". "File and Image data types can be secured, but they can't be masked." Leakage paths: "When a calculated column includes a column that is secured, data might be displayed in the calculated column to users that don't have permission to the secured column. **Both the original column and the calculated column should be secured**"; composite columns (e.g. `fullname`, `address1_composite`) require securing every constituent column. "Changes to column security require a browser refresh from the end user… for the changes to take effect" (S-32). Related: "Column-level security should be used as needed and not excessively as it can add overhead that is detrimental if over used" (S-02).
- **Decision impact:** a "these fields must be invisible to admins" requirement is **unsatisfiable in Dataverse**; it forces the attribute out of Dataverse or forces the admin population to be tightly held (SEC-36). A "hide a lookup / a formula column" requirement is unsatisfiable as stated.
- **Confidence:** HIGH.
- **Sources:** S-02, S-32.

#### SEC-14 — Masking rules exist as a managed-environment control for PII display
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** Masking rules are listed as a managed-environment capability (S-23) and described as replacing sensitive values with masked strings, with "Read unmasked" as a separate column-security-profile permission (options **All Records** / **One record** / **Not Allowed**, default Not Allowed) (S-32, S-34).
- **Decision impact:** partial-display requirements (last four digits) are met natively, but only inside the column-security framework and only in a managed environment.
- **Conditions:** depth not verified — the dedicated masking-rules page was not fetched (SEC-U-05).
- **Confidence:** MEDIUM.
- **Sources:** S-23, S-32, S-34.

### 3.3 Environment as a security boundary

#### SEC-15 — The environment is the platform's security boundary, and cross-environment data access is not a thing
- **Classification:** FACT + DECISION CRITERION
- **Origin:** MS
- **Evidence:** "A Power Platform environment is a logical container and unit of governance management that **represents the security boundary in Power Platform**. Many features such as virtual network, Lockbox, and security groups all operate at an environment-level of granularity" (S-33). "When you create an app in an environment, that app is only permitted to connect to the data sources that are also deployed in that same environment… If you create an app in the Test environment, it only is permitted to connect to the Test database; it isn't able to connect to the 'Dev' database" (S-08). "Each environment is created under a Microsoft Entra tenant, and its resources can only be accessed by users within that tenant. An environment is also bound to a geographic location" (S-08). "These entitlements are only granted within a single database and are individually tracked in each Dataverse database" (S-02). WAF: environments are named as an isolation example, with the explicit trade-off "Segmentation introduces complexity because there's overhead in management" and the risk "Micro-segmentation beyond a reasonable limit loses the benefit of isolation" (S-36).
- **Decision impact:** *the* primary architectural lever. Data residency, blast radius, DLP scope, network posture, CMK, admin delegation and licence cost all follow from environment count and shape. It is also the lever that produces sprawl (see `governance.md` GOV-07, GOV-26).
- **Confidence:** HIGH.
- **Sources:** S-02, S-08, S-33, S-36.

#### SEC-16 — Environment security groups have six documented gaps
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence (all S-26):** "When you associate a security group with an existing environment that has users, you disable all users in the environment who aren't members of the group." "You can't assign security groups to default and developer environment types." "Environments support associating the following group types: Security and Microsoft 365"; "On-premises Windows AD security groups aren't supported." "Members of a security group nested within an environment security group **aren't pre-provisioned or automatically added to the environment**." "If a user isn't part of the assigned security group to the environment, but has the Power Platform Administrator role, the user shows as an active user and can sign in." "All your application users can run in any environments that are secured with a security group, without being a member of the security group." Also: canvas apps can be shared outside the group but such users cannot run them (S-26).
- **Decision impact:** the group is a membership control, not a perimeter. Perimeter claims must be qualified with "except Power Platform admins and application users".
- **Confidence:** HIGH.
- **Sources:** S-26.

#### SEC-17 — The default environment is a permanent, undeleteable, group-less environment in which everyone is a maker
- **Classification:** RISK
- **Origin:** MS
- **Evidence:** "Whenever a new user signs up for Power Apps, they're automatically added to the Maker role of the default environment"; "You can't delete the default environment. You can't manually back up the default environment"; "The default environment is limited to 1 TB of storage capacity"; "The default environment doesn't provide any backup guarantees and shouldn't be used for production workloads"; security column reads "Limited control. All licensed users have the environment maker role" (S-08). "Microsoft 365 Power Platform administrators are no longer automatically assigned the Dataverse system administrator security role in the default environment… **To avoid the possibility of an administrative lockout to the default environment**, we recommend that you assign the system administrator security role to a few trusted users" (S-08). Security groups cannot be assigned to it (S-26).
- **Decision impact:** any solution with a real security requirement must not live in the default environment. Securing the default environment is a governance workstream in its own right (`governance.md` GOV-04, GOV-05).
- **Confidence:** HIGH.
- **Sources:** S-08, S-26.

### 3.4 Connector and connection security

#### SEC-18 — The app is not an authorization layer: the user's rights on the data source decide
- **Classification:** FACT + DECISION CRITERION (foundational)
- **Origin:** MS
- **Evidence:** "**Explicit authentication** means the app user's credentials are used… **Implicit authentication** means the credentials the app maker provided when creating the connection are used. We recommend you use explicit authentication whenever possible. It's more secure. Even in the case of explicit authentication, it's important to remember that **it's the user's rights on a data source that determines what the user can see and edit**." Worked example: an app exposes only the Name column of a SharePoint list, but a user with list permissions to Salary "can create a new app that accesses the **Salary** column. **The permissions that you grant through the user interface of your app don't deny the data source permissions that the user has**" (S-17). "Power Apps and Power Automate *don't* provide users with access to any data assets that they don't already have access to" (S-07).
- **Decision impact:** if the source system cannot express the required authorization, the platform cannot add it — the data must move (to Dataverse, where it can be expressed) or the source must be re-permissioned. This is the single most common source of false security assurance in low-code designs.
- **Confidence:** HIGH.
- **Sources:** S-07, S-17.

#### SEC-19 — Secure implicit connections close the "steal the connection" hole, with eight documented limitations
- **Classification:** FACT + RISK
- **Origin:** MS
- **Evidence:** "Before January 2024, your end users could take the connection that you shared with them and create separate new applications… However, **after January 2024, all newly created shared connections are secured. To secure existing apps, republish them.**" The proxy "only talks to the specific Power App for which it's linked" and limits actions to {Get, Put/Patch, Delete}. Limitations verbatim: "Server and database names are hidden in network traces but visible in the consent dialog. Column names aren't hidden"; "For tabular connectors, the feature only limits CRUD actions… If you have permissions to **Put**, then you have access to **Post**"; "Publishing to an entire tenant… isn't supported"; "There's a known issue when importing an implicitly shared secure connection via a connection reference. **The security isn't set properly in the target environment**"; "There's a known issue importing a solution using a service principal, causing import failure. A workaround is to share the connection with the service principal" (S-18).
- **Decision impact:** legacy apps published before January 2024 are a live exposure until republished — an inventory action, not a design action. The connection-reference known issue means the control can silently fail *after deployment*, coupling this security control to the ALM process (`alm-devops.md` ALM-14).
- **Confidence:** HIGH.
- **Sources:** S-18.

#### SEC-20 — Gateway + Windows authentication is documented as not secure and implicitly shared
- **Classification:** ANTI-PATTERN
- **Origin:** MS
- **Evidence:** "**This type of connection isn't secure because it doesn't rely on end-user authentication**… Since it goes through a gateway, the connector has access to all of the data on that data source. As a result, any information that you can access with the Windows credentials you supply is available to the connector. When you publish the application, you also publish the connection and make it available to your users. This behavior means that your end users can create applications by using this same connection and access the data on that machine" (S-18). Gateway installer control exists tenant-wide but "not at the environment level" (S-34).
- **Decision impact:** on-premises sources reached with a service Windows account must be scoped at the source (a dedicated least-privilege account, a view, a stored procedure surface), because the platform will not scope them.
- **Confidence:** HIGH.
- **Sources:** S-18, S-34.

#### SEC-21 — Connection ownership decides the runtime identity of every flow
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** "When a flow is turned on (enabled), the user turning on the flow needs to own or have permission to use all the connections in the flow"; the `ConnectionAuthorizationFailed` error "indicates that the user trying to activate the flow doesn't have permissions to at least one of the connections"; "**OAuth connections can only be explicitly shared with a user representing a service principal**"; "Ownership of a connection reference can't be transferred to another user from the Solutions area" (S-15).
- **Decision impact:** production automations must be owned by a service principal or a controlled service account, decided at design time; retrofitting ownership after go-live means re-authoring connection references.
- **Confidence:** HIGH.
- **Sources:** S-15.

#### SEC-22 — Flow co-ownership is near-total control; environment admins see all data that flows through
- **Classification:** RISK + RECOMMENDATION
- **Origin:** MS
- **Evidence:** Co-owners can "Manage the properties of the flow… update credentials for a connection", "Edit the flow", "Add or remove other owners, including guest users", "**Delete the flow**". "Only add co-owners as needed… In most cases, if a flow needs to be shared, share it with run-only permissions, which restrict users from viewing the flow run history or making any changes." "Generally, users with full access to workflow tables can edit any flow and view any run history. **Environment admins always have full access to edit workflows and can view all the data that flows through them.**" SPN ownership is recommended for "critical or long-running flows" (S-38).
- **Decision impact:** if a flow carries sensitive payloads, the environment-admin population is part of the data-access population — which pushes the workload into its own environment (SEC-15) and makes admin-count a security metric (SEC-36).
- **Confidence:** HIGH.
- **Sources:** S-38.

#### SEC-23 — Data policies are connector-aware, not connection-aware, and enforce at both design time and run time
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** Enforcement chain: policy saved → cascaded to environments → resources periodically check → violating apps/flows put "in to a *suspended* or *quarantine* state so that it can't operate" → connections "set to a *disabled* state" → running resources "fail at runtime"; "For the most extreme cases, the latency for full enforcement is 24 hours. In most cases, it's within an hour" (S-09). "**Data policies are connector aware, but they don't control connections made using the connector. In other words, data policies can't determine whether the connector is used to connect to a development, test, or production environment**"; "Policies can't be applied at the user level, only at the environment or tenant level"; "Environment data policies can't override tenant-wide data policies"; "If multiple policies are configured for one environment, the most restrictive policy applies" (G-15). Blocked always wins; multiple policies fragment the connector space into 2^n groups, with a worked 3-policy/8-group example (S-40). Non-blockable connector list includes SharePoint, Microsoft 365 Outlook, Teams, OneDrive for Business, Power BI, Dataverse, Approvals, Notifications (S-10). "Because child flows share an internal dependency with the HTTP connector, the grouping that admins choose for HTTP connectors… might affect the ability to run child flows" (S-10).
- **Decision impact:** DLP shapes *what a maker can build*, not *which instance they reach*. Environment separation, not DLP, is what separates dev data from production data.
- **Confidence:** HIGH.
- **Sources:** S-09, S-10, S-40, G-15.

#### SEC-24 — Advanced connector policies invert the model to default-deny, but do not yet cover custom or HTTP connectors
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** "It replaces the Business, Non-Business, and Blocked classification model in classic data policies with **a strict allowlist that blocks all connectors by default**… New connectors added to the platform are automatically blocked." Known limitations verbatim: "**Certified connectors only**… Custom connector and HTTP connector support are planned for a future date"; "**Virtual connectors**: ACP doesn't support virtual connectors and won't support them in the future"; "on non-managed environments, the nonblockable connectors remain nonblockable. **On managed environments… you can block any connector or any action, including those that are nonblockable in classic data policies**." Modes: mixed (default, most restrictive of both) and ACP-only. Design-time enforcement is "rolling out across maker portals" in the order Power Automate → Copilot Studio → Power Apps, and "**Each maker portal's release of design-time enforcement for ACP marks the general availability of ACP for that workload**"; until then ACP is runtime-only for that workload. Removal semantics: removing a group rule or an environment from a group "doesn't automatically remove that rule from the individual environments"; environments "keep their last known ACP configuration" (S-29).
- **Decision impact:** a default-deny connector posture is achievable *today* only for certified connectors, and only fully on managed environments. Custom connectors — the usual route to bespoke back ends — remain governed by the older model.
- **Confidence:** HIGH (documented state as of the fetched page) / MEDIUM (per-workload GA state).
- **Sources:** S-10, S-29.

#### SEC-25 — Endpoint filtering does not survive dynamic values — the most consequential documented gap in the connector plane
- **Classification:** CONSTRAINT + RISK (negative evidence)
- **Origin:** MS
- **Evidence:** Preview. Supported connectors: HTTP, HTTP with Microsoft Entra ID, HTTP Webhook, SQL Server, Azure Blob Storage, SMTP, Browser Automation, UI Automation. "**Endpoint filtering rules don't apply to environment variables, custom inputs, or any endpoint dynamically created at runtime. Only static endpoints are evaluated**"; "This means connector endpoint filtering rules for SQL Server and Azure Blob Storage aren't enforced if the connections are authenticated with Microsoft Entra ID", illustrated with a flow that puts the server and database into variables and "executes successfully". Also: "Power Apps published before October 1, 2020, need to be republished for data policy connector action rules and endpoint rules to be enforced"; for UI automation, "If an expression includes anything other than a literal string, filtering is bypassed"; "Dataverse current environment" is always implicitly allowed (S-30).
- **Decision impact:** never design a control whose only enforcement is endpoint filtering. Where a specific endpoint must be unreachable, enforce it at the target (firewall, private endpoint, source-side authorization) — which is exactly what VNet support and IP firewall are for.
- **Confidence:** HIGH.
- **Sources:** S-30.

#### SEC-26 — Tenant isolation covers Entra-authenticated connectors only and has a documented enforcement hole
- **Classification:** CONSTRAINT + RISK
- **Origin:** MS
- **Evidence:** "Power Platform tenant isolation is different from Microsoft Entra ID-wide tenant restriction. It *doesn't* impact Microsoft Entra ID-based access outside of Power Platform. Power Platform tenant isolation only works for connectors using Microsoft Entra ID-based authentication such as Office 365 Outlook or SharePoint." Warning: "There's a known issue with Azure DevOps connector that results in tenant isolation policy to **not be enforced** for connections established using this connector… we recommend you limit using the connector or its actions using data policies." Default is off — "the default configuration in Power Platform with tenant isolation **Off** is to allow cross-tenant connections to be established seamlessly". "A connection attempt initiated by a guest user, from their host tenant that targets data sources within the same host tenant, isn't evaluated by the tenant isolation rules." "Due to technical limitations, the threshold limit for rules is 500." "It takes about an hour for the latest tenant isolation policy changes to be assessed" (S-11).
- **Decision impact:** cross-tenant exfiltration control is partial by construction. Present it as a reduction of a specific vector, never as containment.
- **Confidence:** HIGH.
- **Sources:** S-11.

### 3.5 Network and platform controls

#### SEC-27 — IP firewall: Dataverse-only, managed-environment-only, audit-mode-by-default, app-users-allowed-by-default
- **Classification:** CONSTRAINT + RISK
- **Origin:** MS
- **Evidence:** "The IP firewall protects your organizational data by ensuring users can only access **Microsoft Dataverse** from allowed IP locations." Prerequisite: "The IP firewall is a feature of managed environments." Defaults: "**Allow access for Microsoft trusted services**… Enabled by default"; "**Allow access for all application users**… Enabled by default"; "**Enable IP firewall in audit-only mode**… Enabled by default" — in audit-only mode it "allows requests regardless of their IP address". Limits: "up to 4,000 alphanumeric characters and allows a maximum of 200 IP ranges"; changes take "about 5-10 minutes". Warnings: "When **Allow Access for Microsoft trusted services** and **Allow access for all application users** are disabled, some services that use Dataverse, such as Power Automate flows, might no longer work"; "By default, TDS endpoint is turned on"; "IP firewall audit logs aren't supported in tenants enabled for bring-your-own-key (BYOK) encryption keys". Licensing: managed environments **plus** users holding "Microsoft 365 or Office 365 A5/E5/G5" or an M365 A5/E5/F5/G5 Compliance / F5 Security & Compliance / Information Protection and Governance / Insider Risk Management subscription. SPN filtering requires an API-based per-user allowlist (`isallowedbyipfirewall`) (S-12).
- **Decision impact:** "restrict to corporate network" is achievable for Dataverse, at a licensing cost that is often larger than the Power Platform cost itself, and with a deliberate rollout (audit mode ≥ 1 week is the documented recommendation).
- **Confidence:** HIGH.
- **Sources:** S-12.

#### SEC-28 — IP-address-based cookie binding is a separate managed-environment control against session replay
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** "The IP address-based cookie binding feature applies only to managed environments with Dataverse. It prevents session hijacking exploits in Dataverse" (S-21); Dataverse "compares the IP address of the cookie's origin against the IP address of the computer making the request. If the two are different, the attempt is blocked" (S-34). Shares the reverse-proxy configuration with the IP firewall (S-12).
- **Confidence:** HIGH.
- **Sources:** S-12, S-21, S-34.

#### SEC-29 — CMK is a scoped control with a documented exclusion list and a self-inflicted-outage risk
- **Classification:** CONSTRAINT + RISK + TRADE-OFF
- **Origin:** MS
- **Evidence:** Excluded from CMK, verbatim: "**The connection settings for connectors continue to be encrypted with a Microsoft-managed key**"; "**Power Platform environment settings continue to be encrypted with a Microsoft-managed key**"; "**Power Apps display names, descriptions, and connection metadata continue to be encrypted with a Microsoft-managed key**"; maker welcome content and solution-checker download results also excluded (S-13). Prerequisites: managed environments + the same E5-class licence list as the IP firewall; key vault with soft-delete and purge protection; RSA/RSA-HSM 2048 or 3072; enterprise policy region must match the environment's region. Operational: "The environment is disabled when it's added to the enterprise policy… The encryption can take up to four days to complete"; "Trial and Teams environment types can't be added to the enterprise policy"; restore is "restricted to the same environment that the backup was taken from or to another environment that is encrypted with the same customer-managed key"; reset "deletes the environment's encrypted data including backups" and reverts to the Microsoft-managed key; the previous key version "must not be disabled or deleted for, at least, 28 days". Insider risk, stated by Microsoft: "a malicious administrator… might use the manage keys feature to create a key and use it to lock your environments in the tenant… **When environments are locked, they can't be accessed by anyone, including Microsoft support. Environments that are locked become disabled and data loss can occur**"; mitigation is separation of duties between the Key Vault admin and the Power Platform admin (S-13). Audit retention is not available for CMK environments (S-27); IP firewall audit is unsupported under BYOK (S-12).
- **Decision impact:** CMK satisfies a specific compliance clause about at-rest key custody. It does not encrypt "everything", it constrains backup/restore/copy topology, and it introduces a new single point of failure that must be governed.
- **Confidence:** HIGH.
- **Sources:** S-12, S-13, S-27.

#### SEC-30 — VNet support removes public-internet exposure for a defined set of outbound paths, and pins the environment
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence:** Subnet delegation for "both Dataverse plugins and connectors"; GA connector list: SQL Server, Azure SQL Data Warehouse, Azure Queues, custom connectors, Azure Key Vault, Azure File Storage, Azure Blob Storage, HTTP with Microsoft Entra ID (preauthorized), Snowflake, Databricks, AI Search. Limitations verbatim: "**Dataverse low-code plugins that use connectors aren't supported** until those connector types are updated to use subnet delegation"; "Azure-aware plugins don't support VNet". Environment support: Production/Default/Sandbox/Developer **Yes**; Trial and Dataverse for Teams **No**. Immutability: "You can't change the IP address range of the subnet after it's delegated… If you change the IP address range, the delegation configuration breaks and the environment stops working"; same for DNS. "You can't reuse the same subnet in multiple enterprise policies." "Each Power Platform environment is linked to one virtual network subnet." Region pairing is mandatory (table of Power Platform region → Azure region pair) and failover requires delegating both. "Power Platform requires the endpoint to present a TLS certificate with the complete chain. You can't add your custom root CA to the list of well-known CAs." "Internet-bound access is available by default from plugins and connectors in a subnet-delegated environment" — a NAT gateway is the documented way to control it. Sizing: 25–30 IPs per production environment, 6–10 per non-production, plus 5 reserved per subnet. "you must associate an Azure subscription with the Power Platform tenant" (S-16). Restore requires the target to be in the same enterprise policy (D-17).
- **Decision impact:** private connectivity is real but rewrites the environment's operational envelope: region pinning, subnet immutability, Azure subscription dependency, an explicit check that every plug-in and connection can reach its target privately ("**Before you enable… check the code of the plugins and the connectors. Update the URLs and connections to work with private connectivity**", S-16), and no trial/Teams environments.
- **Confidence:** HIGH.
- **Sources:** S-16, D-17.

#### SEC-31 — The on-premises gateway is an outbound-only relay whose blast radius is the credential you give it
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence:** "The gateway uses Azure Relay to allow access to on-premises resources securely… The gateway uses these outbound ports: TCP 443, 5671, 5672, and 9350–9354. The gateway doesn't require inbound ports." Roles: Admin (created by the installer), Connection creator, Connection creator with sharing. "You can control who can install an on-premises data gateway in your tenant, **but not at the environment level**." "Use standard network controls on the gateway server to limit the data sources the gateway can access." Clustering is recommended "to meet different compliance or security requirements for different data sources" (S-34). Combined with SEC-20: the connector reaches everything the supplied Windows credential reaches.
- **Decision impact:** gateway design (which cluster, which service account, which network segment) is a security design activity, and the inability to scope installation per environment is a governance gap to compensate for.
- **Confidence:** HIGH.
- **Sources:** S-18, S-34.

### 3.6 Application-surface security (differences that matter)

#### SEC-32 — Power Pages is a distinct security product: web roles + table permissions, with default-deny and specific footguns
- **Classification:** FACT + RISK
- **Origin:** MS
- **Evidence:** Model components: site visibility, authenticated users (Dataverse **contacts**), web roles, table permissions, page permissions, HTTP headers/CORS, security scan (S-19). "**Access to Dataverse records is automatically restricted in Power Pages** when using forms, lists, Liquid, the Portals Web API"; "For a table permission to take effect, it has to be associated to one or more web roles"; access types Global (all records), Contact, Account, Self, Parent, Custom (FetchXML filter; enhanced-authorization sites only, preview); "Polymorphic lookups are not supported when configuring parent-child table permissions"; deactivating a parent permission makes children ineffective while they remain active (S-20). "All authenticated users, or contacts, are automatically assigned to the Authenticated Users web role. Anonymous, or unauthenticated, users can visit a site and get access to assets through the Anonymous Users web role"; "**Because users can be assigned multiple web roles, they can get cumulative access to site resources**" (S-19). Site visibility: "**All sites you create in Power Pages are private by default**"; "Websites in developer environments can't be made public"; "Be cautious when editing a public site. Changes are visible to external users immediately". Private-site access list: "**Users configured to access the private site are stored in an environment variable. Any Dataverse security role with permission to modify the environment variable can add or remove user access to the private site.**" Known issue: "A private Power Pages website doesn't work if you turn off Microsoft Entra authentication" (S-37).
- **Decision impact:** external-facing requirements move the whole security design onto a second model that must be reviewed independently of Dataverse roles. The environment-variable-based private access list is a privilege-escalation path worth an explicit control.
- **Confidence:** HIGH.
- **Sources:** S-19, S-20, S-37.

#### SEC-33 — Attack surface by application type (synthesis)
- **Classification:** DECISION CRITERION
- **Origin:** MS (components) + INF (comparison)
- **Evidence/synthesis:**

| Surface | Who authenticates | What authorizes | Principal risks | Controls that actually bite |
|---|---|---|---|---|
| **Canvas app** | Entra (internal/B2B) | Data-source rights (explicit) or maker credentials (implicit); app sharing | Implicit connections; oversharing; consent fatigue; app UI mistaken for authorization | Explicit auth; secure implicit connections + republish; sharing limits; DLP/ACP; app access control (S-17, S-18, S-24, S-21) |
| **Model-driven app** | Entra | Dataverse RBAC only (roles/BU/teams/sharing/column security) | Over-granted roles; sysadmin sees everything; sharing sprawl | Role design, BU model, column security, audit (S-02, S-03, S-13, S-27) |
| **Power Pages** | Entra External ID / Microsoft / LinkedIn / other providers; or anonymous | Web roles + table permissions + page permissions | Anonymous exposure; Global access type; expired certs/auth keys; missing WAF | Site visibility, table permissions, WAF, security scan, PPAC recommendations (S-19, S-20, S-35, S-37) |
| **Power Automate** | Runs as a connection owner, not as the invoker (unless configured) | Connection ownership; co-owner rights; run-only | Ownership tied to a leaver; co-owner = full control; env admins see payloads | SPN ownership, run-only sharing, sharing limits, block unmanaged customizations for read-only support (S-38, S-24, D-12) |

- **Decision impact:** "we secured the app" is meaningless without naming the surface. Multi-surface solutions need a per-surface security statement.
- **Confidence:** MEDIUM (comparison is analyst synthesis over MS components).
- **Sources:** S-02, S-13, S-17, S-18, S-19, S-20, S-24, S-27, S-35, S-37, S-38, D-12.

#### SEC-34 — Auditing: what it captures, what it costs, what it never sees
- **Classification:** CONSTRAINT + DECISION CRITERION
- **Origin:** MS
- **Evidence:** Levels: environment → table → column; captures create/update/delete, sharing changes, N:N association, security-role changes, audit-log deletion, and user access ("Log access"). "**Auditing isn't supported on table or column definition changes or during authentication. Furthermore, auditing doesn't support retrieve operations or export operations**" — read/export logging requires activity logging into Purview, and "The option to turn on activity logging is only visible when the minimum Microsoft Office licensing requirements are met"; "User access or activity logging is sent to Purview for production environments only". A list of non-auditable system tables is published. Retention: "Each audit log is stamped with the currently active retention period. **Changing the retention period here doesn't change the retention period for already existing records**"; default Forever, custom max 24,855 days; "The audit retention period isn't available for… environments encrypted with a customer's own encryption key". Storage: "Dataverse stores audit logs and they consume log storage capacity". Operational: "**Exporting audit logs isn't currently supported**. Use the Web API or SDK"; large attribute values capped at "5 KB or about 5,000 characters"; deletion runs at "approximately 100 million records per day"; when column auditing is off, before/after values go to Purview as "\*" (S-27).
- **Decision impact:** an audit requirement is a licence + capacity + retention design decision taken before build, and it conflicts with CMK. "We can prove who read the record" requires Purview activity logging, not Dataverse auditing.
- **Confidence:** HIGH.
- **Sources:** S-27.

#### SEC-35 — The security posture tooling is useful for hygiene and explicitly not for assurance
- **Classification:** CONSTRAINT (negative evidence)
- **Origin:** MS
- **Evidence:** "This is a preview feature"; "Microsoft is actively working on updates to the **Security** area… we don't plan to invest in changes to the current preview implementation of logic or the security score calculation… **We recommend using the security score for evaluation purposes only at this time.**" Prerequisite: tenant-wide analytics on, up to 24 h to populate; score refreshes every 24 h. "Although the recommendations span all environments, **you can act on them only in managed environments**." Known limitation: "Only tenant administrators can manage the administrator privileges." Recommendation triggers include: environments with **more than 10 administrators**; auditing off; no tenant-level data policy; no Virtual Network policy; no environment security group; restricted guest access off; IP firewall not configured; cookie binding not configured; no sharing limit; tenant isolation off (S-01). Resource-level security recommendations: apps without a valid owner (active in the last 90 days), apps shared with **Everyone**, Pages sites without WAF, expiring SSL certificates and authentication keys (90-day horizon) — all "Managed environments only: Yes" except the Copilot Studio DLP one (S-35). Environment-level administrator review flags environments with **more than 20** users holding System Administrator (S-21).
- **Decision impact:** the score is a backlog generator, not evidence. Assurance artefacts must be built from configuration state + audit, not from the score.
- **Confidence:** HIGH.
- **Sources:** S-01, S-21, S-35.

#### SEC-36 — Administrative privilege is the largest single lever, and Microsoft has already reduced it by default
- **Classification:** RECOMMENDATION + FACT
- **Origin:** MS
- **Evidence:** "Power Platform, Dynamics 365, and Global Administrators are no longer automatically assigned the Dataverse System Administrator role. **They must self-elevate** before assigning Dataverse roles" (S-26). "Power Platform administrator: This role can perform all admin functions in Power Platform, **regardless of security group membership** at the environment level"; "Dynamics 365 administrator… only for environments where it belongs to the security group" (S-33). Recommended strategies verbatim: "Minimize the number of critical impact accounts"; "Avoid permanent or standing access by using the just-in-time (JIT) features"; "Use Privileged Identity Management (PIM)… to manage, control, and monitor the use of these high-privilege roles"; "Decommission administrative accounts that aren't being used" (S-33, S-03 of governance/G-03). Column security never applies to System Administrator (S-13); environment admins can read all flow data (S-38).
- **Decision impact:** admin count is a security *design* variable, not an operations detail: it caps what column security, flow confidentiality and separation of duties can promise.
- **Confidence:** HIGH.
- **Sources:** S-13, S-21, S-26, S-33, S-38.

#### SEC-37 — Threat model for a Power Platform workload (synthesis)
- **Classification:** DECISION CRITERION
- **Origin:** INF over MS evidence
- **Evidence/synthesis:**

| Threat | Concrete Power Platform vector | Documented mitigation | Residual (documented) |
|---|---|---|---|
| Unauthorised access | Membership without role, or role without membership; default environment openness | Security group + role design + guest restriction | PP admins and application users bypass security groups (SEC-16, SEC-05) |
| Privilege escalation | Additive roles; System Customizer/Environment Maker in production; SPN with System Administrator | Least-privilege roles, environment role separation, delegated deployment SPNs scoped per stage | Deploying plug-ins *requires* System Administrator in the target (ALM-11); grants cannot be subtracted (SEC-08) |
| Data leakage (unintentional) | Oversharing (Everyone), broad DLP groups, Pages Global table permissions | Sharing limits, DLP/ACP, table-permission review, PPAC recommendations | Sharing limits apply only to future sharing (SEC-38) |
| Data exfiltration (intentional) | Environment hopping via a non-blockable connector; runtime-computed endpoints; export to Excel | Tenant isolation, ACP default-deny, IP firewall, Purview activity logging | DLP is scoped by Microsoft to *unintentional* exposure; endpoint filtering ignores dynamic endpoints (SEC-25, SEC-C2) |
| Credential compromise | Implicit/shared connections; gateway service accounts; app-registration secrets | Explicit auth, secure implicit connections, Key Vault + managed identity (plug-ins), SPN ownership | Secrets consumable by only three component types (SEC-07); managed identity only for plug-ins (SEC-06) |
| Malicious/uncontrolled connector | Custom connector to an arbitrary API; HTTP connector | Classic DLP for custom/HTTP; endpoint filtering (partial); ACP for certified | ACP does not cover custom or HTTP connectors (SEC-24) |
| Insecure integration | Public endpoints; TLS chain issues; on-prem credential scope | VNet support / private endpoints; gateway clustering | Custom root CAs unsupported; internet egress open by default in delegated subnets (SEC-30) |
| Excessive permissions | >20 System Administrators; >10 environment admins | PIM/JIT, PPAC recommendations, admin review | Admin review page shows only default-BU roles unless toggled; 24 h lag (S-21) |
| Unmanaged solutions in production | Ad-hoc edits creating unmanaged layers | Block unmanaged customizations; managed-only production | Dataflows exempt; a documented list of first-party features breaks (ALM-15) |
| Citizen-development risk | Personal-productivity assets becoming business-critical without ALM, ownership or support | Environment routing, sharing limits, actions page, environment strategy | Detection is weekly/reactive; full detail only for managed environments (GOV-13) |
| Key-custody self-harm | CMK key revoked by a malicious or careless admin | Separation of Key Vault vs Power Platform admin duties; soft-delete + purge protection | "data loss can occur" is Microsoft's own wording (SEC-29) |

- **Confidence:** MEDIUM (structure is analyst synthesis; each cell traces to a cited finding).
- **Sources:** as per referenced findings.

#### SEC-38 — Sharing limits and "Everyone" are the two levers against oversharing, both with caveats
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS
- **Evidence:** Managed-environment sharing rules cover canvas apps (exclude security groups; cap individuals), solution-aware cloud flows (on/off), and agents (editor/viewer granularity). "**Sharing rules are enforced when users try to share… This restriction doesn't impact any existing users who already have access** before the application of the sharing rules. However, if an app, flow, or agent is out of compliance after rules are set, **only unsharing is allowed** until it is compliant"; "it may take up to an hour for them to start getting enforced" (S-24). "**The Share with Everyone feature is disabled by default**… The **Everyone** group for your organization contains all users who have ever logged in to your tenant, **which includes guests and internal members**… the membership of the **Everyone** group can't be edited nor viewed" (G-03).
- **Decision impact:** oversharing is retrofit-resistant: limits are forward-looking, so the audit of already-shared assets is a separate remediation workstream.
- **Confidence:** HIGH.
- **Sources:** S-24, G-03.

#### SEC-39 — App access control (preview) constrains which apps may run in an environment
- **Classification:** FACT
- **Origin:** MS
- **Evidence:** "The app access control feature applies only to managed environments. It prevents data exfiltration by controlling which apps are allowed and blocked in each environment" (S-21); listed as a managed-environment capability (S-23) and as a data-protection control (S-34).
- **Conditions:** preview; depth not verified (SEC-U-06).
- **Confidence:** MEDIUM.
- **Sources:** S-21, S-23, S-34.

#### SEC-40 — Purview integration provides discovery/classification, not enforcement inside Dataverse
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** "The integration of Microsoft Purview with Microsoft Dataverse enables… automated data discovery and sensitive data classification"; the described outcome is that admins can "either tell the maker how to change the data to follow your policies or use safeguards to secure it" (S-34). WAF SE:03 requires classification labels to "influence workload design, implementation, and security prioritization" (S-05).
- **Decision impact:** classification is an input to the design (which environment, which controls), not a runtime control on Dataverse rows.
- **Conditions:** depth of any label-driven enforcement not verified (SEC-U-04).
- **Confidence:** MEDIUM.
- **Sources:** S-05, S-34.

---

## 4. Security decision criteria (REQUIREMENT → SECURITY CONSTRAINT → ARCHITECTURAL CONSEQUENCE)

| # | Requirement | Security constraint (evidence) | Architectural consequence |
|---|---|---|---|
| 1 | Population A must never see population B's data | Additive privileges; no subtraction (SEC-08) | Design BU/ownership before the data model; least-privilege roles from day one |
| 2 | Strict isolation between workloads | Environment is the security boundary; cross-environment data access is not supported (SEC-15) | One environment per isolation domain; accept licence + ALM + admin overhead |
| 3 | Only a named group may enter | Security groups don't apply to default/developer; PP admins and app users bypass (SEC-16, SEC-05) | Non-default environment + Entra security group + documented bypass exceptions |
| 4 | Row scoping by organisational unit | Ownership type fixed at table creation; owning BU immutable without matrix feature (SEC-09) | Ownership decision is a schema decision; matrix BU = migration programme (SEC-10) |
| 5 | Field-level confidentiality | Column security excludes sysadmin, lookups, formula, primary-name, system columns; leaks via calculated/composite (SEC-13) | Separate table for the sensitive attribute, or accept the exclusions and cap the admin population |
| 6 | Confidential even from administrators | Not achievable in Dataverse (SEC-13, SEC-22, SEC-36) | Keep the attribute outside Dataverse, or reduce admins to an auditable, JIT-only set |
| 7 | External partners | Guest access to Dataverse restricted by default; restriction is Dataverse-only (SEC-04) | Dedicated environment for B2B, explicit guest decision, no non-Dataverse apps assumed protected |
| 8 | Public / customer audience | Pages web roles + table permissions; anonymous role; default-deny but Global access type available (SEC-32) | Pages in its own environment; anonymous-permission review; WAF + cert/key lifecycle in the operating model |
| 9 | Restrict access to corporate network | IP firewall: managed env, Dataverse only, E5-class licences, app users allowed by default (SEC-27) | Managed environment + licence budget + SPN allowlist + audit-mode rollout |
| 10 | No back-end exposed to internet | VNet support: fixed connector list, no trial/Teams, immutable subnet/DNS, region pairing (SEC-30) | Azure subscription dependency, region pinning, plug-in/connection audit before enablement |
| 11 | Customer-controlled keys | CMK: managed env + E5-class, exclusion list, backup/restore constrained, revocation = outage (SEC-29) | CMK only where a clause demands it; separation of Key Vault and Power Platform admin duties |
| 12 | No secrets in the solution | Key Vault secrets consumable by flows / agents / custom connectors only (SEC-07) | Secret-dependent logic moves to flow, custom connector, or plug-in with managed identity (SEC-06) |
| 13 | Automation must survive personnel change | Flow runs as connection owner; OAuth connections shareable only with an SPN user (SEC-21, SEC-22) | SPN-owned flows and connections designed in, not retrofitted |
| 14 | Only approved services reachable | Non-blockable connector list; ACP covers certified only; endpoint filtering ignores dynamic endpoints (SEC-23, SEC-24, SEC-25) | Layered posture: ACP (certified) + classic DLP (custom/HTTP) + target-side controls |
| 15 | No cross-tenant data movement | Tenant isolation covers Entra connectors only; ADO gap (SEC-26) | Tenant isolation + data policies + acceptance of residual vectors |
| 16 | Prove who saw the data | Dataverse audit excludes retrieve/export; Purview activity logging is licence-gated; not available with CMK (SEC-34) | Audit strategy (scope, retention, capacity, licences) fixed before go-live |
| 17 | No unreviewed change in production | Environment roles + managed solutions + block unmanaged customizations (SEC-36, ALM-15) | Makers hold no maker rights in prod; support access via co-ownership on managed flows |
| 18 | Assurance report to a regulator | Security score is preview and "for evaluation purposes only" (SEC-35) | Assurance built from configuration evidence + audit exports, not from the score |
| 19 | Immediate revocation on termination | Token lifetime ~1 h without CAE (SEC-03) | CAE + group-driven role assignment (SEC-11) rather than manual role removal |
| 20 | Data residency | Environment bound to a geography at creation; enterprise policies region-matched (SEC-15, SEC-29, SEC-30) | Region decided per environment at creation; multi-region = multi-environment |

---

## 5. Security anti-patterns (evidence-backed)

- **SEC-A1 — Using the app UI as the authorization layer.** Contradicted verbatim by S-17 (the Salary-column example). *Instead:* enforce in the data source; move to Dataverse if the source cannot express it.
- **SEC-A2 — Shared privileged accounts / a "service account" everyone knows.** Cuts against the documented SPN model (S-38), against auditability (S-27, audit records the acting identity) and against Microsoft's stated privileged-access strategies (S-33). *Instead:* service principals with per-purpose scopes; PIM for humans.
- **SEC-A3 — Everyone is a maker in production, or work lives in the default environment.** S-08: all licensed users hold Environment Maker in default; no backup guarantees; no security group possible. *Instead:* environment routing + a governed production environment (`governance.md` GOV-05, GOV-08).
- **SEC-A4 — Broad Organization-level privileges "to unblock the project".** S-02 states the grant cannot be walked back. *Instead:* time-boxed elevation, not permanent role widening.
- **SEC-A5 — Direct user→role assignment at scale.** S-02/S-34 document the group-team pattern; direct assignment defeats JML automation. *Instead:* Entra group → group team → role.
- **SEC-A6 — Record sharing as the access model.** S-02 explicitly frames sharing as an exception and as less performant and harder to troubleshoot.
- **SEC-A7 — Implicit/shared connections for sensitive data; Windows-auth gateway connections shared with users.** S-18 documents both the exposure and the post-January-2024 remediation (republish).
- **SEC-A8 — Treating DLP as an exfiltration control.** Microsoft scopes data policies to reducing "the risk of users **unintentionally** exposing organizational data" (S-09). T4 evidence describes deliberate cross-environment bypass (S-41). *Instead:* tenant isolation + ACP + target-side controls + monitoring; state DLP's scope honestly.
- **SEC-A9 — Designing a control that depends on endpoint filtering.** S-30 documents non-enforcement for variables and dynamic endpoints.
- **SEC-A10 — Secrets in app formulas, flow actions or custom-connector definitions.** S-28 provides the sanctioned path; canvas apps have none, which is precisely why the anti-pattern appears.
- **SEC-A11 — Leaving IP firewall in audit-only mode and calling it enabled**; or enabling it while leaving "Allow access for all application users" on and assuming SPNs are constrained. Both are documented defaults (S-12).
- **SEC-A12 — Turning on CMK without separating Key Vault and Power Platform admin duties.** Microsoft documents the malicious-admin lock scenario and the mitigation (S-13).
- **SEC-A13 — Public Power Pages site with an unreviewed Anonymous Users web role or a Global-access table permission.** S-19/S-20 make the cumulative-role and all-records semantics explicit.
- **SEC-A14 — Production development / makers holding maker rights in production.** S-33 recommendation 2 verbatim: "**Don't allow maker permissions in test and production environments**".
- **SEC-A15 — No separation between who builds and who deploys.** Delegated deployments exist precisely to break this (`alm-devops.md` ALM-11).

---

## 6. Unknowns (UNKNOWN)

- **SEC-U-01** — Hierarchy security (manager/position hierarchies) was not fetched; its interaction with modernised BUs and with column security is unverified. Do not encode.
- **SEC-U-02** — Whether ACP design-time enforcement has reached the Power Apps maker portal (the documented GA marker per workload) as of 2026-09-03. S-29 states the rollout order only.
- **SEC-U-03** — Current status of the two S-18 known issues (secure implicit connection via connection reference; SPN solution import). Both directly affect whether a security control survives deployment.
- **SEC-U-04** — Depth of Purview sensitivity-label enforcement over Dataverse rows/columns (discovery and classification are documented; enforcement is not).
- **SEC-U-05** — Masking-rule mechanics and limits (dedicated page not fetched).
- **SEC-U-06** — App access control (preview): scope, bypasses, and interaction with sharing limits.
- **SEC-U-07** — Whether any Power Platform control can restrict *export to Excel* / TDS-endpoint reads beyond privacy-related privileges and the IP firewall; S-12 notes the TDS endpoint is on by default.
- **SEC-U-08** — Power Pages WAF: cost, managed-rule coverage and limits (only the recommendation and the configuration pointer were seen).
- **SEC-U-09** — Whether guest access restriction is GA or preview (see SEC-C1).

---

## 7. Conflicts (CONFLICTED)

- **SEC-C1 — Guest access GA state.** S-25 (feature page, ms.date 2026-03-09) carries no preview banner and states the new-environment default plainly. S-33 (adoption guidance, ms.date 2026-03-26) links the same capability as "#guest-access-preview". More authoritative: the feature page. **Resolution:** treat behaviour as documented, GA state as UNKNOWN; re-verify before encoding.
- **SEC-C2 — Is DLP a data-exfiltration control?** S-09 (Microsoft) frames data policies as guardrails against *unintentional* exposure. S-41 (T4, dev.to, 2025-03-10) claims deliberate bypass by moving data through a ubiquitous connector (SharePoint) across environments with different policies, summarised as "if DLP was a house, it would have a fence with its neighbour, but could simply walk onto the road to get around the fence", with the author's own conclusion that DLP "lowers the risk, it doesn't remove". **Resolution:** not a contradiction — they answer different questions. The conflict is with common *practice*, which presents DLP as containment. Record the scope explicitly; the mitigations the T4 author proposes (tenant-wide policy, separate default/Teams policies, service accounts for production, controlled developer-environment access) align with Microsoft's own guidance (G-15). Confidence in the bypass mechanism: LOW-MEDIUM (T4, not reproduced).
- **SEC-C3 — Where should governance tooling come from?** Historically the CoE Starter Kit; now "The Power Platform CoE Starter Kit is no longer actively maintained" (G-09). Affects security operations that were built on kit components. Full treatment in `governance.md` GOV-12.

---

## 8. Deferred to other areas

- Licensing arithmetic of the E5-class prerequisites for IP firewall/CMK/VNet, Entra Conditional Access, and managed environments → `licensing-cost.md` **LC-30**; the dependency is security-owned, the economic population/cost model is cost-owned.
- Monitoring, alerting and incident response mechanics (Application Insights export, Monitor, run history) → **Area 11 (Operations and Support)**; SE:08/SE:10 (S-05) are noted but not researched here.
- Delegation/query behaviour of security filters at scale (performance of BU/team/sharing models) → `performance-scale.md` **PF-U-07**. No Microsoft latency/throughput curve was found; any BU/team/sharing-heavy design therefore carries a representative-load validation obligation rather than a numeric allowance.
- Data classification and residency as data-model concerns → Area 03 `data-architecture.md`.
- Deployment identity, approvals and separation of duties in pipelines → `alm-devops.md` (ALM-11, ALM-20).

---

## 9. Verification list before pack encoding (mandatory)

1. ACP GA state per maker portal (SEC-U-02) and whether custom/HTTP connector rule types shipped (S-29).
2. Endpoint filtering preview → GA, and whether the dynamic-endpoint gap closed (S-30).
3. Security score / Security Hub: whether the preview logic was replaced (S-01 says no investment in the current implementation).
4. Guest access GA state (SEC-C1).
5. S-18 known issues (SEC-U-03) — both are security-control-defeating.
6. VNet connector coverage list and low-code plug-in support (S-16 changes often).
7. CMK exclusion list (S-13) — it grew during the research window.
8. Managed-environment licence enforcement milestone (February 2027, G-11) — changes the cost of every security control that requires managed environments.
9. Whether administrator-privileges and app-access-control previews reached GA (S-21).

---

## 10. Implications for the aisa knowledge model (pointers, not pack content)

- Security requirements should be captured as **signals that name the plane** (`isolation_required`, `row_scoping_required`, `column_confidentiality_required`, `external_audience`, `network_restricted_access_required`, `customer_managed_keys_required`, `read_audit_required`, `secretless_integration_required`, `separation_of_duties_required`). The plane determines which architectural lever moves.
- Several constraints are **irreversible** and therefore belong to early Discovery, not to Options: table ownership type, publisher (see `alm-devops.md`), environment region, Dynamics 365 apps installed at environment creation, and the "grants cannot be subtracted" property of Dataverse roles.
- Several controls carry **licence dependencies outside Power Platform** (E5-class for IP firewall/CMK; Entra P1/P2 for Conditional Access; Purview for read auditing). These belong in the financial lens, not only the governance lens.
- At least four documented controls are **partial by design** (DLP scope, tenant isolation, endpoint filtering, guest restriction). The pack should force an explicit statement of residual risk rather than a binary "control in place".

---

## 11. Source register

Kind: fetched (retrieved 2026-09-03, `ms.date` shown) / search-verified / signals (T3/T4).

| Id | Tier | Kind | Title | URL | ms.date |
|---|---|---|---|---|---|
| S-01 | T1 | fetched | Security overview (PPAC Security area, score, recommendations) | https://learn.microsoft.com/en-us/power-platform/admin/security/security-overview | 2026-04-10 |
| S-02 | T1 | fetched | Security concepts in Microsoft Dataverse | https://learn.microsoft.com/en-us/power-platform/admin/wp-security-cds | 2025-06-03 |
| S-03 | T1 | fetched | Security roles and privileges for Dataverse | https://learn.microsoft.com/en-us/power-platform/admin/security-roles-privileges | 2025-12-09 |
| S-04 | T1 | fetched | Modernized business units security | https://learn.microsoft.com/en-us/power-platform/admin/modernized-business-units-security | 2025-03-13 |
| S-05 | T1 | fetched | WAF — Security checklist (SE:01–SE:10) | https://learn.microsoft.com/en-us/power-platform/well-architected/security/checklist | 2025-08-18 |
| S-06 | T1 | fetched | WAF — Security design principles | https://learn.microsoft.com/en-us/power-platform/well-architected/security/principles | 2025-08-18 |
| S-07 | T1 | fetched | Security and governance considerations in Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/governance-considerations | 2026-04-07 |
| S-08 | T1 | fetched | Power Platform environments overview | https://learn.microsoft.com/en-us/power-platform/admin/environments-overview | 2026-05-28 |
| S-09 | T1 | fetched | Data policies (overview, enforcement, latency) | https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention | 2026-04-07 |
| S-10 | T1 | fetched | Connector classification (incl. non-blockable list) | https://learn.microsoft.com/en-us/power-platform/admin/dlp-connector-classification | 2026-04-07 |
| S-11 | T1 | fetched | Restrict cross-tenant inbound and outbound access (tenant isolation) | https://learn.microsoft.com/en-us/power-platform/admin/cross-tenant-restrictions | 2025-04-23 |
| S-12 | T1 | fetched | IP firewall in Power Platform environments | https://learn.microsoft.com/en-us/power-platform/admin/ip-firewall | 2026-05-18 |
| S-13 | T1 | fetched | Manage your customer-managed encryption key | https://learn.microsoft.com/en-us/power-platform/admin/customer-managed-key | 2026-05-18 |
| S-14 | T1 | fetched | Manage application users in the PPAC | https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users | 2026-04-03 |
| S-15 | T1 | fetched | Use a connection reference in a solution | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-connection-reference | 2026-01-09 |
| S-16 | T1 | fetched | Microsoft Azure Virtual Network support for Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/vnet-support-overview | 2026-07-28 |
| S-17 | T1 | fetched | Connecting and authenticating to data sources | https://learn.microsoft.com/en-us/power-platform/admin/security/connect-data-sources | 2023-08-25 |
| S-18 | T1 | fetched | Overview of connectors for canvas apps (Security and types of authentication) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections-list | 2026-01-13 |
| S-19 | T1 | fetched | Power Pages security | https://learn.microsoft.com/en-us/power-pages/security/power-pages-security | 2026-07-16 |
| S-20 | T1 | fetched | Set table permissions in Power Pages | https://learn.microsoft.com/en-us/power-pages/security/table-permissions | 2026-02-28 |
| S-21 | T1 | fetched | Identity and access management (PPAC Security) | https://learn.microsoft.com/en-us/power-platform/admin/security/identity-access-management | 2026-03-09 |
| S-22 | T1 | fetched | Use environment variables in Power Platform solutions | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables | 2026-01-09 |
| S-23 | T1 | fetched | Managed environments overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview | 2026-02-23 |
| S-24 | T1 | fetched | Limit sharing (managed environments) | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-sharing-limits | 2026-03-02 |
| S-25 | T1 | fetched | Control guest access to Power Platform environments | https://learn.microsoft.com/en-us/power-platform/admin/security/guest-access | 2026-03-09 |
| S-26 | T1 | fetched | Control user access to environments with security groups and licenses | https://learn.microsoft.com/en-us/power-platform/admin/control-user-access | 2026-08-26 |
| S-27 | T1 | fetched | Manage Dataverse auditing | https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing | 2026-04-08 |
| S-28 | T1 | fetched | Use environment variables for Azure Key Vault secrets | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables-azure-key-vault-secrets | 2026-01-09 |
| S-29 | T1 | fetched | Advanced connector policies | https://learn.microsoft.com/en-us/power-platform/admin/advanced-connector-policies | 2026-07-15 |
| S-30 | T1 | fetched | Connector endpoint filtering (preview) | https://learn.microsoft.com/en-us/power-platform/admin/connector-endpoint-filtering | 2026-06-15 |
| S-31 | T1 | fetched | Power Platform managed identity overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-identity-overview | 2025-09-18 |
| S-32 | T1 | fetched | Column-level security | https://learn.microsoft.com/en-us/power-platform/admin/field-level-security | 2025-11-19 |
| S-33 | T1 | fetched | Configure identity and access management (adoption guidance) | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/conditional-access | 2026-03-26 |
| S-34 | T1 | fetched | Establish data protection and privacy controls | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/data-protection | 2025-05-14 |
| S-35 | T1 | fetched | View security recommendations (Actions page) | https://learn.microsoft.com/en-us/power-platform/admin/security-recommendations | 2025-05-28 |
| S-36 | T1 | fetched | WAF — Build a segmentation strategy (SE:04) | https://learn.microsoft.com/en-us/power-platform/well-architected/security/segmentation | 2025-08-18 |
| S-37 | T1 | fetched | Site visibility in Power Pages | https://learn.microsoft.com/en-us/power-pages/security/site-visibility | 2026-03-17 |
| S-38 | T1 | fetched | Understand flow ownership and access | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/understand-access-to-flows | 2025-07-11 |
| S-40 | T1 | fetched | Combined effect of multiple data policies | https://learn.microsoft.com/en-us/power-platform/admin/dlp-combined-effect-multiple-policies | 2024-05-03 |
| S-41 | T4 | fetched (signal) | "Power Platform DLP Bypass" — David Wyatt, DEV Community | https://dev.to/wyattdave/power-platform-dlp-bypass-1a6b | 2025-03-10 |
| S-42 | T3/T4 | search-verified (signal) | Independent governance-gap cluster (i3solutions; Valorem Reply; vBeyond) — DLP/connector-usage drift, ownership gaps | various | 2025–2026 |

Cross-referenced sibling sources cited by their register id in the sibling files: **G-03** (secure the default environment), **G-09** (CoE Starter Kit no longer maintained), **G-11** (managed environment licensing), **G-15** (data policy strategy), **D-12** (block unmanaged customizations), **D-17** (backup and restore).

---

## 12. Cross-area analysis (from the security side)

Kept deliberately separate from `governance.md` and `alm-devops.md`; the same relationship is analysed there from the other side, without duplicating text.

### 12.1 SECURITY ↔ GOVERNANCE

1. **Almost every strong security control is gated behind managed environments** — IP firewall, CMK, Lockbox, sharing limits, cookie binding, app access control, masking rules, VNet (S-23). Managed environments are a *governance* construct with a *licence* consequence (G-11: every active user needs a premium licence; enforcement blocks app opening from February 2027). **Consequence:** a security requirement can force a licensing decision for an entire user population. Security requirements must therefore be surfaced in the financial lens, not only the governance lens.
2. **The security boundary and the governance unit are the same object.** The environment is both (SEC-15). This is why "how many environments" is simultaneously a containment decision, a DLP-scope decision, a cost decision and a sprawl risk (`governance.md` GOV-07, GOV-26).
3. **Environment groups turn security settings into policy** — sharing, IP firewall and cookie binding can be applied at group level, and group rules *lock* the environment-level setting (S-01, G-04). **Consequence:** the security model becomes enforceable at scale, at the cost of local flexibility; per-environment exceptions are not currently supported.
4. **Governance decides who can create the boundary.** If environment creation is not restricted (G-08), any licensed user can create an environment outside every security control — no group, no policy, no firewall. Environment-creation control is therefore a *security* prerequisite, not a tidiness measure.
5. **Detection is governance, containment is security.** Oversharing, ownerless apps, missing WAF and expiring certificates surface through the Actions page — weekly, and only in managed environments (S-35, S-01). A security posture that depends on these signals inherits their cadence and their scope.

### 12.2 SECURITY ↔ ALM

1. **Deployment is a privileged operation.** Deploying solutions containing plug-ins requires **System Administrator** in the target environment (`alm-devops.md` ALM-11). The least-privilege story therefore cannot be told without delegated deployments: a service principal holds the privilege, an approval gates its use, and makers hold nothing in production.
2. **Ownership is created at deployment time.** "Who owns deployed solution objects? **The deploying identity**" (D-06). If a maker deploys, the maker owns production objects — including flows, whose owner is the runtime identity (SEC-21). Delegated deployment with an SPN is the mechanism that makes SEC-21 achievable in practice.
3. **A security control can be lost in transit.** The documented known issue where an implicitly shared secure connection imported via a connection reference has "the security… not set properly in the target environment" (S-18) means the control that protects production is established by the *deployment*, not by the app. Post-deployment verification of connection security belongs in the release checklist.
4. **Unmanaged layers are a security event, not only an ALM hygiene issue.** An unmanaged customisation sits above the managed layer and defines runtime behaviour (D-03) — including form-level and role-adjacent configuration. "Block unmanaged customizations" is therefore a production-integrity control (D-12), with a documented cost: a list of first-party features stops working, and dataflows are exempt.
5. **Environment variables and secrets bind ALM to secret management.** Values should not travel in the solution (D-15); secrets live in Key Vault and are consumed only by flows/agents/custom connectors (SEC-07). The pipeline must therefore supply configuration per environment, and the Key Vault permission model must exist in every target environment.
6. **Security-model artefacts move differently from the rest.** "Security roles and Column Security Profiles can be packaged up and moved… using Dataverse solutions. **Business Units and Teams must be created and managed in each environment**" (S-02). Any BU/team-dependent security model needs an environment-provisioning step outside the solution — and modernised BUs add a foreign-key failure mode across environments (SEC-10).
7. **Audit and CMK constrain the environment lifecycle.** Restore requires matching CMK and matching enterprise policies (D-17, SEC-29, SEC-30); audit retention is unavailable under CMK (SEC-34). The security configuration therefore determines which recovery options exist — see `alm-devops.md` ALM-18.

---

## 13. Summary

Power Platform can satisfy demanding security requirements, but only when the requirement is placed on the right plane and the architecture is shaped early. Four properties dominate every decision: **(1)** Dataverse privileges are additive and cannot be revoked in place, so the security model is an early, hard-to-reverse design artefact; **(2)** the environment is the real security boundary, which makes environment topology the primary security lever and simultaneously the primary governance and cost lever; **(3)** the application is never an authorization layer — the user's rights on the data source decide, so a requirement the source cannot express forces the data to move; **(4)** the strongest platform controls (IP firewall, CMK, VNet, sharing limits, app access control) are managed-environment features with an external licence dependency, which converts security requirements into budget decisions.

The documented weak points are as important as the capabilities: data policies are connector-aware but not connection-aware and are scoped by Microsoft to *unintentional* exposure; endpoint filtering is not enforced for dynamically computed endpoints; tenant isolation covers only Entra-authenticated connectors and has a named gap; the IP firewall and security groups do not, by default, constrain application users; column security never hides data from System Administrators; and the security score is preview and explicitly not for assurance. A design that states these residuals explicitly is defensible. A design that presents any of them as containment is not.

---

## 14. Cross-Block V2 reconciliation

### SEC-XB-01 — Security controls are economic architecture, not free configuration
- **Classification:** DECISION CRITERION + VOLATILE VALUE
- **Origin:** MS / MS-L
- **Evidence:** Current Microsoft documentation states that Power Platform IP firewall and customer-managed key require managed environments and, for users in the governed environment, an E5/A5/G5-class Microsoft 365/Office 365 or named compliance/security subscription. The current Power Platform licensing FAQ also lists VNet support under advanced security/governance with the same broad class of prerequisites. Microsoft Entra documents Conditional Access as requiring Entra ID P1 for standard policies and P2 for risk-based policies. Exact commercial entitlement remains contract-sensitive.
- **Decision impact:** evaluate **security control → external licence prerequisite → affected population → cost** before selecting the control. A security architecture is not feasible if its licence population is unfunded; the correct response is not to weaken the requirement silently but to select another control/topology or escalate the cost decision.
- **Confidence:** HIGH for the current documented prerequisite shape; commercial applicability/pricing remains **VOLATILE VALUE** and customer-contract-specific.
- **Sources:** `https://learn.microsoft.com/en-us/power-platform/admin/ip-firewall`; `https://learn.microsoft.com/en-us/power-platform/admin/customer-managed-key`; `https://learn.microsoft.com/en-us/power-platform/admin/powerapps-flow-licensing-faq`; `https://learn.microsoft.com/en-us/entra/fundamentals/licensing`.

### SEC-XB-02 — External integration components create a second security plane
- **Classification:** DECISION CRITERION
- **Origin:** MS + INF
- **Finding:** APIM, Service Bus, Functions/workers and gateway hosts are not governed by Power Platform DLP. Their identities, RBAC, network exposure, Key Vault use, policy baseline and diagnostic access must be designed in Azure/on-premises governance.
- **Architectural consequence:** a hybrid pattern is admissible only when those controls have an owner. “Move it to Azure for security” is incomplete unless the Azure side has an explicit security baseline. Azure Well-Architected guidance for API Management and Functions explicitly covers RBAC, pipeline protection, private networking, managed identity, Policy and monitoring.
- **Sources:** `integration-architecture.md` §15; `https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-api-management`; `https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-functions`.

### SEC-XB-03 — Security-model performance remains UNKNOWN and testable, not deferred
- **Classification:** CONSTRAINT
- **Origin:** MS + UNKNOWN
- **Finding:** S-02 documents overhead from sharing/excessive security constructs, but this corpus has no Microsoft figure mapping business-unit depth, team/share cardinality or column-security complexity to latency/throughput.
- **Decision impact:** for business-critical models with substantial BU/team/sharing complexity, performance sign-off requires a V2 bounded pilot with representative principals, records and access patterns (`performance-scale.md` PF-U-07). Absence of a published figure must not be converted into an arbitrary “safe” threshold.

### SEC-XB-04 — Cross-boundary transaction/reconciliation privileges
- **Classification:** RISK + RECOMMENDATION
- **Origin:** INF over documented identity/audit controls
- **Finding:** compensation, replay and reconciliation identities can reverse or reapply business writes outside the original user's transaction. They are therefore privileged integration identities.
- **Decision impact:** use least privilege; separate automated repair identity from interactive users; audit replay/compensation actions; govern who can manually disposition failed items. If per-user authorization must survive the seam, a service-identity facade/worker must propagate identity or the pattern is unsuitable.

### Cross-block availability boundary
Dataverse currently documents a **99.9% uptime SLA**, but that does not establish the availability of connectors, Azure components or downstream systems. Security controls such as VNet/IP firewall/CMK can also add dependencies and recovery prerequisites. End-to-end commitments remain flow-level and weakest-dependency based (`operations-support.md` OP-19); RTO/RPO is not an uptime SLA.

