---
name: aisa-capture
description: Process-capture pipeline for engagement inputs — L1 deterministic extraction + L3 replay (script) + L2 process model (LLM). Runs at the end of aisa-start, on stale hashes in aisa-round step 3.5, or manually via /capture. Produces _capture/ artefacts that Discovery lenses consume as primary evidence.
---

# aisa-capture

## Usage

`/capture [file]`

- No argument: capture every supported file in `<engagement>/inputs/`.
- `[file]`: capture only that input file (filename, not path).

Also invoked programmatically by `aisa-start` (step 11) and `aisa-round` (step 3.5).

## What it produces (all under `<engagement>/_capture/`)

| Artefact | Layer | Producer |
|---|---|---|
| `<file>.extraction.json` | L1 | `library/kernel/tools/xlsx_extract.py` (deterministic) |
| `<file>.replay.md` | L3 | same script, `--replay` (deterministic) |
| `process-model.md` | L2 | this skill (LLM), template `library/kernel/capture-templates/process-model.template.md` |
| `_capture-log.md` | all | append-only audit |

`inputs/` stays pure evidence — never written to.

## Supported formats (MVP)

`.xlsx`, `.xlsm`. Other formats keep the normal per-lens reading path (`library/kernel/orchestration.md` → *Reading input documents*); they are NOT captured and NOT logged as failures.

## Execution steps

1. **Resolve the engagement root** (as in `aisa-start`): `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, else `projects/<slug>`. Read `_state.json` for the slug and capture-run counter (`capture_run`, default 0).
2. **Enumerate targets**: supported files in `inputs/` (or the single named file). None → output "no supported inputs; capture skipped" and stop silently (soft, not an error).
3. **L1 — extraction** per file:
   ```
   python library/kernel/tools/xlsx_extract.py "<engagement>/inputs/<file>" "<engagement>/_capture/<file>.extraction.json" --log "<engagement>/_capture/_capture-log.md"
   ```
   (On Windows prepend `PYTHONIOENCODING=utf-8` / `$env:PYTHONIOENCODING='utf-8'`.)
   The script self-caches on SHA-256 (`cache-hit` when unchanged; `--force` to override).
4. **L3 — replay** per file (needs the fresh extraction JSON):
   ```
   python library/kernel/tools/xlsx_extract.py --replay "<engagement>/inputs/<file>" "<engagement>/_capture/<file>.extraction.json" "<engagement>/_capture/<file>.replay.md" --log "<engagement>/_capture/_capture-log.md"
   ```
   Exit 3 = stale/failed extraction → re-run L1 once, then retry; still failing → record and continue (degradation table below).
5. **L2 — process model** (single LLM pass, only after ALL files did L1+L3):
   a. Read every `_capture/*.extraction.json`, every `_capture/*.replay.md`, and `context.json`.
   b. Fill `library/kernel/capture-templates/process-model.template.md` → write `_capture/process-model.md` (overwrite whole file, like `_synthesis/`). Carry `identity.modified` into every rule's `verificado_em`; when a file predates its decay class's half-life, say so in §1 — its rows are born expired and `/status` will raise the re-question.
   b2. **Size budget**: read the digest fields of each extraction JSON first (identity, sheets, column classes, formula-pattern summaries). Descend into a sheet's full detail only when a rule or finding needs it. Two pilots fit comfortably; if the JSONs together exceed roughly 200 KB, summarise per sheet before writing §2 rather than truncating silently.
   c. Increment `capture_run` in `_state.json` (atomically: tmp → rename) and stamp it in the model header.
6. **Log** to `_capture-log.md`: one `L2` line (`generated | run N | files: ...`), plus PM id changes (new/retired ids) when re-running.
7. **Output summary**: files captured (extracted / cache-hit / failed), replay finding counts by severity, top-3 highest-severity findings, PM rule + interrogation counts. One screen, no more.

## Hard rules (mirror kernel)

1. **Never invent.** Every PM-NNN rule cites sheet!cell/range evidence. No check = no claim: what L3 could not replay and L1 could not read is an Unknown in §7, never inferred.
2. **State ∈ {Confirmed, Assumed} only** in §3. Confirmed = formula/validation/CF evidence; Assumed = structural inference with the basis declared.
2b. **Stamp the epistemics** (kernel v0.2.0). Every PM rule carries `verificado_em` = the extraction JSON's `identity.modified` (the file's own last-edit date, NOT the capture run) and a `validade` decay class (`organizacional` default). Every PM-U row carries `criticidade`, `custo` and `swing` per `library/kernel/states.md` → *Question economics*. Unpriced questions inherit the compatibility default and a decisive question then enters disguised as routine — price them here, where the evidence is.
3. **No vendor/product names for solutions** — Discovery-facing. Naming the current tooling ("an Excel file on a shared drive") is current-state and allowed.
4. **PM ids stable across re-runs**: persisting rules keep their id; retired ids are logged in `_capture-log.md` and never reused; new rules take the next free id. Same for PM-U-NNN.
5. **Uncited narrative sentences in §4 are template violations** — log to `_capture-log.md`.
6. **Raw files stay authoritative**: on any conflict between the model and the raw file, the raw file wins and the lens records a Conflicted SU row (see lens skills).

## Degradation & failure modes

| Situation | Behaviour |
|---|---|
| no supported files | skip silently; lenses use the normal reading path |
| `openpyxl` not installed (script exits 2 with `requires openpyxl`) | capture **skipped, not failed**: report `capture skipped — openpyxl missing (pip install openpyxl)`, log it to `_capture-log.md`, lenses fall back to raw reading. Never an empty model: "could not run" is not the same evidence as "0 findings" |
| extraction fails (protected/corrupt) | script writes `status: failed` JSON; PM §7 records the file as Unknown; lenses fall back to raw reading |
| replay exit 3 after one L1 retry | note in `_capture-log.md`; PM §5 states "replay unavailable for <file>"; never guess findings |
| replay 0 findings | §5 says "0 findings" explicitly — absence of findings is evidence |
| model contradicts raw file (lens spot-check) | lens records **Conflicted** citing both; flag capture re-run in `_capture-log.md` |
