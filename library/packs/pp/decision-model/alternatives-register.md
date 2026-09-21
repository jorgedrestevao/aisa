# Alternatives Register — option classes and candidate generation

<!--
provenance: RUNTIME (decision-model register) · consumed at stage S1 of decision-tree.md
authored: 2026-09-04 (Step 3B1) · design authority: Step 3A — Options Decision Model
Stage-local: loaded at S1 (and re-read at S9 for the candidate list a terminal sentence must name).
Never preloaded. `ALT-NNN` ids are internal execution anchors and are NEVER rendered to the engagement
— `options.md` names the class in plain language (decision-tree.md §14.3).
-->

## 0. The one rule that governs this file

> **A trigger generates a candidate. It never produces a verdict.**

A requirement putting a class on the table is **not** evidence that the class satisfies the requirement,
and in almost every row below no such evidence exists. Read this file as *what comes into scope*, then
evaluate it through stages S2–S8 like any other candidate. Rendering this register as a lookup table
produces confident wrong answers.

**Candidate generation and comparator evaluation are different steps** (`decision-tree.md` §13).

---

## 1. The eleven option classes

Ordered from *least* to *most* new technology — the order the pack's own ladders use, since
*configure-or-buy* sits before any application type. **The ordering is a reading aid, not a preference
ranking.** `ALT-005`, `ALT-006` and `ALT-008` are correct answers for the requirements named in their
trigger rows, and arriving there quickly is not a failure.

| Id | Class | Plain-language rendering used in output |
|---|---|---|
| `ALT-001` | Extend the existing system — no new platform | *"extend what we already run"* |
| `ALT-002` | **Process change — no new technology** | *"change the process; build nothing"* |
| `ALT-003` | Collaboration-platform native capability | *"use the collaboration tooling the organisation already has"* |
| `ALT-004` | **This pack's platform** — a class of **forms**, each one a named *surface × store* pair (§1.2) | the **form** is named directly, in products — Options is the one phase where that is allowed, and *"this platform"* alone is not a rendered option |
| `ALT-005` | Custom development | *"build it as a custom application"* |
| `ALT-006` | Cloud-native services (integration, compute, messaging, data) | *"assemble it from cloud services"* |
| `ALT-007` | An existing enterprise platform owns the capability | *"the incumbent system owns this"* |
| `ALT-008` | Another low-code platform | *"a different low-code platform"* |
| `ALT-009` | Hybrid architecture | *"split it: part here, part elsewhere"* |
| `ALT-010` | **Do nothing / defer** | *"do nothing, or defer"* |
| `ALT-011` | Buy — packaged product, SaaS service or marketplace application | *"buy a product"* |

### 1.1 Mandatory members

> **`ALT-002` (process change) and `ALT-010` (do nothing / defer) are conditional members of the candidate set,
> in every engagement, generated at S1 — never appended by the chairman at the end.**

They are **always serious** (`decision-tree.md` §7.1): they are evaluated against the material concerns
and priced on the same ten cost dimensions as everything else. **They are never eliminated by a finding
about `ALT-004`** — only by their own evidence. *Not-doing-it* and *doing-it-manually* are legitimate
economic options and frequently the honest answer.

**`ALT-004` is not the default candidate.** It enters the set exactly like every other class: because a
requirement triggers it. If the surviving set at S9 contains only forms of `ALT-004`, S1 failed and the
procedure is re-run (`decision-tree.md` §6, reachability floor).

### 1.2 `ALT-004` is a class of **forms**, and a form is *surface × store*

> **A platform candidate is not decided until its form is named. `ALT-004` alone is not an option —
> it is a class whose members are named combinations of an application surface and a record store.**

Generated at S1 alongside the classes, re-read at S9. **`options.md` names the form of every platform
candidate, in products** (`decision-tree.md` §14.1) — Options is the one phase where that is allowed,
and the phase exists to put the named choice on the table. An option rendered as *"this platform"*, or
as *"this platform over the store that already runs"*, has withheld the decision it was convened to
present: a sponsor cannot approve a surface they were never shown.

**One option per form.** Two forms differing in surface, or in store, are **two candidates** with two
verdicts, two effort profiles and two reversibility statements. Collapsing them into one option is the
same defect as collapsing two scopes into one outcome (`decision-tree.md` §3, scope pairing).

**The store is not a detail of the surface.** It decides which surfaces are reachable at all, and it is
where the audit, row-security and retention obligations either come free or become build items. Which is
why the pair is the unit, and neither half is a candidate on its own.

#### The valid forms

Surfaces and their boundaries are in `domain-knowledge/application/application-surfaces.md` §3/§4/§6/§7;
stores in `domain-knowledge/data/store-boundaries.md` and the per-store files. **This table generates
candidates; it issues no verdict** (§0) — the *decides* column names what the pair forces, not what it
proves.

| Form (name it in products) | Store the surface admits | What the pair decides |
|---|---|---|
| **Record-centric (model-driven) app + governed store** | The **governed store only** — there is no record-centric app without a data model in it | Row and column security, audit and retention are **inherited**, not built. The shell is platform-owned; a phone browser is unsupported |
| **Canvas app + governed store** | Governed store, over any connector | Inherits the store's security and audit while forfeiting the record-centric shell's automatic responsiveness, accessibility, addressability, multi-language and concurrent making |
| **Canvas app + external relational store** | An external relational store the platform reaches by connector | The store's lifecycle leaves the platform's. Row security needs a real per-user store principal; a server-side audit trigger moves every write behind stored procedures — **which decides who builds the transactional core** |
| **Canvas app + collaboration-platform lists** | List storage in the collaboration platform | No column-level security; delegation and row-scope ceilings apply. Where a requirement crosses those documented triggers, this is `ALT-003`'s exclusion, not a platform exclusion |
| **Custom pages on a record-centric shell + governed store** | Governed store (it lives inside the record-centric app) | Bespoke screens on a structured backbone, at the price of offline, device capability, retained page state and independent publishing. **A standalone canvas app cannot be converted into one** |
| **Code app + governed store or external relational store** | Either | **Every end user requires the premium entitlement.** Compiled assets are served from a publicly reachable endpoint with no address restriction; offline is undocumented |
| **Team-hosted app + team-scoped store** | The team-scoped store only | A combined **2 GB** ceiling that cannot be extended, and **no audit and no column security**. Growth past it is the one-way graduation of §7 |
| **External-audience site + governed store** | Governed store | The only form serving authenticated external or anonymous audiences; requires an external-identity service as a prerequisite |
| **Branded native wrapping over a canvas app** | Follows the wrapped canvas app | A distribution decision, not a store decision: no push, monthly redistribution |
| **Embedded surface (report visual · list-customised form · chat tab) + its host's store** | Follows the host | Each carries its own sharing and lifecycle model; the list-customised form has **no automated cross-environment copy** |

**Not forms of `ALT-004`.** A hybrid split at a step is `ALT-009`; the collaboration platform's own
native capability is `ALT-003`; extending the incumbent is `ALT-001`. A platform surface reading an
external store is a **form of this class**, not a hybrid — the distinction is whether the user-facing
surface stays on the platform.

#### Two rules that stop the forms table becoming an exclusion table

- **A form becoming unavailable is an in-platform redirect, never an exclusion outcome**
  (`decision-tree.md` §3). *"The store choice removes the record-centric surface"* routes to another
  form; it never removes the platform, and it never becomes a disqualifier of any scope.
- **The forfeits are symmetric and must be stated as forfeits.** Naming what a form gives up
  (§6 of the surfaces file) is the decision content. Naming only what it provides is advocacy.

---

## 2. Trigger → candidate map

Twenty-nine rows. **Left column: the dominant requirement. Right column: the classes that come into
scope.** Nothing in this table says a class *satisfies* the requirement.

`COMPARATOR EVIDENCE ABSENT` applies to **every row except the customer-hosted / private-cloud /
air-gapped row**, which is the one axis where comparative capability is documented on both sides. Carry
that marker into the output; it is part of the outcome sentence, not a footnote.

| # | Dominant requirement | Candidate classes |
|---:|---|---|
| 1 | Capability already exists in the estate | `ALT-001`, `ALT-003`, `ALT-007`, `ALT-011` |
| 2 | Value below full cost of ownership | `ALT-002`, `ALT-010` |
| 3 | Process immature or self-inflicted complexity | `ALT-002` |
| 4 | The document *is* the record | `ALT-003` |
| 5 | Relational data + row/column security + audit, internal audience | `ALT-004` |
| 6 | Human decision inside the platform's documented in-platform wait window | `ALT-004` — keep this leg in-platform even if other legs move |
| 7 | Bounded connector work over the existing estate | `ALT-004` |
| 8 | Real computation inside a step | `ALT-006`, `ALT-009`, `ALT-005` |
| 9 | Guaranteed delivery / ordering / dead-lettering | `ALT-006`, `ALT-009` |
| 10 | Process outliving the documented single-run duration, or resumable | `ALT-006`, `ALT-009` |
| 11 | Sustained throughput past the documented meter envelope, with no partitioning available | `ALT-006`, `ALT-009` |
| 12 | Bulk movement / transformation / analytics | `ALT-006`, `ALT-007`, `ALT-009` |
| 13 | High-ingest timestamped events | `ALT-006` |
| 14 | B2B / trading-partner protocols | `ALT-006`, `ALT-007` |
| 15 | Integration already owned, with a published contract | `ALT-007` |
| 16 | Process class already owned by an existing engine | `ALT-007` |
| 17 | Atomicity across two or more systems with no acceptable compensation window | `ALT-005`, `ALT-006`, `ALT-007` — collapse to **one** transactional owner |
| 18 | Product-grade experience; native distribution with push | `ALT-005` |
| 19 | A public third-party API is the deliverable | `ALT-005` |
| 20 | Contractual availability or recovery-time commitment | `ALT-005`, `ALT-006`, `ALT-007` |
| 21 | **Customer-hosted / private-cloud / air-gapped deployment** | `ALT-005`, `ALT-008` — **the one row where comparator capability is documented on both sides**, with the second comparator's capability in early access, not general availability |
| 22 | Portability of the application layer off the vendor | `ALT-005` (`ALT-008` is a candidate, portability `UNKNOWN`) |
| 23 | Behaviour must be frozen / per-release change control | `ALT-005` |
| 24 | Confidential even from platform administrators | `ALT-005`, `ALT-001`, `ALT-007` |
| 25 | Private-network execution the platform cannot enter | `ALT-006`, `ALT-009`, `ALT-007` |
| 26 | Standardised, non-differentiating domain | `ALT-011`, `ALT-007` |
| 27 | A decision-blocking unknown that cannot be resolved in the window | `ALT-010` |
| 28 | A required control's population is unfunded | `ALT-010`, or a scope change |
| 29 | **Conversational or agent-shaped interaction** | **none evaluable.** Fit is `UNKNOWN` in **every** class, `ALT-004` included. The correct output is **decision blocked**, not a candidate set |

**Row 29 is not an omission.** The pack holds no fit assessment of an agent surface in any class. It can
elicit the requirement and record the governance, security, lifecycle and operational obligations it
carries; it cannot assess fit. Emitting a candidate set here would be invention.

---

## 3. Symmetry rules

These are what stop a knowledge-rich pack from becoming an advocacy document. **A reviewer should test
them.**

### 3.1 Equal evidential burden

An alternative is not required to prove itself against claims `ALT-004` is allowed to assert unproven.
Where a fact is known about `ALT-004` and the equivalent fact about an alternative is not, **the
asymmetry is stated as an asymmetry**, not resolved in either direction.

Operationally: `decision-tree.md` §4's evidence-grade rule applies identically to every class. An
`Assumed` claim that `ALT-005` cannot meet a requirement is held to exactly the same standard as one
about `ALT-004`.

### 3.2 The capability gates cut both ways — and the output must say so

The S7 obligation and capability gates (operator, support, skills, cross-boundary release owner,
operational maturity, accepted ownership) make `ALT-005`, `ALT-006` and `ALT-009` **unavailable** more
often than they do `ALT-004`: monitoring, alerting, incident response, backup, recovery, drills and
retirement must all be built **and staffed** there, and approval routing with delegation and escalation
has **no equivalent** in the code-first classes the pack's evidence examined.

`ALT-001`, `ALT-007` and `ALT-011` gain a **candidate** signal on the same criteria, because an operator
already exists and is funded.

> State both halves. This is a **documented capability gap in those classes**, never an advantage of
> `ALT-004`.

### 3.3 What is *not* a reason to leave `ALT-004`

Recorded first, so the trigger rows can be read as the exceptions they are.

- **Scale anxiety without a number.** The meters are published; compute them.
- **A preference for code.** The total-cost-of-ownership argument cuts the other way.
- **One difficult step.** The documented answer is a hybrid split **at the step** (`ALT-009`), not
  relocating the whole solution.
- **Resemblance to a reference architecture.** Every reference architecture carries its own
  *"this is an example"* caveat.
- **Versioning or monitoring gaps as the argument.** Contradicted by the platform's own lifecycle
  documentation; the real differentiators are compute, network and ownership.
- **The absence of a published benchmark.** No component of **any** platform here has an empirical
  benchmark. Absence of proof is symmetric and favours nobody.

---

## 4. Forbidden universal claims — prohibited output

These are **not findings**, and none may appear as a conclusion anywhere in `options.md`, in a
deliverable, or in an SU row.

| Forbidden claim | Why |
|---|---|
| *"Custom development is more expensive"* | Depends on requirements, team, lifecycle and full TCO. No comparative pricing exists; the pack carries a **method**, not a verdict |
| *"Low-code is faster"* | A marketing claim by the source test. Low-code lowers the cost of the *first* version and **shifts the cost of ownership toward change** — a trade, not a win |
| *"The platform scales" / "does not scale"* | Both adjectives are excluded. Encode the documented limits and the escalation conditions instead |
| *"Cloud services are the answer for anything hard"* | Named as an anti-pattern of reasoning twice: assuming a cloud boundary when an incumbent already owns it, and justifying it with claims the platform's own documentation contradicts |
| *"Building it yourself gives you control"* | Countered by the pack's own cost instruction: higher costs must be justified with clear business value |

Add the S9 discipline: **no outcome may contain *preferred*, *better*, *cheaper*, *faster*, *easier*,
*more scalable* or *lower TCO* about a class the pack has not evaluated.** The permitted form is
*excluded → candidates → evidence obligation*.

---

## 5. Symmetrically unknown — carry these, or over-conclude

A reader who forgets this table will over-conclude in whichever direction they were already leaning.

| Unknown | Applies to |
|---|---|
| No empirical throughput, latency or concurrency **benchmark** for any technology | **All eleven classes.** Neither *"the platform will be fast enough"* nor *"custom will be fast enough"* is evidenced |
| No comparative TCO study against any named alternative | `ALT-005`, `ALT-006`, `ALT-008`, `ALT-011` |
| No evaluation of any incumbent enterprise platform | `ALT-001`, `ALT-007`, `ALT-011` |
| No documented failure-rate or incident evidence for any service | All classes |
| Capacity envelopes for two of the three broker services were never established | `ALT-006`, `ALT-009` |
| No capacity or latency figure for any boundary component | `ALT-007`, `ALT-009` |
| Comparator low-code platforms: **everything except the deployment-model axis** | `ALT-008` |
| Gateway-at-scale infrastructure cost | `ALT-006`, `ALT-009` |
| Conversational / agent fit | **All eleven classes**, `ALT-004` included (row 29) |
| Document generation and templating at volume | **All eleven classes** — absent from the pack's evidence entirely. Evaluate on engagement evidence, mark as having **no pack basis**, log as authoring feedback (`decision-tree.md` §7.3) |

---

## 6. The one comparative hypothesis, and its status

> The platform has important people- and scope-based cost mechanisms, while infrastructure alternatives
> often expose more compute- and transaction-based meters. The **users-to-work ratio** can therefore be a
> useful crossover criterion.

**This is a hypothesis to test per engagement, never a verdict.** *Many people doing a little each* tends
toward people-based mechanisms; *few people driving much machine work* tends toward consumption meters.
It must be tested on **all ten cost dimensions** at S8, with current pricing and the customer's own
agreement — build effort, connectivity, observability, support and the second estate sit alongside the
meters and routinely dominate them.
