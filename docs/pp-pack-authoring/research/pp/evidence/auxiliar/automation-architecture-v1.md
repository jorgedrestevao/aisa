Research Status: DRAFT v1 (research complete; adversarial review and gate NOT yet run)
Research Confidence: MEDIUM
Gate: PENDING

# Automation Architecture — Research Evidence

Research area: **04 — Automation Architecture** (`../research-areas.md`). Also skims 05 Integration, 09 Performance and Scale, 13 Anti-Patterns, 14 Alternatives, 15 Decision Criteria without duplicating them.
Version: **2026-09-03**. Cross-references `platform-suitability.md` (VALIDATED, Gate PASS) as **PS-nn**, `application-architecture.md` (VALIDATED, Gate PASS) as **AA-nn**, and `data-architecture.md` (DRAFT v1, Gate PENDING) as **DA-nn**. These peers already cover cloud flow limits (PS-19/PS-23), plug-in timeouts (PS-09), the Service Bus event-driven pattern (PS-27), synchronous timeouts (PS-28), DLP (PS-29), Power Automate vs Logic Apps trade-off (PS-24), transactions (PS-45), concurrency (PS-46) and elastic tables (PS-57); this file cites them rather than re-deriving them, and goes deeper on RPA/desktop flows, human-in-the-loop mechanics, observability, orchestration choice, idempotency, ordering and compensation.
Source policy: `../source-policy.md`. Quotes are verbatim English. Prices are USD list where quoted.

**Purpose.** Answer, with traceable evidence: *"Given these process/integration requirements, what automation architecture should aisa consider — Power Automate cloud flows, Power Automate Desktop/RPA, business process flows, Azure Logic Apps, Azure Functions/Durable Functions, Service Bus/Event Grid, a custom service, or a hybrid — and which requirement changes the answer?"* This is not a Power Automate feature catalogue. Every finding starts from a process/automation requirement and derives the constraint and the architectural implication.

**Provenance rule.** Sources are **fetched** (page retrieved in full, `ms.date` read), **fetched-partial** (page fetched but only part of a very long page captured, e.g. the limits page's endpoint allowlist was truncated after the substantive content), **search-derived** (WebSearch tool's own synthesis of multiple snippets; treated as MEDIUM ceiling even when the underlying page is Tier 1, because the exact wording and context are not independently verified), or **T2/T3/T4** (non-Learn, per `../source-policy.md`). Kind is recorded per source in §10.

**Origin tags.** Every finding carries **Origin:** MS (Microsoft statement, fetched or search-derived) / INF (analyst inference from documented limits) / T3 (independent) / T4 (community signal) / UNKNOWN. A POOR/CONDITIONAL verdict derived by inference is phrased "treat as unsupported/unverified", never as a Microsoft statement.

**Overall confidence MEDIUM.** Reasons for the cap: (1) several high-value pages (Azure Architecture Center "choosing Logic Apps/Functions/Durable Functions/Service Bus", Dataverse plug-in-vs-flow guidance) were consulted via WebSearch synthesis rather than full fetch — cited as search-derived and capped MEDIUM; (2) RPA real-world fragility/TCO evidence leans on Tier 3/4 signals rather than Microsoft's own admission (Microsoft's RPA pages describe mitigations — self-healing selectors — more than they describe the underlying failure mode); (3) no empirical throughput/latency benchmarks exist in this corpus for cloud flows under sustained load, mirroring PS-30's gap; (4) this is a single-session draft, not yet adversarially reviewed or gated. Individual findings keep their own grade where a fetched, dated Tier 1 statement supports them (many are HIGH).

**Volatility.** Power Automate limits, performance profiles, retry defaults, RPA licensing and connector throttles are among the fastest-changing parts of Power Platform (the limits page itself changed substantially between the 2019 request-limit baseline and today, and is on a document-level `ms.date` of 2026-07-17). Treat every number in this file as valid on the fetch date in §10 and re-verify before pack encoding.

---

## 1. Classification model

| Fit class | Meaning |
|---|---|
| **STRONG** | Requirement maps to documented positioning of the technology; no documented limit approached. |
| **CONDITIONAL** | Fit depends on a measurable condition (volume, licence, duration, team skill, governance) that must be validated before commitment. |
| **POOR** | Collides with a documented hard limit, an explicit Microsoft "not the best choice" statement, or an unsupported/fragile scenario. |
| **HYBRID** | Power Automate for orchestration/human interaction/UX plus Azure or a custom service for the part that exceeds its limits — Microsoft's own "no-cliffs" pattern (PS-09). |
| **CUSTOM/OTHER** | Another technology is the documented or inferred better default for the whole requirement. |

Evidence tags: FACT, RECOMMENDATION, CONSTRAINT, TRADE-OFF, RISK, ANTI-PATTERN, DECISION CRITERION, PATTERN (per `../source-policy.md`).

---

## 2. Fit matrix — automation requirement/pattern → technology

Columns: **PA-Cloud** = Power Automate cloud flow; **PAD** = Power Automate Desktop (RPA); **LA** = Azure Logic Apps (Consumption/Standard); **Fn/DF** = Azure Functions / Durable Functions; **SB/EG** = Azure Service Bus / Event Grid / Event Hubs; **Custom** = bespoke service/backend.

| # | Requirement / pattern | PA-Cloud | PAD | LA | Fn/DF | SB/EG | Custom | Origin | Findings |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Business approval / notification workflow over M365 or Dataverse data | STRONG | n/a | CONDITIONAL | POOR (no designer, overkill) | n/a | POOR (reinvents a solved problem) | MS | AT-01, AT-19, PS-22 |
| 2 | Document-centric workflow (routing, e-signature, metadata) | STRONG | n/a | CONDITIONAL | POOR | n/a | CONDITIONAL | MS | AT-01, AT-19 |
| 3 | Dataverse record lifecycle automation (stage-gated process with UI guidance) | HYBRID (BPF + cloud flow) | n/a | n/a | n/a | n/a | n/a | MS | AT-02 |
| 4 | Simple, stable-API system-to-system sync, moderate volume | STRONG | n/a | CONDITIONAL (IT-owned, B2B) | CONDITIONAL | n/a | CONDITIONAL | MS | AT-16, PS-24 |
| 5 | No stable API; UI-only legacy application | POOR (nothing to call) | CONDITIONAL (fragile, licensed, maintenance-heavy) | n/a | n/a | n/a | STRONG if build cost justified (new API layer) | MS+T3 | AT-27–AT-31 |
| 6 | High-frequency events (sub-minute), guaranteed ordering, exactly-once effect | POOR (polling latency; no native ordering/dedup) | n/a | CONDITIONAL | CONDITIONAL (Durable) | STRONG (sessions, dedup) | CONDITIONAL | MS+INF | AT-13, AT-14, AT-33–AT-36 |
| 7 | Massive batch / nightly bulk transform | POOR (loop-per-record; ETL not its job) | n/a | CONDITIONAL | STRONG (Durable fan-out) | n/a | STRONG (ADF/dataflow) | MS | AT-08, AT-09, PS-07, PS-25 |
| 8 | Multi-step business transaction requiring all-or-nothing across systems | POOR (no native cross-system transaction) | n/a | POOR (same) | HYBRID (Durable + saga) | HYBRID (as coordinator) | HYBRID (saga/compensation) | MS+INF | AT-20–AT-24, PS-45, PS-58 |
| 9 | Long-running process with human wait states (approvals, escalation) up to 30 days | STRONG | n/a | CONDITIONAL (less native human-task tooling) | CONDITIONAL (Durable human interaction pattern, code-first) | n/a | CONDITIONAL | MS | AT-25, AT-26, PS-22 |
| 10 | Process with waits > 30 days or complex delegation/escalation trees | CONDITIONAL (persist state externally, re-trigger) | n/a | CONDITIONAL | CONDITIONAL | n/a | CONDITIONAL | MS+INF | AT-25, PS-22 |
| 11 | Private-network-only runtime, dedicated compute, local debugging, B2B/EDI | POOR/CONDITIONAL (Managed Env + VNet is partial) | n/a | STRONG (Standard) | STRONG | n/a | STRONG | MS | AT-17, PS-24, PS-32 |
| 12 | IT-owned integration estate, Git-native CI/CD, resource-level RBAC | CONDITIONAL (pipelines/Git exist but premium-gated) | n/a | STRONG | STRONG | n/a | STRONG | MS | AT-17, PS-24 |
| 13 | Attended, judgment-assisted desktop task (human present) | n/a | STRONG | n/a | n/a | n/a | n/a | MS | AT-27, AT-32 |
| 14 | Unattended, scheduled desktop automation over legacy UI at scale | n/a | CONDITIONAL (licence cost, fragility, governance) | n/a | n/a | n/a | CONDITIONAL/STRONG (build API/RPA-replacement) | MS+T3 | AT-27–AT-31 |
| 15 | Complex distributed orchestration (fan-out/fan-in, sub-orchestrations, versioned replay) | POOR (Power Fx not built for this; 500-action/8-nesting ceiling) | n/a | CONDITIONAL | STRONG (Durable Functions is purpose-built) | HYBRID (as backbone) | CONDITIONAL | MS | AT-37–AT-40, PS-08 |
| 16 | Compute-intensive processing (algorithms, iteration to convergence) | POOR | n/a | POOR | STRONG | n/a | STRONG | MS | PS-08, PS-09 |
| 17 | Continuous high-volume event streaming (telemetry, IoT, logs) | POOR | n/a | POOR | CONDITIONAL (Fn as consumer) | STRONG (Event Hubs) | STRONG | MS | AT-34, AT-36 |
| 18 | Operational observability with correlation, alerting, long retention, root-cause diagnostics | CONDITIONAL (Application Insights export is preview-grade; native UI is basic) | CONDITIONAL (action-level logs, video logs) | STRONG (Azure Monitor/App Insights native) | STRONG | STRONG | STRONG | MS | AT-41–AT-45 |
| 19 | Existing enterprise workflow engine (BPM/ERP native workflow) already covers the process | CUSTOM/OTHER (don't rebuild) | n/a | CUSTOM/OTHER | CUSTOM/OTHER | n/a | CUSTOM/OTHER | INF | cf. PS-41 |

---

## 3. Decision boundaries (requirement × condition → constraint → architectural implication)

Origin in brackets. This is the highest-value section — read before the findings.

- **Any cloud flow × > 500 actions or > 8 levels of nesting** → hard limit; the designer itself degrades before the limit is hit → split into child flows or move the orchestration to Durable Functions/Logic Apps (MS, AT-04).
- **Any cloud flow × loop over > 100,000 items (5,000 on Low profile)** → hard limit on `Apply to each`/pagination → redesign as batch/bulk API calls, or split the workload across multiple flow runs (MS, AT-04, AT-08).
- **Synchronous caller × wait > 120 seconds (inbound or outbound)** → Power Automate returns/times out regardless of business need → redesign as async (poll/webhook-callback) or move the synchronous leg to Durable Functions' async-HTTP pattern (MS, AT-04, cf. PS-28).
- **High-frequency, ordering-sensitive, or exactly-once-effect events (payments, inventory decrements, sequenced state machines)** → Power Automate has no native message ordering, deduplication, or peek-lock semantics; polling triggers replay backlog on re-enable, webhook triggers silently drop events while the flow is off → put Service Bus (sessions, dedup, peek-lock, DLQ) in front and make the flow (or a Function) an idempotent consumer (MS, AT-13, AT-14, AT-33–AT-36).
- **A process step must succeed-or-fail atomically across Dataverse + an external system/connector** → no cross-connector transaction construct exists (confirmed cross-file at PS-45); Power Automate can wrap a same-connector Dataverse change set, but never a multi-connector operation → design a saga: forward action + compensating action per step, idempotency key per step, and a persisted "in-doubt" state a human or a recovery flow can act on (MS+INF, AT-20–AT-24, PS-45, PS-58).
- **Retryable action × non-idempotent write (create without a natural key, send-once notification, external POST)** → default and custom retry policies (up to 90 attempts) can and will re-execute the action on a transient fault, producing duplicate records/emails/charges unless the action itself is idempotent (deterministic key, upsert semantics, dedup check) (MS, AT-05, AT-06, AT-18).
- **Flow consistently throttled or erroring** → turned off automatically after **14 days**; a flow untriggered for **90 days** is also suspended (exempt only for premium/capacity-licensed owners) → operational ownership must monitor for this or automation silently stops (MS, AT-04, AT-42).
- **Owner-based Power Platform request entitlement (daily requests/actions) approached** → throttling first, then 14-day shutoff; entitlement is tied to the flow **owner's licence**, not to volume alone → either assign a Process licence (stackable, 250,000 actions/day, shareable across up to 25 flows via a flow group) or move the workload off cloud flows (MS, AT-04, cf. PS-19).
- **UI-only legacy application, no accessible API, at meaningful frequency or scale** → Power Automate Desktop is the only in-platform option, but it inherits UI fragility (selector breakage on layout/version change), needs Windows infrastructure (cores, RAM, session density), premium/Process licensing per unattended bot, and secrets/credential handling discipline → treat RPA as a bridge, not an end state; prefer building or exposing an API where the legacy system's lifetime and change rate justify it (MS+T3, AT-27–AT-31).
- **Human-in-the-loop wait exceeds 30 days, or requires multi-tier conditional escalation/reassignment logic beyond a single timeout** → the flow **run duration hard limit is 30 days** (approvals included) — pending steps time out; complex escalation trees must be modeled as external state (task record + re-triggering schedule) rather than a single long-running flow (MS, AT-04, AT-25, PS-22).
- **Distributed orchestration needs fan-out/fan-in, sub-orchestrations, versioned replay, or arbitrary code control flow (loops with mutable state, recursion)** → Power Fx/cloud-flow designer is declarative and not built for this (cf. PS-08); Durable Functions is Microsoft's purpose-built code-first answer with these exact patterns (chaining, fan-out/fan-in, async HTTP APIs, human interaction, aggregator) → HYBRID: cloud flow as the business-facing front door, Durable Functions/Logic Apps Standard as the orchestration engine (MS, AT-37–AT-40).
- **Requirement for native message ordering/session state, guaranteed at-least-once delivery, or dead-lettering of poison messages** → Service Bus provides sessions, peek-lock, duplicate detection, TTL-based and max-delivery-count-based dead-lettering; Event Grid guarantees only at-least-once with no ordering; Event Hubs is for streams, not commands → pick the broker by message *type* (command → Service Bus; discrete event/fan-out → Event Grid; stream → Event Hubs), not generically "a queue" (MS, AT-33–AT-36).
- **Observability requirement includes cross-flow correlation, long-term retention beyond the rolling 30-day run history, or proactive alerting on error-rate trends** → native Power Automate analytics/run history give a 30-day rolling window and per-flow view only; Application Insights export (environment-level, preview-labelled feature name notwithstanding its GA-like guidance) and/or Dataverse `FlowRun` table extend this but require setup and, for App Insights, an Azure subscription outside the Power Platform admin surface → CONDITIONAL on operational investment; do not assume out-of-the-box enterprise observability (MS, AT-41–AT-45).
- **Owner leaves the organization / flow ownership is ad hoc** → a flow reverts to the Low performance profile if its owner's licence lapses or the owner leaves, silently cutting its throughput ceiling → operational ownership and licence assignment are architecture decisions, not afterthoughts (MS, AT-04).
- **Polling-trigger flow turned off for an extended period, then re-enabled** → all backlog fires at once, causing delay/throttling spikes at reactivation; a webhook-trigger flow in the same situation silently drops events that occurred while off → neither is "safe by default"; both must be paired with an explicit idempotency/backfill strategy for outage recovery (MS, AT-14, AT-15).
- **A single-connector high-volume write path (e.g., thousands of Dataverse creates) implemented as a per-record loop** → documented anti-pattern; Microsoft's own remedy is CreateMultiple/bulk operations or batch requests, not "buy more licence" (MS, AT-08, AT-09, PS-25).

---

## 4. Findings

### 4.1 Cloud flow trigger types and process characteristics

#### AT-01 — Power Automate's three trigger shapes (automated/event, instant/manual, scheduled) map directly onto three different automation-architecture roles; business process flows are a fourth, non-automation mechanism for guided human process, not a flow type
- **Classification:** PATTERN
- **Evidence:** "An automated cloud flow is initiated based on some event... Schedule flows for repeating and timed operations and use automated flows for reactive activities... if a connector provides an event-based trigger, prefer it over repeatedly checking the same data with a scheduled flow when real-time processing is required" (search-derived from Microsoft Learn "Triggers" and community sources, S-14). Business process flows: "not 'flows' in the automation sense... provide a stage-driven guidance bar inside model-driven apps... Think of BPFs as rails for human workflows, often paired with cloud flows to automate the system-side actions" (search-derived, S-15).
- **Why it matters:** Conflating a guided human process (BPF) with system automation (cloud flow) leads to designs that try to make a BPF do integration work, or a cloud flow do UX guidance, neither of which it is built for.
- **Decision impact:** Guided multi-stage data entry inside a model-driven app → business process flow (STRONG, Dataverse-only). System-to-system or notification automation → cloud flow, trigger type chosen by whether the source can push an event.
- **Confidence:** MEDIUM (search-derived; not independently fetched from a single canonical page).
- **Sources:** S-14, S-15.

#### AT-02 — A business process flow provides no automation on its own; it is commonly paired with cloud flows triggered on stage change
- **Classification:** PATTERN
- **Evidence:** "A sales team can use business process flows to follow a clear set of steps from lead qualification to deal closure, ensuring nothing is missed... Triggering downstream automation when stage changes occur" (search-derived, S-15).
- **Decision impact:** Stage-gated Dataverse processes with both a human-guidance need and system-side automation need → HYBRID (BPF + cloud flow), not either alone.
- **Confidence:** MEDIUM.
- **Sources:** S-15.

#### AT-03 — Cloud flow performance profile (Low/Medium/High/Unlimited Extended) is a function of the flow **owner's** licence, not of the flow's design, and determines its throughput ceiling
- **Classification:** CONSTRAINT
- **Evidence:** "A flow's performance profile determines its Power Platform request limits... A cloud flow uses the plan of its owner... If the original owner leaves the organization, the flow reverts to the Low performance profile." Profiles: Low = Free/M365/Power Apps Plan 1/Per App/Power Automate Plan 1/trials; Medium = Power Apps Plan 2/per-user, Power Automate Plan 2/Premium, Dynamics 365 Enterprise/Professional; High = Power Automate Process licence, per-flow plan; Unlimited Extended = pay-as-you-go flows, Dynamics in-context flows under a service principal. "For cloud flows with a Process license, you can stack multiple Process licenses on a single cloud flow... Each additional license adds 250,000 actions per day... Alternatively, you can share a single Process license across up to 25 flows by using a flow group. Stacking isn't available for flow groups" (MS, S-01, ms.date 2026-07-17).
- **Why it matters:** The same flow definition can silently change throughput class if its owner's licence or employment status changes — an operational/governance risk, not just a technical one.
- **Decision impact:** High-volume or business-critical automation → assign Process/capacity licensing deliberately and document ownership; do not let throughput depend on an individual's personal licence.
- **Confidence:** HIGH.
- **Sources:** S-01.

### 4.2 Execution limits and throttling

#### AT-04 — Cloud flow hard limits (structural, duration, concurrency, throughput, retry) are extensively documented and version-dated; they are the primary POOR-fit trigger for "add Azure" decisions
- **Classification:** CONSTRAINT
- **Evidence (all MS, S-01, ms.date 2026-07-17):**
  - Structural: "Actions per workflow: 500... Allowed nesting depth for actions: 8... Variables per workflow: 250."
  - Duration/retention: "Run duration: 30 days... includes flows with pending steps like approvals. After 30 days, any pending steps time out." "Run retention in storage: 30 days." "Minimum recurrence interval: 60 seconds... Maximum recurrence interval: 500 days."
  - Retention/shutoff: "Flows with errors: 14 days — A cloud flow that has a trigger or actions that fail continuously is turned off." "Flows without trigger activity: 90 days... Flows owned by users with premium licenses or assigned capacity licenses... aren't subject to this suspension." "Consistently throttled flows: 14 days — Assign Power Automate Process licenses to the flow to dedicate capacity and avoid throttling."
  - Concurrency/looping: "Concurrent runs: Unlimited for flows with Concurrency Control turned off; 1 to 100 when Concurrency Control is turned on (defaults to 25)." "Apply to each array item: 5,000 for Low, 100,000 for all others." "Apply to each concurrency: 1 is the default limit... between 1 and 50." "Until iterations: Default 60, Maximum 5,000."
  - Throughput: "Power platform requests per 5 minutes: 100,000." "Power platform requests per 24 hours: 10,000 for Low; 200,000 for Medium; 500,000 for High; 10,000,000 for Unlimited Extended... Distribute the workload across more than one flow as necessary." "Concurrent outbound calls: 500 for Low; 2,500 for all others." Content throughput: "200 MB for Low; 2 GB for Medium; 10 GB for High" per 24 hours.
  - Request/message: "Outbound synchronous request: 120 seconds (2 minutes)... For longer-running operations, use an asynchronous polling pattern or an 'Until' loop." "Inbound request: 120 seconds (2 minutes)." "Message size: 100 MB... with chunking: 1 GB."
  - Retry: default policy is "up to two retries at exponentially increasing intervals... up to an interval of approximately 10 minutes" (Low) or "up to 12 retries... up to an interval of approximately 1 hour" (Medium/High); configurable up to "Retry attempts: 90, Retry maximum delay: One (1) day, Retry minimum delay: Five (5) seconds."
  - Custom connectors: "Number of custom connectors: 50 per user... 500 requests per minute per connection."
- **Why it matters:** This is the single densest, most decision-relevant limits table in the corpus for this area; almost every other finding in this file either cites or is bounded by it.
- **Decision impact:** Any one of these limits being structurally necessary for the use case (not just "might be nice") is a POOR-fit signal for that component of the design → HYBRID with Logic Apps/Durable Functions/Service Bus, or split into multiple flows/child flows.
- **Conditions:** Content-throughput and request numbers were substantially different during the pre-2021 "transition period" quoted on the same page; treat the transition-period column as historical context, not current guidance.
- **Confidence:** HIGH.
- **Sources:** S-01.

#### AT-05 — Retry policy is configurable per action, defaults to exponential backoff, and explicitly handles HTTP 408/429/5xx — but retries interact dangerously with non-idempotent actions and with nested retry layers
- **Classification:** CONSTRAINT + RISK
- **Evidence:** "Power Automate has a feature to set up policies that automatically retry an action if it fails, with a default setting of four retries... Exponential backoff automatically increases the delay between retries... the retry policy handles HTTP status codes 408, 429 and 5xx responses" (search-derived, S-02). Retry attempt/delay ceilings per AT-04 (MS, S-01). Well-Architected guidance: "In most cases, avoid implementations that include duplicated layers of retry code... If you implement retry with a count of three on both calls, there are nine retry attempts in total against the service... Never implement an endless retry mechanism... Never perform an immediate retry more than once" (MS, S-04, ms.date 2025-08-18).
- **Why it matters:** Retries are Power Automate's primary reliability mechanism, but layered retries (connector-level + custom + a caller's own retry) multiply load on the downstream system exactly when it is already struggling.
- **Decision impact:** Design retry at one layer only per call chain; prefer the connector's/action's built-in policy unless a specific reason exists to override it (MS, AT-06).
- **Confidence:** HIGH (Well-Architected quote fetched in full); MEDIUM (search-derived default-count figure — the "four retries" figure in the search summary was not independently confirmed against a fetched page and may not match the Low/Medium/High table in AT-04, which is the authoritative source).
- **Sources:** S-02, S-04, S-01.

#### AT-06 — Well-Architected guidance is explicit that retrying a non-idempotent operation can corrupt data, and that retry scope (single action vs. multi-step) determines whether idempotency is even the right question
- **Classification:** RISK
- **Evidence:** "Consider whether retrying the same operation could cause inconsistencies in data. If some parts of a multistep process are repeated and the operations aren't idempotent, inconsistencies might occur. For example, if an operation that inserts a record into Microsoft Dataverse is repeated, it might cause incorrect values in the table. Or, if you repeat an operation that sends a notification to the user, they might receive duplicate messages. Consider the scope of operations that are retried... it might result in idempotency issues or unnecessary rollback operations" (MS, S-04, ms.date 2025-08-18). "There's no point in retrying operations that attempt an invalid operation, like updating a row in Microsoft Dataverse that doesn't exist or that the user doesn't have permission to" (same source).
- **Why it matters:** This is Microsoft's own explicit acknowledgement that automatic retry — a feature the platform enables by default in many cases — is a source of duplicate-record and duplicate-notification bugs unless the maker designs for it.
- **Decision impact:** Every create/insert/send action inside a flow that can be retried (which is most of them) needs either a natural/business key with upsert semantics, an idempotency-key check ("has this already been processed"), or an explicit acceptance of the duplicate risk.
- **Confidence:** HIGH.
- **Sources:** S-04.

#### AT-07 — "Configure run after" (success/failure/timeout/skipped) plus scopes is Power Automate's structural error-handling primitive; it exists but must be explicitly designed in, it is not the default flow behaviour
- **Classification:** PATTERN
- **Evidence:** "By default an action only runs after the previous action succeeds. Configure run after lets you change that, so an action can run after the previous one fails, times out, or is skipped... Error and exception handling in cloud flows can be configured using scopes and run-after settings" (search-derived, S-03, S-05). Microsoft training module referenced: "Best practices for error handling in Power Automate flows" (S-05).
- **Why it matters:** Without deliberate run-after/scope design, a flow that fails partway leaves no compensating action and no notification — silent partial failure.
- **Decision impact:** Any flow with more than a trivial number of actions should wrap risk-bearing sections in a Scope with a paired "run after has failed/timed out" error-handling Scope (try/catch/finally equivalent).
- **Confidence:** MEDIUM (search-derived).
- **Sources:** S-03, S-05.

### 4.3 Good-fit patterns

#### AT-08 — Microsoft's own anti-pattern guidance doubles as its good-fit guidance: cloud flows are the right layer for orchestration and light-to-moderate volume, and ETL/bulk work should be handed to dataflows or Dataverse bulk operations
- **Classification:** RECOMMENDATION
- **Evidence:** "When you're working with large-scale data transformations, consider whether the task should be handled as an extract, transform, load (ETL) process... Dataflows handle large volumes of data efficiently and provide better performance for ETL tasks than cloud flows do... To manage data load with orchestration logic in cloud flows, combine cloud flows with dataflows" — trigger the dataflow refresh from a cloud flow, then react to "When a dataflow refresh completes" (MS, S-06, ms.date 2025-07-10, fetched in full). "If you need to create or update thousands of records in a data source, don't use a For each loop to process each record sequentially... Batch operations: group multiple operations into a single HTTP request... Parallelism in the For each loop: configure... to process up to 50 records in parallel... Bulk operations are posted and executed as a single operation. The entire bulk request is counted as one operation, which can significantly reduce the number of actions" (MS, S-06). Bulk via `CreateMultiple` Web API cited as replacing "100 Create Row actions... with just one action."
- **Why it matters:** This reframes "Power Automate can't do high volume" into a more precise statement: cloud flows can *initiate and orchestrate* high-volume work, but the volume processing itself belongs in dataflows, bulk/batch APIs, or a downstream service.
- **Decision impact:** Good-fit pattern: cloud flow as the trigger/orchestrator + dataflow or bulk Web API as the workhorse. Poor-fit pattern: cloud flow doing the per-record work itself (§4.4, §4.13).
- **Confidence:** HIGH.
- **Sources:** S-06.

#### AT-09 — OData query expansion collapses a documented anti-pattern (nested loops calling a related table) into a single efficient call — a concrete good-fit technique for moderate-volume Dataverse automation
- **Classification:** PATTERN
- **Evidence:** "Instead, use OData query expansion to replace the nested loop with a single For each loop. This approach reduces the total number of requests to Dataverse to just one RetrieveMultiple call. Use the Expand Query parameter to specify the name of the lookup column... Use the $select parameter to limit the columns returned... Use the Filter Rows parameter to apply conditions directly on the lookup table's columns" (MS, S-06, ms.date 2025-07-10).
- **Decision impact:** Parent/child Dataverse relationships processed in bulk → prefer `$expand`/`$select`/`$filter` on a single retrieve over nested `For each`.
- **Confidence:** HIGH.
- **Sources:** S-06.

#### AT-10 — Trigger conditions and OData filters let a flow avoid running at all for irrelevant events, which is Microsoft's primary documented technique for keeping a high-frequency source (e.g. every Dataverse row change) within throughput limits
- **Classification:** RECOMMENDATION
- **Evidence:** "If you don't want your flows to run every time they're triggered, set them to execute only when a specific condition is met... Use the OData filter property to define precise conditions for when a flow should be triggered based on changes in Dataverse data" (MS, S-07, ms.date 2025-07-11, fetched in full).
- **Decision impact:** Any event-driven flow on a busy table/mailbox should have a trigger condition before performance tuning is attempted anywhere else in the flow.
- **Confidence:** HIGH.
- **Sources:** S-07.

#### AT-11 — Trigger concurrency control exists to prevent duplicate-processing "dirty reads" and to bound simultaneous runs, but Microsoft flags it as an irreversible, use-cautiously setting, not a default-on best practice
- **Classification:** TRADE-OFF
- **Evidence:** "By default, a cloud flow trigger executes as many runs as possible simultaneously when its conditions are met... if your flow reads a record and then updates it but the update fails, the flow might have already acted on the old data, leading to inconsistencies. This situation is known as a dirty read... Concurrency control is irreversible. Once applied, concurrency control settings can't be undone. To remove concurrency control, you need to create a new flow... As a best practice, leave the concurrency control at its default setting. If you need to apply concurrency control, consider doing so on a flow with the least number of actions... organize actions that require concurrency control into a dedicated child flow" (MS, S-07, ms.date 2025-07-11).
- **Why it matters:** This directly informs the ordering/consistency decision boundary (§3): concurrency control is the in-platform tool for order-sensitive processing, but it is a one-way door architecturally.
- **Decision impact:** Order-sensitive single-record processing → concurrency control degree-of-parallelism = 1, isolated to a small child flow. High-throughput independent-record processing → leave default (unlimited/high parallelism).
- **Confidence:** HIGH.
- **Sources:** S-07.

#### AT-12 — Approvals, with manual reassignment, timeout-based escalation, and calendar/out-of-office-aware delegation, are a mature, well-documented human-in-the-loop pattern within the 30-day run-duration ceiling
- See §4.8 (AT-25, AT-26) — cross-referenced here as a good-fit pattern for §4.3.

### 4.4 Poor-fit patterns and alternatives

#### AT-13 — Polling triggers replay their entire backlog when a flow is re-enabled after being off; webhook triggers silently drop events that occurred while off — neither is safe by default for high-frequency or loss-sensitive sources
- **Classification:** CONSTRAINT + RISK
- **Evidence:** "After it's registered, a polling trigger checks the connected service periodically. When the flow is turned off, the trigger stops polling the service but isn't deregistered. When the flow is turned back on, the trigger picks up where it left off, polling the service for new events since the last poll. This behavior ensures that no data is missed... However, if a large number of events occurred while the flow was off, they're all processed when the flow is turned on again, possibly leading to delays and performance issues." "Webhook triggers register with the service to receive notifications when specific events occur. When the flow is turned off, the trigger doesn't receive notifications of new events. When the flow is turned back on, it processes only new events that occur from that point forward. If any events occurred while the flow was off, they're not processed... you might miss some events if the flow is turned off for an extended period of time" (MS, S-07, ms.date 2025-07-11, fetched in full).
- **Why it matters:** This is a structural gap for exactly-once/ordering requirements: the platform's two trigger mechanisms fail in opposite directions (backlog flood vs. silent loss), and neither guarantees processing order across the outage boundary.
- **Decision impact:** Loss-sensitive or order-sensitive high-frequency sources → do not rely on either trigger type's outage behaviour; put a durable broker (Service Bus) upstream, or design explicit reconciliation/backfill logic.
- **Confidence:** HIGH.
- **Sources:** S-07.

#### AT-14 — Power Automate has no native message ordering, deduplication, peek-lock, or session concept; these exist only in a message broker in front of it
- **Classification:** CONSTRAINT
- **Evidence:** Service Bus: "Service Bus queues use sessions to provide ordered delivery... provide a built-in deduping capability that detects and removes duplicate messages... uses a peek-lock mechanism. When a consumer retrieves a message, Service Bus locks it temporarily" (MS, S-11, ms.date 2026-02-11, fetched in full). By contrast, nothing in the cloud flow limits or trigger documentation (S-01, S-07) describes any equivalent mechanism inside Power Automate itself.
- **Why it matters:** "Just add a queue" is not automatically true — Power Automate becomes the *consumer* of the broker's guarantees; it does not gain ordering/dedup on its own trigger.
- **Decision impact:** Ordering/dedup/exactly-once-effect requirements → Service Bus (or equivalent) upstream, with the flow/Function as an idempotent consumer of already-ordered, already-deduplicated messages.
- **Confidence:** HIGH (Service Bus facts) / INF (absence claim for Power Automate — no fetched Microsoft page states this negatively; it is inferred from the limits and trigger pages not describing such a mechanism). Treat the absence claim as unverified until a direct Microsoft statement is found (see U-04).
- **Sources:** S-11, S-01, S-07.

#### AT-15 — Documented cloud-flow anti-patterns are exactly the high-volume/complex-logic scenarios where Power Automate is a poor fit: nested loops, self-triggering loops, large-scale data transformation, and per-record loops for bulk writes
- **Classification:** ANTI-PATTERN
- **Evidence:** "Nested For each loops can be resource-intensive... if you have two loops that each have 10 iterations, the total number of iterations is 10 x 10 = 100... They can exceed limits and quotas... They can degrade performance." "Cloud flows can trigger themselves, creating an infinite loop... Power Automate warns you... 'Actions in this flow may result in an infinite trigger loop...'" Remedies: trigger conditions, and a `Terminate` action as a safeguard. "When you're working with large-scale data transformations, consider whether the task should be handled as an ETL process." "If you need to create or update thousands of records... don't use a For each loop to process each record sequentially" (all MS, S-06, ms.date 2025-07-10, fetched in full).
- **Decision impact:** These four patterns are the concrete, evidence-backed anti-pattern list for §4.13 rather than generic "avoid complexity" advice.
- **Confidence:** HIGH.
- **Sources:** S-06.

#### AT-16 — Power Automate vs. Logic Apps is a trade-off on ownership model, network posture, tooling maturity and B2B/EDI needs — not simply on volume; PS-24 already establishes this in full and should be read as the primary reference
- **Classification:** TRADE-OFF (cross-reference)
- **Evidence:** See PS-24 in full: vendor-authored comparisons overstate Power Automate's monitoring/versioning gaps relative to current Power Platform capability (pipelines, Git integration, App Insights export), but Logic Apps Standard remains the documented choice for private-network runtime, dedicated compute, code-first local debugging, and B2B/EDI (Enterprise Integration Pack). Independent confirmation here: "Power Automate empowers business users, office workers, and citizen developers to build simple integrations without having to work with IT or developers or to write code... Azure Logic Apps supports integrations ranging from little-to-no-code scenarios to more advanced, codeful, and complex workflows. Examples include B2B processes" (MS, S-10, ms.date 2026-03-23, fetched in full).
- **Decision impact:** Do not re-derive this trade-off from volume alone; use PS-24's decision impact directly, and treat AT-37–AT-40 (orchestration) as the deeper layer beneath it.
- **Confidence:** HIGH.
- **Sources:** S-10; PS-24 (and its sources S-09, S-08, S-60, S-48b, S-62–S-65, S-04, S-39).

#### AT-17 — Azure Functions/Logic Apps/Power Automate/WebJobs "can all define input, actions, conditions, and output" and are explicitly designed to be combined rather than treated as exclusive choices
- **Classification:** PATTERN
- **Evidence:** "All of these services can solve integration problems and automate business processes... A Power Automate flow can call an Azure Logic Apps workflow. An Azure Logic Apps workflow can call a function in Azure Functions, and vice versa... You don't have to choose just one of these services. They integrate with each other and with external services" (MS, S-09, ms.date 2026-03-23, fetched in full). Durable Functions vs. Logic Apps comparison table (same page): Durable Functions = "Development: Code-first (imperative)"; Logic Apps = "Development: Designer-first (declarative)"; Logic Apps has "1,400+ prebuilt connectors" vs. Durable Functions' "dozen built-in binding types... write code for custom bindings."
- **Why it matters:** Reframes the automation-architecture decision as "which layer handles which part," not "which single product wins."
- **Decision impact:** A single business process commonly spans: cloud flow (business-facing trigger/approval) → Logic Apps or Durable Functions (complex orchestration) → Functions (custom compute) → Service Bus/Event Grid (decoupling). This is the expected HYBRID shape, not an exception.
- **Confidence:** HIGH.
- **Sources:** S-09.

### 4.5 Integration patterns

#### AT-18 — Commands (must reach the consumer, at-least-once, must not double-process) and events (fire-and-forget, may have zero-to-many subscribers) are architecturally different message types and should not use the same broker choice by default
- **Classification:** DECISION CRITERION
- **Evidence:** "A command is a message that requests a specific action from the consumer... A command must be delivered at least once. If a command doesn't reach its destination, the entire business transaction might fail... consumers shouldn't process a command more than one time. Duplicate processing can cause erroneous transactions, like duplicate orders or double billing." "An event is a message that a producer raises to announce that something happened... has no expectation that the event will result in any specific action... Events can have multiple subscribers or no subscribers at all" (MS, S-11, ms.date 2026-02-11, fetched in full).
- **Decision impact:** A cloud flow (or Function) acting on a *command* (e.g., "charge this invoice") needs the guaranteed-delivery, dedup, ordering machinery of Service Bus. A cloud flow reacting to a *discrete event* (e.g., "a file arrived") is well served by Event Grid's push model. A flow consuming a *stream* (telemetry) is the wrong tool full stop — that is Event Hubs' + Stream Analytics' job.
- **Confidence:** HIGH.
- **Sources:** S-11.

#### AT-19 — Standard connectors wrap REST APIs (synchronous request/response by construction); Power Automate's integration strength is many pre-built synchronous connectors, its weakness is that this synchronous-call model does not natively express asynchronous, queued, or streaming integration without a broker in front
- **Classification:** PATTERN (cross-reference)
- **Evidence:** See PS-26 in full for connector/custom-connector/gateway constraints (500 requests/min per connection, 50 custom connectors per user, premium licensing for on-prem/custom). This file adds: Event Grid pull-delivery exists specifically for consumers "with intermittent availability that prevents reliable real-time push delivery" or "network restrictions that require a private link" or that "can't expose a push notification endpoint" (MS, S-11) — a documented accommodation for exactly the kind of network-constrained consumer a Power Automate flow behind a corporate firewall might be.
- **Decision impact:** Real-time push integration with a well-connected system → connector/webhook (STRONG). Integration with an intermittently available or network-restricted consumer → pull-based polling or Event Grid pull delivery, accepting latency.
- **Confidence:** HIGH (Service Bus/Event Grid facts) / cross-ref PS-26 for connector limits.
- **Sources:** S-11; PS-26.

#### AT-20 — Service Bus dead-letter queues formalize "poison message" and "expired message" handling with concrete mechanisms (MaxDeliveryCount, TTL) — a documented pattern Power Automate itself has no equivalent of natively
- **Classification:** PATTERN
- **Evidence:** "A Service Bus queue has a default subqueue, called the dead-letter queue (DLQ), to hold messages that Service Bus can't deliver or that consumers can't process... A poison message is a message that the consumer can't handle because it's malformed or contains unexpected information. To detect poison messages... set the MaxDeliveryCount property... Service Bus queues let the producer post messages with a time-to-live (TTL) attribute. If this period expires before a consumer receives the message, Service Bus places the message in the DLQ" (MS, S-11, ms.date 2026-02-11, fetched in full).
- **Why it matters:** This is the concrete mechanism behind the brief's "dead-letter patterns" sub-area; Power Automate's own failure handling (run-history error state, 14-day auto-off) is a coarser, flow-level equivalent, not a message-level one.
- **Decision impact:** High-volume integration with a non-trivial poison-message rate → put Service Bus (or equivalent) in front so bad messages are isolated per-message rather than surfacing as whole-flow failures.
- **Confidence:** HIGH.
- **Sources:** S-11.

#### AT-21 — Checkpointing (Service Bus session state) is the documented mechanism for resuming a long-running, multi-message business transaction after a consumer failure — a pattern with no native Power Automate equivalent beyond the flow's own run-history retry
- **Classification:** PATTERN
- **Evidence:** "Business transactions can run for a long time. Each operation in the transaction can have multiple messages. Use checkpointing to coordinate the workflow and provide resiliency if a transaction fails. Service Bus queues support checkpointing through the session state capability... a consumer can track progress by periodically calling GetSessionStateAsync... If a consumer fails, another consumer can use the state information to determine the last known checkpoint and resume the session" (MS, S-11, ms.date 2026-02-11).
- **Decision impact:** Long multi-step transactions with resumability requirements beyond a single flow run → Service Bus session state, or Durable Functions' checkpointed orchestrator state (AT-38), not a bare cloud flow.
- **Confidence:** HIGH.
- **Sources:** S-11.

### 4.6 High-volume automation

#### AT-22 — Batch (grouped-but-independent) and bulk (grouped-and-atomic-as-one-operation) are documented as two distinct high-volume write strategies with different failure semantics, and Power Automate is guided toward both over per-record loops
- **Classification:** PATTERN (cross-reference)
- **Evidence:** See AT-08 above (S-06) for the full quote distinguishing batch ("processed separately... if one operation fails, it doesn't affect the others... increased overhead and latency") from bulk ("posted and executed as a single operation... counted as one operation"). Bulk Web API access requires either direct HTTP calls "authenticated with Microsoft Entra ID" or "the HTTP connector in Power Automate with service principals" (MS, S-06).
- **Decision impact:** Independent-record high-volume writes where partial success is acceptable → batch. All-or-nothing high-volume writes within Dataverse → bulk/CreateMultiple or a change set (cf. PS-45).
- **Confidence:** HIGH.
- **Sources:** S-06.

#### AT-23 — Queue-based load leveling and the competing-consumers pattern are Microsoft's documented answers to "back-pressure" and "retry storms," implemented at the broker layer, not inside a cloud flow
- **Classification:** PATTERN
- **Evidence:** "Producers generate varying message volumes that can spike suddenly. Rather than adding consumers to handle the extra load, a message broker buffers the messages. Consumers then process messages at a manageable rate without overloading the system" (Queue-Based Load Leveling). "Producers can post a large number of messages for multiple consumers to process. Use a message broker to distribute processing across servers and improve throughput... You can dynamically add or remove consumers to scale the system as needed" (Competing Consumers pattern) (MS, S-11, ms.date 2026-02-11).
- **Why it matters:** This directly answers the brief's "back-pressure" and "retry storm" sub-points: the architectural remedy is decoupling via a broker with independently scalable consumers, not tuning retry counts inside the automation tool.
- **Decision impact:** Bursty, high-volume producer (e.g., a batch upload, an IoT spike) feeding an automation pipeline → insert a queue between producer and the flow/Function so the consumer processes at a sustainable rate.
- **Confidence:** HIGH.
- **Sources:** S-11.

#### AT-24 — Trigger concurrency and "Apply to each" concurrency are the two in-flow parallelism controls, and Microsoft's own guidance is to leave the more consequential one (trigger concurrency) at its default and confine deliberate parallelism to a small, isolated child flow
- **Classification:** RECOMMENDATION (cross-reference)
- **Evidence:** See AT-11 (S-07) in full. Complements AT-04's `Apply to each` concurrency ceiling (default 1, configurable 1–50) (MS, S-01).
- **Decision impact:** High-volume independent-record processing inside a single flow run → raise `Apply to each` concurrency (bounded at 50) before reaching for trigger concurrency control, which is irreversible.
- **Confidence:** HIGH.
- **Sources:** S-07, S-01.

### 4.7 Business transactions

#### AT-25 — Cross-system/cross-connector transactional guarantees do not exist in Power Automate; PS-45 and PS-58 already establish the Dataverse-internal boundary and the compensating-transaction remedy in full — this file adds the messaging-layer mechanics that implement that remedy
- **Classification:** CONSTRAINT (cross-reference + extension)
- **Evidence:** PS-45: atomicity exists only inside Dataverse via change sets/`ExecuteTransactionRequest`/synchronous plug-in pipeline; "The Apply to each action isn't supported in a changeset"; canvas `Patch` and cross-connector flows are not transactional. PS-58 (Azure Architecture Center, via PS): compensating transactions are the documented remedy when atomic transactions aren't possible, but "It's not easy to generalize compensation logic. A compensating transaction is application specific," and it is unsuitable when "The system can't tolerate temporary inconsistency." This file's addition: Service Bus session state / checkpointing (AT-21) and dead-lettering (AT-20) are the concrete mechanisms that make a saga's "in-doubt" state observable and recoverable rather than merely a design idea (MS, S-11).
- **Why it matters:** A saga is not "compensating actions in a flow" alone — it needs a durable record of which step succeeded/failed/is pending, which a bare cloud flow's ephemeral run state does not provide once the run itself has ended or timed out.
- **Decision impact:** Multi-system business transaction with partial-failure risk → (1) confirm the transaction cannot be kept entirely inside Dataverse (PS-45's CONDITIONAL path); if it cannot, (2) design a saga with per-step idempotency keys, compensating actions, and a durable state store (Service Bus session state, a Dataverse "transaction ledger" table, or Durable Functions orchestrator state) that a human or recovery process can inspect and act on when compensation itself fails.
- **Confidence:** HIGH (PS-45/PS-58 facts) / MEDIUM (this file's synthesis connecting them to Service Bus mechanics).
- **Sources:** PS-45, PS-58, S-11.

#### AT-26 — Eventual consistency is the default outcome of any multi-system automation that is not entirely inside one Dataverse transaction boundary, and DA-52's "at-least-once + idempotency, never a synchronous webhook for side effects" rule applies equally to Power Automate-authored integrations
- **Classification:** DECISION CRITERION (cross-reference)
- **Evidence:** DA (data-architecture.md, DRAFT v1) §3 decision boundary: "Writes toward the system of record → at-least-once delivery + idempotency (alternate key on the external id); never a synchronous webhook for side effects ('the request sent to the configured endpoint can't be recalled'); one retry owner, exponential backoff, Retry-After honoured (MS, DA-50, DA-52, DA-53)."
- **Decision impact:** Business stakeholders who expect "real-time, always-consistent" cross-system automation from Power Automate need this expectation corrected explicitly during Discovery; the honest default is "eventually consistent, with a defined reconciliation path," not "instant and guaranteed."
- **Confidence:** HIGH (inherited from DA, itself DRAFT — carries DA's own confidence caveat).
- **Sources:** DA-50, DA-52, DA-53 (data-architecture.md).

### 4.8 Human-in-the-loop

#### AT-27 — Approvals support manual reassignment, timeout-based automatic escalation, calendar/out-of-office-aware delegation, and chained multi-tier escalation — a mature pattern, but every mechanism described is community/Tier-3-documented rather than confirmed on a single fetched Microsoft reference page
- **Classification:** PATTERN
- **Evidence:** "The approvals engine allows assignees to manually reassign their active task to another qualified user if they cannot make the decision, and process owners can toggle the 'Enable reassignment' feature on or off... If an approver does not respond within a set timeout (e.g., 24 or 48 hours), Power Automate automatically reassigns the request... Flows can check an approver's out-of-office status or calendar before routing, automatically redirecting the request to a pre-defined delegate or manager if the primary reviewer is unavailable. Timeouts can be chained to create multi-tier escalation paths for high-risk workflows" (search-derived, S-12).
- **Why it matters:** The pattern is real and widely used, but the specific mechanics (what "timeout" means precisely, what "Enable reassignment" toggle is called in-product) should be verified against the Approvals connector reference before being encoded as pack guidance.
- **Decision impact:** Approval-driven processes with escalation/delegation needs → STRONG fit, subject to the 30-day run-duration ceiling (PS-22) and a UNKNOWN flag on exact configuration mechanics (see U-01).
- **Confidence:** MEDIUM (search-derived, not independently fetched).
- **Sources:** S-12.

#### AT-28 — Cancellation, rejection, and auditability of approvals are implied by the Approvals connector and Dataverse run-history/audit surfaces but were not independently confirmed with a fetched, verbatim Microsoft statement in this research pass
- **Classification:** UNKNOWN (partial)
- **Evidence:** No fetched source in this pass produced a verbatim Microsoft statement on approval-specific audit trail retention distinct from general flow run-history (AT-42–AT-45) and Dataverse auditing (cross-reference PS-31, DA-16 for Dataverse audit trail mechanics generally).
- **Decision impact:** Do not assert approval-specific audit guarantees beyond what PS-31/DA-16 already establish for Dataverse auditing in general; treat approval-decision audit trail as "as strong as the surrounding Dataverse/flow-run audit configuration," not as an intrinsically stronger guarantee.
- **Confidence:** LOW / UNKNOWN.
- **Sources:** — (gap; see U-01).

### 4.9 RPA / Power Automate Desktop

#### AT-29 — Power Automate Desktop has concrete, documented hardware/OS/licensing prerequisites that scale non-trivially for unattended and multi-session (high-density) deployment
- **Classification:** CONSTRAINT
- **Evidence:** "Processor: 1.00 GHz or faster with two or more cores. For unattended mode, four or more cores are needed... Minimum RAM: 2 GB... Recommended: 4 GB." Supported OS: "Windows 10 (Home, Pro, Enterprise), Windows 11 (Home, Pro, Enterprise), Windows Server 2016, 2019, 2022, or 2025 (devices with ARM processors aren't supported)." "If your device runs Windows 10 Home or Windows 11 Home, you can use Power Automate to create desktop flows and monitor them... However, you can't trigger desktop flows from the cloud." Multi-session (high-density): "Basic requirements for the first user session: CPU 4 cores, RAM 4 GB, Storage 2 GB. Per additional user session: CPU 2 cores, RAM 4 GB... You need a DSL-range internet (not LAN) bandwidth to function properly." "Desktop flows in v1 schema environments can't exceed 100 MB in size." "The number of actions that can be logged in a single desktop flow run is limited to 10,000. Extra actions are performed but aren't logged" (MS, S-13, ms.date 2026-03-24, fetched in full).
- **Why it matters:** RPA is frequently proposed as a "quick win" with no infrastructure cost; it in fact requires dedicated, licensed, provisioned Windows compute that scales per concurrent bot, not per flow.
- **Decision impact:** Any RPA proposal must include a machine/VM sizing and OS-licensing line item, not just a Power Automate licence line.
- **Confidence:** HIGH.
- **Sources:** S-13.

#### AT-30 — Unattended RPA requires a separate Process (or Hosted Process) licence per concurrent bot, priced per bot/month, independent of and in addition to per-user premium licensing for attended RPA
- **Classification:** CONSTRAINT
- **Evidence:** "Attended RPA is included under the Premium per-user license... Unattended RPA requires a separate Process license... or a Hosted Process license... The Process license fees the automation itself rather than the users, so a single shared workflow can serve unlimited users under one license... Each simultaneous unattended process needs its own bot license, so four parallel processes mean four separate licenses" (search-derived from Power Platform licensing FAQ and pricing pages, S-16). Cross-reference PS-19/PS-23 Process-licence stacking mechanics (per-flow, not per-bot, in the cloud-flow context) — the RPA "per bot" unit is a distinct licensing dimension from the cloud-flow "per flow" Process stacking.
- **Why it matters:** TCO scales with concurrency (number of simultaneous bots), not with the number of processes automated or records processed — a very different cost driver than cloud flow request-based entitlements.
- **Decision impact:** Unattended RPA at scale (many parallel bots) → cost model must be built per-concurrent-bot, and compared explicitly against the cost/effort of exposing an API instead.
- **Confidence:** MEDIUM (search-derived pricing; treat exact $ figures as volatile and unverified against a currently fetched licensing guide page — see U-02).
- **Sources:** S-16.

#### AT-31 — Microsoft's own RPA framing acknowledges UI fragility as the reason RPA exists (no other way to reach the system) rather than as a neutral trait, and mitigates it with AI self-healing selectors rather than removing the underlying fragility
- **Classification:** RISK
- **Evidence:** "Many legacy applications don't have a method for accessing their data or functionality except through their user interface. This inherent reliance on UI automation can make such solutions fragile" (search-derived synthesis of Microsoft RPA training content, S-17). Mitigation: "The AI-powered self-healing feature uses AI to locate elements on the screen at the execution time, and the repaired selector is used in future executions... a repair feature uses Copilot to find and repair the selectors of the required UI elements on the screen, with users simply needing to review and approve Copilot's suggestions" (search-derived, S-17, referencing `repair-at-runtime` and `self-heal-ui-browser-automation-actions-at-execution-ai` release-plan pages).
- **Why it matters:** Self-healing reduces the *frequency* of breakage, it does not remove the structural cause: RPA automates a UI contract the target application owner did not design to be stable, and did not commit to keeping stable.
- **Decision impact:** RPA is a bridge technology for a specific gap (no API) — not a permanent integration strategy; the existence of self-healing does not change RPA's fit classification from CONDITIONAL to STRONG, it only reduces the CONDITIONAL's operating cost.
- **Confidence:** MEDIUM (search-derived; the fragility statement itself was not found as a direct Microsoft quote — it is the search tool's synthesis of Microsoft training content, so treat with caution — see U-03).
- **Sources:** S-17.

#### AT-32 — Power Automate Desktop credential handling has documented secure mechanisms (Get credential action, Azure Key Vault/CyberArk backing, sensitive-variable marking) that must be deliberately used — the platform does not force secure-by-default handling of every secret path
- **Classification:** RECOMMENDATION + RISK
- **Evidence:** "In desktop flows, use the Get credential action to retrieve sensitive values instead of passing them as input variables. This practice ensures credential variables are marked as sensitive by default and aren't stored in the flow run logs. Power Automate now supports storing connection credentials securely in Azure Key Vault (AKV) or CyberArk... Use credentials when creating Microsoft Entra hybrid join network connection to connect hosted machine groups to the Active Directory (AD) domain" (search-derived, S-18). Registry-level governance controls (proxy, certificate revocation check, screenshot-on-error suppression, UNC path disabling, cloud-connector disabling) are extensive and IT-admin-configured, not maker-configured by default (MS, S-19, ms.date 2026-07-03, fetched in full — see e.g. `DisableScreenshotCaptureOnError`, `DisableUNCPaths`, `DisableCloudConnectors` keys).
- **Why it matters:** Credential and log-hygiene risk in RPA is real (screenshots-on-error can capture sensitive on-screen data unless explicitly disabled; action logs are uploaded by default) and requires explicit admin configuration, not merely "using RPA responsibly."
- **Decision impact:** RPA governance checklist item: confirm `Get credential` usage (not hardcoded/variable secrets), confirm screenshot-on-error and log-upload settings match the sensitivity of the automated screens, confirm machine registration is locked to the intended tenant.
- **Confidence:** HIGH (registry mechanics, fetched) / MEDIUM (credential-vault claims, search-derived).
- **Sources:** S-18, S-19.

### 4.10 Orchestration

#### AT-33 — Durable Functions is Microsoft's purpose-built code-first orchestration engine, with named patterns (chaining, fan-out/fan-in, async HTTP APIs, human interaction, aggregator/monitor) that a cloud flow's designer does not natively provide
- **Classification:** PATTERN
- **Evidence:** "With Azure Durable Functions, you can write stateful workflows in a new function type called an orchestrator function, which provides you more control for building workflows than using a designer for Logic Apps... Durable Functions' flexible patterns—chaining, fan-out/fan-in, async APIs, human interaction—make them a strong fit for modern, distributed applications... Durable Functions support fan-out/fan-in patterns, which are often required in scenarios like parallel processing and data aggregation, enabling you to execute multiple tasks concurrently and then aggregate the results when they complete" (search-derived, S-20). Confirmed structurally by S-09 (fetched): "For Azure Functions, you develop orchestrations by writing code and using the Durable Functions extension... execute many instances of a function in parallel, wait for all instances to finish, and then execute a function that computes a result on the aggregate."
- **Decision impact:** Complex distributed orchestration (parallel sub-tasks with aggregation, long-running stateful workflows needing code-level control, versioned replay-safe orchestration) → Durable Functions is the documented purpose-built answer; a cloud flow attempting the same thing runs into AT-04's structural limits (500 actions, 8 levels of nesting) well before Durable Functions would.
- **Confidence:** MEDIUM (S-20 search-derived) / HIGH (S-09 fetched, corroborating).
- **Sources:** S-20, S-09.

#### AT-34 — Logic Apps and Durable Functions are "built on the same underlying technology" per Azure Architecture Center framing (already cited at PS-24, S-60) but differ in development model (designer-first/declarative vs. code-first/imperative), connectivity breadth (1,400+ connectors vs. a dozen native bindings), and monitoring surface — the choice is a team-skill and connector-breadth decision as much as a technical one
- **Classification:** TRADE-OFF (cross-reference + extension)
- **Evidence:** Comparison table (MS, S-09, fetched in full): Development — "Code-first (imperative)" (Durable Functions) vs. "Designer-first (declarative)" (Logic Apps); Connectivity — "A dozen built-in binding types" vs. "1,400+ prebuilt connectors... Enterprise Integration Pack for B2B scenarios"; Monitoring — "Azure Application Insights" vs. "Azure portal / Azure Monitor Logs / Microsoft Defender for Cloud / Application Insights for Standard workflows."
- **Decision impact:** Pro-developer team, custom/complex code logic, few external connectors needed → Durable Functions. Connector-heavy integration, citizen/pro-dev mixed team, B2B/EDI → Logic Apps. Both outrank a cloud flow once AT-04's structural ceilings are the binding constraint.
- **Confidence:** HIGH.
- **Sources:** S-09.

#### AT-35 — Choosing a message broker is itself an orchestration-adjacent decision with documented criteria: Service Bus for commands needing ordering/dedup/sessions, Event Grid for discrete events and high-throughput fan-out (push or pull), Event Hubs for continuous streams
- **Classification:** DECISION CRITERION
- **Evidence:** "Use Service Bus messaging queues to transfer commands from producers to consumers" — sessions, peek-lock, dedup, DLQ, checkpointing (MS, S-11). "Use Event Grid for discrete events... Event Grid has multiple tiers to support high-throughput, high-volume use cases... Event Grid attempts to deliver each message at least once for each subscription... Event Grid doesn't guarantee order for event delivery... In addition to the push model, Event Grid supports HTTP-based pull delivery... Use this model when your event consumers... process events on a schedule rather than continuously [or] have intermittent availability... If your workload requires enterprise messaging features like strictly ordered processing (sessions), transactions, or duplicate detection, use Service Bus instead" (MS, S-11). "When you work with event streams, use Event Hubs as the message broker. Event Hubs buffers large volumes of data at low latency... can ingest millions of events per second" (MS, S-11, all ms.date 2026-02-11, fetched in full).
- **Decision impact:** This is the concrete decision table behind matrix row 6 and 17 (§2): pick the broker by message *type and guarantee needed*, not generically.
- **Confidence:** HIGH.
- **Sources:** S-11.

#### AT-36 — Crossover patterns (Service Bus → Event Grid to drain idle queues; Event Grid → Service Bus to route commands out of a mixed event stream) show that "which broker" is not always a single exclusive choice, mirroring the "combine, don't choose exclusively" pattern already established for Power Automate/Logic Apps/Functions (AT-17)
- **Classification:** PATTERN
- **Evidence:** "Idle queues that occasionally receive messages create inefficiency because the consumer continuously polls the queue for new messages. You can set up an Event Grid subscription and use an Azure function as the event handler. Each time the queue receives a message and no consumers are listening, Event Grid sends a notification that invokes the Azure function to drain the queue" — and the reverse: "Event Grid receives a set of events. Some events require a workflow and other events trigger notifications... If an event requires a workflow, Event Grid sends it to a Service Bus queue... Event Grid sends the notification events to Logic Apps to send alert emails" (MS, S-11, ms.date 2026-02-11).
- **Decision impact:** Do not force a single-broker architecture when the message mix is heterogeneous (some commands, some notifications); route by type at ingestion.
- **Confidence:** HIGH.
- **Sources:** S-11.

### 4.11 Observability and operations

#### AT-37 — Power Automate's built-in observability spans four surfaces of increasing durability and cost: in-designer run history (30-day rolling), per-flow Analytics (30-day rolling, 24-hour refresh), environment-level admin-center Analytics (28 days), and Dataverse `FlowRun` table (longer retention, queryable)
- **Classification:** FACT
- **Evidence:** "You can also view detailed information about specific runs... a rolling 30-day run history" (Analytics). "Known limitations: This feature isn't currently available in government and sovereign clouds. Data refresh cycle: Reports refresh approximately every 24 hours. Real-time data isn't available." Environment-level: "The last 28 days of run history." "Flow run history in Microsoft Dataverse lets you track the execution history of your cloud flows at scale... Each execution of a cloud flow is recorded in the FlowRun table in Dataverse... The run history that's stored in Dataverse is retained longer than the run history that's available in Power Automate" (MS, S-21, ms.date 2026-06-01, fetched in full).
- **Why it matters:** "Power Automate has run history" is true but imprecise; the *default* retention (30 days / 28 days) is short for audit or long-term trend purposes, and the durable option (Dataverse `FlowRun`) requires deliberate configuration.
- **Decision impact:** Compliance/audit requirements needing run history beyond ~30 days → must plan for Dataverse `FlowRun` retention or export, not assume the default UI gives it.
- **Confidence:** HIGH.
- **Sources:** S-21.

#### AT-38 — Application Insights integration gives cross-flow, queryable, alertable telemetry (dependency calls, server requests, custom alerts) but is an explicit environment-level opt-in requiring an Azure resource, not a zero-configuration capability
- **Classification:** CONSTRAINT + RECOMMENDATION
- **Evidence:** "Customers can select to emit cloud flow runs, triggers and action-level data from an environment to Application Insights, and the connection can be set up in just a few steps from the Power Platform Admin Center." "Select Dependency calls for alerting on triggers and actions, and to alert on only failures, select Dependency call failures. Select Server Requests for cloud flow runs, and to alert only on run failures, select Failed requests. Select the threshold for monitoring errors and the frequency... you can combine multiple conditions into a single alert" (search-derived, S-22, corroborated by the fetched Well-Architected page's pointer: "Use the Application Insights integrations to log errors in Power Automate and Power Apps: Set up Application Insights with Power Automate (preview)..." (MS, S-04, ms.date 2025-08-18) — note the source page's own link labels this integration "(preview)" as of the fetched date).
- **Why it matters:** The observability sub-area in the brief (correlation, alerting, retry visibility) is only fully answered once Application Insights is wired up; native Power Automate surfaces (AT-37) do not provide cross-flow correlation or proactive alerting on their own.
- **Decision impact:** Enterprise-grade operational observability requirement → budget for Application Insights setup (an Azure-side artifact, likely a different cost/ownership boundary than the Power Platform environment) as part of the automation architecture, not as an afterthought.
- **Conditions:** The Well-Architected page's own link text still says "(preview)" for the Power Automate Application Insights integration at fetch time (2025-08-18 page date) — verify current GA status before pack encoding (see U-05).
- **Confidence:** MEDIUM (search-derived detail) / HIGH (existence and pointer, fetched).
- **Sources:** S-22, S-04.

#### AT-39 — Process mining/process insights on a flow's own run history is a documented, built-in performance-diagnosis tool distinct from Application Insights, useful for identifying bottleneck actions and throttling-risk action bursts
- **Classification:** PATTERN
- **Evidence:** "Process mining digs deep into the details of your flows to offer valuable insights... Show you how your flow performs, identify areas where it slows down... Detect changes in your flow's performance over time... The '# of Runs and Actions' section of the report includes the number of actions that executed during a run, helping you understand if your flow might run into daily action bursts throttling limits" (MS, S-21, ms.date 2026-06-01, fetched in full).
- **Decision impact:** Before assuming Application Insights is necessary for basic performance diagnosis, use the free, built-in process-insights report on the flow's own details page.
- **Confidence:** HIGH.
- **Sources:** S-21.

#### AT-40 — Transient-fault handling guidance explicitly recommends logging retries as warnings (not errors) to avoid false alerting, and recommends telemetry specifically on retry rate and throttling-vs-other-fault differentiation — a concrete operational-ownership practice, not just a technical one
- **Classification:** RECOMMENDATION
- **Evidence:** "Log transient faults as warning entries rather than as error entries so that monitoring systems don't detect them as application errors that might trigger false alerts. Consider storing a value in your log entries that indicates whether retries are caused by throttling in the service or by other types of faults... so that you can differentiate them during analysis of the data. An increase in the number of throttling errors is often an indicator of a design flaw in the application or the need to add premium capacity" (MS, S-04, ms.date 2025-08-18, fetched in full).
- **Decision impact:** Alerting design for automation should distinguish "retry happened and succeeded" (informational) from "retry exhausted / flow failed" (actionable), and should track throttling rate as a leading indicator of needing more Process-licence capacity (cf. AT-04).
- **Confidence:** HIGH.
- **Sources:** S-04.

#### AT-41 — Operational ownership is a named, explicit requirement in Microsoft's own reliability guidance ("manage operations that continually fail"), including a specific pattern for automatically resuming service once a persistently failing dependency recovers
- **Classification:** RECOMMENDATION
- **Evidence:** "Consider how to handle operations that continue to fail at every attempt... The application can periodically test the service, on an intermittent basis and with long intervals between requests, to detect when it becomes available... When the test succeeds, the application can resume normal operations... In the meantime, you might be able to perform some alternative operations based on the hope that the service will be available soon. For example, it might be appropriate to store requests for the service in a queue or data store and retry them later. Or you might have to return a message to the user to indicate that the application isn't available" (MS, S-04, ms.date 2025-08-18, fetched in full).
- **Decision impact:** A production automation architecture needs an explicit "dependency down" runbook (queue-and-retry-later, or user-facing degraded-mode message), not just per-action retry policy.
- **Confidence:** HIGH.
- **Sources:** S-04.

### 4.12 Decision criteria (requirement → constraint → architectural consequence)

#### AT-42 — Event/process frequency
- **REQUIREMENT:** Automation must react to events occurring more often than roughly once per minute, or must guarantee processing order across events.
- **CONSTRAINT:** Minimum recurrence interval for scheduled flows is 60 seconds (MS, S-01); polling triggers check on a fixed interval and have no ordering guarantee across polls; webhook triggers drop events while off (AT-13); Power Automate itself has no session/ordering primitive (AT-14).
- **ARCHITECTURAL CONSEQUENCE:** Sub-minute or order-sensitive event frequency → put a broker with native ordering (Service Bus sessions) or streaming (Event Hubs) in front; do not rely on flow-native scheduling or trigger behaviour alone.
- **Confidence:** HIGH. **Sources:** S-01, S-07, S-11.

#### AT-43 — Transaction/action volume
- **REQUIREMENT:** Sustained daily action volume approaches or exceeds the flow owner's licence entitlement (Low 10,000 / Medium 200,000 / High 500,000 requests per 24h, or the owner's Power Platform request allocation per PS-19).
- **CONSTRAINT:** Throttling first, then 14-day automatic shutoff for consistently throttled flows (MS, S-01).
- **ARCHITECTURAL CONSEQUENCE:** Assign Process/capacity licensing deliberately (stackable, shareable via flow groups), or move the highest-volume leg of the workload to a bulk/batch API, a dataflow, or an Azure service billed on compute/message volume rather than per-owner entitlement.
- **Confidence:** HIGH. **Sources:** S-01; PS-19.

#### AT-44 — Latency requirement
- **REQUIREMENT:** A caller needs a synchronous response within a bounded time.
- **CONSTRAINT:** Hard 120-second inbound/outbound synchronous timeout (MS, S-01; cf. PS-28's 180s canvas figure for a different call path).
- **ARCHITECTURAL CONSEQUENCE:** Sub-2-minute synchronous requirement inside that ceiling → cloud flow is fine. Longer or unpredictable processing time → redesign as async (accept-and-poll, or webhook callback), or move the synchronous leg to a service with its own SLA (Function, Durable Functions' async-HTTP pattern, or a custom API).
- **Confidence:** HIGH. **Sources:** S-01.

#### AT-45 — Duration (long-running processes)
- **REQUIREMENT:** A process, including any human wait states, must remain open longer than 30 days.
- **CONSTRAINT:** Flow run duration hard limit is 30 days including pending approvals; after 30 days pending steps time out (MS, S-01; PS-22).
- **ARCHITECTURAL CONSEQUENCE:** Long-horizon processes (multi-month approvals, contract renewal cycles) must persist their state outside the flow run (a Dataverse table tracking status) and use a scheduled/re-triggering flow to resume, rather than one continuously running flow instance.
- **Confidence:** HIGH. **Sources:** S-01; PS-22.

#### AT-46 — Reliability requirement (failure semantics, retry, ordering)
- **REQUIREMENT:** The business cannot tolerate duplicate side effects (double charge, duplicate notification) or out-of-order processing.
- **CONSTRAINT:** Default and configurable retry policies will re-execute actions on transient failure (up to 90 attempts configurable) without an idempotency guarantee of their own (MS, S-01, S-04); no native ordering/dedup exists in Power Automate (AT-14).
- **ARCHITECTURAL CONSEQUENCE:** Every retryable side-effecting action needs an idempotency key or upsert semantics designed in; order-sensitive processing needs either trigger concurrency = 1 in an isolated child flow (AT-11) or an upstream ordered broker (Service Bus sessions).
- **Confidence:** HIGH. **Sources:** S-01, S-04, S-07, S-11.

#### AT-47 — Consistency requirement (transactional guarantees)
- **REQUIREMENT:** A multi-step, multi-system operation must be all-or-nothing.
- **CONSTRAINT:** No cross-connector transaction construct exists; Dataverse-internal atomicity is available only via change sets/plug-ins (PS-45).
- **ARCHITECTURAL CONSEQUENCE:** If every write can be kept inside Dataverse standard tables → CONDITIONAL (change set/custom API design). If not → HYBRID: saga with compensating actions, idempotency keys, and durable in-doubt state (AT-25).
- **Confidence:** HIGH (inherited from PS-45). **Sources:** PS-45, PS-58, AT-25.

#### AT-48 — Human interaction requirement
- **REQUIREMENT:** The process needs approval, escalation, delegation, or reassignment by a person.
- **CONSTRAINT:** Approvals are a mature pattern (AT-27) bounded by the 30-day run-duration ceiling (PS-22).
- **ARCHITECTURAL CONSEQUENCE:** Human-in-the-loop within 30 days → STRONG fit for Power Automate approvals. Beyond 30 days, or with escalation logic too complex for the approvals connector's native settings → externalize state to a data table and re-trigger.
- **Confidence:** HIGH. **Sources:** PS-22, S-01, S-12.

#### AT-49 — Integration complexity / API availability
- **REQUIREMENT:** The system to integrate with either has a stable API or does not.
- **CONSTRAINT:** Connectors and custom connectors require a REST (or SOAP-via-custom, per PS-26's unresolved U-10) endpoint to wrap; no API means Power Automate cloud flows have nothing to call.
- **ARCHITECTURAL CONSEQUENCE:** Stable API → cloud flow/connector (STRONG). No API → Power Automate Desktop (RPA), accepting the fragility, licensing-per-bot, and infrastructure cost of AT-29–AT-31, or invest in building/exposing an API instead (often the better long-term answer when the legacy system's remaining lifetime justifies the build cost).
- **Confidence:** HIGH. **Sources:** PS-26, S-13, S-16, S-17.

#### AT-50 — Compute requirement
- **REQUIREMENT:** The process needs algorithmic/iterative computation, not just orchestration and connector calls.
- **CONSTRAINT:** Power Fx/cloud-flow expressions are not a general-purpose imperative language (cf. PS-08); plug-ins cap at 2 minutes (PS-09).
- **ARCHITECTURAL CONSEQUENCE:** Compute-intensive logic → Azure Functions (HYBRID with a flow as the orchestration front door), per Microsoft's own "no-cliffs" extension model (PS-09, PS-30).
- **Confidence:** HIGH (inherited from PS). **Sources:** PS-08, PS-09, PS-30.

#### AT-51 — Operational ownership and existing enterprise infrastructure
- **REQUIREMENT:** The organization already runs an Azure integration estate (Logic Apps Standard, APIM, an enterprise service bus) or an existing workflow/BPM engine for this class of process.
- **CONSTRAINT:** None specific to Power Automate — this is an organizational-fit criterion, not a technical limit.
- **ARCHITECTURAL CONSEQUENCE:** Where IT already owns and operates a comparable capability, introducing Power Automate for the same class of process duplicates the operating model rather than reducing it (cf. PS-24's "volume alone does not decide" framing) — the decision hinges on who owns the process (business vs. IT) and whether the existing infrastructure already meets the requirement, not on Power Automate's technical capability alone.
- **Confidence:** MEDIUM (INF, synthesizing PS-24 and AT-17 into an organizational-fit statement not itself directly quoted from a single source). **Sources:** PS-24, AT-17.

### 4.13 Anti-patterns

#### AT-52 — Documented, evidence-backed anti-patterns (Microsoft's own guidance): nested `For each` loops, self-triggering infinite loops, large-scale data transformation inside a flow, and per-record loops for bulk create/update
- **Classification:** ANTI-PATTERN (cross-reference — see AT-15 for full quotes)
- **Decision impact:** These four are safe to encode in the pack as MS-sourced, HIGH-confidence anti-patterns without qualification.
- **Confidence:** HIGH. **Sources:** S-06.

#### AT-53 — Layered/duplicated retry logic across nested call chains is a documented anti-pattern that multiplies load on a struggling downstream system
- **Classification:** ANTI-PATTERN (cross-reference — see AT-05)
- **Confidence:** HIGH. **Sources:** S-04.

#### AT-54 — Irreversible trigger concurrency control applied broadly "just in case" is a documented caution, not an anti-pattern in the strict sense, but functions as one when applied without the recommended child-flow isolation
- **Classification:** ANTI-PATTERN (RECOMMENDATION-derived)
- **Evidence:** See AT-11 — "leave the concurrency control at its default setting... consider doing so on a flow with the least number of actions" (MS, S-07).
- **Confidence:** HIGH. **Sources:** S-07.

#### AT-55 — Using RPA as the default integration strategy where a stable API exists is contradicted by Microsoft's own decade-old planning guidance (already cited at PS-21) and reinforced by this file's fragility/cost findings (AT-29–AT-31)
- **Classification:** ANTI-PATTERN
- **Evidence:** PS-21: "APIs are meant to be stable even as the application changes over time"; RPA "is susceptible to breaking when things change." This file adds the licensing-per-bot cost driver (AT-30) and the infrastructure/session-density requirement (AT-29) as additional reasons this is not merely a stability preference but a total-cost-of-ownership one.
- **Decision impact:** RPA-first proposals for systems with an accessible API should be challenged during Discovery/Options; RPA is a justified choice specifically for the "no other way in" case, not a default automation starting point.
- **Confidence:** HIGH (PS-21) / MEDIUM (this file's cost extension). **Sources:** PS-21, AT-29, AT-30.

#### AT-56 — Using Power Automate as a general-purpose application backend is flagged (search-derived, T3) as producing hidden operational failure modes: no standardized error propagation, no cross-flow traceability, and operational blind spots as the number of flows grows
- **Classification:** ANTI-PATTERN (labelled as an architectural recommendation, not a Microsoft statement)
- **Evidence:** "Power Automate enables rapid workflow creation, but it lacks a standardized approach for error handling, failure propagation, observability, and cross-flow traceability, which leads to hidden failures and operational blind spots as solutions scale" (search-derived, T3, S-23). This is consistent with, but not identical to, Microsoft's own observability gaps documented in AT-37/AT-38 (short default retention, opt-in Application Insights) — those are Microsoft-confirmed constraints; the "general-purpose backend" framing itself is a T3 architectural argument.
- **Why it matters:** This is the clearest statement in this research pass of the brief's "using Power Automate as a general-purpose application backend" anti-pattern, but it is not a Microsoft-authored claim and should be labelled as such in the pack.
- **Decision impact:** Treat "don't use Power Automate as your application's backend" as a RECOMMENDATION derived from the combination of AT-04 (structural limits), AT-37/AT-38 (observability gaps), and PS-45 (no cross-system transactions) — each individually MS-sourced — rather than citing the T3 framing as if Microsoft said it directly.
- **Confidence:** MEDIUM (T3 framing) / HIGH (the underlying MS-sourced constraints it is built from).
- **Sources:** S-23 (T3); AT-04, AT-37, AT-38, PS-45.

#### AT-57 — Polling when an event-driven/webhook trigger is available is a documented sub-optimal default, but Microsoft's own guidance is nuanced: some connectors only offer polling, and webhook triggers have their own outage-drop risk (AT-13) — this is a trade-off, not an unconditional anti-pattern
- **Classification:** ANTI-PATTERN (conditional)
- **Evidence:** "If a connector provides an event-based trigger, prefer it over repeatedly checking the same data with a scheduled flow when real-time processing is required" (search-derived, S-14). Countervailing nuance already established at AT-13: webhook triggers silently drop events while a flow is off, which a polling trigger's backlog-replay does not.
- **Decision impact:** Prefer event/webhook triggers for latency-sensitive requirements; retain awareness that this trades "no backlog flood" for "silent loss risk," and design outage-recovery accordingly either way.
- **Confidence:** MEDIUM. **Sources:** S-14, AT-13.

---

## 5. Conflicts (CONFLICTED)

| Id | Topic | Source A | Source B | Assessment |
|---|---|---|---|---|
| C-01 | Default retry attempt count | Search-derived summary: "default setting of four retries" (S-02) | Fetched limits page: Low profile "up to two retries"; Medium/High "up to 12 retries" (S-01) | S-01 (fetched, dated, official limits page) is authoritative; the "four retries" figure in S-02 is either a stale/generic claim or refers to a different default context (e.g., a specific connector's own retry policy rather than the flow-level default). Do not encode "four" as the default; use S-01's Low/Medium/High table. |
| C-02 | Whether Power Automate's Application Insights integration is GA or preview | Well-Architected page (2025-08-18) links to it as "(preview)" | Monitoring-and-alerting guidance page (2026-06-01) describes it without a preview caveat, as a standard capability | Likely a genuine status change between the two `ms.date`s (10 months apart) — treat as GA per the more recent page, but flag for re-verification before pack encoding (see U-05). |

---

## 6. Unknowns (UNKNOWN)

| Id | Unknown | Why it matters | Resolution path |
|---|---|---|---|
| U-01 | Exact in-product name/mechanics of the approvals "Enable reassignment" toggle, timeout configuration UI, and delegation/out-of-office check | AT-27's mechanics are search-derived, not fetched from a canonical Approvals reference page | Fetch `learn.microsoft.com/power-automate/*approvals*` reference pages directly |
| U-02 | Current, dated Power Automate Process/Hosted Process per-bot pricing | AT-30's $150/$215-per-bot figures are search-derived from third-party pricing summaries, not the Power Platform Licensing Guide PDF | Fetch the current Power Platform Licensing Guide PDF (cf. DA:S40 in data-architecture.md) and the official pricing page directly |
| U-03 | A direct, fetched Microsoft quote acknowledging UI-automation fragility as an inherent RPA limitation (rather than only describing self-healing mitigations) | AT-31's core claim is a search-tool synthesis, not a verbatim Microsoft admission | Fetch `power-automate/desktop-flows/introduction` and RPA training module content directly for a verbatim statement |
| U-04 | Whether any Microsoft page explicitly states cloud flows lack native message ordering/deduplication (vs. this being inferred from what the limits/trigger pages do not mention) | AT-14's negative claim is INF, capped accordingly | Search Power Automate/Logic Apps run-after and trigger documentation for an explicit statement, or treat as a stable inference given corroboration from the trigger-outage behaviour (AT-13) |
| U-05 | Current GA/preview status of the Power Automate–Application Insights integration | Affects whether AT-38 can be cited as a settled capability or a still-evolving one | Fetch `power-platform/admin/app-insights-cloud-flow` directly and check its current preview banner |
| U-06 | Whether Dataverse plug-in vs. cloud flow guidance (search-derived at AT §4 cross-references, and PS-09) includes any Microsoft statement on plug-ins' 2-minute limit interacting with high-frequency trigger volume specifically | Would sharpen the plug-in-vs-flow decision boundary for high-frequency, low-latency Dataverse-only automation | Fetch `power-apps/developer/data-platform/plug-ins` directly |
| U-07 | Whether business process flows have any documented volume/performance limit of their own (separate from the Dataverse table limits in DA) | Matrix row 3 (§2) currently has no dedicated limit citation | Fetch a canonical business-process-flow limits/overview page |
| U-08 | Current numeric SAP/legacy-terminal RPA action count ("400+ prebuilt actions" was seen only in a search snippet, not fetched) | Cost/breadth claims for PAD as an SAP/mainframe bridge are unverified | Fetch `power-automate/desktop-flows/*` action-reference pages directly |

---

## 7. Deferred to other areas

| Gap | Target area | Effect if undelivered |
|---|---|---|
| Full custom-connector authentication/token-passthrough mechanics for API-fronted integration | 05 Integration | AT-19's "connector wraps REST" statement stays high-level; detailed auth patterns (OAuth, service principal token exchange) remain in PS-26 only |
| On-premises data gateway throughput specifically for high-volume automation (vs. the general gateway limits already in DA) | 05 Integration / 09 Performance | AT §4.6 high-volume findings do not cover the on-prem leg specifically |
| Copilot Studio / autonomous agent flows as an automation modality (explicitly out of this file's scope; one search result surfaced "Power Automate and Copilot Studio Autonomous Agents" as a live comparison topic) | Not yet assigned an area | This corpus is silent on agent-based automation as an alternative/successor pattern; flag for a future area or an explicit scoping decision |
| Full Power Automate + Logic Apps + Functions cost model (per-execution, per-action, per-bot) | 10 Licensing and Cost | AT-30's cost figures stay MEDIUM confidence and unquantified beyond the cited search summary |
| Dataverse background operations reference architecture (cited only by title at S-04's "Related information" link, not fetched) | 12 Architecture Patterns | A named Microsoft reference architecture for background/async Dataverse processing is not analyzed in this file |

Undelivered deferrals should revert the corresponding matrix cells to UNKNOWN when this file is gated, consistent with the convention in `platform-suitability.md` §7 and `data-architecture.md` §9.

---

## 8. Evidence-quality notes

- **Fetched in full (highest confidence tier in this file):** S-01 (limits-and-config), S-04 (handle-transient-faults), S-06 (avoid-anti-patterns), S-07 (optimize-power-automate-triggers), S-09 (functions-compare-logic-apps-ms-flow-webjobs), S-11 (Azure messaging technology choices), S-13 (desktop-flows/requirements), S-19 (desktop-flows/governance, mostly registry-key reference — low decision density but confirms credential/logging controls exist), S-21 (monitoring-and-alerting), S-22 partially corroborated by S-04's own link.
- **Fetched but off-target (attempted and discarded):** two WebFetch calls intended for "reducing-risk" error-handling guidance and an Azure Architecture Center automation-choice page instead returned unrelated content (a Plan Designer page and an Azure Functions eventing-bindings page respectively, likely due to redirects or URL drift) — these are not cited as sources; the equivalent content was instead obtained via S-04 (transient faults) and S-09/S-11 (comparison/messaging pages), which were fetched successfully on retry with corrected URLs.
- **Search-derived (MEDIUM ceiling even where the underlying page is Tier 1):** S-02 (retry policy default count — CONFLICTED with fetched S-01, see C-01), S-03 (run-after/scopes), S-05 (Microsoft training module pointer), S-10 (Power Automate vs. Logic Apps positioning, corroborates PS-24), S-12 (approvals mechanics), S-14 (trigger type guidance), S-15 (business process flow framing), S-16 (RPA licensing figures), S-17 (RPA fragility framing), S-18 (PAD credential handling), S-20 (Durable Functions patterns).
- **T3/T4 with acknowledged bias or unverified authorship:** S-23 ("Power Automate is killing HR onboarding" style blog framing the general-purpose-backend anti-pattern) — used only as the origin of a labelled RECOMMENDATION (AT-56), not as a FACT.
- **No empirical throughput/latency benchmarks** for cloud flows, Durable Functions, or Service Bus under sustained load were found or sought beyond documented limits — consistent with PS-30's and DA's own gap; performance claims in this file are all limit-based (what the platform allows) rather than benchmark-based (what it actually achieves under load).
- **Authorship:** single-session draft by one analyst; adversarial review and gate are pending (status header). Recommend independent spot-check of C-01 (retry default count) and U-02 (RPA pricing) before pack authoring, given both are volatile and currently only MEDIUM confidence.

---

## 9. Implications for the aisa knowledge model (pointers, not pack content)

Nothing below is a question, glossary term, signal, or decision-tree node; these are pointers for later pack authoring.

- **Technology-neutral Discovery signals suggested by the evidence:** event/trigger frequency and whether ordering across events matters; expected daily action/request volume and who the flow's designated owner/licence will be; longest human wait state in the process (days) and escalation-tree complexity; whether any step must be all-or-nothing across more than one system; whether retried actions are naturally idempotent (natural key available) or not; whether the target system has a stable, documented API vs. UI-only access; whether an existing Azure integration estate or enterprise workflow engine already covers this process class; required audit/observability retention window vs. the ~30-day platform default; concurrent unattended-bot count if RPA is in scope; private-network/dedicated-compute mandate.
- **Hard boundaries with Microsoft-stated evidence (safe to encode as CONSTRAINT):** 500 actions/8-nesting/100,000-loop-item/120-second-sync/30-day-run-duration/14-day-shutoff cloud flow ceilings (AT-04); no cross-connector transaction construct (PS-45, AT-25); retry can duplicate non-idempotent side effects (AT-06); polling-backlog-flood vs. webhook-silent-drop on outage (AT-13); RPA hardware/OS/per-bot-licence requirements (AT-29, AT-30).
- **Corrected boundaries (myth vs. mechanism):** "add a queue and it's exactly-once" is false without an idempotent consumer (AT-14, AT-18); "self-healing selectors fixed RPA fragility" overstates a frequency reduction as a structural fix (AT-31); "Power Automate vs. Logic Apps is about volume" is false — it is ownership/network/tooling (AT-16, PS-24); "Application Insights gives you observability for free" is false — it is an explicit, environment-level, possibly still-maturing opt-in (AT-38, U-05).
- **Automation-architecture options the pack must be able to output:** cloud-flow-only (business process orchestration, approvals, notifications, moderate integration); cloud flow + dataflow/bulk API (high-volume Dataverse writes); cloud flow + Service Bus/Event Grid (ordering, dedup, decoupling, high-frequency events); cloud flow + Durable Functions/Logic Apps (complex distributed orchestration, saga/compensation); Power Automate Desktop as a bounded bridge for UI-only legacy systems; Logic Apps Standard/Functions/custom service as the CUSTOM/OTHER default when private-network, dedicated-compute, extreme-throughput, or complex-transactional requirements dominate; business process flow (Dataverse UX) + cloud flow (system automation) as a paired pattern, not substitutes.
- **Validation before commitment (typical):** confirm the flow owner and licence class before estimating throughput headroom; prototype the retry/idempotency design on the highest-risk write path; confirm whether any step needs cross-system atomicity before assuming a saga is unnecessary; size RPA machine/session infrastructure and per-bot licence cost before comparing it to an API-build alternative; confirm current Application Insights GA status and set up alerting thresholds before go-live, not after the first incident.
- **Gate conditions proposed for downstream use (mirroring platform-suitability.md and data-architecture.md conventions):** (1) every verdict keeps its origin tag; search-derived findings stay capped at MEDIUM until independently fetched and confirmed; (2) before pack authoring, resolve C-01 (retry default count) against the fetched S-01 table, verify U-05 (Application Insights GA status) and U-02 (RPA per-bot pricing) directly; (3) the pack must not encode the T3-sourced "general-purpose backend" framing (AT-56) as a Microsoft statement — cite it as a labelled architectural recommendation built from MS-sourced constraints; (4) deferrals in §7 back-reference this file; undelivered deferrals revert the corresponding matrix cells to UNKNOWN; (5) re-verify all AT-04 limits, RPA licensing figures, and the Application Insights preview/GA status before encoding, given their volatility.

---

## 10. Source register

Kind: **fetched** (full page retrieved, `ms.date` read), **fetched-partial** (fetched but only part of a long page substantively captured), **search-derived** (WebSearch tool synthesis of Microsoft and/or third-party pages, not independently fetched), **T3/T4** (non-Microsoft, per tier).

| Id | Tier | Kind | Title | URL | ms.date |
|---|---|---|---|---|---|
| S-01 | T1 | fetched | Limits of automated, scheduled, and instant flows | https://learn.microsoft.com/en-us/power-automate/limits-and-config | 2026-07-17 |
| S-02 | T1 | search-derived | (Retry policy / Configure Run After — multiple Learn and T3 pages synthesized) | https://learn.microsoft.com/en-us/power-automate/guidance/planning/reducing-risk (and T3 pages) | n/d |
| S-03 | T1 | search-derived | Configure run after / error handling (Learn training module + community) | https://learn.microsoft.com/training/modules/error-handling/ | n/d |
| S-04 | T1 | fetched | Handle transient faults recommendation for Power Platform workloads (Well-Architected RE:05) | https://learn.microsoft.com/en-us/power-platform/well-architected/reliability/handle-transient-faults | 2025-08-18 |
| S-05 | T1 | fetched | Monitor your flows (guidance/coding-guidelines/monitoring-and-alerting) | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/monitoring-and-alerting | 2026-06-01 |
| S-06 | T1 | fetched | Avoid anti-patterns — Power Automate | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/avoid-anti-patterns | 2025-07-10 |
| S-07 | T1 | fetched | Optimize Power Automate triggers | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/optimize-power-automate-triggers | 2025-07-11 |
| S-08 | — | (unused; governance registry-key page superseded by S-19) | — | — | — |
| S-09 | T1 | fetched | Integration and Automation Platform Options in Azure (Functions vs. Logic Apps vs. Power Automate vs. WebJobs) | https://learn.microsoft.com/en-us/azure/azure-functions/functions-compare-logic-apps-ms-flow-webjobs | 2026-03-23 |
| S-10 | T1 | search-derived | Power Automate vs. Logic Apps vs. Azure Functions comparisons (multiple pages synthesized, corroborating PS-24 and S-09) | multiple (see PS-24 §12 for the primary fetched sources) | n/d |
| S-11 | T1 | fetched | Asynchronous Messaging Options — Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/messaging | 2026-02-11 |
| S-12 | T1 | search-derived | Power Automate approvals — escalation, reassignment, delegation (multiple Learn/community pages synthesized) | https://learn.microsoft.com/en-us/power-automate (approvals area) and community sources | n/d |
| S-13 | T1 | fetched | Prerequisites and limitations — Power Automate for desktop | https://learn.microsoft.com/en-us/power-automate/desktop-flows/requirements | 2026-03-24 |
| S-14 | T1 | search-derived | Triggers — Power Automate (types, polling vs. event-based recommendation) | https://learn.microsoft.com/en-us/power-automate/triggers-introduction | n/d |
| S-15 | T3/T1 mix | search-derived | Business process flow vs. cloud flow framing (IncWorx, Pragmatiq, and Learn training synthesized) | multiple | n/d |
| S-16 | T3 | search-derived | Power Automate RPA/Process licensing pricing (VE3, SmartProcessFlow, and Power Platform licensing FAQ synthesized) | https://github.com/MicrosoftDocs/power-platform/blob/main/power-platform/admin/power-automate-licensing/faqs.md and T3 pricing pages | n/d |
| S-17 | T1 (search-derived from) | search-derived | RPA fragility / self-healing selectors (Learn RPA training + release-plan pages synthesized) | https://learn.microsoft.com/en-us/power-automate/desktop-flows/repair-at-runtime and release-plan pages | n/d |
| S-18 | T1 | search-derived | Secure your data — Power Automate desktop (credential handling synthesized) | https://learn.microsoft.com/en-us/power-automate/guidance/desktop-flow-coding-guidelines/secure-your-data | n/d |
| S-19 | T1 | fetched | Governance in Power Automate for desktop | https://learn.microsoft.com/en-us/power-automate/desktop-flows/governance | 2026-07-03 |
| S-20 | T1 (search-derived from) | search-derived | Durable Functions orchestration patterns (chaining, fan-out/fan-in) | multiple Learn and T3 pages | n/d |
| S-21 | T1 | fetched | Monitor your flows (same page as S-05; cited separately for Analytics/FlowRun/process-mining sections) | https://learn.microsoft.com/en-us/power-automate/guidance/coding-guidelines/monitoring-and-alerting | 2026-06-01 |
| S-22 | T1 | search-derived | Set up Application Insights with Power Automate | https://learn.microsoft.com/en-us/power-platform/admin/app-insights-cloud-flow | n/d |
| S-23 | T3 | search-derived | "Power Automate Is Killing HR Onboarding at Scale" (m365.fm) — general-purpose-backend anti-pattern framing | https://www.m365.fm/stop-using-power-automate-like-this/ | n/d |

Not independently fetched at full-page level in this pass (relied on search-derived synthesis): S-02, S-03, S-10, S-12, S-14, S-15, S-16, S-17, S-18, S-20, S-22, S-23. These carry a MEDIUM confidence ceiling per §8 and should be fetched directly before pack encoding where they underpin a HIGH-stakes finding (flagged individually in §6 Unknowns).

Cross-referenced peer files (not re-registered here): `platform-suitability.md` §11 (S-01 through S-70, its own numbering — distinct from this file's S-ids), `data-architecture.md` §12 (DV/SQ/SP/EX/XC sub-registers), `application-architecture.md` §11.

---
