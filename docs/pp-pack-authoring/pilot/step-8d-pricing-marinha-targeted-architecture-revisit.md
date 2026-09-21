# Step 8D — Pricing-Marinha Targeted Architecture Revisit — pack pp 1.8.2

> Not Pilot 2. Not a new Discovery, Framing or Options round. Not pack authoring. Not a framework redesign.
> A bounded architecture revisit of `projects/pricing-marinha` using the repaired runtime (1.8.2), at the exact
> failure point Pilot 1 exposed (A-009 → C-062 → "surface confirmed"). Pilot-1 history is preserved; the
> Pilot-1 verdict remains **FAIL**. The runtime was not modified.

**Verdict: `STEP 8D — PRICING-MARINHA TARGETED ARCHITECTURE REVISIT: PASS`** — the revisit executed with
integrity on persisted state; A-009 started as UNKNOWN; C-062 was never used as fit evidence; the recovered
process semantics entered the Shared Understanding before architecture used them; C-057 caused targeted
revalidation, not a rerun; D-002 was checked and preserved; a corrected blueprint (v06) exists and is honestly
**not approved**. Disposition: **`ARCHITECTURE STILL OPEN`**. Full output block at the end.

---

## 1. Basis / checkpoint

| | |
|---|---|
| Checkpoint used | `step-8c-baseline` → `7e977cd562b25c74925347ae4a17bebb6902243e` (HEAD at start; Step 8C.1 freeze correction included) |
| Pack | `pp` `pack_version: 1.8.2` — unchanged |
| Binding inputs | Step 8B adjudication (§4–§9, §14, §18, §20a) and its Step 8C corrections: `MODEL-DRIVEN + EXTERNAL SQL AUTOMATICALLY INCOMPATIBLE: NO` · `CAN BE DEFENSIBLE WITH PRECONDITIONS: YES` · `SPECIFIC SQL ACCESS MECHANISM IDENTIFIED: NO` · `SPECIFIC MECHANISM FIT AGAINST MATERIAL CONTROLS: FAIL` · `A-009 FINAL STATUS: UNKNOWN` · `PRICING-MARINHA DISPOSITION: TARGETED-ARCHITECTURE-REVISIT`. Research mechanisms M1–M4 treated as **candidates only** |
| Runtime modified during Step 8D | **NO** — no file under `library/`, `.claude/` or `docs/` other than this report was touched; `git diff --stat 7e977cd -- library/ .claude/` is empty |
| Engagement artefacts modified | **YES — append-only, through existing mechanisms**: `shared-understanding.md` (new rows; one sanctioned `resolved →` marker on C-062), `answers.md`, `council-log.md`, `story.md`, `_blueprint/blueprint-log.md` (v06 entry = the revisit log), new `_blueprint/ux-blueprint_v06.yaml`, `dashboard.html` regenerated. Nothing under `_render/`, `_synthesis/`, `_capture/`, `decisions.md`, `options.md`, `frame.md`, `_state.json` changed. Note: `projects/*` is gitignored (mount point to the private engagement repo), so these changes are not in this repository's history by design |
| Pilot-1 documents modified | **NO** |
| Web research | **NO** — Step 8B §6 bounded commission and pack Domain Knowledge sufficed; no new architecture-significant technical question exceeded them |
| Previous chat transcript used | **NO** |

---

## 2. Historical state preserved

Untouched: original SU rows (C-062 keeps its text, gains only the sanctioned `resolved → A-010, U-032`
marker), `answers.md` history, `decisions.md` (D-001..D-004), blueprint v01–v05, Pilot-1 reports, all
rendered `_render/*_v01|v02.md`, `_synthesis/*`, `_capture/*`. The lineage is auditable in
`_blueprint/blueprint-log.md` (v06 entry) and in the v06 file header:

```text
v05 — Pilot-1 approved architecture (D-004)
  → post-pilot defect P-OBS-029 (A-009 closed on C-062; Step 8B PR-1 PROVEN-GENERIC; Step 8C repair → 1.8.2)
  → Step 8D targeted revisit (step-8c-baseline; runtime untouched)
  → v06 — corrected architecture, NOT APPROVED (4 structural open choices)
```

---

## 3. Rehydration result

Fresh session. `/status` for the phase `decision` (architecture) derived the `Read to resume` set:
`_state.json` · `decisions.md` (D-002..D-004) · `_blueprint/ux-blueprint_v05.yaml` (+ **v01, forced by the
`SEE_V01` back-references**) · `_blueprint/blueprint-log.md` · `_synthesis/architecture-story.md` · SU material
rows. From that set alone the approved architecture, its authorization, its structural closures and the
approval chain were fully reconstructible.

What the default set did **not** carry and the revisit needed — obtained by targeted pulls, no transcript:

| Need | Source pulled | Why |
|---|---|---|
| O-004 stated strengths (targets of the C-057 revalidation) | `options.md#O-004` | D-002 cites them by reference only |
| Verbatim sponsor answer behind C-062 (PR-1 verbatim-boundary check) | `answers.md` → "A-009" entry | the SU row carries the extracted claim, not the answer |
| Process semantics lost in Pilot 1 | targeted normalized evidence (§4) | absent from SU by adjudicated loss |
| Platform boundaries per architecture section | DK units, one or two per section (§1 table in the log) | pull rule |

`RE-HYDRATION SUFFICIENT: YES` for the architecture record; the semantic gaps were the SU's (adjudicated in
8B), not the read set's. Observation for PR-6: the decision/architecture read-set row lists neither
`options.md` nor `answers.md`, both of which a Decision-basis revalidation needs; targeted pulls are within the
contract, so this is an observation, not a defect (§23).

---

## 4. Targeted evidence pulls

Not a re-capture: `_capture/process-model.md` §4 was **not** regenerated (brief §4 excludes wholesale
re-capture; the engagement's synopsis therefore remains the 1.8.1 workbook-only narrative — §23).

| Pull | Locator | Recovered → SU row |
|---|---|---|
| Calculation chain | docx "Inputs, cálculos e outputs" ¶60–100 | **C-069** Cedência → Base → Venda → Mínimo; unit conversions |
| "Até/após" reference rule | kick-off [00:42:37–00:44:25]; docx ¶91–100 | **C-070** max of the two weekly prices; upward rounding rule ("empola a 3") — exact formula not evidenced |
| Four unit variants as a consumer requirement | docx ¶79–90, ¶151–157; PM-003 | **C-071** — the ×4 recomputation is accidental (C-041), the 4 outputs are genuine |
| `Outputs BIOS` family | docx ¶101–111, ¶137–143; kick-off [00:40:49–00:42:02]; PM-008 | **C-072** blend formula; FAME/HVO prices from Supply; consumer **U-033** |
| `Simulador` as the analyst's task | kick-off [00:57:44–00:58:23], [00:40:22–00:40:50], [01:07:51–01:08:28]; PM-003 | **C-073** projection/what-if is the analyst's central intervention |
| Mon/Tue behaviour as invariant | `context.json.literal_request` (2nd literal ask); C-008/C-039/C-046/C-032/C-055 | **C-074** invariant phrased as behaviour |
| Publications consumer | kick-off [00:42:56–00:43:08], [00:43:35–00:43:51] | **C-075** Sines/Lisboa indicative prices |
| `Base DFA/RF` intermediate stage + cross-source incoherence | docx ¶61, ¶111; PM-007, PM-013, PM-U-007 | **C-076**; **U-035** load-bearing or abandoned |
| PM-U-002 (Critical, never promoted) | `process-model.md` §6 | **U-034** |
| Interpretation needed for domain assignment | C-057 verbatim (answers.md U-029) | **A-012** (workflow state ≠ pricing data) · **U-040** (acceptance) |
| To-be invariant from control asymmetry | C-023, C-029, C-026/C-043 | **A-011** minimum-price floor (inferred, not sponsor-confirmed) |

Every factual conclusion entered the SU through the existing authority mechanism (new rows with locators;
`answers.md` records the pull) before architecture used it. No reasoning ran from raw evidence directly into
the blueprint.

---

## 5. A-009 reopening

A-009 started this revisit as **UNKNOWN** (Step 8B §20a). Mechanically: `C-062` was re-questioned via the
`aisa-answer` revalidation fallback ("the note contradicts the claim → normal `was <id>` flow"), yielding
**A-010** (Assumed — "a connection/gateway is *reported* as configured", second-hand, per rule 3) and
**U-032** (Unknown, Critical, `swing: decisivo`). The settling fact was rewritten from v02's connectivity
question to:

> *What data-access mechanism is used for each material data domain, and does that mechanism satisfy the
> engagement's material functional, security, audit, query, operability and lifecycle requirements?*

C-062 is preserved as history (text untouched, `resolved →` marker). **It is not cited as fit evidence in any
field of v06**; it appears only via A-010 as a reported fact. `C-062 USED AS ARCHITECTURE FIT EVIDENCE: NO`.

---

## 6. SQL arrangement

| Item (brief §10) | Status |
|---|---|
| A shared, already-operated SQL Server relational DB, used by Spain, destination of "tudo o que é pricing" | **Confirmed** (C-057, sponsor, direct) |
| Connection/gateway configured | **SECOND-HAND** (A-010) — sponsor's yes; not shown by IT |
| Hosting topology (on-prem / Azure SQL / managed instance) | **UNKNOWN** (U-036) — "gateway" suggests on-premises but is not evidence |
| Connection identity (implicit shared / service principal / Entra per user) | **UNKNOWN** (U-036) |
| Database owner; schema-change authority (shared with Spain) | owner class known (C-057); change authority **UNKNOWN** (U-036) |
| Tables/views used; primary keys (GUID/int); primary-name column; server-side triggers | **UNKNOWN** (U-036) |
| Volumes / query shapes | history ≈1,460+ daily rows growing 1/day (A-003, A-006); wide daily row (~85 values, PM-001); otherwise UNKNOWN |
| Confidentiality classification | Interno (C-036) |
| Which artefacts use the current connection (Canvas / flow / virtual table / dataflow / provider) | **UNKNOWN** (U-036) |

The mechanism was **not** inferred from the gateway's existence. U-036 is the basis-B verification obligation
that closes or excludes each candidate (proof obligation V1).

---

## 7. Per-domain mechanism analysis

Working analysis (not a kernel contract); vocabulary from `patterns.md` §5 / the blueprint schema; status
values are the existing architecture semantics only.

| Data domain | Authority | Candidate mechanism | Requirement fit | Material limitations (DK) | Evidence | Status |
|---|---|---|---|---|---|---|
| Master data (dictionary) | SQL (C-057) | M1 virtual R/W · M2 replicated | table-level role privilege OK; change approval (C-058) must live outside the virtual table | no audit, BPF, alternate keys, validate-on-update; PK GUID/int + primary name + no triggers | `dataverse.md` §14 (A); U-036 (B pending) | **proof required** · **open** |
| Logistics costs + target margins | SQL | M1 write · M4 stored procedure via custom page/flow | margin decision is the auditable business event → external/custom audit; attribution collapses under a shared credential | as above + identity (`security-controls.md` §6.1) | A | **open** (U-036, U-038) |
| Daily inputs/quotes (feed + manual) | SQL (feed already there) | M1 read; M1 write-through or M4 for the wide grid | ~85 values/day grid; Mon/Tue estimated-value marking (C-074) | write-through virtualization: weak production evidence, performance UNKNOWN; all attributes returned | `patterns.md` §5 (A) | **open** (U-032, U-034) · proof required |
| Consolidated daily price (4 units, BIOS, até/após) | SQL — calculation engine | M1 read-only over SQL views | read-only; no charts/dashboards → grids; export by flow | views are read-only (fits); 1,000-record cap (daily slice small); no table import/export | `azure-sql.md` §3; `dataverse.md` §14 (A) | **proof required** (read path) — coherent |
| Price history (multi-year, 10-year retention) | SQL | M1 read-only with positive date filter · external reporting | filtered audit/dispute queries (R-004); retention stays in the DB (C-060) | 1,000 cap; negative filters corrupt paging; not on the delegable-source list; no performance data | `dataverse.md` §14; `query-and-delegation.md` §4 (A) | **proof required** (spike) |
| Workflow/approval state + application audit journal | **OPEN** — candidate `owned` | native tables | native audit, roles, BPF; approval-before-load native; does not move pricing-data authority (A-012) | requires sponsor/DB-owner acceptance (U-040); audit retention set at environment creation | `dataverse.md` §8/§9 (A); A-012 | **open** (U-040) |
| SAP term-contract terms | SAP (C-052) | read reference — mechanism UNKNOWN | one consumer, read, low volume | none material | C-003, C-063 | open, **non-structural** |

`SPECIFIC DATA-ACCESS MECHANISM IDENTIFIED PER MATERIAL DOMAIN: PARTIAL` — a coherent candidate per domain,
none established. `MECHANISM FIT AGAINST MATERIAL CONTROLS: PARTIAL` — basis A applied for exclusions and
conditional fit; basis B/C absent. **No domain is `settled`.** Coherence rule honoured: no domain asserts
external authority + `keep-in-place` + `direct` + native model-driven behaviour; provisional values are flagged
in-line, exactly the shape Step 8C's accepted fixture uses.

Not needed: M3 (custom provider) — no requirement forces it. Replication (M2) is retained only as a
per-domain fallback where a hard row/column requirement (U-037) or platform data features are required; C-057
forbids turning the platform store into the pricing authority, and v06 does not.

---

## 8. Security

Re-derived explicitly in `ux-blueprint_v06.yaml#architecture.identity_and_controls` (A7 projection). The
Pilot-1 strengths were not carried forward.

| Control | Plane | Classification under the candidate mechanisms |
|---|---|---|
| Authentication (internal users) | 1 — Entra ID | **native** |
| Authorization by action/role (Analyst edits; Committee reviews; Superior approves; Owner approves master data) | 5 + 3 partial | **native-to-mechanism at table level** (per-role privilege on a virtual table); **not applicable** for row/column over virtualized SQL data |
| Row/column restrictions | 3 | **still Unknown** whether hard (U-037); if hard → M2 for that domain or per-user identity to the DB (`azure-sql.md` §5) |
| Server-side enforcement point over SQL data | 3/4 | **external** (DB grants on the connection identity) and **still Unknown** (identity — U-036); under a shared credential the whole population collapses to one principal |
| Separation of duties (approval before load, C-026/C-043) | 3 if workflow domain owned, else 5 + SQL procedure | **native (if owned) / custom (if SQL)** — U-040 |
| Minimum-price floor (A-011) | engine / export flow | **custom / explicitly implemented** |
| Privileged administration | 2/3 | **not applicable** as confidentiality against administrators (classification Interno) |
| Attribution (who did what) | — | **custom** unless delegated identity is proven (U-036): user column written by the app + owned journal |

`SECURITY BASIS REVALIDATED: YES`.

---

## 9. Audit

| Business event | Where recorded | Classification |
|---|---|---|
| Master-data change (request → approval, C-058) | owned journal/approval table (if U-040) or SQL temporal table | native (owned) / custom (SQL) |
| Margin decision; Mon/Tue projection (rule applied, estimated vs actual) | versioned SQL table + temporal table, or owned journal | custom |
| Approval before load (C-026/C-043) | owned (native audit) or SQL approval table | native (owned) / custom |
| Export/publication (file, user, time, price version) | export-flow record → journal | custom |
| Source-data changes (manual inputs, costs, premiums) | SQL temporal tables or audit columns — **triggers break connector/virtual-table writes** (`azure-sql.md` §6; 8B §6 L9) | external / custom |
| Reads and exports of data | not audited by the platform (`dataverse.md` §9) | not applicable |

Retention: 10 years (C-060) — data in SQL; if the workflow domain is owned, audit retention must be configured
at environment creation and is not retroactive. Correlation: a daily-price version id (date × port × product ×
unit) links inputs → calculation → approval → export — an engine/journal obligation. Tamper-resistance level
and audit consumer: **Unknown** (U-038). Absence of native audit was not treated as a disqualifier: the
alternative is designed and carried as proof obligation V2. `AUDIT BASIS REVALIDATED: YES`.

---

## 10. Calculation engine

Preço Cedência → Preço Base → Preço Venda → Preço Mínimo (C-069), blends (C-072), até/após (C-070), the four
unit conversions (C-071), Mon/Tue estimation (C-074, shape U-034): **SQL-side** (views/stored procedures),
recorded as a new composition `pricing-calculation-engine`, pattern `hybrid-low-code-pro-code` (computation
seam), forced by C-057 (authority in SQL) and by "calculations must be done on the external side" for virtual
tables (`dataverse.md` §14). Business logic owner: pricing team (C-068); DB DevOps/operation: the team
operating the shared DB (C-057) — two release pipelines by construction (`azure-sql.md` §11). The experience
surface was **not** used as a proxy for where the engine lives. `CALCULATION ENGINE LOCATION EXPLICIT: YES`.

---

## 11. Business invariants

| Invariant | SU id | Preserved in v06 |
|---|---|---|
| Approval before publication/load | C-022, C-026, C-043 | yes — workflow domain (owned or SQL), SoD control |
| Nothing loaded/published below the approved minimum | **A-011** (new, inferred from C-023/C-029) | yes — engine/export validation (custom); sponsor confirmation still needed |
| Mon/Tue pricing remains possible with incomplete quotes, conservative rule explicit and traceable | **C-074** (new) | yes — engine + audit event; data shape open (U-034) |
| Published price traceable to its inputs | C-024, R-004, R-005, D-002 condition | yes — version id correlation (custom) |
| Port-specific cost rules | PM-005, C-016 | yes — engine; parity scenario (c) |
| KAM output format stays stable | C-009, C-033, R-002 | yes — output family 1 |
| SAP is the truth for term-contract terms | C-052 | yes — relocated responsibility unchanged |

`MON/TUE BEHAVIOUR PRESERVED: YES` (as invariant; mechanism shape open).

---

## 12. Output families

Recorded in `ux-blueprint_v06.yaml#architecture.output_families` with consumer · purpose · source calculation ·
generation · delivery · authority/status for each: daily minimum price ("folha de rosto", KAM + committee);
**four unit variants** (loading — Confirmed, mandatory, C-071); **até/após reference** (publications Sines/Lisboa,
client indicatives — C-070/C-075; exact rounding inside the parity obligation); **Outputs BIOS** (family
Confirmed C-072, consumer **Unknown** U-033 — neither designed away nor designed in); **analyst projection /
what-if** (task Confirmed C-073/C-074; form Unknown U-034/U-039); audit journal (D-002 obligation; mechanism
open). No output was dropped because the workbook implemented it awkwardly.

`OUTPUTS BIOS REPRESENTED: YES` · `SIMULADOR / WHAT-IF REPRESENTED: YES` · `FOUR UNIT OUTPUT FAMILY
REPRESENTED: YES`.

---

## 13. Interaction-shape observation (PR-3 — observation only)

With C-069..C-076, U-034 and U-039 in the SU, the executor's surface reasoning considered: the wide daily
grid entry (~85 values, PM-001/C-006/C-016); computed columns visible during work (C-069, 59 derived columns
today); current-vs-next-week comparison (C-070); the analyst's what-if/projection with missing inputs (C-073,
C-074, U-034, U-039); committee review (C-002); approval (C-026/C-043). It concluded that CRUD and the
approval ladder are record-centric while the daily grid and the what-if are task-focused, and named
"record-centric backbone + custom pages" as the natural candidate composition — **recorded as a candidate,
not chosen**. `INTERACTION SHAPE NATURALLY EVALUATED: YES`; `PR-3 RECURRENCE OBSERVED: NO`.

Evidence caveat, stated plainly: the Step 8D brief (§20) names these shapes, so the executor was primed. The
evidential value for PR-3 is weak-positive; Pilot 2 remains the real test. No task matrix was added.

---

## 14. Experience-surface re-evaluation

`PRIMARY EXPERIENCE SURFACE: OPEN`. `primary_surface` carries v05's value flagged PROVISIONAL (to avoid
inventing another). Candidates recorded with forfeits: record-centric pure · record-centric backbone + custom
pages (natural) · canvas over the SQL connector (identical identity problem to M1 unless explicit Entra).
Exclusions: dashboards/charts over virtual data (two screens re-typed to views/grids); custom pages have no
offline/retained state/locale formats (immaterial for an internal desktop audience, C-013). Open proof
obligations: the surface closes with U-032 (where writes and calculation happen) + U-039 (interactivity) +
U-034 (Monday task shape) — never with connectivity.

---

## 15. Analytics / dashboard re-evaluation

Consumers traced: the committee reviews the day's values (C-002) → a grid, not a chart; history is consulted
for audit/dispute (R-004) → a date-filtered grid. **No chart/KPI consumer is evidenced.** The v01 "dashboard"
screen type was an artefact of the consolidation tree. No second analytical store is designed; should an
analytics requirement emerge, direct reporting over SQL (the data already lives there) is the path — not
assumed, not built.

---

## 16. U-028 status

`U-028 STATUS: COMPARATOR EVIDENCE ABSENT` — Critical, open, unchanged. Nothing in the A-009/U-032 work is
evidence for or against O-003 (Step 8B §14). D-002 stays conditional on U-028 as before; no D-002 condition or
tripwire says the comparator gap now invalidates the selected outcome → no Decision-revisit trigger.

---

## 17. C-057 targeted revalidation (PR-7 acceptance test)

C-057 (pricing authority = external shared SQL) as the premise; dependents classified:

| Dependent conclusion | Classification |
|---|---|
| Access mechanism (`keep-in-place` + `direct` recorded as fact) | **OPEN** — mechanism per domain never established (U-032); provisional values flagged |
| Composition `shared-pricing-sql-server` (`direct`, forced_by "conectividade confirmada (C-062)") | **REVALIDATED** — forced_by rewritten on C-057 alone; pattern provisional pending U-032 |
| Security basis ("row/column security inherited from the store") | **REVALIDATED** — table-level native only; row/column n/a over virtualized SQL; enforcement identity Unknown (U-036/U-037) |
| Audit basis ("audit inherited from the store") | **REVALIDATED** — designed explicitly per event; native only in an owned workflow domain (U-040) |
| Calculation engine location | **REVALIDATED** — SQL-side engine, new composition (`dataverse.md` §14 exclusion) |
| Experience surface ("confirmed" in v03) | **OPEN** — structural choice reopened |
| Dashboards / query shapes (two dashboard screens; ≈1,460-row history) | **REVALIDATED** — re-typed to grids with mandatory positive date filter; measured spike required |
| Integration path — SAP read reference; X-Author relocation; Excel export | **STILL VALID** (C-003/C-052/C-063; C-065); export mechanism revalidated to a flow (no import/export on virtual tables) |
| O-004 strength "segurança nativa por linha/coluna" | **REVALIDATED → does not apply** to pricing-data domains; partial in the owned workflow domain if U-040 |
| O-004 strength "auditoria nativa" | **REVALIDATED → does not apply** to pricing-data domains; partial if U-040 |
| O-004 strength "padrão de integração directa cobre SAP/X-ALT" | **STILL VALID** for SAP; X-Author relocated; does not describe the SQL layer |
| O-004 strength "aprovação do comité em passo nativo" | **OPEN** (U-040) |
| O-004 strength "dados-mestre arrancam com SAP como fonte" | **STILL VALID** |
| D-002 justification — fragility (C-041), master-data ownership (R-006 → C-058), continuity by construction (C-029) | **STILL VALID** |
| D-002 justification — auditability (R-005) closed by O-004 | **REVALIDATED** — closed through the D-002 *condition* "auditoria/SoD desenhados de raiz", i.e. explicit design, not native audit → **TRIPWIRE check run: not fired** |
| D-002 conditions (master-data owner; key cleanup funded; DLP review if new egress) | **STILL VALID** — unchanged by the mechanism |

`C-057 TARGETED REVALIDATION EXECUTED: YES` · `C-057 CAUSED WHOLESALE RERUN: NO` — no phase was rerun; nothing
in `decisions.md` was rewritten; the full `still valid / revalidate` list is in the blueprint-log v06 entry.

---

## 18. O-004 strengths revalidation

`O-004 SECURITY STRENGTH SURVIVES: PARTIAL` · `O-004 AUDIT STRENGTH SURVIVES: PARTIAL` — both survive only
for the workflow/approval/audit domain and only if that domain is owned (U-040 accepted); for every
pricing-data domain under M1/M4 they do not apply and the control is explicit/custom/external. The two
strengths were justification for O-004, not conditions of D-002; the condition D-002 actually carries
("designed from scratch") is what v06 implements.

---

## 19. D-002 tripwire check (brief §25)

| Trigger | Fired? | Basis |
|---|---|---|
| TW-1 build effort > estimate without scope review | **No** | build not started |
| D1 — no supportable per-domain mechanism satisfies the controls | **No** | a coherent candidate assignment exists; establishing it is proof work, not impossibility |
| D2 — controls require violating a confirmed structural constraint | **No** | audit/SoD close with an owned workflow domain (A-012) or SQL-side design; pricing-data authority stays in SQL (C-057) |
| D3 — corrected architecture changes a D-002 condition | **No** | "auditoria/SoD desenhados de raiz" is exactly what v06 does; the "native" strengths were option justification, not conditions |
| D4 — a Decision tripwire fired | **No** | TW-1 above |
| D5 — U-028 or another decision-changing Unknown became adverse | **No** | no new evidence |

`D-002 DECISION REMAINS DEFENSIBLE: YES` (conditional on U-028 as before) · `DECISION REVISIT REQUIRED: NO`.
Escalation condition from 8B §18 (auditability forcing pricing-data authority into Dataverse) did not occur.
Observation: `_simulation/counterfactuals/` does not exist (no `/simulate` ran in Pilot 1) — had escalation been
required, `/revisit` would have stopped at "missing counterfactual" (§23).

---

## 20. Architecture proof obligations

| # | Claim | Level | Basis it supplies | su_ref |
|---|---|---|---|---|
| 1 | Production-grade proof, whole solution (carried from D-002) | V4 | — | D-002 |
| 2 | SQL arrangement inspection: topology, connection identity, schema owner/change authority, tables/views, PK/primary name/triggers, volumes, current connection usage | V1 | **B** | U-036 |
| 3 | Measured virtual-table spike over the shared DB: CRUD on a written table (margins), read-only view (consolidated price, 4 units), history query with positive date filter (1,000 cap / paging), latency under the real identity — only if M1 survives U-036 | V2 | **C** | U-032 |
| 4 | Audit/attribution mechanism proof: owned journal (if U-040) or SQL temporal tables; inputs → calculation → approval → export correlation; DB-owner acceptance | V2 | **C** | U-038 |
| 5 | Calculation-engine parity vs the workbook (`Outputs` authoritative, C-059) — scenarios: normal full-input day; Mon/Tue missing quote (rule applied, logged, never zero); port-specific rule; BIOS blend (conditional U-033); four unit variants; até/após rounding; legitimate manual override (logged); approval before export/load | V3 | **C** | C-069 |
| — | *(conditional, not created)* what-if interaction prototype — only if U-039 = interactive | V2 | — | U-039 |

`PROOF OBLIGATIONS REMAINING: 5`. No spike was created automatically; each obligation is architecture-
significant (fit of the mechanism, audit basis, engine correctness).

---

## 21. Corrected blueprint disposition

`_blueprint/ux-blueprint_v06.yaml` produced through the existing version mechanism (supersedes v05, never
overwrites it). `CORRECTED BLUEPRINT VERSION: v06` · `CORRECTED BLUEPRINT APPROVED: NO`.

Structural open choices (block approval, not production): (1) mechanism per data domain + fit (U-032);
(2) audit basis and placement of workflow/approval state — owned vs SQL (U-040 + U-038); (3) server-side
authorization enforcement point and connection identity + hard row/column requirement (U-036 + U-037);
(4) primary surface/composition (U-032 + U-039 + U-034). `STRUCTURAL OPEN CHOICES REMAINING: 4`. None was
closed on configuration facts, on Domain Knowledge without fit, or on the likelihood of the preferred
direction. Non-structural items carried: U-033, U-034, U-035, SAP read mechanism, R-008, R-012, C-065, R-004,
C-067. The approval gate (brief §33) fails on items 1, 2, 7 and 9 → **not approved**; items 3, 4, 5, 6, 8 and
10 pass.

---

## 22. Deliverable staleness

| Deliverable | Classification | Why |
|---|---|---|
| Architecture Blueprint (`solution-blueprint_v02`) | **STALE — RERENDER REQUIRED** (after approval) | A4 surface "confirmed", A5 `keep-in-place` as fact, A7 inherited controls, A6 `(none)` — all changed |
| Implementation Specification v02 | **STALE — RERENDER REQUIRED** | §4 entities `keep-in-place`, §6 automation `(none)`, §7 "conector relacional directo", §8 enforcement point, §13 single V4 acceptance line |
| Estimate v02 | **STALE — RERENDER REQUIRED** — not edited in place | premise "Model-driven app screen (Dataverse) by analogy" gone; new work: SQL engine packages, virtualization spike, custom audit/attribution, custom pages candidate, view re-typing |
| Executive Report v02 | **STALE — RERENDER REQUIRED** | §10 architecture form (`keep-in-place`, native controls), §9 "0 structural open choices", §8 proof obligations |
| Claude Design Brief v02 | **STALE — RERENDER REQUIRED** | §3 surface, §6 two dashboard screens unsupported on the mechanism, missing task screens candidates |
| Discovery Report v02 | **UNCHANGED** | reads no architecture |
| `_synthesis/architecture-story.md` (topic pack, not a deliverable) | stale relative to v06 | regenerates on `/synthesize` after approval |

Nothing was re-rendered: the architecture is not approved. `IMPLEMENTATION SPEC STALE: YES` · `ESTIMATE STALE:
YES` · `CLAUDE DESIGN BRIEF STALE: YES`.

---

## 23. Runtime observations (PR-1 / PR-3 / PR-7 / PR-6 and others)

| Id | Item | Observation |
|---|---|---|
| OBS-8D-01 | **PR-1** — did the runtime reject fact→fit overreach naturally? | Yes, as executed: the re-question of C-062 applied the verbatim boundary (rule 3, step 4) and step 4b (settle the named fact); v06 closed **no** structural choice without basis A/B/C, and every `would_be_settled_by` names mechanism + fit. Caveat: the brief primed this behaviour; this is compliance evidence, not an unprompted test. |
| OBS-8D-02 | **Comprehension survival** — did recovered meaning become state before architecture used it? | Yes: C-069..C-076, A-011/A-012, U-033..U-040 were written first; the blueprint cites only ids. Note: in a Decision-phase revisit there is no lens run, so the 1.8.2 disposition step (`MAP/ADOPT/DISMISS`) did not apply — the executor projected the pulls directly as SU rows with locators. The engagement synopsis (`process-model.md` §4) was **not** regenerated, so `/status`'s teach-back trigger cannot fire on it for this engagement. |
| OBS-8D-03 | **Structural constraints** — did they stay visible? | Yes: C-057 (data authority), C-056 (internal audience), C-036 (Interno), C-028/C-048 (no separate budget) stayed load-bearing; the previously invisible one — the access mechanism — is now explicit (U-032, `swing: decisivo`). |
| OBS-8D-04 | **PR-7** — did C-057 cause targeted revalidation rather than rerun or silent carry-forward? | Yes: dependents found through `su_refs`, `forced_by`, rationale prose, `options.md` strengths and D-002 clauses; classified line by line; tripwire check run; no phase rerun; `decisions.md` untouched. |
| OBS-8D-05 | **PR-6** — could the session resume from persisted state? | Yes; no transcript. Two read-set observations: (a) `SEE_V01` forced a v01 read (known cost); (b) the decision/architecture row lacks `options.md` and `answers.md`, which a Decision-basis revalidation and a PR-1 verbatim check need — targeted pulls, permitted. |
| OBS-8D-06 | **PR-3** — was interaction shape used naturally with richer semantics? | Yes (§13), primed by the brief; weak-positive evidence. Recurrence: no. |
| OBS-8D-07 | Re-question path | No command re-questions a **non-expired** `Confirmed` row after an adjudication/premise change; `states.md` lists `Confirmed → Unknown` but the only executable route is `--revalidate`'s "changed" fallback, written for expired rows. Documentation-level gap; used as-is; nothing repaired. |
| OBS-8D-08 | `/revisit` precondition | `_simulation/counterfactuals/` absent (no `/simulate` in Pilot 1) → `/revisit` would stop at "missing counterfactual" if escalation were ever needed. Pilot-2 note: run `/simulate` before `/decide`. |
| OBS-8D-09 | Minor v05 vocabulary incoherence | SAP read reference recorded as `access_mode: virtualized` + `pattern: direct` although no virtual table over SAP was established — not flagged in Pilot 1; corrected in v06 (`keep-in-place`, mechanism UNKNOWN, non-structural). |
| OBS-8D-10 | DK pull cost | Units were read in full to locate sections (heavier than "one unit per section"); no effect on the result. |
| OBS-8D-11 | Dashboard hook | `on-su-change.py` regenerated `dashboard.html` on the SU/blueprint tool writes — runtime execution, not modification. Appends made through the shell (answers, council-log, story, blueprint-log) do not fire the hook; `dashboard.py` was run once explicitly at the end to bring the page up to date (deterministic generator, sanctioned execution). |
| OBS-8D-12 | Blueprint YAML strictness | `ux-blueprint_v05.yaml` (approved, frozen) is not strictly parseable YAML: `replacement_of_existing_artefact` is indented inside the `irreversible_choices` list (v05 A9 addition). The runtime reads blueprints as text, so nothing failed in Pilot 1. v06 places the key as a sibling of `irreversible_choices` (same meaning) and parses cleanly; v05 is left untouched (frozen). Documentation-level observation for the render/blueprint contracts. |

`RUNTIME DEFECT OBSERVED DURING REVISIT: NO` — OBS-8D-07 and OBS-8D-08 are documentation/coverage gaps
recorded for later adjudication; nothing misbehaved. `RUNTIME MODIFIED DURING STEP 8D: NO`.

---

## 24. Next action

1. `/answer U-036` with IT central / the DB-operating team (basis B: topology, identity, schema owner, PK/triggers, current connection usage) — the highest-swing item.
2. `/answer U-040`, `/answer U-037`, `/answer U-038` with the sponsor / governance (workflow-state placement; hard row/column requirement; audit events/consumer).
3. `/answer U-039`, `/answer U-034`, `/answer U-033` with the sponsor / analyst (what-if interactivity; Monday sparsity; BIOS consumer).
4. Run proof obligations 2–4 (inspection, spike, audit proof) as U-036 allows; then `/blueprint --refresh` → v07 → business approval → `/synthesize` → `/render --all` (re-render of the 5 stale deliverables; Estimate re-rendered, never edited).
5. Pilot 2 proceeds independently from `step-8c-baseline` (`pilot-2-protocol.md`); OBS-8D-05/07/08 go to its watch list.

---

## 25. Final verdict

The repaired runtime, used at the exact point where Pilot 1 failed, did not let the connectivity fact become
a fit conclusion again; it forced the mechanism question per domain, exposed that the engagement has never
established that mechanism, and produced an architecture that is coherent as a **candidate** (SQL-side engine;
per-domain virtualization or connector access under a still-unknown identity; owned or SQL-side workflow and
audit; a task-shaped surface composition) but **not yet evidence-backed**. The selected decision remains
defensible under its own conditions; the architecture remains open until IT evidence and a measured spike
close it. That is the honest answer to the Step 8D question — and preferable to a corrected blueprint approved
on the strength of a likely direction.

```text
STEP 8D — PRICING-MARINHA TARGETED ARCHITECTURE REVISIT: PASS
STEP 8C CHECKPOINT USED: step-8c-baseline = 7e977cd562b25c74925347ae4a17bebb6902243e
PACK VERSION: 1.8.2
PREVIOUS CHAT TRANSCRIPT REQUIRED: NO
TARGETED RAW/NORMALIZED EVIDENCE PULL REQUIRED: YES
A-009 STARTED AS UNKNOWN: YES
C-062 USED AS ARCHITECTURE FIT EVIDENCE: NO
SQL GATEWAY/CONNECTION VERIFIED: SECOND-HAND
SPECIFIC DATA-ACCESS MECHANISM IDENTIFIED PER MATERIAL DOMAIN: PARTIAL
MECHANISM FIT AGAINST MATERIAL CONTROLS: PARTIAL
SECURITY BASIS REVALIDATED: YES
AUDIT BASIS REVALIDATED: YES
CALCULATION ENGINE LOCATION EXPLICIT: YES
MON/TUE BEHAVIOUR PRESERVED: YES
OUTPUTS BIOS REPRESENTED: YES
SIMULADOR / WHAT-IF REPRESENTED: YES
FOUR UNIT OUTPUT FAMILY REPRESENTED: YES
INTERACTION SHAPE NATURALLY EVALUATED: YES
PR-3 RECURRENCE OBSERVED: NO
PRIMARY EXPERIENCE SURFACE: OPEN
C-057 TARGETED REVALIDATION EXECUTED: YES
C-057 CAUSED WHOLESALE RERUN: NO
O-004 SECURITY STRENGTH SURVIVES: PARTIAL
O-004 AUDIT STRENGTH SURVIVES: PARTIAL
U-028 STATUS: COMPARATOR EVIDENCE ABSENT
D-002 DECISION REMAINS DEFENSIBLE: YES
DECISION REVISIT REQUIRED: NO
CORRECTED BLUEPRINT VERSION: v06
CORRECTED BLUEPRINT APPROVED: NO
STRUCTURAL OPEN CHOICES REMAINING: 4
PROOF OBLIGATIONS REMAINING: 5
IMPLEMENTATION SPEC STALE: YES
ESTIMATE STALE: YES
CLAUDE DESIGN BRIEF STALE: YES
RUNTIME DEFECT OBSERVED DURING REVISIT: NO
RUNTIME MODIFIED DURING STEP 8D: NO
PACK VERSION CHANGED: NO
PRICING-MARINHA ARCHITECTURE NOW DEFENSIBLE: NO
READY TO RERENDER AFFECTED DELIVERABLES: NO
READY FOR PILOT 2: YES
```
