Research Status: DRAFT (consolidated, ungated)
Research Confidence: MEDIUM-HIGH
Gate: PENDING

# Application Architecture — Canonical Research Evidence

Research area: **02 — Application Architecture** (`../research-areas.md`).
Research date: **2026-09-02**. Consolidated from 5 parallel research passes (canvas, model-driven + custom pages, Power Pages, componentisation + code apps, device/offline/accessibility/localisation). All Tier 1 claims verified via fetch of Microsoft Learn pages; ms.date recorded per source.
Source policy: `../source-policy.md`. Cross-references `platform-suitability.md` findings as **PS-nn** and unknowns as **U-nn**.

**Purpose.** Answer: *"What application requirements drive the choice and architecture of Power Platform application components (Canvas, Model-driven, Custom pages, Power Pages, PCF/components, Code apps, Wrap) — and when is another technology or a hybrid preferable?"* Not a product summary; positive capabilities appear only where they define a fit boundary.

**Gap resolution carried from platform-suitability §7:**
- **R-14 (Wrap, Intune/MAM)** — RESOLVED (AA-38..AA-41). Fit-matrix row 12 of platform-suitability no longer reverts to UNKNOWN for branded-app requirements.
- **R-13 (localisation)** — RESOLVED for the localisation dimension (AA-45). Reporting/PDF/notification-throttle dimensions remain with Areas 03/04 (push-notification throttles stay UNKNOWN, AA-43).
- **PS-03 (code apps)** — UPDATED: GA February 2026; solutions + pipelines ALM now supported; Git integration still absent (AA-35).
- **PS-11 (accessibility)** — re-verified and extended (AA-44). **PS-35 (offline)** — re-verified on fresher pages and extended (AA-41a/b/c). **PS-53 (testing)** — corroborated for canvas (AA-08).

**How to read confidence.** HIGH = dated Tier 1 statement fetched this pass. MEDIUM = Tier 1 excerpt/aged, or Tier 3 with partial Tier 1 corroboration. Origin tags per gate V2 convention: **MS** (Microsoft statement) / **INF** (inference from documented limits) / **T3** (independent) / **UNKNOWN**.

**Volatility.** Modern controls, code apps, Power Pages SPA and server logic are 2025–2026 features still churning; licensing and preview flags re-verify before encoding.

---

## 1. App-type fit matrix

Verdict classes per `platform-suitability.md §1` (STRONG phrased as "no documented constraint violated").

| #   | Approach                                          | STRONG fit                                                                                                                                                                                                    | CONDITIONAL fit                                                                                                                                                                                                               | POOR fit                                                                                                                                                                                  | Origin   | Findings             |
| --- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------- |
| 1   | **Canvas app**                                    | Task-focused internal app; 1–2 personas; moderate screen count; mixed or non-Dataverse sources via connectors; specific form factor; device hardware (camera/scan/GPS/NFC)                                    | Responsive multi-device (opt-in effort); multi-persona role UI; queried tables > 2,000 rows (PS-13); long-lived + high change rate (UDF/Git/test discipline required); team > 1–2 makers (partition); brand-critical UX (PCF) | Many divergent experiences in one artefact; Dataverse-centric relational process apps (forms/views/BPF needed); external/anonymous audiences; native-client embedding (PS-12)             | MS + INF | AA-01..AA-11         |
| 2   | **Model-driven app**                              | Data-dense, record-centric, process-driven work over Dataverse; automatic relational navigation; row/column security + audit; native record deep links; accessibility mandates; multi-language                | Bespoke screens via custom pages (limits AA-16); branding = colours/font/logo only; offline (documented gaps); multisession (licence unverified)                                                                              | Brand-first/consumer UX; mobile-first field capture needing device hardware in custom pages; external data with audit/security/offline needs (virtual tables, PS-56); anonymous audiences | MS       | AA-12..AA-20         |
| 3   | **Model-driven shell + custom pages** (converged) | Structured backbone + a few bespoke screens; replaces "one giant canvas app"                                                                                                                                  | ≤ 25 pages/app; ≤ 10 connectors across pages; state loss on back-navigation; double-publish trap                                                                                                                              | Offline or device-capability field UX (unsupported in pages); Outlook embedding; state-heavy flows                                                                                        | MS       | AA-15, AA-16, AA-03  |
| 4   | **Power Pages**                                   | Authenticated external users over Dataverse; portal-shaped interactions (forms, lists, self-service, document exchange); WCAG/EN 301 549 mandates; multi-language                                             | Anonymous/consumer audiences (capacity licensing + misconfiguration RISK); bespoke SPA UX (GA Jan 2026, maturity); traffic spikes (no published ceilings, U-4); near-real-time freshness (server cache)                       | System of record not in (and not moving to) Dataverse; offline data capture; third-party API surface (PS-36); server/caching control required                                             | MS + T3  | AA-21..AA-30         |
| 5   | **Code apps**                                     | Bespoke SPA (React/Vue…) over connectors/Dataverse with platform governance; pro-dev team; internal/B2B audience; premium budget                                                                              | Solutions + pipelines ALM (no Git integration); Conditional Access instead of IP restriction                                                                                                                                  | IP-allowlist/network-isolated estates (public asset endpoint); Windows player; offline (undocumented → treat unsupported); anonymous users                                                | MS       | AA-35                |
| 6   | **Wrap (branded native mobile)**                  | —                                                                                                                                                                                                             | Internal or B2B-guest audience, canvas apps, branding = icon/splash/colours, Intune/store distribution, monthly rewrap ops owned                                                                                              | Consumer/B2C; push notifications; sovereign clouds; CMK/Lockbox mandates; > 150 MB AAB                                                                                                    | MS       | AA-38..AA-40         |
| 7   | **Custom web / native development**               | Preferable when: data outside Dataverse permanently; guaranteed throughput/SLA; product-grade consumer UX; public API; branded app + push; custom sync/conflict rules; per-user licensing uneconomic at scale | —                                                                                                                                                                                                                             | —                                                                                                                                                                                         | MS + T3  | AA-30, AA-40, AA-41c |

---

## 2. Decision boundaries (requirement × condition → architecture)

- Responsive multi-device UX × canvas → opt-in rebuild with containers per screen; "Scale to fit" default wastes screen (MS, AA-02).
- Projected screens > ~25–30 or ≥ 2–3 divergent persona experiences × canvas → partition (multiple apps + `Launch()` with state loss) or model-driven shell + custom pages; retrofit is manual screen-by-screen (MS, AA-03, AA-12-CONF).
- Team > 1–2 makers per canvas artefact → co-authoring removed; one editor per app/custom page; parallelism only via architecture (MS, AA-06).
- Many shareable/bookmarkable record destinations → model-driven native record URLs; canvas deep links are hand-built Param()+StartScreen plumbing per destination, and mobile deep links break May 2026 without environment ID (MS, AA-09, AA-18).
- Offline requirement → decision table AA-41c; browser offline, Teams/custom-page offline, Pages offline-write, offline+field-level-security, offline+flows all UNSUPPORTED (MS).
- Branded mobile app × push notifications → unsatisfiable in Power Platform (Wrap has no push; push only via Microsoft's players) → custom native or drop one requirement (MS, AA-40, AA-43).
- Anonymous/public audience × sensitive Dataverse data → Pages RISK: Global-read + Anonymous role + Web API `*` columns exposes tables; open registration ON by default (T3+MS, AA-25, AA-26).
- Legal accessibility mandate (WCAG 2.2 / EN 301 549 / Section 508) → Power Pages platform-attested; model-driven built-in; canvas maker-dependent with documented impossible patterns (modals, custom key handling) needing PCF (MS, AA-44).
- \> 2–3 languages or RTL → model-driven (language packs) or Pages (43 languages); canvas = hand-built dictionary × screens × languages; RTL not documented for standalone canvas (MS+INF, AA-45).
- Brand-critical UX ladder: modern Fluent controls (brand-tinted) → canvas components/library → PCF (pixel control; premium only if non-connector external calls) → code apps (premium/user) → custom web (MS, AA-36).
- Reusable UI inside galleries/forms → canvas components can't be inserted there; PCF only (MS, AA-31).
- Back-office automation writes that users must see immediately × Power Pages → server cache (15-min SLA, no guarantee for plugin/flow writes) breaks freshness → design workaround or POOR (MS, AA-27).
- Data-dense relational navigation + audit + granular security → model-driven STRONG; same requirement on canvas = hand-built everything (MS, AA-12).
- Non-Dataverse data + model-driven/Pages UX → virtual tables drop audit/security/offline/Pages (PS-56) → replicate into Dataverse or CUSTOM.
- Component-library estate: updates are pull-based (edit + republish every consuming app); "allow customization" forks permanently → no npm-style propagation; a rebrand touches every canvas app (MS, AA-32, AA-33).

---

## 3. Findings

Ids AA-nn are stable for downstream use. Sub-registers: A- (canvas), B- (model-driven), C- (Power Pages), D- (components/code apps), E- (mobile/offline/a11y/l10n) in §7.

### 3.1 Canvas apps

#### AA-01 — Canvas fit envelope: task-focused UX layer over any connector; ceiling is maintainability and persona count, not runtime
- **Classification:** DECISION CRITERION
- **Evidence:** Partition doc positions task-scoped apps as the healthy unit (A-03); comparison table gives canvas "Full control" of UI vs model-driven "Limited, predominantly customization" (B-01); Microsoft claims "Many successful Power Apps implementations use more than 100 tables and over 50 screens while keeping excellent performance" (A-07) — see AA-12-CONF for the maintainability counter-signal.
- **Why it matters:** Canvas is the default low-code UX layer; its POOR verdicts come from audience (external), embedding (PS-12), data volume (PS-13) and organisational factors (team size, personas), not from a hard screen cap.
- **Decision impact:** Fit matrix row 1.
- **Conditions:** U-A1: no Microsoft numeric cap on screens/controls exists; only symptoms are documented.
- **Confidence:** HIGH (facts) / analyst synthesis on envelope.
- **Sources:** A-03, A-07, B-01.

#### AA-02 — Responsiveness is opt-in effort, not default; tooling has documented gaps
- **Classification:** CONSTRAINT + TRADE-OFF
- **Evidence:** "your entire layout scales to fit the screen… can't take advantage of the additional pixels"; "You activate responsiveness by turning off the app's Scale to fit setting, which is on by default"; "you adjust some settings and write expressions throughout your app" (A-02). Gaps: "The authoring canvas doesn't respond to the sizing formulas created. To test responsive behavior, save and publish your app" ; dragging a control "overwrite[s] those expressions or formulas"; Data table/Charts/Add picture "not supported in the layout containers"; Center/End container options "can cause child controls inaccessible" (A-01, A-02).
- **Why it matters:** "Works on phone and desktop" is a per-screen build workload with a slow publish-to-test loop and drag-destroys-formulas fragility.
- **Decision impact:** Multi-form-factor requirement raises canvas effort materially; single-form-factor apps avoid it. Effort driver for estimates.
- **Confidence:** HIGH.
- **Sources:** A-01 (2022-01-27), A-02 (2026-01-13).

#### AA-03 — Partitioning is the documented remedy for large canvas apps; both partition patterns carry costs
- **Classification:** PATTERN + CONSTRAINT (extends PS-06)
- **Evidence:** "large apps can be split into smaller sections"; `Launch()` between apps but "State in the original app is lost when another app is launched" (A-03). Custom-pages route: "Don't exceed 25 custom pages in a model-driven app"; a custom page "is expected to typically be a single screen with loose coupling"; standalone canvas apps "aren't supported for use as a custom page" — migration is manual copy/paste with navigation rewiring (A-13/B-02).
- **Why it matters:** Hub-and-spoke converts in-app navigation into cross-app launches with state-persistence code; the converged route is a re-architecture, not a lift-and-shift.
- **Decision impact:** Plan partition seams up front when scope is projected large; retrofitting is expensive either way.
- **Confidence:** HIGH.
- **Sources:** A-03 (2023-04), A-13/B-02 (2026-03-13).

#### AA-04 — Formula sprawl (> 256K chars) is the documented root cause of Studio degradation; copy-paste silently duplicates it
- **Classification:** ANTI-PATTERN + FACT (extends PS-06)
- **Evidence:** "nearly all apps with a long load time … have at least one formula of more than 256,000 characters. Some apps with the longest load times have formulas of more than 1 million characters"; "copying and pasting a control with a long formula duplicates the formula … without it being realized" (A-03).
- **Decision impact:** Long-lived apps need formula-length review (feasible on `.pa.yaml` source, PS-48) and named-formula refactoring as build standard.
- **Confidence:** HIGH.
- **Sources:** A-03.

#### AA-05 — Sanctioned initialization/maintainability stack: named formulas + StartScreen + user-defined functions; OnStart is deprecated architecture
- **Classification:** RECOMMENDATION + FACT
- **Evidence:** Studio load "drop by as much as 80%" moving OnStart logic to named formulas (A-03). "Using the OnStart property can cause performance problems"; `Navigate` in OnStart "is retired"; OnStart "might be disabled by default" (A-04). UDFs documented without preview flag: typed parameters/returns, behavioural bodies, user-defined types; "Recursion isn't yet supported"; named formulas cannot have side effects (A-04).
- **Why it matters:** The historical "no subroutines, logic duplicated everywhere" critique is narrowed (not closed — no unit-test framework for UDFs, AA-08). Legacy OnStart-heavy apps carry refactoring debt.
- **Decision impact:** UDF-first + App.Formulas + StartScreen as build standard for multi-year apps; heavy OnStart in an existing estate = backlog item.
- **Conditions:** U-A2: formal GA status of UDFs not explicitly announced (page carries no preview marker).
- **Confidence:** HIGH behaviour / MEDIUM GA status.
- **Sources:** A-03, A-04 (2026-06-11), A-18 (T2 blog).

#### AA-06 — Concurrent development: real-time co-authoring was removed; Git integration commits only on publish; one maker per app/page
- **Classification:** CONSTRAINT + RISK
- **Evidence:** "Git version control for editing apps has been removed and is no longer supported" (A-06, 2025-05-14). Replacement Git integration: "You can commit your canvas apps when you publish them. Changes aren't available to commit until you publish"; "You can't edit the .pa.yaml files directly in your repository if your app contains code components" (A-05). Custom pages: "one maker can edit one custom page at a time" (B-02).
- **Why it matters:** Team-of-N development on one canvas artefact is unsupported in 2026; parallelism comes from architecture (apps/pages/components), not tooling. Stale 2022–2024 articles claim live co-authoring — see CONFLICTED AA-C2.
- **Decision impact:** Maker team size > 1–2 per app is itself a partition/model-driven/code-apps signal.
- **Confidence:** HIGH.
- **Sources:** A-05 (2025-10-08), A-06, B-02.

#### AA-07 — The platform's own limits induce its documented anti-patterns; Live Monitor is the audit tool and its worked example shows UI-formula N+1 storms
- **Classification:** ANTI-PATTERN + FACT
- **Evidence:** "Common anti-patterns include loading too much data, turning everything into collections, and overloading OnStart. People often use these patterns to work around real or perceived Power Apps limitations" (A-07, 2026-08-20). Monitor example: a label's `CountRows` over 12 entities re-evaluated per record write → HTTP 429; "For each single request to add a record, you're potentially making 12 additional requests"; "Debug published app" setting itself "has a detrimental impact on the performance of your app for all your users" (A-11).
- **Why it matters:** Reactive formulas make an innocent label a hidden per-keystroke query engine; delegation truncation (PS-13) pushes unskilled makers to collect-everything workarounds. Maker skill is an architecture risk factor.
- **Decision impact:** Monitor-based data-call audit in definition-of-done for canvas apps on shared backends; governance review hunts the three named anti-patterns.
- **Confidence:** HIGH.
- **Sources:** A-07, A-11 (2024-11-14), A-16 (T2 standards PDF).

#### AA-08 — Canvas testing story unstable: Test Engine deprecated April 2026; migration path is code-first Playwright
- **Classification:** RISK (corroborates PS-53)
- **Evidence:** "Effective April 2026, Test Engine is deprecated"; repo removed 2026-11-01; rationale "near-zero usage"; migration "Use Power Platform Playwright samples" (A-15). T3: no meaningful unit tests for Power Fx formulas (A-19).
- **Why it matters:** The refactoring safety net for multi-year canvas maintainability has had two abandoned tool generations; regression cover is browser-level and code-first only.
- **Decision impact:** Long life + high change velocity → budget Playwright investment or accept manual regression; genuine argument for code apps/custom where change velocity is high.
- **Confidence:** HIGH deprecation / MEDIUM outlook.
- **Sources:** A-15, A-19 (T3).

#### AA-09 — Navigation: no route model; deep linking hand-built per destination; mobile deep-link contract changes May 2026
- **Classification:** PATTERN + CONSTRAINT
- **Evidence:** Deep link = `?param=` read with `Param()`, routed in `StartScreen`, hydrated in `OnVisible` — per destination (A-10). "Starting May 1, 2026, all deep links for Power Apps mobile must include the environment ID as a required parameter. Existing deep links without these parameters will stop working" (A-14).
- **Why it matters:** N deep-linkable destinations = N × hand-written plumbing; cross-app navigation post-partition adds state code. Model-driven has native, security-trimmed record URLs (AA-18).
- **Decision impact:** Heavy-linking requirements (record links in email/notifications) favour model-driven.
- **Confidence:** HIGH.
- **Sources:** A-10 (2022-07-27), A-04, A-14 (2026-01-09).

#### AA-10 — Role-based UI in one canvas app is formula-level branching, client-side only
- **Classification:** PATTERN + RISK
- **Evidence:** Tier 1 documents entry-branching (`If(LookUp(Attendees, User = User().Email).Staff, StaffPortal, HomeScreen)`) (A-04); per-control gating is `Visible`-formula practice (T3/T4). Client-side hiding is not a security boundary — enforcement must live in the data source's security model (INF from connector security model; no single T1 quote located, U-A5).
- **Why it matters:** Two personas = conditional formulas smeared across the app → feeds AA-04 sprawl. Model-driven does persona segmentation natively (roles → forms/views/app access, AA-19).
- **Decision impact:** ≥ 2 divergent experiences → app-per-persona or model-driven.
- **Confidence:** HIGH mechanism / MEDIUM security caveat citation.
- **Sources:** A-04, A-19 signals.

#### AA-11 — Modern (Fluent 2) controls are the current generation; classic not deprecated; modern set still churning (property renames Feb 2026)
- **Classification:** FACT + RISK
- **Evidence:** "Canvas apps now support modern controls and theming based on the Microsoft Fluent 2 design system. Modern controls offer improved accessibility, performance, and usability compared to classic controls" (A-12/D-08, 2026-02-23). Still preview 2026-07: Card, Copilot answer, Dropdown, Stream, Table (D-09). No classic-control retirement on the deprecations page (A-14). "Starting February 2026, modern controls in canvas apps have updated versions with new property names, enum-based values, and behavior changes" (T1 snippet). T3: missing hover/pressed state properties vs classic (D-17/D-18).
- **Why it matters:** New apps standardise on modern controls (accessibility + theming), but churn creates rework in Git-diffed YAML and component libraries; mixing generations doubles theming/QA effort.
- **Decision impact:** Pick control generation per app at day 1 and lock it.
- **Confidence:** HIGH status / MEDIUM churn details.
- **Sources:** A-12/D-08, D-09, A-14, D-17, D-18.

#### AA-12-CONF — Microsoft "50+ screens, excellent performance" vs community "30–40 screen maintainability ceiling"
- **Classification:** CONFLICTED (decision-weight kept)
- **Evidence:** Side A (T1): "Many successful Power Apps implementations use more than 100 tables and over 50 screens while keeping excellent performance" (A-07). Side B (T3/T4): 30–40-screen maintainability ceiling cluster; ~500 controls/app heuristics (PS-06 T4).
- **Assessment:** Not strictly contradictory — A is runtime performance with correct patterns; B is human maintainability of formula webs. Record both; size the ceiling by team and change rate, not runtime confidence.
- **Decision impact:** Screens projected > ~30–40 → design partition seams (AA-03) regardless.
- **Confidence:** HIGH that both positions exist.
- **Sources:** A-07, A-19.

### 3.2 Model-driven apps

#### AA-12 — Model-driven fit: process-driven, data-dense, automatic relational navigation
- **Classification:** DECISION CRITERION
- **Evidence:** "especially well suited to process driven apps that are data dense and make it easy for users to move between related records"; navigation through relationships "Automatic, provided relationships exist" vs canvas "Only where designed and applied using Power Fx formulas" (B-01). "without a data model housed within Microsoft Dataverse, you can't create a model-driven app" (B-01).
- **Decision impact:** STRONG signals: many related tables, record-centric work, back-office process users, audit/security granularity. Requires Dataverse (PS-02, PS-56, PS-42 premium).
- **Confidence:** HIGH.
- **Sources:** B-01 (2026-01-09).

#### AA-13 — UI customisation boundary: shell is platform-owned; "Limited, predominantly customization"
- **Classification:** CONSTRAINT
- **Evidence:** "with model-driven apps much of the user interface is determined for you and is largely designated by the components you add to the app" (B-01). Within the boundary, deep customisation IS supported: forms/views/dashboards, business rules, JS form scripting, command bar, PCF controls (B-08, B-09).
- **Decision impact:** "The app must look like X" (pixel layout, bespoke navigation metaphor) fails on model-driven core pages → custom page or canvas.
- **Confidence:** HIGH.
- **Sources:** B-01, B-08 (2026-05-19).

#### AA-14 — Theming boundary (modern/Fluent era): colours, font, logo, header only — and not everywhere; environment-scoped deployment
- **Classification:** CONSTRAINT + FACT
- **Evidence:** "classic theming isn't honored; however, makers can modify the colors used by the app"; "Modern themes currently support providing a custom theme for the entire app, overriding the app header colors, and setting a custom app logo. Other customizations … aren't available"; unthemed areas: "legacy grids, row summaries, focus view, and the sales pipeline" (B-05/D-11). Mechanism: `CustomTheme` XML web resource applied via environment setting — one artefact themes all new-look apps in the environment (D-11). New look mandatory April 2026; MDA custom theming GA ~March 2026 (T2/T3 signals, D-19).
- **Why it matters:** Operationally stronger than canvas theming (deploy once per environment) but shallower (no layout/typography control); accessibility-optimised palette "doesn't guarantee the seed color will appear in any slot".
- **Decision impact:** Branding beyond colour/font/logo → custom pages/PCF or off-platform. Multi-app estates: one design-token palette feeding both canvas theme YAML and MDA CustomTheme XML.
- **Confidence:** HIGH mechanism / MEDIUM GA dates.
- **Sources:** B-05/D-11 (2026-07-07), D-19.

#### AA-15 — Custom pages are Microsoft's convergence vehicle; embedded canvas apps are the legacy path
- **Classification:** PATTERN + RECOMMENDATION
- **Evidence:** "The custom page … brings the power of canvas apps into model-driven apps"; "In most cases, use custom pages instead of embedded canvas apps for tighter integration and better performance"; runtime/ALM/connectors/code components all GA; pages usable as full pages, dialogs, panes; "custom pages don't count toward the app limits"; licence follows the model-driven app (B-02).
- **Decision impact:** For Dataverse-centric solutions needing occasional pixel-perfect screens, "model-driven backbone + custom pages" is the Tier-1-endorsed alternative to a large standalone canvas app.
- **Confidence:** HIGH.
- **Sources:** B-02 (2026-03-13).

#### AA-16 — Custom pages: documented limitations (2026-08)
- **Classification:** CONSTRAINT + RISK
- **Evidence (B-03, verbatim highlights):** mobile "currently in public preview. Offline and device capability controls like barcode scanning, capturing photos from device, or attaching files isn't supported"; "aren't supported within App for Outlook"; double-publish trap — "the model-driven app continues to use the last version of the custom page when the model-driven app was published"; 8-hour hosting-session timeout; "page state isn't restored" on back-navigation or across multi-session tabs; third-party cookies required; "The number of connectors in a model-driven app, across all custom pages, shouldn't exceed 10 … connection references … 20"; not all canvas controls available; user-locale formats unsupported. Plus B-02: ≤ 25 pages/app; no direct conversion from standalone canvas apps.
- **Decision impact:** Converged pattern NOT fit for: offline, device-capability field UX, Outlook embedding, state-heavy flows, > 10-connector hubs.
- **Confidence:** HIGH.
- **Sources:** B-03 (2026-08-06), B-02.

#### AA-17 — Navigation is declarative (sitemap, role-filtered) and free; role-based segmentation is the native persona mechanism
- **Classification:** FACT + PATTERN
- **Evidence:** "Each app that you create can have its own site map" (B-10). "Customize the navigation bar based on user roles. Users should see only the modules and features that are relevant to their roles"; forms associable to security roles (B-07). App-per-persona over one Dataverse instance: N apps, each with own sitemap, role-filtered forms/views/BPFs (B-07, B-10, B-14). No Microsoft cap/optimal number of apps published (U-B2).
- **Decision impact:** "Users browse/search/filter many entity lists and drill into related records" and "≥ 2 personas" both favour model-driven; segmentation by app, not by in-app conditionals (contrast AA-10).
- **Confidence:** HIGH mechanism / MEDIUM doctrine ("prefer multiple smaller apps" not verbatim).
- **Sources:** B-10 (2026-02-12), B-07 (2024-06-03), B-14.

#### AA-18 — Deep linking is native and security-trimmed
- **Classification:** FACT + DECISION CRITERION
- **Evidence:** "URL addressable elements enable you to include links to model-driven apps, forms, views, and reports in other applications"; "can't bypass security" (B-06). `navbar=off`/`cmdbar=false` supported; `navbar` param "only supported in single-session model-driven apps".
- **Decision impact:** "Deep link to a record from email/Teams" favours model-driven over canvas (AA-09). No iFrame embedding (PS-12).
- **Confidence:** HIGH.
- **Sources:** B-06 (2026-04-21).

#### AA-19 — Business process flows: guided stage rails with hard limits, no logic of their own
- **Classification:** FACT + CONSTRAINT
- **Evidence:** "You can activate up to 10 business process flow processes per table. Each process can contain up to 30 stages. Multi-table processes can contain up to five tables"; BPFs "don't provide any conditional business logic or automation beyond providing the streamlined experience for data entry and controlling entry into stages" (B-04) — but stage-path branching exists (B-07); see CONFLICTED AA-C4. Offline only if app offline-enabled AND "The business process flow has a single table"; stage-exit workflow on the last stage never triggers (B-04).
- **Decision impact:** Multi-stage guided process (≤ 5 tables, ≤ 30 stages) → model-driven pillar; heavy conditional wizards → custom page instead of stretched BPF.
- **Confidence:** HIGH.
- **Sources:** B-04 (2026-08-15), B-07.

#### AA-20 — Form performance is design-governed: default-tab rendering, data-hungry controls, field-level-security cost
- **Classification:** RECOMMENDATION + RISK
- **Evidence:** "the controls of the default tab are always rendered when opening a record"; quick view forms, subgrids, timeline "produce the most strain"; "you might be able to add as many fields as a table allows, but it will greatly slow form loading"; "Field-level security does have an impact on your app's performance. Limit its use" (B-08, B-07). Multisession (browser-like tabs) extendable to custom apps via Copilot Service admin center — licence prerequisite UNVERIFIED (U-B1) (B-13).
- **Decision impact:** Data-dense fit assumes tabbed forms + subgrid discipline; no hard numeric caps published (U-B5).
- **Confidence:** HIGH guidance / MEDIUM multisession licensing.
- **Sources:** B-08, B-07, B-13.

### 3.3 Power Pages

#### AA-21 — Fit envelope: the Dataverse-fronted external channel, not a general web platform
- **Classification:** DECISION CRITERION
- **Evidence:** "Access to Dataverse records is automatically restricted in Power Pages when using forms, lists, Liquid, the Portals Web API" (C-01). T3: main reason to choose Pages over custom-on-Dataverse is avoiding "the need to reimplement the security model from scratch" (C-10); negatives: "developers have limited access to optimize server performance, caching, and load times" (C-11/C-12).
- **Decision impact:** Fit matrix row 4. The single driver question: is the data in Dataverse and is the interaction portal-shaped?
- **Confidence:** HIGH drivers / MEDIUM exact boundary (no Tier 1 decision tree exists, U-C2).
- **Sources:** C-01, C-10, C-11, C-12.

#### AA-22 — Authentication: Entra External ID is the viable CIAM for new sites; B2C closed to new customers; local auth "not recommended"
- **Classification:** FACT + CONSTRAINT
- **Evidence:** Provider table: Entra ID (OIDC/SAML2/WS-Fed), Entra External ID (OIDC), Azure AD B2C (OIDC), AD FS, social OAuth2, "Local authentication (not recommended)" (C-02). B2C: "effective May 1, 2025, Azure AD B2C will no longer be available to purchase for new customers"; supported "until at least May 2030" (C-13). Entra External ID has first-class setup (C-04). Local auth default `LocalLoginEnabled: True` (C-03).
- **Why it matters:** External identity is an architecture component with its own tenant, cost and ops, outside Pages licensing.
- **Decision impact:** New external site → Entra External ID as prerequisite dependency. See CONFLICTED AA-C5 (docs still recommend B2C).
- **Confidence:** HIGH.
- **Sources:** C-02, C-03 (2026-02-28), C-04, C-13.

#### AA-23 — UX surface: design studio + Liquid + Bootstrap 5; React SPA support GA January 2026 moves the bespoke-UX ceiling
- **Classification:** FACT + TRADE-OFF
- **Evidence:** "Power Pages supports Bootstrap version 3.3.6 and Bootstrap version 5" (C-05). SPA: "Public preview May 31, 2025; General availability Jan 31, 2026"; "creation and deployment of single-page applications (SPAs) … using familiar front-end frameworks like React … deploy it directly into a Power Pages site … integrate SPAs with Dataverse data and Power Pages Web APIs" (C-06); deploy via `pac pages upload-code-site` (C-14).
- **Why it matters:** The classic "bespoke UX infeasible on Pages" claim is superseded for greenfield; remaining ceilings: no server control, managed rendering, Web API not for third-party integration (PS-36), cache semantics (AA-27).
- **Decision impact:** Bespoke external UX no longer auto-exits the platform; SPA route trades away low-code forms/lists for full code ownership. Maturity risk: GA 8 months old; field evidence thin (U-C1).
- **Confidence:** HIGH facts / MEDIUM maturity.
- **Sources:** C-05, C-06 (2026-02-11), C-14, C-11.

#### AA-24 — Data access gated by table permissions + web roles; secure-by-default deny; Custom FetchXML access type in preview
- **Classification:** FACT / CONSTRAINT
- **Evidence:** "For a table permission to take effect, it has to be associated to one or more web roles"; access types Global/Contact/Account/Self/Parent/Custom (FetchXML, preview) (C-01).
- **Decision impact:** Row-level security is configuration, not code — the core Pages advantage; also the misconfiguration surface of AA-25.
- **Confidence:** HIGH.
- **Sources:** C-01 (2026-02-28).

#### AA-25 — RISK: table-permission misconfiguration exposed millions of records (AppOmni, Nov 2024); open registration ON by default
- **Classification:** RISK
- **Evidence:** AppOmni authorized testing found "several million records" exposed; NHS supplier leaked "over 1.1 million NHS employees'" PII; root causes: `Webapi/<object>/fields: *` wildcards, excessive permissions on Anonymous/Authenticated Users roles, Global access = "unrestricted read access to all rows"; "not a single implementation of column-level security was present" (C-07, corroborated C-15/C-16). Microsoft: configuration issue, added admin warning banners. Compounding default: `OpenRegistrationEnabled: True` — "allows any anonymous visitor to create a user account" (C-03).
- **Why it matters:** Secure-by-default platform, one-checkbox catastrophic misconfiguration. Any web role granted to generic "Authenticated Users" is effectively public while open registration is on.
- **Decision impact:** Acceptance conditions for anonymous/external designs: column security on PII tables; no Global read for Anonymous/Authenticated roles on sensitive tables; explicit Web API field allow-lists; open registration disabled unless required; periodic permission audit in run-book.
- **Confidence:** HIGH.
- **Sources:** C-07 (T3 primary, 2024-11-14), C-15, C-16, C-03.

#### AA-26 — Licensing shape: per unique user/site/month; tiered; cookie-based anonymous counting; bots excluded; internal users covered by Power Apps licences
- **Classification:** CONSTRAINT (architecture-shaping)
- **Evidence (C-00, 2026-08-14):** authenticated packs of 100: $200/pack/mo (Tier 1) → $75 (≥ 100 packs) → $50 (≥ 1,000); anonymous packs of 500: $75 → $37.50 → $25; minimums per environment: 25 authenticated / 200 anonymous; "aren't accumulated … wouldn't carry forward month to month"; anonymous uniqueness by browser cookie ("cleans up browser cookies … counted as a different user"); "Bots and crawler accessing anonymous pages of the website isn't counted"; internal users with Power Apps per-user/D365 licences "won't be counted"; storage accrual per pack (2 GB DB + 16 GB file per authenticated pack).
- **Why it matters:** Cost scales with audience uniqueness, not usage intensity — cheap for repeat heavy users, expensive for broad shallow reach; cookie counting inflates privacy-conscious audiences; bot exclusion removes a feared cost vector.
- **Decision impact:** Consumer-scale anonymous sites: model Tier-2/3 + PAYG before commitment (cross-ref PS-36).
- **Confidence:** HIGH (list prices on Learn).
- **Sources:** C-00.

#### AA-27 — Server-side cache: 15-minute SLA; writes from plugins/flows not reflected immediately; "never guaranteed to be immediate"
- **Classification:** CONSTRAINT
- **Evidence:** config cache "service level agreement of 15 minutes"; instant invalidation only for changes made through the website; "data reflection from Dataverse to websites is never guaranteed to be immediate" for plugin/workflow-driven changes — "This design approach isn't recommended"; manual clear "can lead to users facing performance issues" (C-08).
- **Decision impact:** Real-time status displays fed by background automation → CONDITIONAL/POOR or redesign (write-through on site, client-side Web API reads). Eventual consistency is architectural, not tunable.
- **Confidence:** HIGH.
- **Sources:** C-08 (2026-04-29).

#### AA-28 — CDN + WAF included (Azure Front Door); caching for anonymous users only; throughput ceilings unpublished (U-4 still open)
- **Classification:** FACT + CONSTRAINT
- **Evidence:** "CDN caching is available only for anonymous users"; authenticated pages "aren't available for caching"; production sites only; not in Singapore Local/China/UAE (C-09). "Both CDN and WAF capabilities are included as part of Power Pages licensing" (C-00). Requirements/limits page has no traffic/RPS/concurrency numbers (C-17); U-4 confirmed open in 2026.
- **Decision impact:** Anonymous content scales at the edge; authenticated high-concurrency always hits the app server with unquantified ceilings → load-test before consumer launches; keep custom-app counterfactual.
- **Confidence:** HIGH.
- **Sources:** C-09 (2026-06-18), C-00, C-17.

#### AA-29 — ALM: enhanced data model makes sites solution-aware (pipelines + Git), with documented drift traps; server-logic hybrid is the sanctioned Azure escape hatch
- **Classification:** FACT + TRADE-OFF + PATTERN
- **Evidence:** ALM: "New website components aren't automatically added to the solution"; editing target-env config "creates an unmanaged solution layer" blocking updates; manual post-import steps (C-18, C-19). Virtual tables unsupported in Pages solutions (PS-56). Server logic: "run JavaScript securely on the server … protected by web roles and table permissions"; "Integrate securely with REST APIs, Azure Functions"; sandbox — ECMAScript 2023, no fetch/XHR/DOM, timeout 120 s default/240 s max; tenant admins can "block outbound HTTP calls"; `ServerLogic/AllowedDomains` (C-20, C-21).
- **Decision impact:** Enterprise pipelines credible with checklist discipline; payment/integration/complex-validation requirements no longer auto-disqualify Pages — verify tenant governance posture and sandbox limits. Recent feature → verify GA per tenant (U-C3).
- **Confidence:** HIGH mechanics / MEDIUM maturity.
- **Sources:** C-18 (2026-01-29), C-19, C-20 (2026-05-13), C-21.

#### AA-30 — When a custom web app wins over Power Pages
- **Classification:** DECISION CRITERION
- **Evidence:** T3 triangulation: custom .NET over Dataverse means table permissions/web roles "must be re implemented from scratch" but gives full control; custom faces per-tenant Dataverse service-protection limits directly while Pages pools API calls with licences (C-10); custom wins on deep sign-in flows, downloads, payments, server/caching control (C-11, C-12). No Tier 1 "Pages vs custom app" decision doc exists (U-C2).
- **Decision impact:** Custom preferable when: data permanently outside Dataverse; guaranteed throughput/SLA needs; product-grade consumer UX beyond SPA-on-Pages; third-party API surface (PS-36); massive anonymous scale where per-user licensing loses to infra cost. Pages preferable when: Dataverse is the record system, row security matters, time-to-market + included WAF/CDN/auth outweigh control.
- **Confidence:** MEDIUM (T3 triangulated).
- **Sources:** C-10, C-11, C-12; PS-36, PS-56.

### 3.4 Componentisation and reuse

#### AA-31 — Canvas components: real reuse blocks, but excluded from galleries and forms; no data-bound encapsulation
- **Classification:** CONSTRAINT
- **Evidence (D-01):** "You can't insert a component into a gallery or a form (including SharePoint form)"; "You can't save data sources or controls that include data from those data sources (such as forms, fluid grids, or data tables) with components"; no `UpdateContext` inside components; no flows in component libraries. Limitations apply equally to libraries (D-02).
- **Why it matters:** The two most repetitive surfaces in business apps — gallery row templates and forms — cannot host components; repeated row UI stays copy-paste or moves to PCF.
- **Decision impact:** Componentisation strategy must exclude gallery/form internals; heavy repeated-row UX → PCF or design avoidance.
- **Confidence:** HIGH.
- **Sources:** D-01 (2026-01-13), D-02 (2026-08-20).

#### AA-32 — Component libraries are THE recommended reuse mechanism; updates are pull-based (edit + republish every consuming app); no npm-style dependency management
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Evidence:** "Component libraries are the recommended way to reuse components across apps" (D-02); app-to-app import retired (D-01). Component definitions are "copied into the definition of the canvas app … 'self-contained'"; updates notified only "when makers edit the apps in canvas app studio"; "Only published component library updates are available"; up-to-5-minute propagation (D-02, D-03). Best practice: "Limit the number of components in a library to 20 to get optimal performance" (D-03); solution export "always exports the latest version" — no version pinning.
- **Why it matters:** "Fix once, deployed everywhere" is not achievable in canvas: one shared-header fix = N manual edit/publish cycles. Estate rebrand touches every app.
- **Decision impact:** Cost model for canvas design systems includes per-app update labour; pipelines must sync library and app versions before export.
- **Confidence:** HIGH.
- **Sources:** D-01, D-02, D-03 (2022-06-10).

#### AA-33 — "Allow customization" forks permanently; local edits detach from the library
- **Classification:** TRADE-OFF / RISK
- **Evidence:** "The association with the component library is removed once you edit the component"; local copies "don't receive updates" (D-02); unmanaged layers in target environments block updates (D-03). Well-Architected: components "versatile enough to be used as-is or with slight variations (through parameters) … without the need for modifications" (D-13).
- **Decision impact:** Governance rule required: lock components (managed, no customization) and accept rigidity, or allow forks and accept drift; parameter-driven component APIs are the mitigation.
- **Confidence:** HIGH.
- **Sources:** D-02, D-03, D-13.

#### AA-34 — PCF: pixel-level extensibility with extracted limitations; premium licensing is CONDITIONAL on non-connector external calls (corrects common belief); pro-dev ownership cost
- **Classification:** CONSTRAINT + FACT + TRADE-OFF
- **Evidence:** Limitations (D-04, content now extracted): "Microsoft Dataverse dependent APIs, including WebAPI, are not available for Power Apps canvas applications yet"; no `localStorage`/`sessionStorage`; "Custom auth in code components is not supported"; not supported on-premises. Licensing (D-05, 2026-01-09): "Code components that connect to external services or data directly through the user's browser client and not through connectors are premium … Code components that don't connect to external services or data … the app remains standard, and end-users need at least an Office 365 license." Maintenance: manifest version bumps required for updates; "Code components from an untrusted source can potentially access security tokens and data" — admin review mandated (D-06); virtual React controls pin platform React/Fluent versions, no Power Pages support for platform libraries (D-07). PCF works in canvas, model-driven and Pages; code components allowed in galleries (unlike canvas components, AA-31).
- **Why it matters:** A purely visual PCF control does NOT make a standard-connector canvas app premium — weakens one cost argument against "canvas + PCF for brand-critical UX" (PS-10). But PCF-in-canvas is UI extensibility only, not a data/auth escape hatch.
- **Decision impact:** Brand-critical UX + custom data access patterns → code apps or custom web, not PCF. PCF viable only with long-term pro-dev ownership; citizen-only orgs should buy (Creator Kit) not build — noting Creator Kit is "sample implementations" support-status and CoE kit "is no longer actively maintained" (D-14, D-12).
- **Confidence:** HIGH.
- **Sources:** D-04 (2025-07-01), D-05, D-06 (2026-08-20), D-07, D-12, D-14.

#### AA-35 — Code apps GA (February 2026): supported architecture rung between canvas and custom web; updates PS-03
- **Classification:** FACT + CONSTRAINT (updates PS-03)
- **Evidence:** GA blog 2026-02-05 (D-20); overview (D-15, 2026-08-12) no preview qualifier; "End users that run code apps need a Power Apps Premium license." ALM improved since PS-03: "The Power Apps CLI can automatically place your app inside a Dataverse solution when you run `pa app push` … use Power Platform Pipelines to deploy across stages" (D-22); still "Don't support source code integration [Power Platform Git integration]". Persisting constraints: "compiled app assets are served from a publicly accessible endpoint that doesn't support IP-based restrictions today. To restrict access by IP, use Conditional Access"; "Don't store sensitive user or organizational data in the app"; no Windows player; no PowerBIIntegration; no SharePoint forms (D-15, D-23). Governance parity: DLP at runtime, Conditional Access, sharing limits, tenant isolation (D-15). Mobile-player support and offline: UNDOCUMENTED (U-D2, U-D3).
- **Why it matters:** "Custom UX → leave the platform" boundary moved: the exit trigger is now licensing economics, network isolation, offline and external reach — not UX capability (PS-10 softened).
- **Decision impact:** Code apps legitimately enter Options as a supported architecture; POOR for IP-allowlist estates, Windows-player audiences, offline, anonymous.
- **Confidence:** HIGH.
- **Sources:** D-15, D-20 (T2), D-22 (2026-08-27), D-23.

#### AA-36 — Decision ladder: plain canvas → components/libraries → PCF → code apps → custom web
- **Classification:** DECISION CRITERION (synthesis; each rung Tier 1-anchored)
- **Evidence-anchored ladder:**

| Rung | Choose when | Cost of the step | Anchors |
|---|---|---|---|
| Plain canvas + modern controls/themes | Fluent-consistent, brand-tinted look suffices | none; fastest | D-08, D-10 |
| Canvas components + library | Repeated composite UI across screens/apps; low-code team | pull-based update labour; no gallery/form insertion; fork risk | AA-31..33 |
| PCF code components | Pixel-level brand control; gallery-internal custom UI; behaviour canvas can't express | pro-dev toolchain, security review, version discipline; premium only if non-connector external calls | AA-34 |
| Code apps | Full SPA control (routing, npm, own design system) with platform auth/connectors/governance | Premium per end user; public asset endpoint; no Windows player; own the frontend engineering | AA-35 |
| Custom web app | IP-restricted hosting, offline, public/anonymous users, freedom from per-user premium | lose connectors, managed governance; build auth/DLP equivalents | AA-35 inverse, AA-30 |

- **Decision impact:** Options-phase scaffold for any "the UI must be X" requirement.
- **Confidence:** HIGH per-rung facts / MEDIUM framing.
- **Sources:** as per table.

#### AA-37 — Estate-level reuse: Well-Architected prescribes a design system; Microsoft admits coherence is hard; accelerators carry support risk
- **Classification:** RECOMMENDATION + RISK
- **Evidence:** XO:02: design system = "design tokens, components, pattern libraries, and guidelines"; "Use these controls as much as possible for basic needs, then consider building composite components where gaps exist"; "Currently, coherence is a challenge because components, systems, processes, and culture are often not shared" (D-13). Canvas theming = seed-colour 16-slot palette, shared across apps by YAML copy-paste — no tenant-level theme object (D-10). Creator Kit: "the kit itself represents sample implementations"; issues via GitHub (D-14). CoE theming components: kit "no longer actively maintained" (D-12).
- **Decision impact:** Estate design-token governance is organisational (repo of theme YAML + libraries + guidelines), not platform-enforced; adopting Creator Kit/CoE = owning a fork.
- **Confidence:** HIGH.
- **Sources:** D-13 (2025-08-05), D-10 (2026-01-21), D-12, D-14.

### 3.5 Mobile, Wrap, Intune

#### AA-38 — Wrap: branded native iOS/Android from CANVAS apps only; drags an Azure + signing footprint; GA
- **Classification:** FACT + CONSTRAINT (resolves R-14, part 1)
- **Evidence:** "The wrap feature in Power Apps lets you package your canvas app as a custom-branded Android or iOS app"; "only supports canvas apps (not model-driven apps)"; apps must be in a solution, same environment; multi-app packages navigate via `Launch()` (E-01). Requirements: Entra app registration, "Azure subscription (for Azure Key Vault and Blob Storage)" (paid), code signing (macOS+Xcode / Android Studio or Key Vault auto-sign); "Signing your mobile app with Xcode isn't supported in wrap" (E-01, E-02). No preview banners.
- **Why it matters:** "Branded mobile app" is satisfiable in-platform only on the canvas branch; a model-driven architecture cannot ship a store-branded app. Wrap is not no-code end-to-end: Azure infra + certificate lifecycle + store accounts required.
- **Decision impact:** Branded app + complex relational back-office UX = tension (forces canvas or drops branding). Orgs without Azure subscription access or Apple Business Manager cannot Wrap.
- **Confidence:** HIGH.
- **Sources:** E-01 (2025-02-04), E-02 (2026-06-12).

#### AA-39 — Wrap hard limitations: no push, no B2C, no sovereign clouds, no CMK/Lockbox, size caps; monthly rewrap cadence; licence per end user
- **Classification:** CONSTRAINT + TRADE-OFF
- **Evidence:** "Push notifications aren't supported"; "There's no visible sign out button"; APK ≤ 100 MB / AAB ≤ 150 MB; Android back-button desync; "Wrap doesn't support sovereign cloud environments"; offline wrapped apps "only show image thumbnails" (E-03). "Can I create B2C mobile apps with Power Apps? No." Wrap "doesn't support Customer-Managed Keys (CMK) or Lockbox … customer assets might be exposed to Microsoft service operators during the build process" (E-02). Updates: app content auto-downloads, but "rewrap and redistribute your mobile app at least monthly" recommended; icon/colour changes need rewrap (E-02). Licensing: "you don't need a premium license for wrap. However, if your APK uses certain connectors…"; "Users must have a Power Apps license to use wrapped apps" (E-02, E-01).
- **Why it matters:** These are the exact failure modes of "branded consumer app": consumer identity, engagement push, data sovereignty all out. Shell maintenance is a permanent monthly DevOps commitment; per-user licensing kills large-audience economics before technical limits do.
- **Confidence:** HIGH.
- **Sources:** E-02, E-03.

#### AA-40 — Wrap verdict (binary-testable): when Wrap satisfies "branded mobile app" and when custom native remains
- **Classification:** DECISION CRITERION (resolves R-14)
- **Evidence:** Synthesis of AA-38/39 + Intune findings, each cell Tier 1-traceable.
- **Wrap suffices when ALL hold:** internal or Entra B2B-guest audience with Power Apps licences; canvas app(s); branding = icon/splash/welcome/colours; distribution via Intune/store/ABM; no push; commercial cloud; offline needs met by canvas offline-first; team sustains monthly rewrap. Conditional Access caveat: "Require approved client app" policies block wrapped apps ("You can't get there from here") — policy exclusion needed; wizard auto-configures the Intune MAM API permission (E-02).
- **Custom native (or Power Pages PWA) needed when ANY holds:** consumer/B2C or anonymous users; push required; native UX beyond canvas (gestures, widgets, background processing); sovereign cloud; CMK/Lockbox mandate; per-user licensing uneconomic; > 150 MB.
- **Confidence:** HIGH.
- **Sources:** E-01, E-02, E-03.

#### AA-41 — Intune/MAM: Power Apps Mobile is a managed app (MAM DLP, encryption at rest); advanced Intune app settings unsupported; not a canvas-vs-model-driven differentiator
- **Classification:** FACT + CONSTRAINT (resolves R-14, part 2)
- **Evidence:** Intune can "publish, push, configure, secure, monitor, and update" Power Apps mobile; "Limit sharing of corporate data among apps by restricting data leakage through cut, copy, paste, and save-as. Provide encryption at rest" (E-09). "Intune advanced app settings aren't currently supported with Power Apps Mobile"; per-platform configuration; "Intune is a separate Microsoft product that is not included with Power Apps mobile" (E-09). Power Apps out of scope for Intune Multiple Managed Accounts (E-15).
- **Decision impact:** BYOD + sensitive data coverable via MAM on the shared player (hosts canvas AND model-driven — no app-type differentiator); differentiators are vs Wrap (CA-policy negotiation) and vs browser (MAM doesn't apply; use Conditional Access session controls).
- **Confidence:** HIGH.
- **Sources:** E-09 (2024-10, upd. 2025-05), E-15.

### 3.6 Offline (re-verification and extension of PS-35)

#### AA-41a — Canvas offline-first re-verified (2026-06 page): Dataverse-only, standalone-only; flows, virtual/elastic tables, non-Dataverse connectors excluded; foreground-only sync
- **Classification:** CONSTRAINT
- **Evidence (E-05, 2026-06-17):** "The offline-first feature works for standalone canvas apps only. It doesn't work for embedded canvas apps, custom pages, or canvas apps in Teams"; "Non-Dataverse connectors, like SharePoint, aren't supported"; "Virtual tables and elastic tables aren't supported"; "Power Automate flows aren't supported in offline mode"; 3,000,000-record sync cap; no M:N, one-level lookups, ≤ 15 relationships/table, ≤ 14 image columns per profile; "Data can only be synced regularly when Power Apps is running in the foreground of your device, with the screen unlocked." LoadData/SaveData fallback unchanged: "30-70 MB", manual conflicts (E-04). PS-35 numbers confirmed unchanged.
- **Decision impact:** Offline + SharePoint data = forced Dataverse migration; offline + automation logic = redesign (logic into app or post-sync); M:N/deep-lookup data models need rework before Options.
- **Confidence:** HIGH.
- **Sources:** E-05, E-04 (2024-06-05), E-16.

#### AA-41b — Model-driven offline re-verified: field-level security, personal views, Dataverse search, iOS form web resources all degrade offline
- **Classification:** CONSTRAINT
- **Evidence (E-06, 2024-09-26 upd. 2025-03):** "Field level security and field sharing aren't supported in Mobile offline mode"; personal views unsupported; HTML/JS web resources on forms "Not supported" on iOS (OK Android/Windows); "Dataverse search isn't supported in offline mode"; grid column filtering disabled when an offline profile exists "even when there's network connectivity"; duplicate detection/merge unsupported; custom pages have no offline. Same 3M-row and profile limits as canvas.
- **Decision impact:** Offline + field-level-security requirement = design-level conflict — resolve by data segregation, not FLS. iPad-based field workforce + script-driven forms = critical iOS gap.
- **Confidence:** HIGH.
- **Sources:** E-06, E-17.

#### AA-41c — Offline decision table: which offline requirement forces which architecture; which exceeds Power Platform
- **Classification:** DECISION CRITERION
- **Evidence:** synthesis of AA-41a/b + Pages PWA: Pages pages can be offline-enabled "with read-only content"; "pages with forms to complete or query operations won't function without an internet connection" (E-18).

| Offline requirement | Forced architecture |
|---|---|
| Field worker, Dataverse, ≤ 3M rows, standard conflicts | Canvas offline-first OR model-driven offline (native player, Dataverse mandatory) |
| Offline + heavy custom UX | Canvas offline-first (standalone) |
| Offline + complex relational back-office forms | Model-driven offline (accepting AA-41b gaps) |
| Small cache, non-Dataverse source | LoadData/SaveData (30–70 MB, manual conflicts) — fragile |
| Offline in Teams / embedded canvas / custom pages | Unsupported |
| Offline in a desktop browser | Exceeds Power Platform (PS-35 confirmed) |
| Offline write on a public site | Exceeds Power Platform (Pages = read-only PWA) |
| Custom conflict rules, background/locked-screen sync, multi-day sync queues | Beyond documented capability (INF) → custom mobile development |
| Offline + field-level security | Unsupported combination |
| Offline + Power Automate logic | Unsupported — move logic into app or post-sync |

- **Decision impact:** The offline row of the architecture decision model; each cell evidence-anchored. External audience + no offline writes + branding → Pages PWA beats Wrap (no per-user Power Apps licence for the shell).
- **Confidence:** HIGH documented cells / MEDIUM custom-sync verdict (inference from absence).
- **Sources:** E-04, E-05, E-06, E-18.

### 3.7 Device capabilities and notifications

#### AA-42 — Device hardware pins architecture to native mobile players: NFC iOS/Android only; barcode/camera not in desktop browser or Teams mobile; Windows player materially weaker
- **Classification:** CONSTRAINT
- **Evidence:** "ReadNFC is only supported when running the app on a native mobile app" (E-12). Barcode: "When using desktop browsers, the barcode reader isn't supported"; camera/barcode "isn't supported in Teams Mobile" (E-13). Windows player: "The following is not supported: Advanced controls such as sensors… Mixed reality controls… NFC function" (E-11); docs stale (2023-10) but no retirement on the deprecations page (E-10, 2026-05-22) — see CONFLICTED AA-C6.
- **Decision impact:** Scan/NFC/GPS requirements → iOS/Android native player (or Wrap embedding it); "warehouse scanning on Windows handhelds" is RISKY (barcode gaps, no NFC). Kiosk/shared-device mode: UNKNOWN — no Tier 1 doc found (U-E2).
- **Confidence:** HIGH.
- **Sources:** E-10..E-14.

#### AA-43 — Push notifications: only via Microsoft's own players (Notification V2 connector); none in Wrap; throttles undocumented
- **Classification:** CONSTRAINT + UNKNOWN
- **Evidence:** Connector sends "push notifications to canvas Power Apps, model-driven Power Apps, Field Service, and Sales"; recipient must have the Power Apps mobile app installed, opened once, signed in (E-08); not available US DoD. Wrap: "Push notifications aren't supported" (E-03). No throttling limits documented (U-E1) — partial answer to the R-13 notification-throttle gap: the ceiling is unpublished, not resolved.
- **Decision impact:** {branded app, push} unsatisfiable in Power Apps (AA-40); high-volume push designs must pilot-validate limits.
- **Confidence:** HIGH capabilities / UNKNOWN throttles.
- **Sources:** E-08, E-03.

### 3.8 Accessibility and localisation

#### AA-44 — Accessibility by app type: Pages platform-attested to WCAG 2.2 / Section 508 / EN 301 549; model-driven built-in; canvas maker-dependent with documented impossible patterns needing PCF
- **Classification:** DECISION CRITERION (extends PS-11)
- **Evidence:** Power Pages "conforms to the WCAG 2.2 accessibility standard … the Section 508 guidelines … ETSI EN 301 549"; "When you customize your Power Pages site, you're responsible for meeting accessibility standards" (E-07, 2025-04-22). Model-driven: built-in; screen readers supported; custom web resources are developer responsibility (E-21, E-22). Canvas hard limitations (E-20, 2021-02): "Dialogs and user interfaces that appear on top of other content are not supported"; "It is not possible to react to specific key presses"; no custom ARIA; escape hatch is "Create a code component" (PCF). Canvas guidance page re-verified (content-updated 2025-05, position unchanged: maker responsibility) (E-19). Caveat: the 2021 limitations page may understate modern-control improvements (AA-C7).
- **Why it matters:** Public-sector-grade accessibility is platform-attested only for Pages and effectively built-in for uncustomised model-driven; on canvas some WCAG patterns are impossible with built-in controls. Conformance covers the platform, never the maker's content (U-E3: no per-app-type ACR).
- **Decision impact:** Legal accessibility mandate → prefer model-driven or Pages; canvas only with a11y-skilled makers + PCF budget + audit.
- **Confidence:** HIGH.
- **Sources:** E-07, E-19, E-20, E-21, E-22.

#### AA-45 — Localisation by app type: canvas fully manual; model-driven built-in (language packs + translation export); Pages 43 languages; RTL undocumented for standalone canvas
- **Classification:** DECISION CRITERION (resolves R-13 localisation)
- **Evidence:** Canvas: no resource-file system; official pattern = translation-table + `LookUp` on `Language()` (E-23, 2021-01); locale formatting built-in via `Text()`/`Value()` (E-24). Model-driven: "Dataverse enables you to install multiple language packs"; label translation via export→Excel→import (E-26); platform chrome translated. Pages: 43 OOB languages + custom languages ("System messages … aren't translated into custom languages") (E-25, 2025-08-06). RTL: custom pages "Right-To-Left (RTL) is fully supported … the page will change at runtime automatically" except icons/shapes/images; RTL preview "is not available in standalone canvas apps" (E-27); no Learn page documents RTL for standalone canvas.
- **Why it matters:** Canvas multi-language cost grows linearly with screens × languages and content updates need republish; Pages/model-driven have platform machinery.
- **Decision impact:** > 2–3 languages → model-driven or Pages strongly favoured. RTL (Arabic/Hebrew) → standalone canvas effectively infeasible (INF from absence); use model-driven or custom pages. Locale date/number formats alone: no differentiator.
- **Confidence:** HIGH mechanisms / MEDIUM canvas-RTL infeasibility (absence-based).
- **Sources:** E-23..E-27.

#### AA-46 — Device/UX architecture selection matrix (synthesis)
- **Classification:** DECISION CRITERION / PATTERN

| Requirement | Selected architecture | Anchor |
|---|---|---|
| Field worker, offline, hardware (camera/scan/GPS) | Canvas or model-driven + Dataverse offline, native player | AA-41a/b, AA-42 |
| NFC interaction | Canvas on iOS/Android native player only | AA-42 |
| Branded internal/B2B mobile app | Wrap (AA-40 conditions) | AA-38..40 |
| Branded app + push, or B2C consumer app | Custom native; no-offline variant: Pages PWA | AA-39, AA-43, AA-41c |
| BYOD + corporate data protection | Power Apps Mobile under Intune MAM; browser + CA session controls fallback | AA-41 |
| External authenticated users, browser-first | Power Pages | AA-21..24 |
| Public-sector accessibility mandate | Model-driven or Pages; canvas only with discipline + PCF | AA-44 |
| Multi-language (> 2–3) or RTL | Model-driven / Pages; avoid canvas | AA-45 |
| Desktop-browser offline / offline in Teams | Exceeds Power Platform | AA-41c |
| Kiosk / shared-device mode | UNKNOWN (U-E2) | — |

- **Confidence:** cells inherit anchors.

---

## 4. Anti-patterns (application-architecture specific)

Extends `platform-suitability.md §5` (AP-1..AP-16).

| Id | Anti-pattern | Why it fails | Origin | Findings |
|---|---|---|---|---|
| AP-17 | God canvas app: many personas/experiences in one artefact | Formula sprawl, one-maker bottleneck, Studio degradation; partitioning is the documented remedy | MS | AA-03, AA-04, AA-06, AA-10 |
| AP-18 | Everything in OnStart; `Navigate` in OnStart | Deprecated architecture; retired function; load-time cost | MS | AA-05 |
| AP-19 | Collect-everything workarounds for delegation limits | Microsoft-named anti-pattern trio; N+1 request storms | MS | AA-07, PS-13 |
| AP-20 | Copy-paste component reuse / app-to-app import | Formally retired; invisible formula duplication | MS | AA-32, AA-04 |
| AP-21 | Editing library components in consuming apps ("allow customization" as default) | Permanent fork; unmanaged layers block updates | MS | AA-33 |
| AP-22 | PCF-for-everything before exhausting platform controls | Inverts Well-Architected ordering; inherits pro-dev maintenance + security-review burden | MS | AA-34, AA-37 |
| AP-23 | Unreviewed third-party PCF | "can potentially access security tokens and data" | MS | AA-34 |
| AP-24 | Model-driven for mobile-first field capture with device hardware via custom pages | Device controls unsupported in custom pages; offline gaps | MS | AA-16, AA-41b |
| AP-25 | Bespoke branding pursued inside model-driven core pages | Theming = colours/font/logo only; unthemed areas remain | MS | AA-14 |
| AP-26 | Pages: Global read + generic Authenticated/Anonymous roles + Web API `*` columns on sensitive tables; open registration left ON | Documented mass-exposure incident class | T3+MS | AA-25 |
| AP-27 | Pages fed by background automation presented as real-time | Server cache; freshness "never guaranteed to be immediate" | MS | AA-27 |
| AP-28 | Wrap chosen for consumer/B2C or push-dependent apps | B2C unsupported; push unsupported | MS | AA-39, AA-40 |
| AP-29 | Role-based UI via Visible formulas treated as security | Client-side only; data remains queryable via connection identity | INF | AA-10 |
| AP-30 | Stretching BPF into a conditional wizard engine | BPFs carry no business logic; stage/table caps | MS | AA-19 |

---

## 5. Conflicts (CONFLICTED)

| Id | Topic | Source A | Source B | Assessment |
|---|---|---|---|---|
| AA-C1 | Canvas scale | T1 "50+ screens … excellent performance" (A-07) | T3/T4 30–40-screen maintainability ceiling | Performance vs maintainability; record both (AA-12-CONF) |
| AA-C2 | Canvas co-authoring | 2022–24 articles + one MS blog: live Git co-authoring | T1 2025-05: feature "removed and no longer supported" (A-06) | T1 wins; flag stale sources |
| AA-C3 | PCF licensing | Community "PCF = premium" | T1 2026-01: premium only for non-connector external calls (D-05) | Current Learn page wins; rule shifted over time → short half-life |
| AA-C4 | BPF conditional logic | "don't provide any conditional business logic" (B-04) | "Conditional branching is allowed in business process flows" (B-07) | Reconciled: stage-path branching exists; BPFs still execute no logic |
| AA-C5 | Pages CIAM recommendation | Learn still recommends Azure AD B2C (C-03, 2026-02) | B2C closed to new purchase since 2025-05 (C-13); External ID positioned successor (C-04) | New builds → Entra External ID; record doc inconsistency |
| AA-C6 | Windows player future | Current docs live, no deprecation listed (E-10) | Stale docs (2023-10), narrower capability set, ecosystem retirements | Windows-player-dependent designs RISKY, not blocked |
| AA-C7 | Canvas accessibility limitations currency | Limitations page 2021-02 (E-20) | Modern controls added accessible Tab list etc. (A-12) | 2021 page may overstate gaps; verify per pattern |
| AA-C8 | Pages bespoke UX | T3/T4 2023–25 "React not really supported" (C-11/C-12) | T1 SPA GA Jan 2026 (C-06) | Superseded for greenfield; still true for classic Liquid sites |
| AA-C9 | Model-driven version control | T4 "no version control" | T1 solution-based ALM + Git integration | Weak signal; no per-artifact rollback UI confirmed either way; do not promote |

---

## 6. Unknowns (UNKNOWN)

| Id | Unknown | Why it matters | Resolution path |
|---|---|---|---|
| U-A1 | Numeric caps on screens/controls per canvas app | Sizing heuristics rest on T4 | None published; symptoms only |
| U-A2 | Formal GA status of Power Fx UDFs | Build-standard bet | Watch release plans |
| U-A3 | Solution checker depth on canvas Power Fx | Governance tooling value | Test |
| U-A5 | T1 statement that Visible-hiding is not a security boundary | AP-29 citation strength | Locate or keep INF |
| U-A6 | Max data sources per canvas app (community: 30) | Integration-heavy apps | Not on current limits page |
| U-B1 | Licence prerequisite for multisession in custom model-driven apps | Contact-centre requirements | Verify via Copilot Service licensing |
| U-B2 | Optimal/max number of model-driven apps per environment | App-per-persona sizing | No numeric guidance |
| U-B4 | Classic model-driven UI retirement timeline | Estate planning | Message center |
| U-B5 | Quantified form-load thresholds (fields/subgrids) | Estimation | Microsoft gives direction, not numbers |
| U-C1 | Whether SPA/code sites change Pages licensing/entitlements | Cost of bespoke external UX | No Learn statement |
| U-C2 | Tier 1 decision guidance Pages vs custom web | Boundary confidence stays MEDIUM | None exists; T3 triangulation |
| U-C3 | Server logic GA/regional availability | Hybrid pattern maturity | Verify per tenant |
| U-C4 | Custom (FetchXML) table-permission GA date | Access-model design | Preview watch |
| U-C5 | Pages list/grid performance limits | External UX at volume | Not published |
| U-D1 | Per-control GA status of modern controls | Control-generation lock-in | Reference page preview labels |
| U-D2 | Code apps in iOS/Android mobile players | Mobile reach of code apps | Not documented either way |
| U-D3 | Code apps offline capability | Offline reach | Treat unsupported until documented |
| U-D4 | Enhanced component properties (behaviour functions) status | Component API design | Was experimental |
| U-E1 | Push-notification throttling limits | High-volume notify designs | Pilot-validate (R-13 partial: unpublished) |
| U-E2 | Kiosk / shared-device mode for Power Apps Mobile | Frontline scenarios (ties U-14) | No Tier 1 doc; treat unsupported |
| U-E3 | Per-app-type accessibility conformance reports | Legal conformance claims for maker-built canvas apps | Product-level ACRs only |
| U-E4 | Wrap-specific offline setup differences | Wrapped field apps | Assume = canvas offline-first pending verification |
| U-4 | Power Pages traffic/throughput ceilings | Public high-traffic sites | CONFIRMED STILL OPEN 2026-09 (C-17) |

---

## 7. Source register

Sub-registers by research pass. All Learn URLs fetched 2026-09-02 unless marked "search-verified". Date = ms.date (updated date where noted). Duplicates across passes: code apps overview (A-09 = D-15), custom page overview (A-13 = B-02), modern controls overview (A-12 = D-08).

### 7.1 Canvas (A-)

| Id | Tier | Title | URL | Date |
|---|---|---|---|---|
| A-01 | T1 | Building responsive canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/build-responsive-apps | 2022-01-27 |
| A-02 | T1 | Create responsive layouts in canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-responsive-layout | 2026-01-13 |
| A-03 | T1 | Build large and complex canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/working-with-large-apps | 2023-04-07 |
| A-04 | T1 | App object (Formulas/UDFs/OnStart/StartScreen) | https://learn.microsoft.com/en-us/power-platform/power-fx/reference/object-app | 2026-06-11 |
| A-05 | T1 | Source control for canvas apps (Git integration) | https://learn.microsoft.com/en-us/power-platform/alm/git-integration/canvas-apps-git-integration | 2025-10-08 |
| A-06 | T1 | Disconnect Git version control (feature removed) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/git-version-control | 2025-05-14 |
| A-07 | T1 | How to create performant Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview | 2026-08-20 |
| A-08 | T1 | Power Apps system requirements and limits | https://learn.microsoft.com/en-us/power-apps/limits-and-config | 2026-01-12 |
| A-09 | T1 | Power Apps code apps overview (= D-15) | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview | 2026-08-12 |
| A-10 | T1 | Canvas deep linking | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/how-to/deep-linking | 2022-07-27 |
| A-11 | T1 | Debugging canvas apps with Live monitor | https://learn.microsoft.com/en-us/power-apps/maker/monitor-canvasapps | 2024-11-14 |
| A-12 | T1 | Modern controls and theming overview (= D-08) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/overview-modern-controls | 2026-02-23 |
| A-13 | T1 | Custom page convergence (= B-02) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-app-page-overview | 2026-03-13 |
| A-14 | T1 | Canvas deprecations | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/important-changes-deprecations | 2026-01-09 |
| A-15 | T1 | Important changes — Test Engine deprecation | https://learn.microsoft.com/en-us/power-platform/important-changes-coming#deprecation-of-test-engine | n/a (search-verified) |
| A-16 | T2 | Canvas app coding standards (PDF, June 2024) | https://www.microsoft.com/power-platform/blog/wp-content/uploads/2024/06/PowerApps-canvas-app-coding-standards-and-guidelines.pdf | 2024-06 |
| A-18 | T2 | UDFs/UDTs/enhanced component properties blog | https://www.microsoft.com/en-us/power-platform/blog/power-apps/user-defined-functions-user-defined-types-and-enhanced-component-properties-move-forward/ | n/a |
| A-19 | T3/T4 | Independent cluster: complexity-ceiling, co-authoring (stale), role-UI patterns | aidevme/ESPC/Medium/Withum/Arinco/M. Devaney | 2025–2026 |

### 7.2 Model-driven + custom pages (B-)

| Id | Tier | Title | URL | Date |
|---|---|---|---|---|
| B-01 | T1 | Overview of building a model-driven app | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-driven-app-overview | 2026-01-09 |
| B-02 | T1 | Converge model-driven and canvas apps (custom page) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-app-page-overview | 2026-03-13 |
| B-03 | T1 | Known issues with custom pages | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-app-page-issues | 2026-08-06 |
| B-04 | T1 | Business process flows overview | https://learn.microsoft.com/en-us/power-automate/business-process-flows-overview | 2026-08-15 |
| B-05 | T1 | Modern themes in model-driven apps (= D-11) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/modern-theme-overrides | 2026-07-07 |
| B-06 | T1 | Open apps/forms/views with a URL | https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/open-forms-views-dialogs-reports-url | 2026-04-21 |
| B-07 | T1 | UI/UX design components for model-driven apps (D365 guidance) | https://learn.microsoft.com/en-us/dynamics365/guidance/develop/ui-ux-component-details-model-driven-apps | 2024-06-03 |
| B-08 | T1 | Design forms for performance | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/design-performant-forms | 2026-05-19 |
| B-09 | T1 | Command designer limitations (sighted) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/command-designer-limitations | n/a |
| B-10 | T1 | App designer (sitemap) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/design-custom-business-apps-using-app-designer | 2026-02-12 |
| B-11 | T1 | Plan designer | https://learn.microsoft.com/en-us/power-apps/maker/plan-designer/plan-designer | 2026-08-07 |
| B-12 | T1 | Build your solution (plan designer) | https://learn.microsoft.com/en-us/power-apps/maker/plan-designer/build-solution | 2025-12-09 |
| B-13 | T1 | Enable multisession in custom apps (sighted) | https://learn.microsoft.com/en-us/dynamics365/customer-service/administer/enable-multisession-custom-apps | n/a |
| B-14 | T1/2 | Application modernization white paper (sighted) | https://learn.microsoft.com/en-us/power-platform/guidance/white-papers/application-modernization | n/a |

### 7.3 Power Pages (C-)

| Id | Tier | Title | URL | Date |
|---|---|---|---|---|
| C-00 | T1 | Licensing FAQ (Power Pages section) | https://learn.microsoft.com/en-us/power-platform/admin/powerapps-flow-licensing-faq | 2026-08-14 |
| C-01 | T1 | Table permissions | https://learn.microsoft.com/en-us/power-pages/security/table-permissions | 2026-02-28 |
| C-02 | T1 | Authentication overview | https://learn.microsoft.com/en-us/power-pages/security/authentication/ | 2026-02-28 |
| C-03 | T1 | Local authentication + registration settings | https://learn.microsoft.com/en-us/power-pages/security/authentication/set-authentication-identity | 2026-02-28 |
| C-04 | T1 | Entra External ID setup | https://learn.microsoft.com/en-us/power-pages/security/authentication/entra-external-id | 2026-01-22 |
| C-05 | T1 | Bootstrap overview | https://learn.microsoft.com/en-us/power-pages/configure/bootstrap-overview | 2024-03-19 |
| C-06 | T1 | Release plan: single-page applications | https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave1/power-pages/build-modern-single-page-applications | 2026-02-11 |
| C-07 | T3 | AppOmni: Power Pages data exposure | https://appomni.com/ao-labs/microsoft-power-pages-data-exposure-reviewed/ | 2024-11-14 |
| C-08 | T1 | Server-side caching | https://learn.microsoft.com/en-us/power-pages/admin/clear-server-side-cache | 2026-04-29 |
| C-09 | T1 | CDN configuration | https://learn.microsoft.com/en-us/power-pages/configure/configure-cdn | 2026-06-18 |
| C-10 | T3 | M. Mendes (MVP): Pages vs custom .NET + Dataverse | https://michelcarlo.com/2025/06/01/ | 2025-06-01 |
| C-11 | T4 | UDS Systems: reasons Pages might not fit | uds.systems/blog | n/a |
| C-12 | T4 | Xtivia: when (not) to choose Power Pages | solutions.microsoft.xtivia.com/blog | n/a |
| C-13 | T1 | Azure AD B2C FAQ (purchase closure) | https://learn.microsoft.com/en-us/azure/active-directory-b2c/faq | n/a (search-verified) |
| C-14 | T1 | pac pages CLI (upload-code-site) | https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/pages | n/a (search-verified) |
| C-15 | T3 | SecurityWeek: Low-Code, High Risk | securityweek.com | 2024-11 |
| C-16 | T3 | Infosecurity: Power Pages misconfiguration | infosecurity-magazine.com/news/microsoft-power-pages/ | 2024-11 |
| C-17 | T1 | Power Pages system requirements and limits | https://learn.microsoft.com/en-us/power-pages/system-requirements | 2026-04-28 |
| C-18 | T1 | Use solutions with Power Pages | https://learn.microsoft.com/en-us/power-pages/configure/power-pages-solutions | 2026-01-29 |
| C-19 | T1 | Pages pipelines / enhanced data model | https://learn.microsoft.com/en-us/power-pages/configure/power-pages-pipelines | n/a (search-verified) |
| C-20 | T1 | Server logic overview | https://learn.microsoft.com/en-us/power-pages/configure/server-logic-overview | 2026-05-13 |
| C-21 | T1 | Server logic → Azure Function tutorial | https://learn.microsoft.com/en-us/power-pages/configure/server-logic-azure-function | n/a (search-verified) |

### 7.4 Components, theming, code apps (D-)

| Id | Tier | Title | URL | Date |
|---|---|---|---|---|
| D-01 | T1 | Canvas component overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component | 2026-01-13 |
| D-02 | T1 | Component library | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library | 2026-08-20 |
| D-03 | T1 | Component library ALM | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library-alm | 2022-06-10 |
| D-04 | T1 | PCF limitations | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations | 2025-07-01 |
| D-05 | T1 | PCF overview (licensing section) | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview | 2026-01-09 |
| D-06 | T1 | Code components for canvas apps | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps | 2026-08-20 |
| D-07 | T1 | React controls & platform libraries | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/react-controls-platform-libraries | 2025-10-10 |
| D-08 | T1 | Modern controls overview (= A-12) | (see A-12) | 2026-02-23 |
| D-09 | T1 | Modern controls reference (preview labels) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-controls-reference | 2026-07-20 |
| D-10 | T1 | Canvas modern theming | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming | 2026-01-21 |
| D-11 | T1 | Model-driven modern themes (= B-05) | (see B-05) | 2026-07-07 |
| D-12 | T1 | CoE theming components (kit unmaintained) | https://learn.microsoft.com/en-us/power-platform/guidance/coe/theming-components | 2026-04-20 |
| D-13 | T1 | Well-Architected XO:02 design standards | https://learn.microsoft.com/en-us/power-platform/well-architected/experience-optimization/design-standards | 2025-08-05 |
| D-14 | T1 | Creator Kit overview (preview) | https://learn.microsoft.com/en-us/power-platform/guidance/creator-kit/overview | 2024-08-12 |
| D-15 | T1 | Code apps overview (= A-09) | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview | 2026-08-12 |
| D-16 | T2 | What's new March 2026 (data grid GA) | microsoft.com/power-platform/blog | 2026-03 |
| D-17 | T3 | PowerApps911: modern vs classic reference | powerapps911.com | n/a |
| D-18 | T3 | SharePains: classic→modern migration | sharepains.com | 2026-01-27 |
| D-19 | T3 | MC1254543 MDA theming GA / new look mandatory | mc.merill.net/message/MC1254543 | GA 2026-03-31 |
| D-20 | T2 | Code apps GA blog | microsoft.com/en-us/power-platform/blog/power-apps/generally-available-host-and-run-code-apps-in-power-apps/ | 2026-02-05 |
| D-21 | T4 | Aric Levin: code apps GA licensing signal | ariclevin.com | n/a |
| D-22 | T1 | ALM for code apps | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/how-to/alm | 2026-08-27 |
| D-23 | T1 | Code apps system configuration | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/system-limits-configuration | 2026-08-12 |

### 7.5 Mobile, Wrap, offline, a11y, l10n (E-)

| Id | Tier | Title | URL | Date |
|---|---|---|---|---|
| E-01 | T1 | Overview of wrap | https://learn.microsoft.com/en-us/power-apps/maker/common/wrap/overview | 2025-02-04 |
| E-02 | T1 | FAQ for wrap | https://learn.microsoft.com/en-us/power-apps/maker/common/wrap/faq | 2026-06-12 |
| E-03 | T1 | Advantages and limitations of Wrap | https://learn.microsoft.com/en-us/power-apps/maker/common/wrap/limitations | 2025-02-04 |
| E-04 | T1 | Mobile offline for canvas apps overview | https://learn.microsoft.com/en-us/power-apps/mobile/canvas-mobile-offline-overview | 2024-06-05 |
| E-05 | T1 | Mobile offline limitations — canvas | https://learn.microsoft.com/en-us/power-apps/mobile/limitations-canvas-apps | 2026-06-17 |
| E-06 | T1 | Mobile offline limitations — model-driven | https://learn.microsoft.com/en-us/power-apps/mobile/offline-limitations | 2024-09-26 (upd. 2025-03) |
| E-07 | T1 | Accessibility in Power Pages | https://learn.microsoft.com/en-us/power-pages/admin/accessibility | 2025-04-22 |
| E-08 | T1 | Power Apps Notification V2 connector | https://learn.microsoft.com/en-us/connectors/powerappsnotificationv2/ | 2024-03 (upd. 2025-10) |
| E-09 | T1 | Manage mobile app with Intune | https://learn.microsoft.com/en-us/power-apps/mobile/intune | 2024-10-11 (upd. 2025-05) |
| E-10 | T1 | Important changes (deprecations) | https://learn.microsoft.com/en-us/power-platform/important-changes-coming | 2026-05-22 |
| E-11 | T1 | Use Power Apps for Windows | https://learn.microsoft.com/en-us/power-apps/mobile/windows-app-use | 2023-10-25 |
| E-12 | T1 | ReadNFC function | https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-readnfc | n/a (search-verified) |
| E-13 | T1 | Limitations of controls in canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/control-limitations | n/a (search-verified) |
| E-14 | T1 | Mobile sensors how-to | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/how-to/mobile-sensors | n/a (search-verified) |
| E-15 | T1 | Intune Multiple Managed Accounts (Power Apps out of scope) | https://learn.microsoft.com/en-us/intune/app-management/protection/multiple-managed-accounts | n/a (search-verified) |
| E-16 | T1 | 2025 wave 2: offline profiles in maker studio | https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave2/power-apps/create-offline-profiles-maker-studio-canvas-apps | n/a |
| E-17 | T1 | Set up mobile offline (model-driven) | https://learn.microsoft.com/en-us/power-apps/mobile/setup-mobile-offline | n/a (search-verified) |
| E-18 | T1 | Power Pages progressive web apps | https://learn.microsoft.com/en-us/power-pages/configure/progressive-web-apps | n/a (search-verified) |
| E-19 | T1 | Create accessible canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps | 2022-09-06 (upd. 2025-05) |
| E-20 | T1 | Accessibility limitations in canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-limitations | 2021-02-26 |
| E-21 | T1 | Screen reader in model-driven apps | https://learn.microsoft.com/en-us/power-apps/user/screen-reader | n/a (search-verified) |
| E-22 | T1 | Accessible web resources (model-driven) | https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/create-accessible-web-resources | n/a (search-verified) |
| E-23 | T1 | Build a multi-language canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/multi-language-apps | 2021-01-27 |
| E-24 | T1 | Build global support into canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/global-apps | 2016-10-25 (upd. 2025-05) |
| E-25 | T1 | Multiple-language Power Pages sites | https://learn.microsoft.com/en-us/power-pages/configure/enable-multiple-language-support | 2025-08-06 |
| E-26 | T1 | Export table/column text for translation | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/export-customized-entity-field-text-translation | n/a (search-verified) |
| E-27 | T1 | Localize labels/strings on a custom page (RTL) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/custom-page-localize | n/a (search-verified) |

---

## 8. Evidence-quality notes

- **Aged pages (> 18 months) still relied on:** A-01 (2022-01), A-03 (2023-04), A-10 (2022-07), D-03 (2022-06), E-04 (2024-06), E-06 (2024-09, upd. 2025-03), E-11 (2023-10), E-19 (2022-09, upd. 2025-05), E-20 (2021-02), E-23 (2021-01), E-24 (2016, upd. 2025-05). Findings on them carry MEDIUM on currency where noted.
- **Search-verified (not full-fetched) sources:** A-15, B-09, B-13, B-14, C-13, C-14, C-19, C-21, E-12..E-15, E-17, E-18, E-21, E-22, E-26, E-27. Claims relying solely on them are excerpt-level.
- **T3 with commercial bias:** C-11/C-12 (consultancies), D-17/D-18 (trainers/consultants), A-19 cluster — used for signals and negative evidence only, never for capability claims.
- **Feature churn:** modern controls (property renames Feb 2026), code apps (GA Feb 2026), Pages SPA (GA Jan 2026), Pages server logic (2025–26), Entra External ID migration — all short-half-life facts; re-verify before pack encoding.
- **"Choose your app type" guidance:** the retired patterns/planning pages are replaced by the AI Plan designer (B-11/B-12); the durable written criteria are the B-01 comparison table plus the D365 guidance-hub UI/UX articles. No standalone Microsoft decision tree exists in 2026.

---

## 9. Implications for the aisa knowledge model (pointers, not pack content)

- **Technology-neutral Discovery signals suggested by this area:** number of distinct persona experiences; form factors required (phone/tablet/desktop/browser mix); responsive-reflow expectation; device hardware needs (camera/scan/GPS/NFC); offline depth (none / read / write / custom sync) and offline surface (mobile app vs browser vs Teams); branded-app requirement and its audience (internal/B2B/consumer); push-notification requirement; deep-link/share-by-URL frequency; navigation shape (record-centric relational browsing vs task wizard); accessibility regime (legal mandate vs best-effort); language count and RTL; expected screen count and change velocity; maker team size and pro-dev capacity; UI-reuse ambitions across the estate; freshness expectation for externally visible data; external-user identity type.
- **Hard boundaries with Microsoft-stated evidence:** components not in galleries/forms (AA-31); no co-authoring per canvas artefact (AA-06); custom pages ≤ 25 / connectors ≤ 10, no offline/device controls (AA-16); Wrap no push/B2C/sovereign (AA-39); offline never in browser, never with flows or FLS (AA-41a/b); Pages cache freshness (AA-27); model-driven theming = colours/font/logo (AA-14); BPF caps (AA-19); code apps public asset endpoint + premium (AA-35).
- **Corrected boundaries vs prior corpus:** PCF ≠ automatic premium (AA-34, AA-C3); code apps GA with pipelines ALM (AA-35, updates PS-03); Pages bespoke UX possible via SPA GA (AA-23, softens PS-10 external leg); modern controls soften but don't overturn PS-10's brand-critical verdict (AA-11).
- **Architecture options the pack must be able to output:** single canvas app; partitioned canvas suite (hub-and-spoke); model-driven app(s) per persona; model-driven shell + custom pages; canvas + PCF; component-library-backed canvas estate; code app; Power Pages (Liquid or SPA); Pages + server-logic/Azure hybrid; Wrap-packaged canvas; Pages PWA; custom web/native.
- **Validation before commitment (typical):** persona-count and screen-count projection against partition thresholds; responsive prototype on the real device mix; offline limitation checklist against the data model (M:N, lookups, FLS); deep-link inventory; accessibility audit path per app type; language matrix; Wrap Conditional Access dry run; Pages table-permission review + load test; component-library update-labour estimate; control-generation lock decision.

---

## 10. Summary

**Strongest fit signals**
- Data-dense, record-centric, relational-navigation, audited back-office work on Dataverse → model-driven.
- Task-focused internal app, 1–2 personas, mixed/non-Dataverse sources, device hardware, specific form factor → canvas.
- Authenticated external users over Dataverse with portal-shaped interactions → Power Pages.
- Structured backbone + few bespoke screens → model-driven shell + custom pages.

**Conditional fit signals**
- Responsive multi-device, multi-persona, long-lived/high-change, team development → canvas only with partitioning + UDF/Git/test discipline.
- Anonymous/consumer audiences → Pages, conditional on capacity budget + hardened table permissions.
- Brand-critical UX → ladder: modern controls → PCF → code apps (premium/user) before leaving the platform.
- Branded mobile → Wrap, only for internal/B2B, no-push, commercial-cloud cases with rewrap ops.
- Offline → only native mobile players over Dataverse, within documented feature gaps.

**Poor fit signals**
- Offline in browser/Teams/custom pages; offline writes on Pages; offline + FLS or flows.
- Branded app + push notifications; B2C native mobile; sovereign-cloud Wrap.
- Pixel-perfect branding inside model-driven core pages; consumer-grade UX on model-driven.
- Data permanently outside Dataverse for model-driven/Pages UX (virtual-table gaps).
- Third-party API surface, guaranteed throughput, server control → custom web.

**Important decision criteria**
- Persona-experience count; screen-count × change-velocity; maker team size; form-factor mix; device hardware; offline depth/surface; audience identity (internal / B2B / authenticated external / anonymous); branding depth; push requirement; deep-link frequency; accessibility regime; language count + RTL; UI-reuse scope; freshness expectations; pro-dev capacity; premium-licence budget.

**Important anti-patterns**
- God canvas app; OnStart-heavy initialization; collect-everything delegation workarounds; copy-paste component reuse; library forks via "allow customization"; PCF-before-platform-controls; unreviewed third-party PCF; model-driven for device-capability field capture; Pages with Global/anonymous permissions and Web API wildcards; Wrap for consumer/push scenarios; Visible-formula "security"; BPF stretched into a logic engine.

**Important unknowns**
- Pages throughput ceilings (U-4, confirmed still unpublished); code apps mobile/offline; push-notification throttles; kiosk/shared-device mode; multisession licensing for custom apps; numeric canvas size caps; per-app-type accessibility conformance for maker-built apps; SPA-on-Pages licensing effects.
