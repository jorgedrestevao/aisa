---
template_id: process-model
output_path: _capture/process-model.md
sources:
  - _capture/*.extraction.json
  - _capture/*.replay.md
  - context.json
synthesis_prompt: |
  Reconstruct the as-is process logic that the input file(s) encode — as evidenced
  business rules plus an interrogation list for humans. Work ONLY from the extraction
  JSON(s) and replay report(s); open the raw file only to resolve a doubt, never to
  invent beyond it. Every rule cites a cell/range. What the artefact implies but
  cannot prove becomes a question, not a claim. Stamp every rule with the source file's
  modified date (not today) and a decay class, and price every interrogation row with
  custo + swing — the kernel's epistemic contract applies to captured knowledge exactly as
  it does to knowledge a human gave you. Neutral language: naming the current
  tooling ("an Excel file on a shared drive") is current-state and allowed; naming
  solution vendors/products is forbidden (Discovery-facing document).
---

# Process Model — {{slug}}

> Sources: {{files + sha256 first 8 chars, comma-separated}}  |  Generated: {{ISO-8601}}  |  Capture run: {{N}}

## 1. File map

<Per file: one short block. Per sheet: what it appears to be (register / lookup / archive /
report / staging), its visibility (visible/hidden/veryHidden — hidden sheets are a finding),
row/column volume, and how sheets reference each other (from the dependency graph). Cite
sheet names verbatim.>

## 2. Column classification

<One table per sheet, from the extraction JSON's column classes:>

| column | header | class (input/derived/manual) | evidence |
|---|---|---|---|
| <letter> | <header> | <class> | <dominant formula pattern, or "typed values"> |

<After each table, flag every **manual** column explicitly: **manual column = human process
step** — someone types/maintains this by hand. These anchor §4's narrative and §6's questions.>

## 3. Business rules (PM-NNN)

| id | rule (natural language) | state | evidence | verificado_em | validade |
|---|---|---|---|---|---|
| PM-001 | <the rule as a business statement> | Confirmed \| Assumed | <sheet!range + formula / validation / conditional-format rule> | <ISO date> | <decay class> |

<state ∈ {Confirmed, Assumed} ONLY. Confirmed = a formula, data-validation rule, or
conditional-formatting rule proves it. Assumed = inferred from structure (declare the basis
in the evidence cell). NEVER a rule without a cell citation.

**Epistemic stamping** (kernel v0.2.0, `library/kernel/states.md` → *Epistemic half-lives*).
`verificado_em` = the input file's **modified timestamp** (L1 extraction JSON →
`identity.modified`), NOT the capture-run date: a rule extracted from a file last edited in
January is January's evidence, however fresh the parse. `validade` = `organizacional` by
default; use `legal-regulatorio` for retention/audit rules, `financeiro` for rates/limits,
`volatil` for current operational state. A file older than its class's half-life produces
rows that are **born expired** — correct and useful: /status raises the re-question instead
of the model claiming settled knowledge. State the file's age in §1 when it exceeds a
half-life. Ids are stable across re-runs:
keep the id of a rule that persists, retire ids of rules that disappeared (log retirement in
`_capture-log.md`), append new rules with the next free id.>

## 4. Implicit process narrative

<3-6 paragraphs: the workflow this artefact implies — stages, handoffs, cadence, actors
(by role, from comments/authors/manual columns). EVERY claim cites a PM-NNN or sheet!range;
an uncited sentence is a template violation to be logged in `_capture-log.md`. Neutral
language — no vendor/product names for solutions; naming the current tool is allowed.>

## 5. Anomalies & silent failures

<Replay findings promoted, most severe first. One row per finding kept relevant:>

| severity | finding | location | consequence for the process |
|---|---|---|---|
| high | <from replay report> | <sheet!cell> | <what silently breaks> |

<If the replay report has 0 findings, state that explicitly — absence of findings is evidence.>

## 6. Interrogation list (PM-U-NNN)

<What the file implies but cannot prove. Each row is a candidate SU Unknown for the lenses:>

| id | question | why it matters | suggested respondent (role) | criticidade | custo | swing |
|---|---|---|---|---|---|---|
| PM-U-001 | <question> | <decision/risk it unblocks> | <role, not name> | Low \| Med \| Critical | email \| documento \| reuniao \| spike | <classe: frase> |

<`custo` and `swing` follow `library/kernel/states.md` → *Question economics*, so a lens can
promote the row to an SU Unknown without inventing them. `custo` = what it takes to get the
answer. `swing` = `decisivo` (changes which option survives) \| `dimensionante` (changes
sizing/effort/design) \| `cosmético` (changes nothing material), plus a phrase stating WHAT
changes. Derive both from the "why it matters" column — never leave them blank: an unpriced
question inherits the compatibility default (`email` / `dimensionante`) and a decisive
question then enters the engagement disguised as routine.>

## 7. Not captured

<Explicit list of everything outside mechanical reach: VBA modules, external links,
password-protected sheets, not-replayable formulas (copy the replay report's list),
hidden/veryHidden sheets not parsed. Each entry = an Unknown, never inferred.>
