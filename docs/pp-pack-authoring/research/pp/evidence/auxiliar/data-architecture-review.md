Review Type: ADVERSARIAL QUALITY REVIEW
Reviewed file: `data-architecture.md` (DRAFT v1, 2026-09-02)
Review date: 2026-09-02
Reviewer note: same agent lineage as the author; independence obtained by re-fetching six load-bearing sources and testing claims against them (listed in §Method).

# Data Architecture — Adversarial Review

## Core question

*Could aisa use this research to make a defensible data architecture decision from business and technical requirements, expressed as requirement → constraint → architectural implication, without merely comparing products?*

**Short answer:** mostly yes for the main axes (relational complexity, delegation, transactions, security granularity, retention, reporting offload, system-of-record ownership, freshness, SharePoint disqualifiers, SQL conformance/identity/gateway). Not yet for: (a) five store-fit matrix cells asserted without any fetched source; (b) one boundary that a Microsoft page contradicts (cross-environment reads); (c) the viability of virtual tables at volume, on which the whole "keep in place" branch rests; (d) the Dataverse → Azure SQL replication path, on which the "Dataverse + SQL hybrid" branch rests; (e) translating business transaction volume into platform request budgets. These are targeted gaps, not structural ones.

## Method

- Read `data-architecture.md` in full (§0–§13), `platform-suitability.md` (§1–§3, §4.4–4.5, §4.16–§9) and `application-architecture.md` (§1–§2, §6–§10, §12).
- Re-fetched independently (2026-09-02): `reporting-considerations` (ms.date 2023-12-20), `data-retention-overview` (2026-04-10), `hierarchy-security` (2026-06-22), `limits-tshoot-virtual-tables` (2026-05-15), `connection-common-data-service` (2025-06-19), Microsoft Q&A thread 1417030 (2023-11-06/07). Findings F-02, F-03, F-06, F-07, F-12 derive from these re-fetches.
- Checked every DA-nn cross-reference resolves (61 findings; no dangling ids). Checked U-nn / C-nn ids used in findings against §7/§8 tables.

---

## Findings

### F-01 — Store-fit matrix cells asserted with no fetched source
**Problem.** §2 contains verdicts that cite no source and rest on general knowledge: row 21 "SQL … STRONG (Azure SQL TDE BYOK) — INF" and "SharePoint … POOR (M365 Customer Key, tenant-wide) — INF"; row 12 "SQL … STRONG (archive tables/tiering)"; row 9 "SQL … STRONG (engine)" for high-ingest telemetry; row 17 "SQL … STRONG (ADF/SSIS to SQL)". None of Azure SQL TDE BYOK, M365 Customer Key, Azure SQL archival tiering, or Azure SQL as a telemetry store appears in any of the five sub-registers. Row 21's cells are at least tagged INF; rows 9, 12 and 17 carry no tag at all, so a reader takes them as MS.
**Why it matters.** The matrix is the artefact most likely to be lifted into the pack. An untagged STRONG for SQL on "keep N years of closed records cheaply" or "high-ingest telemetry" would steer decisions on analyst opinion. The file's own provenance rule ("A POOR verdict derived by inference is phrased 'treat as unsupported until verified'") is violated for the SharePoint Customer Key cell.
**Required improvement.** Either fetch Tier 1 evidence (Azure SQL TDE customer-managed keys; Microsoft 365 Customer Key scope; Azure SQL long-term backup retention / data tiering; SQL as ingestion store) and cite it, or downgrade those cells to UNKNOWN and remove the STRONG/POOR wording. Add the origin tag to every non-MS cell in §2, as `platform-suitability.md` §2 does per row.
**Severity.** HIGH

### F-02 — "Environment is a hard data boundary / no cross-environment queries" is contradicted by a Microsoft page
**Problem.** DA-25 states "no cross-environment relationships or queries (inferred)" and §2 row/§11 repeat "environment is the hard data boundary". The Dataverse connector page for canvas apps (`connection-common-data-service`, ms.date 2025-06-19) says: "If you select **Change environment**, specify a different environment to pull data from instead of, or in addition to, the current environment." and "the security roles in the environment control what you can do there." A canvas app can therefore read (and, subject to roles, write) tables in another environment. What does not exist is a cross-environment *relationship* (lookup/join) — the page does not claim that either way.
**Why it matters.** The inference was flagged MEDIUM and U-07 asks for a verbatim statement, which is honest, but the consequence drawn ("one master-data environment serving several app environments → not a Dataverse pattern") is too strong: a read-only reference environment consumed by canvas apps IS possible, at the cost of no joins, separate security configuration and ALM complexity. The finding should distinguish *queries* (possible, per environment selection) from *relationships/joins* (not possible) and from *solution portability* (environment-bound).
**Required improvement.** Rewrite DA-25 and the §11 "hard boundaries" bullet: cross-environment reads are supported for canvas apps via environment selection; cross-environment lookups/joins/cascades/security inheritance are not. Cite `connection-common-data-service`. Re-evaluate the "shared master-data environment" implication accordingly. Close U-07 partially.
**Severity.** HIGH

### F-03 — Virtual-table viability at volume is the weakest link of the "keep in place" branch and is left UNKNOWN
**Problem.** Rows 13–14 of §2, DA-45, DA-46 and §6 recommend virtual tables (read-only) as the default way to keep data in the system of record. The only volume/latency evidence is the SQL provider's "Virtual table queries are limited to returning 1,000 records" — and the re-fetched page scopes that sentence: "If you have a 1:N or N custom multitable (polymorphic) relationship with a virtual table, any query that exceeds this limit fails". DA-45 quotes the 1,000 cap without that qualifier. Nothing is established about: paging behaviour for large external tables, delegation of canvas queries through a virtual table, latency, throttling of the underlying connector (the SQL connector's 100 CRUD / 10 s applies — DA-32 — but the file does not connect it to virtual tables), or the OData v4 provider. U-13 records this as unknown.
**Why it matters.** Without this, the research cannot say whether "surface 2 million SAP items read-only in a model-driven app" is CONDITIONAL or POOR. The most-recommended hybrid mechanism is the least characterised.
**Required improvement.** Fetch the OData v4 provider requirements page, the virtual connector provider page (`create-virtual-tables-using-connectors`) and the connector throttling pages; state precisely which limits apply per provider; correct the 1,000-record sentence in DA-45 to its documented scope; add a "virtual table at volume" boundary to §3 or mark the branch CONDITIONAL-UNVERIFIED explicitly in §2 rows 13–14.
**Severity.** HIGH

### F-04 — No supported path for Dataverse → Azure SQL replication is described, yet "Dataverse + SQL hybrid" is a headline alternative
**Problem.** DA-37 and §6 recommend "Azure SQL alongside Dataverse with an explicit sync path (Synapse Link, Fabric, dataflows, ADF)". The evidence supports SQL → Dataverse (dataflows, ADF, virtual tables) and Dataverse → lake (Synapse Link, Fabric link). It does not evidence Dataverse → Azure SQL: Data Export Service is retired (DA-20), Synapse Link targets ADLS/Synapse (a serverless SQL pool over the lake, not Azure SQL Database), Fabric link targets OneLake. The XC sub-research noted "a SQL copy needs custom pipeline" but this did not survive consolidation.
**Why it matters.** A decision "keep transactions in Dataverse, run heavy reporting/stored-procedure logic in Azure SQL" needs a named, supported replication mechanism with its latency and cost. Without it the hybrid is a slogan.
**Required improvement.** Add a finding stating explicitly: no first-party Dataverse → Azure SQL Database replication service exists after DES; options are Synapse Link + Synapse serverless/dedicated SQL, Fabric link + Fabric SQL endpoint / mirroring, ADF/Fabric pipelines from Dataverse (connector limits, service protection), or Service Bus/webhook events (DA-50). Cite the ADF Dataverse *source* connector page and the Fabric SQL analytics endpoint page. Rank by freshness and cost.
**Severity.** HIGH

### F-05 — "Transaction volume" is covered as API requests, not as business transactions
**Problem.** The brief lists transaction volume and high transaction volume. The file gives service protection (6,000 / 20 min / 52) and daily entitlements (DA-10), and connector quotas for SQL/SharePoint (DA-32, DA-43). It never shows how a business volume ("3,000 work orders/day, each with 6 lines and 2 attachments, audited") maps to requests, given write amplification (plug-ins, audit, cascades, retries, pagination all count — quoted in DV:S06/PS-19). No worked translation, no statement of which operations multiply requests.
**Why it matters.** Discovery captures business volumes, not API calls. Without a translation rule the constraint cannot be applied; aisa would either ignore it or invent a multiplier.
**Required improvement.** Add a finding on write amplification: quote the entitlements page on what counts ("plug-ins, classic workflows, and custom controls"; "Retries and requests from pagination also count"), the audit/retention counting statements, and give the structure of the translation (rows × operations × amplification factors) without inventing factors; mark the factors as engagement-measured inputs. Cross-link PS-19.
**Severity.** HIGH

### F-06 — The 50,000-row limit is generalised beyond its documented scope
**Problem.** DA-03 and §3 say "Aggregation over > 50,000 rows … fails in Dataverse" and "in-platform aggregates fail above 50,000 records". The re-fetched reporting page states: "Within the five-minute duration, reports and queries are allowed to span large datasets that are beyond 50,000 rows, which provide significant flexibility to satisfy most operational reporting needs." The 50,000 limit applies to FetchXML aggregate queries (`AggregateQueryRecordLimit`), dashboard charts/grids, and canvas aggregate functions ("All aggregate functions are limited to a collection of 50,000 rows" — Dataverse connector page); SSRS/paginated reports are bounded by the 5-minute timeout, not by 50,000 rows.
**Why it matters.** Over-stating the limit makes "analytical copy from day one" look mandatory for cases where a filtered paginated report would do. The boundary should be precise so the pack does not encode a false hard limit.
**Required improvement.** Split the boundary: (a) FetchXML/OData aggregates and canvas aggregates → 50,000; (b) charts/dashboard grids → 50,000; (c) reports/queries → 5 minutes, "beyond 50,000 rows" allowed; (d) TDS → 5/2 minutes. Quote the reporting page sentence above. Keep the "shorter periods of time" positioning.
**Severity.** MEDIUM

### F-07 — Dataverse's positive fit rests on positioning statements; the one comparative fact ("broadest delegation") is not cited
**Problem.** §6 and rows 1–2 of §2 assert Dataverse STRONG for relational data and "broadest delegation". Evidence offered: "Dataverse is the preferred choice if you need more complex relational data" (one reference architecture sentence), "If you're building a new app and storage, consider using Dataverse", PS-14's "tends to be faster". The Dataverse delegation table (`connection-common-data-service`: `<, <=, >, >=` delegable on Text and DateTime, `Not`, `In`, `IsBlank`, `StartsWith`, `Sum/Min/Max/Avg`, `Search` on Text) is not cited anywhere, although it is the concrete evidence that SharePoint's table (`Not` never; ID only `=`; `IsBlank` No on text) is narrower and SQL's (`<` on Text No; `IsBlank` No) is partial. Strength claims on business rules and security are capability descriptions from "What is Dataverse", not constraint-derived.
**Why it matters.** The brief says "Do not accept generic claims such as 'Dataverse is good for business applications'". The limitations side is excellent; the strengths side is closer to the generic claim than the file admits.
**Required improvement.** Add the Dataverse delegation table as a source and a side-by-side delegation comparison (Dataverse / SQL / SharePoint) with verbatim table cells; state the "15-table query limit" for `In` and the "aggregate functions … 50,000 rows" note. Re-express Dataverse strengths as constraints the other stores fail (already implicit in DA-33/DA-42/DA-60) rather than as capability lists.
**Severity.** MEDIUM

### F-08 — Reconciliation is asserted, not evidenced
**Problem.** The brief asks about synchronization *and reconciliation*. Reconciliation appears once as a quoted design element of one reference architecture ("Nightly dataflows in the secondary environment correct any missed or failed event-driven updates") and as a design instruction in DA-52/DA-54. There is no evidence on reconciliation mechanisms (row counts/hashes, change-tracking re-seed, dead-letter replay, dual-write's "catchup mode"), on what Microsoft recommends when copies drift, or on how to detect drift.
**Why it matters.** Any replicated read model (DA-45, DA-49) needs a drift-detection and repair story; "nightly dataflow" is one design, not guidance.
**Required improvement.** Add a finding on reconciliation with at least: change tracking full re-seed ("The first time you use this message, it returns all records" — already in EX:S19), dual-write "play, pause, and catchup modes" (EX:S41), Service Bus dead-letter replay (EX:S49), and Power Automate resubmit semantics; mark tooling gaps as UNKNOWN.
**Severity.** MEDIUM

### F-09 — Read/write patterns and user concurrency are treated only through limits, not as design drivers
**Problem.** The brief lists read/write patterns, concurrency and frequent reads/writes. The file covers write throughput (DA-10), record-level edit conflicts (DA-08), caching (DA-54) and PPWA "pre-images"/bulk advice. It does not characterise read-heavy vs write-heavy workloads on each store (e.g., model-driven grid paging and server-side views vs canvas gallery paging; SharePoint read scaling vs the 600 calls/min budget; SQL DirectQuery CPU competition with the app — DA-38 touches it). User concurrency defers entirely to PS-20 ("no documented ceiling").
**Why it matters.** "Many readers, few writers" versus "many writers on few records" leads to different stores and different designs (sharing/POA, locks, elastic). Today the file only says "test".
**Required improvement.** Add a short finding mapping workload shape → store implications using existing quotes (PE:08 "server-side views to prefilter", elastic "high volume of read and write requests", SQL connector per-user vs per-connection quotas, SharePoint per-connection quota, POA hot path). Keep "no user-concurrency ceiling" but state which limit binds first per store.
**Severity.** MEDIUM

### F-10 — Data quality coverage is limited to keys and duplicate rules
**Problem.** DA-53/DA-60 cover alternate keys, duplicate detection, business rules and stewardship quotes. Absent: Microsoft guidance on data cleansing before migration beyond one sentence, data-quality implications of Excel/SharePoint-origin data (type looseness is mentioned only via Power BI Boolean inconsistency), Dataverse validation options (required, format, min/max, business rules scope in canvas vs model-driven), and profiling/cleansing tooling (Power Query in dataflows is mentioned once). The D365 IG data-quality chapter returned 404 and no substitute was found.
**Why it matters.** "Data quality" is an explicit brief item and a common reason a store decision fails (bad master data imported into a strict schema).
**Required improvement.** Locate the current D365 IG data-quality / data-management sub-pages (URLs changed) or the Dynamics 365 guidance hub equivalents; add one finding on validation scope per store and one on cleansing-before-load. Mark remaining gaps UNKNOWN.
**Severity.** MEDIUM

### F-11 — "System of record" vs "source of truth" vocabulary left undefined; ownership per field is evidenced, "authoritative data" is not
**Problem.** The brief asks where the authoritative data lives. The file honestly records (U-14) that the Implementation Guide uses "system of record, or owner" and reserves "source of truth" for the golden configuration environment. It then uses both terms loosely in §2/§6 ("system of record posting as pivot", "source id"). No definition is adopted for the pack.
**Why it matters.** aisa's data lens and glossary will need one operational definition; leaving two overlapping terms invites inconsistent Discovery rows.
**Required improvement.** Adopt and state a working definition in §11 (e.g., owner-per-field = system of record; "source of truth" not used) with the IG quotes as anchor; keep U-14 open for a Microsoft definition.
**Severity.** MEDIUM

### F-12 — Provenance labels: Q&A answer mis-attributed; fetched-summarised support pages carry paraphrased "quotes"
**Problem.** SP:S-16 is described as "Microsoft moderator" / "Microsoft-employee answer"; the thread shows the answerer as "Ling Zhou_MSFT (Microsoft External Staff)". The verbatim sentence "Unfortunately, there is no setting for item editing and saving conflicts in SharePoint lists at this time." is real (2023-11-07). Separately, ten support.microsoft.com sources are "fetched-summarised" and their evidence is labelled "as returned by fetch tool"; DA-40 and C-13 rely on SP:S-07 wording that the file itself suspects is lossy, and U-03 admits the indexed-column limit was not read from the page.
**Why it matters.** Both affect the SharePoint concurrency and integrity findings (DA-08, DA-40) that drive a POOR verdict. T4 labelling is correct, but the attribution should be exact, and paraphrased support text must not be presented as quotes.
**Required improvement.** Correct the attribution to "Microsoft External Staff (Q&A)". Re-fetch SP:S-02 and SP:S-07 in a browser and replace summarised text with verbatim quotes; resolve U-03 and C-13. Downgrade DA-40's integrity sentence to MEDIUM until done (it is already MEDIUM on S-07; make it explicit in §3).
**Severity.** MEDIUM

### F-13 — Consuming enterprise analytics outputs back into apps (Fabric → Dataverse) is unevidenced
**Problem.** Hybrid "Power Platform + enterprise data platforms" is covered one-way (Dataverse → Fabric/Synapse). The reverse — apps consuming warehouse/lakehouse outputs — appears only as "Fabric" in a provider list (DV:S15) and one marketing sentence on the Fabric link page ("By adding those insights back to Dataverse as virtual tables connected to OneLake"). No limits, freshness or security evidence for Fabric/OneLake virtual tables or for reading Fabric SQL endpoints via the SQL connector.
**Why it matters.** "Show the customer's churn score / stock forecast in the app" is a common requirement; its architecture (virtual table over Fabric vs replicated scores vs API) is undecidable from this file.
**Required improvement.** Fetch the Fabric virtual connector / OneLake virtual tables documentation and record limits; add a row to §2 ("consume analytical outputs in the operational app").
**Severity.** MEDIUM

### F-14 — Positive scale evidence for Dataverse is absent; "no technical limit" is an entitlement statement, not a performance statement
**Problem.** The only scale-positive Dataverse statement is "There's no technical limit on the size of a Dataverse environment", which is about capacity entitlement. Performance at tens of millions of rows is inferred negatively from throttled anti-patterns (DA-26) and platform-managed indexing. No Microsoft statement on tested/typical table sizes, and no independent benchmark, is cited. The SQL section correspondingly assumes SQL "STRONG (engine)" for scale without evidence (F-01).
**Why it matters.** The decision "very large dataset → SQL rather than Dataverse" is one of the brief's named boundaries; the file can only say "constrain filter columns or move to elastic/analytical store" (DA-26), which is a reasonable inference but MEDIUM.
**Required improvement.** State explicitly in §2 row 2 and DA-26 that no Microsoft performance envelope for standard-table size is published (UNKNOWN), and that the boundary is query-shape-based, not row-count-based. Defer benchmarks to Area 09 (already in §9) but make the matrix cell say UNKNOWN rather than STRONG for "very large tables with arbitrary filters".
**Severity.** MEDIUM

### F-15 — SQL Managed Instance / SQL on VM specifics dropped during consolidation
**Problem.** The SQL sub-research recorded (its U-6) that SQL authentication is unsupported for hosts with extra subdomains such as Managed Instance ("Connections to servers containing additional subdomains before .database.windows.net … are not supported") and that MI details are otherwise undocumented. DA-36 mentions "Managed Instance via Entra auth" in passing; the consolidated §8 has no MI unknown.
**Why it matters.** MI is the natural lift-and-shift target for the "existing on-prem SQL" requirement the brief emphasises.
**Required improvement.** Reinstate the MI/SQL-on-VM unknown in §8 and the connector quote in DA-36 or DA-30.
**Severity.** LOW

### F-16 — Dynamics 365 Implementation Guide is the main source for integration principles; applicability to non-Dynamics Power Platform solutions is not caveated
**Problem.** DA-46..DA-52 lean on the D365 IG (integration patterns, ownership, anti-patterns). The guide is written for Dynamics 365 implementations; its statements ("Too much data synchronized with Dynamics 365 for reporting purposes…") are applied to Dataverse-only solutions without saying so.
**Why it matters.** The principles transfer (same platform), but the pack should know the guidance's frame; some statements (dual-write, "Dynamics 365 datacenter") are Dynamics-specific.
**Required improvement.** Add one sentence to §10 evidence-quality notes on the D365 IG frame and mark Dynamics-specific statements as such in DA-48/DA-51.
**Severity.** LOW

### F-17 — Standard-table consistency model is never stated
**Problem.** The file contrasts elastic "session-level consistency" with standard tables but never quotes what standard tables guarantee (read-after-write within the database; Azure SQL-backed). DA-09 quotes "Use standard tables when: Your application requires strong data consistency" — that is the closest statement and it is buried.
**Why it matters.** "Consistency" is a brief item; the requirement "user must immediately see what a colleague just saved" should map to an explicit statement.
**Required improvement.** Promote the elastic-vs-standard consistency quote into a small finding under §4.1 with the Power Pages cache and virtual-table caveats as exceptions.
**Severity.** LOW

### F-18 — File size and duplicated sub-registers reduce usability for pack authoring
**Problem.** 1,013 lines / 218 KB; §12 reproduces five sub-registers (~250 rows) with overlapping URLs (e.g., `api-limits`, `dataverse-sql-query`, `capacity-storage`, `data-retention-overview` appear 2–3 times under different ids). The predecessor files use one deduplicated register.
**Why it matters.** Traceability is preserved, but pack authors will struggle to find "the" source for a fact, and duplicated rows hide which fetch is the dated one.
**Required improvement.** Either deduplicate into one register with alias columns (DV:S01 = EX:S37 = XC:… ), or add a short "most-cited sources" table at the top of §12. Optional for gate; recommended before pack authoring.
**Severity.** LOW

### F-19 — Confidence grading is optimistic in two places
**Problem.** DA-03 is HIGH although it rests partly on a 2023-12 page and over-generalises the 50k limit (F-06). DA-40's headline sentence on referential integrity is presented in §3 as an MS boundary although the finding body grades that element MEDIUM on fetch-tool wording.
**Why it matters.** Gate reviewers rely on the grade; §3 boundaries should not outrank their findings.
**Required improvement.** Regrade DA-03 to HIGH (limits) / MEDIUM (reporting scope) and annotate the §3 SharePoint integrity boundary "(MEDIUM, S-07 wording)".
**Severity.** LOW

---

## Coverage Assessment

**Strong areas**
- Requirement → constraint → implication discipline is real, not cosmetic: 61 findings each end in a decision impact stated as a requirement mapping; §3 boundaries and §5 anti-patterns are traceable to verbatim Tier 1 text.
- SharePoint/Lists/Excel disqualifiers: complete and Microsoft-anchored (LVT "can't be changed", 12 joins, delegation table, unique-scope limits, no column security, Excel concurrency, ALM/governance) — the best-evidenced section.
- SQL via connector: conformance checklist, identity model (implicit vs Entra explicit), connector quotas/timeouts, gateway caps and operating model, VNet — concrete and sourced; the Azure Architecture Center positioning of Dataverse vs Azure-native databases is the right anchor.
- Dataverse limitations: capacity meters and borrowing, ownership immutability, POA/sharing, rollups/formula columns, elastic trade-offs, audit/LTR/backups, TDS/reporting limits, Fabric replica on the database meter — thorough and cross-verified across sub-researches.
- Analytics: operational vs analytical separation is explicit (DA-03, DA-19..22), including the Fabric "no copy" correction and the CLS-in-lake tension.
- Security/governance as drivers: Managed Environments gate, CMK/Lockbox/IP firewall licensing, residency (EUDB dual condition, ADR, global metadata, Copilot flex routing), DLP scope — well evidenced.
- Uncertainty: 16 conflicts and 26 unknowns are explicit; volatility and aged pages are flagged; overall MEDIUM cap is justified.

**Weak areas**
- Dataverse strengths argued by positioning rather than comparative evidence (F-07); scale-positive evidence absent (F-14).
- Virtual tables recommended without volume/latency characterisation (F-03).
- Transaction volume handled only as API requests (F-05); read/write patterns and user concurrency light (F-09).
- Reconciliation and drift repair thin (F-08); data quality thin (F-10); consistency model implicit (F-17).
- Provenance of some SharePoint claims (fetched-summarised support pages; Q&A attribution) (F-12).

**Missing areas**
- Dataverse → Azure SQL replication path (F-04).
- Consuming analytical outputs back into apps (F-13).
- SQL Managed Instance / SQL on VM specifics (F-15).
- Explicit "system of record" definition for the pack (F-11).
- Origin tags on every non-MS cell of the §2 matrix (F-01).

**Unsupported claims**
- §2 row 21 (Azure SQL TDE BYOK STRONG; SharePoint Customer Key POOR), row 12 (SQL archive tiering STRONG), row 9 (SQL telemetry STRONG), row 17 (SQL ADF/SSIS STRONG) — no fetched source (F-01).
- DA-25 "no cross-environment queries" — contradicted by `connection-common-data-service` (F-02).
- DA-45 "1,000-record query cap" stated without its documented scope (1:N / polymorphic relationships) (F-03).
- DA-03 / §3 "aggregation over 50,000 rows fails in Dataverse" — over-generalised; reports may span beyond 50,000 within 5 minutes (F-06).
- DA-08 SharePoint concurrency attribution ("Microsoft moderator") — should read "Microsoft External Staff (Q&A)" (F-12).

**Critical gaps**
- None that invalidates the file's structure. The HIGH items (F-01..F-05) are bounded: one matrix row-tagging pass, one finding rewrite (DA-25), two targeted fetch sets (virtual-table providers; Dataverse→SQL paths), one added finding (write amplification). Estimated effort: one focused revision session, no new research area.

---

## Research Verdict

**NEEDS MORE RESEARCH** — targeted revision to v2, not a re-run.

Conditions to reach READY FOR GATE:
1. Resolve F-01 (source or downgrade the five unsourced matrix cells; add origin tags to all non-MS cells).
2. Resolve F-02 (rewrite DA-25 on cross-environment reads vs relationships; cite the Dataverse connector page).
3. Resolve F-03 (virtual-table provider limits; correct the 1,000-record scope; add a volume boundary or mark rows 13–14 CONDITIONAL-UNVERIFIED).
4. Resolve F-04 (add the Dataverse → Azure SQL / Fabric SQL replication-path finding).
5. Resolve F-05 (write-amplification finding with quoted counting rules; no invented factors).
6. Apply F-06, F-07, F-12 corrections (50k scope; Dataverse delegation table cited; Q&A attribution; re-fetch SP:S-02/S-07 verbatim).
7. Carry F-08..F-11, F-13..F-19 either as new findings or as explicit UNKNOWN rows in §8, so the gate can see what remains open.

Everything else in the file — the boundaries, anti-patterns, conflicts, unknowns and the OLTP/analytics separation — is already at the evidentiary standard of `platform-suitability.md` and `application-architecture.md` and should be kept as is.
