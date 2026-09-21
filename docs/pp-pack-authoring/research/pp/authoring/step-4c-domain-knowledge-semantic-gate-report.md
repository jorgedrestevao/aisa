# Step 4C — Domain Knowledge Semantic / Pull Gate

<!--
provenance: AUTHORING GATE REPORT
date: 2026-09-04 (Step 4C)
scope: BEHAVIOURAL. Tests whether the authored domain-knowledge layer behaves correctly under material
       decision pressure. No taxonomy redesign, no re-authoring, no new research, no web access,
       no canonical-research modification, no Step 3 or Step 5 change.
runtime modified during the initial gate: NO.
-->

## 1. Gate basis

### 1.1 What was tested

The runtime under test, pulled only as the fixtures required it:

- `library/packs/pp/domain-knowledge/README.md` — the use contract (read in full; it is the entry point).
- The 15 RESEARCH units — **pulled per fixture, never preloaded**. Nine of the fifteen were opened at all.
- Step 3, consulted only where a fixture genuinely required it: `decision-tree.md` (§4, §7.2, §9, §11),
  `decision-model/volatility-register.md` (§0, §1, §2A rows, §3), `decision-model/blocking-set.md`
  (`B-08`, `BS-01`, `BS-03`), `decision-model/composed-disqualifiers.md` (`CD-05`, `CD-06`).
- `pack.yaml` — the `domain_knowledge` block, to confirm the manifest is not a router.

Gate-side only, never given to the simulated reasoner: `step-4b-research-gaps.md`,
`step-4b-runtime-provenance.md`, `step-4b-number-adjudication.md`.

### 1.2 Two documentation-only corrections applied before the gate

Both in `step-4b-domain-knowledge-implementation-report.md`. No runtime file changed.

| # | Location | Change |
|---|---|---|
| A | §12.1 priority gap **#4** | Stale rationale *"no register row"* replaced with *"volatility ownership now exists (`VS-21` / `VS-22`); the actual control-enforcement / propagation latency remains a knowledge/evidence gap requiring verification"*. **Gap classification unchanged.** |
| B | `Q4-09` row | *"14 priority research gaps"* → *"14 priority **knowledge** gaps"*. Status text and closure-mechanism distinction preserved verbatim. |

### 1.3 The behaviour chain the gate exercises

```text
engagement evidence + material concern → concrete technical question
  → first knowledge pull → reasoning at proportional depth
  → second pull ONLY on a real exposed dependency
  → supported conclusion  OR  UNKNOWN / verification / measurement
  → return to the decision model, which owns the verdict
```

### 1.4 Structural precondition confirmed before fixtures ran

`pack.yaml` §`domain_knowledge` is annotated in-file as *"A MANIFEST — the units that exist. NOT a load
order, NOT a routing table, NOT a concern map, NOT a priority list."* `README.md` §1 states the pull rule,
and its *"No router"* clause names the whole retrieval mechanism: directory = subject boundary, filename =
question domain, **§0 of each unit = the questions it answers**. The gate therefore tested retrieval
against §0 alone.

---

## 2. Fixture set

17 fixtures (target ≈16; one extra was required because `G-001` is a mandatory standalone fixture under §13
and could not be folded into the automation fixture without losing the retry/idempotency principle test).

| Id | Dimension | Engagement shape |
|---|---|---|
| `F-01` | application surface · **ambiguous cross-domain pull** | Field engineers, offline, three confidential columns |
| `F-02` | data/store | Operational store + management dashboards on growing tables |
| `F-03` | delegation/query | Named screen filter over a growing table |
| `F-04` | automation | Retry on a payment-posting step; definition growing |
| `F-05` | integration · **conflicted fact** | High-frequency custom connector to a logistics API |
| `F-06` | security | Per-user row authorization behind a shared connection |
| `F-07` | governance | Requirement for an in-product release gate |
| `F-08` | ALM/reversibility | Sponsor asks *"can we roll back?"* |
| `F-09` | performance/scale | 2,500 concurrent users at month-end peak |
| `F-10` | economics | Solution to be resold to three client organisations |
| `F-11` | operability | Broker + worker design, no named operator, 4-hour RTO |
| `F-12` | architecture composition | Virtualize an external ERP reference table |
| `F-13` | **volatile numeric reading** | Synchronous ERP round-trip inside a user wait |
| `F-14` | **outside-corpus gap** | Delivery partner hands over to customer operations |
| `F-15` | **agent/conversational gap** | Conversational intake assistant is the requested capability |
| `F-16` | **pilot gap · over-blocking** | Dated interface refresh on a back-office surface |
| `F-17` | **empirical-test gap `G-001`** | ERP integration writes must be validated server-side |

---

## 3. Per-fixture results

Notation: **FP** = first pull · **SP** = second pull.

### F-01 — offline together with field-level confidentiality
- **Fragment.** 40 field engineers, rural sites, no connectivity for hours; the asset record carries three
  columns (contract value, incident cause, remediation cost) readable only by two regional managers.
- **Material concerns.** C3 (surface), C6 (security).
- **Question.** *Can a surface deliver full offline while three columns remain confidential from the offline
  population?*
- **Expected FP.** `application/application-surfaces.md`. **Actual FP.** same — §0 bullet 2 names the pair
  verbatim (*"can it deliver offline alongside field-level confidentiality?"*).
- **SP.** Yes — `security/security-controls.md` §7 (authorization grain per store). **Justified:** the
  boundary verdict was complete after FP; the SP was needed only for the *second* half of the question —
  what would satisfy the confidentiality requirement if the offline requirement is dropped. Application §10
  names the dependency explicitly (*"→ security. Offline depth and field-level confidentiality are a
  documented mutual exclusion"*), so the SP was dependency-driven, not precautionary.
- **Grade used.** `decision-grade` only (§5.1, §6, §10).
- **Stable principle.** Offline is five distinct depths, not a boolean; record-centric offline does not
  support field-level security or field sharing; full offline-first exists only over the governed store.
  *"The combination that has no answer on this platform: offline together with field-level confidentiality."*
- **Volatile row.** `VS-38` (offline cache bounds) named but **not** needed — the requirement fails on the
  exclusion, not on a ceiling. Register **not** consulted.
- **Gap.** `G-025` (offline record-set ceiling) present and correctly irrelevant.
- **Conclusion.** Unsatisfiable as stated. Three named resolutions: move the confidential columns out of
  offline scope (data-model change), drop offline, or the requirement leaves the platform.
- **Epistemic status.** Confirmed (stable, vendor-documented).
- **Verdict ownership.** Decision model. The unit states the exclusion and the three resolution shapes; it
  selects none and names no option class.
- **PASS.**

### F-02 — do the dashboards force a second store?
- **Fragment.** 1.2 M rows/yr, growing; managers need month-over-month aggregation charts and 3-year history;
  dashboards must render for ~400 users at month-end.
- **Concerns.** C4, C9. **Question.** *Does the reporting requirement force a second store, and what does the
  copy oblige?*
- **Expected FP / Actual FP.** `data/store-boundaries.md` — §0 bullet 2 is the question; §6 is titled with it.
- **SP.** `performance/performance-and-scale.md` §7, §10. **Justified:** §6 settles *whether* a copy is
  required; the *"renders for 400 users at peak"* clause is a workload commitment that §6 does not and
  cannot answer. Dependency named in store-boundaries §8.
- **Stable principle.** Aggregation/charts/multi-year history on growing tables ⇒ analytical copy from day
  one; and a copy obliges a reconciliation owner, a drift-detection method that is **not** row counts,
  resynchronisation as a routine budgeted operation, rebuilt authorization, capacity, erasure propagation and
  a schema-change owner. From SP: *limits exclude, they do not prove.*
- **Volatile row.** `VC-07` (analytical replication storage ratio, unpublished). Register consulted — the
  value is not decision-changing at this stage, so it is carried as a documented absence, not re-verified.
- **Gaps.** `G-026` (`measurement` — no published row/size envelope for a standard table), `G-029`, `G-030`.
- **Conclusion.** Copy required; seven obligations enumerated; read-only analytical endpoint preferred where
  no write is needed. The rendering commitment is **not settled** — load/soak test at projected peak
  *frequency* in a production-class environment.
- **Epistemic status.** Confirmed (copy requirement) + measurement obligation (rendering).
- **Verdict ownership.** Decision model. No store named as winner.
- **PASS.**

### F-03 — delegation-safe is not fast
- **Fragment.** One screen filters open items by status + region + date over a table heading to ~800 k rows;
  the team reports it *"already works in the test environment"* on 4 k rows.
- **Concern.** C4. **Question.** *Is this access path delegation-safe, and does delegation-safe also mean
  fast enough?*
- **FP.** `data/query-and-delegation.md` — §0 bullet 1 is the question verbatim. **Single pull.**
- **SP.** None. §6 answers both halves and states its own evidence boundary; nothing material was exposed.
- **Stable principle.** Delegation is a **correctness** property; *"a design that violates no documented
  limit is not thereby known to be fast; it is only known not to be structurally excluded"*; the fixed tuning
  order (do not make the call → fewer, wider calls → only then parallelism).
- **Volatile row.** None needed. Register **not** consulted — the principle needs no figure.
- **Gap.** `G-003` (`commission` — per-operation delegation table per connector). Correctly surfaced: the
  class-level boundary answers the architecture question; a **named screen filter** needs the operation
  level, which the baseline does not carry. Emitted as a design-time verification item, **not** a blocker.
- **CRAFT temptation.** `craft/powerfx.md` was **not** pulled. The unit's §0 states it is the single
  authority for delegable-operation behaviour and that `powerfx.md` refers *to it*, never the reverse.
- **Conclusion.** The correctness verdict is answerable at class level; the 4 k-row test proves nothing about
  800 k rows; latency is unproven and needs a row-limit-1 delegation proof plus a shaped server-side read.
- **Epistemic status.** Confirmed (principle) + Unknown (per-operation verdict, `G-003`).
- **PASS.**

### F-04 — retry on a non-idempotent side effect, and a growing definition
- **Fragment.** A flow posts a payment instruction to the finance system, then emails the supplier. Ops
  enabled retry after transient failures. The flow is at ~180 actions and growing; a maker proposes
  *"splitting it across Logic Apps because it's too big"*.
- **Concerns.** C2, C4. **Question.** *What does retry do to this side effect, and does the definition size
  force relocation?*
- **FP.** `automation/automation-mechanisms.md` — §0 bullets 1 and 2. **Single pull.**
- **SP.** None justified. §7 answers reliability in full; the ordering/broker escalation is named but not
  material here (single stream, low volume).
- **Stable principle.** *Retry without an idempotency key duplicates the side effect* — idempotency is a
  precondition for enabling retry on a side-effecting action, not a later refinement. One retry owner per
  call chain. There is **no rollback**; a mid-way failure leaves completed actions completed, and any
  multi-write design must answer three questions in writing. External non-idempotent side effects go last
  and/or behind a claim-check.
- **Volatile reading (not decision-changing).** `VS-24` structural ceilings — stated as a **documented
  reading with its stamp** and used only to refute the relocation proposal: the ceilings are *identical on
  both platforms*, so the consequence is **decomposition, not relocation**. Also `VS-39` retry profile
  (documented reading; recorded because a 20-minute transient outage is survived on one profile and lost on
  another). Neither was re-verified — neither changes the decision, and both were reported as readings, not
  as timeless facts.
- **Gap.** `G-060` (`commission` — documented mid-loop failure behaviour) surfaced; substituted by the three
  written post-failure questions, which is the authored treatment.
- **CRAFT temptation.** `craft/flow-craft.md` **not** pulled — no build question was asked.
- **Conclusion.** Retry must be disabled or made idempotent (alternate key + upsert, or an explicit
  idempotency-key check) before it is enabled; *"too big, so move it"* is unsupported.
- **Epistemic status.** Confirmed principle; volatile ceilings carried as stamped readings.
- **PASS.**

### F-05 — the conflicted custom-connector ceiling
- **Fragment.** A custom connector to a logistics API, ~9 calls/second sustained during dispatch windows; the
  business case rests on that throughput; the integration also becomes a production dependency.
- **Concerns.** C5, C9, C11, C10. **Question.** *Does the mechanism support this rate, and what does the
  answer cost?*
- **FP.** `integration/integration-mechanisms.md` — §0 bullet 1. §10 is titled *The conflicted ceiling*.
- **SP.** `operations/operability-and-support.md`. **Justified:** integration §13 states that throttling rate
  is *an early warning of an outage with a fuse*, that sustained breach disables the artefact, and that every
  stream needs a reconciliation owner — a named operational obligation, not a precaution.
- **Conflict behaviour.** Neither published figure carried on either side. **No average. No conservative
  pick. No settled claim.** The uncertainty is propagated symmetrically — the unit states in-file that the
  block *"cuts across the platform, cloud-native and hybrid classes equally; it is not a penalty against this
  platform."* Because sizing rests on it: **`DECISION BLOCKED`** preserved.
- **Ownership.** `VC-01` / `VS-08` (volatility §3, the live conflict) · `B-08` (blocking set) · `CD-05`
  (composed row). All four named. Register consulted (§3) and blocking entry consulted.
- **Distinction held.** `VS-27` (connector and integration execution envelope) was read for the *other*
  per-connection windows, and the unit states explicitly that the conflicted ceiling is **not** part of that
  family — so the reasoner did not launder the conflict into a settled envelope figure.
- **Closure.** Re-read **both** current sources at the decision date **and** measure representative workload.
  The documented escalation path may be *proposed as a mitigation*, never relied on in advance.
- **Gap.** `G-058` (`measurement`, blocking).
- **Conclusion.** No throughput claim. Two dated readings + one measurement, then the decision model resolves.
- **PASS.**

### F-06 — per-user row authorization behind a shared connection
- **Fragment.** Case records in a relational store; each caseworker must see only their own rows; the proposed
  app uses one connection created by the maker. The security lead also mandates an IP restriction.
- **Concerns.** C6, C11. **Question.** *Does this design still enforce per-user authorization, and what does
  the mandated control oblige?*
- **FP.** `security/security-controls.md` — §0 bullet 2 (*"Does this design change who the backend sees?"*).
- **SP.** `economics/licensing-and-cost-drivers.md` §6, §9. **Justified:** security §12 states its own
  boundary — *"this file carries only the obligation to look"* — and names the meters and populations as
  living in economics. The dependency is material because the IP firewall puts a population, not a user, in
  scope.
- **Stable principle.** *Shared identity collapses per-user authorization to a single principal* — and two
  further collapses ride along: **attribution** (the audit record captures the acting identity) and
  **throughput** (service protection is per identity, so one account is one budget). Secured shared
  connections are hygiene, not an authorization model. From SP: the entitlement boundary is where a technical
  choice silently sets the commercial model for a whole population; multiplexing to avoid it is prohibited
  and carries a documented right of suspension.
- **Volatile.** `TW-V3` (dated managed-environment licence enforcement) surfaced as a stamped reading;
  `VC-05` named. Register consulted.
- **Gaps.** `G-002` (`commission`, blocking — whether one premium capability obliges premium entitlement for
  *every* user of the artefact): carried as a **per-engagement verification item, never an assumption**, per
  the authored treatment. `G-077` (premium-suite prerequisite arithmetic) deferred to economics as authored.
- **Conclusion.** The design does not enforce the requirement; only an explicit per-user database identity or
  a mediation tier setting per-request user context restores the predicate, and a canvas app on the store's
  connector has neither hook (feeds `CD-06`). The IP firewall requires the managed class, which scopes every
  active user of the environment. The entitlement arithmetic is an **evidence obligation**, unresolved.
- **Comparator check.** No claim that another class does this better; the unit's §17 forbids it.
- **PASS.**

### F-07 — release gate requirement → estate precondition
- **Fragment.** Audit requires that no unmanaged customization reach production and that every release pass a
  code-quality gate. The project has one environment and no platform-team contact.
- **Concerns.** C7, C8. **Question.** *What tenant/estate preconditions does this control level require, who
  owns them, and are they funded?*
- **FP.** `governance/governance-and-environments.md` — §0 bullet 1 verbatim.
- **SP.** `alm/release-and-lifecycle.md` §5. **Justified:** governance §16 states the dependency concretely —
  the release gates are governance settings a project *inherits*, and in-product pipelines require managed
  target environments, which makes in-product ALM a tenant entitlement decision.
- **Stable principle.** Almost every enforceable lever is configured **outside the solution, by someone not
  on the project**; preventive levers are **forward-only** (they do not reach what already exists); the
  promotion path must exist before makers are enabled.
- **Volatile.** `TW-V1` (dated pipeline-target auto-conversion) surfaced; register consulted; not settled.
- **Gaps.** `G-080` (`commission`, blocking — de-scoping guidance ahead of dated licence enforcement),
  `G-087` (`pilot` — whether the conversion completed), `G-090` (`pilot` — break-list churn).
- **Conclusion.** The control is available but **not in the project's gift**: an estate precondition with a
  named owner, an entitlement consequence and a dated verification. A single-environment topology cannot
  carry the gate at all.
- **Verdict ownership.** Decision model. No outcome class asserted.
- **PASS.**

### F-08 — "can we roll it back?"
- **Fragment.** The sponsor wants a written rollback commitment before go-live. The team has an in-product
  pipeline and points at *"we deploy through pipelines, so we can redeploy the old version"*.
- **Concerns.** C8, C12. **Question.** *Can this be reversed — and was the mechanism enabled in time?*
- **FP.** `alm/release-and-lifecycle.md` — §0 bullet 2 verbatim. **Single pull.**
- **SP.** None. §8.1–§8.3 answer completely; the restore side effects are stated in-unit.
- **Stable principle.** *An environment/release mechanism does not imply rollback.* There is **no solution
  rollback** — three imperfect paths only. **Restore is not a rollback** and has documented side effects.
  And §8.3: *reversibility mechanisms often must be enabled BEFORE they are needed* — *"We can roll it back"
  is false unless a specific mechanism has been chosen, switched on and tested.*
- **Volatile.** None decision-changing; no figure quoted.
- **Gap.** `G-005` (`commission`, blocking — whether previous-version redeployment is on by default, and its
  retention limits). **Correct closure behaviour:** the gap is *not* converted into "research required". The
  runtime states the **enable-in-advance obligation** without the default, so the engagement action is a
  target-environment configuration check with a named owner — the commission candidacy is an authoring-side
  matter, not an engagement blocker.
- **Conclusion.** No rollback commitment is defensible until the pipeline setting is verified enabled, the
  mechanism named, its destruction list accepted and a rehearsal timed.
- **Over-blocking check.** Not blocked — verifiable in the target environment.
- **PASS.**

### F-09 — 2,500 concurrent users
- **Fragment.** Month-end close: ~2,500 users in a 90-minute window, all writing to a shared approval-queue
  record, and all reads going through one service account for a legacy lookup.
- **Concerns.** C9, C11. **Question.** *Which meter binds first for this workload, and is the requirement
  inside or outside it?*
- **FP.** `performance/performance-and-scale.md` — §0 bullet 1 verbatim.
- **SP.** `economics/licensing-and-cost-drivers.md` §5. **Justified:** the funnel analysis shows the binding
  constraint is the per-identity request budget, which is simultaneously a **meter** — performance §13 names
  the economics dependency, and the fixture's window makes request-meter consumption material.
- **Stable principle.** *No concurrent-user figure is published for any application surface.* Concurrency is
  governed instead by per-identity limits and by contention on shared identities and shared rows — *"the real
  question is where does many users' traffic funnel onto one identity or one row, not how many users are
  supported."* The five meters do not pool; a design passes only if it fits all of them separately.
- **Measurement obligation emitted.** A tested baseline against a **production-like** environment with
  realistic personas, roles, security configurations, data sets and volumes, at **peak frequency, not
  test-data volume**; funnel points sized and tested individually. Explicitly *not* "the platform supports N
  concurrent users".
- **Gaps.** `G-027` / `G-027b` (`measurement`), `G-063` (`measurement` — the corpus is limits-based, and the
  absence is carried **as evidence**), `G-028` (write amplification, measured per engagement or Unknown).
- **Conclusion.** Two structural findings (the shared record, the shared service account) are stated as funnel
  points; the concurrency requirement itself is **unproven and unprovable from documentation**.
- **Comparator check.** The unit states in-file that a boundary here supports *excluding a design*, never
  *preferring a class*. Honoured.
- **PASS.**

### F-10 — resale to three client organisations
- **Fragment.** The sponsor intends to resell the solution to three external client organisations and wants a
  per-client cost figure for the business case.
- **Concerns.** C11, C12. **Question.** *Which meter moves with this audience shape, and is this commercial
  model permissible at all?*
- **FP.** `economics/licensing-and-cost-drivers.md` — §0 bullets 1 and 2. **Single pull.**
- **SP.** None justified — the answer terminates at a scope-blocker; deepening elsewhere would be ceremony.
- **Behaviour.** No price invented (§12 forbids any price, SKU or per-unit currency figure — verified: none
  present anywhere in the directory). Mechanisms, meters and affected populations supplied.
  `craft/estimation-model.md` was **not** pulled; the file itself carries a *"NOT VALID AS COMPARATIVE
  ECONOMICS"* banner, and the reasoner honoured the boundary without needing to open it.
- **Gaps.** `G-014` (`commission`, blocking — multi-tenancy and resale licensing is an unclosed gap) →
  scope-blocker `BS-01` · `VC-09`. `G-102` (`outside-corpus`) surfaced correctly: the unit **refuses** a
  comparative total-cost-of-ownership against named alternative classes and routes to the symmetric method.
- **Conclusion.** No answer offered on resale permissibility. Closure = a **dated written position** from the
  licensing owner plus the customer agreement — a `documento`-cost obligation, not a research commission. Per
  `BS-01`, the **commercial model** is blocked while the technical decision may still proceed on its own
  scope.
- **Comparator check (N3).** No inference that the platform is cheaper. The unit states that no cost or
  entitlement claim is `Confirmed` from documentation; all are `Assumed` with a validity date and a named
  validation owner.
- **PASS.**

### F-11 — technically feasible, not currently operable
- **Fragment.** The design that meets the ordering and replay requirements uses a broker plus a worker
  service. IT has no message-broker skills, no on-call rota beyond office hours, and the business states a
  4-hour recovery-time objective.
- **Concerns.** C10, C9. **Question.** *Can this organisation actually run this design, and is this recovery
  objective evidenced or asserted?*
- **FP.** `operations/operability-and-support.md` — §0 bullets 1 and 3. **Single pull.**
- **SP.** None justified — §8, §9 and §13 answer both halves in-unit.
- **Stable principle.** *Backup is not recovery.* A manual backup is a timestamp and a label over the
  continuous backup — not downloadable, not exportable, not an archive and not a legal hold. **Restore is not
  a rollback** (nine documented breakages enumerated). And §13: where a design includes a component the
  platform does not operate, that component requires a named operator, an on-call route, its own release
  pipeline and its own monitoring; without one, *"the capability is unavailable because no operator exists"*.
- **Volatile reading.** `VS-07` backup retention by environment class, carried as a stamped documented
  reading, plus `VS-17`. **Not decision-changing for the verdict** — the objective fails on the absence of a
  timed rehearsal, not on the retention number — so it was reported as a reading with its re-verify trigger,
  not settled as fact.
- **Gap.** `G-013` (`measurement`, blocking — measured restore duration at representative volume).
  **Measurement obligation emitted:** a **timed restore/recovery rehearsal at representative data volume**.
  The reasoner did **not** infer recovery time from retention or from backup availability.
- **Conclusion, in the required form.** *Technically feasible; not currently operable as drawn.* Explicit
  obligations: named operator, on-call route, release pipeline, monitoring, reconciliation/dead-letter owner;
  and the 4-hour objective is **asserted, not evidenced**.
- **Comparator check (N4).** The operational burden is stated as a capability boundary plus an obligation
  set. The unit says it in-file: *"'Unavailable because no operator exists' is a capability boundary, not a
  comparative judgement… it does not rank the organisation, and it does not make any other option better."*
  No automatic rejection.
- **PASS.**

### F-12 — one composition, in a 924-line unit
- **Fragment.** An external ERP owns the material master. The team proposes virtualization so the records
  appear native. A compliance requirement restricts rows to the owning plant's staff, and a later phase wants
  to write corrections back.
- **Concerns.** C12, C5, C6. **Question.** *Does this composition carry per-row authorization, and what does
  it import?*
- **FP.** `architecture/patterns.md` → **§5 → `### Data virtualization`**. **Single pull, one composition.**
- **Navigation observed.** The reasoner reached one named `###` composition heading, not ten equal candidates.
  §5's ten compositions each carry the same fixed sub-structure (Intent · Prerequisites · Mechanisms composed
  · Strengths · Weaknesses · Risks · **What it imports** · Escalation consequence · Lineage), so the unit is
  addressable at composition granularity.
- **Imported obligations followed selectively.** Only *Governance* (who owns the upstream availability and
  security contract) and *ALM* (the upstream schema is an external dependency that can break the application
  with no platform release) were followed, because the fixture engaged them. Cost, Monitoring, Recovery and
  Operator imports were read and **not** deepened — no second pull.
- **Conclusion.** The row-restriction requirement is excluded by the composition: only organisation-owned
  tables are supported, user-owned filtering is not, field-level security is not supported, auditing is not
  supported, and the **virtual-versus-standard decision is irreversible in place**. Escalating to replication
  buys the exclusion list back at the cost of the whole synchronization risk register — and is a rebuild of
  the modelling layer, not a setting.
- **Weak lineage remained visible.** For the write-back phase: *"write-through virtualization is conditional
  with weak production evidence and `UNKNOWN` performance characteristics"* — treated as `UNKNOWN` until a
  representative pilot (`G-112`, `commission`, blocking). Not upgraded to a capability claim.
- **Pattern is not the Options space.** The composition was reasoned about *given the option class was
  already established* (§0 bullet 1 states this precondition). No branch, no winner, no blueprint.
- **PASS.**

### F-13 — a volatile number that changes the requirement
- **Fragment.** On submit, the app must call the ERP, receive a costing result and show it to the user before
  the screen advances. Finance says the ERP call *"usually takes about two and a half minutes"*.
- **Concerns.** C2, C5, C3. **Question.** *Can this be synchronous at all, and if not, what is the shape?*
- **FP.** `automation/automation-mechanisms.md` §5. **Single pull.**
- **Volatile behaviour — the decision-changing case.** The unit's stamped reading (`VS-23`, *design time,
  before any synchronous commitment*) places the inbound and outbound synchronous ceilings in the low
  single-digit minutes. The stated ERP duration sits **immediately against** that ceiling, so the reading is
  decision-changing. The reasoner therefore:
  1. reported the figures as a **documented reading with its date**, not as fact;
  2. **refused to settle** the conclusion on `read 2026-09-04` — it required a **current verified value** at
     the decision date, recorded on the engagement's own SU row (`verificado_em` + `validade`);
  3. stated the stable half that survives any re-reading: *the synchronous-response boundary is a
     platform-family property, not a product weakness* — the ceilings differ **by degree, not by order of
     magnitude**, so relocation does not buy the requirement, and above the window **the requirement itself
     must change** to accept-and-poll or webhook-callback.
- **Register behaviour.** `volatility-register.md` consulted for `VS-23` only — its re-verification trigger,
  not a value. The register supplied **no figure** (it supplies none, by its own §5), and was not walked.
- **Gap.** `G-098` (`commission` — whether the application request-timeout envelope applies to all
  application surfaces or only one). Carried at mechanism level only, as authored.
- **Conclusion.** *Provisionally outside the synchronous window; verify the current ceiling and the ERP's
  measured p95 before any synchronous commitment.* The design consequence is named (accept-and-poll plus a
  status resource), not chosen.
- **PASS.**

### F-14 — outside-corpus, and correctly not a blocker
- **Fragment.** A delivery partner builds and then hands over to a small internal operations team. The
  sponsor asks what the handover must contain.
- **Concern.** C10. **Question.** *Who operates this after handover, and what does the baseline say the
  handover must contain?*
- **FP.** `operations/operability-and-support.md` §13. **Single pull.**
- **Behaviour.** The unit states plainly that handover from a delivery partner to a customer operations team
  is **entirely undocumented in the baseline** and instructs: *"Treat it as a deliverable to define, not a
  fact to look up."*
- **Gap.** `G-106` (`outside-corpus`, blocking-flagged, *likely permanently open*). Correct handling:
  1. the pack and canonical baseline do **not** provide the evidence — stated explicitly;
  2. **nothing invented** — no handover checklist presented as vendor guidance;
  3. **no research commission requested** — an `outside-corpus` gap is not closed by reading more;
  4. the generic engagement decision proceeds: the requirement becomes an **engagement deliverable** with a
     named owner and a persistence test (*in-house and available now, or an explicit, funded and dated
     commitment*), which is the authored substitute.
- **Over-blocking check.** Not blocked. The gap changes what the engagement must produce, not whether the
  decision can be made. *Unsupported is not automatically a blocker* — demonstrated.
- **PASS.**

### F-15 — the agent / conversational boundary (mandatory)
- **Fragment.** The requested capability **is** a conversational intake assistant: employees describe an issue
  in free text, it asks follow-up questions, classifies and raises the record. The sponsor has seen a vendor
  demo and wants to know fit, cost and controls.
- **Concerns.** C1, C2, C3, C6, C11. **Question.** *Can this platform carry a conversational/agentic surface,
  at what cost, under which controls?*
- **FP.** `application/application-surfaces.md` → **§8 Conversational and agentic surfaces — the boundary**.
  **Single pull.**
- **Behaviour observed.**
  - **No agent domain file exists** and none was expected — the reasoner did not search beyond the directory
    it was already in, and did not treat the absence as a retrieval failure.
  - **No inference from automation knowledge.** `automation/automation-mechanisms.md` was **not** pulled to
    substitute for agent capability; its own §14 records the same silence (`G-119`).
  - **No invented licensing.** Consumption is stated as task-complexity-dependent and therefore
    **unmodellable in advance**. No meter, no bundle, no figure.
  - **No invented security or control behaviour.** Agent-specific authentication and channel controls are
    stated as preview; governance beyond data policies, virtual connectors and sharing is not asserted
    (`G-083`).
  - **No "PP is suitable because the pack is PP".** The unit states fit is `UNKNOWN` **in every option
    class**.
  - **No silent substitution** of a canvas or chat surface for the requested modality.
  - **Decision blocked**, because the requirement is material: `BS-03` (which also blocks *the modality
    question itself* at the autonomous end), volatile row `VS-20`, dated tripwire `TW-V2`.
  - **Instruction honoured:** *"Do not produce a candidate set, a comparison, or a capability claim for this
    surface class."* None was produced.
- **Gaps.** `G-118` / `G-119` (`commission`, blocking) — recorded as the one **dedicated** future
  research-commission candidate, because they are material, recurring and **not** closable by engagement
  measurement.
- **Conclusion.** `UNKNOWN` in every dimension; the honest output is **decision blocked, not a candidate
  set**.
- **PASS (mandatory).**

### F-16 — a pilot-class gap with no decision consequence
- **Fragment.** An internal back-office tool for 25 finance staff on a record-centric surface. No branding
  requirement, no external audience, no accessibility mandate beyond internal policy. A team member raises
  that *"the interface is being refreshed at some point"*.
- **Concerns.** C8, C12 — assessed at **D1**, not D3.
- **Question.** *Does the dated interface refresh bear on this decision?*
- **FP.** `application/application-surfaces.md` §11. **Single pull.**
- **Behaviour.** `G-024` (`pilot` — the date of the mandatory interface refresh) is carried in the unit as *a
  dated change* with verification under `VC-10`. The reasoner:
  - did **not** turn it into timeless knowledge (no asserted date, no asserted behaviour);
  - did **not** raise an immediate general research commission — `pilot` closes by verifying and calibrating
    during the real engagement;
  - did **not** invent an arbitrary default.
- **Over-blocking check — the point of this fixture.** Per `decision-tree.md` §7.2(2) and §4, *"most gaps are
  `dimensionante` or `cosmético` and are simply carried. Do not force every gap to become decision-blocking."*
  The refresh has no decision consequence for this scope. **Unknown remains Unknown**; no `DECISION BLOCKED`.
  Also verified: no accessibility gap (`G-021`) was escalated, because no accessibility mandate is engaged.
- **PASS.**

### F-17 — `G-001`, the empirical-test gap (mandatory)
- **Fragment.** A nightly ERP integration writes ~4,000 rows through the Web API. Compliance requires that no
  row can be created with a cost centre outside the approved list. The team has implemented a table-scoped
  validate-and-error business rule and states *"the rule is server-side, so all writes are covered."*
- **Concerns.** C4, C6. **Question.** *Will this rule hold no matter which client writes — app, API,
  integration?* (`data/dataverse.md` §0 bullet 4, verbatim.)
- **FP.** `data/dataverse.md` §5. **Single pull.**
- **Behaviour observed.**
  - The canonical evidence is **contradictory**, and the unit says so: one part of the same vendor page states
    that table scope reaches *"Model-driven app forms and server"* and describes server-side rules as compiled
    synchronous plug-ins; the FAQ on that same page states flatly that business rules run on clients and
    *"aren't executed inside Dataverse"*.
  - The finding remains **`Assumed`, never `Confirmed`** — the unit states *"This is not resolved here and
    must not be resolved by inference."*
  - **Neither forbidden answer was produced.** No *"yes, business rules execute on all API writes"*; no *"no,
    they do not"*. The fixture supplies no target-environment evidence, so neither is available.
  - The **bounded target-environment test** was named concretely: activate a table-scoped validate-and-error
    rule, attempt a violating create through the Web API, observe.
  - The compliance requirement is decision-changing (a hard *"no row can be created"*), so the affected design
    decision **remains blocked** until the test result exists. The unit's own escape is stated and offered as
    the alternative, not as a resolution: where the guarantee is genuinely required — financial, regulatory,
    safety — use an explicit server-side mechanism or a key-level constraint rather than a business rule.
  - Adjacent supported facts used correctly, and they are the sharper findings: duplicate detection is **off
    by default on Web API updates**, so every integration write that does not explicitly opt in creates
    duplicates the interactive UI would have blocked; and when a rule does fire, the failure surfaces as a
    **server-error-class response, not a validation-class one**, so naive retry logic loops on a business
    rejection.
- **Gap.** `G-001` (`empirical-test`, blocking) — *the highest-value single test in the baseline*.
- **PASS (mandatory).**

---

## 4. First-pull discoverability

| Check | Result |
|---|---|
| One clear first pull identified in every fixture | **17 / 17** |
| Whole-directory scan required | **never** |
| A fixed concern→file routing map needed | **no** — `README.md` §1 states there is no router, and none was reconstructed |
| *"Load all relevant-looking units"* | **never observed** |
| First pull reached from the §0 question list alone | **17 / 17** |

**Ambiguity resolution — the three cases the gate was told to test:**

| Ambiguous case | Two plausible units | Selected | Why it directly owns the question |
|---|---|---|---|
| Offline + field confidentiality (`F-01`) | `application/`, `security/` | `application/application-surfaces.md` | Its §0 names the **pair** verbatim; security owns enforcement planes, not surface forfeits |
| Reporting + store choice (`F-02`) | `data/store-boundaries.md`, `performance/` | `data/store-boundaries.md` | §6 is titled with the question; performance was reached only once a workload commitment appeared |
| Hybrid + economics + operator (`F-05`, `F-10`, `F-11`) | `integration/`, `architecture/`, `economics/`, `operations/` | question-dependent: mechanism envelope → `integration/`; *can we run it* → `operations/`; *which meter moves* → `economics/` | Each unit's §0 phrases its own question in the requirement's own vocabulary; the three questions never collided |

No automatic multi-file loading was accepted anywhere.

**FIRST-PULL DISCOVERABILITY: PASS.**

---

## 5. Selective second-pull behaviour

Six fixtures created a genuine cross-domain dependency; all six matched the required exercise list.

| Fixture | Chain | What exposed the dependency | Verdict |
|---|---|---|---|
| `F-01` | offline → security | `application/` §10 *"→ security"* plus the fixture's second half | justified |
| `F-02` | data → performance | store-boundaries §8; the *"renders for 400 users"* commitment | justified |
| `F-05` | integration → operations | integration §13 (throttling as an outage-with-a-fuse; reconciliation owner) | justified |
| `F-06` | security → economics | security §12 states its own boundary and hands the meters to economics | justified |
| `F-07` | governance → ALM | governance §16 (release gates are governance settings; pipelines need managed targets) | justified |
| `F-09` | scale → economics | performance §13; the funnel is a per-identity budget, which is a meter | justified |

The mechanism that makes this work is structural: every unit carries a **`Consequences elsewhere`** section
naming the specific dependency and the specific unit that owns it. A second pull is therefore triggered by a
*named* dependency, never by the question *looking* complex.

Eleven fixtures resolved on one pull, including three where a second unit was plausible but nothing material
was exposed (`F-03`, `F-08`, `F-12`). No fixture required three or more pulls. No fixture pre-loaded related
files.

**SELECTIVE SECOND-PULL BEHAVIOUR: PASS.**

---

## 6. Stable-principle behaviour

Seven durable principles were exercised; in every case the principle was statable **without** a volatile
lookup, and none produced an option verdict.

| Principle | Unit · section | Volatile figure needed to state it? | Verdict produced? |
|---|---|---|---|
| Delegation-safe is not fast | `data/query-and-delegation.md` §6 | no | no |
| Retry + non-idempotent side effect creates duplication risk | `automation/` §7 | no | no |
| Limits can exclude but do not prove performance | `performance/` §7 | no | no |
| Backup is not recovery | `operations/` §8 | no (`VS-07` read as a stamped reading, not needed for the principle) | no |
| Shared identity collapses per-user authorization | `security/` §6.1 | no | no |
| Imports of a composition accumulate rather than disappear | `architecture/` §3, §5 escalation clauses | no | no |
| Environment/release mechanism does not imply rollback | `alm/` §8.1, §8.3 | no | no |

Each is anchored to a **`decision-grade`** section placed before any implementation content, which is why a
D3 pull could read the principle and stop.

**KNOWN + STABLE BEHAVIOUR: PASS.**

---

## 7. Volatility behaviour

Volatile readings engaged across five fixtures.

| Reading | Owner | Fixture | Decision-changing? | Behaviour |
|---|---|---|---|---|
| Synchronous response windows | `VS-23` | `F-13` | **yes** | Reported as a dated reading; **current verified value required** before settling; the stable half (family property, degree-not-order) stated separately |
| Orchestration structural ceilings | `VS-24` | `F-04` | no | Stated as a documented reading with its stamp; used only to refute *"too big, so move it"* (identical on both platforms, so decomposition, not relocation) |
| Connector and integration execution envelope | `VS-27` | `F-05` | partially | Read for the non-conflicted per-connection windows; the unit's own exclusion of the conflicted ceiling from this family was honoured |
| Backup retention by environment class | `VS-07` | `F-11` | no | Documented reading; the verdict rested on the absent rehearsal, not on the number |
| Retry profile by licence | `VS-39` | `F-04` | no | Reading, plus the design consequence (a 20-minute outage survived on one profile, lost on another) |
| List-store permission-scope ceiling | `VS-29` | surfaced via `F-06` cross-reference | no here | Stamped reading in `data/sharepoint.md`; correctly not used — the fixture's store was relational |
| Dated licence enforcement | `TW-V3` | `F-06` | yes, for costing | Dated tripwire named; entitlement arithmetic left as an evidence obligation |

No fixture treated `read 2026-09-04` as sufficient evidence for a future engagement decision. Where the
reading was decision-changing, the conclusion was explicitly held open pending a current verified value
recorded on the engagement's own SU row.

**KNOWN + VOLATILE BEHAVIOUR: PASS.**

---

## 8. Volatility-register behaviour

The three-layer split held in every fixture that touched a figure:

```text
knowledge unit        → the stable boundary, and why it exists
volatility row        → when currentness must be checked
Shared Understanding  → the value actually verified for this engagement (verificado_em + validade)
```

- The register was consulted in **7 of 17** fixtures, always for a **named row reached from a stamped
  reading**, never by walking it. `README.md` §5 and the register's own §0 both instruct *"Do not walk the
  register"*; behaviour matched.
- It did **not** behave as a current-facts database: the register supplies no figures at all (its §5), and
  every value used came from a stamped reading inside a knowledge unit.
- It was **never preloaded** — no fixture opened it before a figure became material.
- It did **not** become a second domain-knowledge layer: no fixture drew an explanation from it. Its rows
  supplied only scope, mechanism-distinctness rationale, and a re-verification trigger.

---

## 9. Conflict behaviour (`F-05`)

| Required behaviour | Observed |
|---|---|
| Identify the conflict | yes — `integration/` §10 is titled for it; two currently-maintained vendor pages disagree by 20x |
| Do not select either published figure | **neither carried** |
| Do not average | not averaged |
| Do not pick the conservative one and call it fact | not picked |
| Propagate uncertainty symmetrically | yes — stated in-unit that the block cuts across the platform, cloud-native and hybrid classes **equally**, and is *not a penalty against this platform* |
| Require measurement / current verification | yes — re-read **both** current sources at the decision date **and** measure representative workload |
| Preserve `DECISION BLOCKED` where decision-changing | yes — sizing and economics rest on it |
| Ownership named | `VC-01` / `VS-08` · `B-08` · `CD-05` — all four |

The escalation path was correctly handled as *proposable as a mitigation, never relied on in advance*.
**No settled throughput claim was produced anywhere in the gate.**

**CONFLICTED FACT HANDLING: PASS.**

---

## 10. Research-gap behaviour

All five closure classes exercised, with at least one per class, and the action differed by class — the
central test.

| Class | Gap | Fixture | Action taken | Turned into *"research required"*? |
|---|---|---|---|---|
| `commission` | `G-005` | `F-08` | Target-environment configuration check + enable-in-advance obligation | **no** |
| `commission` | `G-014` | `F-10` | Dated **written position** from the licensing owner (`BS-01`) | **no** |
| `commission` | `G-002` | `F-06` | Per-engagement **entitlement verification item**, never an assumption | **no** |
| `commission` | `G-118`/`G-119` | `F-15` | `UNKNOWN` + decision blocked + **dedicated** future commission candidate | commission is the correct class here |
| `commission` | `G-112` | `F-12` | Conditional with weak evidence; representative pilot | **no** |
| `empirical-test` | `G-001` | `F-17` | Named bounded target-environment test | **no** |
| `measurement` | `G-013` | `F-11` | Timed restore rehearsal at representative volume | **no** |
| `measurement` | `G-027`/`G-063` | `F-09` | Production-like load test at peak frequency | **no** |
| `measurement` | `G-058` | `F-05` | Workload measurement + two dated re-reads | **no** |
| `measurement` | `G-026` | `F-02` | Load/soak test at projected multi-year volume | **no** |
| `outside-corpus` | `G-106` | `F-14` | Baseline silence stated; becomes an engagement **deliverable**; not blocked | **no** |
| `outside-corpus` | `G-102` | `F-10` | Comparison **refused**; routed to the symmetric method | **no** |
| `pilot` | `G-024` | `F-16` | Verify/calibrate during the real engagement; Unknown carried, not blocking | **no** |
| `pilot` | `G-087`/`G-090` | `F-07` | Pre-costing verification against a dated tripwire | **no** |

**No unsupported completion occurred in any fixture. No gap was suppressed. No gap was inflated into a
generic research request.**

**UNKNOWN / GAP BEHAVIOUR: PASS.**

---

## 11. Empirical-test behaviour (`G-001`)

Covered in full at `F-17`. Summary against the forbidden outputs:

| Forbidden output | Produced? |
|---|---|
| *"Yes, business rules execute on all API writes."* | **no** |
| *"No, they do not."* | **no** |
| Any resolution by inference from the contradictory page | **no** — the unit states it *"must not be resolved by inference"* |
| `Confirmed` state | **no** — `Assumed`, as authored |

The bounded test was named; the decision remains blocked while the compliance requirement is
decision-changing and no target-environment evidence exists.

**G-001 EMPIRICAL-TEST BEHAVIOUR: PASS.**

---

## 12. Measurement behaviour

Four measurement fixtures. In each the reasoner emitted a **specific** obligation, not a generic one.

| Fixture | Required obligation | Emitted | Forbidden shortcut avoided |
|---|---|---|---|
| `F-09` | Production-like load test, realistic personas and volumes, **peak frequency not test-data volume**, funnel points sized individually | yes | *"the platform supports N concurrent users"* — never stated; no such figure exists |
| `F-11` | Timed restore/recovery rehearsal at representative volume | yes | recovery time **not** inferred from retention or backup availability |
| `F-02` | Load/soak at projected multi-year volume; rendering proven, not assumed | yes | no published service limit treated as proof of acceptable latency |
| `F-05` | Representative-workload throughput measurement + two dated re-reads | yes | neither conflicted figure adopted |

Fidelity conditions were carried, not just the word *"test"*: the same environment class as production, with
managed/network/security controls present where production depends on them, at peak frequency, and with the
five meters checked separately because they do not pool.

**MEASUREMENT OBLIGATION BEHAVIOUR: PASS.**

---

## 13. Agent / conversational boundary

Covered at `F-15`. Every forbidden behaviour was checked individually and none occurred: no inference from
automation knowledge, no invented licensing, no invented security or control behaviour, no *"PP is suitable
because the pack is PP"*, no silent substitution of a canvas or chat surface, no candidate set, no
comparison, no capability claim. Output: `UNKNOWN` in every dimension, **decision blocked** via `BS-03`,
volatile facts on `VS-20`, the dated entitlement removal on `TW-V2`, and a **dedicated** future
research-commission candidacy.

**AGENT GAP G-118/G-119: PASS.**

---

## 14. CRAFT boundary

Three fixtures created a CRAFT temptation; a fourth was available and also declined.

| Fixture | CRAFT file that could have tempted | Pulled? | What held the boundary |
|---|---|---|---|
| `F-03` | `craft/powerfx.md` (Power Fx delegation) | **no** | `data/query-and-delegation.md` §0 declares itself the single authority for delegable-operation behaviour, and states `powerfx.md` refers *to it*, never the reverse |
| `F-04` | `craft/flow-craft.md` (flow sizing) | **no** | No build question was asked; the structural ceilings are register-owned in `automation/` (`VS-24`) |
| `F-10` | `craft/estimation-model.md` (implementation estimation) | **no** | The file carries a *"NOT VALID AS COMPARATIVE ECONOMICS"* banner and states it has no comparator-side basis |
| `F-06` | `craft/security-craft.md` (security implementation) | **no** | The question was an enforcement-plane question, owned by `security/security-controls.md` |

No CRAFT file supplied a platform limit, a threshold, a comparative claim or an option-selection verdict in
any fixture. `craft/estimation-model.md` did **not** settle any comparative economics; `F-10`'s economics
conclusion rests on mechanisms, meters and an unclosed licensing gap.

**CRAFT BOUNDARY: PASS.**

---

## 15. Decision leakage

For each fixture: *did domain knowledge answer the technical question, or did it select or render the
option?*

| Fixture | Output class | Selection verdict produced? |
|---|---|---|
| `F-01` | limitation + resolution shapes | no |
| `F-02` | obligation set + measurement obligation | no |
| `F-03` | capability boundary + trade-off mechanism | no |
| `F-04` | limitation + precondition | no |
| `F-05` | evidence requirement (blocked, symmetric) | no |
| `F-06` | limitation + obligation + evidence obligation | no |
| `F-07` | precondition + ownership | no |
| `F-08` | limitation + precondition | no |
| `F-09` | boundary + measurement obligation | no |
| `F-10` | mechanism + meter + scope-blocker evidence obligation | no |
| `F-11` | capability boundary + obligation set | no |
| `F-12` | capability boundary + import set + escalation cost | no |
| `F-13` | boundary + verification obligation | no |
| `F-14` | explicit unsupported + deliverable | no |
| `F-15` | `UNKNOWN` | no |
| `F-16` | carried Unknown | no |
| `F-17` | `Assumed` + named test | no |

No preferred option, no final recommendation, no outcome class, no comparator winner, no fit score, no
architecture branch, no stage order and no exit class appeared in any conclusion. Each unit's §0 and the
directory `README.md` §6 state the prohibition, and three units restate it in-file (`operations/` §19,
`performance/` §7, `economics/` §1).

**DECISION LEAKAGE DETECTED: NO.**

---

## 16. Comparator neutrality

| Check | Question | Result | Evidence |
|---|---|---|---|
| **N1** | Does richer PP domain knowledge become evidence that PP is better? | **NO** | `performance/` §7 in-file: *"A documented boundary here is not evidence that another option class performs better… supports excluding a design, never preferring a class."* Several units carry the same clause |
| **N2** | When a PP mechanism is unsupported, does the reasoner claim another class supports it? | **NO** | `F-01` named three resolutions, one of which is *"the requirement leaves the platform"* — with **no claim** that any named class satisfies offline plus field-level confidentiality |
| **N3** | Does economics domain knowledge infer PP is cheaper? | **NO** | `F-10`: no price exists anywhere in the directory (the §12 rule was verified); the `G-102` comparison is **refused**; no cost claim is `Confirmed` from documentation |
| **N4** | Does an operational burden become automatic PP rejection? | **NO** | `F-11` produced *"technically feasible; not currently operable as drawn"* plus an obligation set. `operations/` §19: *"it does not rank the organisation, and it does not make any other option better."* |

The conflicted-ceiling block (`F-05`) was stated as **symmetric across the platform, cloud-native and hybrid
classes** — the sharpest available neutrality test, and it held.

**COMPARATOR BIAS DETECTED: NO.**

---

## 17. D3 depth

Every major domain was pushed to a concrete technical chain, and depth rose because the fixture required it.

| Domain | Fixture | Chain actually traversed |
|---|---|---|
| **Data** | `F-17` | authority (ERP write path) → Web API write → rule scope and execution plane → contradicted server-side reach → duplicate detection off by default on updates → server-error-class failure defeating naive retry → named bounded test |
| **Automation** | `F-04` | shape (side-effecting single stream) → state location (no rollback; completed actions stay completed) → failure unit (mid-loop unknown prefix) → retry/idempotency (alternate key + upsert, or explicit key check) → ordering (serialising is a one-way change that introduces trigger loss) → measurement/monitoring (throttle rate as a leading indicator; editing resets the counters) |
| **Integration** | `F-05` | ownership → topology → guarantee (conflicted ceiling, no figure) → identity/network → resilience (disablement after sustained breach) → operator (reconciliation owner, trend alerting) |
| **Security** | `F-06` | enforcement plane → grain (per-store authorization) → identity (shared-connection collapse; attribution and throughput collapses) → trust/egress → control obligation (managed class → external entitlement → population → meter) |
| **Governance / ALM** | `F-07`, `F-08` | estate precondition (tenant-owned levers) → environment → lifecycle rung (pipelines need managed targets) → reversibility/deployment consequence (no rollback; restore side effects; enable-before-needed) |
| **Performance** | `F-09` | workload classification → five non-pooling meters → binding boundary (per-identity budget; funnel onto one identity or one row) → proof required (production-like, peak frequency, funnels individually) |
| **Economics** | `F-10`, `F-06` | mechanism → meter → affected population → growth driver → unresolved current entitlement (`G-002`, `VC-05`) and unclosed resale gap (`G-014`, `BS-01`) |
| **Operability** | `F-11` | operator → monitoring → recovery (restore is not a rollback; nine documented breakages) → drill/evidence (timed rehearsal) → commitment (asserted vs evidenced) |
| **Architecture** | `F-12` | composition → property bought (no copy, therefore no synchronization risk register) → exclusion list → irreversibility → imports followed selectively → escalation cost → weak lineage on the write-through variant |
| **Application** | `F-01`, `F-15` | identity class → device/connectivity → offline depth (five levels) → forfeits → the unsatisfiable pair — and, for the agent modality, a hard `UNKNOWN` boundary |

No fixture produced slogan-level output. No fixture was deepened merely because a file existed — `F-16`
deliberately stayed at D1, and that was the correct behaviour.

**D3 MATERIAL DEPTH: PASS.**

---

## 18. Provenance adversarial checks

Gate-side only, against `step-4b-runtime-provenance.md` and `step-4b-number-adjudication.md`. Canonical
research ids were **not** exposed to the simulated reasoner at any point (the runtime carries zero research
ids, by the frozen Step 3 convention).

| Class | Conclusion used at runtime | Authoring-side basis | Verdict |
|---|---|---|---|
| Stable principle | *Limits exclude; they do not prove* (`F-03`, `F-09`) | `A9` §0/§3/§12 · reservation `NB-07` · `AP-D-048`; gap marker `G-063` | supported |
| Volatile reading | Synchronous-response boundary is a family property; ceilings differ by degree (`F-13`) | `A4` `AT2-12`, `AT2-32`; volatile, owner `VS-23` **(stamped)**; gap `G-098` | supported, correctly volatile |
| Limitation | Offline and field-level confidentiality is an unsupported combination (`F-01`) | `A2` `AA-43`, `AA-44` (stable, no volatility owner) | supported |
| Architecture composition | Virtualization exclusion list + irreversibility (`F-12`) | `A12` `AP-06`; `A3` `DA-45`, `VT-04/05/06/09/10/17`; `A5` `IA-34` | supported |
| Weak lineage inside that composition | Write-through virtualization is conditional, `UNKNOWN` performance | `A12` `APR-C-02`, `APR-U-06`; reservation `NB-05`; gap `G-112` | supported **as a preserved reservation** |
| Unknown boundary | Agent surfaces `UNKNOWN` in every class, decision-blocked | Step 3 registers + `A10`; anchors `BS-03`, `VS-20`, `TW-V2`; gap `G-118`; and `A4` `U-14` for `G-119` | supported as an explicit gap |
| Volatile numbers used | `VS-23`, `VS-24`, `VS-07`, `VS-29` readings | `step-4b-number-adjudication.md` rows for each — all `volatile-retain-stamped`, all restored under a named owner | supported |

**Every material rule used in the gate has either an authoring-side canonical basis or an explicit gap
marker. None rested on model knowledge.**

---

## 19. Context-efficiency

| Fixture | RESEARCH units pulled | 2nd pull justified | CRAFT pulled | Volatility register consulted | Blocking entry consulted |
|---|---:|---|---|---|---|
| `F-01` | 2 | yes | no | no | no |
| `F-02` | 2 | yes | no | yes (`VC-07`) | no |
| `F-03` | 1 | n/a | no | no | no |
| `F-04` | 1 | n/a | no | no (readings used in-unit) | no |
| `F-05` | 2 | yes | no | yes (`VC-01` §3, `VS-27`) | yes (`B-08`, `CD-05`) |
| `F-06` | 2 | yes | no | yes (`TW-V3`, `VC-05`) | no (`CD-06` noted as fed, not consulted) |
| `F-07` | 2 | yes | no | yes (`TW-V1`) | no |
| `F-08` | 1 | n/a | no | no | no |
| `F-09` | 2 | yes | no | no | no |
| `F-10` | 1 | n/a | no | yes (`VC-09`) | yes (`BS-01`) |
| `F-11` | 1 | n/a | no | yes (`VS-07`, `VS-17`) | no |
| `F-12` | 1 | n/a | no | no | no |
| `F-13` | 1 | n/a | no | yes (`VS-23`) | no |
| `F-14` | 1 | n/a | no | no | no |
| `F-15` | 1 | n/a | no | yes (`VS-20`, `TW-V2`) | yes (`BS-03`) |
| `F-16` | 1 | n/a | no | no (`VC-10` named, not walked) | no |
| `F-17` | 1 | n/a | no | no | no |

**Gate-level figures**

```text
total RESEARCH-unit pulls                        23
median RESEARCH units pulled per fixture          1
maximum RESEARCH units pulled in one fixture      2
fixtures with one pull only                      11
fixtures with a justified second pull             6
fixtures with unnecessary third-or-more pulls     0
distinct RESEARCH units opened across the gate    9 of 15
CRAFT pulls                                       0
volatility register consulted                     7 of 17 (always via a named row)
blocking entry consulted                          4 of 17 (only where sizing or scope was engaged)
```

**Judgement: selective depth, not context ceremony.** Six of the fifteen RESEARCH units were never opened —
including three of the five `data/` units, which is the correct behaviour for fixtures whose stores were
relational or list-based. No threshold was applied; the observed pattern is that depth rose *inside* one unit
rather than *across* many.

**SYSTEMIC CONTEXT-CEREMONY DETECTED: NO.**

---

## 20. Large-unit observation

Observed, not edited.

| Unit | Lines | Internal structure | Selective reasoning possible? | Finding |
|---|---:|---|---|---|
| `architecture/patterns.md` | 924 | §5 splits into **ten named `###` compositions**, each with an identical nine-part sub-structure (Intent · Prerequisites · Mechanisms composed · Strengths · Weaknesses · Risks · **What it imports** · Escalation consequence · Lineage) | **yes** — `F-12` reached one composition and one pair of import channels | Do **not** split. The `###` headings are the addressing mechanism, and the *What it imports* block bounds the follow-on. No practical context ceremony observed |
| `alm/release-and-lifecycle.md` | 618 | 16 numbered sections plus `###` sub-sections at §8 (`8.1`–`8.4`), precisely where the reversibility question splits | **yes** — `F-08` used §8.1 and §8.3 and never opened §5–§7 | Do not split |
| `operations/operability-and-support.md` | 586 | 19 numbered sections; the four §0 questions map to §4, §3, §9 and §5/§6 respectively | **yes** — `F-11` used §8, §9, §13; `F-14` used §13 alone | Do not split |

One bounded, **non-blocking** authoring observation for the record (no edit made, no repair required): in
`architecture/patterns.md` the composition headings sit at `###` under a single `## 5.`, so a heading-only
scan shows ten peers without each composition's subject boundary being visible at `##` level. Navigation
still worked in `F-12` because §0's questions name the composition *property* rather than the composition
name. **Recorded as an observation, not a finding.**

---

## 21. Failures and classification

```text
fixtures planned    17
fixtures executed   17
fixture failures     0
```

No failure in any of the seven classes:

| Class | Description | Occurrences |
|---|---|---:|
| **A** | knowledge authoring defect (canonical support exists, runtime unit omitted or misstated it) | 0 |
| **B** | taxonomy / discoverability defect | 0 |
| **C** | volatility-ownership defect | 0 |
| **D** | research gap behaving incorrectly | 0 |
| **E** | decision leakage | 0 |
| **F** | comparator bias | 0 |
| **G** | context-efficiency defect | 0 |

No repair was performed, and none is required. The single §20 observation is explicitly **not** a class-B
defect: the correct first pull was reached in 17 of 17 fixtures.

---

## 22. Final verdict

**Step 4C passes.** Against the PASS criteria:

| Criterion | Result |
|---|---|
| Every planned fixture executed | 17 / 17 |
| First-pull discoverability reliable | yes, 17 / 17, no router reconstructed |
| Second pulls selective | 6 justified, 0 unjustified, 0 third-plus |
| Stable principles usable without volatility handling | 7 / 7 |
| Volatile readings trigger correct freshness behaviour | yes; the one decision-changing reading was held open |
| Conflicted evidence remains unresolved | yes, symmetrically, `DECISION BLOCKED` preserved |
| All five gap closure classes behave correctly | yes, and the action differed by class |
| `G-001` empirical-test behaviour | PASS |
| `G-118` / `G-119` agent gap | PASS (mandatory) |
| Measurement obligations emitted where appropriate | 4 / 4, with fidelity conditions |
| CRAFT does not become platform authority | 0 CRAFT pulls; 4 temptations declined |
| Domain knowledge does not select options | 0 selection verdicts in 17 fixtures |
| No comparator bias | N1–N4 all NO |
| No unsupported claim invented | 0 |
| D3 depth materially sufficient | yes, across all major domains |
| No systemic context-loading problem | median 1 pull, max 2 |

Runtime files under `library/` were **not modified**. No new research was performed. No web access. No
canonical research was touched. No Step 3 decision semantics and no Step 5 artefact were changed —
`architecture/patterns.md` deepened composition reasoning in `F-12` without rendering a blueprint and
without assuming `architecture-templates/<branch>.md` is already valid; `Q4-08` remains Step 5 work.

---

## 23. Recommendation

**Freeze Step 4 — Domain Knowledge.** No bounded repair is warranted: the layer's behaviour under material
decision pressure is correct on every mandatory dimension, and the only observation raised (§20, heading
depth in `architecture/patterns.md`) is cosmetic, non-blocking, and did not degrade retrieval in the one
fixture that exercised that file.

Two items carried forward as **Step 5 / commission inputs**, not as Step 4 defects:

1. `G-118` / `G-119` remain the one **dedicated** research-commission candidate — material, recurring,
   growing in stakeholder salience, and not closable by engagement measurement.
2. The fourteen priority knowledge gaps stay open with their differentiated closure mechanisms; only the
   `commission`-classified subset is a candidate for a commissioned extension of the canonical baseline.

---

## 24. Freeze marker (documentation only — appended 2026-09-04, Step 5A)

The metrics below are the report's own final gate result, restated verbatim as the freeze record. No
runtime file was modified, no fixture was re-run and no research was performed to produce this section.

```text
STEP 4C — DOMAIN KNOWLEDGE SEMANTIC/PULL GATE: PASS
SEMANTIC FIXTURES EXECUTED: 17
FIXTURE FAILURES: 0
FIRST-PULL DISCOVERABILITY: PASS
SELECTIVE SECOND-PULL BEHAVIOUR: PASS
KNOWN + STABLE BEHAVIOUR: PASS
KNOWN + VOLATILE BEHAVIOUR: PASS
UNKNOWN / GAP BEHAVIOUR: PASS
CONFLICTED FACT HANDLING: PASS
G-001 EMPIRICAL-TEST BEHAVIOUR: PASS
AGENT GAP G-118/G-119: PASS
MEASUREMENT OBLIGATION BEHAVIOUR: PASS
CRAFT BOUNDARY: PASS
DECISION LEAKAGE DETECTED: NO
COMPARATOR BIAS DETECTED: NO
UNSUPPORTED CLAIMS INVENTED: 0
D3 MATERIAL DEPTH: PASS
MEDIAN RESEARCH UNITS PULLED PER FIXTURE: 1
MAX RESEARCH UNITS PULLED IN ONE FIXTURE: 2
UNNECESSARY THIRD-PLUS PULLS: 0
SYSTEMIC CONTEXT-CEREMONY DETECTED: NO
RUNTIME MODIFIED DURING INITIAL GATE: NO
NEW RESEARCH PERFORMED: NO
DOMAIN KNOWLEDGE DEFENSIBLE: YES
READY TO FREEZE STEP 4 — DOMAIN KNOWLEDGE: YES
```

**STEP 4 — DOMAIN KNOWLEDGE: FROZEN**
