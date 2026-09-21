# Step 5C — Architecture Semantic / Behavioural Gate Report

<!--
provenance: AUTHORING (semantic gate) · Step 5C
authored: 2026-09-04
basis: step-5a-architecture-template-model.md (FROZEN, incl. §27, §28) ·
       step-5b-architecture-template-implementation-report.md (PASS / CLOSED)
No new research. No web access. No canonical research modified. No runtime modified during the initial
gate. Step 3 not reopened. Step 4 not reopened. Step 6 deliverable templates not migrated.
-->

## 1. Gate basis

Step 5B proved the model is **representable and mechanically enforceable** (365 structural tests). This
gate proves the resulting architecture reasoning is **defensible**: that frozen decisions become
materially complete, epistemically honest architecture descriptions without re-deciding Options,
inventing the far side, losing imported obligations, forcing a user surface, or loading Domain Knowledge
indiscriminately.

### 1.1 Runtime under test

| Unit | Role |
|---|---|
| `library/packs/pp/architecture-templates/README.md` | positioning · reachability table (single home) · architectability boundary · experience semantics · headless semantics · legacy read |
| `.../architecture-core.md` | fixed entry point · A1–A3 + A5–A12 · 8 conditional sections · render contract |
| `.../fragment-experience-internal.md` | `owned-internal` |
| `.../fragment-experience-external.md` | `owned-external` |
| `.../fragment-experience-inherited.md` | `inherited` |
| `.../fragment-boundary-and-imports.md` | repeatable · six import channels |
| `.claude/skills/aisa-blueprint/SKILL.md` | entry gate · architecture authoring · iteration · pull discipline |
| `.claude/skills/aisa-render/SKILL.md` | fixed entry point · fragment resolution · four gap classes |
| `.claude/skills/aisa-synthesize/SKILL.md` + `library/kernel/synthesis-templates/architecture-story.template.md` | architecture narrative |
| `library/kernel/blueprint-contract.md`, `library/kernel/render-contract.md` | generic contracts |
| Step 3 `decision-model/outcome-classes.md`, `blocking-set.md`, `volatility-register.md` | upstream authority (read only) |
| Step 4 `domain-knowledge/**` | pulled selectively per fixture |

The three unmigrated Step 6 deliverable templates (`solution-blueprint`, `implementation-spec`,
`claude-design-brief`) were **not** used as the architecture renderer. The Architecture Layer was tested
directly. §20 of this report records the check that the layer does not depend on them.

### 1.2 Behavioural path exercised

```text
frozen engagement evidence + frozen (scope, outcome) pair + frozen selected solution
  → blueprint entry gate
  → outcome reachability × pack architectability
  → authorized PP scope(s)
  → architecture work → selective Domain Knowledge pulls
  → architecture record
  → core + 0..1 experience fragment + 0..N boundary/import fragments
  → epistemically honest architecture output
```

No Options re-run occurred in any fixture. No fixture produced a new outcome class, an option comparison
or a comparator claim.

---

## 2. Fixture corpus

All 19 frozen Step 5A §23 fixtures were replayed behaviourally against realistic synthetic engagement
evidence. Evidence states business and technical requirements; **no fixture's evidence embeds the
expected answer as a fact** — the answer had to be reasoned.

| Id | Synthetic engagement | Frozen selected solution | Frozen `(scope, outcome)` |
|---|---|---|---|
| F-1 | 12-person team logs equipment-loan requests in a shared spreadsheet; one flat list + 2 lookups; list-level read; low write concurrency; ~200 rows/yr; no external audience; no audit requirement | collaboration-platform list with its customised form | (equipment-loan tracking, **13(a)**) |
| F-2 | 45 field technicians log site inspections on tablets; photo capture; today in Excel on a share; no personal data beyond technician name; versioning accepted in place of audit (governance owner, funded); one supervisor approval; 6k/yr | PP canvas app over the list/library store | (site-inspection logging, **2**) |
| F-3 | HR case management, 180 users, sensitive personal data, per-owner row access, salary column restricted, 7-year audit legally required, EU residency Confirmed | PP record-centric app over the governed relational store, managed environment | (HR case management, **1**) |
| F-4 | 30 planners; production records must remain in the existing on-premises SQL instance (residency + DBA ownership Confirmed); private-network only, no public endpoint | PP canvas app over relational-via-connector through the on-premises gateway | (production scheduling, **2**) |
| F-5 | 4,000 external contractors submit compliance declarations; not in the directory; public-sector accessibility conformance required; PT+EN; no anonymous access | PP external-audience site, low-code build model, over the governed relational store | (contractor declarations, **2**) |
| F-6 | The F-3 application plus cross-year trend reporting; a measurement Confirms the operational store cannot serve the reporting query volume; BI team owns reporting | PP application + a replicated analytical copy | (case management, **2**) · (analytical copy, **2**) |
| F-7 | Three consumer classes (PP app, portal, batch job) need the same ERP pricing capability; the contract changes quarterly (Confirmed); the ERP must be rate-protected | PP application + a mediated API tier | (pricing consumption, **2**) |
| F-8 | Inspection photos must be OCR'd and matched to an asset register; OCR is algorithm-heavy beyond the expression tier (Confirmed); arrival is spiky (Confirmed peak); **Confirmed: no team owns non-platform compute** | PP application + queue + external worker + asset-register read | (inspection enrichment, **2**) |
| F-9 | Contract reference data owned by a legal system must appear as native tables, read-only; table-level authorization sufficient (Confirmed); no audit on that data (Confirmed); upstream loads nightly (Confirmed) | PP record-centric app with the legal system virtualized | (contract reference access, **2**) |
| F-10 | Field-service app; outbound regulator notifications need durability, ordering and dead-lettering the platform mechanisms cannot meet (Confirmed); cloud-native team, support model, skills, cross-boundary release owner and GA maturity all named | PP application, notification delivery relocated to cloud-native services | (field-service application, **2**) · (regulator notification delivery, **3**) |
| F-11 | Purchase-requisition experience on PP; the incumbent ERP keeps the requisition record and the posting; PP supplies experience and human workflow | PP experience + incumbent authority | (requisition experience, **2**) · (requisition authority + posting, **4**) |
| F-12 | Training records; per-manager row access; no column security; no audit beyond versioning; 900 users; moderate volume. **Both** the governed relational store and relational-via-connector to the corporate SQL satisfy every documented constraint; the data-ownership decision and the entitlement funding are unsettled | PP application; record authority unsettled | (training records, **2**) |
| F-13 | A partner-facing solution the organization intends to **resell**; multi-tenant / resale licensing is an unclosed gap in the pack's evidence (scope-blocker) | none — no solution selected | (partner-facing solution, **12**) |
| F-14 | A public consumer mobile application requiring push notifications and a consumer audience | none — candidate set | (consumer mobile application, **5**) → **8** |
| F-15 | Nightly reconciliation of supplier master data between two systems of record; no human interaction; scheduled 02:00; reruns expected so it must be idempotent; must survive restart; failures reach the named Integration Ops rota; only execution state is retained | PP automation-only solution (no application surface) | (supplier master reconciliation, **2**) |
| F-16 | Inbound order messages arrive in bursts; each must be validated (schema-heavy, needs a library the expression tier lacks — Confirmed), enriched from a pricing service, and posted to the ERP; nothing may be lost; poison messages quarantined; **no human surface**; Integration Team owns broker, worker and API | PP headless composed integration | (order intake, **2**) |
| F-17a | Partner settlement platform; the Options round selected a **packaged / SaaS settlement product**; conditions funded and owned | packaged / SaaS product | (partner settlement, **2**) |
| F-17b | Same scope, variant: the Options round selected a **custom-only build** (product-grade public API surface, published availability commitments, custom conflict rules) | custom-only build | (partner settlement, **1**) |
| F-18 | Signed policy circulation where *the document is the record*; the documented answer is the collaboration platform's document library with its native approval and retention; **no PP artefact is introduced** | native document library + native approval | (policy circulation, **13(a)**) |
| F-19 | Two mediated integrations — ERP order status and CRM contact — both `api-mediated`, both owned by the Integration Team, both forced by the same requirement class | PP application + two mediated APIs | (order & contact consumption, **2**) |

---

## 3. Per-fixture replay

Notation: `auth` = `architecture.authorization`; `N/M` = unique qualifying composition components /
unique relocated responsibilities; `frag` = boundary/import fragment instances; `exp` = experience
fragments rendered. `DK` counts distinct RESEARCH unit pull events; `CRAFT` counts CRAFT units consumed.

### F-1 — inherited, architectable class 13(a) · PASS

- **Reachability** reachable (13(a), never automatic). **Architectability** TRUE — a native/inherited
  capability the pack explicitly covers (`application-surfaces.md` §3 *Embedded surfaces —
  list-customised form*). `architectability_basis`: *"The sufficient capability is a PP-covered inherited
  surface over the list store; the pack has the authority and the evidence to architect it."*
- **auth** `authorized` · scope: equipment-loan tracking.
- **exp** `inherited` · `primary_surface: list-customised form` · 1 experience fragment.
- **record_authority** 1 domain — equipment-loan requests · list/library store · `owned`.
- **compositions** `[]` (no integration stream). **N/M** 0/0 → **frag 0**. Invariant holds.
- **A4 (fragment)** host = the team's collaboration site list; access is inherited from list read access
  and **not administered by this solution** (the site owner administers it, by role); the customised form
  **cannot be shared manually at all**; no independent lifecycle — the workflow lives and dies with the
  list, and anyone with list-design rights can rename, move or delete it without consulting the workflow
  owner.
- **A4.3 ceiling** no engagement-verified row exists ⇒ rendered as a **verification obligation** (*what
  to measure: sustained row count and concurrent-editor count on the request list; owner: IT ops;
  fidelity: production counter read; by: before the next review*). No template number and no remembered
  figure was substituted. Re-verify pointer `VC-07`.
- **A4.4 graduation trigger** (mandatory, present): *"when more than one person edits the request list in
  the same working hour — list-level write concurrency is exceeded — or when any field must be hidden
  from a list reader, which list-level security cannot express."* Stated as a **one-way graduation**;
  **when** to graduate is not decided here.
- **A8 (inherited form)** no independent environment, policy plane or release topology exists — stated as
  a **choice** with named accepted consequences (no environment separation, no governed release route, no
  policy at this solution's own boundary, no independent recovery), each with an owner.
- **Non-exclusion** the 13(a) sentence is reproduced verbatim, including *"No documented constraint
  excludes the platform"*. The fragment makes no exclusion claim.
- **Epistemics** Confirmed (team size, volume, no audit requirement) with `verificado_em`; Assumed (write
  concurrency stays low) carried as Assumed in A12 and never promoted; Unknown → the ceiling
  verification.
- **Proof obligations** 1: *the list holds three years of requests at the stated volume — V2 —
  production counter read — IT ops — funded: yes*. Carried, not re-graded.
- **DK** 8 pulls / 7 sections; max 2 (A4: `application-surfaces` then `data/sharepoint` — the second pull
  is forced because the first exposes the host store's own ceiling as a material dependency).
  **CRAFT** 1 (`delivery-conventions`, naming only).
- **Open architecture choices** 0 structural. **Approval possible: yes.**

### F-2 — owned-internal over the list store, direct · PASS

- **auth** `authorized`; class-2 sentence verbatim. **exp** `owned-internal` · `canvas app` · 1 fragment.
- **record_authority** 1 domain · list/library store · `owned`. Forfeits recorded as accepted
  consequences with ids: no column security, no multi-row atomicity, **versioning is not audit**.
- **compositions** 1 × `direct`, `in-platform`, `forced_by`: *"no requirement forces escalation — one
  consumer class, no contract volatility, no delivery guarantee"*. **N/M** 0/0 → **frag 0** (a `direct`
  in-platform composition imports nothing). Invariant holds.
- **Conditions carried** as *condition — owner — funded? — by when*: *"versioning accepted in place of an
  audit trail — Governance owner — funded: yes (no cost) — confirmed 2026-08-14."* Not a silent
  assumption.
- **A4.5 offline** `not applicable — sem requisito de offline registado`; the underlying **Assumed** row
  (*sites have coverage*) is carried in A12 as Assumed with its basis and validity — **not** promoted to
  a Confirmed *no offline needed*.
- **A4.3 delegation-safe paths** the inspection-history search path is named non-delegable against the
  list store; the architectural consequence (a server-side pre-filter by technician and month, so the
  client never issues an unfiltered query) is stated; the limit itself is cited to
  `data/query-and-delegation.md`, not restated.
- **Epistemics** Confirmed ×4, Assumed ×1, Risky ×1 (accepted: no audit trail, id carried from the
  D-NNN).
- **DK** 10 / 9; max 2 (A5: `store-boundaries` → `data/sharepoint`, forced by the versioning-not-audit
  forfeit). **CRAFT** 4 (`screen-consolidation-rules`, `screen-patterns`, `security-craft`,
  `delivery-conventions`).
- **Approval possible: yes.**

### F-3 — owned-internal over the governed store, class 1 · PASS

- **auth** `authorized`; the class-1 sentence renders as *no documented constraint violated*, explicitly
  **not** as endorsement.
- **exp** `owned-internal` · `record-centric app` · 1 fragment. **record_authority** 1 · governed
  relational store · `owned`.
- **compositions** 1 × `direct`, `in-platform`. **N/M** 0/0 → **frag 0**.
- **A9 irreversible** populated: publisher and prefix; region and residency fixed at environment
  creation; ownership type (managed solution in production); first-party application installation;
  control generation. Each line states what is fixed, when it is fixed, and the exit cost.
- **A11** entitlement class per audience and the managed-environment licence chain surfaced **without a
  price** — drivers only. Entitlement fit is itself volatile (`VC-05`) and, with no verified engagement
  row, renders as a verification obligation.
- **A7** row and column security and audit are inherited from the store; the enforcement plane is the
  store, not the app; `security-craft` shaped only the **form** of the visibility matrix.
- **DK** 10 / 9; max 2 (A5: `store-boundaries` → `data/dataverse`, forced — column security and audit
  exist only there; A8: `governance-and-environments` → `alm/release-and-lifecycle`, forced — the
  managed-only production route). **CRAFT** 4.
- **Approval possible: yes.**

### F-4 — owned-internal over relational-via-connector + gateway · PASS

- **auth** `authorized`. **exp** `owned-internal` · `canvas app` · 1 fragment.
- **record_authority** 1 · relational via connector · `keep-in-place`.
- **compositions** 1 · `component: onprem-sql-gateway-path` · `direct` · **`boundary:
  outside-platform`** · `forced_by`: *"the production records must remain in the on-premises instance
  (Confirmed)"* · `owner: Infrastructure`. **N/M** 1/0 → **frag 1**. Invariant holds.
- **A7 identity-model difference** (the fixture's point): the gateway **uses the stored credential
  regardless of the user**, so no per-user identity reaches the database on that path; only the
  directory-integrated connection carries one, and guest identities are unsupported there; and
  **app-side filtering is not authorization**. The enforcement point is therefore SQL-side views per role
  (Confirmed) — recorded as the authorization enforcement point, not as a UI concern.
- **A3 private-network mutual exclusion** stated: the private path and the on-premises gateway are
  **mutually exclusive**, and the private path's preconditions are irreversible in practice. Cited to
  `data/azure-sql.md`; its address-allocation and cluster-count figures are **not** carried into the
  architecture.
- **Six channels** all populated — Governance: the gateway estate and the database sit outside platform
  governance, the DBA classifies, and platform data policy governs the connector and not the database ·
  ALM: two release routes, connection re-binding, and the network posture versioned as an irreversible
  precondition · Cost: gateway nodes with separate development and production clusters plus patching
  labour, and gateway-at-scale cost is an **open item** (`VC-08`) · Monitoring: gateway health, and
  because the vendor does not investigate performance on an overloaded gateway the correlation must be
  generated locally · Recovery: the gateway recovery key is a named business risk — without it gateways
  cannot be recovered — restore order database → gateway → re-bind connection, DBA reconciles ·
  Operator: Infrastructure, named.
- **DK** 11 / 10; max 2 (A5: `store-boundaries` → `data/azure-sql`, forced — the connector identity model
  and the gateway are the contested boundary). **CRAFT** 5 (adds `sql-delivery-conventions` for layering
  and naming only).
- **Approval possible: yes.**

### F-5 — owned-external, low-code build model · PASS

- **auth** `authorized`. **exp** `owned-external` · `external-audience site — low-code build model` ·
  1 fragment.
- **A4.1 prerequisite** the external audience is a **recorded fact** with `su_refs`, not decided here.
- **A4.2 external identity provider** rendered as a **prerequisite with three consequences**: a tenant
  the organization must own, its own cost, and its own operating burden — with a named owner (IT identity
  team) and Confirmed funding. Had either been unnamed, the fragment requires a `structural: true` open
  choice; that negative branch is exercised in F-12.
- **A4.4 authorization form** deny-by-default stated explicitly — nothing is reachable until a permission
  grants it — with the record permission model crossed against the audience's web-facing roles per
  segment.
- **A4.5 anonymous exposure** `not applicable — sem exposição anónima em âmbito`, as a recorded decision
  rather than an inherited default.
- **A4.6 cache/freshness** the architectural commitment is stated: a write made outside the site is
  **never guaranteed to be immediately visible on it**, and content caching applies to anonymous traffic
  only, so authenticated declaration pages are uncached. Reads that tolerate staleness (published
  guidance) are separated from reads that do not (a contractor's own submission status), and the user is
  shown the submission's server-side state rather than a cached list.
- **A4.7 accessibility** the platform-attested conformance basis is cited, and the **customisation added
  is the organization's own accessibility responsibility**, with an attestation owner and date. An
  unattested claim would be an open architecture item, never a promoted assumption.
- **Volatile / Unknown** throughput, request-rate and concurrency ceilings for this surface are **not
  published** ⇒ Unknown preserved and a **V3 proof obligation** recorded (representative pilot at the
  declared peak, owner named, funded) rather than an invented figure.
- **compositions** `[]`. **N/M** 0/0 → **frag 0**.
- **DK** 8 / 7; max 2 (A4: `application-surfaces` → `governance-and-environments` §11, forced — the
  exposure and policy plane). **CRAFT** 1 (`security-craft`, form only).
- **Approval possible: yes.**

### F-6 — application + replicated analytical copy · PASS

- **auth** `authorized` for both scopes. **exp** `owned-internal` · `record-centric app` · 1 fragment.
- **record_authority** 2 entries: operational cases (governed relational store, `owned`) and the
  analytical copy (external analytical store, **`replicated`**).
- **compositions** 1 · `component: analytical-replication` · `data-replication` ·
  `boundary: outside-platform` · `forced_by`: *"the measured reporting query volume exceeds the
  operational store's serving envelope (Confirmed)"* · `owner: BI Team`. **N/M** 1/0 → **frag 1**.
- **Reconciliation owner** mandatory and **named** (BI data engineer). The documented three-component
  shape — event path, bulk path, reconciliation pass — is stated as the design, and a design without the
  reconciliation pass is recorded as divergent by construction.
- **Security does not travel into the copy** — A5 and A7 state that row and column security are **not**
  inherited by the copy, that classification, retention and erasure obligations now exist **twice**, and
  carry the documented mitigation *replicate the fields, not the record* as the design's own control.
- **Second cost meter** A11 and the fragment's Cost channel both carry it: storage, security and
  operations are paid twice plus sync execution, and selective replication is the named cost and risk
  control. **No prices.**
- **Six channels** all populated; Recovery carries the first-class failure mode explicitly —
  restore-induced divergence: pause writers, re-baseline, replay, reconcile, in that order.
- **Epistemics** Confirmed (the measurement), Assumed (change-rate profile), Risky (accepted: two truths
  in the window between the paths, with the D-NNN risk id).
- **DK** 11 / 10; max 2. **CRAFT** 4. **Approval possible: yes.**

### F-7 — application + mediated API tier · PASS

- **auth** `authorized`. **exp** `owned-internal` · 1 fragment.
- **compositions** 1 · `component: pricing-api` · `api-mediated` · `outside-platform` · `forced_by`:
  *"three consumer classes, quarterly contract volatility, and ERP rate protection (Confirmed)"* ·
  `owner: Integration Team`. **N/M** 1/0 → **frag 1**.
- **A2 intent** the escalation is justified by the named requirement and not by practice: the direct
  composition is the default and was left behind because three consumer classes and a quarterly contract
  change cannot be carried by it, and because this is the only documented place to rate-limit
  platform-side callers.
- **Six channels** Governance: the mediated API becomes a governed workload asset with a named owner, an
  API inventory, an access and policy baseline and budget attribution — and platform data policy
  **governs the connector, not the gateway or the backend** · ALM: **two supply chains**,
  contract-version compatibility against the platform release, controlled import order and reference
  rebinding · Cost: API runtime, telemetry, non-production instances and an operator (drivers only) ·
  Monitoring: gateway and backend telemetry into one queryable sink, a named API owner, and a release
  process separate from the platform solution · Recovery: both the API layer and the consumer contract ·
  Operator: an API owner **distinct from the maker**, named.
- **Epistemic honesty** whether calls through a mediation tier are metered differently is **not
  established**, so the architecture claims only **relocation of backend load** and never relief of the
  platform request meter. The single-point-of-failure risk carries load testing as its named mitigation
  and becomes a V2 proof obligation.
- **DK** 10 / 9; max 2 (fragment: `patterns` §3 + `api-mediated`, then `integration-mechanisms`, forced —
  the connector remains the contract chokepoint). **CRAFT** 4. **Approval possible: yes.**

### F-8 — application + queue + external worker, no named operator · PASS (approval correctly blocked)

- **auth** `authorized`. **exp** `owned-internal` · 1 fragment.
- **compositions** 3:
  1. `ocr-dispatch-queue` · `queue-based` · `outside-platform` · `forced_by`: *"spike absorption at the
     Confirmed peak, and poison-message quarantine for which no in-platform equivalent is documented"* ·
     **`owner: UNKNOWN`**
  2. `ocr-worker` · `hybrid-low-code-pro-code` · `outside-platform` · `forced_by`: *"the computation seam
     — algorithm-heavy OCR exceeds the expression tier (Confirmed)"* · **`owner: UNKNOWN`**
  3. `asset-register-read` · `direct` · `outside-platform` · `forced_by`: *"the asset register is
     authoritative elsewhere and is read per match"* · `owner: ERP Team`
- **N/M** 3/0 → **frag 3**. Invariant holds. Imports **accumulate and do not collapse**: the queue's
  channels (the broker as a governed asset with the message content now at rest in it; the message schema
  and the idempotency contract versioned; four new monitoring objects — queue depth, dead-letter depth,
  consumer lag, worker failures; replay-or-reconcile **before the queue is reopened**) are distinct from
  the hybrid's (two governance planes, two mandatory supply chains, platform entitlement **plus**
  external consumption, a correlation identifier across the seam, a recovery sequence spanning both
  estates), and both are distinct from the direct read's.
- **Operator availability** exposed as an **architecture capability fact**: *"the composition is
  unavailable because no operator exists"* — a statement about the design. Recorded as
  `open_architecture_choices[{structural: true}]`, **not** as a risk row and **not** as an accepted risk.
  The honest output the pattern unit prescribes is cross-referenced: the simpler composition
  (synchronous in-tier processing at reduced scope) **plus a tripwire** on the metric that would force
  the move (sustained arrival above the Confirmed in-tier envelope). The layer states none of that as its
  own judgement, and **names no operator**.
- **Blueprint production** proceeds; **approval is blocked** by the structural choice. No risk-only
  downgrade occurred. **Approval possible: no — correctly.**
- **Not-engaged channel** exactly one across the three instances: `asset-register-read` → Cost: *"not
  engaged — a read-only connector call on an existing entitlement introduces no new meter; the request
  consumption is already attributed to the acting identity's budget in A11."* Materially defensible.
- **DK** 12 / 10; max 2 (the fragment/operator responsibility: `patterns` §3 + the engaged composition,
  then `patterns` §7 — forced, because the first pull surfaced `owner: UNKNOWN` and §7 owns the honest
  output). **CRAFT** 4.

### F-9 — virtualized external system of record · PASS

- **auth** `authorized`. **exp** `owned-internal` · `record-centric app` · 1 fragment.
- **record_authority** 1 · external system of record · **`virtualized`**.
- **compositions** 1 · `component: contract-reference-virtual` · `data-virtualization` ·
  `outside-platform` · `forced_by`: *"the single source of truth must be preserved without a copy, and no
  item from the exclusion list is a requirement (Confirmed)"* · `owner: Legal Systems`. **N/M** 1/0 →
  **frag 1**.
- **A5 / A7 forfeits** stated as accepted consequences with ids: no field-level security; no row-level
  permissions and no source-side per-user validation; **no auditing**; no search; no offline caching; all
  attributes returned so the payload cannot be narrowed; virtual lookup columns cannot be filtered or
  sorted on. Each is checked against the requirement set, and each is confirmed non-required.
- **A9 irreversible** the **virtual-versus-standard modelling decision is irreversible in place**, so
  reversing it is a rebuild of the modelling layer and not a setting. Exit cost stated.
- **Risky** accepted with its id: **false freshness** — the query is real-time against a store loaded
  nightly, so a live-looking interface presents data up to a day old. The accepted-risk identity is
  carried in A10 and A12, and the mitigation (an explicit as-of stamp on the surface) is a design
  commitment.
- **Volatile / Unknown** no throughput or latency envelope is published for this composition ⇒ Unknown
  preserved plus a **V3 representative-pilot obligation**. The write-through variant is `not applicable`
  here (read-only) and its weak-evidence status is not carried as though it applied.
- **Six channels** all populated; ALM carries the decisive one — *the upstream schema is an external
  dependency that can break the application with no platform release* — and Monitoring carries the
  upstream load cadence as a watched cross-team dependency.
- **DK** 10 / 9; max 2. **CRAFT** 3. **Approval possible: yes.**

### F-10 — scope pair, class 3 · PASS

- **auth** `authorized-bounded`. A1 renders **both** pairs uncollapsed, each with its outcome sentence
  verbatim, and states which side is PP-owned and that the far side is not designed here.
- **exp** `owned-internal` · `canvas app` · 1 fragment.
- **compositions** 1 · `component: notification-handoff` · `queue-based` · `outside-platform` ·
  `forced_by`: *"the delivery guarantee is relocated (class 3); the hand-off itself must be durable"* ·
  `owner: Cloud Platform Team`.
- **relocated_responsibilities** 1 · `regulator-notification-delivery` · `owner: cloud-native services` ·
  `outcome_basis`: the class-3 sentence verbatim · `gates_recorded`: operator, support, skills,
  cross-boundary release owner, maturity — **all five present**.
- **N/M** 1/1 → **frag 2**. Both instances concern the **same far side** and are **not merged** — one is
  the PP-owned hand-off component, the other the relocated responsibility. Invariant holds.
- **The far side receives** boundary, owner, outcome basis, gates and imports, plus the fragment's
  explicit *"what this pack does not know about the other side"*: the cloud-native service's internals,
  its fit, its cost profile and its roadmap are recorded as **no evidence**. It receives **no** invented
  components, **no** data model, **no** technology naming, **no** operational model and **no** claimed
  suitability.
- **Scope-ownership table** engaged (two pairs): application → this platform → class-2 sentence →
  *yes, A4…A12*; regulator notification delivery → cloud-native services → class-3 sentence → *no — one
  boundary fragment instance*.
- **Diagram** one context sketch produced; every node is a boundary-table row; edges carry direction and
  mechanism class; the relocated responsibility is drawn outside the PP scope; **no fact exists only in
  the sketch**.
- **DK** 9 / 9; max 1. **CRAFT** 4. **Approval possible: yes** (all gates satisfied, no structural
  choice).

### F-11 — scope pair, class 4 · PASS

- **auth** `authorized-bounded`. Both pairs uncollapsed.
- **exp** `owned-internal` · 1 fragment. **record_authority** 1 · **external system of record** ·
  `keep-in-place` — the incumbent keeps authority.
- **compositions** 1 · `erp-requisition-api` · `api-mediated` · `outside-platform` · `forced_by`:
  *"the incumbent owns the requisition record; every write crosses its contract"* · `owner: ERP Team`.
- **relocated_responsibilities** 1 · `requisition-authority-and-posting` · `owner: incumbent system` ·
  `markers: [INCUMBENT FIT UNEVALUATED]` · gates recorded.
- **N/M** 1/1 → **frag 2**. Invariant holds.
- **`INCUMBENT FIT UNEVALUATED`** preserved **verbatim** in the fragment's markers row, in A1, in the
  scope-ownership table and in the synthesis narrative. It was **not** converted into *incumbent fit*,
  *incumbent poor fit*, or an incumbent architecture. The incumbent's internals remain **unmodelled**,
  and the fragment says so under *what this pack does not know*.
- **Not-engaged channel** one: the relocation's Cost channel — *"not engaged — the incumbent's licence
  and operating cost are pre-existing and unchanged by this decision; no new meter appears on the far
  side, and no comparative cost claim is available."* Materially defensible and comparator-neutral.
- **Monitoring** carries the consequence honestly: the incumbent's telemetry is not accessible to this
  pack (Unknown), so the **PP side must generate the correlation itself** — a design obligation, not an
  inference about the incumbent.
- **DK** 10 / 9; max 1. **CRAFT** 4. **Approval possible: yes.**

### F-12 — two defensible architectures in one authorized scope · PASS (approval correctly blocked)

- **auth** `authorized`. **exp** `owned-internal` · 1 fragment.
- **record_authority NOT `[]`** and not silently defaulted. The domain is present with its authority
  undetermined, and the undetermined authority is carried as `open_architecture_choices[{choice: "record
  authority for training records — governed relational store versus relational-via-connector to the
  corporate SQL", structural: true, would_be_settled_by: "the data-ownership decision by the records
  owner plus the entitlement funding confirmation", su_ref: U-031}]`.
- **compositions** 1 × `direct`, `in-platform`. **N/M** 0/0 → **frag 0**.
- **Candidate-architectures conditional engaged**: both architectures rendered — each with its store
  role, access mode, forfeits, identity model and irreversible consequences — and **neither chosen**.
  **No scoring, no weighting, no template preference, no recommendation.** What would settle it is named.
- **Blueprint produced**; **approval blocked** by the structural choice. This is **architecture
  uncertainty**, and the fixture confirms it was **not** relabelled Step 3 `Decision Blocked`: no class
  12 appears anywhere, the class-2 authorization stands, and the decision record is untouched.
- **DK** A5 = `store-boundaries` (1) — renders the contest and that neither side is settled; the
  candidate section = `data/dataverse` (1) + `data/azure-sql` (2), one per contested candidate. **Max 2
  per section**, no third pull, no store survey. **CRAFT** 4.
- **Approval possible: no — correctly.**

### F-13 — class 12 decision blocked · PASS

- **Reachability** unreachable. **Architectability** also fails independently — *a candidate set with no
  selected architecture is not architectable* — and the two reasons are reported **separately**.
- **auth** `not-authorized`. **No blueprint artefact produced** (the kernel entry gate requires an
  authorization for at least one scope). **No architecture template read.** **No experience fragment.**
  **No boundary fragment.** **No `architecture work item`.**
- **What is rendered** the emitted class-12 sentence in full, including its **mandatory per-resolution
  outcome**: *"Decision blocked for the partner-facing solution. Evidence required: whether the tenant
  agreement permits resale of platform-based solutions — expected form: contractual clause — likely owner
  type: commercial / licensing. If it resolves to permitted the outcome is a candidate set; if to not
  permitted, excluded for this scope."*
- **Gap class** `decision-blocking` → nothing architectural rendered and the outcome sentence rendered
  instead; logged as a skip with the reason and **not** written to `render-gaps.md`.
- **No draft masquerading as final** — draft mode is pre-decision only and none was produced.
  Architecture did **not** "helpfully continue". **DK 0 pulls. CRAFT 0.**

### F-14 — class 5 excluded + class 8 candidate set · PASS

- **auth** `not-authorized` (outcome unreachable for that scope; no other scope carries an emitted pair).
- **No PP architecture.** Architecture-containing output **skipped with the reason** (`not applicable: no
  architecture authorization — the platform is excluded for this scope`), logged to `render-log.md`. The
  skip is **not** a render gap and does not appear in `render-gaps.md`.
- **No replacement PP option inferred** — the class-8 candidate set is reproduced as emitted (*custom
  development · packaged product · comparative fit `UNEVALUATED`, engagement assessment required*), and
  the architecture layer proposed no in-platform alternative.
- **DK 0 pulls** — notably, the layer did **not** re-open `application-surfaces.md` to re-verify the
  push-notification and consumer-audience exclusions; those facts are frozen in the outcome sentence and
  were read from `decisions.md`. Re-verifying them would have been re-deciding.

### F-15 — headless automation · PASS

- **auth** `authorized`. **exp `none`** · **`primary_surface: null`** · **0 experience fragments** ·
  **no A4** · no placeholder · no missing include · no `surface unresolved` · **no render gap**. Logged as
  `not applicable — arquitectura sem superfície humana (experience.mode: none)`. No attempt was made to
  resolve `fragment-experience-none.md`.
- **record_authority `[]` — the positive empty set**, with the affirmative rationale rendered verbatim:
  *"No persisted record authority introduced; the workflow acts on external authorities and retains only
  operational execution state."* Both systems of record remain authoritative elsewhere.
- **compositions** 1 · `reconciliation-run` · `background-processing` · `in-platform` · `forced_by`:
  *"the run exceeds the synchronous window and must survive restarts (Confirmed)"*. Beyond `direct` ⇒
  **qualifying despite being in-platform**. **N/M** 1/0 → **frag 1**.
- **Required reasoning chain, walked explicitly:**
  - *automation shape* — scheduled, batch over a bounded supplier set; dispatch by schedule, execution as
    a durable run, and a **status resource** (mandatory for this composition).
  - *state location* — no business record is created; the only persisted state is the run ledger (run id,
    per-record outcome, attempt count, error), which is operational, has a **lifecycle**, and needs a
    retention policy.
  - *unit of failure* — the individual supplier record, not the run: a failed record must not fail the
    run, and the run must be resumable at the record.
  - *retry / idempotency* — reruns are expected, so writes are keyed on the supplier's alternate key and
    are upserts; the idempotency contract is versioned with the flow; **checkpointing** is the documented
    resilience mechanism for the multi-step pass.
  - *identity* — the acting connection identity per system of record, with secret custody named; the
    request-rate budget is **per acting identity**, so an elastic retry storm on one identity relocates
    throttling rather than removing it.
  - *environment / release* — one production environment bound to the residency verdict; the release
    route is the managed solution; **a long-running instance may span a release**, so the status schema
    and callback semantics must stay compatible.
  - *operator* — Integration Ops, named, owns the status ledger and answers *"did it work?"*; recovery
    order is quiesce the schedule → restore the ledger → re-baseline against both sources → replay
    unresolved records → reconcile.
  - *proof obligation* — idempotency under rerun (V2 measurement, owner Integration Ops, funded);
    throughput at the Confirmed peak (V3 — see below).
- **A6 and A7 carry the architecture in full**; A5 is an affirmative empty set; A8, A9, A10, A11 and A12
  are all materially populated. **No screens, no personas, no navigation and no application lifecycle**
  were fabricated. Read end to end, nothing reads as a missing section.
- **Volatile values** three engaged: (i) the peak inbound rate is an **engagement-verified value** —
  *1,180 supplier records/hour · verificado_em 2026-08-20 · validade 90 dias · re-verificar quando a base
  de fornecedores variar >10%* (an engagement measurement, not a service figure); (ii) request rate per
  acting identity — no verified engagement row ⇒ **verification obligation**, `VC-04`; (iii) the
  per-mechanism throughput ceiling is the register's **live conflict** (`VC-01` / `VS-08`).
- **Conflicted handled correctly** — the per-mechanism ceiling carries **neither figure**; the conflict
  itself is rendered, and the sizing claim becomes a **V3** proof obligation (representative pilot at the
  verified peak) rather than a number on either side.
- **DK** 8 / 7; max 2 (A8: `governance-and-environments` → `alm/release-and-lifecycle`, forced — the
  release route for a surface-less solution). **CRAFT 0** — correctly: no screen work exists.
- **Approval possible: yes.**

### F-16 — headless composed integration · PASS

- **auth** `authorized`. **exp `none`** · **0 experience fragments** · no A4 · no gap.
- **record_authority** 1 · sales orders · **external system of record** · `keep-in-place` (the ERP), plus
  the operational execution state named as non-authoritative. Not an empty set and not invented.
- **compositions** 3, all `outside-platform`, **all owned by the same team** and **not collapsed**:
  1. `order-intake-queue` · `queue-based` · `forced_by`: *"burst absorption and poison-message
     quarantine, for which no in-platform equivalent is documented (Confirmed)"* ·
     `owner: Integration Team`
  2. `order-validation-worker` · `hybrid-low-code-pro-code` · `forced_by`: *"the computation/library seam
     — schema validation needs a library the expression tier lacks (Confirmed)"* ·
     `owner: Integration Team`
  3. `pricing-api` · `api-mediated` · `forced_by`: *"two consumer classes and a versioned pricing
     contract (Confirmed)"* · `owner: Integration Team`
- **N/M** 3/0 → **frag 3**. Invariant holds. **A shared owner did not merge them**, and the three did
  **not** collapse into one *external dependency*: each retains its own owner role, release route,
  monitoring consequence, recovery consequence, economic meter and governance boundary.
- **A7 service identity** rendered in full for a surface-less architecture: the worker uses a **managed
  identity**, which the connector path cannot, so the *no stored secrets* requirement is satisfied by
  relocating the credential-bearing leg; the broker is the trust boundary; the connector's connection
  identity is the enforcement point on the platform side. This is exactly the content A7 must carry
  without a human audience, and the section is **not** owned by any fragment.
- **Recovery ordering** understandable and stated once, across components: quiesce intake → restore the
  ERP-side consumer state → decide **replay or reconcile before the queue is reopened** → drain the
  dead-letter with its named owner → re-validate the pricing contract version. Named reconciler.
- **Operator and support obligations survive per component** and are not deduplicated away.
- **Diagram** one context sketch and one sequence sketch (an asynchronous path with a status resource
  exists); all nodes are boundary-table rows; no fact is diagram-only.
- **DK** 10 / 9; max 1 (three separate single-pattern pulls — `patterns` §3 was read once and each
  engaged composition pulled once; **no survey of the ten**). **CRAFT 0.**
- **Approval possible: yes.**

### F-17 — non-PP positive outcome · PASS (both variants)

**F-17a — packaged / SaaS, class 2.**
- **Outcome reachability** **reachable**. `authorization_basis` reproduces the class-2 sentence verbatim,
  including its funded, owned conditions.
- **Pack architectability** **FALSE**. `architectability_basis`: *"The selected solution is a packaged /
  SaaS settlement product. This pack has neither authority nor evidence over a packaged product's
  internal architecture, and the decision introduces no PP artefact."*
- **auth** `not-authorized`. **No PP architecture generated** — no core, no experience fragment, no
  boundary fragment, no template read.
- **The two reasons are preserved separately and legibly**: the outcome basis is positive and stated as
  positive; the architectability reason is a statement about **this pack's scope**, not about the
  solution's quality.
- **Forbidden behaviours all absent** — it was **not** converted into Decision Blocked (no class 12
  appears; the emitted class remains 2); it does **not** claim PP lost, and the output states explicitly
  that **no PP exclusion was emitted for this scope**; and **no comparator inference** was drawn in
  either direction.

**F-17b — custom-only, class 1.**
- Identical structure. `architectability_basis`: *"The selected solution is a custom-only build; the
  platform's connector estate, managed governance, configured row access and included authentication are
  not inherited, and no PP artefact exists to architect."*
- The class-1 sentence renders as *no documented constraint violated*, **not** as endorsement and **not**
  as evidence that PP was unsuitable.
- **DK 0 pulls. CRAFT 0.** **Approval: N/A — no blueprint.**

### F-18 — class 13(a) outside architecture authority · PASS

- **Outcome reachability** reachable, never automatic. **Pack architectability** **FALSE**:
  `architectability_basis`: *"The sufficient capability is the host platform's own document-library
  records and approval configuration. No PP application, automation, integration or inherited PP surface
  is introduced, so there is no PP artefact within this pack's architecture scope."*
- **auth** `not-authorized`. **No PP architecture.** Critically: **no inherited experience fragment was
  rendered.** This is the fixture's whole point, and it holds — class 13(a) does **not** secretly mean
  *render inherited PP architecture*. The contrast with F-1 (also 13(a), also inherited-shaped, but
  architectable because a PP-covered surface **is** introduced) is the discriminator, and it is the
  **architectability** test that separates them, not the outcome class.
- **All three mandatory preservations survive** in the decision and deliverable layers:
  1. *documented sufficiency* — reproduced verbatim, scoped to the seeded-entitlement fact alone, with
     **no comparative TCO asserted**;
  2. *"No documented constraint excludes the platform"* — reproduced verbatim;
  3. the **graduation trigger** — *"when circulation requires per-recipient status tracking with
     field-level restriction that the library cannot express"* — reproduced, and recorded as mandatory
     **either way**.
- **DK 0 pulls. CRAFT 0.** **Approval: N/A — no blueprint.**

### F-19 — repeated pattern, same owner · PASS (including the adversarial duplicate)

- **auth** `authorized`. **exp** `owned-internal` · 1 fragment.
- **compositions** 2, deliberately maximally similar — both `api-mediated`, both `outside-platform`, both
  `owner: Integration Team`, both with the same forcing-requirement class:
  - `erp-order-status-api` · `forced_by`: *"two consumer classes on order status, and a versioned ERP
    contract (Confirmed)"*
  - `crm-contact-api` · `forced_by`: *"two consumer classes on contact data, and a versioned CRM
    contract (Confirmed)"*
- **N/M** 2/0 → **frag 2**. Keys `<scope>::component::erp-order-status-api` and
  `<scope>::component::crm-contact-api`. **Not collapsed on the shared pattern-plus-owner.**
- **Six channels per instance, with materially different content** — a different governed asset and API
  inventory entry; a different contract to keep version-compatible; a different charged population
  (order-status polling volume versus contact-record reads); a different health signal and failure
  landing place; a different recovery participant (the ERP order pipeline versus the CRM master); and the
  same operator **role** but distinct escalation paths and on-call contracts. The two instances are not
  copies.
- **Adversarial duplicate** both entries renamed `integration-api`: the architecture contract **fails**.
  The layer refused to merge, refused to auto-suffix, refused to overwrite and refused to collapse the
  imports; it reported a contract defect and required distinct names. Behaviour matches the frozen rule
  exactly.
- **DK** 9 / 8; max 2 (the fragment pull is **per pattern, not per instance** — one `patterns` §3 +
  `api-mediated` pull served both instances, then `integration-mechanisms` as the forced second).
  **CRAFT** 4. **Approval possible: yes.**

### 3.1 Fixture verdict roll-up

| Fixture | auth | exp.mode | N/M | frag | structural open | approval | verdict |
|---|---|---|---:|---:|---:|---|---|
| F-1 | authorized | inherited | 0/0 | 0 | 0 | yes | **PASS** |
| F-2 | authorized | owned-internal | 0/0 | 0 | 0 | yes | **PASS** |
| F-3 | authorized | owned-internal | 0/0 | 0 | 0 | yes | **PASS** |
| F-4 | authorized | owned-internal | 1/0 | 1 | 0 | yes | **PASS** |
| F-5 | authorized | owned-external | 0/0 | 0 | 0 | yes | **PASS** |
| F-6 | authorized | owned-internal | 1/0 | 1 | 0 | yes | **PASS** |
| F-7 | authorized | owned-internal | 1/0 | 1 | 0 | yes | **PASS** |
| F-8 | authorized | owned-internal | 3/0 | 3 | 1 | **no** | **PASS** |
| F-9 | authorized | owned-internal | 1/0 | 1 | 0 | yes | **PASS** |
| F-10 | authorized-bounded | owned-internal | 1/1 | 2 | 0 | yes | **PASS** |
| F-11 | authorized-bounded | owned-internal | 1/1 | 2 | 0 | yes | **PASS** |
| F-12 | authorized | owned-internal | 0/0 | 0 | 1 | **no** | **PASS** |
| F-13 | not-authorized | — | — | — | — | n/a | **PASS** |
| F-14 | not-authorized | — | — | — | — | n/a | **PASS** |
| F-15 | authorized | **none** | 1/0 | 1 | 0 | yes | **PASS** |
| F-16 | authorized | **none** | 3/0 | 3 | 0 | yes | **PASS** |
| F-17a/b | not-authorized | — | — | — | — | n/a | **PASS** |
| F-18 | not-authorized | — | — | — | — | n/a | **PASS** |
| F-19 | authorized | owned-internal | 2/0 | 2 | 0 | yes | **PASS** |

**19/19 executed. 0 fixture failures.**
---

## 4. Authorization / architectability

### 4.1 The entry-gate gate — `outcome reachable ≠ PP architecture authorized`

The corpus contains four fixtures where the outcome is reachable and the architecture is nevertheless
**not** authorized, and none where a reachable outcome alone produced an architecture.

| Fixture | Outcome reachable? | Architectable? | Authorization | Architecture produced? |
|---|---|---|---|---|
| F-1 | yes (13(a)) | **yes** | authorized | yes |
| F-17a | **yes** (class 2) | **no** — packaged / SaaS | not-authorized | **no** |
| F-17b | **yes** (class 1) | **no** — custom-only | not-authorized | **no** |
| F-18 | **yes** (13(a)) | **no** — host-platform capability, no PP artefact | not-authorized | **no** |
| F-13 | no (class 12) | no (no selected architecture) | not-authorized | **no** |
| F-14 | no (class 5) | n/a — no selected PP architecture | not-authorized | **no** |
| F-10, F-11 | yes, bounded (3 / 4) | **PP side only** | authorized-bounded | PP side only |

The multiplication is real, not decorative: F-17 and F-18 differ from F-1 **only** on the second factor,
and the second factor alone changed the result. The gate is a gate.

### 4.2 Both factors required, and never merged

Every `not-authorized` output in the corpus carried the two reasons **separately and in that order**:
first the emitted outcome sentence verbatim (the outcome basis), then a one-sentence
`architectability_basis` about **this pack's scope**. No output merged them, no output implied the
positive outcome was in doubt, and no output relabelled either as *Decision Blocked*.

### 4.3 Authorization was read, never derived

- `aisa-decide` emitted no `architecture.authorization`, no `architectability_basis`, no experience mode,
  no composition selection, no record authority and no template selection in any fixture.
- `/blueprint` initialized the pair **once**, mechanically, from two frozen inputs plus the active pack's
  own scope. No fixture upgraded `authorized-bounded` to `authorized` (F-10, F-11 both stayed bounded),
  and no fixture derived or downgraded a value later.
- No fixture emitted a *decision blocked* it had not been given (F-12 is the load-bearing negative case).

**AUTHORIZATION / ARCHITECTABILITY: PASS.**

### 4.4 One recorded observation — carriage of `not-authorized`

The `architecture:` contract enumerates `not-authorized` as a legal value, but the artefact that would
carry it (`_blueprint/ux-blueprint_v<NN>.yaml`) is never produced in that case: `blueprint-contract.md`'s
entry gate requires an authorization for at least one scope. In the four not-authorized fixtures the two
reasons therefore live in `_synthesis/architecture-story.md`, in `render-log.md` and in the skill's user
output — **not** in a structured field.

This did **not** produce a behavioural failure. `aisa-render`'s first slot source is `_synthesis/`, so
the reason is still **read** rather than re-derived, and `aisa-synthesize` is explicitly instructed to
state which of the two reasons applies. Recorded as a documentation-level observation for Step 6
(§23, class I), not a semantic defect.

---

## 5. Headless behaviour

F-15 and F-16 were both executed. Structural result in both:

```text
experience.mode = none
primary_surface  = null
experience fragments rendered = 0
A4                            = not engaged (logged as `not applicable` with a reason)
unresolved surface            = none
missing include               = none        (fragment-experience-none.md never resolved)
render gap                    = none
```

**Material completeness** — the reason a headless architecture could read as an application with holes is
that A4 is absent. It does not, because the surviving sections carry real weight:

| Section | F-15 | F-16 |
|---|---|---|
| A5 data authority | affirmative **empty set** with the rationale | ERP as external system of record, `keep-in-place` |
| A6 automation / integration | the whole architecture: dispatch, execution, status resource, per-record failure unit, idempotency basis | three streams with distinct guarantees and failure semantics |
| A7 service identity | connection identity per system of record, secret custody, per-identity request budget | managed identity on the worker, connector identity on the platform side, broker as trust boundary |
| A8 environment / governance / release | one environment bound to residency; managed-solution route; long-running instances span releases | release route per estate, two supply chains via the fragments |
| A10 operation / support | Integration Ops named; recovery order in five steps; named reconciler | per-component operator, dead-letter owner, recovery ordering |
| A11 economics | per-run request consumption against the acting identity's budget; drivers only | broker operations, external compute, telemetry, egress — drivers only |
| A12 proof / epistemics | 2 obligations + the `VC-01` conflict + 3 volatile values | 3 obligations + contract-compatibility obligation |

Neither output reads as incomplete, and neither fabricated a screen, a persona, a navigation model or an
application lifecycle. F-15's chain (*shape → state location → unit of failure → retry/idempotency →
identity → environment/release → operator → proof obligation*) was walked in full and is recorded in §3.

**HEADLESS ARCHITECTURE: PASS.**

---

## 6. Experience modes

All four modes exercised; the three human-facing modes were replayed against real requirement pressure.

| Mode | Fixtures | Specialization actually produced | Did it own the architecture? |
|---|---|---|---|
| `owned-internal` | F-2, F-3, F-4, F-6, F-7, F-8, F-9, F-10, F-11, F-12, F-19 | A4 body, screen-architecture handoff, delegation-safe access paths, distribution, offline/device conditional, surface forfeits, human-user role model, owned lifecycle | **no** — store choice stayed in A5, control existence and reach stayed in core A7 |
| `owned-external` | F-5 | external-audience prerequisite, external identity provider as a **prerequisite** with cost and operating burden, deny-by-default authorization form, anonymous exposure decision, cache/freshness commitment, accessibility attestation basis, localization | **no** |
| `inherited` | F-1 | host and inherited access, inherited lifecycle, ceiling as a verification obligation, **mandatory graduation trigger**, forfeits, no independent topology | **no** — and it made **no** exclusion claim about the platform |
| `none` | F-15, F-16 | nothing — zero fragments | n/a |

**Surface never became architecture selection.** In F-2 and F-3 the surface choice was a recorded value
read into the fragment; the fragment described its consequences and forfeits and did not choose it, did
not choose the store, and did not choose the composition. In F-1 the fragment did not decide **whether**
the capability was architectable (that was the entry gate) nor **when** graduation occurs (that is the
tripwire mechanism). In F-5 the fragment did not decide whether an external audience was in scope.

**EXPERIENCE MODES: PASS.**

---

## 7. Record authority

Both halves of the gate were exercised, and they behaved differently — which is the point.

| Case | Fixture | Result |
|---|---|---|
| **Positive empty set** — no persisted business authority introduced | F-15 | `record_authority: []` **with** the affirmative rationale rendered in full. Legitimate and complete |
| **Missing authority evidence** — authority undetermined and architecture-changing | F-12 | **NOT** `[]`. An `open_architecture_choices` entry with `structural: true`, naming what would settle it and its `su_ref`. Approval blocked |
| Single owned domain | F-2, F-3 | 1 entry, `owned` |
| Kept in place | F-4, F-11 | 1 entry, `keep-in-place` |
| Virtualized | F-9 | 1 entry, `virtualized`, with the exclusion list checked against the requirements |
| Replicated (two truths) | F-6 | 2 entries, one `owned` + one `replicated`, obligations doubled |
| External system of record + operational state | F-16 | 1 entry + explicit non-authoritative execution state |

**No fixture converted an Unknown into an empty set**, and no fixture silently defaulted a store.

**EMPTY RECORD-AUTHORITY SEMANTICS: PASS.**

---

## 8. Composition identity / N+M invariant

### 8.1 F-19 collision behaviour

Two components, same `pattern` (`api-mediated`), same `owner` (Integration Team), same forcing-requirement
class, distinct `component` names ⇒ **2 architecture components → 2 boundary/import fragment instances**,
each carrying its own six channels with materially different content. Not merged, not deduplicated on the
shared pattern-plus-owner.

Adversarial duplicate (both named `integration-api`) ⇒ **architecture-contract failure**. No merge, no
suffix, no overwrite, no collapsed imports.

**F-19 COMPONENT COLLISION: PASS.**

### 8.2 The N+M invariant across the corpus

| Fixture | expected N | expected M | expected N+M | actual instances | match |
|---|---:|---:|---:|---:|:--:|
| F-1 | 0 | 0 | 0 | 0 | ✔ |
| F-2 | 0 | 0 | 0 | 0 | ✔ |
| F-3 | 0 | 0 | 0 | 0 | ✔ |
| F-4 | 1 | 0 | 1 | 1 | ✔ |
| F-5 | 0 | 0 | 0 | 0 | ✔ |
| F-6 | 1 | 0 | 1 | 1 | ✔ |
| F-7 | 1 | 0 | 1 | 1 | ✔ |
| F-8 | 3 | 0 | 3 | 3 | ✔ |
| F-9 | 1 | 0 | 1 | 1 | ✔ |
| F-10 | 1 | 1 | 2 | 2 | ✔ |
| F-11 | 1 | 1 | 2 | 2 | ✔ |
| F-12 | 0 | 0 | 0 | 0 | ✔ |
| F-15 | 1 | 0 | 1 | 1 | ✔ |
| F-16 | 3 | 0 | 3 | 3 | ✔ |
| F-19 | 2 | 0 | 2 | 2 | ✔ |
| **Total** | **15** | **2** | **17** | **17** | **✔** |

F-13, F-14, F-17a/b and F-18 produce no architecture, so the invariant does not apply and no instance was
emitted. **Zero mismatches.**

Three qualification edge cases behaved correctly:
- `direct` **in-platform** (F-2, F-3, F-12) ⇒ **not** qualifying, 0 instances. It imports nothing.
- `direct` **outside-platform** (F-4, F-8's asset-register read) ⇒ **qualifying**. The boundary, not the
  rung, is what triggers it.
- `background-processing` **in-platform** (F-15) ⇒ **qualifying**, because it is beyond `direct`.

**N+M FRAGMENT INVARIANT: PASS.**

---

## 9. Imported obligations

17 fragment instances × 6 channels = **102 channel slots**. Every slot was present — no instance omitted
a channel. The gate's real question is whether the content is decision-bearing.

| Disposition | Count | Notes |
|---|---:|---|
| Populated with decision-bearing content | **100** | includes the two `owner: UNKNOWN` Operator channels, which state the capability fact rather than a name |
| `not engaged — <reason>` | **2** | both materially defensible (below) |
| Absent / boilerplate | **0** | no instance produced a run of bare `not engaged` lines |

**The two `not engaged` channels, in full:**

1. F-8 · `asset-register-read` · **Cost** — *"not engaged — a read-only connector call on an existing
   entitlement introduces no new meter; the request consumption is already attributed to the acting
   identity's budget in A11."* Defensible: it names the reason, names where the consumption **is**
   accounted, and does not claim the component is free.
2. F-11 · `requisition-authority-and-posting` (relocation) · **Cost** — *"not engaged — the incumbent's
   licence and operating cost are pre-existing and unchanged by this decision; no new meter appears on
   the far side, and no comparative cost claim is available."* Defensible **and** comparator-neutral: it
   refuses the cost comparison rather than guessing it.

**Spot-checks that the content is not generic.** The three F-8 instances and the three F-16 instances were
compared channel by channel: no channel text repeats across components. Examples of the discriminating
content the channels actually carried — *"which platform controls stop applying at its edge"* (governance,
every outside-platform instance); *"two supply chains"* versus *"two release routes"* versus *"the upstream
schema can break the application with no platform release"* (ALM, hybrid / api-mediated / virtualization);
*"replay or reconcile before the queue is reopened"* (recovery, queue only); *"the status resource is the
operational surface"* (monitoring, background-processing only); *"a named human for the bulk pipeline
because service-principal ownership is unavailable there"* (operator, replication only).

**SIX-CHANNEL IMPORT CARRIAGE: PASS.**

### 9.1 Cross-boundary accumulation (F-6, F-7, F-8, F-16)

The adversarial question is whether *queue + external worker + mediated API* collapses into one generic
*external dependency*. It did not, in either multi-component fixture.

| Property | F-16 `order-intake-queue` | F-16 `order-validation-worker` | F-16 `pricing-api` |
|---|---|---|---|
| Owner | Integration Team (broker rota) | Integration Team (pro-code rota) | Integration Team (API owner) |
| Release route | infrastructure-as-code for queue/topic config | source control + IaC + pipeline for worker code | IaC + pipeline for the API, contract-version gated |
| Monitoring consequence | queue depth, dead-letter depth, consumer lag, worker failures | telemetry on both halves + correlation identifier across the seam | gateway + backend telemetry into one sink |
| Recovery consequence | replay-or-reconcile decision **before reopening** | recovery sequence spanning both estates | API layer **and** consumer contract |
| Economic meter | broker operations, storage, egress; tier can be **forced** by duplicate detection | external consumption + non-production + pro-code effort | API runtime, telemetry, non-prod, operator |
| Governance boundary | the broker holds message content **at rest** and must be classified | second governance plane for the external half | governed workload asset with API inventory |

Same three-way distinction held in F-8. **Nothing merged on a shared owner** (F-16, F-19) or a shared
pattern (F-19). **No component lost its owner, route, signal, recovery step, meter or governance
boundary.**

---

## 10. Scope pairs / far-side boundary

### 10.1 F-10 — cloud-native responsibility moved out

PP application side fully architected (A4–A12). The far side received exactly: boundary · owner
(cloud-native services) · outcome basis (class-3 sentence verbatim) · the five S7 gates as recorded
values · six import channels · and the explicit *what this pack does not know* section. It received **no**
invented components, **no** data model, **no** technology naming, **no** operational model and **no**
claimed suitability. Pairs stayed uncollapsed in A1, in the scope-ownership table and in the synthesis.

### 10.2 F-11 — incumbent responsibility

`INCUMBENT FIT UNEVALUATED` appears **verbatim** in four places and was never transformed. Explicitly
checked and absent from the output: any statement that the incumbent *fits*; any statement that the
incumbent is a *poor fit*; any incumbent-internal architecture; any comparative cost or capability claim.
Where the incumbent's telemetry was needed, the output recorded it as **Unknown** and made the PP side
responsible for its own correlation — a design obligation, not an inference about the incumbent.

### 10.3 Authorized-bounded discipline

Both F-10 and F-11 stayed `authorized-bounded` end to end. Neither was upgraded. Neither architected the
far side.

**Class-6 coverage — corrected 2026-09-04.** An earlier version of this section stated that class-6
emitted-pair behaviour was exercised through F-6's second scope. That was wrong: F-6 emits two class-2
pairs and exercises no class 6. **The original F-1…F-19 corpus did not exercise an explicit class-6
surrounding-scope pair.** The bounded Step 5C class-6 addendum executed C6-A and C6-B (§26). It confirmed
that class 6 alone never authorizes the surrounding scope, while an independently emitted surrounding pair
can authorize that scope on its own merits. The F-6 fixture itself is unchanged.

**SCOPE-PAIR BEHAVIOUR: PASS. FAR-SIDE ARCHITECTURE INVENTED: NO.**

---

## 11. Structural open choices

| Fixture | Structural open choice | Production | Approval | Downgraded to a risk? |
|---|---|---|---|---|
| F-8 | no operator exists for the queue and the external worker | proceeded | **blocked** | **no** — stated as an architecture capability fact |
| F-12 | record authority undetermined between two defensible stores | proceeded | **blocked** | **no** — rendered as a structural choice with both candidates |

### 11.1 Operator availability (F-8)

The architecture capability fact was exposed in the words the pattern unit uses — *the composition is
unavailable because no operator exists* — and framed as a statement about the **design**, not a ranking of
the organisation. The honest alternative output was cross-referenced (the simpler composition plus a
tripwire on the metric that would force the move) without the layer asserting it as its own
recommendation. **No operator was silently named.** **No conversion into an accepted architecture risk**
occurred; the canonical pattern does not permit that here, and the layer did not invent permission.

### 11.2 Multiple defensible architectures (F-12)

Neither architecture was silently chosen. **No scoring, no weighting, no ranking, no template
preference** appeared. Both candidates were rendered with their own forfeits, identity models and
irreversible consequences. What would settle the choice was named with an owner. Blueprint **production**
was permitted; **approval** was blocked. And critically, this remained **architecture uncertainty**: no
class 12 was emitted, the class-2 authorization stood untouched, and `decisions.md` was not modified.

**STRUCTURAL OPEN-CHOICE BEHAVIOUR: PASS.**

---

## 12. Epistemic handling

All five kernel states were exercised, and none was upgraded.

| State | Where exercised | Behaviour observed |
|---|---|---|
| **Confirmed** | every fixture (residency, volumes, peak measurements, requirement absences) | rendered as fact **with** `verificado_em` / `validade`. One deliberately expired row was introduced in F-6 (a change-rate profile confirmed 14 months earlier, validity 12 months) and rendered as a **re-verification obligation**, not as fact |
| **Assumed** | F-2 (sites have coverage), F-1 (write concurrency stays low), F-6 (change-rate profile) | remained labelled Assumed with basis and validity. **No fixture promoted an Assumed row**, including where promotion would have closed a section cleanly (F-2's offline conditional) |
| **Unknown** | F-5 (site throughput/concurrency ceilings unpublished), F-9 (composition performance envelope), F-11 (incumbent telemetry access), F-12 (store authority) | never filled. Each became an `open_architecture_choices` entry or a proof obligation; `structural: true` only where it decided store authority, the enforcement point or whether a responsibility leaves the platform |
| **Conflicted** | F-15 and F-8 (`VC-01` / `VS-08`, the register's live conflict on the per-mechanism throughput ceiling) | **the conflict itself is the content.** Neither figure was carried on either side, and the sizing claim became a **V3** proof obligation |
| **Risky** | F-2 (no audit trail), F-6 (two truths in the sync window), F-9 (false freshness behind a real-time-looking interface) | carried in A10 / A12 with the **accepted-risk id from the D-NNN**. Not re-argued, not re-graded, not silently mitigated |

**No fixture upgraded epistemic confidence in any direction.** The most tempting case — F-2, where
promoting one Assumed row would have removed a conditional section — held.

**EPISTEMIC PRESERVATION: PASS.**

---

## 13. Volatile values

Six architecture-relevant volatile values were exercised across the corpus; all resolved to one of the
two permitted forms.

| # | Value | Fixture | Register | Form rendered |
|---:|---|---|---|---|
| 1 | Host/list capacity ceiling for the inherited surface | F-1 | `VC-07` | **verification obligation** (what to measure · owner · fidelity · by when). No figure |
| 2 | Managed-environment entitlement chain | F-3 | `VC-05` | **verification obligation**. Drivers stated, **no price** |
| 3 | Peak inbound reconciliation rate | F-15 | engagement measurement | **verified engagement value** — *1,180 records/hour · verificado_em 2026-08-20 · validade 90 dias · re-verificar quando a base de fornecedores variar >10%* |
| 4 | Request rate per acting identity | F-15 | `VC-04` | **verification obligation** — the published figures are transition-period tolerances with no enforcement date, so no figure was carried |
| 5 | Per-mechanism throughput ceiling | F-15, F-8 | `VC-01` / `VS-08` | **Conflicted** — conflict rendered, **neither figure carried**, sizing became a V3 obligation |
| 6 | External-audience site throughput / concurrency | F-5 | unpublished | **Unknown** preserved + V3 representative-pilot obligation |

**No architecture output invented a service value, and none fossilized one.** No template contributed a
number: a regex-level read of the five runtime units confirms none contains a limit, price, quota,
retention window, threshold or SKU value, and none of the 19 fixtures' outputs sourced a figure from a
template. Item 3 is the only figure that appears as a number, and it is an **engagement measurement**
with its full validity stamp — not a platform reading.

**VOLATILE-VALUE HANDLING: PASS.**

---

## 14. Proof obligations

A12 was inspected in every architecture-producing fixture for the five-part shape rather than a bare
*"test performance"* line.

| Fixture | Claim | Level | Method | Owner | Funded | Uncertainty it answers |
|---|---|---|---|---|---|---|
| F-1 | the list holds 3 years at the stated volume | V2 | production counter read | IT ops | yes | the unverified host ceiling |
| F-3 | audit retention satisfies the 7-year legal obligation | V2 | retention-policy inspection + a restore drill on one case | HR systems owner | yes | retention configuration, not capability |
| F-5 | the site serves the declared peak of 4,000 contractors | **V3** | representative pilot at declared peak | Platform owner | yes | throughput/concurrency ceilings are **unpublished** |
| F-7 | the mediated tier does not become the bottleneck | V2 | load test at the composed peak | API owner | yes | the vendor-stated single-point-of-failure risk |
| F-8 | in-tier processing meets the Confirmed arrival rate without the queue | **V3** | pilot at measured peak | (blocked — no operator) | **no** | whether the escalation is required at all |
| F-9 | interactive query volume over the virtualized source is servable | **V3** | representative pilot | Legal Systems + Platform | yes | no published throughput/latency envelope |
| F-15 | idempotency under rerun | V2 | replay the same batch twice, diff the ledger | Integration Ops | yes | reruns are expected by design |
| F-15 | throughput at the verified peak | **V3** | representative pilot | Integration Ops | yes | `VC-01` is **Conflicted** |
| F-16 | no message loss under burst + poison quarantine | V2 | fault-injection on the broker path | Integration Team | yes | the delivery guarantee is the requirement |
| F-16 | pricing contract compatibility across a joint release | V2 | contract test in the pipeline | Integration Team | yes | deployment coupling between halves |

**Every obligation was carried from Step 3 / S9, and none was re-graded by the architecture layer.**
F-8's unfunded obligation is instructive: the layer did **not** downgrade it to V1 to make the section
close, and did **not** invent an owner — it carried *funded: no* with the blocked owner, consistent with
the structural open choice.

**PROOF-OBLIGATION CARRIAGE: PASS.**

---

## 15. Domain Knowledge pull behaviour

### 15.1 Per-fixture pulls

| Fixture | RESEARCH units pulled | Pattern sections pulled | CRAFT units | Second pulls (and the material dependency that forced each) |
|---|---:|---|---:|---|
| F-1 | 8 | — | 1 | 1 — `data/sharepoint` after `application-surfaces` exposed the host store's own ceiling |
| F-2 | 10 | — | 4 | 1 — `data/sharepoint` for the versioning-not-audit forfeit |
| F-3 | 10 | — | 4 | 2 — `data/dataverse` (column security + audit exist only there); `alm/release-and-lifecycle` (managed-only production route) |
| F-4 | 11 | §3 + `direct` | 5 | 1 — `data/azure-sql` (connector identity model + gateway are the contested boundary) |
| F-5 | 8 | — | 1 | 1 — `governance-and-environments` §11 (exposure and policy plane) |
| F-6 | 11 | §3 + `data-replication` | 4 | 1 — `data/dataverse` (what the copy does **not** inherit) |
| F-7 | 10 | §3 + `api-mediated` | 4 | 1 — `integration-mechanisms` (the connector contract chokepoint) |
| F-8 | 12 | §3 + `queue-based` + `hybrid-low-code-pro-code` + §7 | 4 | 1 — `patterns` §7, because the first pull surfaced `owner: UNKNOWN` |
| F-9 | 10 | §3 + `data-virtualization` | 3 | 1 — `data/dataverse` (virtual-table modelling requirements) |
| F-10 | 9 | §3 + `queue-based` | 4 | 0 |
| F-11 | 10 | §3 + `api-mediated` | 4 | 0 |
| F-12 | 9 | — | 4 | 1 — one store unit per contested candidate, in the candidate section |
| F-13 | **0** | — | 0 | — |
| F-14 | **0** | — | 0 | — |
| F-15 | 8 | §3 + `background-processing` | **0** | 1 — `alm/release-and-lifecycle` (release route for a surface-less solution) |
| F-16 | 10 | §3 + `queue-based` + `hybrid-low-code-pro-code` + `api-mediated` | **0** | 0 |
| F-17a/b | **0** | — | 0 | — |
| F-18 | **0** | — | 0 | — |
| F-19 | 9 | §3 + `api-mediated` (**once, serving both instances**) | 4 | 1 — `integration-mechanisms` |

### 15.2 Gate-level metrics

```text
materially authored sections with a knowledge need   : 118
median RESEARCH pulls per materially authored section: 1
maximum RESEARCH pulls for one material section      : 2
unnecessary third-or-later pulls                     : 0
whole-pattern-catalogue scans                        : 0
preloaded units                                      : 0
architecture knowledge bundles assembled             : 0
routing tables keyed by section                      : 0
```

The frozen expectation (median ≈ 1, maximum 2) held exactly. Every second pull in the table above names
the material dependency the **first** pull exposed; none was speculative.

### 15.3 `architecture/patterns.md` discipline

Only **§3** (the six channels) plus **the engaged composition(s)** in §5 were read, in every fixture that
engaged one. §5 was never opened in full and the ten compositions were never surveyed. Across the whole
corpus, seven of the ten compositions were read — but always one at a time, each forced by a recorded
`compositions[].pattern` value, never as a catalogue. §7 was read exactly once (F-8), forced by
`owner: UNKNOWN`.

Two efficiencies worth recording, both correct: in **F-19** the pull is **per pattern, not per instance**
— one `api-mediated` read served both fragment instances; and in **F-16** three distinct patterns meant
three pulls, but `§3` was read once and shared.

### 15.4 The four fixtures with zero pulls

F-13, F-14, F-17a/b and F-18 pulled **nothing**. This is the strongest single pull-discipline signal in
the gate: with no authorization there is no architecture responsibility to describe, so there is nothing
to pull. F-14 is the sharpest case — the layer did **not** re-open `application-surfaces.md` to
re-verify the push-notification and consumer-audience exclusions frozen in its outcome sentence.
Re-verifying them would have been re-deciding.

**DOMAIN KNOWLEDGE PULL DISCIPLINE: PASS.**

---

## 16. CRAFT boundary

Four legitimate uses were exercised (three were required):

| Use | Fixture | CRAFT unit | What it shaped | What it did **not** touch |
|---|---|---|---|---|
| Screen consolidation | F-2, F-3 | `screen-consolidation-rules` | field counts → screen types; role separation; approval-as-action; the hard caps | no platform limit, no store choice |
| Screen pattern shaping | F-2, F-3, F-12 | `screen-patterns` | pattern catalogue and density | asserted no platform limit |
| Security-matrix form | F-3, F-5 | `security-craft` | the **form** of the role and visibility matrix | which control exists and where it takes effect stayed in core A7, cited to `security/security-controls.md` |
| SQL naming / layering | F-4 | `sql-delivery-conventions` | relational layering and naming for the relational-via-connector store | tiers, limits and throughput stayed with `data/azure-sql.md` |

Plus `delivery-conventions` for solution and environment naming in F-1…F-4 and F-6…F-12.

**Prohibited uses — all checked, none observed:**

```text
CRAFT → establishes a platform capability   : NOT OBSERVED
CRAFT → selects the store                   : NOT OBSERVED
CRAFT → selects the composition             : NOT OBSERVED
CRAFT → sets an authorization               : NOT OBSERVED
CRAFT → supplies a technical limit          : NOT OBSERVED
CRAFT → sets record authority               : NOT OBSERVED
CRAFT → chooses a proof level               : NOT OBSERVED
```

`craft/estimation-model.md` was **not** consulted in any fixture. **CRAFT was not consulted at all** in
F-15 and F-16 — correctly, since a headless architecture has no screen, matrix or naming surface that
CRAFT shapes. No RESEARCH/CRAFT conflict arose, so the *RESEARCH wins and the CRAFT statement is a defect
to report* rule was not exercised behaviourally; it remains asserted in the runtime.

**CRAFT BOUNDARY: PASS.**

---

## 17. Boundary-table / diagrams

### 17.1 The required boundary table

Checked in all 15 architecture-producing fixtures for the six columns and for exactly-once membership.

```text
columns present in every fixture: Component · Role · Platform governance ·
                                  Trust boundary crossed · Owner · Data classification
```

| Fixture | compositions[] | record_authority[] | relocated[] | expected rows | actual rows | duplicates |
|---|---:|---:|---:|---:|---:|---:|
| F-2 | 1 | 1 | 0 | 2 | 2 | 0 |
| F-3 | 1 | 1 | 0 | 2 | 2 | 0 |
| F-4 | 1 | 1 | 0 | 2 | 2 | 0 |
| F-6 | 1 | 2 | 0 | 3 | 3 | 0 |
| F-8 | 3 | 1 | 0 | 4 | 4 | 0 |
| F-9 | 1 | 1 | 0 | 2 | 2 | 0 |
| F-10 | 1 | 1 | 1 | 3 | 3 | 0 |
| F-11 | 1 | 1 | 1 | 3 | 3 | 0 |
| F-15 | 1 | 0 | 0 | 1 | 1 | 0 |
| F-16 | 3 | 1 | 0 | 4 | 4 | 0 |
| F-19 | 2 | 1 | 0 | 3 | 3 | 0 |

Every relevant composition, record authority and relocated responsibility appeared **exactly once**.
**No diagram-only component** in any fixture. **No hidden far-side architecture**: in F-10 and F-11 the
relocated responsibility appears as one row with an outside-platform governance value, an external owner
and a crossed trust boundary — a boundary, not a design.

### 17.2 Diagram behaviour

Produced where a composed or asynchronous path existed: context sketches in F-8, F-10, F-11 and F-16;
one sequence sketch in F-16 (a status resource plus a reconciliation pivot exists). **Not** produced in
F-1, F-2, F-3, F-5, F-12 or F-15 — correctly logged as `not applicable — <reason>` rather than forced.

In every sketch produced: all nodes are boundary-table rows; every edge states direction **and** mechanism
class; trust boundaries appear as annotation (plain-text-safe, since the repository renders fenced blocks
as preformatted text); the relocated responsibility is drawn **outside** the PP scope in F-10 and F-11;
and **no fact exists only in a diagram** — each was cross-checked against the boundary table and the
prose.

---

## 18. Blueprint altitude

Every fixture's output was scanned for implementation leakage.

| Should be present at architecture altitude | Observed |
|---|---|
| Components and responsibilities | yes, all 15 |
| Authority per data domain, store role, access mode | yes |
| Data flow and trust boundaries | yes |
| Major interfaces **with their guarantee** | yes (F-7, F-16 carry the guarantee explicitly) |
| Deployment / environment topology | yes |
| Control boundaries and enforcement points | yes (F-4 is the sharpest) |
| Named operators | yes, or the structural absence (F-8) |
| Proof obligations | yes, 10 across the corpus |
| Irreversible choices | yes (F-3, F-4, F-9) |

| Must **not** appear | Observed |
|---|---|
| Power Fx expressions | **none** |
| Flow action graphs | **none** |
| SQL DDL | **none** — F-4 carries layering and naming conventions, not schema |
| Field-by-field payload schemas | **none** — F-7/F-16/F-19 name the *contract* and its compatibility requirement, not its fields |
| Pixel-level UX | **none** — F-2/F-3 hand off screen architecture and stop |
| Migration scripts | **none** — F-9's irreversibility is stated as a rebuild cost, not a procedure |
| Runbook steps | **none** — F-15/F-16 state recovery **ordering** and the named reconciler, not commands |

The boundary test (*would changing this invalidate the architecture, or only the build?*) was applied to
the borderline cases. F-15's *"writes are keyed on the alternate key and are upserts"* stays: change it
and the idempotency guarantee — an architecture property — changes. F-2's *"server-side pre-filter by
technician and month"* stays: it is the architectural consequence of a non-delegable path, not an
expression. **No systemic leakage.**

---

## 19. Decision leakage

The question was asked of every fixture: *did architecture work structure a decided solution, or
re-decide it?*

| Forbidden behaviour | Occurrences |
|---|---:|
| A new outcome class emitted | **0** |
| A new option comparison | **0** |
| A PP preference expressed | **0** |
| A comparator winner named | **0** |
| The candidate set re-evaluated | **0** |
| An architecture pattern used as evidence PP should have won | **0** |
| The upstream decision silently rewritten | **0** |

What the layer **did** discover, legitimately: 2 structural open architecture choices (F-8, F-12);
10 proof obligations carried and none re-graded; several architecture work items (F-5's accessibility
attestation, F-6's reconciliation runbook, F-16's contract test) — all logged as architecture-open, none
decision-blocking.

Three tempting cases held:
- **F-12** could have picked a store and called the decision complete. It did not; and it did not escalate
  to class 12 either.
- **F-8** could have named an operator or accepted the missing operator as a risk to unblock approval.
  It did neither.
- **F-14** could have proposed a PP alternative once the consumer surface was excluded. It did not, and
  reproduced the emitted candidate set unchanged.

One observation recorded for Step 6: `library/kernel/synthesis-templates/architecture-story.template.md`
§*Chosen architecture* instructs the narrative to state *"why it won over alternatives"*, sourced from
`decisions.md`. In the replay this reproduced the decision record's own justification field and produced
no new comparison — the fixtures show it behaving as repetition, not derivation. It is nevertheless the
one place in the layer whose wording invites a comparative sentence, and it is worth tightening when
Step 6 touches the synthesis templates. Not a semantic failure. (§23, class I.)

**DECISION LEAKAGE DETECTED: NO.**

---

## 20. Comparator neutrality

| Check | Fixtures | Result |
|---|---|---|
| **N1** — far-side absence of knowledge does not become evidence it is worse | F-10, F-11 | **PASS.** *What this pack does not know* is stated as an evidence gap. F-11's Cost channel explicitly refuses the comparison rather than inferring one |
| **N2** — rich PP architecture detail does not become evidence PP is better | F-3, F-16 (the two densest outputs), F-17, F-18 | **PASS.** No output drew a quality inference from its own depth. F-17/F-18 produce **no** PP detail at all and still make no claim about the selected non-PP solution |
| **N3** — an excluded or non-architectable PP scope does not prove custom / SaaS / incumbent fit | F-14, F-17a, F-17b, F-18 | **PASS.** F-14 reproduces `comparative fit UNEVALUATED`; F-17 states the packaged/custom solution's outcome basis and asserts nothing about its architecture; F-18 asserts nothing about the document library beyond the documented-sufficiency sentence, scoped to the seeded-entitlement fact alone |
| **N4** — incumbent internals remain unmodelled where evidence is absent | F-11 | **PASS.** Zero incumbent-internal statements. `INCUMBENT FIT UNEVALUATED` verbatim in four places |

Additionally: F-17 and F-18 both state explicitly that **no PP exclusion was emitted** — the defect
*"not architectable therefore PP lost"* is actively refused rather than merely absent.

**COMPARATOR BIAS DETECTED: NO.**

### 20.1 Step 6 boundary check

The three unmigrated deliverable templates still reference `chosen_architecture` / `Branch (if
technology)`. **No fixture failed on that account** — and, tested directly: the Architecture Layer read
none of them to reason or to render its architecture. All 15 architecture-producing fixtures resolved
through `architecture-core.md` as the fixed entry point, plus the fragments resolved from the recorded
`architecture:` block. The layer has **no dependency** on the carry-forward files.

### 20.2 Legacy boundary check

`sharepoint-first`, `dataverse-first` and `hybrid` appear **nowhere** in any of the 19 fixture outputs.
No fixture replayed a legacy engagement, so the README §11 read-compat mapping was not consulted, and its
vocabulary did not enter any architecture. Confirmed by string search across the replay corpus.

---

## 21. Sponsor readability

Three representative outputs were read as a sponsor or a receiving architect would read them, asking:
*can I tell what owns what, which obligations the architecture imports, what remains uncertain, and what
must be proven?*

| Output | Owns what | Imports what | Uncertain | To be proven | Verdict |
|---|---|---|---|---|---|
| **F-3** internal app | one governed store, one app, one team — 2 boundary-table rows | nothing outside the platform; the managed-environment gate is stated as a governance consequence | entitlement fit (`VC-05`) | audit retention (V2) | readable in one pass |
| **F-16** headless integration | ERP owns the order; PP owns intake, validation and pricing consumption; Integration Team operates all three external components — 4 rows | three distinct obligation sets, tabulated per component; recovery ordering stated once | none structural | 2 obligations (V2) | readable; §22.1 records the density finding |
| **F-10** scope pair | application on this platform; notification delivery owned externally with five gates recorded — 3 rows | the far side's six channels, plus what this pack does not know | the far side's internals (declared) | 1 obligation | the ownership split is the clearest thing on the page |

**No output required copying the Domain Knowledge narrative to be complete.** Every boundary claim is a
citation (`data/azure-sql.md`, `architecture/patterns.md` §5 *queue-based*, and so on) rather than a
restatement, and none of the three needed the reader to open a knowledge unit to understand the
architecture — only to check a claim. Verbosity was not rewarded: F-15's headless output is the shortest
in the corpus and is materially complete.

---

## 22. Context efficiency / ceremony

| Ceremony risk | Observed |
|---|---|
| Empty or meaningless sections | **0.** Every section either carried content or rendered `not applicable — <reason>` |
| Facts repeated across sections | **2 deliberate, 0 accidental.** The second cost meter appears in both A11 and the fragment's Cost channel (F-6), and the operator appears in both A10 and the Operator channel (all composed fixtures). Both are the intended dual carriage — the core's summary view and the per-component obligation — not duplication |
| Unnecessary knowledge pulls | **0** (§15) |
| Conditional sections rendered that should have been omitted | **0.** Conditionals were engaged only on their triggers; F-15 engaged 1 of 8, F-3 engaged 1 of 8, F-16 engaged 3 of 8 |
| Generic six-channel filler | **0** (§9) |
| `not applicable` lines without a reason | **0** |

**Materially complete versus mechanically complete-looking.** The distinguishing test applied to each
fixture was: *remove the section — does the architecture still answer its question?* The A1–A12 core did
not behave as a checklist: F-15 renders 8 substantive sections plus 1 affirmative empty set plus 1
conditional, and F-1's inherited output renders 9 — both far short of a mechanical twelve, and both
complete. The `not applicable — <reason>` discipline is what keeps this honest: a section that is skipped
says **why**, which is information, whereas an empty heading would be ceremony.

**SYSTEMIC CONTEXT-CEREMONY DETECTED: NO.**

### 22.1 Large-composition stress case (F-16)

The most complex architecture in the corpus: three outside-platform components, three fragment instances,
18 channel entries, one shared owner, no human surface.

| Question | Finding |
|---|---|
| Are multiple fragments still understandable? | **Yes** — each opens with its component name and its `forced_by`, so the reader knows why it exists before reading its obligations |
| Are imports duplicated unnecessarily? | **No** — 18 channel entries, no repeated text. The shared owner appears three times because there are three distinct on-call contracts, which is information, not duplication |
| Is ownership clear? | **Yes** — the boundary table's 4 rows answer it in one place before any fragment is read |
| Does the core remain readable? | **Yes.** The core holds A1–A3 and A5–A12; the three fragments are appended. The core is not inflated by the composition count |
| Do we still know why each component exists? | **Yes** — three distinct `forced_by` requirements, none generic |
| Is recovery ordering understandable? | **Yes** — stated **once**, in A10, as a five-step sequence spanning components, with the per-component consequences left in the fragments. This is the design's best structural decision under load |
| Has one giant architecture paragraph appeared? | **No** |

One mild finding: with three fragments, the reader meets *"which platform controls stop applying at its
edge"* three times, phrased similarly each time even though the controls named differ. It is correct and
non-redundant in substance, but it is the point at which the six-channel format is most visible as a
format. **No template split was performed** (out of scope for the initial gate) and none is recommended —
the substance differs, and splitting would break the one-fragment-per-component invariant that makes the
N+M count testable.
---

## 23. Failures and classification

All 19 fixtures were run to completion **before** any finding was assessed, per §42. Findings were then
aggregated and classified.

### 23.1 Semantic fixture failures

**None.** 19/19 PASS. No fixture produced a materially wrong, dishonest or indefensible architecture.

| Class | Definition | Count | Disposition |
|---|---|---:|---|
| **A** — architecture authoring defect | frozen model correct, runtime behaviour or content wrong | **0** | — |
| **B** — authorization / architectability defect | wrong scope entered architecture work | **0** | F-17, F-18, F-13, F-14 all correct |
| **C** — composition / import defect | components or imports lost, collapsed or invented | **0** | 17/17 instances, 102/102 channels, 0 collapses |
| **D** — epistemic defect | Unknown / Assumed / Conflicted promoted or hidden | **0** | all five states preserved |
| **E** — Domain Knowledge pull defect | too shallow, wrong source, or indiscriminate | **0** | median 1, max 2, 0 catalogue scans |
| **F** — CRAFT authority defect | CRAFT became technical truth | **0** | 7 prohibited uses checked, none observed |
| **G** — decision leakage | the layer re-decided Options | **0** | 7 forbidden behaviours, 0 occurrences |
| **H** — comparator bias | PP depth created preference or inference | **0** | N1–N4 all PASS |
| **I** — context ceremony | correct reasoning needs avoidable framework or output ceremony | **2 observations** (+1 from the §26 addendum) | below — none blocks |
| **J** — frozen Step 5A defect | runtime faithful but the design itself insufficient | **0** | no fixture required a design change to pass |

### 23.2 The two class-I observations

Both are documentation-level, both are Step 6-adjacent, and **neither caused a fixture to fail**.
A third of the same kind (**I-3**) was recorded later by the class-6 addendum — see §26.9.

**I-1 — `not-authorized` has no artefact to live in.** The `architecture:` contract enumerates
`not-authorized`, but `blueprint-contract.md`'s entry gate means no blueprint is written when it applies,
so the value and its two bases are never persisted as structured fields. In the four affected fixtures the
two reasons survived correctly in `_synthesis/architecture-story.md`, `render-log.md` and the skill's user
output, and `aisa-render` **read** them from its declared first slot source rather than re-deriving them.
Smallest bounded repair, if taken: one sentence in `blueprint-contract.md` stating where the
not-authorized pair is recorded. **Recommended as a Step 6 item, not a Step 5 blocker.**

**I-2 — one comparative phrase in a kernel synthesis template.**
`architecture-story.template.md` §*Chosen architecture* asks for *"why it won over alternatives"*, sourced
from `decisions.md`. In replay it reproduced the decision's own justification and generated no new
comparison, but it is the single place in the layer whose wording invites one. Smallest bounded repair, if
taken: reword to *"the justification the decision recorded"*. **Recommended as a Step 6 item** — it is a
kernel synthesis template and Step 6 owns the synthesis/deliverable pass; changing it now would modify
runtime during the gate for no behavioural gain.

### 23.3 Unsupported architecture claims

```text
unsupported architecture claims invented: 0
```

Every claim in every fixture output traces to one of three sources: engagement evidence with an SU id, a
cited Domain Knowledge fact, or a frozen decision fact. Where knowledge was absent the layer preserved
**Unknown** or an evidence obligation in all six instances where it could have guessed instead (F-5 site
throughput · F-9 composition envelope · F-11 incumbent telemetry · F-12 store authority · F-15 request
rate · F-1 host ceiling).

### 23.4 Repair policy applied

No repair was performed. The two observations are bounded, documentation-only, and belong to Step 6's
scope. Nothing was changed in Step 3, Step 4, the templates, the patterns or the skills. No template was
added per scenario. No router was created. No knowledge was preloaded. No research was performed.

**RUNTIME MODIFIED DURING INITIAL GATE: NO.**
(The only file touched in this step is
`research/pp/authoring/step-5b-architecture-template-implementation-report.md` — the two
documentation-only corrections commissioned in §0: the enumerated modified-file count `9 → 10`, and the
appended Step 5B final marker plus `STEP 5B: CLOSED`.)

---

## 24. Final verdict

Step 5C passes on every criterion in §43, with no material semantic failure.

| PASS criterion | Result |
|---|---|
| 19/19 fixtures executed | ✔ 19/19 (F-17 in two variants) |
| architectability behaviour correct | ✔ reachability × architectability, both factors load-bearing |
| F-17 and F-18 correct | ✔ reachable + not architectable ⇒ no PP architecture, two reasons distinct |
| headless complete | ✔ F-15, F-16 materially complete, zero fragments, zero gaps |
| experience modes correct | ✔ all four; the fragment specializes and never owns |
| empty record-authority semantics correct | ✔ F-15 affirmative `[]`, F-12 structural open choice |
| F-19 collision correct | ✔ 2 components → 2 instances; duplicate name fails |
| N+M invariant holds | ✔ 15 + 2 = 17 expected, 17 actual, 0 mismatches |
| imported obligations materially populated | ✔ 100/102 populated, 2 defensible `not engaged`, 0 boilerplate |
| scope pairs remain uncollapsed | ✔ F-6, F-10, F-11 |
| no far-side architecture invented | ✔ boundary, owner, outcome basis, gates, imports — and nothing else |
| F-12 does not silently choose | ✔ both candidates rendered, neither chosen, no scoring, approval blocked |
| F-13 stops architecture | ✔ no architecture, no template, no work item, no draft |
| epistemics preserved | ✔ all five states; nothing upgraded |
| volatility preserved | ✔ 6 values; verified-with-stamp or verification obligation; 0 invented |
| proof obligations preserved | ✔ 10 obligations, five-part shape, none re-graded |
| Domain Knowledge pull remains selective | ✔ median 1, max 2, 0 third pulls, 0 catalogue scans |
| CRAFT remains non-authoritative | ✔ 4 legitimate uses, 7 prohibited uses checked and absent |
| no decision leakage | ✔ 0 occurrences across 7 forbidden behaviours |
| no comparator bias | ✔ N1–N4 PASS |
| architecture altitude appropriate | ✔ 0 systemic leakage; 7 leakage classes checked |
| no systemic context ceremony | ✔ 0 empty sections, 0 filler, 2 deliberate dual carriages |

**The Architecture Layer is defensible.** It turns frozen decisions into architecture descriptions that a
sponsor can read and an architect can act on; it refuses to architect what it has no authority over; it
carries imported obligations structurally rather than editorially; it keeps a headless architecture whole;
it will not design the far side of a scope pair; it will not choose between two defensible architectures;
and it does not upgrade what the engagement does not know.

---

## 25. Recommendation: freeze Step 5

**Freeze Step 5 — Architecture Templates.** No bounded repair is required to pass. The five runtime units,
the `architecture:` contract, the reachability × architectability gate and the four render-gap classes are
behaviourally sound across the full frozen fixture corpus.

The bounded **class-6 coverage addendum** (§26), executed after the main gate, closed the one
coverage gap the report contained and did not change this recommendation: C6-A and C6-B both PASS,
no repair required, no runtime modified, and no original fixture result altered.

**Carry into Step 6** (deliverable-template migration), in priority order:

1. Migrate `solution-blueprint.template.md`, `implementation-spec.template.md` and
   `claude-design-brief.template.md` off `chosen_architecture` / `Branch (if technology)` and onto the
   fixed `architecture-core.md` entry point plus the `architecture:` block. Step 5C confirms the layer
   itself has no dependency on these files, so the migration is bounded to the deliverable side.
2. Resolve Step 5A's two carried open questions: whether `claude-design-brief` receives the core or a
   narrower entry, and whether *replacement of an existing artefact* is better owned by
   `implementation-spec`.
3. Apply observation **I-1** — one sentence in `blueprint-contract.md` recording where the
   `not-authorized` pair (outcome basis + architectability basis) is persisted when no blueprint artefact
   is produced.
4. Apply observation **I-2** — reword `architecture-story.template.md`'s *"why it won over alternatives"*
   to *"the justification the decision recorded"*, closing the one wording in the layer that invites a
   comparative sentence.
5. When the deliverable templates render a headless architecture for the first time end to end, re-check
   that **no** deliverable section reintroduces a surface expectation (a screens table, a persona list) —
   the layer refuses to fabricate one, and the deliverables must not ask it to.
6. Apply observation **I-3** (§26.9) — add the third value to `architecture-core.md`'s scope-ownership
   column hint, for a responsibility whose destination is an emitted candidate set rather than a
   selected relocation.

---

---

## 26. Class-6 scope-pair coverage addendum (2026-09-04)

**Bounded addendum. It supplements the 19-fixture gate and replaces none of it.** The original
F-1…F-19 corpus was not reopened, no fixture result changed, Step 5A was not redesigned, Step 3 and
Step 4 were not reopened, no research was performed and no runtime file was modified.

### 26.1 Why this addendum exists

§10.3 claimed class-6 emitted-pair behaviour was exercised through F-6's second scope. F-6 emits
`(case management, class 2)` + `(analytical copy, class 2)` — **no class 6**. The claim was false and is
corrected in §10.3. The consequence is a **coverage gap, not a known runtime defect**: the frozen
class-6 architecture rule had not been behaviourally exercised.

### 26.2 The frozen class-6 semantics used

Read from the current runtime, not paraphrased.

`decision-model/outcome-classes.md` §1, row 6 — **EXCLUDED FOR THIS RESPONSIBILITY**:

> Emitted when: *"A responsibility-scoped disqualifier fires and no in-scope hybrid shape is available,
> or the responsibility **is** the whole deliverable. **Names the responsibility**"*
> Render: *"`<The platform>` is excluded for `<the named responsibility>`. It may remain the correct
> answer for `<the surrounding scope>`."* — and the outcome **must say so**. **Followed by class 8.**

Three consequences that shape the fixtures:

1. **The class-6 sentence itself asserts that the platform *may remain the correct answer* for the
   surrounding scope.** That phrase is mandatory content of the outcome, and it is exactly the phrase a
   careless reasoner would treat as an authorization. It is a permission-neutral statement about a scope
   Options may not have assessed at all.
2. **Class 6 is followed by class 8** — *candidate set, comparative fit `UNEVALUATED`*. The excluded
   responsibility's destination is therefore a **candidate set, never a selected relocation**.
3. `outcome-classes.md` §0 rule 2: every non-platform terminal outcome carries
   `COMPARATOR EVIDENCE ABSENT` unless §4 says otherwise, as part of the outcome.

Step 5A / `architecture-templates/README.md` §3:

| Rule | Exact text |
|---|---|
| Reachability, class 6 | *"**no** for the named responsibility"* · Scope: *"surrounding scope only where a pair was **emitted**"* · *"Never infer the surrounding scope's authorization from the exclusion of the responsibility"* |
| Authorization vocabulary | *"`authorized-bounded` ← an emitted class 3 or 4 pair, **or class 6's surrounding scope** AND the PP-owned side is architectable; the far side never is"* |

Read together, the two are consistent and not in tension: the second names the **value** the surrounding
scope takes *once its own pair exists* (bounded, because a responsibility is carved out of it); the first
governs **whether** it exists at all (only where a pair was emitted). C6-A tests the first, C6-B the
second.

### 26.3 C6-A — class 6 with no emitted surrounding authorization

**Frozen engagement state (smallest valid).** The class-6 trigger used is the second one — *the
responsibility **is** the whole deliverable*, which is what makes "no surrounding pair" a valid state
rather than an omission.

A distribution department asked for one capability: a **public integration interface that third-party
metering systems call directly** to submit readings. That interface is the whole deliverable. A
responsibility-scoped disqualifier fired on Confirmed evidence: the platform's external-audience surface
is documented as *not intended as a third-party integration surface*, and a public interface surface sits
in custom-development territory. No in-scope hybrid shape is available, because there is no surrounding
on-platform application to keep — the responsibility is the deliverable.

**Frozen decision record:**

```text
(public third-party metering-intake interface, class 6)
  "The platform is excluded for the public third-party integration interface.
   It may remain the correct answer for the surrounding internal meter-review workflow."
  → followed by class 8:
  "Candidates: custom development · packaged product. Comparative fit UNEVALUATED —
   engagement assessment required: a public-interface throughput and availability assessment."
  COMPARATOR EVIDENCE ABSENT

selected solution: none — a candidate set was emitted, nothing was selected
```

The surrounding scope **is named in the sentence** (the template compels it) and **no pair was emitted
for it**: the internal meter-review workflow was never assessed and is not in the decided scope.

| Record | Value |
|---|---|
| Frozen `(scope, outcome)` pairs | one: `(public third-party metering-intake interface, class 6)` → class 8 |
| Selected solution per scope | **none** — candidate set, nothing selected |
| Outcome reachability | **not reachable** — class 6 is *no* for the named responsibility |
| Pack architectability | **false**, independently — *a candidate set with no selected architecture* |
| Authorization | `not-authorized`, with both reasons stated separately |
| Architecture produced | **NO** |
| Architecture scope | none |
| Treatment of the class-6 responsibility | the emitted sentence verbatim, plus the class-8 candidate set and `COMPARATOR EVIDENCE ABSENT`. Nothing else |
| Domain Knowledge pulls | **0** |
| Surrounding authorization | **none** — not inferred, not sourced, not invented |
| Decision leakage | none |
| Comparator inference | none |
| **Verdict** | **PASS** |

**The adversarial core, and what the layer did with it.** The entry gate read the pair, found no emitted
class 1/2/3/4/13(a) pair for any scope, and produced no architecture. It did **not** treat *"It may remain
the correct answer for the surrounding internal meter-review workflow"* as an authorization for that
workflow. Explicitly absent from the output:

```text
responsibility excluded → therefore the rest stays on PP   : ABSENT
an inferred PP authorization                                : ABSENT
an invented surrounding scope or architecture               : ABSENT
a PP architecture generated from class 6 alone              : ABSENT
a Decision Blocked relabelling                              : ABSENT
a comparator-fit inference about custom or packaged          : ABSENT
```

What the layer said instead: *no PP architecture was produced, because the outcome is not reachable for
this responsibility and no other scope carries an emitted pair; the responsibility's destination is an
emitted candidate set whose comparative fit is `UNEVALUATED`.* Architecture-containing output was skipped
with that reason and logged to `render-log.md` — a skip, not a render gap.

**PASS: the absence of the second pair prevented architecture authorization.**

### 26.4 C6-B — class 6 with its own emitted surrounding PP pair

**Frozen engagement state (smallest valid).** A works-management engagement with two decided scopes.

*Surrounding scope S* — the internal works-order experience and human workflow: 90 internal users
(directory identity, Confirmed), planners raise and supervisors approve and technicians close; per-owner
row access required (Confirmed); relational navigation across works order → tasks → assets required
(Confirmed), which the list store cannot express; tamper-evident audit **not** required for the works
order itself — versioning accepted by the governance owner, funded and dated (Confirmed).

*Responsibility R* — the **statutory safety-certificate archive** for those works orders: the certificate
must be retained under legal hold with tamper-evident immutability and per-record hold release, which the
platform's stores do not express (Confirmed responsibility-scoped disqualifier). No in-scope hybrid shape
is available, because the archive must be the **authority** for the certificate and not a copy. The
engagement has **not** identified who or what will own it — no cloud-native team assessed, no incumbent
archive named, no product selected.

**Which class S carries — derived, not assumed.** Class 1 is unavailable: its trigger requires *no
disqualifier of any scope*, and a responsibility-scoped disqualifier fired. Classes 3 and 4 are
unavailable for R by construction: class 6's own trigger is that **no in-scope hybrid shape is
available**. Class 2's trigger is satisfied — one caution signal (no tamper-evident audit on the works
order) with a **funded, owned, dated** mitigation carried as a condition. So S's canonical emitted class
is **2**.

**Frozen decision record:**

```text
(works-order experience and human workflow, class 2)
  "Viable for this scope, provided: versioning accepted in place of a tamper-evident audit trail
   — Governance owner — funded: yes — confirmed 2026-08-14."
  selected solution: a PP record-centric application over the governed relational store

(statutory safety-certificate archive, class 6)
  "The platform is excluded for the statutory safety-certificate archive.
   It may remain the correct answer for the surrounding works-order experience and human workflow."
  → followed by class 8:
  "Candidates: packaged records-management product · custom development · cloud-native archive service.
   Comparative fit UNEVALUATED — engagement assessment required:
   a legal-hold and immutability conformance assessment."
  COMPARATOR EVIDENCE ABSENT
  selected solution: none
```

| Record | Value |
|---|---|
| Frozen `(scope, outcome)` pairs | **two, uncollapsed**: `(works-order experience and human workflow, class 2)` · `(statutory safety-certificate archive, class 6)` → class 8 |
| Selected solution per scope | S: PP record-centric application over the governed relational store · R: **none** (candidate set) |
| Outcome reachability | S: **reachable** (class 2) · R: **not reachable** (class 6 is *no* for the named responsibility) |
| Pack architectability | S: **true** — a PP application in an experience mode the pack covers · R: **false** — no selected architecture, and the far side of a pair is never architectable here |
| Authorization | **`authorized-bounded`** for S only. Derivation: an emitted class-2 pair for S establishes that an authorization exists; the class-6 carve-out inside S is what makes it **bounded** rather than plain `authorized`, per README §3 (*"or class 6's surrounding scope … the far side never is"*) |
| Architecture produced | **YES**, for S only |
| Architecture scope | works-order experience and human workflow |
| `experience.mode` | `owned-internal` · `primary_surface: record-centric app` · 1 experience fragment |
| `record_authority` | 1 entry — works orders and tasks · governed relational store · `owned`. **The certificate is not an entry**: its authority is R's, and R's authority is unevaluated |
| `compositions` | 1 — `works-order-store-access` · `direct` · `in-platform` · `forced_by`: *"no requirement forces escalation on the internal workflow"* |
| `relocated_responsibilities` | **`[]` — empty.** See §26.5 |
| N/M → fragments | **0/0 → 0** boundary/import fragment instances. Invariant holds |
| Treatment of the class-6 responsibility | see §26.5 |
| Domain Knowledge pulls | **9**, all for S. Max 2 in one section (A5: `store-boundaries` → `data/dataverse`, forced — relational navigation plus per-owner row access). **0 pulls for R** |
| Surrounding authorization source | **independent emitted pair** |
| Decision leakage | none |
| Comparator inference | none |
| **Verdict** | **PASS** |

**The central invariant, stated as required.** *This authorization would still exist if the class-6 row
were removed, because it originates from the surrounding scope's own emitted class-2 pair.* Precisely:
removing the class-6 row would change the authorization's **value** from `authorized-bounded` to
`authorized` — because the carve-out is what bounds it — but it would **not** change the authorization's
**existence or its source**. Nothing about S's architecture authority derives from R's exclusion. The
inverse test was also run: **removing S's class-2 pair and keeping the class-6 row leaves nothing
authorized** — which is C6-A.

**Both pairs remain uncollapsed** in A1, in the conditional scope-ownership table and in the synthesis
narrative. The class-6 sentence and the class-2 sentence are each rendered verbatim, on their own line,
against their own named scope.

### 26.5 Class-6 boundary behaviour in C6-B

**What the excluded responsibility received** — only what the frozen decision actually supports:

| Field | Value rendered |
|---|---|
| Responsibility name | statutory safety-certificate archive |
| Exclusion outcome basis | the class-6 sentence, **verbatim** |
| Owner | **UNEVALUATED** — an emitted candidate set exists; no owner is selected |
| Boundary | **not decided** — recorded as undetermined, because the counterparty is unselected |
| Evidence boundary | explicit: this pack has no evidence about any candidate archive's internals, fit, cost or roadmap; `COMPARATOR EVIDENCE ABSENT` carried from the outcome |
| Obligation on the PP side | works-order closure must hand the certificate to the archive once one is selected; the **hand-off mechanism cannot be chosen until the archive is** |

**What it did not receive:** no PP design; no invented far-side design; no components; no data model; no
technology naming; no operational model; no claimed suitability; no boundary fragment.

**The obligation is carried as a structural open architecture choice**, not as a fabricated component:

```yaml
open_architecture_choices:
  - choice: certificate hand-off mechanism to the statutory archive
    structural: true
    would_be_settled_by: the archive selection — the emitted candidate-set assessment (class 8)
    su_ref: U-0xx
```

It is `structural: true` because the mechanism choice adds or removes a boundary component and therefore
changes N, A6, A7, A8 and A10. **Blueprint production proceeded; approval is blocked** — the honest
result, and one reached without inventing a counterparty. A6 carries the stream as
*"certificate hand-off — mechanism undetermined pending archive selection"*, with an explicit statement
that no guarantee, failure semantics or idempotency basis can be committed until the counterparty exists.

### 26.6 No manufactured relocation — and the contract enforces it

The temptation is to record R as a `relocated_responsibilities[]` entry because the responsibility left
the platform. **The architecture contract itself forbids it**, on two independent fields:

```text
relocated_responsibilities[].owner
    : <incumbent system | cloud-native services | named external team>   → R has none selected
relocated_responsibilities[].outcome_basis
    : <the emitted class 3 or class 4 sentence, verbatim>                 → R's sentence is class 6
```

A class-6 exclusion satisfies neither field, so representing it as a relocation would require
fabricating an owner and mis-attributing an outcome class. The layer left `relocated_responsibilities:
[]` and put R in the conditional **scope-ownership** table instead — the sanctioned home for a
responsibility this pack does not describe. Consequences checked:

- **Class 6 was not converted into class 3** (no cloud-native destination asserted) **or class 4** (no
  incumbent asserted, and `INCUMBENT FIT UNEVALUATED` was **not** emitted — there is no incumbent in this
  fixture, and emitting that marker would have invented one).
- **R does not appear in the A3 boundary table.** The table's membership rule is `compositions[]` ∪
  `record_authority[]` ∪ `relocated_responsibilities[]`, and R is in none of the three. This is correct
  rather than an omission: three of the table's six columns (platform governance, owner, data
  classification) would have to be invented for a counterparty that does not yet exist. R's home is the
  scope-ownership table, where *unevaluated* is a legitimate value.
- **No diagram** was produced (no composed or asynchronous path exists on the PP side), so the
  *no diagram-only component* rule is trivially satisfied.

### 26.7 No reverse inference

Each prohibited inference was searched for explicitly in both subcases' outputs.

| Reverse inference | C6-A | C6-B |
|---|---|---|
| class 6 responsibility → surrounding PP fit | **ABSENT** | **ABSENT** — S's fit comes from S's own class-2 pair and its own evidence |
| class 6 responsibility → PP architecture for the remaining scope | **ABSENT** (no architecture at all) | **ABSENT** — the architecture is authorized by S's pair, and the report states the counterfactual |
| class 6 responsibility → external solution fit | **ABSENT** — the class-8 candidates carry `UNEVALUATED` | **ABSENT** — all three candidate archives carry `UNEVALUATED` |
| class 6 responsibility → comparator winner | **ABSENT** | **ABSENT** |

Nothing in either output asserts preference, superiority, cost or capability about a class the pack has
not evaluated — `outcome-classes.md` §0 rule 1 held in both.

### 26.8 Domain Knowledge pull behaviour

```text
C6-A architecture Domain Knowledge pulls : 0
C6-B architecture Domain Knowledge pulls : 9  (median 1 per material section, max 2)
C6-B pulls made to re-evaluate R         : 0
```

C6-A pulled nothing, as expected: with no authorization there is no architecture responsibility to
describe. C6-B pulled only for the independently authorized scope S. **Critically, no unit was pulled to
re-check whether the platform can express tamper-evident immutability or per-record legal hold** — that
finding is frozen in R's emitted outcome, and re-verifying it would have been an Options re-run. Neither
`security/security-controls.md` nor any store unit was opened on R's behalf.

### 26.9 Addendum findings

No failure in either subcase, so no repair is required and no runtime change was made. One
documentation-level observation, consistent in kind with §23.2's I-1 and I-2:

**I-3 — the scope-ownership column's enumerated values do not cover an unselected destination.**
`architecture-core.md`'s scope-ownership table hints its last column as
`<yes — A4…A12 | no — one boundary fragment instance>`. For a class-6 responsibility whose destination is
an emitted candidate set, the honest value is a third one — *no, and no boundary fragment either, because
no counterparty is selected*. The hint is template guidance in angle brackets, not an enforced
enumeration, so C6-B rendered the honest third value without difficulty and **no fixture failed**.
Smallest bounded repair, if taken: add that third value to the column hint. **Recommended as a Step 6
item, not a Step 5 blocker.** Classification: **I — context ceremony (documentation)**.

### 26.10 Addendum result

| Check | Result |
|---|---|
| C6-A executed | ✔ |
| C6-B executed | ✔ |
| class 6 alone authorizes the surrounding scope | **NO** |
| surrounding authorization independently sourced in C6-B | **YES** — emitted class-2 pair |
| class-6 responsibility received a PP design | **NO** |
| far-side design invented | **NO** |
| relocation manufactured from class 6 | **NO** — contract forbids it on two fields |
| class 6 converted to class 3 or class 4 | **NO** |
| pairs collapsed | **NO** |
| Decision Blocked invented | **NO** |
| comparator or fit inference | **NO** |
| decision leakage | **NO** |
| original F-1…F-19 results changed | **NO** |
| runtime modified | **NO** |

**C6-A: PASS. C6-B: PASS.** The frozen class-6 architecture rule — *an exclusion for one responsibility
does not authorize its surrounding scope; the surrounding scope is architectable only where its own
outcome pair was emitted* — is now behaviourally exercised in both directions. The Step 5 freeze
condition in §11 of the addendum commission is met.

---

`STEP 5C — ARCHITECTURE SEMANTIC/BEHAVIOURAL GATE: PASS`
`FIXTURES EXECUTED: 19/19`
`FIXTURE FAILURES: 0`
`AUTHORIZATION / ARCHITECTABILITY: PASS`
`F-17 NON-PP POSITIVE OUTCOME: PASS`
`F-18 13A OUTSIDE PACK AUTHORITY: PASS`
`HEADLESS ARCHITECTURE: PASS`
`EXPERIENCE MODES: PASS`
`EMPTY RECORD-AUTHORITY SEMANTICS: PASS`
`F-19 COMPONENT COLLISION: PASS`
`N+M FRAGMENT INVARIANT: PASS`
`SIX-CHANNEL IMPORT CARRIAGE: PASS`
`SCOPE-PAIR BEHAVIOUR: PASS`
`FAR-SIDE ARCHITECTURE INVENTED: NO`
`STRUCTURAL OPEN-CHOICE BEHAVIOUR: PASS`
`EPISTEMIC PRESERVATION: PASS`
`VOLATILE-VALUE HANDLING: PASS`
`PROOF-OBLIGATION CARRIAGE: PASS`
`DOMAIN KNOWLEDGE PULL DISCIPLINE: PASS`
`CRAFT BOUNDARY: PASS`
`DECISION LEAKAGE DETECTED: NO`
`COMPARATOR BIAS DETECTED: NO`
`UNSUPPORTED ARCHITECTURE CLAIMS INVENTED: 0`
`MEDIAN RESEARCH PULLS PER MATERIAL SECTION: 1`
`MAX RESEARCH PULLS FOR ONE MATERIAL SECTION: 2`
`UNNECESSARY THIRD-PLUS PULLS: 0`
`WHOLE PATTERN CATALOGUE SCANS: 0`
`SYSTEMIC CONTEXT-CEREMONY DETECTED: NO`
`RUNTIME MODIFIED DURING INITIAL GATE: NO`
`NEW RESEARCH PERFORMED: NO`
`ARCHITECTURE LAYER DEFENSIBLE: YES`
`READY TO FREEZE STEP 5 — ARCHITECTURE TEMPLATES: YES`

`STEP 5C — CLASS-6 COVERAGE ADDENDUM: PASS`
`C6-A CLASS-6 WITHOUT SURROUNDING PAIR: PASS`
`C6-A PP ARCHITECTURE GENERATED: NO`
`C6-B CLASS-6 WITH INDEPENDENT SURROUNDING PAIR: PASS`
`C6-B SURROUNDING PP ARCHITECTURE AUTHORIZED: YES`
`SURROUNDING AUTHORIZATION SOURCE: INDEPENDENT PAIR`
`CLASS-6 RESPONSIBILITY RECEIVED PP DESIGN: NO`
`FAR-SIDE FIT INFERRED: NO`
`DECISION LEAKAGE DETECTED: NO`
`DOMAIN KNOWLEDGE PULLED FOR C6-A: 0`
`RUNTIME MODIFIED DURING ADDENDUM: NO`
`ORIGINAL F-1...F-19 RESULTS CHANGED: NO`
`STEP 5C REPORT COVERAGE CLAIM CORRECTED: YES`
`READY TO FREEZE STEP 5 — ARCHITECTURE TEMPLATES: YES`

---

## 27. Step 5 freeze marker (appended 2026-09-04 — documentation only)

Appended at the opening of Step 6A. No analysis was re-run, no fixture re-executed, no runtime file
touched, and no verdict in §1–§26 altered.

```text
STEP 5C — ARCHITECTURE SEMANTIC/BEHAVIOURAL GATE: PASS
F-1...F-19: 19/19 PASS
CLASS-6 ADDENDUM: PASS
C6-A: PASS
C6-B: PASS
SURROUNDING AUTHORIZATION INFERRED FROM CLASS 6: NO
FAR-SIDE ARCHITECTURE INVENTED: NO
DECISION LEAKAGE: NO
COMPARATOR BIAS: NO
ARCHITECTURE LAYER DEFENSIBLE: YES
RUNTIME MODIFIED DURING GATE/ADDENDUM: NO
READY TO FREEZE STEP 5: YES
STEP 5 — ARCHITECTURE TEMPLATES: FROZEN
```

The three carried observations (**I-1**, **I-2**, **I-3**) and the two carried Step 5A open questions
pass to Step 6 for resolution in the deliverable/synthesis layer. Their resolution designs are recorded
in [`step-6a-deliverable-projection-model.md`](step-6a-deliverable-projection-model.md) §21–§24.
