# Runtime Simplification — Phase B (Shared Evidence / Capture-lite) Report

<!--
provenance: IMPLEMENTATION (one new kernel tool + one new test; four contract/skill files touched)
scope: library/kernel/tools/text_extract.py, library/kernel/tools/tests/, .claude/skills/aisa-capture,
       .claude/skills/aisa-start (1 line), .claude/commands/capture.md (1 line),
       library/kernel/orchestration.md (2 lines)
authored: 2026-09-04
basis: runtime-simplification-plan.md §5 + §11 Phase B; phase-a-report.md §5 (deferred work)
path note: written to the repo's actual `research/pp/authoring/` directory
  (`docs/pp-pack-authoring/research/pp/authoring/`), alongside the plan and the Phase A report.
-->

## 1. Implementation summary

One deterministic script, one test file, one new artefact per text source, one index per engagement.
Nothing else moved.

`inputs/` → `aisa-capture` → deterministic extraction once → `_capture/` → shared evidence surface.

| Added | What |
|---|---|
| `library/kernel/tools/text_extract.py` (535 lines) | deterministic `.docx`/`.pdf`/`.vtt` → `<file>.text.md` + `<file>.extraction.json`; `--index` builds `evidence-index.md`. No LLM, no network |
| `library/kernel/tools/tests/test_text_extract.py` (516 lines, 23 tests) | the one new test the plan authorised (§4), plus the Excel regression |

Extended (not replaced): `aisa-capture` gains an **LT tier** alongside L1/L3/L2, and an index step that
always runs. `aisa-start` step 11 stops hard-coding `.xlsx`/`.xlsm` and defers the supported-format
list to `aisa-capture` — without that one line, text inputs would never trigger capture at all.
`orchestration.md` drops the two sentences that said capture-lite did not exist yet.

## 2. Existing capture reused

The xlsx tier is untouched. `xlsx_extract.py` was not opened for editing; its conventions were copied
rather than re-invented:

- same output directory (`_capture/`, flat) and same `<file>.extraction.json` naming;
- same SHA-256 self-cache with a `cache-hit` line and `--force`;
- same `_capture-log.md` table and `append_log` shape (new layer tag `LT`);
- same tmp → `os.replace` atomic write;
- same degradation philosophy: a failure artefact is always written, never an empty one, and
  "could not run" is never rendered as "0 findings".

`PM-NNN` remains xlsx-only and is written by nobody in the new path. The L2 process model (the only
LLM step in capture) stays scoped to `.xlsx`/`.xlsm`.

## 3. New extraction support

| Format | Library | Preserved | Marker |
|---|---|---|---|
| `.docx` | `python-docx` | heading hierarchy, paragraph order, tables, document order (paragraphs and tables interleaved as authored) | `### <heading>` (level+1, so a Word H1 sits under the file's `# Source:`), `[¶NN]` per paragraph, `[table N]` before each table |
| `.pdf` | `pypdf` | page boundaries, page order, per-page text | `## [p.N]`; a page with no extractable text says so instead of vanishing |
| `.vtt` | stdlib | speaker, time range, chronological (file) order, full utterance text | `[HH:MM:SS–HH:MM:SS] **Speaker:** text` |

VTT normalisation removes transport syntax only: `WEBVTT` header, `NOTE`/`STYLE`/`REGION` blocks, cue
ids, `-->` timing lines, inline tags, and the mid-sentence line wrapping that the format inserts.
HTML entities are decoded (`Jorge Estev&#227;o` → `Jorge Estevão`). Consecutive cues from the **same
named speaker** are merged into one passage carrying the run's start–end range; **unattributed cues
are never merged**, so a transcript without `<v>` tags keeps one line per cue.

Deliberately not implemented: PDF heading detection. The plan's §5 sketch suggested keeping "detected
heading lines" as `###`. Any such detection is a font/layout heuristic — i.e. interpretation — and it
would put capture in the business of labelling structure. The page is the deterministic boundary and
is the only one recorded.

## 4. Shared evidence location / shape

Flat, in the existing `_capture/`, matching the xlsx tier — no `documents/` subtree, no parallel model:

```text
<engagement>/_capture/
    evidence-index.md                 <- the one entry point
    <file>.xlsx.extraction.json       (L1, unchanged)
    <file>.xlsx.replay.md             (L3, unchanged)
    process-model.md                  (L2, unchanged)
    <file>.docx.text.md               (LT, new)
    <file>.docx.extraction.json       (LT, new — identity + status + unit counts only)
    _capture-log.md                   (append-only audit, unchanged shape)
```

`evidence-index.md` is one table for the whole engagement — **source · format · normalized evidence ·
status · cite as** — covering every file in `inputs/` regardless of tier, including the ones that are
not captured. It is a file listing, not a classification: no relevance, no ranking, no per-lens view.

Live result on `pricing-marinha` (5 sources, all `ok`): 2 docx → 117 and 157 paragraphs; 1 xlsx →
unchanged PM tier; 2 vtt → 1442 cues / 799 passages / 3 speakers, and 620 cues / 620 passages /
0 speakers. The 205 KB kick-off transcript becomes a 92 KB readable passage list; the second, with no
speaker tags, is left one line per cue rather than being stitched into an invented narrative.

## 5. Provenance model

Source-type appropriate, plain strings, **no new id namespace**. Locators go in the SU `evidência`
column, which already accepts them; `PM-NNN` is untouched and stays xlsx-only.

| Format | Cite as |
|---|---|
| `.docx` | `<file> · §<heading> ¶NN` |
| `.pdf` | `<file> · p.N` |
| `.vtt` | `<file> · [HH:MM:SS] <speaker>` |
| `.xlsx`/`.xlsm` | `PM-NNN → <sheet>!<cell>` (existing, unchanged) |

Each `.text.md` header repeats the file's identity (size, mtime, sha256), its status, its citation
format, and the path to its raw source. The `.extraction.json` carries identity + status + unit counts
only — enough for the `aisa-round` freshness check to work exactly as it does for xlsx.

## 6. Failure behavior

Visible, per-source, never epistemic. Capture reports a `status`; classifying evidence remains the
lens's job.

| Situation | Status | Effect |
|---|---|---|
| library missing (`python-docx`, `pypdf`) | `skipped` | reason in artefact + index + log; raw reading |
| encrypted / corrupt / unreadable | `failed` | reason in artefact + index + log; raw source untouched |
| image-only or scanned PDF (0 pages with text) | `failed` | reason names "no OCR in this tier"; raw source read directly |
| some pages without text | `ok` | per-page `_no extractable text on this page_`, counted in `units.pages_without_text` |
| `.vtt` with 0 cues, `.docx` with no paragraph or table | `empty` | stated explicitly — absence is evidence |
| unsupported format (`.pptx`, `.msg`, images) | `not captured` | not a failure; listed in the index with the raw path |
| missing file / unsupported format on the CLI | exit 2 | usage error, no artefact written |

One source failing never stops the others. No `Unknown`/`Risky`/`Confirmed` word appears in any
extraction artefact — asserted by a test.

## 7. Tests executed

`python library/kernel/tools/tests/test_text_extract.py` — **23 tests, OK** (~48 s, dominated by the
Excel regression). Fixtures are generated in a temp dir: a `python-docx` document, a hand-built
minimal uncompressed PDF (no extra dependency), and a VTT string. No binary blobs added to the repo.

| Group | Covers |
|---|---|
| `TestDocx` (3) | heading levels, `[¶NN]` numbering, table rendering + pipe escaping, document order, absence of interpretive vocabulary |
| `TestPdf` (2) | page-aware extraction and page order; image-only PDF fails visibly with the raw file intact |
| `TestVtt` (4) | timestamp + speaker markers, entity decoding, same-speaker merge, unattributed cues *not* merged, transport syntax dropped, empty transcript stated |
| `TestFailure` (4) | corrupt source → visible `failed` + raw byte-identical; failure is not an epistemic state; unsupported format and missing file are usage errors that write nothing |
| `TestIdempotency` (4) | second run is a cache-hit that does not even rewrite the file; `--force` re-extraction is byte-identical (only `extracted_at` differs in the JSON); a changed source does re-extract; three runs leave exactly two artefacts |
| `TestEvidenceIndex` (2) | every source listed with its correct status incl. `failed` and `not captured`; regeneration is byte-identical |
| `TestExcelRegression` (4) | capture-lite refuses `.xlsx`/`.xlsm`; artefact ids are distinct; **`xlsx_extract.py` re-extraction of the live `PREÇO BANCAS` workbook is equal to the committed artefact** (`sheets` + `workbook` + `identity.sha256`), and the L3 replay matches the committed report modulo the two run-date-relative lines (replay timestamp, staleness aging distributions); the index reports the xlsx tier, never a `.text.md` |

Also executed outside the suite:

- capture-lite on all 5 real `pricing-marinha` inputs → 4 extracted, xlsx untouched;
- `--index` → 5 sources, correct tier and status for each;
- re-run of all 4 text sources → 4 cache-hits, index byte-identical, no `.tmp` leftovers;
- `dashboard.py --engagement <slug>` on all 4 existing engagements → all build.

## 8. Files changed

**New**

1. `library/kernel/tools/text_extract.py`
2. `library/kernel/tools/tests/test_text_extract.py`

**Modified**

3. `.claude/skills/aisa-capture/SKILL.md` — LT tier in the artefact table; supported-formats table with
   the "extraction, never summarization" statement; step 2 split by tier; step 5b (LT); step 6
   (evidence index, always); steps 7–8 renumbered and extended; hard rules 7 and 8; five degradation rows.
4. `.claude/skills/aisa-start/SKILL.md` — step 11, one line: capture is invoked when `inputs/` has any
   file, and owns its own supported-format list.
5. `.claude/commands/capture.md` — description line.
6. `library/kernel/orchestration.md` — the capture-tier row for `.docx`/`.pdf`/`.vtt` (no longer
   "contract only; not implemented yet") and the sentence that said text formats are read raw until
   capture-lite exists (now: raw reading is the fallback for `failed`/`skipped`/`empty` and for formats
   outside the tiers).

**Generated engagement data** (`projects/` is a gitignored mount point): 4 × `.text.md`,
4 × `.extraction.json`, `evidence-index.md` under `projects/pricing-marinha/_capture/`, plus `LT` lines
in its `_capture-log.md`. Additive only — no existing artefact, SU row, or `_state.json` key changed.

**Note on the `library/` edits.** `library/` is read-only *at runtime*; items 1, 2 and 6 are out-of-band
authoring edits landing as git-tracked changes, the path sanctioned by `.claude/rules/library-readonly.md`
and the one Phase A already used for `orchestration.md`. The plan requires `text_extract.py` at exactly
this path. The user approved these three writes explicitly before they were made.

## 9. Deferred limitations

**Owned by later phases (not gaps in Phase B).**

- `aisa-round` step 3.5 still hashes only `.xlsx`/`.xlsm`, so a text source edited mid-engagement does
  not auto-recapture inside a round; `/capture` and `/start` cover it. Step 3.6 (carrying
  `evidence-index.md` into lens and persona invocations) is likewise unbuilt. Both are Phase D, which
  owns `aisa-round` — extending the freshness check here would have pre-empted that phase's payload
  change for no benefit in Phase B.
- Lens `Inputs` sections still tell each lens to read `inputs/` itself. Phase C. Until then the index
  exists but nothing is required to read it — which is the intended ordering (the plan's `Inputs` line
  may only promise an index once the index exists).

**Extraction-scope limits, deliberate.**

- No OCR. An image-only PDF is a visible `failed`, not a silent gap.
- No PDF heading detection (see §3).
- VTT merging keeps the run's start–end range; intermediate cue starts within a merged run are not
  individually addressable. A citation resolves to the run start. Raw `.vtt` stays authoritative.
- `.docx`: headers, footers, footnotes, comments and text-box content are not extracted; only
  `Heading N` / `Title` styles are recognised, so a document that expresses structure through numbered
  body text (both `pricing-marinha` docs — 100 % `Normal` style) yields 0 headings rather than invented
  ones. That is the correct behaviour under "do not invent semantic labels", and it is why those two
  files cite as `¶NN` alone.
- `.pptx`, `.msg` and images remain raw-read; adding them would be new parser work, not configuration.

## 10. Complexity check

| | Question | Verdict | Basis |
|---|---|---|---|
| A | New evidence state machine? | **NO** | 5 knowledge states untouched; `states.md` not edited; `status` is a per-file extraction outcome the script prints, with no transitions and no persistence beyond its own JSON |
| B | New evidence taxonomy? | **NO** | no new id namespace; `PM-NNN` stays xlsx-only; text locators are plain strings in the existing `evidência` column; `evidence-index.md` is a file listing |
| C | Evidence routing / scoring? | **NO** | the index has no relevance, rank, weight or lens column; which raw source to open stays the lens's judgement |
| D | Semantic AI summarization? | **NO** | no LLM in the LT path; the script only reorders nothing, drops transport syntax, and adds markers. L2 (the one LLM step) stays xlsx-only |
| E | Lens-specific evidence copies? | **NO** | one artefact per source, one index per engagement, read by everyone |
| F | Raw evidence still available? | **YES** | `inputs/` never written, moved or deleted; every artefact names its raw source; raw stays authoritative on conflict |
| G | Excel capture preserved? | **YES** | `xlsx_extract.py` unmodified; live re-extraction equals the committed artefact (test) |
| H | DOCX/PDF/VTT extracted once? | **YES** | one pass, SHA-256 cached; a second capture is a cache-hit that does not rewrite |
| I | Provenance sufficient for selective verification? | **YES** | ¶ / page / timestamp+speaker locate a passage in the raw source; identity + sha256 in every artefact |

No parallel ingestion framework, no evidence database, no vector store, no manifest, no new state key,
no new hook, no new command. One script, one test, one index file.
