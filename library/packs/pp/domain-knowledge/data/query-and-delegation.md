# Query and delegation — access paths, silent truncation, and where the query actually runs

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Is this access path delegation-safe — and does delegation-safe also mean fast enough here?*
- *What silently truncates?*
- *Which filter columns must be indexed for this access path?*
- *What must the server pre-shape so the client never has to?*

This file states **where a query actually executes, and what happens to the answer when it does not
execute at the source**. It does not decide which store, which surface or which option wins — that
belongs to the decision model (`decision-tree.md` S4–S6).

**This is the single authority in this directory for delegable-operation behaviour.** No other file
states a delegable-operation table. `craft/powerfx.md` refers *to this file* for the platform boundary
and never the reverse; formula patterns, workarounds, validation sequences and control-property
references are delivery practice and live there, not here.

---

## 1. What this is for · `decision-grade`

**Delegation-safe ≠ fast.** This is the load-bearing distinction, and collapsing the two produces false
verdicts in both directions.

```text
delegation  →  a CORRECTNESS property.  Does the query execute at the source,
                or does the client silently truncate the row set and answer from a fragment?
latency     →  a SEPARATE question, with SEPARATE levers.
                Round trips, payload width, back-end query shape, client-side processing.
```

- A **delegable** query can still be slow — a wide row on the list store transmits every defined column
  whether the app uses it or not, and dynamic lookup columns add server-side work before anything is
  returned.
- A **non-delegable** query can be entirely correct and fast — below the client's row ceiling, any source
  and any formula works, because the whole table is inside the fragment.

So "no delegation warnings" is not a performance verdict, and "it feels fast in the demo" is not a
correctness verdict. They are two different tests, run against two different requirements.

> The correctness framing above is **supported synthesis over vendor statements**, not a vendor-endorsed
> framing. The vendor publishes the truncation mechanism and its consequence; the "correctness, not
> performance" reading is the baseline's own.

## 2. When it becomes material · `decision-grade`

- Any queried entity **will exceed the client's non-delegable row ceiling** within the horizon.
- A **missing row is a business error** — registers, approvals, inventory, reconciliation.
- The requirement is **free filtering, free search, sorting by categorical fields, or negation**.
- A **count, total or average** is displayed and must be right.
- The access path crosses a **relationship** (list shows entity + parent + person + status).
- The source is a **custom connector, a virtual table, a spreadsheet or a collection**.
- Latency, not correctness, is the complaint — and the access path has never been shaped.

---

## 3. Delegation is a correctness property · `decision-grade`

**The mechanism.** A query is non-delegable if it uses a feature the source does not support. **If any
part of the expression is non-delegable, none of the query is delegated.** The client then retrieves the
first *N* rows from the source and evaluates the whole expression locally against that fragment.

> Documented reading (delegation ceiling — default and maximum rows retrieved for a non-delegable query)
> · read 2026-09-04 · re-verify: VS-02 (design time, per data source)
>
> **Default 500 rows; raisable to a maximum of 2,000.** The ceiling is **per query, not per app**, and it
> is not a store size limit. Below the default, any source and any formula works.

**The failure is silent wrongness, not slowness.** The vendor's own examples: over ten million rows, a
non-delegable filter for names beginning with "Z" returns the first 500 or 2,000 rows — *"so, you get
incorrect results"*; a filter whose target row is number 501 or 500,001 *"doesn't find or return it"*; an
average over a non-delegable read averages only the first 500 rows, and *"a user might think a partial
answer is the complete answer"*. Nothing errors at runtime. The number on the screen is plausible.

**The design-time signal is not a gate.** Two documented traps produce **no warning at all**:

1. **Collections.** `With`, `UpdateContext` and `Set` create collections internally. Collections are a
   static in-memory list of records and cannot participate in delegation — *and no delegation warning is
   shown*.
2. **A source that is not on the delegable list.** Warnings render **only** for formulas over delegable
   sources. A non-delegable source produces silence, not a triangle.

So the common review heuristic — *"the checker is clean, therefore delegation is fine"* — is unsound in
exactly the two cases where a maker is most likely to have worked around delegation.

**The reliable test the vendor names.** Set the data row limit to **1** during test: anything that cannot
be delegated returns a single record, which is trivial to spot. **The proof obligation is a row-limit-1
pass per screen, not a warning count.**

## 4. Delegable-operation behaviour by connector class · `decision-grade`

The delegable set is **a property of the source**, not of the language. The vendor names exactly **four**
delegable tabular sources: the governed relational store, the list store, the relational store via its
SQL connector, and one third-party CRM connector. **Anything not on that list is not delegable and
warrants no warning.**

Where the generic function list and a connector's own delegation table disagree, **the connector's table
governs** — the generic list is an upper bound only, and the baseline records the disagreement.

| Source class | Delegable set | Named non-delegable / throttled classes |
|---|---|---|
| **Governed relational store** (Dataverse) | **Broadest** of the four | Filters over **computed columns** (formula columns) are throttled; **leading-wildcard contains**; **sorts by choice or related columns** in grids. Text search is bounded to the store's searchable / quick-find column set. Aggregates are bounded by the store's aggregation ceiling. |
| **Relational store via connector** (SQL / Azure SQL) | **Partial** | **Text range comparisons** (`<`, `<=`, `>`, `>=` on text) · **blank tests** · **search over numeric columns** · **max/min over dates**. **Date predicates fail entirely through the on-premises gateway**; the documented workaround is an integer date key. Fixed-width character types carry documented pitfalls. |
| **List store** (SharePoint / Lists) | **Narrowest of the delegable sources** | **Negation never delegates.** The **ID column supports equality only**. **Blank test and sort do not delegate on text or complex columns.** **Person columns delegate only on email and display name.** **`StartsWith` does not delegate on choice or lookup subfields.** The vendor states the list store **does not support the count function**, so plain and conditional counting are **not delegated** — the client downloads the ceiling fragment and counts that. Compound `And`/`Or` over otherwise delegable predicates *does* delegate. |
| **Spreadsheet** (Excel) | Delegable function set is **limited enough that the vendor caps the load at the ceiling maximum** | The baseline's boundary statement treats the spreadsheet source as non-delegating for design purposes. The vendor states plainly that it *"isn't a relational database system"* and **declines to publish a transaction threshold** — so the decision is made on shape (read-mostly vs multi-writer), never on a volume number. |
| **In-memory collections** | **Never** | *"Collections are a static in-memory list of records and can't participate in delegation."* No warning is shown. |
| **Custom-connector paths** | **Not delegable at all** | An external source reached through a custom connector has no delegation. Every filter, sort, count and aggregate is client-side against the ceiling fragment. |
| **Virtual tables** | **Absent from the delegable-source list** | No vendor page states which operations delegate to a virtual table. The ceiling applies — **and because warnings render only for delegable sources, truncation can occur with no design-time signal at all.** Column selection is ignored (all attributes always return). A negative-filter query corrupts paging beyond the first page, with *no supported workaround*. This is a **NEGATIVE finding**: the absence of documentation is the finding, and it must be closed by measurement, not by inference. |

**Separate from delegation, and conflicted.** The **throughput ceiling** of the custom-connector
mechanism is `CONFLICTED` — two currently-maintained vendor pages disagree by a factor of twenty, and the
conflict was re-verified and remains open. **Neither figure is carried here.** Any option whose sizing or
economics rests on a high-frequency custom connector is **decision-blocked until measured**
(`VC-01` / `VS-08`, blocking entry `B-08`, composed row `CD-05`). **This cuts across the platform, the
cloud-native classes and the hybrid class equally — it is not a penalty against this platform.** Note
that the *delegation* answer for custom connectors is **not** conflicted: it is settled at none.

## 5. The client cache and paging boundary · `decision-grade`

- **The ceiling is the cache.** A non-delegable expression sees the fragment defined by the ceiling in §3,
  and nothing beyond it. Raising the ceiling to its maximum buys a bigger fragment, not delegation.
- **Galleries page in small increments by default.** The vendor's design target is a **small window per
  screen** — reached by a server-side view that pre-filters, plus **requiring search arguments in the UI
  before showing data**. The baseline's guidance is a shape, not a threshold: the default query for a
  gallery should return a small working set, not a table.
- **A cached count is a cached value.** On the governed relational store the **plain count function
  returns a periodically-recalculated table size, not a transactional count** — the store keeps the figure
  around so it need not scan the table on every call. It is stale by an unstated interval, and the
  staleness is invisible to the user. An **exact** count is available only via the conditional count
  function, and only up to the store's aggregation ceiling.

  > Documented reading (aggregation ceiling bounding the exact-count path) · read 2026-09-04
  > · re-verify: VS-06 (design time, before any reporting commitment)

  **Consequence:** never place a cached count next to a transactional list and imply that they agree. If
  an exact count is a requirement, either bound it below the aggregation ceiling with the conditional
  count, or maintain the count as a materialised column written by server logic.
- **Payload width is part of the read.** Explicit column selection is on by default for new apps, so the
  governed path fetches only the columns in use. The **list store does not behave this way**: matched rows
  are returned **with every column defined on the list, even those the app never reads**. Column count is
  therefore a read cost on the list store regardless of app design.
- **The list store carries a second ceiling, independent of delegation.**

  > Documented reading (list-store scale threshold used as the access-granularity boundary) · read
  > 2026-09-04 · re-verify: VS-04 (design time)
  >
  > **~5,000 items.** A query touching more than the threshold without an indexed, selective filter
  > fails; the vendor states that for the list store *"the LVT limit can't be changed"*. The per-list
  > item ceiling is orders of magnitude higher, so **the item ceiling is never the binding constraint —
  > the query shape is.** The baseline flags both figures as **search-derived in one pass** — verify
  > before encoding.

  **It is orthogonal to delegation**: a perfectly delegable query can still hit the threshold, and a
  small list can be non-delegable. Design consequences are in §10.

## 6. Delegation-safe is not fast — the two lever sets · `decision-grade`

**The vendor publishes limits, not benchmarks.** There is no empirical throughput or latency measurement
in the baseline for any component. **A design that violates no documented limit is not thereby known to
be fast; it is only known not to be structurally excluded.** Treat "within envelope" as *not excluded*,
never as *performs well*.

| Question | Levers |
|---|---|
| **Is the answer right?** (correctness) | Source is on the delegable list · every part of the expression is inside *that source's* delegable set · otherwise the read is **pre-shaped at the server** (view, stored procedure, server-side filter/select/expand) · row-limit-1 proof |
| **Is it fast enough?** (latency) | Fewer round trips · narrower payload · back-end query shape · client-side processing volume |

The two layers the vendor names as usually dominant are **the back end while processing the request** and
**the client while sending the request or manipulating received data** — not the connector hop. The
governed relational store is architecturally shorter than a connector-mediated source because it skips a
layer, which is the one comparative statement the vendor makes between sources; it is a statement about
path length, not about tuning.

**Tuning order, and it is fixed.** Because every meter counts **requests**:

1. **Don't make the call** — trigger conditions, deferred loading, caching the static.
2. **Make fewer, wider calls** — server-side views, joins, expand/select, batch fetching.
3. **Only then parallelism** — and re-check the connector's own throttle at the new setting.

Reducing calls is the only lever that improves every meter simultaneously; parallelism improves
wall-clock time while making several meters worse.

---

## 7. Failure modes · `decision-grade`

> **Non-delegable query over a table that will outgrow the client ceiling.** The client evaluates the
> whole expression against the first fragment and returns a plausible, silently truncated answer.
> Consequence: the wrongness is discovered by a business user reconciling a total, months after go-live.

> **Collect-everything-into-a-collection to escape a delegation warning.** The warning disappears because
> collections never delegate; the ceiling still applies to the *source read*, so the fragment is
> unchanged. Consequence: the same wrong answer, now with no design-time signal, plus payload and client
> memory cost.

> **Trusting the absence of a delegation warning.** Warnings render only for sources on the delegable
> list; a non-delegable source and an internally-created collection both produce silence. Consequence:
> warning count is not a gate — a row-limit-1 test per screen is.

> **A per-row lookup inside a gallery.** Each rendered row issues its own query, so an N-row list becomes
> N+1 requests. Consequence: the acting identity's request budget, not the store, becomes the ceiling — and
> the symptom surfaces as intermittent app slowness under load, not as a query problem.

> **A cached count presented as a live count.** The plain count function on the governed store returns a
> periodically-recalculated table size. Consequence: the KPI tile and the list beneath it disagree, and
> nothing in the UI explains why.

> **A free-text or negative-filter search box over a store that cannot delegate it.** Leading-wildcard
> contains and computed-column filters are throttled by the platform; negation never delegates on the list
> store; a negative filter over a virtual table corrupts paging past the first page with no supported
> workaround. Consequence: the search affordance must be redesigned or the store must change — it is not a
> tuning task.

## 8. What must be verified · `decision-grade`

- **The delegation ceiling — default and maximum — per data source** (`VS-02`, design time). Read it
  current; record it on the engagement's own row with its date.
- **The list-store threshold** (`VS-04`, design time), and the fact that both it and the per-list item
  ceiling are **search-derived** in the baseline.
- **Each connector's own delegable-operation table, at the decision date.** The connector table governs
  over the generic function list; the baseline records that the two disagree and treats the generic list
  as an upper bound only. Delegation support changes with platform releases.
- **The row-limit-1 delegation proof, per screen**, as the scale-readiness gate.
- **Which operations delegate to a virtual table** — no vendor page states it. Close by measurement
  against the actual provider, or do not build the path.
- **The custom-connector throughput ceiling** — `CONFLICTED` (`VC-01` / `VS-08`), decision-blocked until
  re-read from **both** current sources *and* measured against representative workload. Symmetric across
  option classes.
- **Whether vendor support creates indexes on request** on the governed relational store — **UNKNOWN** in
  the baseline. Do not plan an access path that depends on it.
- **Read-after-write visibility and connector-level isolation semantics** for the relational-store
  connector — undocumented; do not assert either way.
- **The freshness answer from the business** — *"how old may this figure be?"* — before any denormalised or
  replicated read model is designed. It is a requirement, not a technical parameter.

## 9. What not to infer · `decision-grade`

- **A capability absence is not a verdict.** *"The list store never delegates negation"* is domain
  knowledge. *"Therefore the list store is inappropriate"* is a **selection verdict** and belongs to
  `decision-tree.md`. There is no store ranking here and no `*-first` branch.
- **Delegation-safe does not mean fast**, and **non-delegable does not mean wrong at every volume** —
  below the default ceiling any source and any formula is correct. Both errors produce false verdicts.
- **A documented boundary here is not evidence that another option class performs better.** The baseline
  holds no like-for-like measurement against SaaS, pro-code, incumbent platforms or other low-code
  stacks; where the comparison is material, `decision-model/outcome-classes.md`'s comparator semantics
  stand.
- **Warning-free is not delegation-proof** (§3).
- **The client ceiling is not a store size limit**, and it is per query, not per app.
- **"It works in the demo data" proves nothing about delegation** — the demo data is inside the fragment.
- **Do not read a "no documented limit violated" verdict as a performance claim** (§6).
- **Formula patterns, workaround code, chunking and pagination recipes, validation sequences, trap
  catalogues and control-property references are delivery practice** — `craft/powerfx.md`, which is not an
  Options pull target. That file cites this one for the boundary; this file never cites it for a limit.

---

## 10. Access-path design consequences · `architecture-grade`

- **Prefilter at the server.** *"Use server-side views to prefilter data."* The vendor's own framing:
  *"most enterprise-grade apps make heavy use of views on the data source."* **One server-side view per
  screen is a first-class deliverable of the design, alongside the screen itself.**
- **Avoid the N+1 per-row lookup.** A lookup, filter or first-record call *inside* a gallery runs once per
  row: the vendor's worked example turns an N-row gallery into **N+1 network requests**. Every avoided
  per-row call is an avoided request against the acting identity's budget. Prefer an index-leveraging
  predicate over one that reads the whole table; whole-table membership operators belong to in-memory
  collections or genuinely small tables.
- **Cache the static, not the volatile.** Caching *"is most effective on static data or data that rarely
  changes"*, and where the underlying data changes frequently **a cache-invalidation mechanism is
  required**. Volatile or sensitive values — price, credit limit, balance — must be read from the primary
  source; a cache-aside pattern does not guarantee consistency.
- **Move the mashup to the server.** Views, and **deliberate denormalisation** where the freshness answer
  permits it. The vendor frames freshness explicitly as a **negotiable business requirement**: *"the key
  question is: how up to date must this data be?"* Ask it, record the answer, and let it decide whether a
  replicated local table is admissible. A duplicated-data design trades consistency for speed and must be
  an explicit, recorded decision.
- **Index the filter columns the access path actually uses — but who *can* index differs by store.**
  - **Governed relational store:** physical indexes are **platform-managed**. Automatic tuning and query
    optimisation are on by default, and query hints are to be applied *"only when recommended by
    Microsoft technical support"*. **A performance risk on a very large table cannot be mitigated by
    adding an index later.** The architect's levers are **schema** (alternate keys, keeping filter columns
    inside the documented maximum length for a filter column, the quick-find column set) and **query
    shape**; order on the primary key where possible. Whether vendor support will create an index on
    request is **UNKNOWN**.
  - **List store:** indexing the filter column is the admin action, and it is what keeps a selective query
    inside the list-view threshold (§5, and the list-store bullet below).
  - **Relational store via connector:** indexes belong to the database owner. The lever is the
    **canvas-facing schema** — views and stored procedures with pre-computed columns, integer date keys
    for the gateway path, no fixed-width character types, no binaries. Stored procedures are **un-paged
    actions with a static return schema**, not refreshable, and are re-invoked whenever the control
    refreshes: they solve delegation, trigger and security problems by **moving paging, filtering and
    refresh control to the maker**.
- **Relationship traversal in one expression is bounded.** There is a low single-digit cap on lookup
  levels in one query — **lower again offline** — and a bounded number of entities expandable in one
  query. A normalised model that reads naturally in a relational store can be **unreachable from the app
  surface**; the vendor's named remedy is a **server-side view**, which is a data-model change, not an app
  fix. An app that traverses correctly online can silently lose reach offline.
- **Query shapes the platform actively throttles.** The store *"heavily throttles queries that use known
  query anti-patterns"*: **leading-wildcard contains**, **filters over computed columns**, and **sorts by
  choice or related columns in grids**. Ordering on choice columns *"requires more compute"*; ordering by
  columns on related tables *"makes the query slower"*. The common origins the vendor names are **a saved
  query used in a grid**, **a query executed by a plug-in**, and **data integration moving a large amount
  of data**. Throttling is the platform's response to the shape — it is not tunable away from the app.
- **Designing around the list-view threshold** (the figure and its stamp are in §5). Every view, every
  app filter and every automation query over the list store must rest on an **indexed, selective filter**
  — that, not the item count, is what keeps the path inside the threshold. Two consequences that are easy
  to miss. First, **the same silent-truncation failure appears on the automation path**: the flow-side
  item retrieval has a low default page size, fails above the threshold without pagination, and **returns
  no records at all when the filter matches nothing inside the first threshold-sized window**. Second, a
  separate documented bound caps the number of join-type columns (lookup, person, workflow status) a
  single view or item-retrieval action can carry; above it the view and the flow fail outright. The
  vendor's own remedies at volume — denormalise people columns, partition the list and expose the
  partition key in the UI — are **functional constraints on the screen**, not tuning steps.

## 11. Consequences elsewhere · `architecture-grade`

- **→ `performance/performance-and-scale.md`.** The meters (requests, execution seconds, concurrency,
  connector throttles) and **the limit-vs-proof rule** live there: limits are published, benchmarks are
  not, and "violates no limit" is not "is fast". Every access-path decision taken here consumes those
  meters; the N+1 elimination in §10 is a meter decision as much as a latency one.
- **→ `data/store-boundaries.md`.** Query and access-path shape is one of the dimensions that decides a
  store. That file asks the dimension; this file answers it.
- **→ `data/sharepoint.md`.** The narrowest delegable set, the all-column read, the join-column bound and
  the list-view threshold are the list store's defining access-path facts.
- **→ `data/dataverse.md`.** Platform-managed indexing, the throttled query shapes, the searchable /
  quick-find column set, the cached count and the aggregation ceiling.
- **→ `data/azure-sql.md`.** The partial delegable set, the gateway date-predicate failure, and stored
  procedures as un-paged actions.
- **→ `automation/automation-mechanisms.md`.** The flow-side item retrieval reproduces the truncation
  failure on the automation path; trigger conditions and server-side filtering are the "don't make the
  call" lever.
- **→ `integration/integration-mechanisms.md`.** Custom-connector paths (no delegation; conflicted
  throughput) and the on-premises gateway envelope.
- **→ `/blueprint` — architecture-grade, not cosmetic.** List and search screen design is constrained
  here, not styled here. A screen's **filter set, sort set, search affordance, default working window and
  mandatory search arguments** are all determined by the store's delegable set and the access path's
  indexed columns. **Designing a free-text search box or a "not assigned to me" filter over a store that
  cannot delegate it produces a screen that is wrong, not slow.** The blueprint must therefore carry, per
  list surface: the delegable predicate set it relies on, the server-side view behind it, and the
  row-limit-1 proof obligation.
- **→ `craft/powerfx.md`** consumes this file's boundary and never restates it. It is not an Options pull
  target and may not state a platform limit.

