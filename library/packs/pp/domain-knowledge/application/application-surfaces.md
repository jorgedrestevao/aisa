# Application surfaces — which surface can carry which experience

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Is this requirement already met by a first-party app or a capability the organisation already owns?*
- *Can this surface deliver the required interaction, offline depth and accessibility — and can it deliver offline alongside field-level confidentiality?*
- *Which surface serves this identity class, and what does it oblige downstream?*
- *What does choosing this surface forfeit, and which of those choices cannot be undone?*

This file states **what each application surface can and cannot carry, and what each one forfeits**. It
does not decide **which surface wins** — that belongs to the decision model (`decision-tree.md` S4–S6).
There is no app-type recommendation tree here, no ranking of surfaces, and no size threshold.

---

## 1. What this is for · `decision-grade`

A surface question is answerable only once the *experience* requirement is observable: who the users are
in identity terms, on what device, connected or not, under which accessibility and language regime, and
how they arrive at a record. Those five inputs, not a preference for a technology, are what the documented
boundaries bite on.

**The prior question — rung 0.** Before any surface is discussed: *is this requirement already met by a
first-party application, a suite feature, or a marketplace product the organisation owns or can buy?* The
vendor's own extension guidance is explicit that settings-level configuration is the least disruptive
change, that low-code extension comes next, that partner solutions are preferable to extending, and that
replicating a legacy solution produces a heavily customised result that fails to use the new platform's
strengths. Every extension carries performance, lifecycle, upgrade and support cost. Rung 0 is answered
first because a positive answer removes the surface question entirely.

Rung 0 is also where the honest negative lives: a first-party application may cover the requirement while
being a poor fit for *part* of it. Record the covered subset and the gap separately, so the remaining
scope is what a surface has to carry.

## 2. When it becomes material · `decision-grade`

- The audience includes anyone who is **not an employee with a work or school account**.
- Work happens **disconnected**, or on a device whose **hardware** (scanner, camera, NFC, location) is part
  of the task.
- A **legal accessibility regime** applies, or the audience is public-sector.
- More than two or three **languages**, or a right-to-left language.
- The organisation wants a **branded, store-distributed** application.
- Users must **arrive directly at a record** from mail, chat or another system.
- **Push notifications** are part of the requirement.
- Two or more **materially divergent persona experiences** are in scope.
- The requirement is **team-scoped today** and might not be in two years.
- An existing **report, list or chat surface** is the natural entry point.
- The requirement is **conversational or agentic** (→ §8: decision-blocked).

## 3. The surfaces, and each one's documented boundary · `decision-grade`

Read a row as: *what does this surface carry, and where does the documentation stop?* This is a
**capability inventory**. It is not ordered by preference and the last rows are not fallbacks.

| Surface                                                                 | What it carries                                                                                                                                                                                                                                                                                                                                                                                    | Documented boundary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Configure / buy / first-party / owned capability** (rung 0)           | A requirement already met by a first-party application, a suite feature or a marketplace product, with or without configuration                                                                                                                                                                                                                                                                    | Feature-fit gaps, and the entitlement for the first-party product itself                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **Canvas app**                                                          | Task-focused internal experience over any connector; pixel-level layout control; device hardware on the native mobile players; the only surface that supports full offline-first                                                                                                                                                                                                                   | Responsiveness is **opt-in effort**, not the default, and the authoring canvas does not render the sizing formulas — behaviour is verified only by publishing; several controls are unsupported inside layout containers. Real-time co-authoring was removed: **one maker per app at a time**. Accessibility is the maker's responsibility. Multi-language is a hand-built dictionary. No route model — deep links are hand-built per destination. External and anonymous audiences are not served here                                                                                                                                                                              |
| **Record-centric app** (model-driven)                                   | Data-dense, record-centric, process-driven work over the governed store; automatic relational navigation; row and column security and audit inherited from the store; built-in accessibility; installed language packs; native addressable, security-trimmed record URLs                                                                                                                           | Requires a data model in the governed store — there is no such app without it. The **shell is platform-owned**: theming reaches colours, font, logo and header, and named areas are not themed at all. **Running it in a phone browser is not supported** — the native mobile player is required. Guided-stage constructs execute no logic of their own and carry published caps on stages and tables. The multisession experience can be enabled **only in an unmanaged solution**, which collides with the managed-only-in-production doctrine                                                                                                                                     |
| **Custom pages inside a record-centric app**                            | A few bespoke screens on a structured backbone; the vendor's own stated convergence vehicle, replacing embedded canvas apps                                                                                                                                                                                                                                                                        | Published ceilings on pages per app and on connectors and connection references across those pages. **No offline. No device-capability controls** (scan, photo capture, file attach) — mobile support is preview. Not supported inside the mail client. **Page state is not restored** on back-navigation or across sessions. The host app keeps serving the last-published version of the page — a double-publish coupling. Third-party cookies required. Not all canvas controls are available; user-locale formats are unsupported. **A standalone canvas app cannot be converted into a custom page**                                                                            |
| **External-audience site — low-code build model** (Liquid)              | Authenticated external users over the governed store; portal-shaped interaction; row access as configuration through table permissions bound to web roles, deny-by-default; platform-attested conformance to the named accessibility standards; many out-of-the-box languages; content delivery and web-application firewall included; read-only offline pages via the progressive-web-app setting | Server-side cache: only changes made **through the website** invalidate instantly, and reflection of store changes into the site **is never guaranteed to be immediate** (§5.2 stamp). Content caching applies to **anonymous** traffic only — authenticated pages are not cached. Throughput, request-rate and concurrency ceilings are **not published**. Offline **write** is not available. Its interface is documented as not intended as a third-party integration surface. Customisation you add is your accessibility responsibility                                                                                                                                         |
| **External-audience site — code-first build model** (SPA)               | A client-rendered single-page experience managed only through source code and command-line tooling                                                                                                                                                                                                                                                                                                 | Surrenders most of what the low-code model provides: no out-of-the-box lists or forms, no Liquid, no low-code design workspaces, no formula language, **single-language only**, **no progressive-web-app setting** (therefore no offline read), limited discoverability by search engines, no built-in test tooling, and **no platform source-control integration**. Minimum site and tooling versions apply. Closer to a hosted custom application than to a customised site. **Preview / general-availability banner state is unverified**                                                                                                                                         |
| **Code app**                                                            | A pro-developer single-page application in a mainstream front-end framework, hosted and governed by the platform, over connectors and the governed store; internal and business-guest audiences at parity with canvas                                                                                                                                                                              | Every end user requires the premium entitlement. **Compiled assets are served from a publicly accessible endpoint that does not support address-based restriction** — the documented alternative is conditional access. The documentation states not to store sensitive user or organisational data in the app. No Windows player. No list-form integration. Lifecycle is solution- and pipeline-based, with **no source-code integration**. Mobile-player support and offline are **undocumented — treat offline as unsupported until verified**. **Banner state unverified**                                                                                                       |
| **Team-hosted surface** (team-scoped store)                             | A team-scoped app inside the collaboration client on seeded entitlement                                                                                                                                                                                                                                                                                                                            | A combined row-count and storage ceiling of **2 GB** that **cannot be extended** *(documented reading · read 2026-09-04 · re-verify: `VC-07`)*, one organisational unit, and no interface access, extension plug-ins, code components, record-centric apps, audit, column security or mobile offline. Growth past it is a **one-way graduation** (§7)                                                                                                                                                                                                                                                                                                                                |
| **Embedded surfaces** — report visual · list-customised form · chat tab | Write-back or drill-through from a report over the selected rows; a form over a single list whose readers are the list's readers; an existing app surfaced as a tab                                                                                                                                                                                                                                | Report visual: a published ceiling on rows passed from the report, **organisation-embedding only** (customer-embedding is not supported), it cannot filter or return data to the report, write-back appears only on the next refresh, the app is shared separately, the report server does not support it, and browser support is uneven. List-customised form: **cannot be shared manually at all** — access is inherited from list read access — generic lists and libraries only, and **no automated cross-environment copy exists**. Chat tab: several sensors are unsupported, content must be served over TLS, and attachment download from the mobile client is not available |
| **Branded native wrapping**                                             | A custom-branded store or managed-distribution mobile application built **from canvas apps only**, with icon, splash, welcome screen and colours                                                                                                                                                                                                                                                   | **No push notifications.** No consumer audience. No sovereign clouds. No customer-managed keys or vendor-access approval — the documentation states assets may be exposed to service operators during the build. A published bundle-size ceiling. No visible sign-out. Requires a cloud subscription for key and blob storage plus code-signing assets, and the packaged application must be **re-wrapped and redistributed at least monthly**. A conditional-access policy requiring an approved client application blocks the wrapped app and needs an explicit exclusion                                                                                                          |
| **Hybrid with cloud services**                                          | Logic, integration or compute beyond the low-code envelope while the user-facing surface stays on-platform — server-side script on the external-audience site, extension plug-ins or cloud functions behind any surface                                                                                                                                                                            | Execution-time and sandbox limits apply, the tenant can **block outbound calls** from server-side site logic, and an allowed-domain list governs what it may reach. Regional and general-availability state is per-tenant                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Custom development**                                                  | Data that stays permanently outside the platform stores; throughput or availability commitments the platform does not publish; product-grade consumer experience; a public interface surface; a branded application with push; custom synchronisation and conflict rules; address-restricted hosting                                                                                               | The platform's connector estate, managed governance, configured row access and included authentication are not inherited — they become build items. There is **no vendor decision guidance** on the site-versus-custom boundary; that judgement is a supported synthesis, not vendor-endorsed                                                                                                                                                                                                                                                                                                                                                                                        |

## 4. Identity class — the first hard fork · `decision-grade`

Identity class is not a preference; it decides which surfaces are reachable at all, and it drives the
meter (`economics/licensing-and-cost-drivers.md`).

| Identity class | Surfaces that serve it | What it obliges |
|---|---|---|
| **Employee** — work or school account in the tenant | Every internal surface | Personal consumer accounts have been removed from the platform; sovereign clouds bind to a specific directory instance |
| **Known external partner** — directory business guest | Canvas, record-centric, code apps and branded wrapping, with explicit tenant setup | The guest's entitlement must be **recognised across tenants**; per-app-scoped plans are not, because they are scoped to apps in one environment. Guests need a standalone browser session |
| **Authenticated customer / consumer identity** | External-audience sites only | An external-identity service is a **prerequisite** — its own tenant, cost and operating burden. The previously recommended consumer-identity service is closed to new customers and its higher tier is being discontinued; the current path for new sites is the external-identity offering. Local site authentication is documented as **not recommended** and is enabled by default |
| **Anonymous public** | External-audience sites, or custom development | Anonymous permissions are documented as making data **visible to anyone**; open self-registration is **on by default**. See §9 and `security/security-controls.md` |
| **Frontline / shared-device / non-directory identity** | `UNKNOWN` | No vendor position located. Do not assume a shared-device or kiosk mode exists; treat as an open Unknown routed to a role or a source (`role:` / `fonte:`) |

## 5. The distinctions that decide a surface · `decision-grade`

### 5.1 Offline depth — the sharpest set of forfeits

Offline is not a yes/no property. Five distinct depths exist, and the requirement has to name one.

| Depth | Where it exists | What it forfeits |
|---|---|---|
| **None** | Any browser session — including a mobile browser — embedded surfaces, custom pages, the team-hosted surface, and code apps (undocumented) | — |
| **Read-only offline pages** | The low-code external-audience site, via the progressive-web-app setting; distributable through app stores | Pages carrying forms or queries do not work offline. The code-first site build model has **no** progressive-web-app setting |
| **Small local file cache** | Any canvas app over non-governed sources | A small memory envelope, **manual conflict resolution**, and no sync engine. Fragile by construction |
| **Full offline-first** | **Standalone** canvas apps over the **governed store only** | Not available in embedded canvas, custom pages, or canvas inside the collaboration client. **Non-governed connectors are not supported.** Virtual and elastic tables are not supported. **Workflow automation does not run offline.** Sync happens **only while the app is in the foreground with the screen unlocked**. Data-model restrictions apply: no many-to-many, single-level lookups, and caps on relationships and image columns per table |
| **Record-centric offline** | The record-centric app in the native player | **Field-level security and field sharing are not supported offline.** Personal views, store-wide search and duplicate detection are unsupported. Form web resources are unsupported on one mobile operating system. Grid column filtering is disabled whenever an offline profile exists — **even when connected** |

**The combination that has no answer on this platform: offline together with field-level
confidentiality.** It is documented as unsupported, not merely awkward. The consequences are structural —
either the confidential columns move out of the offline scope (data segregation, a data-model change), or
the offline requirement is dropped, or the surface leaves the platform. This is the single most expensive
surface forfeit in the corpus, and it lands in `security/security-controls.md` and
`data/store-boundaries.md`, not only here.

**Custom conflict rules, background or locked-screen sync, and multi-day offline queues are not documented
as extensible.** Treat them as unsupported until verified — that phrasing is deliberate: it is an
analyst reading of documented absence, not a vendor statement.

### 5.2 Freshness on an external-audience surface

The low-code external-audience site is served through a server-side cache. Changes made **through the
site** invalidate instantly; changes written by background automation or extension code are **never
guaranteed to be immediate**, and the documentation names presenting them as real-time as a design
approach it does not recommend. Manual cache clearing is documented as itself causing user-visible
performance problems.

The published cache service level is **15 minutes**. Where the requirement states a freshness window,
test it against that figure and record the reading.

> Documented reading · read 2026-09-04 · re-verify: VS-01 (Options, and before any freshness commitment)

### 5.3 Device capability

Device hardware pins the surface to a **native mobile player**, and sometimes to a specific one.

- Near-field reading is supported **only** in the native mobile applications — not in the authoring tool
  and not in a browser.
- Barcode reading is not supported in desktop browsers; the camera is not supported in a browser, and
  several device controls (address input, camera on mobile chat, map, mixed reality, report tile, web
  barcode scanner) are unsupported inside the chat-hosted surface.
- The Windows player lacks sensors, mixed reality and near-field reading. No retirement is documented for
  it, so this is a capability risk rather than a blocked path.
- **Custom pages support no device-capability controls at all**, and their mobile support is preview.
- A record-centric app in a **phone browser is unsupported** — a browser-first mobile programme and a
  record-centric surface collide directly.
- Mobile device and application management applies to the shared first-party player and can cover
  bring-your-own devices; **advanced management settings are not supported** with it. It is not a
  differentiator between canvas and record-centric apps; it differentiates the shared player from a
  branded wrap and from the browser.

### 5.4 Accessibility regime

- The **external-audience site** is platform-attested against the named international and public-sector
  standards — but the documentation is explicit that **customisation you add is your responsibility**.
- The **record-centric app** is accessible and responsive automatically.
- The **canvas app** is maker-dependent, with a documented set of patterns that cannot be made accessible
  at all — overlay dialogs and user interfaces above other content, and reacting to specific key presses —
  whose only documented escape hatch is a **code component**. The limitations page is old enough that it
  may overstate the gap against the current control generation; do not resolve that either way without a
  test.
- **No per-surface conformance report exists.** A legal claim about a maker-built application cannot be
  supported by citing the product's attestation. Where the regime is mandated, the accessibility path
  itself is a deliverable with an owner and an audit, whichever surface is chosen.

### 5.5 Localization and right-to-left

| Requirement | Where it is native | Where it is build effort | Where it is absent |
|---|---|---|---|
| More than two or three languages | Record-centric apps (installed language packs, export/import round-trip); the low-code external site (many out-of-the-box languages plus custom) | Canvas — a hand-built translation table, cost scaling as screens × languages | The code-first external site build model is **single-language** |
| Locale-sensitive formatting | Canvas and record-centric surfaces | — | Custom pages do not support user-locale formats |
| **Right-to-left** | Documented for custom pages, including automatic runtime mirroring — with icons, shapes and images excepted | — | **Standalone canvas: `UNKNOWN`.** No vendor statement exists either way. Treat as unsupported until verified by prototype; an earlier claim of explicit non-support was withdrawn as unsourced |

### 5.6 Distribution

- **Browser** — universal, and the only place the external-audience site lives.
- **First-party mobile players** — the route to device capability and to full offline; mobile management
  applies here.
- **Branded native wrapping** — canvas apps only, with the constraint set in §3, a monthly re-wrap
  obligation, and a conditional-access interaction that must be dry-run before commitment.
- **App-store distribution of a read-only site** — available through the progressive-web-app setting on the
  low-code site model.
- **Code app assets** — served from a public endpoint with **no address-based restriction**; the documented
  compensating control is conditional access, which is an identity control, not a network one. This
  matters in estates whose standing rule is address allow-listing.

### 5.7 Addressability and deep links

- The record-centric surface exposes **native addressable elements** — apps, forms, views and reports —
  and those links **cannot bypass security**; they are trimmed to the user's access.
- Canvas deep links are **hand-built per destination**: a parameter read at start, routed on the start
  screen, hydrated when the screen becomes visible. Cost scales with the number of link destinations.
- The **mobile deep-link contract has a dated breaking change**: links must carry an environment
  identifier, and links built without it stop working. Confirm the current contract before quoting any
  link inventory as durable.
- Where many shareable or bookmarkable record destinations are required, the addressability model — not
  the visual design — is the material distinction between surfaces.

## 6. What choosing a surface forfeits · `decision-grade`

The forfeit, not the feature list, is what a decision needs. Stated per choice:

| Choosing… | Forfeits |
|---|---|
| **Canvas** | Automatic responsiveness, automatic accessibility, native addressability, built-in multi-language, concurrent maker editing, and any external or anonymous audience |
| **Record-centric** | Visual control beyond colours/font/logo/header, phone-browser access, device capability inside custom pages, and — with an external system of record reached by virtualization — audit, row-level security, offline, guided processes, search and site solutions |
| **Custom pages on a record-centric shell** | Offline, device capability, mail-client embedding, retained page state, locale formats, and independent publishing (the host app pins the page version) |
| **Low-code external site** | Offline write, immediate reflection of background writes, caching for authenticated traffic, published throughput ceilings, and control of the server and cache layers |
| **Code-first external site** | Out-of-the-box lists and forms, the template language, multi-language, the offline-read setting, search discoverability, platform source control, and the low-code design workspaces |
| **Code app** | Address-restricted asset delivery, the Windows player, list-form integration, source-code lifecycle integration, standard-entitlement audiences, and (undocumented) offline |
| **Team-hosted surface** | Interface access, extension plug-ins, code components, record-centric apps, audit, column security and offline — and the reversibility of its own growth path |
| **Embedded surfaces** | Portability and solution management (list-customised form), sharing control (access follows list readers), immediate write-back and external report audiences (report visual) |
| **Branded wrapping** | Push notifications, consumer audiences, sovereign clouds, customer-managed keys and vendor-access approval — and a monthly redistribution cycle is acquired |
| **Custom development** | The connector estate, managed governance, configured row access, and included authentication, firewall and content delivery — each becomes a build and an operating item |

## 7. One-way choices and graduations · `decision-grade`

Some surface decisions cannot be undone, and some upgrades are one-directional. These belong on the
decision record as irreversibility statements, and in `alm/release-and-lifecycle.md`.

- **Team-scoped store → full governed store.** Growth past the team-scoped ceiling forces a graduation
  that unlocks interface access, plug-ins, offline and record-centric apps — and **no downgrade path is
  documented**. After it, every app in the environment requires standalone entitlement for its users, and
  the environment's capacity counts against the tenant pool. Cost the graduation at the point the
  team-scoped surface is chosen, not when the ceiling is hit.
- **Standalone canvas app → custom page.** No conversion exists. If the structured shell is a plausible
  two-year destination, the partition seams have to be designed before the first app is built; retrofitting
  is manual either way.
- **Component reuse with customisation allowed.** The association with the shared library is removed the
  moment a consuming app edits the component, and the local copy stops receiving updates — a
  **permanent fork**. Library updates are pull-based in the other direction: one shared fix means an
  edit-and-publish cycle in every consuming app.
- **Control-generation lock.** The current and previous control generations coexist; neither is retired.
  A property-and-behaviour revision of the current generation has already shipped once. Choose the
  generation per app on day one and record it; mixing or migrating later is unbudgeted rework.
- **Non-solution surfaces.** A list-customised form has no automated cross-environment copy and cannot be
  shared manually; a site's new components are **not automatically added to the solution**, and edits in a
  target environment create an unmanaged layer. The code-first site model and code apps have **no
  source-control integration**. Choosing these surfaces chooses their lifecycle.
- **Unmanaged-only capability.** The multisession record-centric experience can be enabled only in an
  unmanaged solution, which is incompatible with a managed-only-in-production rule. The choice is a
  governance exception or a different surface — and it is a standing exception, not a one-off.
- **Residency and region** are fixed at environment creation, upstream of every surface decision →
  `governance/governance-and-environments.md`.

## 8. Conversational and agentic surfaces — the boundary · `decision-grade`

**No surface knowledge exists here, and none may be invented.** The canonical position is that fit is
`UNKNOWN` in every option class, and that both the commercial model and the governance model for an agent
surface are unestablished: consumption depends on task complexity and is therefore unmodellable in
advance, and the agent-specific authentication and channel controls are preview.

Where the requirement is material, the correct output is **decision blocked** (`BS-03`), closed only by an
empirical bounded pilot plus a dated written governance position; the volatile facts sit on `VS-20`, with a
dated removal of a bundled entitlement (`TW-V2`). Do not produce a candidate set, a comparison, or a
capability claim for this surface class.

## 9. Failure modes · `decision-grade`

> **One artefact carrying several divergent persona experiences.** The documented remedy is partitioning,
> and both partition patterns cost something: separate apps lose state when one launches another, and the
> structured-shell route inherits the custom-page ceilings. Meanwhile the single artefact accumulates
> formula sprawl — the vendor's own root cause for authoring degradation, silently duplicated by
> copy-paste — while co-authoring removal makes it a one-maker bottleneck. Consequence: partition seams
> are a day-one design input, because the retrofit is manual.

> **A team-scoped surface grown toward its caps with no budget for the graduation.** The ceiling cannot be
> extended and the graduation is one-way; at the moment it fires, every user of the environment needs
> standalone entitlement. The failure is not the graduation — it is that the surface was chosen as
> "free" without the graduation priced.

> **An external-audience site fed by background automation and presented as real-time.** Only writes made
> through the site invalidate the cache; writes from automation or extension code are documented as never
> guaranteed to be immediate. The status a user sees is stale by design, and manual cache clearing to
> compensate degrades the site for everyone.

> **A non-solution surface treated as a portable, managed application.** A list-customised form cannot be
> shared manually and has no automated cross-environment copy; a report-embedded app is shared separately
> from the report and cannot return data to it. The surface works in one environment and has no promotion
> path — discovered at the first release, not at design time.

> **Branded wrapping chosen for a consumer audience or a push requirement.** Consumer applications are
> explicitly not supported by the wrap, and push notifications are unsupported inside it — while push
> exists only through the first-party players. `{branded application, push}` is unsatisfiable on this
> platform; the combination is a forced move off it, not a configuration problem.

> **An anonymous external surface exposed with unreviewed permissions.** A permission granted to the
> anonymous role makes the table's data visible to anyone, and open self-registration is on by default.
> The mechanism is configuration, so the failure is silent until discovered externally →
> `security/security-controls.md` owns the control set.

## 10. Consequences elsewhere · `decision-grade`

- **→ security.** Offline depth and field-level confidentiality are a documented mutual exclusion (§5.1);
  identity class decides which authentication and authorization planes are even in play (§4); the
  anonymous-surface permission review, the code-app public asset endpoint and its conditional-access
  substitute, and the treatment of visibility formulas — which are **client-side branching, never
  authorization** — all belong to `security/security-controls.md`. Access is governed by the acting
  connection identity and the store's own security, not by what the surface hides.
- **→ economics.** Audience and identity class drive the meter, not intensity of use: an external
  authenticated or anonymous audience is metered on **unique users**, with documented counting hazards in
  the metering unit; some surfaces require the premium entitlement for **every end user**; the team-scoped
  graduation converts a seeded population into a licensed one; and a partner guest's entitlement must be
  recognisable across tenants. `economics/licensing-and-cost-drivers.md` owns the units, drivers and
  populations.
- **→ operations.** The monthly re-wrap cycle is an operating commitment with an owner. There is **no
  first-party low-code test framework** — the previous one is deprecated and the documented migration is
  code-first browser automation — so long-lived, high-change surfaces need either that budget or an
  accepted manual regression cost. Each surface carries a different exposure to vendor-driven interface
  change, and every option needs a named change-absorption owner. `operations/operability-and-support.md`.
- **→ lifecycle.** Every item in §7 is an ALM fact as much as a surface fact: the one-way graduations, the
  absent conversion path, the permanent component fork, the pull-based library update labour, the
  unmanaged-only capability, and the surfaces with no source-control integration →
  `alm/release-and-lifecycle.md`.
- **→ data.** Full offline exists only over the governed store, and virtualizing an external system of
  record forfeits offline, audit, row security and site solutions — so an offline or record-centric surface
  requirement is also a store decision → `data/store-boundaries.md`. Query-shape and truncation questions
  belong to `data/query-and-delegation.md`.
- **→ performance.** **No concurrent-user ceiling is published for any surface.** What governs is the data
  path and per-identity request budgets, so a large-audience surface is a measurement obligation, not a
  documented capacity → `performance/performance-and-scale.md`.
- **→ governance.** Environment class, residency, managed-environment prerequisites and the licence chain
  they create → `governance/governance-and-environments.md`.

## 11. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Application-artefact composition ceilings — pages per app, connectors and connection references per app, guided-stage caps, embedded-report rows, wrapper bundle size, external-site structural thresholds | `VS-25` |
| Offline cache bounds — the offline record-set ceiling and the local file-cache envelope | `VS-38` |
| External-site cache floor and the surrounding freshness window | `VS-01` |
| Preview / general-availability state of the code-first site model, code apps, server-side site logic, the current control generation, and the mandatory interface refresh — plus the dated mobile deep-link contract change | `VC-10` |
| Connector and service permissibility per environment, for whichever connectors the surface needs | `VC-03` |
| Request rate per acting identity, for any large-audience surface | `VC-04` |
| Entitlement fit of the capability set the surface requires — including cross-tenant recognition for partner guests, and the entitlement treatment of the code-first site model, code apps, custom pages under app-scoped plans, wrapping and list-customised forms, all of which are **unresolved in the baseline** | `VC-05` |
| Audience and frequency shape, and the counting unit for external audiences | `VC-06` |
| Agent surface: request bucket, bundled entitlement with a dated removal, preview feature states | `VS-20` |
| Whether users without an appropriate licence are blocked from opening apps in a governed environment, and from which date | `TW-V3` |

## 12. What not to infer · `decision-grade`

**Not established in the baseline** — do not fill from general knowledge:

- **Any numeric size threshold for a canvas app.** No vendor limit on screens or controls exists. The
  vendor's own scale claim is inadmissible as capability evidence, and the community maintainability
  heuristic is not evidence either. **Encode neither.** What is admissible is the partition remedy and the
  team-and-persona conditions that trigger it.
- **Any concurrent-user ceiling for any surface** (§10).
- **Right-to-left support in standalone canvas apps** — `UNKNOWN`, in both directions.
- **Offline in code apps**, and code apps in the mobile players — undocumented; treat offline as
  unsupported until verified, and do not assert mobile reach.
- **A shared-device, kiosk or frontline identity mode**, and its licensing.
- **Published throughput, request-rate or concurrency ceilings for an external-audience site**, and its
  list and grid performance at volume — confirmed still open.
- **Push-notification throttling limits.**
- **The strict banner state** of the code-first site model and code apps — the fetched pages carry no
  preview wording, but a client-rendered banner cannot be ruled out.

**Boundaries of interpretation:**

- **A capability absence is not a verdict.** *"Custom pages support no device-capability controls"* is
  domain knowledge. *"Therefore this surface is inappropriate"* is a selection verdict and belongs to
  `decision-tree.md`.
- **There is no ranking of surfaces here, and no recommendation tree.** The escalation of visual control —
  platform controls, then composed components, then code components, then a code app, then custom
  development — is a map of **how far each mechanism reaches and what it obliges**, not an order of
  preference. A visual code component does **not** by itself make a standard-entitlement app premium; only
  a component calling external services directly, outside the connector layer, does.
- **A documented boundary here is not evidence that another option class performs better.** The baseline
  contains no like-for-like evaluation of any alternative surface stack, and no vendor decision guidance on
  the site-versus-custom boundary exists at all. Where the comparison is material,
  `decision-model/outcome-classes.md`'s comparator semantics stand.
- **Do not read an attested product conformance as an attestation of the application you build on it**
  (§5.4).
- The relative exposure of each surface to vendor-driven interface change is a **supported synthesis, not
  a vendor-endorsed ranking**; use it to require a change-absorption owner, never as a scoring input.

## 13. Where the delivery practice lives · `architecture-grade`

Screen typing, density, navigation shape, validation experience, state handling, the field-inventory to
screen-plan derivation and its naming and caps are **post-Options delivery practice**, not surface
capability: `craft/screen-patterns.md` and `craft/screen-consolidation-rules.md`, with formula-level
practice in `craft/powerfx.md`. Those files are never Options pull targets and state no platform limit —
where one is needed, they cite this file.

Reusable compositions of surfaces and mechanisms, and what each composition imports, are
`architecture/patterns.md`.
