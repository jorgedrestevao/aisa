---
template_id: process-model
output_path: _capture/process-model.md
sources:
  - _capture/evidence-index.md
  - _capture/*.extraction.json
  - _capture/*.replay.md
  - _capture/*.text.md
  - context.json
synthesis_prompt: |
  Reconstruct the as-is process the engagement's evidence encodes — as evidenced business
  rules, a compact cross-source process synopsis, and an interrogation list for humans.
  Work from the NORMALIZED evidence in `_capture/`: the extraction JSON(s) and replay
  report(s) for structured files, and the `*.text.md` files for documents and
  transcripts. Start from `evidence-index.md` and select by materiality: the pass must be
  source-complete in COVERAGE (every process-bearing source inspected and given a
  disposition) but never source-total in simultaneous CONTEXT (no obligation to load
  every source in full). Open the raw file only to resolve a doubt, never to invent
  beyond it. Every rule cites a cell/range; every synopsis line cites a PM id, a
  cell/range or a text locator, and carries an epistemic marker. What the evidence
  implies but cannot prove becomes a question or a HYPOTHESIS, not a claim. Stamp every
  rule with the source file's modified date (not today) and a decay class, and price
  every interrogation row with custo + swing — the kernel's epistemic contract applies to
  captured knowledge exactly as it does to knowledge a human gave you. Neutral language:
  naming the current tooling ("an Excel file on a shared drive") is current-state and
  allowed; naming solution vendors/products is forbidden (Discovery-facing document).
  Depth follows materiality + uncertainty + consequence of misunderstanding — never
  reverse-engineer every formula; reconstruct the stages that matter.
---

# Process Model — {{slug}}

> Sources: {{files + sha256 first 8 chars, comma-separated}}  |  Generated: {{ISO-8601}}  |  Capture run: {{N}}
> Source dispositions: {{per source — USED | CHECKED | TARGETED (named sections) — mirrored in `_capture-log.md`}}

## 1. File map

<Per file: one short block. Per sheet: what it appears to be (register / lookup / archive /
report / staging), its visibility (visible/hidden/veryHidden — hidden sheets are a finding),
row/column volume, and how sheets reference each other (from the dependency graph). Cite
sheet names verbatim. For text sources (`*.text.md`): one line each — what the document or
transcript is, and which sections/passages were material to process reconstruction
(disposition `USED` / `TARGETED`), or `CHECKED — no material process semantics`.>

## 2. Column classification

<One table per sheet, from the extraction JSON's column classes:>

| column | header | class (input/derived/manual) | evidence |
|---|---|---|---|
| <letter> | <header> | <class> | <dominant formula pattern, or "typed values"> |

<After each table, flag every **manual** column explicitly: **manual column = human process
step** — someone types/maintains this by hand. These anchor §4's synopsis and §6's questions.>

## 3. Business rules (PM-NNN)

| id | rule (natural language) | state | evidence | verificado_em | validade |
|---|---|---|---|---|---|
| PM-001 | <the rule as a business statement> | Confirmed \| Assumed | <sheet!range + formula / validation / conditional-format rule> | <ISO date> | <decay class> |

<state ∈ {Confirmed, Assumed} ONLY. Confirmed = a formula, data-validation rule, or
conditional-formatting rule proves it. Assumed = inferred from structure (declare the basis
in the evidence cell). NEVER a rule without a cell citation. PM rules are what the
STRUCTURED artefact proves; semantics that live in documents and transcripts enter §4 with
their text locators, not here.

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

## 4. Process synopsis (cross-source)

<The compact reconstruction of the as-is process, across EVERY source that carries process
semantics — workbook, documents, transcripts, other normalized evidence. This is the
engagement's durable process-comprehension carrier: richer than the Shared Understanding,
never authoritative over it. It is **normalized evidence**; the SU stays the epistemic
authority (`library/kernel/orchestration.md` → *Comprehension survival*).

**Reasoning dimensions** — write only the ones material to this engagement; an irrelevant
dimension gets no heading, never an empty one:

- **Purpose** — what the process exists to decide or produce.
- **End-to-end flow** — stages, handoffs, cadence, timing.
- **Actors** — by role; who decides, who executes, who maintains.
- **Inputs** — each material input: source/provider, cadence, manual vs automatic.
- **Transformation / calculation stages** — the business chain, stage by stage
  (`input → transformation/rule → intermediate stage → transformation → output → consumer /
  business decision`). Stages, not cells: cells stay in §2–§5.
- **Intermediate state** — computed values that exist between input and output.
- **Decisions** — discretionary and rule-based decisions, and who makes them.
- **Outputs and consumers** — every output family, its consumer and the business action it
  drives. An output family whose loss or change would affect scope, option viability,
  architecture shape, a user task, an estimate or acceptance is **material**: it is either
  traced to its inputs/transformations/consumer or its missing link is marked `UNKNOWN`.
  No silent disappearance.
- **Variants** — per product / port / client / channel / unit.
- **Exceptions and workarounds** — what happens when an input is missing, late or wrong.
- **Business invariants** — behaviours the business cannot lose, phrased solution-free
  ("a published price must be traceable to its inputs"); each one is a candidate SU row.
- **Structural constraints** — conditions whose truth could eliminate, reshape or gate
  whole solution classes (where the data must live; who the users are in identity terms;
  existing entitlement boundary; residency; enforcement point). Identify generically —
  Options evaluates candidate consequence, Architecture implements the response. No
  vendor, no product, no product-licensing question.
- **Material user tasks** — what the actors actually do on screen/paper today, where a task's
  shape (wide-grid entry, what-if, review, approve) could shape a future experience.
- **Genuine vs accidental complexity** — where the evidence supports it, which observed
  structure is a genuine business need and which is implementation accident. Repeated
  workbook structure is NEVER converted automatically into a repeated business requirement;
  any such distinction not directly evidenced is `HYPOTHESIS`.
- **Material unresolved semantics** — what the evidence cannot settle and matters.

**Marking** — every synopsis line starts with one marker and ends with a citation:

```text
OBSERVED   — the evidence states or shows it       → eligible for Confirmed when the evidence supports it
INFERRED   — follows from the evidence with a basis → Assumed, basis declared
HYPOTHESIS — a working reconstruction               → stays here, OR projects as the Unknown that would settle it
UNKNOWN    — the evidence cannot say                → Unknown
```

These are markers on normalized evidence, NOT engagement states. No synopsis line becomes
downstream truth by existing: projection into the SU happens in Discovery, line by line,
through an explicit disposition (`MAP` an existing row · `ADOPT` as a new row · `DISMISS`
with a reason — `aisa-round`). Material lines under *Outputs and consumers*, *Transformation
stages*, *Business invariants*, *Structural constraints*, *Material user tasks*, *Exceptions*
and *Material unresolved semantics* carry a short **label in backticks** (e.g.
`` `Outputs BIOS` ``, `` `chain: cedência → mínimo` ``) so a lens can name the line it
disposed of without a new id namespace.

Citations: `PM-NNN`, `<sheet>!<range>`, `<file> · §<heading> ¶NN`, `<file> · p.N`,
`<file> · [HH:MM:SS] <speaker>`. An uncited or unmarked line is a template violation to be
logged in `_capture-log.md`. Where two sources disagree, say so in the line (`OBSERVED …
(docx) vs OBSERVED … (workbook)`) — the lens records the Conflicted row; the synopsis never
picks a winner. Neutral language — no vendor/product names for solutions.>

## 4bis. Cadeia de cálculo (por saída)

<Só para fontes estruturadas com fórmulas. Copiar aqui, **inteiro e sem editar**, o fragmento
`_capture/<file>.calc-chain.md` que o motor escreveu no replay (`xlsx_extract.py` → `CalcChain`):
a tabela `| output | pseudo-código | locators | por confirmar |` com um bloco `CALC-NNN` por saída
rotulada, a lista **Constantes sem racional** e a tabela **Por ler (`TO-READ`)**. Um `CALC-NNN` é
um id estável: `_capture/process-model.md#CALC-003` resolve e o inventário de cobertura conta um
bloco por linha (`coverage-contract.md` §6.2).

O fragmento **abre** com a tabela *Fronteira de capacidade* (mecanismo · presente · detalhe · consequência) e com a
*Cobertura declarada* (`n de m blocos traçados até input terminal · k TO-READ · candidatos = renderizados +
agrupados + absorvidos + TO-READ`). `presente: não` significa «a parte não existe no pacote», nunca «o cálculo
não existe noutro sítio»; `presente: sim` em `power_query`, `data_model`, `vba`, `rtd` diz onde a cadeia **não**
chega — e essa incapacidade declarada vale mais do que uma cadeia parcial plausível. Um `CALC` marcado `invalid`
tem um ramo que não acaba em nenhuma das cinco classes (valor tipado · feed externo · intervalo nomeado sem
fórmula · `TO-READ` · fronteira): não conta para a cobertura nem para o inventário.

A seguir ao fragmento, em linhas próprias marcadas `L2:`, o que só a leitura acrescenta — e nada
mais: a unidade de agregação temporal de cada passo `aggregation` (dia / semana / mês, com o
locator dos rótulos ou datas que a mostram); o que cada passo `selection` escolhe entre (em
palavras, sem porquê); o rótulo que a folha dá a cada factor de conversão (moeda, unidade,
densidade — sem rótulo fica *factor sem rótulo*); e, para cada constante sem racional, a linha de
§3 (`Assumed`, base = o `CALC`) ou o `TO-READ` que a substitui. Nunca o significado de negócio de
um `+10`: isso pergunta-se ao dono. `MIN` numa saída e `MAX` noutra são duas regras, não uma
incoerência. Workbook sem `calc-chain.json` → esta secção diz `calc-chain: absent (<razão>)` e
`_capture-log.md` regista o mesmo.>

## 5. Anomalies & silent failures

<Replay findings promoted, most severe first. One row per finding kept relevant:>

| severity | finding | location | consequence for the process |
|---|---|---|---|
| high | <from replay report> | <sheet!cell> | <what silently breaks> |

<If the replay report has 0 findings, state that explicitly — absence of findings is evidence.>

## 6. Interrogation list (PM-U-NNN)

<What the evidence implies but cannot prove. Each row is a candidate SU Unknown for the
lenses — in Discovery every row receives exactly one disposition (`MAP` / `ADOPT` /
`DISMISS — reason`); a **Critical** row may remain Unknown after adoption but may never
disappear silently. Incoherence inside the reconstruction is itself a source of questions;
name these shapes when they occur: an output without an identified consumer · a material
calculation without an owner · an approval that does not gate publication/load · two
equivalent outputs with different chains · a document claim the workbook contradicts · a
material HYPOTHESIS in §4 (the question that would settle it).>

| id | question | why it matters | suggested respondent (role) | criticidade | custo | swing | classe |
|---|---|---|---|---|---|---|---|
| PM-U-001 | <question> | <decision/risk it unblocks> | `role: <role>` \| `fonte: <artefacto/sistema>` — never a name (`library/kernel/states.md` → *The form of `quem responde`*) | Low \| Med \| Critical | email \| documento \| reuniao \| spike | <classe: frase> | mecânica \| dados \| processo |

<`custo` and `swing` follow `library/kernel/states.md` → *Question economics*, so a lens can
promote the row to an SU Unknown without inventing them. `custo` = what it takes to get the
answer. `swing` = `decisivo` (changes which option survives) \| `dimensionante` (changes
sizing/effort/design) \| `cosmético` (changes nothing material), plus a phrase stating WHAT
changes. Derive both from the "why it matters" column — never leave them blank: an unpriced
question inherits the compatibility default (`email` / `dimensionante`) and a decisive
question then enters the engagement disguised as routine.

`classe` is read off **the signal that generated the row** — the field or line named in
its own *why it matters* — never off what the row happens to mention and never off the
answer it expects. It is not a verdict and it never decides the disposition.

| signal that generated the row | `classe` |
|---|---|
| `protected_sheets`, sheet `state`, cell formats, frozen panes, comment anchors, recalculation order, a corruption or repair of the artefact itself | `mecânica` |
| `columns`, `named_ranges`, `validations`, row/column counts, the column classification, the existence or reach of a dataset | `dados` |
| a §4 synopsis line, a formula that carries a transformation rule, a replay finding about the chain, or anything with no artefact signal at all (policy, scope, ownership, cadence) | `processo` |

Two cautions, both learned by running this template:

- **A §4 line that merely cross-references the row is not its signal.** The synopsis
  registers open questions by id; that citation does not make the row `processo`. Ask
  what the row was *born of*, not where its id appears.
- **Only the first two rows of the table are mechanical.** When the signal is a named
  extractor field, the class follows with no judgement. When the row was born of the
  synopsis, the transcript or the interview, the class is a **judgement with a declared
  default**: `processo` unless the row is plainly about how the old artefact is built.
  Write the class anyway — a declared default that a lens can contest beats a blank —
  but do not report it as deterministic.

A row fed by more than one signal takes the widest class (`processo` > `dados` >
`mecânica`). The class is what makes the content test of
`library/kernel/orchestration.md` → *`PM-U` about the artefact's mechanics* checkable: a
`mecânica` row gets `ADOPT` only when the lens declares which form, volume or rule of the
to-be's data changes with the answer.>

## 7. Not captured

<Explicit list of everything outside mechanical reach: VBA modules, external links,
password-protected sheets, not-replayable formulas (copy the replay report's list),
hidden/veryHidden sheets not parsed, text sources whose extraction is `failed` / `skipped` /
`empty` (named, with the status). Each entry = an Unknown (fonte **inacessível**: VBA não descompilado, ficheiro externo ausente, folha protegida) **or a `TO-READ`** (fonte legível, ainda não lida: fórmulas que o replay não computou, listadas por range compacto — `<folha>!<coluna ou intervalo>`, nunca por célula), never inferred. `TO-READ` não fecha por decurso do tempo: fecha quando a leitura vira linha de §3 ou passo de §4bis, e conta para o portão de Discovery (`phases.md` → *Exit criteria*).>
