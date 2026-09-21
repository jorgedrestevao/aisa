# Step 4B — runtime provenance annex (durable)

<!--
provenance: AUTHORING ANNEX
date: 2026-09-04 (created in the Step 4B pre-4C bounded repair)
source: the per-unit provenance tables produced while authoring the 15 RESEARCH units, persisted here so
        they survive the authoring session. Nothing is regenerated from model knowledge.
scope: AUTHORING-SIDE ONLY. No canonical research id is introduced into any runtime file — the runtime
        convention (zero research ids, inherited from the frozen Step 3 layer) is unchanged.
-->

## 0. What this annex is, and why it exists

Step 4B follows the frozen Step 3 provenance convention: **zero canonical research ids at runtime**, with
traceability held authoring-side. That made the Step 4B report the only carrier of the provenance material
— and the report summarised it rather than persisting it. This annex persists it.

For every **material decision-grade rule** in the 15 RESEARCH units: the runtime file, the rule, the
canonical source, the source's finding id, whether the fact is stable or volatile, the owning volatility
row where one applies, and a research-gap marker where the rule is bounded by a gap.

**This is the object gates G1 / G3 / G7 run against.**

### 0.1 Canonical source shorthand

| Key | Canonical file (`docs/pp-pack-authoring/research/pp/evidence/`) |
|---|---|
| `A1` | `platform-suitability.md` (Area 1) — ids `PS-nn` |
| `A2` | `application-architecture.md` (Area 2) — ids `AA-nn`, conflicts `AA-Cn`, unknowns `U-xn` |
| `A3` | `data-architecture.md` (Area 3) — ids `DA-nn` and the sub-registers `DV/SQ/SP/EX/XC/VT/SY/SQ2/SC/DQ` |
| `A4` | `automation-architecture.md` (Area 4) — ids `AT2-nn`, conflicts `C-nn`, unknowns `U-nn` |
| `A5` | `integration-architecture.md` (Area 5) — ids `IA-nn`, sources `I-nn`, conflict `IA-C-01 (C-01)` |
| `A6` | `security.md` (Area 6) — ids `SEC-nn`, cross-boundary `SEC-XB-nn` |
| `A7` | `governance.md` (Area 7) — ids `GOV-nn`, conflicts `GOV-Cn` |
| `A8` | `alm-devops.md` (Area 8) — ids `ALM-nn`, conflicts `ALM-Cn` |
| `A9` | `performance-scale.md` (Area 9) — ids `PF-nn`, `PF-U-nn`, `PF-C-nn`, `DC-nn` |
| `A10` | `licensing-cost.md` (Area 10) — ids `LC-nn`, `DC-nn` |
| `A11` | `operations-support.md` (Area 11) — ids `OP-nn`, `OP-C-nn`, `OP-U-nn` |
| `A12` | `architecture-patterns.md` (Area 12) — ids `APR-*`, pattern ids `AP-01…AP-10`, failure modes `Y-nn` |
| `AP` | `anti-patterns.md` (Area 13) — ids `AP-D-nnn` |
| `AL` | `alternatives.md` (Area 14) — ids `ALT-nnn` |
| `DC` | `decision-criteria.md` (Area 15) — ids `DC-D-nnn` |
| `MF` | `canonical-manifest.md` — reservations `NB-01…NB-08` |

**Volatility rows** (`VC-nn`, `VS-nn`, `TW-Vn`) are **runtime** register anchors, not research ids. They
are the only identifiers that appear in both this annex and the runtime files.

### 0.2 Coverage

| Unit | Material decision-grade rules traced |
|---|---:|
| `application/application-surfaces.md` | 56 |
| `data/store-boundaries.md` | 25 |
| `data/dataverse.md` | 44 |
| `data/sharepoint.md` | 13 |
| `data/azure-sql.md` | 28 |
| `data/query-and-delegation.md` | 32 |
| `automation/automation-mechanisms.md` | 44 |
| `integration/integration-mechanisms.md` | 46 |
| `security/security-controls.md` | 47 |
| `governance/governance-and-environments.md` | 40 |
| `alm/release-and-lifecycle.md` | 40 |
| `performance/performance-and-scale.md` | 52 |
| `economics/licensing-and-cost-drivers.md` | 49 |
| `operations/operability-and-support.md` | 63 |
| `architecture/patterns.md` | 40 |
| **Total** | **619** |

*The Step 4B report estimated ≈330 provenance rows. Enumerated here the figure is **619** — the report
under-counted, in the same way it under-counted the research gaps. The rows below are the authoritative
count.*

Every rule below was verified against the named canonical file during authoring. Rules whose canonical
basis could not be established were **not authored** — they are in
`step-4b-research-gaps.md` instead.

---

## 1. `application/application-surfaces.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Rung 0 precedes the surface question — configure, buy, first-party, owned capability | `A1`, `A2` | `PS-41`, `PS-44`, `AA-36`, `AA-20` | stable | — | — |
| A first-party app may cover part of the requirement; record covered subset and gap separately | `A2` | `AA-36` | stable | — | — |
| Canvas: responsiveness is opt-in; the authoring canvas does not render sizing formulas; some controls unsupported in containers | `A2` | `AA-02` | stable | — | — |
| Canvas: co-authoring removed — one maker per app at a time | `A2` | `AA-06` | stable | — | — |
| Canvas: no route model; deep links hand-built; a dated mobile deep-link contract change | `A2` | `AA-09` | volatile | `VC-10` | `G-024` |
| **No numeric canvas size threshold exists**; the vendor claim and the third-party heuristics are inadmissible | `A1`, `A2` | `AA-01`, `AA-03`, `AA-C1`, `U-A1`, `PS-06`, A2 §9 gate 3 | stable (absence) | — | — |
| Canvas partition patterns: state lost on cross-app launch; no standalone→custom-page conversion | `A2` | `AA-03` | stable | — | — |
| Record-centric requires the governed data model; automatic relational navigation, accessibility, responsiveness | `A1`, `A2` | `AA-12`, `PS-02`, `PS-11` | stable | — | — |
| Record-centric shell is platform-owned; theming reaches colours/font/logo/header; named areas unthemed | `A2` | `AA-13`, `AA-14` | stable mechanism / volatile dates | `VC-10` | `G-024` |
| Record-centric: phone browser unsupported — native player required | `A1`, `A2` | `AA-45`, `PS-02` | stable | — | — |
| Guided stages execute no logic of their own; published stage and table caps | `A2` | `AA-19`, `AA-C4` | stable | `VS-25` | — |
| Multisession is unmanaged-solution-only — collides with managed-only-in-production | `A1`, `A2` | `AA-20`, `PS-05` | stable | — | — |
| Record-centric has native addressable, security-trimmed record URLs | `A2` | `AA-18` | stable | — | — |
| Custom pages are the stated convergence vehicle; embedded canvas is legacy | `A2` | `AA-15` | stable | — | — |
| Custom pages: no offline, no device controls, mobile preview, no mail-client embedding, state not restored, host pins last-published version, third-party cookies, locale formats unsupported | `A2` | `AA-16` | stable absences / volatile ceilings | `VS-25`, `VC-10` | — |
| External site: table permissions × web roles, deny-by-default; row access as configuration | `A2` | `AA-21`, `AA-24` | stable | — | — |
| External site: server cache — only site-originated writes invalidate instantly; background writes never guaranteed immediate; manual clearing degrades performance | `A2`, `A3` | `AA-27`, `SC-14` | volatile | `VS-01` **(stamped)** | — |
| External site: content caching is anonymous-only; authenticated pages not cached; delivery network and firewall included; **throughput unpublished** | `A2` | `AA-28`, `U-4` | stable / `UNKNOWN` | — | `G-018` |
| External site: platform-attested accessibility standards; your customisation is your responsibility | `A2` | `AA-47` | stable | — | `G-021` |
| External site: many out-of-the-box languages; the code-first model is single-language | `A2` | `AA-48` | stable | — | — |
| Code-first site model: source-code and CLI only; surrenders lists, forms, template language, design workspaces, formula language, offline setting, discoverability, test tooling, platform source control | `A2` | `AA-23`, `U-C6` | volatile / preview state `UNKNOWN` | `VC-10` | `G-020` |
| External site's interface is documented as not intended as a third-party integration surface | `A1` | `PS-36` | stable | — | — |
| Enhanced data model drift: new components not auto-added to the solution; target-environment edits create an unmanaged layer | `A2` | `AA-29` | stable | — | — |
| Server-side site logic: tenant can block outbound calls; allowed-domain list; execution-time limits; regional and availability state per tenant | `A2` | `AA-29`, `U-C3` | volatile maturity | `VC-10` | — |
| Code apps: premium entitlement per end user; public asset endpoint with no IP restriction; *"don't store sensitive data"*; no desktop player; no list forms; pipeline ALM without source-code integration; offline and mobile undocumented | `A1`, `A2` | `AA-35`, `AA-C10`, `U-D2`, `U-D3`, `PS-03` | volatile (already changed once) | `VC-05`, `VC-10` | `G-016`, `G-020` |
| Team-hosted: combined ceiling not extensible; one organisational unit; no interface, plug-ins, code components, record-centric apps, audit, column security or offline | `A1`, `A2` | `AA-50`, `PS-16` | stable absences / volatile ceiling | `VC-07` **(stamped)** | — |
| Team-hosted → governed store graduation is **one-way**; no downgrade documented; all environment users then require standalone entitlement; capacity counts against the tenant pool | `A2` | `AA-50` | stable | `VC-05` | — |
| Report visual: row ceiling, organisation-embedding only, cannot filter or return data, write-back on next refresh, app shared separately, uneven browser support | `A2` | `AA-51` | stable | `VS-25` | — |
| List-customised form: cannot be shared manually — access inherited from list readers; generic lists only; no automated cross-environment copy | `A2` | `AA-51` | stable | — | — |
| Chat tab: sensors unsupported; TLS-only content; no attachment download on mobile | `A2` | `AA-50` | stable | — | — |
| Branded wrapping: canvas only; no push; no consumer audience; no sovereign cloud; no customer key or vendor-access approval; bundle-size ceiling; no visible sign-out; subscription plus code signing; monthly re-wrap; approved-client-app policy blocks it | `A2` | `AA-38`, `AA-39`, `AA-40` | stable / volatile availability | `VS-25` | — |
| Push exists only through first-party players — `{branded app, push}` is **unsatisfiable**; throttles undocumented | `A2` | `AA-46`, `U-E1` | stable / `UNKNOWN` | — | `G-019` |
| Mobile management applies to the shared player; not a canvas-vs-record-centric differentiator | `A2` | `AA-41` | stable | — | — |
| Offline: five depths; no browser offline; none in embedded canvas, custom pages or team-hosted; read-only progressive-web-app on the low-code site, none on code-first; local file cache with manual conflicts; full offline-first on standalone canvas over the governed store only, with non-governed connectors, virtual and elastic tables and automations excluded, foreground-only sync, data-model restrictions | `A1`, `A2` | `AA-42`, `AA-44`, `PS-35` | stable | `VS-38` | `G-025` |
| Record-centric offline: field-level security and field sharing unsupported; personal views, search and duplicate detection unsupported; grid filtering disabled when a profile exists even online | `A1`, `A2` | `AA-43`, `PS-35` | stable | — | — |
| **Offline × field-level confidentiality is an unsupported combination** | `A2` | `AA-43`, `AA-44` | stable | — | — |
| Custom conflict rules, background sync and multi-day queues are not documented as extensible — *treat unsupported until verified* | `A2` | `AA-44` (INF) | INF, marked | — | — |
| Device capability: NFC native-players only; no barcode in desktop browsers; camera not in browser or mobile chat; desktop player lacks sensors, mixed reality and NFC with no retirement documented | `A2` | `AA-45`, `AA-C6` | stable / risk | — | — |
| Accessibility: record-centric built-in; canvas maker-dependent with documented impossible patterns whose escape hatch is a code component; the guidance page may overstate; **no per-surface conformance report** | `A1`, `A2` | `AA-47`, `AA-C7`, `U-E3`, `PS-11` | stable / currency medium | — | `G-021` |
| Localization: record-centric language packs; canvas hand-built dictionary; right-to-left documented for custom pages with icon, shape and image exceptions; **standalone canvas RTL `UNKNOWN`**, the earlier non-support claim withdrawn | `A2` | `AA-48`, `AA-C11`, `U-E6` | stable / `UNKNOWN` | — | `G-015` |
| Identity: employee work or school accounts; personal consumer accounts removed; sovereign clouds bind a directory instance | `A1`, `A2` | `AA-52`, `PS-60` | stable | — | — |
| Identity: business guests reach canvas, record-centric, code apps and wrapping; entitlement must be recognised cross-tenant; app-scoped plans are **not** recognised cross-tenant | `A1`, `A2` | `AA-52`, `PS-36` | stable rule / volatile entitlement | `VC-05` | — |
| Identity: authenticated customers only via external sites; the previously-recommended consumer-identity service closed to new tenants and the higher tier was discontinued; local site auth *"not recommended"* and on by default | `A2` | `AA-22`, `AA-C5` | volatile | `VC-10` | — |
| Identity: the anonymous permission makes data *"visible to anyone"*; open self-registration on by default | `A2` | `AA-25` | stable | — | — |
| Frontline / shared-device identity mode is `UNKNOWN` | `A1`, `A2` | `U-E2`, `PS-60`, `U-14` | `UNKNOWN` | — | `G-017` |
| Component library: pull-based updates — one shared fix is N publish cycles; *allow customization* removes the association **permanently** | `A2` | `AA-32`, `AA-33` | stable | — | `G-023` |
| Control-generation lock: both generations coexist with no retirement; a property and behaviour revision already shipped | `A2` | `AA-11` | volatile | `VC-10` | — |
| A visual code component does not by itself make a standard app premium — only non-connector external calls do | `A2` | `AA-34`, `AA-C3` | volatile (already changed once) | `VC-05` | — |
| No first-party low-code test framework — the previous one is deprecated; documented migration is code-first browser automation | `A1`, `A2` | `AA-08`, `PS-53` | stable | — | `G-089` |
| **No published concurrent-user ceiling for any surface**; governed by the data path and per-identity budgets | `A2`, `A3` | `AA-53`, `U-2`, `U-4`, `SC-16` | stable absence | `VC-04` | `G-027` |
| Relative exposure to vendor-driven interface change differs per surface — **supported synthesis, not a vendor ranking**; every option needs a change-absorption owner | `A1`, `A2` | `AA-54` (INF), `PS-50` | INF, marked | — | — |
| Virtualizing an external system of record forfeits audit, row security, offline, guided processes, search and site solutions | `A1` | `PS-56` | stable | — | — |
| External audience is metered on unique users with a documented counting hazard — **no price carried** | `A1`, `A2` | `AA-26`, `PS-36` | volatile | `VC-06` | — |
| **Agent surfaces: `UNKNOWN` in every class, decision-blocked**; consumption unmodellable; agent controls preview; a dated removal of a bundled entitlement | Step 3 registers + `A10` | `BS-03`, `VS-20`, `TW-V2`, `ALT` row | volatile / blocked | `VS-20`, `TW-V2` | `G-118` |
| Managed-environment licence enforcement can block users from opening apps | `A7`, `A10` | `GOV-11`, `LC-23` | dated | `TW-V3` | `G-080` |
| Visibility formulas are client-side branching, **never** authorization | `A1`, `A2` | `AA-10`, `PS-31` | stable | — | — |

---

## 2. `data/store-boundaries.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| The vendor's own frameworks put data requirements first and legitimise polyglot persistence | `A3` | `DA-01` | stable | — | — |
| *View or data?* — three integration categories; embedding saves time, training and user licences and keeps data in place | `A3` | `DA-46` | stable | — | — |
| Cross-store capability map, per observable requirement | `A3` | §2 store-fit matrix (27 rows), §3 boundaries | stable dimensions / volatile ceilings | per row | — |
| Relational depth: 1:N and N:N with **one parental relationship per child**; list store bounded by a join ceiling with opt-in delete-only integrity | `A3` | `DA-05`, `DA-40` | stable | `VS-33` | — |
| Atomicity: server-side only in the governed store; the expression layer is never transactional; list store has no transaction and last writer wins | `A3` | `DA-07`, `DA-08` | stable | — | — |
| Concurrency: optimistic via SDK/Web API; **connector locking semantics undocumented**; list store has no conflict setting | `A3` | `DA-08`, `DA-41` | stable / `UNKNOWN` | — | `G-043`, `G-050` |
| Authorization grain: the governed store is the only one with API-level column security; list-store row scoping is bounded and recommended far below its maximum, with no column security | `A3` | `DA-11`, `DA-12`, `DA-33`, `DA-42`, `DA-55` | stable | `VS-29` | `G-045` |
| Audit: native and metered on the governed store; build-it in the external relational store, where **server-side triggers break connector writes**; list store has versioning only | `A3` | `DA-16`, `DA-30` | volatile | `VS-05` | — |
| Documents as the record → the list/library store; the governed store's file columns carry **no label mechanism** | `A3` | `DA-15`, `DA-44`, `DA-59` | stable | — | — |
| Binaries: the file meter is an order of magnitude cheaper than the database meter; long-term retention saves **nothing** on files | `A3` | `DA-14`, `DA-17`, `DA-62` | volatile | `VC-07` | — |
| High-ingest: elastic tables forfeit transactions, joins, N:N, rollups, sharing and cascades, and **GA is unresolved**; the vendor routes high-ingest metrics away from relational | `A3` | `DA-09`, `SQ2-06`, `SQ2-07`, `C-02` | stable / **contradicted maturity** | `VS-32`, `VC-10` | `G-041` |
| **Aggregation ceiling bounds aggregate queries, charts and dashboard grids — not ordinary filtered reads** | `A3` | `DA-03` (revised) | volatile | `VS-06` **(stamped)** | — |
| Analytical copy required from day one where aggregation, charts or multi-year history are needed on growing tables; the vendor's own instruction is a dedicated reporting store | `A3` | `DA-03`, `DA-19`, `DA-21`, `DA-51` | stable | — | — |
| **Security does not travel into a copy** — row security rebuilt, secured columns export null, embedded reports ignore app roles | `A3` | `DA-20`, `DA-22` | stable | — | — |
| A copy obliges: reconciliation owner, drift detection that is not row counts, budgeted resynchronisation, rebuilt authorization, capacity, erasure propagation, a schema-change owner | `A3` | `SY-14`, `SY-15`, `SY-07`, `DA-19`, `DA-60` | stable | `VC-07` | `G-029`, `G-030` |
| **No first-party managed path to a writable relational copy** — every writable copy is customer-built and customer-operated | `A3` | `SY-01`, `SY-18` | point-in-time negative | `VC-10` | `G-032` |
| Where no write is required, the auto-provisioned read-only analytical endpoint is the lowest-reconciliation route | `A3` | `SY-02`, `SY-03` | stable | — | — |
| Virtualization forfeits row security, audit, search, offline, rollups and analytics; column selection ignored; never the "1" side; negative filters corrupt paging; absent from the delegable list; **no performance characterisation at any volume** | `A3` | `DA-45`, `VT-04`, `VT-05`, `VT-06`, `VT-09`, `VT-10`, `VT-17` | stable | — | `G-054` |
| Freshness in a virtualization design is bounded by the **upstream** refresh | `A3`, `A5` | `IA-43`, `I-32` | stable | — | — |
| Bidirectional sync needs per-field ownership; product tooling exists for one pairing and **mutates the receiving schema** | `A3`, `A5` | `DA-48`, `IA-38` | stable | — | — |
| Capacity is an entitlement, not a technical limit; the database meter is binding and borrowing is one-directional; **over-capacity blocks administrative operations** | `A3` | `DA-04`, `DA-27` | volatile | `VC-07`, `VS-09` | — |
| Backups and the recycle bin are recovery, not archive | `A3` | `DA-18` | volatile | `VS-07` | — |
| Migrate master data and open transactions, not closed history — **the stronger form is pack opinion, not vendor guidance** | `A3` | `DA-54`, `DQ-05`, `U-41` | preserved as opinion | — | `G-033` |
| Residency, ownership type, long-term retention and the team-scoped upgrade are **irreversible**; names replicate globally | `A3` | `DA-57`, `DA-58`, `DA-12`, `DA-13`, `DA-17` | stable | — | — |
| *System of record* and *source of truth* have **no formal vendor definition** — the pack's vocabulary is pack-local | `A3` | `DQ-03`, `DQ-15`, `U-14` | stable | — | — |

---

## 3. `data/dataverse.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| One parental relationship per child; cascading share and reparent propagate access | `A3` | `DA-05` | stable | — | — |
| Access-table rows cannot be deleted directly; sharing is exception-only and less performant; permissive reparent default | `A3` | `DA-11` | stable | — | — |
| Ownership type immutable at creation; privileges strictly additive; owning unit immutable; units and teams per environment, not solution-portable | `A3` | `DA-12` | stable | — | — |
| Region and residency fixed at creation; the boundary needs tenant **and** all environments; country granularity needs an extra entitlement | `A3` | `DA-57` | stable | — | — |
| Table, column and app names replicate globally; preview data region; some movement irreversible | `A3` | `DA-58` | stable | — | — |
| Long-term retention: managed class required, one-way, read-only, not solution-portable, audit and elastic excluded, cascades execute, day-scale run | `A3` | `DA-17` | volatile | `VC-07` **(stamped)**, `VS-05` | `G-039` |
| Long-term retention saves roughly half the database meter and **nothing** on files | `A3` | `DA-17` | volatile | `VC-07` **(stamped)** | — |
| Team-scoped upgrade one-way; needs capacity plus premium for all users; no interface or record sharing; ceiling not extendable | `A3` | `DA-13`, `DA-43` | stable | `VC-07` | — |
| Column schema name and type immutable; deleting a column deletes data; removing a choice option invalidates rows | `A3` | `DA-15`, `DA-33` | stable | — | — |
| File maximum size immutable after save; image conversion; upload outside form-save semantics | `A3` | `DA-14` | stable | — | — |
| **Alternate keys** are the server-side uniqueness constraint on all write paths, the **upsert** mechanism, and therefore the **idempotency** and **migration-idempotency** mechanism; bounded per table with column and width caps; not on secured columns or virtual tables; reserved characters break addressing | `A3` | `DQ-17`, `DA-53`, `DA-45` | stable | `VS-30` **(stamped)** | `G-040` |
| Duplicate detection is advisory, **suppressed by default on Web API updates**, has no default rules outside a few tables, and fails with a server-error class that naive retry loops on | `A3` | `DQ-12` | stable (oldest source — flagged) | — | — |
| **The vendor's documentation contradicts itself on whether table-scoped rules execute server-side** — carried as `Assumed`, never `Confirmed`, with the named empirical test | `A3` | `DQ-09`, `DQ-10`, `C-17` | **CONFLICTED — preserved** | — | `G-001` |
| Business rules are not retroactive | `A3` | `DQ-10` | stable | — | — |
| Table-scope vs form-scope split; unsupported column types; editable subgrids unsupported; silent no-op when a field is absent from the form; per-table rule ceiling | `A3` | `DQ-09`, `DQ-11` | stable | `VS-30` | — |
| Atomicity server-side only; the expression layer never transactional; elastic not atomic; cross-store saga with a pivot and a human fallback; compensations may themselves fail | `A3` | `DA-07`, `SC-06`, `DA-52` | stable | — | — |
| Outbound synchronous notification cannot be recalled on rollback | `A3` | `DA-50` | stable | — | — |
| Authorization planes; column security not on virtual, lookup, formula, primary-name or system columns; **never hidden from administrators**; masking needs the managed class | `A3` | `DA-55`, `DA-11` | stable | — | `G-069` |
| Managed environments gate retention, customer keys, vendor-access approval, firewall, private networking, masking, extended backups and sharing limits — premium entitlement for **all** users | `A3` | `DA-55`, `DA-61` | volatile | `VC-05`, `TW-V3` | `G-002` |
| Authorization does not travel into copies; secured columns export null; embedded reports ignore app roles | `A3` | `DA-22`, `C-07` | stable | — | — |
| Audit on the log meter; default indefinite; retention non-retroactive; truncation; read and export not audited; no export interface; customer keys remove the retention setting; excluded from the analytical endpoint and from retention | `A3` | `DA-16` | volatile | `VS-05` **(stamped)** | `G-036` |
| Backups and recycle bin are recovery, not retention | `A3` | `DA-18` | volatile | `VS-07` | — |
| Three meters with fixed placement by type; indexes on the database meter; borrowing database→log→file only; database overage cannot be offset | `A3` | `DA-04` | stable | `VC-07` | — |
| Over-capacity blocks create, copy and restore; headroom notifications; a disablement countdown | `A3` | `DA-27`, `DA-04` | volatile | `VS-09` | — |
| System tables grow on the database meter; storage-report lag; a full sandbox copy replicates data and index | `A3` | `DA-27` | stable | — | — |
| The analytical replica bills as **database** storage; the ratio is unpublished; *no copy* is marketing, not mechanism | `A3` | `DA-19`, `C-06`, `U-01` | volatile | `VC-07` | `G-030` |
| **Tenant default database capacity is internally inconsistent in the source** — neither figure carried | `A3` | `C-01` | **CONFLICTED — preserved** | — | `G-031` |
| Standard tables = strong-consistency criterion on a relational substrate; elastic = session consistency requiring a session token, no multi-record transaction, no deep insert | `A3` | `SC-06` | stable | `VS-32` | — |
| Elastic forfeits N:N to standard, rollups, alternate keys, duplicate detection, sharing, access teams, queues, business rules, charts, guided processes, the first-party analytical connector, the SQL endpoint, attachments, import/export and retention; point-in-time restore creates and deletes only; partition key immutable; partition size bounded | `A3` | `DA-09`, `SC-18` | stable | `VS-32` | `G-041` |
| **Elastic GA state unresolved** | `A3` | `C-02`, `U-02` | **UNRESOLVED — preserved** | `VS-32`, `VC-10` | `G-041` |
| Read-after-write across sessions, and read-replica behaviour, **not assertable** | `A3` | `U-27`, `U-28` | `UNKNOWN` | — | `G-034`, `G-035` |
| Rollups asynchronous with an hours-scale floor, bounded budgets, 1:N only, cannot trigger logic — **therefore cannot gate a write** | `A3` | `DA-06` | stable | `VS-30` | — |
| Formula and calculated columns computed at read time; sort, offline, trigger and search limits; not securable; filters throttled | `A3` | `DA-06`, `DA-55` | stable | — | — |
| Indexes platform-managed; hints support-gated; auto-optimisation makes issues irreproducible; the levers are schema and query shape | `A3` | `DA-26`, `SC-18`, `U-08` | stable / medium | — | `G-037` |
| Search: bounded org-wide field budget weighted by type, no related-table fields, eventually consistent with minutes-to-days lag, per-identity rate limit, index on the database meter, leading-wildcard throttling | `A3` | `DA-23`, `DA-26`, `C-12` | volatile | `VS-31` | — |
| Virtual tables: organisation-owned so **no row-level security**; no audit, column security, alternate keys, duplicate detection, derived columns, change tracking, search, offline, guided processes or site solutions; never the "1" side; column selection ignored; negative filters corrupt paging; absent from the delegable list; shared credential; **no published performance characterisation** | `A3` | `DA-45`, `VT-04`, `VT-05`, `VT-06`, `VT-09`, `VT-10`, `VT-17` | stable | — | `G-054` |
| Read-only virtualization over the lake surface; **no write-back** | `A3` | `VT-12`, `VT-13`, `VT-16` | stable | — | — |
| **No published standard-table size envelope** | `A3` | `SC-18`, `U-30` | negative finding | — | `G-026` |
| **No published concurrent-user ceiling**; funnel points are the real constraint; closed by load test | `A3` | `SC-16`, `SC-17`, `U-31` | negative finding | `VC-04` | `G-027` |
| **No published write-amplification multiplier** — internal system requests, plug-ins, classic workflows, retries and pagination all count; measure per engagement | `A3` | `SC-01`, `SC-02`, `SC-21` | negative finding | — | `G-028` |
| Solutions carry schema, not data; deleting a managed solution deletes its data; configuration data needs its own keyed pipeline; units, teams and retained data are not portable | `A3` | `DA-24` | stable | — | — |
| Aggregation ceiling is scope-specific, not a flat store limit | `A3` | `DA-03` (revised) | volatile | `VS-06` | — |
| Vocabulary is pack-local — no formal vendor definition of system-of-record | `A3` | `DQ-03`, `DQ-15` | stable | — | — |
| *Never migrate history* is pack opinion, not vendor guidance | `A3` | `DQ-05`, `U-41` | preserved as opinion | — | `G-033` |

---

## 4. `data/sharepoint.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Per-view threshold **cannot be changed** in the online service; capacity is not the binding boundary | `A3` | `DA-39` | volatile | `VS-04` **(stamped)** | `G-056` |
| Narrowest delegable set; **silent partial results, not slow ones** | `A3` | `DA-39`, `C-09` | volatile | `VS-02` | `G-003` |
| Flow item retrieval has a low default page size, fails past the threshold without pagination, and can return **no** records when the filter misses inside the first window | `A3` | `DA-39` | volatile | `VS-04` | — |
| Join ceiling per view counting lookup, person and metadata columns; the retrieval actions **fail** above it; integrity opt-in per lookup, delete-only, needs list-manage permission, stops past the threshold; row-byte budget; the vendor's advice is to denormalise and partition; the canvas client cannot project columns | `A3` | `DA-40` | stable mechanism | `VS-33` **(stamped)** | — |
| Unique-permission supported and recommended ceilings; inheritance cannot be broken past a higher item count; **no column-level security**; customised forms inherit list read; list edit rights write through other clients; per-item automation is significant operational overhead | `A3` | `DA-42` | volatile figures | `VS-29` **(stamped)** | `G-045` |
| Validation ladder: list- and column-level formulas, unavailable on some types, **row-local**, single-column uniqueness | `A3` | `DQ-13` | stable | — | — |
| Boolean type inconsistency produces wrong data and empty visuals; decimal precision blocks the quick model; **sensitivity label not inherited**; report content follows the connection identity | `A3` | `DQ-14` | stable | — | — |
| Documents-as-record fit; retention labels on items but **not attachments**; recycle bin; versioning; lists sit **outside solutions** with site and list variables required and internal names drifting on recreation; external sharing on by default; guest members can delete; inactive-site archive; conversion is a one-time copy | `A3` | `DA-44` | stable | — | — |
| Labels attach protection that survives download; large encrypted files break on move; **no label mechanism for list items or columns**; the pattern is not item-level security | `A3` | `DA-59`, `DA-42` | stable | — | — |
| Standard connector class on seeded rights pairs with the lowest automation profile; polling triggers coalesce; delete trigger needs a site-collection administrator; item-menu automations only in the default environment | `A3` | `DA-43` | volatile | `VS-03`, `VS-14`, `VC-02` | — |
| **Correction:** a dedicated tenant-or-geo customer-key policy exists for this store — the limit is **granularity**, plus premium entitlement, two paid subscriptions and separate onboarding | `A3` | `SQ2-10` | stable (correction) | — | — |
| The documented positive shapes: the document as the record; small flat trackers; list-level security; forms over one list; seeded licensing outside the team surface | `A3` | §6 alternatives | stable | — | — |
| *The relational store is preferred where more complex relational data is needed* — carried as a **trigger**, never a verdict | `A3` | `DA-44` evidence | stable | — | — |

---

## 5. `data/azure-sql.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Connector rate and concurrency ceilings per connection and per user; **time-based** connection throttling; action timeout with a layered client timeout and retries; **implicitly shared connections share ONE budget** | `A3` | `DA-32`, `SQ2-11`, `C-14` | volatile | `VS-27` | `G-050` |
| Views read-only; stored procedures un-paged, static schema, no refresh primitive, re-invoked on control refresh; large touched fields cause timeouts | `A3` | `DA-30`, `DA-31`, `SQ2-11` | stable | — | — |
| Managed-instance hostnames reject simple auth; directory connections exclude guests; managed identity only in the sibling service; private-network mode closes the action list and **excludes the gateway** | `A3` | `SQ2-11` | stable | `VS-11` | `G-051` |
| Implicit connections reuse the maker's credentials and let users author new apps; secure-implicit is hygiene only; legacy Windows auth *is not secure*; the gateway uses the stored credential regardless of user; a shareable service principal means **all users have the same rights**; app-granted permissions do not deny data-source permissions | `A3` | `DA-33`, `SQ2-15` | stable | — | — |
| Row-level security enforces in the database tier on every access; filter versus block predicates; the principal-name basis needs a real per-user principal and the session-context basis needs a middle tier with **no documented maker hook**; applies to database owners; leak channels; indexed views incompatible; history tables not auto-covered | `A3` | `SQ2-08` | stable mechanics / medium-high inference on the connector coupling | — | `G-048` |
| Schema gate: primary key required for writes, small-integer types invalid as keys, server-side triggers break insert and update, identity plus row-version required for change triggers, unsupported types, protocol-conformant identifiers, views read-only | `A3` | `DA-30` | stable | — | — |
| The low-code expression layer is never transactional; a stored procedure with an explicit transaction is the mechanism | `A3` | `DA-07`, `SQ2-15` | stable | — | — |
| The gateway shrinks the procedure contract: no output parameters, no return value, first result set only, no dynamic schemas | `A3` | `DA-34`, `SQ2-11` | stable | `VS-10` **(stamped)** | — |
| **Log rate is the sustained-write ceiling and is flat across the upper compute range**; per-tier storage ceilings; sessions generous, workers scale with compute | `A3` | `SQ2-07` | volatile | `VS-34` | — |
| High-ingest timestamped metrics routed to a purpose-built time-series service; relational listed only under consistent transactional operations | `A3` | `SQ2-06` | stable | — | — |
| Long-term retention is **backup** retention, restorable only as a new database; coarse granularity; vendor-controlled timing with a multi-day first appearance; not retroactive; same-subscription restore | `A3` | `SQ2-04` | volatile | `VS-07`, `VS-17` | `G-052` |
| **No cold or archive tier for rows**; cheapness means partitioning plus archival compression or moving data out; the historical in-product answer is deprecated (unclosed) | `A3` | `SQ2-05`, `SQ2-14`, `U-36` | stable | — | `G-049` |
| The connector **cannot bulk-load**; a separate toolchain is implied; **no published throughput**, only a bandwidth-derived method and *measure it yourself*; minimal-logging preconditions; replication forces full logging; the managed recovery model is `UNKNOWN` | `A3` | `SQ2-12`, `SQ2-13`, `U-35` | stable | — | `G-047`, `G-053` |
| Customer key real and scopeable at server, instance and database level; revoke-to-deny; switch-on online with no re-encryption; vault soft-delete and purge protection mandatory; minutes to denial, a short window to inaccessible, **no automatic healing** past it; collateral loss of settings; old backups not re-keyed; per-vault ceilings | `A3` | `SQ2-01`, `SQ2-02` | stable mechanics / volatile windows | `VS-35` | — |
| The asymmetry against the governed store: no licence gate beyond the subscription here; managed class **and** a premium compliance entitlement there | `A3` | `SQ2-09` | stable | `VC-05` | `G-077` |
| Private path: tenant-associated subscription, delegated subnets in both paired regions, address allocation per production environment, newer action versions only, **gateway unsupported**, public calls break; otherwise a recurring allowlist refresh; auto-pause produces predictable transient failures | `A3` | `DA-36` | volatile | `VS-11`, `VS-28` | — |
| Gateway payload ceilings; results transit the cloud and spool on the host; *no transit of row data through the vendor cloud* is **not achievable** | `A3` | `DA-34` | volatile | `VS-10` **(stamped)** | — |
| Gateway estate: separate development and production clusters, a node minimum, high availability with random distribution opt-in and primary-first default, monthly cadence with a bounded supported window, recovery-key custody as a business risk, and the vendor *does not investigate poor performance when a gateway is overloaded* | `A3` | `DA-35` | volatile | `VS-11`, `VS-28`, `VC-08` | `G-007` |
| **Database lifecycle sits outside the platform's lifecycle** | `A3` | §2 row 24, `DA-24`, `DA-44` | stable | — | — |
| **No first-party managed replication into a writable relational store** — any writable copy is customer-built and customer-operated | `A3` | `SY-01`, `SY-18`, `C-19` | point-in-time negative | `VC-10` | `G-032` |
| Two control planes — *plan for governance across both* | `A3` | `DA-37` | stable | — | — |
| Connector-level data policy governs which systems an app may talk to, **not the data**, with hours of enforcement latency and artefact suspension | `A3` | `DA-63` | stable | `VS-21` | `G-004` |
| Reference-architecture **triggers**: new app plus new storage → the governed store; data that cannot move → the app over this store; private-network topology; directory or service-principal auth; delegate complex work to views and procedures | `A3` | `SQ2-15` | stable | — | — |
| Entitlement is neutral between this store and the governed one; both are separated from the standard class | `A3` | `DA-61`, `DA-38` | stable | `VC-05` | — |
| **Correction:** this store is not the cheap archive, and not the answer for high-ingest telemetry | `A3` | `SQ2-04`, `SQ2-05`, `SQ2-06` | stable (correction) | — | — |
| Connector concurrency, isolation, locking and deadlock-retry semantics are `UNKNOWN` | `A3` | `U-05` | `UNKNOWN` | — | `G-050` |
| Whether a maker can set session context on the connector's connection is **open and decisive** for per-user row security | `A3` | `U-37` | `UNKNOWN` | — | `G-048` |
| Gateway node throughput for platform traffic is `UNKNOWN` | `A3` | `U-09` | `UNKNOWN` | — | `G-007` |

---

## 6. `data/query-and-delegation.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| A non-delegable query fetches the first N rows and evaluates locally; **default and maximum** | `A3`, `A9` | `DA-02`, `PF-01`, `VT-10` | volatile | `VS-02` **(stamped)** | — |
| **If any part of the expression is non-delegable, no part is delegated** | `A3` | `VT-10` | stable | — | — |
| The failure is silent wrongness, not slowness | `A3`, `A9` | `PF-01`, `DA-02` | stable | — | — |
| The ceiling is **per query, not per app**; below the default any source or formula works | `A9` | `PF-01` | stable | `VS-02` | — |
| The row limit set to **1** is the proof, not warning count | `A3`, `A9` | `PF-02`, `DA-02` | stable | — | — |
| Two traps produce **no warning at all**: internally-created collections, and a source absent from the delegable list | `A9` | `PF-02` | stable | — | — |
| Exactly four delegable tabular sources are named; anything else is non-delegable and warning-free | `A3` | `VT-10` | volatile membership | `VS-02` | `G-003` |
| Governed store broadest; relational-via-connector partial; list store narrowest; spreadsheet and collections none | `A3` | `DA-02` | stable | — | — |
| Relational-connector non-delegable classes: text ranges, blank, numeric search, date max/min; **date predicates fail through the gateway**; stored procedures un-paged, static schema, not refreshable, re-invoked on control refresh | `A3` | `DA-31` | stable | — | — |
| List-store classes: negation never; identity equality only; blank and sort not on text-complex; person email and display-name only; prefix match not on choice or lookup subfields; conjunction and disjunction delegate | `A3` | `DA-39` | stable | — | — |
| **The list store does not support the count function** — plain and conditional counting are not delegated | `A3` | `SC-12` | stable | — | — |
| Spreadsheet is not a relational database; **no transaction threshold is published** — decide on shape | `A3`, `A9` | `DA-41`, `PF-26` | stable (vendor-stated absence) | — | — |
| Custom-connector paths: **no delegation** | `A3` | §2 store-fit matrix row 2 | stable | — | — |
| Virtual tables absent from the delegable list; the ceiling applies; **no warning at all**; column selection ignored; negative filters corrupt paging with no supported workaround | `A3` | `VT-10`, `DAP-34`, `DAP-35` | stable negative finding | — | `G-054` |
| **Custom-connector throughput ceiling `CONFLICTED`, symmetric, decision-blocked** | register + `A9` | `PF-27`, `IA-C-01 (C-01)`, `MF NB-02` | **CONFLICTED** | `VC-01` / `VS-08`, `B-08`, `CD-05` | `G-058` |
| Galleries page in small increments; server-side views plus mandatory search arguments; explicit column selection on by default | `A3` | `SC-12` | stable | — | — |
| **A plain count returns a periodically-recalculated table size**; an exact count needs conditional counting up to the aggregation ceiling | `A3` | `SC-12` | volatile ceiling | `VS-06` **(stamped)** | — |
| The list store returns **every defined column even if unused** | `A3`, `A9` | `PF-24`, `DA-40` | stable | — | — |
| **List-view threshold cannot be changed**; the item ceiling is far higher; both are search-derived in the baseline | `A3`, `A9` | `DA-39`, `PF-24` | volatile | `VS-04` **(stamped)** | `G-056` |
| The vendor publishes **limits, not benchmarks** — *no limit violated* is not *fast* | `A9` | §0 reading rule | stable | — | `G-063` |
| Two dominant layers: back-end processing plus client sending and processing; the governed store skips a layer | `A9` | `PF-05` (aged — flagged) | aged, medium | — | `G-099` |
| Tuning order: do not call → fewer and wider calls → only then parallelism, re-checking the connector throttle | `A9` | `PF-28`, `PF-27` | stable | `VS-27` | — |
| Prefilter at the server; one view per screen; enterprise apps make heavy use of views | `A3` | `SC-11`, `SC-12`, `SC-13` | stable | — | — |
| N+1 per-row lookup; an index-leveraging predicate beats whole-table membership | `A3` | `SC-13` | stable | — | — |
| Cache the static; invalidation required where data changes; volatile and sensitive values always from the primary source | `A3` | `SC-11`, `DAP-23` | stable | — | — |
| Freshness is a **negotiable business requirement** | `A3` | `SC-13` | stable | — | — |
| Governed-store indexes are platform-managed; auto-tuning on by default; hints only on vendor-support recommendation; the levers are schema and query shape | `A3` | `DA-26` | stable (medium) | — | `G-035`, `G-037` |
| Throttled shapes: leading-wildcard containment, computed-column filters, choice and related-column sorts | `A3` | `DA-26`, `DAP-26` | stable | — | — |
| Flow-side item retrieval has a low default page size, fails above the threshold without pagination, and **returns nothing when the filter matches nothing in the first window** | `A3` | `DA-39` | volatile | `VS-04` | — |
| Bounded lookup levels, stricter offline, and bounded expandable entities; the remedy is a server-side view — a data-model change | `A9` | `PF-03` | volatile | `VS-33` | — |
| **The three prior copies disagreed** on the client ceiling, on counting delegability, and on index-gated lookup delegation; all three resolved against canonical only | migration sources vs `A3` | `DA-02`, `SC-12`, `DA-26` | resolved | `VS-02` | — |
| The prior growth ladder and its *no longer appropriate → migrate* verdict were **invented thresholds plus a selection verdict** — not carried in any form | migration source | — | removed | — | — |

---

## 7. `automation/automation-mechanisms.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Four shapes distinguished by **where state lives** and **what the unit of failure is**; ordered classification test | `A4` | §2 (INF taxonomy over MS facts) | stable (synthesis) | — | — |
| A cloud flow is a workflow engine and a front door — **not a state store, not a broker, not a compute host** | `A4` | §2, `AT2-18`, `AT2-21`, `AT2-32` | stable | — | — |
| Three independent meters; **the binding constraint is the smallest**, normally the connector or service-protection one | `A4` | `AT2-02` | stable | `VC-04`, `VS-27` | — |
| Size against the **official** entitlement limits, not the transition-period approximations; the enforcement date is unannounced | `A4` | `AT2-03`, `C-02` | volatile | `VC-04` | — |
| Content throughput per 24 h by owner profile — a document-moving flow hits it first; the remedy is to pass a reference | `A4` | `AT2-02`, `AT2-14`(A5) | volatile | `VS-03` **(stamped)** | — |
| RPA queue: bounded waiting depth, maximum wait, dispatch latency, per-run ceiling, and an auditability ceiling | `A4` | `AT2-37`, `AT2-38` | volatile | `VS-16` **(stamped)** | — |
| Throughput class follows the **owner's licence**, and reverts on the owner's departure | `A4` | `AT2-01` | stable | `VS-39` | — |
| Distribute across service principals; **plug-in-originated data operations are exempt from service protection** | `A4` | `AT2-04`, `AT2-35` | stable | `VC-04` | — |
| Structural definition ceilings on action count, nesting, array items — **identical on both platforms**, and the documented remedy on both is decomposition | `A4` | `AT2-30` | volatile | `VS-24` **(stamped)** | — |
| The **synchronous-response boundary is a platform-family property**; the ceilings differ by degree; above it the requirement must change; respond-then-continue is the documented escape | `A4` | `AT2-12`, `AT2-32` | volatile | `VS-23` **(stamped)** | `G-098` |
| Run duration is the one boundary where relocation is genuinely supported by a limit; the stateless variant is a trap | `A4` | `AT2-13` | volatile | `VS-12`, `VS-13` **(stamped)** | — |
| Beyond the ceiling the architecture changes shape — the process record becomes the state and the flow a resumer | `A4` | `AT2-14` | stable | — | — |
| A wait held in run state does not survive redeployment | `A4` | `AT2-14` | stable | — | — |
| In-database extension runs **inside the transaction**, can veto, and is exempt from service protection | `A4` | `AT2-35` | stable | — | — |
| Guided rails carry published caps and **no logic of their own** | `A4` | `AT2-36` | stable | `VS-25` | — |
| The compute host's **plan is part of the decision**; a hard HTTP cap applies on every plan | `A4` | `AT2-32` | volatile | `VS-23` | — |
| Durable orchestration: replay is exactly why versioning is dangerous; the framework's own guard is unreliable; side-by-side or version-specific hubs are the named strategies | `A4` | `AT2-33`, `AT2-34` | stable | — | — |
| **Retry duplicates non-idempotent side effects** — the vendor states plainly that retrying a non-idempotent operation corrupts data | `A4` | `AT2-16` | stable | — | — |
| Retry defaults differ by profile and by product; the commonly-quoted default belongs to the sibling product | `A4` | `AT2-15`, `C-04` | volatile | `VS-39` **(stamped)** | — |
| **One retry owner per call chain**; disable or reduce the others; prefer the response's own back-off signal | `A4`, `A5` | `AT2-55`, `IA-44` | stable | — | — |
| Idempotency mechanism is an alternate key with upsert, with a sanitised surrogate where the natural key is unusable | `A4` | `AT2-16`, `AT2-56` | stable | `VS-30` | — |
| **Serialising the trigger introduces trigger loss, collapses de-batching, and is irreversible**; ordering at volume is a broker requirement | `A4` | `AT2-06`, `AT2-57` | volatile | `VS-24` **(stamped)** | — |
| Deduplication is a **transport** property; among the three brokers only one has transactions, dedup and dead-lettering; the connector's session cache is bounded and evicting | `A4` | `AT2-18`, `AT2-26`, `AT2-28` | stable | `VS-10` | `G-008` |
| **There is no rollback**; a mid-loop failure leaves an unknown prefix; the design must answer three questions in writing | `A4` | `AT2-21` | stable | — | `G-060` |
| Atomicity exists only inside the governed store; the change set cannot loop or chain outputs; a second system makes all-or-nothing **not expressible**; test the compensation exclusion first | `A4` | `AT2-19`, `AT2-17` | stable | — | — |
| Trigger outage behaviour fails in opposite directions and neither is safe by default | `A4` | `AT2-22` | stable | `VS-14` | — |
| **Sustained breach turns the flow off**, and editing resets the counters; throttling rate is a monitored leading indicator | `A4` | `AT2-10`, `AT2-43`, `AT2-61` | volatile | `VS-09` **(stamped)** | — |
| The synchronous outbound webhook is a **documented dual-write hazard** | `A4`, `A3` | `AT2-29`, `DA-50` | stable | — | — |
| Approvals: data-platform-backed, **standard connector**, several response models, persisted history — the strongest argument for splitting at the human boundary. **Escalation and reassignment mechanics are not established** | `A4` | `AT2-23`, `AT2-24`, `U-03`, `C-06` | stable / `UNKNOWN` | `VS-15` | `G-059` |
| Interface automation: attended and unattended are different architectures; the **queue** is the deciding constraint; prefer an API on the vendor's own stability grounds; a bridge with an exit condition; credential hygiene is admin-configured | `A4` | `AT2-37`, `AT2-38`, `AT2-39`, `AT2-40` | stable | `VS-16` | — |
| Secrets have three documented homes and one anti-home | `A4` | `AT2-50` | stable | — | — |
| The nine corrected myths | `A4` | §14 *(myth vs mechanism)* | stable | — | — |
| Hybrid is a **second operating model** requiring three named commitments | `A4` | `AT2-53` | stable | — | — |
| A flow acts as the **connection owner**, not the triggering user, unless configured otherwise | `A4` | `AT2-48` | stable | — | — |
| Solution-awareness plus connection references make a flow deployable; a non-solution flow is an ALM dead end with **no ownership fix** | `A4` | `AT2-45`, `AT2-44` | stable | — | — |
| Native run history is short-retention and **not a business record** | `A4` | `AT2-41` | volatile | `VS-18` | `G-115` |
| Telemetry export is **managed-class-only, not lossless, and unavailable in sovereign clouds** | `A4` | `AT2-42` | volatile | `VC-05`, `VS-18` | — |
| **No empirical throughput or latency figure exists** for any mechanism here | `A4` | `U-10` | measurement | — | `G-063` |
| **No unit- or contract-test mechanism** for a flow definition | `A4` | `U-09` | `UNKNOWN` | — | `G-061` |
| Whether the platform states cloud flows lack native ordering, dedup or peek-lock is an **absence inference** — *unsupported until verified* | `A4` | `U-04` | INF, marked | — | `G-011` |
| Process-entitlement stacking cap: **the sources disagree** — neither figure encoded | `A4` | `C-01`, `U-11` | **CONFLICTED — preserved** | `VC-05` | `G-062` |
| Broker quota envelopes for two of three services **not fetched** — selection evidence only | `A4` | `U-13` | `UNKNOWN` | — | `G-008` |
| The general-purpose-backend framing must not be encoded as a vendor statement; the narrower sourced claim is used instead | `A4` | `AT2-66`, `AT2-58` | stable | — | — |
| Agent / conversational automation: the baseline is silent; the deferral had no owner | `A4` | `U-14` | `UNKNOWN` | `VS-20` | `G-119` |

---

## 8. `integration/integration-mechanisms.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Twelve requirement dimensions, each a requirement → constraint → consequence chain | `A5` | §2.1, `IA-01`…`IA-16` | stable | per row | — |
| Volume must be **projected over the investment horizon** with a growth rate | `A5` | `IA-01` | stable | — | — |
| **Frequency, not volume, selects the trigger class**; two mechanisms may legitimately serve one dataset | `A5` | `IA-02`, `IA-03` | stable | — | — |
| Directionality is fixed by the **network posture of the weaker party**; the documented remedy is to invert the caller | `A5` | `IA-04` | stable | — | — |
| **The weakest system in the chain sets the ceiling**; the target's own capability is a required input, and `Unknown` there is decision-blocking for a high-frequency stream | `A5` | `IA-06` | stable | — | — |
| Only two structural moves once the weak end is fixed: caching spends **freshness**, buffering spends **latency** | `A5` | `IA-07` | stable | — | — |
| One goal decomposes into N **streams**; elicit a stream inventory; a single verdict per system pair is a smell | `A5` | `IA-05`, `IA-28` | stable | — | — |
| The ordered topology test, with **ownership first** | `A5` | §2.2 (INF ordering over MS constraints) | stable (synthesis) | — | — |
| Mechanism envelope table with the dimension each fails on first | `A5` | §3, `IA-10`…`IA-14` | volatile figures | `VS-27`, `VS-10` | `G-067` |
| Connector throttles are **per connection**, making the connection a capacity-planning object | `A5` | `IA-11` | volatile | `VS-27` **(stamped)** | — |
| The delegated-identity HTTP mechanism is the tightest throttle here and **cannot carry binary payloads** | `A5` | `IA-12` | volatile | `VS-27` **(stamped)** | — |
| Custom connectors are capped in **count** as well as rate, and the count is licence-dependent | `A5` | `IA-13` | volatile | `VC-05` | — |
| **Content throughput is metered in bytes**, and document-heavy integrations hit it before the request meters | `A5` | `IA-14` | volatile | `VS-03` | — |
| Delivery guarantee, ordering, dedup and dead-lettering are **properties of the transport** | `A5` | `IA-15` | stable | — | — |
| **A consistently throttled flow is turned off** — throttling is an availability risk with a fuse | `A5` | `IA-16` | volatile | `VS-09` | — |
| **Retry policy differs by licence profile** — resilience is a property of the owner | `A5` | `IA-17` | volatile | `VS-39` | — |
| Concurrency knobs and a burst cap are the **only** back-pressure controls, and enabling concurrency control **can drop triggers irreversibly** | `A5` | `IA-18`, `IA-22` | stable | `VS-24` | — |
| **Atomicity stops at the governed store's boundary**; three choices, and the design records which | `A5` | `IA-19` | stable | — | — |
| Batch semantics: bounded requests, all-or-nothing change sets, **abort-on-first-error unless a header is set** | `A5` | `IA-20` | volatile | `VS-10` **(stamped)** | — |
| Synchronous outbound notification is a **documented dual-write hazard** | `A5` | `IA-21` | stable | — | — |
| **Five testable justifications for an API layer**, and the cases where it is unnecessary complexity | `A5` | `IA-49`, §4.2 | stable | — | `G-111` |
| Even where a gateway is justified, heavy logic belongs **behind** it | `A5` | `IA-49`, §4.2 | stable | — | — |
| Gateway payload caps are far below the platform's message limits, so document-oriented on-premises integration cannot pass through in its naive form | `A5` | `IA-27` | volatile | `VS-10` **(stamped)** | — |
| **The broker path and the private-network path are mutually exclusive** through the transaction-scoped mechanism | `A5` | `IA-28` | stable | `VS-11` | `G-113` |
| Private networking is an **outbound** control with substantial preconditions that **breaks public calls by design**; identity traffic does not traverse it | `A5` | `IA-29` | volatile | `VS-11` **(stamped)** | — |
| Three private-connectivity mechanisms answer **different** questions; the wrong one is unsupported, not slow | `A5` | `IA-30` | stable | `VS-11` | — |
| **Managed identity is GA for in-database plug-ins only**; a *no stored secrets* requirement therefore relocates the integration | `A5` | `IA-31` | volatile | `VC-10` | `G-010` |
| A custom connector **cannot use the client-credentials grant** | `A5` | `IA-32` | stable | — | — |
| Delegated versus service identity is a fork with consequences for authorization, throughput and audit | `A5` | `IA-33` | stable | — | — |
| **Virtual tables cannot enforce row-level authorization** — so a compliance requirement there excludes virtualization | `A5` | `IA-34` | stable | — | — |
| Secrets belong in a vault surfaced through environment variables, with a stated rotation cadence | `A5` | `IA-35` | stable | — | — |
| System of record is assigned **per entity, per field and per lifecycle phase**; the transfer point is where the integration lives | `A5` | `IA-36` | stable | — | — |
| **The vendor's own reference architecture excludes financial posting entities from bidirectional sync by design** | `A5` | `IA-37` | stable | — | — |
| Tightly-coupled bidirectional sync is the vendor's own name for it and **mutates the receiving schema** | `A5` | `IA-38` | stable | — | — |
| The synchronization risk register — thirteen risks with the mitigation actually available | `A5` | §8, `IA-41`…`IA-43` | stable bases | — | `G-064` |
| **The documented synchronization shape is two mechanisms plus a reconciliation pass** | `A5` | `IA-41` | stable | — | — |
| Synchronization becomes a **risk** rather than a mechanism at identifiable thresholds; the answer is a topology change | `A5` | `IA-42` | stable | — | — |
| Freshness in virtualization is bounded by the **upstream** refresh | `A5` | `IA-43` | stable | — | — |
| **No in-platform dead-letter or circuit-breaker construct** — an escalation trigger, not something to approximate | `A5` | `IA-46`, `U-11` | INF absence, marked | — | `G-011` |
| Every asynchronous integration needs a **status resource** | `A5` | `IA-47` | stable | — | — |
| Trigger conditions are the documented remedy for loop prevention and wasted executions | `A5` | `IA-48` | stable | — | — |
| The nine EXTERNAL conditions, and the four things that are **not** reasons to move the integration out | `A5` | §12, §12.9 | stable | — | — |
| **The conflicted per-connection ceiling — 20×, symmetric, decision-blocked** | `A5` + register | `IA-C-01 (C-01)`, `MF NB-02` | **CONFLICTED** | `VC-01` / `VS-08`, `B-08`, `CD-05` | `G-058` |
| Business-events throughput and quota **not published** | `A5` | `IA` §3, `U-13` | `UNKNOWN` | — | `G-065` |
| **No measurement anywhere** — this domain reasons entirely from published limits | `A5` | §13.1 item 4, `U-04` | measurement | — | `G-066` |
| The connector pages carrying the load-bearing throttle figures are the **weakest-dated** sources in the baseline | `A5` | §13.1 item 2 | volatile | `VS-27` | `G-067` |

---

## 9. `security/security-controls.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Five enforcement planes with enforcer, grain and independent failure | `A6` | §1 table | stable | — | — |
| **The lowest-plane rule** — a requirement must be satisfied on the lowest plane that can enforce it | `A6`, `AP` | §1 closing rule (INF), `AP-D-030` | stable (synthesis, marked) | — | — |
| Worked negative case: an app-hidden column readable through the same connection by any other client | `A6`, `A3` | `SEC-18`, `DA-42`, `DA-33` | stable | — | — |
| Conditional access misses one automation application id; the tier dependency | `A6` | `SEC-02` | volatile | `VC-10` | — |
| Application users bypass the security group and the firewall default | `A6` | `SEC-05`, `SEC-16`, `SEC-27` | stable | — | — |
| Continuous access evaluation exists, scoped to the governed store only | `A6`, `A5` | `SEC-03`, `IA-33` | stable | `VS-22` | — |
| The environment is the security boundary; no cross-environment data access; geography-bound | `A6` | `SEC-15` | stable | — | — |
| The default environment: undeletable, no security group, all makers | `A6`, `A7` | `SEC-17`, `GOV-04` | stable | — | — |
| Privileges are additive, never subtractable | `A6`, `A3` | `SEC-08`, `DA-12` | stable | — | — |
| Ownership type fixed at creation; owning unit immutable; disabling the matrix model rewrites ownership; the root unit cannot change | `A6`, `A3` | `SEC-09`, `SEC-10`, `DA-12` | stable | — | — |
| Column security **never applies to a system administrator**; excluded column classes; calculated and composite leakage | `A6`, `A3` | `SEC-13`, `DA-55` | stable | — | `G-069` |
| Sharing is an exception mechanism; access rows cannot be deleted directly and grow on the storage meter | `A3`, `A6` | `DA-11`, `SEC-12` | stable | — | — |
| Authorization grain per store | `A3` | `DA-42`, `DA-33`, `DA-59`, `SQ2-08` | stable / volatile list-store figures | `VS-29` | `G-045` |
| **Row-level security collapses behind a shared connection**; the session-context basis needs a mediation tier | `A3`, `AP` | `SQ2-08`, `DA-33`, `AP-D-032` | stable | — | `G-048` |
| A flow runs as the **connection owner**; ownership is not transferable from solutions; co-owner is near-total; environment administrators see payloads | `A6` | `SEC-21`, `SEC-22` | stable | — | — |
| Secured implicit connections: hygiene, eight limitations, republish requirement, and a connection-reference known issue | `A6` | `SEC-19` | volatile (known-issue state) | `VC-10` | `G-073` |
| Gateway plus legacy Windows auth is documented as **not secure**; installer control is not per environment | `A6` | `SEC-20`, `SEC-31` | stable | — | — |
| **Virtual tables cannot carry row-level authorization** | `A5`, `A6` | `IA-34`, §8 deferral | stable | — | — |
| Delegated versus service identity fork; throughput concentrates per identity | `A5` | `IA-33` | stable | `VC-04` | — |
| Data policies are **connector-aware, not connection-aware**; not per user; tenant overrides environment; most restrictive wins; combinatorial fragmentation | `A6`, `A7` | `SEC-23`, `GOV-10` | stable | `VC-03` | — |
| The enforcement chain suspends and quarantines artefacts and disables connections, **with latency in hours** | `A6` | `SEC-23` | volatile | `VS-21` | `G-004` |
| The allowlist policy is default-deny, certified connectors only, never virtual connectors, and its availability is per maker portal | `A6`, `A7` | `SEC-24`, `GOV-11b` | volatile | `VC-03`, `VC-10` | `G-075` |
| Endpoint filtering ignores environment variables, custom inputs and runtime endpoints | `A6` | `SEC-25` | volatile | `VC-10` | — |
| Tenant isolation covers directory-based connectors only, with a named gap and the guest case unevaluated | `A6` | `SEC-26` | stable | `VS-21` | — |
| IP firewall: governed store only, managed class, audit-mode default, application users allowed, premium-suite licences | `A6`, `A3` | `SEC-27`, `DA-55` | volatile | `VC-05` | `G-077` |
| Customer key: exclusion list, disable-during-encryption, restore lock, reset deletes backups, audit retention unavailable, a malicious-lock scenario, separation of duties | `A6`, `A3` | `SEC-29`, `SEC-34`, `DA-55`, `SQ2-09` | volatile | `VS-35`, `VC-10`, `VS-17` | — |
| Vendor-access approval is a managed-class control with exclusions | `A3`, `A7` | `DA-55`, `GOV-06` | stable | — | — |
| Private networking is outbound-only; immutable subnet and DNS; region pairing; internet egress open by default; a certificate-chain requirement; the event path is not supported on it | `A6`, `A5` | `SEC-30`, `IA-28`, `IA-29` | volatile | `VS-11`, `VC-10` | `G-113` |
| Vault secrets are consumable by three component types only; canvas apps have none; a secret in an action input is readable from run history | `A6`, `AP` | `SEC-07`, `AP-D-031` | stable | — | — |
| **Managed identity GA for in-database plug-ins only** | `A6`, `A5` | `SEC-06`, `IA-31` | volatile | `VC-10` | `G-010` |
| External surface: cumulative web roles; table permission required and role-bound; the broadest access type means all rows; a private-access list in an environment variable; certificate and key expiry | `A6`, `AP` | `SEC-32`, `AP-D-034` | stable | — | `G-076` |
| Sharing limits are **forward-only**; the organisation-wide group is unviewable and uneditable | `A6` | `SEC-38` | stable | `VS-21` | — |
| The compliance platform is **discovery and classification, not enforcement** | `A6`, `A3` | `SEC-40`, `DA-59` | volatile (depth unverified) | — | `G-071` |
| The security score is preview, evaluation-only, with no further investment, and actionable only in the managed class | `A6` | `SEC-35` | volatile | `VC-10` | — |
| Managed environments gate nearly every strong control; **every active user is in scope, including standard-app users**; a dated enforcement | `A7`, `A6` | `GOV-06`, `GOV-11`, `SEC-XB-01` | volatile | `TW-V3`, `VC-05` | `G-002`, `G-080` |
| Audit: no retrieve or export coverage, a licence gate for deeper audit, retention stamped at write time, consumes log capacity, export unsupported | `A6` | `SEC-34` | volatile | `VS-05`, `VS-19` | `G-072` |
| Environment groups lock settings read-only with no per-environment exception; creation control is not retroactive | `A7` | `GOV-07`, `GOV-08`, `GOV-09` | stable | — | `G-081` |
| **External components sit outside platform data policies** — a second plane needing an owner | `A6` | `SEC-XB-02` | stable | — | — |
| Roles and column-security profiles travel in solutions; units and teams must be created per environment; the deploying identity owns deployed objects | `A6` | §12.2 items 1, 2, 6 | stable | — | — |
| **No numeric curve relating security-model complexity to runtime performance** — a representative pilot is the only closure | `A6`, `MF` | `SEC-XB-03`, `NB-04` | `UNKNOWN` preserved | — | `G-078` |
| Compensation and replay identities are privileged integration identities | `A6` | `SEC-XB-04` | stable | — | — |
| Thirteen controls are **partial by design** | `A6` | §1–§4 synthesis over the plane table | stable | — | — |
| Ten **irreversible** security decisions | `A6`, `A3` | `SEC-09`, `SEC-10`, `DA-57`, `SEC-29` | stable | — | — |
| The residual-risk statement obligation | `A6` | §12, §14 | stable | — | — |
| Control-obliged population lands in economics | `A10`, `A7` | `LC-30`, `GOV-11` | volatile | `VC-05`, `TW-V3` | `G-002` |
| Hierarchy security mechanics **not established** in the baseline | `A6` | §8 deferral | `UNKNOWN` | — | `G-068` |
| Guest-restriction availability state: **two sources disagree** | `A6`, `A7` | `SEC-04`, `GOV-25` | **CONFLICTED — preserved** | `VC-10` | `G-074` |

---

## 10. `governance/governance-and-environments.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Eight levers, each stated by **what it mechanically prevents** | `A7` | §1, `GOV-02`…`GOV-20`, `GOV-XB-01` | stable | — | — |
| Levers 1–6 preventive and managed-gated; 7 detective; 8 boundary | `A7` | §1 consequence, `GOV-13` | stable | — | — |
| **Preventive levers are forward-only; only detection is retroactive** | `A7` | `GOV-09`, `GOV-19` | stable | — | — |
| Creation restriction does not reach existing environments | `A7` | `GOV-09` | stable | — | — |
| A promotion path must exist **before** makers are enabled | `A7`, `AP` | `GOV-02`, `GOV-08`, `AP` §5.6 | stable | — | — |
| The environment is simultaneously a security, governance, policy, residency and licence unit | `A6`, `A7` | `SEC-15`, §13 | stable | — | — |
| The default environment: no group, no backup guarantee, all makers, inflow from lists and chat, and a developer-environment restore target | `A7`, `A6` | `GOV-04`, `GOV-05`, `SEC-17` | stable | — | — |
| Production-to-sandbox conversion **cannot be blocked** | `A7` | `GOV-03`, `GOV-09` | stable | — | — |
| Team-scoped store: no role customisation, no group, **one-way upgrade** | `A7` | `GOV-24` | stable | `VC-07` | — |
| Trial environments are not backed up; per-type operational consequences | `A7`, `A11` | `GOV-21`, `OP-14`, `OP-20` | volatile | `VS-07` | — |
| Guest access restricted by default, with a non-governed-store residual | `A7`, `A6` | `GOV-25`, `SEC-04` | stable | `VC-10` | `G-074` |
| The organisation-wide group includes guests and is not enumerable or editable | `A7`, `A6` | `GOV-05`, `SEC-38` | stable | — | — |
| Backup retention default, extension, and the production-managed condition | `A7`, `A11` | `GOV-21`, `OP-14` | volatile | `VS-07` | — |
| Residency fixed at creation; the boundary is a dual condition; identifiers replicate globally | `A3` | `DA-57`, `DA-58` | stable | — | — |
| Managed environments gate the control set; entitlement families; a developer-plan carve-out | `A7`, `A10`, `A3`, `A11` | `GOV-06`, `GOV-10`, `LC-23`, `DA-55`, `OP-21` | stable | `VC-05` | — |
| **Every active user of a managed environment needs an entitling licence, including standard-app users** | `A7` | `GOV-11` | stable shape / dated enforcement | `TW-V3` | `G-002` |
| The dated licence-enforcement milestone | `A7` | `GOV-11` | volatile | `TW-V3` | `G-080` |
| The dated pipeline-target auto-conversion milestone | `A8`, `A11` | `ALM-10`, `OP-16` | volatile | `TW-V1` | `G-087` |
| Auto-claim assigns on app launch; recommended with the managed class; pair with sharing limits | `A7` | `GOV-18` | stable | — | — |
| The licence-requirement report **under-reports** | `A7` | `GOV-11` | stable | — | — |
| The broad-enablement versus population-entitlement tension is genuine and its resolution is organisation-specific | `A7`, `A8` | `GOV-C2`, `ALM-C2` | stable | — | `G-080` |
| Environment groups: managed-only, one per environment, no nesting, **no exceptions**, rules lock settings read-only, join overrides existing values | `A7` | `GOV-07` | stable | — | `G-081` |
| Routing creates managed developer environments; manual creation is a separate setting; existing environments do not move | `A7` | `GOV-08` | stable | — | — |
| **No data policies by default**; environment cannot override tenant; most restrictive wins; no user scope | `A7` | `GOV-10` | stable | `VC-03` | — |
| Connector-aware, not connection-aware | `A6`, `A7` | `SEC-23`, `GOV-10` | stable | — | — |
| Policy count fragments the connector space **combinatorially** | `A7` | `GOV-10` | stable | — | — |
| A non-blockable set; the allowlist model excludes some mechanisms and never virtual connectors; endpoint filtering fails on dynamic values | `A7`, `A6`, `A3` | `GOV-11b`, `SEC-24`, `SEC-25`, `DA-63` | volatile posture | `VC-03`, `VC-10` | `G-075` |
| Policy retrofit suspends and quarantines, **with enforcement lag** | `A3`, `AP` | `DA-63`, `AP` §5.6 | stable shape | `VS-21` | `G-004` |
| Sharing limits forward-only; only-unsharing until compliant; a publish carve-out | `A7`, `A6` | `GOV-19`, `SEC-38` | stable | `VS-21` | — |
| External-site visibility is a tenant control; already-public stays public; dated certificate and key obligations | `A7` | `GOV-23` | stable | — | — |
| Solution-checker enforcement: modes, critical-only, cancels pre-import, unavailable in administration mode, and **not a test** | `A7`, `A8` | `GOV-20`, `ALM-16` | stable | — | — |
| **Platform governance does not govern the external estate**; a named-owner list | `A7` | `GOV-XB-01`, `GOV-XB-02` | stable | — | — |
| Ownership is not enforced; reassignment grants no permissions | `A7`, `A11` | `GOV-14`, `OP-04`, `OP-05` | stable | — | — |
| Inventory is **not** a service catalogue | `A7` | `GOV-16` | stable | — | `G-084` |
| Read-only production support via block-unmanaged plus co-ownership | `A7`, `A8` | `GOV-15`, `ALM-15` | stable | — | — |
| Retirement: quarantine, orphan and inactivity detection, a move-out procedure, and restore re-exposing cleaned artefacts | `A7` | `GOV-17` | stable | — | — |
| The community governance toolkit is **deprecated and its parity is not established** | `A7`, `A11` | `GOV-12`, `GOV-C1`, `OP-27` | stable / unknown parity | — | `G-079` |
| Sprawl figures are unsourced; the direction is corroborated by product behaviour | `A7` | `GOV-26` | signal only | — | — |
| **Organisational governance is not platform disqualification** — most findings are preconditions, obligations, economic consequences or operating requirements | `A7` | §1 framing, `GOV-XB-01` | stable | — | — |
| **Matched pairs must both be carried** — over- and under-governance are opposing failures of one lever | `A7`, `AP` | `GOV-C2`, `AP-D-039` vs `AP-D-036`/`AP-D-038` | stable | — | — |

---

## 11. `alm/release-and-lifecycle.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Four rungs: what each buys, requires and **does not give** | `A8` | §1 | stable | — | — |
| Rungs 2 and 3 are **not alternatives** | `A8` | `ALM-09` | stable | — | — |
| A single unmanaged layer above all managed layers; top-level-wins with three exceptions; one production edit shadows updates permanently | `A8` | `ALM-03`, `ALM-19` | stable | — | — |
| A managed solution cannot be imported where its unmanaged original lives — **the test environment is structural** | `A8` | `ALM-02`, `ALM-C3` | stable | — | — |
| Update and patch cannot delete components; upgrade deletes what is absent; patches not recommended | `A8` | `ALM-04` | stable | — | — |
| Solution membership gates backup coverage, capacity-licensed ownership, monitoring visibility and pipeline deployment | `A11` | `OP-15`, `OP-14` | stable | — | — |
| Restore asymmetry: solution automations deleted, non-solution retained; a non-solution owner **cannot be changed** | `A11`, `AP` | `OP-15`, `AP` §5.7 | stable | `VS-17` | — |
| Solutions carry no business data; some system tables excluded; units and teams per environment; owning-unit values must match | `A8`, `A6` | `ALM-07`, `ALM-19`, `SEC-10` | stable | — | — |
| Pipelines: artefact immutability across sequential stages, prevalidation, configuration handling, run history, approvals, layer diffs | `A8`, `A11` | `ALM-10`, `OP-16` | stable | — | — |
| Pipeline limits: no cross-tenant, no multi-solution, fixed import behaviour, no pre-export publish, a single development environment, one host, unsupported analytical types | `A8`, `A11` | `ALM-10`, `OP-16` | volatile | `VC-10` | `G-086` |
| Targets must be managed; the host need not be; development may be developer-plan | `A8`, `A11` | `ALM-10`, `ALM-25`, `OP-16` | stable | `VC-05` | `G-094` |
| The dated pipeline-target auto-conversion | `A8` | `ALM-10` | volatile | `TW-V1` | `G-087` |
| The managed-environment entitlement chain is **owned by the governance unit** | `A7`, `A10` | `GOV-06`, `GOV-11`, `LC-23` | stable | `TW-V3` | — |
| Delegated deployment: the delegate replaces the maker; administrator rights required in targets; approvals pending; sharing on first deployment only; no individual-user sharing; a stage-owner limitation | `A8` | `ALM-11` | stable | — | `G-091` |
| Deployed objects are owned by the **deploying identity**; automations run as the connection owner | `A8`, `A6` | `ALM-20`, `SEC-21` | stable | — | — |
| Source-controlled ALM lives in **developer environments**; source of truth, rehydration, fusion teams; a two-copies caveat; canvas caveats | `A8`, `A2` | `ALM-09`, `AA-05`, `AA-06` | stable / canvas maturity unknown | — | `G-088` |
| **No multi-developer isolation inside one environment** | `A8` | `ALM-23` | stable | — | — |
| Build tooling: identity options, multi-factor incompatibility of basic credentials, no mixing task versions | `A8` | `ALM-12` | stable | — | `G-095` |
| Three solution-organisation strategies; four hard rules; the silent dependency failure | `A8` | `ALM-06` | stable | — | — |
| Environment variables: definition and value split; values must not ship; no store-side validation; a managed value visible only via the default solution; reserved names; an identifier mismatch | `A8` | `ALM-13` | stable | `VS-26` | — |
| Connection references: an asymmetry between automation and app types; four failure modes; the workaround creates an unmanaged layer | `A8` | `ALM-14`, §14.1 | stable | — | — |
| Do not silently disable the integrity control to accommodate the workaround | `A8` | §14.1 | stable | — | — |
| Secrets are vault-held and consumable by three component types | `A6`, `A8` | `SEC-07`, `ALM-13` | stable | — | — |
| Block-unmanaged-customizations: a blocked set, an allowed set, a dataflow exemption, and a break-list | `A8` | `ALM-15` | volatile break-list | `VC-10` | `G-090` |
| **There is no rollback**; three imperfect paths; previous-version redeploy only if the setting was enabled | `A8` | `ALM-18`, `ALM-10` | stable | — | `G-005` |
| Restore constraints and post-restore side effects: automations deleted or off, references needing new connections, identifier changes, broad sharing lost, administration mode | `A8`, `A11` | `ALM-18`, `OP-14` | volatile windows | `VS-17`, `VS-07` | `G-013` |
| **Capacity headroom is a recoverability precondition** | `A11` | `OP-22`, `OP-14` | stable | `VC-07`, `VS-17` | — |
| Restore rewinds one participant — a post-restore integration step is required | `A8`, `A11` | §14.4, `OP-14`, `OP-18` | stable | — | — |
| Exit: managed solutions cannot be exported; uninstall destroys custom-table data; the publisher forecloses re-homing; no database backup copy; no cross-tenant pipeline; the repository is the portable asset | `A8`, `A3` | `ALM-02`, `ALM-05`, `ALM-10`, `ALM-18`, `DA-55` | stable | — | — |
| The checker is static analysis, does not know target state, and does not guarantee import | `A8` | `ALM-16` | stable | — | — |
| The low-code test engine is **deprecated**; browser automation is the stated path | `A8`, `A2` | `ALM-17`, `AA-08` | stable | — | `G-089` |
| Four validation levels for a business-critical release | `A8` | §14.3 (supported synthesis) | synthesis, marked | — | — |
| Release governance: what is in-product versus what must be built; traceability only at the top rung | `A8` | `ALM-21` | stable | — | — |
| Two coordinated supply chains; contract compatibility and sequencing; compensation artefacts are versioned contract | `A8` | §14.2, §14.5 | stable | — | — |
| Four **irreversible** week-one choices: publisher, table ownership type, first-party apps at creation, region | `A8`, `A6` | `ALM-05`, `ALM-24`, `SEC-09` | stable | — | — |
| Import into an older service-update station is **not reliable** | `A8` | `ALM-08` | stable | — | — |
| The accelerator tooling is deprecated and its comparison table is stale in at least one row | `A8` | `ALM-22`, `ALM-C1` | stable | — | — |
| **Reversibility mechanisms must be enabled before they are needed** | `A8` | `ALM-18`, `ALM-10` | stable | — | `G-005` |
| Solution size and environment-variable value length are packaging ceilings | `A8` | `ALM-07`, `ALM-13` | volatile | `VS-26` | — |
| Cross-boundary release is a **second supply chain** | `A8`, `A4` | §14.2, `AT2-53` | stable | — | — |

---

## 12. `performance/performance-and-scale.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| Classify the workload before sizing; six shapes, ordered first-yes test | `A9` | §1 (INF taxonomy over MS facts) | stable (synthesis) | — | — |
| Compute shape has no sizing dial; in-database extension time is charged to the triggering request's budget | `A9` | §1, `PF-45`, `PF-22` | stable | — | — |
| Public read funnels all traffic onto one identity; no app-side tuning changes it | `A9` | §1, `PF-25` | stable | `VC-04` | — |
| Sub-interval event frequency is a mechanism problem, not a tuning problem | `A9` | `PF-32` | volatile | `VS-14`, `VC-02` **(stamped)** | — |
| **Five independent meters; the binding one is the smallest, and normally not the daily figure** | `A9`, `A4`, `A3`, `AP` | §2, `AT2-02`, §4.10, `AP-D-049` | stable composition rule | `VC-04`, `VS-08` | — |
| Batching does not bypass entitlement; it trades the request meter for the execution-time meter | `A9` | §2, `PF-23` | stable | — | — |
| The protection figure is **per web server with an undisclosed, licence-dependent count** — which is why the triple is not carried | `A9` | `PF-22`, `PF-U-10` | stable mechanism | `VC-04` | `G-096` |
| Content throughput and inbound runtime-endpoint concurrency are the forgotten meters | `A9`, `A3` | `PF-31`, `DC-09`, `SC-08` | volatile | `VS-03` **(stamped)**, `VS-27` | — |
| Throughput class follows the owner's licence and reverts on departure | `A9`, `A10` | `PF-29`, `DC-18`, `LC-26` | stable | `VS-39` | — |
| The weakest system in the chain limits the result | `AP`, `A5` | `AP-D-049`, `IA-06` | stable | — | — |
| **The seven-way separation and the pairwise collapses** | `A9`, `AP`, `MF` | §0, §3, §11.2, §15.5, `AP-D-048`/`049`/`051`/`052`, `NB-03`, `NB-07` | stable (supported synthesis) | — | — |
| Platform service availability ≠ composite end-to-end SLA; recovery objectives are not uptime; weakest-dependency method per business flow | `A9`, `MF` | §15.5, `DC-13`, `PF-43`, `NB-03` | stable | — | `G-012` |
| Quota → commercial or distributional remedy; throttle → back-off plus per-connection rate; hard boundary → decomposition only | `A9` | §2, `PF-27`, `PF-28`, `PF-38` | stable | — | — |
| Throttle rate as a **trend** is an early warning; sustained breach ends in disablement; editing resets the evidence | `A9`, `A5`, `A3` | `PF-39`, `IA-45`, `SC-10` | volatile | `VS-09` **(stamped)** | — |
| Retries and pagination consume the same meters as real work | `A9`, `A10` | `PF-38`, `LC-09` | stable | — | — |
| Query shaping, not parallelism, is the first throughput lever | `A9` | `PF-28` | stable | — | — |
| **Limits exclude; they do not prove.** Exclusion is the one verdict limits carry alone | `A9`, `MF`, `AP` | §0, §3, §12, `NB-07`, `AP-D-048` | stable | — | `G-063` |
| The vendor's own high-volume method is adaptive back-off, not calculation — *each environment can be different* | `A9` | §0, `PF-23` | stable | — | — |
| A reachable limit plus a redesign trigger is the right unit for a dated claim | `A9`, `A3` | `PF-47`, `DC-20`, `SC-16` | stable | — | — |
| **No concurrent-user figure published for any surface** | `A9`, `A3` | `PF-09`, `SC-16` | stable absence | — | `G-027` |
| **No end-to-end latency figure published for any path** | `A9` | `PF-14` | stable absence | — | `G-063` |
| Write amplification is per-solution and unpublished — measured or `Unknown` | `A3` | `SC-01`, `SC-21` | stable | — | `G-028` |
| The security-model performance curve is `UNKNOWN` with a test obligation | `A9`, `MF` | `PF-U-07`, `NB-04` | `UNKNOWN` | — | `G-078` |
| Delegation: truncated wrong answers, not slow ones; two traps give no warning; test with the row window at its minimum | `A9`, `AP` | `PF-01`, `PF-02`, `DC-01`, `AP-D-050` | volatile | `VS-02` **(stamped)** | — |
| The aggregation ceiling is separate; analytical replication has its own refresh window | `A9`, `A3` | `PF-46`, `DA-03` | volatile | `VS-06` **(stamped)** | — |
| Definition size degrades authoring before runtime; a long-formula pathology; a serial startup path | `A9` | `PF-06`, `PF-07` | stable | `VS-24` | — |
| The only published large-implementation reference is a complexity figure, **not a scale guarantee** | `A9` | `PF-08` | stable | — | — |
| External-site cache floor non-reducible; server-derived values never guaranteed prompt and the pattern is *not recommended*; clearing the cache is a live-site incident | `A9`, `A3` | `PF-17`, `PF-18`, `PF-19`, `SC-14` | volatile | `VS-01` **(stamped)** | — |
| The external-site scale dial is purchased capacity, with **no published capacity-to-throughput relationship** and no published request or concurrency limits | `A9` | `PF-16`, `PF-21`, `PF-U-03` | stable absence | — | `G-018` |
| **No published size envelope for standard tables; no self-service indexing** | `A3` | `SC-18` | stable absence | — | `G-026`, `G-037` |
| Extension-code data operations are **exempt from protection** — a genuine architectural lever | `A9` | `PF-22` | stable | — | — |
| The list store returns all defined columns; dynamic lookups add server work; the vendor instructs partitioning above a stated threshold | `A9` | `PF-24`, `PF-AP-11` | volatile | `VS-04` **(stamped)** | — |
| Spreadsheet is not a relational store and **no transaction threshold is published** | `A9` | `PF-26` | stable | — | — |
| **Analytical traffic is not isolated** — endpoint reads run under protection limits | `A3`, `A9` | `SC-15`, `SC-20`, `PF-46` | stable | `VC-04` | — |
| The scheduling floor and per-connector polling intervals are the real freshness constraint | `A9` | `PF-32`, `PF-U-08` | volatile | `VS-14`, `VC-02` **(stamped)** | — |
| A long-running run and its history expire together; inactivity suspension for non-premium ownership | `A9` | `PF-37`, `PF-39`, `DC-08` | volatile | `VS-13` **(stamped)** | — |
| Serialising a trigger for ordering is **lossy and irreversible**; an ordered broker in front is the documented answer | `A9` | `PF-36`, `DC-10` | stable | `VS-24` | — |
| Payload ceilings are per mechanism, with a chunked variant, and cover the whole message | `A9` | `PF-35`, `DC-09` | volatile | `VS-10` **(stamped)** | — |
| In-region zone redundancy is automatic and quantified; single-region resilience needs no extra architecture | `A9` | `PF-40` | shape | `VS-37` | — |
| Cross-region is opt-in, managed-production-gated, a second full storage copy, **with no published recovery-time objective**, some geographies unpaired, and it degrades high-volume automation | `A9`, `A10` | `PF-41`, `PF-42`, `LC-24` | volatile | `VS-37` | — |
| Backup retention by environment class; trials not backed up; restore duration scales with audit data | `A9` | `PF-41`, §11.2 | volatile | `VS-07`, `VS-17` **(stamped)** | `G-013` |
| Deployment and administrative operations are intensive database operations; release cadence is a performance requirement | `A9` | `PF-44`, `DC-16` | stable (aged sources) | — | `G-099` |
| **The conflicted per-mechanism ceiling — 20×, decision-blocked, symmetric** | register, `A5`, `MF` | §3, `IA-C-01 (C-01)`, `NB-02` | **CONFLICTED** | `VC-01` / `VS-08`, `B-08`, `CD-05` | `G-058` |
| Measurement obligations: peak volumes, amplification as measured slots, an identity register, per-meter headroom, a tested baseline with realistic personas and volumes, funnel points | `A3` | §4.10, `SC-16`, `SC-17` | stable | — | — |
| **Volume-test at projected peak *frequency*, not at test-data volume** | `A5`, `A12` | `IA` §7 item 34, §11.2 | stable | — | — |
| Same environment class; managed, network and security-dependent behaviour needs matching fidelity; trial measurements do not transfer | `AP`, `A9` | `AP-D-052`, `PF-AP-17` | stable | — | — |
| A recovery objective needs a **timed drill**; a drill cannot perfectly replicate | `AP` | `AP-D-052` | stable | — | `G-013` |
| **The validation ladder is decision logic and lives outside this file** | contract | `decision-tree.md` §12 | — | — | — |
| Full-scale load testing against the shared service is constrained, and the surrounding guidance is unresolved against it | `A9` | `PF-15`, `PF-C-03`, `DC-17` | **CONFLICTED — preserved** | — | — |
| **No universal empirical benchmark exists; the absence is itself the finding** | `A9`, `MF` | `PF-U-01`, §12, `NB-07` | stable | — | `G-063` |
| Vendor target-writing example figures must never be encoded as platform characteristics | `A9` | §12 evidence note | stable | — | — |
| Marketing adjectives sit beside a limits page publishing no throughput figure | `A9` | `PF-C-02` | **CONFLICTED — preserved** | — | — |

---

## 13. `economics/licensing-and-cost-drivers.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| **No cost-optimisation discipline exists for this platform**; any discipline here is borrowed and translated — supported synthesis, not vendor guidance | `A10`, `AP` | §0.4, `LC-01`, `AP-D-060` | stable | — | — |
| Five economic mechanisms operate simultaneously, with a billing unit and a growth driver each | `A10` | §1, `LC-03`…`LC-24` | stable (INF taxonomy over MS-sourced facts) | — | — |
| **A design decision can move cost between mechanisms without reducing it** | `A10` | §1 | stable | — | — |
| Per-scope entitlement is a (person, app) pair, stackable, **scoped to one environment** — so app count and environment count are both drivers | `A10` | `LC-04`, `LC-25` | volatile | `VC-05` | — |
| Capacity entitlement buys throughput and autonomy, **never access**, and requires the automation to be in a solution | `A10` | `LC-08` | volatile | `VC-05` | — |
| Storage is **pooled at tenant level** — a conversation a project budget cannot resolve | `A10` | `LC-05` | stable | `VC-07` | — |
| Ordinal storage-rate and run-cost ordering **without figures** | `A10` | `LC-17` | volatile rates / stable ordering | `VC-07` | `G-103` |
| Child decomposition charged once or twice by shape; designer testing and resubmission not charged | `A10` | `LC-19` | volatile | `VC-06` | — |
| Population concepts: an active user opened at least once in the month; repeat access not counted; full per-user holders not counted | `A10` | `LC-17` | volatile | `VC-06` | — |
| Authenticated uniqueness is a contact record; anonymous uniqueness is a browser cookie; a monitoring probe bills as traffic | `A10` | `LC-12`, `LC-20` | volatile | `VC-06` | — |
| Site capacity does not carry forward; per-environment minimum assignments apply | `A10` | `LC-12` | volatile | `VC-06` | — |
| **No user entitlement accrues log capacity, yet auditing consumes it**; retention scope set at creation, not retroactive | `A10` | `LC-05`, `LC-11` | volatile | `VS-05`, `VC-07` **(stamped)** | `G-036` |
| The search index bills at the most expensive tier, and disabling search is **not** a remedy | `A10`, `AP` | `LC-11`, `AP-D-063` | stable mechanism | `VC-07`, `VS-31` | — |
| Cross-region protection consumes a **second full copy** of storage | `A10` | `LC-24` | volatile | `VS-37`, `VC-07` | — |
| Every environment consumes a storage floor; developer and trial classes are free of it | `A10` | `LC-10`, `LC-25` | volatile | `VC-07` | — |
| Cross-capacity borrowing is one-directional | `A10` | §7.2 item 12 | stable | `VC-07` | — |
| Entitlements do not roll over — the peak window is the window provisioned | `A10` | `LC-AP-07` | stable | — | — |
| The non-licensed request pool is shared tenant-wide with **no project view** | `A10`, `AP` | `LC-09`, `AP-D-063` | stable | — | `G-105` |
| Retries and pagination are billed as work; the vendor's throttling remedy is **commercial** | `A10` | `LC-09` | stable | — | — |
| **Exceeding pooled storage blocks administrative operations including restore** — capacity headroom is a recoverability requirement | `A10`, `AP` | `LC-10`, `AP-D-063` | stable | `VC-07`, `VS-17` | — |
| Consumption reporting is preview and partial with documented defects | `A10` | §7.1 items 8–10, `LC-19` | volatile | `VC-06` **(stamped)** | — |
| The managed class obliges entitlement for **every active user of the environment, including standard-app users** | `A10`, `A7` | `LC-23`, `GOV-11` | volatile | `TW-V3`, `VC-05` | `G-002` |
| Individual controls import higher-tier productivity, directory and compliance entitlements | `A10` | `LC-30`, §14.4 | volatile | `VC-05` | `G-077` |
| The chain to model: control → entitlement → population → holdings → gap. The unit is the **affected population**, not the app count | `A10`, `AP` | `LC-30`, `DC-14`, `AP-D-064` | stable | — | — |
| **Mandated control plus unfunded population = economic infeasibility, not a trade-off** — and it asserts nothing about other classes | `A10`, `AP` | `LC-30`, `AP-D-061`, `AP-D-064` | stable | — | — |
| The three dated tripwires and their firing actions | register, `A10` | `LC-15`, `LC-23`, §7.2 item 36 | dated | `TW-V1`, `TW-V2`, `TW-V3` | `G-006`, `G-080`, `G-087` |
| The demand-shape break-even is published and is about **shape, not price** | `A10` | `LC-18`, `DC-02` | volatile | `VC-06` | — |
| Prepaid and consumption coexist in one environment; periodic true-up is the vendor's own advice | `A10` | `LC-18` | volatile | `VC-06` | — |
| External participants: guest entitlement in the correct tenant versus site capacity per unique monthly visitor | `A10` | `LC-07`, `LC-12`, `DC-05` | volatile | `VC-05`, `VC-06` | — |
| **Growth at horizon and the peak is what is priced** | `A10` | `LC-13`, `LC-15`, `LC-AP-07` | volatile | `VC-06`, `VC-07` | — |
| Cost attribution is per environment, surfaced as a cloud resource — the only documented mechanism, and it **couples attribution to topology** | `A10` | `LC-16`, `DC-14` | volatile | `VC-06` | — |
| Enabling consumption billing **silently ignores prepaid assets** assigned to that environment | `A10`, `AP` | `LC-16`, `AP-D-063` | stable mechanism | — | — |
| The entitlement boundary can move the whole population from seeded to standalone; **multiplexing is prohibited with a documented suspension right** | `A10`, `AP` | `LC-03`, `LC-02`, `DC-01`, `AP-D-062` | volatile | `VC-05`, `VC-03` | — |
| Whether one premium capability obliges premium entitlement for every user of an artefact is an **open item** — verification, not assumption | `A10` | §7.3 item 50, `LC-U-05` | `UNKNOWN` preserved | `VC-05` | `G-002` |
| The **licence-avoidance trap** in four documented forms, with the workaround cost required alongside the saving | `A10`, `AP` | `LC-27`, `LC-AP-01`, `AP-D-061` | stable | — | — |
| Cheap automation ownership: lower profile, fewer retries, higher postpone floor, inactivity suspension, reversion on departure — **ownership is architectural** | `A10`, `AP`, `A9` | `LC-26`, `AP-D-066`, `PF-29` | volatile | `VS-03`, `VS-13`, `VS-39` | — |
| Avoiding the managed class forfeits telemetry export, extended backup, cross-region recovery, pipelines and network isolation — **the means of diagnosis and recovery** | `A10` | `LC-23`, `LC-AP-10` | stable | — | — |
| Sunk capability may make the incumbent the correct answer | `A10` | §6, `LC-28` | stable | — | — |
| Process change and do-nothing are legitimate priced options | `A10` | `LC-28`, `DC-15` | stable | — | — |
| Exit cost: a capped free tier, a ceiling that stops new solution creation, a one-way upgrade converting all users, and no export to a full environment — **the exit may be a rebuild** | `A10`, `AP` | `LC-14`, `LC-AP-09`, `AP-D-065` | volatile | `VC-05`, `VC-10`, `VC-07` | — |
| Deprecation-driven remediation is a recurring line; refactoring at structural limits is scheduled | `A10`, `AP` | `LC-29`, `DC-16`, `AP-D-065` | stable | `VC-10` | — |
| Counting hazards: people ≠ pairs; data volume ≠ audit volume; unique people ≠ billable visitors; documented over-count units | `A10` | §12, `LC-20`, `LC-19` | stable | `VC-06` | — |
| **General documentation is not authoritative on entitlement**; the guide and the agreement govern; example prices are illustrative | `A10` | §0.2, §0.3, `LC-02` | stable | — | — |
| Consumption above documented entitlement permits **suspension after reasonable notice** | `A10` | `LC-02` | stable | — | — |
| **No cost or entitlement claim is `Confirmed`** — all `Assumed` with validity and a named owner | `A10`, `AP` | §0.3, §12, `AP-D-055` | stable | `VC-10` | — |
| **The pack must never quote a price** — carry units, ratios, drivers and criteria | `A10` | §12 (explicit instruction) | stable | — | — |
| **No comparative total-cost-of-ownership exists**; the baseline withdrew its row-level comparator claims | `A10` | §6, §7.3 item 51, `LC-U-04` | stable | — | `G-102` |
| The users-to-work ratio is a hypothesis to test, not a verdict | `A10` | §6 | stable (`UNKNOWN` per engagement) | — | — |
| **Platform-side effort bands are barred from comparative economics** | `A10`, `AP`, contract | §6, `AP-D-060` | stable | — | — |

---

## 14. `operations/operability-and-support.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| The platform operates itself; the **solution** is not operated unless decided | `A11` | §0, `OP-01`, `OP-14` | stable | — | — |
| The four-question operational test | `A11` | §0 | stable | — | — |
| The productivity versus mission-critical contrast | `A11` | §1 | stable | — | — |
| **Four maturity classes with an architecture column** | `A11` | §1.1 (INF, marked as synthesis) | stable (synthesis) | — | — |
| A criticality change alters licence footprint, artefacts, topology and region | `A11` | §1.1 | volatile on entitlement | `VC-05`, `TW-V3` | — |
| Ownership is **runtime-significant**; the profile reverts on departure | `A11` | `OP-04` | stable | `VS-39` | — |
| Inactivity, error and throttling disablement countdowns; notifications to individuals | `A11` | `OP-04` | volatile | `VS-09` | — |
| Three distinct ownership roles; an unnamed application owner is **not** a documentation gap | `A11` | `OP-05` | stable | — | — |
| The deploying identity owns the deployed objects | `A11` | `OP-04` | stable | — | — |
| A support plan is required to raise a case; end users cannot | `A11` | `OP-24`, §6.4 | stable | `VS-36` | — |
| **No root-cause analyses**; requesting one downgrades severity | `A11` | `OP-24` | stable | `VS-36` | — |
| A bounded effort then closure on performance and non-reproducible cases | `A11` | `OP-24` | volatile | `VS-36` | — |
| No help with damaged data; preview outside the service commitment | `A11` | `OP-24` | stable | — | — |
| Diagnostic access requires consent | `A11` | `OP-25` | stable | — | — |
| The support role set: first line, internal analysis, partner escalation | `A11` | §4 (INF, marked) | stable (synthesis) | — | `G-106` |
| Service health is free and needs nothing enabled | `A11` | `OP-07` | stable | — | — |
| **Telemetry export is managed-class-only** | `A11` | `OP-08` | volatile | `VC-05`, `TW-V3` | — |
| **Telemetry export is explicitly not lossless** | `A11` | `OP-08` | stable | — | — |
| Telemetry export is unavailable in sovereign clouds | `A11` | §6.1 item 3 | stable | — | — |
| Audit records must be complete and **separate from diagnostics** | `A11` | `OP-03` | stable | `VS-19` | — |
| Run history is the transactional record with bounded retention | `A11` | `OP-09` | volatile | `VS-18` | `G-115` |
| The aggregated monitor: daily aggregation, short windows, a **single non-tail percentile**, a tenant-analytics prerequisite, **no primary-store coverage**, gated recommendations | `A11` | `OP-11` | volatile | `VS-18` | `G-109` |
| Unused resources are invisible to the monitor surfaces | `A11` | §6.1 item 10 | stable | — | — |
| The automation surface: solution-only, ownership not co-ownership, lag, retention, unnamed artefacts; some products have no maker surface | `A11` | `OP-12`, `OP-06` | volatile | `VS-18` | `G-110` |
| The compliance log is comprehensive and **explicitly not for real-time monitoring** | `A11` | `OP-10` | stable | `VS-05` | `G-004` |
| Roles see different, partially non-overlapping surfaces | `A11` | `OP-06` | stable | — | — |
| A correlation id across service boundaries is prescribed and **not automatic** | `A11` | `OP-03`, §13.1 | stable | — | — |
| Platform correlation tracing is experimental, one mechanism only | `A11` | §6.1 items 29–30 | volatile | `VC-10` | — |
| Black-box monitoring is needed for a service-level indicator; **no synthetic monitoring**; an uptime check can bill itself | `A11` | `OP-03`, `OP-07`, §9.2 | stable | — | — |
| Alerting must be constructed; ingestion and retention cost stated twice | `A11` | `OP-13` | stable | — | `G-107` |
| The human side named: on-call, incident management, emergency access, post-mortems | `A11` | `OP-01` | stable | — | — |
| Ordering: rate flows → failure-mode analysis → targets → health model → instrumentation | `A11` | `OP-02` | stable | — | — |
| Backups are continuous; **a manual backup is a timestamped label, not a copy**, and cannot be downloaded | `A11` | `OP-14`, `OP-C-02` | stable | `VS-17` | — |
| Retention is short by default and longer only for a production managed environment | `A11` | `OP-14` | volatile | `VS-07` **(stamped)** | — |
| Trial environments are **not backed up** | `A11` | §6.2 item 36 | stable | `VS-07` **(stamped)** | — |
| Restore cannot target production directly; same region; managed-to-managed; policies must match | `A11` | §6.2 items 37–40 | stable | `VS-17` | — |
| **Restore may exceed a day, and audit inclusion slows it** | `A11` | §6.2 items 43, 51 | volatile | `VS-17` | `G-013` |
| Coverage is limited to solution-held artefacts; mixed environments restore inconsistently | `A11` | `OP-15` | stable | — | — |
| The post-restore breakage list | `A11` | `OP-14`, §6.2 items 45–53 | stable | — | — |
| **A recovery objective requires a timed rehearsal; no measured figure exists** | `A11` | `OP-U-03`, §6.6 | stable (gap) | `VS-17` | `G-013` |
| Cross-region is opt-in, production-and-managed only, has **no published recovery-time objective**, doubles storage, and **degrades** high-volume, parallel and latency-sensitive automation | `A11` | `OP-18`, §6.3 items 56–60 | stable | `VS-37` | — |
| **No prescriptive drill plan; a drill cannot replicate a real outage** | `A11` | §6.3 items 58–59 | stable | — | — |
| Several geographies have no cross-region option; named failover exclusions; region-pinned endpoints must be validated; **no deployments while failed over** | `A11` | §6.3 items 61–69 | stable | `VS-37` | — |
| Commitments stop at the platform boundary; the weakest dependency governs; **do not multiply percentages** | `A11`, `MF` | `OP-19`, §13.2, `NB-03` | stable | — | `G-012` |
| Self-operated components convert a vendor-operated availability profile into an operated one | `A5` | §2.1 row 10 | stable | `VS-28` | — |
| Deployment is a **load event**; a release calendar resolves the conflict | `A11` | `OP-23`, §9.1 | aged | — | `G-099` |
| Pipelines: managed environments for every non-development stage; rollback only if enabled; one solution; a single development environment; no cross-tenant; connection references without a value | `A11`, `A8` | `OP-16`, `ALM-10` | volatile | `VC-05` | `G-086` |
| Connections and connection references are the fragile part of deployment **and recovery** | `A11` | `OP-17` | stable | — | — |
| **Test fidelity ceiling** — managed behaviour is only testable in a managed environment | `A11` | `OP-C-03` | unresolved tension, preserved | — | — |
| Team skills are an explicit architecture criterion — *or commit to training them before you choose* | `A1` | `PS-40` | stable | — | — |
| Hybrid is a second operating model requiring three named commitments | `A4` | `AT2-53` | stable | — | — |
| **No operator ⇒ unavailable because no operator exists** — a capability fact, never a comparative judgement | `A12`, `AP` | `Y-13`, §13, `AP-D-026` | stable | — | — |
| Handover from delivery partner to customer operations is **undocumented** | `A11` | `OP-U-07` | stable (gap) | — | `G-106` |
| Four evidence-retention classes; store audit consumes log capacity no licence provides; audit excluded from restore by default | `A11` | `OP-10`, `OP-14` | volatile | `VS-05`, `VS-19` | — |
| **Capacity overage blocks restore, copy, recover and create** | `A11` | `OP-22` | volatile | `VC-07`, `VS-17` | — |
| The community governance toolkit is unmaintained | `A11`, `A7` | `OP-27`, `GOV-12` | stable | — | `G-079` |
| Deprecation is continuous and dated; several items delete or silently break | `A11` | `OP-26` | volatile | `VC-10` | — |
| **No documented retirement process** — abandonment is silent disablement | `A11` | `OP-28` | stable | — | — |
| *Included as an entitlement* is not *free* | `A11` | `OP-C-01` | preserved conflict, resolved at scope | `TW-V3` | — |
| Sustained overload is silent then terminal; editing resets the throttling evidence | `A11`, `A9` | `OP-04`, `PF-39` | stable | `VS-09` | — |
| **Peak capacity cannot be load-test-proven** against the shared service | `A9` | `PF-15` | stable | — | — |
| The aged intensive-operations guidance is direction, not specification | `A11` | `OP-C-05` | preserved conflict | — | `G-099` |
| Programmatic capacity alerting beyond the periodic administrator email is `UNKNOWN` | `A11` | `OP` §6 | `UNKNOWN` | — | `G-104` |

---

## 15. `architecture/patterns.md`

| Rule | Source | Id | Stability | Row | Gap |
|---|---|---|---|---|---|
| A pattern is a **composition of mechanisms**, not a product or a reference architecture | `A12` | §2 | stable | — | — |
| The simplest composition is the default; every escalation names its requirement | `A12` | §2, `Q-01`, `Q-07` | stable | — | — |
| The variables that move a pattern boundary (twenty named) | `A12` | §3.1 | stable | per mechanism | — |
| The escalation ladder and its orthogonal/enclosing structure | `A12` | §3.2 (INF, marked) | stable (synthesis) | — | — |
| **De-escalation is legitimate and rarely done** | `A12` | §6.3 | stable | — | — |
| Direct: default status, prerequisites, contract fragility, a per-connection cap, licence-dependent retry depth, silent degradation into disablement, accretion | `A12` | `AP-01` | stable / volatile on entitlement | `VS-09`, `VS-27`, `VC-05` | — |
| Mediated: seven justifications; the only documented place to rate-limit platform-side callers; single point of failure and bottleneck; logic creep; tier lock-in; deployment coupling | `A12` | `AP-02` | stable | — | — |
| **Mediation metering unresolved — do not claim relief** | `A12` | `APR-C-03`, `APR-U-03`, `APR-U-04` | `UNKNOWN` preserved | — | `G-111` |
| Event-driven: the inverted-caller condition, no default ordering, at-least-once duplicates, payload ceilings, webhook scale equals the receiver's scale, self-triggering loops, presence-not-change trigger semantics, the dual-write hazard on synchronous emission, abandonment with no listener, the private-network collision, data-pipe misuse | `A12` | `AP-03` | stable | `VS-10` | — |
| The private-egress workaround is **inference** | `A12` | `APR-U-05` | `UNKNOWN` preserved | — | `G-113` |
| Queue: three vendor-stated benefits; the dead-letter queue as the only documented poison destination; at-least-once implies consumer idempotency; unbounded backlog; **overload displacement to a per-identity limit**; durability must be verified | `A12` | `AP-04` | stable | `VC-04` | `G-011` |
| **No operator ⇒ unavailable** | `A12` | `Y-13`, §13 | stable | — | — |
| Hybrid: five seams; in-platform versus out-of-platform variants; the in-transaction exemption from service protection; the managed-identity availability boundary; two operating models; portability asymmetry; seam migration; the casual-posture warning | `A12`, `A1`, `A4` | `AP-05`, `PS-07`…`PS-51`, `AT2-35`, `AT2-53` | stable | `VC-05` | `G-010` |
| Virtualization: the no-copy advantage, the full documented exclusion list, irreversibility, ignored attribute selection, false freshness, a runtime dependency, two documented rejections on row-level security | `A12` | `AP-06` | stable | — | — |
| **Write-through virtualization is conditional with weak production evidence and `UNKNOWN` performance** | `A12`, `MF` | `APR-C-02`, `APR-U-06`, `NB-05` | preserved | — | `G-112` |
| Replication: the three-component design; exclusion-list-as-justification; bulk-mechanism gaps; no service-principal ownership; per-deployment reconnection; throttling remedied by licensing; one-to-one scope; the schema-mutating bidirectional variant; replicate the fields, not the record | `A12` | `AP-07` | stable | — | — |
| **Dual-write sustained far-side failure is `UNKNOWN`** | `A12`, `MF` | `APR-U-11`, `NB-01` | preserved | — | `G-064` |
| Facade: composition versus mediation; the anti-corruption condition; the placement rule; transient-fault centralisation; surface reduction; per-consumer multiplication; a sharper single point of failure; **partial failure must be explicit**; correlation mandatory; permanence by accident; batch-beats-facade for one backend | `A12` | `AP-08` | stable | — | — |
| The facade naming is the baseline's own; structurally strong, platform-specific by inference | `A12` | `AP-08` scope note, `APR-U-01` | preserved | — | `G-116` |
| Background: the vendor's wait test; three parts with the **status resource** as the omitted one; checkpointing; UX cost; coordination problems; polling cost; status-resource lifecycle; low-code clients may not honour the contract; idempotency-key reasoning; cancellation; **asynchrony does not lift the in-transaction ceiling** | `A12` | `AP-09` | stable | `VS-12`, `VS-13`, `VS-23` | — |
| **No saga or compensating-transaction construct** | `A12` | §8 item 28 (INF absence) | *unsupported until verified* | — | `G-011` |
| **The enterprise boundary is supported synthesis (`INF`), not a vendor-endorsed pattern** | `A12`, `MF` | `AP-10` honesty note, `APR-U-08`, `NB-06` | preserved | — | `G-114` |
| Enterprise boundary: the dominant condition is an existing vendor-agnostic capability with a published contract; a self-hosted in-network gateway; six layered control points; leaver-risk removal; the boundary-on-paper risk; the assuming-one-cloud risk; managed-environment gating; the governance-only variant | `A12` | `AP-10` | stable / volatile on entitlement | `TW-V3`, `VC-05` | `G-117` |
| The documented compositions (seven named) | `A12` | §6.1 | stable | — | — |
| Escalation triggers per boundary | `A12` | §6.2 | stable | — | — |
| **Per-stream decisions; one composition per system pair is a smell** | `A12`, `A5` | `Y-14`, `IA` §2 | stable | — | — |
| **One retry site per hop chain** | `A12` | `Y-11` | stable | — | — |
| The fourteen selection failure modes | `A12` | `Y-01`…`Y-14` | stable (two marked medium) | — | — |
| The composed disqualifier set (five named) | `A12` | §13 | stable | — | — |
| **What each composition imports — governance, ALM, cost, monitoring, recovery, a named operator** | `A12` | §3, §4 per pattern | stable | — | — |
| **Imports accumulate and do not merge** | `A12` | §6 rule 4 | stable | — | — |
| **The conflicted per-mechanism ceiling — symmetric, neither figure encoded** | `A12`, register, `MF` | `APR-C-01`, `NB-02` | **CONFLICTED** | `VC-01` / `VS-08`, `B-08`, `CD-05` | `G-058` |
| **No empirical measurement anywhere in the corpus** | `A12`, `MF` | §1, `APR-U-02`, `NB-07` | stable | — | `G-063` |
| Vendor-side positioning: capability facts usable, scale adjectives not; the platform's own scale positioning is itself conflicted | `A12` | §8 item 23, `APR-C-01` | **CONFLICTED**, both adjectives dropped | — | — |
| **Reference architectures are examples, not prescriptions** | `A12` | `Y-01` | stable | — | — |
| **This file explains compositions; it never selects or renders one** | `A12`, contract | §2, §10; `architecture-templates/README.md` positioning | stable | — | — |
| Compositions are reachable only **after** an option class is established — they are never the option space | `A12`, Step 3 | §10; `alternatives-register.md`, `outcome-classes.md` | stable | — | — |
| No numeric platform limit is carried in this file at all — every envelope is delegated by name | `A12`, contract | §9 | stable | all named rows | — |
| Business-events throughput envelope **not published** | `A12`, `A5` | `AP-03`, `IA` §3 | `UNKNOWN` | — | `G-065` |
| Cost comparison of the mediated variants is undocumented | `A12` | `AP-02` | `UNKNOWN` | — | `G-120` |

---

## 16. Verification statement

- Every rule above was checked against the named canonical file during authoring; the per-unit tables were
  produced by the authoring pass and are transcribed here without alteration of substance.
- **No canonical research id from this annex appears in any runtime file.** Asserted mechanically by
  `.claude/tests/test_pp_domain_knowledge.py::TestRuntimeHygiene::test_no_canonical_research_ids_anywhere`.
- Every volatility row named in the *Row* column exists in
  `library/packs/pp/decision-model/volatility-register.md`. Asserted mechanically by the same suite.
- Rules marked **CONFLICTED** carry no figure on either side. Asserted mechanically.
- Rules whose canonical basis could not be established were **not authored**; they are in
  `step-4b-research-gaps.md` and are cross-referenced from the *Gap* column above.
