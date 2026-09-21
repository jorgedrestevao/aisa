## 4. Entidades e estruturas de dados

Fonte: architecture record `record_authority[]` (ux-blueprint_v05.yaml, versão aprovada) + `ux-blueprint#entities` (v05 remete para v01).

Uma linha por entidade. `Dono` = autoridade do registo declarada no architecture record; `—` significa que a autoridade não está declarada nas fontes autorizadas (lacuna, ver §4.2).

### 4.1 Entidades

| Entidade | Etiqueta | Dono (autoridade do registo) | Modo de acesso | Campos | Relações | Índices | Refs SU |
|---|---|---|---|---|---|---|---|
| `DadosMestrePricing` | Dados-Mestre de Pricing | Sistema de registo externo — SQL Server partilhado de pricing | keep-in-place | Não itemizados (`fields_itemized: false`). Decomposição dos ~85 campos manuais é uma escolha de arquitectura aberta (`open_architecture_choices`). Hoje: dicionário contraparte × combustível × métrica, 291 named ranges no Excel | Não declaradas | Não declarados | C-017, C-035, R-006 (+ autoridade: C-017, C-057, C-058, C-062) |
| `CustosLogisticos` | Custos Logísticos | Sistema de registo externo — SQL Server partilhado de pricing | keep-in-place | Não itemizados (`fields_itemized: false`). Escopo declarado: custo por porto e por modo de transporte (carro-tanque, barcaça, pipeline); actualização mensal | Não declaradas | Não declarados | C-016, C-006 (+ autoridade: C-006, C-016, C-057, C-062) |
| `MargensAlvo` | Margens-Alvo | Sistema de registo externo — SQL Server partilhado de pricing | keep-in-place | Não itemizados (`fields_itemized: false`). Escopo declarado: margem por produto, por tipo de cliente e por data, decidida no comité diário | Não declaradas | Não declarados | C-002, C-008, C-039, C-046 (+ autoridade: C-006, C-016, C-057, C-062) |
| `PrecoDiarioConsolidado` | Preço Diário Consolidado | — (não declarada no `record_authority`) | — | Não itemizados. Somente-leitura (`readonly: true`); alimenta output (`feeds_output: true`) — o carregamento em X-ALT. Substitui as 6 folhas hoje divergentes | Não declaradas | Não declarados | C-041, C-001, R-007 |
| `AprovacaoCarregamento` | Aprovação de Carregamento | — (não declarada no `record_authority`) | — | Não itemizados. Requer aprovação (`approval: true`); máquina de estados: `pendente → aprovado → carregado`. Passo de aprovação do superior hierárquico antes do carregamento (resolução de SoD) | Não declaradas | Não declarados | C-026, C-043 |
| `HistoricoPrecos` | Histórico de Preços | Sistema de registo externo — SQL Server partilhado de pricing | keep-in-place | Não itemizados. Somente-leitura (`readonly: true`). Escopo declarado: registo estruturado e consultável do histórico diário, substituindo o arquivo de ficheiros soltos | Não declaradas | Não declarados | C-018, R-004 (+ autoridade: C-018, R-004, C-057, C-060, C-062) |
| `TermosComerciaisCliente` | Termos Comerciais de Cliente (contrato a termo) | Sistema de registo externo — SAP | virtualized | Não itemizados. Externa (`external: true`, `owned_here: false`): não gerida nesta app, referenciada apenas para leitura | Não declaradas | Não declarados | C-052, C-003 |

Máquinas de estado e aprovação declaradas (as únicas duas nas fontes):

| Entidade | Estados | Aprovação |
|---|---|---|
| `DadosMestrePricing` | `proposta → aprovada → activa` | Sim |
| `AprovacaoCarregamento` | `pendente → aprovado → carregado` | Sim |

### 4.2 Lacunas a fechar antes da construção

As fontes autorizadas não contêm o material que o template pede nestas colunas. Não há inferência aqui — cada linha é um item de trabalho, não uma decisão já tomada:

1. **Campos.** Nenhuma das 7 entidades tem campos itemizados. Para `DadosMestrePricing` a decomposição dos ~85 campos manuais está explicitamente registada como escolha de arquitectura aberta (`open_choice_ref`); para as restantes 6 não há sequer registo da escolha. Bloqueia a definição do esquema físico.
2. **Relações.** Nenhuma relação entre entidades está declarada nas fontes. As dependências funcionais são visíveis na prosa (o preço consolidado depende de dados-mestre, custos logísticos e margens-alvo; a aprovação de carregamento refere-se a um carregamento; os termos comerciais são consultados por cliente), mas cardinalidade, obrigatoriedade e chaves não estão fixadas — não são derivadas aqui.
3. **Índices.** Nenhum índice ou chave alternativa declarado, para nenhuma entidade.
4. **Autoridade de registo em falta.** `PrecoDiarioConsolidado` e `AprovacaoCarregamento` não aparecem no `record_authority[]`: não têm dono nem modo de acesso declarados. Como `PrecoDiarioConsolidado` está marcado `readonly: true` e `feeds_output: true`, é preciso declarar quem o escreve e onde reside antes de definir o modelo de dados.
5. **Consistência entre fontes a confirmar.** `MargensAlvo` e `CustosLogisticos` partilham um único domínio no `record_authority` ("Margens-alvo e custos logísticos diários"), mas são duas entidades distintas em `entities`. Confirmar se são duas estruturas separadas na mesma fonte de registo ou uma só.
