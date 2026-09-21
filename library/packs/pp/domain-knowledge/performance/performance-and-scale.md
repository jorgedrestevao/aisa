# Performance and scale — meters, envelopes and the limits of what a limit proves

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Which meter binds first for this workload, and is the requirement inside or outside it?*
- *What must be validated before this commitment, and at what fidelity?*
- *Is this figure a hard boundary, a quota, a throttling behaviour, or somebody's performance hypothesis?*
- *What can a documented limit exclude here, and what can it never prove?*

This file states **what the platform's documented operating boundaries can and cannot settle about a
workload's runtime behaviour**. It does not decide which option wins — that belongs to the decision model
(`decision-tree.md` S4–S6).

---

## 1. What this is for · `decision-grade`

Performance questions arrive as one word — *"will it scale?"* — and are not answerable in that form. They
become answerable only after two moves, in this order:

1. **Classify the workload**, because a different meter binds in each shape. You cannot size what you have
   not classified.
2. **Separate the kinds of statement** that a sizing conversation mixes together — a structural ceiling, an
   entitlement allowance, a runtime rejection protocol, a measurement, a hypothesis, an obligation, and a
   business-level objective. Collapsing any two of them produces a confident, wrong verdict.

The dominant failure in this domain is not that the platform is slow. It is that a workload of one shape
was designed as another shape, and that a number belonging to one of the seven categories was read as
belonging to another.

## 2. When it becomes material · `decision-grade`

- A **volume, frequency, freshness, concurrency or latency** figure appears in the requirement.
- A **commitment** is about to be made — an SLA, an SLO, a go-live date resting on peak behaviour.
- The workload has a **growth horizon** materially different from its launch state.
- One **identity** carries many users' traffic (an integration account, a service principal, a public site).
- The requirement contains the words *live*, *immediately*, *real-time*, or *all of them at once*.
- A **peak** exists — a shift start, a month-end, a campaign, a season.

## 3. Classify the workload before sizing it · `decision-grade`

| Shape | Defining question | What actually binds |
|---|---|---|
| **Interactive read** | Do many people need to *look at* business data quickly? | Client-side payload and round-trip count; the delegation boundary |
| **Interactive write** | Do many people need to *record transactions* through a UI? | Per-identity data-service protection; the connector throttle |
| **Background volume** | Does a large set of records need processing with no person waiting? | Request entitlement; the execution-time meter; run duration |
| **Event stream** | Must high-frequency events be absorbed as they arrive? | Trigger mechanism latency; concurrency control; the presence or absence of a broker |
| **Public / external read** | Must unauthenticated or external users browse content? | Site cache floor and capacity-driven node scaling; the *single* service identity all their traffic lands on |
| **Compute** | Does one step need real calculation rather than orchestrating calls? | Nothing here sizes it — no surface exposes a compute-sizing dial |

**Apply in order; the first *yes* fixes the shape.**

1. Does one step need **real computation** — optimisation, simulation, media processing, large-matrix maths —
   rather than orchestrating calls? → **compute**. No sizing exercise can produce a number for this shape,
   because no dial exists; the computation must be carried by something that does expose one. Note also
   that in-database extension code runs on a shared sandbox and its execution time is charged to the
   triggering request's protection budget, so relocating the computation *inside* the platform does not
   create headroom.
2. Do **unauthenticated or high-volume external** users read the data? → **public / external read**. The
   binding constraint is that all of that traffic reaches the data service through **one** identity, and no
   application-side tuning changes it.
3. Are events arriving **faster than the trigger mechanism's own interval**? → **event stream**. This is a
   mechanism problem, not a tuning problem.
4. Is there **volume with no waiting human**? → **background volume**.
5. Otherwise it is **interactive**, splitting on whether transaction rate or payload dominates.

**Why the order matters.** Shapes 1, 2 and 6 have no in-shape remedy: no amount of app tuning, indexing or
parallelism moves them. Discovering the shape late converts an architecture question into a rework
question.

## 4. The five independent meters · `decision-grade`

There is no single "platform performance limit". Five systems are evaluated **separately**, each with its
own scope and its own window:

| Meter | Unit counted | Scope of evaluation | Window |
|---|---|---|---|
| **Request entitlement** | actions / CRUD operations | the **owning identity**, or the automation object where a capacity licence is assigned | long (daily) sliding, plus a short burst window |
| **Data-service protection** | requests, combined execution-seconds, concurrent requests | the **acting authenticated identity**, *per web server* | short rolling |
| **Connector throttle** | calls | the **connection object** — shared by every artefact using it | per connector, seconds to a minute |
| **Client-side capacity** | rows and bytes delivered, memory, parallel requests | one **user session / device / browser** | continuous |
| **Structural limits** | actions, nesting depth, array size, control and screen counts | one **artefact definition** | static |

**The binding constraint is the smallest of the five — and it is usually not the one people plan against.**
In this baseline it is normally the connector throttle or the data-service protection meter, **not** the
daily entitlement that licence conversations centre on. Sizing against the daily figure alone is sizing
against the wrong meter.

Three consequences that are documented, not inferred:

- **Batching is not a way around the entitlement meter.** The vendor states the two meters are evaluated
  separately and that operations accrue against entitlement whether or not they travel in a batch. Batching
  trades the *request* meter for the *execution-time* meter, so a large batch can pass one and fail the
  other.
- **The data-service protection figure is not a usable throughput number**, because it applies *per web
  server* and the server count is undisclosed and licence-dependent. Effective throughput is therefore
  unknowable in advance by arithmetic; the design has to be **tolerant** of rejection rather than sized
  against a ceiling. A non-production or trial environment class can be allocated the minimum, so a proof
  of concept there measures a different platform than production.
- **Two further meters bind specific shapes and are routinely forgotten**: content throughput, metered in
  **bytes per window** by the automation owner's performance profile — with roughly a fiftyfold spread
  between the lowest and highest profiles, so ownership is a throughput decision; and the runtime-endpoint
  concurrency ceiling on inbound calls.
  > Documented reading · read 2026-09-04 · re-verify: VS-03 (design time, and on any licence change)

**A throughput requirement is therefore not expressible in one unit.** It must be stated in five — plus the
far end's own capability, because the weakest system in the chain sets the result — at the **peak** and at
the **horizon**, not at the average and not at launch.

## 5. The seven-way separation · `decision-grade`

These seven are different kinds of statement. Collapsing any pair produces a false verdict.

| # | Kind | What it **is** | What it is **not** |
|---|---|---|---|
| 1 | **Published hard boundary** | A documented structural ceiling on an artefact definition or a mechanism. A design either fits inside it or does not | **Not evidence of performance.** Also not purchasable and not tunable — the remedy is decomposition or a different mechanism |
| 2 | **Quota / entitlement** | An *allowance* of work per window, attached to an identity or an object, commercial in nature | **Not a throughput guarantee.** It says how much you are permitted, never how fast the service will go |
| 3 | **Throttling behaviour** | The runtime *protocol* when a rate is exceeded: rejection with a retry hint, then slowing, then — on sustained breach — automatic disablement | **Not a limit.** It is what happens at one, and the design must implement the back-off and a visible busy state |
| 4 | **Measured workload** | This engagement's own observed consumption, dated, and scoped to an environment class and a data volume | **Not transferable.** Not to another engagement, another tenant, or another environment class |
| 5 | **Performance hypothesis** | An untested expectation — *"the list will open acceptably"*, *"the nightly job will finish"* | **Not a fact and never a commitment.** It is a thing to test |
| 6 | **Validation requirement** | The obligation that a named claim be evidenced, at a named fidelity, before commitment — with a budget and an environment prerequisite | **Not satisfied by the limit arithmetic that produced it.** A documentation review is not a measurement |
| 7 | **End-to-end SLA / SLO** | The business flow's own objective, composed across **every** dependency on the path, including the ones the customer operates | **Not the platform's service availability.** A published platform uptime figure is not an end-to-end availability figure, and a recovery objective is not an uptime figure either |

**The collapses, and what each one produces:**

- **1 + 5** → *"it violates no documented limit, therefore it is fast enough."* A design that is compliant
  and too slow, discovered at go-live.
- **2 + 1** → *"the allowance is the ceiling."* Sizing against a purchasable allowance while an unpurchasable
  structural ceiling or a connector window binds first.
- **2 + 7** → *"we bought the allowance, so the throughput is committed."* An SLA with no basis.
- **3 + 1** → *"the rejection is the limit."* Wrong remedy: a quota is answered commercially or by
  distributing identities, a throttle by reducing the per-connection call rate or splitting connections, a
  hard boundary only by redesign.
- **4 + 1** → a measured figure from one engagement generalised into a platform threshold. That is invention
  wearing evidence's clothes.
- **6 + 1** → an approval granted on evidence that does not address the claim.
- **7 + platform availability** → a contractual availability commitment resting on the vendor's service
  figure, while the real objective is set by the **worst** dependency on the path. Composite availability is
  analysed per business flow, never per platform. External systems' recovery objectives are explicitly
  outside the platform's own resiliency commitments.

## 6. Quota, throttle and hard boundary — three mechanisms, three remedies · `decision-grade`

| | Mechanism | Remedy that works | Remedy that does not |
|---|---|---|---|
| **Quota / entitlement** | An allowance per identity or object per window; allowances do not roll over between windows and do not pool across environment or tenant | Reduce request *count* (avoid running at all via trigger conditions; project and filter to collapse N calls into one); change or distribute the owning identity; assign the automation its own capacity entitlement | Batching (evaluated separately); raising in-run parallelism, which multiplies pressure on the *other* meters at the same instant |
| **Throttle** | Per-connection rate rejection with a retry hint; sustained breach ends in the artefact being **turned off** rather than erroring, and editing the artefact resets the evidence that would have explained it | Honour the back-off; reduce calls per connection; split connections; reshape queries; monitor the throttle **rate as a trend**, because a rising rate is an early warning of an outage with a fuse | Retrying harder — retries and pagination consume the same meters as real work, so a flaky dependency *increases* load |
| **Hard boundary** | A static ceiling on one artefact definition or one mechanism's contract | Decomposition; a different mechanism; moving the work out of the constrained artefact | Buying anything; tuning anything |

**Query shaping, not parallelism, is the first throughput lever**, because every meter counts *requests*.

## 7. A documented limit excludes; it does not prove · `decision-grade`

> **Limits can exclude designs. They do not prove performance.**

This is the single most important reading rule in this domain, and it is the vendor's own honest position:
each environment differs, and the published guidance for high-volume writing is explicitly *adaptive* —
back off from the service's own signals rather than calculate a safe rate in advance.

**What a documented limit CAN do:**

- **Exclude a specific design** — this expression, over this volume, on this surface, at this freshness.
  Exclusion is the one verdict limits carry by themselves.
- Identify the **binding meter**, and therefore which remedy family is even relevant.
- Identify a **reachable limit** — the consumption level the workload will hit at projected growth — and
  with it the **redesign trigger**, which is the natural unit for a dated, monitorable claim.
- Establish that a requirement is **structurally impossible** as stated (a freshness requirement below a
  non-reducible cache floor; a synchronous step longer than the synchronous window).

**What a documented limit CANNOT do:**

- Prove latency, throughput or concurrency. *No documented limit violated* is not *the vendor says this
  performs well*.
- Supply a concurrent-user figure. **None is published for any application surface.** Concurrency is
  governed instead by per-identity limits and by contention on shared identities and shared rows — which is
  why the real question is *where does many users' traffic funnel onto one identity or one row*, not *how
  many users are supported*.
- Supply an end-to-end latency figure for any path. None is published.
- Supply a write-amplification multiplier. Amplification is a property of **each solution's own
  customisation** — extension code, classic workflows, internal system requests completing a transaction,
  retries, pagination — and is never published. It is measured per engagement or it is an Unknown.
- Supply a security-model performance curve. The vendor documents that authorization complexity adds
  overhead but publishes **no numeric curve** for unit depth, team and sharing cardinality, or
  column-level security. This is an `UNKNOWN` with a test obligation, not a threshold to invent.
- Prove a cross-region recovery time. No such commitment is published.

**A documented boundary here is not evidence that another option class performs better.** This baseline
contains no empirical measurement of any alternative class — SaaS, custom or pro-code, incumbent
platforms, other low-code — so a boundary stated here supports *excluding a design*, never *preferring a
class*. Class-level comparison semantics belong to `decision-model/outcome-classes.md`.

## 8. Scale envelopes, as boundary shapes · `decision-grade`

Read each row as *"this is the shape of the boundary you must test the requirement against"*, never as a
performance characteristic.

**Application layer.**

- **Non-delegable expressions see a client-side row window, not the table.** Above it the answer is
  **silently truncated and wrong**, not slow — no runtime error, only a design-time warning, and two traps
  produce no warning at all (collection-based indirection, and sources absent from the delegable list).
  Any requirement to filter, search, sort, count or aggregate over a table that will exceed the maximum
  window must be delegable or pre-shaped server-side. The documented test is to set the row window to its
  minimum and verify the answer.
  > Documented reading · read 2026-09-04 · re-verify: VS-02 (design time, per data source)
- **Relationship traversal in one query is capped** at a small number of lookup levels — stricter offline —
  and a bounded count of expanded entities. This is a data-model constraint wearing an application limit's
  clothes.
- **Aggregation has its own separate ceiling**, distinct from the row window, and the analytical
  replication path has its own refresh window.
  > Documented reading · read 2026-09-04 · re-verify: VS-06 (design time, before any reporting commitment)
- **Definition size degrades the authoring experience before the runtime**, with a documented pathology
  around very long single formulas. The startup path is serial unless the work is moved off it.
- **The only published large-implementation reference point is a *complexity* figure** — tables and screens
  — not a user or volume figure. It is not a scale guarantee.

**External-site layer.**

- **Freshness has a non-reducible floor.** A server-side cache refresh window governs, it cannot be
  shortened, and values derived by server-side extension code are explicitly *never guaranteed* to reach
  the site promptly — the vendor calls that pattern not recommended. Clearing the cache on a busy live site
  is itself a production performance incident.
  > Documented reading · read 2026-09-04 · re-verify: VS-01 (Options, and before any freshness commitment)
- **The only scale dial is purchased capacity**, not an architectural setting, and **no relationship between
  capacity purchased and throughput delivered is published**. No request, throughput or concurrency limit
  is published for this surface at all. The second node in the traffic manager is failover, not load
  sharing.
- **Structural design thresholds exist** for file, lookup-record and role cardinality, published by the
  first-party checker; above the role threshold the vendor warns of effects on *all* pages.

**Data layer.**

- **No published size envelope** for the primary store's standard tables; the practical ceiling is
  purchased entitlement, not a technical one. Custom indexing is not self-service.
- **Per-identity protection is the real wall**, and it is per web server with an undisclosed count (§4).
  Extension code originating data operations is **exempt** from it — a genuine architectural lever, not a
  tuning trick.
- **A document/list store carries compounding penalties** as an application store: all defined columns are
  returned even when unused, so column count is a performance parameter of every read; dynamic lookup
  columns add server-side work; and the vendor instructs partitioning above a stated list-store threshold.
  > Documented reading · read 2026-09-04 · re-verify: VS-04 (design time)
- **A spreadsheet is not a relational store**, and the vendor declines to publish a transaction threshold
  for it. The absence of a threshold is not permission.
- **Analytical traffic is not isolated.** Query-endpoint reads execute under the same protection limits as
  transactional work, so reporting against the transactional store consumes the app's own budget.

**Automation and integration layer.** Envelope detail lives in
`automation/automation-mechanisms.md` and `integration/integration-mechanisms.md`. The boundaries that
change a *performance* verdict:

- **A structural ceiling on action count and nesting depth** per definition, identical across the
  comparable orchestration products, with nested/child definitions as the documented remedy on both.
- **A scheduling floor** below which recurrence cannot go, and per-connector polling intervals that are the
  real freshness constraint for polling designs.
  > Documented reading · read 2026-09-04 · re-verify: VS-14 / VC-02 (every engagement, per connector)
- **A synchronous window measured in low single-digit minutes**, inbound and outbound; above it the
  requirement itself must change to accept-and-poll or callback.
- **A long-running ceiling where the run *and its history* expire together**, so the audit trail has the
  same lifetime as the process instance — and an inactivity window after which low-frequency automation
  owned by a non-premium identity is suspended.
  > Documented reading · read 2026-09-04 · re-verify: VS-13 (Options, before any long-running design)
- **Ordering bought by serialising a trigger is lossy and irreversible**: it caps and can drop incoming
  triggers and collapses the de-batching ceiling. The documented default is to leave it off and put an
  ordered broker in front.
- **In-run parallelism defaults to sequential** — the commonest cause of *"the automation is slow"* is a
  configuration fact, not a platform limit — and raising it multiplies pressure on the connector and
  protection meters simultaneously.
- **Payload ceilings are per mechanism**, with a chunked variant, and they cover the whole message rather
  than just the file.
  > Documented reading · read 2026-09-04 · re-verify: VS-10 (design time, per stream)

**Availability layer.**

- **In-region redundancy is automatic and quantified** across multiple availability zones, with a
  near-zero recovery-point objective and a recovery-time objective inside minutes. Single-region resilience
  needs no extra architecture.
- **Cross-region recovery is opt-in, gated and asymmetric**: it requires a production environment of the
  managed class, carries a documented enablement lead time measured in days rather than minutes, consumes
  a **second full copy** of storage, **carries no
  published recovery-time commitment**, and several geographies have no pair at all. Enabling it
  **degrades** high-volume, highly parallel or latency-sensitive automation throughput — stated by the
  vendor. Several analytical and adjacent services are **not covered** by the failover.
- **Backup retention differs by environment class**, and the extended window requires the managed
  production class; trial environments are not backed up. Restore duration scales with data volume,
  especially audit data.
  > Documented reading · read 2026-09-04 · re-verify: VS-07 and VS-17 (Options, before any recovery commitment)
- **Deployment and administrative operations are themselves performance events on production** — solution
  import, publishing customisations and bulk security-structure changes are named as intensive database
  operations to keep out of business hours. Release cadence is therefore a performance requirement, and a
  frequent-release requirement that also forbids business-hours degradation is resolved by calendar, not by
  configuration.

## 9. The conflicted per-mechanism ceiling · `decision-grade`

> **The per-connection rate ceiling for the main extensibility mechanism is `CONFLICTED`.** Two
> currently-maintained vendor pages disagree by **20×**. The conflict was re-verified and remains open.

**Neither figure is carried here, on either side.** A design sized against the higher figure that is
actually capped at the lower one fails by a factor of twenty. Consequently **any option whose sizing rests
on a high-frequency custom connector is decision-blocked until measured** (blocking entry `B-08`, composed
row `CD-05`).

**And the block is symmetric.** It cuts across the platform, cloud-native and hybrid classes **equally**;
it is not a penalty against this platform. What closes it: re-read **both** current sources at the decision
date **and** measure representative workload. A documented case-by-case escalation path exists and may be
*proposed as a mitigation*; it may never be *relied on in advance*.

> Conflicted · `VC-01` / `VS-08` · decision-blocked until measured

## 10. Measurement obligations and validation fidelity · `decision-grade`

Because limits cannot prove performance, **every performance commitment carries a measurement obligation
with a cost and an environment prerequisite.** What must be established, and how:

| What | How it is established |
|---|---|
| **Peak business event volumes per event type** | From the business, at the **peak**, never the average — the process-capture output, not an estimate |
| **The request amplification per event** | Measured with first-party monitoring in a representative environment: client calls per event, extra operations caused by extension code and internal system requests, retried attempts, pages fetched. Every factor is a **measured slot**, never a quoted multiplier |
| **The owning identity of every automation**, with its licence and performance profile | Design register — because the profile, and therefore the ceiling, follows the owner and reverts on an HR event |
| **Headroom against each meter separately** | The five-unit check of §4; a design passes only if it fits **all** of them, and they do not pool |
| **Concurrency behaviour** | A tested baseline against a production-*like* environment with realistic personas — roles, locations, security configurations, data sets and activities — and realistic data volumes. There is no number to check against |
| **The funnel points** | Every place many users' traffic collapses onto one identity or one row, sized and tested individually |

**Fidelity is the part that gets skipped, and it is where the evidence fails.** The obligations are
documented:

- **Volume-test at projected peak *frequency*, not at test-data volume.** Two workloads with the same total
  volume and different frequency behave differently, and the documented failure case is precisely a test
  that passed on a handful of items and throttled on a realistic burst.
- **Test in an environment of the same class as production.** A trial or non-production class can be
  allocated the minimum server resources, so its measurements do not transfer; and where production
  behaviour depends on managed-environment, network or security controls, a test environment without them
  is not a mirror.
- **Test the migration itself** where a data migration has a window.
- **Full-scale destructive load testing against the shared service is constrained** by the vendor
  (*limit tests to avoid unintended consequences*), and the guidance elsewhere asking for stress and chaos
  testing is **unresolved against it**. Practical reading: bounded, coordinated testing is expected;
  blasting the shared service is not. So peak confidence is assembled from limit arithmetic **plus** a
  bounded pilot **plus** production throttling monitoring **plus** a documented degradation plan — not from
  a load test alone.
- **Write the performance requirement into the acceptance criteria** alongside the functional ones, with
  explicit degradation limits.
- **Security-model complexity requires its own pilot** at representative principal, share and query
  cardinality, because no curve is published.
- **A recovery objective requires a timed drill**, not a documentation review; no prescriptive recovery
  test plan exists and a drill cannot perfectly replicate a real event.

**What must be proven scales with what is being promised** — a departmental claim and a mission-critical
claim do not need the same evidence. The **ladder** of validation levels, and which level a given
commitment class requires, is decision logic and lives in `decision-tree.md` §12. This file states only
*what must be proven for each mechanism*.

**Evidence has a shelf life of its own.** Native telemetry and diagnostic retention windows are short and
the export path is gated to the managed environment class and is not lossless; run history is the only
transactional record and expires with the run. So the observability that would explain a slowdown may not
exist at the moment the question is asked, and telemetry retention is a design decision taken before
go-live, not after the first incident.
> Documented reading · read 2026-09-04 · re-verify: VS-18 and VS-19 (Options, before any observability commitment)

## 11. The missing benchmark is itself evidence · `decision-grade`

> **This baseline contains no empirical throughput, latency or concurrency benchmark for any component, from
> the vendor or from any independent source. The absence is a canonical finding, not a gap to fill.**

It has three consequences that a reasoner must carry explicitly:

1. **Every envelope verdict in this file means *no documented boundary violated*** — nothing more. The
   phrase *"the vendor says this performs well"* has no source anywhere in the baseline.
2. **There is no third-party measurement to triangulate the published limits against.** Practitioner
   sources agree directionally about which failures dominate, but their figures are unverified and must
   never be encoded as thresholds.
3. **Inventing the missing number is the failure mode with the largest blast radius**, because a fabricated
   figure is believed downstream and propagates into a proposal and then a contract. Where a decision-
   critical figure is unpublished or conflicted, the honest output is a **verification obligation** or a
   decision block closed by measurement — never an estimate.

Illustrative figures found in vendor guidance about *how to write a performance target* are examples of
target-writing, not platform characteristics, and must never be lifted out of that context.

## 12. Failure modes · `decision-grade`

> **Documented limits read as performance guarantees.** A design is declared performant because it violates
> no published boundary. The boundary was an exclusion test, not a service level; the corpus is limits-based,
> not benchmark-based. Consequence: a compliant, too-slow design discovered at go-live, with no baseline to
> compare against.

> **Sizing against a single meter.** Capacity is assessed against the daily entitlement the licence
> conversation centres on, while a connector window or the per-identity protection meter binds first — and
> batching is proposed as the way around it, which the vendor explicitly pre-empts. Consequence: throttling
> at a fraction of the assumed capacity, and the remedy is commercial and unbudgeted.

> **A non-delegable access path over a growing dataset.** The query cannot be pushed to the source, so only
> a client-side window of rows is examined and the truncated result is presented as authoritative. The
> failure is **wrong answers, not slow ones**, and the workaround of loading everything into a client
> collection keeps the ceiling and adds payload and memory cost. Consequence: trust is lost before the
> cause is found, and the remedy is a store or surface change, not tuning.

> **Inventing the number the platform does not publish.** A concurrency ceiling, an amplification
> multiplier, a security-model curve or one side of the live conflict is asserted and sized against.
> Consequence: a sizing error of up to an order of magnitude, and a commitment with no basis that no one
> downstream can validate.

> **Validation fidelity not matched to the commitment.** Static analysis treated as a functional test, a
> functional test treated as a performance test, a documentation review treated as proof of a recovery
> objective, a pilot run in an environment of a different class. Consequence: the commitment fails on first
> contact with production, and the approval was granted on evidence that never addressed the claim.

> **Sustained overload as an operational event rather than an error.** The workload does not fail loudly at
> the limit; it slows, then the artefact is turned off after a documented countdown, the notice goes to an
> individual's mailbox, and editing the artefact resets the evidence. Consequence: an outage with a fuse,
> whose warning signal — the throttle rate trend — nobody was watching.
> Documented reading · read 2026-09-04 · re-verify: VS-09 (design time)

## 13. Consequences elsewhere · `decision-grade`

- **→ architecture.** The binding meter selects the pattern family: partition across identities or
  connections; move the metered data leg to the protection-exempt in-platform mechanism; introduce a broker
  for load levelling or ordering; separate the read path from the write path. A broker changes *which* meter
  binds; it does not make a workload scalable by assertion — ingress, backlog growth, worker drain rate,
  the return-path calls and the retry burst all still need sizing. See `architecture/patterns.md`.
- **→ economics.** Two distinct couplings. **The meter that binds moves the design**: the remedy for a
  bound meter is frequently commercial — capacity or entitlement assigned to the object, a higher owner
  profile, more purchased site capacity — so a performance decision becomes a licence decision. **The meter
  that bills is not the same meter**: retries and pagination are billed as work, resilience consumes a
  second copy of storage, telemetry retention and non-production test estates are priced, and archiving is
  simultaneously a performance and a capacity lever. Cheap ownership buys workaround effort. See
  `economics/licensing-and-cost-drivers.md`.
- **→ data.** The delegation boundary is a *store* decision before it is an app decision; aggregation and
  analytical refresh windows decide whether reporting can share the transactional store at all; audit and
  index growth consume capacity that also gates restore. See `data/store-boundaries.md` and
  `data/query-and-delegation.md`.
- **→ automation.** Owner profile, retry policy, in-run parallelism, trigger concurrency and the
  synchronous window are performance parameters set at design time, several of them irreversibly. See
  `automation/automation-mechanisms.md`.
- **→ integration.** Three of the five meters are the integration meters, the throttle rate is the
  design-quality signal, and the live quantitative conflict lives on the extensibility mechanism. Every
  stream also needs a reconciliation owner. See `integration/integration-mechanisms.md`.
- **→ operations.** Peak confidence is an operational construct: throttling monitoring on trend, a
  degradation plan, a designated role owning the tenant-shared request pool, deployment windows treated as
  performance events, and telemetry whose retention was decided before go-live. Note also that first-party
  support invests a bounded number of hours in a performance case before referring it onward, so
  diagnostic capability must be owned locally. See `operations/operability-and-support.md`.

## 14. What must be verified · `decision-grade`

| Fact class | Volatility row |
|---|---|
| Per-mechanism throughput ceiling — **conflicted** | `VC-01` / `VS-08` |
| Request rate per acting identity, and the concurrency default | `VC-04` |
| Event frequency floor and trigger freshness, per connector | `VC-02` / `VS-14` |
| Delegation ceilings, per data source | `VS-02` |
| External-site cache floor and the freshness window | `VS-01` |
| Content-throughput-per-24-hours meter, by owner profile | `VS-03` |
| List-store scale threshold | `VS-04` |
| Aggregation ceiling and analytical refresh window | `VS-06` |
| Backup retention by environment class · restore windows behind the recovery objective | `VS-07` · `VS-17` |
| The over-limit disablement countdown | `VS-09` |
| Payload ceilings per mechanism | `VS-10` |
| Run-duration ceiling and the trigger-inactivity window | `VS-12` / `VS-13` |
| Telemetry and audit/diagnostic retention windows | `VS-18` / `VS-19` |
| Preview or general-availability state of anything relied on | `VC-10` |

**Dating weakness worth knowing.** The two pages carrying the only network-latency guidance and the only
deployment-window list are the oldest load-bearing sources in this domain; their *direction* is corroborated
by current material, their specifics are not vouched for. Re-read at the decision date.

**Not established in the baseline** — do not fill from general knowledge:

- Any **empirical measurement** of any component. Permanently open unless the engagement measures it.
- A **concurrent-user figure** for any surface, and per-device concurrent-request limits for mobile clients.
- The **relationship between purchased external-site capacity and delivered throughput**.
- The **security-model performance curve** (unit depth, team and share cardinality, column security).
  `UNKNOWN` by documentation, closed only by a bounded pilot at representative model complexity.
- The **actual web-server count** for an environment and how it scales. The vendor states the factors are
  not disclosed — treat as permanently open and make the design tolerant instead.
- **Protection behaviour under burst** rather than sustained load, beyond the retry-hint mechanism.
- Whether the application-request timeout envelope applies to **every** application surface or only one.
- **Agent and conversational surfaces**: request buckets and preview states are moving; where the question
  is material the output is `UNKNOWN` (`VS-20`, `VC-10`), never an inferred answer.

## 15. What not to infer · `decision-grade`

- **A boundary excludes a design; it never proves one.** Being inside a published limit is not evidence of
  speed. Say *no documented boundary violated*, and pair it with the measurement obligation.
- **A boundary excludes a *design*, not an option class.** *"This expression over this volume on this
  surface returns truncated results"* is domain knowledge. *"Therefore this platform is unsuitable"* is a
  selection verdict and belongs to the decision model.
- **A documented boundary here is not evidence that another option class performs better.** No comparative
  measurement of any alternative class exists in this baseline.
- **Platform availability is not end-to-end availability.** A service uptime figure, a recovery-point
  objective and a recovery-time objective are three different things, and none of them is a composite
  solution SLA.
- **Do not resolve the live conflict in either direction**, and do not carry either figure — including
  "provisionally".
- **Do not generalise a measurement.** A dated, scoped reading from this engagement is evidence here and
  invention anywhere else.
- **Do not read a marketing adjective as a scale figure.** *Scalable* and *highly available* on a product
  page sit alongside a limits page that publishes no throughput figure at all; the adjective is not
  evidence, and the two are only reconcilable if scale is understood as capacity-driven.
- **Do not restate the validation ladder here.** Which proof level a commitment class requires is decision
  logic (`decision-tree.md` §12).
- Profiling technique, monitor-tool usage, formula-level tuning, control-count heuristics and screen
  optimisation are **delivery practice** — `craft/` files, which are never an Options pull target and may
  never state a platform limit.
