# Step 9e — Frente C: entrada e linguagem (P-13, P-14)

> Passo do tracker para a **frente C** do `docs/CONSOLIDATED_PLAN.md` §5.
> Ficheiros: `library/kernel/glossary.md` · `CLAUDE.md` · `.claude/skills/aisa-*/SKILL.md` (16 comandos, linhas de output) ·
> `.claude/skills/aisa-orient/SKILL.md` (novo) · `.claude/commands/resume.md` · `library/kernel/tools/dashboard.py` (1.5.0) ·
> `docs/COMO-USAR.md` (novo) · `.claude/tests/test_user_language.py` (novo, 20 testes).
> Cópias de validação: `pricing-marinha-pilot-3` (`/status` real, só a escrita sancionada do cabeçalho) · `pricing-marinha-pilot-3-val-c`
> (`/round business` real, R-04 → R-05) · `pricing-marinha-pilot-1` (só leitura, teste 2 de P-14).
> Modelo: Fable 5.1 (`claude-fable-5-1`) para a prosa e as decisões de forma; validação em Sonnet 5 (modelo de produção do Discovery), subagentes isolados.
> Evidência: `step-9e-evidence/` — `accept_frente_c.py` (aceitação determinística antes/depois), `accept_p14_runs.py` (lint dos outputs reais),
> `status-pilot-3-R04.md`, `round-business-val-c-R05.md`, `p14-runs.md`.

---

## 1. Desenho — o que ficou decidido antes de tocar em ficheiros

**A regra mecânica é a dos parênteses.** O plano pedia «zero termos da coluna esquerda do glossário nas linhas de output sem a frase da coluna direita ao lado». Isso não é verificável sem julgamento. A forma verificável é a que P-13 já enunciava na mecânica 2: **o termo do kernel e o id só aparecem entre parênteses, depois da frase de negócio**. Um lint tira o que está entre parênteses e os comandos/caminhos em crase, e procura o que sobra. Crase não é parêntese: `` `Unknown` `` sozinho continua a ser jargão.

**O glossário passa a contrato máquina.** `glossary.md` ganha a coluna *Como se diz ao utilizador* e uma regra de leitura: cada termo **em negrito** ou em `código` na primeira coluna é um token que o lint procura; uma palavra sem marca na primeira coluna (`custo`, `validade`, `enquadramento`) é português corrente e não se linta. As traduções não podem reutilizar tokens (testado). 60 linhas; as do plano mais as que a validação pediu (*structural choice*, *locator*, *convergence*, *disposition*, *read to resume*).

**Os templates de output ficam marcados.** Cada skill de comando declara o que o utilizador lê num bloco ```` ```user-output ````; o último bloco de cada skill fecha com `A seguir: <passo humano, se houver> → /comando`. O teste lê exactamente esses blocos — não adivinha onde o output está.

**O `/status` foi reestruturado, não só traduzido** — decisão do owner nesta sessão (`AskUserQuestion`, 2026-09-08), opção recomendada: 7 blocos por pergunta do negócio — resumo em 3 linhas (onde estamos · o que falta · o que tens de fazer tu) · alerta **só se houver** (em Discovery/Framing/Options as condições de revisão simplesmente não aparecem, em vez de «Tripwires: verificação incompleta») · o que falta (top-3 desenvolvidos + «também importa») · agenda da próxima reunião · **desde a última passagem** (novo: delta por estado, do motor) · confiança no que sabemos · «para retomar» só no `/resume`. O motor ganhou `round_delta.por_ronda[].novas` (linhas criadas por estado, por ronda) para o bloco 5 — facto no motor, prosa na skill.

**A onda 0 desta frente é a linha de base do lint.** Não havia blocos marcados nas skills antigas; o script de aceitação usa uma heurística (texto a seguir a `Output:` / `Wrap-up output` / bloco cercado) só para o número «antes». O «depois» não precisa de heurística.

## 2. P-13 — duas línguas

| Ficheiro | O que mudou |
|---|---|
| `library/kernel/glossary.md` | secção *Two languages (P-13)* com as 4 regras e o contrato de lint; tabela a 3 colunas, 60 termos |
| `CLAUDE.md` | secção *Duas línguas (P-13)*: regra dos parênteses, ids, `AskUserQuestion` (label vs description), `A seguir:`, blocos `user-output`, excepção dos ficheiros, **deslizes frequentes** (os que a validação apanhou) |
| 15 skills de comando | linhas de output reescritas em linguagem de negócio, em blocos `user-output`, todas fechadas com `A seguir:`; `aisa-frame` passa a pedir a validação da frase por `AskUserQuestion` (aceitar · editar · mais passagens) em vez de «yes/edit/more rounds» em prosa |
| `aisa-status` | bloco 10 reestruturado (§1); *Usage* declara a língua; «Para retomar» exige ids entre parênteses; legenda dos códigos numa linha (U- pergunta · C- facto verificado · …); linha 2 do resumo lê `len(milestone.blocking)` · graves · `len(items)` (ambiguidade apanhada no teste 2 de P-14) |
| `.claude/commands/resume.md` | quatro blocos do `/status` novo (1, 2, 3 abreviado, 7), língua herdada, fecha com `A seguir:` |
| `dashboard.py` 1.5.0 | etiquetas de negócio com o termo do kernel em `title=`: separadores (Outputs → **Etapas**, Artefactos → **Ficheiros**, tooltip com o termo), `SWING_LABEL` (muda o caminho · muda o tamanho · não muda nada), `CUSTO_LABEL` (spike → trabalho técnico), `PHASE_LABEL`/`PHASES` (ouvir e perguntar · a frase do problema · as alternativas · a escolha), colunas (`lens` → perspectiva, `claim` → afirmação, `swing` → o que muda, `criticidade` → gravidade, `ronda` → passagem), títulos (Tripwires → Condições de revisão, Críticos abertos → Graves em aberto, A revalidar → A reconfirmar, render-gaps → O que falta para os documentos finais, Diagnostics do parser → Avisos de leitura do registo), grupos do separador Ficheiros por nome de negócio (`GROUP_LABEL`) com a pasta em tooltip, `read_to_resume.entries[].why` em palavras; `round_delta.por_ronda[].novas` |

**Aceitação determinística** (`accept_frente_c.py`, ref `step-9d-frente-b` vs árvore de trabalho):

| Superfície | antes | depois |
|---|---|---|
| Linhas de output das 15 skills (heurística no antes; `user-output` no depois) | **90** violações em 18 blocos | **0** em 21 blocos; 16/16 fecham com `A seguir:` |
| Etiquetas estáticas do `dashboard.py` (74 lidas) | **13** | **0** |
| Página construída para pilot-3 (93 etiquetas: títulos, cabeçalhos, separadores, caixas) | — | **0** (conteúdo do engagement — títulos de narrativa, tabelas dos documentos de etapa — excluído por ser texto do engagement, não etiqueta) |
| `docs/COMO-USAR.md` | — | 35 linhas não vazias (≤ 70), 0 violações |
| `/status` abre com as três linhas · `/resume` herda | — | sim · sim |

Onde os «antes» eram 0 (`synthesize`, `simulate`, `premortem`) a linha já estava em português; `capture`, `revisit`, `retro` não tinham linha de output detectável — agora têm.

## 3. P-14 — entrada em linguagem natural

| Ficheiro | O que mudou |
|---|---|
| `CLAUDE.md` | secção *Entrada sem comando (P-14)*: três situações (arrancar · reorientar · perguntar), `aisa-orient` não escreve, `aisa-start` escreve, sem vendor |
| `.claude/skills/aisa-orient/SKILL.md` (novo) | A — enquadramento em cinco linhas, entrevista de P-0 (mesmos temas de `aisa-start` 4d), proposta de `/start` por `AskUserQuestion` (slug do processo, tipo de solução só se declarado, ficheiros); B — `/resume` + tabela *pediu → sai de → precisa antes*; C — `AskUserQuestion`; sem `AskUserQuestion` → fica em aberto, nunca inferido |
| `aisa-start` | passo 4 aceita a declaração já recolhida por `aisa-orient` («do not ask again») |
| `docs/COMO-USAR.md` (novo) | uma folha: o que é · o que dá · o que se espera de mim · como começo · como sei o que fazer a seguir · os passos com o comando · uma palavra sobre certeza |

**Teste 1** — mensagem literal de pilot-3 (com os erros de escrita), raiz sem engagement, 3 runs isolados (Sonnet 5, sem `AskUserQuestion`, sem escrita):

| run | 5 linhas | passos + comandos | entrevista P-0 | proposta `/start` (slug) | vendor | lint |
|---|---|---|---|---|---|---|
| 1 | sim | sim | 10 temas listados como «faria», nada inferido | `pricing-cotacoes` | 0 | **0** |
| 2 | sim | sim | 9 temas | `pricing-cotacoes` | 0 | **0** |
| 3 | sim | sim | 9 temas; nota que «o que se faz hoje» e «o que quer mudar» já vinham na mensagem | `pricing` | 0 | **0** |

Os três aplicaram a regra 4 do `aisa-orient` (sem a ferramenta de perguntas → tema em aberto, «não vou adivinhar respostas»). Nenhum criou ficheiros. Nenhum nomeou tecnologia.

**Teste 2** — «já decidimos, quero a estimativa», só pilot-1 existe (Decision, blueprint v06 por aprovar, v05 aprovada em D-004):

| run | situação | diz onde estamos | diz o que falta antes da estimativa | comando certo | lint |
|---|---|---|---|---|---|
| 1 | B | sim | 4 escolhas estruturais → `/blueprint` → `/synthesize` → `/render estimate` | sim | **14** — ids soltos em «linhas materiais: …», «spike» |
| 2 | B | sim | idem | sim | **28** — «blueprint v06», «ronda», ids soltos |
| rerun A (após correcção) | B | sim | idem | sim | **0** |
| rerun B (após correcção) | B | sim | idem | sim | **1** — «ronda», copiado do `why` do motor (`_state.json — fase, ronda`) → corrigido no motor |

As 42 violações dos runs 1–2 concentravam-se em **dois defeitos de template**, não na skill de orientação: a linha «`shared-understanding.md` — linhas materiais: <ids>» do bloco 7 do `/status` convidava a lista solta; e «blueprint vNN» era a forma natural de dizer a versão. Corrigidos (parênteses obrigatórios; *deslizes frequentes* no `CLAUDE.md`), os reruns caíram para 0 e 1 — e o 1 vinha de uma string do motor, que passou a palavras. Achado lateral do run 2: «escolha estrutural» não tinha entrada no glossário — acrescentada.

## 4. Validação real — `/status`, teste de leitura, `/round`

**`/status pricing-marinha-pilot-3`** (skill reescrita, motor 1.5.0; `status-pilot-3-R04.md`): 49 linhas, **0 violações**. Abre com as três linhas; sem bloco de alerta (Discovery, nada caducado); 3 itens desenvolvidos (U-085, U-033, X-009) + 7 «também importa»; agenda com 4 perguntas de reunião formuladas, teach-back com 4 ids, 21 por outro canal, 14 «não gastes reunião»; delta R-04 (22 novas · 33 fechadas · 62 verificados novos …); confiança (139/51/39/1/25, 100% em prazo, 0 sem prova localizável, 25 riscos). Única escrita: o cabeçalho `Saúde epistémica` (sancionada).

**Teste de leitura** — 3 leitores isolados (Sonnet 5) no papel de responsável de negócio, com acesso **apenas** ao ficheiro do `/status`:

| pergunta | leitor 1 | leitor 2 | leitor 3 |
|---|---|---|---|
| o que fazer a seguir e porquê | reunião com Pedro O. + gestão comercial, 4 perguntas + teach-back; «é o que falta para fechar a etapa» | idem | idem |
| quem faz o quê | Pedro O./gestão comercial (reunião) · equipa de entrega (verificação técnica, meio dia) · Governance/IT · **um ponto «por atribuir»** apontado como falha | idem | idem |
| quantos graves e o mais importante | 10; a verificação das séries (U-085) — «é a única que muda o caminho» | idem, com o mesmo porquê | idem |
| precisou de abrir outro ficheiro | não para agir; sim para os códigos e os comandos | idem | idem |

**Critério do plano cumprido 3/3**: a acção, o dono e o porquê saem do ecrã sem abrir nada. **O que os três apontaram como jargão**, apesar de estar entre parênteses: a densidade de códigos (U-/C-/A-/X-/R-/M-), `funding_gate = false`, «o árbitro», `pack pp`, «teach-back», «Leitura incompleta», «Saúde epistémica», `Discovery`. Dois deles leram também a nota de contexto que eu pusera acima do bloco (referências a «motor 1.5.0», «aisa-status», «P-13») — artefacto do teste, não do ecrã. **O que mudou por causa deles**, no template do `/status`: a variável `funding_gate` sai do texto (fica a frase do dono); «o árbitro» → «a verificação automática da passagem seguinte»; «Leitura incompleta» → «Avisos do sistema ao ler o registo»; «Teach-back do processo» → «Confirmar como percebemos o processo (teach-back)»; o pack deixa de aparecer antes da escolha; e uma **legenda dos códigos** numa linha no fim do bloco 6. A densidade de ids não muda: é a decisão de P-13 (ids entre parênteses, porque é assim que se responde com `/answer`) — a legenda é a resposta a essa queixa.

**`/round business` em `pricing-marinha-pilot-3-val-c`** (R-04 → R-05, `round-business-val-c-R05.md`): primeira chamada `/round <lens>` — F06 não interfere. A lente leu o enquadramento (C-157..C-161) contra as suas linhas e escreveu **3 rows**: `C-162 was X-009` (a contradição sobre o que se perde antes de 4ª feira fecha pela declaração do dono em `enquadramento.md#M-5` — volume não entra), `A-053` (o caso de negócio só é quantificável prospectivamente: C-145 + R-021 + M-5) e `U-086` (em que resultado cai a diferença valorização vs apurado — cita M-5, duas respostas com diferença no requisito). Árbitro: U-086 passa (i)–(iii); C-162 tem locator de classe 4 e não excede a declaração. Motor: R-05 `criadas 1 · fechadas 0 · abertas 40 (9 graves)` → **sem convergência** — correcto e visível: o fecho de X-009 é de uma `Conflicted`, não conta como pergunta fechada (o output diz isso). Tensões entregues a `financial` (A-021 sem base após M-5; metade «toneladas» de U-033 sem `M-n`). Output: 5 linhas, **0 violações**.

## 5. O que fica por medir, e achados fora do âmbito

- **Não houve leitor humano.** Os três leitores são modelos no papel de quem não construiu. É o análogo honesto do protocolo (§6.3, subagentes isolados), não o teste de leitura humano que P-13 pede; esse fica para o primeiro utilizador real, com o ficheiro de evidência como controlo.
- **`funding_gate` marcou U-033 pela palavra «ROI»** no texto do `swing` — é uma pergunta de volume/margem, não de orçamento. Falso positivo do detector de P-4 (frente A, `dashboard.py`); registar para a frente E (higiene do motor), não corrigido aqui.
- **Árbitro: 21 de 39 perguntas abertas sem declaração de divergência** (`arbiter.sem_declaracao`) — todas anteriores à regra de P-1, à excepção de U-083/U-084 (R-04). O `/round` só reclassifica as da ronda corrente; o passivo fica visível no `/status` (linha nova do bloco 6) até uma passagem completa.
- **Disposições das etiquetas de §4**: a verificação por presença de string que fiz para o output do `/round` é heurística sobre `` `…` `` inline e não é prova; o motor ainda não carrega essa contagem (fica com P-15/E, como o plano já previa).
- **Um teste de skill pinava o inglês do output** (`test_options_semantics_unchanged`: «option class»; `FS_FramingSurvival`: «What must survive into Options (projection of SU ids»). Resolvido preservando os nomes de contrato **em prosa** ao lado do bloco traduzido — o contrato mantém o nome, o utilizador lê a tradução. Nenhum teste anterior foi enfraquecido.
- **`CLAUDE.md` levava uma alteração não commitada do owner** (regra INVIOLÁVEL das perguntas por `AskUserQuestion`), anterior a esta sessão; vai no commit de P-13 por ser o mesmo ficheiro e a mesma direcção.
- **Deslocamentos que P-13 não pedia e ficaram**: `aisa-frame` pede a validação da frase por `AskUserQuestion` (era prosa «yes/edit»); `aisa-decide` aponta para `/blueprint` antes de `/render` (apontava directo para `render`); o `/status` deixa de imprimir «Tripwires» antes de existir decisão.

## 6. Fecho

Frente C **congelada**. Commits: P-13 (glossário, `CLAUDE.md`, 15 skills, `resume`, `dashboard.py` 1.5.0, teste), P-14 (`aisa-orient`, `aisa-start`, `COMO-USAR.md`), validação (evidência + este passo). Suite completa **859/859** verde (20 testes novos em `test_user_language.py`); aceitação determinística 90 → 0 · 13 → 0 · página 0 · COMO-USAR 0; outputs reais 0 (`/status`, `/round`, 3 runs de orientação, 1 rerun de reorientação) e 1 (o `why` do motor, corrigido a seguir).

Frentes seguintes, pela ordem do plano: **E** (P-15 a P-18) — continua a bloquear a validação lente a lente de A e o desenho de A5, e recebe daqui o falso positivo de `funding_gate` e a contagem de disposições; **D** fica por último, com o veredicto de P-11 (step-9d §1.2) e os três achados de conteúdo à sua espera.
