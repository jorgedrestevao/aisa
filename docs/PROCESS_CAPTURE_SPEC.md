# Process Capture Module — Spec v1.0

> Status: SPEC — not yet built.
> Motivation: pilot (`dpt-galp-jp`) showed the as-is process logic lives largely *inside* the input Excel
> (formulas, manual columns, color-coding), but the current pipeline captures it accidentally — each lens
> re-parses inputs ad-hoc, 6× per round, with no guarantee of depth or consistency. This module makes
> capture systematic, evidenced, and single-pass.

## 1. Purpose & scope

Transform each engagement input file into:

1. A **deterministic extraction** of its structure and logic (machine artefact, cacheable).
2. A **process model** — the as-is logic reconstructed as evidenced business rules + an interrogation
   list for humans (LLM artefact, Discovery-facing).
3. A **replay report** — extracted rules re-applied to the data so silent failures surface mechanically
   instead of by luck.

**In scope (MVP)**: `.xlsx`/`.xlsm`. Other formats keep the current per-lens reading path.
**Out of scope (MVP)**: general formula evaluation engine, VBA decompilation, external-link resolution,
`.pdf`/`.docx` capture modules (same contract, later).

**Non-goals**: this module does NOT replace human discovery. The file is the *artefact* of the process,
not the process — pilot's structuring claims ("3 daily meetings", "5 manual steps") came from humans.
The module's job is to extract what the file can prove and convert what it cannot into questions.

## 2. Position in the pipeline

```
/start ──► scaffold ──► [capture: L1 extract ──► L3 replay ──► L2 process-model] ──► /round R-01 ...
```

- **Trigger**: last step of `aisa-start` when `inputs/` contains supported files; re-triggered by
  `aisa-round` step 3.5 whenever an input file's hash is missing/stale in `_capture/`; runnable
  manually via `/capture` (new command).
- **Order within capture**: L1 (deterministic) → L3 (deterministic, needs L1 output) → L2 (LLM, reads both).
- Lenses in Discovery consume the process model as primary evidence (see §7).

## 3. Artefacts

All derived artefacts live in `<engagement>/_capture/` (sibling of `_synthesis/`, `_render/`).
`inputs/` stays pure evidence — never written to.

| Artefact | Producer | Format |
|---|---|---|
| `_capture/<file>.extraction.json` | L1 script | machine, one per input file |
| `_capture/<file>.replay.md` | L3 script | findings report, one per input file |
| `_capture/process-model.md` | L2 skill | one per engagement, consolidates all inputs |
| `_capture/_capture-log.md` | all | append-only audit (mirrors `_synthesis-log.md`) |

## 4. Layer 1 — deterministic extraction

**Implementation**: `library/kernel/tools/xlsx_extract.py` (Python, `openpyxl` only, no LLM).
Canonical kernel asset — versioned, read/executed at runtime, never edited at runtime.

**Invocation**: `python library/kernel/tools/xlsx_extract.py <input.xlsx> <out.extraction.json>`

**Extracts per file**:

| Group | Fields |
|---|---|
| identity | filename, SHA-256, size, modified timestamp |
| sheets | name, visibility (visible/hidden/veryHidden), dimensions, frozen panes |
| columns (per sheet) | header, inferred type, null count, distinct count, min/max (numeric/date), top-5 values |
| formulas | **unique formula patterns per column** (normalized to R1C1 to detect fill-down), pattern coverage %, and **exception cells** — cells breaking the column's dominant pattern (= manual overrides; high-value process signal) |
| dependency graph | per derived column: which columns/sheets/ranges it reads (parsed from formula refs) — classifies every column as `input` / `derived` / `manual` (manual = typed values, no formula = human work) |
| named ranges | name, target, scope |
| data validation | rules per range (lists, bounds) — these ARE business rules |
| conditional formatting | rules per range (formula, operator, format) — implicit alerting logic |
| color-as-data | cell fills NOT explained by any conditional-formatting rule, enumerated as distinct fill → count per column (manual color-coding = state encoding invisible to pandas) |
| comments/notes | cell, author, text |
| anomaly scan | leading/trailing whitespace in key-like columns, mixed types within a column, duplicate values on candidate key columns |
| flags | VBA present (bool + module names if cheaply listable), external links (paths only), pivot tables (source ranges), password-protected sheets |

**Caching**: skip extraction when stored SHA-256 matches the current file. Log `cache-hit` to `_capture-log.md`.

**Failure**: unreadable/protected file → write extraction JSON with `"status": "failed", "reason": ...`;
never guess contents. L2 records it as Unknown.

## 5. Layer 3 — replay (deterministic validation)

**Implementation**: same script, `--replay` mode (needs the extraction JSON). NOT a general formula
engine — a fixed battery of targeted checks:

| Check | Method | Surfaces |
|---|---|---|
| lookup integrity | re-resolve `VLOOKUP`/`XLOOKUP`/`INDEX+MATCH` against in-file target sheets; diff recomputed vs stored | silent lookup failures (the pilot's trailing-space class — caught mechanically, not by luck) |
| key uniqueness | duplicate scan on candidate keys (id-like columns) | duplicate records, conflicting rows |
| whitespace/casing | `TRIM`/case-normalize keys, re-run lookup check | join defects |
| staleness | date columns vs today: aging distribution, rows beyond thresholds present in conditional-formatting rules | unescalated aging items |
| pattern exceptions | list L1's formula-exception cells with their values | manual overrides of automated logic |
| orphan references | formula refs to empty/missing ranges, broken named ranges | dead logic |

Formulas outside the supported set (external links, VBA-driven, array exotica) → listed as
`not-replayable` with location; L2 converts them to Unknowns. **Explicit rule: no check = no claim.**

**Output**: `_capture/<file>.replay.md` — one finding per row: check, location (sheet!cell), expected,
found, severity.

## 6. Layer 2 — process model (LLM reconstruction)

**Implementation**: skill `aisa-capture` (`.claude/skills/aisa-capture/SKILL.md`) + template
`library/kernel/capture-templates/process-model.template.md`. Single LLM pass reading extraction
JSON(s) + replay report(s) + `context.json`.

**Output — `_capture/process-model.md`, sections**:

```markdown
# Process Model — <slug>
> Sources: <files + hashes>  |  Generated: <ISO>  |  Capture run: <N>

## 1. File map
Per file: sheets, what each sheet appears to be (register/lookup/archive/report), visibility notes.

## 2. Column classification
Table per sheet: column | input/derived/manual | evidence (formula pattern or "typed values").
Manual columns are flagged: **manual column = human process step**.

## 3. Business rules (PM-NNN)
One row per reconstructed rule:
| id | rule (natural language) | state | evidence (sheet!range + formula/validation/format rule) |
- state ∈ {Confirmed, Assumed} only. Confirmed = formula/validation evidence. Assumed = inferred
  from structure (basis declared). NEVER invent a rule without a cell citation.

## 4. Implicit process narrative
3-6 paragraphs: the workflow the artefact implies (stages, handoffs, cadence), each claim citing
PM-NNN or sheet!range. Neutral language — no vendor/product names (Discovery-facing; naming the
current tool, e.g. "an Excel file on a shared drive", is current-state and allowed).

## 5. Anomalies & silent failures
Replay findings promoted with severity + PM/cell citation.

## 6. Interrogation list (PM-U-NNN)
What the file implies but cannot prove — one question per row: question | why it matters | suggested
respondent role. THIS FEEDS THE LENSES: each becomes a candidate SU Unknown.

## 7. Not captured
VBA, external links, protected sheets, not-replayable formulas — explicitly listed as Unknown.
```

**Hard rules** (mirror kernel): never invent; cite cells; no vendor names for *solutions* (current-state
tooling naming allowed); PM ids stable across re-runs (append-only log of changes in `_capture-log.md`;
re-generation overwrites the model file itself, like `_synthesis/`).

## 7. Integration contract (changes to existing assets)

| Asset | Change |
|---|---|
| `library/kernel/orchestration.md` §Reading input documents | Add: when `_capture/process-model.md` exists, lenses read it FIRST as primary evidence. Citing `PM-NNN` counts as "opened" because PM rows carry cell citations. Raw files remain available and authoritative on conflict. |
| every Discovery lens SKILL.md (6) | Inputs list gains `_capture/process-model.md` + replay reports. New step: **spot-check ≥1 PM claim against the raw file per round** before citing it (anti correlated-failure — if the model is wrong, 6 lenses must not inherit the error blind). Interrogation list items relevant to the lens → promoted to SU Unknowns with `quem responde`. |
| `aisa-start` SKILL.md | Step 11: if `inputs/` has supported files → run capture (L1→L3→L2), report summary. |
| `aisa-round` SKILL.md | Step 3.5: hash-check `_capture/` vs `inputs/`; stale/missing → re-run capture before lenses. |
| `phases.md` Discovery | Entry criteria gains: "capture run for supported inputs (soft — warn if missing)". |
| `.claude/commands/capture.md` | New `/capture [file]` command → `aisa-capture` skill. |
| SU provenance | Lens rows citing the model use evidence format `PM-NNN → Sheet1!D2:D400` — traceable to cell through the PM id. |

**Council phases**: personas receive `process-model.md` in their briefing package (it is small and dense —
better signal per token than raw re-parsing).

## 8. Degradation & failure modes

| Situation | Behaviour |
|---|---|
| no supported files in `inputs/` | capture skipped silently; lenses use current path |
| extraction fails | `status: failed` JSON + Unknown in PM §7; lenses fall back to raw reading |
| replay finds nothing | empty §5 with "0 findings" — absence of findings is itself evidence, log it |
| PM contradicts raw file (lens spot-check) | lens records **Conflicted** SU row citing both; capture re-run flagged |
| password/VBA/external | Unknown, never inferred |

## 9. Multi-version capture (v1.1 — spec'd, not MVP)

Daily-operated files (pilot: `Dayly_pending_tickets`) hide the process in the **delta**, not the state.
When `inputs/` holds ≥2 versions of the same stem: `--diff` mode produces `_capture/version-diff.md` —
rows added/removed/changed per version pair, per-column change frequency (columns that change daily =
the actual manual work), cadence estimate. Deferred: needs multi-file collection discipline from
consultants first.

## 10. Build plan

| # | Item | Type | Est. |
|---|---|---|---|
| 1 | `library/kernel/tools/xlsx_extract.py` (L1 + L3 `--replay`) | Python, deterministic | the bulk — ~400-500 lines, unit-testable against the pilot xlsx |
| 2 | `library/kernel/capture-templates/process-model.template.md` | template | small |
| 3 | `.claude/skills/aisa-capture/SKILL.md` + `.claude/commands/capture.md` | skill/command | small |
| 4 | Amend `orchestration.md`, `phases.md`, `aisa-start`, `aisa-round` | edits | small |
| 5 | Amend 6 lens SKILL.md (inputs + spot-check step) | edits | small, repetitive |
| 6 | Validation run against `dpt-galp-jp/inputs/*.xlsx` — must rediscover the trailing-space defect, the duplicate ticket, and the 120-day aging mechanically | test | acceptance gate |

Order: 1 → 6 (script proven against pilot data first) → 2-5 → re-run 6 end-to-end.

**Acceptance criterion**: capture on the pilot file reproduces, without lens involvement, the three
defects Discovery found manually (duplicate `I260309_000413`, trailing-space lookup failure, >120-day
aging) — each as a replay finding with cell citation.

## 11. Risks

| Risk | Mitigation |
|---|---|
| Correlated failure: wrong PM poisons 6 lenses | per-lens spot-check mandate (§7); raw always authoritative; Conflicted row on mismatch |
| Scope creep toward a formula engine | fixed check battery (§5); "no check = no claim"; anything else → Unknown |
| Excel over-fit in the kernel | capture contract is format-agnostic; `xlsx_extract.py` is the first module, `pdf`/`docx` slot in later under the same artefact contract |
| False authority of §4 narrative | narrative must cite PM ids; uncited sentences are a template violation logged to `_capture-log.md` |
| Library read-only vs runtime execution | script is read+executed only; outputs go to `<engagement>/_capture/` — no runtime writes to `library/` |
