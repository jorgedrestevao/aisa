# Step 9B — Frente A (Discovery), parte 1 — fecho da onda 0 na SU e prosa do kernel e das skills

> Segundo passo da frente A do plano consolidado (`docs/CONSOLIDATED_PLAN.md` §5). Duas coisas, e só duas:
> (1) aplicar à SU real de `projects/pricing-marinha-pilot-3` o que o step-9a mediu, bloco a bloco, com validação do dono;
> (2) escrever a **prosa** de P-0, P-1, P-2, P-3, P-4 e P-12 nos ficheiros da frente A — um commit por correcção.
> Nenhum código Python (sessão Opus 5 separada), nenhuma lente correu (sessão de validação separada). Modelo: Fable 5.1 (§5.1).

**Veredicto: `STEP 9B — FRENTE A, PROSA: 6 COMMITS, SU DE PILOT-3 ACTUALIZADA PELO MOTOR — CÓDIGO E VALIDAÇÃO PENDENTES`.**
Sem tag de freeze: só depois da validação (`/round` em cópia).

---

## 1. Base

| | |
|---|---|
| Checkpoint de partida | `0006161` (branch `pp-pack-authoring/step-2-discovery-layer`) |
| Checkpoint de chegada | `c69d5c7` (P-12) — seis commits, listados em §4 |
| Engagement | `projects/pricing-marinha-pilot-3` — fase `discovery`, ronda `R-04`, pack `pp`. Fora do repo (`projects/*` em `.gitignore`): as alterações à SU não são commit, são registo no `council-log.md` e aqui |
| Motor, antes | `dashboard.py --json` (1.1.0, schema 2): abertas C156 A28 U41 X1 R25 · resolvidas C0 A1 U44 X8 R9 · swing abertas 8 decisivo / 31 dimensionante / 2 cosmético · 40 rows `USER_ANSWER` sem `answers.md#` |
| Motor, depois | abertas **C141 A49 U39 X1 R25** · resolvidas **C20 A1 U46 X8 R9** · swing abertas **1 / 24 / 14** · **0** rows `USER_ANSWER` sem âncora · facetas `ronda` ganham `R-00`, `lens` ganha `enquadramento` · 0 diagnostics · saúde 100 % |
| Perguntas de julgamento ao dono | 9, todas por `AskUserQuestion`: 5 blocos (0a–0e) + 3 decisões (Bloco 1) + `funding_gate` de pilot-3 |
| Não tocado | `library/kernel/tools/*.py` · `.claude/hooks/` · `settings.json` · `dashboard.py` · `aisa-status` · `chairman-synthesis` · `aisa-capture` · `aisa-frame` · templates |

Definições (kernel entre parênteses): **regra de negócio declarada pelo dono** (`M-n`, `enquadramento.md`); **facto confirmado** (`Confirmed`); **interpretação com base** (`Assumed`); **pergunta aberta** (`Unknown`); **alcance da resposta** (`swing`: `decisivo` / `dimensionante` / `cosmético`); **âncora** = locator `answers.md#<secção>`.

---

## 2. Bloco 0 — fecho do step-9a na SU real

Cada bloco validado pelo dono antes de escrever. **Nenhum recusado.** Nenhuma row apagada. Contagens só pelo motor.

| Bloco | Acção | Quantidade | Resultado (motor) |
|---|---|---|---|
| 0a | 5 rows `Confirmed` R-00 (M-1..M-5), `lens = enquadramento`, evidência `enquadramento.md#M-n`, validade organizacional | 5 | C-157..C-161; faceta `ronda` = R-00..R-04 |
| 0b | 19 transições `A-nnn was C-nnn` da lista final do step-9a §5 (11 *acima da evidência*, 8 *sem dono*); originais `— resolved → A-nnn` | 19 | A-030..A-048; invariante 156+29 = 185 → 136+1+48 = 185 (136 Confirmed abertas sem as M-n, C-010 superada, 47+1 Assumed) |
| 0c | Marcador em C-010 (superada por C-100) | 1 | `— resolved → C-100` — o marcador sancionado em `states.md`; o precedente local `superseded →` (C-051, A-024) é invisível ao motor e não foi seguido |
| 0d | 21 mudanças de alcance da tabela §4 do step-9a: 7 `decisivo → dimensionante` (sem referente), 12 `dimensionante → cosmético` (sem divergência no to-be), 2 `Unknown → Assumed` (U-022 → A-049, U-023 → A-050) | 19 edições + 2 transições | swing abertas 8/31/2 → 1/24/14; U abertas 41 → 39; a razão fica na célula (`reclassificado P-1 (step-9b)`); criticidade intocada — U-044 fica *Critical + cosmético* |
| 0e | Âncora `answers.md#<secção>` em todas as rows `USER_ANSWER` sem ela | 40 | 32 declarações do dono (28 ainda `Confirmed`, 4 transitadas em 0b) + 8 resoluções internas (todas transitadas em 0b). Mapa: BLOCO-A 3 · B 1 · C 3 · D 2 · E 3 · F 1 · G 4 · H 4 · I 6 · CONFLITOS 5 · RISCOS-FECHADOS 4 · X-001 1 · X-003 1 · MANUTENÇÃO-DE-PREMISSAS 2 |

Mapeamento 0b (para o `/status` e o `/frame` lerem): C-003→A-030 · C-021→A-031 · C-087→A-032 · C-094→A-033 · C-097→A-034 · C-101→A-035 · C-106→A-036 · C-111→A-037 · C-126→A-038 · C-132→A-039 · C-133→A-040 · C-134→A-041 · C-135→A-042 · C-147→A-043 · C-148→A-044 · C-152→A-045 · C-154→A-046 · C-155→A-047 · C-156→A-048.

Correcção ao step-9a §5: o número "32 sem âncora" contava só as declarações do dono; as 8 resoluções internas (C-094, C-126, C-132..C-135, C-155, C-156) também eram `USER_ANSWER` sem âncora — 40 no total. Todas completadas.

Ficam sem locator das quatro classes, **pendentes para a sessão do hook**: C-002 (`context.json.literal_request` — aceite como excepção em `states.md` regra 1) e C-026 (contagens do extractor sem célula — completar com `.extraction.json#<folha>`). Os dois locators de validação (C-107 ← C-144, C-033 ← C-090) **não foram aplicados**: a regra 5 de P-12 já os cobre em prosa, mas a edição de evidência sancionada agora escrita (terceira edição) fala em *completar* a âncora da fonte já nomeada, não em acrescentar uma validação posterior — decidir na validação se é a mesma classe de edição.

Registo: `projects/pricing-marinha-pilot-3/council-log.md`, secção *"R-00 / R-04 — fecho da onda 0 (step-9b, frente A) — 2026-09-08"* + parágrafo *P-4*.

**Saiu:** SU de pilot-3 com enquadramento, 21 reclassificações, 40 âncoras, 19 rebaixamentos honestos.
**Muda para as lentes:** na próxima ronda encontram M-1..M-5 como rows, 14 perguntas marcadas *não gastar reunião*, e uma coluna `decisivo` com 1 pergunta em vez de 8.
**Falta:** `/round` em cópia (validação); hook e faceta `sem locator` (código).

---

## 3. Bloco 1 — três decisões que a onda 0 abriu (dono, 2026-09-08, `AskUserQuestion`)

| # | Tema | Decisão | Onde ficou escrita |
|---|---|---|---|
| 1 | **P-1 × P-4** — custo as-is é `cosmético` pela regra de P-1 e mandato por P-4 | **Baseline por `Assumed`; `Unknown` só com referente.** P-1 mantém as três diferenças (requisito · forma dos dados · esforço do to-be). O custo as-is, o custo de não fazer e o custo de atraso são a *baseline* da lente financeira, escritos como `Assumed` com base (mandato P-4), não perguntados. Uma `Unknown` de custo é `decisivo` só se nomear o branch que a magnitude elimina ou mantém vivo (tipicamente `do nothing` — que é opção em Options, logo o kernel já cobre o caso sem quarta diferença), `dimensionante` se muda esforço ou forma dos dados do to-be, senão `cosmético` — incluindo quando a decisão de construir já está tomada (pilot-3: C-112/C-113). Consequência em pilot-3: U-010, U-030, U-032, U-072 ficam `cosmético` | `states.md` → *Question economics* → *Cost questions* · `lens-financial` step 2 · `cfo-lens.md` |
| 2 | **Âncoras** — aceitação 2 de P-12 previa 5 avisos do hook; o real eram 40 | **`aisa-answer` passa a escrever a âncora; as 40 completam-se agora.** Regra da âncora: primeiro segmento do título da secção antes de « — », espaços → hífens (`answers.md#U-073`, `answers.md#BLOCO-H`). Implica uma **terceira edição sancionada** em `states.md`: completar o locator da evidência de uma row cuja evidência já nomeia a fonte, sem tocar no claim, em lote registado no `council-log.md`. Aceitação 2 reescrita (§5) | `states.md` → *Confirmed threshold* regra 1 + *Append rule* · `aisa-answer` steps 3–4 |
| 3 | **M-1 canónico** — o plano tinha o texto antigo | **`enquadramento.md` passa a canónico**; §3 P-0 do plano recebe o texto corrigido pelo dono (referência; custo real fecha na 2ª feira seguinte; semana N valorizada à média de N-1) e a nota de origem | `CONSOLIDATED_PLAN.md` §3 P-0 |

Mais uma declaração do dono, pedida por P-4: **`funding_gate = false`** em pilot-3 — a decisão de avançar não depende de aprovação orçamental de terceiros. Escrito em `context.json`; registado no `council-log.md`. É declaração, não inferência de C-131/A-001.

---

## 4. Bloco 2 — prosa, um commit por correcção

Só ficheiros da coluna *Ficheiros* da frente A (§5 do plano), mais `cfo-lens.md` por indicação explícita do dono em P-4. Prosa em inglês, como os ficheiros; termos do kernel inalterados.

| P | Commit | Ficheiros | O que saiu | O que muda para as lentes | O que falta |
|---|---|---|---|---|---|
| **P-0** | `fb64021` | `aisa-start` · `aisa-round` · `phases.md` · `states.md` | Step 4d *Enquadramento* (entrevista `AskUserQuestion`, uma pergunta por tema, verbatim, sem inferir do pedido nem do `_capture`, sem vendor) e step 9b (escreve `enquadramento.md` + rows R-00). `aisa-round` 3.6d resolve o ficheiro e passa-o na invocação, ou a linha explícita *"no enquadramento"*. `phases.md`: entry criteria soft; Framing confirma ou corrige cada `M-n` por `was C-nnn`. `states.md`: lens `enquadramento` e ronda `R-00` legítimas, hipótese do dono, nunca editada | Recebem M-1..M-n como ids na invocação e têm de citar o que cada pergunta serve | `dashboard.py` reconhecer `R-00`/`enquadramento` no `/status` (já aparecem nas facetas do JSON; falta a apresentação) |
| **P-1** | `9e775b8` | 6 `lens-*` · `aisa-round` · `states.md` | Hard rule 7 nas seis lentes (cita `M-n` **ou** `swing` com ≥ 2 respostas e diferença no to-be; diferença só no as-is não conta; inferível com base → `Assumed`; `decisivo` exige referente) e step 5 alinhado. `aisa-round` 5f: árbitro de ronda em prosa — só `Unknown` desta ronda, três verificações de presença, reclassificação = edição de metadados sancionada (classe `/simulate`), nunca apaga, nunca julga materialidade, nunca toca criticidade; contagem no output. `states.md` *Question economics*: teste de divergência, referente obrigatório, árbitro sancionado, **decisão 1** (*Cost questions*) | Cada `Unknown` nova tem de declarar por que existe; o orquestrador reclassifica o que não declara | Suporte determinístico do árbitro em `dashboard.py` (presença de `M-n`/≥2 respostas é string-checkable) |
| **P-2** | `8ab6c73` | `aisa-round` · `phases.md` | Step 5g *Convergência*: criadas · fechadas · abertas · Critical abertas, só do motor (chave `round_delta`; até existir, imprime o que o JSON expõe e diz `pendente`, nunca estima); `criadas > fechadas` → `sem convergência`, visível, não bloqueante; linha no output. `phases.md` exit criteria soft: última ronda com criadas ≤ fechadas | Nenhuma — é reporte do orquestrador | `round_delta` em `dashboard.py`; a mesma linha em `aisa-status` (fora dos ficheiros desta sessão) |
| **P-3** | `87e5129` | `orchestration.md` | *Material semantic disposition* ganha o teste de conteúdo: `PM-U` de mecânica do artefacto (protecção, folhas escondidas, formatos, named ranges, contagens, ordem de recálculo) só `ADOPT` se a lente declarar que forma, volume ou regra dos dados do to-be muda; senão `DISMISS — mecânica do as-is`, com razão; o inventário L1 continua fonte de rascunho de campos em Architecture (P-6); Critical dispensada continua a ser disposição | Deixam de subir `PM-U` de protecção/formato como `Unknown` | Classe determinística `mecânica \| dados \| processo` na `PM-U` gerada por `aisa-capture` (código) |
| **P-4** | `4ec644b` | `aisa-start` · `aisa-round` · `lens-financial` · `cfo-lens.md` | Step 4e do `/start` pergunta *"A decisão de avançar depende de aprovação orçamental de terceiros?"* → `context.json.funding_gate` (ausente = `true`). `aisa-round` passa a flag verbatim. `lens-financial`: cues `budget_envelope`, `capex_opex`, `funding_model`, `payback_roi` só com `true`; mandato permanente em `as_is_cost`, `do_nothing_cost`, `cost_of_delay`, `cost_sensitivity` + *o que o negócio faz hoje sozinho e passaria a depender de fila* (o caso de U-071); custo as-is como `Assumed` de baseline; `Unknown` de custo só com referente. `cfo-lens.md` lê a mesma flag; com `false` o frame tem de ser **enunciado** com base, não monetizado | Lente financeira com `false`: zero perguntas de envelope, limiar, CAPEX/OPEX, imputação | `chairman-synthesis` não exigir monetização do frame com `false` (fora dos ficheiros desta frente); aceitação em cópia (`/round financial` sem envelope) |
| **P-12** | `c69d5c7` | `states.md` · 6 `lens-*` · `aisa-round` · `aisa-answer` · `orchestration.md` | `states.md`: linha `Confirmed` e decision rule reescritas; secção nova **Confirmed threshold** (regras 1–5: quatro classes de locator incl. `answers.md#<secção>`/`enquadramento.md#M-n` e regra da âncora; claim ao nível da evidência; confirmação humana só do dono ou autoridade nomeada; `[ÂMBITO AUTORIZADO]` para factos do engagement; `X-`/`R-` por evidência interna → `Assumed`; *industry-standard claim* sai de `Confirmed`; `Assumed → Confirmed` exige locator da validação); transições `Conflicted → Assumed` e `Risky → Assumed`; *Append rule* com a **terceira edição sancionada** (decisão 2) e "reclassificar Confirmed acima da evidência é transição, não edição". 6 lentes: Hard rules 2 e 3 reformuladas. `aisa-round` 5f: segunda leitura das `Confirmed` novas (sem locator → aviso; acima da evidência → `A was C`). `aisa-answer`: `--source` default *dono do processo*; inferência de estado pelo limiar; âncora `answers.md#<id>` obrigatória na evidência; resolução por evidência interna → `Assumed was X/R`; hard rule 3 alargada. `orchestration.md`: `OBSERVED → Confirmed` só com locator e ao nível; ponteiro para o limiar | Nenhuma `Confirmed` sem locator; afirmação acima da evidência passa a `Assumed` no momento de escrever | Hook `su-confirmed-guard.py` + `settings.json` + faceta `sem locator` em `dashboard.py` (código); calibrar falsos positivos em `dpt-galp-jp` e `cae-automation` |

Ficheiros tocados no total: `library/kernel/states.md`, `phases.md`, `orchestration.md` (via scratchpad + `cp` + commit); `.claude/skills/aisa-start`, `aisa-round`, `aisa-answer`, `lens-{business,operations,user,data,governance,financial}/SKILL.md`; `.claude/agents/cfo-lens.md`.

---

## 5. O que fica para as duas sessões seguintes

**Sessão Opus 5 — código** (§5.1 do plano, fast mode aceitável):

1. `dashboard.py`: `round_delta` no JSON (criadas / fechadas / abertas / Critical abertas por ronda) — P-2; faceta `sem locator` (presença de locator das quatro classes + existência do alvo) — P-12; apresentação de `R-00` e `lens = enquadramento` no `/status` — P-0 (as facetas já os expõem).
2. `su-confirmed-guard.py` (novo, `PostToolUse` sobre Write/Edit em `shared-understanding.md`, ao lado de `on-su-change.py`, nunca bloqueia) + entrada em `settings.json` — P-12. Calibrar em `dpt-galp-jp` e `cae-automation` antes de ligar.
3. Suporte determinístico ao árbitro de ronda (presença de `M-n` ou ≥ 2 respostas no `swing`) — P-1, se se quiser mais do que prosa.
4. `aisa-capture`: classe `mecânica | dados | processo` na `PM-U` gerada (string determinística a partir da origem do sinal) — P-3.
5. `aisa-status`: linha de convergência e faceta `sem locator` lidas do JSON — P-2/P-12 (ficheiro fora da coluna desta sessão).
6. `chairman-synthesis`: não exigir monetização do frame com `funding_gate = false` — P-4 (idem).
7. C-026: completar `.extraction.json#<folha>`; confirmar a excepção de C-002 no hook.

**Sessão de validação — `/round` em cópia de pilot-3** (modelo de produção; até ser decidido, Fable 5.1 **e** Opus 5, ≥ 3 runs por lado, registar a diferença — §5.1 nota):

- P-0: nenhuma `Unknown` nova pergunta o porquê da exposição de 2ª/3ª; as de *como* citam M-2/M-4.
- P-1: toda a `Unknown` nova tem as três declarações ou foi reclassificada com registo; U-070 fica `cosmético` (já está).
- P-2: `criadas ≤ fechadas` na ronda; números batem com `dashboard.py --json`.
- P-3: nenhuma `PM-U` Critical desaparece sem disposição; PM-U-026 (protecção) `DISMISS — mecânica`, PM-U-003 continua a subir.
- P-4: `/round financial` com `funding_gate = false` não gera `Unknown` de envelope/limiar/imputação.
- P-12: nenhuma `Confirmed` nova sem locator; toda a conclusão de cadeia entra como `Assumed`; invariante Confirmed+Assumed inalterado pela reclassificação.
- Decidir se o locator de validação (C-107 ← C-144, C-033 ← C-090) é a mesma classe da terceira edição sancionada.

Só depois: tag de freeze e `validado` no quadro de §5 do plano.

---

## 6. Regras cumpridas

- Contagens só pelo motor (`dashboard.py --json`, antes e depois de cada bloco). Nenhuma contagem manual entrou neste ficheiro.
- `library/` editada só por scratchpad + `cp` + commit (hook de runtime não foi contornado). Nenhum Python do kernel tocado.
- 9 perguntas de julgamento por `AskUserQuestion`; nenhum bloco aplicado sem validação; nenhum recusado.
- Nenhuma row apagada; reclassificações de estado são transições append-only; edições a rows existentes limitam-se às três classes sancionadas (marcador `resolved →`, `swing` classe, âncora de evidência).
- Nenhuma lente correu. Nenhuma tag criada.
- Modelo: Fable 5.1 em toda a sessão (§5.1 — prosa do kernel).

Quadro *Estado por correcção* em `CONSOLIDATED_PLAN.md` §5: P-0, P-1, P-2, P-3, P-4, P-12 → `em curso (step-9b) — prosa commitada; código e validação pendentes`.
