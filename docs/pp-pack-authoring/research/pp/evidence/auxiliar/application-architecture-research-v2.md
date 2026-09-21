Research Status: REVISED (v2, addresses application-architecture-review.md; ungated)
Research Confidence: MEDIUM-HIGH
Gate: PENDING

# Application Architecture — Research Evidence v2

Research area: **02 — Application Architecture** (`../research-areas.md`).
Version: **v2, 2026-09-02**. Supersedes `application-architecture.md` (v1 DRAFT). Addresses every HIGH finding and all MEDIUM/LOW findings of `application-architecture-review.md` except where marked "still open" in §12.
Source policy: `../source-policy.md`. Cross-references `platform-suitability.md` (VALIDATED) as **PS-nn** / **U-nn**; its fit-matrix rows as **PS row n**.

**Purpose.** Answer: *"Given these application requirements, which application architecture should aisa consider — canvas, model-driven, converged (model-driven + custom pages), Power Pages, code apps, Teams-hosted, embedded surfaces, Wrap, hybrid with Azure, or custom development — and when does the recommendation change?"*

**Provenance statement (corrected per review Finding 1).** Sources are of three kinds, marked in §10: **fetched** (page retrieved, ms.date read from metadata — the default), **search-verified** (snippet only; findings relying solely on such a source are capped at MEDIUM), and **T2/T3/T4** (non-Learn). The v1 header's "all Tier 1 claims verified via fetch" was inaccurate; in v2 the seven decision-weight sources that were search-verified in v1 have been fetched (V-01..V-19), and the remaining search-verified ones are listed explicitly.

**Origin tags (per review Finding 11).** Every finding carries **Origin:** MS (Microsoft statement) / INF (analyst inference from documented limits) / T3 (independent) / UNKNOWN. Verdict phrasing: STRONG = "no documented constraint violated"; POOR from INF is phrased as "treat as unsupported until verified".

**Gap resolution carried from platform-suitability §7:** R-14 (Wrap, Intune/MAM) RESOLVED (AA-38..AA-41). R-13 localisation RESOLVED (AA-48); push-notification throttles remain UNKNOWN (AA-46). PS-03 UPDATED (code apps: GA wording, B2B guests now supported, pipelines ALM; AA-35). PS-11, PS-35, PS-53 re-verified. PS-02 phone-browser condition restored (AA-45). PS-16 refined at application level (AA-50).

**Volatility.** Modern controls, code apps, Pages SPA/code sites, Pages server logic, Entra External ID migration, model-driven "new look" — all 2025–2026 features with short half-lives. Re-verify before pack encoding.

---

## 1. App-type fit matrix

| # | Approach | STRONG fit | CONDITIONAL fit | POOR fit | Origin | Findings |
|---|---|---|---|---|---|---|
| 0 | **Configure / buy / first-party (no new app)** | Requirement already met by a Dynamics 365 first-party app, Microsoft 365 feature, or ISV product (PS-41, PS-44) | Fit with partial configuration | — | MS | AA-36 rung 0 |
| 1 | **Canvas app** | Task-focused internal app; 1–2 personas; moderate screen count; mixed or non-Dataverse sources via connectors; specific form factor; device hardware (camera/scan/GPS/NFC) | Responsive multi-device (opt-in effort); multi-persona role UI; queried tables > 2,000 rows (PS-13); long-lived + high change rate; team > 1–2 makers; brand-critical UX (PCF) | Many divergent experiences in one artefact; Dataverse-centric relational process apps; external/anonymous audiences; native-client embedding (PS-12) | MS + INF | AA-01..AA-11 |
| 2 | **Model-driven app** | Data-dense, record-centric, process-driven work over Dataverse; automatic relational navigation; row/column security + audit; native record deep links; accessibility mandates; multi-language | Bespoke screens via custom pages (AA-16); branding = colours/font/logo; offline (gaps AA-43); multisession (unmanaged-solution-only, licence indirect) | Brand-first/consumer UX; mobile-first field capture with device hardware in custom pages; phone-browser access; external data with audit/security/offline needs (virtual tables, PS-56); anonymous audiences | MS | AA-12..AA-20, AA-45 |
| 3 | **Model-driven shell + custom pages** | Structured backbone + a few bespoke screens | ≤ 25 pages/app; ≤ 10 connectors across pages; state loss on back-navigation; double-publish trap | Offline or device-capability field UX; Outlook embedding; state-heavy flows | MS | AA-15, AA-16, AA-03 |
| 4 | **Power Pages (Liquid or SPA)** | Authenticated external users over Dataverse; portal-shaped interactions; WCAG/EN 301 549 mandates; multi-language (Liquid sites) | Anonymous/consumer audiences (capacity licensing + misconfiguration RISK); bespoke SPA UX (product-documented, no preview wording, but single-language, no Git, no PWA); traffic spikes (U-4); near-real-time freshness | System of record not in Dataverse; offline data capture; third-party API surface (PS-36); server/caching control | MS + T3 | AA-21..AA-30 |
| 5 | **Code apps** | Bespoke SPA over connectors/Dataverse with platform governance; pro-dev team; internal or B2B audience; premium budget | Solutions + pipelines ALM (no Git integration); Conditional Access instead of IP restriction | IP-allowlist estates (public asset endpoint); Windows player; offline (undocumented → treat unsupported); anonymous users | MS | AA-35 |
| 6 | **Teams-hosted app (Dataverse for Teams)** | Team-scoped app inside Teams; ≤ 2 GB / ~1M rows; seeded licences; no PCF, model-driven, offline, API, plug-ins needed | Growth beyond limits → one-way upgrade to full Dataverse (then premium licences for all users) | Any need on the PS-16 exclusion list; device hardware in Teams (camera/barcode/sensors unsupported) | MS | AA-50 |
| 7 | **Embedded canvas surfaces** (Power BI visual; SharePoint customized forms; Teams tab) | Write-back or drill-through from a report (≤ 1,000 rows passed); form over a single SharePoint list for list readers; existing app surfaced in a Teams tab | Refresh latency in Power BI; no automated cross-environment copy for SharePoint forms | Embed-for-customers (Power BI); Report Server; portable/solution-managed form; device sensors/attachments in Teams | MS | AA-51 |
| 8 | **Wrap (branded native mobile)** | — | Internal or B2B-guest audience, canvas apps, branding = icon/splash/colours, Intune/store distribution, monthly rewrap ops | Consumer/B2C; push notifications; sovereign clouds; CMK/Lockbox; > 150 MB | MS | AA-38..AA-40 |
| 9 | **Hybrid with Azure** (Pages server logic → Functions; plug-ins/Functions behind any UI) | Logic, integration or compute beyond low-code limits with the UI kept on-platform | Sandbox/timeout limits; tenant may block outbound calls | — | MS | AA-29, PS-09, PS-44 |
| 10 | **Custom web / native development** | Data outside Dataverse permanently; guaranteed throughput/SLA; product-grade consumer UX; public API; branded app + push; custom sync/conflict rules; per-user licensing uneconomic at scale | — | — | MS + T3 | AA-30, AA-36, AA-40, AA-44 |

---

## 2. Decision boundaries (requirement × condition → architecture)

Each boundary is tagged with origin. Boundaries derived from absence of documentation are phrased "treat as unsupported until verified".

- Requirement already met by first-party/M365/ISV → configure or buy before any app type (MS, PS-41/PS-44, AA-36 rung 0).
- Responsive multi-device UX × canvas → opt-in rebuild with containers per screen; "Scale to fit" default wastes screen (MS, AA-02).
- Projected screens beyond what one maker can hold, or ≥ 2–3 divergent persona experiences × canvas → partition (multiple apps + `Launch()` with state loss) or model-driven shell + custom pages; retrofit is manual (MS, AA-03). No Microsoft numeric threshold exists (U-A1); the 30–40-screen figure is T3/T4 heuristic only (AA-C1).
- Team > 1–2 makers per canvas artefact → co-authoring removed; one editor per app/custom page; parallelism only via architecture (MS, AA-06).
- Many shareable/bookmarkable record destinations → model-driven native record URLs; canvas deep links hand-built per destination; mobile deep links break May 2026 without environment ID (MS, AA-09, AA-18).
- Phone-browser access × model-driven → unsupported; native player required (MS, AA-45).
- Offline → decision table AA-44; browser offline, Teams/custom-page offline, Pages offline-write, offline + field-level security, offline + flows all UNSUPPORTED (MS).
- Branded mobile app × push notifications → unsatisfiable in Power Platform (MS, AA-40, AA-46).
- Anonymous/public audience × sensitive Dataverse data → Pages RISK: anonymous table permission = "visible to anyone"; open registration ON by default; daily tenant security checks exist (MS + T3, AA-25).
- Legal accessibility mandate → Pages platform-attested; model-driven built-in; canvas maker-dependent with documented impossible patterns needing PCF (MS, AA-47).
- > 2–3 languages → model-driven or Pages Liquid sites; canvas = hand-built dictionary × screens × languages; Pages SPA sites are single-language (MS, AA-48, AA-23). RTL on standalone canvas → no Microsoft statement either way → treat as unsupported until verified (UNKNOWN, AA-48).
- Brand-critical UX ladder: modern Fluent controls → canvas components/library → PCF (premium only if non-connector external calls) → code apps (premium/user) → custom web (MS, AA-36).
- Reusable UI inside galleries/forms → canvas components excluded; PCF only (MS, AA-31).
- Back-office automation writes that users must see immediately × Power Pages → server cache (15-min SLA; plugin/flow writes "never guaranteed to be immediate") (MS, AA-27).
- Team-scoped app + seeded licences + no PCF/model-driven/offline/API → Teams-hosted; growth → one-way upgrade to full Dataverse with premium licences (MS, AA-50).
- Form over one SharePoint list, readers = list readers → customized form; needs solution ALM/portability → standalone app (MS + INF, AA-51).
- Report-driven write-back ≤ 1,000 rows, internal users → Power BI visual; external/embed-for-customers or Report Server → not supported (MS, AA-51).
- Contact-centre multisession × custom model-driven app → unmanaged solution only; conflicts with managed-solution production doctrine (PS-05) (MS, AA-20).
- Concurrent users → no documented ceiling for any app type; capacity governed by data-source and request limits → load-test (MS + UNKNOWN, AA-53, PS-20).
- Long lifetime × low tolerance to vendor UI change → model-driven carries highest wave-driven UI exposure (mandatory new look), canvas medium, code apps lowest UI exposure but full own-maintenance (MS + INF, AA-54).
- Non-Dataverse data + model-driven/Pages UX → virtual tables drop audit/security/offline/Pages (PS-56) → replicate into Dataverse or CUSTOM.
- Component-library estate → pull-based updates (edit + republish every consuming app); "allow customization" forks permanently (MS, AA-32, AA-33).

---

## 3. Findings

Ids AA-nn are stable from v2 onward (v1→v2 mapping in §11). Sub-registers: A- (canvas), B- (model-driven), C- (Pages), D- (components/code apps), E- (mobile/offline/a11y/l10n), V- (v2 verification fetches).

### 3.1 Canvas apps

#### AA-01 — Canvas fit envelope: task-focused UX layer over any connector; the ceiling is maintainability and persona count, not a documented size cap
- **Classification:** DECISION CRITERION
- **Origin:** MS (constraints) + INF (envelope)
- **Evidence:** Partition guidance positions task-scoped apps as the healthy unit (A-03); comparison table: canvas "Full control" of UI, "Dataverse + many others using connectors", "Only responsive if designed in this way" vs model-driven "Limited, predominantly customization", "Dataverse only", "Automatically responsive" (B-01). No Microsoft numeric limit on screens or controls exists (U-A1). *Per PS-06 and review Finding 3, the vendor statement "100 tables and over 50 screens" (A-07) is inadmissible as capability evidence and is recorded only in AA-C1.*
- **Why it matters:** Canvas POOR verdicts come from audience (external), embedding (PS-12), data volume (PS-13) and organisational factors (team size, personas), not from a hard cap.
- **Decision impact:** Fit matrix row 1.
- **Confidence:** HIGH (facts) / MEDIUM (envelope is synthesis).
- **Sources:** A-03, B-01.

#### AA-02 — Responsiveness is opt-in effort, not default; tooling has documented gaps
- **Classification:** CONSTRAINT + TRADE-OFF
- **Origin:** MS
- **Evidence:** "your entire layout scales to fit the screen… can't take advantage of the additional pixels"; "You activate responsiveness by turning off the app's Scale to fit setting, which is on by default"; "you adjust some settings and write expressions throughout your app" (A-02). Gaps: "The authoring canvas doesn't respond to the sizing formulas created. To test responsive behavior, save and publish your app"; dragging a control "overwrite[s] those expressions or formulas"; Data table/Charts/Add picture "not supported in the layout containers"; Center/End container options "can cause child controls inaccessible" (A-01, A-02).
- **Decision impact:** Multi-form-factor requirement raises canvas effort per screen with a publish-to-test loop; single-form-factor apps avoid it.
- **Confidence:** HIGH.
- **Sources:** A-01 (2022-01-27), A-02 (2026-01-13).

#### AA-03 — Partitioning is the documented remedy for large canvas apps; both partition patterns carry costs
- **Classification:** PATTERN + CONSTRAINT (extends PS-06)
- **Origin:** MS
- **Evidence:** "large apps can be split into smaller sections"; `Launch()` between apps but "State in the original app is lost when another app is launched" (A-03). Converged route: "Don't exceed 25 custom pages in a model-driven app"; a custom page "is expected to typically be a single screen with loose coupling"; standalone canvas apps "aren't supported for use as a custom page" (B-02).
- **Decision impact:** Plan partition seams up front; retrofitting is manual screen-by-screen either way. Where the maintainability ceiling sits is not quantified by Microsoft (AA-C1).
- **Confidence:** HIGH.
- **Sources:** A-03 (2023-04), B-02 (2026-03-13).

#### AA-04 — Formula sprawl (> 256K characters) is the documented root cause of Studio degradation; copy-paste silently duplicates it
- **Classification:** ANTI-PATTERN + FACT (extends PS-06)
- **Origin:** MS
- **Evidence:** "nearly all apps with a long load time … have at least one formula of more than 256,000 characters. Some apps with the longest load times have formulas of more than 1 million characters"; "copying and pasting a control with a long formula duplicates the formula … without it being realized" (A-03).
- **Decision impact:** Long-lived apps need formula-length review (feasible on `.pa.yaml` source, PS-48) and named-formula refactoring.
- **Confidence:** HIGH.
- **Sources:** A-03.

#### AA-05 — Sanctioned initialization/maintainability stack: named formulas + StartScreen + user-defined functions; OnStart is deprecated architecture
- **Classification:** RECOMMENDATION + FACT
- **Origin:** MS
- **Evidence:** "Using the OnStart property can cause performance problems"; `Navigate` in OnStart "is retired"; OnStart "might be disabled by default" (A-04). UDFs documented without preview flag: typed parameters/returns, behavioural bodies, user-defined types; "Recursion isn't yet supported"; named formulas cannot have side effects (A-04). Studio-load improvement figure ("as much as 80%", A-03) is a vendor measurement, cited as direction only.
- **Why it matters:** Narrows (does not close) the "no subroutines" critique; no unit-test framework for UDFs (AA-08).
- **Decision impact:** UDF-first + App.Formulas + StartScreen as build standard; heavy OnStart in an estate = refactoring backlog.
- **Conditions:** U-A2: formal GA status of UDFs not explicitly announced.
- **Confidence:** HIGH behaviour / MEDIUM GA status.
- **Sources:** A-03, A-04 (2026-06-11), A-18 (T2).

#### AA-06 — Concurrent development: real-time co-authoring removed; Git integration commits only on publish; one maker per app/page
- **Classification:** CONSTRAINT + RISK
- **Origin:** MS
- **Evidence:** "Git version control for editing apps has been removed and is no longer supported" (A-06, 2025-05-14). Git integration: "Changes aren't available to commit until you publish"; "You can't edit the .pa.yaml files directly in your repository if your app contains code components" (A-05). Custom pages: "one maker can edit one custom page at a time" (B-02).
- **Decision impact:** Maker team > 1–2 per app is itself a partition / model-driven / code-apps signal. Stale 2022–2024 co-authoring articles: AA-C2.
- **Confidence:** HIGH.
- **Sources:** A-05 (2025-10-08), A-06, B-02.

#### AA-07 — The platform's own limits induce its documented anti-patterns; Live Monitor's worked example shows UI-formula N+1 request storms
- **Classification:** ANTI-PATTERN + FACT
- **Origin:** MS
- **Evidence:** "Common anti-patterns include loading too much data, turning everything into collections, and overloading OnStart. People often use these patterns to work around real or perceived Power Apps limitations" (A-07). Monitor: a label's `CountRows` over 12 entities re-evaluated per write → HTTP 429; "For each single request to add a record, you're potentially making 12 additional requests"; "Debug published app … has a detrimental impact on the performance of your app for all your users" (A-11).
- **Decision impact:** Monitor-based data-call audit in definition-of-done; maker skill is an architecture risk factor.
- **Confidence:** HIGH.
- **Sources:** A-07 (2026-08-20; used here for its anti-pattern statement, not its scale claim), A-11 (2024-11-14), A-16 (T2).

#### AA-08 — Canvas testing story unstable: Test Engine deprecated April 2026; migration path is code-first Playwright
- **Classification:** RISK (corroborates PS-53)
- **Origin:** MS
- **Evidence (fetched v2, V-07, 2026-05-22 upd. 2026-08-14):** "Effective April 2026, Test Engine is deprecated. The documentation and GitHub repository are no longer maintained by Microsoft"; "Test Engine has near-zero usage and failed to meet customer needs … The Power Fx implementation created unnecessary limitations that are avoided if using Playwright directly"; "The Power Platform Playwright samples guide the use of Playwright for Power Platform test automation."
- **Decision impact:** Long life + high change velocity → budget Playwright or accept manual regression; genuine argument for code apps/custom at high change velocity.
- **Confidence:** HIGH.
- **Sources:** V-07, A-19 (T3).

#### AA-09 — Navigation: no route model; deep linking hand-built per destination; mobile deep-link contract changes May 2026
- **Classification:** PATTERN + CONSTRAINT
- **Origin:** MS
- **Evidence:** Deep link = `?param=` read with `Param()`, routed in `StartScreen`, hydrated in `OnVisible` (A-10). "Starting May 1, 2026, all deep links for Power Apps mobile must include the environment ID as a required parameter. Existing deep links without these parameters will stop working" (A-14).
- **Decision impact:** Heavy-linking requirements favour model-driven (AA-18).
- **Confidence:** HIGH.
- **Sources:** A-10 (2022-07-27), A-04, A-14 (2026-01-09).

#### AA-10 — Role-based UI in one canvas app is formula-level branching, client-side only; connection identity, not UI, governs data access
- **Classification:** PATTERN + RISK
- **Origin:** MS (mechanism) + MS partial (security anchor via PS-31) + INF
- **Evidence:** Tier 1 entry-branching example `If(LookUp(Attendees, User = User().Email).Staff, StaffPortal, HomeScreen)` (A-04). Security anchor (per review Finding 16): implicitly shared connections expose the maker's credentials to all app users regardless of UI (PS-31/S-43), establishing that data access is governed by connection identity and data-source security, not by `Visible`. No single Learn sentence "hiding controls is not security" was located (U-A5).
- **Decision impact:** ≥ 2 divergent experiences → app-per-persona or model-driven (AA-17). Enforcement belongs in Dataverse roles / source security.
- **Confidence:** HIGH mechanism / MEDIUM security citation.
- **Sources:** A-04, PS-31 (S-43), A-19 signals.

#### AA-11 — Modern (Fluent 2) controls are the current generation; classic not deprecated; modern set still churning
- **Classification:** FACT + RISK
- **Origin:** MS + T3
- **Evidence:** "Canvas apps now support modern controls and theming based on the Microsoft Fluent 2 design system. Modern controls offer improved accessibility, performance, and usability compared to classic controls" (A-12). Still preview 2026-07: Card, Copilot answer, Dropdown, Stream, Table (D-09). No classic-control retirement on the deprecations page (A-14). "Starting February 2026, modern controls in canvas apps have updated versions with new property names, enum-based values, and behavior changes" (T1 snippet). T3: missing hover/pressed state properties vs classic (D-17, D-18).
- **Decision impact:** Pick control generation per app at day 1 and lock it; churn creates YAML/library rework.
- **Confidence:** HIGH status / MEDIUM churn details.
- **Sources:** A-12 (2026-02-23), D-09, A-14, D-17, D-18.

### 3.2 Model-driven apps

#### AA-12 — Model-driven fit: process-driven, data-dense, automatic relational navigation
- **Classification:** DECISION CRITERION
- **Origin:** MS
- **Evidence:** "especially well suited to process driven apps that are data dense and make it easy for users to move between related records"; navigation through relationships "Automatic, provided relationships exist" vs canvas "Only where designed and applied using Power Fx formulas"; "without a data model housed within Microsoft Dataverse, you can't create a model-driven app" (B-01).
- **Decision impact:** STRONG signals: many related tables, record-centric work, back-office process users, audit/security granularity. Requires Dataverse (PS-02, PS-56, PS-42 premium).
- **Confidence:** HIGH.
- **Sources:** B-01 (2026-01-09).

#### AA-13 — UI customisation boundary: shell is platform-owned
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "with model-driven apps much of the user interface is determined for you and is largely designated by the components you add to the app"; "UI control: Limited, predominantly customization" (B-01). Within the boundary: forms/views/dashboards, business rules, JS form scripting, command bar, PCF (B-08, B-09).
- **Decision impact:** "The app must look like X" fails on core pages → custom page or canvas.
- **Confidence:** HIGH.
- **Sources:** B-01, B-08 (2026-05-19).

#### AA-14 — Theming boundary (modern era): colours, font, logo, header only, not everywhere; environment-scoped deployment
- **Classification:** CONSTRAINT + FACT
- **Origin:** MS (mechanism) + T3 (dates)
- **Evidence:** "classic theming isn't honored; however, makers can modify the colors"; "Modern themes currently support providing a custom theme for the entire app, overriding the app header colors, and setting a custom app logo. Other customizations … aren't available"; unthemed: "legacy grids, row summaries, focus view, and the sales pipeline" (B-05). `CustomTheme` XML web resource via environment setting (D-11). New look mandatory April 2026 (T3 message-center archive, D-19 — Tier 1 confirmation still open, U-B4).
- **Decision impact:** Branding beyond colour/font/logo → custom pages/PCF or off-platform. Estate: one palette feeding canvas theme YAML + MDA CustomTheme XML.
- **Confidence:** HIGH mechanism / MEDIUM dates.
- **Sources:** B-05/D-11 (2026-07-07), D-19.

#### AA-15 — Custom pages are the convergence vehicle; embedded canvas apps are legacy
- **Classification:** PATTERN + RECOMMENDATION
- **Origin:** MS
- **Evidence:** "brings the power of canvas apps into model-driven apps"; "In most cases, use custom pages instead of embedded canvas apps for tighter integration and better performance"; runtime/ALM/connectors/code components GA; "custom pages don't count toward the app limits"; licence follows the model-driven app (B-02).
- **Decision impact:** "Model-driven backbone + custom pages" is the Tier-1-endorsed alternative to a large standalone canvas app.
- **Confidence:** HIGH.
- **Sources:** B-02 (2026-03-13).

#### AA-16 — Custom pages: documented limitations (2026-08)
- **Classification:** CONSTRAINT + RISK
- **Origin:** MS
- **Evidence (B-03):** mobile "currently in public preview. Offline and device capability controls like barcode scanning, capturing photos from device, or attaching files isn't supported"; "aren't supported within App for Outlook"; "the model-driven app continues to use the last version of the custom page when the model-driven app was published"; 8-hour session timeout; "page state isn't restored" on back-navigation/multi-session tabs; third-party cookies required; connectors across pages "shouldn't exceed 10 … connection references … 20"; not all canvas controls available; user-locale formats unsupported. B-02: ≤ 25 pages/app; no conversion from standalone canvas apps.
- **Decision impact:** Not fit for offline, device-capability field UX, Outlook embedding, state-heavy flows, > 10-connector hubs.
- **Confidence:** HIGH.
- **Sources:** B-03 (2026-08-06), B-02.

#### AA-17 — Navigation is declarative (sitemap, role-filtered); role-based segmentation by app is the native persona mechanism
- **Classification:** FACT + PATTERN
- **Origin:** MS
- **Evidence:** "Each app that you create can have its own site map" (B-10). "Customize the navigation bar based on user roles. Users should see only the modules and features that are relevant to their roles"; forms associable to security roles (B-07). N apps over one Dataverse instance with own sitemaps and role-filtered forms/views/BPFs (B-07, B-10, B-14). No cap/optimal app count published (U-B2).
- **Decision impact:** Relational browsing and ≥ 2 personas favour model-driven; segmentation by app, not in-app conditionals (contrast AA-10).
- **Confidence:** HIGH mechanism / MEDIUM doctrine.
- **Sources:** B-10 (2026-02-12), B-07 (2024-06-03), B-14.

#### AA-18 — Deep linking is native and security-trimmed
- **Classification:** FACT + DECISION CRITERION
- **Origin:** MS
- **Evidence:** "URL addressable elements enable you to include links to model-driven apps, forms, views, and reports in other applications"; "can't bypass security"; `navbar` param "only supported in single-session model-driven apps" (B-06).
- **Decision impact:** "Deep link to a record from email/Teams" favours model-driven (AA-09). No iFrame embedding (PS-12).
- **Confidence:** HIGH.
- **Sources:** B-06 (2026-04-21).

#### AA-19 — Business process flows: guided stage rails with hard limits, no logic of their own
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** "up to 10 business process flow processes per table … up to 30 stages … up to five tables"; BPFs "don't provide any conditional business logic or automation beyond … controlling entry into stages" (B-04); stage-path branching exists (B-07; AA-C4). Offline only single-table BPFs; last-stage exit workflow never triggers (B-04).
- **Decision impact:** Multi-stage guided process within caps → model-driven pillar; heavy conditional wizards → custom page.
- **Confidence:** HIGH.
- **Sources:** B-04 (2026-08-15), B-07.

#### AA-20 — Form performance is design-governed; multisession in custom apps is unmanaged-solution-only with an indirect Dynamics 365 dependency
- **Classification:** RECOMMENDATION + RISK + CONSTRAINT
- **Origin:** MS
- **Evidence:** "the controls of the default tab are always rendered when opening a record"; quick views, subgrids, timeline "produce the most strain"; "greatly slow form loading"; "Field-level security does have an impact on your app's performance. Limit its use" (B-08, B-07). Multisession (fetched v2, V-08, 2025-10-16): prerequisite "Make sure that the system requirements for Copilot Service workspace are met"; **"You can enable the multisession experience in a model driven app within an unmanaged solution only"**; "This feature isn't supported in model driven apps installed by default, such as Sales Hub." Exact licence clause sits behind the linked system-requirements page (U-B1 narrowed: dependency is structural, wording indirect).
- **Why it matters:** Unmanaged-only conflicts with platform-suitability's enterprise doctrine "only managed solutions allowed in production" (PS-05) — a contact-centre multisession requirement on a custom app forces a governance exception.
- **Decision impact:** Data-dense fit assumes tabbed forms + subgrid discipline; multisession requirement → weigh Dynamics 365 Customer Service first-party app (rung 0) vs custom app with unmanaged exception.
- **Confidence:** HIGH.
- **Sources:** B-08, B-07, V-08.

### 3.3 Power Pages

#### AA-21 — Fit envelope: the Dataverse-fronted external channel, not a general web platform
- **Classification:** DECISION CRITERION
- **Origin:** MS + T3
- **Evidence:** "Access to Dataverse records is automatically restricted in Power Pages when using forms, lists, Liquid, the Portals Web API" (C-01). T3: choose Pages to avoid "the need to reimplement the security model from scratch" (C-10); negatives: "limited access to optimize server performance, caching, and load times" (C-11/C-12).
- **Decision impact:** Fit matrix row 4; driver question: data in Dataverse + portal-shaped interaction? No Tier 1 decision tree (U-C2).
- **Confidence:** HIGH drivers / MEDIUM boundary.
- **Sources:** C-01, C-10, C-11, C-12.

#### AA-22 — Authentication: Entra External ID is the viable CIAM for new sites; B2C closed to new customers (P2 discontinued March 2026); local auth "not recommended"
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** Provider table incl. "Local authentication (not recommended)" (C-02). B2C (fetched v2, V-06, 2025-06-20 upd. 2026-06-11): "Effective May 1, 2025 Azure AD B2C will no longer be available to purchase for new customers"; "We'll continue supporting Azure AD B2C until at least May 2030"; "Azure AD B2C P2 will be discontinued on March 15, 2026, for all customers". Entra External ID first-class setup (C-04). Local auth default `LocalLoginEnabled: True` (C-03).
- **Decision impact:** New external site → Entra External ID prerequisite (own tenant, cost, ops). AA-C5: Learn still recommends B2C on one page.
- **Confidence:** HIGH.
- **Sources:** C-02, C-03 (2026-02-28), C-04, V-06.

#### AA-23 — UX surface: Liquid + Bootstrap 5 design studio, or code-first SPA sites (product-documented 2026-07, no preview wording) with material trade-offs
- **Classification:** FACT + TRADE-OFF (re-based per review Finding 4)
- **Origin:** MS
- **Evidence:** "Power Pages supports Bootstrap version 3.3.6 and Bootstrap version 5" (C-05). SPA product doc (fetched v2, V-09, 2026-07-21): "An SPA site is a Power Pages site that runs entirely in the user's browser (client-side rendering) … you manage SPA sites only through source code and command-line interface (CLI) tools." Limitations: "Power Platform Git integration isn't supported for Single-Page Application (SPA) websites"; Pages/Style workspaces and Liquid not supported; "Single-language support"; no OOB lists/forms; no Power Fx; SEO "limited"; "SPA sites don't support the progressive web app (PWA) setting"; no built-in testing; site version 9.7.4.x+, PAC CLI 1.44.x+. No preview qualifier in body text; strict GA banner status UNKNOWN (fetcher may miss client-rendered banners, U-C6). Release plan states GA 2026-01-31 (C-06) — supporting, not primary. Licensing effects UNKNOWN (U-C1).
- **Why it matters:** Bespoke external UX is possible on-platform, but the SPA route surrenders exactly the things that make Pages cheap (OOB forms/lists, Liquid, multi-language, PWA, Git) — it is closer to "custom SPA hosted by Pages" than to "Power Pages with custom UI".
- **Decision impact:** External bespoke UX → SPA-on-Pages is CONDITIONAL on: single language acceptable, no PWA/offline-read need, pro-dev team, CLI-only ALM acceptable. Otherwise custom web app compares directly (AA-30). Classic Liquid sites remain the low-code path (multi-language, PWA).
- **Confidence:** HIGH facts / MEDIUM GA-strict and maturity.
- **Sources:** C-05, V-09, C-06, C-14.

#### AA-24 — Data access gated by table permissions + web roles; secure-by-default deny; Custom FetchXML access type in preview
- **Classification:** FACT / CONSTRAINT
- **Origin:** MS
- **Evidence:** "For a table permission to take effect, it has to be associated to one or more web roles"; access types Global/Contact/Account/Self/Parent/Custom (preview) (C-01).
- **Decision impact:** Row-level security as configuration — core Pages advantage and the misconfiguration surface of AA-25.
- **Confidence:** HIGH.
- **Sources:** C-01 (2026-02-28).

#### AA-25 — RISK: table-permission misconfiguration exposed millions of records (AppOmni 2024); Microsoft-side controls now documented: anonymous-access indicator, daily security checks, deep scan; open registration ON by default
- **Classification:** RISK (Microsoft side added per review Finding 12)
- **Origin:** T3 (incident) + MS (controls, defaults)
- **Evidence:** AppOmni: "several million records" exposed; NHS supplier "over 1.1 million NHS employees'" PII; causes: Web API field wildcards, excessive Anonymous/Authenticated role permissions, Global access, no column security (C-07; C-15, C-16). Microsoft (fetched v2, V-10, 2025-03-12 upd. 2026-08-31): "Anonymous access to Dataverse tables shows the number of websites where anonymous access is allowed … at least one table permission that allows anonymous users to access the data"; "Security checks are run against all websites in your tenant, once every day automatically"; Deep scan "detecting and addressing vulnerabilities"; site health statuses Standard/Enhanced/Advanced. Table-permission doc snippet: "If you add the Anonymous users web role to a table permission, the data in the table is visible to anyone" (search-verified). Default `OpenRegistrationEnabled: True` (C-03). Web API wildcard verbatim still not fetched (U-C7).
- **Decision impact:** Acceptance conditions for anonymous/external designs: column security on PII tables; no Global read for Anonymous/Authenticated roles on sensitive tables; explicit Web API field allow-lists; open registration disabled unless required; PPAC security checks at "Advanced" in run-book.
- **Confidence:** HIGH.
- **Sources:** C-07 (2024-11-14), C-15, C-16, V-10, C-03.

#### AA-26 — Licensing shape: per unique user/site/month; tiered; cookie-based anonymous counting; bots excluded; internal users covered by Power Apps licences
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence (C-00, 2026-08-14):** authenticated packs of 100: $200 → $75 (≥ 100 packs) → $50 (≥ 1,000); anonymous packs of 500: $75 → $37.50 → $25; minimums 25 authenticated / 200 anonymous per environment; no carry-forward; anonymous uniqueness by browser cookie; "Bots and crawler accessing anonymous pages of the website isn't counted"; internal Power Apps/D365-licensed users "won't be counted"; storage accrual per pack.
- **Decision impact:** Cost scales with audience uniqueness, not intensity; consumer-scale anonymous → model Tier-2/3 + PAYG (PS-36).
- **Confidence:** HIGH.
- **Sources:** C-00.

#### AA-27 — Server-side cache: 15-minute SLA; plugin/flow writes "never guaranteed to be immediate"
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "service level agreement of 15 minutes"; instant invalidation only for changes made through the website; "data reflection from Dataverse to websites is never guaranteed to be immediate … This design approach isn't recommended"; manual clear "can lead to users facing performance issues" (C-08).
- **Decision impact:** Real-time status fed by background automation → CONDITIONAL/POOR or redesign.
- **Confidence:** HIGH.
- **Sources:** C-08 (2026-04-29).

#### AA-28 — CDN + WAF included; caching for anonymous users only; throughput ceilings unpublished (U-4 still open)
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS
- **Evidence:** "CDN caching is available only for anonymous users"; authenticated pages "aren't available for caching" (C-09). "Both CDN and WAF capabilities are included as part of Power Pages licensing" (C-00). Limits page has no traffic/RPS/concurrency numbers (C-17).
- **Decision impact:** Authenticated high-concurrency hits the app server with unquantified ceilings → load-test; keep custom-app counterfactual.
- **Confidence:** HIGH.
- **Sources:** C-09 (2026-06-18), C-00, C-17.

#### AA-29 — ALM: enhanced data model makes sites solution-aware with drift traps; server logic is the sanctioned Azure hybrid
- **Classification:** FACT + TRADE-OFF + PATTERN
- **Origin:** MS
- **Evidence:** "New website components aren't automatically added to the solution"; target-env edits create "an unmanaged solution layer" (C-18, C-19). Server logic: "run JavaScript securely on the server … protected by web roles and table permissions"; "Integrate securely with REST APIs, Azure Functions"; ECMAScript 2023, no fetch/XHR/DOM, 120 s default / 240 s max; tenant admins can "block outbound HTTP calls"; `ServerLogic/AllowedDomains` (C-20, C-21). SPA sites: no Git integration (V-09).
- **Decision impact:** Payment/integration/complex validation no longer auto-disqualify Pages; verify tenant posture and GA per region (U-C3).
- **Confidence:** HIGH mechanics / MEDIUM maturity.
- **Sources:** C-18 (2026-01-29), C-19, C-20 (2026-05-13), C-21, V-09.

#### AA-30 — When a custom web app wins over Power Pages
- **Classification:** DECISION CRITERION
- **Origin:** T3 + INF (no Tier 1 decision guidance, U-C2)
- **Evidence:** Custom over Dataverse must re-implement "Table Permissions, Web Roles … from scratch" but gains full control; custom faces per-tenant service-protection limits directly (C-10); custom wins on sign-in flows, downloads, payments, server/caching control (C-11, C-12). SPA-on-Pages trade-offs (AA-23) narrow the gap for bespoke UX but not for server control, throughput guarantees or multi-language SPA.
- **Decision impact:** Custom preferable when: data permanently outside Dataverse; guaranteed throughput/SLA; product-grade consumer UX beyond SPA-on-Pages constraints; third-party API surface (PS-36); massive anonymous scale where per-user licensing loses. Pages preferable when Dataverse is the record system and row security + included WAF/CDN/auth outweigh control.
- **Confidence:** MEDIUM.
- **Sources:** C-10, C-11, C-12, V-09; PS-36, PS-56.

### 3.4 Componentisation, reuse, code apps

#### AA-31 — Canvas components: reuse blocks excluded from galleries and forms; no data-bound encapsulation
- **Classification:** CONSTRAINT
- **Origin:** MS
- **Evidence:** "You can't insert a component into a gallery or a form (including SharePoint form)"; "You can't save data sources or controls that include data from those data sources … with components"; no `UpdateContext`; no flows in libraries (D-01, D-02).
- **Decision impact:** Repeated row/form UI → PCF or design avoidance.
- **Confidence:** HIGH.
- **Sources:** D-01 (2026-01-13), D-02 (2026-08-20).

#### AA-32 — Component libraries are THE recommended reuse mechanism; updates are pull-based; no npm-style dependency management
- **Classification:** RECOMMENDATION + CONSTRAINT
- **Origin:** MS
- **Evidence:** "Component libraries are the recommended way to reuse components across apps" (D-02); app-to-app import retired (D-01). Definitions "copied into the definition of the canvas app … 'self-contained'"; updates notified "when makers edit the apps in canvas app studio"; "Only published component library updates are available"; ≤ 5-minute propagation; "Limit the number of components in a library to 20"; export "always exports the latest version" (D-02, D-03).
- **Decision impact:** One shared fix = N edit/publish cycles; pipelines must sync library/app versions.
- **Confidence:** HIGH.
- **Sources:** D-01, D-02, D-03 (2022-06-10).

#### AA-33 — "Allow customization" forks permanently
- **Classification:** TRADE-OFF / RISK
- **Origin:** MS
- **Evidence:** "The association with the component library is removed once you edit the component"; local copies "don't receive updates" (D-02); unmanaged layers block updates (D-03). Well-Architected: variations "through parameters … without the need for modifications" (D-13).
- **Decision impact:** Lock components or accept drift; parameter-driven APIs as mitigation (enhanced component properties status U-D4).
- **Confidence:** HIGH.
- **Sources:** D-02, D-03, D-13.

#### AA-34 — PCF: pixel-level extensibility with documented limits; premium is CONDITIONAL on non-connector external calls; pro-dev ownership cost
- **Classification:** CONSTRAINT + FACT + TRADE-OFF
- **Origin:** MS
- **Evidence:** "Microsoft Dataverse dependent APIs, including WebAPI, are not available for Power Apps canvas applications yet"; no `localStorage`; "Custom auth in code components is not supported"; not on-premises (D-04). Licensing: "Code components that connect to external services or data directly through the user's browser client and not through connectors are premium … Code components that don't connect to external services or data … the app remains standard" (D-05, 2026-01-09). Manifest version bumps required; "Code components from an untrusted source can potentially access security tokens and data" (D-06); virtual React controls pin platform React/Fluent versions; no Pages support for platform libraries (D-07). Creator Kit "sample implementations" support (D-14); CoE kit "no longer actively maintained" (D-12).
- **Decision impact:** Visual PCF does not make a standard-connector app premium (AA-C3, softens PS-10 cost leg). PCF-in-canvas is UI extensibility only; custom data/auth patterns → code apps or custom. Requires long-term pro-dev ownership.
- **Confidence:** HIGH.
- **Sources:** D-04 (2025-07-01), D-05, D-06 (2026-08-20), D-07, D-12, D-14.

#### AA-35 — Code apps: GA wording, B2B guests now supported at canvas parity, pipelines ALM; public asset endpoint and no Git integration persist (updates PS-03)
- **Classification:** FACT + CONSTRAINT
- **Origin:** MS (+ T2 GA blog)
- **Evidence:** GA blog 2026-02-05 (D-20). Overview (fetched v2, V-18, 2026-08-12 upd. 2026-08-19): no preview wording; "End users that run code apps need a Power Apps Premium license"; governance table: **"Azure B2B (external user access) | End-users can share code apps and access them by using Azure B2B to access resources in a tenant, similar to canvas apps"** (CHANGED vs earlier preview docs); "compiled app assets are served from a publicly accessible endpoint that doesn't support IP-based restrictions today. To restrict access by IP, use Conditional Access"; "Don't store sensitive user or organizational data in the app"; no Windows player; no PowerBIIntegration (but embeddable via Power Apps visual); no SharePoint forms. ALM: `pa app push` into a solution; pipelines Dev→Test→Prod; "Don't support source code integration" (D-22). Mobile-player support and offline undocumented (U-D2, U-D3). Licensing Guide treatment of code apps not checked (deferred, §9).
- **Decision impact:** Code apps are a supported rung for internal AND B2B bespoke SPA UX; POOR for IP-allowlist estates, Windows-player audiences, offline, anonymous.
- **Confidence:** HIGH.
- **Sources:** V-18, D-20 (T2), D-22 (2026-08-27), D-23.

#### AA-36 — Decision ladder with rung 0: buy/first-party → plain canvas → components/libraries → PCF → code apps → custom web
- **Classification:** DECISION CRITERION (synthesis; each rung Tier 1-anchored)
- **Origin:** MS per rung + INF framing

| Rung | Choose when | Cost of the step | Anchors |
|---|---|---|---|
| 0. Configure / buy / first-party | An existing Dynamics 365 app, M365 feature or ISV product covers the requirement (e.g. multisession contact centre → Customer Service) | Licence for the first-party app; feature fit gaps; "do not replicate the legacy solution" | PS-41, PS-44, AA-20 |
| 1. Plain canvas + modern controls/themes | Fluent-consistent, brand-tinted look suffices | none | D-08, D-10 |
| 2. Canvas components + library | Repeated composite UI across screens/apps | pull-based update labour; no gallery/form insertion; fork risk | AA-31..33 |
| 3. PCF | Pixel-level control; gallery-internal UI; behaviour canvas can't express | pro-dev toolchain, security review, versioning; premium only if non-connector external calls | AA-34 |
| 4. Code apps | Full SPA control with platform auth/connectors/governance; internal or B2B | Premium per user; public asset endpoint; no Windows player; own frontend engineering | AA-35 |
| 5. Custom web app | IP-restricted hosting, offline, anonymous users, freedom from per-user premium, server control | lose connectors + managed governance; build auth/DLP equivalents | AA-30, AA-35 inverse |

- **Confidence:** HIGH per-rung facts / MEDIUM framing.

#### AA-37 — Estate-level reuse: Well-Architected prescribes a design system; Microsoft admits coherence is hard; accelerators carry support risk
- **Classification:** RECOMMENDATION + RISK
- **Origin:** MS
- **Evidence:** XO:02: design tokens, components, pattern libraries, guidelines; "Use these controls as much as possible for basic needs, then consider building composite components where gaps exist"; "coherence is a challenge because components, systems, processes, and culture are often not shared" (D-13). Canvas themes shared by YAML copy-paste (D-10). Creator Kit sample-status (D-14); CoE theming kit unmaintained (D-12).
- **Decision impact:** Design-token governance is organisational, not platform-enforced.
- **Confidence:** HIGH.
- **Sources:** D-13 (2025-08-05), D-10 (2026-01-21), D-12, D-14.

### 3.5 Mobile, Wrap, Intune

#### AA-38 — Wrap: branded native iOS/Android from CANVAS apps only; Azure + signing footprint; GA confirmed by official blog (date unverified)
- **Classification:** FACT + CONSTRAINT (resolves R-14 part 1)
- **Origin:** MS (T2 for GA)
- **Evidence:** "package your canvas app as a custom-branded Android or iOS app"; "only supports canvas apps (not model-driven apps)"; solution + same environment; `Launch()` between bundled apps (E-01). "Azure subscription (for Azure Key Vault and Blob Storage)" (paid); code signing; "Signing your mobile app with Xcode isn't supported in wrap" (E-01, E-02). GA: official blog "Announcing general availability of wrap for Power Apps" exists (V-17); announcement date not verified (U-E5). v1's "GA from absence of preview banners" corrected to a T2 statement.
- **Decision impact:** Branded app + relational back-office UX = tension (canvas or drop branding). No Azure/Apple Business Manager access → cannot Wrap.
- **Confidence:** HIGH facts / MEDIUM GA date.
- **Sources:** E-01 (2025-02-04), E-02 (2026-06-12), V-17 (T2).

#### AA-39 — Wrap hard limitations; monthly rewrap; licence per end user
- **Classification:** CONSTRAINT + TRADE-OFF
- **Origin:** MS
- **Evidence:** "Push notifications aren't supported"; no visible sign-out; APK ≤ 100 MB / AAB ≤ 150 MB; "Wrap doesn't support sovereign cloud environments"; offline "only show image thumbnails" (E-03). "Can I create B2C mobile apps with Power Apps? No."; no CMK/Lockbox — "customer assets might be exposed to Microsoft service operators during the build process"; "rewrap and redistribute your mobile app at least monthly"; "you don't need a premium license for wrap. However, if your APK uses certain connectors…"; "Users must have a Power Apps license to use wrapped apps" (E-02, E-01).
- **Confidence:** HIGH.
- **Sources:** E-02, E-03.

#### AA-40 — Wrap verdict (binary-testable)
- **Classification:** DECISION CRITERION (resolves R-14)
- **Origin:** MS
- **Wrap suffices when ALL hold:** internal or B2B-guest audience with Power Apps licences; canvas app(s); branding = icon/splash/welcome/colours; Intune/store/ABM distribution; no push; commercial cloud; offline via canvas offline-first; monthly rewrap owned. Conditional Access "Require approved client app" blocks wrapped apps ("You can't get there from here") → policy exclusion; wizard auto-configures Intune MAM API permission (E-02).
- **Custom native (or Pages PWA if no offline write) when ANY holds:** consumer/B2C or anonymous; push; native UX beyond canvas; sovereign cloud; CMK/Lockbox; per-user licensing uneconomic; > 150 MB.
- **Confidence:** HIGH.
- **Sources:** E-01, E-02, E-03.

#### AA-41 — Intune/MAM: Power Apps Mobile is a managed app; advanced Intune app settings unsupported; not a canvas-vs-model-driven differentiator
- **Classification:** FACT + CONSTRAINT (resolves R-14 part 2)
- **Origin:** MS
- **Evidence:** Intune can "publish, push, configure, secure, monitor, and update" Power Apps mobile; "restricting data leakage through cut, copy, paste, and save-as. Provide encryption at rest"; "Intune advanced app settings aren't currently supported with Power Apps Mobile"; "Intune is a separate Microsoft product that is not included with Power Apps mobile" (E-09). Out of scope for Multiple Managed Accounts (E-15, search-verified).
- **Decision impact:** BYOD coverable via MAM on the shared player; differentiators are vs Wrap and vs browser (MAM doesn't apply; Conditional Access session controls do — and model-driven has no phone-browser fallback, AA-45).
- **Confidence:** HIGH.
- **Sources:** E-09 (2024-10, upd. 2025-05), E-15.

### 3.6 Offline

#### AA-42 — Canvas offline-first (2026-06 page): Dataverse-only, standalone-only; flows, virtual/elastic tables, non-Dataverse connectors excluded; foreground-only sync
- **Classification:** CONSTRAINT (re-verifies PS-35)
- **Origin:** MS
- **Evidence (E-05, 2026-06-17):** "works for standalone canvas apps only. It doesn't work for embedded canvas apps, custom pages, or canvas apps in Teams"; "Non-Dataverse connectors, like SharePoint, aren't supported"; "Virtual tables and elastic tables aren't supported"; "Power Automate flows aren't supported in offline mode"; 3,000,000-record cap; no M:N, one-level lookups, ≤ 15 relationships/table, ≤ 14 image columns; "Data can only be synced regularly when Power Apps is running in the foreground of your device, with the screen unlocked." LoadData/SaveData "30-70 MB", manual conflicts (E-04).
- **Decision impact:** Offline + SharePoint = forced Dataverse migration; offline + automation = redesign; data-model rework for M:N/deep lookups.
- **Confidence:** HIGH.
- **Sources:** E-05, E-04 (2024-06-05), E-16.

#### AA-43 — Model-driven offline: field-level security, personal views, Dataverse search, iOS form web resources degrade offline
- **Classification:** CONSTRAINT (re-verifies PS-35)
- **Origin:** MS
- **Evidence (E-06, 2024-09-26 upd. 2025-03):** "Field level security and field sharing aren't supported in Mobile offline mode"; personal views unsupported; form web resources "Not supported" on iOS; "Dataverse search isn't supported in offline mode"; grid column filtering disabled when a profile exists "even when there's network connectivity"; duplicate detection unsupported; custom pages no offline.
- **Decision impact:** Offline + FLS = design conflict → data segregation; iPad workforce + script-driven forms = critical gap.
- **Confidence:** HIGH.
- **Sources:** E-06, E-17.

#### AA-44 — Offline decision table
- **Classification:** DECISION CRITERION
- **Origin:** MS cells / INF for the custom-sync row
- **Evidence:** AA-42/43 plus Pages PWA (fetched v2, V-03/V-04): "enable specific pages in your site to be available offline (the content on these pages is read-only)"; "pages that are connected to Microsoft Dataverse that contain forms to fill out or run queries won't work while offline"; PWAs "distributed through app stores for Android, iOS, and Windows". SPA sites don't support the PWA setting (V-09).

| Offline requirement | Forced architecture | Origin |
|---|---|---|
| Field worker, Dataverse, ≤ 3M rows, standard conflicts | Canvas offline-first OR model-driven offline (native player) | MS |
| Offline + heavy custom UX | Canvas offline-first (standalone) | MS |
| Offline + complex relational forms | Model-driven offline (AA-43 gaps) | MS |
| Small cache, non-Dataverse source | LoadData/SaveData (30–70 MB, manual conflicts) — fragile | MS |
| Offline in Teams / embedded canvas / custom pages | Unsupported | MS |
| Offline in a desktop browser | Exceeds Power Platform (PS-35) | MS |
| Offline write on a public site | Exceeds Power Platform (Pages PWA read-only; SPA no PWA) | MS |
| Custom conflict rules, background/locked-screen sync, multi-day queues | Not documented as extensible → treat as custom mobile development until verified | INF |
| Offline + field-level security | Unsupported combination | MS |
| Offline + Power Automate logic | Unsupported | MS |

- **Confidence:** HIGH documented cells / MEDIUM INF row.
- **Sources:** E-04, E-05, E-06, V-03, V-04, V-09.

### 3.7 Devices, notifications, identity, performance, lifecycle

#### AA-45 — Device hardware pins architecture to native mobile players; model-driven in a phone browser is unsupported; Windows player materially weaker
- **Classification:** CONSTRAINT (PS-02 condition restored per review Finding 8)
- **Origin:** MS
- **Evidence (fetched v2):** "ReadNFC is only supported when running the app on a native mobile app, such as the iOS and Android apps … can't be used in Power Apps Studio or in a web browser" (V-01, 2024-03-22 upd. 2025-10). "When using desktop browsers, the barcode reader isn't supported. Use the Power Apps for mobile app"; camera "not supported within the browser or Teams Mobile" (iOS); "the barcode reader control isn't supported in Teams Mobile"; Teams-embedded unsupported: Address Input, Camera (Teams Mobile), Map, Mixed reality, Power BI tile, Web barcode scanner (V-02, 2022-06 upd. 2025-05). **"Using the web browser on a phone to run a model-driven app isn't supported; use the Power Apps mobile app"** (V-19, 2026-01-12). Windows player: no sensors, mixed reality, NFC (E-11); no retirement listed (E-10) — AA-C6.
- **Decision impact:** Scan/NFC/GPS → iOS/Android native player (or Wrap); browser-first mobile BYOD × model-driven = collision (native player + MAM instead); Windows handheld scanning RISKY. Kiosk/shared-device mode: UNKNOWN (U-E2).
- **Confidence:** HIGH.
- **Sources:** V-01, V-02, V-19, E-10, E-11.

#### AA-46 — Push notifications: only via Microsoft's own players; none in Wrap; throttles undocumented
- **Classification:** CONSTRAINT + UNKNOWN
- **Origin:** MS / UNKNOWN
- **Evidence:** Notification V2 connector targets "canvas Power Apps, model-driven Power Apps, Field Service, and Sales"; recipient must have the mobile app installed and signed in (E-08); Wrap: "Push notifications aren't supported" (E-03). No throttling limits documented (U-E1).
- **Decision impact:** {branded app, push} unsatisfiable (AA-40); high-volume push → pilot-validate.
- **Confidence:** HIGH capabilities / UNKNOWN throttles.
- **Sources:** E-08, E-03.

#### AA-47 — Accessibility by app type: Pages platform-attested (WCAG 2.2 / Section 508 / EN 301 549); model-driven built-in; canvas maker-dependent with documented impossible patterns
- **Classification:** DECISION CRITERION (extends PS-11)
- **Origin:** MS
- **Evidence:** Pages "conforms to the WCAG 2.2 accessibility standard … Section 508 … ETSI EN 301 549"; "When you customize your Power Pages site, you're responsible for meeting accessibility standards" (E-07). Model-driven built-in; web resources are developer responsibility (E-21, E-22 search-verified). Canvas limitations (E-20, 2021-02): "Dialogs and user interfaces that appear on top of other content are not supported"; "It is not possible to react to specific key presses"; escape hatch "Create a code component". Canvas guidance re-verified (E-19, upd. 2025-05). 2021 page may overstate gaps vs modern controls (AA-C7). No per-app-type ACR (U-E3).
- **Decision impact:** Legal mandate → prefer model-driven or Pages; canvas only with a11y-skilled makers + PCF budget + audit.
- **Confidence:** HIGH.
- **Sources:** E-07 (2025-04-22), E-19, E-20, E-21, E-22.

#### AA-48 — Localisation by app type: canvas manual; model-driven built-in; Pages Liquid 43 languages, Pages SPA single-language; RTL fully supported on custom pages, undocumented for standalone canvas
- **Classification:** DECISION CRITERION (resolves R-13 localisation; RTL re-based per review Finding 14)
- **Origin:** MS + UNKNOWN (canvas RTL)
- **Evidence:** Canvas: translation-table + `LookUp` on `Language()` pattern (E-23, 2021-01); locale formatting built in (E-24). Model-driven: "Dataverse enables you to install multiple language packs"; export→Excel→import (E-26, search-verified). Pages Liquid: 43 OOB languages + custom (E-25); Pages SPA: "Single-language support" (V-09). RTL (fetched v2, V-05, 2022-05 upd. 2025-05, page still marked pre-release): "Right-To-Left (RTL) is fully supported for languages like Arabic and Hebrew and the page will change at runtime automatically"; exception "icons, shapes, and images". **The v1 clause "RTL not available in standalone canvas apps" was NOT found on the page**; a targeted search found no Learn statement on RTL for standalone canvas apps either way.
- **Decision impact:** > 2–3 languages → model-driven or Pages Liquid; canvas cost = screens × languages; SPA-on-Pages excluded for multi-language. RTL → custom pages documented; standalone canvas **UNKNOWN — treat as unsupported until verified by prototype**, not as a documented POOR.
- **Confidence:** HIGH mechanisms / UNKNOWN canvas RTL.
- **Sources:** E-23, E-24, E-25 (2025-08-06), E-26, V-05, V-09.

#### AA-49 — Device/UX selection matrix (synthesis)
- **Classification:** DECISION CRITERION / PATTERN
- **Origin:** inherits anchors

| Requirement | Selected architecture | Anchor |
|---|---|---|
| Field worker, offline, hardware | Canvas or model-driven + Dataverse offline, native player | AA-42..45 |
| NFC | Canvas on iOS/Android native player only | AA-45 |
| Browser-first mobile BYOD | Canvas in browser (no hardware) or native player + MAM; model-driven requires native player | AA-45, AA-41 |
| Branded internal/B2B mobile | Wrap (AA-40 conditions) | AA-38..40 |
| Branded app + push, or B2C | Custom native; no-offline-write variant: Pages PWA (Liquid site) | AA-39, AA-46, AA-44 |
| External authenticated, browser-first | Power Pages | AA-21..24 |
| Public-sector accessibility mandate | Model-driven or Pages; canvas with discipline + PCF | AA-47 |
| > 2–3 languages | Model-driven / Pages Liquid; avoid canvas and Pages SPA | AA-48 |
| RTL | Custom pages documented; standalone canvas UNKNOWN | AA-48 |
| Desktop-browser offline / offline in Teams | Exceeds Power Platform | AA-44 |
| Kiosk / shared-device | UNKNOWN (U-E2) | — |

#### AA-50 — Teams-hosted apps (Dataverse for Teams) as an application surface: bounded fit with a one-way upgrade path; Teams embedding limits device features
- **Classification:** DECISION CRITERION + CONSTRAINT (new; refines PS row 3 / PS-16)
- **Origin:** MS
- **Evidence (fetched v2):** "Maximum size | 1 million rows or 2 GB"; "The 2 GB storage limit can't be extended further"; feature table: PCF **No**, model-driven apps **No**, mobile offline **No**, API access **No**, plug-ins **No** (V-11, 2025-05-28). Upgrade: "Unlocks all the functionality of Dataverse services for the environment"; "For any standalone Power Apps or Power Automate usage, which also includes Dataverse API access, the Dataverse for Teams environment needs to upgrade to Dataverse"; post-upgrade "Any apps running on the environment require Microsoft Power Platform (Power Apps, Power Automate) licenses to be accessed"; capacity counts against tenant pool; no downgrade path documented (V-12, 2026-05-15). Teams tab embedding of standard canvas apps (V-16, 2020-09 upd. 2024-01): "You must share your own apps before you add them to Teams"; "Not all sensors, such as Acceleration, Compass, and Location, are supported"; https-only content; Teams mobile "End users can't download attachments from canvas apps". Component libraries in Teams studio: compare page silent; studio doc suggests reuse of published libraries (search-verified) — U-T1.
- **Why it matters:** For a team-scoped internal app this is the cheapest correct answer (seeded licences) and was absent from v1. The exit cost is explicit: crossing 2 GB or needing any excluded feature converts every user to a premium licence in one step.
- **Decision impact:** Fit matrix row 6. Signals for Teams-hosted: team audience, collaboration context, seeded licences, no PCF/offline/API/model-driven; anti-signal: expected growth toward the caps (plan the upgrade cost up front). Teams tab for standard apps: fine for desktop task apps; not for sensor/attachment-heavy mobile use.
- **Confidence:** HIGH.
- **Sources:** V-11, V-12, V-16, PS-16.

#### AA-51 — Embedded canvas surfaces: Power BI visual and SharePoint customized forms have their own fit boundaries
- **Classification:** DECISION CRITERION + CONSTRAINT (new; review Finding 6)
- **Origin:** MS (+ INF for "when standalone")
- **Evidence (fetched v2):** Power BI visual (V-13, 2025-03-04): "The maximum number of records that can be passed from Power BI to Power Apps visual using 'PowerBIIntegration' object is limited to 1000"; "Power Apps visual is only supported for Embed for your organization. Embed for your customers is not supported"; "The Power Apps visual can't filter the data or send any data back to the report"; write-back "Changes are reflected on the next scheduled refresh"; "You'll need to share the app separately from your report"; "Power BI Report Server doesn't support the Power Apps visual"; Safari view-only, Firefox unsupported. SharePoint customized forms (V-14, 2025-11-14; V-15, 2026-01-13): "You can't manually share a SharePoint form customized with Power Apps. Instead, any user who has at least Read or Restricted View access to the linked SharePoint list inherits access to the form"; "there's currently no automated method in Power Apps to copy a form from one environment to another"; generic lists/libraries only, document libraries metadata-only. Licensing statement for customized forms not on fetched pages (U-S1); no Microsoft "when to go standalone" statement (INF below).
- **Decision impact:** Power BI visual: STRONG for internal drill-through/write-back on ≤ 1,000 selected rows with refresh-latency tolerance; POOR for external report consumers, Report Server, immediate reflection. SharePoint form: STRONG for a form over one list where readers = list readers and no cross-environment ALM is needed; INF: portability, solution management, multi-list or multi-source logic, or offline → standalone canvas app.
- **Confidence:** HIGH facts / MEDIUM "when standalone" (INF).
- **Sources:** V-13, V-14, V-15.

#### AA-52 — Identity per app type: Entra work/school for internal app types; B2B guests for canvas AND code apps (licence recognition caveat); external identities only via Power Pages
- **Classification:** DECISION CRITERION (new consolidation; review Finding 9)
- **Origin:** MS
- **Evidence:** Internal app types require Entra work/school accounts; personal Microsoft accounts removed (PS-60). B2B guests: canvas apps with cross-tenant-recognised licences — "Power Apps per app plans … can't be recognized across tenants"; guests need "a standalone browser session" (PS-36/S-42b). Code apps: "End-users can share code apps and access them by using Azure B2B … similar to canvas apps" (V-18, CHANGED from preview). Wrap supports B2B guests with explicit tenant setup (E-02, E-03). Model-driven: same Entra/B2B model via Dataverse security roles (PS-31). Consumer/anonymous/social/external-IdP identities: Power Pages only (Entra External ID, OIDC/SAML providers, local auth not recommended; AA-22). Frontline/shared-device identity: UNKNOWN (U-14).
- **Decision impact:** Audience tiers → architecture: employees (any internal app type) · known partners (B2B guests → canvas/model-driven/code apps/Wrap, CONDITIONAL on licence recognition — per-app plans fail) · authenticated customers (Pages) · anonymous public (Pages with AA-25 conditions, or custom).
- **Confidence:** HIGH.
- **Sources:** PS-60, PS-36, PS-31, V-18, E-02, E-03, AA-22.

#### AA-53 — Application-level performance and concurrency: no documented concurrent-user ceiling for any app type; capacity is governed by data-source and request limits; documented performance guidance is design-level
- **Classification:** CONSTRAINT + UNKNOWN (new; review Finding 10)
- **Origin:** MS + UNKNOWN
- **Evidence:** No concurrent-user ceiling for canvas or model-driven; capacity governed by data-source and request limits (PS-20, S-01/S-11); service-protection limits are per user per 5 minutes and "interactive users rarely hit them" (PS-18); Pages limits page silent on RPS/concurrency (C-17, U-4). Design-level guidance: canvas — reduce data calls, delegation, avoid OnStart/collections (A-07, A-11, PS §11 S-11 performance considerations); model-driven — default-tab rendering, subgrid/quick-view strain, FLS cost (B-08, B-07); Pages — cache and CDN only for anonymous (AA-27, AA-28). Load benchmarks: none published (U-2, PS R-24 deferred to Area 09).
- **Why it matters:** "How many users can this app type take" has no documented answer; the honest position is "not the app type's ceiling — test the data path".
- **Decision impact:** Concurrency requirements do not differentiate canvas vs model-driven vs Pages by documentation; they differentiate by data path (Dataverse direct vs connectors vs Pages cache). Any large-audience design → load test; keep PS-18/PS-19 request budgets in the estimate.
- **Confidence:** HIGH that nothing is documented / UNKNOWN actual limits.
- **Sources:** PS-18, PS-20, A-07, A-11, B-07, B-08, C-17.

#### AA-54 — Lifecycle exposure per app type: model-driven absorbs vendor UI change most directly; canvas medium; code apps lowest UI exposure but full own-maintenance
- **Classification:** TRADE-OFF (new; review Finding 13)
- **Origin:** MS (facts) + INF (ranking)
- **Evidence:** Mandatory semi-annual release waves and rolling deprecations (PS-50). Model-driven: new theming system where "classic theming isn't honored" (B-05); new look mandatory (T3 D-19, Tier 1 date open U-B4); multisession only in unmanaged solutions (V-08). Canvas: modern-control property renames Feb 2026 (AA-11); `Navigate` in OnStart retired, mobile deep links break May 2026 (A-04, A-14); Test Engine deprecated (V-07); co-authoring removed (A-06). Custom pages: double-publish coupling (B-03). Code apps: own framework upgrades; platform imposes only host/SDK changes; no Git integration (V-18, D-22). Pages: SPA no Git; enhanced data model migration; B2C sunset (V-06). ALM friction ranking from B-01: model-driven "Simple" migration vs canvas "Potentially complex".
- **Decision impact:** Long-lifetime + low tolerance to unrequested UI change → weigh model-driven's wave exposure against its ALM simplicity; code apps trade wave exposure for owning the frontend stack. Every option requires a change-absorption owner (PS-50, AP-16).
- **Confidence:** HIGH facts / MEDIUM ranking.
- **Sources:** PS-50, B-01, B-03, B-05, V-06, V-07, V-08, V-18, A-04, A-06, A-14, D-19, D-22.

---

## 4. Anti-patterns (application-architecture specific)

Extends `platform-suitability.md §5` (AP-1..AP-16).

| Id | Anti-pattern | Why it fails | Origin | Findings |
|---|---|---|---|---|
| AP-17 | God canvas app: many personas/experiences in one artefact | Formula sprawl, one-maker bottleneck, Studio degradation | MS | AA-03, AA-04, AA-06, AA-10 |
| AP-18 | Everything in OnStart; `Navigate` in OnStart | Deprecated architecture; retired function | MS | AA-05 |
| AP-19 | Collect-everything workarounds for delegation | Microsoft-named anti-pattern trio; N+1 storms | MS | AA-07, PS-13 |
| AP-20 | Copy-paste component reuse / app-to-app import | Retired; invisible formula duplication | MS | AA-32, AA-04 |
| AP-21 | Editing library components in consuming apps | Permanent fork; unmanaged layers block updates | MS | AA-33 |
| AP-22 | PCF-for-everything before platform controls | Inverts Well-Architected ordering; maintenance burden | MS | AA-34, AA-37 |
| AP-23 | Unreviewed third-party PCF | "can potentially access security tokens and data" | MS | AA-34 |
| AP-24 | Model-driven for mobile-first field capture via custom pages | Device controls unsupported in custom pages; offline gaps | MS | AA-16, AA-43 |
| AP-25 | Bespoke branding pursued inside model-driven core pages | Theming = colours/font/logo only | MS | AA-14 |
| AP-26 | Pages: anonymous/generic-authenticated roles with broad table permissions and Web API wildcards; open registration left ON | Documented mass-exposure incident class; "visible to anyone" | T3 + MS | AA-25 |
| AP-27 | Pages fed by background automation presented as real-time | Cache; freshness "never guaranteed to be immediate" | MS | AA-27 |
| AP-28 | Wrap for consumer/B2C or push-dependent apps | B2C unsupported; push unsupported | MS | AA-39, AA-40 |
| AP-29 | Role-based UI via Visible formulas treated as security | Access governed by connection identity/source security (PS-31), not UI | MS partial + INF | AA-10 |
| AP-30 | Stretching BPF into a conditional wizard engine | No business logic; stage/table caps | MS | AA-19 |
| AP-31 | Model-driven app served to phone users via browser | Unsupported; native player required | MS | AA-45 |
| AP-32 | Growing a Dataverse for Teams app toward the 2 GB / feature caps without budgeting the one-way upgrade | Upgrade converts all users to premium licences; no downgrade | MS | AA-50 |
| AP-33 | SPA-on-Pages chosen for a multi-language or PWA/offline-read requirement | SPA sites single-language, no PWA setting | MS | AA-23 |
| AP-34 | SharePoint customized form treated as a portable, solution-managed app | No manual sharing, no automated cross-environment copy | MS | AA-51 |
| AP-35 | Building a custom multisession app when the requirement matches a first-party app | Unmanaged-solution-only; governance exception vs configure/buy | MS | AA-20, AA-36 |

---

## 5. Conflicts (CONFLICTED)

| Id | Topic | Source A | Source B | Assessment |
|---|---|---|---|---|
| AA-C1 | Canvas scale ceiling | T1 vendor statement "50+ screens … excellent performance" (A-07) — **inadmissible as capability evidence per PS-06 / source policy §7** | T3/T4 30–40-screen maintainability heuristic | Neither side is admissible as a threshold; Microsoft publishes no numeric cap (U-A1). Record as: performance (with correct patterns) and maintainability (team/change-rate) are different axes; size seams by team and personas |
| AA-C2 | Canvas co-authoring | 2022–24 articles + one MS blog: live Git co-authoring | T1 2025-05: "removed and no longer supported" (A-06) | T1 wins |
| AA-C3 | PCF licensing | Community "PCF = premium" | T1 2026-01: premium only for non-connector external calls (D-05) | Current page wins; short half-life |
| AA-C4 | BPF conditional logic | "don't provide any conditional business logic" (B-04) | "Conditional branching is allowed" (B-07) | Reconciled: stage-path branching, no logic execution |
| AA-C5 | Pages CIAM recommendation | Learn recommends Azure AD B2C (C-03, 2026-02) | B2C closed to new purchase 2025-05; P2 discontinued 2026-03 (V-06) | New builds → Entra External ID |
| AA-C6 | Windows player future | Docs live, no deprecation (E-10) | Stale docs, narrower capability | RISKY, not blocked |
| AA-C7 | Canvas accessibility limitations currency | Limitations page 2021-02 (E-20) | Modern controls (A-12) | 2021 page may overstate gaps |
| AA-C8 | Pages bespoke UX | T3/T4 "React not really supported" (C-11/C-12) | T1 SPA product doc 2026-07 (V-09) | Superseded for code sites; still true for Liquid sites |
| AA-C9 | Model-driven version control | T4 "no version control" | T1 solution ALM + Git integration | Weak signal; do not promote |
| AA-C10 | Code apps B2B guests | v1 / earlier preview docs: unsupported | V-18 (2026-08): supported "similar to canvas apps" | Changed with GA; v2 wins |
| AA-C11 | RTL on standalone canvas | v1 (from a search-verified E-27 reading): "not available in standalone canvas apps" | V-05 fetched: clause absent; no Learn statement found | UNKNOWN; v1 claim withdrawn |

---

## 6. Unknowns (UNKNOWN)

| Id | Unknown | Why it matters | Resolution path |
|---|---|---|---|
| U-A1 | Numeric caps on screens/controls per canvas app | Sizing heuristics rest on T4 | None published |
| U-A2 | Formal GA status of Power Fx UDFs | Build-standard bet | Release plans |
| U-A3 | Solution checker depth on canvas Power Fx | Governance tooling | Test |
| U-A5 | T1 sentence "hiding controls is not security" | AP-29 strength (partially anchored via PS-31) | Locate or keep INF |
| U-A6 | Max data sources per canvas app | Integration-heavy apps | Not on limits page |
| U-B1 | Exact licence clause for multisession in custom apps | Contact-centre requirements | Fetch Copilot Service workspace system requirements |
| U-B2 | Optimal/max model-driven apps per environment | App-per-persona sizing | None published |
| U-B4 | Tier 1 date for mandatory new look / classic UI retirement | Lifecycle exposure (AA-54) | Message center / release plan |
| U-B5 | Quantified form-load thresholds | Estimation | Direction only |
| U-C1 | Licensing effects of SPA/code sites | Cost of bespoke external UX | Not stated (V-09) |
| U-C2 | Tier 1 decision guidance Pages vs custom web | Boundary confidence MEDIUM | None exists |
| U-C3 | Server logic GA/regional availability | Hybrid maturity | Per tenant |
| U-C4 | Custom (FetchXML) table-permission GA | Access-model design | Preview watch |
| U-C5 | Pages list/grid performance limits | External UX at volume | Not published |
| U-C6 | Strict GA banner status of SPA sites (client-rendered banner risk) | Fit row 4 | Manual browser check of V-09 |
| U-C7 | Web API field-wildcard risk verbatim on Learn | AP-26 anchoring | Fetch web-api-overview / assign-table-permissions |
| U-D1 | Per-control GA status of modern controls | Control-generation lock | Reference page |
| U-D2 | Code apps in iOS/Android players | Mobile reach | Not documented |
| U-D3 | Code apps offline | Offline reach | Treat unsupported |
| U-D4 | Enhanced component properties status | Component API design | Was experimental |
| U-E1 | Push-notification throttling limits | High-volume notify | Pilot |
| U-E2 | Kiosk / shared-device mode | Frontline (ties U-14) | No Tier 1 doc |
| U-E3 | Per-app-type accessibility conformance reports | Legal claims for maker-built apps | Product-level ACRs only |
| U-E4 | Wrap-specific offline differences | Wrapped field apps | Assume = canvas offline-first |
| U-E5 | Wrap GA announcement date | Provenance precision | Fetch V-17 |
| U-E6 | RTL support in standalone canvas apps | Arabic/Hebrew canvas requirements | No Learn statement; prototype |
| U-T1 | Component-library reuse inside Teams-hosted canvas apps | Teams estate reuse | Compare page silent; studio doc suggests yes |
| U-S1 | Licensing of SharePoint customized forms (M365-included?) | Low-end cost path | Licensing Guide (Area 10) |
| U-4 | Power Pages traffic/throughput ceilings | Public high-traffic sites | CONFIRMED STILL OPEN |

---

## 7. Deferred to other areas (per review Finding 15)

| Gap | Target area | Effect if undelivered |
|---|---|---|
| Code apps SKU treatment in the September 2026 Licensing Guide; custom pages under per-app plans; Wrap licensing edge cases; SPA-on-Pages entitlements (U-C1); SharePoint customized-form licensing (U-S1) | 10 | Cost cells of fit rows 3, 4, 5, 7, 8 stay "CONDITIONAL on budget" unquantified |
| Load benchmarks, concurrency behaviour, gateway sizing (U-2, R-24) | 09 | AA-53 stays "not documented — load test" |
| Reporting/analytics and PDF generation per app type (R-13 remainder) | 03, 04 | Requirements with those needs revert to UNKNOWN |
| Push-notification throttles (U-E1) | 04 | High-volume notify designs unvalidated |
| Frontline / shared-device identity and licensing (U-14, U-E2) | 06, 10 | Kiosk row of AA-49 stays UNKNOWN |
| Managed Environment / VNet effects on code apps' public asset endpoint | 06 | Fit row 5 network-isolation cell unverified |

---

## 8. Evidence-quality notes

- **Fetched in v2 (V-01..V-19):** all decision-weight sources that were search-verified in v1, plus the new surfaces. Remaining search-verified sources: B-09, B-13 (superseded by V-08), B-14, C-14, C-19, C-21, E-14, E-15, E-17, E-21, E-22, E-26 — none carries a finding above MEDIUM on its own.
- **Aged pages (> 18 months) still relied on:** A-01, A-03, A-10, D-03, E-04, E-06, E-11, E-19, E-20, E-23, E-24, V-02 (2022-06 upd. 2025-05), V-05 (2022-05, pre-release banner), V-16 (2020-09 upd. 2024-01). Findings on them carry MEDIUM on currency where noted.
- **Inadmissible statements:** A-07's "100 tables / 50 screens" (vendor scale claim) — recorded only in AA-C1. Connector-count and "build faster" marketing figures not used.
- **T3 with commercial bias:** C-10 (MVP consultant), C-11/C-12 (consultancies), D-17/D-18, A-19 cluster — signals and negative evidence only.
- **Client-rendered banner risk:** V-09 and V-18 show no preview wording in fetched body; strict banner state marked UNKNOWN (U-C6) rather than asserted.
- **"Choose your app type" guidance:** retired pattern pages replaced by the AI Plan designer (B-11/B-12); durable written criteria = B-01 comparison table + D365 guidance-hub UI/UX articles. No standalone Microsoft decision tree exists in 2026.

---

## 9. Implications for the aisa knowledge model (pointers, not pack content)

- **Technology-neutral Discovery signals:** distinct persona experiences; form-factor mix and browser-vs-app expectation; responsive reflow need; device hardware; offline depth and surface; branded-app audience; push requirement; deep-link frequency; navigation shape (relational browsing vs task wizard); accessibility regime; language count + RTL; expected screen count and change velocity; maker team size and pro-dev capacity; UI-reuse ambitions; freshness expectation; audience identity tier (employee / known partner / authenticated customer / anonymous); team-scoped vs enterprise scope; report-driven vs list-driven entry point; tolerance to vendor-driven UI change; whether a first-party app already covers the need.
- **Hard boundaries with Microsoft-stated evidence:** components not in galleries/forms (AA-31); no co-authoring (AA-06); custom pages ≤ 25 / ≤ 10 connectors, no offline/device controls (AA-16); Wrap no push/B2C/sovereign (AA-39); offline never in browser, Teams, custom pages, with flows or FLS (AA-42..44); Pages cache (AA-27); model-driven theming ceiling (AA-14); BPF caps (AA-19); code apps public endpoint + premium (AA-35); model-driven no phone browser (AA-45); Dataverse for Teams caps + one-way upgrade (AA-50); Power BI visual 1,000 rows / no embed-for-customers (AA-51); multisession unmanaged-only (AA-20); Pages SPA single-language/no Git/no PWA (AA-23).
- **Corrected vs v1:** RTL on canvas is UNKNOWN, not POOR (AA-48); Wrap GA is a T2 statement, not inferred (AA-38); code apps support B2B guests (AA-35, AA-52); vendor scale statement removed from fit evidence (AA-01).
- **Architecture options the pack must be able to output:** configure/buy/first-party; Teams-hosted app; SharePoint customized form; Power BI-embedded canvas; single canvas app; partitioned canvas suite; model-driven app(s) per persona; model-driven shell + custom pages; canvas + PCF; component-library-backed estate; code app; Power Pages Liquid site; Power Pages SPA site; Pages + server logic/Azure hybrid; Wrap; Pages PWA; custom web/native.
- **Validation before commitment:** persona/screen projection vs partition seams; responsive prototype on the real device mix; offline checklist vs data model; deep-link inventory; accessibility path per app type; language matrix (incl. RTL prototype if canvas); Wrap Conditional Access dry run; Pages table-permission review + PPAC security status + load test; component-library update-labour estimate; control-generation lock; Dataverse for Teams growth forecast vs 2 GB; first-party fit check before any build.

---

## 10. Source register

### 10.1 Canvas (A-)

| Id | Tier | Kind | Title | URL | Date |
|---|---|---|---|---|---|
| A-01 | T1 | fetched | Building responsive canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/build-responsive-apps | 2022-01-27 |
| A-02 | T1 | fetched | Create responsive layouts in canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-responsive-layout | 2026-01-13 |
| A-03 | T1 | fetched | Build large and complex canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/working-with-large-apps | 2023-04-07 |
| A-04 | T1 | fetched | App object (Formulas/UDFs/OnStart/StartScreen) | https://learn.microsoft.com/en-us/power-platform/power-fx/reference/object-app | 2026-06-11 |
| A-05 | T1 | fetched | Source control for canvas apps (Git integration) | https://learn.microsoft.com/en-us/power-platform/alm/git-integration/canvas-apps-git-integration | 2025-10-08 |
| A-06 | T1 | fetched | Disconnect Git version control (removed) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/git-version-control | 2025-05-14 |
| A-07 | T1 (vendor statement on scale) | fetched | How to create performant Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-performant-apps-overview | 2026-08-20 |
| A-08 | T1 | fetched | Power Apps system requirements and limits | https://learn.microsoft.com/en-us/power-apps/limits-and-config | 2026-01-12 |
| A-10 | T1 | fetched | Canvas deep linking | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/how-to/deep-linking | 2022-07-27 |
| A-11 | T1 | fetched | Debugging canvas apps with Live monitor | https://learn.microsoft.com/en-us/power-apps/maker/monitor-canvasapps | 2024-11-14 |
| A-12 | T1 | fetched | Modern controls and theming overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/overview-modern-controls | 2026-02-23 |
| A-14 | T1 | fetched | Canvas deprecations | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/important-changes-deprecations | 2026-01-09 |
| A-16 | T2 | cited | Canvas app coding standards (PDF) | https://www.microsoft.com/power-platform/blog/wp-content/uploads/2024/06/PowerApps-canvas-app-coding-standards-and-guidelines.pdf | 2024-06 |
| A-18 | T2 | cited | UDFs/UDTs/enhanced component properties blog | https://www.microsoft.com/en-us/power-platform/blog/power-apps/user-defined-functions-user-defined-types-and-enhanced-component-properties-move-forward/ | n/a |
| A-19 | T3/T4 | signals | Independent cluster (complexity ceiling; stale co-authoring; role-UI) | aidevme / ESPC / Medium / Withum / Arinco / M. Devaney | 2025–2026 |

### 10.2 Model-driven + custom pages (B-)

| Id | Tier | Kind | Title | URL | Date |
|---|---|---|---|---|---|
| B-01 | T1 | fetched | Overview of building a model-driven app | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-driven-app-overview | 2026-01-09 |
| B-02 | T1 | fetched | Converge model-driven and canvas apps (custom page) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-app-page-overview | 2026-03-13 |
| B-03 | T1 | fetched | Known issues with custom pages | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-app-page-issues | 2026-08-06 |
| B-04 | T1 | fetched | Business process flows overview | https://learn.microsoft.com/en-us/power-automate/business-process-flows-overview | 2026-08-15 |
| B-05 | T1 | fetched | Modern themes in model-driven apps | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/modern-theme-overrides | 2026-07-07 |
| B-06 | T1 | fetched | Open apps/forms/views with a URL | https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/open-forms-views-dialogs-reports-url | 2026-04-21 |
| B-07 | T1 | fetched | UI/UX design components (D365 guidance hub) | https://learn.microsoft.com/en-us/dynamics365/guidance/develop/ui-ux-component-details-model-driven-apps | 2024-06-03 |
| B-08 | T1 | fetched | Design forms for performance | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/design-performant-forms | 2026-05-19 |
| B-09 | T1 | search-verified | Command designer limitations | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/command-designer-limitations | n/a |
| B-10 | T1 | fetched | App designer (sitemap) | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/design-custom-business-apps-using-app-designer | 2026-02-12 |
| B-11 | T1 | fetched | Plan designer | https://learn.microsoft.com/en-us/power-apps/maker/plan-designer/plan-designer | 2026-08-07 |
| B-12 | T1 | fetched | Build your solution (plan designer) | https://learn.microsoft.com/en-us/power-apps/maker/plan-designer/build-solution | 2025-12-09 |
| B-14 | T1/2 | search-verified | Application modernization white paper | https://learn.microsoft.com/en-us/power-platform/guidance/white-papers/application-modernization | n/a |

### 10.3 Power Pages (C-)

| Id | Tier | Kind | Title | URL | Date |
|---|---|---|---|---|---|
| C-00 | T1 | fetched | Licensing FAQ (Power Pages section) | https://learn.microsoft.com/en-us/power-platform/admin/powerapps-flow-licensing-faq | 2026-08-14 |
| C-01 | T1 | fetched | Table permissions | https://learn.microsoft.com/en-us/power-pages/security/table-permissions | 2026-02-28 |
| C-02 | T1 | fetched | Authentication overview | https://learn.microsoft.com/en-us/power-pages/security/authentication/ | 2026-02-28 |
| C-03 | T1 | fetched | Local authentication + registration settings | https://learn.microsoft.com/en-us/power-pages/security/authentication/set-authentication-identity | 2026-02-28 |
| C-04 | T1 | fetched | Entra External ID setup | https://learn.microsoft.com/en-us/power-pages/security/authentication/entra-external-id | 2026-01-22 |
| C-05 | T1 | fetched | Bootstrap overview | https://learn.microsoft.com/en-us/power-pages/configure/bootstrap-overview | 2024-03-19 |
| C-06 | T1 (release plan) | fetched | Release plan: single-page applications | https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave1/power-pages/build-modern-single-page-applications | 2026-02-11 |
| C-07 | T3 | fetched | AppOmni: Power Pages data exposure | https://appomni.com/ao-labs/microsoft-power-pages-data-exposure-reviewed/ | 2024-11-14 |
| C-08 | T1 | fetched | Server-side caching | https://learn.microsoft.com/en-us/power-pages/admin/clear-server-side-cache | 2026-04-29 |
| C-09 | T1 | fetched | CDN configuration | https://learn.microsoft.com/en-us/power-pages/configure/configure-cdn | 2026-06-18 |
| C-10 | T3 | fetched | M. Mendes: Pages vs custom .NET + Dataverse | https://michelcarlo.com/2025/06/01/ | 2025-06-01 |
| C-11 | T4 | signals | UDS Systems: reasons Pages might not fit | uds.systems/blog | n/a |
| C-12 | T4 | signals | Xtivia: when (not) to choose Power Pages | solutions.microsoft.xtivia.com/blog | n/a |
| C-14 | T1 | search-verified | pac pages CLI (upload-code-site) | https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/pages | n/a |
| C-15 | T3 | cited | SecurityWeek: Low-Code, High Risk | securityweek.com | 2024-11 |
| C-16 | T3 | cited | Infosecurity: Power Pages misconfiguration | infosecurity-magazine.com/news/microsoft-power-pages/ | 2024-11 |
| C-17 | T1 | fetched | Power Pages system requirements and limits | https://learn.microsoft.com/en-us/power-pages/system-requirements | 2026-04-28 |
| C-18 | T1 | fetched | Use solutions with Power Pages | https://learn.microsoft.com/en-us/power-pages/configure/power-pages-solutions | 2026-01-29 |
| C-19 | T1 | search-verified | Pages pipelines / enhanced data model | https://learn.microsoft.com/en-us/power-pages/configure/power-pages-pipelines | n/a |
| C-20 | T1 | fetched | Server logic overview | https://learn.microsoft.com/en-us/power-pages/configure/server-logic-overview | 2026-05-13 |
| C-21 | T1 | search-verified | Server logic → Azure Function tutorial | https://learn.microsoft.com/en-us/power-pages/configure/server-logic-azure-function | n/a |

### 10.4 Components, theming, code apps (D-)

| Id | Tier | Kind | Title | URL | Date |
|---|---|---|---|---|---|
| D-01 | T1 | fetched | Canvas component overview | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/create-component | 2026-01-13 |
| D-02 | T1 | fetched | Component library | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library | 2026-08-20 |
| D-03 | T1 | fetched | Component library ALM | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/component-library-alm | 2022-06-10 |
| D-04 | T1 | fetched | PCF limitations | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/limitations | 2025-07-01 |
| D-05 | T1 | fetched | PCF overview (licensing) | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/overview | 2026-01-09 |
| D-06 | T1 | fetched | Code components for canvas apps | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/component-framework-for-canvas-apps | 2026-08-20 |
| D-07 | T1 | fetched | React controls & platform libraries | https://learn.microsoft.com/en-us/power-apps/developer/component-framework/react-controls-platform-libraries | 2025-10-10 |
| D-08 | T1 | fetched | Modern controls overview (= A-12) | (see A-12) | 2026-02-23 |
| D-09 | T1 | fetched | Modern controls reference (preview labels) | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-controls-reference | 2026-07-20 |
| D-10 | T1 | fetched | Canvas modern theming | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/controls/modern-controls/modern-theming | 2026-01-21 |
| D-11 | T1 | fetched | Model-driven modern themes (= B-05) | (see B-05) | 2026-07-07 |
| D-12 | T1 | fetched | CoE theming components (kit unmaintained) | https://learn.microsoft.com/en-us/power-platform/guidance/coe/theming-components | 2026-04-20 |
| D-13 | T1 | fetched | Well-Architected XO:02 design standards | https://learn.microsoft.com/en-us/power-platform/well-architected/experience-optimization/design-standards | 2025-08-05 |
| D-14 | T1 | fetched | Creator Kit overview (preview) | https://learn.microsoft.com/en-us/power-platform/guidance/creator-kit/overview | 2024-08-12 |
| D-16 | T2 | cited | What's new March 2026 (data grid GA) | microsoft.com/power-platform/blog | 2026-03 |
| D-17 | T3 | signals | PowerApps911: modern vs classic | powerapps911.com | n/a |
| D-18 | T3 | signals | SharePains: classic→modern migration | sharepains.com | 2026-01-27 |
| D-19 | T3 | signals | MC1254543 MDA theming GA / new look mandatory | mc.merill.net/message/MC1254543 | 2026-03/04 |
| D-20 | T2 | cited | Code apps GA blog | https://www.microsoft.com/en-us/power-platform/blog/power-apps/generally-available-host-and-run-code-apps-in-power-apps/ | 2026-02-05 |
| D-22 | T1 | fetched | ALM for code apps | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/how-to/alm | 2026-08-27 |
| D-23 | T1 | fetched | Code apps system configuration | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/system-limits-configuration | 2026-08-12 |

### 10.5 Mobile, Wrap, offline, a11y, l10n (E-)

| Id | Tier | Kind | Title | URL | Date |
|---|---|---|---|---|---|
| E-01 | T1 | fetched | Overview of wrap | https://learn.microsoft.com/en-us/power-apps/maker/common/wrap/overview | 2025-02-04 |
| E-02 | T1 | fetched | FAQ for wrap | https://learn.microsoft.com/en-us/power-apps/maker/common/wrap/faq | 2026-06-12 |
| E-03 | T1 | fetched | Advantages and limitations of Wrap | https://learn.microsoft.com/en-us/power-apps/maker/common/wrap/limitations | 2025-02-04 |
| E-04 | T1 | fetched | Mobile offline for canvas apps overview | https://learn.microsoft.com/en-us/power-apps/mobile/canvas-mobile-offline-overview | 2024-06-05 |
| E-05 | T1 | fetched | Mobile offline limitations — canvas | https://learn.microsoft.com/en-us/power-apps/mobile/limitations-canvas-apps | 2026-06-17 |
| E-06 | T1 | fetched | Mobile offline limitations — model-driven | https://learn.microsoft.com/en-us/power-apps/mobile/offline-limitations | 2024-09-26 (upd. 2025-03) |
| E-07 | T1 | fetched | Accessibility in Power Pages | https://learn.microsoft.com/en-us/power-pages/admin/accessibility | 2025-04-22 |
| E-08 | T1 | fetched | Power Apps Notification V2 connector | https://learn.microsoft.com/en-us/connectors/powerappsnotificationv2/ | 2024-03 (upd. 2025-10) |
| E-09 | T1 | fetched | Manage mobile app with Intune | https://learn.microsoft.com/en-us/power-apps/mobile/intune | 2024-10-11 (upd. 2025-05) |
| E-10 | T1 | fetched | Important changes (deprecations) | https://learn.microsoft.com/en-us/power-platform/important-changes-coming | 2026-05-22 |
| E-11 | T1 | fetched | Use Power Apps for Windows | https://learn.microsoft.com/en-us/power-apps/mobile/windows-app-use | 2023-10-25 |
| E-14 | T1 | search-verified | Mobile sensors how-to | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/how-to/mobile-sensors | n/a |
| E-15 | T1 | search-verified | Intune Multiple Managed Accounts | https://learn.microsoft.com/en-us/intune/app-management/protection/multiple-managed-accounts | n/a |
| E-16 | T1 | fetched | 2025 wave 2: offline profiles in maker studio | https://learn.microsoft.com/en-us/power-platform/release-plan/2025wave2/power-apps/create-offline-profiles-maker-studio-canvas-apps | n/a |
| E-17 | T1 | search-verified | Set up mobile offline (model-driven) | https://learn.microsoft.com/en-us/power-apps/mobile/setup-mobile-offline | n/a |
| E-19 | T1 | fetched | Create accessible canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps | 2022-09-06 (upd. 2025-05) |
| E-20 | T1 | fetched | Accessibility limitations in canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/accessible-apps-limitations | 2021-02-26 |
| E-21 | T1 | search-verified | Screen reader in model-driven apps | https://learn.microsoft.com/en-us/power-apps/user/screen-reader | n/a |
| E-22 | T1 | search-verified | Accessible web resources (model-driven) | https://learn.microsoft.com/en-us/power-apps/developer/model-driven-apps/create-accessible-web-resources | n/a |
| E-23 | T1 | fetched | Build a multi-language canvas app | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/multi-language-apps | 2021-01-27 |
| E-24 | T1 | fetched | Build global support into canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/global-apps | 2016-10-25 (upd. 2025-05) |
| E-25 | T1 | fetched | Multiple-language Power Pages sites | https://learn.microsoft.com/en-us/power-pages/configure/enable-multiple-language-support | 2025-08-06 |
| E-26 | T1 | search-verified | Export table/column text for translation | https://learn.microsoft.com/en-us/power-apps/maker/data-platform/export-customized-entity-field-text-translation | n/a |

### 10.6 v2 verification fetches (V-)

| Id | Tier | Kind | Title | URL | Date |
|---|---|---|---|---|---|
| V-01 | T1 | fetched | ReadNFC function | https://learn.microsoft.com/en-us/power-platform/power-fx/reference/function-readnfc | 2024-03-22 (upd. 2025-10-10) |
| V-02 | T1 | fetched | Limitations of controls in canvas apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/control-limitations | 2022-06-01 (upd. 2025-05-07) |
| V-03 | T1 | fetched | Power Pages sites as PWAs | https://learn.microsoft.com/en-us/power-pages/configure/progressive-web-apps | 2024-05-02 |
| V-04 | T1 | fetched | Build and distribute PWAs | https://learn.microsoft.com/en-us/power-pages/configure/build-progressive-web-apps | 2024-11-13 |
| V-05 | T1 (pre-release banner) | fetched | Localize labels and strings on a custom page | https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/custom-page-localize | 2022-05-26 (upd. 2025-05-07) |
| V-06 | T1 | fetched | Azure AD B2C FAQ | https://learn.microsoft.com/en-us/azure/active-directory-b2c/faq | 2025-06-20 (upd. 2026-06-11) |
| V-07 | T1 | fetched | Important changes — Test Engine deprecation | https://learn.microsoft.com/en-us/power-platform/important-changes-coming | 2026-05-22 (upd. 2026-08-14) |
| V-08 | T1 | fetched | Enable multisession in custom apps | https://learn.microsoft.com/en-us/dynamics365/customer-service/administer/enable-multisession-custom-apps | 2025-10-16 |
| V-09 | T1 | fetched | Create and deploy an SPA in Power Pages (code sites) | https://learn.microsoft.com/en-us/power-pages/configure/create-code-sites | 2026-07-21 |
| V-10 | T1 | fetched | Manage website security from PPAC | https://learn.microsoft.com/en-us/power-pages/admin/admin-center-security | 2025-03-12 (upd. 2026-08-31) |
| V-11 | T1 | fetched | Dataverse for Teams vs Dataverse | https://learn.microsoft.com/en-us/power-apps/teams/data-platform-compare | 2025-05-28 |
| V-12 | T1 | fetched | About the Dataverse for Teams environment | https://learn.microsoft.com/en-us/power-platform/admin/about-teams-environment | 2026-05-15 (upd. 2026-08-14) |
| V-13 | T1 | fetched | Power Apps visual for Power BI | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/powerapps-custom-visual | 2025-03-04 |
| V-14 | T1 | fetched | Understand SharePoint forms integration | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/sharepoint-form-integration | 2025-11-14 |
| V-15 | T1 | fetched | Integrate SharePoint Online into Power Apps | https://learn.microsoft.com/en-us/power-apps/maker/canvas-apps/sharepoint-list-integration-overview | 2026-01-13 |
| V-16 | T1 | fetched | Embed a canvas app as a Teams tab | https://learn.microsoft.com/en-us/power-apps/teams/embed-teams-tab | 2020-09-15 (upd. 2024-01-30) |
| V-17 | T2 | search-verified | Announcing GA of wrap for Power Apps (blog) | https://www.microsoft.com/en-us/power-platform/blog/power-apps/announcing-general-availability-of-wrap-for-power-apps/ | date unverified |
| V-18 | T1 | fetched | Power Apps code apps overview | https://learn.microsoft.com/en-us/power-apps/developer/code-apps/overview | 2026-08-12 (upd. 2026-08-19) |
| V-19 | T1 | fetched | Power Apps system requirements and limits (phone-browser footnote) | https://learn.microsoft.com/en-us/power-apps/limits-and-config | 2026-01-12 (upd. 2026-01-14) |

---

## 11. v1 → v2 id mapping

| v1 id | v2 id | Change |
|---|---|---|
| AA-01..AA-11 | AA-01..AA-11 | AA-01 vendor statement removed; AA-08 re-sourced to V-07; AA-10 anchored to PS-31 |
| AA-12-CONF | — (AA-C1 only) | Folded into conflicts; duplicate removed |
| AA-12..AA-20 | AA-12..AA-20 | AA-20 gains multisession unmanaged-only constraint (V-08) |
| AA-21..AA-30 | AA-21..AA-30 | AA-22 adds B2C P2 retirement (V-06); AA-23 re-based on product doc (V-09); AA-25 adds Microsoft controls (V-10) |
| AA-31..AA-37 | AA-31..AA-37 | AA-35 B2B guests changed (V-18); AA-36 gains rung 0 |
| AA-38..AA-41 | AA-38..AA-41 | AA-38 GA re-sourced to T2 blog (V-17) |
| AA-41a / AA-41b / AA-41c | AA-42 / AA-43 / AA-44 | Renumbered; AA-44 Pages PWA cells re-sourced (V-03/V-04/V-09) |
| AA-42 | AA-45 | Adds model-driven phone-browser constraint (V-19); V-01/V-02 fetched |
| AA-43 | AA-46 | unchanged |
| AA-44 | AA-47 | unchanged |
| AA-45 | AA-48 | RTL on canvas re-based to UNKNOWN (V-05) |
| AA-46 | AA-49 | Adds browser-BYOD and RTL rows |
| — | AA-50 | NEW: Teams-hosted apps |
| — | AA-51 | NEW: embedded canvas surfaces |
| — | AA-52 | NEW: identity per app type |
| — | AA-53 | NEW: app-level performance/concurrency |
| — | AA-54 | NEW: lifecycle exposure per app type |

---

## 12. Closing summary

## Gaps Fixed
- Review F1 (provenance): header corrected; seven decision-weight search-verified sources fetched (V-01..V-19); confidence re-graded (RTL → UNKNOWN).
- Review F2 (ids): AA-12 collision removed; offline findings renumbered AA-42..44; per-finding origin tags added; mapping table §11.
- Review F3 (vendor statement): removed from AA-01; confined to AA-C1 as inadmissible.
- Review F4 (SPA GA): re-based on product doc V-09 (2026-07-21, no preview wording) with its limitation list; strict banner state kept UNKNOWN (U-C6).
- Review F5 (Teams): AA-50 + fit row 6 + AP-32.
- Review F6 (embedded surfaces): AA-51 + fit row 7 + AP-34.
- Review F7 (buy/first-party): rung 0 in AA-36 + fit row 0 + AP-35.
- Review F8 (phone browser): AA-45 + AP-31 (V-19).
- Review F9 (identity): AA-52; code apps B2B change captured.
- Review F10 (performance/concurrency): AA-53 with PS-18/PS-20 cross-refs.
- Review F11 (origin tags): every finding tagged.
- Review F12 (AppOmni Microsoft side): V-10 controls added to AA-25.
- Review F13 (lifecycle): AA-54.
- Review F14 (RTL): hedged to UNKNOWN everywhere (boundaries, AA-48, AA-49, summary).
- Review F15 (deferrals): §7 table.
- Review F16 (AP-29): anchored to PS-31/S-43.
- Review F17 (duplicate conflict): removed.

## Gaps Still Open
- Strict preview/GA banner state of Pages SPA sites and code apps (client-rendered banner risk, U-C6).
- Web API field-wildcard verbatim on Learn (U-C7); multisession exact licence clause (U-B1); Wrap GA date (U-E5).
- Tier 1 date for mandatory model-driven new look (U-B4).
- SharePoint customized-form licensing and a Microsoft "when to go standalone" statement (U-S1; INF used).
- Component-library reuse in Teams-hosted apps (U-T1).
- No Tier 1 Pages-vs-custom decision guidance (U-C2) — boundary stays MEDIUM.

## New Decision Criteria
- Configure/buy/first-party before any build (rung 0), with multisession as the worked example.
- Team-scoped app on seeded licences with no PCF/offline/API/model-driven → Teams-hosted; growth forecast vs 2 GB decides.
- Report-driven write-back ≤ 1,000 rows, internal → Power BI visual; external report consumers → not supported.
- Form over one SharePoint list, readers = list readers → customized form; portability/solution ALM → standalone app.
- Phone-browser BYOD × model-driven → collision; native player + MAM required.
- Audience identity tier (employee / B2B guest / authenticated customer / anonymous) → app-type set; B2B guests now include code apps, conditional on licence recognition.
- Multi-language external UX → Pages Liquid, not SPA (single-language).
- Long lifetime × tolerance to vendor UI change → weigh model-driven wave exposure vs ALM simplicity vs code apps' self-maintenance.
- Concurrency does not differentiate app types by documentation; the data path does.

## New Constraints
- Multisession in custom model-driven apps: unmanaged solution only; not for default apps (Sales Hub).
- Pages SPA sites: no Git integration, single-language, no PWA setting, no OOB lists/forms/Liquid, no Power Fx, limited SEO, no built-in testing.
- Azure AD B2C P2 discontinued 2026-03-15; B2C not purchasable since 2025-05-01.
- Dataverse for Teams: 2 GB cap "can't be extended further"; one-way upgrade converts all users to Power Platform licences.
- Power BI visual: 1,000-row pass-through; embed-for-organization only; no Report Server; write-back visible on next refresh.
- SharePoint customized forms: no manual sharing; no automated cross-environment copy.
- Teams tab embedding: sensors (Acceleration, Compass, Location) unsupported; https-only content; no attachment download on Teams mobile.
- Model-driven apps in a phone browser: unsupported.

## New Anti-Patterns
- AP-31 model-driven via phone browser; AP-32 Dataverse for Teams growth without upgrade budget; AP-33 SPA-on-Pages for multi-language/PWA needs; AP-34 SharePoint form as portable app; AP-35 custom multisession build when first-party fits.

## Remaining Unknowns
- U-4 (Pages throughput), U-A1 (canvas numeric caps), U-B1, U-B4, U-C1, U-C6, U-C7, U-D2/U-D3 (code apps mobile/offline), U-E1 (push throttles), U-E2 (kiosk), U-E3 (per-app ACR), U-E5, U-E6 (canvas RTL), U-T1, U-S1 — full table §6.

## Confidence
**MEDIUM-HIGH.** HIGH on documented constraints and the internal/external, offline, device, componentisation and converged-architecture boundaries (all fetched Tier 1 with dates). MEDIUM on: Pages-vs-custom boundary (T3 only), SPA/code-apps strict GA state, maintainability ceiling (no Microsoft threshold; heuristics inadmissible), lifecycle-exposure ranking (INF), and every "CONDITIONAL on budget" cell pending Area 10.
