# Research Gate — Platform Suitability

Inputs: `platform-suitability.md` (44 findings, matrix §2, conflicts §4, unknowns §5) and `platform-suitability-review.md` (24 findings, verdict NEEDS MORE RESEARCH).
Gate date: 2026-09-02. Neither input file was modified.

## Status

FAIL

## Strong Fit

Evidence-backed (Tier 1, dated, cross-referenced) conditions under which Power Platform is the natural default:

- Internal, structured-data business app of the documented pattern family (approval, inspection, asset, calculation, case-style), with queried tables provably delegable and daily request volume well inside the owner's licence entitlement (PS-01, PS-13, PS-19). Caveat: the pattern list itself is excerpt-sourced (R-07).
- Relational, process-heavy data with row/column-level security or audit needs, built as a model-driven app on Dataverse, with premium licences accepted (PS-02, PS-14, PS-31).
- Human-in-the-loop workflows and approvals whose longest pending wait is ≤30 days (PS-22, PS-23).
- Small team solution inside Microsoft Teams, <≈1M rows / 2 GB, no API, offline, audit or field security needs, on seeded Microsoft 365 licences (PS-16, PS-42).
- Document-centric collaboration with light metadata on SharePoint (PS-14).
- Offline field work on managed mobile devices using the Power Apps mobile player with Dataverse data, within the documented offline limitations (PS-35).
- Extension of Microsoft 365 or Dynamics 365 in their own context, where configuration or low-code is Microsoft's stated first choice before code (PS-41, PS-05).

## Conditional Fit

Conditions where the answer depends on a measurable attribute or an organisational fact:

- Queried tables above 2,000 rows on canvas: only with a delegable source and delegable-only formulas; SharePoint becomes weak, Excel/collections fail (PS-13, PS-14).
- Business-critical solution: only with the mission-critical operating model (team, ALM, Managed Environments, premium licences for all active users, monitoring) (PS-04, PS-33, PS-37).
- Organisation-wide audience or sensitive data: requires enterprise environment class and ALM (PS-05).
- Premium or custom connectors, on-premises data, SQL: licence for the whole audience, data gateway, per-connection throttles, secure implicit connections (PS-26, PS-42, PS-31).
- Requests per day per owner approaching 6,000 / 40,000 / 250,000: Process licence, pay-as-you-go, or hybrid for the volume path (PS-19, PS-23).
- Sustained high write throughput from integrations into Dataverse: design for 429s, batching, real-time pacing; beyond that, Azure buffering (PS-18).
- Known external partners via Entra B2B: guest licensing recognised across tenants (per-app plans are not) (PS-36).
- Public or anonymous audience: Power Pages with Dataverse-fronted data and per-unique-user capacity licensing (PS-36; see R-15 on virtual tables).
- Private-network-only requirement: Managed Environments + VNet support, functional parity unverified (PS-32, C-6).
- Complex or reusable business logic: plug-ins (2-minute cap) or custom connectors to Azure Functions; flows only orchestrate (PS-07, PS-09).
- Bespoke brand-critical UX: canvas + PCF, or code apps (Premium per user, no Git integration, no Windows player) (PS-10, PS-03).
- Data-heavy solutions: Dataverse has no technical size limit but capacity is a cost driver ($48/GB/month database overage, USD list) (PS-15).
- Very large single-app scope: partition into multiple apps or model-driven + custom pages (PS-06).
- Data residency: environment region fixed at creation; India/Australia tenant constraints (PS-17).
- Tenant DLP policy: required connectors must be allowed in the target environment (PS-29).
- IT-owned automation that must survive staff turnover: solutions, service-principal ownership, Process licence (PS-34).

## Poor Fit

Situations where Power Platform should not be the default. Rows marked (inferred) derive from documented limits rather than an explicit Microsoft statement (R-20).

- Large-scale ETL or data transformation in cloud flows — Microsoft explicit: "isn't the best choice for large-scale data transformation or integration" (PS-07).
- Offline in a browser, or offline over non-Dataverse data beyond a few tens of MB (PS-35).
- Callers expecting a synchronous response longer than ~2 minutes (PS-28) (inferred).
- Any single cloud-flow hard limit exceeded: 500 actions, nesting 8, 100,000 loop items, 100 MB message, 10 GB/day content (PS-23) (inferred).
- Embedding inside native desktop/mobile products; operation behind intercepting proxies (PS-12).
- Contractual cross-region RTO or availability above 99.9%, or resilience that must include integrated external systems (PS-37) (inferred; SLA scope itself under-verified, R-05).
- Public high-traffic API or third-party integration surface exposed via Power Pages Web API — Microsoft explicit: "isn't optimized for third-party services or application integration" (PS-36).
- Requirement already met by a first-party Dynamics 365 app, AppSource solution or Microsoft 365 feature — configure or buy first (PS-41).
- Exact datacentre disclosure required (PS-17).
- Not yet evidenced but expected POOR: on-premises / air-gapped / customer-hosted deployment (R-03); multi-record ACID transactions across systems without plug-in/custom API (R-02); ISV multi-tenant resale products (R-22).

## Decision Criteria

Concrete attributes the evidence supports asking for, with the thresholds available today:

- Rows per queried table vs 500 / 2,000 non-delegable limit; delegability of each filter, sort, search, aggregate on the chosen source.
- Requests per day per process owner vs 6,000 (M365 seeded, per app, PAYG) / 40,000 (Premium, D365) / 250,000 (Process, per flow); retries and pagination count.
- Requests per 5 minutes per identity vs 6,000 and 52 concurrent (Dataverse service protection), per web server.
- Longest human wait in a process vs 30-day run limit.
- Synchronous latency expected by callers vs 120 s (flows) / 180 s (canvas).
- Items per run, payload size, daily content volume vs 100,000 / 100 MB (1 GB chunked) / 10 GB.
- Offline: device class (mobile player vs browser), data source (Dataverse vs other), rows to sync vs 3M, field-level security needed offline.
- External audience type: employee / contractor (>30 h/week or onsite daily) / external; Entra B2B vs anonymous; unique users per month for Pages capacity.
- Data-access granularity: row / column / hierarchy / audit → Dataverse vs SharePoint.
- Data volume growth: database vs file placement; per-licence accrual 250 MB DB / 2 GB file.
- Licence posture of the full audience: seeded vs premium; any premium trigger (premium/custom connector, Dataverse, on-prem, model-driven, Pages, Managed Environments).
- Criticality class: personal / team / enterprise; business impact of downtime.
- Network mandate: public endpoint acceptable vs private-only.
- Ownership: business-owned vs IT-owned; survives leaver.
- Team capability: citizen makers only vs pro developers (.NET, Azure).
- Existing capability check: first-party, ISV, M365 feature covering the need.
- Tenant DLP: required connectors allowed in target environment.
- Missing from evidence, needed for a decision: atomicity requirement (R-02), deployment model on-prem/cloud (R-03), identity population (R-11), solution lifetime vs deprecation cadence (R-09), concurrent-edit contention (R-18), reporting/document/localisation needs (R-13).

## Alternatives

Microsoft-documented redirects, plus non-build options:

- Azure Logic Apps (Standard): complex, high-volume, security-sensitive, IT-owned integration; VNET, resource-level RBAC, Git CI/CD, dedicated compute (PS-24; source bias noted in R-01).
- Azure Functions / Durable Functions: code-first orchestration, heavy compute, stateful coordination (PS-09, PS-44).
- Dataflows / Azure data services: ETL and bulk transformation (PS-07, PS-25).
- Dataverse plug-ins and custom API: performant transactional logic within the 2-minute cap (PS-09, PS-27).
- Dataverse → Service Bus / Event Hubs / webhooks: decoupled, multi-consumer event integration (PS-27).
- Power Apps code apps: bespoke SPA with platform governance (PS-03).
- Power Pages vs custom web application: external audiences; custom web when UX, traffic or API exposure exceed Pages (PS-36, PS-10).
- Purpose-built database (Azure SQL, Cosmos): high-ingestion or low-latency data workloads (PS-30).
- Configure or buy: Dynamics 365 first-party, AppSource ISV, Microsoft 365 native features (PS-41).
- Process change / do nothing: Microsoft's "determine the need" and "don't replicate the legacy solution" guidance (PS-41).
- Not covered and out of this area's scope: non-Microsoft low-code platforms (OutSystems, Mendix) — handled by other aisa packs.

## Critical Risks

Risks that could flip a recommendation if unmanaged:

- Pilot-to-production failure through non-delegable queries returning partial results silently at runtime (PS-13).
- Licensing-driven architecture: SharePoint/Excel or shared identities chosen to avoid premium, producing delegation, threshold, security and multiplexing violations (PS-43, PS-36).
- Governance coupling: the recommended enterprise operating model requires premium licences for every active user; without budget the solution runs outside Microsoft's recommended posture (PS-33).
- Request-limit enforcement timing: designs built on transition-period limits may be throttled when strict enforcement starts (PS-19, U-1).
- Ownership and lifecycle: user-level access, 90-day inactivity suspension for non-premium flows, flows turned off after 14 days of throttling or errors (PS-34, PS-23).
- Reliability overstatement: availability-zone RPO/RTO is a rollout-dependent architecture, and 99.9% is evidenced for Dataverse only (R-04, R-05).
- Alternative comparison bias: Logic Apps positioning taken from the Logic Apps team; Power Platform ALM under-represented (R-01).
- Platform change cadence and lock-in not assessed; long-lived solutions may be under-priced (R-09).
- Tenant DLP or network policy discovered late invalidating a connector-based design (PS-29, PS-32).
- Team capability mismatch when a hybrid needs .NET/Azure skills the organisation lacks (PS-40).

## Remaining Unknowns

- Start date of strict enforcement of Power Platform request limits (U-1).
- Concurrent-user behaviour of canvas/model-driven apps; no documented ceiling (U-2, C-4).
- Number of Dataverse web servers per environment (U-3).
- Power Pages traffic and throughput ceilings (U-4).
- Current restricted Dynamics 365 tables list (U-5).
- Cross-region RTO (Microsoft publishes none) (U-6).
- Code apps roadmap: Git integration, mobile, IP restriction (U-7).
- Local-currency pricing and enterprise-agreement effects (U-8).
- Full text of Power Apps pattern pages and Power Automate planning pages (U-9, R-07).
- SOAP/legacy protocol support via custom connectors (U-10).
- Whether Managed Environments VNet support covers canvas connector calls end-to-end (U-11, C-6).
- Whether the tenant's region is already on the availability-zone architecture (R-04).
- Default tenant Dataverse database capacity: 10 GB or 20 GB (C-1).
- Self-service DR billing prerequisite: PAYG mandatory or not (C-2).
- Capacity add-on size: 10,000 or 50,000 requests/day (R-16).

## Evidence Gaps

Conclusions that a decision would need but that currently lack sufficient evidence:

- Transactional integrity: no evidence on atomicity in canvas, flows, plug-ins; no POOR/CONDITIONAL rule exists (R-02) — HIGH.
- Deployment model: SaaS-only nature and sovereign-cloud limits not documented; no rule for on-premises/air-gapped requirements (R-03) — HIGH.
- Power Automate vs Logic Apps boundary: single-sourced to the alternative's product team; Power Platform ALM/monitoring/versioning counter-evidence not gathered (R-01) — HIGH.
- Reliability: AZ architecture generalised beyond source; per-service SLAs unverified (R-04, R-05) — HIGH/MEDIUM.
- Lock-in, portability and deprecation cadence: absent (R-09) — HIGH.
- Positive-fit patterns and automation candidates: excerpt-level evidence only (R-07) — MEDIUM.
- Identity prerequisites, testing capability, reporting/document generation/localisation, online concurrency, wrap/MDM, ISV: absent (R-11, R-12, R-13, R-18, R-14, R-22) — MEDIUM/LOW.
- Cost model shape and Power Pages pack pricing: absent (R-10) — MEDIUM.
- Algorithmic-complexity boundary: one blog plus indirect corroboration; matrix states it without hedge (R-17) — MEDIUM.
- Performance: limits only, no latency or load evidence (R-24) — MEDIUM.
- Marketing statements still used as counter-evidence in C-5/PS-06 and connector counts unreconciled (R-06) — MEDIUM.

## Verdict

FAIL. The constraint, licensing and Microsoft-authored-redirect evidence is strong and would already yield useful decision criteria (criteria 2, 4, 5, 7 and 10 are met). The gate fails on criteria 3, 6, 8 and 9: several poor-fit conditions that decide real engagements (multi-system transactions, on-premises or air-gapped deployment, lock-in and platform change cadence) have no evidence at all; the principal alternative comparison is single-sourced to the alternative's own product team; two reliability claims are stated more strongly than their sources allow; and the positive-fit core rests on search excerpts. A pack synthesised from this file today would be biased in both directions: it would accept transactional or on-premises requirements it should reject, and it would push IT-owned automation to Azure on the word of the Azure team.

Required before re-gating: close R-01, R-02, R-03, R-04 and R-09 with Tier 1 evidence; re-read the pattern and planning pages behind PS-01 and PS-21 (R-07); flag C-8 (add-on size) and restate reliability findings with rollout and SLA-scope caveats. No further research area should be started until this gate passes.
