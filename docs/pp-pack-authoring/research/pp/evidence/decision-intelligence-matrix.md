Research Status: CANONICAL
Research Confidence: MEDIUM
Block: D — Decision Intelligence
Companion to: Areas 13, 14, 15
Gate: PASS — Block D Final Bounded Gate Recheck
Canonicalization Basis: Block D Final Bounded Gate Recheck (`block-d-final-gate-recheck.md`)
Upstream Evidence Baseline: Areas 1–12 canonical files (`canonical-manifest.md`)
Canonicalized: 2026-09-03
Freeze Status: FROZEN FOR PP PACK AUTHORING

# Decision Intelligence Matrix — Block D

Derivation date: **2026-09-03**.
Inputs: `anti-patterns.md` (Area 13, 68 entries) · `alternatives.md` (Area 14, 11 classes) · `decision-criteria.md` (Area 15, 116 criteria) · `canonical-manifest.md` and the twelve canonical Area 1–12 files.

**Purpose.** Make Block D a **decision network** rather than three separate documents. The matrix shows, per criterion, which direction each state pushes the architecture, which anti-patterns become detectable, and which alternative classes come into scope.

**What this is not.** Not a score. Not a lookup table that returns an answer. §5 states the evaluation order, and §6's adversarial tests show why order matters: several scenarios produce a *different* outcome depending on whether disqualifiers are evaluated before or after direction.

---

## 1. How to read the matrix

| Column | Meaning |
|---|---|
| **Criterion** | `DC-D-NNN` from `decision-criteria.md` §4 |
| **Positive PP signal** | The state under which no documented constraint is violated. Never "Microsoft endorses" — the corpus's own phrasing rule. |
| **Conditional / hybrid signal** | The state that introduces a stated, measurable condition, or that forces decomposition rather than relocation. |
| **Negative / exit signal** | Opens with the **class** in `decision-criteria.md` §2.5's taxonomy, then the signal. **Every cell states its content**: an `Xp` / `Xr` / `Xe` names what leaves, an `Xc` names its registered §3 row, an `Ri` names the in-platform redirect, a `Cf` names the criterion it feeds. A bare class marker is a defect — V1 left ten cells bare, which is how a `—` carrying information became a class carrying none. |
| **Anti-patterns** | `AP-D-NNN` that become detectable when this criterion is mishandled |
| **Alternatives** | `ALT-NNN` classes that come into scope. **Read as a candidate set carrying `COMPARATOR EVIDENCE ABSENT` by default** — see below |
| **Evidence** | The canonical areas carrying the boundary. Areas: 1 Suitability · 2 Application · 3 Data · 4 Automation · 5 Integration · 6 Security · 7 Governance · 8 ALM · 9 Performance · 10 Cost · 11 Operations · 12 Patterns |

**Exit classes (repair, 2026-09-03).** This matrix previously carried a bare `—` or a bold exit sentence, and reported **46** substantive exits while `decision-criteria.md` reported **36** and its criterion bodies contained **48**. The three counts disagreed because a real distinction was being *used* and never *named*. `decision-criteria.md` §2.5 now names it, and every exit cell below opens with the class:

**Repair note V2 (2026-09-03).** The V1 five-class taxonomy above was applied consistently and was still unsound: `Xr` admitted criteria whose documented answer is a **different in-platform store or pattern** (nothing leaves), and `Xc` claimed its exit *"lives in §3"* for eighteen criteria that appear in no §3 row. Because this file mapped `Xr` to the exclusion outcomes, a pack reading the row for DC-D-030 would have emitted *"Power Platform excluded for this responsibility"* for a concurrency-driven store change — and **T-02 below, which fires four such rows, correctly concludes fit with constraints**, so this file's rule and its own worked scenario disagreed. `decision-criteria.md` §2.5 now carries four exit classes, two non-exit consequence classes and an explicit class → outcome mapping. Every marker and count below is regenerated from it.

| Marker | Exit? | Meaning |
|---|---|---|
| **`Xp`** | yes | **Platform exit** — the solution scope leaves the platform at a named state. **15 rows.** |
| **`Xr`** | yes | **Responsibility exit** — a named leg, step, attribute, surface, store, mechanism or component **leaves the platform**. The platform legitimately keeps the rest. **26 rows.** |
| **`Xe`** | yes | **Economic exit** — infeasible or unattractive on commercial grounds, with no capability finding. **5 rows.** |
| **`Xc`** | yes, in combination | **Composed-only exit** — no exit from this row alone; the exit lives in a **§3 row that names this criterion**. **8 rows**, and all eight are registered in §3. |
| **`Ri`** | **no** | **In-platform redirect** — a documented in-platform pattern, store, mechanism or surface becomes unavailable and the answer is a **different in-platform choice**. **7 rows.** |
| **`Cf`** | **no** | **Combination input** — no exit and no redirect of its own; the row names the criterion whose exit it feeds. **17 rows.** |
| **`—`** | no | **No exit, no redirect, no named dependency. 38 rows.** |

**Repair note V3 (2026-09-03 — bounded gate repair, `block-d-gate-repair-report.md`).** The Block D gate (`block-d-gate.md`) applied `decision-criteria.md` §2.5's own one-limb `Xr` test to the whole `Xr` class rather than to a named subset, and found two rows still failing it: **DC-D-049** (nothing leaves — the run mechanism's documented answer is an in-platform business record) and **DC-D-068** (nothing leaves — no off-platform destination is named anywhere in the criterion, and it is already registered at §3 row 6). Both are moved here to match `decision-criteria.md`: DC-D-049 → `Ri`, DC-D-068 → `Xc`. The gate also found that `Xc`'s outcome mapping could not be a single global set, because §3's twelve registered rows do not share one consequence; §3 below now carries a Class column stating the reachable `decision-criteria.md` §6.2 class **per row**.

**`Xr` is not a weaker `Xp`, and `Ri` is not a quieter `Xr`.** These are the two misreadings this matrix exists to prevent, and they fail in opposite directions:

- An `Xr` is **equally evidence-backed** as an `Xp` and narrower in scope. It produces a **hybrid or partial-scope** outcome (`decision-criteria.md` §6.2 classes 3, 4, 6), never a whole-solution rejection.
- An **`Ri` is not an exit at all.** It produces class 2 `FIT WITH CONSTRAINTS`, or class 13 where the redirect's destination is a class the corpus documents as sufficient. It may **never** produce classes 3, 4, 5, 6 or 7. Reading an `Ri` as an exclusion is how a store change becomes a platform rejection.
- A **`Cf` produces no outcome on its own.** A pack that terminates on one has answered a dependency instead of a decision; resolve the criterion the cell names.

**The 38 dashes are load-bearing, and so are the 24 non-exit consequence rows.** A criterion with no exit signal cannot reject the platform on its own. Any pack that manufactures one is inventing a threshold the corpus does not have — the failure `anti-patterns.md` AP-D-051 names. **Sixty-two of 116 rows (38 `—` + 7 `Ri` + 17 `Cf`) cannot reject the platform**, which is the honest shape of this evidence.

**The Alternatives column is candidate generation, not evaluation.** `decision-criteria.md` §4A.1 makes `COMPARATOR EVIDENCE ABSENT` the default: **28** criteria carry an evidenced alternative-side signal (§4A.2), **88** carry none, and exactly **one** axis (DC-D-108, deployment model) carries comparator evidence strong enough to prefer one candidate over another. A row that lists `ALT-005, ALT-006` is saying *these come into scope*, not *these will work*.

---

## 2. The matrix

### 2.1 Business (DC-D-001 … 008)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-001 Business criticality | Departmental to business-critical with existing entitlement | Enterprise+ → managed-environment chain, licence-gated observability | **[`Xc`]** (combines via 091, 100, 089) | AP-D-039, 040, 047, 052, 053, 065 | ALT-002, 004, 009, 010 | 11, 10, 1, 8, 12 |
| DC-D-002 Strategic differentiation | Adapted or differentiating internal process | Commodity domain with a partial product fit | **[`—`]** | AP-D-007, 004 | ALT-011, 001, 003, 007 | 1, 2, 10 |
| DC-D-003 Time to value | Weeks–months inside existing entitlement | Immediate + business-critical → obligations have lead times | **[`—`]** | AP-D-052, 041, 047 | ALT-001, 002, 003, 011, 010 | 12, 4, 10, 1 |
| DC-D-004 Expected lifespan | 1–3 years with a funded maintainer | > 5 years → remediation provision, change owner | **[`Cf`]** feeds 107 (frozen-behaviour requirement) | AP-D-058, 065, 067, 006 | ALT-002, 010, 005, 011 | 10, 1, 11, 2 |
| DC-D-005 Process maturity | Stable and consistent | Variable → planned iteration toward stability | **[`—`]** | AP-D-007, 001 | ALT-002, 010, 004 | 1, 10, 4 |
| DC-D-006 Accountable ownership | Named and accepted; automation on a service identity | Nominal for a departmental workload with a stated ceiling | **[`Ri`]** blocks in-platform **patterns** — replication, bidirectional mastering — and, via §4A.2, makes the hybrid/brokered patterns `UNAVAILABLE`; the answer is a single-owner shape with a named owner, not a platform change | AP-D-036, 053, 013, 026, 066, 011 | ALT-001, 007, 011, 004 | 11, 7, 8, 4, 12 |
| DC-D-007 Change frequency | Periodic–frequent, business-initiated | Continuous + several makers → isolation is structural | **[`—`]** | AP-D-042, 041, 043 | ALT-004, 005 | 8, 2, 9, 11 |
| DC-D-008 Process value vs TCO | Value clearly exceeds full TCO | Marginal → reduce scope or defer | **[`Xe`]** **Cost exceeds value → build nothing, on any platform** | AP-D-060, 039, 061 | ALT-002, 010, 001, 003 | 10, 9, 11 |

### 2.2 Users and experience (DC-D-009 … 020)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-009 Identity class | Internal; partner guests with recognised entitlement; authenticated customers over the governed store | Public anonymous → cookie-metered capacity, single acting identity, freshness floor, mandatory permission review | **[`Xp`]** **Public anonymous + sub-freshness-floor, or third-party interface surface, or server/caching control, or unexpressible sensitivity → custom web** | AP-D-034, 032, 033 | ALT-004, 005, 003 | 2, 1, 6, 10 |
| DC-D-010 Population size | Any size where licensing shape matches usage shape | Tens of thousands + premium controls | **[`Xe`]** **Per-user/scope economics uneconomic at scale → custom application** (economic exit) | AP-D-051, 062, 064 | ALT-005, 004 | 10, 3, 9, 2, 6 |
| DC-D-011 Persona count | 1–3 overlapping personas | 2–3 divergent → partition or record-centric shell | **[`Cf`]** feeds 012 and 013 | AP-D-051, 050 | ALT-004, 005 | 2, 1 |
| DC-D-012 Interaction complexity | Form/list-shaped or moderately bespoke | Highly bespoke → coded surface or bespoke external site, both conditional pending GA check | **[`Xp`]** **Product-grade consumer experience or mandated design system on record-centric core → custom web/native** | AP-D-003, 057 | ALT-005, 008, 004 | 2, 1 |
| DC-D-013 Brand / design system | None; logo and colours | Full design system via components | **[`Xr`]** **Mandated design system on record-centric core pages → surface change or requirement change** | AP-D-003 | ALT-005, 004 | 2, 1 |
| DC-D-014 Accessibility regime | Legal obligation on platform-attested or built-in surfaces | Legal obligation on a maker-built surface → testing obligation, some patterns need code components | **[`—`]** | AP-D-052 | ALT-004, 005 | 2, 1 |
| DC-D-015 Device / form factor | Desktop, tablet, or mobile with device hardware on the task-focused surface | Mixed serving one artefact → responsive is opt-in effort | **[`Xc`]** **Shared/kiosk is UNKNOWN; combined mobile+hardware+offline+branded-push is unsatisfiable** | AP-D-003 | ALT-004, 005 | 2, 1, 9 |
| DC-D-016 Offline requirement | Offline read/write on the native client over the governed store, within its list | Offline + field-level security → mutually exclusive | **[`Xp`]** **Offline in a browser; offline over non-governed data beyond bound; custom conflict rules → custom application** | AP-D-003, 012 | ALT-005, 004 | 2, 1, 3 |
| DC-D-017 Language / script | Single to 2–3 on any surface; many on record-centric or templated external | Many on the task-focused surface → multiplicative labour | **[`—`]** (right-to-left on standalone task-focused is UNKNOWN, close by prototype) | AP-D-051 | ALT-004, 005 | 2, 1 |
| DC-D-018 Freshness at the surface | Eventual or minutes; immediate within the user's own transaction | Derived values from background automation → never guaranteed immediate | **[`Xr`]** **Sub-15-minute freshness on the external-site read surface for changes made elsewhere → different read surface or custom web** | AP-D-024, 012, 009 | ALT-005, 006, 009 | 9, 2, 3, 5, 4 |
| DC-D-019 Navigation / deep links | Either shape matched to the right surface | Many linkable destinations on a task-focused surface | **[`—`]** | AP-D-058 | ALT-004 | 2 |
| DC-D-020 Native distribution / push | Browser or standard client; branded distribution without push, internal/partner | Wrapping mechanism → monthly re-wrap operations, sovereign exclusion, audience limits | **[`Xp`]** **Branded distribution with push, or consumer app store → custom native** | AP-D-003 | ALT-005, 009 | 2, 1 |

**Added 2026-09-03 — the conversational/agentic row.** DC-D-116 belongs to this domain; it is numbered at the end of the namespace because Block D's ids are already cited from three peer files (`decision-criteria.md` §3).

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-116 Conversational / agentic requirement | `NONE` — the criterion is inert, which is the common case | Assisted search and summary over already-governed content, **internal audience**, with the governance obligations funded | **[`—`]** none evidenced — **and the absence is the finding.** No fit assessment of this surface exists in any canonical file. At `TASK-COMPLETING AGENT` and above the correct output is **`DECISION BLOCKED`** on the commercial model (consumption *"dependent on the complexity of the task"*), on the governance model (agent rules *"evolving"*; authentication/channels preview and unresearched) and, at `AUTONOMOUS AGENT`, on the modality question itself (an **unowned** deferral) | AP-D-068, 033, 030, 057, 051, 062 | **none evaluable** — `UNKNOWN` in every class including ALT-004 | 7, 6, 8, 11, 10 |

### 2.3 Data (DC-D-021 … 034)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-021 System of record | This solution owns the entity | Split by field → ownership matrix, conflict rules, reconciliation, four named roles | **[`Ri`]** blocks the bidirectional-mastering **pattern** for critical data (NB-01); the answer is read-through, a one-way replica, or single-writer-per-phase | AP-D-014, 010, 011, 013, 027 | ALT-001, 007, 009, 011 | 3, 5, 12, 7 |
| DC-D-022 Relational complexity | Relational with integrity on the governed store | Deep traversal → server-side views or flattened model; stricter offline | **[`Cf`]** feeds 023 and 088 — disqualifies specific stores, never the platform | AP-D-008, 012, 050 | ALT-003, 004, 005 | 3, 9, 1 |
| DC-D-023 Queried volume per path | Below ceiling, or above and fully delegable | Partially delegable; growth approaching the ceiling with search | **[`Xr`]** **Non-delegable at volume with no server-side shaping → surface/store change; at the extreme, custom** | AP-D-050, 008, 012 | ALT-003, 004, 005, 009 | 9, 3, 1 |
| DC-D-024 Volume and growth | Small–large with a funded capacity model and lifecycle jobs | Very large / high growth → no published envelope, needs load and soak validation | **[`Cf`]** feeds 031 and 040 | AP-D-063, 051, 010 | ALT-006, 009, 004 | 9, 3, 10, 11 |
| DC-D-025 Attachment volume | Low–moderate on the cheap file meter | High or large files with a low-profile owner → content-throughput meter binds | **[`Ri`]** binaries leave the database meter for file storage or the document store with a reference — a store change, not a platform change | AP-D-063, 049, 066 | ALT-003, 006, 009 | 3, 9, 10 |
| DC-D-026 Access granularity | Record and field scoping on the governed store | Field security + offline (exclusive); + analytical copy (secured columns null); authorization-heavy → NB-04 pilot | **[`Xr`]** **Administrator-excluded → the attribute leaves the governed store** | AP-D-029, 030, 012, 008, 032 | ALT-004, 005, 001, 007 | 6, 3, 12, 9 |
| DC-D-027 Audit / evidence | Change history with a scoped funded retention | Access history (licence-gated); compliance-grade → separate store, retention, budget | **[`Cf`]** feeds 062 | AP-D-063, 054, 008 | ALT-004, 001, 007 | 3, 11, 10, 6 |
| DC-D-028 Atomicity span | Single write; multi-write in one store | Multi-store with an accepted compensation window → saga with durable in-doubt state | **[`Xr`]** **Multi-system with no acceptable compensation window → collapse to one owner or leave the platform** | AP-D-018, 017, 059, 003 | ALT-005, 006, 007, 009 | 3, 1, 5, 4, 12 |
| DC-D-029 Consistency class | Eventual, either width, with reconciliation | Read-your-writes across sessions → UNKNOWN, close by test | **[`Xr`]** **Strict across ≥ 2 systems → single transactional owner or an external coordinator** | AP-D-011, 013, 018 | ALT-005, 006, 007, 009 | 3, 5, 12 |
| DC-D-030 Concurrent edit | None or rare on any store; routine on the governed store with a designed conflict experience | Routine on a relational engine via connector → semantics UNKNOWN, test | **[`Ri`]** routine or high contention disqualifies the spreadsheet and document/list store as system of record → the governed store with an explicit concurrency design | AP-D-008, 017 | ALT-003, 004, 005 | 3, 1 |
| DC-D-031 Analytical separation | Operational only; filtered reports; per-user-secured direct query | Aggregation and trends → analytical copy from day one, budgeted, secured, ≤ 1 h freshness, outside regional failover | **[`Xr`]** **Enterprise analytics as the primary requirement → a data platform owns it; high-ingest events → purpose-built engine** | AP-D-009, 013, 010, 049 | ALT-006, 007, 009 | 3, 9, 11, 5 |
| DC-D-032 Retention / archival | Short; multi-year producible-only with an archival path | Multi-year queryable → archival store; read limits are an open unknown | **[`Xr`]** multi-year queryable at volume → the **archival responsibility** leaves to a lake or archive store; in-platform long-term retention is conditional only and backups are not retention | AP-D-054, 063, 067 | ALT-006, 009 | 3, 11, 10 |
| DC-D-033 Data residency | No constraint; macro-region already satisfied | Sovereign → parity exceptions enumerated; country-level → population-priced add-on | **[`Xp`]** **No cloud transit at all → out of the platform; in-country on-premises → see 108** | AP-D-035, 057, 054 | ALT-005, 007, 008 | 3, 1, 6, 5, 9, 11 |
| DC-D-034 Migration scope | None to master + open transactions with a bulk mechanism | Including history → capacity, throughput, separate toolchain | **[`—`]** | AP-D-010, 016, 051, 063 | ALT-006, 009 | 3, 10, 1 |

### 2.4 Integration (DC-D-035 … 047)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-035 Stream / system count | 1–5 streams, stable contracts, inside throttles | Many streams and systems without a topology decision | **[`Cf`]** feeds 036 and 047 | AP-D-022, 028, 027 | ALT-007, 006, 009 | 5, 12 |
| DC-D-036 Integration ownership | No existing capability; bounded streams served directly | Capability exists without a contract → negotiate or record the failure per requirement | **[`Xr`]** **Capability exists with a published contract → the platform is not the integration layer** (NB-06: pattern is INF) | AP-D-027, 022, 025, 026 | ALT-007, 006, 009 | 5, 7, 4, 12 |
| DC-D-037 Frequency / peak shape | Steady or predictable peaks inside per-window ceilings | Spiky → brokered load levelling with bounded consumers | **[`Xc`]** §3 row 5 — high-frequency custom-connector sizing on either side of the open conflict, with 039 and 040 | AP-D-049, 016, 005 | ALT-006, 009 | 5, 9, 4 |
| DC-D-038 Directionality | Platform initiates over a reachable endpoint | External initiates → inbound endpoint + application identity; inbound private path UNKNOWN | **[`Cf`]** feeds 044 | AP-D-011, 035 | ALT-006, 007, 009 | 5, 12 |
| DC-D-039 Per-mechanism throughput | Well inside on standard mechanisms with horizon headroom | Approaching → partition across connections/identities, or exempt in-platform path | **[`Xr`]** **Exceeds with no partitioning → the responsibility leaves the platform**. `CONFLICTED` by 20× (NB-02) is **decision-blocking** | AP-D-049, 051, 025, 016 | ALT-006, 007, 009 | 5, 9, 3 |
| DC-D-040 Sustained throughput | Inside envelope at horizon, or delegable to a bulk mechanism | Exceeds but partitionable → identity distribution with its management cost | **[`Xr`]** **Exceeds and not partitionable → broker plus workers takes the volume** | AP-D-016, 049, 048, 021 | ALT-006, 007, 009 | 5, 9, 4, 1 |
| DC-D-041 Delivery guarantee / ordering | Best effort; at-least-once with tolerable duplicates | At-least-once needing idempotency → alternate key + upsert, if a stable key exists | **[`Xr`]** **Ordered at volume, effectively-once, replay, or poison-message quarantine → the guarantee moves to a transport** | AP-D-015, 017, 018, 021 | ALT-006, 009, 007 | 5, 4, 9, 12 |
| DC-D-042 Latency class | Eventual, near-real-time, interactive single-hop | Interactive across hops or a customer-operated participant | **[`Xp`]** **Strict low-latency, transactionally visible, end to end → out of the platform** | AP-D-019, 048, 003 | ALT-005, 006, 009 | 5, 9, 4, 1 |
| DC-D-043 Payload size / type | Small–moderate with mechanism headroom | Designs at the gateway margin (two conflicting figures; read the lower) | **[`Xr`]** **On-premises payload above the gateway ceiling → in-network component or boundary** | AP-D-049, 035 | ALT-006, 007, 009 | 5, 4, 3, 12 |
| DC-D-044 Network boundary | Public endpoints; on-premises within payload ceilings on a funded owned gateway estate | Private endpoint → subscription dependency, region pinning, immutable network, premium population | **[`Xr`]** **Unreachable protocol, private CA on the path, excluded environment type, or the private-egress/eventing collision with both required → in-network component or out** | AP-D-035, 026, 019 | ALT-006, 007, 005, 009 | 5, 3, 6, 12, 10 |
| DC-D-045 Interface / protocol | Modern interface with a stable contract | Database-level only → schema audit | **[`Xr`]** **Trading-partner protocols → integration platform; unsupported legacy protocol → mediation; no interface + high volume → build it or move** | AP-D-020, 025, 035 | ALT-006, 007, 005 | 5, 3, 4, 12, 1 |
| DC-D-046 Contract volatility | Stable with a single consumer | Periodic change on a critical path → named owner both sides | **[`Ri`]** frequent change or several consumers → a mediation tier with versioning; the tier's location is a design choice, not a documented exit | AP-D-025, 023, 006 | ALT-006, 007, 009 | 5, 12, 8 |
| DC-D-047 Consumer count | One; two with lightweight mediation inside entitlement | Several without a topology decision | **[`Cf`]** feeds 036 — an existing boundary already provides the tier | AP-D-022, 023, 005 | ALT-006, 007, 009 | 5, 12 |

### 2.5 Automation (DC-D-048 … 057)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-048 Automation shape | Bounded run; any shape with the platform as front door | Mixed → legitimately more than one mechanism | **[`Cf`]** shape selects the family; the ceilings (049, 050, 057) produce the exits | AP-D-015, 016, 018 | ALT-004, 006, 009 | 4, 9, 5 |
| DC-D-049 Process duration | Minutes to 30 days with the human-wait ceiling designed for | Near 30 days → the approval timeout is silent | **[`Ri`]** Beyond 30 days as a single run → the run mechanism itself becomes unavailable; the documented answer is a **business record with a re-triggering automation**, in-platform — a durable orchestrator is a design option for the same redirect, not a documented exit (Repair V3: corrected from `Xr`, which named nothing leaving the platform) | AP-D-015, 021 | ALT-006, 009 | 4, 9, 1 |
| DC-D-050 Synchronous response | None, or within the platform window | An automation as a command channel for short operations | **[`Xr`]** **Strict sub-second at user-facing volume → server-side platform code or a service outside** | AP-D-019, 016, 015 | ALT-005, 006, 009 | 4, 9, 1, 12 |
| DC-D-051 Event floor / freshness | Hourly to minutes with a trigger predicate | Any figure derived from a per-connector interval (open unknown) | **[`Xr`]** **Continuous stream → a streaming service; sub-minute with no push on the source → broker or synchronous call** | AP-D-024, 051, 063 | ALT-006, 009 | 4, 9, 3, 5 |
| DC-D-052 Idempotency key | Stable key exists, or can be created | Any at-least-once path without a key (symmetric across platforms) | **[`—`]** (blocks **retry**, and therefore any at-least-once design) | AP-D-017, 011, 013, 018 | ALT-006, 009 | 4, 3, 5, 9 |
| DC-D-053 Concurrency / ordering | Order irrelevant or preferred, with in-run concurrency set deliberately | Order required at low volume → irreversible setting, isolate it | **[`Xr`]** (order at volume → transport; see 041) | AP-D-015, 049, 016 | ALT-006, 009 | 4, 9, 5 |
| DC-D-054 Failure semantics | Tolerant; compensation defined with idempotent steps | In-doubt state required → persisted marker, human path, named owner | **[`Xr`]** **Must not partially complete across systems → out of the platform for the coordination** | AP-D-018, 017, 021, 011 | ALT-005, 006, 007, 009 | 4, 5, 3, 6, 8 |
| DC-D-055 Human in the loop | Simple to delegated/escalated approval within 30 days — **the platform's strongest documented differentiator here** | Escalation and reassignment mechanics are an open unknown | **[`—`]** | AP-D-015 | ALT-004, 007 | 4, 1, 2 |
| DC-D-056 Unattended UI automation | Attended, on an interface-only target with a person present | Unattended low concurrency → cost multiplier, logging ceiling, selector owner | **[`Xr`]** (the exit is **from this mechanism** to the target's interface) | AP-D-020, 021 | ALT-005, 006, 001 | 4, 10, 1, 12 |
| DC-D-057 Compute intensity | Orchestration only; light calculation | Light calculation growing → same signal as approaching the action ceiling | **[`Xr`]** **Significant or specialised compute → out of the platform for that step, evaluated first** | AP-D-003, 015, 026 | ALT-005, 006, 009 | 9, 4, 1 |

### 2.6 Security (DC-D-058 … 068)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-058 Sensitivity | Internal, confidential with record and field scoping | Highly restricted → verify each mandated control against the exclusion lists | **[`Cf`]** feeds 062 and 092 | AP-D-029, 030, 033, 034, 064 | ALT-001, 003, 005, 007 | 6, 3, 10 |
| DC-D-059 Regulatory regime | Internal policy or sector regulation mapping onto available features with a funded population | Regulated with external audit → assurance artefact constructed, no preview on the path | **[`Xp`]** **Administrator-excluded confidentiality; datacentre disclosure; a mandated control with no implementation → out** | AP-D-033, 057, 029, 064 | ALT-005, 007, 001, 011 | 6, 1, 3, 11, 7 |
| DC-D-060 Authentication model | Directory only, or directory with conditional access | Federated / multiple providers; frontline and shared-device is an open unknown | **[`—`]** | AP-D-032, 033 | ALT-004, 005 | 6, 5, 1 |
| DC-D-061 External identity | Partner guests with recognised entitlement; authenticated customers with a reviewed permission model | Public anonymous (see 009) | **[`Cf`]** feeds 009 | AP-D-034, 033, 058 | ALT-004, 005 | 6, 2, 1, 10 |
| DC-D-062 Privileged access | None, or governed privileged access | Just-in-time only → evidence it rather than assert it | **[`Xr`]** **Administrator exclusion required → the attribute leaves the governed store** | AP-D-029, 032, 030 | ALT-005, 001, 007 | 6, 3 |
| DC-D-063 Network isolation mandate | None or preferred | Mandated → managed class, licence population, identity allowlist, audit-mode rollout | **[`Xc`]** **Mandate whose licence population is unfunded → security requirement and commercial constraint are incompatible** | AP-D-033, 035, 064, 059 | ALT-005, 006, 007, 008 | 6, 3, 5, 10, 12 |
| DC-D-064 Key control | Platform-managed acceptable | Customer-managed → entitlement population, exclusion list, **audit conflict**, revocation-as-outage, key store as tier-zero | **[`Xc`]** (key control **and** audit both mandated can eliminate the option) | AP-D-064, 033, 035 | ALT-003, 005, 007 | 6, 3, 10 |
| DC-D-065 Secrets lifecycle | None required, or secrets in the three supported component types | Run-history exposure where a secret sits in an action input | **[`Xr`]** **No stored secrets mandated on an unsupported surface → server-side code with managed identity, or a worker outside** | AP-D-031, 032, 044 | ALT-005, 006, 009 | 6, 4, 5, 7, 12 |
| DC-D-066 Revocation immediacy | Next day or within hours | Immediate → continuous evaluation plus group-driven assignment, residual stated | **[`—`]** | AP-D-032, 036 | ALT-004 | 6, 5, 4 |
| DC-D-067 Egress control | None or detective; preventive within the allowlist's documented coverage | Custom or interface connectors in scope of a preventive claim (coverage gap) | **[`Xp`]** **Strict exfiltration prevention → not evidenced as achievable; treat as blocked, not met** | AP-D-033, 038, 030 | ALT-001, 007, 005 | 6, 7, 1, 5 |
| DC-D-068 Authorization enforcement point | Platform enforces on the governed store; target enforces with explicit identity | Both enforce → two models to keep aligned | **[`Xc`]** none from this criterion alone. Per-user target authorization **through a shared-identity intermediary** combines into a **registered** disqualifier via DC-D-036 and DC-D-060 (§3 row 6) unless identity is propagated or compensating authorization is implemented (Repair V3: corrected from `Xr` — no off-platform destination is named anywhere in this criterion) | AP-D-030, 032, 012, 059 | ALT-001, 006, 007 | 6, 3, 5, 12 |

### 2.7 Governance (DC-D-069 … 075) — no exit signals evidenced

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-069 Maker / delivery model | Central delivery, fusion with real capacity, governed citizen development | Ungoverned → build the governance package first | **[`—`]** | AP-D-036, 037, 039, 040 | ALT-004, 011 | 7, 1, 8 |
| DC-D-070 Governance maturity | Established for this platform — **a genuine reason to prefer it over a hybrid** | Emerging with a hybrid in the design | **[`—`]** (**blocks hybrid and boundary options**: unavailable, not expensive) | AP-D-026, 046, 059, 058 | ALT-004, 006, 007, 009, 011 | 7, 12, 4, 11, 8 |
| DC-D-071 Environment strategy | Dev/test/prod with development on developer-plan environments | Complex estate → four cost axes compound, no group exceptions | **[`—`]** | AP-D-037, 040, 038 | ALT-004 | 7, 10, 6, 8, 11 |
| DC-D-072 Connector permissibility | Permissive or restrictive-with-exceptions where the required set is permitted | No policy → permissive start is a gap, not a green light | **[`—`]** | AP-D-038, 033, 035 | ALT-006, 007 | 7, 1, 6, 5 |
| DC-D-073 Support ownership | Service desk first line or better, tier matched to criticality | Informal for anything business-critical | **[`—`]** (no capability → vendor-operated or incumbent-owned classes) | AP-D-053, 056, 036, 041 | ALT-001, 007, 011, 004 | 11, 7, 10, 8, 6 |
| DC-D-074 Solution scope | Any scope matched to its environment class and obligations | Single team with a growth path and no graduation trigger | **[`—`]** | AP-D-065, 036, 039, 047 | ALT-003, 004 | 7, 10, 11, 3, 2 |
| DC-D-075 Retirement accountability | Process defined, ideally exercised | Not considered → cost appears as capacity blocking recovery | **[`—`]** | AP-D-067, 063, 054 | ALT-010, 004 | 11, 7, 3, 8 |

### 2.8 ALM and delivery (DC-D-076 … 083) — no exit signals evidenced

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-076 Source control | Not required or desirable for a single-maker departmental solution | Required for review → repository, per-maker environments, pro-code capability | **[`—`]** | AP-D-042, 043, 041 | ALT-004, 005 | 8, 2, 1 |
| DC-D-077 Release frequency / window | Infrequent to periodic with a defined window | Continuous delivery expected → deployment is itself a performance event | **[`—`]** | AP-D-045, 043, 041 | ALT-004, 005 | 9, 11, 8 |
| DC-D-078 Team size | Single maker, or two on separate artefacts | Small team on shared artefacts → structural isolation gap, manual retrofit | **[`—`]** | AP-D-042, 041 | ALT-004, 005 | 8, 2, 1 |
| DC-D-079 Separation of duties | Not required; approval required | Separation mandated → deploying identity becomes a privileged owned asset | **[`—`]** | AP-D-043, 041, 032 | ALT-004 | 8, 6, 7 |
| DC-D-080 Reversibility | Fix forward; previous-version redeploy enabled and tested | Full restore required → extensive side effects, day-scale unknown duration | **[`Xc`]** §3 row 4 — critical workload + no representative managed test environment + no recovery drill; the unrehearsed claim is the *no drill* leg | AP-D-045, 054, 052 | ALT-004, 005 | 8, 11, 3 |
| DC-D-081 Automated testing | None or manual acceptance for the departmental class | Automated regression → pro-code harness budgeted, or manual with a stated regression risk | **[`—`]** (symmetric: a custom stack builds its own harness too) | AP-D-052, 048 | ALT-004, 005 | 8, 1, 4, 9 |
| DC-D-082 Environment count | Dev/test/prod with development on developer-plan environments | Per-maker or multi-stage → cost axes compound; promotion targets must be managed | **[`—`]** | AP-D-037, 040, 041, 052 | ALT-004 | 8, 10, 7, 11 |
| DC-D-083 Cross-boundary deployment | Single platform; two platforms independent and compatible by design | Two platforms coordinated → declared sequencing and compatibility policy | **[`—`]** (**gates hybrid options**: no coordination → unavailable) | AP-D-046, 025, 026, 044 | ALT-006, 009, 007 | 8, 12, 5, 7 |

### 2.9 Performance and scale (DC-D-084 … 091)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-084 Response time | Tolerant or responsive with delegable paths | High-latency or mobile populations → test on target devices; mobile concurrency unpublished | **[`Xp`]** **Hard sub-second transactionally-visible end-to-end → out of the platform** | AP-D-048, 019, 050, 003 | ALT-005, 006, 009 | 9, 4, 1 |
| DC-D-085 User concurrency | Tens to hundreds with delegable paths and distributed identities | Thousands+, or traffic concentrated on one acting identity | **[`Cf`]** **no published ceiling anywhere**; feeds 089 — the exit is 089 (proof required but not obtainable), never a concurrency number | AP-D-051, 048, 052, 040 | ALT-005, 006, 009 | 9, 3, 2 |
| DC-D-086 Request rate per identity | Well inside with a **measured** amplification factor | Single-identity concentration → one identity is one budget | **[`Cf`]** feeds 040 | AP-D-049, 051, 016, 055 | ALT-006, 009 | 9, 3, 4, 10 |
| DC-D-087 Peak / growth horizon | Flat or predictable peaks inside the envelope at horizon | High growth → the reachable limit is likely crossed inside the horizon | **[`Cf`]** moves 040 and 023 across their thresholds | AP-D-049, 063, 006 | ALT-006, 009 | 9, 10, 5 |
| DC-D-088 Records per access path | Shallow and small; shallow and large with delegable paths | Deep anywhere; any path without an indexable selective filter on the document store | **[`Ri`]** deep traversal → server-side views, a flattened model or a different surface; a store, model or surface change, not a platform change | AP-D-050, 008 | ALT-003, 004, 005 | 9, 3 |
| DC-D-089 Provability of capacity | Not required; limit arithmetic suffices; bounded pilot with a representative environment | Bounded pilot without a managed test environment when production is managed | **[`Xr`]** **Full load proof required where testing against the service is constrained → host the peak-bearing component elsewhere** | AP-D-048, 052, 051, 040, 059 | ALT-005, 006, 009 | 9, 8, 11, 12 |
| DC-D-090 In-region availability | Best effort or 99.9% on a production environment type | Above 99.9% → no platform commitment exists above it | **[`Cf`]** feeds 091 and 100 | AP-D-040, 056, 054 | ALT-004, 005, 006 | 9, 1, 11, 6 |
| DC-D-091 End-to-end availability | No commitment; internal target; contractual with platform-only dependencies and parsed terms | Every additional synchronous hop or operated component lowers the composite | **[`Xp`]** **A contractual commitment the composite path cannot support → an architecture whose availability the customer controls, or the commitment changes** | AP-D-056, 019, 026, 054 | ALT-005, 006, 007, 009 | 9, 11, 5, 12, 6 |

### 2.10 Cost (DC-D-092 … 099)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-092 Budget envelope | Defined and adequate inside existing entitlement | Tight with a criticality class that pulls the managed-environment chain | **[`Xe`]** **Inadequate for mandated controls or the required audience → the option is infeasible** | AP-D-060, 061, 064, 039 | ALT-002, 010, 001, 003 | 10, 12, 6, 7 |
| DC-D-093 Entitlement fit | Inside existing entitlement, **verified** | Premium for the whole audience → a step change, the commonest late discovery | **[`Xe`]** **Premium plus external prerequisites across an unfunded population → economically infeasible** (with 092) | AP-D-062, 061, 064, 060 | ALT-003, 004, 005, 008 | 10, 1, 7, 6 |
| DC-D-094 Audience / frequency shape | Small+high-frequency on prepaid; large+low-frequency on consumption | Unpredictable or external → the meter's unit is not a person | **[`—`]** (input to the economic comparison) | AP-D-060, 063, 062 | ALT-005, 006, 008, 004 | 10 |
| DC-D-095 Capacity profile | Well within, with a funded model and lifecycle jobs | Approaching thresholds → administrative operations degrade before anything user-visible | **[`—`]** | AP-D-063, 054, 037, 009 | ALT-003, 006, 009 | 10, 11, 3 |
| DC-D-096 External service cost | None — a single-platform option | Material → the corpus can name these lines but not price them | **[`—`]** (can make a hybrid uneconomic, a different finding) | AP-D-060, 026, 046 | ALT-006, 009, 005 | 10, 4, 9, 12, 5 |
| DC-D-097 Operational / support tier | Basic for a departmental workload | Business-critical tier → the managed-environment step change | **[`Xe`]** **Criticality requiring a tier the budget cannot fund → economically unattractive; avoiding it forfeits diagnosis and recovery** | AP-D-060, 061, 064, 053 | ALT-011, 001, 010, 004 | 10, 11, 9 |
| DC-D-098 Migration / exit cost | Low both ways | Exit-heavy where portability matters but is unpriced | **[`Cf`]** feeds 105 and 106 | AP-D-065, 060, 058 | ALT-005, 008, 011 | 10, 1, 3, 2 |
| DC-D-099 Cost attribution | Not required; showback | Chargeback by business unit → couples finance to environment design | **[`—`]** (per-project chargeback of shared pools is an unmet requirement to record) | AP-D-063, 037 | ALT-004, 006 | 10, 11, 7 |

### 2.11 Operations (DC-D-100 … 104)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-100 Recovery objectives | Best effort; in-region only on a production environment type | Cross-region without a committed time → joint architecture/licensing/region decision, storage doubling, automation degradation | **[`Xp`]** **A contractual cross-region recovery time → no platform commitment exists; drill evidence the customer owns, or an architecture whose recovery time the customer controls** | AP-D-054, 056, 045, 047, 040 | ALT-005, 006, 007, 009 | 11, 9, 10, 8 |
| DC-D-101 Observability depth | Native surfaces for the departmental class | Telemetry export → managed environment, premium population, lossy by the vendor's statement | **[`Xr`]** **Complete, real-time, long-retention message-level observability → a durable log outside the platform** | AP-D-021, 053, 061, 064 | ALT-006, 007, 009 | 11, 4, 5, 10, 9 |
| DC-D-102 Incident response / support | Business hours with an internal first line | 24×7 with defined response → the vendor's contribution is bounded | **[`—`]** (no internal capability → vendor-operated or incumbent classes) | AP-D-056, 053, 057 | ALT-011, 001, 007, 004 | 11, 10, 9 |
| DC-D-103 Evidence retention | None or 30 days operational | Beyond 30 days → the design changes, not a setting | **[`Xr`]** **Complete long-retention message-level evidence → a durable log outside the platform** | AP-D-021, 063, 054 | ALT-006, 007, 009 | 11, 3, 10, 5, 4 |
| DC-D-104 Operational maturity | A class match at any level, including departmental | A one-class gap → closable with a funded plan | **[`Xc`]** (a two-class gap with no plan → the commitment cannot be delivered; external-component options **unavailable**) | AP-D-053, 054, 026, 039, 059 | ALT-011, 001, 007, 010, 004 | 11, 12, 7, 10 |

### 2.12 Strategic and platform (DC-D-105 … 115)

| Criterion | Positive PP signal | Conditional / hybrid signal | Negative / exit signal | Anti-patterns | Alternatives | Evidence |
|---|---|---|---|---|---|---|
| DC-D-105 Lock-in / portability | Lock-in accepted; data portability required | Application-layer portability → the interface, expression logic and automations are a rewrite | **[`Xp`]** **Full portability required → a conventional stack** (ALT-008 is a candidate; comparator portability is UNKNOWN) | AP-D-002, 003 | ALT-005, 008, 007 | 1, 10 |
| DC-D-106 Exit strategy | Not required | Documented plan required → enumerate per layer and price it | **[`Xp`]** **Tested exit required → no mechanism evidenced; descope or choose a conventional stack** | AP-D-065, 060 | ALT-005, 008, 011 | 1, 10, 3, 2 |
| DC-D-107 Change-cadence tolerance | Tolerant; managed with testing | Change control required → revalidation per wave, least-exposed surface, remediation budget | **[`Xp`]** **Behaviour must be frozen → a self-managed stack whose upgrade schedule the organisation controls** | AP-D-058, 057, 052 | ALT-005, 008, 001 | 1, 11, 10, 2 |
| DC-D-108 Deployment model | Vendor-operated service acceptable | A requirement stated as "on-premises" that is really residency or network reach — clarify | **[`Xp`]** **Customer cloud subscription, customer data centre, or air-gapped → documented exits** | AP-D-035, 003, 057 | ALT-005, 008, 007, 001 | 1, 5, 3 + V-D-01/V-D-04 |
| DC-D-109 Existing productivity estate | Productivity plus some premium, where the requirement fits inside it | Extensive including business applications → the overlap check is mandatory | **[`—`]** (makes other classes more attractive rather than disqualifying) | AP-D-007, 062, 004 | ALT-003, 011, 001, 004 | 1, 2, 10, 3 |
| DC-D-110 Team skills | Low-code only, or plus some pro-code, for in-platform options — **a genuine reason to prefer the platform** | Partner-dependent for a long-lived solution | **[`—`]** (**gates hybrid and custom options**; symmetrically, full engineering capability makes ALT-005/006 cheaper) | AP-D-002, 026, 046, 059 | ALT-004, 005, 006, 009, 011 | 1, 12, 4, 11, 8 |
| DC-D-111 Enterprise platform estate | None — a genuinely greenfield integration position | A boundary exists and has not been consulted | **[`—`]** (redirects **specific responsibilities**, not the whole solution) | AP-D-027, 022, 002, 007 | ALT-007, 001, 011, 009 | 5, 7, 4, 12 |
| DC-D-112 Change-tracking ownership | Named owner with a recurring budget | No owner for a solution living beyond a year | **[`Cf`]** feeds 107 | AP-D-058, 057, 006 | ALT-011, 001, 004 | 11, 10, 7, 8, 2 |
| DC-D-113 Multi-tenancy / resale | Single tenant | Multi-tenant internal → the source-controlled rung's prerequisites | **[`—`]** (**resale is decision-blocking on the commercial model**: no evidence exists in the corpus) | AP-D-042, 062 | ALT-005, 011 | 8, 1, 10 |
| DC-D-114 Sourcing / delivery model | Internal build and run, capability matched to criticality | Partner build with internal run → the corpus's named undocumented failure point | **[`—`]** | AP-D-053, 026, 036, 047 | ALT-011, 001, 007, 004 | 11, 12, 1, 6 |
| DC-D-115 Roadmap / preview dependency | No preview dependency | Preview on a non-critical path with a re-verification date | **[`—`]** (preview on a critical path is **blocking** until re-verified or descoped) | AP-D-057, 055, 058 | ALT-011, 005, 010 | 11, 2, 6, 10, 3, 1 |

---
## 3. Composed disqualifiers — the matrix's most important rows

These are not criteria. They are **combinations** in which every individual criterion reads `CONDITIONAL` and the combination is worse than any of its parts. They come from `architecture-patterns.md` §13 and are the reason §5's evaluation order is not commutative and §2 is not a lookup table.

| # | Combination | Criteria involved | Consequence | Class | §6.2 outcome |
|---|---|---|---|---|---|
| 1 | Strict cross-system atomicity + more than one transactional owner + no acceptable compensation window | DC-D-028, 029, 021 | No pattern supplies the atomicity | POOR FIT | **5** |
| 2 | A pattern requiring an external component + no named operator, on-call or release owner | DC-D-070, 073, 083, 104, 110 | **Pattern unavailable, not merely expensive** | ANTI-PATTERN (AP-D-026) | **5** |
| 3 | Private-network / key-control / firewall requirement + unfunded licence population | DC-D-063, 064, 092, 093 | Security requirement and commercial constraint are **incompatible** | CONSTRAINT | **7** — the mandated control is unfunded, which is class 7's own trigger (*"infeasible where a mandated control is unfunded"*); this is an economic finding, not a capability one, and never implies a cheaper alternative |
| 4 | Business- or mission-critical + no representative managed test environment + no recovery drill | DC-D-001, 080, 082, 089, 100 | Production commitment **cannot be evidenced** | RISK (AP-D-052) | **12** — DC-D-001, 080, 089 and 100 are all in `decision-criteria.md` §5.2's blocking set; an unevidenced criticality commitment is a validation gap on those criteria, not a platform-capability finding, so the correct output names the drill as the evidence task, never an exclusion |
| 5 | High-frequency custom-connector workload + sizing on either side of the open conflict, unmeasured | DC-D-039, 040, 037 | Sizing is **decision-blocking** | VOLATILE / CONFLICTED | **12** — DC-D-039 is itself `CONFLICTED` and `B` (§5.2); the row cannot resolve until the figure is re-read and the workload measured |
| 6 | Per-user backend authorization + a facade or worker calling downstream as a shared identity | DC-D-068, 036, 060 | Pattern **changes the authorization semantics** | DECISION CRITERION | **2** where identity is propagated through the intermediary or compensating authorization is implemented (the named condition); **12** where propagation feasibility is `UNKNOWN`. **Never 5, 6 or 7** — no off-platform destination is named by any criterion in this row (Repair V3; this is the row DC-D-068 registers into as `Xc`) |
| 7 | Hybrid required + no pro-code or enterprise-platform capability | DC-D-110, 070, 057 | Platform-only implementation is the wrong fit | POOR FIT | **5** |
| 8 | Replication + no reconciliation owner + a recovery/restore requirement | DC-D-021, 006, 100, 029 | A routine restore creates **unowned data divergence** | ANTI-PATTERN (AP-D-013) | **5** |

**Four further combinations Block D adds**, derived from the same evidence but not enumerated in `architecture-patterns.md` §13. **The register is 8 + 4 = 12, and `anti-patterns.md` AP-D-059 and `decision-criteria.md` §2.4 now carry the same 12** — previously this section carried 10 while AP-D-059 carried 8, so a pack generated from `anti-patterns.md` alone lost Block D's additions:

| # | Combination | Criteria | Consequence | Class | §6.2 outcome |
|---|---|---|---|---|---|
| 9 | Criticality class two or more levels above the demonstrated operating maturity, with no funded plan | DC-D-001 vs DC-D-104 | The commitment cannot be delivered in any architecture; the gap is a sponsor decision, not a design one (AP-D-053, AP-D-054) | SPONSOR DECISION | **11** where the maturity plan is genuinely unfunded (class 11's own trigger names *"a required control unfunded"*), or **12** where the plan itself is undetermined rather than refused. **Never a Power Platform exclusion class (5, 6, 7)** — the gap recurs on every platform, so naming Power Platform would misattribute a sponsor-side finding as a capability one (Repair V3, closing `block-d-gate.md` finding G-M-02: this row previously had no Class column at all) |
| 10 | Offline write + field-level security, **or** offline + non-governed data beyond the bound, **or** mobile-first + device hardware + branded distribution with push | DC-D-016, 026, 015, 020 | Each is a documented mutual exclusion; the combination is unsatisfiable in-platform (AP-D-003) | ANTI-PATTERN | **5** |
| 11 | **Citizen-built artefacts outside a solution, in the default environment + criticality now business-critical or above + the original maker gone** | DC-D-006, 001, 074, 093 | The workload **cannot be brought to the required class in place**: non-solution artefacts are excluded from backup, ineligible for capacity licences and undeployable; a non-solution automation's **owner cannot be changed at all**; the departed maker's profile has already reverted. The outcome is **migration, not remediation** (AP-D-036, AP-D-040, AP-D-047, AP-D-066) | MIGRATION | **14** |
| 12 | **Continuous change + two or more concurrent makers + no pro-code capacity to reach the source-controlled rung** | DC-D-007, 078, 110, 081 | No isolation mechanism is available at any reachable rung — *"Every modification is applied directly to the environment"*, co-authoring removed, and the isolating rung needs pro-dev capability DC-D-110 gates. **Overwriting is the documented outcome**, with no supported first-party functional-test framework to catch it (AP-D-042, AP-D-041, AP-D-043) | ANTI-PATTERN | **5** |

**Why the last two matter disproportionately.** They are the only composed rows drawn from **Governance** and **ALM** — the two domains producing **zero direct exit signals**. Before this repair, a domain that could not reject the platform on any single criterion was also contributing nothing to the one test designed to catch precisely that, so its combinations were invisible to the whole model. T-10 previously reached the right answer by conjoining four separately-detected anti-patterns, which is exactly the reasoning AP-D-059 exists to formalise.

**Registration rule (added 2026-09-03; extended 2026-09-03 — Repair V3).** A criterion may carry `decision-criteria.md` §2.5's **`Xc`** class **only if it is named in the Criteria column of a row above**. The eight that qualify are DC-D-001, 015, 037, 063, 064, 068, 080 and 104. V1 flagged twenty-four criteria `Xc` against this twelve-row register, so eighteen declared an exit that lived nowhere and Step 4 of §5 had nothing to run for them; those eighteen are now `Cf` (combination inputs, not exits). **DC-D-080 was one addition to a row's criteria list**, on row 4: reversibility is the leg the *"no recovery drill"* condition tests, and naming it changes no consequence, no class and no canonical content. **DC-D-068 is the second and most recent** (Repair V3): it was already named in row 6's Criteria column, but no criterion's own class routed to it until §2.5 moved DC-D-068 from `Xr` to `Xc` — the row was registered and unreachable at the same time, which is exactly the defect §2.5's registration requirement exists to prevent. `architecture-patterns.md` §13 carries no criteria column, so the mapping from rows to `DC-D-NNN` is Block D's own and is where both omissions sat.

**Every row now names a reachable `decision-criteria.md` §6.2 class or class pair (added 2026-09-03 — Repair V3, closing `block-d-gate.md` finding G-M-02).** `decision-criteria.md` §2.5's `Xc` → outcome mapping is *"named per registered row"*, not a single set — this table's rightmost column is that naming. No row maps to more than one class except where the row's own consequence is genuinely conditional (row 6, row 9), and in both cases the condition is stated, not left to inference. No row maps to a Power Platform exclusion class (5, 6 or 7) unless the row's consequence is an actual capability or economic finding about the platform: rows 1, 2, 7, 8 and 10 are (patterns the platform cannot supply); row 3 is economic (7, not 5); rows 4, 5 and 6's condition-unresolved branch are evidence gaps (12); row 9 is platform-independent (11 or 12); row 11 is a migration, not an exclusion (14).

**The register is not a wish list.** Adding rows to make the `Xc` flags resolve would have been the other way to close this, and it would have been invention: eighteen combinations whose conjunction the corpus never states as a disqualifier would have acquired one. The corpus registers twelve. The criteria that feed them are inputs.

---

## 4. Volatile and conflicted rows

The rows that must be re-verified rather than read. Reproduced here so a reader of the matrix alone does not miss them.

| Criterion | Status | What must happen before the row is used |
|---|---|---|
| DC-D-039 | **`CONFLICTED`** — two current pages differ by **20×** on the custom-connector ceiling (NB-02). Re-verified 2026-09-03: the limits page says 500/min/connection (dated 2026-07-17); the connector FAQ says 10,000 for this platform (dated 2025-03-13, updated 2025-09-10). | Re-read both pages **and** measure representative workload. Do not encode either figure. A documented case-by-case escalation path exists and may be proposed as a mitigation, never relied on in advance. |
| DC-D-051 | Volatile — per-licence polling intervals are an open unknown in three canonical areas | Read the specific connector's trigger reference for this engagement |
| DC-D-072 | Volatile — new connectors join the default group over time | Check the target environment's policy on the design's date |
| DC-D-086 | Volatile — published figures are **transition-period tolerances with no announced enforcement date**; amplification is never published | Design to official limits; **measure** amplification on a prototype |
| DC-D-093 | Volatile — general documentation is not authoritative on licensing; whether one premium connector obliges premium entitlement for every user of an artefact is an open item | Read the licensing guide and the customer's agreement, with a named owner |
| DC-D-094, 095, 096 | Volatile — several meters are preview; add-on assignability and analytical-replica ratios have open items | Re-verify at Options, implementation and renewal |
| DC-D-113 | Volatile and **evidentially absent** — resale and multi-tenant licensing is an unclosed deferral | Treat as decision-blocking on the commercial model |
| DC-D-115 | Volatile by definition — two facts in the corpus already changed once during its own life | Check general-availability state on the day of the decision |
| DC-D-116 | Volatile and **evidentially incomplete** — the consumption unit is not modellable in advance, one bundled entitlement has a dated removal, and agent governance and authentication/channel controls are preview | Treat as decision-blocking on the commercial and governance model; establish consumption empirically in a pilot |
| **Service-limit group** — DC-D-018, 023, 025, 026, 027, 031, 032, 040, 043, 044, 048, 049, 055, 056, 100, 101, 103 | **Added 2026-09-03.** These rows' exit and caution cells rest on a **published service limit, quota or retention window**, which manifest §5's `VOLATILE VALUE` definition covers (*"quota, limit, feature-state"*) and which this matrix previously treated as timeless. `decision-criteria.md` §7.2 carries the full register and the withdrawal of a mitigation that was claimed and never implemented | **Encode the boundary shape, not the number.** Where an engagement must test a real requirement against a figure, re-read the figure from current documentation at the decision date and record the reading with its date on the engagement's own row |

---

## 5. Evaluation order

The order is **not commutative**, and §6's tests demonstrate it. Evaluating direction before disqualification produces different — and wrong — answers.

```
STEP 0  ABSOLUTES
        DC-D-108 deployment model · DC-D-033 residency · DC-D-059 regulatory regime
        DC-D-062 administrator exclusion · DC-D-028 atomicity span · DC-D-057 compute intensity
        → any exit signal here ends the platform question for the affected scope,
          before any fit or cost analysis is worth doing.

STEP 1  DECISION-BLOCKING UNKNOWNS
        the 28 criteria of `decision-criteria.md` §5.2
        → any UNKNOWN here yields DECISION BLOCKED — MORE EVIDENCE REQUIRED,
          naming the evidence task, its owner and the outcome each resolution would produce.

STEP 2  SHAPE AND OWNERSHIP CLASSIFICATION
        DC-D-021 system of record · DC-D-036 integration ownership · DC-D-111 platform estate
        DC-D-048 automation shape · DC-D-001 criticality
        → these decide *whose problem this is* before deciding *what to build*.

STEP 3  ENVELOPE (exclusion evidence only)
        DC-D-023, 037, 039, 040, 041, 042, 049, 050, 084, 085, 086, 087, 088
        → limits exclude designs; they never prove performance (NB-07, AP-D-048).

STEP 4  COMPOSED DISQUALIFIERS
        §3 above — the twelve registered rows, and only those
        → run explicitly. A set of individually-CONDITIONAL verdicts is NOT a pass.
        → the `Cf` rows are the INPUTS to this step, not candidates for it:
          resolve each `Cf` criterion, then test the registered row it feeds.

STEP 5  OBLIGATION AND CAPABILITY GATES
        DC-D-070, 073, 083, 104, 110 · DC-D-006
        → these make options *unavailable* rather than worse.

STEP 6  ECONOMICS
        DC-D-008, 092–099
        → priced on the same ten dimensions for every surviving class
          (`alternatives.md` §2.1, §5.2). An unfunded mandated control is infeasibility, not a trade-off.

STEP 7  DIRECTION AND TRADE-OFFS
        everything remaining
        → produce an outcome class from `decision-criteria.md` §6.2 — the CLOSED set of 14 —
          with its conditions, its validation obligations and its accepted risks named.
        → the class of the firing criterion determines which outcomes are REACHABLE:
          §2.5's class → outcome mapping is authoritative. Xp→5 · Xr→3/4/6 · Xe→7 ·
          Xc→2/5/7/11/12/14, NAMED PER REGISTERED ROW at §3's Class column, never
          one class for every Xc criterion · Ri→2 or 13 · Cf→none alone · —→1 or 2.
        → an `Ri` may NEVER produce 3, 4, 5, 6 or 7. An in-platform store, pattern
          or surface change is not an exclusion of the platform.
        → if the label you are about to write is not in §6.2, the label is wrong,
          not the set. V1 emitted two that were not (T-01, T-05); §6.2 now defines
          class 13 for the first and states the second as a condition on class 2.

STEP 7a COMPARATOR CHECK  (added 2026-09-03)
        `decision-criteria.md` §4A
        → before writing any terminal sentence, separate the four statements:
          (1) exclusion and at what scope · (2) which ALT classes come into scope ·
          (3) what §4A.2 says about them, or `COMPARATOR EVIDENCE ABSENT` ·
          (4) preference — permitted ONLY where (3) discriminates.
        → on current evidence (4) is available on ONE axis: DC-D-108 deployment model.
          Everywhere else the terminal outcome is
          `POWER PLATFORM <excluded / excluded for responsibility R / economically
           unattractive> → CANDIDATES: ALT-NNN — COMPARATIVE FIT UNEVALUATED`.

STEP 8  VALIDATION LEVEL
        DC-D-089 · DC-D-081 · DC-D-100
        → state which of V1 limits / V2 bounded pilot / V3 pro-code harness / V4 managed-test
          fidelity the commitment requires, and budget it.
```

**Why this order.** Steps 0–1 are cheap and can terminate the analysis; running them last wastes the engagement and — worse — produces a recommendation that a single unasked question invalidates. Steps 4–5 exist because the corpus's own evidence shows that per-criterion favourability does not compose. Step 6 comes after the gates because an option that is unavailable cannot be made available by being cheap. **Step 7a comes last because it is the step that was missing**: the model's internal caveats were surviving every earlier step and then being discarded at the boundary where the outcome is written down.

---

## 6. Adversarial tests

Sixteen scenarios (T-16 added 2026-09-03), each answering: which criteria trigger · which anti-patterns are detected · which alternatives remain viable · can the platform be rejected · is hybrid triggered · does the evidence support the conclusion.

**Method note.** These are tests of the decision model, not worked engagements. Each scenario is deliberately under-specified in the way real ones are, which is why several terminate at `DECISION BLOCKED` — that is the model working, not failing. **The model was not tuned to make these produce neat outcomes**; §7 records where they exposed gaps.

---

### T-01 — Simple departmental internal app

*Twelve people in one team track equipment inspections. Currently a spreadsheet. No integration, no external users, no regulatory regime, low volume, tolerant process.*

- **Criteria triggering:** DC-D-001 `SIMPLE DEPARTMENTAL` · DC-D-008 value marginal but positive · DC-D-010 `TENS` · DC-D-022 `SIMPLE` · DC-D-023 below ceiling · DC-D-030 `RARE` · DC-D-074 `SINGLE TEAM` · DC-D-093 inside existing entitlement · DC-D-104 `SIMPLE DEPARTMENTAL`.
- **Anti-patterns detected:** none in the design. Two **risks of over-correction**: AP-D-039 (imposing enterprise controls) and AP-D-005 (starting above the simplest structure). One latent: AP-D-065 if no graduation trigger is set.
- **Alternatives viable:** ALT-003 (a form over a list, or a team-scoped store), ALT-004, ALT-002 (does the inspection log need to exist at all?), ALT-010.
- **Can the platform be rejected?** No exit signal fires — DC-D-022 is `Cf`, DC-D-030 is `Ri` at `RARE` and inert here, and nothing else carries a class. It is also not *required*.
- **Hybrid triggered?** No.
- **Outcome:** `POWER PLATFORM — STRONG FIT` (`decision-criteria.md` §6.2 class 1) **or** class 13 **`ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED`** naming **ALT-003** — a form over a single list whose readers are the list's readers, which is one of the four shapes the corpus states positively (`data-architecture.md` §6; `anti-patterns.md` AP-D-008 Exceptions). Either way a **graduation trigger is recorded** (DC-D-074, DC-D-001) so growth is a decision rather than a surprise, and class 13 makes that trigger mandatory because the documented path off the team-hosted and collaboration surfaces is a **one-way upgrade** that converts every user to premium (`application-architecture.md` AA-50). *(Corrected 2026-09-03: this scenario emitted `COLLABORATION-PLATFORM NATIVE`, a label `decision-criteria.md` §6 never defined. The label was the symptom; the cause was that the closed set had no class for "an alternative is the documented answer and the platform is not excluded", so a pack implementing §6.2 literally would have had to drop this branch — biasing toward Power Platform on the commonest engagement shape there is. Class 13 exists for it and states the non-exclusion explicitly.)*
- **Evidence supports it?** Yes, and the corpus is explicit that this class is legitimate and over-engineering it is a real cost (`operations-support.md` §1.1, `licensing-cost.md` LC-28). Note what class 13 does **not** say: it makes no comparative claim about cost, speed or scale. Its *"cheaper or lighter"* is the seeded-entitlement fact of DC-D-093, not a TCO comparison — `licensing-cost.md` LC-U-04 records that none exists.

---

### T-02 — Excel replacement

*A finance team's shared workbook. Six writers, ~40,000 rows growing, several lookups, monthly reporting, occasional concurrent edits, some fields visible only to two managers.*

- **Criteria triggering:** DC-D-023 `ABOVE CEILING` · DC-D-030 `ROUTINE` · DC-D-026 `FIELD` · DC-D-022 `RELATIONAL` · DC-D-031 aggregation and trends · DC-D-093 → premium for the whole audience · DC-D-024 moderate with growth.
- **Anti-patterns detected:** **AP-D-008** (the spreadsheet is already the anti-pattern — *"Simultaneous file modifications … are not supported"*, and the row count is past the client ceiling) · **AP-D-050** (any non-delegable path over 40,000 rows returns silently wrong answers) · **AP-D-009** (monthly reporting from the operational store) · **AP-D-061** if the answer is "keep it in a list to avoid premium".
- **Alternatives viable:** ALT-004 (governed relational store — the field-level requirement effectively selects it), ALT-001 if the finance system already holds this, ALT-003 **rejected** by DC-D-026 (no column security) and DC-D-030 (no conflict control).
- **Can the platform be rejected?** No. But note the honest counterweight: DC-D-093 means a premium population, so DC-D-008 must be re-tested after DC-D-093 — a six-person team paying premium is affordable; a six-hundred-person one may not be.
- **Hybrid triggered?** Only for reporting: DC-D-031's `Xr` moves the **enterprise-analytics responsibility** to a data platform if aggregation over growing data is in scope. Nothing else leaves.
- **Class arithmetic (the V1 defect this scenario exposed).** Four criteria fire at consequence states: **DC-D-030 `Ri`** (routine contention disqualifies the spreadsheet and the document/list store as system of record → the governed store with an explicit concurrency design), **DC-D-026 `Xr`** (only at `ADMINISTRATOR-EXCLUDED`, which this scenario does not reach — two managers' field visibility is `FIELD`, satisfied in-platform), **DC-D-023 `Xr`** (only where no server-side shaping is possible; here it is), and **DC-D-022 `Cf`** feeding 023 and 088. So **exactly one `Xr` is live and it is scoped to reporting**, and the rest are in-platform consequences.
- **Outcome:** `POWER PLATFORM — FIT WITH CONSTRAINTS` (`decision-criteria.md` §6.2 class 2 — governed relational store; premium entitlement priced; analytical path for reporting). *(Unchanged 2026-09-03, and this scenario is why the V1 taxonomy had to be repaired: V1 classed DC-D-030, DC-D-025 and DC-D-088 as `Xr` exits, and this file's own rule mapped every `Xr` to outcome classes 3, 4 or 6. Followed literally, that rule turns "use the governed store instead of the list" into **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`**. The scenario was right and the rule was wrong; `Ri` is the class that makes the rule agree with the scenario.)*
- **Evidence supports it?** Yes. This is the corpus's best-evidenced scenario in both directions (`data-architecture.md` §2, `performance-scale.md` PF-AP-12).

---

### T-03 — Business-critical internal app

*Order-exception handling for a manufacturer. 400 users, drives production decisions, four hours' downtime has material cost, integrates with the resource-planning system, five-year expected life.*

- **Criteria triggering:** DC-D-001 `BUSINESS-CRITICAL` · DC-D-004 `3–5 YEARS` · DC-D-021 the resource-planning system owns the order · DC-D-036 integration ownership **must be established** · DC-D-091 end-to-end availability · DC-D-100 recovery objectives · DC-D-101 observability · DC-D-097 support tier · DC-D-093 entitlement · DC-D-047 consumer count · DC-D-104 operational maturity.
- **Anti-patterns detected:** **AP-D-047** if artefacts are not solution-aware from day one · **AP-D-053** if no owner and no monitoring · **AP-D-056** if a four-hour objective is quoted from the platform's figure · **AP-D-010** if the order entity is replicated wholesale · **AP-D-066** if the automation is owned by a person.
- **Alternatives viable:** ALT-004, ALT-001 (extend the resource-planning system), ALT-007 (if an integration platform owns that system), ALT-009.
- **Can the platform be rejected?** Not on current information — but **DC-D-036 and DC-D-100 are decision-blocking**. If the resource-planning system is already integrated through an enterprise platform with a published contract, DC-D-036's exit fires for the *integration responsibility*.
- **Hybrid triggered?** Probably — ALT-007's shape: the resource-planning system keeps authority, the platform supplies the exception-handling experience and workflow.
- **Outcome:** `DECISION BLOCKED` on DC-D-036, DC-D-100, DC-D-091 → then most likely `POWER PLATFORM + ENTERPRISE-SYSTEM HYBRID`, with the managed-environment chain (observability, backup, pipelines) **priced into the option**.
- **Evidence supports it?** Yes, including the blocking. Note the corpus's own caution: *"a departmental solution becomes expensive the day it matters"* — the criticality classification is what makes this option cost what it costs.

---

### T-04 — External customer portal

*Insurance claims status for 200,000 policyholders. Self-registration, claim documents, status updates from a back-office system, expected sub-minute freshness after an adjuster updates a claim.*

- **Criteria triggering:** DC-D-009 `EXTERNAL AUTHENTICATED — CUSTOMERS` · DC-D-061 external identity · DC-D-018 **sub-minute freshness** · DC-D-010 `TENS OF THOUSANDS+` · DC-D-058 sensitivity · DC-D-094 metering unit is the contact record · DC-D-085 concurrency · DC-D-025 documents · DC-D-091 availability.
- **Anti-patterns detected:** **AP-D-034** (the exposure surface — anonymous or generic-authenticated roles with broad permissions is the documented mass-exposure class) · **AP-D-024** and **AP-D-009** if freshness is answered by polling harder · **AP-D-032** (all portal traffic reaches the data layer through one acting identity — DC-D-086's concentration case).
- **Alternatives viable:** ALT-004 (external-site surface), ALT-005 (custom web), ALT-011 (an insurance portal product).
- **Can the platform be rejected?** **Yes, on DC-D-018.** The external-site surface's server-side cache carries a **15-minute, non-reducible** freshness commitment, and derived values from back-office writes are *"never guaranteed to be immediate"*. A sub-minute freshness requirement for changes made elsewhere is a documented exit for that read surface.
- **Hybrid triggered?** Yes, if the requirement is renegotiated: platform for authenticated document access at 15-minute freshness, with status pushed to a separate low-latency read surface. Or custom web for the whole read surface.
- **Outcome:** `DECISION BLOCKED` on the freshness number (is "sub-minute" real?) → then either `POWER PLATFORM — FIT WITH CONSTRAINTS` at 15-minute freshness, or — if the number is real — **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`** (the external-site read surface, an `Xr` exit) **→ `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-005, ALT-011.** The exit is clean; **the replacement's adequacy is unevidenced** — no latency or throughput measurement exists for any technology (NB-07), so the model cannot say how much better another read surface would be, and must not imply it. The platform remains a legitimate candidate for the authenticated document access behind the read surface.
- **Evidence supports it?** Yes — this is one of the cleanest single-criterion exits in the corpus (`performance-scale.md` PF-17…PF-20).

---

### T-05 — High-volume integration

*Nightly plus intraday synchronisation of 900,000 product records between a supplier system and the operational store, with an intraday peak of ~4,000 records per minute. Ordering matters within a product family. Duplicates are unacceptable.*

- **Criteria triggering:** DC-D-040 sustained throughput · DC-D-037 peak per minute · DC-D-039 per-mechanism ceilings · DC-D-041 **ordered, duplicates unacceptable** · DC-D-052 idempotency key · DC-D-086 per-identity rate · DC-D-034 migration scope · DC-D-021 the supplier system owns the product.
- **Anti-patterns detected:** **AP-D-016** (a workflow engine as a high-volume transaction engine) · **AP-D-049** (sizing against one meter) · **AP-D-015** (an integration-orchestration requirement built as workflow automation) · **AP-D-017** if retry is enabled without a key · **AP-D-015** (an integration-orchestration requirement built as workflow automation) if ordering is attempted by setting trigger concurrency — an irreversible and lossy setting, whose criterion is **DC-D-053**. *(Corrected 2026-09-03: this cited AP-D-053, which is* Business-critical application with no monitoring and no incident owner *— a silent failure, because `AP-D-NNN` and `DC-D-NNN` share a numeric range so both ids resolve.)*.
- **Alternatives viable:** ALT-006 (broker plus workers, or a data pipeline for the bulk leg), ALT-007 (if an integration platform exists — check DC-D-036 first), ALT-009.
- **Can the platform be rejected?** **For the integration responsibility, yes** — if DC-D-040 shows the sustained rate exceeds the smallest meter with no natural partitioning. Note the corpus's discipline: this requires the *number*, and *"scale anxiety without a number"* is not a reason to leave.
- **Hybrid triggered?** Yes, and this is the canonical shape: a broker carries ordering and deduplication; a bulk mechanism or pipeline carries the volume; the platform orchestrates and holds the business record.
- **Outcome:** `POWER PLATFORM + CLOUD-NATIVE HYBRID` (`decision-criteria.md` §6.2 class 3) — **conditional on DC-D-070 and DC-D-110** (is there an operator?). Where the operator gate fails, the outcome is **class 2 `POWER PLATFORM — FIT WITH CONSTRAINTS`**, whose named condition is the corpus's own *"single platform + a tripwire, not a paper hybrid"* (`automation-architecture.md` AT2-53, §4 row 22): the ordering requirement is renegotiated, the constraint is documented, and **the metric that would force the move is recorded as the tripwire**. Where neither is acceptable, the whole responsibility goes to ALT-007 under class 6 → class 8. *(Corrected 2026-09-03: `single platform + a tripwire` was emitted as an outcome label and defined in no closed set. It is a **condition on a fit**, not a terminal class — the hybrid was triggered and its gate failed, so the responsibility stays in-platform. The corpus's phrase is kept as the condition's wording; the class is 2.)*
- **Evidence supports it?** Yes. Note **DC-D-039 is decision-blocking** if a custom connector is on the path — the 20× conflict is live.

---

### T-06 — Complex data-centric enterprise application

*Contract lifecycle management. 12,000 contracts with 40 related entity types, clause-level version history, row and field security by business unit and deal team, seven-year retention, board-level reporting, integration with signature and finance systems.*

- **Criteria triggering:** DC-D-022 `RELATIONAL`/`DEEP` · DC-D-026 `RECORD AND FIELD` · DC-D-027 compliance-grade audit · DC-D-032 multi-year queryable retention · DC-D-031 aggregation and trends · DC-D-021 split ownership · DC-D-035 several streams · DC-D-058 confidential · DC-D-001 enterprise · DC-D-071 environment strategy.
- **Anti-patterns detected:** **AP-D-029** if the ownership and business-unit model is designed after the tables (ownership type is **immutable**) · **AP-D-009** (board reporting from the operational store) · **AP-D-012** if signature or finance data is virtualized while field security is required · **AP-D-063** (audit consumes log capacity no entitlement provides) · **AP-D-011** if the finance integration is bidirectional without a field ownership matrix.
- **Alternatives viable:** ALT-004 (the record-centric surface over the governed store is a documented **STRONG** verdict for exactly this shape), ALT-011 (contract-lifecycle products exist — DC-D-002 says check), ALT-009 for reporting and integration.
- **Can the platform be rejected?** No exit fires. **The one criterion that could be misread as an exit is DC-D-022**, which is `Cf`: traversal beyond two lookup levels in a single required view does not reject the platform — it feeds **DC-D-088's `Ri`** (server-side views, a flattened model, or a different surface), an in-platform redirect. The genuine exit risk is **DC-D-062's `Xr`** if administrator exclusion is required on commercially sensitive clauses, which would move that attribute out of the governed store. *(Corrected 2026-09-03: V1's `Xr`/`Xc` classing let DC-D-022's depth read as a platform rejection.)*
- **Hybrid triggered?** Yes, on two axes: an analytical store for board reporting (DC-D-031), and mediation or an existing boundary for the two integrations (DC-D-047 — two consumer classes).
- **Outcome:** `POWER PLATFORM — FIT WITH CONSTRAINTS` (class 2) for the application scope, **plus** `POWER PLATFORM + CLOUD-NATIVE HYBRID` (class 3) for the analytical responsibility only (DC-D-031's `Xr`), with a mandatory ALT-011 check first (DC-D-002, DC-D-109) and the security model designed **before the first table**. *(Corrected 2026-09-03: this read "plus `HYBRID`", a label `decision-criteria.md` §6.2 does not contain. Two classes on two scopes is the accurate statement, and §6.4 already allows an outcome per scope.)*
- **Evidence supports it?** Yes, and this is the scenario where the platform's positive case is strongest — a documented STRONG verdict rather than an absence of violated constraints.

---

### T-07 — Strict low-latency requirement

*A trading-desk pre-trade compliance check. Must return a pass/fail within 200 ms, synchronously, visible in the same transaction, calling two internal services and a market-data feed.*

- **Criteria triggering:** DC-D-084 **strict** · DC-D-042 `STRICT LOW-LATENCY` · DC-D-050 strict sub-second · DC-D-091 composite availability · DC-D-057 possibly compute · DC-D-029 read-your-writes.
- **Anti-patterns detected:** **AP-D-003** (a hard non-functional requirement dominating) · **AP-D-019** (a synchronous chain across three participants) · **AP-D-048** if the answer is "we're inside the 120-second window, so it's fine".
- **Alternatives viable:** ALT-005, ALT-006, ALT-007 (if the trading platform should own the check).
- **Can the platform be rejected?** **Yes, and on the strongest available grounds.** *"No end-to-end latency figure is published for any path"*, and the corpus's boundary B-16 is explicit: a hard sub-second, transactionally-visible end-to-end objective across an application, an automation and an external system is **not sized anywhere** → out, or the objective is renegotiated.
- **Hybrid triggered?** No — this is not a bounded excess; the requirement applies to the whole path.
- **Outcome:** **`POWER PLATFORM — POOR FIT`** for the pre-trade check (an `Xp` exit on DC-D-084 / DC-D-042, over-determined) **→ `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-005, ALT-006, ALT-007.** The platform may still serve the *surrounding* case-management workflow, which is a separate scope. *(Renamed 2026-09-03 from `CUSTOM DEVELOPMENT PREFERRED` or `EXISTING ENTERPRISE PLATFORM PREFERRED`: the exclusion is evidenced, the preference between the three candidates is not — see the note below.)*
- **Evidence supports it?** Yes for the **exclusion**; **no for any preference between the survivors**. The model does **not** claim a custom stack will achieve 200 ms either — DC-D-089 still requires measurement, and NB-07 applies to every technology. This is the scenario that makes the H-02 repair concrete: the old label said *custom development is preferred* on evidence that established only *Power Platform is excluded*. `decision-criteria.md` §4A.2 adds what little can be said on the comparator side here — ALT-005's 230-second HTTP ceiling and cold-start behaviour, ALT-006's identical 120-second synchronous window — none of which favours one over another at 200 ms.

---

### T-08 — Regulated, security-sensitive workload

*Clinical trial adverse-event capture. Special-category personal data, a validated-systems regime requiring change control, customer-managed keys mandated, administrator exclusion demanded by the sponsor's contract, country-level residency, 600 users across four countries.*

- **Criteria triggering:** DC-D-058 `SPECIAL CATEGORY` · DC-D-059 `REGULATED WITH EXTERNAL AUDIT` · DC-D-062 **administrator exclusion required** · DC-D-064 customer-managed keys · DC-D-027 provable evidence · DC-D-033 `COUNTRY-LEVEL` · DC-D-107 `CHANGE CONTROL REQUIRED` · DC-D-092/093 the control population.
- **Anti-patterns detected:** **AP-D-029** (security model late) · **AP-D-033** (one control treated as the whole control) · **AP-D-064** (control prerequisites priced by population) · **AP-D-057** (no preview components on this path) · **AP-D-058** (the mandatory wave cadence versus a validated-systems regime).
- **Alternatives viable:** ALT-005, ALT-011 (validated trial-management products exist), ALT-007, ALT-008 (DC-D-108 is not triggered here, but DC-D-107 makes a self-managed upgrade schedule attractive).
- **Can the platform be rejected?** **Yes, on two independent criteria.** DC-D-062: *"Confidential even from administrators"* is **not achievable** in the governed store — the attribute must live elsewhere or the administrator population must be reduced to an auditable just-in-time set. DC-D-064 + DC-D-027: customer-managed keys and audit have a **documented conflict** (audit is not available with them), which must be resolved before the option is viable. DC-D-107 adds a third pressure: mandatory semi-annual waves against a per-release validation regime is a documented `RISK → CONDITIONAL`.
- **Hybrid triggered?** Possibly: the adverse-event narrative field (the administrator-excluded attribute) outside the governed store, everything else inside. That is a genuine hybrid, and it needs DC-D-070/110 to be satisfied.
- **Outcome:** `DECISION BLOCKED` on DC-D-059's clause reading → then either **`POWER PLATFORM + CLOUD-NATIVE HYBRID`** with the administrator-excluded attribute outside the governed store (DC-D-062's `Xr` exit, gated on DC-D-070/DC-D-110), or — where the regime's mandated control has no available implementation — **`POWER PLATFORM — POOR FIT`** (DC-D-059's `Xp` exit) **→ `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-011, ALT-005, ALT-007, ALT-008.** Note what the model must **not** say here: a validated trial-management product exists as a *category*, and no product was evaluated. **The model must not resolve the key-versus-audit conflict silently** — that is `anti-patterns.md` AP-D-033's failure.
- **Evidence supports it?** Yes, including the refusal to resolve the conflict.

---

### T-09 — Mission-critical workload

*Utility outage dispatch. 24×7, a committed 15-minute recovery time, must survive the loss of a region, integrates with field devices and a geospatial system, 300 dispatchers plus 2,000 field engineers with offline capture.*

- **Criteria triggering:** DC-D-001 `MISSION-CRITICAL` · DC-D-100 **cross-region with a committed time** · DC-D-091 composite availability · DC-D-016 offline write · DC-D-089 provability · DC-D-104 operational maturity · DC-D-097 support tier · DC-D-101 observability · DC-D-040 device throughput.
- **Anti-patterns detected:** **AP-D-056** (a 15-minute recovery time quoted from platform figures — none is published for cross-region) · **AP-D-054** (recovery assumed rather than drilled) · **AP-D-052** (a mission-critical commitment with no drill) · **AP-D-059** (the composed disqualifier: mission-critical + no representative managed test environment + no drill).
- **Alternatives viable:** ALT-005, ALT-006, ALT-007, ALT-009, ALT-011.
- **Can the platform be rejected?** **For the recovery commitment, effectively yes.** Cross-region resilience is opt-in, managed-gated, doubles storage, **degrades high-volume automation**, has **no published recovery-time commitment**, has **no prescriptive test plan**, permits **no deployments while failed over**, and does **not cover** several adjacent services. A **contractual 15-minute cross-region recovery time cannot be underwritten from platform evidence** — it can only rest on the customer's own drills.
- **Hybrid triggered?** Yes, necessarily — and note that a hybrid **worsens** DC-D-091, because each added operated component lowers the composite availability.
- **Outcome:** `DECISION BLOCKED` on DC-D-100 and DC-D-091 → then either the commitment is restated as a drilled, customer-owned objective (in which case `POWER PLATFORM — FIT WITH CONSTRAINTS` is arguable for the dispatch experience with offline capture, which the platform genuinely supports), **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`** (the recovery commitment) **→ `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-005, ALT-006, ALT-007** for the dispatch core. Manifest NB-03 supports that these classes *can* underwrite a contractual objective; **NB-07 means none of them is evidenced to meet 15 minutes either**, so the candidate set is a set of things to assess, not a ranking.
- **Evidence supports it?** Yes. This scenario also demonstrates the order dependency: evaluating DC-D-016 (offline, a platform strength) before DC-D-100 (recovery, a platform absence) produces an optimistic answer that Step 0–1 correctly prevents.

---

### T-10 — Citizen-developed app becoming enterprise-owned

*A team-scoped holiday-planning app built by one person now used by 1,400 people across five countries, in the default environment, unowned, with the original maker having left.*

- **Criteria triggering:** DC-D-006 **`NONE`** (the maker has left) · DC-D-074 scope now cross-function · DC-D-001 now business-critical · DC-D-071 the default environment · DC-D-104 maturity gap · DC-D-093 entitlement now population-wide · DC-D-033 four countries · DC-D-080 reversibility · DC-D-001 criticality now driving solution-awareness, whose failure is **AP-D-047**. *(Corrected 2026-09-03: this cited DC-D-047, which is* Consumer count for a backend capability.*)*.
- **Anti-patterns detected:** **AP-D-036** (maker enablement without ownership or a promotion path) · **AP-D-040** (production workload in the default environment — no security group, no backup guarantee, everyone a maker) · **AP-D-047** (non-solution artefacts: excluded from backup, ineligible for capacity licences, undeployable) · **AP-D-066** (the automation's profile has **reverted to Low** on the maker's departure, and a non-solution automation's owner **cannot be changed at all**) · **AP-D-065** (the free-tier trap, realised) · **AP-D-053**.
- **Alternatives viable:** ALT-004 (rebuild properly), ALT-011 (a leave-management product — DC-D-002 says this is commodity), ALT-001 (the HR system probably owns leave), ALT-002.
- **Can the platform be rejected?** No exit signal — but **DC-D-002 and DC-D-109 make ALT-011/ALT-001 the strongest candidates**: leave management is a commodity domain that the HR system likely already covers, and the corpus's rung 0 says configure or buy **before any build**.
- **Hybrid triggered?** No.
- **Outcome:** `DECISION BLOCKED — MORE EVIDENCE REQUIRED` (class 12) on DC-D-006 (who owns it?) → on resolution, **the registered composed disqualifier fires explicitly** (§3, Block D row 3: citizen-built artefacts outside a solution + criticality now business-critical + the maker gone) and the terminal outcome is **class 14 `IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED`** → **class 8 `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-011, ALT-001, ALT-004 (rebuilt), ALT-002**. The named mechanisms are the row's own: non-solution artefacts are excluded from backup, ineligible for capacity licences and undeployable; a non-solution automation's **owner cannot be changed at all**; the departed maker's profile has already reverted. DC-D-002 (`COMMODITY`) and DC-D-109 make ALT-011 and ALT-001 the strongest *candidates* — the corpus evaluates neither the product category nor the HR system, so "strongest candidate" means *first to assess*, not *chosen*. *(Corrected 2026-09-03: this scenario emitted class 8 **unaccompanied**, against class 8's own definition as the terminal form for an exclusion. The reason it had no antecedent is that no class existed for its actual conclusion: the composed row says the workload cannot be brought to the required class **in place**, which is not "the option is unavailable" — class 5 does not fire, and Power Platform **rebuilt** is a live candidate. Class 14 is that conclusion, and it keeps the platform in the candidate set instead of rejecting it.)* If the platform is retained: a new environment, solution-aware artefacts, named ownership, and a premium-licence census for 1,400 users.
- **Evidence supports it?** Yes, and this scenario is the one where the corpus's mechanics are most unforgiving: three of the detected anti-patterns describe conditions that **cannot be repaired in place**.

---

### T-11 — Hybrid platform + cloud-native solution

*Document-heavy grant assessment. Assessors work in a low-code application; each submission triggers a machine-learning classification and an optical-character-recognition step; 3,000 submissions per month in two annual peaks; a mature cloud platform team exists.*

- **Criteria triggering:** DC-D-057 **specialised compute** · DC-D-025 attachment volume · DC-D-037 seasonal peaks · DC-D-054 failure semantics · DC-D-050 asynchronous · DC-D-070 `ESTABLISHED ACROSS PLATFORMS` · DC-D-110 `FULL ENGINEERING CAPABILITY` · DC-D-083 coordination · DC-D-096 external cost · DC-D-055 human assessment decisions.
- **Anti-patterns detected:** none fatal, and **that is the finding** — the gates pass. Latent: **AP-D-046** if only the platform side gets a pipeline · **AP-D-026** if the cloud components have no named operator (they do, here) · **AP-D-017** if the classification step is retried without an idempotency key · **AP-D-006** if the components remain after the classification model is retired.
- **Alternatives viable:** ALT-009 (this *is* ALT-009), ALT-005 for the whole thing, ALT-006 for more of it.
- **Can the platform be rejected?** No — and it should not be. DC-D-055 is a positive signal (human assessment decisions within 30 days are the platform's strongest differentiator), and DC-D-057's exit applies to **one step**, not the solution. The corpus is explicit: *"one difficult step"* is not a reason to relocate everything.
- **Hybrid triggered?** **Yes, correctly** — a bounded, nameable excess with a satisfied operator gate.
- **Outcome:** `POWER PLATFORM + CLOUD-NATIVE HYBRID`, with two supply chains, a declared release sequence, a propagated correlation identifier, an idempotency key on the classification write, and a status resource for the asynchronous work.
- **Evidence supports it?** Yes. This is the scenario the corpus's hybrid evidence was written for, and the one where the gates being *satisfied* is what makes the option available.

---

### T-12 — The existing enterprise system should own the capability

*Field-service scheduling. The organisation runs a mature service-management platform with a scheduling module it has not deployed, plus an integration platform with published contracts for that system.*

- **Criteria triggering:** DC-D-111 `PLATFORMS EXIST WITH PUBLISHED CONTRACTS` · DC-D-036 the same · DC-D-021 the service platform owns the work order · DC-D-002 `COMMODITY` · DC-D-109 existing estate · DC-D-003 lead time of the platform team.
- **Anti-patterns detected:** **AP-D-027** (bypassing the existing integration owner) · **AP-D-007** (rebuilding what an existing capability provides) · **AP-D-022** (a new point-to-point path to a system already integrated) · **AP-D-002** (Y-12: standing up a parallel boundary).
- **Alternatives viable:** ALT-007 (deploy the incumbent's module), ALT-001, ALT-011, ALT-004 only for a genuinely uncovered surface.
- **Can the platform be rejected?** **Yes, for the integration responsibility outright** (DC-D-036's exit), and probably for the capability, via DC-D-002 + DC-D-111. The corpus's caveat must be applied honestly though: *"reuse is not automatic — an incumbent that cannot meet the requirements remains unsuitable"*, so the incumbent module's fit must be assessed **per requirement**, not assumed.
- **Hybrid triggered?** Possibly the reverse of the usual shape: the incumbent owns scheduling; the platform supplies a lightweight field-facing surface **only if** the incumbent's mobile experience genuinely fails a stated requirement (DC-D-015, DC-D-016).
- **Outcome:** **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`** (the integration responsibility, DC-D-036's `Xr` exit) **→ `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-007 (deploy the incumbent's module), ALT-001, ALT-011** — with `INCUMBENT FIT UNEVALUATED` carried explicitly, a per-requirement gap analysis, and the platform team's lead time recorded as a constraint (not as a justification for bypassing them — that is AP-D-027). Where the incumbent keeps authority and the platform supplies a surface, the outcome is instead **`POWER PLATFORM + ENTERPRISE-SYSTEM HYBRID`**. *(Renamed 2026-09-03 from `EXISTING ENTERPRISE PLATFORM PREFERRED`: the corpus evaluates no incumbent, so "preferred" was a claim it cannot make.)*
- **Evidence supports it?** Partly. **Note NB-06 honestly:** the enclosing-boundary pattern is the corpus's *own synthesis* (`INF`), not vendor-endorsed, and the corpus evaluates **no incumbent platform**. So the *reasoning* is sound and the *fit* is a per-engagement assessment the corpus cannot make.

---

### T-13 — Custom application is clearly preferable

*A customer-facing mobile application for a logistics company: branded, in both app stores, push notifications for delivery events, offline capture with custom conflict rules, 400,000 consumers, an intended public interface for partner integrations.*

- **Criteria triggering:** DC-D-020 **branded distribution with push** · DC-D-009 `PUBLIC` consumers · DC-D-016 offline write with custom conflict rules · DC-D-012 `PRODUCT-GRADE` · DC-D-010 `TENS OF THOUSANDS+` (400,000) · DC-D-045 a public interface for third parties.
- **Anti-patterns detected:** **AP-D-003** (five dominant non-functional requirements, not one) · **AP-D-005** in reverse — the risk here is *under*-engineering by forcing a low-code answer.
- **Alternatives viable:** ALT-005 only, realistically. ALT-009 for a platform-based back office behind a custom consumer front end.
- **Can the platform be rejected?** **Yes, on four independent documented exits**: push notifications with branded distribution are *unsatisfiable in-platform*; the wrapping mechanism explicitly excludes consumer audiences; offline with custom conflict rules is a documented custom-development trigger; a public interface for third parties is not the platform's purpose. DC-D-010 adds an economic exit at 400,000 consumers.
- **Hybrid triggered?** Yes, in its useful form: custom consumer application over platform-hosted business processes and data for the internal back office.
- **Outcome:** **`POWER PLATFORM — POOR FIT`** for the consumer surface — four independent `Xp` exits plus an `Xe` — **→ `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-005** (realistically the only class in scope, which is *scope narrowing*, not evaluation). `POWER PLATFORM` remains a legitimate candidate for the internal operations behind it, and the composition is ALT-009. *(Renamed 2026-09-03. Note what does **not** change: the rejection is as strong as it was, and over-determined.)*
- **Evidence supports it?** Yes — this is the corpus's most over-determined rejection, which is itself useful: a scenario needing four exits to be confident is different from one resting on a single conflicted figure.

---

### T-14 — The platform is economically unattractive

*Internal expense pre-approval. 9,000 employees, each using it perhaps twice a month. Requires the finance system connector (premium) and a network-isolation mandate because of the finance data.*

- **Criteria triggering:** DC-D-010 `THOUSANDS` (9,000) · DC-D-094 **large population × low frequency** · DC-D-093 premium for the whole audience · DC-D-063 network isolation mandated → managed class + higher-tier entitlements · DC-D-092 budget · DC-D-008 value versus cost · DC-D-002 `COMMODITY`.
- **Anti-patterns detected:** **AP-D-062** (the entitlement boundary discovered after design) · **AP-D-064** (control prerequisites priced by **affected population** — 9,000 people) · **AP-D-061** if the response is to drop the isolation control or use a shared identity · **AP-D-060** if the case was built on a licence line.
- **Alternatives viable:** ALT-001 (the finance system almost certainly has expense pre-approval), ALT-011, ALT-002 (is pre-approval needed at all, or is post-hoc sampling sufficient?), ALT-005, ALT-006 (consumption-metered), ALT-010.
- **Can the platform be rejected?** **Yes, economically.** DC-D-094's shape (many users, little work each) plus DC-D-093's premium population plus DC-D-063's higher-tier prerequisites across 9,000 people. The corpus's forbidden move is explicit: **never remove the required control to make the option look cheaper**. And DC-D-094 is where the corpus's retained hypothesis applies — the users-to-work ratio is high, which is *directionally* against people-priced mechanisms. **That is a hypothesis to test with real numbers, not a verdict.**
- **Hybrid triggered?** No.
- **Outcome:** **`POWER PLATFORM — ECONOMICALLY UNATTRACTIVE OR INFEASIBLE`** (`decision-criteria.md` §6.2 class 7 — `Xe` exits on DC-D-010, DC-D-093, DC-D-092) **→ `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`: ALT-001, ALT-011, ALT-002, ALT-005, ALT-006, ALT-010**, with the comparison to be run per engagement on all ten cost dimensions. **The model states that this option is expensive for this demand shape. It states nothing whatever about what the others cost** — `licensing-cost.md` LC-U-04 records that no comparative pricing was fetched for any of them. *(Renamed 2026-09-03; the old form emitted a class §6 never defined, and its continuation `→ EXTEND THE EXISTING SYSTEM or BUY` read as a recommendation.)*
- **Evidence supports it?** **Partly, and this is the model's weakest test.** The *mechanism* is well-evidenced (population-priced entitlement and control prerequisites). The *comparison* is not: `licensing-cost.md` LC-U-04 records that **no comparative pricing was fetched for any alternative**, so the model can say "this is expensive for this shape" and cannot say "that one is cheaper". Recorded as a gap in §7.

---

### T-15 — Insufficient information to choose

*A sponsor asks for "a portal so suppliers can see their orders". No volume, no identity model, no ownership, no budget, no regulatory position, no residency statement, and the order system is unnamed.*

- **Criteria triggering:** essentially the whole of `decision-criteria.md` §5.2 as `UNKNOWN` — including DC-D-009, 021, 036, 037, 040, 059, 061, 092, 093, 100, 104, 108.
- **Anti-patterns detected:** **AP-D-001** (a solution named before the problem is characterised — "a portal" is already a solution shape) · **AP-D-051** if any figure is estimated to unblock the analysis.
- **Alternatives viable:** all eleven remain open, which is the correct state.
- **Can the platform be rejected?** No — and it cannot be selected either.
- **Hybrid triggered?** Unknowable.
- **Outcome:** **`DECISION BLOCKED — MORE EVIDENCE REQUIRED`**, with a named evidence task per blocking criterion, an owner, and — critically — **the outcome each resolution would produce**, so the sponsor can see which questions actually matter. For this scenario the highest-value four are: DC-D-009 (identity class — selects the surface and the licence model), DC-D-021/036 (who owns the order and its integration), DC-D-018 (freshness — the single cleanest exit for a portal), and DC-D-108 (deployment model — can eliminate the platform entirely).
- **Evidence supports it?** Yes. Manifest §5's rule is *"do not silently infer it"*, and the corpus's `system_of_record_undecided` and `integration_volume_unknown` signals exist for exactly this state.

---

### T-16 — A conversational assistant over enterprise data *(added 2026-09-03)*

*A sponsor asks for "an assistant our field engineers and our channel partners can ask questions of, over our maintenance manuals, our parts catalogue and our open work orders". 900 internal engineers, an unstated number of partner users, answers expected to be actionable, and a stated ambition that it should later be able to raise a work order itself.*

This scenario exists because the review found that **no criterion, anti-pattern or alternative class addressed conversational or agent-shaped requirements at all** — the model would have been forced to answer it through DC-D-012 (`FORM AND LIST SHAPED` … `PRODUCT-GRADE`) or DC-D-048 (`WORKFLOW` … `DISTRIBUTED PROCESSING`), neither of which can express it, and would have returned **a confident answer to the wrong question**.

- **Criteria triggering:** **DC-D-116** `TASK-COMPLETING AGENT` (the stated ambition, not the first release) · DC-D-009 `EXTERNAL AUTHENTICATED — PARTNERS` **plus** internal · DC-D-058 sensitivity of the work-order and manual corpus · DC-D-068 whose identity the assistant reads as · DC-D-006 who owns the agent artefact · DC-D-095 consumption · DC-D-093 entitlement · DC-D-079/DC-D-080 the ALM control conflict · DC-D-100/DC-D-101 the runtime and observability position · DC-D-115 preview dependency.
- **Anti-patterns detected:** **AP-D-068** — the agent surface is being scoped inside the app and flow security review, with a partner audience and a graph/search connector on the path, which is the documented guest-access bypass · **AP-D-034** (the exposure surface, arriving through a channel nobody reviewed) · **AP-D-062** if the budget is set before a consumption pilot · **AP-D-051** if any per-interaction figure is estimated to unblock the analysis · **AP-D-057** for anything on the path whose governance controls are preview · latent **AP-D-036** if no owner is named for the agent artefact.
- **Alternatives viable:** **none evaluable.** `alternatives.md` §6 item 9: the corpus holds no fit assessment of an agent surface in **any** class, ALT-004 included.
- **Can the platform be rejected?** **No — and it cannot be selected either.** There is no `Xp`, `Xr` or `Xe` exit on DC-D-116, and the absence of an exit here is *absence of evidence*, not evidence of fit. This is the distinction the model must hold: a `—` on DC-D-018 means the corpus looked and found no exit; a `—` on DC-D-116 means the corpus never looked.
- **Hybrid triggered?** Unknowable on this evidence.
- **Outcome:** **`DECISION BLOCKED — MORE EVIDENCE REQUIRED`**, with three separable blocks and the outcome each resolution would produce:
  1. **Governance and security** — does the partner audience reach content through a graph/search connector? If yes, the guest-access control **does not close the requirement** (`security.md` SEC-04) and the path changes or the requirement is recorded as unmet. If no, the ordinary external-identity chain (DC-D-009, DC-D-061) applies.
  2. **Commercial** — consumption is *"dependent on the complexity of the task"* and cannot be modelled in advance. Closes only with a **pilot**, sized for the monthly peak. Until then DC-D-092 cannot be answered and no option is comparable on cost.
  3. **Modality** — the "raise a work order itself" ambition is `AUTONOMOUS AGENT`, on which `automation-architecture.md` U-14 records that the corpus **cannot answer the question at all** and that the deferral is **unowned**. This block does not close from the existing corpus; it closes from a research commission (`alternatives.md` §6 item 9).
- **Evidence supports it?** **Yes — including, and especially, the refusal.** The three blocks are each anchored in a quoted MS statement, and the one thing the model must not do is convert an absent fit assessment into a fit verdict in either direction. Compare T-15: there, everything is unknown *about the engagement*; here, the engagement could be fully specified and the **corpus** would still be unable to answer.

---

### T-17 — A multi-month approval process *(added 2026-09-03 — Repair V3, `block-d-gate-repair-report.md`)*

*A capital-expenditure approval process runs 90–120 days end to end, dominated by human review and cross-department sign-off. The requesting department owns the process; no external system or component is involved, and no on-call operator exists for anything outside the platform.*

This scenario exists because `block-d-gate.md` found that **DC-D-049 remained classed `Xr` on a field naming nothing leaving the platform**, and that no existing scenario exercised the criterion at all — the taxonomy's own decisive test had not been re-applied to the whole class it defines.

- **Criteria triggering:** DC-D-049 `BEYOND 30 DAYS` (state persists past the 30-day run ceiling) · DC-D-103 audit retention beyond 30 days becomes a functional requirement · DC-D-006 accountable ownership, named and single-department · DC-D-070 / DC-D-073 no operator or support tier is needed, since nothing external is proposed.
- **Anti-patterns detected:** none. The state-record pattern is the corpus's own documented answer, not a workaround. Latent AP-D-015 only if the design instead tries to hold the whole process inside a single run.
- **Alternatives viable:** none required. ALT-005 and ALT-006 remain candidates only if a future requirement genuinely needs an external orchestration tier — and both are `CONSTRAINED` on duration itself (`decision-criteria.md` §4A.2: ALT-005 at a 230-second HTTP ceiling, ALT-006 at a 5-minute stateless envelope), which is the corpus's own evidence that they are *worse*, not better, on the exact axis that would trigger them.
- **Can the platform be rejected?** **No.** DC-D-049 is `Ri`, not an exit: the run mechanism becomes unavailable at `BEYOND 30 DAYS`, and the documented answer is a business record with a re-triggering automation, in-platform.
- **Hybrid triggered?** No.
- **Outcome:** **`POWER PLATFORM — FIT WITH CONSTRAINTS`** (class 2), naming the business-record-plus-re-triggering-automation pattern as the stated condition and DC-D-103's audit-retention requirement as a design input.
- **Evidence supports it?** **Yes.** This is the corrected version of the case `block-d-gate.md` findings G-H-01 / V2-H-01 identified: before Repair V3, DC-D-049's `Xr` class routed here through §2.5's mapping to classes 3, 4 or 6 — and with no operator and no hybrid shape available, class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` fired for a requirement whose own documented answer stays in-platform, pointing the decision at the two alternatives the corpus records as constrained on the triggering axis.

---

### T-18 — Per-user backend authorization through a mediation tier *(added 2026-09-03 — Repair V3, `block-d-gate-repair-report.md`)*

*An expense-reimbursement workflow calls a downstream finance system that enforces authorization per user. A facade service sits on the path and calls the finance system's API using a single shared service identity; the facade does not currently propagate the calling user's identity, and whether it can be modified to do so is not yet known.*

This scenario exists for the same reason as T-17: `block-d-gate.md` found that **DC-D-068 remained classed `Xr` on a field naming no off-platform destination**, though it was already registered as a composed criterion at §3 row 6, and no existing scenario exercised it.

- **Criteria triggering:** DC-D-068 `TARGET ENFORCES PER USER` through a shared-identity intermediary · DC-D-036 integration ownership (who owns the facade) · DC-D-060 (named in the same registered row, §3 row 6).
- **Anti-patterns detected:** none confirmed. The row's own consequence is `DECISION CRITERION`, not an anti-pattern finding, pending the propagation question.
- **Alternatives viable:** none named. No off-platform destination exists anywhere in DC-D-068's own field, and the registered row's Class (§3 row 6) is not an exclusion.
- **Can the platform be rejected?** **No, and not on this criterion alone under any resolution.** `Xc` requires the registered combination to conclude unavailability, and this combination's own consequence is a design constraint, never an exclusion.
- **Hybrid triggered?** No.
- **Outcome:** **`DECISION BLOCKED — MORE EVIDENCE REQUIRED`** (class 12) on whether the facade can be modified to propagate identity. **If yes:** `POWER PLATFORM — FIT WITH CONSTRAINTS` (class 2), with explicit delegated identity as the named condition. **If no:** still class 12, pending a compensating-authorization design — DC-D-068's own field names no exit either way.
- **Evidence supports it?** **Yes.** Before Repair V3, DC-D-068's `Xr` class routed through §2.5's mapping to classes 3, 4 or 6, making class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` reachable for an in-platform authorization design constraint with no off-platform destination named anywhere in the criterion — the exact defect `block-d-gate.md` findings G-H-01 / V2-H-01 identified.

---

## 7. What the adversarial tests exposed

**Passing — the model produced a defensible outcome on adequate evidence: 16 of 18.** T-01, T-02, T-03, T-05, T-06, T-07, T-08, T-09, T-10, T-11, T-12, T-13, T-15, T-16, T-17, T-18.

**Exposing gaps: 2 of 18.** T-14 materially, T-04 partially.

"Passing" includes the five scenarios that terminate at `DECISION BLOCKED` (T-03, T-08, T-09, T-15, T-16). Blocking on a named, closable unknown is the model behaving correctly; it is not a failure to produce an answer.

**Re-run after the 2026-09-03 repair.** All sixteen were re-run against the repaired files. **No scenario changed its substantive conclusion** — the platform is rejected, displaced or blocked in exactly the same scenarios, on exactly the same evidence. What changed is what the terminal sentence *claims*:

| Test | Before | After | Substantive change? |
|---|---|---|---|
| T-04 | `CUSTOM DEVELOPMENT PREFERRED` for the read surface | `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` → candidate set, comparative fit unevaluated | **No.** Same exit, same scope. The claim about the replacement is withdrawn |
| T-07 | `CUSTOM DEVELOPMENT PREFERRED` **or** `EXISTING ENTERPRISE PLATFORM PREFERRED` | `POWER PLATFORM — POOR FIT` → candidate set of three, none evaluated | **No.** The *"or"* was itself the tell: the model could not choose between them, and the label implied it had |
| T-08 | `BUY` / `CUSTOM DEVELOPMENT PREFERRED` | `POWER PLATFORM — POOR FIT` → candidate set; hybrid branch unchanged | **No** |
| T-09 | `CUSTOM/ENTERPRISE PLATFORM PREFERRED` for the dispatch core | `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` → candidate set; NB-07 stated on the candidates too | **No** |
| T-10 | `BUY` or `EXTEND THE EXISTING SYSTEM`, reached by conjoining four anti-patterns | Same direction, now reached by an explicit **composed disqualifier** (§3, Block D row 3) | **No — but the reasoning is now a rule** |
| T-12 | `EXISTING ENTERPRISE PLATFORM PREFERRED` | `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` → ALT-007 candidate with `INCUMBENT FIT UNEVALUATED` | **No.** The corpus evaluates no incumbent; the old label claimed otherwise |
| T-13 | `CUSTOM DEVELOPMENT PREFERRED` | `POWER PLATFORM — POOR FIT` → ALT-005 as the only class in scope | **No.** Still the corpus's most over-determined rejection |
| T-14 | `POWER PLATFORM IS ECONOMICALLY UNATTRACTIVE` → `EXTEND` or `BUY` or `PROCESS REDESIGN` | `POWER PLATFORM — ECONOMICALLY UNATTRACTIVE OR INFEASIBLE` → candidate set of six, none priced | **No.** The *"→ EXTEND or BUY"* continuation was the H-02 defect in its purest form |
| T-05, T-10 | Two id transpositions (`AP-D-053`, `DC-D-047`) | Corrected in place, with the original error named | **No** |
| T-16 | *(did not exist — the model had nowhere to put the requirement)* | `DECISION BLOCKED` on three separable grounds | **Yes — a new capability** |

**Re-run after the 2026-09-03 V2 repair.** V2 repaired the exit taxonomy and the closed outcome set (`decision-criteria.md` §2.5, §6.2). Four scenarios changed their **stated class**; **none changed its substantive conclusion**, and the two that moved off an undefined label moved onto a defined one.

| Test | V1 | V2 | Substantive change? |
|---|---|---|---|
| T-01 | class 1 **or** `COLLABORATION-PLATFORM NATIVE` — a label §6 never defined | class 1 **or** class 13 `ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED` naming ALT-003, graduation trigger mandatory | **No.** Same two branches, same evidence. The alternative branch now has a class, so a pack can no longer be forced to drop it |
| T-02 | class 2 — correct, **and contradicted by this file's own `Xr` mapping rule**, which would have emitted class 6 for a store change | class 2, with the class arithmetic stated: one scoped `Xr` (DC-D-031, analytics), one `Ri` (DC-D-030), one `Cf` (DC-D-022) | **No** — and the rule now agrees with the scenario. This is the scenario that falsified V1 |
| T-05 | class 3, falling back to `single platform + a tripwire` — a label §6 never defined | class 3, falling back to **class 2** whose named condition is the corpus's *"single platform + a tripwire, not a paper hybrid"* | **No.** The fallback was always a conditioned fit, not a terminal class |
| T-06 | class 2 **plus** `HYBRID` — a label §6 never defined; DC-D-022's depth readable as a rejection | class 2 for the application scope **plus** class 3 for the analytical responsibility; DC-D-022 stated as `Cf` feeding DC-D-088's `Ri` | **No.** Two scopes, two classes — §6.4 now states that rule |
| T-10 | `DECISION BLOCKED` → class 8 **unaccompanied**, against class 8's own definition | class 12 → **class 14 `IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED`** → class 8 | **No.** Same migration-not-remediation conclusion; it now has the class it was reaching for, and class 14 keeps Power Platform *rebuilt* in the candidate set rather than rejecting it |

**V2 bias check.** The repair moves in two directions at once, which is the test worth running. It **reduces** the exit count from 54 to 48 by refusing to call six in-platform redirects exits — that direction is *pro*-platform, so it was checked against every scenario that rejects or displaces: **T-04, T-07, T-08, T-09, T-12, T-13 and T-14 all rest on `Xp`, `Xe` or `Xr` exits that V2 did not touch**, and not one softened. It also **adds** class 13, whose effect is to stop a pack dropping the alternative branch on the commonest departmental shape — that direction is *anti*-platform. Power Platform is still rejected, displaced or blocked in **12 of 16** scenarios, the same twelve as before. No scenario gained a comparative claim: class 13's only named comparator is ALT-003 on the four shapes `data-architecture.md` §6 states positively, and class 14 keeps ALT-004 in scope rather than excluding it.

**Bias check on the repair.** The renames move in one direction only: **away from asserting that a non-Power-Platform class is preferred.** That could, in principle, introduce a *pro*-Power-Platform bias by making rejection sound softer. It does not, and the test is T-13 and T-07: both still say the platform is a **POOR FIT**, an explicit rejection class that §6 previously **did not contain at all**. The repair adds an explicit rejection vocabulary and removes an unevidenced preference vocabulary. Power Platform is rejected, displaced or blocked in **12 of 16** scenarios — T-03, T-04, T-05, T-07, T-08, T-09, T-10, T-12, T-13, T-14, T-15 and T-16 — which is the same 11 as before plus the newly added T-16.

**Re-run after the 2026-09-03 bounded gate repair (V3, `block-d-gate-repair-report.md`).** `block-d-gate.md` found that DC-D-049 and DC-D-068 remained classed `Xr` on fields naming nothing leaving the platform, that no existing scenario exercised either criterion, and constructed two adjacent cases (its A-01, A-02) that the repaired rule newly governs. V3 corrects both criteria's class (§2.5) and adds them to the corpus as **T-17** and **T-18**, so the rule that produced the error is now under permanent test rather than only under audit.

| Test | Before Repair V3 | After Repair V3 | Substantive change? |
|---|---|---|---|
| T-17 *(new)* | *(no scenario existed)* — had one been run, DC-D-049's `Xr` class would have routed through §2.5's mapping to classes 3/4/6; with no operator and no hybrid shape, class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY` was reachable for a multi-month approval process whose own documented answer is an in-platform business record | class 2 `POWER PLATFORM — FIT WITH CONSTRAINTS`, naming the business-record-plus-re-triggering-automation pattern as the condition | **Yes — a false exclusion is now prevented, not merely absent from the test set** |
| T-18 *(new)* | *(no scenario existed)* — had one been run, DC-D-068's `Xr` class would have routed the same way; class 6 was reachable for an in-platform authorization design constraint naming no off-platform destination anywhere in the criterion | class 12 `DECISION BLOCKED — MORE EVIDENCE REQUIRED` on the propagation question, or class 2 once it resolves | **Yes — same as T-17** |

**V3 bias check.** Both moves are in the same direction: **away from a false Power Platform exclusion**, which is *pro*-platform. Every scenario that rejects, displaces or blocks Power Platform on other grounds was re-checked against the two reclassifications and none rests on DC-D-049 or DC-D-068: T-04, T-07, T-08, T-09, T-12, T-13 and T-14 are unaffected, and T-16 — which cites DC-D-068 as a triggering criterion — reaches `DECISION BLOCKED` on the agent-governance and commercial grounds already stated there, not on DC-D-068's exit class, so its outcome does not change. Power Platform is rejected, displaced or blocked in **13 of 18** scenarios (the same twelve as before, plus T-18 blocked pending the propagation evidence); T-17 is a new `FIT WITH CONSTRAINTS`, not a rejection. No scenario's substantive conclusion softened, and no new comparative claim was introduced anywhere: T-17's own alternatives cell records ALT-005 and ALT-006 as `CONSTRAINED`, not preferred, and T-18 names no alternative at all.

| Test | Gap exposed | Severity |
|---|---|---|
| **T-14** | **The model can identify that an option is expensive for a given demand shape, and cannot identify which alternative is cheaper.** No comparative pricing exists in the corpus (`licensing-cost.md` LC-U-04, §7.3 item 51), so class 7 is reachable while `ALT-00X IS CHEAPER` is not. Any pack must therefore ask for comparator numbers rather than supply them. **Status after the repair: the gap is unchanged and is now *stated in the output* rather than only in this table** — the terminal outcome carries `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`, and `decision-criteria.md` §4A.1 makes that the governing default. Closing the gap requires the comparative-TCO commission (`alternatives.md` §6 item 1), not a better reading. | **HIGH** — unchanged. |
| **T-16** | **A whole requirement class could not be expressed** and would have been answered through a criterion that cannot represent it — a *silent* failure returning a confident answer to the wrong question. **Status after the repair: the criterion exists (DC-D-116), the anti-pattern exists (AP-D-068), and the model now blocks.** What remains open is upstream: no canonical file assesses agent fit in any class, and `automation-architecture.md` U-14's deferral is **unowned**. | **HIGH before the repair; now a named research commission** (`alternatives.md` §6 item 9). |
| **T-04** | The exit is clean, but the model cannot say **how much better** an alternative read surface would be, because no latency or throughput measurement exists for anything (NB-07). The exit is sound; the replacement's adequacy is unevidenced. | MEDIUM |
| **T-03, T-05** | Both depend on DC-D-036, which requires **consulting a team outside the engagement**. The model correctly blocks, but the blocking condition is organisational rather than technical, and an engagement under time pressure will be tempted to assume it away. | MEDIUM — a process risk, not an evidence gap. |
| **T-12** | The redirect is sound in reasoning and rests on a pattern the corpus itself marks as `INF` (NB-06), with **no incumbent platform evaluated anywhere**. The model can say "ask the incumbent"; it cannot say "the incumbent will do this". | MEDIUM, and honestly labelled. |
| **T-09** | Exposed the **order dependency** most sharply: evaluating platform strengths (offline capture) before platform absences (cross-region recovery commitment) yields an optimistic recommendation. §5's Step 0–1 prevents it — but only if the order is followed. | Design finding, not a gap. |
| **T-08** | Exposed a genuine **control conflict** (customer-managed keys versus audit availability) that the model must surface rather than resolve. It does. | Design finding. |

**Not tuned.** No criterion, state or exit signal was added, removed or softened to make a scenario produce a tidier answer. T-14's gap is the clearest case: it would have been easy to add a "cost efficiency" criterion with comparative states, and that would have been invention.

---

## 8. Cross-linking audit

### 8.1 Coverage

| Link direction | Result |
|---|---|
| Criteria → anti-patterns | **116 of 116** criteria reference at least one `AP-D-NNN` |
| Criteria → alternatives | **116 of 116** criteria reference at least one `ALT-NNN` — read as **candidate sets**, and 88 of them carry `COMPARATOR EVIDENCE ABSENT` (`decision-criteria.md` §4A.1) |
| Anti-patterns → criteria | **68 of 68** are referenced from at least one criterion's `Related anti-patterns` field |
| Alternatives → criteria | **11 of 11** are referenced from at least one criterion's `Related alternatives` field |
| Anti-patterns → alternatives | **68 of 68** name at least one alternative class in `Better alternatives` |
| Alternatives → anti-patterns | **11 of 11** name at least one `AP-D-NNN` in `Related anti-patterns` |
| Criteria → canonical evidence | **116 of 116** carry a `Lineage` field with file-qualified references |
| Anti-patterns → canonical evidence | **68 of 68** carry an `Evidence` field with file-qualified references |

### 8.2 Orphans

**Orphan items remaining: 0** in the sense of an item unreachable from the network.

Three items are **deliberately weakly linked**, and are recorded rather than padded:

| Item | Situation | Why it is left as is |
|---|---|---|
| `AP-D-059` composed disqualifier | Referenced from 11 criteria, but it is not *derived* from any single one — it is a property of combinations | Linking it to more criteria would misrepresent it as criterion-level. §3 is its home. |
| `ALT-008` another low-code platform | Reachable from 7 criteria, but only **one** (DC-D-108) carries evidence strong enough to trigger it | Adding trigger strength it does not have would be invention. §6 of `alternatives.md` records this as the widest gap. |
| `DC-D-113` multi-tenancy / resale | Links out normally, but its evidence base is **empty** — the corpus never closed the deferral | Recorded as an evidential absence, not filled in. |

### 8.3 Local criteria not carried: none

**Repair note (2026-09-03).** This section previously recorded `licensing-cost.md` DC-10 (AI and assistant consumption) as having **no canonical successor**, on the ground that the economics are unmodellable and the governance is preview. Both statements are true; neither justified the omission, because the corpus's agent evidence is not only economic — it is substantively governance-, security-, ALM- and operations-shaped, and none of it was carried forward.

DC-10 now has a successor: **DC-D-116** (`decision-criteria.md` §4.2), carried on the DC-D-113 pattern — the evidence that exists is encoded, the economics stay `UNKNOWN`, and the criterion **blocks** rather than guesses. Its matrix row is in §2.2, its anti-pattern is **AP-D-068**, and T-16 exercises it.

**Local criteria not carried: 0.**

The residual gap is upstream and is a **research commission**, not a Block D decision: no canonical file assesses agent fit in any class (`platform-suitability.md` and `application-architecture.md` carry zero mentions), and `automation-architecture.md` U-14 records the modality question as a deferral that **has no owner**. `alternatives.md` §6 item 9 carries it.

---

## 9. Summary

| | |
|---|---|
| Criteria in the matrix | **116** |
| `Xp` platform exits | **15** |
| `Xr` responsibility exits | **26** |
| `Xe` economic exits | **5** |
| `Xc` composed-only exits, **all eight registered in §3** | **8** |
| `Ri` in-platform redirects — **not exits** | **7** |
| `Cf` combination inputs — **not exits** | **17** |
| Rows with **no** exit evidenced (correctly `—`) | **38** |
| Direct exits (`Xp` + `Xr` + `Xe`) | **46** |
| Rows that **cannot** reject the platform (`—` + `Ri` + `Cf`) | **62 of 116** |
| Domains producing zero direct exits | **2** (Governance, ALM) |
| Rows carrying an **evidenced alternative-side signal** | **28** (`decision-criteria.md` §4A.2) |
| Rows carrying `COMPARATOR EVIDENCE ABSENT` | **88** |
| Axes supporting a **preference between candidates** | **1** (DC-D-108 deployment model) |
| Composed disqualifiers | **12** (8 from `architecture-patterns.md` §13, 4 added by Block D), each now naming a reachable §6.2 class or class pair — same 12 in `anti-patterns.md` AP-D-059 |
| Volatile or conflicted groups requiring re-verification | **10** (§4, including the service-limit group) |
| Evaluation steps, ordered and non-commutative | **10** (§5, Step 0–8 plus Step 7a) |
| Outcome classes emitted, from the closed set | **14** (`decision-criteria.md` §6.2) — every label emitted in this file appears there verbatim or as a stated abbreviation of one |
| Adversarial scenarios tested | **18** |
| Scenarios passing | **16** |
| Scenarios exposing gaps | **2** (T-14 HIGH, T-04 MEDIUM) |
| Scenarios in which Power Platform is rejected, displaced or blocked | **13 of 18** (6 rejected or displaced · 7 blocked pending evidence) |
| Orphan items | **0** (3 deliberately weakly linked, §8.2) |
| Cross-link coverage | 100% in all eight directions (§8.1) |

**The most important thing this matrix says** is in the **62 of 116 rows that cannot reject the platform** — 38 dashes, 7 in-platform redirects and 17 combination inputs — and in its §5 ordering. The corpus supports **disqualification** far better than **preference**: it can say with evidence that a requirement puts a workload outside the platform, and it cannot say with evidence which alternative is faster, cheaper or better. A decision model built on it should be confident when rejecting, explicit about conditions when accepting, and honest that "which alternative wins" is an engagement calculation the research does not contain. *(Corrected 2026-09-03: this sentence said "79 dashes", the pre-taxonomy figure, against 38 in the table above it.)*

`Research Status: CANONICAL` — Block D review 2026-09-03 returned `PASS WITH CORRECTIONS`; the bounded repair of H-01, H-02, H-03, H-04, M-01, M-02, M-07 and L-01 as they touch this file is recorded in `block-d-repair-report.md`. The independent **re-review** 2026-09-03 returned `FAIL` (`block-d-re-review.md`) and this file carried the **V2 repair** of both gate-blocking findings — the exit-class legend and mapping rule (§1), 26 re-tagged rows and 10 filled cells (§2), the `Xc` registration rule (§3), Steps 4 and 7 (§5), scenarios T-01/T-02/T-05/T-06/T-10 (§6), the V2 before/after and bias check (§7) and §9 — recorded in `block-d-repair-v2-report.md`. **Re-review V2** (`block-d-re-review-v2.md`) returned `FAIL` (HIGH 1, gate-blocking MEDIUM 1), and the **Block D gate** (`block-d-gate.md`) independently confirmed both and one dependent finding. This file carries the **bounded V3 gate repair** of all three — DC-D-049 and DC-D-068's reclassification (§1, §2), the per-row `Xc` outcome mapping (§3), Step 7's mapping restatement (§5), scenarios T-17 and T-18 and the V3 bias check (§6, §7), and §9 — recorded in `block-d-gate-repair-report.md`. **Gate recheck performed:** `block-d-final-gate-recheck.md` returned `FINAL BOUNDED GATE RECHECK: PASS` with `NEW GATE-BLOCKING FINDINGS: 0`. Canonicalized 2026-09-03; lineage in `canonical-manifest.md`.

---
