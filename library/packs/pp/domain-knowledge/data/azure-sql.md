# Azure SQL through the platform — connector envelope, identity, and what leaves platform governance

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *What is the connector envelope and identity model when the store sits outside the platform?*
- *What does putting the store here move out of platform governance?*
- *Does this existing schema pass the conformance gate at all, and on which paths?*
- *Is this store the answer for cheap long retention, or for high-ingest telemetry?* (the baseline says no
  to both — §8, §10)

This file states **what the relational store outside the platform supports through the connector, what
identity it can and cannot carry, where its throughput ceiling actually sits, and which
responsibilities move out of the platform's governance when the data lives here**. It does not decide
**which store wins** — that belongs to the decision model (`decision-tree.md` S4–S6).

**There is no architecture branch named for this store in the decision model, and there never was one.** A
previous reference file in this pack declared one; that was a defect, recorded as such. This file names no
branch, no stage order and no exit class.

---

## 1. What this is for · `decision-grade`

The engine is not the question. The engine is capable, well understood, and mostly irrelevant to the
Options decision. Four things are the question:

1. **The connector envelope** — what the platform can push through the connection, per connection, per
   unit of time (§3).
2. **The identity model** — whose credentials reach the database, because that determines whether *any*
   per-user authorization is enforceable at all (§4, §5).
3. **The conformance gate** — whether an existing schema can be written through the connector without
   being altered (§6).
4. **What leaves platform governance** — database lifecycle, network estate, availability profile (§11).
   This is the decision-critical half and the half most often omitted.

The vendor's own reference guidance for this platform states the trigger plainly: build a **new** app with
**new** storage and consider the governed relational store; where the data **already exists** in a
relational store and **cannot be moved**, or organisational policy requires it, run the app over that
store. Read both as **triggers**, not verdicts — and note the corollary: choosing this store without
naming its trigger is arguing against the vendor's own reference architecture.

## 2. When it becomes material · `decision-grade`

- An existing relational database **already holds** the data and cannot move, or policy requires that
  engine.
- Complex relational work is required — joins, views, stored procedures, engine control, deliberate
  indexing — that the governed store deliberately abstracts away.
- A **customer-controlled encryption key** is required and the tenant lacks the premium suite entitlement
  the governed store's key path demands (§10).
- The dataset is **beyond the governed store's practical reach**, or arbitrary-column sub-second filtering
  over very large tables is required (no custom indexing exists in the governed store).
- Region colocation with other cloud services is required.
- Conversely: it is **not** material for cheap long retention (§8) or for high-ingest telemetry (§7) — the
  baseline contradicts both.

## 3. The connector envelope · `decision-grade`

The engine's capacity does **not** translate into platform throughput. The connector is a separate,
narrower budget sitting in front of it.

- **Per connection, over a short window**, there is a call-rate ceiling on create/read/update/delete
  operations and a higher one on native query and stored-procedure calls, plus a **per-connection
  concurrency ceiling**. In the app client the rate ceiling is expressed **per user** instead.
- **Connection-level throttling is also time-based.** Long-running requests consume the connection's
  budget: a burst of slow calls on one connection produces rejections for every other call on that
  connection until they drain. The mechanism is *time spent*, not just calls made.
- **A single action has a low-hundreds-of-seconds timeout**, and the app client layers its own request
  timeout and retry count on top. Design to the **tightest** of the layered limits; the outer figures are
  not the effective one.
- **Implicitly shared connections share ONE budget.** This is the single most consequential sentence in
  this section. Where the connection is implicitly shared, the whole user population runs through one
  connection's concurrency and rate allowance — so the app's scaling behaviour is set by connection
  topology, not by user count or by the database tier.
- **The connector cannot bulk-load. At all.** It is row-at-a-time operations under the rate ceiling above,
  with the action timeout above. A nightly load is a **separate toolchain** outside the platform (§9).
- **Views are read-only** through the connector; **stored procedures are un-paged actions** with a static
  return schema, no client refresh primitive, and invocation tied to whenever the calling control
  refreshes.
- **Large field payloads** in the target table degrade actions and triggers and produce gateway-class
  timeouts; the vendor advises against holding large data in the fields the connector touches.
- **Managed-instance hostnames do not accept the simple authentication path.** The vendor states that
  simple database authentication is supported only for the plain server hostname shape; hostnames carrying
  additional subdomains — the managed-instance shape — are **not supported**. That forces the directory
  identity path, which excludes guest identities. Managed-identity authentication for this connector is
  available only in the sibling integration service, not in the platform's own.
- **A private-networked environment closes the action list.** Only a small closed set of the newer action
  versions works; anything outside it returns an authorization error, and the on-premises gateway is
  **excluded entirely** (§10). Choosing a managed instance for network or compatibility reasons therefore
  costs connector surface area **and** forces the identity design at store-choice time.

> The connector, not the engine, is normally the binding constraint for an interactive application. Sizing
> the database tier without sizing the connection topology answers the wrong question.

## 4. The identity model — why this is the structural difference · `decision-grade`

- **An implicit connection reuses the maker's database credentials for every user.** The vendor's words:
  each time the end user runs the app, they are using the credentials the author created the app with —
  and end users **can author new applications** on those connections.
- **Secure implicit connections are hygiene, not a security model.** The connector moves server-side and
  the proxy restricts query shapes to those the app uses. Column names are still not hidden; write
  permission implies the adjacent operation; and importing such a connection through a connection
  reference has a documented case where **the security is not set correctly in the target environment**.
- **Only the directory-integrated (explicit) connection carries a per-user identity to the database** — and
  even then, **guest identities are unsupported** on that path.
- **Legacy Windows authentication through the gateway "isn't secure"** in the vendor's own words: it does
  not rest on end-user authentication, and the connector holds access to all the data on that source.
  The gateway uses **the stored credential regardless of the user**.
- **A shareable service principal collapses everyone to one principal.** The vendor's own reference
  architecture offers it as a reasonable auth choice and warns in the same breath that **all users have the
  same database access rights**.
- **App-side filtering is not authorization.** The permissions granted through an app's interface **do not
  deny** the data-source permissions the user already holds, and client-side filtering cannot be relied on
  for security.

**Consequence for the decision.** Where the requirement is *per-user* row or column authorization, the
identity model — not the database's capability — is the gate. It forces one of: directory-integrated
authentication end to end, or a custom API / stored-procedure middle tier. **Both change the delivery model
and the licensing conversation**, and both are Options-time facts, not build-time details.

## 5. Row-level security through the connector · `decision-grade`

The engine's row-level security is real and it enforces **in the database tier**, on every access attempt
from any tier — filter predicates silently filter reads, block predicates explicitly reject violating
writes. What it needs is a **trustworthy identity**, and the two documented ways of supplying one split
exactly along the §4 line:

| Predicate basis | What it requires | Reachable from the platform? |
|---|---|---|
| The database principal's own name | A **real per-user database principal** | Only with directory-integrated connections. Behind a shared or implicit connection it **collapses to one principal and enforces nothing** |
| A session-context value set after connect | A **middle tier** that sets the value on **every** connection before querying | The connector owns the connection, and **no documented maker hook exists** to set session context before a query. Treated as not reachable — and explicitly still open (§12) |

Also load-bearing, and not obvious:

- **It is a filter, not a confidentiality guarantee against an adversarial querier.** Documented leak
  channels exist — statistics reporting runs on unfiltered data, change-data-capture can expose whole rows
  to a privileged role, and a crafted expression can infer a filtered value from a division error. The
  predicate also applies to database owners, who can alter or drop the policy (auditably).
- **It constrains the schema and does not fully travel.** Indexed views cannot be created over a table
  carrying a policy, history tables of a system-versioned table are not automatically covered, and on the
  vendor's own analytical platforms **only filter predicates are supported** — a design relying on
  write-blocking does not survive into the analytical copy.

## 6. Relational semantics and the schema-conformance gate · `decision-grade`

*"We already have the database"* is an advantage **only if the schema passes.** This gate is answerable at
Options time from a schema audit, and it is cheap to run.

| Condition | Consequence through the connector |
|---|---|
| **No primary key on the table** | The data is **read-only**. Item get, patch and delete require a key |
| Small-integer types as the primary key | **Not supported** as primary keys |
| **A server-side trigger on the table** | Connector **insert and update do not work**. Writes must go through a stored procedure instead |
| Automation must fire on a row change | The create trigger requires an **identity** column; the modify trigger requires a **row-version** column. Legacy schemas usually have neither |
| Unsupported column types present | Binary, image, row-version, hierarchy, variant, XML and spatial types are unsupported by the connector |
| Identifiers not conformant to the query-protocol standard | **Not supported**. This is a naming property of the existing schema, not something the app can work around |
| **Views** | Query-only. No writes |
| Large data held in a touched field | Degrades actions and triggers; produces gateway-class timeouts |

**Delegation is partial, and the gaps are specific.** Text range comparisons, blank tests, numeric search
and date extrema do not delegate; date predicates **fail through the on-premises gateway** entirely (an
integer date key is the documented workaround); fixed-length character types carry documented pitfalls. The
depth and the operation table are `data/query-and-delegation.md`'s authority, not this file's.
> Documented reading · read 2026-09-04 · re-verify: VS-02 (design time, per data source)

**Nothing in the low-code expression layer is transactional.** The vendor states it directly, with its own
example: a detail row created without its header row simply remains. Where a unit of work spans rows, the
mechanism is a **stored procedure with an explicit transaction** — which means the transactional core of
the solution is written in the database, by whoever owns the database (§11).

**Through the gateway the stored-procedure contract shrinks.** Output parameters are not returned, return
values are unavailable, only the first result set comes back, and dynamic schemas are unsupported. A legacy
procedure library usually has to be redesigned to a single typed result set before it can be called at all.

## 7. The tier and throughput boundary · `decision-grade`

- **Log rate is the real ceiling on sustained writes, and it does not scale with compute size.** Past a
  point, adding compute does **not** raise sustained write throughput: the published per-tier log-rate
  ceilings are flat across the upper compute range, and they differ only between the service tiers. This is
  the physical cap on both continuous ingest and nightly load, and it is the number to size against —
  **not** compute units and **not** storage.
- **Storage ceilings differ by tier**, and only the horizontally-scaling tier answers a dataset beyond a few
  terabytes; that tier also allocates storage on demand and is billed on actual allocation.
- **Concurrent sessions are generous; concurrent workers are not.** Session ceilings are the same across the
  range inspected, but worker counts scale with compute — and at the smallest service objectives the worker
  and external-connection counts are **small**. The connector's own per-connection concurrency ceiling sits
  **inside** that envelope, which is why §3's conclusion holds.
- **This store is not the answer for high-ingest telemetry.** The vendor's own data-store model guide maps
  *"high-ingest timestamped metrics and events"* — sensor metrics, application telemetry, monitoring,
  industrial and market data — to a **purpose-built time-series service**, and lists the relational store
  only under *consistent transactional operations*. The only relational escape hatch the vendor names is a
  different relational engine with a time-series extension, and only where the time-series data must be
  queried alongside existing transactional data. Low-volume event rows inside a business application —
  audit trails, status history — are ordinary relational rows and are fine here; genuinely telemetry-shaped
  workloads are a different store's question.

## 8. Retention, and why this is not the cheap archive · `decision-grade`

The claim *"keep N years of closed records cheaply, read-only"* fails here **as written**, on both halves.

- **Long-term retention is *backup* retention, not readable storage.** Retained backups are **restorable
  only as a new database** — they are not queryable. Reading a year-old record means restoring a whole
  database and paying its compute and storage. Retention answers *"can I recover the state of a past
  year?"*, never *"can users read that year's records?"*
  > Documented reading · read 2026-09-04 · re-verify: VS-07 (Options and renewal)
  > (long-term backup retention: configurable up to **10 years**)
- Granularity is coarse (weekly, monthly or yearly copies), **the vendor controls the timing** — no manual
  creation, and the first retained backup may take days to appear — and **policy changes apply only to
  future backups**. Restore is bound to the **same subscription**, and restoring across the
  horizontally-scaling tier boundary is not supported.
- **There is no cold or archive storage tier for rows.** Old rows cost the same per gigabyte as new ones in
  the same database. The vendor's documented answers to *"keep N years cheaply"* are: **time-partition**,
  apply **archival columnstore compression** to old partitions — explicitly trading query speed and
  processing for size, and only *"when you can afford extra time and CPU resources"* — or **move the
  partitions to a different, cheaper store**. The vendor's partitioning guidance says exactly that: cheap
  archive means a *different type of data store*.
- So: the store keeps N years **readable** perfectly well — they are just rows on the tier's storage rate —
  and keeps N years **recoverable** via backup retention. What it does **not** do is make old rows cheap.
  *"Cheaply"* is an **explicit archive design that must be scoped and estimated**, not a setting. Where
  cheap-and-read-only dominates and the records are genuinely closed, an object or lakehouse store is the
  vendor's own answer.
- The historical in-product cold-tier feature is understood to be **deprecated with no successor**, but the
  baseline could not close that with a quoted notice (§12). Do not rely on it either way.

## 9. Bulk load · `decision-grade`

- **The connector cannot bulk-load** (§3). This is not a tuning problem; the mechanism does not exist. A
  material nightly load implicitly **buys a second toolchain** — a data-integration pipeline, a bulk copy
  utility, or a staged copy — living outside the platform, with its own identity, scheduling, monitoring
  and failure handling.
- **No throughput guarantee is published.** What the vendor publishes is a **method**: estimate against the
  minimum of source, sink and network, then *"use the numbers obtained in your performance tuning tests"*.
  Any asserted rows-per-second figure for this store is invented. The sink-side binding constraint remains
  the log rate (§7).
- **The fast path has preconditions that are not free.** Minimally-logged import requires table locking, a
  target not under replication, no memory-optimised table, and — for index pages to be minimally logged
  too — an **empty** target carrying the clustered index; from the second batch onward only data pages
  benefit. Replication being enabled makes the import fully logged regardless. Compression on the target
  converts rows on import at additional processing cost. In practice that is a **staging-plus-switch
  design**, not *"insert into the live table overnight"*.
- **Whether the managed database service supports the recovery models that minimal logging depends on at
  all is `UNKNOWN`** in the baseline (§12). Do not assert that the fast path exists here; size against log
  rate and prove it with a measured pilot load.
- Where the nightly volume is material, make a **measured pilot** a gate before committing to this store,
  and put the measured number — not a guess — in the estimate.

## 10. Customer-managed key, and the private-networking path · `decision-grade`

**Customer-managed key — supported, scopeable, and not free.**

- Transparent encryption with a customer-managed key is a **first-class capability**, giving the customer
  key creation, rotation, deletion, permissioning and audit, with a documented **revoke-to-deny** path that
  makes the database inaccessible on demand — the compliance selling point.
- **Scope is server or instance level, inherited by the databases on it**, and a per-database option exists
  for the managed database service. Contrast the governed platform store, whose key policy applies to the
  **whole environment** through an enterprise policy.
- **There is no licence gate here beyond the cloud subscription itself.** The governed store's equivalent
  requires **managed environments** *and* a premium compliance suite entitlement **for the users in the
  environment**. That asymmetry is a genuine, quotable store-choice differentiator: in a tenant without that
  entitlement, a hard customer-key requirement is a real argument for putting the regulated data here —
  while accepting this store's premium connector class and per-user-identity costs.
- **Switching on is cheap here and expensive there.** Moving to a customer-managed key requires only
  re-encryption of the data key — fast, online, no downtime. The governed store **disables the environment**
  during encryption, for a duration dependent on database size and documented as taking up to several days.
- **The key vault becomes a tier-0 availability dependency, with a documented failure mode.** Continuous
  access to the key is required for the database to stay online. Lose access and the database starts
  denying all connections within minutes and moves to an **inaccessible** state; restore access quickly and
  it heals itself within the hour; restore access past the documented short window and **automatic healing
  is no longer possible**. When it does come back, **previously configured server- and database-level
  settings are lost** — failover-group configuration, tags, pool configuration, read scale, auto-pause,
  point-in-time restore history and the retention policy among them.
- Preconditions: the vault needs **soft-delete and purge protection** (setup fails otherwise), and a
  firewalled vault needs trusted-service bypass or private endpoints. Permission changes take minutes to
  take effect. **Old backups are not re-keyed** — every historical key version must be retained, because a
  restore needs the key its backup was created with. There is a documented ceiling on how many databases
  should share one vault.
- Net: the key decision drags in a **key-operations run-book** — access monitoring with alerting inside the
  healing window, key rotation treated as a backup-compatibility event, and a dedicated vault for the
  estate — not a checkbox.

**Private networking, and its mutual exclusion with the gateway.**

- The private path requires the platform's own network integration: a cloud subscription **associated with
  the tenant**, subnets **delegated in both paired regions**, an IP allocation per production environment,
  and only the newer action versions on this connector. **The on-premises gateway is not supported** in
  that mode — the two paths are mutually exclusive — and calls to publicly reachable resources **start to
  break** once it is enabled. These preconditions are **irreversible** in practice.
  > Documented reading · read 2026-09-04 · re-verify: VS-11 (design time, before any network commitment —
  > the preconditions are irreversible)
  > (address allocation: **25–30** addresses per production environment; gateway clusters: **at least 2**
  > nodes per cluster, with separate development and production clusters)
- **Without the private path**, the database must allowlist the platform's regional service tags, and that
  allowlist has to be **refreshed on a recurring cycle** — a standing operational obligation, not a
  one-time firewall change.
- **Through the gateway, payloads are capped** and results **transit the cloud** and spool on the gateway
  host. *"No transit of row data through the vendor's cloud"* is **not achievable** with this platform,
  however the store is hosted.
  > Documented reading · read 2026-09-04 · re-verify: VS-10 (design time, per stream)
  > (gateway payload ceilings: **2 MB** request, **8 MB** response)
- **Auto-pausing serverless compute produces predictable transient failures.** The vendor calls retry logic
  *especially important* there, because auto-resume errors are expected. A low-usage cost optimisation is
  therefore an explicit reliability decision: disable pausing, lengthen the delay, or keep the database
  warm.

## 11. What leaves platform governance · `decision-grade`

This is the section that changes decisions, and the one a store comparison usually omits. Putting the store
outside the platform moves three things out of the platform's governance — permanently, and to owners who
may not be in the room.

**1. Database lifecycle leaves the platform's lifecycle.** Solutions carry the platform's schema; they do
not carry this store's. Database change becomes **database DevOps outside the platform's release
mechanism**, with its own source control, its own migration tooling, its own environment promotion and its
own approval path — and it must stay **synchronised** with the platform's releases, because the app and the
schema deploy on two independent tracks. Since the transactional core lives in stored procedures (§6), the
solution's business logic is split across two lifecycles by construction.

**2. The gateway estate becomes an operating model, not a component.** Where the store stays on-premises,
the vendor's own guidance for a business-critical path is: **separate development and production clusters**,
a **node minimum per cluster**, high availability with load balancing (random distribution is opt-in;
primary-first is the default, so a cluster is not a load-sharing pool unless configured), scale-out driven
by processor-utilisation and concurrent-query signals, and a **monthly release cadence** with only a bounded
window of versions supported. Two statements are decision-critical: **recovery-key custody is described by
the vendor as a significant business risk** — without the key, gateways cannot be recovered — and **the
vendor does not investigate poor performance when a gateway is overloaded**. That is servers, a patch
pipeline, monitoring, key custody and an owner — all of which must appear in the option's cost, and none of
which the platform administers. Gateway-at-scale cost is an **open item** in the baseline (`VC-08`).

**3. The availability profile becomes customer-operated.** Tier selection, log-rate headroom, auto-pause
behaviour, backup and restore, the key-vault dependency and its healing window, index and statistics
maintenance, and the recovery objective itself are all **the customer's** to operate. In the governed store
these are platform properties; here they are run-book items with an owning role and a recovery procedure. And **the analytical copy
path is customer-built too**: there is no first-party managed replication from the governed store into a
writable relational database, so any writable copy in this direction is a **customer-built and
customer-operated** pipeline with its own watermark, delete detection and reconciliation job — see
`data/store-boundaries.md`.

**Two control planes, and one that does not cover the data.** Governance now spans the platform's
administration surface **and** the cloud platform's policy surface, and the vendor says to plan for
governance across both. Note what the platform's own data-loss-prevention layer does and does not do: it
governs **which connectors an app may use** — which systems it may talk to — **not the data**, with
enforcement latency measured in hours and suspension of violating artefacts as the consequence. It is not a
substitute for authorization in the database.

## 12. Failure modes · `decision-grade`

> **Implicitly shared connections treated as a security model.** Every user runs as the maker, and users can
> author new applications on the connection. Row-level security keyed to the database principal enforces
> nothing behind it, because there is only one principal.

> **Row-level security keyed to a session value with no middle tier to set it.** The connector owns the
> connection and no maker hook is documented. The policy exists, the predicate never sees the right value,
> and the filter silently passes or blocks the wrong rows.

> **Reusing a legacy schema unaudited.** Triggers break connector writes, missing keys make tables
> read-only, unsupported types and non-conformant identifiers are invisible until the connection is made.
> Discovered after commitment, this converts the option's estimate rather than the design.

> **Per-row loops against the store from automation, or a long-running procedure on the interactive path.**
> The per-connection rate ceiling and the action timeout are hit long before the engine notices load. The
> remedy is set-based procedures and asynchronous handling — a design property, decided early.

> **A single gateway node on a business-critical path.** A single point of failure, primary-first routing
> that does not share load, and a vendor that does not investigate performance on an overloaded gateway.

> **Long-term retention treated as a cheap queryable archive.** It is backup retention, restorable only as a
> new database. The requirement it was chosen for — users reading old records — is never met, and the
> discovery comes at the first retrieval request.

> **This store chosen for telemetry "because it's SQL and we know SQL".** The vendor's own model guide
> routes that workload elsewhere, and sustained write is capped by log rate regardless of compute size.

> **Key rotation without retaining historical key versions.** Old backups are not re-keyed; a restore needs
> the key its backup was created with. The gap appears only during a restore, which is the worst moment to
> find it. The same class of surprise applies to auto-pausing compute left on with no retry logic —
> auto-resume connection errors are documented as predictable, so they are configured behaviour, not bad
> luck.

## 13. Consequences elsewhere · `decision-grade`

- **→ `data/store-boundaries.md`** — the cross-store capability map, the *view-or-data* question, and the
  absence of a first-party managed replication path into a writable relational store.
- **→ `data/query-and-delegation.md`** — the delegable operation set for this connector, the client paging
  cliff, and the gateway's date-predicate failure. **Never restated here.**
- **→ `security/security-controls.md`** — the identity model (§4), row-level security's identity
  prerequisite and its documented leak channels (§5), the customer-key capability and its tier-0 vault
  dependency (§10), and the fact that app-side filtering is not authorization.
- **→ `governance/governance-and-environments.md`** — two control planes, connector-level data-loss
  prevention governing *systems* rather than data, and private-network integration as an environment-level,
  irreversible commitment that also dictates environment topology.
- **→ `operations/operability-and-support.md`** — the gateway estate as an operating model, the
  key-operations run-book, backup and restore reality, index and statistics maintenance, the retry posture
  for auto-resume, and the recovery objective becoming customer-owned.
- **→ `integration/integration-mechanisms.md`** — the connector envelope as an integration budget, payload
  ceilings by mechanism, the bulk-load toolchain outside the platform, and the trigger prerequisites
  (identity and row-version columns) that decide whether change can be detected at all.
- **→ `economics/licensing-and-cost-drivers.md`** — the premium connector class applies to this store and the
  governed one alike, so entitlement constrains **all** users rather than discriminating between the two;
  the real comparison is platform capacity against tier + gateway estate + operations, with gateway-at-scale
  cost an open item. Unit, meter, driver and entitlement shape live there — never a price.
- **→ `alm/release-and-lifecycle.md`** — database DevOps outside the platform's release mechanism, and two
  deployment tracks that must stay synchronised (§11).
- **→ `performance/performance-and-scale.md`** — log rate as the sustained-write ceiling, worker counts
  scaling with compute, and the connector sitting inside the engine's envelope.
- **→ `craft/sql-delivery-conventions.md`** — **all** schema-modelling conventions, layering, audit-column
  standards, procedure wrappers and execution ordering, view conventions, expression/upsert/history
  patterns, index strategy and maintenance, and identifier-collision handling. That file is **delivery
  practice**, is never an Options pull target, and may never state a platform limit.

## 14. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| External relational store tier envelope — the sustained log-rate ceiling and its independence from compute size, per-tier storage ceilings, concurrent sessions and workers | `VS-34` |
| Customer-managed-key operational windows, and the per-vault association ceilings | `VS-35` |
| Payload ceilings by mechanism (gateway request and response) | `VS-10` |
| Gateway host minimum and network preconditions — **irreversible** | `VS-11` |
| Backup and long-term retention windows | `VS-07` (recovery objective: `VS-17`) |
| Delegation ceilings for this connector | `VS-02` |
| Request rate per acting identity (transition-period tolerances, no announced enforcement date) | `VC-04` |
| Whether this connector remains permissible under the target environment's policy | `VC-03` |
| External and hybrid service consumption cost — **gateway-at-scale cost is an open item** | `VC-08` |
| Capacity consumption profile of any analytical copy | `VC-07` |
| Preview and general-availability states of anything relied on | `VC-10` |

**One live conflict, and it is symmetric.** Where a design **fronts this store with a custom connector or an
API layer** — a common answer to §4's identity problem and §6's conformance failures — the **throughput
ceiling of that mechanism is `CONFLICTED`**: two maintained vendor pages disagree by an order of magnitude,
the conflict was re-verified and remains open. Any option whose **sizing or economics** rests on it is
**decision-blocked until measured** (`VC-01` / `VS-08`, blocking entry `B-08`, composed row `CD-05`).
**Encode neither figure.** This cuts across the platform, the cloud-native classes and the hybrid class
**equally** — it is not a penalty against this platform. A documented case-by-case escalation path exists
and may be *proposed as a mitigation*; it may never be *relied on in advance*.

**Not established in the baseline — do not fill from general knowledge:**

- **Connector concurrency, isolation and locking semantics** — the transaction scope of a connector update,
  deadlock behaviour, retry semantics. Correctness under concurrent edits on this store is **`UNKNOWN`**.
  Do not assert either way; test, and check the row version in the procedure.
- **Gateway node throughput** — requests per second for platform traffic. No published figure. Load-test it.
- **Whether the platform's private-network integration requires managed environments.** Not stated on the
  source page; it materially changes the licensing of private connectivity.
- **Whether the managed database service supports the recovery models minimal logging depends on**, or is
  always fully logged (§9).
- **Whether a maker can set a session-context value on the connector's connection** before a query, which is
  what decides whether session-based row-level security is reachable at all without directory-integrated
  authentication or a middle tier (§5).
- **Whether the historical cold-tier feature is formally deprecated with no successor** (§8).
- **Any bulk-load throughput number.** None is published, by any mechanism (§9).
- **Read-access limits on retained backups**, and whether reporting can run against retained data at all.

## 15. What not to infer · `decision-grade`

- **A capability absence is not a verdict.** *"The connector cannot bulk-load"* and *"session-based
  row-level security is not reachable"* are domain knowledge. *"Therefore unsuitable"* is a selection
  verdict and belongs to `decision-tree.md`.
- **There is no architecture branch named for this store, and there never was.** A prior reference file in
  this pack declared one the decision model did not have; that defect is recorded, not inherited. This file
  names no branch, no stage order and no exit class.
- **A documented boundary here is not evidence that another option class performs better.** The baseline
  holds no like-for-like evaluation of hosted software, custom builds, incumbent platforms or other low-code
  stacks against this store. Where that comparison is material, the comparator semantics in
  `decision-model/outcome-classes.md` stand.
- **Do not read the vendor's reference default as evidence of superiority.** *"New app and new storage →
  the governed store"* and *"the data cannot be moved → the app over this store"* are **triggers**. They
  rank nothing.
- **Do not infer engine capability as platform capability.** Everything in §3, §4 and §6 is a property of
  the connector and the identity path, not of the database. A capable engine behind a narrow envelope is
  still a narrow envelope.
- **Do not treat this store as the cheap archive** (§8) **or as the telemetry store** (§7). Both were
  asserted in an earlier reference and both are contradicted by the baseline.
- **Do not carry any price.** Tier, meter, entitlement shape and growth mechanism belong to
  `economics/licensing-and-cost-drivers.md`; money belongs in neither file.
- **Delivery conventions are not platform knowledge.** Layering, audit-column standards, procedure
  templates, execution ordering, view naming, upsert and history patterns, index strategy and maintenance,
  and reserved-identifier handling live in `craft/sql-delivery-conventions.md` and are not consulted in
  Options.
