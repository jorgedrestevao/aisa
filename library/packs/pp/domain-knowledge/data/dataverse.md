# Dataverse — what the governed relational store actually provides

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *What transactional and authorization semantics does this store actually provide?*
- *Which decisions here cannot be undone after provisioning?*
- *What does enabling audit cost in capacity?*
- *Will this rule hold no matter which client writes — app, API, integration?*

This file states **Dataverse's own semantics and boundaries** — modelling, transactions, authorization,
audit, capacity, consistency and extension. It does not decide **whether Dataverse is the right store** —
that belongs to the decision model (`decision-tree.md` S4–S6). Cross-store comparison lives in
`data/store-boundaries.md`; access paths in `data/query-and-delegation.md`.

---

## 1. What this is for · `decision-grade`

Dataverse is a **governed** relational store: the schema, the security model, the audit trail, the
lifecycle and the capacity are platform-managed rather than administrator-managed. That is the whole
trade. What you gain is server-enforced authorization at row and column grain, a native audit plane,
solution-based schema lifecycle, and uniqueness that survives integration paths. What you give up is
physical control — you cannot add an index, you cannot tune the query plan, and several structural choices
are **fixed at creation**.

The consequence for Options is narrow and practical: **most of the expensive decisions about Dataverse are
made before the first row exists**, and a handful of them cannot be revised later without rebuild plus
migration. This file exists so those are recognised as decisions, at the moment they are still open.

## 2. When it becomes material · `decision-grade`

- A rule must hold **regardless of which client writes** (app, Web API, integration, ETL).
- Two or more rows must be written **all-or-nothing**.
- Row visibility depends on **owner, team or organisational unit**; or a **column** must be confidential.
- A **field-change audit** is required, or **retention** is measured in years.
- A table is expected to grow, or **binaries and audit** will be a material share of the volume.
- **Concurrent edits** on the same record are expected.
- A child entity plausibly has **two strong parents**.
- Uniqueness on a business key must hold, and a **migration will be rehearsed more than once**.
- High-churn, weakly-related data (events, telemetry, staging) sits beside transactional data.
- The store must serve both **operational** and **analytical** use.

## 3. Modelling and relationship semantics · `decision-grade`

**1:N and N:N are both supported. Cascading is not free, and it is bounded.**

- **One parental (cascading) relationship per child table.** A child cannot inherit ownership and access
  from two parents. A row that is conceptually owned by both an order and a shipment must nominate a
  **dominant parent**; the second becomes a referential lookup plus explicit process.
- **Cascade behaviour is a security and storage decision embedded in the ERD, not a modelling detail.**
  Cascading *Share* and *Reparent* propagate access silently down the child chain. Every share, access-team
  grant and cascade writes rows into the platform's access table — rows that **cannot be deleted directly**;
  the documented remedy is to change the security model, not to clean up. The default on Reparent is the
  permissive one, which makes it the principal growth driver.
- **N:N relationships are supported between standard tables**, but not from the horizontally-scaling
  (elastic) table type to standard tables (§10).
- **Deliberate denormalisation is sanctioned** where a filter or sort must be served from one row. On the
  elastic table type it is explicitly recommended, because filters on related tables are not available
  there at all.

**What follows for the model.** Ownership type, the parental relationship, the cascade configuration and
the filterable-column shape are the four modelling choices that are cheap now and expensive later. Access
requirements expressed as *"ad-hoc, per-record, many-to-many"* force per-record sharing, which the vendor
itself describes as an **exception mechanism and the less performant path**. *"By organisational unit"* maps
to business units plus roles; *"a manager sees the team"* maps to hierarchy security, which carries a
documented recommended ceiling on effective users under one manager; *"named collaborators per record"*
maps to access teams **with an unshare lifecycle**, which is a design component, not a detail.

## 4. What cannot be undone after provisioning · `decision-grade`

This is the section that earns the file. Each item is irreversible or one-way; each is decided **before or
at creation**, and several are decided by someone who is not in the room during Options.

| Decision | Where it is fixed | What reversal actually costs |
|---|---|---|
| **Ownership type** — organisation-owned vs user/team-owned | At **table creation** | Cannot be changed. The vendor's own instruction is to **delete the table and create a new one** — i.e. rebuild plus data migration. Any table that may *plausibly later* need row-level segmentation must be user/team-owned from the start |
| **Region / residency** | At **environment creation** | Fixed, and it binds Dataverse, apps, connections and gateways. Restore and customer-managed key operations are same-region. A boundary commitment (e.g. an EU data boundary) requires the tenant **and every environment** — one out-of-boundary sandbox breaks it. Country-level granularity needs an additional tenant-wide entitlement, otherwise the datacentre within the macro region is the vendor's choice |
| **Long-term retention** | At policy execution | **One-way.** Retained data cannot be returned to the live application state. It becomes read-only, leaves live views and the read-only SQL endpoint, and is **not portable in solutions** |
| **Team-scoped (Teams) environment upgrade** | At upgrade | **One-way**, and it requires tenant capacity plus premium entitlement for **all** users of the apps involved. The team-scoped variant also has no API, no record sharing, and a combined capacity ceiling that cannot be extended |
| **Owning business unit of a row** | At creation, unless the modernised business-unit model is in use | Immutable otherwise. Business units and teams are **per environment and not solution-portable**, so a sync carrying the owning unit fails against an environment that lacks the same value |
| **Column schema name and data type** | At **first save** | Cannot be changed (one narrow text conversion aside). Type migration is add-migrate-retire. **Deleting a column deletes its data**, and removing a choice option invalidates the rows that used it |
| **Maximum file size on a file column** | At first save | Cannot be raised afterwards. Images are converted on upload |
| **Partition key on an elastic table** | At first write of the row | If left unset it stays unset and cannot be set later |
| **Privilege direction** | Structural | Privileges are **strictly additive** — the greatest access prevails. Broad organisation-level read cannot later be narrowed to hide a single row |

**Residency has exceptions that survive the region choice.** Table and column *names*, app names,
descriptions and logos, and the Power Pages site name and URL **replicate globally**. Preview features
typically store data in one specific region regardless. Generative-AI inputs and outputs may move outside
the region, movement that already occurred **cannot be reversed**, and cross-region routing defaults are
tenant-creation-date dependent. Consequence: sensitive semantics must be kept out of schema and app names,
and *"no processing outside the region"* is not the default posture.

## 5. Integrity that holds on every write path · `decision-grade`

The question *"will this rule hold no matter which client writes?"* has a precise and uncomfortable answer.

**Alternate keys are the mechanism.** An alternate key is a real server-side uniqueness constraint,
enforced on every write path, backed by a database index. It is also the **upsert** mechanism — which makes
it the **idempotency** mechanism for integrations *and* the **migration-idempotency** mechanism, because a
migration is rehearsed at least across integration test, acceptance test and cutover. Without a
natural-key upsert, each rehearsal either duplicates everything or needs a manual wipe.

> Documented reading · read 2026-09-04 · re-verify: VS-30 (design time)
> (at most **10** alternate keys per table, each at most **16** columns and **900** bytes of total key
> width — which is what an integration's natural key has to fit inside)

Its limits are real and often discovered late:

- A **small fixed per-table budget** of keys, shared between business-integrity keys and
  migration/integration addressing keys. They compete for the same budget.
- A bounded number of columns and total key width.
- **Not available on secured columns, and not on virtual tables** — the platform cannot enforce uniqueness
  over data it does not hold.
- Certain reserved characters in key values break the addressing form used by direct record access.
- If the legacy source has **no reliable natural key** — typical of spreadsheet-origin data — a surrogate
  must be manufactured *and written back to the source* before the first rehearsal. That is unbudgeted work
  discovered at the worst moment.

**Duplicate detection is not the mechanism.** It is advisory, has default rules only for a few
out-of-the-box tables and none for custom tables, and — the load-bearing fact — it is **suppressed by
default on Web API updates**. Every flow, function, dataflow and ETL write that does not explicitly opt in
creates duplicates the interactive UI would have blocked. When a rule does fire, the failure surfaces as a
**server-error class response, not a validation-class one**, so naive retry logic loops on a business
rejection.

> **The vendor's own documentation contradicts itself on whether table-scoped business rules execute
> server-side.** One part of the same page states that entity/table scope reaches *"Model-driven app forms
> and server"* and describes server-side rules as compiled synchronous plug-ins; the FAQ on that same page
> states flatly that business rules run on clients and *"aren't executed inside Dataverse"*. **This is not
> resolved here and must not be resolved by inference.** Treat cross-client server-side enforcement of
> business rules as **`Assumed`, never `Confirmed`**, until tested in the target environment. The test is
> cheap and specific: activate a table-scoped validate-and-error rule, attempt a violating create through
> the Web API, observe. Where the guarantee is genuinely required — financial, regulatory, safety — use an
> explicit server-side mechanism or a key-level constraint rather than a business rule.

**Business rules are also not retroactive.** Activating a rule does nothing to existing rows. A new
validation never cleans legacy data; that remains human cleansing work.

## 6. The extension-mechanism boundary · `decision-grade`

These are **capability boundaries**, not a preference ranking. Read them as *"what can this mechanism
express, and on which write paths"* — never as *"which one to use"*.

| Mechanism | What it can express | Which write paths it reaches |
|---|---|---|
| **Business rule — form scope** | Requirement levels, show/hide, enable/disable, recommendations | The model-driven form only. **Bypassable by every other client.** A form-scoped rule referencing a field that is not on the form **silently does nothing** — no error, no signal |
| **Business rule — table scope** | Set value, clear value, set default, validate-and-error. Nothing richer | Model-driven **and canvas**; server-side reach is **`Assumed`, not `Confirmed`** (§5). Cannot handle multi-select choice, file or language columns **at all**, at any scope. Not available in editable subgrids or other dataset controls. A documented per-table rule ceiling exists, counting client and server rules together, beyond which the vendor warns of degradation |
| **Power Fx in the client** | Any expression the client can evaluate | The client that runs it. **Never transactional**, even within one store (§7) |
| **Cloud flow** | Orchestration, long-running work, cross-system calls | Asynchronous. Not an atomicity mechanism; it consumes its own request budget and carries its own retry semantics → `automation/automation-mechanisms.md` |
| **Synchronous plug-in / custom API / transaction API** | Arbitrary server-side logic, **inside a transaction** | Every write path, because it is in the write pipeline. Cost: pro-code, ALM overhead, different skills, and synchronous execution time is added to the calling request |

**The fork that changes a project's shape.** A single requirement that low-code validation cannot express —
a multi-select validation, a cross-row rule ("no overlapping bookings", "line sum equals header"), a
guaranteed API-path constraint — converts the build from low-code to **partly pro-code**, regardless of
which store is chosen. That fork must be identified in Discovery, because it changes cost and staffing, not
just design.

## 7. Transactional scope, and where atomicity stops · `decision-grade`

**Atomicity exists only server-side.** The client expression layer is **never** transactional — not across
stores, not even within Dataverse. Sequential client-side writes are independent operations: if the parent
succeeds and the child fails, the parent **remains**.

The mechanisms that do provide a transaction boundary are the change set / transaction API, a **synchronous**
plug-in, and a custom API. Where atomicity stops:

- **Elastic tables**: multi-record transactions are not supported; grouped operations *succeed* but are
  **not atomic**. Deep insert is not supported there either.
- **File and image column uploads**: they happen **immediately, not on form save** — outside the record's
  save semantics.
- **Asynchronous derived values**: a rollup cannot participate in the transaction that produced it (§12).
- **Across stores or systems**: no transaction exists. The pattern is a saga with local pending state, the
  external posting as the irreversible pivot, irreversible steps last, and a **human fallback**.
  Compensating actions are not guaranteed to succeed.
- **Outbound synchronous notification during a write** is a dual-write hazard: the data operation can roll
  back while the request already sent to the external endpoint **cannot be recalled**.

So the practical rule: **if a unit of work spans more than one row, name its transaction mechanism during
Options** — because the answer determines whether the solution needs server-side code, and that is a cost
and skills decision, not a build detail.

## 8. Authorization grain · `decision-grade`

Dataverse is the store in the platform that enforces authorization **at the API plane**, not in the app.
The planes, coarse to fine:

1. **Business unit** — the organisational partition. Few and stable is the sanctioned shape; the vendor
   explicitly advises against creating a large number of them.
2. **Security role** — additive privileges at organisation / unit / unit-and-child / user depth.
3. **Team** (owner teams, access teams) — the performant path for "these named people on this record".
4. **Row** — ownership plus, as an exception, per-record sharing. Sharing is the vendor's own *exception*
   mechanism and *less performant* path, and it writes rows into an access table that cannot be cleaned
   directly (§3).
5. **Hierarchy security** — manager/position visibility, with a documented recommended ceiling of effective
   users under one manager.
6. **Column security** — the finest grain, and the one no other store in the platform offers at API level.

**Column security has hard edges that must be known before a model is drawn:**

- **Not securable**: virtual-table columns, **lookup columns**, **formula columns**, **primary name
  columns**, system columns. A confidential value modelled as the primary name or as a lookup **cannot be
  secured at all**.
- **Data is never hidden from system administrators.** If the requirement is "hidden from administrators
  too", column security does not satisfy it; that requires separation of duties plus customer-managed keys
  plus vendor-access approval, or keeping the data out of the platform.
- **Masking rules require Managed Environments.**

**The licence chain, stated plainly.** Most authorization- and data-adjacent controls — long-term retention,
customer-managed key, vendor-access approval (Lockbox), IP firewall, private networking, **masking rules**,
extended backups, sharing limits, data policies — sit behind **Managed Environments**. Several of them
additionally require a premium suite entitlement. And a **dated enforcement tripwire (`TW-V3`)** turns
Managed Environments into a per-active-user licence obligation for **the whole environment population**,
not just the app's own users. **Therefore data and security requirements decide the licensing model**, and a
solution scoped as "seeded entitlement only" cannot meet this class of requirement at all →
`economics/licensing-and-cost-drivers.md`, `governance/governance-and-environments.md`.

**Authorization does not travel into an analytical copy.** The read-only SQL endpoint and direct-query
reporting honour the store's roles per user; a replicated copy needs row-level security **rebuilt**, and
secured columns export as **null** unless the sync identity is granted the column-security profile — a fix
that widens exposure to every reader of the copy. An embedded report inside a model-driven form ignores app
security roles entirely. → `security/security-controls.md`.

## 9. Audit and long-term retention semantics · `decision-grade`

**What audit costs, concretely.** Audit lands on the **log meter**, not the database meter — a different,
cheaper meter, but an uncapped one if left unscoped.

- **Default retention is unbounded** (*"Forever"*).
  > Documented reading · read 2026-09-04 · re-verify: VS-05 (Options, and at any compliance review)
- **Changing retention is not retroactive.** Rows already written keep the retention they were written
  under. A requirement stated as *"audit for N years"* must therefore be **configured at environment
  creation**, not discovered at go-live.
- **Large values are truncated** at a small documented threshold — the audit trail is not a full copy of
  the changed value.
- **Read and export operations are not audited** in Dataverse. Access auditing is a separate,
  production-only governance plane, and from a dated cut-off it **no longer receives field values**.
- **There is no export UI.** Audit reporting requires the API or an analytical replication path (which
  supports it only in specific modes).
- **Customer-managed-key environments cannot set audit retention at all** — deletion jobs replace policy.
- **Audit is excluded** from the read-only SQL endpoint, from long-term retention, and by default from
  environment copies.

**The unmeasured part, and it is decision-material.** The **request cost of auditing per audited write is
not published**. A high-volume audited table may consume materially more request budget than a model
assumes. Measure it on a prototype with audit on versus off; do not assume it is free.

**Long-term retention is a capacity mechanism, not an archive product.**

- Requires **Managed Environments**; policies are disabled without it.
- **One-way** (§4). Retained data is read-only, queryable only through specific surfaces, and not portable
  in solutions.
- It reduces the database meter by **roughly half on average**, and **files not at all**.
  > Documented reading · read 2026-09-04 · re-verify: VC-07 (design time, and annually)
- **Audit tables and elastic tables are excluded.**
- A policy run **executes existing delete-cascade behaviour and server-side logic**, consumes request
  budget, and takes on the order of days rather than minutes.
- Take the analytical copy **before** retention runs — retained rows leave live views, and one analytical
  path drops retained data from its shortcuts on engine migration.

**Backups and the recycle bin are recovery, not retention** — a short, same-region, non-downloadable window
by environment class (`VS-07`), and an opt-in bin that captures **deletes only** and only from the moment it
was enabled. "We can always restore it" is false for a record deleted months ago.

## 10. Consistency: standard vs elastic tables · `decision-grade`

Two table types with **different consistency contracts** on the same platform.

| | **Standard tables** | **Elastic tables** |
|---|---|---|
| Substrate | Relational, with transaction support | Horizontally-scaling document store |
| Consistency | The vendor's stated criterion for *"requires strong data consistency"* | **Strong within a logical session only.** Read-your-writes and write-follows-reads hold *inside* one session; **another session may not see the write immediately** — and a read issued without the session token may miss recent changes entirely |
| Transactions | Change set / transaction API / synchronous plug-in / custom API | **None.** No multi-record transactions, no grouped-transaction semantics, no deep insert |
| Relationships | 1:N, N:N, one parental relationship per child | **No N:N to standard tables**, no cascades, no filters on related tables in views or queries |
| Derived and integrity features | Rollups, calculated and formula columns, alternate keys, duplicate detection | **None of these** |
| Sharing / access | Sharing, access teams, cascades | **No table sharing, no access teams, no queues** |
| Other forfeits | — | Business rules, charts, business process flows, the first-party analytical connector, the read-only SQL endpoint, attachments, table import/export, long-term retention |
| Recovery | Standard backup/restore semantics | Point-in-time restore recovers **creates and deletes only** — not updates |
| Partitioning | n/a | Partition key **immutable once unset or set** (§4); a bounded size per logical partition |

**Elastic is a per-table decision for high-churn, weakly-related data** — telemetry, events, log lines,
staging — and it is also an **isolation** mechanism, since that traffic then does not share the relational
tables' path. It is not a global escape hatch for an audited transactional model.

> **The elastic table type's general-availability status is UNRESOLVED in the baseline.** One current
> vendor page says known issues should be addressed *before the feature becomes generally available*, while
> other current pages describe it without a preview caveat. **Do not assert GA.** Treat it as a **maturity
> risk** with a named verification step (`VC-10`). Its support for alternate keys is likewise contradicted
> across pages.

**Two consistency questions the baseline does not answer, and neither may be asserted:** whether standard
tables guarantee **read-after-write across a different session or client** (a flow reading what a plug-in
just wrote elsewhere), and whether any read replica could serve a stale read. The vendor states the
*choice criterion* and the substrate, not a named guarantee. Do not fill this from general knowledge.

## 11. Capacity: three meters, one binding · `decision-grade`

**Capacity is an entitlement, not a technical limit** — there is no published technical size limit on an
environment. But the meters behave asymmetrically, and that asymmetry is a design input.

- **Three meters — database, file, log — with table and column placement fixed by type.** Attachments,
  notes and any table carrying a file or image column bill to **file**. Audit rows, plug-in traces and
  elastic tables bill to **log**. **Everything else bills to database**, and the database meter includes
  **index files**.
- **Borrowing is one-directional: database → log → file, never back.** **Database overages cannot be
  offset**, because it is the highest-value meter. Spare file capacity cannot rescue a database overage.
- **Being over capacity is an availability problem, not only a cost one.** It blocks environment creation,
  copy and restore — i.e. it breaks ALM and compliance work before it breaks the app. There is an
  over-limit disablement countdown (`VS-09`), and notification thresholds fire on remaining headroom.

**What silently consumes the database meter** — this list is the one that gets missed:

- **System tables**: workflow logs, asynchronous operation records, duplicate-record copies, import jobs,
  bulk-delete operations, trace logs. They grow on their own; recurring housekeeping jobs are **design
  components**, not operations hygiene.
- **Search infrastructure**: the search index table and administrator-configured quick-find columns
  **create indexes**, and all indexes report at the database rate (§13).
- **The analytical replica of one of the analytical link paths** bills as **Dataverse database** storage.
  The marketing framing of "no copy" is accurate only in the sense of "no copy *outside* platform-managed
  storage" — a billed replica exists. **The ratio is unpublished** (`VC-07`); pilot it.
- **Every full-data sandbox copy** replicates the full data *and index* footprint.
- Storage reporting **lags** by days, so growth is discovered late.

> **The tenant default database capacity figure is CONFLICTED in the baseline** — the same source's table
> and its own worked example disagree. **Neither figure is carried here.** The fact is
> **decision-blocked until re-verified** in the administration centre at the decision date; owning row
> `VC-07`.

Request throughput is a separate envelope from storage, and it is licence-shaped rather than a tunable knob
→ `performance/performance-and-scale.md`.

## 12. Derived columns: rollup, calculated, formula · `decision-grade`

Three derived-column kinds, three different boundaries. Getting this wrong produces a requirement that
looks satisfied and is not.

- **Rollup columns are asynchronous.** They are computed by scheduled background jobs with a documented
  **minimum recurrence measured in hours**, are limited to a bounded budget **per table and per
  environment**, work over 1:N only (**not N:N**), aggregate under a system context, and **cannot trigger**
  workflows or plug-ins. Consequence: **a rollup cannot gate a write.** A real-time balance, stock level or
  credit check that must block a save is not a rollup — it is a server-side computation or a plug-in-
  maintained persisted column.
- **Formula columns are computed at read time.** They cannot be sorted on when they reference a related
  table's column, do not display in mobile offline mode, cannot trigger workflows or plug-ins, are not
  searchable, and **cannot be secured** with column security (§8). **Filters on computed columns are
  throttled by the platform.**
- **Calculated columns** share the read-time family's limits and the same throttling behaviour on filters.

**The rule that follows:** a derived value used for **filtering, sorting or securing at scale must be
persisted**, not computed at read time. Informational KPIs can be derived; anything on an access path or a
security boundary cannot.

**And you cannot fix it later with an index.** Indexes are platform-managed; automatic tuning and query
optimisation are on by default and not configurable. Query hints are gated behind *"only when recommended
by vendor technical support"*. Automatic optimisation also makes some performance problems **irreproducible**
— the vendor says so explicitly, which is a diagnosis hazard. The levers available at design time are
**schema and query shape**: alternate keys, short filterable text columns, denormalised sort keys, and
positive filters. Whether support will create a custom index on request is **not documented**.

## 13. Search is a finite, eventually consistent, billed resource · `decision-grade`

"Search across everything" is a design artefact with a budget, not a default.

- A **bounded org-wide budget of searchable fields**, and columns are **weighted by type** — a lookup or a
  choice consumes more of the budget than a simple column. The budget is organisation-wide, not per table.
- **Related-table fields are not searchable.**
- **Eventually consistent**, with a documented sync lag ranging from minutes to, for large organisations,
  days. **Do not promise real-time search.**
- **Rate-limited per user**, and the index infrastructure bills on the **database** meter (§11).
- Free-text `contains` with a **leading wildcard cannot use indexes and is throttled** by the platform; the
  vendor's own remedy is to route free-text to the search service rather than to grid filters.
- Multiline text columns should be excluded from the index — they inflate it materially.

## 14. Virtual tables — and what they forfeit · `decision-grade`

Virtual tables surface external data inside Dataverse **without replication**. The forfeited list is
almost exactly the list of reasons anyone wants Dataverse in the first place:

- **Organisation-owned only — therefore no row-level security**, and **no column security**. The vendor's
  own instruction is to implement your own security model in the source system.
- **No auditing. No alternate keys** (uniqueness cannot be enforced over data the platform does not hold).
  **No duplicate detection. No rollup, calculated or formula columns.** Column metadata validation on
  update does not apply.
- **No change tracking, and therefore no analytical replication.** No Dataverse search, no offline, no
  business process flows, no dashboards, no Power Pages.
- **A virtual table can never be the "1" side of a 1:N relationship.**
- **Column selection is ignored** — every attribute returns on every query. **Negative filter operators
  corrupt paging past the first page**, with no supported workaround. It is **absent from the
  delegable-source list**, so truncation can occur **without even a delegation warning**. The relational
  provider uses **one shared credential for all users**, and views are read-only.
- **No performance, latency, throughput, caching or query-pushdown characterisation is published at any
  volume.** That is a documented absence, not an open question awaiting a better search.

**Where the boundary sits** *(supported synthesis, not a vendor-endorsed pattern)*: virtual tables hold up
as a **narrow, positively-filtered, small, read-mostly reference or lookup surface**, with a **mandatory
measured spike** before commitment. Where row-level security, audit, per-user source identity, browsing or
exclusion-filtering of a large set, native children of the external master, offline, search, or any latency
or throughput commitment is in scope, the mechanism does not provide it. The alternative to weigh in every
case is **ingesting a subset into a native table** and accepting duplication in exchange for row security,
audit, delegation, offline, relationships and a **known** performance profile.

Read-only virtualization over an analytical lake surface is **explicitly read-only** — there is no
write-back through it, and any return path must be built as a separate integration with its own identity
and error handling.

## 15. Failure modes · `decision-grade`

> **Relying on a business rule for cross-client enforcement without testing it.** The vendor's own
> documentation contradicts itself at exactly the point that matters (§5). The rule appears configured, the
> UI honours it, and the integration path may write straight past it. Consequence: the constraint is
> `Assumed`; the named test is a requirement, not a nicety.

> **Assuming duplicate detection protects integration writes.** It is suppressed by default on Web API
> updates and has no default rules for custom tables. The duplicates accumulate invisibly and surface at
> reconciliation, and the rejection arrives as a server-error class response that naive retry logic loops on.

> **Per-record sharing as the default access model, with parental relationships everywhere.** Every share
> and every cascade writes access rows that cannot be deleted directly, on the database meter *and* on the
> hot path of every access check. The model degrades gradually and the remedy is a security-model change,
> not a cleanup script.

> **Organisation-owned tables for data that may ever need segmentation.** Ownership type is immutable; the
> reversal is delete-and-recreate plus migration. The cost lands at the moment a second department, region
> or customer appears — which is precisely when the solution is judged successful.

> **Business units mapped one-to-one to a volatile org chart.** A re-org becomes a data-migration event:
> role assignments can be stripped, records move, and the reassignment is sequential and fail-stop.

> **"Audit everything, forever" without scoping.** Unbounded growth on the log meter, retention that cannot
> be applied retroactively, and no export UI. The compliance requirement is met and the capacity plan is not.

> **A rollup used to gate a write.** It is asynchronous with an hours-scale floor and cannot trigger logic.
> The check passes against a stale value and the rule it was protecting is silently unenforced.

> **Elastic tables for transactional or relational entities.** No transactions, no joins, no N:N to standard
> tables, no rollups, no alternate keys, no sharing. Chosen for volume, it removes the integrity mechanisms
> the entity needed.

## 16. Consequences elsewhere · `decision-grade`

- **→ `performance/performance-and-scale.md`.** The three meters and their one-directional borrowing; the
  aggregation and dashboard-grid ceiling and the query timeouts that bound in-platform reporting; the
  request-budget envelope and the fact that internal system requests, plug-ins, classic workflows, retries
  and pagination all count; analytical traffic on the read-only SQL endpoint sharing the operational
  service-protection budget.
- **→ `economics/licensing-and-cost-drivers.md`.** Audit as log-meter consumption with an unbounded default
  and an unpublished per-write request cost; the storage meters and what silently loads the binding one
  (system tables, search indexes, the analytical replica, full sandbox copies); the **Managed-Environment
  licence chain** and its dated enforcement tripwire (`TW-V3`), which prices the whole environment
  population rather than the app's own users.
- **→ `governance/governance-and-environments.md`.** **Managed Environments is the gate** for long-term
  retention, customer-managed keys, vendor-access approval, IP firewall, private networking, masking,
  extended backups and sharing limits. Environment strategy is therefore a data-requirement decision, and
  business units and teams are per-environment and not solution-portable.
- **→ `security/security-controls.md`.** The **column-security plane** and its hard edges (lookup, formula
  and primary-name columns are not securable; administrators always see the data; masking needs Managed
  Environments), and the fact that authorization does not travel into an analytical copy.
- **→ `alm/release-and-lifecycle.md`.** **Irreversibility** (§4) as a release-planning fact: ownership type,
  region, retention and the team-scoped upgrade are one-way. **Solutions carry schema, not data** —
  deleting a managed solution deletes its tables' and columns' data; reference and configuration data need
  their own deterministic pipeline keyed on alternate keys, and business units, teams and retained data are
  not portable.
- **→ `data/query-and-delegation.md`.** Filterable-column design, delegable operation sets, paging
  behaviour, and why filters on computed columns and leading-wildcard searches are throttled.
- **→ `data/store-boundaries.md`.** The cross-store comparison, the "view or data?" question, and what
  replication versus virtualization obliges.
- **→ `integration/integration-mechanisms.md`.** Idempotency mechanics on the alternate key, at-least-once
  delivery, the outbound synchronous-notification hazard, and retry ownership.
- **→ `operations/operability-and-support.md`.** Storage-hygiene run-books, restore reality, and erasure
  run-books across every copy.

## 17. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Governed-store schema-object budgets — alternate keys and their column and width bounds, derived-column counts, table-scoped rule counts, row-byte budget, indexable text length | `VS-30` |
| Search budget and index freshness — the org-wide searchable-field budget and its per-type weighting, per-identity search rate, index lag, and the permanence window on index removal | `VS-31` |
| Horizontally-scaling (elastic) table bounds **and its contradicted maturity state** — the row owns the re-verification, never a settled answer | `VS-32` |
| Query traversal and projection bounds — lookup-traversal depth and its stricter offline variant, expandable entities per query | `VS-33` |
| Audit retention and log-availability windows | `VS-05` |
| Aggregation ceiling and the analytical-replication refresh window | `VS-06` |
| Backup retention windows by environment class | `VS-07` |
| Capacity consumption profile — including the **unpublished** analytical-replica storage ratio and the **internally inconsistent** tenant default database capacity | `VC-07` |
| The over-limit disablement countdown | `VS-09` |
| Request rate per acting identity | `VC-04` |
| Entitlement fit of the required capability set (the Managed-Environment chain) | `VC-05` |
| Preview / GA state — **notably the elastic table type, whose GA status is unresolved**, and its contradicted alternate-key support | `VC-10` |
| Managed-environment licence enforcement, dated | `TW-V3` |

**Not established in the baseline — do not fill from general knowledge:**

- **Whether table-scoped business rules execute server-side on API and integration writes.** The vendor's
  own page argues both ways (§5). This is the single highest-value empirical test in this domain; run it
  before any design relies on it.
- **Any published row-count or size envelope for a standard table.** None exists. Only the elastic table
  type carries published scale claims. A ceiling promise would be invention; validate by load or soak test
  at the projected multi-year volume.
- **Any concurrent-user ceiling for any surface.** No such figure is published. What governs instead is
  per-identity service protection, per-identity daily entitlement, and contention on **shared rows and
  shared identities** — never a headcount. Identify every funnel point where many users' traffic collapses
  onto one identity or one row, and load-test those against a production-like environment with realistic
  personas and data volumes.
- **Any write-amplification multiplier.** The platform counts internal system requests plus every
  plug-in, classic workflow and custom-control operation, plus retries and pagination — but publishes **no
  multiplier**, because amplification is a property of each solution's own customisation. It must be
  **measured per engagement**, never assumed and never carried over from another engagement.
- **The request cost of auditing per audited write** (§9).
- **Read-after-write visibility across sessions or clients**, and whether any read replica could serve a
  stale read (§10).
- **Whether vendor support creates custom indexes on standard tables on request** (§12).
- **The cost and duration of a full analytical-replica resynchronisation** at realistic volume — it is the
  documented remedy for most replica-drift modes, and its price is unpublished.
- **The magnitude of the database increase** caused by enabling the analytical link.

## 18. What not to infer · `decision-grade`

- **A capability absence is not a verdict.** *"Rollups cannot gate a write"* is domain knowledge.
  *"Therefore Dataverse is unsuitable"* is a selection verdict and belongs to `decision-tree.md`.
- **A documented boundary here is not evidence that another option class performs better.** The baseline
  holds no like-for-like evaluation of SaaS, custom/pro-code, incumbent platforms or other low-code stacks
  against these boundaries. Where such a comparison is material to the decision, the decision model's
  comparator semantics stand.
- **There is no `*-first` branch here**, no store ranking, and no threshold that disqualifies anything.
- **Do not read the vendor's reference-architecture default as proof of superiority.** *"New app and new
  storage → consider this store"* and *"the database already exists and cannot move → the relational
  store"* are **triggers**, not verdicts.
- **Do not treat a scoped ceiling as a flat store limit.** The published aggregation ceiling bounds
  aggregate queries, charts and dashboard grids — **not** ordinary filtered reads, which may return far
  more within the query timeout.
- **Do not treat "no copy" as no capacity cost** (§11), and do not treat backups as retention (§9).
- **Do not cite the vendor as the authority for a formal *system of record* versus *source of truth*
  distinction** — the terms are used loosely and interchangeably across its own surfaces. Pack vocabulary
  is pack-local.
- *"Never migrate historical data"* is **pack opinion, not vendor guidance**; the sourced statement is only
  that migration scope is master data and open transactions.

## 19. Where the build detail lives · `implementation-grade`

Schema-rigour conventions, naming, column-length and index-shaping conventions, choice-versus-lookup
conventions, stored-procedure and medallion patterns, plug-in packaging, and migration tooling mechanics are
**delivery practice**, not platform limits: `craft/sql-delivery-conventions.md` and
`craft/delivery-conventions.md`. Those files are never Options pull targets and may never state a platform
limit.
