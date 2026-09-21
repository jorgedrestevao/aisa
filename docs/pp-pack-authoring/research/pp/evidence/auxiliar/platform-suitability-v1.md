# Platform Suitability — Research Evidence

Research area: **01 — Platform Suitability** (see `../research-areas.md`).
Research date: **2026-09-02**. Source policy: `../source-policy.md`.
Status: **complete for this area** (stop condition met: main capabilities, constraints, decision criteria, alternatives, anti-patterns and conflicts identified). Other areas (02–15) are NOT covered here except where a fact is needed to reason about fit.

Volatility warning: limits, licences, prices and feature flags below are **as documented on the dates recorded in §8**. Treat every number as "valid on that date"; re-verify before encoding in the pack.

Language note: quotes are kept in the original English. Currency figures are USD list prices from the Licensing Guide; local pricing is not covered.

---

## 0. Classification model used in this file

Five fit classes, used consistently in the findings and in the matrix (§2):

| Class | Meaning used here |
|---|---|
| **STRONG FIT** | Requirement maps to a documented platform pattern; no documented limit is approached; standard licence models apply cleanly. |
| **CONDITIONAL FIT** | Fit depends on a measurable condition (volume, licence, data source, governance maturity). Must be validated before commitment. |
| **POOR FIT** | Requirement collides with a documented hard limit, an explicit Microsoft "not the best choice" statement, or an unsupported scenario. |
| **HYBRID** | Power Platform for the UX / orchestration / data layer, plus Azure or code components for the part that exceeds platform limits (Microsoft's "no-cliffs" approach). |
| **CUSTOM / OTHER** | Another Microsoft technology (Logic Apps Standard, Azure Functions, custom web app, first-party Dynamics 365, AppSource ISV) is documented as more appropriate for the whole requirement. |

Evidence classification tags follow `../source-policy.md §3`: FACT, RECOMMENDATION, CONSTRAINT, TRADE-OFF, RISK, ANTI-PATTERN, DECISION CRITERION, PATTERN.

Source tiers: **T1** Microsoft Learn / official docs / Licensing Guide; **T2** Microsoft technical material; **T3** independent technical; **T4** community. Source ids (S-nn) resolve in §8.

---

## 1. Findings

Findings are grouped by the dimensions requested (application type, complexity, UX, data, transactions, process, integration, scalability, performance, security, governance, offline, external users, operations, development complexity, licensing/cost, alternatives).

### 1.1 Application types

#### PS-01 — Power Platform is designed for line-of-business apps, process automation and Dataverse-backed external sites; Microsoft's own pattern catalogue names the typical shapes

**Classification:** FACT / PATTERN
**Evidence:** Microsoft's developer overview describes Power Apps as producing canvas and model-driven apps "shared with internal users … run in a browser or on a mobile device"; Power Automate as automating "tasks and orchestrate activities across various services"; Power Pages as "creating, hosting, and administering modern external-facing business websites" (S-20). The Power Apps guidance patterns catalogue lists: Approval ("automated granting of permissions, employee travel requests, overtime requests, and timesheet submissions"), Asset management ("asset check-out, asset rollout, inventory management, supply order management"), Calculation ("cost estimation, decision support, field technician apps, generating work orders or estimates"), Communication, Inspection ("an app user fills out a structured assessment, which is then uploaded to a centralized location"), Project management (S-33). Model-driven apps are "especially well suited to process driven apps that are data dense and make it easy for users to move between related records … onboarding new employees, managing a sales process, or member relationships" (S-31).
**Why it matters:** These are the shapes with the most mature platform support, templates, and precedent. A requirement that maps onto one of them has a high prior of fit.
**Decision impact:** Fit class STRONG when the requirement is a form/approval/inspection/asset/calculation/case-style internal app with structured data and modest volumes.
**Conditions:** Internal users, structured data, no documented limit approached (see PS-13, PS-18, PS-23).
**Confidence:** HIGH.
**Sources:** S-20, S-31, S-33.

#### PS-02 — Canvas vs model-driven is a documented decision: model-driven needs Dataverse and gives responsive/accessible UI for free; canvas gives pixel control and 200+ connectors at the cost of consistency and ALM complexity

**Classification:** DECISION CRITERION
**Evidence:** Microsoft comparison table (S-31): Data platform "Dataverse only" vs "Dataverse + many others using connectors"; UI control "Limited, predominantly customization" vs "Full control"; Migration between environments "Simple" vs "Potentially complex given that the datasources might need to be updated"; Responsive "Automatically responsive" vs "Only responsive if designed in this way"; Accessibility "Built in" vs "Designed into the app". Custom pages bring canvas flexibility inside a model-driven app (S-32).
**Why it matters:** The requirement's data shape (relational, in Dataverse vs scattered across sources) and UX need (standard data-dense forms vs bespoke task UI) determines the app type, and the app type determines ALM effort, accessibility effort and licence (model-driven always premium; canvas may be standard-only).
**Decision impact:** Relational, process-heavy, many related tables → model-driven (STRONG). Task-focused, mobile-first, multi-source → canvas (STRONG/CONDITIONAL on delegation, PS-13).
**Conditions:** Model-driven on a phone browser "isn't supported; use the Power Apps mobile app" (S-01).
**Confidence:** HIGH.
**Sources:** S-31, S-32, S-01.

#### PS-03 — "Code apps" are Microsoft's in-platform hybrid: a pro-developer SPA (React/Vue) hosted and governed by Power Platform, but with real limitations and a premium licence per end user

**Classification:** PATTERN / CONSTRAINT
**Evidence:** "Code apps let developers bring Power Apps capabilities into custom web apps built in a code-first IDE … Build with popular frameworks (React, Vue, and others) while keeping full control over your UI and logic." Features: Entra auth, "1,500+ connectors, callable directly from JavaScript", DLP/Conditional Access/sharing limits apply. Limitations: "don't support Power Platform Git integration", "aren't supported in Power Apps for Windows", no SharePoint forms integration, "compiled app assets are served from a publicly accessible endpoint that doesn't support IP-based restrictions". "End users that run code apps need a Power Apps Premium license." (S-19, dated 2026-08-12). Independent view (T3, S-42): "Choose code apps when you need a custom SPA frontend with stronger engineering control … should solve a real architectural problem, not simply because they sound more advanced"; noted gaps: no mobile via Power Apps client, no native Git.
**Why it matters:** When UX or logic exceeds canvas (PS-06, PS-08, PS-10) but the organisation wants platform governance, data and licensing, code apps are a middle path before leaving the platform.
**Decision impact:** HYBRID candidate for bespoke internal UX with Dataverse/connector data. Not a candidate for anonymous/public, native mobile, or IP-restricted scenarios.
**Conditions:** Pro-dev team; Premium licences; features evolving (verify at decision time).
**Confidence:** HIGH on facts; MEDIUM on maturity.
**Sources:** S-19, S-42.

#### PS-04 — Microsoft distinguishes "productivity" from "mission-critical" workloads and says mission-critical on Power Platform is possible but "demands deep platform knowledge" and "engineering rigor"

**Classification:** DECISION CRITERION / RISK
**Evidence:** Table in S-34: Productivity workload "Built ad-hoc / Built by one / No tests / Development in production / Users monitor quality / Short lifecycle" vs Mission-critical "Built to last / Built and maintained by a team / Automated tests / Exercises application lifecycle management / Monitored to improve / Long lifecycle". "Creating a reliable application at scale is complex. It demands deep platform knowledge to choose the right technologies … Operationalizing mission-critical workloads necessitates a high level of engineering rigor." Platform side: production environments replicated across availability zones, "RTO < 5 minutes", 7-day backups (28 for managed environments).
**Why it matters:** Criticality is an independent axis from functional fit. A functionally simple app that is business-critical needs the enterprise operating model (ALM, monitoring, managed environments), which changes cost and team.
**Decision impact:** Business-critical → CONDITIONAL on the organisation being able to run the mission-critical model (team, ALM, licences). Absence of that capability is a RISK, not a platform limitation.
**Conditions:** See PS-34, PS-38.
**Confidence:** HIGH.
**Sources:** S-34, S-37.

#### PS-05 — Microsoft's own tenant strategy classifies solutions as personal productivity / team / enterprise; enterprise requires ALM, sandboxes and managed solutions in production

**Classification:** RECOMMENDATION
**Evidence:** "Microsoft is structuring its Power Platform environments into three broad categories … personal productivity, team collaboration, and enterprise development." Enterprise: "may store the most sensitive data, use more powerful connectors, and require more governance … ALM is required, with preproduction work happening in sandbox environments and only managed solutions allowed in production environments." Default environment: "Personal Productivity", data policies restricting to "basic, unblockable connectors", sharing limits "between 5 and 50 users" (S-35).
**Why it matters:** The intended audience size and data sensitivity of a requirement sets which environment class and governance tier it needs — and therefore which licences (premium for managed environments, PS-34).
**Decision impact:** Requirement with org-wide audience or sensitive data → enterprise class; CONDITIONAL on governance/licensing readiness.
**Conditions:** Organisation-specific; tenant maturity.
**Confidence:** HIGH.
**Sources:** S-35.

### 1.2 Complexity

#### PS-06 — Large canvas apps degrade the maker experience and runtime; Microsoft documents partitioning strategies, and confirms production apps with 100+ tables and 50+ screens exist

**Classification:** CONSTRAINT / TRADE-OFF
**Evidence:** "As apps become larger and more complex, Power Apps Studio needs to load and manage larger numbers of controls, formulas, and data sources, all with interdependencies that grow exponentially." "nearly all apps with a long load time for Power Apps Studio have at least one formula of more than 256,000 characters." "Some apps grow to thousands of controls and hundreds of data sources, which slows Power Apps Studio … large apps can be split into smaller sections" via separate canvas apps + `Launch`, or "Model-driven app with custom pages" (S-25). Counter-evidence for capacity: "Many successful Power Apps implementations use more than 100 tables and over 50 screens while keeping excellent performance" (S-26). Community/older guidance cites 500 controls per app and 300 per screen as recommendations; App Checker warns on >300 per screen (T4, S-46) — **not found on a current T1 page in this research**.
**Why it matters:** Screen count and control density are observable early. Very large single-app scopes are a maintainability and performance risk on canvas.
**Decision impact:** Large functional scope → CONDITIONAL: partition (multiple apps, model-driven + custom pages) or prefer model-driven. Not a reason alone to leave the platform.
**Conditions:** The 500/300 numbers are MEDIUM confidence (T4 + older T1); the qualitative constraint is HIGH.
**Confidence:** HIGH (constraint) / MEDIUM (numbers).
**Sources:** S-25, S-26, S-46.

#### PS-07 — Microsoft explicitly says complex business logic and large-scale data transformation do not belong in cloud flows; put them in Dataverse plug-ins, custom connectors (Azure Functions / API Management / App Service) or dataflows

**Classification:** RECOMMENDATION / ANTI-PATTERN
**Evidence:** "Power Automate is an excellent tool for automating daily tasks. However, it isn't the best choice for large-scale data transformation or integration. Embedding complex business logic directly into cloud flows can lead to performance bottlenecks, make them hard to understand, debug, and maintain, and be cumbersome to scale." Alternatives: Dataverse plug-ins "for moving or processing a large number of Dataverse records"; custom connectors "for standalone services, like Microsoft Azure Functions, Azure API Management, and Azure App Service … ensuring that the flow remains simple and focused on orchestration rather than on processing"; dataflows for ETL (S-22). Well-Architected adds: put reusable logic in plug-ins because "if you put the business logic in the canvas app, you can't reuse it" (S-24).
**Why it matters:** This is the clearest Microsoft boundary between low-code orchestration and code. It converts "complex logic" from a vague fear into a placement decision.
**Decision impact:** Complex/reusable/high-volume logic → HYBRID (flows orchestrate; plug-ins/Functions compute). Pure ETL → dataflows or Azure integration, not flows.
**Conditions:** Requires pro-dev skills (PS-42).
**Confidence:** HIGH.
**Sources:** S-22, S-24, S-23.

#### PS-08 — Power Fx has no imperative loops or mutable local state and weak debugging; algorithm-heavy logic is a documented pain point (independent) and Microsoft's own docs show workarounds

**Classification:** RISK / CONSTRAINT
**Evidence (T3):** "The friction begins when logic requires sequence." Power Apps lacks `While`/`Repeat`/mutable `For`; a Timer control was repurposed as flow control — "architecturally it is absurd"; debugging relies on Monitor and `Trace`; "Power Apps is not failing. It is succeeding within a narrower complexity band than its marketing sometimes implies." (S-41). **Cross-check (T1):** Microsoft's large-app guidance recommends splitting imperative logic with a hidden Button and `Select(Button)`, and notes named formulas "don't support imperative logic" (S-25) — corroborating the structural constraint.
**Why it matters:** Requirements with algorithmic cores (optimisation, rules engines, state machines, iterative calculations) will fight the language.
**Decision impact:** Algorithmic core → HYBRID (compute in plug-in / Function / custom API; UI in Power Apps) or CUSTOM.
**Conditions:** Simple validations, calculations and CRUD orchestration are fine (PS-01).
**Confidence:** MEDIUM (primary evidence T3; structurally corroborated by T1).
**Sources:** S-41, S-25.

#### PS-09 — Dataverse plug-ins have a hard 2-minute execution limit and synchronous plug-ins delay the user; heavy processing is meant to go to Azure ("no-cliffs")

**Classification:** CONSTRAINT / PATTERN
**Evidence:** "Plug-ins have only a short period of time (a hard limit) to complete their work." "A synchronous plug-in causes the data operation to wait … synchronous plug-ins must execute and complete quickly." Advantages: "the most performant way to apply custom business logic"; disadvantages: "require the special skills of a software developer" (S-27). Related docs state a two-minute timeout for the whole message operation including synchronous plug-ins and custom API plug-ins (S-28). Dynamics 365 guidance: "no-cliffs extension approach. You can start with SaaS, and then for the most challenging scenarios, extend into PaaS … PaaS extensions … handle heavy processing outside of your app." Azure Functions "can move some of the heavy computing processes away" (S-30).
**Why it matters:** Even the code-first in-platform option has a ceiling; long computations, external waits or fan-out work must be asynchronous and often off-platform.
**Decision impact:** Long-running or compute-heavy logic → HYBRID with Azure (Functions/Durable, Service Bus, Logic Apps).
**Conditions:** Asynchronous plug-ins "queued and runs after the data operation finishes" cover many cases without Azure.
**Confidence:** HIGH.
**Sources:** S-27, S-28, S-30.

### 1.3 User experience requirements

#### PS-10 — Bespoke, brand-critical or consumer-grade UX is a poor fit for model-driven, a conditional fit for canvas (within its control library + PCF), and pushes toward Power Pages or custom web for public audiences

**Classification:** TRADE-OFF
**Evidence:** Model-driven UI is "Limited, predominantly customization" (S-31); T3: model-driven offers "less flexibility for bespoke digital experiences" (S-42). Canvas offers "Full control" of layout via a fixed control set plus PCF code components; PCF limitations in canvas: "Microsoft Dataverse dependent APIs, including WebAPI, are not available for Power Apps canvas applications yet", "Custom auth in code components is not supported" (S-29). For external audiences, Power Pages exposes HTML/CSS/Liquid templates (S-20); canvas is embeddable in third-party web sites in a browser but not in "Third party native applications" (S-01).
**Why it matters:** UX ambition is a real cost driver on low-code; "pixel perfect" on canvas means many controls (PS-06) or PCF (pro-dev).
**Decision impact:** Internal task UX → STRONG/CONDITIONAL (canvas). Public consumer UX → Power Pages (CONDITIONAL, Dataverse-only data) or CUSTOM web.
**Conditions:** Design-system-level branding, animations, native gestures are signals toward code apps (PS-03) or custom.
**Confidence:** HIGH (facts) / MEDIUM (threshold is judgement).
**Sources:** S-31, S-29, S-20, S-01, S-42.

#### PS-11 — Accessibility is built in for model-driven apps and is the maker's responsibility for canvas apps

**Classification:** FACT / DECISION CRITERION
**Evidence:** Model-driven: "The apps are accessible and responsive automatically" (S-31). Canvas: guidance on contrast 4.5:1, `AccessibleLabel`, `TabIndex`, verified screen readers (JAWS, Narrator, NVDA, TalkBack, VoiceOver), Accessibility Checker, "unsupported design patterns" (S-36).
**Why it matters:** Regulatory accessibility requirements (public sector, large employers) raise canvas effort and make model-driven attractive.
**Decision impact:** Strict accessibility requirement → prefer model-driven; canvas CONDITIONAL on design discipline and testing.
**Conditions:** Public-facing accessibility (Power Pages) not researched here.
**Confidence:** HIGH.
**Sources:** S-31, S-36.

#### PS-12 — Embedding and client constraints: no canvas embedding in native desktop/mobile clients, no iFrame embedding of model-driven apps, proxies unsupported, mobile browser unsupported for model-driven

**Classification:** CONSTRAINT
**Evidence:** "Power Apps doesn't support the nested embedding of canvas apps in native desktop, mobile, or other non-browser clients." "Power Apps doesn't support embedding a model-driven app or page within an IFrame in another application." "Power Apps doesn't support running with a proxy enabled." Zscaler/Blue Coat/Defender for Cloud Apps/McAfee cited as breaking headers/URLs. Single outbound request timeout 180 s, 4 retries (S-01).
**Why it matters:** Requirements to embed the app inside an existing native product, or deployment inside heavily proxied networks, are frequent hidden blockers.
**Decision impact:** Native-embed requirement → CUSTOM. Proxied enterprise network → CONDITIONAL on network exceptions.
**Conditions:** Browser embedding (SharePoint, Teams web, Power BI web) is supported.
**Confidence:** HIGH.
**Sources:** S-01.

### 1.4 Data characteristics

#### PS-13 — Delegation is the central data-fit rule for canvas apps: non-delegable queries silently operate on the first 500 (max 2,000) rows and can return wrong results

**Classification:** CONSTRAINT / RISK
**Evidence:** "When a query is nondelegable, Power Apps gets the first 500 records from the data source and then runs the actions in the query. You can increase this limit to 2,000 records." "the query might return incorrect results if the data source has more than 500 or 2,000 records." Delegable sources: Dataverse, SharePoint, SQL Server, Salesforce. Notable non-delegable functions: `If`, `*`/`/`/`Mod`, string functions, `GroupBy`, `Concat`, `FirstN/Last/LastN`. Recommendation: "set this value to 1 … to make sure your app scales to large data sets" during testing (S-02). SharePoint delegation is narrower: complex types (Choice/Lookup/Person) partly; ID field only `=`; `IsBlank`, `Not` not delegable (S-10). SQL: `Search` on text yes, direct date filters fail via on-prem gateway, `char`/`nchar` pitfalls (S-40).
**Why it matters:** This is the mechanism by which "it worked in the pilot" fails at production volume. Any list, filter, aggregate or search over a table that will exceed 500–2,000 rows must be provably delegable on the chosen source.
**Decision impact:** Data volume > 2,000 rows per queried table → CONDITIONAL: Dataverse (broadest delegation) or SQL with delegable-only formulas; SharePoint becomes POOR for non-trivial query needs; Excel/collections POOR beyond 2,000.
**Conditions:** Small reference data (<500 rows) is unaffected.
**Confidence:** HIGH.
**Sources:** S-02, S-10, S-40.

#### PS-14 — Data store choice is a fit decision: Dataverse for relational/secured business data (fastest path, bypasses API Management); SharePoint for document-centric collaboration; SQL when the database already exists (premium + gateway on-prem); Excel not a database

**Classification:** DECISION CRITERION
**Evidence:** "When you use Microsoft Dataverse as the data source, data requests go directly to the environment instance without passing through Azure API Management. So, it tends to be faster than other data sources." SharePoint: "Avoid too many dynamic lookup columns", "Consider breaking up large lists … hundreds of thousands of records". Excel: "restricts the canvas app to loading data from the table only up to 2,000 records"; "Excel isn't a relational database system … if the app requires heavy transactions, it can adversely affect the performance" (S-11). Dataverse positioning: "relational, non-relational, file, image, search, and data lake", role/row/column security, hierarchy security, "service level agreement of 99.9% uptime", virtual tables for external data (S-12). SQL: on-premises requires the on-premises data gateway (S-10/S-40); implicitly shared SQL connections are "the least secure" and secure implicit connections were introduced Jan 2024 (S-43). Community signal (T4): SharePoint list view threshold 5,000 and lookup-column delegation problems are recurring failure reports (S-45).
**Why it matters:** Choosing the store to avoid premium licences (SharePoint/Excel) is the most common root cause of later performance, integrity and security problems; Dataverse solves them but triggers premium licensing and capacity cost (PS-15, PS-43).
**Decision impact:** Relational data with relationships, security by row/column, audit → Dataverse (STRONG technically, CONDITIONAL on licence). Documents + light metadata → SharePoint (STRONG). Existing SQL system of record → SQL connector (CONDITIONAL: premium, gateway, delegation table). Spreadsheet as system of record → POOR.
**Conditions:** Volume, relationship depth (max 2 lookup expand levels, 20 joined entities per query — S-02), security granularity, transaction rate.
**Confidence:** HIGH.
**Sources:** S-11, S-12, S-10, S-40, S-43, S-45.

#### PS-15 — Dataverse capacity is an entitlement (not a technical) limit and a material cost driver: 250 MB DB / 2 GB file accrue per Power Apps Premium user; overage DB is $48/GB/month; "There's no technical limit on the size of a Dataverse environment"

**Classification:** TRADE-OFF / CONSTRAINT
**Evidence:** "There's no technical limit on the size of a Dataverse environment. The limits mentioned on this page are entitlement limits based on product licenses you purchase." Default environment includes 3 GB DB / 3 GB file / 1 GB log. Over-capacity blocks environment lifecycle operations (create/copy/restore) and "Microsoft might suspend use of the online service" (S-13). Licensing Guide (Sept 2026): Power Apps Premium accrues "Dataverse Database 250 MB" and "Dataverse File 2 GB" per licence; pay-as-you-go environments get 1 GB DB + 1 GB file; overage "Dataverse Database capacity 1 GB $48/month; File 1 GB $2.40/month; Log 1 GB $12/month" (S-44). Dataverse for Teams: 2 GB / ~1M rows per team, cannot buy more (S-14).
**Why it matters:** Data-heavy requirements (large transactional tables, attachments, audit logs) are technically fine on Dataverse but can dominate TCO; file vs database placement changes cost 20×.
**Decision impact:** High data volume → CONDITIONAL on capacity budget; consider Azure SQL/Blob via virtual tables or connectors as HYBRID for bulk data.
**Conditions:** See conflict C-1 on default tenant capacity (10 vs 20 GB).
**Confidence:** HIGH (rules) / MEDIUM (exact default GB, conflicted).
**Sources:** S-13, S-44, S-14.

#### PS-16 — Dataverse for Teams is a bounded fit: Teams-only, 2 GB/~1M rows, no API, no plug-ins, no model-driven apps, one business unit, no auditing or field security

**Classification:** CONSTRAINT
**Evidence:** Comparison table: API access No; Plug-ins No; PCF No; model-driven apps No; Auditing No; Field-level security No; Business units One; Mobile offline No; "Maximum size 1 million rows or 2 GB"; "Dataverse for Teams is designed to work in the Teams client … To use outside of Teams, you must upgrade" (S-14). Premium connectors in Dataverse for Teams require standalone licences (S-06).
**Why it matters:** It is the only relational store available on seeded M365 licences; its ceiling defines when a "free" solution must be re-platformed.
**Decision impact:** Small team app inside Teams, <1M rows, no integration API → STRONG on Dataverse for Teams. Anything with audit, field security, API, offline, or outside Teams → upgrade to Dataverse (premium).
**Conditions:** Upgrade path exists but is one-way and changes licensing.
**Confidence:** HIGH.
**Sources:** S-14, S-06.

#### PS-17 — Data residency is set per environment at creation and cannot move; India/Australia have tenant-location constraints; on-premises gateway unavailable in India region

**Classification:** FACT / CONSTRAINT
**Evidence:** "Environments can be created in different regions, and are bound to that geographic location … This applies to … databases in the Microsoft Dataverse, apps, connections, gateways, and custom connectors." EU environments keep data "within EU and EFTA member states which are European Union Data Boundary (EUDB) regions." "Tax laws prevent you from creating a database for an environment in India and Australia, if your Microsoft Entra tenant is not in India and Australia." "On-premises data gateways aren't available in the India region." (S-15). Geo migration not supported for Dataverse for Teams (S-06). Microsoft "doesn't disclose the exact details of where your data resides" within a geography (S-37).
**Why it matters:** Residency is usually satisfiable but must be decided before the first environment exists; multi-country deployments may need multiple environments and duplicated governance.
**Decision impact:** Residency requirement → CONDITIONAL on region availability and single-vs-multi environment strategy. Requirement to know exact datacentre → POOR (not disclosed).
**Conditions:** Regional feature availability varies (S-24).
**Confidence:** HIGH.
**Sources:** S-15, S-06, S-37, S-24.

### 1.5 Transaction characteristics

#### PS-18 — Dataverse service protection limits are per user per 5 minutes (6,000 requests, 20 min execution time, 52 concurrent, per web server); interactive users rarely hit them, integrations and portals do

**Classification:** CONSTRAINT
**Evidence:** "These limits don't affect normal users of interactive clients. They affect only client applications that perform an extraordinary volume of API requests." Defaults per web server: 6,000 requests / 300 s; 1,200 s execution time; 52 concurrent. "Portal applications typically send requests from anonymous users through a service principal account … can hit service protection API limits based on the amount of traffic." Plug-in operations don't count as requests but their execution time is added. Batch is "not a valid strategy to bypass entitlement limits". Recommendation: "Move towards real-time integration" instead of large nightly batches (S-03).
**Why it matters:** Bulk loads, mass updates, high-traffic portals and chatty integrations must be engineered with retry/back-off and parallelism; naïve designs get 429s.
**Decision impact:** High-throughput integration → CONDITIONAL (design for limits) or HYBRID (Azure integration services buffer and pace). Very high sustained write rates → CUSTOM store (Azure SQL/Cosmos) with Dataverse as reference data.
**Conditions:** Web-server count per environment is not published (U-3).
**Confidence:** HIGH.
**Sources:** S-03.

#### PS-19 — Daily Power Platform request entitlements are per licence: 40,000 (Premium/D365), 6,000 (M365 seeded, per app, PAYG), 250,000 (Process/per flow); background flows consume the owner's limit; retries and pagination count

**Classification:** DECISION CRITERION / CONSTRAINT
**Evidence:** Table (S-04, 2026-08-14): "Paid licensed users for Power Platform … 40,000"; "Power Apps pay-as-you-go plan, and paid licensed users for Power Apps per app, Microsoft 365 apps with Power Platform access … 6,000"; "Power Automate per flow plan, Microsoft Copilot Studio … 250,000". Non-licensed pool: "Power Apps (all licenses) 25,000 base requests with no per-license accrual", same for Power Automate. "Workflows or automated and scheduled flows that run in the background always use the limits of the owner of the process." "Both successful and failed actions count … Retries and requests from pagination also count." Transition period: enforcement "won't happen until six months after … reporting is generally available"; current transition limits are higher (S-04, S-05).
**Why it matters:** A volume requirement can be expressed as requests/day and compared with the licence plan before design. M365-seeded automation at 6,000/day is a small envelope; loops multiply.
**Decision impact:** Requests/day per owner > licence entitlement → CONDITIONAL (Process licence, PAYG) or HYBRID/Logic Apps for the volume path.
**Conditions:** Enforcement timeline unknown (U-1); "Build your cloud flows based on official limits."
**Confidence:** HIGH (documented) / MEDIUM (enforcement).
**Sources:** S-04, S-05.

#### PS-20 — No documented concurrent-user ceiling exists for canvas or model-driven apps; capacity is governed by data-source and request limits, and Power Pages scales "automatically based on the Power Pages licensing capacity"

**Classification:** FACT (absence) / UNKNOWN
**Evidence:** Searches of T1 limits pages found no per-app concurrent-user maximum (S-01, S-11). Mobile platforms differ in concurrent network requests, affecting large data loads (S-11). Power Pages: "Scaling of these application servers is done automatically based on the Power Pages licensing capacity assigned to the environment" (S-17). Dataverse: "designed to meet enterprise-level scalability needs" (S-12) — marketing-grade statement, translated into PS-18/PS-19 questions.
**Why it matters:** "How many users?" is not itself a limit; it must be translated into requests/day, requests/5 min, data volume and delegation.
**Decision impact:** User count alone never yields POOR; it feeds PS-13/18/19.
**Conditions:** —
**Confidence:** MEDIUM (absence of evidence).
**Sources:** S-01, S-11, S-17, S-12.

### 1.6 Process characteristics

#### PS-21 — Good automation candidates per Microsoft: repetitive, rule-based, high-volume-of-occurrence, manual re-keying between systems, runnable without human interaction

**Classification:** PATTERN / DECISION CRITERION
**Evidence:** Power Automate planning guidance: "Processes that are done the same way every time should be high on your list"; "High-volume processes occur very frequently on a daily basis"; "Manually entering data between systems that don't communicate with each other is a good automation candidate"; "processes that can be run independent of human interaction" (S-38, captured via search excerpt; direct fetch redirected — see U-9).
**Why it matters:** Gives technology-neutral process signals (repetition, rule-clarity, frequency, cross-system re-keying, human dependency) usable in Discovery.
**Decision impact:** Rule-based, moderate-frequency, human-in-the-loop → STRONG (cloud flows/approvals). Judgement-heavy, exception-dominated → CONDITIONAL (human tasks + partial automation).
**Conditions:** "High volume" here means occurrence frequency, not data throughput; see PS-23/24 for throughput limits.
**Confidence:** MEDIUM (excerpt-level evidence).
**Sources:** S-38.

#### PS-22 — Human-in-the-loop and long-running approvals are a strong fit up to 30 days; pending steps time out at 30 days

**Classification:** CONSTRAINT / PATTERN
**Evidence:** "Run duration 30 days … includes flows with pending steps like approvals. After 30 days, any pending steps time out." Run retention 30 days (S-05). Well-Architected: "use Power Automate Approvals if human interaction is required, but choose to use a Dataverse plugin … when human interaction isn't required" (S-24).
**Why it matters:** Approval, review and escalation processes are the archetypal fit; processes with legally or operationally longer waits need state persisted in data, not in a flow run.
**Decision impact:** Approvals/escalations → STRONG. Waits > 30 days → CONDITIONAL (model state in Dataverse, re-trigger) rather than a single long run.
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-05, S-24.

#### PS-23 — Cloud flow hard limits shape fit: 500 actions/flow, nesting 8, apply-to-each 100,000 items (5,000 Low profile), loop concurrency ≤50, 120 s synchronous request timeout, 100 MB message, content throughput 10 GB/day (High) or 200 MB/day (Low); throttled or erroring flows are turned off after 14 days

**Classification:** CONSTRAINT
**Evidence (S-05, 2026-07-17):** "Actions per workflow 500"; "Allowed nesting depth for actions 8"; "Apply to each array item 5,000 for Low, 100,000 for all others"; "Apply to each concurrency 1 is the default … between 1 and 50"; "Until iterations Default 60 Maximum 5,000"; "Outbound synchronous request 120 seconds"; "Inbound request 120 seconds"; "Message size 100 MB … with chunking 1 GB"; "Content throughput per 24 hours 200 MB for Low; 2 GB for Medium; 10 GB for High"; "Consistently throttled flows 14 days — turned off"; "Flows with errors 14 days — turned off"; "Flows without trigger activity 90 days might be turned off" (non-premium). Performance profile Low = M365 plans, per-app, trials; High = Process/per-flow licence.
**Why it matters:** These are checkable against a requirement: payload sizes, items per run, synchronous response expectations (an API façade that must answer in >2 min is out), daily data volume.
**Decision impact:** Any single hard limit exceeded → POOR for cloud flows on that path → HYBRID/Logic Apps/Functions.
**Conditions:** Numbers tied to licence profile; volatile.
**Confidence:** HIGH.
**Sources:** S-05.

#### PS-24 — Microsoft positions Power Automate for "citizen developers and business users" at "small to medium scale" on "shared resources", and Logic Apps Standard for "complex, high-volume, and security-sensitive workloads" with dedicated compute, VNET, resource-level RBAC and Git CI/CD

**Classification:** DECISION CRITERION / TRADE-OFF
**Evidence (S-08, S-09):** Comparison table: Purpose — Standard "Workflow automation with advanced features for enterprise developers" vs Power Automate "Workflow automation for citizen developers and business users"; Scalability — "Large scale workflows with high throughput and low latency" vs "Small to medium scale workflows"; Performance — "Dedicated resources … faster execution, parallel processing" vs "Suitable for lower-scale automation, limited by shared resources in Power Automate"; Custom integration — "Complex logic support through Azure Functions, custom APIs" vs "Limited to mostly no code or low code"; BCDR — "Built-in geo-redundancy, multiregion deployment" vs "Limited regional deployment options"; Version control — "Full Git integration" vs "Limited versioning"; Monitoring — Azure Monitor/App Insights vs "Basic monitoring through the Power Automate portal". "In Power Automate, RBAC works at the user level … In Azure Logic Apps, RBAC works at the resource level … if the workflow creator leaves, you don't lose access." Azure Functions doc: "Power Automate empowers business users, office workers, and citizen developers to build simple integrations … Azure Logic Apps supports integrations ranging from little-to-no-code scenarios to more advanced, codeful, and complex workflows … B2B processes." Community (T3, S-39): differences are mostly licensing (M365 per user vs Azure consumption), audience, DLP vs Azure Policy.
**Why it matters:** This is Microsoft's own boundary statement between the two orchestration engines. It also names the operational criteria (ownership on leaver, monitoring depth, network isolation, CI/CD) that Discovery can ask about without naming products.
**Decision impact:** IT-owned, high-throughput, latency-sensitive, network-isolated, or B2B/EDI integration → CUSTOM/OTHER (Logic Apps Standard, Functions). Business-owned, M365-centric, human-centric orchestration → STRONG (Power Automate).
**Conditions:** See conflict C-3 (scale statement vs Process licence throughput) and C-6 (VNET, version-sensitive).
**Confidence:** HIGH.
**Sources:** S-08, S-09, S-39.

#### PS-25 — Documented flow anti-patterns: nested for-each loops, self-triggering infinite loops, large data transformations in flows, per-record loops for thousands of updates; remedies are OData expand, trigger conditions, dataflows, batch/bulk APIs

**Classification:** ANTI-PATTERN
**Evidence (S-23):** "Avoid nested For each loops … They can exceed limits and quotas." "Avoid infinite loops … a flow is triggered when a record is updated … and the flow updates the same record." "Avoid large numbers of data transformation operations … use an ETL dataflow. Dataflows handle large volumes of data efficiently and provide better performance for ETL tasks than cloud flows do." "If you need to create or update thousands of records … don't use a For each loop to process each record sequentially" → batch (SharePoint/Dataverse `$batch`), bulk (`CreateMultiple`), parallelism up to 50. Community (T4, S-47): variables lock in loops; default concurrency 20/50 triggers connector throttling; Select/Filter array preferred over loops.
**Why it matters:** These are the recurring reasons "simple" automations fail at production scale.
**Decision impact:** Requirement described as "process every row of X nightly" is a signal for dataflows/Azure, not flows.
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-23, S-47.

### 1.7 Integration requirements

#### PS-26 — Integration runs through connectors: 1,400+ prebuilt, custom connectors wrap REST APIs; premium/custom connectors and on-premises data require premium licences and (on-prem) the data gateway; custom connectors are capped at 500 requests/min per connection and 50 per user

**Classification:** CONSTRAINT / FACT
**Evidence:** "A custom connector is a wrapper around a REST API and can be created using tools like Azure Functions and Azure API Management" (S-20). Licensing Guide table: M365 seeded rights include "Standard connectors" only; "Premium and custom connectors" and "On premises and cloud services data transfer" require Power Apps Premium / per app / D365 (S-44). Flow limits: "Number of custom connectors 50 per user"; "500 requests per minute per connection" (S-05). SharePoint connector cap 600 actions/min per connection (S-05 excerpt). Community (T3, S-48): the on-premises gateway "adds latency, complexity, and another dependency"; legacy databases need workarounds.
**Why it matters:** "Does a connector exist and is it standard or premium?" is a licence and cost fork; "is the system on-premises?" adds the gateway as an operational component; per-connection throttles bound integration throughput.
**Decision impact:** Cloud SaaS with standard connector → STRONG. Custom REST/on-prem → CONDITIONAL (premium, gateway, throttles). No API (UI-only legacy) → desktop flows/RPA (out of scope here) or CUSTOM.
**Conditions:** SOAP support via custom connectors was not verified in this research (U-10).
**Confidence:** HIGH (T1 facts) / MEDIUM (T3 operational claims).
**Sources:** S-20, S-44, S-05, S-48.

#### PS-27 — Event-driven and decoupled integration is a documented pattern: Dataverse publishes to Azure Service Bus, Event Hubs or webhooks from plug-in steps (asynchronous recommended), with a 192 KB payload cap

**Classification:** PATTERN / CONSTRAINT
**Evidence:** "The Azure Service Bus provides a secure and reliable communication channel between Dataverse runtime data and external cloud-based line-of-business (LOB) applications." Contracts: queue, one-way, two-way, REST, topic, Event Hubs. "register the plug-in to run asynchronously for best system performance." "When the size of the entire HTTP payload exceeds 192 KB, the following properties are removed … If the size of the payload exceeds 192 KB after the additional data is removed, an error occurs and the message isn't sent." Retries "in exponentially larger and larger time spans" (S-21). Well-Architected: "publishing Dataverse events to a queue for later processing, can improve performance and reliability. However, these methods don't give users immediate feedback" (S-24). Not available in Dataverse for Teams (S-14).
**Why it matters:** Requirements for reliable, decoupled, multi-consumer integration are met by a HYBRID (Dataverse + Azure messaging), not by chaining flows.
**Decision impact:** Event fan-out, guaranteed delivery, multi-subscriber → HYBRID (Service Bus/Event Grid) — flows alone are CONDITIONAL.
**Conditions:** Requires Dataverse (not Teams) and Azure subscription.
**Confidence:** HIGH.
**Sources:** S-21, S-24, S-14.

#### PS-28 — Synchronous integration windows are short: canvas outbound request 180 s; flow synchronous inbound/outbound 120 s; longer operations must be asynchronous

**Classification:** CONSTRAINT
**Evidence:** Power Apps "Timeout 180 seconds, Retry attempts 4" per outgoing request (S-01). Flows: "Outbound synchronous request 120 seconds … For longer-running operations, use an asynchronous polling pattern"; "Flows that contain a response action … always return a response within this limit" (S-05).
**Why it matters:** Requirements framed as "the app calls the ERP and waits for the result" are only a fit if the ERP answers in seconds; otherwise design for async with status.
**Decision impact:** Sync call latency > ~2 min → CONDITIONAL (async redesign) or HYBRID (Durable Functions/Logic Apps orchestration).
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-01, S-05.

#### PS-29 — Tenant DLP policies can make a design infeasible: blocked connectors fail at design time and previously built apps/flows are suspended or quarantined at runtime (up to 24 h latency)

**Classification:** RISK / CONSTRAINT
**Evidence:** "If a data policy blocks the use of MSN Weather connector, a maker can't save their flow or app that uses this connector." "If a violation occurs, put the app, flow, or chatbot in to a suspended or quarantine state so that it can't operate." "the latency for full enforcement is 24 hours. In most cases, it's within an hour." Non-blockable connectors exist; custom connectors need governance (S-16).
**Why it matters:** Feasibility depends on the tenant's policy, not only on the platform. A connector-based design must be validated against the target environment's DLP before commitment.
**Decision impact:** Required connector blocked by policy → CONDITIONAL on policy exception or environment placement; otherwise POOR in that tenant.
**Conditions:** Tenant-specific.
**Confidence:** HIGH.
**Sources:** S-16.

### 1.8 Scalability and performance

#### PS-30 — Well-Architected frames fit as "meet performance targets while staying within the throughput and request limits of the platform" and tells teams to prefer platform features, understand service limits, and weigh custom components against skills

**Classification:** RECOMMENDATION
**Evidence:** "A performant workload is able to handle changes in load without compromising the user experience or exceeding throughput and request limits of the platform" (S-26b). PE:03: "Understand service limits … you can avoid issues such as resource contention, performance degradation, or unexpected service interruptions." "Only develop custom code when service features aren't sufficient." Tradeoff: "a Dataverse plugin might fit your performance needs better, but your workload team might only be familiar with Power Automate cloud flows." Database selection: "if your workload requires high-performance real-time data processing, you might choose a database system optimized for fast data ingestion and low latency" (S-24).
**Why it matters:** Microsoft's own architecture guidance treats platform limits as first-class design inputs and acknowledges that some data workloads need other databases.
**Decision impact:** Performance targets that cannot be met within documented limits → HYBRID/CUSTOM for that component.
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-24, S-26b.

### 1.9 Security

#### PS-31 — Dataverse provides the enterprise security model (roles, business units, row sharing, column-level security, hierarchy, encryption, compliance certifications); SharePoint/SQL-connector designs inherit weaker or riskier models

**Classification:** FACT / RISK
**Evidence:** Dataverse: "role-based security … security roles can be associated directly with users, or … teams and business units"; "column-level security feature"; "manager hierarchy and the position hierarchy"; "Encryption of data, at rest and in transit"; compliance via Trust Center (S-12). Dataverse for Teams lacks auditing, field security, hierarchy, record sharing (S-14). SQL via canvas: implicitly shared connections "the least secure … even the name of the database and other details can be discovered"; "secure implicit connections feature was released in January 2024" (S-43). SharePoint security "primarily revolves around securing sites, lists, libraries" (S-49 excerpt).
**Why it matters:** Requirements for row/column-level access, separation of duties, or auditability point strongly to Dataverse and away from SharePoint/Excel stores.
**Decision impact:** Fine-grained authorisation or audit requirement → Dataverse (STRONG technically; premium). Same requirement on SharePoint → POOR.
**Conditions:** Security design still the customer's responsibility (S-30: "Access to data … shouldn't be bypassed when customizing").
**Confidence:** HIGH.
**Sources:** S-12, S-14, S-43, S-49.

#### PS-32 — Network isolation is a documented differentiator: Logic Apps Standard offers VNET integration and private endpoints; Power Platform has since added VNet support, IP firewall, customer-managed keys and Lockbox — but only as Managed Environment features (premium)

**Classification:** CONSTRAINT / TRADE-OFF (version-sensitive)
**Evidence:** Logic Apps migration doc (2025-07): "Azure Logic Apps (Standard) provides security features that differ from the capabilities in Power Automate … Virtual network integration and private endpoints" (S-09). Managed environments overview (2026-02): features include "IP Firewall", "Customer Managed Key (CMK)", "Lockbox", "Virtual Network support for Power Platform", "Conditional access on individual apps"; "Managed environments are included as an entitlement with standalone Power Apps, Power Automate … licenses" (S-18). Code apps: assets served from a public endpoint; IP restriction not applicable (S-19).
**Why it matters:** Strict network-isolation requirements are satisfiable on Power Platform only with premium licensing for all active users; otherwise Azure services are the documented path.
**Decision impact:** Private-network-only requirement → CONDITIONAL (Managed Environments + VNet) or CUSTOM/OTHER (Logic Apps Standard / Azure).
**Conditions:** See conflict C-6.
**Confidence:** HIGH (facts) / MEDIUM (functional equivalence not verified).
**Sources:** S-09, S-18, S-19.

### 1.10 Governance

#### PS-33 — Enterprise-grade governance (sharing limits, pipelines, solution checker, usage insights, extended backups, DR) is packaged as Managed Environments, which requires every active user to hold a standalone licence or PAYG meter

**Classification:** CONSTRAINT / DECISION CRITERION
**Evidence:** Managed environments feature list (S-18). Licensing Guide: "Once enabled, all active usage in the environment will require one of these standalone licenses or pay-as-you-go meters." "'Standalone licenses' … does not include the limited Power Apps, Power Automate and Power Pages use rights that come with select Dynamics 365 and Microsoft 365 licenses." (S-44). Extended backup 28 days and self-service DR need managed environments (S-34, S-37).
**Why it matters:** The governance tier a business-critical solution needs is coupled to premium licensing for its whole audience — a cost step that often surprises "we have M365" organisations.
**Decision impact:** Business-critical + broad audience on seeded licences → CONDITIONAL (budget for premium) — otherwise the solution runs without the governance Microsoft recommends (RISK).
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-18, S-44, S-34, S-37.

#### PS-34 — Ownership and lifecycle: Power Automate access is user-level (leaver risk), flows owned by users can be auto-disabled after 90 days inactivity unless premium; Logic Apps is resource-level RBAC

**Classification:** RISK
**Evidence:** "In Azure Logic Apps, RBAC works at the resource level … if the workflow creator leaves, you don't lose access to their workflows. In Power Automate, RBAC works at the user level" (S-09). "Flows without trigger activity 90 days … might be turned off. Flows owned by users with premium licenses or assigned capacity licenses … aren't subject to this suspension." (S-05). Solutions and service-principal-owned flows with Process licences mitigate (S-04).
**Why it matters:** Operational ownership requirements (IT-owned, survives staff turnover) are a fit criterion; on Power Platform they require solution-based ALM and appropriate licences, not defaults.
**Decision impact:** IT-owned production automation → CONDITIONAL (solutions, service principal, Process licence) or Logic Apps.
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-09, S-05, S-04.

### 1.11 Offline requirements

#### PS-35 — Offline is supported only in the native mobile players (iOS/Android/Windows), never in a browser; Dataverse-based apps get built-in offline-first (up to 3M rows, automatic conflict handling); non-Dataverse apps get only LoadData/SaveData (30–70 MB, manual conflicts); model-driven offline has functional gaps

**Classification:** CONSTRAINT / DECISION CRITERION
**Evidence:** "Canvas apps running in web browsers can't run offline, even when using a web browser on a mobile device." "If your app connects to Dataverse, offline support is built-in … If your app does not use Dataverse, you can use … LoadData and SaveData … You'll generally have 30-70 megabytes of available memory … don't automatically resolve merge conflicts" (S-07). Built-in offline: "Data size limit … 3 million rows", "Conflict resolution Automatic", "Supported Power Fx functions Partial" (S-07b). Model-driven offline limitations: "Field level security and field sharing aren't supported in Mobile offline mode"; personal views unsupported; N:N relationships read-only; max 15 relationships per table in profile; Dataverse search unsupported offline; duplicate detection unsupported (S-07c).
**Why it matters:** "Must work without connectivity" is one of the sharpest fit discriminators: it forces Dataverse (premium), the mobile app (device management), and excludes browser-only deployment.
**Decision impact:** Offline on managed mobile devices with Dataverse → STRONG. Offline on browser/kiosk, or on SharePoint/SQL data → POOR. Complex custom sync semantics (partial sync rules, custom conflict logic beyond automatic) → CUSTOM (T3 corroborates "offline-first mobile applications with sophisticated sync logic" as a structural limit, S-48).
**Conditions:** Field-level security requirement + offline → conflict; check S-07c list against the requirement.
**Confidence:** HIGH.
**Sources:** S-07, S-07b, S-07c, S-48.

### 1.12 External users

#### PS-36 — External users are a licensing and architecture fork: Entra B2B guests can run canvas apps only with a Power Apps licence recognised across tenants (per-app plans are not); anonymous or consumer-identity access requires Power Pages (Dataverse-only data, capacity licensing); multiplexing does not reduce licences

**Classification:** DECISION CRITERION / CONSTRAINT
**Evidence:** Guest canvas access: "the guest user must have a license with Power Apps use rights that matches the capability of the app"; "Power Apps per app plans are scoped to apps in a specific environment, so they can't be recognized across tenants"; guests need "a standalone browser session"; Power Pages vs canvas table: Pages "Browser-only experience / Allows anonymous and authenticated access / Dataverse" vs canvas "Browser and mobile apps / Requires authentication via Microsoft Entra ID / ~150 out-of-the-box connectors and any custom connector" (S-42b). Power Pages licensing: "Authenticated users per website/month" (packs of 100) and "Anonymous users per website/month" (packs of 500); minimum anonymous 200 per environment (S-06 and S-50 excerpt). Portals Web API: "isn't optimized for third-party services or application integration"; "Web API calls made by anonymous users count towards the anonymous user capacity" (S-51). Licensing Guide: "Multiplexing does not reduce the number of subscription licenses of any type required … Any user or device that inputs data into, queries, views data from or otherwise accesses Power Apps, Power Automate and Power Pages apps, directly or indirectly must be properly licensed." External Users defined as non-employees / contractors under 30 h/week / not onsite daily (S-44).
**Why it matters:** Partner/customer/citizen-facing requirements change product (Pages), data store (Dataverse only), identity (external IdPs), and cost model (per unique user per month). Using a shared account or a proxy to avoid licences is explicitly prohibited.
**Decision impact:** Small set of known partner users with Entra B2B → CONDITIONAL (canvas guests, licences). Public/anonymous/consumer → Power Pages (CONDITIONAL on Dataverse data + capacity budget) or CUSTOM web. Public high-traffic API/integration surface → CUSTOM (Portals Web API not intended).
**Conditions:** Pages traffic ceilings not published (U-4).
**Confidence:** HIGH.
**Sources:** S-42b, S-06, S-50, S-51, S-44.

### 1.13 Operational requirements

#### PS-37 — Platform SLA/BCDR: Dataverse 99.9% SLA; in-region availability zones give near-zero RPO and RTO < 5 min automatically for production environments; cross-region failover is self-service (Managed Environments), replication lag typically < 15 min, no published cross-region RTO; connected external systems are outside the resiliency commitment

**Classification:** FACT / CONSTRAINT
**Evidence:** "Dataverse … offers a service level agreement of 99.9% uptime" (S-12). "The recovery point objective is near zero, and the recovery time objective is less than five minutes" in-region; "This in-region capability is for production environments … don't deploy production processes and data in nonproduction types like sandbox, developer, or trial." Self-service DR "is available only for production environments"; "typical replication lag is under 15 minutes (often under five minutes)"; "Microsoft doesn't publish a cross-region RTO commitment"; "when Power Platform solutions connect to external systems—such as SQL Server, REST APIs … the RPO of those integrations are governed by … the respective target systems, and fall outside the scope." Flows under SSDR "have known performance limitations"; "Connectors might have recovery problems when dependent on external systems". Backups: 7 days; 28 days for managed production (S-37, S-34). Logic Apps Standard advertises "Built-in geo-redundancy, multiregion deployment, high availability with automated failover" vs Power Automate "Limited regional deployment options" (S-09).
**Why it matters:** Availability requirements above 99.9%, contractual cross-region RTO, or resilience that includes integrations cannot be met by platform commitments alone.
**Decision impact:** ≤99.9% with in-region HA → STRONG. Contractual cross-region RTO or >99.9% → CONDITIONAL/POOR (customer-run DR, no MS RTO) → consider Azure for the critical path.
**Conditions:** See conflict C-2 (PAYG requirement for SSDR).
**Confidence:** HIGH.
**Sources:** S-12, S-37, S-34, S-09.

#### PS-38 — Monitoring and versioning depth is lower than Azure: "Basic monitoring through the Power Automate portal", "Limited versioning"; Application Insights export exists but as a Managed Environment feature

**Classification:** TRADE-OFF
**Evidence:** Comparison table (S-09). Managed environments: "Export data to Azure Application Insights" (S-18). Canvas custom telemetry to App Insights supported (S-01 endpoint list).
**Why it matters:** Requirements for SRE-grade observability, alerting SLOs and audit of change history raise the bar; they are achievable but require premium tiers and extra design.
**Decision impact:** Observability-heavy operations → CONDITIONAL (Managed Environments + App Insights) or Azure-hosted orchestration.
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-09, S-18, S-01.

### 1.14 Development complexity and team

#### PS-39 — Microsoft's fusion-development guidance names the cases where citizen development is insufficient: no connector exists, additional business logic must be enforced, complex dynamic business flows — resolved by pro developers via custom connectors, Web APIs, API Management, Logic Apps, Functions

**Classification:** PATTERN / DECISION CRITERION
**Evidence:** "Many apps built like this can fulfill an immediate business need quickly and cheaply, but there will always be more complex situations that can't be satisfied in this way. For example, your organization might have existing systems and databases with which the app needs to interact, and for which no connector is currently available. There might be additional business logic that needs to be enforced to ensure that data remains consistent. An app might need to implement a complex, dynamic business flow. This is where professional developers come into play." (S-40b).
**Why it matters:** These three signals (missing connector, integrity logic, complex dynamic flow) are Microsoft's own triggers for HYBRID.
**Decision impact:** Any of the three → HYBRID; all three at scale → consider CUSTOM.
**Conditions:** Requires pro-dev capacity in the delivery team.
**Confidence:** HIGH.
**Sources:** S-40b, S-20.

#### PS-40 — Team skills are an explicit architecture criterion in Well-Architected; the right service may be one the team cannot build or afford

**Classification:** DECISION CRITERION / TRADE-OFF
**Evidence:** "Choose services that your team knows how to use, or commit to training them before you choose a service." "The best service for your workload might be a technology that your team isn't skilled at, can't afford, or it might require extra security layers." (S-24).
**Why it matters:** Fit is relative to the organisation: a HYBRID that needs .NET plug-ins is a POOR fit for a team with no developers, even if technically ideal.
**Decision impact:** Feed team capability into every HYBRID/CUSTOM recommendation.
**Conditions:** —
**Confidence:** HIGH.
**Sources:** S-24.

#### PS-41 — Extension must not replicate the legacy system; out-of-box, configuration, partner (AppSource) solutions come before customisation; every extension has performance, ALM, upgrade and support costs

**Classification:** RECOMMENDATION / ANTI-PATTERN
**Evidence:** "Don't replicate your legacy solution … can also lead to a highly customized solution that fails to apply the strengths of the new platform." "App settings are the safest and least disruptive way to customize your app. You should always try them first." "Low-code and no-code customizations are the best way to extend your app when changing the app settings doesn't meet your requirements." "Use partner solutions … instead of extending." Extension risks: "overextending forms, synchronous events that affect the user experience, and impact on capacity such as service protection limits" (S-30, S-30b).
**Why it matters:** For requirements adjacent to Dynamics 365 or an existing SaaS, "build in Power Platform" competes with "configure/buy". Discovery must surface the existing-capability option.
**Decision impact:** Requirement already covered by a first-party app or marketplace solution → CUSTOM/OTHER (buy/configure) before build.
**Conditions:** Dynamics 365 context; also applies to M365 features (Lists, Planner, Forms) as the "existing capability" option.
**Confidence:** HIGH.
**Sources:** S-30, S-30b.

### 1.15 Licensing and cost

#### PS-42 — The licence boundary is a fit boundary: Microsoft 365 seeded rights = standard connectors + Dataverse for Teams only; premium connectors, custom connectors, on-premises/cloud data transfer, full Dataverse, model-driven apps, Power Pages, Managed Environments all require premium licences (Premium $20/user/month list; per-app PAYG $10/active user/app/month; Process 250k requests/day)

**Classification:** DECISION CRITERION / CONSTRAINT
**Evidence (S-44, Sept 2026):** Power Apps Basic "allows users to customize and extend Microsoft 365 and Office 365 for productivity scenarios, and to deliver a comprehensive low-code extensibility platform for Microsoft Teams only." Table: Standard connectors ⚫ all columns; "Premium and custom connectors" and "On premises and cloud services data transfer" only Premium / per-app PAYG / D365; "Full Dataverse access" — M365 column "Dataverse for Teams only". "Power Apps Premium $20 per user/month* (or $12 … with 2,000+ new per user licenses)"; "Power Apps per app pay-as-you-go meter $10 per active user/app/month". "Power Automate use rights included with Power Apps don't include RPA functionality". Dynamics 365 rights "must be only within the context of and in the same environment as the licensed Dynamics 365 application". Restricted Dynamics 365 tables require D365 licences (list is on a web page not captured — U-5). FAQ: per app "$5/user/app/month" subscription (S-06) — note two figures exist for different SKUs (subscription vs PAYG meter).
**Why it matters:** Whether a requirement can stay on "included" licences determines cost by orders of magnitude and is the most frequent cause of architectures distorted to avoid premium (PS-43).
**Decision impact:** Requirement satisfiable with standard connectors + SharePoint/Dataverse for Teams → STRONG on seeded licences. Any premium trigger → CONDITIONAL on licence budget for the whole audience (multiplexing forbids workarounds).
**Conditions:** Prices/SKUs volatile; verify month/year.
**Confidence:** HIGH (rules) / MEDIUM (prices, region).
**Sources:** S-44, S-06.

#### PS-43 — Licensing-driven architecture is an anti-pattern: choosing SharePoint/Excel or a shared account to avoid premium licences produces delegation, threshold, security and compliance failures

**Classification:** ANTI-PATTERN
**Evidence:** Composite: delegation limits on SharePoint (S-10, S-02); list view threshold 5,000 and lookup column problems recurring in community and Microsoft Q&A (T4, S-45); SharePoint security model is site/list-scoped (S-49); implicit SQL connection risk (S-43); multiplexing prohibition (S-44). Microsoft: "Switch to Microsoft Dataverse as your data source for the broadest delegation support" (S-49 excerpt).
**Why it matters:** The pattern is very common and its cost appears late (post-pilot).
**Decision impact:** If the only reason for the data store is licence avoidance and the requirement has relational/security/volume needs → flag RISK; re-evaluate Dataverse or CUSTOM.
**Conditions:** Genuinely document-centric, small, low-security lists are fine on SharePoint.
**Confidence:** MEDIUM (T4 corroboration; T1 mechanics HIGH).
**Sources:** S-02, S-10, S-45, S-49, S-43, S-44.

### 1.16 When another Microsoft technology or a hybrid is more appropriate

#### PS-44 — Consolidated Microsoft-documented redirects away from (or alongside) Power Platform

**Classification:** PATTERN / RECOMMENDATION

| Requirement signal | Microsoft-documented target | Evidence |
|---|---|---|
| Complex, high-volume, security-sensitive orchestration; IT-owned; VNET; Git CI/CD; B2B/EDI | Azure Logic Apps (Standard) | S-08, S-09 |
| Code-first orchestration, stateful long-running coordination, heavy compute | Azure Functions / Durable Functions | S-08, S-30b |
| Large-scale ETL / data transformation | Dataflows (Power Query) or Azure data services | S-22, S-23 |
| High-performance transactional business logic on Dataverse data | Dataverse plug-ins (2-minute limit) | S-27, S-22 |
| Reliable event fan-out / decoupling | Dataverse → Service Bus / Event Hubs / webhooks | S-21 |
| Bespoke SPA UX with platform governance | Power Apps code apps | S-19 |
| Public / anonymous / external identity web | Power Pages (Dataverse-only) or custom web | S-42b, S-51 |
| Existing first-party or ISV capability | Configure / AppSource before build | S-30 |
| Real-time high-ingestion data | Purpose-built database ("optimized for fast data ingestion and low latency") | S-24 |

**Why it matters:** Every row is a Microsoft-authored boundary; the pack can encode these as "consider alternative" triggers without inventing them.
**Decision impact:** Presence of a left-column signal moves the component to HYBRID or CUSTOM/OTHER.
**Conditions:** Hybrid adds Azure subscription, DevOps and skills (PS-40).
**Confidence:** HIGH.
**Sources:** as listed.

---

## 2. Consolidated fit matrix

Observable characteristic → default fit class → governing findings. "Default" means before organisation-specific factors (skills, licences owned, tenant policy).

| # | Characteristic of the requirement | Default fit | Findings |
|---|---|---|---|
| 1 | Internal form / approval / inspection / asset / calculation / case app, structured data, moderate volumes | STRONG | PS-01, PS-21, PS-22 |
| 2 | Relational, process-heavy, many related tables, needs row/column security or audit | STRONG (model-driven + Dataverse; premium) | PS-02, PS-14, PS-31 |
| 3 | Small team app inside Teams, <1M rows, no API/offline/audit | STRONG (Dataverse for Teams, seeded) | PS-16, PS-42 |
| 4 | Document-centric collaboration with light metadata | STRONG (SharePoint) | PS-14 |
| 5 | Human-in-the-loop workflow, waits ≤30 days | STRONG | PS-22 |
| 6 | Queried tables > 2,000 rows on canvas | CONDITIONAL (delegable source + formulas) | PS-13, PS-14 |
| 7 | Business-critical (financial/regulatory impact) | CONDITIONAL (mission-critical operating model, Managed Environments, premium) | PS-04, PS-33, PS-37 |
| 8 | Org-wide audience or sensitive data | CONDITIONAL (enterprise environment class, ALM) | PS-05, PS-33 |
| 9 | Premium/custom connectors, on-premises data, SQL | CONDITIONAL (licence for whole audience, gateway) | PS-26, PS-42 |
| 10 | Requests/day per owner approaching licence entitlement | CONDITIONAL (Process/PAYG) → HYBRID | PS-19, PS-23 |
| 11 | Offline on managed mobile devices with Dataverse | STRONG/CONDITIONAL (mobile app only) | PS-35 |
| 12 | Offline in browser, or offline on non-Dataverse data | POOR | PS-35 |
| 13 | Known external partners via Entra B2B | CONDITIONAL (guest licensing) | PS-36 |
| 14 | Anonymous / consumer / public audience | CONDITIONAL (Power Pages, Dataverse-only, capacity cost) or CUSTOM | PS-36, PS-10 |
| 15 | Large-scale ETL, nightly mass processing | POOR for flows → dataflows / Azure | PS-07, PS-25 |
| 16 | Algorithmic core (optimisation, rules engine, state machine) | HYBRID (plug-in/Functions) or CUSTOM | PS-08, PS-09 |
| 17 | Synchronous response > ~2 min expected by caller | POOR (as sync) → async redesign / HYBRID | PS-28 |
| 18 | Any single flow hard limit exceeded (500 actions, 100k items, 100 MB, 10 GB/day) | POOR for that flow → Logic Apps / Functions | PS-23 |
| 19 | Sustained high write throughput to Dataverse from integrations | CONDITIONAL (design for 429s) → HYBRID | PS-18 |
| 20 | Network-isolated (private endpoints only) | CONDITIONAL (Managed Env + VNet) or Logic Apps Standard | PS-32 |
| 21 | Contractual cross-region RTO, >99.9% availability, resilience incl. integrations | CONDITIONAL/POOR → Azure critical path | PS-37 |
| 22 | IT-owned automation surviving staff turnover, deep observability, Git CI/CD | CONDITIONAL (solutions, service principal, Process licence) or Logic Apps | PS-34, PS-38 |
| 23 | Pixel-perfect brand-critical UX | CONDITIONAL (canvas + PCF) / HYBRID (code apps) / CUSTOM (public) | PS-10, PS-03 |
| 24 | Embed inside native desktop/mobile product; heavily proxied network | POOR / CUSTOM | PS-12 |
| 25 | Very large single-app scope (thousands of controls, hundreds of sources) | CONDITIONAL (partition) | PS-06 |
| 26 | Requirement already covered by first-party / ISV / M365 feature | CUSTOM/OTHER (configure or buy) | PS-41 |
| 27 | No pro-dev capacity but HYBRID needed | RISK → reduce scope or CUSTOM by vendor | PS-40 |
| 28 | Exact datacentre disclosure required | POOR | PS-17 |

---

## 3. Anti-patterns (consolidated)

| Id | Anti-pattern | Why it fails | Evidence |
|---|---|---|---|
| AP-1 | Complex business logic or ETL inside cloud flows | Bottlenecks, unmaintainable, limits/quotas | PS-07, PS-25 |
| AP-2 | Nested for-each / per-record loops for thousands of rows | Multiplies actions, throttling, 100k item cap | PS-25, PS-23 |
| AP-3 | Self-triggering flows (update triggers own update) | Infinite loops, throttling | PS-25 |
| AP-4 | Non-delegable formulas over large tables | Silent wrong results at 500/2,000 rows | PS-13 |
| AP-5 | SharePoint/Excel as relational system of record to avoid premium | Delegation, 5,000 threshold, security, integrity | PS-14, PS-43 |
| AP-6 | Implicitly shared SQL connections | Credentials effectively shared; data exposure | PS-31 |
| AP-7 | Production processes in default/sandbox/dev environments | No AZ resilience commitment; governance gaps | PS-37, PS-05 |
| AP-8 | Shared account / proxy to reduce licences | Multiplexing violation | PS-36, PS-42 |
| AP-9 | Replicating the legacy system feature-for-feature | Over-customisation, technical debt | PS-41 |
| AP-10 | Synchronous plug-ins / heavy forms | UX latency, 2-minute cap, service protection | PS-09, PS-41 |
| AP-11 | Giant single canvas app / OnStart-heavy | Studio and runtime degradation | PS-06 |
| AP-12 | Business-critical solution without Managed Environments/ALM | Runs outside Microsoft's recommended operating model | PS-04, PS-33 |

---

## 4. Conflicts (CONFLICTED)

| Id | Topic | Source A | Source B | Assessment |
|---|---|---|---|---|
| C-1 | Default Dataverse database capacity per tenant | Licensing Guide table: "Power Apps Premium — Dataverse Database 20 GB (default)" (S-44 p.~21) | Same guide worked example: "if a new customer purchases Power Apps Premium, the tenant will receive 10 GB of default Dataverse Database capacity" (S-44) | Internal inconsistency in the same T1 document. Use admin-center actuals; treat the number as UNKNOWN until verified on the tenant. |
| C-2 | Self-service DR billing prerequisite | Licensing Guide (Sept 2026): "To use self-serve disaster recovery for an environment, it must be linked to a pay-as-you-go billing plan" (S-44) | BCDR admin page (2026-08-20): "A pay-as-you-go billing plan is no longer a mandatory requirement" (S-37) | Version drift between documents published weeks apart. Product doc is more recent; verify at decision time. |
| C-3 | Power Automate scale | Comparison table: Power Automate "Small to medium scale workflows … limited by shared resources" (S-09) | Limits: Process licence 250k requests/day official, 500k transition; content throughput 10 GB/day High profile (S-04, S-05) | Not contradictory once "scale" is read as dedicated compute, latency and throughput guarantees rather than raw request counts. Record as TRADE-OFF: PA scales by licence within a multitenant envelope; Logic Apps Standard offers dedicated resources. |
| C-4 | Concurrent users | No T1 ceiling documented (S-01, S-11) | T3/T4 report degradation "with larger data sets or higher concurrency" (S-48) | Not a documented limit; performance is a function of data source and design. Treat as UNKNOWN per workload; test. |
| C-5 | Canvas control limits | T4/older guidance: 500 controls/app, 300/screen (S-46) | Current T1: "more than 100 tables and over 50 screens while keeping excellent performance" and qualitative "thousands of controls" warning (S-25, S-26) | Numbers are recommendations, not enforced limits; keep as MEDIUM-confidence heuristics. |
| C-6 | Network isolation on Power Platform | Logic Apps migration doc (2025-07): VNET/private endpoints differentiate Logic Apps from Power Automate (S-09) | Managed environments (2026-02) list "Virtual Network support for Power Platform" (S-18) | Version-sensitive; functional parity not verified. Requirement-level check needed (which connectors/flows run inside the VNet). |
| C-7 | Per-app price | FAQ: "Power Apps per app … $5/user/app/month" (S-06) | Licensing Guide: "Power Apps per app pay-as-you-go meter $10 per active user/app/month" (S-44) | Different SKUs (subscription vs PAYG meter); not a true conflict but easy to confuse. |

---

## 5. Unknowns (UNKNOWN)

| Id | Unknown | Why it matters | How to resolve |
|---|---|---|---|
| U-1 | When strict enforcement of Power Platform request limits starts ("no current ETA") | Volume designs built on transition limits may break | Track admin-center reporting GA announcements |
| U-2 | Concurrent-user ceilings for canvas/model-driven apps | Sizing large-audience apps | Load test against target data source; monitor 429s |
| U-3 | Number of Dataverse web servers per environment (service protection scales per server) | Throughput planning for integrations | "Let the server tell you" (S-03); measure |
| U-4 | Power Pages hard traffic/throughput ceilings | Public high-traffic sites | Microsoft states auto-scale by licensed capacity; no numbers found |
| U-5 | Current list of restricted Dynamics 365 tables | Licensing of apps touching D365 tables | Web page referenced by Licensing Guide (not captured) |
| U-6 | Cross-region RTO commitment | Contractual DR | Microsoft explicitly does not publish one |
| U-7 | Code apps roadmap (Git integration, mobile, IP restrictions) | Hybrid viability | Re-check S-19 at decision time |
| U-8 | Local-currency pricing and EA discounts | Cost modelling | Obtain regional price list |
| U-9 | Full text of Power Automate planning guidance pages (fetch redirected to Plan designer page) | PS-21 rests on search excerpts | Re-fetch or read in browser |
| U-10 | SOAP/legacy protocol support via custom connectors | Legacy integration fit | Not researched here (Area 05) |
| U-11 | Whether Managed Environments VNet support covers canvas app connector calls end-to-end | Network-isolation fit | Area 06 research |

---

## 6. Implications for aisa (not pack content — pointers for later authoring)

Recorded as guidance for the authoring phase; nothing here is a question, glossary term, signal or node yet.

- **Discovery signals worth deriving (technology-neutral):** queried-table volume per screen; requests/day per process owner; longest human wait in the process; synchronous response expectation of callers; offline device class and connectivity pattern; external audience type (known partner vs anonymous public); data-access granularity (row/column); audit/regulatory obligations; network isolation mandate; contractual availability/RTO; embedding target (browser vs native product); existing capability already covering the need; team pro-dev capacity; tenant DLP posture; data-heavy attachments/audit growth.
- **Decision criteria that emerged as hard boundaries:** flow hard limits (PS-23); browser offline (PS-35); Dataverse-only for Power Pages and model-driven (PS-02, PS-36); multiplexing (PS-36); 2-minute plug-in cap (PS-09); Managed Environments ↔ premium for all active users (PS-33).
- **Options the pack must be able to output:** "do nothing / process change", "existing M365 or first-party capability", "Power Platform standard-licence solution", "Power Platform premium solution", "Hybrid with Azure", "Logic Apps/Azure-first", "custom application", "buy (ISV)".
- **Validation before commitment (typical):** delegation proof with data row limit = 1; request-volume estimate vs entitlement; DLP check in target environment; licence census of the full audience; offline limitation checklist against required features; sync/async latency measurement of integrated systems.

---

## 7. Coverage against research-areas.md §01

| Item | Covered by |
|---|---|
| Problems PP is designed to solve | PS-01, PS-21, PS-22 |
| Problems it is not designed to solve | PS-07, PS-23, PS-24, PS-35, PS-44 |
| Characteristics of successful solutions | PS-01, PS-02, PS-04 (mission-critical model), PS-30 |
| Characteristics of poor candidates | §2 rows 12, 15, 17, 18, 24, 28; §3 |
| Good / conditional / poor factors | §2 |
| Boundary with traditional development | PS-03, PS-08, PS-09, PS-39, PS-44 |
| Boundary with other Microsoft technologies | PS-24, PS-27, PS-41, PS-44 |
| When hybrid is preferable | PS-07, PS-09, PS-27, PS-39, PS-44 |

---

## 8. Source register

All Microsoft Learn URLs fetched 2026-09-02. `ms.date` = document date shown in page metadata.

| Id | Tier | Title | URL | Date |
|---|---|---|---|---|
| S-01 | T1 | Power Apps system requirements and limits | https://learn.microsoft.com/en-us/power-apps/limits-and-config | 2026-01-12 |
| S-02 | T1 | Understand delegation in a canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview | 2026-01-13 |
| S-03 | T1 | Service protection API limits (Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/api-limits | 2026-01-09 |
| S-04 | T1 | Requests limits and allocations | https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations | 2026-08-14 |
| S-05 | T1 | Limits of automated, scheduled, and instant flows | https://learn.microsoft.com/en-us/power-automate/limits-and-config | 2026-07-17 |
| S-06 | T1 | Power Platform licensing FAQs | https://learn.microsoft.com/en-us/power-platform/admin/powerapps-flow-licensing-faq | 2026-08-14 |
| S-07 | T1 | Develop offline-capable canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/offline-apps | 2024-03-18 |
| S-07b | T1 | Mobile offline for canvas apps overview | https://learn.microsoft.com/en-us/power-apps/mobile/canvas-mobile-offline-overview | 2024-06-05 |
| S-07c | T1 | Mobile offline limitations for model-driven apps | https://learn.microsoft.com/en-us/power-apps/mobile/offline-limitations | 2024-09-26 |
| S-08 | T1 | Integration and Automation Platform Options in Azure | https://learn.microsoft.com/en-us/azure/azure-functions/functions-compare-logic-apps-ms-flow-webjobs | 2026-03-23 |
| S-09 | T1 | Power Automate migration to Azure Logic Apps (Standard) | https://learn.microsoft.com/en-us/azure/logic-apps/power-automate-migration | 2025-07-18 |
| S-10 | T1 | Connect to SharePoint from a canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online | 2025-03-14 |
| S-11 | T1 | Performance considerations for Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/app-performance-considerations | 2024-12-10 |
| S-12 | T1 | Why choose Microsoft Dataverse? | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/why-dataverse-overview | 2026-05-21 |
| S-13 | T1 | Dataverse capacity-based storage details | https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage | 2026-08-17 |
| S-14 | T1 | Dataverse for Teams vs. Dataverse | https://learn.microsoft.com/en-us/power-apps/teams/data-platform-compare | 2025-05-28 |
| S-15 | T1 | Choose the region when setting up an environment | https://learn.microsoft.com/en-us/power-platform/admin/regions-overview | 2026-05-28 |
| S-16 | T1 | Data policies (DLP) | https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention | 2026-04-07 |
| S-17 | T1 | Power Pages architecture | https://learn.microsoft.com/en-us/power-pages/admin/architecture | 2026-04-28 |
| S-18 | T1 | Managed environments overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview | 2026-02-23 |
| S-19 | T1 | Power Apps code apps overview | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview | 2026-08-12 |
| S-20 | T1 | Introduction to Microsoft Power Platform for developers | https://learn.microsoft.com/en-us/power-platform/developer/get-started | 2025-12-04 |
| S-21 | T1 | Azure Service Bus Integration for Dataverse | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/azure-integration | 2026-03-31 |
| S-22 | T1 | Simplify cloud flows by offloading complex business logic | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/leave-complex-business-logic-out | 2025-07-11 |
| S-23 | T1 | Avoid anti-patterns (Power Automate) | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/avoid-anti-patterns | 2025-07-10 |
| S-24 | T1 | PPWA PE:03 Select the right services and features | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/select-services | 2025-08-15 |
| S-25 | T1 | Build large and complex canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/working-with-large-apps | 2023-04-07 |
| S-26 | T1 | How to create performant Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview | 2026-08-20 |
| S-26b | T1 | PPWA Performance Efficiency design principles | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/principles | 2025-08-15 |
| S-27 | T1 | Use Plug-ins to Extend Business Processes | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/plug-ins | 2026-03-30 |
| S-28 | T1 | Custom process actions / low-code plug-in tips (2-minute limit; via search excerpts) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/workflow-custom-actions ; https://learn.microsoft.com/en-us/power-apps/maker/data-platform/low-code-plug-ins-tips | n/a |
| S-29 | T1 | Limitations of Power Apps component framework | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations | 2025-07-01 |
| S-30 | T1 | D365 Implementation Guide: Extend Dynamics 365 apps without compromising performance | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/extend-your-solution | 2025-07-08 |
| S-30b | T1 | D365 Implementation Guide: Customize and extend Dynamics 365 apps (no-cliffs, PaaS) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/extend-your-solution-scenarios | 2025-07-08 |
| S-31 | T1 | Overview of building a model-driven app | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-driven-app-overview | 2026-01-09 |
| S-32 | T1 | Start building apps (app types, custom pages) | https://learn.microsoft.com/en-us/power-apps/maker/ | 2025-11-17 |
| S-33 | T1 | Power Apps patterns overview (content via search excerpt; direct fetch redirected) | https://learn.microsoft.com/en-us/power-apps/guidance/patterns/overview | n/a |
| S-34 | T1 | Plan mission critical workloads | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/plan-mission-critical | 2026-05-04 |
| S-35 | T1 | Develop a tenant environment strategy | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/environment-strategy | 2026-05-04 |
| S-36 | T1 | Create accessible canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps | 2022-09-06 |
| S-37 | T1 | Business continuity and disaster recovery | https://learn.microsoft.com/en-us/power-platform/admin/business-continuity-disaster-recovery | 2026-08-20 |
| S-38 | T1 | Types of process automation to consider (Power Automate planning; via search excerpt) | https://learn.microsoft.com/en-us/power-automate/guidance/planning/various-types-process-automation | n/a |
| S-39 | T3 | Power Automate vs Logic Apps (PnP community, Paul Bullock) | https://pnp.github.io/community-docs/articles/power-automate-vs-logic-apps.html | n/a |
| S-40 | T1 | Connect to SQL Server from Power Apps overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-connection-overview | 2025-03-14 |
| S-40b | T1 | Fusion development e-book, ch.1 | https://learn.microsoft.com/en-us/power-apps/guidance/fusion-dev-ebook/01-what-is-fusion-dev-approach | 2021-04-26 |
| S-41 | T3 | Alan Bonnici — "The Complexity Ceiling: Where Microsoft Power Apps Needs to Evolve" | https://www.alanbonnici.com/2026/05/the-complexity-ceiling-where-microsoft.html | 2026-05 |
| S-42 | T3 | Arinco — Power Apps Code Apps: when to use them | https://arinco.com.au/blog/power-apps-code-apps-when-to-use-them/ | n/a |
| S-42b | T1 | Share a canvas app with guest users | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/share-app-guests | 2025-06-27 |
| S-43 | T1/T2 | Use Microsoft SQL Server securely with Power Apps; Enhanced security for implicitly shared connections (blog) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-server-security ; https://www.microsoft.com/en-us/power-platform/blog/power-apps/power-apps-secure-implicit-connections/ | 2024-01 |
| S-44 | T1 | Power Platform Licensing Guide, September 2026 (PDF, 30 pp.) | https://go.microsoft.com/fwlink/?LinkId=2085130 | 2026-09 |
| S-45 | T4 | Community/Q&A: SharePoint 5,000 threshold and lookup delegation issues | https://learn.microsoft.com/en-my/answers/questions/5600910/ ; https://www.matthewdevaney.com/sharepoint-delegation-cheat-sheet-for-power-apps/ | n/a |
| S-46 | T4 | Community: 500 controls/app, 300/screen heuristics | https://www.itaintboring.com/power-platform/why-500-matters-for-canvas-apps/ ; https://hiredgun.tech/canvas-app-size/ | n/a |
| S-47 | T4 | Community: Apply-to-each concurrency, throttling, variables in loops | https://sharepains.com/2025/05/15/how-to-avoid-throttling-power-automate/ ; https://theaugmenteddev.com/blog/speeding-up-apply-to-each-power-automate | 2025 |
| S-48 | T3 | Brilworks — Power Apps limitations: signs you need custom development | https://www.brilworks.com/blog/power-apps-limitations/ | n/a |
| S-49 | T1 | Training module: Benefits of using Power Apps with SharePoint / delegation guidance (search excerpts) | https://learn.microsoft.com/en-us/training/modules/get-started-power-apps-sharepoint/benefits | n/a |
| S-50 | T1 | Power Pages website capacity consumption reports | https://learn.microsoft.com/en-us/power-pages/admin/website-consumption-reports | n/a |
| S-51 | T1 | Overview of the Power Pages portals Web API | https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview | 2026-08-27 |

Excluded/failed: TechTarget "top Power Apps limitations" (HTTP 404); Power Apps planning guide pages (`/power-apps/guidance/planning/*`) and Power Automate planning pages redirected to the Plan designer page — content taken from search excerpts only and marked MEDIUM.
