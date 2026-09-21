# Application Architecture — Research Gate

Gate date: 2026-09-02.
Target: `application-architecture-research-v2.md` (54 findings, 22 decision boundaries, 19 anti-patterns AP-17..AP-35, 11 CONFLICTED, 29 UNKNOWN, 54/54 findings origin-tagged).
Inputs: `application-architecture-review.md` (17 findings: 4 HIGH, 9 MEDIUM, 4 LOW), `platform-suitability.md` (VALIDATED) for consistency.
Mechanical checks performed on the v2 file: every referenced AA-id is defined; every V- source cited appears in the register; no stale v1 ids outside the mapping table; every finding carries an Origin line.

Disclosure: research, review and gate were produced in the same working session by the same author. Independent reading before pack authoring is recommended; the gate conditions below are written so that an independent reader can re-check the load-bearing claims in under an hour.

## Status

PASS

## Strong Decision Boundaries

Evidence-backed with fetched, dated Tier 1 sources (origin MS unless noted). Each is stated as requirement → constraint → architectural implication.

1. **Data-dense, record-centric work with relational navigation, row/column security and audit** → model-driven requires a Dataverse data model; relational navigation is automatic there and hand-built in canvas (B-01) → model-driven STRONG; canvas POOR for the same requirement (AA-12, AA-17).
2. **Bespoke screens inside a structured backbone** → custom pages GA; "use custom pages instead of embedded canvas apps"; ≤ 25 pages, ≤ 10 connectors, no offline/device controls, state loss, double-publish (B-02, B-03) → model-driven shell + custom pages is the sanctioned alternative to a large standalone canvas app, bounded by those limits (AA-15, AA-16, AA-03).
3. **Offline** → only native mobile players; Dataverse-only offline-first (3M rows; no flows, virtual/elastic tables, non-Dataverse connectors; foreground-only sync); model-driven offline drops field-level security, personal views, search; Pages PWA is read-only; SPA sites have no PWA (E-05, E-06, V-03/V-04, V-09) → decision table AA-44; browser/Teams/custom-page/Pages-write offline exceed the platform.
4. **Device hardware** → NFC only in iOS/Android native apps; barcode/camera not in desktop browser or Teams Mobile; model-driven "in a phone browser isn't supported" (V-01, V-02, V-19) → native player mandatory; browser-first mobile BYOD × model-driven is a collision (AA-45).
5. **External audience** → anonymous or non-Entra identities only via Power Pages over Dataverse-fronted data with per-unique-user capacity licensing; B2B guests reach canvas, model-driven, code apps and Wrap subject to cross-tenant licence recognition (per-app plans fail) (C-00, C-02, V-18, PS-36) → audience identity tier selects the app-type set (AA-52, AA-21..26).
6. **Branded mobile app** → Wrap is canvas-only; no push, no B2C, no sovereign cloud, no CMK/Lockbox; licence per end user; monthly rewrap (E-01..E-03) → binary verdict AA-40; {branded app + push} is unsatisfiable on-platform (AA-46).
7. **Concurrent development / team size** → canvas co-authoring removed; Git commits only on publish; one maker per app or custom page (A-05, A-06, B-02) → team > 1–2 makers per artefact forces partition, model-driven or code apps (AA-06).
8. **UI reuse inside galleries and forms** → canvas components cannot be inserted there; component-library updates are pull-based per consuming app; customization forks permanently (D-01..D-03) → PCF is the only in-gallery reuse path; estate rebrand touches every canvas app (AA-31..AA-33).
9. **Custom code / extensibility ladder** → PCF has no Dataverse WebAPI in canvas, no custom auth, premium only for non-connector external calls (D-04, D-05); code apps GA with Premium per user, public asset endpoint, no Git integration, B2B supported (V-18, D-22) → requirement-driven ladder buy → canvas → components → PCF → code apps → custom (AA-34..AA-36).
10. **Accessibility mandate** → Pages platform-attested WCAG 2.2 / Section 508 / EN 301 549; model-driven built-in; canvas has documented impossible patterns (modals, key handling) needing PCF (E-07, E-20) → legal mandate steers to model-driven or Pages, canvas only with discipline + PCF budget (AA-47).
11. **Localisation** → model-driven language packs; Pages Liquid 43 languages; Pages SPA single-language; canvas manual dictionary (E-23, E-25, E-26, V-09) → > 2–3 languages favour model-driven or Pages Liquid; SPA-on-Pages excluded (AA-48).
12. **Freshness of externally visible data** → Pages server cache 15-minute SLA; plugin/flow writes "never guaranteed to be immediate" (C-08) → background-automation-fed real-time displays are POOR on Pages (AA-27).
13. **Team-scoped app on seeded licences** → Dataverse for Teams caps at 2 GB / ~1M rows, no PCF/model-driven/offline/API/plug-ins; one-way upgrade converts all users to premium (V-11, V-12) → Teams-hosted STRONG within bounds, with an explicit exit cost (AA-50).
14. **Report-driven write-back / single-list form** → Power BI visual passes ≤ 1,000 rows, embed-for-organization only, no Report Server; SharePoint customized forms cannot be shared manually or copied between environments automatically (V-13..V-15) → embedded surfaces have their own fit rows (AA-51).
15. **Requirement already covered by a first-party app** → configure or buy before build (PS-41, PS-44); multisession in custom apps is unmanaged-solution-only with a Copilot Service dependency (V-08) → rung 0 precedes every app-type choice (AA-36, AA-20).

## Conditional Decision Boundaries

Conditions that change the recommendation are explicit and evidence-backed; where Microsoft publishes no threshold the file says so.

- **Canvas scale and maintainability**: partitioning is the documented remedy (A-03); no Microsoft numeric cap on screens/controls exists (U-A1); the T3/T4 30–40-screen heuristic and the vendor "50+ screens" statement are both recorded as inadmissible thresholds (AA-C1). Condition = maker team size, persona count, change velocity, not a number. Acceptable per gate criteria.
- **Responsive multi-device on canvas**: opt-in rebuild per screen with publish-to-test loop (A-01, A-02) → effort condition, not a fit veto (AA-02).
- **Multi-persona in one canvas app**: formula-level branching, client-side only; data access governed by connection identity (A-04, PS-31) → ≥ 2 divergent experiences → app-per-persona or model-driven (AA-10, AA-17).
- **Bespoke external UX**: SPA-on-Pages documented (V-09, no preview wording) but single-language, no Git, no PWA, no OOB forms/lists → CONDITIONAL on accepting those trade-offs and a pro-dev team; strict GA banner state UNKNOWN (U-C6) (AA-23).
- **Anonymous Pages audience**: RISK conditions are concrete — column security on PII, no Global read for Anonymous/Authenticated roles, Web API field allow-lists, open registration off, PPAC daily checks at "Advanced" (C-07, V-10, C-03) (AA-25).
- **Long-lived apps**: UDF/named-formula/StartScreen stack (A-04), Git-on-publish, Playwright after Test Engine deprecation (V-07) → maintainability conditional on discipline and browser-level testing (AA-05, AA-08).
- **Multisession contact-centre requirement**: custom model-driven app only in an unmanaged solution (V-08) vs PS-05 managed-only production doctrine → governance exception or first-party app (AA-20).
- **Brand depth**: model-driven theming = colours/font/logo, unthemed areas remain (B-05); modern canvas controls brand-tinted, not pixel-faithful; PCF/code apps beyond (AA-14, AA-11, AA-36).
- **Long lifetime × vendor UI change tolerance**: wave exposure ranking model-driven > canvas > code apps is INF over MS facts (PS-50, B-05, V-08) (AA-54).
- **Concurrency**: no documented ceiling for any app type; differentiation is by data path, not app type; load test required (PS-20, C-17) (AA-53).

## Poor-Fit Conditions

Each approach has credible, evidence-backed situations where it must not be the default:

- **Canvas**: many divergent experiences in one artefact; Dataverse-centric relational process apps; external/anonymous audiences; native-client embedding (PS-12); RTL requirement with no Microsoft statement (treat as unsupported until prototyped, U-E6).
- **Model-driven**: brand-first/consumer UX; mobile-first field capture with device hardware via custom pages (B-03); phone-browser access (V-19); external data needing audit/security/offline (virtual tables, PS-56); anonymous audiences.
- **Model-driven + custom pages**: offline or device-capability UX; Outlook embedding; state-heavy back/forward flows; > 10 connectors (B-03).
- **Power Pages**: system of record permanently outside Dataverse; offline data capture; third-party API surface (PS-36); server/caching control; background-automation real-time freshness (C-08); multi-language on SPA sites (V-09).
- **Code apps**: IP-allowlist estates (public asset endpoint); Windows player audiences; offline (undocumented); anonymous users (V-18).
- **Teams-hosted**: any PS-16 exclusion (PCF, model-driven, offline, API); growth toward 2 GB without upgrade budget (V-12).
- **Wrap**: consumer/B2C; push; sovereign cloud; CMK/Lockbox; > 150 MB (E-02, E-03).
- **Embedded surfaces**: Power BI embed-for-customers or Report Server; SharePoint form needing portability/solution ALM (V-13..V-15).

## Alternatives

Represented at three levels:
- **Rung 0 — configure/buy/first-party** (PS-41, PS-44; worked example: multisession → Customer Service) — fit row 0.
- **Hybrid** — Pages server logic → Azure Functions with sandbox/timeout/outbound-block constraints (C-20); plug-ins/Functions behind any UI (PS-09); model-driven shell + custom pages; canvas + PCF; Wrap; Pages PWA — fit rows 3, 8, 9.
- **Custom web / native development** — preferable when data is permanently outside Dataverse, throughput/SLA must be guaranteed, consumer UX exceeds SPA-on-Pages constraints, a public API is required, branded app + push, custom sync/conflict rules, or per-user licensing is uneconomic at scale (AA-30, AA-36 rung 5, AA-40, AA-44). Pages-vs-custom rests on T3 triangulation because Microsoft publishes no decision guidance (U-C2) — declared, MEDIUM.

## Critical Risks

No CRITICAL gap that prevents a defensible architecture decision. Risks that a decision model must carry as explicit conditions:

1. **Anonymous Power Pages misconfiguration** (AA-25, AP-26): documented mass-exposure class; acceptance conditions listed; must be encoded as mandatory checks, not advice.
2. **Preview/GA ambiguity of 2026 features** (U-C6): SPA sites and code apps show no preview wording in fetched bodies but client-rendered banners could be missed. Fit rows 4 and 5 are already CONDITIONAL; a browser check is a gate condition (below).
3. **Multisession unmanaged-only** (AA-20): a contact-centre requirement on a custom app silently breaks managed-solution production doctrine (PS-05).
4. **Dataverse for Teams upgrade cliff** (AA-50, AP-32): one step converts a seeded-licence estate to premium for all users.
5. **Wave-driven UI change** (AA-54): model-driven's mandatory new look and theming reset are facts; the exposure ranking is inference.
6. **Same-author gate**: research, review and gate share an author; the review was adversarial and its HIGH findings were verifiably closed (vendor statement removed, ids repaired, sources fetched, SPA re-based), but independent spot-checking of V-05, V-08, V-09, V-18, V-19 is recommended.

## Remaining Unknowns

Non-blocking; each has a resolution path in v2 §6:
- U-4 Pages throughput/RPS ceilings (confirmed unpublished 2026-09).
- U-A1 canvas numeric size caps (none published; heuristics inadmissible).
- U-B1 exact licence clause for multisession in custom apps; U-B4 Tier 1 date for mandatory new look.
- U-C1 licensing effects of SPA sites; U-C6 strict GA banner state (SPA, code apps); U-C7 Web API wildcard verbatim on Learn.
- U-D2/U-D3 code apps in mobile players / offline.
- U-E1 push-notification throttles; U-E2 kiosk/shared-device mode; U-E3 per-app-type accessibility conformance reports; U-E5 Wrap GA date; U-E6 RTL on standalone canvas.
- U-T1 component-library reuse in Teams-hosted apps; U-S1 SharePoint customized-form licensing.

## Evidence Gaps

- **Pages vs custom web**: no Tier 1 decision guidance; boundary rests on T3 (C-10..C-12) — MEDIUM, declared.
- **Maintainability ceiling**: Microsoft documents symptoms (256K-character formulas, Studio degradation) and remedies (partition), not thresholds — accepted per gate criteria; the pack must not encode 30–40 screens as a rule.
- **Lifecycle exposure ranking** (AA-54) and **custom-sync offline verdict** (AA-44 INF row): inferences over documented facts, tagged INF.
- **Aged pages still load-bearing**: A-03 (2023), E-20 (2021), V-02 (2022 upd. 2025), V-05 (2022, pre-release banner), V-16 (2020 upd. 2024) — findings on them carry MEDIUM currency where noted.
- **Search-verified residue**: B-09, B-14, C-14, C-19, C-21, E-14, E-15, E-17, E-21, E-22, E-26 — none carries a finding above MEDIUM alone (verified in v2 §8).
- **Licensing cells** ("CONDITIONAL on budget" for rows 3, 4, 5, 7, 8) unquantified pending Area 10 (v2 §7 deferral table).
- **Microsoft mitigation wording for Pages Web API wildcards** not yet fetched (U-C7); AP-26 rests on AppOmni + PPAC controls + a search-verified table-permission snippet.

## Confidence

MEDIUM

Rationale: HIGH on the load-bearing constraints (offline, devices, custom pages, components, Wrap, identity tiers, Teams caps, embedded surfaces — all fetched Tier 1 with dates and origin tags). Capped at MEDIUM overall because (a) the Pages-vs-custom boundary is T3-only, (b) strict GA state of SPA sites and code apps is unverified against client-rendered banners, (c) the maintainability ceiling has no Microsoft threshold and rests on team/persona conditions, (d) licence-dependent cells await Area 10, and (e) the same author produced research, review and gate.

## Final Verdict

**PASS.** The v2 research can support a future decision model: every approach (canvas, model-driven, converged, Power Pages Liquid/SPA, code apps, Teams-hosted, embedded surfaces, Wrap, hybrid with Azure, custom development, configure/buy) has requirement-driven STRONG / CONDITIONAL / POOR verdicts with origin tags; 22 boundaries are phrased as requirement → constraint → implication and anchored to fetched Tier 1 sources; poor-fit and alternatives are represented at all levels; uncertainty is explicit in 11 CONFLICTED and 29 UNKNOWN entries with resolution paths; the four HIGH review findings were closed with verifiable changes. No CRITICAL gap remains.

Gate conditions carried into downstream use (mandatory):
1. Every verdict derived from v2 §1/§2 keeps its origin tag (MS / INF / T3 / UNKNOWN); INF-based POOR verdicts (RTL on canvas, custom offline sync, lifecycle ranking) are phrased "treat as unsupported until verified", never as Microsoft statements.
2. Before pack authoring: confirm in a browser the preview/GA banner state of V-09 (Pages SPA) and V-18 (code apps); fetch the Pages Web API / table-permission page for the wildcard wording (U-C7); read the September 2026 Licensing Guide for code apps, custom pages under per-app plans, Wrap and SPA entitlements (v2 §7).
3. The pack must not encode any numeric canvas size threshold (U-A1, AA-C1); it may encode the partition remedy and the team/persona conditions.
4. Fit rows 4 (Pages SPA) and 5 (code apps) stay CONDITIONAL until condition 2 is met.
5. Dimensions deferred in v2 §7 (Areas 03, 04, 06, 09, 10) back-reference this file; undelivered deferrals revert the corresponding cells to UNKNOWN, as in platform-suitability §7.
6. Re-verify short-half-life facts (modern controls, code apps, SPA sites, server logic, Entra External ID, new look) before encoding; treat AA-C3 (PCF licensing) and AA-C10 (code apps B2B) as facts that have already changed once.
