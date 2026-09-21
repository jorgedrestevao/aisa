# Step 9C — Frente A (Discovery), parte 2 — código

> Terceiro passo da frente A do plano consolidado (`docs/CONSOLIDATED_PLAN.md` §5). Uma coisa só:
> escrever o **código** que obedece à prosa commitada no step-9b. Nenhuma edição de prosa em
> `states.md`, `phases.md`, `orchestration.md` ou nas seis lentes; nenhuma lente correu.
> Modelo: Opus 5 (§5.1 — "código com critério fechado; fast mode aceitável").

**Veredicto: `STEP 9C — FRENTE A, CÓDIGO E VALIDAÇÃO: 29 COMMITS, MOTOR 1.4.0, HOOK LIGADO E DISPARADO EM PRODUÇÃO, 6/6 CORRECÇÕES VALIDADAS (P-2 no mecanismo), DUAS REGRAS NOVAS NO KERNEL`.**
**Congelado na tag `step-9c-frente-a`.** Perfil de modelo decidido pelo dono (Discovery em Sonnet 5, council em Opus 5 — §5.2.4, com a ressalva do `n = 1` escrita); quinta classe de prova (§5.4), determinismo do motor (§5.3) e correcção pela prova (§5.5) fechados. Fora da frente e por fazer: o perfil em `pack.yaml`, e um parser de `PM-U` no motor (§5.3). A validação **correu** nesta sessão — R-05 em duas cópias, esforço `high` dos dois lados (§5.2), o que era um passo separado no plano original.

---

## 1. Base

| | |
|---|---|
| Checkpoint de partida | `c69d5c7` (fim do step-9b) |
| Checkpoint de chegada | `82990c4` — dez commits, listados em §2 |
| Motor, antes | `dashboard.py` 1.1.0 (schema 2) |
| Motor, depois | `dashboard.py` **1.2.0** (schema 2 inalterado — só se acrescentam chaves) |
| Engagements usados | `pricing-marinha-pilot-3` (referência) · `dpt-galp-jp` e `cae-automation` (calibração). Cópias reais, nunca fixtures |
| Contagens | só por `python library/kernel/tools/dashboard.py --engagement <slug> --json <ficheiro>`, antes e depois de cada item |
| Perguntas de julgamento ao dono | 5, todas por `AskUserQuestion` (§4) |
| Não tocado | `states.md` · `phases.md` · `orchestration.md` · as 6 `lens-*` · `xlsx_extract.py` · `text_extract.py` |

Definições (kernel entre parênteses): **prova localizável** (locator das quatro classes de
`states.md` regra 1); **facto confirmado** (`Confirmed`); **interpretação com base** (`Assumed`);
**pergunta aberta** (`Unknown`); **convergência** (`criadas ≤ fechadas` numa ronda);
**enquadramento** (`R-00`, rows `M-n`).

---

## 2. Commits

| # | Commit | P | O que saiu | O que muda | O que falta |
|---|---|---|---|---|---|
| 1 | `1279f00` | P-2 | `round_delta` no JSON: por ronda, `criadas` · `fechadas` · `sem_convergencia`; `abertas` e `critical_abertas` correntes. Data de fecho = ronda da row destino do marcador `resolved →`; em alternativa, a data do destino quando identifica uma ronda única; nenhuma das duas → entra em `indeterminadas` e não conta em ronda nenhuma | `/round` e `/status` passam a ter número real de convergência | — |
| 2 | `e7f5fab` | P-12 | `confirmed_locator` no JSON: `locator_classes()` (presença das quatro classes, forma canónica **e** capture-lite), `evidence_targets()` (o que o engagement tem), `locator_target_gaps()` (o alvo só é verificado quando o ficheiro pertence ao span do próprio locator), `audit_confirmed_locators()` com `only_ids` para o hook | Um facto sem prova localizável deixa de ser invisível | Ver o comportamento numa ronda real |
| 3 | `3321ff8` | P-0 | Bloco `enquadramento`: invariantes `M-n` lidos do ficheiro com as rows que cada um ancora; faceta `lens_producao` (as seis lentes, sem `enquadramento`); rótulos `R-00 · enquadramento` e `enquadramento (dono)` nos filtros da página | `R-00` deixa de poder ser lida como quinta ronda de lentes | — |
| 4 | `0e086e9` | P-1 | `arbiter` no JSON: por `Unknown` aberta, presença de citação de `M-n` ou de um `swing` que nomeia ≥ 2 respostas; os dois regex vão no JSON; `sem_coluna_swing` separa o caso das SU pré-v2.3 | O árbitro do step 5f recebe a lista; continua a ser ele a decidir | — |
| 5 | `1571476` | — | `TOOL_VERSION` 1.1.0 → **1.2.0**. Schema 2 mantém-se | — | — |
| 6 | `684bff8` | P-12 | `su-confirmed-guard.py` (novo) + entrada em `settings.json` + linha em `HOOKS.md`. `PostToolUse` sobre Write/Edit em `shared-understanding.md`, ao lado de `on-su-change.py`; importa `audit_confirmed_locators()` — o regex não é duplicado; nunca bloqueia, exit 0 sempre | Um facto sem prova localizável avisa no momento da escrita e fica no registo do council | Ver disparar numa ronda real |
| 7 | `be4ae20` | P-2/P-12/P-0 | `aisa-status`: linha de convergência, linha de factos sem prova localizável, e `R-00` reportada como enquadramento (dono) | O `/status` diz o que falta sem recontar nada | — |
| 8 | `7b5a1f4` | P-2 | `aisa-round` step 5g lê `round_delta` em vez de imprimir `pendente` | — | — |
| 9 | `025a99a` | P-3 | Coluna `classe` (`mecânica \| dados \| processo`) no §6 do template do modelo de processo + a regra determinística em `aisa-capture` | O teste de conteúdo de `orchestration.md` fica verificável | — |
| 10 | `82990c4` | P-4 | `chairman-synthesis` hard rule nova: com `funding_gate = false` o slot `costs <Z> today` é **enunciado com base, não monetizado**; nunca inventar número, nunca marcar o frame incompleto por falta dele | Lente financeira e frame deixam de exigir envelope onde ele não decide nada | Aceitação em cópia |

Ficheiros tocados: `library/kernel/tools/dashboard.py` · `library/kernel/capture-templates/process-model.template.md` (via scratchpad + `cp` + commit) · `.claude/hooks/su-confirmed-guard.py` (novo) · `.claude/hooks/HOOKS.md` · `.claude/settings.json` · `.claude/skills/{aisa-status,aisa-round,aisa-capture,chairman-synthesis}/SKILL.md`.

---

## 3. Calibração do hook (P-12, aceitação 2)

Regra medida: presença de um locator das quatro classes de `states.md` regra 1 **e** existência
do alvo. Aviso, nunca bloqueio; não julga se a afirmação está ao nível da evidência.

### 3.1 Avisos por engagement, antes das correcções

| Engagement | `Confirmed` abertas | Com prova localizável | Excepção | Sem locator | Alvo não abre | Veredicto |
|---|---|---|---|---|---|---|
| `pricing-marinha-pilot-3` | 141 | 128 | 1 (`C-002`) | 8 | 5 | **13 verdadeiros positivos, todos accionáveis** |
| `dpt-galp-jp` | 44 | 0 | 0 | 44 | 0 | **44 verdadeiros positivos, nenhum accionável** |
| `cae-automation` | 33 | 0 | 0 | 33 | 0 | **33 verdadeiros positivos, nenhum accionável** |

### 3.2 Classificação, aviso a aviso

| Grupo | Ids | Verdadeiro / falso positivo | Decisão |
|---|---|---|---|
| Contagens e estrutura do extractor sem ponteiro para dentro da extracção | `C-004` `C-014` `C-018` `C-026` `C-103` `C-105` | **verdadeiro** — a regra 1 manda citar `.extraction.json#<folha>` | Âncora completada (§3.3) |
| Protecção de folha que nenhuma extracção do engagement carrega | `C-015` `C-029` | **verdadeiro** — a fonte (`63fdaf78`) não está em `inputs/` | Transição para interpretação com base (`A-051`, `A-052`) |
| Âncora de `answers.md` com a data colada ao fragmento | `C-112` `C-113` `C-117` `C-119` `C-123` | **verdadeiro** — a referência não abre | Âncora corrigida |
| Pedido literal do dono na entrada | `C-002` | **excepção aceite** pela regra 1, não lacuna | Mantém-se `Confirmed`; o hook aceita-a (testado) |
| Engagements anteriores à regra | 44 + 33 | **verdadeiros pela regra, não accionáveis** — nenhum tem âncora de nenhuma classe porque a regra não existia | Não se corrigem. O hook só olha rows novas ou alteradas por escrita, logo nunca os reavalia |

**Zero falsos positivos** depois de duas correcções feitas durante a calibração, ambas de
desenho e não de dado: (i) a célula passou a aceitar a forma `$` (`Inputs!$DU$9`,
`'Market View'!B:F`) — sem ela, `C-017`, `C-022`, `C-031` e `C-041` caíam sem razão;
(ii) o nome de ficheiro só é verificado quando pertence ao span do próprio locator — sem
isso, um caminho citado em prosa (o `external_links` de `C-031`) e um nome de ficheiro com
espaços (`Pricing Marinha _ Kick-off.vtt` citado como `kickoff`) davam alvo inexistente.

### 3.3 pilot-3 depois das correcções

| | Antes | Depois |
|---|---|---|
| `Confirmed` abertas | 141 | 139 |
| Com prova localizável | 128 | **139** |
| Avisos | 13 | **0** |
| `Assumed` abertas | 49 | 51 |
| `Confirmed + Assumed` abertas | 190 | **190** (invariante cumprido) |
| Rows apagadas | — | **0** |

Registo completo em `projects/pricing-marinha-pilot-3/council-log.md`, secção *"R-04 — fecho de
locators (step-9c, frente A / código) — 2026-09-08"*: as seis âncoras completadas com o que foi
verificado contra cada extracção, as cinco corrigidas, e as duas transições com a razão.

Uma divergência ficou **anotada, não corrigida**: `C-026` diz "`Inputs` 1 461 linhas de dados";
a extracção tem 357 (Janeiro) e 172 (Agosto) linhas de dados — o número é a extensão do
intervalo dos named ranges (`Inputs!$9:$1469`). A nota está na evidência da row; o claim não
foi tocado.

### 3.4 Testes do hook (cópia de pilot-3, `_capture` e `answers.md` reais)

| Caso | Esperado | Obtido |
|---|---|---|
| `Edit` que toca `C-026` (sem locator) | 1 aviso + 1 linha no registo | ✓ |
| O mesmo `Edit` outra vez | aviso, **sem** duplicar a linha | ✓ |
| `Edit` que toca `C-001` (com locator) | silêncio | ✓ |
| `Write` (substitui o ficheiro) | avalia todas as abertas e **di-lo** no âmbito | ✓ 13 avisos, âmbito declarado |
| Escrita noutro ficheiro do engagement | silêncio | ✓ |
| `Edit` que toca `C-002` | silêncio (excepção) | ✓ |
| `Write` sobre pilot-3 depois das correcções | silêncio | ✓ |

### 3.5 Estado de `settings.json`

**Ligado.** `python .claude/hooks/su-confirmed-guard.py` entra no grupo `PostToolUse` /
`Write|Edit`, logo a seguir a `on-su-change.py`. Razão da decisão do dono: o hook só avalia
rows novas ou alteradas por escrita, por isso os 77 avisos não accionáveis dos dois engagements
anteriores à regra nunca chegam a aparecer; e `pilot-3`, o engagement vivo, está a zero.
O hook suporta `MultiEdit` no código, mas o `matcher` partilhado é `Write|Edit` — não foi
alargado para não mexer no gatilho dos outros três hooks do grupo.

---

## 4. Perguntas de julgamento (dono, 2026-09-08, `AskUserQuestion`)

| # | Tema | Decisão |
|---|---|---|
| 1 | A regra apanha 8 rows do extractor, não 1 | **Completar a folha nos 8.** O item 3e passa de uma row para oito; a regra fica como está escrita |
| 2 | Ligar o hook com 77 avisos não accionáveis nos engagements antigos | **Ligar.** O hook só vê rows novas ou alteradas |
| 3 | 5 âncoras de `answers.md` com a data colada | **Corrigir agora**, mesma edição sancionada |
| 4 | `C-015`/`C-029`: a fonte da protecção não está no engagement | **Passar a interpretação com base** (`A-051 was C-015`, `A-052 was C-029`) — não é âncora a completar, é transição |
| 5 | `C-026`: o número de `Inputs` não sai de nenhuma extracção | **Ancorar a Janeiro e anotar** a divergência, sem tocar no claim |

---

## 5. O que fica para a sessão de validação

`/round` em cópia de `pricing-marinha-pilot-3`, no modelo de produção (§5.1 do plano — enquanto
não estiver decidido, Sonnet 5 **e** Opus 5, com os critérios distintos que a nota do plano
fixa). Aceitações abertas:

- **P-0** — nenhuma `Unknown` nova pergunta o porquê da exposição de 2ª/3ª; as de *como* citam `M-2`/`M-4`. `/status` mostra `R-00` como enquadramento (dono).
- **P-1** — toda a `Unknown` nova tem as três declarações ou foi reclassificada com registo; a lista `arbiter.sem_declaracao` da ronda nova é ≈ 0 (em pilot-3 hoje são 21 de 39, todas anteriores).
- **P-2** — `criadas ≤ fechadas` na ronda; o número do output bate com `round_delta`.
- **P-3** — `PM-U-026` sai `mecânica` e `PM-U-003` sai `dados` na próxima geração do modelo de processo (hoje a coluna existe no template, mas o `process-model.md` de pilot-3 é anterior); nenhuma `PM-U` Critical desaparece sem disposição.
- **P-4** — `/round financial` com `funding_gate = false` não gera `Unknown` de envelope/limiar/imputação; um `/frame` de teste enuncia o custo com base, sem monetizar.
- **P-12** — nenhuma `Confirmed` nova sem locator (o hook fica silencioso durante a ronda); toda a conclusão de cadeia entra como `Assumed`.
- Decidir se o locator de validação (`C-107` ← `C-144`, `C-033` ← `C-090`) é a mesma classe da terceira edição sancionada — ficou de fora outra vez, e continua a ser prosa, não código.

Só depois: tag de freeze e `validado` no quadro de §5 do plano.

### 5.1 Cópias preparadas e linha de base (2026-09-08)

Uma cópia por modelo candidato — a segunda ronda no mesmo engagement partiria de estado sujo.
`_state.json.engagement`, `context.json.engagement` e o título da SU reescritos para o slug novo;
`dashboard.html` regenerado do zero.

| | `pricing-marinha-pilot-3-val-sonnet` | `pricing-marinha-pilot-3-val-opus` |
|---|---|---|
| Fase / ronda | `discovery` / `R-04` | `discovery` / `R-04` |
| Rows abertas | C139 A51 U39 X1 R25 | C139 A51 U39 X1 R25 |
| Avisos de prova localizável | **0** | **0** |
| Invariantes do enquadramento | `M-1`..`M-5` | `M-1`..`M-5` |
| Última ronda (`round_delta`) | R-04 22 criadas / 33 fechadas · 39 abertas · 9 Critical | idem |
| Perguntas sem declaração (`arbiter`) | 21 de 39 | 21 de 39 |
| Saúde epistémica · diagnostics | 100 % · 0 | 100 % · 0 |

As duas linhas de base são idênticas por construção: qualquer diferença medida depois da ronda é
do modelo, não do estado de partida. A ronda a correr é `R-05`.

**Litter pré-existente, apagado:** `projects/pricing-marinha-pilot-3.31964.tmp` (2026-09-07) e
`.38772.tmp` (2026-09-08 11:08) eram JSON do motor 1.1.0 órfãos do padrão tmp → `os.replace` de
`_write_text()`, de execuções interrompidas anteriores a esta sessão. Inspeccionados e removidos
a pedido do dono. Nenhum era referenciado (`SKIP_SUFFIX` já os excluía do índice de artefactos).

**Uma nota de dado, não de código — corrigida.** O cabeçalho de
`projects/pricing-marinha-pilot-3/enquadramento.md` dizia que as rows `R-00` "ainda não estão na
SU"; estavam desde o step-9b. Nota actualizada com os cinco ids (`C-157`..`C-161`), o ponteiro
para o registo do bloco 0a e a regra de que são a hipótese do dono, corrigível por `/frame` com
`was C-nnn`. Nenhum invariante alterado, nenhum texto do dono tocado; linha no `council-log.md`.

### 5.2 Resultado da validação — R-05 nas duas cópias (2026-09-08)

Rondas corridas pelo dono, `/round` completo (seis lentes), **esforço `high` nos dois lados** —
igual de um lado e do outro, por isso a comparação é limpa. Leitura pelo script
`tools/compare-validation-round.py` contra a linha de base de §5.1, mais leitura humana de tudo
o que o script marcou `LER`.

| Aceitação | Sonnet 5 | Opus 5 | Cópia de captura |
|---|---|---|---|
| **P-0** enquadramento | passa | passa | passa |
| **P-1** teste de divergência | passa | passa | passa |
| **P-2** convergência | **passa** — 2 criadas / 2 fechadas | **falha** — 7 criadas / 0 fechadas | — |
| **P-3** classe da `PM-U` | não testável | não testável | **passa** |
| **P-4** `funding_gate` | passa | passa | passa |
| **P-12** prova localizável | passa (com incidente, ver §5.2.3) | passa | passa |
| Invariantes | passa | passa | passa |

**P-2, distinção que o quadro do plano tem de guardar:** o **mecanismo** passou nos dois lados —
detectou a não-convergência do lado Opus e etiquetou-a, que é exactamente o que P-2 pede. O que
não foi cumprido foi o **critério de saída** (`criadas ≤ fechadas`), e isso é comportamento do
modelo, não defeito do código.

**P-3** não era testável nas cópias das rondas: o modelo de processo não foi regenerado (nenhum
`/capture` correu nelas), logo a coluna `classe` não existia. Fechada numa terceira cópia,
`-val-capture`, com `/capture` run 4 sobre evidência byte-a-byte idêntica à run 3 —
`PM-U-026` → `mecânica`, `PM-U-003` → `dados`.

#### 5.2.1 O que a validação apanhou — quatro defeitos do código desta sessão

Todos da mesma família: **o motor codificou a forma que o autor esperava, não a forma que os
dados têm.**

| # | Commit | Defeito | Forma assumida | Forma real |
|---|---|---|---|---|
| 1 | `3d18a5d` | árbitro marcava `U-092` como pergunta sem declaração | `ou` · `vs` · `se … se` | `(a) … (b)` — o que as SU reais escrevem |
| 2 | `00e5649` | a regra da `classe` teria classificado `PM-U-026` como `processo`, **contra a própria aceitação de P-3** | "vem da síntese §4" | o §4 cita a `PM-U` só para registar a pergunta aberta; citação cruzada não é sinal |
| 3 | `00e5649` | a regra da `classe` anunciava-se determinística | mecânica nas 23 rows | mecânica em **6 de 23**; as outras nascem da síntese ou da entrevista e são julgamento com default |
| 4 | `00e5649` | o script de comparação nunca teria visto a coluna | `\| id \| question \|` (template, inglês) | `\| id \| pergunta \|` (dados, português) |

No defeito 1 o **árbitro humano-modelo tinha lido bem** e não reclassificou nada; a divergência
era do motor. É o caso limpo do princípio: o motor lista, o árbitro decide — e quando discordam,
não é automático que o motor esteja certo.

Dois erros de método do próprio autor, registados porque se repetem se não ficarem escritos:

- **Linha de base lida de um engagement vivo.** A primeira `baseline-val-R04.json` foi gerada das
  cópias quando estas já corriam R-05 (52 `Assumed` em vez de 51). Regenerada do original
  intocado. Toda a medição estampa o que leu (fonte, sha, ronda) e nunca lê de um alvo em voo.
- **Heredoc do Bash come `\b`.** Um patch escrito por heredoc transformou `\b` em backspace
  (0x08) dentro do regex do árbitro, o que fez a contagem *subir* de 21 para 36 sem erro visível.
  Os patches a `library/` vão por ficheiro escrito com Write, como a regra do projecto já dizia.

#### 5.2.2 O hook disparou em produção, e funcionou

Na cópia Sonnet, `C-162` e `C-163` nasceram com os locators na coluna do **claim**, não na coluna
da **evidência** — que é a única que o motor audita. O `su-confirmed-guard.py` avisou, escreveu as
duas linhas em `council-log.md`, e **o modelo corrigiu as duas rows na mesma ronda**, com
re-auditoria a `sem_locator: []`. Era o teste que faltava: o hook em condições reais, sobre rows
que acabaram de nascer, sem bloquear a ronda.

#### 5.2.3 As duas `Confirmed` que forçaram uma decisão de kernel

Os dois factos novos do lado Sonnet apoiavam-se em trabalho que o **executor** fez sobre a fonte
crua, não em nada que a extracção guardada contivesse: `C-162` (leitura de `Market View` agregada
por semana ISO em Python) e `C-163` (descompilação do VBA com `oletools`; a extracção deste
engagement nunca descompila VBA — `process-model.md` §7). Método declarado, reproduzível — e sem
nada guardado que se possa abrir.

**Decisão do dono** (`AskUserQuestion`, 2026-09-08): a extracção directa é prova legítima, **mas o
resultado tem de ficar escrito em `_capture/`** e a evidência apontar para lá; sem isso o alvo não
existe e a regra 1 do limiar de `Confirmed` não se cumpre. Regra futura: a lente vai à fonte crua
quando precisa, e escreve o que de lá retira em `_capture/`, com nome próprio.

Aplicada em `59009dc` (`tools/extract-direct.py`, determinístico, sha256 da fonte no cabeçalho de
cada artefacto):

| Artefacto | Suporta | Veredicto da prova |
|---|---|---|
| `PREÇO BANCAS_03_08_26.xlsm.market-view-weekly.json` | `C-162` | **confirma o claim**: 83 semanas com observação, min 2, max 5, média 4,83 por série (o claim dizia "83 semanas, de 2 a 5, média 4,82–4,86"). A 84.ª chave (`2026-W32`) é a linha final sem valores em cache, posterior à data do ficheiro — não é falha de série |
| `PREÇO BANCAS_03_08_26.xlsm.vba.md` | `C-163` | **confirma o essencial, contradiz um detalhe**: as duas rotinas de `Main.bas` estão lá e nenhuma toca cálculo de preço, mas os módulos são **11 no total** — `Main.bas` mais **dez** de código-behind, não onze |

Uma armadilha do caminho, que vale como aviso: a primeira versão do extractor contou **zero em
todas as séries**. O cabeçalho de `Market View` ocupa duas linhas e **não nomeia os instrumentos**
— os códigos (`#PUMFD00`, `#fxUSDEURECB`, …) só existem dentro das fórmulas do add-in. Aceitar o
primeiro resultado teria "refutado" um facto correcto. A coluna passou a ser resolvida pela
fórmula (`B` `#fxUSDEURECB` · `C` `#PUMFD00` · `D` `#AAWZC00` · `E` `#PUAAY00` · `F` `#AAYWS00`).

**Persistir a prova apanhou um erro numérico num facto já marcado como confirmado, com locator
aceite pelo motor e pelo hook.** A regra que o dono decidiu pagou-se na primeira aplicação.

#### 5.2.4 Os dois modelos fazem trabalho diferente — e nenhum contornou uma regra

| | Sonnet 5 (`high`) | Opus 5 (`high`) |
|---|---|---|
| `Unknown` criadas | 2 | 7 (4 `decisivo`, todas com ramo nomeado) |
| `Unknown` fechadas | 2 | 0 |
| `Confirmed` novas | 2 | 0 |
| `Assumed` novas | 5 | 5 |
| `Risky` novas | 1 (`R-035 was R-031`) | 2 |
| Regras não aplicadas (candidatos deterministas) | 0 | 0 |
| Regras contornadas (candidatos deterministas) | 0 | 0 |
| Convergiu | sim | não |

Sonnet **executou dois spikes** que estavam escritos com o critério "fecha por leitura, não por
declaração", em vez de os mandar para reunião: leu o Excel e descompilou o VBA, fechando `U-085`
e `U-079`. Opus **fez síntese**: cinco interpretações e sete perguntas, quatro decisivas com o
ramo que cada resposta elimina.

A preocupação que §5.1 do plano levantava — que o modelo mais forte é o mais capaz de contornar
regras de contenção por raciocínio — **não se materializou nesta ronda**: zero contornos dos dois
lados. A diferença é de posição, não de disciplina: um fecha evidência, o outro abre desenho.

**Sugestão aceite pelo dono em 2026-09-08 — é agora a decisão** (registada em `CONSOLIDATED_PLAN.md` §5.1; implementação em `pack.yaml` pendente). Aceite com a ressalva por escrito: `n = 1` por lado, abaixo do ≥ 3 que o protocolo §6.3 pede.

| Fase | Modelo | Porquê |
|---|---|---|
| Discovery (`/round`) | Sonnet 5 | fecha perguntas, e convergência é o critério de saída do Discovery; é também a fase de volume. O seu modo de falha — pequenos erros factuais — é o que o hook e a extracção persistida apanham, e esta sessão provou que apanham |
| Framing · Options · Decision | Opus 5 | onde o trabalho é enumerar ramos, abrir mais do que fecha é inofensivo, e o rigor vale o preço |
| Motores e hooks | indiferente | validam-se uma vez |

Ressalva que não se dispensa: validou-se em esforço `high`. Um passe em `high` é **forte** para
P-12 e P-1 (é onde há mais capacidade de contornar) e **não transfere para baixo** — se a produção
correr no esforço por defeito, o critério do lado Sonnet (regras *não aplicadas*) fica por medir.

#### 5.2.5 Cópias e artefactos da validação

| Cópia | Estado no fim | Serve de |
|---|---|---|
| `pricing-marinha-pilot-3` | R-04, 139 factos, 0 avisos | referência intocada; **nunca correu R-05** |
| `pricing-marinha-pilot-3-val-sonnet` | R-05, C141 A56 U39 X1 R25, 0 avisos | evidência do lado Sonnet + as duas extracções persistidas |
| `pricing-marinha-pilot-3-val-opus` | R-05, C139 A56 U46 X1 R27 | evidência do lado Opus |
| `pricing-marinha-pilot-3-val-capture` | R-04 + `/capture` run 4 | evidência de P-3 |

Ferramentas novas, em `docs/pp-pack-authoring/pilot/tools/`: `compare-validation-round.py` (as sete
aceitações lado a lado; `LER` nunca é passe), `baseline-val-R04.json` (linha de base, gerada do
original), `extract-direct.py` (extracções directas persistidas).

#### 5.2.6 O que fica aberto

1. ~~**`C-163`: onze → dez** e a regra geral que faltava ao kernel.~~ **Fechado em §5.5**
   (`995234d`): transição `Confirmed → Confirmed`, *correcção pela prova*, aplicada em
   `C-164 was C-163`.
2. **Quinta classe de prova** em `states.md` (extracção directa persistida) e a regra "a lente
   escreve em `_capture/` o que retira da fonte crua". As duas decisões de hoje existem no
   `council-log.md` e neste passo, **não no kernel**. Prosa, sessão Fable 5.1.
3. **Determinismo do motor** — quatro pontos mecânicos, sem tocar em prosa: publicar os regex do
   `confirmed_locator` no JSON (como o `arbiter` já faz); declarar a postura de falsos negativos;
   `LER` explícito em vez de lista vazia que se lê como aprovação; e **acabar com a segunda casa
   das regras** — `FUNDING_RE` e `REFERENTE_RE` vivem no script de comparação e têm de passar para
   o motor, senão divergem. Mais: declarar o tripleto de calibração (pilot-3 · dpt-galp-jp ·
   cae-automation) no repo, em vez de escolhido à mão.
4. ~~**Modelo de produção**~~ — **decidido** pelo dono em 2026-09-08: Discovery em Sonnet 5, Framing/Options/Decision em Opus 5, motores indiferentes. Aceite com a
   ressalva do `n = 1` e sem medição no esforço por defeito. **Fica a implementação em `pack.yaml`** (perfil de modelo por comando) — não é desta frente.
5. ~~**Tag de freeze**~~ — feita: `step-9c-frente-a`. **A tag congela o repo, não as cópias**: `projects/` está em `.gitignore`, por isso as três cópias de validação
   não entram nela. Ficam em disco como evidência, e o que sobrevive à sua perda é este registo — §5.2 (números, defeitos, veredictos) e os `council-log.md` de cada cópia.

Fora da frente A e sem dependência disto: **frente B** (P-8, P-9, P-11) pode arrancar em paralelo,
ficheiros disjuntos. **Frente C** só depois de A fechar.

### 5.3 Determinismo do motor — os quatro pontos aplicados (2026-09-08)

Fecho do ponto 3 de §5.2.6. Motor **1.3.0** (schema 2 inalterado — só se acrescentam
chaves). Nenhuma prosa do kernel tocada.

| Ponto | O que saiu | Commit |
|---|---|---|
| Regex publicados | `confirmed_locator`, `arbiter` e `funding_gate` publicam cada um o seu `regex` no JSON. Foi o que fez o defeito do `(a) … (b)` levar minutos a diagnosticar | `9113e3d` |
| Falsos negativos declarados | Cada bloco diz que os aceita **por desenho** e que falsos positivos **não** são aceites — um motor que avisa a torto deixa de ser lido em duas semanas | `9113e3d` |
| `julgamento` explícito | Cada bloco declara o que fica para humano **e o que uma lista vazia significa**: «nada em falta que este regex saiba ver», nunca «aprovado». Era o buraco real — vazio lia-se como passe | `9113e3d` · `a3bbbad` |
| Uma casa por regra | `FUNDING_RE` (P-4) e o referente do `decisivo` (P-1, terceira declaração) viviam no script de comparação. Passaram para o motor: `funding_gate` é bloco novo, `arbiter` ganha `decisivo_sem_referente` e `sem_citacao_m`. O script ficou com **zero** `re.compile` de regra | `9113e3d` · `6aaff44` |
| Calibração declarada | `CALIBRACAO` fixa o tripleto (`pricing-marinha-pilot-3` · `dpt-galp-jp` · `cae-automation`) e vai em cada bloco do JSON, em vez de escolhido à mão. Foi a ausência desta disciplina que produziu os quatro defeitos de §5.2.1 | `9113e3d` |

Verificação: os números do motor batem com os que o script calculava com os seus próprios
regex — R-05 no lado Opus dá `sem_citacao_m` = `U-092`, `U-089`, `U-088` e
`decisivo_sem_referente` vazio, exactamente como antes. Veredictos das sete aceitações
inalterados nas duas cópias. Cinco engagements testados, 0 diagnostics.

**Uma regra fica fora do motor, nomeada em vez de escondida:** a leitura da coluna
`classe` do §6 do modelo de processo continua no script, porque **o motor não lê
`process-model.md`**. Dar-lhe um parser de `PM-U` é feature, não limpeza — e o
`aisa-round` step 5e faria o mesmo trabalho, o que sugere que o parser tem dois
consumidores à espera. Candidato à próxima sessão de código, não a esta.

**O que isto muda para o `/status`:** antes de reportar uma lista vazia, lê o `julgamento`
do bloco. Dizer "0 problemas" onde o motor só verificou presença é precisamente a falha
que o campo existe para travar.

### 5.4 Quinta classe de prova — kernel, motor e consumidores (2026-09-08)

Fecho do ponto 2 de §5.2.6. A decisão de §5.2.3 deixa de existir só no registo do council e
passa a existir no kernel.

| Onde | O que mudou | Commit |
|---|---|---|
| `states.md` regra 1 | Quinta classe: `_capture/<ficheiro>.<extracção>.json#<chave>` ou `.md#<secção>` — extracção directa sobre a fonte crua, **persistida** sob nome próprio, método e sha256 da fonte no cabeçalho. O locator aponta ao ficheiro, nunca ao método | `d9cd05e` |
| `states.md` regra 2 | O nível da nova classe: o que a extracção **mediu**, à sua precisão — não a conclusão de suficiência (o degrau que `C-162` quase subiu) | `d9cd05e` |
| `states.md` transições + duas metades | `Unknown → Confirmed` admite a classe; lista de avisos vazia = «todo o locator aponta a algo que existe», nunca «os factos estão certos» | `d9cd05e` |
| `dashboard.py` **1.4.0** | Classe `extraccao-directa` em `LOCATOR_PATTERNS`, com lookahead negativo para os artefactos do pipeline (continuam classe 1); acrescentada **no fim** porque `answers`/`enquadramento` são indexados por posição; `NAMED_FILE_RE` captura o nome completo para o alvo ser verificado | `4a88ed2` |
| 6 lentes, Hard rule 2 | «five classes», a quinta enumerada, e a frase que fecha a porta: *o que fizeste ao ficheiro cru e não está escrito em `_capture/` não existe como evidência* | `4a88ed2` |
| `aisa-round` 5f · `HOOKS.md` · docstring do hook · `orchestration.md` | «four» → «five»; o step 5f diz que um método declarado em prosa não é locator | `4a88ed2` |

A prosa de `states.md` foi escrita **fora da sessão de código** (estava na árvore de trabalho,
por commit, quando esta sessão a foi escrever); lida contra a decisão de §5.2.3 e commitada
tal como estava — bate ponto por ponto, incluindo a nuance de `C-162`.

Testes do motor: `C-162` e `C-163` (cópia Sonnet) passam a carregar `extraccao-directa`;
`…xlsm.extraction.json#sheets` continua classe 1; `X.xlsm.inventado.json` dá alvo inexistente;
regressão nas três referências inalterada (0 / 44 / 33 avisos). Schema 2 mantém-se.

`lens-technology` não tem a Hard rule 2 — é lente de Options, com regras próprias — e ficou
como estava.

**O que fica aberto depois disto:** só os pontos 1 e 4 de §5.2.6 — a decisão sobre `C-163`
(onze → dez é transição, e por trás está a regra geral que o kernel ainda não tem: *o que fazer
quando a prova guardada contradiz um detalhe de um facto confirmado*) e o perfil de modelo por
fase. Depois: tag de freeze.

### 5.5 Correcção pela prova — a transição que faltava (2026-09-08)

Fecho do ponto 1 de §5.2.6. O caso `C-163` (onze módulos contra os dez que a extracção
persistida mostra) não tinha saída escrita no kernel, e a que existia era errada para ele.

**O diagnóstico.** A tabela de transições só tinha saídas de `Confirmed` **por expiração**.
Nem `Confirmed → Assumed` estava lá — apesar de a *Append rule* a mencionar e de esta sessão
a ter aplicado duas vezes (`A-051`, `A-052` em §3.2). Faltavam as duas, e faltava a
distinção que as separa.

**Três casos ao reler um facto contra a sua prova** (`states.md`, tabela de transições +
*Append rule*, commit `995234d`):

| Caso | Saída |
|---|---|
| A prova **não alcança** a afirmação — afirmação um degrau acima | `A-nnn was C-nnn`, base = os locators |
| A prova **desapareceu** — fonte fora do engagement (`C-015`, `C-029`) | `A-nnn was C-nnn`, base = o que resta |
| A prova **contradiz e fixa o valor certo** | **`C-nnn was C-nnn`** — o estado não desce |

O teste é uma pergunta: **a prova fixa o valor corrigido?** Fixa → a nova row fica
`Confirmed`, porque o facto continua evidenciado, melhor do que antes. Não fixa →
`Assumed`, ou `Unknown` quando nem base houver.

**Duas salvaguardas, para o precedente não virar porta aberta:**

1. A correcção **exige o locator que fixa o valor**. Sem ele cai em `Assumed`. Correcção vem
   sempre de prova melhor, nunca de argumento melhor — é isto que impede a regra de se
   tornar «editar afirmações quando me parece».
2. Ler o valor corrigido numa extracção persistida é **citação de prova, não confirmação
   humana**. Sem esta nuance escrita, a regra nova colidia com a regra 3 (só o dono
   confirma).

E uma consequência assumida na prosa: **nenhum motor apanha este caso.** A metade
determinística verifica presença e existência, nunca verdade. A contradição é sempre achado
de leitura — do árbitro (`aisa-round` step 5f, que passa a fazer **três** perguntas por
`Confirmed` nova, não duas) ou de uma pessoa.

**Primeira aplicação**, na cópia Sonnet: `C-164 was C-163`, mesma afirmação com **dez** em
vez de onze, evidência a apontar ao `…xlsm.vba.md` que fixa o número; `C-163` marcada
` — resolved → C-164`, afirmação **não tocada**. Motor: `Confirmed` abertas 141 antes e
depois (uma fecha, uma abre), resolvidas 22 → 23, 0 avisos. Registo em `council-log.md`.

**Sequência que vale a pena reter:** persistir a prova (§5.2.3) tornou o erro visível;
tornar o erro visível obrigou a escrever a transição que faltava; a transição só ficou segura
porque exige a prova que a motivou. Nenhum dos três passos existia no plano — nasceram todos
de correr o sistema a sério.

---

## 6. Regras cumpridas

- Contagens só pelo motor, antes e depois de cada item; a única contagem manual foi a verificação
  única de `R-04` (22 criadas / 33 fechadas) exigida pela aceitação de P-2 — e bateu.
- `library/` editada só por scratchpad + `cp` + commit. Nenhuma prosa do kernel tocada.
- Cada motor testado nas três cópias reais, nunca em fixtures.
- 5 perguntas de julgamento por `AskUserQuestion`; nenhuma correcção de dado aplicada sem decisão.
- Nenhuma row apagada; a única mudança de estado foram duas transições append-only.
- Nenhuma lente correu. Nenhuma tag criada.
- Modelo: Opus 5 em toda a sessão.
