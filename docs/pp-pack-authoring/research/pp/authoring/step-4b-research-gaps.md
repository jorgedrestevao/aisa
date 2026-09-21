# Step 4B — research-gap annex (durable)

<!--
provenance: AUTHORING ANNEX
date: 2026-09-04 (created in the Step 4B pre-4C bounded repair)
source: the per-unit research-gap tables produced while authoring the 15 RESEARCH units, plus the
        canonical non-blocking reservations. Nothing here is regenerated from model knowledge.
scope: AUTHORING-SIDE ONLY. This is NOT a runtime gap registry and is never loaded at runtime.
-->

## 0. What this annex is

Every research gap found while authoring the domain-knowledge layer, persisted so it survives the
authoring session. A gap is recorded here when a statement a unit *wanted* to make could not be traced to
the canonical baseline. **None was filled from model knowledge; none was authored as fact.**

**Classification vocabulary**

| Class | Meaning |
|---|---|
| `commission` | Research-commission candidate — material, recurring, and not closed by engagement measurement |
| `empirical-test` | Closed by one bounded test in a target environment, not by reading documentation |
| `measurement` | Closed only by measuring the engagement's own workload; no published figure would settle it |
| `outside-corpus` | Intentionally unsupported — outside the baseline's scope, and not to be filled by inference |
| `pilot` | Feedback item for the first real engagement |

**Blocking** = can this gap, left open, make a decision undecidable? (`decision-tree.md` §4 semantics: an
open decision-critical unknown produces *decision blocked*, never a settled exclusion.)

---

## 1. Count correction — read this before using the number

The Step 4B report stated **63** research gaps. **That figure was an estimate made while consolidating
the per-unit returns, and it is wrong.** Enumerated and de-duplicated here, the true count is **120**.

The instruction for this repair was to persist *all* gaps rather than only the fourteen headline
candidates; that has been done, and the count is corrected in the same spirit as the *"7 → 11"* correction
in §13 of the repair brief. Twelve raw rows were the *same* gap surfacing in a second unit; each is
recorded once as a primary entry and cross-referenced from the other unit's table with a `b`/`c` suffix.
The remaining difference between 63 and 120 is simply that the report under-counted.

```text
primary gap entries (G-001 … G-120, contiguous)   120
cross-reference-only rows (suffixed b / c)          12
raw per-unit rows                                  132
distinct gaps persisted                            120
```

`RESEARCH GAPS PERSISTED: 120`  ·  `REPORT FIGURE CORRECTED: 63 → 120`

---

## 2. The fourteen commission candidates

Recorded as **candidates only** — no research was commissioned in this repair. Commission later only where
**material + recurring/general + not adequately closed by engagement measurement**.

| Id | Gap | Units | Class | Blocking |
|---|---|---|---|:--:|
| `G-001` | Whether table-scoped business rules actually fire on Web API / integration writes. The vendor's own documentation **contradicts itself**; carried as `Assumed`, never `Confirmed` | dataverse, store-boundaries | `empirical-test` | yes |
| `G-002` | Whether **one** premium capability obliges premium entitlement for **every** user of an artefact | economics, governance, security | `commission` | yes |
| `G-003` | Verbatim per-operation delegation table per connector. Class-level boundaries answer the architecture question; a named screen filter needs the operation level | query-and-delegation | `commission` | no |
| `G-004` | Control enforcement and propagation latency — decision-material in three separate places | security, governance | `commission` | no |
| `G-005` | Whether the previous-version-redeployment mechanism is on by default, and its retention limits. **The** reversibility mechanism most often assumed rather than enabled | alm | `commission` | yes |
| `G-006` | Per-operation AI / agent consumption — complexity-dependent and unpublished | economics, automation | `measurement` | yes |
| `G-007` | Gateway throughput for platform traffic, and gateway cost at scale | integration, azure-sql, economics, operations | `commission` | yes |
| `G-008` | Quota envelopes for two of the three broker services. Selection evidence exists; sizing evidence does not | integration, automation, architecture | `commission` | no |
| `G-009` | Entitlement treatment of five newer application surfaces (code-first site model, code apps, app-scoped custom pages, branded wrapping, list-customised forms) | application, economics | `commission` | no |
| `G-010` | Whether managed identity extends beyond in-database plug-ins | security, integration | `commission` | yes |
| `G-011` | Whether any in-platform dead-letter, circuit-breaker, saga or compensating-transaction construct is documented. Currently an **absence inference** — *unsupported until verified* | integration, architecture, automation | `commission` | no |
| `G-012` | Composite availability for a business flow across platform services. Needs contractual and product-terms parsing, not search | operations, performance | `commission` | yes |
| `G-013` | Measured restore duration at representative data volume | operations | `measurement` | yes |
| `G-014` | Multi-tenancy and resale licensing — an unclosed gap, already a scope-blocker | economics | `commission` | yes |

**Agent / conversational capability** remains a candidate for a **dedicated** future commission — see
`G-118`, `G-119`.

---

## 3. All gaps, by unit

### 3.1 `application/application-surfaces.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-009` | Entitlement treatment of five newer surfaces *(commission candidate)* | C3, C11 | `commission` | no | Surfaces stated; cost cells left open |
| `G-015` | Right-to-left support in standalone canvas apps | C3 | `commission` | where RTL is mandated | Stated as `UNKNOWN`; the earlier non-support claim withdrawn |
| `G-016` | Code apps: offline behaviour and mobile-player reach | C3 | `commission` | no | Offline treated as unsupported until verified |
| `G-017` | Frontline / shared-device / kiosk identity mode and its licensing | C3, C6, C11 | `commission` | for frontline programmes | Carried as an `UNKNOWN` identity row |
| `G-018` | External-site throughput, request rate, concurrency and grid performance at volume | C9 | `measurement` | for public-scale sites | Measurement obligation stated; no ceiling published |
| `G-019` | Push-notification throttling limits | C3, C2 | `commission` | at volume | Omitted; the unsatisfiable `{branded app, push}` pair is carried |
| `G-020` | Preview / general-availability banner state of the code-first site model and code apps | C3 | `pilot` | on a critical path | Marked unverified, `VC-10` named |
| `G-021` | Per-surface accessibility conformance reports | C3, C7 | `commission` | under a legal mandate | Absence stated |
| `G-022` | Any vendor decision guidance on the site-versus-custom boundary | C3, C12 | `outside-corpus` | no | Marked absent; the synthesis is flagged as synthesis |
| `G-023` | Component-library reuse inside the team-hosted surface | C3, C8 | `outside-corpus` | no | Omitted |
| `G-024` | Date of the mandatory interface refresh on the record-centric surface | C8, C12 | `pilot` | no | Carried as *a dated change*, verification under `VC-10` |
| `G-025` | Offline record-set ceiling — the figure was not captured verbatim, so it could not be restored | C3 | `commission` | no | Boundary shape only; owner now `VS-38` |

### 3.2 `data/store-boundaries.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-026` | Any published row-count or size envelope for a **standard** table | C4, C9 | `measurement` | no | Stated as a negative finding; load/soak test at projected volume |
| `G-027` | Any concurrent-user ceiling for any surface | C9 | `measurement` | no | Negative finding; funnel points named as the real constraint |
| `G-028` | Any write-amplification multiplier | C4, C9, C11 | `measurement` | no | Negative finding; measured per engagement, never carried over |
| `G-029` | Cost and duration of a full replica resynchronisation at realistic volume | C4, C11 | `measurement` | no | Named as a budgeted routine operation with unknown cost |
| `G-030` | Magnitude of the database increase caused by an analytical link | C4, C11 | `commission` | no | No published ratio; `VC-07` named |
| `G-031` | **Tenant default database capacity — internally inconsistent in the source** | C11 | `empirical-test` | no | Carried as conflicted; confirm in the administration centre |
| `G-032` | Whether the mirroring source list ever adds the governed store | C4 | `pilot` | no | Point-in-time negative; re-check per engagement |
| `G-033` | Whether the vendor states anywhere *"do not migrate historical data"* | C4 | `outside-corpus` | no | Carried explicitly as **pack opinion, not vendor guidance** |

### 3.3 `data/dataverse.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-001` | Cross-client server-side rule execution *(commission candidate — the highest-value single test in the baseline)* | C4, C6 | `empirical-test` | yes | `Assumed`, with the named test |
| `G-034` | Cross-session / cross-client read-after-write guarantee for standard tables | C4, C2 | `commission` | no | Stated as not assertable in either direction |
| `G-035` | Whether any read replica or geo-replication could serve a stale read | C4, C9 | `commission` | no | Same — do not assert either way |
| `G-036` | Request cost of auditing per audited write | C6, C9, C11 | `measurement` | no | Named as measured on a prototype with auditing on versus off |
| `G-037` | Whether vendor support creates custom indexes on standard tables on request | C4, C9 | `commission` | no | Levers stated as schema and query shape; support path undocumented |
| `G-038` | Whether private networking itself requires the managed environment class | C5, C6, C7, C11 | `commission` | no | Stated via the managed-class feature list |
| `G-039` | Long-term-retention **read** limits — query volume, and analytics over retained data | C4, C11 | `commission` | no | *"Queryable only through specific surfaces"* |
| `G-040` | Per-table column count and row-byte ceiling; maximum tables per environment | C4 | `commission` | no | Omitted entirely rather than guessed; `VS-30` now owns the family |
| `G-041` | Whether the elastic table type supports alternate keys | C4, C5 | `empirical-test` | no | Carried as contradicted; `VS-32` owns the re-verification |

### 3.4 `data/sharepoint.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-042` | Indexed-column maximum for the online list service (only on-premises figures are sourced) | C4 | `commission` | no | The *"every path indexed and selective"* test stands without it |
| `G-043` | Whether the app connector sends a concurrency token on item update; whether any multi-item transaction exists | C4 | `commission` | no | Last-writer-wins documented; do not assert either way |
| `G-044` | **Delete behaviour of an unenforced lookup — the sources conflict** | C4 | `empirical-test` | no | Carried as conflicted; verify on the page before designing around either |
| `G-045` | An explicit vendor statement that lists have no column-level security | C6 | `commission` | no | Marked strongly supported but resting on an *absence*, not a quote |
| `G-046` | Current reporting-connector volume and refresh behaviour over large lists | C4, C9 | `commission` | no | Not asserted |

### 3.5 `data/azure-sql.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-047` | Whether the managed relational service supports the recovery models minimal logging depends on | C4, C9 | `commission` | no | Sized against log rate instead |
| `G-048` | Whether a maker can set session context on the connector's connection | C6 | `commission` | **yes** | Carried as not reachable **and open** — decisive for per-user row security |
| `G-049` | Formal deprecation of the historical cold-tier feature, with no successor | C4, C11 | `commission` | no | The *no cheap archive tier* finding stands without it |
| `G-050` | Connector concurrency, isolation, locking and deadlock-retry semantics | C4, C9 | `commission` | no | Carried as `UNKNOWN` |
| `G-007` | Gateway node throughput for platform traffic *(commission candidate)* | C5, C9 | `commission` | yes | Unsized |
| `G-051` | Whether private-network integration requires the managed environment class | C6, C7, C11 | `commission` | no | Same subject as `G-038`, recorded here for the external store |
| `G-052` | Read-access limits on retained backups | C4 | `commission` | no | Retention stated as backup, not archive |
| `G-053` | Any published bulk-load throughput figure | C4, C9 | `measurement` | no | Confirmed absent; the tuning *method* is carried instead |

### 3.6 `data/query-and-delegation.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-003` | Per-operation delegation table per connector *(commission candidate — the highest-value gap in this unit)* | C4 | `commission` | no | Class-level boundaries carried |
| `G-054` | Which operations delegate to a **virtual table** | C4, C5 | `measurement` | no | Absence stated; measurement required |
| `G-055` | Per-function verdicts for free-text search and containment on the governed store | C4 | `commission` | no | Carried as the searchable set plus leading-wildcard throttling |
| `G-056` | The list-store view threshold and per-list item ceiling are **search-derived** in one canonical pass, not first-tier fetched | C4 | `commission` | no | Flagged in the unit itself |
| `G-057` | Read-after-write visibility and isolation semantics for the relational-store connector | C4 | `commission` | no | Listed as verify-and-do-not-assert |
| `G-058` | **Custom-connector throughput ceiling — conflicted by 20×** | C5, C9, C11 | `measurement` | **yes** | Conflict carried, symmetric, decision-blocked (`VC-01`/`VS-08`, `B-08`, `CD-05`) |

### 3.7 `automation/automation-mechanisms.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-059` | Approval reassignment, timeout / escalation and audit-retention mechanics | C2 | `commission` | no | Escalation designed explicitly instead; mechanics not encoded |
| `G-011` | Whether the vendor states cloud flows lack native ordering / dedup / peek-lock *(commission candidate)* | C2, C5 | `commission` | no | *Unsupported until verified* |
| `G-060` | Documented behaviour of a **mid-loop failure** in an iteration construct | C2, C9 | `commission` | no | The three post-failure questions are asked instead |
| `G-061` | Any unit- or contract-test mechanism for a cloud-flow definition | C2, C8 | `commission` | no | A platform-independent test strategy is required instead |
| `G-062` | Whether process-entitlement stacking on a single flow is capped — **the sources disagree** | C2, C11 | `commission` | no | Neither figure encoded; the flow-group rule is carried |
| `G-008` | Broker quota envelopes *(commission candidate)* | C2, C5, C9 | `commission` | no | Selection evidence only, sizing evidence absent |
| `G-006` | Per-operation AI / agent consumption *(commission candidate)* | C2, C11 | `measurement` | yes | Unmodellable in advance; bounded pilot |
| `G-063` | Empirical throughput or latency for **any** mechanism in this domain | C9 | `measurement` | no | Every statement is a published limit, stated as such |

### 3.8 `integration/integration-mechanisms.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-064` | Safe outage and backlog envelope, and business invariants, under **prolonged far-side failure** in tightly-coupled bidirectional sync | C5, C4, C9, C10 | `commission` | **yes** | `UNKNOWN` preserved; bounded failure/recovery test plus explicit reconciliation rules required before approving critical bidirectional sync |
| `G-065` | Throughput and quota for the business-events mechanism | C5 | `commission` | no | Unsized |
| `G-011` | In-platform dead-letter / circuit-breaker constructs *(commission candidate)* | C5, C9 | `commission` | no | *Unsupported until verified*; escalation trigger instead |
| `G-007` | Gateway throughput and at-scale cost *(commission candidate)* | C5, C10, C11 | `commission` | yes | Open item |
| `G-066` | No measurement anywhere in this domain — it reasons entirely from published limits | C9 | `measurement` | no | Stated explicitly; *"this will be fast enough"* is unsupported |
| `G-067` | Dating weakness: the connector pages carrying the most decision-relevant throttle figures are the weakest-dated load-bearing sources in the baseline | C5, C9 | `pilot` | no | Flagged; re-read at the decision date (`VS-27`) |

### 3.9 `security/security-controls.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-068` | Hierarchy (manager / position) security mechanics, and its interaction with matrix units plus column security | C6, C4 | `commission` | no | Other row mechanisms are complete; this one is absent |
| `G-069` | Masking-rule mechanics and limits | C6 | `commission` | partly | Stated as managed-class plus column-security framework only |
| `G-070` | Application access-control scope, bypasses, and interaction with sharing limits | C6, C7 | `commission` | partly | Not asserted |
| `G-071` | Depth of label-driven enforcement over store rows and columns | C6 | `commission` | yes | Carried as discovery and classification only, **not enforcement** |
| `G-072` | Whether any control restricts spreadsheet export or direct analytical-endpoint reads | C6, C10 | `commission` | yes | Stated as open |
| `G-073` | Current status of the two connection-security known issues (secured connection via connection reference; service-principal import) | C6, C8 | `pilot` | yes | Carried as a release-checklist obligation |
| `G-074` | Guest-restriction general-availability state — **two vendor sources disagree** | C6 | `pilot` | partly | Behaviour documented, state flagged |
| `G-075` | Allowlist-policy general availability per maker portal; whether custom and HTTP rule types shipped | C6, C7 | `commission` | yes | Carried as certified-connectors-only |
| `G-010` | Whether managed identity extends beyond in-database plug-ins *(commission candidate)* | C6, C5 | `commission` | yes | Stated as plug-ins only |
| `G-076` | External-surface web-application-firewall cost, rule coverage and limits | C6, C3, C11 | `commission` | partly | Not asserted |
| `G-077` | The cost and entitlement arithmetic of the premium-suite prerequisites | C11, C6 | `commission` | yes | Obligation carried; arithmetic deferred to economics |
| `G-078` | No universal numeric curve relating security-model complexity to runtime performance | C6, C9 | `measurement` | no | `UNKNOWN` preserved; representative pilot at target model complexity |

### 3.10 `governance/governance-and-environments.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-079` | Functional parity between the deprecated community toolkit and the in-product inventory, usage, monitoring and recommendation surfaces | C7, C10 | `commission` | sometimes | Deprecation recorded; parity **not** established |
| `G-080` | Any de-scoping guidance ahead of the dated licence enforcement | C7, C11 | `commission` | **yes** | `TW-V3` carried as a dated tripwire |
| `G-081` | Whether environment-group rules will gain per-environment exceptions or a hierarchy | C7 | `commission` | sometimes | Taxonomy must currently be built around the absence of exceptions |
| `G-075b` | *(see `G-075`)* | | | | |
| `G-082` | Whether group-membership automation via the administration connector shipped | C7 | `pilot` | no | Not asserted |
| `G-083` | Governance of agent surfaces beyond data policies, virtual connectors and sharing | C7, C6 | `commission` | where agents are in scope | Not asserted |
| `G-084` | Inventory and API fidelity for external sites and desktop automations | C7, C10 | `commission` | sometimes | Detection coverage stated as partial |
| `G-085` | Residency and retention implications of tenant-level analytics | C7, C4 | `commission` | rarely | Not asserted |

### 3.11 `alm/release-and-lifecycle.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-005` | Previous-version-redeployment default and retention *(commission candidate)* | C8, C12 | `commission` | **yes** | The enable-in-advance obligation is stated without the default |
| `G-086` | Whether pipelines gained source-code integration, multi-solution support, import-behaviour choice or multi-developer support | C8 | `pilot` | yes | Carried as *"not currently"*, `VC-10` named |
| `G-087` | Outcome of the dated pipeline-target auto-conversion | C8, C7, C11 | `pilot` | yes | `TW-V1`; verify before costing an in-product lifecycle path |
| `G-088` | Native source-control integration general-availability state and canvas coverage | C8 | `pilot` | yes | Carried with the canvas caveats |
| `G-089` | Whether a supported first-party functional-test option replaced the deprecated engine | C8, C9 | `commission` | yes | Absence carried; browser automation named as the stated path |
| `G-090` | Break-list churn for the block-unmanaged-customizations control | C8, C7 | `pilot` | yes | Carried with `VC-10` |
| `G-091` | Deployment-settings-file capabilities, and their interaction with delegated deployment | C8 | `commission` | no | Not asserted |
| `G-092` | The component catalogue as a distribution mechanism | C8 | `outside-corpus` | no | Omitted |
| `G-093` | Plug-in and custom-code unit-testing practice, and first-party support for it | C8, C9 | `commission` | sometimes | Not asserted |
| `G-094` | Entitlement position of developer-plan environments used as pipeline targets | C8, C11 | `commission` | yes | The cheap-topology assumption is flagged, not resolved |
| `G-095` | Build-tool task-version position; whether basic-credential service connections survive | C8, C6 | `pilot` | sometimes | Multi-factor incompatibility carried |

### 3.12 `performance/performance-and-scale.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-063b` | **No empirical throughput, latency or concurrency measurement exists anywhere in the baseline** — vendor or independent | C9 | `measurement` | no | The absence is carried **as evidence**, and converted into a measurement obligation. Canonical reservation, permanently open |
| `G-027b` | *(see `G-027`)* concurrent-user figure; plus per-device concurrent-request limits for mobile clients | C9, C3 | `measurement` | no | Replaced by funnel-point analysis plus a tested baseline |
| `G-078b` | *(see `G-078`)* security-model performance curve | C6, C7, C9 | `measurement` | no | `UNKNOWN` with a pilot obligation |
| `G-096` | Actual web-server count per environment, and how it scales with licensing | C9 | `outside-corpus` | no | Vendor states the factors are undisclosed; design must be tolerant, not sized. **This is why the per-identity protection triple was deliberately not restored** |
| `G-018b` | *(see `G-018`)* purchased external-site capacity versus delivered throughput | C9, C3, C11 | `commission` | yes | The only scale dial is unquantified |
| `G-097` | Protection behaviour under **burst** rather than sustained load | C9 | `commission` | no | Not asserted |
| `G-098` | Whether the application-request timeout envelope applies to all application surfaces or only one | C9, C3 | `commission` | no | Carried at the mechanism level only |
| `G-099` | Currency of the aged network-latency and deployment-window guidance | C9, C10 | `pilot` | no | Carried as direction, not specification, with the aged-source caveat |

### 3.13 `economics/licensing-and-cost-drivers.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-006b` | *(see `G-006`)* per-operation AI and agent consumption | C11, C2 | `measurement` | yes | *Unmodellable in advance*; bounded pilot then size for the peak month |
| `G-002` | Whether one premium capability obliges premium entitlement for every user *(commission candidate)* | C11, C6 | `commission` | **yes** | Carried as a per-engagement **verification item**, never an assumption |
| `G-007b` | *(see `G-007`)* on-premises gateway cost at scale | C11, C5 | `commission` | yes | Flagged as an open item |
| `G-100` | Relative cost of long-term retention and archival versus live storage | C11, C4 | `commission` | yes | Archival recommended with unknown relative cost |
| `G-101` | Elapsed-time and capacity cost of an environment copy or restore beyond the free-space precondition | C11, C8, C10 | `measurement` | no | Precondition carried (`VS-17`); cost not |
| `G-102` | Any comparative total-cost-of-ownership against named alternative classes | C11, C12 | `outside-corpus` | yes | The unit **refuses the comparison** and routes to the symmetric method |
| `G-014` | Multi-tenancy and resale licensing *(commission candidate)* | C11, C12 | `commission` | **yes** | Scope-blocker; no answer offered |
| `G-087b` | *(see `G-087`)* whether the pipeline conversion completed as announced | C11, C8 | `pilot` | yes | Open question with a pre-costing verification |
| `G-103` | Storage-rate and run-cost **ratios** — dropped as price-adjacent as well as unowned | C11 | `outside-corpus` | no | Ordinal ordering carried instead; deliberate |

### 3.14 `operations/operability-and-support.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-012` | Composite availability for a business flow *(commission candidate)* | C10, C9 | `commission` | **yes** | Weakest-dependency rule carried; do not multiply or average percentages |
| `G-013` | Measured restore duration at representative volume *(commission candidate)* | C10 | `measurement` | **yes** | A timed rehearsal is prescribed as the substitute |
| `G-104` | Programmatic capacity alerting beyond the periodic administrator email | C10, C11 | `commission` | no | Named owner carried as the compensating control |
| `G-105` | Project-level view of the shared tenant request pool | C10, C11 | `commission` | no | Named tenant owner is the compensating control |
| `G-106` | Operational handover from delivery partner to customer operations | C10 | `outside-corpus` | **yes** | Likely permanently open; recommend defining it as an aisa deliverable |
| `G-107` | Telemetry retention and query cost at realistic volumes | C10, C11 | `measurement` | yes | Cost *direction* stated twice; magnitude not |
| `G-108` | Any independent post-mortem corpus for this domain — nothing triangulates the vendor documentation | C10 | `outside-corpus` | no | Recorded as an evidence-quality limit |
| `G-099b` | *(see `G-099`)* whether the aged intensive-operations list still holds | C10, C9 | `pilot` | no | Direction only |
| `G-109` | Aggregated-monitor coverage of the primary data store, and when it arrives | C10 | `pilot` | no | The most common degradation source has no surface; stated |
| `G-110` | Live-monitor unsupported-scenarios list | C10 | `pilot` | no | Not asserted |

### 3.15 `architecture/patterns.md`

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-063c` | *(see `G-063`)* no capacity, latency or throughput figure for **any** composition component | C9, C2, C5 | `measurement` | no | Stated plainly as a boundary of the whole file |
| `G-111` | Whether a mediation tier changes platform request metering, and whether a facade's backend calls count | C5, C11 | `commission` | **yes** | *"Do not claim relief"* |
| `G-112` | Write-through virtualization as a supported production pattern, and its performance | C4, C5 | `commission` | **yes** | Kept **conditional** with weak production evidence — canonical reservation preserved |
| `G-113` | Whether a private-egress-capable in-transaction component can publish to a broker while transaction-scoped | C5, C6 | `commission` | **yes** | Kept as inference / `UNKNOWN`; the only proposed workaround for the private-network collision |
| `G-114` | Whether the enterprise-boundary composition has any vendor or industry articulation | C5, C7, C12 | `commission` | yes | **Supported synthesis, not vendor-endorsed** — lineage preserved (canonical reservation) |
| `G-064b` | *(see `G-064`)* dual-write failure semantics under sustained far-side failure | C4, C5 | `commission` | yes | `UNKNOWN` with a required test |
| `G-120` | Cost comparison of the mediated composition's two variants | C5, C11 | `commission` | no | The choice is currently made on convention |
| `G-065b` | *(see `G-065`)* business-events throughput envelope | C5 | `commission` | no | Unsized |
| `G-115` | Run-history retention and replay confirmed from a first-tier source | C2, C10 | `commission` | no | Observability verdicts for two compositions rest on it |
| `G-116` | Whether a vendor-published platform pattern catalogue exists beyond a small integration set | C12 | `outside-corpus` | no | Stated: much of the naming is this baseline's synthesis |
| `G-117` | Quantification of the enterprise boundary's lead-time and autonomy cost | C12, C10 | `commission` | no | The main weakness is inference only |

### 3.16 Cross-cutting — the agent / conversational boundary

| Id | Gap | Concern | Class | Blocking | Runtime treatment today |
|---|---|---|---|:--:|---|
| `G-118` | **No evaluable agent / conversational capability class exists in the baseline** — `UNKNOWN` in every dimension | C1, C2, C3, C6, C11 | `commission` | **yes** | **No domain file created.** Where the question is material the output is `UNKNOWN` / decision blocked via scope-blocker `BS-03` and row `VS-20`, with the dated entitlement tripwire `TW-V2`. Nothing was invented |
| `G-119` | Whether agent-based automation changes the automation option set | C2 | `commission` | yes | The baseline is silent; the deferral had no owner |

**`G-118`/`G-119` are the one gap explicitly recommended for a *dedicated* commission**, because they are
material, recurring, growing in stakeholder salience, and **not** closable by engagement measurement.

---

## 4. Canonical non-blocking reservations — carried, not filled

All eight survive as unknowns inside the owning units. They are recorded here so they are not mistaken for
Step 4B omissions.

| Reservation | Where carried |
|---|---|
| Prolonged far-side failure in dual-write | `G-064`; `integration/`, `architecture/` |
| Custom-connector throttle conflict | `G-058`; `integration/` §10, `performance/`, `architecture/` |
| Contractual composite availability ≠ service availability | `G-012`; `operations/`, `performance/` |
| Security-model performance curve | `G-078`; `security/`, `performance/` |
| Write-through virtual-table production evidence | `G-112`; `architecture/`, `data/dataverse.md` |
| Enterprise-boundary pattern is supported synthesis | `G-114`; `architecture/` |
| Corpus is limits-based, not benchmark-based | `G-063`; `performance/` and every mechanism unit |
| Validation-level identifier overload | authoring-side only; no runtime effect |

---

## 5. What this annex is not

- **Not a runtime registry.** No gap registry was created in `library/`. Engagement-level unknowns live on
  the engagement's own Shared Understanding rows with their `custo` and `swing`.
- **Not a commission list.** §2 records candidates. Commission later only where **material + recurring +
  not closed by measurement**.
- **Not a to-do list for Step 4C.** Step 4C is a semantic and pull gate; these gaps are inputs to it only
  insofar as it should test that a reasoner **emits `UNKNOWN` at a gap instead of filling it**.
