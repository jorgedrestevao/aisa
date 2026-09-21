# SQL Delivery Conventions (Azure SQL build standard)

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

**Platform facts are not owned here.** Service tiers and their capacities, connector request and result
limits, throttling behaviour, gateway requirements and anything version-dependent belong to
`data/azure-sql.md` (with `integration/integration-mechanisms.md` for the connector path and
`data/query-and-delegation.md` for query behaviour from the app layer). What follows is how this team builds
against Azure SQL once it is the chosen store: layering, naming, audit, procedure structure, query patterns
and index hygiene.

Cross-references: [`security-craft.md`](security-craft.md) for role-specific views,
[`flow-craft.md`](flow-craft.md) for stored-procedure orchestration.

**O que um «always» significa neste ficheiro.** Convenção da equipa, não limite de plataforma: cada uma é
uma **proposta explícita e substituível**, e existe porque uma propriedade técnica a justifica — a razão
está ao lado da regra. Um engagement pode adoptar outra convenção; a que adoptar fica registada com a sua
razão. Nenhuma delas é obrigação de governance, nenhuma depende de alguém a aprovar, e nenhuma se aplica
onde a propriedade técnica que a justifica não existe.


---

## 1 — Data types: use exactly these

| Category | SQL type | Use when | Notes |
|---|---|---|---|
| Integer | INT | Counts, quantities, IDs | Default integer choice |
| Integer | BIGINT | Large IDs and row counts | Use when INT range is a real risk |
| Decimal | DECIMAL(p,s) | Financial — ALWAYS specify p and s | NEVER use FLOAT for money |
| Float | FLOAT | Scientific/approximate only | |
| Text | NVARCHAR(n) | Variable text — always the N prefix | Unicode required |
| Text | NVARCHAR(MAX) | Long text, JSON payloads | Keep them few and off the hot path |
| Text | NCHAR(n) | Fixed-length codes | Country codes, product codes |
| Date | DATE | Date only | YYYY-MM-DD |
| DateTime | DATETIME2(7) | Timestamps | NEVER use DATETIME |
| Boolean | BIT | Flags | 0/1 |
| GUID | UNIQUEIDENTIFIER | External IDs, integration keys | |
| Binary | VARBINARY(MAX) | File content | Prefer a document store for real files |

**Financial precision standard:** `DECIMAL(18,4)` for monetary values. This is a team standard, applied for
consistency across engagements; type ranges and storage limits themselves are in `data/azure-sql.md`.

---

## 2 — Row-provenance columns — the team's default shape for a table

These four columns are **provenance**, not a compliance audit trail: they say when a row appeared and when
it last changed, which is what incremental loads, change detection and debugging read. Convenção da equipa, não limite de plataforma: é uma **proposta explícita e substituível** — o engagement pode adoptar outra, e a que adoptar fica registada com a sua razão.
The technical reason is the one above; where a target has none of those needs for a given table, the columns
come off with that stated.

A **compliance** audit trail is a different object with a different trigger — an audit requirement covering
the entity, with its retention and its mechanism (`craft/security-craft.md` § audit patterns,
`security/security-controls.md`). Provenance columns do not satisfy it, and it does not replace them.

```sql
[id] INT IDENTITY(1,1) NOT NULL,
[created_at] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME,
[created_by] NVARCHAR(255) NOT NULL,
[modified_at] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME,
[modified_by] NVARCHAR(255) NOT NULL,
CONSTRAINT [PK_[table]] PRIMARY KEY CLUSTERED ([id] ASC)
```

**Bronze additional columns (append-only layer):**
```sql
[ingestion_timestamp] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME,
[source_identifier] NVARCHAR(500) NOT NULL,
[is_processed] BIT NOT NULL DEFAULT 0,
```

---

## 3 — Medallion layering

### Bronze — raw ingestion layer
- 1 table per data source identified during Discovery
- Data stored exactly as received — NO transformation
- Naming: `brz_[source]_[entity]` (e.g. `brz_api_quotes`, `brz_erp_stock`)
- Append-only: NEVER UPDATE or DELETE Bronze records
- All columns NULLABLE (raw data may be incomplete)

### Silver — cleaned and enriched layer
- 1 table per business entity (not per source)
- Multiple Bronze tables may feed one Silver table
- Naming: `slv_[entity]` (e.g. `slv_quote`, `slv_product`)
- Transformations: dedup, type conversion, null handling, validation, enrichment
- Metadata: `processed_timestamp DATETIME2(7)`, `valid_flag BIT`
- NULLABLE where the business allows, NOT NULL where the business requires

### Gold — business logic and output layer
- 1 table per calculation result or output destination
- Naming: `gld_[purpose]` (e.g. `gld_pricing_model`, `gld_monthly_report`)
- Additional audit: `calculated_at DATETIME2(7)`, `calculated_by NVARCHAR(255)`,
  `approved_by NVARCHAR(255)`, `approved_at DATETIME2(7)`

### Reference tables
- Naming: `ref_[entity]` (e.g. `ref_product`, `ref_region`, `ref_parameter`)
- Shared dimensions used across Bronze/Silver/Gold
- Version columns if slowly changing: `valid_from DATETIME2(7)`, `valid_to DATETIME2(7)`, `is_current BIT`

### Execution-telemetry tables — where the target needs diagnosis and recovery

These two tables are the **diagnostic interface** of the SQL side: what ran, when, with what outcome, and
what a recovery has to redo. They are engaged where the architecture owes an operating model with
diagnosis and recovery interfaces (`architecture-templates/architecture-core.md` A10) — which is the normal
case for scheduled or asynchronous work, and not the case for a store nothing runs against. Convenção da equipa, não limite de plataforma: é uma **proposta explícita e substituível** — o engagement pode adoptar outra, e a que adoptar fica registada com a sua razão.
```sql
CREATE TABLE [dbo].[audit_executions] (
 [id] INT IDENTITY(1,1) NOT NULL,
 [sp_name] NVARCHAR(255) NOT NULL,
 [status] NVARCHAR(50) NOT NULL, -- SUCCESS, ERROR, PARTIAL
 [rows_affected] INT NULL,
 [duration_ms] INT NULL,
 [error_message] NVARCHAR(MAX) NULL,
 [parameters] NVARCHAR(MAX) NULL, -- JSON of input params
 [executed_at] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME,
 [executed_by] NVARCHAR(255) NOT NULL DEFAULT SYSTEM_USER,
 CONSTRAINT [PK_audit_executions] PRIMARY KEY CLUSTERED ([id] ASC)
);

CREATE TABLE [dbo].[audit_changes] (
 [id] INT IDENTITY(1,1) NOT NULL,
 [table_name] NVARCHAR(255) NOT NULL,
 [record_id] INT NOT NULL,
 [column_name] NVARCHAR(255) NOT NULL,
 [old_value] NVARCHAR(MAX) NULL,
 [new_value] NVARCHAR(MAX) NULL,
 [changed_at] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME,
 [changed_by] NVARCHAR(255) NOT NULL,
 CONSTRAINT [PK_audit_changes] PRIMARY KEY CLUSTERED ([id] ASC)
);
```

---

## 4 — Stored procedure template — always use this wrapper

```sql
CREATE OR ALTER PROCEDURE [dbo].[sp_[verb]_[what]]
 @param1 NVARCHAR(255),
 @param2 INT = NULL -- optional params have defaults
AS
BEGIN
 SET NOCOUNT ON;
 DECLARE @start_time DATETIME2(7) = SYSUTCDATETIME;
 DECLARE @rows INT = 0;

 BEGIN TRY
 BEGIN TRANSACTION;

 -- ── BUSINESS LOGIC HERE ──────────────────────────
 -- Step 1: [description]
 -- ...
 -- Step N: [description]
 -- ─────────────────────────────────────────────────

 SET @rows = @@ROWCOUNT;
 COMMIT TRANSACTION;

 INSERT INTO [dbo].[audit_executions]
 ([sp_name], [status], [rows_affected], [duration_ms], [parameters], [executed_at], [executed_by])
 VALUES (
 OBJECT_NAME(@@PROCID), 'SUCCESS', @rows,
 DATEDIFF(MILLISECOND, @start_time, SYSUTCDATETIME),
 JSON_OBJECT('param1': @param1, 'param2': @param2),
 SYSUTCDATETIME, SYSTEM_USER
 );

 END TRY
 BEGIN CATCH
 IF @@TRANCOUNT > 0 ROLLBACK TRANSACTION;

 INSERT INTO [dbo].[audit_executions]
 ([sp_name], [status], [error_message], [duration_ms], [executed_at], [executed_by])
 VALUES (
 OBJECT_NAME(@@PROCID), 'ERROR', ERROR_MESSAGE,
 DATEDIFF(MILLISECOND, @start_time, SYSUTCDATETIME),
 SYSUTCDATETIME, SYSTEM_USER
 );

 THROW;
 END CATCH
END;
GO
```

**SP naming convention:**
- `sp_ingest_[source]` — Bronze → Silver transformation
- `sp_calculate_[what]` — Silver → Gold business calculation
- `sp_generate_[output]` — Gold → output format/delivery
- `sp_validate_[what]` — validation rules before processing

---

## 5 — SP execution DAG

Document the execution order as a DAG comment at the end of every SP file:

```sql
-- ============================================================
-- EXECUTION ORDER (DAG)
-- ============================================================
-- sp_ingest_erp_quotes ← no dependencies, run first
-- sp_ingest_api_prices ← no dependencies, parallel with above
-- └─ sp_calculate_margin ← depends on both ingests
-- └─ sp_generate_report ← depends on calculate, run last
--
-- Parallel groups (can run simultaneously):
-- Group A: sp_ingest_erp_quotes, sp_ingest_api_prices
-- Group B (after A): sp_calculate_margin
-- Group C (after B): sp_generate_report
-- ============================================================
```

---

## 6 — View conventions

One view per consumer. Consumers bind to views, never to base tables.

```sql
-- App consumption view
CREATE OR ALTER VIEW [dbo].[vw_app_[screen]]
AS
SELECT
 [col1] AS [DisplayName1], -- always alias to names the app layer can bind readably
 [col2] AS [DisplayName2]
FROM [dbo].[slv_entity]
 LEFT JOIN [dbo].[ref_lookup] ON ...
WHERE [is_active] = 1;
GO

-- Reporting view
CREATE OR ALTER VIEW [dbo].[vw_pbi_[dashboard]]
AS
SELECT ... FROM [dbo].[gld_result] ...;
GO

-- Flow view
CREATE OR ALTER VIEW [dbo].[vw_flow_[output]]
AS
SELECT ... FROM [dbo].[gld_result] WHERE [status] = 'Ready';
GO
```

Role-specific column hiding via views: [`security-craft.md`](security-craft.md) § Artifact formats.

---

## 7 — Row-level security scaffold

```sql
-- Step 1: User role mapping table
CREATE TABLE [security].[user_roles] (
 [id] INT IDENTITY(1,1) NOT NULL,
 [user_email] NVARCHAR(255) NOT NULL,
 [role_name] NVARCHAR(100) NOT NULL,
 [business_unit] NVARCHAR(100) NULL,
 CONSTRAINT [PK_user_roles] PRIMARY KEY ([id]),
 CONSTRAINT [UQ_user_roles_email] UNIQUE ([user_email])
);

-- Step 2: Filter function
CREATE OR ALTER FUNCTION [security].[fn_access_filter](@owner NVARCHAR(255), @bu NVARCHAR(100))
RETURNS TABLE WITH SCHEMABINDING AS RETURN
 SELECT 1 AS [fn_result]
 WHERE EXISTS (
 SELECT 1 FROM [security].[user_roles]
 WHERE [user_email] = CAST(SESSION_CONTEXT(N'user_email') AS NVARCHAR(255))
 AND (
 [role_name] IN ('Admin', 'Finance')
 OR ([role_name] = 'Manager' AND [business_unit] = @bu)
 OR ([role_name] = 'Comercial' AND @owner = [user_email])
 )
 );

-- Step 3: Apply policy
CREATE SECURITY POLICY [security].[AccessPolicy]
 ADD FILTER PREDICATE [security].[fn_access_filter]([cr_ownerid], [cr_business_unit])
 ON [dbo].[slv_quote]
 WITH (STATE = ON);

-- Step 4: Set context on every connection (in the SP or in the flow)
EXEC sp_set_session_context N'user_email', @current_user_email;
```

Whether this composes with app-layer and store-layer controls, and what it does and does not cover, is owned
by `security/security-controls.md`.

---

## 8 — Financial formula implementations (T-SQL)

```sql
-- PMT (periodic payment)
-- pmt = pv * rate / (1 - POWER(1 + rate, -nper))
DECLARE @pmt DECIMAL(18,4) =
 CASE WHEN @rate = 0 THEN @pv / @nper
 ELSE @pv * @rate / (1 - POWER(1.0 + @rate, -@nper))
 END;

-- NPV (net present value) — iterate the cashflows
-- For each cashflow at period t: pv += cashflow / POWER(1+rate, t)

-- IRR — Newton-Raphson iteration in a WHILE loop
-- Seed: irr_guess = 0.1
-- Iterate: irr_new = irr_old - NPV(irr_old) / NPV_derivative(irr_old)
-- Stop on convergence tolerance or the iteration cap, whichever comes first
```

The seed, tolerance and iteration cap are choices of this implementation. Excel-side equivalents and the
Power Fx gap: [`excel-translation.md`](excel-translation.md) § FINANCIAL.

---

## 9 — Batch and volume conventions

Team conventions for write-heavy work. None of these is a platform capacity statement — for capacity, tier
behaviour and connector limits read `data/azure-sql.md` and `integration/integration-mechanisms.md`.

- Bulk inserts inside stored procedures run in batches of roughly 1000–5000 rows, and the batch loop is
  written to be resumable.
- Keep `NVARCHAR(MAX)` columns off tables that are scanned frequently; move long text to a side table where
  the read pattern justifies it.
- Where a long text or binary column must be searchable, index a computed hash rather than the column.
- Size the environment against measured peak load, not against a remembered tier figure — and record the
  measurement in the spec.

---

## 10 — CTE patterns

Use CTEs for multi-step queries instead of nested subqueries. Easier to read, debug, and maintain.

### Pattern 1 — Step-by-step calculation
```sql
-- Calculate weighted average price per category
WITH cte_totals AS (
 SELECT
 [category_id],
 SUM([quantity] * [unit_price]) AS [weighted_sum],
 SUM([quantity]) AS [total_qty]
 FROM [dbo].[slv_orderlines]
 WHERE [is_active] = 1
 GROUP BY [category_id]
),
cte_averages AS (
 SELECT
 [category_id],
 CASE WHEN [total_qty] > 0
 THEN [weighted_sum] / [total_qty]
 ELSE 0
 END AS [weighted_avg_price]
 FROM cte_totals
)
SELECT
 r.[name] AS [category_name],
 a.[weighted_avg_price]
FROM cte_averages a
 INNER JOIN [dbo].[ref_category] r ON r.[id] = a.[category_id]
ORDER BY a.[weighted_avg_price] DESC;
```

### Pattern 2 — Running totals (window function)
```sql
-- Running balance per account, ordered by date
SELECT
 [account_id],
 [transaction_date],
 [amount],
 SUM([amount]) OVER (
 PARTITION BY [account_id]
 ORDER BY [transaction_date]
 ROWS UNBOUNDED PRECEDING
 ) AS [running_balance]
FROM [dbo].[slv_transactions]
ORDER BY [account_id], [transaction_date];
```

### Pattern 3 — Ranking / Top N per group
```sql
-- Top 3 products per category by revenue
WITH cte_ranked AS (
 SELECT
 [category_id],
 [product_id],
 SUM([line_total]) AS [revenue],
 ROW_NUMBER OVER (
 PARTITION BY [category_id]
 ORDER BY SUM([line_total]) DESC
 ) AS [rank]
 FROM [dbo].[slv_orderlines]
 GROUP BY [category_id], [product_id]
)
SELECT * FROM cte_ranked WHERE [rank] <= 3;
```

---

## 11 — MERGE — upsert pattern (Bronze → Silver)

MERGE is the standard pattern for syncing Bronze (raw) into Silver (clean). One statement handles insert,
update, and optionally delete.

```sql
MERGE [dbo].[slv_product] AS target
USING (
 SELECT
 [product_code],
 [name],
 CAST([unit_price] AS DECIMAL(18,4)) AS [unit_price],
 [category]
 FROM [dbo].[brz_erp_products]
 WHERE [is_processed] = 0
) AS source
ON target.[product_code] = source.[product_code]

WHEN MATCHED AND (
 target.[name] <> source.[name]
 OR target.[unit_price] <> source.[unit_price]
) THEN UPDATE SET
 target.[name] = source.[name],
 target.[unit_price] = source.[unit_price],
 target.[modified_at] = SYSUTCDATETIME,
 target.[modified_by] = SYSTEM_USER

WHEN NOT MATCHED BY TARGET THEN INSERT
 ([product_code], [name], [unit_price], [category], [created_by], [modified_by])
 VALUES
 (source.[product_code], source.[name], source.[unit_price], source.[category],
 SYSTEM_USER, SYSTEM_USER);

-- Mark source as processed
UPDATE [dbo].[brz_erp_products] SET [is_processed] = 1
WHERE [is_processed] = 0;
```

**MERGE rules:**
- Always include the `WHEN MATCHED AND (change detection)` clause — avoid unnecessary updates
- Never use `WHEN NOT MATCHED BY SOURCE THEN DELETE` in production without explicit approval — risk of data
  loss
- Always wrap in TRY/CATCH + TRANSACTION (use the SP template)
- Log rows affected: `SET @rows = @@ROWCOUNT` after the MERGE

---

## 12 — Temporal tables — built-in history tracking

An alternative to manual SCD columns (`valid_from` / `valid_to` / `is_current`).

### When to use which

| Scenario | Manual SCD | Temporal table |
|---|---|---|
| Need "value at date X" | Complex query with date ranges | `FOR SYSTEM_TIME AS OF '2024-06-15'` |
| Audit requirement on all columns | Build an audit_changes trigger | System-managed history |
| Compliance (track who changed what) | Manual change tracking | System-managed history |
| Only need current + previous value | Simpler with 2 columns | Heavier than needed |
| History table needs custom indexes | Full control | Auto-managed, less control |

### Create temporal table
```sql
CREATE TABLE [dbo].[slv_product] (
 [id] INT IDENTITY(1,1) NOT NULL,
 [product_code] NVARCHAR(50) NOT NULL,
 [name] NVARCHAR(255) NOT NULL,
 [unit_price] DECIMAL(18,4) NOT NULL,
 [created_at] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME,
 [modified_at] DATETIME2(7) NOT NULL DEFAULT SYSUTCDATETIME,
 -- Temporal columns (system-managed)
 [valid_from] DATETIME2(7) GENERATED ALWAYS AS ROW START NOT NULL,
 [valid_to] DATETIME2(7) GENERATED ALWAYS AS ROW END NOT NULL,
 PERIOD FOR SYSTEM_TIME ([valid_from], [valid_to]),
 CONSTRAINT [PK_slv_product] PRIMARY KEY CLUSTERED ([id])
) WITH (SYSTEM_VERSIONING = ON (HISTORY_TABLE = [dbo].[slv_product_history]));
```

### Query historical data
```sql
-- Value on a specific date
SELECT [product_code], [unit_price]
FROM [dbo].[slv_product]
FOR SYSTEM_TIME AS OF '2024-06-15T00:00:00';

-- All changes between two dates
SELECT [product_code], [unit_price], [valid_from], [valid_to]
FROM [dbo].[slv_product]
FOR SYSTEM_TIME BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY [valid_from];
```

History retention and its storage consequence are an engagement decision — record it in the spec.

---

## 13 — Index strategy

### Clustered index
- Always on the PK (INT IDENTITY) — created by the PRIMARY KEY constraint
- Never change the clustered index column after the table is populated — full rebuild
- For time-series data: consider `([created_at] ASC, [id] ASC)` as clustered if most queries are date-range

### Non-clustered indexes — priority order
1. **FK columns** (every foreign key gets an index — critical for JOIN performance)
2. **Filter columns** (WHERE targets: status, date, owner)
3. **Sort columns** (ORDER BY targets for large result sets)
4. **Covering indexes** (INCLUDE frequently selected columns to avoid lookups)

### Covering index example
```sql
-- Query: SELECT name, total FROM slv_quotes WHERE status = 'Active' ORDER BY created_at DESC
-- Without covering: index seek on status → key lookup for name, total
-- With covering: index seek only — all data in the index

CREATE NONCLUSTERED INDEX [IX_slv_quotes_status_covering]
ON [dbo].[slv_quotes] ([status] ASC, [created_at] DESC)
INCLUDE ([name], [total_value], [customer_id]);
```

### Index maintenance
```sql
-- Rebuild fragmented indexes (scheduled, off-hours)
ALTER INDEX ALL ON [dbo].[slv_quotes] REBUILD WITH (ONLINE = ON);

-- Update statistics (run after large data loads)
UPDATE STATISTICS [dbo].[slv_quotes];
```

Maintenance is scheduled work with an owner — put it in the operations handover, not in tribal memory
(`delivery-conventions.md` §6).

### Index anti-patterns

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Index on every column | Write performance degrades, storage grows | Index only columns used in WHERE, JOIN, ORDER BY |
| Index on a lone BIT column | Cardinality too low to help the optimizer | Composite index: (bit_col, date_col) if both are in the predicate |
| No index on FK columns | JOINs scan | Always index FK columns |
| Never rebuilding indexes | Fragmentation accumulates and reads degrade | Scheduled rebuild + statistics refresh |
| Keeping the index count low by dropping useful ones | Reads regress instead | Measure before and after; keep the write cost visible in the spec |

---

## 14 — SQL connector conventions (from Power Automate)

### Connection configuration
```
Connection name: [SolutionCode]_AzureSQL
Server: [server].database.windows.net
Database: [database_name]
Authentication: [as the environment's security standard requires]
Account: [service account] ← never a personal account
```

### Action choice

| Action | Use | Notes |
|---|---|---|
| Execute stored procedure | All write operations and complex logic | Preferred — the logic stays versioned in the database |
| Execute a SQL query | Simple reads | Inline SQL in a flow is unversioned; keep it short-lived |
| Get rows | Simple filtered reads | Small result sets |
| Insert row | Single-record insert | Simple cases only |

Query-length and result-size limits of the connector are owned by `data/azure-sql.md` /
`integration/integration-mechanisms.md`. Design to a *page size read from the owner*, never to a figure
copied from a pattern.

### Execute stored procedure pattern
```
Action: Execute stored procedure (V2)
 Server: [connection]
 Database: [database]
 Procedure: sp_calculate_margin
 Parameters:
 @period: formatDateTime(utcNow, 'yyyy-MM')
 @user_email: triggerBody?['user_email']
```

### Set session context (for RLS)
```
Action: Execute a SQL query
 Query: EXEC sp_set_session_context N'user_email', '@{triggerBody?['user_email']}'
```
**Ordering rule:** this must be the FIRST action in every flow that reads or writes RLS-protected data.
Session context is per-connection and does not persist across actions — re-set it wherever the connection
may have been recycled, and treat a missing context as a hard failure rather than an empty result set.

### Pagination for large result sets
```
Action: Execute a SQL query
 Query: SELECT * FROM [dbo].[slv_orders]
 ORDER BY [id]
 OFFSET @{variables('offset')} ROWS
 FETCH NEXT @{variables('page_size')} ROWS ONLY
```
Loop with Do Until: increment `offset` by `page_size`, stop when the returned count is less than
`page_size`. Set `page_size` from the connector's documented result limit (owner above), keep it in one
variable, and always ORDER BY a stable key — paging an unordered result silently skips and repeats rows.

---

## 15 — Reserved words

The standard T-SQL reserved-word list applies — common collisions to avoid as identifiers:
`USER, ORDER, GROUP, SCHEMA, KEY, INDEX, TABLE, VIEW, COLUMN, ROW, ROWS, SELECT, FROM, WHERE, INSERT,
UPDATE, DELETE, MERGE, JOIN, WHEN, CASE, END, BEGIN, COMMIT, ROLLBACK, TRANSACTION, AUTHORIZATION, GRANT,
REVOKE, DENY, LEFT, RIGHT, FULL, INNER, OUTER, CROSS, ALL, ANY, SOME, AS, ON, IS, NULL, NOT, AND, OR,
BETWEEN, LIKE, EXISTS, IN, UNION, INTERSECT, EXCEPT, PROC, PROCEDURE, FUNCTION, TRIGGER, ALTER, CREATE,
DROP, TRUNCATE`.

When a collision is unavoidable, square-bracket-quote the identifier (`[user]`, `[order]`) — but rename
rather than rely on quoting, because downstream bindings may not preserve the brackets.
