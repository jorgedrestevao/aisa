## 4. Entidades e estruturas de dados

Uma linha por entidade. `NÃO ESPECIFICADO` = a fonte autorizada (architecture record + `ux-blueprint#entities`) não declara o item; tem de ser fechado antes da implementação, não é decidido aqui.

| # | Entidade | Dono (autoridade do registo) | Modo de acesso | Campos | Relações | Índices |
|---|---|---|---|---|---|---|
| E-1 | `DadosMestrePricing` — Dados-Mestre de Pricing | Sistema externo de registo: SQL Server partilhado de pricing (`C-017`, `C-057`, `C-058`, `C-062`) | keep-in-place | Não itemizados (`fields_itemized: false`). Âmbito conhecido: dicionário contraparte × combustível × métrica, hoje 291 named ranges no Excel (`C-017`, `C-035`, `R-006`). Decomposição dos ~85 campos manuais está aberta — ver `open_architecture_choices` | NÃO ESPECIFICADO | NÃO ESPECIFICADO |
| E-2 | `CustosLogisticos` — Custos Logísticos | Sistema externo de registo: SQL Server partilhado de pricing (`C-006`, `C-016`, `C-057`, `C-062`) | keep-in-place | Não itemizados (`fields_itemized: false`). Âmbito: custo por porto e modo de transporte (carro-tanque, barcaça, pipeline); actualização mensal (`C-016`, `C-006`) | NÃO ESPECIFICADO | NÃO ESPECIFICADO |
| E-3 | `MargensAlvo` — Margens-Alvo | Sistema externo de registo: SQL Server partilhado de pricing (`C-006`, `C-016`, `C-057`, `C-062`) | keep-in-place | Não itemizados (`fields_itemized: false`). Âmbito: margem por produto, tipo de cliente e data, decidida no comité diário (`C-002`, `C-008`, `C-039`, `C-046`) | NÃO ESPECIFICADO | NÃO ESPECIFICADO |
| E-4 | `HistoricoPrecos` — Histórico de Preços | Sistema externo de registo: SQL Server partilhado de pricing (`C-018`, `R-004`, `C-057`, `C-060`, `C-062`) | keep-in-place | Não itemizados. Âmbito: registo estruturado e consultável do histórico diário, substituindo o arquivo de ficheiros soltos (`C-018`, `R-004`). Só leitura na app (`readonly: true`) | NÃO ESPECIFICADO | NÃO ESPECIFICADO |
| E-5 | `TermosComerciaisCliente` — Termos Comerciais de Cliente (contrato a termo) | Sistema externo de registo: SAP (`C-052`, `C-003`) | virtualized | Não itemizados. Não gerido nesta app (`external: true`, `owned_here: false`); referenciado apenas para leitura | NÃO ESPECIFICADO | NÃO ESPECIFICADO |
| E-6 | `PrecoDiarioConsolidado` — Preço Diário Consolidado | NÃO ESPECIFICADO — nenhum domínio de `record_authority` cobre esta entidade | NÃO ESPECIFICADO | Não itemizados. Âmbito: output único que substitui as 6 folhas hoje divergentes (`C-041`) e alimenta o carregamento em X-ALT (`C-001`, `R-007`). Só leitura (`readonly: true`), entidade de output (`feeds_output: true`) | NÃO ESPECIFICADO | NÃO ESPECIFICADO |
| E-7 | `AprovacaoCarregamento` — Aprovação de Carregamento | NÃO ESPECIFICADO — nenhum domínio de `record_authority` cobre esta entidade | NÃO ESPECIFICADO | Não itemizados. Âmbito: passo de aprovação do superior hierárquico antes do carregamento, resolvendo a separação de funções (`C-026`, `C-043`) | NÃO ESPECIFICADO | NÃO ESPECIFICADO |

### 4.1 Máquinas de estado e aprovação

Declaradas na fonte, vinculativas para a implementação:

| Entidade | Estados | Aprovação exigida |
|---|---|---|
| E-1 `DadosMestrePricing` | `proposta` → `aprovada` → `activa` | Sim (`approval: true`) |
| E-7 `AprovacaoCarregamento` | `pendente` → `aprovado` → `carregado` | Sim (`approval: true`) |

As restantes cinco entidades não declaram máquina de estado nem passo de aprovação.

### 4.2 Consequências do modo de acesso

- E-1 a E-4: `keep-in-place`. O SQL Server partilhado de pricing continua a ser o sistema de registo; a aplicação lê e escreve no sítio, sem cópia de dados-mestre para dentro da app.
- E-5: `virtualized`. Leitura projectada a partir do SAP; sem escrita e sem cópia persistente.
- E-4 e E-6: `readonly: true` do lado da aplicação — sem edição pelo utilizador.

### 4.3 Lacunas a fechar antes de construir

1. **Itemização de campos** — as 7 entidades têm `fields_itemized: false` ou nenhuma lista de campos. E-1 tem uma decisão de arquitectura explicitamente aberta (decomposição dos ~85 campos manuais / 291 named ranges) em `open_architecture_choices`.
2. **Relações** — nenhuma relação é declarada na fonte. As referências entre entidades sugeridas pelas descrições (E-6 como output consolidado, E-5 como leitura de contrato) não são relações modeladas e não são inferidas aqui.
3. **Índices** — nenhum índice, chave ou estratégia de unicidade é declarada na fonte, incluindo para as tabelas mantidas em SQL Server.
4. **Autoridade de E-6 e E-7** — o `record_authority` do blueprint aprovado (v05) não cobre nem o Preço Diário Consolidado nem a Aprovação de Carregamento. Onde estas duas vivem, e quem é o seu dono, fica por decidir.
