Research Status: CANONICAL
Research Confidence: MEDIUM
Block: D — Decision Intelligence
Area: 14 — Alternatives
Gate: PASS — Block D Final Bounded Gate Recheck
Canonicalization Basis: Block D Final Bounded Gate Recheck (`block-d-final-gate-recheck.md`)
Upstream Evidence Baseline: Areas 1–12 canonical files (`canonical-manifest.md`)
Canonicalized: 2026-09-03
Freeze Status: FROZEN FOR PP PACK AUTHORING

# Alternatives — Block D Research Evidence

Research area: **14 — Alternatives** (`../research-areas.md`).
Derivation date: **2026-09-03**.
Primary input: `canonical-manifest.md` and the twelve canonical Area 1–12 files it names.
Source policy: `../source-policy.md`.
Peer files: `anti-patterns.md` (Area 13), `decision-criteria.md` (Area 15), `decision-intelligence-matrix.md`.

**The question this file answers.** *If Power Platform is not the best architecture for this requirement, what classes of alternative should be considered, and what requirement makes each of them more appropriate?*

**What this file is not.** It is not a competitive product catalogue, not a vendor comparison, and not framed as "Power Platform versus X". Power Platform appears here as **one option class among eleven** (ALT-004), with the same field structure and the same evidential treatment as every other class.

---

## 1. Identifier namespace

Alternatives use **`ALT-NNN`**. Collision check across the canonical corpus on 2026-09-03: `grep -ohE '\bALT-[0-9A-Za-z]+\b' *.md` returned empty. The namespace is clean. See `anti-patterns.md` §1 for the full Block D namespace rationale, including why `AP-NNN` and `DC-NNN` were **not** reused.

---

## 2. The symmetry rule, stated before anything else

This is the field where a decision-support corpus most easily becomes an advocacy document. Three rules are applied throughout, and a reviewer should test them.

### 2.1 Equal evidential burden

An alternative is not required to prove itself against claims Power Platform is allowed to assert unproven. Where this corpus knows a fact about Power Platform and does not know the equivalent fact about an alternative, **the asymmetry is stated as an asymmetry**, not resolved in either direction.

The corpus already enforces this on itself. Its own remediation record notes that v1's *"principal weakness was that all its negative evidence was about Power Automate and none about the alternatives it recommended; that asymmetry is corrected here"* (`automation-architecture.md` §8). The result is a negative-evidence register with **33 documented negative facts about the alternatives** it recommends (§8.2–§8.6) alongside 16 about Power Automate — and this file inherits those.

### 2.2 Forbidden universal claims

The following are **not** findings and appear nowhere in this file as conclusions:

| Forbidden claim | Why |
|---|---|
| "Custom development is more expensive" | Depends on requirements, team, lifecycle and full TCO. The corpus rejected its own earlier row-level cost comparisons as *"too weakly evidenced on the comparator side"* and replaced them with a **method** (`licensing-cost.md` §6). |
| "Low-code is faster" | A marketing claim by the source policy's own test (§7: *"'build faster' … are NOT evidence by themselves"*). Low-code lowers the cost of the *first* version, which *"shifts the cost of ownership toward change"* (`licensing-cost.md` LC-29) — a trade, not a win. |
| "Power Platform scales" / "does not scale" | Both adjectives are excluded. The corpus's rule for the one place where two Microsoft sources disagree on scale positioning is **"encode neither adjective"** — encode the documented limits and the escalation conditions instead (`integration-architecture.md` C-04). |
| "Azure is the answer for anything hard" | The corpus names this as an anti-pattern of reasoning twice: assuming Azure is the boundary when an enterprise platform already owns it (`architecture-patterns.md` Y-12), and justifying Azure with claims the platform's own documentation contradicts (`platform-suitability.md` AP-15). |
| "Building it yourself gives you control" | Countered by the corpus's own cost instruction: *"Custom solutions might seem powerful but often require a bigger budget for development, licensing, and support. Justify higher costs with clear business value"* (`integration-architecture.md` §12.9). |

### 2.3 What is *not* a reason to leave Power Platform

Recorded first, so the exit triggers in §4 can be read as the exceptions they are. From `integration-architecture.md` §12.9, all MS-sourced:

- **Scale anxiety without a number.** The meters are published; compute them. *"Scales effortlessly"* and *"small to medium scale"* are both marketing.
- **A preference for code.** The total-cost-of-ownership instruction cuts the other way (quoted in §2.2).
- **One difficult step.** The documented answer is a hybrid split *at the step*, not relocating the whole solution (→ ALT-009).
- **Resemblance to a reference architecture.** Every reference architecture carries its own *"This article provides an example"* caveat.

Add two more from elsewhere in the corpus:

- **Versioning or monitoring gaps as the argument.** `platform-suitability.md` AP-15 records this as contradicted by the platform's own lifecycle documentation; *"the real differentiators are compute, network, ownership"* (PS-24, PS-48).
- **The absence of a published benchmark.** No component of *any* platform in this corpus has an empirical benchmark (manifest **NB-07**). Absence of proof is symmetric and favours nobody.

---

## 3. The option set the corpus requires

Two canonical files independently state that a defensible option set must be broader than a technology shortlist.

`licensing-cost.md` LC-28 (*"Not-doing-it and doing-it-manually are legitimate economic options and are frequently the honest answer"*) requires that Options **always** carry:

> (a) process change without technology, (b) the existing capability already licensed, (c) Power Platform, (d) alternatives, (e) do nothing.

`platform-suitability.md` §9 lists the options the pack must be able to output:

> do nothing / process change; existing M365 or first-party capability; Power Platform on seeded licences; Power Platform premium; hybrid with Azure; Logic Apps/Azure-first; custom application; buy (ISV).

The eleven classes below are the union of those two lists, plus the two classes the corpus discusses substantively but omits from both summaries — an existing enterprise platform that already owns the domain (`governance.md` GOV-XB-02, `integration-architecture.md` §12.1, `automation-architecture.md` AT2-52) and another low-code platform (out of scope in Area 1, admitted here on the evidence of §5 V-D-04).

| Id | Class | Corpus basis |
|---|---|---|
| ALT-001 | Extend the existing system — no new platform | LC-28(b), PS-41 |
| ALT-002 | Process change — no new technology | LC-28(a), PS-44 |
| ALT-003 | Collaboration-platform native capability | PS §9, PS-14, AA-51 |
| ALT-004 | **Power Platform** (in its several forms) | PS §9, all areas |
| ALT-005 | Custom development | PS §9, AA-30/AA-36, §12.7 |
| ALT-006 | Cloud-native services (integration, compute, messaging, data) | PS-44, AT2 §3.B, IA §12 |
| ALT-007 | Existing enterprise platform owns the capability | GOV-XB-02, IA §12.1, AT2-52 |
| ALT-008 | Another low-code platform | admitted on §5 V-D-04; out of scope in PS §4.17 |
| ALT-009 | Hybrid architecture | AP-05, AP-10, AT2 §6, PS §2 row 17 |
| ALT-010 | Do nothing / defer | LC-28(e) |
| ALT-011 | Buy — packaged product, SaaS or ISV | PS-41, PS-44, AA-36 rung 0 |

**Ordering note.** The list is deliberately ordered from *least* to *most* new technology, which is the order the corpus's own ladders use — configure or buy sits at *"rung 0, before any app type"* (`application-architecture.md` AA-36), and the integration classification test puts "already owned elsewhere" at **step 1** (`integration-architecture.md` §2.2). The ordering is a reading aid, **not** a preference ranking: ALT-005, ALT-006 and ALT-008 are correct answers for the requirements named in their trigger fields, and arriving there quickly is not a failure.

---

## 4. Alternative classes

Field order per entry: Class · Problem types it fits · Requirement triggers · Strengths · Weaknesses · Architectural consequences · Security/governance consequences · Delivery/ALM consequences · Performance/scale consequences · Cost/TCO consequences · Operations consequences · When preferable to Power Platform · When Power Platform is preferable · Hybrid opportunities · Key decision criteria · Related anti-patterns · Evidence · Confidence.

`Origin` conventions follow the corpus: **MS** = Microsoft statement · **MS-V** = Microsoft vendor-side positioning (capability facts only) · **V3** = non-Microsoft vendor documentation, capability facts only, marked where used · **INF** = supported synthesis · **T3/T4** = independent/community, corroborative only.

---

### ALT-001 — Extend the existing system; no new platform

**Class.** The capability is added to, or configured within, the system that already performs the surrounding work — the line-of-business application, the enterprise resource planning or customer system, the incumbent database application.

**Problem types it fits.** A gap in an existing process where the surrounding process, the data and the users already live in one system. Reporting or workflow additions to an application that supports both. Requirements expressible as configuration rather than construction. Cases where the data must not be copied.

**Requirement triggers.**
- The system of record for the entity is the incumbent, and the requirement is a *view or an interaction* rather than new authoritative data (DC-D-021).
- The incumbent already offers the capability as configuration — *"App settings are the safest and least disruptive way to customize your app"* (`platform-suitability.md` PS-41).
- Audit, compliance or authorization obligations already live in the incumbent and would have to be rebuilt anywhere else (`data-architecture.md` §6, `architecture-patterns.md` matrix rows 17–18).
- The requirement would otherwise create a second master (→ `anti-patterns.md` AP-D-010, AP-D-014).
- The incumbent enforces per-row or per-field authorization that a copy could not (`data-architecture.md` DA-11, DA-33, §2 row 5).

**Strengths.** No new platform, no new licence class, no new operating model. Authority, audit and authorization stay where they are already enforced and evidenced. No synchronisation, therefore none of the synchronisation risk register (`integration-architecture.md` §8). The corpus's cost method names *"existing sunk capability"* as a dimension where *"the economically correct answer may be 'use the incumbent'; avoid double-paying for a second platform"* (`licensing-cost.md` §6).

**Weaknesses.** Constrained by the incumbent's own extensibility model, release cadence and vendor. Change lead time is the incumbent team's, not the project's. Where extension means customisation rather than configuration, it carries *"performance, ALM, upgrade and support cost"* (`platform-suitability.md` PS-41) in the incumbent — a cost this corpus can name but not size, because it holds no evidence about any specific incumbent. The user experience is the incumbent's; where the requirement is a materially better experience, that is a real limit (DC-D-012).

**Architectural consequences.** No new integration, no new store, no new topology — the strongest possible outcome on `integration-architecture.md`'s classification test, which never reaches step 6. The architecture question collapses to "what does the incumbent support".

**Security / governance consequences.** The incumbent's controls apply unchanged; no second enforcement plane, no second policy model, no second identity surface. Governance ownership is unchanged, which the corpus treats as the point: *"ask whether the enterprise capability already satisfies the required protocol, security, reliability, latency and ownership model before creating a new boundary"* (`governance.md` GOV-XB-02). The residual governance question is who owns the configuration change and its review.

**Delivery / ALM consequences.** The incumbent's lifecycle, which may be more or less mature than the project's — the corpus asserts nothing either way. No second supply chain (contrast `alm-devops.md` §14.2). Where the incumbent has no lifecycle discipline, extension inherits that, and that is a genuine risk to record rather than assume away.

**Performance / scale consequences.** Inherits the incumbent's envelope. No new meters, and none of the five-meter analysis of `performance-scale.md` §2 applies. Whether the incumbent's envelope is adequate is a per-engagement measurement question (DC-D-084…DC-D-091); **this corpus holds no performance evidence about any incumbent.**

**Cost / TCO consequences.** Usually the lowest incremental cost, because the licences, environments, monitoring and support already exist. Not automatically the cheapest: incumbent change may be charged at a rate the project does not control, and enterprise-application customisation can be the most expensive change class in an estate. Priced on the same ten dimensions as every other class (`licensing-cost.md` §6).

**Operations consequences.** No new artefact to monitor, support, recover or retire — the class that best avoids `anti-patterns.md` AP-D-053, AP-D-054 and AP-D-067. Incident ownership is unchanged.

**When preferable to Power Platform.** When the incumbent already owns the entity and can satisfy the requirement by configuration; when the requirement's authorization or audit obligations are already enforced there; when a copy would create a second master; when the incremental cost of a second platform is not justified by the delta in outcome.

**When Power Platform is preferable.** When the incumbent cannot satisfy the requirement — recorded **per requirement**, not asserted. `governance.md` GOV-XB-02 is explicit: *"Reuse is not automatic: an incumbent that cannot meet the requirements remains unsuitable."* Also when the incumbent's change lead time or cost is incompatible with a genuine business deadline (recorded as a constraint), when the requirement spans several systems none of which owns it, when the experience requirement genuinely exceeds what the incumbent can present, or when the incumbent is on a dated decommissioning plan.

**Hybrid opportunities.** The dominant and often best composition: the incumbent keeps authority; Power Platform supplies the experience or the orchestration and reads through or receives events (`architecture-patterns.md` AP-06, AP-03; `data-architecture.md` §2 rows 13–14). This is ALT-009 in its most common form.

**Key decision criteria.** DC-D-021 (system of record), DC-D-111 (existing enterprise platform estate), DC-D-006 (accountable ownership), DC-D-012 (interaction complexity), DC-D-092 (budget), DC-D-003 (time to value), DC-D-034 (migration scope).

**Related anti-patterns.** `anti-patterns.md` AP-D-007 (rebuilding what exists), AP-D-010 (shadow system of record), AP-D-014 (system of record undeclared), AP-D-027 (existing ownership bypassed).

**Evidence.** `platform-suitability.md` PS-41, PS-44 (last rows), §2 row 26, §9; `application-architecture.md` AA-36 rung 0, §1 row 0, §2 (first boundary), AA-20; `licensing-cost.md` LC-28, §6 (existing sunk capability), LC-21; `governance.md` GOV-XB-02; `integration-architecture.md` §12.1, §2.2 step 1, §9 row 23; `data-architecture.md` §2 rows 13–14, §6, DA-45, DA-46; `architecture-patterns.md` matrix rows 16–18, 29.

**Confidence:** MEDIUM. The *trigger* evidence is Microsoft-sourced and strong; the *comparator* side — what any particular incumbent can actually do, at what cost — is **`UNKNOWN` per engagement** and must be established, not assumed. This asymmetry is intrinsic to the class.

---

### ALT-002 — Process change; no new technology

**Class.** The problem is solved by changing how the work is done: removing steps, standardising a variant process, simplifying or removing approvals, eliminating duplicate data capture, changing who does the work or when.

**Problem types it fits.** Processes whose cost is structural rather than tooling — redundant approvals, rework from upstream data quality, duplicate capture across systems, variation with no business justification. Low-frequency, low-value processes. Cases where automating the current process would fix its symptoms and preserve its cause.

**Requirement triggers.**
- The full cost of ownership exceeds the value of the process. `licensing-cost.md` LC-28 states this plainly: full TCO *"frequently exceeds the value of a low-frequency process even when licences are free"* — the strongest single trigger for this class in the corpus.
- Process maturity is low or the process is unstable (DC-D-005): automating an unsettled process fixes the wrong version of it.
- The requirement is a feature list of an outgoing system rather than an outcome (→ `anti-patterns.md` AP-D-007; *"Don't replicate your legacy solution"*, `platform-suitability.md` PS-41).
- The requirement includes steps that exist only because of a previous tool's limitations.
- The requirement's hard constraint (atomicity, latency, residency) disappears if the process is re-sequenced — a redesign that no technology choice can substitute for.

**Strengths.** Removes cost rather than moving it. No licence, no environment, no monitoring, no support plan, no lifecycle, no retirement obligation — none of the twelve-plus cost lines of `licensing-cost.md` LC-21. No technical debt and no deprecation exposure (→ `anti-patterns.md` AP-D-058). Frequently the only option that improves the *cause* rather than the symptom.

**Weaknesses.** Requires organisational authority the project may not have, and change management effort that is real but which this corpus cannot size. Politically the hardest option to carry, because it is nobody's deliverable. It can be used as a way to decline a legitimate requirement, which is its own failure mode. And the corpus is candid that **no Microsoft source frames this option — the absence is the point** (`licensing-cost.md` LC-28), so the evidence for it is `INF` framed by analogy from cloud cost-optimisation guidance.

**Architectural consequences.** None, which is the whole value. It also frequently *changes the requirements* for whatever is built afterwards — a re-sequenced process can move a requirement from strict atomicity to eventual convergence, or from sub-minute freshness to hourly, either of which changes every downstream decision.

**Security / governance consequences.** No new attack surface, no new policy scope, no new maker population. Where the change removes a system or a data copy, it *reduces* governance surface.

**Delivery / ALM consequences.** No supply chain. Delivery is organisational: communication, training, and enforcement of the new way of working — with no rollback mechanism, which is a real asymmetry against technical options.

**Performance / scale consequences.** Not applicable in platform terms. Note that process change can *achieve* a scale objective that no platform choice would: removing a step removes its throughput requirement entirely.

**Cost / TCO consequences.** Ordinarily the lowest, and the corpus requires it to be **priced and carried** rather than mentioned: *"Always carry process change, existing capability and do-nothing as priced options"* (`licensing-cost.md` LC-28, `licensing-cost.md` DC-15). Its real cost is change-management effort and the opportunity cost of the capability not built.

**Operations consequences.** No operational footprint. The ongoing obligation is behavioural compliance, which decays without reinforcement — the mirror of technical debt.

**When preferable to Power Platform.** When the economics do not support automation at all; when the process is immature or unstable; when the requirement's difficulty is self-inflicted; when the same outcome is reachable by removing work rather than tooling it. Also as a *precondition*: standardising a variant process before automating it usually reduces the resulting solution by more than any platform choice would.

**When Power Platform is preferable.** When the process is stable, valuable, and its cost is genuinely tooling-driven; when volume, compliance or evidence requirements make manual execution untenable; when process change has already been tried and the residual cost is tooling. Also when the sponsor's authority genuinely does not extend to changing the process — a constraint to record rather than a reason to pretend the option does not exist.

**Hybrid opportunities.** Process change plus a *smaller* technical solution is the most under-used composition in the corpus's own framing: re-sequence to remove the hard constraint, then build the simplified remainder — which often moves the answer down `architecture-patterns.md`'s escalation ladder by one or two rungs.

**Key decision criteria.** DC-D-005 (process maturity), DC-D-008 (process value), DC-D-092 (budget), DC-D-003 (time to value), DC-D-006 (ownership and authority), DC-D-004 (expected lifespan), DC-D-007 (change frequency).

**Related anti-patterns.** `anti-patterns.md` AP-D-007, AP-D-039 (enterprise controls on a trivial workload), AP-D-060 (licence line as TCO — which is what hides this option), AP-D-065.

**Evidence.** `licensing-cost.md` LC-28, LC-21, LC-29, `licensing-cost.md` DC-15, §6, §7.1 item 1 (no cost pillar); `platform-suitability.md` PS-41, PS-44 (last rows), §9; `application-architecture.md` AA-36 rung 0; `data-architecture.md` §6; `automation-architecture.md` §4.1 (organisational fit), AT2-52.

**Confidence:** MEDIUM. The economic trigger is well-evidenced within the corpus; the class itself is `INF` because no Microsoft source frames it, and the corpus says so explicitly.

---

### ALT-003 — Collaboration-platform native capability

**Class.** The requirement is met by capabilities of the collaboration and productivity platform the organisation already licenses — document libraries and lists, team surfaces, forms, spreadsheets, and the standard workflows over them — without building an application.

**Problem types it fits.** Document-centric work where **the document is the record**. Small flat trackers. Simple structured collection. Team-scoped collaboration. A form over a single list where the readers are that list's readers. Report-driven write-back at small volume.

**Requirement triggers.**
- The document *is* the record: files plus metadata, versions, retention labels, and protection that travels with the file (`data-architecture.md` §2 row 7, §6).
- Light metadata with no relational query requirement (`platform-suitability.md` §2 row 4).
- Team-scoped, self-contained, within the team data store's ceiling, needing none of its exclusions (`data-architecture.md` DA-13, `application-architecture.md` §1 row 6).
- Readers of a list are the intended audience of the form over it (`application-architecture.md` AA-51).
- Seeded entitlement is the funding constraint **and** the requirement genuinely fits it (contrast `anti-patterns.md` AP-D-061).

**Strengths.** Already licensed; no premium entitlement; no new environment; no new operating model. Genuinely strong for its documented purposes — document libraries with versioning and label-based protection are the corpus's positive recommendation, not a fallback (`data-architecture.md` §6). Confidentiality at document level is supported, including customer-managed key coverage via a dedicated policy — the corpus explicitly **corrects** an earlier claim to the contrary (`data-architecture.md` DAP-43, SQ2-10), which is a useful check against reflexively dismissing this class.

**Weaknesses.** Documented and severe **outside** its purposes, and this is where `anti-patterns.md` AP-D-008 lives: a list view threshold around 5,000 items that *"can't be changed"*; a 12 lookup/person/metadata column ceiling per view or retrieval; the narrowest delegation table of the three connectors, producing **silent partial results**; ≤ 5,000 unique permission scopes recommended and **no column-level security**; no transactions, last writer wins; lists outside the solution lifecycle with internal-name drift; all defined columns returned on every read, making column count a performance parameter; partitioning instructed above *"hundreds of thousands of records"*. Spreadsheet-as-store adds: *"Simultaneous file modifications … are not supported"*, a six-minute lock, a 25 MB ceiling, duplicate inserts on retry, and *"Excel isn't a relational database system"* with **no transaction threshold published**. Team-scoped store adds: a hard capacity ceiling that **cannot be extended**, feature exclusions, a **one-way** upgrade converting all users to premium, and export to a full environment *"not yet available"* — so the exit may be a rebuild.

**Architectural consequences.** No application architecture. The constraint set is the store's, and it is narrow: the access paths must be few and indexable, the relational depth shallow, the concurrency low.

**Security / governance consequences.** Document-level protection and labelling are strengths. Row-scope and column-level confidentiality are **not available** at the granularity a relational store offers, so a segmentation requirement disqualifies the class. Artefacts sit largely outside the platform's own governance surfaces, which cuts both ways: less policy overhead, and less inventory and detection.

**Delivery / ALM consequences.** Weak by design: lists are outside solutions, environment variables do not apply, internal names drift across environments, and a customised form over a list is *not* portable — *"no manual sharing, no automated cross-environment copy"* (`application-architecture.md` AA-51, AP-34). Acceptable for the class's intended scope, disqualifying above it.

**Performance / scale consequences.** Bounded by the thresholds above, and the failure mode is **wrong answers rather than slow ones** — the single most important fact about this class (`performance-scale.md` PF-AP-01, PF-AP-11, PF-AP-12).

**Cost / TCO consequences.** Lowest incremental licence cost of any class that involves building something, because the entitlement exists. **Not** automatically lowest TCO: `licensing-cost.md` LC-27 documents the licence-avoidance case where the standard-connector path is licence-cheap but carries *"documented performance penalties"* and remediation cost. The honest position: cheapest where the fit is genuine, most expensive where it is a workaround.

**Operations consequences.** Minimal footprint, and correspondingly minimal observability, recoverability and inventory. Artefacts outside solutions are excluded from backup coverage and pipeline deployment, and are invisible to the automation-monitoring surface (`operations-support.md` OP-15, OP-AP-07).

**When preferable to Power Platform.** When the document is the record; when the tracker is small, flat and low-concurrency; when the form's audience is the list's audience; when team scope and seeded entitlement genuinely match the requirement. In these cases it is not a compromise — it is the documented recommendation.

**Outcome class (added 2026-09-03).** These four shapes are the **only** place in Block D where an alternative class may be named as the answer without a `COMPARATOR EVIDENCE ABSENT` marker, and they have a class of their own: `decision-criteria.md` §6.2 **class 13 `ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED`**. Three properties of that class matter here and are not negotiable. It states that **Power Platform is not excluded** — no exit fires in these shapes, and the class is not a rejection. It asserts **nothing comparative** about cost, speed, scale or reliability; the only cost fact it may carry is the seeded-entitlement one the corpus does state (DC-D-093), never a TCO comparison, which `licensing-cost.md` LC-U-04 records as absent for every class. And it **requires a graduation trigger**, because the documented path out of this class and the team-hosted surface is a **one-way upgrade** that converts every user to premium (`application-architecture.md` AA-50) — which is why `anti-patterns.md` AP-D-065 exists. Outside these four shapes, and for every other alternative class, class 13 is followed by class 8 and carries the marker like everything else.

**When Power Platform is preferable.** Any of AP-D-008's trigger conditions: growth past the thresholds, relational depth, row or column confidentiality, all-or-nothing writes, concurrent editing, field-level audit, or inclusion in a solution lifecycle. Also when a documented graduation path is needed rather than a one-way upgrade.

**Hybrid opportunities.** Well-documented and often correct: documents in the library (where labels and protection travel), structured metadata and process state in a relational store, with a reference between them — accepting that the composition *"inherits two security models that do not synchronise"* (`data-architecture.md` DA-44, DA-59). Also: binaries in the cheap file store rather than the expensive database meter (`data-architecture.md` DA-14, DA-62).

**Key decision criteria.** DC-D-022 (relational complexity), DC-D-023 (queried volume per access path), DC-D-026 (access granularity), DC-D-027 (audit), DC-D-028 (atomicity), DC-D-030 (concurrent edit), DC-D-025 (attachment volume), DC-D-093 (entitlement fit), DC-D-074 (scope).

**Related anti-patterns.** `anti-patterns.md` AP-D-008 (the central one), AP-D-050, AP-D-061, AP-D-065, AP-D-047.

**Evidence.** `data-architecture.md` §2 rows 1–8, 22, 25, §6, DA-13, DA-14, DA-39…DA-44, DA-59, DA-62, DA-63, DAP-1, DAP-2, DAP-43, SQ2-10, C-05; `platform-suitability.md` PS-14, PS-16, PS-42, PS-43, AP-5, §2 rows 3–4; `application-architecture.md` AA-50, AA-51, AP-32, AP-34, §1 rows 6–7; `performance-scale.md` PF-AP-11, PF-AP-12, §8.1 items 38–40, §3.B; `licensing-cost.md` LC-27, LC-AP-01, LC-AP-09, §7.2 items 31–33; `operations-support.md` OP-15, OP-AP-07; `governance.md` GOV-24.

**Confidence:** HIGH on both the fit and the disqualifiers — this is the best-evidenced alternative class in the corpus, in both directions.

---

### ALT-004 — Power Platform

**Class.** The low-code application, automation, data and external-site platform, in its several forms: task-focused apps, record-centric apps over the governed relational store, external-facing sites, workflow automation, server-side platform code, and the team-scoped variant.

**This entry is deliberately written to the same standard as every other class.** Its weaknesses field is longer than its strengths field, which reflects the corpus's evidence balance and its own rule that positive capabilities appear *"only where they define a fit boundary"* (`platform-suitability.md` purpose statement).

**Problem types it fits.** Internal structured-data applications — forms, approvals, inspections, asset and case tracking. Relational, process-heavy work with row and column security and audit. Human-in-the-loop workflow within a month. Bounded connector-based integration over the productivity and business-application estate. Authenticated external-user portals over the governed store. Team-scoped collaboration apps.

**Requirement triggers (positive).** Phrased as the corpus requires — *"no documented constraint violated"*, never as endorsement:
- Queried collections delegable or below the client ceiling; per-identity request volumes inside the meters (`platform-suitability.md` §2 row 1).
- Relational, process-heavy data needing row/column security and audit — the record-centric app over the governed store, which is a **STRONG** verdict with `MS` origin (`platform-suitability.md` §2 row 2).
- A human must decide, delegate, escalate, reject or cancel within 30 days — approvals are a first-class construct on a **standard (non-premium) connector** with five response models, reachable from mail, chat and an action centre, *"with no equivalent in the alternatives"* (`automation-architecture.md` §4.1, AT2-23, AT2-24).
- The trigger is a business event in the productivity or business-application estate and the work is a bounded sequence of connector calls — 1,400+ connectors, business ownership, and the licence usually already paid; here *"the alternatives' technical advantage … is nil and their operating cost is not"* (`automation-architecture.md` §4.1).
- **The organisation has no operating model for a second platform** — no subscription ownership, no on-call for cloud resources, no infrastructure-as-code pipeline. This is an explicit, MS-reasoned trigger *for* staying in-platform (`automation-architecture.md` §4.1), and the mirror of `anti-patterns.md` AP-D-026.
- Guided multi-stage human data entry inside a record-centric app, within the stage and table caps.
- Immediate, unbypassable, transaction-participating logic **inside** the governed store — server-side platform code is **STRONG** here and is additionally **exempt from the per-identity service-protection meter**, which is the corpus's highest-leverage documented scale remedy (`performance-scale.md` B-09, `automation-architecture.md` AT2-35).

**Strengths.** Breadth of connectivity; first-class human-workflow constructs on standard entitlement; a governed relational store with row-, column- and unit-scoped authorization, audit and alternate keys; offline over that store within its documented list; accessibility attested at product level for two of the surfaces; multi-language support in two of the surfaces; a solution-based lifecycle with promotion, environment variables and connection references; in-region zone redundancy with recovery-point near zero and recovery time under five minutes, automatic, with no extra architecture; a maker population that can build without the delivery organisation.

**Weaknesses.** From the corpus's own registers, restricted to those that change a decision:
- **Deployment model is fixed:** internet-only SaaS; disconnected, air-gapped and customer-hosted are **unsupported** (`platform-suitability.md` PS-47; re-verified, `anti-patterns.md` §6 V-D-01).
- **No atomicity beyond the governed store's own boundary**, and no cross-system coordinator anywhere (PS-45, IA-19).
- **No compute-sizing dial**, and server-side code is capped at two minutes with its execution charged to the caller's budget (PF-45, PS-09).
- **Five independently-evaluated meters**, with the binding one usually *not* the daily entitlement that licence conversations centre on; batching explicitly cannot bypass entitlement (PF §2, AT2-02).
- **Silent failure modes:** non-delegable queries return truncated results as if complete; sustained overload slows then **disables after 14 days**, and editing the artefact **resets the evidence**.
- **Ownership fragility:** throughput profile follows the owner's licence with a **50× spread** and reverts on their departure; 90-day inactivity suspension; a non-solution automation's owner cannot be changed at all.
- **No published concurrent-user figure, no published end-to-end latency figure, and no empirical benchmark anywhere** (manifest NB-07).
- **Operational capability is licence-gated:** telemetry export, extended backup, cross-region recovery, pipelines, network isolation, key control and firewall all require the managed environment class — premium licences **for every active user of that environment** (LC-23).
- **No published cross-region recovery-time commitment**; cross-region is opt-in, doubles storage, and **degrades high-volume automation** (PF-40, PF-43).
- **No cost-optimization pillar** for the platform, so no first-party structured cost-review method exists (LC-01).
- **Mandatory semi-annual release waves and a continuous deprecation register**; behaviour cannot be frozen (PS-50).
- **No supported first-party low-code functional-test framework** after the previous one's deprecation (ALM-17).
- **Portability is asymmetric:** data and server-side .NET components are portable; the user interface, the expression language and the automations are **not** (PS-51).
- **Licensing is not authoritatively documented** in the general documentation — every page defers to the licensing guide and the customer's agreement, with a documented **right of suspension** for consumption above entitlement (LC-02).

**Architectural consequences.** A layered model with five independent security enforcement planes, five independent meters, and an escalation ladder that must be climbed only on named requirements. Several modelling decisions are **irreversible** (table ownership type, virtual-versus-standard, team-store upgrade, business-application installation at environment creation, trigger concurrency), which front-loads decision weight into Discovery.

**Security / governance consequences.** Capable at the data layer (unit/role/team scoping, column security, masking, audit) and at the identity layer; the enforcement plane model means a requirement must be satisfied on the *lowest* plane that can enforce it. Governance is a set of platform configurations, most of which are **preventive only in the managed environment class**; the detective controls run weekly and only there. Several controls are narrower than commonly claimed (see `anti-patterns.md` AP-D-033).

**Delivery / ALM consequences.** Four rungs with different guarantees and prerequisites; **source control is what forces the top rung, not automation**; the promotion mechanism requires managed target environments (hence premium licences), cannot cross tenants, and **there is no solution rollback**. Two or more makers on one artefact requires an environment per maker, since co-authoring on the low-code app artefact was removed.

**Performance / scale consequences.** Limits-based, not benchmark-based. Documented envelopes are exclusion evidence; performance requires measurement. The highest-leverage in-platform remedies are the service-protection-exempt server-side path, bulk mechanisms with the automation orchestrating rather than iterating, and delegable access paths.

**Cost / TCO consequences.** Five simultaneous economic mechanisms (per-user, per-app/scope, capacity licence, consumption meter, stored capacity). Cost is driven by **people and scope** more than by machine work, which is the corpus's retained hypothesis for a crossover test (see §5.2). At least twelve TCO lines, only one of which the vendor prices. Criticality drives the licence model through the managed-environment chain, which is why *"a departmental solution becomes expensive the day it matters."*

**Operations consequences.** Nothing is monitored by default; there is no default owner, alert or runbook. Observability depth is a licensing decision. Native transactional run history expires at 30 days. Restore is not a rollback and has extensive side effects. A support plan is a separate purchase, end users cannot raise tickets, there are no root-cause analyses, and performance and non-reproducible cases are capped at four hours.

**When preferable to the alternatives.** When the requirement matches the positive triggers above **and** at least one of: the entitlement already exists and the requirement stays inside it; the human-workflow construct is central; the connector breadth over the existing productivity and business-application estate is the actual value; the organisation cannot operate a second platform; the governed relational store's authorization and audit model is what the requirement needs; time-to-value from a business-owned maker population is the decisive constraint.

**When another class is preferable.** When any of §4's other entries' triggers fire — most sharply: a deployment-model constraint (ALT-005, ALT-008), a dominant hard non-functional requirement (ALT-005, ALT-006), an existing owner of the capability (ALT-001, ALT-007), an existing packaged product (ALT-011), economics that do not support automation (ALT-002, ALT-010), or sustained throughput past the three-meter envelope with no natural partitioning (ALT-006, ALT-009).

**Hybrid opportunities.** ALT-009 in full. The corpus's documented shapes: front-end and human workflow in-platform with compute, messaging, brokering or protocol handling outside; governed store plus analytical store; platform plus enterprise boundary. Each imports the obligations of `anti-patterns.md` AP-D-026 and AP-D-046.

**Key decision criteria.** Essentially all of `decision-criteria.md`. The decision-blocking set for this class specifically: DC-D-040/DC-D-037 (throughput and frequency), DC-D-021 (system of record), DC-D-059 (regulatory regime), DC-D-100 (availability and recovery objective), DC-D-061 (external identity model), DC-D-092 (budget), DC-D-108 (deployment model).

**Related anti-patterns.** All 67, since they are derived from this platform's evidence. Those that specifically *disqualify* this class: AP-D-003, AP-D-035, AP-D-059.

**Evidence.** All twelve canonical files. Load-bearing: `platform-suitability.md` §2, §3, §5, §8; `application-architecture.md` §1, §2; `data-architecture.md` §2, §3; `automation-architecture.md` §3, §4; `integration-architecture.md` §3, §4, §12; `security.md` §1, §2, §4; `governance.md` §1, §2; `alm-devops.md` §1, §2; `performance-scale.md` §2, §3, §4; `licensing-cost.md` §1, §2, §7; `operations-support.md` §1, §6; `architecture-patterns.md` §3, §5, §13.

**Confidence:** MEDIUM — the manifest's own overall figure for the corpus, and capped for the same reason: the positive-fit half rests substantially on inference from *absent* constraint violations rather than on endorsement or measurement, and no empirical performance evidence exists.

---
### ALT-005 — Custom development

**Class.** A conventional application stack built and operated by a development team: a custom web or mobile front end, a dedicated backend or API, a database of the team's choosing, deployed and run on infrastructure the organisation selects.

**Problem types it fits.** Requirements whose dominant characteristic is a hard non-functional constraint the low-code platform documents as unsupported; product-grade or consumer-grade experiences; capabilities the organisation intends to sell or embed; requirements with strict portability or deployment mandates.

**Requirement triggers.** Each is a documented *absence* on the platform side, not a claim about custom development's merits:

| Trigger | Documented platform boundary |
|---|---|
| Data permanently outside the governed store, with an experience requiring platform data features on it | Virtualization forfeits audit, row/column security, search, offline, rollups and charts, and the choice is irreversible (`platform-suitability.md` PS-56; `application-architecture.md` §1 row 10) |
| Guaranteed throughput or a contractual service level | No published concurrent-user figure, no published end-to-end latency figure, no cross-region recovery-time commitment (`performance-scale.md` PF-09, PF-14, PF-40) |
| Product-grade consumer experience; native gestures; a design system | Theming on the record-centric surface is colours, font and logo only; the task-focused surface is maker-dependent; the ladder ends at custom web (`application-architecture.md` AA-14, AA-36) |
| A branded native mobile app **with push notifications** | Unsatisfiable in-platform (`application-architecture.md` AA-40, AA-46) |
| A public API for third parties | Not the platform's purpose (`platform-suitability.md` PS-36, PS-51) |
| Custom synchronisation or conflict rules; offline in a browser; offline over non-governed data | Unsupported (`application-architecture.md` AA-42…AA-44) |
| Embedding in a native product; intercepting proxies | POOR / CUSTOM (`platform-suitability.md` PS-12, §2 row 24) |
| Real computation as a step | No compute-sizing dial exists (`performance-scale.md` PF-45, B-14) |
| Customer-hosted, air-gapped or on-premises deployment | Unsupported — SaaS only (`platform-suitability.md` PS-47; `anti-patterns.md` §6 V-D-01) |
| Per-user licensing uneconomic at the audience's scale | An economic, not technical, trigger (`application-architecture.md` §1 row 10; `licensing-cost.md` §6) |
| Portability off the vendor: the interface, expression language and automations must be re-hostable | Not portable; data and server-side .NET components are (`platform-suitability.md` PS-51) |
| Behaviour must be frozen / change controlled per release | Mandatory semi-annual waves and rolling deprecations (`platform-suitability.md` PS-50) |

**Strengths.** Every constraint above becomes a design choice rather than a boundary: compute sizing, deployment location, networking, data engine, transaction semantics, release cadence, portability, experience fidelity, and the ability to expose an API. Also the only class in which the organisation controls the *whole* dependency chain, which is what makes a contractual commitment underwritable.

**Weaknesses.** The corpus is careful not to assert cost or speed, but it does hold specific negative facts about the code-first alternatives it recommends — 9 documented items about a serverless compute host and 9 more about a broker architecture (`automation-architecture.md` §8.3, §8.4). Structurally: **connectivity must be built.** The comparison the corpus records is *"A dozen built-in binding types - Write code for custom bindings"* against 1,400+ connectors — so every integration the platform would have supplied as a connector becomes development and maintenance. Human-workflow constructs (approval routing with delegation, escalation and an action centre, on standard entitlement) have **no equivalent** and must be built. And the vendor's own cost caution applies here directly: *"Custom solutions might seem powerful but often require a bigger budget for development, licensing, and support. Justify higher costs with clear business value"*; and *"more code-first developer work is needed to develop and maintain the RESTful service and data layer."* Finally, **team capability is a hard gate**: *"Choose services that your team knows how to use, or commit to training them before you choose a service"* — and a design needing capability the team lacks is a documented RISK (`platform-suitability.md` PS-40) and a **composed disqualifier** (`architecture-patterns.md` §13: *"Hybrid architecture required + no pro-dev/enterprise platform capability available → POOR FIT"*).

**Architectural consequences.** Every architectural decision is now the team's, including the ones the platform previously made: authorization model, audit, retention, concurrency semantics, transaction boundaries, resilience, observability. Freedom and obligation are the same fact.

**Security / governance consequences.** Nothing is inherited. The corpus's rule for external estate applies in full: identities, role-based access, network exposure, secret management, policy baseline and diagnostic access must all be designed (`security.md` SEC-XB-02; `governance.md` GOV-XB-01). Against that: capabilities that are **impossible** in the governed store become available — most sharply *"confidential even from administrators"*, which `security.md` §4 row 6 records as **not achievable** in the platform's data layer.

**Delivery / ALM consequences.** A full software supply chain: source control, branching, review, infrastructure-as-code, environments, automated testing, release management. Where the organisation already has this, it is a strength — the class inherits a mature capability instead of building on the four-rung ladder. Where it does not, it is the dominant cost and risk, and the corpus's guidance requires infrastructure-as-code, source control and continuous delivery for these components, plus *"predictable automated pipelines with testing/quality gates"* (`alm-devops.md` §14.2).

**Performance / scale consequences.** The envelope becomes a sizing decision rather than a published limit — which is a genuine advantage where the platform's envelope is the blocker. But **note the symmetry**: this corpus has *no empirical benchmark for any technology*, including these (manifest NB-07; `automation-architecture.md` §8.7: *"No empirical throughput or latency measurement for any technology here"*). "Custom will be fast enough" is exactly as unevidenced as "the platform will be fast enough". Documented ceilings do exist on the code-first side and must not be overlooked: a **230-second maximum HTTP response on every plan** of one serverless host, a 5/10-minute execution cap on its legacy plan (itself legacy, with a dated retirement), cold starts unless always-ready instances are paid for continuously, and a 600-active-outbound-connection cap on that plan.

**Cost / TCO consequences.** **No universal direction.** The corpus rejects both universal claims (§2.2) and replaces them with the ten-dimension method (`licensing-cost.md` §6). The dimensions that most often favour this class: audience (cost does not scale with people or with app scope), machine workload at high volume, and existing sunk delivery capability. The dimensions that most often favour the platform: build and change effort, connectivity, observability and support already provided, and the absence of a second estate to fund. **No comparative TCO study of the platform against named alternatives was found** (`licensing-cost.md` LC-U-04, §7.3 item 51) — so the crossover is an engagement calculation, and the corpus says so.

**Operations consequences.** Everything must be built and staffed: monitoring, alerting, incident response, backup, recovery, drills, retirement. Against that, everything is *available* to be built at the depth the requirement needs, rather than gated behind an environment class. Where 24×7 operation with a contractual recovery objective is required, this class can underwrite it and the platform cannot (manifest NB-03).

**When preferable to Power Platform.** When a documented platform absence dominates the requirement (the trigger table); when the audience's scale makes per-user or per-scope economics unattractive; when portability or a customer-hosted deployment is mandated; when the organisation already has a mature delivery and operations capability and the requirement is a long-lived product rather than a business process.

**When Power Platform is preferable.** When the requirement fits ALT-004's positive triggers; when connectivity breadth over the existing estate is the actual value; when human-workflow constructs are central; when there is no delivery or operations capability to build on — the corpus's own caution runs in this direction (*"Justify higher costs with clear business value"*); when time-to-value from a business-owned maker population is decisive; and when *"one difficult step"* is the only blocker, in which case the answer is ALT-009, not this class (`integration-architecture.md` §12.9).

**Hybrid opportunities.** The most common and best-documented composition in the corpus: keep the experience, the human workflow and the business record in-platform, and put the one exceeding step — compute, protocol, duration, guarantee, network reach, or secret-free identity — in code (`architecture-patterns.md` AP-05; `automation-architecture.md` §6.2). Also: a custom front end over the platform's data and services where the experience is the blocker but the data model is not.

**Key decision criteria.** DC-D-108 (deployment model), DC-D-105/DC-D-106 (portability and exit), DC-D-012 (interaction complexity), DC-D-020 (native distribution and push), DC-D-057 (compute intensity), DC-D-084 (response time), DC-D-100 (availability and recovery objective), DC-D-028 (atomicity span), DC-D-110 (team skills), DC-D-092 (budget), DC-D-004 (lifespan).

**Related anti-patterns.** `anti-patterns.md` AP-D-003 (the under-engineering case that leads here), AP-D-002 (arriving here by preference for code — the corpus's counterweight), AP-D-026 and AP-D-046 (the obligations this class carries), AP-D-060 (costing it asymmetrically), AP-D-048 (assuming it will be fast enough without measurement).

**Evidence.** `platform-suitability.md` PS-08, PS-12, PS-36, PS-40, PS-44, PS-47, PS-50, PS-51, PS-56, §2 rows 17, 23, 24, 29, 32, §9; `application-architecture.md` AA-14, AA-30, AA-35, AA-36, AA-40, AA-42…AA-44, AA-46, §1 rows 5, 10; `automation-architecture.md` AT2-32, AT2-33, AT2-34, N-25…N-33, §8.3, §8.7, §3.B rows 10–17; `integration-architecture.md` §12.7, §12.9, I-31, I-38 (MS-V capability facts only); `performance-scale.md` PF-14, PF-45, B-14, B-16, PF-U-01; `licensing-cost.md` §6, LC-U-04, §7.3 item 51; `security.md` §4 row 6, SEC-XB-02; `governance.md` GOV-XB-01; `alm-devops.md` §14.2; `architecture-patterns.md` AP-05, §13; manifest NB-03, NB-07.

**Confidence:** MEDIUM. The *triggers* are HIGH (documented platform absences, several re-verified). The *comparative* claims are deliberately absent, because the corpus holds no comparative TCO or benchmark evidence — which is itself the finding.

---

### ALT-006 — Cloud-native services

**Class.** Purpose-built managed services composed into an architecture: API management, code-first orchestration, serverless compute, message brokers and event services, streaming, data pipelines, purpose-built data stores, worker services.

**Problem types it fits.** Integration and orchestration at enterprise scale; message-guaranteed workloads; event streams; bulk data movement and transformation; compute; long-running and resumable processes; private-network execution; protocol handling the low-code platform cannot express.

**Requirement triggers.** The corpus states these as boundaries that force the work out of the low-code automation and integration layer:

| Trigger | Documented reason |
|---|---|
| Messages must not be lost, duplicated or reordered; poison messages need a destination | The guarantee is a property of the **transport**, not of the automation; there is **no dead-letter and no circuit-breaker construct** in the low-code automation (`integration-architecture.md` IA-15, IA-46, X-09) |
| A producer bursts faster than the consumer or target can absorb | The documented remedy is queue-based load levelling and competing consumers *"not larger retry counts inside the automation tool"* (`automation-architecture.md` §4.2) |
| Continuous event streams | A run per event is the wrong unit; a streaming service is the documented technology (`automation-architecture.md` AT2-26) — though **unsized in this corpus** (U-13) |
| Fan-out/fan-in, sub-orchestration, resumable stateful workflow, mutable control state | The declarative designer does not express these; a durable orchestrator is the documented answer (`automation-architecture.md` AT2-33, AT2-34) |
| Real computation | No compute-sizing dial in-platform (`performance-scale.md` PF-45) |
| A process must outlive 30 days or resume mid-way after a failure or deployment | Run duration is a **30-day hard ceiling including human waits**, and run state is not addressable once the run ends (`automation-architecture.md` AT2-13, AT2-14) |
| Private-network runtime, managed identity, resource-level access control surviving the author's departure | Platform access control *"works at the user level"* and profile reverts on departure; managed identity covers only server-side platform code (`automation-architecture.md` AT2-31, AT2-49; `integration-architecture.md` IA-31) |
| Code-first delivery: local debugging, infrastructure-as-code, branch review of the integration definition, zero-downtime deployment | Capability facts from vendor-side positioning, fenced (`integration-architecture.md` §12.7, I-38 `MS-V`) |
| B2B / trading-partner protocol handling | Assigned explicitly to the integration platform tier, not the low-code automation (`integration-architecture.md` §12.2) |
| Bulk data movement or transformation at scale | *"complex business logic and large-scale transformation do not belong in cloud flows"*; a data pipeline owns bulk movement (`platform-suitability.md` PS-07; `integration-architecture.md` §12.8) |
| Message-level audit, replay or long retention | Native retention is ~30 days; the durable option requires a broker with dead-lettering plus a status store (`integration-architecture.md` §12.6) |
| High-ingest timestamped metrics and events | Routed by the vendor's own data-store guidance to a purpose-built engine — **not** to a relational store, which the corpus flags as a familiarity-driven error (`data-architecture.md` SQ2-06, DAP-36) |
| Sustained throughput past the three-meter envelope with no natural partitioning | (`integration-architecture.md` §12.4) |

**Strengths.** Each service is purpose-built for the property the low-code layer lacks: durable ordered delivery with duplicate detection and dead-lettering; contract versioning, quota enforcement, transformation, caching and tracing at an API tier; determinism-checked durable orchestration; compute plans sized to the workload; private networking, managed identity and resource-scoped access control; infrastructure-as-code and zero-downtime deployment; capture and replay for streams. Also: composability — the corpus documents seven compositions that are *"documented, not merely possible"*.

**Weaknesses.** The corpus deliberately collected negative evidence here, and it is substantial (`automation-architecture.md` §8.2–§8.4, 24 items). Load-bearing examples:
- **Escalation does not always relieve the ceiling.** The code-first orchestration service has the **identical** 500-action / 8-nesting ceiling and prescribes the same remedy; its consumption tier has the **same 120-second synchronous window**; *"'Move to Logic Apps' does not relieve it."*
- **A stateless choice silently shrinks the envelope** — 5-minute run duration, 100-item arrays, 100 loop iterations.
- **Brokers are bounded too:** 256 KB standard-tier messages (forcing a claim-check for documents), 1,000 operations per second on that tier, connector-side session caching that **silently evicts** beyond 1,500 sessions, managed identity to the broker available only from the code-first orchestrator, and **all connector triggers are long-polling with a 30-second wait — a latency floor, not push**.
- **The event service guarantees neither ordering nor exactly-once**, so the consumer must be idempotent anyway; the streaming service has **no dead-lettering**.
- **Orchestrator code is constrained** (no current time, random identifiers, bindings, I/O, statics, environment variables, HTTP, sleeps or arbitrary async), its own **non-determinism guard is explicitly unreliable**, deploying a change **can break in-flight orchestrations**, and one hosting model has a **dated end of support** forcing a migration.
- **Connectivity must be coded** (a dozen bindings versus 1,400 connectors).
- **A queue is not infinite, and autoscaling can just move the overload** downstream — into the platform's own per-identity meter, which is the case that matters here.
- **The hybrid shape itself** imports two lifecycle models, two access-control models, two monitoring surfaces and two retention windows, and *"correlation across the boundary exists only if the design propagates an explicit id."*
- **The private-egress collision:** the platform's own event-publishing mechanism *"doesn't support VNet"*, so "events out to a broker" and "all egress private" cannot both hold through that mechanism.

**Architectural consequences.** The topology becomes explicit and multi-tier: producer, transport, consumer, status resource, reconciliation. Two of the corpus's patterns are effectively mandatory companions — asynchronous background processing needs a **status resource** (*"you must implement a mechanism"*), and any at-least-once transport needs **idempotent consumers**.

**Security / governance consequences.** Strong controls available (managed identity, resource-scoped access control, private endpoints, vault-held secrets, policy baselines, API-tier authentication and quotas) — and **none of them inherited**. These resources are **not governed by the platform's data policies**, so their access model, network exposure, policy baseline and diagnostic access must be designed in the other domain, with a named owner. *"'Move it to Azure for security' is incomplete unless the Azure side has an explicit security baseline."*

**Delivery / ALM consequences.** Requires a **second coordinated supply chain**, with the release unit declaring contract compatibility and sequencing; deploying one side alone is admissible only under a guaranteed compatibility policy. Compensation, reconciliation and idempotency artefacts are **part of the contract** and need change control equal to the forward path.

**Performance / scale consequences.** Higher and more shapeable ceilings, with the documented exceptions above. **The same evidential limit applies**: no empirical benchmark exists for any of these services in this corpus, and two of the three brokers are recommended *on positioning, not on capacity* because their quota envelopes were never fetched (`automation-architecture.md` U-13; `integration-architecture.md` U-03).

**Cost / TCO consequences.** A second billing model with consumption meters of a different shape — which is precisely why it can win on machine-heavy workloads and lose on people-heavy ones. Costs the corpus names but does not price: the estate itself, its administration, its monitoring and log retention (*"There are cost implications for storing and querying logs"*), its pipelines, and the skills. An API tier's own tier choice locks in network and availability capabilities. `licensing-cost.md` LC-U-06 leaves gateway-at-scale infrastructure cost open.

**Operations consequences.** Deeper observability is *available* — and must be built and staffed. Two surfaces to correlate across, with no platform-provided correlation. A named operator, on-call rota, policy baseline, backup position and cross-platform runbook are **preconditions**, not follow-ups: without them the pattern is *"unavailable, not merely expensive"*.

**When preferable to Power Platform.** When a trigger above fires and the requirement is confined to the integration, orchestration, compute, messaging or data-movement responsibility. Most decisively: guaranteed delivery, streams, real computation, processes outliving 30 days, private-network execution, protocol handling, bulk movement, and message-level audit or replay.

**When Power Platform is preferable.** When the work is a bounded sequence of connector calls over the existing estate, where *"the alternatives' technical advantage here is nil and their operating cost is not"*; when a human decision is central; when the volume can be delegated to a bulk mechanism with the automation orchestrating; and — explicitly — **when the organisation has no operating model for the second platform**, in which case the corpus's answer is *"single platform + a tripwire, not a paper hybrid"*.

**Hybrid opportunities.** This class is *usually* ALT-009 rather than a whole-solution replacement. The documented shapes: automation as the business-facing front door with compute outside; broker between producer and consumer with an idempotent in-platform consumer; API tier as the contract with a service behind it holding the domain logic; queue plus status resource for long-running work; data pipeline for bulk with the platform consuming the result.

**Key decision criteria.** DC-D-041 (delivery guarantee and ordering), DC-D-037 (frequency and peak shape), DC-D-040 (sustained throughput), DC-D-049 (process duration), DC-D-050 (synchronous response), DC-D-054 (failure semantics), DC-D-057 (compute intensity), DC-D-044 (network boundary), DC-D-045 (protocol), DC-D-101 (observability depth), DC-D-070 (organisational maturity), DC-D-110 (team skills), DC-D-096 (external service consumption cost).

**Related anti-patterns.** `anti-patterns.md` AP-D-005 (arriving here without a trigger), AP-D-023 (mediation with no requirement), AP-D-026 (no operator — the gate), AP-D-046 (single-sided supply chain), AP-D-015/AP-D-016 (the under-engineering cases that lead here), AP-D-002 (Y-12: assuming this is the boundary when an enterprise platform already owns it).

**Evidence.** `automation-architecture.md` §3.B, §4.2, §4.3, §6, §8.2, §8.3, §8.4, §8.6, AT2-26, AT2-28…AT2-34, AT2-49, AT2-53, N-17…N-42, N-51…N-53, U-12, U-13; `integration-architecture.md` §3, §4.2, §4.3, §12.2, §12.4…§12.8, IA-15, IA-46, I-12, I-20, I-27, I-29, I-44, I-38 (`MS-V`), U-03, U-11, U-12, U-19; `platform-suitability.md` PS-07, PS-08, PS-24, PS-44, PS-48, AP-15; `performance-scale.md` PF-45, B-07…B-14; `architecture-patterns.md` AP-02…AP-05, AP-08, AP-09, §6.1, §8, Y-03, Y-04, Y-13, §13; `data-architecture.md` SQ2-06, DAP-36, SY-01, SY-18; `security.md` SEC-XB-02; `governance.md` GOV-XB-01; `alm-devops.md` §14.2, §14.5; `licensing-cost.md` §6, LC-U-06; `operations-support.md` §13.1.

**Confidence:** MEDIUM-HIGH on the triggers and on this class's own documented limits (the corpus collected both deliberately); MEDIUM on any comparative conclusion, and LOW on capacity for the two brokers whose envelopes were never fetched.

---

### ALT-007 — An existing enterprise platform owns the capability

**Class.** The capability is delivered by a platform that already owns the relevant domain in the organisation: the enterprise resource planning or customer system, the service-management platform, the business-process or workflow engine, the integration platform or message backbone, the data platform, or an industry-specific system.

**Problem types it fits.** Requirements sitting inside a domain another platform already masters — financial posting, service requests, case management, HR processes, procurement, master data, integration and message routing, analytical workloads.

**Requirement triggers.**
- **The integration responsibility already has an owner**, with a published contract. The corpus makes this **step 1** of its classification test and is candid about why: *"Nothing in the fetched Microsoft material tells an architect to check this, which is precisely why it must be step 1"* (`integration-architecture.md` §12.1).
- **An enterprise workflow or process engine already owns this process class.** *"Adding Power Automate duplicates the operating model rather than reducing it"* (`automation-architecture.md` §4.3, AT2-52).
- **The entity's authority lives there** — most sharply for authoritative ledgers, which the vendor's own bidirectional product *deliberately excludes* to avoid shadow behaviour (`integration-architecture.md` I-26).
- Audit, compliance or authorization obligations are already enforced and evidenced there (`data-architecture.md` §6).
- Analytical or high-ingest workloads that the vendor's own guidance routes to a purpose-built platform (`data-architecture.md` DA-51, SQ2-06).
- B2B or trading-partner protocol handling (`integration-architecture.md` §12.2).

**Strengths.** Governance, ownership, operating model, controls and audit already exist. The corpus frames the reuse question as **a governance decision before a product decision** (`governance.md` GOV-XB-02) and lists the concrete strengths of a governed boundary: *"one contract, one policy point, one audit trail"*; discovery with control; federated ownership with central oversight; legacy modernisation without migration; partner onboarding that stops being per-integration; and — importantly — *"it removes the leaver risk from the integration path"*, moving ownership from a maker's personal licence to a platform team with resource-level access control. This class is also **the only pattern in the corpus that can be satisfied by a non-Microsoft platform**, which the corpus calls *"the antidote to 'Azure is automatically the answer'"*.

**Weaknesses.** Documented, and mostly organisational rather than technical: **lead time and loss of autonomy** — every new capability needs a change owned by another team, and *"nothing in the fetched evidence quantifies this"*; a second or third platform to fund and operate; **double abstraction** where the platform reaches it through a generated connector over an API over a backend, so three contracts must stay aligned; **governance can become the bottleneck**, at which point makers route around it — the failure mode policy is meant to prevent, made messier by its own enforcement lag; **the boundary that exists only on paper**, where a stale or incomplete published contract means makers use the direct path anyway and the boundary becomes a fiction with a maintenance cost; and a **single point of failure at estate scale**. Two evidential weaknesses must be stated plainly: manifest **NB-06** records that this pattern is *supported synthesis (`INF`), not a Microsoft-endorsed pattern*, and `architecture-patterns.md` calls it *"the weakest-evidenced pattern in the file and the most consequential for governance"* (`APR-U-08`). And **the corpus contains no evaluation of any incumbent platform**: *"no Microsoft or independent source evaluates incumbent BPM/ESB platforms; treat as reasoning, not evidence"* (`automation-architecture.md` §3.B row 19).

**Architectural consequences.** The platform's role shrinks to consuming a published contract — the strongest simplification available on the integration axis. Where the incumbent owns the whole capability, there is no platform architecture at all. Where it owns part, the boundary becomes the enclosing structure and the other patterns operate *inside* it.

**Security / governance consequences.** Usually the strongest position of any class: one authentication point, backends network-isolated, quotas enforced, secrets in a vault, and directory-based identity for both developers and consumers. Note the licensing catch: several **boundary controls are managed-environment-gated** on the platform side, so even a boundary architecture can carry a premium-licence precondition.

**Delivery / ALM consequences.** The incumbent's lifecycle applies, with the platform side coordinating against a versioned contract. Where the connector is the seam, `alm-devops.md` ALM-14's obligations apply (separate solution, import order, and the unmanaged-layer conflict). Lead time is the incumbent's.

**Performance / scale consequences.** *"Moves the ceiling to the boundary's own capacity and tier"* — and, critically, **the boundary does not lift the platform's own meters for individual artefacts**, which the corpus notes is *"frequently missed"*. No capacity or latency figure for any boundary component exists in the corpus (`APR-U-02`).

**Cost / TCO consequences.** Often the lowest incremental cost, because the platform and its team are already funded — the *"existing sunk capability"* dimension. Against it: the boundary's own tier costs, the coordination overhead, and (where the incumbent must be extended) enterprise-application change rates that can be the highest in an estate. No comparative figures exist in this corpus.

**Operations consequences.** Requires a named platform team, a published catalogue, a maker-onboarding process, and **joint incident management across the boundary**. Where those exist, this is the best-operated class; where the boundary is nominal, it is among the worst.

**When preferable to Power Platform.** When the domain's authority, controls and audit already live there; when an integration platform with a published contract already exists; when a process engine already owns the process class; when the requirement is trading-partner protocol handling, bulk movement or analytics; when duplicating the operating model would cost more than it saves.

**When Power Platform is preferable.** When the incumbent **cannot meet** a stated requirement — recorded per requirement, since *"reuse is not automatic"*; when its lead time or change cost is incompatible with a genuine deadline (recorded as a constraint, with an expiry); when the requirement spans several systems none of which owns it; when the experience layer is the deliverable and the incumbent supplies only the data.

**Hybrid opportunities.** The definitive shape: the incumbent keeps authority and the contract; the platform supplies the experience and the human workflow, consuming the contract. This is the composition most often available and least often considered, because it requires talking to another team.

**Key decision criteria.** DC-D-021 (system of record), DC-D-111 (existing enterprise platform estate), DC-D-036 (integration ownership), DC-D-045 (protocol), DC-D-070 (organisational maturity), DC-D-073 (support ownership), DC-D-003 (time to value), DC-D-092 (budget).

**Related anti-patterns.** `anti-patterns.md` AP-D-027 (bypassing the owner — the central one), AP-D-010 (shadow system of record), AP-D-014, AP-D-022 (the estate this class prevents), AP-D-002 (standing up a parallel boundary), AP-D-007.

**Evidence.** `integration-architecture.md` §12.1, §12.2, §12.8, §2.2 step 1, §9 row 23, I-20, I-23, I-26, IA-36, IA-37; `governance.md` GOV-XB-01, GOV-XB-02, GOV-A11; `automation-architecture.md` AT2-52, §3.B row 19, §4.3; `architecture-patterns.md` AP-10 (full entry incl. its honesty note), matrix rows 15, 28, 29, 30, Y-12, APR-U-02, APR-U-08; `data-architecture.md` DA-51, SQ2-06, §2 row 13, §6; `platform-suitability.md` PS-41; `licensing-cost.md` §6; manifest NB-06.

**Confidence:** MEDIUM on the decision logic; **LOW on any specific incumbent's fit**, which the corpus explicitly cannot assess. Both figures should be read alongside NB-06's warning that the pattern itself is `INF`.

---

### ALT-008 — Another low-code platform

**Class.** An enterprise low-code or high-productivity application platform other than the one this pack targets, considered as the primary delivery platform.

**Scope discipline.** `platform-suitability.md` §4.17 places non-Microsoft low-code platforms *"out of this area's scope (handled by other aisa packs)"*, and Block D does **not** reverse that. No vendor ranking, no feature matrix and no performance or productivity comparison appears here. What follows is the narrower thing a decision model needs: **the requirement classes under which this option should be put on the table**, and an honest statement of what this corpus does and does not know.

**Problem types it fits.** Requirements that are recognisably low-code-shaped — business applications, process automation, portals — but which collide with a *structural* property of the target platform rather than with a capability gap that a hybrid could close.

**Requirement triggers.** Only one is evidence-backed in this corpus at the level of a materially relevant distinction; the rest are recorded as candidate triggers with their evidential status stated.

| Trigger | Status |
|---|---|
| **Deployment model: customer-hosted, private-cloud or air-gapped operation is mandated** | **EVIDENCE-BACKED.** The target platform is SaaS-only and disconnected/customer-hosted deployment is *unsupported* (`platform-suitability.md` PS-47; re-verified `anti-patterns.md` §6 V-D-01). At least one enterprise low-code platform documents Kubernetes-based private-cloud and on-premises deployment including *"fully air-gapped private clouds or on-premise"*, with a standalone operator for air-gapped delivery pipelines; a second announced self-hosted deployment (*"your own private or public cloud, or on-premises Kubernetes infrastructure"*, dated 2026-03-31) but **in an Early Access Program, not generally available** (`anti-patterns.md` §6 V-D-04, vendor documentation, capability facts only). This is the one axis on which the corpus can say a comparator documents a generally-available capability the target platform documents as unsupported. |
| Portability and exit: the application layer must be re-hostable | CANDIDATE. The target platform's asymmetry is documented — data and server-side .NET components portable, interface/expression language/automations **not** (`platform-suitability.md` PS-51). The comparators' portability is **`UNKNOWN` in this corpus**; a platform that runs on the customer's own cluster is not thereby portable *off that vendor*. Do not infer. |
| Enterprise development model: strongly typed, code-adjacent, IDE-based, branch-and-merge delivery as the primary model | CANDIDATE, `UNKNOWN`. The target platform's constraints are documented (co-authoring removed on one artefact type; environment-per-maker for parallelism; no supported first-party low-code functional-test framework — `application-architecture.md` AA-06, `alm-devops.md` ALM-17, ALM-23). Whether a comparator materially differs is not established here. |
| Licensing shape mismatch: the audience is very large or the work is machine-heavy relative to the number of people | CANDIDATE, `UNKNOWN` on the comparator side. The target platform's shape is documented (five simultaneous mechanisms, largely people- and scope-driven — `licensing-cost.md` §1), and the corpus retains *"the users-to-work ratio"* as a **hypothesis to test**, not a finding (§5.2). No comparator pricing was fetched; `licensing-cost.md` LC-U-04 stands. |
| Existing organisational estate: the organisation already runs another low-code platform with a delivery team, governance and operations | CANDIDATE, and the strongest *non-technical* trigger. It is the same argument as ALT-007's — reuse of a funded operating model — applied to the application layer. |
| Interface or integration requirements the target platform documents as unsupported | CANDIDATE. Where the requirement is a single step, ALT-009 is the better answer (`integration-architecture.md` §12.9); this trigger applies only where the unsupported property is pervasive. |

**Strengths.** Not assessable from this corpus, with one exception: **deployment-model flexibility**, which is documented on the comparator side and absent on the target side. Everything else — productivity, performance, cost, governance depth, connector breadth, maturity — is **`UNKNOWN` here**, and this file will not guess.

**Weaknesses.** Symmetrically not assessable. What *can* be said, from the target platform's own evidence, is what changing platform costs regardless of destination: the interface layer, the expression language and the automations are **not portable**, so a move is a rewrite of those layers (`platform-suitability.md` PS-51); the connector estate over the existing productivity and business-application estate would have to be re-established; and the human-workflow constructs on standard entitlement have no assumed equivalent. A self-hosted platform also **converts a SaaS availability profile into an operated one**, which is the same obligation `anti-patterns.md` AP-D-026 imposes on any external estate — a named operator, a policy baseline, a pipeline, monitoring, backup and on-call. That obligation is a *documented consequence*, not a criticism of any product.

**Architectural consequences.** A different platform's constraint set, unknown to this corpus. Two consequences are knowable: the existing estate's integrations must be re-established, and a self-hosted deployment makes infrastructure an owned responsibility.

**Security / governance consequences.** Unknown per comparator. Knowable: a self-hosted deployment satisfies residency and network mandates the target platform cannot, and imports the full governance obligation for the hosting estate.

**Delivery / ALM consequences.** Unknown per comparator. Knowable: an in-flight migration is a rewrite of the non-portable layers; and where a comparator's self-hosted capability is in early access rather than general availability, adopting it on a critical path is `anti-patterns.md` AP-D-057.

**Performance / scale consequences.** **`UNKNOWN`, and symmetrically so.** The corpus holds no empirical benchmark for the target platform either (manifest NB-07). No performance claim in either direction is available.

**Cost / TCO consequences.** **`UNKNOWN`.** `licensing-cost.md` LC-U-04 and §7.3 item 51 record that no comparative TCO study was found, and §6 replaces comparison-by-verdict with comparison-by-method. Any comparison must price both candidates on the same ten dimensions, and the self-hosted case must include the hosting estate.

**Operations consequences.** Unknown per comparator. Knowable: self-hosted means the organisation operates the platform, not just the application.

**When preferable to Power Platform.** With current evidence, one class stands on its own: **a mandated customer-hosted, private-cloud or air-gapped deployment**, where the target platform is documented as unsupported and at least one comparator is documented as capable. Beyond that, the honest output is that the option should be **evaluated in a separate exercise** — which is what the aisa pack structure already provides for.

**When Power Platform is preferable.** When none of the triggers fires — and in particular when the organisation's estate, entitlements and skills already centre on it, which is the mirror of the existing-estate trigger above. Also when the blocker is a *single step* rather than a structural property, in which case ALT-009 is cheaper than a platform change.

**Hybrid opportunities.** Multi-low-code estates are outside this corpus. The realistic composition is organisational rather than architectural: the platform that owns each domain keeps it, with integration between them treated as any other enterprise integration (ALT-007's logic).

**Key decision criteria.** DC-D-108 (deployment model — the decisive one), DC-D-105/DC-D-106 (portability and exit), DC-D-111 (existing platform estate), DC-D-110 (team skills), DC-D-093/DC-D-094 (entitlement and licensing shape), DC-D-059 (regulatory regime), DC-D-070 (organisational maturity).

**Related anti-patterns.** `anti-patterns.md` AP-D-035 (the trigger discovered late), AP-D-003, AP-D-057 (adopting an early-access capability on a critical path), AP-D-002 (switching platform by preference rather than trigger), AP-D-060 (comparing asymmetrically).

**Evidence.** `platform-suitability.md` PS-47, PS-51, §2 rows 29, 32, §4.17 (scope statement); `application-architecture.md` AA-06, §1 row 10; `alm-devops.md` ALM-17, ALM-23; `licensing-cost.md` §1, §6, LC-U-04, §7.3 item 51; `anti-patterns.md` §6 V-D-01, V-D-04 (external verification, vendor documentation, capability facts only); manifest NB-07.

**Confidence:** **LOW overall**, and deliberately so. **MEDIUM-HIGH** on the single deployment-model trigger (documented on both sides, re-verified 2026-09-03, with the early-access caveat stated). `UNKNOWN` on every comparative dimension. This is the largest evidence gap in Block D and is reported as such in §6.

---
### ALT-009 — Hybrid architecture

**Class.** Responsibilities are deliberately decomposed across two or more technologies, each holding what it is documented to do well: the low-code platform for the experience, the human workflow and the business record; another technology for the step, the guarantee, the compute, the protocol, the network reach or the data shape it cannot supply.

**This is a first-class option, not a compromise.** The corpus treats decomposition as the *normal* answer to a bounded excess, and treats relocating the whole solution because of *"one difficult step"* as an error (`integration-architecture.md` §12.9). Its own escalation ladder is a hybrid ladder.

**Problem types it fits.** Requirements that are overwhelmingly low-code-shaped with a bounded, nameable exception. Also: requirements that are genuinely two-shaped — an interactive business application over a governed store *plus* a high-volume integration; a portal *plus* an analytical workload.

**Requirement triggers.** The corpus's documented hybrid-forcing boundaries:

| Trigger | Documented shape |
|---|---|
| A step needs real computation | Automation as the business-facing front door, compute in a serverless function (`automation-architecture.md` §4.2) |
| Messages must not be lost, duplicated or reordered | Broker carries the guarantee; the platform is producer or **idempotent** consumer, *"never the guarantee itself"* (`integration-architecture.md` §2.2 step 2) |
| A producer bursts faster than the consumer or target can absorb | Broker between them, converting a whole-run failure into a per-message failure (`automation-architecture.md` §4.2) |
| One business operation must be atomic across the governed store and anything else | Saga with per-step idempotency keys, compensating actions, persisted in-doubt state, irreversible steps last, and a human resolution path (`automation-architecture.md` §4.2) |
| The process must outlive 30 days or resume mid-way | State in a business process record with a re-triggering automation, or durable orchestrator state (`automation-architecture.md` §4.2) |
| Enterprise-grade observability is required | Telemetry export for correlation and alerting, accepting that it is managed-environment-only, *"not 100% lossless"*, and unavailable in sovereign clouds (`automation-architecture.md` §4.2) |
| ≥ 2 consumer classes need one backend capability; or contract versioning, rate limiting, composition, caching, tracing, semantic translation, private reach with credential isolation, or discovery is required | API-mediated access (`integration-architecture.md` §4.2) |
| Aggregation, charts or cross-period history over growing data | Analytical copy from day one (`data-architecture.md` §3) |
| Platform data features required on externally-owned data | Scoped one-way replica as a disposable read model (`data-architecture.md` DA-45, DA-46) |
| On-premises payload above the gateway ceiling; or a network the platform cannot enter | An in-network component — a self-hosted API gateway is the documented mechanism (`architecture-patterns.md` matrix row 24, `integration-architecture.md` §12.5) |
| "No stored secrets" on a leg the sanctioned mechanism does not serve | Server-side platform code with managed identity, or a worker outside (`architecture-patterns.md` matrix row 26) |
| Work exceeds a synchronous window or must survive restarts | Background processing **with a status resource** — *"you must implement a mechanism"* (`architecture-patterns.md` AP-09) |

**Strengths.** Each responsibility sits where its constraints are satisfiable, so no single technology is asked to do what it documents itself as unable to do. It preserves the parts of the low-code platform that are genuinely differentiated — connector breadth over the existing estate, human-workflow constructs on standard entitlement, the governed store's authorization and audit, business-owned change — while removing the constraint that would otherwise disqualify the whole option. The corpus documents **seven compositions that are "documented, not merely possible"**, so the shapes are evidenced rather than invented. It also keeps a **de-escalation path**: when the forcing requirement disappears, the external component can be retired (`architecture-patterns.md` §6.3) — an option a whole-solution relocation forecloses.

**Weaknesses.** The corpus collected these deliberately as *"negative evidence against HYBRID as a shape"*:
- **A second operating model.** *"a cost and skills commitment well beyond a Power Platform app"*, with the other platform billed separately.
- **Doubled models.** *"Two ALM models, two RBAC models, two monitoring surfaces, two retention windows."*
- **Correlation is not provided.** *"Correlation across the boundary exists only if the design propagates an explicit id"* — no platform-provided cross-boundary correlation is documented. This is the cross-cutting problem every hybrid creates (`automation-architecture.md` §6.4).
- **Availability profile changes.** Introducing an operated component *"converts a SaaS availability profile into an operated one; that cost belongs in the option"* (`architecture-patterns.md` §3.1).
- **Two supply chains, with sequencing.** The release unit must declare contract compatibility and order; deploying one side alone is admissible only under a guaranteed compatibility policy.
- **Governance does not extend.** The external estate is not governed by the platform's data policies; its access model, network exposure, policy baseline, cost owner and diagnostic access must all be designed elsewhere.
- **Recovery crosses the boundary.** Restoring one side rewinds one participant while the other retains later state, so a post-restore reconciliation step with a business sign-off owner is mandatory.
- **Compensation artefacts are contract artefacts.** Idempotency keys, mapping rules, compensating actions and reconciliation schemas need change control equal to the forward path.
- **The private-egress collision.** The platform's own event-publishing mechanism does not support private networking, so "events out to a broker" and "all egress private" cannot both hold through that mechanism.

**Architectural consequences.** An explicit boundary with a versioned contract, a propagated correlation identifier, an idempotency strategy on any at-least-once path, a status resource for anything asynchronous the caller cares about, and a reconciliation pass wherever state is duplicated. These are not refinements; they are the definition of the pattern.

**Security / governance consequences.** A **second enforcement plane** that the platform's controls do not reach. `governance.md` GOV-XB-01 lists the gate: a named owning team; inventory and tagging; access and privileged-access model; policy and security baseline; budget and cost owner; delivery pipeline owner; monitoring and alert ownership; backup and recovery position. Until those exist, the pattern *"is not production-ready"*. Compensation and replay identities are **privileged integration identities** and need least privilege, separation from interactive users, and auditing (`security.md` SEC-XB-04).

**Delivery / ALM consequences.** Two coordinated supply chains with declared sequencing (see `anti-patterns.md` AP-D-046). Where the seam is a generated connector, its own obligations apply: separate solution, explicit import order, and the unmanaged-layer conflict with production integrity control — which the corpus insists must be redesigned or exception-recorded, **never silently overridden**.

**Performance / scale consequences.** Relieves the specific ceiling that forced the split — and **does not relieve the others**. Two cautions the corpus states explicitly: a boundary *"does not lift the platform's ceilings for individual artefacts"*, and autoscaling a consumer without bounding its aggregate downstream rate *"only moves the overload to downstream dependencies"* — which, when the consumer writes back into the governed store, means straight into the per-identity meter.

**Cost / TCO consequences.** Two billing models. `licensing-cost.md` §6 requires the **external estate** and **observability/support** dimensions to be priced for the hybrid option specifically — the corpus's named failure is evaluating a hybrid on the low-code cost alone (`anti-patterns.md` AP-D-060). Against that: a hybrid can be *cheaper* than either extreme, by keeping the people-heavy part on entitlement the organisation already owns and the machine-heavy part on a consumption meter that matches it.

**Operations consequences.** A cross-platform runbook, joint incident management, correlated telemetry, and a recovery procedure spanning both sides. The corpus's operational-maturity model puts these at the business-critical class and above; below it, a hybrid is usually the wrong answer for operating-model reasons rather than technical ones.

**When preferable to a single platform.** When the excess is **bounded and nameable**, the organisation can operate the second estate, and the remaining requirement is genuinely well-served in-platform. Also when the requirement is genuinely two-shaped.

**When a single platform is preferable.** Two cases, both documented. **Stay in-platform** when there is no operating model for the second estate — *"single platform + a tripwire, not a paper hybrid"* (`automation-architecture.md` §9 row 22), because a hybrid without an operator is *unavailable*, not merely expensive. **Leave entirely** when the exceeding property is pervasive rather than bounded — when the deployment model, the atomicity requirement, the experience fidelity or the contractual availability commitment applies to the *whole* solution (ALT-005, ALT-006, ALT-007, ALT-008).

**Hybrid opportunities.** This class *is* the composition. Its documented forms: platform + serverless compute; platform + broker + workers; platform + API tier; platform + analytical store; platform + enterprise boundary; platform front end + custom API and data layer; platform + in-network gateway.

**Key decision criteria.** DC-D-070 (organisational maturity — the gate), DC-D-073 (support ownership), DC-D-110 (team skills), DC-D-083 (cross-boundary deployment coordination), DC-D-101 (observability depth), DC-D-096 (external service cost), DC-D-091 (end-to-end availability), plus whichever criterion forced the split.

**Related anti-patterns.** `anti-patterns.md` AP-D-026 (no operator — the gate), AP-D-046 (single-sided supply chain), AP-D-059 (composed disqualifier), AP-D-005 (hybrid with no trigger), AP-D-060 (costed on one side only), AP-D-006 (never de-escalated), AP-D-017 (idempotency, which every at-least-once hybrid needs).

**Evidence.** `architecture-patterns.md` AP-05, AP-09, AP-10, §3.1, §3.2, §6.1, §6.2, §6.3, §5.1, §13, Y-13; `automation-architecture.md` §4.2, §6, §6.4, §8.6, AT2-53, N-51…N-53, §9 row 22; `integration-architecture.md` §4.2, §4.3, §12.5, §12.9, IA-24, I-44; `data-architecture.md` §3, DA-45, DA-46, §6 (hybrid bullet); `security.md` SEC-XB-02, SEC-XB-04; `governance.md` GOV-XB-01, GOV-XB-04; `alm-devops.md` §14.1, §14.2, §14.4, §14.5; `licensing-cost.md` §6; `operations-support.md` §13.1, §1.1; `performance-scale.md` §4.2.

**Confidence:** MEDIUM-HIGH on the trigger boundaries and on this class's own documented costs — the corpus collected both. MEDIUM on the composition shapes, which are `INF` synthesis over documented compositions.

---

### ALT-010 — Do nothing; defer

**Class.** No solution is built. The current cost is accepted, or the decision is deliberately deferred until a named condition changes or a named unknown is closed.

**Why this is an option class and not an absence.** `licensing-cost.md` LC-28 requires it: *"aisa's mission requires it to be able to conclude 'not Power Platform' and also 'not now' or 'not automated'."* The corpus also notes the evidential position honestly — **no Microsoft source frames this option; the absence is the point** — and frames it by analogy from cloud cost-optimisation guidance (*"Regularly remove or optimize legacy, unneeded, and underutilized workload components"*; *"Align the cost of each flow with flow priority"*).

**Problem types it fits.** Low-frequency, low-value processes. Requirements whose decisive evidence is missing. Requirements whose forcing condition is expected to change (a system being decommissioned, a process being reorganised, a platform capability on a dated roadmap). Portfolio situations where the capability is real but not the best use of the next increment.

**Requirement triggers.**
- **The economics do not support it.** Full TCO *"frequently exceeds the value of a low-frequency process even when licences are free"* (`licensing-cost.md` LC-28) — the primary trigger.
- **A decision-blocking criterion is unknown** and cannot be closed inside the decision window. `decision-criteria.md` §5 enumerates these; the correct output is `DECISION BLOCKED — MORE EVIDENCE REQUIRED`, and *deferral with a named evidence task* is the action, not a guess.
- **A composed disqualifier is present** and cannot be broken (`architecture-patterns.md` §13; `anti-patterns.md` AP-D-059).
- **A required control's population is unfunded** — *"the option is economically infeasible rather than 'secure by configuration'"*, and the corpus forbids dropping the control to make the option look cheaper (`licensing-cost.md` LC-30).
- **The incumbent is on a dated decommissioning plan**, making any investment in the current shape a sunk cost.
- **A dependency is expected to change on a known date** — a deprecation, a wave, an early-access capability reaching general availability. Note the discipline: this is deferral against a *dated* fact, not against hope.

**Strengths.** Zero incremental cost, zero technical debt, zero operational and retirement obligation, zero deprecation exposure. Preserves optionality — the corpus's own exit/option-value dimension. It is also the only option that can be *correct* when the honest answer is that the evidence is insufficient, which is a state the corpus insists on being able to express rather than resolve by inference (manifest §5: *"do not silently infer it"*).

**Weaknesses.** The current cost continues, and it is frequently under-measured — the corpus's cost-of-doing-nothing framing requires it to be **priced**, not assumed to be zero. Deferral decays into drift without a **named revisit condition and owner**. It can also be used to avoid a decision rather than to make one, which is its characteristic failure mode. And it has no rollback: a deferral whose window closes leaves the organisation where it started, later.

**Architectural consequences.** None — which includes not accruing the irreversible modelling decisions this platform front-loads (table ownership type, virtual-versus-standard, one-way upgrades, business-application installation at environment creation).

**Security / governance consequences.** No new surface, no new policy scope, no new maker population. Any *existing* risk in the current way of working remains and should be recorded rather than deferred alongside the solution.

**Delivery / ALM consequences.** None. The residual obligation is to hold the deferral as a tracked decision with a revisit condition — otherwise it is not a decision, just an absence.

**Performance / scale consequences.** Not applicable, except that a deferral against expected growth should record the growth figure that would reopen it.

**Cost / TCO consequences.** The corpus requires **both** sides on the table: the do-nothing option priced (the cost of the current way of working) and the solution priced on the full ten dimensions. `licensing-cost.md` LC-28: *"For genuinely low-value processes… Price Power Platform with the full TCO lines, not the licence line."*

**Operations consequences.** No footprint. The existing manual process's operational risk is unchanged and should be stated.

**When preferable to any build.** When the value does not exceed the full TCO; when a decision-blocking unknown cannot be closed in the window; when a composed disqualifier stands; when a required control is unfunded; when a dated change is imminent that would alter the answer.

**When a build is preferable.** When the process is valuable, stable and its cost is genuinely tooling-driven; when volume, compliance or evidence obligations make the current way untenable; when the cost of doing nothing has been priced and exceeds the solution's TCO.

**Hybrid opportunities.** Deferral *plus* a cheap interim: process change now (ALT-002), a build later against a named trigger. Also: a bounded evidence task now — a measurement, a pilot, a licence census — with the decision reconvened against its result. This is the corpus's `V2 bounded pilot` used as a *decision* instrument rather than a validation one.

**Key decision criteria.** DC-D-008 (process value), DC-D-003 (time to value), DC-D-005 (process maturity), DC-D-092 (budget), DC-D-004 (lifespan), DC-D-115 (roadmap and preview dependency), plus every criterion in `decision-criteria.md` §5's decision-blocking set.

**Related anti-patterns.** `anti-patterns.md` AP-D-060 (the mis-costing that hides this option), AP-D-039 (over-engineering a workload that should not be built at all), AP-D-051 (guessing rather than deferring), AP-D-059.

**Evidence.** `licensing-cost.md` LC-28, LC-21, LC-29, LC-30, `licensing-cost.md` DC-15, §6, §7.1 item 1; `platform-suitability.md` PS-41, PS-44 (last rows), §9; `architecture-patterns.md` §13; manifest §5 (UNKNOWN handling), §7.

**Confidence:** MEDIUM. The economic trigger and the decision-blocking logic are well-founded in the corpus; the class is `INF` because no vendor source frames it, and the corpus says so.

---

### ALT-011 — Buy: a packaged product, SaaS service or marketplace application

**Class.** The capability is purchased rather than built: a first-party application from the vendor's own business-application suite, a marketplace or independent-software-vendor product, or a third-party SaaS service.

**Problem types it fits.** Standardised domains with mature products — service management, expense, procurement, contract management, field service, contact centre, industry-specific processes. Requirements that are recognisably somebody's product.

**Requirement triggers.**
- **The requirement is already covered by a first-party application, a marketplace product or a platform feature.** The corpus places this at **rung 0, before any app type** (`application-architecture.md` AA-36 rung 0, §2 first boundary), and the platform-suitability matrix routes it to `CUSTOM/OTHER (configure or buy)` (`platform-suitability.md` §2 row 26, PS-41, PS-44 last rows).
- **The specification is converging on an existing product's feature set** — a strong signal that the product is the answer (→ `anti-patterns.md` AP-D-007).
- **A capability that is unmanaged-solution-only in a custom build is available supported in a first-party product.** The corpus documents exactly this case: a custom multi-session application is unmanaged-solution-only and conflicts with the managed-production doctrine, so *"first-party app or governance exception"* (`application-architecture.md` AA-20, AP-35).
- The domain is standardised and non-differentiating, so a bespoke build buys no advantage (DC-D-002).

**Strengths.** The vendor owns the roadmap, the security posture, the operations and the compliance evidence. No build, no lifecycle, no retirement obligation on the organisation's side. Frequently the fastest time to value for a standardised domain. For a first-party product inside the same estate, it also inherits the estate's identity, governance and data-layer integration without a new integration.

**Weaknesses.** Fit is the product's, not the requirement's — configuration space is bounded, and exceeding it returns to customisation with all its cost (*"every extension carries performance, ALM, upgrade and support cost"*). Commercial dependency on a vendor's pricing and roadmap. **Extension of a first-party product is not free of this platform's constraints**: the corpus records that touching restricted business-application tables has its own licensing consequence, and that the current restricted-table list was itself an open unknown (`platform-suitability.md` U-5). Products also constrain the data question — where the product becomes the system of record for an entity, that is an architectural decision with downstream consequences (`anti-patterns.md` AP-D-014). And the corpus contains **no evaluation of any specific product**, so fit is a per-engagement assessment.

**Architectural consequences.** The product becomes a participant, and usually the system of record for its domain — which turns the remaining question into an integration question, answerable by ALT-007's logic and the ordered classification test.

**Security / governance consequences.** The product's controls apply, and must be assessed against the requirement rather than assumed adequate. Where the product is inside the same estate, the estate's identity and policy model largely applies; where it is external SaaS, it is a second enforcement plane with all of `anti-patterns.md` AP-D-026's ownership obligations.

**Delivery / ALM consequences.** Configuration and release follow the product's model. A marketplace or first-party product deployed as a managed solution participates in the estate's lifecycle; an external SaaS service does not. Note that the corpus flags **cross-tenant delivery** as needing the source-controlled rung, which matters for independent-software-vendor scenarios (`alm-devops.md` §4 row 16).

**Performance / scale consequences.** The product's envelope, unknown to this corpus. Where a first-party product sits on the same data platform, the platform's meters and its data-layer constraints still apply to anything built alongside it.

**Cost / TCO consequences.** Subscription plus configuration plus integration plus the internal support model. Frequently lower than a build for a standardised domain and higher for a narrow one. `licensing-cost.md` §6 requires it on the same ten dimensions, and notes that independent-software-vendor and multi-tenant resale licensing was an open deferral in the corpus (`platform-suitability.md` §7, target Area 10).

**Operations consequences.** Vendor-operated, with the organisation retaining first-line support, user administration, integration operations and the commercial relationship. Where the product is external, its availability joins the weakest-link analysis for every business flow that depends on it (`anti-patterns.md` AP-D-056).

**When preferable to Power Platform.** When a product already covers the domain to an adequate standard; when the domain is standardised and non-differentiating; when a required capability is supported in a product and only achievable by an exception in a custom build; when time to value is decisive and configuration reaches it.

**When Power Platform is preferable.** When no product fits without customisation that costs more than a build; when the process is genuinely organisation-specific or differentiating; when the requirement spans domains that no single product owns; when integrating the product would cost more than building the capability. Also when the product's own data-residency, identity or deployment posture fails a stated requirement.

**Hybrid opportunities.** Very common and often correct: buy the domain product, and build the organisation-specific surface, workflow or reporting around it on the low-code platform — with the product as the system of record and the platform consuming its contract (ALT-007's logic applied to a purchased system).

**Key decision criteria.** DC-D-002 (strategic differentiation), DC-D-003 (time to value), DC-D-021 (system of record), DC-D-092 (budget), DC-D-111 (existing platform estate), DC-D-059 (regulatory regime), DC-D-108 (deployment model), DC-D-105 (lock-in tolerance).

**Related anti-patterns.** `anti-patterns.md` AP-D-007 (the central one), AP-D-014, AP-D-026 (external SaaS with no operator), AP-D-056, AP-D-060.

**Evidence.** `platform-suitability.md` PS-41, PS-44 (last rows), §2 row 26, §7 (ISV deferral), U-5, §9; `application-architecture.md` AA-20, AA-36 rung 0, AP-35, §1 row 0, §2; `licensing-cost.md` §6, LC-28; `alm-devops.md` §4 row 16; `governance.md` GOV-XB-02; `integration-architecture.md` §2.2, §12.1.

**Confidence:** MEDIUM on the trigger logic; **`UNKNOWN` on any specific product's fit**, which the corpus cannot assess and which is a per-engagement task.

---

## 5. Cross-class analysis

### 5.1 The trigger-to-class map

One consolidated view: given a dominant requirement, which classes come into scope. Read as *candidate set*, not verdict — the composed test of `anti-patterns.md` AP-D-059 still applies.

**Read the third column as a candidate-generation citation, never as a comparison.** The `Evidence` cited is the evidence that the requirement **puts these classes on the table** — it is *not* evidence that any of them satisfies the requirement, and in all but one row the corpus holds no such evidence. `decision-criteria.md` §4A.1 makes this a governing default: **`COMPARATOR EVIDENCE ABSENT` applies to every row below except the customer-hosted/private-cloud/air-gapped row**, which is the corpus's only evidenced comparative axis (§4 ALT-008). A pack rendering this table must carry that marker into the output; §8 already warns that rendering §5.1 as a lookup table *"will produce confident wrong answers"*, and this is the specific way it goes wrong.

| Dominant requirement | Candidate classes | Evidence (that these classes come into scope) |
|---|---|---|
| Capability already exists in the estate | ALT-001, ALT-003, ALT-007, ALT-011 | PS-41, AA-36 rung 0, GOV-XB-02 |
| Value below full TCO | ALT-002, ALT-010 | LC-28 |
| Process immature or self-inflicted complexity | ALT-002 | LC-28, PS-41 |
| Document is the record | ALT-003 | DA §2 row 7, §6 |
| Relational + row/column security + audit, internal audience | ALT-004 | PS §2 row 2 |
| Human decision within 30 days | ALT-004 (keep this leg in-platform even if others move) | AT2-23, AT2-24, §4.1 |
| Bounded connector work over the existing estate | ALT-004 | AT2 §4.1 |
| Real computation in a step | ALT-006, ALT-009, ALT-005 | PF-45, AT2-32 |
| Guaranteed delivery / ordering / dead-lettering | ALT-006, ALT-009 | IA-15, IA-46 |
| Process outliving 30 days or resumable | ALT-006, ALT-009 | AT2-13, AT2-14 |
| Sustained throughput past the three-meter envelope, no partitioning | ALT-006, ALT-009 | IA §12.4 |
| Bulk movement / transformation / analytics | ALT-006, ALT-007, ALT-009 | PS-07, DA-51, IA §12.8 |
| High-ingest timestamped events | ALT-006 | SQ2-06, DAP-36 |
| B2B / trading-partner protocols | ALT-006, ALT-007 | IA §12.2 |
| Integration already owned with a published contract | ALT-007 | IA §12.1, GOV-XB-02 |
| Process class owned by an existing engine | ALT-007 | AT2-52 |
| Atomicity across ≥ 2 systems, no compensation window | ALT-005, ALT-006, ALT-007 (collapse to one owner) | IA-19, IA §12.3, APR §13 |
| Product-grade experience, native distribution with push | ALT-005 | AA-14, AA-36, AA-40 |
| Public third-party API | ALT-005 | PS-36, PS-51 |
| Contractual availability or recovery-time commitment | ALT-005, ALT-006, ALT-007 | PF-40, NB-03 |
| Customer-hosted / private-cloud / air-gapped deployment | ALT-005, ALT-008 | PS-47, V-D-01, V-D-04 — **the one row where comparator capability is documented on both sides**, with the second comparator's capability in Early Access, not GA |
| Portability of the application layer off the vendor | ALT-005 (ALT-008 candidate, `UNKNOWN`) | PS-51 |
| Behaviour must be frozen / per-release change control | ALT-005 | PS-50 |
| Confidential even from administrators | ALT-005, ALT-001, ALT-007 | SEC §4 row 6 |
| Private-network execution the platform cannot enter | ALT-006, ALT-009, ALT-007 | IA §12.5, I-10 |
| Standardised, non-differentiating domain | ALT-011, ALT-007 | PS-41, AA-36 rung 0 |
| Decision-blocking unknown unresolvable in the window | ALT-010 | manifest §5; DC §5 |
| Required control's population unfunded | ALT-010, or scope change | LC-30, SEC-XB-01 |
| **Conversational or agent-shaped interaction** | **none evaluable** — `UNKNOWN` in every class including ALT-004 | The corpus holds **no fit assessment of an agent surface in any class**. `platform-suitability.md` and `application-architecture.md` carry zero mentions; `automation-architecture.md` U-14 records the modality question as an **unowned deferral**. The criterion is `decision-criteria.md` DC-D-116 and its correct output is `DECISION BLOCKED`, not a candidate set (§6 item 9) |

### 5.2 The one comparative hypothesis the corpus retains, and its status

`licensing-cost.md` §6 keeps a single durable heuristic and is explicit that it is **a hypothesis to test, not a finding**:

> Power Platform has important people-/scope-based cost mechanisms, while infrastructure alternatives often expose more compute/transaction-based meters. The **users-to-work ratio** can therefore be a useful crossover criterion.

Block D carries this forward unchanged, with its status intact. Practically: *many people doing a little work each* tends toward the platform's economics; *few people driving a lot of machine work* tends toward consumption-metered alternatives. **This is a direction to test per engagement, not a rule**, and it must be tested on all ten cost dimensions (`licensing-cost.md` §6), because the platform's people-based mechanisms and the alternatives' machine-based mechanisms are not the only lines that matter — build effort, connectivity, observability, support and the second estate all sit alongside them.

### 5.3 What is symmetrically unknown

Recorded together, because a reader who forgets these will over-conclude in whichever direction they were already leaning:

| Unknown | Applies to |
|---|---|
| No empirical throughput, latency or concurrency **benchmark** for any technology (manifest NB-07; `automation-architecture.md` §8.7) | **All eleven classes.** Neither "the platform will be fast enough" nor "custom will be fast enough" is evidenced. |
| No comparative TCO study against named alternatives (`licensing-cost.md` LC-U-04, §7.3 item 51) | ALT-005, ALT-006, ALT-008, ALT-011 |
| No evaluation of any incumbent enterprise platform (`automation-architecture.md` §3.B row 19) | ALT-001, ALT-007, ALT-011 |
| No documented failure-rate or incident evidence for any service (`automation-architecture.md` §8.7) | All classes |
| Capacity envelopes for two of the three broker services never fetched (`automation-architecture.md` U-13; `integration-architecture.md` U-03) | ALT-006, ALT-009 |
| No capacity or latency figure for any boundary component (`architecture-patterns.md` APR-U-02) | ALT-007, ALT-009 |
| Comparator low-code platforms: everything except the deployment-model axis | ALT-008 |
| Gateway-at-scale infrastructure cost (`licensing-cost.md` LC-U-06) | ALT-006, ALT-009 |

---

## 6. Comparative evidence gaps

The brief asks for these explicitly. In order of decision impact:

1. **Comparator TCO — the largest gap.** No like-for-like pricing was fetched for custom development, cloud-native services, other low-code platforms or packaged products, and no independent comparative study was found. `licensing-cost.md` deliberately replaced verdicts with a **method** for exactly this reason. **Consequence:** Block D can say *which* cost dimensions favour which class directionally, and cannot state a crossover point. Any pack built on this must ask for the numbers, not supply them.
2. **Other low-code platforms — the widest gap.** One axis is evidenced (deployment model, §4 ALT-008, re-verified). Everything else is `UNKNOWN`, and Area 1 placed the topic out of scope. **Consequence:** ALT-008 can be *triggered* on one requirement class and cannot be *compared*. If the pack needs a real comparison, it is a separate research commission.
3. **Incumbent enterprise platforms.** The corpus evaluates none, and says so. **Consequence:** ALT-001, ALT-007 and ALT-011 are decision-logic classes whose *fit* is always a per-engagement assessment. The corpus's contribution is the questions, not the answers.
4. **Empirical performance for anything.** Symmetric, and it is the corpus's own headline reservation. **Consequence:** no class may be selected or rejected on a performance claim without measurement; limits remain exclusion evidence only.
5. **Broker and streaming capacity.** Two of the three services recommended for guaranteed-delivery and streaming requirements are recommended on positioning, not capacity. **Consequence:** ALT-006 can be triggered but not sized for those two; sizing is a validation task.
6. **The custom-connector throughput conflict.** Re-verified 2026-09-03 and **still open by 20×** (`anti-patterns.md` §6 V-D-02/V-D-03). **Consequence:** any option whose economics or sizing rests on a high-frequency custom connector is decision-blocked until measured — this cuts across ALT-004, ALT-006 and ALT-009.
7. **Far-side failure envelope for bidirectional synchronisation** (manifest NB-01). **Consequence:** ALT-009's bidirectional forms remain unavailable for critical data without a bounded failure/recovery test.
8. **Early-access status on the comparator deployment capability.** One of the two comparator platforms' self-hosted capability is in an early-access programme, not generally available (§4 ALT-008, `anti-patterns.md` §6 V-D-04). **Consequence:** it must not be presented as an available alternative today; the other platform's capability is documented as generally available.
9. **Conversational and agent capability — evaluable in no class** (added 2026-09-03). The corpus carries substantive agent evidence in governance, security, ALM, operations and licensing, and **no fit assessment anywhere**: `platform-suitability.md` and `application-architecture.md` mention the surface zero times, and `automation-architecture.md` U-14 records that the corpus *"is silent on agent-based automation as an alternative or successor pattern"* and *"cannot answer 'should this be an agent instead of a flow?'"*, with the deferral explicitly **unowned**. **Consequence:** `decision-criteria.md` DC-D-116 can elicit the requirement and encode its governance, security, ALM and operational obligations, and **no class — including ALT-004 — can be assessed for fit**. Unlike every other gap in this section, this one is not asymmetric; it is total, so the honest output is `DECISION BLOCKED`, not a candidate set. The commission is an **agent / Copilot Studio research area** covering fit boundaries, governance scope, security posture (including the graph-connector guest-access bypass), operational coverage and economics.
10. **Document generation and templating — absent from the entire corpus** (added 2026-09-03). Zero mentions across all twelve canonical files. Document output at volume is a recurring architecture-changing requirement in this domain. **Consequence:** no class can be triggered or excluded on it. Recorded as an **Areas 1–12 scoping gap**, not a Block D defect.

---

## 7. Evidence-quality notes

1. **Derivation with four external checks.** Ten of the eleven classes are derived entirely from Areas 1–12. ALT-008 additionally rests on `anti-patterns.md` §6 V-D-01 and V-D-04.
2. **Comparator evidence is vendor-side and fenced.** V-D-04's facts come from the comparators' own documentation, used under the corpus's `MS-V` discipline: capability facts yes, adjectives no. Early-access status is stated wherever cited.
3. **ALT-004 is written to the same standard as the others.** Its weaknesses field is the longest in the file. This is deliberate: a file that softened the target platform's entry would fail the symmetry rule it opens with.
4. **`INF` classes.** ALT-002, ALT-007 and ALT-010 are `INF`-framed — ALT-002 and ALT-010 because no vendor source frames them (which the corpus states), ALT-007 because manifest **NB-06** records its underlying pattern as supported synthesis, not vendor-endorsed. None is presented as vendor guidance.
5. **Confidence is uneven by design.** ALT-003 is HIGH (best-evidenced in both directions); ALT-008 is LOW except on one axis; ALT-001, ALT-007 and ALT-011 carry `UNKNOWN` comparator fit as an intrinsic property of the class rather than a defect of the research.
6. **No forbidden claim appears.** §2.2's five prohibited universals were checked against the finished text; none is asserted. The one retained comparative heuristic (§5.2) is labelled a hypothesis, as its source labels it.
7. **Single author, single session.** As with Areas 1–12. `Research Status: CANONICAL` after independent review; lineage in `canonical-manifest.md`.

---

## 8. Implications for the aisa knowledge model (pointers, not pack content)

- **Eleven classes, and the pack must be able to output all of them** — including the three that are not technology decisions (ALT-001, ALT-002, ALT-010). `licensing-cost.md` LC-28 makes carrying them a requirement, not a courtesy.
- **Options are candidate sets, not verdicts.** §5.1 produces candidates; the composed test (`anti-patterns.md` AP-D-059) and the decision-blocking set (`decision-criteria.md` §5) then reduce or block them. A pack that renders §5.1 as a lookup table will produce confident wrong answers.
- **A class can be the answer without Power Platform being excluded, and the pack must be able to say so** (added 2026-09-03; scoping corrected 2026-09-03 — Repair V3, `block-d-gate-repair-report.md`). `decision-criteria.md` §6.2 class 13 exists for exactly this: no exit fires, and a class other than ALT-004 is the documented answer for the requirement shape. **Two renders, never merged.** Where the shape is one of the four `data-architecture.md` §6 / `anti-patterns.md` AP-D-008 states positively, **ALT-003 is the documented answer and the lighter option on the seeded-entitlement fact alone (DC-D-093)** — no comparative TCO is asserted. Everywhere else, **ALT-001 or ALT-011 are candidates only**, carrying `COMPARATOR EVIDENCE ABSENT` — the corpus prices neither (§6 item 1; `licensing-cost.md` LC-U-04) and a pack must not call either "the lighter answer" on no evidence. *(V1/V2 defect, repaired here: this bullet and §6.2's render template both carried the comparative clause unconditionally, extending ALT-003's own documented sufficiency to two classes the corpus never evaluates — `block-d-gate.md` finding V2-M-01/G-M-01.)* The pack must render the non-exclusion explicitly and must carry the graduation trigger in both forms. Without this class an implementation of the closed outcome set has no terminal for the commonest departmental shape in this domain, and the only way to render it is to reach for ALT-004 — which is a structural bias toward the platform, arrived at by omission rather than by evidence.
- **Hybrid is a first-class option (ALT-009), gated on an operator.** Its gate (`anti-patterns.md` AP-D-026) must be enforced, or "hybrid" becomes the answer to everything difficult and nothing gets operated.
- **Every class carries obligations, not just capabilities.** The `*Consequences` fields are the material for trade-off statements; the corpus's characteristic failure is selecting a class on its strengths and inheriting its obligations unbudgeted.
- **The symmetry rule needs to survive into the pack.** §2.2's five forbidden universals are exactly the sentences a pack most easily reintroduces. They should be treated as prohibited output, not merely as absent findings.
- **Comparator gaps are engagement questions.** §6 items 1–3 mean the pack must be able to say *"this needs numbers we do not have"* — which is `DECISION BLOCKED`, and is a legitimate output.

Nothing in this section is pack content. Question banks, decision trees and pack files remain out of scope by instruction.

---

## 9. Summary

| | |
|---|---|
| Alternative classes | 11 |
| Classes that are not technology decisions | 3 (ALT-001 extend, ALT-002 process change, ALT-010 do nothing/defer) |
| Classes with HIGH confidence | 1 (ALT-003) |
| Classes with LOW confidence | 1 (ALT-008, MEDIUM-HIGH on its single evidenced axis) |
| Classes carrying `UNKNOWN` comparator fit intrinsically | 4 (ALT-001, ALT-007, ALT-008, ALT-011) |
| `INF`-framed classes | 3 (ALT-002, ALT-007, ALT-010) |
| Forbidden universal claims checked and absent | 5 (§2.2) |
| Retained comparative hypotheses | 1 (§5.2, users-to-work ratio — labelled a hypothesis) |
| Comparative evidence gaps reported | 10 (§6) |
| Criteria carrying an **evidenced** alternative-side signal | 28 (`decision-criteria.md` §4A.2) |
| Axes on which a **preference between candidate classes** is evidenced | **1** — deployment model (ALT-008, ALT-005) |
| Requirement classes evaluable in **no** class | 1 (conversational / agentic, §6 item 9) |
| External verification checks relied on | 2 (V-D-01, V-D-04, in `anti-patterns.md` §6) |

**The most consequential finding for a decision model** is that Power Platform can be **rejected on evidence** for a bounded, enumerable set of requirement classes — deployment model, cross-system atomicity, real compute, contractual availability, product-grade experience with native distribution, a public API, frozen behaviour, and administrator-excluded confidentiality — while for every *comparative* question (cost, speed, performance, productivity) the corpus's honest answer is that it holds no evidence in either direction. A decision model built on this must be strong on **disqualification** and modest on **preference**.

`Research Status: CANONICAL` — Block D review 2026-09-03 returned `PASS WITH CORRECTIONS`; the bounded repair of H-02, H-03 and H-04 as they touch this file is recorded in `block-d-repair-report.md`. The independent **re-review** 2026-09-03 returned `FAIL` (`block-d-re-review.md`) and this file carried the **V2 repair** as it touches ALT-003 — `decision-criteria.md` §6.2 class 13, its three non-negotiable properties, and the §8 pack implication — recorded in `block-d-repair-v2-report.md`. **Re-review V2** (`block-d-re-review-v2.md`) returned `FAIL`, and the **Block D gate** (`block-d-gate.md`) independently confirmed the finding. This file carries the **bounded V3 gate repair** of the §8 pack-implication bullet — scoping the "lighter option" claim to ALT-003 alone and marking ALT-001/ALT-011 `COMPARATOR EVIDENCE ABSENT` — recorded in `block-d-gate-repair-report.md`. **Gate recheck performed:** `block-d-final-gate-recheck.md` returned `FINAL BOUNDED GATE RECHECK: PASS` with `NEW GATE-BLOCKING FINDINGS: 0`. Canonicalized 2026-09-03; lineage in `canonical-manifest.md`.

---
