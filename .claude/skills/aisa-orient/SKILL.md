---
name: aisa-orient
description: Entry without a command. Runs when a message describes a process, a problem or an intent to start — or asks for a result of a later step — and carries no slash command. Orients in business language (what will happen, the steps, the enquadramento interview) and proposes `/start`; or, when an engagement already exists, reorients like `/resume` and says what is missing before what was asked. Collects and proposes only — it never creates or writes files; `aisa-start` writes.
---

# aisa-orient

`CLAUDE.md` → *Entrada sem comando* says when this skill runs. The user is not a builder: everything they read here follows the column *Como se diz ao utilizador* of `library/kernel/glossary.md` — kernel term only between parentheses after the business phrase, ids likewise, commands literal in backticks. No vendor, product or platform is named: principle 1 holds before the Options phase, and orientation happens before any phase.

## Execution steps

1. **Situate.** Resolve the engagements root (`$AISA_ENGAGEMENTS_ROOT` or `projects/`); list the folders with `_state.json`. Decide which of three situations this is:
   - **A — arrancar**: no engagement, or the message clearly describes a new process or problem.
   - **B — reorientar**: an engagement já existe and the message is about it — it names the slug, or there is exactly one engagement and the message asks for a result (estimativa, ecrãs, alternativas, frase do problema, documentos) or for "where are we".
   - **C — perguntar**: it could be either (several engagements; a new process that resembles an existing slug). Ask via `AskUserQuestion` — options *Começar um projecto novo* · *Continuar `<slug>`* · *Só uma pergunta — não mexer em nada*; slug and phase go in each option's `description`. Never assume.

### A — arrancar

2. **Enquadramento do aisa em cinco linhas** — this shape, business language, no vendor:
   ```user-output
   O que vai acontecer: ouvir quem manda no processo, ler os ficheiros que já existem, fazer perguntas em passagens, chegar a uma frase do problema, comparar alternativas (incluindo não construir nada), escolher, desenhar os ecrãs, entregar os documentos.
   Quanto tempo de quem: do dono do processo, uma conversa agora e depois respostas curtas por passagem — cada pergunta diz se precisa de reunião ou se um email chega; de quem constrói, nada até à escolha.
   O que se espera de ti: dizer como o negócio funciona nas tuas palavras, responder ao que só tu sabes, validar a frase do problema, escolher entre alternativas, aprovar o desenho dos ecrãs.
   Os passos, pela ordem: ouvir e perguntar (`/round`) → responder (`/answer`) → ver onde estamos (`/status`) → fixar a frase do problema (`/frame`) → comparar alternativas (`/options`) → ensaiar e testar (`/simulate`, `/premortem`) → escolher (`/decide`) → desenhar os ecrãs (`/blueprint`) → entregar (`/render --all`). Não precisas de decorar nada: o fim de cada resposta diz o que vem a seguir.
   A seguir: começo por perceber como o negócio funciona — vêm aí algumas perguntas, uma de cada vez.
   ```
3. **Entrevista de enquadramento** (P-0 — **the same seven themes, same ids and same order** as `aisa-start` step 4d and `library/kernel/phases.md` → *Enquadramento (P-0)*, because that step will not ask again): one `AskUserQuestion` per theme, "Other" for free text, answer kept **verbatim**:

   | # | id | pergunta ao dono |
   |---|---|---|
   | T1 | `actors` | Quem faz parte disto — que papéis intervêm, e quem manda no processo? |
   | T2 | `trigger` | O que faz este processo começar, e com que frequência? |
   | T3 | `activities` | O que se faz, por ordem, e onde é que se decide alguma coisa? |
   | T4 | `outcomes` | O que sai no fim, para quem, e como se sabe que correu bem? |
   | T5 | `invariants` | O que tem de se manter sempre verdadeiro — as regras que ninguém pode quebrar? |
   | T6 | `failure_today` | O que corre mal hoje, e quanto custa quando corre mal? |
   | T7 | `change_requested` | O que é que o pedido quer mudar nisto? |

   **Right after T4**, one `AskUserQuestion`, in **every** engagement: *A saída deste processo é um preço, cotação, margem ou valorização?* — *Sim* / *Não*. **Never inferred** from the message. Only *Sim* opens the five pricing themes (`P1 sold_what_when` · `P2 price_fixing_moment` · `P3 cost_driver` · `P4 valuation_driver` · `P5 uncertainty_shape`), each its own question, before T5.

   Then the invariants read back from **T5** in the owner's words (one sentence each — they become `M-n`), who besides the owner can confirm facts about this process, and the funding question (*A decisão de avançar depende de aprovação orçamental de terceiros?* — Sim / Não).

   The user is already talking about the mechanism: **start from what the message said and ask only what it did not say** — a theme the message already answered is not asked again, and the answer it gave is carried verbatim. Never rephrase an answer, never infer an invariant, never turn a vendor the owner names into an invariant. Everything asked here is handed to `aisa-start`, which does **not** ask any of it again (step 4 there).
3b. **Ficheiros nomeados mas não entregues.** Read whatever source material the interview drew on (transcript, document, message) for a concrete artefact it names — a file, a report, a system, a spreadsheet someone was working from — that was not itself attached in this conversation. For each one, ask by name **before** the proposta de arranque, one `AskUserQuestion`: *"A entrevista fala de `<artefacto>` — tens esse ficheiro?"*, options *Vou arranjá-lo antes de começar* · *Ainda não tenho, começa sem ele* · *Não se aplica*. This is not the general "any files?" ask in step 4 — it is specific to what the source material itself already named, so the gap never gets discovered for the first time in a capture summary after the engagement exists. No named artefact found → skip silently.
4. **Proposta de arranque** — one `AskUserQuestion`: the **slug** proposed from what was said (kebab-case, the process name — `pricing-marinha`, not the client), the tipo de solução em vista only if the user declared one (otherwise *por decidir — não muda as primeiras etapas*; the pack default applies), and any remaining files to drop in `inputs/` (beyond what step 3b already settled). Options: *Arrancar com este nome* · *Arrancar com outro nome* · *Ainda não*. Confirmed → invoke the `aisa-start` skill with `<slug> [pack]` **and hand it everything collected verbatim** (literal request = the user's message, requester, the declaration, invariants, authorities, funding gate, and the step-3b answers on named artefacts); `aisa-start` writes the files and does not ask again what is already answered. Nothing is written before that call.

### B — reorientar

5. Invoke the `aisa-status` skill in its `/resume` shape (blocks 1, 2, 3 abbreviated, 7). Then map what the user asked for to the step that produces it and to what must exist before:

   | Pediu | Sai de | Precisa antes |
   |---|---|---|
   | estimativa, custo, prazo | os documentos finais (`/render estimate`) | a escolha (`/decide`), o desenho dos ecrãs aprovado (`/blueprint`), os resumos por tema (`/synthesize`) |
   | ecrãs, protótipo | o desenho dos ecrãs (`/blueprint`) | a escolha (`/decide`) |
   | alternativas, "o que podemos fazer" | as alternativas (`/options`) | a frase do problema (`/frame`) |
   | a frase do problema | `/frame` | passagens suficientes (`/round`) e as perguntas graves respondidas |
   | responder a algo | `/answer <id> "…"` | — |
   | "onde estamos" | `/status` | — |

   ```user-output
   Onde estamos: <etapa em palavras> (<fase · ronda>) — projecto `<slug>`.
   O que pediste: <em palavras> — sai da etapa «<etapa>»; antes disso falta: <o que falta, em palavras, e quem o fecha>.
   A seguir: <passo humano, se houver> → `/<comando certo>`.
   ```
   Never run the step the user asked for from here; this skill orients.

### C — perguntar

6. `AskUserQuestion` as in step 1. The answer routes to A or B; *Só uma pergunta* → answer it and stop.

## Hard rules

1. **Never creates or writes files.** No `_state.json`, no `enquadramento.md`, no folder — `aisa-start` writes, after the user confirms the proposal.
2. **No vendor, product or platform** in anything the user reads here, even when the user named one — it stays in their verbatim.
3. **Ambiguous → ask.** Between starting, continuing and asking, `AskUserQuestion`; never assume.
4. **No `AskUserQuestion` available** (subagent context) → say so and stop at the orientation; the enquadramento stays open, never inferred.
