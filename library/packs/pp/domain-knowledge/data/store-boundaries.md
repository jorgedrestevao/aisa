# Store boundaries — what each store can support

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Which available store can satisfy this authority + integrity + query-shape requirement?*
- *Does the reporting need force a second store, and what does that oblige?*
- *Should this data move at all, or stay where it is?*
- *What does replication import that virtualization does not, and vice versa?*

This file states **what each store can and cannot defensibly support, per observable data requirement**.
It does not decide **which store wins** — that belongs to the decision model (`decision-tree.md` S4–S6).
There are no `*-first` architecture branches here, and no disqualification thresholds.

---

## 1. What this is for · `decision-grade`

A store question is answerable only once the *data* requirement is observable. This is the cross-store
entry point: it names the dimensions that must be answered, states what each store supports on each, and
hands off to the store's own unit (`dataverse.md`, `sharepoint.md`, `azure-sql.md`) or to
`query-and-delegation.md` when the question is about access paths.

**The cheapest question first: view or data?** Three integration categories exist — UI/embedding, data,
and process. Embedding *saves time, reduces training and reduces user licences* and keeps the data where
it is. Ask whether the requirement is to **see** the data or to **own** it before asking which store.

## 2. When it becomes material · `decision-grade`

- An entity's **authority** is contested, or authority must transfer at a lifecycle boundary.
- **Relational integrity**, cascades or referential behaviour is required.
- Writes must be **all-or-nothing** across rows.
- **Row- or column-level** confidentiality must be enforced *by the store*.
- A queried entity is projected past the client's paging behaviour.
- **Concurrent edits** on the same record are expected.
- **Binaries, documents or attachments** are a material share of the volume.
- **Retention** is measured in years, or **residency** is constrained.
- The same entities must serve **operational** and **analytical** use.

## 3. The dimensions that decide a store · `decision-grade`

Answer each as a **number or a category**, not as an adjective. Any dimension left `Unknown` where it
could plausibly be material is an evidence gap, not a pass.

| # | Dimension | The question |
|---:|---|---|
| 1 | **Source authority** | Who may create, who may change **which fields**, and at which lifecycle phase does authority transfer? |
| 2 | **Relational depth** | How many related entities, and what integrity behaviour is required on delete and reparent? |
| 3 | **Integrity enforcement** | Must the rule hold no matter which client writes — app, API, integration? |
| 4 | **Atomicity span** | Is there a unit of work over ≥ 2 rows or ≥ 2 systems that must succeed or fail together? |
| 5 | **Authorization granularity** | Table, row, or **column**? Enforced by the store, or by the app? |
| 6 | **Query and access-path shape** | Which filters and sorts, over how many rows, on which paths? (→ `query-and-delegation.md`) |
| 7 | **Concurrency** | Do several users edit the same record, and what must happen on conflict? |
| 8 | **Binary and attachment volume** | GB of files, and must protection travel with the file when downloaded? |
| 9 | **Retention** | How many years, read-only or queryable, and is erasure required? |
| 10 | **Residency** | Which boundary, at what granularity, and is the decision reversible? |
| 11 | **Analytical vs operational** | Aggregates, trends, cross-period history — and must per-user security hold in the report? |
| 12 | **Replication / virtualization consequence** | If the data stays elsewhere, which platform data features are forfeited, and what does the copy oblige? |

## 4. Cross-store capability map · `decision-grade`

Read a row as: *given this observable requirement, what does each store support?* This is a **capability**
map. It is not a scoring table, and the rightmost column is a legitimate answer, not a fallback.

| Observable requirement | Governed relational store (Dataverse) | Relational store via connector (SQL / Azure SQL) | List / library store (SharePoint, Lists) | Keep in the external system of record |
|---|---|---|---|---|
| Several related entities, referential integrity, cascades | Supported: 1:N and N:N, **one parental (cascading) relationship per child table** | Supported by the engine; **conditional on connector conformance** | Bounded: a low ceiling on lookup/person/metadata joins per view; integrity is **opt-in per lookup and delete-only** | n/a |
| Any queried entity past the client paging cliff, with non-trivial filters and sorts | Broadest delegable operation set of the three connectors | Delegable but **partial** — several operations and types are not | **Narrowest** delegable set; the list-view threshold binds independently | Custom connector paths are **not delegable at all** |
| Multi-row writes that must succeed or fail together | Server-side only — change set, transaction API, synchronous plug-in or custom API | Stored procedure with an explicit transaction | **Not supported**; last writer wins | Saga with the external posting as the pivot |
| Concurrent edits on the same record | Optimistic concurrency through the SDK / Web API; the canvas client surfaces a server conflict error | **Connector locking and isolation semantics are undocumented** | No conflict setting; version history is *recovery*, not concurrency control | Depends on the system |
| Row visibility by owner/team/unit **and** column-level confidentiality | The only store here with **API-level column security** and masking; unit/role/team row security | Row-level security **in the database**, and only with an explicit per-user identity — internal users only | Row scoping is bounded and recommended far below its maximum; **no column-level security** | Keep in place if the system enforces it |
| Field-change audit for N years | Native, metered, with retention set at environment creation | Build it in the database — **but server-side triggers break connector writes** | Versioning only; attachment changes are not tracked | Keep in place |
| The document **is** the record — files, metadata, versions, protection labels | Conditional: file columns exist but carry **no label mechanism** | Not applicable | Native: libraries, versioning, retention and sensitivity labels | n/a |
| GB of binaries | Conditional: the file meter is an order of magnitude cheaper than the database meter, but long-term retention saves **nothing** on files | Blob storage sits outside the store | Native at high per-file size — but the row security of the governed store is **lost** | Blob/library plus a reference |
| High-ingest, semi-structured, time-bounded data (events, telemetry, logs) | Conditional: horizontally-scaling elastic tables, which **forfeit** transactions, joins, N:N to standard tables, rollups, sharing and cascades. GA status is **unresolved** | **Weak** — the vendor's own data-store model guide routes high-ingest timestamped metrics and events *away* from relational, and sustained write is capped by log rate **regardless of compute size** | Not supported | A purpose-built ingest store is the vendor's own named target |
| Aggregates and KPIs over large row counts; trend or multi-year reporting | Bounded in-platform → an **analytical copy is required** | Native in the engine | Import-only and slow | Warehouse, or keep in place |
| Reporting must respect **per-user** record security | Supported through the read-only SQL endpoint honouring store roles — but security **does not travel into a copy** | Conditional on SSO and database row-level security | Reports run as the connection owner | Depends |
| Keep N years of closed records cheaply, read-only | Conditional: long-term retention requires managed environments, is **irreversible**, saves roughly half the database meter and nothing on files | Conditional — **not strong**: long-term retention is *backup* retention restorable only as a new database. **No cold or cheap tier exists for rows**; cheapness means partitioning plus archival compression (slower reads, more CPU) or moving the data out | Conditional: labels apply to items, **not to attachments** | Lake or archive store |
| Data must remain in an existing system of record | Keep in place with read-through **or** a replicated subset (§6) | Keep in place plus connector (gateway if on-premises) | n/a | Native |
| The app must keep working when the external system is down | Local pending state + queue + idempotent writes | Same | Not viable | Not viable as the sole store |
| Two systems both edit the same entity | Only with a **per-field ownership map**; bidirectional sync is a build, with product tooling existing only for one specific ERP pairing | Same | Not viable | Same |
| Hard uniqueness on a business key; idempotent integration | Native — alternate keys, which are also the **upsert** mechanism | Native — unique index | Single-column uniqueness only | n/a |
| Multi-environment ALM for the **schema** | Native — solutions carry schema; data moves by a separate tool | Conditional — database DevOps sits **outside** the platform's lifecycle | Lists sit outside solutions; internal names drift when recreated | n/a |
| Team-scoped app on seeded licences, small footprint, no API/sharing/ALM | The team-scoped variant, within its combined capacity ceiling — **and the upgrade is one-way** | n/a | Conditional (lists) | n/a |
| Data must stay on-premises | Not supported (SaaS) | Conditional through a gateway, with payload caps, cluster operations, and results transiting the cloud | Not supported | Native **for the store**; platform transit remains cloud |
| No public endpoint on the cloud database | Conditional — IP firewall (managed environments) and outbound private networking | Conditional — private networking with its own preconditions, and the gateway is then excluded | Not supported | Via private network paths |
| Country-level or boundary residency | Conditional and **irreversible per environment** — the macro-region choice binds the tenant and every environment; a country-level guarantee needs an additional tenant-wide entitlement | Conditional on region choice | Conditional on the suite's geo | As is |
| Customer-controlled encryption key | Conditional — needs managed environments **and** a premium suite entitlement | Supported and **cheaper to reach**, scoped at server/instance/database level — but the key vault becomes a tier-0 availability dependency with a documented failure mode | **Conditional, not unsupported** — a dedicated tenant/geo-level policy exists; the real limit is *granularity*, plus premium entitlement and paid subscriptions | As is |

**Note the two corrections this map exists to carry.** *"The list store cannot do customer-managed keys"*
is **wrong** — the limit is granularity, not absence. And *"the relational store is the cheap archive"* is
**wrong** — no cold tier for rows exists there.

## 5. Decision-sensitive distinctions · `decision-grade`

- **Available ≠ enforced on the required plane.** A store that *can* express a rule in one client does not
  enforce it for every client. Where a rule must hold on integration paths, only a server-side mechanism
  qualifies — and one of those mechanisms is documented **inconsistently by the vendor itself** (see
  `dataverse.md`). Treat cross-client enforcement as `Assumed`, never `Confirmed`, until tested in the
  target environment.
- **Delegation-safe ≠ fast.** Correctness and latency are separate questions → `query-and-delegation.md`.
- **Capacity is an entitlement, not a technical limit** — and the meters are not interchangeable. The
  database meter is the binding and most expensive one, and borrowing flows in only one direction across
  the three. Exceeding capacity **blocks administrative operations** (copy, restore, create), which makes
  it an availability problem and not only a cost one.
- **Backups are not an archive.** A short, same-region, non-downloadable backup window and a recycle bin
  are recovery mechanisms. A retention requirement measured in years needs a retention mechanism.
- **A published aggregate ceiling bounds *aggregate queries, charts and dashboard grids* — not ordinary
  filtered reads**, which may return far more inside the query timeout. Reading the ceiling as a flat store
  limit is a common and consequential error.
  > Documented reading · read 2026-09-04 · re-verify: VS-06 (design time, before any reporting commitment)
  > (**50,000** rows for aggregate queries, charts and dashboard grids — **not** a ceiling on ordinary
  > filtered reads, which may return far more inside the query timeout. Scheduled replication has a
  > **30-minute** minimum increment, at most **48** refreshes per 24 h and a **24 h** maximum run.)
- **Security does not travel into an analytical copy.** Copies need row-level security **rebuilt**; secured
  columns export as null unless the sync identity is granted the profile; and an embedded report ignores
  app roles entirely.
- **Store choice driven by licence avoidance is a documented anti-pattern**, not a cost strategy (§9).
- **Vocabulary is pack-local.** *"System of record"* and *"source of truth"* have **no formal vendor
  definition** — the terms are used loosely and interchangeably across the vendor's own surfaces. The only
  near-definition ties source-of-truth to a **per-entity consistency requirement**. Declare the pack's
  vocabulary as pack-local; never cite the vendor as the authority for a formal distinction.

## 6. Does the reporting need force a second store? · `decision-grade`

This is the most common cross-store question, and it has one boundary and one consequence set.

**The boundary.** The operational store serves ordinary filtered reads within its query timeout. It does
**not** serve aggregation over large row counts, charts and dashboard grids past the published aggregate
ceiling, or cross-period history on growing tables. Where *aggregation, charts or multi-year history* are
required on growing tables, **an analytical copy is required from day one** — the vendor's own words are
to use a dedicated store for reporting purposes instead.

**What a copy obliges** — this is the decision-grade half, and it is what gets omitted:

| Obligation | Why |
|---|---|
| **A reconciliation owner** | A fast path loses updates by design; the vendor's own reference design has a scheduled bulk pass **repair** the event path. Cadence is a requirement input, and the pass is mandatory, not optional |
| **A drift-detection method that is not row counts** | Replicas diverge while reporting sync success: secured columns export as null, calculated columns freeze if the row version does not change, direct-database deletes never propagate, and new columns do not appear until a data change occurs. Row-count comparison detects none of these |
| **Resynchronisation as a routine budgeted operation** | It is the documented remedy for most drift modes — and its cost and duration at realistic volume are **not published** |
| **Rebuilt authorization** | §5 |
| **Capacity** | One analytical path bills its replica against the **operational database meter**; the ratio is unpublished |
| **Erasure propagation** | Append-only lake modes do not propagate deletes — a direct conflict with an erasure obligation |
| **An owner for schema change** | Schema changes break or pause the sync, and several pause causes sit outside the owning team's control |

**There is no first-party managed path from the governed store to a writable relational database.** Any
writable copy is a **customer-built and customer-operated** pipeline with its own watermark,
delete-detection and reconciliation job as first-class budgeted components. Where **no write is required**,
an auto-provisioned read-only analytical SQL endpoint answers the question with the lowest reconciliation
burden — prefer it over a custom pipeline whenever writes are not needed, noting its own type and
truncation limits.

## 7. Replication vs virtualization vs keep-in-place · `decision-grade`

| Choice | What it buys | What it forfeits or obliges |
|---|---|---|
| **Keep in place + embed / read-through** | No copy, no divergence, no capacity cost; the owning system keeps authority and audit | A **synchronous availability dependency** inherited by the UI; small payloads only; sensitive to delays |
| **Virtualization** | External data appears native **without replication** | Organization-scoped only, so **no row-level security**; no audit, no search, no offline, no rollups, no analytics on it; **column selection is ignored** — all attributes always return; it can never be the *"1"* side of a 1:N relationship; negative filter operators corrupt paging past the first page with **no supported workaround**; it is **absent from the delegable-source list**, so truncation can occur without even a warning. **No performance, latency, throughput, caching or pushdown characterisation is published at any volume.** Appropriate only as a narrow, positively-filtered, small, read-mostly reference surface with a **mandatory measured spike** before commitment — never as a general integration layer |
| **Replication (one-way subset)** | Full platform data features on the copy — audit, row security, search, offline, rollups | Everything in §6. Keyed by the source id and treated as a **disposable read model** |
| **Bidirectional sync** | Two masters | Conflict rules **per field**; product-grade tooling exists for exactly one ERP pairing and it *mutates the receiving schema*; otherwise it is a build |

**Freshness in a virtualization design is bounded by the *upstream* refresh, not by the virtualization.**
Trace the requirement to the original source's cadence and record it as a cross-team dependency.

**Migrate master data and open transactions, not closed history.** Separate configuration data from
migration data. *(The stronger form — "never migrate history" — is **pack opinion, not vendor guidance**;
the baseline could not source it.)*

## 8. Consequences elsewhere · `architecture-grade`

- **→ performance and cost.** The database meter is the binding one and cannot be offset; binaries belong
  on the cheaper file meter or outside the store; system tables (workflow logs, async operations,
  duplicate-record copies, import jobs, traces) grow silently on the database meter, and storage reports
  lag. **Lifecycle and housekeeping jobs are design components, not operations hygiene.** Audit volume is
  not data volume. See `performance/performance-and-scale.md` and
  `economics/licensing-and-cost-drivers.md`.
- **→ security and governance.** Most store-related controls — long-term retention, customer-managed keys,
  vendor-access approval, IP firewall, private networking, masking, extended backups, sharing limits — sit
  behind **managed environments**, a single licensing gate. **Data requirements therefore decide the
  licensing model.** See `governance/governance-and-environments.md` and `security/security-controls.md`.
- **→ irreversibility.** Region and residency are fixed at environment creation; ownership type is
  immutable at table creation; long-term retention and the team-scoped upgrade are one-way. These are ALM
  and reversibility facts as much as data facts → `alm/release-and-lifecycle.md`.
- **→ integration.** Delivery guarantees, idempotency mechanics, gateway envelopes and the network boundary
  are `integration/integration-mechanisms.md`.
- **→ operations.** Restore reality, storage-hygiene run-books and erasure run-books are
  `operations/operability-and-support.md`.

## 9. Failure modes · `decision-grade`

> **Licence-avoidance store choice.** Choosing a store because it rides seeded entitlement, for a
> requirement it does not support — relational integrity, delegable access paths, row scoping at scale,
> column confidentiality, transactions. The entitlement saved is real; so is the rebuild.

> **The operational store as the reporting warehouse.** Aggregate ceilings, query timeouts, and analytical
> traffic sharing the operational service-protection budget. The vendor's own instruction is a dedicated
> store for reporting purposes instead.

> **Replicating the whole external system, or closed history, into the platform store.** Capacity cost on
> the binding meter, service-protection pressure, and a documented *"too much data synchronised … overloads
> the database"*.

> **Two-way sync without a per-field ownership map.** Conflict resolution becomes undecidable and data is
> copied for every system.

> **Assuming a managed replication service exists.** It does not (§6); every writable copy is
> customer-operated.

> **Trusting row counts to detect replica drift.** At least eight documented silent-divergence modes all
> report sync success (§6).

> **Virtualization for data that needs audit, row security, search, offline, rollups or analytics.** All are
> forfeited by design (§7).

> **A spreadsheet as a store with more than one writer, or past the paging cliff.** Simultaneous file
> modification is documented as unsupported, the file locks for minutes after use, and retries insert
> duplicates. Seed, reference and export only.

> **Caching volatile or sensitive values** — price, credit limit, balances. A cache-aside pattern does not
> guarantee consistency; this class of data is always retrieved from the primary source.

> **Sensitive semantics in table, column or app names.** Names replicate globally regardless of the
> environment's region.

## 10. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Horizontally-scaling (elastic) table bounds and its contradicted maturity state | `VS-32` |
| Delegation ceilings (default and maximum) | `VS-02` |
| List-store view/query threshold — the access-path boundary | `VS-04` |
| List-store unique-permission scope ceiling — the row-authorization boundary | `VS-29` |
| Audit retention and log-availability windows | `VS-05` |
| Aggregation ceiling and the analytical-replication refresh window | `VS-06` |
| Backup retention windows by environment class | `VS-07` |
| Capacity consumption profile (the analytical-replication storage ratio is **unpublished**) | `VC-07` |
| The over-limit disablement countdown | `VS-09` |
| Preview / GA state — notably the horizontally-scaling table type, whose GA status is **unresolved** | `VC-10` |

**Not established in the baseline** — do not fill from general knowledge:

- **Any published row-count or size envelope for a standard table.** Only the horizontally-scaling table
  type carries a published scale claim. Promising a ceiling would be invention; validate by load or soak
  test at the projected multi-year volume.
- **Any concurrent-user ceiling for any surface.** No such figure is published anywhere. What governs
  instead is per-identity service protection, per-identity daily entitlement, and contention on shared rows
  and identities — never a headcount. The concurrency question is answered **only** by a load test against
  a production-like environment with realistic personas and data volumes.
- **Any write-amplification multiplier.** The platform counts internal system requests, plug-ins, classic
  workflows, custom controls, retries and pagination — but publishes **no multiplier**, because
  amplification is a property of each solution's own customisation. It must be **measured per engagement**,
  never assumed or carried over from another one.
- **The request cost of auditing per audited write.**
- **Read-after-write visibility across sessions or clients**, and whether any read replica could serve a
  stale read. Do not assert either way.
- **Connector-level concurrency, isolation and locking semantics** for the relational-store connector.
- **The magnitude of the database increase caused by an analytical link** (no published ratio).
- **Cost and duration of a full replica resynchronisation** at realistic volume.
- Whether the tenant default database capacity figure is the one in the licensing table or the one in the
  same guide's worked example — the source is **internally inconsistent**. Confirm in the administration
  centre.

## 11. What not to infer · `decision-grade`

- **A capability absence is not a verdict.** *"No column-level security in the list store"* is domain
  knowledge. *"Therefore inappropriate"* is a selection verdict and belongs to `decision-tree.md`.
- **There is no store ranking here, and no `*-first` branch.** The question this file answers is *what can
  this store support*, never *which store wins*.
- **A documented boundary here is not evidence that another option class does better.** The baseline holds
  no like-for-like comparison against non-platform data stacks; where the comparison is material,
  `decision-model/outcome-classes.md`'s comparator semantics stand.
- **Do not restate a scoped ceiling as a flat store limit** (§5).
- **Do not treat the vendor's reference-architecture defaults as evidence of superiority.** *"Building a new
  app and new storage → consider the governed store"* and *"the database already exists and cannot move →
  the relational store"* are **triggers**, not verdicts.
- Schema-modelling conventions, medallion layering, index policy, naming and stored-procedure patterns are
  **delivery practice** — `craft/sql-delivery-conventions.md` and `craft/delivery-conventions.md`, which are
  not Options pull targets.
