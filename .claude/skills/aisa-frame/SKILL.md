---
name: aisa-frame
description: Transition Discovery → Framing. Checks Discovery's soft exit gate, flips _state.json to phase=framing/round=F-01, launches 6 council personas in parallel via the Task tool (council-independent mode), then invokes the chairman-synthesis skill to write frame.md and the synthesised Shared Understanding rows. On user validation, registers the frame approval (next free D-NNN, with the sentence's fingerprint) in decisions.md.
---

# aisa-frame

## Usage

`/frame [--override "<reason>"]`

- No argument: runs the soft gate check; if any criterion is red and no override is provided, stop with a clear summary and ask the user before proceeding.
- `--override "<reason>"`: bypass the soft gate. The reason is logged in `decisions.md`.

## Phase model

- **From**: `phase: discovery`.
- **To**: `phase: framing`, `round: F-01` (subsequent framing rounds become `F-02`, `F-03`, …, by re-running `/frame`).
- **Mode**: `council-independent`. See `library/kernel/orchestration.md`.

The aisa-frame skill is itself **NOT a lens** — it does no lens analysis. It is the orchestrator that fans out to the 6 council personas (Discovery lenses, embodied as agents) and then in-fans to the chairman synthesis.

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/council-log.md`.
- `<engagement>/lens-outputs/*.md` (so you can compose each persona's thematic SU excerpt).
- `library/kernel/phases.md` (Framing entry criteria).
- `<engagement>/_capture/evidence-index.md` (the shared evidence surface handed to every persona).
- `<engagement>/_capture/process-model.md` §4 (the process synopsis) and §6 (PM-U) — for the comprehension-survival soft gate (step 2) and the chairman's survival block; when absent, the gate runs on the SU alone and says so.
- `<engagement>/lens-outputs/*.md` `Open evidence` blocks — where the dispositions (`MAP` / `ADOPT` / `DISMISS`) live.
- `library/packs/<pack>/pack.yaml` — `lenses_config.<lens>.extra_signals` only, as attention cues.
- `.claude/skills/chairman-synthesis/SKILL.md` → *Council launch preamble* (the persona prompt is built from it).

`<engagement>` resolves to `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, otherwise `projects/<slug>`. `<pack>` is read from `_state.json.pack`.

## Outputs (written, via chairman-synthesis except where noted)

- `<engagement>/_state.json` (atomic write — this skill).
- `<engagement>/frame.md` (chairman-synthesis).
- New rows in `<engagement>/shared-understanding.md` (chairman-synthesis).
- `<engagement>/lens-outputs/chairman-synthesis-F-<NN>.md` (chairman-synthesis).
- A `D-NNN — Frame agreed (F-NN)` record in `<engagement>/decisions.md` after the user validates the frame sentence (this skill, on validation), carrying `Frame sha256` — the fingerprint of the sentence approved.
- `<engagement>/council-log.md` summary lines (this skill + chairman-synthesis).

## Execution steps

### 1. Pre-flight

1. Resolve the engagement root and read `_state.json`. If `phase != discovery` → stop with: "/frame transitions Discovery → Framing; current phase is `<phase>`. Use /options or /decide instead." Exception: if `phase == framing` already, treat this as a re-run (subsequent framing round).
2. Read `library/kernel/phases.md`, section "Phase 2: Framing — Entry criteria".

### 2. Soft gate check (Discovery exit criteria, advisory)

**The mechanical verdict already exists.** The `phase-gate-check.py` hook evaluated Discovery's criteria before this skill loaded and wrote them to `<engagement>/gate-log.md` (id `G-discovery-framing-...`, coverage *n de m por codigo*). Read that line, repeat it to the user, and add what the motor does not do: the comprehension test below is recorded there as `juizo`, and it is yours. A criterion recorded as `n/a` is never re-stated as OK.


Compute from `shared-understanding.md`:

- `confirmed_count` — rows in `## Confirmed`.
- `unknown_critical_count` — rows in `## Unknown` with `criticidade = Critical`.
- `conflicted_critical_count` — rows in `## Conflicted` with `criticidade = Critical`.
- `lenses_with_output` — set of lens narratives present under `lens-outputs/` (expect `business`, `operations`, `user`, `data`, `governance`, `financial`).

Soft criteria from `phases.md`:
- `confirmed_count ≥ 10`.
- `unknown_critical_count == 0`.
- `conflicted_critical_count == 0`.
- `len(lenses_with_output) == 6`.
- `_state.json.round_in_progress` empty. Non-empty and ahead of `round` means a passagem is still open: part of the lenses ran and the round never closed (`library/kernel/phases.md` → *Rounds — in progress vs completed*). Soft, like the rest — report it as a red criterion naming the open round and the lenses that did not run (`engagement.lentes_ronda_aberta.em_falta` from the motor — never inferred from the habitual order, since `/round <lens>` runs lenses alone in any order), and offer `/round --close` (or `/round <lens>` for each missing one) before the transition. The flip in step 5 clears `round_in_progress` either way: Framing does not inherit an open Discovery round.

**Comprehension survival test** (same gate, same soft doctrine — no score, no completeness percentage, no fixed question count). Read the SU and, where it exists, `_capture/process-model.md` §4/§6 plus the lens `Open evidence` blocks, and answer each question with the ids that make it true or with the concrete missing understanding:

1. Can the material process be explained without naming the future solution?
2. Is every materially important output family traceable (inputs → transformations → consumer) or explicitly `Unknown`?
3. Are the behaviours the business cannot lose represented as rows?
4. Are the known structural constraints represented as rows?
5. Are the suspected decision-changing structural constraints explicit `Unknown`s (`swing: decisivo`)?
6. Are the material scope / user-task obligations visible as rows?
7. Has every Critical `PM-U` row and every labelled material synopsis line received a disposition (`aisa-round` step 5e — `undisposed` must be empty)?

A failing question is a red criterion. **Do not pretend comprehension is sufficient**: name the missing understanding concretely — shape: `output X has no identified consumer`, `material calculation chain Y is not reconstructed`, `structural question Z (where must the data live?) is still absent`, `PM-U-NNN (Critical) undisposed` — and route it through the existing mechanisms: another `/round <lens>` to adopt or dismiss it into the SU, or `/answer` when the sponsor already answered. Never manufacture an SU row, a process model or an Options set from this gate. Few open Unknowns ≠ deep understanding: a 100% epistemic health with an untraced material output family still fails question 2.

If any criterion is red AND no `--override` was passed → stop with a one-line-per-criterion summary and ask the user: "Proceed anyway (re-run with `--override "<reason>"`)? Or run more Discovery rounds (`/round`)?" Do not transition yet.

If `--override` is set, log the override reason — it goes into `decisions.md` as part of the frame approval's metadata (`Override used at /frame`, the existing soft-gate record; no new field). An override of the comprehension survival test names the failing question(s) in the reason.

**Override ≠ evidence · override ≠ resolution · override ≠ absence.** An override changes whether execution may proceed; it never changes what is known. The gate output therefore records, and the chairman reads:

```text
gate: FAIL
missing understanding: <category> — <specific gap>   (one line per gap)
override: YES
override reason: <reason>
proceed: allowed under existing soft-gate doctrine
```

The missing item stays visible as what it honestly is — an SU `Unknown` (written first, through the existing authority model, if it does not yet exist), an unresolved material trace, or an `undisposed` line named by `aisa-round` step 5e — and the chairman projects **that id** into the survival block. The chairman never writes `(none) — <override reason>`: `(none) — <reason>` is reserved for the substantive conclusion that **no material item of that semantic class exists for this engagement** (`chairman-synthesis` → rules for the survival block). An override that hides a missing material trace behind `(none)` is a defect, not a projection.

### 3. Flip state to Framing (atomic)

1. Determine the framing round:
   - If `_state.json.round` does not yet start with `F-` → set `round = F-01`.
   - Else → increment (`F-01` → `F-02`).
2. Update `_state.json`: `phase = framing`, `round = <F-NN>`, `round_in_progress = ""` (an open Discovery passagem does not cross the phase boundary; it stays in the log, not in the state). Write atomically: `_state.json.tmp` → `Move-Item -Force` (Windows) / `mv` (Unix).
3. Update the SU header `Fase actual: Framing` and `Última actualização: <ISO timestamp>`.

### 4. Compose thematic Shared Understanding excerpts

For each of the 6 personas, slice the SU into a thematic excerpt:

| Persona | Slice |
|---|---|
| business-analyst | All rows where `lens = business` + any row touching shadow stakeholders, KPIs, sponsor authority |
| operations-lead | All rows where `lens = operations` + any row touching as-is process steps, volumes, cycle times |
| user-advocate | All rows where `lens = user` + any row touching personas, devices, accessibility |
| data-steward | All rows where `lens = data` + any row touching sensitivity, ownership, retention |
| compliance-officer | All rows where `lens = governance` + every Conflicted row + every row touching audit/access control |
| cfo-lens | All rows where `lens = financial` + any row touching cost, volume × time anchors |

Each excerpt is a Markdown fragment with the section headers preserved. **Every excerpt must ALSO include the resolved rows and their resolutions** (rows marked `resolved →` plus the `C-` rows carrying `(was …)`), under a heading "Resoluções já fechadas (não re-litigar)" — otherwise personas whose slice missed a resolution re-raise closed conflicts (observed in live validation). Save each as a transient file under `<engagement>/lens-outputs/_council-prep/F-<NN>-<persona>.md` so the audit trail can show what each agent saw. Save the union of these into the council-log too.

**solution-architect is NOT invoked in Framing.** Do not launch it. (Its own agent file refuses if called pre-Options.)

### 4b. Assemble the common council context

Bookkeeping only — the same resolution `aisa-round` step 3.6 performs, reused here. The orchestrator
resolves paths and one manifest key; it decides nothing about what any of it means.

a. **Shared evidence** — `<engagement>/_capture/evidence-index.md`. Present → carry its path into every
   persona prompt. Absent → carry the explicit line
   *"no `_capture/evidence-index.md` — raw `inputs/` is the evidence surface"*; never let a persona
   assume a shared capture exists. Name likewise any source reported `failed` or `skipped`. Do **not** rank, assign, summarize or bundle sources,
   and do not build a per-persona evidence view: the index is a source map, and which of it matters
   is the persona's judgement. This replaces the old instruction to read every file under `inputs/`.
b. **Pack attention cues** — read `_state.json.pack`, resolve `library/packs/<pack>/pack.yaml` →
   `lenses_config.<lens>.extra_signals` for the lens each persona is the council voice of
   (business-analyst → business · operations-lead → operations · user-advocate → user · data-steward →
   data · compliance-officer → governance · cfo-lens → financial). Missing `pack` key, missing
   `lenses_config.<lens>`, missing `extra_signals` or an empty list → inject nothing for that persona
   and omit the cue line. A `pack.yaml` that does not parse is a visible failure — report it and stop.
   Pass the tokens through **verbatim**: no scoring, ranking, filtering, reordering or rewriting.
c. **Memory pointer** — `.claude/agent-memory/_universal/<persona>/*.md` (incl. `diary.md`) and
   `_tenant/<tenant>/<persona>/*.md`. A pointer, never contents.

### 5. Launch the 6 personas in parallel via the Task tool

Send **one assistant message with 6 Task tool calls** so they execute concurrently. Each Task call:

- `subagent_type`: the persona name (`business-analyst`, `operations-lead`, `user-advocate`, `data-steward`, `compliance-officer`, `cfo-lens`).
- `description`: e.g., "Framing F-01 — business angle".
- `prompt`: the **council launch preamble**, authored once in `.claude/skills/chairman-synthesis/SKILL.md`
  → *Council launch preamble*, used verbatim with these substitutions:
  - `<phase>` = `Framing` · `<round>` = `F-<NN>` · `<slug>`, `<pack>`, `<engagement>` = this engagement
  - `<persona>` = the persona being launched; its `_council-prep` excerpt path is `F-<NN>-<persona>.md`
  - shared evidence · pack cues · memory pointer = whatever step 4b resolved for that persona
  - keep the `[Framing, all personas]` technology-neutrality line; drop the `frame.md` read (Options only)
    and the other bracketed selectors

  The preamble is the whole prompt: it carries mode, phase, round, engagement, pack, the excerpt, the
  evidence pointer, the cues, the memory pointer, the independence rule, technology neutrality, the
  evidence-integrity invariant and the return schema. Do not restate any of it, and do not tell a
  persona to read its lens `SKILL.md` — one channel, chosen deliberately
  (`library/kernel/orchestration.md` → *Persona boundary*).

Wait for all 6 to return. Collect their tool results verbatim.

### 5b. Dialectic round (conditional)

If chairman-synthesis returns material divergences (its Step 2b), run the antithesis round BEFORE it writes anything: for each divergence (max 3 per round), launch 2 Task calls in parallel — each side's persona receives the other's full thesis with this prompt:

```
Estás na ronda dialéctica de <fase> <ronda> do engagement <slug>. A tua proposta diverge da
da persona <X> neste ponto: <divergência, citada verbatim com ids>.
Lê a tese completa dela (em anexo). A tua tarefa NÃO é defender a tua — é atacar a tese
mais forte dela com a melhor evidência disponível, e depois dizer honestamente:
(1) onde ela tem razão; (2) onde falha e porquê (com ids/inputs);
(3) a síntese que proporias se tivesses de assinar as duas.
Devolve nas secções: Concedo / Contesto / Síntese proposta. Máx. 300 palavras.
```

Collect the `Concedo / Contesto / Síntese proposta` returns and re-invoke chairman-synthesis with theses + antitheses. Cost cap: ≤6 extra calls per round; if there are more than 3 material divergences, take the 3 with the highest impact on the phase artefact and record the rest as Conflicted directly.

### 6. Hand off to chairman-synthesis

Invoke the `chairman-synthesis` skill with:

- The 6 persona outputs (just collected).
- The current `<engagement>` paths.
- Phase = `framing`, round = `F-<NN>`.

The chairman-synthesis skill writes `frame.md`, the new SU rows, and the synthesis log. Wait for it to return.

### 7. Present the frame to the user and ask for validation

Output to the user (business language — `CLAUDE.md` → *Duas línguas*; kernel labels and ids only between parentheses). The contract block *What must survive into Options (projection of SU ids — `frame.md`)* renders as «O que tem de sobreviver até às alternativas»: same five sub-lists, same `(none) — <reason>` semantics, ids projected from the SU.

```user-output
Proposta de frase do problema (passagem F-NN):

  <a frase, de `frame.md`>

Em que se apoia:
  - <uma linha por cláusula, com os factos que a sustentam (ids)>

Perguntas em aberto que ainda pesam: <nenhuma | <pergunta curta> (U-nnn) …>
Onde as fontes ainda se contradizem: <nenhuma | <contradição curta> (X-nnn) …>

O que tem de sobreviver até às alternativas (frame.md):
  O que o processo significa:        <uma linha (ids)> | nada — <porquê>
  Regras do negócio que não mudam:   <uma linha cada (ids)> | nada — <porquê>
  Restrições estruturais:            <uma linha cada (ids)> | nada — <porquê>
  Perguntas que mudam o caminho:     <uma linha cada (ids)> | nada — <porquê>
  Obrigações de âmbito e tarefas:    <uma linha cada (ids)> | nada — <porquê>

Compreensão suficiente para avançar: <sim | não — falta: <categoria — lacuna>, … · avançar mesmo assim: sim — <razão> (D-NNN)>

A seguir: valida a frase — a pergunta vem já a seguir (aceitar · editar · mais passagens).
```

**Before asking, check whether this sentence is already approved.** Run
`python library/kernel/tools/dashboard.py --engagement <slug> --json <tmp>/model.json --quiet`
and read `frame.verdict` (`library/kernel/phases.md` → *Frame approval record*). `match` or
`match-other-round` → the sentence did not change since approval `frame.latest.id`: **do not
ask again and do not write a new block**. Append one line to `council-log.md` —
`F-<NN> — frame unchanged since <D-00x> (sha256 match) — aprovação mantida` — and tell the
user:

```user-output
A frase do problema não mudou desde que foi aprovada (D-00x) — continua aprovada; nesta passagem só as âncoras foram refeitas.
A seguir: → `/options` para pôr as alternativas na mesa.
```

Otherwise ask via `AskUserQuestion` (never a prose question): *Aceitar a frase* (description: registo a aprovação como uma decisão própria (D-NNN) em `decisions.md`, com a impressão digital da frase) · *Editar a frase* (description: escreve a tua versão em "Other"; escrevo-a em `frame.md` e registo essa) · *Mais passagens de descoberta* (description: volto à etapa de ouvir e perguntar; `/round` corre de novo).

### 8. On validation, write the approval (this skill)

**Order matters**: the final sentence goes into `frame.md` FIRST, then the motor computes
its fingerprint, then the block is written. The fingerprint in `decisions.md` is therefore
always the fingerprint of a sentence that really is on file — never of the text typed into
the block (`pricing-marinha-pilot-1` holds an English sentence in `frame.md` and a
Portuguese one in `D-001`: that drift is what this ordering closes).

1. If the user edited the sentence, write it into `frame.md` under `## Single problem sentence`.
2. Run the motor (`--json`) and read `frame.sha256` — never compute a hash by hand.
3. Read the next free id: `max(D-NNN in decisions.md) + 1`, zero-padded to 3 digits. It is
   **not** always `D-001`; frame, solution and blueprint approvals share one counter.
4. Append to `<engagement>/decisions.md` the record contracted in
   `library/kernel/phases.md` → *Frame approval record*:

```markdown

## D-NNN — Frame agreed (F-NN)

- **Frame sentence**: <final agreed sentence, verbatim as written in frame.md>
- **Agreed in round**: F-<NN>
- **Frame sha256**: <frame.sha256 from the motor>
- **Supersedes**: <D-00x (frame F-0y) — the previous frame approval, if any | —>
- **Anchors**: <list of clause → SU ids>
- **Override used at /frame**: <reason or "—">
- **Validated by**: owner (<name/role>, via AskUserQuestion) | executor [ÂMBITO AUTORIZADO]
- **Timestamp**: <ISO-8601>
```

Never edit an existing block: `decisions.md` is append-only, and `Supersedes` in the new
block is the only pointer written (the motor derives the reverse one).

Then append a one-line summary to `council-log.md`: "F-<NN> — frame agreed (D-NNN)".

### 8a. On "more rounds"

Roll back `_state.json.phase` to `discovery` and leave `round` at the last completed Discovery round (`R-NN`). Tell the user:
```user-output
Voltámos a ouvir e perguntar (Discovery, ronda R-NN) — a frase do problema fica para depois.
A seguir: outra passagem das perspectivas pelo material → `/round`.
```

### 8b. On "edit: <new sentence>"

Overwrite the single-sentence line of `frame.md` with the user's edit (preserve all other sections), then proceed with step 8 using the edited sentence.

### 8c. Story

Append one narrative episode to `<engagement>/story.md` (`## Episódio <N> — <data> — o problema ganhou uma frase (frame)`): 4-8 frases na voz do sponsor, sem jargão de kernel, máx. 2 ids citados. Create the file with `# Story — <slug>` if missing (pre-v2.3 engagements).

### 9. Wrap-up output

```user-output
Frase do problema fixada e aprovada (D-NNN, passagem F-NN).
A seguir: comparar alternativas — aqui entra pela primeira vez a perspectiva tecnológica → `/options`; ou `/status` para ver onde estamos.
```

## Notes

- **Concurrency**: the 6 personas must launch in a single assistant message (one message with 6 parallel Task tool uses). Sequential launches defeat the cost envelope advantage described in `library/kernel/orchestration.md`.
- **One prompt template.** Every persona prompt is the same preamble with substitutions; the return
  schema inside it is owned by `chairman-synthesis`, its only consumer. Persona files carry identity,
  mandate and memory — nothing mechanical.
- **Only the chairman writes the SU.** The 6 personas have `tools: [Read, Grep, Glob]` and return their proposals as text — they cannot write even if they tried.
- **The survival block is a projection, not a second truth.** Semantic ownership of invariants, constraints, obligations and Unknowns stays in the SU; `frame.md` names ids. If the chairman notices a missing material item while framing, the SU row is written first and projected second (`chairman-synthesis` step 6). `/options` personas read the block; the Options blocking set remains the primary candidate-specific check.
- **Idempotence**: re-running `/frame` is allowed (produces F-02, F-03, …). The previous `frame.md` is overwritten; chairman-synthesis-F-<NN>.md from each round is preserved.
