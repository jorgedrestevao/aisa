# aisa — Project Memory

## What this is

<!-- SCOPE-STATEMENT v1 -->
**aisa** runs discovery on a process to reach a grounded technical decision: which technology and pattern, against which alternatives, at what cost. It is not an open-ended business-discovery platform; a question is admitted only when its answer can change the decision. It runs as a Claude Code project, over digitalization projects (Power Platform, OutSystems, Mendix, custom).

> **Full architecture**: `docs/ARCHITECTURE.md`
> **Philosophy**: `docs/PHILOSOPHY.md`
> **Onboarding**: `docs/ONBOARDING.md`

## Operating principles (inviolable)

1. **Discovery before solution, always.** Lenses do not mention vendor/product before the Options phase.
2. **Shared Understanding as process artefact; deliverables as transition artefacts.** SU is the source of truth during the engagement; the 6 deliverables are rendered at the end.
3. **5 knowledge states**: Confirmed / Assumed / Unknown / Conflicted / Risky. No state×tag combinatorics. Confirmed/Assumed carregam validade — conhecimento expira e revalida-se (`library/kernel/states.md` → *Epistemic half-lives*).
4. **Council híbrido** by phase: inline in Discovery; council-independent (parallel subagents) in Framing/Options. Decision is interactive (user-driven; optional `/decide --consult` technology review).
5. **Soft gates**: warnings, overrideable with justification. The only hard rule is `library/` is read-only at runtime.
6. **Native Claude Code primitives**: skills, agents, hooks, commands. No reinvention.
7. **Pack activo per-engagement**: declared in `projects/<slug>/_state.json.pack`. Not global.
8. **Atomic writes** to `_state.json`: tmp → mv pattern.
9. **Knowledge expires; questions have prices; decisions keep their counterfactuals.** (kernel v0.2.0: half-lives, question economics, tripwires/multiverso, diários do council.)
10. **Reason deeply → persist selectively → claim conservatively → rehydrate selectively → revalidate when premises change.** Determinism governs what must survive compression, who owns it (SU), what may not be silently promoted or dropped (disposition `MAP`/`ADOPT`/`DISMISS`; fact ≠ fit), what is revalidated when a premise changes, and what a fresh session reloads (phase ≠ session). Never the internal reasoning sequence. (`library/kernel/orchestration.md` → *Comprehension survival*.)

## Key paths

- `library/kernel/` — universal protocols (phases, states, orchestration, render-contract, blueprint-contract, coverage-contract, glossary).
- `library/kernel/tools/` — **a camada de memória persistente** (P2–P8), os seis motores que fazem o estado do engagement sobreviver a uma sessão e a uma falha. Nenhum é opcional desde que o grafo é obrigatório:
  - `graph.py` — o grafo aditivo do engagement (`<engagement>/_graph/`). Espelha a SU (`provenance.mirror_of`) e **nunca prevalece sobre ela**: `drift` compara e reporta; `state`, `criticidade` e `resolved` divergentes bloqueiam, texto divergente informa.
  - `operation.py` — o coordenador. Toda a escrita de conhecimento passa por aqui: intenção → marcador de pendência → publicação temp+rename → verificação → recibo → retirar a pendência. Exclusão por `flock` (do kernel, não pela existência do ficheiro); `status()` publica sob que garantia foi produzido (`exclusion`).
  - `bootstrap.py` — a reconstrução comum. É o que qualquer leitor ou escritor consulta ANTES de concluir: pendência, snapshot e grafo de **uma revisão só**, autoridade comparada com o espelho, contexto com orçamento e truncagem declarada. `ready=False` nomeia sempre a acção que o desbloqueia.
  - `resolve.py` — as transições de estado do `/answer` e as quatro operações de ciclo de vida (`revalidate` · `withdraw` · `accept_risk` · `resolve_conflict`), planeadas e publicadas pelo coordenador. `cited_by`/`impact_of` dão os derivados que citam uma linha — **candidatos, não veredicto**. `sync_mirror` é o espelho das escritas que **não** passam pelo coordenador — as das lentes, pela ferramenta Edit — e corre sozinho pelo hook `on-su-mirror.py`.
  - `migrate.py` — legado → memória persistente (`dry-run` · `apply` · `restore` · `init`). `init` é o grafo com que um engagement NASCE, e recusa um engagement que já tem conhecimento — isso migra-se.
  - `projection.py` — o estado operacional em linguagem de negócio: bloqueios com motivo, evidência e acção; é o que o `/status` consulta antes de responder.
- `library/kernel/tools/` — motores determinísticos de conteúdo, **read and executed** at runtime (`xlsx_extract.py`, `text_extract.py`, `dashboard.py`, `fields_draft.py` — L1 → rascunho de campos/contratos, invocado por `/blueprint`; `coverage.py` — a conferência de que o que se produz responde ao que foi pedido, em três etapas (`reconciliation` · `blueprint` · `render`), invocada por `/blueprint` (passos 1b e 13b), `/render` (passos 2b e 9b), `/answer`, `/capture` e `/status`; contrato em `library/kernel/coverage-contract.md`). Executing is not writing: the read-only rule covers runtime *edits* — e `finalize` é a única operação de escrita do motor, e escreve só em `<engagement>/_coverage/`.
- `library/packs/<id>/` — domain-specific (PP, OS, Mendix). Read-only at runtime.
- `.claude/skills/` — lenses + commands + synthesis + render.
- `.claude/agents/` — personas for council-independent mode.
- `.claude/hooks/` — programmatic enforcement.
- `projects/<slug>/` — engagement state (mount point to private repo).
- `projects/<slug>/_graph/` · `_ops/` · `_migration/` — **estado coordenado. Nunca editar à mão.** O grafo é autoridade operacional (o contexto é construído dele); `_ops/` é a barreira (marcador de pendência + recibos). Quem lá escreve é `operation.py`, em Python. O hook `pre-authority-guard.py` recusa `Write`/`Edit` nestes caminhos — uma escrita por ferramenta aqui é, por construção, edição à mão de estado coordenado.
- `projects/<slug>/dashboard.html` — generated living page. Never hand-edit: `shared-understanding.md` stays the source of truth.

## Slash commands

| Command | Purpose |
|---|---|
| `/start <slug> [pack]` | New engagement |
| `/round [lens\|--close]` | Run a Discovery round — sem argumento corre as 6 perspectivas pela ordem obrigatória; `/round <lens>` corre **uma** isolada, sem pré-requisito, por qualquer ordem; `--close` dá a passagem por fechada |
| `/capture [file]` | Process-capture an input file (`.xlsx`/`.xlsm`): deterministic extraction + replay + process model into `_capture/`. Auto-runs in `/start` and on stale hashes in `/round` |
| `/answer <id> "..."` | Resolve an Unknown/Conflicted/Assumed/Risky row (state transition + answers.md) |
| `/status` | O que falta para o próximo passo — 7 blocos em linguagem de negócio: resumo em 3 linhas (onde estamos · o que falta · o que tens de fazer tu) · alerta só se houver · o que falta (top-3 + também importa) · agenda da próxima reunião · desde a última passagem · confiança no que sabemos · `A seguir:` |
| `/frame` | Transit to Framing phase |
| `/options` | Transit to Options phase |
| `/simulate [O-NNN ...]` | Project each option (screens, effort, risks) + decision-flipping Unknowns, before `/decide` |
| `/premortem [--horizon <meses>]` | Write the project's obituary before deciding — failure causes anchored to SU ids; mitigations → requirements/tripwires |
| `/decide [--consult]` | Capture decision; auto-runs `/synthesize` |
| `/blueprint` | Produce the UX blueprint (screen architecture) from the SU + pack rules; iterate to business approval. Confere as fontes antes de desenhar e o desenho depois (`library/kernel/coverage-contract.md`): estrutura, cobertura, aprovação e ponta-a-ponta são quatro perguntas separadas, e nenhuma responde pela outra |
| `/synthesize` | Produce topic packs (auto after `/decide` or manual) |
| `/render [deliverable\|--all]` | Render the deliverables (filtered by decision type). Confere duas vezes, e as duas não se misturam (`library/kernel/coverage-contract.md` §8.2/§8.3): **antes** de cada deliverable, as autoridades que *ele* declara e a versão de desenho que o *seu template* manda ler; **depois**, se a projecção carregou o que foi seleccionado. Autoridade que ainda não existe é *skip com razão* em `render-log.md`, nunca lacuna; obrigação perdida é lacuna com dono em `render-gaps.md`, devolvida a montante |
| `/revisit <TW-n\|O-NNN>` | Compare the present with a frozen counterfactual when a tripwire fires; recommend keep/adapt/reopen |
| `/retro` | Close-of-engagement: personas write diaries (human-curated) — the council gets wiser |
| `/resume` | Resume from `_state.json` and name the next command |
| `/dashboard [slug] [--serve\|--url\|--open]` | Regenerate the living dashboard `projects/<slug>/dashboard.html` — 6 separadores em barra lateral (Panorama / Etapas / Agenda / Registo / Narrativa / Ficheiros; Etapas renderiza frame.md, options.md, premortem, synthesis e blueprint por extenso), self-contained, deterministic. O separador aberto e a linha aberta vivem no URL (`#estado/C-157`, partilhável); o Registo ordena por coluna e exporta CSV do que está no ecrã. The `on-su-change.py` hook covers agent writes only; `--serve` adds a localhost server + mtime watcher, and over HTTP the page reloads only when the build hash changes (on `file://` it can only reload blindly). `--url` prints where to open it when the link is lost; `--serve` reattaches instead of starting a second watcher |

Sem comando: uma mensagem que descreve um processo, um problema ou pede um resultado («quero a estimativa») é a entrada principal → skill `aisa-orient` (ver *Entrada sem comando*).

## Duas línguas (P-13)

O vocabulário do kernel é preciso e **fica**: nos ficheiros, ids, colunas e contratos. **Tudo o que o utilizador lê ou responde** — a linha final de qualquer comando, perguntas `AskUserQuestion`, `story.md`, dashboard, deliverables — vai em linguagem de negócio, pela coluna *Como se diz ao utilizador* de `library/kernel/glossary.md`.

- Termo do kernel só **entre parênteses, depois da frase de negócio**, na primeira ocorrência: `pergunta em aberto (Unknown)`. Nunca sozinho, nunca como título.
- Ids entre parênteses depois da frase que identificam: `a regra de arredondamento (U-012)`. Nunca como sujeito.
- `AskUserQuestion`: pergunta e `label` das opções em linguagem de negócio; id e termo do kernel na `description`.
- Todo o output de comando termina com `A seguir: <passo humano, se houver> → `/comando args``. O utilizador não decora comandos.
- Os templates de output nas skills vão em blocos ```user-output; `.claude/tests/test_user_language.py` lê-os contra o glossário — termo ou id fora de parênteses é falha.
- Excepção: os ficheiros. `shared-understanding.md`, `_state.json`, logs e artefactos de fase mantêm o vocabulário do kernel intacto.
- Deslizes frequentes (observados na validação, step-9e): «blueprint v06» → *o desenho dos ecrãs, versão 06*; «ronda» → *passagem*; «spike» → *trabalho técnico*; «tripwire» → *condição de revisão*; uma lista de ids solta («linhas materiais: U-032, U-036») → *entre parênteses* («linhas materiais (U-032, U-036)»). Ids em crase não são parênteses.

## Entrada sem comando (P-14)

Uma mensagem que descreve um processo, um problema ou uma intenção de começar — sem comando — é a entrada principal, não um erro. Invocar a skill `aisa-orient`:

- **Não há engagement que corresponda** → enquadramento do aisa em cinco linhas de negócio, os passos com o comando de cada um, a entrevista de enquadramento (P-0, o dono já está a falar do mecanismo), depois a proposta de `/start` por `AskUserQuestion` (slug proposto, tipo de solução se declarado, ficheiros). Confirmado → `aisa-start` corre com a declaração já recolhida e não volta a perguntar.
- **Já existe engagement e a mensagem é sobre ele** («já decidimos, quero a estimativa») → `aisa-orient` reorienta como `/resume` e diz, em linguagem de negócio, o que falta antes do que foi pedido e o comando exacto.
- **Ambíguo** entre começar, continuar e só perguntar → `AskUserQuestion`; nunca assumir.

`aisa-orient` não escreve nada; `aisa-start` escreve. Sem vendor nem produto no enquadramento (princípio 1). `docs/COMO-USAR.md` é a página de uma folha para quem usa; `docs/ONBOARDING.md` fica para consultor/developer.

## Anti-patterns to avoid

- Naming Power Platform / OutSystems / Mendix / Dataverse before the Options phase.
- Editing `library/` at runtime (hook will reject).
- Inventing claim states without evidence (use Unknown instead).
- Bypassing `/synthesize` between `/decide` and `/render`.
- Editar `_graph/`, `_ops/` ou `_migration/` à mão (o guarda recusa, e com razão: apaga a prova de que uma operação aconteceu, ou inventa uma que não aconteceu).
- Concluir antes de apresentar limitações. Um leitor que responde sobre estado por reconstruir apresenta estado misto como estado — as contagens ficam certas e a conclusão errada, e a diferença não aparece em contagem nenhuma.

## Where things live

For full layout: `docs/ARCHITECTURE.md §6`.

## Regras (hard rules)

- **Nunca inventar.** No guessed IDs, fields, endpoints, values. Unknown → say so, don't fill gaps.
- **Pergunta em aberto (`Unknown`) só com as três declarações** (P-26, `library/kernel/states.md` → *Admission of a question*): o `M-n` que serve (ou o marcador `TO-BE DIVERGENCE` com o que o alvo tem de decidir) · ≥ 2 respostas · qual dos oito eixos muda com cada uma (tecnologia · padrão arquitetural · componentes · modelo de dados · plano de imposição de permissões · esforço de alto nível · custo · risco técnico). `M-n` **nunca** dispensa o eixo. Sem eixo → `cosmético` (a gravidade desce com ele); sem 2ª resposta → não se escreve. Vale para todos os escritores (6 lentes, `chairman-synthesis`, `/answer`, `PM-U` de `/capture`). Só muda detalhe ou faixa → `Assumed` com base; só se resolve na implementação → nenhuma linha. **A organização não saber não é trabalho do projecto**: falta de política escrita, de inventário ou de maturidade descreve a organização; o que o alvo tem de definir é requisito, não pergunta pendente.
- **Perguntar antes de assumir.** Ambiguous instruction, ambiguous "yes"/"sim" to an either/or question, or any request that could be read as fact-statement OR action-request → confirm scope before mutating anything. Read-only exploration never needs confirmation.
- **INVIOLÁVEL — perguntas ao utilizador vão SEMPRE por `AskUserQuestion`.** Sempre que o processo pede ao utilizador para resolver um tema — responder a uma `Unknown`/`Conflicted`/`Assumed`/`Risky`, escolher entre alternativas, aprovar um blueprint/versão, confirmar âmbito, autorizar um override de gate, decidir em `/decide`, validar um teach-back — a pergunta é feita com a ferramenta `AskUserQuestion` (opções explícitas; "Other" fica disponível por defeito). Uma pergunta em prosa no fim da resposta **não conta** como pergunta feita e não autoriza a assumir nada. Aplica-se a todas as skills/comandos aisa nesta sessão. Excepção única: quando a ferramenta não está disponível (ex.: subagente sem `AskUserQuestion`) — nesse caso o tema fica registado como aberto (`Unknown`), nunca resolvido por inferência.
- **Estilo de resposta: Caveman — curto, direto, zero enchimento.**
- **Execução real > teoria.** Respostas priorizam execução real, geração de resultado, impacto mensurável.
- **Direto, lógico, estruturado.** Evitar excesso de teoria, abstrações desnecessárias, explicações longas sem ação. Sempre que possível: passos acionáveis, frameworks, modelos prontos, exemplos aplicáveis, checklists, roteiros, estruturas reutilizáveis em contextos reais de negócio.
- **Clareza > sofisticação de linguagem.**
- **Sem validação automática de ideias.** Análise crítica: riscos, gargalos, pontos fracos, oportunidades de melhoria, contrapontos construtivos. Agir como conselheiro estratégico, não gerador de respostas agradáveis.
- **Linguagem simples, profissional, objetiva, sem clichês retóricos.** Sem frases genéricas motivacionais, sem contrastes artificiais. Raciocínio progressivo, clareza lógica, utilidade prática.
- **Estruturar hierarquicamente** — secções bem definidas, leitura rápida, decisão rápida.
- **Objetivo final de toda resposta:** ajudar a tomar decisões melhores, executar mais rápido, escalar resultados, aplicar IA de forma prática em negócios reais.

### Regras output (verbatim spec)

Respond terse like smart caveman. All technical substance stay. Only fluff die.

Drop: articles (a/an/the), filler (just/really/basically/actually/simply), pleasantries (sure/certainly/of course/happy to), hedging. Fragments OK. Short synonyms (big not extensive, fix not "implement a solution for"). Technical terms exact. Code blocks unchanged. Errors quoted exact.

Pattern: `[thing] [action] [reason]. [next step].`

Not: "Sure! I'd be happy to help you with that. The issue you're experiencing is likely caused by..."
Yes: "Bug in auth middleware. Token expiry check use < not <=. Fix:"
