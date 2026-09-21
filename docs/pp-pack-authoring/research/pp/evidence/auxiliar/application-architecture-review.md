# Application Architecture — Adversarial Quality Review

Review date: 2026-09-02.
Target: `application-architecture.md` (DRAFT, consolidated 2026-09-02).
Consistency baseline: `platform-suitability.md` (VALIDATED, gate PASS).
Reviewer stance: adversarial. The original file was NOT modified.

Method: the 18 review questions were checked against the target file line by line; consistency claims were verified by direct comparison with the platform-suitability text (quotes located in both files), not from memory.

---

## Finding 1 — Provenance overclaim: header says "All Tier 1 claims verified via fetch", but 16 sources are marked "search-verified"

### Problem
The header states: "All Tier 1 claims verified via fetch of Microsoft Learn pages; ms.date recorded per source." Sections 7 and 8 of the same file list 16 sources as "search-verified" (not fetched): A-15, B-09, B-13, B-14, C-13, C-14, C-19, C-21, E-12, E-13, E-14, E-15, E-17, E-18, E-21, E-22, E-26, E-27. Several of these carry decision-weight claims:
- E-18 (Pages PWA offline read-only) → the "offline write on a public site exceeds Power Platform" cell of AA-41c and the "Pages PWA beats Wrap" recommendation.
- E-12 (ReadNFC) → the NFC row of AA-42 and AA-46.
- E-27 (RTL on custom pages) → the RTL POOR verdict in AA-45.
- C-13 (B2C closed to new customers) → the CIAM default in AA-22 and conflict AA-C5.
- A-15 (Test Engine deprecation section) → AA-08.
- B-13 (multisession in custom apps) → AA-20.

### Why it matters
The header is the trust statement downstream consumers read first. A gate applying platform-suitability's standard (origin tags, dated Tier 1 fetches for HIGH confidence) would find the file self-contradictory. Any finding resting solely on a snippet is excerpt-level and by the corpus's own convention should be MEDIUM at most — yet AA-42 and AA-45 carry HIGH.

### Required improvement
Fetch the search-verified sources that support decision-weight findings (minimum: E-12, E-13, E-18, E-27, C-13, A-15, B-13) and record ms.date; or downgrade the affected findings' confidence and correct the header to state the split explicitly.

### Severity
HIGH

---

## Finding 2 — Finding-id scheme is broken: AA-12 is assigned twice; AA-41 suffixing collides across unrelated topics

### Problem
- `AA-12-CONF` (canvas scale conflict) and `AA-12` (model-driven fit) coexist. The fit matrix compounds it: row 1 cites "AA-01..AA-11" (excluding the canvas conflict finding AA-12-CONF from the canvas row), and row 2 cites "AA-12..AA-20", a range that lexically swallows AA-12-CONF, which is not a model-driven finding.
- `AA-41` (Intune/MAM) is immediately followed by `AA-41a/b/c` (offline) — the suffixes suggest sub-findings of the Intune finding, but they are a different topic in a different section.

### Why it matters
Platform-suitability's gate made stable ids a mandatory condition ("Ids PS-nn are stable across review and gates"). Downstream pack authoring will cite AA-nn; an ambiguous id space produces wrong cross-references silently.

### Required improvement
Renumber: give the conflict finding its own id outside the sequential range (e.g., move it to §5 as AA-C1 only, which already exists and duplicates it), and renumber offline findings as standalone ids. One finding = one id, no suffix overloading.

### Severity
HIGH

---

## Finding 3 — Methodological inconsistency with the validated corpus: reuses a vendor statement that platform-suitability explicitly excluded

### Problem
PS-06 states verbatim: "The vendor statement 'many successful implementations use more than 100 tables and over 50 screens' (S-26) is not used as evidence." The new file uses exactly that statement (same page, create-performant-apps-overview, now A-07) as evidence twice: in AA-01 ("Microsoft claims 'Many successful Power Apps implementations use more than 100 tables and over 50 screens…'") and as Side A of AA-12-CONF/AA-C1.

### Why it matters
Two files in the same corpus now apply opposite evidentiary standards to the same sentence. Source policy §7 (avoid marketing content) is the reason platform-suitability excluded it. Using it in AA-01's fit envelope inflates the canvas STRONG case with a claim the corpus already ruled inadmissible.

### Required improvement
Either (a) remove the statement from AA-01's evidence and keep it only inside the CONFLICTED record, explicitly labelled "vendor statement, inadmissible as capability evidence per PS-06"; or (b) formally revise PS-06's exclusion with justification. (a) is correct: the statement remains a marketing-adjacent claim with no supporting data.

### Severity
HIGH

---

## Finding 4 — Power Pages SPA "GA Jan 31 2026" rests on a release-plan page, not on shipped product documentation

### Problem
AA-23's pivotal claim — "React SPA support GA January 2026 moves the bespoke-UX ceiling" — cites C-06, a release plan (`release-plan/2025wave1/...`). Release plans are forward-looking and routinely slip; the file itself treats release plans as weaker elsewhere (E-16 used only as "actively invested" signal). The corroborating source C-14 (pac CLI `upload-code-site`) is search-verified only. No fetched product doc (e.g., a Power Pages "code sites" Learn article without preview banner) confirms GA shipped.

### Why it matters
This claim softens a PS-10 boundary and changes fit-matrix row 4 ("bespoke SPA UX" as CONDITIONAL instead of POOR). If SPA support is still preview or regionally gated, external bespoke-UX engagements would be scoped on a wrong premise. Same class of error as C-2 in platform-suitability (version drift between documents).

### Required improvement
Fetch the current Power Pages code-sites/SPA product documentation; record preview/GA banner state and ms.date; adjust AA-23 confidence and the fit matrix conditionally. Also resolve U-C1 (licensing effects) at least to "checked, not stated".

### Severity
HIGH

---

## Finding 5 — Teams as an application surface is absent

### Problem
The file mentions Teams only negatively (no offline in Teams; camera/barcode unsupported in Teams Mobile). It never treats "app inside Teams" as an application-architecture option, although platform-suitability's fit matrix row 3 (Dataverse for Teams: STRONG within bounds — no PCF, no model-driven, no offline, 2 GB/1M rows, PS-16) makes it a first-class approach that this area should have refined: when does a Teams-embedded canvas app satisfy the requirement at seeded-licence cost, and what UX/architecture limits apply (Teams tab embedding of standard canvas apps, deep links into Teams, Teams-specific player constraints)?

### Why it matters
Question 18: for a small internal team app, "Teams app on Dataverse for Teams" is often the cheapest correct answer; a decision model built only from this file would never propose it. It is also the natural counterfactual to "plain canvas + premium" in cost discussions.

### Required improvement
Add a fit-matrix row and at least one finding for Teams-hosted apps (Dataverse for Teams limits from PS-16 refined with app-architecture specifics: control set, component library availability, upgrade path to full Dataverse), plus the Teams-tab embedding option for standard canvas apps.

### Severity
MEDIUM

---

## Finding 6 — Embedded canvas surfaces (Power BI, SharePoint customized forms) not investigated

### Problem
Canvas apps embedded in Power BI reports and SharePoint list customized forms are documented application-architecture options with their own constraints (licensing, no offline, host-lifecycle coupling). The file mentions PowerBIIntegration only as a code-apps gap and SharePoint forms only as unsupported in components/code apps. No finding covers when embedding is the right architecture or its limits.

### Why it matters
"Form over a SharePoint list" is one of the most common real-world requirements; the customized-form pattern versus standalone canvas app is a genuine decision with licence and ALM consequences (customized forms don't appear in solutions the same way). Its absence leaves a hole exactly at the low-complexity end of the decision model.

### Required improvement
Add a short finding set: canvas in Power BI (when/limits), SharePoint customized forms (when/limits, ALM), and their poor-fit boundaries.

### Severity
MEDIUM

---

## Finding 7 — "Configure or buy" and Dynamics 365 first-party apps missing as application-level alternative

### Problem
PS-41 (configure/buy before build) and PS-44's redirect row ("Need already covered by first-party / ISV / M365 feature → CUSTOM/OTHER") are not cross-referenced anywhere in the new file. The app-type decision ladder (AA-36) starts at "plain canvas" — it has no rung zero: "an existing first-party app or ISV product already provides this application".

### Why it matters
The area's own fit matrix row 7 covers custom development but not the buy side. A pack derived from this file would compare build options against each other and never against "don't build an app at all".

### Required improvement
Add rung 0 to AA-36 (or a boundary in §2) cross-referencing PS-41/PS-44; note model-driven's specific proximity to Dynamics 365 first-party apps (same platform, licence interplay).

### Severity
MEDIUM

---

## Finding 8 — Model-driven in a phone browser is unsupported (PS-02 condition) — dropped from the device matrix

### Problem
Platform-suitability records: model-driven in a phone browser "isn't supported; use the Power Apps mobile app" (S-01). The new file's device findings (AA-42) and selection matrix (AA-46) omit this. AA-46's "BYOD + corporate data protection" row even offers "browser + CA session controls as fallback" without noting that the fallback fails for model-driven apps on phones.

### Why it matters
A browser-first mobile BYOD requirement plus a model-driven verdict is a real collision this area exists to catch. The prior corpus caught it; the refinement lost it.

### Required improvement
Add the constraint to AA-42/AA-46 with the PS-02/S-01 cross-reference; qualify the BYOD fallback row.

### Severity
MEDIUM

---

## Finding 9 — Authentication requirements are investigated deeply only for Power Pages

### Problem
The task listed "authentication requirements" across approaches. The file covers Pages identity thoroughly (AA-22) but for canvas/model-driven/code apps it relies implicitly on PS-60/PS-36 without integrating them: no statement in this file that internal app types require Entra work/school identity, that B2B guest access to canvas apps depends on cross-tenant-recognised licences (per-app plans are not recognised), or how code apps handle guests (D-15 mentioned "B2B guests" in the governance parity table but the file dropped it).

### Why it matters
Internal-vs-external is a primary fork of this area. The external branch is well built for Pages; the "external known partner via B2B into canvas/model-driven/code apps" branch is only reachable by leaving this file for platform-suitability, and the code-apps guest question is silently lost.

### Required improvement
Add an identity-per-app-type finding consolidating PS-60/PS-36 cross-refs plus the code-apps B2B statement from D-15, so this file answers internal/external standalone.

### Severity
MEDIUM

---

## Finding 10 — Application-level performance and concurrency evidence is thin and does not cross-reference the established unknowns

### Problem
Question 9 coverage is partial: form performance (AA-20), Studio/formula degradation (AA-04), N+1 storms (AA-07). Missing: (a) no cross-reference to PS-20/U-2 (no documented concurrent-user ceiling; sizing = load test) — the file is silent on concurrency; (b) the canvas performance-considerations guidance (PS §11 S-11, app-performance-considerations) is unused; (c) Pages list/grid performance marked UNKNOWN (U-C5) but model-driven grid/large-org behaviour got no equivalent probe; (d) no app-startup/load-time guidance thresholds.

### Why it matters
"How many concurrent users can this app type take" is among the first sponsor questions; the file neither answers it nor explicitly says "not documented — load test" the way platform-suitability does.

### Required improvement
Add a short performance finding: restate PS-20/U-2 for the app level, integrate S-11-class guidance (image/media, N+1, pagination), and mark model-driven large-grid behaviour as investigated-or-unknown explicitly.

### Severity
MEDIUM

---

## Finding 11 — Origin tags are not carried at finding level, breaking the gate convention

### Problem
Platform-suitability's gate condition 1 requires every fit verdict to carry an origin tag (MS/INF/T3/UNKNOWN). The new file's fit matrix has an Origin column (good) and §2 boundaries carry tags (good), but §3 findings do not systematically tag which parts are MS statements vs INF inferences. Examples where the distinction is material: AA-45's RTL verdict (INF from absence, buried in prose), AA-38's "GA" for Wrap (inferred from absence of preview banners, presented as a header fact), AA-41c's custom-sync verdict (INF, noted only in confidence line).

### Why it matters
The distinction between "Microsoft says POOR" and "analyst infers POOR from documented limits" is the corpus's core honesty mechanism. Where it is not machine-visible per finding, downstream automation will promote inferences to facts.

### Required improvement
Add an explicit origin line (MS/INF/T3/UNKNOWN) per finding, as platform-suitability's matrix does per row; re-label AA-38's GA claim as INF pending a Tier 1 GA statement.

### Severity
MEDIUM

---

## Finding 12 — AppOmni exposure RISK (AA-25) lacks any Microsoft-side source

### Problem
AA-25 rests on AppOmni (T3 primary) plus two T3 press articles. Microsoft's response ("configuration issue, added admin warning banners") is cited only "via S-107's account" — through the researcher's own framing of the AppOmni text. No MSRC statement, Microsoft blog, or the Learn security-best-practices page documenting the warning banners was fetched.

### Why it matters
This RISK drives hard acceptance conditions in §2 and AP-26. A T3-only foundation for a finding this consequential is below the corpus's cross-check standard ("Cross-check important findings"); the specific mitigations list (warning banners, column-security posture) may be stale or misattributed.

### Required improvement
Fetch the Power Pages security best-practices / site-security-check Learn documentation to anchor the mitigation side in Tier 1; keep AppOmni as the incident evidence.

### Severity
MEDIUM

---

## Finding 13 — Lifecycle and release-wave impact per app type not consolidated

### Problem
The task asked for "application lifecycle implications". ALM facts exist but are scattered (AA-06 canvas Git, AA-15/16 custom-page publish coupling, AA-29 Pages, AA-35 code apps), and the vendor-driven change dimension (PS-50: mandatory waves; new look mandatory April 2026 appears only via a T3 message-center archive, D-19; classic-UI retirement is U-B4 "not researched") is not treated as an app-type-differentiating criterion at all — even though model-driven apps absorb wave-driven UI changes (new look, theming resets) far more directly than code apps do.

### Why it matters
For long-lifetime solutions, "how much does Microsoft change my app's UI without my consent, per app type" is a genuine decision criterion the file gestures at but never states.

### Required improvement
Add one consolidated lifecycle finding: per-app-type exposure to release waves (model-driven highest UI exposure, canvas medium, code apps lowest UI/highest own-maintenance), with the new-look mandatory date sourced from Tier 1/2 rather than T3.

### Severity
MEDIUM

---

## Finding 14 — RTL-on-canvas "effectively infeasible" is an absence-based inference presented as a near-hard boundary

### Problem
§2 states "> 2–3 languages or RTL → model-driven (…) or Pages; RTL not documented for standalone canvas (MS+INF…)" and the Summary lists it under decision criteria. The support is one search-verified custom-page localisation article plus a T4 idea-forum signal. The file marks confidence MEDIUM honestly, but the boundary and summary lines drop the hedge.

### Why it matters
Boundaries and summaries are what get encoded downstream; an absence-of-documentation inference propagating as a POOR verdict without its hedge is exactly the failure mode gate V2 policed (STRONG/POOR phrasing rules).

### Required improvement
Fetch E-27 and search for any canvas RTL statement (including modern-controls docs); if still absent, phrase the boundary as "RTL support undocumented for standalone canvas → treat as unsupported until verified (INF)".

### Severity
MEDIUM

---

## Finding 15 — Licensing dimension has no explicit deferral table

### Problem
Per-app-type licence facts appear ad hoc (Pages prices in AA-26, PCF conditional premium in AA-34, code apps premium in AA-35, Wrap in AA-39, custom pages "follows the model-driven app"). There is no §-level statement of what this area deliberately defers to Area 10 (e.g., per-app plan interplay with custom pages, code apps SKU treatment in the Licensing Guide, Wrap + per-app), unlike platform-suitability §7's explicit deferral table.

### Why it matters
Without an explicit deferral, a gate cannot distinguish "not researched" from "deferred"; the code-apps licence claim in particular rests on the overview page, not on the September 2026 Licensing Guide the prior gate mandated reading (U-15 discipline).

### Required improvement
Add a deferred-gaps table mirroring platform-suitability §7, naming what Area 10 must confirm (code apps in Licensing Guide; custom-pages under per-app plans; Wrap licensing edge cases; SPA-on-Pages entitlements = U-C1).

### Severity
LOW

---

## Finding 16 — AP-29 (Visible-formula "security") is an anti-pattern built on an unlocated citation

### Problem
AP-29 and AA-10's security caveat rest on INF with U-A5 open ("no single T1 quote located"). The file handles this honestly, but an anti-pattern table is precisely where downstream consumers stop reading conditions.

### Why it matters
Anti-pattern tables get encoded as rules. An INF-based rule should be visibly tagged in the table (it is: "INF") — but the resolution path exists and was not attempted: the implicitly-shared-connections documentation (PS-31/S-43) already establishes that connection identity, not UI, governs data access for SQL; a similar Tier 1 anchor likely exists.

### Required improvement
Anchor AP-29 to PS-31/S-43 (implicit connection sharing) as partial Tier 1 support, or fetch a Learn security statement; then close U-A5.

### Severity
LOW

---

## Finding 17 — Duplicate content between AA-12-CONF and conflicts table AA-C1

### Problem
The canvas-scale conflict is recorded twice in full (finding AA-12-CONF and row AA-C1), with the same sources and assessment.

### Why it matters
Duplication invites divergence on future edits; platform-suitability keeps conflicts only in §6 with findings referencing them.

### Required improvement
Keep the §5 row; reduce the finding to a pointer (fold its decision impact into AA-03).

### Severity
LOW

---

## Question-by-question coverage check

| # | Question | Verdict |
|---|---|---|
| 1 | App types differentiated by requirements? | YES — differentiation is requirement-driven (navigation shape, personas, audience, offline, branding), not generic. Strongest aspect of the file. |
| 2 | Concrete decision criteria? | YES — §2 boundaries, AA-36 ladder, AA-41c/AA-46 matrices are concrete and mostly measurable. Weakness: a few criteria lack thresholds by nature (screen-count heuristic is T4-derived, honestly marked). |
| 3 | Strong/conditional/poor per approach? | YES — §1 matrix covers all approaches with origin tags. Gap: Teams surface missing (Finding 5); "buy/first-party" alternative missing (Finding 7). |
| 4 | Important limitations documented? | YES — custom-page limits, component/gallery exclusion, Wrap limits, cache, co-authoring removal, theming ceilings are all present with verbatim evidence. |
| 5 | Offline properly investigated? | YES — strongest section; re-verified on 2026 pages, per-surface decision table, FLS/flows/browser exclusions. Residual: Wrap-offline depth (U-E4) and code-apps offline (U-D3) open but declared. |
| 6 | Internal vs external properly investigated? | PARTIAL — Pages branch excellent (identity, licensing, exposure risk); B2B-into-apps branch not consolidated in this file (Finding 9). |
| 7 | Complex UX properly investigated? | YES — responsive costs, theming ceilings, PCF limits, code apps, SPA-on-Pages; the AA-36 ladder is decision-usable. Caveat: SPA GA evidence weakness (Finding 4). |
| 8 | Maintainability and complexity considered? | YES — formula sprawl, UDFs, testing instability, co-authoring, component-library update labour, partition costs. Above the prior corpus's depth. |
| 9 | Performance/scalability at app level? | PARTIAL — form/Studio/N+1 covered; concurrency and load benchmarks absent and not explicitly deferred (Finding 10). |
| 10 | Accessibility considered? | YES — per-app-type differentiation incl. canvas impossible-patterns and Pages formal conformance; honest ACR-scope unknown (U-E3). |
| 11 | Custom code / extensibility? | YES — PCF (with corrected licensing rule), form scripting, server logic, code apps, plug-in cross-refs. |
| 12 | Hybrid architectures? | YES — MD shell + custom pages, Pages + server logic/Azure, canvas + PCF, Wrap, PWA. |
| 13 | Traditional/custom alternatives? | YES — AA-30, AA-36 rung (e), AA-40; grounded mostly in T3 for Pages-vs-custom (declared, U-C2). |
| 14 | Anti-patterns? | YES — AP-17..AP-30, mostly MS-origin; AP-29 weak anchor (Finding 16). |
| 15 | Claims backed by authoritative evidence? | MOSTLY — verbatim Tier 1 quotes with dates dominate; exceptions are the search-verified cluster (Finding 1), SPA GA (Finding 4), AppOmni mitigation side (Finding 12), vendor statement reuse (Finding 3). |
| 16 | Version-sensitive claims identified? | YES — §8 churn list, AA-C3 half-life note, preview labels. Improvement: per-finding origin/volatility tagging (Finding 11). |
| 17 | Contradictions/uncertainty recorded? | YES — 9 CONFLICTED, 23 UNKNOWN, honestly maintained; header provenance contradiction is the exception (Finding 1). |
| 18 | Enough to answer the key question? | LARGELY — for the mainstream paths (internal canvas/MD, converged, Pages external, offline, branded mobile, custom-UX ladder) the evidence supports a defensible recommendation. Not yet for: Teams-surface option, embedded surfaces, buy-vs-build rung, B2B-into-apps, concurrency sizing. |

### Consistency with platform-suitability

Checked directly against the validated file:
- Consistent and correctly cross-referenced: PS-02 (except phone-browser drop, Finding 8), PS-06 (extended), PS-10 (softening explicitly declared), PS-11, PS-12, PS-13, PS-35 (re-verified, numbers unchanged), PS-36, PS-42, PS-50 (partially, Finding 13), PS-53, PS-56, U-4 (correctly kept open).
- Updates properly declared: PS-03 (code apps GA + pipelines; Git still absent — matches PS-03's stale-ALM framing), AA-C3 vs the PCF-premium belief.
- Breaches: S-26 vendor statement admissibility (Finding 3); PS-16 Teams row not refined (Finding 5); gate origin-tag convention not carried to finding level (Finding 11).
- No factual contradictions found between the two files' verbatim quotes.

---

## Coverage Assessment

**Strong areas**
- Offline (best-evidenced section; per-surface decision table; 2026 re-verification).
- Custom pages / convergence limits (verbatim, current, decision-shaped).
- Componentisation economics (pull-based updates, fork risk, gallery/form exclusion) — genuinely novel decision material.
- Wrap / Intune (R-14 resolved with binary-testable verdict).
- Accessibility and localisation differentiation per app type (R-13 localisation resolved).
- Anti-pattern set and conflicts/unknowns bookkeeping.

**Weak areas**
- Provenance discipline (header overclaim; search-verified cluster carrying HIGH-confidence findings).
- Identity/external-user branch outside Power Pages.
- Application-level performance/concurrency (no explicit "not documented — load test" statement).
- Lifecycle/release-wave exposure per app type.
- Id scheme and origin-tag machine-readability.

**Missing areas**
- Teams as an application surface (Dataverse for Teams refinement; Teams-tab embedding).
- Embedded canvas surfaces: Power BI, SharePoint customized forms.
- "Buy/first-party/ISV" rung 0 of the decision ladder (PS-41/PS-44 cross-reference).
- Explicit deferral table to Areas 03/06/09/10.

**Unsupported or under-supported claims**
- Pages SPA GA (release plan only) — AA-23.
- Wrap "GA" (absence of preview banners, INF as fact) — AA-38.
- RTL infeasibility on standalone canvas (absence-based, unhedged in §2/Summary) — AA-45.
- AppOmni mitigation side (no Microsoft source) — AA-25.
- Canvas "50+ screens" vendor statement readmitted against PS-06's exclusion — AA-01.
- Multisession in custom apps (search-verified, licence unknown) — AA-20.

**Critical gaps**
- None that invalidate the core differentiation. The gaps are additive (missing surfaces/rungs) and evidentiary (unfetched sources), not structural. However, the header provenance contradiction (Finding 1) must be fixed before any gate reads the file's confidence labels at face value.

## Research Verdict

**NEEDS MORE RESEARCH** — targeted, not a rework.

Minimum before gate (in order of leverage):
1. Fix the header provenance statement and fetch the decision-weight search-verified sources (Finding 1); re-grade affected confidences.
2. Repair the id scheme (Finding 2) and add per-finding origin tags (Finding 11).
3. Remove the readmitted vendor statement from AA-01 (Finding 3).
4. Verify Pages SPA GA from product docs (Finding 4).
5. Add the missing surfaces/rungs: Teams, embedded canvas, buy/first-party (Findings 5–7).
6. Restore the model-driven phone-browser constraint (Finding 8) and consolidate identity-per-app-type (Finding 9).

Scope estimate: one focused v2 pass (fetch ~10 pages, add ~5 findings, renumber), comparable to the platform-suitability v1→v2 cycle.
