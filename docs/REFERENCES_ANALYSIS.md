# References Analysis — Old aisa → aisa v2 PP pack transplant proposal

- **Date:** 2026-05-28
- **Source analysed:** `C:\Users\jorge.estevao\Documents\Galp\Claude Code\skill\references\`
- **Target:** `C:\Users\jorge.estevao\Documents\Galp\Claude Code Projects\aisa\library\packs\pp\`
- **Note:** this is a proposal. The aisa v2 pack is read-only at runtime — the user decides what to transplant via an out-of-band edit.

---

## 1. Triage table

| Ref file | Classification | One-line reason |
|---|---|---|
| `ref-00-state-index.md` | IGNORE — pipeline | State-skeleton index; obsolete (v2 uses Shared Understanding, not the old state JSON). |
| `ref-01-excel-patterns.md` | DOMAIN | Excel → Power Fx / T-SQL translation catalogue. No v2 counterpart. |
| `ref-02-dataverse.md` | DOMAIN | Dataverse reference (types, rollups, business rules, licensing). No v2 counterpart. |
| `ref-03-azure-sql.md` | DOMAIN | Azure SQL reference (medallion, RLS, MERGE, temporal tables). No v2 counterpart. |
| `ref-04-sharepoint.md` | DOMAIN | SharePoint reference (12-index limit, 5K threshold, OData). No v2 counterpart. |
| `ref-05-powerfx.md` | DOMAIN | Power Fx patterns — already direct-ported into `domain-knowledge/powerfx-patterns.md`. |
| `ref-05b-powerfx-validator.md` | DOMAIN | Power Fx validation sequence — already absorbed as §3 of v2 `powerfx-patterns.md`. |
| `ref-06-security.md` | DOMAIN | Security model — already direct-ported into `domain-knowledge/security-patterns.md`. |
| `ref-07-anonymization.md` | DOMAIN | Anonymisation pools (PT/EN), NIF/IBAN generators, sensitivity types. No v2 counterpart. |
| `ref-08-estimation.md` | DOMAIN | Effort table, phase structure, risk register, licensing prices. No v2 counterpart. |
| `ref-09-flows.md` | DOMAIN | Power Automate patterns, adaptive cards, OData, expressions. No v2 counterpart. |
| `ref-10-screen-patterns.md` | DOMAIN | Screen patterns — already direct-ported into `domain-knowledge/screen-patterns.md`. |
| `ref-12-qa.md` | HYBRID | Pipeline-keyed (Agent NN), but the rule families (D/S/P/E/M sections) are domain-coherent. |
| `ref-12-qa-universal.md` | IGNORE — pipeline | Confidence calibration / flag counting per agent; obsolete (v2 has 5 knowledge states). |
| `ref-14-traceability.md` | IGNORE — pipeline | Traceability-matrix schema; obsolete (v2 uses SU `was X-NNN` lineage). |
| `ref-15-decision-trees.md` | IGNORE — pipeline | Index file pointing to `decision-trees/dt-NN-*.md`. |
| `ref-16-document-extraction.md` | IGNORE — pipeline | Agent-00b extraction rules; obsolete (v2 uses inputs/ free-form). |
| `ref-18-python-forensics.md` | IGNORE — pipeline | Python forensics for Excel; obsolete in v2 (no Python execution stack). |
| `ref-docx-gen.md` + `docx-templates/*` | IGNORE — pipeline | Old docx generation; v2 deliverables are markdown templates already present in `deliverable-templates/`. |
| `docx-base.js` | IGNORE — pipeline | JS for docx rendering. |
| `ref-agent-common-protocol.md` | IGNORE — pipeline | Agent contract; obsolete (v2 uses native Claude Code skills/agents). |
| `ref-error-recovery.md` | IGNORE — pipeline | Pipeline error recovery; obsolete. |
| `ref-pipeline-modes.md` | IGNORE — pipeline | Pipeline mode selection; obsolete. |
| `ref-resume.md` | IGNORE — pipeline | Session resume; obsolete (v2 uses `_state.json` + `/resume`). |
| `ref-session-groups.md` | IGNORE — pipeline | Session-relay grouping; obsolete. |
| `ref-session-management.md` | IGNORE — pipeline | Session-relay management; obsolete. |
| `ref-skip-handler.md` | IGNORE — pipeline | Skip-phase logic; obsolete (v2 has soft gates). |
| `ref-state-skeletons.md` | IGNORE — pipeline | Old state JSON skeletons; obsolete. |
| `ref-token-tiers.md` | IGNORE — pipeline | HOT/WARM/COLD token tiers; obsolete (v2 loads on demand). |
| `SESSION_RELAY_TEMPLATE.md` | IGNORE — pipeline | Cross-session handoff template; obsolete. |
| `ref-requirements.json` | IGNORE — pipeline | JSON requirements schema; obsolete. |
| `ref-ex-*.md` (00, 01, 01a, 01b, 02, 03, 04, 05, 06, 07, 08, 10, 11, 12) | IGNORE — pipeline | Per-agent output format anchors; obsolete. |
| `decision-trees/dt-01-sheet-classification.md` | IGNORE — pipeline | Excel-sheet classifier for Agent 01; obsolete. |
| `decision-trees/dt-02-column-role.md` | IGNORE — pipeline | Excel-column classifier for Agent 01; obsolete. |
| `decision-trees/dt-03-technology.md` | HYBRID | Pipeline-keyed but the SharePoint/Dataverse/SQL disqualification gates + scoring are pure domain. |
| `decision-trees/dt-04-screen-consolidation.md` | DOMAIN | Screen-consolidation rules (8/16-field thresholds, role splits, caps). No v2 counterpart. |
| `decision-trees/dt-05-conflict-blocking.md` | IGNORE — pipeline | Phase-02 conflict gating; obsolete. |
| `decision-trees/dt-06-schema-rigor.md` | HYBRID | Per-platform reserved-word + type-coherence checks are domain; phase-keying is pipeline. |
| `decision-trees/dt-07-cross-phase-coherence.md` | IGNORE — pipeline | Cross-phase coherence (C1–C11) referencing Agent NN; obsolete (v2 Chairman handles this). |

---

## 2. Comparative analysis

### 2a. DOMAIN files that DUPLICATE v2 (deltas only)

**`ref-05-powerfx.md` vs `powerfx-patterns.md`** — v2 is a strict superset. v2 added §3 (validation sequence merged from `ref-05b`) and reorganised section numbering. No net-new content in the ref.

**`ref-05b-powerfx-validator.md` vs `powerfx-patterns.md` §3** — fully absorbed. Identical structure (A1–A5 syntax, B1–B3 schema, C1–C5 logic, D report format).

**`ref-06-security.md` vs `security-patterns.md`** — direct port. v2 dropped the "Azure SQL RLS view" subsection from Section E (`vw_app_quote_comercial` example with role-specific column hiding). Worth merging back — see §3.

**`ref-10-screen-patterns.md` vs `screen-patterns.md`** — direct port; identical body. Only difference is v2 removed the "Agent 10 output" framing in §15. No net-new content in the ref.

### 2b. DOMAIN files with NO v2 counterpart (summaries)

**`ref-01-excel-patterns.md`** (Excel → Power Fx / T-SQL translation catalogue):
- Arithmetic / Conditional / Lookup / Aggregation / Text / Date / Financial / Array tables, side-by-side Excel ↔ Power Fx ↔ T-SQL.
- SUMPRODUCT Power Automate pattern (running-total pseudocode) and PMT / IRR T-SQL implementations.
- WORKDAY approximation in Power Fx (with the warning that it ignores holidays).
- This is the *core* knowledge for discovery-driven Excel → Power Platform migrations. High value, zero v2 overlap.

**`ref-02-dataverse.md`** (Dataverse complete reference):
- Data-type matrix, reserved column names, relationship naming, calculated-column tiers.
- Rollup column limitations (12h staleness, recalc API), alternate keys, plugin-vs-flow decision matrix.
- Licensing impact on architecture (M365 Standard vs Per User vs Per App) — directly drives architectural branches.
- 7 anti-patterns table (FLOAT for currency, >150 Choice, Business Rule for critical validation, etc).

**`ref-03-azure-sql.md`** (Azure SQL complete reference):
- Medallion architecture (Bronze/Silver/Gold/Reference/Audit) — full naming conventions and column templates.
- SP template with TRY/CATCH + audit_executions wrapper.
- RLS implementation (`fn_access_filter` + `CREATE SECURITY POLICY` + `sp_set_session_context`).
- MERGE upsert pattern, temporal tables (`SYSTEM_VERSIONING = ON`), CTE patterns, index strategy.
- This file is what unlocks the `azure-sql-first` architectural branch — currently absent from v2's pack.

**`ref-04-sharepoint.md`** (SharePoint complete reference):
- Hard limits (12 indexes / 5000 items / 10 lookups), calculated-column supported-function list.
- Edit-own + sensitive-column protection via Power Automate (SharePoint has no native column/row security).
- OData filter syntax cheat sheet (lookup `/Id`, person `/EMail`, `startswith`, year/month functions).
- Growth-planning thresholds (2k / 5k / 20k / 100k+) with concrete actions per threshold.

**`ref-07-anonymization.md`** (Anonymisation pools + sensitivity types):
- Detection signals + replacement methods for 8 sensitivity types: names, emails, phones, NIFs/tax IDs, addresses, financial values, company names, IBANs.
- PT and EN name pools, PT street/city pools, PT IBAN check-digit algorithm, NIF check-digit algorithm.
- Synthetic-data distributions (date recency bias, qty skewed-low, choice proportions).
- Real PT bank codes to NEVER use (CGD/BPI/Santander/BCP/BIC/Crédito Agrícola).

**`ref-08-estimation.md`** (Implementation estimation model):
- Effort table: days per component per technology (SP / Dataverse / SQL columns); 1.0× / 1.2× / 1.5× complexity multipliers; 20% buffer.
- Phase 0–7 structure with overlap rules (Phase 7 always ≥2 weeks parallel operation with Excel).
- Standard team composition + standard 6-risk register + license cost ranges (€/user/month).
- Quick-wins criteria, 7 estimation anti-patterns, uncertainty handling rules.

**`ref-09-flows.md`** (Power Automate patterns):
- Connector reference (call-rate limits per system), 5-tier flow category (Ingestion / Calculation / Publication / Monitoring / Approval).
- Ingestion / Calculation / Publication / SP-orchestration templates with full pseudocode.
- Error-handling patterns (Run After / Try-Scope-Catch / exponential retry / 429 handling), child-flow contract.
- Adaptive Card JSON template for Teams approvals (PT), OData filter table, expression catalogue (text/date/logic/array).

**`ref-12-qa.md`** (HYBRID — domain rule families):
- Section B (Data Integrity D01–D08), Section C (Schema S01–S09), Section D (Power Fx P01–P10), Section E (Security E01–E07), Section H (Estimation M01–M09).
- Rule IDs are pipeline-keyed (Agent NN) but the rules themselves are domain quality gates that the SU / lenses should enforce.

**`decision-trees/dt-03-technology.md`** (HYBRID — domain gates):
- DT-03a hard disqualification thresholds (SharePoint disqualified if >30k rows / >100 formulas / cross-list joins; Dataverse disqualified if premium rejected; Azure SQL disqualified if no SQL skills + no budget).
- DT-03b weighted-scoring dimensions (volume / complexity / integration / skill / migration-risk weights).
- DT-03c–f scoring, tiebreakers, hybrid trigger, coherence validation.
- This is essentially the *quantitative* version of v2's `decision-tree.md`. v2 has 6 rules with qualitative verdicts; the ref has hard cutoffs (>30k rows, >100 formulas) that would *strengthen* v2's R1–R6.

**`decision-trees/dt-04-screen-consolidation.md`** (Screen consolidation thresholds):
- Field-count rules: ≤8 editable → single form, 9–16 → sections/tabs, >16 → wizard.
- Role-separation logic (same fields / overlapping / different).
- Hard caps: max 3 entities per screen, max 12 visible editable fields, max 5 action buttons.
- Naming convention: `[Entity]ListScreen` / `[Entity]FormScreen` / `[Entity]DashboardScreen`.

**`decision-trees/dt-06-schema-rigor.md`** (HYBRID — per-platform type matrices):
- DT-06b reserved-word check (Dataverse / Azure SQL / SharePoint).
- DT-06c type-coherence rules per platform (Money 4-decimal max in Dataverse, DECIMAL(p,s) bounds in SQL, SharePoint multi-line 63KB limit).
- DT-06d FK consistency (CASCADE / RESTRICT / SET NULL must be explicit), DT-06g sensitivity-type enumeration (11 types).

---

## 3. Recommendations

### 3a. Transplant as-is (net-new, no v2 counterpart)

Suggested target paths inside `library/packs/pp/domain-knowledge/`:

1. **`excel-patterns.md`** ← `ref-01-excel-patterns.md` (Excel → Power Fx / T-SQL translation catalogue).
2. **`dataverse-reference.md`** ← `ref-02-dataverse.md` (Dataverse types / rollups / business rules / licensing).
3. **`azure-sql-reference.md`** ← `ref-03-azure-sql.md` (medallion / RLS / SP template / temporal tables).
4. **`sharepoint-reference.md`** ← `ref-04-sharepoint.md` (12-index / 5K threshold / OData / sensitive-column workarounds).
5. **`anonymization.md`** ← `ref-07-anonymization.md` (PT/EN pools, NIF/IBAN algorithms, sensitivity-type enum — consumed by data lens and synthetic-data needs).
6. **`flows-patterns.md`** ← `ref-09-flows.md` (PA connector limits, flow categories, adaptive cards, OData).
7. **`estimation-model.md`** ← `ref-08-estimation.md` (effort table, phases, risks, licensing — consumed by `estimate.template.md` and CFO lens).
8. **`screen-consolidation-rules.md`** ← `dt-04-screen-consolidation.md` (field-count / role / cap rules — could also merge into `screen-patterns.md` §14 instead).

> All eight are pack-internal domain references. Naming PP / SharePoint / Dataverse / Azure SQL inside these files is allowed (the v2 no-tech-before-options rule applies to *lens prose in Discovery*, not pack-internal references consulted in Options).

### 3b. Merge with existing (deltas worth bringing in)

1. **`security-patterns.md` ← add Azure SQL RLS view example** from `ref-06-security.md` Section E (`vw_app_quote_comercial` showing role-specific column hiding via view definitions). v2 currently drops this single subsection.
2. **`decision-tree.md` (PP architectural branches) ← merge quantitative gates from `dt-03-technology.md`** as a new section:
   - Move v2's R1–R6 to keep as qualitative verdicts, but add an **R0 — Hard gates** section mirroring DT-03a (SharePoint disqualified if `max_volume > 30k`, cross-list joins, `formula_count > 100`, financial precision >2 decimals, audit required, multi-stage approval).
   - Add the **DT-03e hybrid trigger** as a sidebar (when ≥2 simple entities + ≥2 complex entities → hybrid).
3. **`screen-patterns.md` §14 ← add `dt-04` field-count caps** (≤8 / 9–16 / >16 editable, max 3 entities per screen, max 12 visible fields, max 5 buttons) and the entity-prefixed naming.
4. **`question-bank.md` and lens skill files ← seed the QA rule families** from `ref-12-qa.md` as "facts to confirm or risk acceptance" — e.g., D01 "every spreadsheet sheet must be classified" (operations lens), S07 "SharePoint never >12 indexed columns" (technology lens / Options), E01 "no blank cell in permission matrix" (governance lens).
5. **Optional — `dataverse-reference.md` post-merge ← absorb DT-06b/c/d/g** from `dt-06-schema-rigor.md` as a "Per-platform schema-validation matrix" appendix (reserved words, type bounds, sensitivity enumeration).

### 3c. Skip

- All session/pipeline/state files (`ref-state-skeletons.md`, `ref-pipeline-modes.md`, `ref-token-tiers.md`, `ref-resume.md`, `ref-session-*.md`, `SESSION_RELAY_TEMPLATE.md`, `ref-error-recovery.md`, `ref-skip-handler.md`).
- All Agent-NN protocols (`ref-agent-common-protocol.md`, all `ref-ex-NN.md`).
- All Excel-forensics + document-extraction (`ref-18-python-forensics.md`, `ref-16-document-extraction.md`) — v2 has no Python stack and reads `inputs/` free-form.
- `ref-12-qa-universal.md` — the confidence-flag-counting system contradicts v2's 5-state model.
- `ref-14-traceability.md` — v2's `was X-NNN` SU lineage replaces this.
- `ref-15-decision-trees.md` index — re-create as a pack-internal index after transplant.
- The docx generators (`ref-docx-gen.md`, all `docx-templates/*.md`, `docx-base.js`) — v2 deliverables are markdown.
- `dt-01-sheet-classification.md` and `dt-02-column-role.md` — Excel-specific Agent-01 classifiers, irrelevant in v2.
- `dt-05-conflict-blocking.md` — phase-02 conflict gating (replaced by SU `Conflicted` state).
- `dt-07-cross-phase-coherence.md` — replaced by Chairman synthesis.

---

## 4. Red flags

Items in references that violate v2 invariants (and how to handle on transplant):

1. **Old vocabulary — STRIP on transplant:**
   - "Agent NN", "Agent 03/04/05/etc.", "Phase 01–13", "Phase 02 answers", "CP-A", "CP-B" — all over `ref-12-qa.md`, the decision trees, and most pipeline files. Anything transplanted into `domain-knowledge/` must be rephrased to phase-neutral or consumer-neutral (e.g., "consumed by the data lens" instead of "Agent 04").
   - "`[FACTO]` / `[HIPÓTESE]` / `[DOC-FACTO]` / `[DISCOVERED_LOGIC]`" origin tags (in `dt-06-schema-rigor.md` and `dt-05-conflict-blocking.md`) — v2 uses the 5 states (`Confirmed / Assumed / Unknown / Conflicted / Risky`). Drop tag references or map: `FACTO → Confirmed`, `HIPÓTESE → Assumed`, `DOC-FACTO → Confirmed (doc-evidenced)`.
   - "`meta.decision_log[D-001]`", "state schema", "`schema.entities_generated[]`", "`data_map.formula_count`", "`excel.forensics.*`" — drop all references to the old state object. v2 references SU rows by their SU-id.
   - "Pipeline mode (fast / standard / forensic)" — obsolete; v2 has no pipeline-mode concept.
   - "Confidence band 🔴×N 🟡×N" — replaced by 5-state coverage.
   - I did not see "Claim Ledger" / "Wave" / "Cell" anywhere in the references — those vocabulary leaks are absent.

2. **Vendor-name leakage location check:** All vendor-named content (Dataverse, SharePoint, Azure SQL, Power Automate, Canvas Apps) appears in files that would become pack-internal `domain-knowledge/` references — consumed only in Options + Decision. This is *correct* per the v2 rule. No leakage into would-be Discovery lens prose.

3. **Frontmatter assumptions:** `dt-NN-*.md` files use YAML frontmatter (`Consumer: agent-NN`). v2's decision-tree.md *does* use frontmatter (line 1–22) so this convention is compatible, but the keys (`consumer:`, `consumed_by:`) need updating to v2 lens / phase names (`consulted_by: [lens-technology, solution-architect]`).

4. **PT-locale assumption:** `ref-08-estimation.md` license prices and `ref-07-anonymization.md` IBAN/NIF logic are PT-specific. Worth keeping (the PP pack is implicitly Galp/PT-centric) but should be flagged in a header note: "Numbers and pools are PT-locale defaults — adapt per engagement."

5. **Hard-currency price tables in `ref-08-estimation.md`:** lists "Power Apps per user ~€18-20" etc. These dates from ~2024. Transplant with the existing "Preços indicativos — confirmar com Microsoft CSP" footnote intact; flag for periodic refresh on each Power Platform release wave.
