# Snapshot `b81d39c` — diferenças justificadas (A2, plano de endurecimento §4)

Cada linha é uma diferença entre `bp_read` em `b81d39c` e `bp_read` com o parser Y1-Y7. Um diff que não esteja aqui é regressão (`test_blueprint_yaml.py`).

| ficheiro | chave | item | regra | o que mudou |
|---|---|---|---|---|
| `pricing-marinha-pilot-1-val-b/_blueprint/ux-blueprint_v02.yaml` | `open_choices` | 0 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |
| `pricing-marinha-pilot-1-val-b/_blueprint/ux-blueprint_v02.yaml` | `structural_open` | — | Y7-in-Y4 | `structural_open` passa a incluir a escolha `structural: true` que o leitor antigo dobrava para texto |
| `pricing-marinha-pilot-1-val-b/_blueprint/ux-blueprint_v03.yaml` | `open_choices` | 0 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |
| `pricing-marinha-pilot-1-val-b/_blueprint/ux-blueprint_v03.yaml` | `structural_open` | — | Y7-in-Y4 | `structural_open` passa a incluir a escolha `structural: true` que o leitor antigo dobrava para texto |
| `pricing-marinha-pilot-1-val-b/_blueprint/ux-blueprint_v04.yaml` | `open_choices` | 3 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |
| `pricing-marinha-pilot-1-val-b/_blueprint/ux-blueprint_v05.yaml` | `open_choices` | 3 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |
| `pricing-marinha-pilot-1/_blueprint/ux-blueprint_v02.yaml` | `open_choices` | 0 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |
| `pricing-marinha-pilot-1/_blueprint/ux-blueprint_v02.yaml` | `structural_open` | — | Y7-in-Y4 | `structural_open` passa a incluir a escolha `structural: true` que o leitor antigo dobrava para texto |
| `pricing-marinha-pilot-1/_blueprint/ux-blueprint_v03.yaml` | `open_choices` | 0 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |
| `pricing-marinha-pilot-1/_blueprint/ux-blueprint_v03.yaml` | `structural_open` | — | Y7-in-Y4 | `structural_open` passa a incluir a escolha `structural: true` que o leitor antigo dobrava para texto |
| `pricing-marinha-pilot-1/_blueprint/ux-blueprint_v04.yaml` | `open_choices` | 3 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |
| `pricing-marinha-pilot-1/_blueprint/ux-blueprint_v05.yaml` | `open_choices` | 3 | Y7-in-Y4 | o texto do `choice` deixa de arrastar `structural:` / `would_be_settled_by:` / `su_ref:`; esses campos passam a ler-se |

## Regra Y7-in-Y4

Escalar em bloco (`>`/`|`) como **primeiro** par de um item `- k: v`. O leitor de `b81d39c` só tratava `pend_key` para o par corrente e, como as chaves irmãs vinham a seguir sem nova linha `- `, eram anexadas ao escalar. Consequência histórica: em `pricing-marinha-pilot-1` v02 e v03 (e nas cópias `-val-b`) uma escolha `structural: true` ficou invisível ao motor — `structural_open` reportava menos uma escolha. As versões correntes (v06) e a aprovada (v05) não têm este padrão em escolhas estruturais, por isso o estado do engagement não muda.

Medido em `b81d39c`: **0** valores `none` sem aspas nos 12 blueprints reais — a correcção `none`→texto não produz diff real; prova-se por fixture.
