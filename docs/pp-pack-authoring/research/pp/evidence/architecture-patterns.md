Research Status: CANONICAL
Research Confidence: MEDIUM
Gate: PASS — Cross-Block Gate Recheck
Canonicalization Basis: Cross-Block Gate Recheck
Canonicalized: 2026-09-03

# Architecture Patterns — Power Platform Research Evidence

Research area: **12 — Architecture Patterns** (`../research-areas.md`), scoped by the **Research Block A (Areas 05 and 12)** brief to *reusable solution structures* with WHEN / WHY / TRADE-OFFS / LIMITATIONS, deliberately **not** a catalogue of Microsoft products or a gallery of reference architectures.
Research date: **2026-09-03**. Source policy: `../source-policy.md`.
Companion file from the same pass: `integration-architecture.md` (Area 05). The two are conceptually distinct. That file establishes **which integration requirement forces which constraint** — the evidence, the envelopes, the limits, the failure semantics. This file establishes **which reusable structure satisfies a given set of requirements**, and what each structure costs. Where a fact is already established there it is cited as `IA-nn` rather than restated; the point of this file is the *structure*, not the fact.

**Id convention (Cross-Block V2).** `AP-nn` are **Area-12 architecture patterns** in this file and only this meaning is valid across files. Block C anti-patterns are now file-qualified (`PF-AP-nn`, `LC-AP-nn`, `OP-AP-nn`). Legacy local conflicts/unknowns are qualified when cited across files as `APR-C-nn` / `APR-U-nn`. `Q-nn` are **sources** in this file (§12). `IA-nn` are findings in `integration-architecture.md`; `I-nn` are its sources. `PS-nn` / `AA-nn` / `DA-nn` / `AT2-nn` are findings in the other peer evidence files. A pattern id and a source id that share a number are unrelated.

**Peer files cross-referenced, status verified 2026-09-03:** `platform-suitability.md` (VALIDATED, PASS, MEDIUM) as **PS-nn**; `application-architecture.md` (VALIDATED, PASS, MEDIUM) as **AA-nn**; `data-architecture.md` (VALIDATED, PASS, HIGH) as **DA-nn**; `automation-architecture.md` (VALIDATED, PASS, MEDIUM) as **AT2-nn**; `integration-architecture.md` (DRAFT, this pass, MEDIUM-HIGH) as **IA-nn**.

**The question this file answers.** Not *"which Microsoft reference architecture looks similar?"* but *"which architectural structure best satisfies these requirements, and what am I buying and selling by choosing it?"* Every pattern therefore carries a **When NOT to use** section and an **Alternatives** section, and those two sections are the load-bearing content. A pattern description without them is marketing.

---

## 1. How to read this file

**Classification** per `../source-policy.md`. Every entry in §4 is classified **PATTERN**; the individual claims inside it carry their own classification where it differs (CONSTRAINT, TRADE-OFF, RISK, ANTI-PATTERN). Cross-Block V2 additionally uses **VOLATILE VALUE** for dated limits, licensing/entitlement assumptions and feature states that must not become timeless pattern rules.

**Origin tag** on every pattern and on every load-bearing claim:
- **MS** — Microsoft statement on a page fetched in this pass (`ms.date` in §12).
- **MS-V** — Microsoft statement authored by the team selling the recommended alternative (here the Azure Logic Apps team, Q-16). Capability facts usable; **scale and performance adjectives are not evidence** (see `integration-architecture.md` IA-C-04).
- **INF** — analyst inference over documented facts. Most *pattern boundaries* in this file are INF over MS facts, and are labelled as such.
- **T3** — independent technical source.
- **UNKNOWN** — not established.

**A note on what "pattern" means here, and the honesty problem it creates.** Two kinds of evidence back the ten patterns below:
1. **Structural evidence** — Microsoft's own generic pattern catalogue (Azure Architecture Center: Queue-Based Load Leveling, Asynchronous Request-Reply, Gateway Aggregation, Anti-Corruption Layer, Circuit Breaker). These pages carry rigorous *Problems and considerations*, *When to use* and *This pattern might not be suitable when* sections, and they are the strongest available basis for trade-offs and limitations. They are **not Power-Platform-specific**.
2. **Instantiation evidence** — Microsoft's Power Platform reference architectures and key-concept pages, which show these structures built with Power Platform components and state their conditions. These are Power-Platform-specific but are written as *examples*, each carrying the caveat *"This article provides an example scenario and a generalized example architecture… The architecture example can be modified for many different scenarios and industries."*

Where a pattern has both kinds, confidence is HIGH. Where it has only instantiation evidence, the *limitations* are the weak part and confidence is MEDIUM. Where the pattern boundary itself is this file's synthesis, it is tagged INF and says so. **No pattern in this file is claimed to be a Microsoft-endorsed Power Platform pattern unless a fetched Microsoft page says so.**

**Absence claims.** Where a pattern's limitations include "the platform has no construct for X", the claim states whether Microsoft documents the absence (MS) or whether it is inferred from the capability not appearing in the reference documentation (INF). INF absence claims read **"treat as unsupported until verified"** wherever they appear.

**Confidence.** HIGH = both structural and instantiation evidence, fetched and dated. MEDIUM = one of the two, or the boundary is inferred. LOW/UNKNOWN = stated as such.

**Overall confidence MEDIUM.** Lower than the companion file, deliberately. The *structures* are well evidenced and the *constraints* behind them are HIGH-confidence facts carried from `integration-architecture.md`. But three things cap this file:
1. **The trade-off content for Power-Platform-specific patterns is thinner than for the generic Azure patterns.** Microsoft's Power Platform reference architectures document what was built and why; they rarely document what the design gives up. Most "Weaknesses" and "Risks" content below is therefore INF over documented constraints rather than a Microsoft statement of the weakness. This is the file's main honesty limitation and it is flagged per pattern.
2. **No empirical measurement exists anywhere in this corpus** (carried: `integration-architecture.md` IA-U-04). Every scalability statement is limit-based.
3. **Single author, single session** for research, organisation and self-review. The three highest-value independent checks are AP-06 (data virtualization's limitation list, because it is the pattern most often chosen for the wrong reason), AP-07 (replication's reconciliation obligation), and AP-10 (the enterprise-boundary pattern, whose evidence is the thinnest in the file).

---

## 2. What this file is not

Per the brief, three explicit exclusions, restated because the failure mode is easy to fall into:

- **Not a product catalogue.** "Use Azure Service Bus" is not a pattern. *"Place a queue between the task and the service"* (Q-02) is a pattern; Service Bus is one implementation of it, chosen by reading required guarantees off a property table (IA-15).
- **Not a reference-architecture gallery.** The reference architectures in §12 are evidence *for* patterns, not the patterns themselves. A design that resembles one is not thereby justified.
- **Not a decision tree or question bank.** Those are pack artefacts and are out of scope for this pass by instruction. §3 supplies the *variables*; §5 supplies a selection matrix; neither is an authored decision tree.

One further exclusion this file imposes on itself: **no pattern is recommended by default.** The corpus rule is *"Power Platform must NOT be assumed to be the answer"* (`../README.md`), and the pattern-level equivalent is that the *simplest* structure is the default and every escalation must name the requirement that forces it. Microsoft's own instruction is the same: *"When selecting an integration pattern, prioritize solutions that meet business needs with minimal complexity. Balance technical capability with cost, licensing, and maintenance requirements. Choose the simplest approach that fulfills requirements and avoids unnecessary investment"* (Q-01, MS).

---

## 3. The pattern-selection decision model

The brief asks for the variables that change the architecture, expressed as REQUIREMENT → CONSTRAINT → ARCHITECTURAL CONSEQUENCE. `integration-architecture.md` §2.1 does this for the twelve *requirement dimensions* and §9 lists the 28 elicitable variables. This section does something different and complementary: it names, for each variable, **which pattern boundary it moves**. That is the pattern-selection view of the same evidence, and it is what makes the catalogue in §4 navigable.

### 3.1 Variables that move a pattern boundary

| Variable | REQUIREMENT (what is asked) | CONSTRAINT (what binds) | ARCHITECTURAL CONSEQUENCE (which pattern moves) |
|---|---|---|---|
| **Volume** | sustained records/messages per period at horizon | smallest of {entitlement, service protection per identity, connector throttle per connection} — IA-10 | Above the envelope: AP-01 → AP-04 (queue + worker) or AP-05 (hybrid). Never AP-01 with a bigger flow |
| **Frequency** | peak per minute, plus seasonality | connector throttle is a per-window rate, not a daily total — IA-11 | Spiky arrival: AP-01 → AP-04. Predictable bulk: AP-01 → AP-07 (scheduled replication). May legitimately produce **two** patterns for one dataset — IA-02 |
| **Latency** | interactive / near-real-time / eventual, with a number | 120 s flow in/out, 180 s canvas, 2 min plug-in — IA-08, IA-09 | Beyond the window: AP-09 (background) mandatory, usually composed with AP-04. Sub-second interactive: AP-01 or AP-02 only |
| **Directionality** | who initiates, per stream | gateway is outbound-only; VNet support is outbound-only; legacy systems may forbid inbound — IA-04, IA-29 | Enterprise system must initiate: AP-03 (event-driven, inbound) or an inbound endpoint. Neither side may initiate: AP-04 with both reaching the broker outbound |
| **Capability of the far end** | the *other* system's documented throughput | weakest link governs — IA-06 | Weak far end: AP-06 (virtualize, accepting upstream freshness) or AP-07 (replicate) or AP-04 (buffer). Not AP-01 |
| **Ownership / system of record** | per entity, per field, per lifecycle phase | authority is assignable per phase; financial ledgers are presumptively excluded from bidirectional sync — IA-36, IA-37 | Another system owns it: AP-06 (read) not AP-07 (copy). Authority transfers mid-lifecycle: AP-02 or AP-05 with a locking step |
| **Coupling tolerance** | may the caller's availability depend on the target's? | direct calls inherit the target's availability; brokers do not — IA-26, Q-02 | No tolerance: AP-03/AP-04. Tolerance: AP-01 acceptable |
| **Consistency** | strict / read-your-writes / eventual, with a convergence window | atomicity stops at the Dataverse boundary — IA-19 | Strict across systems: no pattern in this file satisfies it; collapse to one writer (AP-02/AP-05) or leave the platform (AP-10 / `integration-architecture.md` §12.3) |
| **Transaction semantics** | is there a multi-system unit of work? | no cross-system atomicity; synchronous webhook is a dual-write hazard — IA-20, IA-21 | Multi-system UoW: AP-09 + compensation + reconciliation, or AP-10 |
| **Delivery guarantee** | at-most / at-least / effectively-once; ordering; duplicate tolerance; replay | guarantee is a property of the transport — IA-15 | Anything beyond "retry then fail": AP-04 with the transport chosen from the property table. Replay requirement: Event Hubs Capture or an external log — AP-10 |
| **Availability** | availability of the weakest link *including customer-operated parts* | gateway and self-hosted components are customer-operated — IA-27, IA-28 | Introducing AP-05 or AP-10 converts a SaaS availability profile into an operated one; that cost belongs in the option |
| **Network boundary** | public / private endpoint / on-premises | gateway 2 MB caps; VNet preconditions; **Azure-aware plug-ins do not support VNet** — IA-27…IA-29 | On-premises: AP-01 via gateway, or AP-10 with an in-network component. Private **and** Dataverse events: collision — see AP-03 limitations |
| **Security / identity** | delegated user / service principal / managed identity / stored secret | managed identity covers Dataverse plug-ins only — IA-31; no `client_credentials` for custom connectors — IA-32 | "No stored secrets": AP-05 with the plug-in leg, or AP-10. "Backend enforces per-user authorization": AP-01/AP-02 delegated; **excludes AP-06** |
| **Integration reuse** | how many consumers need this capability? | ≥ 2 consumers is the documented trigger for centralising — IA-49 | 1 → AP-01. ≥ 2 → AP-02. Many consumers + many backends per view → AP-08 |
| **Contract volatility** | how often does the backend contract change? | custom connector schema change forces republish + reconnect in every consumer — IA-49, I-07 | Volatile contract: AP-02 with versioning. Semantically hostile contract: AP-08's anti-corruption variant |
| **Failure handling** | what happens to a failed message? | no dead-letter and no circuit-breaker construct in cloud flows — IA-46 (INF, treat as unsupported until verified) | Poison-message quarantine or fail-fast: AP-04 or AP-02/AP-10. Not achievable inside AP-01 |
| **Observability** | trace / message-level audit / replay / retention | Power Automate monitoring is portal + optional App Insights injection — IA-45, X-18 | Message-level audit or replay: AP-04 (broker + dead-letter) plus AP-09's status resource, or AP-10 |
| **Operational ownership** | who runs it, who is paged | hybrid and boundary patterns import a second operating model — AT2-53 | AP-05 and AP-10 require a named operator and a second pipeline; if there is none, the pattern is not available |
| **Licence profile of the owner** | which plan owns the flow and the connections | retry depth, loop items, content throughput and request ceiling are all licence-dependent; a leaver reverts the profile — IA-16, IA-17, AT2-01 | Low-profile ownership degrades AP-01, AP-03 and AP-09 silently; business-critical use requires dedicated capacity or the pattern's reliability claim is void |
| **Existing enterprise capability** | is integration already owned, with a published contract? | nothing in the platform documentation prompts this question — `integration-architecture.md` §12.1 | Yes → AP-10, and AP-01…AP-09 apply only *inside* the boundary |

### 3.2 The escalation ladder

The ten patterns are not peers; they form an ordered ladder in which each rung buys a specific property at a specific price. Reading the ladder is often faster than reading the catalogue.

```
AP-01  Direct                          — cheapest; buys nothing, costs nothing
  ↓ two or more consumers, or contract volatility, or composition, or rate limiting
AP-02  API-mediated                    — buys abstraction/versioning/policy; costs a hop, a bill, a team
  ↓ many backends behind one client operation
AP-08  API facade / BFF                — buys composition + a single client contract; costs a SPoF and partial-failure design
  ↓ producer must not depend on consumer availability; or events already exist upstream
AP-03  Event-driven                    — buys decoupling and freshness; costs ordering, duplicates, loop risk
  ↓ delivery guarantees, spike absorption, poison-message handling, scheduled delivery
AP-04  Queue-based                     — buys durability + load levelling; costs latency, idempotency work, backlog ops
  ↓ one step exceeds the platform (compute, duration, protocol, guarantee)
AP-05  Hybrid low-code + pro-code      — buys capability; costs a second operating model
  ↓ work exceeds a synchronous window or must survive restarts
AP-09  Background processing           — buys responsiveness; costs a status resource and UX complexity
```

Orthogonal to the ladder — these answer *where the data lives*, not *how the call is made*:

```
AP-06  Data virtualization             — buys freshness-at-read + no copy; costs platform data features and per-row authorization
AP-07  Data replication                — buys platform data features + local performance; costs the whole synchronization risk register
```

And enclosing all of the above:

```
AP-10  Enterprise boundary             — buys governance, reuse and an owner; costs autonomy and lead time
```

**How to use the ladder.** Start at AP-01. Climb only when a *named requirement* from §3.1 forces it, and record which one. Two rungs at once (e.g. AP-01 → AP-04) is common and legitimate; skipping the *justification* is not. Coming back **down** the ladder is also legitimate and rarely considered: if the requirement that forced a rung disappears, the structure should be simplified.

- **Classification:** DECISION CRITERION · **Origin:** INF (the ladder and the variable-to-boundary mapping are this file's synthesis; every constraint is MS-sourced in `integration-architecture.md` §5 or in §4 below) · **Confidence:** MEDIUM · **Sources:** synthesis over Q-01…Q-20 and IA-01…IA-49.
---

## 4. Pattern catalogue

Each pattern carries the eleven fields the brief requires, plus **Evidence**, **Origin**, **Confidence** and **Sources**. The **When NOT to use** and **Alternatives** fields are the ones that make the catalogue usable as a decision aid rather than a description.

---

### AP-01 — Direct integration

```
Power Apps / Power Automate  ──►  External system
```

**Classification:** PATTERN · **Origin:** MS (the structure and its default status) + INF (the boundary conditions) · **Confidence:** HIGH

**Problem solved.** A Power Platform artefact needs to read from or write to one external system, and the requirement is satisfied by a call. No intermediary exists to justify, no guarantee beyond "it worked or it failed" is needed, and no other consumer needs the same capability.

**Appropriate conditions** (all must hold — this is IA-§4.1 restated as a pattern precondition):
- One consumer of the capability.
- Projected peak-minute volume inside the connector throttle, measured per connection.
- Stable backend contract, or acceptance of the republish-and-reconnect cost on every change.
- Completion inside 120 s (flow) / 180 s (canvas).
- Transformation and business rules exist in exactly one place.
- "Retry per policy then fail and log" is acceptable failure semantics.
- The backend's own authorization model suffices, or a per-user explicit connection is available.

**Architectural structure.** Artefact → connector (standard, premium, custom, or HTTP) → system. Where the system is on-premises, the gateway sits in the path with its 2 MB write cap. Where private egress is required, the environment is subnet-delegated and the connector must be on the VNet-supported list.

**Strengths.**
- Lowest total cost of ownership, and Microsoft says so explicitly: *"start with Power Automate as the default option. It offers unmatched cost-effectiveness for both development and maintenance"* (Q-07, MS).
- Fastest to build and to change; no second deployment unit, no second team.
- Fewest moving parts, therefore fewest failure modes to design for.
- The connector abstracts protocol and auth; the maker does not implement OAuth.

**Weaknesses.**
- **Tight coupling to availability and latency.** A synchronous user-triggered call makes the enterprise system's uptime part of the app's UX. Microsoft states the consequence: *"Instant triggers aren't truly instant… Avoid scenarios where users select a button and receive no response, which leads to a poor user experience"* (Q-07, MS).
- **Throughput is capped by the connector, not by the design**, and the cap is per connection so unrelated artefacts contend (IA-11).
- **Contract fragility.** *"If you update (remove, add, or change) a field in the API… Republish the connector… Remove any connection / data source in any app that used that connector… Re-add the connection"* (Q-37, MS) — a backend change is a coordinated change across every consumer.
- **No reuse.** The second consumer duplicates the integration, and the third makes it an anti-pattern (X-01).
- **Failure semantics are shallow.** Retry policy depth is a function of the *owner's licence* (IA-17), which means the pattern's resilience is not a property of the design.

**Risks.**
- **Silent degradation to POOR on volume growth.** The design that is correct at launch becomes throttled at 3× volume, and a consistently throttled flow is turned off after 14 days (IA-16). This is the pattern's characteristic failure: it does not get slower, it gets switched off.
- **Point-to-point explosion by accretion.** Each new requirement adds one more direct pipeline; nobody decides to build a spaghetti architecture (Q-07's own word) — it is what AP-01 becomes when nobody counts.
- **Licence-dependent behaviour** (IA-17, AT2-01): retry depth, loop item ceilings, content throughput and request ceilings all move with the owner's plan, and a leaver reverts the profile.

**Operational implications.** Monitoring is flow run history plus, optionally, Application Insights (preview, managed-environments-only, *"not 100% lossless"* — AT2-42). There is no message-level audit and no replay. Ownership is the flow owner, which must be a deliberate choice rather than "whoever built it" (IA-16).

**Security implications.** The connection is the identity boundary. Shared/implicit connections reuse the maker's credentials for every user (DA-33); explicit per-user connections preserve backend authorization but multiply connections. Secrets live in the connection or in the action unless externalised to Key Vault via environment variables (IA-35). No managed identity is available on this path (IA-31).

**Scalability implications.** Bounded by the smallest of the three meters (IA-10), and the connector meter normally binds first. Documented partitioning levers: multiple connections, multiple identities (DA-10), multiple flows (Q-30's repeated *"Distribute the workload across more than one flow as necessary"*). Documented non-lever: batching to evade entitlement — *"Batch operations aren't a valid strategy to bypass entitlement limits"* (AT2-02).

**Governance implications.** Direct connector use stays inside Power Platform governance, so DLP/ACP, environment strategy, connector inventory and connection ownership are the main controls. It is not “zero governance”: a shared connection can become a production dependency whose owner leaves.

**ALM implications.** Lowest cross-estate burden when standard connectors are used. Custom connectors change the answer: import order, connection references and post-deployment binding from `alm-devops.md` ALM-14 apply.

**Performance / scale boundary.** The first binding entitlement/service-protection/connector meter governs. The custom-connector per-connection rate is `CONFLICTED` corpus-wide and must not be used as a fixed sizing number.

**Cost implications.** Usually the lowest structural cost, but premium/custom connectors, gateway, managed-environment controls and the licence profile of the audience can dominate. Treat current entitlements/rates as **VOLATILE VALUE**.

**Operations / recovery.** The caller inherits target availability and needs retry/error ownership. A restore of either side can still create data divergence if writes are duplicated elsewhere; direct integration does not provide replay.

**Power Platform ownership boundary.** Use only while the responsibility is genuinely application integration. If the API contract is shared by multiple consumers, needs central policy/versioning, or already belongs to an enterprise integration team, move to AP-02 or AP-10.

**Validation.** V1 documentation/limits is enough only for clearly low-volume, low-criticality cases; otherwise use a V2 bounded pilot with the real connector and target.

**When NOT to use.**
- Two or more consumers need the same capability → AP-02.
- The call exceeds 120 s / 180 s → AP-09.
- Delivery guarantees, ordering, duplicate suppression or dead-lettering are required → AP-04.
- The producer must not depend on the consumer's availability → AP-03 or AP-04.
- Payload exceeds the gateway's 2 MB write cap or the content-throughput meter → AP-05 or AP-10 with reference-passing.
- The backend contract is semantically hostile and would leak into every flow → AP-08 (anti-corruption variant).
- The far end cannot take the frequency → AP-04, AP-06 or AP-07.

**Alternatives.** AP-02 (reuse, contract, policy), AP-03 (decoupling), AP-04 (guarantees and levelling), AP-06 (read without a call per row), AP-10 (someone else already owns it).

**Evidence.** Structure and default status: Q-07 (*"start with Power Automate as the default option"*; the four reasons; the exit condition *"Use these options only when Power Automate doesn't meet your business or technical needs"*). Minimal-complexity instruction: Q-01. Worked instantiation with all four streams direct before escalation: Q-01's example. Weaknesses and risks: Q-30 (limits, retry-by-profile, auto-off), Q-37 (contract change procedure), IA-10…IA-17.
**Sources:** Q-01, Q-07, Q-30, Q-37; IA-10, IA-11, IA-16, IA-17, IA-23; peers DA-10, DA-33, AT2-01, AT2-02, AT2-42.

---

### AP-02 — API-mediated architecture

```
Power Platform  ──►  API / API Management  ──►  Enterprise services
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH

**Problem solved.** Several consumers need the same backend capability; or the backend contract must evolve independently of its consumers; or the backend must be protected, cached, transformed or observed as a managed asset rather than as whatever each caller happens to do.

**Appropriate conditions** (any one is sufficient — the five named justifications of IA-49, plus two governance conditions):
1. ≥ 2 consumer classes need the capability.
2. Multi-source composition per client operation (*"when multiple data sources are needed to build a single view"* — Q-18, MS).
3. Contract stability and versioning are required (*"allowing API providers to abstract API implementations and evolve backend architecture without impacting API consumers"* — Q-24, MS).
4. The backend must be protected by quota or rate limit, or accelerated by cache (*"Enforces usage quotas and rate limits"*; *"caches responses to improve response latency and minimize the load on backend services"* — Q-24, MS).
5. End-to-end telemetry across the call path is required (*"Emits logs, metrics, and traces"* — Q-24, MS).
6. Discovery and controlled consumption are required — the developer portal plus *"export these APIs to the Power Platform… as custom connectors for discovery and consumption by citizen developers"* (Q-25, MS).
7. Private-network reach with credential isolation — the documented shape is custom connector + Entra-ID-protected backend + subnet-delegated environment + client id/secret from Key Vault through environment variables (Q-19, MS).

**Architectural structure.** Power Platform artefact → custom connector → APIM gateway (or a plain API) → backend service(s). Policies at global / workspace / product / API / operation scope. Optionally a service *behind* the gateway for domain logic. Where the backend is private, APIM Premium/Premium v2 for VNet, or the self-hosted gateway inside the network.

**Strengths.**
- **One place for the contract.** Consumers see a stable surface; the backend can change behind it.
- **One place for policy.** Rate limiting, quotas, key/JWT/certificate verification, transformation, caching, CORS — configured, not coded (Q-24, MS).
- **The only documented place to rate-limit Power-Platform-side callers.** Power Automate has no rate-limit construct beyond concurrency control, whose defect is IA-22.
- **Observability across the whole path**, which the flow-only design cannot provide (Q-04's telemetry guidance, MS).
- **Reuse is a first-class outcome:** *"centralizing the logic where it could be used by other applications in the organization"* (Q-18, MS).
- **Federated governance is supported** — APIM workspaces give *"isolated administrative access and API runtime"* so decentralised teams own their APIs while a platform team retains oversight (Q-24, MS).

**Weaknesses.**
- **A hop, a bill and a team.** The layer is an Azure resource with its own lifecycle, tiering decision, SLA and operator. Microsoft's own cost warning applies: *"Custom solutions might seem powerful but often require a bigger budget for development, licensing, and support. Justify higher costs with clear business value"* (Q-07, MS).
- **More code-first work.** Stated plainly in the Power Platform instantiation: *"This architecture offers flexibility, but also means that more code-first developer work is needed to develop and maintain the RESTful service and data layer"* (Q-18, MS).
- **Deployment coupling.** *"With the dependency between the application and the REST API you should ensure you have a tested strategy to mitigate a roll out of either that develops errors after one of the components is updated"* (Q-18, MS).
- **The custom connector remains a contract-change chokepoint** even with a stable API behind it (IA-49, Q-37).
- **OpenAPI 2.0 only, and custom-connector count caps** (1 on Microsoft 365 / Dynamics 365 plans) push toward fewer, coarser connectors — which can undo some of the granularity the API layer was meant to provide (IA-13, MS).

**Risks.**
- **Single point of failure and bottleneck.** *"The gateway service might introduce a single point of failure (SPoF). Ensure that the gateway is properly designed to meet your application's availability requirements."* *"The gateway might introduce a bottleneck. Ensure that the gateway has adequate performance to handle the current load and can be scaled to meet your anticipated growth."* *"Perform load testing against the gateway to ensure that you don't introduce cascading failures for services"* (Q-04, MS).
- **Logic creep into the gateway** — the named remedy is to put a service behind it (Q-04, MS; X-12).
- **A pass-through gateway with no policy** is pure cost and pure risk: it adds the SPoF without the benefit (INF over Q-04).
- **Tier lock-in on network requirements.** Private backends, multi-region and availability zones are Premium/Premium v2 features (Q-24, MS) — a network requirement discovered late is a tier change, i.e. a cost change.

**Operational implications.** Azure Monitor + Application Insights for the gateway; *"Route API Management and back-end telemetry to a Log Analytics workspace for unified querying, alerting, and troubleshooting"* (Q-04, MS). Requires a named API owner and a release process for the API separate from the Power Platform solution. CORS policy plus a connector policy is needed merely to test from the Power Apps console (Q-25, MS) — a small but real friction.

**Security implications.** Strongly positive: fewer touchpoints, backends network-isolated from clients. *"This topology often reduces the number of touchpoints that a client has with a system, which reduces the public surface area and authentication points. The aggregated back ends can remain fully network-isolated from clients"* (Q-04, MS). Entra ID for backend protection and developer auth; Key Vault for client certificates and secrets (Q-24, MS). Caveat: the custom connector cannot use `client_credentials` (IA-32), so the *Power-Platform-to-gateway* leg still carries a delegated user token or a stored secret; and *"OAuth and token requests do not transit the linked Virtual Network"* (Q-37, MS), so the IdP stays publicly reachable even in a private design.

**Scalability implications.** Moves the ceiling from the connector to the gateway tier plus the backend. Does **not** remove the Power-Platform-side meters: the calls still count as Power Platform requests, and whether an APIM-fronted custom connector is metered differently is **not established** (APR-U-04, carried from `integration-architecture.md` IA-U-22). Caching at the gateway is the documented lever for reducing backend load (Q-24, MS).

**Governance implications.** The mediated API/gateway becomes a governed workload asset: named owner, API inventory, RBAC/Policy baseline, budget attribution and lifecycle policy. Power Platform DLP governs use of the connector; it does not govern the gateway/backend itself.

**ALM implications.** If Power Platform consumes the mediation layer through a custom connector, ALM-14 applies: keep the connector in a deliberate solution boundary, control import order and connection-reference rebinding, and test the canvas-app workaround that can create an unmanaged layer. **Decision boundary:** where the workaround would defeat `block unmanaged customizations`, the pattern is unavailable under that production-integrity policy unless the consumer is redesigned. The API/gateway also needs its own IaC/CI-CD pipeline and contract-version compatibility with the Power Platform release.

**Performance / scale boundary.** Mediation can centralise caching/rate limiting but adds a hop and can become a bottleneck. It does not erase downstream connector/service limits.

**Cost implications.** Adds Azure/API runtime, telemetry, non-production and operator cost; can reduce duplicated integration implementation across multiple consumers. Price per engagement, not from a static comparator table.

**Operations / recovery.** Requires gateway/API health, backend dependency monitoring, correlation, safe deployment and incident ownership. Recovery must cover both the API layer and the consumer contract.

**Power Platform ownership boundary.** Power Platform should not own the mediation layer where an existing enterprise API platform already owns the contract or where API lifecycle/governance is an enterprise capability.

**Validation.** V2 bounded pilot for latency/policy behaviour; V3 automated API contract/regression tests for business-critical use; V4 managed-test fidelity where network/security controls matter.

**When NOT to use.**
- One consumer, one backend, stable contract, inside the throttle → AP-01. This is the majority case and the discipline matters.
- The backend is already an enterprise-managed API → consume it; wrapping a managed API in a second managed API duplicates contract management (INF over Q-24, Q-25).
- The motive is convention or resemblance rather than a named justification → AP-01, per the brief's FINAL TEST.
- The requirement is durability, ordering or spike absorption → AP-04. An API layer does not buffer; a gateway under a spike is a bottleneck, not a shock absorber (Q-04, MS).
- The requirement is long-running work → AP-09; a gateway with a long-held connection is the anti-shape (Q-03's premise).

**Alternatives.** AP-01 (below the threshold), AP-08 (when composition rather than mediation is the point), AP-04 (when the property needed is durability), AP-10 (when the enterprise already provides the gateway), and the plain-API variant of AP-02 — a Function or service with a custom connector and no gateway, which is Q-18's actual instantiation and is materially cheaper than APIM.

**Evidence.** Justifications and structure: Q-24 (gateway responsibilities, components, tiers, workspaces, policies, integrations), Q-18 (the Power Platform instantiation, its rationale and its stated cost), Q-19 (the private-network instantiation), Q-25 (the APIM→Power Platform connector path). Weaknesses and risks: Q-04 (SPoF, bottleneck, load testing, aggregation placement, telemetry), Q-07 (TCO), Q-37 and IA-13/IA-32 (connector-side constraints).
**Sources:** Q-04, Q-07, Q-18, Q-19, Q-24, Q-25, Q-37; IA-13, IA-22, IA-32, IA-49.

---

### AP-03 — Event-driven architecture

```
System A  ──event──►  Event infrastructure  ──►  Power Platform / other consumers
```
…and symmetrically:
```
Dataverse  ──event──►  webhook / Service Bus / Event Hubs / business event  ──►  external consumers
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH

**Problem solved.** Work must start when something happens, without a user asking and without polling. The producer should not know or care who consumes, and should not wait for them.

**Appropriate conditions.**
- A state change in a system is the natural trigger and the system can emit it (Dataverse can, via row triggers, business events, webhooks, or Service Bus/Event Hubs — Q-10, Q-11, Q-12).
- Freshness matters more than a fixed schedule, and the volume is event-shaped rather than batch-shaped.
- The consumer's work is independent of the producer's transaction (post-commit — IA-21).
- Loss and duplication tolerances are understood, because the transport decides them (Q-09).
- Inbound-only network posture on the producer side: *"Legacy on-premises systems might restrict inbound connections. In such cases, design the integration so the legacy system initiates communication with the cloud application"* (Q-01, MS) — this makes AP-03 the pattern of choice when the enterprise system must be the initiator.

**Architectural structure.** Producer emits → transport (webhook endpoint, Service Bus queue/topic, Event Grid, Event Hubs, or a Dataverse trigger consumed by a flow) → consumer(s). Inside Dataverse the emission mechanism is an Azure-aware plug-in registering a service endpoint, or a webhook step, or a catalogued business event, each with different semantics (IA-25, IA-26).

**Strengths.**
- **Decoupling in time and in knowledge.** The producer does not wait and does not enumerate consumers. Topics allow *"one or more listeners"* to subscribe (Q-10, MS).
- **Scales with the platform's own trigger machinery**, with server-side filtering so unwanted events never become runs: change type, `Select Columns`, `Filter Rows` (Q-07, MS).
- **Microsoft calls it intuitive and scalable:** *"This pattern is intuitive and scalable, making it ideal for automating business processes based on system events"* (Q-07, MS).
- **Non-CRUD events are expressible** via business events and custom APIs — including events that originate *outside* Dataverse (Q-12, MS).
- **Cheaper than polling** for the same freshness, because polling costs a request per interval whether or not anything changed (IA-§6 X-04).

**Weaknesses.**
- **No ordering by default**, and per-partition or FIFO-with-sessions only on specific transports (Q-09, MS).
- **At-least-once means duplicates**; the consumer must be idempotent (Q-02, MS) and in Dataverse that means an alternate key (DA-53).
- **Volume is unpredictable:** *"Launch based on user actions or system events. Harder to predict. Can spike unexpectedly, especially in public-facing systems"* (Q-01, MS). Downstream services have their own caps: *"Notification services (email, SMS, and others) limit how many messages you can send in a given time frame"* (Q-07, MS).
- **Payload ceilings are low and lossy.** 192 KB for the Service Bus/Event Hubs context with property stripping and hard failure above it after stripping; 256 KB for webhooks with a truncation header (IA-25, MS). Events carrying whole records will silently lose context.
- **Webhook scale is the receiver's scale:** *"Webhooks can only scale to the point at which your hosted web service can handle the messages"* (Q-11, MS).
- **Weak retry on the webhook path:** 60 s timeout, one extra attempt and only on 502/503/504 (Q-11, MS).

**Risks.**
- **Self-triggering loops** — the pattern's characteristic catastrophic failure. *"Avoid loops where an event triggers an action that retriggers the same event. Prevent multiple updates from causing rapid, repeated notifications"* (Q-07, MS); *"Make sure to use trigger conditions to prevent endless loops if, as part of the workflow, you change the data source that starts the workflow"* (Q-23, MS). Aggravated by the Dataverse trigger's presence-not-change semantics: *"The flow triggers if any of the columns is present in the update payload regardless of if data is modified"* (Q-38, MS).
- **Synchronous emission from a transaction is a dual-write hazard**: *"the data operation rolls back but the request sent to the configured endpoint can't be recalled"* (Q-11, MS).
- **One-way / Two-way Service Bus contracts eventually abandon the message** when no listener is present, ending as a Failed system job (Q-10, MS) — re-coupling what the broker was meant to decouple.
- **Private-network collision.** *"Azure-aware plugins don't support VNet"* (Q-29, MS) — the standard Dataverse event-emission mechanism and a mandatory-private-egress policy cannot both be satisfied through that mechanism today (IA-28). This is the pattern's least-known and most consequential limitation.
- **Events used as a data pipe.** Microsoft names the misuse: *"If your intent is to transfer data to a recipient and, in effect, realize a data export scenario, don't use business events. Using business events for data transfer scenarios is a misuse of the business events"* (Q-12, MS).

**Operational implications.** Failures land in **two** places: flow run history for flow-consumed events, and the Dataverse **System Jobs** view for Azure-aware plug-in posts (*"check the status of the related system job in the web application for more information about the error"* — Q-10, MS). Both must be monitored; they are separate surfaces. Event-rate monitoring is a requirement, not an option: *"Estimate the number of events per day or month. Implement throttling or rate-limiting mechanisms. Prepare a mitigation plan for unexpected spikes in event frequency"* (Q-07, MS).

**Security implications.** Webhook endpoints are secured by header or query-string keys — *"This approach is simpler than the SAS authentication model that you might currently use for Azure Service Bus integration"* (Q-11, MS) — which is convenient and weaker; a leaked key is a full subscription. Service Bus uses SAS with a Dataverse-signed claim (Q-10, MS). Inbound business events from external systems require a Dataverse application user and S2S auth (Q-12, MS). Event payloads cross a boundary, so field-level sensitivity must be assessed on the *event*, not only on the table (INF over DA-59).

**Scalability implications.** The transport's scaling model applies (Event Grid serverless/automatic; Event Hubs throughput units; Service Bus messaging units — Q-09, MS). On the Power Platform side the consumer is still bound by the three meters, so a high event rate consumed by flows re-imports the AP-01 ceiling. Consuming with an Azure worker instead is AP-04/AP-05.

**Governance implications.** Event ownership, schema/version governance, publisher/subscriber inventory and data classification of payloads must be explicit. Existing enterprise event backbones take precedence over creating a project-local one.

**ALM implications.** Event schema is a versioned contract. Publisher and subscriber releases must preserve compatibility; infrastructure subscriptions/topics and Power Platform listeners have separate deployment lifecycles.

**Performance / scale boundary.** Events decouple callers but do not guarantee a throughput envelope. Trigger latency, subscriber limits and broker quotas must be sized independently.

**Cost implications.** Adds broker/event operations, retention/telemetry and operator cost where an external backbone is introduced.

**Operations / recovery.** Correlation identifiers must be carried in the event envelope. Define poison-event handling, retry/dead-letter/replay semantics where the transport supports them. A restore can require replay/reconciliation from the restored time boundary.

**Power Platform ownership boundary.** Do not make Power Platform the enterprise event backbone. If enterprise eventing already exists, Power Platform is a producer/consumer at that boundary.

**Validation.** V2 pilot must include burst, duplicate/retry and subscriber-failure cases; V3 harness where schema compatibility is contractual.

**When NOT to use.**
- Strict ordering or exactly-once is required and the transport cannot provide it → AP-04 with Service Bus sessions, or reconsider the requirement.
- The consumer cannot absorb the burst → AP-04 (the queue is the shock absorber; the event is not).
- Bulk data movement → AP-07 or a data pipeline (X-17).
- The producer's transaction must be able to un-say the event → do not emit synchronously; the pattern does not support retraction.
- The event context exceeds 192/256 KB and matters → pass a reference and let the consumer fetch (Q-12's *"Lightweight… the information in the event should provide the context to allow them to retrieve it"*).
- Mandatory private egress plus Dataverse-transaction-level eventing → currently unsatisfiable through Azure-aware plug-ins (IA-28); use a VNet-supported connector path from a flow, or a plug-in writing directly to a private endpoint (both INF; APR-U-05).

**Alternatives.** AP-04 (when guarantees or levelling are needed), AP-01 with polling (when the source has no event surface — accepting the request cost), AP-07 (when the requirement is really "keep a copy in step"), AP-10 (when the enterprise already runs an event backbone with its own contract).

**Evidence.** Pattern definition and conditions: Q-07 (event-driven/automatic-trigger pattern, trigger configuration, loop avoidance, volume-and-frequency considerations), Q-01 (trigger classes, inverted caller). Mechanism semantics: Q-10 (contracts, 192 KB, retry-to-abandonment, System Jobs), Q-11 (webhook vs Service Bus comparison, 256 KB, 60 s, retry rules, rollback hazard), Q-12 (business events, catalogues, design principles, misuse statement). Transport properties: Q-09. Limitation: Q-29 (VNet exclusion).
**Sources:** Q-01, Q-02, Q-07, Q-09, Q-10, Q-11, Q-12, Q-23, Q-29, Q-38; IA-21, IA-25, IA-26, IA-28; peers DA-53, DA-59.

---

### AP-04 — Queue-based architecture

```
Power Platform  ──►  Queue  ──►  Worker / service
```
…and inbound:
```
External producer  ──►  Queue  ──►  Worker  ──►  Dataverse
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH

**Problem solved.** Arrival rate and processing rate must be allowed to differ — because of spikes, because the target throttles, because the consumer may be down, or because the work must not be lost. *"Use a queue that acts as a buffer between a task and the service that it invokes. This approach smooths intermittent heavy loads that might cause the service to fail or the task to time out"* (Q-02, MS).

**Appropriate conditions.** Microsoft states them: *"Use this pattern when: Your workload experiences intermittent spikes that can overwhelm downstream services. You need to decouple request intake from processing throughput to improve resilience and cost control"* (Q-02, MS). Add, from the Power Platform instantiations:
- Throttling avoidance is the explicit goal — Q-01's escalation ends *"To decrease the dependency even further, decouple the create and update requests from the website using a queuing service such as Azure Service Bus"*, whose stated purpose is to *"prevent throttling errors (such as HTTP 429 Too Many Requests)"* (MS).
- Scheduled future delivery with cancellation — Q-17 schedules Service Bus messages and retains *"sequence numbers for future updates or cancellations"* (MS).
- Poison-message quarantine is required (dead-letter queue) — no in-platform equivalent exists (IA-46).
- Long-running work must be dispatched off the interactive path — Q-20's clone jobs: *"Azure Service Bus dispatches long-running clone jobs to an Azure Function for asynchronous processing, and the function writes the job status to Dataverse"* (MS).

**Architectural structure.** Producer (flow, plug-in, app, or external system) → queue/topic → worker (Azure Function, Container App, Logic App, or a flow triggered by the queue connector) → target. A status record in Dataverse tracks each unit of work (AP-09's status resource). Dead-letter queue plus depth monitoring closes the loop.

**Strengths.** Microsoft's three, verbatim: *"It helps maximize availability because service delays don't immediately and directly affect the application. The application can continue to post messages to the queue even when the service isn't available or isn't currently processing messages."* *"It helps maximize scalability because the number of queues and the number of services can vary to meet demand."* *"It helps control costs because you only need enough service instances to meet the requirements for an average load rather than the peak load"* (Q-02). Plus:
- **The guarantee lives in the transport**, so it is configured rather than coded (Q-09).
- **Dead-lettering gives poison messages a destination** — the only documented mechanism in this corpus for that requirement (Q-02, Q-09).
- **Cancellation and rescheduling become possible** via broker sequence numbers (Q-17, MS).
- **Explicitly cited by Microsoft as the way past a Power Automate ceiling:** the notification architecture exists *"overcoming the limitations of relying solely on Power Automate for orchestrating large volumes of notifications"* and uses the broker *"without the overhead that Power Automate-based delays would introduce"* (Q-17, MS).

**Weaknesses.**
- **Latency by construction.** The pattern trades immediacy for durability; *"This pattern might not be suitable when: The caller requires a low-latency, synchronous response"* (Q-02, MS).
- **One-way by nature.** *"Message queues are a one-way communication mechanism. If a task expects a reply from a service, you might need to implement a mechanism that the service can use to send a response"* (Q-02, MS) — which is why AP-04 and AP-09 are usually composed.
- **Idempotency is now the consumer's job.** *"Most queue services deliver messages with at-least-once semantics… Design consumer logic to be idempotent so that processing the same message multiple times produces the same outcome and avoids problems such as duplicate records or repeated charges"* (Q-02, MS).
- **Ordering is not preserved by default** with parallel consumers (Q-02, MS).
- **Complexity where none is warranted:** *"The workload volume is predictably low and stable, so adding queueing complexity provides little benefit"* (Q-02, MS).
- **A second operating model** — the worker is code with its own pipeline, monitoring and on-call (AT2-53).

**Risks.**
- **Unbounded backlog.** *"If your average producer rate exceeds the consumer rate, the queue continues to grow and latency increases. Monitor queue depth and scale consumers within safe limits, or shed work at the producer"* (Q-02, MS).
- **Overload displacement.** *"Autoscaling without bounding consumers' aggregate downstream rate only moves the overload to downstream dependencies. This overload can increase contention for resources that these services share and diminish the effectiveness of the queue to level the load"* (Q-02, MS). Decisive when the worker writes to Dataverse, whose service-protection limit is per identity (DA-10) — an elastic worker on one service principal will simply move the 429s.
- **Message loss if durability is assumed rather than verified.** *"This pattern depends on queue durability to prevent message loss. If the broker doesn't persist messages to durable storage, a crash or capacity limit can cause enqueued data to be lost before consumers process it. Choose a queue service that persists messages to disk or replicated storage, and understand its size quotas and retention limits"* (Q-02, MS).
- **The wrong transport chosen for the guarantee.** Event Hubs has **no** dead-lettering; only Service Bus has transactions and duplicate detection (Q-09, MS).
- **Dataverse-side emission constraints** if the producer is a plug-in: 192 KB context and, on the Azure-aware path, no VNet (IA-25, IA-28).

**Operational implications.** New operational objects: queue depth, dead-letter depth, consumer lag, worker failures. *"Monitor dead-letter queue depth so that your operations team can investigate failures, fix the underlying problem, and resubmit messages when appropriate"* (Q-02, MS). The instantiation names the toolchain: *"Application Insights and Azure Monitor track function executions, queue health, delivery success, and failures. Dead-letter queues in Service Bus capture undeliverable messages for later analysis"* (Q-17, MS). This is the pattern that most clearly requires an operations owner outside the Power Platform team.

**Security implications.** Positive on secrets: the worker can use managed identity, which the connector path cannot (IA-31). *"Azure Functions use managed identities to securely interact with Dataverse, Service Bus, and Key Vault without storing credentials in code or configuration files"* and *"Store sensitive credentials, such as SendGrid and Twilio keys, only in Azure Key Vault and access them through managed identities"* (Q-17, MS). Private networking is available on the Azure side: *"You can further secure communication between the system's components by using private endpoints and virtual networks"* (Q-17, MS). Caveat: message content now sits at rest in a broker, so data classification applies to the queue (INF over DA-59).

**Scalability implications.** The strongest of the ten patterns, and it is where Microsoft's Power Platform instantiations go when volume is the problem (Q-17: *"Supports thousands of notifications per day while remaining reliable and performant"*; Q-01's fully-decoupled escalation; Q-20's asynchronous clone jobs). The residual ceiling is the *target*, not the pattern — hence the back-pressure caveat above. Consumer scaling must be bounded to the downstream limit, using target-based scaling and scale-out limits (Q-02, MS).

**Governance implications.** A queue/broker is an external governed asset with RBAC, policy, data classification, retention and ownership. “No operator” makes the pattern unavailable (Y-13; `operations-support.md` §1.1/OP-05).

**ALM implications.** Queue/topic configuration and worker code need IaC/CI-CD; message schema and idempotency contract must be versioned with the Power Platform producer/consumer.

**Performance / scale boundary.** The broker buys load levelling, not infinite capacity. Size ingress, backlog growth, worker drain rate, connector calls back into Power Platform and retry bursts.

**Cost implications.** Adds broker operations/storage, compute workers, telemetry, egress where applicable and operational labour. Service tier can be forced by sessions, duplicate detection or DR requirements.

**Operations / recovery.** Dead-letter ownership, replay procedure, oldest-message/backlog alerts and correlation are mandatory for business-critical use. Restore of a consumer data store requires a replay/reconciliation decision before the queue is reopened.

**Power Platform ownership boundary.** Do not emulate a durable queue with flow variables/retry loops. If durable delivery, ordering, replay or poison isolation is the requirement, the broker responsibility belongs outside Power Automate.

**Validation.** V2 pilot under peak/burst plus worker outage; V3 automated idempotency/replay tests for critical workloads.

**When NOT to use.**
- A synchronous low-latency response is required (Q-02, MS) → AP-01 or AP-02.
- Volume is *"predictably low and stable"* (Q-02, MS) → AP-01; the queue is pure complexity.
- Strict global ordering is required and sessions/partitioning cannot express the key → reconsider the requirement; a queue will not give it back.
- Nobody will own the worker and the queue operationally → the pattern is unavailable, not merely expensive. This is the most common real-world disqualifier and it is an organisational fact, not a technical one (INF over AT2-53).
- The requirement is really "keep two stores in step" → AP-07, with §8 of the companion file.

**Alternatives.** AP-03 (when decoupling is needed but guarantees are not), AP-09 (when the issue is duration rather than rate — often composed with AP-04), AP-05 (when the issue is capability), AP-02 (when the issue is protecting the backend from callers — rate limiting rather than buffering), AP-10 (when the enterprise already runs a message backbone).

**Evidence.** Structural: Q-02 in full (context, solution, three benefits, seven considerations, when/when-not, the Functions and Container Apps variants, target-based scaling). Instantiation: Q-01 (the escalation to a queue to prevent 429s), Q-17 (Service Bus + Functions + Dataverse status table + dead-letter + managed identity), Q-20 (Service Bus + Function for beyond-platform-limit work). Transport properties: Q-09.
**Sources:** Q-01, Q-02, Q-09, Q-17, Q-20; IA-15, IA-25, IA-28, IA-31, IA-46; peers DA-10, DA-59, AT2-53.
---

### AP-05 — Hybrid low-code + pro-code (fusion)

```
Power Apps  ──►  Power Automate  ──►  API / Function / Service  ──►  Enterprise system
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH

**Problem solved.** The solution as a whole belongs in Power Platform — the users, the business records, the human workflow, the pace of change — but **one capability** exceeds the platform: computation, duration, a protocol, a delivery guarantee, or an identity requirement. Moving the whole solution is disproportionate; moving the capability is not.

**Appropriate conditions.** Microsoft's worked example gives the shape and the trigger: *"An online banking service wants to qualify customers for loans more quickly. The qualification process involves complex calculations and data retrieval from multiple systems… Following an initial evaluation, the banking service considered cloud flow unsuitable given the complexity of the calculations. However, in this case a hybrid approach is the answer: Power Automate to handle data collection with built-in connectors; Complex calculations encapsulated in custom code running as an Azure Function, which can be independently scaled, or in a custom connector"* (Q-07, MS). The stated strategy: *"Don't choose tools in isolation. Instead, combine their strengths. For example: Use Power Automate for orchestration and connectivity; Use Azure Functions for compute-intensive tasks; Use custom connectors to extend functionality when needed"* (Q-07, MS).

The five documented seams at which to split:
1. **Computation** — algorithm-heavy work; Power Fx lacks imperative loops and mutable local state (PS-08), and Microsoft states that complex business logic and large-scale transformation do not belong in cloud flows (PS-07).
2. **Duration** — beyond 120 s synchronous or beyond the plug-in's hard 2-minute ceiling (PS-09); Q-20 *"relies on Azure services for long-running asynchronous execution beyond platform limits"* (MS).
3. **Protocol** — SOAP outside Logic Apps, EDI/B2B, or anything a connector cannot express (IA-32, Q-34).
4. **Guarantee** — durability, ordering, dead-lettering (composed with AP-04).
5. **Identity** — managed identity is available to Dataverse plug-ins and to Azure workers, and **not** to connectors and flows (IA-31); a "no stored secrets" requirement is satisfied by moving the credential-bearing leg.

Microsoft's fusion-development guidance names when citizen development alone is insufficient: no connector exists, integrity logic must be enforced, complex dynamic business flows (PS-39).

**Architectural structure.** Two variants, and the choice matters:
- **In-platform pro-code** — Dataverse plug-in or Custom API. Runs inside the transaction (so it can enforce integrity), is exempt from service-protection limits for its own data operations (AT2-35), supports managed identity (IA-31), supports VNet (IA-29) — but has a hard 2-minute ceiling (PS-09).
- **Out-of-platform pro-code** — Function / Container App / Logic App Standard behind a custom connector or a queue. No duration ceiling of consequence, full library access, managed identity, private endpoints — but outside the transaction, and a second operating model.

The seam artefact is a custom connector (synchronous) or a queue (asynchronous). Q-18 documents the synchronous variant end to end: canvas app → custom connector → Entra-ID-secured Function → data store, with two Entra ID app registrations.

**Strengths.**
- **Keeps the cheap 80 % cheap.** The user experience, the business records and the human workflow stay in the low-code estate where change is fast.
- **Independent scaling of the expensive part:** *"which can be independently scaled"* (Q-07, MS).
- **Server-side logic is testable in isolation:** *"By shifting the logic from the canvas app to the REST API you should be able to independently test the API separate from the app that uses it"* (Q-18, MS).
- **Server-side shaping reduces client chattiness**, with a documented performance rationale (Q-18, MS) — and the corpus's canvas-performance evidence agrees (AA/PS-06 on large-app degradation).
- **Reuse across consumers** falls out for free (Q-18, MS).
- **Enables requirements the platform cannot meet at all** — managed identity, private endpoints, long-running work, protocols.
- **The in-platform variant has a genuine architectural lever:** plug-in-originated Dataverse operations are exempt from service-protection limits (AT2-35), so the same data work can cost budget in a flow and none in a plug-in.

**Weaknesses.**
- **Two operating models.** Two pipelines, two monitoring surfaces, two skill sets, two on-call rotations. AT2-53 records this as an explicit boundary condition and it is the pattern's dominant cost.
- **More code-first work**, stated in the instantiation: *"more code-first developer work is needed to develop and maintain the RESTful service and data layer"* (Q-18, MS).
- **Deployment coupling between the two halves**, with the mitigation named as a requirement: *"you should ensure you have a tested strategy to mitigate a roll out of either that develops errors after one of the components is updated"* (Q-18, MS).
- **Skills dependency is an architecture criterion, not a staffing detail** (PS-40); a hybrid design without a pro-code team is a design that will not be maintained.
- **The in-platform variant's 2-minute ceiling** is hard and applies even to plug-ins invoked from background operations: *"the two-minute execution time-out applies to any plug-ins invoked during the process"* (Q-21, MS).
- **Portability asymmetry.** .NET plug-in code and data are portable; canvas UI, Power Fx and flow definitions are not (PS-51) — so the hybrid split also splits the exit options.

**Risks.**
- **The seam migrates.** Once a Function exists, the temptation is to move "just one more thing" into it until the low-code half is a thin shell — at which point the platform choice should be revisited honestly rather than by drift (INF over Q-07's TCO instruction).
- **Cost justification is required and often skipped:** *"Every integration decision must consider the total cost of ownership… Justify higher costs with clear business value"* (Q-07, MS).
- **Silent divergence of business rules** across the two halves (X-13); the remedy is one enforcement site, server-side, and Dataverse is the only store with rules enforced *"regardless of the app used to create the data"* (DA-60).
- **Environment/registration hygiene.** *"It is also important that the Entra ID apps registered are separate between the environments to keep the protection of each stage of data and not mix across environments"* (Q-18, MS) — a cross-environment leak is easy to create and hard to notice.

**Operational implications.** Requires telemetry on both halves and a correlation identifier across the seam: *"telemetry should be captured from the REST API component to track its health. For example, using Azure Monitor – Application Insights logging"* (Q-18, MS). Requires a joint release process and a rollback strategy spanning both. Q-20's runbook instruction generalises: *"Implement monitoring across Power Automate runs, Dataverse plugin execution, and Azure Function/Service Bus data. Provide runbooks for common failure patterns"* and *"Document ownership and support processes for apps, plugins, flows, Azure resources, and ERP integrations"* (MS).

**Security implications.** Net positive if done as documented: secrets move to Key Vault accessed by an integration identity (*"Store secrets in Key Vault and access them via an integration identity. Avoid embedding secrets in flows, apps, or source control"* — Q-20, MS); the Azure leg can use managed identity (IA-31); the backend can be network-isolated (Q-19). Net negative if done casually: a Function with a stored connection string in app settings and a custom connector with a shared API key is a *worse* posture than a governed connector, because it is outside DLP's visibility (INF over PS-29's connector-scoped DLP model).

**Scalability implications.** The pattern's purpose. The Azure half scales on its own plan; the Power Platform half remains bound by the three meters for whatever still runs there. Where the seam is a queue, AP-04's back-pressure caveat applies. Where the seam is a synchronous custom connector, the 120 s ceiling and the custom-connector throttle (CONFLICTED — 500 or 10,000/min, IA-C-01) still bind the call path.

**Governance implications.** Hybrid means two governance planes. Power Platform controls do not govern the Azure/custom half; assign Azure RBAC/Policy, inventory, budget tags and a named platform/application owner.

**ALM implications.** Two supply chains are mandatory. Custom connectors inherit ALM-14 hazards; Azure code/infrastructure needs source control, IaC/CI-CD and compatible contract versioning. A joint release needs sequencing and fix-forward/rollback coordination.

**Performance / scale boundary.** Move only the capability that exceeds the low-code envelope. The Power Platform caller and return path still have their own timeouts/throttles; hybrid does not prove performance.

**Cost implications.** Power Platform licence/capacity plus Azure consumption, monitoring, environments and pro-dev/operations effort. A hybrid option without this second cost model is incomplete.

**Operations / recovery.** Requires end-to-end correlation, Azure monitoring/alerts, support ownership, runbooks and a recovery sequence across both estates.

**Power Platform ownership boundary.** If the pro-code half becomes the dominant business logic, state owner or operational burden, reassess whether Power Platform should remain more than a UX/orchestration edge.

**Validation.** V2 pilot for the cross-boundary path; V3 automated contract/function tests; V4 where private networking or managed-environment controls are required.

**When NOT to use.**
- The problem is volume rather than capability → AP-04 first; a Function behind a synchronous connector does not solve throttling.
- There is no pro-code team, or no owner for the Azure resources → the pattern is unavailable (AT2-53, PS-40).
- The whole solution is really pro-code with a Power Apps veneer → make the platform decision explicitly (PS-04's mission-critical framing; PS-41's *configure or buy before build*).
- One step is slow but inside the limits → optimise in place; the hybrid's fixed cost is not repaid by a marginal gain.
- The requirement is integrity enforcement rather than computation → the in-platform variant (plug-in / Custom API), not an external service, because only the in-platform variant runs inside the transaction (AT2-35, PS-45).

**Alternatives.** AP-01 (if the capability turns out to be within limits), AP-02 (if reuse and contract are the real drivers), AP-04 (if the driver is rate or durability), AP-09 (if the driver is only duration), AP-10 (if the enterprise already owns the compute or the protocol handling).

**Evidence.** Structural and instantiation both: Q-07 (the hybrid example, the strategy, the TCO instruction), Q-18 (full synchronous instantiation with rationale, cost, testing, deployment and security considerations), Q-20 (asynchronous instantiation beyond platform limits, plus reliability/security/operational considerations), Q-21 (the plug-in 2-minute ceiling inside background operations), Q-34 (Durable Functions vs Logic Apps division of labour).
**Sources:** Q-07, Q-18, Q-19, Q-20, Q-21, Q-34; IA-24, IA-31, IA-32; peers PS-04, PS-07, PS-08, PS-09, PS-39, PS-40, PS-41, PS-45, PS-51, DA-60, AT2-35, AT2-53.

---

### AP-06 — Data virtualization

```
Power Platform  ──►  Virtual access (Dataverse virtual table / connector)  ──►  External data platform
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH (the limitation list is unusually well documented)

**Problem solved.** Data owned elsewhere must be usable inside Power Platform experiences **without copying it**. *"Virtual tables… enable the integration of data residing in external systems with Microsoft Dataverse. This integration seamlessly represents that external data as tables in Dataverse, without replication of data and often without custom coding"* (Q-13, MS).

**Appropriate conditions.**
- The data is **reference or read-oriented** and another system is its system of record (IA-36).
- Table-level authorization is sufficient — *"In Dataverse, a security role on the table grants table-level permission"* (Q-26, MS).
- None of the platform data features on the exclusion list are required (see Weaknesses).
- The external store can serve interactive query volumes at the required frequency (IA-06), and its **upstream** refresh cadence satisfies the freshness requirement (see Risks).
- The external data can be modelled as a Dataverse table: *"All tables in the external data source must have an associated GUID primary key"*, all properties expressible as Dataverse columns, relationships modellable (Q-13, MS).

**Architectural structure.** Dataverse virtual table + data provider (OData v4 shipped in-box with full CRUD; Cosmos DB provider from Marketplace; or a custom provider implemented as plug-ins, which now support full CRUD) → external store. Regular Dataverse tables may hold lookups to the virtual tables, which is how Q-14's design combines *"editable Dataverse records"* with *"read-only enterprise data"*. A non-Dataverse variant of the same intent is a connector reading the source per screen — cheaper but without the Dataverse-native experience.

**Strengths.**
- **No copy, therefore no synchronization risk register.** The entire §8 register of the companion file simply does not apply. This is the pattern's decisive advantage and it is chronically undervalued.
- **Single source of truth preserved** — the owning system stays authoritative (IA-36, IA-37).
- **Native experience.** The data appears as tables, so model-driven apps, views, forms and lookups work over it (Q-14's instantiation).
- **Heavy work stays where it belongs:** *"Use the data warehouse for heavy processing, and keep only lightweight references in Dataverse to ensure the architecture scales"* (Q-14, MS).
- **No storage meter consumption** for the virtualized data (INF over DA-04's meter model — the data is not persisted in Dataverse).
- **Explicitly presented as replacing worse alternatives:** *"Virtual tables replace previous client-side and server-side approaches to integrating external data, which required customized code and suffered from numerous limitations. These limitations include imperfect integration, data duplication, or extensive commitment of development resources"* (Q-13, MS).

**Weaknesses.** This is the most consequential list in the file, quoted from Q-13 (MS) unless noted:
- *"Only organization-owned tables are supported. The security filtering applied to user-owned tables isn't supported."*
- *"Field-level security isn't supported."*
- Row-level permissions and source-side per-user validation are **not possible** (Q-26, MS).
- *"Auditing isn't supported."*
- *"Search functionality isn't supported for virtual tables as they don't persist data."*
- *"Charts and dashboards aren't supported for virtual tables."*
- *"Virtual tables can't be enabled for queues."*
- *"Offline caching of values isn't supported for virtual tables."*
- *"A virtual table can't represent an activity and don't support business process flows."*
- *"A column on a virtual table can't be calculated or rollup."*
- *"Although you can add virtual table columns as a lookup on a grid or other UI views, you can't filter or sort based on this virtual table lookup column."*
- *"Once created, a virtual table can't be changed to be a standard (nonvirtual) table. The reverse is also true."* — an irreversible schema decision.
- **`$select` is ignored:** *"Selecting attributes in Retrieve and RetrieveMultiple queries won't be applied since all attributes are returned"* — so payload cannot be narrowed, a hidden cost on wide tables.
- *"Reduce and limit including virtual table lookup columns in your grid view. It can take a while to read the virtual table lookup columns."*

**Risks.**
- **False freshness.** *"They query the data warehouse in real time. This process means the request uses the warehouse data available at creation time. **However, the actual freshness of that data depends on how frequently the upstream source systems load and refresh the data warehouse**"* (Q-14, MS). A live-looking query over a nightly-loaded store is stale data with a real-time UI.
- **Runtime dependency on the external store.** Every read is a call; the store's availability and latency become the app's. The mitigation is explicit: *"Ensure the data warehouse is resilient to failure and has high availability"* (Q-14, MS).
- **Query-volume amplification.** A grid over a virtual table can generate per-row reads for lookup columns (Q-13's own warning), and `$select` cannot reduce the payload.
- **Authorization gap discovered late.** Teams choose virtual tables for elegance and discover the row-level-security exclusion in security review. Q-15 records exactly this outcome twice: *"Using virtual tables isn't feasible when the secondary system's tables already exist and require row-level security"* and *"The team rejected virtual tables because the financial team needed to enrich records with department-specific attributes governed by strict row-level security"* (MS).
- **Irreversibility** — the virtual/standard decision cannot be changed in place (Q-13, MS).

**Operational implications.** Two monitoring surfaces again: *"Enable monitoring at each stage—from data warehouse ingestion to Dataverse virtual table usage—to quickly detect data quality or connectivity issues"* (Q-14, MS). The upstream load cadence becomes a cross-team dependency that must be owned and watched. Data quality is inherited: *"Use cleaned-up data in the data warehouse to ensure completeness and data quality in the virtual tables"* (Q-14, MS).

**Security implications.** Weaker than native Dataverse by design: table-level only, no field-level security, no audit. The documented compensating posture is to restrict the surface: *"Restrict access to the virtual tables to read access only"* and *"Ensure the data warehouse data is read-only and only visible in the Power Apps application and referenceable from regular Dataverse tables"* (Q-14, MS). For SAP specifically the trade-off is stated as a pro/con pair (Q-26, MS). Where per-user authorization at the source is a compliance requirement, this pattern is **excluded**.

**Scalability implications.** Scales with the external store, not with Dataverse — which is the point when the store is a warehouse. The documented levers are surface reduction and on-demand retrieval: *"Only expose the required datasets using virtual tables to minimize query load"*, *"Optimize Power Apps screens and Dataverse tables to retrieve data on demand rather than loading full datasets"*, *"Trigger Power Automate flows only when necessary"* (Q-14, MS). Peers add the delegation caveat: PS-13's silent 500/2,000-row truncation applies to how the app queries, independent of virtualization.

**Governance implications.** External source remains authoritative. Govern who may expose it as a virtual table, which tables/columns are visible and who owns the upstream availability/security contract.

**ALM implications.** Provider/configuration changes and environment bindings must be deployable and revalidated; the upstream schema is an external dependency that can break the app without a Power Platform release.

**Performance / scale boundary.** Microsoft publishes no general virtual-table throughput/latency envelope; source capability and provider behaviour govern. Treat performance as `UNKNOWN` until a representative V2 pilot.

**Cost implications.** Avoids data-copy/storage/reconciliation cost but can import premium connector/provider and upstream platform cost.

**Operations / recovery.** No local copy means upstream outage is immediately visible to the application. Recovery is primarily upstream; cache/offline/replay assumptions must not be invented.

**Power Platform ownership boundary.** Correct when Power Platform should not own the data. If native Dataverse security/audit/offline or deterministic performance is required, replicate or choose another application/data architecture.

**Validation.** V2 representative source/data-volume/security test is mandatory for material workloads.

**When NOT to use.**
- Row-level or field-level security is required on that data (Q-13, Q-15, Q-26) → AP-07.
- Audit, search, charts, offline, queues, activities or business process flows are required on that data (Q-13) → AP-07.
- The data must be enriched with local attributes governed by local security (Q-15's actual case) → AP-07.
- Freshness must be tighter than the upstream load cadence (Q-14) → AP-07 with a faster path, or fix the upstream.
- The external store cannot serve interactive query volume (IA-06) → AP-07, or AP-04-buffered reads, or Q-01's data-lake read-offload variant.
- Write-heavy transactional use — even though CRUD is supported, the pattern's evidence base and Microsoft's own instantiations are read-oriented (INF; APR-U-06).

**Alternatives.** AP-07 (copy it and accept the sync risk), AP-02/AP-08 (query it through an API per operation rather than modelling it as a table — better when the access is operation-shaped rather than table-shaped), AP-01 with a connector (simplest, no Dataverse modelling, no native experience), and Q-01's read-offload variant (interpose a scalable store between the source and the consumer purely to absorb reads).

**Evidence.** Q-13 (definition, providers, modelling requirements, the full limitation list), Q-14 (the warehouse instantiation with the freshness caveat and all five pillar considerations), Q-26 (the SAP pro/con pair), Q-15 (two independent rejection cases with stated reasons — unusually valuable negative evidence).
**Sources:** Q-13, Q-14, Q-15, Q-26; IA-34, IA-43; peers PS-13, PS-56, DA-04, DA-45.

---

### AP-07 — Data replication / synchronization

```
System of Record  ──►  Integration  ──►  Dataverse / other store
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH

**Problem solved.** Data owned elsewhere must live locally — because platform data features are required on it (row-level security, audit, search, offline, charts, business process flows), because local enrichment is needed, because the source cannot serve the query volume, or because latency or residency demands a local copy.

**Appropriate conditions.** Microsoft's stated reasons, verbatim: *"Although storing the same data twice might seem inefficient, this pattern supports specific business needs, such as performance and regulatory compliance. **Performance**: Local data access improves responsiveness, especially in latency-sensitive industries. **Compliance**: Legal regulations might require data to be stored within national borders. Organizations often deploy local instances with synchronization processes to meet these requirements"* (Q-07). Add the empirically-observed reason from Q-15: virtual tables were rejected because *"the financial team needed to enrich records with department-specific attributes governed by strict row-level security"* (MS) — i.e. **AP-06's exclusion list is AP-07's justification list**.

**Architectural structure.** The documented shape is **three components, not one** (IA-41):
1. **Event path** for latency — *"CRUD operations in the primary Dataverse environment trigger Power Automate flows… A cloud flow sends an HTTP POST to a published endpoint. A subscriber cloud flow is triggered by the webhook, processes the payload, and applies the update in the secondary Dataverse environment in near real-time"* (Q-15, MS).
2. **Bulk path** for correctness and initial load — dataflows *"Ideal for bulk operations, such as initial data population and synchronization… Upserts are performed by using an alternate key to avoid duplicates"* (Q-15, MS).
3. **Reconciliation** — *"Nightly dataflows in the secondary environment correct any missed or failed event-driven updates"* (Q-15, MS).
Plus a companion flow for what dataflows cannot do: *"a dataflow can't change row statuses or delete records that are removed (absent) in the primary Dataverse environment"* (Q-15, MS).

For ERP the documented shape is different and narrower: *"three patterns—virtual entities (read), dual-write (write), and an OData API"* with financial posting entities **excluded** from dual-write (Q-20, MS).

**Strengths.**
- **Full platform data features** on the replicated data — the entire AP-06 exclusion list becomes available (row-level security, audit, search, offline, charts, activities, BPFs).
- **Local enrichment** — the copy can carry columns the source does not have (Q-15's actual driver).
- **Local performance and residency** (Q-07's two stated reasons).
- **Source protection** — the source is read on a schedule rather than per user action; this is the read-offload logic of Q-01's data-lake escalation.
- **Idempotency has a documented mechanism** — alternate keys plus upsert (Q-15, MS), with limits at DA-53.
- **Reconciliation is designed in**, which makes eventual correctness a property of the design rather than a hope (Q-15, MS).

**Weaknesses.**
- **Two copies means two truths in the window between them.** *"Power Automate is asynchronous and doesn't guarantee real-time performance. If business users expect immediate data availability, clarify limitations early in the design process"* (Q-07, MS).
- **Dataflow floors and gaps:** 30-minute increments, ≤ 48 refreshes/24 h, 24 h maximum run (DA-49); cannot delete rows or change statuses; **cannot be owned by a service principal**; connection must be manually re-established after each deployment unless isolated in its own solution (Q-15, MS).
- **Throughput exposure:** *"High-frequency CRUD activity can trigger throttling, especially in scenarios where flows execute tens of thousands of actions per day. For business-critical or high-throughput integrations, apply appropriate Power Automate licensing to increase throughput limits"* (Q-15, MS) — licensing as a reliability control again (IA-16).
- **Manual residue is admitted:** *"Manual intervention might be required for data quality problems (for example, missing keys)"* (Q-15, MS).
- **Fan-out does not scale:** *"This architecture is designed for a one-to-one relationship… Scenarios where one master environment must synchronize with multiple other environments require a more scalable or distributed solution"* (Q-15, MS).
- **The bidirectional variant is tightly coupled by Microsoft's own description:** dual-write is *"tightly coupled, bidirectional"* and *"Synchronous"*, and it **mutates the Dataverse schema** — company, party, date effectivity, optional 10-decimal currency (Q-28, MS).
- **Storage cost.** The copy consumes the Dataverse database meter, which is the most expensive of the three (DA-04, DA-62).

**Risks.** The whole of `integration-architecture.md` §8 applies. The five sharpest:
- **Silent divergence** — the reference design *assumes* the fast path loses updates, which is why reconciliation exists (Q-15). A design without reconciliation is divergent by construction.
- **Self-triggering loops** in bidirectional sync (Q-07, Q-23, and the presence-not-change trigger semantics of Q-38).
- **Conflicting writes** without a per-field owner (DA-48).
- **Copy proliferation for reporting** — Microsoft's named anti-pattern: *"Too much data synchronized with Dynamics 365 for reporting purposes that overloads the database. You should use a dedicated data warehouse"* (DA-51, MS).
- **Shadow system of record** — Microsoft's own remedy is exclusion by design: *"Financial posting entities… are deliberately excluded from dual-write, avoiding any shadow-ERP behavior"* (Q-20, MS).

**Operational implications.** Requires: a reconciliation schedule with an owner; failure alerting on both paths (*"Monitoring and alerting for failed syncs"*, Q-15, MS); a divergence report; and a manual-intervention runbook for key problems. Dataflow ALM has a documented quirk that must be designed around: *"after each deployment, you must manually re-establish the dataflow connection. By placing dataflows in a separate solution that you deploy only when you change the dataflows, you avoid unnecessary manual work"* (Q-15, MS). Ownership is constrained: *"Service accounts and security groups for access control. When using dataflows, you can't assign service principals as owners"* (Q-15, MS) — a named human owns the pipeline, which reintroduces the leaver risk (AT2-01).

**Security implications.** Positive: the copy gets Dataverse's security model (roles, business units, row sharing, column security — PS-31), which is precisely why the pattern is chosen over AP-06. Negative: sensitive data now exists in two places, so classification, retention and erasure obligations double (DA-59, DA-60). Selective replication is the documented mitigation — Q-07's compliance example synchronizes only non-sensitive data: *"Configure filters to: Monitor only allowed fields; Prevent synchronization of restricted data"* and *"Medical data is excluded from synchronization"* (MS). That is a strong, reusable idea: **replicate the fields, not the record**.

**Scalability implications.** Bulk path scales on the dataflow engine within its floors; event path is bound by the three meters and is the part that throttles (Q-15's own warning). Fan-out beyond 1:1 is explicitly outside the pattern (Q-15). Above that, the structure must change to publish-once/subscribe-many — i.e. AP-03/AP-04 with the store as one subscriber among several.

**Governance implications.** Duplication creates two controlled data estates. Define system/field ownership, retention/erasure responsibility, reconciliation owner and who may replay failed changes.

**ALM implications.** Mapping, filters, keys and reconciliation logic are versioned integration artefacts. Deployment order matters when schemas change.

**Performance / scale boundary.** Size steady-state sync plus re-seed/reconciliation and retry bursts. Freshness is an SLA requirement, not “near-real-time” prose.

**Cost implications.** Pays twice for storage/security/operations and adds sync execution. Selective replication is the primary cost/risk control.

**Operations / recovery.** Restore-induced divergence is a first-class failure mode. After either side is restored, pause writers and explicitly re-baseline/replay/reconcile before normal operation.

**Power Platform ownership boundary.** Do not copy data merely to avoid solving an API/security problem. If the external system can remain authoritative and the app only needs read-through, AP-06 or AP-02 is safer.

**Validation.** V2 failure/recovery test including duplicates, conflicting writes, missed/deleted rows and re-seed; V3 reconciliation assertions for critical data.

**When NOT to use.**
- The data can be read in place with acceptable freshness and no platform-data-feature requirement → AP-06. Choose AP-07 only against a named item on AP-06's exclusion list.
- The driver is reporting → analytical copy paths (Fabric link DA-19, Synapse Link DA-20), not operational sync (DA-51).
- More than one target environment or system → the pattern does not scale; publish once instead (Q-15).
- Bidirectional with no per-field owner defined → do not start; define ownership first (DA-48).
- The entity is another system's authoritative ledger → read it (Q-20's exclusion).
- No owner for the reconciliation pass → the correctness guarantee is absent, so the pattern is not actually available (INF over Q-15).

**Alternatives.** AP-06 (no copy), AP-04 (publish once, let each store subscribe), the analytical copy paths (reporting), dual-write (Microsoft's tightly-coupled bidirectional option, with its schema cost — Q-28), and AP-10 (the enterprise's MDM or integration platform owns the mastering).

**Evidence.** Q-15 in full (the three-component design, the dataflow limitations, the ownership constraints, the ALM quirk, the throttling warning, the two virtual-table rejection reasons, the 1:1 scope statement), Q-07 (the synchronization pattern, its two justifications, selective-field filtering, the realism warning on real-time expectations), Q-20 (the ERP three-pattern split and the shadow-ERP exclusion), Q-28 (dual-write's coupling and schema impact).
**Sources:** Q-07, Q-15, Q-20, Q-23, Q-28, Q-38; IA-36…IA-38, IA-41, IA-42; peers PS-31, DA-04, DA-19, DA-20, DA-48, DA-49, DA-51, DA-53, DA-59, DA-60, DA-62, AT2-01.
---

### AP-08 — API facade / backend-for-frontend

```
Power Apps  ──►  API facade  ──►  Multiple backend services
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH (structurally) / MEDIUM (as a Power Platform pattern — see the note below)

**Note on scope.** AP-08 is a *specialisation* of AP-02, not a peer. AP-02 mediates one backend for many consumers; AP-08 composes **many backends for one client operation**. Microsoft's generic pattern for the composition half is Gateway Aggregation (Q-04); the anti-corruption variant is Q-05. The Power Platform instantiation evidence is Q-18, which describes the intent without using the BFF vocabulary: *"This approach can also allow the Power Apps application to act as an integrator of multiple backend services providing a single view to the user of data and logic from all the sources"* (MS). Because the *naming* is this file's, the pattern is tagged MEDIUM as a Power Platform pattern even though its structural evidence is strong.

**Problem solved.** One client operation — a screen, a step, a decision — needs data or actions from several backends. Doing it client-side means N round trips, N failure modes, N auth configurations and N sets of paging logic inside Power Fx or inside a flow.

**Appropriate conditions.**
- *"A client needs to communicate with multiple back-end services to perform an operation"* (Q-04, MS).
- *"The client might use networks that have significant latency, such as cellular networks"* (Q-04, MS) — directly relevant to mobile Power Apps.
- The client's view is stable enough to be worth a purpose-built contract; the facade is shaped for *this* consumer.
- The backend contracts are semantically hostile or legacy, and their shape should not leak into the client — the anti-corruption condition: *"When you maintain access between new and legacy systems, you force the new system to adhere to at least some of the legacy system's APIs or other semantics. When these legacy features have quality problems, this support corrupts what might otherwise be a cleanly designed modern application"* (Q-05, MS).
- Chattiness is measurably hurting the client: *"evaluation of how Power Apps using different data sources directly might be too chatty with the data sources. This can create a performance slowdown due to the latency of the individual request being sent to each data store"* (Q-18, MS).

**Architectural structure.** Power Apps → custom connector → facade (APIM with `send-request` policies for lightweight composition, or a Function/service for anything with domain logic) → N backends. The documented placement rule is firm: *"This approach works well when the gateway performs lightweight composition, shaping, and response assembly. If the aggregation requires custom domain logic, complex transformations, or longer-running orchestration, place that functionality in a dedicated custom service behind the gateway"* (Q-04, MS). The anti-corruption variant places translation — and **only** translation — in the layer: *"it's important to focus the anti-corruption layer on translation logic. Avoid placing business rules or orchestration in the layer"* (Q-05, MS).

**Strengths.**
- **One round trip instead of N**, with the client-side benefit stated: *"This pattern can reduce the number of requests that the application makes to back-end services and improve application performance over high-latency networks"* (Q-04, MS).
- **Server-side shaping**, which is the documented Power Platform performance argument: *"the data response can be shaped server-side and delivered to the client more efficiently"* (Q-18, MS).
- **Transient-fault handling centralised:** *"you can shift transient fault handling from a distributed implementation across clients to a centralized implementation"* (Q-04, MS) — which matters because the client-side implementation would be flow retry policies whose depth depends on a licence (IA-17).
- **Reduced attack surface:** *"This topology often reduces the number of touchpoints that a client has with a system, which reduces the public surface area and authentication points. The aggregated back ends can remain fully network-isolated from clients"* (Q-04, MS).
- **Backends evolve independently:** *"This pattern enables back-end logic to evolve independently from clients. This decoupling gives you the flexibility to change the chained service implementations, or even data sources, without needing to change client touchpoints"* (Q-04, MS).
- **Caching at the composition point:** *"Caching in aggregation implementations minimizes calls to back-end systems"* (Q-04, MS).
- **The domain model is protected** in the anti-corruption variant — *"you can keep one system unchanged without compromising the design and technological approach of the other"* (Q-05, MS).

**Weaknesses.**
- **A new component to own, scale and monitor** — *"The anti-corruption layer adds an extra service that you must manage and maintain"* and *"Consider how you plan to scale the anti-corruption layer"* (Q-05, MS).
- **Added latency** — *"The anti-corruption layer adds latency to calls between the two systems"* (Q-05, MS).
- **Coupling risk in the wrong direction:** *"The gateway shouldn't introduce service coupling across the back-end services"* (Q-04, MS) — a facade that makes backends depend on each other is worse than the chattiness it replaced.
- **A facade per consumer multiplies facades.** The BFF idea is deliberately consumer-specific, so three clients can mean three facades — and on Power Platform the custom-connector count cap (1 on seeded plans, IA-13) pushes the other way.
- **Placement discipline required**, or the facade becomes the monolith (X-12).

**Risks.**
- **SPoF and bottleneck** — the same two risks as AP-02, and here they are sharper because every client operation depends on the facade: *"The gateway service might introduce a single point of failure"*; *"The gateway might introduce a bottleneck"*; *"Perform load testing against the gateway to ensure that you don't introduce cascading failures for services"* (Q-04, MS).
- **Partial failure must be an explicit product decision.** *"If one or more service calls take too long, it might be acceptable to time out and return a partial set of data. Consider how your application will handle this scenario"*, and *"If one of the back-end calls times out or returns an error, API Management can apply the behavior that best fits the operation. For example, it might return a partial response when missing data is acceptable, or it might fail the entire request when complete and consistent order data is required. **Make this decision explicit in the policy design so that clients experience predictable behavior**"* (Q-04, MS). This is the single most commonly skipped design step in the pattern.
- **Debuggability collapses without correlation:** *"Implement distributed tracing by using correlation IDs to track each individual call"* (Q-04, MS); the anti-corruption variant adds *"Plan for observability, including correlation IDs and structured logging, to diagnose translation failures"* (Q-05, MS).
- **The facade becomes permanent by accident.** In a migration context the layer should have an end date: *"If the anti-corruption layer is part of an application migration strategy, consider whether it's permanent or whether you plan to retire it after you migrate all legacy functionality"* (Q-05, MS).

**Operational implications.** Requires full-path telemetry, because a single client operation now has N+1 hops: *"collect telemetry across the full request path so that you can correlate API Management behavior with back-end latency. This visibility is important in a gateway aggregation pattern because a single client operation depends on multiple back-end calls, and failures or slow responses in any one dependency can affect the final aggregated result"*, with the concrete outcome *"you can detect timeout patterns, identify which back-end dependency caused a partial or failed response, and create alerts for elevated latency or error rates"* (Q-04, MS). Resilience must be implemented, not assumed: *"Implement a resilient design by using techniques such as bulkheads, circuit breaking, retry, and timeouts"* and *"Harden your API Management policies by using per-request timeouts, conditional error handling, and circuit breakers"* (Q-04, MS).

**Security implications.** Net positive (surface reduction, network isolation of backends — Q-04, MS). One addition specific to the anti-corruption variant: *"Because the anti-corruption layer mediates systems that might have different trust levels, consider enforcing input validation and sanitization at this boundary"* (Q-05, MS). The facade is also the natural place to apply a single authorization decision — with the caveat that a facade calling backends with its own identity *replaces* per-user backend authorization, which may be exactly what compliance forbids (INF over IA-33).

**Scalability implications.** *"The gateway should be located near the back-end services to reduce latency as much as possible"*, *"Use asynchronous input and output (I/O) to ensure that a delay at the back end doesn't cause performance problems in the application"*, and *"Monitor request metrics and response sizes"* (Q-04, MS). The facade's capacity must be planned for growth explicitly, because it now carries every client operation.

**Governance implications.** The facade owns a semantic contract, not just routing. Assign API governance, authorization-policy ownership, data-classification review and change approval.

**ALM implications.** Custom connector consumers inherit ALM-14. The facade needs source control/IaC/CI-CD and versioned backend adapters; anti-corruption mappings must be regression tested. If the canvas custom-connector workaround would create a forbidden unmanaged layer, redesign the consumption seam.

**Performance / scale boundary.** Aggregation reduces client round trips but can concentrate latency and failure. Define partial-failure policy and test worst-backend latency; the facade can become the bottleneck.

**Cost implications.** Adds runtime/telemetry/operator cost in exchange for reuse, contract stability and reduced client complexity.

**Operations / recovery.** Correlate each aggregate request across backend calls; define partial vs whole-request failure. Recovery of one backend must not silently return stale/inconsistent aggregates.

**Power Platform ownership boundary.** If semantic mediation serves multiple platforms, it belongs to the enterprise API/application platform, not inside one Power Platform solution.

**Validation.** V2 latency/failure pilot; V3 API contract and partial-failure regression tests.

**When NOT to use.**
- *"You want to reduce the number of calls between a client and a single service across multiple operations. In that scenario, adding a batch operation to the service might be more suitable"* (Q-04, MS) — i.e. batching beats a facade for single-backend chattiness. In Dataverse terms that is `$batch` (IA-20).
- *"The client or application is located near the back-end services and latency isn't a significant factor"* (Q-04, MS).
- *"The new and legacy systems have no significant semantic differences"* (Q-05, MS) — for the anti-corruption variant.
- The composition is really one backend plus a lookup → AP-01 or AP-02.
- The requirement is durability or ordering → AP-04. A facade under load is a bottleneck, not a buffer.
- Nobody will define the partial-failure behaviour → the pattern will produce unpredictable client behaviour; resolve that first (Q-04's *"Make this decision explicit"*).

**Alternatives.** AP-02 (mediate, don't compose), batch operations on a single backend (Q-04's own alternative; `$batch` for Dataverse), AP-06 (model the external data as tables and let the platform do the joining — where table-shaped access fits), AP-04 (when the client can be told "we'll get back to you"), AP-10 (when the enterprise's integration layer already composes).

**Evidence.** Structural: Q-04 in full (problem, solution, ten considerations, when/when-not, the APIM instantiation with `send-request`, the telemetry guidance, the partial-failure instruction); Q-05 in full (context, solution, eleven considerations, when/when-not, the APIM+Functions conceptual implementation, the asynchronous variant). Instantiation: Q-18 (Power Apps as integrator of multiple backends; chattiness; server-side shaping; caching; telemetry).
**Sources:** Q-04, Q-05, Q-18, Q-24; IA-13, IA-17, IA-20, IA-33, IA-49.

---

### AP-09 — Background processing

```
User-facing application  ──►  Asynchronous processing  ──►  Worker / automation
                                        │
                                        └──►  Status resource  ◄── polled or pushed to the client
```

**Classification:** PATTERN · **Origin:** MS · **Confidence:** HIGH

**Problem solved.** Work must happen, but the user (or the calling system) must not wait for it — because it exceeds a synchronous window, because it is resource-intensive, because it involves human waits, or because it must survive restarts.

**Appropriate conditions.** Microsoft's test: *"To choose which task to designate as a background job, consider whether the task runs without user interaction and whether the UI needs to wait for the task to complete. Tasks that require the user or the UI to wait while they run are typically not appropriate background jobs"* (Q-23, MS). The named job types: *"Resource-intensive jobs that take a long time to complete… Batch jobs, such as nightly data updates or scheduled processing… Long-running workflows, such as order fulfillment or provisioning services and systems… Workflows that require asynchronous collaboration, such as approvals… Sensitive-data processing that transfers the task to a more secure location for processing"* (Q-23, MS). Plus the hard triggers: 120 s synchronous windows, 180 s canvas, 2-minute plug-in ceiling (IA-09).

**Architectural structure.** Three parts, and the third is the one that gets omitted:
1. **Dispatch** — an event, a schedule, or an explicit request. *"Initiate background jobs with: Event-driven triggers… Schedule-driven triggers"* (Q-23, MS).
2. **Execution** — a flow, a Dataverse background operation (*"Background operations are used to send requests that Dataverse processes asynchronously"* — Q-21, MS), or an external worker (AP-04/AP-05).
3. **Status resource** — the artefact that makes the pattern operable. *"If you require a background task to communicate with the calling task to indicate progress or completion, you must implement a mechanism such as: Write a status indicator value to storage that's accessible to the UI or the caller task… Expose an API or endpoint from the background task that the UI or caller can access to obtain status information… Configure the background task to respond with the status or the data that it processed back to the UI"* (Q-23, MS). Dataverse's platform version: *"you receive notifications by: Including a callback URL with your request. Subscribing to the `OnBackgroundOperationComplete` event"* (Q-21, MS). The HTTP contract version is Q-03's 202 + `Location` + `Retry-After` + status endpoint.

**Strengths.**
- **Responsiveness.** *"Background jobs help minimize the load on the application UI, which improves availability and reduces interactive response time"* (Q-23, MS).
- **The platform supports "respond then continue" natively:** *"Child flows that start before the response action continue running separately, and actions after the response action continue running beyond this limit, enabling a flow to respond and continue running other operations"* (Q-30, MS).
- **Long windows are available** where the backend cooperates: *"Outbound asynchronous request | Configurable up to 30 days"* (Q-30, MS).
- **Dataverse offers a first-class asynchronous request mechanism** with a documented retry: *"The system retries the failed request up to three times, using an exponential backoff strategy"*, and it *"eliminate[s] the need to maintain a persistent connection during execution"* (Q-21, MS).
- **Checkpointing is the documented resilience mechanism:** *"Background tasks need to gracefully handle restarts without corrupting data or introducing inconsistency… For long-running or multistep tasks, consider using checkpoints. Use checkpoints to save the state of jobs in persistent storage or as messages in a queue and configure retry logic in case of unexpected failures of an action"* (Q-23, MS).
- **Composes naturally with AP-04:** *"When you use queues to communicate with background tasks, the queues can act as a buffer to store requests that are sent to the tasks while the application is under higher than usual load. The tasks can catch up with the UI during less busy periods, and restarts don't block the UI"* (Q-23, MS).

**Weaknesses.**
- **The UX gets harder, and Microsoft says so:** *"background jobs might require the user to wait for a notification, refresh the page, or manually check the status of the task. These behaviors can increase the complexity of the user interaction and negatively affect the user experience"* (Q-23, MS). The recommended mitigations are a status list page or a push notification rather than client polling (Q-23, MS).
- **Coordination and consistency problems appear:** *"Background jobs can create challenges for data synchronization and process coordination, especially if the background tasks depend on each other or on other data sources. For example, background jobs might handle data consistency problems, race conditions, deadlocks, or timeouts"* (Q-23, MS).
- **More components, more cost** — Microsoft's explicit trade-off: *"Background jobs introduce more components and dependencies to the system, which can increase the complexity and maintenance costs of the solution. For example, background jobs might require a separate monitoring service and retry mechanism"* (Q-23, MS).
- **Polling costs.** Q-03's HTTP variant requires a `Retry-After` discipline or the client hammers the status endpoint: *"This header helps polling clients avoid sending too many requests to the back end"* (MS). On Power Platform each poll is a request against the meters.
- **The status resource has a lifecycle:** *"The status resource and any stored results consume storage and compute. Define a retention policy to clean them up after a reasonable period"* (Q-03, MS) — and in Dataverse that lands on the database meter (DA-04, DA-27).
- **Low-code clients may not honour the contract:** *"Clients that others author, including clients built by using no-code or low-code tools like Azure Logic Apps, can apply their own handling for HTTP 202"* (Q-03, MS) — a caution that applies directly to Power Platform as a *consumer* of someone else's asynchronous API.

**Risks.**
- **Bottleneck displacement:** *"To prevent the loss of performance under load, you might implement logic so that a single point of the processing chain doesn't cause a bottleneck. Consider other limitations, such as the maximum throughput of workflow actions, storage, and other services that the application and the background tasks rely on"* (Q-23, MS).
- **Duplicate submission.** Q-03's remedy is an idempotency key: *"You can require clients to supply an idempotency key… If the back end receives a duplicate key, it should return the existing status resource instead of enqueuing a second work item. This approach protects against network failures that cause the client to retry a POST that the server already accepted. **It's especially important in this pattern because the client can't distinguish between a lost response and a request that was never received**"* (MS).
- **Abandoned work.** Cancellation must be designed: *"To provide a way for clients to cancel a long-running request, expose a DELETE operation on the status endpoint resource… Determine whether the operation supports partial rollback or requires a compensating transaction"* (Q-03, MS). Q-17's instantiation does exactly this with Service Bus sequence numbers.
- **Recovery of multi-step work:** *"Manage the recovery for task steps that fail. If one or more of the steps fail, an application might need to undo the work that a series of steps performs, which together defines an eventually consistent operation"* (Q-23, MS). This is the compensating-transaction obligation, and Power Platform has no construct for it (IA-19, IA-46).
- **The plug-in ceiling still applies inside background operations:** *"When using Dataverse background operations to execute requests asynchronously, the two-minute execution time-out applies to any plug-ins invoked during the process"* (Q-21, MS) — asynchrony does not lift the plug-in limit.

**Operational implications.** The status resource *is* the operational surface: it carries state, attempt counts, errors and correlation. Q-17's `Notification` table is the concrete template — *"tracking the channel…, scheduled delivery time, status (Scheduled, Sent, Failed, or Canceled), number of attempts, and the associated Service Bus sequence number"*, whose purpose is *"real-time tracking, reporting, and error handling"* and which lets administrators *"audit the delivery history, monitor failed attempts, and take corrective action"* (MS). Q-20 states the same requirement as a reliability principle: *"Track job status in Dataverse for recoverability and support"* and *"Capture failure states explicitly (validation failures, pricing evaluation exceptions, integration faults) and surface them with actionable remediation guidance"* (MS). Retention of the status data must be planned (Q-03; DA-27's storage-hygiene warning).

**Security implications.** Mostly inherited, with two specifics. Q-23 names a security *motive* for the pattern: *"Sensitive-data processing that transfers the task to a more secure location for processing. For example, you might not want to process sensitive data within a web app. Instead, you might use a pattern such as the Gatekeeper pattern to transfer the data to an isolated background process that has access to protected storage"* (MS). And the status resource, if exposed over HTTP, needs its own access control — Q-03 points at a valet-key/SAS approach for the `Location` URL (MS).

**Scalability implications.** *"Background jobs can scale with increasing workloads without compromising performance or reliability"* (Q-21, MS) — with the caveat that the *dispatching* side still consumes the three meters and the executing side is bounded by whatever host runs it. Where the executing side is a flow, AP-01's ceilings apply; where it is a worker behind a queue, AP-04's back-pressure caveat applies.

**Governance implications.** Background work needs an owner, allowed runtime/data boundary and an explicit status/audit model. “Fire and forget” is not a governance model.

**ALM implications.** Status schema, worker/flow version and callback semantics must survive deployment. Long-running instances may span releases, so compatibility matters.

**Performance / scale boundary.** Removes synchronous timeout pressure but does not remove entitlement, connector, worker or backlog limits. Size arrival rate versus completion rate.

**Cost implications.** Adds status storage, polling/callback traffic, telemetry and potentially Azure compute; can be cheaper than holding synchronous capacity.

**Operations / recovery.** Expose status, age, failure and retry. Correlate request → background work → result. Define what happens to in-flight work during deployment/restore.

**Power Platform ownership boundary.** If the “background job” is actually compute-heavy, high-volume or durable orchestration, move that responsibility to an appropriate compute/orchestration service and keep Power Platform at the edge.

**Validation.** V2 duration/backlog/failure pilot; V3 harness for retry/idempotency and release compatibility where critical.

**When NOT to use.**
- The UI genuinely must wait for the result (Q-23's own test) → AP-01 or AP-02, inside the synchronous window.
- The work fits comfortably inside the window and has no restart requirement → the status resource and the extra components are unrepaid cost.
- A native asynchronous notification service is available and better: *"You can use a service built for asynchronous notifications instead, like Azure Event Grid"* (Q-03, MS) → AP-03.
- Results must stream in real time — *"Consider using Server-Sent Events (SSEs)"* (Q-03, MS).
- The client needs many results and latency matters — *"Consider using a message broker instead"* (Q-03, MS) → AP-04.
- Persistent connections (WebSockets/SignalR) or open callback ports are available (Q-03, MS) → push instead of poll.

**Alternatives.** AP-03 (event/callback instead of polling), AP-04 (broker instead of a status endpoint, or both), AP-05 (when the reason for asynchrony is capability rather than duration), and the platform-native option: Dataverse background operations with `OnBackgroundOperationComplete` (Q-21), which is the lowest-cost expression of this pattern inside Power Platform.

**Evidence.** Structural: Q-03 in full (context, 202/`Location`/`Retry-After`/status-endpoint contract, status-field table, ten considerations including idempotency keys, cancellation, retention and 303-vs-302, when/when-not), Q-23 in full (job types, triggers, return-results mechanisms, coordination patterns, resiliency, scaling, the explicit trade-off, Power Platform facilitation). Instantiation: Q-21 (Dataverse background operations, three retries, callback/event notification, the plug-in ceiling), Q-17 (status table, sequence-number cancellation, dead-letter), Q-20 (Service Bus + Function + status in Dataverse, idempotent handlers), Q-30 (the platform's own timeout and respond-then-continue behaviour).
**Sources:** Q-03, Q-17, Q-20, Q-21, Q-23, Q-30; IA-09, IA-19, IA-46, IA-47; peers DA-04, DA-27, PS-09.

---

### AP-10 — Enterprise boundary architecture

```
Power Platform  ──►  Governed enterprise integration boundary  ──►  Enterprise systems
```

**Classification:** PATTERN · **Origin:** INF over MS evidence · **Confidence:** MEDIUM (the pattern's *components* are MS-evidenced; the pattern as a named structure is this file's synthesis — see the honesty note)

**Honesty note.** This is the weakest-evidenced pattern in the file and it is included because the brief asks for it and because its absence is the corpus's most consequential gap. **No fetched Microsoft page presents "the enterprise integration boundary" as a Power Platform pattern.** What the evidence provides is: (a) the *components* of such a boundary, each documented (APIM gateway and self-hosted gateway, DLP, VNet support, environment strategy, connector governance); (b) Microsoft's own B2B and integration-platform positioning, which locates certain responsibilities outside Power Platform (Q-16, Q-34, Q-08); and (c) repeated instructions to involve infrastructure and security stakeholders (Q-01). The synthesis — that these constitute a single architectural boundary through which Power Platform reaches the enterprise, and that the boundary may be owned by a non-Microsoft platform — is INF and is flagged as such. It should be validated against a customer reference or an explicit Microsoft statement before pack encoding (APR-U-08).

**Problem solved.** Many Power Platform artefacts, built by many makers at many skill levels, need controlled access to enterprise systems — and the enterprise needs one place where the contract, the identity, the rate limit, the audit and the change control live. Without such a boundary the estate becomes the accretion described in AP-01's risks and named by Microsoft's own word, *"spaghetti architecture"* (Q-07, MS).

**Appropriate conditions.**
- Multiple Power Platform artefacts, multiple makers, and a governance requirement.
- An existing enterprise integration capability (ESB, iPaaS, API gateway, message backbone, MDM) with a published contract — **this is the dominant condition and it is vendor-agnostic**. Where it exists, it is the answer, and Power Platform's role shrinks to experience and human workflow.
- Requirements that Microsoft's own material locates outside Power Automate: B2B/EDI and trading-partner handling (Q-16 lists *"B2B capabilities"* and the *"Enterprise Integration Pack for B2B scenarios"* for Logic Apps; Q-34 names B2B as a Logic Apps example), bulk ETL (Q-08 lists Data Factory as the integration service for *"orchestrating data movement and transformation at scale"*), and message-level replay/retention (Q-16's monitoring and versioning rows).
- Network requirements the platform cannot satisfy directly — the documented in-network mechanism is APIM's self-hosted gateway: *"an API provider can deploy the API gateway to the same environments where they host their APIs, to optimize API traffic and ensure compliance with local regulations and guidelines. The self-hosted gateway enables organizations with hybrid IT infrastructure to manage APIs hosted on-premises and across clouds from a single API Management service in Azure… packaged as a Linux-based Docker container"* (Q-24, MS).

**Architectural structure.** Power Platform (apps, flows, agents) → custom connectors generated from the boundary's published definitions → the boundary (API gateway and/or message backbone and/or integration platform, wherever it runs) → enterprise systems. Governance controls sit on the Power Platform side of the boundary: DLP policies scoping which connectors may be used per environment; environment strategy separating lifecycle stages; connector governance; VNet support where egress must be private. Q-26's security diagram enumerates the layered control points explicitly: *"1. Tenant access and isolation 2. Environment access 3. Resource permissions 4. Connector access and data loss prevention (DLP) policies 5. Role-based data access 6. On-premises data gateway"* (MS).

**Strengths.**
- **One contract, one policy point, one audit trail** for enterprise access (Q-24's gateway responsibilities, MS).
- **Discovery with control** — the developer portal plus the export-to-Power-Platform path lets professional developers publish and citizen developers consume: *"Citizen developers using the Microsoft Power Platform often need to reach the business capabilities developed and deployed by professional developers in Azure. Azure API Management enables professional developers to publish their backend service as APIs, and easily export these APIs to the Power Platform… for discovery and consumption by citizen developers"* (Q-25, MS).
- **Federated ownership is supported without losing central oversight** — APIM workspaces give *"isolated administrative access and API runtime"* while *"allowing the API platform team to retain oversight. This includes central monitoring, enforcement of API policies and compliance, and publishing APIs for discovery through a unified developer portal"* (Q-24, MS).
- **Legacy modernisation without migration:** *"APIs are used to abstract and modernize legacy backends and make them accessible from new cloud services and modern applications. APIs allow innovation without the risk, cost, and delays of migration"* (Q-24, MS).
- **B2B onboarding stops being per-integration:** *"APIs exposed to partners and customers lower the barrier to integrate business processes and exchange data between business entities. APIs eliminate the overhead inherent in point-to-point integration"* (Q-24, MS).
- **It removes the leaver risk from the integration path.** Ownership moves from a maker's licence and personal account (IA-16, AT2-01) to a platform team with resource-level access control (Q-16's RBAC contrast, MS-V capability fact).
- **It is the only pattern that can be satisfied by a non-Microsoft platform**, which is what makes it the corpus's antidote to "Azure is automatically the answer".

**Weaknesses.**
- **Lead time and autonomy loss.** Every new capability now needs a boundary change owned by another team. Nothing in the fetched evidence quantifies this; it is the well-known cost of central governance (INF).
- **A second (or third) platform to fund and operate**, with tier decisions that lock in network and availability capabilities (Q-24's tier grouping, MS).
- **Double abstraction.** Power Platform artefacts see a custom connector over an API over a backend; three contracts must stay aligned, and the custom-connector layer has its own change cost (IA-49, Q-37).
- **Governance can become the bottleneck**, at which point makers route around it — the failure mode DLP is meant to prevent and which its own enforcement lag makes messy: PS-29's blocked connectors fail at design time and can suspend or quarantine running artefacts with up to 24 h enforcement lag.
- **Boundary controls are Managed-Environments-gated** for several capabilities (VNet, IP firewall, sharing limits, pipelines — DA-55, PS-33), which requires every active user to hold a premium licence. The boundary therefore has a licensing precondition.

**Risks.**
- **The boundary that exists on paper only.** If the published contract is stale or incomplete, makers will use the direct connector anyway and the boundary becomes a fiction with a maintenance cost. Mitigation is DLP enforcement plus discoverability (Q-24, Q-25) — governance and enablement together, not governance alone (INF).
- **Assuming Azure is the boundary.** Where the enterprise's integration platform is another vendor's, standing up APIM alongside it creates two boundaries and duplicates contract management. This is the anti-pattern the brief warns about (*"Do not assume Microsoft/Azure is automatically the answer"*), and nothing in the Microsoft evidence prompts the question.
- **SPoF at enterprise scale.** AP-02's and AP-08's SPoF and bottleneck risks (Q-04, MS) apply with the whole estate behind them; load testing and availability design are not optional here.
- **DLP as an unplanned outage source** (PS-29, MS).
- **Unmeasured.** No capacity or latency figure for any boundary component exists in this corpus (APR-U-02, carried).

**Operational implications.** Requires a named platform team, a published catalogue, an onboarding process for makers, and joint incident management across the boundary. Azure API Center is the documented inventory mechanism: *"to build a complete inventory of APIs in the organization - regardless of their type, lifecycle stage, or deployment location - for API discovery, reuse, and governance"* (Q-24, MS). Monitoring spans both sides and needs correlation (Q-04's telemetry guidance).

**Security implications.** The strongest of the ten patterns: one authentication point, backends network-isolated, quotas enforced, Key Vault for certificates and secrets, Defender for APIs and DDoS protection available, Entra ID for both developer authentication and backend authorization (Q-24, MS). Q-19's environment-level VNet association adds lifecycle isolation: *"This setup prevents lower-level environments, like dev environments, from accidentally connecting to test or production Azure resources, helping maintain a secure development life cycle"* (MS). Residual concern: a boundary that calls backends with its own identity removes per-user backend authorization unless it propagates identity (INF over IA-33).

**Scalability implications.** Moves the ceiling to the boundary's own capacity and tier. On the Power Platform side the three meters still apply per artefact, so the boundary does not lift AP-01's ceilings for individual flows — a point frequently misunderstood. Whether APIM-fronted custom connector calls are metered differently is **not established** (APR-U-03).

**Governance implications.** This pattern is only valid when the boundary has an explicit owner and enterprise governance. Azure/API/broker resources need inventory, RBAC/Policy, budget/cost attribution, security baseline and lifecycle controls; Power Platform DLP remains only the consumer-side control.

**ALM implications.** The boundary must have its own source-controlled/IaC supply chain. If Power Platform uses custom connectors, ALM-14 applies as well. Cross-platform contract versions and release sequencing are first-class.

**Performance / scale boundary.** Enterprise ownership does not make the boundary infinite. Published service quotas plus measured workload tests still govern; Power Platform-side connector/service limits remain.

**Cost implications.** Usually the highest fixed governance/operations burden but may be the lowest marginal cost when the enterprise capability already exists and is shared. If it does not already exist, include the programme/platform-team cost rather than pricing only an APIM namespace or broker.

**Operations / recovery.** Requires enterprise monitoring, correlation, incident routing, DR and support. A boundary with no operator is unavailable (Y-13).

**Power Platform ownership boundary.** This pattern explicitly says Power Platform should **not** own enterprise integration responsibility. It consumes a published enterprise contract.

**Validation.** Reuse the enterprise platform's established quality gates where they exist; otherwise V2/V3/V4 validation is mandatory before calling the new boundary “enterprise”.

**When NOT to use.**
- A single solution with one or two integrations and no governance requirement → AP-01/AP-02. Standing up a boundary for one solution is the clearest case of unnecessary complexity (Q-01's minimal-complexity instruction, MS).
- No platform team and no funding for one → the pattern is unavailable, not deferred. An ungoverned boundary is worse than no boundary because it adds a hop and an illusion.
- The enterprise integration platform already exists and is adequate → **use it**; do not build a parallel Microsoft boundary beside it.
- Speed of delivery is the dominant requirement and the estate is small → the governance cost is not repaid yet; revisit at scale.

**Alternatives.** AP-02 (a single mediated API without an enterprise programme — the pragmatic 80 % answer), the enterprise's existing platform (the most common correct answer where one exists), AP-04 with an enterprise message backbone (where the boundary is a bus rather than a gateway), and Power Platform's native governance-only boundary: DLP + environment strategy + connector governance with **no** intermediary, which controls *which* systems may be reached without mediating *how* — cheaper, weaker, and often sufficient (INF over PS-29, DA-63).

**Evidence.** Components: Q-24 (gateway, management plane, developer portal, self-hosted gateway, workspaces, tiers, policies, API Center, Defender, Key Vault, Entra ID), Q-25 (publish-and-consume path), Q-19 (environment-level private connectivity and lifecycle isolation), Q-26 (the six layered control points). Responsibility location: Q-16 (B2B, RBAC, monitoring, versioning — MS-V capability facts only), Q-34 (B2B as a Logic Apps example), Q-08 (Azure integration service set including Data Factory for bulk). Stakeholders: Q-01. Failure mode being prevented: Q-07 (*"spaghetti architecture"*).
**Sources:** Q-01, Q-04, Q-07, Q-08, Q-16, Q-19, Q-24, Q-25, Q-26, Q-34, Q-37; IA-16, IA-33, IA-49; peers PS-29, PS-33, DA-55, DA-63, AT2-01.
---

## 5. Pattern selection matrix

Verdicts: **STRONG** (no documented constraint violated — never "Microsoft endorses"), **CONDITIONAL** (fit depends on the stated condition), **POOR** (collides with a documented limit or an explicit Microsoft "not suitable when"), **n/a** (not addressable by this pattern), **UNKNOWN** (not established in this corpus — do not infer).

Read a row, take the leftmost STRONG. Where the only STRONG is AP-05, AP-07 or AP-10, the requirement carries an operating-model cost that belongs in the option.

| # | Requirement | AP-01 Direct | AP-02 API | AP-03 Event | AP-04 Queue | AP-05 Hybrid | AP-06 Virtual | AP-07 Replicate | AP-08 Facade | AP-09 Background | AP-10 Boundary | Origin |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | One consumer, one backend, stable contract, inside throttle | **STRONG** | CONDITIONAL (cost unjustified) | n/a | POOR (complexity, Q-02) | POOR | n/a | POOR | POOR | n/a | POOR | MS (Q-01, Q-02, Q-07) |
| 2 | ≥ 2 consumers need the same backend capability | POOR (duplication → X-01) | **STRONG** | CONDITIONAL | CONDITIONAL | CONDITIONAL | n/a | n/a | CONDITIONAL (if composing) | n/a | STRONG at estate scale | MS (Q-18, Q-24) |
| 3 | Backend contract changes often | POOR (republish + reconnect per change) | **STRONG** (versioning) | n/a | n/a | CONDITIONAL | POOR (schema modelled) | POOR | STRONG (facade absorbs) | n/a | STRONG | MS (Q-24, Q-37) |
| 4 | Backend contract is legacy/semantically hostile | POOR (leaks into every flow) | CONDITIONAL | n/a | n/a | CONDITIONAL | POOR | POOR | **STRONG** (anti-corruption, Q-05) | n/a | STRONG | MS (Q-05) |
| 5 | One client operation needs 3+ backends | POOR (chatty, Q-18) | CONDITIONAL | n/a | n/a | CONDITIONAL | CONDITIONAL (if table-shaped) | n/a | **STRONG** | n/a | STRONG | MS (Q-04, Q-18) |
| 6 | Same-backend chattiness across operations | CONDITIONAL | CONDITIONAL | n/a | n/a | n/a | n/a | n/a | POOR — *"adding a batch operation to the service might be more suitable"* (Q-04) | n/a | n/a | MS (Q-04) |
| 7 | Producer must not depend on consumer availability | POOR | POOR | **STRONG** | **STRONG** | CONDITIONAL | n/a | n/a | POOR | CONDITIONAL | STRONG | MS (Q-02, Q-10) |
| 8 | Spiky arrival that would throttle the target | POOR (429s → 14-day auto-off) | POOR (gateway is a bottleneck, not a buffer) | POOR (event does not absorb) | **STRONG** | CONDITIONAL | CONDITIONAL | CONDITIONAL | POOR | CONDITIONAL | STRONG | MS (Q-01, Q-02, Q-04) |
| 9 | Ordering required | POOR | POOR | POOR (no guarantee, Q-09) | CONDITIONAL (Service Bus sessions / partition key) | CONDITIONAL | n/a | POOR | POOR | POOR | CONDITIONAL | MS (Q-02, Q-09) |
| 10 | Duplicates must be suppressed | POOR | POOR | POOR | CONDITIONAL (Service Bus duplicate detection; or idempotency key) | CONDITIONAL | n/a | CONDITIONAL (alternate key upsert, Q-15) | POOR | CONDITIONAL (idempotency key, Q-03) | CONDITIONAL | MS (Q-02, Q-03, Q-09, Q-15) |
| 11 | Poison messages need a destination | POOR (no dead-letter — INF, treat as unsupported until verified) | CONDITIONAL | POOR | **STRONG** (dead-letter, Q-02) | CONDITIONAL | n/a | n/a | POOR | CONDITIONAL (status resource as substitute) | STRONG | MS (Q-02, Q-09) + INF (absence) |
| 12 | Replay of past messages required | POOR | POOR | CONDITIONAL (Event Hubs Capture only, Q-09) | CONDITIONAL | CONDITIONAL | n/a | n/a | POOR | POOR | STRONG | MS (Q-09) |
| 13 | Work exceeds 120 s / 180 s / 2 min plug-in | POOR | POOR | CONDITIONAL | STRONG (composed) | STRONG | n/a | n/a | POOR | **STRONG** | CONDITIONAL | MS (Q-30, Q-03, Q-23) |
| 14 | One step needs real computation | POOR (Q-07's own example) | CONDITIONAL | n/a | CONDITIONAL | **STRONG** | n/a | n/a | CONDITIONAL | CONDITIONAL | CONDITIONAL | MS (Q-07, Q-18) |
| 15 | Protocol not expressible by a connector (SOAP, EDI, RFC-only) | POOR | CONDITIONAL | n/a | CONDITIONAL | **STRONG** | n/a | n/a | CONDITIONAL | n/a | **STRONG** (B2B/EDI belongs here, Q-16/Q-34) | MS + MS-V |
| 16 | Read reference data owned elsewhere; table-level authz suffices | CONDITIONAL (per-call) | CONDITIONAL | n/a | n/a | n/a | **STRONG** | CONDITIONAL (copy unnecessary) | CONDITIONAL | n/a | CONDITIONAL | MS (Q-13, Q-14) |
| 17 | Row-level or field-level security required on external data | CONDITIONAL (delegated identity) | CONDITIONAL (delegated) | n/a | n/a | n/a | **POOR** (excluded, Q-13/Q-26) | **STRONG** | CONDITIONAL | n/a | CONDITIONAL | MS (Q-13, Q-15, Q-26) |
| 18 | Audit / search / offline / charts / BPF required on that data | n/a | n/a | n/a | n/a | n/a | **POOR** (all excluded, Q-13) | **STRONG** | n/a | n/a | n/a | MS (Q-13) |
| 19 | Freshness tighter than the source's refresh cadence | CONDITIONAL | CONDITIONAL | STRONG (event on change) | STRONG | CONDITIONAL | **POOR** (false freshness, Q-14) | CONDITIONAL (event path) | CONDITIONAL | n/a | CONDITIONAL | MS (Q-14) |
| 20 | Strict atomicity across two systems | POOR | POOR | POOR | POOR | POOR | POOR | POOR | POOR | POOR | CONDITIONAL (external coordinator) | MS (IA-19) |
| 21 | Bidirectional master data, 1:1 | POOR | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | POOR | **STRONG** (3-component design, Q-15) | n/a | n/a | STRONG | MS (Q-15, Q-28) |
| 22 | Bidirectional master data, 1:N | POOR | CONDITIONAL | STRONG (publish once) | **STRONG** | CONDITIONAL | POOR | **POOR** (explicitly out of scope, Q-15) | n/a | n/a | STRONG | MS (Q-15) |
| 23 | On-premises source, payload ≤ 2 MB | **STRONG** (gateway) | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | CONDITIONAL | n/a | STRONG | MS (Q-31, Q-27) |
| 24 | On-premises source, payload > 2 MB | **POOR** (gateway cap, Q-31) | CONDITIONAL | CONDITIONAL | CONDITIONAL | STRONG (in-network component) | POOR | CONDITIONAL | CONDITIONAL | CONDITIONAL | **STRONG** (self-hosted gateway, Q-24) | MS (Q-31, Q-24) |
| 25 | Mandatory private egress | CONDITIONAL (VNet-supported connectors only) | STRONG (Q-19's shape) | **POOR** for Azure-aware plug-ins (Q-29) | CONDITIONAL (Azure Queues connector is VNet-supported) | STRONG | CONDITIONAL | CONDITIONAL | STRONG | CONDITIONAL | STRONG | MS (Q-19, Q-29) |
| 26 | No stored secrets permitted | POOR (no managed identity on connectors, IA-31) | CONDITIONAL (secret still on the PP leg) | POOR | STRONG (worker uses managed identity, Q-17) | **STRONG** (plug-in or worker) | POOR | POOR | CONDITIONAL | CONDITIONAL | STRONG | MS (Q-17, IA-31) |
| 27 | Message-level audit or long retention | POOR | CONDITIONAL | POOR | **STRONG** (broker + status table) | CONDITIONAL | n/a | CONDITIONAL | CONDITIONAL | STRONG (status resource) | **STRONG** | MS (Q-17, Q-20) + MS-V (Q-16) |
| 28 | Bulk ETL / warehouse loading | POOR (PS-07, DA-51) | POOR | POOR | CONDITIONAL | CONDITIONAL | n/a | CONDITIONAL (bulk path) | POOR | CONDITIONAL | **STRONG** (Data Factory / platform, Q-08) | MS (Q-08) + peers |
| 29 | Enterprise already owns integration with a published contract | POOR (bypasses the owner) | POOR (duplicate boundary) | POOR | POOR | POOR | CONDITIONAL | POOR | POOR | n/a | **STRONG** | INF over Q-24, Q-25 |
| 30 | Governance across many makers and artefacts | POOR | CONDITIONAL | CONDITIONAL | CONDITIONAL | POOR | CONDITIONAL | CONDITIONAL | CONDITIONAL | n/a | **STRONG** | MS (Q-24, Q-26) |

- **Classification:** DECISION CRITERION · **Origin:** per-row as marked; the *matrix* is INF · **Confidence:** MEDIUM · **Sources:** as cited per row.

---


### 5.1 Cross-block selection rows added in V2

| Decision input | Moves toward simpler/on-platform patterns when… | Forces escalation / disqualifies when… | Evidence owner |
|---|---|---|---|
| **Budget constraint** | Existing entitlement and standard connectors satisfy the requirement; no second operated estate is needed | Security prerequisites, premium audience, broker/API/worker, telemetry/support or external platform team exceed the approved TCO | `licensing-cost.md` LC-30, LC-21, LC-23 |
| **Deployment maturity** | One solution lifecycle and standard connectors are sufficient | Custom connector + API/worker/broker requires two supply chains, contract versioning or IaC/CI-CD the team cannot operate | `alm-devops.md` ALM-14 + §14 V2 |
| **Operational maturity** | Departmental criticality and inherited dependency availability are acceptable | AP-04/AP-05/AP-10 require a named operator; mission-critical requires drills, incident ownership, monitoring and recovery | `operations-support.md` §1.1, OP-03, OP-05, OP-19 |
| **Licence profile of user population** | Existing licences cover required connectors/environment controls | Premium/managed-environment and E5-class/Entra prerequisites apply to a broad population and make the option uneconomic | `licensing-cost.md` LC-30; `security.md` SEC-27/SEC-29 |

## 6. Pattern composition, and how patterns move

### 6.1 Compositions that are documented, not merely possible

| Composition | What it is for | Evidence |
|---|---|---|
| **AP-04 + AP-09** | Durable dispatch plus a status resource — the standard shape for long-running work with a caller that needs to know | Q-17 (Service Bus + Functions + `Notification` table), Q-20 (Service Bus + Function + status in Dataverse), Q-23 (*"queues can act as a buffer… restarts don't block the UI"*) |
| **AP-03 + AP-04** | Events carry the notification; the queue carries the guarantee. Emit on change, absorb the burst | Q-01's escalation (direct → decoupled reads → queued writes); Q-09 (transport properties) |
| **AP-06 + AP-07** | Read reference data live; replicate only what needs platform data features. Two mechanisms for one dataset, deliberately | Q-20's three-pattern split (virtual entities read, dual-write write, OData API for the rest); Q-14 (virtual reference data alongside editable Dataverse records) |
| **AP-02 + AP-05** | The API layer is the contract; a service behind it holds the domain logic | Q-04 (*"place that functionality in a dedicated custom service behind the gateway"*), Q-18 (custom connector over a Function) |
| **AP-05 + AP-04** | The externalised capability is reached through a queue rather than synchronously — the shape when the capability is also slow | Q-20 (clone jobs), Q-17 (delivery function) |
| **AP-07 + AP-09** | Replication with a job-status ledger, so reconciliation has something to reconcile against | Q-15 (sync-status column driving a follow-up flow), Q-20 (*"Track job status in Dataverse for recoverability"*) |
| **AP-10 enclosing everything** | The boundary is not an alternative to the other patterns; the others operate *inside* it | Q-24, Q-25, Q-26 (layered control points) |

### 6.2 Escalation triggers — the requirement that moves each boundary

| From → To | Trigger (the requirement that forces the move) | Evidence |
|---|---|---|
| AP-01 → AP-02 | second consumer; contract volatility; composition; rate limiting; caching; telemetry; discovery | Q-18, Q-24, IA-49 |
| AP-01 → AP-03 | producer must not wait or must not know its consumers; enterprise system must be the initiator | Q-01, Q-07 |
| AP-01/AP-03 → AP-04 | delivery guarantee; spike absorption; scheduled delivery with cancellation; poison-message destination | Q-01, Q-02, Q-17 |
| AP-01 → AP-05 | computation, duration, protocol, guarantee, or identity exceeds the platform at **one step** | Q-07, Q-18, Q-20 |
| AP-01/AP-02 → AP-09 | work exceeds a synchronous window or must survive restarts | Q-03, Q-23, Q-30 |
| AP-02 → AP-08 | one client operation needs several backends, or the backend contract is semantically hostile | Q-04, Q-05, Q-18 |
| AP-06 → AP-07 | any item on AP-06's exclusion list becomes a requirement (row/field security, audit, search, offline, charts, BPF, local enrichment) | Q-13, Q-15, Q-26 |
| AP-07 → AP-03/AP-04 | fan-out beyond 1:1 | Q-15 |
| anything → AP-10 | many makers plus governance; or the enterprise already owns integration; or B2B/EDI; or bulk ETL; or message-level retention | Q-08, Q-16, Q-24, Q-25 |

### 6.3 De-escalation — the move nobody makes

When the requirement that forced a rung disappears, the structure should come back down. Two concrete cases from the evidence:
- **A retired anti-corruption layer.** *"If the anti-corruption layer is part of an application migration strategy, consider whether it's permanent or whether you plan to retire it after you migrate all legacy functionality"* (Q-05, MS).
- **A queue whose volume never materialised.** *"This pattern might not be suitable when… The workload volume is predictably low and stable, so adding queueing complexity provides little benefit"* (Q-02, MS) — a condition that can become true after the fact, when a projected peak did not arrive.

The corpus should treat "the structure is more complex than the current requirement justifies" as a legitimate finding, not as a stable state. Microsoft's minimal-complexity instruction (Q-01) is not only an initial-design rule.

- **Classification:** DECISION CRITERION + RECOMMENDATION · **Origin:** MS for each trigger's evidence; INF for the composition table's organisation · **Confidence:** MEDIUM

---

## 7. Pattern-selection anti-patterns

These are anti-patterns of *choosing* a pattern. Implementation anti-patterns live in `integration-architecture.md` §6 (X-01…X-18) and are not repeated.

| Id | Anti-pattern | Why it is one | Corrective |
|---|---|---|---|
| **Y-01** | **Pattern by resemblance** — selecting the structure that matches a reference architecture rather than the requirements | The brief's FINAL TEST is explicit. Every Microsoft reference architecture carries its own caveat: *"This article provides an example scenario and a generalized example architecture… The architecture example can be modified for many different scenarios and industries"* (Q-17, Q-19, Q-20, Q-26, MS) — they are examples, not prescriptions | Run §3.1's variables; take the leftmost STRONG in §5; record which requirement forced each rung |
| **Y-02** | **Starting above AP-01** — beginning the design at the API layer or the broker because that is what enterprise architecture looks like | *"start with Power Automate as the default option"*; *"Use these options only when Power Automate doesn't meet your business or technical needs"*; *"Choose the simplest approach that fulfills requirements and avoids unnecessary investment"* (Q-07, Q-01, MS) | Start at AP-01 and climb with a named justification |
| **Y-03** | **Buffer as a substitute for capacity** — adding a queue while leaving the consumer unbounded | *"Autoscaling without bounding consumers' aggregate downstream rate only moves the overload to downstream dependencies"* (Q-02, MS) | Bound consumer concurrency to the documented downstream limit; the queue levels arrival, it does not create target capacity |
| **Y-04** | **Gateway as a shock absorber** — expecting an API layer to solve a spike | A gateway under load is a bottleneck and a SPoF, not a buffer (Q-04, MS) | AP-04 for spikes; AP-02 for contract, policy and reuse |
| **Y-05** | **Virtualization chosen for elegance** — AP-06 selected without checking the exclusion list | Two independent rejection cases are documented, both discovered against security requirements (Q-15, MS) | Check the AP-06 exclusion list against the requirement **before** choosing; the check is a security-review item, not a preference |
| **Y-06** | **Replication chosen by default** — copying because copying is familiar | *"Too much data synchronized with Dynamics 365 for reporting purposes that overloads the database"* (DA-51, MS); *"Financial posting entities… are deliberately excluded from dual-write, avoiding any shadow-ERP behavior"* (Q-20, MS) | Require a named item from AP-06's exclusion list as the justification for AP-07 |
| **Y-07** | **Sync without reconciliation** — the fast path only | The reference design's nightly pass exists precisely because the fast path loses updates (Q-15, MS) | Three components or none: event path, bulk path, reconciliation |
| **Y-08** | **Async without a status resource** — fire and forget where someone will ask "did it work?" | *"you must implement a mechanism"* (Q-23, MS); the client *"can't distinguish between a lost response and a request that was never received"* (Q-03, MS) | Define the status entity before building the worker |
| **Y-09** | **Partial failure left undefined** in a composed call | *"Make this decision explicit in the policy design so that clients experience predictable behavior"* (Q-04, MS) | Decide per operation: partial response or whole-request failure; write it into the policy |
| **Y-10** | **Approximating resilience patterns in the wrong layer** — retry loops in place of a circuit breaker, variables in place of a dead-letter queue | The Circuit Breaker pattern serves a *different purpose* from retry: *"The Retry pattern enables an application to retry an operation with the expectation that it eventually succeeds. The Circuit Breaker pattern prevents an application from performing an operation that's likely to fail"* (Q-06, MS). Q-06 also notes it is often unnecessary in message-driven designs: *"You have a message-driven or event-driven architecture, because they often route failed messages to a dead letter queue… Built-in failure isolation and retry mechanisms are often sufficient"* | Where fail-fast is genuinely required, put it at the API layer (Q-04's *"circuit breakers"* in APIM policies) or in the worker; where the architecture is message-driven, use the broker's dead-letter and stop trying to build a breaker |
| **Y-11** | **Cascading retry across the pattern stack** — retry configured at app, flow, connector, gateway and backend | *"If you implement retry with a count of three on both calls, there are nine retry attempts in total against the service"*; *"Never implement an endless retry mechanism"* (Q-22, MS) | One retry site per hop chain, chosen deliberately; disable the others |
| **Y-12** | **Assuming Azure is the boundary** — standing up APIM beside an existing enterprise integration platform | The brief's instruction; nothing in the Microsoft evidence prompts the question, which is exactly why it must be asked (INF) | Ask §3.1's last variable first: does an enterprise integration capability already exist, with a published contract? |
| **Y-13** | **Adopting a pattern with no operator** — AP-04, AP-05 or AP-10 without a named team for the non-Power-Platform half | AT2-53's hybrid operating-model cost; Q-20's instruction to *"Document ownership and support processes for apps, plugins, flows, Azure resources, and ERP integrations"* (MS) | Treat "no operator" as making the pattern **unavailable**, not merely expensive |
| **Y-14** | **One pattern per system pair** — deciding "how we integrate with SAP" instead of per stream | Q-01's worked example decomposes one goal into four streams and gives them **different** treatments (MS) | Decide per stream; per-stream heterogeneity is expected |

- **Classification:** ANTI-PATTERN · **Origin:** MS for each evidence cell except Y-12 (INF) and Y-13 (MS instruction + INF conclusion) · **Confidence:** HIGH except Y-12, Y-13 (MEDIUM)

---

## 8. Negative evidence

Per the brief and the source policy, collected deliberately. Pattern-level negative evidence only; mechanism-level limits are in `integration-architecture.md` §7.

**Microsoft's own "not suitable when" statements** — the most valuable negative evidence in this file, because it is the vendor bounding its own patterns:
1. Queue-based: *"The caller requires a low-latency, synchronous response"*; *"The workload volume is predictably low and stable, so adding queueing complexity provides little benefit"* (Q-02).
2. Asynchronous request-reply: unsuitable when a native notification service is available, when results must stream in real time, when *"the client needs to collect many results, and the latency of those results is important"*, when persistent connections are available, or when callbacks/webhooks are reachable (Q-03).
3. Gateway aggregation: unsuitable when reducing calls to a **single** service — *"adding a batch operation to the service might be more suitable"* — and when *"the client or application is located near the back-end services and latency isn't a significant factor"* (Q-04).
4. Anti-corruption layer: unsuitable when *"The new and legacy systems have no significant semantic differences"* (Q-05).
5. Circuit breaker: unsuitable for local resources, as a substitute for exception handling, when retry alone suffices, when breaker-reset delay is unacceptable, in message-driven architectures with dead-lettering, and when *"Failure recovery is managed at the infrastructure or platform level"* (Q-06).
6. Background jobs: *"Tasks that require the user or the UI to wait while they run are typically not appropriate background jobs"* (Q-23).
7. Direct/low-code default: bounded by *"Use these options only when Power Automate doesn't meet your business or technical needs"* — read in reverse, this bounds the *escalated* patterns, not AP-01 (Q-07).

**Documented costs stated by Microsoft in the same breath as the benefit:**
8. *"Background jobs introduce more components and dependencies to the system, which can increase the complexity and maintenance costs of the solution"* (Q-23).
9. *"The anti-corruption layer adds latency to calls between the two systems"* and *"adds an extra service that you must manage and maintain"* (Q-05).
10. *"This architecture offers flexibility, but also means that more code-first developer work is needed to develop and maintain the RESTful service and data layer"* (Q-18).
11. *"Custom code, Azure Functions, Data Factory, or Service Bus might give you more control or better performance, but they add complexity and cost"*; *"Custom solutions might seem powerful but often require a bigger budget for development, licensing, and support"* (Q-07).
12. *"The gateway service might introduce a single point of failure"*; *"The gateway might introduce a bottleneck"* (Q-04).

**Pattern-invalidating limitation lists:**
13. AP-06's thirteen documented exclusions, including the irreversibility of the virtual/standard decision and the ignored `$select` (Q-13).
14. AP-06 rejected twice in a documented design, both times on row-level security (Q-15).
15. AP-07 explicitly scoped to 1:1 — *"Scenarios where one master environment must synchronize with multiple other environments require a more scalable or distributed solution"* (Q-15).
16. AP-07's dataflow gaps: cannot change statuses, cannot delete absent rows, cannot be owned by a service principal, connection re-established manually per deployment (Q-15).
17. AP-03's private-network collision: *"Azure-aware plugins don't support VNet"* (Q-29).
18. AP-03's misuse statement for business events as a data pipe (Q-12).
19. AP-01/AP-05 protocol constraint: the SAP ERP connector uses RFC/BAPI and therefore *"only works with the SAP OData connector"* for the VNet data gateway path (Q-26); the gateway requires *"a Windows virtual machine (VM) with at least 8 GB of RAM"* and a cluster for production (Q-27).
20. AP-01 on-premises payload ceiling: 2 MB write, 2 MB request / 8 MB compressed response, 2,048-character GET URL, 1,000 data sources per cluster (Q-31).
21. RPA as an integration pattern is positioned as exceptional — *"Use desktop flows on the rare occasions when the connectors don't meet your requirements or for a one-time screen scraping need"* (Q-26) — and even the RPA reference architecture reaches for an API first and *"sends a notification if the API isn't available"* (Q-32).

**Microsoft naming the failure state of an unmanaged pattern estate:**
22. *"This pattern results in a service-oriented architecture—sometimes humorously called 'spaghetti architecture'"* (Q-07). Microsoft describes this as an outcome of the service-oriented integration pattern rather than condemning it, but the paired instructions — *"Avoid monolithic flows"* and *"Avoid over-consolidation"* — show it is a state to be managed, not a target.

**Vendor-side positioning, fenced (MS-V — capability facts only, adjectives not evidence):**
23. Q-16's capability table: Power Automate has *"Basic monitoring through the Power Automate portal - Custom injection into Application Insights"*, *"Limited versioning"*, *"Limited regional deployment options"*, user-level rather than resource-level RBAC, and *"Error handling | Flow Checker - Lists of errors within the flow"*. Against Logic Apps Standard's managed identity, VNet integration, private endpoints, resource-level RBAC, Git integration, ARM/Bicep and deployment slots. The **scale adjectives on the same page are excluded** per §9 APR-C-01.

**Independent (T3) — corroborative only, not authoritative:**
24. A concrete AP-01 failure at volume: fine with twenty files in test, 429s from the SharePoint connector with *"several hundred files triggered in a short window"*, *"retries piled up, and runs that should take seconds were taking minutes or failing entirely"* (Q-35, 2026-04-14). Note that this source's remedy — reducing concurrency to 1–5 — collides with Microsoft's own warning that concurrency control can drop triggers (IA-22).
25. Claimed operational gaps: fixed 30-day run-history retention, shared-resource performance variability, deployment downtime *"minutes to hours"* (Q-36, 2024-10-20). **Unverified in Tier 1** (APR-U-07).

**Absence claims (INF — treat as unsupported until verified):**
26. No dead-letter construct inside Power Automate, which is why AP-04 is the corrective for poison-message requirements (carried: `integration-architecture.md` IA-U-11).
27. No circuit-breaker construct inside Power Automate or connectors (carried: `integration-architecture.md` IA-U-12).
28. No saga or compensating-transaction construct anywhere in Power Platform; the pattern exists only on the Azure side (carried: IA-19, and Q-08's transactional-outbox reference).

---

## 9. Conflicts (CONFLICTED)

**APR-C-01 — Power Automate's scale positioning** (carried from `integration-architecture.md` IA-C-04 and `automation-architecture.md` APR-C-03). Q-07 (Power Platform Architecture Center, MS): *"start with Power Automate as the default option"*, *"Scales well for most business scenarios"*. Q-16 (Azure Logic Apps documentation, **MS-V**): *"Small to medium scale workflows"*, *"Suitable for lower-scale automation, limited by shared resources in Power Automate"*. **Resolution for this file: encode neither adjective.** The escalation triggers in §6.2 and the documented limits carried from the companion file are the encodable content. Q-16's capability facts remain usable.

**APR-C-02 — Is AP-06 a read pattern or a full-CRUD pattern?** Q-13 states that the OData v4 provider *"supports create, read (retrieve, retrieve multiple), update and delete (CRUD) operations"* and that *"Full CRUD operation is now supported for custom virtual table data provider"* (MS). Yet every Power Platform instantiation fetched in this pass is read-oriented, and Q-14 recommends *"Restrict access to the virtual tables to read access only"* (MS), while Q-26 lists write-side limitations as cons (MS). **Reading:** the capability is CRUD; the *evidenced* pattern is read. Treat write-through virtualization as CONDITIONAL with no instantiation evidence in this corpus (APR-U-06), not as STRONG.

**APR-C-03 — Does an API layer change how Power Platform requests are metered?** Not a source conflict but an unresolved interaction: AP-02 and AP-08 add a hop, and whether an APIM-fronted custom connector call is metered differently from a direct connector call is **not established** (APR-U-03, carried from `integration-architecture.md` IA-U-22). This matters because it determines whether the API-mediated pattern relieves or merely relocates the request-meter pressure. Do not claim relief.

---

## 10. Unknowns (UNKNOWN)

| Id | Unknown | Why it matters | What would close it |
|---|---|---|---|
| **APR-U-01** | Whether Microsoft publishes any Power-Platform-specific pattern catalogue beyond the five integration patterns of Q-07 and the reference-architecture gallery | Determines how much of this file's pattern *naming* is synthesis. Currently AP-06…AP-10's names are this file's | A survey of the Architecture Center's key-concepts tree over time; a Microsoft pattern index for Power Platform |
| **APR-U-02** | No capacity, latency or throughput figure for **any** pattern component — gateway node, APIM tier, broker, or connector — anywhere in this corpus | Every scalability statement in §4 is limit-based. "This pattern scales" is not a measured claim | Measurement, or Microsoft capacity-planning pages per component |
| **APR-U-03** | Whether APIM-fronted custom connector calls are metered differently from direct connector calls (APR-C-03) | Decides whether AP-02/AP-08 relieve the request meter | The Power Platform request definition applied to custom connectors |
| **APR-U-04** | Whether the Power Platform request meter counts the *facade's* backend calls at all (they occur outside Power Platform) | Cost model of AP-08 | As APR-U-03 |
| **APR-U-05** | Whether a Dataverse plug-in (VNet-supported) can publish to Service Bus in a way that satisfies both private egress and transaction-scoped eventing | The proposed workaround for AP-03's private-network collision is currently inference | A Microsoft statement or a working reference architecture |
| **APR-U-06** | Whether write-through data virtualization (AP-06 with CRUD) is a supported production pattern, and its performance characteristics | APR-C-02's unresolved half; teams will attempt it because the capability exists | A Microsoft instantiation or an explicit position |
| **APR-U-07** | Cloud flow run-history retention and replay, from Tier 1 | Load-bearing for AP-01's and AP-09's observability verdicts and for §5 row 27 | A Microsoft retention statement |
| **APR-U-08** | Whether "enterprise integration boundary" is a recognised pattern with a Microsoft or industry-standard articulation applicable to Power Platform | AP-10 is the weakest-evidenced pattern in the file and the most consequential for governance | A Microsoft governance/architecture statement, a CoE-level reference, or a credible independent articulation |
| **APR-U-09** | Cost comparison between AP-02 variants — APIM versus a plain Function + custom connector | The plain variant is materially cheaper and is Q-18's actual instantiation; the choice is currently made on convention | Pricing analysis at representative volumes |
| **APR-U-10** | Whether Dataverse business events have a published throughput or quota envelope | AP-03's business-event variant is unsized (carried: `integration-architecture.md` IA-U-13) | A limits statement on the business-events or connector pages |
| **APR-U-11** | Dual-write failure semantics under sustained far-side failure | An AP-07 bidirectional decision cannot be made responsibly without it (carried: `integration-architecture.md` IA-U-14) | Dual-write error-handling documentation |

---

## 11. Evidence-quality notes and implications for the aisa knowledge model

### 11.1 Evidence-quality notes
1. **Two evidence classes, unequal strength.** The generic Azure pattern pages (Q-02…Q-06) are the strongest material in this file: each carries an explicit *"This pattern might not be suitable when"* section, which is exactly the content the brief asks for and which the Power Platform pages almost never provide. The Power Platform reference architectures (Q-14, Q-15, Q-17, Q-18, Q-19, Q-20, Q-26, Q-32) are the strongest *instantiation* material but document what was built, not what it costs. **Consequence:** the "Weaknesses" and "Risks" fields for AP-06, AP-07 and AP-10 lean more on INF than the others, and this is the file's main honesty limitation.
2. **Two reference architectures are unusually candid** and worth citing as models: Q-15 states *why virtual tables were rejected* (twice) and admits residual manual work; Q-20 states an explicit exclusion (*"avoiding any shadow-ERP behavior"*). Negative evidence written by the vendor about its own products is the highest-value evidence in this corpus and both should be re-read before pack authoring.
3. **Pattern naming is partly this file's.** AP-01…AP-05 and AP-09 map onto structures Microsoft names. AP-06 and AP-07 map onto Microsoft mechanisms (virtual tables, dataflows/dual-write) rather than named patterns. AP-08 borrows the BFF/facade vocabulary from general practice; Microsoft names Gateway Aggregation and Anti-Corruption Layer for its two halves. AP-10 is synthesis (APR-U-08). The pack must not present synthesised names as Microsoft terminology.
4. **No measurement anywhere** (APR-U-02). Carried from every peer file.
5. **Vendor-side positioning is present and fenced** (Q-16), consistent with `automation-architecture.md` and `integration-architecture.md`.
6. **Negative search was run and the yield pattern is worth recording:** the strongest negative evidence is Microsoft's own *"not suitable when"* sections and its reference architectures' stated exclusions — not third-party criticism. Independent commentary (Q-35, Q-36) yielded one useful concrete failure case and several unverified operational claims.
7. **Single author, single session** for research, organisation and self-review. Three highest-value independent checks named in §1.

### 11.2 Implications for the aisa knowledge model (pointers, not pack content)
Per `03-KNOWLEDGE-MODEL.md` the chain is Requirement → Signal → Evidence → Knowledge State → Decision Criterion → Candidate Options → Trade-offs → Risk → Validation. This file supplies the **Candidate Options** and **Trade-offs** links; `integration-architecture.md` supplies the Requirement → Constraint links. Neither authors the pack.

- **Candidate options.** The ten patterns are option *shapes*, and §5's matrix is the raw material for generating a shortlist from elicited variables. Note that AP-10's strongest form is often a **non-Power-Platform** option, which is what keeps the corpus rule (*"Power Platform must NOT be assumed to be the answer"*) operative at pattern level.
- **Trade-offs.** Each pattern's Strengths/Weaknesses pair is written to be quotable as a trade-off statement with a source. The escalation ladder (§3.2) is the compact form: each rung names what is bought and what is paid.
- **Risks.** Each pattern's Risks section is the source of Risky claims. Those grounded in a Microsoft *"might not be suitable when"* statement are the strongest; those tagged INF need validity dates and revalidation, per the kernel's epistemic half-lives.
- **Decision criteria.** §3.1's variable-to-boundary mapping is the pattern-selection half of `integration-architecture.md` §9's 28 variables. The two should be encoded together or neither.
- **Validation.** Per pattern, the evidence yields concrete validation instructions: for AP-01, volume-test at projected peak *frequency* (Q-35's failure case); for AP-04, load-test the leveling and monitor queue and dead-letter depth (Q-02); for AP-02/AP-08, load-test the gateway to avoid cascading failure and decide partial-failure behaviour explicitly (Q-04); for AP-06, check the exclusion list against the security requirement before committing (Q-15's two rejections); for AP-07, prove the reconciliation pass actually converges (Q-15).
- **Anti-patterns.** §7's Y-01…Y-14 are pattern-selection anti-patterns and are distinct from `integration-architecture.md`'s implementation anti-patterns X-01…X-18. Both sets belong in the pack; conflating them would lose the distinction between *choosing wrong* and *building wrong*.

Nothing in this section is pack content. Question banks, decision trees and pack files are out of scope for this pass by instruction.

---

## 12. Source register

All fetches performed 2026-09-03. `ms.date` is the page's stated date; the bracketed date is the last-updated stamp where it differs. Several sources are shared with `integration-architecture.md`; the mapping to its `I-nn` ids is given so the two registers can be reconciled.

| Id | Title | URL | Type | `ms.date` (updated) | = companion id | Used for |
|---|---|---|---|---|---|---|
| Q-01 | Determine integration requirements | learn.microsoft.com/power-platform/architecture/key-concepts/integration-patterns/requirements | Tier 1 — PP Architecture Center | 2025-12-11 (2026-04-17) | I-01 | §2, §3, AP-01, AP-03, AP-04, AP-10; Y-02, Y-14 |
| Q-02 | Queue-Based Load Leveling pattern | learn.microsoft.com/azure/architecture/patterns/queue-based-load-leveling | Tier 1 — Azure Architecture Center | 2026-06-09 (2026-08-15) | I-44 | AP-04 (primary), §8; Y-03 |
| Q-03 | Asynchronous Request-Reply pattern | learn.microsoft.com/azure/architecture/patterns/asynchronous-request-reply | Tier 1 — Azure Architecture Center | 2026-03-30 (2026-07-14) | I-45 | AP-09 (primary), §8; Y-08 |
| Q-04 | Gateway Aggregation pattern | learn.microsoft.com/azure/architecture/patterns/gateway-aggregation | Tier 1 — Azure Architecture Center | 2026-06-02 (2026-06-03) | I-46 | AP-08 (primary), AP-02, AP-10; Y-04, Y-09 |
| Q-05 | Anti-Corruption Layer pattern | learn.microsoft.com/azure/architecture/patterns/anti-corruption-layer | Tier 1 — Azure Architecture Center | 2026-05-28 (2026-05-30) | I-47 | AP-08 (anti-corruption variant), §6.3, §8 |
| Q-06 | Circuit Breaker pattern | learn.microsoft.com/azure/architecture/patterns/circuit-breaker | Tier 1 — Azure Architecture Center | 2025-02-05 (2026-07-02) | I-43 | Y-10, §8 |
| Q-07 | Explore integration patterns | learn.microsoft.com/power-platform/architecture/key-concepts/integration-patterns/patterns | Tier 1 — PP Architecture Center | 2025-12-11 (2026-04-17) | I-02 | AP-01, AP-03, AP-05, AP-07, AP-10; Y-02; §8 |
| Q-08 | Get Started with Integration Architecture Design | learn.microsoft.com/azure/architecture/integration/integration-get-started | Tier 1 — Azure Architecture Center | 2026-06-18 (2026-08-25) | I-04 | AP-10, §5 row 28, §8 item 28 |
| Q-09 | Compare Messaging Services | learn.microsoft.com/azure/service-bus-messaging/compare-messaging-services | Tier 1 | 2026-06-12 | I-12 | AP-03, AP-04, §5 rows 9–12 |
| Q-10 | Azure Service Bus Integration for Dataverse | learn.microsoft.com/power-apps/developer/data-platform/azure-integration | Tier 1 | 2026-03-31 (2026-04-01) | I-05 | AP-03 (contracts, 192 KB, abandonment) |
| Q-11 | Use Webhooks to Create External Handlers for Server Events | learn.microsoft.com/power-apps/developer/data-platform/use-webhooks | Tier 1 | 2026-03-31 (2026-04-01) | I-06 | AP-03 (webhook vs Service Bus, rollback hazard) |
| Q-12 | Microsoft Dataverse business events | learn.microsoft.com/power-apps/developer/data-platform/business-events | Tier 1 | 2026-02-11 (2026-02-12) | I-24 | AP-03 (business events, design principles, misuse statement) |
| Q-13 | Get started with virtual tables | learn.microsoft.com/power-apps/developer/data-platform/virtual-entities/get-started-ve | Tier 1 | 2026-01-07 (2026-02-12) | I-16 | AP-06 (definition, providers, full limitation list); APR-C-02 |
| Q-14 | Connect Power Apps to a centralized data warehouse with Dataverse virtual tables | learn.microsoft.com/power-platform/architecture/reference-architectures/power-apps-virtual-tables | Tier 1 — reference architecture | 2026-08-18 | I-32 | AP-06 (instantiation, false-freshness caveat) |
| Q-15 | Synchronize data across Dataverse environments | learn.microsoft.com/power-platform/architecture/reference-architectures/sync-dataverse-data | Tier 1 — reference architecture | 2026-04-30 | I-28 | AP-07 (primary), AP-06 rejections; Y-05, Y-07 |
| Q-16 | Power Automate migration (to Azure Logic Apps Standard) | learn.microsoft.com/azure/logic-apps/power-automate-migration | Tier 1, **vendor-side (MS-V)** | 2025-07-18 (2026-02-13) | I-38 | AP-10, §5 row 15/27, §8 item 23; APR-C-01 |
| Q-17 | Implement a scalable notification system with Power Platform | learn.microsoft.com/power-platform/architecture/reference-architectures/scalable-notification-system | Tier 1 — reference architecture | 2025-12-09 (2026-06-11) | I-29 | AP-04, AP-09 (status table, dead-letter, managed identity) |
| Q-18 | Use REST APIs to extend the functionality of canvas apps | learn.microsoft.com/power-platform/architecture/reference-architectures/custom-connector-canvas | Tier 1 — reference architecture | 2025-04-17 (2025-08-27) | I-31 | AP-02, AP-05, AP-08 (instantiation and stated costs) |
| Q-19 | Secure Power Platform access to resources inside your virtual network | learn.microsoft.com/power-platform/architecture/reference-architectures/secure-access-azure-resources | Tier 1 — reference architecture | 2025-07-15 (2025-08-27) | I-27 | AP-02 (private variant), AP-10 |
| Q-20 | Integrate Dynamics 365 finance and operations apps with Power Platform | learn.microsoft.com/power-platform/architecture/reference-architectures/finance-and-operations-dataverse | Tier 1 — reference architecture | 2026-08-11 | I-26 | AP-05, AP-07, AP-09, §6.1; Y-06, Y-13 |
| Q-21 | Use Dataverse background operations | learn.microsoft.com/power-platform/architecture/reference-architectures/dataverse-background-operations | Tier 1 — reference architecture | 2025-04-17 (2025-08-27) | I-17 | AP-05, AP-09 (three retries, callback/event, plug-in ceiling) |
| Q-22 | Handle transient faults (PP Well-Architected RE:05) | learn.microsoft.com/power-platform/well-architected/reliability/handle-transient-faults | Tier 1 | 2025-08-18 (2025-08-20) | I-14 | Y-11 (cascading retry prohibitions) |
| Q-23 | Develop background jobs (PP Well-Architected RE:05) | learn.microsoft.com/power-platform/well-architected/reliability/background-jobs | Tier 1 | 2025-08-15 (2025-08-20) | I-21 | AP-09 (primary), AP-03 loop warning, §8 |
| Q-24 | Azure API Management — Overview and Key Concepts | learn.microsoft.com/azure/api-management/api-management-key-concepts | Tier 1 | 2025-10-13 (2026-06-25) | I-20 | AP-02 (primary), AP-08, AP-10 |
| Q-25 | Export APIs from Azure API Management to Microsoft Power Platform | learn.microsoft.com/azure/api-management/export-api-power-platform | Tier 1 | 2025-10-07 (2026-06-25) | I-23 | AP-02, AP-10 |
| Q-26 | Integrate Power Platform with SAP | learn.microsoft.com/power-platform/architecture/reference-architectures/arch-pattern-sap | Tier 1 — reference architecture | 2026-07-14 (2026-07-15) | I-25 | AP-06 (pro/con), AP-10 (control points), §8 items 19, 21 |
| Q-27 | Connect Microsoft Power Platform and SAP | learn.microsoft.com/power-platform/sap/connect/connect-power-platform-and-sap | Tier 1 | 2026-03-17 (2026-05-21) | I-18 | §5 row 23, §8 item 19 (gateway sizing, protocols) |
| Q-28 | Dual-write overview | learn.microsoft.com/dynamics365/fin-ops-core/dev-itpro/data-entities/dual-write/dual-write-overview | Tier 1 | 2026-01-15 (2026-09-01) | I-15 | AP-07 (bidirectional variant, schema impact); APR-U-11 |
| Q-29 | Microsoft Azure Virtual Network support | learn.microsoft.com/power-platform/admin/vnet-support-overview | Tier 1 | 2026-07-28 (2026-07-29) | I-10 | AP-03 (VNet collision), §5 row 25, §8 item 17 |
| Q-30 | Limits of automated, scheduled, and instant flows | learn.microsoft.com/power-automate/limits-and-config | Tier 1 | 2026-07-17 (2026-07-18) | I-13 | AP-01, AP-09 (timeouts, respond-then-continue, 30-day async) |
| Q-31 | What is an on-premises data gateway? | learn.microsoft.com/data-integration/gateway/service-gateway-onprem | Tier 1 | 2025-06-10 (2026-01-16) | I-09 | §5 rows 23–24, §8 item 20 |
| Q-32 | Integrate legacy data with Power Automate and SharePoint | learn.microsoft.com/power-platform/architecture/reference-architectures/app-legacy-data-integration | Tier 1 — reference architecture | 2025-07-09 (2025-08-27) | I-30 | §8 item 21 (RPA positioning) |
| Q-33 | Power Platform and Copilot Studio Architecture Center (overview) | learn.microsoft.com/power-platform/architecture/architecture-center-overview | Tier 1 | 2025-07-15 | I-40 | §11.1 note 3 (what the Architecture Center publishes); APR-U-01 |
| Q-34 | Integration and Automation Platform Options in Azure | learn.microsoft.com/azure/azure-functions/functions-compare-logic-apps-ms-flow-webjobs | Tier 1 | 2026-03-23 (2026-06-02) | I-11 | AP-05, AP-10, §5 row 15 |
| Q-35 | Halilcan Soran, *Power Automate Throttling Limits Will Break Your Flow in Production* | halilcansoran.com/power-automate-throttling-limits-fix/ | **T3** | published 2026-04-14 | I-41 | §8 item 24; AP-01 validation instruction |
| Q-36 | Dieter Gobeyn, *Overlooked Limitations of Power Automate vs Logic Apps* (AzureTechInsider) | azuretechinsider.com/overlooked-limitations-power-automate-vs-logic-apps/ | **T3** | published 2024-10-20 | I-42 | §8 item 25 (unverified operational claims); APR-U-07 |
| Q-37 | Custom connectors overview | learn.microsoft.com/connectors/custom-connectors/ | Tier 1 | 2026-06-03 (2026-08-27) | I-07 | AP-01 (contract-change procedure), AP-02, AP-10 |
| Q-38 | Microsoft Dataverse connector reference | learn.microsoft.com/connectors/commondataserviceforapps/ | Tier 1 — connector reference | 2024-03-01 (2026-07-11) | I-33 | AP-03 (trigger parameters, presence-not-change), AP-07 |

**End of file.** Next steps for this area, in order: resolve APR-C-02 and APR-U-06 (write-through virtualization); close APR-U-08 (whether AP-10 has a recognised articulation) before encoding it as a pattern; carry APR-C-01's handling rule into any pack material; then run the review and gate for Block A jointly with `integration-architecture.md`. No pack authoring until the gate passes.

---

## 13. Cross-Block V2 composed disqualifiers and validation

These are **combinations** that can invalidate an option even where every individual dimension looks merely CONDITIONAL. They are negative evidence assembled from existing findings; no new product capability is asserted.

| Combination | Consequence | Classification |
|---|---|---|
| Strict cross-system atomicity + more than one transactional owner + no acceptable compensation window | No pattern here supplies the required atomicity; collapse to one owner or move the transaction responsibility elsewhere | DECISION CRITERION / POOR FIT |
| AP-04/AP-05/AP-10 + no named operator/on-call/release owner | Pattern is unavailable, not merely expensive | ANTI-PATTERN |
| Private-network / CMK / IP-firewall requirement + no budget/entitlement for managed environment and external licence prerequisites | Security requirement and commercial constraint are incompatible with the proposed Power Platform design | CONSTRAINT |
| Business-/mission-critical workload + no representative managed test environment + no recovery drill | Production commitment cannot be evidenced; do not encode “ready” from limits alone | RISK |
| High-frequency custom-connector workload + decision relies on 500 or 10,000/min without measurement/Microsoft confirmation | Sizing is decision-blocking because the official sources remain conflicted | VOLATILE VALUE / CONFLICTED |
| Per-user backend authorization required + facade/worker calls downstream only as a shared service identity | Pattern changes the authorization semantics and is unsuitable unless identity is propagated or compensating authorization is implemented | DECISION CRITERION |
| Hybrid architecture required + no pro-dev/enterprise platform capability available | Power Platform-only implementation is the wrong fit; either acquire the capability or select another architecture/platform | POOR FIT |
| Replication + no reconciliation owner + recovery/restore requirement | A routine restore can create unowned data divergence; pattern is unavailable for material data | ANTI-PATTERN |

### Validation contract

Every pattern validation instruction now uses the four-level model in `integration-architecture.md` §15.8: **V1 documentation/limits**, **V2 bounded pilot with monitoring**, **V3 pro-dev automated harness**, **V4 managed-test fidelity**. These levels are complementary. `alm-devops.md`'s absence of a supported first-party low-code functional-test framework does not contradict performance pilots or external test harnesses.

### V2 research basis for the external estate

Azure Well-Architected guidance for API Management and Functions requires workload ownership, security baselines, automated deployment, observability, testing and cost governance. Those responsibilities are the evidence basis for the new Governance/ALM/Operations/Cost fields above; they are not assumed to be supplied by Power Platform. See:

- `https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-api-management`
- `https://learn.microsoft.com/en-us/azure/well-architected/service-guides/azure-functions`
- `https://learn.microsoft.com/en-us/azure/architecture/guide/management-governance/management-governance-get-started`
- `https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability`

