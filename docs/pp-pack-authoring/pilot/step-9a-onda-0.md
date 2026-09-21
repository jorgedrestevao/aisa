# Step 9A — Onda 0, frente Discovery — medição de P-0, P-1 e P-12 sobre pilot-3

> Não é ronda de Discovery, não é correcção de código, não é edição do kernel. É a **onda 0** do plano consolidado
> (`docs/CONSOLIDATED_PLAN.md` §5): medir, sobre a SU real de `projects/pricing-marinha-pilot-3`, o que P-0, P-1 e P-12
> vão mudar — antes de mudar seja o que for. Julgamento em Fable 5.1 (§5.1); contagens só pelo motor.

**Veredicto: `STEP 9A — ONDA 0 (DISCOVERY): MEDIÇÃO CONCLUÍDA — SU INTACTA, VALIDAÇÃO DO DONO PENDENTE`.**
Os três números que mudam o diagnóstico: **18 de 85** perguntas não serviam nenhum invariante nem divergiam no futuro a construir
(3 delas eram o próprio enquadramento em falta); **12 das 41 abertas** são `cosmético` disfarçado (2 → 14) e o `decisivo` cai de **8 para 1**;
**19 de 156** `Confirmed` estão acima da evidência ou sem dono — **12 %**, não os 23 % extrapolados da amostra.

---

## 1. Base

| | |
|---|---|
| Checkpoint | `000616190d080bd9b06451de7d3a92446a0bddc9` (branch `pp-pack-authoring/step-2-discovery-layer`, HEAD ao início) |
| Engagement | `projects/pricing-marinha-pilot-3` — fase `discovery`, ronda `R-04`, pack `pp` |
| Motor | `python library/kernel/tools/dashboard.py --engagement pricing-marinha-pilot-3 --json` (tool_version 1.1.0, schema 2) — gerado 2026-09-08T12:14:32 |
| Contagens de partida (motor) | 313 rows: 156 `Confirmed` · 29 `Assumed` · 85 `Unknown` (41 abertas, 44 resolvidas) · 9 `Conflicted` · 34 `Risky`. Abertas por `swing`: 31 `dimensionante` · 8 `decisivo` · 2 `cosmético`. Coincide com §0 do plano |
| Modelo | Fable 5.1 (`claude-fable-5-1`), conforme §5.1 para a onda 0 |
| Escreveu | `projects/pricing-marinha-pilot-3/enquadramento.md` (novo) · este ficheiro · quadro *Estado por correcção* de `CONSOLIDATED_PLAN.md` §5 |
| **Não tocou** | `shared-understanding.md` · `answers.md` · `_state.json` · `library/` · qualquer outro ficheiro do engagement. Nenhuma row criada, editada ou marcada |
| Perguntas de julgamento ao dono | 6, todas por `AskUserQuestion` (M-1..M-5 e autoridades nomeadas) |

Definições usadas (kernel entre parênteses): **invariante** (`M-n`) = regra do negócio declarada pelo dono; **pergunta aberta** (`Unknown`); **alcance da resposta** (`swing`): *muda a escolha* (`decisivo`), *muda o tamanho* (`dimensionante`), *não muda nada material* (`cosmético`); **facto confirmado** (`Confirmed`); **interpretação com base** (`Assumed`).

---

## 2. Tarefa 1 — Enquadramento do mecanismo de negócio (P-0)

Entrevista ao dono do processo, 2026-09-08, uma pergunta por invariante, opções *confirmo / corrigir / retirar*, "Other" livre; mais uma pergunta sobre autoridades nomeadas (regra 3 de P-12).

| id | resultado | texto final |
|---|---|---|
| M-1 | **corrigido por palavras do dono** | "O preço fixa-se hoje como referência para uma venda que se verifica na semana seguinte. A valorização real do custo dessa venda só estará fechada na 2ª feira da semana seguinte, quando as cotações desta semana completa estiverem fechadas. Uma venda na semana N é valorizada à média das cotações da semana N-1" |
| M-2 | confirmado tal como está | A venda é valorizada à média das cotações da semana anterior à venda — a semana em que o preço se fixa |
| M-3 | confirmado tal como está | O custo de cedência é indexado a Platts |
| M-4 | confirmado tal como está | A incerteza decresce ao longo da semana (0–1 cotações à 2ª, 4 à 6ª) |
| M-5 | confirmado tal como está | O efeito é valorização errada, não venda perdida |
| Autoridades | **"Ninguém — só eu"** | Supply, IT / dono da base de dados, comerciais são fontes, não autoridades |

O que a correcção de M-1 acrescenta ao P-0: o preço de hoje é **referência**, e o custo real de uma venda só se conhece na **2ª feira seguinte**. Isto dá data ao fecho da média (M-2) e fixa o instante em que a margem valorizada se pode comparar com a apurada (M-5). Nenhuma lente perguntou "quando é que o custo de uma venda fica conhecido" em quatro rondas.

O que a resposta sobre autoridades muda em P-12: neste engagement, qualquer facto sobre sistema alheio (base de dados de pricing, add-in, feed, folha do Supply) declarado pelo dono é `Assumed` até documento — a regra 2 aplica-se sem excepção, porque não há segunda autoridade nomeada.

Escrito: [`enquadramento.md`](../../../projects/pricing-marinha-pilot-3/enquadramento.md) — cabeçalho (dono, datas, pedido literal), declaração verbatim canónica + correcção de M-1 verbatim, tabela `M-n · invariante · o que orienta · fonte`, autoridades, regras. As rows `Confirmed` R-00 (`lens = enquadramento`, evidência `enquadramento.md#M-n`) **não foram escritas** — aguardam validação deste ficheiro.

**Saiu:** `enquadramento.md` com M-1..M-5, M-1 corrigido pelo dono, autoridade única declarada.
**Número que muda o diagnóstico:** 1 invariante em 5 estava incompleto (M-1 sem o instante em que o custo fecha); 0 autoridades além do dono.
**Falta:** 5 rows `Confirmed` R-00 na SU (após validação); `dashboard.py` ainda não reconhece `R-00` nem `lens = enquadramento` (frente A).

---

## 3. Tarefa 2 — As 85 perguntas contra os invariantes (P-0)

Regra aplicada a cada `Unknown`, aberta ou resolvida, tal como escrita:

- **serve M-n** — a resposta refina ou operacionaliza um invariante (como o mecanismo se materializa em dados, fontes, momentos, KPI). Cita o M-n.
- **diverge no to-be sem M-n** — não toca no mecanismo, mas ≥ 2 respostas dão requisito, forma de dados ou esforço diferentes no sistema a construir.
- **nenhum** — nem uma nem outra: só as-is, sem divergência, cosmético, governação do engagement, ou **redundante com um M-n** (a pergunta pedia o que o enquadramento teria dado no dia zero).

| classe | total (85) | abertas (41) | resolvidas (44) |
|---|---|---|---|
| serve M-n | 18 | 6 | 12 |
| diverge no to-be | 49 | 20 | 29 |
| nenhum | 18 | 15 | 3 |

Por ronda de origem e por lens:

| ronda | serve M-n | diverge | nenhum | total |
|---|---|---|---|---|
| R-01 | 5 | 19 | 10 | 34 |
| R-02 | 4 | 7 | 3 | 14 |
| R-03 | 3 | 10 | 2 | 15 |
| R-04 | 6 | 13 | 3 | 22 |

| lens | serve M-n | diverge | nenhum | total |
|---|---|---|---|---|
| business | 2 | 9 | 3 | 14 |
| data | 9 | 7 | 2 | 18 |
| financial | 1 | 3 | 5 | 9 |
| governance | 0 | 15 | 1 | 16 |
| operations | 4 | 7 | 5 | 16 |
| user | 2 | 8 | 2 | 12 |

Leitura:

- **18 de 85 não serviam nada** (21 %). 15 delas continuam abertas — o grupo *nenhum* é hoje **15 das 41 abertas** (37 %), porque as que serviam M-n ou divergiam fecharam-se primeiro. É a medida do custo do Discovery sem enquadramento, em rows.
- **3 são redundantes com um M-n** (U-001, U-022, U-062): a pergunta pedia o próprio mecanismo. U-062 é o caso extremo — foi ela que trouxe C-136/C-137, formulada como "venda perdida" contra M-5. Com P-0, as três não existiriam.
- **18 servem um M-n**, mas nenhuma o citou — o mecanismo chegou na R-04. As 5 de R-01 (U-003, U-007, U-014, U-018, U-041) perguntavam pelo *sintoma* (o gesto de 2ª/3ª, a regra do maior, a janela) sem o *porquê*. Com M-1/M-2 no dia zero, teriam sido perguntas de **como** desde a primeira ronda.
- **`governance` não serve nenhum M-n** (0 de 16) e é a lens com mais divergência (15). Coerente com o mandato: o mecanismo de valorização não é tema de controlo. `data` é a lens que mais o serve (9 de 18).
- **`financial` tem 5 de 9 em *nenhum*** — as quatro de envelope/custo as-is (U-030, U-032, U-034, U-072) e U-062. Confirma §0 ponto 3: o problema da lens é mandato, não volume.

Tabela completa (id · lens · ronda · estado · classe · M-n ou razão):

| id | lens | ronda | estado | classe | M-n ou razão |
|---|---|---|---|---|---|
| U-001 | business | R-01 | resolvida → C-138 | nenhum | redundante com M-5 — quem sente a consequência é a margem valorizada; P-0 tê-lo-ia dado |
| U-002 | business | R-01 | resolvida → C-054 | diverge no to-be | construir vs reutilizar capacidade já paga → classe de opção |
| U-003 | business | R-01 | resolvida → C-125 | serve M-n | M-5 — o alvo mensurável é margem apurada vs valorizada; a resposta (continuidade) ficou aquém do M-5 |
| U-004 | business | R-01 | resolvida → C-061 | diverge no to-be | a causa da falha anterior fixa a condição que a opção tem de bater (curvas forward excluídas) |
| U-005 | business | R-01 | resolvida → C-115 | nenhum | governação do engagement (quem assina), não requisito do sistema |
| U-006 | business | R-01 | aberta | nenhum | janela de entrega; nenhum requisito, forma de dados ou esforço muda |
| U-007 | operations | R-01 | resolvida → C-064 | serve M-n | M-4 — o gesto de 2ª/3ª hoje; perguntado pelo sintoma porque M-2 não existia |
| U-008 | operations | R-01 | resolvida → C-065 | diverge no to-be | tela vs simulador → superfície a reconstruir |
| U-009 | operations | R-01 | resolvida → C-100 | diverge no to-be | excepções intencionais = requisitos em falta; cicatrizes = defeitos a não reproduzir |
| U-010 | operations | R-01 | aberta | nenhum | baseline as-is (tempo de ciclo); não muda o to-be |
| U-011 | operations | R-01 | aberta | nenhum | causa da corrupção do artefacto que se abandona; as-is |
| U-012 | operations | R-01 | resolvida → C-066 | diverge no to-be | handoffs fora do ficheiro → âmbito de integrações |
| U-013 | user | R-01 | resolvida → C-055, U-044 | diverge no to-be | papéis → perfis de ecrã |
| U-014 | user | R-01 | resolvida → C-071 | serve M-n | M-1 — janela das 9:30 e frescura no ponto de uso |
| U-015 | user | R-01 | resolvida → C-073 | diverge no to-be | offline elimina classes de solução |
| U-016 | user | R-01 | resolvida → C-072 | diverge no to-be | automatizar a entrada vs dar-lhe superfície → desenhos distintos |
| U-017 | user | R-01 | aberta | nenhum | cosmético declarado (rótulos) |
| U-018 | data | R-01 | resolvida → C-123, U-074 | serve M-n | M-3 — qual das fontes Platts é registo da cotação |
| U-019 | data | R-01 | aberta | diverge no to-be | famílias vivas → modelo de dados e superfície de entrada |
| U-020 | data | R-01 | resolvida → C-079, U-058 | diverge no to-be | dono por entidade → integração vs dado mestre novo |
| U-021 | data | R-01 | resolvida → C-151 | diverge no to-be | retenção → registo persistido e versionado ou não |
| U-022 | data | R-01 | aberta | nenhum | redundante com M-2 — a valorização é à média passada, não a curva forward (C-061 confirmou) |
| U-023 | data | R-01 | aberta | diverge no to-be | metadado a preservar → campos novos no modelo |
| U-024 | governance | R-01 | resolvida → C-121 | diverge no to-be | obrigação de reporte → o que guardar e por quanto tempo |
| U-025 | governance | R-01 | resolvida → C-122 | diverge no to-be | gate vs registo posterior → estado de workflow |
| U-026 | governance | R-01 | resolvida → C-120 | diverge no to-be | reprodutibilidade → registo versionado |
| U-027 | governance | R-01 | resolvida → C-056, U-045 | diverge no to-be | residência, identidade, ponto de autorização → classes de solução |
| U-028 | governance | R-01 | resolvida → C-152, U-084 | diverge no to-be | via de cotação sancionada → replicar vs redesenhar integração |
| U-029 | governance | R-01 | aberta | diverge no to-be | gate de go-live; reversibilidade a construir ou herdada |
| U-030 | financial | R-01 | aberta | nenhum | custo as-is (taxa carregada); não muda o to-be |
| U-031 | financial | R-01 | resolvida → C-114, U-072 | diverge no to-be | envelope elimina classes de opção |
| U-032 | financial | R-01 | aberta | nenhum | custo as-is (direitos já pagos); não muda o to-be |
| U-033 | financial | R-01 | aberta | serve M-n | M-5 — quantifica margem por tonelada em risco: o KPI do enquadramento |
| U-034 | financial | R-01 | aberta | nenhum | cosmético declarado (rubrica contabilística) |
| U-035 | business | R-02 | resolvida → C-057, U-052 | diverge no to-be | famílias de output entregues → âmbito |
| U-036 | business | R-02 | aberta | diverge no to-be | input vs output → desenho da tela |
| U-037 | operations | R-02 | aberta | serve M-n | M-2 — que cotações entram na média (janela deslocada = esperar fecho) |
| U-038 | operations | R-02 | aberta | nenhum | ordem de recálculo do artefacto; o motor novo define a sua (C-037 já captura o ciclo) |
| U-039 | user | R-02 | aberta | diverge no to-be | número vs decomposição auditável → tela e persistência |
| U-040 | data | R-02 | aberta | serve M-n | M-3 — a segunda fonte Platts é fonte usada ou resíduo |
| U-041 | data | R-02 | resolvida → C-077 | serve M-n | M-1 — semana em curso vs semana seguinte: a regra do maior existe porque o preço é para a semana seguinte |
| U-042 | data | R-02 | aberta | diverge no to-be | ratios variáveis → superfície de manutenção e histórico |
| U-043 | data | R-02 | aberta | nenhum | as-is (limite de 12 linhas); só reformulada — "que horizonte a média precisa" — serviria M-2 |
| U-044 | user | R-02 | aberta | nenhum | contagem de utilizadores: mesmo requisito; papéis já em C-055/C-139 |
| U-045 | governance | R-02 | resolvida → C-119, U-073 | diverge no to-be | ponto de aplicação da autorização → classes de solução |
| U-046 | user | R-02 | resolvida → C-140 | diverge no to-be | conversão na app vs ficheiro → capacidade a construir |
| U-047 | operations | R-02 | resolvida → C-141 | serve M-n | M-1 — a média mínima das duas semanas carregada no sistema de propostas decorre da publicação de duas semanas |
| U-048 | governance | R-02 | resolvida → C-117 | diverge no to-be | aprovador e substituto → gate implementável ou não |
| U-049 | business | R-03 | resolvida → C-112 | diverge no to-be | reutilizar 80% vs 20% → decisões distintas |
| U-050 | business | R-03 | aberta | diverge no to-be | swap em âmbito → fluxo com contraparte externa |
| U-051 | business | R-03 | resolvida → C-145 | serve M-n | M-2 — a série histórica para treinar o fecho da média semanal |
| U-052 | business | R-03 | aberta | diverge no to-be | outputs com consumidor → âmbito |
| U-053 | operations | R-03 | resolvida → C-099 | diverge no to-be | artefacto vivo vs morto → dimensionamento sobre números certos |
| U-054 | operations | R-03 | aberta | diverge no to-be | input dentro da janela → requisito de tolerância a atraso, ou nada |
| U-055 | operations | R-03 | aberta | diverge no to-be | reemissão → versões com validade e retirada, ou sobrepor |
| U-056 | user | R-03 | resolvida → C-124 | serve M-n | M-4 — reunir informação vs sugerir incremento: como se resolve 2ª/3ª |
| U-057 | data | R-03 | resolvida → C-146, U-080 | serve M-n | M-3 — de onde vem a cedência indexada a Platts |
| U-058 | data | R-03 | aberta | diverge no to-be | prémios/SLIs → dado mestre novo vs integração |
| U-059 | data | R-03 | aberta | diverge no to-be | constante vs parâmetro vs tabela → campo vs entidade |
| U-060 | governance | R-03 | resolvida → C-116 | diverge no to-be | extensão de controlo vs alteração de política → projectos distintos |
| U-061 | governance | R-03 | aberta | diverge no to-be | governação de release herdada ou a construir |
| U-062 | financial | R-03 | resolvida → C-136 | nenhum | redundante com M-2/M-5 — a resposta É o enquadramento (C-136, C-137); formulada como "venda perdida" contra M-5 |
| U-063 | operations | R-03 | aberta | nenhum | C-100/C-101 já fixam a re-ancoragem à mão como gesto; a edição no to-be é desenho (C-149, C-052), não herança |
| U-064 | business | R-04 | aberta | diverge no to-be | família em âmbito → motor, coluna, componentes |
| U-065 | business | R-04 | aberta | diverge no to-be | linha viva → reproduzir; morta → remover do âmbito |
| U-066 | operations | R-04 | resolvida → C-142, U-079 | diverge no to-be | VBA no cálculo → regra a reproduzir que nenhuma extracção leu |
| U-067 | operations | R-04 | resolvida → C-143 | serve M-n | M-4 — o câmbio também é desconhecido à 2ª/3ª: segunda família de alvo |
| U-068 | user | R-04 | aberta | diverge no to-be | glossário existe → blueprint derivado vs elicitação coluna a coluna |
| U-069 | data | R-04 | resolvida → C-144 | serve M-n | M-2 — a estimativa emitida como série para aprender o fecho da média |
| U-070 | governance | R-04 | aberta | nenhum | preservar e criar protecção dão o mesmo requisito (exemplo canónico de P-1) |
| U-071 | financial | R-04 | resolvida → C-118 | diverge no to-be | família sem desenvolvimento → custo único vs recorrente |
| U-072 | financial | R-04 | aberta | nenhum | limiar de aprovação do engagement, não do sistema; cue de envelope inactivo com funding_gate=false |
| U-073 | governance | R-04 | resolvida → C-147, U-081 | diverge no to-be | autorização na base hoje → herdar vs construir |
| U-074 | data | R-04 | resolvida → C-148, U-082 | serve M-n | M-3 — quem alimenta a cotação, com que frescura, e o que sucede em falha |
| U-075 | financial | R-04 | resolvida → C-153 | diverge no to-be | 212 vs 465 colunas → factor 2,2 no esforço |
| U-076 | governance | R-04 | resolvida → C-149 | diverge no to-be | comercial vê margem → modelo de autorização |
| U-077 | user | R-04 | resolvida → C-150, U-083 | diverge no to-be | simulação comunicável → cobertura do gate |
| U-078 | operations | R-04 | aberta | nenhum | o próprio swing declara que não altera o desenho; decide só a duração de R-020 |
| U-079 | governance | R-04 | aberta | diverge no to-be | código no cálculo → reconstrução incompleta e estimativa a rever |
| U-080 | data | R-04 | aberta | serve M-n | M-3 — por que via a cedência entra no processo |
| U-081 | governance | R-04 | aberta | diverge no to-be | dois níveis de acesso suportados vs a construir |
| U-082 | data | R-04 | aberta | serve M-n | M-3/M-4 — comportamento do feed em falha e frescura visível da cotação |
| U-083 | user | R-04 | aberta | diverge no to-be | variáveis da simulação → inputs da superfície do comercial |
| U-084 | governance | R-04 | aberta | diverge no to-be | saída de dados → condiciona opções com serviço externo |
| U-085 | data | R-04 | aberta | serve M-n | M-2 — os cinco instrumentos reconstroem a média semanal de valorização? |

**Saiu:** 85 classificadas — 18 serve · 49 diverge · 18 nenhum.
**Número que muda o diagnóstico:** 18 rows sem serventia (21 % do total; 37 % das abertas), 3 delas eram o enquadramento em falta.
**Falta:** `/round` numa cópia com `enquadramento.md` presente para confirmar que nenhuma `Unknown` nova pergunta o porquê de 2ª/3ª (aceitação de P-0, frente A).

---

## 4. Tarefa 3 — As 41 abertas com a regra de P-1

Regra aplicada à row **tal como está escrita** (o árbitro de P-1 verifica presença de declarações, não materialidade): (i) cita um M-n **ou** o `swing` nomeia ≥ 2 respostas; (ii) nomeia a diferença no requisito, forma dos dados ou esforço do sistema a construir (dispensado se cita M-n); (iii) `decisivo` nomeia o frame candidato ou branch que a resposta elimina. Falha em (i) ou (ii) → `cosmético`; falha em (iii) → `dimensionante`. Onde a divergência é inferível com base declarada → `→ Assumed` (a regra manda escrever `Assumed` em vez de `Unknown`).

| swing | actual | proposto |
|---|---|---|
| decisivo | 8 | 1 |
| dimensionante | 31 | 24 |
| cosmético | 2 | 14 |
| → Assumed | 0 | 2 |

**21 das 41 mudam de classe.** Leitura:

- **`decisivo` 8 → 1.** Só U-085 nomeia o referente que a resposta elimina (C-155: o modelo é construível). As outras sete (U-033, U-065, U-068, U-079, U-080, U-081, U-082) descrevem consequência em esforço, âmbito ou requisito — isso é `dimensionante` por definição do kernel. Duas recuperam `decisivo` se nomearem o referente: U-081 (C-119, autorização na base) e U-033 (C-124/R-029, a projecção como meio). O `/status` mostra hoje 8 perguntas "que mudam a escolha"; com a regra, mostra 1.
- **`cosmético` 2 → 14.** As 12 novas: U-078 (o próprio `swing` diz que não altera o desenho), U-070 (exemplo canónico do plano), U-072, U-063, U-044, U-043, U-038, U-030, U-032, U-010, U-011, U-006. Nenhuma tem `custo = reuniao` excepto U-010, U-011 e U-072 — a agenda de reunião do `/status` perde 3 pontos.
- **`→ Assumed` 2.** U-022 (M-2 + C-061 dizem que não há curva forward em uso) e U-023 (C-104/C-019 dizem que a semântica vive nos comentários). São perguntas cuja resposta já está na SU com base declarada.
- **Uma Critical fica `cosmético`:** U-044 (quantas pessoas). Criticidade e alcance são eixos separados; a regra não toca na criticidade, mas o par *Critical + cosmético* é sinal de criticidade herdada de U-013 sem revisão.
- **Tensão P-1 × P-4, a resolver na frente A.** Quatro das novas `cosmético` são o mandato que P-4 mantém activo na lens `financial` com `funding_gate = false`: `as_is_cost` (U-010, U-030) e direitos já pagos (U-032), mais U-072. Pela regra de P-1 — diferença *no sistema a construir* — o custo as-is não muda requisito, dados nem esforço, logo é `cosmético`. Pelo mandato de P-4, é o denominador do caso de negócio. Ou P-1 admite uma quarta diferença ("no critério de decisão"), ou P-4 aceita que o custo as-is entra por `Assumed`/`Confirmed` de baseline e não por `Unknown`. Não decidi; registo.

Tabela completa (id · lens · ronda · criticidade · custo · swing actual · swing proposto · razão). **↓** = desce.

| id | lens | ronda | crit. | custo | swing actual | swing proposto | razão |
|---|---|---|---|---|---|---|---|
| U-006 | business | R-01 | Med | email | dimensionante | cosmético **↓** | fixa janela de entrega; não muda requisito, dados nem esforço |
| U-010 | operations | R-01 | Med | reuniao | dimensionante | cosmético **↓** | baseline as-is; não muda o sistema. Tensão P-1 × P-4 (as_is_cost) |
| U-011 | operations | R-01 | Med | reuniao | dimensionante | cosmético **↓** | causa da corrupção de um artefacto que se abandona; todos os mecanismos já registados (C-010, C-011) |
| U-017 | user | R-01 | Low | email | cosmético | cosmético | mantém |
| U-019 | data | R-01 | Med | documento | dimensionante | dimensionante | famílias vivas → modelo de dados |
| U-022 | data | R-01 | Med | email | dimensionante | → Assumed **↓** | inferível com base declarada: M-2 (valorização à média passada) + C-061 (curvas forward descartadas) → "resíduo de preenchimento" |
| U-023 | data | R-01 | Med | email | dimensionante | → Assumed **↓** | inferível: C-104 e C-019 mostram que a semântica das colunas vive nos comentários → metadado a preservar |
| U-029 | governance | R-01 | Med | email | dimensionante | dimensionante | gate de go-live; reversibilidade a construir ou herdada |
| U-030 | financial | R-01 | Med | email | dimensionante | cosmético **↓** | custo as-is: não muda requisito, dados nem esforço do sistema. Tensão P-1 × P-4 (as_is_cost é mandato) |
| U-032 | financial | R-01 | Med | email | dimensionante | cosmético **↓** | idem: direitos já pagos alteram a comparação de custo, não o sistema. Tensão P-1 × P-4 |
| U-033 | financial | R-01 | Critical | reuniao | decisivo | dimensionante **↓** | cita M-5 (fica Unknown); decisivo exige referente e não o nomeia — recuperaria se nomeasse C-124/R-029 como branch em risco |
| U-034 | financial | R-01 | Low | email | cosmético | cosmético | mantém |
| U-036 | business | R-02 | Med | email | dimensionante | dimensionante | input vs output → desenho da tela |
| U-037 | operations | R-02 | Med | email | dimensionante | dimensionante | cita M-2; regra → parâmetro; artefacto → corrigir |
| U-038 | operations | R-02 | Med | reuniao | dimensionante | cosmético **↓** | a ordem de recálculo é do artefacto; o motor novo define a sua e C-037 já captura o ciclo |
| U-039 | user | R-02 | Med | reuniao | dimensionante | dimensionante | número vs decomposição → tela e persistência; C-149 já responde pela metade dos comerciais |
| U-040 | data | R-02 | Med | email | dimensionante | dimensionante | cita M-3; passo de processo invisível a suportar ou resíduo |
| U-042 | data | R-02 | Med | email | dimensionante | dimensionante | superfície de manutenção + histórico vs constantes |
| U-043 | data | R-02 | Med | email | dimensionante | cosmético **↓** | como escrita é as-is ("o que acontece hoje"); reformulada — "que horizonte a média precisa" — serve M-2 e é dimensionante |
| U-044 | user | R-02 | Critical | email | dimensionante | cosmético **↓** | contagem: 3 ou 6 utilizadores dão o mesmo requisito e a mesma forma de dados; papéis já fixados |
| U-050 | business | R-03 | Med | email | dimensionante | dimensionante | fluxo de swap dentro ou fora |
| U-052 | business | R-03 | Med | email | dimensionante | dimensionante | dois outputs em âmbito ou não |
| U-054 | operations | R-03 | Med | email | dimensionante | dimensionante | cita M-1 (janela); input → requisito de tolerância a atraso; output → nada |
| U-055 | operations | R-03 | Med | reuniao | dimensionante | dimensionante | versões com validade e retirada vs sobrepor o último |
| U-058 | data | R-03 | Med | email | dimensionante | dimensionante | dado mestre novo vs integração |
| U-059 | data | R-03 | Med | email | dimensionante | dimensionante | campo de configuração vs entidade |
| U-061 | governance | R-03 | Med | reuniao | dimensionante | dimensionante | release herdado vs a construir → esforço e reversibilidade |
| U-063 | operations | R-03 | Med | documento | dimensionante | cosmético **↓** | C-100/C-101 já respondem ao conteúdo; a diferença restante é só as-is |
| U-064 | business | R-04 | Med | email | dimensionante | dimensionante | em âmbito → motor + coluna + componentes; fora → nada |
| U-065 | business | R-04 | Critical | email | decisivo | dimensionante **↓** | viva → reproduzir; morta → remover: âmbito. A-014 não é frame nem branch — sem referente, desce |
| U-068 | user | R-04 | Critical | email | decisivo | dimensionante **↓** | documento vs elicitação muda duração, custo e risco — dimensionamento, não escolha |
| U-070 | governance | R-04 | Med | email | dimensionante | cosmético **↓** | preservar e criar dão o mesmo requisito; a pergunta boa ("quem altera a composição") é Assumed-able de C-052/C-149 |
| U-072 | financial | R-04 | Med | email | dimensionante | cosmético **↓** | limiar de aprovação muda quem assina o engagement, não o sistema; cue inactivo (funding_gate=false) |
| U-078 | operations | R-04 | Med | email | dimensionante | cosmético **↓** | o próprio swing diz "não altera o desenho desta solução" |
| U-079 | governance | R-04 | Critical | spike | decisivo | dimensionante **↓** | código no cálculo muda requisitos e esforço (C-154); nenhum frame ou branch nomeado |
| U-080 | data | R-04 | Critical | documento | decisivo | dimensionante **↓** | cita M-3; integração vs carregamento vs manual muda o requisito; não nomeia branch que elimina |
| U-081 | governance | R-04 | Critical | documento | decisivo | dimensionante **↓** | 2 respostas → herdar vs construir 2 níveis (esforço); recuperaria decisivo se nomeasse C-119 como branch eliminado |
| U-082 | data | R-04 | Critical | documento | decisivo | dimensionante **↓** | cita M-3/M-4; alerta vs silêncio muda requisito de frescura; C-123 sobrevive às duas |
| U-083 | user | R-04 | Med | email | dimensionante | dimensionante | ≥2 respostas (volume, porto, produto…) e diferença no to-be: inputs da superfície do comercial |
| U-084 | governance | R-04 | Med | email | dimensionante | dimensionante | 2 respostas; diferença no to-be só para opções com serviço externo — não elimina branch vivo |
| U-085 | data | R-04 | Critical | spike | decisivo | decisivo | cita M-2 e nomeia o referente eliminado: C-155 (modelo construível) cai e R-028 volta |

**Saiu:** 41 reclassificadas — 1 decisivo · 24 dimensionante · 14 cosmético · 2 → Assumed; 21 mudam.
**Número que muda o diagnóstico:** 12 `cosmético` disfarçadas (29 % das abertas) e `decisivo` 8 → 1.
**Falta:** decidir P-1 × P-4 (custo as-is); aplicar as 21 edições de `swing` como edição de metadados sancionada com registo em `council-log.md` (mesma classe da correcção do `/simulate`) — após validação; `/round` em cópia para a aceitação de P-1.

---

## 5. Tarefa 4 — As 156 `Confirmed` com os dois testes de P-12

Teste 1 — **locator numa das quatro classes** (fórmula/prosa no Excel ou extractor · transcrição `[hh:mm:ss]` · docx · declaração do dono em `answers.md#`/`enquadramento.md#`). Teste 2 — **afirmação ao nível da evidência**: fórmula → "o artefacto contém"; transcrição → "X afirmou"; dono → facto dentro da sua autoridade; sobe um nível (regra de negócio a partir de fórmula, facto a partir de terceiro, facto técnico de sistema alheio por negócio, conclusão de cadeia, generalização de dois instantâneos) → `Assumed`. Regra 3 — confirmação humana só do dono (hoje declarado autoridade única): resolução de `X-`/`R-` por evidência interna → **sem dono**.

| nível | rows |
|---|---|
| ao nível | 134 |
| acima | 14 |
| sem dono | 8 |

| fonte | rows |
|---|---|
| Excel (fórmula/extractor) | 59 |
| transcrição | 36 |
| dono · AskUserQuestion (sem âncora) | 17 |
| dono · answers.md# | 16 |
| dono · declaração 2026-09-07 (sem âncora) | 14 |
| interna (executor) | 8 |
| Excel + transcrição | 3 |
| context.json (fora das 4 classes) | 1 |
| extractor sem locator citável | 1 |
| dono (sem âncora) | 1 |

Leitura:

- **19 rows recebem `A-nnn was C-nnn`** (12 %): 8 *sem dono* (C-094, C-126, C-132, C-133, C-134, C-135, C-155, C-156 — seis riscos e duas colisões fechados por raciocínio do executor) e 11 *acima* (C-003, C-021, C-087, C-097, C-101, C-106, C-111, C-147, C-148, C-152, C-154). As 7 da amostra de §0 estão todas cá; as outras 12 são a extensão. **15 das 19 são R-04** — a subida acontece quando a ronda encadeia raciocínio sobre rows anteriores, como §0 previa. A extrapolação da amostra (~36) sobreavaliou para o dobro: a amostra 1-em-5 apanhou 6 R-04 em 30 e a R-04 é a ronda mais densa.
- **Uma superada, não transição:** C-010 (95 substituições manuais) foi corrigida por C-100 e não está marcada `resolved →`. Marcador sancionado, não row nova.
- **Duas conclusões de cadeia validadas a posteriori:** C-107 (pelo dono, C-144) e C-033 (pela transcrição, C-090). Regra 5 de P-12: ficam `Confirmed` se ganharem o locator da validação — não precisam de `A was C`.
- **14 ficam `Confirmed` com nota de redacção** — o núcleo está ao nível, a cauda ultrapassa (C-116 "herda limiar e trilha"; C-059 "nunca"; C-095 "o mecanismo é clonar"; C-062 "nada é manual" de terceiro; C-027 "curva forward" é rótulo do extractor; C-031, C-034, C-099, C-100, C-146, C-085) ou a fonte é o dono a falar de sistema que não governa mas que financia (C-047, C-048, C-151). Não são transições; são frases a mover para a coluna de evidência na próxima revalidação.
- **Teste 1 falha em forma, não em classe, em 32 rows:** todas as `USER_ANSWER` de 2026-09-07/08 citam a data e o mecanismo (`AskUserQuestion`, "declaração em reunião") mas **não a âncora** `answers.md#BLOCO-x`. O alvo existe em `answers.md`; a row não aponta. O hook `su-confirmed-guard.py` de P-12 vai listar 32, não as 5 que a aceitação 2 do plano espera (C-155, C-126, C-131, C-120, C-114) — a aceitação tem de ser reescrita ou as âncoras completadas antes de ligar o hook. Duas classes fora das quatro: C-002 (`context.json.literal_request` — palavras do dono, propor aceitar) e C-026 (contagens do extractor sem célula citável — completar com `.extraction.json#folha`).
- **Por lens, as 19:** governance 6 · business 4 · data 3 · operations 2 · financial 2 · user 2. `governance` lidera porque fechou 5 riscos/colisões por raciocínio (C-133, C-134, C-094, C-147, C-152).

### Lista final — `A-nnn was C-nnn` a criar (19)

| C-nnn | lens | ronda | nível | base do `Assumed` |
|---|---|---|---|---|
| C-003 | business | R-01 | acima | `'Outputs BIOS'!M` = `#REF!` em Jan e Ago; "viva" fica para U-065 |
| C-021 | data | R-01 | acima | padrão dominante `INDEX/MATCH(Data_Lista)`; "todo o modelo" é generalização |
| C-087 | governance | R-03 | acima | `kickoff · [01:13:19]` LF afirma a trilha; existência não verificada |
| C-094 | governance | R-03 | sem dono | adjudicação sobre C-088, C-029, C-010/C-012; sem resposta de sponsor |
| C-097 | business | R-04 | acima | replay #14–#21: duas formas de extrapolação; "não existe método" é inferência |
| C-101 | operations | R-04 | acima | PM-035, replay #2/#7/#11; "criado a partir do anterior" é inferência |
| C-106 | data | R-04 | acima | dois instantâneos (A1:N285→N416; Inputs!B 356→171); "nunca trunca" é política inferida |
| C-111 | financial | R-04 | acima | replay: 465 colunas sem padrão em 13 folhas; "motor de esforço" é modelo |
| C-126 | operations | R-04 | sem dono | adjudicação sobre C-097, PM-034, C-012, A-017; sem resposta de sponsor |
| C-132 | business | R-04 | sem dono | C-112/C-113 (dono) + raciocínio "risco sem objecto" (executor) |
| C-133 | governance | R-04 | sem dono | C-120, C-121, C-128, C-130 + raciocínio (executor) |
| C-134 | governance | R-04 | sem dono | C-120, C-121, C-106, C-107, PM-035 + raciocínio (executor) |
| C-135 | user | R-04 | sem dono | C-124, C-117, C-118 + raciocínio (executor) |
| C-147 | governance | R-04 | acima | declaração do dono sobre capacidade da base; verificação em U-081 |
| C-148 | data | R-04 | acima | declaração do dono sobre carregamento da base; verificação em U-082 |
| C-152 | governance | R-04 | acima | declaração do dono sobre estatuto de IT do add-in; metade de U-028 em U-084 |
| C-154 | financial | R-04 | acima | C-153 (dono) + A-024 + aritmética 465−49−204; estimativa, não facto |
| C-155 | business | R-04 | sem dono | C-137, C-106, C-107, A-028 + raciocínio; premissa em verificação em U-085 |
| C-156 | user | R-04 | sem dono | C-139, C-140, C-149, C-150 + raciocínio; residual em R-034 |

Invariante de P-12 (aceitação 4): nenhuma row apagada; `Confirmed + Assumed` passa de 156 + 29 = 185 para 137 + 48 = 185.

Tabela completa (id · lens · ronda · fonte · nível · razão · acção):

| id | lens | ronda | fonte | nível | razão | acção |
|---|---|---|---|---|---|---|
| C-001 | business | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-002 | business | R-01 | context.json (fora das 4 classes) | ao nível | palavras do dono em context.json.literal_request — classe fora das quatro de P-12; propor aceitar como declaração do dono | locator |
| C-003 | business | R-01 | Excel (fórmula/extractor) | acima | "linha de produto viva": a evidência mostra só o erro; U-065 pergunta exactamente se está viva | A was C |
| C-004 | business | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-005 | business | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-006 | business | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-007 | operations | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-008 | operations | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-009 | operations | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-010 | operations | R-01 | Excel (fórmula/extractor) | acima | "95 substituições manuais" — C-100 corrigiu a leitura (rótulos ≠ substituições); C-010 não está marcada superada | superada por C-100 |
| C-011 | operations | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-012 | operations | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-013 | operations | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-014 | operations | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-015 | user | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-016 | user | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-017 | user | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-018 | user | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-019 | user | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-020 | data | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-021 | data | R-01 | Excel (fórmula/extractor) | acima | "todo o modelo" a partir do padrão dominante — exemplo de P-12 | A was C |
| C-022 | data | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-023 | data | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-024 | data | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-025 | data | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-026 | data | R-01 | extractor sem locator citável | ao nível | contagens do extractor sem locator citável (folhas sem célula/ficheiro) — completar com .extraction.json#folha | locator |
| C-027 | data | R-01 | Excel (fórmula/extractor) | ao nível | "curva forward" é o rótulo heurístico do extractor; ao nível é "115 datas futuras" — U-022 pergunta o resto | nota |
| C-028 | governance | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-029 | governance | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-030 | governance | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-031 | governance | R-01 | Excel (fórmula/extractor) | ao nível | "não governadas dentro do processo" é juízo; C-152 mostra o add-in governado por IT fora do processo | nota |
| C-032 | financial | R-01 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-033 | financial | R-01 | Excel (fórmula/extractor) | acima | "ciclo corre em dias úteis" lido de formatação condicional; validado pela transcrição em C-090 | manter C; acrescentar locator C-090 |
| C-034 | financial | R-01 | Excel (fórmula/extractor) | ao nível | fórmulas citadas; "a base sobre a qual um erro se materializa" é cauda interpretativa | nota |
| C-035 | business | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-036 | business | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-037 | operations | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-038 | operations | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-039 | operations | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-040 | operations | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-041 | data | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-042 | data | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-043 | data | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-044 | data | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-045 | data | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-046 | data | R-02 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-047 | data | R-02 | dono · answers.md# | ao nível | existência da base declarada por quem a financia; o detalhe técnico verifica-se com U-081/U-082 | nota |
| C-048 | data | R-02 | dono · answers.md# | ao nível | conteúdo da base declarado pelo dono de negócio; verificar por documento (U-081/U-082) | nota |
| C-049 | business | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-050 | governance | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-051 | user | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-052 | governance | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-053 | operations | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-054 | business | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-055 | user | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-056 | governance | R-02 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-057 | business | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-058 | business | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-059 | business | R-03 | transcrição | ao nível | "nunca interrompeu" generaliza "de férias estou a enviar" | nota |
| C-060 | business | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-061 | business | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-062 | business | R-03 | transcrição | ao nível | funcionalidades demonstradas em reunião (observado); "nada é manual" é citação de terceiro | nota |
| C-063 | business | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-064 | operations | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-065 | operations | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-066 | operations | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-067 | operations | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-068 | operations | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-069 | operations | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-070 | operations | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-071 | user | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-072 | user | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-073 | user | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-074 | user | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-075 | user | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-076 | data | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-077 | data | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-078 | data | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-079 | data | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-080 | data | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-081 | data | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-082 | data | R-03 | Excel + transcrição | ao nível | locators das duas classes; afirmação ao nível do observado e do dito |  |
| C-083 | data | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-084 | governance | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-085 | governance | R-03 | transcrição | ao nível | afirmação de JE com assentimento do dono; "não existe hoje" coerente com C-030 | nota |
| C-086 | governance | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-087 | governance | R-03 | transcrição | acima | existência de trilha na app adjacente afirmada por terceiro (LF) e registada como facto | A was C |
| C-088 | governance | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-089 | governance | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-090 | financial | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-091 | financial | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-092 | financial | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-093 | financial | R-03 | transcrição | ao nível | passagem citada com timestamp; afirmação atribuída a quem falou |  |
| C-094 | governance | R-03 | interna (executor) | sem dono | X-003 resolvida por evidência interna, sem resposta do sponsor — mesma classe de C-126 | A was C |
| C-095 | business | R-04 | Excel (fórmula/extractor) | ao nível | deltas medidos; "o mecanismo de extensão é clonar" é inferência sobre a estrutura de Base HS | nota |
| C-096 | business | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-097 | business | R-04 | Excel (fórmula/extractor) | acima | "não existe método" a partir de duas fórmulas — exemplo de P-12 | A was C |
| C-098 | business | R-04 | Excel + transcrição | ao nível | locators das duas classes; afirmação ao nível do observado e do dito |  |
| C-099 | operations | R-04 | Excel + transcrição | ao nível | datas do ficheiro provam execução em 2026-08-03; "em vigor" em Setembro é pequena extrapolação | nota |
| C-100 | operations | R-04 | Excel (fórmula/extractor) | ao nível | contagens do replay; "é aqui que está a fragilidade real" é cauda interpretativa | nota |
| C-101 | operations | R-04 | Excel (fórmula/extractor) | acima | "criado a partir do anterior" inferido da estrutura — exemplo de P-12 | A was C |
| C-102 | operations | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-103 | operations | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-104 | user | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-105 | user | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-106 | data | R-04 | Excel (fórmula/extractor) | acima | "acumula e nunca trunca" / "a cada ciclo" generaliza dois instantâneos para política | A was C |
| C-107 | data | R-04 | Excel (fórmula/extractor) | acima | conclusão de cadeia (C-106 + PM-034 + C-101) validada a posteriori pelo dono em C-144 | manter C; acrescentar locator C-144 |
| C-108 | data | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-109 | data | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-110 | governance | R-04 | Excel (fórmula/extractor) | ao nível | fórmula ou estrutura lida do extractor; a afirmação descreve o artefacto |  |
| C-111 | financial | R-04 | Excel (fórmula/extractor) | acima | "motor de esforço" é modelo de estimativa; a evidência dá 465 colunas sem padrão — exemplo de P-12 | A was C |
| C-112 | business | R-04 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-113 | business | R-04 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-114 | financial | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-115 | business | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-116 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | núcleo declarado pelo dono; cauda ("herda limiar e trilha, não é alteração de política") é inferência de C-084/C-069 — mover para evidência | nota |
| C-117 | governance | R-04 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-118 | financial | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-119 | governance | R-04 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-120 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-121 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-122 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-123 | data | R-04 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-124 | user | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-125 | business | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-126 | operations | R-04 | interna (executor) | sem dono | X-001 resolvida por evidência interna, sem resposta do sponsor — exemplo de P-12 | A was C |
| C-127 | business | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-128 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-129 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-130 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-131 | governance | R-04 | dono · declaração 2026-09-07 (sem âncora) | ao nível | declaração do dono, datada; decisão ou facto do seu processo — falta âncora answers.md#BLOCO | âncora answers.md |
| C-132 | business | R-04 | interna (executor) | sem dono | risco declarado "sem objecto" por raciocínio do executor sobre C-112/C-113 | A was C |
| C-133 | governance | R-04 | interna (executor) | sem dono | risco "respondido" por cadeia C-120/C-121/C-128/C-130; executor | A was C |
| C-134 | governance | R-04 | interna (executor) | sem dono | risco fechado "como risco de governação" por cadeia; executor | A was C |
| C-135 | user | R-04 | interna (executor) | sem dono | risco "materialmente mitigado" por cadeia C-124/C-117/C-118; executor | A was C |
| C-136 | financial | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-137 | data | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-138 | business | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-139 | user | R-04 | dono · answers.md# | ao nível | declaração do sponsor/dono em answers.md#A-001; facto do seu processo |  |
| C-140 | user | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-141 | operations | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-142 | operations | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-143 | operations | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-144 | data | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-145 | business | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-146 | data | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono sobre o input do seu processo; "parcela dominante" vem de C-076 (primeiro termo), não de valor | nota |
| C-147 | governance | R-04 | dono · AskUserQuestion (sem âncora) | acima | facto técnico de sistema alheio (autorização na base) confirmado por negócio — exemplo de P-12 | A was C |
| C-148 | data | R-04 | dono · AskUserQuestion (sem âncora) | acima | facto técnico de sistema alheio (carregamento automatizado) confirmado por negócio | A was C |
| C-149 | governance | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-150 | governance | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-151 | data | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | dono declara ausência de regra própria; a própria row regista que controlo interno não respondeu | nota |
| C-152 | governance | R-04 | dono · AskUserQuestion (sem âncora) | acima | estatuto de política de IT ("sancionado") declarado por negócio; o mais fraco dos 11 | A was C |
| C-153 | business | R-04 | dono · AskUserQuestion (sem âncora) | ao nível | declaração do dono, datada; facto ou decisão dentro da sua autoridade — falta âncora answers.md#BLOCO | âncora answers.md |
| C-154 | financial | R-04 | dono (sem âncora) | acima | estimativa derivada (465−49−204) "a reconstruir" — inferência sobre C-153 + A-024, não facto | A was C |
| C-155 | business | R-04 | interna (executor) | sem dono | conclusão de cadeia do executor (R-028 sem objecto); nenhuma declaração do dono | A was C |
| C-156 | user | R-04 | interna (executor) | sem dono | conclusão de cadeia ("ficou falsa") sobre C-139/C-140; o dono decidiu o âmbito, não o veredicto do risco | A was C |

**Saiu:** 156 testadas — 134 ao nível · 14 acima · 8 sem dono; 19 `A was C`; 1 superada; 2 locators de validação; 14 notas; 32 âncoras em falta.
**Número que muda o diagnóstico:** 19 de 156 (12 %), não ~36 (23 %); 15 das 19 são R-04.
**Falta:** criar as 19 rows (após validação); marcar C-010; completar 32 âncoras antes de ligar `su-confirmed-guard.py`; reescrever a aceitação 2 de P-12 (5 → 32).

---

## 6. O que a onda 0 muda no plano

| Medição (§5 onda 0) | Esperado no plano | Medido | Consequência |
|---|---|---|---|
| Custo do Discovery sem enquadramento | "em rows" | 18 de 85 (3 redundantes com M-n; 15 sem divergência) | P-0 evita directamente 3; as outras 15 são P-1. Juntos, 21 % das perguntas |
| `cosmético` disfarçadas | "número real" | 12 (2 → 14 de 41) | `/status` agenda perde 3 reuniões; tensão P-1 × P-4 aparece |
| `decisivo` com referente | mantido, com referente obrigatório | 8 → 1 | a coluna "muda a escolha" do `/status` está sobreavaliada 8× |
| `Confirmed` acima do nível | ~36 (23 %) | 19 (12 %) + 1 superada + 2 locators | a metade determinística de P-12 (hook) importa mais do que a amostra sugeria: 32 âncoras em falta, não 5 |
| Autoridades além do dono | por registar | nenhuma | regra 2 de P-12 sem excepções neste engagement |

Três coisas para a frente A que o plano não tinha:

1. **P-1 × P-4**: o custo as-is é `cosmético` pela regra de P-1 e mandato por P-4. Decidir antes de escrever os `lens-*/SKILL.md`.
2. **Âncoras**: 32 rows `USER_ANSWER` sem `answers.md#`. Ou `aisa-answer` passa a escrever a âncora, ou o hook nasce a avisar 32 vezes. A aceitação 2 de P-12 está errada nos números.
3. **`M-1` corrigido**: P-0 no plano tem o texto antigo. O canónico passa a ser o de `enquadramento.md`; actualizar §3 P-0 quando a frente A arrancar.

## 7. Pendente de validação do dono (nada foi aplicado)

| Acção | Quantidade | Mecanismo quando validado |
|---|---|---|
| Rows `Confirmed` R-00 na SU (M-1..M-5) | 5 | append, `lens = enquadramento`, evidência `enquadramento.md#M-n`, `validade = organizacional` |
| `A-nnn was C-nnn` | 19 | transição append-only; original marcada `— resolved → A-nnn`; registo em `council-log.md` |
| Marcador `resolved → C-100` em C-010 | 1 | marcador sancionado |
| Locator de validação em C-107 (C-144) e C-033 (C-090) | 2 | edição de evidência — mecanismo a definir na frente A (revalidação sancionada?) |
| Edições de `swing` | 21 | edição de metadados sancionada, registada em `council-log.md` (classe `/simulate`) |
| Âncoras `answers.md#BLOCO-x` | 32 | edição de evidência em lote — mecanismo a definir |

## 8. Regras cumpridas

- Contagens de partida e de estado só pelo motor (`--json`); as contagens das classificações são do script sobre o JSON do motor, nunca à mão.
- `library/` não tocada. `shared-understanding.md`, `answers.md`, `_state.json` não tocados.
- 6 perguntas de julgamento ao dono por `AskUserQuestion`; nenhuma inferência de M-n a partir do pedido literal ou do `_capture`.
- Modelo: Fable 5.1 em toda a sessão (§5.1, onda 0 — julgamento).

Quadro *Estado por correcção* em `CONSOLIDATED_PLAN.md` §5: P-0, P-1, P-12 → `em curso (step-9a)`. A frente A começa noutra sessão.
