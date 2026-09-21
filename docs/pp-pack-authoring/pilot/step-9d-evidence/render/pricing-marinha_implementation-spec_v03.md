# Implementation Specification — Pricing Marinha

> Especificação de construção accionável. Audience: equipa de implementação.
>
> **Arquitectura → obrigações de construção.** A arquitectura registada é **lida**: esta especificação
> não escolhe store, não escolhe composição nem padrão, não altera o modo de experiência, não reabre
> Options e não inventa detalhe de implementação para uma escolha arquitectural **não resolvida** —
> essa renderiza-se como *open work item* com dono e com o que a resolveria.
>
> Fonte de arquitectura: `_blueprint/ux-blueprint_v05.yaml` (aprovada, `decisions.md#D-004`).
>
> **v03 — re-render direccionado.** Só três slots foram re-executados, contra a mesma
> arquitectura aprovada e sem qualquer alteração upstream: `flows_to_implement` (§6),
> `build_gates` (§2, uma célula de estado) e `open_work_items` (§16). Todas as outras secções
> são idênticas a `v02`, carácter a carácter. Razão: a alteração de contrato de P-8 —
> `implementation-spec.template.md# slot_conditions.flows_to_implement`.

## 1. Âmbito de construção

Âmbito PP-owned: a aplicação inteira de pricing diário de bancas — dados-mestre, custos logísticos, margens-alvo, dashboard de preço diário com aprovação de carregamento, histórico de preços, exportação para Excel (`decisions.md#D-002`, âmbito único "whole solution"). Não existe um segundo âmbito nesta decisão — não há categorias de propriedade de âmbito a projectar (apenas um par (âmbito, resultado)).

Fora do âmbito de construção desta app, com fronteira representada e nada desenhado do lado de fora: a BD SQL Server partilhada de pricing (autoridade de dados, `keep-in-place`, operada por outra equipa); a referência de leitura ao SAP para termos de contrato a termo (operada por IT centralizado); o carregamento efectivo em X-Author (responsabilidade de outra iniciativa, fora desta engagement — esta app só exporta Excel).

## 2. Portões de construção (condições e pré-condições que travam o arranque)

| Condição/pré-condição | Dono | Financiada? | Até quando | O que trava | Estado |
|---|---|---|---|---|---|
| Dono de dados-mestre nomeado + processo mínimo de controlo de mudança | Pedro O. / governance | not named | not named | Início do desenho de schema | **Parcialmente satisfeito** — `C-058` nomeia o dono (Pedro O.) e exige aprovação formal das mudanças; **não** descreve o processo mínimo de controlo de mudança, que a condição também pede |
| Limpeza das chaves de contraparte (`C-019`) financiada | not named | not named | Antes da 1ª migração | Migração de dados | Por satisfazer |
| Revisão DLP/residência | IT security | not named | Se introduzir novo ponto de saída externo | Introdução de novo ponto de saída | Não engajado — nenhum novo ponto de saída externo além dos já registados |
| Regra de desempate entre as 6 folhas divergentes | Pedro O. / operations-lead | — | — | Consolidação num único modelo de cálculo | Satisfeito (`C-059`) |
| Confirmação do blast radius de `DF_GRID_1` | Pedro O. | — | Antes de qualquer migração | Migração das folhas dependentes | Por satisfazer (`R-008`) |
| Confirmação de retenção legal com jurídico | jurídico | — | — | Definição do prazo de retenção do histórico | Por satisfazer — conflito não resolvido (`X-005`) |

Nenhum destes portões é convertido em «satisfeito» por este documento. Os dois estados de satisfação vêm de evidência do engagement (`C-058`, `C-059`) e nada mais; face a `v02`, o primeiro portão passa de *satisfeito* a **parcialmente satisfeito**, porque `C-058` cobre a metade do dono e não a metade do processo. Os restantes permanecem por satisfazer, com o seu dono e estado tal como registados.

## 3. Restrições de arquitectura (projectadas)

- **A1** — Âmbito autorizado: "whole solution", `authorized`, base de outcome "it fits with stated, funded conditions" (`decisions.md#D-002`).
- **A2** — Intenção: composição-base seria isolada; duas escaladas forçadas por `C-057`/`C-062` (BD partilhada já existe) e `C-003` (SAP já calcula termos de contrato a termo).
- **A3** — 4 componentes de fronteira, todos `outside-platform`: `shared-pricing-sql-server`, `sap-term-pricing-reference`, e as responsabilidades relocadas `termos-comerciais-contrato-a-termo` e `carregamento-em-x-author`.
- **A5** — Autoridade de registo: 4 domínios, todos externos (`keep-in-place` × 3, `virtualized` × 1) — nenhum store nativo da plataforma introduzido para dados persistentes de negócio.
- **A6** — Nenhum stream de automação assíncrono registado; as integrações são referências síncronas directas.
- **A7** — Identidade: directório interno; ponto de imposição: aplicação (Aprovação de Carregamento) + o que a BD partilhada já impõe do seu lado.
- **A8** — 2 ambientes (Dev, Produção, sem Teste formal, `C-067`); rota de release Dev→Produção directa; residência inalterada (Interno, `C-036`); plano de política inferido para IT centralizado (`C-063`), não confirmado como afirmação directa (item aberto, secção 16).
- **A9** — Autoridade de dados fixada em `keep-in-place` externo (`C-057`) — reversível hoje, internalizar depois teria custo real. Propriedade: equipa de pricing dona da app e dos dados de negócio; IT centralizado opera a infra-estrutura partilhada por baixo (`C-068`).

## 4. Entidades e estruturas de dados

| Entidade | Autoridade de registo | `access_mode` | Notas |
|---|---|---|---|
| Dados-Mestre de Pricing | external system of record (SQL Server partilhado) | keep-in-place | Dicionário contraparte × combustível × métrica; hoje 291 named ranges no Excel, decomposição exacta em ~85 campos manuais ainda não itemizada nesta captura (`C-017`, ver secção 16) |
| Custos Logísticos | external system of record (SQL Server partilhado) | keep-in-place | Por porto e modo de transporte, actualização mensal (`C-016`) |
| Margens-Alvo | external system of record (SQL Server partilhado) | keep-in-place | Por produto, tipo de cliente e data, decidida em comité diário (`C-002`) |
| Preço Diário Consolidado | external system of record (SQL Server partilhado) | keep-in-place | Output único, substitui as 6 folhas hoje divergentes (`C-041`); alimenta a exportação para Excel |
| Aprovação de Carregamento | external system of record (SQL Server partilhado) | keep-in-place | Estados: pendente → aprovado → carregado (`C-026`, `C-043`) |
| Histórico de Preços | external system of record (SQL Server partilhado) | keep-in-place | Registo estruturado e consultável, substitui o arquivo de ficheiros soltos (`C-018`, `R-004`) |
| Termos Comerciais de Cliente (contrato a termo) | external system of record (SAP) | virtualized | Não gerido nesta app — referenciado apenas para leitura; SAP é a fonte de verdade (`C-052`) |

Nenhum store nativo da plataforma detém autoridade sobre estes dados — todos residem em sistemas externos já operados.

## 5. Ecrãs / componentes a construir

Condicional a `experience.mode != none` — engajado. Fonte: `ux-blueprint_v05.yaml` (SEE_V01 + export_features).

| Ecrã | Padrão | Personas | `su_refs` |
|---|---|---|---|
| DadosMestreListScreen | gallery | Analista de Pricing, Dono de Dados-Mestre | `C-017`, `C-035` |
| DadosMestreFormScreen | form (com acção de aprovação) | Analista de Pricing, Dono de Dados-Mestre | `U-027` → `C-058` |
| CustosLogisticosFormScreen | form, secções por porto | Analista de Pricing | `C-016` |
| MargensAlvoFormScreen | form, visibilidade condicional por papel | Analista de Pricing, Comité de Aprovação | `C-002`, `C-008` |
| PrecoDiarioDashboardScreen | dashboard (com acção de aprovação, fundida com Aprovação de Carregamento; inclui exportar para Excel) | Analista de Pricing, Comité de Aprovação, Superior Hierárquico | `C-041`, `C-026`, `C-043`, `C-065` |
| HistoricoPrecosDashboardScreen | dashboard | Analista de Pricing, Comité de Aprovação | `C-018`, `R-004` |

Detalhe de controlos, estados de UI e visibilidade RBAC por ecrã: ver Claude Design Brief. Nada aqui é inventado além do que o blueprint aprovado carrega.

## 6. Fluxos, automação e transições de estado a implementar

### 6.1 Streams de automação (A6)

`(none)` — nenhum stream de automação assíncrono está registado na arquitectura (A6). As trocas de dados desta app são leituras/escritas directas sobre a BD SQL Server partilhada e uma referência de leitura ao SAP, mais uma exportação para Excel accionada pelo utilizador — nenhuma delas é um fluxo agendado ou disparado por evento externo.

### 6.2 Transições de estado

A ausência de stream em A6 **não** é a ausência de transição a especificar. `experience.mode: owned-internal`, e o blueprint aprovado carrega **duas** entidades com máquina de estados e passo de aprovação (`_blueprint/ux-blueprint_v05.yaml# entities`, remetido a `v01`).

O **conjunto** de transições é lido do blueprint. Actor, regra de validação, destinatário da notificação e gatilho são projectados do modelo de papéis (A7, o mesmo que a secção 8 projecta) e de `decisions.md`; onde nenhum deles os nomeia, renderizam `not named` **e** um item de trabalho em aberto na secção 16. Nada abaixo foi preenchido por analogia com outra entidade ou outro papel.

**`AprovacaoCarregamento` — `pendente → aprovado → carregado`** (`approval: true`, `C-026`, `C-043`)

| Transição | Quem transiciona | O que valida | O que notifica quem | O que dispara o ciclo |
|---|---|---|---|---|
| `pendente → aprovado` | Superior hierárquico da margem (`C-026`) — o **papel** está nomeado, a **pessoa** não | Aprovação independente e **anterior** à execução (`C-026`), com registo auditável de data/hora/aprovador (`C-043`). Invariante adicional **Assumed**, não confirmada pelo sponsor: nenhum preço abaixo do mínimo aprovado pode ser carregado (`A-011`) — renderiza como premissa com trabalho de validação, nunca como regra confirmada | `not named` — nenhuma fonte da arquitectura ou da decisão nomeia destinatário ou canal de notificação | O preço diário consolidado fica pronto para carregamento, a jusante da decisão de margem do comité diário (`C-002`) |
| `aprovado → carregado` | `not named` — o carregamento efectivo ocorre em X-Author, responsabilidade **relocada** para outra iniciativa (`relocated_responsibilities# carregamento-em-x-author`, `C-065`). Do lado PP existe apenas o registo do estado | `not named` — nenhuma regra registada diz o que confirma que o carregamento ocorreu | `not named` | `not named` — nenhum mecanismo registado devolve a confirmação do carregamento a esta app; o único canal registado no sentido de saída é a exportação para Excel accionada pelo utilizador |

**`DadosMestrePricing` — `proposta → aprovada → activa`** (`approval: true`)

| Transição | Quem transiciona | O que valida | O que notifica quem | O que dispara o ciclo |
|---|---|---|---|---|
| `proposta → aprovada` | **Propõe**: Analista de Pricing (`personas# AnalistaDePricing.proposes`, `C-005`, `C-013`). **Aprova**: o dono do dicionário de dados-mestre — Pedro O. (`C-058`) | Que a mudança passou por **aprovação formal** (`C-058`). O **processo** de controlo de mudança não está registado: `C-058` exige a aprovação e não descreve o processo — ver secções 2 e 16 | `not named` | `not named` — nenhuma fonte registada diz o que inicia uma proposta de mudança ao dicionário |
| `aprovada → activa` | `not named` | `not named` | `not named` | `not named` — nenhuma fonte registada diz o que activa uma versão aprovada do dicionário |

A persona `DonoDeDadosMestre` do blueprint `v01` ainda diz `owner: UNKNOWN` (`U-027`); a autoridade **actual** é `C-058`, que resolve `U-027` e nomeia Pedro O. — é essa que se projecta. Os restantes `not named` são itens de trabalho em aberto (secção 16), não lacunas de render.

## 7. Integrações

| Sistema | Direcção | Mecanismo | Classificação | Fronteira |
|---|---|---|---|---|
| BD SQL Server partilhada de pricing | Leitura/escrita | Conector relacional directo | Interno (`C-036`) | `shared-pricing-sql-server` — outside-platform, owner: equipa que já opera a BD |
| SAP OZP01/OZP02 | Leitura apenas | Referência API-mediada directa | Interno (`C-036`) | `sap-term-pricing-reference` — outside-platform, owner: IT centralizado (`C-063`) |
| Exportação para Excel | Saída, accionada pelo utilizador | Geração de ficheiro `.xlsx` | Interno | Formato exacto de colunas a confirmar com a outra iniciativa que trata do carregamento em X-Author (`C-065`) |

Autenticação e custódia de segredos: não especificadas nesta captura — item aberto (ver secção 16).

## 8. Implementação de segurança e roles

Classe de identidade: directório interno (Azure AD / equivalente) — sem identidade de serviço registada. Ponto de imposição: aplicação (Aprovação de Carregamento) + o que a BD partilhada impõe do seu lado. Papéis: Analista de Pricing (edita Custos Logísticos, Margens-Alvo; propõe Dados-Mestre), Comité de Aprovação (revê Margens-Alvo, Preço Diário), Superior Hierárquico (aprova Carregamento), Dono de Dados-Mestre (aprova Dados-Mestre). Segregação de funções: quem decide continua a carregar, mas com aprovação de superior antes do carregamento, deixando registo auditável (`C-026`, `C-043`). A forma da matriz (símbolos OK/EDIT-OWN/READ/CREATE/NONE, matriz Papel×Ecrã, Papel×Entidade×CRUD) segue `library/packs/pp/domain-knowledge/craft/security-craft.md` §B — existência e alcance dos controlos vêm de A7, não do craft.

## 9. Ambientes, governação e release

2 ambientes: Dev e Produção — sem ambiente de Teste formal separado (`C-067`). Rota de release: Dev → Produção, directa, sem tier intermédio de validação. Vinculação de residência: classificação Interno (`C-036`), sem constraint de residência evidenciado. Plano de política: IT centralizado (`C-063`), por extensão da sua operação das integrações partilhadas — **não confirmado como afirmação directa e distinta**; dono explícito do controlo de release (quem aprova a promoção Dev→Produção) permanece um item aberto (ver secção 16).

## 10. Monitorização e recuperação

Por componente de fronteira: `shared-pricing-sql-server` — sinal de saúde via o gateway já configurado (`C-062`), reconciliação após falha por quem já opera a BD hoje; `sap-term-pricing-reference` — falha de leitura reportada ao IT centralizado (`C-063`), recuperação pelo mesmo. As duas responsabilidades relocadas não engajam monitorização/recuperação desta plataforma — `not engaged`, pertencem aos seus próprios owners. O que "aceite" significa como evidência de recuperação: não definido nesta captura (item aberto, secção 16).

## 11. Obrigações do operador

Operador nomeado por componente: `shared-pricing-sql-server` → equipa que já opera essa BD; `sap-term-pricing-reference` e `termos-comerciais-contrato-a-termo` → IT centralizado da empresa (`C-063`); `carregamento-em-x-author` → outra iniciativa, fora desta engagement. Nenhum operador `UNKNOWN` permanece — todos os 4 componentes têm operador nomeado ou fronteira explicitamente fora do pack; nenhuma escolha estrutural aberta nesta secção.

## 12. Responsabilidade analítica / reporting

`not applicable` — nenhum requisito de reporting força hoje um segundo store ou cópia analítica.

## 13. Pacotes de trabalho de prova e condições de aceitação

| Obrigação de prova | Nível | Método | Dono | Financiada? | Pacote de trabalho | Condição de aceitação |
|---|---|---|---|---|---|---|
| Prova em ambiente produtivo (scope de solução inteira) | V4 | not specified further | not named | não | Executar o processo de pricing diário completo em ambiente produtivo, ponta a ponta, incluindo aprovação e carregamento | O ciclo diário completo (dados-mestre → cálculo → aprovação → output) corre sem intervenção manual fora do desenhado, com registo auditável completo |

Cenários de fricção do as-is que podem **acrescentar cenários** de teste (nunca determinam o nível de prova): pico de 2ª-feira com múltiplas fontes manuais (`C-006`); ficheiro a partir a meio do ciclo (`C-042`); divergência entre as 6 folhas de output antes da consolidação (`C-041`).

## 14. Sequenciamento

Dependências apenas, sem durações: (1) a BD SQL Server partilhada e a referência SAP já existem e já estão operadas (`C-057`, `C-003`) — não bloqueiam o arranque; (2) o desenho de schema de Dados-Mestre depende do dono já nomeado (`C-058`, satisfeito); (3) a consolidação num único modelo de cálculo depende da regra de desempate já registada (`C-059`, satisfeita); (4) a migração de dados depende da limpeza de chaves de contraparte, ainda por financiar (`C-019`); (5) a promoção Dev→Produção depende de A8 (rota directa, sem tier de validação), mas do dono explícito do controlo de release, ainda por confirmar (secção 16). A narrativa financeira não é autoridade de sequenciamento.

## 15. Migração e cutover

`not applicable — o conditional A9 de substituição de um artefacto existente nunca foi formalmente activado na versão aprovada (v05)`, apesar de esta solução substituir, na prática, o ficheiro Excel actual. Isto é registado como item aberto na secção 16, não inventado aqui.

## 16. Itens de trabalho em aberto

| Item | Dono | O que o resolveria | Ancoragem |
|---|---|---|---|
| Blast radius de `DF_GRID_1` (`#REF!`) — artefacto morto ou activo | `architecture` | Confirmação directa do Pedro O. | `R-008` |
| Confirmar com amostra de KAM se a capacidade de simulação deve ser preservada nalgum canal | `design` | Sessão de validação KAM já autorizada | `R-012` |
| Formato exacto do Excel exportado para a iniciativa de carregamento em X-Author | `implementation` | Alinhamento com o dono dessa outra iniciativa | `C-065` |
| Dono explícito do controlo de release (aprovação Dev→Produção) | `architecture` | Confirmação directa com IT centralizado | `C-067` |
| A9 — substituição do Excel actual nunca formalmente activada, apesar de ser o que esta solução faz na prática | `architecture` | Revisão explícita do blueprint (v06) activando o conditional de substituição de artefacto | `R-004` |
| Decomposição exacta em campos dos ~85 campos manuais hoje na sheet `Inputs` | `implementation` | Redesenho do dicionário de dados-mestre, uma vez a BD partilhada confirmada | `C-017` |
| Caminhos de acesso delegation-safe contra o esquema real da BD partilhada | `architecture` | Confirmação do esquema exacto da BD partilhada | — (ver `boundary_fragments# o_que_nao_se_sabe`, `_blueprint/ux-blueprint_v05.yaml`) |
| Autenticação e custódia de segredos para as integrações SQL/SAP | `implementation` | Definição pela equipa de implementação em Fase 0 | — |
| Retenção legal do histórico de preços | `evidence` | Confirmação jurídica explícita | `X-005` (Conflicted — nenhum lado escolhido aqui) |
| Destinatário e canal de notificação de **cada** transição de estado (secção 6.2) — nenhuma fonte os nomeia | `architecture` | Registar o plano de notificação em A7 (quem é avisado, por que canal, em que transição) | `_blueprint/ux-blueprint_v05.yaml# entities[].approval` |
| Gatilho e regra de confirmação de `aprovado → carregado` — nenhum mecanismo devolve a confirmação do carregamento a esta app | `architecture` | Alinhamento com o dono da iniciativa de carregamento em X-Author, ou decisão explícita de que o estado `carregado` é marcado à mão e por quem | `C-065` |
| Gatilho de uma proposta de mudança ao dicionário, e o que activa `aprovada → activa` | `architecture` | Desenho do ciclo de mudança do dicionário, junto com o processo de controlo de mudança que `C-058` exige | `C-058` |
| Processo mínimo de controlo de mudança do dicionário de dados-mestre — `C-058` exige aprovação formal e não descreve o processo | `architecture` | Declaração do processo (quem propõe, quem aprova, que registo fica) pela governance da equipa de pricing | `C-058` (portão parcialmente satisfeito, secção 2) |

Face a `v01`: os 2 itens ligados a A8/A9 (ambientes ausentes, dono da app ausente) fecharam-se com a aprovação de `v05` — deixam de aparecer aqui. O dono do controlo de release, que A8 deixou por confirmar, entra como novo item aberto.

Face a `v02`: **4 itens novos**, todos produzidos pela secção 6.2 e pelo portão parcialmente satisfeito da secção 2. Nenhum item de `v02` fechou e nenhum desapareceu. Os 4 existiam antes — a `v02` não os mostrava porque a secção 6 renderizava `(none)` sobre duas máquinas de estado vivas.
