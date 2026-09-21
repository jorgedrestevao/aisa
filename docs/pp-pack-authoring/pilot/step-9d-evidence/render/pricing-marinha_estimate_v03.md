# Estimativa de Implementação — Pricing Marinha

> **v03 — re-render direccionado.** Re-executados apenas os slots que a alteração de contrato da
> frente B toca: `phases_table` (§5), `named_uncertainties` (§9), `estimate_assumptions` (§13),
> `estimate_preconditions` (§14, novo), `team_effort` + `profile_load` (§16) e
> `delivery_recommendations` (§19). Todas as outras secções são idênticas a `v02`, carácter a
> carácter, e **o total de 44 pessoa-dias não muda** — P-8, P-9 e F09 são projecções, não um
> recálculo. As secções 14–18 de `v02` passam a 15–19.

> Estimativa de **esforço de implementação** para o âmbito decidido. Audience: sponsor + procurement.
>
> **Esta entrega é a dona do cálculo.** Método: `library/packs/pp/domain-knowledge/craft/estimation-model.md`
> (método apenas, pessoa-dias). **Não é economia de decisão** (essa vive no Relatório Executivo, S8).
> **Sem preços.** Denominador: pessoa-dias.

## 1. Modo de input

**Modo A — estimativa de implementação.** Inventário de origem: `_render/pricing-marinha_implementation-spec_v02.md` (arquitectura aprovada `v05` + o inventário dessa Especificação). Nenhuma unidade de trabalho foi acrescentada além do que a Especificação carrega.

## 2. Âmbito desta estimativa

Apenas o lado PP-owned: a aplicação de pricing diário de bancas (dados-mestre, custos logísticos, margens, dashboard de preço diário com aprovação, histórico, exportação para Excel). A obrigação de integração do lado PP com a BD SQL Server partilhada e com o SAP **é** estimada (secções 3, 7); a entrega do lado de fora — quem opera essas integrações, o carregamento efectivo em X-Author por outra iniciativa — está **excluída** (secção 14).

## 3. Decomposição de trabalho

| Unidade de trabalho | Origem (Implementation Spec) | Qtd | Banda | Subtotal |
|---|---|---|---|---|
| Ecrã model-driven (DadosMestreList, DadosMestreForm, CustosLogisticosForm, MargensAlvoForm, PrecoDiarioDashboard, HistoricoPrecosDashboard) | secção 5 | 6 | 1d (Model-driven app screen, Dataverse) | 6d |
| Approval workflow (Aprovação de Carregamento) | secção 5, 8 | 1 | 2d | 2d |
| Vista SQL role-specific (por papel: Analista, Comité, Superior, Dono de Dados-Mestre) | secção 8 | 4 | 0,5d (SQL View) | 2d |
| Vista SQL consolidada (Preço Diário, Histórico) | secção 4 | 2 | 0,5d (SQL View) | 1d |
| Integração externa — referência SAP (leitura) | secção 7 | 1 | 4d (External integration, midpoint da banda 3-5d) | 4d |
| Fluxo de publicação — exportação para Excel | secção 7, 13 | 1 | 2d (PA flow, publicação, ficheiro + geração) | 2d |
| Configuração de colunas de auditoria (6 entidades) | secção 4 | 6 | 0,25d | 1,5d |
| Trabalho de prova em ambiente produtivo (V4) | secção 13 | 1 | 3d (alocação directa, método não especificado além disso) | 3d |
| Preparação e mapeamento (Fase 0 — formalizar regras, clarificar integrações, validar modelo de dados, configurar os 2 ambientes já confirmados) | secção 3, 9, 16 | — | 4d | 4d |
| UAT, operação paralela obrigatória, formação (Fase 7) | secção 13 | — | 5d | 5d |
| **Total bruto** | | | | **30,5d** |

**Controlo de âmbito**: nenhuma unidade acima está ausente da Especificação de Implementação; nenhuma foi acrescentada por esta estimativa. Sem alterações face a `v01` — a aprovação de v05 (A8/A9) não introduz nenhuma unidade de trabalho nova, apenas remove incerteza sobre ambientes e propriedade (secção 9).

## 4. Bandas de esforço

Método: `craft/estimation-model.md`, tabela "Effort table (days per component per store)". Ecrãs estimados pela banda **Model-driven app screen** (coluna Dataverse) — ver premissa nomeada na secção 13: os dados residem numa BD SQL Server externa via conector, não num store Dataverse nativo; a banda mais próxima disponível no método foi usada por analogia, não existe uma banda específica para "model-driven app sobre store externo virtualizado".

## 5. Fases

| Fase | Conteúdo | Dias | Perfil responsável | Dependências | Incerteza que a ameaça (§9) |
|---|---|---|---|---|---|
| 0 — Preparação | Formalizar regras do Excel, clarificar integrações SQL/SAP, validar modelo de dados, configurar os 2 ambientes (Dev, Produção — `C-067`) | 4d | PP developer (+ SME, + IT para ambientes) | Ambientes já confirmados (`C-067`) — dono do controlo de release ainda por confirmar | — |
| 1 — Camada de dados | Vistas SQL (role-specific + consolidadas), colunas de auditoria | 4,5d | PP developer | BD partilhada já operada (`C-057`) — sem bloqueio | Retenção legal do histórico (`X-005`) — sem quantificação nesta captura |
| 2 — Ingestão | Integração de leitura ao SAP | 4d | PP developer | SAP já calcula termos de contrato a termo (`C-003`) | — |
| 3 — Aplicação | 6 ecrãs + approval workflow | 8d | PP developer (+ SME na validação) | Dono de dados-mestre e regra de desempate já satisfeitos (`C-058`, `C-059`) | Capacidade de simulação dos KAM (`R-012`) — +3–5d se confirmada necessária |
| 4 — Publicação | Fluxo de exportação para Excel | 2d | PP developer | Formato exacto por confirmar com a outra iniciativa (`C-065`) | Formato exacto do Excel (`C-065`) — +1–2d de rework |
| 7 — UAT e go-live | Testes, operação paralela (mínimo 2 semanas, obrigatória), trabalho de prova V4, formação | 8d (3d prova + 5d UAT/formação) | PP developer + SME (+ IT no go-live) | — | Dono do controlo de release (`C-067`) — sem esforço de build, pode atrasar |
| **Total** | | **30,5d** | | | |

Sequenciado pelas dependências que a Especificação de Implementação carrega (secção 14 da Especificação) — a narrativa financeira não é autoridade de sequenciamento.

Duas incertezas de §9 **não ameaçam nenhuma fase deste total**, e ficam registadas como tal: `DF_GRID_1` (`R-008`) e a substituição do artefacto Excel (`R-004`) ameaçam a fase de **migração**, que não está incluída neste total (ver secção 8).

### 5.1 Fases ≥ 5 pessoa-dias — tarefas em intervalo de planeamento

Duas fases atingem o limiar de 5 pessoa-dias: a Fase 3 e a Fase 7. As restantes quatro não se decompõem — granularidade abaixo do limiar seria fabricada, não medida.

**Como se deriva cada intervalo** (premissa de método, secção 13): onde `craft/estimation-model.md` dá uma **banda**, é essa a banda; onde dá uma **taxa pontual**, o intervalo é `min == max` e diz que é taxa pontual; onde **não dá entrada nenhuma**, o intervalo é `min == max` com a analogia nomeada e a marca *sem banda no método*. Nenhum intervalo foi alargado para parecer uma banda.

**Fase 3 — Aplicação (8d)**

| Tarefa | Intervalo de planeamento | Perfil |
|---|---|---|
| Construir os 6 ecrãs do blueprint aprovado | 6,0 – 6,0 d (6 × 1d, `Model-driven app screen` — **taxa pontual** do método) | PP developer |
| Implementar o approval workflow de Aprovação de Carregamento | 2,0 – 2,0 d (`Approval workflow` — **taxa pontual** do método) | PP developer |
| **União dos intervalos** | **8,0 – 8,0 d** — contém a figura da fase (8d) | |

**Fase 7 — UAT e go-live (8d)**

| Tarefa | Intervalo de planeamento | Perfil |
|---|---|---|
| Trabalho de prova V4 — prova em ambiente produtivo | 3,0 – 3,0 d — **sem banda no método**; analogia com o esforço de teste ponta-a-ponta | PP developer + SME |
| UAT, operação paralela obrigatória (mín. 2 semanas de calendário) e formação | 5,0 – 5,0 d — **sem banda no método**; 5d de esforço activo distribuídos pela janela de calendário | PP developer + SME |
| **União dos intervalos** | **8,0 – 8,0 d** — contém a figura da fase (8d) | |

A decomposição **redistribui** o que a fase já carregava: a figura de cada fase e o total de 30,5d brutos (44d após complexidade e buffer) são idênticos aos de `v02`. Que os quatro intervalos sejam degenerados (`min == max`) é o resultado honesto de um método que, para estes componentes, dá taxas pontuais e nenhuma distribuição — e é informação útil: diz exactamente onde o método não tem banda.

## 6. Resumo de esforço

Total bruto: 30,5 pessoa-dias. Complexidade: **Média** (7 entidades, dentro da banda 5-20 entidades) → ×1,2 = 36,6d. Buffer (sempre +20% para unknowns) → ×1,2 = 43,9d ≈ **44 pessoa-dias base** (inalterado face a v01).

## 7. Esforço de trabalho de prova

| Obrigação de prova | Nível | Método | Dono | Financiada? | Esforço | Incerteza |
|---|---|---|---|---|---|---|
| Prova em ambiente produtivo (scope de solução inteira) | V4 | not specified further | not named | não | 3d (incluído no total da secção 6) | Método de prova não especificado além do nível — esforço pode variar consoante o que "aceite" acabe por significar como evidência (ver Implementation Spec secção 10) |

## 8. Esforço de migração

`not applicable` — a Especificação de Implementação não carrega uma secção de migração e cutover engajada (o conditional A9 de substituição de artefacto existente nunca foi formalmente activado, nem em v04 nem em v05). Ver secção 14 (âmbito excluído) e secção 9 (incertezas nomeadas).

## 9. Incertezas nomeadas

| Item em aberto | Esforço que oscila | Fase ameaçada | O que o resolveria | Id |
|---|---|---|---|---|
| `DF_GRID_1` — artefacto morto ou activo | Se activo: +2-3d de investigação/correcção antes da migração das folhas dependentes | Fase de **migração** — não incluída neste total (secção 8) | Confirmação directa do Pedro O. | `R-008` |
| Capacidade de simulação dos KAM — preservar nalgum canal fora da app | Se confirmada necessária: +3-5d para um novo canal/funcionalidade não contemplada nesta decomposição | Fase 3 — Aplicação | Sessão de validação KAM já autorizada | `R-012` |
| Formato exacto do Excel exportado | +1-2d de rework do fluxo de publicação se o formato acordado divergir do assumido | Fase 4 — Publicação | Alinhamento com o dono da iniciativa de carregamento em X-Author | `C-065` |
| Dono explícito do controlo de release (Dev→Produção) | Sem esforço de build directo, mas pode atrasar a Fase 7 se não confirmado a tempo | Fase 7 — UAT e go-live | Confirmação directa com IT centralizado | `C-067` |
| Substituição do artefacto Excel actual nunca formalmente activada | Se activada: uma fase de migração inteira, **não incluída** no total acima (ver secção 8) — tipicamente 2-3d por esta tabela de método para migração histórica, mas por confirmar o volume real | Fase de **migração** — não incluída neste total (secção 8) | Revisão explícita do blueprint (v06) activando o conditional A9 | `R-004` |
| Retenção legal do histórico de preços | Sem esforço de build directo à data; pode alterar requisitos de retenção do store, sem quantificação nesta captura | Fase 1 — Camada de dados | Confirmação jurídica explícita | `X-005` (Conflicted — nenhum lado escolhido) |

Face a `v01`: os 2 itens ligados à ausência de A8/A9 (ambientes, propriedade) foram **removidos** desta lista — resolvidos pela aprovação de v05. Nenhum destes está escondido dentro da contingência da secção 10 — cada um é nomeado, com o seu próprio esforço estimado e o que o resolveria.

Face a `v02`: a lista é a mesma, com a coluna **Fase ameaçada** acrescentada. Cada um dos 6 itens aparece também na linha da sua fase, na secção 5 — o mesmo item, referenciado, nunca uma segunda incerteza. Os 2 que ameaçam a migração dizem-no: a fase que ameaçam não está neste total.

## 10. Gama e contingência

Base: 44 pessoa-dias (secção 6). Contingência sobre os itens nomeados da secção 9 (excluindo a migração, que fica fora do total por não estar engajada): +3 a +5 pessoa-dias, consoante quantos destes itens se materializem — **gama estreitada face a v01** (era +4 a +7), reflectindo os 2 itens resolvidos por v05. **Gama total com contingência incluída: 44-49 pessoa-dias.**

## 11. Confiança

**Média-alta** (subiu face a v01). Baseado numa arquitectura aprovada (`v05`, `decisions.md#D-004`) com 0 escolhas estruturais em aberto e, agora, 0 gaps de conteúdo em A8/A9 — mas ainda com uma premissa metodológica não trivial (banda "Model-driven app screen" aplicada por analogia a um store externo virtualizado, não Dataverse nativo — secção 4) e 5 itens não-estruturais por confirmar (secção 9). Não é uma estimativa de modo B.

## 12. Estimativas por candidato

`not applicable` — modo A resolveu; não existem candidatos de arquitectura em aberto.

## 13. Premissas da estimativa

- Ecrãs estimados pela banda "Model-driven app screen" (Dataverse) por ser a única banda do método para este tipo de superfície — o store real é uma BD SQL Server externa virtualizada, não Dataverse nativo (ver secção 4).
- Integração SAP estimada no ponto médio da banda "External integration" (3-5d) — sem detalhe do protocolo exacto de leitura.
- Trabalho de prova V4 alocado a 3d por analogia com o esforço de teste ponta-a-ponta do método — o método em si não especifica um valor para esta obrigação específica.
- Fase 7 (UAT + operação paralela obrigatória, mínimo 2 semanas de calendário) estimada em 5d de esforço activo distribuído por essa janela — não 2-3 semanas de esforço a tempo inteiro.
- **Derivação de cada intervalo de planeamento** (secção 5.1): banda do método onde o método dá banda; `min == max` marcado como *taxa pontual* onde dá taxa pontual; `min == max` com a analogia nomeada e a marca *sem banda no método* onde não dá entrada. Nenhum intervalo é alargado para parecer banda, e nenhum quantil é afirmado — o método não tem distribuição.
- `_synthesis/risks-and-assumptions.md# Assumptions to validate during build` — nenhuma das premissas aí listadas (`A-001` a `A-008`) altera directamente uma unidade de trabalho desta estimativa; são premissas de negócio/dados, não de esforço de construção.

**O que saiu desta secção, e para onde.** Disponibilidade de SME, acessos, licenças, entitlements e aprovisionamento **não** são premissas de método: são **pré-condições de entrega**, e vivem na secção 14 com dono, prazo e a fase que travam. Nesta estimativa nenhuma delas estava escrita como premissa em `v02` — estavam **ausentes**. A secção 14 não as relocaliza: acrescenta-as.

## 14. Pré-condições de entrega

| Pré-condição | Dono | Até quando | Que fase trava | Estado |
|---|---|---|---|---|
| Disponibilidade do SME / dono do processo a **20%** ao longo do projecto, com blocos de calendário acordados à cabeça | Pedro O. / equipa de pricing | Antes do arranque da Fase 0 | Fases 0, 3 e 7 — formalização das regras, validação com utilizador, UAT | Por satisfazer — nenhuma evidência do engagement registou o acordo dos blocos |
| Acesso (leitura e escrita) à BD SQL Server partilhada de pricing | Equipa que já opera a BD partilhada (`compositions# shared-pricing-sql-server`, `C-057`) | Antes do arranque da Fase 1 | Fase 1 — camada de dados | Por satisfazer — o acesso não está registado como concedido |
| Acesso de leitura ao SAP para termos de contrato a termo | IT centralizado (`compositions# sap-term-pricing-reference`, `C-063`) | Antes do arranque da Fase 2 | Fase 2 — ingestão | Por satisfazer |
| Ambientes Dev e Produção aprovisionados | IT / infra-estrutura (A8, `C-063` / `C-067`) | Antes do fim da Fase 0 | Fase 0 → Fase 1 | Por satisfazer — o **modelo** de 2 ambientes está confirmado (`C-067`); o aprovisionamento não está registado |
| Dono explícito do controlo de release (aprovação Dev→Produção) | `not named` — inferido por extensão de `C-063`, não confirmado | Antes da Fase 7 | Fase 7 — go-live | Por satisfazer (`C-067`, item em aberto do blueprint) |
| Dono de dados-mestre nomeado + processo mínimo de controlo de mudança | Pedro O. / governance | `not named` | Início do desenho de schema (Fase 0 → Fase 1) | **Parcialmente satisfeito** — `C-058` nomeia o dono e exige aprovação formal; não descreve o processo |
| Limpeza das chaves de contraparte (`C-019`) financiada | `not named` | Antes da 1ª migração | Fase de **migração** — não incluída neste total (secção 8) | Por satisfazer (`decisions.md#D-002` — Conditions) |
| Confirmação do blast radius de `DF_GRID_1` | Pedro O. | Antes de qualquer migração | idem | Por satisfazer (`R-008`) |
| Confirmação de retenção legal com jurídico | Jurídico | `not named` | Fase 1 — camada de dados (prazo de retenção do histórico) | Por satisfazer — conflito não resolvido (`X-005`) |
| Revisão DLP / residência | IT security | `not named`, apenas se for introduzido novo ponto de saída externo | Introdução de novo ponto de saída | **Não engajada** — nenhum novo ponto de saída externo além dos já registados |

Nenhuma destas pré-condições é convertida em «satisfeita» por esta estimativa: os dois estados de satisfação parcial vêm de evidência do engagement (`C-058`) e nada mais. Nenhum dono foi inventado — `not named` renderiza como `not named`.

A **dedicação de 20% do SME** declarada na primeira linha é a que a secção 16 lê para a ocupação por perfil. É uma declaração, lida duas vezes; não duas declarações.

## 15. Âmbito excluído desta estimativa

- **Relocado, fronteira representada**: operação da BD SQL Server partilhada (equipa que já a opera) e da referência SAP (IT centralizado) — a obrigação de integração do lado PP está estimada (secções 3, 7); a entrega/operação do lado de fora não.
- **Relocado, fronteira representada**: carregamento efectivo em X-Author — pertence a outra iniciativa, fora desta engagement; nenhuma provisão, placeholder ou banda de contingência para esse trabalho.
- **Migração e cutover** (secção 8): não engajada na arquitectura aprovada — sem alocação nesta estimativa; ver secção 9 para o que aconteceria se activada.

## 16. Equipa e esforço por perfil

| Perfil | Pessoa-dias | Dedicação (secção 14) | Fases envolvidas |
|---|---|---|---|
| Power Platform developer | 44 (o total desta estimativa) | 100% | 0, 1, 2, 3, 4, 7 |
| SME / dono do processo (Pedro O. / equipa de pricing) | `not named` | 20% ao longo de todo o projecto | 0, 3, 7 |
| IT / infra-estrutura | `not named` | Pontual (ambientes, acessos, entitlements) | 0, 7 |

Escala: complexidade Média → 1-2 developers Power Platform + SME, per `craft/estimation-model.md` §"Standard team composition".

Os 44 pessoa-dias são esforço do perfil de **developer**: o total é construído a partir das taxas por componente do método, que são trabalho de construção. A dedicação de 20% do SME e a dedicação pontual do IT são **exigências de disponibilidade**, não linhas deste total — e os seus pessoa-dias não estão itemizados em nenhuma fonte autoritativa. Não se inventam aqui.

### 16.1 Ocupação por perfil

Aritmética apenas: `pessoa-dias ÷ dedicação → semanas mínimas`, a 5 dias por semana.

| Perfil | Pessoa-dias | Dedicação | Semanas mínimas |
|---|---|---|---|
| Power Platform developer | 44 | 100% | 44 ÷ 1,0 = 44 dias → **≥ 9 semanas** |
| SME / dono do processo | `not named` | 20% | — (`pessoa-dias not named`: sem pessoa-dias não há figura de semanas) |
| IT / infra-estrutura | `not named` | Pontual — não quantificável em percentagem | — (`dedication not named` como percentagem) |

A ocupação do developer cabe na dedicação declarada: 44 pessoa-dias a 100% ao longo de 9 semanas são 44 dias contra 45 disponíveis.

**Sem grelha, sem Gantt, sem data de calendário, sem sobreposição derivada entre perfis.** O paralelismo é julgamento, e a equipa não é observada aqui. A única coisa que esta estimativa diz sobre paralelismo é a restrição que a Especificação carrega, em prosa: as Fases 0–2 são sequenciais; as Fases 3 e 4 podem sobrepor-se parcialmente; a Fase 7 é obrigatoriamente **posterior** a todas as fases de desenvolvimento. As 9 semanas mínimas são um mínimo de ocupação, não um plano — nada aqui as converte em datas.

## 17. Impacto operacional

`not applicable` — o inventário autoritativo da Especificação de Implementação não carrega uma alteração de caminho operacional quantificada (nenhuma linha de "tempo poupado" foi especificada). O as-is (menos de 1h/dia, `C-030`) não é fonte desta secção.

## 18. Drivers de custo

Classe de entitlement: utilizadores internos directos (equipa de pricing, comité, superior hierárquico) — não licenciamento por KAM, que ficam fora do âmbito de utilizadores (`C-056`). População afectada pelo output: ~200 KAM (`C-013`), sem serem utilizadores licenciados. Driver de crescimento: volume/margem reportados num pico plurianual (`A-005`) — sem impacto directo no dimensionamento de licenças conhecido nesta captura. Sem preços, SKUs nem quotas.

## 19. Recomendações de entrega

- Resolver primeiro os 2 itens de sequenciamento sem custo de build (`DF_GRID_1`, formato de export) antes da Fase 3, para evitar rework.
- Confirmar o dono explícito do controlo de release com IT centralizado antes da Fase 7, para não atrasar o go-live.
- Não activar a fase de migração enquanto o conditional A9 de substituição do Excel não for formalmente decidido — evita construir para um cutover ainda não desenhado.

**Dimensão de repetição: nenhuma.** A decomposição não repete o mesmo trabalho sobre N ≥ 3 instâncias nomeadas — há um âmbito único (`decisions.md#D-002`, *whole solution*), 7 entidades distintas e 6 ecrãs distintos, não N cópias do mesmo trabalho. Os ~200 KAM (`C-013`) são audiência do output, não instâncias de construção, e estão fora do âmbito de utilizadores (`C-056`). **Nenhum piloto sobre subconjunto é recomendado**, porque não há subconjunto que o inventário nomeie — recomendar um seria fabricá-lo.
