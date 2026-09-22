---
name: aisa-capture
description: Process-capture pipeline for engagement inputs — the structured xlsx tier (L1 deterministic extraction + L3 replay + L2 process model) plus the capture-lite text tier (LT, deterministic .docx/.pdf/.vtt/.srt/.txt/.md/.csv extraction). Runs at the end of aisa-start, on stale hashes in aisa-round step 3.5, or manually via /capture. Produces the _capture/ shared evidence surface (entry point evidence-index.md) that lenses and council personas read.
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
| `<file>.extraction.json` | L1 (xlsx) | `library/kernel/tools/xlsx_extract.py` (deterministic) |
| `<file>.replay.md` | L3 (xlsx) | same script, `--replay` (deterministic) |
| `process-model.md` | L2 (cross-source) | this skill (LLM), template `library/kernel/capture-templates/process-model.template.md` — PM rules from the structured tier + the **process synopsis** (§4) reconstructed across every normalized source |
| `<file>.text.md` | LT (text) | `library/kernel/tools/text_extract.py` (deterministic, **no LLM**) |
| `<file>.extraction.json` | LT (text) | same script — identity + status + unit counts only |
| `evidence-index.md` | — | same script, `--index` (deterministic) — the entry point to the shared evidence surface |
| `_capture-log.md` | all | append-only audit |

`inputs/` stays pure evidence — never written to, never moved, never deleted.

## Supported formats

| Source | Tier | What it becomes |
|---|---|---|
| `.xlsx`, `.xlsm` | **structured capture** (L1 + L3 + L2) | `process-model.md` (`PM-NNN` rules with cell citations) + `*.replay.md` |
| `.docx`, `.pdf`, `.vtt`, `.srt` | **capture-lite** (LT) | `<file>.text.md` — loss-minimizing text with provenance markers (`### <heading>` + `[¶NN]`, `## [p.N]`, `[HH:MM:SS] **Speaker:**`) |
| `.txt`, `.md`, `.csv` | **capture-lite** (LT) | `<file>.text.md` — `.txt` uma linha não vazia por `[¶NN]`; `.md` cabeçalhos e tabelas intactos; `.csv` **todas** as linhas em tabela, citadas por `linha N`. Nenhum dos três amostra |
| anything else | not captured (**not a failure**) | raw reading per the format table in `library/kernel/orchestration.md` → *Evidence contract* |

**Capture-lite is extraction, never summarization.** It writes no model, no findings, no requirements, no risks, no interrogation list, no architectural inference — everything the source said, plus where it said it. There is no LLM in the LT path. The L2 process model (LLM, step 5) is the **one comprehension pass** and reads every tier's normalized output — extraction JSON, replay reports **and** `*.text.md` — so the as-is process is reconstructed across sources, not from the workbook alone. Capture does not own epistemic classification: an extraction failure is a `status`, never an `Unknown`; a synopsis marker (`OBSERVED` / `INFERRED` / `HYPOTHESIS` / `UNKNOWN`) is a marker on normalized evidence, never an engagement state.

## Execution steps

1. **Resolve the engagement root** (as in `aisa-start`): `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, else `projects/<slug>`. Read `_state.json` for the slug and capture-run counter (`capture_run`, default 0).
2. **Enumerate targets**: supported files in `inputs/` (or the single named file), split by tier — structured (`.xlsx`/`.xlsm` → steps 3–5) and text (`.docx`/`.pdf`/`.vtt` → step 5b). No supported file of either tier → output "no supported inputs; capture skipped", still run step 6 so the index exists, and stop (soft, not an error).
3. **L1 — extraction** per structured file:
   ```
   python library/kernel/tools/xlsx_extract.py "<engagement>/inputs/<file>" "<engagement>/_capture/<file>.extraction.json" --log "<engagement>/_capture/_capture-log.md"
   ```
   (On Windows prepend `PYTHONIOENCODING=utf-8` / `$env:PYTHONIOENCODING='utf-8'`.)
   The script self-caches on SHA-256 (`cache-hit` when unchanged; `--force` to override).
4. **L3 — replay** per structured file (needs the fresh extraction JSON):
   ```
   python library/kernel/tools/xlsx_extract.py --replay "<engagement>/inputs/<file>" "<engagement>/_capture/<file>.extraction.json" "<engagement>/_capture/<file>.replay.md" --log "<engagement>/_capture/_capture-log.md"
   ```
   Exit 3 = stale/failed extraction → re-run L1 once, then retry; still failing → record and continue (degradation table below).
5. **L2 — process model** (single LLM pass, only after ALL structured files did L1+L3 **and** all text files did LT — run step 5b before this step):
   a. Read every `_capture/*.extraction.json`, every `_capture/*.replay.md`, and `context.json`.
   a2. **Cross-source comprehension — source-complete in coverage, not source-total in context.** Inspect `_capture/evidence-index.md`; identify the sources and sections materially relevant to reconstructing the process; read compact process documents (`*.text.md` of a flowchart, an inputs/calculations/outputs note) **in full** where appropriate; pull **targeted** transcript passages where they suffice (a `[HH:MM:SS]` range, not the whole recording); and give **every** process-bearing source a disposition, recorded in the model header and the `_capture-log.md` L2 line:
      ```
      USED      — material to the reconstruction (read in full)
      CHECKED   — inspected; no material process semantics (or unavailable: <status>)
      TARGETED  — only the named sections/passages were required: <locators>
      ```
      No maximum source count, no KB budget, no transcript-length threshold: the contract is *enough evidence inspected to reconstruct the material process*, not *all evidence loaded*. Never mark a source `CHECKED` without inspecting it. The index is the register; no separate source-disposition file.
   a3. **Passagem de cálculo (obrigatória para cada workbook).** O replay (passo 4) já escreveu `_capture/<file>.calc-chain.json` e `_capture/<file>.calc-chain.md` — a cadeia de cálculo de cada saída rotulada, reconstruída pelo motor a partir das fórmulas (`CalcChain`, `xlsx_extract.py`): blocos `CALC-NNN` com um passo por célula e o locator de cada um, anotados **por forma** — agregação (`SUM`/`AVERAGE*`), selecção (`MIN`/`MAX`), lookup, arredondamento, factor de conversão (literal `0<k<2` multiplicativo), constante sem rótulo (`+10`, `-10`), `INDIRECT` dinâmico como `TO-READ`. Copiar o fragmento **inteiro** para §4bis do process-model, sem editar as linhas do motor. O que a L2 acrescenta, **a seguir** ao fragmento e só em linhas próprias: (i) a **unidade de agregação temporal** de cada passo `aggregation` (dia / semana / mês — lida dos rótulos e das datas do intervalo, com locator), (ii) a **regra de selecção entre alternativas** de cada passo `selection` (o que `MIN` e `MAX` escolhem entre, em palavras, sem dizer porquê), (iii) as **conversões** nomeadas pelo rótulo que a folha lhes dá (moeda, unidade, densidade — só se o rótulo existir; sem rótulo fica *factor sem rótulo*), (iv) cada **constante sem rótulo** como linha de §3 em estado `Assumed` com base no `CALC` **ou** como `TO-READ`/pergunta — nunca como significado inferido. Um workbook sem `calc-chain.json` é uma captura incompleta: `_capture-log.md` regista `L2 | <file> | calc-chain: absent (<razão>)` e o portão de Discovery lê-o. `MIN` numa saída e `MAX` noutra são **duas regras**, não uma incoerência a resolver aqui.
   b. Fill `library/kernel/capture-templates/process-model.template.md` → write `_capture/process-model.md` (overwrite whole file, like `_synthesis/`). Carry `identity.modified` into every rule's `verificado_em`; when a file predates its decay class's half-life, say so in §1 — its rows are born expired and `/status` will raise the re-question. §4 is the **process synopsis** — cross-source, every line marked `OBSERVED` / `INFERRED` / `HYPOTHESIS` / `UNKNOWN` and cited (PM id, cell/range or text locator), material lines labelled in backticks, only the reasoning dimensions material to this engagement (purpose · flow · actors · inputs · transformation stages · intermediate state · decisions · outputs and consumers · variants · exceptions · invariants · structural constraints · user tasks · genuine vs accidental complexity · unresolved semantics). For a calculation-replacement process the synopsis reconstructs the chain `input → transformation → intermediate → transformation → output → consumer` at the depth materiality + uncertainty + consequence of misunderstanding warrant — stages, never formula-by-formula. Every material output family is traced or its missing link is `UNKNOWN`; no silent disappearance. A genuine-vs-accidental distinction not directly evidenced stays `HYPOTHESIS`.
   b2. **Size budget**: read the digest fields of each extraction JSON first (identity, sheets, column classes, formula-pattern summaries). Descend into a sheet's full detail only when a rule or finding needs it. Two pilots fit comfortably; if the JSONs together exceed roughly 200 KB, summarise per sheet before writing §2 rather than truncating silently. The same discipline applies to text: a long transcript is pulled by passage (step a2), never loaded whole to satisfy coverage.
   c. Increment `capture_run` in `_state.json` (atomically: tmp → rename) and stamp it in the model header.
5b. **LT — capture-lite** per text file (`.docx`/`.pdf`/`.vtt`). Runs **before** step 5 (the L2 pass reads its output) but is independent of steps 3–4: it needs no process model and no LLM pass, and a structured-tier failure never blocks it. An engagement with text sources and no structured file still gets an L2 pass — the synopsis is reconstructed from the `*.text.md` files alone (§2/§3/§5 then state "no structured source").
   ```
   python library/kernel/tools/text_extract.py "<engagement>/inputs/<file>" "<engagement>/_capture/<file>.text.md" "<engagement>/_capture/<file>.extraction.json" --log "<engagement>/_capture/_capture-log.md"
   ```
   Same SHA-256 self-cache as L1 (`cache-hit` when unchanged; `--force` to override). Exit 0 always writes an artefact — `ok`, `empty`, `failed` or `skipped`; exit 2 is a usage error (missing file / unsupported format) and writes nothing. Never read the extraction back to "improve" it: what the script wrote is the evidence.
6. **Evidence index** (always, even when nothing was captured):
   ```
   python library/kernel/tools/text_extract.py --index "<engagement>" --log "<engagement>/_capture/_capture-log.md"
   ```
   Rebuilds `_capture/evidence-index.md` in full from `inputs/` + the extraction JSONs — one row per input file, whatever its tier or status. Deterministic and idempotent: re-running on unchanged state rewrites the same bytes. This file is the entry point the orchestrator carries into lens and persona invocations.
7. **Log** to `_capture-log.md`: one `L2` line (`generated | run N | files: ... | sources: <file> USED · <file> TARGETED (<locators>) · <file> CHECKED`), plus PM id changes (new/retired ids) when re-running. `LT` and index lines are written by the script itself.
7b. **What the new capture did to the coverage reviews — computed, never declared.** Capture changes the denominator: a new file in `inputs/`, a re-extraction, a regenerated process model or a source that failed where it used to read all move the base a recorded review claims to have read (`coverage-contract.md` §6.1, §6.3). Where `_coverage/` carries any record, ask the motor — it does not write anything:

   ```
   python library/kernel/tools/coverage.py check --engagement <slug> --stage reconciliation --json
   ```

   - `freshness: stale` → say which review, and **what changed** (the motor names the file or unit). It must be redone — by `/blueprint` step 1b, never here — before it is used again. `stale` is not a verdict on the old conclusion; it says nobody re-read the sources since they moved.
   - A source now `unverifiable` (no extractor, macro not captured, read failure) **stays in the denominator** with its reason and its impact. It never becomes `not_applicable` because support is missing, and it never becomes covered.
   - No record → nothing to say. No flag is written anywhere; `_state.json` gains no coverage boolean (`coverage-contract.md` §10).

8. **Output summary** — files captured per tier (extracted / cache-hit / empty / failed / skipped), replay finding counts by severity, top-3 highest-severity findings, PM rule + interrogation counts, synopsis line counts per marker (`OBSERVED` / `INFERRED` / `HYPOTHESIS` / `UNKNOWN`) and the source dispositions, and the text-tier unit counts (paragraphs / pages / cues). Name every failed or skipped source explicitly. One screen, no more, in business language (`CLAUDE.md` → *Duas línguas*):
   ```user-output
   Ficheiros lidos: <N> — folhas de cálculo: <n> extraídas · <n> já lidas antes · <n> vazias · <n> falharam · <n> saltadas; textos: <n> páginas · <n> parágrafos · <n> falas.
   Problemas encontrados nas fórmulas: <N> (<graves · médios · leves>) — os 3 mais graves: <…>.
   Processo reconstruído: <N> regras · <N> perguntas que os ficheiros levantaram (PM-U) · síntese com <n> frases observadas, <n> inferidas, <n> hipóteses, <n> por saber.
   Ficheiros que falharam ou foram saltados: <nenhum | <ficheiro> — <razão>>.
   Conferência do que foi pedido: <não se aplica — ainda não há nenhuma | mantém-se válida | tem de ser refeita: <o que mudou>> — material novo obriga a reler antes de voltar a servir de base.
   A seguir: uma passagem das perspectivas pelo material → `/round`.
   ```

## Hard rules (mirror kernel)

1. **Never invent.** Every PM-NNN rule cites sheet!cell/range evidence; every §4 synopsis line cites a PM id, a cell/range or a text locator (`<file> · §<heading> ¶NN`, `<file> · p.N`, `<file> · [HH:MM:SS] <speaker>`). No check = no claim: what L3 could not replay and L1 could not read is an Unknown in §7, never inferred. **Uma fórmula que o replay não computou não é ilegível — é por ler.** Entra em §7 como `TO-READ` (com o range compacto a ler), não como Unknown, e passa a linha de §3 (`PM-NNN`) ou a passo de §4bis assim que for lida (`library/kernel/states.md` → *Confirmed threshold*, «um replay falhado nunca impede a leitura»). §7 só admite `Unknown` quando a fonte é **inacessível** — VBA não descompilado, ficheiro externo ausente, folha protegida — nunca quando é legível e não foi lida. `TO-READ` é tarefa, não pergunta: não carrega as três declarações de admissão, e conta para o portão de Discovery.
2. **State ∈ {Confirmed, Assumed} only** in §3. Confirmed = formula/validation/CF evidence; Assumed = structural inference with the basis declared.
2b. **Stamp the epistemics** (kernel v0.2.0). Every PM rule carries `verificado_em` = the extraction JSON's `identity.modified` (the file's own last-edit date, NOT the capture run) and a `validade` decay class (`organizacional` default). Every PM-U row carries `criticidade`, `custo` and `swing` per `library/kernel/states.md` → *Question economics*, plus `classe` (`mecânica` | `dados` | `processo`) — a **deterministic** string read off the signal the row came from, per the template's §6 note: `protected_sheets` / sheet `state` / formats / frozen panes / comment anchors / recalculation order → `mecânica`; `columns` / `named_ranges` / `validations` / row-column counts / column classification → `dados`; a §4 synopsis line → `processo`; more than one signal takes the widest (`processo` > `dados` > `mecânica`). It is not a judgement and it does not decide the disposition — it is what makes the content test of `library/kernel/orchestration.md` → *`PM-U` about the artefact's mechanics* checkable. In pilot-3: `PM-U-026` (protection only) is `mecânica`; `PM-U-003` (hidden sheets **and** the 212-vs-465 column consequence) is `dados`. Unpriced questions inherit the compatibility default and a decisive question then enters disguised as routine — price them here, where the evidence is. **Price the `swing` by the eight technical axes** (P-26, `library/kernel/states.md` → *Admission of a question*): the phrase names ≥ 2 possible answers and which axis moves with each — `tecnologia` · `padrão arquitetural` · `componentes` · `modelo de dados` · `plano de imposição de permissões` · `esforço de alto nível` · `custo` · `risco técnico`. A `PM-U` about the **artefact's own mechanics** with no consequence on the system to be built — a protection, a hidden sheet, a format — is `cosmético` with `criticidade: Low`, however striking it looked in the file: it is a fact about the outgoing tool, not a question about the target. `classe` stays what the signal says (`mecânica` / `dados` / `processo`) and never decides the `swing`: a `mecânica` row whose consequence reaches the data model is priced by that consequence.
3. **No vendor/product names for solutions** — Discovery-facing. Naming the current tooling ("an Excel file on a shared drive") is current-state and allowed.
4. **PM ids stable across re-runs**: persisting rules keep their id; retired ids are logged in `_capture-log.md` and never reused; new rules take the next free id. Same for PM-U-NNN.
5. **Uncited or unmarked synopsis lines in §4 are template violations** — log to `_capture-log.md`.
6. **Raw files stay authoritative**: on any conflict between the model and the raw file, the raw file wins and the lens records a Conflicted SU row (see lens skills).
7. **Capture-lite interprets nothing.** The LT tier is the script's output verbatim. Do not summarize it, re-headline it, label its sections, extract requirements or risks from it, or write a `.text.md` by hand. If the script could not run, the answer is a visible `failed`/`skipped` status and the raw source — never a hand-written substitute.
8. **Extraction failure is never silent and never epistemic.** A failed source appears in `evidence-index.md` and `_capture-log.md` with its reason. Classifying it (`Unknown`, `Risky`, …) is the lens's job, not capture's.
9. **The synopsis is normalized evidence, not authority.** `OBSERVED` / `INFERRED` / `HYPOTHESIS` / `UNKNOWN` are markers, never engagement states; the Shared Understanding remains the authority for `Confirmed` / `Assumed` / `Unknown` / `Conflicted` / `Risky`. No synopsis line becomes downstream truth by existing — it is projected in Discovery, line by line, through the lens's disposition (`aisa-round`). The synopsis is never edited by a lens; it is regenerated here (stale hash or `--force`), and a sponsor answer that contradicts it enters the SU by `/answer` (degradation table: Conflicted row + re-run flag).
10. **Cross-source ≠ full preload.** Coverage is complete by disposition, not by loading: no source count, size or length target; select by materiality through the index; record `USED` / `CHECKED` / `TARGETED` per source; a `CHECKED` source was actually inspected. Repeated workbook structure is never converted automatically into a repeated business requirement — that distinction is `HYPOTHESIS` until evidenced.

## Degradation & failure modes

| Situation | Behaviour |
|---|---|
| no supported files | skip silently; lenses use the normal reading path |
| `openpyxl` not installed (script exits 2 with `requires openpyxl`) | capture **skipped, not failed**: report `capture skipped — openpyxl missing (pip install openpyxl)`, log it to `_capture-log.md`, lenses fall back to raw reading. Never an empty model: "could not run" is not the same evidence as "0 findings" |
| extraction fails (protected/corrupt) | script writes `status: failed` JSON; PM §7 records the file as Unknown; lenses fall back to raw reading |
| replay exit 3 after one L1 retry | note in `_capture-log.md`; PM §5 states "replay unavailable for <file>"; never guess findings |
| replay 0 findings | §5 says "0 findings" explicitly — absence of findings is evidence |
| model contradicts raw file (lens spot-check) | lens records **Conflicted** citing both; flag capture re-run in `_capture-log.md` |
| **LT** extraction library missing (`python-docx` / `pypdf`) | `status: skipped` + reason in the artefact, the index and `_capture-log.md`; lens falls back to raw reading. Never an empty extraction file |
| **LT** encrypted / corrupt / image-only PDF, unreadable docx | `status: failed` + reason; raw source stays available and is read directly. **No OCR in this tier** — do not add one ad hoc |
| **LT** `.vtt` with no cues, `.docx` with no paragraph or table | `status: empty`, stated explicitly — absence is evidence, the source is not silently omitted |
| **LT** unsupported format (`.pptx`, images, `.msg`) | not captured, not a failure; listed in the index as `not captured` with the raw path |
| a text source is `failed` / `skipped` / `empty` at L2 time | disposition `CHECKED — unavailable (<status>)`; §7 names it; any process semantics that would have come from it are `UNKNOWN` lines in §4 where material — never reconstructed from memory of the raw file |
| one source fails | every other source still captures; the index reports each status separately |
