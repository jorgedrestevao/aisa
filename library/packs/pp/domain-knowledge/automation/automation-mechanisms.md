# Automation mechanisms — shape, envelope and failure semantics

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Which automation mechanism carries this work shape, and what fails first?*
- *What happens on retry, and what must the design guarantee?*
- *Can this wait survive a deployment or a version change?*
- *This work must be all-or-nothing — is that expressible at all?*

This file states **what each automation mechanism can carry and what it fails on first**. It does not
decide which option wins — that belongs to the decision model (`decision-tree.md` S4–S6).

---

## 1. What this is for · `decision-grade`

Automation questions arrive as products (*"can Power Automate do this?"*) and are only answerable as
**shapes**. The dominant failure in this domain is not a missing feature; it is a shape-2/3/4 requirement
built as a shape-1 workflow. Classify first, then read the mechanism envelope, then ask what fails first.

## 2. When it becomes material · `decision-grade`

- The work has **state** that must outlive one execution — a wait, a resumable step, a *"where am I"*.
- The work has **side effects** that are not safely repeatable.
- A **message** must not be lost, duplicated or reordered.
- Volume or computation must be **split and recombined**, or one step needs real computation.
- A caller **waits** for the result.
- Something must succeed or fail **atomically** across more than one system.

## 3. The four shapes, and the ordered classification test · `decision-grade`

Shapes are distinguished by **where state lives** and **what the unit of failure is** — which is what
actually decides the mechanism.

| Shape | Defining question | State lives in | Unit of failure | Natural mechanisms |
|---|---|---|---|---|
| **Workflow automation** | Does a business event need a bounded sequence of steps, usually involving people or documents? | The run instance (ephemeral) plus the business record | The whole run | Power Automate cloud flow; business process flow for the human-guidance part |
| **Process orchestration** | Does a long-lived process need to survive waits, restarts, versioning and partial completion, with a durable *"where am I"*? | An explicit, queryable process record **outside** the run | A step, individually resumable | Durable Functions; Logic Apps Standard (stateful); a Dataverse process table plus a re-triggering flow |
| **Integration orchestration** | Must a message move between systems with delivery, ordering, dedup and poison-message guarantees? | The broker | The message | Service Bus / Event Grid plus an idempotent consumer |
| **Distributed processing** | Must volume or computation be split across workers and recombined? | The job / partition ledger | The partition or the item | Durable Functions fan-out/fan-in; dataflows; Dataverse bulk APIs |

**Apply in order; the first *yes* fixes the shape.**

1. Is the primary artefact a **message that must not be lost, duplicated or reordered**? → integration orchestration.
2. Must the work be **split and recombined**, or does one step need real computation rather than calls? → distributed processing.
3. Must the process **outlive a single run** — survive a deployment, a version change, or resume mid-way after failure? → process orchestration.
4. Otherwise → workflow automation.

**Consequence.** A cloud flow is a first-class workflow-automation engine and a competent *front door* to
the other three shapes. It is **not a state store, not a broker and not a compute host**. Where the shape
is 2, 3 or 4, the design needs an explicit state store, a broker or a compute host — and the front door
may legitimately stay in Power Automate.

## 4. Metering — three independent systems, evaluated separately · `decision-grade`

A throughput requirement is not answerable in one unit. Three meters govern the same flow and are
evaluated independently:

| Meter | Unit | Scope |
|---|---|---|
| **Entitlement (Power Platform requests)** | requests / actions per 24 h | the owning identity or the flow, by licence-derived performance profile |
| **Dataverse service protection** | requests, execution seconds and concurrency per identity per short rolling window | the acting identity against Dataverse |
| **Connector throttle** | calls per **connection** per window | the connection object, shared across every artefact using it |

**The binding constraint is the smallest of the three, and it is normally the connector or the
service-protection one — not the daily figure people plan against.** Microsoft's own instruction is to
size against the **official** entitlement limits rather than the higher transition-period approximations
published on the flow-limits page, because the date on which a compliant design becomes a throttled one
is unannounced and outside the customer's control.

Two further meters bind specific shapes:

- **Content throughput** — bytes carried through run history per 24 h, metered by performance profile. A
  document-moving flow hits this long before any request meter. The documented remedy is to move the
  *bytes* out of the flow entirely and pass a reference instead.
  > Documented reading · read 2026-09-04 · re-verify: VS-03 (design time, and on any licence change)
  > (per 24 h by owner profile: **200 MB / 2 GB / 10 GB** — roughly a **fiftyfold** spread, so the same
  > design is viable or impossible depending only on who owns it)
- **Desktop-flow (RPA) throughput** — a bounded run queue with its own waiting-run depth, maximum wait,
  dispatch latency and per-run ceiling. Effective throughput is *(machines in group) ÷ (mean run
  duration)*, and the **queue** becomes the constraint long before machine count does.
  > Documented reading · read 2026-09-04 · re-verify: VS-16 (design time)
  > (queue depth **500** waiting runs; maximum wait **12 h**; dispatch latency up to **50 s**; hard
  > per-run ceiling **24 h**; auditability ceiling **10,000** logged actions per run)

**Throughput class follows the flow owner's licence, not the flow's design.** A flow uses the plan of its
owner, and reverts to the lowest performance profile if that owner leaves the organisation — losing most
of its daily ceiling through an HR event, with no edit and no design-time warning. Two documented
consequences: distributing load **across service principals** rather than a single identity is the
sanctioned mitigation for the service-protection meter; and Dataverse operations originating from
**plug-ins** are exempt from service protection entirely, which is a genuine architectural lever rather
than a tuning trick. For business-critical automation the owning identity is an architectural decision.

## 5. Mechanism envelopes — what each fails on first · `decision-grade`

| Mechanism | Fails first on | Decision-relevant boundary |
|---|---|---|
| **Power Automate cloud flow** | run duration, then the meters | A structural definition ceiling on action count and nesting depth; a hard run-duration ceiling *including pending approvals*; executes **asynchronously, after** the triggering transaction commits, so it can neither veto the operation nor guarantee its effect is visible to the next reader |
| **Logic Apps (Consumption and Standard)** | the same structural ceiling | **The action-count and nesting ceilings are identical to Power Automate's**, and the documented remedy on both is nested/child workflows. *"Too big, so move it"* is not a supported justification. The genuine differences are run duration, synchronous window, throughput mode, networking, managed identity, resource-level RBAC and Git-native ALM |
| **Dataverse plug-in / Custom API** | computation time | Runs **inside the database transaction**: an exception rolls the transaction back, so it can be immediate and unbypassable. Exempt from service protection on the data operations it originates. Tight computation ceiling. A Custom API also avoids the change-set restrictions that make a flow change set unusable with a loop |
| **Business process flow** | its published caps, and it carries no logic of its own | A human-guidance rail inside a model-driven app; complementary to a cloud flow, never an alternative. Heavy conditional wizard logic belongs in a custom page. Restricted offline |
| **Azure Functions** | plan choice, then the synchronous cap | The **hosting plan is part of the decision**: it sets the timeout, the cold-start latency and the cost shape. A hard HTTP response cap applies on every plan, so a Function is *not* an escape from the synchronous-response problem |
| **Durable Functions** | determinism and versioning discipline | The documented answer for fan-out/fan-in, sub-orchestration, monitor loops and resumable stateful progress in code. Deploying an orchestrator change with instances in flight can corrupt them and the framework's own guard is explicitly unreliable; side-by-side deployment or version-specific task hubs are the named strategies. The trade is connectivity — a dozen bindings against 1,400+ connectors — so a durable orchestration touching many SaaS systems still wants a flow at its edges |
| **Broker (Service Bus / Event Grid / Event Hubs)** | nothing inside Power Platform's remit — the constraint moves to the broker side | Guarantees are properties of the **transport**, not of the consumer (§7). Command → Service Bus. Discrete event with fan-out → Event Grid, and the consumer must be idempotent because delivery is at-least-once and unordered. Stream → Event Hubs, where a flow run per event is the wrong unit of work entirely |
| **Power Automate Desktop (RPA)** | the run queue, not UI fragility | Bounded queue depth, maximum wait, dispatch latency and per-run ceiling, plus a logged-action ceiling above which the run still executes but stops being auditable. Machine groups are unavailable in sovereign clouds |

**The synchronous-response boundary is a platform-family property, not a Power Automate weakness.** Every
mechanism here caps a synchronous caller's wait in the low single-digit minutes, and the ceilings differ
by degree, not by order of magnitude — Logic Apps Standard buys some headroom, a Function does not
meaningfully. Above that window **the requirement itself must change** to accept-and-poll or
webhook-callback. Power Automate's own escape hatch is to place the response action early and let the
remaining actions continue past the inbound limit.

> Documented reading · read 2026-09-04 · re-verify: VS-23 (design time, before any synchronous commitment)
> (cloud flow and Logic Apps Consumption **120 s** inbound and outbound · Logic Apps Standard **225 s** ·
> Functions HTTP **230 s**, which no plan removes · canvas outbound **180 s** · in-transaction extension
> **2 min**. The asynchronous outbound window is configurable to **30 days** where the backend implements
> the accepted-plus-location contract — that is the escape, and it changes the contract.)

**Run duration is the one boundary where relocation is genuinely supported by a limit** — Logic Apps
carries a materially longer single-run window than Power Automate, with a far shorter ceiling on its
*stateless* variant. Never choose a stateless workflow for a process containing waits.

> Documented reading · read 2026-09-04 · re-verify: VS-12 (Options) and VS-13 (before any long-running design)
> (cloud flow **30 days** per run *including pending approvals*; Logic Apps **90 days** stateful and
> **5 min** stateless; trigger-inactivity suspension at **90 days**)

> Documented reading · read 2026-09-04 · re-verify: VS-24 (design time, and at any definition-size review)
> (**500 actions**, **8 nesting levels** and **100,000 array items** per definition — **identical on both
> platforms**, which is what makes *"too big, so move it"* unsupported. In-run parallelism defaults to
> **1** and caps at **50**; serialising the trigger collapses de-batching from **100,000** to **100**.)

**Bulk work belongs to bulk mechanisms.** Microsoft's own remedy for volume is `CreateMultiple` / `$batch`
/ dataflows, not a different orchestrator: the flow stays inside its envelope because it issues one
request instead of N. Batching is not a free win, though — it trades the *request* meter for the
*execution-time* meter, so a large batch can pass one and fail the other. Prefer moderate batches with
parallelism for raw throughput, and treat a shift from a request-count error to an execution-time error as
the signal that batch size is now the problem. **Query shaping, not parallelism, is the first throughput
lever**: trigger conditions to avoid running at all, then projection and filtering to collapse N calls
into one. In-run parallelism defaults to sequential and has a bounded ceiling; raising it multiplies
pressure on the connector and service-protection meters at the same instant.

## 6. Long-running waits · `decision-grade`

A wait is a shape question, not a timeout setting.

- **Inside the run-duration ceiling** — the run holds the wait. The human-decision window bounding the
  in-platform approvals construct is the practical ceiling.
  > Documented reading · read 2026-09-04 · re-verify: VS-15 (Options)
- **Beyond it, the architecture changes shape.** The process record becomes the state and the flow becomes
  a *resumer*: an explicit process/task table with status and due date, driven by a scheduled flow, with
  each human interaction as a short-lived run against that record.
- **A wait held in run state does not survive a redeployment.** Deleting or republishing a flow is a
  destructive act against in-flight business processes when the state lives in the run, and run state is
  not addressable once the run ends. With state externalised, redeployment is safe — and the process
  becomes observable and reportable beyond the run history's retention, which the run history is not.

## 7. Reliability semantics — retry, idempotency, ordering, dedup · `decision-grade`

**Retry without an idempotency key duplicates the side effect.** Retry is the platform's *default*
reliability mechanism, so idempotency is a precondition for enabling it on a side-effecting action, not a
later refinement. Microsoft states plainly that retrying a non-idempotent operation corrupts data.

- **Retry defaults differ by performance profile and by product.** Resilience is therefore a property of
  the owning licence, not of the definition: the same flow retries a transient failure a couple of times
  over minutes on the lowest profile and many times over about an hour on the higher ones. A transient
  backend outage of twenty minutes is survived on one and lost on the other. A stated reliability
  requirement means retry is configured **explicitly per action**, and the profile of the owning identity
  is recorded as part of the design. *(A commonly quoted "four retries" default is Logic Apps
  Consumption's, not Power Automate's.)*
  > Documented reading · read 2026-09-04 · re-verify: VS-39 (design time, and on any change of owning identity)
  > (lowest profile **2** retries over roughly **10 min**; higher profiles **12** retries over roughly
  > **1 h** — so a twenty-minute transient outage is survived on one and lost on the other)
- **One retry owner per call chain.** A path such as app → flow → custom connector → gateway → backend has
  four places that each default to retrying; the multiplicative effect turns a transient failure into a
  self-inflicted denial of service against a system already struggling, and each attempt consumes
  entitlement. Microsoft's own guidance is to investigate how to disable or reduce the built-in mechanisms
  when implementing retry at a higher level, and to obey a response's own back-off header rather than
  computing a rate.
- **Idempotency mechanism.** In Dataverse the mechanism is an **alternate key with upsert semantics**,
  subject to its own limits (see `data/dataverse.md`); otherwise an explicit idempotency-key check before
  the write. Where the external identifier contains reserved characters, or the natural key sits on a
  secured column, a sanitised surrogate or hash is required. Where the side effect is external and
  non-idempotent — a payment, a customer-facing notification — the action goes **last** and/or behind a
  claim-check record.
- **Ordering is not a trigger setting.** Setting trigger concurrency to serialise a flow **introduces
  trigger loss** under sustained load, shrinks `SplitOn` de-batching by three orders of magnitude, and is
  a **one-way change** that cannot be reverted without recreating the trigger. Ordering at volume is a
  broker requirement: Service Bus sessions, or partition-by-ordering-key. Serialising is defensible only
  for low-volume, loss-tolerant, order-sensitive work isolated in a small child flow.
- **Deduplication is a transport property.** Among the three common brokers, only **Service Bus** offers
  transactions, duplicate detection *and* dead-lettering; Event Hubs has **no** dead-lettering; Event Grid
  has no ordering, no transactions and no duplicate detection. **Picking the transport is picking the
  failure semantics** — and the consumer must still be idempotent, because at-least-once means duplicates
  by design. Note two connector-level surprises when a flow is the consumer: a queue tier's message-size
  cap can be far below the flow's own message ceiling (forcing a claim-check for documents), and the
  connector's session cache is bounded and evicts the oldest, which is an undocumented failure mode for a
  session-per-entity design at higher cardinality.
- **There is no rollback.** A flow that fails mid-way leaves completed actions completed; nothing in the
  documentation describes an automatic undo, and a mid-loop failure over N records leaves an unknown prefix
  processed. Any multi-write design must answer three questions **in writing**: what state the world is in
  if the run fails at each step; how that state is discoverable afterwards (run history is not a business
  record and expires); and who or what completes or reverses it. If none of the three has an answer, the
  requirement needs a transaction boundary or a compensating design — not better error handling.
- **Atomicity exists only inside Dataverse**, and the flow-level construct is a **same-connector change
  set** with material restrictions (cannot loop, cannot chain outputs), which usually forces a Custom API
  instead. The moment a second system enters the unit of work, all-or-nothing is **not expressible**; the
  options are (a) collapse the unit of work into one system, (b) accept eventual consistency plus
  compensation with an explicit reversal path, a persisted in-doubt state, irreversible steps last, a human
  fallback and a reconciliation job, or (c) move the orchestration to a platform with saga support. Test
  the compensation exclusion **first**: where the business cannot tolerate *temporary* inconsistency,
  compensation is the wrong answer. Never present a compensating design to a stakeholder as transactional.
- **Trigger outage behaviour fails in opposite directions and neither is safe by default** — a polling
  trigger floods on recovery, a push trigger drops silently. For loss- or order-sensitive sources the
  recovery design is part of the architecture: a durable broker whose backlog is the broker's problem with
  redelivery bounded by a max-delivery count, or an explicit reconciliation/backfill query that can rebuild
  the missed window from the source.
- **Sustained breach turns the flow off.** Automation does not fail loudly at a meter; it slows, then is
  disabled after a documented period of consistent failure or throttling — and **editing the flow resets
  the counters**, which masks the cause rather than fixing it. Throttling *rate* is therefore a monitored
  **leading** indicator with a watching role and an alert destination, separated in the log from other faults, alerted on trend rather
  than on individual failures. Treat *"we republished it and it's fine now"* as masking, not resolution.
  > Documented reading · read 2026-09-04 · re-verify: VS-09 (design time)
  > (**14 days** of consistent failure or throttling, and separately **90 days** of trigger inactivity)
- **Dataverse's own outbound channels have different semantics, and the synchronous webhook is a
  documented dual-write hazard**: the data operation rolls back but the outbound request cannot be
  recalled, creating records downstream for a transaction that did not happen. For side effects, use an
  asynchronous channel (Service Bus, change tracking, or business events on completed operations) with an
  idempotent consumer — **never a synchronous webhook**. Payload truncation applies to both webhook and
  Service Bus paths; version the message contract before the first consumer goes live.

## 8. Human-in-the-loop and approval semantics · `decision-grade`

- A first-class, **Dataverse-backed** approvals construct exists on a **standard (non-premium)** connector,
  with several response models including sequential, reachable from Outlook, Teams and the action centre,
  and with a persisted history. Relocating this leg means hand-building a task store, a notification
  surface and a response UI. **This is the strongest single argument for splitting a process at the human
  boundary** rather than migrating it wholesale.
- **The ceiling is the run-duration window.** Escalation, reassignment and audit-retention mechanics are
  **not established** in the canonical baseline (§13). Design escalation as an explicit, visible mechanism
  — an approval action plus a parallel timeout branch and a state column — which also survives the
  run-duration ceiling because the state lives in the record. Encode the observed response *behaviours*,
  not a count of approval types; the source is internally inconsistent on the count.
- **Machine-only work gets none of this.** A process with both a human decision and a machine-heavy leg is
  a hybrid **by construction**, not a compromise. Choosing one mechanism for the whole process optimises
  the wrong half.

## 9. Interface automation (RPA) boundary · `decision-grade`

- **Attended and unattended are different architectures** with different infrastructure, entitlement and
  failure models. Unattended cost scales with **peak concurrency** (bots), not with volume or process
  count; attended avoids that dimension entirely. Desktop-flow *executions* are exempt from the request
  meter, though the orchestrating cloud flow's own actions are not.
- **The deciding constraint is the queue, not UI fragility** (§4). Sizing needs trigger rate × mean run
  duration → required concurrency, then a check that peak backlog stays inside the queue's depth and wait
  ceilings and that dispatch latency meets the business expectation. Where required concurrency exceeds the
  per-bot entitlement budget, the requirement is **not satisfiable by RPA at that latency** and must be
  re-scoped or re-platformed to an API.
- **Where a stable programmatic interface exists, prefer it.** Microsoft's stated preference for API over
  UI automation is a **stability** argument: UI automation depends on a contract the target's owner never
  committed to keeping stable. RPA is justified only when *all* hold: no API, database, file or message
  interface exists; the target's remaining lifetime does not justify building one; volume and latency fit
  the queue model; and an owner exists for selector maintenance and machine patching. Where chosen, record
  it as a **bridge with an exit condition**, not the target architecture.
- Credential and log hygiene is **admin-configured, not secure-by-default**: use the credential construct
  rather than variables or hardcoding, and match screenshot-on-error and log-upload settings to the
  sensitivity of the screens being automated.
- **Secrets have three documented homes and one anti-home.** Never pass a secret as a flow or desktop-flow
  input variable; use the desktop credential store, Key Vault, or environment variables for non-secret
  per-environment configuration only. Any design that logs action inputs for diagnostics must be checked
  for secret leakage into run history.

## 10. Corrected myths this file exists to teach · `decision-grade`

| Claim commonly made | What the evidence supports |
|---|---|
| *"Hit 500 actions? Move it to Logic Apps."* | **False.** The action-count and nesting ceilings are identical, and the documented remedy on both is decomposition. Justify a move by run duration, synchronous window, throughput mode, networking, identity, RBAC or ALM — and say which |
| *"Logic Apps is for large scale, Power Automate for small."* | Unsupported as stated, and authored by the destination product's own team. Both publish the same structural envelope; the real differences are the capability list in §5 |
| *"Add a queue and it's exactly-once."* | False without an idempotent consumer. Session ordering also has a bounded, evicting session cache in the connector |
| *"Move it to a Function to beat the 2-minute plug-in timeout."* | Only up to the Function host's own hard HTTP cap. Beyond it the asynchronous pattern is mandatory regardless of host — and the legacy Consumption plan's own timeout is one of the tightest compute ceilings in the whole option set |
| *"Durable Functions gives you versioned replay."* | Replay is exactly *why* versioning is dangerous (§5) |
| *"Application Insights gives observability for free."* | Managed-Environments-only, explicitly **not lossless**, and unavailable in sovereign clouds |
| *"The flow runs as the person who triggered it."* | Only if connections are configured that way. The **default is the owner's identity** — an invisible elevation (§12) |
| *"Plan capacity from the daily request number."* | Three meters apply and the daily one is usually not the binding constraint (§4) |
| *"RPA is a quick win with no infrastructure."* | Per-concurrent-bot entitlement, per-session Windows compute, a bounded queue, and an auditability ceiling (§9) |

## 11. Failure modes · `decision-grade`

> **Retry without an idempotency key.** A retry re-executes the side effect. Where the effect is a posting,
> a notification or an external write, the duplicate is invisible until reconciliation. Consequence: a
> reconciliation owner becomes a requirement, not a nicety.

> **A shape-2/3/4 requirement built as shape 1.** Almost every documented automation anti-pattern in the
> baseline is an instance of this one error — hand-built sagas with no durable state, giant flows, heavy
> computation inside a declarative run, simulated distributed-transaction guarantees. Classify (§3) before
> selecting.

> **Layered retry across a call chain.** Multiplied attempts hit the downstream system hardest exactly when
> it is already failing, and each attempt consumes entitlement.

> **Serialising the trigger to obtain ordering.** Trades a correctness problem for a *loss* problem, and the
> change is irreversible (§7).

> **A cloud flow as a synchronous application backend.** Acceptable as an app's fire-and-forget *command*
> channel or for short operations. For a request/response contract at user-facing volume the answers are a
> Dataverse Custom API, a Function, or Logic Apps Standard — sized against user concurrency, with a service
> principal or capacity-licensed owning identity.

> **Deep child-flow chains.** Decomposition is right; a deep chain is not free — it multiplies the
> observability problem and the entitlement consumption, and each synchronous hop re-imposes the inbound
> window. Prefer shallow decomposition with one clear orchestrator; a genuinely deep chain is the signal for
> code-first orchestration.

> **Excessive polling.** A trade-off decided per source, **not an unconditional anti-pattern**: push
> triggers cut latency and entitlement waste but exchange backlog flood for silent loss (§7). Always add a
> trigger condition on a busy source.

> **Tight synchronous coupling across many systems.** Each additional synchronous hop multiplies the failure
> surface and pins the chain to its slowest, least available participant. Decouple at the first boundary
> where availability differs.

## 12. Consequences elsewhere · `architecture-grade`

- **→ economics.** The metering **shape** decides which architectures are affordable: a per-user shape
  punishes concentrating automation on one owner; a per-flow shape rewards consolidating a high-volume
  workload into **one** flow, since stacking works per flow and not per flow group; a per-bot shape
  punishes concurrency; and a pooled shape silently caps every service-principal-owned integration in the
  tenant unless a process entitlement or designated user is attached. Read the ceiling from the shape that
  matches the owning identity. See `economics/licensing-and-cost-drivers.md`.
- **→ performance.** The three meters here are three of the five in
  `performance/performance-and-scale.md` §3. A documented ceiling **excludes** a design; it never proves the
  design performs.
- **→ integration.** Delivery guarantees, broker selection, payload ceilings, gateway paths and the network
  boundary belong to `integration/integration-mechanisms.md`. Where a *message guarantee* is the
  requirement, that file is the next pull, not this one.
- **→ security.** A flow acts as the **connection owner**, not as the person who triggered it, unless
  connections are explicitly configured otherwise. A user who can trigger a shared flow can therefore cause
  reads and writes they could not perform themselves — a legitimate, often intentional elevation that is
  invisible in the flow definition. Every shared flow needs a recorded decision: act **as the service**
  (embedded connection — deliberate elevation, and the flow must then validate authorisation itself) or act
  **as the caller** (the flow's reach is the caller's reach, and the connection cannot be shared onward).
  The enforcement-plane analysis is `security/security-controls.md`.
- **→ ALM.** Solution-awareness plus connection references are what make a flow deployable at all; a flow
  built outside a solution is an ALM dead end with no ownership fix. Deployment also needs a named
  connection owner and activator, and OAuth connection sharing effectively makes a service principal
  mandatory for automated deployment. Per-workflow version history and rollback, and zero-downtime
  deployment, are Logic Apps capabilities rather than Power Automate ones. See
  `alm/release-and-lifecycle.md`.
- **→ operations.** Native run history is short-retention and is not a business record; a durable audit or
  trend requirement is an **architectural component** — a `FlowRun`-table or export design — not a setting.
  Telemetry export carries a managed-environment dependency and is not lossless. Ownership is wired into
  throughput, identity and survival, which is why *"who owns this flow"* belongs in the architecture
  document, not the runbook. See `operations/operability-and-support.md`.
- **→ hybrid cost.** A hybrid verdict is a **second operating model**: a second billing model, a second
  deployment pipeline, a second support rota, a second identity model, and a correlation problem across the
  boundary. It must be accompanied by three named commitments — who owns the Azure resources, how the two
  halves are deployed and monitored together, and what the Azure-side run cost is. Where those cannot be
  named, the honest output is the single-platform design plus an explicit tripwire on the metric that will
  force the move. Correlation needs an explicit correlation id propagated across the boundary.

## 13. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Content-throughput-per-24-hours meter, by owner profile | `VS-03` |
| Run-duration ceiling as a work-shape boundary | `VS-12` |
| Run-duration ceiling and the trigger-inactivity window | `VS-13` |
| Trigger polling intervals, per connector | `VS-14` (also `VC-02`) |
| The human-decision window used as the in-platform boundary | `VS-15` |
| Interface-automation throughput and payload figures | `VS-16` |
| The over-limit disablement countdown | `VS-09` |
| Request rate per acting identity | `VC-04` |
| Entitlement fit of the required capability set | `VC-05` |
| Preview / GA state of any capability relied on | `VC-10` |

**Not verifiable from documentation.** No empirical throughput or latency figure exists in the baseline for
any mechanism in this file. Every performance statement here is a **published limit** — what the platform
allows — not a measurement of what it achieves under sustained load. Where performance is
decision-critical, measurement is the only closure (`performance/performance-and-scale.md`).

**Not established in the baseline** — do not fill from general knowledge:

- Approval **reassignment, timeout/escalation and audit-retention** mechanics.
- Whether Microsoft states anywhere that cloud flows lack native ordering / dedup / peek-lock of their own.
  The claim is an **absence inference** — treat as *unsupported until verified*.
- Documented behaviour of a **mid-loop failure** in an iteration construct (partial completion, and whether
  concurrency changes it).
- Any **unit- or contract-test mechanism** for a cloud-flow definition. Automation with material financial or
  compliance consequence therefore needs a test strategy that does not depend on a platform feature: a
  dedicated environment with environment-variable-driven endpoints, idempotent writes so a re-run is safe,
  and a documented manual verification path. Where that is unacceptable, the requirement is an argument for
  the code-first option, where the team's existing test tooling applies.
- Whether **process-entitlement stacking on a single flow is capped**; the sources disagree, and it matters
  only above a very high volume. Both agree the **flow-group** rule is a shared allowance with no stacking.
- **Event Grid and Event Hubs quota envelopes.** Of the three brokers only Service Bus is sized in the
  baseline, so a verdict on the other two supports **choosing** the technology, not **sizing** it.
- Whether **agent / conversational automation** changes the option set. The baseline is silent; where the
  question is material the correct output is `UNKNOWN` / decision blocked (scope-blocker `BS-03`,
  volatility row `VS-20`), never an inferred answer.

## 14. What not to infer · `decision-grade`

- **Being inside a published ceiling is not evidence the design will perform.** The rule that governs this
  — and the seven distinctions it rests on — is owned by `performance/performance-and-scale.md`; it is not
  restated here.
- **A capability absence is not a verdict.** *"No native dead-letter construct"* is domain knowledge;
  *"therefore unsuitable"* is selection logic and belongs to the decision model.
- **A documented boundary here is not evidence that another option class performs better.** The baseline
  contains no evidence evaluating incumbent workflow, BPM or integration engines at all — the
  existing-engine consideration is *reasoning about operating models*, not evidence about capability. Where
  the comparison is material, `decision-model/outcome-classes.md`'s comparator semantics stand.
- **Do not read a vendor migration page's adjectives as facts.** Capability rows are verifiable; scale
  characterisations authored by a destination product's own team are positioning.
- **Do not replace shape reasoning with a complexity tier.** *"Simple / medium / complex"* is an estimating
  device, not a mechanism selector — it cannot tell you where state lives or what the unit of failure is.
- **Do not encode "the platform is a general-purpose application backend" as a vendor position.** The
  narrower, fully-sourced statement is the one in §11.
- Build patterns, error-handling templates, expression catalogues, adaptive cards and decomposition
  heuristics are **delivery practice** — `craft/flow-craft.md`, which is not an Options pull target.
