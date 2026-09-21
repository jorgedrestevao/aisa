# Adversarial Quality Review — platform-suitability.md

Reviewed file: `platform-suitability.md` (2026-09-02, 44 findings PS-01…PS-44, matrix §2, anti-patterns §3, conflicts §4, unknowns §5).
Review date: 2026-09-02. Scope: quality of the existing research only. No new research performed; where a gap is named, the improvement describes what would need to be fetched.
Reviewer stance: assume Power Platform is being oversold until proven otherwise; look for what would make aisa recommend it wrongly, or reject it wrongly.

Finding ids: R-nn. Severity: CRITICAL / HIGH / MEDIUM / LOW.

---

## Finding R-01 — The Power Automate vs Logic Apps boundary rests on a source written by the Logic Apps product team to motivate migration

### Problem
PS-24, PS-32, PS-34, PS-37, PS-38 and matrix rows 20–22 all lean on S-09 ("Power Automate migration to Azure Logic Apps (Standard)"). That page exists to sell a migration; its comparison table ("Small to medium scale", "Limited versioning", "Basic monitoring", "Limited regional deployment options") is one product group characterising a sibling product. The file treats it as neutral Tier 1 and does not cross-check against the Power Automate team's own enterprise positioning (Process licence, Hosted Process, enterprise RPA, solution-aware flows, pipelines, Git integration).

### Why it matters
aisa could steer IT-owned or higher-volume automation to Azure when Power Automate with Process licences and solution ALM would have sufficed, inflating cost and skills demands. The "Limited versioning" claim in particular contradicts Power Platform's documented solution/pipeline/Git tooling (S-19 even names "Power Platform Git integration").

### Required improvement
Cross-check each S-09 cell against Power Automate documentation (ALM for flows, solution-aware flows, pipelines, Application Insights export, Process licence throughput) and against the Azure Architecture Center's neutral "choose an integration service" guidance. Re-tag PS-24 as TRADE-OFF with explicit "source authored by the alternative's product team" caveat.

### Severity
HIGH

---

## Finding R-02 — Transactional integrity is not analysed at all

### Problem
No finding addresses atomicity/consistency across multiple records or systems. Canvas `Patch`/`SubmitForm` calls, cloud-flow action sequences and connector writes have no multi-step transaction; Dataverse offers transactions only inside plug-ins/custom API/`ExecuteTransaction`. The research areas explicitly list "Transactional requirements" and "Transaction boundaries", and this is a classic reason to reject low-code for ledgers, stock movements or payment-like processes.

### Why it matters
aisa could rate a financial or inventory process "STRONG fit" (matrix row 1 "case app") without noticing that partial failure leaves inconsistent data and that compensation logic must be hand-built.

### Required improvement
Fetch Dataverse documentation on transactions (plug-in pipeline stages, `ExecuteTransactionRequest`, custom API), Power Automate guidance on error handling/compensation (scopes, run-after), and canvas `Patch` semantics. Add a finding + decision criterion "multi-record/multi-system atomicity required" with default fit CONDITIONAL (plug-in/custom API) or CUSTOM.

### Severity
HIGH

---

## Finding R-03 — "SaaS only" is never stated: on-premises, air-gapped or customer-hosted deployment is impossible and this is absent from the poor-fit list

### Problem
Power Platform cannot be deployed on-premises or in a customer-controlled datacentre; sovereign-cloud availability (GCC, China 21Vianet) is regional and feature-lagging. The file covers data residency by region (PS-17) but never records "must run disconnected / on customer infrastructure / OT network" as a hard POOR fit.

### Why it matters
For an energy company with OT/industrial segments, a requirement to operate inside an isolated plant network is realistic. aisa would have no evidence-backed rule to reject the platform outright.

### Required improvement
Add a finding citing the SaaS-only nature (S-20 "low-code software as a service" for Pages; environment/region docs), sovereign cloud availability pages, and the proxy/required-endpoints list (S-01) as the connectivity precondition. Decision criterion: "deployment must be on-premises/air-gapped" → POOR.

### Severity
HIGH

---

## Finding R-04 — The availability-zone RPO/RTO claim is generalised beyond what the source says

### Problem
PS-37 states in-region near-zero RPO and RTO < 5 min "automatically for production environments". The source (S-37) qualifies: "A limited number of customers in certain regions are transitioning to the improved architecture. Whether the region transitioned or is transitioning, the service always keeps a backup … in more than one data center." The AZ architecture is therefore not universal at the time of writing.

### Why it matters
A reliability target could be accepted on the basis of an architecture the tenant's region may not yet have.

### Required improvement
Reword PS-37 to "target architecture; rollout in progress; verify region status". Record as version-sensitive with date. Add to Unknowns: "Is the tenant's region on the AZ architecture?"

### Severity
HIGH

---

## Finding R-05 — 99.9% SLA is quoted for Dataverse only; SLAs for Power Apps, Power Automate and Power Pages were not verified

### Problem
PS-37 and matrix row 21 use "Dataverse 99.9%" as the platform SLA. The Microsoft Online Services SLA document (which defines service-specific SLAs, exclusions and credit terms) was not fetched. Power Automate and Power Pages may carry different terms and exclusions (for example, connector or third-party dependency exclusions).

### Why it matters
Availability requirements will be judged against a number that applies to one component of a multi-component solution.

### Required improvement
Fetch the current "Service Level Agreement for Microsoft Online Services" and extract per-service SLAs and exclusions. Record date.

### Severity
MEDIUM

---

## Finding R-06 — Marketing-grade statements are used as supporting evidence in several places

### Problem
Despite the file flagging one case (PS-20), several findings still lean on promotional wording:
- PS-06 / C-5 use "Many successful Power Apps implementations use more than 100 tables and over 50 screens while keeping excellent performance" (S-26) as counter-evidence to control-count heuristics. This is an unquantified anecdote, not data.
- PS-01 and PS-36 cite Power Pages as "secure, enterprise-grade, low-code SaaS" and the architecture page's "business-critical websites" without independent corroboration.
- PS-03 quotes code apps as accelerating "safe, rapid innovation".
- Connector counts ("1,400+", "1,500+", "~150 out-of-the-box", "200 data sources") appear across findings unreconciled; the numbers are marketing metrics with no bearing on fit.

### Why it matters
Per source-policy §7, these phrases are not evidence. Using them as counterweights (C-5) softens a real constraint (large-app degradation).

### Required improvement
Strip or downgrade these quotes to "vendor statement"; for C-5 rely only on the qualitative T1 constraint (S-25) and mark the numeric heuristics as unverified. Reconcile connector counts or drop them.

### Severity
MEDIUM

---

## Finding R-07 — Core "strong fit" evidence (application patterns, automation candidates) rests on search excerpts, not fetched pages

### Problem
PS-01 (pattern catalogue, S-33) and PS-21 (automation candidates, S-38) are the two findings that most directly define STRONG fit, and both are marked "content via search excerpt; direct fetch redirected". The file is honest about this, but the matrix (rows 1 and 5) still assigns STRONG without hedge.

### Why it matters
The positive half of the suitability model is the least-verified half. A pattern catalogue is also survivorship evidence (what worked), not boundary evidence (what did not).

### Required improvement
Re-read the pattern pages and the Power Automate planning pages in a browser or via corrected URLs; capture each pattern's stated characteristics and, importantly, any stated limitations per pattern. Downgrade matrix rows 1 and 5 to "STRONG (pending verification)" until done.

### Severity
MEDIUM

---

## Finding R-08 — Independent (T3) sources are few and two of them have commercial bias toward custom development

### Problem
Only three T3 sources are used (S-41 Bonnici, S-42 Arinco, S-48 Brilworks). S-48 is a custom-development vendor; S-42 is a Power Platform consultancy. PS-35's "complex sync → CUSTOM" and PS-26's "gateway adds latency" cite S-48 without noting the bias. No analyst, peer-reviewed, or large-sample failure evidence is present.

### Why it matters
Negative-fit conclusions are as biased as positive ones if their sources sell the alternative.

### Required improvement
Add bias notes to S-42/S-48 in the register. Seek at least two neutral independent sources (analyst reports, public post-mortems, Microsoft FastTrack/Success by Design lessons, community "failed project" retrospectives) for Area 13 and back-fill here.

### Severity
MEDIUM

---

## Finding R-09 — Vendor lock-in, exit strategy and roadmap/deprecation risk are absent as decision criteria

### Problem
Nothing in the file addresses reversibility: Power Fx is proprietary; canvas apps cannot be exported to another runtime; Dataverse data is exportable but schema/logic is not; Microsoft deprecates designers and SKUs regularly (the file itself records portals→Pages licensing transition and PAYG rule drift). S-30 mentions "awareness of deprecations and roadmaps" but this was not extracted as a RISK/criterion.

### Why it matters
A strategic advisory pack that cannot ask "what does it cost to leave?" will systematically under-price long-lived solutions on a fast-changing platform.

### Required improvement
Add findings on: export/portability options (solutions, Dataverse export, Synapse Link), Power Fx portability, historical deprecation cadence (release-plan/important-changes pages), and licence-model change frequency. Decision criterion: expected solution lifetime vs platform change cadence.

### Severity
HIGH

---

## Finding R-10 — Cost is documented as licence facts, not as a decision model; several cost inputs needed for the matrix are missing

### Problem
PS-15, PS-42 and PS-36 give list prices for some SKUs but: Power Pages pack prices are absent ("capacity cost" is called CONDITIONAL with no figures); the "minimum 200 anonymous users per environment" comes from a search snippet; environment overhead (1 GB per environment, S-13) is not extracted; no statement of how cost scales with audience (linear per user) versus custom development (fixed). Regional pricing is an Unknown.

### Why it matters
Matrix rows 7, 9, 13, 14 say "CONDITIONAL on budget" but the research gives aisa no way to estimate the budget.

### Required improvement
Extract full Licensing Guide price tables (Pages packs, Process, add-ons), the per-environment storage overhead, and the multiplexing/external-user rules into a cost-driver table. Even without local pricing, record the scaling shape (per user/month, per active user/app, per flow, per GB).

### Severity
MEDIUM

---

## Finding R-11 — Identity prerequisite is not stated: internal users need Microsoft Entra ID; non-Entra populations change the architecture

### Problem
The file assumes an Entra tenant. Requirements involving workers without Entra identities (contractors, frontline staff on shared devices, joint ventures) or non-Microsoft identity providers are only touched via Power Pages external identities.

### Why it matters
Identity landscape is a first-order fit criterion; without it aisa may classify an internal app as STRONG for users who cannot sign in.

### Required improvement
Fetch canvas/model-driven authentication prerequisites, frontline/shared-device licensing (F-SKUs, shared device mode), and Power Pages identity providers. Add a decision criterion "user population has Entra identities?".

### Severity
MEDIUM

---

## Finding R-12 — Testing and quality-engineering capability is not evaluated, although PS-04 makes "automated tests" a mission-critical requirement

### Problem
The mission-critical table quoted in PS-04 demands automated tests, but the research never checks what automated testing Power Platform supports (Test Studio, Test Engine, flow testing, solution checker) or its limitations.

### Why it matters
aisa cannot judge whether the mission-critical operating model is actually achievable on the platform.

### Required improvement
Fetch Test Engine/Test Studio documentation and Power Automate testing guidance; record scope and limits (Area 08/11 overlap, but needed here for the criticality criterion).

### Severity
MEDIUM

---

## Finding R-13 — Several common requirement types have no fit evidence: reporting/analytics, document generation and printing, localisation, notifications at scale

### Problem
Nothing on: reporting over Dataverse (view/aggregate limits, Power BI dependency), PDF/document generation (a very frequent approval-process requirement), multi-language support (built-in for model-driven, manual for canvas), or high-volume email/notification limits (Office 365 Outlook connector caps). Each is a recurring reason a "simple" app becomes a hybrid.

### Why it matters
Discovery will surface these needs; the pack will have no evidence to grade them.

### Required improvement
Targeted fetches: Dataverse aggregate/FetchXML limits and reporting options; Word/PDF generation options and limits; localisation for canvas vs model-driven; Outlook/SharePoint connector throttling limits. Add as CONDITIONAL criteria.

### Severity
MEDIUM

---

## Finding R-14 — Branded native mobile distribution ("wrap") and MDM/BYOD constraints were not researched

### Problem
PS-35 and PS-12 assume the Power Apps mobile player. The "wrap" capability (packaging canvas apps as branded native apps), app-store distribution limits, and device policy (60-day OS support window, S-01) are not assessed.

### Why it matters
A frontline requirement for a branded app on managed devices might be wrongly classed CUSTOM, or an unmanaged-BYOD requirement wrongly classed STRONG.

### Required improvement
Fetch wrap documentation (capabilities, limitations, licensing) and Intune/MAM support pages.

### Severity
LOW

---

## Finding R-15 — "Dataverse-only" for Power Pages and model-driven apps is stated more absolutely than the evidence supports

### Problem
PS-02, PS-10, PS-36 and matrix row 14 say Pages/model-driven are Dataverse-only. S-12 documents virtual tables ("map data in an external data source so that it appears to exist in Dataverse … real-time data operations against the external data source"), and model-driven apps can embed canvas/custom pages with connectors (S-20, S-32). The nuance (external data via virtual tables or embedded canvas) is not carried into the fit statements.

### Why it matters
A requirement with an external system of record could be rejected for Pages/model-driven when a virtual-table design would fit.

### Required improvement
Add virtual-table capabilities and limitations (providers, performance, unsupported features) as a CONDITIONAL path; soften "Dataverse-only" to "Dataverse-fronted".

### Severity
MEDIUM

---

## Finding R-16 — An unflagged contradiction between two Tier 1 pages on request capacity add-ons

### Problem
S-04 states "Each capacity add-on raises the request limit by another 50,000 per 24 hours"; S-12 states "Each capacity add-on provides an additional 10,000 requests every 24 hours". Both were fetched; the discrepancy is not in §4.

### Why it matters
Volume remediation cost (how many add-ons) would be mis-estimated by 5×.

### Required improvement
Add to §4 as C-8; resolve via the Licensing Guide add-on section and the capacity add-on admin page.

### Severity
LOW

---

## Finding R-17 — Algorithmic-complexity conclusions (PS-08, matrix row 16) are firmer than their single-blog evidence

### Problem
PS-08 is marked MEDIUM and sourced mainly to one blog (S-41), yet matrix row 16 states "HYBRID (plug-in/Functions) or CUSTOM" without hedging, and §3/§6 treat it as settled. The T1 corroboration offered (hidden-button `Select` workaround) shows imperative-logic friction, not an inability to implement algorithms.

### Why it matters
Legitimate canvas solutions with moderate calculation logic (the "Calculation" pattern is one of Microsoft's own) could be pushed to code prematurely.

### Required improvement
Fetch Power Fx reference for user-defined functions, `ForAll` semantics, named formulas, and any Microsoft statement on algorithmic limits; define observable thresholds (iteration until condition, mutable state across steps, recursion) rather than "algorithmic core".

### Severity
MEDIUM

---

## Finding R-18 — Concurrency and multi-user conflict handling (optimistic locking, last-writer-wins) is missing

### Problem
Apart from offline conflict resolution (PS-35), the file says nothing about concurrent edits online: Dataverse optimistic concurrency exists; canvas `Patch` on SharePoint/SQL is last-writer-wins; flows racing on the same record is a common defect.

### Why it matters
Collaborative or high-contention processes (shared queues, allocations) can be classed STRONG without the criterion "concurrent edits on the same record".

### Required improvement
Fetch Dataverse optimistic concurrency documentation and canvas data-source behaviour on conflicts; add as CONDITIONAL criterion.

### Severity
MEDIUM

---

## Finding R-19 — Several findings rely on pages that are two to five years old without stating that as a risk

### Problem
S-07 (offline canvas, 2024-03), S-25 (large apps, 2023-04), S-36 (accessibility, 2022-09), S-40b (fusion dev, 2021-04), S-07c (model-driven offline limits, 2024-09) carry `ms.date` values that predate significant product change (offline-first GA, new designers, code apps). The register shows dates but the affected findings (PS-06, PS-11, PS-35, PS-39) are all rated HIGH confidence.

### Why it matters
Age is a volatility signal per source-policy §6; HIGH confidence on stale pages can encode obsolete limits (for example, LoadData/SaveData memory figures or accessibility guidance).

### Required improvement
Downgrade to MEDIUM where the page is >18 months old, and add an "as of" clause in each such finding's Conditions.

### Severity
LOW

---

## Finding R-20 — Microsoft publishes no negative-fit guidance; the research should say so and treat its inferred boundaries as such

### Problem
Every POOR/CUSTOM conclusion is inferred from limits, comparisons or third parties. Microsoft's only explicit negative statement found is the flows/ETL sentence (S-22). The file does not state this methodological fact, so readers may assume Microsoft endorses the poor-fit list.

### Why it matters
Per research-prompt "Never present an opinion as a fact": inferred boundaries should be labelled as analyst inference.

### Required improvement
Add a methodological note at the top of §2 and §3: which rows are Microsoft-stated, which are inferred from limits, which are third-party. Tag each matrix row accordingly.

### Severity
MEDIUM

---

## Finding R-21 — Fit thresholds are qualitative where measurable inputs exist

### Problem
Matrix row 1 says "moderate volumes"; row 8 "org-wide audience"; row 25 "very large single-app scope"; PS-36 "small set of known partner users". The research already holds numbers that could anchor these (500/2,000 delegation rows, 6,000/40,000/250,000 requests per day, 100,000 loop items, 30-day runs, 3M offline rows, 2 GB Teams). They are not tied to the qualitative words.

### Why it matters
aisa's decision model needs measurable criteria (research-areas §15); vague adjectives push judgement back to the engagement.

### Required improvement
Rewrite matrix rows with explicit thresholds derived from the cited limits, and mark where no number exists (concurrency, Pages traffic) as UNKNOWN rather than adjective.

### Severity
MEDIUM

---

## Finding R-22 — ISV / resale and multi-tenant product scenarios are unaddressed

### Problem
Building a product to sell to other organisations (each needing licences), or a multi-tenant SaaS on Power Platform, has specific licensing (ISV Connect) and architectural limits. Not covered; matrix has no row.

### Why it matters
Less relevant to internal enterprise engagements, but if a partner/JV scenario appears aisa has nothing.

### Required improvement
Short fetch of ISV/AppSource licensing guidance; add a POOR/CONDITIONAL row.

### Severity
LOW

---

## Finding R-23 — Classification discipline: several findings carry two tags and some "FACT" entries are absence-of-evidence or vendor statements

### Problem
PS-20 is "FACT (absence) / UNKNOWN"; PS-01 mixes FACT and PATTERN; PS-31 "FACT / RISK". Source-policy asks for one classification per finding. Also, DECISION CRITERION findings rarely state the measurable attribute and threshold.

### Why it matters
Downstream authoring will need to map classifications to pack structures (signals vs criteria vs risks); mixed tags create ambiguity.

### Required improvement
Split dual-tagged findings into separate entries, or pick the dominant tag and move the secondary into "Decision impact". For each DECISION CRITERION, add an "attribute / threshold / measurement" line.

### Severity
LOW

---

## Finding R-24 — Performance evidence is limits-based; no latency or load-behaviour evidence exists

### Problem
"Performance" in the file means "documented limits". There is no evidence on typical response times, cold-start behaviour, gateway latency figures, or how canvas apps behave at N concurrent users on a given source. PS-20 admits no ceiling exists but the matrix still implies performance can be judged.

### Why it matters
A performance-sensitive requirement (sub-second interactions, field workers on poor networks) cannot be graded.

### Required improvement
Gather Microsoft performance guidance with numbers (execution phases doc, network capacity/throughput verification page cited in S-24, gateway sizing) and at least one independent load-test write-up. Otherwise state explicitly that performance fit must be validated by test.

### Severity
MEDIUM

---

## Coverage Assessment

**Strong areas**
- Hard limits: delegation, flow limits, service protection, request entitlements, storage entitlements — well sourced (T1, dated), decision-relevant, cross-referenced.
- Offline (browser vs mobile, Dataverse vs LoadData/SaveData, model-driven gaps).
- Licensing boundary (seeded vs premium, multiplexing, external users, Managed Environments coupling).
- Microsoft-authored redirects to Azure (plug-ins, dataflows, Service Bus, Functions, "no-cliffs"), and the Power Automate anti-pattern set.
- Conflict register (7 items) and explicit unknowns — good epistemic hygiene.

**Weak areas**
- Positive-fit evidence (patterns, automation candidates) built on search excerpts.
- Power Automate vs Logic Apps comparison sourced to the Logic Apps team; PP ALM capabilities under-represented.
- Reliability claims (AZ rollout, SLA scope) overstated relative to source wording.
- Independent evidence thin and partly commercially biased.
- Performance treated as limits only; no latency/load evidence.
- Fit thresholds expressed as adjectives despite available numbers.

**Missing areas**
- Transactional integrity and compensation.
- SaaS-only / on-premises impossibility / sovereign clouds.
- Lock-in, portability, deprecation cadence.
- Identity prerequisites (Entra, frontline, shared devices).
- Testing capability for mission-critical model.
- Reporting, document generation, localisation, notification limits.
- Concurrency/optimistic locking online.
- Branded mobile distribution (wrap), MDM.
- ISV/multi-tenant products.
- Cost model shape (Pages pack prices, environment overhead).

**Unsupported or over-supported claims**
- "RTO < 5 min automatically" for all production environments (rollout-dependent).
- Platform SLA 99.9% (Dataverse-only evidence).
- "Limited versioning / basic monitoring" for Power Automate (single biased source).
- "Dataverse-only" for Pages/model-driven (ignores virtual tables/embedded canvas).
- Algorithmic core → HYBRID/CUSTOM (one blog).
- Control-count heuristics vs anecdotal "100 tables/50 screens" (both weak).
- Capacity add-on size (10k vs 50k, unflagged contradiction).

**Critical gaps**
- None rated CRITICAL: no finding was found that would cause a confidently wrong recommendation on its own. Four HIGH items (R-01, R-02, R-03, R-04, R-09) together mean the research cannot yet safely reject or accept the platform for transactional, on-premises, long-lived or IT-owned-integration requirements.

## Research Verdict

**NEEDS MORE RESEARCH**

Rationale: the constraint and licensing backbone is solid enough to seed decision criteria, but the positive-fit evidence is under-verified, one key alternative comparison is single-sourced and biased, and five decision dimensions that routinely decide real engagements (transactions, deployment model, lock-in, identity, testing) have no evidence. Address the HIGH findings (R-01…R-04, R-09) and re-verify the excerpt-based findings (R-07) before synthesis; the MEDIUM items can be folded into Areas 02–15 where they overlap, provided the suitability file back-references them.
