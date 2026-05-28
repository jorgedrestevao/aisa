# azure-sql-reference — Azure SQL Complete Reference

**Source:** transplanted 2026-05-28 from the previous-aisa references (`ref-03-azure-sql.md`).
**Consulted by:** `lens-technology`, `solution-architect`, `implementation-spec` and `claude-design-brief` deliverable templates.
**Phase eligibility:** Options + Decision only.

Authoritative Azure SQL reference for the pp pack. Use when the chosen architecture is `azure-sql-first` (volume / financial precision / complex calculation drivers exceed Dataverse + SharePoint capabilities) or as the heavy-data side of a `hybrid` branch. Cross-reference with [`security-patterns.md`](security-patterns.md) for the RLS view example, [`flows-patterns.md`](flows-patterns.md) for SP orchestration via Power Automate, and [`dataverse-reference.md`](dataverse-reference.md) when comparing platform fit.

---

## DATA TYPES — Use Exactly These

| Category | SQL Type | Use When | Notes |
|---|---|---|---|
| Integer | INT | Counts, quantities, IDs | 2B limit |
| Integer | BIGINT | Large IDs, row counts >2B | |
| Decimal | DECIMAL(p,s) | Financial — ALWAYS specify p and s | NEVER use FLOAT for money |
| Float | FLOAT | Scientific/approximate only | |
| Text | NVARCHAR(n) | Variable text — always N prefix | Unicode required |
| Text | NVARCHAR(MAX) | Long text, JSON payloads | Max 2GB |
| Text | NCHAR(n) | Fixed-length codes | Country codes, product codes |
| Date | DATE | Date only | YYYY-MM-DD |
| DateTime | DATETIME2(7) | Timestamps | NEVER use DATETIME |
| Boolean | BIT | Flags | 0/1 |
| GUID | UNIQUEIDENTIFIER | External IDs, integration keys | |
| Binary | VARBINARY(MAX) | File content | |

**Financial precision standard:** `DECIMAL(18,4)` for monetary values.

---

## MANDATORY AUDIT COLUMNS — Every Table Without Exception

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

## MEDALLION ARCHITECTURE

### Bronze — Raw Ingestion Layer
- 1 table per data source identified during Discovery
- Data stored exactly as received — NO transformation
- Naming: `brz_[source]_[entity]` (e.g., `brz_api_quotes`, `brz_erp_stock`)
- Append-only: NEVER UPDATE or DELETE Bronze records
- All columns NULLABLE (raw data may be incomplete)

### Silver — Cleaned and Enriched Layer
- 1 table per business entity (not per source)
- Multiple Bronze tables may feed one Silver table
- Naming: `slv_[entity]` (e.g., `slv_quote`, `slv_product`)
- Transformations: dedup, type conversion, null handling, validation, enrichment
- Metadata: `processed_timestamp DATETIME2(7)`, `valid_flag BIT`
- NULLABLE where business allows, NOT NULL where business requires

### Gold — Business Logic and Output Layer
- 1 table per calculation result or output destination
- Naming: `gld_[purpose]` (e.g., `gld_pricing_model`, `gld_monthly_report`)
- Additional audit: `calculated_at DATETIME2(7)`, `calculated_by NVARCHAR(255)`, `approved_by NVARCHAR(255)`, `approved_at DATETIME2(7)`

### Reference Tables
- Naming: `ref_[entity]` (e.g., `ref_product`, `ref_region`, `ref_parameter`)
- Shared dimensions used across Bronze/Silver/Gold
- Version columns if slowly changing: `valid_from DATETIME2(7)`, `valid_to DATETIME2(7)`, `is_current BIT`

### Audit Tables (always include both)
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

## STORED PROCEDURE TEMPLATE — Always Use This Wrapper

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

## SP EXECUTION DAG

Document execution order as a DAG comment at the end of every SP file:

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

## VIEW DEFINITIONS

```sql
-- Canvas App consumption view
CREATE OR ALTER VIEW [dbo].[vw_app_[screen]]
AS
SELECT
 [col1] AS [DisplayName1], -- always use aliases readable by Power Apps
 [col2] AS [DisplayName2]
FROM [dbo].[slv_entity]
 LEFT JOIN [dbo].[ref_lookup] ON ...
WHERE [is_active] = 1;
GO

-- Power BI view
CREATE OR ALTER VIEW [dbo].[vw_pbi_[dashboard]]
AS
SELECT ... FROM [dbo].[gld_result] ...;
GO

-- Power Automate flow view
CREATE OR ALTER VIEW [dbo].[vw_flow_[output]]
AS
SELECT ... FROM [dbo].[gld_result] WHERE [status] = 'Ready';
GO
```

---

## ROW-LEVEL SECURITY

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

-- Step 4: Set context on every connection (in SP or Power Automate)
EXEC sp_set_session_context N'user_email', @current_user_email;
```

Role-specific column hiding via views: see [`security-patterns.md`](security-patterns.md) § Azure SQL RLS view.

---

## FINANCIAL FORMULA IMPLEMENTATIONS (T-SQL)

```sql
-- PMT (periodic payment)
-- pmt = pv * rate / (1 - POWER(1 + rate, -nper))
DECLARE @pmt DECIMAL(18,4) =
 CASE WHEN @rate = 0 THEN @pv / @nper
 ELSE @pv * @rate / (1 - POWER(1.0 + @rate, -@nper))
 END;

-- NPV (net present value) — iterative via cursor or JSON
-- For each cashflow at period t: pv += cashflow / POWER(1+rate, t)

-- IRR — Newton-Raphson iteration (implement in SP with WHILE loop, max 100 iterations)
-- Seed: irr_guess = 0.1 (10%)
-- Iterate: irr_new = irr_old - NPV(irr_old) / NPV_derivative(irr_old)
-- Stop when ABS(irr_new - irr_old) < 0.0001
```

---

## PERFORMANCE LIMITS AND GUIDELINES

| Limit | Value | Design Impact |
|---|---|---|
| Max row size | 8060 bytes | Avoid many NVARCHAR(MAX) columns |
| Max columns per table | 1024 | No practical limit for normal schemas |
| Max indexes per table | 999 | Keep under 20 for write performance |
| Recommended batch size | 1000-5000 rows | For bulk inserts in SPs |
| Max NVARCHAR(MAX) in index | Not indexable | Use computed column with hash |
| Azure SQL DTU limits | Varies by tier | Size tier for peak load + 30% buffer |

---

## CTE PATTERNS — Common Table Expressions

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

## MERGE STATEMENT — Upsert Pattern (Bronze → Silver)

MERGE is the standard pattern for syncing Bronze (raw) into Silver (clean). One statement handles insert, update, and optionally delete.

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
- Never use `WHEN NOT MATCHED BY SOURCE THEN DELETE` in production without explicit approval — risk of data loss
- Always wrap in TRY/CATCH + TRANSACTION (use SP template)
- Log rows affected: `SET @rows = @@ROWCOUNT` after MERGE

---

## TEMPORAL TABLES — Built-in History Tracking

Azure SQL temporal tables automatically track all changes. Alternative to manual SCD (valid_from/valid_to/is_current).

### When to use temporal tables
| Scenario | Manual SCD | Temporal Table |
|---|---|---|
| Need to query "value at date X" | Complex query with date ranges | Simple `FOR SYSTEM_TIME AS OF '2024-06-15'` |
| Audit requirement on all columns | Build audit_changes trigger | Automatic — no code needed |
| Compliance (track who changed what) | Manual change tracking | Automatic history |
| Only need current + previous value | Simpler with 2 columns | Overkill |
| History table needs custom indexes | Full control | Limited (auto-managed) |

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
-- Price on a specific date
SELECT [product_code], [unit_price]
FROM [dbo].[slv_product]
FOR SYSTEM_TIME AS OF '2024-06-15T00:00:00';

-- All changes between two dates
SELECT [product_code], [unit_price], [valid_from], [valid_to]
FROM [dbo].[slv_product]
FOR SYSTEM_TIME BETWEEN '2024-01-01' AND '2024-12-31'
ORDER BY [valid_from];
```

---

## INDEX STRATEGY

### Clustered index
- Always on PK (INT IDENTITY) — already created by PRIMARY KEY constraint
- Never change clustered index column after table is populated — full table rebuild
- For time-series data: consider `([created_at] ASC, [id] ASC)` as clustered if most queries are date-range

### Non-clustered indexes — priority order
1. **FK columns** (every foreign key gets an index — critical for JOIN performance)
2. **Filter columns** (WHERE clause targets: status, date, owner)
3. **Sort columns** (ORDER BY targets for large result sets)
4. **Covering indexes** (INCLUDE frequently selected columns to avoid table lookups)

### Covering index example
```sql
-- Query: SELECT name, total FROM slv_quotes WHERE status = 'Active' ORDER BY created_at DESC
-- Without covering: index seek on status → key lookup for name, total (expensive at scale)
-- With covering: index seek only — all data in the index

CREATE NONCLUSTERED INDEX [IX_slv_quotes_status_covering]
ON [dbo].[slv_quotes] ([status] ASC, [created_at] DESC)
INCLUDE ([name], [total_value], [customer_id]);
```

### Index maintenance
```sql
-- Rebuild fragmented indexes (run weekly, off-hours)
ALTER INDEX ALL ON [dbo].[slv_quotes] REBUILD WITH (ONLINE = ON);

-- Update statistics (run after large data loads)
UPDATE STATISTICS [dbo].[slv_quotes];
```

### Anti-patterns

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Index on every column | Write performance degrades, storage explodes | Index only columns used in WHERE, JOIN, ORDER BY |
| Index on BIT column | Cardinality too low — optimizer ignores it | Composite index: (bit_col, date_col) if both used in WHERE |
| No indexes on FK columns | JOINs do full table scans | Always index FK columns |
| Never rebuilding indexes | Fragmentation >30% degrades read performance | Schedule weekly rebuild |

---

## POWER AUTOMATE — SQL SERVER CONNECTOR

### Connection configuration
```
Connection name: [SolutionCode]_AzureSQL
Server: [server].database.windows.net
Database: [database_name]
Authentication: SQL Server Authentication or Azure AD
Username: [service_account] ← never personal accounts
```

### Common actions

| Action | Use | Notes |
|---|---|---|
| Execute a SQL query | SELECT statements, simple reads | Max 2048 chars query length |
| Execute stored procedure | All write operations, complex logic | Preferred over inline SQL |
| Get rows | Simple filtered reads | OData-style, good for small result sets |
| Insert row | Single record insert | Simple cases only |

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
WARNING: must be the FIRST action in every flow that reads/writes SQL data with RLS enabled. Context is per-connection, resets after each action.

### Pagination for large result sets
SQL connector returns max 2048 rows per query. For larger datasets:
```
Action: Execute a SQL query
 Query: SELECT * FROM [dbo].[slv_orders]
 ORDER BY [id]
 OFFSET @{variables('offset')} ROWS
 FETCH NEXT 2000 ROWS ONLY
```
Loop with Do Until: increment offset by 2000, stop when result count < 2000.

---

## RESERVED WORDS (T-SQL)

The standard T-SQL reserved-word list applies — common collisions to avoid as identifiers:
`USER, ORDER, GROUP, SCHEMA, KEY, INDEX, TABLE, VIEW, COLUMN, ROW, ROWS, SELECT, FROM, WHERE, INSERT, UPDATE, DELETE, MERGE, JOIN, WHEN, CASE, END, BEGIN, COMMIT, ROLLBACK, TRANSACTION, AUTHORIZATION, GRANT, REVOKE, DENY, LEFT, RIGHT, FULL, INNER, OUTER, CROSS, ALL, ANY, SOME, AS, ON, IS, NULL, NOT, AND, OR, BETWEEN, LIKE, EXISTS, IN, UNION, INTERSECT, EXCEPT, PROC, PROCEDURE, FUNCTION, TRIGGER, ALTER, CREATE, DROP, TRUNCATE`.

When a collision is unavoidable, square-bracket-quote the identifier (`[user]`, `[order]`) — but rename rather than rely on quoting, because Power Apps / Power BI bindings may not preserve the brackets.
