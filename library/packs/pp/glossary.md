# Power Platform Pack — Glossary

<!--
provenance: RUNTIME (shared vocabulary)
phase-visibility: discovery+ (Part A) · options+ (Part B, quarantined) · options+ (Part C)
authored: 2026-09-03 (Step 2) · trimmed 2026-09-04 (runtime simplification, phase G)
         · Part C added 2026-09-04 (Step 3B1, Options vocabulary)
authoring provenance: docs/pp-pack-authoring/research/pp/authoring/runtime-simplification-phase-g-report.md
-->

Pack-local vocabulary for `pp` engagements. Universal aisa terms live in `library/kernel/glossary.md`.

A term is here only because it is (a) engagement language a participant will actually use, (b) a distinction that stops evidence being misread, or (c) a word that lets business and technical people mean the same thing. Ordinary process and finance vocabulary is not repeated, and nothing here carries implementation guidance.

**Part A is the vocabulary of the problem** — technology-neutral, applicable unchanged to a custom build, another low-code platform, a packaged product, a process change, or doing nothing. **Part B is a translation table**: when a participant says a product name, it converts back into a Part A concept and the requirement is recorded. Nothing in Part B may be used to select, favour or exclude anything. **Part C is the Options vocabulary** — four terms a sponsor, architect or reviewer meets once the phase produces option verdicts. It is gated to Options and later, and it is deliberately small: strong internal decision semantics do not require exposing framework vocabulary to anyone.

Three hard rules:

1. **Vendor and product terms are not Discovery vocabulary** (`.claude/rules/no-tech-mention-before-options.md`). An existing system may be named **only as current state**, never as a target.
2. **No Part A term carries a number.** Volumes, limits and durations are elicited from the customer and recorded on the engagement's own rows with `verificado_em` and `validade` (`library/kernel/states.md`).
3. **Roles, never people** (P-21). No term here is satisfied by a person's name. Authority, review, publication and ownership are recorded as a **role**, the operation that role may perform, and the plane that enforces it. A question whose only possible answer is a name, a signature, an approval or a document proving a third party's position is out of scope (`library/kernel/states.md` -> *Question economics*, the role rule).

---

# Part A — Discovery vocabulary

## A1. Work and failure

| Term | Meaning in Discovery |
|---|---|
| **Work shape** | Which of four shapes the requirement has: a bounded run; a long-running case; the coordination of exchanges between systems; or distributed processing of many items. The shape, not the volume, decides the mechanism class. |
| **Human wait** | The longest period an instance sits waiting for a person. A first-class design input, not an inefficiency to be assumed away. |
| **Failure semantics** | What the business requires to be true after work stops half-done: retry and continue, compensate, hold in an in-doubt state, or never partially complete. |
| **Compensation** | The business action that corrects a completed step when a later step fails, and the window in which it is acceptable. |
| **Stable business key** | An identifier carried by the work item that is the same every time the same item arrives. Its absence is a scope item, not a detail. |

## A2. Accountability

| Term | Meaning in Discovery |
|---|---|
| **Accountable role** | The **role** that owns the requirement and the data, and the role a failure reaches. Recorded as a role, the operations it must be able to perform, and the plane that enforces them — never as a person's name. What a design consumes is *which role may do what on which entity*; who currently fills the role is engagement trivia. |
| **Operational ownership** | The **roles** accountable for noticing failure, acting on it and holding the evidence, and the **mechanism** each one uses (alert, log, dashboard, recovery path). Recorded as roles and mechanisms; a name and an acceptance are not design inputs. |
| **Delivery model** | Who builds and who runs afterwards: central delivery, a mixed business/engineering team, governed local building, or ungoverned local building. |
| **Pro-code capacity** | Engineering capability that exists **in-house and is available** — not merely present on an org chart, and not a plan. |
| **Scope reach** | How far the initiative reaches: one team, one function, across functions, enterprise-wide, or a shared capability others depend on. |

## A3. Information

| Term | Meaning in Discovery |
|---|---|
| **Source of record** | The system that is *authoritative* for an entity or a field — where it is created and corrected. May differ per field and may change at a lifecycle boundary. |
| **Contested authority** | Two teams already report different figures for the same thing. A finding in its own right, recorded as **Conflicted**. |
| **Sensitivity class** | The organisation's own classification tier for this data, and the controls that tier mandates. |
| **Access granularity** | The finest level at which access must be controlled: whole dataset, individual record, individual field, or record-and-field. A separate question from *who* has access. |
| **Atomicity span** | The set of writes that must all succeed or all fail: one write, several in one store, across stores, or across systems. |
| **Consistency window** | How long two systems may legitimately disagree, and what the business does during that window. |
| **Freshness** | How current a displayed value must be, expressed in seconds or minutes, with the business consequence of staleness stated. |
| **Analytical workload** | Reporting that aggregates, trends or spans periods — distinct from filtered operational lists, and separately constrained when it must respect per-user record visibility. |

## A4. Users and surfaces

| Term | Meaning in Discovery |
|---|---|
| **Identity class** | Whose directory the users belong to: the organisation's, a partner's, a customer's, none (anonymous), or a non-directory frontline population. Selects surface, topology and cost simultaneously. |
| **Interaction bespokeness** | Whether the experience is form-and-list shaped, moderately bespoke, highly bespoke, or product-grade. |
| **Design obligation** | Whether a design system or brand conformance is mandated, and whether the mandate is contractual. |
| **Accessibility regime** | The applicable obligation: none stated, internal policy, legal, or legal with attestation required. Attestation changes the work. |
| **Offline requirement** | Whether work must continue without connectivity, and at what depth: read only, write, or extended disconnected operation — plus the conflict behaviour expected on reconnection. |
| **Native distribution** | Whether the thing must appear under the organisation's brand in an app store or enterprise catalogue, and whether notifications must arrive when it is closed. |

## A5. Exchange and constraint

| Term | Meaning in Discovery |
|---|---|
| **Exchange stream** | One flow of information with a named source, target, initiator, payload, trigger and business purpose. The unit of analysis — **one decision per stream, not per system pair**. |
| **Delivery guarantee** | What the business requires of each message: best effort, at-least-once, ordered, effectively-once, or replayable. |
| **Unattended interface automation** | Driving another system through the interface a human would use, because no programmatic interface exists. A last resort with its own operating cost. |
| **Deployment-model constraint** | Where the runtime is *required to execute*: a vendor-operated service is acceptable; a customer cloud subscription; a customer data centre; air-gapped. Decided before any architecture work. |
| **Service permissibility posture** | Whether the organisation operates a permissive baseline, a restrictive baseline with exceptions, or a strict allowlist for what a workload may connect to — plus the exception process, its owner and its lead time. |
| **Administrator exclusion** | A requirement that people with platform-administration rights must not be able to read the data. Rare, decisive, and usually written in a clause. |
| **Authorization enforcement point** | Whether the other system enforces per-user rules itself, or whether the new capability is expected to be the enforcement point. Changes the shape of every exchange. |
| **Proof requirement** | What evidence the sponsor or a contract requires before commitment: published-limit arithmetic; a bounded pilot; an engineered test harness; a production-like load proof. Chosen and funded in Discovery, not discovered later. |
| **Precondition** | Something that must already be true in the organisation before the work can proceed. A missing precondition is a deliverable with an owner and a cost, not a footnote. |

## A6. Operations, change and money

| Term | Meaning in Discovery |
|---|---|
| **Criticality class** | What unavailability actually costs: simple departmental, business-critical, enterprise, or mission-critical. It sets the operating model, the evidence obligations and the cost. |
| **Operational maturity class** | How the organisation *actually operates* comparable things today, on the same four-class scale. The gap between criticality and maturity is a sponsor decision, not a design one. |
| **Isolation domain** | A separated space for a stage or a boundary (development, test, production; a region; a business unit). Named neutrally because every delivery platform has some form of it. |
| **Reversibility requirement** | What the business expects when a release is bad: fix forward, redeploy the previous version, or full restore. **Rollback must not be assumed to exist.** |
| **Change-control regime** | Whether a validated or regulated process forbids uncontrolled change, up to requiring behaviour to be frozen between releases. |
| **Vendor-change tolerance** | How much vendor-driven change the organisation can absorb, and who tracks the change stream today. |
| **Cost driver** | The quantity that makes the cost move: how many people, how often each acts, how many distinct capabilities each needs, how much data, how much machine work. |
| **Entitlement exposure** | The risk that the capability set the requirement implies falls outside what the organisation already holds — for a subset of people or for the whole audience. |
| **Audience and frequency shape** | Whether this is a small population acting often, a large population acting rarely, or both large and frequent. Different shapes have different economics. |

## A7. Distinctions that must not be collapsed

Each row is a pair routinely conflated in engagements. Collapsing one produces a confident wrong answer.

| Keep apart | Why |
|---|---|
| **Residency** vs **deployment model** | Where data may live is a different question from where the runtime must execute. |
| **A published constraint** vs **a measured behaviour** | A documented limit excludes designs; it never proves performance. |
| **Average load** vs **peak load** | Sizing on the average is sizing for the case that never fails. |
| **Effort** vs **elapsed duration** | A two-hour task inside a nine-day process is a nine-day process. |
| **Availability of a platform** vs **availability of a business flow** | The second is computed from every dependency on the path; the first is one input to it. |
| **A backup exists** vs **recovery is possible** | Restore is a procedure with a duration, not a button. |
| **Number of people** vs **number of (person, capability) pairs** | Different cost drivers. |
| **"Real time"** vs **the one interface that needs it** | The general ask is almost never the specific requirement. |

---

# Part B — Contextual vendor vocabulary (quarantined)

> **PHASE: options+ · NOT Discovery reasoning vocabulary.**
> One purpose only: when a participant uses a product name, translate it back into the Part A concept and record *that*. Nothing here may be used to select, shortlist, favour or exclude anything.

A participant says a product name → note it as *current state* or *stated expectation*, whichever it is → ask the Part A question → record the answer as the requirement. The product name never enters the Shared Understanding as a requirement.

| If a participant says… | It is evidence of… | Ask instead, and record |
|---|---|---|
| a low-code platform or app-building product by name | a stated expectation about the *surface*, or an existing estate | Who are the users, on what devices, at what response expectation, with what bespokeness? → A4 |
| a managed relational data service by name | an expectation about the *store* | What are the entities, relationships, access granularity and volume requirements? → A3 |
| a document or list collaboration product | usually current state | Where do the records live today, who owns them, and what does the process actually need? → A3, A1 |
| a workflow or automation product by name | an expectation about the *mechanism* | What is the work shape, human wait and failure semantics? → A1 |
| an external-facing site product | an expectation about the *audience* | Which identity class, what population, knowable in advance or not? → A4 |
| an assistant or agent product by name | a conversational expectation | Is the ask retrieval and summary, or task completion with side effects, and for whom? → A4 |
| "premium" / "we'd need licences for that" | an entitlement concern | Which capabilities does the requirement imply, for which audience, and what is held today? → A6 |
| "we'd need a separate environment for that" | an isolation or lifecycle requirement | Which isolation domains do the lifecycle and the audience actually require? → A5, A6 |

Product definitions themselves — platform components, app types, connector classes, licence plan names, packaging and lifecycle artefacts — belong to the Options vocabulary and are not authored here.


---

# Part C — Options vocabulary

> **PHASE: options+.** Four terms, added because the absence of a shared meaning would materially damage
> the decision conversation. Everything else the Options procedure runs on is **internal** — exit-scope
> codes, depth codes, outcome numbers, register ids — and never becomes engagement vocabulary.

| Term | Meaning in Options |
|---|---|
| **Option class** | The *kind* of response an option is: change the process, extend what already exists, use tooling the organisation already has, buy a product, build on a low-code platform, build custom, assemble cloud services, let the incumbent system own it, split it, or do nothing. Without this word the option space silently collapses into a set of architectures for one platform, and a sponsor comparing two architectures is being shown one class presented as the whole choice. |
| **Disqualifier** | A requirement an option **cannot** satisfy, at a **named scope** — the whole solution, or one named responsibility. Two grades, and the difference matters: a **settled** disqualifier rests on confirmed, current evidence; a **provisional** one rests on an assumption and is carried with its basis, never rendered as settled. The single most important thing a reviewer must be able to challenge: *what exactly ruled this out, and how sure are we?* |
| **Comparator evidence absent** | We can say this option is excluded. We **cannot** say the replacement is better, because no comparison exists. It is part of the outcome sentence, not a caveat on it — without the shared meaning, *"excluded → candidates"* is read as *"candidates are better"*, which is the exact error it exists to prevent. |
| **Graduation trigger** | The named condition under which a *"the lighter option is sufficient"* answer must be revisited. Mandatory whenever that answer is given, because the documented growth path out of the lighter surfaces is a **one-way upgrade** that converts every user to the paid tier. Without the trigger, that answer is a trap. |

**Two terms Options reuses from Part A rather than restating.**

- **Precondition** (A5) — something that must become true before the work can proceed: *a deliverable with
  an owner and a cost, not a footnote*. Options adds only that it must also be **dated**.
- **Proof requirement** (A5) — what evidence a commitment requires before it can be made, and what it
  costs: published-limit arithmetic · a bounded pilot · an engineered test harness · a production-like
  proof. **This is the single shared term. *Validation level* is not a second term for the same thing** —
  the four levels are the *values* of the proof requirement, and Options states **and budgets** which one
  the commitment needs.

**Not vocabulary, deliberately.** *Branch* keeps its word but loses its role — it is an architecture
shape chosen **after** an outcome, never an option class. *Score*, *fit rating* and *weighting* do not
exist here: there is no scoring model. *Pros and cons* are replaced by the sharper distinction between
**strengths**, **trade-offs** and **disqualifiers**, which carries decision meaning that a two-column
list does not.
