# delegation-matrix — Quick reference for delegable operations on Power Platform connectors

**Consumers**: `lens-technology` / `solution-architect` (Options & Decision phases) when assessing whether an architectural branch can serve the volumes and operations the Shared Understanding has anchored. The `claude-design-brief` deliverable embeds this matrix's conclusions inline so downstream Claude Design produces delegation-safe Power FX from the first draft.

**Companion**: this file is the at-a-glance reference; the full treatment (workarounds, validation sequence, traps) lives in `powerfx-patterns.md` (§§ 1–4).

---

## What delegation means

A delegable operation is processed **server-side** by the connector — the data source filters/sorts/aggregates and returns only the matching rows. A non-delegable operation is processed **client-side** in the Canvas App, limited to the cached set (default 500 rows, max 2000 via `Set(App.MaxAppCacheSize, 2000)` in `App.OnStart`).

When a non-delegable operation is applied to a table larger than the cache, the app silently returns wrong/incomplete results. **The matrix below is the load-bearing thing this pack protects against.**

---

## Dataverse connector

| Operation | Delegable | Notes |
|---|---|---|
| Filter on Choice column | Yes | |
| Filter on Text (equals) | Yes | |
| Filter on Text (StartsWith) | Yes | |
| Filter on Text (Contains) | Partial | Only on the primary name column |
| Filter on Number | Yes | |
| Filter on Date | Yes | |
| Filter on Lookup | Yes | If the FK column is indexed |
| Filter on Calculated column | No | Never delegable |
| Search() | Partial | Only on columns where `searchable = Yes` |
| Sum / Average / Max / Min(Table, Column) | Yes | |
| CountRows(Table) | Yes | |
| CountIf(Table, delegable cond) | Yes | The condition must itself be delegable |
| Sort on indexed column | Yes | |
| Sort on non-indexed column | Partial | Client-side; 500 limit |

## SharePoint connector

| Operation | Delegable | Notes |
|---|---|---|
| Filter on indexed column (equals) | Yes | Column **must** be indexed at the list level |
| Filter on non-indexed column | No | 500 limit |
| Sum / Average / Max / Min | **No** | Always non-delegable on SharePoint |
| CountRows | Yes | |
| CountIf with simple condition | Partial | Only on an indexed column |
| Search() | **No** | Never delegable on SharePoint |
| Sort on indexed column | Yes | |
| Sort on non-indexed column | No | 500 limit |

---

## Decision implications

Use this matrix during `lens-technology` / `solution-architect` work:

- **Large tables + aggregations (Sum/Average/Max/Min)** → SharePoint cannot deliver. Either move the entity to Dataverse, pre-aggregate via Power Automate into a denormalised SharePoint list (with a refresh schedule), or use chunked collection preload (§ 2.2 in powerfx-patterns).
- **Search() across the dataset** → SharePoint cannot deliver. Either move to Dataverse with `searchable = Yes` columns, or collect-then-Filter locally for ≤ 2000 records.
- **Filter on a non-indexed column** of a >2000-row list → either index the column (SharePoint admin action) or move the entity.
- **Calculated column filter** anywhere → never delegable; force the calculation into a stored column upstream.

When the Solution Architect's options analysis identifies a delegation cliff for an entity, the `Risky` SU row should name (a) the entity, (b) the operation, (c) the volume signal, and (d) the proposed mitigation (preload / index / move / aggregate-upstream).

---

## Workarounds at a glance

(Full code in `powerfx-patterns.md` § 2.)

1. **Collection preload** — `ClearCollect(col, Filter(source, delegable-cond))` in `OnStart` or `OnVisible`; then operate on `col` locally. The most common pattern. Limit: total returned must fit in cache (≤ 2000).
2. **Chunked loading** — for >2000 records, paginate via cursor; rarely worth the complexity if the entity can move to Dataverse instead.
3. **Server-side pre-filtering** — narrow the dataset with a delegable Filter first, then apply non-delegable operations on the narrower result. Works when the time/owner/status filter cuts the working set under 2000.
4. **Upstream pre-aggregation** — daily Power Automate flow produces a denormalised summary list that the app reads directly. Trades freshness for query speed.

---

## Maintenance note

When Microsoft adds or changes delegation support (semi-annual Power Platform releases), this matrix is the first file to update in the pack. The `pack_version` in `library/packs/pp/pack.yaml` should bump on every change here.
