Research Status: CANONICAL
Research Confidence: MEDIUM
Block: D — Decision Intelligence
Area: 13 — Anti-Patterns
Gate: PASS — Block D Final Bounded Gate Recheck
Canonicalization Basis: Block D Final Bounded Gate Recheck (`block-d-final-gate-recheck.md`)
Upstream Evidence Baseline: Areas 1–12 canonical files (`canonical-manifest.md`)
Canonicalized: 2026-09-03
Freeze Status: FROZEN FOR PP PACK AUTHORING

# Anti-Patterns — Block D Research Evidence

Research area: **13 — Anti-Patterns** (`../research-areas.md`).
Derivation date: **2026-09-03**.
Primary input: `canonical-manifest.md` and the twelve canonical Area 1–12 files it names.
Source policy: `../source-policy.md`.
Peer files: `alternatives.md` (Area 14), `decision-criteria.md` (Area 15), `decision-intelligence-matrix.md`.

**Purpose.** Extract, from the canonical evidence base, the recurring structures that create material risk — and state, for each, *what decision should change when it is detected*. This file is a decision-support layer over Areas 1–12, not a new body of Power Platform guidance and not a style guide.

**What this file is not.** It is not a list of implementation defects. Areas 1–12 already own those, and they stay there: nested `For each` loops (`automation-architecture.md` AT2-54), overloaded `OnStart` (`performance-scale.md` PF-AP-03), leading-wildcard `contains` (`data-architecture.md` DAP-26), cross-screen control references (`performance-scale.md` PF-AP-05) and their peers are code-review findings, not decision inputs. Block D promotes an item only when detecting it should change a **platform, architecture, scope, ownership or proceed/stop decision**.

**Reading rule.** Nothing here is pack content. No question bank, no signal catalogue, no decision tree. The `Detection Signals` fields are *pointers* for a later authoring step, not authored signals.

---

## 1. Identifier namespace, and why it is new

### 1.1 The namespace chosen

Block D anti-patterns use **`AP-D-NNN`**.

### 1.2 Why not `AP-NNN`

The `AP-` prefix is already **overloaded** across the canonical corpus, and a further reuse would break the manifest's `AMBIGUOUS REFERENCES: 0` guarantee at the first downstream regex:

| Existing namespace              | Owner                            | Meaning                                              | Range     |
| ------------------------------- | -------------------------------- | ---------------------------------------------------- | --------- |
| `AP-01` … `AP-10`               | `architecture-patterns.md` §4    | **Patterns** (Direct, API-mediated, Event-driven, …) | 2-digit   |
| `AP-1` … `AP-16`                | `platform-suitability.md` §5     | **Anti-patterns**                                    | 1–2 digit |
| `AP-17` … `AP-35`               | `application-architecture.md` §4 | **Anti-patterns** (continues the PS series)          | 2-digit   |
| `PF-AP-*`, `LC-AP-*`, `OP-AP-*` | Areas 9, 10, 11                  | Area-local anti-patterns                             | qualified |
| `DAP-*`                         | Area 3                           | Area-local anti-patterns                             | qualified |
| `SEC-A*`, `GOV-A*`, `ALM-A*`    | Areas 6, 7, 8                    | Area-local anti-patterns                             | qualified |
| `X-*` / `Y-*`                   | Areas 5 / 12                     | Implementation / selection anti-patterns             | qualified |

Two consequences are recorded rather than repaired (see §1.4):

- `AP-01`…`AP-10` (**patterns**) and `AP-1`…`AP-9` (**anti-patterns**) are distinguished only by a leading zero. A pattern reference and an anti-pattern reference can be one character apart, and `\bAP-0?[1-9]\b` matches both.
- A bare `AP-nn` reference is resolvable only from its file context. Block D therefore always writes peer references **file-qualified** — `platform-suitability.md AP-5`, never `AP-5`.

`AP-D-NNN` collides with none of the above (`grep -ohE '\bAP-D-[0-9]+\b' *.md` returned empty across the canonical corpus, checked 2026-09-03) and reads unambiguously as "Block D anti-pattern".

### 1.3 Other Block D namespaces

| Namespace | File | Collision check on canonical corpus, 2026-09-03 |
|---|---|---|
| `AP-D-NNN` | this file | clean |
| `ALT-NNN` | `alternatives.md` | clean |
| `DC-D-NNN` | `decision-criteria.md` | clean (`DC-NN` is **not** — see `decision-criteria.md` §1) |

### 1.4 Lineage defects observed, not repaired

Block D is an extraction pass and does not modify Areas 1–12. Two integrity observations are recorded here as evidence for a future bounded repair:

- **`licensing-cost.md` carries a duplicate `DC-14`.** Two distinct criteria share the id: *"Which security controls are mandatory and how many people are in their enforcement scope?"* (→ LC-30) and *"Does cost need to be attributed to business units?"* (→ LC-16). Manifest §4 records `DUPLICATE CANONICAL IDS: 0` and cites a *"Licensing/Cost `DC-14…DC-18` repair"*; in the mounted snapshot that repair is **incomplete**. Downstream must disambiguate `licensing-cost.md DC-14` by its question text, never by its number alone.
- **`AP-` overload** as described in §1.2.

Neither weakens the canonical architectural substance. Both weaken *mechanical* reference resolution, which is why Block D avoids both prefixes.

- **Classification:** CONSTRAINT · **Origin:** INF (mechanical inspection of the canonical corpus) · **Confidence:** HIGH

---

**Citation-form note (added 2026-09-03).** Two manifest reservations are cited in this file under their **qualified** names, `IA-U-14` and `IA-C-01`, because `pre-canonicalization-repair.md` records those as the canonical forms. The **mounted** `integration-architecture.md` still carries the unqualified `U-14` and `C-01`. A mechanical reference check against the mounted file will therefore report these two as unresolved; they are not errors, and every citation of them in this file now names both forms. This is the manifest's own lineage reservation made concrete, and it is **recorded, not repaired** — repairing Areas 1–12 is out of Block D's scope.

---

## 2. What qualifies as an anti-pattern here

The quality rule from the brief, applied literally. An item is accepted only when all four elements are present and evidenced:

| Element | Test |
|---|---|
| **CONTEXT** | There is a stated condition under which the structure is harmful — and, by implication, conditions under which it is not. A structure that is always wrong is a *constraint*, not an anti-pattern. |
| **FAILURE MECHANISM** | The *architectural* reason it fails is nameable and traceable to canonical evidence — not "Microsoft advises against it". |
| **CONSEQUENCE** | The damage is specific and lands somewhere identifiable (business, data, security, cost, operations, …). |
| **DECISION IMPACT** | Detecting it changes a decision. If detection changes only an implementation detail, the item belongs to Areas 1–12. |

**Three classifications, not one (repair, 2026-09-03).** The `Classification` field previously read `ANTI-PATTERN` on all 67 entries, including six that state `Exceptions: None` and supply a **scope boundary** in place of an exception. By this section's own test — *"A structure that is always wrong is a **constraint**, not an anti-pattern"* — those six are not context-conditional. §8 half-recognised this by naming three of them *"gates rather than risks"* without changing any `Classification` field. The field now carries one of three values, and a pack must render them differently:

| Classification | Meaning | How a pack renders it |
|---|---|---|
| **ANTI-PATTERN** | Harmful **in a stated context**, with real conditions under which the same structure is correct. 61 entries. | A contextual warning, evaluated against the `Exceptions` field |
| **GATE** | Where it holds, an option is **unavailable**, not merely worse. The `Exceptions` field states scope, not exemption. 3 entries: **AP-D-026**, **AP-D-059**, **AP-D-013** (for material data). | A **hard check**. Failing it removes the option from the candidate set; it is not overridable by a mitigation statement |
| **CONSTRAINT** | Always wrong within its stated scope; the `Exceptions` field bounds the scope rather than admitting exceptions. 4 entries: **AP-D-031**, **AP-D-044**, **AP-D-051**, **AP-D-067**. | A **rule**, checked and reported, not weighed |

The six the review identified are AP-D-026, AP-D-031, AP-D-044, AP-D-051, AP-D-059 and AP-D-067; AP-D-013 is added to the `GATE` set because §8 already named it one. The count is therefore **61 ANTI-PATTERN + 3 GATE + 4 CONSTRAINT = 68** (67 original entries plus AP-D-068, added below). Nothing was removed and no entry's evidence changed; only the field a pack reads to decide **how hard** to enforce it.

Three additional rules inherited from manifest §7:

1. **`INF` lineage is preserved.** Where the anti-pattern *framing* is synthesis over Microsoft-stated facts, the entry says so. No entry claims Microsoft endorsement for a synthesised boundary.
2. **`CONFLICTED` and `UNKNOWN` are preserved.** No entry converts an open conflict into a threshold. Where an anti-pattern is *precisely* "acting as if an open conflict were resolved", that is stated as the mechanism (AP-D-051).
3. **Absence of a Microsoft prohibition is not evidence of safety**, and absence of a published number is not licence to invent one.

### 2.1 The symmetry rule

An anti-pattern that says "do not use Power Platform here" must carry the same evidential burden as one that says "do not leave Power Platform here". Both directions appear in this file, deliberately:

- **Under-engineering** anti-patterns: AP-D-003, AP-D-008, AP-D-016, AP-D-018, AP-D-048.
- **Over-engineering** anti-patterns: AP-D-005, AP-D-006, AP-D-023, AP-D-039.

The corpus is explicit that it can argue the first direction more strongly than the second: *"No case documented where Power Automate is the correct choice at high volume, which means the corpus can argue against under-engineering but has no Microsoft-sourced ceiling for over-engineering"* (`automation-architecture.md` §8.7). The over-engineering entries therefore rest on Microsoft's minimal-complexity instruction and its own "not suitable when" statements rather than on limits, and are marked accordingly.

---

## 3. Candidate evaluation ledger

Every candidate from the brief, plus every candidate surfaced from the canonical corpus, with its verdict. This is the audit trail for §5.

**Verdicts:** `ACCEPTED` · `MERGED` (same failure mechanism as an accepted entry) · `REJECTED — Areas 1–12` (real, but an implementation defect with no decision impact) · `REJECTED — misclassified` (it is a constraint, a requirement or a risk, not a pattern).

### 3.1 Architecture and selection

| Candidate | Verdict |
|---|---|
| Power Platform selected before discovery | ACCEPTED — AP-D-001 |
| Architecture chosen by product familiarity rather than requirement fit | ACCEPTED — AP-D-002 |
| Pattern selected by resemblance to a reference architecture | MERGED → AP-D-002 (one mechanism: selection by precedent, not by requirement) |
| Low-code used where hard non-functional requirements dominate | ACCEPTED — AP-D-003 |
| Power Platform used as universal enterprise platform | ACCEPTED — AP-D-004 |
| Starting above the simplest sufficient structure | ACCEPTED — AP-D-005 |
| Structure never de-escalated when its forcing requirement disappears | ACCEPTED — AP-D-006 |
| Replicating the legacy system feature-for-feature | ACCEPTED — AP-D-007 |
| Building what a first-party / existing capability already covers | MERGED → AP-D-007 |
| Excessive coupling to platform-specific capabilities | MERGED → AP-D-002 for the selection failure; the portability *requirement* is DC-D-105/DC-D-106, not an anti-pattern in itself |

### 3.2 Data

| Candidate | Verdict |
|---|---|
| SharePoint used as enterprise relational database | ACCEPTED — AP-D-008 (generalised to any document/spreadsheet store) |
| Excel with more than one writer | MERGED → AP-D-008 |
| Operational and analytical workloads mixed incorrectly | ACCEPTED — AP-D-009 |
| Unnecessary Dataverse replication | ACCEPTED — AP-D-010 (generalised: shadow system of record) |
| Bidirectional synchronization without ownership/reconciliation model | ACCEPTED — AP-D-011 |
| Virtual tables selected without understanding their feature/security limits | ACCEPTED — AP-D-012 (generalised: data virtualization without its exclusion list) |
| Replica trusted without drift detection | ACCEPTED — AP-D-013 |
| Multiple uncontrolled systems of record | ACCEPTED — AP-D-014 |
| Nightly bulk load as the integration pattern | MERGED → AP-D-016 |
| Ownership type / business-unit model decided after build | ACCEPTED — AP-D-029 (classified under Security: it is an authorization decision) |
| "Audit everything, forever" without scoping | MERGED → AP-D-063 |
| Backups treated as archive or legal hold | MERGED → AP-D-054 |
| Choice columns for externally-owned value lists | REJECTED — Areas 1–12 (`data-architecture.md` DAP-24) |
| Caching volatile or sensitive values | REJECTED — Areas 1–12 (`data-architecture.md` DAP-23) |
| Leading-wildcard filters; sorts on related columns | REJECTED — Areas 1–12 (`data-architecture.md` DAP-26) |
| `DateOnly` rules assuming local time zone | REJECTED — Areas 1–12 (`data-architecture.md` DAP-44) |
| Snapshot payloads in outbound sync messages | REJECTED — Areas 1–12 (`data-architecture.md` DAP-32) |

### 3.3 Automation

| Candidate | Verdict |
|---|---|
| Automation shape mismatch (process/message/volume built as workflow) | ACCEPTED — AP-D-015 |
| Power Automate used as a high-volume transaction engine | ACCEPTED — AP-D-016 |
| Non-idempotent retry behaviour | ACCEPTED — AP-D-017 |
| Business-critical workflow without failure/recovery model | ACCEPTED — AP-D-018 |
| Long synchronous flow chains | ACCEPTED — AP-D-019 |
| Synchronous integration across fragile systems | MERGED → AP-D-019 |
| Unattended RPA used where stable API integration is available | ACCEPTED — AP-D-020 |
| Automation without observability | ACCEPTED — AP-D-021 |
| Nested loops / action multiplication | REJECTED — Areas 1–12 (`automation-architecture.md` AT2-54) |
| Layered retry across a call chain | REJECTED — Areas 1–12 (`automation-architecture.md` AT2-55); the ownership *decision* it implies is in AP-D-021 |
| Trigger concurrency = 1 to obtain ordering | REJECTED — Areas 1–12 (`performance-scale.md` PF-AP-13); the decision form is DC-D-053 / AP-D-015 |
| Self-triggering flows | REJECTED — Areas 1–12 (`integration-architecture.md` X-06) |
| "It lacks error handling / observability" used as the argument for Azure | REJECTED — misclassified. It is an anti-pattern of *reasoning*, carried as `platform-suitability.md` AP-15 and `automation-architecture.md` AT2-66 (T3 framing, explicitly not encodable as Microsoft's position). Its corrective lives in AP-D-002. |

### 3.4 Integration

| Candidate | Verdict |
|---|---|
| Direct point-to-point connectors everywhere | ACCEPTED — AP-D-022 |
| Power Automate as enterprise integration backbone without boundaries | MERGED → AP-D-016 + AP-D-022 (the two mechanisms it is composed of) |
| API layer with no requirement behind it | ACCEPTED — AP-D-023 |
| Polling used where event-driven architecture is required | ACCEPTED — AP-D-024 (framed on the freshness *floor*, not on preference) |
| Custom connectors without API lifecycle ownership | ACCEPTED — AP-D-025 |
| Hybrid architecture without explicit external-service operator | ACCEPTED — AP-D-026; the composed form is AP-D-059 |
| Existing enterprise integration ownership bypassed | ACCEPTED — AP-D-027 |
| One integration decision per system pair rather than per stream | ACCEPTED — AP-D-028 |
| Heavy logic inside the gateway | REJECTED — Areas 1–12 (`integration-architecture.md` X-12) |
| Filtering in the flow rather than the trigger | REJECTED — Areas 1–12 (`integration-architecture.md` X-05) |
| Business events used as a data pipe | REJECTED — Areas 1–12 (`integration-architecture.md` X-17) |
| Duplicated transformation and business rules | MERGED → AP-D-022 (the estate-level consequence of point-to-point growth) |

### 3.5 Security

| Candidate | Verdict |
|---|---|
| Security model added late | ACCEPTED — AP-D-029 |
| Application UI treated as the authorization layer | ACCEPTED — AP-D-030 |
| Production secrets embedded in makers' assets | ACCEPTED — AP-D-031 |
| Privileged service identities without lifecycle ownership | ACCEPTED — AP-D-032 |
| Shared account / proxy to reduce licences (multiplexing) | MERGED → AP-D-032 (identity mechanism) + AP-D-061 (licence-avoidance motive) |
| Security requirements assumed solved by environment separation alone | ACCEPTED — AP-D-033 |
| Data policy treated as an exfiltration control | MERGED → AP-D-033 |
| Over-sharing applications/data | MERGED → AP-D-034 (external/broad surface) + AP-D-036 (maker enablement without ownership) |
| Internet/private-network requirements ignored during solution selection | ACCEPTED — AP-D-035 |
| Assurance claimed from a preview security score | MERGED → AP-D-057 |
| **Agent / conversational surface assumed covered by the app and flow access model** | **ACCEPTED — AP-D-068** (added 2026-09-03). Three MS-documented mechanisms: permanent ACP non-coverage of virtual connectors, the graph-connector guest-access bypass, and per-workload design-time enforcement. Same failure family as AP-D-030 and AP-D-033 |
| Agent artefact left without an owner or sharing configuration | MERGED → AP-D-036 (maker enablement without ownership) + AP-D-068 |
| Agent consumption committed to a budget before a pilot | MERGED → AP-D-062 (entitlement boundary discovered after design) + AP-D-051 (acting on an unmeasured figure); the criterion is `decision-criteria.md` DC-D-116 |
| Autonomous agent selected as an automation modality without a shape analysis | **REJECTED — evidence absent.** `automation-architecture.md` U-14 records that the corpus *"is silent on agent-based automation as an alternative or successor pattern"* and *"cannot answer 'should this be an agent instead of a flow?'"*, and that the deferral **has no owner**. An entry here would be invention. Recorded as a research commission, not as an anti-pattern |
| CMK enabled without separating key-vault and platform admin duties | REJECTED — Areas 1–12 (`security.md` SEC-A12) |
| Direct user→role assignment at scale | REJECTED — Areas 1–12 (`security.md` SEC-A5) |
| Record sharing as the access model | REJECTED — Areas 1–12 (`security.md` SEC-A6, `data-architecture.md` DAP-10) |

### 3.6 Governance

| Candidate | Verdict |
|---|---|
| Citizen development without ownership | ACCEPTED — AP-D-036 |
| Orphaned apps/flows | MERGED → AP-D-036 |
| Uncontrolled environment proliferation | ACCEPTED — AP-D-037 |
| DLP policy without an operating model | ACCEPTED — AP-D-038 |
| A policy per project (fragmentation) | MERGED → AP-D-038 |
| Enterprise governance imposed on trivial workloads | ACCEPTED — AP-D-039 |
| Excessive centralisation / excessive decentralisation | ACCEPTED as the pair AP-D-039 / AP-D-036 — the two failure directions of one lever |
| Production workloads in the default environment | ACCEPTED — AP-D-040 |
| Business-critical apps with no accountable owner | MERGED → AP-D-053 |
| Governance built on unmaintained tooling | MERGED → AP-D-058 |
| Building governance tooling that duplicates the product | MERGED → AP-D-058 |
| Treating a detection page as assurance | MERGED → AP-D-057 |

### 3.7 ALM

| Candidate | Verdict |
|---|---|
| Development directly in production | ACCEPTED — AP-D-041 |
| Unmanaged solutions in production without justified exception | MERGED → AP-D-041 |
| No source control for business-critical solutions | ACCEPTED — AP-D-042 |
| Manual deployment as permanent operating model | ACCEPTED — AP-D-043 |
| Environment-specific values hardcoded | ACCEPTED — AP-D-044 |
| Rollback assumed to exist | ACCEPTED — AP-D-045 |
| Hybrid solutions with only Power Platform components under CI/CD | ACCEPTED — AP-D-046 |
| Non-solution artefacts above the departmental class | ACCEPTED — AP-D-047 |
| Multiple publishers | REJECTED — Areas 1–12 (`alm-devops.md` ALM-A4) |
| Patches as the hotfix mechanism | REJECTED — Areas 1–12 (`alm-devops.md` ALM-A9) |
| Static analysis treated as a test gate | MERGED → AP-D-052 |
| Ignoring cross-solution dependency management | REJECTED — Areas 1–12 (`alm-devops.md` ALM-A10) |
| Shared development environment for a team | MERGED → AP-D-042 (the isolation requirement is what forces source control) |

### 3.8 Performance and scale

| Candidate | Verdict |
|---|---|
| Relying on documented limits as performance guarantees | ACCEPTED — AP-D-048 |
| Ignoring weakest-link limits across connectors/APIs | ACCEPTED — AP-D-049 |
| Non-delegable large-data patterns | ACCEPTED — AP-D-050 — accepted at decision altitude because the failure is *silently wrong answers*, which is a correctness decision, not a tuning one |
| Invented thresholds where none are published | ACCEPTED — AP-D-051 (with "acting on a `CONFLICTED` limit as if resolved" as its second mechanism) |
| High-volume workload approved without representative testing | ACCEPTED — AP-D-052 |
| Synchronous scale assumptions | MERGED → AP-D-019 |
| Reporting from the transactional store | MERGED → AP-D-009 |
| Business-critical workload in a non-production environment | MERGED → AP-D-040 |
| Depending on transition-period generosity | ACCEPTED — AP-D-055 (classified under Cost: the damage lands on the business case) |
| Deploying during business hours | REJECTED — misclassified. It is a release-window **requirement** (DC-D-077), carried as `performance-scale.md` PF-AP-15. |

### 3.9 Cost

| Candidate | Verdict |
|---|---|
| Licence price treated as full TCO | ACCEPTED — AP-D-060 |
| Hybrid architecture evaluated only on Power Platform cost | MERGED → AP-D-060 |
| Cheap initial build masking high support/operations cost | MERGED → AP-D-060 (the mechanism is the same omission) |
| Licence-driven architecture / licence-avoidance | ACCEPTED — AP-D-061 |
| Premium connector architecture without entitlement analysis | ACCEPTED — AP-D-062 |
| Uncontrolled flow/API consumption | ACCEPTED — AP-D-063 |
| Security/governance requirements ignored in cost model | ACCEPTED — AP-D-064 |
| Cheap start on a path to criticality (free-tier trap) | ACCEPTED — AP-D-065 |
| Cheap ownership of business-critical automation | ACCEPTED — AP-D-066 |
| Case built on transition-period or preview terms | ACCEPTED — AP-D-055 |
| Forecasting anonymous audiences as unique people | REJECTED — Areas 1–12 (`licensing-cost.md` LC-AP-11) — forecasting method |
| Enabling consumption billing without auditing prepaid capacity | REJECTED — Areas 1–12 (`licensing-cost.md` LC-AP-08) |
| Turning off search capability to reclaim storage | REJECTED — Areas 1–12 (`licensing-cost.md` LC-AP-14) |

### 3.10 Operations

| Candidate | Verdict |
|---|---|
| Business-critical application without monitoring | ACCEPTED — AP-D-053 |
| No incident ownership | MERGED → AP-D-053 (one accountability mechanism) |
| No recovery/reconciliation strategy | ACCEPTED — AP-D-054 |
| Platform SLA treated as composite application SLA | ACCEPTED — AP-D-056 |
| Expecting the vendor's support to do the incident work | MERGED → AP-D-056 (same misattribution of responsibility) |
| Preview features on a critical path | ACCEPTED — AP-D-057 |
| No retirement lifecycle | ACCEPTED — AP-D-067 |
| Hybrid system without cross-platform runbook | MERGED → AP-D-026 |
| Unmanaged deprecation exposure | ACCEPTED — AP-D-058 |
| Alerts to an individual mailbox | REJECTED — Areas 1–12 (`operations-support.md` OP-AP-20) |
| No documentation | REJECTED — Areas 1–12 (`operations-support.md` OP-AP-21); not decision-relevant at this altitude |

### 3.11 Cross-cutting, surfaced from the corpus rather than the brief

| Candidate | Verdict |
|---|---|
| Composed disqualifier ignored — every dimension merely CONDITIONAL, the combination unavailable | ACCEPTED — AP-D-059. Source: `architecture-patterns.md` §13. This is the highest-value Block D addition not present in the brief's candidate list. |
| Validation level not matched to the commitment | ACCEPTED — AP-D-052 |
| System of record undeclared / vocabulary borrowed from a vendor that does not define it | ACCEPTED — AP-D-014 |

### 3.11b User experience and interaction *(added 2026-09-03)*

**Repair note.** §3 previously carried **no user-experience section at all**, while `decision-criteria.md` §4.2 makes Users the second-densest exit domain in the register (4 `Xp`, 2 `Xr`, 1 `Xe`). Exits without detection signals fire only if the right question happened to be asked. `application-architecture.md` §11's **AP-17 … AP-35** were therefore re-tested **individually** against §2's four-element test, rather than rejected as a block. Every candidate below is that file's own entry, quoted by its id and its own summary.

| Candidate (`application-architecture.md`) | Verdict |
|---|---|
| **AP-17** God canvas app: many personas/experiences in one artefact | MERGED → AP-D-005 (starting above the simplest sufficient structure, in reverse — one structure carrying more than it should). The named consequences are build-time (formula sprawl, Studio degradation); the *decision* is persona partitioning, carried by DC-D-011 and DC-D-078, and the multi-maker half is now a composed disqualifier (AP-D-059, ALM row) |
| **AP-18** Everything in `OnStart`; `Navigate` in `OnStart` | REJECTED — Areas 1–12 (implementation; deprecated architecture and a retired function) |
| **AP-19** Collect-everything workarounds for delegation | MERGED → AP-D-050 (the delegation failure family; AA-07, PS-13 are already in its evidence) |
| **AP-20** Copy-paste component reuse / app-to-app import | REJECTED — Areas 1–12 (build practice; retired mechanism) |
| **AP-21** Editing library components in consuming apps | REJECTED — Areas 1–12 (unmanaged-layer mechanics; the decision-altitude form is AP-D-042/AP-D-043) |
| **AP-22** PCF-for-everything before platform controls | MERGED → AP-D-005 (inverts the vendor's own minimal-complexity ordering) |
| **AP-23** Unreviewed third-party code component (*"can potentially access security tokens and data"*) | REJECTED — Areas 1–12. Real and MS-sourced, but detecting it changes a **governance control**, not the platform decision. A pack's governance controls should carry it; §2's fourth element is not met |
| **AP-24** Record-centric app for mobile-first field capture via custom pages | MERGED → AP-D-003. The decision sits in DC-D-015 (`Xc`) and DC-D-016 (`Xp`) — device controls unsupported in custom pages, offline gaps (AA-16, AA-43) |
| **AP-25** Bespoke branding pursued inside record-centric core pages | MERGED → AP-D-003. The decision is DC-D-013's `Xr` exit — theming is colours, font and logo only (AA-14) |
| **AP-26** External-site anonymous/generic-authenticated roles with broad table permissions and interface wildcards; open registration left on | **CONFIRMED HOME — AP-D-034.** The documented mass-exposure incident class; already the file's strongest external-surface entry |
| **AP-27** External site fed by background automation presented as real-time | **CONFIRMED HOME — AP-D-024.** The decision is DC-D-018's `Xr` exit (AA-27) |
| **AP-28** Wrapping for consumer/B2C or push-dependent applications | MERGED → AP-D-003. The decision is DC-D-020's `Xp` exit — B2C unsupported, push unsupported (AA-39, AA-40) |
| **AP-29** Role-based UI via visibility formulas treated as security | **CONFIRMED HOME — AP-D-030** (the application UI treated as the authorization layer). Note this is the same failure family as the newly added AP-D-068 |
| **AP-30** Stretching the guided-stage construct into a conditional wizard engine | REJECTED — Areas 1–12. The boundary is already carried as a **criterion**: DC-D-055's `Decision impact` names it, with the stage/table caps and *"executes no logic of its own"* (AA-19) |
| **AP-31** Record-centric app served to phone users via a browser | MERGED → AP-D-003. The decision is DC-D-015 — unsupported; the native client is required (AA-45) |
| **AP-32** Growing a team-hosted app toward its caps without budgeting the one-way upgrade | **CONFIRMED HOME — AP-D-065** (the free-tier trap). Converts all users to premium; no downgrade (AA-50) |
| **AP-33** Single-page-application site chosen for a multi-language or offline-read requirement | MERGED → AP-D-003. The decisions are DC-D-017 and DC-D-016 — those sites are single-language with no offline setting (AA-23) |
| **AP-34** Document-store customized form treated as a portable, solution-managed app | MERGED → AP-D-047 (non-solution artefacts: no manual sharing, no automated cross-environment copy — AA-51) |
| **AP-35** Building a bespoke multisession app where a first-party application matches the requirement | **CONFIRMED HOME — AP-D-007** (rebuilding what an existing capability already provides; AA-20, AA-36 rung 0 → ALT-011) |

**Result: 19 candidates · 0 new entries · 9 merged · 5 confirmed to an existing home · 5 rejected as Areas 1–12 altitude.**

**The thin UX anti-pattern coverage is therefore correct, and is now audited rather than assumed.** The domain's decision weight genuinely sits in the **criteria** — DC-D-012, DC-D-013, DC-D-015, DC-D-016, DC-D-018, DC-D-020 carry seven of the register's exits between them — and in **AP-D-003**, which is the detection home for five of the nineteen. What the audit adds is the mapping: for every UX failure `application-architecture.md` documents, this ledger now names *where in Block D it is detected*, which is what a question bank needs and what its absence previously made impossible to check.

### 3.12 Ledger totals

| | Count |
|---|---|
| Candidate topics evaluated | **124** (101 original + 4 agent candidates, §3.5 + 19 user-experience candidates, §3.11b) |
| Accepted (distinct entries in §4/§5) | **68** (67 + AP-D-068) |
| Merged into, or confirmed to, an existing entry | **37** (21 original + 2 agent + 14 user-experience) |
| Rejected — belongs to Areas 1–12 (implementation altitude) | **25** (20 original + 5 user-experience) |
| Rejected — misclassified (constraint / requirement / reasoning defect) | **3** |
| Rejected — evidence absent (an entry would be invention) | **1** (autonomous agents as an automation modality, §3.5) |

**Footnote — the table does not balance on its own, and this is why.** 68 + 37 + 25 + 3 + 1 = **134** verdict rows against **124** candidate topics. The difference is exactly **10**, and it has one cause: **ten accepted topics split into two entries each** during drafting, because their failure mechanisms proved distinct. Each split is visible in §3, and §4's register is authoritative for ids. *(Recorded as a footnote 2026-09-03: the previous version stated this reconciliation immediately below the table without flagging that the table alone does not balance, so a reader auditing the trail stopped at the arithmetic.)*

---

## 4. Register

Authoritative id → name map. Categories are for navigation only; several anti-patterns are cross-cutting and each entry's `Consequences` field says where the damage actually lands.

| Id | Anti-pattern | Category | Confidence |
|---|---|---|---|
| AP-D-001 | Solution named before the problem is characterised | Selection | HIGH |
| AP-D-002 | Selection by precedent — familiarity or architectural resemblance | Selection | MEDIUM |
| AP-D-003 | Low-code selected where a hard non-functional requirement dominates | Selection | HIGH |
| AP-D-004 | One platform for every workload class | Selection | MEDIUM |
| AP-D-005 | Starting above the simplest sufficient structure | Architecture | HIGH |
| AP-D-006 | Structure never de-escalated | Architecture | MEDIUM |
| AP-D-007 | Rebuilding what an existing capability already provides | Selection | HIGH |
| AP-D-008 | Document or spreadsheet store as the relational system of record | Data | HIGH |
| AP-D-009 | The operational store serving the analytical workload | Data | HIGH |
| AP-D-010 | Shadow system of record | Data | HIGH |
| AP-D-011 | Bidirectional synchronisation without field ownership and reconciliation | Data | HIGH |
| AP-D-012 | Data virtualization chosen without its exclusion list | Data | HIGH |
| AP-D-013 | Replica trusted without drift detection | Data | HIGH |
| AP-D-014 | System of record undeclared | Data | MEDIUM |
| AP-D-015 | Automation shape mismatch | Automation | MEDIUM |
| AP-D-016 | Workflow engine as a high-volume transaction engine | Automation | HIGH |
| AP-D-017 | Retry enabled on non-idempotent writes | Automation | HIGH |
| AP-D-018 | Transaction semantics hand-built in orchestration logic | Automation | HIGH |
| AP-D-019 | Synchronous chain across heterogeneous availability | Automation | MEDIUM |
| AP-D-020 | UI automation where a stable interface exists or can be built | Automation | MEDIUM |
| AP-D-021 | Automation with no observability and no throttling owner | Automation | HIGH |
| AP-D-022 | Point-to-point proliferation | Integration | HIGH |
| AP-D-023 | Mediation layer with no requirement behind it | Integration | HIGH |
| AP-D-024 | Polling below the mechanism's own freshness floor | Integration | HIGH |
| AP-D-025 | Integration seam without contract lifecycle ownership | Integration | HIGH |
| AP-D-026 | External component adopted without an operator | Integration | MEDIUM |
| AP-D-027 | Existing integration ownership bypassed | Integration | MEDIUM |
| AP-D-028 | One integration decision per system pair instead of per stream | Integration | MEDIUM |
| AP-D-029 | Authorization model deferred past an irreversible decision | Security | HIGH |
| AP-D-030 | Application UI treated as the authorization layer | Security | HIGH |
| AP-D-031 | Secrets held in makers' assets | Security | HIGH |
| AP-D-032 | Shared identity as the access or integration model | Security | HIGH |
| AP-D-033 | One control treated as the whole control | Security | HIGH |
| AP-D-034 | External or anonymous surface exposed with unreviewed permissions | Security | HIGH |
| AP-D-035 | Network and deployment constraints discovered after platform selection | Security | HIGH |
| AP-D-036 | Maker enablement without ownership or a promotion path | Governance | HIGH |
| AP-D-037 | Uncontrolled environment proliferation | Governance | HIGH |
| AP-D-038 | Policy without an operating model | Governance | HIGH |
| AP-D-039 | Enterprise controls imposed on a trivial workload | Governance | MEDIUM |
| AP-D-040 | Production workload in a non-production environment class | Governance | HIGH |
| AP-D-041 | Development in production | ALM | HIGH |
| AP-D-042 | Business-critical solution without source control | ALM | MEDIUM |
| AP-D-043 | Manual deployment as the permanent operating model | ALM | HIGH |
| AP-D-044 | Environment-specific values shipped inside the release artefact | ALM | HIGH |
| AP-D-045 | Rollback assumed to exist | ALM | HIGH |
| AP-D-046 | Single-sided supply chain for a two-sided architecture | ALM | MEDIUM |
| AP-D-047 | Unmanaged artefact structure above the departmental class | ALM | HIGH |
| AP-D-048 | Documented limits read as performance guarantees | Performance | HIGH |
| AP-D-049 | Sizing against a single meter | Performance | HIGH |
| AP-D-050 | Non-delegable access path over a growing dataset | Performance | HIGH |
| AP-D-051 | Inventing the number the platform does not publish | Performance | HIGH |
| AP-D-052 | Validation level not matched to the commitment being made | Performance | MEDIUM |
| AP-D-053 | Business-critical application with no monitoring and no incident owner | Operations | HIGH |
| AP-D-054 | Recovery assumed rather than designed and drilled | Operations | HIGH |
| AP-D-055 | Case built on transition-period or preview terms | Cost | HIGH |
| AP-D-056 | Platform commitment quoted as the solution's commitment | Operations | HIGH |
| AP-D-057 | Preview or unsupported components on a critical path | Operations | HIGH |
| AP-D-058 | Unmanaged platform-change exposure | Operations | HIGH |
| AP-D-059 | Composed disqualifier ignored | Cross-cutting | MEDIUM |
| AP-D-060 | Licence line treated as the total cost of ownership | Cost | HIGH |
| AP-D-061 | Licence-avoidance architecture | Cost | MEDIUM |
| AP-D-062 | Entitlement boundary discovered after the design is fixed | Cost | HIGH |
| AP-D-063 | Consumption without an owner or a growth model | Cost | HIGH |
| AP-D-064 | Operational and security prerequisites omitted from the cost model | Cost | HIGH |
| AP-D-065 | Cheap start on a path to criticality | Cost | HIGH |
| AP-D-066 | Cheap ownership of business-critical automation | Cost | HIGH |
| AP-D-067 | No retirement lifecycle | Operations | MEDIUM |
| AP-D-068 | Agent surface treated as covered by the app and flow access model | Security | MEDIUM-HIGH |

**Count: 67.**

---

## 5. Anti-patterns

Field order per entry: Description · Classification · Trigger conditions · Why it fails · Consequences · Detection signals · Decision impact · Better alternatives · Exceptions · Evidence · Confidence.

`Origin` follows the corpus convention: **MS** = Microsoft statement; **MS-V** = Microsoft vendor-side positioning (capability facts only); **INF** = supported synthesis over documented facts; **T3/T4** = independent/community, corroborative only.

`Classification` carries the **enforcement strength** and takes one of three values — `ANTI-PATTERN` (contextual, evaluate against `Exceptions`), `GATE` (the option is *unavailable*), `CONSTRAINT` (always wrong within its stated scope). See §2.

**Ordering note.** The subsections group entries by category for reading, and **two entries sit outside strict numeric order within their subsection**: AP-D-055 appears in §5.11 after AP-D-066, and AP-D-067 appears in §5.9 before AP-D-059. Both are filed under the category their `Consequences` field lands in rather than under their number. **§4's register is authoritative for ids and is complete** — a sequential read of §5 is not a completeness check, and nothing is missing.

---

### 5.1 Selection and architecture

#### AP-D-001 — Solution named before the problem is characterised

**Description.** A technology, product family or architecture is fixed before the requirement's volume, latency, identity, atomicity, availability, residency and ownership characteristics are established. All subsequent analysis is a search for justification.

**Classification:** ANTI-PATTERN · **Origin:** INF over MS-stated method

**Trigger conditions.**
- The engagement's framing already contains a product name ("we're building this in Power Apps").
- The option set contains only variants of one technology.
- No stated requirement would change the answer — i.e. there is no criterion whose value could reject the chosen platform.
- Discovery artefacts describe screens and connectors before they describe volume, ownership and failure semantics.

**Why it fails.** Every fit verdict in the canonical corpus is *conditional on a measurable requirement*. `platform-suitability.md` §2's 36 rows and §3's boundary list all take the form *requirement × condition → constraint*, and several of those conditions are **irreversible once built**: Dataverse table ownership type is fixed at creation (`data-architecture.md` DA-12, `security.md` SEC-09), the virtual-versus-standard table decision is irreversible (`data-architecture.md` VT-* / `architecture-patterns.md` Q-13), the Dataverse-for-Teams upgrade is one-way (`application-architecture.md` AA-50), Dynamics 365 apps cannot be installed or uninstalled after environment creation (`alm-devops.md` ALM-24), and turning on trigger concurrency "can't be undone" (`performance-scale.md` PF-36). Naming the solution first means these decisions are made by default rather than by analysis. Microsoft's own instruction runs the other way: *"Choose the simplest approach that fulfills requirements"* (`integration-architecture.md` I-01) and *"Don't replicate your legacy solution"* (`platform-suitability.md` PS-41).

**Consequences.**
- *Business:* the option set presented to the sponsor is not a real choice; the "do nothing / process change / existing capability" options that `licensing-cost.md` LC-28 says are frequently the honest answer are never priced.
- *Architecture:* irreversible modelling decisions taken as defaults.
- *Cost:* the premium/entitlement boundary is discovered after design (→ AP-D-062).
- *Governance:* no recorded justification, so the decision cannot be revisited when a tripwire fires.

**Detection signals.** Product names in the problem statement · single-family option set · no criterion in the analysis that could produce rejection · screen inventory produced before volume estimate · sponsor's stated constraint is a platform, not an outcome.

**Decision impact.** Do not produce an architecture. Return to requirement characterisation, and specifically to the criteria the corpus marks **decision-blocking when unknown** (`decision-criteria.md` §5): throughput at horizon, regulatory regime, system-of-record ownership, availability objective, external identity model, budget envelope, deployment-model constraint. Until at least those are stated, the correct output is `DECISION BLOCKED — MORE EVIDENCE REQUIRED`, not a platform.

**Better alternatives.** Requirement-first classification: the ordered tests already in the corpus — `integration-architecture.md` §2.2 (integration topology), `automation-architecture.md` §2 (automation shape), `performance-scale.md` §1 (workload shape), `data-architecture.md` §2 (store fit). Each terminates in a class, not a product.

**Exceptions.** A genuine constraint-driven mandate exists — an enterprise standard, a signed agreement, or a sunk platform investment — and is recorded **as a constraint with an owner**, not disguised as an analytical conclusion. The corpus supports this: `platform-suitability.md` PS-40 makes team skills an explicit architecture criterion, and `licensing-cost.md` §6 makes existing sunk capability a cost dimension. The anti-pattern is the concealment, not the constraint.

**Evidence.** `integration-architecture.md` I-01, §2.2, §12.9 ("scale anxiety without a number", "resemblance to a reference architecture"); `platform-suitability.md` PS-41, §2, §3; `licensing-cost.md` LC-28; `data-architecture.md` DA-12; `application-architecture.md` AA-50; `alm-devops.md` ALM-24; `architecture-patterns.md` Y-01.

**Confidence:** HIGH (the irreversibility facts are MS; the framing is INF).

---

#### AP-D-002 — Selection by precedent — familiarity or architectural resemblance

**Description.** The architecture is chosen because the team knows it, or because it looks like a published reference architecture, rather than because a requirement forces it. Two variants with one mechanism: *familiarity* ("we always use X") and *resemblance* ("the reference architecture has an API gateway, so we need one").

**Classification:** ANTI-PATTERN · **Origin:** MS (both correctives) + INF (the shared framing)

**Trigger conditions.**
- The justification for a component is a precedent, a diagram or a habit, and no criterion is cited.
- A reference architecture is presented as the design rather than as an input.
- The reverse case: an option is excluded because the team has not used it, without stating that as a capability constraint.

**Why it fails.** Reference architectures are scoped to their own examples and say so — *"This article provides an example"* (`architecture-patterns.md` Y-01, MS). Copying the structure imports its components without its conditions. `architecture-patterns.md` Y-01 and Y-12 name both halves: pattern-by-resemblance, and standing up a second integration boundary beside an existing enterprise one. Familiarity fails in the mirror direction: `platform-suitability.md` PS-40 makes skills a *criterion to feed in* — *"The best service for your workload might be a technology that your team isn't skilled at"* — not a filter to apply silently. And the corpus documents one specific familiarity-driven mis-selection with evidence: choosing a relational engine for high-ingest telemetry *"because it's SQL and we know SQL"*, where Microsoft's own data-store guide routes that workload elsewhere (`data-architecture.md` DAP-36, SQ2-06).

**Consequences.**
- *Architecture:* components with no requirement behind them (→ AP-D-023) or missing components whose requirement was invisible.
- *Cost:* a second operated estate funded without a driver (`architecture-patterns.md` Y-12).
- *Delivery:* effort spent conforming to a shape rather than to a need.
- *Operations:* an unfamiliar component adopted for resemblance has no operator (→ AP-D-026).

**Detection signals.** Justification of the form "this is how it's normally done" · a reference-architecture diagram used as the design · an option rejected on skills without that being recorded as a constraint · a component whose removal no stated requirement would notice.

**Decision impact.** Require, per component, the named requirement that forces it (`architecture-patterns.md` §3.1's variable table is the checklist) — and, separately, record team capability as an explicit criterion (DC-D-110) that can legitimately move a recommendation, once it is visible. A hybrid that needs pro-code with no pro-dev capacity is `platform-suitability.md` PS-40's documented RISK and `architecture-patterns.md` §13's `POOR FIT` composed disqualifier, not a training problem to be waved through.

**Better alternatives.** Requirement→pattern mapping (`architecture-patterns.md` §3.1, §6.2 escalation triggers); explicit skills criterion with either a training commitment or an option change; the ordered classification tests of `integration-architecture.md` §2.2 and `automation-architecture.md` §2.

**Exceptions.** A deliberate standardisation decision — accepting a slightly worse local fit to keep one operating model — is legitimate *when priced*. `licensing-cost.md` §6 makes "existing sunk capability" a cost dimension and notes the economically correct answer may be "use the incumbent".

**Evidence.** `architecture-patterns.md` Y-01, Y-12, §3.1; `platform-suitability.md` PS-40, AP-15; `data-architecture.md` DAP-36, SQ2-06; `integration-architecture.md` §12.9; `automation-architecture.md` AT2-66 (T3 framing — not to be presented as Microsoft's position).

**Confidence:** MEDIUM (correctives are MS; the unified framing is INF).

---

#### AP-D-003 — Low-code selected where a hard non-functional requirement dominates

**Description.** The functional requirement is an ordinary business application, so a low-code platform is selected — while a single non-functional requirement in the set is one the platform documents itself as unable to meet.

**Classification:** ANTI-PATTERN · **Origin:** MS (each boundary) + INF (the framing)

**Trigger conditions.** Any one of the following is a stated requirement and is not negotiable:

| Dominant requirement | The documented boundary |
|---|---|
| Real computation in one step (optimisation, simulation, media processing) | No compute-sizing dial exists anywhere in the platform; plug-in execution time is charged to the triggering request's service-protection budget (`performance-scale.md` PF-45, PF-22, B-14) |
| Strict sub-second, transactionally-visible end-to-end latency across app + automation + external system | No end-to-end latency figure is published for any path (`performance-scale.md` PF-14, B-16, PF-U-01) |
| Atomicity across two or more systems | Atomicity stops at the Dataverse boundary; no cross-system coordinator exists (`integration-architecture.md` IA-19, §12.3; `platform-suitability.md` PS-45) |
| Contractual cross-region RTO | Microsoft publishes no cross-region RTO commitment (`performance-scale.md` PF-40, PF-U-*; `platform-suitability.md` PS-37) |
| On-premises, air-gapped or customer-hosted deployment | Unsupported — SaaS only (`platform-suitability.md` PS-47; re-verified 2026-09-03, §6 source V-D-01) |
| Offline in a browser, or offline over non-Dataverse data | Unsupported (`application-architecture.md` AA-42…AA-44; `platform-suitability.md` PS-35) |
| Branded native mobile app with push notifications | Unsatisfiable in-platform (`application-architecture.md` AA-40, AA-46) |
| Public third-party API surface | Not the platform's purpose (`platform-suitability.md` PS-36, PS-51) |
| Frozen behaviour / no vendor-driven change | Mandatory semi-annual release waves and rolling deprecations (`platform-suitability.md` PS-50) |

**Why it fails.** These are not performance targets to be tuned toward; they are documented absences. A functional-requirements-led selection weights the 90% of the requirement the platform serves well and discounts the 10% it cannot serve at all — and the 10% is the part that decides whether the system works. The corpus states the ordering explicitly for the clearest case: compute intensity is *"an out-of-platform verdict before other sizing"* (`performance-scale.md` §1 classification test, step 1).

**Consequences.**
- *Business:* the requirement is quietly dropped, renegotiated late, or met by a workaround the business never agreed to.
- *Architecture:* the workaround becomes the architecture — compute pushed into flow expressions (`automation-architecture.md` AT2-62), atomicity simulated in flow logic (→ AP-D-018), offline replaced by "connectivity is usually fine".
- *Cost:* rework at the point of discovery; the out-of-platform component is funded late and unbudgeted.
- *Operations:* a commitment has been made that no drill can substantiate (→ AP-D-056).

**Detection signals.** A stated requirement matching any trigger row · "just needs to do the maths" · a hard latency number with no measurement plan · a compliance clause naming an RTO · a deployment or residency mandate · offline requirement on a browser surface · push notifications on a branded app.

**Decision impact.** Run the dominant non-functional requirement **before** the functional fit assessment. The outcome classes it can produce are drawn from the **closed set** in `decision-criteria.md` §6.2: class 3 or 4 **`POWER PLATFORM + … HYBRID`** where the requirement is confined to one step; class 5 **`POWER PLATFORM — POOR FIT`** or class 6 **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`** where it is not, each followed by class 8 **`CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`**; or class 9 **`DEPLOYMENT MODEL EXCLUDES THIS PLATFORM`** specifically where the blocker is the deployment model, which is the one axis on which comparators document a materially different capability (`alternatives.md` ALT-008).

**Better alternatives.** Decompose so the hard requirement leaves the platform (`architecture-patterns.md` AP-05 hybrid, AP-09 background, AP-10 boundary); relocate the whole workload (`alternatives.md` ALT-005, ALT-006, ALT-007, ALT-008); or renegotiate the requirement explicitly and record it as an accepted risk with a named owner.

**Exceptions.** The requirement is confined to a single step and the organisation can operate a hybrid — then this is AP-05, not an anti-pattern. `integration-architecture.md` §12.9 is explicit that *"one difficult step"* is not a reason to relocate everything. The exception fails if there is no operator for the external half (→ AP-D-026, AP-D-059).

**Evidence.** `performance-scale.md` §1, §4.3 (B-14…B-17), PF-45, PF-40, PF-14; `platform-suitability.md` PS-08, PS-09, PS-35, PS-36, PS-37, PS-45, PS-47, PS-50; `application-architecture.md` AA-40, AA-42…AA-44, AA-46; `integration-architecture.md` IA-19, §12.3; `automation-architecture.md` AT2-62, §4.3.

**Confidence:** HIGH.

---

#### AP-D-004 — One platform for every workload class *(portfolio altitude)*

**Description.** After a successful first delivery, the platform becomes the default answer for every subsequent need — interactive apps, high-volume integration, analytics, streaming, compute, B2B — because it is present, licensed and understood.

**Classification:** ANTI-PATTERN — **portfolio altitude, explicitly outside the engagement-altitude set** (re-scoped 2026-09-03) · **Origin:** INF over MS-stated workload boundaries

**Altitude note (repair, 2026-09-03).** This entry's failure mechanism decomposes without residue into AP-D-015 (shape mismatch), AP-D-009 (analytics on the operational store), AP-D-039 / AP-D-036 (simultaneous over- and under-governance) and AP-D-063 (shared-capacity contention). What is left that is genuinely its own is **portfolio-level**: its trigger conditions describe *an estate*, not a solution, and no Discovery process confined to one engagement can produce them. Left classified as an ordinary engagement-altitude anti-pattern it would either never fire or fire on judgement rather than evidence.

It is therefore **retained and re-scoped** rather than merged away: the estate-level finding is real and MS-evidenced (shared tenant capacity, estate-wide restore blocking, no project-level request view), and deleting it would lose the only place the corpus records that a platform *standard* needs a workload-class exclusion list. But it is now marked as belonging to a **portfolio or platform-standard review**, not to a solution decision, and a pack must not surface it as an engagement finding. Within an engagement, its constituent mechanisms fire through AP-D-015, AP-D-009, AP-D-039, AP-D-036 and AP-D-063, all of which are engagement-altitude and evidenced.

**Trigger conditions.**
- An estate in which workloads of visibly different shapes all run on the same platform.
- A standard of the form "all new applications are built on X" with no workload-class exclusions.
- Analytics, streaming, ETL or B2B/EDI requirements arriving into the platform backlog.

**Why it fails.** The corpus's shape taxonomies exist precisely because different shapes bind on different meters. `performance-scale.md` §1 identifies six workload shapes and states that *"Most Power Platform performance failures in this corpus are not the platform being slow. They are a shape-2/3/6 requirement implemented as shape 1."* `automation-architecture.md` §2 says the same for automation: *"Most failed Power Automate architectures are a shape-2/3/4 requirement implemented as shape 1."* Microsoft assigns several classes elsewhere outright: large-scale transformation and complex business logic *"do not belong in cloud flows"* (`platform-suitability.md` PS-07); *"use a dedicated datastore for reporting purposes instead"* (`data-architecture.md` DA-51); high-ingest timestamped metrics and events route to a different store family (`data-architecture.md` SQ2-06); B2B/EDI belongs to an integration platform (`integration-architecture.md` §12.2). Universalisation also concentrates blast radius: the tenant capacity pool is shared, storage overage *blocks restore, copy, recover and environment creation* estate-wide (`operations-support.md` OP-22), and the non-licensed request pool is shared tenant-wide with *no project-level view* (`licensing-cost.md` L-11, `operations-support.md` OP-U-05).

**Consequences.**
- *Performance:* workloads compete on meters they do not know they share.
- *Cost:* one project's growth consumes another's headroom; capacity overage becomes a recoverability incident (`operations-support.md` OP-22).
- *Operations:* a single platform team owns incompatible operational profiles.
- *Governance:* over-governance of trivial workloads and under-governance of critical ones simultaneously (→ AP-D-039, AP-D-036).

**Detection signals.** Analytical, streaming, ETL or B2B requirements in the platform backlog · tenant capacity headroom below the documented notification thresholds · no workload-class exclusion list in the platform standard · one environment or one tenant pool serving several criticality classes.

**Decision impact.** Classify every incoming requirement by shape *before* assigning it to the platform, and maintain an explicit exclusion list. The corpus supplies the exclusions: analytics off the operational store, bulk movement to a data pipeline, streams to a streaming service, B2B/EDI to an integration platform, compute out of platform.

**Better alternatives.** Portfolio-level workload routing; `architecture-patterns.md` AP-10 as the enclosing boundary; `alternatives.md` ALT-006 (cloud-native services), ALT-007 (existing enterprise platform), ALT-009 (hybrid) for the classes that leave.

**Exceptions.** Deliberate consolidation on a single platform for a defined workload class, with the excluded classes named. Also: a small organisation for which the operating-model cost of a second platform genuinely exceeds the mis-fit cost — `automation-architecture.md` §4.1 makes exactly this argument for keeping work in Power Automate when there is *"no Azure operating model"*.

**Evidence.** `performance-scale.md` §1; `automation-architecture.md` §2, §4.1; `platform-suitability.md` PS-07, PS-41; `data-architecture.md` DA-51, SQ2-06; `integration-architecture.md` §12.2, §12.8; `operations-support.md` OP-22, OP-U-05; `licensing-cost.md` LC-05, L-11.

**Confidence:** MEDIUM (each boundary is MS; the estate-level framing is INF).

---

#### AP-D-005 — Starting above the simplest sufficient structure

**Description.** The design begins at an API layer, a broker, a replicated store or a hybrid split because that is what enterprise architecture is expected to look like — not because a named requirement forces the rung.

**Classification:** ANTI-PATTERN · **Origin:** MS (the instruction and the "not suitable when" statements) + INF (the ladder framing)

**Trigger conditions.**
- A mediation, broker or replication component exists in the design and no §3.1-style variable is cited for it.
- One consumer, one backend, a stable contract and projected volume inside the connector throttle — yet the design has three tiers.
- Volume is described as "high" with no number (`integration-architecture.md` §12.9: *"scale anxiety without a number"*).
- The design was produced before the volume, frequency and consumer-count figures existed.

**Why it fails.** Each rung on `architecture-patterns.md` §3.2's ladder buys a property at a stated price: an API layer costs *"a hop, a bill, a team"*; a queue costs *"latency, idempotency work, backlog ops"*; a hybrid costs *"a second operating model"*. Paid without a requirement, the price is pure loss — and it is not only monetary. Microsoft bounds its own patterns: queue-based load levelling is unsuitable when *"The workload volume is predictably low and stable, so adding queueing complexity provides little benefit"*; gateway aggregation is unsuitable for a single service, where *"adding a batch operation to the service might be more suitable"*; an anti-corruption layer is unsuitable when *"The new and legacy systems have no significant semantic differences"*; background jobs *"introduce more components and dependencies… which can increase the complexity and maintenance costs"* (`architecture-patterns.md` §8, items 1–8). A gateway with nothing to do is *"a single point of failure (SPoF)"* and *"a bottleneck"* with no compensating benefit (`integration-architecture.md` X-11, §4.2). And the operating-model cost is real: two ALM models, two RBAC models, two monitoring surfaces, two retention windows (`automation-architecture.md` N-52).

**Consequences.**
- *Architecture:* availability *reduced* — a SaaS profile converted into an operated one (`architecture-patterns.md` §3.1, Availability row).
- *Cost:* a second estate, a second pipeline and a second support rota funded with no driver (→ AP-D-060).
- *Operations:* more components to monitor, and a cross-boundary correlation problem *"the requirement never had"* (`automation-architecture.md` §4.1, §6.4).
- *Delivery:* lead time spent on structure rather than outcome.

**Detection signals.** Mediation/broker/replication present with no cited variable · "high volume" without a figure · consumer count of one · design predates the volume estimate · the same transformation implemented once, in one place, behind a layer built for reuse.

**Decision impact.** Start at the simplest structure and climb only on a named requirement, recording which one (`architecture-patterns.md` §3.2: *"Climb only when a named requirement from §3.1 forces it, and record which one"*). Where the number that would justify the rung is unknown, that is a decision-blocking unknown to close (DC-D-040, DC-D-037, DC-D-047), not a reason to buy the rung defensively.

**Better alternatives.** The escalation ladder used in order; direct integration where its seven conditions hold (`integration-architecture.md` §4.1); connector-level trigger conditions and OData filters as the documented first remedy for a busy source (`automation-architecture.md` AT2-60); bulk APIs and dataflows as the documented remedy for volume, with the automation orchestrating rather than iterating (`automation-architecture.md` §4.1, `performance-scale.md` B-04).

**Exceptions.** An existing enterprise boundary already provides the rung — then consuming it is not over-engineering but reuse (`architecture-patterns.md` matrix row 29, AP-10). Also: a credible, dated growth forecast that crosses the boundary inside the investment horizon justifies building for it now, provided the forecast is recorded as the justification.

**Evidence.** `architecture-patterns.md` §3.2, §8 items 1–12, Y-02, Y-04, matrix rows 1, 6, 29; `integration-architecture.md` I-01, X-11, §4.2 ("When API-MEDIATED is unnecessary complexity"), §12.9; `automation-architecture.md` §4.1, AT2-53, AT2-60, N-51…N-53; `performance-scale.md` B-04.

**Confidence:** HIGH (Microsoft's own "not suitable when" statements carry this directly).

---

#### AP-D-006 — Structure never de-escalated

**Description.** A component was added for a requirement that has since disappeared — the migration finished, the volume never arrived, the second consumer was retired — and the structure remains, carrying its full operating cost.

**Classification:** ANTI-PATTERN · **Origin:** MS (both documented cases) + INF (the general framing)

**Trigger conditions.**
- An anti-corruption or facade layer whose legacy counterpart has been decommissioned.
- A broker whose measured throughput is far below the level that justified it.
- A replicated store whose platform-feature justification (audit, row security, offline) was dropped from scope.
- A hybrid component whose external step was later solved in-platform.

**Why it fails.** The corpus records this as *"the move nobody makes"* and gives two Microsoft-documented cases: *"If the anti-corruption layer is part of an application migration strategy, consider whether it's permanent or whether you plan to retire it after you migrate all legacy functionality"*, and a queue *"might not be suitable when… The workload volume is predictably low and stable"* — *"a condition that can become true after the fact"* (`architecture-patterns.md` §6.3). Microsoft's minimal-complexity instruction *"is not only an initial-design rule"* (same section). Meanwhile every surviving component keeps its costs: a second supply chain (`alm-devops.md` §14.2), a named operator and on-call (`architecture-patterns.md` Y-13), governance ownership in a second domain (`governance.md` GOV-XB-01), and its own consumption meters (`licensing-cost.md` §6).

**Consequences.**
- *Cost:* recurring spend on a component with no current requirement; `licensing-cost.md` LC-29 records refactoring and deprecation remediation as real, recurring lines that attach to *every* component.
- *Operations:* a component nobody has a reason to understand becomes the one that fails.
- *Architecture:* the structure ossifies; each later change must respect a constraint that no longer serves anything.
- *Governance:* a resource with no current owner (→ AP-D-067).

**Detection signals.** A component whose justification references a completed migration · measured volume an order of magnitude below the escalation trigger · a replicated dataset whose platform features are unused · an external component with no incidents and no consumers · a periodic architecture review that has never removed anything.

**Decision impact. Treat "the structure is more complex than the current requirement justifies" as a finding, not a stable state** (`architecture-patterns.md` §6.3). At revalidation, run the escalation triggers in reverse: for each rung, ask whether its forcing requirement still holds; where it does not, put de-escalation into the option set with its migration cost priced. Note that de-escalation is itself a change with its own risk — the finding is that it should be *considered*, not that it should be automatic.

**Better alternatives.** Scheduled architecture revalidation against §6.2's escalation triggers; recording each rung's forcing requirement at the time it is added, so its expiry is detectable; a tripwire on the volume assumption.

**Exceptions.** The component also satisfies a second requirement that still holds. Or the migration cost exceeds the residual operating cost over the remaining lifespan — a legitimate priced decision, provided it is made rather than defaulted.

**Evidence.** `architecture-patterns.md` §6.3, §6.2, Y-13; `integration-architecture.md` I-01; `licensing-cost.md` LC-29, §6; `alm-devops.md` §14.2; `governance.md` GOV-XB-01; `operations-support.md` OP-28.

**Confidence:** MEDIUM (two MS cases; the general rule is INF).

---

#### AP-D-007 — Rebuilding what an existing capability already provides

**Description.** A new application is built for a need already met — wholly or largely — by a first-party product, an existing licensed platform feature, a purchasable product, or the incumbent system's own configuration. Its strongest form is rebuilding the legacy system feature-for-feature on a new platform.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.**
- The requirement maps to a capability the organisation already licenses.
- The specification is a feature list of the outgoing system.
- The chosen approach requires customisation to reach parity with a configurable product.
- No configure/buy/extend option appears in the option set.

**Why it fails.** Microsoft states both halves. On rebuilding: *"Don't replicate your legacy solution… can also lead to a highly customized solution that fails to apply the strengths of the new platform"*, and *"App settings are the safest and least disruptive way to customize your app. You should always try to…"* (`platform-suitability.md` PS-41). On the ladder: configure or buy sits at rung 0, *before any app type* (`application-architecture.md` AA-36 rung 0, §2 first boundary). The corpus also documents the specific case where a custom build duplicates a first-party app and is forced into an *unmanaged-solution-only* posture that conflicts with the managed-production doctrine (`application-architecture.md` AA-20, AP-35). And every extension carries *"performance, ALM, upgrade and support cost"* (`platform-suitability.md` PS-41) — costs a configuration does not.

**Consequences.**
- *Cost:* double payment — the incumbent's licence plus the new build's full TCO (`licensing-cost.md` §6 "existing sunk capability": *"avoid double-paying for a second platform"*).
- *Delivery:* effort spent reaching parity rather than creating value.
- *ALM:* a customisation posture that can conflict with production integrity controls (`application-architecture.md` AA-20; `alm-devops.md` ALM-15's break-list).
- *Operations:* another artefact to monitor, support, patch and eventually retire.

**Detection signals.** Requirement expressed as the outgoing system's feature list · an existing product covering the domain · configuration option absent from the option set · "we need it to work exactly like the old one" · a first-party application in the tenant with overlapping scope.

**Decision impact.** Run the configure/buy/extend check **before** any build decision, and carry it into Options as a priced option. `licensing-cost.md` LC-28 requires the option set to always include *(a) process change without technology, (b) the existing capability already licensed, (c) Power Platform, (d) alternatives, (e) do nothing*. This anti-pattern is the failure to carry (a) and (b).

**Better alternatives.** `alternatives.md` ALT-001 (extend the existing system), ALT-002 (process change), ALT-003 (native platform capability), ALT-007 (existing enterprise platform owns the domain), ALT-011 (buy).

**Exceptions.** The existing capability genuinely fails a stated requirement — recorded per requirement, not asserted. `governance.md` GOV-XB-02 is explicit that reuse is not automatic: *"an incumbent that cannot meet the requirements remains unsuitable."* Also legitimate: the incumbent is being decommissioned on a dated plan, making its configuration a dead end.

**Evidence.** `platform-suitability.md` PS-41, PS-44 (last rows), AP-9, §2 row 26; `application-architecture.md` AA-20, AA-36 rung 0, AP-35, §2; `licensing-cost.md` LC-28, §6; `governance.md` GOV-XB-02; `alm-devops.md` ALM-15.

**Confidence:** HIGH.

---
### 5.2 Data

#### AP-D-008 — Document or spreadsheet store as the relational system of record

**Description.** A list-, library- or spreadsheet-based store is used as the transactional relational store for an application with relational, security, volume or integrity requirements. The commonest motive is licence avoidance; the second commonest is that the data already lives there.

**Classification:** ANTI-PATTERN · **Origin:** MS (every mechanism) + T3/T4 (frequency)

**Trigger conditions.** The store is the system of record **and** any of:
- any queried collection expected to exceed ~2,000 rows with non-trivial filters or sorts;
- more than one or two relationships, or a need for referential integrity beyond opt-in delete behaviour;
- per-row or per-column confidentiality;
- multi-row writes that must succeed or fail together;
- concurrent edits on the same record;
- field-level audit history;
- inclusion in a solution-based release lifecycle.

**Why it fails.** The mechanisms are individually documented and compound: a ~5,000-item list view threshold where *"the LVT limit can't be changed"*; a 12 lookup/person/metadata column ceiling per view or retrieval; the narrowest delegation table of the three connectors (`Not` never delegable, `IsBlank` unavailable on text and complex columns, ID only `=`), producing **silent partial results** rather than errors; ≤ 5,000 unique permission scopes recommended for row access and no column security at all; no transactions and last-writer-wins; lists outside solutions, with internal-name drift across environments. For spreadsheets: *"Simultaneous file modifications … are not supported"*, a six-minute lock, a 25 MB ceiling, duplicate inserts on retry, and Microsoft's own *"Excel isn't a relational database system"* with no transaction threshold published. All defined columns are returned even when unused, making column count a performance parameter for every read; Microsoft instructs partitioning above *"hundreds of thousands of records"*.

**Consequences.**
- *Data:* silent partial results — the failure is **wrong answers, not slow ones** (`performance-scale.md` PF-AP-01); orphaned rows after partial writes; lost updates under concurrency.
- *Security:* confidentiality requirements unenforceable at the store; app-side filtering *"never overrides"* store permissions (`data-architecture.md` DAP-18).
- *Cost:* the licence saving returns as workaround effort, and the documented remediation is a store migration (`licensing-cost.md` LC-27).
- *ALM:* artefacts outside the solution lifecycle (→ AP-D-047).
- *Operations:* incidents present as data-quality complaints, which is the hardest class to diagnose.

**Detection signals.** Row count trajectory over the investment horizon · lookup/relationship count per screen · any confidentiality statement at row or column level · "must all save together" · two people editing the same record · audit or history requirement · the store chosen with an explicit licence rationale · existing threshold errors or "the list got slow".

**Decision impact.** The store choice is a **decision-blocking** input, not an implementation detail: table ownership type is immutable after creation and the virtual/standard choice is irreversible (`data-architecture.md` DA-12, `security.md` SEC-09). Where any trigger condition holds, the option set must contain a governed relational store (and therefore its licence consequence for the whole audience) or a different platform — never the cheap store plus a workaround.

**Better alternatives.** A governed relational operational store (`alternatives.md` ALT-004 with its premium consequence); the existing relational database where it *"can't be moved"* — Microsoft's own stated trigger (`data-architecture.md` SQ2-15); keeping the data in its owning system with read-through (ALT-001, ALT-007); a document-centric store where **the document genuinely is the record**, which is its documented strength (`data-architecture.md` §2 row 7); process change that removes the relational requirement (ALT-002).

**Exceptions.** Legitimate and common: the document is the record (files + metadata + versions + retention labels + protection that travels with the file); small flat trackers with ≤ 1–2 lookups, list-level security, single environment, low write concurrency; a form over a single list where the readers are the list's readers; seeded-licence scope with no relational ambitions. `data-architecture.md` §6 states these positively — this anti-pattern is not "never use it".

**Evidence.** `data-architecture.md` DAP-1, DAP-2, DAP-18, DA-39, DA-40, DA-41, DA-42, DA-44, DA-61, §2 rows 1–7, §6; `platform-suitability.md` AP-5, PS-14, PS-43; `performance-scale.md` PF-AP-01, PF-AP-11, PF-AP-12, §8.1 items 38–40; `licensing-cost.md` LC-AP-01, LC-27.

**Confidence:** HIGH.

---

#### AP-D-009 — The operational store serving the analytical workload

**Description.** Dashboards, aggregates, trend reporting and cross-period history are served directly from the transactional store that the application writes to.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.**
- Aggregation over growing data — the corpus's documented failure point is ~50,000 rows for aggregate operations, with query timeouts at 5 minutes (2 minutes for `SELECT *`/joins on the T-SQL endpoint).
- Multi-year or cross-period trend reporting.
- Operational reporting running concurrently with transactional work on the same identities.
- "We need live reporting" stated as a requirement without a freshness number.

**Why it fails.** Two independent mechanisms. First, hard aggregate and timeout ceilings: aggregation beyond the documented row count fails outright — while, importantly, *ordinary filtered reports* are explicitly *"allowed to span large datasets that are beyond 50,000 rows"* within the timeout window, so the boundary is **aggregation, charts and cross-period history**, not report size (`data-architecture.md` DA-03 revised). Microsoft's instruction is direct: *"use a dedicated datastore for reporting purposes instead"*. Second, contention: reporting *"consumes the same per-identity service-protection budget as transactional work"*, so the symptom surfaces in the application rather than in the report (`performance-scale.md` PF-46, PF-AP-16, `performance-scale.md` DC-19). A third, subtler mechanism applies to the remedy: **security does not travel to the copy.** Analytical replicas need row-level security rebuilt; secured columns export as null unless the sync identity holds the column profile; embedded report visuals ignore application roles — *"security roles and privileges don't affect the data that is displayed"* (`data-architecture.md` DA-20, DA-22, DAP-17).

**Consequences.**
- *Performance:* application slowdown caused by reporting, diagnosed in the wrong place.
- *Data:* an analytical copy that under-enforces confidentiality, or over-exposes it when the documented fix widens access to all readers of the copy (`data-architecture.md` C-07).
- *Cost:* replica storage billed on the platform's own database meter; *"can double or triple your storage footprint"* with no published ratio (`data-architecture.md` DA-19, U-01).
- *Business:* reporting requirements met late, after the architecture is fixed.

**Detection signals.** Aggregate/KPI/trend requirement over a growing table · "live reporting" with no freshness figure · dashboards over the transactional store in the current state · report users and transaction users sharing identities · a compliance requirement on who may see which rows *in reports*.

**Decision impact.** An analytical copy is required **from day one** whenever aggregation, charts or cross-period history over growing tables is in scope (`data-architecture.md` §3). That decision carries its own budget (replica storage), its own security work (rebuild row and column security in the copy), its own freshness ceiling (*"near real-time"* is undefined; plan for ≤ 1 hour — `data-architecture.md` C-11), and its own resilience gap (analytical replication is **not** covered by cross-region failover — `performance-scale.md` DC-19, `operations-support.md` OP-19). It is not a reporting add-on.

**Better alternatives.** A dedicated analytical store fed one-way from the operational store; the free read-only analytical SQL endpoint where no write requirement exists — *"prefer this over a custom pipeline whenever no write requirement exists"* (`data-architecture.md` SY-02, SY-03); import-mode reporting for modest volumes; per-user-secured direct query where the requirement is that reporting respect record security (`data-architecture.md` DA-20, with its limits).

**Exceptions.** Small, non-growing datasets with filtered (non-aggregating) operational reports inside the timeout window; and per-user-secured reporting through the documented direct-query path, which is the one case where keeping reporting on the operational store is the *correct* answer because security travels.

**Evidence.** `data-architecture.md` DAP-3, DAP-16, DAP-17, DA-03, DA-19, DA-20, DA-21, DA-22, DA-51, SY-02, SY-03, C-07, C-11, U-01, §2 rows 10–11; `performance-scale.md` PF-AP-16, PF-46, B-12, DC-19; `operations-support.md` OP-19; `integration-architecture.md` §8 ("copy proliferation for reporting"), §12.8.

**Confidence:** HIGH.

---

#### AP-D-010 — Shadow system of record

**Description.** Data owned and mastered by another system is replicated into the new platform at greater scope than the application needs — often the whole entity, often including closed history — creating a second de facto master.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.**
- The replication scope is "the whole table" or "the whole module" rather than a named field set.
- Closed or historical transactions are in scope.
- Authoritative ledgers (financial postings in particular) are in the replication scope.
- The stated reason is convenience of access rather than a platform data feature the application requires.

**Why it fails.** Microsoft's statements are direct: *"Too much data synchronized … overloads the database. You should use a dedicated data warehouse"*, and migration scope is enumerated as **master data and open transactions** — not history (`data-architecture.md` DA-51, DA-54; note U-41 records that Microsoft does not state "don't migrate history" as a rule, so the boundary is an inference from the enumerated categories and must not be attributed to Microsoft as a prohibition). For ledgers the exclusion *is* explicit in Microsoft's own bidirectional product: *"Financial posting entities … are deliberately excluded from dual-write, avoiding any shadow-ERP behavior"* (`integration-architecture.md` I-26, X-14). Mechanically, the copy consumes the database capacity meter — the one meter that cannot be offset (borrowing runs Database → Log → File only) — and every synchronised write consumes per-identity service-protection budget.

**Consequences.**
- *Data:* two masters, divergence, and no defensible answer to "which is right".
- *Cost:* capacity growth on the most expensive meter; overage **blocks restore, copy, recover and environment creation** (`operations-support.md` OP-22, `licensing-cost.md` LC-05).
- *Governance:* the owning system's controls and audit obligations are not inherited by the copy.
- *Operations:* a reconciliation obligation that was never scoped or funded (→ AP-D-013).

**Detection signals.** Replication scope stated as a table or module · history in scope · ledger entities in scope · no named platform data feature justifying the copy · no field-level ownership map · no reconciliation job in the design.

**Decision impact. Replicate only what a named platform data feature requires, keyed by the source identifier, as a disposable read model.** Where the application needs only to read, the decision is read-through, not copy (`data-architecture.md` DA-45, DA-46). Where a copy is genuinely required, its scope, its ownership map, its reconciliation job and its capacity cost enter the option's economics as first-class components.

**Better alternatives.** Keep the data in place with read-through virtualization for narrow reference reads (subject to AP-D-012's exclusion list); a one-way replicated subset as an explicitly disposable read model; events from the owning system; an analytical path for reporting needs (AP-D-009); `alternatives.md` ALT-001, ALT-007, ALT-009.

**Exceptions.** A named platform data feature the application genuinely needs on that data — audit, row/column security, search, offline, rollups, charts, business process flows — which the read-through mechanism forfeits by design. Then a scoped one-way replica is the documented answer, not an anti-pattern.

**Evidence.** `data-architecture.md` DAP-4, DA-45, DA-46, DA-51, DA-54, DA-62, U-41, §2 row 13; `integration-architecture.md` I-26, X-14, §8; `architecture-patterns.md` AP-07, Y-06; `operations-support.md` OP-22; `licensing-cost.md` LC-05.

**Confidence:** HIGH (mechanisms MS; the history boundary is INF and flagged).

---

#### AP-D-011 — Bidirectional synchronisation without field ownership and reconciliation

**Description.** Two systems both edit the same entity, and the design provides a two-way pipeline without a per-field ownership map, conflict rules, a reconciliation pass, or an agreed behaviour under sustained far-side failure.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Two-way editing of one entity, plus any of:
- no per-field ownership matrix;
- no stated conflict rule (last-writer-wins is a decision, not a default);
- no reconciliation pass with a cadence;
- fan-out beyond one-to-one;
- business-critical data with no defined safe outage envelope.

**Why it fails.** Microsoft's own description of the pattern is *"There's no clear record keeper"*, and its own bidirectional product exists for exactly one system pairing while *"making crucial changes in the Dataverse schema"* and being characterised as *"tightly coupled"*; the general guidance is *"Avoid creating tightly coupled point-to-point…"* (`data-architecture.md` DA-48, C-15; `integration-architecture.md` I-15). Outside that product, bidirectional synchronisation is a **build** — with hand-written conflict resolution: *"Tricky conflict resolution. Data gets copied for each system"*. Three compounding facts: at-least-once delivery makes duplicates the norm (`integration-architecture.md` I-44); the reference design's *"Nightly dataflows … correct any missed or failed event-driven updates"* means **the fast path is assumed to lose updates**; and the documented replication mechanisms *cannot* change statuses or delete rows absent upstream, so status and deletion drift is structural (`integration-architecture.md` I-28). Fan-out beyond 1:1 is explicitly out of scope for the documented design: *"Scenarios where one master environment must synchronize with multiple other environments require a more scalable or distributed solution."*

**The decision-blocking unknown.** Manifest reservation **NB-01 / `IA-U-14`** stands: behaviour under *prolonged* far-side failure — what happens to the initiating transaction, and how pause/catch-up behave — remains `UNKNOWN`, and the safe outage/backlog envelope and business invariants are therefore unestablished for critical bidirectional use. The manifest's handling rule is to **keep it UNKNOWN and require a bounded failure/recovery test plus explicit reconciliation rules before approving critical bidirectional synchronisation.** This is not a gap to reason past.

**Consequences.**
- *Data:* silent divergence; conflicting writes; deletion and status drift; duplicates.
- *Business:* decisions taken on whichever copy the user happened to open.
- *Operations:* an unowned queue of unresolved conflicts; a restore on one side rewinds one participant while the other retains later state (`alm-devops.md` §14.4).
- *Governance:* nobody named to adjudicate conflicts (`governance.md` GOV-XB-04 requires four named roles: field authority, who may replay/compensate, who approves manual resolution, who signs off reconciliation after restore).

**Detection signals.** "Both systems need to update it" · no field-ownership matrix · no reconciliation cadence · more than two participants · no self-triggering-loop guard · no stated behaviour when the far side is down for a day.

**Decision impact.** Prefer **per-field one-way** flows. Where bidirectional is genuinely required, treat it as `DECISION BLOCKED` for business-critical data until: (1) a per-field ownership matrix exists; (2) conflict rules are stated and accepted; (3) a reconciliation pass with a cadence is designed and funded; (4) the four governance roles are named; (5) the bounded failure/recovery test required by NB-01 has been run. Fan-out beyond 1:1 changes the pattern to publish-once-subscribe-many, not a second pipeline.

**Better alternatives.** Single-writer-per-lifecycle-phase with authority handover (`integration-architecture.md` I-26, IA-36/IA-37); per-field one-way flows; a broker with publish-once fan-out for 1:N; the owning system keeps authority and the platform reads through.

**Exceptions.** The vendor-supported bidirectional product for its one supported system pairing, adopted with its schema changes accepted. And low-value, loss-tolerant data where last-writer-wins is explicitly accepted and recorded.

**Evidence.** `data-architecture.md` DAP-5, DA-48, DA-49, C-15, §2 row 16; `integration-architecture.md` I-15, I-26, I-28, I-44, §8 (synchronization risk register), manifest **NB-01 / `IA-U-14`** (= `integration-architecture.md` `U-14` in the mounted snapshot; the qualified form is the canonical one per `pre-canonicalization-repair.md`), §12.3; `architecture-patterns.md` AP-07, Y-07, matrix rows 21–22, APR-U-11; `governance.md` GOV-XB-04; `alm-devops.md` §14.4, §14.5; `security.md` SEC-XB-04; manifest NB-01.

**Confidence:** HIGH on the mechanisms; the far-side-failure envelope remains UNKNOWN by design.

---

#### AP-D-012 — Data virtualization chosen without its exclusion list

**Description.** External data is surfaced in place, as if native, to avoid a copy — without checking that the application does not require any of the platform data features the mechanism forfeits, and without measuring it at the intended volume.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Virtualization selected while the requirement includes any of: field-level security, row-level security (the surfaced tables are organization-owned only), auditing, search, charts or dashboards, rollups or calculated columns, offline caching, queues, activities, business process flows. Or: the dataset is large, or writes are required, or a negative-filter ("does not contain") search is exposed over it.

**Why it fails.** The exclusions are documented and total — *"All forfeited by design"* — and the choice is **irreversible**: a virtual table cannot be converted to a standard table. Two further mechanisms make the volume case worse than it looks: Microsoft publishes **no performance, latency, throughput, caching or query-pushdown characterisation at any volume**, and the mechanism is absent from the delegable-data-source list, so *truncation can occur without a delegation warning appearing at all*; column selection is ignored (all attributes always return); and it can never be the "1" side of a one-to-many relationship. Negative filter operators *"corrupt paging beyond page 1"* with *"no supported workaround"*. The corpus records two independent documented cases where this mechanism was selected and then **rejected on row-level security** during design (`architecture-patterns.md` Y-05, Q-15). Manifest reservation **NB-05 / `APR-U-06`** additionally keeps write-through virtualization conditional: the capability exists, but production pattern and performance evidence remain weak, and `APR-C-02` records the read-versus-CRUD question as unresolved.

**Consequences.**
- *Security:* a confidentiality requirement discovered to be unenforceable after the model is built.
- *Data:* silent truncation with no warning; corrupted paging on negative filters.
- *Architecture:* an irreversible modelling decision; a relationship shape that cannot be expressed.
- *Delivery:* redesign to replication, with its full synchronisation obligation, late.

**Detection signals.** Any exclusion-list item in the requirement · row count over the low hundreds against the external source · write requirement · free-text search including negative operators · "real-time, no copy" stated as the goal without a freshness number traced to the *upstream* source.

**Decision impact.** Check the exclusion list against the requirement **before** selecting the mechanism, and require a **measured spike** at representative volume before commitment. Appropriate scope is a narrow, positively-filtered, read-mostly, sub-1,000-row reference or lookup surface — not a general integration layer. Where any exclusion is required, the decision moves to replication (with AP-D-010/AP-D-013's obligations) or to keeping the interaction in the owning system.

**Better alternatives.** A scoped one-way replicated read model; a connector call for per-request reads with the synchronous dependency accepted; an API-mediated read where composition or per-user authorization is needed; embedding the owning system's own surface.

**Exceptions.** Narrow reference/lookup reads with uniform security, acceptable upstream freshness, and no platform-data-feature requirement — the mechanism's documented sweet spot. Note the freshness trap even here: virtualizing over a batch-loaded store gives *"false freshness"*, because *"the actual freshness of that data depends on how frequently the upstream source systems load and refresh"* (`integration-architecture.md` I-32).

**Evidence.** `data-architecture.md` DAP-9, DAP-34, DAP-35, DA-45, VT-04, VT-05, VT-06, VT-09, VT-10, VT-17, §2 rows 13–14, 26; `platform-suitability.md` PS-56; `architecture-patterns.md` AP-06, Y-05, Q-13, matrix rows 16–19, APR-C-02, APR-U-06; `integration-architecture.md` §7 item 10, I-32, §8 ("false freshness"); manifest NB-05.

**Confidence:** HIGH on the exclusions; write-through remains conditional per NB-05.

---

#### AP-D-013 — Replica trusted without drift detection

**Description.** A replicated copy is treated as equivalent to its source because the replication mechanism reports success, with no divergence detection beyond row counts and no reconciliation budgeted as routine work.

**Classification:** **GATE** (reclassified 2026-09-03 — where it holds, the option is *unavailable*, not worse; see §2) · **Origin:** MS

**Trigger conditions.** A replica exists and any of:
- the only integrity check is a row-count comparison;
- no reconciliation job with a cadence and an owner;
- resynchronisation is treated as an incident rather than a routine operation;
- the replica is used for decisions, compliance evidence or downstream writes;
- the replica participates in the recovery plan.

**Why it fails.** The corpus documents **at least eight silent-divergence modes that all report sync success**: secured columns export as null unless the sync identity holds the column-security profile; calculated columns freeze at their initial value if the row version does not change; direct-SQL deletes never propagate; new columns do not appear until a data change occurs. *"Row-count comparison does not detect drift"*, and Microsoft's documented remedy for most of these is *"resynchronize the table"* — which *"must be budgeted as a routine operation, not an incident"* (`data-architecture.md` SY-14, SY-15, DAP-31). Two related traps: run-resubmission is not a reconciliation mechanism (20 runs per batch, capped by connector limits, no duplicate protection — `data-architecture.md` DAP-33); and there is **no first-party managed replication service** to a writable relational target, so every such copy is customer-built and customer-operated, watermark, delete-detection and reconciliation included (`data-architecture.md` SY-01, SY-18, DAP-30). Cost of a full resynchronisation at realistic volume is `UNKNOWN` (`data-architecture.md` U-39).

**Consequences.**
- *Data:* decisions and reports based on stale or null values that look complete.
- *Business:* compliance evidence that is quietly incomplete — secured columns exporting as null is the sharpest case.
- *Operations:* an unbudgeted recurring resynchronisation, of unknown duration.
- *Cost:* a pipeline whose real operating cost was never in the option's economics.

**Detection signals.** No reconciliation job in the design · row counts cited as the integrity check · column-security or calculated columns in the replicated set · deletes performed at the source outside the application · "the sync is green" as the assurance statement · the replica in scope for compliance reporting or recovery.

**Decision impact.** A replication decision is only complete when it includes: a divergence-detection method that is not a row count; a reconciliation job with a cadence and a named owner; a budgeted, measured resynchronisation procedure; and an explicit statement of which columns are known to diverge silently. Absent these, the replication option is **not available** for material data — this is one of `architecture-patterns.md` §13's composed disqualifiers (*"Replication + no reconciliation owner + recovery/restore requirement"* → the pattern is unavailable, not merely expensive).

**Better alternatives.** Read-through where no platform data feature is required (AP-D-012's sweet spot); the free read-only analytical endpoint where writes are not needed (`data-architecture.md` SY-02); a narrower replica scope, which shrinks the reconciliation surface; keeping the decision in the owning system.

**Exceptions.** A disposable read model whose divergence is tolerable and which is rebuilt rather than reconciled — provided "rebuild" is a tested procedure with a known duration, and nothing downstream treats it as authoritative.

**Evidence.** `data-architecture.md` DAP-30, DAP-31, DAP-32, DAP-33, SY-01, SY-04, SY-10, SY-12, SY-13, SY-14, SY-15, SY-18, C-20, U-39; `integration-architecture.md` I-28, §8; `architecture-patterns.md` AP-07, Y-07, §13; `governance.md` GOV-XB-04; `alm-devops.md` §14.4, §14.5.

**Confidence:** HIGH.

---

#### AP-D-014 — System of record undeclared

**Description.** The engagement proceeds without a written, per-entity (and where necessary per-field and per-lifecycle-phase) statement of which system holds authority — usually because the terms are assumed to have a shared meaning.

**Classification:** ANTI-PATTERN · **Origin:** MS (the vocabulary gap) + INF (the framing)

**Trigger conditions.**
- "System of record" or "source of truth" used in requirements without a per-entity assignment.
- Two or more systems hold the same entity and none is designated.
- Authority changes at a lifecycle boundary (quote → order → invoice) and this is not modelled.
- Integration design begins before ownership is assigned.

**Why it fails.** There is **no single vendor definition to borrow**. The corpus establishes this carefully: the implementation guidance uses *"primary data"* and *"master data source"*; the architecture guidance's only near-definition ties *"source of truth"* to a **consistency requirement** per entity (*"Use a single source of truth when you require strong consistency… Other services might hold their own copy… not considered the source of truth"*); and *"system of record"* is itself shown handing over between systems at a lifecycle boundary. The corpus's conclusion is explicit: *"the pack must declare its own vocabulary as pack-local, never cite Microsoft as the authority for a formal distinction"* (`data-architecture.md` DQ-03, DQ-15, U-14). Without a declared assignment, ownership is decided implicitly by whichever pipeline was built first — and ownership is the variable that decides read-versus-copy, sync direction, conflict rules, and which system's controls and audit obligations apply (`integration-architecture.md` IA-36, IA-37; `architecture-patterns.md` §3.1 Ownership row).

**Consequences.**
- *Data:* the preconditions for AP-D-010, AP-D-011 and AP-D-013 all follow from this omission.
- *Architecture:* read-versus-copy decided by accident.
- *Governance:* no field authority to adjudicate conflicts (`governance.md` GOV-XB-04's first named role).
- *Business:* two answers to the same question, with no tie-break.

**Detection signals.** The phrase used without an assignment table · the same entity in two systems with no designation · lifecycle-phase authority handover in the process narrative · integration design underway with ownership unassigned · conflicting figures already reported by different teams.

**Decision impact.** Produce a per-entity ownership assignment — extended to per-field and per-lifecycle-phase where the process requires it — **before** any integration or store decision. Where ownership cannot be established, it is a decision-blocking unknown (DC-D-021); the corpus names it as one of the signals a discovery process should carry (`integration-architecture.md` §13.2: `system_of_record_undecided`).

**Better alternatives.** An entity/field ownership matrix with a named business owner per row; single-writer-per-phase with explicit authority handover; a declared pack-local vocabulary, stated as pack-local.

**Exceptions.** A genuinely single-system domain with no second copy anywhere — in which case the assignment is trivial but should still be written down, because the *second* copy is usually added later without revisiting it.

**Evidence.** `data-architecture.md` DQ-03, DQ-15, U-14, §3 (last boundary); `integration-architecture.md` IA-36, IA-37, §9 row 9, §13.2; `architecture-patterns.md` §3.1 (Ownership / system of record row); `governance.md` GOV-XB-04.

**Confidence:** MEDIUM (the vocabulary gap is MS-evidenced; the anti-pattern framing is INF).

---

### 5.3 Automation and process

#### AP-D-015 — Automation shape mismatch

**Description.** A requirement whose real shape is process orchestration, integration orchestration or distributed processing is implemented as workflow automation, because workflow automation is the tool in front of the team.

**Classification:** ANTI-PATTERN · **Origin:** INF (the taxonomy) over MS capability facts

**Trigger conditions.** Apply the corpus's ordered test; a mismatch exists when the requirement's shape is not the shape being built:

| Shape | Defining question | What must hold the state |
|---|---|---|
| Integration orchestration | Is the primary artefact a **message that must not be lost, duplicated or reordered**? | the broker |
| Distributed processing | Must work be **split and recombined**, or does one step need real computation? | a job/partition ledger |
| Process orchestration | Must the process **outlive a single run** — survive 30+ days, a deployment, a version change, or resume mid-way? | an explicit, queryable process record outside the run |
| Workflow automation | Otherwise | the run instance plus the business record |

**Why it fails.** The shapes are distinguished by *what holds the state* and *what the unit of failure is* — which is what actually decides the technology. A workflow engine is a first-class workflow automation engine and a competent front door to the other three, but it *"is not a state store, not a broker, and not a compute host"*. The corpus's judgement is blunt in both files that build a taxonomy: *"Most failed Power Automate architectures are a shape-2/3/4 requirement implemented as shape 1"* and *"Most Power Platform performance failures in this corpus … are a shape-2/3/6 requirement implemented as shape 1."* The concrete consequences are the documented ceilings of the wrong shape: a 30-day hard run-duration ceiling *including pending human waits*, with run state not addressable once the run ends; no ordering, deduplication or dead-letter construct; ordering obtainable only by a trigger setting that is **irreversible**, drops triggers and collapses batch size; loop parallelism defaulting to 1.

**Consequences.**
- *Architecture:* reliability properties approximated in the wrong layer (→ AP-D-018, AP-D-021).
- *Data:* lost or duplicated work at the shape boundary.
- *Business:* a process that cannot answer "where is instance 4711?" after 30 days.
- *Delivery:* rebuild when the mismatch surfaces, typically in production.

**Detection signals.** Process duration in months · "must resume where it left off" · "must not be lost / must be in order / must not be processed twice" · fan-out/fan-in language · a computation described as a step · an approval expected to wait longer than a month · run history proposed as the audit trail.

**Decision impact.** Classify the shape first; the shape selects the technology family, and only then does the option set form. Workflow automation stays the right answer for bounded human/document sequences under a month — the corpus is explicit that moving the human-approval leg elsewhere loses a first-class, standard-connector capability with no equivalent in the alternatives.

**Better alternatives.** Durable state in a business process record with a re-triggering automation; a broker carrying the delivery guarantee with an idempotent consumer; a purpose-built durable orchestrator for fan-out/fan-in and resumable state; bulk APIs or data pipelines for volume — *with the workflow retained as the initiator and business-facing front door*, which is the corpus's recommended hybrid shape.

**Exceptions.** A shape-2/3/4 requirement of genuinely low volume and loss tolerance, where the workaround is cheaper than the second operating model — the corpus makes this argument explicitly for organisations with *"no Azure operating model"* (`automation-architecture.md` §4.1). This exception must be recorded with the accepted loss, not assumed.

**Evidence.** `automation-architecture.md` §2 (the four shapes and the classification test), §4.1–§4.3, AT2-13, AT2-14, AT2-18, AT2-21, AT2-32, AT2-06, AT2-07, N-04, N-05, N-07, N-09; `performance-scale.md` §1, PF-36, PF-34, PF-37; `integration-architecture.md` §2.2, IA-46.

**Confidence:** MEDIUM (taxonomy is INF; every constituent capability fact is MS).

---

#### AP-D-016 — Workflow engine as a high-volume transaction engine

**Description.** Sustained per-record transaction volume — ETL, mass processing, nightly bulk loads, high-frequency integration — is processed one record per action inside a workflow engine.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.**
- Per-record work over thousands of records per run, or sustained rates approaching any of the platform's meters.
- Nightly or scheduled bulk load as the integration mechanism.
- Transformation of large datasets inside the automation.
- The automation is the enterprise integration backbone by default rather than by design.

**Why it fails.** Microsoft states the boundary directly: complex business logic and large-scale transformation *"do not belong in cloud flows"*, and its own remedy for bulk work is batch/bulk APIs and data pipelines rather than a different orchestrator. Four mechanisms then bite: (1) **action multiplication** — every action, including retries and pagination, consumes the owner's request entitlement, and *"Retries and extra requests from pagination count as actions"*; (2) **the meters are evaluated separately** — *"Batch operations aren't a valid strategy to bypass entitlement limits. Service protection API limits and entitlement limits are evaluated separately"*; (3) **failure is silent, then terminal** — sustained overload does not error, *"flow activity slows"*, and *"if a cloud flow consistently remains above the limits for 14 days, the system turns it off"*, while editing the flow **resets the evidence**; (4) **structural ceilings** — 500 actions per definition, 8 nesting levels, 5,000 array items on the low profile. Nightly bulk loading additionally collides with per-identity five-minute service-protection windows, and Microsoft's stated direction is *"move towards real-time integration"*.

**Consequences.**
- *Business:* the process stops without a decision, fourteen days after the problem started.
- *Cost:* consumption billed on retries and pagination; the documented remedy for throttling is **commercial** — buy capacity, buy a capacity licence, or move to consumption billing.
- *Operations:* the failure mode is invisible without a monitored throttling metric (→ AP-D-021).
- *Data:* partial completion with no rollback (→ AP-D-018).

**Detection signals.** Records per run in the thousands · a nightly window as the integration design · transformation described as a flow step · loops over collections of unbounded size · existing throttling or 429s · "we re-published it and it's fine" as an incident resolution.

**Decision impact.** Keep the automation as **initiator and orchestrator**; move the volume to a bulk mechanism, a data pipeline, a broker with workers, or an in-platform mechanism that is exempt from the per-identity meter. That exemption is the corpus's highest-leverage documented remedy: *"Service protection limits don't apply to data operations that originate from plug-ins and custom workflow activities"* — so the data-heavy leg moves to server-side code inside the platform, not necessarily out of it. Above the three-meter envelope with no natural partitioning, the integration responsibility leaves the platform (`integration-architecture.md` §12.4).

**Better alternatives.** Bulk/batch data APIs; data pipelines and dataflows for movement and transformation; server-side platform code (plug-in / custom API) for the metered data leg; broker plus workers for sustained throughput; `alternatives.md` ALT-006, ALT-009.

**Exceptions.** High volume where the *processing* can be delegated: the automation issues one request and a bulk mechanism does the work — Microsoft's own remedy, and explicitly **not** an anti-pattern (`automation-architecture.md` §4.1). Also genuinely bounded peaks that fit the meters with headroom at the horizon.

**Evidence.** `platform-suitability.md` PS-07, PS-25, AP-1, AP-2, §2 rows 10, 16, 19; `automation-architecture.md` AT2-02, AT2-04, AT2-08, AT2-10, AT2-35, AT2-62, N-02, N-03, §4.1, §4.3; `performance-scale.md` §2, PF-22, PF-29, PF-33, PF-34, PF-AP-06, PF-AP-14, B-04, B-09, §8.1 items 6, 24; `data-architecture.md` DAP-6, DA-10, DA-51; `integration-architecture.md` §12.4, §12.8, IA-10; `licensing-cost.md` LC-09, §7.2 items 24, 26.

**Confidence:** HIGH.

---

#### AP-D-017 — Retry enabled on non-idempotent writes

**Description.** Automatic retry is left at its default on actions with side effects, without an idempotency mechanism — so a transient failure produces duplicate records, duplicate notifications or duplicate downstream transactions.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.**
- A side-effecting write (create, post, send, charge) on a retryable action with no idempotency key.
- No stable business key available to deduplicate on.
- At-least-once transport anywhere on the path.
- Retry configured at more than one layer of the same call chain.

**Why it fails.** Retry is **on by default**, and Microsoft's own examples of its consequence are a repeated insert causing *"incorrect values in the table"* and a repeated notification meaning users *"might receive duplicate messages"*. Trigger-side delivery is at-least-once, and the general transport rule is stated plainly: *"Most queue services deliver messages with at-least-once semantics, which means that consumers can receive the same message more than once. Design consumer logic to be idempotent."* Retry depth is not even stable across the estate — it is a function of the **owner's licence** (2 retries on one profile, 12 on others), so the same design duplicates differently depending on who owns it. The concrete in-platform idempotency mechanism is an alternate key with upsert semantics — which requires a stable business key to exist, and **duplicate detection is not a substitute**: it is suppressed by default on API updates, has no default rules outside a few standard entities, and returns an error status that naive retry logic loops on.

**Consequences.**
- *Data:* duplicate transactions in systems of record; corrupted aggregates.
- *Business:* duplicate customer communications, duplicate payments, duplicate orders.
- *Cost:* retries are billed as actions, so an unreliable dependency is a cost driver at the same time as a correctness one.
- *Operations:* the incident surfaces downstream, far from the cause.

**Detection signals.** Any side-effecting action on a retried path · no stable business key in the payload · retry configured at several layers · an unreliable dependency in the chain · existing duplicate-record complaints · a broker or trigger anywhere on the path.

**Decision impact. Idempotency is a precondition for enabling retry on a side-effecting action, not a later refinement.** The decision it forces is upstream: **does a stable business key exist?** If not, the requirement must fund creating one (DC-D-052). Where no key can exist and duplicates are intolerable, the design must move the write inside a single transactional boundary or accept and document the duplicate risk with a named owner. One retry owner per call chain must be named in the design.

**Better alternatives.** Alternate key plus upsert; an explicit idempotency-key check against a durable ledger; broker-level duplicate detection where the transport offers it; collapsing the write into one transactional owner; a documented accepted risk where the value does not justify the key.

**Exceptions.** Genuinely idempotent operations (pure updates to a known key, reads, set-to-value writes). And low-consequence duplicates explicitly accepted — a duplicate log entry is not a duplicate payment.

**Evidence.** `automation-architecture.md` AT2-16, AT2-55, AT2-56, N-06, §9 rows 8–9; `data-architecture.md` DA-52, DA-53, DAP-39, DQ-12, DA-60; `integration-architecture.md` I-44, §8 ("duplicate processing"), IA-15, §9 rows 12, 26; `performance-scale.md` PF-38, §8.1 item 23; `architecture-patterns.md` Y-11, matrix row 10; `licensing-cost.md` LC-09.

**Confidence:** HIGH.

---
#### AP-D-018 — Transaction semantics hand-built in orchestration logic

**Description.** A multi-step, multi-system operation is treated as a transaction by writing "check everything succeeded and undo it if not" inside the orchestration, with no durable state and no compensation design.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Writes that must succeed or fail together, spanning either two systems, or two connectors, or a store that offers no transaction — combined with the absence of a saga design (per-step idempotency keys, compensating actions, a persisted in-doubt state, irreversible steps ordered last, a human resolution path).

**Why it fails.** No cross-connector transaction construct exists; the in-platform change set is same-connector only, cannot contain a loop, and cannot chain outputs; the low-code expression language is *never* atomic even within one store; and **nothing in the error-handling guidance describes an undo** — a failed run leaves completed actions completed. So the "undo" branch is a hand-built saga whose own state lives in the run, and the run's history expires. Meanwhile the synchronous outbound-notification variant is a documented dual-write hazard: *"the data operation rolls back but the request sent to the configured endpoint can't be recalled."*

**Consequences.** *Data:* orphaned and half-posted records; inconsistent state across systems with no in-doubt marker. *Business:* financial or inventory positions that do not reconcile. *Operations:* no queue of in-doubt items to work, because the design never created one. *Governance:* nobody named to adjudicate or replay (`governance.md` GOV-XB-04).

**Detection signals.** "It all has to save together" across systems · a compensating branch inside the orchestration · no in-doubt state field on the business record · no reconciliation job · a synchronous callback firing inside a transaction.

**Decision impact.** Either **collapse the unit of work into one system's transaction** — the corpus's preferred shape, with one system composing and then handing authority over — or move the orchestration to a host with durable state and compensation. Where temporary inconsistency is genuinely intolerable, Microsoft's instruction is to *"Use strong consistency mechanisms or atomic transactions across all steps instead"*, which no pattern in this corpus supplies across systems — making it a platform-exit condition (`integration-architecture.md` §12.3, `architecture-patterns.md` matrix row 20).

**Better alternatives.** Single-transaction collapse; in-store change set or server-side code where all writes are in one store; an explicit saga with durable state, idempotency keys, ordered irreversible steps and a human resolution path; an external durable orchestrator; `alternatives.md` ALT-006, ALT-007, ALT-009.

**Exceptions.** All writes inside one store that offers a transaction construct — then atomicity is available and this is not an anti-pattern. And genuinely compensable business operations where eventual convergence with a reconciliation pass is accepted and documented.

**Evidence.** `automation-architecture.md` AT2-17, AT2-19, AT2-21, AT2-64, §4.2; `platform-suitability.md` PS-45, AP-13, §2 row 28; `data-architecture.md` DA-07, DA-50, DA-52, DAP-7, DAP-8, §2 row 3, §6 (last bullet); `integration-architecture.md` IA-19, IA-20, IA-21, X-08, X-16, §12.3; `architecture-patterns.md` matrix row 20, §13 (first composed disqualifier); `governance.md` GOV-XB-04; `security.md` SEC-XB-04.

**Confidence:** HIGH.

---

#### AP-D-019 — Synchronous chain across heterogeneous availability

**Description.** A user-facing or time-bounded operation calls several systems in sequence, synchronously, where the participants have different availability profiles and different owners.

**Classification:** ANTI-PATTERN · **Origin:** MS (the constituent facts) + INF (the framing)

**Trigger conditions.** Two or more synchronous hops on the request path; at least one participant is customer-operated or externally owned; the operation has a user or caller waiting; or the aggregate path approaches a synchronous window.

**Why it fails.** Each hop pins the whole chain to the slowest and least available participant, and every documented remedy is decoupling — queue-based load levelling, competing consumers, dead-lettering — not larger retry counts. The synchronous windows are hard and layered (a flow's inbound and outbound windows, a canvas app's outbound window, a plug-in's execution ceiling), and *"the documented remedy is asynchronous, not a longer timeout"*. Availability compounds in the wrong direction: the governing figure is the **weakest link in the integration path, including the parts the customer operates** — a gateway host is a customer-operated Windows VM that Microsoft *"doesn't investigate poor performance"* for when overloaded. On a high-latency link the binding constraint becomes round-trip **count**, not per-call latency.

**Consequences.** *User:* time-outs presented as application failure. *Business:* the composite availability is worse than any single participant's, and worse than what was promised (→ AP-D-056). *Operations:* an incident in one owner's system pages another owner's on-call. *Cost:* retries multiply load precisely during the dependency's outage.

**Detection signals.** Chained dependent calls on the user path · a hard "must see the result immediately" statement · a participant with no published or measured availability · a customer-operated component on the path · existing time-out complaints · high-latency or satellite users.

**Decision impact.** Decouple at the first boundary where availability differs, and version the message contract across it. The number of synchronous hops on a user-facing path is an architectural budget, not an implementation detail. Where the requirement is a hard synchronous latency across fragile participants, no pattern in the corpus sizes it — that is a platform-exit condition (`performance-scale.md` B-16).

**Better alternatives.** Respond inside the window and continue asynchronously with a status resource; a broker between producer and consumer; caching or a local read model for the weakest participant; API-mediated composition shaped server-side; renegotiating the immediacy requirement.

**Exceptions.** A single hop to a highly available participant, inside the window, with the coupling accepted — the documented conditions under which direct integration is not merely acceptable but preferred.

**Evidence.** `automation-architecture.md` AT2-27, AT2-29, AT2-43, AT2-65, AT2-12, §4.2; `integration-architecture.md` X-07, IA-06, IA-07, IA-08, IA-09, IA-24, IA-26, IA-27, §2.1 rows 4, 5, 10, §4.1, §4.3; `performance-scale.md` PF-04, PF-11, PF-12, PF-13, PF-35, PF-AP-07, B-08, B-16, DC-07, DC-11; `data-architecture.md` DA-34, DA-35, DA-47, DAP-21, DAP-28, §2 row 15; `platform-suitability.md` PS-28.

**Confidence:** MEDIUM (facts MS; framing INF).

---

#### AP-D-020 — UI automation where a stable interface exists or can be built

**Description.** Robotic UI automation is selected for a target that already exposes a programmatic interface, or for which one could be built within the target's remaining lifetime.

**Classification:** ANTI-PATTERN · **Origin:** MS (the stability preference) + MEDIUM (the cost extension)

**Trigger conditions.** A stable API exists on the target and is reachable; or the target's remaining lifetime and volume would justify building one; or unattended UI automation is proposed at scale as the steady-state integration mechanism.

**Why it fails.** UI automation binds to a contract the target's owner never committed to keeping stable: *"APIs are meant to be stable even as the application changes over time"*, against UI automation's susceptibility *"to breaking when things change"*. The cost and operability profile compounds it: a bounded run queue (500 runs, 12-hour maximum wait, 24-hour maximum run); dispatch adding up to 50 seconds per run, which *"can make parallel runs look sequential"*; only the **first 10,000 actions of a run are logged** — *"Extra actions are performed but aren't logged"*, i.e. unobserved execution; one licence per simultaneous unattended process, with unattended runs costing a multiple of cloud runs; a Premium *user* still required to register the machine; host sizing of 4+ cores plus 2 cores and 4 GB per additional session; and regional unavailability in several sovereign clouds. Microsoft's positioning is explicitly exceptional: *"Use desktop flows on the rare occasions when the connectors don't meet your requirements or for a one-time screen scraping need."*

**Consequences.** *Operations:* fragile automation that breaks on the target's release cycle, partly unobserved. *Cost:* per-concurrent-bot licensing plus host infrastructure; the multiplier belongs in the API-versus-RPA decision. *Business:* an automation whose failures are silent beyond the logging ceiling.

**Detection signals.** An API on the target that nobody has costed · UI automation proposed as the permanent mechanism · concurrency requirements implying several bots · the target on an active release cycle · no owner for selector maintenance.

**Decision impact.** Prefer the programmatic interface. UI automation is justified only where **all** hold: no programmatic access exists, the target's remaining lifetime does not justify building one, and the volume fits the queue model. Otherwise the decision is to build or buy the interface — which may itself move the integration out of the platform.

**Better alternatives.** The target's own API; an API built over the legacy target (the anti-corruption/facade shape); the vendor's supported integration mechanism; process change removing the interaction; retiring the target.

**Exceptions.** Genuinely no programmatic access, short remaining lifetime, bounded volume, attended use with a human present — the documented sweet spot. Note the corpus records **no Microsoft statement acknowledging UI fragility as inherent** (`automation-architecture.md` U-07), so the fragility framing must not be presented as Microsoft's admission.

**Evidence.** `automation-architecture.md` AT2-37, AT2-38, AT2-39, AT2-40, AT2-63, N-43…N-50, U-07, §3.A rows 6–7; `platform-suitability.md` PS-21; `architecture-patterns.md` §8 item 21 (Q-26); `licensing-cost.md` LC-08, LC-17, `licensing-cost.md` DC-09.

**Confidence:** MEDIUM.

---

#### AP-D-021 — Automation with no observability and no throttling owner

**Description.** Business-relevant automation runs with no monitored throttling metric, no failure alerting to a shared destination, and no named owner — so degradation is invisible until the platform disables it.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Business-relevant automation plus any of: no monitored throttling rate; failure notifications to an individual mailbox; no named owner; observability requirements assumed to be met by default; audit or diagnostic evidence needed beyond the native retention window.

**Why it fails.** The failure mode is **not an error**. Sustained overload means *"flow activity slows. It automatically resumes when the sliding window has activity below the limit. However, if a cloud flow consistently remains above the limits for 14 days, the system turns it off"* — and *"if you update your flow, it resets the limits"*, so the ordinary remediation destroys the evidence. Additional silent terminations exist: continuously failing automation after 14 days, and low-frequency automation owned by non-premium identities after 90 days of inactivity. Nothing is monitored by default: telemetry export requires a managed environment, is *"not 100% lossless"*, and is unavailable in sovereign clouds; the aggregated monitoring surface is daily-aggregated with short log retention and percentile-only metrics; the compliance log has ~24-hour latency and Microsoft says *"Don't use this information for real-time monitoring"*; and native run history — the *only* transactional record — expires at 30 days. There is *no default owner, no default alert and no default runbook*, and suspension notices go to individual mailboxes, including a leaver's.

**Consequences.** *Business:* the process stops without a decision. *Operations:* no evidence to diagnose with, and the standard fix erases what there was. *Data:* work silently not done, discovered downstream. *Cost:* throttling remediation is commercial, so the unmonitored case is also an unbudgeted one.

**Detection signals.** No named owner · alerts to a personal mailbox · no throttling metric in the operational model · "users will tell us" · evidence requirement beyond 30 days with no export design · managed-environment features assumed but not licensed.

**Decision impact. Observability depth is a licensing and environment decision taken during option selection, not an operational afterthought** — because the export mechanism is gated behind a managed environment and therefore behind premium licences for that environment's users. If those are out of scope, diagnostic capability is materially reduced and **the support model must say so**. Where evidence must survive beyond the native window, it must be written to a **business record as part of the process** — a functional requirement on the design.

**Better alternatives.** Named business, application and platform owners; alerts to a shared destination with pre-granted read access for whoever is on call; a monitored throttling metric with a threshold; telemetry export where the criticality justifies the licence; evidence written into business records for long retention; correlation identifiers across service boundaries for the enterprise class.

**Exceptions.** Genuinely departmental automation with a short life, a tolerant process and users who *are* the monitoring — the corpus calls this *"a legitimate class"* and warns that over-engineering it is a real cost (→ AP-D-039).

**Evidence.** `automation-architecture.md` AT2-10, AT2-42, AT2-44, AT2-61, N-01, N-02, N-10, N-11, §9 rows 16–17; `operations-support.md` OP-04, OP-05, OP-08, OP-09, OP-10, OP-11, OP-AP-01…OP-AP-05, OP-AP-20, `operations-support.md` DC-01, DC-02, DC-03; `performance-scale.md` §8.1 items 18, 24, 25, §11.2; `licensing-cost.md` LC-23, LC-AP-10, §7.2 item 46; `integration-architecture.md` X-18, §12.6.

**Confidence:** HIGH.

---

### 5.4 Integration

#### AP-D-022 — Point-to-point proliferation

**Description.** Integrations are added one system pair at a time, each with its own pipeline, credentials, transformation and error handling, until the estate has no describable topology.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Integration count growing without a topology decision; the same transformation or business rule implemented in more than one place; the same backend reached by three or more artefacts, each directly; no inventory of streams.

**Why it fails.** Microsoft names the end state and does not flatter it: *"This pattern results in a service-oriented architecture—sometimes humorously called 'spaghetti architecture'"*, paired with *"Avoid creating tightly coupled point-to-point…"*. The mechanical driver is that the trigger for centralising is **two consumers** of the same capability — *"centralizing the logic where it could be used by other applications in the organization"* — so every direct integration past the second is duplicated work. Duplication then produces divergence: the same mapping in an automation, in server-side code and in a report drifts, and each copy must be found when the contract changes. Contract change is itself expensive per consumer: a connector schema change *"requires republishing and removing/re-adding the connection in every consuming app."*

**Consequences.** *Architecture:* no topology, so no change can be assessed. *Delivery:* linear-to-quadratic growth in change cost. *Governance:* credentials and endpoints spread across artefacts with no inventory. *Data:* divergent transformations producing inconsistent results from the same source.

**Detection signals.** Stream count without an inventory · the same mapping in several artefacts · ≥ 2 consumers of one backend reached directly · connector credentials held per artefact · a change to one system requiring an unknown number of artefact updates.

**Decision impact.** Once a capability has two or more consumer classes, the decision is mediation — but **only for that capability**, and only if a mediation requirement (reuse, versioning, rate limiting, composition, caching, observability, translation, discovery) actually applies. Where an enterprise boundary already exists, the decision is to consume it (→ AP-D-027). The symmetric error is buying mediation with one consumer (→ AP-D-023).

**Better alternatives.** API-mediated access for shared capabilities; a broker for decoupling; the existing enterprise boundary; per-stream decisions rather than per-system-pair (→ AP-D-028); modular automation with a documented stream inventory.

**Exceptions.** A genuinely small, stable estate: one consumer per capability, stable contracts, volumes inside the throttles. Microsoft's guidance is that this *"is the correct answer far more often than architects trained on enterprise integration expect"* (`integration-architecture.md` §2.2 step 6).

**Evidence.** `integration-architecture.md` X-01, X-02, X-03, X-13, I-02, I-07, I-31, IA-49, §2.2, §4.1, §4.2; `architecture-patterns.md` AP-01, AP-02, matrix rows 1–3, §8 item 22, §6.2; `alm-devops.md` ALM-14, §14.1.

**Confidence:** HIGH.

---

#### AP-D-023 — Mediation layer with no requirement behind it

**Description.** An API gateway, facade or broker is inserted where one consumer calls one backend over a stable contract at volume inside the throttle — adding a hop, a bill, a deployment unit and an owner with no requirement behind any of them.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A mediation component whose justification is not one of the documented triggers (≥ 2 consumer classes, composition across backends, contract versioning, rate limiting to protect the backend, end-to-end tracing across a fan-out, server-side caching, semantic translation from a hostile contract, private-network reach with credential isolation, consumption governance/discovery). Special cases: wrapping an already-managed enterprise API in a second managed API; a gateway that only forwards; a gateway expected to absorb a spike.

**Why it fails.** Microsoft's instruction is *"Choose the simplest approach that fulfills requirements"*, and a forwarding gateway has documented costs with no offsetting benefit: *"The gateway service might introduce a single point of failure (SPoF)"* and *"The gateway might introduce a bottleneck."* A gateway is not a buffer — expecting it to absorb a spike is a distinct error, since under load it is the bottleneck. Aggregation inside the gateway is separately warned against: *"Rather than build aggregation into the gateway, consider placing an aggregation service behind the gateway."* And wrapping a managed API duplicates contract management rather than reducing it.

**Consequences.** *Architecture:* availability reduced by a component that adds no property. *Cost:* a tier, a bill and a team. *Operations:* one more thing on the critical path to monitor and patch. *Delivery:* lead time for changes that need no mediation.

**Detection signals.** One consumer, one backend, stable contract, volume inside throttle · the mediation component has no policy, transformation, cache or aggregation · the backend is already an enterprise-managed API · the stated purpose is "best practice" · spike absorption cited as the reason.

**Decision impact.** Remove the layer, or name the requirement. Where the requirement is spike absorption, the answer is a broker, not a gateway; where it is reuse, the trigger is a real second consumer, not an anticipated one. The corpus's discipline: *"the FINAL TEST for this area is deliberately 'Which architectural structure best satisfies these requirements?' — not 'Which Microsoft reference architecture looks similar?'"*

**Better alternatives.** Direct integration under its seven conditions; a broker for spikes and guarantees; a connector generated from the existing API's definition; connector-level trigger conditions and filters for busy sources.

**Exceptions.** Any one of the documented triggers genuinely applies — then it is the API-mediated pattern, correctly selected. A dated growth forecast crossing a trigger inside the horizon also qualifies, recorded as the justification.

**Evidence.** `integration-architecture.md` X-11, X-12, I-01, I-20, I-31, §4.2 (both directions); `architecture-patterns.md` Y-02, Y-04, AP-02, AP-08, §8 items 3, 12, matrix rows 1, 6, APR-U-09; `automation-architecture.md` §4.1; `licensing-cost.md` §6.

**Confidence:** HIGH.

---

#### AP-D-024 — Polling below the mechanism's own freshness floor

**Description.** A freshness or latency requirement tighter than the polling mechanism's floor is answered by polling more often — treating a mechanism limit as a tuning parameter.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A stated freshness requirement below the scheduling floor (60 seconds) or below the relevant connector's own poll interval; polling a busy source with no trigger-side predicate; polling used where the source publishes events.

**Why it fails.** The floor is structural: minimum scheduled recurrence is 60 seconds, per-trigger latency is a **per-connector property with no published aggregate**, and *"Instant triggers aren't truly instant."* Below the floor it is *"not a tuning problem"* — it is a mechanism problem requiring event/webhook push, a broker, or a synchronous call. Polling also consumes entitlement on every empty check: *"Even when a flow makes few Power Platform requests, it can still reach the limits if it runs more frequently than you expect."* The documented mitigation is a **trigger-side** predicate, not in-flow filtering. Crucially, the corpus keeps this a *conditional* anti-pattern: switching to a webhook is **not a pure win**, because the two trigger types are *"unsafe across an outage, in opposite directions"* — polling replays a backlog on resume, push silently loses events. And the current per-licence polling intervals are `UNKNOWN` across three areas (`performance-scale.md` PF-U-08, `automation-architecture.md` U-02, `data-architecture.md` U-20, C-10), so the floor cannot be quoted numerically per connector.

**Consequences.** *Business:* a freshness promise that cannot be met by the chosen mechanism. *Cost:* entitlement consumed on empty polls; a documented cost driver. *Data:* stale reads presented as current. *Operations:* either backlog floods or silent loss at the trigger boundary, depending on which mechanism was chosen.

**Detection signals.** A freshness number below a minute · "real-time" without a figure · polling frequency increased in response to complaints · no trigger condition on a busy source · the upstream source itself batch-loaded (the "false freshness" case).

**Decision impact.** Trace the freshness requirement to the **original** source's cadence, not to the nearest mechanism. Where it is tighter than the floor, the decision is a different mechanism — event/push, broker, or synchronous call — and, if none is available, the requirement must change. Always add a trigger-side predicate on a busy source, and state the outage behaviour of the trigger type chosen.

**Better alternatives.** Source-published events; a broker with push delivery; a synchronous call at read time; server-side computation inside the user's own transaction where immediacy matters; renegotiating freshness against the upstream cadence.

**Exceptions.** Freshness requirements comfortably above the floor with a trigger predicate in place — polling is then the simpler, cheaper and *more outage-tolerant* choice, which is why the corpus classes this as conditional.

**Evidence.** `automation-architecture.md` AT2-11, AT2-22, AT2-60, N-08, §4.3, U-02; `integration-architecture.md` X-04, X-05, I-02, I-22, I-32, §2.1 rows 2, 5, §8 ("false freshness"); `performance-scale.md` PF-32, PF-AP-08, B-07, PF-U-08, DC-06; `data-architecture.md` DA-47, DA-49, DA-51, C-10, C-11, U-20; `platform-suitability.md` PS-56.

**Confidence:** HIGH (the floor and the trade-off are MS; per-connector intervals remain UNKNOWN).

---

#### AP-D-025 — Integration seam without contract lifecycle ownership

**Description.** A custom connector or bespoke integration seam is created without anyone owning the backend contract's versioning, deprecation and release coordination.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A custom connector or bespoke seam plus any of: no named owner of the backend API; no versioning policy; no coordinated release order between the connector, the consuming solution and the backend; the backend contract expected to change; the seam on a business-critical path.

**Why it fails.** The seam is a **versioned contract crossing an organisational boundary**, and its change cost is documented and manual: a schema change *"requires republishing and removing/re-adding the connection in every consuming app"*; the connector must live in a separate solution with an explicit import order; canvas apps *"don't recognise connection references"*, and the documented workaround *"can create an unmanaged layer"* — which **directly conflicts with a production policy that blocks unmanaged customizations**. The corpus's rule is emphatic: *"if that workaround is required, do not silently disable the integrity control"* — redesign, use another supported binding, or record a governance exception with owner and expiry. Two more constraints bind the seam itself: no client-credentials grant type, definition files under 1 MB, OpenAPI 2.0 only, and a **connector count capped at one** on several common licence plans. And the throughput figure is `CONFLICTED` (see AP-D-051).

**Consequences.** *Delivery:* an unplanned, manual change across every consumer on each contract change. *ALM:* an unmanaged layer in production, or a disabled integrity control. *Operations:* a break with no owner on either side. *Cost:* certification lead time (*"three to five business days… another 7 to 10 business days"*) if the seam must be certified, and premium-only classification.

**Detection signals.** A custom connector with no named API owner · no versioning statement · consumers not enumerated · a canvas consumer plus a mandatory unmanaged-customizations block · the backend owned by a third party or another team.

**Decision impact. Treat the connector and the backend API contract as one release boundary.** The decision is whether an owner exists on both sides; where none does, the seam is not available for a business-critical path and the option must change — mediate behind an owned API, consume an existing enterprise contract, or keep the interaction where the contract already has an owner.

**Better alternatives.** An enterprise-owned API contract consumed as a connector generated from its definition; API-mediated access with versioning; the existing boundary; a standard connector where one satisfies the requirement.

**Exceptions.** A stable, internally-owned contract with a single consumer, an accepted republish-and-reconnect cost per change, and no unmanaged-layer conflict — the documented conditions under which the direct seam is fine.

**Evidence.** `integration-architecture.md` I-07, I-08, I-13, IA-49, §3 (custom connector row), §7 item 4, §9 row 8, C-01, C-02, U-02; `alm-devops.md` ALM-14, criterion 8/8a, §14.1; `architecture-patterns.md` Q-37, §13 (high-frequency custom-connector row); `platform-suitability.md` PS-26; manifest NB-02.

**Confidence:** HIGH.

---

#### AP-D-026 — External component adopted without an operator

**Description.** A hybrid or external component — broker, gateway host, worker, API tier, integration platform — is introduced into the architecture without a named team that owns its RBAC, policy baseline, pipeline, monitoring, cost, backup position and on-call.

**Classification:** **GATE** (reclassified 2026-09-03 — where it holds, the option is *unavailable*, not worse; see §2) · **Origin:** MS (the obligations) + INF (the unavailability conclusion)

**Trigger conditions.** An external component is in the design and any of the following is unnamed: owning team; inventory/tagging; RBAC and privileged-access model; policy/security baseline; cost owner; CI/CD or infrastructure-as-code owner; monitoring and alert ownership; backup/DR position; cross-platform incident runbook.

**Why it fails.** External resources are **not governed by the platform's own controls** — their identities, RBAC, network exposure, secret management, policy baseline and diagnostic access must be designed in the other domain (`security.md` SEC-XB-02, `governance.md` GOV-XB-01). The hybrid split imports *"two ALM models, two RBAC models, two monitoring surfaces, two retention windows"* and is *"a cost and skills commitment well beyond a Power Platform app"*. Correlation across the boundary exists **only if the design propagates an explicit identifier** — no platform-provided cross-boundary correlation is documented. And "move it to Azure for security" is explicitly incomplete unless the other side has a security baseline. The corpus's conclusion is a hard one: patterns involving external components *"are not production-ready"* until the listed roles exist, and where there is no operator the pattern is **unavailable, not merely expensive** (`architecture-patterns.md` Y-13, §13).

**Consequences.** *Operations:* an unmonitored, unpatched component on the critical path; incidents that span two unconnected surfaces with no shared correlation id. *Security:* a second, ungoverned enforcement plane. *Cost:* consumption in another billing domain with no owner. *ALM:* one side deployed without the other (→ AP-D-046).

**Detection signals.** An external component with no named team · no second pipeline in the delivery plan · no cross-platform runbook · no correlation-id design · "the platform team will look after it" without that team's agreement · no cost owner in the other domain.

**Decision impact.** The presence of a named operator is a **gating condition** on the hybrid and boundary patterns. Where it is absent, the decision is: acquire the capability (with its cost and lead time in the option), keep the whole requirement in one platform and accept the resulting constraint with a tripwire, or select a different architecture. What is *not* available is a paper hybrid — *"single platform + a tripwire, not a paper hybrid"* (`automation-architecture.md` §9 row 22).

**Better alternatives.** Consume an existing enterprise capability that already has an operator (→ AP-D-027); keep the requirement in-platform with the constraint documented; a managed service that reduces the operating surface; a delivery partner with a dated handover plan — noting that operational handover from partner to customer is *"the commonest real-world failure point for partner-delivered solutions, and entirely undocumented"* (`operations-support.md` OP-U-07).

**Exceptions.** None as such — but the *scale* of the obligation varies with criticality. A departmental workload's external component still needs an owner; it does not need 24×7 on-call.

**Evidence.** `architecture-patterns.md` Y-13, §13 (2nd composed disqualifier), AP-05, AP-10 (Governance/Operational implications), §5.1; `automation-architecture.md` AT2-53, N-51, N-52, N-53, §6.4, §9 row 22; `governance.md` GOV-XB-01, GOV-XB-03; `security.md` SEC-XB-02; `alm-devops.md` §14.2; `operations-support.md` §13.1, OP-U-07; `licensing-cost.md` §6 (external estate row); `integration-architecture.md` §7 items 28–30, IA-27, IA-29.

**Confidence:** MEDIUM (obligations MS; "unavailable" is INF).

---

#### AP-D-027 — Existing integration ownership bypassed

**Description.** The organisation already owns an integration capability — an enterprise service bus, integration platform, API gateway or message backbone — with a published contract and an owning team, and the project builds its own path to the same system anyway.

**Classification:** ANTI-PATTERN · **Origin:** INF over MS mechanism evidence

**Trigger conditions.** An enterprise integration capability exists; the target system is already integrated with it or in scope for it; the project's design reaches the system directly, or stands up a parallel mediation tier beside it.

**Why it fails.** The corpus is candid that **nothing in the vendor's material tells an architect to check this** — *"which is precisely why it must be step 1 of the classification test"* — and the consequences of skipping it are exactly the anti-patterns above: point-to-point proliferation, duplicated contract management, and split ownership of the same system's access. `governance.md` GOV-XB-02 frames it as a **governance decision before a product decision**: a project-local mediation stack *"duplicates governance and creates split ownership."* The specific version where the enterprise's platform is another vendor's and a parallel one is stood up beside it is named directly (`architecture-patterns.md` Y-12) — and this is what makes the corpus's boundary pattern *"the only pattern that can be satisfied by a non-Microsoft platform… the corpus's antidote to 'Azure is automatically the answer'."*

**Consequences.** *Governance:* two boundaries, two contracts, two audit trails for one system. *Cost:* a second platform funded alongside one already paid for. *Operations:* two owners for one integration path, and no single place to see message history. *Security:* a second, differently-governed access path to the same system.

**Detection signals.** An existing integration platform in the estate · the target system already integrated elsewhere · a project-local mediation tier proposed · no consultation with the platform-owning team · the phrase "it was quicker to go direct".

**Decision impact.** Make this **step 1**: ask whether the integration responsibility is already owned, with a published contract. If yes, the platform consumes the contract and integrates nothing — the transformation, the contract and the audit trail stay with the owner. Reuse is not automatic: an incumbent that **cannot meet** the stated protocol, security, reliability, latency or ownership requirements remains unsuitable, and that finding must be recorded per requirement rather than asserted.

**Better alternatives.** Consume the published contract, ideally as a connector generated from its definition; negotiate an extension to the enterprise contract; where the incumbent genuinely fails a requirement, document which one and escalate the boundary decision jointly.

**Exceptions.** The incumbent demonstrably fails a stated requirement; or the incumbent is on a dated decommissioning plan; or the boundary team's lead time is incompatible with a genuine business deadline — the last recorded as an accepted governance exception with an owner and an expiry, not as an architecture.

**Evidence.** `integration-architecture.md` §12.1, §2.2 step 1, §9 row 23, I-20, I-23; `governance.md` GOV-XB-02, GOV-A11; `architecture-patterns.md` Y-12, AP-10, matrix rows 29–30, §3.1 (last variable), APR-U-08; `automation-architecture.md` AT2-52, §4.3 (existing engine), §3.B row 19; manifest NB-06.

**Confidence:** MEDIUM (the priority ordering is INF; the corpus flags AP-10 as its weakest-evidenced pattern per NB-06).

---

#### AP-D-028 — One integration decision per system pair instead of per stream

**Description.** The engagement decides "how we integrate with system X" once, and applies that single mechanism to every interaction with it — masters, transactions, documents, events, reporting.

**Classification:** ANTI-PATTERN · **Origin:** MS (the worked counter-example) + INF (the framing)

**Trigger conditions.** A single mechanism assigned to a system pair; interactions of visibly different shape (reference reads, transactional writes, bulk extracts, event notifications) sharing one pipeline; no stream inventory.

**Why it fails.** The requirement dimensions that decide a mechanism — volume, frequency, directionality, latency, guarantee, ownership, consistency — vary **per stream**, not per system. Microsoft's own worked example decomposes one integration goal into four streams and gives them **different** treatments; another documented design deliberately uses three mechanisms for one system pairing (virtual reads, a narrow write path, and a separate API for the rest). The corpus states the rule directly: *"Decide per stream; per-stream heterogeneity is expected"* — and notes that the same total volume with a different distribution *"changes the solution design. Don't assume one solution fits both."* Forcing one mechanism means every stream inherits the worst constraints of the mechanism chosen for the hardest one, or the weakest guarantees of the one chosen for the easiest.

**Consequences.** *Architecture:* over-engineered reference reads and under-engineered critical writes, simultaneously. *Cost:* mediation or brokerage paid for streams that never needed it. *Data:* guarantees absent exactly where they mattered. *Delivery:* one pipeline becoming a monolith that every change must pass through (`integration-architecture.md` X-02).

**Detection signals.** "We integrate with X via Y" as a whole-system statement · no stream inventory · one pipeline serving reads, writes and extracts · one mechanism decision recorded for a system with several interaction shapes.

**Decision impact.** Produce a **stream inventory** and decide per stream. This changes the shape of the option set: a single system pairing may legitimately produce two or three patterns, and that heterogeneity is the expected output rather than a sign of indiscipline.

**Better alternatives.** Per-stream classification using the ordered topology test; documented compositions (read-through for reference plus replication for the subset needing platform features; events for notification plus a queue for the guarantee).

**Exceptions.** A genuinely single-stream relationship. And a deliberate standardisation on one mechanism to reduce operating surface — priced, and with the streams that suffer named.

**Evidence.** `integration-architecture.md` I-01, I-02, X-02, X-03, §2.1, §2.2, §9; `architecture-patterns.md` Y-14, §6.1 (compositions), Q-20; `data-architecture.md` §2 rows 13–17, §6.

**Confidence:** MEDIUM.

---
### 5.5 Security

#### AP-D-029 — Authorization model deferred past an irreversible decision

**Description.** The data model is built first and access control is designed afterwards — after decisions that cannot be reversed without rebuilding and migrating.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Tables created before the access model exists; row-scoping needs unclear at modelling time; an organisational-unit hierarchy assumed from the current org chart; a matrix organisation with no expression of it in the model; "we'll add security later" as an accepted plan.

**Why it fails.** Three documented irreversibilities. (1) **Table ownership type is immutable after creation** — changing it means rebuild plus migration, so "row-level visibility that may *ever* be needed" is a decision per table *before build*. (2) **Privileges are additive and cannot be subtracted**: row access is the sum of role depth + business unit + team membership + shares, and a broad grant made "to unblock the project" *cannot be walked back*. (3) The classic unit hierarchy cannot express a matrix organisation without owner-team workarounds; the modernised alternative is a **migration programme** (impact analysis, RACI per unit, forms updated to carry the owning unit) with a one-way-ish switch. Two more late-discovery traps: column-level security **never applies to the system administrator** and cannot secure lookups, formula, primary-name or system columns, and leaks through calculated and composite columns — so "confidential even from administrators" is *not achievable* in that store and must be designed out, not configured in; and per-record sharing at scale writes access rows that grow on the database meter and sit on the access hot path, which is why sharing is documented as an *exception*, not a model.

**Consequences.** *Security:* a confidentiality requirement that cannot be met by the built model. *Data:* rebuild-and-migrate to fix a modelling decision. *Cost:* access-row growth on the most expensive meter; unbudgeted remodelling. *Performance:* an authorization-heavy model whose cost is `UNKNOWN` — manifest **NB-04 / `PF-U-07`** states there is *no universal numeric curve* for unit depth, team/share cardinality or column-security complexity versus runtime performance, so the only answer is a representative pilot.

**Detection signals.** Any confidentiality statement at row or column level · a matrix or frequently re-organising structure · "administrators must not see it" · sharing described as the access mechanism · tables already created with no access model · a re-organisation expected inside the solution's life.

**Decision impact. Design the ownership and unit model before the first table is created.** Where administrator-exclusion is required, the attribute must live outside that store or the administrator population must be reduced to an auditable, just-in-time set — an architecture decision, not a setting. Where the model will be authorization-heavy, sign-off requires a bounded pilot at target complexity (NB-04); a numeric threshold must not be invented (→ AP-D-051).

**Better alternatives.** Ownership decisions per table up front; group-driven role assignment via directory groups rather than direct assignment; teams and unit hierarchy before sharing; a separate table for the sensitive attribute; keeping the attribute in a system that can enforce the requirement; `alternatives.md` ALT-005/ALT-007 where administrator-exclusion is absolute.

**Exceptions.** Organisation-wide, non-segmented data with no plausible future segmentation — but the corpus's own anti-pattern is exactly assuming this (`data-architecture.md` DAP-11), so the exception needs a stated reason, not a default.

**Evidence.** `security.md` SEC-08, SEC-09, SEC-10, SEC-13, SEC-A4, SEC-A5, SEC-A6, §2, §4 rows 1–6, SEC-XB-03, SEC-U-01; `data-architecture.md` DA-11, DA-12, DAP-10, DAP-11, DAP-12, §2 row 5, §3; `performance-scale.md` PF-U-07; manifest NB-04.

**Confidence:** HIGH.

---

#### AP-D-030 — Application UI treated as the authorization layer

**Description.** Access control is implemented by hiding controls, screens or navigation, on the assumption that what a user cannot see they cannot reach.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Role-based behaviour implemented in UI visibility expressions; a data source the application filters but the store does not restrict; a shared or implicit connection under the application; per-user authorization required at the backend.

**Why it fails.** Access is governed by the **connection identity and the source's own security**, not by the interface. The corpus's rule from the enforcement-plane model is direct: *"a requirement satisfied only in plane 5 (the app) is not enforced at all against a user who has plane-4 credentials."* Application-side filters *"never override"* store permissions, and Microsoft's own worked counter-example is a salary column hidden in the app but readable through the connection. With **implicit** authentication the maker's credentials govern for every user; with explicit authentication the user's own rights govern — which is why sensitive sources require explicit identity. A related exposure: preloading application assets for speed places compiled app content, including authored text and the environment URL, on **unauthenticated endpoints**.

**Consequences.** *Security:* data reachable by anyone with the app's credentials or the source's endpoint. *Compliance:* an access-control claim that cannot be evidenced. *Architecture:* the store choice is wrong — if the source cannot express the requirement, no app-side work fixes it.

**Detection signals.** Visibility expressions cited as the access control · a store with no row/column security under a segmented requirement · implicit/shared connections on sensitive data · "only managers see the manager screen" with no store-side rule.

**Decision impact.** Enforce on the **lowest plane that can enforce it**. If the chosen store cannot express the requirement, the store decision changes — to a store that can, or to keeping the data where it is already enforced. Note the residual: the corpus records `SEC-U-A5`/`U-A5` — no located verbatim statement that hiding controls is not security — so the framing is partly INF, anchored via the connection-identity fact.

**Better alternatives.** Store-level row and column security; explicit (delegated) identity so the backend authorizes per user; keeping enforcement in the owning system; API-mediated access that propagates identity.

**Exceptions.** UI tailoring for usability, layered **on top of** enforced authorization — legitimate and desirable. The anti-pattern is UI tailoring *instead of* enforcement.

**Evidence.** `security.md` SEC-18, SEC-A1, §1 (five planes and the derived rule), §4 row 1; `application-architecture.md` AA-10, AP-29, U-A5; `data-architecture.md` DA-33, DAP-18, §2 row 5; `platform-suitability.md` PS-31, AP-6; `performance-scale.md` §8.1 item 43.

**Confidence:** HIGH.

---

#### AP-D-031 — Secrets held in makers' assets

**Description.** API keys, connection strings, certificates or passwords are placed in application formulas, automation action inputs or connector definitions.

**Classification:** **CONSTRAINT** (reclassified 2026-09-03 — always wrong within its scope; see §2) · **Origin:** MS

**Trigger conditions.** Any secret required by a component; a "no secrets in the solution" policy; a secret needed by a component type the sanctioned mechanism does not serve.

**Why it fails.** There is a sanctioned path — vault-backed secret variables — but it is **consumable by only three component types** (cloud flows, agents, custom connectors), and *"the secrets aren't available for use in other customizations or generally via the API"*. So canvas apps and other surfaces have **no sanctioned mechanism**, which is precisely why the anti-pattern appears. Where the secret does land in an action input it becomes **readable from run history**, at read volumes up to 60,000 calls per five minutes on higher profiles. Managed identity — the mechanism that removes the secret entirely — covers **only server-side platform code**, not connectors, flows or apps.

**Consequences.** *Security:* credential disclosure to anyone with run-history or maker access. *Compliance:* a secrets-management control that is documented but unimplementable for part of the design. *Operations:* rotation becomes a manual hunt across artefacts.

**Detection signals.** A secret required by a surface outside the three supported component types · secrets visible in run history · a "no stored secrets" requirement in the security schedule · certificate or key expiry with no owner.

**Decision impact.** The requirement "no secrets in the solution" **selects the component type**. Secret-dependent logic must move to a flow, a custom connector, or server-side code with managed identity. Where the requirement is absolute and the surface cannot comply, the decision moves out of the platform for that leg (`architecture-patterns.md` matrix row 26: the STRONG answers are the worker or the server-side-code variants).

**Better alternatives.** Vault-backed secret variables for the supported component types; server-side platform code with managed identity; a mediated API holding the credential outside the platform; the documented reference shape of connector plus directory-protected backend plus vault-sourced client credentials.

**Exceptions.** None for production secrets. Non-secret configuration belongs in environment variables and is a different thing.

**Evidence.** `security.md` SEC-06, SEC-07, SEC-A10, §2, §4 row 12; `automation-architecture.md` AT2-49, AT2-50, N-14, §9 row 18; `integration-architecture.md` IA-31, IA-32, I-27, I-36, §7 items 22–23; `architecture-patterns.md` matrix row 26; `alm-devops.md` ALM-13.

**Confidence:** HIGH.

---

#### AP-D-032 — Shared identity as the access or integration model

**Description.** A shared account, generic "service account", or an implicitly shared connection is the identity through which users or integrations reach data — often to reduce licence count or to simplify setup.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A shared or generic account in the design; implicit/shared connections on sensitive sources; integrations running as a personal account; a shared identity introduced to avoid per-user licensing; no lifecycle owner for a privileged service identity.

**Why it fails.** Four mechanisms. (1) **Auditability collapses** — the audit record captures the acting identity, so a shared identity destroys attribution. (2) **Licence multiplexing is prohibited**, so the cost motive is not merely risky but a contractual violation, and the corpus records that entitlement breaches carry a documented **right of suspension**. (3) **Throughput collapses onto one budget** — service protection is *per identity*, so *"one account is one budget regardless of user count"*; the same mechanism makes public/anonymous surfaces a concentrated-identity problem. (4) **Automation identity is fragile** — automation runs with the connection owner's permissions by default and invisibly (*"All users of the flow use embedded connections"*), reverts to the lowest performance profile if that owner leaves, and a non-solution artefact's owner *cannot be changed at all*. Related: relational-store row-level security based on the session's user name **collapses to one principal** behind a shared connection — the reference architecture states that a shareable service identity means *"all users have the same database access rights."*

**Consequences.** *Security:* no attribution; over-broad effective rights. *Performance:* one identity's budget for the whole population. *Cost:* a contractual exposure, plus the throughput remedy being commercial. *Operations:* automation that dies when a person leaves, with a 30-day warning to their mailbox.

**Detection signals.** A generic account name in the design · implicit connections on sensitive sources · integrations owned by a named individual · licence-count arithmetic that implies sharing · no owner for the service identity's credentials and rotation.

**Decision impact.** Service principals with per-purpose scope, designed in rather than retrofitted; per-user identity wherever the backend must authorize per user; and the licence census done on the **real** population, because the sharing workaround is not available. For business-critical automation, ownership by a service principal or a capacity-licensed identity is an **architectural** decision (→ AP-D-066).

**Better alternatives.** Service-principal-owned automation and connections; explicit (delegated) authentication for sensitive sources; directory-group-driven role assignment; identity propagation through a mediated API where the backend authorizes per user.

**Exceptions.** A genuine integration identity with a named owner, scoped rights, rotation and audit — that is the recommended pattern, not the anti-pattern. The anti-pattern is the *unowned* or *human-shared* identity.

**Evidence.** `security.md` SEC-19, SEC-21, SEC-22, SEC-A2, SEC-A7, §4 rows 13, 17, SEC-XB-04; `platform-suitability.md` PS-36, PS-42, AP-8, PS-31; `automation-architecture.md` AT2-44, AT2-46, AT2-48, AT2-51, N-12, N-13, N-15; `performance-scale.md` PF-25, B-11, DC-04, DC-18; `data-architecture.md` DA-33, DAP-18, DAP-38, SQ2-08, SQ2-15; `licensing-cost.md` LC-02, §7.1 item 3, §7.2 items 40–42; `operations-support.md` OP-04, OP-17, `operations-support.md` DC-12.

**Confidence:** HIGH.

---

#### AP-D-033 — One control treated as the whole control

**Description.** A single mechanism — environment separation, or a connector data policy, or tenant isolation — is presented as satisfying a security requirement it only partially addresses.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** "It's in a separate environment, so it's isolated"; "DLP prevents exfiltration"; "tenant isolation stops data leaving"; a control assumed to be enforcing when it is in audit-only mode or preview.

**Why it fails.** Each control has a documented scope that is narrower than the claim. **Environment**: it *is* the isolation boundary and cross-environment data access is not supported — but security groups **do not apply to default or developer environments**, and platform administrators and application users **bypass the group**; membership plus a data-layer role are *both* required and neither is implied by a licence. **Data policies**: Microsoft scopes them to reducing *"the risk of users **unintentionally** exposing organizational data"* — guardrails, not an exfiltration control; independent evidence describes deliberate cross-environment bypass through a ubiquitous connector (T4, so a signal requiring validation, not authority); the default state is permissive (*"By default, no data policies are implemented in the tenant"*); the newer allowlist mechanism currently covers **certified connectors only** and does not cover custom or HTTP connectors; endpoint filtering is preview, covers a handful of connectors, and is **not enforced for environment variables, custom inputs or runtime-computed endpoints**. **Tenant isolation**: covers directory-authenticated connectors only, has a documented gap, and takes about an hour to propagate. **Network controls**: the firewall control protects one data service only, defaults to **audit-only mode**, and by default still allows *all* application users and trusted services.

**Consequences.** *Security:* a control claimed and not delivered. *Compliance:* assurance built on a mechanism outside its stated scope. *Operations:* a policy change that **suspends or quarantines running applications**, with up to 24 hours of enforcement lag — a governance action presenting as an integration outage.

**Detection signals.** A single mechanism named as the answer to a security requirement · audit-only mode left on · custom or HTTP connectors in scope of an allowlist-based claim · a control in preview cited in an assurance document · no layered posture described.

**Decision impact.** Build a **layered posture** and state each layer's scope: allowlist for what it covers, classic policy for the custom/HTTP gap, target-side controls for the rest, plus tenant isolation with its residual accepted. Never design a control whose enforcement depends on a mechanism documented as non-enforcing. Where the requirement is absolute exfiltration prevention, the honest output is that this corpus cannot evidence it — a `DECISION BLOCKED` or a scope change, not a claim.

**Better alternatives.** Layered controls with named scopes; enforcement at the target system; a dedicated environment *plus* a directory group *plus* data-layer roles, with the documented bypass exceptions listed; identity-side controls for revocation immediacy.

**Exceptions.** Using each control for what it is documented to do — environment separation for blast radius and residency, data policy for accidental misuse, tenant isolation for cross-tenant connector reach. The anti-pattern is the over-claim.

**Evidence.** `security.md` SEC-04, SEC-05, SEC-15, SEC-16, SEC-17, SEC-23, SEC-24, SEC-25, SEC-26, SEC-27, SEC-A3, SEC-A8, SEC-A9, SEC-A11, SEC-C2, §2, §4 rows 2, 3, 9, 14, 15; `governance.md` GOV-10, GOV-11b, GOV-A4, GOV-A5, GOV-C3, §4 rows 5–6; `platform-suitability.md` PS-29; `integration-architecture.md` §7 item 27, X-18, §9 row 28.

**Confidence:** HIGH.

---

#### AP-D-034 — External or anonymous surface exposed with unreviewed permissions

**Description.** A public or externally-authenticated surface is published over sensitive data with broad table permissions, permissive roles, or open self-registration left at its default.

**Classification:** ANTI-PATTERN · **Origin:** T3 (the incident class) + MS (the mechanisms)

**Trigger conditions.** An anonymous or externally-authenticated surface over data with any confidentiality requirement; broad access-type permissions; wildcard field exposure on the data API; open registration left on; no security review before publication; no web application firewall in the operating model.

**Why it fails.** Access is **cumulative across roles**, an anonymous role's table permission means *"visible to anyone"*, the broadest access type means **all rows**, and open registration is **on by default**. Without a table permission there is no access — but a table permission without a role has no effect, so the model is easy to get subtly wrong in both directions. The corpus records this as a **documented mass-exposure incident class** (T3 evidence, corroborated by the vendor's own mechanism documentation and by the existence of daily tenant-level security checks). Certificate and authentication-key expiry are dated obligations with a named-owner requirement, and public/non-production site visibility is governed at tenant level.

**Consequences.** *Security:* mass data exposure — the highest-severity outcome in this file. *Business:* regulatory and reputational consequence. *Governance:* a site whose lifecycle obligations (certificates, keys, visibility) have no owner. *Cost:* consumption-metered external audiences whose forecast was built on people rather than browser cookies (`licensing-cost.md` LC-20).

**Detection signals.** Anonymous access over any table carrying personal or commercial data · broad access types · wildcard field permissions on the data API · registration defaults unreviewed · no pre-publication security review · no named owner for certificates and keys.

**Decision impact.** Treat the external surface as an **internet-facing application**: its own environment, a mandatory table-permission and role review before publication, registration defaults explicitly decided, a firewall and certificate/key lifecycle in the operating model, and a named owner. Where the data's sensitivity and the anonymous requirement cannot be reconciled, the option changes — a custom web surface, or the data does not go there.

**Better alternatives.** Authenticated external access with per-contact scoping; a dedicated environment for the external workload; a read-optimised projection containing only publishable fields; a custom web application where control over caching, headers and the security model is required.

**Exceptions.** Genuinely public content with no confidentiality requirement — the surface's intended use. Note the corpus's residual `U-C7`: the wildcard-risk wording was not verbatim-anchored, so that specific claim is flagged rather than asserted.

**Evidence.** `application-architecture.md` AA-25, AP-26, U-C7, §1 row 4, §2; `security.md` SEC-32, SEC-A13, §4 row 8, SEC-U-08; `platform-suitability.md` PS-36, PS-56, §2 rows 14–15; `governance.md` GOV-23, §4 row 12; `performance-scale.md` PF-21, PF-25, B-11; `licensing-cost.md` LC-12, LC-20, LC-AP-11.

**Confidence:** HIGH on mechanisms; the incident-class framing is T3.

---

#### AP-D-035 — Network and deployment constraints discovered after platform selection

**Description.** A private-connectivity, on-premises-reachability or deployment-location requirement is treated as an infrastructure detail to be handled during implementation, after the platform is chosen.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Any of: "no public endpoints"; an on-premises or private-network target; a customer-hosted or air-gapped deployment mandate; a residency requirement at country level; a sovereign-cloud regime; a target presenting a certificate not chained to a well-known root.

**Why it fails.** These constraints are **platform-selection inputs**, because several of them are absolute and the rest carry preconditions that change the option's cost and topology. Absolutes: disconnected or customer-hosted deployment is **unsupported** — the platform is SaaS only (re-verified 2026-09-03, §6 V-D-01); a custom root certificate authority **cannot** be added to the trusted list; several environment types are excluded from private networking entirely, as is one sovereign-cloud tier. Preconditions with teeth: private egress requires a linked subscription, delegated subnets in **both** regions of a pair (pinning the environment's region), 25–30 production addresses per environment, and a dedicated subnet per policy; enabling it **breaks public calls by design** unless address translation is attached; subnet range and DNS become immutable; identity/token traffic does **not** traverse the private path, so the identity provider must stay publicly reachable; and **the event-publishing mechanism does not support private networking at all**, so "events out to a broker" and "all egress private" cannot both be satisfied through that mechanism. The on-premises alternative is a **customer-operated** estate with 2 MB write and 2 MB/8 MB read payload ceilings, a ≥ 2-node-per-cluster requirement for business-critical use, key custody described as *"a significant business risk"*, and the vendor stating it *"doesn't investigate poor performance when a gateway … is overloaded."* Finally, the controls carry **licence prerequisites across the affected population** (managed environment plus, for some, higher-tier directory/productivity entitlements) — so the security architecture can be economically infeasible rather than merely complex.

**Consequences.** *Architecture:* region pinning and immutable network decisions taken late; a collision between two required capabilities. *Cost:* an unbudgeted licence population (`licensing-cost.md` LC-30). *Delivery:* a dependency on another team's subscription and network. *Operations:* a customer-operated component with an availability profile nobody modelled.

**Detection signals.** A network or residency clause in the requirement or contract · an on-premises target · a self-signed or private certificate authority on the path · a country-level residency requirement · a sovereign-cloud regime · both private egress and platform events required.

**Decision impact.** Evaluate the network and deployment constraint **before** platform selection. Its outcomes are drawn from `decision-criteria.md` §6.2: class 2 **`POWER PLATFORM — FIT WITH CONSTRAINTS`** (private egress with its preconditions costed), class 3 **`POWER PLATFORM + CLOUD-NATIVE HYBRID`** (an in-network component), class 6 **`POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`** followed by class 8 **`CANDIDATE SET — COMPARATIVE FIT UNEVALUATED`**, or class 9 **`DEPLOYMENT MODEL EXCLUDES THIS PLATFORM`** specifically for a customer-hosted or air-gapped mandate, which is the one axis where comparator platforms document a materially different deployment capability (`alternatives.md` ALT-008).

**Better alternatives.** An in-network mediation component (a self-hosted gateway is the documented mechanism); inverting the caller so the private system initiates; an alternative platform whose deployment model matches; the requirement renegotiated with the security owner.

**Exceptions.** A public-endpoint-tolerant estate with standard residency — the ordinary case, where none of this applies. And private egress genuinely satisfied by the documented mechanism for a connector on its supported list, with the region pairing accepted.

**Evidence.** `platform-suitability.md` PS-32, PS-47, §2 rows 20, 29, 30, §3; `security.md` SEC-27, SEC-29, SEC-30, §2, §4 rows 9–11, SEC-XB-01; `integration-architecture.md` I-09, I-10, IA-27…IA-30, §3 (gateway and VNet rows), §7 items 5, 18–22, 28–29, §12.5, U-09, U-20; `data-architecture.md` DA-34, DA-35, DA-36, DA-57, DA-58, DAP-21, DAP-27, U-10, §2 rows 18–20; `architecture-patterns.md` matrix rows 23–25, Q-29, §13 (3rd composed disqualifier); `licensing-cost.md` LC-30; `governance.md` GOV-02, GOV-03.

**Confidence:** HIGH.

---


#### AP-D-068 — Agent surface treated as covered by the app and flow access model

**Description.** A conversational or agent surface is added over content the organisation already governs, and its access, connector and audience controls are assumed to be the ones already established for apps and flows. They are not the same controls, and two of the differences are documented as **permanent** rather than as a maturity gap.

**Classification:** ANTI-PATTERN · **Origin:** MS (each fact) + INF (the framing as one failure family with AP-D-030 and AP-D-033)

**Trigger conditions.**
- An agent or conversational surface is in scope and the security review reused the app's or flow's review.
- The organisation's connector posture rests on the **advanced connector policy** default-deny allowlist, and an agent surface is in scope.
- Guest access is restricted at the data layer, and an agent reaching organisational content through a search/graph connector is in scope.
- An external, partner or guest audience is named for a conversational surface.
- The agent's answer is treated as a read, and nobody has asked what it can reach on behalf of whom.

**Why it fails.** Three documented mechanisms, each of which breaks an assumption that holds for apps and flows:

1. **The strongest connector control does not cover this surface, by design and permanently.** The advanced connector policy — the default-deny allowlist that replaces the three-group classification — states as a **known limitation**: *"**Virtual connectors**: ACP doesn't support virtual connectors and won't support them in the future."* Copilot Studio's virtual connectors are meanwhile *"evolving into their own dedicated governance rules"*. So an organisation whose stated posture is *"all connectors are denied unless allowlisted"* does **not** have that posture on the agent surface, and the documentation says it never will through this control.
2. **An authorization decision made at one plane is bypassed at another.** *"Copilot Studio items using Microsoft Graph connectors **might access the information in these items even if you block guest access**."* This is the same failure family as AP-D-030 (the UI treated as the authorization layer) and AP-D-033 (one control treated as the whole control): the control was applied, it is working as documented, and it does not cover the path the requirement actually travels.
3. **The design-time enforcement that makes a policy visible to makers arrives per workload, not at once.** Design-time enforcement is *"rolling out across maker portals"* in the order Power Automate → Copilot Studio → Power Apps, and *"each maker portal's release of design-time enforcement for ACP marks the general availability of ACP for that workload"* — until then the policy is **runtime-only** for that workload, so a maker can build something the policy will later refuse to run.

**Consequences.**
- *Security:* organisational content reachable by an audience the organisation believes it excluded — the mass-exposure class of AP-D-034, arriving through a surface nobody reviewed.
- *Governance:* a stated connector posture that is true for two workloads and not the third, with no single place that says so.
- *Business:* an answer generated from content the asker was not entitled to see, which is a disclosure event rather than a defect.
- *Delivery:* a maker builds against a policy that is not enforced at design time and discovers the refusal at runtime.

**Detection signals.** An agent or "ask a question" requirement present while the security section names only apps and flows · a connector posture described as default-deny with no statement about virtual connectors · guest or external access restricted at the data layer with a graph/search-connector agent in scope · no named owner for the agent artefact · agent sharing not covered by the environment's sharing rules (they do cover agents, with editor/viewer granularity — absence means it was never configured) · a conversational requirement that never reached the security review at all.

**Decision impact.** Treat the agent surface as a **separate review scope** with its own audience, connector and authorization questions — `decision-criteria.md` **DC-D-116** is where the requirement is elicited, and DC-D-009, DC-D-058 and DC-D-068 are where its consequences land. Where the audience includes guests, partners or the public and a graph/search connector is on the path, the guest-access control **does not close the requirement** and either the path changes or the requirement is recorded as unmet. Where the organisation's posture depends on default-deny connector control, record explicitly that the posture does not extend to virtual connectors and name what does cover them.

**Better alternatives.** Scope the agent to content whose authorization is enforced at the data layer for every audience that can reach it; keep external and internal agent audiences in separate environments; make the agent's own artefact ownership and sharing an explicit decision (`governance.md` sharing rules cover agents with editor/viewer granularity); where the requirement genuinely needs an external conversational surface over sensitive content, `decision-criteria.md` §4A records that **no class is evaluated for this** and the outcome is `DECISION BLOCKED — MORE EVIDENCE REQUIRED`, not a redirect.

**Exceptions.** An agent scoped to content that is already unrestricted to the whole audience in question — there is no authorization boundary to bypass. Also: an internal-only agent in an environment with no guest access enabled and no virtual connectors in the design, where the app and flow controls genuinely are the whole control surface. Both exceptions require the check to have been made, which is the point.

**Evidence.** `security.md` SEC-04 (S-25 — guest-access bypass through graph connectors), SEC-24 (S-29 — ACP virtual-connector non-coverage, per-workload design-time enforcement), SEC-07/SEC-06 (S-28 — secrets consumable by agents), §9 (agent authentication/channels changed within the research window; re-verify); `governance.md` GOV-11b (G-13, G-17 — virtual connectors *"evolving into their own dedicated governance rules"*), GOV-19 (G-12 — sharing rules cover agents), GOV-16 (G-09 — agents in tenant inventory), GOV-U-06 (agent authentication and channel controls preview, not researched); `operations-support.md` OP-06 (O-08). Family: AP-D-030, AP-D-033, AP-D-034.

**Confidence:** MEDIUM-HIGH on each documented mechanism (all MS-sourced and quoted); MEDIUM on the framing as a single anti-pattern, which is this file's synthesis. **Note the standing gap:** `governance.md` GOV-U-06 records agent governance beyond data policy, virtual connectors and sharing limits as *preview and not researched*, so this entry covers the mechanisms the corpus documents and **cannot claim to be complete** for this surface.

---

### 5.6 Governance

#### AP-D-036 — Maker enablement without ownership or a promotion path

**Description.** Business users are enabled to build, without a defined promotion route to a governed environment, without ownership assignment, and without a support model — so successful tools become unowned production dependencies.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Maker enablement without: personal development environments inside a governed group; a promotion path that exists on day one; ownership assignment; restriction of manual environment creation; a support model.

**Why it fails.** The documented model is *managed makers*: personal developer environments, restricted sharing, a restrictive default-environment policy, and promotion via a pipeline — and *"the promotion path must exist before makers are unleashed."* Without it, adoption lands where governance is weakest (→ AP-D-040). Ownership is **not enforced by the platform**: ownerless artefacts are detected **weekly and only in managed environments**, and reassigning an owner *"doesn't automatically"* grant them environment or data-source permissions — so the detection does not produce a working owner. Standard deployment additionally makes the **requesting maker** the owner of deployed objects, which the corpus names as *the upstream cause of ownerless applications*. The consequences then chain into the automation-ownership failures: profile reversion when the owner leaves, 90-day inactivity suspension, suspension notices to an individual's mailbox.

**Consequences.** *Business:* a production dependency nobody is accountable for. *Operations:* no rota, no escalation, no runbook; the platform's response to abandonment is **silent disablement**. *Security:* over-sharing that the tenant only detects, never prevents; sharing limits *do not affect existing shares*. *Cost:* licence auto-claim assigning premium entitlements on app launch in managed environments, making sharing a cost event.

**Detection signals.** Makers building with no promotion route · unowned artefacts in the inventory · sharing at "everyone" scope · manual environment creation enabled · no support model documented · business processes depending on a tool with no named owner.

**Decision impact.** Enablement is a **governance package**, not a licence grant: environment routing to personal developer environments inside a governed group, manual creation restricted (separately — routing does not do it), a promotion path live on day one, ownership and support assigned per artefact class, and sharing limits set as both a security and a cost control. Where the package does not exist, the decision is to build it first — or to keep the workload in a governed delivery model.

**Better alternatives.** The managed-maker model with routing; a promotion pipeline; a named owner per artefact with a periodic attestation; the enterprise delivery model for anything above departmental class; a documented graduation trigger (→ AP-D-065).

**Exceptions. Genuinely personal productivity tools.** The corpus is explicit that a simple departmental class exists, is legitimate, and that over-engineering it is a real cost (→ AP-D-039). The anti-pattern is the absence of the *graduation* mechanism, not the existence of the class.

**Evidence.** `governance.md` GOV-01, GOV-04, GOV-08, GOV-09, GOV-13, GOV-14, GOV-17, GOV-18, GOV-19, GOV-A1, GOV-A2, GOV-A7, GOV-A8, §2, §4 rows 4, 7, 9; `alm-devops.md` ALM-20, ALM-A14; `operations-support.md` OP-04, OP-05, OP-28, OP-AP-01, OP-AP-19, `operations-support.md` DC-01; `automation-architecture.md` AT2-01, AT2-44, N-01, N-13; `licensing-cost.md` GOV-linked LC-23.

**Confidence:** HIGH.

---

#### AP-D-037 — Uncontrolled environment proliferation

**Description.** Environments are created per team, per app or on request, without a topology decision — outside every group, policy and control, and with a cost consequence nobody owns.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Manual environment creation enabled for licensed users; no naming or grouping taxonomy; one environment per app or team as the default; environment count growing without a cost view.

**Why it fails.** Without the tenant settings, any licensed user creates environments **outside every group, policy and control** — and the restriction *does not reach environments already created*. Configuration then drifts, because per-environment settings are per-environment; the grouping mechanism that fixes drift is itself **managed-environments-only**, one group per environment, no nesting, and **no per-environment exceptions**. The cost consequence runs on **four independent axes**: every environment consumes 1 GB of the tenant pool regardless of database; per-app entitlements are scoped **per environment**, so the same app in two environments is two entitlements; external-facing sites carry per-environment minimum assignments; and every *managed* environment requires premium licences for its active users. Those axes point in different directions from the governance and ALM axes, which is what makes this a genuine trade-off rather than a simple "fewer is better".

**Consequences.** *Governance:* an estate that cannot be described, policed or inventoried. *Cost:* storage floors, duplicated entitlements and premium populations, all unattributed. *Operations:* capacity overage that **blocks restore, copy, recover and environment creation** tenant-wide. *Security:* environments outside the isolation and policy model.

**Detection signals.** Environment count without a taxonomy · creation unrestricted · unmanaged environments holding business data · tenant capacity headroom near the notification thresholds · per-app entitlements duplicated across environments.

**Decision impact.** Decide the environment topology **with the cost axes visible**, alongside the governance and ALM requirements — and restrict creation as a separate, explicit action. The documented direction: development on developer-plan environments (free of both capacity and managed obligations), the count of *managed* environments minimised to those that genuinely need the premium feature set, sites consolidated, and billing/attribution aligned to the business units that carry cost.

**Better alternatives.** A designed topology with a grouping taxonomy built around its exceptions; environment routing for makers; developer-plan environments for development; consolidation where isolation is not required.

**Exceptions.** Environment-per-region or per-business-unit where residency or data rules require it — environments are geography-bound at creation, so this is a real driver, not sprawl.

**Evidence.** `governance.md` GOV-02, GOV-03, GOV-04, GOV-07, GOV-08, GOV-09, GOV-A2, GOV-U-02, GOV-U-03, §2, §4 rows 3, 10; `licensing-cost.md` LC-25, LC-AP-13, `licensing-cost.md` DC-13, §7.2 items 16, 18, 41; `operations-support.md` OP-20, OP-22, OP-AP-15, `operations-support.md` DC-15, DC-17; `alm-devops.md` ALM-08, ALM-24, ALM-25, ALM-U-05; `security.md` SEC-15, SEC-16.

**Confidence:** HIGH.

---

#### AP-D-038 — Policy without an operating model

**Description.** Connector and data policies are either absent, or created per project, with no catalogue, no exception process and no owner — so the policy layer either does nothing or fragments into an unmaintainable space.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** No tenant baseline policy (the starting state); a policy created per project or per environment; no connector catalogue; no exception process; no owner for policy change.

**Why it fails.** Both failure directions are documented. **Absence**: *"By default, no data policies are implemented in the tenant"* — the starting state is permissive, and new connectors are added to the default group over time, so the permissive surface grows on its own. **Fragmentation**: a policy per project produces **2^n fragmentation** of the connector space with empty groups, and maker-visible failures that are *hard to diagnose*; the most restrictive policy wins, so the composite behaviour is emergent rather than designed. Both directions produce the same operational hazard: a policy change can **suspend or quarantine existing applications and automations at runtime**, with up to 24 hours of enforcement lag — an outage caused by a governance action, arriving a day late.

**Consequences.** *Governance:* a control layer that either permits everything or is unmaintainable. *Delivery:* design-time blocks discovered late; makers routing around governance. *Operations:* runtime suspension presenting as an integration outage with no obvious cause. *Architecture:* a required connector blocked after the design depends on it.

**Detection signals.** No tenant baseline · policy count rising with project count · no connector catalogue or exception route · makers reporting unexplained blocks · a required connector's policy status unverified in the target environment.

**Decision impact.** A tenant baseline plus **minimal** environment exceptions, with a connector catalogue and a named exception process — and **policy count treated as an architectural variable**. Operationally, verify the required connector set against the target environment's policy **before** committing the design (the corpus lists this as a standard pre-commitment validation).

**Better alternatives.** Tenant baseline with documented exceptions; a layered posture (allowlist for certified connectors, classic policy for the custom/HTTP gap, target-side controls beyond); group-level rules where the grouping mechanism is available.

**Exceptions.** A small, homogeneous estate where one baseline suffices — which is the recommended end state anyway.

**Evidence.** `governance.md` GOV-10, GOV-11b, GOV-A4, GOV-A5, GOV-C3, §1 (lever 4), §2, §4 rows 5–6; `security.md` SEC-23, SEC-24, SEC-25, SEC-A8, SEC-A9, §4 row 14; `platform-suitability.md` PS-29, §3 (last boundary); `integration-architecture.md` §7 item 27, X-18, §9 row 28.

**Confidence:** HIGH.

---

#### AP-D-039 — Enterprise controls imposed on a trivial workload

**Description.** The full enterprise apparatus — managed environments, pipelines, source control, telemetry export, drills, support tiers — is applied to a short-lived departmental tool whose failure has no material consequence.

**Classification:** ANTI-PATTERN · **Origin:** MS (the class definition and the cost statements) + INF (the framing)

**Trigger conditions.** A workload in the simple departmental class — one maker, users report problems, no formal support, short life — carrying obligations from a higher class. Or: an organisation-wide standard with no differentiation by criticality.

**Why it fails.** The corpus is explicit that the departmental class *"is a legitimate class and over-engineering it is a real cost"*, and that at that class *"Nothing"* needs to change in the architecture. The cost is not hypothetical: managed environments require **premium licences for every active user** of the environment; the operational feature set (telemetry export, extended backup, cross-region recovery, pipelines, network isolation) all sits behind that; support plans are a **separate purchase**; and separate test environments, tooling and test runs carry stated costs. The corpus's most direct statement of the economics: full TCO *"frequently exceeds the value of a low-frequency process even when licences are free"* — so the correct answer for such a process may be **process change or do nothing**. Over-governance also has a second-order effect: group rules remove local administrative control in the ruled dimensions with **no exceptions supported**, and over-centralising *drives shadow adoption* — i.e. it produces the ungoverned estate it was meant to prevent.

**Consequences.** *Cost:* premium populations, environments and support tiers funded for no risk reduction. *Delivery:* lead time that makes the platform useless for the class it serves best. *Governance:* shadow adoption — the mirror failure of AP-D-036. *Business:* a negative-return automation delivered rigorously.

**Detection signals.** A criticality classification absent from the engagement · one uniform standard for all workloads · a short-lived low-value tool with pipelines and drills in scope · makers building outside the platform to avoid the process.

**Decision impact.** Classify criticality **first**, and let the class select the obligations. The chain the corpus states is *criticality → operational requirements → managed environment → premium licences* — which means the class decision is also the economics decision, and it belongs in option selection rather than in an operations review. For genuinely low-value processes, carry process change and do-nothing as priced options.

**Better alternatives.** A tiered governance model with an explicit graduation trigger; the departmental class served with light controls and a documented ceiling; process change; the existing licensed capability.

**Exceptions.** A workload that *looks* trivial but sits on a critical path, handles sensitive data, or has a plausible route to criticality — then the higher class is correct, and the trap is AP-D-065 instead. The two anti-patterns are a matched pair and the classification is what separates them.

**Evidence.** `operations-support.md` §1, §1.1, OP-21, `operations-support.md` DC-16; `licensing-cost.md` LC-22, LC-23, LC-25, LC-28, LC-AP-13, §7.2 items 34–39; `governance.md` GOV-06, GOV-07, GOV-11, GOV-A9, GOV-A10, GOV-C2, §4 row 2; `alm-devops.md` §1 (the ladder), ALM-C2; `performance-scale.md` §11.1 (testing costs money).

**Confidence:** MEDIUM (the class and costs are MS; the over-engineering framing is INF, consistent with the corpus's own §8.7 caveat).

---

#### AP-D-040 — Production workload in a non-production environment class

**Description.** A business process runs in a default, sandbox, developer or trial environment — usually because that is where it was built and it worked.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Business data or a business process in a non-production environment type; the default environment holding anything beyond personal productivity; a trial environment on any path that matters.

**Why it fails.** The environment **type** determines zone redundancy, backup and backup retention, recovery eligibility, pipeline eligibility, service-protection headroom and capacity consumption. The vendor's statement is direct: *"Don't deploy production processes and data in nonproduction types like sandbox, developer, or trial environments."* Specifics: **trial environments are not backed up at all** and have a **single web server**, which means a proof of concept there measures a different platform than production; the default environment **cannot have a security group applied**, has **no backup guarantee** and cannot be manually backed up, and **every licensed user holds maker rights in it**; non-production types get **none** of the zone-redundancy guarantees; extended backup retention requires a *production managed* environment; and restore *cannot target production directly*.

**Consequences.** *Business:* unrecoverable data loss with no contractual position. *Security:* no membership boundary; everyone a maker. *Operations:* outside the resilience commitments, and outside the recovery mechanisms. *Performance:* a capacity profile that does not represent production.

**Detection signals.** Business processes in the default environment · trial environments in the delivery plan · no security group on an environment holding sensitive data · backup expectations stated without checking the environment type · a proof of concept whose performance results are being used for sizing.

**Decision impact.** Environment type is a **design decision tied to criticality**: production type for anything business-critical, developer-plan for development, managed where the operational feature set is needed, never trial for anything that matters. Moving out is a documented procedure with a data-migration step, so the cost of getting this wrong is a migration, not a setting change.

**Better alternatives.** A designed environment topology (→ AP-D-037); the documented move-out procedure with an owner; environment routing so makers never build in the default environment in the first place.

**Exceptions.** Genuinely non-production work — development, training, throwaway prototypes — in the environment types intended for it.

**Evidence.** `operations-support.md` OP-14, OP-20, OP-22, OP-AP-16, `operations-support.md` DC-05, DC-15; `governance.md` GOV-04, GOV-17, GOV-21, GOV-A1, GOV-A3, §4 row 1; `platform-suitability.md` PS-05, PS-37, AP-7; `performance-scale.md` PF-41, PF-AP-17, §8.1 items 5, 34–36, §3.D row 34; `security.md` SEC-17, SEC-A3; `integration-architecture.md` IA-29 (trial/Teams excluded from private networking).

**Confidence:** HIGH.

---
### 5.7 ALM and delivery

#### AP-D-041 — Development in production

**Description.** Changes are made directly in the production environment, or production carries unmanaged artefacts, so there is no separation between authoring and running.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Edits made in production; unmanaged solutions or default-solution work in production; makers holding maker rights in production; no development or test environment.

**Why it fails.** An unmanaged layer **permanently shadows managed updates** — the vendor's position is unambiguous (*"Except for your development environment, you should only have managed solutions in your environments"*), and the countermeasure exists precisely because the practice is common. Unmanaged work is also **not portable and data-destructive to unwind**. The mission-critical contrast is stated as a table row: *"Development in production"* versus *"Exercises application lifecycle management."* Security guidance is equally direct: *"Don't allow maker permissions in test and production environments."* Two consequences bite later: the integrity control that prevents this **breaks a documented list of first-party features**, so enabling it is a real decision with a real cost; and the environment class that supports the controlled alternative is managed, hence premium-licensed.

**Consequences.** *ALM:* changes that cannot be promoted, reviewed or reverted. *Security:* no separation of duties; unreviewed change in production. *Operations:* no way to reproduce a defect outside production. *Business:* an outage caused by an unreviewed edit, with no rollback (→ AP-D-045).

**Detection signals.** Production edits in the change history · unmanaged layers present · maker roles assigned in production · no test environment · "we'll fix it live".

**Decision impact.** A custom solution with a single publisher and a managed-only downstream estate is the **minimum rung** for anything beyond a personal tool; production integrity control is a decision with a named break-list to accept or a named exception to record. Where a first-party workload's features conflict with the control, the choice is explicit — *"Either forgo that control or forgo those features — record the decision."*

**Better alternatives.** Development environment plus managed downstream; block-unmanaged-customizations with its break-list accepted; support access via co-ownership on managed artefacts (which permits reading run history, enabling/disabling and running, without edit rights); the documented conversion procedure for an existing unmanaged estate.

**Exceptions.** The development environment itself. And the documented case where a required capability is **unmanaged-solution-only** (contact-centre multi-session), which the corpus flags as a conflict requiring a first-party alternative or a governance exception — not a silent override.

**Evidence.** `alm-devops.md` ALM-01, ALM-02, ALM-03, ALM-05, ALM-15, ALM-A1, ALM-A2, ALM-A3, §1, §2, §4 rows 1–2, 15; `security.md` SEC-36, SEC-A3, SEC-A14, SEC-A15, §4 row 17; `governance.md` GOV-15, GOV-20, GOV-A6, §4 row 8; `operations-support.md` OP-AP-06, §1; `application-architecture.md` AA-20, AP-35.

**Confidence:** HIGH.

---

#### AP-D-042 — Business-critical solution without source control

**Description.** A solution on which the business depends has no version history, no branch-based review and no rehydration path — typically because promotion automation was mistaken for source control.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Business-critical or enterprise-class solution plus any of: no repository; more than one maker on one artefact; a requirement that changes be reviewed before test; code-first components in the solution; a cross-tenant delivery requirement.

**Why it fails.** The rungs buy different things. Promotion automation gives artefact immutability across stages, run history and optional approvals — but **no code review and no diff**. Version history, branching, pull requests, code review and rehydration come only from source control, so *"source control is the requirement that forces rung 3, not automation."* Team size forces it independently: unmanaged solutions give **no isolation** — *"Every modification is applied directly to the environment, regardless of which solution is being edited"* — and co-authoring on the low-code app artefact **was removed**, so parallelism is achievable only through architecture (an environment per developer or branch). Cross-tenant delivery also forces it, since the built-in promotion mechanism cannot cross tenants.

**Consequences.** *Delivery:* concurrent work overwritten; no reviewable change record. *Governance:* no compliance evidence linking a change to an approval or a work item (work-item traceability is not in-product). *Operations:* no recovery to a previous known state. *Business:* a critical dependency whose history cannot be reconstructed.

**Detection signals.** No repository for a critical solution · two or more makers on one artefact · a review requirement with only approval gates available · code components in scope · an ISV or multi-tenant delivery model.

**Decision impact.** The **rung is selected by the requirement**, and the requirement is usually review or team size rather than automation. Rung 3 carries prerequisites that belong in the option: a repository, a development environment per maker or branch, and pro-dev capability. Note also that the two rungs are **not alternatives** — the documented position is source control in *developer* environments and promotion automation for *deployment*.

**Better alternatives.** Native repository integration in developer environments plus promotion automation for deployment; build-tool pipelines where cross-tenant or deeper control is needed; a documented manual record where the class genuinely does not justify rung 3.

**Exceptions.** Single-maker departmental tools — rung 1 is sufficient and rung 3's prerequisites are a real cost (→ AP-D-039). Residual uncertainty is recorded: `alm-devops.md` ALM-U-03 leaves the practical maturity of repository integration for the low-code app artefact specifically unverified, so the *mechanism* claim is MEDIUM even though the *requirement* claim is HIGH.

**Evidence.** `alm-devops.md` §1 (the ladder), ALM-06, ALM-09, ALM-10, ALM-21, ALM-23, ALM-A5, ALM-A7, §2, §4 rows 3–5, 12, 14, 16, ALM-C1, ALM-U-03; `application-architecture.md` AA-06, AA-C2, AA-C9; `platform-suitability.md` PS-24, PS-48, AP-15.

**Confidence:** MEDIUM.

---

#### AP-D-043 — Manual deployment as the permanent operating model

**Description.** Export-and-import by hand is the steady-state release mechanism for a solution that matters, rather than a transitional state.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Manual promotion as the documented steady state; no artefact integrity guarantee between stages; no run history of deployments; the deployer becoming the owner of deployed objects; a separation-of-duties requirement.

**Why it fails.** Manual export/import has **no traceability, no artefact integrity and no prevalidation**, and it makes the **deployer the owner of the objects** — which the corpus identifies as the upstream cause of ownerless applications. It also cannot satisfy separation of duties: the mechanism designed for that is delegated deployment with a service principal, which itself requires that identity to hold administrative rights in each target (*"Lower permission security roles can't deploy plug-ins and other code components"*), making the deploying identity a **governed asset**.

**Consequences.** *Governance:* no release evidence; no separation between who builds and who deploys. *Operations:* ownership of production objects assigned by accident. *Delivery:* deployment defects and drift between stages. *Compliance:* no auditable record of what was released when.

**Detection signals.** Release process documented as manual steps · no deployment history · production objects owned by individuals · a separation-of-duties requirement with no delegated identity · differences between stages that nobody can explain.

**Decision impact.** Automated promotion is required for anything above the departmental class — and it carries a **prerequisite that changes the economics**: target environments must be managed, therefore premium-licensed for their active users. The corpus records this as a genuine tension (`alm-devops.md` ALM-C2: the "approachable" option is the licence-expensive one), which belongs in the option's cost rather than being discovered afterwards. Cross-tenant or multi-developer isolation needs the build-tool route instead.

**Better alternatives.** In-platform pipelines with delegated deployment and approvals; build-tool pipelines for cross-tenant or deeper control; a documented manual record with an accepted risk statement for the departmental class.

**Exceptions.** Departmental class with a single maker and a tolerant process. Also a genuine transition period, provided it is dated.

**Evidence.** `alm-devops.md` ALM-10, ALM-11, ALM-20, ALM-A6, ALM-A14, §1, §4 rows 5–6, ALM-C2, ALM-U-02; `governance.md` GOV-14, GOV-A7; `security.md` SEC-22, SEC-36, SEC-A15; `operations-support.md` OP-16, `operations-support.md` DC-09; `licensing-cost.md` LC-23, L-21.

**Confidence:** HIGH.

---

#### AP-D-044 — Environment-specific values shipped inside the release artefact

**Description.** Connection details, endpoints, identifiers and other per-environment values are embedded in the solution, so the same artefact cannot be promoted unchanged.

**Classification:** **CONSTRAINT** (reclassified 2026-09-03 — always wrong within its scope; see §2) · **Origin:** MS

**Trigger conditions.** Any per-environment value inside the solution; no environment-variable or connection-reference design; secrets in the solution; a dataflow or connector whose connection must be re-established per deployment.

**Why it fails.** Contradicted verbatim in the canonical evidence, with a named outcome: it *"produces production pointing at development data sources."* The sanctioned mechanism separates definition (in the solution) from value (supplied at deployment), and secrets go to a vault — consumable, as noted in AP-D-031, by only three component types. Two documented complications belong in the design rather than in the implementation: connectors need a separate solution with an explicit import order, and the low-code app artefact **does not recognise connection references**, with a workaround that can create an unmanaged layer; and dataflow deployments require **manual connection re-establishment**, with the documented mitigation being a separate solution per dataflow set.

**Consequences.** *Data:* production writing to development data, or reading it. *Security:* credentials travelling in an artefact. *Delivery:* every promotion becomes a manual edit, which reintroduces AP-D-043. *Operations:* connections break on restore and must be re-supplied (→ AP-D-045).

**Detection signals.** Endpoints or identifiers visible in the solution · no environment variables in the design · promotion requiring post-import edits · connections re-created by hand each release · secrets in action inputs.

**Decision impact.** Environment variables and connection references are **designed in from the start**, and the connector/dataflow exceptions are named as explicit post-deployment steps with owners. Where the workaround would create an unmanaged layer against a mandatory integrity control, the corpus's rule applies: redesign the seam or record a governance exception with owner and expiry — do not disable the control silently.

**Better alternatives.** Environment variables plus connection references with per-environment deployment settings; vault-backed secrets for the supported component types; a separate solution per connector and per dataflow set with a documented import order.

**Exceptions.** None for values that differ per environment. Genuinely invariant values are not this anti-pattern.

**Evidence.** `alm-devops.md` ALM-13, ALM-14, ALM-A11, §2, §4 rows 7, 8, 8a, ALM-U-07, §14.1; `security.md` SEC-07, §4 row 12; `integration-architecture.md` I-28, §7 item 33; `data-architecture.md` DA-49; `operations-support.md` OP-17, `operations-support.md` DC-12.

**Confidence:** HIGH.

---

#### AP-D-045 — Rollback assumed to exist

**Description.** The release plan assumes a bad change can be undone, without establishing which mechanism would do it or what it destroys.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A reversibility requirement with no named mechanism; restore treated as rollback; a previous-version redeployment assumed available without the setting being enabled; no rehearsal.

**Why it fails. There is no solution rollback.** The three real options are: redeploy a previous version (only where that setting is enabled *before* it is needed), restore a backup, or fix forward. Restore is not a rollback — it **deletes solution automations in the target, invalidates every connection reference, changes app identifiers, loses broad sharing, returns the environment in administration mode, cannot target production directly, is same-region and managed-to-managed, needs free capacity, and can take more than a day**. Patches, the apparent hotfix mechanism, are documented as *"not recommended"*, and the promotion mechanism **cannot bypass a stage**, so a hotfix is a normal release on a compressed schedule or a governed exception. And restore has an integration consequence: it **rewinds one participant** while external systems, queues and replicated copies retain later state, so the release/recovery plan needs a post-restore integration step.

**Consequences.** *Operations:* an outage extended by a recovery that was never rehearsed and that breaks connections. *Data:* divergence between the restored environment and everything integrated with it. *Business:* a rollback promise that cannot be kept. *Cost:* capacity overage silently **blocking** restore altogether.

**Detection signals.** "We can always roll back" with no mechanism named · restore in the plan with no reconnection checklist · previous-version redeployment assumed but not enabled · no restore rehearsal · tenant capacity headroom below the threshold that blocks restore.

**Decision impact.** The reversibility strategy must be **named, enabled and rehearsed before go-live**: which mechanism, what it destroys, who re-establishes connections and sharing, how long it takes, and what happens to integrated systems and replicas. Capacity headroom becomes a **recoverability requirement**, not a finance matter. For a business-critical workload this is a gating condition, not a runbook appendix.

**Better alternatives.** Previous-version redeployment enabled and tested; fix-forward with a compressed but identical release path; a rehearsed restore runbook including reconnection, re-enablement, re-sharing and republishing, with owners and elapsed-time estimates; feature flags where the change can be disabled rather than reverted.

**Exceptions.** Departmental class with a tolerant process — fix-forward with an accepted risk statement is a legitimate answer, provided it is stated.

**Evidence.** `alm-devops.md` ALM-03, ALM-04, ALM-10, ALM-18, ALM-A8, ALM-A9, §2, §4 rows 9–10, ALM-U-06, §14.4; `operations-support.md` OP-14, OP-16, OP-17, OP-22, OP-23, OP-AP-08, OP-AP-10, `operations-support.md` DC-05, DC-06, DC-09, DC-11, OP-U-03; `data-architecture.md` DA-18, DAP-14; `governance.md` GOV-21, GOV-XB-04; `performance-scale.md` §8.1 item 27, §11.2 (restore is not performance-neutral).

**Confidence:** HIGH.

---

#### AP-D-046 — Single-sided supply chain for a two-sided architecture

**Description.** A hybrid architecture is delivered with only the low-code half under a managed lifecycle; the external half is deployed by hand, unversioned, and released independently of the contract it serves.

**Classification:** ANTI-PATTERN · **Origin:** MS (the obligations) + INF (the framing)

**Trigger conditions.** A hybrid design where the external component has no pipeline, no infrastructure-as-code, no versioned contract, or no declared release sequencing with the platform side.

**Why it fails.** Hybrid patterns **require two coordinated supply chains**: a solution pipeline *and* an infrastructure/code pipeline, with the release unit declaring **contract compatibility and sequencing**. Deploying only one side is admissible only where backward/forward compatibility is guaranteed — otherwise the two halves diverge in production. The seam itself is a versioned contract whose change cost is manual across every consumer (→ AP-D-025). Two further obligations are easy to miss: the compensation and reconciliation artefacts (idempotency keys, mapping rules, compensating actions, reconciliation schemas) are **part of the contract** and require change control equal to the forward write path; and recovery crosses the boundary, so a restore on one side needs a defined action on the other.

**Consequences.** *Delivery:* a production mismatch between contract versions. *Operations:* an incident whose cause is a partial release nobody recorded. *Data:* compensation logic out of step with the write path it is meant to reverse. *Governance:* an external estate outside change control (→ AP-D-026).

**Detection signals.** A hybrid design with one pipeline · no declared release order · no contract version in the interface · reconciliation logic maintained outside change control · the external half deployed by an individual.

**Decision impact.** A hybrid option is only complete when **both** supply chains exist, with a declared sequencing rule and a compatibility policy. If the second pipeline cannot be funded or owned, the hybrid is not available — the same conclusion as AP-D-026, reached from the delivery side.

**Better alternatives.** Two pipelines with a declared release order and a backward-compatibility policy; treating the connector and API contract as one release boundary; an existing enterprise boundary whose supply chain already exists; keeping the requirement in one platform.

**Exceptions.** A genuinely versioned, backward-compatible contract where the sides can release independently by design — which is itself a designed property, not a default.

**Evidence.** `alm-devops.md` §14.1, §14.2, §14.4, §14.5, ALM-14, criterion 8a; `architecture-patterns.md` §5.1 (deployment-maturity row), AP-05, AP-10, §13; `automation-architecture.md` AT2-53, N-52; `governance.md` GOV-XB-01; `integration-architecture.md` I-07, IA-49, §12.7.

**Confidence:** MEDIUM.

---

#### AP-D-047 — Unmanaged artefact structure above the departmental class

**Description.** Applications and automations are built outside solutions for a workload that needs backup coverage, capacity licensing, monitoring or automated deployment.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Non-solution artefacts plus any requirement for: backup coverage, a capacity licence on an automation, inclusion in the automation-monitoring surface, or pipeline deployment.

**Why it fails.** All four of those capabilities require the artefact to be **in a solution**. Non-solution artefacts are excluded from backup coverage, ineligible for capacity licences, invisible to the monitoring surface, and undeployable by pipeline; restore also treats solution and non-solution artefacts differently. Ownership is worse: a **non-solution automation's owner cannot be changed at all**. The corpus's conclusion is that solution-aware artefacts are *"a day-one hard requirement above the departmental class"* and that *"retrofitting is rework."*

**Consequences.** *Operations:* artefacts outside recovery and monitoring. *Cost:* the capacity-licence remedy for throughput or ownership is unavailable, which forecloses the fix for AP-D-066. *Governance:* an artefact whose ownership is permanently stuck with a departed individual. *Delivery:* retrofit work at exactly the moment the workload became important.

**Detection signals.** Apps and automations outside solutions · backup expectations on non-solution artefacts · a capacity licence proposed for an automation not in a solution · artefacts missing from the inventory · an automation owned by a leaver.

**Decision impact.** Solution-awareness is a **day-one structural decision** driven by the criticality class, not a later tidy-up. It is also a precondition for several other decisions (capacity-licensed ownership, pipeline deployment, backup coverage), so it must be settled before those options are costed.

**Better alternatives.** Custom solution with a single publisher from day one; a documented graduation trigger for the departmental class (→ AP-D-065); retrofit planned and funded where it is already the case.

**Exceptions.** Genuinely personal or team-scoped productivity tools with no backup, licensing, monitoring or deployment requirement.

**Evidence.** `operations-support.md` OP-15, OP-14, OP-AP-07, `operations-support.md` DC-10, §1.1; `alm-devops.md` ALM-02, ALM-05, ALM-A3, §4 row 1; `automation-architecture.md` AT2-46, N-13; `licensing-cost.md` LC-08, §7.2 item 43; `governance.md` GOV-14.

**Confidence:** HIGH.

---

### 5.8 Performance and scale

#### AP-D-048 — Documented limits read as performance guarantees

**Description.** A design is declared performant because it violates no published limit — treating an exclusion boundary as a service level.

**Classification:** ANTI-PATTERN · **Origin:** MS (the absence) + INF (the framing)

**Trigger conditions.** A performance conclusion drawn from limit arithmetic alone; "within envelope" read as "fast enough"; a latency or throughput commitment made with no measurement plan; a sizing conversation that never mentions measurement.

**Why it fails.** Manifest reservation **NB-07** states it directly: the corpus is **limits-based, not benchmark-based**, and *no universal empirical throughput, latency or concurrency benchmark exists*. The handling rule is that documented limits are **exclusion/envelope evidence only**, and workload measurement is required where performance is decision-critical. The corpus enforces this in its own vocabulary — verdicts are phrased *"no documented constraint violated"*, never *"Microsoft says this performs well"* — and records the absences plainly: **no concurrent-user figure is published for any application surface**; **no end-to-end latency figure is published for any path**; effective throughput on the primary data service is *not a published number* (a per-window figure multiplied by an **undisclosed, licence-dependent** web-server count); and no independent benchmark of any component was found, *"the absence is itself the finding."*

**Consequences.** *Business:* a performance commitment with no evidentiary basis. *Architecture:* a design that is compliant and too slow. *Delivery:* remediation discovered at go-live. *Operations:* a degradation with no baseline to compare against.

**Detection signals.** "It's within the limits" as the performance answer · a latency or concurrency figure quoted with no source · no measurement in the validation plan · a proof of concept in an environment type with a different capacity profile (→ AP-D-040).

**Decision impact.** Separate two verdicts explicitly: **envelope** (from limits — a genuine exclusion test) and **performance** (from measurement). Where performance is decision-critical, a measurement obligation enters the option with its cost and its environment prerequisites. Where it cannot be measured, the honest output is an accepted risk with a degradation plan, not a claim.

**Better alternatives.** Limit arithmetic as an exclusion filter, followed by a bounded pilot with monitoring at representative volume and personas; a degradation plan and throttling monitoring in production; hosting the peak-bearing component where measurement is permitted if proof is existential.

**Exceptions.** Where the limit arithmetic **excludes** the design, that conclusion is sound on limits alone — exclusion is the one verdict limits can carry by themselves.

**Evidence.** `performance-scale.md` §0, §3 (verdict framing), PF-09, PF-14, PF-15, PF-22, PF-U-01, PF-U-10, §8.1 items 4, 13–17, §8.2 item 48, §8.3, PF-C-02, PF-C-03; `automation-architecture.md` §8.7, U-10; `integration-architecture.md` U-04, §13.1 item 4; `architecture-patterns.md` APR-U-02; `data-architecture.md` U-30, U-31; manifest NB-07.

**Confidence:** HIGH.

---

#### AP-D-049 — Sizing against a single meter

**Description.** Capacity is assessed against one limit — usually the daily entitlement that licence conversations centre on — while the constraint that actually binds is a different, independently-evaluated one.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A sizing statement citing one number; no per-connector throttle analysis; peak expressed as a daily total; the client-side and structural limits absent from the analysis; batching proposed as a way around an entitlement.

**Why it fails.** **Five meters are evaluated separately**: the request entitlement (per owner identity, 24-hour and 5-minute windows), service protection (per authenticated user, per web server, 5-minute window), the per-connector throttle (per connection, 10–60-second windows), client-side capacity (per session/device), and product structural limits (per artefact definition). The binding constraint is the **smallest of the five** — and the corpus states that in practice it is *normally the connector or service protection, not the daily entitlement*. Microsoft pre-empts the obvious workaround: *"Batch operations aren't a valid strategy to bypass entitlement limits. Service protection API limits and entitlement limits are evaluated separately."* Connector limits are *"often reached before"* platform limits. Frequency matters independently of volume: *"Two integration scenarios might involve the same total volume, such as 60,000 records per hour and 1,000 records per minute, but differ in frequency… Don't assume one solution fits both."* And the weakest-link rule extends beyond the platform: *"Integration performance depends on the capability of each system involved. The weakest system in the chain limits the overall result."*

**Consequences.** *Performance:* throttling at a fraction of the assumed capacity. *Business:* silent slowdown then automatic disablement (→ AP-D-021). *Cost:* the remedy is commercial, and unbudgeted. *Architecture:* a design whose partitioning strategy was never considered because the constraint was never identified.

**Detection signals.** A single number in the sizing · peak stated as a daily average · no connector named in the throughput analysis · batching cited as the scaling strategy · no figure for the *other* system's capability · a shared connection carrying several artefacts' traffic.

**Decision impact.** Express throughput in **all five units** before any verdict, plus the far end's own capability, at the **peak** rather than the average, over the investment horizon. The binding meter selects the remedy: partition across identities or connections; move the data leg to the service-protection-exempt in-platform mechanism; introduce a broker; or leave the platform where no natural partitioning exists.

**Better alternatives.** Five-unit sizing with the peak and the horizon; per-connection throttle analysis for every connector on the path; the exempt server-side mechanism for the metered data leg; brokered load levelling with bounded consumers.

**Exceptions.** Workloads so far inside every meter that the analysis is trivially satisfied — but the corpus's point is that this must be *checked*, since the cheapest owner profile is 50× below the highest on two separate meters.

**Evidence.** `performance-scale.md` §2, §3.C, PF-22, PF-27, PF-28, PF-29, PF-31, PF-AP-09, PF-AP-14, B-03, B-09, §8.1 items 4, 6, 44, PF-C-01; `automation-architecture.md` AT2-02, AT2-04, §9 row 3, C-02; `integration-architecture.md` I-01, IA-01, IA-02, IA-06, IA-07, IA-10, IA-11, §2.1 rows 1–4, §12.4, U-15; `data-architecture.md` DA-10, DA-32, SC-01, SC-02, SC-21; `licensing-cost.md` LC-09, LC-C-01.

**Confidence:** HIGH.

---

#### AP-D-050 — Non-delegable access path over a growing dataset

**Description.** An interactive query path that cannot be pushed to the data source is built over a dataset that will exceed the client-side row ceiling — so the application returns a truncated answer as if it were complete.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Free filtering, sorting, searching, counting or aggregating expected over a collection above ~2,000 rows, where the expression set or the source is not delegable. Two traps produce **no warning at all**: collection-based indirection, and sources that are not on the delegable list — including the virtualization mechanism, which is absent from that list.

**Why it fails.** The failure is **silently wrong answers, not slow ones**: only the first 500 (default) or 2,000 (maximum) rows are considered, and the result is presented as authoritative. The workaround family — loading everything into a collection to escape the warning — is named by Microsoft itself as part of an anti-pattern trio, and does not help: the ceiling still applies and the network payload and client memory cost are added. Delegability is **source-specific**, and the document/list store's table is the narrowest of the three. Aggregation has its own separate ceiling on the primary store, and traversal depth is capped.

**Consequences.** *Data:* wrong figures in business decisions, with no error to investigate. *Business:* trust lost in the application, usually before the cause is found. *Performance:* payload and memory pressure from the workaround. *Architecture:* the store or the access path is wrong, and the remedy is a store or design change, not tuning.

**Detection signals.** Row-count trajectory over the horizon versus the ceiling · free-text or negative-operator search over a large collection · aggregation or counting requirements · a non-delegable source under an interactive path · collections used as the data layer · users reporting "the number looks wrong".

**Decision impact.** Above the ceiling, **every interactive query must be delegable or the read must be pre-shaped server-side** — and the corpus gives an explicit test: set the data row limit to 1 and verify. If neither is possible, the interactive surface is **out of envelope**, which is a store or surface decision. This is a correctness decision, which is why it sits at Block D altitude while its implementation cousins do not.

**Better alternatives.** A delegable store with a delegable expression set; server-side shaped views or an API returning pre-aggregated results; an analytical path for aggregates (→ AP-D-009); constraining the access paths so they are few and indexable.

**Exceptions.** Small, bounded, non-growing datasets. And genuinely delegable expression sets against a delegable source, which is the normal, correct case.

**Evidence.** `performance-scale.md` PF-01, PF-02, PF-03, PF-05, PF-AP-01, PF-AP-02, B-01, B-02, §3.A rows 1–3, §8.1 items 1–3, §8.2 item 46, DC-01, DC-02; `data-architecture.md` DA-02, DA-31, DA-39, DA-40, DAP-22, VT-05, VT-09, C-09, §2 row 2, §3; `platform-suitability.md` PS-13, AP-4, §2 row 6; `application-architecture.md` AA-07, AP-19.

**Confidence:** HIGH.

---

#### AP-D-051 — Inventing the number the platform does not publish

**Description.** A threshold is asserted where the platform publishes none, or one side of a documented conflict is adopted as fact — and a design or a commitment is sized against it.

**Classification:** **CONSTRAINT** (reclassified 2026-09-03 — always wrong within its scope; see §2) · **Origin:** MS (the absences and the conflicts) + INF (the framing)

**Trigger conditions.** Any of the following quoted as a figure:
- a concurrent-user ceiling — **none is published anywhere**, across the sources the corpus checked;
- a write-amplification multiplier ("one business transaction = N requests") — amplification is a property of *each solution's own customisation*, never published;
- a security-model performance curve for unit depth, team/share cardinality or column-security complexity (**NB-04 / `PF-U-07`**);
- a standard-table row or size ceiling — none published;
- the custom-connector throughput limit — **`CONFLICTED`** (**NB-02 / `IA-C-01`**);
- a cross-region recovery-time commitment — none published;
- the effective per-identity throughput of the primary store (a per-window figure × an **undisclosed** web-server count);
- a canvas size threshold — the corpus explicitly forbids encoding one;
- default tenant database capacity, capacity add-on size, or entitlement figures where two pages disagree.

**Why it fails.** Two distinct mechanisms. **Invention**: the number does not exist, so the design rests on a fabrication that no one can validate and that will be believed downstream. The corpus makes this an anti-pattern in its own right in three areas, and manifest §7 forbids *"inventing missing numeric thresholds, availability guarantees, cost values, performance curves or supported behaviours."* **Premature resolution of a conflict**: for the custom-connector figure the two current Microsoft pages differ by **20×** — *"A design sized at 10,000/min that is actually capped at 500/min fails by a factor of twenty."* Verified again on **2026-09-03** (§6, V-D-02/V-D-03): the limits page states *"500 requests per minute per connection"* (`ms.date` 2026-07-17, updated 2026-07-18) while the connector FAQ still states *"10000 requests for each connection created by the connector"* for this platform (`ms.date` 2025-03-13, updated 2025-09-10). **The conflict is open.** The manifest's rule stands: do not encode either value as a threshold; revalidate and measure.

**Consequences.** *Architecture:* a sizing error of up to an order of magnitude. *Business:* a commitment with no basis. *Governance:* a fabricated figure propagating into a pack, a proposal and a contract. *Cost:* remediation whose scale was never modelled.

**Detection signals.** A concurrency, amplification or throughput figure with no citation · a figure attributed to "another project" or "a blog" · a conflict resolved in the analysis but not in the sources · a security-model performance assurance · a contractual recovery-time figure.

**Decision impact.** Where a number is decision-critical and unpublished or conflicted, the criterion becomes **decision-blocking**: `DECISION BLOCKED — MORE EVIDENCE REQUIRED`, closed by a bounded measurement or a vendor statement, not by an estimate. The corpus supplies the substitutes: a load test against a production-like environment for concurrency; measurement per engagement for amplification; a representative pilot at target model complexity for the security-model curve; measurement plus current-documentation revalidation for the connector throughput.

**Better alternatives.** Measure it (the corpus names the instrumentation); drive concurrency from the runtime hint the service returns rather than a hard-coded value; record the unknown as an unknown with a resolution path; where the figure is existential, host the peak-bearing component where it can be proven.

**Exceptions.** None. Recording a *measured* value from this engagement, dated and scoped, is not invention — it is evidence, and it must not be generalised to the next engagement.

**Evidence.** `data-architecture.md` DAP-41, DAP-42, SC-01, SC-02, SC-16, SC-17, SC-21, U-30, U-31, U-33, U-39, C-01; `performance-scale.md` PF-U-01, PF-U-03, PF-U-07, PF-U-10, PF-AP-14, §3.C row 29, §8.1 items 4, 13–16, PF-C-01; `integration-architecture.md` IA-C-01 (C-01), U-01…U-04, U-15, §3; `application-architecture.md` AA-C1, U-A1, §9 condition 3; `licensing-cost.md` LC-C-01, LC-U-02…LC-U-05; `platform-suitability.md` C-1, C-8, U-2, U-3, U-6, U-15; manifest §5, §7, NB-02, NB-04, NB-07. Verification: §6 V-D-02, V-D-03.

**Confidence:** HIGH.

---

#### AP-D-052 — Validation level not matched to the commitment being made

**Description.** The evidence gathered before go-live does not support the promise made — static analysis treated as a functional test, a functional test treated as a performance test, or a documentation review treated as proof of a recovery objective.

**Classification:** ANTI-PATTERN · **Origin:** MS (the tool limits) + INF (the level model)

**Trigger conditions.** A business-critical or mission-critical commitment with no validation plan; static analysis cited as the release gate; performance sign-off with no measurement; a recovery objective with no drill; a proof of concept in an environment whose class differs from production; behaviour that depends on managed-environment, network or security controls, tested where those are absent.

**Why it fails.** The corpus defines four **complementary** levels — V1 documentation/limits, V2 bounded pilot with monitoring, V3 pro-dev automated harness, V4 managed-test fidelity — and states that *"A business-critical release must state which validation level is required and budget it."* The individual tool limits are documented: static analysis *"doesn't guarantee that a solution import will be successful"* and is not a functional test; there is **no supported first-party low-code functional-test framework** after the deprecation of the previous one, so a functional harness is a pro-dev cost or a manual UAT with an explicit regression-risk statement; **full-scale load testing against the shared service is constrained** (*"Limit tests to avoid unintended consequences"*), which is why peak confidence must come from limit arithmetic plus a bounded pilot plus production throttling monitoring plus a degradation plan; a test environment cannot mirror production if production is managed and the test environment is not; **no prescriptive recovery test plan exists** and a drill *"can't perfectly replicate"* a real event; and a trial environment has a **single web server**, so measurements taken there do not transfer.

**Consequences.** *Business:* a commitment that fails on first contact with production. *Operations:* an unrehearsed recovery attempted under pressure. *Delivery:* regression risk carried silently. *Governance:* an approval granted on evidence that does not address the claim.

**Detection signals.** A criticality class with no stated validation level · static analysis as the gate · no measurement for a performance claim · no drill for a recovery claim · a pilot environment of a different class · behaviour dependent on controls absent from the test environment.

**Decision impact. State the required validation level per commitment, and budget it in the option.** Where the required level cannot be reached — no representative managed test environment, no drill — the corpus's composed disqualifier applies: *"Production commitment cannot be evidenced; do not encode 'ready' from limits alone"* (`architecture-patterns.md` §13). That is a RISK to surface, and for a mission-critical workload it is a gate.

**Better alternatives.** The four-level model applied explicitly; a bounded pilot with monitoring at representative volume and model complexity; a pro-dev functional/regression harness where criticality justifies it; timed restore and failover rehearsals with owners; production throttling monitoring plus a documented degradation plan.

**Exceptions.** Departmental class, where V1 plus user feedback is proportionate — provided the commitment made matches (→ AP-D-039).

**Evidence.** `alm-devops.md` (the four-level validation model V1 documentation/limits, V2 bounded pilot with monitoring, V3 pro-dev automated harness, V4 managed-test fidelity). **Citation repaired 2026-09-03:** this entry previously cited `integration-architecture.md` §15.8, which does not exist — that file has fourteen sections. The dangling citation is inherited from `architecture-patterns.md` and `performance-scale.md`, which carry it too; it is an Areas 1–12 defect recorded in §9 and **not** repaired here; `alm-devops.md` ALM-16, ALM-17, ALM-A12, §4 rows 11, 14, §14.3; `performance-scale.md` PF-15, PF-20, PF-AP-17, PF-C-03, §8.1 items 5, 17, §11.2; `operations-support.md` OP-18, OP-AP-09, OP-AP-16, `operations-support.md` DC-07, OP-C-03, OP-U-03, §13.5; `platform-suitability.md` PS-53, §9 (validation list); `architecture-patterns.md` §13 (4th composed disqualifier, Validation contract); `application-architecture.md` §9.

**Confidence:** MEDIUM (level model is INF; every tool limit is MS).

---
### 5.9 Operations

#### AP-D-053 — Business-critical application with no monitoring and no incident owner

**Description.** A workload the business depends on has no named owner, no alert route to a shared destination, and no runbook — because none of those is provided by default and nobody's role included creating them.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Business-critical class plus any of: no named business, application and platform owner; alerts to individual mailboxes; no runbook; no pre-granted read access for whoever is on call; observability assumed to exist.

**Why it fails.** *"There is no default owner, no default alert and no default runbook"*, and suspension notices go to **individual mailboxes** — including a leaver's, which is exactly the case in which the automation is about to be suspended. Nothing is monitored by default: telemetry export needs a managed environment, the aggregated surface needs tenant analytics enabled, and per-app insights need both a tenant setting and a per-app connection string. The observability that would explain a slowdown is **gated and lossy**, and the only transactional record expires in 30 days. Vendor support does not close this gap: **a support plan is a separate purchase**, **end users cannot raise tickets**, there are no root-cause analyses *"as part of any support experience"*, there is a four-hour cap on performance and non-reproducible cases after which the case closes, and no help with corrupted data — so **an internal first line is mandatory**.

**Consequences.** *Business:* an outage nobody notices until customers do. *Operations:* diagnosis attempted with no telemetry, no baseline and no runbook. *Data:* silent non-processing discovered downstream. *Governance:* no accountable party when a regulator asks.

**Detection signals.** No named owner · alerts to a person · no runbook · no support plan · managed-environment features assumed but unlicensed · "the maker knows how it works".

**Decision impact.** Named business, application and platform/operations owners; alerts to a shared destination with pre-granted environment read access; an internal first line; and **the support tier derived from the criticality**, not from the licence count. Observability depth is a licensing decision taken in option selection — if managed environments are out of scope, **the support model must state that diagnosis capability is materially reduced**.

**Better alternatives.** Named ownership with attestation; shared alert destination; telemetry export where criticality justifies it; internal root-cause capability with the telemetry to support it; a partner or engineering capability for customised and performance cases; correlation identifiers across boundaries for the enterprise class.

**Exceptions.** The departmental class, where users *are* the monitoring — legitimate, and over-engineering it is its own anti-pattern (→ AP-D-039).

**Evidence.** `operations-support.md` OP-03, OP-04, OP-05, OP-08, OP-11, OP-24, OP-25, OP-AP-01, OP-AP-02, OP-AP-03, OP-AP-13, OP-AP-20, `operations-support.md` DC-01, DC-02, DC-13, DC-14, §1.1, OP-C-04, OP-U-07; `licensing-cost.md` LC-22, LC-23, §7.2 items 39, 46; `governance.md` GOV-13, GOV-A8; `automation-architecture.md` AT2-42, AT2-61, N-10, N-11; `performance-scale.md` §11.2.

**Confidence:** HIGH.

---

#### AP-D-054 — Recovery assumed rather than designed and drilled

**Description.** The recovery position is inherited from the platform's marketing surface rather than designed: backups assumed sufficient, restore assumed clean, regional resilience assumed present, and none of it rehearsed.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A recovery objective with no designed procedure; backups treated as archive or legal hold; regional resilience assumed without the opt-in; no drill; artefacts outside solutions expected to be covered; no reconciliation step for integrated systems after a restore.

**Why it fails.** Every assumption is documented as false. **Backups**: 7 days by default, 28 only for a *production managed* environment, **trial environments not backed up at all**, same-region, not downloadable — *"not a retention mechanism"*. **Restore**: cannot target production directly, is managed-to-managed and same-region, needs free capacity (and capacity overage **blocks it**), can take **more than a day**, and its side effects are extensive (see AP-D-045). **Regional resilience**: opt-in, production-only, managed-environment-gated, doubles storage consumption from the tenant pool, takes up to 48 hours to enable, **degrades high-volume automation throughput**, has **no published recovery-time commitment**, has **no prescriptive test plan**, permits **no deployments while failed over**, several geographies have no option at all, and a set of adjacent services (analytical replication, agent runtime, business events and others) is **not covered**. **Coverage**: only artefacts *in solutions* are covered. **Integration**: a restore rewinds one participant while everything integrated retains later state, so a post-restore reconciliation step is mandatory and needs a business sign-off owner.

**Consequences.** *Business:* an unrecoverable loss, or a recovery that takes an order of magnitude longer than promised. *Data:* divergence between the restored environment and every integrated system and replica. *Operations:* a manual multi-step procedure attempted for the first time during an incident. *Cost:* capacity headroom discovered to be a recoverability prerequisite at the worst moment.

**Detection signals.** A recovery objective with no procedure · "it's backed up" as the answer · resilience assumed without the opt-in · no drill history · non-solution artefacts in scope · no reconciliation owner · tenant headroom below the blocking threshold.

**Decision impact.** Recovery is a **designed, rehearsed procedure with an owner**, and its prerequisites (environment class, licence tier, capacity headroom, solution-awareness) belong in the option's cost. Where a contractual recovery time is required, it must rest on **the customer's own drill evidence**, because the platform publishes none — and where the geography has no cross-region option, the residency-versus-resilience trade-off must be surfaced rather than resolved silently.

**Better alternatives.** A rehearsed runbook covering reconnection, re-enablement, re-sharing, republishing and integration reconciliation, with owners and measured elapsed times; drills on a recommended cadence; connectors audited for region-pinned endpoints; capacity headroom as a standing precondition; evidence written into business records where retention beyond the native window is required.

**Exceptions.** Departmental class with an accepted loss position, stated explicitly.

**Evidence.** `operations-support.md` OP-03, OP-14, OP-15, OP-17, OP-18, OP-19, OP-22, OP-AP-08, OP-AP-09, OP-AP-10, `operations-support.md` DC-05, DC-06, DC-07, DC-08, §6.2, §6.3, OP-C-02, OP-U-03; `performance-scale.md` PF-39, PF-40, PF-41, PF-43, PF-44, §3.D, §8.1 items 28–36, DC-13, DC-14, DC-15; `licensing-cost.md` LC-24, §7.2 items 37–38; `data-architecture.md` DA-18, DAP-14; `alm-devops.md` ALM-18, §14.4; `governance.md` GOV-21, GOV-XB-04; `platform-suitability.md` PS-37, PS-52, U-6, U-12; manifest NB-03.

**Confidence:** HIGH.

---

#### AP-D-056 — Platform commitment quoted as the solution's commitment

**Description.** A platform service's availability figure — or its support commitment — is presented as the availability or support position of the whole solution, ignoring every dependency on the path and every part the customer operates.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** An availability number quoted for a composite solution; a support severity commitment cited as the incident-resolution position; dependencies on the critical path not enumerated; customer-operated components in the path; external systems in scope of an availability claim.

**Why it fails.** Manifest reservation **NB-03** states it: platform service availability **does not equal an end-to-end contractual solution availability**, and dependency and contractual scope remain engagement-specific. The corpus is specific about what falls outside: external-system recovery objectives are *"explicitly outside Power Platform's resiliency commitments"*; the platform's commitments *"stop at the platform boundary"*, with analytical replication, agent runtime, business events and other services **not covered**; the governing figure is the **weakest link including the parts the customer operates**, and the gateway host is one of those, with the vendor stating it *"doesn't investigate poor performance when a gateway … is overloaded."* On support, the two statements must be read together: a Severity A case means *"you commit to continuous, 24x7 operation, every day with the Microsoft team until resolution"*, while performance and non-reproducible cases are capped at **four hours** and then closed — and preview features are *"excluded from the Service SLAs"*. The corpus's instruction is direct: **rate each flow, analyse failure modes per flow, and record the weakest dependency as that flow's real objective — never quote platform figures as the solution's.**

**Consequences.** *Business:* a contractual commitment that cannot be met and was never underwritten. *Operations:* an incident whose resolution path was assumed to be the vendor's. *Governance:* an assurance statement to a regulator built on the wrong scope. *Architecture:* dependencies never analysed, so no resilience design exists where it is needed.

**Detection signals.** An availability percentage quoted for the whole solution · no dependency inventory per business flow · external or customer-operated components on the path with no stated availability · a recovery-time figure in a contract · vendor support cited as the incident plan · preview components on a path with an availability claim.

**Decision impact.** Availability and recovery are analysed **per business flow, not per platform**, and the flow's objective is the **worst dependency on its path**. Where a contractual commitment is required, it must be constructed from parsed service terms plus the customer's own drill evidence plus each dependency's position — or the commitment must change. This is one of the decision-blocking criteria (DC-D-100, DC-D-091).

**Better alternatives.** Per-flow dependency mapping with a stated objective per flow; parsed applicable service terms for the specific services in scope; drill evidence owned by the customer; an internal first line with root-cause capability; no preview components on committed paths (→ AP-D-057).

**Exceptions.** A single-service, single-region, no-external-dependency flow — where the platform figure genuinely is the flow's ceiling, still subject to the customer's own contractual parsing.

**Evidence.** `operations-support.md` OP-19, OP-24, OP-25, OP-AP-13, OP-AP-14, `operations-support.md` DC-08, DC-13, DC-14, §6.4, OP-C-04, OP-U-01; `performance-scale.md` PF-40, PF-44, §3.D row 37, §8.1 items 32–33, §11.2 (four-hour case), DC-13; `platform-suitability.md` PS-37, PS-52, U-12, §2 row 21; `integration-architecture.md` IA-27, IA-28, §2.1 row 10, §7 item 28; `security.md` "Cross-block availability boundary"; `data-architecture.md` §2 row 15; manifest NB-03.

**Confidence:** HIGH.

---

#### AP-D-057 — Preview or unsupported components on a critical path

**Description.** A capability marked preview, in early access, or otherwise outside the support and service commitments is placed on a path the business depends on — or used as the basis of an assurance statement.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Any preview or early-access component on a business-critical path; a preview capability cited in an assurance or compliance artefact; a control whose enforcement is preview relied upon as enforcing; a design depending on a capability whose general-availability state is `UNKNOWN`.

**Why it fails.** Preview capabilities are *"Provided as-is, with all faults, and as available… **excluded from the Service SLAs**"*, with English-only, business-hours break-fix support, and previews default to particular regions — which matters directly for a regulated workload. The corpus also holds concrete instances where a *control* is preview and therefore cannot be the control: endpoint filtering is preview, covers a handful of connectors, and is **not enforced** for environment variables, custom inputs or runtime-computed endpoints; the security score is preview and *"for evaluation purposes only at this time"*, refreshes daily and is actionable only on managed environments — so it *"must not be used as the assurance artefact"*. Several cost meters are preview with billing caveats, so an economic case can rest on a preview artefact (→ AP-D-055). And a set of general-availability states is `UNKNOWN` in the corpus itself — the high-volume table type, the bespoke external-site and code-app surfaces, the server-logic capability — which the corpus handles by keeping those fit verdicts **CONDITIONAL** until confirmed in a browser.

**Consequences.** *Business:* a dependency with no service commitment and limited support hours. *Compliance:* an assurance built on a mechanism explicitly labelled non-authoritative. *Operations:* a component that can change or disappear without the normal deprecation path. *Cost:* a business case resting on preview billing behaviour.

**Detection signals.** Preview or early-access labels on components in the design · a control whose enforcement scope is preview · an assurance artefact citing a preview score · a general-availability state nobody has verified · region defaults unexamined for a regulated workload.

**Decision impact.** No preview components on committed paths. Where a requirement can *only* be met by a preview capability, the honest outputs are: proceed with an explicitly accepted, owner-named risk and a dated re-verification; change the requirement; or select an option that does not depend on it. Where the general-availability state is unverified, the fit verdict stays **CONDITIONAL** — the corpus's own gate condition, not an optional refinement.

**Better alternatives.** Supported, generally-available components on critical paths; assurance built from configuration evidence and audit exports rather than from a preview score; a dated re-verification obligation where a preview dependency is accepted.

**Exceptions.** Non-critical paths, pilots and deliberate early adoption with an accepted risk and a named owner — which is a legitimate strategy, not this anti-pattern.

**Evidence.** `operations-support.md` OP-AP-14, `operations-support.md` DC-13, §6.4, §6.5; `security.md` SEC-25, SEC-35, SEC-A9, SEC-A12(context), §4 rows 14, 18, SEC-U-02, SEC-U-06, SEC-U-09, SEC-C1; `governance.md` GOV-A12, GOV-U-06; `licensing-cost.md` LC-AP-06, §7.1 item 10, §7.2 item 47, LC-U-09; `application-architecture.md` U-C6, AA-C10, §9 conditions 2, 4, 6; `data-architecture.md` C-02, U-02, U-06, VT-12 (preview); `platform-suitability.md` U-16, PS-53.

**Confidence:** HIGH.

---

#### AP-D-058 — Unmanaged platform-change exposure

**Description.** No one tracks the platform's mandatory release cadence, deprecation register or component retirements, and no budget exists for the remediation they force — while parts of the estate depend on components already announced as retiring or unmaintained.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** No named owner for platform-change tracking; no recurring remediation budget; a long-lived solution with change-control expectations incompatible with mandatory waves; dependencies on components announced as deprecated or unmaintained; governance or delivery tooling built on an unmaintained accelerator.

**Why it fails.** The change stream is **mandatory and continuous**: two release waves a year cannot be declined, and *"assuming behaviour can be frozen"* is itself a named anti-pattern; the deprecation register is *"continuous and dated"*, and *"several items delete or silently break things"*. Concrete instances already in the corpus: the previous governance accelerator *"is no longer actively maintained… Issues are no longer reviewed or addressed"*, while itself being built from components subject to the same deprecation stream; the previous delivery accelerator is deprecated and unmaintained; the previous low-code test framework is deprecated, leaving no supported first-party functional-test framework; a bundled credit allocation has a **dated removal**; an identity service for external consumers closed to new tenants, changing the recommended path; and mobile deep links were noted as breaking on a dated change without an environment identifier. Two facts the corpus records that make this a cost line rather than a risk register entry: technical debt is named as a performance-efficiency concern by the vendor, and remediation is *"a recurring, unavoidable line"*.

**Consequences.** *Business:* unplanned remediation competing with roadmap work, indefinitely. *Operations:* a silent break on a date the vendor published and nobody read. *Delivery:* tooling that must be replaced mid-engagement. *Cost:* an unbudgeted recurring line (`licensing-cost.md` LC-29).

**Detection signals.** No named owner for change tracking · no remediation budget line · a five-year-plus expected lifetime with a "no change" expectation · a dependency on an accelerator or framework already announced as unmaintained · a bundled entitlement with a removal date in the business case.

**Decision impact.** A **standing duty with a named owner** monitoring the change and deprecation streams, plus a **recurring remediation provision** in the business case, plus a preference for supported non-preview components on critical paths. Where the sponsor wants productivity-workload economics with a mission-critical lifecycle, the corpus's instruction is to **name the contradiction** rather than absorb it. Existing accelerator dependencies are recorded as **technical debt with a migration path**, not as a working capability.

**Better alternatives.** In-product capabilities over custom or community tooling — *"Prioritize the built-in features of the platform… instead of building your own tools"*, with custom tooling re-evaluated as features arrive; a dated migration plan off unmaintained components; early-access wave regression dry-runs; a preference for the vendor's supported path.

**Exceptions.** Short-lived solutions whose life ends before the next wave — legitimate, and worth stating explicitly so the exception is a decision.

**Evidence.** `operations-support.md` OP-26, OP-27, OP-28, OP-AP-12, OP-AP-18, `operations-support.md` DC-18, DC-20, §6.5; `licensing-cost.md` LC-14, LC-29, LC-AP-06, §14.4 (volatile/deprecation register), §7.2 items 29, 48; `platform-suitability.md` PS-50, AP-16, §2 row 31, §3; `governance.md` GOV-02, GOV-12, GOV-A11, GOV-C1; `alm-devops.md` ALM-17, ALM-22, ALM-A13; `application-architecture.md` AA-05, AA-09, AA-18, AA-C5, AA-C6, AA-54, §9 condition 6; `data-architecture.md` C-04, SY-01/U-38 (point-in-time negative finding to re-check per engagement).

**Confidence:** HIGH.

---

#### AP-D-067 — No retirement lifecycle

**Description.** The solution has no defined end: no retirement stage, no decommissioning checklist, no owner for the data, and no periodic review to find what is no longer used.

**Classification:** **CONSTRAINT** (reclassified 2026-09-03 — always wrong within its scope; see §2) · **Origin:** INF over MS facts

**Trigger conditions.** No retirement stage in the lifecycle; no owner for end-of-life data; no periodic review of usage; unused artefacts and environments present in the estate.

**Why it fails. No retirement process is documented**, and the platform's response to abandonment is **silent disablement** rather than removal — so nothing prompts a decision. Meanwhile unused resources are **invisible to the monitoring surface but still consume capacity**, contributing to the ceiling that **blocks restore, copy, recover and environment creation**. The platform supplies fragments — quarantine (administrator-only), inactivity and orphan detection (weekly, managed environments only), automatic deletion of developer environments after 90 days, and a documented move-out procedure — so retirement is *"a process with platform support, not a platform feature"*, which means it must be designed. The corpus also records that the *data* question is separate and harder: retention and deletion decisions are stamped at write time, retention changes are non-retroactive, and backups are not an archive — so "we'll deal with the data at retirement" is not available.

**Consequences.** *Cost:* capacity consumed by dead assets, and entitlements assigned to them. *Operations:* recoverability blocked by dead weight; an estate nobody can inventory meaningfully. *Governance:* orphaned artefacts indistinguishable from live ones; data retained past its lawful basis. *Security:* dormant surfaces with dormant credentials.

**Detection signals.** No retirement stage in the lifecycle model · artefacts with no usage and no owner · developer environments approaching automatic deletion with work in them · capacity headroom shrinking with no growth in live use · data retention decisions never made.

**Decision impact.** An explicit retirement stage with a **checklist and an owner**, plus a periodic review using the inventory and usage surfaces, plus a **data disposition decision made at design time** (retention scope, audit scope, deletion policy) because several of those decisions are non-retroactive or stamped at creation.

**Better alternatives.** A lifecycle model with a retirement stage; scheduled inventory and usage review; the documented move-out and quarantine mechanisms used deliberately; retention and deletion decided at environment and table creation; a dated decommissioning plan for anything replaced.

**Exceptions.** None in principle. The *depth* scales with class — a departmental tool needs a decision and a delete, not a programme.

**Evidence.** `operations-support.md` OP-28, OP-22, OP-AP-15, OP-AP-19, `operations-support.md` DC-19, §2.6, §6.5; `governance.md` GOV-17, GOV-A7, §2, §4 row 14; `data-architecture.md` DA-16, DA-17, DA-18, DAP-13, DAP-14, DAP-15, DAP-29, U-16, §2 row 12, §3; `licensing-cost.md` LC-05, LC-AP-03, LC-AP-13; `alm-devops.md` ALM-25.

**Confidence:** MEDIUM (facts MS; the "designed retirement" conclusion is INF).

---

### 5.10 Cross-cutting

#### AP-D-059 — Composed disqualifier ignored

**Description.** Every dimension of an option is assessed individually as CONDITIONAL, each with a stated mitigation, and the option is approved — while the *combination* of those conditions makes it unavailable.

**Classification:** **GATE** (reclassified 2026-09-03 — see §2) · **Origin:** INF over MS facts (the corpus's own composed-disqualifier set)

**Trigger conditions.** Any of the corpus's documented combinations, assessed dimension-by-dimension:

| Combination | Consequence | Class |
|---|---|---|
| Strict cross-system atomicity + more than one transactional owner + no acceptable compensation window | No pattern supplies the atomicity; collapse to one owner or move the responsibility | POOR FIT |
| A pattern requiring an external component + no named operator, on-call or release owner | **Pattern unavailable, not merely expensive** | ANTI-PATTERN |
| Private-network / key-control / firewall requirement + no budget or entitlement for the managed environment and external licence prerequisites | Security requirement and commercial constraint are **incompatible** with the proposed design | CONSTRAINT |
| Business- or mission-critical + no representative managed test environment + no recovery drill | Production commitment **cannot be evidenced**; do not encode "ready" from limits alone | RISK |
| High-frequency custom-connector workload + sizing resting on either side of the open conflict, unmeasured | Sizing is **decision-blocking** | VOLATILE VALUE / CONFLICTED |
| Per-user backend authorization required + facade or worker calling downstream as a shared service identity | Pattern **changes the authorization semantics** and is unsuitable unless identity is propagated | DECISION CRITERION |
| Hybrid architecture required + no pro-dev or enterprise-platform capability available | Platform-only implementation is the wrong fit; acquire the capability or select another architecture | POOR FIT |
| Replication + no reconciliation owner + recovery/restore requirement | A routine restore can create **unowned data divergence**; pattern unavailable for material data | ANTI-PATTERN |

**Four further combinations, added by Block D** (2026-09-03). The first eight rows are `architecture-patterns.md` §13 transcribed. These four are derived from the same corpus but are not enumerated there; they are marked so a reader can tell inherited rows from derived ones. **The register is 8 + 4 = 12, and `decision-intelligence-matrix.md` §3 and `decision-criteria.md` §2.4 carry the same 12.**

| Combination | Consequence | Class | Derived from |
|---|---|---|---|
| Criticality class **two or more levels above** the demonstrated operating maturity, with no funded plan to close the gap | The commitment **cannot be delivered in any architecture**; the gap is a sponsor decision, not a design one. Options carrying an external component are additionally unavailable | POOR FIT | `operations-support.md` §1.1; `architecture-patterns.md` §5.1 (operational-maturity row); DC-D-001 × DC-D-104 |
| Offline write + field-level security · **or** offline + non-governed data beyond the documented bound · **or** mobile-first + device hardware + branded distribution with push | Each is a **documented mutual exclusion**; the combination is unsatisfiable in-platform, so no mitigation sequence exists | ANTI-PATTERN (AP-D-003) | `application-architecture.md` AA-40, AA-42…AA-44, AA-46; DC-D-016 × DC-D-026 × DC-D-015 × DC-D-020 |
| **Citizen-built artefacts outside a solution, in the default environment, with the criticality class now business-critical or above and the original maker gone** | The workload **cannot be brought to the required class in place**: non-solution artefacts are excluded from backup, ineligible for capacity licences and undeployable; a non-solution automation's **owner cannot be changed at all**; the departed maker's automation profile has already reverted. The outcome is **migration, not remediation** — and the remediation estimate a sponsor is usually given is for the wrong work | ANTI-PATTERN (AP-D-036 × AP-D-040 × AP-D-047 × AP-D-066) | `governance.md` G-03 (default-environment exposure); `operations-support.md` O-05, O-10; `alm-devops.md` ALM-14; DC-D-006 × DC-D-001 × DC-D-074 |
| **Continuous change frequency + two or more concurrent makers + no pro-code capacity to reach the source-controlled rung** | No isolation mechanism is available at any rung the organisation can reach: *"Every modification is applied directly to the environment, regardless of which solution is being edited"*, canvas co-authoring was removed, and the isolating rung requires developer environments per maker **plus** pro-dev capability that DC-D-110 gates. **Overwriting is the documented outcome**, and there is no supported first-party functional-test framework to catch it | POOR FIT / RISK | `alm-devops.md` ALM-06, ALM-17, ALM-23, §4 rows 3 and 11; `application-architecture.md` AA-06; DC-D-007 × DC-D-078 × DC-D-110 |

**Why the last two matter more than their position suggests.** They are the only two composed rows drawn from **Governance** and **ALM** — the two domains that produce **zero direct exit signals** (`decision-criteria.md` §9 item 5). A domain that cannot reject the platform on any single criterion was, before this repair, also contributing nothing to the one test designed to catch exactly that situation, so its combinations were invisible to the whole model. *Citizen development becoming business-critical* is arguably the most common real engagement in this domain, and it previously had no rule — only four separately-detected anti-patterns whose conjunction nothing tested.

**Why it fails.** A per-dimension assessment is a **conjunction, not a sum**. Each CONDITIONAL verdict carries a mitigation, and the mitigations can be mutually exclusive (private egress *and* platform-native eventing), or can all depend on one absent resource (an operator, a budget, a test environment), or can each individually be affordable while their combination is not. The corpus assembled the inherited set precisely because *"every individual dimension looks merely CONDITIONAL"* — and three of those eight rows, plus three of the four added, conclude that the option is **unavailable** or **undeliverable** rather than expensive, which no per-dimension score would ever produce.

**Consequences.** *Architecture:* an option approved that cannot be built as specified. *Business:* a commitment that fails at the first combination test. *Cost:* the true cost appears only when the mitigations are all funded. *Governance:* an approval whose basis was never a whole-option assessment.

**Detection signals.** Several CONDITIONAL verdicts on one option · mitigations that each name a resource nobody has confirmed · two mitigations that cannot both be true · an option summary that lists conditions but never tests them jointly · the same missing role (operator, cost owner, reconciliation owner) appearing in more than one mitigation.

**Decision impact.** After per-criterion assessment, run the **composed test** explicitly. Where a documented combination is present, the outcome is drawn from the **closed outcome set** in `decision-criteria.md` §6.2 and from nowhere else — **the reachable class is named per row**, not one class for every composed match, because the twelve rows do not share one consequence: `decision-intelligence-matrix.md` §3's Class column is the authority (Repair V3, 2026-09-03 — `block-d-gate.md` finding G-M-02: a single global mapping had left at least one registered row, this entry's own per-user-authorization row, with no valid class to route to). In practice this reaches class 2 **FIT WITH CONSTRAINTS** (the per-user-authorization row, where the named condition is satisfied), class 5 **POWER PLATFORM — POOR FIT**, class 7 **ECONOMICALLY UNATTRACTIVE OR INFEASIBLE** (the unfunded-control row), class 11 **DO NOTHING / DEFER** or class 12 **DECISION BLOCKED — MORE EVIDENCE REQUIRED**, class 14 **IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED**, or an option redesigned to break the combination. Where the row's outcome is class 5, 6, 7 or 14, the terminal statement additionally carries class 8 **CANDIDATE SET — COMPARATIVE FIT UNEVALUATED**: the composed test can say the option is unavailable, and it cannot say which surviving class is better. **This test must not be replaced by a score** — this is a direct instance of why Block D deliberately produces no scoring model: a weighted average of eight CONDITIONALs would pass an option the corpus says is unavailable.

**Class 5 and class 14 are not the same conclusion, and the distinction is this entry's own (added 2026-09-03).** Three of the twelve rows conclude the option is **unavailable** — no architecture delivers it — which is class 5. The citizen-development row concludes something narrower and more commonly mishandled: the workload cannot be brought to the required class **in place**, while the same platform **rebuilt** remains a legitimate candidate. That is class 14, and emitting class 5 for it would reject a platform the row does not reject. Where a row's consequence names what cannot be *repaired* rather than what cannot be *built*, the class is 14.

**The register is closed at twelve, and `decision-criteria.md` §2.5's `Xc` class depends on it.** A criterion may carry `Xc` only if it is named in a row above or in `decision-intelligence-matrix.md` §3 — eight do (DC-D-001, 015, 037, 063, 064, 068, 080, 104; DC-D-068 added 2026-09-03, Repair V3 — it was already named in the per-user-authorization row above, but no criterion's own class had routed to it until `decision-criteria.md` §2.5 moved DC-D-068 from `Xr`). Criteria whose bodies say *"combines with…"* against a combination this register does **not** carry are `Cf` (combination inputs), not exits; V1 flagged eighteen of them `Xc`, which promised an exit this test could never run. Extending the register to make those flags resolve would have been invention — the corpus registers twelve combinations, not thirty.

**Better alternatives.** Break the combination (collapse the transaction owner, acquire the operator, fund the entitlement, reduce the atomicity requirement); select an option whose conditions do not interact; escalate the missing resource as a decision for the sponsor rather than an assumption.

**Exceptions.** None — but the combinations themselves are the exception boundary: a single CONDITIONAL with a funded, owned mitigation is an ordinary conditional fit, not a disqualifier.

**Evidence.** `architecture-patterns.md` §13 (all eight rows), §5.1, Y-13; `integration-architecture.md` §12.3; manifest **NB-02 / `IA-C-01`** (= `integration-architecture.md` `C-01`) and **NB-01 / `IA-U-14`** (= `U-14`) — the qualified forms are canonical per `pre-canonicalization-repair.md`, and the mounted snapshot carries the unqualified ones; `security.md` SEC-XB-01, SEC-XB-02, SEC-XB-04; `licensing-cost.md` LC-30; `alm-devops.md` §14.2, §14.3; `operations-support.md` §1.1, §13.5; `governance.md` GOV-XB-01, GOV-XB-04; `data-architecture.md` SY-14; manifest NB-01, NB-02, NB-04, NB-07.

**Confidence:** MEDIUM (the individual facts are MS; the composition is the corpus's own INF synthesis).

---

### 5.11 Cost

#### AP-D-060 — Licence line treated as the total cost of ownership

**Description.** The business case prices licences and calls it the cost, omitting the other lines the vendor states but does not price — and, in a hybrid, omitting the other platform entirely.

**Classification:** ANTI-PATTERN · **Origin:** MS (each omitted line) + INF (the assembly)

**Trigger conditions.** A business case whose cost section is a licence count; no non-production estate, monitoring, support plan, storage, migration, testing, training or technical-debt line; a hybrid option costed only on the low-code side; a "cheap to build" comparison against an alternative costed over its full life.

**Why it fails.** The structural finding frames it: **there is no cost-optimization pillar for this platform** — only for the cloud platform — so cost is *"not systematically challenged in the way reliability and performance now are"*, and the cost statements are scattered as incidental callouts inside performance and reliability guidance. Assembled, they show a licence-only case omits **at least eleven other lines**: non-production estate (*"There are costs associated with maintaining separate test environments, storing data, using tooling, and running tests"*), storage across three separately-metered types **including audit and index, which no user licence funds**, environment count × the per-environment storage floor, monitoring and telemetry (*"Logic monitoring tools are likely to increase costs"*; *"There are cost implications for storing and querying logs"*), the **separately purchased** support plan, external and hybrid service consumption, migration, training, optimisation effort, deprecation-driven remediation, and technical debt. The hybrid case is explicitly out of scope of a low-code-only costing: the external estate imports *"Azure/on-premises consumption and administration"*. And the comparison must be **symmetric** — the corpus rejects row-level "where Power Platform is favoured" claims as *"too weakly evidenced on the comparator side"* and replaces them with a **method** comparing the same ten dimensions for every candidate.

**Consequences.** *Business:* an approved case that is wrong by a large multiple, discovered after commitment. *Governance:* an option comparison that is not like-for-like. *Delivery:* unfunded work (test environments, telemetry, migration) descoped under pressure — usually the operational work. *Cost:* a "cheap" option that is the expensive one.

**Detection signals.** A cost section that is a licence table · no support-plan line for a business-critical workload · no storage or audit-capacity line · a hybrid option with one platform's cost · an alternative dismissed on price with no TCO comparison · no do-nothing baseline.

**Decision impact.** Price every option on the **same ten dimensions** (audience; machine workload; data; security prerequisites; environment/lifecycle; external estate; observability/support; build/change effort; existing sunk capability; exit/option value), and carry the do-nothing and process-change baselines. The corpus's rule is explicit: *"Price Power Platform with the full TCO lines, not the licence line"*, and *"do not demand exhaustive proof from non-Power-Platform options while accepting broad claims"* for the incumbent choice.

**Better alternatives.** The ten-dimension comparison method; a translated cost-review discipline borrowed from the cloud platform's pillar (the corpus does this explicitly and marks it INF); a dated business case with the volatile commercial facts flagged for revalidation at decision, implementation and renewal.

**Exceptions.** A genuinely trivial workload on existing entitlement with no new environment, monitoring, support or storage implication — where the licence line really is the cost, and saying so is a finding.

**Evidence.** `licensing-cost.md` LC-01, LC-21, LC-22, LC-26, LC-27, LC-28, LC-29, LC-AP-04, §0.4, §1, §2.5, §6, §7.1 items 1–2, 5, §7.3 item 51, LC-U-04, `licensing-cost.md` DC-15; `performance-scale.md` §11.1; `operations-support.md` §9.2; `architecture-patterns.md` §5.1 (budget row); `automation-architecture.md` AT2-53, N-51; `integration-architecture.md` §12.9 ("A preference for code" cuts the other way).

**Confidence:** HIGH.

---

#### AP-D-061 — Licence-avoidance architecture

**Description.** The data store, connector, ownership model or identity design is chosen to keep a licence line low, and the resulting workaround cost is never stated alongside the saving.

**Classification:** ANTI-PATTERN · **Origin:** INF over MS-documented mechanisms

**Trigger conditions.** A design choice whose primary justification is avoiding an entitlement: a document/spreadsheet store instead of a relational one; a shared identity instead of per-user licensing; a non-premium owner for a high-volume automation; avoiding the managed environment class to avoid premium licences; a free-tier start for something with a path to criticality.

**Why it fails.** Four documented cases, each *"a rational local optimisation that produces a globally worse system"*, and the pattern is always the same — *"a licence line is visible and a workaround cost is not, so the invisible cost wins the decision."* (1) The cheap store carries the documented performance, integrity, security and delegation penalties of AP-D-008. (2) The shared identity is **licence multiplexing**, which is prohibited and carries a documented right of suspension, and collapses throughput onto one budget (AP-D-032). (3) The cheap automation owner buys a profile with **50× less** request entitlement and content throughput, fewer retries, a higher postpone floor, a 90-day inactivity suspension and profile reversion when the owner leaves (AP-D-066). (4) **Avoiding the managed environment class** forfeits telemetry export, extended backup, cross-region recovery, pipelines and network isolation — *"i.e. the means of diagnosing and recovering from incidents. The saving returns as outage duration."*

**Consequences.** *Cost:* higher total cost by a different route, plus a possible remediation migration. *Operations:* diagnosis and recovery capability traded away. *Security:* a contractual exposure. *Data:* the integrity and correctness penalties of the cheap store.

**Detection signals.** A store or ownership choice justified by licence cost · licence arithmetic implying shared identities · a business-critical automation owned by a personal non-premium account · managed environments explicitly excluded for cost with no consequence statement · a free-tier start for a solution with a growth path.

**Decision impact. Whenever a design choice is justified primarily by licence avoidance, require the workaround cost to be stated explicitly alongside the saving** — extra storage, extra synchronisation runs, extra build effort, forfeited operational capability, migration risk. If the workaround cost exceeds the saving, the licence is the cheaper option. If the saving is genuinely necessary because the budget is fixed, the honest outputs are a reduced scope, a different option class, or `decision-criteria.md` §6.2 class 7 **POWER PLATFORM — ECONOMICALLY UNATTRACTIVE OR INFEASIBLE** — not a degraded design presented as equivalent. That class asserts nothing about what any other class would cost: see `decision-criteria.md` §4A.1.

**Better alternatives.** Fund the entitlement where the requirement needs it; reduce scope so the cheaper entitlement genuinely fits; process change; an existing licensed capability; a different platform whose licensing shape matches the workload (`alternatives.md` §5 on the users-to-work ratio, retained as a hypothesis to test).

**Exceptions.** A cheap option that genuinely fits the requirement — a document store for document-centric work, seeded entitlements for a standard-connector workload. That is not avoidance; it is fit.

**Evidence.** `licensing-cost.md` LC-03, LC-23, LC-26, LC-27, LC-AP-01, LC-AP-02, LC-AP-09, LC-AP-10, LC-AP-12, LC-AP-13, §2.6, §7.2 items 34–36; `platform-suitability.md` PS-42, PS-43, AP-5, AP-8, §2 rows 9, 25; `data-architecture.md` DA-43, DA-63, DAP-1, §2 row 25; `performance-scale.md` §11.1 (last row), PF-29, PF-31; `operations-support.md` OP-21, `operations-support.md` DC-16; `governance.md` GOV-06, GOV-11, GOV-C2.

**Confidence:** MEDIUM (mechanisms MS; the framing is INF and engagement-specific).

---

#### AP-D-062 — Entitlement boundary discovered after the design is fixed

**Description.** The design commits to a capability on the paid side of an entitlement boundary — a premium or custom connector, an on-premises data path, a particular application type, an external-facing site, a managed environment — without checking the licence consequence for the **whole** audience.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Any of these in the design with no licence census: a premium or custom connector; an on-premises or cloud-database data path; a model-driven application type; an external-facing site; a managed environment; a capability requiring higher-tier productivity or directory entitlements.

**Why it fails.** The licence boundary **is a fit boundary**: seeded productivity rights cover standard connectors and the team-scoped data store only; premium and custom connectors, on-premises and cloud data transfer, the full data platform, the model-driven application type, external-facing sites and managed environments **all** require standalone entitlement for **every active user** — and **multiplexing is prohibited**, so there is no workaround. The consequence is that a single connector decision can move the entire user population from seeded to paid. Note the residual honesty: whether *one* premium connector obliges premium licensing for *every* user of the artefact is **`LC-U-05` / `LC-C-05`** — stated categorically by independent sources, consistent with the vendor's entitlement statements, but not verbatim-confirmed on a fetched page. It is load-bearing for the corpus's largest cost finding and is a per-engagement verification item, not an assumption.

**Consequences.** *Cost:* a step change in the licence line, discovered after the design. *Business:* an option that becomes economically infeasible late. *Delivery:* redesign, or an unfunded procurement. *Governance:* an entitlement breach if the population is not licensed, with a documented right of suspension.

**Detection signals.** Connector tier unverified against the licence position · audience size not enumerated · an application type or site chosen with no entitlement check · a managed environment in the design with no premium-licence line · "we have Microsoft 365, so we're covered".

**Decision impact. Establish the connector tier and the entitlement consequence at design time, on the whole audience.** Where a standard path meets the requirement, the saving is population-wide; where it does not, the premium cost belongs in that option's economics **from the first comparison**. The corpus's routing rule also applies: entitlement questions go to the authoritative licensing document and the customer's own agreement, with a named owner — the general documentation is explicitly not authoritative on licensing.

**Better alternatives.** A licence census of the full audience during option formation; a standard-connector path where one satisfies the requirement; a consumption-billing model where the audience is large and infrequent; scope reduction; a different option class.

**Exceptions.** Designs entirely inside seeded entitlement, verified rather than assumed.

**Evidence.** `licensing-cost.md` LC-02, LC-03, LC-AP-02, `licensing-cost.md` DC-01, DC-02, DC-03, LC-C-05, LC-U-02, LC-U-05, §7.1 items 2–4, §7.3 items 49–50; `platform-suitability.md` PS-26, PS-42, PS-33, PS-36, §2 rows 9, 22, §3; `governance.md` GOV-06, GOV-11, GOV-18, §4 rows 2, 9; `security.md` SEC-XB-01; `data-architecture.md` DA-43, DA-55, DA-61; `application-architecture.md` §7 (deferred cost cells).

**Confidence:** HIGH on the boundary; the per-artefact obligation is MEDIUM pending `LC-U-05`.

---

#### AP-D-063 — Consumption without an owner or a growth model

**Description.** Metered consumption — requests, storage across its several types, audit and index growth, external service usage — has no owner, no growth model and no threshold, so its first visible symptom is an operation being blocked.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** No named owner for tenant capacity or the shared request pool; sizing on today's average; no audit-scope decision; "audit everything, forever"; no growth or peak forecast; external service consumption with no cost owner.

**Why it fails.** The failure is **not a bill, it is a block**: storage overage *"blocks environment create, copy, restore, recover and Dataverse-add"* — so a capacity problem presents as a **recoverability** problem. Several growth vectors are unfunded or invisible: **no user licence accrues log capacity**, yet auditing consumes it; the search index bills at the **most expensive** rate; every environment consumes a storage floor regardless of database; cross-capacity borrowing is **one-directional**; **retries and pagination are billed as actions**, so an unreliable dependency is a cost driver; entitlements **do not roll over**; the non-licensed request pool is **shared tenant-wide with no project-level view**, so *"one integration's growth silently consumes another project's headroom"*; and external-audience metering counts browser cookies rather than people. Detection is also weak: consumption reporting is **preview and partial**, with documented defects, and capacity notifications begin only when headroom is already low.

**Consequences.** *Operations:* restore and recovery blocked at the moment they are needed. *Cost:* growth in the invisible meters (audit, index, replicas, retries). *Governance:* a shared pool with no owner and no per-project view. *Business:* administrative operations degrading estate-wide because of one project.

**Detection signals.** No named tenant-capacity owner · sizing on today's average · audit scope undecided or unlimited · no forecast for the peak month · external service consumption with no cost owner · capacity notifications already firing.

**Decision impact.** A **named tenant-level owner** for capacity and the shared pool; capacity headroom treated as a **recoverability requirement** with a standing minimum; audit and retention **scoped at creation** because those decisions are non-retroactive; sizing against the horizon and the **peak**, not the average; and lifecycle jobs for binaries and history designed in. Where consumption is decision-critical and unmodellable in advance (agent and AI consumption in particular is explicitly unmodellable before a pilot), it is a decision-blocking unknown closed by a pilot, not an estimate.

**Better alternatives.** Explicit capacity model per meter with growth and peak; scoped audit with a stated retention; binaries in the cheaper file meter and out of the database meter; lifecycle and archival jobs; consumption billing where demand is bursty; cost attribution via the documented per-environment billing mechanism.

**Exceptions.** Small workloads with bounded, forecast growth — provided the forecast exists and someone owns the threshold.

**Evidence.** `licensing-cost.md` LC-05, LC-09, LC-10, LC-11, LC-16, LC-19, LC-20, LC-AP-03, LC-AP-05, LC-AP-07, LC-AP-11, LC-AP-14, §7.1 items 8–9, §7.2 items 11–28, LC-U-08, LC-U-10, `licensing-cost.md` DC-04, DC-07, DC-10; `operations-support.md` OP-22, OP-AP-15, `operations-support.md` DC-04, DC-17, OP-U-04, OP-U-05; `data-architecture.md` DA-14, DA-16, DA-17, DA-19, DA-62, DAP-13, DAP-16, U-01, U-29; `performance-scale.md` §11.1, DC-09, DC-20.

**Confidence:** HIGH.

---

#### AP-D-064 — Operational and security prerequisites omitted from the cost model

**Description.** The security and operational controls the requirement mandates are treated as configuration, when they carry entitlement prerequisites priced by **affected population** — often a larger line than the platform licences themselves.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A mandated control — network firewall, customer-managed keys, private networking, conditional access, extended backup, cross-region recovery, telemetry export, pipelines, desktop-flow policy, lockbox — with no population-based cost line; a criticality classification with no derived licence consequence.

**Why it fails.** Nearly every capability needed to **operate** the platform responsibly sits behind the managed environment class, which requires **premium licences for every active user of that environment** — and several controls additionally require higher-tier productivity, directory or compliance entitlements for users in scope. The unit is therefore **the affected user population, not the number of apps**, which is why *"the security control can create a larger cost line than the platform licence itself"*. The corpus states the causal chain to model: **control → required entitlement → affected population → current customer holdings → incremental cost** — and, separately, *criticality → operational requirements → managed environment → premium licences*. Its instruction on the failure mode is explicit: *"if unfunded, the option is economically infeasible rather than 'secure by configuration'"*, and *"Never remove a required security control merely to make the Power Platform option look cheaper."* Two further prerequisites are commonly missed: cross-region recovery consumes a **second full copy of storage** from the same tenant pool, and a **support plan is a separate purchase** whose tier follows criticality.

**Consequences.** *Cost:* a step change larger than the platform licences. *Security:* pressure to drop the control to save the option — the outcome the corpus explicitly forbids. *Business:* an option approved that cannot be delivered compliantly. *Operations:* the diagnostic and recovery capability descoped to fit the budget (→ AP-D-061).

**Detection signals.** A control mandated in the security schedule with no cost line · criticality classified with no licence consequence · cross-region recovery in scope with no storage-doubling line · no support-plan line · the affected population never enumerated.

**Decision impact.** Model the full chain **during option selection**, because it changes the option's economics, and revalidate at implementation and renewal (these are `VOLATILE VALUE` facts). Where the required control's population is unfunded, the outcome is `DECISION BLOCKED` or a different option class — stated as such. Budget the support tier from the **criticality**, not from the licence count.

**Better alternatives.** Control-to-population cost modelling before accepting the architecture; scope reduction so fewer users are in the governed environment; an option class whose control model does not carry the same population cost; explicit escalation of the funding gap to the sponsor.

**Exceptions.** Controls already funded by existing entitlements — verified against the customer's actual holdings, not assumed from the product tier.

**Evidence.** `licensing-cost.md` LC-22, LC-23, LC-24, LC-30, `licensing-cost.md` DC-11, DC-12, DC-14 (security-controls variant — see §1.4), §7.2 items 34–39; `security.md` SEC-XB-01, SEC-27, SEC-29, SEC-30, §4 rows 9–11; `governance.md` GOV-06, GOV-11, GOV-XB-03, GOV-C2, §4 row 2; `operations-support.md` OP-21, OP-24, `operations-support.md` DC-13, DC-16, OP-C-01; `performance-scale.md` PF-40, PF-41, DC-14, §11.1; `architecture-patterns.md` §5.1 (licence-profile row), §13 (3rd composed disqualifier).

**Confidence:** HIGH on the prerequisite shape; commercial values are `VOLATILE VALUE`.

---

#### AP-D-065 — Cheap start on a path to criticality

**Description.** A solution is started on a free or seeded tier with a plausible route to business-criticality, and the cost, capability and migration consequences of that route are never modelled.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** A free or team-scoped tier chosen for something with a plausible criticality path; no graduation trigger defined; growth toward a documented ceiling with no budgeted upgrade; a proof of concept becoming production by default.

**Why it fails.** The ceiling is not a soft one and the exit is not free. The team-scoped tier **cannot buy more capacity**, and reaching its ceiling **stops new solution creation while data keeps growing**; it excludes the capabilities a maturing solution needs (audit, enterprise lifecycle, custom connectors, log capacity, robotic automation, AI capability); its upgrade is **one-way** and converts **all** users to premium; and export to a full environment *"is not yet available"*, so **the exit may be a rebuild**. The same shape appears at the environment level: the class that unlocks operational capability requires premium licences for every active user, so *"a departmental solution becomes expensive the day it matters."* And the corpus records the general mechanism as a cost line: the migration cost of a *"deliberately-cheap starting point"* is part of technical debt, alongside deprecation remediation and refactoring at structural limits.

**Consequences.** *Business:* a growth stop at the moment of success. *Cost:* an unbudgeted step change, or a rebuild. *Operations:* a critical workload without the operational feature set, because it was never licensed for it. *Data:* migration risk on data that is now business-critical.

**Detection signals.** A free or team-scoped tier with a growth story · no graduation trigger · storage or feature ceilings approaching · a proof of concept in production use · "we'll upgrade if it takes off" with no cost attached.

**Decision impact.** Define the **graduation trigger and its cost at the start**: which measurable condition (volume, criticality, audience, capability need) moves the solution to the next class, what that costs, and what the migration involves — including whether it is a rebuild. Where the criticality path is likely, starting in the target class is often cheaper than the migration. Where the sponsor wants low-tier economics with a critical lifecycle, the corpus's instruction is to **name the contradiction**.

**Better alternatives.** Start in the class the solution will need; define a dated graduation trigger with a budget; keep genuinely departmental work in the cheap tier with a documented ceiling and an accepted stop; process change where the value does not justify the class.

**Exceptions.** Genuinely bounded, short-lived, team-scoped work with no criticality path — the tier's intended use, and over-provisioning it is AP-D-039.

**Evidence.** `licensing-cost.md` LC-14, LC-23, LC-29, LC-AP-09, `licensing-cost.md` DC-11, DC-16, §7.2 items 31–33; `data-architecture.md` DA-13, DA-43, §2 row 22, C-05; `application-architecture.md` AA-50, AP-32, §1 row 6; `platform-suitability.md` PS-16, PS-33, §2 rows 3, 7; `governance.md` GOV-24, §4 row 11; `operations-support.md` §1.1, OP-21.

**Confidence:** HIGH.

---

#### AP-D-066 — Cheap ownership of business-critical automation

**Description.** A business-critical automation is left owned by an individual's non-premium account, so its throughput ceiling, retry behaviour and survival depend on that person's licence and employment.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Business-critical automation owned by a personal or non-premium account; no service-principal or capacity-licensed ownership; the automation not in a solution (which forecloses the remedy); no owner-departure plan.

**Why it fails.** The performance profile **follows the owner's licence**, and the spread is **50× on request entitlement and 50× on content throughput**, plus fewer retries and a higher postpone floor. Worse, it is not stable: *"If the original owner leaves the organization, the flow reverts to the Low performance profile"* — a silent loss of most of the ceiling. Low-frequency automation owned by non-premium identities is **suspended after 90 days of inactivity**, and a non-solution automation's owner **cannot be changed at all**. The remedies are documented but each has a prerequisite: a capacity licence **requires the automation to be in a solution**; service-principal ownership couples licensing to the delivery lifecycle; and service-principal-owned automation draws on a **tenant-shared base pool** unless separately licensed.

**Consequences.** *Business:* an automation that quietly loses 98% of its ceiling, or stops, because of an HR event. *Operations:* the 30-day warning arriving in a departed person's mailbox (→ AP-D-053). *Cost:* the cheap ownership buys workaround effort and a suspension risk. *Architecture:* a design decomposed to fit a ceiling that a licence would have removed.

**Detection signals.** Business-critical automation owned by a named individual · non-premium owner on a high-volume path · automation not in a solution · no ownership entry in the operational model · profile reversion already observed.

**Decision impact. Ownership is an architectural decision**, taken with the design: service-principal or capacity-licensed ownership for business-critical or high-volume automation, which in turn requires solution-awareness from day one (→ AP-D-047). The corpus's framing: *"Business-critical automation → service principal or a capacity licence assigned to the flow."*

**Better alternatives.** Service-principal ownership with a named credential owner and rotation; a capacity licence assigned to the automation (solution-aware); moving the metered data leg to the exempt in-platform mechanism so the ceiling matters less; a documented owner-transfer procedure.

**Exceptions.** Departmental automation where the ceiling and the suspension risk are both acceptable and stated.

**Evidence.** `automation-architecture.md` AT2-01, AT2-44, AT2-46, AT2-51, N-01, N-13, N-15, §9 rows 2, 20; `performance-scale.md` PF-29, PF-31, PF-38, PF-39, DC-18, §8.1 items 18, 25, §11.1; `licensing-cost.md` LC-08, LC-26, LC-AP-12, `licensing-cost.md` DC-08, §7.2 items 42–44; `operations-support.md` OP-04, OP-15, OP-AP-01, OP-AP-11, `operations-support.md` DC-01, DC-10, DC-12; `security.md` SEC-21, SEC-22, §4 row 13.

**Confidence:** HIGH.

---

#### AP-D-055 — Case built on transition-period or preview terms

**Description.** The design or the business case is sized against figures the vendor identifies as transitional, preview, or bundled-and-expiring — and treats them as the steady state.

**Classification:** ANTI-PATTERN · **Origin:** MS

**Trigger conditions.** Sizing against published transition-period request figures rather than official entitlements; a business case resting on a preview billing cap; reliance on a bundled allocation with a stated removal date; a design assuming a manual-automation licensing behaviour that is stated to be changing; any economic dependency on preview terms.

**Why it fails.** The vendor labels these as transitional and instructs building against the official figures: the published daily request figures *"are greater than the documented request limits… during the licensing transition period"*, enforcement has **no announced date** (*"no current ETA"*), and manual automation will move to the **invoking user's** limits. A design sized to transition figures can be an order of magnitude out (the corpus records the two published sets and the resolution rule). Separately: a consumption billing cap is a **preview artefact**, so *"the bill can understate real usage"*; a bundled AI allocation has a **dated removal**; and several core meters remain preview. The structural hazard is that the estate can be **non-compliant with no bill and no error** — so nothing surfaces the problem until enforcement begins.

**Consequences.** *Business:* a case that breaks when enforcement starts, on a date nobody controls. *Cost:* a bill that appears later at a different scale. *Architecture:* a design whose volume assumptions were never valid. *Governance:* an entitlement position that is quietly non-compliant, with a documented right of suspension.

**Detection signals.** Transition-period figures in the sizing · a preview meter or cap in the business case · a bundled allocation with a removal date used as a saving · manual-automation volume sized on today's behaviour · no revalidation trigger on any commercial assumption.

**Decision impact.** Size against **official** entitlements, and flag every dependency on transitional, preview or bundled terms as a **dated assumption with a revalidation trigger**. The corpus's instruction: *"Do not build a business case on transition-period generosity."* Where enforcement timing is decision-critical, it is an open unknown to track, not a figure to adopt.

**Better alternatives.** Official-entitlement sizing with headroom; dated assumptions with named owners and revalidation triggers at decision, implementation and renewal; a capacity or consumption model that does not depend on preview behaviour; tracking the enforcement-reporting status as a standing duty (→ AP-D-058).

**Exceptions.** Explicitly accepting a transitional benefit as a *bonus* rather than a dependency — the case must stand without it.

**Evidence.** `licensing-cost.md` LC-09, LC-19, LC-AP-06, LC-C-01, LC-U-09, §7.1 item 10, §7.2 items 23, 27–30, 47, §14.4, `licensing-cost.md` DC-17; `performance-scale.md` PF-AP-18, PF-C-01, §8.1 items 19, 22, §3.C row 29; `automation-architecture.md` AT2-03, N-03, C-02; `data-architecture.md` U-32; `platform-suitability.md` U-1, C-8, U-15.

**Confidence:** HIGH.

---
## 6. External verification performed in this pass

Block D is primarily an extraction pass over Areas 1–12. Four external checks were run, each for one of the reasons the brief permits (validate an alternative, fill a genuine evidence gap, verify current product boundaries, strengthen negative evidence). All follow `../source-policy.md`.

| Id | Purpose | Source | Result |
|---|---|---|---|
| **V-D-01** | Verify the deployment-model boundary underpinning AP-D-003, AP-D-035 and `alternatives.md` ALT-008 is still current | Microsoft Learn (search + platform documentation), fetched 2026-09-03 | **Confirmed.** The platform and its data service are SaaS-only; no on-premises or self-hosted deployment option is documented. On-premises *connectivity* exists (gateway, private networking with an express route into the virtual network); on-premises *deployment* does not. Consistent with `platform-suitability.md` PS-47. Tier 1. |
| **V-D-02** | Re-test manifest reservation **NB-02 / `IA-C-01`** (custom-connector throughput conflict) — the corpus's single most consequential open conflict | *Limits of automated, scheduled, and instant flows*, `ms.date` 2026-07-17, `updated_at` 2026-07-18; fetched 2026-09-03 | **"Number of requests per minute for a custom connector \| 500 requests per minute per connection"**, alongside *"Number of custom connectors \| 50 per user"*. Tier 1. |
| **V-D-03** | The other side of the same conflict | *Custom connector frequently asked questions*, `ms.date` 2025-03-13, `updated_at` 2025-09-10; fetched 2026-09-03 | For this platform: **"Number of requests per minute for each connection created by a custom connector \| 10000 requests for each connection created by the connector"**; connector count *"Free plan: one; Office 365 and Dynamics 365 plans: one; Per user plan: 50"*; also *"We handle throttling limit adjustments on a case-by-case basis"*. Tier 1. |
| **V-D-04** | Validate the one comparator-side claim Block D makes — that the deployment-model axis is a *materially relevant* distinction for `alternatives.md` ALT-008 | Vendor product documentation for two enterprise low-code platforms, fetched 2026-09-03 | **Materially relevant distinction confirmed, with precision.** One vendor documents Kubernetes-based private-cloud and on-premises deployment, including *"fully air-gapped private clouds or on-premise"* and a standalone operator for air-gapped DevOps. The other announced self-hosted deployment (*"your own private or public cloud, or on-premises Kubernetes infrastructure"*) dated 2026-03-31, but it is in an **Early Access Program, not generally available**; its older product line remains the on-premises-capable option. Vendor-side (analogous to the corpus's `MS-V` convention): **capability facts used; performance, cost and "productivity" claims not used.** |

### 6.1 Consequence of V-D-02 and V-D-03 for the corpus

**`NB-02 / IA-C-01` remains `CONFLICTED` as of 2026-09-03.** Two current Microsoft pages state figures differing by **20×** for the same platform. The newer page (the limits page, 2026-07) says 500; the FAQ (2025-03, updated 2025-09) says 10,000. This re-verification does **not** resolve the conflict, and the manifest's handling rule stands unchanged: **do not encode either figure as a sizing threshold; revalidate current documentation and measure the representative workload before commitment.**

Two things this check *does* establish:

1. The conflict is **live, not stale** — it survives in currently-maintained pages, so it is a genuine documentation inconsistency rather than an artefact of a superseded page. It must therefore be re-checked per engagement, not treated as closed.
2. There is a **documented escalation path** — throttle adjustments are handled *"on a case-by-case basis"* with justification — which is a legitimate mitigation to put in an option, and which no engagement can rely on in advance.

This is the evidential basis for AP-D-051's second mechanism, for DC-D-039's decision-blocking status, and for the corresponding row in `decision-intelligence-matrix.md` §4.

### 6.2 Consequence of V-D-04 for Area 14

The corpus previously placed non-Microsoft low-code platforms out of scope (`platform-suitability.md` §4.17: *"handled by other aisa packs"*). Block D does **not** reverse that, and does not build a vendor comparison. What V-D-04 establishes is narrower and sufficient for a decision model: **the deployment model is an axis on which at least one enterprise low-code alternative documents a generally-available capability that this platform documents as unsupported.** That makes "another low-code platform should be evaluated" a *evidence-backed* outcome for one specific class of requirement (customer-hosted, private-cloud or air-gapped deployment), rather than a courtesy option.

Everything else about those platforms — performance, cost, delivery speed, suitability — is **`UNKNOWN` in this corpus** and is recorded as such in `alternatives.md` ALT-008. See also §7 item 5.

---

## 7. Evidence-quality notes

1. **Derivation, not discovery.** 64 of the 68 entries are extractions from Areas 1–12 with no new external evidence. Their confidence is inherited from, and capped by, the canonical findings they cite. Four entries rest additionally on §6 (AP-D-003, AP-D-035, AP-D-051, and the ALT-008 link in AP-D-003/AP-D-035).
2. **The over-engineering asymmetry is real and is not hidden.** As §2.1 states, the corpus can argue against under-engineering from documented limits, but its case against over-engineering rests on Microsoft's minimal-complexity instruction plus its own "not suitable when" statements. AP-D-005, AP-D-006, AP-D-023 and AP-D-039 are therefore MEDIUM-to-HIGH on the vendor's own bounding statements and **not** supported by any limit. A reviewer should test these four hardest.
3. **`INF` framings.** AP-D-068's *framing* is `INF` over MS-sourced facts; each of its three mechanisms is quoted. AP-D-001, AP-D-002, AP-D-004, AP-D-014, AP-D-015, AP-D-019, AP-D-026, AP-D-027, AP-D-028, AP-D-039, AP-D-046, AP-D-048, AP-D-052, AP-D-059, AP-D-060, AP-D-061, AP-D-067 carry `INF` framings over MS-sourced facts. None is presented as Microsoft guidance. AP-D-027 additionally inherits manifest **NB-06**: the enterprise-boundary pattern it depends on is the corpus's weakest-evidenced pattern and is explicitly *not* Microsoft-endorsed.
4. **T3/T4 use.** Three entries rely on independent evidence for their *frequency or incident-class* claim while resting on MS evidence for the mechanism: AP-D-034 (external-surface exposure incident class), AP-D-020 (UI fragility framing — with `automation-architecture.md` U-07 recording that no Microsoft statement acknowledges it), AP-D-050 (practitioner reports of production-scale delegation failures). AP-D-033 uses a T4 bypass claim as a *signal requiring validation*, per `security.md` SEC-C2. In no case does a T3/T4 source carry a platform limit.
5. **Vendor-side comparator evidence is fenced.** V-D-04's capability facts come from the comparators' own documentation. Following the corpus's `MS-V` discipline, capability facts are used and adjectives are not. One is `EAP`, not GA, and that is stated wherever it is cited — Block D must not present an early-access capability as an available alternative.
6. **Preserved unknowns and conflicts.** No entry converts an open item into a threshold. Specifically preserved: NB-01 (far-side failure envelope, in AP-D-011), NB-02 (connector throughput, in AP-D-025/AP-D-051), NB-03 (composite availability, in AP-D-056), NB-04 (security-model performance curve, in AP-D-029/AP-D-051), NB-05 (write-through virtualization, in AP-D-012), NB-07 (no empirical performance, in AP-D-048/AP-D-052), plus `LC-U-05` (per-artefact premium obligation, in AP-D-062) and `licensing-cost.md`'s duplicate `DC-14` (§1.4).
7. **Single author, single session.** Derivation, categorisation and self-review share one author, as with the canonical files. The ledger in §3 exists so that an independent reviewer can audit the accept/reject boundary rather than only the accepted entries. `Research Status: CANONICAL` since that review; lineage in `canonical-manifest.md`.
8. **What is deliberately absent.** No scoring, no weights, no severity ranking beyond the Confidence field, no numeric thresholds not already in Areas 1–12, and no signals or questions. AP-D-059 is the entry that explains why a score would be actively harmful here.

---

## 8. Implications for the aisa knowledge model (pointers, not pack content)

Per `03-KNOWLEDGE-MODEL.md`, the chain is Requirement → Signal → Evidence → Knowledge State → Decision Criterion → Candidate Options → Trade-offs → Risk → Validation. This file supplies material for the **Risk** and **Trade-off** links, and its `Detection Signals` fields are raw material for the **Signal** link. It stops short of authoring any of them.

- **Detection signals** are technology-neutral by construction wherever the underlying evidence allowed it, so they are usable in a Discovery phase that forbids naming vendors and products. Where a signal cannot be expressed neutrally (an existing estate's actual technology, for example), the entry says so.
- **Anti-patterns map to knowledge states**, not to verdicts. A detected anti-pattern is a **Risky** claim about the current or proposed design; the corresponding requirement usually becomes an **Unknown** or **Conflicted** row until closed. Nine entries can produce a *decision-blocking* Unknown: AP-D-011, AP-D-013, AP-D-025, AP-D-035, AP-D-045, AP-D-051, AP-D-052, AP-D-056, AP-D-059.
- **The `Classification` field now carries the enforcement strength, and §8's old prose list has been folded into it** (repair, 2026-09-03). **Three entries are `GATE`** — where they hold, an option is *unavailable*, not merely worse: **AP-D-026**, **AP-D-059**, and **AP-D-013** for material data. **Four entries are `CONSTRAINT`** — always wrong within their stated scope, with the `Exceptions` field bounding the scope rather than admitting an exemption: **AP-D-031**, **AP-D-044**, **AP-D-051**, **AP-D-067**. The remaining 61 are `ANTI-PATTERN`. A pack that renders a `GATE` as a warning will lose the corpus's strongest negative findings; one that renders a `CONSTRAINT` as a contextual judgement will invite an override that has nothing to override.
- **One entry is portfolio altitude and must not be surfaced as an engagement finding:** AP-D-004 (see its altitude note). Its constituent mechanisms fire inside an engagement through AP-D-015, AP-D-009, AP-D-039, AP-D-036 and AP-D-063.
- **The matched pairs matter.** AP-D-036/AP-D-039 (under- and over-governance), AP-D-005/AP-D-003 (over- and under-engineering), AP-D-065/AP-D-039 (starting too cheap and starting too heavy) are opposing failures of the same lever. A pack that encodes one half of a pair will systematically push engagements toward the other.
- **Validation obligations** cluster in AP-D-048, AP-D-051 and AP-D-052 and reference the four-level model (V1 limits, V2 bounded pilot, V3 pro-dev harness, V4 managed-test fidelity). Those three entries are the natural source of a pack's validation-requirement logic.
- **Cross-links** are formalised in `decision-intelligence-matrix.md`. Every entry here is reachable from at least one criterion in `decision-criteria.md` and at least one alternative class in `alternatives.md`; orphans are reported in that file's §6.

Nothing in this section is pack content. Question banks, signal catalogues, glossaries and decision trees remain out of scope by instruction.

---

## 9. Summary

| | |
|---|---|
| Candidate topics evaluated | 124 |
| Accepted entries | 68 |
| Merged or confirmed to an existing entry | 37 |
| Rejected — Areas 1–12 altitude | 25 |
| Rejected — misclassified | 3 |
| Rejected — evidence absent | 1 |
| Entries with `INF` framing | 18 |
| Entries preserving a canonical `UNKNOWN` or `CONFLICTED` | 12 |
| Classification: `ANTI-PATTERN` · `GATE` · `CONSTRAINT` | 61 · 3 · 4 |
| Entries that make an option *unavailable* rather than worse (`GATE`) | 3 |
| Entries at portfolio rather than engagement altitude | 1 (AP-D-004) |
| Composed disqualifiers in AP-D-059 | **12** (8 from `architecture-patterns.md` §13, 4 added by Block D) |
| External verification checks performed | 4 (§6) |
| Canonical reservations carried forward untouched | NB-01, NB-02, NB-03, NB-04, NB-05, NB-06, NB-07 |
| Lineage defects observed and recorded, not repaired | 2 (§1.4) |

**The single most consequential addition** relative to the brief's candidate list is **AP-D-059 — Composed disqualifier ignored**. It is the entry that makes the rest of Block D usable: without it, a reader can pass an option by assessing each dimension favourably in isolation, which is exactly the failure `architecture-patterns.md` §13 was written to prevent, and exactly what a scoring model would institutionalise.

`Research Status: CANONICAL` — Block D review 2026-09-03 returned `PASS WITH CORRECTIONS`; the bounded repair of M-02, M-07, M-08, M-09, M-10, M-11 and L-03 is recorded in `block-d-repair-report.md`. The independent **re-review** 2026-09-03 returned `FAIL` (`block-d-re-review.md`) and this file carried the **V2 repair** as it touches AP-D-059 — outcome class 14, the class 5 / class 14 boundary, and the `Xc` registration authority — recorded in `block-d-repair-v2-report.md`. **Re-review V2** (`block-d-re-review-v2.md`) returned `FAIL`, and the **Block D gate** (`block-d-gate.md`) independently confirmed both remaining findings. This file carries the **bounded V3 gate repair** as it touches AP-D-059 — the eighth `Xc` registration (DC-D-068) and the per-row outcome mapping, replacing the single global {5, 12, 14} — recorded in `block-d-gate-repair-report.md`. **Gate recheck performed:** `block-d-final-gate-recheck.md` returned `FINAL BOUNDED GATE RECHECK: PASS` with `NEW GATE-BLOCKING FINDINGS: 0`. Canonicalized 2026-09-03; lineage in `canonical-manifest.md`. Note that R-03 (the DC-D-055 matrix row) remains **open and out of this repair's scope**.

---
