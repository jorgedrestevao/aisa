# Architecture patterns — reusable compositions of mechanisms, and what each one imports

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Given the option class is already established, which composition of mechanisms fits these requirements — and what does that composition import?*
- *What does moving from this composition to the next one actually cost?*
- *Which composition carries the property this requirement needs — durability, ordering, replay, per-row authorization, local platform data features?*
- *This design resembles a reference architecture; what would make it justified rather than merely similar?*

This file states **what each reusable composition is made of, what property it buys, what it costs, and
what obligations it imports into other domains**. It explains compositions. It **does not decide**
which composition wins, and it never selects or renders a blueprint — selection belongs to the
decision model (`decision-tree.md` S4–S6), and the reusable output shapes generated from this
knowledge are a separate downstream layer.

---

## 1. What this is for · `decision-grade`

A pattern here is **not** a product, not a reference architecture and not an option. It is a *reusable
composition of mechanisms* — the mechanisms themselves, their envelopes and their guarantees live in
`integration/integration-mechanisms.md`, `automation/automation-mechanisms.md`,
`data/store-boundaries.md` and `application/application-surfaces.md`.

Three boundaries on this file, and they are binding:

1. **It is reachable only after an option class is established.** A comparison whose top level is "one
   structural shape versus another structural shape" is showing one option class presented as the whole
   choice. Compare option classes first (`decision-model/alternatives-register.md`,
   `decision-model/outcome-classes.md`); consult compositions second.
2. **It explains; it never selects.** Where this file says a property is not carried by a composition, that
   is a capability boundary. *"Therefore this option is unsuitable"* is a selection verdict and does not
   live here.
3. **It is not the template layer.** Templates are reusable blueprint shapes reachable from an outcome
   class. This file is the knowledge those templates are generated **from**.

**Two things earn this file its place.** First, the *simplest composition is the default* and every
escalation must name the requirement that forces it — the vendor's own instruction is to choose the
simplest approach that fulfils the requirements. Second, and more importantly:

> **What a composition IMPORTS is the most decision-bearing content here.** Every escalation beyond the
> direct composition brings governance surface, a second release route, a cost meter, a monitoring
> obligation, a recovery order and **an operating model** — role, identity, alert destination — into the
design. Those imports are what output
> shapes most often omit, and they are why a structurally elegant design turns out to be unrunnable.

## 2. When it becomes material · `decision-grade`

- A requirement names a property the direct composition does not carry: durability, ordering, duplicate
  suppression, replay, poison-message quarantine, per-row authorization on external data.
- More than one consumer needs the same backend capability, or the backend contract changes often.
- Work exceeds the synchronous window, or must survive a restart.
- Data owned elsewhere must be usable here, and the choice is between reading it and copying it.
- One step exceeds the platform's compute, duration, protocol or identity envelope.
- An integration capability is already owned by another team, with a published contract.
- Several artefacts built by several makers need controlled access to the same enterprise systems.

## 3. What "imports" means, and the six import channels · `decision-grade`

Every composition below states its imports under six headings. They are not decoration; each is a real
obligation with an owner and usually a meter.

| Channel | The question it answers |
|---|---|
| **Governance** | What new controlled asset exists, who may create and change it, who classifies the data that now sits in it, and which platform controls **stop applying** at its edge |
| **ALM** | How many release routes exist, what contract must stay version-compatible across them, and what must be rebound after every deployment |
| **Cost** | Which new meters appear, and which population they are charged against |
| **Monitoring** | What new health signal exists, where its failures land, and what correlation the design must generate itself |
| **Recovery** | What has to happen, in what order, after a restore of any participant — and who reconciles |
| **Operating model** | The **role** that intervenes, the **identity** it runs as, the permission that identity needs, the alert destination, and the recovery procedure. Where a design has not defined them, the composition carries an **operating-model requirement with a cost** — a gap in the design, closed by the design. Never an availability verdict: those belong to the decision model (README §6) |

**The platform's own controls do not cross the boundary.** Data-loss-prevention policy governs which
mechanisms a maker may use; it does not govern an external gateway, broker, worker or store. Every
composition that places a component outside the platform therefore acquires a **second governance plane**,
with its own role-based access, policy baseline, inventory, budget attribution and lifecycle.

## 4. The escalation ladder, and how compositions move · `decision-grade`

The ten compositions are not peers. Nine of them form an ordered ladder in which each rung buys a named
property at a named price; two answer *where the data lives* rather than *how the call is made*; and one
encloses the rest.

> **Lineage.** The ladder — its ordering and the mapping from requirement to moved boundary — is
> **supported synthesis over documented facts, not a vendor-published catalogue**. The individual
> constraints behind each rung are documented; the ladder shape is not. Whether the vendor publishes a
> platform-specific pattern catalogue beyond a small set of integration patterns is `UNKNOWN`, and several
> of the names below are the baseline's own.

```
Direct                    — cheapest; buys nothing, costs nothing
  ↓  two or more consumers · contract volatility · composition · rate limiting · caching · telemetry
API-mediated              — buys abstraction, versioning, policy; costs a hop, a meter, a team
  ↓  one client operation needs several backends
API facade / BFF          — buys composition + one client contract; costs a single point of failure
  ↓  producer must not depend on consumer availability, or events already exist upstream
Event-driven              — buys decoupling and freshness; costs ordering, duplicates, loop risk
  ↓  delivery guarantee · spike absorption · poison-message destination · scheduled delivery
Queue-based               — buys durability + load levelling; costs latency, idempotency work, backlog ops
  ↓  one step exceeds the platform's compute, duration, protocol, guarantee or identity envelope
Hybrid low-code + pro-code — buys capability; costs a second operating model
  ↓  work exceeds a synchronous window, or must survive restarts
Background processing     — buys responsiveness; costs a status resource and UX complexity
```

Orthogonal — *where the data lives*:

```
Data virtualization       — buys freshness-at-read and no copy; costs platform data features and per-row authorization
Data replication          — buys platform data features and local performance; costs the whole synchronization risk register
```

Enclosing all of the above:

```
Enterprise boundary       — buys governance, reuse and an owner; costs autonomy and lead time
```

**How the ladder is used.** Start at the direct composition. Climb only when a **named requirement** forces
it, and record which one. Two rungs at once is common and legitimate; skipping the justification is not.
**Coming back down is equally legitimate and almost never done** — when the requirement that forced a rung
disappears (a projected peak that never arrived; a translation layer whose migration completed), the
structure should be simplified. "More complex than the current requirement justifies" is a legitimate
finding about a live system, not a stable state.

## 5. The ten compositions · `decision-grade`

### Direct integration

*Artefact → connector → system.*

- **Intent.** One consumer needs to read from or write to one external system, and the requirement is
  satisfied by a call. No intermediary is justified and no guarantee beyond "it worked or it failed" is
  needed. Vendor-stated as the default starting point, with the exit condition stated in the same place:
  escalate only where the default does not meet the business or technical need.
- **Prerequisites** (all must hold). One consumer. Projected peak-window volume inside the mechanism's
  throttle, measured **per connection**. Stable backend contract, or acceptance of the republish-and-reconnect
  cost on every change. Completion inside the synchronous window. Transformation and business rules in
  exactly one place. "Retry per policy, then fail and log" is acceptable failure semantics. The backend's
  own authorization model suffices, or a per-user explicit connection is available.
- **Mechanisms composed.** A connector (standard, premium, custom or generic HTTP); the on-premises gateway
  where the target is in a private network, with its payload cap in the path; subnet delegation where
  private egress is required, which restricts the design to the supported mechanism list.
- **Strengths.** Lowest total cost of ownership, vendor-stated. Fastest to build and change. Fewest moving
  parts, so fewest failure modes to design for. The mechanism abstracts protocol and authentication.
- **Weaknesses.** Tight coupling to the target's availability and latency — a user-triggered synchronous
  call makes the enterprise system's uptime part of the experience. Throughput is capped by the mechanism
  rather than by the design, and the cap is **per connection**, so unrelated artefacts contend. Contract
  fragility: a backend field change forces a republish plus a coordinated reconnect in every consumer. No
  reuse — the second consumer duplicates the integration. Failure semantics are shallow, and **retry depth
  is a function of the owning identity's plan**, so the composition's resilience is not a property of the
  design.
- **Risks.** **Silent degradation into disablement** is its characteristic failure: the design that is
  correct at launch becomes throttled at multiples of that volume, and a sustained-throttling countdown
  disables the artefact. It does not get slower; it gets switched off. **Point-to-point accretion**: nobody
  decides to build an unmanageable estate — it is what this composition becomes when nobody counts.
  Licence-dependent behaviour across retry depth, loop ceilings, content throughput and request ceilings,
  all of which move with the owner's plan.
- **What it imports.** *Governance:* nothing new outside the platform — but a shared connection can become
  a production dependency whose owner leaves, so connection ownership is a real control. *ALM:* lowest
  burden with standard mechanisms; a custom connector changes the answer (import order, connection
  references, post-deployment binding). *Cost:* usually the lowest structural cost; premium or custom
  mechanisms, the gateway estate and the environment class can still dominate. *Monitoring:* run history
  plus optional telemetry export — **no message-level audit and no replay**. *Recovery:* the caller inherits
  the target's availability; a restore of either side can create divergence, and this composition provides
  no replay. *Operator:* the artefact owner, which must be a deliberate identity rather than "whoever built
  it".
- **Escalation consequence.** Every move off this rung buys a property and spends the same three things:
  a hop, a meter and someone to own the new component.
- **Lineage.** The structure and its default status are vendor-stated. The boundary conditions are
  inference over documented limits.

### API-mediated

*Platform → custom connector → API or gateway → enterprise services.*

- **Intent.** Several consumers need the same backend capability; or the contract must evolve independently
  of its consumers; or the backend must be protected, cached, transformed or observed as a managed asset
  rather than as whatever each caller happens to do.
- **Prerequisites** (any one suffices). Two or more consumer classes. Multi-source composition per client
  operation. Contract stability and versioning required. The backend needs quota, rate limiting or caching
  — this is the **only documented place to rate-limit platform-side callers**, since the automation tier has
  no rate-limit construct beyond a concurrency control with its own documented defect. End-to-end telemetry
  across the call path. Discovery with controlled consumption. Private-network reach with credential
  isolation.
- **Mechanisms composed.** Custom connector; API gateway with policy scopes, or a plain API; optionally a
  service *behind* the gateway holding domain logic; a secret store reached through environment variables;
  a higher gateway tier where a private backend or multi-region is required.
- **Strengths.** One place for the contract; one place for policy, configured rather than coded.
  Observability across the whole path, which a single-artefact design cannot provide. Reuse becomes a
  first-class outcome. Federated ownership is supported — isolated administrative access and runtime per
  team, with central oversight retained.
- **Weaknesses.** **A hop, a bill and a team.** More code-first work to develop and maintain, vendor-stated
  in its own platform instantiation. **Deployment coupling** between consumer and API, with a tested
  mitigation strategy named as a requirement. The custom connector remains a contract-change chokepoint even
  with a stable API behind it. Interface-definition version limits and per-plan custom-connector count caps
  push toward fewer, coarser connectors — which can undo the granularity the layer was meant to provide.
- **Risks.** **Single point of failure and bottleneck**, both vendor-stated, with load testing named as the
  mitigation. **Logic creep into the gateway** — the named remedy is a service behind it. A pass-through
  gateway with no policy is pure cost and pure risk. **Tier lock-in on network requirements**: a private
  backend or multi-region discovered late is a tier change, which is a cost change.
- **What it imports.** *Governance:* the mediated API becomes a governed workload asset — an accountable role, API
  inventory, access and policy baseline, budget attribution, lifecycle policy. Platform data policy governs
  use of the connector; **it does not govern the gateway or the backend**. *ALM:* two supply chains. The
  connector belongs in a deliberate solution boundary with controlled import order and reference rebinding;
  the API needs its own infrastructure-as-code and pipeline, with contract-version compatibility against the
  platform release. Where a canvas consumption workaround would create an unmanaged layer, that collides
  with a production-integrity policy forbidding unmanaged customisations and the consumer must be
  redesigned. *Cost:* API runtime, telemetry, non-production instances and an operator. *Monitoring:*
  gateway and backend telemetry routed to one queryable sink; a named API owner; a release process separate
  from the platform solution. *Recovery:* both the API layer and the consumer contract. *Operator:* an API
  owner, distinct from the maker.
- **Escalation consequence.** Moving here from direct costs a hop and a permanent second team relationship;
  moving *from* here to the facade composition adds partial-failure design; moving to the queue composition
  is a different purchase entirely — an API layer does not buffer.
- **Lineage.** Structure, justifications and both named risks are vendor-stated. Whether calls through a
  mediation tier are **metered differently** from direct calls is **not established** — so do not claim
  relief of the platform request meter, only relocation of the backend load.

### Event-driven

*Producer emits → event transport → consumers.* Symmetrically, the platform's store emits to external
consumers.

- **Intent.** Work must start when something happens, without a user asking and without polling. The
  producer should not know or care who consumes, and should not wait.
- **Prerequisites.** A state change is the natural trigger and the source can emit it. Freshness matters
  more than a schedule, and the volume is event-shaped rather than batch-shaped. The consumer's work is
  independent of the producer's transaction — post-commit. Loss and duplication tolerances are understood,
  **because the transport decides them**. Where the enterprise system must be the initiator because it
  forbids inbound connections, this is the composition the guidance names.
- **Mechanisms composed.** Row-change triggers, catalogued business events, webhook steps, or a
  transaction-aware plug-in registering a service endpoint against a broker or event service; server-side
  trigger filtering so unwanted events never become runs.
- **Strengths.** Decoupling in time and in knowledge; topics allow many listeners. Non-CRUD events are
  expressible, including events originating outside the store. Cheaper than polling for equivalent
  freshness, because polling costs a request per interval whether or not anything changed.
- **Weaknesses.** **No ordering by default**; ordering exists only on specific transports and only with a
  session or partition key. **At-least-once means duplicates**, so the consumer must be idempotent, which in
  the platform store means an alternate key. Volume is inherently unpredictable and can spike; downstream
  notification services have their own caps. **Event payload ceilings are low and lossy** — property
  stripping then hard failure on one path, truncation with a header on another, so events carrying whole
  records silently lose context. Webhook scale is the receiver's scale, with weak retry semantics on a
  narrow set of status codes.
- **Risks.** **Self-triggering loops** — the characteristic catastrophic failure, aggravated by trigger
  semantics that fire on a column's *presence* in an update payload rather than on its change. **Synchronous
  emission from inside a transaction is a dual-write hazard**: the data operation rolls back and the request
  already sent cannot be recalled. A broker contract with no listener present eventually **abandons** the
  message, re-coupling what the broker was meant to decouple. **Private-network collision**: the standard
  transaction-scoped emission mechanism does not support virtual-network egress, so mandatory private egress
  and transaction-level eventing cannot both be satisfied through it. **Events used as a data pipe** is a
  named misuse.
- **What it imports.** *Governance:* event ownership, schema and version governance, a publisher and
  subscriber inventory, and **data classification of the payload itself** — the event crosses a boundary, so
  sensitivity is assessed on the event, not only on the table. An existing enterprise event backbone takes
  precedence over a project-local one. *ALM:* the event schema is a versioned contract; publisher and
  subscriber releases must preserve compatibility, and infrastructure subscriptions and platform listeners
  have separate lifecycles. *Cost:* broker or event operations, retention and telemetry, plus an operator
  where an external backbone is introduced. *Monitoring:* **failures land in two places** — the automation
  run history for flow-consumed events, and the store's own system-job view for transaction-aware
  emissions. Both are monitored or a whole failure class is invisible. Event-rate monitoring with throttling
  and a spike mitigation plan is named as a requirement, not an option. *Recovery:* a correlation identifier
  in the event envelope; poison-event handling; retry, dead-letter and replay semantics where the transport
  supports them; replay or reconciliation from the restore boundary after any restore. *Operator:* whoever
  owns the transport and the subscription inventory.
- **Escalation consequence.** Moving to the queue composition buys the guarantee the event does not carry
  and costs latency plus idempotency work. Moving to replication is a different purchase — "keep a copy in
  step" rather than "tell me when it changes".
- **Lineage.** Structure, the loop warning, the payload ceilings, the private-egress exclusion and the
  data-pipe misuse are all vendor-stated. The proposed workaround for the private-egress collision — a
  virtual-network-supported plug-in publishing to a broker while remaining transaction-scoped — is
  **inference and `UNKNOWN`**; treat it as unsupported until verified.

### Queue-based

*Producer → queue → worker.*

- **Intent.** Arrival rate and processing rate must be allowed to differ — because of spikes, because the
  target throttles, because the consumer may be down, or because the work must not be lost. The vendor's
  framing: place a queue as a buffer between the task and the service it invokes.
- **Prerequisites.** Intermittent spikes that would overwhelm the downstream service; or a need to decouple
  intake from processing throughput for resilience and cost control. Platform-specific additions: throttling
  avoidance as the explicit goal; scheduled future delivery with cancellation; **poison-message quarantine**,
  for which no in-platform equivalent is documented; long-running work dispatched off the interactive path.
- **Mechanisms composed.** A broker queue or topic with its guarantee properties read off a property table;
  a worker (function, container, workflow, or a queue-triggered flow); a **status record** tracking each
  unit of work; a dead-letter destination plus depth monitoring.
- **Strengths.** Vendor-stated: maximises availability, because service delays do not immediately affect the
  application; maximises scalability, because queue and service counts vary independently; controls cost,
  because capacity is sized for average rather than peak load. Plus: **the guarantee lives in the transport**,
  so it is configured rather than coded; dead-lettering gives poison messages a destination — the only
  documented mechanism for that requirement in this baseline; cancellation and rescheduling become possible
  through broker sequence numbers. The vendor itself cites this as the route past an automation-tier ceiling.
- **Weaknesses.** **Latency by construction** — the vendor's own "not suitable when" names the case where
  the caller needs a low-latency synchronous response. **One-way by nature**, which is why it is usually composed with the
  background-processing status resource. **Idempotency becomes the consumer's job**, since most queue
  services deliver at-least-once. **Ordering is not preserved by default** with parallel consumers.
  Explicitly unwarranted where volume is predictably low and stable. And **a second operating model** — the
  worker is code with its own pipeline, monitoring and rota.
- **Risks.** **Unbounded backlog** where average producer rate exceeds consumer rate. **Overload
  displacement**, vendor-stated: autoscaling consumers without bounding their aggregate downstream rate only
  moves the overload downstream — decisive when the worker writes back into a store whose service-protection
  limit is **per identity**, because an elastic worker on one service principal simply relocates the
  throttling. **Message loss where durability is assumed rather than verified.** **The wrong transport for
  the guarantee** — not every event or messaging service offers dead-lettering, transactions or duplicate
  detection. Where the producer is a transaction-aware plug-in, that path's payload ceiling and
  private-egress exclusion still apply.
- **What it imports.** *Governance:* the broker is an external governed asset with access control, policy,
  **data classification of the message content now at rest in it**, retention and ownership. *ALM:* queue and
  topic configuration and worker code need infrastructure-as-code and a pipeline; the **message schema and
  the idempotency contract** are versioned alongside the platform producer and consumer. *Cost:* broker
  operations and storage, compute workers, telemetry, egress where applicable, and operational labour — and
  the service tier can be **forced** by sessions, duplicate detection or replication requirements. *Monitoring:*
  four new operational objects — queue depth, dead-letter depth, consumer lag, worker failures — with
  dead-letter depth monitored so failures can be investigated, fixed and resubmitted. *Recovery:*
  dead-letter ownership, a replay procedure, oldest-message and backlog alerts, correlation; and after a
  restore of the consumer's store, an explicit replay-or-reconcile decision **before the queue is reopened**.
  *Operator:* this is the composition that most clearly requires an operations owner outside the platform
  team. Positive import worth naming: the worker can use a managed identity, which the connector path
  cannot, so a "no stored secrets" requirement is satisfied by moving the credential-bearing leg here.
- **Escalation consequence.** Arriving here from direct or event-driven costs latency, an idempotency
  design, backlog operations and an operating model for the backlog. Moving on to the hybrid composition is not an escalation
  of the same kind — it is a capability purchase, and the two are frequently composed rather than sequenced.
- **Lineage.** The structure, all three benefits, both risks and the when-not conditions are vendor-stated.
  **Errata, 2026-09-10.** The baseline's documented instruction — define who operates the queue — stands
  and is cited. The step from it to *"therefore the composition is unavailable"* was this file's inference,
  and it is withdrawn: an undefined operating model is a requirement with a cost, and whether that cost
  blocks is the decision model's ruling (README §6).

### Hybrid low-code + pro-code

*Platform surface → automation → API, function or service → enterprise system.*

- **Intent.** The solution as a whole belongs on the platform — the users, the business records, the human
  workflow, the pace of change — but **one capability** exceeds it. Moving the whole solution is
  disproportionate; moving the capability is not.
- **Prerequisites.** One of five documented seams. **Computation** — algorithm-heavy work, where the
  expression language lacks imperative loops and mutable local state and the vendor states that complex
  logic and large-scale transformation do not belong in the automation tier. **Duration** — beyond the
  synchronous window, or beyond the in-transaction extensibility ceiling. **Protocol** — anything a connector
  cannot express. **Guarantee** — durability, ordering, dead-lettering, composed with the queue composition.
  **Identity** — managed identity is available to in-transaction extensibility and to external workers and
  **not** to connectors and flows, so "no stored secrets" is satisfied by relocating the credential-bearing
  leg. The fusion guidance names three further signals: no connector exists, integrity logic must be
  enforced, the business flow is complex and dynamic.
- **Mechanisms composed.** Two variants, and the choice matters. **In-platform pro-code** — a plug-in or
  custom API: runs *inside* the transaction so it can enforce integrity, is exempt from service-protection
  limits for its own data operations, supports managed identity and private egress — but carries a hard
  in-transaction duration ceiling that **applies even when invoked from a background operation**.
  **Out-of-platform pro-code** — a function, container or workflow behind a custom connector or a queue: no
  duration ceiling of consequence, full library access, managed identity, private endpoints — but outside
  the transaction, and a second operating model. The seam artefact is a custom connector (synchronous) or a
  queue (asynchronous).
- **Strengths.** Keeps the cheap majority cheap. Independent scaling of the expensive part, vendor-stated.
  Server-side logic becomes testable in isolation. Server-side shaping reduces client chattiness, with a
  documented performance rationale. Reuse across consumers falls out for free. **Enables requirements the
  platform cannot meet at all** — managed identity, private endpoints, long-running work, unsupported
  protocols. And the in-platform variant carries a genuine architectural lever: extensibility-originated
  data operations are exempt from service-protection limits, so identical data work can consume request
  budget in a flow and none in a plug-in.
- **Weaknesses.** **Two operating models** — two pipelines, two monitoring surfaces, two skill sets, two
  rotas. This is the dominant cost and the baseline records it as an explicit boundary condition. More
  code-first work to build and maintain. **Deployment coupling between the halves**, with the mitigation
  named as a requirement. **Skills dependency is an architecture criterion, not a staffing detail.** The
  in-platform variant's duration ceiling is hard. **Portability asymmetry**: the pro-code half and the data
  are portable, the low-code surfaces are not — so the split also splits the exit options.
- **Risks.** **The seam migrates.** Once an external service exists, the temptation is to move "just one
  more thing" until the low-code half is a thin shell — at which point the platform decision should be
  revisited honestly rather than by drift. **Cost justification is required and routinely skipped**, and the
  vendor says so in the same breath as the capability. **Silent divergence of business rules** across the two
  halves; the remedy is one enforcement site, server-side, in the store whose rules apply regardless of the
  app that wrote the data. **Environment and registration hygiene** — identity registrations must be
  separate per environment, and a cross-environment leak is easy to create and hard to notice.
- **What it imports.** *Governance:* **two governance planes.** Platform controls do not govern the external
  half; it needs its own access control, policy, inventory, budget tags and a named platform and application
  owner. Done casually — a function with a stored connection string and a connector with a shared key — the
  posture is **weaker** than a governed connector, because it sits outside the platform policy's visibility.
  *ALM:* **two supply chains are mandatory**; the connector inherits its own rebinding hazards, the external
  code needs source control, infrastructure-as-code and a pipeline, and a joint release needs sequencing
  with coordinated fix-forward or rollback. *Cost:* platform entitlement and capacity **plus** external
  consumption, monitoring, non-production environments and pro-code plus operations effort. **A hybrid
  option without this second cost model is incomplete.** *Monitoring:* telemetry on both halves and a
  correlation identifier across the seam, plus runbooks for common failure patterns and documented ownership
  spanning apps, extensibility, flows, external resources and the enterprise integration. *Recovery:* a
  recovery sequence spanning both estates. *Operating model:* a pro-code capability **and** a role
  accountable for the external resources, with the identity it runs as and its alert destination. Where the
  design defines neither, that is an operating-model requirement priced with the option.
- **Escalation consequence.** This rung's price is paid once and is mostly fixed, which is why marginal
  gains do not repay it: where one step is slow but inside the limits, optimising in place is the cheaper
  move. Where the problem is volume rather than capability, the queue composition comes first — an external
  service behind a synchronous connector does not solve throttling.
- **Lineage.** Both variants, the five seams, the strengths and the stated costs are vendor-sourced. "The
  seam migrates" and the casual-posture warning are inference over documented facts.

### Data virtualization

*Platform → virtual access → external data platform.*

- **Intent.** Data owned elsewhere must be usable inside platform experiences **without copying it**,
  represented as native tables.
- **Prerequisites.** The data is reference or read-oriented and another system is its system of record.
  **Table-level authorization is sufficient.** None of the excluded platform data features is required. The
  external store can serve interactive query volumes at the required frequency, **and its upstream refresh
  cadence satisfies the freshness requirement**. The data is modellable — a globally-unique primary key per
  table, all properties expressible as columns, relationships representable.
- **Mechanisms composed.** A virtual table plus a data provider — an in-box open-protocol provider with full
  create-read-update-delete support, a marketplace provider, or a custom provider implemented as
  extensibility code. Regular tables may hold lookups to the virtual ones, which is how editable local
  records are combined with read-only enterprise data. A cheaper non-native variant reads the source per
  screen through a connector, without the native experience.
- **Strengths.** **No copy, therefore no synchronization risk register** — the decisive advantage, and
  chronically undervalued. Single source of truth preserved. Native experience: model-driven surfaces,
  views, forms and lookups work over it. Heavy processing stays where it belongs, with only lightweight
  references locally. No storage-meter consumption for the virtualized data. The vendor presents it as
  replacing worse alternatives that suffered duplication and imperfect integration.
- **Weaknesses.** The exclusion list is the most consequential content in this composition, and it is
  vendor-documented: only organisation-owned tables are supported and user-owned security filtering is not;
  **field-level security is not supported**; row-level permissions and source-side per-user validation are
  not possible; **auditing is not supported**; search is not supported; charts and dashboards are not
  supported; the tables cannot be enabled for queues; **offline caching is not supported**; a virtual table
  cannot represent an activity and does not support business process flows; its columns cannot be calculated
  or rollup; a virtual lookup column can be displayed on a grid but cannot be filtered or sorted on; and the
  **virtual-versus-standard decision is irreversible in place**. Two further costs: attribute selection is
  ignored, so **all attributes are returned** and the payload cannot be narrowed on wide tables; and virtual
  lookup columns in a grid are explicitly slow.
- **Risks.** **False freshness** — the query is real-time against the store, but the store's actual freshness
  depends on how often the upstream systems load it. A live-looking query over a nightly-loaded store is
  stale data behind a real-time interface. **Runtime dependency**: every read is a call, so the store's
  availability and latency become the application's, and the mitigation named is to make that store highly
  available. **Query-volume amplification** from per-row lookup reads with no way to narrow the payload.
  **Authorization gap discovered late** — the pattern is chosen for elegance and the row-level exclusion
  surfaces in security review; the baseline records two independent rejections on exactly this ground.
- **What it imports.** *Governance:* the external source remains authoritative. Govern who may expose it,
  which tables and columns are visible, and **who owns the upstream availability and security contract**.
  *ALM:* provider configuration and environment bindings must be deployable and revalidated, and **the
  upstream schema is an external dependency that can break the application without any platform release**.
  *Cost:* avoids copy, storage and reconciliation cost; can import premium mechanism and upstream platform
  cost. *Monitoring:* two surfaces — from upstream ingestion through to virtual-table usage — and the
  **upstream load cadence becomes a cross-team dependency that must be owned and watched**. Data quality is
  inherited, not fixable locally. *Recovery:* no local copy means an upstream outage is immediately visible
  in the application; recovery is primarily upstream, and cache, offline or replay assumptions must not be
  invented. *Operator:* the upstream platform's owner, whose availability the design now depends on.
- **Escalation consequence.** Moving to replication buys the entire exclusion list back and costs the whole
  synchronization risk register plus a second copy of every retention, classification and erasure
  obligation. Because the virtual-versus-standard decision is irreversible in place, that move is a rebuild
  of the modelling layer, not a setting.
- **Lineage.** The definition, the providers, the modelling requirements and the whole exclusion list are
  vendor-documented, which is why this composition's limitations are unusually well evidenced. **The
  write-through variant is different**: the capability is documented as full create-read-update-delete, but
  every fetched platform instantiation is read-oriented and one recommends restricting access to read only.
  So **write-through virtualization is conditional with weak production evidence and `UNKNOWN` performance
  characteristics** — never presented as a strong production fit, and requiring scenario-specific
  validation. No general throughput or latency envelope is published; treat performance as `UNKNOWN` until
  a representative pilot.

### Data replication / synchronization

*System of record → integration → local store.*

- **Intent.** Data owned elsewhere must live locally — because platform data features are required on it,
  because local enrichment is needed, because the source cannot serve the query volume, or because latency
  or residency demands a local copy. Vendor-stated reasons: **performance** and **compliance/residency**.
  Empirically, **the virtualization exclusion list is this composition's justification list.**
- **Prerequisites.** A named item from that exclusion list, or a named residency, latency or
  source-protection requirement. Per-field ownership defined before any bidirectional design starts. And a
  **defined reconciliation pass** — the role authorised to run it, the identity it runs as, and the
  mechanism that detects the divergence it repairs. Without the pass itself the correctness guarantee does
  not exist: that is a requirement of the design, priced with it.
- **Mechanisms composed.** The documented shape is **three components, not one**: an **event path** for
  latency; a **bulk path** for correctness and initial load, using upsert on an alternate key to avoid
  duplicates; and a **reconciliation pass** that corrects whatever the fast path missed. Plus a companion
  automation for what the bulk mechanism cannot do — it cannot change row statuses and cannot delete rows
  that are absent at the source. For enterprise-resource systems the documented shape is narrower — read
  virtualization, a bidirectional write mechanism, and a query API — with **financial posting entities
  deliberately excluded from the bidirectional path**.
- **Strengths.** The full platform data feature set on the copied data — row-level security, audit, search,
  offline, charts, activities, process flows. Local enrichment with columns the source does not have. Local
  performance and residency. **Source protection**: the source is read on a schedule rather than per user
  action. Idempotency has a documented mechanism in alternate-key upsert. And **reconciliation is designed
  in**, which makes eventual correctness a property of the design rather than a hope.
- **Weaknesses.** **Two copies means two truths in the window between them**, and the vendor says to clarify
  that with business users early because the fast path is asynchronous and guarantees nothing real-time.
  Bulk-mechanism floors and gaps: a minimum increment, a bounded refresh count per day, a maximum run
  duration, no status changes, no deletion of absent rows, **cannot be owned by a service principal**, and
  the connection must be manually re-established after each deployment unless isolated in its own solution.
  **Throughput exposure**: high-frequency change activity can throttle, and the documented remedy is
  licensing — licensing as a reliability control. **Manual residue is admitted** for data-quality problems
  such as missing keys. **Fan-out does not scale**: the design is explicitly one-to-one, and more than one
  target requires a different structure. The bidirectional variant is described by the vendor itself as
  tightly coupled and synchronous, and it **mutates the local schema**. Storage cost: the copy consumes the
  most expensive of the store's meters.
- **Risks.** **Silent divergence** — the reference design *assumes* the fast path loses updates, which is
  why the reconciliation pass exists; a design without it is divergent by construction. **Self-triggering
  loops** in bidirectional sync, aggravated by presence-not-change trigger semantics. **Conflicting writes**
  without a per-field owner. **Copy proliferation for reporting**, a named anti-pattern — the remedy is a
  dedicated analytical store, not more operational sync. **Shadow system of record**, whose vendor remedy is
  exclusion by design.
- **What it imports.** *Governance:* **two controlled data estates.** Define system and field ownership,
  retention and erasure responsibility on both copies, the reconciliation owner, and who may replay failed
  changes. Sensitive data now exists in two places, so classification, retention and erasure obligations
  double — and the documented mitigation is strong and reusable: **replicate the fields, not the record.**
  *ALM:* mapping, filters, keys and reconciliation logic are versioned integration artefacts; deployment
  order matters when schemas change; the bulk mechanism's connection must be re-established per deployment
  unless isolated. *Cost:* pays twice for storage, security and operations, plus sync execution. Selective
  replication is the primary cost and risk control. *Monitoring:* failure alerting on **both** paths, a
  divergence report, and a manual-intervention runbook for key problems. *Recovery:* **restore-induced
  divergence is a first-class failure mode** — after either side is restored, pause writers and explicitly
  re-baseline, replay and reconcile before resuming. *Operator:* a reconciliation owner, and a named human
  for the bulk pipeline because service-principal ownership is unavailable there — which reintroduces the
  leaver risk this baseline treats as a runtime property.
- **Escalation consequence.** Beyond one-to-one, this composition does not extend — the structure changes to
  publish-once-subscribe-many, which is the event or queue composition with the store as one subscriber
  among several. Coming back to virtualization is only possible if every exclusion-list item has stopped
  being a requirement, and the local enrichment has to go somewhere.
- **Lineage.** The three-component design, the mechanism gaps, the ownership constraint, the throttling
  warning and the one-to-one scope statement are vendor-documented. **Failure semantics under sustained
  far-side failure in the tightly-coupled bidirectional variant are `UNKNOWN`** — the safe outage and
  backlog envelope and the business invariants are not established. Keep the unknown; require a bounded
  failure-and-recovery test plus explicit reconciliation rules before approving critical bidirectional
  synchronization.

### API facade / backend-for-frontend

*Client surface → facade → several backends.*

- **Intent.** One client operation — a screen, a step, a decision — needs data or actions from several
  backends. Doing it client-side means many round trips, many failure modes, many authentication
  configurations and many sets of paging logic inside the low-code layer.
- **Prerequisites.** A client must talk to multiple backends to perform one operation; or the client uses
  high-latency networks, which is directly relevant to mobile use; or the client's view is stable enough to
  justify a purpose-built contract; or the backend contracts are **semantically hostile** and their shape
  should not leak into the client — the anti-corruption condition, where forcing a new system to adhere to a
  legacy system's semantics corrupts an otherwise clean design; or chattiness is measurably hurting the
  client.
- **Mechanisms composed.** Custom connector → facade → several backends. The placement rule is firm: a
  gateway performing **lightweight** composition, shaping and response assembly; anything with domain logic,
  complex transformation or longer orchestration goes in a **dedicated service behind** the gateway. The
  anti-corruption variant places **translation and only translation** in the layer — no business rules, no
  orchestration.
- **Strengths.** One round trip instead of many, with a stated benefit over high-latency networks.
  Server-side shaping. **Transient-fault handling centralised** rather than distributed across clients —
  which matters because the client-side implementation would be retry policies whose depth depends on a
  licence. Reduced attack surface, with backends able to remain fully network-isolated from clients. Backends
  evolve independently of client touchpoints. Caching at the composition point. In the anti-corruption
  variant, the domain model is protected on both sides.
- **Weaknesses.** A new component to own, scale and monitor, vendor-stated. **Added latency.** **Coupling
  risk in the wrong direction** — a facade that makes backends depend on each other is worse than the
  chattiness it replaced. **A facade per consumer multiplies facades**, which collides with per-plan
  custom-connector count caps pushing the other way. Placement discipline is required or the facade becomes
  the monolith.
- **Risks.** **Single point of failure and bottleneck**, sharper here than in the mediated composition
  because *every* client operation depends on it; load testing is named as the mitigation. **Partial failure
  must be an explicit product decision** — return a partial response where missing data is acceptable, or
  fail the whole request where completeness is required, and the vendor's instruction is to **make that
  decision explicit in the policy design** so clients experience predictable behaviour. This is the single
  most commonly skipped design step. **Debuggability collapses without correlation identifiers.** **The
  facade becomes permanent by accident** — in a migration context the layer should carry an end date.
- **What it imports.** *Governance:* the facade owns a **semantic contract**, not just routing — so API
  governance, authorization-policy ownership, data-classification review and change approval. A facade
  calling backends under its own identity **replaces per-user backend authorization**, which may be exactly
  what compliance forbids. *ALM:* connector consumers inherit their rebinding hazards; the facade needs
  source control, infrastructure-as-code, a pipeline and versioned backend adapters, with anti-corruption
  mappings regression-tested. *Cost:* runtime, telemetry and operator cost, in exchange for reuse, contract
  stability and reduced client complexity. *Monitoring:* full-path telemetry, because one client operation is
  now several hops — the vendor's stated outcome is being able to detect timeout patterns, identify which
  dependency caused a partial or failed response, and alert on elevated latency or error rates. Resilience
  must be implemented, not assumed: bulkheads, circuit breaking, retries, per-request timeouts. *Recovery:*
  correlate each aggregate request across its backend calls, and ensure that recovery of one backend does
  not silently return stale or inconsistent aggregates. *Operator:* an API owner; where semantic mediation
  serves multiple platforms it belongs to the enterprise platform rather than inside one solution.
- **Escalation consequence.** Arriving here from the mediated composition adds partial-failure design and a
  sharper single point of failure. There is a cheaper move that is frequently the right one: where the
  chattiness is against a **single** backend, the vendor's own alternative is a **batch operation** on that
  backend rather than a facade.
- **Lineage.** The structural evidence — composition, anti-corruption, all considerations and the
  partial-failure instruction — is vendor-documented and strong. **The naming of this composition as a
  platform pattern is the baseline's own**; the platform instantiation describes the intent without the
  vocabulary. Treat it as structurally well-evidenced and platform-specific only by inference. Whether the
  facade's own backend calls count against the platform request meter at all is **not established**.

### Background processing

*Client surface → asynchronous processing → worker, with a status resource the client can read.*

- **Intent.** Work must happen, but the user or the calling system must not wait — because it exceeds a
  synchronous window, because it is resource-intensive, because it involves human waits, or because it must
  survive restarts.
- **Prerequisites.** The vendor's test: does the task run without user interaction, and does the interface
  need to wait for it? Tasks that require the user to wait are explicitly not appropriate background jobs.
  Named job types: resource-intensive long jobs, batch and scheduled processing, long-running workflows,
  workflows requiring asynchronous human collaboration such as approvals, and sensitive-data processing
  moved to a more secure location. Plus the hard triggers — the synchronous windows and the in-transaction
  extensibility ceiling.
- **Mechanisms composed.** Three parts, **and the third is the one that gets omitted**: dispatch (an event,
  a schedule, or an explicit request); execution (a flow, a platform-native asynchronous request, or an
  external worker); and a **status resource** — the artefact that makes the composition operable. The
  documented options for it are a status value in storage the caller can read, an endpoint the caller can
  query, or a response back to the caller. The platform-native version supports a callback URL or a
  completion event; the HTTP contract version is an accepted response with a location header, a retry hint
  and a status endpoint.
- **Strengths.** Responsiveness — background work minimises interface load, which improves availability and
  interactive response time. The platform supports "respond then continue" natively. Long outbound
  asynchronous windows are available where the backend cooperates. The store offers a first-class
  asynchronous request mechanism with documented bounded retries and exponential backoff, eliminating the
  need for a persistent connection. **Checkpointing is the documented resilience mechanism** for
  multi-step work. Composes naturally with the queue composition, which then absorbs load while restarts do
  not block the interface.
- **Weaknesses.** **The user experience gets harder, and the vendor says so** — waiting for a notification,
  refreshing, or manually checking status all increase interaction complexity; the recommended mitigations
  are a status list surface or a push notification rather than client polling. **Coordination and
  consistency problems appear** — dependencies between background tasks bring race conditions, deadlocks
  and timeouts. **More components, more cost**, stated as an explicit trade-off, potentially including a
  separate monitoring service and retry mechanism. **Polling costs**: without a retry-hint discipline the
  client hammers the status endpoint, and each poll is a request against the platform meters. **The status
  resource has a lifecycle** — it and its stored results consume storage and compute and need a retention
  policy. And **low-code clients may not honour the contract**, which applies directly when the platform is
  the *consumer* of someone else's asynchronous API.
- **Risks.** **Bottleneck displacement** — a single point in the processing chain becomes the new limit.
  **Duplicate submission**, whose documented remedy is an idempotency key, and the reasoning is worth
  keeping: the client cannot distinguish a lost response from a request that was never received.
  **Abandoned work** — cancellation must be designed, exposed on the status resource, with a decision about
  partial rollback versus a compensating action. **Recovery of multi-step work** is a compensating-transaction
  obligation, and **no saga or compensating-transaction construct is documented anywhere in the platform**
  (an inferred absence — treat as unsupported until verified). **Asynchrony does not lift the in-transaction
  ceiling**: the extensibility duration limit still applies to code invoked inside a background operation.
- **What it imports.** *Governance:* background work needs an owner, an allowed runtime and data boundary,
  and an explicit status and audit model — "fire and forget" is not a governance model. *ALM:* the status
  schema, the worker or flow version and the callback semantics must survive deployment, and **long-running
  instances may span releases**, so compatibility matters. *Cost:* status storage, polling or callback
  traffic, telemetry and possibly external compute — potentially cheaper than holding synchronous capacity.
  *Monitoring:* **the status resource is the operational surface** — it carries state, attempt counts,
  errors and correlation; expose status, age, failure and retry, and correlate request → background work →
  result. Retention of the status data must be planned. *Recovery:* define what happens to in-flight work
  during a deployment or a restore. *Operator:* whoever owns the status ledger and answers "did it work?".
- **Escalation consequence.** Where the work fits comfortably inside the window and has no restart
  requirement, the status resource and the extra components are unrepaid cost. Where the reason for
  asynchrony is capability rather than duration, the hybrid composition is the purchase; where many results
  are needed with latency mattering, the queue composition is.
- **Lineage.** The contract, the job types, the return mechanisms, the considerations and the explicit
  trade-off are all vendor-documented. The absence of a compensating-transaction construct is an inferred
  absence carried from the mechanism baseline.

### Enterprise boundary

*Platform → governed enterprise integration boundary → enterprise systems.*

> **Lineage — read this before using this composition.** This is **supported synthesis, not a
> vendor-endorsed platform pattern.** No fetched vendor page presents "the enterprise integration boundary"
> as a platform pattern. What the evidence provides is: the **components** of such a boundary, each
> documented individually; the vendor's own positioning locating certain responsibilities outside the
> platform; and repeated instructions to involve infrastructure and security stakeholders. The synthesis —
> that these constitute a single architectural boundary through which the platform reaches the enterprise,
> and that the boundary **may be owned by a non-vendor platform** — is inference. It is the
> weakest-evidenced composition in the baseline and simultaneously the most consequential for governance.
> Preserve the lineage; never restate it as official guidance; validate it against a customer reference or
> an explicit vendor statement before relying on it.

- **Intent.** Many artefacts, built by many makers at many skill levels, need controlled access to
  enterprise systems — and the enterprise needs **one place** where the contract, the identity, the rate
  limit, the audit and the change control live. Without it the estate becomes the accretion described under
  the direct composition, for which the vendor has its own uncomplimentary name.
- **Prerequisites.** Multiple artefacts, multiple makers and a governance requirement. Or — **the dominant
  condition, and it is vendor-agnostic** — an existing enterprise integration capability with a published
  contract, in which case it *is* the answer and the platform's role shrinks to experience and human
  workflow. Or requirements the vendor's own material locates outside the automation tier: trading-partner
  and business-to-business handling, bulk extract-transform-load, message-level replay and retention. Or
  network requirements the platform cannot satisfy directly, where the documented in-network mechanism is a
  self-hosted gateway deployed alongside the APIs it fronts.
- **Mechanisms composed.** Custom connectors generated from the boundary's published definitions → the
  boundary itself (an API gateway, a message backbone, an integration platform, wherever it runs) →
  enterprise systems. Governance controls sit on the **platform side** of the boundary: data policy scoping
  which mechanisms may be used per environment, environment strategy separating lifecycle stages, mechanism
  inventory, and private egress where required. The documented layered control points are tenant access and
  isolation, environment access, resource permissions, mechanism access and data policy, role-based data
  access, and the on-premises gateway.
- **Strengths.** One contract, one policy point, one audit trail. **Discovery with control** — a developer
  portal plus an export path that lets professional developers publish capabilities and citizen developers
  consume them. Federated ownership without losing central oversight. Legacy modernisation without
  migration; partner onboarding stops being per-integration. **It removes the leaver risk from the
  integration path**, moving ownership from a maker's licence and personal account to a platform team with
  resource-level access control. And it is **the only composition that can be satisfied by a non-vendor
  platform** — the baseline's antidote to assuming one cloud is automatically the answer.
- **Weaknesses.** **Lead time and autonomy loss** — every new capability now needs a boundary change owned
  by another team. Nothing in the evidence quantifies this; it is inference. **A second or third platform to
  fund and operate**, with tier decisions that lock in network and availability capabilities. **Double
  abstraction** — a connector over an API over a backend, three contracts to keep aligned. **Governance can
  become the bottleneck**, at which point makers route around it — the very failure the policy layer exists
  to prevent, made messier by its own enforcement lag, which can suspend or quarantine already-running
  artefacts. And several boundary controls are **managed-environment-gated**, so the boundary carries an
  entitlement precondition across that environment's whole population.
- **Risks.** **The boundary that exists on paper only** — a stale or incomplete published contract means
  makers use the direct mechanism anyway, and the boundary becomes a fiction with a maintenance cost; the
  mitigation is enforcement **plus** discoverability, governance and enablement together. **Assuming one
  cloud is the boundary** — where the enterprise's integration platform is another vendor's, standing a
  parallel one beside it creates two boundaries and duplicates contract management, and nothing in the
  vendor evidence prompts the question. **Single point of failure at estate scale.** **Policy enforcement as
  an unplanned outage source.** **Unmeasured** — no capacity or latency figure for any boundary component
  exists anywhere in the baseline.
- **What it imports.** *Governance:* this composition **is** a governance import, and it is only valid when
  the boundary has an explicit owner and enterprise governance. The external resources need inventory,
  role-based access, policy baseline, budget and cost attribution and lifecycle controls; the platform's own
  data policy remains **only the consumer-side control**. *ALM:* the boundary needs its own source-controlled
  and infrastructure-as-code supply chain; where the platform consumes it through connectors, their rebinding
  hazards apply as well; cross-platform contract versions and release sequencing become first-class.
  *Cost:* usually the **highest fixed** governance and operations burden, and potentially the **lowest
  marginal** cost where the enterprise capability already exists and is shared. Where it does not exist,
  the cost is a programme and a platform team — not a gateway instance. *Monitoring:* a published catalogue,
  an API inventory mechanism, monitoring spanning both sides with correlation, and joint incident management
  across the boundary. *Recovery:* enterprise monitoring, correlation, incident routing, disaster recovery
  and support. *Operating model:* a platform-team **role**, a maker onboarding process, and joint incident
  management. **A boundary with no defined operating model is an incomplete design, not an unavailable
  one** — the requirement is the role, the identity, the alert destination and the incident route, priced
  here. What holds without qualification: an ungoverned boundary is worse than no boundary, because it adds
  a hop and an illusion.
- **Escalation consequence.** Standing up a boundary for a single solution is the clearest case of
  unnecessary complexity. Where the enterprise platform already exists and is adequate, the move is to
  **use it**, not to build a parallel one. Where speed dominates and the estate is small, the governance
  cost is not yet repaid — the recorded output is the simpler composition **plus a tripwire on the metric
  that would force the move**, not a boundary nobody funds. There is also a cheaper native variant worth
  naming: data policy plus environment strategy plus mechanism governance with **no intermediary at all**,
  which controls *which* systems may be reached without mediating *how* — weaker, cheaper, and often
  sufficient (inference).
- **Additional lineage note.** The security posture is the strongest of the ten compositions on documented
  grounds — one authentication point, network-isolated backends, enforced quotas, a secret store, and
  environment-level private connectivity that prevents lower environments from reaching production
  resources. One residual concern is inference: a boundary calling backends under its own identity removes
  per-user backend authorization unless it propagates identity.

## 6. Composition rules · `decision-grade`

**Compositions are the normal case, not the exception.** These combinations are documented rather than
merely possible:

| Composition | What it is for |
|---|---|
| **Queue + background processing** | Durable dispatch plus a status resource — the standard shape for long-running work whose caller needs to know. The most frequently documented pairing in the baseline |
| **Event-driven + queue** | The event carries the notification; the queue carries the guarantee. Emit on change, absorb the burst |
| **Virtualization + replication** | Read reference data live; copy only what needs platform data features. **Two mechanisms for one dataset, deliberately** — the documented enterprise-resource shape splits read, write and query across three mechanisms |
| **API-mediated + hybrid** | The API layer is the contract; a service behind it holds the domain logic. This is the documented placement rule, not a variation on it |
| **Hybrid + queue** | The externalised capability is reached asynchronously rather than synchronously — the shape when the capability is also slow |
| **Replication + background processing** | Replication with a job-status ledger, so the reconciliation pass has something to reconcile against |
| **Enterprise boundary enclosing everything** | The boundary is **not an alternative** to the others; the others operate *inside* it |

Four rules govern how they combine:

1. **One requirement, one rung.** Every escalation names the requirement that forced it. Two rungs at once
   is legitimate; an unjustified rung is not.
2. **Decide per stream, not per system pair.** One business goal decomposes into several streams, and the
   documented worked examples give the same system pair **different** treatments per stream. Per-stream
   heterogeneity is expected; a single verdict for a system pair is a smell.
3. **Imports accumulate; they do not merge.** Composing two rungs composes their imports. A design with a
   broker and an external worker and a mediation tier has three governance surfaces, three release routes
   and three cost meters — and possibly one operator, which is the gap.
4. **One retry site per hop chain.** Retry configured at the surface, the automation, the mechanism, the
   gateway and the backend multiplies rather than adds; the documented arithmetic is unforgiving, and the
   instruction against endless retry is explicit.

## 7. Selection failure modes · `decision-grade`

These are failures of **choosing** a composition. Implementation failure modes live with the mechanisms.

> **Pattern by resemblance.** A structure is selected because it matches a published reference architecture
> rather than because a requirement forces it. Every such reference carries its own caveat that it is an
> example modifiable for many scenarios, not a prescription. Consequence: the design imports an operating
> model nobody asked for and nobody owns.

> **Starting above the direct composition.** The design begins at the API layer or the broker because that
> is what enterprise architecture looks like. The vendor's instruction is the opposite — start with the
> simplest and escalate only where it does not meet the need. Consequence: fixed cost is paid for a
> property the requirement never named.

> **Buffer as a substitute for capacity.** A queue is added while the consumer stays unbounded.
> Autoscaling consumers without bounding their aggregate downstream rate only moves the overload
> downstream. Consequence: the throttling reappears at the target, now with a backlog in front of it.

> **Gateway as a shock absorber.** An API layer is expected to solve a spike. Under load a gateway is a
> bottleneck and a single point of failure, not a buffer. Consequence: the spike takes down the layer that
> every other consumer also depends on.

> **Virtualization chosen for elegance.** The composition is selected without checking the exclusion list.
> The baseline records two independent rejections, both discovered against **security** requirements.
> Consequence: the modelling decision is irreversible in place, so the discovery costs a rebuild.

> **Replication chosen by default.** Copying is chosen because copying is familiar, with no named item from
> the virtualization exclusion list as justification. Consequence: an operational store overloaded by
> reporting copies, or a shadow system of record that the source system's own guidance excludes by design.

> **Synchronization without reconciliation.** Only the fast path is built. The reference design's
> reconciliation pass exists *because* the fast path loses updates. Consequence: divergence by
> construction, discovered by a user rather than by a report.

> **Asynchrony without a status resource.** Fire-and-forget where someone will eventually ask "did it
> work?". The client cannot distinguish a lost response from a request never received. Consequence:
> duplicate submissions and unanswerable support questions.

> **Partial failure left undefined** in a composed call. The instruction to make the choice explicit in the
> policy is unambiguous. Consequence: clients experience unpredictable behaviour that looks like
> intermittent corruption.

> **Approximating a resilience pattern in the wrong layer.** Retry loops in place of a circuit breaker,
> variables in place of a dead-letter queue. Retry expects eventual success; a breaker prevents an
> operation likely to fail — different purposes. Consequence: a home-grown approximation with none of the
> guarantees and all of the maintenance. In a message-driven design, the broker's dead-letter is the
> documented answer and a breaker is often unnecessary.

> **Assuming one cloud is the boundary.** A parallel gateway is stood up beside an existing enterprise
> integration platform. Nothing in the vendor evidence prompts the question, which is exactly why it must
> be asked first. Consequence: two boundaries, duplicated contract management, and neither authoritative.

> **Adopting a composition whose operating model nobody defined.** A broker, an external worker or a
> boundary with no role accountable for the non-platform half, no execution identity and no alert
> destination. Consequence: the option carries an operating-model requirement with its own cost and risk —
> a statement about the design, never a ranking of the organisation. Where that cost is not worth paying,
> the honest output is the simpler composition plus a tripwire on the metric that would force the move.

> **One composition per system pair.** Deciding "how we integrate with system X" instead of deciding per
> stream. Consequence: the read/write asymmetry that should have driven the design is never surfaced.

## 8. Consequences elsewhere · `decision-grade`

- **→ governance and environments.** Every composition beyond the direct one creates a governed asset the
  platform's own data policy does not reach, and several boundary controls are gated on the
  **managed-environment** class. Ownership of each control, per environment, is a governance decision. See
  `governance/governance-and-environments.md`.
- **→ ALM and release.** Escalation is measured in **supply chains**. Custom connectors carry their own
  solution-boundary, import-order and rebinding hazards; external components need their own source control,
  infrastructure-as-code and pipeline; contract versions must stay compatible across a joint release. Where
  a consumption workaround would create an unmanaged layer, that collides with a production-integrity
  policy. See `alm/release-and-lifecycle.md`.
- **→ economics.** Each composition names its own meters, and the imports are where option costs are
  systematically understated: broker operations, worker compute, API runtime, telemetry ingestion and
  retention, doubled storage for a copy, non-production instances, and **operational labour**. A design with
  a second estate needs a second cost model or the option is incomplete. See
  `economics/licensing-and-cost-drivers.md`.
- **→ operations and support.** The **operator** import is the one that most often makes a design
  unrunnable. What a cross-boundary composition must carry operationally — a named service owner and
  escalation route, an end-to-end health model, a propagated correlation identifier, alert ownership for
  each half, a deployment route for both supply chains, a recovery order with reconciliation, a telemetry
  retention and cost owner, and a dependency and exclusion inventory — is stated in
  `operations/operability-and-support.md`.
- **→ performance and scale.** No composition removes the platform-side meters. Mediation, brokering and
  boundary ownership relocate a ceiling; they do not lift it. Every scalability statement in this baseline
  is **limit-based, never measured**. See `performance/performance-and-scale.md`.
- **→ the mechanisms these compositions are made of.** Envelopes, guarantees, payload ceilings, network
  boundaries and identity models are `integration/integration-mechanisms.md`; run-shape and trigger
  semantics are `automation/automation-mechanisms.md`; virtualization, replication and authority boundaries
  are `data/store-boundaries.md`; surface and offline behaviour is `application/application-surfaces.md`.
- **→ security.** Identity propagation across a facade or worker, secret custody, private egress and the
  operational preconditions the advanced controls add are `security/security-controls.md`.

## 9. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Per-mechanism throughput ceiling — **conflicted, see below** | `VC-01` / `VS-08` |
| Payload ceilings by mechanism (event envelopes, gateway writes) | `VS-10` |
| Gateway host minimum and network preconditions (**irreversible**) | `VS-11` |
| Run-duration ceilings that force the background-processing composition | `VS-12` / `VS-13` |
| Mechanism and service permissibility posture, per environment | `VC-03` |
| Request rate per acting identity (the back-pressure ceiling for any worker) | `VC-04` |
| Entitlement fit of the required capability set | `VC-05` |
| External and hybrid service consumption cost — gateway-at-scale is an open item | `VC-08` |
| Preview or general-availability state of anything on a critical path | `VC-10` |
| Managed-environment licence enforcement across the environment population | `TW-V3` |

**The one live quantitative conflict.** The per-connection throughput ceiling for the main extensibility
mechanism is **`CONFLICTED`** — two currently-maintained vendor sources disagree by a wide margin, the
conflict has been re-verified and remains open. **Neither figure is carried here, on either side.** Any
design whose sizing or economics rests on a high-frequency custom connector is **decision-blocked until
measured** (blocking entry `B-08`, composed row `CD-05`). The consequence is **symmetric across option
classes** — it cuts across this platform, the cloud-native classes and the hybrid class equally, and it is
never a penalty against this platform. A documented case-by-case escalation path exists and may be
*proposed* as a mitigation; it may never be *relied on in advance*.

**Not established in the baseline** — do not fill from general knowledge:

- **No capacity, latency or throughput figure for any composition component** — gateway node, API tier,
  broker or mechanism. Every scalability claim here is limit-based. "This composition scales" is not a
  measured statement.
- **Whether a mediation tier changes how platform requests are metered**, and whether a facade's own
  backend calls are counted at all. Do not claim meter relief.
- **Whether write-through virtualization is a supported production pattern**, and its performance
  characteristics.
- **Whether a private-egress-capable in-transaction component can publish to a broker while remaining
  transaction-scoped** — the proposed workaround for the event composition's private-network collision is
  inference.
- **Whether "enterprise boundary" is a recognised pattern** with a vendor or industry articulation
  applicable to this platform.
- **Whether any in-platform dead-letter, circuit-breaker, saga or compensating-transaction construct is
  documented.** Treat all four as unsupported until verified.
- **Failure semantics under sustained far-side failure** in tightly-coupled bidirectional synchronization.
- **Cost comparison between the mediated composition's variants** — a full gateway versus a plain service
  plus a connector. The plain variant is the documented platform instantiation; the choice is currently
  made on convention.

## 10. What not to infer · `decision-grade`

- **This file explains compositions; it does not select one and does not render a blueprint.** A capability
  boundary here is domain knowledge. *"Therefore this option is unsuitable"* is a selection verdict and
  belongs to the decision model.
- **Compositions are not the option space.** They are reachable only after an option class is established.
  A comparison whose top level is one structural shape against another is showing one option class as the
  whole choice.
- **A documented boundary here is not evidence that another option class performs better.** The structural
  costs, imports and failure modes of hosted services, custom-built systems, incumbent platforms and other
  low-code platforms are outside this baseline entirely; no like-for-like comparison exists. Where the
  comparison is material, `decision-model/outcome-classes.md`'s comparator semantics stand.
- **The ladder is not a fit scale.** It orders compositions by the property each buys and the price each
  charges. It does not rank options, and a higher rung is not a better design.
- **Resemblance to a reference architecture is not justification.** Every such reference states that it is
  an example, modifiable across scenarios and industries.
- **A documented limit above the workload is not evidence the composition meets the requirement.** Limits
  exclude; measurement proves.
- **An undefined operating model is a requirement with a cost, never an availability verdict.** That a
  design has not yet named the role that intervenes, the identity it runs as or the alert destination says
  the design is incomplete — it does not say the composition is unavailable, and it ranks nobody. Pricing
  that gap is this file's job; deciding what it does to an option is the decision model's (README §6).
- **The enterprise-boundary composition is supported synthesis, not vendor-endorsed guidance.** Extract its
  underlying requirements, constraints and ownership boundary; never claim endorsement.
- **Vendor-side positioning is not evidence.** Where a page's own product team characterises a competing
  product's scale, the capability rows are usable and the scale adjectives are not. The platform's scale
  positioning is itself `CONFLICTED` between two vendor sources; **encode neither adjective**. The
  encodable content is the escalation triggers and the documented mechanism limits.
- **Escalation is not one-way.** When the requirement that forced a rung disappears, simplification is a
  legitimate finding about a live system.
- **Naming is partly this baseline's own.** Several composition names here are not vendor terminology, and
  whether a vendor-published platform pattern catalogue exists beyond a small set of integration patterns
  is `UNKNOWN`. Use the names as handles, not as citations.
