Research Status: VALIDATED
Research Confidence: MEDIUM
Gate: PASS

# Platform Suitability — Canonical Research Evidence

Research area: **01 — Platform Suitability** (`../research-areas.md`).
Canonical version: **2026-09-02**, consolidated from `platform-suitability-research-v2.md` (primary) with the conditions of `platform-suitability-gate-v2.md`. Superseded drafts kept for traceability: `platform-suitability-v1.md`, `platform-suitability-review.md`, `platform-suitability-gate.md`.
Source policy: `../source-policy.md`. Quotes are verbatim English. Prices are USD list.

**Purpose.** Answer, with traceable evidence: *"Given these requirements, constraints and risks, should Power Platform be considered, and if so, what type of architecture is appropriate?"* This is not a product summary. Positive capabilities appear only where they define a fit boundary.

**How to read confidence.** HIGH = dated Tier 1 statement or limit. MEDIUM = Tier 1 but excerpt-level, aged (> 18 months) or inferred; or Tier 3 with partial Tier 1 corroboration. UNKNOWN = not established. Gate V2 capped the file at MEDIUM overall because the positive-fit half rests on inference from absent constraint violations, the SLA document was not read, and performance has no empirical evidence.

**Gate conditions carried into this file (mandatory for downstream use):**
1. Every fit verdict derived from §2 must carry the row's origin tag (**MS** Microsoft statement / **INF** analyst inference from documented limits / **T3** independent source / **UNKNOWN**) and the relevant U-ids from §8. STRONG must be phrased as "no documented constraint violated", never as Microsoft endorsement.
2. Before pack authoring: read the September 2026 SLA document (U-12) and the Licensing Guide add-on section (U-15); confirm flow-changeset restrictions from the fetched page (S-55).
3. Dimensions deferred to Areas 02–15 (§9) must back-reference this file; if not delivered, the corresponding matrix rows revert to UNKNOWN.

**Volatility.** All limits, licences, prices and feature flags are valid on the page dates in §11. Re-verify before encoding.

---

## 1. Classification model

| Fit class | Meaning |
|---|---|
| **STRONG FIT** | Requirement maps to documented platform positioning; no documented limit approached; standard licence path. Phrased as "no documented constraint violated". |
| **CONDITIONAL FIT** | Fit depends on a measurable condition (volume, licence, data source, governance maturity, team) that must be validated before commitment. |
| **POOR FIT** | Collides with a documented hard limit, an explicit Microsoft "not the best choice" statement, or an unsupported scenario. |
| **HYBRID** | Power Platform for UX / orchestration / data plus Azure or code for the part that exceeds platform limits (Microsoft's "no-cliffs" approach). |
| **CUSTOM / OTHER** | Another Microsoft technology, or configure/buy, is documented as more appropriate for the whole requirement. |

Evidence tags (one dominant tag per finding): FACT, RECOMMENDATION, CONSTRAINT, TRADE-OFF, RISK, ANTI-PATTERN, DECISION CRITERION, PATTERN. Source tiers T1–T4 per `../source-policy.md`.

---

## 2. Fit matrix

| # | Observable characteristic | Threshold / measure | Default fit | Origin | Findings |
|---|---|---|---|---|---|
| 1 | Internal structured-data app: forms, approvals, inspections, asset/case tracking | Queried tables ≤ 2,000 rows or delegable; ≤ 6,000 requests/day/user on seeded licences | STRONG | MS + INF | PS-01, PS-13, PS-19 |
| 2 | Relational, process-heavy data with row/column security or audit | Any | STRONG (model-driven + Dataverse; premium) | MS | PS-02, PS-14, PS-31 |
| 3 | Team app inside Teams | < 2 GB / ≈1M rows; no API, offline, audit, field security | STRONG (Dataverse for Teams, seeded) | MS | PS-16 |
| 4 | Document-centric collaboration | Light metadata, no relational queries | STRONG (SharePoint) | MS | PS-14 |
| 5 | Human-in-the-loop workflow | Longest pending wait ≤ 30 days | STRONG | MS | PS-22 |
| 6 | Canvas over large tables | > 2,000 rows in any queried table | CONDITIONAL (delegable source + formulas) | MS | PS-13 |
| 7 | Business-critical process | Downtime causes financial/regulatory harm | CONDITIONAL (mission-critical model; Managed Environments; premium for all active users) | MS | PS-04, PS-33 |
| 8 | Broad audience or sensitive data | Beyond a personal-productivity sharing scope (Microsoft's own default-environment guidance caps sharing at 5–50 users) | CONDITIONAL (enterprise environment class, ALM) | MS | PS-05 |
| 9 | Premium/custom connectors, on-prem or SQL data | Any | CONDITIONAL (licence for whole audience; gateway) | MS | PS-26, PS-42 |
| 10 | Automation volume | Requests/day/owner vs 6,000 / 40,000 / 250,000 (Process, stackable ×10) | CONDITIONAL → HYBRID above | MS | PS-19, PS-23 |
| 11 | Integration write throughput into Dataverse | > 6,000 requests / 5 min / user or > 52 concurrent | CONDITIONAL (429 handling) → HYBRID | MS | PS-18 |
| 12 | Offline, managed mobile, Dataverse | ≤ 3M rows; features within PS-35 list | STRONG/CONDITIONAL | MS | PS-35 |
| 13 | Offline in browser, or offline on non-Dataverse data | Any | POOR | MS | PS-35 |
| 14 | External partners with Entra B2B | Licence recognised cross-tenant (per-app plans are not) | CONDITIONAL | MS | PS-36 |
| 15 | Anonymous / public audience | Unique users/month × pack; Dataverse-fronted data | CONDITIONAL (Power Pages) or CUSTOM | MS | PS-36, PS-56 |
| 16 | ETL / nightly mass processing in flows | Thousands of rows per run | POOR for flows → dataflows / Azure | MS | PS-07, PS-25 |
| 17 | Algorithmic core (iteration to convergence, mutable state, recursion) | Any | HYBRID (plug-in / Functions) or CUSTOM | T3 + INF | PS-08 |
| 18 | Synchronous caller wait | > 120 s (flow) / 180 s (canvas) | POOR as sync → async / HYBRID | MS | PS-28 |
| 19 | Flow hard limits | > 500 actions, nesting > 8, > 100,000 items, > 100 MB, > 10 GB/day | POOR for that flow → Logic Apps / Functions | MS | PS-23 |
| 20 | Private-network-only | No public endpoints permitted | CONDITIONAL (Managed Env + VNet) or Logic Apps Standard | MS (version-sensitive) | PS-32 |
| 21 | Availability / DR | > 99.9%, contractual cross-region RTO, or integrations inside the resilience boundary | CONDITIONAL / POOR | MS + UNKNOWN | PS-37, PS-52 |
| 22 | IT-owned automation, Git-first, deep observability | Any | CONDITIONAL (solutions, pipelines, Git integration, App Insights — all premium) or Logic Apps Standard | MS | PS-24, PS-48 |
| 23 | Brand-critical UX | Design-system branding, native gestures | CONDITIONAL (canvas+PCF) / HYBRID (code apps) / CUSTOM | MS + T3 | PS-10, PS-03 |
| 24 | Embed in native product; intercepting proxies | Any | POOR / CUSTOM | MS | PS-12 |
| 25 | Single-app scope | Thousands of controls, hundreds of sources, formulas > 256k chars | CONDITIONAL (partition) | MS | PS-06 |
| 26 | Need already covered by first-party / ISV / M365 feature | Any | CUSTOM/OTHER (configure or buy) | MS | PS-41 |
| 27 | No pro-dev capacity but HYBRID needed | Any | RISK | MS | PS-40 |
| 28 | Multi-record / multi-system atomicity | Writes that must succeed or fail together | CONDITIONAL inside Dataverse (change set / plug-in) — POOR across connectors or on elastic tables → compensation or CUSTOM | MS | PS-45, PS-57 |
| 29 | On-premises / air-gapped / customer-hosted | Any | POOR (SaaS only) | MS | PS-47 |
| 30 | Regulated sovereign cloud | GCC/GCC High/DoD eligibility; China 21Vianet | CONDITIONAL (eligibility; parity exceptions) | MS | PS-47 |
| 31 | Frozen behaviour / long solution lifetime | Cannot absorb two mandatory release waves per year; > 5-year lifetime | RISK → CONDITIONAL | MS | PS-50 |
| 32 | Exit / portability requirement | Must be re-hostable off Microsoft | RISK (UI and flows rewrite; data portable) | MS + INF | PS-51 |
| 33 | Concurrent edits on the same record | Multi-user contention | CONDITIONAL (Dataverse optimistic concurrency via code; canvas conflict handling) | MS | PS-46 |
| 34 | Users without Entra work/school identity | Frontline, shared devices, non-Entra IdP | CONDITIONAL (B2B, Pages identities); UNKNOWN for frontline licensing | MS (partial) | PS-60 |
| 35 | Automated testing required (mission-critical) | Any | CONDITIONAL (Playwright, code-first; Test Engine deprecated) | MS | PS-53 |
| 36 | Exact datacentre disclosure | Any | POOR | MS | PS-17 |

---

## 3. Decision boundaries (requirement × condition → constraint)

Validated by Gate V2 as the strongest evidence-backed boundaries. Origin in brackets.

- Queried table > 2,000 rows × non-delegable Power Fx (or SharePoint complex columns / relational filters on ID) → silent partial results at runtime (MS, S-02/S-10).
- Writes that must succeed or fail together × any write outside Dataverse standard tables → no atomicity; hand-built compensation → POOR for low-code alone (MS, S-52/S-57/S-58). Same × all writes on Dataverse standard tables → atomic via change set (≤ 1,000 ops) or synchronous plug-in (2-minute cap) → CONDITIONAL (MS, S-52/S-54/S-27).
- Cloud flow × > 500 actions, nesting > 8, > 100,000 loop items, > 100 MB payload, > 10 GB/day, pending step > 30 days → failure/time-out (MS, S-05).
- Synchronous caller × latency > 120 s (flow) / 180 s (canvas) → time-out → async or Azure orchestration (MS, S-05/S-01).
- Owner licence × requests/day: seeded 6,000 / Premium 40,000 / Process 250,000 stackable ×10 → throttling; consistently throttled flows turned off after 14 days (MS, S-04/S-05/S-48b).
- Integration identity × > 6,000 requests or > 52 concurrent per 5 min per web server → 429 with Retry-After (MS, S-03).
- Offline × browser client, or × non-Dataverse data beyond 30–70 MB → unsupported (MS, S-07/S-07b). Offline × Dataverse × field-level security, N:N edits, personal views → unavailable offline (MS, S-07c).
- Any audience × premium/custom connector, on-prem data, model-driven app, Power Pages or Managed Environment → standalone licence for every active user; multiplexing prohibited (MS, S-44).
- Disconnected or customer-hosted deployment → unsupported (MS, S-68/S-47a). US public-sector regulated data or data-in-China → sovereign cloud with eligibility and parity exceptions (MS, S-47b/S-47c).
- Frozen behaviour / per-release change control → conflicts with mandatory semi-annual waves and rolling deprecations (MS, S-66/S-67).
- Re-hostable off Microsoft → UI, Power Fx, flows not portable; data and .NET plug-ins are (MS + INF, S-40c/S-64/S-62).
- IT-owned automation × private-network runtime, dedicated compute, local debugging or B2B/EDI → Logic Apps Standard; × business ownership, M365/Dataverse context, human approvals → Power Automate; volume alone does not decide (MS, S-08/S-60/S-48b).
- Production-grade ALM/monitoring → only with Dataverse + Managed Environments on target environments → premium licences (MS, S-62/S-63/S-65).
- Availability > 99.9% or contractual cross-region RTO → no Microsoft commitment; integrations outside resilience scope (MS + UNKNOWN, S-12/S-37).
- Business-critical × automated tests → code-first Playwright; Test Engine deprecated (MS, S-70/S-67).
- External system of record × model-driven UX × audit, row security, offline or Pages → virtual tables insufficient (MS, S-56).
- Public/anonymous audience → Power Pages capacity per unique user per month; Web API not for third-party integration (MS, S-06/S-51/S-44).
- Required connector blocked by tenant DLP → design-time block, runtime quarantine (MS, S-16).

---

## 4. Findings

Ids PS-nn are stable across review and gates. Merged/retired ids are noted.

### 4.1 Application types and workload class

#### PS-01 — Power Platform targets line-of-business apps, process automation and Dataverse-backed external sites; the former "Power Apps patterns" catalogue is unreachable and apparently retired
- **Classification:** PATTERN
- **Evidence:** Developer overview: canvas/model-driven apps "shared with internal users … run in a browser or on a mobile device"; Power Automate "automate tasks and orchestrate activities across various services"; Power Pages "modern external-facing business websites" (S-20). Model-driven apps "especially well suited to process driven apps that are data dense and make it easy for users to move between related records … onboarding new employees, managing a sales process, or member relationships" (S-31). Power Automate planning source (2020-12-10): API-based automation preferred because "APIs are meant to be stable even as the application changes over time"; RPA "is susceptible to breaking when things change" (S-38b). Retrieval note: all `/power-apps/guidance/patterns/*` URLs redirected to the Plan designer page on 2026-09-02 and GitHub source returned 404 (S-33); the approval / asset / calculation / communication / inspection / project-management list survives only in search snippets.
- **Why it matters:** The positive-fit prior rests on positioning statements plus absence of constraint violations, not on a curated catalogue of successful patterns.
- **Decision impact:** STRONG for data-dense process apps and API-based automation of stable systems, phrased as "no documented constraint violated"; pattern names are heuristics.
- **Conditions:** Microsoft's current "what to build" entry point is the AI Plan designer (S-32).
- **Confidence:** HIGH (positioning statements) / MEDIUM (pattern list).
- **Sources:** S-20, S-31, S-38b, S-33, S-32.

#### PS-02 — Canvas vs model-driven: model-driven requires a Dataverse data model (external data via virtual tables, with limits) and provides responsive/accessible UI; canvas gives pixel control and connectors at the cost of consistency and ALM effort
- **Classification:** DECISION CRITERION
- **Evidence:** Comparison table (S-31): Data platform "Dataverse only" vs "Dataverse + many others using connectors"; UI control "Limited, predominantly customization" vs "Full control"; Migration "Simple" vs "Potentially complex given that the datasources might need to be updated"; Responsive "Automatically responsive" vs "Only responsive if designed in this way"; Accessibility "Built in" vs "Designed into the app". Custom pages bring canvas into model-driven (S-32). Virtual tables (PS-56).
- **Why it matters:** Data shape and UX need determine app type, which determines ALM, accessibility effort and licence (model-driven always premium).
- **Decision impact:** Relational, many related tables → model-driven. Task-focused, multi-source, mobile-first → canvas (CONDITIONAL on delegation).
- **Conditions:** Model-driven in a phone browser "isn't supported; use the Power Apps mobile app" (S-01).
- **Confidence:** HIGH.
- **Sources:** S-31, S-32, S-01, S-56.

#### PS-03 — Code apps: pro-developer SPA hosted and governed by Power Platform; Premium licence per end user; no Git integration, no Windows player, public asset endpoint
- **Classification:** PATTERN
- **Evidence:** "Build with popular frameworks (React, Vue, and others) while keeping full control over your UI and logic"; limitations: "don't support Power Platform Git integration", "aren't supported in Power Apps for Windows", no SharePoint forms integration, "compiled app assets are served from a publicly accessible endpoint that doesn't support IP-based restrictions"; "End users that run code apps need a Power Apps Premium license" (S-19, 2026-08-12). T3: "Choose code apps when you need a custom SPA frontend with stronger engineering control … should solve a real architectural problem" (S-42).
- **Why it matters:** Middle path before leaving the platform when UX or logic exceeds canvas.
- **Decision impact:** HYBRID candidate for bespoke internal UX over Dataverse/connectors. Not for anonymous, native mobile or IP-restricted scenarios.
- **Conditions:** Pro-dev team; features evolving (U-7).
- **Confidence:** HIGH facts / MEDIUM maturity.
- **Sources:** S-19, S-42.

#### PS-04 — Microsoft distinguishes productivity from mission-critical workloads and states the latter "demands deep platform knowledge" and "engineering rigor"
- **Classification:** DECISION CRITERION
- **Evidence:** Table (S-34): productivity "Built ad-hoc / Built by one / No tests / Development in production / Users monitor quality / Short lifecycle" vs mission-critical "Built to last / Built and maintained by a team / Automated tests / Exercises application lifecycle management / Monitored to improve / Long lifecycle". "Creating a reliable application at scale is complex. It demands deep platform knowledge … Operationalizing mission-critical workloads necessitates a high level of engineering rigor."
- **Why it matters:** Criticality is an axis independent of functional fit; it changes team, ALM, licences and testing.
- **Decision impact:** Business-critical → CONDITIONAL on the operating model (PS-33, PS-48, PS-53).
- **Confidence:** HIGH.
- **Sources:** S-34.

#### PS-05 — Microsoft's own tenant classification: personal productivity / team / enterprise; enterprise requires ALM, sandboxes and managed solutions in production
- **Classification:** RECOMMENDATION
- **Evidence:** "personal productivity, team collaboration, and enterprise development"; enterprise: "may store the most sensitive data, use more powerful connectors, and require more governance … ALM is required, with preproduction work happening in sandbox environments and only managed solutions allowed in production environments"; default environment sharing limit "A common limit is between 5 and 50 users" (S-35).
- **Decision impact:** Broad audience or sensitive data → enterprise class → CONDITIONAL on governance and licences.
- **Confidence:** HIGH.
- **Sources:** S-35.

### 4.2 Complexity

#### PS-06 — Large canvas apps degrade Studio and runtime; Microsoft documents partitioning (multiple apps, model-driven + custom pages)
- **Classification:** CONSTRAINT
- **Evidence:** "As apps become larger and more complex, Power Apps Studio needs to load and manage larger numbers of controls, formulas, and data sources, all with interdependencies that grow exponentially"; "nearly all apps with a long load time … have at least one formula of more than 256,000 characters"; "Some apps grow to thousands of controls and hundreds of data sources, which slows Power Apps Studio … can be split into smaller sections" (S-25, 2023-04). Community heuristics of 500 controls/app and 300/screen (S-46) are T4. The vendor statement "many successful implementations use more than 100 tables and over 50 screens" (S-26) is not used as evidence.
- **Decision impact:** Large functional scope → CONDITIONAL (partition) or prefer model-driven; not a reason alone to leave the platform.
- **Confidence:** HIGH (constraint) / MEDIUM (numbers).
- **Sources:** S-25, S-46.

#### PS-07 — Microsoft: complex business logic and large-scale transformation do not belong in cloud flows
- **Classification:** RECOMMENDATION
- **Evidence:** "Power Automate is an excellent tool for automating daily tasks. However, it isn't the best choice for large-scale data transformation or integration. Embedding complex business logic directly into cloud flows can lead to performance bottlenecks, make them hard to understand, debug, and maintain, and be cumbersome to scale." Alternatives: Dataverse plug-ins "for moving or processing a large number of Dataverse records"; custom connectors to "Azure Functions, Azure API Management, and Azure App Service … ensuring that the flow remains simple and focused on orchestration rather than on processing"; dataflows for ETL (S-22). Well-Architected: "if you put the business logic in the canvas app, you can't reuse it" (S-24).
- **Decision impact:** Complex/reusable/high-volume logic → HYBRID (flows orchestrate; plug-ins/Functions compute). Pure ETL → dataflows/Azure.
- **Confidence:** HIGH.
- **Sources:** S-22, S-24.

#### PS-08 — Power Fx lacks imperative loops and mutable local state; algorithm-heavy logic is documented friction (T3) with structural corroboration in Tier 1
- **Classification:** RISK
- **Evidence:** T3 (S-41): "The friction begins when logic requires sequence"; no `While`/`Repeat`/mutable `For`; Timer used as flow control "architecturally it is absurd"; "Power Apps is not failing. It is succeeding within a narrower complexity band than its marketing sometimes implies." T1: hidden-button `Select` workaround for imperative logic; named formulas "don't support imperative logic" (S-25). Power Fx overview: declarative/functional by design, "offers imperative logic when needed", user-defined functions "with more enhancements on the way" (S-40c).
- **Decision impact:** Iteration-to-convergence, recursion, mutable multi-step state → HYBRID (plug-in / Function) or CUSTOM. Simple validations and calculations → fine.
- **Confidence:** MEDIUM.
- **Sources:** S-41, S-25, S-40c.

#### PS-09 — Dataverse plug-ins: hard 2-minute execution limit; synchronous plug-ins delay users; heavy processing belongs in Azure ("no-cliffs")
- **Classification:** CONSTRAINT
- **Evidence:** "Plug-ins have only a short period of time (a hard limit) to complete their work"; "synchronous plug-ins must execute and complete quickly"; "the most performant way to apply custom business logic"; "require the special skills of a software developer" (S-27). Two-minute timeout for the whole message including synchronous plug-ins and custom API (S-28). "no-cliffs extension approach. You can start with SaaS, and then for the most challenging scenarios, extend into PaaS … handle heavy processing outside of your app" (S-30b).
- **Decision impact:** Long-running or compute-heavy logic → HYBRID (Functions/Durable, Service Bus, Logic Apps); asynchronous plug-ins cover many cases without Azure.
- **Confidence:** HIGH.
- **Sources:** S-27, S-28, S-30b.

### 4.3 User experience

#### PS-10 — Bespoke, brand-critical or consumer-grade UX: poor on model-driven, conditional on canvas (control library + PCF), Power Pages or custom web for public audiences
- **Classification:** TRADE-OFF
- **Evidence:** Model-driven UI "Limited, predominantly customization" (S-31); T3: "less flexibility for bespoke digital experiences" (S-42). PCF limits in canvas: "Microsoft Dataverse dependent APIs, including WebAPI, are not available for Power Apps canvas applications yet"; "Custom auth in code components is not supported" (S-29). Power Pages exposes HTML/CSS/Liquid (S-20). Canvas embeddable in third-party web sites but not "Third party native applications" (S-01).
- **Decision impact:** Internal task UX → STRONG/CONDITIONAL. Public consumer UX → Power Pages (CONDITIONAL) or CUSTOM. Design-system branding, animations, native gestures → code apps (PS-03) or CUSTOM.
- **Confidence:** HIGH facts / MEDIUM threshold.
- **Sources:** S-31, S-29, S-20, S-01, S-42.

#### PS-11 — Accessibility is built in for model-driven apps and is the maker's responsibility for canvas apps
- **Classification:** DECISION CRITERION
- **Evidence:** Model-driven "accessible and responsive automatically" (S-31). Canvas: contrast 4.5:1, `AccessibleLabel`, `TabIndex`, verified screen readers (JAWS, Narrator, NVDA, TalkBack, VoiceOver), Accessibility Checker, "unsupported design patterns" (S-36, 2022-09).
- **Decision impact:** Strict accessibility requirement → prefer model-driven; canvas CONDITIONAL on design discipline.
- **Confidence:** HIGH (model-driven) / MEDIUM (canvas page age).
- **Sources:** S-31, S-36.

#### PS-12 — No canvas embedding in native desktop/mobile clients; no iFrame embedding of model-driven apps; proxies unsupported; 180 s outbound request timeout
- **Classification:** CONSTRAINT
- **Evidence:** "Power Apps doesn't support the nested embedding of canvas apps in native desktop, mobile, or other non-browser clients." "Power Apps doesn't support embedding a model-driven app or page within an IFrame in another application." "Power Apps doesn't support running with a proxy enabled" (Zscaler, Blue Coat, Defender for Cloud Apps, McAfee cited). Outgoing request "Timeout 180 seconds, Retry attempts 4" (S-01, 2026-01).
- **Decision impact:** Native-embed requirement → CUSTOM. Proxied enterprise network → CONDITIONAL on network exceptions.
- **Confidence:** HIGH.
- **Sources:** S-01.

### 4.4 Data

#### PS-13 — Delegation: non-delegable queries silently operate on the first 500 (max 2,000) rows and can return wrong results
- **Classification:** CONSTRAINT
- **Evidence:** "When a query is nondelegable, Power Apps gets the first 500 records from the data source and then runs the actions in the query. You can increase this limit to 2,000 records." "the query might return incorrect results if the data source has more than 500 or 2,000 records." Delegable sources: Dataverse, SharePoint, SQL Server, Salesforce. Non-delegable: `If`, `*`/`/`/`Mod`, string functions, `GroupBy`, `Concat`, `FirstN/Last/LastN`, collections. Testing advice: "set this value to 1 … to make sure your app scales to large data sets" (S-02). SharePoint: complex types partly delegable; ID only `=`; `IsBlank`, `Not` not delegable (S-10). SQL: `Search` on text delegable; date filters fail via on-prem gateway; `char`/`nchar` pitfalls (S-40).
- **Why it matters:** The mechanism by which pilots pass and production fails.
- **Decision impact:** Any queried table > 2,000 rows → CONDITIONAL: Dataverse (broadest delegation) or SQL with delegable-only formulas; SharePoint weak for non-trivial queries; Excel/collections POOR beyond 2,000.
- **Confidence:** HIGH.
- **Sources:** S-02, S-10, S-40.

#### PS-14 — Data store choice: Dataverse for relational/secured business data (direct path, bypasses API Management); SharePoint for document-centric collaboration; SQL when the database exists (premium, gateway on-prem, connection-sharing risk); Excel is not a database
- **Classification:** DECISION CRITERION
- **Evidence:** "When you use Microsoft Dataverse as the data source, data requests go directly to the environment instance without passing through Azure API Management. So, it tends to be faster than other data sources." SharePoint: "Avoid too many dynamic lookup columns"; "Consider breaking up large lists … hundreds of thousands of records". Excel: "up to 2,000 records"; "Excel isn't a relational database system … if the app requires heavy transactions, it can adversely affect the performance" (S-11). Dataverse: relational/file/search/lake, role/row/column security, hierarchy, "service level agreement of 99.9% uptime", virtual tables (S-12). SQL: on-prem requires gateway (S-40); implicitly shared connections "the least secure"; secure implicit connections released January 2024 (S-43). T4 recurring reports: SharePoint 5,000 list view threshold and lookup-column delegation failures (S-45).
- **Decision impact:** Relational + security + audit → Dataverse (STRONG technically; premium). Documents → SharePoint (STRONG). Existing SQL → SQL connector (CONDITIONAL). Spreadsheet as system of record → POOR.
- **Conditions:** Max two lookup expand levels; 20 joined entities per query (S-02).
- **Confidence:** HIGH.
- **Sources:** S-11, S-12, S-10, S-40, S-43, S-45.

#### PS-15 — Dataverse capacity is an entitlement, not a technical limit; 250 MB DB / 2 GB file accrue per Power Apps Premium user; DB overage $48/GB/month; over-capacity blocks environment lifecycle operations and can lead to suspension
- **Classification:** TRADE-OFF
- **Evidence:** "There's no technical limit on the size of a Dataverse environment. The limits mentioned on this page are entitlement limits." Default environment includes 3 GB DB / 3 GB file / 1 GB log. Over-capacity blocks create/copy/restore; "Microsoft might suspend use of the online service" (S-13). Licensing Guide (Sept 2026): Premium accrues "Dataverse Database 250 MB", "Dataverse File 2 GB"; PAYG environments 1 GB DB + 1 GB file; overage "Database capacity 1 GB $48/month; File 1 GB $2.40/month; Log 1 GB $12/month" (S-44). Dataverse for Teams 2 GB / ≈1M rows, cannot buy more (S-14).
- **Decision impact:** Data-heavy requirements → CONDITIONAL on capacity budget; file vs database placement changes cost 20×; consider Azure storage via virtual tables/connectors as HYBRID.
- **Conditions:** Conflict C-1 on default tenant capacity (10 vs 20 GB).
- **Confidence:** HIGH (rules) / MEDIUM (default GB).
- **Sources:** S-13, S-44, S-14.

#### PS-16 — Dataverse for Teams is a bounded fit: Teams-only, 2 GB / ≈1M rows, no API, plug-ins, PCF, model-driven apps, auditing, field security, offline; one business unit
- **Classification:** CONSTRAINT
- **Evidence:** Comparison table: API access No; Plug-ins No; PCF No; model-driven No; Auditing No; Field-level security No; Business units One; Mobile offline No; "Maximum size 1 million rows or 2 GB"; "To use Dataverse for Teams outside of Teams, you must upgrade" (S-14). Premium connectors in Dataverse for Teams require standalone licences (S-06).
- **Decision impact:** Small team app in Teams with none of the excluded needs → STRONG on seeded licences; anything else → upgrade (premium, one-way).
- **Confidence:** HIGH.
- **Sources:** S-14, S-06.

#### PS-17 — Data residency: environment bound to region at creation; macro-region replication permitted; some metadata stored globally; exact datacentre not disclosed; India/Australia tenant constraints
- **Classification:** CONSTRAINT
- **Evidence:** "Environments can be created in different regions, and are bound to that geographic location … databases in the Microsoft Dataverse, apps, connections, gateways, and custom connectors" (S-15). "Microsoft might replicate your customer data to other datacenter regions within a macro region geography"; "Dataverse table and column names … replicated globally for support and troubleshooting purposes, but the content within those database tables remains stored in geo"; Power Pages "Website name and URL are stored globally"; Power Apps/Automate connected to Dynamics 365 "customer data may be sent outside of the designated region"; Brazil South may replicate to South Central US (S-47a, 2026-07). "Tax laws prevent you from creating a database for an environment in India and Australia, if your Microsoft Entra tenant is not in India and Australia"; "On-premises data gateways aren't available in the India region" (S-15). Microsoft "doesn't disclose the exact details of where your data resides" (S-37).
- **Decision impact:** Residency requirement → CONDITIONAL on region and environment strategy; metadata-in-geo or exact-location requirement → POOR.
- **Confidence:** HIGH.
- **Sources:** S-15, S-47a, S-37.

### 4.5 Transactions, throughput and concurrency

#### PS-18 — Dataverse service protection limits: 6,000 requests, 20 minutes execution time, 52 concurrent per user per 5-minute window per web server; interactive users rarely hit them, integrations and portals do
- **Classification:** CONSTRAINT
- **Evidence:** "These limits don't affect normal users of interactive clients. They affect only client applications that perform an extraordinary volume of API requests." Defaults per web server: 6,000 / 300 s; 1,200 s execution; 52 concurrent. Portals send anonymous traffic "through a service principal account … can hit service protection API limits". Plug-in operations don't count as requests but their execution time does. Batch is "not a valid strategy to bypass entitlement limits". "Move towards real-time integration" instead of nightly bulk (S-03). Dataverse connector: "API calls per connection 6000 / 300 seconds" (S-45b).
- **Decision impact:** High-throughput integration → CONDITIONAL (429 handling, parallelism, pacing) or HYBRID (Azure buffering); very high sustained writes → CUSTOM store with Dataverse as reference data.
- **Conditions:** Web-server count per environment not published (U-3).
- **Confidence:** HIGH.
- **Sources:** S-03, S-45b.

#### PS-19 — Daily Power Platform request entitlements are per licence: 40,000 (Premium/D365), 6,000 (M365 seeded, per app, PAYG), 250,000 (Process/per flow, stackable ×10, shareable across 25 flows); background flows consume the owner's limit; retries and pagination count; enforcement is in a transition period
- **Classification:** DECISION CRITERION
- **Evidence:** Table (S-04, 2026-08-14): 40,000 / 6,000 / 250,000; non-licensed pool "25,000 base requests with no per-license accrual"; "automated and scheduled flows that run in the background always use the limits of the owner"; "Both successful and failed actions count … Retries and requests from pagination also count"; enforcement "won't happen until six months after … reporting is generally available". Process: "Up to 10 Process licenses can be stacked on a single cloud flow … Alternatively, you can assign a Process license to a flow group to share 250,000 actions per day across up to 25 cloud flows" (S-48b, 2026-07-20).
- **Decision impact:** Requests/day per owner above entitlement → CONDITIONAL (Process/PAYG); above 2.5M/day per flow or where latency guarantees matter → HYBRID/Logic Apps.
- **Conditions:** "Build your cloud flows based on official limits"; U-1.
- **Confidence:** HIGH (documented) / MEDIUM (enforcement timing).
- **Sources:** S-04, S-05, S-48b.

#### PS-20 — No documented concurrent-user ceiling for canvas or model-driven apps; capacity is governed by data-source and request limits
- **Classification:** FACT (absence)
- **Evidence:** No per-app maximum found in limits pages (S-01, S-11). Mobile platforms differ in concurrent network requests (S-11). Power Pages "Scaling of these application servers is done automatically based on the Power Pages licensing capacity assigned" (S-17).
- **Decision impact:** User count alone never yields POOR; translate into requests/day, requests/5 min, data volume and delegation.
- **Confidence:** MEDIUM (absence).
- **Sources:** S-01, S-11, S-17.

#### PS-45 — Atomicity exists only inside Dataverse (change sets, ExecuteTransaction, synchronous plug-in pipeline); canvas `Patch`, cross-connector flows and elastic tables are not transactional; Microsoft's cross-service remedy is the compensating-transaction pattern
- **Classification:** DECISION CRITERION
- **Evidence:** Dataverse Web API: "Batch requests can contain up to 1,000 individual requests … When multiple operations are contained in a change set, all the operations are considered atomic … if any one of the operations fails, the batch request rolls back any completed operations"; `GET` not allowed in change sets (S-52). SDK `ExecuteTransactionRequest`: "Should any one of the requests fail and the transaction is rolled back, any data changes completed during the transaction are undone"; cannot nest `ExecuteMultiple` (S-53). Event pipeline: PreOperation/PostOperation "within the database transaction"; "An exception thrown by your code at any synchronous stage within the database transaction causes the entire transaction to roll back"; asynchronous steps "run outside of the database transaction" (S-54). Power Automate Dataverse action: "Perform a changeset request … perform a group of Microsoft Dataverse connector operations as a single transaction. If one of the operations fails, all the successful actions are rolled back" (S-45b); restrictions (excerpt): only "Add a new row, Delete a row, and Update a row"; "The Apply to each action isn't supported in a changeset"; "You can't reference an output of a previous action in the changeset scope" (S-55). No transactional construct exists across different connectors. Canvas `Patch`: per-record errors via `IfError`/`Errors`; no atomicity statement across records/tables (S-56b). Elastic tables: "don't support multi-record transactions … grouping requests in a single database transaction … Currently, these operations succeed but aren't atomic" (S-57). Azure Architecture Center: compensating transactions for operations that "can't rely on atomic transactions"; "It's not easy to generalize compensation logic. A compensating transaction is application specific"; not suitable when "The system can't tolerate temporary inconsistency … Use strong consistency mechanisms or atomic transactions across all steps instead" (S-58).
- **Why it matters:** Ledger-like, stock, allocation or payment-like processes need all-or-nothing semantics. Available only when every write is a Dataverse standard-table operation in one change set or plug-in; anything touching SharePoint, SQL connectors, external APIs or elastic tables is eventually consistent by construction.
- **Decision impact:** Within Dataverse → CONDITIONAL (design with change sets / plug-in; canvas must call a custom API or flow changeset rather than sequential `Patch`). Across connectors/systems → POOR for low-code alone → HYBRID (orchestrator with idempotent compensation) or CUSTOM. On elastic tables → POOR.
- **Conditions:** Batch ≤ 1,000 operations; 2-minute plug-in cap (PS-09); S-55 restrictions to be confirmed from the fetched page (gate condition 2).
- **Confidence:** HIGH (Dataverse, elastic, pattern) / MEDIUM (flow changeset restrictions, excerpt-level).
- **Sources:** S-52, S-53, S-54, S-45b, S-55, S-56b, S-57, S-58.

#### PS-46 — Concurrent edits: Dataverse optimistic concurrency is available only through SDK/Web API; canvas `Patch` on Dataverse surfaces a server-conflict error the maker must handle; behaviour on SharePoint/SQL not established
- **Classification:** CONSTRAINT
- **Evidence:** "Optimistic concurrency is supported on all out-of-box tables enabled for offline sync and all custom tables … You can only set optimistic concurrency behavior through an SDK API call. There's currently no setting for it in a form of the web application"; errors `ConcurrencyVersionMismatch`, `ConcurrencyVersionNotProvided` (S-59, 2026-08-27). `Patch`: "'Conflicts exist with changes on the server': This error occurs when another user or process modifies the same record between the time your app reads the record and writes the change. Refresh the data source … and retry" (S-56b).
- **Decision impact:** High-contention records → CONDITIONAL (Dataverse + explicit conflict handling); on other stores → UNKNOWN (U-13) → test.
- **Confidence:** HIGH (Dataverse) / UNKNOWN (SharePoint/SQL).
- **Sources:** S-59, S-56b.

#### PS-57 — Elastic tables give Cosmos-DB-backed horizontal scale inside Dataverse for spiky/high-volume data, at the cost of transactions, deep insert and cross-session consistency
- **Classification:** TRADE-OFF
- **Evidence:** "Use elastic tables … You must handle a high volume of read and write requests"; "Use standard tables … Your application requires strong data consistency … transactional capability across tables or during plug-in execution … complex joins"; "Each logical partition can store 20 gigabytes (GB)"; session-token consistency; TTL; "Elastic tables don't support multi-record transactions"; known issues "should be addressed before this feature becomes generally available" (S-57, 2026-08-04).
- **Decision impact:** IoT/telemetry/log-style data → HYBRID-within-platform (elastic + standard tables); transactional high volume → HYBRID/CUSTOM.
- **Conditions:** Maturity caveat (U-16).
- **Confidence:** HIGH facts / MEDIUM maturity.
- **Sources:** S-57.

### 4.6 Process characteristics

#### PS-21 — Automation candidates per Microsoft: repetitive, rule-based, frequent, cross-system re-keying, runnable without humans; API-based automation preferred over UI automation for stability
- **Classification:** DECISION CRITERION
- **Evidence:** Planning source (2020-12-10): DPA via APIs "meant to be stable even as the application changes over time"; RPA "susceptible to breaking when things change, such as when updates are applied to a local computer's environment or the layout of an application's screens" (S-38b). Methods page (2022-03-16): connector "Easiest"; custom connector "resilient to system changes"; HTTP for one-offs; browser/desktop automation for UI-only; "In complex automation scenarios, you can combine all these methods"; the document does not state when Power Automate is not the right tool (S-38c). The repetitive / frequent / re-keying / human-independent list is excerpt-level (S-38).
- **Decision impact:** Stable API available → STRONG (cloud flows). UI-only legacy → CONDITIONAL (RPA fragility, licences). Judgement-heavy, exception-dominated → CONDITIONAL (partial automation).
- **Confidence:** MEDIUM.
- **Sources:** S-38, S-38b, S-38c.

#### PS-22 — Human-in-the-loop approvals are a strong fit up to 30 days; pending steps time out at 30 days
- **Classification:** CONSTRAINT
- **Evidence:** "Run duration 30 days … includes flows with pending steps like approvals. After 30 days, any pending steps time out"; run retention 30 days (S-05). Well-Architected: "use Power Automate Approvals if human interaction is required, but choose to use a Dataverse plugin … when human interaction isn't required" (S-24).
- **Decision impact:** Approvals/escalations → STRONG. Waits > 30 days → CONDITIONAL (persist state in data, re-trigger).
- **Confidence:** HIGH.
- **Sources:** S-05, S-24.

#### PS-23 — Cloud flow hard limits: 500 actions/flow, nesting 8, apply-to-each 100,000 items (5,000 Low profile), loop concurrency ≤ 50, 120 s synchronous request, 100 MB message (1 GB chunked), content throughput 10 GB/day (High) or 200 MB/day (Low); throttled or erroring flows turned off after 14 days; inactive non-premium flows after 90 days
- **Classification:** CONSTRAINT
- **Evidence (S-05, 2026-07-17):** "Actions per workflow 500"; "Allowed nesting depth for actions 8"; "Apply to each array item 5,000 for Low, 100,000 for all others"; "Apply to each concurrency 1 is the default … between 1 and 50"; "Until iterations Default 60 Maximum 5,000"; "Outbound synchronous request 120 seconds"; "Inbound request 120 seconds"; "Message size 100 MB … with chunking 1 GB"; "Content throughput per 24 hours 200 MB for Low; 2 GB for Medium; 10 GB for High"; "Consistently throttled flows 14 days"; "Flows with errors 14 days"; "Flows without trigger activity 90 days … Flows owned by users with premium licenses or assigned capacity licenses … aren't subject to this suspension". Profiles: Low = M365, per-app, trials; High = Process/per-flow.
- **Decision impact:** Any hard limit exceeded → POOR for cloud flows on that path → HYBRID/Logic Apps/Functions.
- **Confidence:** HIGH.
- **Sources:** S-05.

#### PS-24 — Power Automate vs Logic Apps Standard is a trade-off on ownership, network runtime, dedicated compute and code-first tooling, not on raw volume; the most-cited comparison is authored by the Logic Apps product group and several of its cells are contradicted by Power Platform documentation
- **Classification:** TRADE-OFF
- **Evidence:** Vendor-side comparison (S-09, 2025-07): Power Automate "Small to medium scale workflows … limited by shared resources"; "Limited versioning"; "Basic monitoring through the Power Automate portal"; "In Power Automate, RBAC works at the user level … In Azure Logic Apps, RBAC works at the resource level … if the workflow creator leaves, you don't lose access". Neutral Azure guidance (S-08, 2026-03): "Power Automate empowers business users, office workers, and citizen developers to build simple integrations … Azure Logic Apps supports integrations ranging from little-to-no-code scenarios to more advanced, codeful, and complex workflows. Examples include B2B processes"; Architecture Center: both "well-suited for trigger-based or time-based tasks" and "built on the same underlying technology" (S-60). Power Platform counter-evidence: Process licence stacking (S-48b); pipelines with pre-validation, approvals, immutable artefacts and rollback (S-62); native Git integration (S-63); canvas source files (S-64); App Insights export for flows (S-65); service-principal-owned flows with Process licence (S-04). T3 community comparison: differences are mostly licensing model, audience, DLP vs Azure Policy (S-39).
- **Why it matters:** Recommending Azure because "Power Automate has limited versioning/monitoring" is not supportable; recommending it for dedicated compute, VNET-native runtime, resource-level RBAC, local debugging, B2B/EDI, or an Azure-native team is.
- **Decision impact:** Logic Apps Standard when IT owns the integration estate, private-network runtime is mandatory, latency/throughput needs dedicated compute, code-first CI/CD with local debugging is required, or B2B/EDI. Power Automate when business ownership, M365/Dataverse context, human tasks, volume within Process licences, Managed Environments acceptable. Volume alone is CONDITIONAL.
- **Conditions:** Power Platform ALM/monitoring capabilities require Managed Environments/premium for target environments (PS-48).
- **Confidence:** HIGH.
- **Sources:** S-09, S-08, S-60, S-48b, S-62, S-63, S-64, S-65, S-04, S-39.

#### PS-25 — Documented flow anti-patterns: nested for-each loops, self-triggering loops, large transformations in flows, per-record loops for thousands of updates; remedies are OData expand, trigger conditions, dataflows, batch/bulk APIs
- **Classification:** ANTI-PATTERN
- **Evidence (S-23):** "Avoid nested For each loops … They can exceed limits and quotas." "Avoid infinite loops." "Avoid large numbers of data transformation operations … use an ETL dataflow." "If you need to create or update thousands of records … don't use a For each loop to process each record sequentially" → batch (`$batch`), bulk (`CreateMultiple`), parallelism up to 50. T4: variables lock in loops; default concurrency triggers connector throttling; Select/Filter array over loops (S-47).
- **Decision impact:** "Process every row of X nightly" → dataflows/Azure, not flows.
- **Confidence:** HIGH.
- **Sources:** S-23, S-47.

### 4.7 Integration

#### PS-26 — Connectors wrap REST APIs; premium/custom connectors and on-premises data require premium licences and (on-prem) the data gateway; custom connectors capped at 500 requests/min per connection and 50 per user
- **Classification:** CONSTRAINT
- **Evidence:** "A custom connector is a wrapper around a REST API and can be created using tools like Azure Functions and Azure API Management" (S-20). Licensing Guide: seeded M365 includes "Standard connectors" only; "Premium and custom connectors" and "On premises and cloud services data transfer" require Premium / per app / D365 (S-44). "Number of custom connectors 50 per user"; "500 requests per minute per connection" (S-05). T3 (custom-dev vendor, bias noted): gateway "adds latency, complexity, and another dependency" (S-48). Connector counts (1,400+/1,500+/~150/200) are marketing figures and not used as evidence.
- **Decision impact:** Cloud SaaS with standard connector → STRONG. Custom REST/on-prem → CONDITIONAL. No API (UI-only legacy) → RPA (fragile) or CUSTOM.
- **Conditions:** SOAP via custom connectors not verified (U-10).
- **Confidence:** HIGH (T1) / MEDIUM (T3 claims).
- **Sources:** S-20, S-44, S-05, S-48.

#### PS-27 — Event-driven, decoupled integration is a documented pattern: Dataverse publishes to Azure Service Bus, Event Hubs or webhooks from plug-in steps (asynchronous recommended), 192 KB payload cap; not available in Dataverse for Teams
- **Classification:** PATTERN
- **Evidence:** "The Azure Service Bus provides a secure and reliable communication channel between Dataverse runtime data and external cloud-based line-of-business (LOB) applications"; contracts queue, one-way, two-way, REST, topic, Event Hubs; "register the plug-in to run asynchronously for best system performance"; "When the size of the entire HTTP payload exceeds 192 KB … an error occurs and the message isn't sent"; exponential retry (S-21). Well-Architected: queue-based processing "can improve performance and reliability. However, these methods don't give users immediate feedback" (S-24). Not in Dataverse for Teams (S-14).
- **Decision impact:** Event fan-out, guaranteed delivery, multi-subscriber → HYBRID (Service Bus/Event Grid); flows alone CONDITIONAL.
- **Confidence:** HIGH.
- **Sources:** S-21, S-24, S-14.

#### PS-28 — Synchronous windows are short: canvas outbound 180 s; flow synchronous inbound/outbound 120 s
- **Classification:** CONSTRAINT
- **Evidence:** "Timeout 180 seconds, Retry attempts 4" (S-01). "Outbound synchronous request 120 seconds … For longer-running operations, use an asynchronous polling pattern"; response actions "always return a response within this limit" (S-05).
- **Decision impact:** Sync latency > ~2 min → CONDITIONAL (async redesign) or HYBRID (Durable Functions / Logic Apps).
- **Confidence:** HIGH.
- **Sources:** S-01, S-05.

#### PS-29 — Tenant DLP policies can make a design infeasible: blocked connectors fail at design time and existing apps/flows are suspended or quarantined at runtime (up to 24 h)
- **Classification:** RISK
- **Evidence:** "If a data policy blocks the use of MSN Weather connector, a maker can't save their flow or app that uses this connector." "If a violation occurs, put the app, flow, or chatbot in to a suspended or quarantine state so that it can't operate." "the latency for full enforcement is 24 hours" (S-16).
- **Decision impact:** Required connector blocked → CONDITIONAL on policy exception; otherwise POOR in that tenant.
- **Confidence:** HIGH.
- **Sources:** S-16.

### 4.8 Scalability and performance

#### PS-30 — Well-Architected frames fit as meeting performance targets "within the throughput and request limits of the platform", preferring platform features and weighing team skills; some data workloads need other databases
- **Classification:** RECOMMENDATION
- **Evidence:** "A performant workload is able to handle changes in load without compromising the user experience or exceeding throughput and request limits of the platform" (S-26b). "Understand service limits … avoid issues such as resource contention, performance degradation, or unexpected service interruptions." "Only develop custom code when service features aren't sufficient." Tradeoff: "a Dataverse plugin might fit your performance needs better, but your workload team might only be familiar with Power Automate cloud flows." "if your workload requires high-performance real-time data processing, you might choose a database system optimized for fast data ingestion and low latency" (S-24).
- **Decision impact:** Targets not met within documented limits → HYBRID/CUSTOM for that component. Performance fit must otherwise be validated by test (no latency/load evidence in this corpus, R-24).
- **Confidence:** HIGH (guidance) / UNKNOWN (empirical performance).
- **Sources:** S-24, S-26b.

### 4.9 Security

#### PS-31 — Dataverse provides the enterprise security model (roles, business units, row sharing, column security, hierarchy, encryption, certifications); SharePoint/SQL-connector designs inherit weaker or riskier models
- **Classification:** FACT
- **Evidence:** "role-based security … security roles can be associated directly with users, or … teams and business units"; "column-level security feature"; "manager hierarchy and the position hierarchy"; "Encryption of data, at rest and in transit"; compliance via Trust Center (S-12). Dataverse for Teams lacks auditing, field security, hierarchy, record sharing (S-14). SQL via canvas: implicitly shared connections "the least secure … even the name of the database and other details can be discovered"; secure implicit connections January 2024 (S-43). SharePoint security "primarily revolves around securing sites, lists, libraries" (S-49).
- **Decision impact:** Row/column authorisation, separation of duties, auditability → Dataverse (STRONG technically; premium). Same on SharePoint → POOR.
- **Conditions:** Security design remains the customer's responsibility (S-30).
- **Confidence:** HIGH.
- **Sources:** S-12, S-14, S-43, S-49, S-30.

#### PS-32 — Network isolation: Logic Apps Standard documents VNET integration and private endpoints; Power Platform has since added VNet support, IP firewall, customer-managed keys and Lockbox as Managed Environment features (premium); functional parity unverified
- **Classification:** TRADE-OFF (version-sensitive)
- **Evidence:** "Azure Logic Apps (Standard) provides security features that differ from the capabilities in Power Automate … Virtual network integration and private endpoints" (S-09, 2025-07). Managed environments (2026-02): "IP Firewall", "Customer Managed Key (CMK)", "Lockbox", "Virtual Network support for Power Platform", "Conditional access on individual apps"; entitlement with standalone licences (S-18). Code apps: assets on a public endpoint (S-19).
- **Decision impact:** Private-network-only → CONDITIONAL (Managed Environments + VNet) or CUSTOM/OTHER (Logic Apps Standard).
- **Conditions:** C-6, U-11.
- **Confidence:** HIGH (facts) / MEDIUM (equivalence).
- **Sources:** S-09, S-18, S-19.

### 4.10 Governance, ALM and lifecycle

#### PS-33 — Enterprise governance (sharing limits, pipelines, solution checker, usage insights, extended backups, DR) is packaged as Managed Environments, which require every active user to hold a standalone licence or PAYG meter
- **Classification:** CONSTRAINT
- **Evidence:** Feature list (S-18). Licensing Guide: "Once enabled, all active usage in the environment will require one of these standalone licenses or pay-as-you-go meters"; "'Standalone licenses' … does not include the limited Power Apps, Power Automate and Power Pages use rights that come with select Dynamics 365 and Microsoft 365 licenses" (S-44). Pipelines: "Licenses granting premium use rights are required for all managed environments" (S-62).
- **Decision impact:** Business-critical + broad audience on seeded licences → CONDITIONAL (budget premium) — otherwise runs outside Microsoft's recommended posture (RISK).
- **Confidence:** HIGH.
- **Sources:** S-18, S-44, S-62.

#### PS-34 — Ownership and lifecycle: Power Automate access is user-level (leaver risk); non-premium flows may be turned off after 90 days inactivity; mitigations are solutions, service-principal ownership and Process licence
- **Classification:** RISK
- **Evidence:** "In Azure Logic Apps, RBAC works at the resource level … if the workflow creator leaves, you don't lose access … In Power Automate, RBAC works at the user level" (S-09). "Flows without trigger activity 90 days … might be turned off. Flows owned by users with premium licenses or assigned capacity licenses … aren't subject to this suspension" (S-05). Service-principal-owned flows with Process licence use the flow's own entitlement (S-04); Process "maintain a flow without each co-owner needing a user license" (S-48b).
- **Decision impact:** IT-owned production automation → CONDITIONAL (solutions, service principal, Process licence) or Logic Apps.
- **Confidence:** HIGH.
- **Sources:** S-09, S-05, S-04, S-48b.

#### PS-48 — Power Platform has a documented production ALM stack (solutions, pipelines with pre-validation, approvals, artefact immutability and rollback, native Git integration, human-readable canvas source, Application Insights export) — all gated on Dataverse and Managed Environments
- **Classification:** FACT
- **Evidence:** "Solutions are the mechanism for implementing ALM … Source control should be your source of truth … all environments that participate in ALM must include a Dataverse database" (S-61). Pipelines: "Solution deployments are prevalidated against the target environment"; "Connections and environment variables are provided upfront and validated"; "the system doesn't re-export a solution for deployments to subsequent stages … prevents any tampering"; rollback "If the pipeline setting is enabled, you can redeploy previous solution versions"; "Pipelines … don't contain data stored within Dataverse tables"; "Can pipelines deploy to a different tenant? No"; "The current implementation uses a single development environment for a given solution"; "All other environments used in pipelines must be enabled as managed environments"; "Starting February 2026, Microsoft will start enabling managed environments for any pipeline target environments" (S-62). Git integration: "Use Git integration with developer environments, not in your test or production environments"; code-first objects should come from a build process, not committed binaries (S-63). Canvas source: "The generated canvas app YAML code is read-only and can't be modified … External editing, merging, and conflict resolution is supported only in Power Platform Git Integration"; "The YAML schema is in active development" (S-64). Flow telemetry: Requests/Dependencies tables, alert rules; "supported for managed environments only"; "not 100% lossless"; not available in GCC/GCC High/DoD (S-65).
- **Why it matters:** Rebuts "limited versioning / basic monitoring" as a reason to leave the platform, while exposing the real constraints: Dataverse dependency, premium licensing, single dev environment per solution, read-only canvas source outside Git integration, no data migration in solutions, no cross-tenant pipelines.
- **Decision impact:** IT-grade ALM requirement → CONDITIONAL (Managed Environments + Dataverse + pipelines/Git). Cross-tenant deployment or multi-developer isolated environments per solution → Azure DevOps/GitHub extensions.
- **Confidence:** HIGH.
- **Sources:** S-61, S-62, S-63, S-64, S-65.

#### PS-50 — Platform change cadence is mandatory and fast: two release waves per year that "can't be postponed", weekly service updates, and a rolling deprecation list with notice periods from months to years
- **Classification:** RISK
- **Evidence:** "Each release wave becomes generally available twice a year. Your environments automatically receive these mandatory updates." "A release wave is a mandatory update and can't be postponed." Regional windows (e.g., Europe April 10–13 and October 9–12, 2026) (S-66). Deprecation policy: "'Deprecated' means we intend to remove the feature … fully supported until it's officially removed. This deprecation notification can span a few months or years." 2025–26 deprecations include Cards for Power Apps, Test Engine (April 2026), Power Automate mobile app (Aug 2026), classic look for model-driven apps (April 2026), Editable/Read-Only Grid controls (March 2026), BYOK, SQL connector V1 actions (S-67). Power Fx forward compatibility: "Every saved Power Fx document includes a language version stamp … 'back compat converter' … automatically rewrites the formula" (S-40c).
- **Decision impact:** Frozen/validated behaviour required (e.g., regulated revalidation per change) → RISK → CONDITIONAL (budget wave regression, early-access testing). Lifetime > 5 years → deprecation exposure in TCO.
- **Confidence:** HIGH.
- **Sources:** S-66, S-67, S-40c.

#### PS-51 — Portability: data and .NET plug-in code are portable; canvas UI, Power Fx formulas and flow definitions are not re-hostable outside Power Platform (Power Fx open-sourcing "in the process"); exit means rebuilding UI and orchestration
- **Classification:** RISK
- **Evidence:** "Microsoft will make Power Fx available as open-source software. It's currently integrated into canvas apps, and Microsoft is in the process of extracting it from Power Apps … and as open source" (S-40c, 2026-08). `.pa.yaml` read-only, "schema is in active development" (S-64). Solutions move components between Dataverse environments; "Can pipelines deploy to a different tenant? No" (S-62). Data exit paths: TDS endpoint ports 1433/5558 (S-68), Synapse Link, Data Export Service, events to Service Bus (S-14). Flows: JSON definitions with a Microsoft-documented migration path to Logic Apps Standard only (S-09).
- **Decision impact:** Vendor-neutral / re-hostable requirement → RISK (HIGH) → prefer CUSTOM, or keep logic in portable layers (Dataverse data + .NET/Azure) and treat Power Apps as replaceable UI.
- **Confidence:** HIGH (facts) / MEDIUM (exit-cost judgement).
- **Sources:** S-40c, S-64, S-62, S-68, S-14, S-09.

### 4.11 Offline

#### PS-35 — Offline only in native mobile players (iOS/Android/Windows), never in a browser; Dataverse offline-first built in (3M rows, automatic conflicts); non-Dataverse apps limited to LoadData/SaveData (30–70 MB, manual conflicts); model-driven offline has feature gaps
- **Classification:** CONSTRAINT
- **Evidence:** "Canvas apps running in web browsers can't run offline, even when using a web browser on a mobile device." Non-Dataverse: "LoadData and SaveData … You'll generally have 30-70 megabytes of available memory … don't automatically resolve merge conflicts" (S-07, 2024-03). Built-in offline: "Data size limit … 3 million rows", "Conflict resolution Automatic", "Supported Power Fx functions Partial" (S-07b, 2024-06). Model-driven offline limits: "Field level security and field sharing aren't supported in Mobile offline mode"; personal views unsupported; N:N read-only; max 15 relationships per table in profile; Dataverse search unsupported offline; duplicate detection unsupported (S-07c, 2024-09). T3 (custom-dev vendor): "offline-first mobile applications with sophisticated sync logic" as a structural limit (S-48).
- **Decision impact:** Offline on managed mobile devices with Dataverse → STRONG. Browser/kiosk offline or SharePoint/SQL data → POOR. Custom sync semantics beyond automatic → CUSTOM.
- **Confidence:** HIGH (constraint) / MEDIUM (page age, numbers).
- **Sources:** S-07, S-07b, S-07c, S-48.

### 4.12 External users and identity

#### PS-36 — External users are a licensing and architecture fork: Entra B2B guests run canvas apps only with cross-tenant-recognised licences (per-app plans are not); anonymous or consumer-identity access requires Power Pages over Dataverse-fronted data with capacity licensing; multiplexing does not reduce licences; Pages Web API is not for third-party integration
- **Classification:** DECISION CRITERION
- **Evidence:** "the guest user must have a license with Power Apps use rights that matches the capability of the app"; "Power Apps per app plans are scoped to apps in a specific environment, so they can't be recognized across tenants"; guests need "a standalone browser session"; Pages vs canvas: "Browser-only experience / Allows anonymous and authenticated access / Dataverse" vs "Browser and mobile apps / Requires authentication via Microsoft Entra ID / … connectors" (S-42b). Pages licensing: authenticated users per website/month (packs of 100), anonymous (packs of 500); minimum anonymous 200 per environment (S-06, S-50 excerpt). Web API: "isn't optimized for third-party services or application integration"; anonymous Web API calls count toward anonymous capacity (S-51). Licensing Guide: "Multiplexing does not reduce the number of subscription licenses of any type required … Any user or device that inputs data into, queries, views data from or otherwise accesses Power Apps, Power Automate and Power Pages apps, directly or indirectly must be properly licensed"; External Users defined as non-employees / contractors under 30 h/week / not onsite daily (S-44). Virtual tables cannot enable "Power Pages solutions" (S-56).
- **Decision impact:** Known partner users via B2B → CONDITIONAL. Public/anonymous → Power Pages (CONDITIONAL on Dataverse-fronted data and capacity budget) or CUSTOM web. Public API surface → CUSTOM.
- **Conditions:** Pages traffic ceilings not published (U-4).
- **Confidence:** HIGH.
- **Sources:** S-42b, S-06, S-50, S-51, S-44, S-56.

#### PS-60 — Identity prerequisite: internal use requires Microsoft Entra work or school accounts; sovereign clouds bind to specific Entra instances; personal Microsoft accounts removed from Power Automate; frontline/shared-device licensing not researched
- **Classification:** CONSTRAINT
- **Evidence:** Power Automate Free "included at no cost for work or school accounts in a Microsoft Entra tenant" (S-48b). GCC High "enables and requires the customer to use Microsoft Entra Government for customer identities, in contrast to GCC which uses Public Microsoft Entra ID" (S-47b). Deprecation: "Personal Microsoft service accounts in Power Automate — May 27, 2025 … July 26, 2025" (S-67). Guests via B2B (S-42b).
- **Decision impact:** Non-Entra population → CONDITIONAL (B2B, Pages identities); frontline shared-device licensing → UNKNOWN (U-14).
- **Confidence:** MEDIUM (partial coverage).
- **Sources:** S-48b, S-47b, S-67, S-42b.

### 4.13 Operations, reliability and deployment model

#### PS-37 — Reliability: Dataverse 99.9% SLA statement; availability-zone architecture targets near-zero RPO and RTO < 5 min but is rolling out; cross-region DR is self-service with no published RTO; integrations are outside the resilience commitment
- **Classification:** CONSTRAINT
- **Evidence:** "Dataverse … offers a service level agreement of 99.9% uptime" (S-12). BCDR (2026-08-20): "The recovery point objective is near zero, and the recovery time objective is less than five minutes"; "A limited number of customers in certain regions are transitioning to the improved architecture. Whether the region transitioned or is transitioning, the service always keeps a backup of environment data in more than one data center"; "This capability is available only for production environments"; "Microsoft doesn't publish a cross-region RTO commitment"; "when Power Platform solutions connect to external systems … fall outside the scope of Power Platform's resiliency commitments"; flows under self-service DR have "known performance limitations"; backups 7 days, 28 for managed production (S-37, S-34). Licensing Guide: self-service DR "must be linked to a pay-as-you-go billing plan" (S-44) vs BCDR "no longer a mandatory requirement" (C-2).
- **Decision impact:** ≤ 99.9% with in-region HA → STRONG once the tenant's region is confirmed on the AZ architecture; otherwise CONDITIONAL. Contractual cross-region RTO or > 99.9% → POOR (INF).
- **Conditions:** U-12b region status; SLA document unread (PS-52).
- **Confidence:** HIGH (statements) / MEDIUM (applicability to a tenant).
- **Sources:** S-12, S-37, S-34, S-44.

#### PS-47 — Power Platform is cloud-only: it "requires connectivity to the internet", stores customer data in Azure datacenters, and offers no on-premises or customer-hosted deployment; sovereign options are US Government (eligibility-gated) and China 21Vianet, both with feature-parity exceptions
- **Classification:** CONSTRAINT
- **Evidence:** "Microsoft Power Platform requires connectivity to the internet. The endpoints listed in this article should be reachable" (S-68, 2026-08). "Microsoft Dynamics 365 and Power Platform store customer data in Microsoft Azure datacenters located in various geographic regions around the world" (S-47a). Sandbox plug-ins reaching external services need `PowerPlatformPlex` ranges (S-68). US Government: "available to (1) US federal, state, local, tribal, and territorial government entities and (2) other entities that handle data that's subject to government regulations … subject to validation of eligibility"; "There are exceptions to the principle of maintaining product functional parity" (S-47b). China: "physically separated environment of cloud services … operated … by a local operator … subject to Chinese laws"; parity "exceptions … affected by dependent service availability, market priorities, or compliance regulations" (S-47c). No Microsoft page describes on-premises or private-hosted Power Platform; the on-premises data gateway only bridges cloud-hosted apps to on-premises data (S-10, S-48b).
- **Decision impact:** Disconnected, customer-hosted or isolated OT-network deployment → POOR (MS). Regulated US public-sector or data-in-China → CONDITIONAL on eligibility and parity. Otherwise connectivity prerequisites (endpoints, proxies — PS-12) must be validated.
- **Conditions:** Parity documents are PDFs not read in this research.
- **Confidence:** HIGH.
- **Sources:** S-68, S-47a, S-47b, S-47c, S-10, S-48b.

#### PS-52 — Per-service SLA figures not verified: the Microsoft Online Services SLA is published as downloadable documents behind an index; only the Dataverse 99.9% statement is in Tier 1 web documentation
- **Classification:** UNKNOWN
- **Evidence:** Two attempts (licensing docs index; Product Terms page) returned indexes; Product Terms displayed "ServiceLevelAgreements is not available on this date" (S-69). Licensing Guide: Power Automate desktop free application "with no SLA or Microsoft support" (S-44 footnote 9).
- **Decision impact:** Any availability commitment beyond "Dataverse 99.9%" and any connector/third-party exclusion is UNKNOWN until the September 2026 SLA document is read (U-12; gate condition 2).
- **Sources:** S-69, S-44.

#### PS-53 — Automated testing: Test Engine is deprecated (April 2026, "near-zero usage"); Microsoft's documented path is Playwright with Power Platform samples (canvas, model-driven, custom pages), CI/CD-ready but code-first
- **Classification:** CONSTRAINT
- **Evidence:** "Effective April 2026, Test Engine is deprecated … Test Engine has near-zero usage and failed to meet customer needs … The Power Fx implementation created unnecessary limitations that are avoided if using Playwright directly" (S-70). Playwright samples: "reliable, maintainable end-to-end tests for all Power Platform app types … Works headlessly in GitHub Actions, Azure Pipelines" (S-71, excerpt).
- **Decision impact:** Mission-critical (PS-04) + no pro-dev/QA automation capacity → RISK; otherwise CONDITIONAL.
- **Confidence:** HIGH (deprecation) / MEDIUM (samples scope).
- **Sources:** S-70, S-71, S-67.

### 4.14 Development model and team

#### PS-39 — Microsoft's fusion-development guidance names when citizen development is insufficient: no connector exists, integrity logic must be enforced, complex dynamic business flows — resolved by pro developers via custom connectors, Web APIs, API Management, Logic Apps, Functions
- **Classification:** PATTERN
- **Evidence:** "there will always be more complex situations that can't be satisfied in this way. For example, your organization might have existing systems and databases with which the app needs to interact, and for which no connector is currently available. There might be additional business logic that needs to be enforced to ensure that data remains consistent. An app might need to implement a complex, dynamic business flow. This is where professional developers come into play" (S-40b, 2021-04).
- **Decision impact:** Any of the three signals → HYBRID; all three at scale → consider CUSTOM.
- **Confidence:** MEDIUM (page age) — content corroborated by S-20.
- **Sources:** S-40b, S-20.

#### PS-40 — Team skills are an explicit architecture criterion
- **Classification:** DECISION CRITERION
- **Evidence:** "Choose services that your team knows how to use, or commit to training them before you choose a service." "The best service for your workload might be a technology that your team isn't skilled at, can't afford, or it might require extra security layers" (S-24).
- **Decision impact:** Feed team capability into every HYBRID/CUSTOM recommendation; a HYBRID needing .NET plug-ins is POOR for a team with no developers.
- **Confidence:** HIGH.
- **Sources:** S-24.

#### PS-41 — Configure or buy before build; do not replicate the legacy solution; every extension carries performance, ALM, upgrade and support cost
- **Classification:** RECOMMENDATION
- **Evidence:** "Don't replicate your legacy solution … can also lead to a highly customized solution that fails to apply the strengths of the new platform." "App settings are the safest and least disruptive way to customize your app. You should always try them first." "Low-code and no-code customizations are the best way to extend your app when changing the app settings doesn't meet your requirements." "Use partner solutions … instead of extending." Extension risks: "overextending forms, synchronous events that affect the user experience, and impact on capacity such as service protection limits" (S-30, S-30b).
- **Decision impact:** Requirement already covered by first-party app, AppSource or M365 feature → CUSTOM/OTHER (configure/buy) before build; also supports "process change / do nothing".
- **Confidence:** HIGH.
- **Sources:** S-30, S-30b.

### 4.15 Licensing and cost

#### PS-42 — The licence boundary is a fit boundary: Microsoft 365 seeded rights = standard connectors + Dataverse for Teams only; premium connectors, custom connectors, on-prem/cloud data transfer, full Dataverse, model-driven apps, Power Pages and Managed Environments require premium licences (Premium $20/user/month list; per-app PAYG $10/active user/app/month; Process 250k requests/day)
- **Classification:** DECISION CRITERION
- **Evidence (S-44, Sept 2026):** Power Apps Basic "allows users to customize and extend Microsoft 365 and Office 365 for productivity scenarios, and to deliver a comprehensive low-code extensibility platform for Microsoft Teams only." Table: Standard connectors all columns; "Premium and custom connectors" and "On premises and cloud services data transfer" only Premium / per-app PAYG / D365; "Full Dataverse access" — M365 column "Dataverse for Teams only". "Power Apps Premium $20 per user/month* (or $12 … with 2,000+ new per user licenses)"; "Power Apps per app pay-as-you-go meter $10 per active user/app/month". "Power Automate use rights included with Power Apps don't include RPA functionality". Dynamics 365 rights "must be only within the context of and in the same environment as the licensed Dynamics 365 application". Restricted D365 tables require D365 licences (list not captured, U-5). FAQ: per app subscription "$5/user/app/month" (S-06) — different SKU (C-7).
- **Decision impact:** Satisfiable with standard connectors + SharePoint/Dataverse for Teams → STRONG on seeded licences. Any premium trigger → CONDITIONAL on licence budget for the whole audience (multiplexing forbids workarounds).
- **Conditions:** Prices/SKUs volatile; local pricing unknown (U-8).
- **Confidence:** HIGH (rules) / MEDIUM (prices).
- **Sources:** S-44, S-06.

#### PS-43 — Licensing-driven architecture is an anti-pattern: choosing SharePoint/Excel or shared identities to avoid premium licences produces delegation, threshold, security and compliance failures
- **Classification:** ANTI-PATTERN
- **Evidence:** Composite: SharePoint delegation limits (S-10, S-02); SharePoint 5,000 list view threshold and lookup problems recurring in community and Q&A (T4, S-45); SharePoint security site/list-scoped (S-49); implicit SQL connection risk (S-43); multiplexing prohibition (S-44). Microsoft: "Switch to Microsoft Dataverse as your data source for the broadest delegation support" (S-49).
- **Decision impact:** Data store chosen only for licence avoidance while the requirement has relational/security/volume needs → RISK; re-evaluate Dataverse or CUSTOM.
- **Confidence:** MEDIUM (T4 corroboration; mechanics HIGH).
- **Sources:** S-02, S-10, S-45, S-49, S-43, S-44.

### 4.16 Data-platform nuance

#### PS-56 — Virtual tables expose external data inside Dataverse in real time but drop most enterprise features: no auditing, column security, row-level security ("organization owned"), change tracking/Synapse, offline, dashboards, business process flows or Power Pages solutions
- **Classification:** CONSTRAINT
- **Evidence:** "contain data that is sourced from an external database … without the need for data replication"; "don't support auditing"; "can't be used in rollups or calculated columns"; "Dashboards and charts are not supported"; cannot enable "queues, knowledge management, SLAs, duplicate detection, change tracking, mobile offline capability, column security, Dataverse search, and Power Pages solutions"; "organization owned and don't support the row-level Dataverse security concepts. We recommend that you implement your own security model for the external data source"; "Business process flows are not supported" (S-56, 2026-04).
- **Decision impact:** External system of record + model-driven UX without audit/security/offline needs → CONDITIONAL; with those needs → replicate into standard tables or CUSTOM.
- **Confidence:** HIGH.
- **Sources:** S-56.

### 4.17 Alternatives and hybrid redirects (consolidated)

#### PS-44 — Microsoft-documented redirects away from, or alongside, Power Platform
- **Classification:** PATTERN

| Requirement signal | Target | Evidence |
|---|---|---|
| IT-owned integration estate; dedicated compute; VNET-native runtime; code-first CI/CD with local debug; B2B/EDI | Azure Logic Apps (Standard) | S-08, S-60, S-09 (vendor-side) |
| Code-first orchestration, stateful long-running coordination, compensation across services | Azure Functions / Durable Functions + Service Bus | S-08, S-30b, S-58 |
| Large-scale ETL / transformation | Dataflows / Azure data services | S-22, S-23 |
| Transactional business logic on Dataverse data | Plug-ins, custom API, change sets (2-minute cap) | S-27, S-52, S-54 |
| High-volume semi-structured data | Elastic tables (in-platform) or purpose-built database | S-57, S-24 |
| Reliable event fan-out, multi-consumer | Dataverse → Service Bus / Event Hubs / webhooks | S-21 |
| Bespoke SPA UX with platform governance | Code apps | S-19 |
| Public / anonymous / external-identity web | Power Pages (Dataverse-fronted) or custom web | S-42b, S-51 |
| Requirement already covered | Configure / AppSource ISV / Microsoft 365 native; process change; do nothing | S-30, S-30b |
| Real-time high-ingestion, low-latency data | Purpose-built database | S-24 |
| On-premises / air-gapped | Not Power Platform | S-68, S-47a |

Non-Microsoft low-code platforms are out of this area's scope (handled by other aisa packs).

---

## 5. Anti-patterns

| Id | Anti-pattern | Why it fails | Origin | Findings |
|---|---|---|---|---|
| AP-1 | Complex logic or ETL inside cloud flows | Bottlenecks, unmaintainable, limits | MS | PS-07, PS-25 |
| AP-2 | Nested / per-record loops for thousands of rows | Action multiplication, throttling, 100k cap | MS | PS-25, PS-23 |
| AP-3 | Self-triggering flows | Infinite loops | MS | PS-25 |
| AP-4 | Non-delegable formulas over large tables | Silent partial results | MS | PS-13 |
| AP-5 | SharePoint/Excel as relational system of record to avoid premium | Delegation, threshold, security, integrity | MS + T4 | PS-14, PS-43 |
| AP-6 | Implicitly shared SQL connections | Credential exposure | MS | PS-31 |
| AP-7 | Production processes in default/sandbox/dev environments | Outside resilience commitment; governance gaps | MS | PS-37, PS-05 |
| AP-8 | Shared account / proxy to reduce licences | Multiplexing violation | MS | PS-36, PS-42 |
| AP-9 | Replicating the legacy system feature-for-feature | Over-customisation, technical debt | MS | PS-41 |
| AP-10 | Synchronous heavy plug-ins / overloaded forms | UX latency, 2-minute cap, service protection | MS | PS-09, PS-41 |
| AP-11 | Giant single canvas app / OnStart-heavy | Studio and runtime degradation | MS | PS-06 |
| AP-12 | Business-critical solution without Managed Environments, ALM and automated tests | Outside Microsoft's recommended operating model | MS | PS-04, PS-33, PS-53 |
| AP-13 | Sequential `Patch` or connector writes treated as a transaction | No atomicity; partial failure leaves inconsistent state | MS | PS-45 |
| AP-14 | Elastic tables for transactional data | No multi-record transactions | MS | PS-57 |
| AP-15 | Justifying Azure with "Power Automate has limited versioning/monitoring" | Contradicted by Power Platform ALM docs; real differentiators are compute, network, ownership | MS | PS-24, PS-48 |
| AP-16 | Assuming behaviour can be frozen | Mandatory semi-annual waves; deprecations | MS | PS-50 |

---

## 6. Conflicts (CONFLICTED)

| Id | Topic | Source A | Source B | Assessment |
|---|---|---|---|---|
| C-1 | Default Dataverse DB capacity per tenant | Licensing Guide table: 20 GB (S-44) | Same guide worked example: 10 GB (S-44) | Internal inconsistency; verify in admin center |
| C-2 | Self-service DR billing prerequisite | Licensing Guide Sept 2026: PAYG required (S-44) | BCDR page Aug 2026: "no longer a mandatory requirement" (S-37) | Version drift; product page more recent; verify |
| C-3 | Power Automate "scale" | S-09: "small to medium scale … shared resources" | Process stacking 2.5M requests/day (S-48b) | Resolved as TRADE-OFF: dedicated compute/latency vs request counts (PS-24) |
| C-4 | Concurrent users | No T1 ceiling (S-01, S-11) | T3 degradation reports (S-48) | UNKNOWN per workload; test |
| C-5 | Canvas control heuristics | T4 500/300 (S-46) | T1 qualitative only (S-25) | Heuristic, MEDIUM |
| C-6 | VNET on Power Platform | S-09 (2025): lacking | Managed Environments (2026): "Virtual Network support" (S-18) | Version-sensitive; parity unverified (U-11) |
| C-7 | Per-app price | $5 subscription (S-06) | $10 PAYG meter (S-44) | Different SKUs |
| C-8 | Capacity add-on size | 50,000/day (S-04) | 10,000/day (S-12); admin page silent (S-72) | Unresolved (U-15) |
| C-9 | Availability-zone RPO/RTO applicability | "RTO < 5 minutes" (S-34, S-37) | "limited number of customers … transitioning" (S-37) | Target architecture with rollout caveat (U-12b) |
| C-10 | Existence of Power Apps pattern guidance | Search index lists pattern pages | All fetches redirect; repo 404 (S-33) | Treat as retired until it reappears |

---

## 7. Known gaps deferred to other areas

| Gap | Review id | Target area | Effect if undelivered |
|---|---|---|---|
| Reporting/analytics over Dataverse; document/PDF generation; localisation; notification connector throttles | R-13 | 02, 03, 04 | Rows 1, 5 revert STRONG → UNKNOWN for requirements with these needs |
| Wrap (branded mobile), Intune/MAM | R-14 | 02 | Row 12 UNKNOWN for branded-app requirements |
| ISV / multi-tenant resale licensing | R-22 | 10 | No row; POOR/CONDITIONAL unknown |
| Latency/load benchmarks; gateway sizing | R-24 | 09 | Performance fit stays "validate by test" |
| Full cost model incl. Power Pages pack prices, environment overhead | R-10 | 10 | "CONDITIONAL on budget" rows cannot be quantified |
| Frontline/shared-device identity and licensing | R-11 | 06, 10 | Row 34 UNKNOWN |
| Managed Environment VNet functional parity | C-6 | 05, 06 | Row 20 UNKNOWN |
| SOAP/legacy protocols via custom connectors | U-10 | 05 | Row 9 UNKNOWN for SOAP systems |
| Independent (non-vendor) evidence for fit and failure cases | R-08 | 13 | Confidence stays MEDIUM |

---

## 8. Unknowns (UNKNOWN)

| Id | Unknown | Why it matters | Resolution path |
|---|---|---|---|
| U-1 | Start of strict enforcement of request limits ("no current ETA") | Volume designs on transition limits may break | Track admin-center reporting GA |
| U-2 | Concurrent-user behaviour of apps | Sizing large-audience apps | Load test |
| U-3 | Dataverse web-server count per environment | Throughput planning | "Let the server tell you" (S-03) |
| U-4 | Power Pages traffic/throughput ceilings | Public high-traffic sites | None published |
| U-5 | Current restricted Dynamics 365 tables list | Licensing of apps touching D365 tables | Web page referenced by Licensing Guide |
| U-6 | Cross-region RTO | Contractual DR | Microsoft does not publish one |
| U-7 | Code apps roadmap (Git, mobile, IP restrictions) | Hybrid viability | Re-check S-19 |
| U-8 | Local-currency pricing and EA effects | Cost modelling | Regional price list |
| U-9 | Full text of retired pattern/planning pages | Positive-fit evidence | Possibly retired (C-10) |
| U-10 | SOAP via custom connectors | Legacy integration fit | Area 05 |
| U-11 | Managed Environment VNet coverage of canvas connector calls | Network-isolation fit | Area 06 |
| U-12 | Per-service SLA figures and exclusions | Availability requirements above 99.9% | Read SLA September 2026 document (gate condition) |
| U-12b | Whether the tenant's region is on the availability-zone architecture | Reliability applicability | Ask Microsoft / admin center |
| U-13 | Conflict behaviour of canvas writes on SharePoint/SQL | Multi-user contention | Test |
| U-14 | Frontline / shared-device identity and licensing | Non-Entra populations | Area 10 |
| U-15 | Capacity add-on size (C-8) | Volume remediation cost | Licensing Guide add-on section (gate condition) |
| U-16 | Elastic tables GA status | Maturity of high-volume option | Re-check S-57 |

---

## 9. Implications for the aisa knowledge model (pointers, not pack content)

Nothing below is a question, glossary term, signal or decision-tree node; these are pointers for authoring.

- **Technology-neutral Discovery signals suggested by the evidence:** queried-table volume per screen; requests/day per process owner; longest human wait; synchronous response expectation of callers; atomicity requirement across writes/systems; concurrent-edit contention; offline device class and connectivity pattern; external audience type (known partner vs anonymous public); identity population (Entra vs other); data-access granularity (row/column) and audit obligations; network isolation mandate; deployment model (SaaS acceptable? disconnected sites?); sovereignty regime; contractual availability/RTO; embedding target (browser vs native); existing capability covering the need; expected solution lifetime and tolerance to vendor-driven change; exit/portability requirement; automated-testing obligation; team pro-dev capacity; tenant DLP posture; data growth (attachments, audit).
- **Hard boundaries with Microsoft-stated evidence:** internet-only SaaS (PS-47); no atomicity across connectors (PS-45); flow hard limits (PS-23); browser offline (PS-35); mandatory release waves (PS-50); Managed Environments ↔ premium for all active users (PS-33); multiplexing (PS-36); 2-minute plug-in cap (PS-09); Dataverse-fronted data for Pages and model-driven with virtual-table limits (PS-02, PS-56).
- **Corrected boundary:** Power Automate vs Logic Apps is decided by ownership, network runtime, dedicated compute and code-first tooling — not by "versioning" or "monitoring" (PS-24, PS-48).
- **Options the pack must be able to output:** do nothing / process change; existing M365 or first-party capability; Power Platform on seeded licences; Power Platform premium; hybrid with Azure; Logic Apps/Azure-first; custom application; buy (ISV).
- **Validation before commitment (typical):** delegation proof with data row limit = 1; request-volume estimate vs entitlement; DLP check in target environment; licence census of the full audience; offline limitation checklist; sync/async latency measurement of integrated systems; prototype of one change-set transaction on the critical write path; confirm region AZ status; read SLA document; wave-regression dry run in early access; confirm Managed Environment budget for pipeline targets.

---

## 10. Evidence-quality notes

- **Source bias:** S-09 is authored by the Logic Apps product group to motivate migration; used only for Azure-side capabilities. S-42 (consultancy) and S-48 (custom-development vendor) carry commercial bias toward their offerings; S-41 is an individual blog. Flagged wherever used.
- **Excerpt-only sources:** S-33 (pattern list), S-38 (candidate list), S-50 (Pages minimum anonymous), S-55 (flow changeset restrictions), S-71 (Playwright scope). Findings relying on them are MEDIUM.
- **Aged pages (> 18 months) still used:** S-07 (2024-03), S-07b (2024-06), S-07c (2024-09), S-25 (2023-04), S-36 (2022-09), S-40b (2021-04), S-38b (2020-12), S-38c (2022-03). Findings relying on them carry MEDIUM on numbers or currency.
- **Microsoft publishes no negative-fit guidance** beyond the flows/ETL statement (S-22) and the Pages Web API statement (S-51). All other POOR verdicts are inferences from documented limits and are tagged INF in §2.
- **Documentation drift:** the Power Apps "patterns" and "planning" guidance sets were unreachable on 2026-09-02 (redirect to Plan designer; GitHub 404); Power Automate planning source files remain in the public repo with 2020/2022 dates.

---

## 11. Source register

All Microsoft Learn URLs fetched 2026-09-02. Date = `ms.date` shown in page metadata (updated date where different).

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
| S-09 | T1 (vendor-side) | Power Automate migration to Azure Logic Apps (Standard) | https://learn.microsoft.com/en-us/azure/logic-apps/power-automate-migration | 2025-07-18 |
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
| S-26 | T1 (vendor statement) | How to create performant Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview | 2026-08-20 |
| S-26b | T1 | PPWA Performance Efficiency design principles | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/principles | 2025-08-15 |
| S-27 | T1 | Use Plug-ins to Extend Business Processes | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/plug-ins | 2026-03-30 |
| S-28 | T1 | Custom process actions / low-code plug-in tips (2-minute limit; excerpts) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/workflow-custom-actions ; https://learn.microsoft.com/en-us/power-apps/maker/data-platform/low-code-plug-ins-tips | n/a |
| S-29 | T1 | Limitations of Power Apps component framework | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations | 2025-07-01 |
| S-30 | T1 | D365 Implementation Guide: Extend Dynamics 365 apps without compromising performance | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/extend-your-solution | 2025-07-08 |
| S-30b | T1 | D365 Implementation Guide: Customize and extend Dynamics 365 apps (no-cliffs, PaaS) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/extend-your-solution-scenarios | 2025-07-08 |
| S-31 | T1 | Overview of building a model-driven app | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-driven-app-overview | 2026-01-09 |
| S-32 | T1 | Start building apps (app types, custom pages, Plan designer) | https://learn.microsoft.com/en-us/power-apps/maker/ | 2025-11-17 |
| S-33 | T1 (unreachable) | Power Apps patterns overview — redirects to Plan designer; GitHub source 404 on 2026-09-02 | https://learn.microsoft.com/en-us/power-apps/guidance/patterns/overview | n/a |
| S-34 | T1 | Plan mission critical workloads | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/plan-mission-critical | 2026-05-04 |
| S-35 | T1 | Develop a tenant environment strategy | https://learn.microsoft.com/en-us/power-platform/guidance/adoption/environment-strategy | 2026-05-04 |
| S-36 | T1 | Create accessible canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps | 2022-09-06 |
| S-37 | T1 | Business continuity and disaster recovery | https://learn.microsoft.com/en-us/power-platform/admin/business-continuity-disaster-recovery | 2026-08-20 |
| S-38 | T1 (excerpt) | Types of process automation (Learn page; redirects) | https://learn.microsoft.com/en-us/power-automate/guidance/planning/various-types-process-automation | n/a |
| S-38b | T1 | Types of process automation (public docs source file) | https://raw.githubusercontent.com/MicrosoftDocs/power-automate-docs/main/articles/guidance/planning/various-types-process-automation.md | 2020-12-10 |
| S-38c | T1 | Determining which automation method to use (source file) | https://raw.githubusercontent.com/MicrosoftDocs/power-automate-docs/main/articles/guidance/planning/determine-automation-methods.md | 2022-03-16 |
| S-39 | T3 | Power Automate vs Logic Apps (PnP community, Paul Bullock) | https://pnp.github.io/community-docs/articles/power-automate-vs-logic-apps.html | n/a |
| S-40 | T1 | Connect to SQL Server from Power Apps overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-connection-overview | 2025-03-14 |
| S-40b | T1 | Fusion development e-book, ch. 1 | https://learn.microsoft.com/en-us/power-apps/guidance/fusion-dev-ebook/01-what-is-fusion-dev-approach | 2021-04-26 |
| S-40c | T1 | Microsoft Power Fx overview | https://learn.microsoft.com/en-us/power-platform/power-fx/overview | 2026-08-04 |
| S-41 | T3 | Alan Bonnici — "The Complexity Ceiling: Where Microsoft Power Apps Needs to Evolve" | https://www.alanbonnici.com/2026/05/the-complexity-ceiling-where-microsoft.html | 2026-05 |
| S-42 | T3 (consultancy) | Arinco — Power Apps Code Apps: when to use them | https://arinco.com.au/blog/power-apps-code-apps-when-to-use-them/ | n/a |
| S-42b | T1 | Share a canvas app with guest users | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/share-app-guests | 2025-06-27 |
| S-43 | T1/T2 | Use SQL Server securely with Power Apps; Enhanced security for implicitly shared connections (blog) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-server-security ; https://www.microsoft.com/en-us/power-platform/blog/power-apps/power-apps-secure-implicit-connections/ | 2024-01 |
| S-44 | T1 | Power Platform Licensing Guide, September 2026 (PDF, 30 pp.) | https://go.microsoft.com/fwlink/?LinkId=2085130 | 2026-09 |
| S-45 | T4 | Community/Q&A: SharePoint 5,000 threshold and lookup delegation issues | https://learn.microsoft.com/en-my/answers/questions/5600910/ ; https://www.matthewdevaney.com/sharepoint-delegation-cheat-sheet-for-power-apps/ | n/a |
| S-45b | T1 | Microsoft Dataverse connector reference (changeset action; throttling) | https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/ | 2024-03-01 (updated 2026-07-11) |
| S-46 | T4 | Community: 500 controls/app, 300/screen heuristics | https://www.itaintboring.com/power-platform/why-500-matters-for-canvas-apps/ ; https://hiredgun.tech/canvas-app-size/ | n/a |
| S-47 | T4 | Community: apply-to-each concurrency, throttling, variables in loops | https://sharepains.com/2025/05/15/how-to-avoid-throttling-power-automate/ ; https://theaugmenteddev.com/blog/speeding-up-apply-to-each-power-automate | 2025 |
| S-47a | T1 | Dynamics 365 and Power Platform data residency | https://learn.microsoft.com/en-us/dynamics365/get-started/availability | 2026-07-07 |
| S-47b | T1 | Power Apps US Government | https://learn.microsoft.com/en-us/power-platform/admin/powerapps-us-government | 2026-05-05 |
| S-47c | T1 | Power Platform operated by 21Vianet in China | https://learn.microsoft.com/en-us/power-platform/admin/about-microsoft-cloud-china | 2025-12-05 |
| S-48 | T3 (custom-dev vendor) | Brilworks — Power Apps limitations: signs you need custom development | https://www.brilworks.com/blog/power-apps-limitations/ | n/a |
| S-48b | T1 | Types of Power Automate licenses | https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/types | 2026-07-20 |
| S-49 | T1 (excerpt) | Training: Benefits of using Power Apps with SharePoint / delegation guidance | https://learn.microsoft.com/en-us/training/modules/get-started-power-apps-sharepoint/benefits | n/a |
| S-50 | T1 (excerpt) | Power Pages website capacity consumption reports | https://learn.microsoft.com/en-us/power-pages/admin/website-consumption-reports | n/a |
| S-51 | T1 | Overview of the Power Pages portals Web API | https://learn.microsoft.com/en-us/power-pages/configure/web-api-overview | 2026-08-27 |
| S-52 | T1 | Execute batch operations using the Web API (change sets) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/execute-batch-operations-using-web-api | 2026-03-09 |
| S-53 | T1 | Execute messages in a single database transaction | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/org-service/use-executetransaction | 2025-05-21 |
| S-54 | T1 | Event Framework in Dataverse | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/event-framework | 2026-03-09 |
| S-55 | T1 (excerpt) | Use a flow to perform a changeset request in Dataverse | https://learn.microsoft.com/en-us/power-automate/dataverse/change-set | n/a |
| S-56 | T1 | Create and edit virtual tables | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-virtual-entities | 2026-04-17 |
| S-56b | T1 | Patch function (Power Fx reference) | https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-patch | 2026-05-04 |
| S-57 | T1 | Elastic tables for developers | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/elastic-tables | 2026-08-04 |
| S-58 | T1 | Compensating Transaction pattern (Azure Architecture Center) | https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction | 2026-04-16 |
| S-59 | T1 | Optimistic concurrency (Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimistic-concurrency | 2026-08-27 |
| S-60 | T1 | Get started with integration architecture design (Azure Architecture Center) | https://learn.microsoft.com/en-us/azure/architecture/integration/integration-get-started | 2026-06-18 |
| S-61 | T1 | ALM with Microsoft Power Platform (overview) | https://learn.microsoft.com/en-us/power-platform/alm/overview-alm | 2025-01-29 |
| S-62 | T1 | Overview of pipelines in Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/pipelines | 2026-01-12 |
| S-63 | T1 | Overview of Dataverse Git integration | https://learn.microsoft.com/en-us/power-platform/alm/git-integration/overview | 2025-04-21 |
| S-64 | T1 | Source code files for canvas apps (pa.yaml) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/power-apps-yaml | 2025-03-18 |
| S-65 | T1 | Set up Application Insights with Power Automate | https://learn.microsoft.com/en-us/power-platform/admin/app-insights-cloud-flow | 2025-01-16 |
| S-66 | T1 | General availability deployment (release waves) | https://learn.microsoft.com/en-us/power-platform/admin/general-availability-deployment | 2026-02-20 |
| S-67 | T1 | Important changes (deprecations) coming in Power Platform | https://learn.microsoft.com/en-us/power-platform/important-changes-coming | updated 2026-08-14 |
| S-68 | T1 | Power Platform URLs and IP address ranges | https://learn.microsoft.com/en-us/power-platform/admin/online-requirements | 2026-08-03 |
| S-69 | T1 (index only) | Service Level Agreement for Microsoft Online Services | https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services | Sept 2026 edition listed |
| S-70 | T1 | Power Apps Test Engine overview (deprecated) | https://learn.microsoft.com/en-us/power-apps/developer/test-engine/overview | 2026 |
| S-71 | T1 (excerpt) | Power Platform Playwright samples overview | https://learn.microsoft.com/en-us/power-platform/developer/playwright-samples/overview | n/a |
| S-72 | T1 | Capacity add-ons for Power Apps and Power Automate | https://learn.microsoft.com/en-us/power-platform/admin/capacity-add-on | 2025-12-12 |
