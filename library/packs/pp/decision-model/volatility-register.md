# Volatility Register — facts with a shelf life

<!--
provenance: RUNTIME (decision-model register) · consulted ON DEMAND from any stage of decision-tree.md
authored: 2026-09-04 (Step 3B1) · design authority: Step 3A — Options Decision Model
amended: 2026-09-04 (Step 4B pre-4C bounded repair) — §2A adds 19 volatility-OWNERSHIP family rows
and splits VS-04; seven existing rows had their scope clarified. No stage, concern, blocking entry,
option class, outcome, composed row or comparator semantic was changed. The register still supplies
no figures (§5).
NOT loaded at the start of Options and NEVER read as a standing checklist. Consulted only where an
active decision question depends on a volatile fact or a dated tripwire (decision-tree.md §11).
-->

## 0. The rule this register serves

```text
stable decision principle   →  decision logic   (decision-tree.md)
volatile platform fact      →  evidence         (domain knowledge + the engagement's own row)
```

**A published figure is exclusion evidence with a shelf life, never a permanent decision rule.**

1. The spine encodes the **question and the boundary shape** — *"is the required freshness below the
   documented external-site floor?"* — **never the number**.
2. Where the number must appear, because the engagement has to test a real requirement against it, it is
   **re-read from current documentation at the decision date** and the reading is recorded **with its
   date** on the engagement's own row (`verificado_em` + `validade`), not baked into the pack.
3. **No published figure is a state name.** Revalidating a limit changes one sentence, not a taxonomy.
4. **Verification obligation.** Where a volatile fact is **decision-critical** and sufficiently current
   evidence is unavailable: open an `Unknown` (`custo: documento|spike`, `swing: decisivo`) whose `quem responde`
   carries the role that owes it or the source to consult (`role:` / `fonte:`, never a person), and
   the date, and **do not treat the affected conclusion as settled**. Where the fact is in
   `blocking-set.md`, the terminal is *decision blocked*.

**How to use this file.** You have a live decision question; you have found that it turns on a figure.
Look the figure's class up here, read its re-verification trigger, do that, and record the reading on the
engagement's row. **Do not walk the register.**

---

## 1. Commercial and licensing volatility — 10 entries

Date-sensitive on their **commercial** dimension. Verification is required at decision, implementation
and renewal time; canonicalisation does not freeze these.

| # | What is volatile | Why it moves | Re-verify at |
|---:|---|---|---|
| **VC-01** | Per-mechanism throughput ceiling | **Live conflict — see §3.** Connector counts are also licence-conditional | **Every engagement, before sizing** |
| **VC-02** | Event frequency floor and trigger freshness | Per-licence polling intervals are an open unknown in three areas of the pack's evidence; one source's figures may be stale | Every engagement, **per connector** |
| **VC-03** | Connector and service permissibility posture | New connectors are added to the default group over time. **A policy check is valid on its date only** | Before design commitment, **per environment** |
| **VC-04** | Request rate per acting identity | Published figures are **transition-period tolerances with no announced enforcement date**; the concurrency default may be higher per environment | Design time, **and on any enforcement announcement** |
| **VC-05** | Entitlement fit of the required capability set, **including licence-conditional artefact counts (e.g. custom-connector count per plan)** | The general documentation is **not authoritative** on licensing; prices are labelled illustrative; whether one premium capability obliges premium entitlement for **every** user of an artefact is an open item | Options, implementation **and renewal** |
| **VC-06** | Audience and frequency shape, **including per-environment entitlement minimums and any preview billing cap** | Several meters are preview; metering units (browser cookie, contact record) have documented **over-count** behaviour | Options and renewal |
| **VC-07** | Capacity consumption profile, **including the per-environment storage floor, the team-scoped combined ceiling and the capped free tier** | Add-on assignability was constrained during the transition period; the analytical-replication storage ratio is unpublished | Design time, and annually |
| **VC-08** | External and hybrid service consumption cost | Cloud pricing and tier capabilities change; **gateway-at-scale cost is an open item** | Options and renewal |
| **VC-09** | Multi-tenancy and resale requirement | Resale and multi-tenant licensing is an **unclosed gap** in the pack's evidence. Scope-blocker `BS-01` | Before any resale commitment |
| **VC-10** | Roadmap and preview dependency, **including interface-definition version support and governance-tooling availability states** | Preview and general-availability states change; **two facts in this pack's own evidence already changed once during its life**. Scope-blocker `BS-02` | Every engagement, **and before encoding anything** |

---

## 2. Service-limit, quota and feature-state volatility — 20 entries

These rows carry a **published service limit, quota, retention window or feature state**. They were
previously treated as timeless, which is how a decision rule acquires a dated number.

| # | What carries the figure | Re-verify at |
|---:|---|---|
| **VS-01** | External-site cache floor and the surrounding freshness window | Options, and **before any freshness commitment** |
| **VS-02** | Delegation ceilings (default and maximum) | Design time, **per data source** |
| **VS-03** | Content-throughput-per-24-hours meter, by owner profile | Design time, and on any licence change |
| **VS-04** | List-store **view/query** threshold — the access-path boundary. *Authorization scope moved to `VS-29`* | Design time, **per access path** |
| **VS-05** | Audit retention and log-availability windows, **including the latency before an audit or compliance event becomes visible** | Options, and at any compliance review |
| **VS-06** | Aggregation ceiling and the analytical-replication refresh window, **including the scheduled-replication floors (minimum increment, refreshes per period, maximum run)** | Design time, **before any reporting commitment** |
| **VS-07** | Backup retention windows by environment class | Options and renewal |
| **VS-08** | Per-mechanism ceilings — *also `VC-01`; **conflicted**, §3* | **Every engagement, before sizing** |
| **VS-09** | The over-limit disablement countdown | Design time |
| **VS-10** | Payload ceilings by mechanism | Design time, **per stream** |
| **VS-11** | Gateway host minimum and network preconditions | Design time, **before any network commitment**. Note the preconditions are **irreversible** |
| **VS-12** | Run-duration ceiling used as a work-shape boundary | Options |
| **VS-13** | Run-duration ceiling and the trigger-inactivity window | Options, **before any long-running design** |
| **VS-14** | Trigger polling intervals — *also `VC-02`* | Every engagement, per connector |
| **VS-15** | The human-decision window used as the in-platform boundary | Options |
| **VS-16** | Interface-automation throughput and payload figures | Design time |
| **VS-17** | Backup and restore windows underpinning the recovery objective, **including restore duration behaviour and the free-capacity precondition without which restore is blocked** | Options, **and before any recovery commitment** |
| **VS-18** | Native telemetry retention window | Options, **and before any observability commitment** |
| **VS-19** | Native audit/diagnostic retention window | Options, and at any compliance review |
| **VS-20** | Agent surface: request bucket, a bundled credit entitlement **with a dated removal**, and preview feature states — *also `VC-10`; scope-blocker `BS-03`* | **Every engagement** |

---

## 2A. Ownership amendment — 19 family rows (Step 4B pre-4C bounded repair, 2026-09-04)

Step 4B found **~60 decision-relevant quantitative subjects with canonical support but no owning row**.
That was a **volatility-ownership gap, not a research gap**: the knowledge existed and the figure had to be
dropped only because §5.2's third condition (*a figure must name the row that owns its re-verify trigger*)
could not be met. These rows close it.

**Nothing in this amendment changes a decision semantic.** No stage, concern, blocking entry, option
class, outcome, composed row or comparator rule is touched. The amendment adds **ownership of
re-verification** and nothing else — these rows still supply no figures (§5).

**Grouping rule applied.** A row owns a **coherent family** of readings that share a factual subject, a
volatility mechanism, a re-verification trigger **and** a decision consequence. Where any of those four
diverged, the family was split rather than widened — which is why V1 became two rows, V3 became three, and
`VS-04` was split. **No row groups unrelated facts merely because both are limits.**

| # | What carries the figure — the coherent family | Why these belong together | Re-verify at |
|---:|---|---|---|
| **VS-21** | **Control propagation and enforcement latency** — the delay between an administrative control change and the control actually binding: data-policy enforcement, tenant-isolation propagation, sharing-limit enforcement, environment-group rule application, connector-permissibility posture propagation | One subject (*when does a configured control start enforcing*), one mechanism (asynchronous propagation across the control plane), one consequence (a window in which the control is **not** enforced, and a retrofit can present as an outage) | **Before relying on any control as enforced**, and after any policy change |
| **VS-22** | **Credential and session revocation window** — how long an already-issued credential or session keeps working after access is removed, and what shortens it | Distinct from `VS-21`: the mechanism is credential lifetime, not propagation, and the consequence is *a removed user still has access* | Before any revocation or joiner-mover-leaver commitment |
| **VS-23** | **Synchronous response windows per mechanism, and the asynchronous window that replaces them** — the inbound and outbound synchronous ceilings, the application-surface request timeout, the in-transaction extension compute ceiling, and the long asynchronous outbound window | One decision (*can this be synchronous at all, and if not what is the shape*). Every member is a wait a caller experiences; the asynchronous window is the same decision's other half | Design time, **before any synchronous commitment** |
| **VS-24** | **Orchestration definition structural ceilings** — action count, nesting depth, array items per iteration construct, switch/case count, variable count | One subject (the size and shape of one orchestration definition), one consequence (**decomposition**, not relocation — the ceilings are identical across the comparable products, which is the correction this row exists to keep testable) | Design time, and at any definition-size review |
| **VS-25** | **Application-artefact composition ceilings** — pages per application, connectors and connection references per application, guided-stage caps, embedded-report row ceiling, branded-wrapper bundle size, external-site structural thresholds (file, lookup-record and role cardinality), per-user artefact ceiling | One subject (how much can be composed into one application artefact), one consequence (split the artefact or change surface). Deliberately **not** merged with `VS-24`: a different service family with a different remedy | Design time, per surface |
| **VS-26** | **Release-artefact packaging ceilings** — solution size ceiling, environment-variable value length | One subject (what may travel inside a release artefact), one consequence (the content must travel outside the solution). Distinct mechanism from `VS-24`/`VS-25`: ALM packaging | Before a release design |
| **VS-27** | **Connector and integration execution envelope** — per-connection call rate and concurrency, per-user application call rate, action timeout and the layered client request timeout, the inbound runtime-endpoint concurrency ceiling, and the narrow retry semantics of the outbound notification mechanism. **Excludes the conflicted custom-connector throughput ceiling — that stays `VC-01`/`VS-08` and stays conflicted** | One subject (what an integration path allows per connection, per identity, per window), one consequence (the connection becomes a capacity-planning object and is normally the binding meter) | Design time, **per connector and per connection topology** |
| **VS-28** | **Customer-operated integration estate currency obligations** — the supported-release window for self-hosted components, and any allowlist or service-tag refresh cycle | One subject (how often the customer-operated estate must be refreshed to stay supported), one consequence (a standing **operating obligation**, not a design ceiling) — which is why it is not folded into `VS-27` | At operating-model design, and continuously thereafter |
| **VS-29** | **List-store unique-permission scope ceiling** — the supported and recommended counts of uniquely-permissioned scopes, and the item count above which inheritance can no longer be broken. *Split from `VS-04`* | A **row-authorization granularity** boundary. `VS-04` is an **access-path** boundary. Same store, different fact, different decision — they must not share an owner | Design time, **before any per-record authorization commitment** |
| **VS-30** | **Governed-store schema-object budgets** — alternate keys per table and their column and width bounds, derived-column counts per table and per environment, table-scoped rule counts, row-byte budget, and the text length above which a column cannot be indexed | One subject (how many of this schema object may a table or environment carry), one mechanism (metadata budget), one consequence (the model fits the budget or is restructured) | Design time |
| **VS-31** | **Search budget and index freshness** — the organisation-wide searchable-field budget and its per-type weighting, the per-identity search rate, index synchronisation lag, and the permanence window on index removal | One subject (the searchable surface as a finite, billed, eventually-consistent resource), one consequence (search scope is designed and budgeted, and removal is not a cheap remedy) | Design time, and before any search commitment |
| **VS-32** | **Horizontally-scaling (elastic) table bounds and maturity state** — the size bound per logical partition, and the support and general-availability state. *The maturity state is contradicted in the baseline; this row owns the re-verification, never a settled answer* | One subject (whether the high-volume table type is available and what it bounds), one consequence (whether the high-ingest option exists at all) | **Every engagement that considers it** |
| **VS-33** | **Query traversal and projection bounds** — lookup-traversal depth in one expression and its stricter offline variant, expandable entities per query, and the join-type column ceiling per view | One subject (how much relational traversal one query or view may express), one consequence (denormalise, or move the mashup server-side — a data-model change). Distinct from `VS-02`, which owns delegation | Design time, **per access path** |
| **VS-34** | **External relational store tier envelope** — the sustained log-rate ceiling and its independence from compute size, per-tier storage ceilings, and concurrent session and worker counts | One subject (what the external relational tier sustains), one consequence (the sustained-write ceiling, which is not raised by buying compute) | Before sizing, and at any tier change |
| **VS-35** | **Customer-managed-key operational windows** — the window to denial after key removal, the window to an inaccessible state, the absence of automatic healing past it, previous-key-version retention, and per-vault association ceilings | One subject (the availability consequences of customer key custody), one consequence (a tier-0 dependency with a documented cliff) | Before any key-control commitment |
| **VS-36** | **Support plan structure and coverage** — severity response windows, the per-case effort cap, and covered hours | One subject (what the vendor's support actually commits to), one consequence (what the organisation must staff itself). No existing row owned this; `VC-08` owns support **cost**, not structure | Options, and at renewal |
| **VS-37** | **Cross-region protection envelope** — recovery-point and recovery-time objectives, enablement lead time, and the throughput it degrades | One subject (the cross-region option), one consequence (whether the objective is achievable and what it costs). Distinct mechanism from `VS-07`/`VS-17`, which own **backup** windows | **Before any disaster-recovery commitment** |
| **VS-38** | **Offline cache bounds** — the offline record-set ceiling and the local file-cache envelope | One subject (how much can be carried offline), one consequence (the offline depth achievable, and therefore the surface) | Design time, **before any offline commitment** |
| **VS-39** | **Profile-derived execution defaults** — retry depth and postpone behaviour that follow the owning identity's performance profile | One subject (execution behaviour inherited from the licence rather than designed), one consequence (**resilience is a property of the owner, not of the definition** — the same artefact behaves differently under a different owner). Deliberately not merged with `VS-03`, which owns a byte meter: same mechanism, unrelated facts | Design time, **and on any change of owning identity** |

### 2A.1 What this amendment deliberately did not do

- **It did not create one row per number.** ~60 subjects are owned by 19 rows plus scope clarifications on
  seven existing rows.
- **It did not widen a row to absorb unrelated facts.** Splitting `VS-04` is the precedent, and the same
  test was applied to every candidate family: V1 → two rows (propagation ≠ credential lifetime), V3 →
  three rows (orchestration ≠ application artefact ≠ release artefact), and `VS-39` was kept out of
  `VS-03` for exactly that reason.
- **It did not resolve any conflict.** `VC-01`/`VS-08` remains conflicted and is explicitly excluded from
  `VS-27`. `VS-32` owns the re-verification of a contradicted maturity state and supplies no answer.
- **It did not supply figures.** §5 stands unchanged: this register names what is volatile and when to
  re-read it. The reading is taken at the decision date and recorded on the engagement's row.
- **It added no research.** Every family here has canonical support; what was missing was ownership.

### 2A.2 Subjects deliberately left without a figure in runtime

Adjudicated and **not** given an owning row, because the boundary *shape* answers the decision and the
number would not improve it: derived-computation recurrence floor · per-list item ceiling · governance
recommendation cadence and warm-up · developer-environment disuse window · environment-variable
propagation window · capacity notification threshold · the monitoring metric's reported percentile ·
service-update station count · trial-environment lifetime · storage-rate and run-cost ratios (also
price-adjacent) · bundled credit quantity (also price-adjacent) · cascading-retry arithmetic ·
store asynchronous-request retry count · notification milestones preceding a dated tripwire.

Two subjects are **measurement-owned** rather than register-owned, because no published figure would
settle the engagement's requirement: the per-identity service-protection triple, whose effective value
depends on an undisclosed licence-dependent multiplier; and any concurrent-user figure, for which none is
published anywhere.
---

## 3. The live conflict

> **The per-mechanism throughput ceiling for the main extensibility mechanism is `CONFLICTED`.**

Two currently-maintained vendor pages disagree by **20×** on the ceiling. The conflict was re-verified
and remains open. This fact is in the blocking set (`B-08`).

**Consequence, and it is symmetric.** Any option whose **sizing or economics** rests on a high-frequency
custom connector is **decision-blocked until measured**. This cuts across the platform, the cloud-native
classes and the hybrid class **equally** — it is **not** a penalty against this platform.

**What closes it:** re-read **both** current sources at the decision date **and** measure representative
workload. **Encode neither figure.** A documented case-by-case escalation path exists and may be
*proposed as a mitigation*; it may never be *relied on in advance*.

Composed row `CD-05` is the registered form of this combination.

---

## 4. Dated tripwires

These are **dated commitments**, not rules. They feed `/decide`'s revision conditions and `/revisit`;
they are the mechanism by which a decision made today knows when to re-examine itself.

| # | Date | Commitment | What it changes | On firing |
|---|---|---|---|---|
| **TW-V1** | **February 2026** *(already past — verify the outcome)* | Automatic conversion of deployment-pipeline target environments to managed environments | Adopting in-product ALM becomes a **tenant licence decision**. Whether the conversion completed as announced, and what it did to tenants that had not planned for the licence impact, is an **open question in the pack's evidence** | Confirm the current default with the platform-owning team **before** costing an in-product ALM path |
| **TW-V2** | **1 November 2026** | Retirement of the bundled AI Builder credit entitlement | Any option economics resting on the bundled credits loses its basis. Per-operation consumption is **complexity-dependent and unpublished** | Re-price on the consumption meter; establish consumption **empirically in a bounded pilot**, then size for the peak month |
| **TW-V3** | **February 2027** | Managed-environment licence enforcement — users without an appropriate licence are **blocked from opening apps** in a managed environment | Nearly every preventive governance control requires a managed environment, and every **active user** of that environment then requires a premium licence — **including users of standard apps**. Governance capability acquires a hard, quantifiable price | Re-price the whole environment population, not the app's own users. Where the control is **mandated** and the population is unfunded, this is *economically infeasible*, not a trade-off (composed row `CD-03`) |

**Recording a tripwire.** When an option's viability or economics rests on one of these, state it in the
option's assessment as a dated assumption with `verificado_em` + `validade`, and carry it into `/decide`
as a **revision condition**. `/revisit` then compares the present against the frozen counterfactual when
it fires.

---

## 5. What this register does *not* do

- **It does not supply figures.** It names what is volatile and when to re-read it. The number is read
  from current documentation on the decision date and recorded on the engagement's row.
- **It is not a checklist.** Walking all thirty entries in every engagement is the failure mode this
  file's loading rule exists to prevent.
- **It does not create exclusions.** A volatile fact with no current reading produces a **verification
  obligation**, never a settled exclusion (`decision-tree.md` §4).
