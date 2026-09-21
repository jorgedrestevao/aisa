Research Status: VALIDATED
Research Confidence: HIGH
Gate: PASS

# Data Architecture — Canonical Research Evidence

Research area: **03 — Data Architecture** (`../research-areas.md`).
Canonical version: **2026-09-02**, consolidated from `data-architecture-research-v2.md` (primary) after the Research Gate verdict **PASS / HIGH confidence**. Lineage: v1 draft (`data-architecture.md`, superseded — its content is now this file's history, not a separate surviving file) → adversarial review (`data-architecture-review.md`, verdict NEEDS MORE RESEARCH on 5 HIGH-severity gaps) → v2 targeted revision (five additional sub-researches: virtual tables at volume + Fabric consumption `VT`; Dataverse→SQL replication paths + reconciliation `SY`; Azure SQL store-choice evidence `SQ2`; business-volume→platform-budget + concurrency + consistency `SC`; data quality/ownership vocabulary `DQ`) → Research Gate (PASS). v1's 61 `DA-nn` findings, the store-fit matrix, decision boundaries, anti-patterns and alternatives are carried forward **with corrections** where the review or the v2 research contradicted them; the 90 new findings are held under their own prefixes (`VT-nn`, `SY-nn`, `SQ2-nn`, `SC-nn`, `DQ-nn`) the same way this file already cross-references `PS-nn` (`platform-suitability.md`) and `AA-nn` (`application-architecture.md`).
Source policy: `../source-policy.md`. Quotes are verbatim English. Prices are USD list.

**Purpose.** Answer, with traceable evidence: *"Given these data requirements, which data architecture should aisa consider for a Power Platform solution — Dataverse, SQL/Azure SQL, SharePoint/Lists, an external system of record left in place, or a hybrid — and which requirement changes the answer?"* This is NOT a generic Dataverse vs SQL vs SharePoint comparison. Every finding starts from a data requirement and derives the constraint and the architectural implication.

**Corrections applied in v2 (see "Gaps Fixed" at the end for detail):**
1. Five store-fit-matrix cells that v1 asserted without any source (§2, review F-01) are now sourced, corrected, or downgraded. Net effect: Azure SQL is **not** STRONG for cheap long-term archival (CONTRADICTED — `SQ2-04`, `SQ2-05`) or for high-ingest telemetry (CONTRADICTED — `SQ2-06`); it **is** supportable for customer-managed keys (`SQ2-01`/`SQ2-09`, with real operational cost); SharePoint/M365 CMK support was **wrong** in v1 — Customer Key does cover SharePoint (`SQ2-10`).
2. The "environment is a hard data boundary / no cross-environment queries" claim (v1 DA-25, review F-02) is corrected: cross-environment **reads** are supported for canvas apps by explicit environment selection; cross-environment **relationships/joins** are not. See `DA-25` (revised) below.
3. Virtual-table viability at volume (review F-03) is now characterised: 17 new findings (`VT-01`..`VT-17`), including the explicit negative finding that Microsoft publishes no virtual-table performance/latency/throughput characterisation at all (`VT-09`), and that Fabric-sourced virtual tables are read-only (`VT-12`) with no write-back path anywhere in Link to Fabric or Synapse Link (`VT-13`).
4. The Dataverse→Azure SQL replication path (review F-04) is now resolved: there is **no first-party Dataverse→Azure SQL Database service** (`SY-01`, a hard negative finding checked against the Fabric Mirroring source list). Three real paths and their reconciliation cost are documented (`SY-18`).
5. Write amplification / business-volume-to-request-budget translation (review F-05) is now structured (`SC-21`): the counting rules are quoted, and every multiplier is explicitly marked as an engagement-measured input, never a published figure.
6. The 50,000-row limit (review F-06) is now scoped precisely per surface (aggregate queries vs charts vs reports) rather than stated as one flat ceiling — see `DA-03` (revised).
7. The Dataverse delegation table (review F-07) is now cited directly and compared against SQL's and SharePoint's.
8. Reconciliation and drift detection (review F-08) now has 18 findings (`SY-06`..`SY-17`) covering change-tracking re-seed, dead-letter replay, Microsoft's own reconciliation reference architectures, and — the single most load-bearing new finding — the Synapse Link FAQ's catalogue of ways a replica silently diverges while reporting success (`SY-14`).
9. Read/write workload shape and concurrency (review F-09) now has explicit PE:08 doctrine (`SC-11`..`SC-13`) and an explicit negative finding that no concurrent-user ceiling is published anywhere (`SC-16`), closed instead by a testing method (`SC-17`).
10. Data quality (review F-10) now has 18 findings (`DQ-01`..`DQ-18`), including a genuine contradiction discovered in Microsoft's own business-rules documentation (`DQ-10`) and the high-impact finding that duplicate detection is suppressed by default on Web API updates (`DQ-12`).
11. "System of record" vs "source of truth" vocabulary (review F-11) is resolved as far as Microsoft resolves it: the terms are used loosely and interchangeably across Learn surfaces, with the closest thing to a definition found in the Azure Architecture Center microservices data-considerations page, tied to consistency requirements, not to Power Platform (`DQ-03`, `DQ-15`).
12. Provenance corrections (review F-12): the SharePoint concurrency Q&A answerer is corrected from "Microsoft moderator" to "Microsoft External Staff" — see `DA-08` (revised).
13. Consuming Fabric/analytical outputs back into apps (review F-13) is now evidenced: read-only OneLake virtual tables are the only documented maker-side path (`VT-12`, `VT-16`); freshness is ~1 hour (`VT-14`).
14. SQL Managed Instance connector specifics (review F-15) are restored (`SQ2-11`).
15. Standard-table consistency model (review F-17) is now explicit (`SC-06`), alongside the documented exceptions (Power Pages 15-min cache — `SC-14`; `CountRows` cached value — `SC-12`).

**Provenance rule.** Sources are **fetched** (page retrieved, `ms.date` read — the default), **fetched-summarised** (fetch tool returned a summary rather than raw text; quotes are as returned), **snippet-only** (search result only; any finding relying solely on it is capped at MEDIUM or LOW), or **T2/T3/T4** (non-Learn). Kind is recorded per source in §12. Source ids keep their sub-register prefix (`DV:S01`, `SQ:S1`, `SP:S-01`, `EX:S05`, `XC:S02` from v1; `VT:S1`, `SY:S-01`, `SQ2:S1`, `SC:S1`, `DQ:S1` new in v2) so each quote is traceable to the sub-research that fetched it.

**Origin tags.** Every finding carries **Origin:** MS (Microsoft statement) / INF (analyst inference from documented limits) / T3 (independent) / T4 (community signal) / UNKNOWN. A POOR verdict derived by inference is phrased "treat as unsupported until verified", never as a Microsoft statement. **New in v2:** every store-fit-matrix cell now carries an explicit origin tag (review F-01 required this).

**Overall confidence HIGH**, per the Research Gate verdict (PASS / HIGH, recorded against this v2 revision). Raised from v1's MEDIUM because: the five HIGH-severity review gaps are closed with 90 new Tier-1-dominant findings (all but a handful of the ~95 new sources are Microsoft Learn, fetched and dated); the two most consequential v1 gaps (no sourced Dataverse→SQL path; unsourced SQL matrix cells) are resolved with hard evidence, including one explicit negative finding in each case. The gate found no CRITICAL gap and judged the remaining open items — a genuine, honestly-flagged self-contradiction in Microsoft's own docs on whether business rules enforce on Web API writes (`DQ-10`); a handful of engagement-measured unknowns that are documented absences rather than answerable facts (virtual-table throughput at volume, `VT-09`; no published concurrent-user or standard-table-row ceiling, `SC-16`/`SC-18`); and some MEDIUM-gap content resting on AI-assisted, 3-year-refresh-cycle Microsoft guidance (`DQ-01`) — to bound the *precision* of specific claims, not the *direction* of the guidance, and therefore not to block canonicalization. These items are carried forward as the Area 3 maintenance backlog (see "Gaps Still Open" and "Remaining Unknowns" at the end of this file).

**Volatility.** Everything flagged volatile in v1 remains volatile. New volatile items: virtual-table provider preview status (Fabric, Salesforce, Oracle — `VT-01`), the Fabric low-latency sync engine "rolling out now" (`VT-14`), the Power Automate licensing transition period (`SC-04`, no ETA for GA), and Fabric Mirroring's source list, which has grown repeatedly and could add Dataverse at any time (`SY-01`, re-check before every engagement).

---

---

## 1. Classification model

| Fit class | Meaning (data-store context) |
|---|---|
| **STRONG FIT** | The data requirement maps to a documented capability of the store; no documented limit approached; the licence path is the one the audience already has. Phrased as "no documented constraint violated". |
| **CONDITIONAL FIT** | Fit depends on a measurable data condition (row volume per query, relationship count, security granularity, freshness, concurrency, licence, network posture) that must be validated before commitment. |
| **POOR FIT** | Collides with a documented hard limit, an explicit Microsoft "not designed for" statement, or an unsupported scenario. |
| **HYBRID** | Two or more stores with an explicit ownership map and sync/read-through mechanism (Microsoft's own "polyglot persistence" and "Azure-native database alongside Dataverse" guidance). |
| **KEEP IN PLACE** | The data stays in the existing system of record; Power Platform reads through (virtual table / connector / embedding) or receives events; no copy. |

Evidence tags per `../source-policy.md`: FACT, RECOMMENDATION, CONSTRAINT, TRADE-OFF, RISK, ANTI-PATTERN, DECISION CRITERION, PATTERN.

---

## 2. Store fit matrix (data requirement → default fit per store)

Read each row as: given this observable data requirement, what is the default fit of each store, and which finding carries the evidence. "Dataverse" = standard tables unless stated. Origin MS unless tagged.

| # | Data requirement (observable) | Dataverse | SQL / Azure SQL (connector) | SharePoint / Lists | Keep in external system | Findings |
|---|---|---|---|---|---|---|
| 1 | Relational model with several related entities, referential integrity, cascades | STRONG | STRONG (engine) / CONDITIONAL (connector conformance) | POOR (12 joins/view; delete-only opt-in integrity) | n/a | DA-05, DA-06, DA-30, DA-40 |
| 2 | Any queried table expected > 2,000 rows with non-trivial filters/sorts in a canvas app | STRONG (broadest delegation) | CONDITIONAL (delegation subset; types) | CONDITIONAL → POOR (`Not`, ID ranges, complex columns non-delegable; 5,000 LVT) | CONDITIONAL (custom connector = no delegation) | DA-02, DA-31, DA-39 |
| 3 | Multi-row writes that must succeed or fail together | CONDITIONAL (change set / plug-in / custom API only) | CONDITIONAL (stored procedure with transaction) | POOR (no transaction, last writer wins) | HYBRID (saga; system of record posting as pivot) | DA-07, DA-08, DA-52, PS-45 |
| 4 | Concurrent edits on the same record by several users | CONDITIONAL (optimistic concurrency via SDK/API; canvas conflict error) | UNKNOWN (connector semantics undocumented) | POOR (no conflict setting; version history is recovery) — T4 | depends on system | DA-08, DA-41, PS-46 |
| 5 | Row-level visibility by owner/team/unit; column-level confidentiality | STRONG (BU/roles/teams; column security; masking with Managed Env) | CONDITIONAL (Entra explicit connections + RLS in DB; internal users only) | POOR (≤5,000 unique scopes recommended; no column security) | KEEP IN PLACE if the system enforces it | DA-11, DA-12, DA-33, DA-42, DA-55 |
| 6 | Audit trail of field changes for N years | STRONG (log meter; set retention at creation) | CONDITIONAL (build in DB; triggers break connector writes) | POOR (versioning only; attachment changes not tracked) | KEEP IN PLACE | DA-16, DA-30 |
| 7 | Documents as the record (files + metadata, versions, labels) | CONDITIONAL (file columns ≤131 MB; JPG conversion; no labels) | POOR | STRONG (libraries, versioning, Purview labels) | n/a | DA-15, DA-44, DA-59 |
| 8 | Attachments-heavy volume (GB of binaries) | CONDITIONAL (file meter 20× cheaper than database; LTR does not shrink files) | n/a (blob outside) | STRONG (250 GB/file) — loses Dataverse row security | HYBRID (Blob/SharePoint + reference) | DA-14, DA-15, DA-62 |
| 9 | High-ingest, semi-structured, time-bounded data (events, telemetry, logs) | CONDITIONAL (elastic tables; no transactions/joins; GA status UNKNOWN) | CONDITIONAL/WEAK — Microsoft's own data-store model guide routes "high-ingest timestamped metrics and events" to Azure Data Explorer/Eventhouse, not Azure SQL; sustained write capped by log rate (50/96/100 MiB/s, does not scale with vCores) — origin MS, `SQ2-06`, `SQ2-07` | POOR | HYBRID (Azure Data Explorer/Eventhouse in Fabric is Microsoft's named target — origin MS, `SQ2-06`) | DA-09, PS-57, SQ2-06, SQ2-07 |
| 10 | Aggregates/KPIs over > 50,000 rows; trend or multi-year reporting | POOR in-platform → analytical copy required | STRONG (engine; Power BI import) | POOR (import-only, slow) | KEEP IN PLACE / warehouse | DA-03, DA-19, DA-20, DA-21 |
| 11 | Reporting must respect per-user record security | STRONG via TDS/DirectQuery (Dataverse roles) — limits apply; RLS must be rebuilt in any copy | CONDITIONAL (SSO/RLS) | POOR (connection-owner view) | depends | DA-20, DA-22 |
| 12 | Keep N years of closed records cheaply, read-only | CONDITIONAL (long-term retention: Managed Env, irreversible, ~50% DB saving, none for files) | CONDITIONAL, not STRONG — Long-Term Retention is *backup* retention restorable only as a new database, not a queryable archive; no cold/cheap storage tier exists for Azure SQL rows; cheapness requires time partitioning + columnstore archival compression (slower reads, more CPU) or export to a different store — origin MS, `SQ2-04`, `SQ2-05`, `SQ2-14` | CONDITIONAL (Purview labels on items; not attachments) | Lake / archive store | DA-17, DA-18, SQ2-04, SQ2-05, SQ2-14 |
| 13 | Data must remain in an existing system of record (ERP/legacy) | KEEP IN PLACE + read-through (virtual tables lose audit/row security/search/offline) or replicated subset | KEEP IN PLACE + connector (gateway if on-prem) | n/a | STRONG | DA-45 … DA-53 |
| 14 | Live value from the external system at UI time ("can't do without real-time") | virtual table / connector call (synchronous dependency accepted) | connector call | n/a | STRONG (embedding / read-through) | DA-46, DA-47 |
| 15 | App must keep working when the external system is down | HYBRID (local pending state + queue + idempotent writes) | same | POOR | POOR as sole store | DA-47, DA-50, DA-52 |
| 16 | Two systems both edit the same entity | HYBRID only with per-field ownership map; bidirectional sync = build (no product tooling outside D365 F&O dual-write) | same | POOR | same | DA-48, DA-49 |
| 17 | Nightly bulk load of large volumes into Dataverse | CONDITIONAL (service protection; bulk APIs; elastic staging) → Microsoft steers to real-time/delta | CONDITIONAL, not STRONG — throughput capped by tier log rate; minimal logging (the fast path) needs TABLOCK + empty target + no replication; Microsoft publishes no throughput guarantee, only "measure it yourself"; the Power Platform SQL connector cannot bulk-load at all (100 CRUD/10s, 110s timeout) — a separate ETL toolchain (ADF/bcp) is implied — origin MS, `SQ2-07`, `SQ2-12`, `SQ2-13` | POOR (600 calls/min/connection) | n/a | DA-10, DA-51, SQ2-07, SQ2-12, SQ2-13 |
| 18 | Data must stay on-premises | POOR (SaaS) | CONDITIONAL (gateway: 2 MB/8 MB caps, cluster ops, results transit cloud) | POOR | STRONG for the store; Power Platform transit remains cloud | DA-34, DA-35, DA-58 |
| 19 | No public endpoint on the cloud database | CONDITIONAL (Managed Env IP firewall; VNet for outbound) | CONDITIONAL (VNet support: Azure sub, paired regions, V2 actions, no gateway) | POOR (M365 endpoints only) | via VNet/ExpressRoute | DA-36, DA-56 |
| 20 | Data residency: EU Data Boundary / country-level | CONDITIONAL (macro region #3 + EU billing; ADR for country; schema names replicate globally) | CONDITIONAL (Azure region choice) | CONDITIONAL (M365 geo) | as is | DA-57, DA-58 |
| 21 | Customer-controlled encryption key / approve Microsoft access | CONDITIONAL (CMK, Lockbox: Managed Env + E5-class; feature gaps) | STRONG, with conditions — Azure SQL TDE/BYOK is real, scopeable to server/instance/(SQL DB) database, cheaper to reach than Dataverse CMK (no Managed-Environment/E5 gate), but the key vault becomes a tier-0 availability dependency with a 30-minute recovery cliff — origin MS, `SQ2-01`, `SQ2-02`, `SQ2-09` | CONDITIONAL, not POOR (v1 was WRONG here) — Microsoft 365 Customer Key explicitly covers SharePoint/OneDrive via a dedicated DEP; the real limit is *granularity* (one policy per tenant/geo, not per site/library/app) plus E5-class licensing and two paid Azure subscriptions — origin MS, `SQ2-10` | as is | DA-55, SQ2-01, SQ2-02, SQ2-09, SQ2-10 |
| 22 | Team-scoped app, seeded licences, ≤ 2 GB, no API/sharing/ALM | STRONG (Dataverse for Teams) — one-way upgrade | n/a | CONDITIONAL (lists) | n/a | DA-13, DA-43 |
| 23 | Hard uniqueness on a business key; idempotent integration | STRONG (alternate keys ≤10/table; not on secured columns) | STRONG (unique index) | POOR (single-column "enforce unique" only) | n/a | DA-53, DA-60 |
| 24 | Multi-environment ALM (dev/test/prod) for the schema | STRONG (solutions carry schema; data via CMT/dataflows) | CONDITIONAL (DB DevOps outside Power Platform) | POOR (lists outside solutions; env variables; internal names drift) | n/a | DA-24, DA-44 |
| 25 | "Free" store to avoid premium licences | n/a (premium) — except Dataverse for Teams | n/a (premium) | Seeded (standard connector) — AP: licensing-driven store choice | n/a | DA-43, DA-63 |
| 26 | App must display a computed analytical insight (score, forecast, segment) produced in Fabric | CONDITIONAL (read-only OneLake virtual table; preview; needs a genuinely unique source key or rows silently disappear) | n/a | n/a | STRONG (insight stays in Fabric; app reads via virtual table or is told the result through a separate integration) | VT-12, VT-13, VT-14, VT-16 |
| 27 | One master-data environment must serve canvas apps built in other environments | CONDITIONAL — cross-environment **reads** are supported via explicit environment selection in the Dataverse connector; cross-environment **relationships/joins/cascades/security inheritance** are not — origin MS | n/a | n/a | n/a | DA-25 (revised) |

---

## 3. Decision boundaries (data requirement × condition → constraint → implication)

Strongest evidence-backed boundaries. Origin in brackets.

- **Queried table > 2,000 rows × non-delegable Power Fx** → silent first-500/2,000 results → store must be delegable AND the formula set restricted to that store's delegation table; SharePoint's table is the narrowest (`Not` never; ID only `=`; complex columns partial); Excel/collections never (MS, DA-02, DA-31, DA-39).
- **Any query touching > 5,000 items in SharePoint Online without an indexed, selective filter** → list view threshold error; "the LVT limit can't be changed" → SharePoint only when access paths are few and indexable (MS, DA-39).
- **Entity with > 12 lookup/person/metadata columns in one view or flow `Get items`** → SharePoint query/flow fails → denormalise or leave SharePoint (MS, DA-40).
- **Writes that must be all-or-nothing** → Power Fx is never transactional, even within one store → Dataverse change set / custom API / plug-in, or SQL stored procedure; across stores → saga with pending state and ERP posting as pivot (MS, DA-07, DA-52).
- **Per-user row/column security enforced at the store** → Dataverse natively; SQL only with Entra Integrated explicit connections + RLS/DENY in the database (Windows/SQL auth = one shared principal, "isn't secure"); SharePoint never for columns and ≤ 5,000 scopes recommended for rows (MS, DA-11, DA-33, DA-42).
- **Aggregation over > 50,000 rows (FetchXML/OData aggregates, canvas `Sum`/`Min`/`Max`/`Avg`, model-driven charts/dashboard grids) or queries > 5 min (2 min for `SELECT *`/joins on TDS)** → fails in Dataverse; note the 50,000 figure does NOT bound ordinary filtered reports, which "are allowed to span large datasets that are beyond 50,000 rows" within the 5-minute window (MS, reporting-considerations, quoted in `DA-03` revised) → analytical copy (Fabric link / Synapse Link / Power BI import) from day one when *aggregation, charts, or cross-period history* on growing tables are required (MS, DA-03, DA-19, DA-21).
- **Reporting on a copy × Dataverse security** → security does not travel: Fabric/Synapse copies need RLS rebuilt; secured columns export as null unless the lake app user is in the profile; embedded Power BI ignores app roles (MS, DA-20, DA-22).
- **Retention "N years" × cost** → long-term retention requires Managed Environments, is irreversible, saves ~50% database and 0% file; audit retention is non-retroactive and defaults to Forever → decide retention and audit scope at environment creation (MS, DA-16, DA-17).
- **Backups as archive** → ≤ 28 days, same region, not downloadable → not a retention mechanism (MS, DA-18).
- **Relational volume × capacity** → database is the meter that cannot be offset (borrowing Database → Log → File only); add-on $40/GB database vs $2/GB file; over-capacity blocks copy/restore/create → binaries to file columns or external store; lifecycle jobs mandatory (MS, DA-14, DA-62).
- **Row-level visibility that may ever be needed on a table** → ownership type (user/team vs organization) is immutable after creation → decide per table before build (MS, DA-12).
- **Ad-hoc per-record collaboration at scale** → sharing writes PrincipalObjectAccess rows (default Reparent = Cascade All multiplies per child); POA cannot be deleted directly → teams/BUs/hierarchy security first; referential relationships unless inheritance is required (MS, DA-11).
- **Data owned by an external system × need for audit, row security, search, offline, rollups or analytics on it in Dataverse** → virtual tables drop all of these → replicate a subset one-way (dataflow/event) as a disposable read model keyed by the source id; otherwise virtual table for uniform-security reference reads (MS, DA-45, DA-46).
- **Freshness requirement** → real-time only for "can't do without live" (synchronous coupling); events/queue for minutes; dataflows ≥ 30-min floor, ≤ 48 refreshes/day; Fabric/Synapse link "near real-time, not guaranteed", up to 60 min; Power Pages server cache 15 min (MS, DA-47, DA-49, DA-51).
- **Two-way edits on one entity** → conflict rules per field; Microsoft's own bidirectional product (dual-write) exists only for D365 F&O and "makes crucial changes in the Dataverse schema" → prefer per-field one-way flows; bidirectional is a build (MS, DA-48).
- **Writes toward the system of record** → at-least-once delivery + idempotency (alternate key on the external id); never a synchronous webhook for side effects ("the request sent to the configured endpoint can't be recalled"); one retry owner, exponential backoff, Retry-After honoured (MS, DA-50, DA-52, DA-53).
- **Nightly bulk into Dataverse** → 6,000 requests / 20 min execution / 52 concurrent per user per web server per 5 min; entitlement limits separate; "move towards real-time integration" → delta + bulk APIs + parallel identities + Retry-After, or stage in elastic tables (MS, DA-10, PS-18).
- **Existing on-prem SQL** → gateway mandatory: 2 MB request / 8 MB response, 110 s action timeout, stored procedures lose OUTPUT/return/multi-result sets, "Execute a SQL query (V2)" unsupported; business-critical → ≥ 2 nodes per cluster, dev + prod clusters, key custody → cost the gateway estate or move to Azure SQL + VNet (MS, DA-34, DA-35).
- **Existing SQL schema reuse** → PK required for writes (no tinyint/smallint), server-side triggers break Insert/Update, flow triggers need IDENTITY + ROWVERSION, unsupported types (binary, rowversion, hierarchyid, spatial…), OData identifier rules → schema audit before Options (MS, DA-30).
- **High call volume against SQL through the connector** → 100 CRUD calls / 10 s per connection (flows), 300 calls / 30 s per user (apps), 125 concurrent per connection, time-based connectionID throttling → set-based stored procedures, no per-row loops; implicitly shared connections share ONE connection budget (MS, DA-32).
- **Private Azure SQL** → VNet support: Azure subscription linked, paired-region subnets, V2 actions only, no gateway; otherwise 90-day service-tag allowlist refresh (MS, DA-36).
- **Sensitive documents that must carry protection when downloaded** → SharePoint + sensitivity labels; Dataverse file columns have no label mechanism; hybrid inherits two security models that do not synchronise (MS, DA-44, DA-59).
- **EU Data Boundary** → tenant and ALL environments in macro region "EU and EFTA" (#3, not "Europe and UK") + EU billing address; country-level only with Advanced Data Residency on all M365 seats; table/column names, app names and Power Pages URLs replicate globally; Copilot flex routing defaults on for tenants created after 2026-03-25 (MS, DA-57, DA-58).
- **Customer-managed key / Lockbox / IP firewall / masking / 28-day backups / long-term retention** → Managed Environments (premium for all users); CMK, Lockbox, IP firewall additionally E5-class M365 → data requirements decide the licensing model (MS, DA-55, DA-61).
- **Team-scoped app on seeded licences** → Dataverse for Teams: 2 GB combined, no API, no record sharing, no copy; upgrade one-way and requires tenant capacity + premium licences for all users (MS, DA-13, DA-43). The "1 million rows" figure appears on the Dataverse for Teams overview/licensing FAQ pages but not on the environment page (C-05).
- **Excel as a store × more than one writer or > 2,000 rows** → "Simultaneous file modifications … are not supported", 6-minute lock, 25 MB, duplicate inserts on retry → seed/reference/export only (MS, DA-41).
- **Cross-environment master data × canvas apps** → the Dataverse connector supports selecting a *different* environment as a data source ("specify a different environment to pull data from") → **reads** across environments are possible; but relationships, joins, cascades and security-role inheritance never cross environments → a shared reference environment is viable only as a read source per app, never as a relational parent (MS, DA-25 revised, VT-N/A — see §12 for the connector page).
- **Read-model target must be a writable SQL/Azure SQL Database × Dataverse as the source** → no first-party managed replication exists (Dataverse is absent from the Fabric Mirroring source list; Synapse Link targets ADLS Gen2; Link to Fabric targets OneLake; Data Export Service is retired) → any writable Azure SQL copy is a customer-built-and-operated pipeline (ADF/Fabric Data Factory or Dataflow Gen2 incremental refresh), with its own watermark, delete-detection and reconciliation job as first-class, budgeted components (MS, SY-01, SY-04, SY-13, SY-18).
- **Read-only SQL access to Dataverse data is required, writes are not** → Link to Fabric's auto-provisioned SQL analytics endpoint answers this for free (Fabric capacity aside) but is read-only T-SQL with 8 KB text truncation on lakehouse tables and a 150-item-per-workspace ceiling → prefer this over a custom pipeline whenever no write requirement exists (MS, SY-02, SY-03).
- **Trustworthy replica × Synapse Link/Fabric link** → the replica can diverge from Dataverse while reporting sync success: secured columns silently export as null unless the sync application user is granted column-security-profile read; calculated columns freeze at their initial value if the row version doesn't change; direct-SQL deletes never propagate; new columns don't appear until a data change occurs → row-count comparison does not detect drift; the documented remedy for most of these is "resynchronize the table", which must be budgeted as a routine operation, not an incident (MS, SY-14, SY-15).
- **Virtual table over a large or write-required external source** → Microsoft publishes no performance, latency, throughput, caching or query-pushdown characterisation for virtual tables at any volume, and virtual tables are absent from the canvas delegable-data-source list (so delegation warnings may not even appear when truncation happens); column selection is ignored (all attributes always return); a virtual table can never be the "1" side of a 1:N relationship → appropriate only as a narrow, positively-filtered, sub-1,000-row, read-mostly reference/lookup surface with a mandatory measured spike before commitment; not a general integration layer (MS, VT-05, VT-06, VT-09, VT-10, VT-17).
- **Business volume (orders/day, lines, attachments) must be translated into a Dataverse request budget** → Microsoft counts CRUD, assign, share, "user-driven and internal system requests required to complete CRUD transactions", plug-ins, classic workflows and custom controls, plus retries and pagination — but publishes no amplification multiplier, because it is a property of each solution's customisation, not of the platform → the multiplier must be measured per engagement (Application Insights for Dataverse; flow Analytics → Actions tab), never assumed or quoted from another engagement (MS, SC-01, SC-02, SC-21).
- **No published concurrent-user ceiling exists for any Dataverse/Power Apps surface** → the governing constraints are per-authenticated-user service protection, per-identity daily entitlements, and contention on shared rows/identities, not a headcount ceiling → the concurrency question is answered only by a load test against a production-like environment with realistic personas and data volumes (PE:05), never by a quoted number (MS, SC-16, SC-17).
- **A rule must hold no matter which client writes the data (canvas, API, integration)** → only *table-scoped* (not form-scoped) business rules reach beyond the model-driven client, and even that is contradicted on the same Microsoft page (the FAQ says business rules "aren't executed inside Dataverse", while the scope table says Entity scope reaches "server"); duplicate detection is suppressed by default on Web API updates and has no default rules outside accounts/contacts/leads → treat cross-client server-side enforcement of business rules as **Assumed, not Confirmed**, until tested in the target environment; use alternate keys (not duplicate detection) for any uniqueness that must hold on integration paths (MS, DQ-09, DQ-10, DQ-12).
- **"System of record" and "source of truth" have no single Microsoft definition** → the D365 Implementation Guide uses "primary data" and "master data source"; the Azure Architecture Center's only near-definition ties "source of truth" to a *consistency requirement* per entity ("Use a single source of truth when you require strong consistency… Other services might hold their own copy… not considered the source of truth"), and even "system of record" is shown handing over between systems at a lifecycle boundary → the pack must declare its own vocabulary as pack-local, never cite Microsoft as the authority for a formal distinction (MS, DQ-03, DQ-15).

---

## 4. Findings

Ids DA-nn are stable. Sub-register source ids in brackets (`DV:S01` = Dataverse sub-research source S01, etc.; see §12).

### 4.1 Data characteristics → architectural implications

#### DA-01 — Microsoft's own frameworks put data requirements first: model, transaction rate, concurrency, growth, access method, consistency model, team skills, service limits — and legitimise polyglot persistence
- **Classification:** RECOMMENDATION (method) · **Origin:** MS
- **Evidence:** PPWA PE:03: "Understand the specific requirements of your workload, such as data volume, expected transaction rates, concurrency, data types, and expected growth." "if your data has a highly relational structure, you might opt for a relational database management system (RDBMS)". "Most cloud workloads use a combination of storage technologies. This technique is known as the polyglot persistence approach." "The best service for your workload might be a technology that your team isn't skilled at, can't afford, or it might require extra security layers." [SQ:S16, EX:S02]. Azure Architecture Center criteria: "Consistency model: Strong, eventual, or configurable"; "Concurrency needs: Optimistic versus pessimistic locking"; "Data access method: Direct query language … REST API, SDK … Some platforms restrict access to a proprietary API layer, which affects query flexibility" [EX:S10, SQ:S17].
- **Why it matters:** The data lens must elicit these attributes per entity before any store is named; Microsoft explicitly frames "proprietary API layer" access as the axis on which Dataverse differs from SQL.
- **Decision impact:** Capture per entity: volume, growth, relations, transaction rate, concurrency, consistency, access method, residency → store per entity, not per solution.
- **Confidence:** HIGH · **Sources:** SQ:S16, SQ:S17, EX:S02, EX:S10

#### DA-02 — Volume is a query-shape problem before it is a storage problem: non-delegable queries silently return the first 500 (max 2,000) rows in canvas apps; collections cannot participate in delegation
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** "When a query is nondelegable, Power Apps gets the first 500 records from the data source and then runs the actions in the query. You can increase this limit to 2,000 records." "If the record you want is record 501 or 500,001, Filter doesn't find or return it." "Collections are a static in-memory list of records and can't participate in delegation." Test advice: "set this value to 1" [EX:S16, SP:S-33]. Anti-patterns named by Microsoft: "loading too much data, turning everything into collections, and overloading OnStart" [EX:S25].
- **Why it matters:** The failure is silent wrongness, not slowness (PS-13). The delegation table is store-specific: Dataverse broadest; SQL partial; SharePoint narrowest; Excel/collections none.
- **Decision impact:** Requirement "any queried table may exceed 2,000 rows" → constraint: delegable store + delegable formula subset → implication: store choice constrained by query shape; delegation proof with row limit = 1 is a validation gate.
- **Confidence:** HIGH · **Sources:** EX:S16, EX:S25, SP:S-33

#### DA-03 — Aggregation and history (REVISED in v2 — the 50,000 figure is scope-specific, not a flat Dataverse ceiling; see review F-06): 50,000 bounds *aggregate queries, charts and dashboard grids*, NOT ordinary filtered reports, which may return far more within the 5-minute (2-minute for `SELECT *`/joins) timeout; Microsoft still says built-in reporting is for "shorter periods of time"
- **Classification:** CONSTRAINT / DECISION CRITERION · **Origin:** MS
- **Evidence:** "Queries that return aggregate values are limited to 50,000 records … AggregateQueryRecordLimit exceeded" [DV:S05]. "The default and maximum page size is 5,000 for standard tables and 500 for elastic tables." Simple paging "Can't return a dataset larger than 50,000 records" [DV:S04]. "Charts display views that return up to 50,000 records." [XC:S05]. **Precision added in v2** (re-fetched verbatim, ms.date 2023-12-20, updated 2025-05-07): "The reporting capabilities built in to Microsoft Dataverse are designed to let users run reports on datasets that span shorter periods of time." — followed immediately by: "**Within the five-minute duration, reports and queries are allowed to span large datasets that are beyond 50,000 rows, which provide significant flexibility to satisfy most operational reporting needs.**" "For charts and grids displayed in dashboards, your apps allow users to run queries that have a dataset that has fewer than 50,000 rows. Should a user run a dashboard query that spans a dataset of 50,000 or more rows, the message 'The maximum row limit is exceeded. Reduce the number of rows' is returned." "Both options effectively offload reporting workloads from Dataverse to another datastore" [XC:S06]. PPWA PE:08 defines OLAP as separate from OLTP [DV:S25]. Canvas apps carry their own, separate 50,000-row aggregate cap: "All aggregate functions are limited to a collection of 50,000 rows" [connection-common-data-service, cited in DA-33 revision].
- **Why it matters:** The 50,000-row ceiling applies specifically to (a) FetchXML/OData `AggregateQueryRecordLimit`, (b) model-driven charts/dashboard grids, and (c) canvas `Sum`/`Min`/`Max`/`Avg`/`CountIf` aggregate functions — NOT to ordinary filtered, non-aggregate reports, which Microsoft explicitly says may span "beyond 50,000 rows" inside the 5-minute window. Over-generalising the limit (as v1 did) would make the pack encode a false hard constraint and push every moderately large reporting requirement into an unnecessary analytical-copy design.
- **Decision impact:** Requirement "aggregate/KPI/chart over > 50,000 rows, or cross-period/org-wide history" → constraint: `AggregateQueryRecordLimit`, chart/dashboard-grid cap, 5-min (2-min) report timeout → implication: analytical copy (Fabric link / Synapse Link / Power BI import) is a day-one design element for aggregation and history (DA-19..DA-21). Requirement "large but *filtered, non-aggregate* operational report" → in-platform may suffice within the 5-minute window; do not reflexively route it to an analytical copy.
- **Conditions:** XC:S06 predates Fabric link; principle stands, mechanism updated (C-04). Re-fetched and confirmed by the v2 consolidator, 2026-09-02.
- **Confidence:** HIGH · **Sources:** DV:S04, DV:S05, DV:S25, XC:S05, XC:S06

#### DA-04 — Growth: three Dataverse meters (database / file / log) with fixed table placement; capacity is an entitlement, not a technical limit; database is the binding and most expensive meter and cannot be offset
- **Classification:** FACT / CONSTRAINT · **Origin:** MS
- **Evidence:** "There's no technical limit on the size of a Dataverse environment. The limits mentioned on this page are entitlement limits". File meter: "Attachment; AnnotationBase; Any custom or out-of-the-box table that has columns of datatype file or image". Log: "AuditBase; PlugInTraceLogBase; Elastic tables". "All other tables count for your database". "Database storage includes both the database rows and index files". "All Dataverse indexes are reported at the Dataverse database capacity rate." Borrowing: "Capacity can flow only from Database to File, and never in the opposite direction: Database → Log → File." "Database overages can't be offset because Database is the highest-value storage type." [DV:S01]. Licensing Guide Sept 2026: add-ons "Database capacity … $40/month; File … $2/month; Log … $10/month" per GB; PAYG "$48 / $2.40 / $12"; Power Apps Premium accrues "250 MB" database and "2 GB" file per user [DV:S40].
- **Why it matters:** Schema decisions (text vs file column, search-enabled columns, audit on/off, elastic vs standard, index-creating Quick Find) land on differently priced meters. Database is 20× file per GB and is the one meter spare capacity elsewhere cannot rescue.
- **Decision impact:** Requirement "N GB relational + M GB binaries + audit" → constraint: meter placement fixed by column/table type → implication: binaries in file/image columns or external store; narrow filterable columns; scoped search/audit; cost model per meter (DA-62).
- **Conditions:** Default tenant database capacity conflicted 10 vs 20 GB (C-01).
- **Confidence:** HIGH · **Sources:** DV:S01, DV:S40

#### DA-05 — Relational complexity: Dataverse supports 1:N and N:N, but only one parental (cascading) relationship per child table; cascading Share/Reparent silently propagates access
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** "for each table pair there's only one parental relationship." "No new relationship can have any action set to Cascade All, Cascade Active, or Cascade User-Owned if the related table … already exists as a related table in another relationship that has any action set to Cascade All". "A custom table can't be the primary table in a relationship with a related system table that cascades." Changing cascade to None requires the "Inherited access rights cleanup" job [DV:S07].
- **Why it matters:** A child with two "strong" parents (order line ↔ order and shipment) cannot be modelled; one parent must be referential. Cascade behaviour is a security and storage decision embedded in the ERD (DA-11).
- **Decision impact:** Requirement "child inherits ownership/access from two parents" → constraint: single parental relationship → implication: choose the dominant parent; second via lookup + explicit process/sharing.
- **Confidence:** HIGH · **Sources:** DV:S07

#### DA-06 — Derived data: rollup columns are asynchronous (≥ 1 h; 50/table, 200/environment; 1:N only; cannot trigger workflows); formula columns are computed at read time (unsortable across tables, no offline, no triggers, no search; filters on them are throttled)
- **Classification:** CONSTRAINT / TRADE-OFF · **Origin:** MS
- **Evidence:** "The rollups are calculated by scheduled system jobs that run asynchronously in the background." "The default minimum recurrence setting is one hour." "maximum of 200 rollup columns for the environment and up to 50 rollup columns per table." "A workflow can't be triggered by the rollup column updates." "A rollup can't be done over the N:N relationships." "A rollup column is aggregated under the system user context." [DV:S08]. Formula columns: "You can't change a column type after the column is created." "sorting is disabled on: A formula column that contains a column of a related table". "You can't trigger workflows or plug-ins on formula columns." "Formula columns don't display values when the app is in mobile offline mode." [DV:S09]. Filters on formula/calculated columns → `ComputedColumnCauseTimeout` and throttling [DV:S42].
- **Why it matters:** Real-time totals that gate business logic (credit limit at save, stock balance) cannot rely on rollups; derived values used for filtering/sorting at scale must be persisted.
- **Decision impact:** Requirement "real-time balance/total gating a write" → constraint: rollups async, non-triggering → implication: plug-in-maintained denormalised column or query-at-runtime; rollups for informational KPIs only.
- **Confidence:** HIGH · **Sources:** DV:S08, DV:S09, DV:S42

#### DA-07 — Transactional requirements: atomicity exists only server-side — Dataverse change set / ExecuteTransaction / synchronous plug-in / custom API, or a SQL stored procedure; Power Fx is never transactional, even within one store
- **Classification:** DECISION CRITERION · **Origin:** MS
- **Evidence:** Dataverse + canvas reference architecture: "Each operation is independent and isn't handled as an atomic transaction. For example, if the application created a Venue row but couldn't create a session, the Venue row would remain." "With both of these approaches [custom API, Functions in Dataverse], the work performed by the logic is in a transaction." [EX:S52]. SQL + canvas reference architecture: "Each Power Fx operation is independent and isn't handled as an atomic transaction… Use SQL Server stored procedures with transaction support." [EX:S53]. Elastic tables: "these operations succeed but aren't atomic" [DV:S03]. Cross-store: "Traditional database guarantees like ACID aren't directly applicable to multiple independently managed data stores." "Compensating transactions might not always succeed" [EX:S12, EX:S13]. Dataverse mechanics in PS-45.
- **Why it matters:** Header + lines, stock movements, allocations and postings need a transaction boundary; the UI layer cannot provide one; across Dataverse and an ERP the only option is a saga with a pivot and a human fallback.
- **Decision impact:** Requirement "all-or-nothing multi-row write" → constraint: no client-side multi-Patch → implication: custom API / plug-in (Dataverse) or stored procedure (SQL); cross-system → saga with ERP posting as the irreversible pivot, pending state in Dataverse, reconciliation queue (DA-52).
- **Confidence:** HIGH · **Sources:** EX:S52, EX:S53, EX:S12, EX:S13, DV:S03, PS-45

#### DA-08 — Concurrency: Dataverse optimistic concurrency is SDK/Web API-only (canvas `Patch` surfaces a server-conflict error); SQL connector locking semantics are undocumented; SharePoint Online lists have no conflict handling (last writer wins)
- **Classification:** CONSTRAINT / RISK · **Origin:** MS (Dataverse) / UNKNOWN (SQL) / T4 (SharePoint: Microsoft moderator answer)
- **Evidence:** Dataverse: PS-46 (`ConcurrencyVersionMismatch`; canvas "Conflicts exist with changes on the server"). SQL: no Microsoft page found on connector isolation/transaction scope of `Patch`/`UpdateIf` (U-05). SharePoint: "Unfortunately for lists, we don't have any settings to ensure that only one user can edit an item at a time." "If a conflict occurs and modified values are overwritten, you can restore it by checking the version history." [SP:S-16, Microsoft Q&A 2023-11]. Versioning "50,000 major versions" [SP:S-01]; recycle bin 93 days [SP:S-18].
- **Why it matters:** Multi-user editing of the same record is common in case/asset management; only Dataverse offers a documented (code-level) mechanism.
- **Decision impact:** Requirement "concurrent edits on the same record" → Dataverse with explicit conflict handling (CONDITIONAL); SharePoint POOR (single-writer process design or accept overwrites); SQL → test.
- **Confidence:** HIGH (Dataverse) / MEDIUM (SharePoint) / UNKNOWN (SQL) · **Sources:** PS-46, SP:S-16, SP:S-01, SP:S-18

#### DA-09 — High-ingest / semi-structured data: elastic tables (Cosmos DB, log meter) scale horizontally but forfeit transactions, joins, N:N to standard tables, rollups, sharing, cascades, Power BI Dataverse connector, TDS, long-term retention; PITR restores creates/deletes only; partition key immutable; GA status unresolved
- **Classification:** TRADE-OFF / CONSTRAINT · **Origin:** MS
- **Evidence:** "Dataverse elastic tables use Azure Cosmos DB." Use standard when "strong data consistency … transactional capability across tables … complex joins." "Each logical partition can store 20 gigabytes (GB) of data." "If you don't set a partitionid value for each row, the value remains null, and you can't change it later." "Elastic tables don't support multi-record transactions." [DV:S03]. Not supported: "Business rules; Charts; Business process flows; One Dataverse connector for Power BI; Many-to-many (N:N) relationships to standard tables; Alternate key; Duplicate detection; Calculated and rollup columns; … Table sharing; Composite indexes; Cascade operations". "Point in time restore doesn't restore 'updated' records". "Use bulk operation messages. This allows you to achieve 10 times the throughput" [DV:S24]. "The TDS endpoint can't be used with elastic tables." [DV:S14]. LTR: "audit tables and elastic tables aren't supported" [DV:S02]. "known issues with elastic tables should be addressed before this feature becomes generally available" [DV:S03, 2026-08] (C-02; alternate-key support conflicted, C-03).
- **Why it matters:** The in-platform answer to telemetry/event/log data is a different database with a different consistency and recovery model; it must be split from master/transactional data.
- **Decision impact:** Requirement "high-volume, time-bounded events" → constraint: elastic semantics → implication: split model (elastic with TTL for events; standard for master/transactional); replicate to lake for BI; never transactional entities on elastic.
- **Confidence:** HIGH (facts) / LOW (GA) · **Sources:** DV:S02, DV:S03, DV:S14, DV:S24, PS-57

#### DA-10 — Write patterns and throughput: service protection is per user per web server (6,000 requests / 20 min execution / 52 concurrent per 5-min window); web-server count scales with licences; batching does not bypass entitlements; Microsoft's remedy for nightly bulk jobs is "move towards real-time integration"
- **Classification:** CONSTRAINT / RECOMMENDATION · **Origin:** MS
- **Evidence:** "Each web server that your environment makes available enforces these limits independently. Most environments have more than one web server. Trial environments allocate only a single web server … One of the factors is how many user licenses you purchase." "Service protection limits don't apply to data operations that originate from plug-ins … However, the extra computation time … is added to the initial request". "Batch operations aren't a valid strategy to bypass entitlement limits." "Most scenarios are fastest sending single requests with a high degree of parallelism." "If your current business processes depend on large periodic nightly, weekly, or monthly jobs … consider how you might enable a real-time data integration strategy." "Let the server tell you how much it can handle" [DV:S13, EX:S18]. Bulk ops: "The type of table you choose … has the greatest impact on how much throughput"; "synchronous plug-ins that exceed two seconds to run seriously degrade performance"; bulk APIs "Not currently available for all tables … Any error … causes the entire operation to fail" [DV:S27]. Daily entitlements: 40,000 (Premium) / 6,000 (per app, M365) / 250,000 (Process); non-licensed pool "25,000 base requests" for Power Apps-only tenants; retention runs, plug-ins and workflows all count [DV:S06, DV:S02].
- **Why it matters:** Throughput is a licensing-shaped envelope, not a knob; write amplification (plug-in cascades, audit, retention sweeps, integration users) burns two separate budgets.
- **Decision impact:** Requirement "sync N rows/day" or "initial load of millions" → constraint: per-identity 5-min window + daily entitlement → implication: delta-based continuous sync, parallel application users guided by the DOP header, small batches, Retry-After compliance, staging in elastic/plug-in-light tables, validated data before load (bulk APIs fail-all).
- **Confidence:** HIGH · **Sources:** DV:S06, DV:S13, DV:S27, EX:S17, EX:S18, PS-18, PS-19

### 4.2 Dataverse as the application store

#### DA-11 — Security model is a storage and performance decision: sharing is "less performant" and exception-only; every share/access-team/cascade writes PrincipalObjectAccess rows that cannot be deleted directly; default Reparent = Cascade All is the main bloat driver; hierarchy security ≤ 50 users per manager
- **Classification:** RISK / ANTI-PATTERN / RECOMMENDATION · **Origin:** MS (+T4 magnitudes)
- **Evidence:** "It should be an exception, though, because it's a less performant way of controlling access. Sharing is tougher to troubleshoot". "Access teams are more performant". "Column-level security should be used as needed and not excessively" [DV:S11]. POA: "all sharing of records and their permissions are stored in the PrincipalObjectAccess (POA) table." "By default, the relationship of the Reparent option is set to Cascade All. All related subrecords are shared to the owner of the parent record." "Direct deletion on this table is not supported … The correct way to clean up the POA table is by adjusting the security model" [DV:S26]. "Keep the effective hierarchy security to 50 users or less under a manager or position." "Avoid creating a large number of business units." [DV:S12]. T4: POA "from over 100 GB to less than half a GB" after Reparent → Cascade None [DV:S29].
- **Why it matters:** Access requirements expressed as "ad-hoc, per-record, many-to-many" force sharing → POA growth on the database meter and on the hot path of every access check. "By org unit" maps to BU + roles; "manager sees team" to hierarchy security; "collaborators per record" to access teams.
- **Decision impact:** Requirement "collaboration across teams on records with many child rows" → constraint: cascade share/reparent multiplies POA per child → implication: referential relationships (Cascade None on Share/Reparent) unless inheritance is required; team ownership; access teams with unshare lifecycle; column security scoped to PII.
- **Confidence:** HIGH (T1) / MEDIUM (T4 magnitudes) · **Sources:** DV:S11, DV:S12, DV:S26, DV:S29, XC:S37, XC:S38

#### DA-12 — Ownership type (organization vs user/team) is immutable at table creation; privileges are strictly additive; Owning Business Unit is immutable unless Modernized BUs; BUs/teams are per environment and not solution-portable; changing a user's BU can strip roles and move records
- **Classification:** CONSTRAINT / DECISION CRITERION · **Origin:** MS
- **Evidence:** "Organization owned, and User or Team owned. This is a choice that happens at the time the table is created and can't be changed." "all privilege grants are accumulative with the greatest amount of access prevailing. If you gave broad organization level read access to all contact records, you can't go back and hide a single record." "Business Units and Teams must be created and managed in each environment". Sync jobs including owningbusinessunit fail "with a Foreign KEY constraint violation if the target environment doesn't have the same Owning Business Unit value" [DV:S11]. "If you later determine that your custom table must be of a different type, you need to delete it and create a new one." [XC:S22]. "By changing the business unit for a user, you can remove all security role assignments for the user." Record reassignment "is a sequential action, where if the transfer of records of the first entity fails, all subsequent entities will not be transferred" [XC:S39].
- **Why it matters:** The single irreversible security decision per table; organization-owned tables that later need segmentation force rebuild + migration. Mapping BUs 1:1 to a volatile org chart makes every re-org a data-migration event.
- **Decision impact:** Requirement "row-level visibility by department/region, now or plausibly later" → user/team-owned at creation; organization-owned only for reference/config. Requirement "org volatility" → few, stable BUs; teams/hierarchy for the volatile part. Discovery must produce the visibility matrix per entity before schema.
- **Confidence:** HIGH · **Sources:** DV:S11, XC:S22, XC:S39, XC:S40

#### DA-13 — Dataverse for Teams: 2 GB combined DB+file (not extendable), no API, no record sharing, no copy/reset, Teams-only runtime; upgrade to Dataverse is one-way, needs tenant capacity and premium licences for all users
- **Classification:** CONSTRAINT / DECISION CRITERION · **Origin:** MS
- **Evidence:** "Each Dataverse for Teams environment provides 2 GB of combined database and file storage". "The 2 GB storage limit can't be extended further." "No direct API access to Dataverse for Teams is provided". "Record sharing isn't supported". Copy/Reset "Not available by default". Upgrade: "the tenant must have at least as much available capacity as the size of the Dataverse for Teams environment … Any apps running on the environment require Microsoft Power Platform (Power Apps, Power Automate) licenses" [DV:S18]. Licensing FAQ: "can store up to 1,000,000 records based on typical usage (enforced as 2 GB relational database storage …)" [SP:S-09]; "when a team is deleted, the associated environment is also deleted" [SP:S-21].
- **Why it matters:** The seeded relational middle ground between SharePoint lists and full Dataverse — a dead end for integration, growth, sharing or ALM.
- **Decision impact:** Requirement "team-scoped, self-contained app, seeded licences" → STRONG; any of API / > 2 GB / sharing / multi-env ALM / audience outside the team → start on full Dataverse.
- **Confidence:** HIGH · **Sources:** DV:S18, SP:S-09, SP:S-21, PS-16

#### DA-14 — Binary placement: Microsoft itself moves attachments/notes to file storage; file/image columns are the sanctioned pattern (file ≤ 131,072 KB, immutable after save; images converted to JPG, ≤ 30,720 KB); file uploads bypass form save semantics
- **Classification:** PATTERN / CONSTRAINT · **Origin:** MS
- **Evidence:** "File-type data such as 'Annotation' and 'Attachment' is moving from database to file storage." [DV:S01]. "The default Maximum file size is 32 MB, and the largest size you can set by using the designer is 131,072 KB". "You can't change the maximum file size after you save it." "When you upload the image, it's converted to a .jpg format". "File columns don't work with business process flows, business rules, charts, rollup columns, or calculated columns." "deleting or uploading a file on a form happens immediately, not on form save." [DV:S10]. Storage-management guidance: "consider offloading attachments" [DV:S28].
- **Why it matters:** Originals > 131 MB or lossless images cannot live in Dataverse; file placement is the first cost lever (DA-04); file-column uploads are outside the record transaction.
- **Decision impact:** Requirement "documents attached to records" → file/image columns (keeps Dataverse row security; file meter) or SharePoint/Blob with reference (loses Dataverse security, gains labels/versioning) → decided by confidentiality granularity (DA-59).
- **Confidence:** HIGH · **Sources:** DV:S01, DV:S10, DV:S28

#### DA-15 — Column limits and types: Text 4,000 chars; Multiline 1,048,576; filterable text must be ≤ 850 chars or it is a "large text column" that cannot be indexed; canvas apps lack decimal and BigInt; schema name and data type are immutable after save; deleting a column deletes its data
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** [DV:S10] type limits. "You can use conditions on string columns that have a MaxLength configured for fewer than 850 characters … Large text columns are too large to effectively index" [DV:S42]. "Canvas apps don't currently support decimal type numbers"; "Big and BigInt aren't supported in canvas and model-driven apps." [DV:S10]. "Once a column is saved, you can't change the data type except for converting text columns to autonumber columns." "When you delete a column, any data stored in the column is lost." "If you remove an option which has been used by an entity record the data for that record will become invalid" [DV:S33].
- **Why it matters:** Schema changes in production are additive-only in practice; type migrations are add-migrate-retire; filter columns must be designed short.
- **Decision impact:** Requirement "evolving model" → data-model review gate before first production import (types, lengths, ownership, file sizes, choice sets). Requirement "financial precision in canvas" → compute server-side.
- **Confidence:** HIGH · **Sources:** DV:S10, DV:S33, DV:S42

#### DA-16 — Auditing: log meter; default retention Forever; retention changes not retroactive; 5 KB truncation; no export UI; read/export access is not audited in Dataverse (Purview, production only); from May 2026 Purview receives no field values; CMK environments cannot set audit retention
- **Classification:** FACT / RISK · **Origin:** MS
- **Evidence:** "Dataverse stores audit logs and they consume log storage capacity." "Default: Forever". "Changing the retention period here doesn't change the retention period for already existing records." "auditing doesn't support retrieve operations or export operations." "Exporting audit logs isn't currently supported. Use the Web API or SDK". "Large attribute values … are limited to 5 KB". "The audit retention period isn't available … for environments encrypted with a customer's own encryption key." [DV:S19]. "Starting in May 2026, Dataverse will no longer include before-and-after field change values in the audit events that are sent to Microsoft Purview." [XC:S07]. Audit table excluded from TDS [DV:S14] and LTR [DV:S02]; Synapse Link can export it (Delta Lake profiles only) [XC:S43]. Single-record audit deletion needs "Delete Audit Record Change History" privilege [DV:S19].
- **Why it matters:** "Audit everything forever" silently grows the $10/GB meter; a compliance requirement stated as "N years" must be configured at go-live; audit reporting needs Synapse Link or API.
- **Decision impact:** Requirement "field-level audit for N years" → scope audited tables/columns; set retention at environment creation; plan Synapse Link audit export; CMK → deletion jobs instead of policy.
- **Confidence:** HIGH · **Sources:** DV:S02, DV:S14, DV:S19, XC:S07, XC:S43

#### DA-17 — Long-term retention: Managed Environments required; one-way, read-only (Advanced Find / flow / OData); ~50% database saving on average; zero file saving; audit and elastic tables excluded; policy runs consume API requests and take 72–96 h; retained data not portable in solutions
- **Classification:** FACT / CONSTRAINT / TRADE-OFF · **Origin:** MS
- **Evidence:** "must be a Managed Environment … policies are disabled" otherwise. "Once data is retained … it can't be moved back to the Dataverse live (active) application state." "Every GB moved … consumes, on average, 50% less database capacity." "For file and image attachments, Dataverse long term retention doesn't reduce capacity consumed." "audit tables and elastic tables aren't supported". "All the existing delete action cascade relationships and plugins for tables are executed when a data retention policy is run" [DV:S02, XC:S08]. Synapse Link FAQ: "designed for analytics purposes. We recommend customers use long-term-retention for archive purposes." [XC:S43]. Fabric relink: "shortcuts include live data only. Retained data is no longer surfaced" [XC:S31].
- **Why it matters:** LTR halves, not eliminates, cold relational cost; does nothing for attachment-heavy history; retained rows leave live views/TDS/Power BI; history reporting needs an analytical copy taken beforehand.
- **Decision impact:** Requirement "7–10 years of closed records, M months active" → Managed Env + read-only history via Advanced Find/OData, or external archive for attachments-heavy history; define the "inactive" criterion early; take the lake copy before retention.
- **Confidence:** HIGH · **Sources:** DV:S02, XC:S08, XC:S31, XC:S43

#### DA-18 — Backups and recycle bin are not archives: backups ≤ 7 days (28 for production Managed Environments), same region, not downloadable, exclude audit by default, need 1 GB free capacity; recycle bin opt-in, 1–30 days, deletes only, not for elastic/virtual/600+-attribute tables
- **Classification:** FACT / CONSTRAINT · **Origin:** MS
- **Evidence:** "the system retains backups … for seven days. However, for production managed environments, you can extend the retention period up to 28 days". "You must restore an environment in the same region". "You can't get a copy of your database backup." "You can't directly restore backups to production environments." "To restore an environment, you need 1 gigabyte (GB) of free capacity." [XC:S11]. Recycle bin: "between 1 and 30" days; "You can only restore records deleted after the setting is turned on."; unsupported "Virtual tables … Elastic tables; Tables with more than 600 attributes" [XC:S10].
- **Why it matters:** "We can always restore" for records deleted months ago is false; point-in-time recovery beyond four weeks or an offline DB copy is not available from the platform.
- **Decision impact:** Requirement "recover accidental deletes" → enable recycle bin at creation (30 d). Requirement "legal hold / PITR > 28 d / offline copy" → role privileges (no delete) + LTR + analytical copy; keep ≥ 1 GB capacity headroom.
- **Confidence:** HIGH (mechanics) / MEDIUM (recycle-bin GA wording, U-06) · **Sources:** XC:S10, XC:S11

#### DA-19 — Analytical copy path 1 — Link to Fabric: no ETL, no BYO storage, but the delta-parquet replica bills as Dataverse *database* storage; all change-tracked tables added by default; one Fabric workspace per environment; Fabric capacity in-geo required; up to 60 min latency; ≤ 2,000 active tables; low-latency engine migration drops retained data from shortcuts
- **Classification:** TRADE-OFF / CONSTRAINT · **Origin:** MS (+T4 cost signals)
- **Evidence (spot-checked by consolidator 2026-09-02, ms.date 2026-07-06):** "the system creates an optimized replica of your data in delta parquet format … using Dataverse storage". "Tables added to OneLake consume Dataverse storage". "Enabling this feature results in an increase in **Dataverse database** storage consumption … you notice an additional file `Account-Analytics`". "Today, a Dataverse environment links to a single Fabric workspace." "the system adds all nonsystem Dataverse tables that have the **Track changes** property enabled." Comparison table: "No copy, no ETL" vs "Consumes additional Dataverse storage." "Microsoft continues to invest in Link to Fabric as the primary sync path" [DV:S17, XC:S04]. "A Power BI premium license or Fabric capacity within the same Azure geographical region … is required." "It might take up to 60 minutes to update data in OneLake". "If you have more than 2,000 active Dataverse tables, Link to Fabric can fail". "After you relink, the shortcuts include live data only." [XC:S31]. Storage-management guidance: analytics "can double or triple your storage footprint" [DV:S28]. T4 (snippet only): practitioners report bill shock at "$40/gig/month" [XC:S52].
- **Why it matters:** The strategic analytics path converts analytics into the meter that cannot be offset (DA-04). "No copy" is accurate only in the sense of "no copy outside Dataverse-managed storage" (C-06).
- **Decision impact:** Requirement "Fabric/Power BI Direct Lake analytics" → budget database capacity ≈ + replica of linked tables (magnitude UNKNOWN, U-01); select tables explicitly; compare with Synapse Link to own ADLS at volume; do not rely on Fabric shortcuts for retained history during the engine transition.
- **Confidence:** HIGH (mechanism) / LOW (magnitude) · **Sources:** DV:S17, DV:S28, XC:S04, XC:S31, XC:S44, XC:S52

#### DA-20 — Analytical copy path 2 — Azure Synapse Link: free Dataverse feature (Azure costs only), push-based CUD replication, requires Track changes; ADLS Gen2 + Synapse in same region and tenant; incompatible with data-exfiltration protection / managed VNet workspaces; ≤ 10 profiles per environment; "near real-time can't be guaranteed" under high churn; secured columns export as null unless the lake app user is in the profile; notes file content not synced; type change = unlink/relink; deletes replicate
- **Classification:** PATTERN / CONSTRAINT · **Origin:** MS
- **Evidence:** "The tables you want to export via Azure Synapse Link must have the Track changes property enabled." "Synapse workspaces featuring managed private endpoints, data exfiltration protection, or managed virtual networks aren't supported." "limited to a maximum of 10." "In these high-volume scenarios, data availability in near real-time can't be guaranteed." [DV:S16, XC:S30]. FAQ: "Azure Synapse Link is a free feature with Dataverse … consider potential costs for the Azure service". "If the application user isn't added to the profile that secures the column … the secured column is exported as null." "doesn't sync file content stored on the annotation (Notes) table." "Changing the data type of a column is a breaking change and you need to unlink and relink." "Append only mode is the recommended option … when the data volumes are high" [XC:S43]. "All create, update, and delete operations are exported" [XC:S03]. Data Export Service EOL Nov 2022 [DV:S35, XC:S07].
- **Why it matters:** Microsoft's sanctioned OLTP→OLAP separation; it needs an Azure landing zone whose security posture is compatible, schema discipline (change tracking, frozen types), and a deliberate decision on column security in the lake (nulls vs widened exposure).
- **Decision impact:** Requirement "enterprise lake/warehouse feed" → enable Track changes at design; align Azure landing zone (public-network Synapse or Fabric link); treat lake as eventually consistent; "append only" conflicts with GDPR erasure (DA-60).
- **Confidence:** HIGH · **Sources:** DV:S16, DV:S35, XC:S03, XC:S07, XC:S30, XC:S43

#### DA-21 — Direct reporting on Dataverse: TDS endpoint is read-only SQL emulation (Entra-only, 5-min timeout → 2 min with `SELECT *`/JOINs, service-protection limits, no file/audit/virtual/elastic tables, bypasses retrieve plug-ins); Power Query Dataverse connector "mostly suited toward analytics workloads, not bulk data extraction" (~500 rows/s guideline); DirectQuery adds a 4-min / 1M-row layer
- **Classification:** CONSTRAINT / DECISION CRITERION · **Origin:** MS
- **Evidence:** "The SQL connection provides read-only access". "there's a fixed five (5) minute timeout … queries containing SELECT *, NESTED FROMs and/or JOINs automatically adjust the timeout limit to two (2) minutes". "Queries using the TDS endpoint execute under the service protection API limits." "Querying data using SQL doesn't trigger any plug-ins registered on the RetrieveMultipleRequest". "Consider using data integration tools such as Azure Synapse Link for Dataverse and dataflows for large data queries" [DV:S14, XC:S02]. "To use the Dataverse connector, the TDS endpoint setting must be enabled … TCP ports 1433 or 5558". "most default tables are retrieved at a rate of approximately 500 rows per second". "Both the Dataverse connector and the OData APIs are meant to serve analytical scenarios where data volumes are relatively small." [XC:S01]. DirectQuery: "Use import by default." "One million row intermediate result limit." "The service enforces a 4-minute timeout per query." "Unless SSO is configured, DirectQuery uses configured stored credentials for all viewers." [XC:S32].
- **Why it matters:** TDS is a convenience for ad-hoc/small BI, not an analytics or integration backbone; any confidentiality implemented in retrieve plug-ins is bypassed by TDS.
- **Decision impact:** Requirement "BI over Dataverse" → small/medium, filtered, per-user operational views → TDS/DirectQuery acceptable; large/historical/org-wide → Fabric link / Synapse Link (DA-19, DA-20). Requirement "masking via plug-in" → use column security / masking rules instead.
- **Confidence:** HIGH · **Sources:** DV:S14, XC:S01, XC:S02, XC:S32, SQ:S12

#### DA-22 — Security does not travel into reporting copies: TDS/DirectQuery honour Dataverse roles per user; Fabric/Synapse copies need RLS rebuilt and export secured columns as null; embedded Power BI in model-driven forms ignores app security roles; SharePoint-list reports show the connection owner's view
- **Classification:** CONSTRAINT / RISK · **Origin:** MS
- **Evidence:** "The Dataverse endpoint SQL connection uses the Dataverse security model for data access." [XC:S02]. "the secured column is exported as null" unless the lake app user is in the profile [XC:S43]. Embedded Power BI: "Power Apps security roles and privileges don't affect the data that is displayed … use Row-level security (RLS) with Power BI." [XC:S47]. SharePoint list in Power BI: "The Power BI view of the SharePoint list data is determined by the permissions of the account used to establish the Power BI connection" [SP:S-28]; sensitivity label "isn't inherited by the semantic model" [SP:S-28].
- **Why it matters:** "Embed the report and security follows the app" is false; two security models must be kept in sync, and per-principal column security conflicts with per-workspace lake security (C-07).
- **Decision impact:** Requirement "reports respect record/column visibility" → DirectQuery/TDS per-user identity for hot operational views; import/lake copies with RLS mirroring BU/team structure (maintenance cost) and an explicit decision on secured columns (nulls vs widened exposure).
- **Confidence:** HIGH · **Sources:** XC:S02, XC:S43, XC:S47, SP:S-28

#### DA-23 — Search is a finite, eventually consistent, database-billed resource: 1,000 searchable fields per organisation (lookups cost 3, choices 2), no related-table fields, indexed attribute ≤ 1,700 bytes, up to 15 min–days sync, 1 request/s per user; Quick Find columns create indexes on the database meter; leading-wildcard `contains` queries are throttled
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** "the maximum is 1,000 searchable fields for an organization, you can configure up to 950". "Dataverse search doesn't support related table fields". "Changes … might take up to 15 minutes to appear … a couple of days for large-size organizations." "Dataverse search must be turned on to support lifecycle operations" [DV:S34]. "Admin-configured Quick Find values can increase the size of the indexes"; "Eliminate multiline text columns from inclusion." "The DataverseSearch table … stores indexed data for the global search and generative AI experiences." [DV:S01]. "Dataverse can't take advantage of database indexes when a query using leading wild cards"; "Use Dataverse search instead." [DV:S42]. Search API "one request per second for each user" [DV:S13].
- **Why it matters:** "Search across everything" is a design artefact with a budget and a cost; free-text `contains` in grids is throttled at scale.
- **Decision impact:** Requirement "full-text search across many wide tables / near-real-time search" → constrain searchable fields and Quick Find columns; route free-text to Dataverse search; do not promise real-time search.
- **Confidence:** HIGH · **Sources:** DV:S01, DV:S13, DV:S34, DV:S42

#### DA-24 — ALM moves schema, not data: deleting a managed solution deletes its tables' data; reference/config data moves via Configuration Migration tool (uniqueness condition; no images/Calendar) or dataflows (alternate keys, parent-before-child, no N:N, no Status); solution ≤ 95 MB; BUs/teams/retained data not portable
- **Classification:** CONSTRAINT / PATTERN · **Origin:** MS
- **Evidence:** "When you delete a managed solution, the following data is lost: data stored in custom tables … and data stored in custom columns that are part of the managed solution on other tables" [DV:S23]. CMT: "Configuration data is different from end user data"; "Migrating the Calendar entity is not supported. Migrating the Image column is not supported." [DV:S22]. Dataflows: "you must create an alternate key in the parent table before you can set a lookup column on the child table." "You can't import many-to-many relationship data." "You can't map to Status and Status Reason fields." [DV:S31]. Environment variables: "Yes if your configuration data isn't relational … Other tools such as the Configuration migration utility are better suited for migration of relational configuration data" [EX:S34].
- **Why it matters:** Config-driven apps need a deterministic data pipeline keyed on natural/alternate keys; solution removal is a data-loss event.
- **Decision impact:** Requirement "lookup lists / rules tables owned by the app" → custom tables with alternate keys + CMT; "key:value per environment" → environment variables; "static enumerations" → choices; never uninstall managed solutions holding production data without export.
- **Confidence:** HIGH · **Sources:** DV:S22, DV:S23, DV:S31, EX:S34, EX:S35

#### DA-25 (REVISED in v2 — v1's blanket "no cross-environment queries" claim was contradicted by a Microsoft page; see review F-02) — Environment is the boundary for *relationships*, entitlements, security config, backups, CMK, VNet, retention and Fabric/Synapse links — but NOT for canvas-app *reads*, which can explicitly target another environment; copy is sandbox-only, same tenant/region, hours-long, brings PII in "Everything" mode, excludes audit by default
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence — the correction:** "Connect to Microsoft Dataverse" (canvas apps, ms.date 2025-06-19): "By default, the app connects to the current environment for Dataverse tables. If your app moves to another environment, the connector connects to data in the new environment." "If you select **Change environment**, specify a different environment to pull data from instead of, or in addition to, the current environment." "Even if you see an environment in the list, the security roles in the environment control what you can do there. For example, if you don't have read privileges, you can't see the tables and records in the environment." A canvas app can therefore be built to read (and, subject to security roles, write) tables in a *different* environment than the one it runs in — cross-environment relationships/joins/lookups still do not exist, because a Dataverse relationship is metadata defined within a single environment's schema, and the connector exposes each environment's tables as a separate, unrelated data source in the app.
- **Evidence — what remains a genuine environment boundary:** "These entitlements are only granted within a single database and are individually tracked in each Dataverse database." "Business Units and Teams must be created and managed in each environment" [DV:S11]. "You can only copy to an environment in the same tenant and region." "you can't overwrite production environments". "Components that have not been added to a solution … might not be part of the copy." "Copying audit logs can significantly add to the time … by default isn't done." Schema-only copy truncates Account, Contact, Annotation, Attachment, Audit, PrincipalObjectAccess, WorkflowLog [DV:S21]. "Today, a Dataverse environment links to a single Fabric workspace." [DV:S17]. "Each Power Platform environment is linked to one virtual network subnet." [XC:S17].
- **Why it matters:** The v1 conclusion — "a shared master-data environment is not a Dataverse pattern" — was too strong. It IS possible for several canvas apps in different environments to read a common reference/master-data environment directly through the Dataverse connector, at the cost of: no native relationships to the local schema (must be modelled as an unenforced lookup key, or the master row copied/cached locally), separate security-role configuration per environment, and no cross-environment ALM story (the "Change environment" pointer is app-level configuration, not solution metadata). "One environment per department/country" still multiplies entitlements, BU/team config, backup/CMK/VNet scope and Fabric/Synapse links — those remain genuinely per-environment.
- **Decision impact:** Requirement "several apps in different environments must read one master-data source" → constraint: cross-environment reads are supported per app (not per relationship) → implication: viable pattern for read-only reference data with a documented security-role and ALM plan per consuming environment; NOT viable for a native relationship, cascade, or shared security model — those still require co-location (solution segmentation) or replication (dataflow/virtual table, DA-31/DA-45). Requirement "realistic test data without PII" → post-copy anonymisation or synthetic data via CMT/dataflows. Choose environment strategy on data requirements before app design.
- **Confidence:** HIGH (both the correction and the remaining boundary statements are directly quoted) · **Sources:** DV:S11, DV:S17, DV:S21, XC:S17, XC:S42, connection-common-data-service (ms.date 2025-06-19, re-fetched in the v2 revision pass)

#### DA-26 — Physical tuning is not an architect's lever: indexes are platform-managed (automatic tuning and query optimisation on by default; query hints "only when recommended by Microsoft technical support"); the levers are schema (alternate keys, ≤ 850-char filter columns, Quick Find columns) and query shape; known anti-patterns (leading wildcards, filters on computed columns, sort by choice/related columns) are throttled by the platform
- **Classification:** CONSTRAINT / ANTI-PATTERN · **Origin:** MS
- **Evidence:** "all Dataverse stores have tuning enabled by default." [DV:S01]. "Automatic query optimization doesn't require any configuration." [DV:S44]. "Only apply these options when recommended by Microsoft technical support." [DV:S45]. "Dataverse heavily throttles queries that use known query anti-patterns"; common causes "a saved query used in a grid or a query executed by a plug-in"; "data integration that moves a large amount of data" [DV:S43]. "ordering on choice columns requires more compute"; "Ordering by columns on related tables makes the query slower" [DV:S42]. "When possible, queries should order on the primary key" [DV:S04].
- **Why it matters:** Unlike SQL, a performance risk on a very large standard table cannot be mitigated by "adding an index" later; whether support creates indexes on request is not documented (U-08).
- **Decision impact:** Requirement "sub-second filtered queries on tens of millions of rows by arbitrary columns" → constrain filter/sort columns at design time (alternate keys, short text, denormalised sort keys) or use elastic (partition-key access) / analytical store for arbitrary slicing; treat this as a SQL-favouring signal.
- **Confidence:** MEDIUM · **Sources:** DV:S01, DV:S04, DV:S42, DV:S43, DV:S44, DV:S45

#### DA-27 — Storage hygiene is operational design: system tables (workflow logs, async ops, duplicate-record copies, import jobs, traces) grow on the database meter; storage reports lag 72 h; over-capacity blocks create/copy/restore (1 GB minimum) and carries contractual suspension risk; each full sandbox copy "Replicates the full data and index footprint"
- **Classification:** RISK / RECOMMENDATION · **Origin:** MS
- **Evidence:** Growers: WorkflowLogBase, AsyncOperationBase, DuplicateRecordBase, ImportJobBase, BulkDeleteOperationBase, TraceLogBase; "The system can take up to 72 hours to update storage information."; "You can't restore your data once you delete it." [DV:S20]. "The following administrative environment lifecycle operations aren't available when the required storage capacity isn't available: Create a new environment (requires minimum 1-GB capacity available); Copy an environment; Restore an environment". "Microsoft might suspend use of the online service." Notifications at "less than 15% of capacity available" [DV:S01]. "Environment sprawl is a major driver of storage cost and complexity." "Search indexes … may persist unless explicitly removed." "system-generated logs, including audit logs and plug-in trace logs, are counted against the customer's storage entitlement." [DV:S28].
- **Why it matters:** Data growth does not break the app; it breaks ALM (sandbox refresh) and compliance first. Lifecycle jobs are run-book items that must be designed in.
- **Decision impact:** Requirement "predictable storage cost with N environments" → cost model = production footprint × (1 + full-copy sandboxes) + analytics replica; schema-only copies; search/audit off in non-prod; recurring bulk-delete jobs; pre-authorised PAYG or tenant pool headroom.
- **Confidence:** HIGH · **Sources:** DV:S01, DV:S20, DV:S28, DV:S46

### 4.3 SQL Server / Azure SQL

#### DA-30 — Schema conformance gates the SQL option: PK required for writes (no tinyint/smallint), server-side triggers break connector Insert/Update, flow triggers need IDENTITY + ROWVERSION, unsupported types (binary, varbinary, image, rowversion, hierarchyid, sql_variant, xml, spatial), OData-conformant identifiers, views read-only, > 30 MB fields cause 504s
- **Classification:** DECISION CRITERION (pre-decision checklist) · **Origin:** MS
- **Evidence:** "Insert and update to a table won't work if you defined a SQL server-side trigger on the table." "A Primary Key is required for the following operations: GetItem, PatchItem, DeleteItem". "When an item is modified (V2) | A ROWVERSION column is required." "When an item is created (V2) | An IDENTITY column is required." "SQL views don't support primary key". "Database schema that do not conform to OData standard identifiers are not supported". "It is not recommended to store large amounts of data (more than 30 megabytes) in the target table fields" [SQ:S1]. "'tinyint' and 'smallint' are not supported as primary keys." Unsupported types list [SQ:S2]. "If a SQL Server table doesn't have a primary key, the data is read-only." "Views only support queries—not updates." [SQ:S3]. Virtual tables over SQL: "GUID or an integer field as the primary key"; "String primary keys are supported only if the values can be parsed as GUID"; unsupported "Time, Datetime2, Image, Geometry, Geography, RowVersion, Choice" [SQ:S7].
- **Why it matters:** "We already have the database" is an advantage only if the schema passes; legacy schemas with DML triggers (audit, cascades) cannot be written through the connector; vendor-owned databases that cannot be altered degrade to read-only or API-fronted.
- **Decision impact:** Requirement "reuse existing SQL schema" → schema audit before Options; classify tables direct-use / view-wrapped / SP-only / not exposable; add ROWVERSION/IDENTITY where flows must fire; writes via stored procedures where triggers exist.
- **Confidence:** HIGH · **Sources:** SQ:S1, SQ:S2, SQ:S3, SQ:S7

#### DA-31 — SQL is delegable but partially: text range comparisons, `IsBlank`, `Search` on numbers, `Max/Min` on dates not delegable; date predicates fail through the on-prem gateway (integer date key workaround); `char/nchar` pitfalls; stored procedures are un-paged actions with static schema, no `Refresh()`, called whenever the control refreshes
- **Classification:** CONSTRAINT / PATTERN · **Origin:** MS
- **Evidence:** Delegation table [SQ:S2]: `<, <=, >, >=` on Text "No"; `IsBlank` "No"; "Direct date filters don't work for SQL Server with an on premise Data Gateway." "Don't use char/nchar on SQL server". "The following data types can't be used as query option predicates: date, datetime, datetime2, smalldatetime" [SQ:S1]. Stored procedures: "Check a stored procedure as safe only if: 1. There are no side effects … You can't control when the stored procedure is called. 2. The stored procedure returns a modest amount of data … They aren't automatically paged … bring in fewer than 2,000 records." "The schema of the return values … should be static". "Refresh() only works with tabular data sources". "Power Automate handles asynchronous actions best." [SQ:S3]. Conflict with older security page "Power Apps doesn't currently connect to stored procedures" (C-08).
- **Why it matters:** "SQL handles large data" is true for the delegable subset; SPs solve delegation/trigger/security problems but move paging, filtering and refresh to the maker.
- **Decision impact:** Requirement "large relational tables in the app" → canvas-facing schema (views/SPs with pre-computed columns, varchar, integer date keys for gateway, no BLOBs); SPs accept paging/filter parameters, side-effect-free for reads; long-running SPs via Power Automate.
- **Confidence:** HIGH · **Sources:** SQ:S1, SQ:S2, SQ:S3, SQ:S14

#### DA-32 — Connector throughput is capped independently of the SQL engine: flows 100 CRUD calls / 10 s and 125 concurrent per connection (500 / 200 for native SP/query); apps 300 calls / 30 s per user; time-based connectionID throttling; 110-second action timeout; Power Apps request 180 s / 4 retries
- **Classification:** CONSTRAINT · **Origin:** MS (spot-checked by consolidator 2026-09-02)
- **Evidence:** Throttling table: "Logic Apps & Power Automate | Shared Environment | CRUD | API calls per connection | 100 | 10"; "Native | API calls per connection | 500 | 10"; "CRUD | Concurrent calls per connection | 125"; "Power Apps | … | API calls per user | 300 | 30"; "Power Apps | … | Concurrent calls per connection | 125". "connectionID level throttling is also applied based on total time spent by previous requests". "if a connection makes 200 calls at the same time, and each call takes 50 seconds to execute, all other calls will fail with a 429 error for the next 50 seconds." "If the execution time exceeds 110 seconds for a SQL query or stored procedure, actions will time out." [SQ:S1]. Power Apps: "Timeout | 180 seconds"; "Retry attempts | 4" [SQ:S33]. T4 signal: 504s tied to Azure SQL DTU micro-bursts on an S1 tier [SQ:S27].
- **Why it matters:** "High transaction volume" does not translate to SQL capacity; a per-row flow loop is capped at 100 calls per 10 s; implicitly shared connections make the whole user base share ONE connection's concurrency budget; long-running work must be asynchronous.
- **Decision impact:** Requirement "high volume / batch" → set-based stored procedures, no per-row loops, Entra per-user connections to distribute connection IDs, ADF/dataflows for bulk. Requirement "interactive app on SQL" → size Azure SQL for peak, sub-110-s calls, treat timeouts as an architecture signal.
- **Confidence:** HIGH (limits) / LOW (T4 root cause) · **Sources:** SQ:S1, SQ:S13, SQ:S27, SQ:S33

#### DA-33 — Identity model is the structural security difference: implicit connections reuse the maker's SQL credentials for every user (and let users author new apps on them); secure implicit connections (GA Jan 2024) are hygiene, not a security model; only Microsoft Entra Integrated (explicit) connections give per-user identity at SQL — with RLS/DENY in the database; Windows auth via gateway "isn't secure"; guest users unsupported
- **Classification:** RISK / RECOMMENDATION / CONSTRAINT · **Origin:** MS
- **Evidence:** "Each time the end user runs the app, they're using the credentials the author created the app with." "end users can author new applications based on those connections." "You can't rely on the security of data through filtering or other client-side operations to be secure." "To securely filter data on the server side, use built-in security features in SQL Server such as row level security … This approach uses the Microsoft Entra user identity" [SQ:S5]. Windows Authentication: "This type of connection isn't secure because it doesn't rely on end-user authentication … the connector has access to all of the data on that data source". Secure implicit: "Column names aren't hidden." "If you have permissions to Put, then you have access to Post." "known issue when importing an implicitly shared secure connection via a connection reference. The security isn't set properly in the target environment." [SQ:S22]. "Microsoft Entra ID guest users aren't supported for Microsoft Entra ID connections to SQL Server." [SQ:S1]. Generic: "The permissions that you grant through the user interface of your app don't deny the data source permissions that the user has." [XC:S42].
- **Why it matters:** Dataverse enforces row/column security per Entra user natively; SQL via connector enforces it only if the connection is explicit AND the database implements RLS/DENY; with SQL/Windows auth every user is the same principal.
- **Decision impact:** Requirement "row/column security per user, external/guest users, or tenant-wide publishing" → Dataverse or an API layer with user tokens; Azure SQL + Entra Integrated + RLS acceptable for internal users; never rely on app-side filters; reject implicit SQL connections.
- **Confidence:** HIGH · **Sources:** SQ:S1, SQ:S5, SQ:S22, SQ:S25, SQ:S28, XC:S42

#### DA-34 — On-premises SQL through the gateway is a reduced feature set: 2 MB request / 8 MB response caps, no "Execute a SQL query (V2)", stored procedures lose OUTPUT parameters, return values, multiple result sets and dynamic schemas; results transit Microsoft cloud and spool on the gateway; stored credential regardless of user; gateway not available in India region
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** "The request size limit is 2 MB through on-premises SQL Server. The response size limit is 8 MB". "Output values for OUTPUT parameters aren't returned … Return value isn't available. Only the first result set is returned. Dynamics schemas aren't supported". "Execute a SQL query (V2) | Not supported for on-premises SQL Server or connections with gateway" [SQ:S1]. "The gateway has a 2-MB payload limit for write operations." "credentials aren't used for approximately 5 hours" after change [SQ:S8]. Architecture: "The results are sent from the data source back to the gateway and then to the cloud service." "data is temporarily stored on the gateway machine … spooling." "Regardless of the user, the gateway uses the stored credential to connect." [XC:S21]. "On-premises data gateways aren't available in the India region." [XC:S18].
- **Why it matters:** "Keep data on-prem" via gateway avoids cloud storage but not cloud transit; the SP contract must be redesigned for a single typed result set.
- **Decision impact:** Requirement "reuse on-prem SQL + stored procedures" → redesign SPs (single result set, fixed schema), or move to Azure SQL/Managed Instance + VNet, or front SQL with an API. Requirement "no transit of row data through Microsoft cloud" → not achievable with Power Platform.
- **Confidence:** HIGH · **Sources:** SQ:S1, SQ:S8, XC:S18, XC:S21

#### DA-35 — Business-critical gateway estate is an operating model: separate dev and prod clusters, ≥ 2 nodes per cluster, HA + load balancing (random distribution opt-in; primary-first by default), scale-out at CPU > 80% / > 40 concurrent queries, monthly releases (last six supported), recovery-key custody is "a significant business risk", "Microsoft doesn't investigate poor performance when a gateway … is overloaded"
- **Classification:** RECOMMENDATION / RISK · **Origin:** MS
- **Evidence:** [SQ:S26]: "Set up a minimum of two gateways per gateway cluster"; "We don't recommend that a single business-critical gateway cluster be used for an entire company"; thresholds "CPU is above 80% … Running more than 40 queries simultaneously on a single node"; "Without a recovery key, gateways can't be recovered". [SQ:S9]: "Each cluster can support up to 10 gateway members." "The gateway cloud service always uses the primary gateway in a cluster unless that gateway isn't available." [SQ:S10]: "8-core CPU; 8 GB of memory … SSD"; "Using an on-premises data gateway with private link enabled isn't supported." No published throughput figures per node (U-09).
- **Why it matters:** These are the concrete costs of "keep SQL on-premises" (4+ servers, patch pipeline, key custody, monitoring) that must appear in the option comparison against Azure SQL + VNet.
- **Decision impact:** Requirement "on-prem SQL for a business-critical app" → cost the gateway estate (servers, ops FTE, monitoring); if unaffordable, Azure SQL / Managed Instance migration becomes part of the option.
- **Confidence:** HIGH · **Sources:** SQ:S9, SQ:S10, SQ:S26, EX:S46

#### DA-36 — Private connectivity to Azure SQL requires Power Platform VNet support (Azure subscription linked to the tenant, subnets delegated in both paired Azure regions, 25–30 IPs per production environment, V2-only SQL actions, no on-prem gateway, public calls "start to break"); otherwise Azure SQL must allowlist regional service tags refreshed every 90 days; serverless auto-pause adds predictable transient failures
- **Classification:** PATTERN / CONSTRAINT / TRADE-OFF · **Origin:** MS
- **Evidence:** "you must associate an Azure subscription with the Power Platform tenant." "you need to delegate the virtual networks for both Azure regions". "allocate 25 to 30 IPs for production environments". "The calls to publicly available resources start to break." Supported connectors incl. "SQL Server … Custom connectors … Azure Key Vault … Azure Blob Storage … HTTP with Microsoft Entra ID" [SQ:S4, XC:S17]. SQL under VNet: "Any action outside of this list will return a '403 Unauthorized'"; "On-premise data gateway is not supported" [SQ:S1]. Allowlisting: "update the IP addresses allow listed in your inbound firewalls at least every 90 days"; "allow-list your regional PowerPlatformPlex service tag along with the existing AzureConnectors tags" [SQ:S23]. Serverless: "Retry logic for serverless databases is especially important because temporary connectivity errors due to auto-resume are predictable." [SQ:S11].
- **Why it matters:** "No public endpoint" is an environment-level architectural commitment with network-team ownership; the Managed Environments dependency of VNet support was not confirmed on the fetched page (U-10). SharePoint is not in the VNet list — it always reaches Power Platform over Microsoft public endpoints.
- **Decision impact:** Requirement "Azure SQL behind private endpoint" → dedicated VNet-linked environments decided up front; Managed Instance via Entra auth. Requirement "minimise Azure SQL cost for low-usage app" → explicit auto-pause decision (disable, long delay, or warm-up flow).
- **Confidence:** HIGH (facts) / MEDIUM (Managed Env dependency) · **Sources:** SQ:S1, SQ:S4, SQ:S11, SQ:S23, XC:S17

#### DA-37 — Microsoft's positioning of SQL beside Dataverse: Dataverse "abstracts away all infrastructure … which limits query flexibility and throughput compared to Azure-native database services"; for "high-throughput processing, complex analytical queries, or direct database control, use an Azure-native database service alongside Dataverse"; reference architecture uses SQL data warehouse + read-only virtual tables; canvas reference rule: new app + new storage → Dataverse; data that "can't be moved" → app over SQL
- **Classification:** DECISION CRITERION / PATTERN · **Origin:** MS
- **Evidence:** Azure Architecture Center [SQ:S17, EX:S10] as quoted; Dataverse "Distributed multiprimary writes: No"; "plan for governance across both control planes." Reference architecture: "A centralized data warehouse provides a governed source of reference data, which Microsoft Dataverse exposes through virtual tables." "Restrict access to the virtual tables to read access only." "Use the data warehouse for heavy processing, and keep only lightweight references in Dataverse" [SQ:S32]. "If you're building a new app and storage, consider using Dataverse." "If you have data in SQL Server that can't be moved, or your organization requires SQL Server, consider using Power Apps over SQL Server." [EX:S53].
- **Why it matters:** Clearest Tier-1 statement of the split: Dataverse for the app-facing, security-rich business layer; Azure SQL for throughput, analytics, engine control, region colocation. Frames "SQL vs Dataverse" as "which parts go where".
- **Decision impact:** Requirement "high-throughput / complex analytics / direct DB control / specific Azure region" → Azure SQL alongside Dataverse with an explicit sync path (Synapse Link, Fabric, dataflows, ADF) and dual governance (PPAC + Azure Policy).
- **Confidence:** HIGH · **Sources:** SQ:S17, SQ:S30, SQ:S32, EX:S10, EX:S53

#### DA-38 — Reporting on SQL: "Use import by default" (Pro ≤ 8 refreshes/day, Premium/PPU ≤ 48); DirectQuery only for freshness, source-RLS passthrough or "no persisted copy" (1M-row, 4-min, 10-connection limits; stored credentials unless SSO); licensing is neutral between SQL and Dataverse (both premium) — the real cost delta is Dataverse capacity vs Azure SQL tier + gateway + ops
- **Classification:** TRADE-OFF / DECISION CRITERION · **Origin:** MS
- **Evidence:** [SQ:S24/XC:S32] as quoted; "Stored procedure calls and common table expressions (CTEs) aren't supported in a way that allows folding in DirectQuery." Gateway DirectQuery "16-MB uncompressed data response limit" [SQ:S8]. Connector class: "Power Apps | Premium", "Power Automate | Premium", "Logic Apps | Standard" [SQ:S1]. "A standalone Power Apps or Power Automate plan license is required to access all Premium, on-premises, and custom connectors." [SP:S-09].
- **Why it matters:** Relative to Dataverse TDS (DA-21), SQL offers the real engine (indexes, views, unrestricted import); but real-time DirectQuery on the transactional DB competes with the app. Licence cost does not discriminate SQL from Dataverse; it discriminates both from standard connectors.
- **Decision impact:** Requirement "operational reporting" → SQL/warehouse + Power BI import with incremental refresh; "near-real-time or passthrough RLS" → DirectQuery with aggregations/SSO/read replica. Requirement "minimise cost" → compare Dataverse capacity add-ons vs Azure SQL tier + gateway + ops per volume and usage pattern; PAYG for wide, infrequent use in either store.
- **Confidence:** HIGH · **Sources:** SQ:S1, SQ:S8, SQ:S20, SQ:S24, SQ:S29, SQ:S31, SP:S-09

### 4.4 SharePoint lists / Microsoft Lists / Excel

#### DA-39 — SharePoint capacity is a query-shape limit: 30 million items per list, but a 5,000-item list view threshold that "can't be changed" in SharePoint Online; delegation to SharePoint is the narrowest of the delegable sources (`Not` never; ID only `=`; `IsBlank`/`Sort` not on text/complex; Person only Email/DisplayName; `StartsWith` not on Choice/Lookup subfields); flow `Get items` defaults to 100 and fails above 5,000 without pagination
- **Classification:** CONSTRAINT · **Origin:** MS (spot-checked by consolidator 2026-09-02)
- **Evidence:** "You can store up to 30 million items or files in a list or library." "For SharePoint, the LVT limit can't be changed, and is in place to allow users on shared tenants to always have good performance on queries." [SP:S-02]. "Expressions that are joined with And or Or are delegable to SharePoint. Not won't delegate." "SharePoint only supports the equal ('=') operation for delegation on an ID field." "Only Email and DisplayName are delegable in the Person data type." "SharePoint does not support delegation of StartsWith on subfields of Choice or Lookup complex types." Table: Sort on Complex "No" [SP:S-04]. "If you get an incomplete data set … this problem might by caused by delegation limits." [SP:S-03]. "The default item limit is 100"; "If you go beyond 5,000 item limit, Power Automate fails"; "you may observe that no records are returned if there are no items matching the filter query in the first 5000 items" [SP:S-34]. Generic delegation list (`Not`, `IsBlank`, `In`) is an upper bound; the connector table governs (C-09).
- **Why it matters:** A list with 50k rows works only if every view/filter is indexed and selective; common business queries (sort by status choice, "not assigned to me", ID ranges) are non-delegable → silently wrong results, not slow ones, once the list passes 500/2,000 rows.
- **Decision impact:** Requirement "a missing row is a business error" (registers, approvals, inventory) or "multi-criteria filters / sorting by categorical fields / negations" → SharePoint unsafe without engineering controls → Dataverse/SQL. SharePoint acceptable for simple equality filters on indexed scalar columns over small lists.
- **Confidence:** HIGH · **Sources:** SP:S-01, SP:S-02, SP:S-03, SP:S-04, SP:S-33, SP:S-34, XC:S45

#### DA-40 — Relational complexity in SharePoint: 12 lookup/person/metadata joins per view (flows `Get items`/`Get files` fail above 12 lookups); referential integrity is opt-in per lookup, delete-only ("Restrict delete" / "Cascade delete"), needs Manage Lists permission and stops working above the threshold; 8,000-byte row budget; Microsoft's own performance advice is to denormalise people columns and partition lists with "hundreds of thousands of records"; canvas apps cannot project columns
- **Classification:** CONSTRAINT / ANTI-PATTERN · **Origin:** MS
- **Evidence:** "Specifies the maximum number of join operations, such as those based on lookup, Person/Group, or workflow status columns" = 12 [SP:S-02]. "If your list/library has lookup columns, Get items and Get files actions support returning items with a maximum of 12 lookup columns. If your list or library exceeds this threshold, the flow in Power Automate fails." [SP:S-19]. "you can check Enforce relationship behavior then select either Restrict delete or Cascade delete." "You must have Manage Lists permission" [SP:S-07, fetched-summarised]. "there is a still an overall limit on the number of columns based on their storage size, up to a maximum of 8,000" bytes [SP:S-02]. "Avoid too many dynamic lookup columns … use static columns to keep email aliases or people's names." "the records … are retrieved and transmitted back to the client with all the columns defined in the list—even if the app doesn't use all of them." "Consider breaking up large lists" [SP:S-06].
- **Why it matters:** Microsoft's recommended mitigations (denormalise, shard one entity across lists) are the opposite of relational design and push integrity into the app. No FK on insert/update, no composite keys, no native N:N.
- **Decision impact:** Requirement "normalised business data with several FKs per entity" or "referential integrity" → SharePoint POOR; acceptable only for flat entities with ≤ 1–2 lookups. If partitioning is needed, the store is wrong.
- **Confidence:** HIGH (12-join, 8,000 bytes, perf guidance) / MEDIUM (S-07 wording, U-11) · **Sources:** SP:S-02, SP:S-06, SP:S-07, SP:S-19, SP:S-35

#### DA-41 — Excel is not a database (Microsoft's words): 2,000-row ceiling from limited delegation; Excel Online (Business) connector 25 MB max, file locked up to 6 minutes after use, "Simultaneous file modifications … are not supported", 30-second eventual consistency, duplicate inserts on retry, 256 rows/page default, 100 calls/min, one filter and one sort column; data must be a table; calculated columns unusable
- **Classification:** ANTI-PATTERN (as primary store) / CONSTRAINT · **Origin:** MS
- **Evidence:** "Excel isn't a relational database system … if the app requires heavy transactions, it can adversely affect the performance of the app." "it restricts the canvas app to loading data from the table only up to 2,000 records due to limited delegable functions." [SP:S-06]. "The maximum size of an Excel file … is 25 MB." "An Excel file may be locked for an update or delete up to 6 minutes since the last use of the connector." "Users should avoid writing data to a single Excel file from multiple clients concurrently … This can cause possible merge conflicts and data inconsistency." "Delays up to 30 seconds are expected". "data can be inserted multiple times because of retry policy." "In the case of multiple matches … only the first row will be updated/deleted." [SP:S-05]. "If your Excel data includes a calculated column, you can't use it to build an app" [SP:S-38].
- **Why it matters:** No row locking, no concurrency model, eventual consistency, duplicate risk — each disqualifying for a multi-user transactional store.
- **Decision impact:** Requirement "more than one concurrent writer" or "immediate durability" → Excel disqualified. Legitimate roles: seed import, static reference data, export target, single-writer files.
- **Confidence:** HIGH · **Sources:** SP:S-05, SP:S-06, SP:S-38, PS-14

#### DA-42 — SharePoint security granularity: unique permissions supported 50,000 / recommended 5,000 per list; inheritance cannot be broken above 100,000 items; no column-level security; customized forms inherit list Read; users with list edit rights can edit any item via the Lists UI, Excel or Graph regardless of the app; Microsoft's own pattern calls per-item ACL automation "significant operational overhead" and states SharePoint permissions "don't automatically align" with Dataverse row security
- **Classification:** CONSTRAINT / RISK · **Origin:** MS
- **Evidence:** "The supported limit of unique permissions for items in a list or library is 50,000. However, the recommended general limit is 5,000." "When a list … contains more than 100,000 items, you can't break permissions inheritance" [SP:S-01]. "any user who has at least Read or Restricted View access to the linked SharePoint list inherits access to the form." [SP:S-08]. "The permissions that you grant through the user interface of your app don't deny the data source permissions that the user has." (Salary example) [XC:S42]. "Dataverse enforces record-level security, but those permissions don't automatically apply to documents stored in SharePoint." "Per-item Access Control List (ACL) automation requires inheritance breaking, Microsoft Graph automation, and managing access at scale, creating significant operational overhead." "This pattern isn't suitable where strict file-level security is required for compliance reasons." [SP:S-24]. No Microsoft page found stating column-level security exists for lists (U-12; inference).
- **Why it matters:** "Each requester sees only their own records" is unscalable beyond a few thousand records; "hide this field" in the app is cosmetic.
- **Decision impact:** Requirement "row-level visibility per user/team at scale" or "sensitive fields visible only to some roles" → SharePoint cannot enforce → Dataverse (ownership/BU/column security) or SQL RLS. SharePoint suits coarse, list-level or few-group security.
- **Confidence:** HIGH (statements) / MEDIUM (no-column-security inference) · **Sources:** SP:S-01, SP:S-02, SP:S-08, SP:S-15, SP:S-24, XC:S42

#### DA-43 — Licensing gravity: SharePoint and Excel are Standard connectors usable on Microsoft 365 seeded rights, but seeded flows run in the "Low" performance profile (5,000 loop items; 10,000 requests/day; 2 retries), SharePoint triggers are polling-based (minutes; changes coalesce), the delete trigger is site-collection-admin-only, and item-menu flows live only in the default environment; Dataverse for Teams is the seeded relational alternative
- **Classification:** TRADE-OFF / DECISION CRITERION · **Origin:** MS
- **Evidence:** "A standalone Power Apps or Power Automate plan license is required to access all Premium, on-premises, and custom connectors." "Customers can continue to run standalone apps to extend and customize Microsoft 365 using standard connectors." [SP:S-09]. "Low | - Free - Microsoft 365 plans - Power Apps Plan 1, Per App plans …"; "Apply to each array item | 5,000 for Low"; "Power platform requests per 24 hours | 10,000 for Low" [SP:S-11]. "Power Automate periodically checks for changes … the flow run may occur within minutes … expect that the flow may gather more than one change in subsequent flow runs". "When an item is deleted … using a site collection admin account." "Only flows within the default environment can be executed manually from a SharePoint list." "Flows for lists are supported only in generic lists and generic document libraries." [SP:S-19, SP:S-03]. SharePoint connector throttling "API calls per connection | 600 | 60 seconds" [SP:S-03].
- **Why it matters:** Cost, not fit, is the usual driver for SharePoint-as-database; it pairs the least capable store with the least capable automation profile and the weakest ALM (default environment).
- **Decision impact:** Budget constraint "no premium licences" → evaluate Dataverse for Teams first when the audience is a Team; SharePoint only when the app must run outside Teams without premium AND the data profile passes DA-39..DA-42. Requirement "sub-minute reaction / field-level change audit / bulk processing" → not SharePoint + seeded licensing.
- **Confidence:** HIGH · **Sources:** SP:S-03, SP:S-09, SP:S-10, SP:S-11, SP:S-19, EX:S26

#### DA-44 — Governance and ALM of SharePoint-backed data: lists sit outside solutions (Site + List environment variables required; "the internal names won't match" if lists are recreated — Microsoft's mitigation is site duplication); the store inherits collaboration-site governance (external sharing on by default; guests with Edit can delete lists and items; inactive-site read-only/archive policies; site ownership turnover); reporting is import-only with type quirks and connection-owner permissions. Strengths: Purview retention labels on items (not attachments), full retention on library files, 93-day recycle bin, versioning
- **Classification:** CONSTRAINT / PATTERN · **Origin:** MS
- **Evidence:** "for SharePoint, in addition to a valid connection, a separate environment variable is required for Site and List." "if you create a list with the same name and columns in a target environment, the internal names won't match. The metadata always matches if you duplicate a SharePoint site" [SP:S-12]. "External sharing is turned on by default for your entire SharePoint and OneDrive environment." "if you add a guest as a site member, they have Edit permissions and they can add, edit, and delete lists." [SP:S-36]. Site lifecycle: "Set sites to read-only mode." "Archive sites after a configurable read-only period" (SharePoint Advanced Management) [SP:S-37]. "List items aren't supported by retention policies but are supported by retention labels"; standard label: "The document attachment doesn't automatically inherit the retention settings" [SP:S-25]. Power BI: "The semantic model won't be created if the SharePoint list contains values with more than four digits after a decimal place"; "Boolean values are represented inconsistently as TRUE/FALSE or 1/0" [SP:S-28, SP:S-29]. Positive fit: "Dataverse is the preferred choice if you need more complex relational data." (SharePoint or Dataverse as repository) [SP:S-20]; Microsoft's own hybrid: "Dataverse for structured business data and SharePoint for document storage" [SP:S-24]. Migration: "Create with external data … SharePoint list (preview)"; excluded columns "Image / Task outcome / External data / Managed metadata / Attachment (single) / Multiple attachments / images / … Unique values" [SP:S-26]; conversion is a one-time copy, not a sync [EX:S54, snippet].
- **Why it matters:** The application database is governed by SharePoint admins and collaboration policies, not by the app owner; an inactive-site policy can lock the store. "Start on SharePoint, move later" drops attachments/images/metadata columns and re-implements permissions.
- **Decision impact:** Requirement "controlled dev→test→prod with schema changes" or "store owned and lifecycle-managed by the app team" → Dataverse. Requirement "documents as the record, metadata on files, retention labels, versions" → SharePoint STRONG. If growth beyond SharePoint limits is plausible within the app's life, price the migration at decision time.
- **Confidence:** HIGH · **Sources:** SP:S-12, SP:S-20, SP:S-24, SP:S-25, SP:S-26, SP:S-27, SP:S-28, SP:S-29, SP:S-36, SP:S-37, EX:S54

### 4.5 External systems of record and multi-store architectures

#### DA-45 — Virtual tables: read/write external data in Dataverse "without the need for data replication", at the cost of most platform data features — organization-owned only (no row-level security), no auditing, change tracking, Synapse/Fabric sync, rollups, calculated/formula columns, duplicate detection, alternate keys, column security, Dataverse search, offline, BPF, dashboards, Power Pages; SQL provider: one shared credential, 1,000-record query cap, GUID/int PK, views read-only
- **Classification:** PATTERN / CONSTRAINT · **Origin:** MS
- **Evidence:** "Virtual tables are organization owned and don't support the row-level Dataverse security concepts. We recommend that you implement your own security model for the external data source." "Virtual tables don't support auditing." "Many features … cannot be enabled with virtual tables. Examples include queues, knowledge management, SLAs, duplicate detection, change tracking, mobile offline capability, column security, Dataverse search, and Power Pages solutions." "cannot be synchronized by using … Azure Synapse Link". "Column metadata properties that validate on update don't apply" [DV:S15, EX:S14]. "Alternate keys aren't supported in virtual tables because the system can't enforce uniqueness when the data is on another system." [EX:S20]. SQL provider: "These will be the credentials used for all authentication for the virtual table". **Precision added in v2** (review F-03; re-fetched verbatim, ms.date 2026-05-15): "Virtual table queries are limited to returning 1,000 records. **If you have a 1:N or N custom multitable (polymorphic) relationship with a virtual table, any query that exceeds this limit fails and provides an error.** Use filtering in your query to reduce the record set as a workaround to this limitation." — i.e. the 1,000-record cap is stated specifically in the context of 1:N/polymorphic relationship queries, not asserted as a flat ceiling on every virtual-table query; treat it as the binding figure for that scenario and see `VT-06`/`VT-09` for the broader, largely uncharacterised volume/paging picture. "Audit functionality isn't available"; "A virtual table can't be on the 1 side of a 1:N" [SQ:S6, SQ:S7]. Reference architecture: "Restrict access to the virtual tables to read access only." [SQ:S32]. Rejected in Microsoft's own sync reference: "the financial team needed to enrich records with department-specific attributes governed by strict row-level security." [EX:S30].
- **Why it matters:** The canonical "keep the data in the system of record, show it in the app" mechanism; the forfeited list is exactly the list of reasons you would need a copy. Availability and latency of the external source become the app's, and — closed in v2 — Microsoft publishes **no** performance/latency/throughput/caching characterisation for virtual tables at any volume (`VT-09`); column selection is also ignored, so every attribute returns on every query regardless of what the app needs (`VT-05`).
- **Decision impact:** Requirement "surface ERP/SQL master data without duplicating" AND uniform security AND no audit/search/offline/rollup/analytics on it → virtual table (read-only preferred, positively filtered, sub-1,000-row, narrow table — see `VT-17` for the full appropriate/not-appropriate ladder). Any of those needs, or any volume/latency SLA, or any need to be the "1" side of a relationship (`VT-06`) → replicate a subset one-way (DA-49) as a disposable read model keyed by the source id (DA-53).
- **Confidence:** HIGH · **Sources:** DV:S15, EX:S14, EX:S20, EX:S30, SQ:S6, SQ:S7, SQ:S32, PS-56, VT-05, VT-06, VT-09, VT-17

#### DA-46 — "View or data?" is the cheapest question: three integration categories (UI/embedding, data, process); embedding "saves time and reduces the need for training and user licenses" and keeps data in its home system but is "Tough to use this data for crunching numbers"; data availability (real-time vs end-of-day), direction, volume and throttling are Microsoft's stated pattern selectors
- **Classification:** DECISION CRITERION / PATTERN · **Origin:** MS
- **Evidence:** "Integration scenarios generally fall into three categories: user interface (UI), data, and process integration." "The simplest UI integration involves embedding a widget or app from one system into another" [EX:S06]. Embedding: "Pros: Easy since the data stays put in its home system. Cons: Tough to use this data for crunching numbers or processing." Aggregation: "Detailed data stays where it's most used. Limits traffic". "Data availability: When do you need the data ready? Is real-time essential, or is end-of-day collection sufficient?" "Flow direction … Scalability … Service protection and throttling" [EX:S05].
- **Why it matters:** If only a view is needed, no copy and no store decision arise; the moment the app must filter, join, secure or compute on foreign data, a copy or a delegable read-through is needed.
- **Decision impact:** Requirement "look-up only" → embed/read-through, no store. Requirement "filter/join/aggregate/secure on it" → copy (analytical or operational subset). Elicit per interface: freshness, direction, volume, throttling tolerance.
- **Confidence:** HIGH · **Sources:** EX:S05, EX:S06

#### DA-47 — Synchronous coupling vs asynchronous default: sync gives "Up-to-the-minute values" but "Only small payloads. Can lead to systems being too dependent on each other. Sensitive to delays" — use only when "You can't do without real-time information"; "Most recommended integration patterns and technologies are asynchronous but can feel like real-time"; app resilience to an ERP outage requires no synchronous dependency at write time
- **Classification:** TRADE-OFF · **Origin:** MS
- **Evidence:** [EX:S05] as quoted; "Synchronous integration patterns and near-real-time patterns often get mixed up and wrongly swapped." PPWA: "Real-time integration can provide immediate benefits to users, but it might affect performance and reliability. Using asynchronous approaches like Power Automate, or publishing Dataverse events to a queue … can improve performance and reliability. However, these methods don't give users immediate feedback." [EX:S02]. D365 IG anti-pattern: "Latency between your on-premises apps and the Dynamics 365 datacenter that affects the user experience." [EX:S08].
- **Why it matters:** Stakeholders say "real-time" when they mean "fresh enough"; the distinction decides whether the app depends on the enterprise system's availability.
- **Decision impact:** Requirement "app must keep working when ERP is down" → queue/event-based async, local pending state, eventual consistency accepted by the business, UI for "pending". Requirement "must see live value" → synchronous read-through with an availability story for the dependency.
- **Confidence:** HIGH · **Sources:** EX:S02, EX:S05, EX:S08

#### DA-48 — Ownership is decided per entity AND per field ("the Sales app owns the customer name and contact information, while the Finance app owns the credit limit and payment terms"); one-way sync "Sets a clear record keeper"; bidirectional sync is for when "There's no clear record keeper" and costs "Tricky conflict resolution. Data gets copied for each system"; Microsoft's only product-grade bidirectional sync (dual-write) exists for D365 F&O and "makes some crucial changes in the Dataverse schema"
- **Classification:** PATTERN / DECISION CRITERION / TRADE-OFF · **Origin:** MS
- **Evidence:** "it's crucial to identify which system owns the information." Per-field example as quoted [EX:S06]. One-way: "Pros: Sets a clear record keeper. Simple conflict solving. Cons: The receiver might not be able to lock down data as read-only". Bidirectional cons as quoted [EX:S05]. "Avoid creating tightly coupled point-to-point, custom synchronous service integrations" [EX:S09]. Dual-write: "tightly coupled, bidirectional integration between finance and operations apps and Dataverse"; "Dataverse includes new concepts such as company and party." [EX:S41]. Master data: "The data elements are typically stored within a master data management (MDM) solution … customers, accounts, products" [EX:S07]. Microsoft uses "system of record, or owner"; "source of truth" appears only for the golden configuration environment (U-14).
- **Why it matters:** The ownership map is the artefact that prevents two-master chaos; for non-Microsoft ERPs a bidirectional sync is a build with the same costs and none of the tooling.
- **Decision impact:** Requirement "customer/product master in the app" → owner = MDM/ERP; replicated attributes read-only in the app; app-specific enrichment in separate columns/tables. Requirement "two-way edits" → split field ownership into one-way flows; residual bidirectional only with explicit per-field conflict rules.
- **Confidence:** HIGH · **Sources:** EX:S05, EX:S06, EX:S07, EX:S09, EX:S41

#### DA-49 — Replication mechanisms and their freshness floors: dataflows 30-min increments, ≤ 48 refreshes/24 h, 24 h max run, single human owner, cannot delete rows or change status (Microsoft's own reference pairs them with event flows + nightly reconciliation); Fabric link up to 60 min; Synapse Link "near real-time can't be guaranteed", hourly snapshots; Power Pages server cache 15-min SLA ("never guaranteed to be immediate" for indirect writes); flow polling triggers minutes by plan; Dataverse change tracking deltas expire (default 7 days)
- **Classification:** PATTERN / CONSTRAINT · **Origin:** MS
- **Evidence:** "A dataflow can be refreshed up to 48 times per 24 hours (once every 30 minutes)." "There's only one owner of any dataflow" [EX:S29, SQ:S18]. Sync reference: "a dataflow can't change row statuses or delete records that are removed"; "Nightly dataflows in the secondary environment correct any missed or failed event-driven updates."; "When using dataflows, you can't assign service principals as owners." [EX:S30]. Fabric: "It might take up to 60 minutes" [XC:S31]. Synapse: "data availability in near real-time can't be guaranteed." [EX:S15]. Pages: "Automatic cache update has a service level agreement of 15 minutes." "data reflection from Dataverse to websites is never guaranteed to be immediate." [EX:S32]. Change tracking: "After you enable change tracking for a table, you can't disable it." "Changes are returned if the last token is within a default value of seven days." [EX:S19]. Polling: "your flow doesn't run again until five minutes elapses" (Office 365 / Dynamics 365 plans; page may be stale vs profile model, C-10) [EX:S47].
- **Why it matters:** "Near real-time" is undefined across sources (C-11); every mechanism has a documented floor that the business must accept explicitly.
- **Decision impact:** Freshness SLA X → mechanism: sync read-through (live); events/queue (minutes); dataflows (≥ 30 min, plus delete/status handling and reconciliation); Fabric/Synapse (≤ 1 h, analytics only); portal users see backend writes within 15 min at best.
- **Confidence:** HIGH · **Sources:** EX:S15, EX:S19, EX:S29, EX:S30, EX:S32, EX:S47, SQ:S18, XC:S31

#### DA-50 — Pushing Dataverse changes outward: synchronous webhooks are a dual-write hazard ("the data operation rolls back but the request sent to the configured endpoint can't be recalled"; 60-s timeout; one extra attempt on 502/503/504); Service Bus is async-only, queued, retried exponentially by the async service, 192 KB payload truncation; Microsoft's master-data reference publishes a canonical model to a Service Bus topic and warns "When the first listener is 'live', it's hard to change the model"
- **Classification:** DECISION CRITERION / PATTERN · **Origin:** MS
- **Evidence:** [EX:S21, EX:S22, EX:S31] as quoted; "Azure Service Bus works for high scale processing, and provides a full queuing mechanism … Webhooks can only scale to the point at which your hosted web service can handle the messages." "register the plug-in to run asynchronously for best system performance." "The asynchronous service continues to try to post the message in an exponential pattern".
- **Why it matters:** When the app is the master for an entity (field-captured data), consumers must be decoupled via a durable channel with a versioned contract; a sync webhook to an ERP creates phantom records on rollback.
- **Decision impact:** Requirement "ERP must reliably learn of app changes" → async Service Bus/queue (or pull via change tracking within the expiry window) + consumer idempotency; never a sync webhook for side effects; canonical contract and versioning policy before the first consumer.
- **Confidence:** HIGH · **Sources:** EX:S19, EX:S21, EX:S22, EX:S31

#### DA-51 — Microsoft-named integration anti-patterns: "Too much data synchronized with Dynamics 365 for reporting purposes that overloads the database. You should use a dedicated datastore for reporting purposes instead"; "Repeated connections between on-premises and cloud apps … send data in batches instead"; stakeholders wanting to "sync large amounts of data in real time or use Dynamics 365 as a reporting tool … can hurt the scalability and performance"; nightly bulk vs service protection; "a data warehouse is different from an ERP"
- **Classification:** ANTI-PATTERN · **Origin:** MS
- **Evidence:** [EX:S08, EX:S09] as quoted; "Dynamics 365 and Power Platform have limits on how much data you can store and how often you can access it … you might face service throttling, errors, or increased storage costs." Service protection remedy "move towards real-time integration" [EX:S18]. Storage management: analytics "can double or triple your storage footprint" [DV:S28].
- **Why it matters:** Direct Microsoft evidence against "replicate the ERP into Dataverse" and against "Dataverse as the report warehouse"; the enforcement mechanisms (capacity cost, API limits, throttling) bite at scale, not in pilots.
- **Decision impact:** Requirement "reporting across ERP history" → analytical store fed from both systems; Dataverse holds only what the app operates on. Requirement "migrate history" → do not; link out or lake-load (DA-54).
- **Confidence:** HIGH · **Sources:** DV:S28, EX:S08, EX:S09, EX:S18

#### DA-52 — Failure handling across stores: requests must be idempotent ("if an operation that inserts a record into Microsoft Dataverse is repeated, it might cause incorrect values"); exponential retry for background, fixed/immediate for interactive, never endless, never cascading; queue + dead-letter for async; Retry-After honoured; saga with pivot ("point of no return"), irreversible steps last, human fallback; flows with continuous errors or throttling are turned off after 14 days and revert to Low profile when the owner leaves
- **Classification:** RECOMMENDATION / RISK · **Origin:** MS
- **Evidence:** PPWA RE:05 [EX:S03]: "Never implement an endless retry mechanism." "Avoid designs that include cascading retry mechanisms … nine retry attempts in total". "An increase in the number of throttling errors is often an indicator of a design flaw". D365 IG: "For asynchronous integrations, set up queues for checking and redoing actions, keeping aside any failed messages to fix later." "Make sure your requests can't be duplicated because of retries." [EX:S05]. Saga/compensation [EX:S12, EX:S13]: "Pivot transactions serve as the point of no return"; "Sometimes manual intervention is the only way to recover"; not suitable when "The system can't tolerate temporary inconsistency". Queue-based load leveling: "Design consumer logic to be idempotent"; "route them to a dead-letter queue"; not suitable when "The caller requires a low-latency, synchronous response." [EX:S49]. Power Automate: "Flows with errors 14 days … turned off"; "Consistently throttled flows 14 days … turned off"; "If the original owner leaves the organization, the flow reverts to the Low performance profile." "Outbound synchronous request 120 seconds" [EX:S26]. Triggers: "'at-least-once' design … design them to be idempotent … using key constraints in Dataverse" [EX:S47].
- **Why it matters:** Duplicates on retry are the most common data-quality defect in low-code integrations; a flow-based sync inherits a person's licence profile and silently downgrades.
- **Decision impact:** Requirement "write to Dataverse and ERP" → idempotency key per write (alternate key / message id), single retry owner, queue + DLQ monitoring, ERP posting as pivot, pending-state column + reconciliation. Requirement "sync must survive owner change and volume growth" → service-principal/Process-licensed flow or Azure integration.
- **Confidence:** HIGH · **Sources:** EX:S03, EX:S05, EX:S12, EX:S13, EX:S26, EX:S47, EX:S49

#### DA-53 — Idempotency and master-data keys: alternate keys (≤ 10 per table; ≤ 16 columns / 900 bytes; not on secured columns or virtual tables; reserved characters `/ # < > * % & : \ ? +` break GET/PATCH) are the integration-grade uniqueness mechanism; duplicate detection is advisory (matchcode; 5 published rules per table; defaults only for account/contact; not offline); reference data has three homes (named formulas, environment variables ≤ 2,000 chars, custom tables via CMT); ERP-owned lists are lookups, not choices
- **Classification:** PATTERN / CONSTRAINT · **Origin:** MS (choice-vs-lookup rule INF)
- **Evidence:** [EX:S20, XC:S24, XC:S25] as quoted; "Attributes must not have field-level security applied". "You can publish only five rules for the same base record type" [XC:S26]. Named formulas: "The formula's value is always up to date"; "Using the OnStart property can cause performance problems" [EX:S33]. Env vars: "Yes if your configuration data isn't relational … key: value pairs and when the value likely needs to different in other environments"; "limited to a maximum of 2,000 characters" [EX:S34]. Global vs local choices [EX:S35].
- **Why it matters:** The external system's id becomes the key; a secured PII column (national id) cannot be a key → surrogate/hash. Choices are metadata (solution deployment) and cannot be sourced from an external master (INF, U-15).
- **Decision impact:** Requirement "records originate in ERP" → ERP id as alternate key; upsert-by-key on every sync path; sanitised surrogate for ids with reserved characters. Requirement "list of values maintained by business in ERP" → one-way replicated lookup table; "static enumeration" → choice; "endpoint/threshold per environment" → environment variable.
- **Confidence:** HIGH (keys, rules) / MEDIUM (choice-vs-lookup rule) · **Sources:** EX:S20, EX:S33, EX:S34, EX:S35, XC:S24, XC:S25, XC:S26

#### DA-54 — Migration and caching: migrate master data and open transactions, not closed history ("Migrated data is either master data … or open transactions"); separate configuration data from migration data; golden configuration environment as "source of truth for your configurations"; test migration in SIT and UAT; ADF into Dataverse is upsert-only with alternate keys, default 10×10 concurrency, 52-concurrent-batch ceiling, business-logic bypass flags; Excel/CSV import has a 12-min export limit and cannot preserve created/modified/owner; caching (collections, named formulas, Cache-Aside) is for static data — "doesn't guarantee consistency", unsuitable for sensitive data, local caches diverge
- **Classification:** RECOMMENDATION / CONSTRAINT · **Origin:** MS
- **Evidence:** [EX:S27, EX:S28] as quoted; "data migration activities can be a disruptive task and shouldn't coexist with other testing activities." ADF: "writeBehavior … must be 'Upsert'"; "100 records are concurrently submitted by default"; "there's a limit of 52 concurrent batch calls per organization"; "bypassBusinessLogicExecution" [EX:S42]. Import: "Exports have a 12 minute time limit."; unsupported "Timezone, Choices (multiselect), Image, File" and "Createdon, Modifiedon, Ownerid" [EX:S24]. Cache-Aside: "doesn't guarantee consistency between the data store and the cache"; not suitable when "The data is sensitive or security related"; "a local cache is private … can quickly become inconsistent" [EX:S11]. PPWA: "use variables in cloud flows or collections in canvas apps to cache data"; "If underlying data changes frequently, implement a cache invalidation mechanism" [EX:S01]. Materialized view: "completely disposable because it can be entirely rebuilt from the source data stores" [EX:S50].
- **Why it matters:** "Open transactions only" scopes migration; history is a reporting concern. Bypassed plug-ins = business rules not applied to loaded rows → post-load validation. A Dataverse table fed from the ERP and never edited locally is a materialized view: disposable and rebuildable.
- **Decision impact:** Requirement "history visible" → do not migrate closed transactions; link or lake. Requirement "initial load" → staging + validation, alternate keys, service-principal identity, migration window vs service protection, post-load validation. Requirement "user must never see stale price/credit limit" → no cache for that attribute; cache static reference data only.
- **Confidence:** HIGH · **Sources:** EX:S01, EX:S11, EX:S24, EX:S27, EX:S28, EX:S42, EX:S50

### 4.6 Cross-cutting: sensitivity, network, residency, ownership, quality, cost

#### DA-55 — Managed Environments is the single licensing gate behind most data-requirement controls (long-term retention, CMK, Lockbox, IP firewall, VNet, masking rules, 28-day backups, sharing limits, data policies); CMK, IP firewall and Lockbox additionally require E5-class Microsoft 365 licences; CMK locks copy/restore to the same key, removes audit retention settings, and leaves connector settings on Microsoft keys; Lockbox excludes Azure OpenAI/Copilot features and break-glass; column security never hides data from system administrators
- **Classification:** FACT / DECISION CRITERION / CONSTRAINT · **Origin:** MS
- **Evidence:** Managed Environments feature list "Limit sharing … Data policies … IP Firewall … Customer Managed Key (CMK) … Lockbox … Extended backup … Virtual Network support … Create and manage masking rules"; "included as an entitlement with standalone Power Apps, Power Automate, Microsoft Copilot Studio, Power Pages, and Dynamics 365 licenses." [XC:S28]. CMK: "only enforced on environments that are activated for managed environments"; users need "Microsoft 365 or Office 365 A5/E5/G5"; "The environment is disabled when it's added to the enterprise policy"; "The connection settings for connectors continue to be encrypted with a Microsoft-managed key."; restore "restricted to … another environment that is encrypted with the same customer-managed key." [XC:S15]. "The audit retention period isn't available … for environments encrypted with a customer's own encryption key." [XC:S09]. Lockbox: "Features powered by Azure OpenAI Service are excluded"; "Tenant-to-tenant migration isn't supported when Customer Lockbox is enabled." [XC:S29]. IP firewall: "A malicious user who tries to download data from Dataverse using a client tool like Excel or Power BI from a disallowed IP location is blocked" [XC:S16]. Column security: "Data is never hidden from system administrators."; not securable: "Columns in virtual tables; Lookup columns; Formula columns; Primary name columns; System columns"; masking "must be a managed environments" [XC:S12, XC:S14].
- **Why it matters:** Any data requirement in the classes "retain N years", "customer key", "approve Microsoft access", "block by IP", "private network", "mask PII", "> 7-day backups" implies premium licensing for every user of the environment; a solution scoped as "seeded licences only" cannot meet them. Sensitive values must not be modelled as primary name or lookup.
- **Decision impact:** Data requirements decide the licensing model, not only app type. Requirement "hide from admins too" → not achievable via column security → CMK + separation of duties + Lockbox, or keep data out of the platform.
- **Confidence:** HIGH · **Sources:** XC:S09, XC:S12, XC:S14, XC:S15, XC:S16, XC:S28, XC:S29

#### DA-56 — Network posture: VNet support is "the only supported option for all the scenarios for outbound connectivity from Power Platform except Power BI and Power Platform dataflows" (which use the VNet data gateway); the connector list covers SQL, Azure Blob/File/Queue, Key Vault, custom connectors, HTTP with Entra, Snowflake, Databricks — not SharePoint; enabling VNet breaks public calls; Dataverse for Teams and trials excluded
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** [XC:S17, SQ:S4] as quoted; "A virtual network linked to a Power Platform environment must reside in the Power Platform environment's region."; environment types "Trial | No; Microsoft Dataverse for Teams | No".
- **Why it matters:** "Data must not traverse the public internet" is satisfiable for Azure SQL / on-prem via ExpressRoute / Blob / Key Vault, never for SharePoint (M365 endpoints); it brings Azure subscription, subnet sizing, region pairing and dual-region delegation.
- **Decision impact:** Requirement "private connectivity to corporate SQL" → VNet-enabled Managed Environment + Azure subscription + enterprise policy; requirement applies to SharePoint data → not achievable (M365 boundary applies instead).
- **Confidence:** HIGH · **Sources:** SQ:S4, XC:S17

#### DA-57 — Residency is per environment and irreversible: region fixed at creation and binds Dataverse, apps, connections, gateways; EU Data Boundary requires the tenant AND all environments in macro region "European Union (EU) and EFTA" (not "Europe and United Kingdom") plus an EU billing address — "Meeting only one doesn't place your environments within the EU Data Boundary"; without Advanced Data Residency on all M365 seats the datacentre within the macro region is Microsoft-chosen; India/Australia tenant restrictions; restore and CMK are same-region
- **Classification:** CONSTRAINT · **Origin:** MS
- **Evidence:** "Environments can be created in different regions, and are bound to that geographic location." "Tax laws prevent you from creating a database for an environment in India and Australia, if your Microsoft Entra tenant is not in India and Australia" [XC:S18]. EUDB requirements as quoted [XC:S19]. "To select a specific datacenter region within a macro region geography … enable: Advanced data residency for all Microsoft 365 seats". "Europe and United Kingdom (UK) … shouldn't be considered EUDB." "Plan for the possibility that unforeseen circumstances might place environments … in different datacenter regions within that macro region. This placement can affect Azure network alignment, VNet integration design, latency expectations". "Don't interpret macro-regions as legal, regulatory, tax, or compliance-defined areas" [XC:S23]. Synapse/Fabric targets must be same-region/geo [XC:S30, XC:S31].
- **Why it matters:** A single non-EU environment (a US sandbox) takes the tenant out of EUDB scope by Microsoft's wording; country-level residency ("data stays in Portugal") is not guaranteed without ADR; VNet/CMK designs assuming a fixed Azure region pair may need rework.
- **Decision impact:** Requirement "data at rest in EU" → environment-creation policy (all environments, incl. dev/test, in macro region #3; EU billing); analytical targets in-geo. Requirement "country-level" → ADR licence or accept macro-region only. Provision the first environment before designing VNets unless ADR.
- **Confidence:** HIGH · **Sources:** XC:S11, XC:S18, XC:S19, XC:S23, XC:S30, XC:S31

#### DA-58 — Residency exceptions that survive region selection: Dataverse table and column *names*, app names/descriptions/logos and Power Pages website name/URL replicate globally; preview features "typically store customer data in the United States"; Brazil South replicates to South Central US for DR; Power Apps/Automate connected to Dynamics 365 "may be sent outside of the designated region"; generative AI "inputs (prompts) and outputs (results) might move outside of your region" — Copilot features on by default, "Flex routing is on by default for eligible tenants that were created after March 25, 2026", movement "can't be reversed"; on-prem gateway results transit Azure Relay and the cloud service
- **Classification:** FACT / RISK · **Origin:** MS
- **Evidence:** [XC:S41] as quoted: "Dataverse table and column names … are replicated globally for support and troubleshooting purposes, but the content within those database tables remains stored in geo." "Regardless of where the customer data is stored, Microsoft does not control or restrict the locations from which customers, or their end users, may access customer data." Copilot: Europe → Azure OpenAI "In European Union (EU) Data Boundary"; Bing search "United States"; "Data movement that occurred while your environment was allowed to move data across regions can't be reversed" [XC:S20]. Gateway: "The results are sent from the data source back to the gateway and then to the cloud service." "By using Azure ExpressRoute, you can make sure this traffic doesn't traverse the public internet." [XC:S21].
- **Why it matters:** Schema names can be sensitive (`hiv_status`, confidential project codes); "no processing outside EU" is not met by defaults; data-at-rest commitments hold, processing and access location are the customer's job.
- **Decision impact:** Requirement "no data outside region" → naming convention keeping sensitive semantics out of schema/app names; no preview features in production; disable cross-region AI data movement and flex routing via environment-group rules; IP firewall/Conditional Access for access location; "keep on-prem via gateway" still transits Microsoft cloud.
- **Confidence:** HIGH · **Sources:** XC:S20, XC:S21, XC:S41, PS-17

#### DA-59 — Sensitivity class → acceptable store: structured PII with role-based field visibility → Dataverse (only store with API-level column security; masking with Managed Env); documents that must carry protection when downloaded → SharePoint/OneDrive with sensitivity labels (Office/PDF/MP4; encrypted files need service processing enabled; > 12 MB encrypted files break on move); no label mechanism for list items/columns or Dataverse rows/file columns; Purview Data Map scans Dataverse metadata (no incremental scan; not in sovereign clouds); Well-Architected: classify backups and analytical copies too; the Dataverse-record + SharePoint-document hybrid "isn't suitable where strict file-level security is required"
- **Classification:** DECISION CRITERION · **Origin:** MS
- **Evidence:** Labels [XC:S49]: "Until you enable this feature, these services can't process encrypted files, which means that coauthoring, eDiscovery, data loss prevention, search … won't work". "Microsoft Dataverse integrates with Microsoft Purview to apply data labels." "If your workload generates new data that wasn't previously stored anywhere, like when transitioning from a paper-based process, we suggest storing this data in Microsoft Dataverse." "have you classified the backup of your highly sensitive data store? … If you use analytical data stores, how is the aggregated data classified?" [XC:S36]. Purview scan: "Incremental Scan — No"; "isn't available in sovereign clouds" [XC:S35]. SharePoint-Dataverse pattern: "The intent of this pattern isn't to enforce security at the SharePoint item level." [SP:S-24]. Column security [XC:S12]; SharePoint Salary example [XC:S42].
- **Why it matters:** The two security models do not synchronise; a hybrid inherits both and needs an explicit permission-sync design (or accepts discoverability-level control on documents).
- **Decision impact:** Per entity: classification → store: structured confidential fields → Dataverse CLS (never as primary name/lookup); labelled documents → SharePoint; hybrid → explicit permission-sync design or Dataverse file columns (row security, no labels). Classification must follow data into Fabric/Synapse/Power BI copies and backups.
- **Confidence:** HIGH · **Sources:** SP:S-24, XC:S12, XC:S35, XC:S36, XC:S42, XC:S49

#### DA-60 — Data quality and erasure: server-enforced rules "regardless of the app used to create the data" exist only in Dataverse (business rules, required columns, alternate keys, duplicate detection); SharePoint validation lives in the app/form; Excel/SharePoint-origin data carries type looseness into BI; GDPR erasure must be executed across every copy — Dataverse record + audit history (dedicated privilege) + retained store (deletion policy) + Synapse/Fabric replicas (deletes replicate unless append-only; soft delete then hard delete after 30 days) + Power BI import datasets; "Removing personal data includes system-generated logs but not audit-log information"
- **Classification:** CONSTRAINT / RECOMMENDATION · **Origin:** MS
- **Evidence:** "Business rules validate data across multiple columns and tables, and provide warning and error messages, regardless of the app used to create the data." [SP:S-22]. Alternate keys enforce uniqueness "using database indexes" [XC:S24]; duplicate detection "You can publish only five rules" [XC:S26]. DSR: "Removing personal data includes system-generated logs but not audit-log information." [XC:S34]. "Dataverse auditing supports the deletion of a single record's entire audit history … Users must have the Delete Audit Record Change History privilege" [XC:S09]. Synapse: "All create, update, and delete operations are exported" [XC:S03]; "Append only mode is the recommended option … when the data volumes are high"; Delta: "soft delete … followed by a hard delete after 30 days" [XC:S43]. Retained data "immutable and read-only"; deletion via "Data Life Cycle Config … deletion policies" [XC:S08] (scope UNKNOWN, U-16). D365 IG: data quality "is still typically a human responsibility"; "The users who are most familiar with their data should be the gatekeepers for cleansing" [EX:S07, XC:S48].
- **Why it matters:** Retention and erasure pull in opposite directions; "append only" lake mode conflicts with erasure; quality is stewardship, not tooling.
- **Decision impact:** Requirement "rules must hold regardless of entry channel" → Dataverse. Requirement "GDPR erasure within N days" → erasure runbook per store from day one; avoid append-only lake where erasure applies; name a data steward per entity.
- **Confidence:** HIGH (elements) / MEDIUM (cross-store synthesis) · **Sources:** EX:S07, SP:S-22, XC:S03, XC:S08, XC:S09, XC:S24, XC:S26, XC:S34, XC:S43, XC:S48

#### DA-61 — Licensing does not favour SQL over Dataverse (both premium; both need Managed Environments for the controls in DA-55); it does separate both from Standard connectors (SharePoint, Excel, Dataverse for Teams); multiplexing/shared connections to avoid licences is prohibited (PS-36); pay-as-you-go suits "Widely distributed apps … with infrequent and/or unpredictable use"
- **Classification:** DECISION CRITERION / ANTI-PATTERN · **Origin:** MS
- **Evidence:** SQL connector "Power Apps | Premium" [SQ:S1]; "the capabilities of Dataverse included with select Microsoft 365 licenses don't allow customers to create custom apps with Power Apps or use the premium connectors" [SQ:S20]; "Standard connectors don't require special licensing." [SQ:S22]; PAYG: "only pay if and when they're used" [SQ:S31]. Dataflows authoring requires a premium plan [DV:S32].
- **Why it matters:** Two anti-patterns follow: choosing SharePoint/Excel to avoid premium and then hitting relational/security needs (AP-5 in PS); choosing SQL "because Dataverse storage is expensive" without costing gateway/Azure/ops.
- **Decision impact:** Requirement "minimise cost" → licence is a constraint on all users, not a discriminator between SQL and Dataverse; compare capacity vs Azure SQL tier + gateway + ops; PAYG for wide, infrequent audiences.
- **Confidence:** HIGH (facts) / MEDIUM (anti-pattern framing) · **Sources:** DV:S32, SQ:S1, SQ:S20, SQ:S22, SQ:S31, PS-36

#### DA-62 — Cost model per meter (Licensing Guide Sept 2026): add-ons $40 DB / $2 File / $10 Log per GB/month (Tier 2 DB $30 at ≥ 1,000 GB); PAYG $48 / $2.40 / $12 (no log allocation); Power Apps Premium accrues 250 MB DB + 2 GB File per user (Process 50 MB / 200 MB; Power Pages per pack 2 GB DB / 16 GB File / 1 GB Log); tenant default 20 GB DB / 20 GB File / 2 GB Log (guide's own example says 10 GB DB — C-01); one Premium licence ($20/user/month) buys 250 MB of database
- **Classification:** FACT / DECISION CRITERION · **Origin:** MS (PDF, text-extracted)
- **Evidence:** [DV:S40 pp.8, 20–22] as quoted; "Dataverse capacity add-ons do not apply to Dataverse for Teams scenarios"; "Additional subscriptions do not add to the tenant's default capacity." Dynamics 365 Sales Premium uplift (MC1253515, April 2026) seen only in message-centre archive/T3 [DV:S38, DV:S41] (U-17).
- **Why it matters:** Database is 20× file per GB and 4× log; per-user accrual is heavily file-skewed (a 100-user Premium tenant: ~45 GB database vs ~220 GB file entitlement) — database is scarce, file is abundant; 1 GB of extra database costs 2× a user licence per month.
- **Decision impact:** Cost per month ≈ max(0, DB_GB − (default + 0.25·users))·$40 + max(0, File_GB − (default + 2·users))·$2 + max(0, Log_GB − 2)·$10; binaries to file columns; audit scoped; LTR (~50% DB) or external archive for cold relational data; Fabric replica on the DB meter; PAYG priced ~20% above add-ons — for spiky/uncertain workloads only. USD list, billed annually; EUR/EA effects UNKNOWN (U-18).
- **Confidence:** HIGH (rules) / MEDIUM (default GB) · **Sources:** DV:S38, DV:S40, DV:S41, DV:S47

#### DA-63 — Environment strategy, DLP and stewardship make the store decision enforceable: DLP governs connectors, not data ("which systems may this app talk to"), with up to 24-h enforcement latency and suspension of violating apps/flows; advanced connector policies do not support virtual connectors; ownership is organisational (LOB owner + named data steward) before it is technical (record owner/BU); "one environment per unit" multiplies every data control, "one shared environment" pushes segmentation into BU/roles
- **Classification:** RECOMMENDATION / PATTERN · **Origin:** MS
- **Evidence:** DLP: "If a violation occurs, put the app, flow, or chatbot in to a suspended or quarantine state"; "the latency for full enforcement is 24 hours"; "Advanced connector policies (ACP) don't support virtual connectors" [XC:S46]. "A data steward is a role that's responsible for the management and oversight of your data assets." "Every line of business (LOB) has a level of ownership of their data" [XC:S48]. Environment boundary statements in DA-25.
- **Why it matters:** The store decision becomes configuration (business/blocked connector groups per environment) — retrofitting DLP can suspend running apps; platform constructs encode access, not accountability.
- **Decision impact:** Requirement "regulated data stays in approved stores" → DLP groups per environment at design time. Discovery must yield per entity: owner (LOB), steward, classification, retention rule, quality gate — these feed schema decisions that are immutable after creation (DA-12, DA-15).
- **Confidence:** HIGH · **Sources:** XC:S46, XC:S48, DA-25

---

### 4.7 Virtual tables at volume, and consuming Fabric/analytical outputs (new in v2 — closes review F-03, F-13)

The following 17 findings (`VT-01`..`VT-17`) close the review's highest-priority gap: virtual tables were the most-recommended "keep in place" mechanism in v1 (DA-45, DA-46, §6) and the least characterised. All are sourced from Microsoft Learn (12 pages, all fetched 2026-09-02); no T2/T3/T4 material was used.

#### VT-01 — Provider roster is broader than SQL/SharePoint/Excel: eight virtual connector providers, Excel demoted to legacy

**Classification:** FACT
**Origin:** MS (T1)
**Evidence** [S1]:
> "This document covers the new experience using Power Apps (make.powerapps.com) to create virtual tables using the following virtual connector providers:" — followed by "SQL Server", "SharePoint", "Microsoft Fabric", "Salesforce", "Oracle Database", "Snowflake", "PostgreSQL", "Azure Databricks".
> "You can create a virtual table for Excel using a legacy process with a virtual connector provider."
[S2]: > "Excel is currently not supported in the table driven virtual table experience."
Preview status is explicit per provider on [S1]: "Microsoft Fabric (preview)", "Salesforce (preview)", "Oracle (preview)", each carrying "Preview features aren't meant for production use and may have restricted functionality."

**Why it matters:** The viable provider set for a production engagement is narrower than the marketing list. Snowflake, PostgreSQL, SQL Server and SharePoint are GA; Fabric, Salesforce and Oracle carry the preview disclaimer; Excel is legacy-only.
**Decision impact:** data requirement (external system stays system of record) → constraint (only GA providers are production-safe; Fabric/Salesforce/Oracle are preview) → architectural implication (if the source is Fabric/Salesforce/Oracle, the virtual-table path is a prototype-grade option only; plan a connector or ETL fallback).
**Conditions:** As of ms.date 2026-05-07. Preview status changes; re-verify at decision time.
**Confidence:** HIGH

---

#### VT-02 — CRUD is supported "unless the data source forbids it"; the per-provider write matrix is defined by connector limitations, not by Dataverse

**Classification:** CONSTRAINT
**Origin:** MS (T1)
**Evidence** [S1]:
> "Virtual tables allow for full create, read, update, and delete privileges unless the data source they're connecting to specifically forbids it."
> "To learn more about supported actions and limitations with each connector, go to:" — links to the SQL Server, Excel Online Business, SharePoint Online, Salesforce, Oracle, Snowflake and PostgreSQL connector references.
[S2] concrete write failures:
> "SQL Server tables without primary keys: You can select any nonstring field as the primary key. You can create the virtual table successfully. `RetrieveMultiple` works, but the other operations fail with the following error message (coming from SQL connector): \"APIM request wasn't successful: BadRequest: No primary key exists in table.\""
> "You can use SQL views to create a virtual table but they only provide read operations."
> "The **Microsoft Entra ID** virtual table provided by Microsoft only allows read access."
[S4] (dev overview): > "An [OData v4] provider is included with the service and is installed by default. This provider supports create, read (retrieve, retrieve multiple), update and delete (CRUD) operations."
> "Full CRUD operation is now supported for custom virtual table data provider."

**Why it matters:** There is no single published "write support per provider" table. Write viability must be derived per provider from that provider's connector reference plus the source schema (PK presence/type). Read-only outcomes are silent at design time and fail at runtime.
**Decision impact:** data requirement (app must write to the external source) → constraint (write support is a property of the underlying connector + source PK, verifiable only per-table) → architectural implication (proof-of-write on the actual source table is a mandatory spike before committing to virtual tables for a write scenario; views and PK-less tables are read-only by construction).
**Conditions:** Per provider, per table.
**Confidence:** HIGH

---

#### VT-03 — Single shared connection, and connections shared *with* you cannot be used

**Classification:** CONSTRAINT
**Origin:** MS (T1)
**Evidence** [S1]:
> "These will be the credentials used for all authentication for the virtual table so use credentials with the correct level of permissions with SQL Server."
> "The connection can be shared with one user or can be shared with the entire organization. This allows users to access and operate virtual tables using a shared connection. By using security roles, virtual table access can be restricted to a specific set of users within your organization. You can even specify which roles have create, read, update, or delete privileges in this way."
> "Connections that are shared with you aren't available for use with this feature. Only connections created by the current user appear in the virtual table wizard."
[S2]: > "If you deleted the connection connected to virtual table and recreated it, the Virtual Connector Provider app loses permission to access the new connection, preventing data retrieval."

**Why it matters:** Adds NEW detail to the known "single shared credential" fact: (i) authorisation granularity is limited to Dataverse security-role CRUD privileges on the whole table — never per row, never per source-side identity; (ii) the creating maker's identity is baked in, which is a personal-account/service-account governance issue and a bus-factor risk; (iii) connection re-creation silently breaks data retrieval.
**Decision impact:** data requirement (per-user or per-row authorisation on external data) → constraint (virtual tables authenticate as one identity; only table-level role privileges are available) → architectural implication (any row-level or source-side-identity requirement disqualifies virtual tables; a service principal / dedicated service account owned by the platform team, not a maker, is mandatory).
**Conditions:** All virtual connector providers.
**Confidence:** HIGH

---

#### VT-04 — Negative filter operators corrupt paging beyond the first page, with no workaround

**Classification:** ANTI-PATTERN
**Origin:** MS (T1)
**Evidence** [S2]:
> "Queries against virtual tables that use negative filter operators, such as Does Not Equal or Does Not Contain, might result in incorrect paging behavior beyond the first page. There's currently no supported workaround. Avoid using negative filters."

**Why it matters:** This is the only explicit Microsoft statement found on virtual-table *paging correctness*. It is a data-integrity defect, not a performance note: page 2+ can return wrong rows. "No supported workaround" is unusually blunt for Learn.
**Decision impact:** data requirement (users filter grids with exclusion criteria — "status not closed", "not archived") → constraint (negative operators break paging; the platform will not fix in-query) → architectural implication (model exclusions as positive enumerations — e.g. an explicit status set — or push the filter into a source-side view; never expose an "does not contain" search box over a virtual table).
**Conditions:** Any virtual table query with negative operators, beyond page 1.
**Confidence:** HIGH

---

#### VT-05 — Column selection is ignored: virtual tables always return all attributes

**Classification:** CONSTRAINT
**Origin:** MS (T1)
**Evidence** [S4]:
> "Selecting attributes in Retrieve and RetrieveMultiple queries won't be applied since all attributes are returned"
> "Reduce and limit including virtual table lookup columns in your grid view. It can take a while to read the virtual table lookup columns."
[S3] (OData provider best practice, contradicting direction for the OData provider specifically):
> "For retrieve multiple queries, such as when you load data in to a grid, control the size of the dataset returned from the external data source by using the select and filter query parameters."

**Why it matters:** The single most effective payload-reduction technique on a wide table ($select / column-subset) is non-functional for virtual tables in general. Row count is the ONLY dimension the app can control. Combined with the 1,000-row cap, payload size per page is fixed by table width. The "$select" advice in [S3] applies to the OData endpoint contract level, not to Dataverse-side query column pruning.
**Decision impact:** data requirement (wide source table, e.g. 80+ columns, shown in a list) → constraint (all columns cross the wire on every retrieve; no column pruning) → architectural implication (narrow the *source* — build a purpose-shaped source-side view/projection per app screen and virtualise that, rather than virtualising the base table; accept that a source-side view is read-only [S2]).
**Confidence:** HIGH

---

#### VT-06 — Virtual table lookup columns cannot be filtered or sorted, and a virtual table cannot be the "1" side of a 1:N

**Classification:** CONSTRAINT
**Origin:** MS (T1)
**Evidence** [S4]:
> "Although you can add virtual table columns as a lookup on a grid or other UI views, you can't filter or sort based on this virtual table lookup column."
[S2]:
> "A virtual table can't be on the *1* side of a 1:N (one-to-many) relationship. This is because virtual tables are metadata representations of the source table. When you create a relationship, additional supporting columns are added to the 1 side of the 1:N relationship. Dataverse doesn't have the ability to create new columns in source systems."
[S5] (metadata table): > "ManyToOneRelationships | valid | Not supported between two virtual tables."
And [S2] on the interaction with the known 1,000-row cap:
> "Virtual table queries are limited to returning 1,000 records. If you have a 1:N or N custom multitable (polymorphic) relationship with a virtual table, any query that exceeds this limit fails and provides an error. Use filtering in your query to reduce the record set as a workaround to this limitation."

**Why it matters:** The relational modelling envelope is much tighter than "it looks like a Dataverse table". A virtual table can be the *many* side and can be looked up, but it can't parent native records, can't relate to another virtual table many-to-one, and lookups over it are dead weight in views (unsortable, unfilterable, slow per [S4]).
**Decision impact:** data requirement (native Dataverse child records hanging off external master data — e.g. Dataverse-side approvals against external work orders) → constraint (virtual table cannot occupy the 1 side; two virtual tables cannot be related N:1) → architectural implication (either replicate the master key as a plain text/GUID column on the native child and lose referential integrity, or ingest the master data into a real Dataverse table via dataflow/Fabric link and reserve virtual tables for read-only reference lookups).
**Confidence:** HIGH

---

#### VT-07 — Custom (plug-in) data providers: five events, stage 30, no registered steps, explicit TimeoutException contract

**Classification:** FACT
**Origin:** MS (T1)
**Evidence** [S6]:
> "Each data provider is composed of a reusable set of Dataverse plug-ins that implement the supported CRUD operations. For each virtual table, also known as a virtual entity, developers can create plug-ins and register them representing each of the **Create**, **Update**, **Retrieve**, **RetrieveMultiple**, and **Delete** operations."
> "**RetrieveMultiple** | Contains a [QueryExpression] object defining the query. The framework contains a **QueryExpressionVisitor** class designed to inspect different parts of the query expression tree."
> "For both events, you must: 1. Convert the respective information in the execution context into a query that works for your external data source. 2. Retrieve the data from the external system. 3. For **Retrieve**, convert the data into an [Entity]; otherwise, for **RetrieveMultiple**, convert it to an [EntityCollection]."
> "Unlike an ordinary plug-in, use the Plug-in Registration Tool (PRT) to register the assembly and the plug-ins for each event. Don't register specific steps. Your plug-in runs in stage 30, the main core transaction stage for the operation that isn't available for ordinary plug-in steps."
> "Custom data providers require substantial development resources to create and maintain."
> "[TimeoutException] | The external operation didn't complete within the allowed time; for example, the result of an HTTP status 408 from the external data service."
> "Instead of creating a custom data source provider, consider adapting your data source to an existing data provider. For example, if you create an OData v4 interface to your external data source, you can directly access it by using the supplied standard OData v4 Data Provider, which supports CRUD operations."
[S2] (operational trap): > "When a custom data provider for a virtual table is updated to support new operations (e.g., create, update, delete), the platform does not automatically add corresponding permissions to the existing virtual table entity." → "the user must recreate the virtual table entity after updating the data provider."

**Why it matters:** Custom providers are pro-code with a maintenance tail, explicitly discouraged by Microsoft in favour of exposing OData. NEGATIVE FINDING on the "2-minute plug-in limit": the custom-provider page states no execution-time figure; it defines a `TimeoutException` for the *external* call and points to the data-source-level "Timeout in seconds" setting for the OData provider [S3]. No Learn page found asserts that the documented plug-in 2-minute limit applies to virtual-table providers — do not assert it as fact.
**Decision impact:** data requirement (source has no supported connector and no OData surface) → constraint (custom provider = .NET plug-in development, stage 30, PRT registration, per-operation plug-ins, and table re-creation on capability change) → architectural implication (prefer building/renting an OData v4 façade over the source and using the shipped provider; a custom provider is only justified when the source cannot be fronted at all and the volume/latency envelope has been measured).
**Confidence:** HIGH (facts) / HIGH for the negative finding on the 2-minute limit being undocumented here

---

#### VT-08 — Paging mode and timeout are configuration on the OData data source, not on the query

**Classification:** DECISION CRITERION
**Origin:** MS (T1)
**Evidence** [S3]:
> "**Timeout in seconds**. Enter the number of seconds to wait for a response from the web service before a data request time-out. For example, enter 30 to wait a maximum of thirty seconds before a time-out occurs."
> "**Pagination mode**. Select whether to use client-side or server-side paging to control how query results are paged. The default value is client-side paging. With server-side paging, the server controls how results are paged by using the $skiptoken parameter, which is added to the query string."
> "**Return inline count**. Returns the total number rows in the result set. This setting is used to enable next page functionality when you return data to a grid. Use a value of false if your OData endpoint doesn't support the OData $inlinecount parameter. The default value is false."
> "You can't use the OData v4 Data Provider to connect to another environment."
> "Up to 10 header or query strings can be added."
Data-type gaps: > "You can only map ID columns to external columns with the `Edm.Guid` data type. You can’t map an `Edm.Int32` data type to a Unique Identifier data type column in Dataverse." Unsupported for mapping: "`Edm.Binary`", "`Edm.Time`", "`Edm.Float`", "`Edm.Single`", "`Edm.Int16`", "`Edm.Byte`", "`Edm.SByte`".

**Why it matters:** This is the most concrete paging evidence Microsoft publishes. Key consequences: (i) the DEFAULT is client-side paging — i.e. Dataverse pages the result itself, which implies the endpoint returns more than the page; (ii) grid "next page" only works if the endpoint supports `$inlinecount`, and the default for that flag is `false`, so out of the box a grid may have no next-page affordance; (iii) there is a hard per-request timeout the architect chooses. The page's ms.date is 2021-08-11 — the oldest source in this file.
**Decision impact:** data requirement (users browse beyond the first page of an external dataset) → constraint (server-side paging must be explicitly selected, the endpoint must implement `$skiptoken`, and `$inlinecount` must be supported and switched on) → architectural implication (make endpoint paging capability a written acceptance criterion on the OData façade; if the source cannot do `$skiptoken` + `$inlinecount`, design single-page/search-first screens instead of browsable grids).
**Conditions:** OData v4 Data Provider specifically. ms.date 2021-08-11 — stale; treat behaviour as needing re-verification.
**Confidence:** MEDIUM (facts are HIGH; currency is the weak point)

---

#### VT-09 — NEGATIVE FINDING: Microsoft publishes no virtual-table performance, latency, caching, throttling or pushdown characterisation

**Classification:** RISK
**Origin:** MS (T1) — absence of evidence
**Evidence:** Across [S1] [S2] [S3] [S4] [S5] [S6] the only performance-adjacent statements are:
> "It can take a while to read the virtual table lookup columns." [S4]
> "Reduce and limit including virtual table lookup columns in your grid view." [S4]
> "control the size of the dataset returned from the external data source by using the select and filter query parameters" [S3]
> "You get notified that a timeout occurred during the virtual table creation. **Solution**: This can occur when other existing jobs cause the virtual table creation to be delayed. Wait for a few minutes and try again." [S2] — this is *creation-time*, not query-time.
Throttling appears only as a *creation-time* artefact: > "Here, table creation failed due to 429 \"Too Many Requests\" error:" [S2].
No page states a latency figure, a concurrency ceiling, a request-per-minute budget for virtual-table traffic, whether Dataverse caches virtual-table results, or which FetchXML clauses are pushed down to the source versus evaluated after retrieval. `IsEnabledForCharts` is qualified as "*limited* | Only for supported Fetch clauses." [S5] — which implies a pushdown-support set exists but is not enumerated anywhere found.

**Why it matters:** Volume viability is undocumented by the vendor. Any statement of the form "virtual tables handle N rows at acceptable latency" is unevidenced. The absence is itself the finding: the platform gives no SLA, no capacity guidance, and no cache, so end-to-end latency is entirely the source system's plus per-hop overhead, on every single grid render, with no server-side result reuse.
**Decision impact:** data requirement (volume/latency SLA on an external dataset surfaced in an app) → constraint (no vendor performance characterisation exists; no caching layer is documented) → architectural implication (mandatory measured spike against production-like volume before commitment, and the measurement — not documentation — becomes the evidence; the design must degrade to search-first single-page screens rather than browsable grids, and Dataverse API request entitlements must be checked separately because every render is a live source call).
**Conditions:** Valid as of 2026-09-02 across the six Learn pages fetched. Not an exhaustive proof of absence across all of Learn.
**Confidence:** MEDIUM (negative findings on documentation absence cannot reach HIGH)

---

#### VT-10 — Canvas delegation: virtual tables are absent from Microsoft's delegable-data-source list, and the 500/2,000 cliff applies

**Classification:** RISK
**Origin:** MS (T1) — mixed positive/negative
**Evidence** [S9]:
> "These popular tabular data sources support delegation:" — the list names exactly four: "Power Apps delegable functions and operations for Microsoft Dataverse", "…for SharePoint", "…for SQL Server", "…for Salesforce". Virtual tables are not named anywhere on the page.
> "A query is **nondelegable** if it uses a feature the data source doesn't support. If any part of a query expression is nondelegable, Power Apps doesn't delegate any part of the query."
> "When a query is nondelegable, Power Apps gets the first 500 records from the data source and then runs the actions in the query. You can increase this limit to 2,000 records."
> "if you use the **Filter** function with a selection formula that can't be delegated over a data source with a million records, only the first 500 records are scanned. If the record you want is record 501 or 500,001, **Filter** doesn't find or return it."
> "Delegation warnings appear only on formulas that use delegable data sources. If you don't see a warning but think your formula isn't delegated, check your data source type against the list of delegable data sources"
> "To make sure your app scales to large data sets, set this value to 1. Anything that can't be delegated returns a single record, which is easy to detect when testing your app."
> "You can expand or join up to 20 entities in a single query."

**Why it matters:** NEGATIVE FINDING — no Microsoft page found states which Power Fx operations delegate to a virtual table. A canvas app addresses a virtual table through the Dataverse connector, so the Dataverse delegation list is the nominal contract, but the actual pushdown depends on the underlying provider/connector, which Microsoft does not document. The compounding danger is the quoted warning-suppression rule: if the runtime does not treat the source as delegable, **no delegation warning is shown at all** — the maker gets silently truncated results with no design-time signal.
**Decision impact:** data requirement (canvas app filters/searches an external dataset larger than 2,000 rows) → constraint (virtual-table delegation behaviour is undocumented; the 1,000-row virtual-table cap and the 500/2,000 canvas cap stack; delegation warnings may be absent even where truncation occurs) → architectural implication (set Data row limit to 1 during build to force truncation into the open; test filter results against a known row beyond the cap; if the dataset exceeds the caps, do not surface it in a canvas gallery — front it with a search-first pattern or a Power Automate/API call that returns a bounded result set).
**Conditions:** Canvas apps over virtual tables. Model-driven grids are a separate question (see VT-11).
**Confidence:** MEDIUM (the delegation mechanics are HIGH; "virtual tables are not on the list" is an absence, not a denial)

---

#### VT-11 — Model-driven grids over virtual tables: paging exists but its correctness is conditional

**Classification:** CONSTRAINT
**Origin:** MS (T1)
**Evidence** [S3]:
> "**Return inline count**. Returns the total number rows in the result set. This setting is used to enable next page functionality when you return data to a grid. Use a value of false if your OData endpoint doesn't support the OData $inlinecount parameter. The default value is false."
[S2]:
> "Queries against virtual tables that use negative filter operators, such as Does Not Equal or Does Not Contain, might result in incorrect paging behavior beyond the first page."
> "Virtual table queries are limited to returning 1,000 records."
[S4]:
> "Reduce and limit including virtual table lookup columns in your grid view. It can take a while to read the virtual table lookup columns."
[S5]: > "IsEnabledForCharts | *limited* | Only for supported Fetch clauses."

**Why it matters:** Model-driven views over virtual tables do paginate, but "next page" is a capability of the *provider/endpoint*, not of the grid. With the OData provider it is off by default and requires `$inlinecount` support upstream. Combined with the 1,000-record ceiling and negative-filter paging corruption, a model-driven grid over a virtual table is only safe over a pre-filtered, positively-filtered, sub-1,000-row slice.
**Decision impact:** data requirement (users browse a long external list in a model-driven app) → constraint (paging correctness depends on endpoint capabilities and breaks with negative filters; hard 1,000-row cap) → architectural implication (design views with mandatory, positive, source-side-narrowing default filters; treat the virtual table as a lookup/detail surface, not a browse surface; verify next-page behaviour empirically at build time).
**Confidence:** MEDIUM

---

#### VT-12 — Virtual tables sourced from Fabric OneLake are READ-ONLY — explicit and unambiguous

**Classification:** FACT
**Origin:** MS (T1)
**Evidence** [S7]:
> "Virtual tables created with data from Microsoft Fabric OneLake are read-only. Currently, you can't modify the data in Fabric OneLake with Power Apps."
> "With Dataverse virtual tables sourced with Fabric, your low-code app builders connect to data in OneLake and build Power Apps and drive business actions. Additionally, with Power Pages, low-code makers can build external facing websites and drive action from OneLake insights with partners, suppliers, and customers."
> "This feature is enabled by default with all environments. Admins can disable this feature in the Power Platform admin center in the environment feature settings."
Primary-key caveat: > "While the table you selected from Fabric Lakehouse might not have a primary key defined, you need to select a field that is unique to continue. If you don't select a unique field, the table might not show all the records. While the wizard selects a field based on metadata available, the selection might not be accurate."
Prerequisite: > "Contributor or administrator access to a Fabric workspace with data." / "If you don’t have Power BI premium license or Fabric capacity, you can sign up for a free [Fabric trial capacity]."
[S1] confirms the provider is preview: > "Microsoft Fabric (preview)".

**Why it matters:** This closes gap (b) at the core. The Fabric→Dataverse direction works as a read-only projection of analytical output into apps. The silent-data-loss trap is severe: a lakehouse table with no real key can be virtualised anyway, and the result "might not show all the records" — wrong data with no error.
**Decision impact:** data requirement (app must surface a computed/aggregated analytical result — score, forecast, segment) → constraint (Fabric-sourced virtual tables are read-only, preview, and require a genuinely unique column or rows silently disappear) → architectural implication (write the analytical output to a lakehouse/warehouse table with an explicitly materialised unique key column; use the virtual table purely to display the insight; capture the resulting human action in a *native* Dataverse table keyed to that insight — the write path and read path are different stores by design).
**Conditions:** Preview feature as of ms.date 2026-04-09. Fabric capacity or trial required.
**Confidence:** HIGH

---

#### VT-13 — No write-back from Fabric link / Synapse Link to Dataverse: the pipeline is one-directional by construction

**Classification:** CONSTRAINT
**Origin:** MS (T1)
**Evidence** [S7]: > "Virtual tables created with data from Microsoft Fabric OneLake are read-only. Currently, you can't modify the data in Fabric OneLake with Power Apps."
[S10] (Synapse Link FAQ, on the lake side): > "Data files shouldn't be modified by a customer and no customer files should be placed in the data folders."
[S8] (Fabric link FAQ): > "Removing a table doesn't delete the table in Dataverse; it only removes the OneLake shortcut and stops data sync."
[S11] (Fabric link overview): > "With shortcuts from Dataverse directly into OneLake, your data stays in Dataverse while authorized users get to work with data in Fabric."
> "the system creates an optimized replica of your data in delta parquet format… using Dataverse storage such that your operational workloads aren't impacted."
> "Low-code makers can build apps and automations to orchestrate business processes and react to insights found in Fabric. By adding those insights back to Dataverse as virtual tables connected to OneLake, makers build low-code apps"

**Why it matters:** Resolves the open unknown. Neither FAQ contains any statement supporting write-back; both describe an export/replica model, and the lake side is explicitly declared off-limits for customer modification. The **only** documented return path from Fabric into Power Platform is a read-only virtual table over OneLake [S7] — the sanctioned pattern in [S11] is literally "adding those insights back to Dataverse as virtual tables connected to OneLake". Note this is an argument from consistent absence plus the [S7] explicit read-only statement, not a single sentence saying "write-back is unsupported".
**Decision impact:** data requirement (round-trip: Dataverse → Fabric analytics → correction/enrichment written back into Dataverse) → constraint (the link is a one-way replica; the lake must not be written by the customer; the return path is read-only) → architectural implication (the return leg must be built explicitly — a Fabric pipeline / notebook / Power Automate flow calling the Dataverse Web API as a separate integration with its own identity, throttling budget and error handling — it is NOT a feature of the link; budget it as a distinct component).
**Confidence:** HIGH for the read-only virtual-table path; MEDIUM for "no write-back anywhere in the link feature" (evidenced by absence)

---

#### VT-14 — Fabric analytical freshness is ~1 hour, and `SinkModifiedOn` is not a reliable latency signal

**Classification:** TRADE-OFF
**Origin:** MS (T1)
**Evidence** [S8]:
> "When the initial sync is complete, the system continuously refreshes updates in Dataverse in the lakehouse. Incremental updates typically take up to one hour to appear, though actual timing depends on table size, number of updates and transactions happening in the environment, number of tables, row count, and system load periods."
> "Because the metadata sync isn't instantaneous and takes up to *one hour* to propagate to Fabric."
> "`SinkModifiedOn` is typically later than `ModifiedOn`, and the difference depends on factors such as batch size, system load, and the number of records being processed."
> "Use caution when building latency reports based on the difference between `SinkModifiedOn` and `ModifiedOn`, as it can give a misleading impression of actual data availability."
[S12] (Power Automate, quoting the Fabric link doc): > "it can take up to **60 minutes** to update data in OneLake, including the conversion to delta parquet format."
[S11] hints at improvement: > "Microsoft continues to invest in Link to Fabric as the primary sync path, including the low-latency sync engine that's rolling out now."

**Why it matters:** Quantifies the freshness envelope for the Fabric round trip. An insight surfaced in an app via a Fabric-sourced virtual table is at minimum ~1 hour behind the operational Dataverse row, plus whatever the Fabric transformation adds. This is the decisive number for whether analytics-into-app is viable for a given process.
**Decision impact:** data requirement (operational decision must reflect a computed insight) → constraint (round-trip freshness is ~1 hour+ end to end, not near-real-time; there is no published SLA, only "typically") → architectural implication (only processes whose decision cadence tolerates ≥1 hour staleness may consume Fabric-derived insight in-app; for anything faster, compute in Dataverse — low-code plug-in, flow, or a Dataverse-side aggregate — and keep Fabric for reporting; always surface the insight's as-of timestamp in the UI so users see the staleness).
**Conditions:** Fabric link. "Low-latency sync engine" is announced as rolling out — re-verify.
**Confidence:** HIGH

---

#### VT-15 — Fabric link is constrained by Dataverse mechanics: change tracking mandatory, 2,000-table ceiling, 200 MiB per-record cap, schema changes break sync

**Classification:** CONSTRAINT
**Origin:** MS (T1)
**Evidence** [S8]:
> "Any table that doesn't have change tracking enabled isn't supported."
> "If you have more than 2,000 active Dataverse tables, Link to Fabric can fail with an error."
> "Link to Fabric reads rows through Dataverse, so every Dataverse per-record limit applies to sync. The most common limit is the 200 MiB cap on the uncompressed size of a single record returned by the server." / "This is a Dataverse platform limit and can't be raised on request."
> "Changing the data type or precision of a column that's already synced isn't supported." → "These changes cause *permanent delta sync failures*." → "Deleting the column and re-creating it with the same name and a different type *doesn't* work."
> "When you delete a column in Dataverse, link to Fabric *doesn't* physically drop the column from the downstream store. Instead, its values are sent as **null** going forward."
> "Existing profiles where the data is saved as CSV files can't be linked to Fabric." / "Azure Synapse Link profiles secured with managed identities currently can't be linked to Fabric."
> "Today, a Dataverse environment links to a single Fabric workspace." [S11]
> "Enabling this feature results in an increase in **Dataverse database** storage consumption." [S11]
[S10] (Synapse Link, column security trap): > "Azure Synapse Link reads Dataverse data as an application user. When a column is secured, the application user must be granted read access to that column through a column security profile. If the application user isn't added to the profile that secures the column, the sync completes successfully and all other columns export as expected, but the secured column is exported as null."
[S10] (calculated columns): > "If a calculated column value changes without a corresponding version change to the record, the updated value isn't synchronized to the data lake until the record is updated and its version changes."
[S10] (hard-delete blind spot): > "For any direct SQL call to remove a record, the Azure Synapse Link for Dataverse service doesn't trigger because BPO.Delete isn't being called."

**Why it matters:** The analytics path has silent-wrongness failure modes that look like success: secured columns export as null, calculated columns go stale without a version bump, deleted columns keep reporting null. Schema evolution is a genuine operational hazard — a data-type change permanently breaks delta sync and cannot be repaired by drop-and-recreate.
**Decision impact:** data requirement (Dataverse operational data feeding Fabric analytics that the app later consumes) → constraint (change tracking mandatory; schema is effectively frozen post-link for types/precision; column security silently nulls data; storage billed against Dataverse) → architectural implication (freeze the analytical column contract before linking and version schema changes as remove-and-re-add of the table; add the sync application user to every relevant column security profile; never let a calculated column be an analytical input — materialise it; add a reconciliation check comparing Dataverse row counts to lakehouse row counts).
**Confidence:** HIGH

---

#### VT-16 — Reading a Fabric SQL analytics endpoint from Power Apps/Power Automate: no first-party documented path; the sanctioned route is the OneLake virtual table

**Classification:** DECISION CRITERION
**Origin:** MS (T1) — partly negative finding
**Evidence** [S11]:
> "Dataverse also generates an enterprise-ready [Microsoft Fabric Lakehouse and SQL endpoint] and a Power BI dataset for your Power Apps and Dynamics 365 data. This makes it easier for data analysts, data engineers, and database admins to combine business data with data already present in OneLake using Spark, Python, or SQL."
> "By adding those insights back to Dataverse as virtual tables connected to OneLake, makers build low-code apps with Power Apps, Power Pages, or Power Automate using the design tools already available."
> "Using connectors to over 1,000 apps, makers create business processes that span Dynamics 365 as well as many other enterprise applications."
[S12] confirms the endpoint exists per link: > "After linking the environment, you see a Lakehouse, a semantic model, and a SQL analytics endpoint."
NEGATIVE: across [S7] [S11] [S12] no page states that Power Apps or Power Automate connects to a Fabric SQL analytics endpoint via the SQL Server connector, nor names a Fabric connector for Power Apps. Every consumption route named for makers is the OneLake **virtual table**. Consumption routes named for the endpoint itself are analyst/engineer tools ("Spark, Python, or SQL").

**Why it matters:** Closes gap (b)'s second half. The documented, supported maker-side consumption pattern for Fabric output is exactly one: a read-only virtual table over OneLake. Anything else — pointing the SQL Server connector at the Fabric SQL analytics endpoint — is undocumented on Learn for Power Apps/Power Automate and must be treated as unverified, not as a supported architecture. Do not present it as a fact either way without a spike.
**Decision impact:** data requirement (app or flow must read a Fabric warehouse/lakehouse result) → constraint (only the OneLake virtual table is a documented maker path; it is read-only, preview, and carries all VT-01..VT-11 limits) → architectural implication (design the Fabric side to emit a small, narrow, uniquely-keyed "insight" table purpose-built for the app — not a wide analytical fact table — and virtualise that; if a SQL-endpoint connector route is desired, it is a spike with an explicit support-status question to Microsoft before it enters an architecture).
**Conditions:** As of 2026-09-02 across the Learn pages fetched. Not exhaustive proof of absence.
**Confidence:** MEDIUM

---

#### VT-17 — Composite verdict: when virtual tables ARE appropriate, and when they are not

**Classification:** DECISION CRITERION
**Origin:** INF (synthesis of MS-sourced findings above — inference, not a Microsoft statement)
**Evidence:** Derived from VT-01 through VT-16. No Microsoft page states this verdict; it is an inference from the quoted constraints.

**Appropriate when ALL hold:**
- The result set the user sees is reliably under 1,000 rows after a mandatory, *positive* filter [S2].
- Read-only, or writes are proven per-table against the actual source (real PK, not a view) [S1][S2].
- Authorisation is table-level only — no row-level, no per-user source identity [S1].
- The table is narrow, because column selection is ignored and all attributes return [S4].
- The virtual table is the *many* side or a pure lookup — never the 1 side of a 1:N [S2].
- The source's own latency is acceptable on every single render, because no caching is documented [VT-09].
- Avoiding data duplication is a genuine requirement — the source stays the system of record.

**Not appropriate when ANY holds:**
- Row-level security, auditing, or per-user source identity is required [S1][S4].
- Users must browse, sort, or exclusion-filter a large dataset [S2].
- Native Dataverse records must be children of the external master [S2].
- A latency or throughput SLA must be met — the vendor publishes none [VT-09].
- Offline, BPF, Dataverse search, charts, or duplicate detection are in scope [S4][S5].
- The source is Fabric, Salesforce, or Oracle and the deliverable is production [S1].

**Alternative to weigh in every case:** ingest into a native Dataverse table (dataflow / Fabric link / integration) and accept duplication in exchange for RLS, auditing, delegation, offline, relationships and a known performance profile — or expose an OData v4 façade and use the shipped provider rather than building a custom one [S6].
**Decision impact:** data requirement (external data needed inside a Power Platform app) → constraint (the virtual-table envelope above) → architectural implication (virtual tables are a *reference-data and read-only insight surface*, not a general integration layer; the default for transactional, secured, or high-volume data is replication into native Dataverse).
**Confidence:** MEDIUM (inference clearly labelled; each input constraint is HIGH)

---

---

### 4.8 Dataverse→SQL/warehouse replication paths and reconciliation (new in v2 — closes review F-04, F-08)

The following 18 findings (`SY-01`..`SY-18`) close two review gaps at once: (a) v1 recommended a "Dataverse + Azure SQL hybrid" without evidencing how the copy is made — `SY-01` establishes, as a hard negative finding, that no first-party managed replication exists; (b) v1's reconciliation/drift-repair coverage was thin — `SY-06`..`SY-17` document the mechanisms (change tracking, dual-write, Service Bus dead-lettering, Microsoft's own resilient-sync reference architecture) and, in `SY-14`, the concrete ways a Synapse Link replica silently diverges while reporting success. All 19 sources are Tier 1 Microsoft Learn.

#### SY-01 — No first-party Dataverse→Azure SQL Database replication; Dataverse is not a Fabric mirroring source

**Classification:** Negative finding (hard). **Origin:** MS (T1).

**Evidence**
Fabric Mirroring overview (`S-01`, ms.date 2026-08-28) enumerates the complete set of mirrorable sources. Verbatim table entries: "Azure Cosmos DB", "Azure Databricks", "Azure Database for PostgreSQL", "Azure Database for MySQL (preview)", "Azure SQL Database", "Azure SQL Managed Instance", "Dremio catalog (preview)", "Google BigQuery", "Oracle", "SAP", "SharePoint List (preview)", "Snowflake", "SQL Server", "Open mirrored databases", "Fabric SQL database". **Dataverse does not appear.** The page states: "Currently, the following external databases are available:" — followed by that table.

Mirroring direction is *into* Fabric, not into Azure SQL: "You can continuously replicate your existing data estate directly into Fabric's OneLake from various Azure databases and external data sources." And "Mirroring in Fabric is a fully managed service, so you don't have to worry about hosting, maintaining, or managing replication of the mirrored connection."

Note the reverse direction *is* first-party for Azure SQL: "Azure SQL Database → Database mirroring" is supported, i.e. Azure SQL can be a mirroring **source** into Fabric, never a mirroring **target** for Dataverse.

Evidence checked and exhausted for a Dataverse→Azure SQL first-party path: (1) Mirroring overview source list `S-01`; (2) Link to Fabric (already established — target is a Fabric delta-parquet replica, not Azure SQL); (3) Synapse Link (already established — target is customer-owned ADLS Gen2, not Azure SQL); (4) Data Export Service, the only historical first-party Dataverse→Azure SQL service, retired Nov 2022 (already established); (5) the ADF/Fabric Dataverse connector `S-03`, which is a *pipeline you build and operate*, not a managed replication service.

**Why it matters**
The v2 evidence file recommends a "Dataverse + Azure SQL hybrid" with "replicated read models" but does not say who makes the copy. There is no Microsoft-operated service that does it. Every Dataverse→Azure SQL copy is customer-built and customer-operated ETL, with the customer owning scheduling, watermarking, failure handling, backfill and reconciliation.

**Decision impact**
Data requirement: relational SQL read model over Dataverse data → constraint: no managed replication exists; only (a) customer-built ADF/Fabric pipelines, or (b) accept a *lake/Fabric* target (Synapse Link / Link to Fabric) and query it read-only via SQL analytics endpoint → architectural implication: if the read model must be a writable Azure SQL database, budget a bespoke pipeline plus a reconciliation job as first-class components with an owner; if read-only SQL suffices, prefer Link to Fabric + SQL analytics endpoint and delete the Azure SQL tier from the design.

**Conditions:** Applies while the mirroring source list stands as of 2026-08-28. Re-check `S-01` before each engagement — the list has grown repeatedly (SharePoint List, SAP, Oracle are recent additions), so a future Dataverse entry is plausible.
**Confidence:** High for the negative (explicit enumerated list on a Tier-1 page).
**Sources:** S-01, S-02, S-03.

---

#### SY-02 — Fabric/lakehouse SQL analytics endpoint is read-only T-SQL; it is not an operational store

**Classification:** Hard constraint. **Origin:** MS (T1).

**Evidence** (`S-02`, ms.date 2026-05-19)
"The SQL analytics endpoint gives you a read-only T-SQL query surface over the Delta tables in your lakehouse."
"The SQL analytics endpoint operates in read-only mode over Delta tables — you can't insert, update, or delete data through it. To modify data, switch to the lakehouse and use Apache Spark."
Scope of the same surface across items: "Other Fabric items — including warehouses, mirrored databases, SQL databases, and Azure Cosmos DB — also auto-provision a SQL analytics endpoint. The experience and limitations are the same across all of them."
What is available inside the read-only boundary: "Query Delta tables with T-SQL", "Create views, functions, and stored procedures", "Apply row-level and object-level security", "Build Power BI reports", "Query across workspaces".
Cross-source joins: "you can write cross-database queries, joining data from mirrored databases, warehouses, and the SQL analytics endpoints of Lakehouses in a single T-SQL query" (`S-01`).

**Why it matters**
This is the actual SQL surface a "Dataverse + warehouse" design gets for free (via Link to Fabric). It answers reporting/aggregation needs but cannot host application writes, staging tables written by an app, or a two-way read model.

**Decision impact**
Data requirement: T-SQL access to Dataverse data for reporting, joins across systems, RLS-controlled analytics → constraint: read-only; DML must happen in Dataverse or via Spark in the lakehouse → architectural implication: reporting and cross-system joins can be served with zero custom pipeline (Link to Fabric + endpoint), but any requirement for writes into the SQL tier forces a separate, customer-built warehouse/Azure SQL and re-opens SY-01.

**Conditions:** Fabric capacity required. Note also `S-01`: "A running Microsoft Fabric capacity is required for mirroring. A paused or deleted capacity affects mirroring and no data is replicated."
**Confidence:** High.
**Sources:** S-01, S-02.

---

#### SY-03 — SQL analytics endpoint schema/type limitations distort the replicated model

**Classification:** Hard constraint (data-fidelity). **Origin:** MS (T1).

**Evidence** (`S-02`)
"Data should be in Delta Parquet format to be autodiscovered in the SQL analytics endpoint."
"Delta column mapping by name is supported, but Delta column mapping by ID is not supported."
"Delta tables created outside of the `/tables` folder aren't available in the SQL analytics endpoint." And: "The tables that reference data in the `/files` folder in the lake aren't exposed in the SQL analytics endpoint."
"Some columns that exist in the Spark Delta tables might not be available in the tables in the SQL analytics endpoint."
"External Delta tables created with Spark code aren't visible to the SQL analytics endpoint. Use shortcuts in the Tables section to make external Delta tables visible."
Long text: "The **varchar(max)** data type is only supported in SQL analytics endpoints of mirrored items and Fabric databases, and not for lakehouses." And: "Data truncation to 8 KB still applies on the tables in SQL analytics endpoint of the lakehouse, including shortcuts to a mirrored item."
Schema-change lock-in: "If you add a foreign key constraint between tables in the SQL analytics endpoint, you won't be able to make any further schema changes (for example, adding the new columns)."
Item ceiling: "A workspace supports up to **150 warehouse and SQL analytics endpoint items combined**."
Reserved names: "Schemas with names that conflict with system schemas (such as `sys` or `information_schema`) and database security principals (such as `db_owner`, `db_datareader`) aren't supported in the SQL analytics endpoint. Tables under these schemas will fail to sync to the SQL analytics endpoint."

**Why it matters**
A "replicated read model" is not a faithful copy. Long multiline text and rich-text Dataverse columns can be truncated at 8 KB on a lakehouse endpoint; some columns may simply not surface. Any consumer that assumes byte-equality with Dataverse will produce false drift alarms — or, worse, silently lose content.

**Decision impact**
Data requirement: replicated read model used for reporting and downstream integration → constraint: 8 KB truncation on lakehouse endpoints, possible missing columns, no ID-based column mapping → architectural implication: enumerate long-text/rich-text columns up front; either exclude them from the replica and fetch on demand from Dataverse, or target a mirrored item/Fabric database where varchar(max) is supported; never define reconciliation hashes over columns subject to truncation.

**Conditions:** Lakehouse endpoints specifically; mirrored items and Fabric databases differ.
**Confidence:** High.
**Sources:** S-02.

---

#### SY-04 — ADF/Synapse Dataverse connector: source-side read behaviour is FetchXML-only, with schema inferred by sampling

**Classification:** Hard constraint. **Origin:** MS (T1).

**Evidence** (`S-03`, ms.date 2025-07-25)
Supported activities: "Copy activity (source/sink)", "Mapping data flow (source/sink)", "Lookup activity" — with mapping data flow marked Azure IR only ("① Azure integration runtime ② Self-hosted integration runtime"; data flow shows ① only).
Query surface: "FetchXML is a proprietary query language that is used in Dynamics online and on-premises." The source `query` property is "No if `entityName` in the dataset is specified" — i.e. either a whole table or a FetchXML query, nothing else.
Primary key: "The PK column will always be copied out even if the column projection you configure in the FetchXML query doesn't contain it."
Schema inference hazard: "When the service imports a schema in the authoring UI, it infers the schema. It does so by sampling the top rows from the Dynamics query result to initialize the source column list. In that case, columns with no values in the top rows are omitted. The same behavior also applies to data preview and copy executions if there's no explicit mapping."
Mitigation stated by MS: "When you copy data from Dynamics, explicit column mapping from Dynamics to sink is optional. But we highly recommend the mapping to ensure a deterministic copy result."
Data-flow typing loss: "If you select **Query** as input type, the column type from tables can not be retrieved. It will be treated as string by default."
Unsupported source column types: "The Dynamics data types **AttributeType.CalendarRules**, **AttributeType.MultiSelectPicklist**, and **AttributeType.PartyList** aren't supported."
Read of views is indirect: "To retrieve data from Dynamics views, you need to get the saved query of the view, and use the query to get the data." — via the `savedquery` / `userquery` tables.
Application-type scope: "This connector doesn't support other application types like Finance, Operations, and Talent."

**Why it matters**
This is the only generally available way to *pull* Dataverse rows into an arbitrary SQL sink, and it has two silent-data-loss traps: sampled schema inference dropping sparse columns, and multi-select choice / party-list columns being unsupported outright. Incremental extraction is not a connector feature — it is a FetchXML `modifiedon` filter the author writes (MS's own sample filters `modifiedon` "between" two literal timestamps), so the watermark is the customer's problem.

**Decision impact**
Data requirement: incremental Dataverse extraction into a SQL sink → constraint: FetchXML-only queries, sampled schema inference, no built-in watermark, three unsupported attribute types → architectural implication: pin explicit column mappings in every pipeline (never rely on inferred schema); design and persist the watermark yourself (or drive extraction from change tracking, SY-08); model multi-select choices and party lists as separate child extractions or exclude them with an explicit decision recorded.

**Conditions:** ADF/Synapse; Fabric Data Factory has its own connector doc ("This connector is also available in Data Factory in Microsoft Fabric") — verify Fabric-specific behaviour separately.
**Confidence:** High for the quoted constraints.
**Sources:** S-03.

---

#### SY-05 — ADF write-side concurrency is bounded by the Dataverse 52-concurrent-batch limit; defaults are deliberately small

**Classification:** Hard constraint (throughput). **Origin:** MS (T1).

**Evidence** (`S-03`)
"The default value for both the sink **writeBatchSize** and the copy activity **parallelCopies** for the Dynamics sink is 10. Therefore, 100 records are concurrently submitted by default to Dynamics."
"For Dynamics 365 online, there's a limit of 52 concurrent batch calls per organization. If that limit is exceeded, a 'Server Busy' exception is thrown before the first request is ever run. Keep **writeBatchSize** at 10 or less to avoid such throttling of concurrent calls."
"The optimal combination of **writeBatchSize** and **parallelCopies** depends on the schema of your entity. Schema elements include the number of columns, row size, and number of plug-ins, workflows, or workflow activities hooked up to those calls. The default setting of **writeBatchSize** (10) × **parallelCopies** (10) is the recommendation according to the Dynamics service."
Business-logic bypass exists but is privileged: `bypassBusinessLogicExecution` — "Note that you must have the `prvBypassCustomBusinessLogic` privilege. By default, only users with the system administrator security role have this privilege." Also `bypassPowerAutomateFlows`.
Idempotency: sink "writeBehavior" — "The value must be 'Upsert'", with "alternateKeyName — The alternate key name defined on your entity to do an upsert."

**Why it matters**
Relevant to the *repair* direction: when drift is found and rows must be pushed back into Dataverse, throughput is capped and the cap is per-organization, shared with every other integration. Plug-ins and flows firing on each write both slow the repair and can cause secondary drift. The bypass switches make bulk repair feasible but require system-administrator-level privilege and change business semantics.

**Decision impact**
Data requirement: bulk drift repair / backfill writing into Dataverse → constraint: 52 concurrent batch calls per organization, default 100 concurrent records, plug-ins/flows fire per write → architectural implication: size repair windows from these numbers rather than from row counts alone; decide explicitly whether repair writes bypass custom business logic and Power Automate flows (and who holds `prvBypassCustomBusinessLogic`); make repair idempotent via an alternate key so a re-run is safe.

**Conditions:** "Server Busy" is thrown *before* the first request runs when the concurrency limit is exceeded — a failure mode that looks like a connectivity error, not a throttle.
**Confidence:** High.
**Sources:** S-03.

---

#### SY-06 — Change tracking's first call is a full re-seed; token expiry throws and forces re-seed

**Classification:** Hard mechanism (this is the reconciliation primitive). **Origin:** MS (T1).

**Evidence** (`S-04`, ms.date 2026-03-31)
Re-seed: "The first time you use this message, it returns all records for the table. You can use that data to populate the external storage. The message also returns a version number that you send back with the next use of the `RetrieveEntityChanges` message so that only data for those changes that occurred since that version is returned."
Tokenless call = full re-seed, deletes lost: "You can track only one table in retrieve changes. If you execute `RetrieveEntityChanges` with no version or token, the server treats it as the system minimum version and returns all of the records as new. Deleted objects aren't returned."
Expiry throws: "Changes are returned if the last token is within a default value of seven days. The value of the Organization table ExpireChangeTrackingInDays column controls this duration and can be changed. If unprocessed changes are older than the configured value, the system throws an exception."
Tombstone over-delivery: "If a client has a set of changes for a table, say version 1, a record is created and deleted before the next query for changes, the client gets the deleted item even if they didn't have the item to begin with."
Ordering and paging: "Records are retrieved in the order determined by server side logic. Usually, the caller gets all new or updated records first (sorted by version number) followed by deleted records. If there are 3,000 records created or updated and 2,000 records deleted, Dataverse returns a collection of 5,000 records for standard tables, which have the first 3,000 entries comprised of new or updated records and the last 2,000 entries for deleted records." And: "If the new or updated item collection is greater than 5,000, the user can page through the collection."
Privilege: "The calling user must have organization level read access to the table. If the user has limited read access, the system throws a privilege check error."
Irreversible: "After you enable change tracking for a table, you can't disable it."
Web API delta-link restrictions: "System query options `$filter`, `$orderby`, `$expand`, and `$top` aren't supported when you use the `Prefer: odata.track-changes` header in a Web API request." Error text: `The \"${filter|orderby|expand|top}\" query parameter isn't supported when Change Tracking is enabled.`
Count helper: "To get the number of changes, add `$count` to the delta link returned from the initial change tracking request."

**Why it matters**
This is the whole drift-repair story in one page. There is no partial repair primitive: either you have a valid token and get a delta, or you have nothing and must re-seed the entire table. Re-seed does not carry deletes, so a re-seed after expiry leaves orphan rows in the target unless the target is truncated or a separate delete-detection pass runs.

**Decision impact**
Data requirement: keep a replica converged with Dataverse and repair it after an outage → constraint: token valid ≤ ExpireChangeTrackingInDays (default 7); expired token throws; tokenless re-seed returns all rows as new and **no deletes**; delta feed cannot be filtered or ordered → architectural implication: (1) persist the token durably and monitor its age against the org's ExpireChangeTrackingInDays with an alert well inside the window; (2) design the re-seed path as truncate-and-reload, or pair re-seed with a target-side anti-join to remove rows absent from the seed; (3) an outage longer than the expiry window is a *re-seed event*, so size the re-seed (rows, time, service-protection budget) before go-live, not during the incident.

**Conditions:** `RetrieveEntityChanges` (.NET SDK) and `Prefer: odata.track-changes` (Web API) are the two surfaces; the `$count` on a delta link is the cheapest available "how far behind am I" signal.
**Confidence:** High.
**Sources:** S-04.

---

#### SY-07 — Microsoft's own Dataverse-to-Dataverse sync reference architecture makes a scheduled bulk job the reconciliation mechanism

**Classification:** Design pattern, Microsoft-endorsed. **Origin:** MS (T1).

**Evidence** (`S-05`, ms.date 2026-04-30)
Bulk path: "Each dataflow connects to the primary Dataverse environment as its data source." "Dataflows run on a fixed schedule (for example, nightly or after another dataflow runs successfully) or on demand (for example, for initial setup)."
Idempotency: "Upserts are performed by using an alternate key to avoid duplicates. This method updates existing data and inserts new records when no match exists."
The explicit reconciliation section, verbatim, is two bullets — "**Error handling and reconciliation**": "Nightly dataflows in the secondary environment correct any missed or failed event-driven updates." and "Manual intervention might be required for data quality problems (for example, missing keys)."
Reliability pillar, verbatim: "Nightly dataflows ensure consistency." / "Event-driven flows deliver fast updates." / "Manual monitoring detects data quality issues."
Stated gap that forces a compensating flow: "Status fields are managed through a dedicated 'sync status' column. A Power Automate flow updates the actual status field accordingly. This flow runs after the dataflow and is required because a dataflow can't change row statuses or delete records that are removed (absent) in the primary Dataverse environment."
Stated scope limit: "This architecture is designed for a one-to-one relationship: a single master data management (MDM) environment linked to another single environment. Scenarios where one master environment must synchronize with multiple other environments require a more scalable or distributed solution."
Throughput caveat: "High-frequency CRUD activity can trigger throttling, especially in scenarios where flows execute tens of thousands of actions per day."
Operational friction: "after each deployment, you must manually re-establish the dataflow connection" and "When using dataflows, you can't assign service principals as owners."

**Why it matters**
This is the closest thing Microsoft publishes to a reconciliation design for Dataverse replication, and it is deliberately unglamorous: a **full-scan scheduled upsert that overwrites whatever the event stream got wrong**. No row-level comparison, no hash, no diff report. Drift is not *detected* — it is *overwritten*. Deletes and status changes fall outside the dataflow's power and need a separate Power Automate flow. Microsoft names manual intervention and manual monitoring as parts of the design, not as failures of it.

**Decision impact**
Data requirement: keep two stores converged with acceptable staleness → constraint: dataflows cannot delete rows or change statuses; the event path can silently miss; the correcting job is a scheduled full upsert → architectural implication: budget three components per synchronized table, not one — (a) event-driven near-real-time path, (b) scheduled full-scan upsert keyed on an alternate key, (c) a delete/status compensation flow; and accept that the design's convergence guarantee is only as fresh as the schedule of (b).

**Conditions:** Written for Dataverse→Dataverse; the pattern generalizes but the quoted limitations are Power Platform dataflow limitations. One-to-one only.
**Confidence:** High (the quotes are the architecture's own reliability section).
**Sources:** S-05.

---

#### SY-08 — Dual-write is the only Microsoft-operated bidirectional sync with play/pause/catch-up, initial sync and an error dashboard — and it is scoped to finance and operations apps

**Classification:** Comparator / bounded precedent. **Origin:** MS (T1).

**Evidence** (`S-06`, ms.date 2026-01-15; `S-11`, ms.date 2026-04-03; `S-10`, ms.date 2026-01-15)
What the infrastructure claims (`S-06`): "Synchronous and bidirectional data flow between applications"; "Synchronization, together with play, pause, and catchup modes to support the system during online and offline/asynchronous modes"; "Ability to sync initial data between the applications"; "Combined view of activity and error logs for data admins"; "Ability to configure custom alerts and thresholds, and to subscribe to notifications".
Scope: "Dual-write provides tightly coupled, bidirectional integration between finance and operations apps and Dataverse."
Concrete state machine (`S-11`) — documented statuses **Not running / Initializing / Running / Paused / Resuming**. Verbatim: "The table map then goes through an initialization phase, where it does an initial write by copying pre-existing data on tables on both sides. When the table is completely enabled, it changes the status of the table map to **Running**."
Pause semantics: "While the status is **Running**, you can pause a table. All changes are then queued until you resume. When you resume, the table enters 'catch-up mode' and plays back all the queued changes." Status table: "Paused | The table is in a paused state, and all new requests are queued." / "Resuming | The table is catching up on rows that were queued while the table was paused."
Conflict resolution at seed time: "During data synchronization, if records that have the same keys are found on both sides, and the keys have competing attribute values, a merge conflict occurs. In this case, you must select a **Master for initial sync** value for every entity map in the list to specify the master data that should be used to resolve conflicts. By default, Dataverse is used." Caveat: "The **Master for initial sync** value is used only to resolve conflicts. It doesn't control the direction that data should move in."
Initial-sync error loop: "If any errors occur, you can view the details on the **Initial sync details** tab. This tab shows details about all the errors that occur while pre-existing data is copied. After you fix the underlying errors, you can rerun the execution and monitor the outcome." Escape hatch: "if you no longer want to sync the pre-existing data, or if you experience recurring issues because of underlying data, you can skip the initial write phase. Instead, you can turn on live writes by selecting **Skip initial sync**."
Key requirement: "To enable table maps for dual-write, you must define an alternative key in Dataverse. The key that you define in the finance and operations app must match the value of the alternative key in Dataverse."
Dependency ordering: "Because these apps have relational data, if you don't enable the dependent tables, you might encounter errors later. To help prevent these errors, before you enable a table map, the system provides a list of the related tables that you should enable." And: "You can also drag the table maps to change the order that they'll be synced in."
Error surfaces in practice (`S-10`): plug-in trace log — "Setting the dropdown to **Exception** only provides trace information when exceptions (errors) occur"; F&O side — "there's a flag **IsDebugMode** on the **DualWriteProjectConfiguration** table" and "The verbose logs are stored in the **DualWriteErrorLog** table"; and a third surface, the VM event log at "**Applications and Services Logs > Microsoft > Dynamics > AX-DualWriteSync > Operational**".

**Why it matters**
Dual-write is the existence proof of what a properly operated two-way sync needs: a per-table state machine with pause/catch-up, an initial seed with an explicit conflict master, dependency-ordered enablement, alternate keys as the join, and dedicated error tables. None of that comes for free in a Dataverse↔Azure SQL design — but a design that omits any of it is omitting something Microsoft found necessary. Note also `S-10`: even in the first-party product, diagnosing a sync failure means three separate log surfaces and system-admin rights.

**Decision impact**
Data requirement: bidirectional or repairable sync between Dataverse and another store → constraint: dual-write does not apply outside finance and operations apps, so its machinery must be rebuilt → architectural implication: specify explicitly, per synchronized table, (1) the alternate key that joins the two sides, (2) the conflict master for the seed, (3) the enablement/seed order across dependent tables, (4) a pause/queue/catch-up mechanism for planned outages, (5) a persistent error table with a rerun path. Name the owner of the error dashboard before go-live.

**Conditions:** Dual-write is not available for a Dataverse↔Azure SQL pairing. Quoted as a design template and as evidence of required operational surface, not as an option.
**Confidence:** High.
**Sources:** S-06, S-10, S-11.

---

#### SY-09 — Service Bus dead-lettering: the reasons are enumerated, and replay is a manual operator action

**Classification:** Hard mechanism. **Origin:** MS (T1).

**Evidence** (`S-07`, ms.date 2026-07-16)
Purpose: "The purpose of the dead-letter queue is to hold messages that can't be delivered to any receiver, or messages that couldn't be processed. Messages can then be removed from the DLQ and inspected. An application might let a user correct issues and resubmit the message."
System reasons, verbatim from the table: `HeaderSizeExceeded` — "The size quota for this stream exceeded the limit."; `TTLExpiredException` — "The message expired and was dead-lettered."; `Session ID is null` — "Session enabled entity doesn't allow a message whose session identifier is null."; `MaxTransferHopCountExceeded` — "The maximum number of allowed hops when forwarding between queues exceeded the limit. This value is set to 4."; `MaxDeliveryCountExceeded` — "Message couldn't be consumed after maximum delivery attempts."
Delivery count: "There's a limit on the number of attempts to deliver messages for Service Bus queues and subscriptions. The default value is 10. Whenever a message is delivered under a peek-lock, but is either explicitly abandoned or the lock has expired, the delivery count on the message is incremented. When the delivery count exceeds the limit, the message is moved to the DLQ." And: "This behavior can't be disabled, but you can set the max delivery count to a large number."
DLQ does not self-clean and does not expire: "In addition, time-to-live isn't observed, and you can't dead-letter a message from a DLQ." "There's no automatic cleanup of the DLQ. Messages remain in the DLQ until you explicitly retrieve them from the DLQ and complete the dead-letter message."
Paths: `<queue path>/$deadletterqueue`, `<topic path>/Subscriptions/<subscription path>/$deadletterqueue`, transfer DLQ at `<queue path>/$Transfer/$DeadLetterQueue`. Location matters: a failed forward "is placed in the *transfer dead-letter queue* (TDLQ) of the **source** entity that did the forwarding, not on the destination entity."
Silent-loss trap: "If you close the receiver or its connection before you settle a message (complete, abandon, defer, or dead-letter), the settlement doesn't reach the service, so the message stays locked until the lock expires. The service then redelivers the message, which increases its delivery count. A message that's repeatedly received but never settled is eventually moved to the dead-letter queue with the reason `MaxDeliveryCountExceeded`." Also: "The service closes an idle connection after 10 minutes, which also releases the lock." And: "A lost lock isn't always caused by your code. Transient network failures, network outages, or the service-enforced 10-minute idle timeout can also detach the connection before you settle a message."
Replay: "Once you resolve the issue that caused a message to be dead-lettered, you can resubmit it to the queue or topic to be reprocessed. The simplest approach is to use Service Bus Explorer in the Azure portal, which lets you peek messages in the dead-letter queue, edit their content or properties if needed, and resend them - individually or in batches."

**Why it matters**
The DLQ is where drift is *stored*, not where it is *fixed*. Nothing drains it. A message sitting in a DLQ is a row that exists on one side and not the other, indefinitely, and the platform's own answer to replay is a portal tool an operator clicks. A design with a Service Bus outbound channel and no DLQ monitor has a silent, unbounded divergence backlog.

**Decision impact**
Data requirement: durable outbound propagation of Dataverse changes → constraint: DLQ has no TTL and no auto-drain; default max delivery count 10; messages can be dead-lettered for reasons outside the handler's code (lock loss, 10-minute idle timeout) → architectural implication: make DLQ depth a monitored, alerted SLO metric with a named owner and a target of zero; build (or explicitly assign to an operator with Service Bus Explorer) a replay path; make every consumer idempotent, because replay re-delivers.

**Conditions:** Also monitor `TransferDeadLetterMessageCount` on any forwarding entity — TDLQ messages sit on the *source*, so a monitor pointed at the destination sees nothing.
**Confidence:** High.
**Sources:** S-07.

---

#### SY-10 — Microsoft's own resilient-sync reference architecture: latest-snapshot re-fetch, retry counter, DLQ, ack queue

**Classification:** Design pattern, Microsoft-endorsed. **Origin:** MS (T1).

**Evidence** (`S-13`, ms.date 2025-10-09)
Outbox on the Dataverse side: "The system creates a notification message based on the row data and adds an internal record to a dedicated table before trying to send it, including the notification content, to the Service Bus." Then: "After the message reaches the Service Bus, the system deletes the internal record to confirm delivery." Failure path: "If the plugin can't reach the Service Bus, it updates the internal record's status to show the failure and the reason. This setup lets you resend the message by running a retry process on this table."
Bounded retry then DLQ: "If any errors happen, including temporary ones, the system returns the notification message to the initial queue and schedules it for retry up to X times. The notification message has a **RetryCount** property to track the number of tries. If it hits a set threshold (which is better if it's configurable), the system moves the message to the *dead-letter queue* (DLQ). Otherwise, it reschedules the message in the outbound queue with an exponential backoff, so the delay between retries grows each time."
The anti-stale-write rule — the single most important sentence for drift repair: "An Azure Function gets the current state of the record from Dynamics 365 or Dataverse by using the details in the notification message (**Source Row ID**)." and "An Azure Function gets the current state of the record from Dataverse before sending it. This approach makes sure the system never sends outdated values, so you avoid data inconsistencies." And: "This mechanism also makes sure that automatic or manual retries don't overwrite newer data with older snapshots."
Separate acknowledgment channel: "The main reason for using a second queue is to make sure that if the next step—reaching the Dynamics 365 or Dataverse instance—doesn't work, only the acknowledgment process is retried, not the whole dataflow." The ack carries "both integration keys (**Source Row ID** and **Target System Row ID**)".
Failure containment claim: "If a message fails after multiple retries, the system moves it to the dead-letter queue for manual intervention. This process makes sure no data is lost."
Traceability: "the system logs all telemetry in Application Insights by using a correlation ID for traceability and troubleshooting."
Ordering and idempotency: "Use session-enabled queues or correlation tokens to preserve message order when required." / "Ensure idempotency in API logic and message handlers."
Throttling mitigations named: "Distribute loads across service principles rather than a single user."; "Disable Affinity Cookie so Dataverse doesn't use sticky sessions, allowing requests to be load balanced across different front-end servers."; "Batch requests where possible using XMultiples or Batch APIs."; "Introduce exponential backoff in custom code and integrations."; "Use Azure Durable Functions or Logic Apps with delay/retry policies."
Monitoring: "define alert rules on queue length, execution time, and failure rates."

**Why it matters**
This is the reference answer to "how do I repair without making it worse". The payload is a *notification*, not the data; the worker re-reads current state at send time. That single choice makes retry and manual replay safe by construction — a replayed message from three days ago still writes today's values. Any drift-repair design that ships row snapshots in the message instead is buying a stale-overwrite bug.

**Decision impact**
Data requirement: repairable propagation of Dataverse changes to a target store → constraint: retries and manual replays are inevitable, and a snapshot payload makes them destructive → architectural implication: (1) send notifications carrying only the row id, re-fetch state at send time; (2) keep an outbox table in Dataverse so a failure to reach the bus is itself recoverable; (3) carry a RetryCount and a configurable DLQ threshold; (4) separate the acknowledgment queue from the delivery queue; (5) store the target-system key on the source row so reconciliation has a key join rather than a fuzzy match; (6) correlation id end to end.

**Conditions:** Written for Dynamics 365 Sales → external target with an acknowledging target system. Microsoft states the trade-off plainly: "The system retrieves the latest snapshot, ensuring data accuracy, but might introduce slight processing delays."
**Confidence:** High.
**Sources:** S-13.

---

#### SY-11 — Dataverse background operations retry three times with exponential backoff, then stop

**Classification:** Hard constraint. **Origin:** MS (T1).

**Evidence** (`S-12`, ms.date 2025-04-17)
"**Error handling:** If an error occurs during the execution of a background operation, Dataverse employs a retry mechanism. The system retries the failed request up to three times, using an exponential backoff strategy."
Completion signalling: "On completion of a background operation, you receive notifications by: Including a callback URL with your request. Subscribing to the `OnBackgroundOperationComplete` event."
Plug-in timeout still applies: "When using Dataverse background operations to execute requests asynchronously, the two-minute execution time-out applies to any plug-ins invoked during the process."
Well-Architected guidance on the same page: "Anticipate potential failures by incorporating comprehensive error-handling mechanisms. Manage transient faults using retry policies with exponential backoff."

**Why it matters**
Three attempts is the platform's entire automatic-repair budget for a background operation. Beyond that the operation is simply failed and something outside Dataverse must notice. There is no platform-side dead-letter for it and no built-in replay; the `OnBackgroundOperationComplete` subscription is the only hook.

**Decision impact**
Data requirement: asynchronous Dataverse-side processing that must not silently drop work → constraint: three retries with exponential backoff, then failure; two-minute plug-in timeout persists → architectural implication: subscribe to `OnBackgroundOperationComplete` (or supply a callback) and persist every terminal failure to a table that a scheduled reconciliation job reads; do not treat "background operation" as durable delivery — it is bounded retry, not a queue.

**Conditions:** The developer page linked from `S-12` is titled "Background operations (preview)"; GA status not verified here (U-04).
**Confidence:** High for the retry number (verbatim). Medium on production readiness.
**Sources:** S-12.

---

#### SY-12 — Power Automate resubmit: 20 runs at a time, 28-day history, no duplicate protection

**Classification:** Hard constraint (operational repair ceiling). **Origin:** MS (T1).

**Evidence** (`S-14`, ms.date 2026-04-21)
Batch ceiling: "You can resubmit or cancel up to 20 flow runs at a time."
Connector budget binds it: "The number of flow runs that you can resubmit is limited by the maximum number of API calls for the connectors in the flow."
History window: runs are reached via "the flow name > **All runs** from the **28-day run history** list."
Permission gate: "Users can always resubmit their own flow runs initiated by instant triggers. To allow users to also resubmit flow runs initiated by other users, enable the **Power Automate flow run resubmission** setting in the Power Platform admin center." Tenant flag `powerPlatform.powerAutomate.disableFlowRunResubmission`, and "It takes approximately an hour for the function to become enabled after the PowerShell commands are applied."
Throttle deadlock during mass failure: "If the flow was throttled, the queue remains stuck until you assign one or more Power Automate Process licenses to give the flow additional capacity. Each Process license adds 250,000 actions per day, and up to 10 can be stacked on a single cloud flow."
Bulk cancel is slow: "This process can take up to 24 hours."
Microsoft's product documentation on resubmission also warns that resubmitting a run which creates records or sends emails can produce duplicated data or emails, that the flow should already include error handling and retry policies, and that the input data must still be valid — deleted files or records change the outcome of a resubmitted run.

**Why it matters**
"Just resubmit the failed runs" is the reflexive answer to sync failure in a Power Platform design, and it does not scale: 20 at a time, capped by connector API limits, only within the run-history window. A weekend-long integration outage produces more failed runs than this path can practically repair, and each resubmission risks duplicates unless the flow is idempotent.

**Decision impact**
Data requirement: repair a backlog of failed integration runs → constraint: 20 per batch, run history window, connector API limits, no duplicate protection, cross-user resubmit needs a tenant setting with ~1h activation → architectural implication: do not make flow resubmission the reconciliation strategy above trivial volume; make the scheduled reconciliation job (SY-07) the repair mechanism and treat resubmit as a spot fix. Make every writing flow idempotent (alternate-key upsert) so a resubmit is safe. Enable the tenant resubmission setting during build, not during the incident.

**Conditions:** Run-history retention governs how far back repair is possible; verify per environment/licence (U-05).
**Confidence:** High for the quoted limits.
**Sources:** S-14.

---

#### SY-13 — Dataflow Gen2 incremental refresh does reach Azure SQL Database — with replace-only semantics and no delete propagation

**Classification:** Enabling path with hard constraints. **Origin:** MS (T1).

**Evidence** (`S-15`, ms.date 2025-07-23)
Destinations, verbatim: "These data destinations support incremental refresh: Fabric Lakehouse, Fabric Warehouse, Azure SQL Database."
Preconditions: "A data source that supports folding (recommended) and contains a Date/DateTime column for filtering data"; "Make sure your query fully folds, which means the query gets pushed down to the source system."; "default destination configuration is not supported for incremental refresh. You must explicitly define the destination in your query settings."
Mechanism: "If the maximum value changed for that bucket, the dataflow gets the whole bucket and replaces the data in the destination. If the maximum value didn't change, the dataflow doesn't get any data." And: "It uses a 'replace' approach: first it deletes the old data for that specific bucket, then it inserts the fresh data."
The critical omission, verbatim: "**The only supported update method in the data destination is `replace`**", together with "The dataflow doesn't remove any data from the destination that's outside the bucket range. If you have data in the destination that's older than the first bucket, incremental refresh doesn't affect it."
Bucket ceilings: "Each query can handle up to 50 buckets." / "For your entire dataflow, the limit is 150 buckets total."
Schema rigidity: "The data destination must be set to a fixed schema, which means the schema of the table in the data destination must be fixed and can't change."
Conversion trap: "Switching from non-incremental to incremental refresh with existing overlapping data in the destination is not supported."
Ordering trap: "set up a data destination for the query. Do this before the first incremental refresh, or your destination will only contain the incrementally changed data since the last refresh."
Duplicate hazard: "If data shifts between buckets, the dataflow might not detect the changes correctly and might create duplicated data in your destination."
Lakehouse-specific: "Maximum number of concurrent evaluations is 10." and "if other tools (like Spark) or processes also write to the same table, they can interfere with incremental refresh. We recommend avoiding other writers while using incremental refresh."
Source-pressure control: "Go to your dataflow's global settings and look for the parallel query evaluations setting. Set this to a lower number to reduce the requests sent to your source system."

**Why it matters**
This is the one documented, first-party-configured path that lands Dataverse-shaped data into **Azure SQL Database** on a schedule without hand-written code — the closest thing to what "replicated read model" implies. But its update method is bucket-replace over a DateTime column. A Dataverse row deleted outright, or a row whose `modifiedon` moves it between buckets, is not correctly reconciled: deletes leave orphans, bucket-shifting rows duplicate.

**Decision impact**
Data requirement: scheduled incremental Dataverse→Azure SQL read model → constraint: replace-only per DateTime bucket; deletes never propagate; ≤50 buckets/query and ≤150/dataflow; fixed schema; folding required → architectural implication: usable for append/update-heavy reporting tables keyed on `modifiedon`; **not** usable alone where deletes matter — pair with a periodic full anti-join delete pass, or drive deletes from change tracking (SY-06). Choose the change-detection column deliberately and never reuse the filter column for it.

**Conditions:** Whether the Dataverse source folds under real transformations is not asserted by this page (U-02). Dataflow refresh-cadence limits (already established) still bound freshness.
**Confidence:** High for the quoted limits; Medium on folding behaviour in practice.
**Sources:** S-15.

---

#### SY-14 — Synapse Link's own FAQ documents the concrete ways a lake replica silently diverges from Dataverse

**Classification:** Hard constraint / drift catalogue. **Origin:** MS (T1). **Most decision-relevant finding for drift detection.**

**Evidence** (`S-17`, ms.date 2026-09-01)
**Secured columns look synced but are null:** "If a table syncs successfully but specific columns contain null values for every row, check whether column-level security is enabled on those columns." "When a column is secured, the application user must be granted read access to that column through a column security profile. If the application user isn't added to the profile that secures the column, the sync completes successfully and all other columns export as expected, but the secured column is exported as null." Repair is not retroactive: "After you grant read access, the values are exported with the next data change on the affected rows. Rows that aren't updated continue to show null until the record changes or you resynchronize the table." The app user is named: "**Dynamics365Athena2**".
**New columns don't appear until a data change:** "Azure Synapse Link syncs metadata changes together with data changes—it doesn't trigger an independent sync for a metadata-only change." "If no data change occurs after the column is added, the new column remains only at the source and isn't synced automatically." "To bring in the new column immediately when no data change is expected, resynchronize the affected tables."
**Deleted columns are not dropped:** "When you delete a column from a table in the source, the column isn't dropped from the destination. Instead, the rows are no longer updated and are marked as null while preserving the previous rows."
**Type change is breaking:** "Changing the data type of a column is a breaking change and you need to unlink and relink."
**Calculated columns go stale invisibly:** "If a calculated column value changes without a corresponding version change to the record, the updated value isn't synchronized to the data lake until the record is updated and its version changes." "if a calculated column evaluates to `NULL` during the initial synchronization, `NULL` is written to the data lake. If the inputs used by the calculation change later but the record version doesn't change, Azure Synapse Link won't detect the recalculated value and the data lake continues to show `NULL`."
**Direct SQL deletes never propagate:** "For any direct SQL call to remove a record, the Azure Synapse Link for Dataverse service doesn't trigger because BPO.Delete isn't being called."
**Duplicate versions are expected in append-only:** "if Azure Synapse Link for Dataverse doesn't get an acknowledgment from the Azure data lake that the data has been committed due to any reason such as network delays, Azure Synapse Link retries in those scenarios and commit the data again. The downstream consumption should be made resilient to this scenario by filtering data using `SinkModifiedOn`."
**Correct latest-row logic:** "you should identify the latest version of record with the same ID using `VersionNumber` and `SinkModifiedOn` then apply `isDeleted=0` on the latest version."
**Delete semantics differ per mode:** in-place CSV — "the row is also deleted from the corresponding data partition in the Azure Data Lake. In other words, data is hard deleted from the destination."; append-only CSV — "a row is added and set as `isDeleted=True`"; Delta — "Azure Synapse Link performs a soft delete on data during the next delta synchronization cycle, followed by a hard delete after 30 days."
**Latency measurement is a trap:** "the difference between `SinkCreatedOn` and `CreatedOn` in these modes isn't a reliable indicator of sync delay and shouldn't be interpreted as such." And: "Use caution when building latency reports based on the difference between `SinkModifiedOn` and `ModifiedOn`, as it can give a misleading impression of actual data availability."
**Excluded data:** "Azure Synapse Link doesn't sync file content stored on the `annotation` (Notes) table." — "`annotation` records that have a value in the `documentbody` column (notes with a file attachment) aren't exported to the data lake." Unsupported tables: "Any table that doesn't have change tracking enabled isn't supported in addition to following system tables: Attachment, Calendar, Calendarrule."
**Per-record size cap:** "The most common limit is the 200 MiB cap on the uncompressed size of a single record returned by the server." "This is a Dataverse platform limit and can't be raised on request."
**Not an archive:** "Azure Synapse Link for Dataverse is designed for analytics purposes. We recommend customers use long-term-retention for archive purposes."
**Do not touch the files:** "Data files shouldn't be modified by a customer and no customer files should be placed in the data folders."

**Why it matters**
Every item above is a way the replica is *wrong while reporting success*. None raise an error. Several — secured columns exporting null, calculated columns frozen at their initial value, direct-SQL deletes never replicating, notes with attachments simply absent — produce a replica that a naive row-count comparison declares healthy. This is the concrete answer to "how do I detect drift": row counts are insufficient, and Microsoft's own remedy for most of these is **resynchronize the table**.

**Decision impact**
Data requirement: trustworthy replicated read model over Dataverse → constraint: at least eight documented silent-divergence modes → architectural implication: (1) grant the Synapse Link application user `Dynamics365Athena2` Read on every column security profile covering exported columns, **before** first sync; (2) never expose calculated columns through the replica — recompute downstream; (3) treat schema change in Dataverse as a resync trigger, not a no-op; (4) forbid direct-SQL deletion paths on replicated tables; (5) build latest-row logic on `VersionNumber` + `SinkModifiedOn` + `isDeleted=0`; (6) do not build sync-latency SLOs on `SinkModifiedOn − ModifiedOn`; (7) budget "resynchronize table" as a routine operation with a known cost.

**Conditions:** Specific to Azure Synapse Link. Link to Fabric shares the change-tracking foundation, so change-tracking-derived items likely carry over — inference, not quoted (U-01).
**Confidence:** High (verbatim, ms.date 2026-09-01, current at research date).
**Sources:** S-17.

---

#### SY-15 — Synapse Link pauses rather than fails, and several pauses are caused by changes outside the Dataverse team's control

**Classification:** Hard constraint (operational). **Origin:** MS (T1).

**Evidence** (`S-18`, ms.date 2026-09-01)
Framing: "you might see an error with a message and link to this article. In addition, users might also see **Error** status next to tables that are already in an Azure Synapse Link profile."
The recurring phrase across the error table is "**Data updates are paused.**" — `MSI-801`, `ADLS-802`, `CT-803`, `SPARK-807`, `CT-809`, `FnO-810`.
Selected causes, verbatim:
- `ADLS-802`: "Azure Synapse Link service can't access storage account and the service has paused. Permissions associated with storage account assigned to Azure Synapse Link profile might have changed or the storage account doesn't exist."
- `DV-804`: "When a Power Platform environment is in administration mode all services including Azure Synapse Link service are temporarily paused." Second gate on recovery: "Also verify that the **Background operations** environment setting is **Enabled** after **Administration mode** is **Disabled**."
- `SPARK-808`: "When a large batch of data is available for update, the size of the Spark pool provided in the Azure Synapse Link profile might not provide sufficient compute power. This can happen especially when you add large tables as the initialization process creates a large batch of data."
- `SYN-805`: "Synapse tables might not be created immediately when you resolve this issue. The system creates tables in the Synapse workspace when data gets updated in Dataverse."
- `SYN-809`: "Synapse Link profiles with Delta conversion option requires Synapse workpaces without data exfiltration policies." — resolution suggests "You might also consider using Fabric link as an alternative to Synapse Link."
- `CT-803` forces re-initialization: "Enable the configuration key and remove and readd finance and operations apps tables to resume. Impacted tables are initialized to reflect new data."
- `FnO-813` explicitly does not: "The system resumes once the data issue has been resolved. You don't need to reinitialize the table."

**Why it matters**
Pausing is worse than failing for drift purposes: the replica keeps answering queries, just frozen at the pause point. Consumers see a consistent, plausible, stale dataset. Two pause causes — a storage-account permission change and putting the environment in administration mode — are routine acts performed by *other* teams who have no reason to know they just froze a downstream warehouse. `SYN-805` adds a second-order trap: after the access problem is fixed, tables still don't appear until data changes in Dataverse, so "fixed" and "recovered" are different moments.

**Decision impact**
Data requirement: dependable freshness of the replicated read model → constraint: the link pauses silently on causes owned by other teams; some errors force re-initialization; recovery is data-change-triggered → architectural implication: (1) monitor link freshness *from the consumer side* (max `SinkModifiedOn` age per table against an expected bound) rather than trusting an absent error; (2) add "Synapse Link / Fabric Link is downstream of this" to the change-control checklist for the storage account, the Synapse workspace, and environment administration mode; (3) publish a freshness stamp with every report built on the replica so consumers see staleness rather than infer it.

**Conditions:** Error codes are Synapse Link specific; Link to Fabric has its own surface (not researched here).
**Confidence:** High.
**Sources:** S-18.

---

#### SY-16 — Synapse serverless SQL over the lake: read-only, per-query cost, explicitly analytics-scoped

**Classification:** Hard constraint. **Origin:** MS (T1), but on a materially stale page.

**Evidence** (`S-16`, ms.date **2021-08-06** — five years old at research date)
"You can use the Azure Synapse Link to connect your Microsoft Dataverse data to Azure Synapse Analytics to explore your data and accelerate time to insight. This article shows you how to query your Dataverse data with built-in serverless SQL pool in your Azure Synapse Analytics workspace."
Hard exclusion: "Azure Synapse Link for Dataverse does not support the use of dedicated SQL pools at this time."
The surface is a lake database of external tables: "Expand **Lake database**, select your Dataverse container. Your exported tables are displayed under the **Tables** directory on the left sidebar." Entry point: "**New SQL script** > **Select TOP 100 rows**".
Cross-environment join requires co-location: "Querying multiple Dataverse databases requires that both Dataverse environments are in the same region."
Access prerequisites: "You must be granted one of the following roles for the storage account: Storage Blob Data Reader, Storage Blob Data Contributor, or Storage Blob Data Owner." Plus "You must be granted the **Synapse Administrator** role access within Synapse studio."
Cost model (`S-17`): "Azure Synapse Link is a free feature with Dataverse. Utilizing Azure Synapse Link for Dataverse doesn't incur additional charges under Dataverse. However, consider potential costs for the Azure service: Data storage in Azure Data Lake Storage Gen2 ... Data consumption cost (such as Synapse Workspace)". The cost of *reading* is therefore an Azure-side, consumption-based charge, not a Dataverse charge.
Query-time instability on CSV (`S-17`): "Dataverse data can continuously change through creating, updating, and deleting transactions. This error is caused by the underlying file being changed when you read data from it. So, for tables with continuous changes, change your consumption pipeline to use snapshot data (partitioned tables) to consume."
Storage role needed to query at all (`S-17`): "You need the 'Storage Blob Data Contributor' role in the linked storage account to perform read and query operations through Synapse Workspace."
Not the operational store (`S-17`): "Azure Synapse Link for Dataverse is designed for analytics purposes."
Read-only nature of serverless synchronized objects and external tables is asserted in the Synapse SQL documentation (`S-19`) — **surfaced via search summary only, not fetched verbatim**; treated as unverified (U-09).

**Why it matters**
The serverless surface answers "can I do SQL over Dataverse data" with yes, and "can I use it as the application's SQL store" with no — read-only, consumption-billed, and files that can move under a running query. The Dataverse-specific page's 2021 date is itself a signal that Microsoft's investment has moved to Link to Fabric.

**Decision impact**
Data requirement: SQL access to exported Dataverse data → constraint: serverless only (no dedicated pools), consumption cost, same-region requirement for cross-environment joins, CSV read instability on hot tables, storage RBAC required per consumer → architectural implication: acceptable for analyst/BI access and ad-hoc joins; unacceptable as an application read model with predictable cost or latency. If a bounded-cost, always-on SQL surface is needed, that favours Link to Fabric + capacity over Synapse serverless — and either way it stays read-only (SY-02).

**Conditions:** Page is materially stale. Re-verify before quoting to a client (U-03).
**Confidence:** Medium-High — High on what is quoted, Medium on current accuracy.
**Sources:** S-16, S-17, S-19 (unverified).

---

#### SY-17 — Microsoft's migration guidance mandates verification and rehearsal but supplies no reconciliation method

**Classification:** Guidance + negative finding. **Origin:** MS (T1).

**Evidence** (`S-09`, ms.date 2024-01-17; `S-08`, ms.date 2026-06-17)
Rehearsal is mandated (`S-09`): "You should also test and verify your data migration at least once in your system integration testing (SIT) and user acceptance testing (UAT) environments."
Isolation of the exercise: "data migration activities can be a disruptive task and shouldn't coexist with other testing activities."
Verification is a listed planned activity: "Verifying and validating the data quality and accuracy in your Dynamics 365 solution." In the roles table the "Data migration architect/developer" is the one who "Transforms and tests data. Validates and verifies data quality and accuracy." The "Data steward" "Maintains and manages data according to data properties and standards."
The migration strategy must state mode and direction per entity: "The data entities and tables that you'll migrate and their volumes and characteristics, such as direction relative to Dynamics 365 (from, to, or both), mode (full push or incremental), and frequency (one-time or recurring)".
Environment sizing: "We recommend that you procure a dedicated high-tier data migration environment that's sized appropriately to handle the volume of data in scope. We also recommend that you have all databases and environments running under the same location and region and with acceptable latency."
Cutover is planned: the strategy covers "The pre-cutover and post-cutover data migration activities that you'll perform."
Golden config environment: "A golden configuration environment is a separate environment that you use only for configuration data. You don't create any transactions or test data in this environment."
ETL tool options, verbatim: "Data import/export wizards", "Azure Data Factory or Azure Synapse Analytics", "SQL Server Integration Services (SSIS)", "Non-Microsoft integration products".
**Negative finding:** across `S-08` and `S-09` Microsoft prescribes *that* you verify and validate, and *who* does it — but gives no method. No row-count comparison procedure, no checksum or hash approach, no audit-based verification technique, no reconciliation report template. `S-08` is a 199-word stub that defines configuration vs. migrated data and links onward.

**Why it matters**
Microsoft tells you to reconcile and does not tell you how. Reconciliation logic — what to compare, at what grain, with what tolerance, and what to do about mismatches — is entirely a project deliverable. It must be estimated, staffed and signed off like any other component, and it is routinely forgotten because the guidance's imperative voice makes it sound like a checkbox.

**Decision impact**
Data requirement: assurance that a migration or a replica is correct → constraint: no Microsoft-supplied reconciliation method exists; only a mandate to verify, a named role, and a mandate to rehearse in SIT and UAT → architectural implication: make "reconciliation specification" an explicit deliverable owned by the Data migration architect/developer, covering per-table row counts, per-column null/aggregate checks on business-critical columns, key-set anti-joins in both directions, a documented tolerance and an escalation path. Schedule at least one full mock migration into a correctly sized environment; treat its reconciliation output as the go/no-go artefact.

**Conditions:** `S-09` carries `ms.update-cycle: 1095-days` from 2024-01-17 — Microsoft does not plan to revisit it before 2027.
**Confidence:** High for the quoted mandates; High for the negative (both pages read end to end).
**Sources:** S-08, S-09.

---

#### SY-18 — Synthesis: the three viable Dataverse→SQL/warehouse paths and what each costs in reconciliation work

**Classification:** Synthesis (derived). **Origin:** INF over MS sources — no new quotes.

| Path | Target | Who operates it | Deletes propagate? | Reconciliation burden |
|---|---|---|---|---|
| **Link to Fabric** (established) + SQL analytics endpoint (`S-02`) | Fabric delta-parquet replica, read-only T-SQL | Microsoft | Yes (change-tracking based) | Lowest. Drift is platform-side and pause-shaped (SY-15); monitor freshness, resync. No writable SQL (SY-02); type/truncation caveats (SY-03). |
| **Synapse Link** (established) + serverless SQL (`S-16`) | Customer ADLS Gen2, read-only external tables | Microsoft (link) / customer (storage, workspace, RBAC) | Yes, mode-dependent (`S-17`) | Medium. Documented silent-divergence catalogue (SY-14); consumption cost; stale docs. |
| **Custom pipeline**: ADF/Fabric Data Factory (`S-03`) or Dataflow Gen2 incremental refresh (`S-15`) | Any, incl. **writable Azure SQL Database** | Customer, entirely | **No** | Highest. Watermark, backfill, delete detection, reconciliation job, DLQ/replay all customer-built (SY-04, SY-05, SY-13). |

The decisive asymmetry: **the two managed paths handle deletes; the only path that reaches a writable Azure SQL Database does not.** Dataflow Gen2 is replace-per-bucket (`S-15`); ADF copy activity has no delete semantics on the source side (`S-03`). Deletes must come from change tracking (`S-04`) or a periodic full anti-join — and change tracking's tokenless re-seed explicitly excludes them ("Deleted objects aren't returned"), so a post-expiry recovery loses delete information twice over.

**Why it matters**
The v2 recommendation ("Dataverse + Azure SQL hybrid", "replicated read models") lands in the third row without saying so. That row has no managed service, no delete propagation, and a customer-owned reconciliation obligation Microsoft mandates but does not specify (SY-17).

**Decision impact**
Data requirement: the read model's actual write/read profile → constraint: writable SQL forces the custom path and its full reconciliation burden → architectural implication: force the choice early with one question — **does anything write to the SQL tier?** If no: take Link to Fabric, delete the Azure SQL component, and the reconciliation problem largely disappears. If yes: accept and budget a watermark store, a delete-detection pass, alternate-key upserts, outbox + DLQ + replay (SY-10), a scheduled full-scan reconciliation upsert (SY-07), and a named owner for the error dashboard (SY-08). Do not present the hybrid as "Microsoft replicates it for you" — it does not (SY-01).

**Conditions:** Valid as of 2026-09-02 against the cited mirroring source list, connector and dataflow documentation.
**Confidence:** High on the composition; underlying facts are Tier-1 verbatim.
**Sources:** S-01 … S-17.

---

---

### 4.9 Azure SQL store-choice evidence: five previously unsourced claims tested (new in v2 — closes review F-01)

v1's store-fit matrix (§2) asserted five Azure SQL/SharePoint cells with no citation at all. The following 16 findings (`SQ2-01`..`SQ2-16`) test each claim against Microsoft Learn. Net verdict (`SQ2-16`): **one claim is right (customer-managed keys), one is wrong (SharePoint CMK), one is contradicted by Microsoft's own guidance (high-ingest telemetry), and two are conditional rather than strong (cheap long retention; nightly bulk load)**. The corrected matrix cells are already applied in §2 above; the findings below are the evidentiary record.

#### SQ2-01 — Azure SQL customer-managed TDE (BYOK) is a real, first-class capability, but server/instance-scoped and operationally fragile

**Classification:** Evidence — SUPPORTS C1 (with conditions)
**Origin:** MS (T1)

**Evidence** [S1]:
- "Transparent data encryption (TDE) in Azure SQL with customer-managed key (CMK) enables Bring Your Own Key (BYOK) scenario for data protection at rest, and allows organizations to implement separation of duties in the management of keys and data."
- "With customer-managed TDE, the customer is responsible for and in a full control of a key lifecycle management (key creation, upload, rotation, deletion), key usage permissions, and auditing of operations on keys."
- Scope: "For Azure SQL Database and Azure Synapse Analytics, the TDE protector is set at the server level and is inherited by all encrypted databases associated with that server. For Azure SQL Managed Instance, the TDE protector is set at the instance level".
- Database-level option exists: "Managing the TDE protector at the database level in Azure SQL Database is available."
- Key store: "the TDE protector ... is stored in either Azure Key Vault or Azure Key Vault Managed HSM"; "Azure Key Vault supporting FIPS 140-2 Level 2 and Azure Key Vault Managed HSM supporting FIPS 140-2 Level 3".
- Revocability (the compliance selling point): "Azure Key Vault administrator can revoke key access permissions to make encrypted database inaccessible."
- Migration cost is low: "data remains encrypted during the process of switching over, and there's no downtime nor re-encryption of the database files. Switching from a service-managed key to a customer-managed key only requires re-encryption of the DEK, which is a fast and online operation."

**Why it matters:** C1 is the one of the five claims that survives intact. Azure SQL supports CMK/BYOK at server, instance and (for SQL DB) database level, backed by AKV or Managed HSM, with a documented revoke-to-deny path.

**Decision impact:** data requirement "encryption key must be customer-controlled / revocable" → constraint "TDE protector in AKV or Managed HSM, with soft-delete + purge protection, server identity granted wrap/unwrap" → architectural implication "Azure SQL is a valid store; but the key becomes a live availability dependency of the database (see SQ2-02), so the CMK decision drags in a key-ops runbook, not just a checkbox."

**Conditions:** Applies to Azure SQL Database, Azure SQL Managed Instance, Azure Synapse. Symmetric (AES) TDE protectors are preview-only.
**Confidence:** High.
**Sources:** S1.

---

#### SQ2-02 — CMK on Azure SQL has hard operational requirements and a documented failure mode (database goes *Inaccessible*)

**Classification:** Evidence — QUALIFIES C1
**Origin:** MS (T1)

**Evidence** [S1]:
- Requirement: "Soft-delete and purge protection features must be enabled on the Azure Key Vault. ... If soft-delete and purge protection aren't enabled on the key vault, the TDE protector setup fails with an error."
- Firewall: "When using a firewall with Azure Key Vault, you must enable the option **Allow trusted Microsoft services to bypass the firewall**, unless you're using private endpoints for the Azure Key Vault."
- Continuous dependency: "When TDE is configured to use a customer-managed key, continuous access to the TDE protector is required for the database to stay online. If the server loses access to the customer-managed TDE protector ... in up to 10 minutes a database starts denying all connections ... and change its state to *Inaccessible*."
- "If the server loses access to the customer-managed TDE protector ... due to any Azure Key Vault error (such as a 4XX error), the database is moved to an inaccessible state after 30 minutes."
- Recovery cliff: "If key access is restored within 30 minutes, the database automatically heals within the subsequent hour. However, if key access is restored after more than 30 minutes, automatic healing of the database isn't possible."
- Collateral loss: "Once the database is back online, previously configured server-level settings, including failover group configurations, tags, and database-level settings such as elastic pool configurations, read scale, auto pause, point-in-time restore history, long-term retention policy, and others are lost."
- Permission latency: "It may take around 10 minutes for any permission changes to take effect for the key vault."
- Backup/restore coupling: "When the TDE protector is changed for a database, old backups of the database **are not updated** to use the latest TDE protector. At restore time, each backup needs the TDE protector it was encrypted with at creation time." And: "Backed up log files remain encrypted with the original TDE protector, even if it was rotated".
- Scale guidance: "Associate **no more than 500 General Purpose databases** with a single Azure Key Vault"; "no more than 200 Business Critical databases"; Hyperscale: "Do not associate more than **500 page servers** with a single Azure Key Vault."

**Why it matters:** The unsourced file rated Azure SQL "STRONG" for CMK as if it were free. It is supported, not free: CMK converts the key vault into a tier-0 availability dependency with a 30-minute recovery cliff and a loss of LTR policy/PITR history on the slow path.

**Decision impact:** data requirement "customer-controlled key" → constraint "AKV soft-delete + purge protection + firewall bypass or private endpoint; every historical key version retained for restore" → architectural implication "add key-access monitoring with <30 min alerting; treat key rotation as a backup-compatibility event; budget a dedicated key vault for the SQL estate."

**Conditions:** All Azure SQL CMK deployments.
**Confidence:** High.
**Sources:** S1.

---

#### SQ2-03 — Comparison point: Dataverse CMK vs Azure SQL CMK scope

**Classification:** Evidence — context for C1
**Origin:** MS (T1)
**Status:** Resolved — the full side-by-side (licence gates, scope, switch-on cost, coverage gaps) is in **SQ2-09** below. Headline: Azure SQL CMK has no licence gate beyond the Azure subscription; Dataverse CMK requires Managed Environments **and** an E5-class compliance SKU for users in the environment.

---

#### SQ2-04 — Long-term retention in Azure SQL is *backup* retention, not a queryable read-only archive

**Classification:** Evidence — CONTRADICTS C2 as stated
**Origin:** MS (T1)

**Evidence** [S2]:
- "Long-term retention can be configured for up to 10 years on backups for Azure SQL Database (including in the Hyperscale service tier) and Azure SQL Managed Instance."
- "By using the LTR feature, you can store specified full SQL Database and SQL Managed Instance backups in redundant Azure Blob storage with a configurable retention policy of up to 10 years. **LTR backups can then be restored as a new database.**"
- Granularity is coarse: "If you specify W, one backup every week is copied to long-term storage. If you specify M, the first backup of each month is copied to the long-term storage. If you specify Y, one backup during the week specified by WeekOfYear is copied".
- No customer control of timing: "The timing of individual LTR backups is controlled by Microsoft. You can't manually create an LTR backup or control the timing of the backup creation. After you configure an LTR policy, it might take up to seven days before the first LTR backup shows up on the list of available backups."
- Policy changes are not retroactive: "Changes to the LTR policy apply only to future backups."
- Restore is subscription-bound: "The database can be restored to any existing server or managed instance **under the same subscription** as the original database."
- Hyperscale boundary: "Restoring databases between the Hyperscale service tier and the other service tiers of Azure SQL Database is not currently supported."
- MI ceiling / workaround: copy-only backups to your own storage account are the documented alternative to "Keep backups for longer than 10 years", "Keep daily copies of your databases for longer than 35 days", and "Store database backups on immutable storage."

**Why it matters:** C2 says "keep N years of closed records cheaply, **read-only**". LTR does not deliver read-only *access*. An LTR backup is not queryable; the only way to read it is to restore it as a new database, which costs a full database's compute and storage. LTR answers "can I recover the state of 2019?", not "can users read 2019 records".

**Decision impact:** data requirement "N years of closed records, readable" → constraint "LTR gives recoverability up to 10 years, not online read access; reading a year-old record means restoring a whole database" → architectural implication "if the requirement is *read* access to old records, LTR is the wrong mechanism — the rows must stay online in the database (paying hot storage) or be exported to a separate cheap store (Blob/Parquet/Fabric/lakehouse). If the requirement is only *retention for audit/recovery*, LTR fits and is genuinely cheap."

**Conditions:** Azure SQL Database and Managed Instance. Max 10 years.
**Confidence:** High.
**Sources:** S2.

---

#### SQ2-05 — Azure SQL has no documented "cheap cold/archive tier" for rows

**Classification:** Gap / negative evidence — CONTRADICTS the "cheaply" half of C2
**Origin:** MS (T1) — absence of a documented feature
**Status:** provisional pending the archive-pattern searches in SQ2-09/SQ2-10.

**Evidence so far** [S2][S3]: Azure SQL Database storage is priced as allocated data storage in the chosen service tier — General Purpose and Business Critical are "1 GB - 4 TB", Hyperscale "10 GB - 128 TB" with "you pay for storage based on actual allocation" [S3]. There is no per-row or per-partition "cool"/"archive" storage tier documented for Azure SQL Database data files, in contrast to Azure Blob Storage access tiers. LTR (S2) is backup-only.

**Why it matters:** "cheaply" in C2 assumes a cold tier that Azure SQL does not expose. Old rows in Azure SQL cost the same per GB as hot rows in the same database.

**Decision impact:** data requirement "N years closed records, cheap" → constraint "no row-level archive tier; all online rows billed at the tier's storage rate" → architectural implication "cheap long retention requires moving rows out of SQL (Blob/Parquet + external table, Fabric/Synapse, or a second cheap database), which is an ETL project, not a SQL setting."

**Confidence:** Medium-High (negative claim; strengthened by SQ2-09/10).
**Sources:** S2, S3.

---

#### SQ2-06 — Microsoft's own data-store model guide routes high-ingest telemetry AWAY from relational

**Classification:** Evidence — **CONTRADICTS C3**
**Origin:** MS (T1)

**Evidence** [S4] (Azure Architecture Center, *Understand Data Models*, ms.date 2025-08-21):
- Classification table, verbatim rows:
  - "| Relational (OLTP) | Consistent transactional operations | Azure SQL Database, Azure Database for PostgreSQL, or Azure Database for MySQL |"
  - "| Time series | High-ingest timestamped metrics and events | Azure Data Explorer or Eventhouse in Fabric |"
- Time-series model definition: "Time-series data stores manage a set of values organized by time. ... They're optimized to ingest and analyze large volumes of data in near real time. They're typically append-only databases."
- Its workloads: "IoT sensor metrics, application telemetry, monitoring, industrial data, and financial market data".
- Relational considerations, verbatim: "Horizontal scale generally requires sharding or partitioning, and normalization can increase join cost for read-heavy denormalized views."
- Relational workloads, verbatim: "Order management, inventory tracking, financial ledger recording, billing, and operational reporting." — telemetry is **not** in that list.
- Heuristics table, verbatim rows: "| Wide, sparse, write-heavy telemetry | Column family or time series |" and "| High-ingest timestamp metrics with window queries | Time series |".
- Re-evaluation signal, verbatim: "| Time-window queries slow on column-family store | Adopt purpose-built time-series database |".
- ADX positioning, verbatim: "Azure Data Explorer (Kusto) | High-ingest telemetry, time-series analytics | KQL, fast ad-hoc queries, time-window functions | Real-time analytics for application logs and metrics".
- The only relational escape hatch Microsoft names is PostgreSQL, not SQL: "Some transactional databases provide limited time-series capabilities as part of their broader feature set or through extensions. For example, Azure Database for PostgreSQL supports TimescaleDB. Select this option if you need to query time-series data alongside existing transactional data in the database."

**Why it matters:** Claim C3 ("Azure SQL STRONG for high-ingest, semi-structured, time-bounded data") is the opposite of Microsoft's published model→service mapping. Microsoft assigns that exact phrase-space ("High-ingest timestamped metrics and events") to Azure Data Explorer / Eventhouse. Azure SQL appears only under "Relational (OLTP) — Consistent transactional operations".

**Decision impact:** data requirement "capture events/telemetry/logs at high rate, query by time window, retain for a bounded period" → constraint "Microsoft reference guidance points to Azure Data Explorer or Fabric Eventhouse (KQL), not Azure SQL; SQL's log-rate ceiling caps sustained ingest (SQ2-07)" → architectural implication "if the engagement's data is genuinely telemetry-shaped, the store decision must not stop at SQL; SQL is defensible only when the volume is small and it must sit next to transactional data. C3 must be downgraded from STRONG to CONDITIONAL/WEAK."

**Conditions:** Applies to the "high-ingest" framing. Low-volume event rows inside a business app (audit trails, status history) are ordinary relational rows and are fine in SQL.
**Confidence:** High — the contradiction is explicit in a first-party decision guide.
**Sources:** S4.

---

#### SQ2-07 — Azure SQL scale envelope: the concrete numbers the file lacked (log rate is the real ceiling)

**Classification:** Evidence — bounds for both C3 and C4
**Origin:** MS (T1)

**Evidence** [S5] single-database vCore resource limits, ms.date 2026-03-09; [S3] Hyperscale overview, ms.date 2026-05-19:
- Storage ceilings [S3]: General Purpose "1 GB - 4 TB"; Business Critical "1 GB - 4 TB"; Hyperscale "10 GB - 128 TB". Also "Autoscaling storage with support for up to 128 TB of database or 100 TB elastic pool size."
- Hyperscale sizing behaviour [S3]: "Hyperscale databases aren't created with a defined max size. A Hyperscale database grows as needed - and you're billed only for the storage capacity allocated." "Storage is automatically allocated between 10 GB and 128 TB".
- Compute [S3]: General Purpose "2 to 128 vCores", Business Critical "2 to 128 vCores", Hyperscale "2 to 192 vCores" (160/192 preview).
- IOPS [S3]: GP "320 IOPS per vCore with 16,000 maximum IOPS"; BC "4,000 IOPS per vCore with 327,680 maximum IOPS"; Hyperscale "5,500 IOPS per vCore with 544,000 maximum local SSD IOPS."
- **Log rate is the sustained-write ceiling** [S5]: GP provisioned Gen5 at 24/32/40/80/128 vCores — "Max log rate (MiB/s) | 50 | 50 | 50 | 50 | 50". Business Critical Gen5 24→128 vCores — "Max log rate (MiB/s) | 96 | 96 | 96 | 96 | 96". Hyperscale Gen5 — "Max log rate (MiB/s) | 100 | 100 | 100 | 100 | 100 | 100 | 100". It does **not** increase with vCores past those points.
- Concurrency [S5]: "Max concurrent sessions | 30,000" at every SLO inspected (GP serverless 1 vCore through Hyperscale 128 vCore). Workers scale with vCores: GP provisioned 128 vCore "Max concurrent workers | 12,800"; BC 128 vCore "12,800"; Hyperscale provisioned 128 vCore "8000".
- Small-SLO reality [S5]: GP serverless 1 vCore — "Max data size (GB) | 512", "Max data IOPS ^3^ | 320", "Max log rate (MiB/s) | 4.5", "Max concurrent workers | 75", "Max concurrent external connections ^4^ | 7".
- IOPS at scale [S5]: GP 128 vCore "Max data IOPS ^2^ | 16,000"; BC 128 vCore "Max data IOPS ^2^ | 327,680".

**Why it matters:** These are the missing "large dataset / high transaction volume" numbers. Two consequences. (a) Sustained write throughput does not grow with vCores past a point — log rate flatlines at 50 MiB/s (GP), 96 (BC), 100 (Hyperscale). That is the physical cap on both telemetry ingest (C3) and nightly bulk load (C4). (b) 30,000 concurrent sessions is generous, but concurrent *workers* on a small SLO (75 at 1 vCore, 7 external connections) is small — and the Power Platform connector's 125-concurrent-calls-per-connection limit sits inside that envelope, so the connector, not SQL, is normally the binding constraint for interactive apps.

**Decision impact:** data requirement "large dataset / high transaction volume" → constraint "≤4 TB on GP/BC, ≤128 TB on Hyperscale; sustained write ≤50/96/100 MiB/s of log regardless of vCores; workers = f(vCores); sessions capped at 30,000" → architectural implication "size the SLO by log rate and worker count, not by vCores or storage; if required sustained ingest exceeds ~100 MiB/s of log, Azure SQL is the wrong store at any price; and Hyperscale is the only tier that answers 'dataset > 4 TB'."

**Conditions:** Single databases, vCore model, standard-series (Gen5) unless noted. Elastic pools, DTU model, and Managed Instance have separate tables.
**Confidence:** High.
**Sources:** S3, S5.

---

#### SQ2-08 — Row-level security works, but per-user enforcement needs an identity the shared Power Platform connection does not supply

**Classification:** Evidence + INF (Power Platform coupling)
**Origin:** MS (T1) for SQL mechanics; INF for the connector coupling

**Evidence** [S6] *Row-Level Security*, ms.date 2025-09-11:
- "Row-level security (RLS) enables you to use group membership or execution context to control access to rows in a database table."
- "The access restriction logic is located in the database tier rather than away from the data in another application tier. The database system applies the access restrictions every time that data access is attempted from any tier."
- "Filter predicates silently filter the rows available to read operations (SELECT, UPDATE, and DELETE)." / "Block predicates explicitly block write operations (AFTER INSERT, AFTER UPDATE, BEFORE UPDATE, BEFORE DELETE) that violate the predicate."
- **The shared-connection pattern, verbatim (Example C):** "This example shows how a middle-tier application can implement connection filtering, where application users (or tenants) share the same SQL Server user (the application). The application sets the current application user ID in SESSION_CONTEXT after connecting to the database, and then security policies transparently filter rows that shouldn't be visible to this ID, and also block the user from inserting rows for the wrong user ID. No other app changes are necessary."
- Responsibility is on the app: "In practice, the application is responsible for setting the current user ID in SESSION_CONTEXT() after opening a connection."
- Pooling caveat, verbatim: "Note: @read_only prevents the value from changing again until the connection is closed (returned to the connection pool)".
- Privilege caveat: "Security policies apply to all users, including dbo users in the database. Dbo users can alter or drop security policies however their changes to security policies can be audited."
- Performance/compat caveats: "Avoid using excessive table joins in predicate functions to maximize performance."; "indexed views can't be created on top of tables that have a security policy, because row lookups via the index would bypass the policy."; "RLS is incompatible with Filestream."; "Temporal tables are compatible with RLS. However, security predicates on the current table aren't automatically replicated to the history table."
- Leak channels: "DBCC SHOW_STATISTICS reports statistics on unfiltered data, and can leak information otherwise protected by a security policy."; "Change Data Capture (CDC) can leak entire rows that should be filtered to members of db_owner"; and the crafted-query example "SELECT 1/(SALARY-100000) FROM PAYROLL WHERE NAME='John Doe';".
- Platform gap: "Microsoft Fabric and Azure Synapse Analytics support filter predicates only. Block predicates aren't currently supported on Microsoft Fabric and Azure Synapse Analytics."

**Why it matters:** This is the hinge for SQL under Power Platform. Established fact: implicit/shared connections run as the maker's credentials, and only Microsoft Entra Integrated gives per-user identity. Microsoft's RLS examples split exactly along that line — Example A/D use `USER_NAME()` (needs a real per-user principal), Example C uses `SESSION_CONTEXT` (needs a middle tier that calls `sp_set_session_context` on every connection). A canvas app on the SQL connector has neither: the connector owns the connection, and there is no documented maker hook to set session context before each query.

**Decision impact:** data requirement "each user must see only their own rows" → constraint "SQL can enforce it, but the predicate needs a trustworthy identity: a real per-user database principal (Entra Integrated) or SESSION_CONTEXT set by a middle tier" → architectural implication "with the shared/implicit connection, `USER_NAME()`-based RLS collapses to one principal and enforces nothing; per-user row security therefore forces either Entra Integrated auth end-to-end, or a custom API / stored-procedure middle tier — both change the delivery model and the licensing conversation."

**Conditions:** SQL Server 2016+, Azure SQL DB, Azure SQL MI, Synapse, Fabric.
**Confidence:** High for SQL mechanics; Medium-High for the Power Platform coupling (inference from established connector behaviour, not a single quoted MS sentence).
**Sources:** S6.

---

#### SQ2-09 — Dataverse CMK vs Azure SQL CMK: same key vault, very different entry price and blast radius

**Classification:** Evidence — factual comparison for C1
**Origin:** MS (T1)

**Evidence** [S7] *Manage your customer-managed encryption key* (Power Platform), ms.date 2026-05-18:
- Licensing gate, verbatim: "Customer-managed key policy is only enforced on environments that are activated for managed environments. Managed environments are included as an entitlement in standalone Power Apps, Power Automate, Microsoft Copilot Studio, Power Pages, and Dynamics 365 licenses that give premium usage rights."
- Second gate, verbatim: "In addition, access to using customer-managed key for Microsoft Power Platform and Dynamics 365 requires users in the environments where the encryption key policy is enforced to have one of these subscriptions: Microsoft 365 or Office 365 A5/E5/G5; Microsoft 365 A5/E5/F5/G5 Compliance; Microsoft 365 F5 Security & Compliance; Microsoft 365 A5/E5/F5/G5 Information Protection and Governance; Microsoft 365 A5/E5/F5/G5 Insider Risk Management."
- Machinery: "the administrator creates a Power Platform enterprise policy, which references the encryption key and grants this enterprise policy access to read the key from your Azure Key Vault." Key type: "Key type: RSA, RSA key size: 2048 or 3072" (or RSA-HSM for Managed HSM, "This gives you FIPS 140-2 Level 3 support").
- **What CMK does not cover in Power Platform**, verbatim: "The connection settings for connectors continue to be encrypted with a Microsoft-managed key."; "Power Platform environment settings continue to be encrypted with a Microsoft-managed key."; "Power Apps display names, descriptions, and connection metadata continue to be encrypted with a Microsoft-managed key."; "Nuance Conversational IVR and maker welcome content are excluded from customer-managed key encryption."
- Downtime, verbatim: "The environment is disabled when it's added to the enterprise policy for data encryption. The duration of the system downtime is dependent on the size of the database." And: "The encryption can take up to four days to complete".
- Environment restrictions: "You can only add environments that are enabled as managed environments. Trial and Teams environment types can't be added to the enterprise policy."
- Restore/copy coupling: "The environment to overwrite (the restored to environment) is restricted to the same environment that the backup was taken from or to another environment that is encrypted with the same customer-managed key."
- Key-version rule: "the previous key version must not be disabled or deleted for, at least, 28 days to support database restoration."

**Compared with Azure SQL CMK [S1]:**

| | Azure SQL CMK | Dataverse CMK |
|---|---|---|
| Licence gate | None beyond the Azure SQL SKU + AKV | Managed Environment **and** E5-class compliance licence for users in the environment |
| Scope | Server / instance / (SQL DB) database | Whole Dataverse environment via enterprise policy |
| Key types | RSA (AKV/MHSM); AES symmetric in preview | RSA 2048/3072, RSA-HSM 2048/3072 |
| Switch-on cost | "no downtime nor re-encryption of the database files" | environment disabled during encryption, "up to four days to complete" |
| Coverage gaps | TDE covers data at rest in the DB; backups need historical keys | connector connection settings, environment settings, Power Apps display names/descriptions/connection metadata stay Microsoft-managed |

**Why it matters:** C1 is true for Azure SQL and cheaper to reach there than in Dataverse. If "customer-controlled encryption key" is a hard requirement, SQL clears it with an Azure subscription; Dataverse clears it only with Managed Environments plus an E5-class compliance SKU per user. That is a genuine, quotable store-choice differentiator — and one the unsourced file asserted without it.

**Decision impact:** data requirement "customer must hold/revoke the encryption key" → constraint "Dataverse path needs Managed Environments + E5-class licences and a multi-day encryption window; Azure SQL path needs only AKV with soft-delete/purge protection" → architectural implication "in a tenant without E5-class compliance licensing, CMK is a real argument for putting the regulated data in Azure SQL rather than Dataverse — while accepting SQL's premium-connector and per-user-identity costs."

**Conditions:** Commercial cloud; GCC High list is shorter.
**Confidence:** High.
**Sources:** S1, S7.

---

#### SQ2-10 — "SharePoint/M365 POOR for customer-managed keys" is WRONG: Customer Key has a dedicated SharePoint/OneDrive DEP

**Classification:** Evidence — **CONTRADICTS C5**
**Origin:** MS (T1)

**Evidence** [S8] *Overview of Customer Key* (Purview), ms.date 2025-02-03:
- Scope, verbatim: "Microsoft 365 also offers an added layer of encryption for your content through Customer Key. This content includes data from Microsoft Exchange, SharePoint, OneDrive, Teams, and Windows 365 Cloud PCs (Enterprise)".
- Purpose: "Customer Key helps you meet compliance or regulatory requirements by letting you control the root encryption keys at the application level."
- **A dedicated SharePoint DEP exists**, verbatim heading and text: "### DEP for SharePoint and OneDrive — This DEP encrypts content stored in SharePoint and OneDrive, including Teams files stored in SharePoint. Multi-geo tenants can create one DEP per geo; single-geo tenants can create one DEP."
- Granularity is the real limitation, verbatim: multi-workload DEPs "encrypt data across several Microsoft 365 workloads for all users in the tenant", and explicitly **"Not encrypted by multi-workload DEPs (protected by other methods): SharePoint and OneDrive data (use SharePoint DEP)"**; Exchange gets per-mailbox granularity ("You can have up to 50 active mailbox DEPs per tenant"), SharePoint does not — it is one policy per geo.
- Revocation path exists: "Revoking access to your keys triggers deletion of the availability key, resulting in cryptographic deletion of your data."
- Hybrid gap: "Customer Key encrypts only data at rest in the cloud. It doesn't protect on-premises mailboxes or files."

**Evidence** [S9] *Set up Customer Key*, ms.date 2025-09-08:
- Cost/complexity gates, verbatim: "Azure subscriptions: Two paid Azure subscriptions (Free, Trial, Sponsorship, MSDN, or Legacy Support aren't eligible)"; "Customer Key requires two keys for each DEP. To support this requirement, you must create two separate Azure subscriptions."
- Vault count, verbatim: "If you're using Customer Key for Multiple Workloads, Exchange, and SharePoint scenarios, you need three pairs of key vaults, for a total of six."
- Vault requirements, verbatim: "you must enable both soft delete and purge protection during the initial vault creation process. Customer Key requires all vaults to have both features enabled with a retention period of 90 days."
- SharePoint onboarding is a separate path, verbatim: the onboarding service "isn't currently available for the following scenarios: ... SharePoint and OneDrive: See Onboard to Customer Key for SharePoint and OneDrive."
- Granularity restated: "A SharePoint policy covers all data in an organization's geographic location (or geo), while a multi-workload policy covers supported workloads across all users in the organization."
- Ops constraint: "Don't set expiration dates on encryption keys used with Customer Key. The Customer Key Onboarding Service only accepts keys without an expiration date."
- Licensing: pointer only — "For licensing requirements, see Microsoft Purview Customer Key Licensing" (E5-class; see Unknowns U3).

**Why it matters:** Claim C5 as written ("SharePoint/M365 POOR for customer-managed keys") is factually wrong. SharePoint Online **is** covered by Customer Key, via a dedicated DEP. The accurate statement is about **granularity and scope**, not absence: a SharePoint Customer Key DEP is one policy per tenant (or per geo), tenant-wide, applied at the M365 service layer — you cannot scope a customer key to one site collection, one library or one app's data, whereas Azure SQL CMK can be scoped to a server, an instance or (SQL DB) a single database. Plus: tenant-wide setup cost (two paid Azure subscriptions, six key vaults for the full set), a separate SharePoint onboarding path, and an E5-class licence.

**Decision impact:** data requirement "customer-controlled key over the data this app stores" → constraint "SharePoint gives you a tenant-or-geo-wide DEP and no per-workspace scoping; Azure SQL gives you server/instance/database scoping" → architectural implication "'SharePoint POOR for CMK' must be rewritten as 'SharePoint supports Customer Key at tenant/geo granularity only, requiring E5-class licensing, two paid Azure subscriptions and a separate onboarding path — so it fails a *scoped* key requirement, not a key requirement as such.' Any store-choice matrix carrying the old wording will mis-score SharePoint."

**Conditions:** Commercial cloud; GCC-H/DoD/21Vianet need a support request. On-premises content is out of scope.
**Confidence:** High.
**Sources:** S8, S9.

---

#### SQ2-11 — Azure SQL Managed Instance with the Power Platform SQL connector: SQL Authentication is not supported, and VNet mode excludes the gateway

**Classification:** Evidence — connector support envelope
**Origin:** MS (T1)

**Evidence** [S10] SQL Server connector reference, ms.date 2024-03-01 (page updated 2026-07-11):
- **The MI statement, verbatim:** "SQL Authentication is supported only for servers that follow the format &lt;servername&gt;.database.windows.net. Connections to servers containing additional subdomains before .database.windows.net (for example, those used by Managed Instances) are not supported."
- Entra path exists but excludes guests, verbatim: "Due to current authentication pipeline limitations, Microsoft Entra ID guest users aren't supported for Microsoft Entra ID connections to SQL Server. To resolve this problem, use SQL Server authentication or Windows authentication instead."
- Managed identity is Logic Apps only, verbatim: "Currently, only Azure Logic Apps supports managed identity authentication for the SQL Server connector."
- **VNet-linked environments, verbatim:** the supported action list is closed — "Any action outside of this list will return a '403 Unauthorized' error"; "On-premise data gateway is not supported"; "When using Microsoft Entra ID Integrated authentication, please type in the database name manually as a Custom Value"; "When specifying the name of the SQL Server for VNet implementations, do not include a port number". Supported actions are only Delete row (V2), Execute a SQL query (V2), Get row (V2), Get rows (V2), Get tables (V2), Insert row (V2), Update row (V2), Execute stored procedure (V2).
- Gateway limits (confirming established facts): "The request size limit is 2 MB through on-premises SQL Server."; "The response size limit is 8 MB through on-premises SQL Server."; stored procedures via gateway — "Output values for OUTPUT parameters aren't returned."; "Return value isn't available."; "Only the first result set is returned."
- "Execute a SQL query limited support | Execute a SQL query (V2) | Not supported for on-premises SQL Server or connections with gateway"
- Timeout (confirming): "If the execution time exceeds 110 seconds for a SQL query or stored procedure, actions will time out."
- Payload advice: "It is not recommended to store large amounts of data (more than 30 megabytes) in the target table fields (e.g. xml or text data types). It can lead to a significamt performance degradation of actions and triggers, causing 504 timeout errors." [sic — verbatim]
- Other bindings: "Insert and update to a table won't work if you defined a SQL server-side trigger on the table."; "Power Platform and Logic Apps navigator views are limited to a list size of 10,000 tables."; "Tabular Data Stream (TDS) protocol 8.0 is currently not supported by the SQL connector."
- Throttling table (confirming established facts): Power Apps shared environment "All | API calls per user | 300 | 30" and "All | Concurrent calls per connection | 125"; Logic Apps & Power Automate CRUD "API calls per connection | 100 | 10", "Concurrent calls per connection | 125"; Native "500 | 10" and "Concurrent calls per connection | 200".

**Why it matters:** MI is often proposed as the "enterprise SQL" answer in Power Platform engagements. The connector page says the *simple* auth path (SQL Authentication) is unavailable for MI hostnames, which forces Entra-based auth — and Entra connections exclude guest users, and managed identity is Logic Apps-only. Separately, a VNet-linked environment (the usual answer for private MI) shrinks the connector to eight actions and drops the on-premises gateway entirely.

**Decision impact:** data requirement "store must be Azure SQL Managed Instance (or SQL on VM behind a private network)" → constraint "no SQL Authentication for MI hostnames; Entra-based auth only, no guest users; if the environment is VNet-linked, only 8 SQL actions work and the gateway is unavailable" → architectural implication "MI + Power Platform is a narrower design surface than Azure SQL Database + Power Platform. Choosing MI for network or SQL-Server-compatibility reasons costs connector surface area and forces the Entra identity model — plan the identity design at store-choice time, not at build time."

**Conditions:** Managed connector for Power Apps/Power Automate/Copilot Studio (Premium class); Logic Apps built-in connector has a different envelope. SQL on VM behind a gateway falls under the on-prem limits, not the MI hostname rule.
**Confidence:** High for the quoted statements; Medium on generalising the hostname rule to every SQL-on-VM topology (the rule is about hostname shape, not product).
**Sources:** S10.

---

#### SQ2-12 — Bulk load into SQL: fast only when minimal-logging preconditions are met, and never through the connector

**Classification:** Evidence — QUALIFIES C4
**Origin:** MS (T1)

**Evidence** [S11] *Prerequisites for Minimal Logging in Bulk Import*, ms.date 2025-09-07:
- The cost of getting it wrong, verbatim: "For a database under the full recovery model, all row-insert operations that are performed by bulk import are fully logged in the transaction log. Large data imports can cause the transaction log to fill rapidly if the full recovery model is used."
- Preconditions, verbatim: "Minimal logging requires that the target table meets the following conditions: The table isn't being replicated. Table locking is specified (using TABLOCK). The table isn't a memory-optimized table."
- The empty-table rule, verbatim: "If the table has a clustered index and is empty, both data and index pages are minimally logged. In contrast, if a table has a B-tree based clustered index and is non-empty, data pages and index pages are both fully logged regardless of the recovery model."
- Multi-batch caveat, verbatim: "If you start with an empty rowstore table and bulk import the data in batches, both index and data pages are minimally logged for the first batch, but from the second batch onward, only data pages are bulk logged."
- Replication kills it: "When transactional replication is enabled, BULK INSERT operations are fully logged even under the bulk logged recovery model."
- Compression interaction [S12]: "When data is imported, if the target table has been enabled for compression, the Database Engine converts the data into compressed row format. This can cause increased CPU usage compared to when data is imported into an uncompressed table."

**Why it matters:** C4 ("Azure SQL STRONG for nightly bulk load of large volumes") is *conditionally* true and the conditions are non-trivial. Two independent facts undercut a flat STRONG rating:
1. **Azure SQL Database is always in the full recovery model** — the bulk-logged/simple recovery models that this page's minimal logging depends on are a SQL Server / on-prem concept. So the classic minimal-logging escape is unavailable in Azure SQL Database, and the sustained ceiling is the log rate from SQ2-07 (50/96/100 MiB/s). Flagged as U1 in Unknowns — Microsoft does not state this on this page and it needs its own citation.
2. **Even where minimal logging applies**, it needs TABLOCK, no replication, no memory-optimized table, and ideally an empty table with the clustered index — i.e. a staging-table + partition-switch design, not "insert into the live table overnight".
- And the Power Platform angle: **bulk load never goes through the SQL connector.** The connector is row-at-a-time CRUD under 100 calls/10 s and a 110-second action timeout [S10]. Nightly bulk load is an ADF / bcp / BULK INSERT job outside Power Platform entirely.

**Decision impact:** data requirement "nightly bulk load of large volumes" → constraint "throughput is capped by the tier's log rate; minimal logging needs TABLOCK + empty target + no replication; the Power Platform connector cannot do bulk load at all" → architectural implication "the store choice implicitly buys a second toolchain (ADF pipeline, bcp job, or Logic App with staged copy) and a staging-plus-switch table design. Rate C4 as CONDITIONAL: strong *if* someone owns an ETL tool and designs for it; weak if the plan was 'a flow will load it'."

**Conditions:** The minimal-logging page is scoped "Applies to: SQL Server" only — see U1.
**Confidence:** High for the quoted preconditions; Medium for the Azure SQL Database recovery-model claim (unsourced here — U1).
**Sources:** S10, S11, S12.

---

#### SQ2-13 — Microsoft's documented bulk-load throughput guidance is a tuning method, not a number

**Classification:** Evidence — bounds C4
**Origin:** MS (T1)

**Evidence** [S13] *Copy activity performance and scalability guide* (ADF/Synapse), ms.date 2025-07-25:
- No absolute throughput is promised; it is bandwidth-derived, verbatim: "you can estimate the overall throughput by measuring the minimum throughput available with the following resources: Source data store; Destination data store; Network bandwidth in between the source and destination data stores."
- Explicit caveat on the published table, verbatim: "The duration provided below are meant to represent achievable performance in an end-to-end data integration solution by using one or more performance optimization techniques ... You should use the numbers obtained in your performance tuning tests for production deployment planning, capacity planning, and billing projection."
- Concrete published durations (the only numbers Microsoft states here), verbatim from the table: 100 GB at 1 Gbps = "0.2 hrs"; 1 TB at 1 Gbps = "2.3 hrs"; 1 TB at 100 Mbps = "23.3 hrs"; 10 TB at 1 Gbps = "0.9 days".
- Parallelism ceilings, verbatim: "When using Azure integration runtime (IR), you can specify up to 256 data integration units (DIUs) for each copy activity, in a serverless manner."; self-hosted IR can "Scale out to multiple machines (up to 4 nodes)".
- Method, verbatim: "A good size takes at least 10 minutes for copy activity to complete."; "Once single copy activity runs can't achieve better throughput, consider whether to maximize aggregate throughput by running multiple copies concurrently."

**Why it matters:** There is no Microsoft-published "Azure SQL ingests N rows/second". Anyone asserting a bulk-load number is inventing it. What Microsoft gives is (a) a bandwidth-derived duration table with an explicit "measure it yourself" disclaimer, and (b) the parallelism knobs. The binding constraint on the *sink* side remains the log rate from SQ2-07.

**Decision impact:** data requirement "nightly window of N hours to load X GB" → constraint "no vendor throughput guarantee; plan against min(source, sink log rate, network) and prove it with a ≥10-minute pilot copy" → architectural implication "make a measured pilot load a gate before committing to SQL as the store when the nightly volume is material; put the measured number, not a guess, in the estimate."

**Conditions:** ADF/Synapse copy activity. bcp/BULK INSERT have no published throughput numbers either.
**Confidence:** High.
**Sources:** S13.

---

#### SQ2-14 — Cheap long retention in SQL means partitioning + archival compression + moving data out — Microsoft documents the patterns, not a tier

**Classification:** Evidence — confirms SQ2-05, **QUALIFIES C2**
**Origin:** MS (T1)

**Evidence** [S14] *Data partitioning guidance* (Azure Architecture Center, ms.date 2022-07-25):
- The archive rationale, verbatim: "Partitioning can improve scalability, reduce contention, and optimize performance. It can also provide a mechanism for dividing data by usage pattern. For example, **you can archive older data in cheaper data storage**."
- The cheap storage is a *different store*, verbatim: "Partitioning allows each partition to be deployed on a different type of data store, based on cost and the built-in features that data store offers. For example, large binary data can be stored in blob storage, while more structured data can be held in a document database."
- Retention as an operational chore, verbatim: "How to archive and delete the data on a regular basis. To prevent the excessive growth of partitions, you need to archive and delete data regularly (such as monthly). It might be necessary to transform the data to match a different archive schema."
- Backup-frequency differentiation, verbatim: "partitions that hold transaction data might need to be backed up more frequently than partitions that hold logging or trace information."
- Scoping note, verbatim: "In this article, the term partitioning means the process of physically dividing data into separate data stores. It isn't the same as SQL Server table partitioning."

**Evidence** [S12] *Data compression* (SQL, ms.date 2023-10-27):
- The in-SQL cold-data lever, verbatim: "Use columnstore archival compression to further reduce the data size for situations when you can afford extra time and CPU resources to store and retrieve the data."
- Its cost, verbatim: "When you compress columnstore indexes with archival compression, this causes the index to perform slower than columnstore indexes that don't have the archival compression. Use archival compression only when you can afford to use extra time and CPU resources to compress and retrieve the data."
- Its intended use, verbatim: "The benefit of archival compression is reduced storage, which is useful for data that isn't accessed frequently. For example, if you have a partition for each month of data, and most of your activity is for the most recent months, you could archive older months to reduce the storage requirements."
- Per-partition control, verbatim: "For partitioned columnstore tables and columnstore indexes, you can configure the archival compression option for each partition, and the various partitions don't have to have the same archival compression setting."
- Row/page compression tradeoff, verbatim: "data compression can help improve performance of I/O intensive workloads because the data is stored in fewer pages ... However, extra CPU resources are required on the database server to compress and decompress the data".

**Why it matters:** This closes SQ2-05. Microsoft's answer to "keep N years cheaply" inside SQL is: partition by time, apply `COLUMNSTORE_ARCHIVE` to old partitions (trading query speed and CPU for size), and — for genuinely cheap — move partitions to a *different, cheaper data store*. There is no Azure SQL storage tier that costs less per GB for old rows. Note also that the historic in-product answer, Stretch Database, is deprecated (see U2).

**Decision impact:** data requirement "keep N years of closed records cheaply, read-only" → constraint "no cold storage tier in Azure SQL; cheapness comes from columnstore archival compression (slower reads, more CPU) or from exporting the partitions to Blob/Data Lake/Fabric" → architectural implication "C2 becomes CONDITIONAL: Azure SQL keeps N years *readable* fine (it is just rows), and LTR keeps N years *recoverable* up to 10 years — but 'cheaply' requires an explicit archive design (time partitioning + archival compression, or an export pipeline) that must be scoped and estimated, not assumed. If cheap-and-read-only is the dominant requirement and the records are truly closed, Blob/Parquet or a lakehouse beats SQL on cost."

**Conditions:** Columnstore archival compression requires columnstore indexes; note Hyperscale's in-memory OLTP limitation and the general "row-size 8,060 bytes" compression rules from S12.
**Confidence:** High.
**Sources:** S2, S3, S12, S14.

---

#### SQ2-15 — Microsoft's own Power Platform reference architecture: default to Dataverse; choose SQL when the data can't move

**Classification:** Evidence — answers request item 9
**Origin:** MS (T1)

**Evidence** [S15] *Use the SQL Server with canvas apps* (Power Platform architecture reference), ms.date 2025-07-15:
- **The store-choice statement, verbatim:** "If you're building a new app and storage, consider using Dataverse. Its features are designed to make building enterprise-grade apps easier." / "If you have data in SQL Server that can't be moved, or your organization requires SQL Server, consider using Power Apps over SQL Server." / "If the data can't be moved, use Power Apps over SQL Server. Existing apps still depend on that data, so you need to move those apps to the cloud to modernize them."
- Recommended network topology, verbatim: "While many previous implementations of Power Apps with SQL Server used a gateway, this example architecture highlights the virtual private network (VNET) architecture with SQL Server. A SQL Server instance can be Azure SQL or an on-premises SQL database exposed to the cloud through Azure Arc."
- Recommended auth, verbatim: "While there are many SQL authentication types available, Microsoft Entra ID and shareable SPN (service principal name) are two of the better choices." And the shared-identity warning, verbatim: "Shareable SPN is an admin-enabled access method and should be granted carefully, as **all users have the same database access rights**."
- Secure implicit connections, verbatim: "With secure implicit connections, the connector stays inside the Power Apps cloud service and doesn't reside on the client. ... The proxy connector has a policy that restricts query types to queries in the app."
- Delegation, verbatim: "Power Fx expressions are translated into OData expressions, which are then converted into SQL expressions. However, Power Fx and OData don't fully represent all the capabilities of an SQL expression." and "Use Power Fx for basic, straightforward queries, and use stored procedures for more complex SQL expressions."
- **No transactions in Power Fx**, verbatim: "Each Power Fx operation is independent and isn't handled as an atomic transaction. For example, if an application creates a sales order detail row but doesn't create a sales order header record, the sales order detail row remains. Don't leave these required procedural steps in Power Fx. Use SQL Server stored procedures with transaction support."
- Async guidance, verbatim: "Delegate complex tasks to views and stored procedures. Then, use those stored procedures directly for synchronous actions. Use Power Automate for any asynchronous actions, including calls to long-running stored procedures."

**Why it matters:** This is Microsoft's explicit Dataverse-vs-SQL decision rule for Power Platform, and it inverts the usual "SQL is the serious choice" instinct: **Dataverse is the default for new storage; SQL is the answer when the data already exists there or policy demands it.** It also confirms the SQ2-08 identity problem in Microsoft's own words ("all users have the same database access rights" under shareable SPN) and adds a transactional-integrity constraint that the store-choice matrix should carry.

**Decision impact:** data requirement "new app, new data, Power Platform delivery" → constraint "Microsoft's reference guidance defaults to Dataverse; SQL is justified by immovable data, org policy, or a capability Dataverse lacks (e.g. CMK without E5 — SQ2-09; >4 TB / Hyperscale scale — SQ2-07)" → architectural implication "a store-choice document that rates Azure SQL STRONG across the board without naming the immovable-data / policy trigger is arguing against Microsoft's own reference architecture. Each SQL recommendation should carry its trigger, plus the VNet-or-gateway decision, the Entra-vs-SPN identity decision, and a stored-procedure layer for anything transactional."

**Conditions:** Canvas apps specifically; model-driven apps are Dataverse-only.
**Confidence:** High.
**Sources:** S15.

---

#### SQ2-16 — Verdicts on the five unsourced claims

| # | Claim as written in the evidence file | Verdict | Basis |
|---|---|---|---|
| C1 | Azure SQL **STRONG** for "customer-controlled encryption key" | **SUPPORTED, with conditions** | SQ2-01, SQ2-02, SQ2-09. TDE with CMK is real, scopeable to server/instance/database, and cheaper to reach than Dataverse CMK (no E5/Managed Environments gate). Conditions: AKV soft-delete + purge protection, key becomes a tier-0 availability dependency with a 30-minute recovery cliff, all historical key versions must be retained for restore. |
| C2 | Azure SQL **STRONG** for "keep N years of closed records cheaply, read-only" | **CONTRADICTED as written; CONDITIONAL when restated** | SQ2-04, SQ2-05, SQ2-14. LTR is *backup* retention (max 10 years, restore-as-new-database only) — it is not readable storage. There is no cheap/cold storage tier for Azure SQL rows: old rows cost the same per GB as new ones. Cheapness requires time partitioning + `COLUMNSTORE_ARCHIVE` (slower, more CPU) or export to a different, cheaper store. |
| C3 | Azure SQL **STRONG** for "high-ingest, semi-structured, time-bounded data (events/telemetry/logs)" | **CONTRADICTED** | SQ2-06, SQ2-07. Microsoft's own data-store model guide maps "High-ingest timestamped metrics and events" to **Azure Data Explorer / Eventhouse in Fabric**, and lists Azure SQL only under "Relational (OLTP) — Consistent transactional operations". Sustained write is capped by log rate (50/96/100 MiB/s) that does not scale with vCores. Downgrade to WEAK/CONDITIONAL. |
| C4 | Azure SQL **STRONG** for "nightly bulk load of large volumes" | **CONDITIONAL, not STRONG** | SQ2-12, SQ2-13, SQ2-07. Works, but: capped by log rate; minimal logging needs TABLOCK + empty target + no replication (and is a SQL Server recovery-model feature — see U1); Microsoft publishes no throughput guarantee, only a "measure it yourself" method; and the Power Platform SQL connector cannot bulk load at all (100 CRUD calls/10 s, 110-second timeout) — a separate ETL toolchain is implied. |
| C5 | SharePoint/M365 **POOR** for customer-managed keys | **WRONG** | SQ2-10. Customer Key explicitly covers "Microsoft Exchange, SharePoint, OneDrive, Teams", with a dedicated "DEP for SharePoint and OneDrive". The true limitation is *granularity and setup cost*: one DEP per tenant (or per geo), E5-class licensing, two paid Azure subscriptions, six key vaults for the full set, and a separate onboarding path. Restate as "tenant/geo-granularity only — fails a *scoped* key requirement, not a key requirement." |

**Net effect on the store-choice matrix:** of the five unsourced assertions, **one is right (C1), one is wrong (C5), one is contradicted by Microsoft's own guidance (C3), and two are conditional-not-strong (C2, C4)**. Any matrix built on these five is mis-scoring SQL upward in three cells and mis-scoring SharePoint downward in one.

---

---

### 4.10 Business volume → platform request budget, read/write patterns, concurrency, consistency (new in v2 — closes review F-05, F-09, F-17)

The following 21 findings (`SC-01`..`SC-21`) close three review gaps: (a) transaction volume was previously handled only as raw API-limit numbers, with no translation from business volume to platform budget — `SC-21` supplies the translation *structure*, with every multiplier explicitly marked as an engagement-measured input, never a published figure (per the brief's instruction not to invent thresholds); (b) read/write workload shape and concurrency were thin — `SC-11`..`SC-13` supply Microsoft's PE:08 doctrine, and `SC-16`/`SC-17` supply the explicit negative finding that no concurrent-user ceiling exists anywhere, closed by a testing method instead; (c) the standard-table consistency model was implicit — `SC-06` makes it explicit, with the two documented staleness exceptions (Power Pages 15-minute cache, `CountRows` cached value) in `SC-12`/`SC-14`. All 16 sources are Tier 1 Microsoft Learn.

#### SC-01 — Dataverse counts internal system requests, not just the user's click

**Classification**: Counting rule (write amplification) — hard, documented.
**Origin**: MS (T1).

**Evidence** — [S1] *Requests limits and allocations*, ms.date 2026-08-14:

> "**Dataverse**: All create, read, update, and delete (CRUD), assign, and share operations including user-driven and internal system requests required to complete CRUD transactions, and special operations like share or assign. These operations can be from any client or application (including Dynamics 365) and use any endpoint (SOAP or REST). These operations include plug-ins, classic workflows, and custom controls that perform the earlier mentioned operations."

> "Dataverse excludes a small set of internal system operations from limits, such as login, logout, and system metadata operations."

FAQ, same page [S1]:

> "Yes, if these requests make CRUD, assign, or share-type requests, they count. For classic workflows, this logic includes actions such as checking conditions, starting child workflows, or stopping workflows. However, requests generated internally from the platform don't count, such as `sdkmessagerequest`, `solutioncomponentdefinition`, and `ribbonclientmetadatareporting`."

**Why it matters**: the request budget is *not* the count of business transactions. One business save can fan out into platform-internal writes plus every plug-in and classic-workflow CRUD it triggers. The amplification factor is a property of the *customization*, not of the business volume.

**Decision impact**:
- *Data requirement*: "N business transactions/day, each touching a parent + child rows + attachments, with audit."
- *Constraint*: each transaction consumes an unknown-until-measured multiple of N requests, because internal system requests and all custom logic CRUD count.
- *Architectural implication*: the amplification multiplier must be **measured in the target environment** (Application Insights for Dataverse / PPAC reports), never assumed. Design choices that add sync plug-ins, classic workflows or per-row flows are *budget* decisions, not only latency decisions.

**Conditions**: applies to all Dataverse traffic regardless of client or endpoint.
**Confidence**: High (verbatim, current page).
**Sources**: S1.

---

#### SC-02 — Retries and pagination count as consumption (Power Automate)

**Classification**: Counting rule — hard, documented.
**Origin**: MS (T1).

**Evidence** [S1]:

> "**Power Automate**: All API requests to connectors, process advisor analysis, HTTP actions, and built-in actions from initializing variables to a simple compose action. Both successful and failed actions count toward these limits. Retries and requests from pagination also count as action executions."

> "**Power Apps**: All API requests to connectors and Microsoft Dataverse."

> "**Microsoft Copilot Studio**: API requests (or calls) to Power Automate flows."

And on double counting [S1]:

> "Requests from Power Automate to Dataverse aren't double-counted. A flow that calls one action only counts as one request against your limit, not two."

**Why it matters**: the naive "one flow = one request" model is wrong by an order that depends on flow shape. Every `Initialize variable` and `Compose` is chargeable. Failures and their retries are chargeable — so an unstable integration costs *more* budget precisely when it is working worst. Paging a large result set costs one action per page.

**Decision impact**:
- *Data requirement*: "the flow reads 3,000 rows/day and writes them elsewhere."
- *Constraint*: cost = (actions per run × runs) + retries + pages, where pages ≈ rows / page size; not rows.
- *Architectural implication*: prefer few coarse actions over many fine ones; push filtering server-side so fewer pages are fetched; treat retry policy as a budget knob. A flow with a large `Apply to each` over rows is the dominant budget line item in most designs.

**Conditions**: Power Automate consumption; the non-double-counting statement is specific to flow→Dataverse.
**Confidence**: High.
**Sources**: S1.

---

#### SC-03 — Consumption is measurable, but the reporting is still preview and Dataverse/Power Apps are NOT in it

**Classification**: Observability gap — decision-relevant.
**Origin**: MS (T1).

**Evidence** [S1] (section "View detailed Power Platform request usage information in the Power Platform admin center (preview)"):

> "These reports are in preview and currently limited to Power Automate API requests. API requests from Dataverse, Microsoft Copilot Studio, and Power Apps aren't included at this time."

> "Reporting for Power Platform request usage in preview is available in the Power Platform admin center. These reports are currently limited to Power Automate API requests."

Path: Power Platform admin center → **Licensing** → **Capacity add-ons** → **Summary** → *Add-ons* → **Download reports** → **Microsoft Power Platform requests**, scoped to *Licensed User*, *Non-licensed User*, or *Per Flow Licensed Flows*, downloaded as an Excel CSV. Licensed-user report fields include `Entitled quantity`, `Total consumed quantity`, `Power Automate Requests`.

Known preview defects [S1]:

> "The entitlements for licensed users are showing up in the reporting per user per day per environment. The limits should apply at the per user per day level."

> "The **Licensed user** report doesn't show correct entitlements for users licensed via the Power Apps per app license or Power Apps per app pay-as-you-go meter. Entitlements for such users is shown as 0, when in fact, they should be shown as 6000".

**Why it matters**: you cannot close the loop on a Dataverse request budget with the first-party licensing report today. Dataverse amplification must be observed through **Application Insights for Dataverse** instead — [S2] PE:08 states: "The [Application Insights for Dataverse](...) data stream currently provides performance data related to Dataverse API incoming calls, Dataverse plug-in execution calls, and Dataverse SDK calls."

**Decision impact**:
- *Data requirement*: "we need to know if we will breach entitlements."
- *Constraint*: the licensing report answers this only for Power Automate; Dataverse/Power Apps consumption is invisible in it.
- *Architectural implication*: make Application Insights export a **day-one, non-optional** design item for any volume-sensitive build; do not promise budget verification from PPAC licensing reports alone.

**Conditions**: preview status as of ms.date 2026-08-14; expected to change.
**Confidence**: High.
**Sources**: S1, S2.

---

#### SC-04 — Enforcement is deliberately deferred; today's headroom is not tomorrow's

**Classification**: Timing/risk — documented.
**Origin**: MS (T1).

**Evidence** [S1]:

> "Any possible high usage enforcement won't happen until six months after Power Platform Request usage reporting is generally available in the Power Platform admin center."

> "Microsoft reserves the right to enforce limits for overages. If you experience high usage enforcement, you might see throttling."

> "Public preview reporting for Power Platform Requests rolled out in June 2022. Following a public preview period, the reports move to general availability. There's no current ETA for when GA happens. Any potential high usage enforcement won't start until at least six months after reports are generally available. However, Power Automate continues to throttle at transition limits until enforcement."

Transition period, Power Automate [S1]:

> "All organizations are in a transition period. That means that enforcement isn't strict and PPR limits are higher."

> "The transition period doesn't mean there are no daily limits. It means the currently enforced limits are more generous than the official limits to prevent potential unintended impact on your apps or flows."

> "These transition period limits are applied at the cloud flow level during the transition period. Additionally, a separate per user level limit of 1,000,000 cloud flow actions is applied during the transition period to ensure users don't exceed 1M actions across all their flow runs in a day."

> "Build your cloud flows based on official limits."

> "During the transition period, manual cloud flows don't use the flow owners/flow invokers limits. Every manual cloud flow has a performance profile of Medium (100,000 requests/flow/24 hours). After the transition period, manual cloud flows will use the request limits of invoking user."

> "Since the limits are more generous during the transition period, stacking of user licenses isn't supported."

Capacity relief [S1]:

> "Each capacity add-on raises the request limit by another 50,000 per 24 hours. Multiple capacity add-ons can be assigned to increase limits."
> "Currently, you can't assign capacity add-ons to users (including application, administrative, and noninteractive users)."

**Why it matters**: a solution that "works today" may be running on transition-period generosity and on the *cloud flow* rather than the *user* as the unit of accounting. When the transition ends, the unit of accounting moves to the user for Premium licences, and stacking stops rescuing multi-licence users. The published mitigation (capacity add-ons) is *not currently assignable* to the service accounts most integrations run under.

**Decision impact**:
- *Data requirement*: "volume grows 3x over 18 months."
- *Constraint*: design must fit the **official** limits, not the observed transition limits; add-on relief for application users is not currently available.
- *Architectural implication*: for high-volume integration, prefer a Process-licensed flow (250k/licence, stackable) or push the work to a client application against Dataverse rather than parking it on a user's 40k.

**Conditions**: transition period status; ends after PPAC reports reach GA + 6 months.
**Confidence**: High.
**Sources**: S1.

---

#### SC-05 — Whose budget a process spends: on-demand vs background

**Classification**: Counting rule (attribution) — documented.
**Origin**: MS (T1).

**Evidence** [S1]:

> "It depends on whether the process runs on demand or in the background. Instant flows, which run on demand, use the limits of the account that starts the process. Workflows or automated and scheduled flows that run in the background always use the limits of the owner of the process, regardless of why the process started or which accounts are used for connections within the process."

> "The 24 hours is a sliding window, meaning that anytime a cloud flow runs, the system looks at the requests in the past 24 hours to determine if the user is at their limit."

> "To prevent a usage-heavy flow or user from impacting other users, the system tracks this capacity based on consumption at an individual user or flow level and it can't be pooled at any other level like environment or tenant levels."

> "A Power Automate cloud flow owned by a service principal doesn't use the non-licensed user pool if it has a Process or Per-flow license, belongs to a [flow group](...) that has a Process license assigned, or has a designated licensed user. When you designate a licensed user, the flow uses that user's action limits."

> "The five-minute limit is 100,000 requests and it's independent of a user's license."

> "Desktop flow executions don't consume Power Platform requests."

> "Non-Microsoft data integration tools are subject to the exact same limits as scheduled, instant, or automated flows."

**Why it matters**: entitlements do not pool. The budget question is never "does the tenant have enough?" — it is "does *this identity* have enough in the last 24 hours?". A single background flow owned by one architect can exhaust that person's 40k and stall the whole integration, while the tenant is barely used.

**Decision impact**:
- *Data requirement*: "3,000 orders/day processed by a nightly integration."
- *Constraint*: all of it lands on the flow owner's single 24-hour sliding entitlement unless the flow carries a Process/per-flow licence or a designated licensed user.
- *Architectural implication*: ownership of automation is an **architectural** decision. Name the owning identity and its licence in the design; do not let it default to whoever built it. Also: "swap Power Automate for an external ETL tool to dodge limits" is explicitly refuted.

**Conditions**: 5-minute 100,000 cap is licence-independent and applies on top.
**Confidence**: High.
**Sources**: S1.

---

#### SC-06 — Standard tables = strong consistency; elastic = session consistency you must carry

**Classification**: Consistency model — documented, explicit.
**Origin**: MS (T1).

**Evidence** — [S3] *Elastic Tables for Developers*, ms.date 2026-08-04:

> "Use elastic tables in these situations: ... You must handle a high volume of read and write requests."

> "Use standard tables in these situations: Your application requires strong data consistency. Your application requires relational modeling and needs transactional capability across tables or during plug-in execution. Your application requires complex joins."

> "Elastic table supports strong consistency during a *logical session*. A logical session is a connection between a client and Dataverse."

> "Session tokens ensure that all the read operations that are performed during the same logical session context return the most recent write that was made during that logical session. In other words, session tokens ensure that reads always honor the *read-your-writes* and *write-follows-reads* guarantees during a logical session. If a different logical session performs a write operation, other logical sessions might not immediately detect those changes."

> "If you retrieve a record without a session token, the recently applied changes might not be applied. Instead, they might be returned in subsequent requests."

> "Elastic tables don't support multi-record transactions."
> "Elastic tables also don't support grouping requests in a single database transaction ... Currently, these operations succeed but aren't atomic."
> "Elastic tables don't support *deep insert* as standard tables do."

Storage substrate, from [S4] *Optimize Performance for Bulk Operations*, ms.date 2026-03-26:

> "A **standard** table stores data using Azure SQL. Standard tables provide transaction support and greater capabilities for modeling relationships."
> "An **elastic** table stores data using Azure Cosmos DB. Elastic tables automatically scale horizontally to handle large amounts of data and high levels of throughput with low latency."

**Why it matters**: this is the clearest published statement of the consistency contract. Microsoft states the *choice criterion* ("requires strong data consistency" → standard) rather than a formal guarantee document for standard tables; the substrate statement (Azure SQL, transaction support) is the supporting evidence. Read-after-write on standard tables is not spelled out as a named guarantee anywhere located in this pass — see Unknowns.

**Decision impact**:
- *Data requirement*: "the confirmation screen must show the order exactly as just saved, including server-computed fields."
- *Constraint*: this requires the strong-consistency / transactional side, i.e. standard tables. Choosing elastic to survive volume moves the burden onto the client to carry `x-ms-session-token` (`MSCRM.SessionToken` header / `SessionToken` optional parameter) on every subsequent read, and forfeits multi-table transactions, deep insert and complex joins.
- *Architectural implication*: elastic is a **per-table** decision for the high-churn, weakly-related data (telemetry, events, log lines, staging), not a global escape hatch for an audited transactional order model. Mixed models are sanctioned: "A combination of elastic and standard tables might be appropriate".

**Conditions**: elastic-table page still lists known issues, incl. no session token returned for delete operations.
**Confidence**: High for the quoted criteria; Medium for inferring standard-table read-after-write (not stated as such).
**Sources**: S3, S4.

---

#### SC-07 — Bulk-write throughput: what Microsoft actually prescribes (and refuses to number)

**Classification**: Throughput engineering — documented, deliberately non-numeric.
**Origin**: MS (T1).

**Evidence** [S4]:

> "The type of table you choose to store your data has the greatest impact on how much throughput you can expect with bulk operations."

> "If data load times are your primary concern, elastic tables provide the best performance."

Degree of parallelism:

> "Dataverse returns data in a response header that tells you a [recommended degree of parallelization (DOP) for your environment]. Performance worsens if you send more parallel requests than the response header recommends. The client hardware you use to run your application might need more CPU cores to send this many requests in parallel. You might need to use more clients to get maximum throughput."

> "Depending on your client-side architecture, you might need to split the recommended degree of parallelism. For example, when you have two clients, and your recommended DOP is 50, configure each client to use 25."

> "Not every Dataverse environment has the same number of web server resources allocated to it. Dataverse scales to the need of the environment by adding more web server resources to support it. A production environment supporting thousands of active users requires more web servers than a trial environment."

Batch sizing:

> "You can send up to 1,000 operations per request, but for best results, start with a smaller number and experiment to determine what size batch works best for your case."

> "Each operation within the request is applied sequentially on the server, so there's no improved efficiency per operation."

> "Both bulk operation and batch APIs see significant performance gains when used in parallel."

The calibration statement:

> "Bulk operation projects always make extraordinary demands, so you need to be prepared to manage the errors that service protection limits return. **If you aren't getting some service protection limit errors, you haven't maximized the capability of your application.**"

> "Service protection limit errors are just another kind of transient error that your client should be prepared to handle, like a temporary loss of network connectivity. ... The only difference is that service protection limits tell you how long you need to wait before retrying."

Bypass:

> "As a developer of a client application performing the bulk operation, you can apply an [optional parameter] to the requests you send to bypass logic. **Only a system administrator, or users who are granted a specific privilege, can use this header.**"

> "However, disabling plug-ins disables the logic from being applied from *any* client. Any user or other process adding data to Dataverse during this period won't have any of the business logic applied."

Affinity:

> "you see best results when you configure your client to use all the available web servers by [removing the Azure affinity cookie] that tries to associate your application to a single web server. Disabling Azure affinity isn't appropriate for interactive applications that use cached data from the server to optimize the user experience."

**Why it matters**: Microsoft publishes **no throughput figure** — no rows/second, no records/hour. Every quantitative lever (DOP, batch size) is defined as *environment-returned* or *experimentally determined*. The 429 rate is redefined as a *tuning signal*, not a failure.

**Decision impact**:
- *Data requirement*: "we must load/refresh X million rows in a Y-hour window."
- *Constraint*: feasibility is unpublished and environment-specific; the only honest answer pre-build is "must be measured".
- *Architectural implication*: budget an explicit **throughput spike** in the plan — build the client, read the DOP header, tune batch size upward from small, and record achieved rows/hour as a project fact. Treat 429 handling with Retry-After as a functional requirement of the loader, not an error path. Note the bypass header needs sysadmin or an explicitly granted privilege — a governance conversation, not a code switch.

**Conditions**: standard tables; the "not all core tables support bulk APIs" limitation (Account, Contact named) still applies.
**Confidence**: High.
**Sources**: S4.

---

#### SC-08 — Power Automate as an integration engine: the performance profile is the real budget unit

**Classification**: Throughput envelope — hard numbers, published.
**Origin**: MS (T1).

**Evidence** — [S5] *Limits of automated, scheduled, and instant flows*, ms.date 2026-07-17:

> "A flow's *performance profile* determines its Power Platform request limits."

Profiles (verbatim table):

| Performance profile | Plans |
| --- | --- |
| Low | "- Free - Microsoft 365 plans  - Power Apps Plan 1, Per App plans  - Power Automate Plan 1  - All license trials - Dynamics 365 Team Member- Microsoft Power Apps for Developer" |
| Medium | "- Power Apps triggered flows, manual flows, child flows, Power Apps Plan 2, Power Apps per user plan - Power Automate Plan 2, Power Automate Premium ... Dynamics 365 Enterprise plans, Dynamics 365 Professional plans - Dynamics 365 non-licensed users, application users, users with special free licenses" |
| High | "Power Automate Process license, Power Automate per flow plan" |
| Unlimited Extended | "Pay-as-you-go flows, Dynamics in context flows running under service principal" |

> "A cloud flow uses the plan of its owner. If a cloud flow is shared with multiple people, then generally the owner is the flow's creator. ... **If the original owner leaves the organization, the flow reverts to the Low performance profile.**"

> "If a user has multiple plans, such as a Microsoft 365 plan and a Dynamics 365 plan, the flow has the performance profile of the higher of the plans."

Throughput table (transition-period limits) [S5]:

> "| Power platform requests per 5 minutes | 100,000 |"
> "| Power platform requests per 24 hours | **10,000 for Low; 200,000 for Medium; 500,000 for High; 10,000,000 for Unlimited Extended** | These limits represent approximations of how many requests are allowed daily. **They aren't guarantees.** Actual amounts might be smaller, but are greater than the documented request limits and allocations during the licensing transition period. |"
> "| Concurrent outbound calls | **500 for Low; 2,500 for all others** |"

Counting confirmation [S5]:

> "These requests are counted for all types of actions, including connector actions, HTTP actions, and built-in actions, from initializing variables to a simple compose action. Both successful and failed actions count toward the limits. Retries and requests from pagination also count as action runs."

> "To view the number of actions your flow runs, select **Analytics** on the flow details page and check the **Actions** tab."

Process stacking [S5]:

> "you can stack multiple Process licenses on a single cloud flow to increase its daily action entitlement. Each additional license adds 250,000 actions per day. Alternatively, you can share a single Process license across up to 25 flows by using a flow group. **Stacking isn't available for flow groups** - if a workload needs more than 250,000 actions per day, assign Process licenses directly to the individual flow."

Content throughput [S5]:

> "| Content throughput per 5 minutes | 120 MB for Low; 1.2 GB for all others |"
> "| Content throughput per 24 hours | 200 MB for Low; 2 GB for Medium; 10 GB for High | 2.5 GB for Low; 20 GB for Medium; 50 GB for High |"

**Why it matters**: three separate budgets constrain a flow simultaneously — the *owner's* daily entitlement (SC-04/SC-05), the *flow version's* profile-based throughput, and the *content* (payload) throughput. The attachment-heavy scenario hits the third, easy to miss because it is measured in bytes, not requests.

**Decision impact**:
- *Data requirement*: "3,000 transactions/day, each carrying 2 attachments."
- *Constraint*: attachment bytes flowing through flow run history count against 2 GB/day (Medium) or 10 GB/day (High); at Low profile the ceilings are 10,000 requests and 200 MB/day.
- *Architectural implication*: do not let attachment bytes transit a flow if avoidable — pass URLs/references or move the binary through a client or direct upload. And an integration owned by an individual becomes a **Low-profile** flow the day that person leaves; ownership by a service principal with a Process licence removes that failure mode.

**Conditions**: numbers quoted are *transition-period* limits and are explicitly non-guarantees.
**Confidence**: High.
**Sources**: S5, S1.

---

#### SC-09 — Loop, concurrency and paging caps put a hard ceiling on "process every row in a flow"

**Classification**: Design envelope — hard numbers, published.
**Origin**: MS (T1).

**Evidence** [S5], concurrency/looping/debatching table:

> "| Concurrent runs | - Unlimited for flows with Concurrency Control turned off- 1 to 100 when Concurrency Control is turned on (defaults to 25) | ... **Turning on Concurrency Control can't be undone without deleting and re-adding the trigger.** |"
> "| Waiting runs | - Not applicable when Concurrency Control is off  - 10 plus the degree of parallelism (1-100) when Concurrency Control is on | ... **To ensure all triggers result in flow runs, leave the Concurrency Control setting off in the flow's trigger.** |"
> "| Apply to each array item | **5,000 for Low, 100,000 for all others** | To filter larger arrays, you can use the query action. |"
> "| Apply to each concurrency | **1 is the default limit. You can change the default to a value between 1 and 50 inclusively.** |"
> "| Split on items | - 5,000 for Low without trigger concurrency - 100,000 for all others without trigger concurrency - **100 with trigger concurrency** |"
> "| Paginated items | **5,000 for Low, 100,000 for all others** | To process more items, trigger multiple flow runs over your data. |"

Definition limits [S5]:

> "| Actions per workflow | 500 | ... Consider using child flows to reduce the number of actions in a single flow ... |"
> "| Allowed nesting depth for actions | 8 |"
> "| Number of flows owned by a single user | 600 |"

Duration [S5]:

> "| Run duration | 30 days |"  "| Run retention in storage | 30 days |"
> "| Minimum recurrence interval | 60 seconds |"
> "| Outbound synchronous request | 120 seconds (2 minutes) |"  "| Inbound request | 120 seconds (2 minutes) |"

Retry policy [S5]:

> "| Low | This policy sends up to two retries at *exponentially increasing* intervals, which scale by 5 minutes up to an interval of approximately 10 minutes for the last retry. |"
> "| Medium, High | This policy sends up to 12 retries at *exponentially increasing* intervals, which scale by seven (7) seconds up to an interval of approximately 1 hour for the last retry. |"
> "| Retry attempts | 90 |" / "| Retry maximum delay | One (1) day |" / "| Retry minimum delay | Five (5) seconds |"

**Why it matters**: `Apply to each` default concurrency is **1** — a serialized loop. The instinct is to raise it toward 50, which multiplies pressure on the Dataverse service-protection concurrency ceiling per user. Retries at Medium/High default to *12 attempts*, and each attempt is a chargeable request (SC-02).

**Decision impact**:
- *Data requirement*: "the nightly job must reconcile 80,000 rows in a 4-hour window."
- *Constraint*: one flow run can page at most 100,000 items (non-Low) and loop at most 100,000 array items, with 1–50 parallel iterations.
- *Architectural implication*: for volumes near these caps, the sanctioned pattern is Microsoft's own wording — "trigger multiple flow runs over your data" / "Distribute the workload across more than one flow". Above that, move to a client application using bulk APIs (SC-07). Set retry policy deliberately: the default 12 retries is a 12x budget multiplier on a persistently failing action.

**Conditions**: numbers differ for Low vs all other profiles; concurrency control is irreversible without re-adding the trigger.
**Confidence**: High.
**Sources**: S5.

---

#### SC-10 — Flows get turned off: 14 days failing, 14 days throttled, 90 days idle

**Classification**: Operational risk — hard rule, published.
**Origin**: MS (T1).

**Evidence** [S5], retention limits table:

> "| Flows with errors | **14 days** | A cloud flow that has a trigger or actions that fail continuously is turned off. |"
> "| Flows without trigger activity | **90 days** | A cloud flow that isn't triggered within a 90 day period might be turned off. **Flows owned by users with premium licenses or assigned capacity licenses (Power Automate Process, per flow) aren't subject to this suspension.** Flow owners and co-owners are notified 30 days prior to suspension, and can turn the flow back on for it to continue operating. |"
> "| Consistently throttled flows | **14 days** | A cloud flow that is consistently throttled is turned off. **Assign Power Automate Process licenses to the flow to dedicate capacity and avoid throttling.** |"

And [S5]:

> "If a cloud flow exceeds one of the limits, flow activity slows. It automatically resumes when the sliding window has activity below the limit. However, if a cloud flow consistently remains above the limits for 14 days, the system turns it off. Be sure to monitor email for notifications about such flows."

> "The Power Automate maker portal and the Power Platform admin center show suspended flows as suspended. ... the flow has **State=Suspended** with appropriate **FlowSuspensionReason** and **FlowSuspensionTime** values."

**Why it matters**: exceeding the budget is not only slow — it is a **silent decommission** of the integration after 14 days. Quarterly or annual processes are exposed to the 90-day idle rule unless the owner is premium-licensed.

**Decision impact**:
- *Data requirement*: "a compliance job that only runs at quarter end."
- *Constraint*: 90-day idle suspension unless owner holds a premium or capacity licence.
- *Architectural implication*: budget breaches must be alerted on, not discovered. Monitor `State=Suspended` / `FlowSuspensionReason` for any business-critical flow; give low-frequency critical flows a premium- or Process-licensed owner.

**Conditions**: notifications go to owners/co-owners; 30-day pre-warning applies to idle suspension only.
**Confidence**: High.
**Sources**: S5.

---

#### SC-11 — PE:08 is the read/write shape doctrine: prefilter on the server, avoid N+1, cache the static, optimize the update

**Classification**: Design doctrine — qualitative, no thresholds.
**Origin**: MS (T1).

**Evidence** — [S2] *Optimize data performance recommendation (PE:08)*, ms.date 2025-08-15:

> "**PE:08 | Optimize data performance. Optimize data stores for their intended and actual use in the workload.**"

Read-side:

> "*Optimize query performance.* Analyze and optimize queries that run in the workload. Use techniques such as query optimization and caching. **Use server-side views to prefilter data.**"

> "*Avoid the N+1 query problem.* Minimize the number of roundtrips to the database by using joins and batch fetching to retrieve related data efficiently."

> "*Cache queries.* Store the results of frequently run queries for easy reuse. Query caching eliminates the need for repeatedly running the same query, and it reduces query processing overhead."

> "Caching improves read speeds and user response times, especially for frequently accessed data. **This method is most effective on static data or data that rarely changes.**"

> "*In-memory caching*: ... For example, you can use variables in cloud flows or collections in canvas apps to cache data."

> "*Database query caching*: ... Also consider using server-side views where possible to prefilter data to narrow down data relevant to your query."

> "**Tradeoff**: If underlying data changes frequently, implement a cache invalidation mechanism to ensure that the cached data remains up to date."

Write-side (the section is literally titled *Optimize data updates*):

> "Updates can affect performance more than other operations because they can trigger unnecessary work and cause locking conflicts."

> "*Data changes*. Optimize automation to use pre-images of the data or filters to minimize work when no actual change has occurred. Avoid triggering automation for unmodified data."

> "*Automation*. Evaluate when and how updates are triggered based on data changes, and optimize triggers to include a filter. ... Evaluate updates that incrementally trigger automations multiple times. Instead, consider whether you can create a custom operation to handle all processing. For example, if an order ships and the ship date and tracking number are updated separately, they could both be updated at the same time in a custom 'ShipOrder' operation."

> "*Deadlocks*. Evaluate slow update operations that might be causing issues due to multiple flows updating the same data in different sequences. This inefficiency can lead to locking conflicts or even potential deadlocks, resulting in unnecessary rework. **Update the different resources in the same sequence to minimize contention.**"

> "*Bulk updates*. If you run operations on multiple rows of a table, consider using bulk operations."

Volume/partitioning/archiving:

> "*Analyze the data volume.* Assess the volume of your data to understand the overall size and growth patterns. Determine the number of records or documents and the size of individual tables or collections. This information helps you estimate storage requirements and identify scalability issues."

> "Partitioning enhances data performance efficiency by distributing the workload and improving parallel processing. ... For example, if using Dataverse Elastic tables consider what should be the partitioning key."

> "Archiving relocates older, less-frequently accessed data to more cost-effective storage. Purging data permanently removes redundant data. Both methods contribute to performance efficiency by reducing data volume, increasing data access speed, and reducing backup and recovery times."

Indexing / replicas (note: written generically about Azure data services, **not** as a Dataverse capability):

> "Use SQL Database to perform [automatic tuning] for queries to improve their performance."
> "**Optimize storage load**: Many Azure database services support read replicas. The availability and configuration of read replicas vary depending on the Azure database service."

**Why it matters**: PE:08 is the only first-party page that treats read-heavy and write-heavy as distinct optimization problems. Note carefully what it does **not** do: it gives no row counts, no read/write ratios, no cache TTLs. Every number is left to the workload. The read-replica sentence is about Azure database services generally and must **not** be read as a Dataverse standard-table feature.

**Decision impact**:
- *Data requirement*: "the app is read-heavy during the day and write-heavy at night."
- *Constraint*: read cost is dominated by roundtrips and payload width; write cost is dominated by triggered automation, locking order, and update granularity.
- *Architectural implication*: (a) one server-side view per screen, not client-side joins; (b) merge multi-field updates into one custom operation so automation fires once, not N times; (c) enforce a consistent resource-update order across all automation to avoid deadlocks; (d) plan archiving before the table is large, not after.

**Conditions**: qualitative guidance; the SQL/Cosmos indexing paragraphs describe Azure services, not Dataverse's own knobs.
**Confidence**: High for the quotes; Medium for read-replica applicability to Dataverse (see SC-14 / Unknowns).
**Sources**: S2.

---

#### SC-12 — Canvas apps page in ~100 records by default and CountRows returns a *cached* value

**Classification**: Client read shape + consistency exception — documented.
**Origin**: MS (T1).

**Evidence** — [S6] *Small data payloads in Power Apps*, ms.date 2023-12-01:

> "when connected directly to a remote data source, a Gallery control **pages in data in small increments, for example, 100 records**. This default leverages the fact that an end user rarely really needs more than a hundred records for a user task."

> "When the data source is bound directly to a gallery or table, then the data is paged or handed back the data to Power Apps in small performant increments of 100 records."

> "**Dataverse supports CountRows in a limited way. Dataverse calculates the size of the table periodically and keep that value around. When CountRows is called, you're given that value. That way it doesn't have to perform a full table scan to get the exact number for every CountRows call. But Dataverse also supports an exact count with CountIf up to 50,000 rows.**"

> "In contrast, SharePoint doesn't support this function. So, a Power Fx expression with CountRows or CountIf for SharePoint isn't delegated. Instead, Power Apps downloads a limited number of rows, 500 – 2000. Power Fx works on the 500/2000 records locally and returns a result. If your data is always less than 500/2000 records this approach can work. **But if it's greater than 500/2000 records you might get incorrect results.**"

> "Aim for the default query for a gallery or table to only return approximately **100 – 200 records**."
> "Consider using a data source based view that automatically filters the data. **Most enterprise-grade apps make heavy use of views on the data source.**"
> "Consider requiring search arguments in the UI before you show data."
> "By default, Power Apps computes the actual columns you need for a given query using a feature call **Explicit Column Selection**. This feature is on by default for all new apps."

Scale claim from [S7] *How to create performant Power Apps*, ms.date 2026-08-20:

> "Power Apps guides you toward well known performant patterns by default. These patterns include streamlined data loading at launch, automatic incremental paging, caching data for collections, and loading only essential data for each page. **Many successful Power Apps implementations use more than 100 tables and over 50 screens while keeping excellent performance.**"

> "Common anti-patterns include loading too much data, turning everything into collections, and overloading OnStart."

**Why it matters**: **`CountRows` on a Dataverse table is a periodically-refreshed cached number, not a live count.** That is a documented, first-party consistency exception inside the "standard tables are strongly consistent" story — and it is invisible to the user. Any KPI tile or dashboard number built on `CountRows` is stale by an unstated interval. Exact counts are only available via `CountIf` up to 50,000 rows.

**Decision impact**:
- *Data requirement*: "the home screen shows 'X open orders' and it must be right."
- *Constraint*: `CountRows` gives a periodically-calculated table size, not a transactional count; `CountIf` is exact only to 50,000 rows.
- *Architectural implication*: do not put a `CountRows`-based figure next to a transactional list and imply they agree. If an exact count is a requirement, either bound it below 50,000 with `CountIf` or maintain the count as a materialized column updated by server logic. Design galleries to the 100–200 record default and use server-side views plus mandatory search arguments to stay there.

**Conditions**: Dataverse; the 500/2000 non-delegable truncation applies to non-delegable sources/expressions.
**Confidence**: High.
**Sources**: S6, S7.

---

#### SC-13 — Move the mashup to the server: views, no per-row lookups, deliberate denormalization

**Classification**: Design doctrine — qualitative.
**Origin**: MS (T1).

**Evidence** — [S8] *Optimized query data patterns in Power Apps*, ms.date 2023-12-01:

> "The simplest and fastest data query pattern is: 1. A single table or view 2. Prefiltered on the server to what you need 3. Columns are indexed correctly for the expected queries"

> "**Use server-side views.** Views are probably the most common tool to help balance these goals. They present a single table structure for queries, prefilter data for what you need in the query, and enable lookups and joins to other tables. Because the filters, lookups and joins for the view are computed on the server, both the payload and client-side compute are minimized."

N+1 in the client:

> "For each record in the gallery, the app needs to run a separate query to the other data source and get the lookup value. This means that the app may need to run many queries for each record, which can take a long time and affect the app performance. **This anti-pattern is sometimes known as 'N squared, (n^2)' or an 'N+1' problem.**"

> "In general, use an expression that leverages an index like **StartsWith** or **Filter** instead of one that reads the entire table like **In**. The In operator is fine for in-memory collections or if the external data source table is very small."

Deliberate staleness as a design tool:

> "Sometimes data is slow to access in a query because it is stored in a different location or format. To make the query faster, you can copy the slow data and store it locally in a table that is fast and easy to query. **However, this means that the local data may not be the most updated version of the original data.** Then run another process to update the local data periodically."

> "**The key question is: how up to date must this data be?** If you can afford some delay, you can use this technique to speed up your app."

> "There's a trade-off between query speed and data normalization. ... sometimes you need to duplicate some data to make the queries faster and easier."

**Why it matters**: this is the read-side answer to write amplification. Every avoided per-row lookup is an avoided request against the user's entitlement *and* against the 5-minute service-protection window. Microsoft frames freshness explicitly as a **negotiable business requirement**, which is exactly the question an engagement must ask rather than assume.

**Decision impact**:
- *Data requirement*: "the list shows order + customer + salesperson + status."
- *Constraint*: rendering that from four tables client-side costs one request per row per lookup — the N+1 pattern — against a per-user budget.
- *Architectural implication*: a **server-side view per screen** is a first-class deliverable of the design, alongside the screen itself. Where the source is slow or remote, ask the business the freshness question ("how old may this be?") and record the answer — it determines whether a replicated local table is admissible.

**Conditions**: canvas apps; the "duplicate data" pattern trades consistency for speed and must be an explicit, recorded decision.
**Confidence**: High.
**Sources**: S8.

---

#### SC-14 — Power Pages: a documented 15-minute staleness window, and an explicit "never guaranteed to be immediate"

**Classification**: Consistency exception — explicit, published.
**Origin**: MS (T1).

**Evidence** — [S9] *How server-side caching works in Power Pages*, ms.date 2026-04-29:

> "In order to improve scalability and performance, Power Pages websites cache the data that is queried from Microsoft Dataverse. This caching is done on the application server for all business data and website metadata and is different from browser based or content delivery network caching of static resources."

Configuration tables:

> "All configuration table data is same for all users and is cached automatically. This configuration data cache for any table is updated automatically when any record is changed. **Automatic cache update has a service level agreement of 15 minutes.** Any change done for a configuration record would be automatically available on the website within 15 minutes."

Data tables:

> "This data is typically cached per user except in certain cases like anonymous users or tables with global permission. Also only the data accessed by user on the website is cached and not the data for whole table."

> "Any record for a table (or a related table) is created, updated, or deleted on the website by any website user. **The action will instantaneously clear the cache for all the website users for that specific table.**"
> "**Cache is cleared automatically within 15 minutes even if no changes are made.**"

FAQ — the decisive statements:

> "Can I change the cache refresh duration from 15 minutes to a lesser duration? **No. SLA for cache refresh remains 15 minutes.** Any changes from Dataverse will reflect on the website within 15 minutes for both data tables and configuration tables."

> "I'm using plugins or workflows to update data in other tables and need these data changes to reflect immediately on my website. **This design approach isn't recommended. Except the primary record where the create or update action is triggered, data reflection from Dataverse to websites is never guaranteed to be immediate.**"

> "How long does it take for changes to reflect from a website to Dataverse? **Immediately, as long as the update changes a primary record and isn't based on indirect changes to data using post operation plugins or workflows.**"

> "The clear cache option should be seldom used as it clears cache for all data tables as well as configuration tables and can cause temporary slowness. For live site with heavy usage, this can lead to users facing performance issues."

**Why it matters**: this is the sharpest published consistency statement in the whole Power Platform surface — **writes into Power Pages are immediate; reads of anything changed *outside* the page (plug-in, flow, back office) are eventually consistent with a 15-minute, non-tunable SLA.** It contradicts the naive assumption that a portal is just a thin view over Dataverse.

**Decision impact**:
- *Data requirement*: "the external partner submits a request, back-office logic enriches it, and the partner sees the enriched result."
- *Constraint*: the enrichment is produced by a plug-in/flow, so its visibility on the site is bounded by the 15-minute cache and explicitly "never guaranteed to be immediate".
- *Architectural implication*: design the portal journey so the user's own write carries everything the user must immediately see. Anything computed asynchronously must be presented as pending, or delivered through a channel that bypasses the cache (notification, direct-write pattern). Do not sell "real time" on Power Pages for server-derived values. Never design an operational process around the manual clear-cache button.

**Conditions**: Power Pages only; the per-user data cache is invalidated instantly by *website-originated* writes.
**Confidence**: High.
**Sources**: S9.

---

#### SC-15 — Analytical traffic is not isolated: TDS runs under service protection limits

**Classification**: Workload isolation — explicit statement.
**Origin**: MS (T1).

**Evidence** — [S10] *Use SQL to query data (Microsoft Dataverse)*, ms.date 2026-06-01:

> "**Queries using the TDS endpoint execute under the service protection API limits.**"

> "The Microsoft Dataverse business layer provides a Tabular Data Stream (TDS) endpoint that emulates a SQL data connection. The SQL connection provides read-only access to the table data of the target Dataverse environment ... The Dataverse endpoint SQL connection uses the Dataverse security model for data access."

Timeouts and sizing:

> "The Dataverse TDS endpoint no longer has a hard maximum size limit. Instead, there's a **fixed five (5) minute timeout**. With the introduction of data streaming, you can retrieve as much data as can be completed in the fixed five (5) minute timeout. **Consider using data integration tools such as Azure Synapse Link for Dataverse and dataflows for large data queries that require more than five (5) minutes to complete.**"

> "The five (5) minute timeout **can be adjusted to two (2) minutes depending on the query complexity**. For example, queries containing `SELECT *`, `NESTED FROMs and/or JOINs` automatically adjust the timeout limit to two (2) minutes as those queries put too much pressure on the server when left running for a long time."

Query shape guidance:

> "When building a query, only return the necessary columns. ... In general, **keeping a query under 100 columns is recommended.**"
> "It's important to use a top clause in your queries to prevent trying to return the whole table of data."
> "When building queries, **don't use the table hint NOLOCK. This hint prevents Dataverse from optimizing queries.**"
> "the label portion ('choicecolumn' name) is stored separately, which cost more to retrieve and **can't be indexed**. Using a significant number of choice label columns may generate a slower performing query."
> "Including a large number of choice labels in your query have significant impact on performance. It's best to use less than 10 labels if possible."

Other constraints:

> "Querying data using SQL doesn't trigger any plug-ins registered on the RetrieveMultipleRequest or RetrieveRequest messages."
> "**The TDS endpoint can't be used with elastic tables.**"
> "the tables types 'virtual' and 'audit' aren't supported at this time."
> "To prevent data exfiltration, turn on the user level access control for TDS endpoint."

**Why it matters**: a Power BI report over TDS, or an analyst in SSMS, spends the **same** service-protection budget as the operational app, under the *querying user's* identity. Reporting is therefore not free and not isolated. Microsoft's own escape hatch is named explicitly: Synapse Link / dataflows for anything beyond five minutes.

**Decision impact**:
- *Data requirement*: "management dashboards refresh hourly over the transactional data."
- *Constraint*: TDS reads count under service protection limits; 5-minute (or 2-minute for `SELECT *`/nested joins) timeout; no elastic-table access; audit tables not reachable.
- *Architectural implication*: **separate the analytical plane** — Synapse Link / Fabric / dataflows into an analytical store — before reporting volume is material. DirectQuery-style patterns aimed at Dataverse put analyst behaviour directly into the operational envelope. Reporting over *audit* data is not possible via TDS at all, which matters for the "audited" half of the volume scenario.
**Conditions**: TDS/SQL endpoint; must be enabled (on by default); Entra ID auth only.
**Confidence**: High.
**Sources**: S10.

---

#### SC-16 — Microsoft publishes NO concurrent-user ceiling; what governs instead is per-identity limits plus your own tested baseline

**Classification**: Absence of a published envelope — explicit negative finding.
**Origin**: MS (T1), by exhaustion.

**Evidence**: across the pages read in this pass — [S1] request limits, [S2] PE:08, [S4] bulk operations, [S5] Power Automate limits, [S11] PE:02 performance planning, [S12] PE:05 performance testing — **no page states a maximum number of concurrent users an environment, app or Dataverse database supports.** The closest first-party statements are:

[S4] *Optimize Performance for Bulk Operations*:
> "Dataverse is designed as a data source to support multiple applications with large numbers of concurrent users."
> "Not every Dataverse environment has the same number of web server resources allocated to it. Dataverse scales to the need of the environment by adding more web server resources to support it. A production environment supporting thousands of active users requires more web servers than a trial environment."

[S7] *How to create performant Power Apps*:
> "Many successful Power Apps implementations use more than 100 tables and over 50 screens while keeping excellent performance."

**The decision is contextual, and Microsoft says so by substituting process for numbers.** [S11] *Performance planning recommendation (PE:02)*, ms.date 2025-08-15:

> "Capacity planning refers to the process of determining the resources required to meet workload performance targets."
> "Estimate the expected demand for your resources based on historical data, market trends, and business projections. **Consider the number of transactions, concurrent users, or any other relevant metrics.**"
> "*API Requests*: Evaluate your API request consumption against your available capacity and the service protection limits. Consider factors like initial load of data and potential spikes in usage."
> "*Security modeling*: Will your security rules work well with a lot of users and data? Are there any bottlenecks?"
> "You also need to determine **reachable limits**, which involves identifying the maximum thresholds or boundaries of a workload. These limits usually apply to infrastructure (compute, storage, network), application (concurrent connections, response times, availability), and service (requests per second). **When capacity planning identifies reachable limits, you need to modify the workload before the limit creates a performance problem. Performance baselines, continuous monitoring, and testing are essential to validating the limits and the solution.**"
> "**There are scaling limits within your configuration and services that you should be aware of. You can read the documentation or run tests.**"
> "if you aim to support an integration with 1 million updates nightly, but current data shows slow update speeds, you need to adjust your system."

Planning triggers [S11]:
> "Design (prediction) / Regular spikes (8:00 AM sign-in rush) / Launch (prediction validation) / Business model change / Acquisition or merger / Marketing push / Seasonal change / Feature launch / Periodically"

**Why it matters**: any answer of the form "Power Platform supports N concurrent users" is fabricated. The governing limits are **per authenticated user** (service protection) and **per identity per 24 hours** (entitlements) — meaning concurrency scales with users almost by construction, and the real ceilings appear at *shared* identities (integration service accounts), *shared* rows (locking), and *shared* automation (a single flow owner).

**Decision impact**:
- *Data requirement*: "800 field users, ~150 concurrent at the morning peak."
- *Constraint*: no published ceiling to check against; the binding constraints are per-user limits, contention on hot rows, and any single identity that funnels many users' work.
- *Architectural implication*: state explicitly in the design that user-count scaling is **not** the risk; identify instead every *funnel point* where many users' traffic collapses onto one identity or one row, and size/test those. Answer the concurrency question with a **tested baseline**, not a quoted number.

**Conditions**: valid as of this research pass; a future published figure would supersede.
**Confidence**: High that no ceiling is published in these pages; Medium that none exists anywhere on Learn (absence proof is bounded by pages read).
**Sources**: S1, S2, S4, S5, S7, S11, S12.

---

#### SC-17 — PE:05 turns "will it scale?" into a testable contract

**Classification**: Method — qualitative, first-party.
**Origin**: MS (T1).

**Evidence** — [S12] *Performance testing recommendation (PE:05)*, ms.date 2026-07-17:

> "**PE:05 | Test performance. Perform regular testing in an environment that matches the production environment. Compare results against the performance targets and the performance benchmark.**"

> "conduct performance tests as early as possible in the development lifecycle. Early testing allows you to catch and fix performance issues before you go to production. **You can use a proof of concept (POC) if production code isn't ready.**"

> "**If migrating data from a prior system and migration must be completed in a specific time window, your performance testing should include measuring performance of the data migration.**"

Test types (verbatim table):
> "| Load testing | Simulate realistic user loads to measure how your workload performs under expected peak workloads. | Determines load tolerance. |"
> "| Stress testing | Push your workload beyond its normal limits to identify its breaking points and measure its ability to recover. | Determines resilience and robustness. |"
> "| Soak testing (endurance testing) | Run your workload under sustained high loads for an extended period to identify performance degradation, memory leaks, or resource issues. |"
> "| Spike testing | Simulate sudden increases in user load to assess how your workload handles abrupt changes in demand. |"

User modelling:
> "User personas: **Understand the number and types of users who will use your solution at the same time.** Define user personas that represent different roles, locations, security configurations, data sets, and activities."
> "Define day-in-the-life scenarios that reflect the actions users perform on a typical day. **Include peak load and normal load scenarios.**"
> "**Use realistic data volumes for each scenario. Don't use more or less data than users need.**"

The 2-second example is explicitly an *example*, not a platform standard:
> "you might have a target for your response time to be under a certain threshold, such as less than 2 seconds."
> "suppose your performance target for response time is 2 seconds or less. Your acceptance criterion could be *The average response time of the workload should be less than 2 seconds*."

Shared-infrastructure caution:
> "When planning and running performance tests it's important to remember that, in many cases, **the Microsoft Cloud uses shared infrastructure to host your assets and the assets belonging to other customers. Limit tests to avoid unintended consequences.**"

Tooling named [S12]: Azure Pipelines, **Power Platform Playwright samples**, Azure Test Plans, Azure Load Testing + Azure Chaos Studio (for Azure resources), **Power Apps Monitor**, Application Insights / Azure Monitor.

> "*Set degradation limits*. Define numeric thresholds that specify the level of performance degradation that's acceptable over time."
> "*Include quality assurance*. Incorporate performance requirements, such as maximum requests per second, into the quality assurance process. **Treat performance requirements with the same level of importance as functional requirements.**"

**Why it matters**: this closes SC-16. Since no ceiling is published, the deliverable is a *measured* baseline plus acceptance criteria. Note the shared-infrastructure caution — Power Platform load testing is not unconstrained; you cannot simply blast a production tenant.

**Decision impact**:
- *Data requirement*: "must handle the Monday-morning peak."
- *Constraint*: the platform will not tell you if it can; only a load test against a production-like environment with realistic data volumes will.
- *Architectural implication*: put a performance-test environment, realistic test data (with a scrubbing strategy — [S12] flags the sensitive-data risk), and an APM tool into the project budget at kickoff. Write "maximum requests per second" into the acceptance criteria alongside functional requirements. If a data migration has a window, **test the migration itself**.

**Conditions**: 2 seconds is an illustrative example only — never cite it as a Microsoft standard.
**Confidence**: High.
**Sources**: S12.

---

#### SC-18 — Large tables: no published size envelope; Dataverse tunes itself and index requests go through support

**Classification**: Absence of an envelope + platform behaviour.
**Origin**: MS (T1).

**Evidence** — [S13] *Optimize performance using QueryExpression*, ms.date 2025-08-11:

> "**Automatic query optimization.** Don't be surprised when the performance of a slow query improves without any change on your part. Dataverse actively monitors data retrieval operations to improve performance. When a specific query using standard tables performs poorly, Dataverse might automatically make changes that improve the performance of the query. **This behavior might make certain performance issues appear transient because they can't be reproduced later.** Automatic query optimization doesn't require any configuration. It's enabled by default for everyone."

> "**Only apply these options when recommended by Microsoft technical support. Incorrect use of these options can damage the performance of a query.**" (on `QueryExpression.QueryHints` — `ForceOrder`, `DisableRowGoal`, `LoopJoin`, `MergeJoin`, `HashJoin`, `NO_PERFORMANCE_SPOOL`, etc.)

> "In earlier versions, the QueryExpression.NoLock property used to prevent shared locks on records. **It's no longer necessary to include this property**"

And [S10] TDS: "don't use the table hint NOLOCK. This hint prevents Dataverse from optimizing queries."

Elastic-table scale, the only order-of-magnitude figure located — [S14] *Create and edit elastic tables*, ms.date 2025-03-31:

> "Elastic tables are designed to handle large volumes of data in real-time. With elastic tables, you can import, store, and analyze large volumes of data without scalability, latency, or performance issues."
> "**Elastic tables automatically scale to ingest tens of millions of rows every hour.**"
> "The requirement for Contoso's marketing application is that it must be able to ingest up to 100 million or more coupon details within a few hours, read millions of coupons per hour, and send coupons to customers. **Elastic tables will automatically scale for this high throughput scenario.**"
> "As your business data grows, elastic tables provide **unlimited auto scalability** based on your application workload, both for size and throughput"
> "Use [bulk operation messages]. This allows you to achieve **10 times the throughput** with the same Dataverse API throttling limits."
> "**Since the elastic tables are isolated from the standard tables, performance for the overall marketing application won't be negatively impacted.**"
> "Each logical partition can store **20 gigabytes (GB) of data**." [S3]

Elastic trade-offs that bear on modelling [S14]:
> "Elastic tables don't support filters on related tables when creating views, advanced find, or any query in general using API. **If you frequently need to filter on related table columns, we recommend that you denormalize columns from related tables**"
> Not supported: "Business rules / Charts / Business process flows / One Dataverse connector for Power BI / Many-to-many (N:N) relationships to standard tables / Alternate key / Duplicate detection / Calculated and rollup columns / Currency columns / ... / Table sharing / Composite indexes / Cascade operations: Delete, Reparent, Assign, Share, Unshare / ... / Access teams / Queues / Attachment / Import and export functionality of table data."

**Why it matters**: **there is no published maximum row count for a Dataverse standard table.** The only quantified scale claims belong to elastic tables. Meanwhile Dataverse self-tunes standard-table queries silently — which is good for steady state and *bad for diagnosis*, because Microsoft warns that issues can become irreproducible. Customer-controlled index tuning does not exist as a self-service feature: query hints are gated behind "only when recommended by Microsoft technical support".

**Decision impact**:
- *Data requirement*: "this table will hold 40 million rows in five years."
- *Constraint*: no published size envelope for standard tables; you cannot self-service an index; hints require support engagement; automatic optimization makes performance non-deterministic over time.
- *Architectural implication*: treat table growth as a **design** input, not an operational surprise — decide the archiving/purging policy (PE:08) and the elastic-vs-standard split at design time. If a table is high-volume, weakly relational, and mostly read by partition key, elastic is the sanctioned answer *and* an isolation mechanism ("isolated from the standard tables"). But price the losses honestly: no rollups, no alternate keys, no N:N to standard, no attachments, no Power BI Dataverse connector, no cross-table filters in views.

**Conditions**: elastic figures are Microsoft's own scenario claims, not an SLA.
**Confidence**: High for the quotes; High that no standard-table row ceiling is published in the pages read.
**Sources**: S3, S10, S13, S14.

---

#### SC-19 — The DOP hint is a per-environment, time-varying number the platform hands you — there is no fixed value

**Classification**: Throughput mechanism — exact, named, non-numeric.
**Origin**: MS (T1).

**Evidence** — [S15] *Send Parallel Requests to Dataverse*, ms.date 2026-03-26:

> "Dataverse manages resource allocation for environments. Production environments that many licensed users heavily use have more allocated resources. **The number and capabilities of the servers allocated might vary over time, so there's no fixed number for the optimum degree of parallelism. Instead, use the integer value returned from the `x-ms-dop-hint` response header.** This value provides a recommended degree of parallelism for the environment."

> "When you use Parallel Programming in .NET, the default degree of parallelism depends on the number of CPU cores on the client running the code. **If the number of CPU cores exceeds the best match for the environment, you might be sending too many requests.**"

> "One of the three facets monitored for service protection limits is the number of concurrent requests. **By default, this value is 52 but it might be higher.** ... **If you depend on the `x-ms-dop-hint` response header value to limit the degree of parallelism, you should rarely hit this limit.**"

> "| `-2147015898` | `0x80072326` | `Number of concurrent requests exceeded the limit of 52.` |"

Server affinity:

> "When you connect to a service on Azure, the service returns a cookie with the response. All your subsequent requests try to go to the same server ... **Interactive client applications, especially browser clients, benefit from this cookie because it allows the application to reuse data cached on the server. Web browsers always have server affinity enabled and you can't disable it.**"

> "When you send requests in parallel from your client application, you can gain performance benefits by disabling this cookie. Each request you send routes to any of the eligible servers. This change not only increases total throughput, but it also **helps reduce the impact of service protection limits because each limit applies per server**."

> "Sending parallel requests within a plug-in isn't supported."

Access paths: SDK — `ServiceClient.RecommendedDegreesOfParallelism`; Web API — `whoAmIResponse.Headers.GetValues("x-ms-dop-hint")`; affinity off via `PreferConnectionAffinity=false` / `EnableAffinityCookie = false` / `HttpClientHandler { UseCookies = false }`.

**Why it matters**: the service-protection concurrency limit is **per user per web server**, and the affinity cookie pins a client to one server — so an integration that keeps affinity on is voluntarily capping itself at one server's share. Conversely, browser-based apps cannot turn it off, which means the interactive app's concurrency is bounded per server by construction. Also confirms **52 is a default, not a ceiling** ("might be higher").

**Decision impact**:
- *Data requirement*: "the loader must finish inside a 3-hour window."
- *Constraint*: parallelism is dictated by an environment-returned integer that varies over time; exceeding it *worsens* performance.
- *Architectural implication*: read `x-ms-dop-hint` at runtime and drive `MaxDegreeOfParallelism` from it — never hard-code. Split the value across clients when scaling out. Disable affinity for non-interactive loaders only. Never parallelize inside a plug-in.

**Conditions**: server-side (plug-in) code excluded; affinity must stay on for interactive/cached clients.
**Confidence**: High.
**Sources**: S15, S4.

---

#### SC-20 — DirectQuery reporting is Dataverse operational load with a Power BI face on it

**Classification**: Analytical isolation — documented.
**Origin**: MS (T1).

**Evidence** — [S16] *Power BI modeling guidance for Power Platform*, ms.date 2024-12-30:

> "**Create a DirectQuery connection by using the Dataverse connector**: ... A DirectQuery model consists only of metadata defining the model structure. **When a user opens a report, Power BI sends native queries to Dataverse to retrieve data.**"

> "**While a DirectQuery model can be a good alternative when you need near real-time reporting or enforcement of Dataverse security in a report, it can result in slow performance for that report.**"

> "Conversely, DirectQuery models only retrieve data from the source after the user opens a report, resulting in seconds of delay as the report renders. **Additionally, user interactions on the report require Power BI to requery the source, further reducing responsiveness.**"

> "A DirectQuery connection to Dataverse is a good choice when the report's query result isn't large. **A large query result has more than 20,000 rows in the report's source tables**, or the result returned to the report after filters are applied is more than 20,000 rows."

> "**The 20,000 row size isn't a hard limit. However, each data source query must return a result within 10 minutes.**"

> "**Attempting to retrieve data from all columns is an anti-pattern.** It often results in extended data refresh operations, and it will cause the query to fail when the time needed to return the data exceeds 10 minutes."

> "When you query a system user table, for example, it could contain more than 1,000 columns."

The escape hatch and the reason for it:

> "**Even larger semantic models—with several hundreds of thousand or even millions of rows—can benefit from using Azure Synapse Link for Dataverse.** This approach sets up an ongoing managed pipeline that copies Dataverse data into ADLS Gen2 as CSV or Parquet files."

> "This approach is used to report on hundreds of thousands or even millions of records in Dataverse environments."

> "**Generally, you should import data to Power BI whenever possible.**"

> "For high-usage activity, **simultaneous writes and reads can create locks that cause queries to fail**. To ensure reliability when retrieving data, two versions of the table data are synchronized in Azure Synapse." — near real-time vs "**Snapshot data**: Provides a read-only copy of near real-time data that's updated at regular intervals (in this case every hour)."

> "**If you anticipate that a high volume of read and write operations will be executed simultaneously, retrieve data from the snapshot tables to avoid query failures.**"

Refresh cadence for the import alternative:
> "You can schedule up to eight refreshes per day on a shared capacity. On a Premium capacity or Microsoft Fabric capacity, you can schedule up to 48 refreshes per day, which can achieve a 15-minute refresh frequency."

And note the crossover to SC-15: DirectQuery over the Dataverse connector reaches the same TDS surface, where [S10] states "Queries using the TDS endpoint execute under the service protection API limits."

**Why it matters**: DirectQuery makes *every report interaction* a live Dataverse query under the report user's identity and the service protection limits. Microsoft's own answer for anything past ~20,000 rows or 10 minutes is to leave the operational store. It even documents lock contention between concurrent reads and writes as a reason to read snapshots instead.

**Decision impact**:
- *Data requirement*: "operational reporting on the transaction table, near real time, honouring Dataverse security."
- *Constraint*: near-real-time + row-level security pushes you to DirectQuery, which is explicitly slow and bounded by 10-minute query time and a ~20,000-row soft guide; import is capped at 8 refreshes/day (shared) or 48 (Premium/Fabric, ~15 minutes).
- *Architectural implication*: force the freshness question early. If "near real time" is genuinely required *and* Dataverse security must be enforced, accept DirectQuery's cost and keep result sets small (dual-mode dimensions, DirectQuery facts, SSO). Otherwise **isolate analytics** onto Synapse Link/Fabric and read snapshot tables — this is the only path Microsoft describes for millions of rows, and it removes reporting from the operational request budget entirely.

**Conditions**: 20,000 rows is explicitly *not* a hard limit; the 10-minute query timeout is.
**Confidence**: High.
**Sources**: S16, S10.

---

#### SC-21 — STRUCTURE: how business volume becomes a request budget (every multiplier is engagement-measured, none is published)

**Classification**: Method / synthesis. **Not a source of numbers.**
**Origin**: INF (inference from documented counting rules only).

> **Warning to any reader or downstream author**: below, `A_*` symbols are *measurement slots*, not values. Microsoft publishes **no** amplification factors, no requests-per-transaction figures, and no rows-per-second throughput. Every slot must be filled by measurement in the target environment (Application Insights for Dataverse for Dataverse traffic — [S2]; the flow's **Analytics → Actions** tab for flow actions — [S5]; PPAC licensing reports for Power Automate consumption only — [S1]). Filling a slot from memory, from a blog, or from a "typical" figure invalidates the whole calculation.

### The four budgets that must each be checked separately

Documented in the sources, not derived:

| # | Budget | Unit of accounting | Window | Source |
|---|---|---|---|---|
| 1 | Daily entitlement | **per identity** (licensed user / non-licensed pool / flow with Process licence) | 24h sliding | S1 |
| 2 | Service protection | **per authenticated user per web server** (requests / execution time / concurrency) | 5-min sliding | established prior work; S15 |
| 3 | Flow throughput | **per cloud flow version**, by performance profile | 5-min and 24h sliding | S5 |
| 4 | Flow content throughput | **per cloud flow version**, in bytes | 5-min and 24h | S5 |

A design passes only if it fits **all four**. They do not pool: "it can't be pooled at any other level like environment or tenant levels" [S1].

### The translation skeleton

For each business event type *e* (order, line, attachment, approval, audit query…):

```
requests(e) = volume(e) × A_client(e) × A_server(e) × A_retry(e) × A_page(e)
```

Where every factor is a **measured input**, justified by a documented counting rule:

| Slot | What it captures | Documented reason it exists | Where to measure |
|---|---|---|---|
| `volume(e)` | business events/day, at **peak**, not average | — | business, from process capture |
| `A_client(e)` | calls the client makes per event (form loads, lookups, saves, gallery pages) | "Power Apps: All API requests to connectors and Microsoft Dataverse" [S1]; galleries page ~100 records [S6]; per-row lookups are the N+1 anti-pattern [S8] | Power Apps Monitor [S12]; App Insights |
| `A_server(e)` | extra CRUD caused by plug-ins, classic workflows, custom controls, and platform-internal requests completing the transaction | "including user-driven and internal system requests required to complete CRUD transactions … include plug-ins, classic workflows, and custom controls" [S1] | App Insights for Dataverse: "Dataverse API incoming calls, Dataverse plug-in execution calls, and Dataverse SDK calls" [S2] |
| `A_retry(e)` | retried attempts | "Both successful and failed actions count … Retries … also count" [S1][S5]; Medium/High default is up to 12 retries [S5] | flow Analytics; retry policy configuration |
| `A_page(e)` | pages fetched for a read | "requests from pagination also count as action executions" [S1]; page caps 5,000 (Low) / 100,000 [S5] | rows ÷ configured page size |

Flow-side, separately (because it is budget #3, not #1):

```
flow_requests = runs/day × actions_per_run(incl. every Initialize variable / Compose) × A_retry
flow_bytes    = runs/day × payload bytes through run history   (against 2 GB / 10 GB per 24h) [S5]
```

### Worked *structure* (not a worked answer)

For "3,000 orders/day, 6 lines each, 2 attachments, audited":
- The **row** counts are business facts: 3,000 orders + 18,000 lines + 6,000 attachments = 27,000 rows/day created.
- The **request** count is **not** 27,000. It is 27,000 × (unmeasured `A_server`) + all reads + all flow actions + retries + pages.
- "Audited" adds server-side work whose request accounting is not documented per-operation in the sources read → **an Unknown**, not a factor to invent.
- Whether this fits depends on **which identity** carries it (SC-05) and **which of the four budgets** it lands in — a single service account is the failure mode, not the volume.

### The output the engagement owes

1. Peak (not average) event volumes per event type, from the business.
2. A named identity for every automation, with its licence and profile.
3. A measured `A_*` set from a prototype or pilot, recorded with date and environment.
4. The four-budget check, showing headroom against each.
5. A load test validating it (SC-17), because none of the above is guaranteed by Microsoft.

**Confidence**: High for the structure and every cited counting rule; **the multipliers themselves carry no confidence because they are not published — they are slots.**
**Sources**: S1, S2, S5, S6, S8, S12, S15.

---

---

### 4.11 Data quality, ownership vocabulary, and validation-per-store (new in v2 — closes review F-10, F-11)

The following 18 findings (`DQ-01`..`DQ-18`) close two review gaps: (a) data quality coverage was limited to keys and duplicate rules — the previous pass could not find the Dynamics 365 Implementation Guide's data-quality/governance chapters (they had 404'd); this pass confirms they are live under a different URL shape and extracts them in full, including a genuine contradiction discovered in Microsoft's own business-rules documentation (`DQ-10`) and the high-impact finding that duplicate detection is suppressed by default on Web API updates (`DQ-12`); (b) "system of record" vs "source of truth" vocabulary was left undefined — `DQ-03` and `DQ-15` establish that Microsoft uses at least four overlapping labels across surfaces with no formal cross-reference, and that the closest thing to a definition (Azure Architecture Center, microservices context) ties the concept to a *consistency requirement* per entity, not to Power Platform specifically. 13 sources, all Tier 1 except two support.microsoft.com pages explicitly flagged as weaker evidence.

#### DQ-01 — The D365 Implementation Guide data chapters are ALIVE; the previous 404s were wrong URL shapes

**Classification**: Source correction / navigational
**Origin**: MS (T1)

**Evidence**
The data-management chapter set exists today under the flat `implementation-guide/data-management*` prefix (NOT under a `/data/` sub-folder). Confirmed live, with `ms.date`:

| URL | Title | ms.date |
|---|---|---|
| `https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management` | "Manage your data in Dynamics 365 implementation projects" | 2024-01-08 |
| `https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management-check-list` | "Checklist for data management and governance" | 2024-01-18 |
| `https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management-configuration-data-migration` | "Manage configuration and migration data for Dynamics 365 projects" | 2024-01-17 |
| `https://learn.microsoft.com/en-us/dynamics365/guidance/reference-architectures/dataverse-master-data-system` | "Dataverse as a master data system" | 2025-11-04 |

Note the freshness signal: all three implementation-guide pages carry `ms.update-cycle: 1095-days` (3 years) and `ai-usage: ai-assisted` / `ms.custom: ai-gen-docs-bap`. The content is AI-assisted and on a 3-year refresh cadence — it is guidance, not a spec.

**Why it matters**: an evidence file citing dead URLs is unauditable. The chapter naming is flat-prefixed, so future sub-chapters will be `data-management-<topic>`, discoverable by that pattern.

**Decision impact**: data requirement → *cite a live, dated primary source for governance claims* → constraint → *use the `data-management-*` prefix family* → architectural implication → *governance claims in the pack are traceable to T1 with an explicit 2024 date and an AI-assisted caveat*.

**Conditions**: valid as of 2026-09-02.
**Confidence**: High (fetched directly).
**Sources**: S1, S2, S3, S8.

---

#### DQ-02 — Microsoft's data-ownership vocabulary is "data steward", not "data owner"; ownership is asserted per line of business

**Classification**: Vocabulary / governance
**Origin**: MS (T1)

**Evidence** (S1, verbatim)
- "*Data management* is about the operational issues of data. *Data governance* is about taking a high-level strategic view of the policies and procedures that define the availability, usability, quality, and security of your data."
- "A *data steward* is a role that's responsible for the management and oversight of your data assets. Their goal is to provide data to users in a usable, safe, and trusted way."
- "The data steward uses established data governance processes to ensure the fitness of data elements, both the content and metadata."
- "Their specialist role incorporates processes, policies, guidelines, and responsibilities for administering your data in compliance with policy and regulatory obligations."
- "Every line of business (LOB) has a level of ownership of their data along with the use cases that drive the solution design."

From the checklist (S2, verbatim):
- "Appoint a data steward to apply and monitor the data governance principles."
- "Define a data architecture that shows a holistic view of your data repositories, their relationships, and ownership. Identify the data owners, systems, and conceptual flow between systems during your design and analysis phases."

**Why it matters**: Microsoft splits the vocabulary in two. *Ownership* sits with the line of business (a business fact, per-LOB and per-use-case). *Stewardship* is a named appointed role that operationalises governance. The checklist demands both be identified **during design and analysis** — i.e. before build, which is exactly Discovery.

**Decision impact**: data requirement → *every data domain must name an owning LOB and an appointed steward* → constraint → *Discovery must not close with unnamed owners; a "shared" owner is an Unknown, not a Confirmed* → architectural implication → *the data-architecture artefact must be a repositories × relationships × ownership map, not just an ERD*.

**Conditions**: guidance, not enforced by any product.
**Confidence**: High.
**Sources**: S1, S2.

---

#### DQ-03 — "Source of truth" is used loosely by Microsoft; there is no formal source-of-truth vs system-of-record definition in the D365 IG

**Classification**: Vocabulary gap (negative finding)
**Origin**: MS (T1)

**Evidence**
In the whole data-management chapter (S1), neither "source of truth" nor "system of record" appears as a defined term. The IG's own vocabulary for the concept is **"primary data"** and **"master data management (MDM)"** (S1, verbatim):
- "Most enterprises keep a primary set of data used across the organization to supplement systems and reporting. The data elements are typically stored within a master data management (MDM) solution."
- "Internal teams must often follow rules of engagement when they request access to the primary data. Such rules are documented in the data governance plan and managed by the data steward."

Where "source of truth" *does* appear in the IG, it is used casually about an **environment**, not a data domain (S3, verbatim, on the golden configuration environment): "Use it as a source of truth for your configurations and restore it to other environments as needed."

The master-data reference architecture (S8) uses a third phrasing again — "master data source" (verbatim): "Use this solution when Dataverse either directly or through a Dynamics 365 app is the master data source for some of the data (such as products, accounts, contacts, and addresses)."

**Why it matters**: this is the finding that justifies the pack defining its own vocabulary. Microsoft uses at least four labels for near-identical concepts — *primary data*, *master data source*, *source of truth*, *record keeper* — with no cross-reference and no definition. Any pack that treats "system of record" as a Microsoft term is inventing an authority that does not exist.

**Decision impact**: data requirement → *unambiguous ownership language across lenses* → constraint → *the pack must define its own terms and state they are pack-local, not Microsoft-normative* → architectural implication → *no lens may cite Microsoft as the authority for a system-of-record definition; cite "primary data" / "master data source" instead and flag the mapping explicitly*.

**Conditions**: negative finding — absence of evidence within the pages fetched (S1, S2, S3, S8). Broader Learn surfaces (Purview, Fabric, Azure Architecture Center) were not exhaustively swept; see Unknowns U-01.
**Confidence**: Medium-High for the D365 IG; Medium as a Learn-wide claim.
**Sources**: S1, S3, S8.

---

#### DQ-04 — Data quality is a governance pillar with a named human gatekeeper, and the validation gap is the documented failure mode

**Classification**: Data quality / process
**Origin**: MS (T1)

**Evidence** (S1, verbatim)
- "Data quality is at the forefront of data governance policies. It should be thought of as high quality and fit for the intended use."
- "The users who are most familiar with their data should be the gatekeepers for cleansing, including standardization and adherence to the policies outlined by the data steward."
- The retailer worked example: "The company found that online customers who buy as guests could enter any value in the email field with no validation. This discovery led data stewards and LOB process owners to set up new validation processes."
- "They were challenged to define 'good' data to satisfy the use case."
- "With artificial intelligence (AI) and machine learning (ML) becoming more prominent in most digital transformation projects, and the fact that their success depends on data quality, it's wise to take data governance seriously."

From the checklist (S2, verbatim):
- "Assess your data quality realistically and estimate the efforts required to perform the cleanup."
- "Ensure that the apps have the validations and controls to enforce data quality and that you have processes to measure and report on it."
- "Maintain high-quality data by following the principles in this article and by having leadership drive the habit of managing data on an ongoing basis."

**Why it matters**: three separable claims. (a) Quality is *fitness for the intended use* — so it is undefinable without the use case, which makes it a Discovery question, not a build question. (b) The **cleansing gatekeeper is the business user closest to the data**, not IT and not the platform. (c) Microsoft's own worked example of a quality failure is precisely *a field with no validation* — which makes "which store can enforce this rule?" the operative architectural question (see DQ-05..DQ-08).

**Note on quality dimensions**: the IG names "accuracy and completeness" ("It's often dedicated teams that drive data accuracy and completeness across the organization") and, in the governance definition, "availability, usability, quality, and security"; the checklist adds "availability, usability, integrity, security, and compliance". Microsoft does **not** publish a canonical numbered dimension list (e.g. the DAMA six) in this chapter. See U-02.

**Decision impact**: data requirement → *"good data" must be defined per use case before build* → constraint → *a named business gatekeeper per data domain owns cleansing; the estimate must carry a cleanup effort line* → architectural implication → *validation must be placed where it is actually enforceable, and any store that cannot enforce it converts the rule into recurring human effort*.

**Conditions**: content dated 2024-01-08, AI-assisted, 3-year refresh cycle.
**Confidence**: High.
**Sources**: S1, S2.

---

#### DQ-05 — Migration guidance: cleanse in a staging database, verify quality in the target, and migrate only relevant data; migration must not share a window with testing

**Classification**: Migration / data quality
**Origin**: MS (T1)

**Evidence** (S3, verbatim)
- "You need to migrate the data that's relevant and useful for your Dynamics 365 solution."
- "Migration data can be either master data, such as customers, products, and vendors, or open transactions, such as sales orders, purchase orders, stock on hand, and open balances."
- "Verifying and validating the data quality and accuracy in your Dynamics 365 solution." (listed as a required plan item)
- "Don't forget to include environment considerations in your planning, like the size of the import and staging databases needed to migrate and cleanse the data."
- "We recommend that you procure a dedicated high-tier data migration environment that's sized appropriately to handle the volume of data in scope."
- "When you're building a migration plan, keep in mind that data migration activities can be a disruptive task and shouldn't coexist with other testing activities."
- "You should also test and verify your data migration at least once in your system integration testing (SIT) and user acceptance testing (UAT) environments."
- Roles, verbatim: "Data steward | Maintains and manages data according to data properties and standards. Coordinates with stakeholders. Provides definitions and rules for data."
- "Data migration architect/developer | Designs and develops the environments and packages for data migration. Transforms and tests data. Validates and verifies data quality and accuracy."

**On not migrating history**: the IG does **not** state "don't migrate history" as a rule. What it states is the *scope* filter above ("relevant and useful") and the enumerated migration categories — **master data and open transactions**. Closed/historical transactions are conspicuously absent from that enumeration, but this is an inference from an example list, not an explicit prohibition. Do not quote it as a Microsoft rule. See U-03.

**Why it matters**: cleansing has a named *place* (a staging/import database in a dedicated sized environment), not just a named owner. And migration is scheduled as an exclusive activity — it cannot be squeezed into the UAT window.

**Decision impact**: data requirement → *legacy data must reach the target clean* → constraint → *a staging database and a dedicated sized migration environment are line items, and the migration window is exclusive of testing* → architectural implication → *cleansing happens pre-load in the ETL layer, because post-load correction in the target is manual work by the DQ-04 business gatekeeper*.

**Conditions**: D365 F&SCM/CE framing; the environment-tier advice is product-specific, the sequencing advice is general.
**Confidence**: High for quoted items; the history claim is explicitly downgraded to an inference.
**Sources**: S3.

---

#### DQ-06 — Dataverse as master: when it qualifies, and the canonical-model one-way door

**Classification**: Master data / architecture
**Origin**: MS (T1)

**Evidence** (S8, verbatim, ms.date 2025-11-04)
- Applicability test: "Use this solution when Dataverse either directly or through a Dynamics 365 app is the master data source for some of the data (such as products, accounts, contacts, and addresses)."
- "Use this reference architecture when you define Dynamics 365 apps as the master data source for entities such as products, accounts, contacts, and addresses. In this scenario, you need to make this data available in other systems. This architecture supports fast data distribution."
- Ownership of the decision: "The key stakeholders in this solution are the business users because they're responsible for the master data system and the requirements to have this information available in other systems."
- **Canonical-model warning**: "Define your canonical model carefully. When the first listener is 'live', it's hard to change the model (you can add but can't delete or restructure)."
- **Consumer responsibility**: "The retrieving systems are responsible for retrieval and removal from the bus. They can do this work directly or through Azure services like a Logic App or Azure Function."
- Extensibility advice: "Make the function as flexible as possible so you don't need to write code when adding extra data to messages."
- Scope caveat: "Not all implementations with Dynamics 365 apps include Dataverse, so review the list in the ***Applies to*** section."
- Dataflow (verbatim, condensed): "Dataverse maintains the data." → "A trigger publishes on a service bus whenever a create or update takes place." → transform to canonical model via Logic App Data Mapper → "The result publishes to a Service Bus Topic." → "Multiple listeners can retrieve the updates from the Service Bus Topic."

**Why it matters**: three hard consequences. (a) Mastering is scoped **per entity** ("for *some* of the data") — consistent with the already-established per-entity/per-field ownership finding, now confirmed at reference-architecture level. (b) The canonical model is a **one-way door**: additive-only once a listener is live. That is an irreversible design commitment made early, which belongs in the decision record with its counterfactual. (c) The publisher does not guarantee delivery semantics — consumers own retrieval *and removal*, so a broken consumer is the consumer's problem, and back-pressure/poison-message handling is not provided.

**Decision impact**: data requirement → *one authoritative copy of an entity, distributed to N systems* → constraint → *the canonical model must be right before the first consumer goes live; consumers must be built to drain the bus* → architectural implication → *Dataverse-as-master is only viable with a real integration layer (Service Bus + Logic Apps + Functions + Storage), which is a cost and skills commitment well beyond a Power Platform app; the licence covers Dataverse but Azure components are billed separately*.

**Cost note** (S8, verbatim): "The licenses cover the Dataverse and Dynamics costs. For Azure, the following costs apply:" — Application Insights, Azure Key Vault, Storage Account, Azure Service Bus, Azure Function, Logic App (standard).

**Conditions**: applies only where Dataverse is present; a single professional-services origin ("This solution was created for a professional services organization").
**Confidence**: High.
**Sources**: S8.

---

#### DQ-07 — The IG requires the Common Data Model "without deviations" and demands a storage forecast

**Classification**: Data modelling / storage
**Origin**: MS (T1)

**Evidence** (S2, verbatim)
- "Define, document, and update a data model that serves as a blueprint for your solution."
- "Follow the Common Data Model standard without deviations to ensure compatibility and readiness for future updates across applications."
- "Estimate and forecast your data storage needs across different environments and types of data stores in your solution."
- "Store only the necessary data in the app for the key processes that interact with it. Choose the right type of data store based on the usage."

**Why it matters**: "without deviations" is unusually strong for guidance prose, and it directly constrains custom-entity design. The pairing with "store only the necessary data in the app" and "choose the right type of data store based on the usage" is Microsoft explicitly endorsing a **polyglot** answer — not everything belongs in the app's own store.

**Decision impact**: data requirement → *long-lived, upgradeable data model* → constraint → *extend the standard model rather than replace it; forecast storage per environment; keep non-process data out of the app store* → architectural implication → *the "put it all in Dataverse" and the "put it all in a SharePoint list" answers are both contradicted by the same sentence — store choice is per-usage*.

**Conditions**: checklist prose, 2024-01-18.
**Confidence**: High.
**Sources**: S2.

---

#### DQ-08 — Archiving / retention: NOT covered in the current data-management chapter set

**Classification**: Coverage gap (negative finding)
**Origin**: MS (T1)

**Evidence**
The chapter overview (S1) advertises the scope, verbatim: "You'll learn about data governance, architecture, modeling, migration and integration, storage, and quality." Archiving is named once, only as a stakeholder concern (S1, verbatim): "Architects and administrators care about security, licensing, storage costs, archival, and scalability."

The checklist (S2) has sections for **Data governance and architecture, Data modeling, Data storage, Configuration data and data migration, Data integration, Data quality** — and **no archiving, retention, or data-lifecycle section at all**. The single storage task is the forecast quoted in DQ-07.

**Why it matters**: the IG raises archival as something architects care about and then does not tell them what to do. Retention/lifecycle guidance must come from elsewhere (product-specific long-term-retention docs, Purview retention policies), not from the IG. A pack claiming "the D365 IG covers retention" would be wrong.

**Decision impact**: data requirement → *retention and archiving policy* → constraint → *no IG-level guidance exists; the policy is sourced from compliance and product docs* → architectural implication → *retention is an open Unknown at Discovery by default, and the governance lens cannot resolve it by citing the IG*.

**Conditions**: absence of evidence in S1 and S2 as fetched on 2026-09-02.
**Confidence**: High for these two pages; see U-04 for whether a separate lifecycle page exists elsewhere in the IG.
**Sources**: S1, S2.

---

#### DQ-09 — Business rule scope: only "Entity" scope reaches the server; "table as scope" is mandatory for canvas apps

**Classification**: Validation / enforcement boundary
**Origin**: MS (T1)

**Evidence** (S4, `data-platform-create-business-rule`, ms.date 2026-07-06 — the freshest source in this file)

Scope table, **verbatim**:

| If you select this item... | The scope is set to... |
|---|---|
| **Entity** | Model-driven app forms and server |
| **All Forms** | Model-driven app forms |
| Specific form (**Account** form, for example) | Just that model-driven app form |

- "If you're building a Canvas app, you must use table as the scope."
- "Business rules defined for a table apply to both *canvas apps* and *model-driven apps* if the table is used in the app. Not all business rule actions are available on canvas apps at this time."
- Capabilities, verbatim: "Set column values" / "Clear column values" / "Set default values" / "Validate data and show error messages"
- **Form-scope-only actions**, verbatim: "The following actions only apply to form scope business rules." — "Set column requirement levels" / "Show or hide columns" / "Enable or disable columns" / "Create business recommendations based on business intelligence."
- **Not available on canvas apps**, verbatim: "Show or hide columns" / "Enable or disable columns" / "Create business recommendations based on business intelligence"

**Why it matters**: this is the precise boundary. Only **Entity/table scope** is described as reaching "server". Everything richer — requirement levels, show/hide, enable/disable, recommendations — is **form-scope only**, i.e. model-driven UI only, i.e. bypassable by any other client. The genuinely cross-client subset of business rules is narrow: set value, clear value, set default, validate-and-error.

Note the answer to the "required field levels" question: **dynamic requirement levels are form-scope only**. A business rule cannot make a field required in a way that a canvas app or an API caller will respect.

**Decision impact**: data requirement → *a rule must hold no matter which app writes* → constraint → *only table-scoped business rules qualify, and only the four cross-client actions are available* → architectural implication → *conditional requiredness and conditional field visibility are UI affordances, not data-integrity controls; a rule expressed that way must be re-expressed as a table-scoped validation, or as a column-level requirement level on the table itself, if it actually matters*.

**Conditions**: as documented 2026-07-06.
**Confidence**: High.
**Sources**: S4.

---

#### DQ-10 — CONTRADICTION IN MICROSOFT'S OWN DOC: the same page says Entity scope runs "and server" and that business rules "aren't executed inside Dataverse"

**Classification**: Evidence conflict — do NOT resolve from docs alone
**Origin**: MS (T1), both sides

**Evidence** (S4, both statements on the same page, same ms.date 2026-07-06)

Side A — scope table, verbatim: "**Entity** | Model-driven app forms **and server**"

Side A supporting, verbatim (from the 150-rule performance note): "This limit includes both client side (JavaScript) **and server side (XAML generated as synchronous plugins)** business rules."

Side B — FAQ, verbatim: "*When I update a business rule, is it executed against all existing records?*" — "No. **Business rules are run on clients.** For example, they run when a form is opened by a user and when a field value changes on that open form. **They aren't executed inside Dataverse.**"

**Reading**: the FAQ answer is scoped to a narrow question (does a rule change retro-apply to existing rows?) and its "run on clients" phrasing over-generalises. The scope table and the "server side (XAML generated as synchronous plugins)" note are the more specific, mechanism-level statements, and they point to entity-scoped rules being compiled to **synchronous plugins** — which do execute server-side on the write pipeline, and therefore on API writes. But Microsoft never says that in one place, and the FAQ flatly contradicts it.

**Why it matters**: the previously-established claim that business rules validate "regardless of the app used to create the data" rests entirely on this. It is **defensible but not cleanly evidenced** — the same page can be quoted against it. A pack asserting server-side enforcement as settled fact is overstating what Microsoft documents.

**Second, independent load-bearing fact regardless of how the conflict resolves**: rules are **not retroactive**. Activating a rule does nothing to existing rows. A new validation rule never cleans legacy data — that remains the DQ-04 / DQ-05 human cleansing job.

**Decision impact**: data requirement → *guaranteed enforcement on every write path* → constraint → *business rules are documented ambiguously at exactly the point that matters; treat "enforced on API writes" as **Assumed**, not Confirmed, until tested in the target environment* → architectural implication → *where the guarantee is genuinely required (financial, regulatory, safety), use an explicit synchronous plugin or a column/key-level constraint rather than relying on a business rule; and never assume rule activation repairs history*.

**Conditions**: this belongs in the SU as an Assumed row with a named validation test — activate a table-scoped validate-and-error rule, attempt a violating create via Web API, observe.
**Confidence**: Medium (the conflict itself is High confidence; the resolution is not).
**Sources**: S4.

---

#### DQ-11 — Business rules have hard capability and scale limits: unsupported column types, unsupported grid controls, silent no-ops, and a 150-rule ceiling

**Classification**: Validation / platform limits
**Origin**: MS (T1)

**Evidence** (S4, verbatim)
- Unsupported types: "business rules don't work with the following column types:" — "Choices (multi-select)" / "File" / "Language". Supported: "Business rules work with most column types including text, number, choice, date, lookup, owner, and image."
- Grid gaps: "In a model-driven app, not all business rule actions are available for editable grids. For table based view pages, recommendations can't be created. **Editable subgrids don't support business rules. Business rules won't work with other types of dataset controls.**"
- Scale ceiling: "Power Platform today supports up to 150 business rules for a single table. Beyond 150 business rules, performance degradation can be experienced. This limit includes both client side (JavaScript) and server side (XAML generated as synchronous plugins) business rules. To avoid performance issues with Dataverse, we recommend that you don't create more than 150 business rules for a single table."
- **Silent-failure mode**: "A business rule might not execute because the field referenced in the business rule isn't included with the form."
- Ordering: "*Do business rules react to changes made by an onLoad script?*" — "No, they'll execute before an onload script is executed."
- Timezone trap: "When you configure business rules with `DateOnly` columns, the dates are in the UTC time zone by default, irrespective of the user's set time zone. This can lead to unexpected results if you're expecting `DateOnly` values to align with local time settings."
- Composite attributes: "Actions or conditions that use Composite attributes aren't supported in apps based on the Unified Interface."
- Maker friction: "If you want to modify an existing business rule, you must deactivate it before you can modify it."

**Why it matters**: three independently disqualifying facts. (a) **Multi-select choice columns — extremely common on real forms — cannot be validated by business rules at all.** (b) A form-scoped rule **silently does nothing** if the referenced field isn't on the form: the failure is invisible, not an error, so the rule appears configured and isn't running. (c) 150 is a real ceiling that a rules-heavy core table can approach, and it counts client and server rules together.

**Decision impact**: data requirement → *validate a multi-select field, or validate inside an editable grid* → constraint → *business rules cannot do it, at any scope* → architectural implication → *low-code validation has a hard capability edge; crossing it means a plugin (pro-code, ALM overhead, different skills) or accepting the rule as unenforced — and that fork must be identified in Discovery, because it changes the cost and staffing profile of the whole build*.

**Conditions**: "today" per the 2026-07-06 doc.
**Confidence**: High.
**Sources**: S4.

---

#### DQ-12 — Duplicate detection is OFF BY DEFAULT on the Web API: integrations create duplicates unless a header explicitly opts in

**Classification**: Validation / integration path — HIGH IMPACT
**Origin**: MS (T1)

**Evidence** (S5, `manage-duplicate-detection-create-update`, ms.date 2022-12-31, verbatim)
- Header semantics: "The value assigned to `MSCRM.SuppressDuplicateDetection` header determines whether the Create or Update operation can be completed:" — "`true` – Create or update the record, if a duplicate is found." / "`false` – Do not create or update the record, if a duplicate is found."
- Required opt-in on create: "Use preference header `MSCRM.SuppressDuplicateDetection` and set its value to `false` in the Web API request."
- **Explicit default on update**: "Set the value of `MSCRM.SuppressDuplicateDetection` header to `false` in your `PATCH` request to avoid creation of a duplicate record during Update operation. **By default, duplicate detection is suppressed when you are updating records using the Web API.**"
- Prerequisite rules: "Make sure there are appropriate duplicate detection rules in place. **Dataverse includes default duplicate detection rules for accounts, contacts, and leads, but not for other types of records.** If you want the system to detect duplicates for other record types, you'll need to create a new rule."
- Failure shape when it does fire: `HTTP/1.1 500 Internal Server Error`; `"code": "0x80040333"`; `"message": "A record was not created or updated because a duplicate of the current record already exists."`

**Why it matters**: this is the most consequential finding in the file for integration design. Duplicate detection is an **interactive-UI safety net that integrations opt out of by default**. Every Power Automate flow, Azure Function, ETL load and dataflow write that does not set the header will create duplicates that the UI would have blocked. Combined with the already-established fact that duplicate detection is *advisory* even in the UI, duplicate rules protect close to nothing on the paths that generate the most volume — which is exactly the migration and integration traffic of DQ-05.

**Precision note (do not over-quote)**: the page states the default suppression explicitly only for **Update**. For **Create** it instructs setting the header to `false`, which implies the same default but is not stated as such in this page's prose. The Create default is an inference. See U-05.

**Failure-semantics note**: a fired rule returns **HTTP 500**, not a 4xx. Naive integration error handling that retries on 5xx will loop; handlers that branch only on 400-class validation errors will misclassify a business rejection as a transient fault.

**Decision impact**: data requirement → *no duplicate customers/products regardless of entry path* → constraint → *duplicate detection does NOT cover API or integration writes unless every caller sets `MSCRM.SuppressDuplicateDetection: false`, and no rules exist at all outside accounts, contacts and leads* → architectural implication → *uniqueness that actually matters must be enforced by an **alternate key** — a real server-side constraint on all paths — not by duplicate detection; duplicate detection is a UX assist for human entry only, and integration error handling must treat `0x80040333` / HTTP 500 as a business rejection, never a retry*.

**Conditions**: Web API; ms.date 2022-12-31 — the oldest source in this file, re-verify. The SDK / Organization Service has an equivalent parameter documented separately (`detect-duplicate-data`, not fetched — see U-05).
**Confidence**: High for the Update default, the header semantics, the default-rules scope and the error shape; Medium-High for the Create default.
**Sources**: S5.

---

#### DQ-13 — Validation-per-store: the enforcement ladder, and where it actually breaks

**Classification**: Comparative / architecture
**Origin**: MS (T1), synthesised

**Evidence**

**Dataverse** — several tiers, only some server-side:
- Table-scoped business rules: "**Entity** | Model-driven app forms and server" (S4); implemented at least partly as "server side (XAML generated as synchronous plugins)" (S4) — but see the DQ-10 contradiction.
- Form-scoped rules: model-driven UI only (S4).
- Alternate keys: real uniqueness constraint, all paths (established in prior pass).
- Duplicate detection: advisory, and **off by default on API** (S5, DQ-12).

**SharePoint** — validation exists as a setting, but is thin:
- List-level, verbatim (S7): "Specify a formula to use for validation. Create a message that helps users understand what valid data looks like."
- Column-level, verbatim (S6): "To add column validation, select **Column Validation** to expand the section, and enter the **Formula** that you want to use to validate the data. You should also add a **User message** that describes what valid data should look like to help users enter valid data."
- Availability caveat, verbatim (S6): "The **Column Validation** section is not available for all types of columns."
- Column constraints available, verbatim (S7): "edit the properties, such as **required data, unique values, and maximum characters** for a text field".
- **Row-locality limit**, verbatim (S9, on calculated fields — the same formula engine): "Calculated fields can only operate on their own row, so you can't reference a value in another row, or columns contained in another list or library."

**Excel** — Excel has Data Validation as a workbook authoring feature, but it is not a store guarantee. An Excel file consumed as a data source carries no constraint any consumer must honour, and no Microsoft documentation establishes enforcement for Excel-as-data-source. Treated as **no server-side validation**.

**Why it matters**: the ladder is real but shorter than usually claimed. SharePoint validation is evaluated **per row on write**, cannot reference other rows or other lists, and is expressly unavailable on some column types. That rules out every referential rule ("this code must exist in the reference list"), every uniqueness rule beyond the single per-column "unique values" setting, and every cross-record rule ("no overlapping bookings", "sum of lines equals header").

The honest form of the claim "server-enforced rules exist only in Dataverse" is narrower: **SharePoint enforces single-row, single-column validation on write; only Dataverse offers cross-column server rules, relational integrity and multi-column uniqueness keys; neither offers declarative cross-row validation.**

**Decision impact**: data requirement → *enforce rule R on all write paths* → constraint → *classify R first — single-row field-level → any of the three stores; single-column uniqueness → Dataverse alternate key or SharePoint unique-values; multi-column uniqueness or referential → Dataverse only; cross-row or cross-entity aggregate → **no declarative option in any store**, requires code* → architectural implication → *store choice is driven by the hardest rule in the set, not the average one; and the presence of a single cross-row rule silently converts a low-code project into a pro-code one regardless of which store is chosen*.

**Conditions**: SharePoint validation semantics are documented on support.microsoft.com — consumer-grade pages with no `ms.date` — which is materially weaker evidence than Learn. The row-locality quote is from the calculated-fields page and is applied here to the validation formula engine by inference; see U-06.
**Confidence**: High for Dataverse; Medium-High for SharePoint; Medium for Excel (negative finding).
**Sources**: S4, S5, S6, S7, S9.

---

#### DQ-14 — SharePoint-origin data carries Microsoft-documented type defects that break downstream analytics and leak classification

**Classification**: Data quality defect / documented
**Origin**: MS (T1)

**Evidence**

Power Query SharePoint list connector (S10, ms.date 2025-11-21), under a section literally titled **"Inconsistent behavior around boolean data"**, verbatim:
- "When you use the SharePoint list connector, Boolean values are represented inconsistently as TRUE/FALSE or 1/0 in Power BI Desktop and Power BI service environments. **This inconsistency might result in wrong data, incorrect filters, and empty visuals.**"
- "This issue only happens when the **Data Type** isn't explicitly set for a column in the Query View of Power BI Desktop. You can tell that the data type isn't set by seeing the 'ABC 123' image on the column and 'Any' data type in the ribbon."
- "The user can force the interpretation to be consistent by explicitly setting the data type for the column through the Power Query editor."
- OData path limit, verbatim: "If you use an OData feed to access a SharePoint List, there's an approximately 2100 character limitation to the URL you use to connect."

Create a semantic model from a SharePoint List (S11, ms.date 2023-02-22), **Considerations and limitations**, verbatim:
- "**The semantic model won't be created if the SharePoint list contains values with more than four digits after a decimal place ('.')**"
- "The sensitivity label (if any) of the SharePoint list isn't inherited by the semantic model that is created."
- "This flow does not support business-to-business (B2B) scenarios or scenarios where authentication takes place against a service principal."

Also load-bearing on ownership (S11, verbatim): "The Power BI view of the SharePoint list data is determined by the permissions of the account used to establish the Power BI connection to the SharePoint data source (that is, the SharePoint site)." And: "since the connection now uses your current login credentials, views of the data in semantic models you might have created previously from that SharePoint site might also change, and this could affect reports and other downstream items that users might have created based on those semantic models".

**Why it matters**: these are Microsoft-documented defects, not folklore. Four distinct classes:
1. **Silent wrongness** — the Boolean case produces "wrong data, incorrect filters, and empty visuals" with no error. The report looks fine and is wrong. The mitigation exists but is manual and per-column, so it is a recurring discipline, not a one-time fix.
2. **Hard blocking** — five decimal places blocks semantic model creation outright on the quick path.
3. **Governance leakage** — the **sensitivity label is not inherited**. Classified data in a SharePoint list becomes an unclassified semantic model. That is a governance regression caused purely by the choice of store plus the choice of the quick export path.
4. **Identity smearing** — what a report shows depends on *whose credentials created the connection*, and re-authenticating can retroactively change what other people's existing reports show.

**Decision impact**: data requirement → *trustworthy reporting over the operational store, with classification preserved* → constraint → *SharePoint-as-store imposes explicit per-column typing discipline, a four-decimal ceiling on the quick path, loss of sensitivity labels downstream, and connection-identity-dependent report content* → architectural implication → *where the solution has real BI or any classified data, SharePoint-as-store costs more in downstream remediation than it saves at build time; and "who owns the data" acquires a second, undocumented answer — the identity behind the connection — that no governance artefact captures*.

**Conditions**: the Boolean issue is Power BI Desktop/service specific and is mitigable; the decimal limit applies to the "Export to Power BI" quick path, not to Power BI Desktop modelling.
**Confidence**: High.
**Sources**: S10, S11.

---

#### DQ-15 — Microsoft DOES define both terms — but in Azure Architecture Center, not in the D365/Power Platform guidance, and only as microservices patterns

**Classification**: Vocabulary — the definitive answer to question 2
**Origin**: MS (T1)

**Evidence** (S12, "Data Considerations for Microservices", Azure Architecture Center, ms.date 2022-07-26)

**"Source of truth" — the closest thing to a Microsoft definition**, verbatim:
- "**Use a single source of truth when you require strong consistency.** One service might represent the source of truth for a given entity and expose it through an API. Other services might hold their own copy of the data, or a subset of the data, that's eventually consistent with the primary data but **not considered the source of truth**."
- Worked example, verbatim: "For example, in an e-commerce system that has a customer order service and a recommendation service, the recommendation service might listen to events from the order service. But if a customer requests a refund, the order service, not the recommendation service, has the complete transaction history."

**"System of record" — used, never defined**, verbatim: "The information stored in Azure Managed Redis is short-lived. After a delivery finishes, **the delivery history service becomes the system of record**."

Supporting principles, verbatim:
- "Two services shouldn't share a data store. Each service manages its own private data store, and other services can't access it directly."
- "Traditional data modeling follows the rule of *one fact in one place*. Every entity appears exactly once in the schema. Other entities might reference it but not duplicate it."
- "**Store only the data that a service needs.** A service might only need a subset of information about a domain entity. For example, in the shipping bounded context, you need to know which customer is associated with a specific delivery. But you don't need the customer's billing address because the accounts bounded context manages that information."
- "**Define the required consistency level for each component, and prefer eventual consistency where possible.** Identify areas in the system where you need strong consistency or atomicity, consistency, isolation, and durability (ACID) transactions. And identify areas where eventual consistency is acceptable."

**Why it matters — this is the answer to question 2**:
1. Microsoft's **only** near-definition of "source of truth" is **per entity, tied to strong consistency, and expressed as: the one service that owns the entity and exposes it via API, while every other holder has an eventually-consistent copy that is explicitly NOT the source of truth.** That is a genuinely usable definition and it directly corroborates the already-established per-entity ownership finding — now from a completely independent Microsoft surface.
2. **"System of record" is used but never defined.** In S12 it appears once, describing a *handover*: Redis holds the delivery while in flight; after completion, the history service "becomes the system of record". So Microsoft's implicit usage is **lifecycle-stage-dependent** — the system of record for an entity can *change over the entity's life*.
3. The two terms are **not distinguished anywhere**. Microsoft uses "source of truth", "system of record", "primary data", "master data source" and "authoritative" interchangeably across surfaces, with no cross-reference. **The terms are used loosely.** Any pack that asserts a formal Microsoft distinction between them is inventing it.
4. "Store only the data that a service needs" plus the billing-address example is the same per-field ownership logic as the established Sales-owns-name / Finance-owns-credit-limit finding — arrived at independently, from bounded-context reasoning.

**Decision impact**: data requirement → *name the authoritative holder for each entity* → constraint → *"source of truth" is definable only alongside a consistency requirement; if eventual consistency is acceptable, the question "who is the source of truth" may not need a hard answer at all, and copies are legitimate* → architectural implication → *the ownership question must be asked as two questions, not one: (a) which system owns this entity, and (b) does this consumer need strong consistency? Only (a)+(b) together forces a synchronous, single-writer design; (a) alone permits replicated read copies. And ownership may legitimately hand over between systems at a lifecycle boundary.*

**Conditions**: microservices context; ms.date 2022-07-26, `ms.update-cycle: 1095-days`. Generalising it to a Power Platform engagement is an analogy, not a citation.
**Confidence**: High for the quotes; High for the "used loosely / no formal distinction" conclusion.
**Sources**: S12, plus the negative evidence in DQ-03 (S1, S3, S8).

---

#### DQ-16 — Purview over Dataverse is shallow: metadata only, no incremental scan, deletions never propagate, and unavailable in sovereign clouds

**Classification**: Governance tooling limits
**Origin**: MS (T1)

**Evidence** (S13, "Connect to and manage Microsoft Dataverse in Microsoft Purview", ms.date 2026-02-02 — recent)

Scanning capabilities table, **verbatim**:

| Metadata Extraction | Full Scan | Incremental Scan | Scoped Scan |
|---|---|---|---|
| Yes | Yes | **No** | Yes |

- Extraction scope, verbatim: "When scanning Dataverse source, Microsoft Purview supports extracting technical metadata including:" — "Environment" / "Tables, including columns". **That is the entire list.**
- Scoping, verbatim: "When setting up a scan, you can choose to scope the scan by selecting tables as needed."
- Deferred capabilities, verbatim: "For **classifications**, **sensitivity labels**, **policies**, **data lineage**, and **live view**, see the [list of supported capabilities]." — i.e. the Dataverse page itself asserts **none** of these; it points elsewhere.
- **Known limitations**, verbatim: "When object is deleted from the data source, currently the subsequent scan won't automatically remove the corresponding asset in Microsoft Purview." and "Dataverse integration with Microsoft Purview Data Map isn't available in sovereign clouds."
- Access model, verbatim: the scanning identity must be created as an application user and assigned "the security role **Service Reader**".

**Why it matters**: four consequences for "who owns the data".
1. **Metadata only, at environment/table/column granularity.** Purview tells you a table exists and what columns it has. It does not tell you who owns it, who stewards it, or whether the data in it is any good. The DQ-02 ownership map is **not** a Purview output — it is a human artefact Purview cannot produce.
2. **No incremental scan** means every refresh is a full scan. In a large environment that is a cost and scheduling constraint, and it caps how fresh the catalogue can realistically be.
3. **Deletions never propagate.** The catalogue monotonically accumulates. Over time it drifts into describing tables that no longer exist — a catalogue that is confidently wrong, which is worse for governance than no catalogue.
4. **Sovereign cloud exclusion** removes the option entirely for regulated/sovereign deployments — precisely the tenants with the strongest governance obligations.

**On SharePoint/SQL differing**: the Dataverse page defers classification/label/policy/lineage support to a shared capability matrix rather than asserting it, which is itself the signal — Dataverse is not a first-class Purview source in the way Azure SQL is. The comparative matrix was not fetched; see U-07.

**Decision impact**: data requirement → *a governed, discoverable, ownership-attributed data estate* → constraint → *Purview over Dataverse provides table/column inventory only, staleness-on-delete, full-scan-only refresh, and nothing in sovereign clouds* → architectural implication → *ownership and stewardship must be maintained as a first-class human-curated artefact in the engagement, not delegated to a tool; "we'll catalogue it in Purview" does not answer the ownership question, and budgeting Purview as the governance answer is a category error*.

**Conditions**: classic Purview governance portal / Data Map; ms.date 2026-02-02.
**Confidence**: High.
**Sources**: S13.

---

#### DQ-17 — Alternate keys are the only uniqueness mechanism that also enables upsert, which makes them the migration-idempotency mechanism too

**Classification**: Validation / migration — synthesis
**Origin**: MS (T1) + established prior findings

**Evidence** (synthesis; the individual facts are established or quoted above)
- Alternate keys enforce uniqueness at ≤10 per table and are a real server-side constraint on all write paths (established prior pass).
- Duplicate detection does **not** cover API writes by default and has no default rules outside accounts/contacts/leads (S5, DQ-12).
- Migration explicitly requires repeatability: "You should also test and verify your data migration at least once in your system integration testing (SIT) and user acceptance testing (UAT) environments" (S3) — i.e. the same load runs at least three times across SIT, UAT and cutover.

**Why it matters**: the migration of DQ-05 is run repeatedly by design. Without a natural-key-based upsert, each rehearsal either duplicates everything or requires a manual wipe. Duplicate detection cannot prevent this (DQ-12: off by default on the API path that ETL uses, and absent entirely for custom tables). The alternate key is therefore doing double duty — it is simultaneously the **only** uniqueness guarantee that survives integration writes *and* the enabler of idempotent reloads.

The ≤10-per-table ceiling is consequently tighter than it looks: keys are consumed by both integrity requirements and migration/integration addressing needs, competing for the same budget.

**Decision impact**: data requirement → *repeatable migration rehearsals + guaranteed uniqueness on all paths* → constraint → *each migrated table needs an alternate key on its legacy natural key, drawn from the same ≤10 budget as business uniqueness keys* → architectural implication → *alternate-key design is a Discovery-time question, not a build-time one: it needs the legacy natural key, which needs the legacy system's own uniqueness semantics — and if the legacy source has no reliable natural key (typical of Excel-origin data), a surrogate must be manufactured and back-written to the source before the first rehearsal, which is unbudgeted work*.

**Conditions**: partly synthesis across sources rather than a single quoted Microsoft statement. The upsert/alternate-key linkage is established Dataverse behaviour but was not re-fetched verbatim in this pass; see U-08.
**Confidence**: Medium-High (components are High; the synthesis is mine).
**Sources**: S3, S5, prior-pass alternate-key findings.

---

#### DQ-18 — The composite picture: Microsoft's guidance assumes governance maturity the low-code entry point does not require

**Classification**: Cross-cutting synthesis
**Origin**: MS (T1) synthesis

**Evidence** (all quoted above; assembled)
- The IG requires, before build: a data steward appointed (S2), a data architecture with named owners (S2), use cases defining "good" data (S1), a realistic quality assessment with cleanup effort estimated (S2), a migration strategy with a dedicated sized environment (S3), and a data model following "the Common Data Model standard without deviations" (S2).
- Meanwhile the platform's actual enforcement surface is: narrow (DQ-09), ambiguously documented at the critical point (DQ-10), capability-limited (DQ-11), off-by-default on integration paths (DQ-12), and thinner still outside Dataverse (DQ-13).
- And the governance tooling that would police it is metadata-only and staleness-prone (DQ-16).
- Meanwhile SharePoint/Excel-origin data arrives with documented type defects that fail silently (DQ-14).

**Why it matters**: the gap is structural, not incidental. Microsoft's *guidance* is enterprise-MDM-shaped — stewards, canonical models, governance plans, dedicated migration environments. Microsoft's *low-code product surface* lets a citizen developer stand up a SharePoint list in ten minutes with none of it. The IG's own worked example of a data quality failure is literally "any value in the email field with no validation" (S1) — a failure of exactly the kind the fast path produces.

Nothing in the platform forces the guidance. Every control in the IG checklist is a human commitment. This is the concrete content of the established finding that data quality "is still typically a human responsibility": not that tools are weak, but that the tools are **optional and default-off**, while the guidance assumes they are in place.

**Decision impact**: data requirement → *a solution whose data stays trustworthy after go-live* → constraint → *no combination of platform features delivers this; the gap is closed by named humans (steward, LOB gatekeeper) and by explicit design decisions (alternate keys, table-scoped rules, typed columns, header-setting integrations)* → architectural implication → *the estimate must carry a line for ongoing data stewardship, and the Discovery exit gate must record: owner per entity, steward appointed, "good data" defined per use case, hardest validation rule classified against DQ-13's ladder, and cleanup effort assessed. A build that skips these does not fail at go-live — it degrades over 12-18 months, which is why it is a tripwire candidate rather than a risk.*

**Conditions**: synthesis; the causal claim about degradation timing is judgement, not documented.
**Confidence**: High for the components; Medium for the synthesis as stated.
**Sources**: S1, S2, S3, S4, S5, S10, S11, S13.

---

---

## 5. Anti-patterns

| Id | Anti-pattern | Why it fails | Origin | Findings |
|---|---|---|---|---|
| DAP-1 | SharePoint list or Excel as relational system of record to avoid premium licences | 5,000 LVT, 12 joins, narrow delegation (silent partial results), ≤ 5,000 unique scopes, no column security, no transactions, last writer wins, outside solutions | MS + T3 | DA-39..DA-44, DA-61 |
| DAP-2 | Excel with more than one writer | "Simultaneous file modifications … are not supported"; 6-min lock; duplicate inserts on retry | MS | DA-41 |
| DAP-3 | Dataverse as the reporting warehouse / analytics on the operational store | 50k aggregate cap, 5-min timeouts, TDS service protection; "use a dedicated datastore for reporting purposes instead" | MS | DA-03, DA-21, DA-51 |
| DAP-4 | Replicating the whole ERP (or closed history) into Dataverse | Capacity cost on the database meter, service protection, "Too much data synchronized … overloads the database"; migrate master + open transactions only | MS | DA-51, DA-54, DA-62 |
| DAP-5 | Two-way sync without a per-field ownership map | "Tricky conflict resolution. Data gets copied for each system"; product-grade tooling exists only for D365 F&O | MS | DA-48 |
| DAP-6 | Nightly bulk loads as the integration pattern | Per-identity 5-min service protection windows; "move towards real-time integration"; bulk APIs fail-all | MS | DA-10, DA-51 |
| DAP-7 | Synchronous webhook / plug-in call to an external system for side effects | "the data operation rolls back but the request sent to the configured endpoint can't be recalled" | MS | DA-50 |
| DAP-8 | Sequential `Patch`/connector writes treated as a transaction | Power Fx is never atomic; partial failure leaves orphans | MS | DA-07 |
| DAP-9 | Virtual tables for data that needs audit, row security, search, offline, rollups or analytics | All forfeited by design | MS | DA-45 |
| DAP-10 | Per-record sharing as the default access model; parental relationships everywhere | POA growth on the database meter and the access hot path; sharing "less performant", "exception" | MS | DA-11 |
| DAP-11 | Organization-owned tables for data that may ever need segmentation | Ownership type immutable → rebuild + migration | MS | DA-12 |
| DAP-12 | BUs mapped 1:1 to a volatile org chart | Re-org = role loss, cascaded ownership moves, fail-stop reassignment | MS | DA-12 |
| DAP-13 | "Audit everything, forever" without scoping | Unbounded log-meter growth; retention non-retroactive; CMK removes the setting | MS | DA-16 |
| DAP-14 | Backups or recycle bin as archive / legal hold | ≤ 28 days, same region, not downloadable; bin ≤ 30 days | MS | DA-18 |
| DAP-15 | Long-term retention as a file-cost remedy | Zero saving on file/image attachments; irreversible | MS | DA-17 |
| DAP-16 | Fabric link with default "all change-tracked tables" and no capacity budget | Replica bills as Dataverse database storage; "can double or triple your storage footprint" | MS + T4 | DA-19 |
| DAP-17 | Embedding Power BI and assuming app security follows | "security roles and privileges don't affect the data that is displayed" | MS | DA-22 |
| DAP-18 | Implicitly shared SQL connections; Windows auth via gateway as a security model | Maker credentials for every user; "isn't secure"; app filters "never override" store permissions | MS | DA-33 |
| DAP-19 | Per-row flow loops against SQL; long-running SPs on the canvas path | 100 CRUD calls / 10 s per connection; 110-s timeout | MS | DA-32 |
| DAP-20 | Reusing a legacy SQL schema unaudited | Triggers break writes; missing PKs read-only; unsupported types; identifier rules | MS | DA-30 |
| DAP-21 | Single gateway node for a business-critical on-prem path | SPOF; primary-first routing; "Microsoft doesn't investigate poor performance when a gateway … is overloaded" | MS | DA-35 |
| DAP-22 | Collections / OnStart as the data layer | 500/2,000-row truncation; "turning everything into collections" named by Microsoft | MS | DA-02, DA-54 |
| DAP-23 | Caching volatile or sensitive values (price, credit limit, balances) | Cache-Aside "doesn't guarantee consistency"; "Always retrieve this type of data from the primary source" | MS | DA-54 |
| DAP-24 | Choice columns for ERP-owned value lists | Metadata change per value; cannot be sourced from the master (INF) | INF | DA-53 |
| DAP-25 | Elastic tables for transactional or relational entities | No multi-record transactions, joins, N:N, rollups, sharing | MS | DA-09 |
| DAP-26 | Leading-wildcard `contains`, filters on formula columns, sorts by choice/related columns in grids | Platform-enforced throttling | MS | DA-26 |
| DAP-27 | Sensitive semantics in table/column/app names; preview features in regulated production | Names replicate globally; previews default to US | MS | DA-58 |
| DAP-28 | Fixed-interval or cascading retries across flow + connector + Dataverse | Load multiplication during the dependency's outage | MS | DA-52 |
| DAP-29 | Append-only lake mode where GDPR erasure applies | Deletes do not propagate | MS | DA-60 |
| DAP-30 *(new v2)* | Assuming a Dataverse→Azure SQL replication service exists ("Microsoft syncs it for you") | No first-party managed path; Dataverse is absent from the Fabric Mirroring source list; every writable-SQL copy is customer-built | MS | SY-01, SY-18 |
| DAP-31 *(new v2)* | Trusting row counts to detect replica drift on Synapse Link / Fabric link | ≥8 documented silent-divergence modes (secured columns null, calculated columns frozen, direct-SQL deletes never propagate) all report sync success | MS | SY-14 |
| DAP-32 *(new v2)* | Snapshot payloads in outbound sync messages (send the row, not the id) | Replays/retries overwrite newer data with stale values; Microsoft's own pattern re-fetches current state at send time | MS | SY-10 |
| DAP-33 *(new v2)* | Treating Power Automate run-resubmission as the reconciliation strategy | 20 runs/batch, capped by connector API limits, no duplicate protection; not a diff/repair mechanism | MS | SY-12, SY-18 |
| DAP-34 *(new v2)* | Virtual tables as a general integration layer for large or write-required external data | No performance/latency/throughput/pushdown documentation exists at any volume; absent from the canvas delegable-data-source list; column selection ignored | MS | VT-09, VT-05, VT-10, VT-17 |
| DAP-35 *(new v2)* | Exposing a "does not contain"/negative-filter search box over a virtual table | Negative operators corrupt paging beyond page 1, "no supported workaround" | MS | VT-04 |
| DAP-36 *(new v2)* | Choosing Azure SQL for high-ingest telemetry/events "because it's SQL and we know SQL" | Microsoft's own data-store model guide routes "high-ingest timestamped metrics and events" to Azure Data Explorer/Eventhouse; SQL's log rate is capped regardless of vCores | MS | SQ2-06, SQ2-07 |
| DAP-37 *(new v2)* | Treating Azure SQL Long-Term Retention as a cheap queryable archive | LTR is backup retention restorable only as a new database; no cold-storage tier for SQL rows; old rows cost the same per GB as new ones | MS | SQ2-04, SQ2-05 |
| DAP-38 *(new v2)* | Relying on `USER_NAME()`-based SQL row-level security behind a shared/implicit Power Platform connection | Collapses to one principal; Microsoft's own reference architecture: shareable SPN means "all users have the same database access rights" | MS | SQ2-08, SQ2-15 |
| DAP-39 *(new v2)* | Assuming duplicate detection protects integration/ETL writes | Suppressed by default on Web API updates; no default rules outside accounts/contacts/leads; failure returns HTTP 500, which naive retry logic loops on | MS | DQ-12 |
| DAP-40 *(new v2)* | Relying on business rules for cross-client (API/integration) enforcement without testing | Microsoft's own docs contradict themselves on whether entity-scoped rules execute server-side; treat as Assumed, never Confirmed, until tested | MS | DQ-09, DQ-10 |
| DAP-41 *(new v2)* | Quoting a concurrent-user ceiling for Dataverse/Power Apps | No such figure is published anywhere; the real constraints are per-user/per-identity limits and row/identity contention | MS | SC-16 |
| DAP-42 *(new v2)* | Assuming a write amplification multiplier (e.g. "1 business transaction = N requests") from memory, a blog, or another engagement | Amplification is a property of each solution's own customisation (plug-ins, workflows, retries, paging), never published by Microsoft, and must be measured per engagement | MS | SC-01, SC-21 |
| DAP-43 *(new v2)* | Citing "SharePoint can't do customer-managed keys" | Microsoft 365 Customer Key explicitly covers SharePoint/OneDrive via a dedicated DEP; the real limitation is tenant/geo granularity, not absence | MS | SQ2-10 |
| DAP-44 *(new v2)* | Building `DateOnly`-based business rules or reports assuming local time zone | Business rules evaluate `DateOnly` columns in UTC by default regardless of the user's time zone | MS | DQ-11 |

---

## 6. Alternatives — when each is preferable (evidence-backed)

- **Dataverse (standard tables) is preferable when:** relational model with integrity and cascades (broadest delegation table of the three connectors — `Not`, `IsBlank`, `In`, `StartsWith`, `Sum/Min/Max/Avg` all delegable — connection-common-data-service, closing review F-07); row/column security per Entra user; field-level audit; offline (mobile players); solution-based ALM; alternate-key idempotency; new app with new storage — Microsoft's own reference architecture states this explicitly: "If you're building a new app and storage, consider using Dataverse" (SQ2-15). Server-enforced business rules "regardless of the app" is **downgraded to Assumed, not Confirmed** in v2 — Microsoft's own business-rules documentation contains an unresolved internal contradiction over whether entity-scoped rules execute on Web API writes (DQ-10); verify empirically before relying on it. (DA-05, DA-07, DA-11, DA-12, DA-16, DA-24, DA-33, DA-37, DA-53, DA-60, DQ-09, DQ-10, SQ2-15).
- **SQL / Azure SQL is preferable when:** the database already exists and "can't be moved" — Microsoft's own canvas-app reference architecture states this as the trigger, not a general performance argument (SQ2-15); complex relational workloads needing joins, indexes, views, stored procedures and engine control; **customer-managed encryption keys** (cheaper and more granular to reach than Dataverse CMK — no Managed-Environment/E5 gate, server/instance/database scoping — SQ2-01, SQ2-09); **datasets beyond Dataverse's practical reach** (Hyperscale scales to 128 TB with autoscaling storage — SQ2-07 — vs no published Dataverse standard-table size envelope, SC-18); region colocation with Azure services; arbitrary-column sub-second filtering on very large tables (no custom indexing in Dataverse, SC-18) — provided the schema passes conformance (DA-30), users are internal via Microsoft Entra Integrated auth (implicit/shared connections collapse row-level security to one principal — SQ2-08) and gateway/VNet costs are accepted. **NOT preferable, contrary to v1, for:** cheap long-term archival (no cold-storage tier exists for Azure SQL rows; Long-Term Retention is backup-only, restorable only as a new database — SQ2-04, SQ2-05, SQ2-14) or high-ingest telemetry/events (Microsoft's own data-store model guide routes that workload to Azure Data Explorer/Eventhouse, not Azure SQL — SQ2-06; sustained write is capped by log rate regardless of vCores — SQ2-07). Bulk load is CONDITIONAL, not automatically STRONG: throughput has no published guarantee and the Power Platform SQL connector cannot bulk-load at all — a separate ADF/bcp toolchain is implied (SQ2-12, SQ2-13). (DA-26, DA-30, DA-33, DA-36, DA-37, DA-38, SQ2-01, SQ2-04..SQ2-15).
- **SharePoint / Lists is preferable when:** the document is the record (files + metadata, versions, retention labels, protection travelling with the file); small flat trackers with ≤ 1–2 lookups, list-level security, single environment, low write concurrency; forms over one list; seeded licensing must stay and the app runs outside Teams; **customer-managed encryption key over SharePoint/OneDrive content** is achievable via Microsoft 365 Customer Key's dedicated DEP — contrary to v1, this is NOT a disqualifier, only a tenant/geo-granularity limitation with an E5-class licence and two paid Azure subscriptions (SQ2-10) (DA-44, DA-59, PS-14, SQ2-10).
- **Dataverse for Teams is preferable when:** team-scoped, self-contained app on seeded licences within 2 GB, no API/sharing/ALM ambitions (DA-13).
- **Azure Data Explorer / Eventhouse in Fabric is preferable when:** the workload is genuinely "high-ingest timestamped metrics and events" (IoT, application telemetry, monitoring, financial market data) — this is Microsoft's own named target for that model, not Azure SQL or Dataverse (SQ2-06). *(New alternative surfaced in v2; not previously named in this file.)*
- **The external system should remain the system of record when:** it owns the entity/fields (MDM/ERP); the app needs only a view or lookup; audit/compliance obligations live there; bidirectional sync would create two masters (no product-grade bidirectional tooling exists outside D365 F&O dual-write, and even that requires a careful one-way-door canonical model — DQ-06); history/reporting belongs to the warehouse — surface via embedding, a virtual table (uniform security, narrow/positively-filtered/sub-1,000-row, read-mostly — see the full appropriate/not-appropriate ladder in `VT-17`; Microsoft publishes no performance characterisation at any volume, `VT-09`) or a read-only replicated subset (DA-45..DA-48, DA-51, VT-09, VT-17, DQ-06).
- **A hybrid data architecture is preferable when:** operational UX needs Dataverse features on a subset of ERP data (replicated read model + event/queue path back — but note there is NO first-party managed Dataverse→Azure SQL replication service; every writable-SQL copy is a customer-built-and-operated pipeline with its own reconciliation job, `SY-01`, `SY-18`); analytics/history needs a lake (Fabric/Synapse link) beside the OLTP store — the free, lowest-reconciliation-burden route is Link to Fabric's auto-provisioned read-only SQL analytics endpoint when no writes are needed (`SY-02`); high-ingest events need elastic/purpose-built storage beside relational master data; documents need SharePoint labels beside Dataverse records; binaries need Blob/SharePoint beside Dataverse references (DA-09, DA-14, DA-19, DA-20, DA-37, DA-49, DA-59, SY-01, SY-02, SY-18).
- **Another technology should be considered when:** strict cross-system consistency cannot tolerate temporary inconsistency ("Use strong consistency mechanisms or atomic transactions across all steps instead"); no transit of row data through Microsoft cloud is mandated; distributed multi-primary writes are required (Dataverse: "No"); country-level residency without ADR; reporting needs sub-15-minute freshness across systems (Power Pages caches at a non-tunable 15-minute SLA, `SC-14`; DirectQuery over Dataverse is explicitly slow past ~20,000 rows / 10-minute query timeout, `SC-20`) (DA-07, DA-34, DA-37, DA-49, DA-57, SC-14, SC-20).

---

## 7. Conflicts (CONFLICTED)

| Id | Topic | Source A | Source B | Assessment |
|---|---|---|---|---|
| C-01 | Default tenant Dataverse database capacity | Licensing Guide Sept 2026 table: 20 GB [DV:S40 p.20] | Same guide worked example: 10 GB [DV:S40 p.21] | Internal inconsistency (also PS C-1). Model with 10 GB; confirm in admin center. |
| C-02 | Elastic tables GA status | Developer page 2026-08: "known issues … should be addressed before this feature becomes generally available" [DV:S03] | Maker page and bulk-ops page describe them without preview caveat [DV:S24, DV:S27] | Unresolved (also PS U-16). Treat as maturity risk. |
| C-03 | Elastic tables — alternate keys | Maker page 2025-03: "Alternate key" not supported [DV:S24] | Developer page 2026-08 references alternate keys for partitioned rows [DV:S03] | Newer developer page likely current; verify in environment. |
| C-04 | Reporting offload mechanism | Reporting considerations 2023-12: SSIS/ETL tools [XC:S06] | 2026 pages: Synapse Link / Fabric link [XC:S01, XC:S04, XC:S43] | Principle valid, mechanism stale. |
| C-05 | Dataverse for Teams row figure | Environment page: only "2 GB" [DV:S18] | Licensing FAQ: "up to 1,000,000 records based on typical usage (enforced as 2 GB …)"; overview: "up to 1 million rows" [SP:S-09, SP:S-10] | 1M is Microsoft's "typical usage" gloss on the 2 GB enforcement; cite as such. |
| C-06 | Fabric link "no copy" | "No copy, no ETL"; "your data stays in Dataverse" [XC:S04] | Same page: "optimized replica … using Dataverse storage"; "increase in Dataverse database storage" [XC:S04] | Marketing vs mechanism; a billed replica exists inside Dataverse-managed storage. |
| C-07 | Column security vs analytical copies | CLS "apply to all data access requests" [XC:S12] | Secured columns export as null unless lake app user is in profile; fix widens exposure to all lake readers [XC:S43] | Design tension, not contradiction. |
| C-08 | Canvas apps calling stored procedures | Security page 2025-05: "Power Apps doesn't currently connect to stored procedures." [SQ:S5] | Access-data page 2025-06: direct SP calls in Power Fx, incl. secure implicit connections [SQ:S3] | Newer, specific page wins; security page stale. |
| C-09 | Delegable functions vs SharePoint connector | Generic delegation list includes `Not`, `IsBlank`, `In`, `StartsWith` [SP:S-33] | SharePoint table: `Not` never; `IsBlank` No on text/complex; `StartsWith` not on Choice/Lookup subfields [SP:S-04] | Connector-specific table governs. |
| C-10 | Flow polling intervals | Troubleshoot page: 15 min (Free), 5 min (Office 365 / Dynamics 365 plans) [EX:S47] | Current limits page organises by Low/Medium/High profile without minute figures [EX:S26] | Possibly stale; verify before quoting. |
| C-11 | "Near real-time" | Synapse/Fabric "near real-time insights", "continuously refreshes" [XC:S03, XC:S31] | "can't be guaranteed" under high churn; "up to 60 minutes" [XC:S30, XC:S31] | Undefined term; plan for ≤ 1 h. |
| C-12 | Where the Dataverse search index bills | "All Dataverse indexes are reported at the Dataverse database capacity rate." [DV:S01] | "Search indexes are stored in both log and database storage" [DV:S28] | Capacity page newer and authoritative → database meter. |
| C-13 | SharePoint unenforced-lookup delete behaviour | Fetch-summarised S-07: target item "is also removed" when unenforced | Common description elsewhere: lookup value emptied, item kept | Fetch tool may be lossy; verify page directly (U-11). |
| C-14 | Effective sync timeout canvas → SQL | Connector: 110 s for query/SP actions [SQ:S1] | Power Apps request 180 s [SQ:S33]; T4 "typically 2 minutes" [SQ:S27] | Layered limits; design to 110 s; do not cite "2 minutes" as Microsoft. |
| C-15 | Bidirectional sync legitimacy | Listed as a pattern "There's no clear record keeper" [EX:S05] | "Avoid creating tightly coupled point-to-point…" [EX:S09]; dual-write "tightly coupled" [EX:S41] | Offered and warned; only with product tooling or explicit per-field ownership. |
| C-16 | SharePoint referential integrity | T3: "no referential integrity, no cascading deletes" [SP:S-31] | T1: opt-in "Restrict delete / Cascade delete" per lookup [SP:S-07] | T1 wins: exists, opt-in, delete-only, threshold-bound. |
| C-17 *(new v2)* | Do entity-scoped business rules execute server-side on Web API/integration writes? | Scope table: "Entity \| Model-driven app forms **and server**"; perf note: "server side (XAML generated as synchronous plugins)" [DQ:S4] | Same page's FAQ: "Business rules are run on clients... **They aren't executed inside Dataverse.**" [DQ:S4] | Unresolved on docs alone (`DQ-10`). Treat as **Assumed**, not Confirmed; the single highest-value empirical test in this research: activate a table-scoped validate-and-error rule, POST a violating record via Web API, observe. |
| C-18 *(new v2)* | Is Duplicate Detection suppressed by default on Web API **Create**, not only Update? | Page states the default explicitly only for Update: "By default, duplicate detection is suppressed when you are updating records" [DQ:S5] | Create requires setting the header to `false`, which implies (but does not state) the same default | Treat the Create default as Medium-High confidence inference, not a direct quote (`DQ-12`, U-05 in `v2-quality.md`). |
| C-19 *(new v2)* | Does Fabric Mirroring's source list ever include Dataverse? | v2 finding: Dataverse absent from the enumerated source list as of ms.date 2026-08-28 [SY:S-01] | The list has grown repeatedly (SharePoint List, SAP, Oracle recently added) | Point-in-time negative finding (`SY-01`). Re-check before every engagement; a future addition would materially change the Dataverse→SQL recommendation. |
| C-20 *(new v2)* | Does Link to Fabric share Synapse Link's documented silent-divergence modes (secured columns null, calculated columns frozen, direct-SQL deletes not propagating)? | Both mechanisms rest on Dataverse change tracking, so overlap is plausible | No page found states this explicitly for Link to Fabric — the divergence catalogue (`SY-14`) is sourced from the Synapse Link FAQ specifically | Unresolved (`SY` Unknown U-01). Read the Link to Fabric FAQ/limitations pages end to end and compare item by item before assuming the mitigations transfer. |

---

## 8. Unknowns (UNKNOWN)

| Id | Unknown | Why it matters | Resolution path |
|---|---|---|---|
| U-01 | Magnitude of Dataverse database increase from Link to Fabric (no Microsoft ratio) | Analytics cost model | Pilot one environment; read "-Analytics" entries in capacity report |
| U-02 | Elastic tables GA status and alternate-key support (C-02, C-03) | Maturity of the high-volume option | Release plans; test in environment |
| U-03 | SharePoint Online indexed-columns maximum and per-type column counts (Server figures only) | Index budget under the LVT | Read support page table directly; SPO admin docs |
| U-04 | Whether the Power Apps SharePoint connector uses ETag/If-Match on `Patch`; any multi-item transaction | Concurrency/integrity claims for lists (T4-based today) | Connector docs / test |
| U-05 | SQL connector concurrency/locking semantics (isolation, transaction scope of Patch/UpdateIf, deadlock retry) | Correctness under concurrent edits on SQL | Test; ROWVERSION checks in SPs |
| U-06 | Recycle bin GA wording ("When the deleted records setting is generally available…") | Reliance in production | PPAC label in target tenant; release plans |
| U-07 | **PARTIALLY CLOSED in v2.** Verbatim Microsoft statement "relationships/queries cannot span environments" | DA-25 rests on inference | v2: cross-environment **reads** are confirmed supported (connection-common-data-service, "Change environment"); cross-environment **relationships/joins** remain unconfirmed by an explicit Microsoft statement (still inferred from relationships being single-environment metadata) — see `DA-25` revised. |
| U-08 | Whether Microsoft support creates custom indexes on standard tables on request | Mitigability of large-table performance risk | Support/FastTrack guidance |
| U-09 | Gateway node throughput / requests-per-second for Power Apps traffic | Gateway sizing | Load test; monitoring docs |
| U-10 | Whether Power Platform VNet support requires Managed Environments (not stated on the overview) | Licensing of private connectivity | vnet-support-setup-configure page; Managed Environments overview |
| U-11 | Exact wording of SharePoint lookup relationship page (unenforced delete behaviour; 1,000-item delete cap) | Integrity semantics (C-13) | Open support page in browser |
| U-12 | A Microsoft page stating explicitly that SharePoint lists have no column-level security | Negative claim rests on absence | Search permission-level docs; else keep INF/MEDIUM |
| U-13 | **LARGELY CLOSED in v2** (17 new findings `VT-01`..`VT-17`). Virtual table provider limits (OData v4, SQL beyond 1,000 rows, SharePoint, Fabric): paging, latency, throttling, write support | Feasibility per external system | v2 confirms: CRUD is provider-dependent, not documented in one matrix (`VT-02`); OData paging config documented but stale page (`VT-08`); **no performance/latency/throughput/caching characterisation exists for ANY provider** — this is now a hard negative finding, not an open unknown (`VT-09`). Still open: per-provider write matrix for Snowflake/PostgreSQL/Databricks (`VT` U-07). |
| U-14 | **CLOSED in v2** (as far as Microsoft resolves it). Microsoft's formal distinction "system of record" vs "source of truth" (IG uses "owner"; "source of truth" only for golden config env) | Vocabulary for the decision model | v2: the D365 IG chapters are alive (`DQ-01`, corrected URLs); Microsoft uses "primary data" / "master data source" in the IG and, in the Azure Architecture Center microservices guidance, ties "source of truth" to a per-entity *consistency requirement* — the only near-definition found (`DQ-03`, `DQ-15`). **Conclusion: the terms are used loosely and interchangeably across Microsoft surfaces; no formal distinction exists. The pack must declare its own vocabulary as pack-local.** |
| U-15 | Choice-option change = solution deployment (metadata) — implied, not quoted | Choice-vs-lookup rule (DA-53) | Dataverse metadata docs |
| U-16 | "Data Life Cycle Config" deletion policies: scope and GA | GDPR erasure of retained data | LTR set-up / deletion policy page |
| U-17 | Dynamics 365 Sales Premium capacity uplift (MC1253515) on Learn | Capacity accrual for D365 tenants | Dynamics 365 Licensing Guide |
| U-18 | EUR pricing / EA effects on capacity add-ons and PAYG | Cost localisation | Regional price list |
| U-19 | **CLOSED in v2.** Explicit "no write-back" statement for Synapse Link / Fabric link | Closing the one-way OLTP→OLAP claim with a quote | v2: "Virtual tables created with data from Microsoft Fabric OneLake are read-only. Currently, you can't modify the data in Fabric OneLake with Power Apps." Plus the Synapse Link lake-side statement "Data files shouldn't be modified by a customer" (`VT-13`). The only documented return path is the read-only OneLake virtual table (`VT-12`, `VT-16`); any write-back must be built as a separate integration with its own identity and error handling. |
| U-20 | Current Power Automate polling interval per performance profile (C-10) | Freshness of flow-based sync | Licensing types page; connector trigger docs |
| U-21 | LTR read-access limits (query volume; Power BI on retained data) and storage rate | Feasibility of read-only history via LTR | Developer LTR page |
| U-22 | CMK interplay with Synapse Link / Fabric link | CMK + analytics decision | CMK/Fabric FAQ or support |
| U-23 | Power Automate flow run history counted toward Dataverse capacity? (assumed not) | Classic workflow vs cloud flow storage argument | Power Automate limits page |
| U-24 | Column count / row-byte hard limits per Dataverse table; max tables per environment | Wide-table design | Not on fetched pages |
| U-25 | SharePoint / Azure Blob per-GB prices (T3 claims ~$0.20/GB) | Offload ROI | Azure/M365 pricing pages |
| U-26 | Power Query SharePoint Online List connector (implementation 2.0) volume/LVT behaviour and refresh performance | BI viability over big lists | power-query/connectors/sharepoint-online-list |
| U-27 *(new v2)* | Whether Dataverse standard tables guarantee read-after-write for a *different* session/client (cross-process, not just within one transaction) | A design that assumes cross-session immediate visibility (e.g. a flow reading what a plug-in just wrote elsewhere) may rest on an unstated assumption | Ask Microsoft support/FastTrack for an explicit statement; `SC-06` establishes the *choice criterion* ("requires strong data consistency" → standard tables) and the substrate (Azure SQL) but not a named read-after-write guarantee |
| U-28 *(new v2)* | Whether Dataverse standard tables use any read replica or geo-replication that could serve stale reads | PE:08's read-replica sentence is about "Azure database services" generically, not confirmed as a Dataverse feature | Confirm with Microsoft; do not assert either way (`SC-06` Unknown) |
| U-29 *(new v2)* | Quantified request cost of auditing per audited write | Audited high-volume tables could consume materially more request budget than modelled; audit tables are not queryable via TDS | Measure via Application Insights for Dataverse on a prototype with auditing on vs off (`SC-21`) |
| U-30 *(new v2)* | Maximum row count/size for a Dataverse **standard** table (only elastic tables carry published scale claims: "tens of millions of rows every hour") | Promising a specific standard-table ceiling would be invented | No published envelope exists; validate by load/soak test at projected 3-5-year volume (`SC-18`) |
| U-31 *(new v2)* | Exact number of concurrent users an environment/app supports | Any quoted ceiling would be fabricated | None published anywhere across 16 sources checked; close with a load test against a production-like environment (PE:05) (`SC-16`, `SC-17`) |
| U-32 *(new v2)* | When the Power Automate licensing transition period ends and official (lower) enforcement begins | Designs sized to transition-period limits (200k/500k per flow) would break at official enforcement (40k/250k per identity) | Track PPAC reporting GA status; design to official limits now, as Microsoft itself instructs (`SC-04`) |
| U-33 *(new v2)* | Does the Dataverse service-protection concurrency default of 52 vary by environment, and by how much ("might be higher") | Hard-coding 52 under-uses larger environments; assuming more over-drives smaller ones | Drive concurrency from the `x-ms-dop-hint` response header at runtime, never from a constant (`SC-19`) |
| U-34 *(new v2)* | Whether model-driven app clients have any documented server-side data cache (beyond Power Pages 15-min and Dataverse's cached `CountRows`) | No page found in this pass addresses model-driven client caching directly | Targeted research on model-driven `RetrieveMultiple` caching if a scenario depends on it (`SC-12`, `SC-14` Unknowns) |
| U-35 *(new v2)* | Whether Azure SQL Database (PaaS) supports the bulk-logged/simple recovery models that minimal logging depends on, or is always in full recovery model | Decides whether "bulk load STRONG" has any minimal-logging path at all, or is purely log-rate-bound | Fetch Azure SQL Database automated-backups/recovery-model documentation and quote directly (`SQ2-12` U1) |
| U-36 *(new v2)* | Whether Stretch Database (the historical "cheap cold tier" answer for SQL Server) is formally deprecated with no successor | If dead, the "no cheap archive tier in Azure SQL" negative finding (`SQ2-05`) is airtight | Fetch the Stretch Database deprecation notice and quote it (`SQ2` U2) |
| U-37 *(new v2)* | Can a Power Apps canvas app or cloud flow set `SESSION_CONTEXT` on the SQL connector's connection before a query, to make `SESSION_CONTEXT`-based row-level security reachable from Power Platform | Decides whether per-user SQL RLS is reachable at all inside Power Platform without Entra Integrated auth or a custom middle tier | Search Learn for SQL connector + `sp_set_session_context`; likely resolves to "not supported" (`SQ2-08` U4) |
| U-38 *(new v2)* | Does Fabric Mirroring's source list ever add Dataverse as a mirrorable source | The headline negative finding `SY-01` is a point-in-time enumeration on a page updated repeatedly through 2026 | Re-check the Fabric Mirroring overview page at the start of every engagement (`SY` U-10) |
| U-39 *(new v2)* | Cost and duration of a full Synapse Link / Link to Fabric table resynchronization at realistic volumes | Microsoft prescribes "resynchronize the table" as the remedy for most drift modes (`SY-14`, `SY-15`) but never states its cost | Measure on a sandbox with a representative table (`SY` U-07) |
| U-40 *(new v2)* | Whether entity-scoped business rules actually fire on Web API/integration writes | Determines whether "validates regardless of the app used" is Confirmed or Assumed — the single highest-value empirical test identified in this research | Activate a table-scoped validate-and-error rule; POST a violating record via Web API; observe (`DQ-10` U-10) — **do this before encoding any pack rule that assumes server-side business-rule enforcement** |
| U-41 *(new v2)* | Whether Microsoft anywhere states "don't migrate historical data" as a rule (vs. an inference from the enumerated migration categories "master data" and "open transactions") | The pack should not attribute a rule to Microsoft that Microsoft does not state | Search D365 F&SCM data-migration best-practice docs and FastTrack guidance; until found, treat "don't migrate history" as pack opinion, not Microsoft guidance (`DQ-05`, `DQ` U-03) |

---

## 9. Deferred to other areas

| Gap | Target area | Effect if undelivered |
|---|---|---|
| Power Automate as sync engine at volume: per-profile throughput, trigger intervals (U-20), 14-day auto-off operational handling | 04 | DA-49/DA-52 freshness and reliability cells stay "verify per tenant" |
| Custom connectors / API-fronted SQL and ERP (auth, token passthrough, paging, SOAP), Azure API Management | 05 | "API layer with user tokens" alternative in DA-33/DA-45 unquantified |
| Entra identity population, external users, service principals for integration identities | 06 | Guest-user exclusions (SQL Entra connections) and integration identity sizing stay partial |
| Environment strategy doctrine (per unit vs shared), DLP design, CoE data policies | 07 | DA-25/DA-63 remain principles without an operating model |
| Data pipelines in ALM (CMT/Package Deployer/pipelines pre-deployment steps), dataflow connection re-establishment after deployment | 08 | DA-24 reference-data pipeline unvalidated |
| Load benchmarks: Dataverse web-server count vs licences, gateway throughput (U-09), TDS/DirectQuery at concurrency | 09 | Performance cells stay "validate by test" |
| Full cost model: capacity in EUR/EA (U-18), Fabric capacity SKUs, Azure SQL tiers, gateway servers, Managed Environments per-user effect | 10 | "CONDITIONAL on budget" cells cannot be quantified |
| Backup/DR operating model, storage-hygiene run-book, erasure run-book execution | 11 | DA-18/DA-27/DA-60 stay design principles |
| Hybrid reference patterns (Dataverse + Azure SQL + Fabric; ERP event hub) as first-class patterns | 12 | DA-37/DA-49/DA-50 remain findings, not catalogued patterns |

Undelivered deferrals revert the corresponding matrix cells to UNKNOWN, as in `platform-suitability.md` §7.

---

## 10. Evidence-quality notes

- **Fetched (default):** ≈ 210 of ≈ 230 sources across the five sub-registers, all decision-weight Tier 1 pages included. **Fetched-summarised** (support.microsoft.com pages returned as summaries): SP:S-02, S-07, S-15, S-17, S-18, S-23, S-27, S-30, S-31, S-32; SQ:S25, S27, S28. **Snippet-only:** DV:S36; EX:S43, S45, S54; XC:S52, S53, S54, S55 — none carries a finding above MEDIUM alone.
- **Independent spot-checks by the consolidator (2026-09-02):** Fabric link storage statements (DV:S17/XC:S04, ms.date 2026-07-06) — confirmed verbatim; SharePoint LVT "can't be changed", 30M items, 12 joins, 50,000/5,000 unique permissions (SP:S-02) — confirmed; SQL connector class Premium, 100 CRUD calls/10 s, 125 concurrent, 110-s timeout, 2 MB/8 MB gateway caps, trigger statement (SQ:S1, updated 2026-07-11) — confirmed.
- **Cross-verification between sub-researches:** service protection limits, TDS endpoint, long-term retention, capacity meters, virtual-table limitations, alternate keys, delegation, Synapse/Fabric link, Managed Environments prerequisites and the SharePoint delegation table were each fetched independently by two or more sub-researches with matching quotes.
- **Aged pages (> 18 months) still load-bearing:** XC:S06 reporting considerations (2023-12), DV:S26/XC:S37 POA (2023-09), DV:S22/EX:S36 CMT (2023-11), XC:S42 connect-data-sources (2023-08), SP:S-34 Get items (2022-06), SP:S-19 base 2020 (updated 2026-05), EX:S35 choices (2022-08), EX:S50 materialized view (2022-07), SP:S-35 SharePoint Server boundaries (2018 — Server figures, flagged), DV:S39 SharePoint integration (2020-09), SQ:S13/SP:S-06 performance considerations (2024-12). Findings on them carry MEDIUM on currency where noted.
- **T3/T4 with commercial or opinion bias:** DV:S29/S30 (POA blogs), DV:S36–S38 (ISV/consultancy storage blogs), SP:S-30/S-31/S-42 (consultant blogs), SQ:S28 (Power Apps Guide), EX:S44/S45 (integration vendors), XC:S52–S55 (community threads) — used as signals and negative evidence only.
- **404 / retired at fetch time:** D365 IG `data-management-data-migration`, `-data-architecture`, `-data-quality`, `-data-governance`, `-data-storage`; `power-apps/guidance/planning/data-storage` and `data-design`; `power-platform/admin/optimize-performance-dataverse`; `canvas-apps/connections/sql-connection-security` and `sql-stored-procedures` (content covered by SQ:S5/SQ:S3); Power Query dataflows limits pages; AAC transactional-outbox; the former "Using the SharePoint connector with canvas apps" real-world example now redirects to the reference-architecture index. No current Microsoft reference architecture uses SharePoint lists as the primary transactional store (SP U-05).
- **Microsoft publishes no explicit negative-fit guidance for stores** beyond "Excel isn't a relational database system", "Dataverse is the preferred choice if you need more complex relational data", the reporting "shorter periods of time" statement and the D365 IG integration anti-patterns; other POOR verdicts are inferences from documented limits and are tagged INF in §2.
- **Authorship:** five sub-researches and the consolidation were produced in one session by the same agent lineage; adversarial review and gate are pending (status header). Independent spot-check recommended for DV:S40 (PDF extraction), SP:S-07, SP:S-16 and EX:S54 before pack authoring.
- **v2 additions (new in v2):** ≈95 new sources across five targeted sub-researches (`VT` 12, `SY` 19, `SQ2` 15, `SC` 16, `DQ` 13), all but four Tier 1 Microsoft Learn, fetched 2026-09-02. Weakest new sources, flagged by their own sub-researches: `VT:S3` (OData v4 provider page, ms.date 2021-08-11, five years stale — `VT-08`); `SY:S16` (Synapse Link serverless SQL page, ms.date 2021-08-06, five years stale — `SY-16`); `SY:S19` (Synapse SQL external-tables docs, search-summary only, not fetched verbatim — `SY-16` U-09); `DQ:S6`/`DQ:S7`/`DQ:S9` (support.microsoft.com SharePoint pages, no `ms.date` — `DQ-13`). The `DQ` sub-research corrected a source-navigation failure from the prior pass: the D365 Implementation Guide's data chapters were NOT 404 — they are live under a flat `implementation-guide/data-management*` URL prefix; the prior 404s were wrong URL shapes (`DQ-01`).
- **v2 discovered one genuine contradiction inside Microsoft's own documentation**, not resolvable from the docs alone: the business-rules page states both that Entity scope reaches "server" (compiled to synchronous plug-ins) and, in its own FAQ, that business rules "aren't executed inside Dataverse" (`DQ-10`, conflict `C-17`). This is flagged, not silently resolved, and is named as the single highest-value empirical test to run before pack authoring (`DQ-10`, Unknown U-40).
- **v2 independent spot-checks by the consolidator (2026-09-02):** re-fetched and confirmed verbatim: `reporting-considerations` (the "beyond 50,000 rows" sentence, closing review F-06); `data-retention-overview` (LTR mechanics); `hierarchy-security` (50-user/manager guidance); `limits-tshoot-virtual-tables` (1,000-record scope, closing review F-03 in part); `connection-common-data-service` (the Dataverse delegation table and the "Change environment" cross-environment read capability, closing review F-02 and F-07); the SharePoint Q&A thread (corrected the "Microsoft moderator" attribution to "Ling Zhou_MSFT, Microsoft External Staff", closing review F-12).

---

## 11. Implications for the aisa knowledge model (pointers, not pack content) and gate conditions

Nothing below is a question, glossary term, signal or decision-tree node; these are pointers for authoring.

- **Technology-neutral Discovery signals suggested by the evidence (per entity, not per solution):** expected rows and growth per queried table; query shape (filters, negations, sorts, free-text, aggregates); relationship count and cascade expectations; all-or-nothing write groups; concurrent editors on the same record; freshness expectation per interface ("live" vs minutes vs daily) and tolerance to the source being down; owner system per entity and per field; whether only a view or the data itself is needed; binary volume and originals vs derived images; audit obligation (fields, years) and read-audit needs; retention years and legal-hold; erasure obligations; reporting scope (per-user/time-boxed vs org-wide/historical) and whether reports must respect record security; row/column sensitivity matrix; residency regime (EUDB / country) and AI processing constraints; on-prem vs cloud location of existing data; private-network mandate; environment/organisational boundaries and re-org volatility; seeded-only licence constraint; existing SQL schema hygiene (PKs, triggers, types); data steward availability; **new in v2:** peak (not average) business-event volume per event type, for the write-amplification translation (SC-21); named owning identity and licence for every automation (SC-05); which single interface actually needs sub-15-minute freshness, as distinct from a general "real time" ask (SC-14); whether the read model needs writes at all, since that single question decides whether a customer-built SQL pipeline is needed (SY-18).
- **Hard boundaries with Microsoft-stated evidence:** delegation truncation (DA-02); SharePoint LVT and 12 joins (DA-39, DA-40); no client-side atomicity (DA-07); ownership immutability (DA-12); one-directional capacity borrowing (DA-04); aggregate-query/chart 50k ceiling, precisely scoped — NOT a flat report ceiling (DA-03 revised); LTR irreversible, Managed Env, no file saving (DA-17); backups ≤ 28 d (DA-18); Fabric replica on database meter (DA-19); virtual-table forfeits, including the newly precise 1,000-record scope for 1:N/polymorphic queries (DA-45 revised, VT-06); sync-webhook rollback hazard (DA-50); gateway 2 MB/8 MB and SP degradation (DA-34); SQL connector 100/10 s and 110 s (DA-32); implicit connections = maker identity (DA-33); Managed Environments gate (DA-55); EUDB dual condition and global metadata (DA-57, DA-58); **new in v2:** no first-party Dataverse→Azure SQL replication service (SY-01); no virtual-table performance/throughput characterisation at any volume (VT-09); no concurrent-user ceiling published anywhere (SC-16); no cheap cold-storage tier for Azure SQL rows (SQ2-05); Azure SQL sustained write capped by log rate regardless of vCores (SQ2-07); duplicate detection off by default on Web API updates (DQ-12).
- **Corrected boundaries:** licensing does not discriminate SQL from Dataverse (DA-61); "keep data on-prem via gateway" does not keep it out of Microsoft cloud transit (DA-34, DA-58); "no copy" Fabric link is a billed replica (C-06); "embed Power BI and security follows" is false (DA-22); "start on SharePoint, move later" drops attachments/images/metadata and re-implements permissions (DA-44); **new in v2:** "environment is a hard boundary for everything" is corrected — cross-environment reads work, cross-environment relationships don't (DA-25 revised); SharePoint/M365 "cannot do customer-managed keys" is wrong (SQ2-10); Azure SQL "strong for telemetry/cheap archival/bulk load" is contradicted/downgraded (SQ2-06, SQ2-05, SQ2-12); "resubmitting failed flow runs" is not a reconciliation strategy (SY-12, SY-18); "row counts detect replica drift" is false — the Synapse Link FAQ documents ≥8 silent-divergence modes (SY-14).
- **Data-architecture options the pack must be able to output:** Dataverse-only; Dataverse + SharePoint documents; Dataverse + file/Blob offload; Dataverse + elastic tables; Dataverse + Fabric/Synapse analytical tier (+ LTR archive tier), noting the read-only SQL analytics endpoint as the lowest-reconciliation-burden reporting path (SY-02, SY-18); Dataverse for Teams; SQL/Azure SQL as store (with gateway or VNet); SQL system of record + Dataverse virtual tables (read-only reference, volume/latency unverified — VT-09); customer-built Dataverse→writable-Azure-SQL pipeline with its own reconciliation job (SY-18); Azure Data Explorer/Eventhouse for genuine high-ingest telemetry (SQ2-06); replicated subset (dataflow/event) + queue back to ERP; embedding/read-through with no store; Azure-native database alongside Dataverse; SharePoint list for document-centric/flat trackers; keep in place + process change.
- **Validation before commitment (typical):** delegation proof with row limit = 1 per store/query; schema audit of any reused SQL database; ownership/visibility matrix per entity before schema; capacity model per meter incl. sandboxes and analytics replica; freshness SLA per interface accepted by the business; one change-set/stored-procedure transaction prototype on the critical write path; erasure and retention run-book per copy; residency check (macro region, billing address, ADR, AI settings); gateway estate costing or VNet design; DLP groups per environment; PII masking step for environment copies; **new in v2:** a write-amplification pilot per solution before quoting any request budget (Application Insights for Dataverse / flow Analytics → Actions, SC-21); a virtual-table volume/latency spike against production-like data before committing to that path (VT-09, VT-17); the single empirical test on whether business rules enforce on Web API writes (DQ-10, U-40); a measured pilot copy load before committing to any SQL bulk-load window (SQ2-13); a load test (PE:05) instead of a quoted concurrent-user figure (SC-17).
- **Gate conditions proposed for downstream use (mandatory once gated):** (1) every store verdict keeps its origin tag; INF-derived POOR phrased "treat as unsupported until verified" — **now applied to the §2 matrix in v2** (review F-01 closed); (2) before pack authoring: resolve C-01 in the admin center, verify SP:S-07 and SP:S-16 wording directly, confirm U-10 (VNet ↔ Managed Env — still open in v2), re-check elastic GA (U-02 — still open in v2); U-19 (no write-back) is **CLOSED** in v2 (VT-13); (3) the pack must not encode any numeric "practical row ceiling" for SharePoint beyond Microsoft's 5,000-per-query and 30M storage figures (SP C-05), nor a Fabric storage multiplier (U-01), nor a virtual-table volume ceiling (no Microsoft figure exists — VT-09), nor a Dataverse standard-table row ceiling (none published — SC-18), nor a concurrent-user ceiling (none published — SC-16), nor a write-amplification multiplier (SC-21 — engagement-measured only); (4) deferrals in §9 back-reference this file; undelivered deferrals revert cells to UNKNOWN; (5) re-verify short-half-life facts (Fabric low-latency engine, elastic tables, recycle bin, SharePoint→Dataverse conversion preview, Copilot flex routing, VNet connector list, virtual-table provider preview status — Fabric/Salesforce/Oracle) before encoding; (6) **new in v2:** before encoding any pack rule that assumes server-side business-rule enforcement on integration writes, run the empirical test in U-40 (DQ-10) — this is the single highest-value unresolved contradiction in the whole research corpus; (7) **new in v2:** re-check the Fabric Mirroring source list (SY-01) before every engagement — a future addition of Dataverse would materially change the Dataverse→SQL recommendation.

---

## 12. Source register

All Microsoft Learn URLs fetched 2026-09-02 by the sub-research named in each sub-register (or by the consolidator where noted in §10). Date = `ms.date` shown in page metadata (updated date where different). Kind: fetched / fetched-summarised / snippet-only / T2–T4 as recorded by the sub-research. Ids are cited in findings with the sub-register prefix.

### 12.1 Dataverse sub-research (cite as `DV:Sxx`)

| Id | Tier | Fetched? | Title | URL | ms.date |
|---|---|---|---|---|---|
| S01 | T1 | fetched | Dataverse capacity-based storage details | https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage | 2026-08-17 |
| S02 | T1 | fetched | Dataverse long term data retention overview | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-retention-overview | 2026-04-10 |
| S03 | T1 | fetched | Elastic Tables for Developers | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/elastic-tables | 2026-08-04 |
| S04 | T1 | fetched | Page Results Using FetchXml | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/page-results | 2026-03-12 |
| S05 | T1 | fetched | Aggregate Data Using FetchXml | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/aggregate-data | 2026-03-09 |
| S06 | T1 | fetched | Requests limits and allocations | https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations | 2026-08-14 |
| S07 | T1 | fetched | About table relationships for Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-entity-relationships | 2026-01-09 |
| S08 | T1 | fetched | Define rollup columns with Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/define-rollup-fields | 2024-04-30 |
| S09 | T1 | fetched | Work with Dataverse formula columns | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/formula-columns | 2026-01-09 |
| S10 | T1 | fetched | Column data types in Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/types-of-fields | 2026-06-24 |
| S11 | T1 | fetched | Security concepts in Microsoft Dataverse | https://learn.microsoft.com/en-us/power-platform/admin/wp-security-cds | 2025-06-03 |
| S12 | T1 | fetched | Hierarchy security | https://learn.microsoft.com/en-us/power-platform/admin/hierarchy-security | 2026-06-22 |
| S13 | T1 | fetched | Service protection API limits | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/api-limits | 2026-01-09 |
| S14 | T1 | fetched | Use SQL to query data (TDS endpoint) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/dataverse-sql-query | 2026-06-01 |
| S15 | T1 | fetched | Create and edit virtual tables | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-virtual-entities | 2026-04-17 |
| S16 | T1 | fetched | Create an Azure Synapse Link for Dataverse with your Azure Synapse Workspace | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-synapse | 2026-07-06 |
| S17 | T1 | fetched | Link your Dataverse environment to Microsoft Fabric | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-view-in-fabric | 2026-07-06 |
| S18 | T1 | fetched | About the Microsoft Dataverse for Teams environment | https://learn.microsoft.com/en-us/power-platform/admin/about-teams-environment | 2026-05-15 |
| S19 | T1 | fetched | Manage Dataverse auditing | https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing | 2026-04-08 |
| S20 | T1 | fetched | Free up storage space | https://learn.microsoft.com/en-us/power-platform/admin/free-storage-space | 2026-03-26 |
| S21 | T1 | fetched | Copy an environment | https://learn.microsoft.com/en-us/power-platform/admin/copy-environment | 2025-12-04 |
| S22 | T1 | fetched | Move configuration data across organizations (Configuration Migration tool) | https://learn.microsoft.com/en-us/power-platform/admin/manage-configuration-data | 2023-11-21 |
| S23 | T1 | fetched | Solution concepts with Power Platform | https://learn.microsoft.com/en-us/power-platform/alm/solution-concepts-alm | 2025-01-29 |
| S24 | T1 | fetched | Create and edit elastic tables | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-elastic-tables | 2025-03-31 |
| S25 | T1 | fetched | Optimize data performance (Power Platform Well-Architected PE:08) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/optimize-data-performance | 2025-08-15 |
| S26 | T1 | fetched | Manage PrincipalObjectAccess storage | https://learn.microsoft.com/en-us/power-platform/admin/manage-principalobjectaccess-storage | 2023-09-20 |
| S27 | T1 | fetched | Optimize Performance for Bulk Operations: Best Practices | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimize-performance-create-update | 2026-03-26 |
| S28 | T1 | fetched | Storage management in Dataverse and finance and operations apps | https://learn.microsoft.com/en-us/power-platform/admin/storage-management | 2025-05-30 |
| S29 | T4 | fetched | How To Shrink Your Principal Object Access POA Table By 99% (Andrew Howes) | https://andyhowes.co/how-to-fix-the-principal-object-access-table/ | 2024-04-15 (publish) |
| S30 | T4 | fetched | How uncontrolled parental relationships fuel Dynamics 365 Dataverse growth (Think Tech With SJ) | https://thinktechwithsj.wordpress.com/2024/12/20/how-uncontrolled-parental-relationships-fuel-dynamics-365-dataverse-growth/ | 2024-12-20 (publish) |
| S31 | T1 | fetched | Migrate Data Between Dataverse Environments Using the OData Connector | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/dataverse-odata-dataflows-migration | 2026-03-12 |
| S32 | T1 | fetched | What licenses do you need to use dataflows | https://learn.microsoft.com/en-us/power-query/dataflows/what-licenses-do-you-need-in-order-to-use-dataflows | 2024-07-24 |
| S33 | T1 | fetched | Create and edit columns in Dataverse using Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-field-portal | 2026-01-09 |
| S34 | T1 | fetched | Configure Dataverse search for your environment | https://learn.microsoft.com/en-us/power-platform/admin/configure-relevance-search-organization | 2026-05-08 |
| S35 | T1 | fetched | Important changes (deprecations) coming in Power Platform | https://learn.microsoft.com/en-us/power-platform/important-changes-coming | 2026-05-22 |
| S36 | T3 | search-snippet-only | Dynamics 365 Document Management: Storage Options ... (MSDynamicsWorld) / ERP Software Blog / CRM Software Blog snippets | https://msdynamicsworld.com/blog/dynamics-365-document-management-storage-options-attachments-limitations-best-practices | n/d |
| S37 | T3 | fetched | Power Platform File Storage Options Strengths & Limitations (rockhop.ai) | https://rockhop.ai/insights/power-platform-file-storage-options | 2024-01-24 (publish) |
| S38 | T3 | fetched | Microsoft Is Doubling Your Dataverse File Storage (Inogic) | https://www.inogic.com/blog/2026/03/microsoft-is-doubling-your-dataverse-file-storage-what-every-dynamics-365-admin-should-do-before-april-15/ | 2026-03-24 (publish) |
| S39 | T1 | fetched | Benefits of document management with SharePoint integration | https://learn.microsoft.com/en-us/power-platform/admin/set-up-sharepoint-integration | 2020-09-28 |
| S40 | T1 | fetched (PDF, text-extracted) | Power Platform Licensing Guide — September 2026 | https://go.microsoft.com/fwlink/?linkid=2085130 → https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/bade/documents/products-and-services/en-us/bizapps/Power-Platform-Licensing-Guide-September-2026.pdf | Sept 2026 edition |
| S41 | T2 | fetched | MC1253515 — Dynamics 365 Sales – Get additional Dataverse storage capacity (Message Center archive, merill.net) | https://mc.merill.net/message/MC1253515 | 2026-03-16 (published) |
| S42 | T1 | fetched | Query anti-patterns (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/query-antipatterns | 2025-09-10 |
| S43 | T1 | fetched | Query throttling (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/query-throttling | 2025-01-08 |
| S44 | T1 | fetched | Optimize performance using OData | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/query/optimize-performance | 2025-08-11 |
| S45 | T1 | fetched | Optimize performance using FetchXml | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/fetchxml/optimize-performance | 2025-08-11 |
| S46 | T1 | fetched | Dataverse capacity-based storage overview (what's new in storage) | https://learn.microsoft.com/en-us/power-platform/admin/whats-new-storage | 2026-08-17 |
| S47 | T1 | fetched | Capacity add-ons for Power Apps and Power Automate | https://learn.microsoft.com/en-us/power-platform/admin/capacity-add-on | 2025-12-12 |
| — | — | 404 | https://learn.microsoft.com/en-us/power-platform/admin/optimize-performance-dataverse | not found |

### 12.2 SQL / Azure SQL sub-research (cite as `SQ:Sx`)

| Id | Tier | Fetched / snippet | Title | URL | ms.date |
|---|---|---|---|---|---|
| S1 | T1 | Fetched | SQL Server - Connectors | https://learn.microsoft.com/en-us/connectors/sql/ | 2024-03-01 (updated_at 2026-07-11) |
| S2 | T1 | Fetched (redirect from connection-azure-sqldatabase) | Connect to SQL Server from Power Apps overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-connection-overview | 2025-03-14 |
| S3 | T1 | Fetched | Access data in SQL Server - Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-connection-access-data | 2025-06-19 |
| S4 | T1 | Fetched | Microsoft Azure Virtual Network support - Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/vnet-support-overview | 2026-07-28 |
| S5 | T1 | Fetched | Use Microsoft SQL Server securely with Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-server-security | 2025-05-21 |
| S6 | T1 | Fetched | Create virtual tables using virtual connectors in Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-virtual-tables-using-connectors | 2026-05-07 |
| S7 | T1 | Fetched | Limitations and troubleshooting virtual tables with Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/limits-tshoot-virtual-tables | 2026-05-15 |
| S8 | T1 | Fetched | What is an on-premises data gateway? | https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem | 2025-06-10 |
| S9 | T1 | Fetched | Manage on-premises data gateway high-availability clusters and load balancing | https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-high-availability-clusters | 2025-06-12 |
| S10 | T1 | Fetched | Install an on-premises data gateway | https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-install | 2025-10-15 |
| S11 | T1 | Fetched | Serverless compute tier - Azure SQL Database | https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-overview | 2026-07-28 |
| S12 | T1 | Fetched | Use SQL to query data (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/dataverse-sql-query | 2026-06-01 |
| S13 | T1 | Fetched | Performance considerations for Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/app-performance-considerations | 2024-12-10 |
| S14 | T1 | Fetched | Understand delegation in a canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview | 2026-01-13 |
| S15 | T1 | Fetched (redirect from performance-tips) | How to create performant Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview | 2026-08-20 |
| S16 | T1 | Fetched | Select the right services and features recommendation for Power Platform workloads (PE:03) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/select-services | 2025-08-15 |
| S17 | T1 | Fetched (redirect from data-store-considerations) | Prepare to Choose a Data Store in Azure - Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-stores-getting-started | 2025-09-02 |
| S18 | T1 | Fetched | Create and use dataflows in Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-and-use-dataflows | 2026-01-09 |
| S19 | T1 | Fetched | Serverless auto-pause and auto-resume - Azure SQL Database | https://learn.microsoft.com/en-us/azure/azure-sql/database/serverless-tier-auto-pause-resume | 2026-07-28 |
| S20 | T1 | Fetched | Licensing overview for Microsoft Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/pricing-billing-skus | 2025-06-17 |
| S21 | T1 | Fetched | Power Platform URLs and IP address ranges | https://learn.microsoft.com/en-us/power-platform/admin/online-requirements | 2026-08-03 |
| S22 | T1 | Fetched | Overview of connectors for canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections-list | 2026-01-13 |
| S23 | T1 | Fetched | Managed connectors outbound IP addresses | https://learn.microsoft.com/en-us/connectors/common/outbound-ip-addresses | 2024-03-01 (updated_at 2025-11-19) |
| S24 | T1 | Fetched | DirectQuery in Power BI: When to Use, Limitations, Alternatives | https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about | 2025-09-25 |
| S25 | T2 | Fetched (summarised by fetch tool) | Enhanced security for implicitly shared connections in Power Apps (Power Platform Blog) | https://www.microsoft.com/en-us/power-platform/blog/power-apps/power-apps-secure-implicit-connections/ | 2023-03-30 |
| S26 | T1 | Fetched | Plan, scale, and maintain a business-critical gateway solution | https://learn.microsoft.com/en-us/data-integration/gateway/plan-scale-maintain | 2025-06-26 |
| S27 | T4 | Fetched (summarised by fetch tool) | PowerApps SQL connector has become intermittent with regular timeouts for some users (Microsoft Q&A) | https://learn.microsoft.com/en-us/answers/questions/5637283/powerapps-sql-connector-has-become-intermittent-wi | 2025-11-26 (question date) |
| S28 | T3 | Fetched (summarised by fetch tool) | SQL - Caution! This is how users can hack shared SQL connections (Power Apps Guide) | https://powerappsguide.com/blog/post/sql-security-how-to-hack-implicit-connections | 2021-01-23 |
| S29 | T1 | Fetched | Dataverse capacity-based storage details | https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage | 2026-08-17 |
| S30 | T1 | Fetched | Microsoft Dataverse reference architectures and solution ideas | https://learn.microsoft.com/en-us/power-platform/architecture/products/microsoft-dataverse | 2026-08-25 |
| S31 | T1 | Fetched | Pay-as-you-go plan overview | https://learn.microsoft.com/en-us/power-platform/admin/pay-as-you-go-overview | 2025-05-29 |
| S32 | T1 | Fetched | Connect Power Apps to a centralized data warehouse with Dataverse virtual tables (reference architecture) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/power-apps-virtual-tables | 2026-08-18 |
| S33 | T1 | Fetched | Power Apps system requirements and limits | https://learn.microsoft.com/en-us/power-apps/limits-and-config | 2026-01-12 |

Not retrievable (HTTP 404 at fetch time, 2026-09-02): `…/canvas-apps/connections/sql-connection-security`, `…/canvas-apps/connections/sql-stored-procedures` (content covered by S5 and S3 respectively).

### 12.3 SharePoint / Lists / Excel sub-research (cite as `SP:S-xx`)

| id | tier | fetched? | title | URL | ms.date |
|---|---|---|---|---|---|
| S-01 | T1 | fetched | SharePoint limits - Service Descriptions | https://learn.microsoft.com/en-us/office365/servicedescriptions/sharepoint-online-service-description/sharepoint-online-limits | 2025-05-29 |
| S-02 | T1 | fetched (summarised by fetch tool) | Manage large lists and libraries / List View Threshold | https://support.microsoft.com/en-us/office/manage-large-lists-and-libraries-b8588dae-9387-48c2-9248-c24122f07c59 | n/d |
| S-03 | T1 | fetched | SharePoint - Connectors | https://learn.microsoft.com/en-us/connectors/sharepointonline/ | 2024-03-01 (updated 2026-08-01) |
| S-04 | T1 | fetched | Connect to SharePoint from a canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online | 2025-03-14 |
| S-05 | T1 | fetched | Excel Online (Business) - Connectors | https://learn.microsoft.com/en-us/connectors/excelonlinebusiness/ | 2024-03-01 (updated 2026-07-11) |
| S-06 | T1 | fetched | Performance considerations for Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/app-performance-considerations | 2024-12-10 |
| S-07 | T1 | fetched (summarised by fetch tool) | Create list relationships by using unique and lookup columns | https://support.microsoft.com/en-us/office/create-list-relationships-by-using-unique-and-lookup-columns-80a3e0a6-8016-41fb-ad09-8bf16d490632 | n/d |
| S-08 | T1 | fetched | Understand SharePoint forms integration | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/sharepoint-form-integration | 2025-11-14 |
| S-09 | T1 | fetched | Power Platform licensing FAQs | https://learn.microsoft.com/en-us/power-platform/admin/powerapps-flow-licensing-faq | 2026-08-14 |
| S-10 | T1 | fetched | Microsoft Dataverse for Teams overview | https://learn.microsoft.com/en-us/power-apps/teams/overview-data-platform | 2026-05-20 |
| S-11 | T1 | fetched | Limits of automated, scheduled, and instant flows | https://learn.microsoft.com/en-us/power-automate/limits-and-config | 2026-07-17 |
| S-12 | T1 | fetched | Use environment variables in Power Platform solutions | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables | 2026-01-09 |
| S-13 | T1 | fetched | Integrate SharePoint Online into Power Apps overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/sharepoint-list-integration-overview | 2026-01-13 |
| S-14 | T1 | fetched | Optimize data performance (Well-Architected PE:08) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/optimize-data-performance | 2025-08-15 |
| S-15 | T1 | fetched (summarised by fetch tool) | Customize permissions for a SharePoint list or library | https://support.microsoft.com/en-us/office/customize-permissions-for-a-sharepoint-list-or-library-02d770f3-59eb-4910-a608-5f84cc297782 | n/d |
| S-16 | T4 (Microsoft Q&A; answer by Microsoft moderator) | fetched | Why our SharePoint Online lists do not track any save conflicts... | https://learn.microsoft.com/en-us/answers/questions/1417030/why-our-sharepoint-online-lists-do-not-track-any-s | 2023-11-06 |
| S-17 | T1 | fetched (summarised) | Enable and configure versioning for a list or library | https://support.microsoft.com/en-us/office/enable-and-configure-versioning-for-a-list-or-library-1555d642-23ee-446a-990a-bcab618c7a37 | n/d |
| S-18 | T1 | fetched (summarised) | Restore items in the recycle bin that were deleted from SharePoint or Teams | https://support.microsoft.com/en-us/office/restore-items-in-the-recycle-bin-that-were-deleted-from-sharepoint-or-teams-6df466b6-55f2-4898-8d6e-c0dff851a0be | n/d |
| S-19 | T1 | fetched | Microsoft SharePoint Connector for Power Automate | https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/sharepoint-connector-actions-triggers | 2020-03-10 (updated 2026-05-12) |
| S-20 | T1 | fetched | Integrate legacy data with Power Automate and SharePoint (reference architecture) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/app-legacy-data-integration | 2025-07-09 |
| S-21 | T1 | fetched | Dataverse for Teams vs. Dataverse | https://learn.microsoft.com/en-us/power-apps/teams/data-platform-compare | 2025-05-28 |
| S-22 | T1 | fetched | What is Microsoft Dataverse? | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-intro | 2026-03-31 |
| S-23 | T1 | fetched (summarised) | What is a list in Microsoft 365? | https://support.microsoft.com/en-us/office/what-is-a-list-in-microsoft-365-93262a88-20ad-4edc-8410-b6909b2f59a5 | n/d |
| S-24 | T1 | fetched | Manage SharePoint document visibility in Dataverse solutions | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/sharepoint-dataverse-security | 2026-08-25 |
| S-25 | T1 | fetched | Learn about retention for SharePoint and OneDrive | https://learn.microsoft.com/en-us/purview/retention-policies-sharepoint | 2025-09-22 |
| S-26 | T1 | fetched | Create and edit tables using Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-entities-portal | 2026-01-09 |
| S-27 | T2 | fetched (summarised) | Easier than ever experience to import data from SharePoint List (Power Platform blog) | https://www.microsoft.com/en-us/power-platform/blog/power-apps/easier-than-ever-experience-to-import-data-from-sharepoint-list/ | 2024-04-04 |
| S-28 | T1 | fetched | Create a semantic model from a SharePoint List (Power BI) | https://learn.microsoft.com/en-us/power-bi/connect-data/create-dataset-sharepoint-online-list | 2023-02-22 |
| S-29 | T1 | fetched | Power Query SharePoint list connector | https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-list | 2025-11-21 |
| S-30 | T3 | fetched (summarised) | SharePoint - how to fix list threshold errors... (powerappsguide.com, T. Leung) | https://powerappsguide.com/blog/post/large-sharepoint-list-fix-list-view-threshold-error | 2021-04-01 |
| S-31 | T3 | fetched (summarised) | Best SharePoint List vs Dataverse: Essential 2026 Guide (wrvishnu.com) | https://www.wrvishnu.com/sharepoint-list-vs-dataverse/ | 2026-01-06 / upd. 2026-05-08 |
| S-32 | T2 | fetched (summarised) | SharePoint delegation improvements (Power Apps blog) | https://www.microsoft.com/en-us/power-platform/blog/power-apps/sharepoint-delegation-improvements/ | 2019-08-14 |
| S-33 | T1 | fetched | Understand delegation in a canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview | 2026-01-13 |
| S-34 | T1 | fetched | In-depth analysis into 'Get items' and 'Get files' | https://learn.microsoft.com/en-us/sharepoint/dev/business-apps/power-automate/guidance/working-with-get-items-and-get-files | 2022-06-28 |
| S-35 | T1 (SharePoint Server, not Online) | fetched | Software boundaries and limits for SharePoint Servers 2016 and 2019 | https://learn.microsoft.com/en-us/sharepoint/install/software-boundaries-limits-2019 | 2018-01-08 |
| S-36 | T1 | fetched | Overview of external sharing in SharePoint and OneDrive | https://learn.microsoft.com/en-us/sharepoint/external-sharing-overview | 2026-05-07 |
| S-37 | T1 | fetched | SharePoint site lifecycle management | https://learn.microsoft.com/en-us/sharepoint/site-lifecycle-management | 2026-07-01 |
| S-38 | T1 | fetched | Connect to cloud-storage from Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/cloud-storage-blob-connections | 2021-03-15 |
| S-39 | T1 | fetched | Column-level security (Dataverse) | https://learn.microsoft.com/en-us/power-platform/admin/field-level-security | 2025-11-19 |
| S-40 | T1 | fetched | Create and use dataflows in Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-and-use-dataflows | 2026-01-09 |
| S-41 | T1 | fetched | Create a report on a SharePoint List in Power BI Desktop | https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-sharepoint-online-list | 2024-12-03 |
| S-42 | T3 | fetched (summarised) | Power Apps Dataverse vs SharePoint List (spguides.com, B. Kumar) | https://www.spguides.com/power-apps-dataverse-vs-sharepoint-list/ | 2026-04-03 |
| S-43 | T1 | fetched (summarised) | How to create performant Power Apps (overview) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview | 2026-08-20 |
| — | T1 | 404 / redirect | "Using the SharePoint connector with canvas apps" (guidance real-world example) → now redirects to reference-architectures index | https://learn.microsoft.com/en-us/power-platform/guidance/architecture/real-world-examples/sharepoint-canvas | n/a |
| — | T1 | 404 | Software boundaries and limits (SharePoint Server, old URL) | https://learn.microsoft.com/en-us/sharepoint/install/software-boundaries-and-limits-0 | n/a |

Notes on S-39/S-40/S-41/S-42/S-43: fetched for contrast/verification; S-39 quote used: "Use column-level security to manage access to data in specific columns. Column-level security configurations are organization-wide and apply to all data access requests." (Dataverse). S-41 adds the Microsoft framing "Many teams and organizations use lists in SharePoint Online to store data because it's easy to set up and easy for users to update." S-42 (opinion): "if the broken app would cause a real business problem, invest in Dataverse. If the broken app would just be inconvenient, SharePoint list is probably fine."

### 12.4 External systems & multi-store patterns sub-research (cite as `EX:Sxx`)

| Id | Tier | Fetched? | Title | URL | ms.date |
|---|---|---|---|---|---|
| S01 | T1 | fetched | Optimize data performance recommendation for Power Platform workloads (PE:08) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/optimize-data-performance | 2025-08-15 |
| S02 | T1 | fetched | Select the right services and features recommendation (PE:03) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/select-services | 2025-08-15 |
| S03 | T1 | fetched | Handle transient faults recommendation (RE:05) | https://learn.microsoft.com/en-us/power-platform/well-architected/reliability/handle-transient-faults | 2025-08-18 |
| S04 | T1 | 404 | (reliability/design-workloads-resilient-to-failures) | https://learn.microsoft.com/en-us/power-platform/well-architected/reliability/design-workloads-resilient-to-failures | n/d |
| S05 | T1 | fetched | Choose the right pattern for your integration strategy (D365 IG) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/integrate-other-solutions-choose-pattern | 2024-01-26 |
| S06 | T1 | fetched | Choose the right design for your Dynamics 365 apps integration (D365 IG) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/integrate-other-solutions-choose-design | 2024-01-25 |
| S07 | T1 | fetched | Manage your data in Dynamics 365 implementation projects (D365 IG) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management | 2024-01-08 |
| S08 | T1 | fetched | Overcome integration challenges in Dynamics 365 projects (D365 IG) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/integrate-other-solutions-challenges | 2024-01-26 |
| S09 | T1 | fetched | Select the ideal platform for your Dynamics 365 apps integration (D365 IG) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/integrate-other-solutions-choose-platform | 2024-01-25 |
| S10 | T1 | fetched (redirect target) | Prepare to Choose a Data Store in Azure (AAC) | https://learn.microsoft.com/en-us/azure/architecture/guide/technology-choices/data-store-considerations → data-stores-getting-started | 2025-09-02 |
| S11 | T1 | fetched | Cache-Aside Pattern (AAC) | https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside | 2025-09-11 |
| S12 | T1 | fetched | Saga Design Pattern (AAC) | https://learn.microsoft.com/en-us/azure/architecture/patterns/saga | 2025-02-25 |
| S13 | T1 | fetched | Compensating Transaction Pattern (AAC) | https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction | 2026-04-16 |
| S14 | T1 | fetched | Create and edit virtual tables with Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-virtual-entities | 2026-04-17 |
| S15 | T1 | fetched | Create an Azure Synapse Link for Dataverse with your Azure Synapse Workspace | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-synapse | 2026-07-06 |
| S16 | T1 | fetched | Understand delegation in a canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview | 2026-01-13 |
| S17 | T1 | fetched | Optimize Performance for Bulk Operations: Best Practices | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimize-performance-create-update | 2026-03-26 |
| S18 | T1 | fetched | Service protection API limits (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/api-limits | 2026-01-09 |
| S19 | T1 | fetched | Use change tracking to synchronize data with external systems | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/use-change-tracking-synchronize-data-external-systems | 2026-03-31 |
| S20 | T1 | fetched | Work with alternate keys (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/define-alternate-keys-entity | 2026-03-30 |
| S21 | T1 | fetched | Use Webhooks to Create External Handlers for Server Events | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/use-webhooks | 2026-03-31 |
| S22 | T1 | fetched | Azure Service Bus Integration for Dataverse | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/azure-integration | 2026-03-31 |
| S23 | T1 | fetched | Set up duplicate detection rules to keep your data clean | https://learn.microsoft.com/en-us/power-platform/admin/set-up-duplicate-detection-rules-keep-data-clean | 2025-04-24 |
| S24 | T1 | fetched | Import data from Excel and export data to CSV | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-import-export | 2026-01-16 |
| S25 | T1 | fetched (redirect target) | How to create performant Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/performance-tips → create-performant-apps-overview | 2026-08-20 |
| S26 | T1 | fetched | Limits of automated, scheduled, and instant flows (Power Automate) | https://learn.microsoft.com/en-us/power-automate/limits-and-config | 2026-07-17 |
| S27 | T1 | fetched | Manage configuration and migration data for Dynamics 365 projects (D365 IG) | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management-configuration-data-migration | 2024-01-17 |
| S28 | T1 | fetched | Data migration for Dynamics 365 implementation projects | https://learn.microsoft.com/en-us/dynamics365/guidance/resources/migrate-data | 2026-06-17 |
| S29 | T1 | fetched | What licenses do you need to use dataflows (Power Query) | https://learn.microsoft.com/en-us/power-query/dataflows/what-licenses-do-you-need-in-order-to-use-dataflows | 2024-07-24 |
| S30 | T1 | fetched | Synchronize data across Dataverse environments using Power Platform (ref. arch.) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/sync-dataverse-data | 2026-04-30 |
| S31 | T1 | fetched | Dataverse as a master data system (D365 ref. arch.) | https://learn.microsoft.com/en-us/dynamics365/guidance/reference-architectures/dataverse-master-data-system | 2025-11-04 |
| S32 | T1 | fetched | How server-side caching works in Power Pages | https://learn.microsoft.com/en-us/power-pages/admin/clear-server-side-cache | 2026-04-29 |
| S33 | T1 | fetched | App object in Power Apps (Power Fx reference) | https://learn.microsoft.com/en-us/power-platform/power-fx/reference/object-app | 2026-06-11 |
| S34 | T1 | fetched | Use environment variables in Power Platform solutions | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/environmentvariables | 2026-01-09 |
| S35 | T1 | fetched | Create and edit choices (picklists) overview for Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-global-option-sets | 2022-08-05 |
| S36 | T1 | fetched | Move configuration data across organizations (Configuration Migration tool) | https://learn.microsoft.com/en-us/power-platform/admin/manage-configuration-data | 2023-11-21 |
| S37 | T1 | fetched | Dataverse capacity-based storage details | https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage | 2026-08-17 |
| S38 | T1 | fetched | Configuration Migration tool in Power Platform (ALM) | https://learn.microsoft.com/en-us/power-platform/alm/configure-and-deploy-tools | 2026-08-19 |
| S39 | T1 | fetched | Link your Dataverse environment to Microsoft Fabric | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-view-in-fabric | 2026-07-06 |
| S40 | T1 | fetched | Dataverse long term data retention overview | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-retention-overview | 2026-04-10 |
| S41 | T1 | fetched | Dual-write overview (D365 F&O) | https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/dual-write/dual-write-overview | 2026-01-15 |
| S42 | T1 | fetched | Copy and transform data in Dynamics 365 (Microsoft Dataverse) — Azure Data Factory connector | https://learn.microsoft.com/en-us/azure/data-factory/connector-dynamics-crm-office-365 | 2025-07-25 |
| S43 | T3 | search-snippet only | Dual-write to Dataverse: the initial sync and cutover runbook (dev.to/sapotacorp) | https://dev.to/sapotacorp/dual-write-to-dataverse-the-initial-sync-and-cutover-runbook-2cf3 | n/d |
| S44 | T3 | fetched | How to Navigate API Rate Limits for High-load Integrations with Microsoft Dataverse (uds.systems) | https://uds.systems/blog/navigating-api-rate-limits-for-high-load-integrations-with-microsoft-dataverse/ | 2025-08-20 |
| S45 | T3/T4 | search-snippet only | KingswaySoft help manual / ClonePartner blog (SSIS vs ADF) | https://www.kingswaysoft.com/products/ssis-integration-toolkit/help-manual/major-enterprise-applications/dynamics-365/crm/destination ; https://clonepartner.com/blog/dynamics-365-migration-ssis-kingswaysoft-vs-adf-vs-clonepartner/ | n/d |
| S46 | T1 | fetched | Plan, scale, and maintain a business-critical gateway solution | https://learn.microsoft.com/en-us/data-integration/gateway/plan-scale-maintain | 2025-06-26 |
| S47 | T1 | fetched (redirect target) | Troubleshoot common problems with Power Automate triggers | https://learn.microsoft.com/en-us/troubleshoot/power-platform/power-automate/flow-run-issues/triggers-troubleshoot | 2026-08-07 |
| S48 | T1 | fetched | Performance considerations for Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/app-performance-considerations | 2024-12-10 |
| S49 | T1 | fetched | Queue-Based Load Leveling Pattern (AAC) | https://learn.microsoft.com/en-us/azure/architecture/patterns/queue-based-load-leveling | 2026-06-09 |
| S50 | T1 | fetched | Materialized View pattern (AAC) | https://learn.microsoft.com/en-us/azure/architecture/patterns/materialized-view | 2022-07-28 |
| S51 | T1 | fetched | Use Dataverse background operations (ref. arch.) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/dataverse-background-operations | 2025-04-17 |
| S52 | T1 | fetched | Use Dataverse as a data source for canvas apps (ref. arch.) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/dataverse-canvas-app | 2025-07-15 |
| S53 | T1 | fetched | Use the SQL Server with canvas apps (ref. arch.) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/sqlserver-canvas-app | 2025-07-15 |
| S54 | T1 | search-snippet only | FAQ for SharePoint List to table and app | https://learn.microsoft.com/en-us/power-apps/maker/common/faqs-sharepoint-list-to-table-app | n/d |
| S55 | T3 | fetched (no relevant content) | ERP Integration Patterns (Steven Singer) | https://stevensinger.org/blog/2025/06/erp-integration-patterns.html | 2025-06-13 |
| — | T1 | 404 | Requested D365 IG URLs not found: data-management-data-migration, -data-architecture, -data-quality, -data-governance, -data-storage; Azure Architecture Center saga reference-architecture path; Power Query dataflows-limitations/-refresh-limitations/-limits; power-pages/configure/configure-cache; create-table-sharepoint-list; AAC transactional-outbox | — | — |

### 12.5 Cross-cutting requirements sub-research (cite as `XC:Sxx`)

| id | tier | fetched? | title | URL | ms.date |
|---|---|---|---|---|---|
| S01 | T1 | fetched | Power Query Dataverse connector | https://learn.microsoft.com/en-us/power-query/connectors/dataverse | 2026-04-08 |
| S02 | T1 | fetched | Use SQL to query data (Dataverse TDS endpoint) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/dataverse-sql-query | 2026-06-01 |
| S03 | T1 | fetched | Azure Synapse Link for Dataverse (overview) | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/export-to-data-lake | 2026-04-27 |
| S04 | T1 | fetched | Link your Dataverse environment to Microsoft Fabric | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-view-in-fabric | 2026-07-06 |
| S05 | T1 | fetched | Create or edit a model-driven app system chart | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/create-edit-system-chart | 2026-05-05 |
| S06 | T1 | fetched | Reporting considerations (model-driven apps) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/reporting-considerations | 2023-12-20 |
| S07 | T1 | fetched | Important changes (deprecations) coming in Power Platform | https://learn.microsoft.com/en-us/power-platform/important-changes-coming | 2026-05-22 |
| S08 | T1 | fetched | Dataverse long term data retention overview | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-retention-overview | 2026-04-10 |
| S09 | T1 | fetched | Manage Dataverse auditing | https://learn.microsoft.com/en-us/power-platform/admin/manage-dataverse-auditing | 2026-04-08 |
| S10 | T1 | fetched | Restore deleted Dataverse table records | https://learn.microsoft.com/en-us/power-platform/admin/restore-deleted-table-records | 2026-04-27 |
| S11 | T1 | fetched | Back up and restore environments | https://learn.microsoft.com/en-us/power-platform/admin/backup-restore-environments | 2026-06-23 |
| S12 | T1 | fetched | Column-level security | https://learn.microsoft.com/en-us/power-platform/admin/field-level-security | 2025-11-19 |
| S13 | T1 | fetched | Security concepts in Microsoft Dataverse | https://learn.microsoft.com/en-us/power-platform/admin/wp-security-cds | 2025-06-03 |
| S14 | T1 | fetched | Create and manage masking rules | https://learn.microsoft.com/en-us/power-platform/admin/create-manage-masking-rules | 2025-10-30 |
| S15 | T1 | fetched | Manage your customer-managed encryption key | https://learn.microsoft.com/en-us/power-platform/admin/customer-managed-key | 2026-05-18 |
| S16 | T1 | fetched | IP firewall in Power Platform environments | https://learn.microsoft.com/en-us/power-platform/admin/ip-firewall | 2026-05-18 |
| S17 | T1 | fetched | Azure Virtual Network support for Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/vnet-support-overview | 2026-07-28 |
| S18 | T1 | fetched | Choose the region when setting up an environment | https://learn.microsoft.com/en-us/power-platform/admin/regions-overview | 2026-05-28 |
| S19 | T1 | fetched | What is the EU Data Boundary? | https://learn.microsoft.com/en-us/privacy/eudb/eu-data-boundary-learn | 2026-07-21 |
| S20 | T1 | fetched | Move data across regions for Copilots and generative AI features | https://learn.microsoft.com/en-us/power-platform/admin/geographical-availability-copilot | 2026-05-21 |
| S21 | T1 | fetched | On-premises data gateway architecture | https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem-indepth | 2025-06-10 |
| S22 | T1 | fetched | Types of tables (ownership) | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/types-of-entities | 2026-07-30 |
| S23 | T1 | fetched | Power Platform and Dynamics 365 macro region geography | https://learn.microsoft.com/en-us/power-platform/admin/macro-regions | 2026-07-15 |
| S24 | T1 | fetched | Work with alternate keys (developer) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/define-alternate-keys-entity | 2026-03-30 |
| S25 | T1 | fetched | Define alternate keys using Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/define-alternate-keys-portal | 2025-05-14 |
| S26 | T1 | fetched | Set up duplicate detection rules | https://learn.microsoft.com/en-us/power-platform/admin/set-up-duplicate-detection-rules-keep-data-clean | 2025-04-24 |
| S27 | T1 | fetched | Power Query SharePoint list connector | https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-list | 2025-11-21 |
| S28 | T1 | fetched | Managed environments overview | https://learn.microsoft.com/en-us/power-platform/admin/managed-environment-overview | 2026-02-23 |
| S29 | T1 | fetched | Customer Lockbox in Power Platform and Dynamics 365 | https://learn.microsoft.com/en-us/power-platform/admin/about-lockbox | 2026-05-05 |
| S30 | T1 | fetched | Create an Azure Synapse Link with your Synapse workspace | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-synapse | 2026-07-06 |
| S31 | T1 | fetched | Configure your environment and link to Microsoft Fabric | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/fabric-link-to-data-platform | 2026-08-17 |
| S32 | T1 | fetched | DirectQuery in Power BI: when to use, limitations | https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about | 2025-09-25 |
| S33 | T1 | fetched | Service protection API limits (Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/api-limits | 2026-01-09 |
| S34 | T1 | fetched | Responding to DSR requests for Power Apps customer data | https://learn.microsoft.com/en-us/power-platform/admin/powerapps-privacy-dsr-guide | 2024-12-09 |
| S35 | T1 | fetched | Connect to and manage Microsoft Dataverse in Microsoft Purview | https://learn.microsoft.com/en-us/purview/register-scan-dataverse | 2026-02-02 |
| S36 | T1 | fetched | Well-Architected: Data classification recommendation | https://learn.microsoft.com/en-us/power-platform/well-architected/security/data-classification | 2025-08-18 |
| S37 | T1 | fetched | Manage PrincipalObjectAccess storage | https://learn.microsoft.com/en-us/power-platform/admin/manage-principalobjectaccess-storage | 2023-09-20 |
| S38 | T1 | fetched | Hierarchy security | https://learn.microsoft.com/en-us/power-platform/admin/hierarchy-security | 2026-06-22 |
| S39 | T1 | fetched | Create or edit business units | https://learn.microsoft.com/en-us/power-platform/admin/create-edit-business-units | 2025-05-21 |
| S40 | T1 | fetched | Update a record Owner and Owning Business Unit | https://learn.microsoft.com/en-us/power-platform/admin/update-record-owner | 2025-11-26 |
| S41 | T1 | fetched | Dynamics 365 and Power Platform data residency documentation | https://learn.microsoft.com/en-us/dynamics365/get-started/availability | 2026-07-07 |
| S42 | T1 | fetched | Connecting and authenticating to data sources | https://learn.microsoft.com/en-us/power-platform/admin/security/connect-data-sources | 2023-08-25 |
| S43 | T1 | fetched | Azure Synapse Link for Dataverse FAQ | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/export-data-lake-faq | 2026-09-01 |
| S44 | T1 | fetched | Microsoft Fabric Link for Dataverse FAQ | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/fabric-link-faq | 2026-08-18 |
| S45 | T1 | fetched | Connect to SharePoint from a canvas app (delegation) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/connection-sharepoint-online | 2025-03-14 |
| S46 | T1 | fetched | Data policies (DLP) overview | https://learn.microsoft.com/en-us/power-platform/admin/wp-data-loss-prevention | 2026-04-07 |
| S47 | T1 | fetched | Embed a Power BI report in a model-driven app main form | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/embed-powerbi-report-in-system-form | 2026-04-03 |
| S48 | T1 | fetched | D365 Implementation Guide: Manage your data | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management | 2024-01-08 |
| S49 | T1 | fetched | Enable sensitivity labels for files in SharePoint and OneDrive | https://learn.microsoft.com/en-us/purview/sensitivity-labels-sharepoint-onedrive-files | 2026-08-07 |
| S50 | T1 | fetched | Responding to DSR requests for Dataverse customer data | https://learn.microsoft.com/en-us/power-platform/admin/dataverse-privacy-dsr-guide | 2025-11-20 |
| S51 | T1 | fetched | Connect to SQL Server from Power Apps overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-connection-overview | 2025-03-14 |
| S52 | T4 | search-snippet-only (fetch 403) | Fabric Community: "Dataverse Costs - Link to Microsoft Fabric (F&O)" | https://community.fabric.microsoft.com/t5/Fabric-platform/Dataverse-Costs-Link-to-Microsoft-Fabric-F-amp-O/m-p/4644645 | n/d |
| S53 | T4 | search-snippet-only | Fabric Community / blogs: slow SharePoint list refresh in Power BI | https://community.fabric.microsoft.com/t5/Desktop/Power-BI-Sharepoint-List-Slow-Refresh/td-p/1437464 ; https://www.vojtechsima.com/post/how-to-fix-slow-sharepoint-list-refresh-in-power-bi | n/d |
| S54 | T4 | search-snippet-only | Fabric/Power BI Community: Dataverse DirectQuery slowness / timeouts | https://community.fabric.microsoft.com/t5/Desktop/Connection-to-dataverse-extremely-slow/td-p/1781593 ; https://community.powerbi.com/t5/Power-Query/Timeout-issue-on-dataverse-side/td-p/1628943 | n/d |
| S55 | T4 | not fetched (403) | Fabric Community: "Real-World Cost Impact of Dataverse Link to Fabric" | https://community.fabric.microsoft.com/discussions/ac_dataengineering/real-world-cost-impact-of-dataverse-link-to-fabric/5220983 | n/d |
| S56 | T1 | fetched | Access data in SQL Server (Power Apps) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/connections/sql-connection-access-data | 2025-06-19 |

Not reachable (404): `power-apps/guidance/planning/data-storage`, `.../data-design`, `canvas-apps/connections/sql-connection-implicit-connections`, `power-apps/important-changes-coming` (content now at S07 path).

### 12.6 Virtual tables / Fabric consumption sub-research (cite as `VT:Sxx`)


| id | tier | fetched | title | URL | ms.date |
|---|---|---|---|---|---|
| S1 | T1 | full fetch 2026-09-02 | Create virtual tables using virtual connectors in Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-virtual-tables-using-connectors | 2026-05-07 |
| S2 | T1 | full fetch 2026-09-02 | Limitations and troubleshooting virtual tables with Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/limits-tshoot-virtual-tables | 2026-05-15 |
| S3 | T1 | full fetch 2026-09-02 | Use the virtual table OData v4 Data Provider with Microsoft Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/virtual-entity-odata-provider-requirements | 2021-08-11 |
| S4 | T1 | full fetch 2026-09-02 | Get started with virtual tables (entities) (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/virtual-entities/get-started-ve | 2026-01-07 |
| S5 | T1 | full fetch 2026-09-02 | API considerations of virtual tables (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/virtual-entities/api-considerations-ve | 2026-03-20 |
| S6 | T1 | full fetch 2026-09-02 | Custom virtual table data providers (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/virtual-entities/custom-ve-data-providers | 2026-08-27 |
| S7 | T1 | full fetch 2026-09-02 | Build apps and take action with insights from Microsoft Fabric | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-build-apps-with-fabric | 2026-04-09 |
| S8 | T1 | full fetch 2026-09-02 | Frequently asked questions about Microsoft Fabric Link for Dataverse | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/fabric-link-faq | 2026-08-18 |
| S9 | T1 | full fetch 2026-09-02 | Understand delegation in a canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/delegation-overview | 2026-01-13 |
| S10 | T1 | full fetch 2026-09-02 | FAQ about exporting Dataverse table data to Azure Synapse Analytics and Azure Data Lake | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/export-data-lake-faq | 2026-09-01 |
| S11 | T1 | full fetch 2026-09-02 | Link your Dataverse environment to Microsoft Fabric and unlock deep insights | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-view-in-fabric | 2026-07-06 |
| S12 | T1 | full fetch 2026-09-02 | Automation-centric data analytics with the Dataverse - Fabric integration | https://learn.microsoft.com/en-us/power-automate/automation-analytics-with-fabric-introduction | 2024-12-19 |

No T2/T3/T4 sources were used. Every finding above rests on Microsoft Learn (T1) or is explicitly labelled INF.

---

### 12.7 Dataverse→SQL replication & reconciliation sub-research (cite as `SY:S-xx`)


| id | Title | URL | Tier | ms.date |
|---|---|---|---|---|
| S-01 | Mirroring — Microsoft Fabric (canonical `/fabric/mirroring/overview`) | https://learn.microsoft.com/en-us/fabric/database/mirrored-database/overview | T1 | 2026-08-28 |
| S-02 | What is the SQL analytics endpoint for a lakehouse? | https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-sql-analytics-endpoint | T1 | 2026-05-19 |
| S-03 | Copy and transform data in Dynamics 365 (Microsoft Dataverse) or Dynamics CRM | https://learn.microsoft.com/en-us/azure/data-factory/connector-dynamics-crm-office-365 | T1 | 2025-07-25 |
| S-04 | Use change tracking to synchronize data with external systems (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/use-change-tracking-synchronize-data-external-systems | T1 | 2026-03-31 |
| S-05 | Synchronize data across Dataverse environments using Power Platform | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/sync-dataverse-data | T1 | 2026-04-30 |
| S-06 | Dual-write overview | https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/dual-write/dual-write-overview | T1 | 2026-01-15 |
| S-07 | Service Bus Dead-Letter Queues | https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues | T1 | 2026-07-16 |
| S-08 | Data migration for Dynamics 365 implementation projects | https://learn.microsoft.com/en-us/dynamics365/guidance/resources/migrate-data | T1 | 2026-06-17 |
| S-09 | Manage configuration and migration data for Dynamics 365 projects | https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management-configuration-data-migration | T1 | 2024-01-17 |
| S-10 | Dual-write general troubleshooting | https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/dual-write/dual-write-troubleshooting | T1 | 2026-01-15 |
| S-11 | Enable table maps for dual-write | https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/dual-write/enable-entity-map | T1 | 2026-04-03 |
| S-12 | Use Dataverse background operations (reference architecture) | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/dataverse-background-operations | T1 | 2025-04-17 |
| S-13 | Build Resilient Data Sync Using Asynchronous Request-Reply | https://learn.microsoft.com/en-us/dynamics365/guidance/reference-architectures/sales-reliable-data-sync-asynchronous-request-reply | T1 | 2025-10-09 |
| S-14 | Cancel or resubmit flow runs in bulk in Power Automate | https://learn.microsoft.com/en-us/power-automate/how-tos-bulk-resubmit | T1 | 2026-04-21 |
| S-15 | Incremental refresh in Dataflow Gen2 | https://learn.microsoft.com/en-us/fabric/data-factory/dataflow-gen2-incremental-refresh | T1 | 2025-07-23 |
| S-16 | Query Azure Synapse Link for Dataverse data with serverless SQL pool | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-serverless | T1 | 2021-08-06 (stale) |
| S-17 | FAQ: exporting Dataverse table data to Azure Synapse Analytics and Azure Data Lake | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/export-data-lake-faq | T1 | 2026-09-01 |
| S-18 | Azure Synapse Link for Dataverse troubleshooting guide | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/azure-synapse-link-troubleshooting-guide | T1 | 2026-09-01 |
| S-19 | Synapse SQL external tables / shared-databases access control | https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/develop-tables-external-tables · https://learn.microsoft.com/en-us/azure/synapse-analytics/sql/shared-databases-access-control | T1 | n/d — **search summary only, NOT fetched verbatim** |

**Negative research performed (brief item 8).** Searched Microsoft-first for "sync drift", "dataflow refresh failure", "change tracking token expired", "dead letter". Microsoft publishes **no page using the term "sync drift"** for Dataverse. The closest first-party material is the Synapse Link FAQ divergence catalogue (`S-17` → SY-14) and the troubleshooting error table (`S-18` → SY-15). Change-tracking token expiry is documented only as an unnamed exception (`S-04`). Dead-lettering is well documented (`S-07`) but replay is a manual portal operation. Community threads (T4) exist on Synapse Link not syncing updates and on programmatic flow resubmission — recorded as signals only, not used as evidence.

---

### 12.8 Azure SQL store-choice sub-research (cite as `SQ2:Sxx`)


| id | Title | URL | ms.date | Tier |
|---|---|---|---|---|
| S1 | Customer-managed transparent data encryption (TDE) — Azure SQL Database & Managed Instance & Synapse | https://learn.microsoft.com/en-us/azure/azure-sql/database/transparent-data-encryption-byok-overview | 2026-06-02 | T1 MS |
| S2 | Long-Term Retention Backups — Azure SQL Database & Managed Instance | https://learn.microsoft.com/en-us/azure/azure-sql/database/long-term-retention-overview | 2026-03-06 | T1 MS |
| S3 | What is the Hyperscale service tier? — Azure SQL Database | https://learn.microsoft.com/en-us/azure/azure-sql/database/service-tier-hyperscale | 2026-05-19 | T1 MS |
| S4 | Understand Data Models — Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/data-guide/technology-choices/understand-data-store-models | 2025-08-21 | T1 MS |
| S5 | Single database vCore resource limits — Azure SQL Database | https://learn.microsoft.com/en-us/azure/azure-sql/database/resource-limits-vcore-single-databases | 2026-03-09 | T1 MS |
| S6 | Row-Level Security — SQL Server | https://learn.microsoft.com/en-us/sql/relational-databases/security/row-level-security | 2025-09-11 | T1 MS |
| S7 | Manage your customer-managed encryption key — Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/customer-managed-key | 2026-05-18 | T1 MS |
| S8 | Overview of Customer Key — Microsoft Purview | https://learn.microsoft.com/en-us/purview/customer-key-overview | 2025-02-03 | T1 MS |
| S9 | Set up Customer Key — Microsoft Purview | https://learn.microsoft.com/en-us/purview/customer-key-set-up | 2025-09-08 | T1 MS |
| S10 | SQL Server (connector reference) | https://learn.microsoft.com/en-us/connectors/sql/ | 2024-03-01 (page updated 2026-07-11) | T1 MS |
| S11 | Prerequisites for Minimal Logging in Bulk Import — SQL Server | https://learn.microsoft.com/en-us/sql/relational-databases/import-export/prerequisites-for-minimal-logging-in-bulk-import | 2025-09-07 | T1 MS |
| S12 | Data compression — SQL Server | https://learn.microsoft.com/en-us/sql/relational-databases/data-compression/data-compression | 2023-10-27 | T1 MS |
| S13 | Copy activity performance and scalability guide — ADF & Synapse | https://learn.microsoft.com/en-us/azure/data-factory/copy-activity-performance | 2025-07-25 | T1 MS |
| S14 | Data partitioning guidance — Azure Architecture Center | https://learn.microsoft.com/en-us/azure/architecture/best-practices/data-partitioning | 2022-07-25 | T1 MS |
| S15 | Use the SQL Server with canvas apps — Power Platform architecture | https://learn.microsoft.com/en-us/power-platform/architecture/reference-architectures/sqlserver-canvas-app | 2025-07-15 | T1 MS |

Note on S4/S14: the requested URL `…/data-guide/scenarios/time-series` no longer resolves to a time-series page — it redirects to *Get Started with Database Architecture Design* (ms.date 2026-03-05). The time-series guidance now lives in S4.

---

### 12.9 Business-volume/scale/concurrency sub-research (cite as `SC:Sxx`)


| id | Title | URL | ms.date | Tier |
|---|---|---|---|---|
| S1 | Requests limits and allocations — Power Platform | https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations | 2026-08-14 | T1 |
| S2 | Optimize data performance recommendation (PE:08) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/optimize-data-performance | 2025-08-15 | T1 |
| S3 | Elastic Tables for Developers | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/elastic-tables | 2026-08-04 | T1 |
| S4 | Optimize Performance for Bulk Operations: Best Practices | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/optimize-performance-create-update | 2026-03-26 | T1 |
| S5 | Limits of automated, scheduled, and instant flows | https://learn.microsoft.com/en-us/power-automate/limits-and-config | 2026-07-17 | T1 |
| S6 | Small data payloads in Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/small-data-payloads | 2023-12-01 | T1 |
| S7 | How to create performant Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview | 2026-08-20 | T1 |
| S8 | Optimized query data patterns in Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/optimized-query-data-patterns | 2023-12-01 | T1 |
| S9 | How server-side caching works in Power Pages | https://learn.microsoft.com/en-us/power-pages/admin/clear-server-side-cache | 2026-04-29 | T1 |
| S10 | Use SQL to query data (Microsoft Dataverse) | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/dataverse-sql-query | 2026-06-01 | T1 |
| S11 | Performance planning recommendation (PE:02) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/performance-planning | 2025-08-15 | T1 |
| S12 | Performance testing recommendation (PE:05) | https://learn.microsoft.com/en-us/power-platform/well-architected/performance-efficiency/performance-test | 2026-07-17 | T1 |
| S13 | Optimize performance using QueryExpression | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/org-service/queryexpression/optimize-performance | 2025-08-11 | T1 |
| S14 | Create and edit elastic tables | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-elastic-tables | 2025-03-31 | T1 |
| S15 | Send Parallel Requests to Dataverse | https://learn.microsoft.com/en-us/power-apps/developer/data-platform/send-parallel-requests | 2026-03-26 | T1 |
| S16 | Power BI modeling guidance for Power Platform | https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-modeling-guidance-for-power-platform | 2024-12-30 | T1 |

All 16 sources are Tier 1 (Microsoft Learn). No T2/T3/T4 material was used; no community signal was needed, and none is cited.
Not reachable: `/power-platform/well-architected/performance-efficiency/capacity-planning` returned **HTTP 404** — capacity planning lives at S11 (PE:02) instead.

---

### 12.10 Data quality / ownership vocabulary sub-research (cite as `DQ:Sxx`)


| id | Title | URL | Tier | ms.date | Notes |
|---|---|---|---|---|---|
| S1 | Manage your data in Dynamics 365 implementation projects | `https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management` | T1 | 2024-01-08 | **LIVE** — the main data chapter. `ai-usage: ai-assisted`, 1095-day update cycle |
| S2 | Checklist for data management and governance | `https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management-check-list` | T1 | 2024-01-18 | **LIVE** — the actionable checklist; six sections, no archiving section |
| S3 | Manage configuration and migration data for Dynamics 365 projects | `https://learn.microsoft.com/en-us/dynamics365/guidance/implementation-guide/data-management-configuration-data-migration` | T1 | 2024-01-17 | **LIVE** — migration chapter |
| S4 | Create a business rule in Microsoft Dataverse | `https://learn.microsoft.com/en-us/power-apps/maker/data-platform/data-platform-create-business-rule` | T1 | 2026-07-06 | Freshest source; contains the DQ-10 internal contradiction |
| S5 | Detect duplicate data using the Web API (Microsoft Dataverse) | `https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/manage-duplicate-detection-create-update` | T1 | 2022-12-31 | Oldest source; the off-by-default finding |
| S6 | Create a column in a list or library | `https://support.microsoft.com/en-us/sharepoint/lists/data-and-lists/create-a-column-in-a-list-or-library` | T1-weak | n/d | support.microsoft.com, no ms.date; column validation settings |
| S7 | Edit list settings | `https://support.microsoft.com/en-us/office/edit-list-settings-4d35793b-246e-42a3-990c-563a83795b7f` | T1-weak | n/d | List-level validation formula + user message |
| S8 | Dataverse as a master data system | `https://learn.microsoft.com/en-us/dynamics365/guidance/reference-architectures/dataverse-master-data-system` | T1 | 2025-11-04 | **LIVE** — reference architecture, canonical-model warning |
| S9 | Examples of common formulas in lists | `https://support.microsoft.com/en-us/office/examples-of-common-formulas-in-lists-d81f5f21-2b4e-45ce-b170-bf7ebf6988b3` | T1-weak | n/d | Calculated columns, NOT validation; source of the row-locality quote |
| S10 | Power Query SharePoint list connector | `https://learn.microsoft.com/en-us/power-query/connectors/sharepoint-list` | T1 | 2025-11-21 | Boolean TRUE/FALSE vs 1/0 defect |
| S11 | Create a semantic model from a SharePoint List | `https://learn.microsoft.com/en-us/power-bi/connect-data/create-dataset-sharepoint-online-list` | T1 | 2023-02-22 | 4-decimal limit; sensitivity label not inherited |
| S12 | Data Considerations for Microservices (Azure Architecture Center) | `https://learn.microsoft.com/en-us/azure/architecture/microservices/design/data-considerations` | T1 | 2022-07-26 | The only near-definition of "source of truth" found |
| S13 | Connect to and manage Microsoft Dataverse in Microsoft Purview | `https://learn.microsoft.com/en-us/purview/register-scan-dataverse` | T1 | 2026-02-02 | Purview Dataverse scan scope + limitations |

---

## 13. Summary (revised in v2)

**Strongest data architecture signals**
- Relational model with integrity, cascades, row/column security and field audit → Dataverse standard tables ("Dataverse is the preferred choice if you need more complex relational data"; new app + new storage → Dataverse, SQ2-15). Server-enforced business rules "regardless of the app" is now **Assumed, not Confirmed** pending one empirical test — see `DQ-10`.
- Data already in a system of record that owns it → keep it there; read-through (embedding / virtual table for uniform-security reference data, positively filtered, sub-1,000-row, narrow — `VT-17`) or one-way replicated subset keyed by the source id; never two masters (no product-grade bidirectional sync exists outside D365 F&O dual-write — `DQ-06`).
- Org-wide, cross-period historical, or aggregate/chart reporting over > 50k rows → analytical copy (Fabric link / Synapse Link / Power BI import) from day one; Dataverse built-in reporting is for "shorter periods of time" — **but note the 50k figure does not bound ordinary filtered reports**, which may span "beyond 50,000 rows" within the 5-minute window (`DA-03` revised).
- Documents as the record → SharePoint libraries (versions, labels, retention); documents attached to secured records → Dataverse file columns (row security, file meter). SharePoint/OneDrive **can** carry a customer-managed key via a dedicated DEP (`SQ2-10`, corrected in v2).
- Team-scoped app on seeded licences within 2 GB → Dataverse for Teams.
- **New in v2 — customer-managed encryption keys**: Azure SQL TDE/BYOK is genuinely STRONG and cheaper to reach than Dataverse CMK (no Managed-Environment/E5 gate; server/instance/database scoping) — but the key vault becomes a tier-0 availability dependency with a 30-minute recovery cliff (`SQ2-01`, `SQ2-02`, `SQ2-09`).
- **New in v2 — genuine dataset scale**: Azure SQL Hyperscale (10 GB–128 TB, autoscaling) is the concrete answer when a dataset exceeds Dataverse's unpublished practical envelope (`SQ2-07`, `SC-18`).

**Conditional signals**
- Canvas app over tables > 2,000 rows → delegable store + delegable formula subset (SharePoint narrowest; SQL partial; Dataverse broadest — the Dataverse delegation table is now cited directly, `SQ2` finding context / connection-common-data-service); proof with row limit = 1.
- All-or-nothing multi-row writes → change set / custom API / plug-in or SQL stored procedure; cross-system → saga with pivot and pending state.
- Per-user security on SQL → only Azure SQL + Entra Integrated explicit connections + RLS/DENY, internal users only; `SESSION_CONTEXT`-based RLS needs a middle tier the Power Platform connector does not provide (`SQ2-08`).
- High-ingest events → elastic tables (no transactions/joins; GA status unresolved) **or, per Microsoft's own data-store model guide, Azure Data Explorer/Eventhouse — not Azure SQL** (`SQ2-06`, corrected in v2).
- Retention "N years" → in Dataverse, long-term retention only with Managed Environments (~50% database saving, zero for files, irreversible); in Azure SQL, Long-Term Retention is **backup-only**, restorable as a new database, not a queryable archive — cheap online history requires partitioning + columnstore archival compression or export to a different store (`SQ2-04`, `SQ2-05`, `SQ2-14`, corrected in v2).
- Analytics via Fabric link → budget Dataverse database capacity for the replica; select tables explicitly; the auto-provisioned SQL analytics endpoint is a free, read-only T-SQL surface with 8 KB text truncation and a 150-item workspace ceiling (`SY-02`, `SY-03`, new in v2).
- Consuming a Fabric-computed insight back into an app → read-only OneLake virtual table (preview), ~1-hour freshness, silent row loss if the source key isn't genuinely unique (`VT-12`, `VT-14`, new in v2).
- Nightly bulk load into SQL → CONDITIONAL, not automatically strong: capped by log rate (50/96/100 MiB/s regardless of vCores), minimal logging needs TABLOCK + empty target + no replication, no vendor throughput guarantee, and the Power Platform SQL connector cannot bulk-load at all — a separate ADF/bcp toolchain is implied (`SQ2-07`, `SQ2-12`, `SQ2-13`, corrected in v2).
- On-prem SQL → gateway estate (≥ 2 nodes per cluster, dev + prod clusters) and 2 MB / 8 MB / 110-s caps, or Azure SQL + VNet (Managed Instance excludes SQL Authentication for its hostname shape — `SQ2-11`, new in v2).
- Private connectivity → VNet-enabled environments (Azure subscription, paired regions, V2-only actions; SharePoint excluded).
- EU Data Boundary → all environments in macro region "EU and EFTA" + EU billing; country-level only with Advanced Data Residency.
- Freshness → mechanism floors: live read-through; events/queue (minutes, but dead-letter queues do not self-drain — `SY-09`); dataflows ≥ 30 min / ≤ 48 per day (replace-only, no deletes — `SY-13`); Fabric/Synapse ≤ 1 h; Power Pages cache 15 min, non-tunable (`SC-14`).
- Dataverse→writable-SQL read model → CONDITIONAL only, and only via a customer-built pipeline (ADF/Fabric Data Factory or Dataflow Gen2 incremental refresh); no managed service exists; deletes require a separate mechanism (`SY-01`, `SY-04`, `SY-13`, `SY-18`, new in v2).
- Cross-environment master data for canvas apps → CONDITIONAL: reads work via explicit environment selection; relationships/joins/cascades do not (`DA-25` revised, new in v2).

**Poor-fit conditions**
- SharePoint list as relational system of record: 5,000 LVT "can't be changed", 12 joins, `Not`/ID-range/complex-column non-delegation, ≤ 5,000 unique scopes, no column security, no transactions, last writer wins, outside solutions, collaboration-site governance.
- Excel with more than one writer or > 2,000 rows.
- Dataverse as the reporting warehouse or as the target for replicating the whole ERP / closed history.
- Virtual tables as a general integration layer for large or write-required external data (no performance/throughput/pushdown documentation at any volume — `VT-09`, new negative finding in v2); as a parent (1-side) of a relationship (`VT-06`); with negative-filter searches (paging corrupts beyond page 1 — `VT-04`).
- Azure SQL as a cheap cold-storage tier, or as the default answer for high-ingest telemetry (both corrected/contradicted in v2 — `SQ2-05`, `SQ2-06`).
- Strict cross-system consistency that cannot tolerate temporary inconsistency; distributed multi-primary writes; no cloud transit of row data; country-level residency without ADR.
- Organization-owned tables for data that may ever need segmentation; BUs mirroring a volatile org chart.
- Backups/recycle bin as archive; long-term retention as a file-cost remedy; "audit everything forever".
- **New in v2:** trusting row counts to detect Synapse Link/Fabric-link replica drift (≥ 8 documented silent-divergence modes — `SY-14`); treating flow-run resubmission as a reconciliation strategy (20-run batches, connector-API-capped, no dedupe — `SY-12`); relying on duplicate detection to protect integration/ETL writes (suppressed by default on Web API updates — `DQ-12`).

**Decision criteria (observable, per entity/interface)**
- Rows per queried table and growth; query shape (negations, sorts, free-text, aggregates); relationship count and cascade needs; atomic write groups; concurrent editors; freshness SLA and outage tolerance; owner per entity and field; view-only vs data; binary volume and lossless originals; audit fields/years and read-audit; retention years, legal hold, erasure; reporting scope and security-in-reports; sensitivity matrix (row/column); residency regime and AI processing; on-prem vs cloud location; private-network mandate; environment/organisational boundaries and re-org volatility; seeded-only licence constraint; SQL schema hygiene (PKs, triggers, types); steward availability; **new in v2:** peak (not average) business-event volume per event type, for the write-amplification pilot (`SC-21`); which single interface genuinely needs sub-15-minute freshness (`SC-14`); whether the read model needs writes at all (`SY-18`); whether the hardest validation rule in the set is cross-row/cross-entity (no declarative option exists in any store — `DQ-13`).

**Important constraints**
- Delegation 500/2,000 truncation; aggregate-query/chart 50,000 ceiling (precisely scoped in v2 — not a flat report ceiling, `DA-03`); 5,000-row pages; 5-min report/TDS timeouts (2 min with joins); service protection 6,000 / 20 min / 52 per user per web server per 5 min (52 is a default that "might be higher" — `SC-19`); daily request entitlements; capacity meters with one-way borrowing ($40 DB / $2 File / $10 Log per GB add-on); ownership type immutable; one parental relationship per child; rollups async (≥ 1 h; 50/table); formula columns unsortable across tables; column type/name immutable; file column ≤ 131 MB, images → JPG; Dataverse search 1,000 fields; audit retention non-retroactive, Forever default; LTR Managed Env + irreversible; backups ≤ 28 d; Fabric replica on database meter, ≤ 60 min, one workspace per environment, ≤ 2,000 active tables (`VT-15`); Synapse Link needs change tracking, same region/tenant, no exfiltration-protected workspaces, ≤ 10 profiles; virtual tables organization-owned, 1,000 rows (SQL, scoped to 1:N/polymorphic queries — corrected in v2), no audit/keys/search/offline, no vendor performance data at any volume (`VT-09`); alternate keys ≤ 10/table, not on secured columns; duplicate detection 5 rules/table, **suppressed by default on Web API updates** (`DQ-12`, new in v2); dataflows 48/day, single owner, no deletes/status; change-tracking deltas expire (7 d default), tokenless re-seed excludes deletes (`SY-06`); SQL connector Premium, 100 CRUD/10 s, 125 concurrent, 110 s, PK/trigger/type rules; Azure SQL log-rate ceiling 50/96/100 MiB/s regardless of vCores, 30,000 max concurrent sessions (`SQ2-07`, new in v2); gateway 2 MB/8 MB, SP degradation, ≥ 2 nodes; VNet: Azure subscription, paired regions, V2-only, no gateway, no SharePoint; SharePoint 30M items / 5,000 LVT / 12 joins / 8,000 bytes / 50,000–5,000 scopes / 600 calls per min; Excel 25 MB / 6-min lock / 100 calls per min; Managed Environments gate; CMK/Lockbox/IP firewall E5-class; SharePoint/OneDrive Customer Key tenant/geo-granularity only (`SQ2-10`, corrected in v2); EUDB dual condition; global schema-name replication; Copilot flex routing default on for new tenants; no first-party Dataverse→Azure SQL replication service (`SY-01`, new in v2); no published concurrent-user ceiling anywhere (`SC-16`, new in v2); no published Dataverse standard-table row ceiling (`SC-18`, new in v2).

**Anti-patterns** — §5 (DAP-1..DAP-44, 15 new in v2): licence-driven SharePoint/Excel stores; Dataverse as warehouse; replicating the ERP; two-way sync without ownership map; nightly bulk; sync webhooks for side effects; sequential `Patch` as transaction; virtual tables for governed data; sharing/parental relationships by default; organization-owned tables for segmentable data; BUs = org chart; unscoped audit; backups as archive; LTR for files; default-all Fabric link; embedded Power BI "inherits" security; implicit SQL connections; per-row SQL loops; unaudited legacy schema; single gateway node; collections as data layer; caching volatile/sensitive values; choices for ERP lists; elastic for transactional; throttled query shapes; sensitive schema names / previews in production; cascading retries; append-only lake under erasure duties; **new in v2:** assuming a Dataverse→SQL replication service exists; trusting row counts for drift detection; snapshot (not id) payloads in sync messages; flow-resubmission as reconciliation; virtual tables as a general integration layer; negative-filter search over virtual tables; SQL for telemetry; SQL LTR as a queryable archive; shared-connection SQL RLS; unverified duplicate-detection reliance on integration paths; unverified business-rule server-side enforcement; quoting a concurrent-user ceiling; inventing a write-amplification multiplier; "SharePoint can't do CMK"; `DateOnly` business rules assuming local time zone.

**Alternatives** — §6: Dataverse; SQL/Azure SQL alongside Dataverse (repositioned in v2: strong for CMK, scale >4 TB, engine control; NOT strong for telemetry or cheap archival); Azure Data Explorer/Eventhouse for genuine high-ingest telemetry (new alternative, v2); SharePoint for documents and flat trackers (now including CMK-covered content, v2); Dataverse for Teams; external system kept as system of record (embed / virtual table, now volume-uncharacterised / read-only replica); hybrid (operational subset + queue back; OLTP + lake, now with the free read-only SQL-analytics-endpoint path named, v2; relational + elastic; records + labelled documents; references + Blob); other technology when strong cross-system consistency, no cloud transit, multi-primary writes, country-level residency without ADR, or sub-15-minute cross-system reporting are mandatory.

**Unknowns** — §8 (U-01..U-41, 15 new in v2; several v1 unknowns closed): Fabric replica magnitude; elastic GA/alternate keys; SharePoint indexed-column max; SQL connector locking; recycle-bin GA; support-created indexes; gateway throughput; VNet ↔ Managed Environments (still open); Data Life Cycle Config deletion scope; D365 capacity uplift on Learn; EUR/EA pricing; current polling intervals; LTR read limits; CMK × Synapse/Fabric; flow run history vs capacity; column/row/table hard limits; SharePoint/Blob prices; **closed in v2:** cross-environment reads (confirmed supported), explicit no-write-back for Synapse/Fabric (confirmed: read-only), "system of record" vs "source of truth" vocabulary (confirmed: used loosely, no formal distinction); **new in v2:** standard-table cross-session read-after-write guarantee; standard-table read replicas; audit request-cost quantification; Dataverse standard-table row ceiling; concurrent-user ceiling; Power Automate transition-period end date; service-protection concurrency-default variance; model-driven client caching; Azure SQL Database recovery-model support for minimal logging; Stretch Database deprecation status; `SESSION_CONTEXT` reachability from the SQL connector; Fabric Mirroring source-list evolution; Synapse/Fabric-link table-resync cost; **whether business rules enforce on Web API writes — the single highest-value unresolved test in the entire corpus (`DQ-10`, U-40)**; whether Microsoft ever states "don't migrate history".

---

## Gaps Fixed

Numbered against the adversarial review (`data-architecture-review.md`), findings F-01..F-19.

1. **F-01 (HIGH) — five unsourced store-fit-matrix cells.** Fixed with 16 new findings (`SQ2-01`..`SQ2-16`). Verdicts: customer-managed keys for Azure SQL — SUPPORTED with conditions (`SQ2-01`, `SQ2-02`, `SQ2-09`); cheap long retention for Azure SQL — CONTRADICTED as stated, CONDITIONAL when restated (`SQ2-04`, `SQ2-05`, `SQ2-14`); high-ingest telemetry for Azure SQL — CONTRADICTED by Microsoft's own data-store model guide (`SQ2-06`, `SQ2-07`); nightly bulk load for Azure SQL — CONDITIONAL, not STRONG (`SQ2-12`, `SQ2-13`); SharePoint/M365 "POOR for CMK" — WRONG, Customer Key covers SharePoint via a dedicated DEP (`SQ2-10`). Every §2 matrix cell now carries an explicit origin tag.
2. **F-02 (HIGH) — cross-environment reads contradicted by a Microsoft page.** Fixed: `DA-25` rewritten to distinguish cross-environment *reads* (supported, per the canvas "Change environment" capability) from cross-environment *relationships/joins/cascades* (not supported, never were). §2 gained a new row (27) and §3 gained a corrected boundary bullet.
3. **F-03 (HIGH) — virtual-table volume viability uncharacterised.** Fixed with 17 new findings (`VT-01`..`VT-17`), closing with an explicit negative finding that Microsoft publishes no performance/latency/throughput/caching/pushdown characterisation for virtual tables at any volume (`VT-09`) and a full appropriate/not-appropriate decision ladder (`VT-17`). `DA-45`'s 1,000-record quote is corrected to its documented scope (1:N/polymorphic relationships only).
4. **F-04 (HIGH) — no Dataverse→Azure SQL replication path evidenced.** Fixed with 18 new findings (`SY-01`..`SY-18`). `SY-01` is a hard negative finding (Dataverse is absent from the enumerated Fabric Mirroring source list). `SY-18` synthesises the three real paths (Link to Fabric + SQL analytics endpoint; Synapse Link + serverless SQL; customer-built ADF/Dataflow-Gen2 pipeline) and their reconciliation cost — only the third reaches a writable Azure SQL Database, and it is the only one that does not propagate deletes.
5. **F-05 (HIGH) — transaction volume handled only as raw API limits, no business-to-platform translation.** Fixed with `SC-01`, `SC-02` and the dedicated synthesis `SC-21`, which supplies the translation structure (`requests(e) = volume(e) × A_client × A_server × A_retry × A_page`) with every multiplier explicitly marked as an engagement-measured input, never a published figure — following the brief's instruction not to invent thresholds.
6. **F-06 (MEDIUM, gated as blocking) — 50,000-row limit over-generalised.** Fixed: `DA-03` revised to scope the figure precisely (FetchXML/OData aggregates; model-driven charts/dashboard grids; canvas aggregate functions) and to quote Microsoft's own statement that ordinary filtered reports "are allowed to span large datasets that are beyond 50,000 rows" within the 5-minute window.
7. **F-07 (MEDIUM) — Dataverse strengths argued by positioning, not comparative evidence.** Fixed: the Dataverse delegation table (connection-common-data-service) is now cited directly in §6 and compared against SQL's and SharePoint's; "server-enforced rules regardless of the app" is explicitly downgraded to Assumed pending `DQ-10`'s resolution.
8. **F-08 (MEDIUM) — reconciliation and drift repair thin.** Fixed with 18 new findings (`SY-06`..`SY-17`): change-tracking re-seed mechanics and its delete-exclusion trap (`SY-06`); Microsoft's own Dataverse-to-Dataverse sync reference architecture, whose reconciliation mechanism is a scheduled full-scan upsert (`SY-07`); dual-write as the existence proof of what real bidirectional sync requires (`SY-08`); Service Bus dead-letter mechanics and the fact that nothing auto-drains it (`SY-09`); Microsoft's resilient-sync reference pattern (re-fetch current state at send time, never ship a snapshot) (`SY-10`); and, most load-bearing, the Synapse Link FAQ's catalogue of ≥ 8 silent-divergence modes that all report sync success (`SY-14`).
9. **F-09 (MEDIUM) — read/write workload shape and concurrency light.** Fixed with `SC-06` (explicit standard-vs-elastic consistency contract), `SC-11`..`SC-13` (PE:08 read/write doctrine: server-side views, avoid N+1, optimize updates, deliberate denormalisation as a negotiated freshness trade-off), and the explicit negative finding + resolution pair `SC-16`/`SC-17` (no concurrent-user ceiling published anywhere; the answer is a load test, not a number).
10. **F-10 (MEDIUM) — data quality coverage limited to keys and duplicate rules.** Fixed with 18 new findings (`DQ-01`..`DQ-18`). The prior pass's 404s on the D365 Implementation Guide are resolved — the chapters are alive under a corrected URL shape (`DQ-01`). New material includes the genuine self-contradiction in Microsoft's business-rules documentation (`DQ-10`), the high-impact finding that duplicate detection is suppressed by default on Web API updates (`DQ-12`), and a precise validation-per-store enforcement ladder (`DQ-13`).
11. **F-11 (MEDIUM) — "system of record" vs "source of truth" left undefined.** Fixed: `DQ-03` confirms the D365 Implementation Guide never formally distinguishes the terms (using "primary data"/"master data source" instead); `DQ-15` finds the closest thing to a Microsoft definition in the Azure Architecture Center's microservices guidance, which ties "source of truth" to a per-entity *consistency requirement*, not to Power Platform. Conclusion: the pack must declare its own vocabulary as pack-local and never cite Microsoft as the authority for a formal distinction.
12. **F-12 (MEDIUM) — SharePoint concurrency Q&A mis-attributed; support-page paraphrases presented as quotes.** Fixed: the answerer is corrected from "Microsoft moderator" to "Ling Zhou_MSFT (Microsoft External Staff)" in `DA-08`. The underlying support.microsoft.com sources (`SP:S-06`, `SP:S-07`, `SP:S-09` and others) remain flagged as weaker evidence in §10, consistent with the review's concern; full re-fetch of every such page was out of scope for this targeted revision (see Gaps Still Open).
13. **F-13 (MEDIUM) — consuming Fabric/analytical outputs back into apps unevidenced.** Fixed with `VT-12` (Fabric OneLake virtual tables are explicitly read-only, with a silent-row-loss trap on non-unique keys), `VT-13` (no write-back path anywhere in Link to Fabric or Synapse Link — the lake side is explicitly off-limits for customer modification), `VT-14` (≈1-hour round-trip freshness), and `VT-16` (the OneLake virtual table is the *only* documented maker-side consumption route; a SQL-analytics-endpoint connector route is undocumented and must be treated as unverified).
14. **F-15 (LOW) — SQL Managed Instance connector specifics dropped.** Fixed: `SQ2-11` restores and extends the finding — SQL Authentication is unsupported for MI hostnames, Entra connections exclude guest users, managed identity is Logic-Apps-only, and VNet-linked environments shrink the connector to eight actions with no gateway.
15. **F-16 (LOW) — D365 Implementation Guide framing not caveated.** Partially addressed: `DQ-01` notes the IG content is `ai-usage: ai-assisted` on a 1095-day (3-year) refresh cycle — guidance, not spec — and this caveat is now carried in the header and in `DQ-01`/`DQ-18`.
16. **F-17 (LOW) — standard-table consistency model never stated.** Fixed: `SC-06` makes the choice criterion and substrate explicit ("Use standard tables … Your application requires strong data consistency" / "A standard table stores data using Azure SQL. Standard tables provide transaction support"), alongside the two documented staleness exceptions carried in `SC-12` (`CountRows` cached value) and `SC-14` (Power Pages 15-minute cache).
17. **F-18 (LOW) — file size / duplicated sub-registers.** Not addressed in this revision (explicitly out of scope — see Gaps Still Open). The v2 file is larger, not smaller; deduplicating the source registers is a housekeeping pass better done once the gate has run and no further content churn is expected.
18. **F-19 (LOW) — optimistic confidence grading in two places.** Addressed for `DA-03` (now HIGH for the limits, explicitly scoped for the reporting-precision claim) via the revision itself; the general recommendation to keep §3 boundary confidence no higher than the underlying finding's grade is restated in the gate conditions (§11, item 1).

---

## Gaps Still Open

- **F-12 residual** — the SharePoint support.microsoft.com pages flagged by the review (`SP:S-06`, `SP:S-07`, `SP:S-09`, and siblings) were not individually re-fetched and re-verified verbatim in this pass; they remain in §10's "weaker evidence" list. A full re-fetch pass is a bounded, low-risk task for the next revision or for the gate itself.
- **F-18** — the source register remains split across ten sub-registers (five from v1, five new in v2) rather than deduplicated into one canonical list. Traceability is intact (every quote cites its sub-register id) but a pack author will need to check multiple tables for the same URL in a few cases (e.g. the Synapse Link FAQ appears in both `XC` and `SY`/`VT` sub-registers under different local ids for the same URL).
- **U-40 (new, HIGH-value)** — whether entity-scoped business rules execute server-side on Web API/integration writes is a genuine, unresolved contradiction inside Microsoft's own documentation (`DQ-10`). This is flagged, not resolved, because it requires an empirical test in a live environment, which is out of scope for a documentation-based research pass. **This is the single highest-priority follow-up before pack authoring encodes any rule assuming server-side business-rule enforcement.**
- **U-13 residual** — per-provider virtual-table write support for Snowflake, PostgreSQL, Databricks, Salesforce and Oracle (as distinct from SQL Server, SharePoint and Excel, which are documented) was not individually fetched; `VT-02` establishes the *pattern* (deferred to each connector's own reference page) but not the specific matrix.
- **U-01/U-02 (elastic tables)** — GA status and alternate-key support for elastic tables remain conflicting between two Microsoft pages of different dates (`C-02`, `C-03`); not resolved by this pass, which added no new elastic-table-specific fetches beyond what v1 already had.
- **U-10 (VNet ↔ Managed Environments)** — still open; not targeted by any of the five v2 sub-researches.
- **DQ-16 residual (Purview capability matrix)** — v1/v2 confirm Purview-over-Dataverse is metadata-only, but the comparative capability matrix against SharePoint/Azure SQL sources (classification, labels, lineage) was not fetched (`DQ` U-07).
- **No adversarial review or gate has run on v2 itself.** All the corrections above should be treated as a first-pass fix, not a validated final state, until v2 is itself reviewed.

---

## Strongest Decision Boundaries

The ten boundaries below are the ones most likely to change an architecture decision, ranked by how often they recur across the requirement space aisa will encounter. Each restates requirement → constraint → architectural implication → trade-off → when the recommendation changes, per the brief's instruction.

1. **Relational integrity + row/column security, at any real volume.**
   *Requirement:* several related entities with referential integrity, and access must differ by owner/team/role, at a volume that will exceed a few thousand rows.
   *Constraint:* SharePoint fails at 12 joins/view and ≤ 5,000 recommended unique-permission scopes with no column security; Excel is capped at ~2,000 delegable rows with no multi-user write safety; Dataverse offers the broadest delegation table, BU/role/column security, and alternate-key uniqueness (DA-39, DA-42, SP delegation table vs Dataverse delegation table, DA-11, DA-12).
   *Architecture:* Dataverse standard tables, user/team-owned, with the row/column security model decided **before** the table is created (immutable after).
   *Trade-off:* premium licensing for every user; POA/sharing growth if per-record collaboration is modelled carelessly (DA-11).
   *Changes when:* the data already lives in an existing SQL system that can't be moved (→ SQL, with schema conformance and Entra-Integrated identity, `SQ2-15`), or the requirement is genuinely document-centric with only light metadata (→ SharePoint).

2. **All-or-nothing multi-row writes (transactions).**
   *Requirement:* header + lines, stock movements, financial postings that must succeed or fail together.
   *Constraint:* Power Fx is never transactional, even within one store (DA-07, `EX:S52`/`EX:S53`); across systems there is no distributed transaction, only compensation.
   *Architecture:* Dataverse change set / custom API / synchronous plug-in within Dataverse; SQL stored procedure within SQL; a saga with an explicit pivot (the irreversible step last) and pending state across systems (DA-52).
   *Trade-off:* pro-code investment (plug-ins, stored procedures) versus accepting partial-failure risk.
   *Changes when:* the "transaction" is actually a single Dataverse write with denormalised fields — then no special mechanism is needed.

3. **Reporting/analytics scope: operational vs historical/org-wide.**
   *Requirement:* dashboards, KPIs, trend/YoY analysis, or any query touching more than a filtered, time-boxed slice.
   *Constraint:* Dataverse's aggregate/chart ceiling is 50,000 rows and TDS/report queries time out at 5 (or 2) minutes — but this does **not** flatly block large filtered reports, only aggregates and charts (`DA-03` revised, closing review F-06).
   *Architecture:* per-user, time-boxed, non-aggregate reporting can stay in-platform; aggregate, cross-period, or org-wide reporting needs an analytical copy — Fabric link (free within Dataverse, but the replica bills as *database* storage, `DA-19`) or Synapse Link (customer-owned ADLS, more divergence risk but full Azure-side control, `SY-14`) or Power BI import.
   *Trade-off:* Fabric link's "no copy" claim is a billed replica inside Dataverse-managed storage, not actually free (`C-06`); Synapse Link's replica can silently diverge (`SY-14`) while reporting success.
   *Changes when:* the requirement is genuinely real-time AND must respect Dataverse's own row/column security — then DirectQuery is the (slow, ~20,000-row-guided) answer, not a copy (`SC-20`).

4. **Data must remain in an existing system of record.**
   *Requirement:* an ERP, legacy system, or other application already owns the entity.
   *Constraint:* virtual tables give a read-through (occasionally read/write) surface without replication, but forfeit row security, audit, search, offline, rollups, and — closed as a hard negative finding in v2 — carry **no published performance/latency/throughput characterisation at any volume** (`VT-09`).
   *Architecture:* virtual table for narrow, positively-filtered, sub-1,000-row, read-mostly reference data with uniform security tolerance (`VT-17`); replicate a subset one-way, keyed by the source id with an alternate key, for anything needing audit/security/offline/relationships (DA-45, DA-53).
   *Trade-off:* virtual tables avoid duplication but inherit the source's live latency on every render, with zero platform-side caching documented; replication duplicates data and needs a reconciliation job.
   *Changes when:* the volume/latency requirement is unknown — then a measured spike against production-like data is mandatory before either path is committed to (`VT-09`, `VT-17`).

5. **A relational read model must be built from Dataverse into a warehouse/SQL store.**
   *Requirement:* "we need a SQL/Power BI/warehouse copy of Dataverse data."
   *Constraint:* **there is no first-party managed Dataverse→Azure SQL Database replication service** — Dataverse is absent from the Fabric Mirroring source list, Synapse Link targets ADLS, Link to Fabric targets OneLake, and Data Export Service is retired (`SY-01`, a hard negative finding).
   *Architecture:* if no writes are needed, Link to Fabric's auto-provisioned SQL analytics endpoint is free and lowest-reconciliation-burden (`SY-02`); if writes are needed, a customer-built ADF/Fabric Data Factory pipeline or Dataflow Gen2 incremental refresh reaches a writable Azure SQL Database, but neither propagates deletes and both need a hand-built watermark and reconciliation job (`SY-04`, `SY-13`, `SY-18`).
   *Trade-off:* the two managed paths (Fabric link, Synapse Link) handle deletes and cost nothing extra in engineering, but are read-only; the only path reaching a writable SQL store is the one that does not handle deletes and costs the most in reconciliation engineering.
   *Changes when:* the requirement is purely reporting (no writes) — always prefer the managed path.

6. **System of record / ownership for a shared entity.**
   *Requirement:* an entity (customer, product, account) is used by more than one system.
   *Constraint:* ownership is decided **per entity AND per field** (Sales owns name/contact, Finance owns credit limit — `EX:S06`); Microsoft's only near-definition of "source of truth" ties it to a *consistency requirement*, not to a fixed authority (`DQ-15`); no product-grade bidirectional sync tooling exists outside D365 F&O dual-write (`DQ-06`).
   *Architecture:* one-way sync per field from its owner; bidirectional only with an explicit per-field conflict map and — if genuinely required — the operational machinery dual-write demonstrates is necessary (alternate keys, conflict master, pause/catch-up, dedicated error tables — `SY-08`).
   *Trade-off:* one-way sync means the non-owning side cannot always be made read-only for users, causing UX confusion; bidirectional sync costs conflict-resolution engineering that scales with the number of shared fields.
   *Changes when:* eventual consistency is acceptable for the consumer — then the "source of truth" question does not need a hard single answer at all, and replicated read copies are legitimate (`DQ-15`).

7. **Business volume must be translated into a platform request/throughput budget.**
   *Requirement:* "N transactions/day" stated as a business number.
   *Constraint:* Dataverse counts CRUD, assign, share, "internal system requests required to complete CRUD transactions", plug-ins, classic workflows, retries and pagination — but the amplification factor from one business transaction to N platform requests is a property of each solution's own customisation and is never published by Microsoft (`SC-01`, `SC-02`, `SC-21`).
   *Architecture:* the translation must be measured per engagement (Application Insights for Dataverse; flow Analytics → Actions tab), never assumed from a rule of thumb; four independent budgets must each be checked (daily entitlement per identity; service protection per user per web server; flow throughput per profile; flow content-byte throughput) because they do not pool (`SC-21`).
   *Trade-off:* a measured pilot costs time before the estimate can be finalised; skipping it risks discovering the real multiplier in production.
   *Changes when:* the automation is owned by a Process-licensed flow or a client application calling Dataverse directly rather than a per-user-licensed flow — this removes the single-identity bottleneck that is the most common real-world failure mode (`SC-05`).

8. **Concurrency and "will it scale?"**
   *Requirement:* N concurrent users at peak.
   *Constraint:* **no Microsoft page publishes a concurrent-user ceiling for any Dataverse/Power Apps surface** — the governing limits are per-authenticated-user (service protection) and per-identity-per-24-hours (entitlements), so concurrency scales with users almost by construction; the real ceilings appear at *shared* identities, *shared* rows, and *shared* automation (`SC-16`).
   *Architecture:* identify every funnel point where many users' traffic collapses onto one identity, one row, or one flow, and size/test those specifically; answer the concurrency question with a load test against a production-like environment (PE:05) using realistic personas and peak scenarios, never with a quoted number (`SC-17`).
   *Trade-off:* a proper load test costs a dedicated environment, realistic (scrubbed) data, and an APM tool — genuine project cost, not optional.
   *Changes when:* it doesn't — this boundary applies to every engagement regardless of scale, because the absence of a published ceiling is universal.

9. **Data quality / validation must hold regardless of entry channel.**
   *Requirement:* a rule (uniqueness, required value, cross-field check) must be enforced whether the record is created via app, API, or integration.
   *Constraint:* only **table-scoped** business rules reach beyond the model-driven client, and even that is contradicted on the same Microsoft page (`DQ-09`, `DQ-10`); duplicate detection is suppressed by default on Web API updates and has default rules only for accounts/contacts/leads (`DQ-12`); SharePoint validation is row-local, single-column, and cannot express referential or cross-row rules (`DQ-13`).
   *Architecture:* alternate keys (not duplicate detection) for any uniqueness that must hold on integration paths (`DQ-17`); a plug-in or custom API for any rule that must be provably server-side; SharePoint acceptable only for single-row, single-column validation.
   *Trade-off:* crossing from "business rule" to "plug-in" is a genuine cost and skills-profile change that should be identified in Discovery, not discovered during build (`DQ-11`).
   *Changes when:* the empirical test in `DQ-10`/U-40 confirms entity-scoped business rules do execute reliably server-side on the target environment — this would upgrade the confidence of the whole boundary from Assumed to Confirmed, but must not be assumed in advance.

10. **Customer-managed encryption keys / "who can access our data".**
    *Requirement:* the customer must control (and be able to revoke) the encryption key.
    *Constraint:* Azure SQL TDE/BYOK is genuinely strong and reachable with only an Azure subscription (no Managed-Environment/E5 licensing gate), scoped to server/instance/database, but the key vault becomes a tier-0 availability dependency with a 30-minute recovery cliff (`SQ2-01`, `SQ2-02`). Dataverse CMK requires Managed Environments plus an E5-class compliance SKU for every user in the environment and a multi-day switch-on window, with several artefacts (connector settings, environment metadata) staying Microsoft-managed regardless (`SQ2-09`). SharePoint/OneDrive **is** covered, via a dedicated Customer Key DEP — the real limitation is tenant/geo granularity, not absence (`SQ2-10`, corrected in v2).
    *Architecture:* in a tenant without E5-class licensing, this is a genuine, quotable argument for putting the regulated data in Azure SQL rather than Dataverse — accepting SQL's premium-connector and per-user-identity costs in exchange.
    *Trade-off:* Azure SQL CMK's operational simplicity is offset by the key-vault-as-availability-dependency risk; Dataverse CMK's operational complexity is offset by staying inside the platform's native security/audit model.
    *Changes when:* the tenant already holds E5-class licensing for unrelated reasons — then the marginal cost of Dataverse CMK drops sharply and the decision reverts to whichever store best fits the other requirements.

---

## New Constraints

The following constraints did not exist, or existed only as a v1 assertion, before this v2 revision. Each is sourced.

- **No first-party Dataverse→Azure SQL Database replication service exists** (`SY-01`) — Dataverse is absent from the Fabric Mirroring source list.
- **Fabric/Synapse-linked SQL surfaces are read-only** — the lakehouse SQL analytics endpoint "operates in read-only mode over Delta tables" (`SY-02`); Synapse serverless SQL over the exported lake is likewise read-only, consumption-priced (`SY-16`).
- **Replica drift is silent on Synapse Link/Fabric link** — at least 8 documented modes (secured columns export null, calculated columns freeze, direct-SQL deletes never propagate, new columns don't sync until a data change occurs, type changes permanently break sync) all report success (`SY-14`).
- **Dead-letter queues do not self-drain** — no TTL, no automatic cleanup; replay is a manual portal action (`SY-09`).
- **Change-tracking tokenless re-seed excludes deletes** — "Deleted objects aren't returned" (`SY-06`); an outage longer than the expiry window (default 7 days) is a re-seed event that loses delete information.
- **Power Automate flow-run resubmission is capped at 20 runs per batch**, bounded further by connector API limits, with no duplicate protection (`SY-12`).
- **Virtual tables have no published performance/latency/throughput/caching/pushdown characterisation at any volume** — a hard negative finding, not an assumption (`VT-09`).
- **Virtual tables always return every column** — "Selecting attributes ... won't be applied since all attributes are returned" (`VT-05`); row count is the only controllable payload dimension.
- **A virtual table can never be the "1" side of a 1:N relationship**, and two virtual tables cannot relate many-to-one to each other (`VT-06`).
- **Negative filter operators corrupt virtual-table paging beyond page 1**, with "no supported workaround" (`VT-04`).
- **Fabric OneLake virtual tables are read-only**, preview, and silently drop records if the chosen key isn't genuinely unique (`VT-12`).
- **Azure SQL Long-Term Retention is backup retention, not a queryable archive** — restorable only as a new database, up to 10 years, with no customer control over backup timing (`SQ2-04`).
- **No cold/cheap storage tier exists for Azure SQL Database rows** — old rows cost the same per GB as new ones; cheapness requires partitioning + columnstore archival compression or export (`SQ2-05`, `SQ2-14`).
- **Azure SQL sustained write throughput is capped by log rate, not by vCores** — 50 MiB/s (General Purpose), 96 (Business Critical), 100 (Hyperscale), flat regardless of compute tier (`SQ2-07`).
- **Azure SQL Managed Instance excludes SQL Authentication for its hostname shape**, forcing Entra-based auth, which itself excludes guest users (`SQ2-11`).
- **Row-level security via `SESSION_CONTEXT` needs a middle tier that the Power Platform SQL connector does not provide** — a shared/implicit connection collapses `USER_NAME()`-based RLS to one principal (`SQ2-08`).
- **Dataverse request accounting includes internal system requests, retries, and pagination** — one business save can fan out into an unmeasured multiple of platform requests, and the multiplier is a property of the customisation, not the platform (`SC-01`, `SC-02`).
- **The Power Platform Requests licensing report excludes Dataverse and Power Apps traffic** — it is preview and currently limited to Power Automate (`SC-03`).
- **No concurrent-user ceiling is published for any Dataverse/Power Apps surface** (`SC-16`).
- **No maximum row count/size is published for a Dataverse standard table** — only elastic tables carry a scale claim (`SC-18`).
- **`CountRows` on a Dataverse table is a periodically-computed cached value, not a live count** — exact counts require `CountIf`, capped at 50,000 (`SC-12`).
- **Power Pages caches at a non-tunable 15-minute SLA**, and writes made outside the page (plug-in, flow) are "never guaranteed to be immediate" on the site (`SC-14`).
- **DirectQuery over Dataverse is guided to ~20,000 rows and hard-capped at a 10-minute query timeout**, and shares the operational service-protection budget (`SC-15`, `SC-20`).
- **Duplicate detection is suppressed by default on Web API updates**, and Dataverse ships default rules only for accounts, contacts and leads (`DQ-12`).
- **Only table-scoped (not form-scoped) business rules can reach beyond the model-driven client**, and even that is internally contradicted in Microsoft's own documentation (`DQ-09`, `DQ-10`).
- **Business rules cannot validate multi-select choice, File or Language columns**, silently no-op if the referenced field is not on the form, and are capped at 150 per table (`DQ-11`).
- **SharePoint/OneDrive Customer Key exists but at tenant/geo granularity only** — not scopeable to a site, library or app (`SQ2-10`).
- **SharePoint-origin data carries documented type defects**: Boolean TRUE/FALSE vs 1/0 inconsistency, a four-decimal-place semantic-model creation block, and sensitivity labels that are not inherited by downstream Power BI models (`DQ-14`).
- **Purview scanning of Dataverse is metadata-only** (environment/tables/columns), has no incremental scan, never removes deleted assets from the catalogue, and is unavailable in sovereign clouds (`DQ-16`).

---

## New Anti-Patterns

See §5 (`DAP-30`..`DAP-44`) for the full table with sources; summarised here:

- Assuming Microsoft operates a Dataverse→Azure SQL replication service.
- Trusting row-count comparisons to detect Synapse Link/Fabric-link replica drift.
- Shipping row snapshots (rather than an id + re-fetch) in outbound sync messages.
- Treating Power Automate run-resubmission as a reconciliation strategy.
- Using virtual tables as a general integration layer for large or write-required external data.
- Exposing a negative-filter ("does not contain") search box over a virtual table.
- Choosing Azure SQL for high-ingest telemetry "because it's SQL".
- Treating Azure SQL Long-Term Retention as a cheap queryable archive.
- Relying on `USER_NAME()`-based SQL row-level security behind a shared/implicit Power Platform connection.
- Assuming duplicate detection protects integration/ETL writes.
- Relying on business-rule server-side enforcement for cross-client integrity without testing it first.
- Quoting a concurrent-user ceiling for Dataverse/Power Apps.
- Inventing a write-amplification multiplier instead of measuring it per engagement.
- Asserting "SharePoint can't do customer-managed keys."
- Building `DateOnly`-based business rules or reports that assume the user's local time zone.

---

## Alternatives

Restated from §6, with the v2 corrections foregrounded:

- **Dataverse** — the default for new storage with relational integrity, security granularity, audit and offline; broadest delegation of the three connectors; server-side business-rule enforcement is Assumed pending one empirical test.
- **SQL / Azure SQL** — preferable for immovable existing data, complex relational engine control, customer-managed keys (cheaper entry than Dataverse CMK), and datasets beyond Dataverse's unpublished practical envelope (Hyperscale to 128 TB). **No longer** positioned as strong for high-ingest telemetry or cheap long-term archival — both corrected in v2.
- **Azure Data Explorer / Eventhouse in Fabric** — newly named in v2 as Microsoft's actual target for high-ingest timestamped metrics and events, where v1 had pointed to Azure SQL.
- **SharePoint / Lists** — document-centric collaboration, small flat trackers, now confirmed CMK-capable via a dedicated DEP (tenant/geo granularity).
- **Dataverse for Teams** — team-scoped, seeded-licence, sub-2 GB apps only.
- **External system as system of record** — kept in place with embedding, a volume-uncharacterised virtual table (read-mostly, narrow, positively filtered), or a one-way replicated subset; never a second master.
- **Hybrid architectures** — Dataverse + Fabric/Synapse (with the free read-only SQL analytics endpoint as the lowest-effort reporting path); Dataverse + customer-built SQL pipeline only when writes to the SQL tier are genuinely required, budgeted with full reconciliation machinery; Dataverse + elastic tables for high-ingest data that must stay inside the platform; Dataverse + SharePoint/Blob for documents and binaries.
- **Another technology** — when strict cross-system consistency, no cloud transit, multi-primary writes, country-level residency without ADR, or sub-15-minute cross-system freshness are hard requirements.

---

## Remaining Unknowns

The most consequential open items (full list in §8, U-01..U-41):

1. **U-40 — does an entity-scoped business rule execute server-side on a Web API write?** Genuinely contradictory Microsoft documentation; resolvable only by an empirical test. Highest priority of all remaining unknowns.
2. **U-38 — could Dataverse be added to the Fabric Mirroring source list?** The list has grown repeatedly; a future addition would materially change the Dataverse→SQL recommendation. Re-check before every engagement.
3. **U-31 — no concurrent-user ceiling is published**, and none was found across 16 sources checked; the substitute is a load test, not a fact to look up.
4. **U-30 — no Dataverse standard-table row/size ceiling is published**; only elastic tables carry a scale claim.
5. **U-13 (residual) — per-provider virtual-table write support** for Snowflake, PostgreSQL, Databricks, Salesforce, Oracle beyond the pattern established for SQL/SharePoint/Excel.
6. **U-20 — no first-party Dataverse-connector auto-created indexes**; whether Microsoft support will create custom indexes on request remains unconfirmed (carried from v1, U-08).
7. **U-35/U-36 — Azure SQL Database's actual recovery-model support for minimal logging**, and Stretch Database's deprecation status, both bear directly on whether the "bulk load conditional" finding (`SQ2-12`) has any fast-path exception.
8. **U-01/U-02 — elastic table GA status and alternate-key support remain conflicting** between two Microsoft pages of different dates; unresolved since v1.
9. **U-10 — whether Power Platform VNet support requires Managed Environments** is still not stated on the overview page; unresolved since v1.
10. **U-41 — whether Microsoft ever explicitly states "don't migrate historical data"**; the current evidence is an inference from the enumerated migration categories (master data, open transactions), not a stated rule — the pack must not attribute it to Microsoft as written guidance.

---

## Confidence

**HIGH — confirmed by the Research Gate (verdict PASS, 2026-09-02).**

Raised from v1's MEDIUM. Justification, as put to the gate and upheld by it:

- All five HIGH-severity review gaps (F-01 through F-05) are closed with sourced, Tier-1-dominant findings, including two explicit hard negative findings (no Dataverse→Azure SQL replication, `SY-01`; no virtual-table performance characterisation, `VT-09`) that resolve ambiguity by stating clearly what does *not* exist, rather than leaving a gap.
- The two most consequential corrections — the unsourced SQL matrix cells (three of five contradicted or downgraded) and the missing Dataverse→SQL path — materially change the store-choice guidance the file gives, in a direction that makes the guidance *more* defensible, not less (the file now argues against, rather than for, several previously-asserted SQL strengths).
- 90 new findings across 5 targeted sub-researches, drawn from ≈95 new sources, of which all but four are Microsoft Learn, fetched and dated 2026-09-02.
- The requirement → constraint → architectural implication discipline (the brief's core test) is maintained throughout the new material, including in the two most synthesis-heavy new findings (`SC-21`'s volume-to-budget structure; `SY-18`'s three-path reconciliation-cost comparison), both of which explicitly refuse to invent numbers where Microsoft publishes none.

The Research Gate found no CRITICAL gap and confirmed HIGH despite the following open items, which it judged to bound the *precision* of specific claims, not the *direction* of the guidance (carried forward as the Area 3 maintenance backlog — see "Gaps Still Open" above and the gate's own High/Medium Gaps):

- **One genuinely unresolved contradiction remains inside Microsoft's own documentation** (`DQ-10`, business-rule server-side enforcement) that cannot be closed by further reading — it requires an empirical test in a live environment before any pack rule assumes it.
- **Several MEDIUM gaps are closed on content Microsoft itself flags as AI-assisted with a 3-year refresh cycle** (`DQ-01`, the D365 Implementation Guide) — durable, but not held to the same authoring standard as hand-written product documentation.
- **A handful of unknowns are irreducibly open** (no published concurrent-user ceiling, no published standard-table row ceiling, no published write-amplification factor) not because research was insufficient, but because Microsoft does not publish the answer — these are correctly represented as engagement-measured inputs, not as gaps to be closed by more reading.
- Source-register fragmentation across ten sub-registers, and two carried-over conflicts (elastic-table GA status/alternate keys; VNet ↔ Managed Environments) inherited from v1.

**Gate outcome:** PASS, HIGH confidence. This file is now the canonical Area 3 research; no further gate is pending.
