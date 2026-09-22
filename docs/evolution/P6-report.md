# P6 — Coerência, fontes e Coverage

Estado: **GO**

## Identidade e precondições

- **Data/ambiente:** 2026-09-22 · Linux · Python 3.11.15
- **GO anterior:** P5 **GO** — 53 ficheiros / 2156 testes.
- **Contratos:** `MIGRATION_AND_COVERAGE.md` §C3 (fontes e proveniência) e §C4 (Coverage);
  `library/kernel/states.md` → *Transitions*.
- **Casos:** L06–L10 + C01–C08 — **13 dos 61**, o maior bloco depois de P2.

## Nota pré-alteração

- **Problema:** o P4 só cobria `Unknown → Confirmed/Assumed`. Faltavam findings, contradições,
  retirada, validade e dependências. E o Coverage não sabia nada do grafo.
- **Risco maior, e foi o que guiou o desenho:** criar um **segundo** comparador de atualidade.
  O contrato proíbe-o e o próprio código avisa.
- **Reversão:** dois ficheiros de teste novos; dois módulos existentes estendidos.

## Alterações realizadas

| Ficheiro | O quê |
|---|---|
| `library/kernel/tools/graph.py` | `+dependency_fingerprint`, `+as_coverage_source` |
| `library/kernel/tools/resolve.py` | `+revalidate`, `+withdraw`, `+resolve_conflict`, `+accept_risk`, `+finding`, `+dispose_finding`, `+dependents_of`, `+decision_rewritten_by` |
| `.claude/tests/test_coverage_graph.py` | C01–C08, 29 testes |
| `.claude/tests/test_knowledge_lifecycle.py` | L06–L10, 24 testes |

**Zero linhas alteradas no `coverage.py`.**

### A integração precisou de uma só primitiva

`coverage.py` já tinha `su_fingerprint`, `decision_fingerprint`, `inventory_digest` e
`check_freshness`. E o `finalize_recheck` já explicava, em comentário, porque não pode haver
um segundo comparador:

> *«É `check_freshness` — de propósito. Ter uma segunda comparação aqui seria ter duas
> definições de "a base mudou", e mais cedo ou mais tarde elas divergiriam.»*

Faltava uma coisa: **o fingerprint do subconjunto do grafo efectivamente consumido**. Entra
como mais uma fonte `use: freshness` no `basis`, e o `check_freshness` compara-a sem saber
que é um grafo.

Uma primitiva, as três propriedades do contrato:

| | Reordenar | Aresta de navegação | Aresta consumida |
|---|---|---|---|
| Dependência consumida | igual (C02) | **igual** (C04) | **muda** (C05) |
| Revisão global do store | igual | **muda** | muda |

O C04 afirma a distinção de frente: é exactamente por isso que **não se usa a versão global**.

### Casos → evidência

| Caso | Afirma |
|---|---|
| L06 | os quatro campos do finding (distinção, evidência, criticidade, acção) viajam como props e **sobrevivem a processo novo**; dispor/reabrir **acrescenta** à história em vez de a substituir; sem base é recusado |
| L07 | os dois lados sobrevivem em ambos os caminhos; **inverter a ordem não muda o veredicto** — é assim que se testa «sem escolher por recência»; sem dono resolve para `Assumed`, não `Confirmed` |
| L08 | retirada sai «por um marcador na última coluna e por mais nada»; não vira facto, não apaga história; risco aceite continua `Risky` com base registada; ambos exigem razão |
| L09 | facto inalterado → **edição sancionada**, renova `verificado_em` **sem linha nova**; facto mudado → fluxo normal com `was`, e **nunca** renova |
| L10 | revalidação direccionada com um teste que afirma que **sobra alguém de fora**; uma resposta **nunca** reescreve uma decisão |
| C01 | mesmas entradas mantêm atualidade; reabrir não move a revisão |
| C02 | reordenar não invalida nem move o fingerprint |
| C03 | claim consumida alterada → `stale`, **com a fonte nomeada**; `stale` não quer dizer «a conclusão é falsa» |
| C04 | aresta de navegação não torna nada stale, **embora a revisão global mude** |
| C05 | aresta consumida alterada muda o fingerprint; o conjunto consumido fica registado, para a revisão ser auditável |
| C06 | a exclusão que impede a aprovação de se auto-invalidar está guardada de regressão; excluir aprovações **não** é excluir decisões |
| C07 | fonte alterada reporta os dois hashes; renomear aparece como removida+acrescentada; grafo ilegível **não** passa por check limpo; registo sem base é `not_evaluated`, não `current` |
| C08 | pendência fecha o gate; espelho divergente é reportado e **não prevalece**; **nenhum flag** de coverage entra no `_state.json` |

## Verificação

| Runner | Collected | Passed | Failed | Skipped | Xfail | Errors |
|---|---:|---:|---:|---:|---:|---:|
| `python3 <ficheiro>` × 55 | **2209** | 2192 | **0** | 14 | 3 | **0** |

2156 → 2209 = +53, exactamente os testes novos. Zero regressões.

### Nota de processo

A verificação de contagem por classe — o check que apanhou três falsos verdes nesta linha de
trabalho — **falhou desta vez com `SyntaxError`** (backslash dentro de expressão f-string).
Só dei por isso porque li o output em vez do exit status. Refeita: 8 e 5 classes, 29 e 24
testes, nada depois do bloco `main`.

O check que protege contra falsos verdes pode ele próprio falhar em silêncio. Ler o output.

## Resultado e limitações

### GO/NO-GO por critério

| Critério (P6) | Veredicto |
|---|---|
| Cobrir Unknowns, Findings, Conflicted, Risky, Assumed, revalidação/expiração | **Cumprido** — L06–L10 |
| Respeitar `was`, `resolved`, N/A e retirada | **Cumprido** — L08, L09 |
| Comparação semântica por campo/ID, não equivalência de prosa | **Cumprido** — fingerprints sobre estrutura |
| Campo material tem autoridade existente **ou** fingerprint — nunca ambos | **Cumprido** — a dependência entra como fonte única |
| Reutilizar `coverage.py` e os seus fingerprints | **Cumprido** — zero linhas alteradas |
| Sem `coverage_valid`/`coverage_stale`/percentagens no estado | **Cumprido** — C08 |
| Zero divergência material; nenhum flag substitui o motor | **Cumprido** |
| L06–L10 + C01–C08 + regressão completa | **Cumprido** — 13/13, 55/55 |

**GO.**

### Limitações, declaradas

1. **As funções do ciclo decidem, não escrevem.** `revalidate`, `withdraw`, `resolve_conflict`
   e `accept_risk` devolvem o veredicto e a forma da marcação; ligá-las ao `apply()` que
   publica pelo coordenador é trabalho que ficou por fazer. O que está provado é a **regra**,
   não o percurso completo até ao disco.
2. **`consumed` é declarado, não inferido.** Quem escreve a revisão diz o que consumiu. Um
   consumidor que mentisse sobre o seu próprio conjunto não é detectado — e é a razão de o
   conjunto ficar registado em `as_coverage_source`, para a revisão ser auditável.
3. **As etapas `blueprint` e `render` não foram exercitadas ponta-a-ponta** com grafo. C06
   guarda a exclusão de regressão; não corre um fluxo de aprovação real.

### Próxima acção concreta

**P7** — projecções e UX de todo o workflow (U01–U05). É onde a limitação 1 se fecha e onde
os pontos de entrada passam de facto pelo bootstrap.
