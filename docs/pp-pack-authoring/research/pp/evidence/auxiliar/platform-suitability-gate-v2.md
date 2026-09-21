# Platform Suitability — Gate V2

Inputs: `platform-suitability-research-v2.md` (v2), compared against `platform-suitability-review.md` (R-01…R-24) and `platform-suitability-gate.md` (FAIL, 2026-09-02).
Gate date: 2026-09-02. No existing file modified.
Test applied: "Could aisa use this evidence to make a defensible Power Platform suitability decision?" — where *defensible* means every fit verdict can be traced to a dated Microsoft statement, a documented limit, or an explicitly labelled inference/unknown, and no verdict rests on marketing language or a single interested source.

## Status

PASS

## What V2 Fixed

Checked item by item against the previous gate's failure reasons (criteria 3, 6, 8, 9) and the review's HIGH findings.

- **R-01 (biased Logic Apps comparison)** — fixed. PS-24 now rests on neutral Azure guidance (S-08, S-60) plus Power Platform ALM documentation (S-61–S-65, S-48b). The vendor-side table (S-09) is retained only for Azure-side capabilities and is explicitly flagged (PS-49). The boundary is restated on ownership, network runtime, dedicated compute and code-first tooling; "limited versioning / basic monitoring" is now an anti-pattern justification (AP-15), not a criterion.
- **R-02 (transactions)** — fixed with T1 evidence: change sets ≤ 1,000 operations and atomic (S-52); `ExecuteTransaction` rollback (S-53); synchronous plug-in stages inside the database transaction (S-54); flow changeset action restricted to Add/Update/Delete rows without loops (S-45b, S-55); `Patch` per-record errors and server-conflict error (S-56b); elastic tables "don't support multi-record transactions" (S-57); compensating-transaction pattern as Microsoft's cross-service remedy (S-58). Matrix row 28 and AP-13/AP-14 encode it.
- **R-03 (SaaS only)** — fixed: "requires connectivity to the internet" (S-68); data in Azure datacenters with macro-region replication (S-47a); US Government eligibility and parity exceptions (S-47b); 21Vianet (S-47c). Matrix rows 29–30.
- **R-04 (AZ overstatement)** — fixed: PS-37 carries the "limited number of customers … transitioning" caveat and a region-status unknown (U-12b); C-9 records the tension inside the same source.
- **R-09 (lock-in, cadence)** — fixed: mandatory semi-annual waves that "can't be postponed" (S-66); deprecation policy and 2025–26 list (S-67); Power Fx open-sourcing "in the process", `.pa.yaml` read-only, no cross-tenant pipelines, Dataverse export paths (PS-50, PS-51). Matrix rows 31–32, AP-16.
- **R-12 (testing)** — fixed: Test Engine deprecated April 2026; Playwright path (PS-53).
- **R-15 ("Dataverse-only")** — fixed with virtual-table limits (PS-56); wording softened in PS-02/PS-36.
- **R-18 (online concurrency)** — fixed (PS-46).
- **R-06 (marketing as evidence)** — fixed: "100 tables / 50 screens" and connector counts withdrawn as evidence.
- **R-20 / R-21 (inference labelling, adjective thresholds)** — fixed: every matrix row carries an origin tag (MS / INF / T3 / UNKNOWN) and a numeric threshold where one exists.
- **R-16 / C-8** — honestly left CONFLICTED; the admin page fetched does not state the add-on size.

## Remaining Critical Gaps

None. No remaining gap would cause aisa to issue a confidently wrong STRONG or POOR verdict on a requirement type that the matrix claims to cover, provided the verdict carries the row's origin tag and the listed unknowns.

## Remaining High Gaps

Gaps that materially reduce confidence but do not prevent a defensible decision, because each is surfaced as UNKNOWN or MEDIUM in v2 rather than hidden:

1. **Positive-fit evidence base is thin (R-07).** The Power Apps pattern catalogue is unreachable and apparently retired (PS-58, C-10); the automation-candidate list remains excerpt-level; the DPA/RPA source is dated 2020. STRONG verdicts therefore rest on the model-driven positioning statement (S-31) plus the absence of constraint violations. Defensible as "no documented constraint violated", not as "Microsoft endorses this pattern".
2. **Per-service SLA not read (R-05, PS-52, U-12).** Only "Dataverse 99.9%" is in T1 web documentation. Any availability requirement above that, or any question about connector/third-party exclusions, must be answered "unknown".
3. **Performance is limits-based only (R-24).** No latency or load evidence; concurrency ceiling undocumented (U-2). The matrix correctly forces "validate by test" but cannot rank options on performance.
4. **Cost model absent (R-10).** Licence boundaries are precise; cost magnitudes (Pages packs, environment overhead, local pricing) are not. Rows marked "CONDITIONAL on budget" cannot be quantified from this file.
5. **Identity coverage partial (R-11, PS-60).** Entra prerequisite documented; frontline/shared-device licensing and non-Entra populations remain UNKNOWN (U-14).
6. **Excerpt-level dependencies inside HIGH-confidence findings.** PS-45's flow-changeset restrictions (S-55) and PS-53's Playwright scope (S-71) come from search excerpts, not fetched pages.
7. **Independent evidence remains thin and partly interested** (R-08): three T3 sources, two with commercial bias, flagged but not offset.
8. **Deferred functional dimensions** (R-13, R-14, R-22): reporting, document generation, localisation, wrap/MDM, ISV. These would move verdicts STRONG→CONDITIONAL, not to POOR, and are assigned to Areas 02–15.

## Decision Boundaries

Strongest evidence-backed boundaries, stated as requirement × condition → constraint (origin in brackets):

- Any single queried table > 2,000 rows × non-delegable Power Fx (or SharePoint complex columns/ID relational filters) → silent partial results at runtime → canvas verdict depends on delegable source + formulas (MS, S-02/S-10).
- Two or more writes that must succeed or fail together × any write outside Dataverse standard tables (SharePoint, SQL connector, external API, elastic table) → no atomicity available; hand-built compensation required → POOR for low-code alone (MS, S-52/S-57/S-58).
- Same requirement × all writes on Dataverse standard tables → atomic via change set (≤ 1,000 ops) or synchronous plug-in (2-minute cap) → CONDITIONAL (MS, S-52/S-54/S-27).
- Cloud flow × any of: > 500 actions, nesting > 8, > 100,000 loop items, > 100 MB payload, > 10 GB/day content, pending step > 30 days → hard failure or time-out → POOR for that flow (MS, S-05).
- Caller expects synchronous response × latency > 120 s (flow) / 180 s (canvas) → time-out → async redesign or Azure orchestration (MS, S-05/S-01).
- Owner licence × requests/day: seeded M365 6,000; Premium 40,000; Process 250,000 stackable ×10 per flow → throttling above; consistently throttled flows turned off after 14 days (MS, S-04/S-05/S-48b).
- Integration identity × > 6,000 requests or > 52 concurrent per 5 minutes per web server → 429 with Retry-After (MS, S-03).
- Offline required × browser client, or × non-Dataverse data beyond 30–70 MB → not supported (MS, S-07/S-07b).
- Offline required × Dataverse × field-level security or N:N edits or personal views → feature not available offline (MS, S-07c).
- Any user population × premium connector, custom connector, on-premises data, model-driven app, Power Pages, or Managed Environment → standalone licence for every active user; multiplexing prohibited (MS, S-44).
- Deployment must be disconnected from the internet or on customer-controlled infrastructure → unsupported (MS, S-68/S-47a).
- Regulated US public-sector or data-in-China mandate → sovereign cloud with eligibility validation and feature-parity exceptions (MS, S-47b/S-47c).
- Solution requires frozen behaviour or change control per release → conflicts with mandatory semi-annual waves and rolling deprecations → regression cost and risk (MS, S-66/S-67).
- Solution must be re-hostable off Microsoft → UI, Power Fx and flows are not portable; data and .NET plug-ins are → rebuild on exit (MS + INF, S-40c/S-64/S-62).
- IT-owned automation × need for private-network runtime, dedicated compute, local debugging or B2B/EDI → Logic Apps Standard; × business ownership, M365/Dataverse context, human approvals → Power Automate; volume alone does not decide (MS, S-08/S-60/S-48b).
- Production-grade ALM/monitoring required → available (pipelines, Git integration, App Insights export) only with Dataverse and Managed Environments for target environments → premium licences (MS, S-62/S-63/S-65).
- Availability requirement > 99.9% or contractual cross-region RTO → no Microsoft commitment; integrations outside resilience scope (MS + UNKNOWN, S-12/S-37).
- Business-critical × automated testing obligation → code-first Playwright; Test Engine deprecated (MS, S-70/S-67).
- External system of record × model-driven UX × need for audit, row security, offline or Pages → virtual tables insufficient (MS, S-56).
- Public/anonymous audience → Power Pages capacity per unique user per month; Web API not for third-party integration (MS, S-06/S-51/S-44).
- Required connector blocked by tenant DLP → design-time block and runtime quarantine (MS, S-16).

## Confidence

MEDIUM

Rationale: constraint, licensing, transaction, deployment-model and lifecycle boundaries are HIGH-confidence and dated Tier 1. Confidence is capped at MEDIUM because the positive-fit half relies on inference from absent violations rather than on current Microsoft pattern guidance, the SLA document was not read, performance has no empirical evidence, and several findings still depend on search excerpts.

## Final Verdict

PASS, with conditions. V2 closes every HIGH finding from the review and the four criteria on which the first gate failed: poor-fit conditions now include transactions, deployment model and lifecycle risk; limitations cover atomicity, concurrency, connectivity and change cadence; decision criteria carry numeric thresholds and origin tags; the one interested source is quarantined and counter-evidenced. A suitability verdict produced from this file can be traced to dated Microsoft statements or to an explicitly labelled inference or unknown, which is the standard for "defensible".

Conditions attached to the pass:
1. aisa must surface the origin tag (MS / INF / T3 / UNKNOWN) and the relevant U-ids with every verdict; STRONG verdicts must be phrased as "no documented constraint violated", not as Microsoft endorsement.
2. Before pack authoring, read the September 2026 SLA document and the Licensing Guide add-on section (U-12, U-15), and confirm the flow-changeset restrictions from the fetched page (S-55).
3. The deferred dimensions (reporting, document generation, localisation, wrap/MDM, ISV, cost magnitudes, frontline identity, performance evidence, VNet parity) are owed by Areas 02–15 and must back-reference this file; if any of them is not delivered, the corresponding matrix rows revert to UNKNOWN.

The research may proceed to the next area under these conditions.
