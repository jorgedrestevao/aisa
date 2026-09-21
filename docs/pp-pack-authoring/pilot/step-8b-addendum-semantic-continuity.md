# Step 8B Addendum — Deep Comprehension, Structural Constraints & Semantic Continuity — pricing-marinha

> Model / contract adjudication. Not a pilot, not pack authoring, not a runtime repair. It asks one
> question of the frozen runtime: what is the **minimum** contract that lets Claude reason naturally and
> deeply over messy business evidence, and then deterministically preserves what must survive —
> compression, phase transitions, evidence changes and session resets.

**Verdict: `STEP 8B ADDENDUM — SEMANTIC CONTINUITY: PASS`** — the adjudication completed on evidence; the
runtime was not modified; `projects/pricing-marinha/**` was not modified; Steps 3–7 were not reopened; no
web research; no new framework layer proposed. Full output block at the end.

---

## 1. Basis

| | |
|---|---|
| Baseline | commit `78391d7ea00cc59c45b23ec65b384de8c812ab39`, branch `pp-pack-authoring/step-2-discovery-layer`, pack `pp` 1.8.1 |
| Runtime modified | **NO** — `git status` shows only untracked docs (`docs/pp-pack-authoring/pilot/`, `docs/FRAMEWORK-NEGOCIO.md`, two stray Obsidian files) |
| `projects/pricing-marinha/**` modified | **NO** — read only |
| Steps 3–7 reopened | **NO** |
| Web research | **NO** |
| Prior adjudication relied on | `step-8b-post-pilot-adjudication-report.md` (PR-1 PROVEN-GENERIC, PR-2 → PR-2A DOCUMENTATION, PR-3 PRACTICE; loss counts 3 / 1 / 2) — taken as established, not re-derived |

Sources read in full for this addendum: `step-8-real-engagement-pilot-report.md` §18–24 + final block;
`step-8-pilot-observation-log.md` P-OBS-014, P-OBS-027..029 and the post-8B block;
`step-8b-post-pilot-adjudication-report.md` (all sections); engagement — `_state.json`, `context.json`,
`shared-understanding.md`, `frame.md`, `options.md`, `decisions.md`, `answers.md`, `premortem.md`, `story.md`,
`lens-outputs/*.md`, `lens-outputs/_council-prep/O-01-solution-architect.md`, `_resolucoes-fechadas-O01.md`,
`_capture/process-model.md`, `_capture/evidence-index.md`, `_capture/_capture-log.md`, both `.docx.text.md`
files in full, the kick-off `.vtt.text.md` at the passages cited below, `_blueprint/ux-blueprint_v01.yaml`,
`_blueprint/ux-blueprint_v05.yaml`, `_blueprint/blueprint-log.md`, `_synthesis/as-is.md`,
`_synthesis/architecture-story.md`, `_synthesis/risks-and-assumptions.md`,
`_render/*_implementation-spec_v02.md` §1–6, §13–16, `_render/*_estimate_v02.md` (grep); runtime —
`library/kernel/{orchestration,states,phases,glossary,blueprint-contract,render-contract}.md`,
`library/kernel/capture-templates/process-model.template.md`, `docs/PROCESS_CAPTURE_SPEC.md`,
`docs/PHILOSOPHY.md`, `.claude/skills/{aisa-capture,aisa-round,aisa-frame,aisa-options,aisa-decide,
aisa-synthesize,aisa-render,aisa-blueprint,aisa-answer,aisa-status,aisa-simulate,aisa-revisit,
chairman-synthesis,lens-operations,lens-data}/SKILL.md`, `.claude/commands/resume.md`,
`.claude/agents/{chairman,solution-architect,operations-lead}.md`, `.claude/hooks/HOOKS.md`,
`library/packs/pp/pack.yaml`, `decision-tree.md` §3, §5, §11, `decision-model/blocking-set.md` §0–1,
`architecture-templates/README.md`, `domain-knowledge/craft/{excel-translation,screen-consolidation-rules}.md`
(heads).

---

## 2. Pilot-1 observed quality gap

Step 8B counted six material losses. This addendum asks what *kind* of failure each one is. They do not
collapse into one defect.

| Loss | Where it was in the evidence | Where it stopped | Failure kind |
|---|---|---|---|
| **Simulador as what-if task** (PM-003 facet) | `process-model.md` §1 "what-if clone of `Outputs`… editable simulation copy"; docx ¶117–120 lists `Simulador` among the *output* sheets; kick-off `[00:40:22–00:40:50]` ("o simulador é para os Campos mexerem"), `[01:07:51–01:08:28]` ("Este é um simulador dos preços… simula… como é que afeta a margem"); Pedro `[00:57:44–00:58:23]`: "a minha intervenção… é fazer aqui uma projeção, uma estimativa… jogar também em paralelo com a margem" | SU carried only the duplication facet (C-041). No row names the Simulador's business role. `R-012` records only KAM simulation | **premature compression** — a rich normalized fact reached the SU as one facet of a defect row |
| **Calculation chain** (PM-007 + docx §2) | docx ¶61–111: `Preço Cedência = Platts + Prémio + SLI` → `Preço Base = Cedência + Logística` → `Preço Venda = Base + Margem` → `Preço Mínimo = Venda − Descontos`, "até/após" rule, blend formula; kick-off `[00:42:37–00:44:25]`: reference price = "o maior dos 2" weeks, "regra que empola a 3"; PM-007 model-style base sheets | **No** SU row, no frame clause, no options.md line, no lens-output sentence carries the chain. Only C-041 cites docx ¶79–90 (unit conversions). Grep confirms: `Cedência`/`SLI`/`maior das`/`semana seguinte` appear in no reasoning artefact | **insufficient comprehension + missing projection obligation** — the L2 model is `.xlsx`-only by contract (§6 below), so the chain that lives in the `.docx` was never reconstructed anywhere; lenses read it and projected atoms |
| **`Outputs BIOS` output family** (PM-008) | PM-008 (Assumed); docx ¶101–111 (blend calc), ¶137–143 (Outputs BIOS as a deliverable); kick-off `[00:40:49–00:42:02]` (FAME/HVO blends, "geram esta tabela semelhante") | SU mentions `Outputs BIOS` only as a sheet name inside A-007/R-008 (the `DF_GRID_1` reference). No scope row | **premature compression** — a whole output family compressed away because no artefact asks "what are the outputs and who consumes each?" |
| **PM-U-002 Mon/Tue input sparsity** (Critical) | `process-model.md` §6, priced `spike / decisivo` | Never promoted, never dismissed | **missing projection obligation** — PM-U adopt/dismiss step exists in spec + template, not in any lens skill (PR-2A, established) |
| **Estimation as capability requirement** | C-008, C-039, C-046 (rule), C-032/C-055 (incidents), frame sentence ("low-information Monday/Tuesday pricing") | Options treated it as exposure (A-008) — options.md never states estimation as a behaviour any option must support | **reasoning-depth failure at SU→Options + missing carrier** — `frame.md` has no slot for "behaviours that must survive"; `options.md` has no slot for "obligations every option must meet" |
| **Audit / server-side authorization after C-057** | Options concern coverage: "qualquer opção tem de desenhar um trilho de auditoria real"; "ponto de aplicação real, do lado do servidor"; v01 rationale "auditoria herdada do store" | C-057 flipped `record_authority` (P-OBS-014, correct) and opened A-009 for the surface only; audit/security basis and O-004 strengths never re-derived; v03 closed A-009 on connectivity | **stale downstream reasoning after new evidence** (+ PR-1 enforcement gap) |

Not observed: a session/context continuity failure. Pilot 1 ran as one continuous session. §19 tests
continuity statically.

**Interpretation.** Two losses are premature compression, two are missing projection obligations (one
already PR-2A), one is a missing carrier at the SU→Options boundary, one is stale reasoning after a premise
change. Extraction (L1/L3) was sufficient for the workbook; comprehension was not sufficient for the
*process*, because the process is described across four sources and the only reconstruction artefact is
scoped to one of them.

---

## 3. Governing doctrine

Evaluated and **adopted** as the governing principle for this addendum:

> AISA must not replace Claude's natural intelligence with determinism. Determinism exists to ensure that
> natural intelligence produces durable, epistemically honest state that survives compression, phase
> transitions, evidence changes and session resets.

```text
natural deep reasoning → bounded epistemic formalisation → durable semantic memory
→ selective rehydration → continued deep reasoning
```

Consistency check against the frozen doctrine: `docs/PHILOSOPHY.md` already refuses "motor determinístico"
and positions AISA as "sintetizador contextual + detector de inconsistências"; `orchestration.md` already
forbids the orchestrator from deciding what evidence means. The addendum doctrine is a sharpening, not a
reversal: it says *what* determinism is for (durability, honesty, survival) and *what it must not touch*
(cognition). Every repair below is tested against it (§25).

---

## 4. Extraction vs comprehension

| Layer | Pilot-1 evidence | Verdict |
|---|---|---|
| **L1 extraction** (`xlsx_extract.py`) | 17 sheets, 728 columns, 291 named ranges, formula patterns, exceptions, flags. One misdetection (`Inputs` header row), correctly flagged and worked around by the L2 model | **sufficient** |
| **L3 replay** | 173 findings; the 95 overrides that anchor C-041/R-007; `DF_GRID_1` orphan; `#VALUE!` in Riviera | **sufficient** |
| **LT capture-lite** | 2 `.docx` + 2 `.vtt` normalized with locators; no LLM | **sufficient as extraction** |
| **L2 process model** | 14 PM rules, 11 PM-U, a 5-paragraph §4 narrative — all from the workbook only. §4 describes *sheet mechanics* (register → lookup chain → six copies) and closes with a good interpretive hypothesis ("absorbed successive ad-hoc extensions"). It does not state what is computed in business terms (Cedência → Base → Venda → Mínimo), who consumes each output, or the Mon/Tue behaviour | **insufficient as comprehension** — by contract, not by execution |

Where the comprehension gap is anchored in the runtime:

- `aisa-capture` → *Supported formats*: "the L2 process model (LLM) stays scoped to `.xlsx`/`.xlsm`".
- `process-model.template.md` → `synthesis_prompt`: "Work ONLY from the extraction JSON(s) and replay
  report(s)".
- `orchestration.md` → *Capture tiers*: "The L2 process model (LLM) stays scoped to `.xlsx`/`.xlsm`."

So the one artefact whose job is "reconstruct the as-is process logic" is forbidden from reading the two
documents that explain the as-is process logic. The lenses are the only place where the four sources meet —
and a lens writes atomic rows plus a 2–4 sentence narrative. **No artefact holds a coherent cross-source
process reconstruction.** That is the structural root of the three Capture→SU losses, independent of how
well any lens reasoned.

One illustration of inference embedded in a Confirmed PM row: PM-001 reads "Daily counterparty quotes
(margin, barge/CT transport, premium) are entered by hand". *Typed values* is observed; *daily* is
inferred from the date column; *counterparty quotes* is a label inference from named-range names. The docx
(¶4–24) says Platts quotes arrive automatically and only logistics costs and target margins are manual. The
two accounts were never reconciled into one model. Not a defect in the PM row's citation discipline — a
symptom of no artefact being responsible for the reconciliation.

**Extraction depth: PARTIAL** (L1/L3/LT sufficient; L2 source scope too narrow). **Comprehension depth: NO.**

---

## 5. Exploration vs formalisation

Does the runtime formalise too early? Two mechanisms were inspected.

**Discovery lenses (inline).** `lens-*` step 2 says "Reconstruct one real instance end to end… Then hunt what
the diagram omits" (operations), "trace lifecycle and lineage" (data) — exploratory instructions exist. But
the only persisted outputs are SU rows (state assigned at write time) and a short narrative. The exploration
happens; what is persisted is the compressed result. The `## What matters` block in each `lens-outputs/*.md`
is where the pilot's coherent thinking is visible (operations: "existe uma regra de negócio informal… que
não vive em nenhuma célula") — 2–4 sentences, by contract.

**Council personas / chairman.** `chairman-synthesis` Step 2 ("Build the synthesis map — do not write yet")
and Step 2b (dialectic) are explicitly exploratory before Step 3 assigns states. The persona return schema
(`Headline / Evidence anchors / Proposal / …`) is a proposal, not a row. Formalisation is deferred correctly
inside a round. What is missing is the same: the coherent reconstruction is not one of the return
sections, so it cannot be persisted.

**Verdict.** Early formalisation *of what is persisted* is not the defect; the epistemic discipline is
correct and must stay. The defect is that **the only persistable unit is the atom**. A reconstruction
(inputs → transformations → outputs → consumers, with exceptions and hypotheses) has no carrier, so it
either dies in the lens's context or is force-fitted into rows. The doctrine "explore / reconstruct →
challenge → formalise material conclusions" is **warranted as doctrine**, and its implementation is a
carrier (§12), not a procedure.

**Contribution to the shallow process representation: YES, via the missing carrier.** Not via the state
model.

---

## 6. Process reconstruction

Benchmark applied: a capable analyst given the workbook, the two docx files and the two transcripts, told
"identify inputs, calculations and outputs and understand how the process works". Against that benchmark,
what the persisted state carries today:

| Dimension | Persisted today (best locator) | Gap |
|---|---|---|
| Actors | C-002, C-005, C-013 (3 populations), C-026 | none material |
| Inputs | C-016 (2 manual re-entries), PM-001 (85 manual cols), C-006 (Monday load) | source/provider/cadence per input scattered; docx ¶1–59 input taxonomy (Platts, FX, logistics, margins, premiums/discounts, densities, Supply cedência) not projected |
| Transformations | C-041 (duplication), PM-002/005/007 (lookup mechanics) | **the business chain itself is absent** (docx ¶61–111) |
| Intermediate state | — | `Base DFA/RF` as intermediate computation never named as such |
| Decisions | C-002 (committee), C-008/C-039/C-046 (Mon/Tue rule), C-025 (12 €/t floor) | good |
| Outputs | C-001 (minimum price to KAM), C-009 (folha de rosto) | `Outputs BIOS`, the four unit variants as a deliberate output family, `Simulador` as a task — absent |
| Consumers | KAM (C-013/C-015), X-ALT/X-Author load (C-001/C-064), publications for Sines/Lisboa (kick-off `[00:42:56–00:43:08]`) | publications consumer never recorded; Simulador consumer unknown, never asked |
| State transitions | C-026/C-043 approval before load | good |
| Variants | ports, fuels, counterparties (PM-001/005) | blends (BIOS) absent |
| Exceptions | C-008 (missing quotes), C-011 (hedging), C-032 (compensation) | good |
| Workarounds | C-021 (protection removal), PM-013 (typed conversions) | good |
| Dependencies | C-003 (SAP), C-057 (shared SQL — late), Market View/Ulysses (PM-010/011) | Market View consumption unknown (PM-U-006, never promoted) |
| Timing | C-006, C-007 (Friday reference approval), X-003 (weekly vs daily unreconciled) | good |
| Failure points | R-001, R-007, R-008, C-019 | good |

The persisted state is strong on actors, decisions, exceptions, timing and failure points — the lenses'
native perspectives — and weak exactly where the *process as computation* lives: transformations,
intermediate state, output families, consumers. These are the dimensions that shape a calculation-replacement
architecture. **Reasoning dimensions, not template sections**: the table above is a diagnostic, not a
proposed schema.

---

## 7. Calculation / output lineage

**Output-first lineage test**, applied to the material outputs the evidence names:

| Output | ← calculation | ← input | ← source/actor | Consumer / business action | Traceable from persisted state? |
|---|---|---|---|---|---|
| Daily minimum price per port × product (`Outputs`) | Mínimo = Venda − Descontos; Venda = Base + Margem; Base = Cedência + Logística; Cedência = Platts + Prémio + SLI (docx ¶62–96) | Platts/FX (feed), logistics (manual, monthly), margins (manual, committee), Supply cedência (email) | Market View; Pedro/Cláudia; Supply team | KAM negotiation floor (C-001/C-015); load to X-Author (C-001/C-064) | **NO** — chain absent; endpoints present |
| "Até / após" reference price | max of the two weekly prices, +3 uplift rule (kick-off `[00:42:37–00:44:25]`; docx ¶91–100) | same | same | publications (Sines/Lisboa), indicative quotes to clients | **NO** — never recorded |
| Unit variants (`usd_ton`, `eur_ton`, `usd_m3`, `eur_m3`) | conversions via FX and densities (docx ¶79–90) | densities (DFA/RF/BIOS blocks) | — | system load in four units (docx ¶151–157) | **PARTIAL** — recorded as duplication defect (C-041), not as output requirement |
| `Outputs BIOS` | blend formula (docx ¶106–110) over base output (PM-008) | blend %, FAME/HVO prices from Supply | — | biofuel customers | **NO** |
| `Simulador` | same as `Outputs`, editable | same | pricing analyst (Pedro's "projeção… jogar em paralelo com a margem") | Mon/Tue projection; margin what-if | **NO** |
| `Checklist` sign-off | — | — | Pedro | audit evidence (C-024/R-005) | YES |

Four of six material outputs fail the lineage test from persisted state. The evidence to pass it was
normalized and available. **A formula inventory (PM-002/005/007) is not comprehension**: the pilot had the
inventory and lacked the chain. The runtime does distinguish literal inputs / derived values (L1 column
classes) and overrides (L3); it does not distinguish *business-significant* calculations from *technical
helper* calculations, because nothing asks the question.

---

## 8. Business vs implementation complexity

The frozen adjudication already separated calculation complexity from interaction complexity (8B §11). This
addendum adds the third axis: **genuine business complexity vs accidental implementation complexity**.

| Observed structure | Genuine? | Accidental? | Recorded as |
|---|---|---|---|
| Six 104-column output copies | four unit outputs *are* required by consumers (docx ¶151–157) | five independent recomputations instead of one model + toggle (PM-003, PM-U-009) | C-041/R-007 — accidental only; the genuine "four units required" facet not recorded |
| `INDIRECT`-built per-port lookups (PM-005) | port-specific cost rules are genuine | string-built lookup is accidental | not classified |
| `Base DFA/RF` model-style sheets (PM-007) | blend/product-specific chains plausibly genuine | one-formula-per-row plausibly accidental | not recorded at all |
| Typed-over conversions (PM-013) | — | accidental (defect) | C-019/C-041 |
| Weekly Friday reference approval vs daily committee (X-003) | genuine, unresolved | — | X-003 open |
| "Sempre pior" heuristic (C-008) | genuine business rule (tribal) | — | C-039/C-046 |

The `process-model.md` §4 closing paragraph already makes the right hypothesis ("consistent with a workbook
that has absorbed successive ad-hoc extensions… rather than being redesigned"). It is unmarked prose. Marked
as **HYPOTHESIS** and carried per output family, it becomes the distinction §9 asks for. **Faithfully
reproducing the workbook ≠ reproducing the business need** — the pilot's blueprint consolidated the six
copies (correct) but also dropped BIOS and the Simulador (incorrect), because the accidental/genuine line was
never drawn per family. **This distinction should become a comprehension obligation carried by the synopsis
(§12), classified as hypothesis until verified.**

---

## 9. Business invariants

Candidate invariants observable in Pilot-1 evidence, and how the runtime carried them:

| Invariant (business truth independent of technology) | Evidence | Carried? |
|---|---|---|
| Committee/superior approval precedes publication or load | C-022, C-026, C-043 | YES — `AprovacaoCarregamento` entity, SoD in v01 |
| Nothing may be loaded below the minimum price | C-023 (Spain enforces by system; Portugal by checklist) | PARTIAL — recorded as control asymmetry; never stated as a to-be invariant |
| Mon/Tue pricing must remain possible with incomplete quotes, with the agreed conservative behaviour | C-008, C-039, C-046, sponsor ask #2 | **NO** — became exposure (A-008), not behaviour |
| A published price must be traceable to its inputs (audit) | C-024, R-004, R-005, D-002 condition | PARTIAL — stated as design condition; mechanism lost after C-057 |
| Port-specific cost rules apply to the correct port | PM-005, C-016 | PARTIAL — `CustosLogisticos` "por porto" |
| The output format the KAM receive stays stable | C-009, C-033, R-002 | YES (R-002) |
| SAP is the truth for term-contract client terms | C-052 | YES |

Minimum-complexity representation, options adjudicated:

| Option | Assessment |
|---|---|
| A — new first-class label / state | **Rejected.** Violates "no state×tag combinatorics" (CLAUDE.md principle 3). Invariants are Confirmed or Assumed facts about the business; they need no new epistemic status |
| **B — existing semantics + stronger guidance** | **Adopted.** An invariant is a `Confirmed`/`Assumed` row whose claim is phrased as a behaviour that must remain true regardless of solution. The synopsis (§12) lists them; Framing projects them (§14/§27). No new column |
| C — Framing survival obligation only | **Adopted as the projection**, not as the owner. Without an owner row, the frame block would become a second truth |
| D — not needed | Rejected: one material invariant was lost (estimation) and one was designed away without a row (BIOS) |

**BUSINESS INVARIANT TREATMENT: EXISTING-SEMANTICS**, with the frame block as its projection. One owner
(SU row), one durable list (synopsis §4 "invariants"), one projection (frame.md) — see §60 one-source table.

---

## 10. Evidence-derived questioning

Principle tested: *internal model incoherence is itself a source of questions.* The runtime already has
this mechanism — the PM-U interrogation list ("what the file implies but cannot prove"). In Pilot 1 it
generated PM-U-006 ("Are Market View and UlyssesQuotes actually read by anyone?") — an incoherence-derived
question. What it did **not** generate:

- "The `Simulador` exists; what business decision consumes it?" (PM-U-009 asked *why six copies*, not *what
  the editable copy is for*).
- "`Outputs BIOS` is a report; who receives it and how often?"
- "`Base DFA/RF` dates stopped advancing 35–39 days ago (PM-U-007, Low) — yet the docx says these sheets
  'aplicam toda a lógica de pricing'; which is true?" — a cross-source incoherence the xlsx-only L2 cannot
  see.

The gap is scope, not mechanism. Widening the L2 model's sources (§12) lets the existing PM-U list ask
cross-source incoherence questions. The L2 prompt should name the incoherence shapes explicitly (output
without consumer; critical calculation without owner; approval that does not gate publication; two
equivalent outputs with different chains; a document claim the workbook contradicts). **No new question
engine.** The bank stays the single consumer of `aisa-status` step 6; PM-U rows stay candidate Unknowns for
the lenses (PR-2A wiring makes their disposition mandatory).

---

## 11. Teach-back

**Survival test** (pre-Options): "Explain the current business process back without mentioning any future
solution." Applied to the persisted state alone (SU + frame + PM), the best available answer is:

> Daily, Pedro/Cláudia enter logistics costs and target margins into a protected Excel with 291 named
> ranges; Platts and FX arrive automatically; a daily committee decides margins and Mon/Tue projections using
> a worst-case rule; the output (minimum price per port and product) is reviewed by Pedro against a checklist,
> archived, e-mailed to ~200 KAM as a floor and loaded manually into X-Author after a superior's approval;
> term contracts are priced by SAP; the calculation logic is duplicated across six sheets that have diverged.

That is a sound *organisational* account and would pass a shallow test. It fails the deep test: it cannot say
what is computed (Cedência → Base → Venda → Mínimo), why there are four unit outputs, what the "até/após"
reference price is, that a biofuel-blend output family exists, or what the analyst actually does in the
Simulador each Monday. Those are the facts that shaped the architecture question. **FRESH-SESSION PROCESS
TEACH-BACK: FAIL.**

The failing example the brief gives — "The current process is a complex Excel with duplicated sheets and
manual work" — is close to the frame sentence's process clause. The frame is *correct as a problem statement*
and *insufficient as process meaning*; both roles were loaded onto one sentence.

**Test warranted: YES**, as a soft gate at `/frame` (Discovery exit) and re-checked at `/options` entry:
the check is "does the persisted state let a reader trace each material output to inputs, transformations,
decisions and consumers, or name the gap as an Unknown?" — no score, no word count, no writing-quality
judgement. Failure behaviour in §63.

### Human validation placement

| Mode | Assessment |
|---|---|
| Always | Rejected — ceremony for engagements with a two-page process |
| **Materiality-triggered** | **Adopted.** Trigger: the synopsis carries at least one HYPOTHESIS or UNKNOWN on a *material* output family, transformation or consumer. Then the synopsis itself becomes **one** `reuniao` agenda item in `/status` ("This is how we understand the process to work; what is materially wrong or missing?"), replacing N atomic questions. Pricing-marinha would have triggered (Simulador consumer unknown; BIOS Assumed; Market View consumption unknown) |
| Optional practice | Insufficient — Pilot 1 shows the question does not get asked unprompted |
| Not needed | Rejected |

Question burden goes **down**, not up: one structured teach-back replaces several PM-U items and is the
cheapest way to convert HYPOTHESIS into Confirmed/Unknown. It rides the existing agenda mechanism; no new
ceremony, no new artefact.

---

## 12. Durable process memory

Question: should `_capture/process-model.md` become the durable semantic process memory, at two altitudes,
rather than a new `process-understanding.md`?

**Can the existing artefact carry it?** YES, with two bounded changes:

1. **Source scope.** L2 reads *all* normalized evidence (`*.extraction.json`, `*.replay.md`, **and**
   `*.text.md`) plus `context.json`. LT stays extraction-only (its rule "interprets nothing" is untouched);
   L2 is already the LLM pass and already exists. PM rows keep cell citations for workbook facts; a
   synopsis sentence anchored in a document cites `<file> · §<heading> ¶NN` or `[HH:MM:SS] <speaker>` —
   locator formats that already exist in `orchestration.md`.
2. **Two altitudes in one file.** §4 becomes the **compact synopsis** (purpose · end-to-end flow · actors ·
   inputs · transformation stages · key decisions · outputs and consumers · variants and exceptions ·
   invariants · material unresolved semantics), each line marked **OBSERVED / INFERRED / HYPOTHESIS /
   UNKNOWN** and cited. §1–3, §5–7 remain the **detailed normalized evidence** exactly as today. No page
   limit; "as compact as possible without material loss".

Why not a new artefact: it would be a second process truth beside `process-model.md`, with its own update
ownership and its own drift; and §4 of the existing template already promises "the workflow this artefact
implies — stages, handoffs, cadence, actors" — the intent is there, the scope is not.

**Epistemic marking maps onto existing states at projection**: OBSERVED → Confirmed (cited); INFERRED →
Assumed (basis declared); HYPOTHESIS → never a row on its own — it projects as an Unknown (the question that
would settle it) or stays in the synopsis; UNKNOWN → Unknown. **No new state.** The marking is how the
synopsis stays aggressive in understanding and conservative in claiming (§4 of the brief).

**Update ownership (§59).** The synopsis is regenerated by `aisa-capture` on a stale hash (existing) or
`/capture --force` (existing). Sponsor answers about the as-is enter the SU by `/answer` with `was <id>`
(existing). Where an answer contradicts a PM row or synopsis line, the existing degradation path applies —
Conflicted row citing both + capture re-run flag in `_capture-log.md`. Rule already present in
`aisa-capture` hard rule 6 and the degradation table. **No manual synchronisation.** A fresh session reads
synopsis + SU; SU wins on conflict (§17).

**Not a new authority (§17).** `process-model.md` stays normalized evidence — citable, richer than the SU,
never authoritative over it. Every downstream claim still needs an SU/evidence basis. The disposition step
(PR-2A, widened) is what turns synopsis lines into SU rows; the synopsis is not edited by lenses.

**Rich comprehension, compact SU (§18).** The projection is *selective*: only material lines become rows
(the disposition may be "map" to an existing id or "dismiss — not material, reason"). The SU does not grow
by the synopsis's size; it grows by what changes an option's viability, scope or shape.

---

## 13. Material compression survival

**Compression is allowed.** The rule is not "preserve everything everywhere" but "know what is compressed
and preserve what remains decision-relevant". The operational question at each boundary: *what material
meaning could be lost if this representation replaces the richer one for downstream reasoning?*

Semantic classes that must not be **silently** lost (a downstream artefact may omit detail, never the
obligation):

| Class | Pilot-1 instance | Owner | Durable carrier | Projection consumers |
|---|---|---|---|---|
| business invariant | Mon/Tue behaviour; approval before load | SU row | synopsis §4 list | frame block → options personas → blueprint |
| structural constraint | shared SQL data authority (C-057, late); internal audience (C-056); no separate budget (C-028) | SU row | frame block | options (blocking set S3) → architecture |
| decision-changing Unknown | U-028; PM-U-002 | SU `Unknown` with `swing: decisivo` | frame block / `/status` agenda | options, simulate |
| material scope / output family | `Outputs BIOS`; four unit outputs | SU row (from synopsis) | synopsis "outputs and consumers" | frame → options → blueprint entities/screens |
| material user task | daily ~85-value entry; Mon/Tue what-if in `Simulador` | SU row | synopsis "actors × decisions" | blueprint step 4 (task model) |
| material transformation obligation | the calculation chain; `Base DFA/RF` | SU row | synopsis "transformation stages" | options (calc-layer concern) → spec → estimate Fase 0 |
| material exception | missing quotes; file breaks mid-cycle | SU row | synopsis "exceptions" | premortem, spec acceptance scenarios |
| material control obligation | audit trail; server-side authorization | SU row / options concern | decisions.md conditions | blueprint (structural choice when the store moves) |

This is a **documentation-level list** (6–8 lines in `orchestration.md`), not a matrix. It names what a
boundary check looks for; it does not require any artefact to repeat any item. **NEW COMPRESSION MATRIX
WARRANTED: NO.**

### Semantic survival checkpoints (§21 of the brief)

| Boundary | Intentionally compressed | Must survive | Current mechanism | Pilot-1 failure | Smallest guard |
|---|---|---|---|---|---|
| Capture → SU | cell-level detail, every formula, every sheet | material output families, transformation obligations, tasks, invariants, PM-U Critical | lens reads PM + text.md; writes rows; PM-U "candidate Unknowns" (spec only) | 3 losses + PM-U-002 | synopsis altitude in `process-model.md` + explicit disposition (adopt / map / dismiss) of PM-U rows and synopsis material lines in each lens's `Open evidence` block (PR-2A widened) |
| SU → Framing | 60+ rows → one sentence + anchors | problem, process meaning, invariants, constraints, decision-changing Unknowns | `frame.md`: sentence · anchors · open questions · conflicts | estimation behaviour became a cost clause only | one `frame.md` block "What must survive into Options" (4 sub-lists, id-anchored); `(none) — reason` allowed |
| Framing → Options | — | same block | personas read `frame.md` (already) | Options never stated estimation as a requirement; B-04 under-applied | none new — the frame block is the guard; SA reads it against `blocking-set.md` S3 |
| Options → Decision | 12 concern lines + per-option fields → D-NNN | outcome sentence verbatim, conditions, proof obligations, tripwires | `aisa-decide` serialises verbatim | none observed | none |
| Decision → Architecture | D-NNN → `architecture:` block | conditions as open items; su_refs everywhere; structural choices block approval | `aisa-blueprint` steps 1–2, 11 | audit/authorization basis not re-derived after C-057 | targeted revalidation on premise change (§20) + PR-1 |
| Architecture → Deliverables | architecture record → six projections | no silent Unknown resolution; residual lines; gaps with owner | `render-contract.md` (four gap classes; forbidden transformations) | none observed | none |

Two guards are new (frame block; disposition), one is an extension of an existing step (revalidation at
`/answer` / `--refresh`). The rest already exist.

---

## 14. Structural constraints

Definition adopted: *a confirmed or unresolved condition whose truth could materially eliminate, reshape or
gate whole solution classes.* Not an architecture decision. The pack already carries the vocabulary in two
places — Discovery cues (`user_population_identity_class`, `existing_entitlement_baseline`,
`systems_of_record`, `deployment_model_constraint`, `authorization_enforcement_point`,
`offline_operating_requirement`, `connectivity_and_egress_policy_posture`) and the Options blocking set
(B-03 identity class, B-04 source of record, B-05 residency, B-10 network boundary, B-13 sensitivity, B-14
regime, B-23 budget, B-24 entitlement fit, B-27 deployment model). What it lacks is a **pre-Options
visibility point**: constraints survive Discovery only as scattered rows, and `frame.md` has no slot for them.

Placement preserved: Discovery/Framing identify generically → Options tests candidates → Architecture
implements the response (§23 of the brief). Hard vs soft vs unknown uses existing states: a hard constraint
is a `Confirmed` row whose violation disqualifies (decision-tree §3 *Disqualifier*); a soft constraint is a
`Confirmed`/`Assumed` row that becomes a trade-off; an unknown constraint is an `Unknown` with `swing:
decisivo`. **No scoring, no new state.**

### Pilot-1 replay — structural constraints (§55 of the brief)

| Condition | Evidence | Visible pre-Options? | Classification |
|---|---|---|---|
| Audience entirely internal; KAM receive, do not use | C-013 (R-01), C-056 (post-premortem) | partly (C-013 yes; C-056 late but pre-decision) | PRE-OPTIONS STRUCTURAL |
| Sensitivity Interno | C-036 (R-01 answer) | yes | PRE-OPTIONS STRUCTURAL |
| No separate budget; internal IT builds | C-028, C-048 | yes | PRE-OPTIONS STRUCTURAL |
| SAP is the truth for term-contract terms | C-020 → X-002 → C-052 (O-01) | as Conflicted, yes | PRE-OPTIONS STRUCTURAL (resolved in Options) |
| Pricing data authority is a shared SQL Server already operated ("tudo o que é pricing fica nessa base de dados") | C-057 (Blueprint v01 answer to U-029) | **no** — the DB existed and was in use by Spain at Discovery time; nobody asked where pricing data must live | PRE-OPTIONS STRUCTURAL in kind; surfaced in Architecture. B-04 (source of record) at S3 was applied to client terms only |
| Output format continuity for KAM; e-mail push | C-009, C-033 | yes (R-002) | PRE-OPTIONS STRUCTURAL (soft → hard by sponsor expectation) |
| Retention floor 10 years | A-004 / X-005 / C-060 | as Conflicted, yes | PRE-OPTIONS STRUCTURAL UNKNOWN |
| Approval before load (SoD) | C-022, C-026, C-043 | yes | business invariant, not a constraint |
| Connectivity/gateway to the shared SQL exists | C-062 | — | ARCHITECTURE-SPECIFIC (transport prerequisite) |
| Model-driven fit over virtualized SQL | A-009 | — | OPTIONS/ARCHITECTURE-SPECIFIC |
| Entitlement fit of the required capability set | options.md: "não avaliado nesta ronda" | — | OPTIONS-SPECIFIC (B-24), not evaluated |
| Six-sheet duplication | C-041 | — | NOT A CONSTRAINT (a defect to remove) |

One structural constraint of the highest consequence was invisible until Architecture. The question that
would have surfaced it ("is there an existing or mandated data platform for pricing data?") is a
`systems_of_record` cue and a B-04 blocking entry — both existed and were under-applied. A frame block that
must list structural constraints *and* unresolved structural Unknowns gives a second, earlier prompt to notice
the absence of a row about where the data must live. Whether it would have caught C-057: **UNCERTAIN**
(depends on the analyst noticing the absence); whether it would have caught the estimation invariant: **YES**
(the frame already carried it as a cost clause; the block asks for it as a behaviour).

**STRUCTURAL CONSTRAINT CONCEPT WARRANTED: YES** (as a frame.md projection and vocabulary already in the
pack). **NEW STATE: NO.**

---

## 15. Licensing / entitlement placement

| Question | Placement | Pack evidence | Pilot 1 |
|---|---|---|---|
| A — user population / internal-external | **Discovery / Framing** | Discovery cue `user_population_identity_class`; B-03 | C-013, C-056 — answered |
| B — existing entitlement boundary | **Discovery / Framing** | Discovery cue `existing_entitlement_baseline` (financial) | never asked; low materiality for a ~5-person internal team, but the cue exists |
| C — willingness/budget to buy incremental entitlement | **Discovery / Framing** | B-23 budget envelope; `question-bank.md` carries no licensing question (grep `licen|entitle|seat`: none) — correctly technology-neutral | C-028 ("custo implícito… equipa de IT") — answered as funding model |
| D — exact entitlement a candidate requires | **Options** | B-24 at S3; `economics/licensing-and-cost-drivers.md` pulled by the architect | options.md: "Entitlement fit — não avaliado nesta ronda" — a documented non-evaluation |
| E — exact licensing composition | **Architecture** | A11 economics in `architecture-core.md` (drivers only, no prices) | Estimate/spec carry drivers |

Expected placement `A–C → Discovery/Framing · D → Options · E → Architecture` **confirmed** and already
implemented in the pack's vocabulary. Allowed pre-Options: "Is incremental per-user entitlement acceptable?"
"Must data remain in its current system of record?" Not allowed pre-Options: "Do 200 users have Power Apps
Premium?" — the neutrality rule (`.claude/rules/no-tech-mention-before-options.md`) already forbids it.
**LICENSING USER/ENTITLEMENT BOUNDARY BELONGS PRE-OPTIONS: YES. SPECIFIC PRODUCT LICENSING QUESTION
BELONGS PRE-OPTIONS: NO. TECHNOLOGY-NEUTRAL DISCOVERY PRESERVED: YES** — nothing in this addendum names a
vendor before Options; the synopsis inherits the template's neutrality rule verbatim.

---

## 16. Pre-Options sufficiency

Bounded gate (soft, at `/frame` exit and `/options` entry), five questions, no score:

| | Question | Pilot 1 at `/options` entry | How checked |
|---|---|---|---|
| A | Can the process be explained at material depth? | **NO** (calc chain, output families, Simulador role absent) | synopsis present and every material output has a traced or explicitly Unknown lineage (§7) |
| B | Are the behaviours that must survive visible? | **PARTIAL** (approval, format; estimation missing) | frame block "invariants" non-empty or `(none) — reason` |
| C | Are known structural constraints visible? | **PARTIAL** (audience, budget, sensitivity yes; data authority no) | frame block "structural constraints" |
| D | Are unresolved structural constraints visible as Unknowns? | **PARTIAL** (X-005 yes; "where must pricing data live" absent) | frame block "decision-changing Unknowns" + `swing: decisivo` rows |
| E | Are material scope/output/user-task obligations visible? | **NO** (BIOS, what-if, grid entry) | synopsis "outputs and consumers" + "actors × tasks" projected to rows |

**"Sufficiently understood" — refined definition** (§62 of the brief). Candidate: *every material business
outcome traced to inputs, transformations, decisions and consumers, all gaps explicit.* Too strict as
worded only if "material" is unbounded. Refined:

> The current process is sufficiently understood for Options when (a) every output family whose loss,
> change or misdesign would alter an option's viability, scope or shape is traced to its inputs,
> transformations, deciding actors and consumers — or the missing link is an explicit `Unknown`; (b) the
> business behaviours the sponsor cannot lose are stated as rows; (c) every known structural constraint is a
> row and every suspected one is an `Unknown`; and (d) all of this can be said without naming a solution.

Not "everything must be known": HYPOTHESIS and UNKNOWN are legitimate endpoints. **Few Unknowns ≠ deep
understanding** (§29): pricing-marinha entered Options with 2 open Unknowns and health 100% — and failed A
and E above. The gate detects "many isolated facts, no coherent trace" without a new state: it is a
survival-test failure with a named missing trace.

### Failure behaviour (§63 of the brief)

On failure: `/frame` (or `/options`) stays soft-gated — warn, name the specific missing understanding
("`Outputs BIOS` has no consumer recorded"; "the calculation chain from cedência to minimum price is not
traced"), and hand the gap to `/status` as a targeted `reuniao`/`documento` item (existing agenda). Do not
manufacture Options, do not invent a process model, do not start technology comparison. Override with logged
reason remains available (soft gate doctrine unchanged). No generic "need more requirements" message.

### Depth follows materiality (§64 of the brief)

```text
materiality + uncertainty + consequence of misunderstanding → comprehension depth
```

Deep comprehension is not reverse-engineering every formula or asking about every output. In
pricing-marinha the `INDIRECT` mechanics (PM-005) are legitimately non-material at Options; the chain's
*stages* and the *output families* are material. The synopsis carries stages, not cells; cells stay in §2–§5.

---

## 17. Phase vs session

Binding doctrine adopted: **PHASE ≠ SESSION.** A phase may span many sessions; a small engagement may run
several phases in one session. Nothing in the runtime uses a session boundary as a semantic boundary:
`_state.json.phase`/`round` are the only phase markers; `/resume` exists; hooks resolve the engagement from
disk. **PHASE EQUALS SESSION: NO.**

Corollary adopted: **session context is a disposable cache; repository engagement state is durable memory.**
Deep reasoning may be local and temporary; material understanding must be durable and selectively
reloadable. This is a documentation statement (`docs/ARCHITECTURE.md` carries no session doctrine today;
grep `session|resume|rehydrat|handoff` finds only the `/resume` command row).

### Session context dependency audit (§58 of the brief)

Grep of `.claude/skills`, `.claude/agents`, `library/kernel`, `.claude/commands` for implicit chat
dependence (`this conversation`, `earlier`, `previous session`, `in-flight`, `collected`, `verbatim`,
`from memory`):

| Hit | Nature | Material? |
|---|---|---|
| `aisa-frame` step 5/6, `aisa-options` step 5/6, `chairman-synthesis` *Inputs*: persona outputs "collected… verbatim" and handed to the chairman in-turn | transient in-turn hand-off; persona *inputs* persisted in `_council-prep/`, chairman *result* persisted as SU rows + `chairman-synthesis-<round>.md`; raw persona outputs not persisted | **not material** — the durable product of the round is the SU + synthesis log; an interrupted round is detected by `phase-completeness.py` and re-run |
| `.claude/agents/chairman.md` step 6: "read it, do not reconstruct it from memory" | explicitly *anti*-memory | none |
| `aisa-decide` interactive Q&A | persisted verbatim in the D-NNN block | none |
| `aisa-answer` | verbatim in `answers.md` | none |
| `aisa-blueprint` rationale, `open_architecture_choices` | persisted in the YAML | none |
| Discovery inline mode: lenses "share accumulated context" | by design; each lens's persisted product is rows + `lens-outputs/<lens>.md` | **material only in the PR-4 sense**: the coherent cross-source reconstruction a lens builds lives in context and is not persisted (no carrier) |

**No runtime instruction requires the previous transcript. PREVIOUS CHAT TRANSCRIPT REQUIRED TO RESUME:
NO.** The one material dependency is semantic, not procedural: understanding that was never formalised
cannot be rehydrated. That is PR-4, not a session-handling defect.

---

## 18. Session rehydration

Minimum bootstrap for a fresh session — what exists and what is missing:

| Step | Exists | Where |
|---|---|---|
| identify engagement | yes | `aisa-status` step 1 |
| identify phase/round | yes | `_state.json` |
| load authoritative state | yes (SU, decisions) | `aisa-status` reads SU; `/resume` names the next command |
| load compact process synopsis | **no** — no synopsis exists; `process-model.md` §4 is xlsx-only mechanics | PR-4 |
| load material unresolved items | yes | `aisa-status` steps 4–6 (Critical rows, agenda, tripwires) |
| load current phase artefact | implicit (skill Inputs lists) | each skill's *Inputs (read)* |
| pull detailed evidence only if needed | yes | `evidence-index.md` + materiality rule |

Phase-specific read sets, **derived** (not maintained by hand) — a fixed small table the kernel can carry:

| Phase | Read to resume |
|---|---|
| Discovery | `_state.json`, `context.json`, SU, `lens-outputs/*.md` (current round), `_capture/evidence-index.md`, `process-model.md` §4 synopsis |
| Framing | + `frame.md` (if a round ran), synopsis, SU |
| Options | `frame.md` (incl. survival block), SU, `options.md` (if a round ran), synopsis — detail (§2–§5) only if material |
| Decision / Architecture | `decisions.md` (latest D), latest `_blueprint/ux-blueprint_v<NN>.yaml` (note `SEE_V01` back-references force a v01 read — a rehydration cost worth stating), `_synthesis/architecture-story.md`, SU material rows; DK selectively |
| Deliverables | closest authorities only (`render-contract.md` slot order) |

**Bootstrap manifest** (§35 of the brief): `aisa-status` already exposes phase, health, agenda, tripwires and
next action. Adding one derived block to its output —

```text
Read to resume (<phase>):
  decisions.md#D-004 · _blueprint/ux-blueprint_v05.yaml (+v01 for SEE_V01 sections)
  shared-understanding.md — material rows: U-025, U-028, X-003, X-005, X-006
  _capture/process-model.md §4 (synopsis)
```

— is ~6 lines in one skill, derived from `_state.json.phase` and the file system, no new authority, no new
artefact. `/resume` already delegates to `aisa-status`; it needs no change.

**No handoff-summary cascade (§34).** `session-1-summary.md`, `discovery-handoff.md` and the like are
rejected: each would be a second truth with its own staleness. The canonical artefacts are intrinsically
rehydratable once the synopsis exists. **NEW SESSION-HANDOFF ARTEFACT WARRANTED: NO.**

**Evidence-heavy authoring; evidence-light runtime; selectively rehydratable sessions (§46–47).** A fresh
session should not need all source files, all lens outputs, all transcripts or all DK. With the synopsis in
place, the Options read set is `frame.md` + SU + synopsis (~80 KB) instead of SU + four `text.md` files
(~220 KB) — and the second set still fails the teach-back today because the reconstruction has to be
re-done, not re-read.

---

## 19. Fresh-session simulation

Static simulation on the actual Pilot-1 artefacts. No runtime executed; the question is what the persisted
state *can* yield.

### Fresh Framing session (post-Discovery state, no transcript)

Allowed: SU (R-01 rows), `lens-outputs/*.md`, `evidence-index.md` → `process-model.md`, four `text.md`,
`context.json`, `story.md`, `council-log.md`.

| Test | Result | Basis |
|---|---|---|
| Explain the process | organisational flow YES; computation NO from SU+PM; YES only by re-reading both docx `text.md` and re-doing the reconstruction | §11 |
| Material concepts lost if only SU + PM are read | calc chain; até/após rule; BIOS family; Simulador's role; blends; publications consumer | §2, §7 |
| Hallucination risk | PM-001's "counterparty quotes" label vs docx input taxonomy (§4) | one |
| Unnecessary raw-source rereads | none *raw*; but two normalized documents must be re-comprehended end to end — the reconstruction cost repeats every session | — |
| Context burden | SU 52 KB + PM 26 KB + docx text 12 KB + vtt text 148 KB | the transcripts dominate; the synopsis would make them optional |

**FRESH-SESSION FRAMING CONTINUITY: PASS** — the frame itself (sentence, anchors, D-001, open questions,
conflicts) is fully persisted and a fresh session can continue into Options procedurally with the same
frame. The *semantic* depth behind it fails (teach-back FAIL above); continuity of the artefact passes.

### Fresh Options session (post-Framing state + declared authorities)

Allowed: `frame.md`, SU, D-001, `evidence-index.md`, `options.md` (once a round ran).

| Must retain | Retained? | Where / why not |
|---|---|---|
| what-if | **NO** | no row; R-012 is KAM simulation |
| output families | **NO** | BIOS and unit outputs absent as scope |
| task shape | PARTIAL | C-006, C-016; no grid/85-value shape |
| invariants | PARTIAL | C-022/C-026, C-023, C-052, C-009; estimation absent |
| structural constraints | PARTIAL | C-013/C-056, C-036, C-028; data-authority mandate absent |

**FRESH-SESSION OPTIONS CONTINUITY: FAIL** — the in-session Options round had the same state and produced the
same omissions; a fresh session is no worse, and the state is insufficient either way.

### Fresh Architecture session

Allowed: `decisions.md`, `ux-blueprint_v05.yaml` (+v01), SU, `architecture-story.md`, selective DK.

Enough business meaning to avoid a purely entity-driven architecture? **NO.** The persisted state carries a
data-model projection (entities ← `lens=data` rows, per `aisa-blueprint` step 4) and no task model. The
in-session blueprint *was* entity-driven with full context available (P-OBS-028) — so durable memory alone
would not have fixed it; the user-task derivation obligation (§22) is a separate, practice-level item (PR-3).

---

## 20. Semantic invalidation

Doctrine adopted: *a new material fact must trigger reconsideration of conclusions whose validity depended on
the changed premise* — targeted revalidation, not rebuild.

**Dependency without a dependency engine (§38).** Existing references that already encode dependency:
`su_refs` on every blueprint node; `D-NNN` justification ids; `open_architecture_choices.su_ref`;
`forced_by` on compositions; `conditions` and `proof_obligations`; the `was <id>` chain; tripwires. A
targeted rule can be executed by grep over these — no graph.

**Candidate rule** (bounded):

```text
when /answer creates or supersedes a row, or a blueprint version changes an architecture field value
  → list the dependents: rows/fields whose su_refs, anchors or rationale name the changed id or field
  → for each: still valid | revalidate (say why) — written, not implied
  → Decision-phase dependents in decisions.md → tripwire check → /revisit (advisory); never rewritten
```

Trigger scope (§41): new/changed fact **and** material **and** explicitly contradicts or changes an
assumption a downstream conclusion used. No "rerun all phases".

**Authority preserved (§40).** Architecture may reopen its own choice or a tripwire; it never rewrites the
Decision. Where the new fact moves the decision basis, the path is tripwire → `/revisit` — existing
semantics (`aisa-revisit`, `aisa-status` step 7).

**One finding that shapes the rule.** In v01 the surface rationale said "segurança por linha/coluna e
auditoria herdada do store" — a dependency on `record_authority` — while `experience.su_refs` was
`[C-013, C-002, C-056]`. An `su_refs`-only invalidation would have missed it. The dependency was on
another *architecture field*, stated in prose. Hence one contract sentence: **a rationale that depends on
another architecture field names that field** (e.g. `depends_on: [record_authority]`), so a field change
lists it. Cheap, and it is what the chairman did by judgement at v02 (A-009).

**FULL DEPENDENCY GRAPH WARRANTED: NO.**

---

## 21. C-057 replay

| Step | Content |
|---|---|
| **Valid before** | v01: `record_authority` = governed relational store / owned for 3 domains; surface rationale "auditoria herdada do store", "segurança por linha/coluna"; options.md O-004 strengths "segurança nativa por linha/coluna e auditoria nativa… passo de aprovação nativo"; D-002 justification cites R-005 (auditability) as a closed clause |
| **Changed premise** | C-057 (answer to U-029): all pricing data, feed included, lives in an already-operated shared SQL Server — `record_authority` external for 3 domains |
| **Requiring revalidation** | security basis; audit basis; composition pattern (`direct` vs virtualization/replication); access mode; surface fit; the two dashboard screens against query shape; where the calculation engine lives; export/import path; O-004's two "native" strengths; the D-002 auditability clause |
| **What the runtime did** | flipped `record_authority` × 3 and the composition owner (correct); opened A-009 for the *surface* (correct, by the executor's judgement); blocker count 4→2 (honest). Did **not** list audit/security/O-004 strengths as revalidation items; A-009 was recorded as `A-` (Assumed) not `U-`; v03 closed it on connectivity (PR-1) |
| **What the minimal guard would have done** | at `/answer U-029 → C-057`: dependents list = every blueprint field with `su_refs ∩ {C-017, C-035, C-006, C-016, C-018, R-004}` whose value was the store assumption (`record_authority` ×3), plus fields naming `record_authority` as a dependency (experience rationale), plus `decisions.md#D-002` clauses naming R-005/auditability → printed as "revalidate: experience.rationale · security basis · audit basis · D-002 auditability clause (tripwire check)". The new fact does not reverse them; it makes them *not settled* until revalidated |
| **Would the failure have been caught?** | With PR-1 (closure needs mechanism + fit) **and** PR-7 (dependents listed): **YES**. With PR-7 alone: UNCERTAIN — O-004's strengths in `options.md` are not id-anchored to a store row; the dependency is prose |

**C-057 SHOULD HAVE TRIGGERED TARGETED REVALIDATION: YES.** No hindsight applied to unrelated choices
(SAP reference, X-Author relocation, export feature stay valid).

---

## 22. UX / mockup implications

Path to preserve: business behaviour → human task → information required → manipulation/decision →
interaction requirement → surface. Pilot-1 shortcut: Excel named ranges → entities → gallery/form/dashboard
(`screen-consolidation-rules.md` tree is field-count driven; `aisa-blueprint` step 4 compiles entities from
`lens=data` rows and personas from `lens=user` rows — there is no step "compile tasks from `lens=operations`
rows").

Signals present and unused: ~85-value daily entry (PM-001); computed columns visible to users (PM-002/003);
what-if (`Simulador`, sponsor ask #2, Pedro's own description of his intervention); comparison across
weeks ("o maior dos 2"); approval (C-026). **Hypothesis confirmed on the evidence**: the prototype represents
the data model, not the analyst's task. The surface question is not "Canvas vs model-driven" (8B §10 removed
that presumption); it is "what does the analyst do on Monday morning?" — unanswerable from persisted state.

Minimum: one sentence in `aisa-blueprint` step 4 — *tasks ← `lens=operations` rows and the synopsis's
actors × decisions; each screen names the task it serves* — plus the synopsis making the tasks available.
Practice-level (PR-3), not a new layer.

---

## 23. Specification implications

Implementation Spec v02 §13 acceptance: "O ciclo diário completo (dados-mestre → cálculo → aprovação →
output) corre… com registo auditável completo" — a single V4 line. §6 automation: `(none)`. §4 entities: a
table of stores. The Estimate's Fase 0 "Formalizar regras do Excel — 4d" is the only place the calculation
layer is sized. There are no calculation work packages, no edge cases (missing quote, six-sheet
divergence beyond a test-scenario mention), no validation scenarios per output family, no migration
(A11 not engaged).

The render layer behaved correctly — it may not invent upstream meaning. A stronger specification requires
the meaning to exist upstream: the synopsis's transformation stages become material transformation
obligations (rows) → options concern → blueprint → spec work packages with business acceptance conditions
("a missing Monday quote never yields zero; the conservative rule applies and is logged"). **Deep
comprehension materially improves acceptance conditions, calculation packages, edge cases and validation
scenarios — but only through the upstream carrier; the Design Brief and Spec must never recover it by
re-reading raw evidence (§45).**

---

## 24. Context dilution

One session accumulated: five inputs (≈650 KB raw), capture, six lens outputs, 84 SU rows, frame, options,
premortem ×2, five blueprints, five synthesis packs, twelve rendered deliverables. Pilot 1 reported no
systemic ceremony (report §19) and no quality degradation attributable to length — but the entity-driven
architecture and the unrevalidated audit basis happened *late* in that session. Causation cannot be shown at
n=1; the direction of risk is clear. The architecture already supports deliberate shedding (pull-based DK,
parse-once evidence, `_council-prep` excerpts). What is missing for a *reload* is the synopsis (§12) and the
read-set (§18). **Deep reasoning local and temporary; material understanding durable and reloadable** —
adopted.

---

## 25. Determinism boundary

Deterministic (constrained): what must survive (§13 classes); what is authoritative (SU; decisions;
architecture record); what cannot be silently dropped (disposition; frame block; residual lines); what must
be revalidated (§20 rule); what a fresh session reloads (§18 read set).

Not prescribed (free): the order of exploratory hypotheses; the number of reasoning passes; the number of
questions; the internal chain of thought; how a lens reads a transcript; what a persona proposes.

Every repair in §26–§34 was checked against this line. None adds a reasoning procedure, a checklist a lens
must cover, a scoring formula or a routing table. The OBSERVED/INFERRED/HYPOTHESIS/UNKNOWN marking
constrains **how a conclusion is labelled when persisted**, not how it is reached. **Constrain semantic
survival, not internal cognition.**

---

## 26. Ceremony analysis

| Repair | Lines / instructions added (est.) | Mandatory reads added | New artefact | New state | New loop | New questions | New runtime branch | Expected semantic benefit |
|---|---|---|---|---|---|---|---|---|
| **R-4 synopsis + source scope** (`process-model.template.md` §4, `aisa-capture` step 5a + hard rule, `orchestration.md` one sentence) | ~15–20 | L2 reads `*.text.md` — one pass per capture, not per lens | none | none (markers map to existing states) | none | none new (PM-U list widens its incoherence shapes) | none | closes 3 Capture→SU loss types; makes teach-back and rehydration possible |
| **R-2A widened disposition** (one paragraph in `aisa-round` context or one line per lens *Open evidence*) | ~3–6 | none | none | none | none | none | none | PM-U Critical and synopsis material lines get adopt/map/dismiss — the missing projection obligation |
| **R-5 frame survival block** (`chairman-synthesis` Framing template; `aisa-frame` step 7 display + soft gate line) | ~10 | none (personas already read `frame.md`) | none | none | none | none | none | invariants, constraints, decision-changing Unknowns survive into Options as one block |
| **R-7 targeted revalidation** (`aisa-answer` step 7; `aisa-blueprint` step 11 + `depends_on`) | ~8–10 | grep of ids across existing files | none | none | none | none | none | dependents listed on premise change; no graph |
| **R-6 derived read-set** (`aisa-status` step 9 block) | ~6 | none | none | none | none | none | none | operational rehydration; testable |
| **R-8 doctrine lines** (`orchestration.md` classes + boundary question; `ARCHITECTURE.md` phase≠session) | ~10 | none | none | none | none | none | none | shared vocabulary for boundary checks |
| Rejected: new `process-understanding.md`; handoff summaries; dependency graph; compression matrix; new state/label; mandatory human teach-back; question engine | — | — | 1–5 | 1 | — | many | yes | duplicated truths, ceremony > risk reduction |

No repair's framework cost exceeds the observed risk reduction. All are edits to text in existing skills,
templates and kernel docs. **NEW RUNTIME MACHINERY REQUIRED: NO.**

---

## 27. PR-4 adjudication — Deep Process Comprehension

**Classification: PROVEN-GENERIC** (structural, per the §65 standard):

- material observed failure — three Capture→SU losses, the calculation chain absent from every reasoning
  artefact, teach-back fails from persisted state;
- structurally reproducible under the current runtime — the L2 model is `.xlsx`-only by three contract
  statements; no artefact is responsible for cross-source reconstruction; lenses persist atoms; any
  multi-source process-replacement engagement reproduces it regardless of reasoning quality;
- repair engagement-independent — yes;
- low complexity — ~20 lines across a template, a skill and one kernel sentence; no new artefact/state.

Bounded repair: **R-4** (§26). Not: a reasoning procedure, a mandatory section list, a formula-by-formula
mandate. The process-reconstruction dimensions (§6) are guidance to the L2 prompt; sections appear only where
material.

---

## 28. PR-5 adjudication — Structural Constraint Survival

**Classification: PROVEN-GENERIC** — narrowly, as the *carrier gap*:

- material observed failure — the estimation behaviour reached Framing as a cost clause and left it as an
  exposure (A-008); one structural constraint of the highest consequence (C-057) was invisible until
  Architecture;
- structurally reproducible — `frame.md` has four sections (sentence · anchors · open questions · conflicts)
  and no place for behaviours or constraints; they survive only as scattered rows and the Options concern
  list does not ask for "obligations every option must satisfy";
- repair engagement-independent and low complexity — one block, ~10 lines.

Catch probability at n=1: estimation invariant **YES**; C-057 **UNCERTAIN**. Honest scope: the block is a
second chance, not a guarantee; B-04 at S3 remains the primary Options-side check and was under-applied
(practice).

Bounded repair: **R-5** (§26). Not: a new state, a constraint register, a score.

---

## 29. PR-6 adjudication — Cross-Session Semantic Rehydration

**Classification: DOCUMENTATION** — with one derived output line:

- no cross-session failure was observed (single-session pilot);
- static simulation shows the *state* is insufficient (teach-back FAIL; Options continuity FAIL) — but the
  insufficiency is PR-4/PR-5's, not a rehydration mechanism's;
- `/resume` and `aisa-status` already provide the bootstrap; the read-set block is derived and trivial;
- the fresh-session adversarial test (§36 of the brief) is a **Pilot-2 protocol item**, not runtime.

Bounded repair: **R-6** (derived read-set in `aisa-status`) + doctrine lines (phase ≠ session; context as
cache) + the fresh-session test written into the Pilot-2 protocol. **No handoff artefacts.**

---

## 30. PR-7 adjudication — Semantic Invalidation on Material Change

**Classification: PROVEN-GENERIC**:

- material observed failure — audit/security basis and O-004 strengths carried unrevalidated after C-057;
  the S4 chain rests on it;
- structurally reproducible — no step lists dependents when a row is superseded or an architecture field
  flips; `aisa-answer` step 7 prompts only "verifica se [o swing] se materializou" for Unknowns (A-009 was
  Assumed, no swing); P-OBS-014's correct partial reaction was executor judgement, not contract;
- repair engagement-independent, low complexity — ~10 lines, grep over existing references, `depends_on`
  on rationale.

Bounded repair: **R-7** (§26). Reuses `su_refs`, D-NNN anchors, tripwires, `/revisit`. **No dependency
engine.** Overlap with PR-1: PR-1 governs *how a structural choice may close*; PR-7 governs *what reopens
when a premise changes*. Complementary, not duplicate; both needed for the C-057 chain (§21).

---

## 31. PR-8 adjudication — Material Meaning Survival Across Compression

**Classification: DOCUMENTATION** — the class list and the boundary question are doctrine (~10 lines in
`orchestration.md`). Its two proven subsets are not separate repairs:

- Capture→SU subset → carried by R-4 + R-2A (PR-4);
- SU→Framing/Options subset → carried by R-5 (PR-5);
- Options→Architecture subset → carried by R-7 + PR-1;
- Architecture→Deliverables → already enforced by `render-contract.md`; no change.

**No matrix, no per-artefact repetition rule.**

---

## 32. Consolidation with PR-1 / PR-2A

| Candidate | Relationship |
|---|---|
| PR-1 (technical-claim closure) | separate; complementary to PR-7 at the Decision→Architecture boundary |
| PR-2A (PM-U adopt/map/dismiss) | **subsumed** into the comprehension-survival contract: its disposition step is the same step that disposes of synopsis material lines |
| PR-4 | core of the consolidated contract |
| PR-5 | the Framing projection of the same contract |
| PR-8 | doctrine wrapper; proven subsets carried by PR-4/PR-5/PR-7 |
| PR-6 | documentation + one derived line; independent |
| PR-7 | separate bounded obligation; reuses existing references |

**The consolidation the brief asks about (§52) holds**: PR-2A + PR-4 + PR-8(Capture→SU) are one principle —
*material process semantics captured during reconstruction must receive an explicit downstream disposition
before compression* — and should ship as **one bounded contract** ("comprehension survival"), not three
rules. PR-7 reuses `su_refs`, tripwires and open choices rather than adding machinery. Duplicate guards
avoided: the frame block is the only new slot; the disposition is one step; the synopsis is one section.

---

## 33. Package A / B / C / D comparison

| | A — Guidance only | **B — Comprehension survival** | **C — B + session continuity** | D — New semantic artefact / framework |
|---|---|---|---|---|
| Content | practice notes; no runtime text | R-4 synopsis + source scope; R-2A disposition; R-5 frame block; R-7 revalidation; R-8 doctrine | B + R-6 derived read-set + fresh-session test in Pilot-2 protocol + phase≠session doctrine | new `process-understanding.md`; survival matrix; handoff files; possibly a new label |
| Pilot-1 loss coverage (6) | 0–1 (depends on the analyst) | 5 of 6 (grid task shape UNCERTAIN → PR-3 practice) | same 5 | same 5 |
| Semantic coverage of P1–P5 | none durable | P1, P2, P4, P5 | P1–P5 | P1–P5 |
| Complexity | none | ~55 lines of contract text across 6 existing files | + ~6 lines + protocol doc | new artefact + ownership + sync rules |
| Context cost | none | one heavier capture pass; lighter Options/Architecture reads | + one status block | second file to read every phase |
| Duplication risk | none | low (one owner per concept, §60) | low | **high** — two process truths |
| Cross-session robustness | untested, likely FAIL | improved but unmeasured | improved **and testable** | improved; duplicated |
| Verdict | insufficient — Pilot 1 shows unprompted practice does not persist the reconstruction | sufficient for observed losses | **smallest package covering all five properties** | rejected — violates one-source and no-new-layer |

**RECOMMENDED PACKAGE: C** — with the explicit note that C minus the read-set line and the test protocol is
B, and that those two increments add no artefact, state, loop or branch.

### One-source table (§60 of the brief)

| Persisted concept | Semantic owner | Durable carrier | Projection consumers |
|---|---|---|---|
| process synopsis (flow, stages, outputs, consumers, hypotheses) | `aisa-capture` L2 | `_capture/process-model.md` §4 | lenses (disposition), frame block, options personas, blueprint step 4, `/status` teach-back item |
| business invariant | SU row (Confirmed/Assumed) | SU | frame block → options → blueprint |
| structural constraint | SU row | SU | frame block → S3 blocking set → architecture |
| decision-changing Unknown | SU Unknown (`swing: decisivo`) | SU | frame block, `/status` agenda, `/simulate` VOI |
| revalidation list | derived at `/answer` / blueprint version | `open_architecture_choices` (revalidate) / `/revisit` artefact | blueprint, decisions (advisory) |
| read-to-resume set | derived by `aisa-status` | none (computed) | `/resume` output |

No concept has two owners. Multiple projections are allowed and expected.

---

## 34. Recommended Step 8C scope

Proposed exact scope (design only; nothing implemented here):

1. **PR-1** — technical-claim closure enforcement: R-A (`aisa-answer` step 4) + R-B (`aisa-blueprint` step
   15 / structural closure) + TC-1..TC-5 test module — unchanged from 8B.
2. **Comprehension-survival contract** (PR-2A + PR-4 + PR-5 + PR-8 subsets, one bounded change set):
   - `process-model.template.md` §4 → cross-source synopsis with OBSERVED/INFERRED/HYPOTHESIS/UNKNOWN marking
     and the material classes; PM-U incoherence shapes named;
   - `aisa-capture` step 5a + *Supported formats* + hard rule 7 clarification: L2 reads all normalized
     evidence; LT unchanged;
   - `orchestration.md`: one sentence lifting the `.xlsx`-only L2 scope; the material-survival classes and
     boundary question (~10 lines);
   - `aisa-round` step 4b context (or one line per lens *Open evidence*): explicit disposition of PM-U rows
     and synopsis material lines — adopt / map / dismiss with reason;
   - `chairman-synthesis` Framing artefact: block "What must survive into Options" (process meaning ·
     invariants · structural constraints · decision-changing Unknowns), id-anchored, `(none) — reason`
     allowed; `aisa-frame` step 7 shows it; soft-gate line names any missing material trace;
   - `aisa-status` step 6: when the synopsis carries a material HYPOTHESIS/UNKNOWN, one teach-back
     `reuniao` item replaces the corresponding atomic questions.
3. **PR-7 targeted revalidation**: `aisa-answer` step 7 dependents list; `aisa-blueprint` step 11 field-change
   revalidation + `depends_on` on rationale; Decision-layer dependents route to tripwire check → `/revisit`.
4. **PR-6 documentation + derived line**: `aisa-status` "Read to resume" block; `ARCHITECTURE.md` phase ≠
   session, context-as-cache doctrine; `docs/pp-pack-authoring/pilot/` Pilot-2 protocol gains the
   fresh-session adversarial test (Session A closes Discovery; Session B rehydrates from declared state only;
   record lost/hallucinated concepts, rereads, burden).
5. **PR-3 practice** (from 8B): `aisa-blueprint` step 4 one sentence — tasks compiled from `lens=operations`
   rows and the synopsis; each screen names the task it serves. Watch in Pilot 2.

Test cases to add to the Step 7-style module (design): TC-6 fresh-session teach-back on pricing-marinha state
after re-capture names calc chain, output families, Simulador role and Mon/Tue behaviour or marks each
Unknown; TC-7 every Critical PM-U has a disposition; TC-8 `frame.md` survival block present and id-anchored;
TC-9 `/answer` on a row cited by `record_authority.su_refs` lists dependents; TC-10 synopsis contains no
vendor/product name.

Explicitly **not** in Step 8C: a new process-comprehension artefact; a dependency graph; a compression
matrix; handoff summaries; a new state or label; mandatory human teach-back; a question engine; any change
to Steps 3–7 semantics (decision tree, registers, DK, architecture templates, deliverable contracts).

**STEP 8C SCOPE SHOULD EXPAND: YES** — from two candidates to the five items above, consolidated so that
the net addition is one contract, one obligation, one derived output and doctrine text.

---

## 35. Final verdict

Pilot 1's semantic losses are not six missing fields and not one defect. They are: a comprehension carrier
that does not exist (the only reconstruction artefact may not read the documents that explain the process),
a Framing artefact with no slot for what must survive, a projection obligation promised but unwired, and a
runtime that flips a premise without listing what depended on it. Each is structural, engagement-independent
and cheap to repair with text in existing files. None requires new machinery. Claude's natural reasoning
was not the weak point — the pilot's lens narratives show it read everything and understood much of it. What
failed was durability: the understanding never became state, so it could not be compressed honestly, could
not be rehydrated, and could not be revalidated. Determinism should be spent exactly there.

```text
STEP 8B ADDENDUM — SEMANTIC CONTINUITY: PASS
PREMATURE COMPRESSION PROVEN: YES
EXTRACTION DEPTH SUFFICIENT: PARTIAL
PROCESS COMPREHENSION DEPTH SUFFICIENT: NO
EXPLORATION BEFORE FORMALISATION WARRANTED: YES
DURABLE PROCESS COMPREHENSION MEMORY WARRANTED: YES
EXISTING PROCESS-MODEL CAN CARRY DURABLE COMPREHENSION: YES
NEW PROCESS-COMPREHENSION ARTEFACT WARRANTED: NO
BUSINESS INVARIANT TREATMENT: EXISTING-SEMANTICS
TEACH-BACK SURVIVAL TEST WARRANTED: YES
HUMAN TEACH-BACK VALIDATION: MATERIALITY-TRIGGERED
STRUCTURAL CONSTRAINT CONCEPT WARRANTED: YES
STRUCTURAL CONSTRAINT REQUIRES NEW STATE: NO
LICENSING USER/ENTITLEMENT BOUNDARY BELONGS PRE-OPTIONS: YES
SPECIFIC PRODUCT LICENSING QUESTION BELONGS PRE-OPTIONS: NO
TECHNOLOGY-NEUTRAL DISCOVERY PRESERVED: YES
PHASE EQUALS SESSION: NO
PREVIOUS CHAT TRANSCRIPT REQUIRED TO RESUME: NO
CROSS-SESSION REHYDRATION WARRANTED: YES
NEW SESSION-HANDOFF ARTEFACT WARRANTED: NO
FRESH-SESSION PROCESS TEACH-BACK: FAIL
FRESH-SESSION FRAMING CONTINUITY: PASS
FRESH-SESSION OPTIONS CONTINUITY: FAIL
SEMANTIC INVALIDATION ON MATERIAL CHANGE WARRANTED: YES
FULL DEPENDENCY GRAPH WARRANTED: NO
C-057 SHOULD HAVE TRIGGERED TARGETED REVALIDATION: YES
MATERIAL COMPRESSION-SURVIVAL GUARD WARRANTED: YES
NEW COMPRESSION MATRIX WARRANTED: NO
PARSE-ONCE BOUNDARY PRESERVED: YES
PILOT-1 WHAT-IF LOSS WOULD LIKELY HAVE BEEN CAUGHT: YES
PILOT-1 OUTPUT-BIOS LOSS WOULD LIKELY HAVE BEEN CAUGHT: YES
PILOT-1 CALC-LAYER LOSS WOULD LIKELY HAVE BEEN CAUGHT: YES
PILOT-1 C-057 STALE-CONCLUSION FAILURE WOULD LIKELY HAVE BEEN CAUGHT: YES
PR-4 DEEP PROCESS COMPREHENSION: PROVEN-GENERIC
PR-5 STRUCTURAL CONSTRAINT SURVIVAL: PROVEN-GENERIC
PR-6 CROSS-SESSION REHYDRATION: DOCUMENTATION
PR-7 SEMANTIC INVALIDATION: PROVEN-GENERIC
PR-8 MATERIAL COMPRESSION SURVIVAL: DOCUMENTATION
RECOMMENDED PACKAGE: C
NEW RUNTIME MACHINERY REQUIRED: NO
STEP 8C SCOPE SHOULD EXPAND: YES
```
