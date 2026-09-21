# Integration mechanisms — envelope, guarantee, topology and boundary

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Which mechanism supports this guarantee, payload and network boundary at this throughput?*
- *Whose responsibility is this integration already?*
- *What happens to identity through this mediation tier?*
- *Which connectivity mechanisms support this private-network boundary, and what do they exclude?*

This file states **what each integration mechanism's documented envelope is, what guarantee it carries,
and what it fails on first**. It does not decide which option wins — that belongs to the decision model
(`decision-tree.md` S4–S6).

---

## 1. What this is for · `decision-grade`

Integration debates present as connector choices and are almost always something else: an **ownership**
question, a **network-posture** question, or a **guarantee** question. This file gives the three things a
mechanism choice needs to be defensible — the requirement dimensions that must be answered before any
mechanism is named, the topology class the answers imply, and each mechanism's envelope with the dimension
it fails on first.

**A limit excludes. Measurement proves.** Never claim a mechanism *meets* a throughput requirement merely
because a documented limit sits above the workload.

## 2. When it becomes material · `decision-grade`

- Data or events must cross a system boundary in either direction.
- A **guarantee** is required — no loss, no duplicates, ordering, replay, audit of a message.
- The path crosses a **network** boundary the platform cannot freely enter.
- A **backend** enforces per-user authorization, or forbids stored credentials.
- Something must be **atomic** across two systems.
- Another team already owns an integration capability for this class of work.

## 3. Requirement dimensions — answered before any mechanism is named · `decision-grade`

Twelve dimensions. Each is a chain: **requirement → documented constraint → architectural consequence.**

| # | Dimension | What must be answered | Consequence if unanswered |
|---:|---|---|---|
| 1 | **Volume** | Records/messages per period, **projected over the investment horizon** with a stated growth rate | The mechanism choice cannot be made; record as `Unknown`, never assume |
| 2 | **Frequency** | Same total volume — what distribution? 60,000/hour and 1,000/minute are different designs | Frequency, not volume, selects the trigger class and the buffering decision. Seasonal peaks are a first-class requirement |
| 3 | **Directionality** | Which side originates, **per stream**, not per system pair | Fixed by the **network posture of the weaker party**. Legacy systems often forbid inbound, so the documented remedy is to *invert the caller* |
| 4 | **Capability** | What each end can actually do — send, receive, transform, throttle, page, retry | **The weakest system in the chain sets the ceiling for the whole chain.** The target system's own documented or measured capability is a required input; `Unknown` here is decision-blocking for a high-frequency stream |
| 5 | **Latency** | Interactive, near-real-time or eventually consistent — with a number | Anything beyond the synchronous window is **re-shaped**, not lengthened. Microsoft's own caution: many real-time-access requests lack a strong business case, so the first move is to challenge the requirement |
| 6 | **Reliability** | At-most-once, at-least-once or effectively-once? What loss is tolerated? | A guarantee stronger than *"retry a few times and log"* **selects a transport**; it is not achievable inside the automation tool alone |
| 7 | **Consistency** | Must both sides agree at all times, or is convergence enough — over what window? | A strict-consistency requirement across a boundary is an architectural veto on the naive path (§7) |
| 8 | **Transaction** | Is there a unit of work spanning ≥ 2 systems that must succeed or fail together? | Multi-system atomicity is **not available**. Silence on this question is the most expensive omission in the domain |
| 9 | **Security** | Which identity calls, whose authorization applies, where do secrets live, what may cross? | The identity model is a **topology driver**, not a configuration detail (§8) |
| 10 | **Availability** | The availability of the **weakest link including the parts the customer operates** | Introducing a gateway or any self-hosted component converts a SaaS availability profile into a **customer-operated** one. That is an operating-model cost that belongs in the option, not a footnote |
| 11 | **Authority and operation** | Which system is the **record of truth** for the data, which **identity** the call executes as, which **role** is authorised to reprocess or reconcile, and which **mechanism** detects that it must be done | The dimension most often left implicit and the one that most often breaks the design later. Every stream declares all four; three names on a page declare none of them |
| 12 | **Operations** | How is it monitored, alerted, replayed and reconciled? | If the requirement includes *"prove what happened to message X"* or *"replay yesterday's failures"*, run history is insufficient and the design needs a durable message log or an explicit status table |

**One business goal decomposes into N *streams*, and each stream is an independent design decision.**
Counting streams rather than system pairs is what surfaces the read/write asymmetry that drives the
design. Elicit a **stream inventory** — source, target, direction, volume, frequency, latency class,
consistency class — not *"integrations with SAP"*. Per-stream verdicts are legitimate and expected; a
single verdict for a system pair is a smell. Volume and frequency being separate requirements can
legitimately produce **two** integrations for one dataset — a thin high-frequency path plus a bulk path.

**When the weak end cannot be improved there are exactly two structural moves**, and each spends a
different currency: **caching/replication spends freshness; buffering spends latency.** Name the currency
so the business decides, rather than hiding it in a technical choice. If neither can be sold, the
requirement itself must change or the weak system must be re-platformed — there is no third mechanism in
the baseline.

## 4. The ordered topology test · `decision-grade`

Apply in order; the first *yes* fixes the topology class.

1. **Is the integration responsibility already owned elsewhere in the enterprise?** (An existing ESB,
   iPaaS, API gateway, message backbone, or a system-owning team with a published contract.) →
   **EXTERNAL.** The platform consumes the published contract and integrates nothing. **This is the
   question to ask first, and the one most often skipped** (§9).
2. **Must a message not be lost, duplicated or reordered — or survive the consumer being down?** →
   **EVENT-BROKERED / QUEUE-BASED.** The transport carries the guarantee; the platform is a producer or an
   idempotent consumer, never the guarantee itself.
3. **Do ≥ 3 platform artefacts, or ≥ 2 consumer classes, need the same backend capability — or must the
   contract be versioned, rate-limited, transformed or observed independently of its consumers?** →
   **API-MEDIATED** (§6).
4. **Does the work exceed a synchronous window, or need to survive restarts?** → **ASYNCHRONOUS /
   BACKGROUND**, often composed with 2.
5. **Is the requirement to *read* reference data owned elsewhere, with acceptable source freshness and no
   need for platform data features?** → **DATA VIRTUALIZATION.** If platform data features (audit,
   row-level security, offline, search, charts) are required on that data → **REPLICATION**, and the
   synchronization risk register (§7) applies in full.
6. **Otherwise: one artefact calling one endpoint, at low volume, with a stable contract and a single
   consumer?** → **DIRECT.** This is the correct answer far more often than architects trained on
   enterprise integration expect; the vendor's own instruction is to choose the simplest approach that
   fulfils the requirement.

**Why the order matters.** Step 1 before step 6 is what stops *"we built our own integration layer"* from
becoming the default outcome; running 2–5 before 6 is what stops a broker or an API layer being added to a
two-endpoint problem. The two failure modes are symmetrical and both are documented.

## 5. Mechanism envelopes — what each fails on first · `decision-grade`

| Mechanism | Identity model | Fails first on | Decision-relevant boundary |
|---|---|---|---|
| **Standard connector** | Connection object; user, or shared/implicit | **Volume and frequency** — the throttle is per **connection**, so multiple flows sharing one connection share one quota | Usable on seeded collaboration-suite rights. Throttles differ by an order of magnitude between connectors for the same nominal volume |
| **Premium connector** | Connection; explicit directory identity, service principal, certificate or stored credential | **Licensing and identity, before throughput** | Entitlement is a precondition, not a later detail |
| **Custom connector** | OAuth 2.0 (directory recommended), generic OAuth 2, Basic, API key | **Contract management** — a field change requires republish *and* removing/re-adding the connection in every consuming app | **Count is capped and licence-dependent** — on seeded rights it can be *one*, which pushes designs toward few coarse-grained connectors, which is itself an argument for a real API gateway. Definition-file size cap; **OpenAPI 2.0 only**; REST only for apps and flows; **`client_credentials` grant is not supported**; API-key auth unavailable through the on-premises gateway. Its per-connection rate ceiling is **CONFLICTED** (§10) |
| **Generic HTTP action** | Whatever the maker configures; secrets live in the action unless externalised | **Governance** — it can reach anything, so it is the mechanism data policy most often has to block | Governed by the flow envelope: synchronous window, message ceiling, request-URL length |
| **Preauthorized HTTP with directory identity** | **Delegated** identity on behalf of the signed-in user | **Throughput, then payload shape** | The tightest throttle of any mechanism here — well below many interactive app patterns. **Base64-encodes the body; binary content is unsupported by design and may corrupt.** Home tenant only; federated-SSO resources unsupported; the `Location`-header asynchronous pattern is unsupported. Scope grants require an administrator-created consent. The documented fallback (generic HTTP or a custom connector) **changes the identity model and the governance posture** |
| **Dataverse Web API / `$batch`** | Application user / service principal, or interactive user | **Consistency scope** — atomicity stops at the Dataverse boundary | Bounded requests per batch; **no nested batches; no reads inside a change set**; change sets atomic; **abort-on-first-error unless the continue-on-error preference is set** — the default is fail-fast, so one bad row stops the rest and the caller must work out where it stopped. Bound by service protection per identity |
| **Dataverse webhook** | Header key, query-string key or configured key | **Reliability at scale** — it scales only as far as the hosted receiver can absorb the messages | Payload **truncation** above a documented size (heavy context properties stripped); short timeout; only 2xx counts as success; **retries once, and only on a narrow set of gateway-class errors**; in synchronous mode it is a **documented dual-write hazard** — the data operation rolls back but the outbound request cannot be recalled |
| **Dataverse → broker via Azure-aware plug-in** | Shared access signature | **Network posture** — *Azure-aware plug-ins do not support the platform's VNet support*, so the broker path and the private-network path are **mutually exclusive** through this mechanism today | Payload truncation, then hard failure above a second threshold. Contract type matters: **one-way/two-way relay contracts require a live listener** and eventually abandon the message, recreating the coupling the broker was meant to remove. For decoupled publishing choose **queue or topic**. Failures land in the system-jobs surface, not in flow run history |
| **Business events** | Application user for inbound invocation | **Payload size by design** — the guidance is *lightweight: only the data needed to describe the event* | Events must be catalogued to be exposed; custom events notify only on **completed** operations. Explicit misuse statement: **do not use business events for data transfer/export**. Throughput and quota are not published in the baseline |
| **Polling trigger** | Connection identity | **Cost and entitlement, before latency** — every poll consumes entitlement whether or not data changed | Predictable in timing, **unpredictable in volume** |
| **Scheduled replication / dataflows** | **A single human owner — a constraint, not a choice**; service principals cannot own them | **Ownership and ALM, before throughput** | Freshness floor in fixed increments with a bounded refresh count per day and a maximum run length; **cannot delete rows or change statuses**; the connection must be re-established manually after each deployment unless isolated in its own solution |
| **Broker (queue / topic / event / stream)** | Managed identity from a cloud worker; shared access signature from Dataverse | Nothing inside the platform's remit — the constraint moves to the broker side | Guarantees differ per service (§7). Only one of the three common services has transactions, duplicate detection **and** dead-lettering; one has **no** dead-lettering; one has no ordering, transactions or duplicate detection |
| **API gateway** | Directory identity for developer auth and backend protection; subscription keys for products | **Cost and ownership** — it is a resource with its own lifecycle, team and bill | Acts as a façade: verifies keys/tokens/certificates, **enforces usage quotas and rate limits**, transforms, caches, emits logs/metrics/traces. Tiers differ in capacity, private-network support and SLA. Can publish an API to the platform as a custom connector directly |
| **On-premises data gateway** | Customer-operated component | **Payload caps, then availability** | Requires **no inbound ports** — only outbound. Write payloads are capped **far below** the flow's own message ceiling, so naive document-oriented on-premises integration cannot pass through it at all; the bytes must travel another way. Production needs a **cluster** (single node is test-only), separate dev and prod clusters, and recovery-key custody that is itself a business risk. Only the most recent monthly releases are supported |
| **Platform VNet support** | Subnet-delegated outbound path | **Preconditions, and it breaks public calls by design** | An **outbound** control only. IP planning across **both** paired regions or failover is lost; a per-policy dedicated subnet; immutable network settings; a certificate-chain requirement many internal endpoints fail. **Enabling it requires an audit of every existing plug-in and connector URL**, and custom connectors created before delegation must be re-saved. **Identity traffic does not traverse the VNet** — only API-endpoint requests — so the identity provider must stay publicly reachable |
| **Middleware / integration platform (any vendor)** | — | — | Out of scope for the baseline's limits research; the criteria for choosing it are in §9 |

> Documented reading (payload ceilings by mechanism) · read 2026-09-04 · re-verify: VS-10 (design time, per stream)
> (flow message **100 MB**, **1 GB** chunked · gateway **2 MB** request and **8 MB** response — far below the
> flow's own ceiling, which is why naive document integration cannot pass through it · outbound webhook
> truncates at **256 KB** · the broker plug-in path strips context at **192 KB** and then fails outright ·
> **1,000** requests per batch, no nesting)
> Documented reading (gateway host minimum and network preconditions — **the preconditions are irreversible**) · read 2026-09-04 · re-verify: VS-11 (before any network commitment)

> Documented reading · read 2026-09-04 · re-verify: VS-27 (design time, per connector and per connection topology)
> (per-connection windows differ by an **order of magnitude for the same nominal volume**: list store
> **600 calls / 60 s** · governed store **6,000 calls / 300 s** · preauthorized delegated-identity HTTP
> **100 calls / 60 s**, the tightest here · relational connector **100 CRUD / 10 s** with **125** concurrent
> per connection and **300 calls / 30 s** per app user, on a **110 s** action timeout. The conflicted
> custom-connector ceiling is **not** part of this family — see §10.)

**Throughput must be expressed in three units before a mechanism is chosen** — entitlement per 24 h,
service-protection requests per identity per short window, and connector calls per connection per window.
**Pick the smallest.** The vendor's own warning is that individual connectors have their own limits, which
are often reached before the platform-level ones. Above the envelope the options are: partition across
connections or identities, batch, or move the path off connectors entirely — and **only the third is a
genuine architecture change**.

**The connection is a capacity-planning object.** Two well-behaved flows can throttle each other without
either exceeding its own budget, because the quota attaches to the connection rather than the artefact.
This is invisible in design and in single-artefact testing, and is the mechanism behind most *"it worked in
test"* throttling incidents. Enumerate which artefacts share each connection; give a stream needing
guaranteed headroom a dedicated connection, and where identity matters, a dedicated service principal.

**Bytes are metered separately from calls.** A file-moving integration is sized against the content-
throughput meter (`automation/automation-mechanisms.md` §4) and the gateway's write cap — not against the
request meters. The documented alternative shape is to move the bytes out of the pipeline entirely: pass a
reference and let the endpoints transfer directly.

## 6. When mediation is justified — and when it is not · `decision-grade`

**Five testable justifications for an API layer**, each traceable to a requirement:

1. **Reuse** — ≥ 2 consumer classes (apps, flows, agents, external systems) need the same capability.
2. **Composition / chattiness** — the client needs data from several backends per screen or per step;
   shaping the response server-side is the documented remedy.
3. **Contract and versioning** — the backend must evolve without breaking consumers.
4. **Rate limiting / caching to protect the backend** — this is the **only** documented place where
   platform-side callers can be rate-limited by policy; the automation tool has no back-pressure construct
   beyond coarse concurrency control, which has its own defect (§7).
5. **End-to-end observability** across a client operation that fans out to several backends.

Two further conditions, distinct from the five: **semantic translation** from a legacy contract, so the
legacy model does not leak into the platform's data model and into every flow; and **private-network reach
with credential isolation**, whose documented reference shape is a custom connector over a
directory-protected backend from a subnet-delegated environment, with the client secret pulled from a
vault through environment variables.

**When mediation is unnecessary complexity.** One consumer, one backend, stable contract, inside the
throttle → the layer adds a hop, a bill, a team and a deployment unit with no requirement behind it.
Wrapping an already-managed API in a second managed API duplicates contract management; consume it
instead. A gateway that only forwards is a **single point of failure and a bottleneck with no compensating
benefit**. And even where a gateway is justified, heavy logic does not belong in it — place aggregation and
domain logic in a dedicated service **behind** the gateway.

**Resemblance to a reference architecture is not a justification.** The test is *"which structure best
satisfies these requirements"*, not *"which published diagram looks similar"*.

## 7. Delivery, ordering and dedup — the guarantee is the transport's · `decision-grade`

**Delivery guarantee, ordering, duplicate detection and dead-lettering are properties of the transport.
Picking the transport is picking the failure semantics.** The most common correction: a business process
that needs ordering and no duplicates cannot use a fan-out event service, however *"event-driven"* the
requirement sounds.

A reliability requirement statement is incomplete until it answers five things: at-most/at-least/
effectively-once; ordering required, and at what scope; duplicate tolerance; poison-message destination;
replay requirement. **If any answer is *"we don't know"*, the design cannot be fixed and it becomes a
decision-blocking `Unknown`.**

**What a broker does not fix, and must be designed for:**

- **At-least-once means duplicates.** Consumer logic must be idempotent. In Dataverse the idempotency key
  mechanism is an alternate key with upsert semantics, with its own limits (`data/dataverse.md`).
- **A queue is not infinite.** If producer rate exceeds consumer rate the queue grows and latency rises.
  Monitor depth; scale consumers within safe limits, or shed work at the producer.
- **Autoscaling the consumer can just move the overload.** Bound the consumer's aggregate downstream rate
  to the *target's* documented limit — decisive when the consumer writes back into a store whose service
  protection is per identity.
- **Ordering is not preserved by default**, especially with multiple parallel consumers. Sessions, or
  partitioning by the ordering key, or order-insensitive consumers.
- **Poison messages need a destination** — a dead-letter queue with depth monitoring. **There is no
  documented in-platform dead-letter construct**; the error-handling surface is retry policy, run-after
  configuration and scopes. Treat the absence as *unsupported until verified*, and treat a poison-message
  or fail-fast requirement as an **escalation trigger** to a broker or an API layer, not something to
  approximate with variables. The closest in-platform approximations — a status table plus a scheduled
  repair pass for dead-lettering, and a dependency-health flag checked by trigger conditions for circuit
  breaking — are hand-built and must be recorded as such.
- **Coarse back-pressure only.** Concurrency knobs and a burst cap are the entire in-platform toolkit;
  there is no rate-limit policy, token bucket or adaptive throttle. *"Never exceed N calls/second to the
  target"* is not expressible — buffer, or put the limit in an API layer. And **enabling trigger
  concurrency can drop triggers and cannot be undone without deleting the trigger**, so it is not the
  remedy for a no-loss requirement.

### 7.1 Synchronization risk register · `decision-grade`

Replication is the mechanism most often adopted for convenience and most likely to become the system's
dominant failure source.

| Risk | Trigger condition | Mitigation actually available |
|---|---|---|
| **Duplicate processing** | Any at-least-once transport; any retried write | Alternate key as idempotency key + upsert, within its documented limits |
| **Lost updates / silent divergence** | Fast path only, no reconciliation | **A scheduled reconciliation pass is mandatory, not optional,** for any event-driven sync. The vendor's own reference design assumes the fast path loses updates and has the bulk path repair it. Cadence is a requirement input |
| **Conflicting writes** | Bidirectional sync without a per-field owner | Per-field ownership matrix, or single-writer-per-phase, or accept last-writer-wins **and record the acceptance** |
| **Status and deletion drift** | Dataflow-based sync | Dataflows cannot change statuses or delete absent rows; a companion flow sequenced after the dataflow is required |
| **Ordering violations** | Parallel consumers, or a queue without sessions | Sessions, partition by ordering key, or order-insensitive consumers |
| **Unbounded backlog** | Producer rate > consumer rate | Queue-depth monitoring and alerting; consumer scaling bounded by the **downstream** limit |
| **Overload displacement** | Autoscaling into a rate-limited target | Bound consumer concurrency to the target's documented per-identity limit |
| **Self-triggering loop** | Bidirectional sync, trigger not filtered | **Trigger conditions plus a provenance marker.** Filtering *inside* the logic still consumes an execution and a request per event. Note that column-filter semantics can be presence-not-change |
| **Poison message blocking** | Any queue-based consumer | Broker dead-letter queue + depth monitoring; **no in-platform equivalent** |
| **Fan-out multiplication** | More than one target environment or system | Publish once to a topic and subscribe N times; **do not clone the pipeline** |
| **Copy proliferation for reporting** | Sync driven by a reporting requirement | An analytical copy path, not operational sync (`data/store-boundaries.md`) |
| **False freshness** | Virtualization over a batch-loaded store | **Freshness is bounded by the *upstream* refresh, not by the virtualization.** Trace the requirement to the original source's cadence and record it as a cross-team dependency; if the requirement is tighter than that cadence, virtualization cannot satisfy it regardless of implementation |
| **Schema capture** | Tightly-coupled bidirectional sync adoption | The receiving data model is **mutated** by adoption. Decide with the schema change in view; prefer scoped read-only virtualization plus a narrow, explicitly-scoped write path |

**The documented synchronization shape is two mechanisms plus a reconciliation pass, not one pipeline** —
an event path for latency, a bulk path for correctness and initial load, and a reconciliation cadence for
the convergence guarantee. A design with only a fast path has no correctness guarantee; a design with only
a slow path cannot meet latency requirements.

**Synchronization becomes a *risk* rather than a mechanism at identifiable thresholds** — multiple target
environments, reporting-driven volume, bidirectional writes without field ownership, and copies whose
divergence nobody detects. When one is crossed the answer is **not a better pipeline**; it is a topology
change: a hub publishing events, virtualization instead of replication, or a dedicated analytical path.
Record which threshold triggered the change.

## 8. Consistency, atomicity and identity · `decision-grade`

**Atomicity stops at the governed store's boundary.** *"Write to the ERP and to the platform store, both or
neither"* is **not expressible**. Three choices, and the design must record which and what the failure
window looks like:

- **(a) Single-owner write** — all writes land in one system; the other is updated asynchronously from it.
- **(b) Compensating design** — explicit reversal path plus a reconciliation job.
- **(c) Relocate the orchestration** to a platform with saga support.

**System of record is assigned per entity, per field, and per lifecycle phase.** Composing a value in the
platform store, then locking it and handing authority to the incumbent system, is a legitimate documented
shape that a single-owner model cannot express. For each entity in scope record: who may create, who may
change which fields, at which phase authority transfers, and what happens to in-flight records at the
transfer. **The transfer point is where the integration lives**, and locking is what makes it safe.

**Sync scope defaults to minimum.** The vendor's own ERP reference architecture **excludes financial
posting entities from bidirectional sync by design**, to avoid a shadow ledger. Entities constituting
another system's authoritative ledger should be read or queried, not replicated bidirectionally. Require a
per-entity justification for every bidirectional entity, and treat postings and inventory ledgers as
presumptively excluded.

**Identity propagation is an integration-design fork, and it is a separate question from app
authentication.** Connecting and authenticating to a data source is documented as separate from
authenticating to the platform service. Per stream, decide and record:

| | Delegated identity | Service identity |
|---|---|---|
| Whose authorization applies at the backend | the user's | uniform, the service's |
| Throughput | spread across users | **concentrated on one identity**, and therefore on one service-protection limit set |
| Audit | per user | one actor for everything |

- Where **backend row-level authorization is a compliance requirement, delegated is mandatory** — and
  virtualization is excluded, because a virtual table cannot enforce row-level authorization or
  source-side user validation.
- Where **high throughput** is required, a service identity is needed **and must be distributed across
  several principals**.
- **Managed identity is GA for in-database plug-ins only.** Every connector-based path still needs a
  stored credential or a delegated user, and a custom connector cannot use the client-credentials grant —
  which removes the standard service-to-service OAuth flow from the connector path. A *"no stored
  secrets"* requirement therefore forces the integration into a plug-in with managed identity, or onto a
  host that supports managed identity with the platform calling it. Where connectors must be used, the
  mitigation is a service-principal or certificate connection with the secret in a vault surfaced through
  environment variables — **not elimination of the secret**. Unattended integrations must plan credential
  ownership and rotation as an operational process: record the identity, its owner and its rotation
  cadence.

**Mediation can silently change who the backend sees.** A tier in front of a per-user-authorizing backend
may cause the backend to stop seeing the user, moving authorization to a plane that may not be able to
enforce it. The plane analysis is `security/security-controls.md`.

## 9. Integration ownership — the first question · `decision-grade`

The boundary to **EXTERNAL** is crossed when any of the following is true:

1. **The integration responsibility already has an owner** and a contract exists.
2. The requirement is **B2B / EDI / partner protocol** handling.
3. **Strict cross-system transactionality or saga compensation** is required.
4. **Sustained throughput exceeds the three-meter envelope** with no natural partitioning.
5. The integration must execute **inside a network the platform cannot enter**.
6. **Message-level audit, replay or long retention** is required beyond run-history retention.
7. The integration must be **delivered and operated as code** with infrastructure-as-code and
   zero-downtime release.
8. The integration is **bulk data movement or transformation at scale**.
9. The integration must **survive its author's departure** without a licence-and-ownership migration
   exercise.

**What is *not* a reason to move the integration out** — recorded to keep the boundary honest:

- **Scale anxiety without a number.** The three meters are published; compute them. *"Scales
  effortlessly"* and *"small to medium scale"* are both positioning.
- **A preference for code.** The total-cost-of-ownership instruction cuts the other way: custom solutions
  often need a bigger budget for development, licensing and support, and the higher cost must be justified
  by business value.
- **One difficult step.** The documented answer is a **hybrid split at the step** — keep the orchestration
  and the connectors, externalise the offending capability (compute, duration, guarantee, protocol) — not
  relocating the whole integration.
- **Resemblance to a reference architecture.**

**The platform's own documented default for a new integration requirement is the simplest direct
mechanism**, and every escalation must be justified by a *named documented constraint* from §5 or a
*stated requirement* from §3 — not by preference or convention.

## 10. The conflicted ceiling · `decision-grade`

> **The per-connection rate ceiling for the custom-connector mechanism is `CONFLICTED`.** Two
> currently-maintained vendor pages disagree by **20×**. The conflict was re-verified and remains open.

**Neither figure is carried here, on either side.** A design sized against the higher figure that is
actually capped at the lower one fails by a factor of twenty. Consequently **any option whose sizing or
economics rests on a high-frequency custom connector is decision-blocked until measured** (blocking entry
`B-08`, composed row `CD-05`).

**And the block is symmetric.** It cuts across the platform, cloud-native and hybrid classes equally; it is
**not** a penalty against this platform. What closes it: re-read **both** current sources at the decision
date **and** measure representative workload. A documented case-by-case escalation path exists and may be
*proposed as a mitigation*; it may never be *relied on in advance*.

> Conflicted · `VC-01` / `VS-08` · decision-blocked until measured

## 11. Network boundary and its mutual exclusions · `decision-grade`

Three private-connectivity mechanisms exist and they are **not alternatives for the same problem**;
choosing the wrong one produces an *unsupported* configuration rather than a slow one:

| Requirement | Mechanism |
|---|---|
| On-premises source reached by apps and flows | **On-premises data gateway** |
| ETL / dataflow / analytics over a private network | **VNet data gateway** |
| Everything else outbound and private | **Platform VNet support** |

**Documented mutual exclusions and collisions:**

- **Broker path vs private egress.** *Azure-aware plug-ins do not support VNet support*, so *"events out of
  the governed store to a broker"* and *"all platform egress inside my VNet"* cannot both be satisfied
  through that mechanism. The options are: publish via a VNet-supported **connector** driven from a flow
  (accepting flow-level rather than transaction-level eventing); publish from a **plug-in** (VNet-supported)
  directly to a private-endpoint-protected broker; or accept public egress for the event path with
  compensating controls. **Record which was chosen and why.**
- **VNet support vs gateway on the same connector path.** Under VNet support for the relational connector,
  the on-premises gateway is **not supported** — a design cannot mix them on one path.
- **Protocol decides the network path.** A legacy remote-call protocol cannot traverse the VNet data
  gateway, so that integration style **requires** an on-premises gateway estate with all its payload caps
  and operating model. An OData-shaped path can use HTTPS, can be fronted by a gateway for directory
  authentication, and is the documented way to obtain directory identity on that connector at all.
- **A private-connectivity requirement is a joint platform + network-engineering workstream** with an owning
  role on each side and a URL audit, not a toggle (§5).

**Legacy systems with no programmable surface push the integration to UI automation**, framed as an
exception with a named fallback. Before accepting it, establish that no API, database, file or message
interface exists **and that the owning team will not build one**. Where chosen, the design must include an
availability check, an explicit UI-change fragility risk, and the per-bot entitlement cost. See
`automation/automation-mechanisms.md` §9.

## 12. Asynchronous integration needs a status resource · `architecture-grade`

The synchronous window is not extendable, but the **asynchronous** outbound window is far longer. That is
the sanctioned escape and **it changes the contract**:

- **Respond-then-continue** — answer the caller inside the window and keep working, with a status record
  the client polls.
- **Require the backend to implement the accepted-plus-location-plus-retry-after contract.** This is a
  **requirement on the other team** and must be raised with them, not assumed.
- **Or move the work behind a queue and a worker.**

**Every asynchronous integration defines a status entity** with at least: correlation id, state, attempt
count, last error, timestamps, and — where a broker is used — the broker's message identifier for
cancellation. The status resource is simultaneously the UX affordance, the retry ledger, the reconciliation
input and the audit trail. It is also the honest in-platform answer to *"we need dead-lettering"* (§7).

**Every user-triggered integration must specify** the timeout budget, the progress affordance, the cancel
affordance, and the failure message. *"Instant"* triggers are documented as not truly instant, and
concurrency at peak must be estimated: a per-user integration multiplied by the user count **is a
throughput requirement in disguise**.

**Trigger class carries a different dominant risk each way.** Scheduled work fails by overlapping itself —
attach a runtime-versus-interval alert. Event-driven work fails by spiking — attach a spike plan with
throttling or rate limiting. Record the trigger class per stream with its matching operational control.

## 13. Consequences elsewhere · `architecture-grade`

- **→ resilience and operations.** Throttling rate is a **design-quality signal**: a rising rate means
  either the design or the capacity is wrong, and the log must separate throttling from other faults for
  anyone to tell which. Combined with automatic disablement after sustained breach, a rising throttle rate
  is an **early warning of an outage with a fuse**, not merely a performance note. Monitoring must alert on
  **trend**. Every stream needs the reconciliation pass itself: the role authorised to run it, the identity
  it runs as, and the mechanism that detects the divergence. See
  `operations/operability-and-support.md`.
- **→ performance.** The three meters here are three of the five in
  `performance/performance-and-scale.md`; the conflicted ceiling (§10) is the baseline's one live
  quantitative conflict.
- **→ economics.** Premium connectors, gateway estate at scale, an API gateway resource and broker
  messaging units are all separate cost drivers with their own meters. Gateway-at-scale cost is an **open
  item** in the baseline. See `economics/licensing-and-cost-drivers.md`.
- **→ governance.** The generic HTTP mechanism is the one data policy most often has to block; connector
  permissibility posture is **valid on its date only** and per environment. See
  `governance/governance-and-environments.md`.
- **→ security.** Identity propagation, egress and secret custody land in `security/security-controls.md`.
- **→ data.** Store-side authority, integrity and virtualization-vs-replication boundaries are
  `data/store-boundaries.md`; the alternate-key limits that make idempotency possible are
  `data/dataverse.md`.
- **→ ALM.** Custom connectors ship in their own solution first; dataflow connections must be
  re-established after deployment unless isolated; connector URLs need re-saving after subnet delegation.
  See `alm/release-and-lifecycle.md`.

## 14. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Connector and integration execution envelope — per-connection call rate and concurrency, per-user app rate, action and client timeouts, inbound runtime-endpoint concurrency | `VS-27` |
| Customer-operated estate currency — the supported-release window for self-hosted components, and any allowlist or service-tag refresh cycle | `VS-28` |
| Payload ceilings by mechanism | `VS-10` |
| Gateway host minimum and network preconditions (**irreversible**) | `VS-11` |
| Per-mechanism throughput ceiling — **conflicted** | `VC-01` / `VS-08` |
| Connector and service permissibility posture, per environment | `VC-03` |
| Request rate per acting identity | `VC-04` |
| Trigger polling intervals, per connector | `VS-14` / `VC-02` |
| External and hybrid service consumption cost (gateway-at-scale is an open item) | `VC-08` |
| Preview / GA state of any capability relied on | `VC-10` |

**Dating weakness worth knowing.** The connector reference pages carrying the most decision-relevant
throttle figures are the weakest-dated load-bearing sources in the baseline. Re-read them at the decision
date.

**Not established in the baseline** — do not fill from general knowledge:

- **Safe outage/backlog envelope and business invariants under prolonged far-side failure** in tightly-
  coupled bidirectional sync. Keep `UNKNOWN`; require a bounded failure/recovery test plus explicit
  reconciliation rules before approving critical bidirectional synchronization.
- **Quota envelopes for two of the three broker services.** Selection evidence exists; sizing evidence does
  not.
- **Throughput and quota for the business-events mechanism.**
- Whether any in-platform **dead-letter or circuit-breaker** construct is documented (§7).
- **Gateway throughput for high-volume automation**, and gateway-at-scale cost.
- **No measurement anywhere.** This domain reasons entirely from published limits. Any statement resembling
  *"this will be fast enough"* is unsupported by the baseline.

## 15. What not to infer · `decision-grade`

- **A documented limit above the workload is not evidence the mechanism meets the requirement.** Limits
  exclude; measurement proves. This is the single most important rule in this file.
- **A capability absence is not a verdict.** *"No in-platform dead-letter construct"* is domain knowledge;
  *"therefore unsuitable"* is selection logic and belongs to the decision model.
- **A documented boundary here is not evidence that another option class performs better.** Middleware and
  integration-platform products are outside the baseline's limits research entirely; no like-for-like
  comparison exists. Where the comparison is material,
  `decision-model/outcome-classes.md`'s comparator semantics stand.
- **Do not resolve the conflicted ceiling for convenience** (§10) — not even *"we'll assume the lower
  figure to be safe"*. The blocking consequence is the finding.
- **A single verdict for a system pair is not an answer.** Verdicts are per stream (§3).
- **Vendor-side positioning is not evidence.** Where a page's own product team characterises a competing
  product's scale, the capability rows are usable and the adjectives are not.
