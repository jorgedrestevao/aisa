# Step 4B — number-adjudication annex (durable)

<!--
provenance: AUTHORING ANNEX
date: 2026-09-04 (created in the Step 4B pre-4C bounded repair; reflects the bounded volatility repair)
source: the per-file number-adjudication tables produced while authoring the 15 RESEARCH units and
        migrating the 10 CRAFT units. Nothing regenerated from model knowledge.
scope: AUTHORING-SIDE ONLY. This table is never copied into runtime.
-->

## 0. Classification vocabulary

| Class | Meaning | Runtime effect |
|---|---|---|
| `stable-retain` | A structural, non-volatile fact — a count of enumerated things, not a service limit | Carried **unstamped** |
| `volatile-retain-stamped` | Decision-relevant, canonically supported, owned by a volatility row | Carried as a **documented reading** with its row |
| `register-owned` | Volatile and owned by a row, but the figure itself is not needed to answer the decision | **Boundary shape** carried; figure read at the decision date |
| `implementation-trivia` | Build-time detail, not decision-grade | Retained in `craft/` where it is build guidance; dropped from RESEARCH units |
| `unsupported-remove` | No canonical support, or an invented threshold, or a price, or a selection verdict | **Removed** |
| `conflicted` | Canonically conflicted | **Carried on neither side**; the register owns the re-verification |

## 1. Effect of the bounded volatility repair

Step 4B dropped ~60 decision-relevant figures because §5.2's third condition (*a figure must name the row
that owns its re-verify trigger*) could not be met — there was no owning row. The bounded repair added 19
family rows and split `VS-04`, so those subjects now **have** owners. They were then re-adjudicated
against the survival test — *would knowing this reading materially help test a real requirement?* — and
only a disciplined subset returned.

```text
figures dropped in Step 4B for want of an owner        ~60
subjects re-adjudicated in this repair                  60
restored: figure FAMILIES                               15
restored: individual numeric readings                   65   (14 carriers, 8 units)
left as boundary shape, now with a named owner          14   subjects
deliberately left out entirely                          14   subjects
measurement-owned (no published figure would settle)     2   subjects
```

**Restoring a figure was never automatic.** *"The new register can own it"* is not a reason to carry it —
that is stated explicitly in the repair brief and was applied.

---

## 2. Restored to runtime — 15 families, 65 individual readings

*Counted two ways because both matter: a **family** is one coherent reading set with one owner (what the register tracks); an **individual reading** is one number a requirement is compared against (what a reasoner uses). 15 families · 65 readings · 14 stamped or inline carriers · 8 units.*

Each has a single stamped home. No figure is stamped in two files.

| Family | Readings restored | Home | Row |
|---|---|---|---|
| Content throughput per 24 h by owner profile | three profile values, and the ~fiftyfold spread | `automation/` §4 | `VS-03` |
| Interface-automation (RPA) queue envelope | queue depth · maximum wait · dispatch latency · per-run ceiling · logged-action ceiling | `automation/` §4 | `VS-16` |
| Synchronous response windows | flow and consumption sibling · the standard sibling · the compute host's hard cap · canvas outbound · in-transaction extension · the long asynchronous window | `automation/` §5 | `VS-23` |
| Orchestration structural ceilings | action count · nesting depth · array items · in-run parallelism default and maximum · the de-batching collapse | `automation/` §5 | `VS-24` |
| Run-duration ceilings | flow per-run window · the sibling's stateful window · the stateless cliff · trigger-inactivity suspension | `automation/` §5 | `VS-12`, `VS-13` |
| Retry defaults by profile | low-profile attempts and window · higher-profile attempts and window | `automation/` §7 | `VS-39` |
| Disablement countdowns | sustained failure/throttling window · trigger-inactivity window | `automation/` §7 | `VS-09` |
| Payload and batch ceilings | flow message and chunked variant · gateway request and response caps · webhook truncation · broker-plug-in strip-then-fail thresholds · requests per batch | `integration/` §5 | `VS-10` |
| Connector execution envelope | list-store per-connection window · governed-store per-connection window · delegated-identity HTTP window · relational connector CRUD window, concurrency and per-user rate · action timeout | `integration/` §5 | `VS-27` |
| Alternate-key budget | keys per table · key columns · total key width | `data/dataverse.md` | `VS-30` |
| List-store join ceiling | join-type columns per view | `data/sharepoint.md` | `VS-33` |
| List-store permission scopes | supported ceiling · recommended ceiling · inheritance-break item count | `data/sharepoint.md` | `VS-29` |
| Aggregation ceiling and replication floors | aggregate/chart/grid row ceiling · minimum replication increment · refreshes per period · maximum run | `data/store-boundaries.md` | `VS-06` |
| Team-scoped combined ceiling | the combined storage ceiling | `application/` §3 | `VC-07` |
| Backup retention by environment class | default window · production-managed window · trials not backed up | `operations/` | `VS-07` |

**Survival-test rationale, in one line each:** every one of these is a figure an engagement requirement is
*literally compared against* — *"the caller waits N seconds"*, *"we move N documents a day"*, *"the natural
key is N columns"*, *"N people each need their own row scope"*, *"the report aggregates N rows"*, *"recovery
must reach N days back"*.

---

## 3. Left as boundary shape, now with a named owner (14 subjects)

Owned by a row, deliberately without a figure — the shape answers the decision and the figure would not
improve it. A reasoner who needs the number now knows exactly which row to re-read.

| Subject | Row | Why the shape suffices |
|---|---|---|
| Control propagation and enforcement latency | `VS-21` | The decision is *"is there a window in which this is not enforced?"* — yes is the answer; the length is an operating input |
| Credential and session revocation window | `VS-22` | *"A removed user may still have access for a bounded period"* is the design consequence |
| Application-artefact composition ceilings | `VS-25` | The decision is *"will this artefact hold the whole experience?"* — the remedy (split, or change surface) does not depend on the count |
| Release-artefact packaging ceilings | `VS-26` | The consequence — large content travels outside the solution — is the content |
| Customer-operated estate currency obligations | `VS-28` | A standing obligation, not a threshold to compare against |
| Governed-store derived-column and rule budgets | `VS-30` | *"There is a per-table budget"* is what changes the model; only the alternate-key half is compared against a requirement (§2) |
| Search budget and index freshness | `VS-31` | The decision is *"is search a designed, budgeted, eventually-consistent surface?"* |
| Horizontally-scaling table bounds | `VS-32` | Its **maturity state is contradicted**, so the row owns re-verification rather than a value |
| Query traversal depth and expandable entities | `VS-33` | The remedy is a server-side view — a data-model change independent of the depth |
| External relational tier envelope | `VS-34` | The decision-grade fact is *log rate is the ceiling and it does not rise with compute* |
| Customer-managed-key operational windows | `VS-35` | *"A tier-0 dependency with a cliff and no automatic healing"* is the decision |
| Support plan structure and coverage | `VS-36` | The decision is *what must we staff ourselves* |
| Cross-region protection envelope | `VS-37` | *No recovery-time objective is published* — the absence is the finding |
| Offline cache bounds | `VS-38` | The offline **depth ladder** decides the surface; also the figure was not captured verbatim (`G-025`) |

---

## 4. Left out entirely (14 subjects)

Adjudicated `implementation-trivia`, `unsupported-remove` or price-adjacent. No owning row created.

| Subject | Class | Reason |
|---|---|---|
| Derived-computation recurrence floor | `implementation-trivia` | *Asynchronous, hours-scale, therefore cannot gate a write* is the whole decision |
| Per-list item ceiling | `register-owned`, dropped | Explicitly *never the binding boundary* — the view threshold binds first |
| Governance recommendation cadence and warm-up | `implementation-trivia` | *Detection is periodic, measured in days* suffices |
| Developer-environment disuse window | `implementation-trivia` | An operating detail |
| Environment-variable propagation window | `implementation-trivia` | *Propagation is not immediate* suffices |
| Capacity notification threshold | `implementation-trivia` | *Notifications begin only when headroom is already low* is the point |
| Monitoring metric's reported percentile | `implementation-trivia` | *A single non-tail percentile, so tail latency is invisible* is the decision-grade fact |
| Service-update station count | `implementation-trivia` | The **directional rule** is stable and is what is carried |
| Trial-environment lifetime | `implementation-trivia` | — |
| Storage-rate and run-cost ratios | `unsupported-remove` | **Price-adjacent** — a numeric ratio moves with prices. Ordinal ordering carried instead |
| Bundled credit quantity | `unsupported-remove` | Price-adjacent; `TW-V2` owns the removal |
| Cascading-retry arithmetic | `implementation-trivia` | *Multiplies rather than adds* is the mechanism |
| Store asynchronous-request retry count | `implementation-trivia` | *Bounded retries with exponential backoff* suffices |
| Notification milestones preceding a dated tripwire | `implementation-trivia` | The tripwire owns the date |

### 4.1 Measurement-owned (2 subjects) — deliberately never carried

| Subject | Why no published figure would settle it |
|---|---|
| Per-identity service-protection triple | The effective value is *the published figure × an undisclosed, licence-dependent web-server count*. Carrying the figure invites exactly the arithmetic the baseline forbids. `VC-04` owns the re-verification; the design must be **tolerant, not sized** |
| Any concurrent-user figure | **None is published anywhere.** The real constraints are per-identity limits and contention on shared rows and identities. Closed only by a load test against a production-like environment |

---

## 5. The five conflicted figures — carried on neither side

| Subject | Rendering | Owner |
|---|---|---|
| **Per-mechanism (custom-connector) throughput ceiling** — two maintained vendor pages disagree by 20× | *conflicted · decision-blocked until measured*, **symmetric across option classes**, in `integration/` §10, `performance/`, `architecture/` | `VC-01` / `VS-08`, `B-08`, `CD-05` |
| Tenant default database capacity — internally inconsistent in one source | conflicted; confirm in the administration centre | — |
| Elastic-table maturity / general-availability state | unresolved; a maturity risk; the row owns re-verification, never an answer | `VS-32`, `VC-10` |
| Elastic-table alternate-key support | contradicted between sources | `VS-32` |
| Platform scale positioning versus the published envelopes | **both adjectives dropped**; capability rows used | — |

**The bounded repair settled none of them.** `VS-27` explicitly **excludes** the conflicted
custom-connector ceiling so that a family row could not quietly absorb it into a settled value.

---

## 6. Per-source-file adjudication

Every numeral encountered in the 13 pre-existing files and in the canonical sections read while authoring.

### 6.1 `powerfx-patterns.md` → `craft/powerfx.md`

| Numeral | Class | Disposition |
|---|---|---|
| Client retrieval ceiling (default and maximum), stated in four places | `register-owned` | **Deleted from craft**; owner is `data/query-and-delegation.md` (`VS-02`, stamped there) |
| Per-operation delegability matrices, two connectors | `register-owned` | Sections **deleted**; owner is `data/query-and-delegation.md` |
| Chunked-load chunk size | `register-owned` | Deleted; the owner supplies the window |
| Nested-condition depth ≤ 3 | `implementation-trivia` | Retained |
| Notification durations | `implementation-trivia` | Retained |
| Tax multiplier, overdue-day threshold, gallery example values | `implementation-trivia` | Retained (illustrative) |

### 6.2 `screen-patterns.md` → `craft/screen-patterns.md`

| Numeral | Class | Disposition |
|---|---|---|
| Status palette hex values | `implementation-trivia` | Retained |
| Density pixel and point values; column-count bands | `implementation-trivia` | Retained |
| Async debounce | `implementation-trivia` | Retained |
| Sidebar item count; navigation depth | `implementation-trivia` | Retained |
| Responsive breakpoints | `implementation-trivia` | Retained |
| Screen-count planning bands | `implementation-trivia` | Retained, relabelled team planning bands |
| *Screen count > N → evaluate the other surface* | `unsupported-remove` | **Deleted** — a surface-fit verdict |
| Field-count thresholds and hard caps | `implementation-trivia` (named hard contract) | Retained **verbatim** |
| Fields per group; section thresholds; sub-view count | `implementation-trivia` | Retained |

### 6.3 `screen-consolidation-rules.md` → `craft/screen-consolidation-rules.md`

| Numeral | Class | Disposition |
|---|---|---|
| Editable-field bands; screen-type thresholds; hard caps (fields, actions) | `implementation-trivia` (**named hard contract**) | **Byte-identical.** Verified by diff against the prior revision |

### 6.4 `excel-patterns.md` → `craft/excel-translation.md`

| Numeral | Class | Disposition |
|---|---|---|
| Rounding precision; decimal scale; string offsets | `implementation-trivia` | Retained |
| Iterative-solver seed, tolerance, maximum iterations | `implementation-trivia` | Retained, **relabelled an implementation choice, not a platform limit** |
| Delegation verdict cells | `register-owned` | Converted to **check-prompts** against the owner |

### 6.5 `flows-patterns.md` → `craft/flow-craft.md` + `automation/automation-mechanisms.md`

| Numeral | Class | Disposition |
|---|---|---|
| Connector per-window limits (four values) | `register-owned` | **Deleted from craft**; the decision-grade subset restored in `integration/` (`VS-27`) |
| Retry count and back-off interval | `implementation-trivia` | Retained in craft as *our configured setting* |
| Ingestion chunk size | `implementation-trivia` | Replaced by *size from the destination's guidance* |
| Child-definition nesting; synchronous cap | `register-owned` | Deleted from craft; restored in `automation/` (`VS-24`, `VS-23`) |
| Card expiry (twice) | `register-owned` | Deleted; owner named |
| Items-per-minute throttle threshold | `register-owned` | Deleted; owner named |
| Reporting refresh cadences; minimum interval | `register-owned` | Minimum **deleted**; cadence now derived from staleness tolerance |
| List-store item threshold in a reporting note | `register-owned` | Deleted; owner named |
| Action-count decomposition heuristics (three values) | `implementation-trivia` | Retained, **labelled team debuggability conventions** |
| Complexity-tier action bands and day estimates | `implementation-trivia` | Retained, labelled our tiering |
| Expression constants (tick divisor, format token, weekday base) | `stable-retain` | Retained |

### 6.6 `security-patterns.md` → `craft/security-craft.md` + `security/security-controls.md`

| Numeral | Class | Disposition |
|---|---|---|
| Approval-authority currency example | `unsupported-remove` | **Deleted** (price/currency); reworded to *below a stated value threshold* |
| Currency symbol in a format mask | `unsupported-remove` | **Deleted** |
| Retention years (two values) | `implementation-trivia` | Retained as a team default with `TODO(team)` and a named compliance owner |
| Column-security exclusion count | `stable-retain` | Carried as the **named column classes**; the count dropped |
| Endpoint-filter connector count; policy fragmentation exponent | `implementation-trivia` | Carried as *a handful* / *combinatorially* |
| Enforcement and propagation latencies | `register-owned` | Boundary shape; owner now `VS-21` |
| Token lifetime | `register-owned` | Boundary shape; owner now `VS-22` |
| Firewall character and range limits; propagation minutes; rollout weeks | `implementation-trivia` | Dropped |
| Private-network address allocations | `implementation-trivia` | Dropped (integration-owned) |
| Gateway port numbers | `implementation-trivia` | Dropped |
| Tenant-isolation rule threshold | `implementation-trivia` | Dropped |
| Security-score hygiene triggers (two values) | `unsupported-remove` | **Dropped** — preview-tool hygiene; carrying them would read as invented thresholds |
| Hierarchy-security users per manager | `unsupported-remove` here | Flagged `UNKNOWN` in the source; the figure is data-area-owned (`G-068`) |
| Customer-key encryption and previous-version windows; per-vault ceilings | `register-owned` | Boundary shape; owner now `VS-35` |
| Key sizes | `implementation-trivia` | Dropped |
| Secured-connection cutover and endpoint-republish dates | `register-owned` | Boundary shape; owner now `VS-28`/`VC-10` |
| Service availability percentage | out of scope | Composite is `UNKNOWN` (`G-012`) |

### 6.7 `azure-sql-reference.md` → `craft/sql-delivery-conventions.md` + `data/azure-sql.md`

| Numeral | Class | Disposition |
|---|---|---|
| Row-size, column-count and index-count limits; compute-unit-by-tier table | `register-owned` | **Whole table deleted** from craft; the decision-grade subset (log rate, storage ceilings) now owned by `VS-34` as shape |
| *Peak load + N % buffer* | `unsupported-remove` | **Deleted** — an invented sizing rule; replaced by *size against measured peak* |
| Fragmentation threshold | `unsupported-remove` | **Deleted** — an invented threshold |
| Type range annotations | `register-owned` | Annotations deleted; owner named |
| Type precision and length standards | `implementation-trivia` | Retained (team standard) |
| Connector query length and result-row caps; hardcoded page size | `register-owned` | Deleted; replaced by a variable set from the owner (`VS-27`) |
| Batch sizing range | `implementation-trivia` | Retained as a convention, **explicitly not a capacity statement** |
| Top-N-per-group, window-frame and temporal example values | `implementation-trivia` | Retained |
| Capacity add-on per-GB rates | `unsupported-remove` | **Deleted** (prices) |

### 6.8 `dataverse-reference.md` → `data/dataverse.md`

| Numeral | Class | Disposition |
|---|---|---|
| Per-user and per-app licence prices | `unsupported-remove` | **Deleted** (prices) |
| Alternate-key budget (three values) | `volatile-retain-stamped` | **Restored** in this repair → `VS-30` |
| Derived-column budgets and recurrence floor | `register-owned` | Boundary shape → `VS-30`; the floor is `implementation-trivia` |
| Table-scoped rule ceiling | `register-owned` | Boundary shape → `VS-30` |
| Text length limits; filterable-text index threshold | `register-owned` / `implementation-trivia` | Index threshold → `VS-30` as shape; the rest dropped |
| File and image column maximum sizes | `implementation-trivia` | Dropped; **irreversibility** is the decision-grade half |
| Audit default retention | `volatile-retain-stamped` | `VS-05` |
| Audit truncation threshold | `implementation-trivia` | Dropped |
| Long-term-retention database saving | `volatile-retain-stamped` | `VC-07` |
| Backup and recycle-bin windows | `register-owned` | `VS-07` |
| Three capacity meters; borrowing order | `stable-retain` | Retained |
| Analytical-replica storage ratio | `register-owned`, unpublished | `VC-07`; no figure exists (`G-030`) |
| Tenant default database capacity | **`conflicted`** | Neither figure carried |
| Elastic partition size; elastic scale claim | `register-owned` | Boundary shape → `VS-32` |
| Search budget values (four) | `register-owned` | Boundary shape → `VS-31` |
| Team-scoped combined ceiling | `volatile-retain-stamped` | **Restored** in this repair → `VC-07` |
| Service protection triple | **measurement-owned** | Deliberately not carried (§4.1) |
| Recycle-bin day range; restore headroom minimum; storage-report lag | `implementation-trivia` | Dropped |

### 6.9 `sharepoint-reference.md` → `data/sharepoint.md`

| Numeral | Class | Disposition |
|---|---|---|
| Per-view item threshold | `volatile-retain-stamped` | `VS-04` |
| Unique-permission ceilings (three values) | `volatile-retain-stamped` | **Restored** in this repair → `VS-29` (split from `VS-04`) |
| Join-type column ceiling | `volatile-retain-stamped` | **Restored** in this repair → `VS-33` |
| Per-list item ceiling | `register-owned`, dropped | Never the binding boundary |
| Row-byte budget; recycle-bin window; per-file size; encrypted-move break size | `register-owned` | Boundary shape only |
| Quick-export decimal precision | `implementation-trivia` | Numeral removed, shape kept |
| **Row-count disqualification threshold** | `unsupported-remove` | **DELETED** — a deleted R0 gate with an invented number |
| **Formula-count disqualification threshold** | `unsupported-remove` | **DELETED** — same |
| **The growth ladder and its migrate verdict** | `unsupported-remove` | **DELETED** — invented thresholds **plus** a selection verdict |
| Indexed-column maximum | `unsupported-remove` here | Contradicted by the baseline: the online maximum is `UNKNOWN` (`G-042`) |

### 6.10 `delegation-matrix.md` → `data/query-and-delegation.md`

| Numeral | Class | Disposition |
|---|---|---|
| Client ceiling — **the three prior copies disagreed** | `volatile-retain-stamped` | Resolved against canonical only; `VS-02`, stamped once |
| Per-operation delegability verdicts | `register-owned` | Class-level behaviour carried; the per-operation table is `G-003` |
| Maintenance instruction (*bump the pack version when the matrix changes*) | `unsupported-remove` | Superseded by the register |

### 6.11 `estimation-model.md` → `craft/estimation-model.md`

| Numeral | Class | Disposition |
|---|---|---|
| Six per-user licence prices; two tier prices | `unsupported-remove` | **Section deleted, not migrated** |
| Cost column (currency per day × days) | `unsupported-remove` | **Deleted**; days only |
| Price front-matter and *confirm with the reseller* instruction | `unsupported-remove` | **Deleted** |
| Effort tables; multipliers; buffer; phase weeks; overlap; worked example | `implementation-trivia` | Retained (own-practice calibration, days only) |
| Integration, migration, role and reference-list effort values | `implementation-trivia` | Retained |
| Formula-count multiplier trigger | `implementation-trivia` | Retained but **reworded to remove an invented hard threshold** |

### 6.12 `anonymization.md` → `craft/anonymization.md`

| Numeral | Class | Disposition |
|---|---|---|
| National identifier format, checksum weights and modulus | `stable-retain` | Retained (national format, not a platform limit) |
| Postal and account-number structures | `stable-retain` | Retained |
| Real bank codes listed as *never use* | `implementation-trivia` | **Named-code map removed**; the unallocated-range rule kept |
| Synthetic value ranges, distributions and jitter | `implementation-trivia` | Retained; currency removed from the heading |

### 6.13 `delivery-conventions.md` → `craft/delivery-conventions.md`

| Numeral | Class | Disposition |
|---|---|---|
| Hypercare duration; stamping sample size | `implementation-trivia` | Retained with `TODO(team)` |

### 6.14 Canonical sections read while authoring the new units

| Numeral family | Class | Disposition |
|---|---|---|
| Synchronous windows across the mechanism family (five values) | `volatile-retain-stamped` | **Restored** → `VS-23` |
| Structural definition ceilings (five values) | `volatile-retain-stamped` | **Restored** → `VS-24` |
| Run duration, stateless cliff, inactivity suspension | `volatile-retain-stamped` | **Restored** → `VS-12`, `VS-13` |
| Disablement countdowns | `volatile-retain-stamped` | **Restored** → `VS-09` |
| Retry attempts and windows by profile | `volatile-retain-stamped` | **Restored** → `VS-39` |
| Content throughput per profile | `volatile-retain-stamped` | **Restored** → `VS-03` |
| RPA queue envelope (five values) | `volatile-retain-stamped` | **Restored** → `VS-16` |
| Connector windows (six values) | `volatile-retain-stamped` | **Restored** → `VS-27` |
| Payload, truncation and batch ceilings (six values) | `volatile-retain-stamped` | **Restored** → `VS-10` |
| Aggregation ceiling; replication floors | `volatile-retain-stamped` | **Restored** → `VS-06` |
| Backup retention by class | `volatile-retain-stamped` | **Restored** → `VS-07` |
| External-site cache floor | `volatile-retain-stamped` | `VS-01` |
| Delegation default and maximum | `volatile-retain-stamped` | `VS-02` |
| List-view threshold | `volatile-retain-stamped` | `VS-04` |
| Entitlement request sets (official and transition) | `register-owned` | **Not carried** — the *instruction to size against official limits* is the content |
| Custom-connector throughput | **`conflicted`** | Neither side |
| Gateway host minimum and node count | `register-owned` | Boundary shape → `VS-11` |
| Recovery-point and recovery-time objectives; enablement lead time | `register-owned` | Boundary shape → `VS-37` |
| Guided-stage caps; site checker thresholds; report-visual rows; wrapper bundle size; pages and connectors per app | `register-owned` | Boundary shape → `VS-25` |
| Solution size; environment-variable value length | `register-owned` | Boundary shape → `VS-26` |
| Log-rate and per-tier storage ceilings; session and worker counts | `register-owned` | Boundary shape → `VS-34` |
| Lookup traversal depth; expandable entities | `register-owned` | Boundary shape → `VS-33` |
| Support severity windows and effort cap | `register-owned` | Boundary shape → `VS-36` |
| Offline record-set ceiling; local file-cache envelope | `register-owned` | Boundary shape → `VS-38`; figure also not captured verbatim (`G-025`) |
| Vendor canvas scale claim; third-party screen and control heuristics | `unsupported-remove` | **Not encoded** — the source policy forbids treating a vendor scale adjective as evidence, and a gate condition forbids the heuristics |
| Practitioner concurrency and row-count figures | `unsupported-remove` | **Not encoded** — explicitly unverified in the baseline |
| A vendor target-writing example latency | `unsupported-remove` | Carried as *a target-writing example*, no figure |
| All prices, SKU rates and per-unit currency values | `unsupported-remove` | **Zero carried anywhere** |

---

## 7. Verification statement

- **No price token survives in any runtime domain file.** Asserted mechanically
  (`test_no_prices_anywhere`, which scans prose and skips fenced sample code).
- **Every stamped reading names a row that exists**, and every row referenced by a unit exists. Asserted
  mechanically.
- **No conflicted figure is carried numerically.** Asserted mechanically for the live conflict.
- **No unit reads as a current-facts database** — the bound is on stamped figures per unit, not on row
  references, because naming a row in a *what must be verified* table is the sanctioned pattern.
- **Every one of the 52 register rows is referenced by at least one unit, and no unit references a
  non-existent row.** Asserted mechanically after the bounded repair.
