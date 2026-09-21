---
name: aisa-status
description: Answer "what is missing for the next step?" for the current engagement — next milestone, tripwire verdicts, the material blockers with consequence / owner / closure criterion, one next action, the meeting agenda, SU counts and epistemic health, and the derived `Read to resume` set. Reads the deterministic model from dashboard.py --json and adds only what needs judgement. With --check, validates the aisa install.
---

# aisa-status

## Usage

`/status [--check]`

- No argument: the full view for the current engagement — the seven output blocks in step 10.
- `--check`: validates the aisa install (paths, kernel, pack, hooks, tools); no engagement needed.
- `/resume` invokes this skill and shows four of those blocks only — the three opening lines, the alert (when there is one), *O que falta* abbreviated, and `Read to resume`. Reorient, never re-analyse.
- Language: `CLAUDE.md` → *Duas línguas*. Everything printed follows the column *Como se diz ao utilizador* of `library/kernel/glossary.md`; kernel labels and ids only between parentheses, after the business phrase. The files (`shared-understanding.md` header included) keep the kernel vocabulary.

## Division of labour (normative)

**The motor carries the facts; this skill carries the judgement.** `library/kernel/tools/dashboard.py --json` is the single source for every count, date, version, citation and reference below. This skill never recounts SU rows, never re-derives expiry, never re-reads the blueprint to find structural choices — doing so is how the two drifted apart (plan §1). What the skill adds, and only the skill may add:

- the **tripwire verdict** (disparou / em vigilância / não avaliável nesta fase);
- the **consequence** of each blocker, in words, anchored to the reference the model gives;
- the **question formulation** from the pack's question bank, and the **teach-back** grouping;
- the **priority within "A revalidar"** by material dependency;
- the **prose** of the next action.

Nothing here resolves a row, executes a proof, changes a phase or approves anything. The only write is the SU health header (step 3).

## Execution steps (no argument)

1. **Resolve the engagement.** Scan the engagements root (`$AISA_ENGAGEMENTS_ROOT` or `projects/`) for folders with `_state.json`; if more than one and none is named, ask which.

2. **Run the motor and read the model.** From the repo root:
   ```
   python library/kernel/tools/dashboard.py --engagement <slug> --json <tmp>/aisa-status-<slug>.json --quiet --force
   ```
   `<tmp>` is the OS temp dir — **never inside the engagement**. The run also refreshes `<engagement>/dashboard.html`, which is the same output the `on-su-change.py` hook produces; that is expected. Read the JSON. Use `model.status.*` for everything below; `model.health`, `model.agenda`, `model.revalidate`, `model.su` for the counts.
   **Motor failed or JSON unreadable → stop and say so**: `verificação incompleta — motor falhou: <first stderr line>`. Do not recompute by hand; do not present partial counts as the view.
   Every `model.diagnostics` entry of level `warn`/`error` is surfaced verbatim in the **Shared Understanding** block.

3. **Write the SU health header** (the one sanctioned write). From `model.health`: update `> Saúde epistémica: NN% (X expiradas) — <today>` in `shared-understanding.md` (create the line if the SU predates it). Half-lives and the compatibility rule for pre-v2.2 SUs are applied by the motor per `library/kernel/states.md` → *Epistemic half-lives*; never migrate the SU.

4. **Tripwire verdicts** (`status.tripwires`). The motor read them from the **solution decision** (`source_decision`, kind `solution`), never from a later blueprint approval, and gives per tripwire `cited_ids`, `resolvable_ids`, `unresolvable_ids`, `evidence` and `status ∈ {watch, no-evidence}`. Neither value is a verdict — `verdict_owner: "skill"`. For each tripwire decide **one** of:
   - **Disparou** — only when a row in `evidence` *satisfies the condition as written*, not merely touches its subject. State the row and the clause it satisfies. → alert first in the output + `/revisit TW-n`.
   - **Em vigilância** — `status: watch` and the condition is not yet met: name the open Critical/expired rows the tripwire depends on.
   - **Não avaliável nesta fase** — the condition measures something with no source in the SU at this point (build effort, post-handoff volume, production metric). `no-evidence` from the motor is the *trigger to ask this question*, never a green light. Say what would make it evaluable.
   `source_decision` empty → `Tripwires: verificação incompleta — sem decisão-solução em decisions.md`. Never print `Tripwires: OK` unless every tripwire is evaluable and none is disparou/em vigilância.
   **Only declared tripwires exist.** `unlabelled_notes` holds bullets recorded under the same heading that do not declare a `TW-<n>` id — in `pricing-marinha` D-002 that note says the other premortem candidates were considered and **not** adopted. Never treat one as a tripwire; mention them, if at all, as one line: *a decisão registou N notas sob a rubrica que não são tripwires formais*.

5. **"O que falta para avançar"** — from `status.milestone` and `status.items`.
   `items` is one entry per SU id (the grouping key; plan §3), ordered blockers-of-approval → criticidade → swing. **Within a tie, order by impact on the technical decision** (P-26): first the items sitting on one of the seven axes that may block a decision (`library/packs/<pack>/decision-tree.md` §6.1), then the ones that move one of the eight admission axes (`library/kernel/states.md` → *Admission of a question*), then the rest. This is a reading order, not a new state and not a re-ranking of the motor's `items`: the motor's order is the spine, this breaks its ties. It is the whole material set, so read it in three tiers and never collapse them:
   - **Develop about three**: `milestone.blocking` first, then the remaining Critical ones.
   - **"Também materiais"**: one line each (id — consequence) for every *other* item that is Critical **or** carries an `obligations` entry. All of them — **never hide a blocker to fit**.
   - **Risk context**: a `Risky` item with no `obligations` is not a thing that is missing; it goes to the risk line in the **Shared Understanding** block. A `cited_by` naming `decisions.md` makes this *more* true, not less — the decision recorded the risk as accepted (label **"pode seguir com risco registado"**), which is the opposite of a blocker. Only an obligation moves a `Risky` row into "o que falta".
   Each developed item shows the fields below, each from a named source in the model; a field the model does not carry is shown as absent — **never filled by inference**:

   | Field | From | If absent |
   |---|---|---|
   | Tema + referência | `id`, `claim`; `obligations[].source` (blueprint path + key) | — |
   | Bloqueia / Afeta | `blocks_approval` + `obligations[].rule` (cites `blueprint-contract.md` regra 5); `cited_by` (`TW-n (D-NNN)`, `options.md`, `decisions.md`) | "sem ligação registada a decisão/opção/entrega" |
   | Falta | `obligations[].what` (structural choice, proof obligation), else the `claim` (the open question itself) | — |
   | Quem | `owner.role` and `owner.source` when either is non-empty — the prefix the row carries (`library/kernel/states.md` → *The form of `quem responde`*); otherwise `owner.humans`, which is what rows written before the prefix carry. `obligations[].owner` likewise for the proof executor (may differ from who answers). Show it as what the row carries — a **role** (`Operações`, `dono dos dados`) or a **source to consult** (a system, a document, a team) — never as a demand for a person's identity: the answer is owed by whoever holds the role, and no name is a precondition for the next step (P-21 / P-26; the field's mechanics come with block F) | **"por atribuir"** — when the row names neither role nor source, and also when only a council persona was named (`owner.personas`), a persona is a lens, not somebody to ask |
   | Fecha quando | `closes_when` (`would_be_settled_by` / proof `method`) | `closes_when_substitute` = the swing phrase, labelled **"critério formal por definir"** |
   | Próxima ação | the command that records the outcome, after the human step | — |

   Labels are descriptions with scope, not new states (the five SU states keep authority):
   - **Portão da fase** (`status.gates`, e a última linha de `gate-log.md`) — o veredicto mecânico da transição que se segue, com a cobertura declarada (*n de m por código*). Um critério `juizo` ou `n/a` reporta-se como tal, **nunca** como cumprido.
   - **Avisos da síntese** (`status.synthesis_checks`) — recalculados na consulta; `stale_record` diz que a linha registada foi calculada contra outro texto ou outras fontes, e por isso não vale como veredicto.
   - **Conferência do desenho** (`status.coverage`) — the fourth dimension, beside blueprint, synthesis and render, and the one that must never be merged with them. It carries **four separate answers** (`readiness.structure` · `readiness.coverage` · `readiness.approval` · `readiness.e2e`) and the model keeps them apart on purpose: a version whose structure is `valid` can have dropped a requirement the SU already carried, a `complete` coverage is not an approval, and an approval is not a proof that the solution works. Report them as four, never as one verdict. `present: false` → *ainda não foi conferido* (`not_evaluated`), which is **neither a pass nor a failure and revokes no approval on file** (`coverage-contract.md` §10) — never print it as "sem lacunas" and never as "reprovado". `readiness.coverage: stale` → the sources, the decision or the version moved after the review; say **what moved** (`stages.<etapa>.diagnostics`) and that it must be redone — never that the earlier conclusion became false. `approve_eligible: true` means the version may be **put** to the business, never that the business approved; `blockers` is what must close first. `engine != "ok"` or a stage with `error` → *verificação incompleta*, with the reason, never zero gaps. `limitations` (sources with no extractor, capture limits) are shown as limitations, never converted into coverage. `julgamento` says what the block does and does not prove; read it before reporting.
   - **Estrutura do desenho** (`blueprint.versions[].valid`, `blueprint.approved_valid`, `issue_codes`) — a version with `valid: false` cannot be approved and an approval over it is not consumable (`blueprint-contract.md` → *Validação estrutural*). Report it next to the structural choices: *o desenho dos ecrãs, versão NN, falha a verificação de estrutura (<N> falhas: códigos entre parênteses) — não pode ser aprovado / a aprovação registada não vale para entregar*; fix = refazer o desenho → `/blueprint`. A `readable: false` version is reported as ilegível, never as OK.
   - **Bloqueia aprovação/entrega** — an explicit contract rule; cite it (regra 5: a structural open choice blocks *approval* of the version, never its *production*).
   - **Resolver antes de decidir** — a material gap or a recorded condition; say whether it is a warning or a blocker recorded in Options.
   - **Pode seguir com risco registado** — only where the decision and contracts allow; cite the acceptance.
   - **Não aplicável** — outside the authorised outcome/scope; not a failure (`render-contract.md` §Applicability).
   A pending proof obligation blocks only what its recorded obligation says it blocks. Saúde epistémica 100% means evidence within validity — it never means readiness.

6. **Próxima ação** — one. From `milestone.text` / `milestone.command`, written as: the human step first when one is needed (who does what), then the command that records it, with placeholders only where the answer does not exist yet (`/answer U-032 "<resultado real>" --source "<fonte>"`). Placeholder commands are models for use after the human step — this skill never runs them. Where the milestone is an approval blocked by structural choices, say explicitly: *a resposta resolve o facto; a aprovação exige fechar a escolha estrutural* (`aisa-answer` 4b, fact ≠ fit).
   Phase language: in Discovery and Framing no vendor, product or platform is named — the milestone table and the items carry none; pack knowledge enters through the pack in the phases that allow it.

7. **Agenda** — from `model.agenda` (`reuniao` / `outro_canal` / `nao_gastar`, ordered decisivo → dimensionante). Each agenda line **points to its item** in **O que falta para avançar** when the id is there, instead of repeating the explanation.
   a. **Formulate the questions** — the one place in aisa that consults the pack's question bank. Resolve `_state.json.pack` → `library/packs/<pack>/pack.yaml` → `question_bank` and read that file. Use it to (i) phrase each agenda item as a question a human can actually answer, instead of echoing the terse `pergunta` cell, and (ii) add a probe (`P-<LENS>-NN`) **only** where the SU shows its stated trigger observed. The same consult may phrase the question that would resolve a material `Conflicted` or `Risky` row, or close an evidence gap `_capture/evidence-index.md` reports (`failed`/`skipped`/`empty`).
      **Selective, never exhaustive.** Do not enumerate the bank, do not ask every core question, do not produce one question per Unknown, and do not treat the bank as coverage to satisfy — *reason first, formulate questions second*. Prioritize qualitatively with the metadata the rows already carry (`criticidade`, `custo`, `swing`, state): ask the smallest number of questions that could materially improve the decision. No scoring formula, no ranking engine.
      **Degrade gracefully**: no `pack` key, no `question_bank` key, or the file missing/unreadable → say so in one line and build the agenda from the SU rows alone, exactly as before. The bank is optional; the agenda is not.
   b. **Process teach-back (materiality-triggered, never mandatory).** When `_capture/process-model.md` §4 carries a material `HYPOTHESIS` or `UNKNOWN` about an output family, a transformation, a consumer, a business invariant or the process shape — or an adopted Critical `PM-U` is still an open `Unknown` — group the related open Unknowns into **one** `reuniao` agenda item: *"Teach-back do processo — é assim que entendemos que funciona (<synopsis lines>); o que está materialmente errado ou em falta?"*, listing every id it covers (`U-101, U-102, U-103`). One conversation, many questions: each underlying Unknown keeps its own identity and closure criterion and transitions independently through `/answer <id>`; the meeting never collapses them into one "process confirmed" row. An engagement whose synopsis carries no material hypothesis gets no teach-back item.
   c. **Não gastes tempo com** — every `cosmético`, listed explicitly; never promoted to priority work.
   d. **Degraded agenda.** `model.su.schema_flavour == "legacy"` means the SU predates the `custo`/`swing` columns, so every row read as `custo: email` / `swing: dimensionante` **by default, not by judgement** — the meeting bucket comes out empty and nothing is cosmético. Say that in one line instead of presenting the channels as decisions, and do not invent a channel for a row. Same for an item whose `closes_when_source` says *sem swing na SU*: print "critério por definir", never a blank.

8. **Contagens e validade** — from `model.su.sections`, `model.health`, `model.revalidate`. Rows with a `resolved →` marker are reported as resolved, never as open. **A revalidar**: the motor gives the expired rows and the re-question (`"Ainda é verdade que <claim>? Verificado pela última vez em <data>."`). Order them by **material dependency first** — an expired row cited by the solution decision, the current blueprint (`su_refs`), the chosen option or a tripwire outranks an older one nobody depends on — age as tie-break. Show the total and at most five in detail. Expired ≠ false: never state the fact changed.
   Also here, **read, never recounted**: **convergência** — `round_delta`: for `_state.json.round`, `criadas` · `fechadas` · `abertas` · `critical_abertas`, and the label `sem convergência` when the round's `criadas > fechadas` (visible, never a gate; `library/kernel/phases.md` Discovery exit criteria). `round_delta.indeterminadas` non-empty → say how many closures the motor could not date, never estimate them. **Factos sem prova localizável** — `confirmed_locator`: the count and the ids of `sem_locator` + `alvo_ausente` (`library/kernel/states.md` → *Confirmed threshold*), and the `excepcao_literal_request` ids as an accepted exception, not a gap. It is a presence check: never say the fact is false, say the evidence has no anchor that opens. **Every deterministic block publishes `julgamento`** — read it before reporting an empty list: empty means *nothing missing that this regex can see*, never *approved*, and saying "0 problems" where the motor only checked presence is the failure this field exists to prevent. `falsos_negativos` says the same for coverage. **`funding_gate`** (P-4): with `aplicavel: true` and a non-empty `infracoes`, name the ids — open financial questions about envelope, threshold or allocation in an engagement whose go-ahead does not depend on a third party's budget; with `aplicavel: false` there is nothing to check and the empty list means exactly that. **Enquadramento** — `enquadramento.presente` false in Discovery → one line saying the owner has not declared the business mechanism (`M-n`) yet; true → `R-00` is reported as *enquadramento (dono)*, never as a round of lenses, and the `M-n` rows never count towards a lens (`facets.lens_producao`).
   Also here: `status.synthesis.topics[<topic>].verdict` — **per topic** (P-18 / F04): `stale` (the topic ran before an authority it consumes — `reasons[]` names which: the blueprint approval, a SU row verified later, a newer decision block, or the blueprint **identity** the architecture-story stamped ≠ the approved version), `desconhecido` (pack present, no line in `_synthesis-log.md` — say *sem registo*, never *posterior à aprovação*), `missing`, `fresh`; `stale_topics` / `unknown_topics` are the lists to name; `stale_vs_approval` survives as the architecture-story-vs-approval shorthand. One fresh topic never speaks for another. Also `status.blueprint.latest_authorized` (the version the Architecture Blueprint deliverable reads, with its `state` — approved or not, and why), `status.render.behind_current_blueprint`, `status.simulations[].stale` (cites a resolved/expired/absent id), and every motor diagnostic. An expected authority missing or unreadable is reported as **"verificação incompleta — falta X"**; a file the phase does not yet expect is not a gap; absent data never becomes "zero bloqueios".

9. **Derive the `Read to resume` set** — **PHASE ≠ SESSION**: session context is a disposable cache, repository engagement state is the durable memory, and a fresh session must not depend on the previous transcript. The block comes from `status.read_to_resume` — **computed** from `_state.json.phase` and the file system every time; it is never persisted, it is not a new authority and it is not a handoff summary. It names only what the active phase materially needs — never all raw evidence, all transcripts, all lens outputs or all Domain Knowledge:

   | Phase | Read to resume (in this order) |
   |---|---|
   | discovery | `_state.json` · `context.json` · `shared-understanding.md` (open rows; Critical first) · `_capture/evidence-index.md` · `_capture/process-model.md` §4 (synopsis) + §6 (PM-U) · `lens-outputs/<lens>.md` of the **current** round only |
   | framing | `_state.json` · `shared-understanding.md` (material rows) · `_capture/process-model.md` §4 · `frame.md` (if a round ran) · `decisions.md#D-001` (if agreed) |
   | options | `_state.json` · `frame.md` (sentence + *What must survive into Options*) · `shared-understanding.md` (material rows) · `options.md` (if a round ran) · `_capture/process-model.md` §4 only where the synopsis is needed — detail sections when material |
   | decision (pre-blueprint) | `_state.json` · `decisions.md` (solution D-NNN, conditions, tripwires) · `options.md` (chosen option and the strengths the decision cites) · `shared-understanding.md` (material rows) · `_synthesis/*.md` |
   | decision (architecture) | `_state.json` · `decisions.md` (solution decision + blueprint approvals) · latest `_blueprint/ux-blueprint_v<NN>.yaml` (+ any version it back-references) · `_blueprint/blueprint-log.md` (last entry) · `options.md` (chosen option's strengths — the target of a Decision-basis revalidation) · `answers.md` (verbatim answer per id — the SU carries the extracted claim, not the answer) · `_synthesis/architecture-story.md` · `shared-understanding.md` (material rows) · Domain Knowledge **pulled per the blueprint's own rules**, never listed here |
   | deliverables | the closest authorities the render contract names (`library/kernel/render-contract.md`) · `_render/render-gaps.md` · `_render/render-log.md` |

   "Material rows" (`read_to_resume.material_rows`) = open Critical `Unknown`/`Conflicted`, `Risky`, rows cited by the current phase artefact, and expired rows. Detailed process evidence (`process-model.md` §2–§3/§5, `*.text.md`, raw `inputs/`) is pulled **only** when the synopsis and the SU do not answer a material question — name that pull as targeted, never as default reading. Existing pointers stay authoritative for their content: this block says *where to look first*, not *what is true*.

10. **Output**, in this order — seven blocks, each answering one business question (owner decision 2026-09-08, frente C; plan §2 for the sources). Every number is the model's; nothing is recounted. Blocks 1, 2, 3 (abbreviated to one line per item) and 7 are what `/resume` shows.
   ```user-output
   Onde estamos: <etapa em palavras — ouvir e perguntar · a frase do problema · as alternativas · a escolha e o que vem depois> (<fase · ronda>) — projecto `<slug>`<, tipo de solução escolhida: <em palavras, só a partir da escolha — antes disso a linha não nomeia tecnologia nem tipo de solução>>.   [1]
   O que falta para o próximo passo: <milestone.marco em palavras> — <len(milestone.blocking)> pontos bloqueiam-no (<quantos graves>), de <len(items)> pontos materiais no total.
   O que tens de fazer tu: <o passo humano, com quem — ou «nada agora: o próximo passo é meu»>.

   ⚠ Alerta                                                                                    [2 — só se houver]
   Condição de revisão disparou (<TW-n>, decisão <D-NNN>): <linha do registo> satisfaz «<cláusula>» → `/revisit TW-n`
   Facto grave caducou: <facto curto> (<id>) — pede reconfirmação → `/answer --revalidate <id>`
   Resumos por tema desactualizados face ao que consomem: <tema — razão curta; …> → `/synthesize <tema>` antes de `/render`
   Resumos por tema sem registo de produção (<temas>) — verificação incompleta, não se afirma que estão actualizados → `/synthesize <tema>`
   Frase do problema por aprovar (<mudou desde a aprovação <D-00x> | nunca aprovada | aprovação antiga, sem impressão digital>) → `/options` pergunta-te antes de avançar   [só se o veredicto da frase não for «confere» (frame.verdict ∉ match, match-other-round, no-frame)]
   Alternativas reabertas (decisão <D-00x> substituída) — a escolha anterior fica no registo → `/decide` quando escolheres   [só se houver reabertura em curso (reopen)]
   Documentos finais feitos sobre um desenho antigo (versão <NN>; a actual é <MM>) · ensaio que cita factos já resolvidos ou caducados (<ids>)

   O que falta para o próximo passo                                                             [3]
   1. <tema, em meia linha> (<id>)
      Bloqueia: <o que não pode acontecer sem isto — âmbito + regra citada> · Afeta: <condição de revisão (TW-n, D-NNN) · alternativa · decisão · documento | «sem ligação registada a decisão, alternativa ou entrega»>
      Falta: <a escolha estrutural ou a prova em falta | a própria pergunta>
      Quem: <o papel ou a fonte a consultar | «por atribuir»>   (executa a prova: <quem>, se distinto)
      Fecha quando: <critério | «<o que muda com a resposta> — critério formal por definir»>
      Como: `/answer <id> "…"` | `/blueprint --refresh` | <o comando que o modelo nomeia>
      Fonte: <ficheiro#chave | registo, linha <id>>
   2. …  3. …
   Também importa: <tema curto> (<id>) — <consequência>; …          (todos os graves e todos com obrigação registada — nunca escondidos para caber)

   Agenda da próxima reunião                                                                    [4]
   Muda o caminho: <pergunta formulada> (<id>) — <o que muda> → quem: <papel> → ver «o que falta» N   [Q-/P-LENS-NN se veio do banco]
   Muda o tamanho: <pergunta formulada> (<id>) → quem: <papel>
   Confirmar como percebemos o processo [reunião] (teach-back) — «é assim que entendemos que funciona: <frases da síntese>; o que está errado ou em falta?» — cobre <n> perguntas (<ids>); cada uma fecha por si via `/answer`   [só se 7b disparou]
   Por outro canal: <pergunta curta> (<id>, email) · <pergunta curta> (<id>, documento) · <pergunta curta> (<id>, trabalho técnico — canal, sem duração registada)
   Não gastes reunião nisto: <pergunta curta> (<id>) …

   Desde a última passagem (<ronda>)                                                            [5]
   <n> perguntas novas · <n> fechadas · <n> em aberto no total (<c> graves) <· abrimos mais do que fechámos>
   Factos novos nesta passagem: <n> verificados · <n> assumidos · <n> contradições entre fontes · <n> riscos   (round_delta.por_ronda[ronda].novas)
   <n> fechos que o motor não consegue datar — não contam em nenhuma passagem   [só se round_delta.indeterminadas]
   A passagem <M> ficou a meio: faltam <perspectivas em palavras> — `/round <perspectiva em falta>` para continuar (qualquer uma, por qualquer ordem), ou `/round --close` para a dar por fechada   [só se houver passagem em curso (engagement.round_in_progress); as em falta vêm do motor (engagement.lentes_ronda_aberta.em_falta), nunca inferidas da ordem habitual]

   Conferência do desenho (só a partir do momento em que existe desenho)                        [5b]
   Estrutura: <verificada, sem falhas | <N> falhas que impedem a aprovação (códigos entre parênteses) | ilegível>
   O pedido está todo lá: <ainda não foi conferido — não é nem bom nem mau sinal | conferido, sem lacunas | <N> por responder e <M> por fundamentar: <tema curto> (<id>) … | tem de ser reconferido: mudou <o quê>>
   O negócio aprovou: <sim, a versão <NN> (<D-NNN>) | ainda não | aprovou a versão <MM>, e a actual é a <NN>>
   Funciona de ponta a ponta: nunca foi provado aqui — isso mede-se a correr a solução, não a lê-la.
   <o que falta antes de poder levar à aprovação: <razão curta> …>   [só se houver]
   <o que não foi possível conferir: <ficheiro ou fonte> — <razão>>   [só se houver]

   Confiança no que sabemos                                                                     [6]
   verificado <N> (+r já resolvidos) · assumido <N> · em aberto <N> (<C> graves, +r resolvidas) · em conflito <N> (<C> graves) · riscos <N>
   Em prazo: <NN>% — <X> factos por reconfirmar (Saúde epistémica) — mede a validade da prova, não a prontidão
   Factos sem prova localizável: <N> (<ids>) — a evidência não tem âncora que abra; não é o facto que está errado
   A reconfirmar primeiro (por dependência material, depois antiguidade; top-5 de <X>):
     <facto curto> (<id>, <validade>, verificado <data>) — «Ainda é verdade que …?» → `/answer --revalidate <id>`
   Riscos registados: <N> (<ids>) — com mitigação proposta; não são pendências
   Perguntas de orçamento que não deviam estar abertas — o dono declarou que avançar não depende de aprovação de terceiros: <n> (<ids>)   (só se funding_gate.aplicavel e infracoes ≠ [])
   Perguntas que ainda não dizem o que muda com a resposta: <n> de <total> — a verificação automática da passagem seguinte reclassifica-as   (só se arbiter.sem_declaracao ≠ [])
   Como o negócio funciona, dito pelo dono: <n> regras declaradas (<ids>), registadas no arranque | ainda não declarado   (só em Discovery)
   Avisos do sistema ao ler o registo: <verbatim | nenhum>
   Códigos entre parênteses = linhas do registo: U- pergunta · C- facto verificado · A- assumido · X- contradição · R- risco · M- regra do negócio; respondem-se com `/answer <código> "…"`.

   Para retomar (Read to resume (<phase>)) — derivado, nunca guardado; uma sessão nova não precisa do transcript anterior:   [7 — só no /resume]
     <ficheiro> — <do que é a autoridade>
     `shared-understanding.md` — linhas materiais (<ids, entre parênteses, nunca soltos>)
     só se o acima não chegar: <process-model §2–§5 | *.text.md | unidade de Domain Knowledge>

   A seguir: <o passo humano, se houver — quem faz o quê> → `/<comando com os argumentos reais>`
   ```
   Block 5b prints **only where a design version exists** (`status.blueprint.versions` non-empty) — before that there is nothing to check and its absence is not a finding. Its four lines are the four questions of `status.coverage`, in the model's order, each from its own field: they are never collapsed into one verdict and one is never allowed to speak for another. *Ainda não foi conferido* (`present: false`) is printed as exactly that — it is not a failure, and an approval already on file stays on file and is still reported on the third line. `/resume` does not print block 5b.
   Block 2 is omitted entirely when nothing fired, caducou or drifted — no "Alerta: nenhum" line; while no solution decision exists (Discovery, Framing, Options) the revision conditions simply do not appear — they belong to the decision, and their absence is not a finding. Block 7 prints only under `/resume`. Omit "A reconfirmar" when nothing is expired; omit the teach-back line when 7b did not trigger. Blocks 3 and 6 never omit a material blocker or a diagnostic to save space. Where the milestone is a blocked approval, the `A seguir` line says that a fact never closes a structural choice by itself (fact ≠ fit). Block 2 reads `frame` (P-18): a `verdict` other than `match` / `match-other-round` means the sentence on file is not the approved one — `mismatch` (it changed), `none` (never approved) or `legacy` (approved before the fingerprint rule, so it cannot be verified); `no-frame` is not an alert in Discovery, where there is no sentence yet. It also reads `reopen`: a REABRIR verdict from `/revisit` with the engagement back in Options is a reopening in progress, not a fresh Options round. Block 5 reads `round_delta.por_ronda` for the round in `_state.json` (`criadas`, `fechadas`, `sem_convergencia`, `novas` per state) and `round_delta.abertas` / `critical_abertas` for the totals. The round it reports is `engagement.round` — the last **completed** one. When `engagement.round_in_progress` is non-empty a passagem is open with only part of the perspectives run (`library/kernel/phases.md` → *Rounds*): say which are missing and the exact command, and never report the open round's partial counts as a closed passagem's balance.

## Hard rules

1. **Never invent.** No owner, deadline, day count, acceptance criterion or conclusion that the model or the sources do not carry. `custo=spike` names a channel, not a duration. Absent → say absent.
2. **Facts from the motor, judgement from the skill.** Do not recount or re-derive what `--json` already carries.
3. **`no-evidence` is not OK.** It is the question "is this even evaluable now?".
4. **Fact ≠ fit.** A resolved row never closes a structural choice from here (`aisa-answer` 4b / `aisa-blueprint` 11); the item says what would.
5. **Approval of an older version never covers a newer one.**
6. **Discovery/Framing name no technology.**
7. **Absence is incomplete, never zero.**
8. **Structure, coverage, approval and end-to-end are four questions** (`coverage-contract.md` §1). Report four answers; never let one stand for another, and never print *ainda não foi conferido* as a pass or as a failure.
9. **Reading the state writes nothing.** This skill's only write stays the SU health header (step 3). The coverage dimension is derived from the records and the sources on every read — it finalizes no review, sets no flag and records no approval, so consulting the status can never change what the status says.

## Execution steps (--check)

1. `library/kernel/`: the 7 protocol files (`phases.md`, `states.md`, `orchestration.md`, `render-contract.md`, `blueprint-contract.md`, `coverage-contract.md`, `glossary.md`) + `synthesis-templates/` with 5 templates + `capture-templates/process-model.template.md` + `tools/` with `dashboard.py`, `xlsx_extract.py`, `text_extract.py`, `fields_draft.py`, `coverage.py`.
2. `python library/kernel/tools/dashboard.py --version` runs and prints a version ≥ 1.1.0 (the status model).
3. At least one pack under `library/packs/` with a `pack.yaml`.
4. Engagements root resolvable: `$AISA_ENGAGEMENTS_ROOT` is set, or `projects/` exists and is writable.
5. `.claude/hooks/pre-write-guard.py` and `.claude/hooks/on-su-change.py` exist; `python`/`python3` on PATH (all hooks are Python 3).
6. Output green/red per check:
   ```
   ✓ kernel: 7/7 protocol files · synthesis-templates 5/5 · capture-templates 1/1 · tools 5/5
   ✓ dashboard.py 1.1.0 (status model)
   ✓ packs: pp (+ generic, mendix, outsystems)
   ✓ engagements root: projects/ (or $AISA_ENGAGEMENTS_ROOT)
   ✓ hooks: pre-write-guard.py, on-su-change.py (Python)
   ✓ ready.
   ```
   A red line names what is missing; `--check` never touches an engagement.
