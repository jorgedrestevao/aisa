---
name: aisa-options
description: Transition Framing → Options. Checks Framing's exit gate, flips _state.json to phase=options/round=O-01, launches 7 council personas in parallel via the Task tool (council-independent mode — adds solution-architect for the first time), then invokes chairman-synthesis to write options.md and synthesised Shared Understanding rows.
---

# aisa-options

## Usage

`/options [--override "<reason>"] [--reopen "<justificação>"]`

- No argument: runs the soft gate check; if any criterion is red and no override is provided, stop with a clear summary and ask the user before proceeding.
- `--override "<reason>"`: bypass the soft gate. The reason is logged in `decisions.md`.

## Phase model

- **From**: `phase: framing`.
- **To**: `phase: options`, `round: O-01` (subsequent options rounds become `O-02`, `O-03`, …).
- **Mode**: `council-independent` with **7** personas (the 6 Discovery personas + `solution-architect`). The solution-architect activates here for the first time in the engagement — this is where vendor/product naming becomes allowed (via `lens-technology`).

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/council-log.md`.
- `<engagement>/frame.md` (the agreed problem sentence from Framing).
- `<engagement>/lens-outputs/*.md` (incl. any prior chairman-synthesis logs).
- `library/kernel/phases.md` (Options entry criteria).
- `<engagement>/_capture/evidence-index.md` (the shared evidence surface handed to every persona).
- `library/packs/<pack>/pack.yaml` — `lenses_config.<lens>.extra_signals` as attention cues for the six
  Discovery personas. `decision-tree.md` and `domain-knowledge/*.md` are **not** read here: they are
  `solution-architect`'s to pull, selectively, for the option it is actually evaluating
  (`library/kernel/orchestration.md` → *Pack context*).
- `.claude/skills/chairman-synthesis/SKILL.md` → *Council launch preamble* (the persona prompt is built from it).

## Outputs (written, via chairman-synthesis except where noted)

- `<engagement>/_state.json` — atomic write (this skill).
- `<engagement>/options.md` (chairman-synthesis).
- New rows in `<engagement>/shared-understanding.md` (chairman-synthesis).
- `<engagement>/lens-outputs/chairman-synthesis-O-<NN>.md` (chairman-synthesis).
- `<engagement>/council-log.md` summary lines (this skill + chairman-synthesis).

## Execution steps

### 1. Pre-flight

1. Resolve the engagement root and read `_state.json`. Run the motor once —
   `python library/kernel/tools/dashboard.py --engagement <slug> --json <tmp>/model.json --quiet` —
   and read `frame`, `reopen` and `options_history` from it. Then, by phase:
   - `framing` or `options` → normal path (a second `options` run is a re-run);
   - **`decision` → reopening the alternatives** (`library/kernel/phases.md` → *Transition rules*).
     Allowed when `reopen.verdict == "REABRIR"` (the latest `/revisit` recommended it) **or**
     the user passed `--reopen "<justificação>"`. Neither → stop:
     ```user-output
     Já há uma decisão registada (D-00x). Voltar a pôr as alternativas na mesa exige uma condição de revisão que tenha disparado, ou uma razão tua.
     A seguir: `/revisit TW-n` para ver o que mudou → ou `/options --reopen "<a tua razão>"` para reabrir na mesma.
     ```
     `--reopen` without a justification stops the same way: the reason is the record.
     When `reopen.decision` names a decision that is not the one in force
     (`status.tripwires.source_decision`), stop and say which is the current one.
   - any other phase → stop with: "/options transitions Framing → Options; current phase is `<phase>`. Use /frame first."
2. **Is the sentence on file the approved one?** Read `frame.verdict` (`library/kernel/phases.md`
   → *Frame approval record*). This replaces the old existence check for a `D-001` line, which
   could not tell an approval of THIS sentence from an approval of a previous one (F05):

   | `frame.verdict` | What it means | What this skill does |
   |---|---|---|
   | `match` | approved, in the current framing round | continue |
   | `match-other-round` | same sentence, approved in an earlier round (only the anchors were redone) | continue; say so in one line |
   | `none` | there is a sentence, and nobody approved it | ask (below) |
   | `mismatch` | the sentence changed since the last approval | ask (below), showing **both** sentences |
   | `legacy` | the approval predates the fingerprint rule — it cannot be verified | ask (below) |
   | `no-frame` | there is no sentence yet | stop: *"Ainda não há uma frase do problema. A seguir: → `/frame`."* |

   For `none` / `mismatch` / `legacy`, show the current sentence (and, for `mismatch`, the
   approved one under it) and ask via `AskUserQuestion` — never a prose question:
   *Aprovar a frase actual* (description: escrevo a aprovação como decisão própria (D-NNN) com a impressão digital da frase; em `mismatch`/`legacy` leva `Supersedes: D-00x`) ·
   *Refazer a frase* (description: volto ao passo da frase do problema — `/frame`) ·
   *Avançar sem aprovação* (description: escreve a razão em "Other"; fica registada e a frase continua por aprovar).
   Approving here writes exactly the record of `phases.md` → *Frame approval record*, by the
   same order as `aisa-frame` step 8 (sentence in `frame.md` first, fingerprint from the motor,
   then the block). "Avançar sem aprovação" writes `## O-NN — gate override (frame <verdict>) — <ts>`
   with the justification into `council-log.md` and **never fabricates an approval**; `/status`
   keeps showing the sentence as unapproved.
3. Read `library/kernel/phases.md` (Options entry criteria).

### 2. Soft gate check

**The mechanical verdict is in `<engagement>/gate-log.md`** (id `G-framing-options-...`), written by `phase-gate-check.py` before this skill loaded. Repeat it and add the judgement; a criterion recorded as `n/a` is not OK.


- Frame approval covers the current sentence (`frame.verdict` ∈ {`match`, `match-other-round`}) → checked in pre-flight 2; an override there is this criterion's override.
- Sponsor confirmation captured in the approval record (`Validated by`).

If a soft criterion is red and no `--override` was passed → stop with a one-line-per-criterion summary and ask the user. If `--override` is set, log the reason — it goes into `decisions.md` alongside D-NNN.

### 3. Flip state to Options (atomic)

1. Compute the options round **from history, never from `_state.json` alone**: use
   `options_history.next` from the motor (highest of `lens-outputs/chairman-synthesis-O-NN.md`,
   the `## O-NN` headings of `council-log.md`, and the state when it holds an `O-`). After a
   decision the state holds `D-01`, and deriving `O-01` from it would overwrite the very round
   that produced the decision being revisited (F07).
2. Update `_state.json`: `phase = options`, `round = <options_history.next>`, `round_in_progress = ""`
   (a Discovery passagem left open never crosses a phase boundary). Atomic write
   (`_state.json.tmp` → `Move-Item -Force` / `mv`).
2b. **When this is a reopening**, also append to `council-log.md`:
   `## O-NN — reabertura da decisão D-00x — <ISO ts>` with what triggered it
   (`_simulation/<revisit file>`, `TW-n`) or the `--reopen` justification, and the line
   `_state.json → phase=options, round=O-NN (era decision/D-NN)`. The previous decision is
   **not touched**: `/decide` will write the new block with `Supersedes: D-00x`. Append one
   episode to `story.md` ("voltámos a pôr as alternativas na mesa — <porquê>").
3. Update the SU header `Fase actual: Options` and `Última actualização: <ISO timestamp>`.

### 4. Compose thematic Shared Understanding excerpts

Same slicing as `aisa-frame` for the first 6 personas — including the mandatory "Resoluções já fechadas (não re-litigar)" block in every excerpt. Add a 7th excerpt for `solution-architect`:

| Persona | Slice |
|---|---|
| solution-architect | The **full** Shared Understanding (the architect needs the cross-lens picture) + the pack metadata files listed in *Inputs* + `frame.md` |

Each excerpt is saved transiently under `<engagement>/lens-outputs/_council-prep/O-<NN>-<persona>.md` for the audit trail.

### 4b. Assemble the common council context

Identical to `aisa-frame` step 4b — shared evidence index, pack attention cues, memory pointer — with
one difference: **`solution-architect` receives no Discovery `extra_signals`.** Its pack access is
pull-based and its own (see step 5). Bookkeeping only; the orchestrator decides nothing about meaning.

### 5. Launch the 7 personas in parallel via the Task tool

Send **one assistant message with 7 Task tool calls** so they execute concurrently. Each Task call:

- `subagent_type`: persona name (`business-analyst`, `operations-lead`, `user-advocate`, `data-steward`, `compliance-officer`, `cfo-lens`, `solution-architect`).
- `description`: e.g., "Options O-01 — architecture proposal".
- `prompt`: the **council launch preamble**, authored once in `.claude/skills/chairman-synthesis/SKILL.md`
  → *Council launch preamble*, used verbatim with these substitutions:
  - `<phase>` = `Options` · `<round>` = `O-<NN>` · `<slug>`, `<pack>`, `<engagement>` = this engagement
  - `<persona>` = the persona being launched; its `_council-prep` excerpt path is `O-<NN>-<persona>.md`
  - keep the `frame.md` read — Options personas reason against the agreed problem
  - shared evidence · pack cues · memory pointer = whatever step 4b resolved for that persona
  - technology-neutrality selector: `[Options, the six Discovery personas]` for the six;
    `[Options, solution-architect]` for the architect

  For `solution-architect` only, append one line naming the resolved pack root:

  ```
  Your pack access is pull-based and Options-only (see your agent file → *Lens binding*). The active
  pack lives at `library/packs/<pack>/`.
  ```

  That is the whole architect addition. Its option-set mandate is in its agent file; do not restate it
  here, and never place `decision-tree.md` or `domain-knowledge/` contents in the prompt — the
  architect pulls what it needs.

  The preamble is otherwise the whole prompt. Do not restate its mechanics, and do not tell a persona
  to read its lens `SKILL.md` (`library/kernel/orchestration.md` → *Persona boundary*).

Wait for all 7 to return. Collect their tool results verbatim.

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

Invoke `chairman-synthesis` with the 7 persona outputs and phase = `options`, round = `O-<NN>`. The chairman writes `options.md` (≥3 options) and the new SU rows.

Four contract checks before reporting to the user, all owned by `chairman-synthesis`:

1. **Every option names its technology**, and a platform option names its **form** — surface and store, one option per form (`decision-tree.md` §14.1; for `pp`, `decision-model/alternatives-register.md` §1.2). A round whose architect returned a platform class with no form-level candidate is reported as such in `Summary` and raised as an open question — a form is never invented to fill the column.
2. **Every option carries an order of magnitude with its source marker**, or `ORDER OF MAGNITUDE UNAVAILABLE — <what is missing>`. A band with no source is invented; a blank cell is a contract breach.
3. **The round closes with the recommendation** — the option, what separates it from its siblings, what it rests on, what would flip it. Where the terminal is *decision blocked* or *multiple defensible options*, `no recommendation — <what would produce one>`. The recommendation is the aisa's; the choice is the owner's, at `/decide`.
4. **The artefact is within budget** (~1 500 words of prose, ≤120 per option). The full field set, the concern coverage and the `DO-NOTHING` / `PROCESS-CHANGE` class coverage live in `lens-outputs/chairman-synthesis-O-<NN>.md`.

### 7. Present options to the user

Output to the user (business language — `CLAUDE.md` → *Duas línguas*; kernel labels and ids only between parentheses). Each line carries the option class in words (não construir nada · mudar o processo · construir …), **the technology named** — for an option built on the pack's platform, the *form*: the kind of application **and** where the data lives, in product names, because Options is the phase where that is said out loud — the effort driver and the reversibility. Same facts as the table in `options.md`, nothing added:

```user-output
Alternativas na mesa (passagem O-NN): <N>.

  - <nome> — <tipo: não construir nada · mudar o processo · construir …> — <tecnologia: <produto> sobre <onde os dados vivem> | sem tecnologia | por avaliar> — <ordem de grandeza: <banda>, <de onde vem: do ensaio · do modelo do pacote · por semelhança com <caso>> | ainda sem base: falta <o que falta>>, fácil de reverter: <pouco | médio | muito> (O-001)
  - <nome> — … (O-002)

O que o aisa recomenda, e porquê: <alternativa> — <o que a separa das irmãs, numa frase> (O-nnn). Assenta em: <pressupostos curtos> (<ids>). Mudava de ideias se: <o que a inverteria> (<ids>).
  <ou, quando não há base para recomendar: «Sem recomendação por agora: <o que falta para a haver>.»>
  A escolha é tua — isto é o parecer, não a decisão.

Alternativa que só passa se uma regra mudar: <nenhuma | <alternativa> — regra: <qual>, quem a pode mudar: <papel>, estado: <não pedido | pedido | recusado> (O-nnn)>
Perguntas em aberto que ainda pesam nas alternativas: <nenhuma | <pergunta curta> (U-nnn) …>
Onde as fontes ainda se contradizem: <nenhuma | <contradição curta> (X-nnn) …>

A seguir: lê `options.md`; ensaiar cada alternativa → `/simulate`; escrever o obituário do projecto → `/premortem`; escolher → `/decide`. Faltou uma classe de alternativa? → `/options` outra vez (sai a passagem seguinte).
```

### 7b. Story

Append one narrative episode to `<engagement>/story.md` (`## Episódio <N> — <data> — as opções na mesa`): 4-8 frases na voz do sponsor, sem jargão de kernel, máx. 2 ids citados. Create the file with `# Story — <slug>` if missing (pre-v2.3 engagements).

### 8. Wrap-up output

```user-output
Alternativas fechadas (passagem O-NN) — <N> na mesa, <n> sem construir nada.
A seguir: ensaiar antes de escolher → `/simulate`; o obituário do projecto → `/premortem`; escolher → `/decide`.
```

## Notes

- **Concurrency**: the 7 personas must launch in a single assistant message (one message with 7 parallel Task tool uses), mirroring `aisa-frame`.
- **One prompt template.** Every persona prompt is the same preamble with substitutions (plus the two
  architect-only lines); the return schema inside it is owned by `chairman-synthesis`, its only consumer.
- **Domain knowledge is pulled, never preloaded.** The orchestrator does not read `decision-tree.md` or
  `domain-knowledge/` and never puts their contents in a prompt — pointers only.
- **solution-architect is the lone vendor-naming surface.** The other 6 personas keep returning *needs and constraints*, never vendor choices, per `.claude/rules/no-tech-mention-before-options.md` (they run isolated and never see the solution-architect's output in-flight). The chairman, when synthesising, may name a vendor only where it is anchored to a solution-architect output; cross-lens rows not pinned to such an anchor stay technology-neutral.
- **Idempotence**: re-running `/options` produces O-02, O-03, …. The previous `options.md` is overwritten; each round's `chairman-synthesis-O-<NN>.md` is preserved.
