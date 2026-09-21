# Platform Suitability — Research Evidence (v2)

Research area: **01 — Platform Suitability** (`../research-areas.md`).
Version: **v2, 2026-09-02** — supersedes `platform-suitability.md` (v1, kept unchanged for traceability). Incorporates the remediation demanded by `platform-suitability-review.md` (R-01…R-24) and `platform-suitability-gate.md` (FAIL).
Source policy: `../source-policy.md`. Language: English (corpus language); quotes kept verbatim.

Volatility warning: limits, licences, prices and feature flags are valid **on the page dates recorded in §9**. Re-verify before encoding in the pack.

---

## 0. What changed from v1 (remediation log)

| Gap (review id) | Severity | Status in v2 | Where |
|---|---|---|---|
| R-01 Logic Apps comparison single-sourced to the Logic Apps team; Power Platform ALM under-represented | HIGH | **Fixed** — Power Platform ALM/monitoring/testing evidence gathered (solutions, pipelines, Git integration, pa.yaml, App Insights export, Playwright samples); S-09 re-tagged as vendor-side comparison; boundary restated | PS-24 (revised), PS-48, PS-49 |
| R-02 Transactional integrity absent | HIGH | **Fixed** — Dataverse transactions (ExecuteTransaction, change sets, plug-in pipeline), canvas `Patch`, flow changeset action, elastic tables, compensating-transaction pattern | PS-45, PS-57 |
| R-03 SaaS-only / on-premises / sovereign clouds absent | HIGH | **Fixed** — internet connectivity requirement, data residency model, GCC/GCC High/DoD eligibility, 21Vianet; POOR rule for air-gapped | PS-47 |
| R-04 Availability-zone RPO/RTO overstated | HIGH | **Fixed** — restated with rollout caveat | PS-37 (revised) |
| R-09 Lock-in, portability, deprecation cadence absent | HIGH | **Fixed** — release-wave cadence, deprecation policy and 2025–26 list, Power Fx/pa.yaml/solutions/Dataverse export portability | PS-50, PS-51 |
| R-05 SLA scope | MEDIUM | **Partially fixed** — SLA document could not be retrieved (index only); recorded as UNKNOWN with the Dataverse 99.9% statement kept as the only T1 figure | PS-52, U-12 |
| R-07 Positive-fit evidence on excerpts | MEDIUM | **Partially fixed** — pattern pages appear retired (all URLs redirect; GitHub source 404); PS-01 downgraded and re-based on model-driven overview + Power Automate planning source files (2020/2022) | PS-01 (revised), PS-21 (revised), PS-58 |
| R-12 Testing capability | MEDIUM | **Fixed** — Test Engine deprecated Apr 2026; Playwright samples are the documented path | PS-53 |
| R-15 "Dataverse-only" overstated | MEDIUM | **Fixed** — virtual tables capabilities/limits added; wording softened | PS-56, PS-02/PS-36 (revised) |
| R-16 / C-8 capacity add-on 10k vs 50k | LOW | **Still CONFLICTED** — admin page does not state the number | C-8 |
| R-18 Online concurrency | MEDIUM | **Fixed** — optimistic concurrency (SDK/Web API only), canvas conflict error | PS-46 |
| R-11 Identity prerequisites | MEDIUM | **Partially fixed** — Entra work/school account prerequisite documented; frontline/shared-device licensing not researched | PS-60, U-14 |
| R-06 Marketing statements | MEDIUM | **Fixed** — "100 tables / 50 screens" and connector counts removed as evidence; kept only as vendor statements | PS-06, PS-26 |
| R-20 Inferred vs Microsoft-stated boundaries | MEDIUM | **Fixed** — every matrix row tagged MS / INF / T3 | §2 |
| R-21 Adjective thresholds | MEDIUM | **Fixed** — matrix rows carry numeric thresholds where a number exists, UNKNOWN otherwise | §2 |
| R-13 reporting/document generation/localisation; R-14 wrap/MDM; R-22 ISV; R-24 performance benchmarks; R-10 full cost model | MEDIUM/LOW | **Not fixed** — out of this pass; listed in §6 for Areas 02–15 | §6 |

---

## 1. Classification model

| Class | Meaning |
|---|---|
| **STRONG FIT** | Documented platform pattern; no documented limit approached; standard licence models apply cleanly. |
| **CONDITIONAL FIT** | Fit depends on a measurable condition (volume, licence, data source, governance maturity, team). Must be validated before commitment. |
| **POOR FIT** | Collides with a documented hard limit, an explicit Microsoft "not the best choice" statement, or an unsupported scenario. |
| **HYBRID** | Power Platform for UX/orchestration/data plus Azure or code for the part that exceeds platform limits (Microsoft's "no-cliffs" approach). |
| **CUSTOM / OTHER** | Another Microsoft technology or configure/buy is documented as more appropriate for the whole requirement. |

Evidence tags: FACT, RECOMMENDATION, CONSTRAINT, TRADE-OFF, RISK, ANTI-PATTERN, DECISION CRITERION, PATTERN. Source tiers T1–T4 as in `../source-policy.md`. Origin tags used in §2: **MS** = explicit Microsoft statement; **INF** = inferred by the analyst from documented limits; **T3** = independent source.

---

## 2. Consolidated fit matrix (revised)

| # | Observable characteristic | Threshold / measure | Default fit | Origin | Findings |
|---|---|---|---|---|---|
| 1 | Internal structured-data app: forms, approvals, inspections, asset/case tracking | Queried tables ≤ 2,000 rows or delegable; ≤ 6,000 requests/day/user on seeded licences | STRONG | MS (model-driven "process driven apps") + INF | PS-01, PS-13, PS-19 |
| 2 | Relational, process-heavy data with row/column security or audit | Any | STRONG (model-driven + Dataverse, premium) | MS | PS-02, PS-14, PS-31 |
| 3 | Team app inside Teams | < 2 GB / ≈1M rows; no API, offline, audit, field security | STRONG (Dataverse for Teams) | MS | PS-16 |
| 4 | Document-centric collaboration | Light metadata, no relational queries | STRONG (SharePoint) | MS | PS-14 |
| 5 | Human-in-the-loop workflow | Longest pending wait ≤ 30 days | STRONG | MS | PS-22 |
| 6 | Canvas over large tables | > 2,000 rows in any queried table | CONDITIONAL (delegable source + formulas) | MS | PS-13 |
| 7 | Business-critical process | Downtime causes financial/regulatory harm | CONDITIONAL (mission-critical model; Managed Environments; premium for all active users) | MS | PS-04, PS-33 |
| 8 | Org-wide audience or sensitive data | > ~50 users or regulated data | CONDITIONAL (enterprise environment class, ALM) | MS | PS-05 |
| 9 | Premium/custom connectors, on-prem or SQL data | Any | CONDITIONAL (licence for whole audience; gateway) | MS | PS-26, PS-42 |
| 10 | Automation volume | Requests/day/owner vs 6,000 / 40,000 / 250,000 (stackable ×10) | CONDITIONAL → HYBRID above | MS | PS-19, PS-23 |
| 11 | Integration write throughput into Dataverse | > 6,000 requests / 5 min / user or > 52 concurrent | CONDITIONAL (429 handling) → HYBRID | MS | PS-18 |
| 12 | Offline, managed mobile, Dataverse | ≤ 3M rows; features within S-07c list | STRONG/CONDITIONAL | MS | PS-35 |
| 13 | Offline in browser, or offline on non-Dataverse data | Any | POOR | MS | PS-35 |
| 14 | External partners with Entra B2B | Licence recognised cross-tenant (not per-app) | CONDITIONAL | MS | PS-36 |
| 15 | Anonymous/public audience | Unique users/month × pack price; Dataverse-fronted data | CONDITIONAL (Power Pages) or CUSTOM | MS | PS-36, PS-56 |
| 16 | ETL / nightly mass processing in flows | Thousands of rows per run | POOR for flows → dataflows / Azure | MS | PS-07, PS-25 |
| 17 | Algorithmic core (iteration to convergence, mutable state, recursion) | Any | HYBRID (plug-in / Functions) or CUSTOM | T3 + INF | PS-08 |
| 18 | Synchronous caller wait | > 120 s (flow) / 180 s (canvas) | POOR as sync → async / HYBRID | MS | PS-28 |
| 19 | Flow hard limits | > 500 actions, nesting > 8, > 100,000 items, > 100 MB, > 10 GB/day | POOR for that flow → Logic Apps / Functions | MS | PS-23 |
| 20 | Private-network-only | No public endpoints permitted | CONDITIONAL (Managed Env + VNet) or Logic Apps Standard | MS (version-sensitive) | PS-32 |
| 21 | Availability / DR | > 99.9% or contractual cross-region RTO, or integrations inside the resilience boundary | CONDITIONAL/POOR | MS + UNKNOWN (SLA doc) | PS-37, PS-52 |
| 22 | IT-owned automation, Git-first, deep observability | Any | CONDITIONAL (solutions, pipelines, Git integration, App Insights export — all premium) or Logic Apps Standard | MS | PS-24, PS-48, PS-49 |
| 23 | Brand-critical UX | Design-system-level branding, native gestures | CONDITIONAL (canvas+PCF) / HYBRID (code apps) / CUSTOM | MS + T3 | PS-10, PS-03 |
| 24 | Embed in native product; intercepting proxies | Any | POOR / CUSTOM | MS | PS-12 |
| 25 | Single-app scope | Thousands of controls, hundreds of data sources, formulas > 256k chars | CONDITIONAL (partition) | MS | PS-06 |
| 26 | Need already covered by first-party / ISV / M365 feature | Any | CUSTOM/OTHER (configure or buy) | MS | PS-41 |
| 27 | No pro-dev capacity but HYBRID needed | Any | RISK | MS | PS-40 |
| 28 | **Multi-record / multi-system atomicity** | Two or more writes that must succeed or fail together | CONDITIONAL (Dataverse change set / plug-in) — POOR across connectors or on elastic tables → compensation or CUSTOM | MS | PS-45, PS-57 |
| 29 | **On-premises / air-gapped / customer-hosted** | Any | POOR (SaaS only) | MS | PS-47 |
| 30 | **Regulated sovereign cloud** | GCC/GCC High/DoD eligibility; China 21Vianet | CONDITIONAL (eligibility, feature parity exceptions) | MS | PS-47 |
| 31 | **Frozen behaviour / long solution lifetime** | Cannot absorb two mandatory release waves per year; > 5-year lifetime | RISK → CONDITIONAL | MS | PS-50, PS-51 |
| 32 | **Exit / portability requirement** | Must be re-hostable elsewhere | RISK (UI and flows rewrite; data portable) | MS + INF | PS-51 |
| 33 | **Concurrent edits on the same record** | Multi-user contention | CONDITIONAL (Dataverse optimistic concurrency via code; canvas conflict error handling) | MS | PS-46 |
| 34 | **Users without Entra work/school identity** | Frontline, shared devices, non-Entra IdP | CONDITIONAL (guest B2B, Pages identities) — UNKNOWN for frontline licensing | MS (partial) | PS-60 |
| 35 | **Automated testing required (mission-critical)** | Any | CONDITIONAL (Playwright, code-first; Test Engine deprecated) | MS | PS-53 |
| 36 | Exact datacentre disclosure | Any | POOR | MS | PS-17 |

---

## 3. Findings

Findings PS-01…PS-44 carried from v1 (condensed where unchanged; **revised** ones marked). PS-45…PS-60 are new.

### 3.1 Application types

#### PS-01 (revised) — Power Platform targets line-of-business apps, process automation and Dataverse-backed external sites; the former "Power Apps patterns" catalogue could not be retrieved and appears retired
**Classification:** FACT / PATTERN
**Evidence:** Developer overview: canvas/model-driven apps "shared with internal users … run in a browser or on a mobile device"; Power Automate "automate tasks and orchestrate activities"; Power Pages "external-facing business websites" (S-20). Model-driven apps "especially well suited to process driven apps that are data dense … onboarding new employees, managing a sales process, or member relationships" (S-31). Power Automate planning source (ms.date 2020-12-10): API-based digital process automation preferred because "APIs are meant to be stable even as the application changes over time", whereas "RPA is susceptible to breaking when things change" (S-38b). **Retrieval note:** every URL under `/power-apps/guidance/patterns/` redirected to the Plan designer page on 2026-09-02 and the GitHub source files returned 404 (S-33); the approval/inspection/asset/calculation list survives only in search snippets.
**Why it matters:** The positive-fit prior now rests on the model-driven statement and process-automation guidance, not on a curated pattern catalogue.
**Decision impact:** STRONG for data-dense process apps and API-based automation of stable systems; the specific "pattern names" are heuristics (MEDIUM).
**Conditions:** Verify pattern guidance if it reappears; Microsoft's current entry point for "what to build" is the AI Plan designer (S-32).
**Confidence:** HIGH (model-driven/DPA statements) / MEDIUM (pattern list).
**Sources:** S-20, S-31, S-38b, S-33, S-32.

#### PS-02 (revised) — Canvas vs model-driven decision: model-driven requires a Dataverse data model (external data possible via virtual tables) and gives responsive/accessible UI; canvas gives pixel control and connectors at the cost of consistency and ALM effort
**Classification:** DECISION CRITERION
**Evidence:** Comparison table (S-31): Data platform "Dataverse only" vs "Dataverse + many others using connectors"; UI control "Limited" vs "Full"; migration "Simple" vs "Potentially complex"; responsive/accessible built in vs designed in. Virtual tables let external data "appear to exist in Dataverse" with restrictions (S-56, see PS-56). Custom pages bring canvas into model-driven (S-32).
**Decision impact:** Relational, many related tables → model-driven. Task-focused, multi-source, mobile-first → canvas (CONDITIONAL on delegation).
**Conditions:** Model-driven on phone browser unsupported (S-01).
**Confidence:** HIGH. **Sources:** S-31, S-32, S-01, S-56.

#### PS-03 — Code apps: pro-dev SPA hosted and governed by Power Platform; Premium licence per user; no Git integration, no Windows player, public asset endpoint
**Classification:** PATTERN / CONSTRAINT
**Evidence:** S-19 (2026-08-12): "don't support Power Platform Git integration", "aren't supported in Power Apps for Windows", "compiled app assets are served from a publicly accessible endpoint", "End users … need a Power Apps Premium license". T3 (S-42): "Choose code apps when you need a custom SPA frontend with stronger engineering control."
**Decision impact:** HYBRID candidate for bespoke internal UX. Not for anonymous, native mobile, IP-restricted.
**Confidence:** HIGH facts / MEDIUM maturity. **Sources:** S-19, S-42.

#### PS-04 — Productivity vs mission-critical workload: mission-critical "demands deep platform knowledge" and "engineering rigor"
**Classification:** DECISION CRITERION / RISK
**Evidence:** S-34 table (built ad-hoc vs built to last; no tests vs automated tests; development in production vs ALM). "Operationalizing mission-critical workloads necessitates a high level of engineering rigor."
**Decision impact:** Business-critical → CONDITIONAL on operating model (PS-33, PS-48, PS-53).
**Confidence:** HIGH. **Sources:** S-34.

#### PS-05 — Personal / team / enterprise classification; enterprise requires ALM, sandboxes, managed solutions in production
**Classification:** RECOMMENDATION
**Evidence:** S-35: enterprise "ALM is required, with preproduction work happening in sandbox environments and only managed solutions allowed in production"; default environment sharing limit "between 5 and 50 users".
**Confidence:** HIGH. **Sources:** S-35.

### 3.2 Complexity

#### PS-06 (revised) — Large canvas apps degrade Studio and runtime; partition via multiple apps or model-driven + custom pages
**Classification:** CONSTRAINT / TRADE-OFF
**Evidence:** S-25: "nearly all apps with a long load time for Power Apps Studio have at least one formula of more than 256,000 characters"; "Some apps grow to thousands of controls and hundreds of data sources, which slows Power Apps Studio". The v1 counter-quote ("100 tables and over 50 screens", S-26) is a vendor statement without data and is **no longer used as evidence**. 500/300 control heuristics are T4 (S-46), MEDIUM.
**Decision impact:** Large scope → CONDITIONAL (partition).
**Confidence:** HIGH constraint / MEDIUM numbers. **Sources:** S-25, S-46.

#### PS-07 — Microsoft: complex logic and large-scale transformation do not belong in cloud flows
**Classification:** RECOMMENDATION / ANTI-PATTERN
**Evidence:** S-22: "isn't the best choice for large-scale data transformation or integration"; alternatives: plug-ins, custom connectors to Azure Functions/APIM/App Service, dataflows. S-24: reuse via plug-ins.
**Confidence:** HIGH. **Sources:** S-22, S-24.

#### PS-08 — Power Fx lacks imperative loops/mutable state; algorithm-heavy logic is friction (T3) with T1 structural corroboration
**Classification:** RISK / CONSTRAINT
**Evidence:** S-41 (T3); S-25 hidden-button `Select` workaround; S-40c (Power Fx overview): declarative/functional design, "Power Fx offers imperative logic when needed", user-defined functions "with more enhancements on the way".
**Decision impact:** Iteration-to-convergence, recursion, mutable multi-step state → HYBRID or CUSTOM. Simple calculations → fine.
**Confidence:** MEDIUM. **Sources:** S-41, S-25, S-40c.

#### PS-09 — Plug-ins: hard 2-minute limit, synchronous plug-ins delay users; heavy processing to Azure ("no-cliffs")
**Classification:** CONSTRAINT / PATTERN
**Evidence:** S-27, S-28, S-30b.
**Confidence:** HIGH. **Sources:** S-27, S-28, S-30b.

### 3.3 UX

#### PS-10 — Bespoke/brand-critical/consumer UX: poor on model-driven, conditional on canvas (+PCF), Power Pages or custom web for public
**Classification:** TRADE-OFF
**Evidence:** S-31, S-29 (PCF: no Dataverse WebAPI in canvas, no custom auth), S-20, S-01, S-42.
**Confidence:** HIGH facts. **Sources:** S-31, S-29, S-20, S-01, S-42.

#### PS-11 — Accessibility built in for model-driven; maker responsibility for canvas
**Classification:** FACT / DECISION CRITERION. **Evidence:** S-31, S-36 (page dated 2022-09; MEDIUM currency). **Sources:** S-31, S-36.

#### PS-12 — No native-client embedding of canvas; no iFrame of model-driven; proxies unsupported; 180 s outbound timeout
**Classification:** CONSTRAINT. **Evidence:** S-01. **Confidence:** HIGH.

### 3.4 Data

#### PS-13 — Delegation: non-delegable queries operate on first 500 (max 2,000) rows and can return wrong results
**Classification:** CONSTRAINT / RISK. **Evidence:** S-02, S-10, S-40. **Confidence:** HIGH.

#### PS-14 — Data store choice: Dataverse (relational, secured, bypasses APIM); SharePoint (documents); SQL (existing DB, premium, gateway, implicit connection risk); Excel not a database
**Classification:** DECISION CRITERION. **Evidence:** S-11, S-12, S-10, S-40, S-43, S-45 (T4). **Confidence:** HIGH.

#### PS-15 — Dataverse capacity is an entitlement, not a technical limit; 250 MB DB / 2 GB file accrue per Premium user; DB overage $48/GB/month
**Classification:** TRADE-OFF / CONSTRAINT. **Evidence:** S-13, S-44, S-14. **Conditions:** C-1 (10 vs 20 GB default). **Confidence:** HIGH rules / MEDIUM default GB.

#### PS-16 — Dataverse for Teams bounded: 2 GB/≈1M rows, no API/plug-ins/PCF/model-driven/audit/field security/offline
**Classification:** CONSTRAINT. **Evidence:** S-14, S-06. **Confidence:** HIGH.

#### PS-17 (revised) — Data residency: environment bound to region; macro-region replication permitted; some metadata stored globally; exact datacentre not disclosed
**Classification:** FACT / CONSTRAINT
**Evidence:** S-15; S-47a (2026-07-07): "Microsoft might replicate your customer data to other datacenter regions within a macro region geography"; globally stored items include "Dataverse table and column names … replicated globally for support and troubleshooting purposes, but the content within those database tables remains stored in geo"; Power Pages "Website name and URL are stored globally"; Power Apps/Power Automate connected to Dynamics 365 "customer data may be sent outside of the designated region to where these services are deployed"; "Microsoft does not control or restrict the locations from which customers, or their end users, may access customer data." Brazil South may replicate to South Central US.
**Decision impact:** Residency requirement → CONDITIONAL; metadata-in-geo or exact-location requirement → POOR.
**Confidence:** HIGH. **Sources:** S-15, S-47a, S-37.

### 3.5 Transactions and concurrency

#### PS-18 — Dataverse service protection: 6,000 requests / 20 min execution / 52 concurrent per user per 5 minutes per web server
**Classification:** CONSTRAINT. **Evidence:** S-03; Dataverse connector throttling "API calls per connection 6000 / 300 seconds" (S-45b). **Confidence:** HIGH.

#### PS-19 — Daily request entitlements 40,000 / 6,000 / 250,000; flows use owner's limits; retries count; enforcement in transition
**Classification:** DECISION CRITERION. **Evidence:** S-04, S-05; Process licences "Up to 10 Process licenses can be stacked on a single cloud flow" and flow groups share 250,000 across up to 25 flows (S-48b, 2026-07-20). **Confidence:** HIGH.

#### PS-20 — No documented concurrent-user ceiling for apps
**Classification:** FACT (absence). **Evidence:** S-01, S-11, S-17. **Confidence:** MEDIUM.

#### PS-45 (new) — Atomicity exists only inside Dataverse (change sets, ExecuteTransaction, synchronous plug-in pipeline); canvas `Patch`, cross-connector flows and elastic tables are not transactional; Microsoft's documented remedy across services is the compensating-transaction pattern
**Classification:** DECISION CRITERION / CONSTRAINT
**Evidence:**
- Dataverse: "Batch requests can contain up to 1,000 individual requests … When multiple operations are contained in a change set, all the operations are considered atomic … if any one of the operations fails, the batch request rolls back any completed operations." `GET` not allowed in change sets (S-52). SDK: `ExecuteTransactionRequest` — "Should any one of the requests fail and the transaction is rolled back, any data changes completed during the transaction are undone"; cannot nest `ExecuteMultiple` inside (S-53). Event pipeline: PreOperation and PostOperation run "within the database transaction"; "An exception thrown by your code at any synchronous stage within the database transaction causes the entire transaction to roll back"; asynchronous steps "run outside of the database transaction" (S-54).
- Power Automate: Dataverse connector action "Perform a changeset request … perform a group of Microsoft Dataverse connector operations as a single transaction. If one of the operations fails, all the successful actions are rolled back" (S-45b); documented restrictions: only "Add a new row, Delete a row, and Update a row" are supported; "The Apply to each action isn't supported in a changeset"; "You can't reference an output of a previous action in the changeset scope" (S-55, via search excerpt of the change-set page). No transactional construct exists across different connectors.
- Canvas: `Patch` with tables writes one-for-one records; errors surface per record via `IfError`/`Errors` ("Some records failed to update"); no statement of atomicity across records or tables; "Conflicts exist with changes on the server" error when another user modified the record (S-56b).
- Elastic tables: "don't support multi-record transactions … Elastic tables also don't support grouping requests in a single database transaction … Currently, these operations succeed but aren't atomic" (S-57).
- Cross-service: Azure Architecture Center compensating-transaction pattern — "Use this pattern when a business operation spans multiple steps, services, or data stores and must be undone if a later step fails … can't rely on atomic transactions"; "It's not easy to generalize compensation logic. A compensating transaction is application specific"; not suitable when "The system can't tolerate temporary inconsistency, or compensation can't reliably restore a valid state. Use strong consistency mechanisms or atomic transactions across all steps instead." (S-58)
**Why it matters:** Ledger-like, stock-movement, allocation or payment-like processes need all-or-nothing semantics. On Power Platform that is available only when every write is a Dataverse standard-table operation inside one change set / plug-in; anything touching SharePoint, SQL connectors, external APIs or elastic tables is eventually consistent by construction and needs hand-built compensation.
**Decision impact:** Requirement "writes must succeed or fail together": within Dataverse → CONDITIONAL (design with change sets or plug-in; canvas must call a custom API/flow changeset rather than sequential `Patch`); across connectors/systems → POOR for low-code alone → HYBRID (orchestrator with compensation, e.g., Durable Functions) or CUSTOM; on elastic tables → POOR.
**Conditions:** Batch ≤ 1,000 operations; plug-in 2-minute cap applies (PS-09); compensation logic must be idempotent and monitored (S-58).
**Confidence:** HIGH.
**Sources:** S-52, S-53, S-54, S-45b, S-55, S-56b, S-57, S-58.

#### PS-46 (new) — Concurrent edits: Dataverse optimistic concurrency is available only via SDK/Web API ("no setting for it in a form of the web application"); canvas `Patch` on Dataverse surfaces a server-conflict error that the maker must handle; behaviour on SharePoint/SQL not documented here
**Classification:** CONSTRAINT / DECISION CRITERION
**Evidence:** "Optimistic concurrency is supported on all out-of-box tables enabled for offline sync and all custom tables … You can only set optimistic concurrency behavior through an SDK API call. There's currently no setting for it in a form of the web application." Errors `ConcurrencyVersionMismatch` etc. (S-59, 2026-08-27). `Patch`: "'Conflicts exist with changes on the server': This error occurs when another user or process modifies the same record between the time your app reads the record and writes the change. Refresh the data source … and retry" (S-56b).
**Why it matters:** Shared queues, allocations and collaborative editing lose updates silently unless the app or code handles versions.
**Decision impact:** High-contention records → CONDITIONAL (Dataverse + explicit conflict handling in canvas or code); on other stores → UNKNOWN (U-13) → validate.
**Confidence:** HIGH (Dataverse) / UNKNOWN (others).
**Sources:** S-59, S-56b.

### 3.6 Process

#### PS-21 (revised) — Automation candidates: repetitive, rule-based, frequent, cross-system re-keying, human-independent; API-based automation preferred over UI automation for stability
**Classification:** PATTERN / DECISION CRITERION
**Evidence:** Source file (2020-12-10): DPA via APIs "meant to be stable even as the application changes over time"; RPA "susceptible to breaking when things change, such as when updates are applied … or the layout of an application's screens" (S-38b). Automation methods page (2022-03-16): connector "Easiest"; custom connector "resilient to system changes"; HTTP for one-offs; browser/desktop automation for UI-only; "In complex automation scenarios, you can combine all these methods"; the document "does not explicitly state when Power Automate is not the right tool" (S-38c). The "repetitive/high-volume/manual re-keying" list remains excerpt-level (MEDIUM).
**Decision impact:** Stable API available → STRONG (cloud flows). UI-only legacy → CONDITIONAL (RPA fragility). Judgement-heavy → CONDITIONAL.
**Confidence:** MEDIUM. **Sources:** S-38b, S-38c.

#### PS-22 — Approvals/long waits ≤ 30 days STRONG; pending steps time out at 30 days
**Classification:** CONSTRAINT / PATTERN. **Evidence:** S-05, S-24. **Confidence:** HIGH.

#### PS-23 — Flow hard limits (500 actions, nesting 8, 100k items, 120 s sync, 100 MB, 10 GB/day High, 14-day auto-off when throttled/erroring)
**Classification:** CONSTRAINT. **Evidence:** S-05 (2026-07-17). **Confidence:** HIGH.

#### PS-24 (revised) — Power Automate vs Logic Apps Standard is a trade-off on ownership, network isolation, dedicated compute and code-first ALM — not on raw volume; the most-cited comparison is authored by the Logic Apps product group and several of its cells are contradicted by Power Platform documentation
**Classification:** TRADE-OFF / DECISION CRITERION
**Evidence:**
- Vendor-side comparison (S-09, Logic Apps docs, 2025-07): Power Automate "Small to medium scale workflows … limited by shared resources"; "Limited versioning"; "Basic monitoring through the Power Automate portal"; "RBAC works at the user level … In Azure Logic Apps, RBAC works at the resource level".
- Neutral Azure guidance (S-08, 2026-03): "Power Automate empowers business users, office workers, and citizen developers to build simple integrations … Azure Logic Apps supports integrations ranging from little-to-no-code scenarios to more advanced, codeful, and complex workflows. Examples include B2B processes." Architecture Center: both are "well-suited for trigger-based or time-based tasks" and "built on the same underlying technology" (S-60).
- Power Platform counter-evidence: Process licence gives 250,000 requests/day per flow, stackable to 10 (2.5M/day), flow groups; "Organizations looking to automate their business processes at scale using cloud flows or unattended desktop automations" (S-48b). Solutions + pipelines: "Solutions are exported as soon as a deployment request is submitted … The same solution artifact must pass through pipeline stages in sequential order. The system also prevents any tampering"; approvals via delegated deployments; "Can I roll back to a previous version? Yes" (S-62). Native Git integration for solutions in developer environments (S-63, 2025-04). Canvas source files `.pa.yaml` (S-64). Flow telemetry to Application Insights with alerting, managed environments only, "not 100% lossless" (S-65). Service-principal-owned flows with Process licence remove the leaver dependency (S-04).
**Why it matters:** Recommending Azure because "Power Automate has limited versioning/monitoring" is not supportable; recommending it for dedicated compute, VNET-native runtime, resource-level RBAC, local debugging, B2B/EDI, or a team already Azure-native is.
**Decision impact:** Choose Logic Apps Standard when: IT owns the integration estate; private-network runtime is mandatory (see PS-32 for the Power Platform alternative); latency/throughput SLAs need dedicated compute; code-first CI/CD with local debugging is required; B2B/EDI. Choose Power Automate when: business ownership; M365/Dataverse context; human tasks/approvals; volume fits Process licences; governance via Managed Environments is acceptable. Volume alone is CONDITIONAL, not POOR.
**Conditions:** Every Power Platform ALM/monitoring capability above requires Managed Environments/premium licences for target environments (S-62 "Licenses granting premium use rights are required for all managed environments").
**Confidence:** HIGH.
**Sources:** S-09, S-08, S-60, S-48b, S-62, S-63, S-64, S-65, S-04.

#### PS-25 — Flow anti-patterns (nested loops, infinite loops, transformations, per-record loops) and remedies
**Classification:** ANTI-PATTERN. **Evidence:** S-23. **Confidence:** HIGH.

### 3.7 Integration

#### PS-26 (revised) — Connectors wrap REST APIs; premium/custom connectors and on-prem data need premium licences and (on-prem) the gateway; custom connectors capped at 500 req/min/connection and 50 per user; connector counts are marketing figures and not used as evidence
**Classification:** CONSTRAINT / FACT. **Evidence:** S-20, S-44, S-05, S-48 (T3, custom-dev vendor bias noted). **Confidence:** HIGH facts.

#### PS-27 — Event-driven integration via Service Bus / Event Hubs / webhooks; 192 KB payload cap; not in Dataverse for Teams
**Classification:** PATTERN / CONSTRAINT. **Evidence:** S-21, S-24, S-14. **Confidence:** HIGH.

#### PS-28 — Synchronous windows: 180 s canvas, 120 s flows
**Classification:** CONSTRAINT. **Evidence:** S-01, S-05. **Confidence:** HIGH.

#### PS-29 — Tenant DLP can make a design infeasible (design-time block; runtime quarantine; up to 24 h)
**Classification:** RISK. **Evidence:** S-16. **Confidence:** HIGH.

### 3.8 Scalability and performance

#### PS-30 — Well-Architected: stay within platform limits; prefer platform features; weigh skills
**Classification:** RECOMMENDATION. **Evidence:** S-24, S-26b. **Confidence:** HIGH.

#### PS-57 (new) — Elastic tables give Cosmos-DB-backed horizontal scale inside Dataverse for spiky/high-volume data, at the cost of transactions, deep insert and strong cross-session consistency
**Classification:** PATTERN / TRADE-OFF
**Evidence:** "Use elastic tables … You must handle a high volume of read and write requests"; "Use standard tables … Your application requires strong data consistency … transactional capability across tables or during plug-in execution … complex joins"; "Each logical partition can store 20 gigabytes (GB)"; session-token consistency; TTL expiry; "Elastic tables don't support multi-record transactions"; known issues "should be addressed before this feature becomes generally available" (S-57, 2026-08-04).
**Why it matters:** IoT/telemetry/log-style requirements previously pushed off-platform have an in-platform option, but it is not a substitute for a transactional store.
**Decision impact:** High-ingestion semi-structured data → HYBRID-within-platform (elastic + standard tables); transactional high-volume → still HYBRID/CUSTOM.
**Conditions:** Maturity caveat ("before this feature becomes generally available" wording present on a 2026 page).
**Confidence:** HIGH facts / MEDIUM maturity.
**Sources:** S-57.

### 3.9 Security

#### PS-31 — Dataverse enterprise security model; SharePoint/SQL-connector designs weaker or riskier
**Classification:** FACT / RISK. **Evidence:** S-12, S-14, S-43, S-49. **Confidence:** HIGH.

#### PS-32 — Network isolation: Logic Apps VNET vs Power Platform Managed Environment VNet support (version-sensitive; parity unverified)
**Classification:** CONSTRAINT / TRADE-OFF. **Evidence:** S-09, S-18, S-19. **Conditions:** C-6, U-11. **Confidence:** HIGH facts / MEDIUM equivalence.

### 3.10 Governance and lifecycle

#### PS-33 — Managed Environments package enterprise governance and require standalone licences for all active users
**Classification:** CONSTRAINT / DECISION CRITERION. **Evidence:** S-18, S-44, S-62. **Confidence:** HIGH.

#### PS-34 — Ownership: user-level access; 90-day inactivity auto-off for non-premium flows; mitigations via solutions, service principals, Process licence
**Classification:** RISK. **Evidence:** S-09, S-05, S-04, S-48b. **Confidence:** HIGH.

#### PS-48 (new) — Power Platform has a documented production ALM stack — solutions, pipelines with pre-validation, approvals, artefact immutability and rollback, native Git integration, human-readable canvas source, App Insights export — all gated on Dataverse and Managed Environments
**Classification:** FACT / CONSTRAINT
**Evidence:** "Solutions are the mechanism for implementing ALM … Source control should be your source of truth … all environments that participate in ALM must include a Dataverse database" (S-61). Pipelines: "Solution deployments are prevalidated against the target environment"; "Connections and environment variables are provided upfront and validated"; "the system doesn't re-export a solution for deployments to subsequent stages … prevents any tampering"; rollback "If the pipeline setting is enabled, you can redeploy previous solution versions"; "Pipelines … don't contain data stored within Dataverse tables"; "Can pipelines deploy to a different tenant? No"; "The current implementation uses a single development environment for a given solution"; licences: "All other environments used in pipelines must be enabled as managed environments. Licenses granting premium use rights are required for all managed environments"; "Starting February 2026, Microsoft will start enabling managed environments for any pipeline target environments" (S-62). Git integration: "Use Git integration with developer environments, not in your test or production environments"; code-first objects should be built by a build process, not committed as binaries (S-63). Canvas source: "The generated canvas app YAML code is read-only and can't be modified … External editing, merging, and conflict resolution is supported only in Power Platform Git Integration"; "The YAML schema is in active development" (S-64). Flow telemetry: "Requests" and "Dependencies" tables, alert rules; "turned on and supported for managed environments only"; "aren't transactional data and hence are not 100% lossless"; not available in GCC/GCC High/DoD (S-65).
**Why it matters:** Directly rebuts "limited versioning / basic monitoring" as a reason to leave the platform, while showing the real constraints: Dataverse dependency, premium licensing, single dev environment per solution in pipelines, read-only canvas source outside Git integration, and no data migration in solutions.
**Decision impact:** IT-grade ALM requirement → CONDITIONAL (Managed Environments + Dataverse + pipelines/Git) rather than POOR. Cross-tenant deployment or multi-developer isolated environments per solution → use Azure DevOps/GitHub extensions.
**Conditions:** Dates: pipelines page 2026-01-12; Git integration 2025-04-21; pa.yaml 2025-03-18; App Insights 2025-01-16.
**Confidence:** HIGH.
**Sources:** S-61, S-62, S-63, S-64, S-65.

#### PS-49 (new) — Source bias note: the Logic Apps migration comparison is authored to motivate migration; its claims are retained only where corroborated
**Classification:** RISK (evidence quality)
**Evidence:** S-09 is titled "Power Automate migration to Azure Logic Apps (Standard)" and opens "This guide outlines the advantages gained from transitioning to Azure Logic Apps (Standard)". Cells corroborated elsewhere: dedicated compute and VNET-native runtime (S-08 says Standard offers "direct access to virtual network integration"); resource-level RBAC (Azure RBAC docs); local development in VS Code. Cells contradicted or nuanced: "Limited versioning" (PS-48), "Basic monitoring" (S-65), "Small to medium scale" (PS-19 Process stacking).
**Decision impact:** Use S-09 only for Azure-side capabilities; use Power Platform docs for Power Platform capabilities.
**Confidence:** HIGH. **Sources:** S-09, S-08, PS-48 sources.

#### PS-50 (new) — Platform change cadence is mandatory and fast: two release waves per year that "can't be postponed", weekly service updates, and a rolling deprecation list with notice periods from months to years
**Classification:** RISK / DECISION CRITERION
**Evidence:** "Each release wave becomes generally available twice a year. Your environments automatically receive these mandatory updates." "A release wave is a mandatory update and can't be postponed." Regional windows (e.g., Europe April 10–13 and October 9–12, 2026) (S-66, 2026-02-20). Deprecation policy: "'Deprecated' means we intend to remove the feature … fully supported until it's officially removed. This deprecation notification can span a few months or years." 2025–2026 deprecations include Cards for Power Apps, Test Engine (April 2026), Power Automate mobile app (Aug 2026), classic look for model-driven apps (April 2026), Editable Grid/Read-Only Grid controls (March 2026), BYOK, SQL connector V1 actions (S-67, updated 2026-08-14). Power Fx: "Every saved Power Fx document includes a language version stamp … 'back compat converter' … automatically rewrites the formula" (S-40c).
**Why it matters:** Solutions inherit continuous change: UI controls, connectors and designers can be deprecated during the solution's life; regression testing per wave is an operating cost; behaviour cannot be frozen. Power Fx itself is designed for forward compatibility, which mitigates language-level breakage.
**Decision impact:** Requirement for frozen/validated behaviour (e.g., regulated systems needing revalidation per change) → RISK → CONDITIONAL (budget for wave regression, early-access testing). Long lifetime (> 5 years) → include deprecation exposure in TCO.
**Conditions:** Early access opt-in exists; Message Center notifications.
**Confidence:** HIGH.
**Sources:** S-66, S-67, S-40c.

#### PS-51 (new) — Portability: data and .NET plug-in code are portable; canvas UI, Power Fx formulas and flow definitions are not re-hostable outside Power Platform (Power Fx open-sourcing is "in the process"); exit means rebuilding UI and orchestration
**Classification:** RISK / DECISION CRITERION
**Evidence:** Power Fx: "Microsoft will make Power Fx available as open-source software. It's currently integrated into canvas apps, and Microsoft is in the process of extracting it from Power Apps for use in other Microsoft Power Platform products and as open source" (S-40c, 2026-08-04). Canvas source `.pa.yaml`: read-only, "schema is in active development", external editing only via Git integration (S-64). Solutions export components between Dataverse environments; "Can pipelines deploy to a different tenant? No" (S-62). Dataverse data access for exit: TDS endpoint ports 1433/5558 (S-68), Synapse Link, Data Export Service, events to Service Bus (S-14). Flows: JSON definitions; Microsoft documents a migration path to Logic Apps Standard (S-09) — i.e., flows are portable only toward Azure.
**Why it matters:** The pack must price reversibility. Data is exportable; logic in plug-ins is standard .NET; but every canvas/model-driven screen, Power Fx formula and flow is a rewrite on exit. There is no documented export to a non-Microsoft runtime.
**Decision impact:** Requirement "solution must be re-hostable / vendor-neutral" → RISK (HIGH) → prefer CUSTOM or keep logic in portable layers (Dataverse data + .NET/Azure) and treat Power Apps as a replaceable UI.
**Conditions:** Multiplexing/licensing does not restrict export of your own data.
**Confidence:** HIGH (facts) / MEDIUM (exit-cost judgement).
**Sources:** S-40c, S-64, S-62, S-68, S-14, S-09.

### 3.11 Offline

#### PS-35 — Offline only in mobile players; Dataverse offline-first (3M rows, auto conflicts); non-Dataverse LoadData/SaveData 30–70 MB; model-driven offline feature gaps
**Classification:** CONSTRAINT / DECISION CRITERION. **Evidence:** S-07 (2024-03), S-07b (2024-06), S-07c (2024-09) — MEDIUM currency. **Confidence:** HIGH constraint / MEDIUM numbers.

### 3.12 External users and identity

#### PS-36 (revised) — External users: B2B guests need cross-tenant-recognised licences; anonymous/consumer via Power Pages over Dataverse-fronted data with capacity licensing; multiplexing prohibited; Pages Web API not for third-party integration
**Classification:** DECISION CRITERION / CONSTRAINT. **Evidence:** S-42b, S-06, S-50, S-51, S-44; virtual tables in Pages exist but "Power Pages solutions" is listed among features virtual tables cannot enable (S-56) — treat Pages external data as CONDITIONAL. **Confidence:** HIGH.

#### PS-60 (new, partial) — Identity prerequisite: internal use requires Microsoft Entra work or school accounts; sovereign clouds bind to specific Entra instances; personal Microsoft accounts have been removed from Power Automate
**Classification:** CONSTRAINT / DECISION CRITERION
**Evidence:** Power Automate Free: "included at no cost for work or school accounts in a Microsoft Entra tenant" (S-48b). GCC High "enables and requires the customer to use Microsoft Entra Government for customer identities, in contrast to GCC which uses Public Microsoft Entra ID" (S-47b). Deprecation: "Personal Microsoft service accounts in Power Automate — May 27, 2025 … July 26, 2025" (S-67). Guests via Entra B2B (S-42b).
**Why it matters:** Populations without Entra identities (contractors on shared devices, JV staff) cannot use internal apps without licensing and identity work.
**Decision impact:** Non-Entra population → CONDITIONAL (B2B, Pages identities); frontline shared-device licensing → UNKNOWN (U-14).
**Confidence:** MEDIUM (partial coverage).
**Sources:** S-48b, S-47b, S-67, S-42b.

### 3.13 Operations, reliability, deployment model

#### PS-37 (revised) — Reliability: Dataverse 99.9% SLA statement; availability-zone architecture targets near-zero RPO and RTO < 5 min but is **rolling out** ("A limited number of customers in certain regions are transitioning"); cross-region DR is self-service with no published RTO; integrations are outside the resilience commitment
**Classification:** FACT / CONSTRAINT
**Evidence:** "Dataverse … offers a service level agreement of 99.9% uptime" (S-12). BCDR page (2026-08-20): "The recovery point objective is near zero, and the recovery time objective is less than five minutes"; "A limited number of customers in certain regions are transitioning to the improved architecture. Whether the region transitioned or is transitioning, the service always keeps a backup of environment data in more than one data center"; "This capability is available only for production environments"; "Microsoft doesn't publish a cross-region RTO commitment"; "when Power Platform solutions connect to external systems … fall outside the scope of Power Platform's resiliency commitments"; Power Automate under SSDR "known performance limitations" (S-37). Licensing Guide: SSDR "must be linked to a pay-as-you-go billing plan" (S-44) vs BCDR page "no longer a mandatory requirement" (C-2).
**Decision impact:** ≤ 99.9% and in-region HA → STRONG once the tenant's region is confirmed on the AZ architecture; otherwise CONDITIONAL. Contractual cross-region RTO or > 99.9% → POOR (INF).
**Conditions:** Verify region status (U-12b); SLA document not retrieved (PS-52).
**Confidence:** HIGH (statements) / MEDIUM (applicability to a given tenant).
**Sources:** S-12, S-37, S-44.

#### PS-38 — Monitoring/versioning: see PS-48 (revised position). App Insights export exists for apps and flows (managed environments); flow run history transactional, 30-day retention
**Classification:** TRADE-OFF. **Evidence:** S-65, S-05. **Confidence:** HIGH.

#### PS-47 (new) — Power Platform is cloud-only: it "requires connectivity to the internet", stores customer data in Azure datacenters, and offers no on-premises or customer-hosted deployment; sovereign options are US Government (eligibility-gated) and China 21Vianet, both with feature-parity exceptions
**Classification:** CONSTRAINT / DECISION CRITERION
**Evidence:** "Microsoft Power Platform requires connectivity to the internet. The endpoints listed in this article should be reachable" (S-68, 2026-08-03). "Microsoft Dynamics 365 and Power Platform store customer data in Microsoft Azure datacenters located in various geographic regions around the world" (S-47a). Sandbox plug-ins reaching external services need the `PowerPlatformPlex` service tag ranges (S-68). US Government: "available to (1) US federal, state, local, tribal, and territorial government entities and (2) other entities that handle data that's subject to government regulations … subject to validation of eligibility"; "There are exceptions to the principle of maintaining product functional parity within the US Government clouds" (S-47b, 2026-05-05). China: "physically separated environment of cloud services … operated … by a local operator … subject to Chinese laws"; "there are exceptions that are affected by dependent service availability, market priorities, or compliance regulations" (S-47c). No Microsoft page found describing an on-premises or private-hosted Power Platform; the only on-premises component is the data gateway, which bridges cloud-hosted apps to on-premises data (S-10, S-48b).
**Why it matters:** Industrial/OT networks, classified enclaves, or policies forbidding SaaS for a data class cannot be served. The gateway does not change where the app and its logic run.
**Decision impact:** Must run disconnected from the internet, inside a customer-controlled datacentre, or on an isolated OT network → POOR (MS). Regulated public-sector data in the US or data-in-China mandates → CONDITIONAL on eligibility and feature parity. Everything else → connectivity prerequisite (endpoints, proxies — PS-12) must be validated.
**Conditions:** Regional feature parity documents (aka.ms/BAPFunctionalParity) are PDFs not read in this pass.
**Confidence:** HIGH.
**Sources:** S-68, S-47a, S-47b, S-47c, S-10, S-48b.

#### PS-52 (new) — Per-service SLA figures could not be verified: the Microsoft Online Services SLA is published as downloadable documents behind an index page; only the Dataverse 99.9% statement is in T1 web documentation
**Classification:** UNKNOWN (evidence gap)
**Evidence:** Two attempts to read the SLA (licensing docs index and Product Terms page) returned indexes only; the Product Terms page displayed "ServiceLevelAgreements is not available on this date" (S-69). Licensing Guide notes Power Automate desktop free application "with no SLA or Microsoft support" (S-44, footnote 9).
**Decision impact:** Any availability commitment above "Dataverse 99.9%" is UNKNOWN until the SLA document (September 2026 edition) is read; exclusions for connectors/third-party dependencies unknown.
**Confidence:** n/a.
**Sources:** S-69, S-44.

#### PS-53 (new) — Automated testing: Test Engine is deprecated (April 2026, "near-zero usage"); Microsoft's documented path is Playwright with Power Platform samples (canvas, model-driven, custom pages, Gen UX), CI/CD-ready but code-first
**Classification:** CONSTRAINT / DECISION CRITERION
**Evidence:** "Effective April 2026, Test Engine is deprecated … Test Engine has near-zero usage and failed to meet customer needs … The Power Fx implementation created unnecessary limitations that are avoided if using Playwright directly" (S-70). Playwright samples: "framework that lets you write reliable, maintainable end-to-end tests for all Power Platform app types … Works headlessly in GitHub Actions, Azure Pipelines" (S-71, search excerpt).
**Why it matters:** The mission-critical model (PS-04) requires automated tests; on Power Platform that now means TypeScript/Playwright skills, not a low-code test tool.
**Decision impact:** Mission-critical + no pro-dev/QA automation capacity → RISK; otherwise CONDITIONAL.
**Confidence:** HIGH (deprecation) / MEDIUM (samples scope, excerpt-level).
**Sources:** S-70, S-71, S-67.

#### PS-39 — Fusion development triggers: missing connector, integrity logic, complex dynamic flow → pro developers
**Classification:** PATTERN. **Evidence:** S-40b (2021 — MEDIUM currency), S-20. **Confidence:** MEDIUM/HIGH.

#### PS-40 — Team skills as an architecture criterion
**Classification:** DECISION CRITERION. **Evidence:** S-24. **Confidence:** HIGH.

#### PS-41 — Configure/buy before build; don't replicate legacy
**Classification:** RECOMMENDATION. **Evidence:** S-30, S-30b. **Confidence:** HIGH.

### 3.14 Licensing and cost

#### PS-42 — Licence boundary: M365 seeded = standard connectors + Dataverse for Teams; premium triggers; Premium $20/user/month; per-app PAYG $10/active user/app/month; Process 250k/day
**Classification:** DECISION CRITERION / CONSTRAINT. **Evidence:** S-44 (Sept 2026), S-06, S-48b. **Confidence:** HIGH rules / MEDIUM prices.

#### PS-43 — Licensing-driven architecture anti-pattern
**Classification:** ANTI-PATTERN. **Evidence:** S-02, S-10, S-45 (T4), S-49, S-43, S-44. **Confidence:** MEDIUM.

#### PS-44 (revised) — Microsoft-documented redirects away from or alongside Power Platform

| Requirement signal | Target | Evidence |
|---|---|---|
| IT-owned integration estate; dedicated compute; VNET-native runtime; code-first CI/CD with local debug; B2B/EDI | Azure Logic Apps (Standard) | S-08, S-09 (vendor-side), S-60 |
| Code-first orchestration, stateful long-running coordination, compensation across services | Azure Functions / Durable Functions + Service Bus | S-08, S-30b, S-58 |
| Large-scale ETL | Dataflows / Azure data services | S-22, S-23 |
| Transactional business logic on Dataverse | Plug-ins, custom API, change sets (2-minute cap) | S-27, S-52, S-54 |
| High-volume semi-structured data | Elastic tables (in-platform) or purpose-built DB | S-57, S-24 |
| Event fan-out | Dataverse → Service Bus / Event Hubs / webhooks | S-21 |
| Bespoke SPA with governance | Code apps | S-19 |
| Public / anonymous web | Power Pages or custom web | S-42b, S-51 |
| Existing capability | Configure / AppSource / M365 | S-30 |
| On-premises / air-gapped | Not Power Platform | S-68, S-47a |

### 3.15 Data platform nuances

#### PS-56 (new) — Virtual tables expose external data inside Dataverse in real time but drop most enterprise features: no auditing, no column security, no row-level security ("organization owned"), no change tracking/Synapse, no offline, no dashboards, no BPF, no Power Pages solutions
**Classification:** CONSTRAINT / PATTERN
**Evidence:** "Virtual tables … contain data that is sourced from an external database, such as an Azure SQL Database … without the need for data replication"; restrictions: "don't support auditing"; "can't be used in rollups or calculated columns"; "Dashboards and charts are not supported"; features that "cannot be enabled": "queues, knowledge management, SLAs, duplicate detection, change tracking, mobile offline capability, column security, Dataverse search, and Power Pages solutions"; "Virtual tables are organization owned and don't support the row-level Dataverse security concepts. We recommend that you implement your own security model for the external data source"; "Business process flows are not supported" (S-56, 2026-04-17).
**Why it matters:** They rescue "system of record stays in SQL" scenarios for model-driven UX, but not when the requirement also needs audit, row security, offline or Pages.
**Decision impact:** External system of record + model-driven UX + no audit/security/offline needs → CONDITIONAL; with those needs → replicate into standard tables or CUSTOM.
**Confidence:** HIGH.
**Sources:** S-56.

#### PS-58 (new) — Documentation drift as an evidence risk: the Power Apps "patterns" and "planning" guidance sets are unreachable on Microsoft Learn (redirect to Plan designer) and absent from the public docs repository as of 2026-09-02
**Classification:** RISK (evidence quality)
**Evidence:** Fetch attempts: `/power-apps/guidance/patterns/overview`, `/approval-pattern`, `/inspection-pattern`, `/power-apps/guidance/planning/*`, `/power-automate/guidance/planning/*` (Learn) → Plan designer page; GitHub raw for patterns → 404; Power Automate planning source files still present in the repo (S-38b, S-38c) but with 2020/2022 dates.
**Decision impact:** Do not encode pattern names as Microsoft-endorsed fit rules; treat as heuristics.
**Confidence:** HIGH (observation).
**Sources:** S-33, S-38b, S-38c.

#### PS-59 (new) — Capacity add-on size remains conflicted between two T1 pages
**Classification:** CONFLICTED
**Evidence:** S-04: "Each capacity add-on raises the request limit by another 50,000 per 24 hours." S-12: "Each capacity add-on provides an additional 10,000 requests every 24 hours." Admin add-on page (S-72, 2025-12-12) does not state the number.
**Decision impact:** Volume remediation cost estimates must carry a 5× uncertainty until the Licensing Guide add-on section is read.
**Sources:** S-04, S-12, S-72.

---

## 4. Anti-patterns (consolidated, revised)

| Id | Anti-pattern | Why it fails | Origin | Evidence |
|---|---|---|---|---|
| AP-1 | Complex logic or ETL inside flows | Bottlenecks, limits | MS | PS-07, PS-25 |
| AP-2 | Nested / per-record loops for thousands of rows | Action multiplication, 100k cap | MS | PS-25 |
| AP-3 | Self-triggering flows | Infinite loops | MS | PS-25 |
| AP-4 | Non-delegable formulas over large tables | Silent partial results | MS | PS-13 |
| AP-5 | SharePoint/Excel as relational system of record to avoid premium | Delegation, threshold, security | MS+T4 | PS-14, PS-43 |
| AP-6 | Implicitly shared SQL connections | Credential exposure | MS | PS-31 |
| AP-7 | Production in default/sandbox/dev environments | Outside resilience commitment | MS | PS-37 |
| AP-8 | Shared account / proxy to reduce licences | Multiplexing violation | MS | PS-36 |
| AP-9 | Replicating legacy feature-for-feature | Over-customisation | MS | PS-41 |
| AP-10 | Synchronous heavy plug-ins / forms | UX latency, 2-min cap | MS | PS-09 |
| AP-11 | Giant single canvas app | Studio/runtime degradation | MS | PS-06 |
| AP-12 | Business-critical without Managed Environments/ALM/tests | Outside recommended model | MS | PS-04, PS-33, PS-53 |
| **AP-13** | **Sequential `Patch`/connector writes treated as a transaction** | No atomicity; partial failure leaves inconsistent state | MS | PS-45 |
| **AP-14** | **Elastic tables for transactional data** | No multi-record transactions | MS | PS-57 |
| **AP-15** | **Justifying Azure with "Power Automate has limited versioning/monitoring"** | Contradicted by Power Platform ALM docs; real differentiators are compute, network, ownership | MS | PS-48, PS-49 |
| **AP-16** | **Assuming behaviour can be frozen** | Mandatory semi-annual waves; deprecations | MS | PS-50 |

---

## 5. Conflicts (CONFLICTED)

| Id | Topic | A | B | Assessment |
|---|---|---|---|---|
| C-1 | Default Dataverse DB capacity | Licensing Guide table 20 GB | Same guide example 10 GB | Internal inconsistency; verify in admin center |
| C-2 | SSDR billing prerequisite | Licensing Guide Sept 2026: PAYG required | BCDR page Aug 2026: "no longer mandatory" | Version drift; verify |
| C-3 | Power Automate "scale" | S-09 "small to medium" | Process stacking 2.5M/day | Resolved as TRADE-OFF (compute/latency vs request counts) — see PS-24 |
| C-4 | Concurrent users | No T1 ceiling | T3 degradation reports | UNKNOWN per workload |
| C-5 | Canvas control heuristics | T4 500/300 | T1 qualitative only | Heuristic, MEDIUM |
| C-6 | VNET on Power Platform | S-09 (2025) lacks | Managed Env (2026) has | Version-sensitive; parity unverified |
| C-7 | Per-app price | $5 subscription | $10 PAYG meter | Different SKUs |
| **C-8** | Capacity add-on size | 50,000 (S-04) | 10,000 (S-12) | Unresolved (PS-59) |
| **C-9** | Reliability architecture applicability | "RTO < 5 min" (S-34, S-37) | "limited number of customers … transitioning" (S-37) | Same source; treat as target architecture with rollout caveat |
| **C-10** | Existence of Power Apps pattern guidance | Search index lists pattern pages | All fetches redirect; repo 404 | Treat as retired until reappears |

---

## 6. Gaps deliberately left for other areas (not fixed in v2)

| Gap | Review id | Target area |
|---|---|---|
| Reporting/analytics over Dataverse; document/PDF generation; localisation; notification connector throttles | R-13 | 02 Application, 03 Data, 04 Automation |
| Wrap (branded mobile), Intune/MAM | R-14 | 02 Application |
| ISV / multi-tenant resale licensing | R-22 | 10 Licensing |
| Latency/load benchmarks; gateway sizing | R-24 | 09 Performance |
| Full cost model incl. Power Pages pack prices, environment overhead | R-10 | 10 Licensing |
| Frontline/shared-device licensing | R-11 | 10 Licensing / 06 Security |
| Managed Environment VNet functional parity | C-6 | 06 Security / 05 Integration |
| SOAP/legacy protocols via custom connectors | U-10 | 05 Integration |

---

## 7. Unknowns (UNKNOWN)

| Id | Unknown | Resolution path |
|---|---|---|
| U-1 | Strict enforcement start for request limits | Admin-center reporting GA |
| U-2 | Concurrent-user ceilings for apps | Load test |
| U-3 | Dataverse web-server count per environment | Measure |
| U-4 | Power Pages traffic ceilings | None published |
| U-5 | Restricted D365 tables list | Web page not captured |
| U-6 | Cross-region RTO | Not published by Microsoft |
| U-7 | Code apps roadmap | Re-check S-19 |
| U-8 | Local pricing | Price list |
| U-9 | Full text of retired pattern/planning pages | Possibly retired (C-10) |
| U-10 | SOAP via custom connectors | Area 05 |
| U-11 | Managed Env VNet parity | Area 06 |
| U-12 | Per-service SLA figures and exclusions | Download SLA September 2026 document (PS-52) |
| U-12b | Is the tenant's region on the availability-zone architecture | Ask Microsoft / admin center |
| U-13 | Conflict behaviour of canvas writes on SharePoint/SQL | Test |
| U-14 | Frontline / shared-device identity and licensing | Area 10 |
| U-15 | Capacity add-on size (C-8) | Licensing Guide add-on section |
| U-16 | Elastic tables GA status ("before this feature becomes generally available") | Re-check S-57 |

---

## 8. Implications for aisa (pointers, not pack content)

- **New technology-neutral Discovery signals:** atomicity requirement across writes/systems; deployment model (SaaS acceptable? disconnected sites?); sovereignty regime; expected solution lifetime and tolerance to vendor-driven change; exit/portability requirement; identity population (Entra vs other); concurrent-edit contention; automated-testing obligation.
- **Hard boundaries now evidence-backed:** internet-only SaaS (PS-47); no atomicity across connectors (PS-45); mandatory release waves (PS-50); UI/logic not re-hostable (PS-51); flow hard limits (PS-23); browser offline (PS-35).
- **Corrected boundary:** Power Automate vs Logic Apps is decided by ownership, network, dedicated compute and code-first tooling — not by "versioning" or "monitoring" (PS-24, PS-48, PS-49).
- **Validation before commitment (additions):** confirm region AZ status; read SLA document; confirm Managed Environment budget for pipeline targets; prototype one change-set transaction for the critical write path; run a wave-regression dry run in early access.

---

## 9. Source register

Existing ids S-01…S-51 as in v1 (`platform-suitability.md §8`) unless re-dated below. New or re-used ids:

| Id | Tier | Title | URL | Date |
|---|---|---|---|---|
| S-33 | T1 | Power Apps patterns (unreachable; redirects to Plan designer; GitHub source 404 on 2026-09-02) | https://learn.microsoft.com/en-us/power-apps/guidance/patterns/overview | n/a |
| S-38b | T1 | Types of process automation (source file) | https://raw.githubusercontent.com/MicrosoftDocs/power-automate-docs/main/articles/guidance/planning/various-types-process-automation.md | 2020-12-10 |
| S-38c | T1 | Determining which automation method to use (source file) | https://raw.githubusercontent.com/MicrosoftDocs/power-automate-docs/main/articles/guidance/planning/determine-automation-methods.md | 2022-03-16 |
| S-40c | T1 | Microsoft Power Fx overview | https://learn.microsoft.com/en-us/power-platform/power-fx/overview | 2026-08-04 |
| S-45b | T1 | Microsoft Dataverse connector reference (changeset action; throttling 6000/300 s) | https://learn.microsoft.com/en-us/connectors/commondataserviceforapps/ | 2024-03-01 (updated 2026-07-11) |
| S-47a | T1 | Dynamics 365 and Power Platform data residency | https://learn.microsoft.com/en-us/dynamics365/get-started/availability | 2026-07-07 |
| S-47b | T1 | Power Apps US Government | https://learn.microsoft.com/en-us/power-platform/admin/powerapps-us-government | 2026-05-05 |
| S-47c | T1 | Power Platform operated by 21Vianet in China | https://learn.microsoft.com/en-us/power-platform/admin/about-microsoft-cloud-china | 2025-12-05 |
| S-48b | T1 | Types of Power Automate licenses | https://learn.microsoft.com/en-us/power-platform/admin/power-automate-licensing/types | 2026-07-20 |
| S-52 | T1 | Execute batch operations using the Web API (change sets) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/execute-batch-operations-using-web-api | 2026-03-09 |
| S-53 | T1 | Execute messages in a single database transaction | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/org-service/use-executetransaction | 2025-05-21 |
| S-54 | T1 | Event Framework in Dataverse | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/event-framework | 2026-03-09 |
| S-55 | T1 | Use a flow to perform a changeset request in Dataverse (search excerpt) | https://learn.microsoft.com/en-us/power-automate/dataverse/change-set | n/a |
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
| S-68 | T1 | Power Platform URLs and IP address ranges (online requirements) | https://learn.microsoft.com/en-us/power-platform/admin/online-requirements | 2026-08-03 |
| S-69 | T1 | Service Level Agreement for Microsoft Online Services (index only; document not read) | https://www.microsoft.com/licensing/docs/view/Service-Level-Agreements-SLA-for-Online-Services | Sept 2026 edition listed |
| S-70 | T1 | Power Apps Test Engine overview (deprecated) | https://learn.microsoft.com/en-us/power-apps/developer/test-engine/overview | 2026 |
| S-71 | T1 | Power Platform Playwright samples overview (search excerpt; direct fetch 404) | https://learn.microsoft.com/en-us/power-platform/developer/playwright-samples/overview | n/a |
| S-72 | T1 | Capacity add-ons for Power Apps and Power Automate | https://learn.microsoft.com/en-us/power-platform/admin/capacity-add-on | 2025-12-12 |

Bias notes: S-09 authored by the alternative's product team (PS-49); S-42 consultancy; S-48 custom-development vendor; S-41 individual blog. Excerpt-only sources: S-33, S-55, S-71.
