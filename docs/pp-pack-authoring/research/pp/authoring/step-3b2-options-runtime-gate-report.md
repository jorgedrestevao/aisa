# Step 3B2 — Options Runtime Behaviour Gate

<!--
provenance: AUTHORING GATE (never loads at runtime)
executed: 2026-09-04 · gate type: SEMANTIC RUNTIME GATE (behaviour, not structure)
runtime under test: the exact Step 3B1 artefacts, unmodified during the replay.
-->

## 1. Gate basis

**What was executed.** Every canonical Block D scenario `T-01`…`T-18` was replayed conceptually
against the authored Options runtime: scenario evidence → S0–S9 as applicable → serious option set →
material concern evaluation → disqualifier / precondition / risk / uncertainty → outcome. A scenario
passes only where the runtime reaches the canonical result **for the canonical reason**.

**Runtime under test (7 files, read-only).**

```text
library/packs/pp/decision-tree.md                              (436 lines — the spine)
library/packs/pp/decision-model/alternatives-register.md        (S1)
library/packs/pp/decision-model/blocking-set.md                 (S3)
library/packs/pp/decision-model/composed-disqualifiers.md       (S6)
library/packs/pp/decision-model/outcome-classes.md              (S9)
library/packs/pp/decision-model/volatility-register.md          (on demand)
library/packs/pp/pack.yaml                                      (decision_model + constraints_to_check)
```

**Expectation authority (read, not reopened).**

- `decision-intelligence-matrix.md` §6 — the `T-01`…`T-18` bodies, used as **frozen fixtures**.
- `decision-intelligence-matrix.md` §3 — the twelve registered composed rows and their class mapping.
- `step-3a-options-decision-model.md` §20 — the 16 regression scenarios, the 18-row canonical id audit,
  the four G5 carry-forwards.
- `step-3b1-options-runtime-implementation-report.md` §13 (seven deviations) and §14 (gate inputs).

**Mapping used.** Runtime local anchors ↔ canonical objects, verified 1:1 before the replay:
`CD-01…CD-12` ↔ matrix §3 rows 1–12 (same conditions, same consequence, same class) · outcome classes
**1–14** identical to `decision-criteria.md` §6.2 · exit scopes `Xp`/`Xr`/`Xe`/`Xc` and the two
non-exit consequences `Ri`/`Cf` identical · `ALT-001…011` identical · `B-01…28` + `BS-01…03` are the
canonical blocking set carried as pack-authored patterns.

**No runtime file was opened for writing at any point.** All eighteen scenarios were replayed before any
finding was recorded.

---

## 2. `T-01`…`T-18` replay

Legend — **Grade**: evidence grade of the decisive fact. **Scope**: whole solution `[W]` · named
responsibility `[R]` · economic `[E]` · sponsor-side `[S]`. Outcome numbers are internal bookkeeping and
are never rendered to an engagement (spine §14.3).

### T-01 — Simple departmental internal app

| | |
|---|---|
| **Decisive evidence** | 12 people, one team; no integration; no external users; no regulatory regime; low volume; tolerant process; value marginal but positive; inside existing entitlement |
| **S1 candidates** | Trigger row 1 *capability already exists in the estate* → `ALT-001`, `ALT-003`, `ALT-007`, `ALT-011`; mandatory `ALT-002`, `ALT-010`. `ALT-004` enters only where a requirement triggers it — none of rows 5/6/7 fires on this shape |
| **Stages exercised** | S0 (D2 — value marginal but positive; the *does this need to exist* question is raised, not assumed) · S1 · S2 (no absolute) · S5 (mostly D0/D1) · S6 (no row's first condition holds) · S7 (no external component) · S8 (seeded entitlement; `ALT-002`/`ALT-010` priced on the same ten dimensions) · S9 |
| **Decisive concern** | C1 (existing capability) — the shape matches a documented sufficiency |
| **Grade** | `Confirmed` on the shape facts; seeded entitlement `Confirmed` |
| **Blocker** | none. `B-17` is **not engaged**: no pattern requires an external component, so `CD-02` cannot fire and the absence is not decision-changing |
| **Disqualifier** | none of any scope |
| **Composed** | none |
| **Outcome** | **13 form (a)** — *"no documented constraint excludes the platform; the collaboration capability is the documented answer for this shape, lighter on the seeded-entitlement fact alone; graduation trigger: `<team scope / population growth>`"*. Stands alone, **not** followed by class 8. Class **1** is the alternative canonical branch, reachable where a requirement triggers `ALT-004` |
| **Comparator** | no comparative claim; the *lighter* clause is scoped to the entitlement fact only (form (a)'s narrow licence) |
| **Verdict** | **PASS** — canonical allows class 1 **or** class 13; the runtime lands on the branch the canonical repair note endorses, with the mandatory graduation trigger |

**Depth exemplars carried from this scenario.** Legitimate **D0**: C5 integration — *"no integration in
scope"* is affirmative engagement evidence, not silence. **Evidence gap ≠ D0**: C3's offline dimension —
equipment inspection could plausibly be walked; the scenario says nothing → **D1 + `Unknown`**,
`swing: dimensionante`, carried, **not** blocking.

---

### T-02 — Excel replacement

| | |
|---|---|
| **Decisive evidence** | 6 writers; ~40,000 rows growing; several lookups; monthly reporting; occasional concurrent edits; two managers-only fields |
| **S1 candidates** | Row 5 *relational + row/column security + audit, internal audience* → `ALT-004`; row 1 → `ALT-001`, `ALT-003`, `ALT-007`, `ALT-011`; row 12 *bulk / analytics* → `ALT-006`, `ALT-007`, `ALT-009` for the reporting leg; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 (no absolute) · S5 (**widest**, D2 on C4/C9/C11) · S6 (none) · S7 (trivial) · S8 (entitlement) · S9 |
| **Decisive concern** | C4 — non-delegable path past the client ceiling; routine contention; field-level visibility |
| **Grade** | `Confirmed` (row count, writers, field visibility) |
| **Disqualifier** | **none.** Routine contention is `Ri` — an **in-platform store change** to the governed relational store. Field visibility is `FIELD`, satisfied in-platform (no administrator exclusion → no `Xr`). The volume `Xr` is inert because server-side shaping exists |
| **Composed** | none |
| **Outcome** | **2 — FIT WITH CONSTRAINTS.** Conditions: governed relational store with an explicit concurrency design · premium entitlement priced (owner, funded, by when) · analytical path for the monthly reporting |
| **Comparator** | `ALT-003` is **eliminated by its own evidence** (no column security, no conflict control) and appears in the comparison with that finding — elimination is a finding, not a deletion |
| **Verdict** | **PASS** — and this is the scenario proving `Ri` never renders as *excluded for this responsibility*, the V1 defect the canonical repair exists for |

---

### T-03 — Business-critical internal app

| | |
|---|---|
| **Decisive evidence** | 400 users; drives production decisions; 4 h downtime materially costly; integrates with the resource-planning system; five-year life |
| **S1 candidates** | Row 1 / row 15 / row 16 → `ALT-001`, `ALT-007`; row 5 → `ALT-004`; hybrid `ALT-009`; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 · **S3 (terminal for this round)** · S6 (`CD-04`, `CD-09` tested) · re-entry after resolution |
| **Decisive concern** | C5 (integration ownership) + C9/C10 (recovery, composite availability, maturity) |
| **Grade** | `Unknown` on `B-06`, `B-22`, `B-25`, `B-26` — all `swing: decisivo` by construction |
| **Blocker** | **yes** — `B-06` integration ownership · `B-22` end-to-end availability of the composed flow · `B-25` RPO/RTO **plus a timed drill** |
| **Composed** | **`CD-04`** engaged (business-critical + no representative managed test environment + no drill) → **class 12, never an exclusion** — the drill *is* the evidence task. **`CD-09`** is *undetermined rather than refused* → its class-12 branch, **never a platform exclusion** |
| **Outcome** | **12 — DECISION BLOCKED**, per-resolution outcomes mandatory: *incumbent owns the integration with a published contract* → **4 — hybrid with the incumbent**, `INCUMBENT FIT UNEVALUATED`; *unowned* → the integration responsibility is in scope and priced → **2** with the managed-environment chain (observability, backup, pipelines) priced into the option |
| **Comparator** | `INCUMBENT FIT UNEVALUATED` on the `ALT-007` branch |
| **Verdict** | **PASS** |

---

### T-04 — External customer portal *(evidence-grade regression)*

| | |
|---|---|
| **Decisive evidence** | 200,000 policyholders; self-registration; claim documents; **expected** sub-minute freshness after a back-office write |
| **S1 candidates** | `ALT-004` (external-site surface), `ALT-005` (row 18 — product-grade external surface), `ALT-011` (row 26 — standardised domain); mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 (identity class, sensitivity) · **S3 (terminal first)** · S5 D3 on C3/C9 · S9 |
| **Decisive concern** | C3 / C9 — freshness at the read surface against the documented external-site cache floor |
| **Grade** | the sub-minute figure is **`Assumed` and decision-changing** (it flips the outcome between class 2 and class 6). Spine §4 forbids settling a hard exclusion on it |
| **Blocker** | **yes** — provisional disqualifier + evidence obligation; `Unknown`, `swing: decisivo`; volatility `VS-01` requires the floor to be **re-read at the decision date** and recorded with `verificado_em`/`validade` |
| **Sequence** | `uncertain decisive evidence → 12 → evidence resolved → settled outcome`. Never `assumption → settled exclusion` |
| **Outcome** | **12** → on resolution: 15-minute freshness acceptable → **2**; sub-minute confirmed real → **6 — excluded for the named responsibility** (the external-site read surface, `Xr`) → **8** naming `ALT-005`, `ALT-011` |
| **Scope pair** | the platform **remains** a candidate for the authenticated document access behind the read surface — the exclusion does not travel beyond the named responsibility |
| **Comparator** | `COMPARATOR EVIDENCE ABSENT` inside the outcome string: no latency or throughput measurement exists for **any** technology, so the replacement's adequacy is unevidenced |
| **Verdict** | **PASS** |

---

### T-05 — High-volume integration *(volatility + operability)*

| | |
|---|---|
| **Decisive evidence** | 900,000 records; ~4,000/min intraday peak; ordering within a product family; duplicates unacceptable |
| **S1 candidates** | Row 9 (delivery guarantee / ordering) → `ALT-006`, `ALT-009`; row 11 (sustained throughput, no partitioning) → `ALT-006`, `ALT-009`; row 12 → `+ALT-007`; row 7 → `ALT-004`; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 · S3 · S5 (envelope: limits **exclude designs, never prove performance**) · **S6 (`CD-05`)** · **S7 (the gate is the pivot)** · S8 · S9 |
| **Decisive concern** | C5 + C9 — per-mechanism ceiling, delivery guarantee, sustained throughput |
| **Grade** | peak figure `Confirmed` (engagement measurement). **`B-08` per-mechanism ceiling is `Conflicted` — the live 20× vendor conflict** |
| **Blocker** | **yes where a custom connector is on the path** — `B-08`; volatility `VC-01`/`VS-08` §3 |
| **Composed** | **`CD-05`** — high-frequency custom-connector workload + sizing on either side of the open conflict, unmeasured → **12**, naming *both* the re-read and the measurement. Explicitly **symmetric** across `ALT-004`, `ALT-006`, `ALT-009` — not a penalty against the platform |
| **Outcome** | gates satisfied → **3 — hybrid with cloud-native services** (a broker carries ordering and de-duplication; a bulk mechanism carries volume; the platform orchestrates and holds the business record). **Operator gate fails** → the hybrid is **unavailable, not worse** → the responsibility stays in-platform: **2**, condition *"single platform plus a tripwire, not a paper hybrid"*, with the metric that would force the move recorded. Neither acceptable → **6 → 8** to `ALT-007` |
| **Comparator** | `COMPARATOR EVIDENCE ABSENT`; the register's symmetric unknown *capacity envelopes for two of the three broker services were never established* is carried onto `ALT-006`/`ALT-009` |
| **Verdict** | **PASS** — the canonical class 3 / class 2 branch pair is reproduced exactly, including the tripwire wording as a **condition**, never a class |

---

### T-06 — Complex data-centric enterprise application *(scope-pair regression)*

| | |
|---|---|
| **Decisive evidence** | 12,000 contracts, 40 related entities; clause-level history; row **and** field security by business unit and deal team; seven-year retention; board-level reporting; signature + finance integrations |
| **S1 candidates** | Row 5 → `ALT-004`; row 26 → `ALT-011` (CLM products exist — a mandatory buy-check, not a preference); row 12 → `ALT-006`/`ALT-007`/`ALT-009` for the analytical leg; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 · S4 (source of record per entity and field — `B-04`) · S5 D3 on C4/C6/C7 · S6 · S7 (gates for the analytical component) · S8 · S9 |
| **Decisive concern** | C4 (authority, granularity, retention) + C9/C11 (analytics, audit capacity) |
| **Grade** | `Confirmed` on the shape; **administrator exclusion is `Unknown`** — it is *not* asserted, so no `Xr` is settled on it |
| **Disqualifier** | deep traversal is **`Ri`** (server-side views / flattened model / a different surface) — never an exclusion. Analytics and multi-year queryable retention are **`Xr` at named responsibilities** |
| **Composed** | none fires (`CD-01` needs multiple transactional owners with no compensation window — resolved by the ownership matrix; `CD-08` needs replication with no reconciliation owner) |
| **Outcome — two pairs, uncollapsed** | *(application scope)* → **2 — FIT WITH CONSTRAINTS**: security and ownership model designed **before the first table** (ownership type is immutable); mandatory `ALT-011` buy-check first. *(analytical / board-reporting responsibility)* → **3 — hybrid with cloud-native services**, with the five S7 gates named in the outcome template (`operator · support · skills · cross-boundary release owner · maturity`) as stated conditions where the evidence is not yet in hand |
| **Comparator** | `ALT-011` is *first to assess*, never *chosen*; `COMPARATOR EVIDENCE ABSENT` |
| **Verdict** | **PASS** |

---

### T-07 — Strict low-latency requirement

| | |
|---|---|
| **Decisive evidence** | pass/fail within 200 ms, synchronous, transactionally visible, across two internal services and a market-data feed |
| **S1 candidates** | Row 17 *atomicity across ≥2 systems with no acceptable compensation window — collapse to one transactional owner* → `ALT-005`, `ALT-006`, `ALT-007`; mandatory `ALT-002` (renegotiating the objective is a legitimate response), `ALT-010` |
| **Stages** | S2 (absolute — the requirement applies to the **whole path**) · S5 D3 · S9. S6–S8 add nothing decisive |
| **Decisive concern** | C2 + C9 — a hard sub-second, transactionally-visible end-to-end objective is **sized nowhere** |
| **Grade** | `Confirmed` requirement; `Confirmed` and current pack evidence that no end-to-end latency figure is published for any path |
| **Disqualifier** | **`Xp`, whole scope** for the pre-trade check — over-determined. **Not a bounded excess**, so no hybrid shape is available |
| **Outcome** | **5 — POOR FIT, excluded for this scope** → **8**: `ALT-005`, `ALT-006`, `ALT-007`, `COMPARATIVE FIT UNEVALUATED` |
| **Scope** | the surrounding case-management workflow is a **separate scope** where the platform stays viable |
| **Comparator** | the runtime does **not** claim a custom stack achieves 200 ms; the alternative-side evidence it may state is the documented **limits** (`ALT-005`'s HTTP ceiling and cold start, `ALT-006`'s synchronous window) — none of which favours one over another at 200 ms |
| **Verdict** | **PASS** |

---

### T-08 — Regulated, security-sensitive workload *(evidence-grade regression)*

| | |
|---|---|
| **Decisive evidence** | special-category personal data; validated-systems regime with change control; customer-managed keys mandated; administrator exclusion demanded contractually; country-level residency; 600 users / 4 countries |
| **S1 candidates** | Row 24 *confidential even from platform administrators* → `ALT-005`, `ALT-001`, `ALT-007`; row 23 *behaviour frozen / per-release change control* → `ALT-005`; row 26 → `ALT-011`; `ALT-008` on the self-managed upgrade cadence; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 (absolutes: residency, regulatory regime, administrator exclusion) · **S3 (terminal first)** · S5 D3 · S6 (`CD-03` branch) · S8 · S9 |
| **Decisive concern** | C6 + C7 — mandated controls against documented availability |
| **Grade** | **`Unknown` — the regime clause has not been read** (`B-14`, `custo: documento`). The key-versus-audit incompatibility is a **`Conflicted` decision-critical value** and may not be settled either way |
| **Blocker** | **yes** — `B-14` regulatory regime · `B-05` residency clause · the `Conflicted` key/audit pair. Spine §4: none of these can settle a hard exclusion |
| **Sequence** | **12 first** — never a settled class 5 emitted from an assumed reading of the regime |
| **Composed** | **`CD-03`** available on the branch where the mandated control's licence population is **unfunded** → **7 (`7-INFEASIBLE`)**, an economic finding, never a capability one |
| **Outcome** | **12** → on resolution: administrator-excluded attribute placed outside the governed store, S7 gates satisfied → **3 — hybrid**; mandated control with **no available implementation** → **5** (`Xp`) → **8**: `ALT-011`, `ALT-005`, `ALT-007`, `ALT-008` |
| **Comparator** | a validated trial-management product exists **as a category**; no product was evaluated → `COMPARATIVE FIT UNEVALUATED`. The key-versus-audit conflict is **not silently resolved** |
| **Verdict** | **PASS** |

---

### T-09 — Mission-critical workload *(evidence-grade regression)*

| | |
|---|---|
| **Decisive evidence** | 24×7 outage dispatch; committed 15-minute recovery time; must survive region loss; field devices + geospatial; 300 dispatchers + 2,000 field engineers with offline capture |
| **S1 candidates** | Row 20 *contractual availability or recovery-time commitment* → `ALT-005`, `ALT-006`, `ALT-007`; `ALT-009`; row 26 → `ALT-011`; `ALT-004` for the dispatch experience with offline over the governed store; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 · **S3 (terminal first)** · S5 · **S6 (`CD-04`)** · S7 · S9 |
| **Decisive concern** | C9 + C10 — cross-region recovery, composite availability, provability |
| **Grade** | **`Unknown`** on `B-25` (objectives **plus a timed drill**) and `B-22` (per-flow dependency map). No published cross-region recovery-time commitment exists to cite |
| **Blocker** | **yes** — a contractual 15-minute cross-region objective **cannot be underwritten from platform evidence**; it can only rest on the customer's own drills |
| **Composed** | **`CD-04`** → **12**, *the drill and the representative managed test environment are the evidence task, never an exclusion* |
| **Outcome** | **12** → on resolution: commitment restated as a drilled, customer-owned objective → **2** for the dispatch experience with offline capture (a genuine platform strength); commitment held as contractual → **6 — excluded for the named responsibility** (the recovery commitment) → **8**: `ALT-005`, `ALT-006`, `ALT-007` for the dispatch core |
| **Order dependency** | evaluating offline (a strength) before recovery (an absence) produces an optimistic answer; the spine's non-commutative S2→S3-before-S4/S5 ordering prevents it |
| **Comparator** | **none of the candidate classes is evidenced to meet 15 minutes either** — the candidate set is a set to assess, not a ranking. A hybrid **worsens** composite availability, and the outcome says so |
| **Verdict** | **PASS** |

---

### T-10 — Citizen-developed app become enterprise-owned *(migration regression)*

| | |
|---|---|
| **Decisive evidence** | team-scoped holiday-planning app; now 1,400 users across five countries; **default environment**; **non-solution artefacts**; unowned; **original maker gone**; criticality now business-critical; entitlement now population-wide |
| **S1 candidates** | Row 1 → `ALT-001` (the HR system probably owns leave), `ALT-003`, `ALT-007`, `ALT-011`; row 26 *standardised, non-differentiating domain* → `ALT-011`, `ALT-007`; `ALT-004` **rebuilt**; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 · **S3 (terminal first)** · S5 · **S6 (`CD-11`)** · S7 · S8 · S9 |
| **Decisive concern** | C7 + C8 + C10 — the two concerns that produce no exclusion of their own, decisive **only** in combination |
| **Grade** | `Confirmed` on all three participating conditions (default estate, non-solution artefacts, maker departed, criticality). **Ownership of the future state is `Unknown`** (`B-02`, named **and accepted**) |
| **Blocker** | **yes, first** — `B-02` *who owns it?* |
| **Composed** | **`CD-11` fires**, all three conditions holding. Named mechanisms: non-solution artefacts are outside backup, ineligible for capacity licensing and undeployable; a non-solution automation's **owner cannot be changed at all**; the departed maker's profile has already reverted |
| **Outcome** | **12** → on resolution → **14 — IN-PLACE REMEDIATION UNAVAILABLE, MIGRATION REQUIRED** → **8**: `ALT-011`, `ALT-001`, `ALT-004 (rebuilt)`, `ALT-002` |
| **Migration checks** | (i) `CD-11` fires correctly ✔ (ii) it does **not** render as an ordinary platform exclusion — class 5 does **not** fire and the class-14 template states the platform **rebuilt** is a live candidate ✔ (iii) it does **not** render as remediation — the output says the required work is **migration/replacement of the artefact at that scope** ✔ |
| **Not the operability scenario** | `CD-09` (criticality ≥2 classes above demonstrated maturity) is also live here and is **sponsor-side and platform-independent** — it may reach 11 or 12, **never** a platform exclusion. The two rows coexist without contaminating the terminal |
| **If the platform is retained** | preconditions carried on the `ALT-004 (rebuilt)` assessment: a new environment · solution-aware artefacts · named ownership · a premium-licence census for 1,400 users |
| **Comparator** | `ALT-011`/`ALT-001` are *strongest candidates* = **first to assess**, never *chosen*; `COMPARATIVE FIT UNEVALUATED` |
| **Verdict** | **PASS** |

---

### T-11 — Hybrid platform + cloud-native

| | |
|---|---|
| **Decisive evidence** | assessors work in a low-code application; each submission triggers ML classification and OCR; 3,000/month in two annual peaks; **a mature cloud platform team exists** |
| **S1 candidates** | Row 8 *real computation inside a step* → `ALT-006`, `ALT-009`, `ALT-005`; row 6 *human decision inside the documented in-platform wait window — keep this leg in-platform even if other legs move* → `ALT-004`; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 · S5 (C2 compute — a **bounded, nameable** excess) · S6 (**`CD-02` and `CD-07` tested and do not fire**) · **S7 (all five gates satisfied — and that is the finding)** · S8 · S9 |
| **Decisive concern** | C2 (compute intensity at one step) — explicitly **not** a reason to relocate the solution |
| **Grade** | `Confirmed` — the operator, support and pro-code capability exist and are funded |
| **Outcome** | **3 — HYBRID WITH CLOUD-NATIVE SERVICES**, rendered as a scope pair. Conditions: two supply chains · a declared release sequence · a propagated correlation identifier · an idempotency key on the classification write (`B-11`) · a status resource for the asynchronous work |
| **Comparator** | no preference asserted between `ALT-009`, `ALT-005`, `ALT-006`; the gates passing is a **capability fact about this organisation**, not an advantage of any class |
| **Verdict** | **PASS** — the inverse of T-05: the gates *being satisfied* is what makes the option available |

---

### T-12 — The incumbent should own the capability *(scope-pair regression)*

| | |
|---|---|
| **Decisive evidence** | a mature service-management platform with an **undeployed** scheduling module; an integration platform with **published contracts** for that system; the platform team has a lead time |
| **S1 candidates** | Row 15 *integration already owned, with a published contract* → `ALT-007`; row 16 *process class already owned by an existing engine* → `ALT-007`; row 1 → `ALT-001`, `ALT-011`; row 26 → `ALT-011`; `ALT-004` only for a genuinely uncovered surface; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 · S4 (**whose problem is this** — integration ownership before what to build) · S5 · S7 · S9 |
| **Decisive concern** | C5 — integration ownership |
| **Grade** | **`Confirmed`** — the contract exists and is published, which is what permits a **settled** responsibility-scoped exclusion |
| **Disqualifier** | **`Xr` — named responsibility only**: the platform is not the integration layer |
| **Outcome — two pairs, uncollapsed** | *(integration responsibility)* → **6 — EXCLUDED FOR THIS RESPONSIBILITY** → **8**: `ALT-007` (deploy the incumbent's module), `ALT-001`, `ALT-011`. *(surrounding scope)* → **4 — HYBRID WITH THE INCUMBENT SYSTEM** where the incumbent keeps authority and the platform supplies a lightweight field-facing surface — but **only if** the incumbent's mobile experience fails a stated requirement |
| **Bounded-exit check** | class 6's template **mandates** *"it may remain the correct answer for `<the surrounding scope>`"*. The bounded exit does **not** become a whole-solution rejection |
| **Comparator** | `INCUMBENT FIT UNEVALUATED` carried explicitly; a per-requirement gap analysis is required; the platform team's lead time is recorded as a **constraint**, never as a justification for bypassing them. *Preferred* is not in the closed set and is not emitted |
| **Verdict** | **PASS** |

---

### T-13 — Custom application clearly preferable *(comparator regression)*

| | |
|---|---|
| **Decisive evidence** | branded consumer mobile app in both stores; push notifications; offline capture with **custom conflict rules**; 400,000 consumers; an intended **public third-party interface** |
| **S1 candidates** | Row 18 *product-grade experience; native distribution with push* → `ALT-005`; row 19 *a public third-party API is the deliverable* → `ALT-005`; `ALT-009` for the composition; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S2 (absolutes: identity class, offline behaviour, distribution) · S5 · **S6 (`CD-10`)** · S8 (economic corroboration) · S9 |
| **Decisive concern** | C3 — interaction, identity class, distribution and offline behaviour |
| **Grade** | `Confirmed` on four independent documented exits |
| **Disqualifier** | **`Xp`, whole scope (the consumer surface)**, over-determined; a corroborating **`Xe`** at 400,000 consumers |
| **Composed** | **`CD-10`** third leg — *mobile-first + device hardware + branded distribution with push* — a documented mutual exclusion, unsatisfiable in-platform |
| **Outcome** | **5 — POOR FIT, excluded for this scope** → **8**: `ALT-005` |
| **Comparator** | a candidate set of one is **scope narrowing, not evaluation**, and the outcome says so. `COMPARATOR EVIDENCE ABSENT` sits **inside** the outcome string. The runtime does **not** emit *custom is better / cheaper / faster* — both directions are prohibited universals |
| **Second scope** | the platform remains a legitimate candidate for the **internal operations** behind the consumer surface; the composition is `ALT-009` |
| **Class-7 discipline** | the economic finding corroborates a capability exclusion at the same scope; **no disjunction and no class-7 terminal is emitted**, because class 5 is settled on capability evidence |
| **Verdict** | **PASS** |

---

### T-14 — Economically unattractive *(class-7 + comparator regression)*

| | |
|---|---|
| **Decisive evidence** | internal expense pre-approval; **9,000 employees, each using it about twice a month**; the finance-system connector is premium; a **network-isolation mandate** because of the finance data |
| **S1 candidates** | Row 1 → `ALT-001` (the finance system almost certainly has expense pre-approval), `ALT-011`; row 25 *private-network execution* → `ALT-006`, `ALT-009`, `ALT-007`; row 26 → `ALT-011`; row 28 *a required control's population is unfunded* → `ALT-010`, or a scope change; row 2 → `ALT-002`, `ALT-010`; `ALT-005`; mandatory members present |
| **Stages** | S0 (value versus **full** cost) · S1 · S5 (platform remains **technically** viable) · S6 (**`CD-03`**) · **S8 (the pivot — ten dimensions, same workload, every candidate)** · S3 re-run after S8 · S9 |
| **Decisive concern** | C11 — entitlement, control population and demand shape |
| **Grade** | **`Confirmed`**: population, frequency, the premium connector requirement, the isolation mandate and the managed-class consequence. **`Unknown`**: whether the resulting licence population is funded (`B-23`) |
| **Subtype selection (mandatory discriminator)** | chosen **from the trigger, not from tone**: the settled finding is the **demand shape** — large population × low frequency, entitlement across 9,000 people, control prerequisites priced by **affected population**, support tier — with funding not shown to be absent ⇒ **`7-UNATTRACTIVE`: *economically unattractive for this demand shape***. The unfunded-mandate leg is **not** settled; it is carried as an evidence obligation on `B-23`, and **on resolution to *unfunded* the outcome hardens to `7-INFEASIBLE`** via `CD-03` (a funding fact — *funding it restores viability*) |
| **Disjunction** | **not rendered.** One explicit semantic reason is emitted, with the dimensions that move and the mechanism by which they move |
| **Volatility** | tripwire **`TW-V3`** (managed-environment licence enforcement, February 2027) is directly on the path — the whole environment population is re-priced, not the app's own users. Carried as a dated assumption with `verificado_em`/`validade` and into `/decide` as a revision condition |
| **Outcome** | **7 (`7-UNATTRACTIVE`)** → **8**: `ALT-001`, `ALT-011`, `ALT-002`, `ALT-005`, `ALT-006`, `ALT-010` |
| **Comparator** | *this option is expensive for this demand shape* is stated; **nothing whatever is stated about what the others cost** — no comparative TCO study exists against any named alternative. The forbidden repair *never remove the required control to make the option look cheaper* is enforced at S8: an unfunded **mandated** control is infeasibility, not a trade-off |
| **Hypothesis discipline** | the users-to-work ratio is high and **directionally** against people-priced mechanisms — carried as *a hypothesis to test on all ten dimensions with current pricing and the customer's own agreement*, never as a verdict |
| **Verdict** | **PASS** |

---

### T-15 — Insufficient information

| | |
|---|---|
| **Decisive evidence** | *"a portal so suppliers can see their orders"* — no volume, no identity model, no ownership, no budget, no regulatory position, no residency statement, the order system unnamed |
| **S1 candidates** | no dominant requirement is known, so no trigger row can close the set; **all eleven classes remain open** and the two mandatory members (`ALT-002`, `ALT-010`) are generated regardless. A class not generated is **not** a class eliminated |
| **Stages** | S0 (cannot establish value against cost) · S1 · **S3 (terminal)**. S4–S9 are not reached, legitimately |
| **Decisive concern** | all twelve are `Unknown` at the dimensions that select an option |
| **Grade** | `Unknown` throughout; **no figure may be estimated to unblock the analysis** |
| **Blocker** | `B-03` identity class · `B-04`/`B-06` source of record and integration ownership · `B-27` deployment model · plus `B-05`, `B-14`, `B-23`, `B-24`, `B-25`, `B-26` |
| **Outcome** | **12 — DECISION BLOCKED**, one named evidence task per engaged entry, each with its **expected form** (clause / inventory / measurement / drill result), its **likely role type**, its `custo` default and — mandatory — **the outcome each resolution would produce**, so the sponsor can see which questions actually matter |
| **Anti-pattern guard** | *"a portal"* is already a solution shape; the spine's *architecture shapes are not the option space* rule prevents the analysis starting there |
| **Verdict** | **PASS** |

---

### T-16 — Conversational assistant over enterprise data *(agentic regression)*

| | |
|---|---|
| **Decisive evidence** | an assistant for 900 internal engineers **and** an unstated number of channel partners, over maintenance manuals, a parts catalogue and open work orders; answers expected actionable; a stated ambition that it later raise a work order itself |
| **S1** | **Row 29 fires: *conversational or agent-shaped interaction → none evaluable*.** Fit is `UNKNOWN` in **every** class, `ALT-004` **included**. The correct output is a block, **not** a candidate set — emitting one would be invention |
| **Stages** | S1 · **S3 (terminal)** · volatility consulted on demand. S5–S9 cannot run on fit that does not exist |
| **Decisive concern** | C3/C6/C7/C10/C11 — but the decisive fact is the **absence of any fit assessment in the corpus**, which is a different thing from an absence of exits |
| **Grade** | `Unknown` — and specifically *the pack never looked*, not *the pack looked and found no exit*. That distinction is what stops the block collapsing into a fit verdict |
| **Blocker** | **`BS-03`** — the commercial and governance model for an agent surface and, at the autonomous end, the **modality question itself**; consumption is *dependent on task complexity* and unmodellable in advance; agent governance is evolving with preview authentication and channel controls. Volatility `VS-20` (request bucket, a bundled credit entitlement with a **dated removal** — `TW-V2`, 1 November 2026) and `VC-10` |
| **Outcome** | **12 — DECISION BLOCKED**, for **every** option class including `ALT-004`, with three separable blocks: **governance/security** (does the partner audience reach content through a graph/search connector — if so the guest-access control does not close the requirement) · **commercial** (closes only with a bounded pilot sized for the monthly peak) · **modality** (the autonomous ambition closes from a research commission, not from the existing corpus) |
| **Neutrality checks** | richer platform knowledge creates **no** preference ✔ · no candidate is declared fit by inference ✔ · the missing evidence is named ✔ · nothing is invented ✔ |
| **Class 11 not emitted** | the unknowns are **closable** (pilot, commission), so *do nothing / defer* would be a wrong terminal |
| **Verdict** | **PASS** |

---

### T-17 — Multi-month approval process *(`Ri` regression — mandatory)*

| | |
|---|---|
| **Decisive evidence** | capital-expenditure approval running 90–120 days end to end, dominated by human review and cross-department sign-off; the requesting department owns it; **no external system or component is involved**; **no on-call operator exists for anything outside the platform** |
| **S1 candidates** | Row 10 *process outliving the documented single-run duration, or resumable* → `ALT-006`, `ALT-009` (**candidate generation, not a verdict**); row 6 *human decision inside the documented in-platform wait window — keep this leg in-platform even if other legs move* → `ALT-004`; mandatory `ALT-002`, `ALT-010` |
| **Stages** | S0 · S1 · S2 (**the finding is classified as `Ri`, not as an exit**) · S5 · S6 · S7 · S9 |
| **Decisive concern** | C2 — work shape against the documented single-run ceiling |
| **Grade** | `Confirmed` on the process duration; the run-duration ceiling itself is volatile (`VS-12`/`VS-13`) and is re-read at the decision date — **the spine carries no figure** |
| **Consequence class** | **`Ri` — in-platform redirect.** The run mechanism becomes unavailable and the documented answer is a **different in-platform choice**: a business record with a re-triggering automation. **Nothing leaves the platform.** Spine §3 and outcome §1.3 forbid `Ri` from producing 3, 4, 5, 6 or 7 |
| **`CD-02` must not fire** | its first participating condition is *a pattern requiring an external component*. None is proposed, so the row cannot fire — which is precisely why the absence of an on-call operator does not manufacture an exclusion here |
| **S7 gates** | the operator gate **fails for `ALT-006`/`ALT-009`**, making those classes **unavailable**. The output states this is a **documented capability gap in those classes, not an advantage of the platform**, and notes both are themselves constrained on the duration axis that triggered them |
| **Outcome** | **2 — FIT WITH CONSTRAINTS**, the business-record-plus-re-triggering-automation pattern named as the stated condition, with the audit-retention requirement beyond the run window as a design input |
| **Regression result** | `Ri` produces **no exclusion**; **no responsibility is falsely moved outside the platform**; the output says the **design/pattern changes while platform viability remains** |
| **Verdict** | **PASS** |

---

### T-18 — Per-user backend authorization through a mediation tier *(`Xc` regression — mandatory)*

| | |
|---|---|
| **Decisive evidence** | an expense-reimbursement workflow calls a finance system that enforces authorization **per user**; a facade sits on the path and calls it with a **single shared service identity**; the facade does not propagate the caller's identity; **whether it can be modified to do so is not yet known** |
| **S1 candidates** | Row 7 *bounded connector work over the existing estate* → `ALT-004`; row 15 → `ALT-007` where the facade's owner holds a published contract (`B-06`); mandatory `ALT-002`, `ALT-010`. **No off-platform destination is named by any condition in this row** |
| **Stages** | S2 (the finding is classified as a **combination input** — it carries no exit of its own) · S3 · **S6 (`CD-06`)** · S9 |
| **Decisive concern** | C6 — authorization model and enforcement point |
| **Grade** | **`Unknown`** on propagation feasibility, and decision-changing |
| **Combination-input discipline** | terminating on the authorization-enforcement finding alone would be a **category error**; the runtime resolves the row it feeds |
| **Composed** | **`CD-06` fires** — per-user backend authorization required **+** a facade or worker calling downstream as a shared identity. Its consequence is **conditional by design**: *fit with constraints* where identity is propagated or compensating authorization is implemented; *decision blocked* where propagation feasibility is unknown; **never an exclusion outcome** |
| **Outcome** | **12 — DECISION BLOCKED** on the propagation question. **Resolves yes → 2**, with explicit delegated identity as the named, owned condition. **Resolves no → still 12**, pending a compensating-authorization design |
| **Forbidden terminals** | **5, 6 and 7 are unreachable from this row** — the composed register states no row maps to an exclusion outcome unless its consequence is an actual capability or economic finding about the platform, and `CD-06`'s is a design constraint |
| **Verdict** | **PASS** |

---

### Replay summary

| T | Canonical expectation | Runtime terminal | Reason matched | Verdict |
|---|---|---|:--:|:--:|
| T-01 | 1 **or** 13, graduation trigger mandatory | **13 form (a)**, stands alone, trigger recorded | ✔ | PASS |
| T-02 | 2 | **2**, `Ri` store change, entitlement priced | ✔ | PASS |
| T-03 | 12 → 4 (hybrid with incumbent) | **12 → 4 / 2** per resolution | ✔ | PASS |
| T-04 | 12 → 2 **or** 6 → 8 | **12 → 2 / 6 → 8** | ✔ | PASS |
| T-05 | 3, or 2 when the operator gate fails | **3 / 2 (tripwire condition) / 6 → 8**; 12 on `CD-05` | ✔ | PASS |
| T-06 | scope pair 2 + 3 | **2 (application) + 3 (analytical)**, uncollapsed | ✔ | PASS |
| T-07 | 5 → 8 (`Xp`) | **5 → 8**, three candidates, none preferred | ✔ | PASS |
| T-08 | 12 → 3 **or** 5 → 8 | **12 → 3 / 5 → 8**; `CD-03` branch to 7 available | ✔ | PASS |
| T-09 | 12 → 6 → 8 (recovery commitment) | **12 → 2 / 6 → 8** | ✔ | PASS |
| T-10 | 12 → **14** → 8 | **12 → 14 → 8**, `CD-11`, migration not remediation | ✔ | PASS |
| T-11 | 3, gates pass | **3**, gates satisfied and stated | ✔ | PASS |
| T-12 | 6 → 8, or 4 | **6 → 8 (integration) + 4 (surrounding)**, uncollapsed | ✔ | PASS |
| T-13 | 5 → 8 (`ALT-005` only) | **5 → 8**, scope narrowing stated; `CD-10` | ✔ | PASS |
| T-14 | 7 → 8, subtype rendered | **7 (`7-UNATTRACTIVE`) → 8**, hardening path to `7-INFEASIBLE` named | ✔ | PASS |
| T-15 | 12 | **12**, eleven classes open, per-resolution outcomes | ✔ | PASS |
| T-16 | 12 in **every** class | **12**, three separable blocks, `ALT-004` included | ✔ | PASS |
| T-17 | **2** | **2**, `Ri` condition named | ✔ | PASS |
| T-18 | **12 → 2** | **12 → 2**; 5/6/7 unreachable | ✔ | PASS |

**18/18 traced. 0 terminal mismatches.**

---

## 3. Evidence-grade regression

The final Step 3A rule was exercised in all five states.

| Evidence state | Scenario exercising it | Runtime behaviour | Correct |
|---|---|---|:--:|
| `Confirmed` **and current** | T-12 (published contract), T-13 (four documented exits), T-07 (whole-path objective), T-10 (`CD-11`'s three conditions) | Settles the exclusion at its scope — 6, 5, 5, 14 respectively | ✔ |
| `Assumed`, **not** decision-changing | T-02 (the growth assumption behind the analytical path) | Provisional, carried with its basis; does not block, does not become fact | ✔ |
| `Assumed`, **decision-changing** | **T-04** (the *expected* sub-minute freshness figure) | Provisional disqualifier **+ evidence obligation**; `Unknown`, `swing: decisivo`; **decision blocked** | ✔ |
| `Unknown` | **T-08** (regime clause), **T-09** (RPO/RTO + drill), **T-10** (accepted ownership), T-03, T-15, T-18 | Obligation created; blocked where decision-changing | ✔ |
| `Conflicted` | **T-08** (key control versus audit), **T-05** (the live 20× ceiling conflict) | Both readings named; **not resolved silently**; blocked | ✔ |
| Materially expired | structural — an expired row reads as **weak `Assumed`** and may never be cited as `Confirmed`; `/answer --revalidate` is the route | Enforced by spine §4 | ✔ |

**The forbidden sequence `assumption → settled exclusion` did not occur in any of the eighteen replays.**
The mandated sequence — `uncertain decisive evidence → decision blocked → evidence resolved → settled
outcome` — was observed in **T-04, T-08, T-09, T-10**, exactly as the gate requires.

**Symmetry.** In T-07, T-09 and T-14 the same standard was applied to the alternative classes: no
`Assumed` claim that a custom build *cannot* (or *can*) meet the requirement was allowed to settle
anything. In T-09 the runtime states explicitly that none of `ALT-005`/`006`/`007` is evidenced to meet
15 minutes either.

**Result: PASS.**

---

## 4. `Ri` / `Xc` / migration regressions

### 4.1 `Ri` — T-17 (in-platform redirect)

| Check | Result |
|---|:--:|
| `Ri` produces **no** exclusion outcome (3, 4, 5, 6, 7 unreachable) | ✔ |
| No responsibility is falsely moved outside the platform | ✔ |
| Output states the **design/pattern changes while platform viability remains** | ✔ |
| `CD-02` cannot fire (no pattern requiring an external component) — the missing operator does not manufacture an exclusion | ✔ |
| The S7 gate failure for `ALT-006`/`ALT-009` is rendered as a **documented capability gap in those classes**, not an advantage of the platform | ✔ |
| Terminal | **class 2** |

**PASS.** This is the defect the canonical Repair V3 exists for, and the authored runtime is structurally
immune to it: the redirect is classified at S2 as a non-exit consequence, so no off-platform destination
is ever proposed for the exit machinery to consume.

### 4.2 `Xc` — T-18 (composed authorization semantics)

| Check | Result |
|---|:--:|
| `CD-06` fires on both participating conditions | ✔ |
| Unknown propagation → **class 12** | ✔ |
| Condition satisfied → **class 2**, delegated identity as the named, owned condition | ✔ |
| Classes **5, 6, 7 never reachable** from this row | ✔ |
| The authorization finding is treated as a **combination input** with no terminal of its own | ✔ |

**PASS.**

### 4.3 Migration — T-10

| Check | Result |
|---|:--:|
| `CD-11` fires on all three conditions | ✔ |
| Does **not** render as an ordinary platform exclusion (class 5 does not fire; the platform **rebuilt** stays in the candidate set) | ✔ |
| Does **not** render as remediation | ✔ |
| Output makes clear the required work is **migration/replacement of the artefact at that scope**, naming the mechanisms (backup exclusion · capacity-licence ineligibility · undeployability · an automation owner that cannot be changed at all · the reverted maker profile) | ✔ |
| Not confused with the operability scenario — `CD-09` is present, **sponsor-side**, and never renders as a platform exclusion | ✔ |
| Terminal | **12 → 14 → 8** |

**PASS.**

---

## 5. Scope-pair regression

| Scenario | Pairs rendered | Collapsed? |
|---|---|:--:|
| **T-06** | *(application scope → 2 fit with constraints)* **+** *(analytical/board-reporting responsibility → 3 hybrid with cloud-native)* | **No** |
| **T-12** | *(integration responsibility → 6 excluded → 8)* **+** *(surrounding scope → 4 hybrid with the incumbent; the platform may remain the correct answer, and the outcome must say so)* | **No** |
| T-04 | *(external-site read surface → 6)* **+** *(authenticated document access → still a candidate)* | No |
| T-07 | *(pre-trade check → 5)* **+** *(surrounding case management → separate scope, viable)* | No |
| T-09 | *(recovery commitment → 6)* **+** *(dispatch experience with offline → 2)* | No |
| T-13 | *(consumer surface → 5)* **+** *(internal operations behind it → candidate; composition `ALT-009`)* | No |
| T-05 | *(bulk/ordering responsibility → 3)* **+** *(application scope → viable)* | No |

**No bounded responsibility exit became a whole-solution rejection in any scenario.** Class 6's render
template makes the surrounding-scope statement **mandatory**, which enforces this structurally rather
than by discipline.

**Result: PASS.**

---

## 6. Economic / class-7 regression

Exercised on **T-14** (primary), with T-13 and T-08 as controls.

| Requirement | Behaviour |
|---|---|
| One explicit semantic reason, never the disjunction | **`7-UNATTRACTIVE` — *economically unattractive for this demand shape***, naming the dimensions that move and the mechanism |
| Subtype chosen by **evidence/trigger**, not tone | The settled trigger is the demand shape (population × frequency × control prerequisites priced by affected population), all `Confirmed`. The *unfunded mandated control* trigger is **not** settled, because `B-23` is `Unknown` |
| The unresolved leg handled correctly | Carried as an evidence obligation; **on resolution to *unfunded* the outcome hardens to `7-INFEASIBLE` via `CD-03`** — a funding fact, and *funding it restores viability* |
| No unsupported comparative price claim | None emitted; no comparative TCO study exists against any named alternative and the outcome says so |
| Excluding the platform economically does **not** imply another class is cheaper | Enforced by class 7's rule 4 and by the class-8 continuation, `COMPARATIVE FIT UNEVALUATED` |
| The forbidden repair | *Never remove the required control to make the option look cheaper* — S8: an unfunded **mandated** control is infeasibility, not a trade-off |
| Volatility | `TW-V3` (managed-environment licence enforcement, February 2027) carried as a dated assumption and as a `/decide` revision condition; `VC-05`/`VC-06` re-read at the decision date |
| Control — T-13 | An economic finding corroborates a capability exclusion at the same scope; class 5 is emitted on capability evidence and **no class-7 disjunction appears** |
| Control — T-08 | `CD-03`'s economic branch is available and distinct from the capability branch (class 5) — the two are not conflated |

**Result: PASS.**

---

## 7. Comparator discipline

The four statements — exclusion · candidate generation · comparative evaluation · preference — stayed
separate in every scenario.

| Scenario | Exclusion | Candidates | Comparative evidence | Preference |
|---|---|---|---|---|
| T-04 | 6 `[R]` | `ALT-005`, `ALT-011` | **absent** — no latency/throughput measurement exists for any technology | none |
| T-07 | 5 `[W]` | `ALT-005`, `ALT-006`, `ALT-007` | documented **limits** on `ALT-005`/`ALT-006` only; nothing favouring either at 200 ms | none |
| T-08 | 5 `[W]` or 3 | `ALT-011`, `ALT-005`, `ALT-007`, `ALT-008` | a product **category** exists; **no product evaluated** | none |
| T-09 | 6 `[R]` | `ALT-005`, `ALT-006`, `ALT-007` | those classes *can* underwrite a contractual objective; **none is evidenced to meet 15 minutes** | none |
| T-10 | 14 `[W]` | `ALT-011`, `ALT-001`, `ALT-004` rebuilt, `ALT-002` | none — *strongest candidate* means **first to assess** | none |
| T-12 | 6 `[R]` | `ALT-007`, `ALT-001`, `ALT-011` | **`INCUMBENT FIT UNEVALUATED`** — the pack evaluates no incumbent | none |
| **T-13** | 5 `[W]` | `ALT-005` **only** | **absent**; a set of one is **scope narrowing, not evaluation** | none |
| **T-14** | 7 `[E]` | six classes | **absent in every direction** — no comparative pricing was ever fetched | none |

**The forbidden inference `platform excluded → therefore custom is better` did not appear in any
scenario, in either direction.** `COMPARATOR EVIDENCE ABSENT` / `COMPARATIVE FIT UNEVALUATED` is carried
**inside** the outcome string, never as a footnote.

**The one permitted preference axis — the deployment model (class 9) — is not triggered by any canonical
scenario** (T-08 names `ALT-008` for an unrelated reason, and the canonical body states the
deployment-model criterion is not triggered there). The class remains reachable, and its comparator claim
did **not** leak into any other scenario.

**Result: PASS.**

---

## 8. Reachability floor

| Scenario | Surviving/candidate classes | Only platform forms? | Reasoning started from |
|---|---|:--:|---|
| T-01 | 003, 001, 007, 011, 002, 010 | No | *what materially different responses remain defensible* |
| T-02 | 004, 001, 003 (eliminated on its own evidence), 011, 002, 010 | No | same |
| T-03 | 001, 007, 009, 004, 002, 010 | No | same |
| T-04 | 005, 011, 004 (partial scope), 002, 010 | No | same |
| T-05 | 006, 009, 007, 004, 002, 010 | No | same |
| T-06 | 004, 011, 006/007/009, 002, 010 | No | same |
| T-07 | 005, 006, 007, 002, 010 | No | same |
| T-08 | 011, 005, 007, 008, 002, 010 | No | same |
| T-09 | 005, 006, 007, 009, 011, 004 (partial), 002, 010 | No | same |
| T-10 | 011, 001, 004 rebuilt, 002, 010 | No | same |
| T-11 | 009, 005, 006, 004, 002, 010 | No | same |
| T-12 | 007, 001, 011, 004 (uncovered surface only), 002, 010 | No | same |
| T-13 | 005, 009 composition, 004 (internal only), 002, 010 | No | same |
| T-14 | 001, 011, 002, 005, 006, 010 | No | same |
| T-15 | all eleven open | No | same |
| T-16 | none evaluable — block | No | same |
| T-17 | 004, 006/009 (**eliminated by their own S7 evidence**), 002, 010 | No | same |
| T-18 | 004, 007, 002, 010 | No | same |

**`ALT-002` and `ALT-010` are mandatory members at S1 in all eighteen replays** and are never eliminated
by a finding about the platform — only by their own evidence. **No scenario's reasoning began with
*which platform architecture should we use?*** The architecture templates are explicitly not the option
space (spine §1), and no candidate set collapsed to platform forms only.

**T-17 is the sharpest instance**: `ALT-006`/`ALT-009` were **generated**, then **eliminated by their own
capability evidence** (no operator; both constrained on the very duration axis that triggered them) —
not omitted because the active pack is the platform.

**Result: PASS.**

---

## 9. D0 versus evidence gap

| Case | Scenario | Concern | Rationale | Classification |
|---|---|---|---|---|
| **Legitimate D0** | **T-17** | C10 (external operator/support dimension) | *"No external system or component is involved"* — affirmative engagement evidence that nothing outside the platform must be operated | **D0**, auditable one-liner |
| **Legitimate D0** | T-01 | C5 integration | *"No integration"* — affirmative | **D0** |
| **Legitimate D0** | T-01 | C7 regulatory dimension | *"No regulatory regime"* — affirmative | **D0** |
| **Legitimate D0** | T-11 | C10 operator | *"A mature cloud platform team exists"* with named operators — affirmative, and the finding is that the gates pass | **D0/D1** |
| **Evidence gap ≠ D0** | **T-01** | C3 offline dimension | Equipment inspection could plausibly be walked; the scenario is **silent**. Silence is never a D0 rationale | **D1 + `Unknown`**, `swing: dimensionante`, **carried, not blocking** |
| **Evidence gap ≠ D0** | T-06 | C6 administrator exclusion | Could be material on commercially sensitive clauses; not stated | **D1/D2 + `Unknown`**, escalates only if asserted |
| **Evidence gap that *does* block** | T-03, T-09 | C10 / C9 | Support tier, maturity, RPO/RTO at business- and mission-critical class | **D3 + `Unknown`**, `swing: decisivo` → class 12 |

**Depth distribution observed across the replay** (representative, not exhaustive):
**D0** — T-01 C5/C7, T-17 C10-external, T-13 C4 residency · **D1** — T-01 most concerns, T-02 C7/C12,
T-17 C11 · **D2** — T-02 C4/C11, T-06 C5, T-05 C2, T-14 C1 · **D3** — T-04 C3/C9, T-07 C2/C9,
T-08 C6/C7, T-09 C9/C10, T-10 C7/C8/C10, T-14 C11.

**Not every `Unknown` was made decisive.** T-01's offline gap and T-06's administrator-exclusion gap were
carried without blocking; only a `decisivo` swing or an **engaged** blocking-set entry escalated.

**Result: PASS.**

---

## 10. C10 operability

No Discovery cue was added and no Discovery file was touched.

| Requirement | Scenario | Behaviour |
|---|---|---|
| C10 is reachable and evaluable | S5 **and** S7 both bind it; S7's gates make options **unavailable, not worse** | ✔ |
| **Evidence sufficient** | **T-11** | Operator, support, skills, cross-boundary release owner and maturity are all present and funded → the hybrid class becomes **available**, and the gates passing *is* the finding |
| **Decision-material evidence missing → `Unknown` / class 12** | **T-03** (support tier, maturity at business-critical), **T-09** (`CD-04`: no representative managed test environment, no drill) | Blocks; the drill and the environment are the **evidence task**, never an exclusion |
| **Gate failure makes an option unavailable rather than worse** | **T-05** (operator gate fails → the hybrid is unavailable; the responsibility stays in-platform with a tripwire), **T-17** (`ALT-006`/`ALT-009` unavailable) | ✔ |
| ***Technically feasible but not operable* remains expressible** | T-05, T-17, and `CD-02` generally | ✔ — the option is technically fine and **unavailable** for want of an operator, stated as such |
| Sponsor-side maturity is never a platform exclusion | T-03, T-10 (`CD-09`) | ✔ — 11 or 12, never 5/6/7 |

**Result: PASS.**

---

## 11. Cross-domain behaviour

| Interaction | Scenario(s) | Mechanism used |
|---|---|---|
| **security → economics** | **T-14**, **T-08** | Registered row **`CD-03`** (private-network / key-control / firewall requirement + unfunded licence population) → class 7, economic not capability; and secondary consequence carriage *security requirement → economics* |
| **data → performance / cost** | **T-02**, **T-06** | Secondary consequence carriage *data architecture → performance and cost*: delegation ceiling → analytical copy → budget; audit and retention consume log capacity no entitlement provides |
| **governance → ALM / operations** | **T-10**, **T-03** | Registered rows **`CD-11`** (default estate + criticality + departed maker) and **`CD-09`**; *governance control → lifecycle and operations* |
| **user / offline → architecture, control, support** | **T-13**, **T-09** | Registered row **`CD-10`** (offline + field-level security · offline + non-governed data beyond bound · mobile-first + device hardware + branded push) |
| **integration → resilience / operations** | **T-05**, **T-03** | Registered rows **`CD-05`**, **`CD-02`**; *integration limitation → workaround and resilience* |
| **scale → architecture / economics** | **T-14**, **T-04**, **T-09** | *Scale requirement → architecture and economics*; metering unit and population effects priced at S8 |

**Registered rows exercised in the replay:** `CD-02` (tested and correctly **not** fired in T-17),
`CD-03`, `CD-04`, `CD-05`, `CD-06`, `CD-09`, `CD-10`, `CD-11`. **Not exercised by the canonical corpus:**
`CD-01`, `CD-07`, `CD-08`, `CD-12` — coverage of the canonical scenario set, not runtime defects.

**Emergent-combination rule.** Emergent combinations arose (T-06: audit retention × log capacity × cost;
T-09: hybrid composition **worsening** composite availability) and were recorded as `Risky` rows with
**both** anchors named — **no thirteenth registered row was created anywhere in the replay.** The register
remains closed at twelve.

**Result: PASS.**

---

## 12. Volatility behaviour

| Requirement | Evidence from the replay |
|---|---|
| The stable decision **principle** stays in the spine | The spine carries the boundary shapes (*is the required freshness below the documented external-site floor?*) and **no platform figure anywhere** |
| The current **fact** is consulted from evidence / the register | T-04 → `VS-01` (external-site cache floor, re-verify *before any freshness commitment*) · T-17 → `VS-12`/`VS-13` (run-duration ceiling) · T-14 → `VC-05`/`VC-06` + `TW-V3` · T-16 → `VS-20`/`VC-10` + `TW-V2` |
| **Stale / conflicted decisive facts block** | T-05 → `VC-01`/`VS-08`, the **live 20× conflict**, `B-08`, `CD-05` → class 12 until *both* sources are re-read **and** the workload is measured. Neither figure is encoded |
| A **re-verification obligation** is produced | Every case above opens an `Unknown` (`custo: documento|spike`, `swing: decisivo`) with a named owner and date; the affected conclusion is **not treated as settled** |
| Volatile values do **not** become timeless rules | No figure entered any decision sentence; readings are recorded on the engagement's own row with `verificado_em` + `validade` |
| **The live conflict behaves symmetrically** | `CD-05` and the register both state it cuts across the platform, the cloud-native classes **and** the hybrid class **equally** — in T-05 the sizing block applies to `ALT-004`, `ALT-006` and `ALT-009` alike, and is **not** a penalty against the platform |
| Dated tripwires feed `/decide` and `/revisit` | `TW-V3` (T-14), `TW-V2` (T-16), `TW-V1` where an in-product ALM path is costed (T-03, T-10) |

**Result: PASS.**

---

## 13. Neutrality

**Categories the replay demonstrably reaches.**

| Category | Reached at |
|---|---|
| Process change | `ALT-002` live in T-01, T-10, T-14; class 10 reachable from S0 + trigger rows 2/3 (**no canonical `T` terminates there** — recorded, not a defect) |
| Existing capability | **T-01** (class 13 form (a), `ALT-003`), **T-12** (`ALT-007`/`ALT-001`) |
| This platform | **T-02**, **T-06**, **T-11**, **T-17** (classes 2 and 3), T-01's class-1 branch |
| SaaS / package | `ALT-011` as a live candidate in **T-08**, **T-10**, **T-14** — and correctly **never** as a *preferred* terminal, since that preference class is withdrawn |
| Custom / pro-code | **T-07**, **T-13** (class 5 → 8, `ALT-005`) |
| Hybrid / composed | **T-05**, **T-06**, **T-11** (class 3); **T-03**, **T-12** (class 4) |
| Do nothing / defer | `ALT-010` mandatory in all eighteen; class 11 reachable via `CD-09`-unfunded and trigger rows 27/28 (**no canonical `T` terminates there**) |
| Decision blocked | **T-03, T-04, T-08, T-09, T-10, T-15, T-16, T-18** |
| Multiple defensible options | **T-09, T-12, T-14** (class 8 with ≥2 candidates) |

**N1 — Did any scenario give the platform preference because the pack contains more platform knowledge?**
**NO.** The decisive test is **T-16**: the pack's platform knowledge is by far its richest, and the
scenario still terminates at *decision blocked in every class, `ALT-004` included*, because no fit
assessment of an agent surface exists anywhere. T-01 is the second test: the commonest engagement shape
there is lands on *an alternative is sufficient and the platform is not excluded*, not on the platform.

**N2 — Did any scenario infer comparator superiority merely from platform exclusion?**
**NO.** Every exclusion terminal (T-04, T-07, T-08, T-09, T-10, T-12, T-13, T-14) carries
`COMPARATIVE FIT UNEVALUATED` / `COMPARATOR EVIDENCE ABSENT` inside the outcome string. T-13's
single-candidate set is explicitly labelled **scope narrowing, not evaluation**.

**N3 — Did any scenario begin with platform architecture branches as the option space?**
**NO.** S1 generates **option classes**; architecture shapes are reachable only *after* an outcome
establishes that a solution containing the platform remains viable.

**Asymmetry stated in both directions.** T-17 and T-05 state that the S7 gates make the code-first classes
unavailable more often — as a **documented capability gap in those classes**, never as an advantage of the
platform — while T-12 and T-10 state the converse, that classes with an existing funded operator gain a
**candidate** signal on the same criteria.

**Result: PASS.**

---

## 14. Defensibility

For every verdict, a senior reviewer can identify the evidence that caused it.

| Scenario | Decisive evidence | Grade | Concern | Scope | Economics | Comparator | Proof requirement |
|---|---|---|---|---|---|---|---|
| T-01 | single team, no integration, seeded entitlement | Confirmed | C1 | `[W]` | seeded | none asserted | V1 |
| T-02 | 40k rows, routine contention, field visibility | Confirmed | C4 | `[W]` | premium priced | none | V1/V2 |
| T-03 | integration ownership unknown; recovery unknown | Unknown | C5/C9/C10 | `[W]`+`[R]` | managed chain priced | incumbent unevaluated | V2–V4 |
| T-04 | freshness expectation vs documented floor | **Assumed → blocked** | C3/C9 | `[R]` | metering unit | absent | V2 |
| T-05 | 4,000/min peak; 20× ceiling conflict | Confirmed / **Conflicted** | C5/C9 | `[R]` | broker + gateway cost | absent | V3 |
| T-06 | 40 entities, field security, 7-year retention, board reporting | Confirmed | C4/C6 | `[W]`+`[R]` | audit capacity | `ALT-011` unassessed | V2 |
| T-07 | 200 ms end-to-end, transactionally visible | Confirmed | C2/C9 | `[W]` | — | absent | V3 |
| T-08 | regime clause unread; key vs audit conflict | **Unknown / Conflicted** | C6/C7 | `[W]` | control population | category only | V4 |
| T-09 | committed 15-min cross-region RTO, no drill | **Unknown** | C9/C10 | `[R]` | storage doubling | absent | V4 |
| T-10 | default estate, non-solution artefacts, maker gone | Confirmed (+ ownership Unknown) | C7/C8/C10 | `[W]` | 1,400-user census | first to assess | V2 |
| T-11 | specialised compute at one step; operator exists | Confirmed | C2/C10 | `[R]` | external consumption | none | V2 |
| T-12 | published integration contract exists | **Confirmed** | C5 | `[R]` | lead time as constraint | **incumbent unevaluated** | V1/V2 |
| T-13 | branded push, offline conflict rules, public API, 400k | Confirmed ×4 | C3 | `[W]` | `Xe` corroboration | absent | V2 |
| T-14 | 9,000 users × low frequency; isolation mandate | Confirmed (budget Unknown) | C11 | `[E]` | **ten dimensions** | absent | V1 |
| T-15 | nothing specified | Unknown | all | — | — | — | — |
| T-16 | no fit assessment exists in any class | **Unknown (never looked)** | C3/C6/C7/C11 | `[W]` | unmodellable | absent in all classes | pilot |
| T-17 | 90–120-day process; nothing external proposed | Confirmed | C2 | `[W]` | in-platform | gap stated on both sides | V1 |
| T-18 | shared-identity facade; propagation unknown | **Unknown** | C6 | `[R]` | — | — | V2 |

Every PASS verdict exposes decisive evidence, its grade, the decisive concern, disqualifier scope,
preconditions, uncertainty, economic reason, comparator status and the proof requirement — as
**traceable reasoning**, not prose.

**Result: PASS.**

---

## 15. Context-efficiency observation

*Observation only — no simplification was performed, and no decision behaviour was altered.*

| Question | Finding |
|---|---|
| Were the 10 stages easy to follow? | **Yes.** S0–S3 are cheap and terminated three scenarios outright (T-15 at S3; T-16 at S1+S3; T-01 barely engaged S5–S8). The stage names carry their own job description, so no lookup was needed to know what a stage was for |
| Were stages skipped legitimately? | **Yes, and often.** T-15 never reached S4–S9 in substance; T-16 could not; T-07 gained nothing from S6–S8 once the whole-path absolute fired at S2; T-17 needed no S8 depth. Early termination behaved as the procedure permits |
| Did stage-local registers prevent unnecessary loading? | **Yes.** T-01 needed S1 and S9 only; the volatility register was opened in exactly four scenarios (T-04, T-05, T-14, T-16) and never walked. The absence of a router meant no lookup step preceded any read |
| Did the 436-line spine materially help, or produce ceremony? | **Materially helped, in three identifiable places.** (a) The **non-commutative ordering** is what prevents T-09's optimistic answer (offline before recovery). (b) §3's `Ri`/`Cf` classes are what make T-17 and T-18 structurally unable to emit an exclusion. (c) §4's evidence-grade table is what forces T-04/T-08/T-09/T-10 to block first |
| Where does ceremony appear? | **One place: S6.** *"Run the registered rows explicitly"* is uniform regardless of materiality, so a scenario like T-01 pays twelve conjunction checks to record *no row's participating conditions hold*. The cost is one output line and each row fails on its first condition, so it is cheap — but it is the single stage whose depth is not proportional. **This is by design** (the rows are invisible to per-concern reading, which is why they must be run rather than hoped for), and it is recorded, not repaired |
| Fixed per-round cost | The twelve-line concern-coverage summary. Mitigated by D0/D1 one-liners; a five-candidate engagement produces roughly sixty assessments of which most are one line, as §7.5 predicts |

**No genuine context-efficiency problem was found.** The spine reads as a light framework carrying
non-lightweight reasoning.

---

## 16. Findings and classification

**No scenario failed.** Four non-terminal findings were recorded during the replay. None changes a
terminal, none is class A, C or D, and **no runtime file was modified**.

| # | Finding | Class | Terminal effect | Smallest bounded repair (NOT applied) |
|---|---|---|---|---|
| **F-1** | Spine §7.2 note 2 reads *"only a `decisivo` swing, **or membership of the blocking set**, escalates to decision blocked"* without qualification, while `blocking-set.md` §0 governs with *"for each entry **engaged by the engagement**"*. Read unqualified, T-01 and T-02 would over-block on `B-17` (support and operational ownership) even though `CD-02` cannot fire because no pattern requires an external component | **B — authored ambiguity** | **None.** The owning register's governing rule resolves it, and `B-01`'s own resolution column keeps fit outcomes open at a low criticality class | Six words in spine §7.2: *"or membership of the blocking set **where the entry is engaged**"* |
| **F-2** | The trigger→candidate map has no row whose dominant requirement is *freshness below the documented external-site floor*, which is T-04's decisive axis. `ALT-005`/`ALT-011` are reached via rows 18 and 26 plus S9's re-read of the register | **B — authored coverage thinness** | **None.** The same candidate classes are named, and the canonical terminal is reached for the canonical reason | Authoring feedback for a later map revision; **not** a runtime change, since adding rows to make a scenario resolve is the invention failure mode |
| **F-3** | `CD-01`, `CD-07`, `CD-08`, `CD-12`, outcome class **9** (deployment model), class **10** and class **11** are **not exercised** by any canonical `T` scenario | **Not a failure — canonical corpus coverage** | None. Step 3A §20 already records that classes 10 and 11 have no dedicated canonical scenario | None. Recorded so a future scenario commission knows where the corpus is silent |
| **F-4** | §7.1(b) — *a candidate not generated at S1 because no requirement triggers it* — means class **1** (strong fit) is reachable for `ALT-004` only where a trigger row fires, so T-01 lands on class 13 form (a) rather than class 1 | **Not a failure — intended neutrality behaviour** | None. Canonical T-01 admits both, and the canonical repair note endorses the class-13 branch precisely because the alternative biases toward the platform on the commonest engagement shape | None |

**Class A (implementation defect): 0. Class C (canonical inconsistency): 0. Class D (research gap): 0.**

**One point deserving explicit non-conflict treatment.** The canonical T-14 body renders class 7 as the
disjunction *"ECONOMICALLY UNATTRACTIVE OR INFEASIBLE"*, while the runtime renders one resolved subtype.
This is **not** a canonical inconsistency: Step 3A §16.4 (approved) mandates the discriminator, Step 3A
§20 scenario 11 states T-14 must render *"7, with its subtype"*, and this gate's own §11 requires it.
The **class** is unchanged; only the sentence is sharpened, in the direction the design authority
specifies.

---

## 17. Final verdict

All eighteen canonical scenarios were replayed against the exact Step 3B1 runtime, in one pass, with no
runtime modification at any point. Every terminal matched its canonical expectation and, in each case,
matched it **for the canonical reason**. The four carry-forward regressions — migration (`T-10`),
agentic (`T-16`), in-platform redirect (`T-17`), composed authorization (`T-18`) — all pass, as do the
evidence-grade, scope-pair, class-7, comparator, reachability, D0/gap, C10, cross-domain, volatility,
neutrality and defensibility gates.

No score exists anywhere in the model, and no scenario privileged the active pack's own technology.

---

`STEP 3B2 — OPTIONS RUNTIME BEHAVIOUR GATE: PASS`
`CANONICAL SCENARIOS REPLAYED: 18/18`
`TERMINAL MISMATCHES: 0`
`EVIDENCE-GRADE REGRESSION: PASS`
`RI REGRESSION T-17: PASS`
`XC REGRESSION T-18: PASS`
`MIGRATION REGRESSION T-10: PASS`
`SCOPE-PAIR REGRESSION: PASS`
`CLASS-7 SEMANTICS: PASS`
`COMPARATOR DISCIPLINE: PASS`
`REACHABILITY FLOOR: PASS`
`D0 VS EVIDENCE-GAP: PASS`
`C10 OPERABILITY PATH: PASS`
`CROSS-DOMAIN REASONING: PASS`
`VOLATILE-FACT HANDLING: PASS`
`PP STRUCTURAL PREFERENCE DETECTED: NO`
`WEIGHTED SCORING DETECTED: NO`
`UNRESOLVED CANONICAL INCONSISTENCIES: 0`
`RUNTIME MODIFIED DURING INITIAL REPLAY: NO`
`OPTIONS MODEL DEFENSIBLE: YES`
`READY TO CLOSE STEP 3 — OPTIONS LAYER: YES`

---

## 18. Closure note — Step 3 final freeze repair (2026-09-04, post-gate)

**F-1 repaired.** The spine's D0/evidence-gap escalation clause (§7.2 note 2) now carries the
engaged-entry qualification, so the binding semantics are `entry exists in the blocking set` **≠**
`entry is engaged by this engagement`. A blocking entry whose applicability conditions are not engaged
by the actual evidence creates **no `Unknown` merely because the entry exists**, and therefore **no
decision blocked** — the T-01/T-02 `B-17` case the gate identified. The clause now reads *"only a
`decisivo` swing, or membership of the blocking set **where the entry is engaged by the engagement**,
escalates to decision blocked — presence in the register is not engagement
(`decision-model/blocking-set.md` §0)"*.

**Exact file changed.** `library/packs/pp/decision-tree.md` — §7.2 note 2, one clause. Nothing else in
the section was rewritten. No register was touched. Applied out-of-band per
`.claude/rules/library-readonly.md`.

**Targeted test.** `.claude/tests/test_pp_options_decision_model.py` →
`TestSpine.test_blocking_set_membership_alone_does_not_block`, asserting (a) the engaged-entry
qualification is present, (b) *presence in the register is not engagement* is stated, (c) the
unqualified form no longer appears anywhere in the spine, (d) the owning register is cited. **Suite:
94 tests, OK** (was 93). Regression: Phase G 22 · Phase E 31 · Phase D 23 · scaffold 15 · kernel tools
23 — **all OK**.

**No decision semantics changed.** The repair removes an ambiguity between the spine's escalation clause
and `blocking-set.md` §0's governing rule. The replay already executed under the register's qualified
reading, which is why F-1 was recorded as non-terminal in §16. **The 18/18 result with 0 terminal
mismatches remains authoritative** and was not re-run.

**Carried forward unchanged.** **F-2** — trigger-map thinness around external-site freshness; no trigger
row was added, since adding one to make a scenario cleaner is the invention failure mode. **F-3** —
`CD-01`, `CD-07`, `CD-08`, `CD-12` and outcome classes 9, 10, 11 are unexercised by the canonical
scenario corpus; this is scenario-corpus coverage feedback, not a runtime defect. **F-4** — T-01
reaching class 13 form (a) rather than class 1 is intended neutrality behaviour and was not altered.

**STEP 3 — OPTIONS LAYER: FROZEN.**
