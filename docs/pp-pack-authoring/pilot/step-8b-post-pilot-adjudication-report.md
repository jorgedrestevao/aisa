# Step 8B — Post-Pilot Evidence Adjudication & Repair Decision — pricing-marinha

> Not a pilot. Not pack authoring. Not a runtime repair. This report separates genuine generic framework
> defects from engagement-specific mistakes, reviewer assumptions, incomplete evidence and current platform
> facts, and decides whether pack 1.8.1 should change before a second pilot.

**Verdict: `STEP 8B — POST-PILOT EVIDENCE ADJUDICATION: PASS`** — the adjudication completed on evidence;
the runtime was not modified; the engagement artefacts were not modified. The adjudication itself found one
proven generic enforcement defect (PR-1), one documentation/contract drift (PR-2) and one engagement-practice
defect (PR-3). Full output block at the end.

---

## 1. Basis

| | |
|---|---|
| Baseline under adjudication | commit `78391d7ea00cc59c45b23ec65b384de8c812ab39`, branch `pp-pack-authoring/step-2-discovery-layer`, pack `pp` 1.8.1 |
| Runtime modified during adjudication | **NO** — `git diff --stat 78391d7 -- library/ .claude/` is empty; working tree holds only untracked docs |
| Engagement artefacts (`projects/pricing-marinha/**`) modified | **NO** — read only |
| Steps 3–7 reopened | **NO** |
| Pilot-1 documents modified | **YES — documentation only**: `step-8-real-engagement-pilot-report.md` (consistency corrections, §3 below) and `step-8-pilot-observation-log.md` (Step 8B adjudication notes appended; no historical entry erased) |
| Web research performed | **YES — one bounded commission** (§6), Microsoft Learn only, read 2026-09-05 |
| Model knowledge used to fill a gap | **NO** — every platform statement below carries a Microsoft Learn locator with its `ms.date`, or a pack RESEARCH unit section |
| Reviewer assertions treated as authority | **NO** — treated as evidence to investigate (§4, §7) |

Sources read for this adjudication (all read in full or at the cited sections): the two Pilot-1 documents;
`projects/pricing-marinha/` — `shared-understanding.md`, `answers.md`, `council-log.md`, `decisions.md`,
`options.md`, `frame.md`, `premortem.md`, `lens-outputs/*.md`, `lens-outputs/_council-prep/O-01-*.md`,
`_capture/process-model.md`, `_capture/evidence-index.md`, `_blueprint/blueprint-log.md`,
`_blueprint/ux-blueprint_v01..v05.yaml`, `_synthesis/architecture-story.md`, `_render/*_implementation-spec_v02.md`,
`_render/*_estimate_v02.md`, `_render/render-log.md`, `_render/render-gaps.md`; runtime contracts —
`library/kernel/states.md`, `library/kernel/orchestration.md`, `library/kernel/blueprint-contract.md`,
`.claude/skills/aisa-answer/SKILL.md`, `.claude/skills/aisa-blueprint/SKILL.md`, `.claude/skills/aisa-options/SKILL.md`,
`.claude/skills/chairman-synthesis/SKILL.md`, `.claude/skills/lens-technology/SKILL.md`, `.claude/agents/solution-architect.md`,
`library/packs/pp/pack.yaml`, `decision-tree.md` (§4, §11), `domain-knowledge/README.md`,
`architecture-templates/README.md` (§3–4), `architecture-core.md`; pack RESEARCH units —
`application/application-surfaces.md` (§1, §3, §5, §11, §12), `architecture/patterns.md` (§3, §5),
`data/dataverse.md` (§8, §9, §14), `data/store-boundaries.md` (§4, §7), `data/azure-sql.md` (§4, §5),
`security/security-controls.md` (§6); `docs/PROCESS_CAPTURE_SPEC.md`, `library/kernel/capture-templates/process-model.template.md`.

---

## 2. Preserved Pilot-1 history

```text
Pilot initially compiled as PASS (at P-OBS-026)
→ human reviewer found P-OBS-027 / P-OBS-028 / P-OBS-029
→ report revised to FAIL
→ Step 8B adjudication (this document)
```

Nothing above is rewritten. The Pilot-1 verdict stands as **FAIL**. The pilot did correctly demonstrate, and
these remain evidence in the pilot's favour:

- strong epistemic discipline in many other cases (U-007 held Unknown; U-025 held Unknown twice; U-010→A-006 and
  U-017→A-008 held at Assumed; `replacement_of_existing_artefact` not force-closed);
- no decision/architecture authority bypass (blueprint v01–v05 structured D-002, never re-decided it; render
  read the approved version twice rather than the more complete unapproved one);
- no scope leakage;
- selective Domain Knowledge pulls (2 in Options, both cited with section);
- no unnecessary stakeholder questions observed (33 asked, 0 judged avoidable);
- successful render-gap behaviour (5 gaps → 0 with one approval, no gap papered over);
- zero runtime edits during the pilot.

Also preserved as **valuable pilot evidence**: the live instrumentation logged the A-009→C-062 event
positively (P-OBS-014, "epistemic promotion held") and did not challenge the content of C-062. The pilot's own
review layer shares the failure mode it later documented.

---

## 3. Report consistency corrections (documentation only)

Applied to `step-8-real-engagement-pilot-report.md` on 2026-09-05. Historical result untouched.

| Location | Was | Now |
|---|---|---|
| §22 observation count | "Every one of the 26 observations" | "29 observations total — each a single data point" |
| Final evaluation Q3 | "Yes — no fabricated platform capability…" | "No. C-062 was accepted as Confirmed without sufficient technical verification and became architecture-significant. Whether its underlying mechanism is ultimately viable is subject to Step 8B technical adjudication." |
| Final evaluation Q14 | "None yet — every finding is a first data point" | "P-OBS-029 identifies a potentially generic runtime-control defect — architecture-significant platform claims may be settled without cited technical authority. Genericity and repair scope are being adjudicated in Step 8B. P-OBS-027/028 remain separate candidates." |
| Final evaluation Q15 | "Yes." | "No — not until Step 8B determines whether P-OBS-029 requires a bounded runtime repair." |
| §21 P-OBS-029 wording | "…materially incorrect technical claim… Model-driven (Dataverse-based) apps do not natively run against an external SQL Server as primary record authority." | "…unverified technical claim… C-062 asserted that existing/native connectivity was sufficient to confirm the record-centric/model-driven surface. That conclusion was not supported by an identified connectivity mechanism or by evidence that the mechanism satisfies the engagement's material data, security, audit, query and operability requirements." — with the earlier factual assertion explicitly withdrawn |
| §21 closing sentence, §23 verdict paragraph | "incorrect technical premise / materially incorrect technical claim" | "unverified load-bearing technical premise / unverified, load-bearing technical claim" |
| FINAL OUTPUT `UNSUPPORTED FACTS INVENTED` | "…model-driven apps do not natively run against external SQL Server as record authority" | "…no connectivity mechanism identified, no evidence that the mechanism satisfies the engagement's material data, security, audit, query and operability requirements; mechanism viability adjudicated in Step 8B" |
| FINAL OUTPUT `DECISION REMAINS DEFENSIBLE` | "…rests on an incorrect technical premise" | "…rests on an unverified load-bearing technical claim (C-062); the data-access mechanism and experience-surface choice must be re-examined (Step 8B)…" |
| FINAL OUTPUT preamble | — | one added paragraph recording that Step 8B corrections were applied and the FAIL verdict is unchanged |

`step-8-pilot-observation-log.md`: Step 8B adjudication notes appended under P-OBS-027, P-OBS-028 and P-OBS-029
and a post-8B block appended after the revised severity table. No entry deleted or reworded.

---

## 4. P-OBS-029 provenance trace — how C-062 became Confirmed

### 4.1 The chain, reconstructed from the artefacts

| Step | Artefact | What happened | Who / what asserted |
|---|---|---|---|
| 0 | `answers.md` → U-029, blueprint v01 | Sponsor, asked who owns the integrations, answers (verbatim, typos preserved): *"essas ligações externas vao desaparecer, o feed de mercado já eiste num base de dados relacional em sql server usada para outros processso de pricing (ex:espanha) e vai ser utilizada tambe para este. tudo o que é ricing fica nessa base de dados."* → **C-057** (Confirmed, USER_ANSWER). | human (sponsor) — engagement fact |
| 1 | SU row **A-009** (lens `chair`, section **Assumed**) | *"Tensão estrutural nova: o desenho de referência 'Record-centric app (model-driven)' do blueprint v01 assume dados no store nativo governado da plataforma; C-057 move a autoridade de dados para uma BD SQL Server externa — pode exigir Canvas app (qualquer conector) ou um desenho híbrido (store nativo só para o workflow de aprovação/auditoria)."* Base: *"inferido do cruzamento entre C-057 e application-surfaces.md §3 … proposto pelo chairman ao rever o blueprint v01, sem segundo anchor de persona."* | blueprint executor (chairman role) — a correct structural question, one DK anchor (`application-surfaces.md §3`) |
| 2 | `ux-blueprint_v02.yaml#open_architecture_choices` | `choice`: surface compatible with external SQL master data — Canvas vs Record-centric vs hybrid. `structural: true`. **`would_be_settled_by: "Confirmar com IT se a BD SQL Server partilhada é acessível via conector nativo da plataforma, e decidir a superfície com base nisso"`**. `su_ref: A-009`. | blueprint executor — **this is where the settling fact was defined as a connectivity fact** |
| 3 | `answers.md` → "A-009 — superfície primária vs BD externa" | **Resposta (verbatim): "Sim, já há ligação/gateway configurado."** Fonte: sponsor (Pedro O.), not IT. | human (sponsor) — a yes/no about a configured connection/gateway |
| 4 | `/answer` → SU row **C-062** (Confirmed, lens `chair`, `validade: plataforma-tecnica`) | Claim as written: *"Já existe ligação/gateway configurado que permite a ferramentas low-code/Power Platform aceder à BD SQL Server partilhada de pricing (C-057) — **a conectividade nativa não é um obstáculo**."* Evidence: `USER_ANSWER 2026-09-05 — sponsor (Blueprint v02, resolve A-009)`. `answers.md` transition note: *"conectividade nativa já existe; a escolha de superfície deixa de estar bloqueada pela localização externa dos dados."* | `/answer` execution — the extracted claim **adds** an interpretive clause the sponsor did not say |
| 5 | `ux-blueprint_v03.yaml#experience` + `blueprint-log.md` v03 | `primary_surface: "Record-centric app (model-driven)"`; rationale: *"já existe ligação/gateway configurado … (C-062) — a conectividade nativa (relacional via conector) **sustenta o Record-centric app (model-driven) sem necessidade de mudar para Canvas app. Superfície confirmada**."* Structural blocker removed. `record_authority` stays `external system of record / keep-in-place`; composition `shared-pricing-sql-server` stays `pattern: direct`. No DK pull recorded for v03. | blueprint executor — **second inference: connectivity → surface fit**, no mechanism named |
| 6 | D-003 (v04), D-004 (v05), `/synthesize`, `/render --all` ×2 | Surface, record authority and composition carried unchanged into the approved blueprint, architecture-story, Implementation Spec v02, Estimate v02 (44–49 person-days; the estimate itself flags the "Model-driven app screen (Dataverse)" band as an analogy for "store externo virtualizado, não Dataverse nativo"). | downstream layers read, did not re-decide — correct behaviour over an unsound input |

### 4.2 Classification of what was asserted

| Component of C-062 as used | Source class | Evidence attached | Grade the evidence actually supports |
|---|---|---|---|
| "a connection/gateway to the shared SQL Server is configured" | **human assertion** (sponsor; the `would_be_settled_by` named IT as respondent) | USER_ANSWER | Confirmed **as an engagement fact reported by the sponsor**; strictly, a second-hand statement about IT configuration — `aisa-answer` rule 3 would allow Assumed-with-basis as the conservative reading |
| "native connectivity is not an obstacle" | **runtime inference** written into the claim text at step 4 | none | not supported by the answer — inference |
| "connectivity sustains the model-driven surface; surface confirmed; Canvas not needed" | **blueprint inference** at step 5 | C-062 (which does not say this) | not supported — no mechanism identified (virtual table? replication? connector from a canvas/custom page?), no DK section, no external technical evidence |
| source-document fact / Domain Knowledge evidence / external technical evidence | — | **none** at steps 3–5 | — |

### 4.3 The exact transition point

```text
technical proposition ("model-driven surface fits an externally-authoritative SQL Server")
    → became Confirmed at step 4 (/answer A-009 → C-062), by (a) applying the default
      "direct sponsor statement → Confirmed" inference to a yes/no about connectivity, and
      (b) writing an interpretive clause into the extracted claim;
    → became architecture-authoritative at step 5 (blueprint v03), when the structural
      open choice was marked resolved on the strength of C-062 alone, with no mechanism
      named and no Domain Knowledge pull.
```

Two runtime components accepted it: **`aisa-answer`** (transition engine, step 4) and **`aisa-blueprint`**
(closure of a structural `open_architecture_choices` entry, step 5). No hook, gate or checklist sits between
"structural choice resolved" and "approval" that inspects *how* the choice was settled.

Contributing slip: A-009 was recorded in the **Assumed** section although its content is an open structural
question. `aisa-blueprint` step 11 says a new unknown emerging in architecture is appended as a `U-NNN` row and
referenced by `su_ref`. Recording it as `A-` made the `Assumed → Confirmed` ("validation of the assumption",
`states.md`) path available to a sponsor "yes" — and the answer did not validate the assumption's proposition,
it answered a narrower question sideways.

---

## 5. Existing-runtime guard audit — was C-062 already forbidden under 1.8.1 as written?

| # | Rule (frozen, as written) | Where | Bears on C-062? | Complied? |
|---|---|---|---|---|
| G1 | *Confirmed* = "Verified by direct evidence or sponsor"; transitions: `Assumed → Confirmed` = **"Validation done"** (validation of *the assumption*) | `library/kernel/states.md` | Yes — the sponsor answer did not validate A-009's proposition | **No** — used as if it did |
| G2 | "**Verbatim in, structured out.** … the SU row carries the extracted fact." Step 4: claim = "the answered fact (specifics preserved)" | `aisa-answer` hard rule 1, step 4 | Yes — the claim text added "a conectividade nativa não é um obstáculo" | **No** |
| G3 | "**No silent upgrades**: an answer that is hearsay or inference goes to Assumed with the basis declared, not Confirmed — even if the user typed it confidently." | `aisa-answer` hard rule 3 | Yes — the fit conclusion is inference; the gateway statement is at best second-hand | **No** |
| G4 | "A lens must not claim stronger evidential support than the evidence it actually inspected supports. Weaker support → Assumed with the basis declared, or Unknown." | `library/kernel/orchestration.md` → Evidence contract | Yes — applies to the executor writing the v03 rationale | **No** |
| G5 | "Every Confirmed row must have ≥2 persona anchors OR a direct document/sponsor citation." | `chairman-synthesis` hard rule 3 | Partly — the gateway statement has a sponsor citation; the fit conclusion has none | Satisfied only for the part the sponsor said |
| G6 | Domain Knowledge pull rule: "architecture responsibility being described → pull ONE relevant knowledge unit … For an engaged composition the pull is `architecture/patterns.md` §3 plus **the one** engaged pattern in §5". `record_authority.access_mode ∈ {owned, virtualized, replicated, keep-in-place}`; `compositions.pattern ∈ {direct … data-virtualization, data-replication …}` | `aisa-blueprint` → Domain Knowledge pull rules; step 2 schema | Yes — describing a model-driven surface over an external store *is* describing either `data-virtualization` or `data-replication`; the unit was not pulled, and the recorded triple `external system of record / keep-in-place / direct` + model-driven is incoherent under the pack's own §5 (Data virtualization: "Native experience: model-driven surfaces, views, forms and lookups work over it" is a property of **virtual tables**, not of a connector call) | **No** — no DK pull recorded for v02/v03 |
| G7 | CRAFT boundary: "RESEARCH establishes the technical boundary … CRAFT may not … establish a platform capability". "No platform numbers": "where no verified row exists, carry the **verification obligation** instead" | `aisa-blueprint` | Yes — a platform-capability proposition was established by the executor without a RESEARCH citation | **No** |
| G8 | "Where a volatile fact is decision-critical and sufficiently current evidence is unavailable, create a verification obligation: an Unknown (`custo: documento|spike`, `swing: decisivo`) … **do not treat the affected conclusion as settled**." | `decision-tree.md` §11; `volatility-register.md` §0 | Yes by analogy — platform capability is the `plataforma-tecnica` decay class the row itself carries | **No** — the conclusion was treated as settled |
| G9 | "`Unknown` is never filled — it becomes an `open_architecture_choices` entry"; a `structural: true` entry blocks approval | `architecture-core.md` render contract; `blueprint-contract.md` hard rule 5 | Yes — the structural entry existed and correctly blocked v02; it was then filled by an answer to a different question | Mechanism worked at v02, was defeated at v03 |
| G10 | The very DK unit A-009 cited: Record-centric app "**Requires a data model in the governed store — there is no such app without it.**" Canvas: "over any connector". | `application-surfaces.md` §3 | Yes — the unit that opened the question also says what would close it: a data model in the governed store (which, over external SQL, means virtual tables or replication) | Read at v02, **not re-read** at v03 |
| G11 | Pack RESEARCH already documents the exact mechanism and its forfeits: `dataverse.md` §14 (virtual tables — no row/column security, no audit, one shared credential, 1:N side, "narrow, positively-filtered, small, read-mostly … mandatory measured spike"); `patterns.md` §5 Data virtualization / Data replication; `store-boundaries.md` §7; `security-controls.md` §6.3 | pack DK, frozen at 1.8.1 | Yes — one pull would have shown that "connectivity" is not the settling fact | **Not pulled** |

**Result: Case A.** Under pack 1.8.1 *as actually written*, C-062-as-used was already forbidden from becoming
Confirmed and from closing the structural choice: G1–G4, G6–G8 each independently required either an
Assumed-with-basis, an Unknown/verification obligation, or a DK pull naming the mechanism. The knowledge to
answer A-009 correctly was **inside the frozen pack** (G10–G11).

Therefore **P-OBS-029 is a runtime execution/compliance defect, not a missing semantic principle.** What is
missing is **enforcement/testability at one closure point**: nothing forces the executor, when a structural
`open_architecture_choices` entry is resolved, to check (a) that the resolving answer settles the fact named in
`would_be_settled_by`, (b) that the extracted claim does not exceed the verbatim answer, and (c) that any
platform-capability proposition carried by the closure has a RESEARCH / engagement-verifiable / measured basis.
The principles exist in four files; the check exists in none. Repair scope (§16) is therefore: strengthen the
existing guard at that point — no new principle, state, ledger, router or matrix.

---

## 6. Technical research commission — C-062 mechanism (bounded)

Scope: RQ-1..RQ-4 only. Authority: Microsoft Learn, read 2026-09-05. Each statement carries the page and its
`ms.date`. Pack RESEARCH units are cited where they already hold the same fact, to show the knowledge was
available at pilot time.

| Ref | Page | `ms.date` |
|---|---|---|
| L1 | [Create and edit virtual tables with Microsoft Dataverse](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-virtual-entities) | 2026-04-17 |
| L2 | [Create virtual tables using virtual connectors in Microsoft Dataverse](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-virtual-tables-using-connectors) | 2026-05-07 |
| L3 | [Get started with virtual tables (developer)](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/virtual-entities/get-started-ve) | 2026-01-07 |
| L4 | [Limitations and troubleshooting virtual tables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/limits-tshoot-virtual-tables) | 2026-05-15 |
| L5 | [Setting up relationships with virtual tables](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/setup-virtual-table-relationships) | 2026-05-15 |
| L6 | [Overview of building a model-driven app](https://learn.microsoft.com/en-us/power-apps/maker/model-driven-apps/model-driven-app-overview) | 2026-01-09 |
| L7 | [What is an on-premises data gateway?](https://learn.microsoft.com/en-us/data-integration/gateway/service-gateway-onprem) | 2025-06-10 (updated 2026-01-16) |
| L8 | [Create and use dataflows in Power Apps](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-and-use-dataflows) | 2026-01-09 |
| L9 | [SQL Server connector reference](https://learn.microsoft.com/en-us/connectors/sql/) | 2024-03-01 (updated 2026-07-11) |

### RQ-1 — Can a model-driven app expose and operate data whose system of record remains SQL Server?

**Yes, via Dataverse virtual tables.** L6: model-driven apps' data platform is *"Dataverse only"*; *"without a
data model housed within Microsoft Dataverse, you can't create a model-driven app."* L1: *"A virtual table is a
custom table in Microsoft Dataverse that has columns containing data from an external data source … Rows based
on virtual tables are available in all clients."* L2: *"Solutions, apps, flows, and more can use virtual tables
as if they were native Dataverse tables. Virtual tables allow for full create, read, update, and delete
privileges unless the data source they're connecting to specifically forbids it."* SQL Server is a listed
virtual connector provider (L2), including on-premises deployments via gateway (L2: *"gateway (on-premises
deployments only)"*).

```text
external SQL authority  ≠  automatic model-driven disqualifier
```

The reviewer's original formulation ("model-driven apps do not natively run against an external SQL Server as
primary record authority") is **not** supportable as stated and is withdrawn (§3). The Dataverse data model is
still required — the virtual table *is* that model, without replication.

### RQ-2 — Supported mechanisms

| Mechanism | What it is | Status / notes |
|---|---|---|
| **M1 — Dataverse virtual tables, SQL Server virtual connector provider** | Metadata table in Dataverse; rows fetched from SQL at runtime; CRUD; connection + connection reference; ALM-supported in managed solutions; environment variables supported for SQL (L2) | GA for SQL Server (Fabric/Salesforce/Oracle are preview, L2). Pack: `patterns.md` §5 *Data virtualization*, `dataverse.md` §14 |
| **M2 — Replication into Dataverse** | Standard dataflow (Power Query) loads SQL data into Dataverse tables on a schedule ("30-minute increments", one owner, one-way source→Dataverse, L8); or a built bidirectional sync (event path + bulk path + reconciliation — pack `patterns.md` §5 *Data replication*) | Copy exists in Dataverse → full platform data features on the copy; two truths in the window (pack §5) |
| **M3 — Custom virtual table data provider** | Plug-ins implementing CRUD against the external API (L3) | Code; same virtual-table limitation set (L3) |
| **M4 — Non-model-driven access (context only)** | Canvas app / custom page / flow over the SQL Server connector directly (L9; pack `azure-sql.md` §3–5, `application-surfaces.md` §3 Canvas "over any connector") | Not a model-driven surface; a hybrid (record-centric backbone + custom pages) is the pack's documented convergence vehicle (`application-surfaces.md` §3) |
| **Transport — on-premises data gateway** | Locally installed bridge, outbound-only; used by Power Apps, Power Automate, Dataverse virtual tables (via connector), dataflows (L7) | A **transport prerequisite** for several of M1/M2/M4 when SQL Server is on-premises; 2 MB request / 8 MB response caps; credential cache ≈5 h; 1,000 data sources per cluster (L7) |

### RQ-3 — Limitations of virtual tables over SQL Server that bear on this engagement

| Dimension | Documented fact (locator) | Pack unit already stating it |
|---|---|---|
| CRUD | Full CRUD unless the source forbids (L2). **SQL views → read-only** (L4). **"Insert and update to a table won't work if you defined a SQL server-side trigger on the table"** (L9; L4 defers to L9) | `store-boundaries.md` §4: "server-side triggers break connector writes" |
| Primary key | *"SQL virtual tables use a GUID or an integer field as the primary key"*; string PK only if parseable as GUID; table without PK: only `RetrieveMultiple` works; a non-PK **string field is required as primary name** (L4). GUID mapping is "a specific and required mapping" (L3) | `patterns.md` §5: "a globally-unique primary key per table" |
| Row-level security | *"Virtual tables are organization owned and don't support the row-level Dataverse security concepts. We recommend that you implement your own security model for the external data source."* (L1) *"Only organization-owned tables are supported. The security filtering applied to user-owned tables isn't supported."* (L3). Access on/off per security role, incl. per-privilege (L2) | `dataverse.md` §14; `security-controls.md` §6.3 |
| Connection identity | *"These will be the credentials used for all authentication for the virtual table"* (L2, SQL tab) — one stored credential for every user | `dataverse.md` §14: "one shared credential for all users"; `security-controls.md` §6.1 identity collapse (authorization, **attribution**, throughput) |
| Field-level security | *"Field-level security isn't supported."* (L3); column security cannot be enabled (L1) | `dataverse.md` §8: virtual-table columns "Not securable" |
| Auditing | *"Virtual tables don't support auditing."* (L1); *"Audit functionality isn't available for virtual tables because Dataverse can only perform and store audit data for locally stored data."* (L4) | `dataverse.md` §14; `patterns.md` §5 |
| Relationships | 1:N, N:1 and polymorphic supported between local and virtual tables and virtual↔virtual of the same provider; **a virtual table can't be on the 1 side of a 1:N**; relationships are defined manually; a lookup to a virtual table can be shown on a grid but **not filtered or sorted** (L5, L3, L4) | `dataverse.md` §14 |
| Calculations / rollups / formulas | *"Rollups and calculated fields can't be calculated for virtual tables"*; *"Formula columns can't use virtual tables"* (L4); *"Any desired calculations must be done on the external side"* (L3). No business rules validation-on-update semantics (L1). **No business process flows** (L1) | `patterns.md` §5 |
| Charts / dashboards / search / offline | *"Dashboards and charts are not supported with virtual tables"*; no Dataverse search; no mobile offline; no duplicate detection; no change tracking (L1, L3) | `dataverse.md` §14 |
| Query / result limits | *"Virtual table queries are limited to returning 1,000 records"* — with a 1:N or polymorphic relationship a query exceeding it **fails with an error**; negative filter operators break paging past page 1, *"no supported workaround"*; all attributes always returned; text columns capped at 4,000 chars; `bigint` → decimal; `time`, `datetime2`, `image`, `geometry`, `rowversion` columns excluded (L4, L3) | `dataverse.md` §14; `store-boundaries.md` §7 (absent from delegable-source list) |
| Import/export | *"Import and export functionality of table data isn't supported for virtual tables."* (L4) | — |
| ALM | Supported; virtual tables + connection reference in a managed solution; environment variables for SQL/SharePoint (L2). Only connections **created by the current user** appear in the wizard (L2). Recreating a connection requires re-sharing it with the Virtual Connector Provider app (L4) | `patterns.md` §5 (connection rebinding) |
| Operability | Provider solution updates from Marketplace (L4); gateway estate when on-premises (L7); `Execute a SQL query` not supported through the gateway (L9); credential cache ≈5 h (L7) | `azure-sql.md` §11 (gateway estate as operating model); `integration-mechanisms.md` §5 |
| Entitlement | *"To create a virtual table, you must have a Microsoft Dataverse license through Power Apps or Microsoft Dynamics 365. Microsoft 365 or Teams licenses can't be used."* (L2) | `economics/licensing-and-cost-drivers.md` (not re-read here) |
| Performance | No published latency/throughput/caching characterisation at any volume — a documented absence | `dataverse.md` §14: "mandatory measured spike before commitment" |

### RQ-4 — Does "connectivity already configured" prove the model-driven surface is fit?

**No.**

```text
connectivity exists  ≠  solution fit proven
```

A configured connection/gateway is a transport prerequisite shared by M1, M2 and M4 (L7). It determines
**none** of: which mechanism is used; whether the shared DB's tables carry a GUID/integer primary key and a
string primary name (L4); whether written tables carry server-side triggers (L9); whether audit, row/column
security, dashboards, search or calculations required by the engagement are available on virtual data (L1, L3,
L4); whether the 1,000-record cap and paging behaviour fit the query shapes (L4); whose identity reaches SQL
(L2); or what the gateway estate obliges operationally (L7). The pack's own RESEARCH units said the same at
pilot time (`dataverse.md` §14, `store-boundaries.md` §7, `security-controls.md` §6.3).

---

## 7. SQL / Dataverse mechanism findings — what C-062 should have said

The honest, evidence-grade reformulation of the resolution of A-009 is:

> A connection/gateway between Power Platform and the shared pricing SQL Server is reported by the sponsor as
> configured (engagement fact, second-hand from a business sponsor — Assumed until IT confirms the mechanism
> and identity). A model-driven surface over that store is **possible** through Dataverse virtual tables (SQL
> virtual connector provider) or through replication into Dataverse. **Which** mechanism, **per data domain**,
> and whether the mechanism's documented exclusions (no audit, no row/column security, one shared credential,
> 1,000-record query cap, no dashboards/charts, no calculated columns, PK/trigger constraints on the shared
> schema) defeat any material requirement, is the structural question — and it remains **open** until each
> domain is assigned a mechanism against those exclusions and the shared schema is verified.

Under the pack's vocabulary the coherent recordings would have been `access_mode: virtualized` +
`pattern: data-virtualization` (per domain where the exclusion list is acceptable) or `access_mode: replicated`
+ `pattern: data-replication` (per domain needing audit/row security/analytics), never
`keep-in-place` + `direct` under a model-driven surface.

---

## 8. O-004 claimed strengths — re-adjudication under the actual data-access mechanism

The Options record (`options.md#O-004`) anchored O-004 on `dataverse.md §8-9` and `patterns.md §5` and stated
these strengths. They were true of a *Dataverse-owned* store (blueprint v01). C-057 moved authority to external
SQL; v03 kept the surface and never re-tested the strengths. Under the only mechanism consistent with the
recorded architecture (virtual tables):

| Claimed strength (options.md#O-004) | Verdict | Evidence |
|---|---|---|
| "segurança nativa por linha/coluna" (native row/column security) | **DOES NOT APPLY** | Virtual tables are organization-owned, no row-level security, no column security (L1, L3); one stored credential for all users (L2) → store-side SQL row-level security also collapses (`azure-sql.md` §4–5, `security-controls.md` §6.1). Would apply only to a **replicated** Dataverse copy, or to SQL with a per-user directory identity end-to-end — neither is recorded |
| "auditoria nativa" (native audit trail) | **DOES NOT APPLY** | "Virtual tables don't support auditing" (L1); "Dataverse can only perform and store audit data for locally stored data" (L4). Audit must be built SQL-side (temporal tables / audit columns — note **triggers break connector writes**, L9) or the audited domain must live in Dataverse. The Estimate v02 already carries "colunas de auditoria (6 entidades)" as SQL work — an implicit acknowledgement that contradicts the "native audit" strength |
| "o padrão de integração directa cobre a forma da carga de trabalho sobre SAP/X-ALT" (direct integration pattern covers the workload) | **APPLIES WITH LIMITATION** | Applies to `sap-term-pricing-reference` (one consumer, low volume, read-only — `patterns.md` §5 *Direct*). X-Author integration was removed (C-065). **Does not describe the SQL data layer** under a model-driven surface: that composition is `data-virtualization` (or `data-replication`), not `direct`; the blueprint mis-patterns it |
| "passo de aprovação do comité … encaixa num passo de aprovação nativo da plataforma" (committee approval fits a native approval step) | **UNKNOWN** | Business process flows and Dataverse-native validation semantics are unavailable on virtual tables (L1). An approval can still be driven by Power Automate (SQL connector triggers "When an item is modified (V2)", L9) or by a Dataverse-owned approval table; not designed, not recorded |
| "o desenho de dados-mestre já pode arrancar com SAP como fonte de verdade confirmada" | **APPLIES** | Independent of the access mechanism (C-052) |

The two strengths that carried R-005 (self-reviewed control) and R-006 (informal master-data ownership) —
the frame's auditability clause — **do not survive the mechanism as recorded**. This is more consequential than
the abstract "Canvas vs model-driven" question.

---

## 9. A-009 verdict

> **Step 8C correction (2026-09-05, applied before the runtime repair).** The verdict below conflated two
> different findings. The research (§6) identified **candidate** mechanisms (M1–M4) through which a
> record-centric surface *can* be defensible over an externally-authoritative SQL Server, with
> preconditions. The **engagement** never established *which* mechanism is actually used, per data domain,
> nor its fit against the material controls. `candidate mechanism exists` ≠ `engagement mechanism
> established`. The adjudication therefore records: `SPECIFIC SQL ACCESS MECHANISM IDENTIFIED: NO` ·
> `MODEL-DRIVEN + EXTERNAL SQL CAN BE DEFENSIBLE WITH PRECONDITIONS: YES` · `A-009 FINAL STATUS: UNKNOWN`.
> The original wording is preserved below as history; the requirement table and the flip conditions remain
> valid as the **preconditions** the targeted architecture revisit must verify. See §20a.

**A-009 FINAL STATUS (as first written): DEFENSIBLE WITH PRECONDITIONS** — and **NOT DEFENSIBLE as currently specified**
(`direct` + `keep-in-place` + model-driven, with "native security/audit inherited from the store" as rationale).
**Corrected status: UNKNOWN** — defensibility is *possible* with preconditions (research), *unestablished* for this engagement (no mechanism per domain recorded).

Evaluation against the engagement's actual requirements (no score):

| Requirement | Source | Under virtual tables (M1) | Under replication (M2) for that domain | Precondition / verification obligation |
|---|---|---|---|---|
| **Row/column authorization** | Roles differ by *action* (Analista edits; Comité reviews; Superior approves; Dono approves master data — v01 personas); classification **Interno** (C-036); no hard row-subset requirement recorded; `excluded_from_ui` hides internal calc columns (UI, not server-side) | Table-level per role only; no row/column security; all users reach SQL as one principal | Full Dataverse grain on the copy | **VERIFY**: is any row-subset or server-side column confidentiality a *hard* requirement? If yes → M2 for that domain or per-user SQL identity; if no → M1 acceptable with app-level role visibility declared as *not authorization* (`azure-sql.md` §4) |
| **Audit / evidence** | Options concern "qualquer opção tem de desenhar um trilho de auditoria real"; D-002 condition "auditoria/SoD/escada de sign-off desenhados de raiz"; R-005; C-043 auditable approval; C-060 10-year retention of price history | **Not available** natively; SQL-side audit needed; triggers break writes → temporal tables or a write path outside the virtual table | Native audit on the copy (retention set at environment creation, `dataverse.md` §9) | **PRECONDITION**: choose the audit mechanism per domain explicitly — the approval/audit domain is the natural candidate for Dataverse ownership (the hybrid A-009 itself proposed); the DB owner must accept temporal tables/audit design on shared tables |
| **Calculation shape** | 59 derived output columns via INDEX/MATCH over `Data_Lista`; `INDIRECT`-built per-port lookups; 6 duplicated copies; model-style `Base DFA/RF` (PM-002/003/005/007) | No calculated/rollup/formula columns → calc lives in SQL (views/procedures); SQL views as virtual tables are read-only — suits `PrecoDiarioConsolidado`/`HistoricoPrecos` (read-only entities in v01) | Same: calc in SQL or Dataverse plug-ins | **VERIFY** with the DB owner where the calculation engine lives (it is "tudo o que é pricing" per C-057) — a calc-layer design decision, not a surface decision (§11) |
| **What-if / Monday–Tuesday estimation** | Sponsor's literal ask #2; `Simulador` sheet = editable what-if copy (PM-003); PM-U-002/003 never asked | Model-driven forms over virtual data cannot compute interactively; needs a custom page/canvas or calc-on-save | Same | **VERIFY** (P-OBS-028 territory): is an interactive estimation task in scope for the pricing team? Not recorded in SU |
| **Write semantics** | Approval state machine pendente→aprovado→carregado (v01 `AprovacaoCarregamento`); daily entry of ~85 manual values (PM-001) | CRUD via virtual table if PK is GUID/int, no triggers, string primary name exists; no BPF; validation-on-update metadata not applied | Native | **PRECONDITION**: schema conformance of every written table (PK type, primary name, no triggers) — currently `o_que_nao_se_sabe` in the blueprint |
| **Query volume** | Quote history rows 9–1469 (≈1,460 rows, A-003/A-006); two **dashboard** screens in v01 | 1,000-record query cap; dashboards/charts not supported on virtual tables; negative filters break paging | No cap of that kind on the copy | **MEASURE**: the pack's own "mandatory measured spike" (`dataverse.md` §14); redesign the two dashboard screens as views/custom pages or over replicated data |
| **Integration** | SAP read reference (C-003); Excel export (C-065) | SAP: `direct`, unchanged. Export: table import/export unsupported on virtual tables → export is a flow (Estimate v02 already has one) | — | none new |
| **Operational ownership** | Shared DB operated by another team (C-057); IT central operates integrations (C-063); pricing team owns the app (C-068) | Virtual-table definitions, connection reference and provider updates are the app team's; connection owned by one maker; gateway estate if on-premises (unknown) | Dataflow has a single owner; reconciliation owner needed (`patterns.md` §5) | **VERIFY**: on-premises vs Azure SQL (the sponsor said "gateway"); who owns the connection identity and its rotation; who owns reconciliation if M2 |
| **Migration** | Key cleanup before first migration (C-019, D-002 condition); 6-sheet consolidation with `Outputs` authoritative (C-059) | Migration is into **SQL** (the DB team's schema), not into Dataverse | Initial load + reconciliation pass | **VERIFY**: the DB team's acceptance of the pricing schema and its change control (shared with Spain) |
| **Supportability** | 2 environments, no formal test tier (C-067) | Provider solution updates; connection re-share after recreate; environment variables for ALM | Dataflow re-binding after deployment | none blocking |

Which preconditions could flip the verdict to **NOT DEFENSIBLE**: a hard row/column confidentiality
requirement with no Dataverse-owned domain permitted; the DB owner refusing GUID/integer keys or temporal tables
on shared tables; or a measured spike failing on the ≈1,460-row history and its filters. Which could flip it
toward a stronger **DEFENSIBLE**: IT confirming a per-user (Entra) identity path, and the approval/audit domain
being accepted as Dataverse-owned (consistent with C-057 if pricing *data* authority stays in SQL and only
workflow/audit state lives in Dataverse).

This verdict does **not** say "Canvas wins" (§9 of the brief). It says the record-centric surface is not
disqualified by external SQL authority, and that its defensibility depends on a mechanism-per-domain decision
that the engagement never made.

---

## 10. P-OBS-028 adjudication — Canvas presumption removed; was the interaction shape evaluated?

**Presumption removed.** "High customization → Canvas should win" is not a rule of this pack and is not used
here (`application-surfaces.md` §12: no ranking, no size threshold; §6 of `domain-knowledge/README.md`:
domain knowledge never chooses the winner). Six calculation sheets and 291 named ranges are **calculation
complexity**, not evidence about the user interface (§11 below).

**The valid question**: did the experience-surface selection explicitly evaluate the process's
interaction/customization shape? What v01 recorded as rationale: *"Audiência inteiramente interna …; trabalho
denso em dados, centrado em registos, com navegação relacional automática, segurança por linha/coluna e auditoria
herdada do store — exactamente a forma que dataverse.md §8-9 descreve."* — i.e. **identity class, data
density, relational navigation, and store-inherited controls**. The pack's own inputs to a surface question are
*"who the users are in identity terms, on what device, connected or not, under which accessibility and language
regime, and how they arrive at a record"* (`application-surfaces.md` §1), and §3 distinguishes Canvas
("task-focused internal experience … pixel-level layout control") from Record-centric ("data-dense,
record-centric, process-driven work"). The Discovery cues `work_shape_class` (operations) and
`interaction_bespokeness_and_design_obligation` (user) exist in `pack.yaml`.

| Interaction signal | Evidence available at v01 | Evaluated in surface selection? |
|---|---|---|
| Number and shape of user tasks | Daily cycle: enter quotes → compute → committee decides margin → approve → load → e-mail (C-005, C-006, C-013, C-026, PM-001, Fluxograma) | **Partly** — personas and screens derived; the *task shape* of the daily entry (wide grid, ~85 values, PM-001) not discussed |
| Density of calculations visible to users | 59 derived output columns; comparison across 6 copies; `Base DFA/RF` (PM-002/003/007; C-041) | **No** — treated as an implementation concern (`excluded_from_ui`: "Detalhe interno de fórmulas"); whether users *see and interact with* computed columns was not asked |
| Cross-record interactions | `INDIRECT` lookups across counterparty × fuel × port; date-keyed history (PM-002, PM-005) | **No** |
| Simulation / what-if | `Simulador` = "editable what-if copy" (PM-003 narrative §4); sponsor ask #2 = estimate Mon/Tue with few quotes; PM-U-002/003 (Critical) never asked; R-012 covers only KAM simulation | **No** — the pricing team's own what-if need never became an SU row; the blueprint has no estimation feature |
| Guided process needs | Committee step + superior approval (C-002, C-026) | **Yes** — approval-as-action on the dashboard screen |
| Grid vs form dominance | `Inputs`: 85 manual columns per daily row (PM-001); `Outputs`: 76-column report (PM-003) | **No** — screens typed by the consolidation tree's field counts, which were themselves "not itemized" (v01 `fields_itemized: false`) |
| Bespoke workflow | Standard approval ladder | **Yes** (standard) |
| Per-port / per-counterparty variation | Data-model shape (named ranges; `CustosLogísticos_*_<Port>`) | **Yes** as data model (`CustosLogisticosFormScreen` "por porto"); not as interaction |
| Custom visual interaction | Output "folha de rosto" format for KAM (C-009) — out of app after C-056 | **Legitimately not material** for this surface |
| Standard CRUD suitability | Master data, costs, margins, approval | **Yes** — genuinely CRUD-suitable |

**Verdict: material signals existed and were not evaluated** — the daily wide-grid entry task, the visible
calculation density, and the what-if/estimation task that is the sponsor's second literal ask. **P-OBS-028
remains a semantic reasoning defect**, reformulated: not "the wrong surface was chosen" but "the surface was
selected on identity, data density and store-inherited controls alone; the interaction shape was never
recorded". Severity stays **S3**. Whether the correct answer is model-driven, canvas, or a record-centric
backbone with custom pages for entry/what-if is for the architecture revisit (§17), not for this adjudication.

---

## 11. Calculation complexity vs interaction complexity — kept separate

```text
calculation / domain complexity      →  where the pricing engine lives (SQL views/procedures, Dataverse-side
                                        logic, or a service) — a data/composition decision, independent of surface
interaction / experience complexity  →  what the user does on screen (grid entry, what-if, review, approve)
                                        — the surface decision
```

- The six calculation sheets, `INDIRECT` chain and model-style base sheets prove the **calculation layer** is
  a separate deliverable (the pack already says so for financial functions: `craft/excel-translation.md`,
  "the calculation layer is a separate deliverable from the app layer"). They do **not** prove the UI must be
  canvas. A complex engine can sit behind a standard record-oriented experience (read-only computed views as
  virtual tables, L4).
- Conversely, the daily entry of ~85 values per row and the Monday/Tuesday estimation task could require a
  bespoke interaction even over a simple data model. That is the signal P-OBS-028 says was not evaluated.
- Both were left implicit: the estimate's Fase 0 "Formalizar regras do Excel — 4d" is the only place the
  calculation layer is sized, and no artefact sizes or designs the interaction shape of entry/estimation.

---

## 12. Capture → SU → Options → Architecture lineage (P-OBS-027)

Frozen authority model respected: capture = normalized evidence; Shared Understanding = engagement
factual/epistemic authority. The question is not "was `_capture/process-model.md` cited" (it was: C-017,
C-041, A-006, U-010 cite it; all six lens outputs state they read it in full) but whether each material rule
reached the SU and was used.

### 12.1 The 14 process rules

| PM | Rule (short) | SU row(s) | Material concern | Options treatment | Architecture treatment | Class |
|---|---|---|---|---|---|---|
| PM-001 | Daily manual entry of quotes into `Inputs`, 291 named ranges = counterparty×fuel×metric | C-017, C-016, C-006 | data-model shape; **daily wide-grid entry task** | master-data ownership (R-006/U-027) | `DadosMestrePricing` entity, fields not itemized (non-structural open choice) | **CARRIED** (data model) / **PRESENT IN SU BUT NOT USED** (entry task shape → §10) |
| PM-002 | Date lookup over the full quote history via `Data_Lista` | A-003, A-006, U-010 (history rows 9–1469) | history volume (~1,460 rows), date-keyed access | not used (capacity concern judged "não material" on transaction volume) | `HistoricoPrecos` entity, no expected volume recorded | **PRESENT IN SU BUT NOT USED** — now material against the 1,000-record cap (§6 RQ-3) |
| PM-003 | 6 structurally identical output copies incl. `Simulador` (editable what-if copy) | C-041 (cites PM-003/PM-U-009), R-007, U-026→C-059 | duplication root cause; **what-if facet** | R-007, U-026 handled; what-if not treated | consolidation to one `PrecoDiarioConsolidado`; no what-if | **CARRIED CORRECTLY** (duplication) / **LOST CAPTURE→SU** (what-if facet) |
| PM-004 | `Inputs`/`Outputs` protected sheets | C-021 | protection ≠ access control | authorization enforcement point (material) | A7 "ponto de imposição: aplicação + o que a BD já impõe" | **CARRIED** |
| PM-005 | `INDIRECT`-built per-port logistics lookup | C-016 (partial) | calculation-chain complexity | — | `CustosLogisticosFormScreen` "por porto"; calc chain deferred to Fase 0 | **LEGITIMATELY NON-MATERIAL** at Options/Architecture; material to the calc layer/estimate (covered by Fase 0 generically) |
| PM-006 | Single dated self sign-off in `Checklist` | C-024, R-005 | audit/independent review | observability concern (material) | approval-as-action; audit mechanism not designed (§8) | **CARRIED** to SU and Options; **not used** in Architecture after C-057 (see §12.3) |
| PM-007 | `Base DFA/RF` model-style sheets (one formula per row) | — (only indirectly via A-007/R-008 on `Base RF`) | calc formalization effort; auditability of the engine | — | — | **LOST CAPTURE→SU** (dimensionante — sizes Fase 0) |
| PM-008 | `Outputs BIOS` biofuel-blend report layered on base output (Assumed) | — | **a whole output family / scope element** | — | no BIOS entity or screen | **LOST CAPTURE→SU** (material — scope) |
| PM-009 | Dead "X-Author for Excel" link | C-038, U-005, U-025, C-064 | prior automation killed by veto | U-025 decisive | v03 flag → v04 relocation (C-065) | **CARRIED CORRECTLY** |
| PM-010 | `UlyssesQuotes` automated feed | C-016, C-037 | market-data source | — | v01 `market-data-feed-integration` → subsumed by C-057 | **CARRIED** |
| PM-011 | `Market View` second, unreconciled series (Assumed); PM-U-006 | C-037 names both | two feeds, consumption unproven | — | dissolved by C-057 ("feed de mercado incluído") | **LEGITIMATELY NON-MATERIAL** after C-057 |
| PM-012 | `APOIO` weekday/port static lookup | — | none | — | — | **LEGITIMATELY NON-MATERIAL** |
| PM-013 | Currency/unit conversions typed over formulas in `Base` sheets | C-041 (replay #1-95), C-019 | override class of defect | R-007 | consolidation | **CARRIED** |
| PM-014 | `DF_GRID_1` → `#REF!` | A-007, R-008 | blast radius | precondition of O-002/O-004 | non-structural open choice, watch-list | **CARRIED CORRECTLY** |

**Traced: 14/14.**

### 12.2 The Critical PM-U questions

| PM-U | Question | Reached SU? | Consequence |
|---|---|---|---|
| PM-U-001 (Critical) | who else can repair the workbook | U-001 → C-029 | carried |
| PM-U-002 (Critical) | which `Inputs` columns are empty Mon/Tue; today's workaround | **No** | the estimation ask (#2) never acquired a requirement shape |
| PM-U-003 (Critical) | is there a method to estimate a missing quote | Partly — U-006 → C-039 ("sempre pior", never measured), C-046 | rule captured as tribal knowledge; **no capability requirement** derived |
| PM-U-005 (Critical) | what X-Author for Excel provided, why it stopped | U-005 → C-038; U-025 open | carried |
| PM-U-009 (Critical) | why 6 identical copies | U-026 → C-059 | carried |
| PM-U-011 (Critical) | cadence/deadline/readers of `Outputs` | C-006, C-007, C-030 (partly) | carried in substance |

The runtime contract for PM-U consumption exists only in `docs/PROCESS_CAPTURE_SPEC.md` ("THIS FEEDS THE LENSES:
each becomes a candidate SU Unknown"; planned lens-skill step "Interrogation list items relevant to the lens →
promoted to SU Unknowns") and in the capture template ("Each row is a candidate SU Unknown for the lenses").
**No Discovery lens `SKILL.md` and not `aisa-round` carry an adopt-or-dismiss step for PM-U rows.** The
lenses followed the template partially (4 of 6 Critical rows promoted, 1 partly, 1 not at all).

### 12.3 Loss counts

| Boundary | Material losses | Items |
|---|---|---|
| Capture → SU | **3** | PM-003 what-if facet (`Simulador`); PM-007 (model-style base sheets — sizes the calc layer); PM-008 (`Outputs BIOS` output family — scope). Plus PM-U-002 (Critical) not promoted |
| SU → Options | **1** | the Mon/Tue estimation rule (C-008/C-039/C-046) was treated as an *exposure* (A-008) and never as a **capability requirement** any option had to meet — options.md never mentions estimation as a feature of O-002..O-005 |
| Options → Architecture | **2** | the Options material concerns "observability & evidence retention — qualquer opção tem de desenhar um trilho de auditoria real" and "authorization enforcement point — do lado do servidor" were carried into v01 as "inherited from the store" and **not re-derived after C-057** moved the store; both losses are entangled with P-OBS-029 |

---

## 13. P-OBS-027 verdict

Decision tree (§15 of the brief) applied per loss:

- PM-003 what-if facet, PM-007, PM-008, PM-U-002 → **root cause: Discovery/capture-to-SU projection loss.** The
  lenses read the model in full and projected summary facts; three material facets and one Critical question
  did not become rows. This is a projection-depth issue in lens execution, aggravated by the missing
  adopt-or-dismiss contract for PM-U rows (§12.2).
- Estimation capability → **root cause: Options reasoning-depth defect** (the rule was in the SU; Options
  reframed it as risk, not requirement).
- Audit mechanism and server-side authorization after C-057 → **root cause: Architecture reasoning-depth
  defect**, the same event as P-OBS-029.
- The absence of `_capture/process-model.md` citations in `options.md` and the blueprints is **not a defect**:
  C-041 (which they cite) carries `PM-003/PM-U-009`; the frozen model says reasoning runs from the SU. Citation
  ceremony is not rewarded here.

**P-OBS-027 FINAL SEVERITY: S3** — re-rooted. The material consequence is real (a missing output family, a
missing feature shape, an unsized calculation layer), but it is not "the architecture did not re-read the
capture"; it is "three facets never reached the SU and one SU rule never became a requirement".

**Parse-once boundary preserved (§16 of the brief).** No repair proposed here makes Options or Architecture
re-read the capture model. The sanctioned shape is already in the contract (`orchestration.md`: PM rows are
citable evidence; raw sources openable "when material to confidence"):

```text
material question at a decision point (e.g. "what does the daily entry task look like?")
  → targeted pull of the normalized capture evidence (the PM row / replay finding)
  → any new factual conclusion written to the SU (new row, with the PM locator as evidence)
  → reasoning continues from the SU
```

No permanent capture preload; no whole-process reread.

---

## 14. Comparator gap U-028 — adjudicated separately from A-009

U-028: *"O dono da aplicação de referência já em produção (C-012) tem capacidade/mandato para absorver uma
segunda linha de pricing, e o seu modelo de dados consegue exprimir a forma da Marinha … sem colisão?"* —
Critical, `swing: decisivo: determina se O-003 (reaproveitar) é uma opção real, ou se O-004/O-005 (build de
raiz) é o único caminho`. Still open at the stopping point.

**Would resolving U-028 plausibly change the decision between O-003 and O-004?** **YES.** `options.md` says so
in its own words ("U-028 decide entre O-003 e O-004/O-005"), records `COMPARATOR EVIDENCE ABSENT` for O-003 vs
O-004/O-005, and O-003's stated strengths (audit trail, margin configuration, indexed-client formulas, feed
quotes without manual entry — C-012) map onto exactly the frame clauses D-002 cites for choosing O-004.

Therefore **D-002 remains conditional on a decision-changing Unknown.** `COMPARATOR EVIDENCE ABSENT` is
preserved. Nothing in §§6–9 is evidence for O-003: the mechanism findings about O-004's data layer do **not**
imply that the reference application would fit, absorb the Marinha shape, or be operated by a team with
mandate. The two questions stay separate; both stay open.

---

## 15. Pilot-1 consumer-test limitation

```text
DELIVERABLE CONSUMER VALIDATION: NOT EXERCISED
```

Pilot 1 did not execute: the sponsor Executive-Report consumer test; the architecture handoff test; the
implementation handoff test; the independent Estimate comparison (Estimate v02 was rendered in Mode A from the
Implementation Specification; no developer/lead estimate exists to compare). Pilot 1 is therefore **not** a
validation of deliverable usefulness. This is not a pack defect; a future pilot must execute that part of the
protocol, and — given §§8–9 — must do so on artefacts whose architecture has been re-verified first.

---

## 16. Candidate repairs, individually classified

| Candidate | What it would be | Classification | Basis |
|---|---|---|---|
| **PR-1 — architecture-significant technical-claim verification guard** | Enforcement of existing rules at the point where a structural `open_architecture_choices` entry (or an `/answer` whose target row carries `validade: plataforma-tecnica` or is referenced by a structural choice) is resolved | **PROVEN GENERIC DEFECT (Case A — enforcement/testability of existing guards)** | §4–5: the closure path in `aisa-answer` + `aisa-blueprint` accepts, by construction, a sponsor yes/no plus executor inference as a Confirmed platform-capability fact and as a structural closure; nothing engagement-specific is required to reproduce it (TC-2 and TC-5 in §17 pass through unchallenged today). Genericity rests on structural analysis of the path, not on recurrence (n=1) |
| **PR-2 — process-shape carriage/depth rule** | A rule making Options/Architecture engage the capture model at depth | **DOCUMENTATION DEFECT** (contract drift) — no new carriage/depth rule proven | §12: the only proven gap is that `PROCESS_CAPTURE_SPEC.md` and the capture template promise a PM-U adopt-or-dismiss step that no lens `SKILL.md` carries. The three projection losses are engagement-execution consequences at n=1. A generic "carriage depth" rule would need more pilot evidence and would risk the parse-once boundary |
| **PR-3 — experience-surface material-concern rule** | A requirement that surface selection record the interaction-shape evaluation | **ENGAGEMENT PRACTICE DEFECT** (at n=1) | §10: the knowledge to evaluate the interaction shape was in the pack (`application-surfaces.md` §1, §3; Discovery cues) and the signals were in capture/SU; the executor did not evaluate them. Proven in this engagement; genericity unproven. Watch in Pilot 2; a one-line strengthening of `aisa-blueprint` step 3 is the candidate if it recurs |

Not bundled. Only PR-1 is a runtime repair before the next pilot.

---

## 17. Minimum-complexity repair options (design only — nothing implemented here)

### 17.1 The narrow class under stronger verification

A technical proposition is **architecture-significant** when changing its truth value could change at least one
of: architecture authorization; experience mode/surface; record authority; composition; security/control
architecture; integration mechanism; hard feasibility; a material proof obligation; material cost/operability
shape. Only this class is in scope. No citation is required for technical sentences outside it.

### 17.2 The candidate invariant, tested

```text
architecture-significant platform/capability claim
+ used to settle a structural architecture choice
→ must carry ONE of:
    (a) authoritative RESEARCH / domain-knowledge evidence (file + section), read against the
        engagement's material requirements — capability confirmed ≠ fit confirmed;
    (b) engagement-supplied verifiable evidence (a named mechanism, configuration or artefact
        an accountable owner can show — not a business sponsor's yes/no about connectivity);
    (c) an explicit proof / measurement result (spike, published-limit arithmetic).
otherwise
→ the proposition stays Unknown (verification obligation, custo/swing) or Assumed-with-basis,
  and the structural choice stays open (blocks approval, never production — existing mechanism).
```

**Sufficient?** Yes for TC-1..TC-5 (§17.4), **provided clause (a) includes the fit test** — reading the
unit's exclusion list against the requirements in scope, which is exactly what `dataverse.md` §14 and
`store-boundaries.md` §7 are written to support. Without the fit clause, C-062's failure repeats with a
citation attached ("virtual tables exist, §14" → "surface confirmed").

**Not required** (and not proposed): web research per choice; three-source citation; Domain Knowledge
preload; a citation on every architecture sentence.

### 17.3 Where the smallest existing contract should hold it — context cost

| Option | Change | Context cost | Assessment |
|---|---|---|---|
| **R-A — strengthen `aisa-answer` step 4** | When the resolved row is referenced by a structural `open_architecture_choices` entry, or the new claim's `validade` is `plataforma-tecnica`: (i) compare the verbatim answer with the choice's `would_be_settled_by` — if it does not settle that fact, say so and keep the row/choice open; (ii) the extracted claim may not exceed the verbatim answer — inference goes to a separate Assumed row with basis (rule 3 already says this); (iii) a platform-capability proposition needs (a)/(b)/(c) or stays Unknown | ≈6–8 lines in one skill; no new state, ledger, router or matrix | **Preferred core.** Makes G1–G3 testable at the one point they failed |
| **R-B — strengthen `aisa-blueprint` step 15 (approval) and the closure of structural choices** | A structural entry may be marked resolved only when its resolving row's evidence class satisfies §17.2; if the choice concerns record authority or surface over an external store, the pull rule already names `patterns.md` §5 (the one engaged pattern) — record `access_mode`/`pattern` coherently (`virtualized`/`data-virtualization`, `replicated`/`data-replication`) and never `keep-in-place`+`direct` under a model-driven surface | ≈5 lines in one skill; reuses existing vocabulary | **Preferred companion.** Makes G6–G9 testable |
| R-C — a hook (`pre-write-guard`-style) checking SU rows for `plataforma-tecnica` + `USER_ANSWER`-only evidence | Programmatic flag on write | Small script; but it cannot judge fit, only evidence class — would flag legitimate engagement facts (a configured tenant setting confirmed by IT) | Not preferred alone; possible later as a `/status` warning, not a write block |
| R-D — new "technical-claim ledger" / new state / router | — | High | **Rejected** — violates §21 of the brief and the pack's own no-router doctrine |

Recommended repair scope: **R-A + R-B**, plus a test module exercising TC-1..TC-5 against fixtures (the Step 7
pattern). No semantic layer of Steps 3–7 changes; `dataverse.md` §14 and `patterns.md` §5 already hold the
knowledge.

### 17.4 Adversarial cases the guard must pass (designed, not implemented)

| Case | Input | Expected |
|---|---|---|
| **TC-1** | IT confirms, with the mechanism named ("virtual tables over the shared SQL Server via the SQL virtual connector provider, Entra identity, tables X/Y have integer PKs, no triggers") | May become **Confirmed with basis** (clause b); the structural choice may close **if** the fit test against the exclusion list is recorded |
| **TC-2** | A persona or the blueprint executor says "the platform supports it" with no authority | **Cannot become Confirmed**; stays Assumed-with-basis or Unknown; structural choice stays open |
| **TC-3** | Domain Knowledge has an authoritative section (e.g. `dataverse.md` §14) | Claim may be settled **within the section's evidence and volatility bounds** (validade `plataforma-tecnica`; re-verify trigger carried) |
| **TC-4** | The current value depends on tenant/configuration (a DLP policy, a gateway, an entitlement) | **Engagement verification required** (clause b or c); DK alone is insufficient — mirrors `decision-tree.md` §11 |
| **TC-5** | Capability exists generally but a documented limitation may defeat a material requirement (virtual tables exist; audit is required; virtual tables don't audit) | **capability confirmed ≠ fit confirmed** — the row may record the capability as Confirmed; the structural choice **stays open** until the requirement-level fit is recorded per domain. This case is the direct guard against a repeat of C-062 |

---

## 18. Engagement artefact disposition

**PRICING-MARINHA DISPOSITION: TARGETED-ARCHITECTURE-REVISIT** — with a named escalation condition to
DECISION-REVISIT, and U-028 preserved as an independent conditional on D-002.

Why not "artefacts remain valid": blueprint v03–v05, architecture-story, Implementation Spec v02 and Estimate
v02 all rest on C-062 as used; two of O-004's stated strengths do not apply under the recorded mechanism (§8);
two dashboard screens are unsupported on virtual data; the estimate's own §13 names the model-driven-over-
external-store analogy as an unverified premise.

Why not "return to Options" or "decision revisit" now: D-002 chose **O-004 = a purpose-built platform
application, whole solution**. Options never chose a surface or a data-access mechanism; the blueprint did. The
frame clauses D-002 cites (fragility C-041, master-data ownership R-006, auditability R-005, continuity by
construction C-029) remain closable by O-004 through a mechanism-per-domain hybrid (pricing data authority in
SQL as C-057 requires; workflow/approval/audit state Dataverse-owned or SQL-side by design). The pack's own
instrument for "a post-decision fact changes the decision basis" is a tripwire → `/revisit` (advisory), not a
silent return to Options.

What the revisit must do (blueprint v06, not produced here):

1. Reopen A-009 as a **structural** `open_architecture_choices` entry (recorded as `U-`, not `A-`), with
   `would_be_settled_by` naming the **mechanism per data domain and its fit against audit, authorization,
   query volume and schema constraints** — not connectivity.
2. Record `record_authority.access_mode` and `compositions.pattern` coherently per domain
   (`virtualized`/`data-virtualization` or `replicated`/`data-replication`), pulling `patterns.md` §5 for the
   one engaged pattern and `dataverse.md` §14 for the exclusion test.
3. Design the audit-trail mechanism and the server-side authorization point explicitly (the two
   Options→Architecture losses, §12.3).
4. Record the **interaction-shape** evaluation for the surface (daily grid entry; what-if/estimation; computed
   columns visible to users) with `su_refs`; where the SU lacks the fact, open the Unknown (PM-U-002/003 are
   ready-made, Critical, priced).
5. Carry the **measured spike** the pack mandates before committing to virtualization at this volume.
6. Open the verification obligations: shared-schema PK/trigger/primary-name conformance; on-premises vs Azure
   SQL and the identity that reaches it; DB-owner acceptance of schema/audit design; whether any row/column
   confidentiality requirement is hard.

**Escalation to DECISION-REVISIT** if the revisit finds that closing the auditability/SoD clause requires
moving pricing *data* authority into Dataverse against C-057, or that no mechanism-per-domain assignment
satisfies the material controls — then D-002's basis has moved and `/revisit` should be run against O-004
with O-003 (U-028) still open as the comparator.

Until then: the rendered v02 deliverables are **provisional**, not withdrawn; nothing was rewritten in this
step.

---

## 19. Next-pilot readiness

| | |
|---|---|
| `PACK 1.8.1 READY FOR NEXT PILOT UNCHANGED` | **NO** |
| `BOUNDED RUNTIME REPAIR REQUIRED BEFORE NEXT PILOT` | **YES — PR-1 only** (R-A + R-B + TC-1..TC-5 test module), classified Case A: enforcement of existing guards, no semantic change to Steps 3–7 |
| PR-2 | Documentation/contract alignment (PM-U adopt-or-dismiss step) — may be done with PR-1 if kept to one sentence per lens skill or one line in the `aisa-round` invocation; otherwise practice note for Pilot 2 |
| PR-3 | Practice — the revisit records the interaction-shape evaluation; watch for recurrence in Pilot 2 |
| Pilot 2 must additionally | execute the deliverable consumer tests (§15); watch whether unverified technical claims reach Confirmed anywhere; watch `solution_name`/A8/A9 recurrence (carried from Pilot 1) |

---

## 20a. Step 8C final corrections (2026-09-05)

Applied before the Step 8C runtime repair, on the instruction that the adjudication must not confuse a
candidate mechanism with an established one. Three lines of the final block change; the rest of the
adjudication (§4–§8, §10–§19) is untouched and remains the basis of Step 8C.

| Line | Was | Now | Reason |
|---|---|---|---|
| `SPECIFIC SQL ACCESS MECHANISM IDENTIFIED` | `YES` | **`NO`** | §6 identified supported **candidate** mechanisms (M1 virtual tables, M2 replication, M3 custom provider, M4 non-model-driven access). The engagement did **not** establish which mechanism is actually used per data domain; `record_authority` was recorded as `keep-in-place` + `direct` — no mechanism at all. |
| *(new)* `MODEL-DRIVEN + EXTERNAL SQL CAN BE DEFENSIBLE WITH PRECONDITIONS` | — | **`YES`** | RQ-1/RQ-2: the combination is not automatically incompatible; defensibility depends on a mechanism-per-domain assignment tested against the exclusion lists (§9 table). This is the research finding, stated as such. |
| `A-009 FINAL STATUS` | `DEFENSIBLE-WITH-PRECONDITIONS` | **`UNKNOWN`** | The status of the engagement's structural question is what the engagement established — nothing. "Defensible with preconditions" described the *research* possibility, not the *engagement* state. Under the runtime's own vocabulary the honest state of A-009 is `Unknown` (verification obligation, `swing: decisivo`), exactly what the targeted revisit (§18) reopens it as. |

```text
candidate mechanism exists      (research — YES)
≠
engagement mechanism established (engagement — NO)
```

Nothing in this correction weakens §18: the disposition stays TARGETED-ARCHITECTURE-REVISIT, and the
revisit's first task is to turn `UNKNOWN` into a recorded mechanism per data domain with its fit — or into
a `DECISION-REVISIT` escalation.

## 20. Final verdict

The Pilot-1 FAIL stands and its cause is now precisely located: not a false technical fact, but an
**unsupported load-bearing technical claim** that the frozen runtime already forbade and did not enforce at
one closure point. The reviewer's stronger factual assertion is withdrawn; the reviewer's integrity finding is
upheld and sharpened. The engagement needs a targeted architecture revisit before its deliverables are treated
as final. The pack needs one bounded enforcement repair, not a new principle.

```text
STEP 8B — POST-PILOT EVIDENCE ADJUDICATION: PASS
PILOT 1 HISTORICAL VERDICT PRESERVED: YES
P-OBS-029 LOAD-BEARING CLAIM WAS TECHNICALLY VERIFIED BEFORE CONFIRMATION: NO
P-OBS-029 REMAINS INTEGRITY DEFECT: YES
MODEL-DRIVEN + EXTERNAL SQL AUTOMATICALLY INCOMPATIBLE: NO
MODEL-DRIVEN + EXTERNAL SQL CAN BE DEFENSIBLE WITH PRECONDITIONS: YES
SPECIFIC SQL ACCESS MECHANISM IDENTIFIED: NO
SPECIFIC MECHANISM FIT AGAINST MATERIAL CONTROLS: FAIL
O-004 NATIVE SECURITY CLAIMS STILL APPLY: NO
O-004 NATIVE AUDIT CLAIMS STILL APPLY: NO
A-009 FINAL STATUS: UNKNOWN
P-OBS-028 CANVAS PRESUMPTION REMOVED: YES
P-OBS-028 MATERIAL SURFACE-CONCERN OMISSION PROVEN: YES
PROCESS RULES TRACED: 14/14
MATERIAL CAPTURE→SU LOSSES: 3
MATERIAL SU→OPTIONS LOSSES: 1
MATERIAL OPTIONS→ARCHITECTURE LOSSES: 2
P-OBS-027 FINAL SEVERITY: S3
U-028 DECISION-CHANGING: YES
DELIVERABLE CONSUMER VALIDATION COMPLETED IN PILOT 1: NO
PR-1 TECHNICAL-CLAIM GUARD: PROVEN-GENERIC
PR-2 PROCESS-SHAPE CARRIAGE: DOCUMENTATION
PR-3 EXPERIENCE-SURFACE CONCERN: PRACTICE
RUNTIME MODIFIED DURING ADJUDICATION: NO
PRICING-MARINHA DISPOSITION: TARGETED-ARCHITECTURE-REVISIT
PACK 1.8.1 READY FOR NEXT PILOT UNCHANGED: NO
BOUNDED RUNTIME REPAIR REQUIRED BEFORE NEXT PILOT: YES
```
