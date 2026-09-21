# Anti-pattern single-home table (authoring-side · Step 4B §30)

Canonical set: **68 entries** = 61 `ANTI-PATTERN` + 3 `GATE` + 4 `CONSTRAINT`
(`GATE`: AP-D-013, AP-D-026, AP-D-059 · `CONSTRAINT`: AP-D-031, AP-D-044, AP-D-051, AP-D-067 ·
portfolio altitude: AP-D-004).

**Precedence applied** (Step 4A §11.1): decision model (if it can make an option unavailable) → a
failure-mode note in the owning knowledge unit → an architecture-composition concern → authoring-only.
**Ids are authoring-side only and appear in no runtime file.** Lower levels may cross-reference; none
restates a normative rule owned above it.

| Behaviour | Primary runtime home | Secondary reference(s) |
|---|---|---|
| Solution named before the problem is characterised | decision model — S0/S1 + reachability floor | — |
| Selection by precedent — familiarity or resemblance | decision model — comparator discipline | — |
| Low-code selected where a hard non-functional requirement dominates | decision model — S2/S3 absolutes + blocking set | — |
| **One platform for every workload class** | **authoring-only** — portfolio altitude; must never surface as an engagement finding. Its mechanisms fire through shape mismatch, analytics-on-operational-store, over-/under-governance and shared-capacity contention | — |
| Starting above the simplest sufficient structure | `architecture/patterns.md` — escalation ladder | — |
| Structure never de-escalated | `architecture/patterns.md` — escalation ladder | — |
| Rebuilding what an existing capability already provides | decision model — S1 rung-0 / alternatives register | `application/application-surfaces.md` (rung-0 boundary) |
| Document or spreadsheet store as the relational system of record | `data/store-boundaries.md` failure mode | — |
| The operational store serving the analytical workload | `data/store-boundaries.md` §6 failure mode | `performance/performance-and-scale.md` |
| Shadow system of record | `data/store-boundaries.md` — authority per entity/field/phase | `integration/integration-mechanisms.md` (sync scope defaults to minimum) |
| Bidirectional synchronisation without field ownership and reconciliation | `data/store-boundaries.md` failure mode | `integration/integration-mechanisms.md` §7.1 risk row (mechanism only) |
| Data virtualization chosen without its exclusion list | `data/store-boundaries.md` §7 failure mode | `data/dataverse.md` (virtual-table semantics) |
| **Replica trusted without drift detection** | **decision model — `GATE`** (material data); composed row CD-08 | `data/store-boundaries.md` §6 — the divergence *mechanism* only, no availability verdict |
| System of record undeclared | decision model — blocking entry B-04 | `data/store-boundaries.md` §5 (vocabulary is pack-local) |
| Automation shape mismatch · workflow engine as a high-volume transaction engine · transaction semantics hand-built in orchestration logic | `automation/automation-mechanisms.md` — **folded into ONE decision-sensitive distinction**: a shape-2/3/4 requirement built as shape 1 | `architecture/patterns.md` |
| Retry enabled on non-idempotent writes | `automation/automation-mechanisms.md` §11 (the worked note) | `integration/integration-mechanisms.md` §7 (at-least-once ⇒ duplicates) |
| Synchronous chain across heterogeneous availability | `automation/automation-mechanisms.md` §11 | `integration/integration-mechanisms.md` |
| UI automation where a stable interface exists or can be built | `automation/automation-mechanisms.md` §9 | `integration/integration-mechanisms.md` §11 |
| Automation with no observability and no throttling owner | `automation/automation-mechanisms.md` §7 (throttling rate as a monitored leading indicator with a named owner) | `operations/operability-and-support.md` |
| Point-to-point proliferation | `integration/integration-mechanisms.md` §4 topology test + §9 ownership test | `architecture/patterns.md` |
| Mediation layer with no requirement behind it | `integration/integration-mechanisms.md` §6 — *when mediation is unnecessary complexity* | `architecture/patterns.md` |
| Polling below the mechanism's own freshness floor | `integration/integration-mechanisms.md` §5 (polling envelope, freshness floor) | `automation/automation-mechanisms.md` §11 (the per-source trade-off) |
| Integration seam without contract lifecycle ownership | `integration/integration-mechanisms.md` §3 dim 11 + §9 | `alm/release-and-lifecycle.md` |
| **External component adopted without an operator** | **decision model — `GATE`**; composed row CD-02 | `architecture/patterns.md` (a pattern imports a *named operator*) · `operations/operability-and-support.md` |
| Existing integration ownership bypassed | `integration/integration-mechanisms.md` §4 step 1 | `governance/governance-and-environments.md` |
| One integration decision per system pair instead of per stream | `integration/integration-mechanisms.md` §3 (stream inventory) + §15 | — |
| Authorization model deferred past an irreversible decision | `security/security-controls.md` — irreversible decisions | `data/dataverse.md` (ownership type immutable) |
| Application UI treated as the authorization layer | `security/security-controls.md` — the lowest-plane rule's **worked negative case** | — |
| **Secrets held in makers' assets** | `security/security-controls.md` failure-mode note — `CONSTRAINT`, carrying the scope statement that bounds it | `automation/automation-mechanisms.md` §9 (the anti-home for secrets) |
| Shared identity as the access or integration model | `security/security-controls.md` — the shared-identity failure | `integration/integration-mechanisms.md` §8 · `data/azure-sql.md` |
| One control treated as the whole control | `security/security-controls.md` — partial-by-design controls | — |
| External or anonymous surface exposed with unreviewed permissions | `security/security-controls.md` | `application/application-surfaces.md` (identity class) |
| Network and deployment constraints discovered after platform selection | decision model — S2 absolutes; blocking entries B-05, B-10 | `integration/integration-mechanisms.md` §11 · `governance/governance-and-environments.md` |
| **Agent surface treated as covered by the app and flow access model** | decision model — scope-blocker BS-03 → `UNKNOWN` / decision blocked | `security/security-controls.md` states only that the access model is **not established**. **No agent domain file exists** |
| Maker enablement without ownership or a promotion path | `governance/governance-and-environments.md` | `alm/release-and-lifecycle.md` |
| Uncontrolled environment proliferation | `governance/governance-and-environments.md` — environment topology, blast radius | — |
| Policy without an operating model | `governance/governance-and-environments.md` — preventive vs detective, control ownership | `operations/operability-and-support.md` |
| **Enterprise controls imposed on a trivial workload** | `governance/governance-and-environments.md` — **the over-governance half of the matched pair**; both halves are carried deliberately | — |
| Production workload in a non-production environment class | `governance/governance-and-environments.md` | `alm/release-and-lifecycle.md` (rungs) |
| Development in production | `alm/release-and-lifecycle.md` — rung 0, what it does not provide | `governance/governance-and-environments.md` |
| Business-critical solution without source control | `alm/release-and-lifecycle.md` — the source-controlled rung | — |
| Manual deployment as the permanent operating model | `alm/release-and-lifecycle.md` | — |
| **Environment-specific values shipped inside the release artefact** | `alm/release-and-lifecycle.md` failure-mode note — `CONSTRAINT`, with its scope statement (connection references / environment variables) | — |
| Rollback assumed to exist | `alm/release-and-lifecycle.md` — **there is no rollback** | `operations/operability-and-support.md` (recovery ≠ rollback) |
| Single-sided supply chain for a two-sided architecture | `alm/release-and-lifecycle.md` — cross-boundary release as a second supply chain | `operations/operability-and-support.md` (deployment ownership) · `automation/automation-mechanisms.md` §12 (hybrid = second operating model) |
| Unmanaged artefact structure above the departmental class | decision model — composed row CD-11 (*in-place remediation unavailable — migration required*) | `alm/release-and-lifecycle.md` |
| Documented limits read as performance guarantees | `performance/performance-and-scale.md` — the limit-vs-proof rule, **stated once** | — |
| Sizing against a single meter | `performance/performance-and-scale.md` — five meters, smallest binds | `automation/` · `integration/` (their own meter subsets) |
| Non-delegable access path over a growing dataset | `data/query-and-delegation.md` | `data/sharepoint.md` · `data/store-boundaries.md` (cross-reference only) |
| **Inventing the number the platform does not publish** | **decision model only — `CONSTRAINT`** (the spine's own reasoning rule). **Deliberately not restated in domain knowledge** | — |
| Validation level not matched to the commitment being made | decision model — the four proof levels | `performance/performance-and-scale.md` says *what* must be proven, **never the ladder** |
| Business-critical application with no monitoring and no incident owner | `operations/operability-and-support.md` | `governance/governance-and-environments.md` |
| Recovery assumed rather than designed and drilled | `operations/operability-and-support.md` — backup ≠ recovery, drills | decision model composed row CD-04 |
| Platform commitment quoted as the solution's commitment | `performance/performance-and-scale.md` — the end-to-end vs platform-availability distinction | `operations/operability-and-support.md` (what evidence underwrites a commitment) |
| Preview or unsupported components on a critical path | `operations/operability-and-support.md` | every unit's *what must be verified* → `VC-10` |
| Unmanaged platform-change exposure | `operations/operability-and-support.md` | `governance/governance-and-environments.md` |
| **No retirement lifecycle** | `operations/operability-and-support.md` failure-mode note — `CONSTRAINT`, with its scope statement | `economics/licensing-and-cost-drivers.md` (sunk capability) |
| **Composed disqualifier ignored** | **decision model — `GATE`**; the composed register itself | — |
| Case built on transition-period or preview terms | `economics/licensing-and-cost-drivers.md` | tripwires `TW-V1`, `TW-V2`, `TW-V3` · `performance/` (transition-period request figures) |
| Licence line treated as the total cost of ownership | `economics/licensing-and-cost-drivers.md` | — |
| Licence-avoidance architecture | `economics/licensing-and-cost-drivers.md` — the trap, at economic altitude | `data/store-boundaries.md` §9 — the *store-choice* instance of it |
| Entitlement boundary discovered after the design is fixed | `economics/licensing-and-cost-drivers.md` | `governance/governance-and-environments.md` (licence chain) |
| Consumption without an owner or a growth model | `economics/licensing-and-cost-drivers.md` | `operations/operability-and-support.md` |
| Operational and security prerequisites omitted from the cost model | `economics/licensing-and-cost-drivers.md` | `security/security-controls.md` (control-obliged population) · `operations/` |
| Cheap start on a path to criticality | `economics/licensing-and-cost-drivers.md` | `operations/operability-and-support.md` (maturity classes) |
| Cheap ownership of business-critical automation | `economics/licensing-and-cost-drivers.md` | `automation/automation-mechanisms.md` §12 (owner identity is architectural) |
| User-experience and interaction candidates from the canonical ledger | `application/application-surfaces.md` notes where the entry names one surface mechanism; **the remainder authoring-only** — several are already absorbed into the Discovery C3 signals | — |

## Duplication control result

- No behaviour has two **primary** homes.
- No normative rule owned by the decision model is restated in a knowledge unit; where a unit touches one,
  it carries the *mechanism* and cross-references, never the availability verdict.
- The three `GATE` entries and the reasoning `CONSTRAINT` stay decision-model-only.
- **68 of 68 accounted for. 0 copied into runtime as an encyclopedia entry.** Runtime carries roughly
  30 mechanism-level failure-mode notes across the units, not 68 catalogue rows.

## One adjudicated fold, recorded rather than improvised

Step 4A §11.3 states the automation family *"is largely one error — a shape-2/3/4 requirement built as
shape 1 — so it becomes **one** decision-sensitive distinction, not N notes."* Applied literally, three
entries fold into that single distinction (shape mismatch · workflow engine as a high-volume transaction
engine · hand-built transaction semantics). The remaining four automation entries were **kept as separate
notes** because each names a distinct mechanism that the shape distinction does not imply — retry
duplication, heterogeneous-availability coupling, the UI-automation interface test, and the
throttling-owner requirement. Recorded here as an adjudication, not as a deviation from the design.
