---
name: aisa-start
description: Start a new aisa engagement. Captures the literal request + requester, scaffolds the engagement folder, and writes the initial _state.json (phase=discovery).
---

# aisa-start

## Usage

`/start <slug> [pack]`

- `<slug>`: kebab-case slug for the engagement (e.g., `galp-adv`).
- `[pack]`: pack id (default: `pp`). Must exist as `library/packs/<pack>/pack.yaml`.

## Execution steps

1. **Resolve the engagement root**:
   - If `$AISA_ENGAGEMENTS_ROOT` is set → `<root>/<slug>/`.
   - Else → `projects/<slug>/` (assumes a symlink/junction is configured, or local MVP testing).
2. If the folder already exists → stop with: "Engagement `<slug>` already exists. Use /resume." Do not overwrite.
3. **Validate the pack**: confirm `library/packs/<pack>/pack.yaml` exists. If not, list available packs and stop.
4. **Capture from the user** (interactive — ask, do not invent). **Invoked by `aisa-orient`** with the request, requester, enquadramento declaration, invariants, authorities, funding gate and named-artefact answers (step 3b there) already collected verbatim → **do not ask again**; carry that verbatim into steps 6 and 9b and ask only what is still missing.
   a. The literal request, verbatim, with no reformulation.
   b. The requester: name, role, authority level.
   c. Optional: documents to drop into `inputs/`.
   d. **Enquadramento — the business mechanism, declared by the process owner** (P-0, `library/kernel/phases.md` → *Enquadramento (P-0)*). Before any lens runs, the owner says in their own words how the business works at the point the request touches. **Seven themes, fixed order, one `AskUserQuestion` per theme**, "Other" for free text, answer kept **verbatim**. The ids are stable and become the anchors of `enquadramento.md`:

      | # | id | pergunta ao dono |
      |---|---|---|
      | T1 | `actors` | Quem faz parte disto — que papéis intervêm, e quem manda no processo? |
      | T2 | `trigger` | O que faz este processo começar, e com que frequência? |
      | T3 | `activities` | O que se faz, por ordem, e onde é que se decide alguma coisa? |
      | T4 | `outcomes` | O que sai no fim, para quem, e como se sabe que correu bem? |
      | T5 | `invariants` | O que tem de se manter sempre verdadeiro — as regras que ninguém pode quebrar? |
      | T6 | `failure_today` | O que corre mal hoje, e quanto custa quando corre mal? |
      | T7 | `change_requested` | O que é que o pedido quer mudar nisto? |

   d1. **Activation of the `pricing` set** — immediately after **T4**, **one** `AskUserQuestion`, asked in **every** engagement, whatever the process looks like:

      > *A saída deste processo é um preço, cotação, margem ou valorização?* — options *Sim* / *Não*

      **Never inferred** from the narrative, from the slug, or from what the request seems to be about: a process that mentions money is not a pricing process, and a pricing process that never says so still gets asked. **Only `Sim`** opens these five, each its own `AskUserQuestion`, verbatim, before T5:

      | id | pergunta ao dono |
      |---|---|
      | `P1 sold_what_when` | O que se vende, e quando? |
      | `P2 price_fixing_moment` | Quando é que o preço se fixa, e quando é que a venda acontece? |
      | `P3 cost_driver` | O que determina o custo? |
      | `P4 valuation_driver` | O que determina a valorização? |
      | `P5 uncertainty_shape` | De onde vem a incerteza, e como evolui no tempo? |

      `Não` → none of the five is asked, and `enquadramento.md` has no `## pricing` section. A pack may add themes of its own through `pack.yaml: enquadramento.extra_themes[]`; every pack declares it empty today.

      After the themes, and in this order: read the invariants back from **T5** (`M-n`, business language, one sentence each — the owner's words, never a rewrite), then ask who besides them has authority to confirm facts about this process (`library/kernel/states.md` → *Confirmed threshold*, rule 3).
   d2. **Ficheiros nomeados mas não entregues** — only when this skill was invoked directly (not via `aisa-orient`, which already did this at its step 3b). Read whatever source material the interview drew on for a concrete artefact it names — a file, a report, a system, a spreadsheet someone was working from — that was not attached in this conversation. For each one, ask by name before continuing: one `AskUserQuestion`, *"A entrevista fala de `<artefacto>` — tens esse ficheiro?"*, options *Vou arranjá-lo antes de começar* · *Ainda não tenho, começa sem ele* · *Não se aplica*. Do not let this surface for the first time in the `aisa-capture` summary (step 11) after the folder already exists. No named artefact found → skip silently.
   e. **Funding gate** (`AskUserQuestion`, one question): *"A decisão de avançar depende de aprovação orçamental de terceiros?"* — options *Sim* / *Não*. The answer is the owner's declaration, never inferred from authority text or from the SU. It becomes `context.json.funding_gate` (`true` / `false`); when the key is absent the lenses behave as `true`. The enquadramento is **not the request**: it is the invariant the request serves. Never infer an `M-n` from the literal request or from `_capture/` — record only what the human said. If the owner names a vendor, product or solution, it stays in the verbatim and does not become an `M-n`. Owner unavailable → the file says *"não declarado"* and the lenses work as before.
5. **Create the folder structure**:
   ```
   <slug>/
   ├── _state.json
   ├── context.json
   ├── enquadramento.md          (owner-declared business mechanism — step 9b)
   ├── shared-understanding.md   (skeleton — see below)
   ├── lens-outputs/             (empty)
   ├── council-log.md            (header only)
   ├── decisions.md              (empty header)
   ├── answers.md                (header only — filled by /answer)
   ├── inputs/                   (raw source material — any captured docs)
   └── _capture/                 (deterministic shared evidence generated from supported inputs — written by step 11; raw `inputs/` stays authoritative)
   ```
6. **Write `context.json`**:
   ```json
   {
     "engagement": "<slug>",
     "literal_request": "<verbatim>",
     "requester": { "name": "<name>", "role": "<role>", "authority": "<authority>" },
     "funding_gate": true | false,
     "inputs": ["<filenames in inputs/>"],
     "captured": "<ISO-8601 timestamp>"
   }
   ```
7. **Write `_state.json` atomically** (write `_state.json.tmp`, then rename over `_state.json` — `Move-Item -Force` on Windows, `mv` on Unix):
   ```json
   {
     "engagement": "<slug>",
     "pack": "<pack>",
     "phase": "discovery",
     "round": "R-00",
     "round_in_progress": "",
     "aisa_version": "0.1.0",
     "created": "<ISO-8601 timestamp>"
   }
   ```
   (`round` seeds at `R-00` — no round has **completed** yet. The first `/round` opens `R-01` and closes it when all six perspectives have stamped it (or on `/round --close`). `round_in_progress` seeds empty — no round open; `/round` fills it while a passagem is in flight and clears it on close (`library/kernel/phases.md` → *Rounds — in progress vs completed*).)
8. **Write the `shared-understanding.md` skeleton** (the 5 state sections with their column headers, per `library/kernel/states.md`; `verificado_em`/`validade` per its *Epistemic half-lives* section; `custo`/`swing` per its *Question economics* section; the `Saúde epistémica` header line stays `—` here — `/status` fills it):
   ```markdown
   # Shared Understanding — <slug>

   > Engagement: <name>
   > Sponsor: <requester name>
   > Iniciado: <date>
   > Fase actual: Discovery
   > Última actualização: <timestamp>
   > Saúde epistémica: —

   ## Confirmed

   | id | lens | claim | evidência | verificado_em | validade | ronda |
   |----|------|-------|-----------|---------------|----------|-------|

   ## Assumed

   | id | lens | claim | base da assumption | verificado_em | validade | ronda |
   |----|------|-------|--------------------|---------------|----------|-------|

   ## Unknown

   | id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
   |----|------|----------|---------------|-------------|-------|-------|-------|

   ## Conflicted

   | id | lens | conflito | partes | criticidade | ronda |
   |----|------|----------|--------|-------------|-------|

   ## Risky

   | id | lens | risco | impacto | mitigação proposta | ronda |
   |----|------|-------|---------|--------------------|-------|
   ```
9. Write `council-log.md` with a header (`# Council Log — <slug>`), `decisions.md` with a header (`# Decisions — <slug>`), `answers.md` with a header (`# Answers — <slug>`), and `story.md` with `# Story — <slug>` + **Episódio 1** (o pedido: quem pediu, o quê, porquê — 4-6 frases na voz do sponsor).
9b. **Write `enquadramento.md` and the `R-00` rows** from step 4d. File: header (owner, date, executor, literal request), then **one section per theme, in order and with the stable anchor** — `## T1 · actors`, `## T2 · trigger`, `## T3 · activities`, `## T4 · outcomes`, `## T5 · invariants`, `## T6 · failure_today`, `## T7 · change_requested` — each carrying the owner's answer **verbatim**. **`## pricing` exists only when the owner answered *Sim* at step d1**, carries the marker `<!-- INTAKE-SET: pricing -->` on its first line, and holds the five answers (`P1`..`P5`) verbatim; answered *Não*, the section is absent — never present and empty. Then a table `id · invariante · o que orienta · fonte` built from **T5 verbatim** (one `M-n` per declared sentence, nem mais nem menos), the named authorities (or *"Ninguém — só o dono"*), and the rules block (hypothesis of the owner; `/frame` confirms or corrects each `M-n`; nothing inferred; no vendor). Each `M-n` then enters the SU as `Confirmed`: `lens = enquadramento`, `ronda = R-00`, evidência = `declaração do dono do processo, <date> — enquadramento.md#M-n`, `verificado_em` = today, `validade = organizacional`. Log one line in `council-log.md` (`R-00 — enquadramento: M-1..M-n declarados pelo dono`). *"Não declarado"* → write the file with that line and no rows. Reference copy of the **older** shape (no `Tn` sections, written before this contract): `projects/pricing-marinha-pilot-3/enquadramento.md` — it is read as it is and never rewritten; the presence of the sections is what distinguishes the shapes, never a date or a version number.
9c. **O engagement nasce com grafo.** Correr, uma vez, depois de a pasta existir e antes de qualquer outro comando aisa tocar no engagement:

    ```
    python library/kernel/tools/migrate.py init --engagement <slug>
    ```

    Publica um grafo vazio e válido pelo coordenador (recibo em `_ops/receipts/graph-init.json`). Idempotente: correr outra vez devolve `already`, e um grafo já existente nunca é substituído. **Não é opcional.** Desde a decisão de tornar o grafo obrigatório (P7.5 §2), ausência de grafo bloqueia — e um engagement acabado de criar não tem nada que migrar, por isso ou nasce migrado ou fica bloqueado à nascença por trabalho que não existe. Falha aqui → parar e reportar o erro tal como veio; não continuar para o passo 10 com o engagement por nascer.

10. Output (business language — `CLAUDE.md` → *Duas línguas*; kernel labels only between parentheses):
    ```user-output
    Projecto `<slug>` criado — tipo de solução em vista: <em palavras> (pack `<pack>`).
    Etapa: ouvir, ler e perguntar (Discovery).
    Como o negócio funciona, dito pelo dono: <n regras declaradas (M-1..M-n) | não declarado — cada pergunta terá de justificar-se sozinha>.
    Ficheiros para ler: <n em inputs/ | nenhum>.
    A seguir: primeira passagem das perspectivas pelo material → `/round` (ou uma perspectiva de cada vez: `/round business`).
    ```
11. **Process capture**: if `inputs/` contains any file → invoke the `aisa-capture` skill and report its summary. It owns the supported-format list (structured `.xlsx`/`.xlsm` → L1/L3/L2; capture-lite `.docx`/`.pdf`/`.vtt` → LT) and always writes `_capture/evidence-index.md`, the shared evidence surface for the engagement. Empty `inputs/` → skip silently.
