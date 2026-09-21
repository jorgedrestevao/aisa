Research Status: CANONICAL
Research Confidence: MEDIUM
Gate: PASS — Cross-Block Gate Recheck
Canonicalization Basis: Cross-Block Gate Recheck
Canonicalized: 2026-09-03

# Performance and Scale — Research Evidence

Research area: **09 — Performance and Scale** (`../research-areas.md`).
Research date: **2026-09-03**. Source policy: `../source-policy.md`.
Sibling files produced in the same block, deliberately kept conceptually distinct: `licensing-cost.md` (**LC-nn**) answers *what the workload costs*; `operations-support.md` (**OP-nn**) answers *how the workload is run in production*. This file answers only *whether the workload's runtime behaviour fits inside the platform's operating characteristics*. Where a performance decision has a cost or operations consequence, this file states the consequence and points at the sibling finding rather than re-deriving it (§11).

Cross-references to peer files, statuses verified 2026-09-03: `platform-suitability.md` (VALIDATED, Gate PASS, MEDIUM) as **PS-nn**; `application-architecture.md` (VALIDATED, Gate PASS, MEDIUM) as **AA-nn**; `data-architecture.md` (VALIDATED, Gate PASS, **HIGH**) as **DA-nn**; `automation-architecture.md` (VALIDATED, Gate PASS, MEDIUM) as **AT2-nn**. Findings here are **PF-nn**; sources are **P-nn**. A finding id and a source id sharing a number are unrelated.

**The question this file answers.** Not *"how fast is Power Platform?"* but:

> **When does the required workload exceed the appropriate operating characteristics of Power Platform — and which specific requirement changes the answer?**

Every finding runs **REQUIREMENT → PERFORMANCE CONSTRAINT → ARCHITECTURAL CONSEQUENCE**. A technology name is an output of that chain, never its starting point.

**Deliberate scope boundary against the automation peer.** `automation-architecture.md` already carries the cloud-flow limits envelope in depth (AT2-01…AT2-12, AT2-30…AT2-34). This file does **not** re-derive it. §5.6 states only the numbers needed to reason about *end-to-end workload throughput and latency*, cites AT2 for the automation-shape decision, and adds the two things AT2 explicitly left open for this area: how flow limits compose with app and data limits into a single binding constraint (PF-31), and the client-side half of latency (PF-13, PF-14).

---

## 0. How to read this file

**Classification** (per `../source-policy.md`): FACT · RECOMMENDATION · CONSTRAINT · TRADE-OFF · RISK · ANTI-PATTERN · DECISION CRITERION · PATTERN · VOLATILE VALUE.

**Origin tag** on every finding: **MS** (Microsoft statement on a page fetched in this pass, `ms.date` recorded in §14) · **MS-A** (Microsoft statement on a page whose `ms.date` is more than 18 months old — the claim is Microsoft's, the currency is not vouched for) · **INF** (analyst inference over documented facts) · **T3** (independent technical source) · **T4** (community signal) · **UNKNOWN**.

**Confidence.** HIGH = dated Tier 1 statement fetched in this pass or inherited from a VALIDATED peer. MEDIUM = Tier 1 but aged (> 18 months), inferred, or search-derived. LOW/UNKNOWN = not established; the finding says so.

**Absence claims.** Where this file says a figure is not published, it states whether Microsoft says so (MS) or whether it is inferred from the figure not appearing on the reference page (INF). INF absence claims are phrased *"treat as unpublished until verified"* everywhere they appear, including in the matrices.

**The single most important reading rule for this area.** Microsoft publishes **limits**, not **benchmarks**. There is no empirical throughput, latency or concurrency measurement anywhere in this corpus for any Power Platform component, and Microsoft says the honest thing about it twice: *"Each environment can be different"* (P-15) and *"Don't try to calculate how many requests to send at a time"* (P-15). Every performance statement below is therefore **limit-based, not measurement-based**. A design that violates no documented limit is *not* thereby known to be fast; it is only known not to be structurally excluded. Reviewers must not let §3's `WITHIN ENVELOPE` verdicts be read as "Microsoft says this performs well" (see §13, PF-U-01).

**Volatility.** Limits, connector throttles, performance profiles and preview states move fastest in this area. Every number is valid on the `ms.date` in §14. The Power Platform request model is *explicitly mid-transition* with no announced enforcement date (AT2-03, PF-30) — a design compliant today can be throttled on a date outside the customer's control.

---

## 1. Classify the workload before sizing it

v0 of this area risked the standard failure: quoting the biggest published number ("500,000 requests/day", "30 million SharePoint items") and concluding the platform scales. The numbers only mean something once the workload's **shape** is fixed, because a different meter binds in each shape.

| Workload shape | Defining question | What actually binds | Where sized |
|---|---|---|---|
| **INTERACTIVE READ** | Do many people need to *look at* business data quickly? | Client-side payload and round trips; delegation | §5.1, §5.5 |
| **INTERACTIVE WRITE** | Do many people need to *record transactions* through a UI? | Dataverse service protection per identity; connector throttle | §5.5, §5.8 |
| **BACKGROUND VOLUME** | Does a large set of records need processing without a person waiting? | Power Platform requests; execution-time meter; run duration | §5.6 |
| **EVENT STREAM** | Do high-frequency events need to be absorbed as they arrive? | Trigger mechanism latency; concurrency control; broker | §5.6, §5.7 |
| **PUBLIC / EXTERNAL READ** | Do unauthenticated or external users need to browse content? | Power Pages cache and node scaling; the *single service-principal identity* | §5.3, §5.5 |
| **COMPUTE** | Does one step need real calculation rather than calls? | Nothing in Power Platform sizes this — see PF-45 | §6 |

**Classification test** (apply in order; first "yes" fixes the shape):

1. Does one step need **real computation** (optimisation, simulation, image/video processing, large-matrix maths) rather than orchestrating calls? → **COMPUTE**. Power Platform has no compute-sizing dial (PF-45); this is an out-of-platform verdict before any other sizing is attempted.
2. Do **unauthenticated or high-volume external** users read the data? → **PUBLIC / EXTERNAL READ**. The binding constraint is that all their traffic lands on one Dataverse identity (PF-25), which no app-side tuning changes.
3. Are events arriving **faster than the trigger mechanism's own interval**? → **EVENT STREAM**. This is a mechanism problem, not a tuning problem (PF-32).
4. Is there **volume without a waiting human**? → **BACKGROUND VOLUME**.
5. Otherwise it is **INTERACTIVE**, and read/write splits by whether the transaction rate or the payload dominates.

**Why this matters architecturally.** Most Power Platform performance failures in this corpus are not the platform being slow. They are a shape-2/3/6 requirement implemented as shape 1 — an interactive app asked to be a batch engine, a broker, or a compute host. The anti-patterns in §6 are almost all instances of that single error.

- **Classification:** DECISION CRITERION · **Origin:** INF (the taxonomy is this file's synthesis; every capability fact behind it is MS-sourced in §5) · **Confidence:** MEDIUM · **Sources:** synthesis over PF-01…PF-46.

---

## 2. The meter map — five independent limit systems

The single most consequential structural fact in this area, and the one most often missed in sizing conversations, is that **there is no one "Power Platform performance limit"**. Five systems are evaluated *separately*, and the one that bites first is usually not the one people plan against.

| # | Meter | Scope of evaluation | Window | Typical binding value | Where |
|---|---|---|---|---|---|
| 1 | **Power Platform requests (PPR)** — entitlement | Per **owner identity** (or per flow with a capacity licence) | 24 h sliding + 5 min | 40,000/user/24 h official; 100,000/5 min | PF-29, PF-30 |
| 2 | **Dataverse service protection** | Per **authenticated user**, per **web server** | 300 s sliding | 6,000 requests · 1,200 s execution · 52+ concurrent | PF-22 |
| 3 | **Per-connector throttle** | Per **connection** | Per connector (10 s–60 s) | SharePoint 600/60 s; custom connector **CONFLICTED: 500 vs 10,000/min/connection; do not size from either without verification** | PF-27, PF-28 |
| 4 | **Client-side capacity** | Per **user session / device / browser** | Continuous | Data row limit 500–2,000; JS heap; concurrent requests per platform | PF-01, PF-13 |
| 5 | **Product structural limits** | Per **artefact definition** | Static | 500 actions/flow; 8 nesting; 5,000 array items (Low) | PF-33, PF-34 |

Microsoft states the independence of meters 1 and 2 explicitly and pre-empts the obvious workaround: *"Batch operations aren't a valid strategy to bypass entitlement limits. Service protection API limits and entitlement limits are evaluated separately. Entitlement limits are based on CRUD operations and accrue whether or not they're included in a batch operation"* (P-15, `ms.date` 2026-01-09).

**Consequence for any sizing exercise.** A throughput requirement must be expressed in **five** units before a verdict is possible:

1. actions or CRUD operations per 24 h, per owning identity (entitlement);
2. requests and combined execution-seconds per 5 min, per acting identity (service protection);
3. calls per window, per connection, for **each** connector on the path (throttle);
4. rows and bytes delivered to **one** client session (client capacity);
5. actions, nesting and array size in **one** artefact definition (structural).

The binding constraint is the smallest of the five, and in this corpus it is normally (3) the connector or (2) service protection — **not** (1) the daily entitlement that licence conversations centre on. Sizing against the daily number alone is sizing against the wrong meter.

- **Classification:** DECISION CRITERION · **Origin:** MS (each meter) + INF (the composition rule) · **Confidence:** HIGH for the meters, MEDIUM for the composition rule · **Sources:** P-15, P-16, P-13, P-01, P-02, AT2-02

---

## 3. Scale envelopes by layer

Verdicts: **WITHIN ENVELOPE** (no documented limit violated at the stated scale — *never* "Microsoft says this performs well", see §0) · **CONDITIONAL** (fit depends on the stated, measurable condition) · **BEYOND ENVELOPE** (collides with a documented limit, or with an explicit Microsoft "not the best choice") · **UNPUBLISHED** (Microsoft publishes no figure for this dimension — do not infer one).

### 3.A Application layer

| # | Dimension | Canvas app | Model-driven app | Power Pages | Binding evidence |
|---|---|---|---|---|---|
| 1 | Rows a **non-delegable** expression can see | **BEYOND ENVELOPE** above 500 (default) / 2,000 (max) | n/a (server-side views) | n/a (server-side) | PF-01 |
| 2 | Rows a **delegable** query can filter over | WITHIN ENVELOPE — delegated to source; source limits then apply | WITHIN ENVELOPE | WITHIN ENVELOPE | PF-01, PF-05 |
| 3 | Lookup / relationship traversal depth in one query | **CONDITIONAL** — max 2 lookup levels (1 offline); ≤ 20 entities expanded | WITHIN ENVELOPE | WITHIN ENVELOPE | PF-03 |
| 4 | Single outbound request duration | **CONDITIONAL** — 180 s timeout, 4 retries | UNPUBLISHED (INF: not stated on the limits page — treat as unpublished until verified) | UNPUBLISHED | PF-04 |
| 5 | App size / complexity | **CONDITIONAL** — degrades in Studio at thousands of controls, hundreds of data sources, formulas > 256,000 chars | WITHIN ENVELOPE — metadata-driven | WITHIN ENVELOPE | PF-06, PF-07 |
| 6 | Stated large-implementation reference point | WITHIN ENVELOPE — MS cites "> 100 tables and over 50 screens" as working | UNPUBLISHED | UNPUBLISHED | PF-08 |
| 7 | Data freshness from a Dataverse write | Near-immediate on the primary record | Near-immediate | **BEYOND ENVELOPE** below 15 min — cache SLA is 15 min and is not reducible | PF-19, PF-20 |
| 8 | Static file volume | n/a | n/a | **CONDITIONAL** — Site Checker warns above 500 active web files | PF-21 |
| 9 | Role/permission cardinality | n/a | WITHIN ENVELOPE | **CONDITIONAL** — above 100 web roles "can cause performance issues that affect all web pages" | PF-21 |
| 10 | Concurrent users | **UNPUBLISHED** (INF: no figure on any fetched page — treat as unpublished until verified) | **UNPUBLISHED** | **UNPUBLISHED** — capacity-driven node scaling, no user figure | PF-09, PF-16, PF-42 |

### 3.B Data layer

| # | Dimension | Dataverse | Azure SQL / SQL Server | SharePoint list | Excel | Binding evidence |
|---|---|---|---|---|---|---|
| 11 | Stated maximum data volume | **WITHIN ENVELOPE** — *"no technical limit on the size of a Dataverse environment"*; the ceiling is a purchased-entitlement ceiling, not a technical one | WITHIN ENVELOPE (tier-dependent) | CONDITIONAL — ~5,000 item List View Threshold, not changeable in SharePoint Online (search-derived) | **BEYOND ENVELOPE** above 2,000 rows | PF-17, PF-26, PF-24 |
| 12 | Requests per identity per 5 min | **CONDITIONAL** — 6,000 per web server; web-server count undisclosed and licence-dependent | Connector throttle governs | 600 calls/connection/60 s | n/a | PF-22, PF-27 |
| 13 | Combined execution time per identity per 5 min | **CONDITIONAL** — 1,200 s | UNPUBLISHED | UNPUBLISHED | UNPUBLISHED | PF-22 |
| 14 | Concurrent requests per identity | **CONDITIONAL** — 52 or higher | 125 concurrent calls/connection (DA-10) | UNPUBLISHED | UNPUBLISHED | PF-22, DA-10 |
| 15 | Bulk write strategy | CONDITIONAL — MS says *avoid large batches*; start at 10 with parallelism | Set-based DML | **BEYOND ENVELOPE** for bulk — no bulk API via connector (INF) | BEYOND ENVELOPE | PF-23 |
| 16 | Payload per operation | Governed by flow message size (100 MB / 1 GB chunked) | Gateway payload limits apply | Attachments ≤ 90 MB (Power Apps/Automate); 1,000 MB/min bandwidth per connection | n/a | PF-35, PF-27 |
| 17 | Suitability as a transactional store under load | WITHIN ENVELOPE | WITHIN ENVELOPE | CONDITIONAL — dynamic lookup columns and all-column transmission degrade it | **BEYOND ENVELOPE** — *"Excel isn't a relational database system"* | PF-24, PF-26 |
| 18 | Exemption from service protection | **WITHIN ENVELOPE** for plug-ins / custom workflow activities — a genuine architectural lever | n/a | n/a | n/a | PF-22 |

### 3.C Automation and integration layer

| # | Dimension | Value | Verdict framing | Binding evidence |
|---|---|---|---|---|
| 19 | Actions per flow definition | 500 (nesting 8, switch cases 25, variables 250) | BEYOND ENVELOPE above — split to child flows | PF-33 |
| 20 | Array items in one `Apply to each` | 5,000 (Low) / 100,000 (all others) | BEYOND ENVELOPE above — partition across runs | PF-34 |
| 21 | In-run parallelism | default **1**, max 50 | CONDITIONAL — the default is the commonest cause of "the flow is slow" | PF-34 |
| 22 | Trigger concurrency | off = unlimited runs; on = 1–100 (default 25) and **irreversible**, and drops triggers | TRADE-OFF — see AT2-06; MS says leave it off | PF-36 |
| 23 | Synchronous request timeout | 120 s outbound, 120 s inbound | BEYOND ENVELOPE above — asynchronous pattern required | PF-35 |
| 24 | Asynchronous / long-running | configurable to 30 days; run duration 30 days; pending steps time out at 30 days | WITHIN ENVELOPE | PF-37 |
| 25 | Scheduling floor | 60 s minimum recurrence | BEYOND ENVELOPE below — broker or synchronous call required | PF-32 |
| 26 | Action burst | 100,000 actions / 5 min | CONDITIONAL — licence-independent | PF-29 |
| 27 | Content throughput | 120 MB / 5 min (Low), 1.2 GB / 5 min (others) | CONDITIONAL — the *forgotten* meter in file-heavy designs | PF-31 |
| 28 | Runtime endpoint concurrency | ~1,000 concurrent inbound calls | CONDITIONAL | PF-31 |
| 29 | Custom connector rate | **CONFLICTED / VOLATILE VALUE**: 500 vs 10,000 requests/min per connection across Microsoft pages; connector-count entitlement is also licence/profile-sensitive | **UNKNOWN for commitment until verified/measured**; custom connectors require premium/trial for flow use | PF-27; `integration-architecture.md` IA-C-01 |
| 30 | Retry behaviour | Low: 2 retries; Medium/High: 12 retries exponential to ~1 h; configurable to 90 attempts | CONSTRAINT — retries consume PPR | PF-38 |

### 3.D Availability layer

| # | Dimension | In-region | Cross-region | Binding evidence |
|---|---|---|---|---|
| 31 | Redundancy | ≥ 2 (usually 3) availability zones, typically < 100 km apart, automatic | Opt-in only (SSDR) | PF-39 |
| 32 | RPO | "approximately near zero" | "typical replication lag is under 15 minutes (often under five minutes)" | PF-39, PF-40 |
| 33 | RTO | "under five minutes" | **UNPUBLISHED** — *"Microsoft doesn't publish a cross-region RTO commitment"* | PF-39, PF-40 |
| 34 | Backup retention | 7 days; 28 days only for **production managed environments** | Not replicated unless SSDR is explicitly enabled | PF-41, OP-14 |
| 35 | Prerequisites for cross-region | none | Production type + managed environment (premium tier) + up to 48 h to enable + double storage consumption | PF-40 → LC-24 |
| 36 | Throughput under cross-region protection | full | **degraded** — *"high-volume, highly parallel, or latency-sensitive flows might take longer to start or have lower throughput"* | PF-43 |
| 37 | External-system RPO | out of scope | out of scope — *"fall outside the scope of Power Platform's resiliency commitments"* | PF-44 |

---

## 4. Decision boundaries

These are the boundaries at which a **performance or scale requirement**, on its own, changes the architecture. Each carries its origin tag; none should be read as Microsoft endorsement of the resulting design.

### 4.1 Boundaries that keep the workload inside Power Platform

- **B-01** Interactive queries are expressible with delegable functions against a delegable source (PF-01, PF-02). **MS**
- **B-02** Relationship traversal in one query is ≤ 2 lookup levels and ≤ 20 expanded entities (PF-03). **MS**
- **B-03** Per-identity Dataverse traffic stays below 6,000 requests / 1,200 execution-seconds / 52 concurrent per 5 minutes, and the workload can tolerate `Retry-After` back-off (PF-22). **MS**
- **B-04** Volume work is done by bulk APIs or dataflows, with the flow orchestrating rather than iterating (AT2-08, PF-23). **MS**
- **B-05** Freshness requirements are ≥ 15 minutes wherever Power Pages is the read surface, or the read surface is an app rather than a portal (PF-19). **MS**
- **B-06** Availability requirements are satisfied by in-region zone redundancy: RPO ≈ 0, RTO < 5 min (PF-39). **MS**

### 4.2 Boundaries that force a hybrid design

- **B-07** **Event frequency below 60 seconds, or a synchronous freshness requirement.** The scheduled-recurrence floor is 60 s and per-trigger latency is a per-connector property with no published aggregate (PF-32). → broker push (Service Bus / Event Grid) in front, or a synchronous Dataverse plug-in / Custom API. **MS + INF**
- **B-08** **A single step exceeds 120 seconds synchronously.** → asynchronous pattern, or move the step to a service that permits a longer synchronous window (PF-35). **MS**
- **B-09** **Per-identity Dataverse throughput is the wall.** → distribute across identities, or move the data leg to a plug-in / Custom API, which is *exempt* from service protection (PF-22). This is the highest-leverage documented remedy in the area. **MS**
- **B-10** **Ordering is required at meaningful volume.** Trigger concurrency = 1 buys ordering at the price of dropped triggers and a 100-item `SplitOn` ceiling, and cannot be undone (PF-36, AT2-06). → ordered broker in front, concurrency left off. **MS**
- **B-11** **Public/anonymous read volume is high.** All anonymous Power Pages traffic reaches Dataverse through one service principal, concentrating it on one service-protection budget (PF-25). → cache aggressively, enable CDN, or serve the public surface from a read-optimised store outside Dataverse. **MS + INF**
- **B-12** **Reporting or analytical queries over large volumes.** Dataverse is an OLTP store; analytical scan-and-aggregate work belongs in a replicated analytical store (DA cross-ref; PF-46). **INF over MS facts**
- **B-13** **Cross-region recovery is contractually required with a committed RTO.** Microsoft publishes none (PF-40). → the recovery commitment must be met by design and drill evidence the customer owns, or by an architecture whose RTO is not Power Platform's to make. **MS (absence stated by MS)**

### 4.3 Boundaries that put the workload outside Power Platform

- **B-14** **Compute-bound work.** No Power Platform surface exposes a compute-sizing dial; a plug-in runs in a shared sandbox and its execution time is charged to the triggering request's service-protection budget (PF-45, PF-22). → out of platform. **INF over MS facts**
- **B-15** **Excel as the transactional store under load.** Microsoft's own statement is that it is not a relational database and gives no transaction threshold (PF-26). → out, before any tuning. **MS**
- **B-16** **A hard sub-second, transactionally-visible end-to-end SLA across an app, an automation and an external system.** Nothing in this corpus sizes such a path; the platform publishes no end-to-end latency figure at all (PF-14, PF-U-01). → out, or the SLA is renegotiated. **INF; the absence is MS-stated by omission**
- **B-17** **A workload whose peak is validated only by full-scale load testing against the production service.** Microsoft constrains that testing (PF-15). → the design must be provable from limits, or hosted where load testing is permitted. **MS**

---

## 5. Findings

### 5.1 Application performance — canvas apps

#### PF-01 — The delegation boundary is the hardest scale wall in the platform, and crossing it produces **wrong answers**, not slow ones
- **Classification:** CONSTRAINT + RISK · **Origin:** MS
- **Evidence:** *"When a query is nondelegable, Power Apps gets the first 500 records from the data source and then runs the actions in the query. You can increase this limit to 2,000 records."* *"Power Apps limits the result size to 500 records to keep your app performing well."* And the consequence, stated plainly: *"if your data source has 10 million records and your query needs to work on the last part of the data, like family names that start with 'Z', and your query uses a nondelegable operator like distinct, you only get the first 500 or 2,000 records. So, you get incorrect results."* Also: *"if you use the Filter function with a selection formula that can't be delegated over a data source with a million records, only the first 500 records are scanned. If the record you want is record 501 or 500,001, Filter doesn't find or return it."* And for aggregates: *"Only the first 500 records are averaged. If you're not careful, a user might think a partial answer is the complete answer"* (P-02, `ms.date` 2026-01-13).
- **Why it matters:** This is the single most decision-relevant fact in the area, and it is misfiled by most teams as a *performance* issue. It is a **correctness** issue with a performance disguise. A non-delegable query over a large table returns a plausible, silently truncated answer. No error surfaces at runtime; the only design-time signal is a warning triangle and a blue underline.
- **Decision impact:** Any requirement to *filter, search, sort, aggregate or count over a table that will exceed 2,000 rows* must be satisfiable with delegable functions against a delegable source, or the read must be pre-shaped server-side (view, stored procedure, Dataverse `$filter`/`$select`/`$expand`). If neither is possible, the requirement is outside a canvas app's envelope regardless of how the app is tuned.
- **Conditions:** *"If you work with small data sets (fewer than 500 records), you can use any data source and formula."* The limit is per-query, not per-app.
- **Confidence:** HIGH · **Sources:** P-02

#### PF-02 — Two delegation traps produce **no warning at all**, which makes the design-time signal unreliable as a gate
- **Classification:** RISK · **Origin:** MS
- **Evidence:** (1) *"When you use `With`, `UpdateContext`, or `Set`, these functions create collections internally. Collections are a static in-memory list of records and can't participate in delegation. **You don't see a delegation warning.**"* (2) *"Delegation warnings appear only on formulas that use delegable data sources. If you don't see a warning but think your formula isn't delegated, check your data source type against the list of delegable data sources"* (P-02).
- **Why it matters:** The common review heuristic — "App Checker is clean, therefore delegation is fine" — is unsound in exactly the two cases where a maker is most likely to have worked around delegation: caching into a collection, and using a non-delegable source in the first place.
- **Decision impact:** Delegation compliance cannot be verified by the absence of warnings. It must be verified by (a) confirming every tabular source is on the delegable list, and (b) Microsoft's own test: *"To make sure your app scales to large data sets, set this value to 1. Anything that can't be delegated returns a single record, which is easy to detect when testing your app. This helps you avoid surprises when moving a proof-of-concept app to production."* Encode **Data row limit = 1 during test** as the scale-readiness gate, not warning count.
- **Confidence:** HIGH · **Sources:** P-02

#### PF-03 — Relationship depth is capped at two lookup levels (one offline) and twenty expanded entities, which is a **data-model** constraint expressed as an app limit
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"Power Apps lets you use up to two lookup levels. A Power Fx query expression can include a maximum of two lookup functions to maintain performance… One additional level beyond this is supported as the maximum. **For offline scenarios, only one level of lookup expand is supported.**"* *"You can expand or join up to 20 entities in a single query. If you need to join more than 20 tables in one query, try creating a view on the data server if possible."* Also a non-obvious syntactic constraint: *"Put the property of an entity to be compared on the left hand side (LHS) of an equation"* — the same logical predicate written with the sides reversed does not work (P-02).
- **Why it matters:** A normalised model that reads naturally in SQL can be unreachable from a canvas app. The remedy Microsoft names is a **server-side view**, which means the data model or the source must change — an architecture decision, not an app fix. The offline reduction to one level is a second-order trap: an app that works online silently loses reach offline.
- **Decision impact:** Requirement "users navigate deep relationships" or "users work offline over related data" → validate traversal depth against the model *before* committing to canvas as the surface; budget for server-side views; treat offline as a separate, stricter data-model constraint (cross-ref AA on offline).
- **Confidence:** HIGH · **Sources:** P-02

#### PF-04 — The canvas app request timeout is **180 seconds with 4 retries** — different from Power Automate's 120 s, and the retries are invisible
- **Classification:** FACT · **Origin:** MS
- **Evidence:** *"These limits apply to each single outgoing request: Timeout | 180 seconds; Retry attempts | 4."* With the caveat *"The retry value might vary. For certain error conditions, retrying isn't necessary"* (P-01, `ms.date` 2026-01-12).
- **Why it matters:** Two consequences. First, the app and the automation layers have *different* synchronous budgets (180 s vs 120 s, PF-35), so a call that fits in an app may not fit in a flow and vice versa — a routine source of "it works in the app but the flow times out". Second, up to four automatic retries mean a slow or failing back end multiplies its own load, and each retry consumes a Power Platform request (PF-29).
- **Decision impact:** Size the slowest interactive call against 180 s and design the back end to be idempotent, because retries are automatic and not maker-controlled. Do not assume one user action equals one back-end call.
- **Confidence:** HIGH · **Sources:** P-01

#### PF-05 — Data reaches the client through a layered path, and Microsoft names the two layers that usually dominate
- **Classification:** PATTERN · **Origin:** MS-A
- **Evidence:** Startup is four sequential phases: *"Authenticate the user… Get metadata… Initialize the app: Performs any tasks specified in the OnStart property… Render the screens."* Data calls *"send data to tabular data sources by using connectors over the OData protocol. OData requests flow to back-end layers to reach out to the target data source."* And the diagnosis: *"In many apps, two particular spots commonly present noticeable overhead: **Back-end data source** while processing the request. **Client** while sending the request—or while manipulating the received data on the heap memory and executing the associated JavaScript functions to process data to show in screens."* Dataverse is architecturally shorter: *"data requests go to the environment instance directly—without passing through Azure API Management. Because of this, the performance of data calls is faster compared to the rest of the data sources"* (P-04, `ms.date` 2021-01-22 — **aged**).
- **Why it matters:** It locates the two levers that matter and rules out a third. The levers are *the back end* and *the client's own processing*; the connector/API-Management hop is real but is not where Microsoft points. It also gives the one comparative performance statement Microsoft makes between data sources — Dataverse is faster *because it skips a layer*, not because of tuning.
- **Decision impact:** Where the read surface is a canvas app and latency matters, prefer Dataverse over a connector-mediated source on architectural grounds, and attack back-end query shape and client-side payload before anything else. `OnStart` sits on the critical path of every session (PF-07).
- **Conditions:** Page is aged (2021); the layering has been stable across the corpus but the claim's currency is not vouched for.
- **Confidence:** MEDIUM (aged) · **Sources:** P-04

#### PF-06 — App size degrades the **maker** experience first and the runtime second, with a documented formula-length pathology
- **Classification:** CONSTRAINT · **Origin:** MS-A
- **Evidence:** *"Our studies have shown that nearly all apps with a long load time for Power Apps Studio have at least one formula of more than 256,000 characters. Some apps with the longest load times have formulas of more than 1 million characters."* Comparison: *"in Excel formulas are limited to one expression and are capped at 8,000 characters. Power Apps formulas can grow much longer with the introduction of imperative logic and the chaining operator."* A named amplifier: *"copying and pasting a control with a long formula duplicates the formula in the control's properties without it being realized."* And at the top end: *"Some apps grow to thousands of controls and hundreds of data sources, which slows Power Apps Studio"* (P-06, `ms.date` 2023-04-07 — **aged**).
- **Why it matters:** This is the only quantified complexity threshold Microsoft publishes for canvas apps, and it is about *maintainability throughput*, not user-facing speed. An app that has crossed it is still deliverable but is expensive to change — a technical-debt cost that lands in TCO (→ LC-29) and in lifecycle operations (→ OP-28), not in the runtime budget.
- **Decision impact:** Treat "one app, one screen count" as a design decision with a ceiling. Requirement "one app covers many business areas" → partition into separate apps launched via `Launch()` with state passed as parameters, or use a model-driven app with custom pages as the container. Microsoft documents both.
- **Conditions:** State is lost across `Launch()`: *"State in the original app is lost when another app is launched. Be sure to save any state before you call the Launch function."* Partitioning therefore has a functional cost, not only a benefit.
- **Confidence:** MEDIUM (aged, and the 256,000 figure is presented as a study observation rather than an enforced limit) · **Sources:** P-06

#### PF-07 — `App.OnStart` is a serial critical path; named formulas move the same work off it
- **Classification:** PATTERN + RECOMMENDATION · **Origin:** MS-A
- **Evidence:** *"Because they're a sequence of statements, your app must evaluate these Set and Collect calls in order before it can display the first screen, which makes the app load more slowly."* Against named formulas in `App.Formulas`: *"Because each named formula is independent of the others, Power Apps can analyze them independently… **We've seen Power Apps Studio load time drop by as much as 80% with this change alone.** Your app also loads faster because it doesn't have to evaluate these formulas until it needs the result. The first screen of the app is displayed immediately."* And the boundary: *"Named formulas can't be used in all situations because you can't modify them or use them with Set"* (P-06). Independently corroborated as a top symptom: *"Slow app/page load times | Overloaded OnStart… Move calculations out of OnStart"* (P-03, `ms.date` 2025-02-14).
- **Why it matters:** Deferred evaluation is the highest-yield documented performance change in a canvas app, and it is a *design pattern*, not a setting. It also carries a caveat that is routinely lost: named formulas are immutable, so the pattern does not apply to genuine mutable state.
- **Decision impact:** Startup-latency requirement → `App.Formulas` for everything static; `Set` only for state that actually changes; defer the rest to first use. Where a maker has "moved everything into collections on start" to work around delegation, PF-01 and PF-07 are in direct conflict and the *data model*, not the app, is the thing to fix.
- **Confidence:** MEDIUM (aged; the 80% figure is a Microsoft observation, not a specification) · **Sources:** P-06, P-03

#### PF-08 — Microsoft's only published canvas scale reference point is a **complexity** figure, not a user or volume figure
- **Classification:** FACT · **Origin:** MS
- **Evidence:** *"Power Apps guides you toward well known performant patterns by default. These patterns include streamlined data loading at launch, automatic incremental paging, caching data for collections, and loading only essential data for each page. These proven patterns work well for data-heavy enterprise apps. **Many successful Power Apps implementations use more than 100 tables and over 50 screens while keeping excellent performance.**"* And the counterpart admission: *"Common anti-patterns include loading too much data, turning everything into collections, and overloading OnStart. **People often use these patterns to work around real or perceived Power Apps limitations.** Even with guidance, you might still use a bad pattern and end up with a slow app"* (P-05, `ms.date` 2026-08-20).
- **Why it matters:** This is the closest Microsoft comes to a scale statement for canvas apps, and it deliberately measures *artefact complexity* (tables, screens) rather than *load* (users, transactions, rows). That asymmetry is itself the finding: Microsoft will describe how big an app can be, not how many people can use it at once (PF-09). The second quotation is unusually candid negative evidence — Microsoft naming its own workaround-driven anti-patterns.
- **Decision impact:** Do not use "100 tables / 50 screens" as a capacity answer to a concurrency question. Use it only to rebut "canvas apps don't scale to enterprise data models", which it does support.
- **Confidence:** HIGH (for what it says) · **Sources:** P-05

#### PF-09 — **No concurrent-user figure is published for any Power Platform application surface**
- **Classification:** UNKNOWN · **Origin:** MS (absence) + INF
- **Evidence:** No concurrent-user, requests-per-second or sessions-per-environment figure appears on: `power-apps/limits-and-config` (P-01), `power-pages/system-requirements` (P-12), the performance-efficiency pillar (P-17, P-18, P-19, P-20), or the Architecture Center performance pages (P-21, P-22). Microsoft instead directs sizing at the *request* meters (P-18: *"Evaluate your API request consumption against your available capacity and the service protection limits"*) and warns that measurement is environment-specific (P-15). The limits page's own framing is device-level: *"Performance testing and results can vary between device types… Make sure the test results meet your business requirements before you roll out the solutions in production"* (P-01).
- **Why it matters:** "How many concurrent users can it take?" — the first question every sponsor asks — **has no documented answer**, and answering it with a number would be inventing a threshold. The defensible reformulation is per-meter: concurrency becomes *requests per identity per 5 minutes* (PF-22) and *calls per connection per window* (PF-27), both of which are published.
- **Decision impact:** Reformulate every concurrency requirement into the five units of §2 before attempting a verdict. Where the sponsor needs a concurrency assurance, the only honest routes are (a) a proof of concept, which Microsoft recommends (P-18: *"Small-scale pilot projects or prototypes can help you gather real-time data"*), or (b) load testing, which Microsoft constrains (PF-15). Record the residual as a Risky claim, never as Confirmed.
- **Confidence:** HIGH that the figure is unpublished; the *absence* is INF over six fetched pages — treat as unpublished until verified.
- **Sources:** P-01, P-12, P-15, P-17, P-18, P-19, P-20, P-21, P-22

#### PF-10 — Preloading trades startup latency against exposing compiled app assets on unauthenticated endpoints
- **Classification:** TRADE-OFF · **Origin:** MS
- **Evidence:** The **Preload app for enhanced performance** setting: *"This makes the compiled app assets accessible via unauthenticated endpoints to enable loading them before authentication. However, users can still only use your app to access data via connectors only after authentication and authorization completes… Compiled app assets include a collection of JavaScript files containing text authored in app controls (such as PCF controls), media assets (such as images), the app name, and the environment URL the app resides in… If media and information must be added to the app, without coming from a connection, and it is considered sensitive you may want to disable this setting. Note, disabling this setting will result in users waiting a bit longer to access an app"* (P-23, `ms.date` 2024-12-10).
- **Why it matters:** A rare, explicit **performance ↔ security** trade-off with a named data-exposure surface. Data stays protected; *authored content* (labels, hard-coded text, images, environment URL) does not.
- **Decision impact:** Requirement "fast app start" + governance constraint "no unauthenticated exposure of any solution content" → these conflict; the decision needs an owner. Apps that hard-code business terminology, customer names or internal URLs in control text should not be preloaded.
- **Confidence:** HIGH · **Sources:** P-23

### 5.2 Application performance — model-driven apps and the Dataverse client

#### PF-11 — Microsoft's only published client-latency recommendation is **≤ 150 ms**, and it is aged
- **Classification:** RECOMMENDATION · **Origin:** MS-A
- **Evidence:** *"Of particular importance is the **Latency Test** row value. This value is an average of twenty individual test runs. Generally, the lower the number, the better the performance of the client. Although users may receive a satisfactory experience by using connections with more latency, **for best application performance we recommend that the value be 150 ms (milliseconds) or less.**"* A diagnostic exists: `https://myorg.crm.dynamics.com/tools/diagnostics/diag.aspx` (P-08, `ms.date` 2020-09-11 — **aged, six years**).
- **Why it matters:** It is the only network threshold Microsoft publishes anywhere in this corpus, and it is measurable before a line is built. It converts a vague "users in region X complain" into a testable pre-condition.
- **Decision impact:** Requirement "users in geography X" → measure client-to-environment latency with the diagnostic before choosing the environment region; treat > 150 ms as a Risky claim needing a mitigation (region placement, or a design with fewer round trips). Note the figure predates the modern Unified Interface, so it is a screening threshold, not an SLA.
- **Conditions:** Documented for customer-engagement apps / model-driven clients. No equivalent figure exists for canvas apps or Power Pages — do not port it across surfaces.
- **Confidence:** MEDIUM (aged) · **Sources:** P-08

#### PF-12 — Bandwidth and latency are independent, and a request/reply design multiplies latency by round trips
- **Classification:** FACT · **Origin:** MS-A
- **Evidence:** *"One of the main causes of poor performance of customer engagement apps is the latency of the network over which the clients connect to the organization."* *"Networks with high bandwidth don't guarantee low latency. For example, a network path traversing a satellite link often has high latency, even though throughput is very high. It's common for a network round trip traversing a satellite link to have five or more seconds of latency. An application designed to send a request, wait for a reply, send another request, wait for another reply, and so on, will wait at least five seconds for each packet exchange, regardless of the speed of the server."* Also: *"even if the latency of a network connection is low, bandwidth can become a performance degradation factor if there are many resources sharing the network connection"* (P-08).
- **Why it matters:** It names the exact failure mode that the N+1 anti-pattern (PF-46) produces on a high-latency link: chattiness is multiplied by latency, and no server-side tuning helps. It also supplies a concrete adverse-condition figure (5+ s satellite round trip) for field, maritime, mining and remote-site scenarios.
- **Decision impact:** Requirement "remote sites, satellite or cellular connectivity" → the design constraint is **round-trip count**, not payload size. Batch, precompute, or go offline-first (cross-ref AA offline). Reject designs whose per-screen round-trip count is unbounded.
- **Confidence:** MEDIUM (aged) · **Sources:** P-08

#### PF-13 — Client platform, not app design, sets the ceiling on parallel data retrieval
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"The performance of an app might vary when loading large sets of data on different platforms like iOS or Android. This variation happens because of different network request limitations on each platform. **For example, the number of concurrent network requests allowed differs by platform.** These differences can have a major impact act on the data load time for large datasets"* (P-23, `ms.date` 2024-12-10). Reinforced device-side: *"Check the scenarios that exceed the memory threshold of the JS heap"* (P-04). And an explicit test warning: *"Performance testing and results can vary between device types such as mobile, desktop, and laptops. Factors include processing power, memory capacity, network connectivity, app complexity, and other apps running in parallel on a device"* (P-01).
- **Why it matters:** The same app is a different performance artefact on each client, and Microsoft **does not publish the per-platform concurrency numbers**. So the one lever that would let you predict mobile data-load time is undocumented.
- **Decision impact:** Requirement "mobile as primary device" → performance acceptance must be tested on the actual target devices, not on a desktop browser; the design should minimise the *number* of startup calls rather than rely on parallelism, because the parallelism budget is client-set and unpublished.
- **Conditions:** Per-platform concurrent-request counts are **UNPUBLISHED** (PF-U-02) — treat as unpublished until verified.
- **Confidence:** HIGH (that the variation exists and is platform-set) / UNKNOWN (magnitude) · **Sources:** P-23, P-04, P-01

#### PF-14 — There is **no published end-to-end latency figure** for any Power Platform path
- **Classification:** UNKNOWN · **Origin:** MS (absence) + INF
- **Evidence:** The limits pages publish *timeouts* (180 s app, 120 s flow) and *floors* (60 s recurrence, 5 s/1 s postpone), never expected latency. The performance pillar's own facilitation section directs the reader to Application Insights to *measure* latency rather than to any published figure (P-17). Microsoft's advice on targets makes the reason explicit: *"When using services that abstract the underlying platform, don't set goals that are tied to factors you don't control. For instance, setting a target of 200 ms for a screen load would be unrealistic if the baseline performance is already 250 ms, before you even have a chance to incorporate your custom logic"* (P-17, `ms.date` 2025-08-15). AT2-11 reaches the same conclusion for automation: latency is a **per-connector** property, not a platform property.
- **Why it matters:** Microsoft is telling customers that the platform's own baseline is a number the customer must *discover*, and that targets should be set relative to it. Any latency commitment made before that baseline is measured is unfounded.
- **Decision impact:** A latency or freshness SLA cannot be validated from documentation. Sequence it: (1) measure the baseline on the target surface, region and device; (2) set the target above it; (3) if the required target is below the measured baseline, the requirement is out of envelope (B-16) and either the design or the SLA must change. Record any pre-measurement latency commitment as **Risky**.
- **Confidence:** HIGH that no figure is published (INF over the fetched limits and pillar pages — treat as unpublished until verified) · **Sources:** P-17, P-01, AT2-11

#### PF-15 — Microsoft **constrains load testing** against its own service, which removes the standard way of proving peak capacity
- **Classification:** CONSTRAINT + RISK · **Origin:** MS
- **Evidence:** *"When planning and running performance tests it's important to remember that, in many cases, the Microsoft Cloud uses shared infrastructure to host your assets and the assets belonging to other customers. **Limit tests to avoid unintended consequences**"* (P-20, `ms.date` 2026-07-17). At the same time the pillar demands testing in a production-like environment: *"Mirror your production environment… Provision sufficient resources… Replicate network conditions"* and names stress, soak and spike testing as the ways to find breaking points.
- **Why it matters:** A genuine, under-discussed tension. RE:06 and PE:05 ask for chaos and stress testing; PE:05 then tells you to limit the tests because the infrastructure is shared. The practical effect is that **the breaking point of a Power Platform workload is normally not empirically established before go-live**, and confidence rests on limit arithmetic plus a pilot.
- **Decision impact:** Requirement "prove the system survives the seasonal peak" → do not promise a load-test-verified answer. Deliver instead: limit arithmetic in the five units of §2, a pilot at representative-but-bounded scale (P-18 endorses pilots), throttling-rate monitoring in production (→ OP-08), and a documented degradation plan. Where the peak is genuinely existential and must be proven, that is an argument for hosting the peak-bearing component where load testing is unconstrained (B-17).
- **Confidence:** HIGH · **Sources:** P-20, P-18

### 5.3 Application performance — Power Pages

#### PF-16 — Power Pages scales its own application nodes, but the scaling dial is **licensing capacity**, not a performance setting
- **Classification:** FACT + TRADE-OFF · **Origin:** MS
- **Evidence:** *"Each Power Pages production website consists of at least two application server nodes hosted in different Azure datacenter regions to provide high availability and disaster recovery. Azure Traffic Manager constantly monitors these nodes and directs traffic to the node that is available."* Each site gets *"an Azure Traffic Manager instance that is set in active/passive mode"*. The primary region *"is determined by the primary region of the Power Platform organization to maintain minimal latency between Dataverse and the website"*. And the load-bearing sentence: ***"Scaling of these application servers is done automatically based on the Power Pages licensing capacity assigned to the environment."*** CDN is available but *"isn't enabled by default"*; an out-of-the-box WAF exists; external CDN/WAF providers (Azure Front Door, Akamai, Cloudflare, Imperva) are supported (P-09, `ms.date` 2026-04-28).
- **Why it matters:** This is the most direct **performance ↔ cost** coupling in the platform, and it is stated by Microsoft rather than inferred: to give a Power Pages site more server capacity you *buy more licensing capacity*. Performance headroom is therefore a procurement decision, not an architectural one. Second: Traffic Manager is **active/passive**, so the second node is a failover node, not a load-sharing node — the published architecture does not describe horizontal scale-out across regions.
- **Decision impact:** Requirement "public site must absorb a campaign peak" → the lever is assigned Power Pages capacity (→ LC-12, LC-13) plus caching and CDN, and the CDN must be *deliberately enabled*. Do not model the two nodes as doubling throughput. Do not expect a Power Pages site to be faster than the Dataverse region it is pinned to.
- **Conditions:** The relationship between a given capacity assignment and the resulting node count or throughput is **UNPUBLISHED** (PF-U-03) — treat as unpublished until verified.
- **Confidence:** HIGH · **Sources:** P-09

#### PF-17 — Power Pages performance depends on a server-side cache whose refresh SLA is **15 minutes and cannot be shortened**
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"In order to improve scalability and performance, Power Pages websites cache the data that is queried from Microsoft Dataverse. This caching is done on the application server for all business data and website metadata."* Configuration tables: *"All configuration table data is same for all users and is cached automatically… **Automatic cache update has a service level agreement of 15 minutes.**"* Data tables: *"This data is typically cached per user except in certain cases like anonymous users or tables with global permission. Also only the data accessed by user on the website is cached and not the data for whole table."* Invalidation: *"Any record for a table (or a related table) is created, updated, or deleted on the website by any website user. The action will instantaneously clear the cache for all the website users for that specific table. Cache is cleared automatically within 15 minutes even if no changes are made."* And the explicit refusal: *"Can I change the cache refresh duration from 15 minutes to a lesser duration? **No. SLA for cache refresh remains 15 minutes.**"* (P-10, `ms.date` 2026-04-29).
- **Why it matters:** Power Pages is architecturally a **cached read surface**. That is why it scales, and it is also a hard functional boundary: any requirement for sub-15-minute visibility of a change made *outside* the website is not satisfiable by configuration.
- **Decision impact:** Requirement "external users must see the updated status immediately" → satisfiable only if the update is made *on the website* by a user (which invalidates instantly) or on the primary record of a website-initiated write. Otherwise the requirement is out of envelope for Power Pages and the read surface must change (B-05). Note the per-user cache: an anonymous or global-permission table is cached once for everyone, an authenticated per-user table is cached per user — so cache effectiveness *falls* as user count rises for per-user data.
- **Confidence:** HIGH · **Sources:** P-10

#### PF-18 — Microsoft explicitly warns that **plug-in and workflow writes are not guaranteed to reach a Power Pages site promptly**, and calls the pattern not recommended
- **Classification:** ANTI-PATTERN · **Origin:** MS
- **Evidence:** *"I'm using plugins or workflows to update data in other tables and need these data changes to reflect immediately on my website. **This design approach isn't recommended. Except the primary record where the create or update action is triggered, data reflection from Dataverse to websites is never guaranteed to be immediate.**"* Conversely, website→Dataverse is prompt: *"How long does it take for changes to reflect from a website to Dataverse? Immediately, as long as the update changes a primary record and isn't based on indirect changes to data using post operation plugins or workflows"* (P-10).
- **Why it matters:** The asymmetry is the finding. Writes *from* the portal are immediate; derived values computed *by server-side logic* are not visible on a predictable schedule. A design that shows a user a status field computed by a plug-in is showing them a value that may be up to 15 minutes stale, with no error.
- **Decision impact:** Requirement "portal shows a derived/calculated status" → compute it on the primary record in the same transaction as the user's write, or accept up to 15 minutes of staleness and design the UI to say so. Do not build a portal experience that depends on asynchronous server-side derivation being fast. (Note: `automation-architecture.md` corrected an earlier over-broad reading of this evidence — the quotation is scoped to Dataverse→Power Pages freshness and must not be cited as a general statement about flow write visibility.)
- **Confidence:** HIGH · **Sources:** P-10, AT2 §0 (scoping correction)

#### PF-19 — Clearing the Power Pages cache is an **operational hazard on a live site**
- **Classification:** RISK · **Origin:** MS
- **Evidence:** *"Updates to the data in configuration tables or invoking the clear cache or config actions should be performed during non-peak hours. Frequent or too many table changes may adversely affect website performance."* And: *"The clear cache option should be seldom used as it clears cache for all data tables as well as configuration tables and can cause temporary slowness. **For live site with heavy usage, this can lead to users facing performance issues**"* (P-10).
- **Why it matters:** The remedy for the 15-minute staleness (PF-17) is itself a performance incident on a busy site. So the two obvious responses to "content isn't updating" — change configuration more often, or clear the cache — both degrade the thing they are meant to fix.
- **Decision impact:** Content-change frequency is a **design parameter** for Power Pages, not a free operational action. High-churn content belongs in data tables (per-table invalidation) rather than configuration tables (global invalidation). Cache clearing needs a change-window procedure (→ OP-19).
- **Confidence:** HIGH · **Sources:** P-10

#### PF-20 — Site Checker publishes the only concrete Power Pages design thresholds: **500 web files, 200 lookup records, 100 web roles**
- **Classification:** DECISION CRITERION · **Origin:** MS-A
- **Evidence:** Web files: *"having a large number of these files can cause slowness during the startup of your website. The Site Checker tool will check for this scenario and provide you an indication if you have **more than 500 active web files**"*; remedy is *"an external file server like Azure Blob Storage or Azure Content Delivery Network"*, or re-parenting files off the home page (a web file is loaded with the home page if its parent page is home). Lookups: *"Enabling a lookup to render as a dropdown mode in basic forms or advanced forms can lead to performance issues if **the number of records shown in the dropdown list exceeds 200** and the records are changed frequently. Use this option for only static lookups, such as country and state lists"*; at scale *"it can slow the entire website by using website resources to render this page"*. Web roles: *"If the **number of web roles exceeds 100** in your website, it can cause performance issues that affect all web pages."* Output caching: *"Disabling header output cache on your website can lead to performance issues in your website during high load"* (same for footer) (P-11, `ms.date` 2023-03-03 — **aged**).
- **Why it matters:** These are the only numeric Power Pages design limits in the corpus, and two of them are *modelling* constraints in disguise: 100 web roles is a **security-model** ceiling with a performance consequence, and 200 lookup records is a **data-model** ceiling. A permission model designed without this knowledge can make every page on the site slow.
- **Decision impact:** Requirement "fine-grained external permissions" → cap distinct web roles well below 100 and express variation through table permissions and record ownership rather than role proliferation (cross-ref governance). Requirement "external users select from a large reference list" → full lookup control or a custom AJAX control, never a dropdown. Static assets → external CDN/blob above ~500 files. Verify header/footer output caching is on before any launch.
- **Conditions:** Page is aged (2023) and several of its other checks reference retired features (page tracking, sign-in tracking), so the *thresholds* should be spot-checked before encoding (PF-U-04).
- **Confidence:** MEDIUM (aged) · **Sources:** P-11

#### PF-21 — Power Pages publishes **no request, throughput or concurrency limits at all**
- **Classification:** UNKNOWN · **Origin:** MS (absence) + INF
- **Evidence:** `power-pages/system-requirements` (P-12, `ms.date` 2026-04-28) — the page whose title promises "system requirements and limits" — contains browser support, operating-system support, IP address guidance, required service domains, a proxy warning and a pointer to Dataverse column-type limits. It contains **no** limit on sites per environment, pages per site, requests per second, concurrent sessions, table permissions, web roles, or payload size. The only numeric Power Pages design figures in the corpus come from Site Checker (PF-20) and the licensing capacity model (→ LC-12).
- **Why it matters:** For a product positioned for *"business-critical websites"* (P-09) and public internet exposure, the absence of a published request or concurrency envelope is material. It means a public-facing scale requirement cannot be validated against documentation, and the only published dial is a commercial one (capacity, PF-16).
- **Decision impact:** Any external-facing volume requirement (campaign traffic, seasonal registration peak, public incident spike) must be treated as **Unknown**, sized by the Dataverse identity constraint underneath it (PF-25), and de-risked commercially (capacity headroom, → LC-13) and architecturally (CDN, caching, static offload). Do not represent a Power Pages concurrency figure to a sponsor; there isn't one.
- **Confidence:** HIGH that no figures are published on the named page (INF for the absence — treat as unpublished until verified) · **Sources:** P-12, P-09

### 5.4 Data access performance

#### PF-22 — Dataverse's real throughput wall is service protection: **6,000 requests / 1,200 execution-seconds / 52 concurrent per identity per 5 minutes, per web server** — and the web-server count is undisclosed and licence-dependent
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"Two of the service protection API limits use a five-minute (300 second) sliding window."* Per web server: *"Number of requests | 6,000 within the five-minute sliding window"*; *"Execution time | 20 minutes (1,200 seconds) within the five-minute sliding window"*; *"Number of concurrent requests | 52 or higher"*. Scope: *"The system evaluates service protection API limits for each user. Each authenticated user has an independent limit."* Server count: *"Each web server that your environment makes available enforces these limits independently. Most environments have more than one web server. **Trial environments allocate only a single web server.** Multiple factors determine the actual number of web servers that your environment makes available… **One of the factors is how many user licenses you purchase.**"* Errors: `0x80072322` (request count), `0x80072321` (execution time), `0x80072326` (concurrency), with `Retry-After`. Escalating back-off: *"If the application continues to send such demanding requests, the duration is extended to minimize the impact on shared resources."* Exemption: *"**Service protection limits don't apply to data operations that originate from plug-ins and custom workflow activities.** Plug-ins and custom workflow activities run within the isolated sandbox service"* — but *"the extra computation time that these operations contribute is added to the initial request that triggered them"* (P-15, `ms.date` 2026-01-09).
- **Why it matters:** Four consequences that reshape sizing. (1) Effective Dataverse throughput for an environment is **not a published number** — it is 6,000 × (undisclosed web-server count) per identity per 5 min, and that count moves with licensing. (2) A **trial environment has one web server**, so a proof of concept measures the worst case and a production environment will behave differently — in both directions. (3) Because limits are per *identity*, any design that funnels traffic through one account (service principal, portal, integration user) concentrates all of it on one budget. (4) The plug-in exemption is a real architectural lever: the same data work costs service-protection budget in a flow and none in a plug-in.
- **Decision impact:** High-volume Dataverse write requirement → plan against 6,000 requests / 1,200 execution-seconds / 52 concurrent per identity per 5 min, then choose deliberately between: spreading across identities (*"Distribute loads across service principles rather than a single user"*, DA-10), moderate batching with parallelism, or moving the data leg into a plug-in / Custom API (B-09). Instrument for **both** `0x80072322` and `0x80072321`, and treat a shift from one to the other as the signal that batch size is now the problem.
- **Conditions:** *"These limits can change and might vary between different environments. These numbers represent default values."* Dataverse search is separately metered at *"one request per second for each user"* on a different API.
- **Confidence:** HIGH · **Sources:** P-15, DA-10

#### PF-23 — Microsoft's throughput guidance contradicts the "batch everything" reflex, and its own recommended method is **empirical, not calculated**
- **Classification:** RECOMMENDATION · **Origin:** MS
- **Evidence:** *"**Avoid large batches.** Most scenarios are fastest sending single requests with a high degree of parallelism. If you feel batch size might improve performance, start with a small batch size of 10 and increase concurrency until you start getting service protection API limit errors that you retry."* *"With the SDK for .NET, this approach means using ExecuteMultipleRequest, which typically allows sending up to 1,000 operations in a request. The main benefit… is that it reduces the total amount of XML payload… For service protection limits, it increases the total execution time per request. **Larger sized batches increase the chance you encounter execution time limits rather than limits on the number of requests.**"* And the method: *"**Don't try to calculate how many requests to send at a time. Each environment can be different.** Gradually increase the rate you send requests until you begin to hit limits and then depend on the service protection API limit Retry-After value to tell you when to send more. This value keeps your total throughput at the highest possible level."* Also *"Use multiple threads"* and, on strategy: *"If your current business processes depend on large periodic nightly, weekly, or monthly jobs that attempt to process large amounts of data in a short period of time, consider how you might enable a real-time data integration strategy"* (P-15).
- **Why it matters:** Three things worth encoding. (1) Batching does not create capacity — it *moves* consumption from the request meter to the execution-time meter, so a 1,000-operation batch can pass one limit and fail the other. (2) Microsoft's recommended tuning method is adaptive back-off, which means a compliant high-volume integration must be **written to be throttled** rather than sized to avoid throttling. (3) Microsoft's structural advice is to *stop doing big batch windows*, which is an architecture recommendation, not a tuning tip.
- **Decision impact:** Bulk-load or migration requirement → prefer `CreateMultiple`/bulk for entitlement efficiency and atomic intent; prefer moderate batches (order of 10) with parallelism for raw throughput; implement `Retry-After` handling as a functional requirement, not an error handler. Nightly-window requirement → challenge the window itself before sizing it (B-12 adjacency). A migration with a fixed cut-over window is a performance requirement and must be tested: *"If migrating data from a prior system and migration must be completed in a specific time window, your performance testing should include measuring performance of the data migration"* (P-20).
- **Confidence:** HIGH · **Sources:** P-15, P-20

#### PF-24 — SharePoint as an application data store carries three compounding performance penalties, one of which Microsoft names as a partitioning requirement
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** (1) Dynamic columns: *"SharePoint supports various data types, including dynamic lookups such as Person, Group, and Calculated. If a list defines too many dynamic columns, it takes more time to manipulate these dynamic columns within SharePoint before returning data to the client running the canvas app. To avoid this, don't overuse the dynamic lookup columns in SharePoint. For example, use static columns to keep email aliases or people's names."* (2) All-column transmission: *"The number of columns in the list affects the performance of the data requests. This is because the matched records, or the records up to the defined data row limits, are retrieved and transmitted back to the client with all the columns defined in the list—**even if the app doesn't use all of them**."* (3) Volume: *"If you have a large list with hundreds of thousands of records, consider partitioning the list or splitting it into several lists based on parameters such as categories, or date and time. For instance, your data might be stored in different lists on a yearly or monthly basis. In such a case, you can design the app to let a user select a time window and retrieve the data within that range"* (P-23, `ms.date` 2024-12-10). Connector throttle: *"API calls per connection | 600 | 60 seconds"*, bandwidth *"Maximum number of megabytes being transferred to/from the connector within a bandwidth time interval (per connection) | 1000"* per 60,000 ms, and *"This connector supports list item attachment sizes up to 90 MB"* (P-13, `ms.date` 2024-03-01, page updated 2026-08-01). Microsoft also flags delegation as a known connector limitation: *"If you get an incomplete data set, or if you can't get accurate results from a SharePoint list, this problem might by caused by delegation limits"* (P-13).
- **Why it matters:** The second point is the one teams miss: **column count is a performance parameter even for unused columns**, because the connector returns the whole row. A wide list is slow for every read regardless of how narrow the app's use of it is. The third point is Microsoft telling you that beyond "hundreds of thousands" of records the *data architecture* must change (time-partitioned lists with a user-selected window) — which is a functional constraint on the UI, not a tuning step.
- **Decision impact:** Requirement "SharePoint list as the app's data store" → cap column count and avoid Person/Group/Calculated columns for anything read at scale; size against 600 calls/connection/60 s and 1,000 MB/min; above ~hundreds of thousands of rows the design must partition and the UI must expose the partition key. If the requirement resists all three, the store is wrong (cross-ref DA on SharePoint-as-database).
- **Conditions:** The ~5,000-item List View Threshold and the 30-million-item list ceiling are **search-derived** in this pass (P-24) and not fetched from a Tier-1 page — verify before encoding (PF-U-05).
- **Confidence:** HIGH for the connector figures and the three penalties; MEDIUM for the SharePoint platform thresholds · **Sources:** P-23, P-13, P-24

#### PF-25 — A portal or service-principal design **concentrates all traffic on one identity**, and Microsoft names the required UI behaviour when it throttles
- **Classification:** CONSTRAINT + PATTERN · **Origin:** MS
- **Evidence:** *"Portal applications typically send requests from anonymous users through a service principal account. **Because the service protection API limits are based on a per user basis, portal applications can hit service protection API limits based on the amount of traffic the portal experiences.** Like interactive client applications, don't display service protection API limits errors to the portal end user. The UI for the portal should disable further requests and display a message that the server is busy. The message might include the time when the application can begin accepting new requests calculated using the Retry-After duration returned with the error"* (P-15).
- **Why it matters:** This is the mechanism that makes PF-21's missing Power Pages concurrency figure tractable. The public-facing scale ceiling is not a portal figure — it is the **per-identity Dataverse budget** shared by every anonymous visitor. It also means the portal's cache (PF-17) is not a nice-to-have: it is the thing standing between visitor volume and a single service-protection budget.
- **Decision impact:** Public-facing volume requirement → (1) maximise cacheability (anonymous and global-permission tables cache once for all users, PF-17); (2) offload static content to CDN/blob (PF-20); (3) design a graceful busy state driven by `Retry-After` as a **functional requirement**; (4) where volume is genuinely high, serve the public read surface from a store that is not one Dataverse identity (B-11). Interactive client applications get the same instruction: *"Client application developers shouldn't just throw the error to display the message to the user. The error message isn't intended for end users."*
- **Confidence:** HIGH · **Sources:** P-15

#### PF-26 — Microsoft states Excel is not a database and **declines to give a transaction threshold**
- **Classification:** ANTI-PATTERN + UNKNOWN · **Origin:** MS
- **Evidence:** *"It restricts the canvas app to loading data from the table only up to 2,000 records due to limited delegable functions. To load more than 2,000 records, partition your data in different data tables as other data sources."* And: *"**Note the limitations of Excel as a database. Excel isn't a relational database system**: Any changes from an app are managed by Excel in the same way as if a user were changing data in an Excel file directly. If the app has a high number of reads, but fewer update operations, it might perform well. However, if the app requires heavy transactions, it can adversely affect the performance of the app. **There's no specific threshold value for the number of transactions.** It also depends on the data being manipulated"* (P-23).
- **Why it matters:** A rare case where Microsoft names an anti-pattern *and* explicitly refuses to quantify the boundary. That refusal is the useful part: it means "how many transactions can Excel take?" is unanswerable, so the decision must be made on shape (read-heavy vs write-heavy) rather than volume.
- **Decision impact:** Excel-as-source is acceptable only for read-mostly reference data under 2,000 rows. Any multi-user write requirement → move the store (Dataverse or SQL) before designing the app. This is a Discovery-detectable signal: "the data lives in a spreadsheet everyone edits" plus "several people update it during the day" is out of envelope without needing a volume number.
- **Confidence:** HIGH · **Sources:** P-23

#### PF-27 — Connector throttles are per **connection** and are usually the first meter to bite
- **Classification:** CONSTRAINT + VOLATILE VALUE · **Origin:** MS
- **Evidence:** SharePoint: 600 API calls per connection per 60 s; 1,000 MB per 60 s bandwidth per connection (P-13). **Custom connector rate is CONFLICTED:** the Power Automate limits page (P-16, updated 2026-07-17) states 500 requests/minute/connection, while Microsoft's Custom Connector FAQ (Cross-Block V2 verification, updated 2025-09-04) states 10,000 requests/minute/connection for Power Apps/Power Automate. This 20× disagreement is `integration-architecture.md` IA-C-01 and neither value is a stable design constant. Microsoft's own ranking remains useful: *"Individual connectors have their own limits, **which you often reach before the limits mentioned previously**. Be sure to check the documentation for your connector"* (P-16). The framing of throttling behaviour: *"Connector throttling in Power Automate refers to the mechanism by which connectors enforce rate limits or usage quotas… **Every connector has its own throttling limit.** When a flow runs into connector-level throttling limits, the service returns error code 429 (Too Many Requests) with error text like Rate limit is exceeded. Try again in 27 seconds"* (P-25, `ms.date` 2025-07-11). And the interaction with parallelism: *"a concurrent loop in a Power Automate flow processing each item at a time could surpass the request limits of a connector used in the loop's logic"* (P-19, `ms.date` 2025-08-15).
- **Why it matters:** Microsoft states the ordering explicitly — connector limits bite before platform limits. And because they are per *connection*, they are affected by an identity and sharing decision (how many connections exist, owned by whom) rather than by app or flow design. This is the meter most often absent from sizing conversations and the one most likely to cause the first production incident.
- **Decision impact:** Every connector on the critical path must have its own throttle read from its own reference page and entered into the sizing model (§2 unit 3). Raising in-run parallelism (PF-34) without re-checking the connector throttle at the new parallelism converts a slow flow into a throttled one. Where the throttle is binding and cannot be raised, the remedies are: fewer calls (query shaping), more connections/identities, or a different integration path.
- **Confidence:** HIGH for the general per-connection/throttling principle; **CONFLICTED** for the current custom-connector numeric value · **Sources:** P-13, P-16, P-25, P-19, `integration-architecture.md` IA-C-01

#### PF-28 — Query shaping, not parallelism, is the first throughput lever — because every meter counts **requests**
- **Classification:** PATTERN · **Origin:** MS
- **Evidence:** From the Well-Architected data guidance: *"Optimize query performance… Use server-side views to prefilter data"*; *"**Avoid the N+1 query problem.** Minimize the number of roundtrips to the database by using joins and batch fetching to retrieve related data efficiently"*; *"Reorder joins… Cache queries… Store the results of frequently run queries for easy reuse"*; *"Only load the data that you need in an app or flow. Use server-side views to prefilter data to narrow down data relevant to your query"* (P-18, P-19). AT2-09 records the automation-side equivalent (trigger conditions, `$expand`/`$select`/`$filter` collapsing N calls into one).
- **Why it matters:** It establishes the correct tuning order. Because the binding meters count *requests* and *execution time* rather than *runs*, reducing the number of calls dominates every other optimisation — and it is the only one that improves all five meters of §2 simultaneously. Parallelism improves wall-clock time while making three of the five meters worse.
- **Decision impact:** Fixed tuning order for any performance finding: (1) don't make the call at all (trigger conditions, deferred loading, caching); (2) make fewer, wider calls (`$expand`, `$select`, server-side views, joins); (3) only then tune parallelism, and re-check the connector throttle at the new setting (PF-27).
- **Confidence:** HIGH · **Sources:** P-18, P-19, AT2-09

### 5.5 Automation performance

> This subsection states only what is needed to compose automation limits with app and data limits. The automation *shape* decision (workflow vs orchestration vs integration vs distributed processing), the alternatives envelope (Logic Apps, Functions, Durable Functions, Service Bus) and the reliability semantics (idempotency, ordering, compensation) are in `automation-architecture.md` and are **not** repeated here.

#### PF-29 — A flow's throughput class is a property of its **owner's licence**, and it degrades silently on an HR event
- **Classification:** CONSTRAINT + RISK · **Origin:** MS
- **Evidence:** *"A flow's performance profile determines its Power Platform request limits."* Profile membership: **Low** = Free, Microsoft 365 plans, Power Apps Plan 1 / Per App, Power Automate Plan 1, all trials, Dynamics 365 Team Member, Power Apps for Developer. **Medium** = Power Apps-triggered flows, manual flows, child flows, Power Apps Plan 2 / per user, Power Automate Plan 2 / Premium, Dynamics 365 Enterprise and Professional, and non-licensed/application/special-free-licence users. **High** = Power Automate Process, per-flow plan. **Unlimited Extended** = pay-as-you-go flows, Dynamics-in-context flows under a service principal. *"A cloud flow uses the plan of its owner. If a cloud flow is shared with multiple people, then generally the owner is the flow's creator… **If the original owner leaves the organization, the flow reverts to the Low performance profile.**"* *"If a user has multiple plans… the flow has the performance profile of the higher of the plans"* (P-16, `ms.date` 2026-07-17).
- **Why it matters:** The same flow definition can lose 98% of its daily request ceiling (500,000 → 10,000) through a leaver, with no code change and no design-time warning. Note also that **Power Apps-triggered, manual and child flows are Medium by definition**, which is a rare case where the *trigger type* sets the throughput class.
- **Decision impact:** Business-critical automation → own it with a service principal or assign a Process/capacity licence to the flow deliberately; never let throughput depend on an individual's personal licence. Record flow ownership as an architectural decision with a named owner (→ OP-04, LC-08).
- **Confidence:** HIGH · **Sources:** P-16, AT2-01

#### PF-30 — The Power Platform request model is mid-transition, so today's compliant design can be throttled on a date the customer does not control
- **Classification:** RISK · **Origin:** MS
- **Evidence:** Official per-24 h limits: 40,000 (paid Power Platform / Dynamics 365 excluding Team Member), 6,000 (pay-as-you-go, Power Apps per app, Microsoft 365 apps with Power Platform access, Dynamics 365 Team Member), 250,000 (Power Automate per flow, Copilot Studio base and add-on), 200 (paid Power Apps Portals login). The 5-minute limit is *"100,000 requests and it's independent of a user's license."* Transition-period figures are higher (Premium 200k per cloud flow, Process 500k per licence, Free 10k per cloud flow). The flow limits page carries the reconciliation verbatim: *"These limits represent approximations of how many requests are allowed daily. They aren't guarantees."* Microsoft's instruction: *"**Build your cloud flows based on official limits.**"* Timing: *"Any possible high usage enforcement won't happen until six months after Power Platform Request usage reporting is generally available"* and *"**There's no current ETA for when GA happens.**"* Transition-only quirks: a *"separate per user level limit of 1,000,000 cloud flow actions"*; *"manual cloud flows don't use the flow owners/flow invokers limits. Every manual cloud flow has a performance profile of Medium… **After the transition period, manual cloud flows will use the request limits of invoking user**"*; *"stacking of user licenses isn't supported"*; capacity add-ons *"aren't assignable to users or cloud flows during the transition period"* (P-26, `ms.date` 2026-08-14; P-16).
- **Why it matters:** Every one of those quirks flips at an unknown date. The most consequential is manual flows moving from a fixed Medium profile to the *invoking user's* limits — which can turn a widely-shared instant flow from comfortably-sized into throttled overnight, with no change to the flow.
- **Decision impact:** Size against **official** limits, not transition numbers. Treat "we are within limits today" as a Confirmed claim with a short half-life and an explicit revalidation trigger (the PPR reporting GA announcement). Flag any design that depends on transition-only generosity — especially widely-shared manual flows — as **Risky** with a named tripwire (→ OP-26).
- **Confidence:** HIGH · **Sources:** P-26, P-16, AT2-03

#### PF-31 — The meters teams forget: **content throughput**, **runtime endpoint concurrency** and the **action burst cap**
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** Content throughput (data read from or written to run history): *"Content throughput per 5 minutes | 120 MB for Low; 1.2 GB for all others"*; *"Content throughput per 24 hours | 200 MB for Low; 2 GB for Medium; 10 GB for High"* (transition: 2.5 GB / 20 GB / 50 GB). Runtime endpoint: *"Concurrent inbound calls | ~1,000"*; *"Read calls per 5 minutes | 6,000 for Low; 60,000 for all others"*; *"Invoke calls per 5 minutes | 4,500 for Low; 45,000 for all others"*. Concurrent outbound calls: *"500 for Low; 2,500 for all others"*. Action burst: *"Action burst limits refer to the maximum number of actions that can be triggered in a specific period, typically measured in a rolling window of time. **Currently, the cap is 100,000 actions in five minutes.** To stay under this limit, distribute the load between multiple flows using child flows or add trigger conditions"* (P-16, P-25).
- **Why it matters:** File-moving automations are the classic victim. A flow that copies documents is well inside the action count and the daily request entitlement but can exhaust **200 MB per 24 hours** on a Low profile — a limit almost nobody plans against, and one that scales with *payload*, not with *activity*. Similarly, an app that calls a flow synchronously for every user action is sized by the ~1,000 concurrent-inbound-call ceiling, not by the daily entitlement.
- **Decision impact:** Any document- or attachment-heavy automation must be sized in **bytes per window**, and the owner's performance profile becomes a throughput decision (200 MB vs 10 GB per day is a 50× difference driven purely by licence, → LC-08). App→flow synchronous call patterns must be sized against runtime endpoint concurrency. High-frequency designs must be sized against the 100,000-action 5-minute burst cap, which is licence-independent.
- **Confidence:** HIGH · **Sources:** P-16, P-25

#### PF-32 — Sub-minute event frequency is a **mechanism** problem, not a tuning problem
- **Classification:** CONSTRAINT · **Origin:** MS + INF
- **Evidence:** *"Minimum recurrence interval | 60 seconds"*; *"Maximum recurrence interval | 500 days"*; *"Minimum postpone interval | Five (5) seconds for Low, one (1) second for all other performance profiles"* (P-16). Per-trigger latency is a per-connector property with no published aggregate (AT2-11), and some managed connectors are materially slower than the recurrence floor — the Service Bus connector, for instance, long-polls and waits 30 seconds for more messages before the next poll (AT2-11 quoting the connector reference).
- **Why it matters:** The 60-second floor applies to *scheduled recurrence*, which is a different mechanism from an event/webhook trigger. Conflating them produces two opposite errors: concluding that nothing can react faster than a minute (false — webhook triggers can), and assuming a polling trigger will react in seconds (false — bounded below by that connector's own interval).
- **Decision impact:** Answer freshness requirements *per trigger*, never from the limits page: (a) source pushes via event/webhook → lowest available latency, bounded by that connector's behaviour; (b) polling trigger → bounded by that connector's documented poll interval; (c) requirement tighter than the connector's interval → the trigger mechanism is wrong, and the answer is a broker push, a Dataverse plug-in, or a synchronous call (B-07).
- **Conditions:** Current per-licence polling intervals are **UNKNOWN** in this corpus; `data-architecture.md` records a conflict between an older 15 min / 5 min statement and the current profile-based page (DA U-20, AT2 U-02). Do not quote a polling-interval number.
- **Confidence:** HIGH for the floors; UNKNOWN for polling intervals · **Sources:** P-16, AT2-11

#### PF-33 — Structural flow limits are a **maintainability** ceiling that Microsoft says bites before the stated number
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"Actions per workflow | 500 | **Flows with a large number of actions might encounter performance issues while you edit them, even if they have fewer than 500.** Consider using child flows to reduce the number of actions in a single flow or if you need more than 500."* *"Allowed nesting depth for actions | 8"*; *"Switch scope cases limit | 25"*; *"Variables per workflow | 250"*; *"Characters per expression | 8,192"*; *"Length of action or trigger name | 80 characters"*; *"Maximum size of trackedProperties | 16,000 characters"*. Also *"Number of flows owned by a single user | 600 | Use flows under solutions if you need more than 600"* (P-16). Microsoft's framing: *"You might encounter limits on the complexity of a flow that are defined at the design and definition level. **Consider redesigning your flow if you encounter them**"* (P-25).
- **Why it matters:** Same shape as PF-06 for apps: the published number is not the practical one, and the cost lands on change velocity rather than runtime. Microsoft's own remedy for hitting it is *redesign*, not a bigger limit.
- **Decision impact:** Treat approaching these limits as a signal that the process decomposition is wrong, not that the platform is small. Child flows are the documented remedy — but note child flows are **Medium** profile by definition (PF-29) and, for pay-as-you-go, child cloud/attended runs are not separately charged while unattended child runs are (→ LC-19).
- **Confidence:** HIGH · **Sources:** P-16, P-25

#### PF-34 — In-run parallelism **defaults to 1**, and the array a loop can process is set by the owner's profile
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"Apply to each array item | 5,000 for Low, 100,000 for all others"*; *"Apply to each concurrency | **1 is the default limit.** You can change the default to a value between 1 and 50 inclusively"*; *"Until iterations | Default: 60 - Maximum: 5,000"*; *"Paginated items | 5,000 for Low, 100,000 for all others | To process more items, trigger multiple flow runs over your data"*; *"Split on items | 5,000 for Low without trigger concurrency - 100,000 for all others without trigger concurrency - **100 with trigger concurrency**"* (P-16).
- **Why it matters:** The default of 1 means most loops process strictly sequentially unless someone changed a setting — a very common cause of "the flow is slow" that is a *configuration* fact, not a platform limit. Conversely raising it to 50 multiplies instantaneous pressure on the connector and service-protection meters (PF-27, PF-22).
- **Decision impact:** For independent per-record work inside one run, raise `Apply to each` concurrency **before** touching trigger concurrency, then re-verify the connector throttle at the new parallelism. Above the profile's array ceiling, partition across runs rather than seeking a bigger loop.
- **Confidence:** HIGH · **Sources:** P-16

#### PF-35 — The synchronous budget is **120 seconds** in and out, and the message ceiling is 100 MB (1 GB chunked)
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"Outbound synchronous request | 120 seconds (2 minutes) | **Tip**: For longer-running operations, use an asynchronous polling pattern or an 'Until' loop."* *"Outbound asynchronous request | Configurable up to 30 days."* *"Inbound request | 120 seconds (2 minutes)… Flows that contain a response action including Respond to Copilot, HTTP Response, and Respond to a PowerApp or flow always return a response within this limit. Child flows that start before the response action continue running separately, and actions after the response action continue running beyond this limit, enabling a flow to respond and continue running other operations."* *"Message size | 100 MB | To work around this limit, consider allowing chunking… **When you send files through a connector, the overall size of the payload and not just the file needs to be under 100 MB.**"* *"Message size with chunking | 1 GB."* *"Expression evaluation limit | 131,072 characters"*; *"Request URL character limit | 16,384 characters"*. Testing artefact: *"If you test a cloud flow that runs for longer than 10 minutes, you might get a timeout message in Power Automate, even though the flow continues to run in the background"* (P-16).
- **Why it matters:** The inbound-response detail is the useful, under-known part: a flow *can* respond inside 120 s and keep working afterwards, which is the documented pattern for "the app needs an answer now but the work takes longer". And the payload note matters — 100 MB is the *whole payload*, not the file, so metadata-heavy calls hit it earlier than expected.
- **Decision impact:** Requirement "app waits for the answer" → design for a response inside 120 s with the remainder continuing asynchronously; do not extend the synchronous path. Requirement "process large documents" → size the whole payload, confirm the specific connector supports chunking (*"some connectors and APIs might not support chunking or even the default limit"*), and size against content throughput too (PF-31).
- **Confidence:** HIGH · **Sources:** P-16

#### PF-36 — Trigger concurrency is an irreversible one-way door that also **caps and can drop** incoming triggers
- **Classification:** TRADE-OFF + RISK · **Origin:** MS
- **Evidence:** *"Concurrent runs | Unlimited for flows with Concurrency Control turned off - 1 to 100 when Concurrency Control is turned on (defaults to 25) | **Turning on Concurrency Control can't be undone without deleting and re-adding the trigger.**"* *"Waiting runs | Not applicable when Concurrency Control is off - 10 plus the degree of parallelism (1-100) when Concurrency Control is on | **Additional triggers that arrive while the waiting runs limit is met might be re-tried by the connector. However, the retry attempts might not succeed if the maximum waiting limit continues to be met for an extended period of time. To ensure all triggers result in flow runs, leave the Concurrency Control setting off in the flow's trigger.**"* Plus the `SplitOn` collapse to 100 items with concurrency on (P-16).
- **Why it matters:** The sharpest reliability trade-off in the product. Turning concurrency on to obtain ordering *introduces trigger loss* under sustained load, shrinks debatching by three orders of magnitude, and cannot be reverted without recreating the trigger.
- **Decision impact:** Ordering requirement → do **not** reach for trigger concurrency = 1 at any meaningful volume; that trade is "ordered but lossy". Put an ordered broker in front and leave concurrency off (B-10). Use concurrency = 1 only for low-volume, order-sensitive, loss-tolerant single-record processing, isolated in a small child flow.
- **Confidence:** HIGH · **Sources:** P-16, AT2-06

#### PF-37 — Long-running work is supported to 30 days, but the run **and its history** both expire at 30 days
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"Run duration | 30 days | Run duration is calculated using a run's start time and includes flows with pending steps like approvals. **After 30 days, any pending steps time out.**"* *"Run retention in storage | 30 days | Run retention is calculated using a run's start time"* (P-16).
- **Why it matters:** Two distinct consequences that get conflated. (1) A business process with a human step that can legitimately take longer than a month **cannot be held open in a single flow run** — the approval times out. (2) Run history, which is the transactional record of what happened (→ OP-11), is gone after 30 days, so any audit or dispute-resolution requirement with a longer horizon needs telemetry or a business record outside the run.
- **Decision impact:** Requirement "process may wait months for a counterparty" → the state must live in a business record (a Dataverse process row) with a re-triggering flow, not in a suspended run (AT2 shape: PROCESS ORCHESTRATION). Requirement "we must be able to show what happened 90 days ago" → export telemetry (→ OP-11), because run history will not be there.
- **Confidence:** HIGH · **Sources:** P-16

#### PF-38 — Retries are automatic, profile-dependent, and consume the same meters as real work
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** Defaults: *"Low | This policy sends up to two retries at exponentially increasing intervals, which scale by 5 minutes up to an interval of approximately 10 minutes for the last retry."* *"Medium, High | This policy sends up to 12 retries at exponentially increasing intervals, which scale by seven (7) seconds up to an interval of approximately 1 hour for the last retry."* Settings ceilings: *"Retry attempts | 90"*; *"Retry maximum delay | One (1) day"*; *"Retry minimum delay | Five (5) seconds"*. And the accounting: *"Both successful and failed actions count toward limits, but not skipped actions… **Retries and extra requests from pagination count as actions**"* (P-16, P-25).
- **Why it matters:** Three compounding effects. (1) A failing dependency does not reduce load, it *multiplies* it — up to 12× per action on Medium/High. (2) Those retries are billed against PPR, so an outage in a downstream system consumes the automation's entitlement (→ LC-09). (3) The default retry envelope differs by profile, so the same flow behaves differently under different owners (PF-29).
- **Decision impact:** Any integration with an unreliable dependency must have its retry policy set deliberately rather than inherited, must be idempotent (AT2-17), and its throttling/failure rate must be monitored (→ OP-08) — because the platform's response to failure is more load, and the platform's response to sustained overload is to turn the flow off after 14 days (PF-39).
- **Confidence:** HIGH · **Sources:** P-16, P-25

#### PF-39 — Automation does not fail loudly at the limit; it slows, then is **turned off**, and editing the flow erases the evidence
- **Classification:** RISK · **Origin:** MS
- **Evidence:** *"If a cloud flow exceeds one of the limits, flow activity slows. It automatically resumes when the sliding window has activity below the limit. However, **if a cloud flow consistently remains above the limits for 14 days, the system turns it off.** Be sure to monitor email for notifications about such flows."* *"Because these limits are for a single version, **if you update your flow, it resets the limits.**"* Suspension rules: *"Flows with errors | 14 days | A cloud flow that has a trigger or actions that fail continuously is turned off."* *"Flows without trigger activity | 90 days… Flows owned by users with premium licenses or assigned capacity licenses (Power Automate Process, per flow) aren't subject to this suspension. Flow owners and co-owners are notified 30 days prior to suspension."* *"Consistently throttled flows | 14 days… Assign Power Automate Process licenses to the flow to dedicate capacity and avoid throttling"* (P-16). Also: *"Flows can be turned on again at any time, but if they continue to violate the limits, they continue to get turned off"* (P-25).
- **Why it matters:** The failure mode is *quiet degradation followed by silent death two weeks later*, with the notification going to an individual's mailbox. And the version-reset behaviour means throttling history is **not durable evidence**: a redeployment masks the symptom without fixing the design, so "we edited it and it's fine now" is not a resolution.
- **Decision impact:** Any production automation needs a monitored throttling-rate signal and a named owner, or it will stop without anyone deciding that it should (→ OP-04, OP-08). Note that the 90-day inactivity suspension is *licence-dependent* — a low-frequency but business-critical flow (quarterly close, annual renewal) owned by a non-premium user will be switched off between runs, which is a licensing decision presenting as an availability failure (→ LC-08).
- **Confidence:** HIGH · **Sources:** P-16, P-25

### 5.6 Availability and reliability

#### PF-40 — In-region resilience is automatic and quantified: **RPO ≈ 0, RTO < 5 minutes**, across ≥ 2 availability zones
- **Classification:** FACT · **Origin:** MS
- **Evidence:** *"A geography has at least one Azure region, which usually includes three availability zones but never has fewer than two availability zones."* *"Microsoft automatically detects availability zone-level failures and switches to other availability zones in the region almost instantly to protect you from data loss while keeping downtime near zero in most cases."* *"Zone-redundant data services replicate data across multiple zones… **The recovery point objective is near zero, and the recovery time objective is less than five minutes.**"* *"Availability zones are typically separated by several kilometers and are usually within 100 kilometers."* Scope: *"This in-region capability is for production environments that host business-critical application processes and data. **To avoid disruption, don't deploy production processes and data in nonproduction types like sandbox, developer, or trial environments**"* (P-27, `ms.date` 2026-08-20). Corroborated: *"Environments designated for production workloads are replicated synchronously across at least two (and typically three) physically separated Azure zones within the selected region… ensuring zero data loss and rapid failover (recovery time objective or RTO < 5 minutes)"* (P-28, `ms.date` 2026-05-04).
- **Why it matters:** These are the only RTO/RPO numbers Microsoft publishes for Power Platform, they are strong, and they are free — but only for **production-type** environments. That last clause is a governance requirement disguised as an availability fact: a business-critical workload running in a sandbox or developer environment has no such protection.
- **Decision impact:** Availability requirements satisfied by RPO ≈ 0 / RTO < 5 min within one region need **no** additional architecture (B-06). This also settles a common question: for single-region resilience, Power Platform is stronger out of the box than most self-built alternatives. Conversely, the requirement "the workload lives in a production-type environment" becomes a hard architectural constraint, with the licensing consequence that production and sandbox environments consume capacity while trial/developer do not (→ LC-05).
- **Confidence:** HIGH · **Sources:** P-27, P-28

#### PF-41 — Cross-region recovery is **opt-in, gated, capacity-doubling, and carries no published RTO commitment**
- **Classification:** CONSTRAINT + TRADE-OFF · **Origin:** MS
- **Evidence:** *"Self-service disaster recovery is a Power Platform infrastructure capability that lets you replicate your environment across long distances and start environment failover between regions yourself… **This capability is available only for production environments.**"* Region pairing: *"Most geographies have region pairs separated by at least 300 miles when possible."* Enablement: *"The process can take up to 48 hours to finish."* Cost and gating: *"**You must select a managed environment.** This environment requires a premium license tier"*; *"suppose you have 10 GB of capacity consumption in the primary location. When you turn on self-service disaster recovery, you create a copy of the data in the remote secondary region and this copy consumes another 10 GB."* Objectives: *"typical replication lag is under 15 minutes (often under five minutes), and the platform is designed to complete failover within minutes once initiated. **Because customers retain control of when and whether to trigger a cross-region failover, Microsoft doesn't publish a cross-region RTO commitment.**"* The critical default: *"**Database backups are not replicated to secondary regions** for scenarios supported by self-service disaster recovery, unless you explicitly allow self-service disaster recovery. Without self-service disaster recovery, backups remain in the primary region only, which means cross-region failover can't be guaranteed."* Coverage gaps: *"Regions that don't have a regional Azure pair aren't supported"* — as of November 2025 Austria East, Belgium Central, Chile Central, Indonesia Central, Israel Central, Italy North, Malaysia West, Mexico Central, New Zealand North and Poland Central are single regions; *"Brazil and South Africa don't have self-service disaster recovery because their regional pairs are in heavily constrained regions"*; UAE *"continues to be capacity-constrained"*. Disabling *"deletes all replicated environment data in the paired region"* (P-27).
- **Why it matters:** Four independent gates before regional resilience exists at all: production type, managed environment (premium licence), a supported region pair, and 48 hours. Then it costs a second copy of storage. And even then there is **no RTO commitment**, because Microsoft has moved the trigger decision to the customer. The backup-replication default is the sharpest point: without SSDR explicitly enabled, backups sit in the primary region only, so a regional loss is not recoverable from backup.
- **Decision impact:** Requirement "survive the loss of a region" → this is an architecture *and* a licensing *and* a region-selection decision taken together (→ LC-24, OP-18). Requirement "committed cross-region RTO in a contract" → cannot be met by citing Microsoft; it must be met by the customer's own drill evidence and monitored replication lag, or the commitment must change (B-13). Any solution in a single-region geography (the November 2025 list, Brazil, South Africa) has **no cross-region option** — that is a data-residency-versus-resilience trade-off that must be surfaced in Discovery.
- **Conditions:** The region list is dated November 2025 and will change; re-verify. Fabric link, Synapse Link, Copilot Studio conversation runtime, Customer Insights – Data, Project Operations and Commerce Scale Units are explicitly **not** covered by SSDR failover.
- **Confidence:** HIGH · **Sources:** P-27

#### PF-42 — Enabling cross-region protection **degrades automation throughput** — Microsoft says so
- **Classification:** TRADE-OFF + RISK · **Origin:** MS
- **Evidence:** *"Power Automate desktop flows and cloud flows support failover and failback with self-service disaster recovery but have known performance limitations."* And verbatim: *"**Power Automate environments enabled for self-service disaster recovery run on isolated, runtime capacity. Most workloads shouldn't notice a difference, but high-volume, highly parallel, or latency-sensitive flows might take longer to start or have lower throughput. Validate business-critical workloads before enabling this feature.**"* Enablement additionally requires opting in via a sign-up form (P-27, as of October 2025).
- **Why it matters:** A direct, Microsoft-stated conflict between **resilience** and **performance**, and it lands precisely on the workloads most likely to need both. It also inverts the usual assumption that a DR feature is transparent to the runtime.
- **Decision impact:** Requirement "high-volume automation" + requirement "cross-region DR" → these interact and must be validated together, on the same environment, before commitment. Microsoft's own instruction is to validate business-critical workloads before enabling. This is a strong argument for keeping high-throughput automation *out* of the SSDR-enabled environment where the data-residency requirement permits — an environment-strategy consequence (→ OP-20).
- **Confidence:** HIGH · **Sources:** P-27

#### PF-43 — The resilience of anything Power Platform **integrates with** is explicitly out of scope
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** *"It's important to note that when Power Platform solutions connect to external systems—such as SQL Server, REST APIs, or other third-party services—**the RPO of those integrations are governed by the availability and recovery capabilities of the respective target systems, and fall outside the scope of Power Platform's resiliency commitments.**"* And in the known-limitations list: *"Connectors might have recovery problems when dependent on external systems, like SharePoint, SQL server, or third-party applications."* Also *"You should validate any connectors that use hard-coded to primary region endpoints for failover and failback"* (P-27).
- **Why it matters:** It bounds the whole availability story. A solution's real RPO/RTO is the **worst** of its own and every dependency's — and Power Platform's strong in-region numbers (PF-40) say nothing about the ERP, the on-premises SQL instance, or the third-party API on the critical path. Hard-coded region endpoints in connectors are a named failure mode after failover.
- **Decision impact:** Availability analysis must be done **per flow across dependencies**, not per platform (this is RE:02/RE:03 — identify and rate flows, then failure-mode analysis). For each critical business flow, record the dependency with the weakest recovery capability; that is the solution's actual objective. Never quote Power Platform's RTO/RPO as the solution's RTO/RPO when an external dependency is on the path.
- **Confidence:** HIGH · **Sources:** P-27, P-29 (RE:02, RE:03)

#### PF-44 — Deployment and administrative operations are themselves **performance events on production**
- **Classification:** CONSTRAINT · **Origin:** MS-A
- **Evidence:** *"Microsoft recommends that you don't execute operations that require concurrent database transactions. Also, don't execute operations that require intensive database transactions during normal business hours, when users are most likely to access the system. Example operations that require intensive database transactions include: Enable one or more language packs; **Solution import, upgrade, delete, or export**; Install or upgrade apps from Microsoft Marketplace or the Dynamics 365 admin center; **Publish customizations**; Large bulk record operations, such as business unit changes"* (P-07, `ms.date` 2020-09-08 — **aged, six years**). Independently, solution import is named as a service-protection-heavy operation: *"Batch operations, importing solutions, and highly complex queries can be very demanding"* (P-15).
- **Why it matters:** This is a genuine **performance ↔ operations** coupling and it is easy to miss: the ALM process that makes the solution safe to change (pipelines, solution import, publish) is itself a load event on the production database. A team that deploys during business hours to "reduce risk" is choosing a different risk.
- **Decision impact:** Deployment windows are a performance requirement, not just a change-management convenience (→ OP-16). Requirement "frequent releases" + requirement "no degradation during business hours" → these conflict and the resolution is a release calendar, not a tuning setting. Bulk security-model changes (business unit reassignment) are explicitly named and should be treated as a maintenance-window operation.
- **Conditions:** Page is six years old; the Dataverse storage engine has changed substantially since. Corroborated in part by the current service-protection page, so the *direction* is safe; treat the specific list as indicative (PF-U-06).
- **Confidence:** MEDIUM (aged, partially corroborated) · **Sources:** P-07, P-15

### 5.7 Performance architecture patterns

#### PF-45 — Microsoft's own pattern catalogue for performance: cache, partition, queue, precompute, archive, co-locate
- **Classification:** PATTERN · **Origin:** MS
- **Evidence:** **Caching** — *"Caching stores commonly accessed data in a fast-access storage area… This method is most effective on static data or data that rarely changes."* Three named layers: *"In-memory caching… For example, you can use variables in cloud flows or collections in canvas apps to cache data"*; *"Database query caching… Also consider using server-side views where possible to prefilter data"*; *"Content delivery network caching… effective for static content, like images, CSS files, and JavaScript files."* **Partitioning** — vertical (*"Divide a table into smaller tables by selecting specific columns"*) and horizontal/sharding (*"Split data based on rows or ranges of values"*), with *"if using Dataverse Elastic tables consider what should be the partitioning key."* **Queues** — *"A queue is a storage buffer located between a requesting component (producer) and the processing component (consumer)… A queue is often the best way to hand off work to a processing service that experiences peaks in demand"*, citing the Queue-Based Load Leveling pattern. **Precomputation** — *"use Dataverse calculated columns, rollup fields or Power Fx columns instead of calculating the value in code and storing it with a save operation."* **Asynchrony** — *"Evaluate if work could be done asynchronously instead of synchronously in your logic. For example, instead of performing the operation inline, consider implementing a Power Automate flow to process the work asynchronously."* **Archive and purge** — *"Archiving relocates older, less-frequently accessed data to more cost-effective storage… Reducing data volume: Less data means faster processing times… Reducing backup and recovery times."* **Data proximity** — *"the strategic placement of data closer to the users or services that access it most frequently."* **Read/write separation** — *"Many Azure database services support read replicas"* (P-18, P-19, `ms.date` 2025-08-15).
- **Why it matters:** Every one of these is available in or adjacent to Power Platform, and the mapping to native features is explicit: caching → collections/variables/server-side views/CDN; precomputation → rollup, calculated and Power Fx columns; partitioning → elastic table partition keys and time-sliced lists; queues → Service Bus / work queues; archive → Dataverse long-term retention. This is the constructive counterpart to §6: the anti-patterns are what happens when these are absent.
- **Decision impact:** Use as the standard remediation ladder when a performance requirement is at the edge of the envelope, applied in the PF-28 order (eliminate calls → widen calls → parallelise). Note two Microsoft-stated caveats that make these patterns non-free: *"If underlying data changes frequently, implement a cache invalidation mechanism to ensure that the cached data remains up to date"* (cache staleness), and *"Before you enable concurrency, keep in mind that this means multiple actions will be performed at the same time—if you're writing data as part of the loop, ensure the destination of the data can handle simultaneous requests"* (parallelism pushes the problem downstream).
- **Confidence:** HIGH · **Sources:** P-18, P-19

#### PF-46 — Read/write separation and analytical offload are the documented answer to reporting load, not query tuning
- **Classification:** PATTERN · **Origin:** INF over MS facts
- **Evidence:** The performance pillar distinguishes OLTP from OLAP explicitly (*"Online analytical processing (OLAP): A technology that organizes large business databases, supports complex analysis, and performs complex analytical queries **without negatively affecting transactional systems**"*) and recommends read replicas where available (P-18). Dataverse's throughput wall is per-identity request and execution-time budget (PF-22), which reporting queries consume from the same budget as transactional work. `data-architecture.md` carries the replication mechanisms (Synapse Link, Fabric link) and their trade-offs. Elastic tables and long-term retention are the in-platform volume levers (DA cross-ref).
- **Why it matters:** Reporting is the most common source of "the app got slow and nothing changed" — a new dashboard or an increasingly ambitious view starts consuming the same service-protection budget as the transactional workload, and the symptom appears in the app rather than in the report.
- **Decision impact:** Any requirement combining "operational app" with "cross-entity analytics over history" should separate the read path from the write path at design time rather than after the incident. In-platform first (server-side views, rollups, archived history out of the hot store), then replication to an analytical store. Note the resilience consequence: Fabric link and Synapse Link are **not** covered by SSDR failover (PF-41), so an analytical dependency introduces an unprotected component.
- **Confidence:** MEDIUM (the pattern is MS-endorsed generically; the specific Dataverse-budget-contention mechanism is INF over PF-22) · **Sources:** P-18, PF-22, DA cross-ref

---

## 6. Anti-patterns

Each entry names the requirement that usually produces it, so it is detectable in Discovery rather than only in review.

| # | Anti-pattern | Usually caused by the requirement… | Documented consequence | Origin | Sources |
|---|---|---|---|---|---|
| **PF-AP-01** | **Non-delegable query over a large table.** Filtering, sorting, aggregating or counting with non-delegable functions where the table will exceed 2,000 rows. | "users need to search/filter freely" | Silently **wrong answers**, not slow ones: only the first 500/2,000 rows are examined | MS | P-02 |
| **PF-AP-02** | **Collect-everything-into-a-collection.** Loading a table into a collection to escape delegation. | "delegation warnings blocked us" | Large network payload, client memory pressure, no delegation warning shown, and the 500/2,000 ceiling still applies to the source read | MS | P-02, P-05 |
| **PF-AP-03** | **Overloaded `OnStart`.** Serial `Set`/`Collect` chains before the first screen renders. | "have everything ready when the app opens" | Named by Microsoft as a top cause of slow app/page load | MS | P-05, P-03, P-06 |
| **PF-AP-04** | **Select N+1 in a gallery.** `LookUp`/`Filter`/`First` against a data source inside a gallery or loop. | "show related details in the list" | Microsoft's worked example: a 50-row gallery becomes **51 network requests** | MS | P-21 |
| **PF-AP-05** | **Cross-screen references.** A control on screen A reading a control on screen B. | "reuse what the user already entered" | Forces Power Apps to fully load and evaluate **both** screens before showing one; flagged by App Checker as "Inefficient Delay Loading" | MS | P-21 |
| **PF-AP-06** | **Massive per-record loop in a flow.** `Apply to each` doing per-record work over thousands of items. | "process the whole file/table nightly" | Concurrency defaults to 1; array ceiling 5,000 (Low); every action consumes PPR; retries multiply it | MS | P-16, AT2-08 |
| **PF-AP-07** | **Excessive synchronous calls.** App or flow waiting on a chain of dependent calls. | "the user must see the result immediately" | 120 s flow / 180 s app timeouts; on a high-latency link, latency multiplies by round trips (5+ s each on satellite) | MS | P-16, P-01, P-08 |
| **PF-AP-08** | **Polling instead of subscribing.** Scheduled flows checking for change. | "keep the systems in sync" | Bounded below by the 60 s recurrence floor and the connector's own poll interval; consumes PPR on every empty check | MS | P-16, AT2-11 |
| **PF-AP-09** | **Ignoring connector throttling.** Sizing only against PPR. | "we're well inside our daily limit" | Microsoft: connector limits are *"often reached before"* platform limits; 429 with `Retry-After` | MS | P-16, P-25 |
| **PF-AP-10** | **Power Platform as a compute host.** Real calculation inside a flow or plug-in. | "it just needs to do the maths" | No compute-sizing dial exists; plug-in execution time is charged to the triggering request's service-protection budget | INF over MS | P-15 |
| **PF-AP-11** | **Wide SharePoint list as the app database.** Many columns, dynamic lookups, hundreds of thousands of rows. | "the data already lives in SharePoint" | All defined columns transmitted even if unused; dynamic columns add server-side work; Microsoft says partition the list | MS | P-23, P-13 |
| **PF-AP-12** | **Excel as the transactional store.** Multi-user writes to a workbook. | "we're replacing a spreadsheet" | 2,000-row ceiling; *"Excel isn't a relational database system"*; no transaction threshold published | MS | P-23 |
| **PF-AP-13** | **Trigger concurrency = 1 for ordering.** Serialising a high-volume trigger. | "records must be processed in order" | Ordered **but lossy**: waiting-run cap drops triggers; `SplitOn` collapses to 100; irreversible without recreating the trigger | MS | P-16 |
| **PF-AP-14** | **Sizing against the biggest published number.** Quoting 500,000 requests/day or "no size limit" as the capacity answer. | sponsor asks "will it scale?" | Ignores the four other meters of §2, of which connector and service protection normally bind first; and quotes *transition-period* figures Microsoft says not to build against | MS | P-15, P-26, P-16 |
| **PF-AP-15** | **Deploying during business hours.** Solution import / publish customisations on a busy production environment. | "release when the team is available" | Microsoft names solution import, publish customisations and bulk business-unit changes as intensive database operations to avoid during business hours | MS-A | P-07 |
| **PF-AP-16** | **Reporting from the transactional store.** Dashboards and cross-entity views against live Dataverse. | "we need live reporting" | Consumes the same per-identity service-protection budget as transactional work; symptom appears in the app | INF over MS | PF-22, P-18 |
| **PF-AP-17** | **Business-critical workload in a non-production environment.** | "the sandbox was already set up" | No zone-redundant protection (Microsoft: *"don't deploy production processes and data in nonproduction types"*); trials are **not backed up**; trial environments have a **single web server**, so service-protection headroom is at its minimum | MS | P-27, P-30, P-15 |
| **PF-AP-18** | **Depending on transition-period generosity.** Especially widely-shared manual flows relying on the fixed Medium profile. | "it's been fine for a year" | Microsoft: build against official limits; manual flows will move to the *invoking user's* limits at an unannounced date | MS | P-26 |

---

## 7. Decision criteria

**REQUIREMENT → PERFORMANCE CONSTRAINT → ARCHITECTURAL CONSEQUENCE.** These are the observable or measurable requirements that change the architecture on performance grounds alone. Each is phrased so it can be asked in Discovery without naming a product.

| # | Requirement (technology-neutral) | Performance constraint | Architectural consequence |
|---|---|---|---|
| **DC-01** | How many rows will the largest table hold at year 3, and must users filter/sort/aggregate freely over all of them? | Non-delegable expressions see only 500 (default) / 2,000 (max) rows and return truncated results silently (PF-01) | Above ~2,000 rows every interactive query must be delegable, or reads must be pre-shaped server-side. Test with data row limit = 1. If neither is possible, the interactive surface is out of envelope |
| **DC-02** | How deep are the relationships a user must traverse in a single view? | Max 2 lookup levels (1 offline), ≤ 20 expanded entities (PF-03) | Deeper traversal forces server-side views, a flattened model, or a different surface. Offline is a stricter, separate constraint |
| **DC-03** | How many business records will one identity create or update per five minutes at peak? | 6,000 requests / 1,200 execution-seconds / 52 concurrent per identity per 5 min, per web server; web-server count undisclosed (PF-22) | Above it: distribute across identities, batch moderately with parallelism, or move the data leg to a plug-in / Custom API (exempt). Never size from the daily entitlement |
| **DC-04** | Does all traffic reach the data store through one account (integration user, service principal, public portal)? | Service protection is per identity, so one account is one budget regardless of user count (PF-25) | Public/anonymous and integration designs need caching, CDN, identity distribution, or a separate read store. Design a `Retry-After`-driven busy state as a functional requirement |
| **DC-05** | How fresh must the data be on the screen the user is looking at? | Power Pages server-side cache SLA is 15 min and not reducible; derived values from server-side logic are *"never guaranteed to be immediate"* (PF-17, PF-18) | Sub-15-minute freshness rules out Power Pages as the read surface unless the change is made on the site itself. Compute derived values in the user's own transaction |
| **DC-06** | What is the shortest interval between events the system must react to? | Scheduled recurrence floor 60 s; per-trigger latency is per-connector and unpublished (PF-32) | Below 60 s (or below the connector's poll interval): event/webhook trigger, broker push, or synchronous plug-in. Not a tuning problem |
| **DC-07** | Must any single step complete while a person or caller waits? | 120 s synchronous in/out for automation; 180 s for an app request (PF-35, PF-04) | Above it: respond inside 120 s and continue asynchronously; or move the step out of the synchronous path entirely |
| **DC-08** | How long may a single business process instance remain open? | Run duration 30 days; pending approvals time out at 30 days; run history retained 30 days (PF-37) | Beyond 30 days: state must live in a business record with a re-triggering flow. Beyond 30 days of audit need: export telemetry |
| **DC-09** | How many megabytes of documents or attachments move per day? | Content throughput 200 MB / 2 GB / 10 GB per 24 h by owner profile; message size 100 MB (1 GB chunked) — whole payload, not just the file (PF-31, PF-35) | Size in **bytes per window**, not actions. Owner licence becomes a throughput decision (50× spread). Large files → chunking (if the connector supports it) or direct-to-storage patterns |
| **DC-10** | Is ordering of records required, and at what volume? | Trigger concurrency = 1 gives ordering but drops triggers, collapses `SplitOn` to 100, and is irreversible (PF-36) | At meaningful volume: ordered broker in front, concurrency off. Concurrency = 1 only for low-volume, loss-tolerant cases in an isolated child flow |
| **DC-11** | Where are the users, on what devices, over what network? | ≤ 150 ms client latency recommended (aged); satellite round trips 5+ s; per-platform concurrent-request limits differ and are unpublished (PF-11, PF-12, PF-13) | Measure latency before choosing the environment region. On high-latency links the design constraint is round-trip **count**. Mobile acceptance must be tested on target devices |
| **DC-12** | Is one step actual computation rather than orchestration of calls? | No compute-sizing dial; plug-in execution time is charged to the triggering request's budget (PF-45, PF-22) | Compute belongs outside the platform. This is an out-of-platform verdict before other sizing |
| **DC-13** | What availability does the business flow need, end to end? | In-region RPO ≈ 0 / RTO < 5 min automatic for production environments; external dependencies explicitly out of scope (PF-40, PF-43) | Single-region resilience needs no extra architecture. The solution's real objective is the **worst** dependency on the path — analyse per flow, not per platform |
| **DC-14** | Must the workload survive the loss of an entire region, with a committed RTO? | Cross-region is opt-in, production-only, managed-environment-gated, doubles storage, takes 48 h to enable, and has **no published RTO commitment**; some geographies have no pair at all (PF-41) | Joint architecture + licensing + region decision. A contractual RTO must rest on the customer's own drills. Single-region geographies have no option — surface the residency-vs-resilience trade-off |
| **DC-15** | Is the automation both high-volume and cross-region-protected? | SSDR-enabled Power Automate runs on isolated capacity: *"high-volume, highly parallel, or latency-sensitive flows might take longer to start or have lower throughput"* (PF-42) | Validate the two requirements together before commitment. Consider keeping high-throughput automation out of the SSDR environment |
| **DC-16** | How often will the solution be deployed, and when? | Solution import, publish customisations and bulk security changes are intensive database operations Microsoft says to keep out of business hours (PF-44) | Release windows are a performance requirement. Frequent releases + no business-hours degradation is a conflict resolved by calendar, not configuration |
| **DC-17** | Must peak capacity be *proven* before go-live? | Microsoft constrains load testing against shared infrastructure; no concurrent-user figure is published (PF-15, PF-09) | Peak confidence comes from limit arithmetic + a bounded pilot + production throttling monitoring + a degradation plan — not from a load test. If proof is existential, host the peak-bearing component elsewhere |
| **DC-18** | Who owns the automation, and what licence do they hold? | Performance profile follows the owner's licence; reverts to **Low** if the owner leaves; low-frequency flows owned by non-premium users are suspended after 90 days (PF-29, PF-39) | Ownership is an architectural decision. Business-critical automation → service principal or a capacity licence assigned to the flow |
| **DC-19** | Will operational reporting run against the same store as transactions? | Reporting consumes the same per-identity service-protection budget (PF-46, PF-22) | Separate read and write paths at design time. Note analytical replication (Fabric/Synapse link) is **not** covered by cross-region failover |
| **DC-20** | What growth is expected, and is there a seasonal or event-driven peak? | *"For every system, there's a limit to how much you can scale it without redesigning, introducing a workaround, or incorporating human involvement"*; capacity planning must precede predicted change (PF-47) | Size against year-3 volume and the peak, not today's average. Identify the **reachable limit** and the redesign trigger before it is hit |

#### PF-47 — Microsoft's own framing: every system has a scale ceiling beyond which redesign is required, and planning must precede the change
- **Classification:** DECISION CRITERION · **Origin:** MS
- **Evidence:** *"**For every system, there's a limit to how much you can scale it without redesigning, introducing a workaround, or incorporating human involvement.** If you don't include performance efficiency practices and consider the tradeoffs, your design is potentially at risk"* (P-31, `ms.date` 2025-08-15). PE:02 requires planning *"before there are predicted changes in usage patterns. Predicted changes include seasonal variations, product updates, marketing campaigns, special events, or regulatory changes"*, and names the trigger points: *"Design (prediction); Regular spikes (8:00 AM sign-in rush); Launch (prediction validation); Business model change; Acquisition or merger; Marketing push; Seasonal change; Feature launch; Periodically."* On limits: *"You need to understand the limitations of the resources in your workload and factor those limitations into your design decisions… you should know whether resource limitations require you to change the design approach or to change resources altogether. You also need to determine **reachable limits**… When capacity planning identifies reachable limits, you need to modify the workload **before** the limit creates a performance problem."* Trade-off: *"Misjudged capacity planning can lead to over-provisioning or under-provisioning of resources. Over-provisioning can lead to higher costs. Under-provisioning can result in poor performance"* (P-18).
- **Why it matters:** Microsoft supplies the honest framing this whole area needs: the question is not *"does Power Platform scale?"* but *"at what point does this workload require redesign, and will we see it coming?"* The concept of a **reachable limit** — a limit you will hit at projected growth — is the right unit for a Shared Understanding entry, because it converts an unbounded worry into a dated, monitorable claim.
- **Decision impact:** For every workload, record: the binding meter (§2), the current consumption, the projected consumption at year 3 and at peak, and the **redesign trigger** — the consumption level at which the architecture must change. That trigger is a natural decision tripwire. Also record the named change events (merger, campaign, seasonal peak, feature launch) as revalidation triggers for performance claims.
- **Confidence:** HIGH · **Sources:** P-31, P-18

---

## 8. Negative evidence register

Collected deliberately, per `../source-policy.md` §2. Entries are evidence *against* Power Platform or against a particular Power Platform design.

### 8.1 Published limitations that bound the platform

1. Non-delegable queries return **silently truncated, incorrect results** above 500/2,000 rows (P-02).
2. Two delegation traps produce **no warning at all** (collections via `With`/`Set`/`UpdateContext`; non-delegable sources) (P-02).
3. Relationship traversal capped at 2 lookup levels — **1 offline** — and 20 expanded entities (P-02).
4. Effective Dataverse throughput is **not a published number**: 6,000 × undisclosed, licence-dependent web-server count (P-15).
5. **Trial environments allocate only a single web server** — a proof of concept measures a different platform than production (P-15).
6. Batching **cannot** bypass entitlement limits; the two meters are evaluated separately (P-15).
7. Microsoft's throughput method is **adaptive back-off, not calculation**: *"Don't try to calculate how many requests to send at a time"* (P-15).
8. Power Pages cache refresh SLA is **15 minutes and cannot be shortened** (P-10).
9. Dataverse→Power Pages freshness for server-side-derived data is *"never guaranteed to be immediate"*, and the pattern is *"not recommended"* (P-10).
10. Clearing the Power Pages cache *"can lead to users facing performance issues"* on a busy live site (P-10).
11. Power Pages Traffic Manager is **active/passive** — the second node is failover, not load sharing (P-09).
12. Power Pages node scaling is driven by **purchased licensing capacity**, not by an architectural setting (P-09).
13. Power Pages publishes **no request, throughput or concurrency limits** (P-12).
14. **No concurrent-user figure is published for any Power Platform application surface** (P-01, P-12, P-17–P-22).
15. **No end-to-end latency figure is published for any path** (P-17, P-01, AT2-11).
16. Per-platform concurrent-request limits for mobile clients differ and are **unpublished** (P-23).
17. Load testing against the service is **constrained**: *"Limit tests to avoid unintended consequences"* (P-20).
18. A flow's throughput class follows its **owner's licence** and reverts to Low if the owner leaves (P-16).
19. The request model is **mid-transition with no announced enforcement date**; manual flows will move to the invoking user's limits (P-26).
20. In-run loop concurrency **defaults to 1** — most flows are serial unless changed (P-16).
21. Trigger concurrency is **irreversible**, drops triggers under load, and collapses `SplitOn` to 100 (P-16).
22. Content throughput on a Low profile is **200 MB per 24 hours** — a limit scaled by payload, not activity (P-16).
23. Retries (up to 12 on Medium/High) **consume the same meters** as real work, so a failing dependency increases load (P-16).
24. Sustained overload does not error — the flow **slows, then is turned off after 14 days**; editing it **resets the evidence** (P-16).
25. Low-frequency flows owned by non-premium users are **turned off after 90 days of inactivity** (P-16).
26. Run duration and run history both end at **30 days**; pending approvals time out (P-16).
27. Deployment operations (solution import, publish customisations, bulk business-unit changes) are named as **intensive database operations to avoid during business hours** (P-07).
28. Cross-region DR has **no published RTO commitment** (P-27).
29. Without SSDR explicitly enabled, **backups are not replicated** out of the primary region (P-27).
30. Enabling SSDR **degrades** high-volume, highly parallel or latency-sensitive automation throughput (P-27).
31. Several geographies have **no cross-region option at all** (single regions; Brazil; South Africa; UAE constrained) (P-27).
32. Fabric link, Synapse Link, Copilot Studio conversation runtime, Customer Insights – Data, Project Operations and Commerce Scale Units are **not covered** by SSDR failover (P-27).
33. External-system RPO is **explicitly outside Power Platform's resiliency commitments** (P-27).
34. Backup retention is **7 days** unless the environment is a *production managed* environment (28 days max) (P-30).
35. Trial environments are **not backed up at all** (P-30).
36. Business-critical workloads in non-production environment types get **none** of the zone-redundancy guarantees (P-27).
37. Site Checker's Power Pages thresholds are low and structural: **500 web files, 200 lookup records, 100 web roles** (P-11).
38. SharePoint returns **all defined columns even when unused**, so column count is a performance parameter for every read (P-23).
39. Microsoft instructs partitioning SharePoint lists above *"hundreds of thousands of records"* — a UI-visible design constraint (P-23).
40. *"Excel isn't a relational database system"*, and Microsoft **declines to publish** a transaction threshold for it (P-23).
41. Microsoft names its own workaround-driven anti-patterns: *"loading too much data, turning everything into collections, and overloading OnStart"* (P-05).
42. Nearly all slow-to-load apps have a formula over **256,000 characters**; some exceed **1 million** (P-06).
43. Preloading for speed exposes compiled app assets — including authored text and the environment URL — on **unauthenticated endpoints** (P-23).
44. Dataverse search is separately metered at **one request per second per user** (P-15).
45. Named data-source bottlenecks are largely **outside** Power Platform: missing indexes, huge joins, table scans (`In` instead of `StartsWith`), resource-starved back ends, blocking/deadlocks, unhealthy or under-scaled gateways (P-23).

### 8.2 Independent and community signals (T3/T4 — require validation, not authoritative)

46. **T3** — Practitioner sources consistently name delegation as the dominant cause of slow canvas apps, and describe production symptoms at scale (order of hundreds of concurrent users against tens of thousands of rows) with multi-second screen loads and form submissions. Directionally consistent with P-02 and P-21, but the specific figures are **unverified** and must not be encoded as thresholds (P-32).
47. **T3** — The same sources describe a recurring pattern of "development-time intuition versus production-scale reality", i.e. that canvas performance defects surface only under real data volume and user load. Consistent with Microsoft's own PE:05 guidance and with PF-15's testing constraint, but community-sourced (P-32).
48. **Gap** — No independent benchmark of any Power Platform component was found in this pass. The absence is itself the finding: there is no third-party measurement to triangulate Microsoft's limits against (PF-U-01).

### 8.3 What negative evidence is still missing

- No empirical throughput, latency or concurrency **measurement** from any source, Microsoft or independent (PF-U-01).
- No published relationship between Power Pages capacity purchased and node count or throughput delivered (PF-U-03).
- No per-platform mobile concurrency figures (PF-U-02).
- No documented service-protection behaviour under *burst* rather than sustained load beyond the `Retry-After` mechanism.
- No Microsoft statement on the performance cost of security-model complexity (row-level sharing volume, hierarchy depth) — `data-architecture.md` carries the PrincipalObjectAccess storage angle but not a latency figure (PF-U-07).

---

## 9. Conflicts (CONFLICTED)

**PF-C-01 — Two published sets of Power Platform request numbers.** The licensing page states official per-licence limits (40,000 / 6,000 / 250,000 / 200 per 24 h); the flow limits page states higher transition-period approximations by performance profile (10,000 / 200,000 / 500,000 / 10,000,000). **Resolution:** not a contradiction — the same meter at two enforcement strengths, and Microsoft says so on the page (*"These limits represent approximations… They aren't guarantees"*) with the instruction *"Build your cloud flows based on official limits."* Recorded because a reader encountering only one page will size wrongly. **Sources:** P-26, P-16.

**PF-C-02 — "Highly available and scalable" versus no published scale figures for Power Pages.** P-09 describes Power Pages as *"a secure, scalable, and highly available platform to build business-critical websites"*; P-12, the page titled "system requirements and limits", publishes no request, concurrency or throughput limit. **Resolution attempt:** the two are reconcilable if scale is understood as capacity-driven (PF-16) rather than specified. **Not fully resolved**, and the marketing adjective must not be treated as evidence (`../source-policy.md` §7). **Sources:** P-09, P-12.

**PF-C-03 — "Limit tests" versus "test in a production-like environment under stress".** PE:05 requires load, stress, soak and spike testing against a mirrored environment, and then instructs the reader to limit tests because the infrastructure is shared. RE:06 asks for chaos engineering *"in your test and production environments"*. **Resolution:** unresolved in the documentation. Practical reading: bounded, coordinated testing is expected; full-scale destructive load testing against the shared service is not. Treat as CONFLICTED until Microsoft publishes a testing policy. **Sources:** P-20, P-29.

**PF-C-04 — Aged model-driven performance guidance versus the current storage engine.** The 150 ms latency recommendation and the "avoid intensive database operations during business hours" list are from 2020 pages (P-07, P-08) describing a platform that has since moved to availability-zone replication and continuous Azure SQL backups. The *direction* of both is corroborated by the current service-protection page (P-15), but the currency of the specifics is not vouched for. Recorded as CONFLICTED-by-age rather than by content. **Sources:** P-07, P-08, P-15, P-27.

---

## 10. Unknowns (UNKNOWN)

| id | Unknown | Why it matters | How to close |
|---|---|---|---|
| **PF-U-01** | No empirical performance measurement exists anywhere in this corpus for any component. Every statement is limit-based. | Caps this file's confidence at MEDIUM and makes every `WITHIN ENVELOPE` verdict a "no documented limit violated" statement only | Controlled benchmark on a representative environment; or accept permanently and always pair a verdict with a pilot requirement |
| **PF-U-02** | Per-platform (iOS/Android/Windows/browser) concurrent-request limits for Power Apps clients | Determines mobile data-load time for large datasets; PF-13 says the variation is material but not how large | Device testing; or a Microsoft statement if one exists outside the pages fetched |
| **PF-U-03** | The relationship between assigned Power Pages licensing capacity and delivered node count / throughput | This is the *only* scale dial Power Pages exposes (PF-16) and its effect is unquantified | Microsoft engagement; or empirical observation across capacity tiers |
| **PF-U-04** | Whether the Site Checker thresholds (500 web files, 200 lookup records, 100 web roles) are current | They are the only numeric Power Pages design limits available, and the page is from 2023 with other checks referencing retired features | Re-run Site Checker on a current site; check the release notes |
| **PF-U-05** | SharePoint List View Threshold (~5,000) and list ceiling (30 million) are **search-derived** in this pass, not fetched | Load-bearing for any SharePoint-as-store verdict | Fetch the Tier-1 SharePoint limits page directly |
| **PF-U-06** | Whether the 2020 "intensive database operations" list (P-07) still reflects current behaviour | Drives the deployment-window recommendation (PF-44, PF-AP-15) | Look for a current equivalent page; or observe during a controlled solution import |
| **PF-U-07** | Performance cost of Dataverse security-model complexity (sharing volume, hierarchy depth, business-unit count) at scale | Requested by `security.md` SEC-08…SEC-13 / S-02 and materially affects authorization-heavy designs; Microsoft documents overhead but publishes no latency/throughput curve | **UNKNOWN by documentation.** Close per solution with a V2 bounded pilot using representative users, BU/team/share cardinality and queries; do not invent a numeric safe threshold |
| **PF-U-08** | Current per-licence **polling intervals** for managed connector triggers | Blocks any freshness answer for polling-triggered designs (PF-32); DA and AT2 both leave it open | Connector-by-connector reference pages; the platform-wide figure appears no longer to be published |
| **PF-U-09** | Whether the Power Apps 180 s / 4-retry envelope applies to model-driven and Power Pages surfaces or only to canvas | PF-04 is stated on the Power Apps limits page without surface qualification | Microsoft clarification |
| **PF-U-10** | Actual web-server count for a given environment, and how it scales with licences purchased | Makes effective Dataverse throughput unknowable in advance (PF-22, negative evidence 4) | Microsoft states the factors are not disclosed — likely permanently open; design must be tolerant rather than sized |

---

## 11. Cross-area analysis

These are the couplings where a **performance** decision changes cost or operations. Stated here once, with the sibling finding named; the siblings own the detail.

### 11.1 PERFORMANCE ↔ COST

| Coupling | Mechanism | Evidence |
|---|---|---|
| **Scale drives licence and capacity spend directly** | Power Pages node scaling *is* purchased capacity (PF-16); Dataverse has *"no technical limit"* on size — the ceiling is a purchased entitlement (PF-17 / LC-05) | P-09, P-14 → **LC-05, LC-12, LC-13** |
| **Owner licence is a throughput dial worth up to 50×** | Content throughput 200 MB (Low) vs 10 GB (High) per 24 h; PPR 10k vs 500k; and the fix Microsoft names for throttling is *"Assign Power Automate Process licenses to the flow"* | P-16 → **LC-08, LC-09** |
| **Retries and pagination are billed** | *"Retries and extra requests from pagination count as actions"* — a flaky dependency consumes entitlement | P-16, P-26 → **LC-09** |
| **Resilience doubles storage cost** | SSDR *"consumes another 10 GB"* for a 10 GB primary, from existing entitlements, and requires a managed environment (premium tier) | P-27 → **LC-24** |
| **Monitoring performance costs money** | Microsoft's own trade-off callout: *"Logic monitoring tools are likely to increase costs"*; and *"There are cost implications for storing and querying logs"* | P-19, P-33 → **LC-27, OP-11** |
| **Performance testing costs money** | *"There are costs associated with maintaining separate test environments, storing data, using tooling, and running tests"* | P-20 → **LC-26** |
| **Archiving is simultaneously a performance and a cost lever** | *"Archiving relocates older, less-frequently accessed data to more cost-effective storage"* and reduces backup/recovery time | P-18 → **LC-11** |
| **Capacity misjudgement cuts both ways** | *"Over-provisioning can lead to higher costs. Under-provisioning can result in poor performance"* | P-18 → **LC-21** |
| **The cheapest licence can be the slowest architecture** | Low profile: 5,000-item arrays, 200 MB/day content, 10,000 requests/day, 2 retries, 5 s postpone floor — a design sized for it may need workarounds that cost more than the licence saved | P-16 → **LC-28** |

### 11.2 PERFORMANCE ↔ OPERATIONS

| Coupling | Mechanism | Evidence |
|---|---|---|
| **Sustained overload is an operational failure, not an error** | Flows slow, then are **turned off after 14 days**; notification goes to an individual's mailbox; editing the flow resets the evidence | P-16 → **OP-04, OP-08** |
| **Peak capacity cannot be proven by load testing** | *"Limit tests to avoid unintended consequences"*, so confidence must come from monitoring in production plus a degradation plan | P-20 → **OP-08, OP-13** |
| **Deployment is a performance event** | Solution import and publish customisations are named intensive database operations to keep out of business hours | P-07 → **OP-16** |
| **Cross-region protection degrades throughput** | SSDR-enabled Power Automate runs on isolated capacity with lower throughput for high-volume flows | P-27 → **OP-18, OP-20** |
| **The observability that would explain a slowdown is gated and lossy** | Flow telemetry export is *"managed environments only"* and *"not 100% lossless"*; PPAC Monitor metrics are daily aggregates, logs retained 7 days, metrics 28 days, and report only the 75th percentile | P-34, P-35 → **OP-08, OP-11, OP-12** |
| **Run history is the only transactional record, and it expires in 30 days** | *"Flow execution history… is transactional, and therefore provides full view of events, in case of transient missing log data on Application Insights"* — but retained 30 days | P-34, P-16 → **OP-11** |
| **Cache clearing is a production performance incident** | *"For live site with heavy usage, this can lead to users facing performance issues"* | P-10 → **OP-19** |
| **Microsoft support invests four hours in a performance case, then closes it** | *"The Microsoft Dynamics support team invests up to four hours of time on a break-fix case… If after four hours the issue isn't resolved, consult a partner or the community forums"* | P-36 → **OP-24** |
| **Restore is not a performance-neutral operation** | Copying/restoring *"might take more than one day, depending on the size of the data, especially if you must copy audit data"* | P-30 → **OP-14** |

### 11.3 Where this file defers

| Topic | Owner | Why deferred |
|---|---|---|
| Automation shape selection; alternatives envelopes (Logic Apps, Functions, Durable Functions, Service Bus); idempotency, ordering, compensation | `automation-architecture.md` | Already carried in depth as AT2-01…AT2-53; this file cites rather than duplicates |
| Dataverse data modelling, elastic tables, long-term retention, Synapse/Fabric replication mechanics, PrincipalObjectAccess storage | `data-architecture.md` | DA is the VALIDATED, HIGH-confidence owner |
| Offline architecture and its data-model constraints; PCF and client extensibility limits | `application-architecture.md` | AA owns the app-architecture envelope |
| Whether Power Platform is the right platform at all | `platform-suitability.md` | PS owns the fit verdict; this file supplies the performance inputs to it |
| Licence prices, capacity units, TCO, cost drivers | `licensing-cost.md` (this block) | Kept conceptually separate by instruction |
| Monitoring tooling, incident management, support model, ALM after deployment | `operations-support.md` (this block) | Kept conceptually separate by instruction |

---

## 12. Evidence-quality notes

- **31 sources, of which 25 are Tier 1 pages fetched in this pass with `ms.date` read.** Two are inherited from VALIDATED peers; two are search-derived (P-24, P-32) and flagged at every point of use; two are Azure/Well-Architected pages used for pattern vocabulary only.
- **Aged Tier 1 material.** Five pages exceed 18 months: P-04 (2021-01-22), P-06 (2023-04-07), P-07 (2020-09-08), P-08 (2020-09-11), P-11 (2023-03-03). All five are tagged **MS-A** and the currency caveat is repeated in the finding body. Two of them (P-07, P-08) carry the only network and deployment-window numbers in the corpus, so their age is a real weakness, partially mitigated by corroboration from the current P-15.
- **The corpus is limits-only.** No empirical measurement exists (PF-U-01). This is the single largest quality gap and it caps confidence at MEDIUM. Every §3 verdict must be read as "no documented limit violated", never as endorsement.
- **Absence claims are broad but shallow.** The concurrency (PF-09) and latency (PF-14) absence claims rest on nine and three fetched pages respectively. They are phrased as "treat as unpublished until verified" and should be spot-checked against the Power Platform Architecture Center reference architectures, which were not fully swept in this pass.
- **Microsoft-example numbers are a live encoding hazard.** P-17 contains illustrative figures (0.1% error rate, 200 ms latency, 10 million transactions/month, "99% of customer lookup requests completing in less than 2 seconds", "target response time of less than 500 milliseconds") that are **examples of how to write a target**, not platform thresholds. They must never be encoded as Power Platform performance characteristics. Flagged here because they are exactly the kind of number that gets lifted out of context.
- **Single-author, single-session.** Research, structure and synthesis share one author and one session. Independent spot-checking is recommended before pack authoring; the four highest-value checks are PF-22 (the web-server multiplier, because effective throughput depends on it), PF-16 (capacity-driven Power Pages scaling, because it is the whole external-scale story), PF-41/PF-42 (the SSDR gates and the throughput degradation, because they reverse the usual assumption that DR is transparent), and PF-01/PF-02 (delegation as a correctness rather than performance issue, because it changes how the finding must be communicated).

---

## 13. Implications for the aisa knowledge model (pointers, not pack content)

Recorded as pointers only; the pack is authored later and is not in scope here.

- **Discovery-safe signals** implied by §7, all technology-neutral: `largest_table_row_count_year3`, `free_text_search_over_large_set_required`, `relationship_traversal_depth`, `peak_transactions_per_identity_per_5min`, `single_identity_funnel_present`, `data_freshness_tolerance`, `shortest_event_interval`, `synchronous_wait_required`, `max_process_instance_duration`, `document_volume_bytes_per_day`, `record_ordering_required`, `user_geography_and_network_quality`, `primary_device_class`, `compute_intensive_step_present`, `availability_objective_per_business_flow`, `region_loss_tolerance`, `release_frequency`, `peak_proof_required`, `growth_and_seasonality`.
- **Two signals that are usually collapsed and must not be:** *delegation-safe query* (a correctness property, PF-01) is not the same as *fast query* (a latency property). And *availability of the platform* (PF-40) is not the same as *availability of the business flow* (PF-43).
- **Knowledge-state guidance.** Performance claims should rarely be Confirmed from documentation alone. `PPR headroom` is Confirmed-with-short-half-life (PF-30 revalidation trigger: PPR reporting GA). `Concurrent user capacity` and `end-to-end latency` are structurally **Unknown** until measured (PF-09, PF-14) and should be recorded as such rather than assumed. `Peak survival` is **Risky** unless a pilot or monitoring plan exists (PF-15).
- **Natural decision tripwires** from §7: consumption reaching the redesign trigger on the binding meter (PF-47); the PPR transition ending (PF-30); a flow owner leaving (PF-29); crossing the Power Pages Site Checker thresholds (PF-20); an external dependency's recovery capability changing (PF-43).
- **The pack must be able to conclude "not Power Platform" on performance grounds alone**, via B-14 to B-17: compute-bound work, Excel-as-transactional-store, a hard sub-second transactional end-to-end SLA, and a peak that must be load-test-proven.

---

## 14. Source register

Kind: **fetched** (retrieved in this pass, `ms.date` read) · **inherited** (from a VALIDATED peer, re-cited) · **search-derived** (WebSearch synthesis — MEDIUM ceiling) · **T3** (independent technical source).

| Id | Tier | Kind | Title | URL | ms.date |
|---|---|---|---|---|---|
| P-01 | T1 | fetched | Power Apps system requirements and limits | `learn.microsoft.com/power-apps/limits-and-config` | 2026-01-12 |
| P-02 | T1 | fetched | Understand delegation in a canvas app | `learn.microsoft.com/power-apps/maker/canvas-apps/delegation-overview` | 2026-01-13 |
| P-03 | T1 | fetched | Troubleshoot Power Apps canvas app performance issues | `learn.microsoft.com/troubleshoot/power-platform/power-apps/canvas-app-performance/troubleshoot-perf-table` | 2025-02-14 |
| P-04 | T1 | fetched (**aged**) | Understand canvas app execution phases and data call flow | `learn.microsoft.com/power-apps/maker/canvas-apps/execution-phases-data-flow` | 2021-01-22 |
| P-05 | T1 | fetched | How to create performant Power Apps | `learn.microsoft.com/power-apps/maker/canvas-apps/create-performant-apps-overview` | 2026-08-20 |
| P-06 | T1 | fetched (**aged**) | Build large and complex canvas apps | `learn.microsoft.com/power-apps/maker/canvas-apps/working-with-large-apps` | 2023-04-07 |
| P-07 | T1 | fetched (**aged**) | Performance tuning and optimization for customer engagement apps | `learn.microsoft.com/power-platform/admin/performance-tuning-and-optimization` | 2020-09-08 |
| P-08 | T1 | fetched (**aged**) | Verify network capacity and throughput for clients | `learn.microsoft.com/power-platform/admin/verify-network-capacity-throughput-clients` | 2020-09-11 |
| P-09 | T1 | fetched | Power Pages architecture | `learn.microsoft.com/power-pages/admin/architecture` | 2026-04-28 |
| P-10 | T1 | fetched | How server-side caching works in Power Pages | `learn.microsoft.com/power-pages/admin/clear-server-side-cache` | 2026-04-29 |
| P-11 | T1 | fetched (**aged**) | Site Checker performance | `learn.microsoft.com/power-pages/admin/site-checker-performance` | 2023-03-03 |
| P-12 | T1 | fetched | Power Pages system requirements and limits | `learn.microsoft.com/power-pages/system-requirements` | 2026-04-28 |
| P-13 | T1 | fetched | SharePoint (managed connector reference) | `learn.microsoft.com/connectors/sharepointonline/` | 2024-03-01 (page updated 2026-08-01) |
| P-14 | T1 | fetched | Dataverse capacity-based storage details | `learn.microsoft.com/power-platform/admin/capacity-storage` | 2026-08-17 |
| P-15 | T1 | fetched | Service protection API limits (Microsoft Dataverse) | `learn.microsoft.com/power-apps/developer/data-platform/api-limits` | 2026-01-09 |
| P-16 | T1 | fetched | Limits of automated, scheduled, and instant flows | `learn.microsoft.com/power-automate/limits-and-config` | 2026-07-17 |
| P-17 | T1 | fetched | Define performance targets (PE:01) | `learn.microsoft.com/power-platform/well-architected/performance-efficiency/performance-targets` | 2025-08-15 |
| P-18 | T1 | fetched | Performance planning (PE:02) | `learn.microsoft.com/power-platform/well-architected/performance-efficiency/performance-planning` | 2025-08-15 |
| P-19 | T1 | fetched | Optimize code and logic (PE:06) | `learn.microsoft.com/power-platform/well-architected/performance-efficiency/optimize-code` | 2025-08-15 |
| P-20 | T1 | fetched | Performance testing (PE:05) | `learn.microsoft.com/power-platform/well-architected/performance-efficiency/performance-test` | 2026-07-17 |
| P-21 | T1 | fetched | Identify and mitigate canvas app performance issues | `learn.microsoft.com/power-platform/architecture/key-concepts/performance/top-issues` | 2025-07-15 |
| P-22 | T1 | fetched | Manage Power Platform solution performance | `learn.microsoft.com/power-platform/architecture/key-concepts/performance/` | 2025-07-15 |
| P-23 | T1 | fetched | Performance considerations for Power Apps | `learn.microsoft.com/power-apps/maker/canvas-apps/app-performance-considerations` | 2024-12-10 |
| P-24 | T2/T3 | search-derived | SharePoint List View Threshold (~5,000) and 30M-item list ceiling | support.microsoft.com + Learn troubleshooting pages, via search | n/d — **verify (PF-U-05)** |
| P-25 | T1 | fetched | Understand platform limits and avoid throttling | `learn.microsoft.com/power-automate/guidance/coding-guidelines/understand-limits` | 2025-07-11 |
| P-26 | T1 | fetched | Requests limits and allocations (Power Platform) | `learn.microsoft.com/power-platform/admin/api-request-limits-allocations` | 2026-08-14 |
| P-27 | T1 | fetched | Business continuity and disaster recovery | `learn.microsoft.com/power-platform/admin/business-continuity-disaster-recovery` | 2026-08-20 |
| P-28 | T1 | fetched | Plan mission critical workloads | `learn.microsoft.com/power-platform/guidance/adoption/plan-mission-critical` | 2026-05-04 |
| P-29 | T1 | fetched | Recommendation checklist for Reliability (RE:01–RE:08) | `learn.microsoft.com/power-platform/well-architected/reliability/checklist` | 2025-08-15 |
| P-30 | T1 | fetched | Back up and restore environments | `learn.microsoft.com/power-platform/admin/backup-restore-environments` | 2026-06-23 |
| P-31 | T1 | fetched | Recommendation checklist for Performance Efficiency (PE:01–PE:10) | `learn.microsoft.com/power-platform/well-architected/performance-efficiency/checklist` | 2025-08-15 |
| P-32 | T3 | search-derived | Practitioner accounts of canvas app performance at production scale | multiple independent blogs and Medium articles, via search | n/d — **directional only** |
| P-33 | T1 | fetched | Design a reliable monitoring and alerting strategy (RE:08) | `learn.microsoft.com/power-platform/well-architected/reliability/monitoring-alerting-strategy` | 2025-08-18 |
| P-34 | T1 | fetched | Set up Application Insights with Power Automate | `learn.microsoft.com/power-platform/admin/app-insights-cloud-flow` | 2025-01-16 |
| P-35 | T1 | fetched | Monitor the health of your resources (PPAC Monitor) | `learn.microsoft.com/power-platform/admin/monitoring/monitoring-overview` | 2025-11-20 |
| P-36 | T1 | fetched | Support for Microsoft Power Platform and Dynamics 365 apps | `learn.microsoft.com/power-platform/admin/support-overview` | 2025-07-31 |

Peer files cited but not re-registered here (each maintains its own source register): `platform-suitability.md` §11, `application-architecture.md` §11, `data-architecture.md` §12, `automation-architecture.md` §15.

---

## 15. Cross-Block V2 reconciliation

### 15.1 Security ↔ Performance
Dataverse authorization complexity is no longer deferred in a circle. Microsoft evidence supports the direction (“sharing/excessive security constructs add overhead”) but not a numeric curve. `PF-U-07` is therefore a **documented UNKNOWN with a test obligation**: BU/team/sharing-heavy business-critical designs require representative principals, records and access patterns in a V2 bounded pilot.

### 15.2 Integration ↔ Performance
The custom-connector rate is **CONFLICTED corpus-wide**. Current Microsoft pages disagree: Power Automate limits (2026-07-17) says 500 requests/minute/connection; Custom Connector FAQ (2025-09-04) says 10,000. Both are **VOLATILE VALUE**. This file must not use either as a settled envelope; measured tenant/connector behaviour or Microsoft confirmation is required before commitment.

Broker/worker/API patterns change which meter binds but do not make the workload “scalable” by assertion. Size ingress, backlog growth, worker drain rate, the Power Platform calls on the return path and retry/reconciliation bursts.

### 15.3 Operations ↔ Performance
A performance test is one evidence mechanism, not the same thing as functional regression. Use `integration-architecture.md` §15.8's V1–V4 validation model. Production claims require a health/telemetry plan (`operations-support.md` OP-02/OP-03), and security/managed-environment dependent behaviour may require V4 test fidelity.

### 15.4 Cost ↔ Performance
Performance headroom can require additional connections, broker/worker capacity, telemetry retention, non-production load testing and specialist time. Those are cost drivers even where no Power Platform licence changes. `licensing-cost.md` must price the **workload shape**, not infer economics from the daily entitlement alone.

### 15.5 Availability semantics
Dataverse documents 99.9% uptime. This is not a composite solution SLA and does not make an external dependency, connector, gateway or Azure component equally available. RTO/RPO remain recovery objectives, not uptime. For end-to-end flows use the weakest-dependency method in `operations-support.md` OP-19.

### V2 sources
- `https://learn.microsoft.com/en-us/connectors/custom-connectors/faq` (updated 2025-09-04)
- `https://learn.microsoft.com/en-us/power-automate/limits-and-config` (updated 2026-07-17)
- `https://learn.microsoft.com/en-us/power-apps/maker/data-platform/why-dataverse-overview` (updated 2026-05-21)

