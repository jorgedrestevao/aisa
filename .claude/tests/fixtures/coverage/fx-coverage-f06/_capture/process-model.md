# Process Model — fx-coverage-f06

> Modelo de processo reconstruído a partir da captura L1/L3 dos dois workbooks. Fixture
> sintética: nenhum conteúdo descreve uma organização real.

## 1. File map

| ficheiro | folhas | papel |
|---|---|---|
| `registo-de-lotes.xlsx` | Entradas, Resumo de Lotes, Resumo Aditivos, Parametros | registo corrente + as duas saídas de resumo + parâmetros |
| `registo-de-lotes-2024.xlsx` | Entradas, Resumo Aditivos | arquivo do ano anterior; a folha `Resumo Aditivos` repete o nome, não o conteúdo |
| `fluxo-de-libertacao.pptx` | — | formato fora dos tiers de captura — `not captured`, lido pelo humano |

## 2. Column classification

18 colunas no workbook corrente: 12 de escrita, 6 calculadas. Um grupo de três colunas
de forma repetida (`Custo_Posto_A/B/C`) e uma entrada de dicionário sem dados
(`Custo_Posto_D`).

## 3. Business rules (PM-NNN)

| id | regra | locator |
|---|---|---|
| PM-001 | O resultado do lote é o valor medido multiplicado pelo factor de resultado | `Resumo de Lotes!C` → `Parametros!$B$2` |
| PM-002 | A percentagem de aditivo é o valor medido dividido pela base de aditivo | `Resumo Aditivos!D` → `Parametros!$B$3` |
| PM-003 | As duas folhas de resumo derivam da mesma folha de entradas, linha a linha | `Resumo de Lotes!A:B`, `Resumo Aditivos!A:B` |
| PM-004 | O estado do lote é escrito à mão na folha de resumo | `Resumo de Lotes!D` |
| PM-005 | O limite de alerta existe nos parâmetros e não é referido por nenhuma fórmula | `Parametros!B4` |
| PM-006 | O workbook do ano anterior tem a mesma folha de saída com outro conteúdo | `registo-de-lotes-2024.xlsx!Resumo Aditivos` |

## 4. Process synopsis (cross-source)

- `OBSERVED` — saída: `Resumo de Lotes`, consumida pelas equipas de produção por email (C-006).
- `OBSERVED` — saída: `Resumo Aditivos`, não enviada; o ficheiro é gravado para consulta (C-007).
- `OBSERVED` — saída: ficheiro de integração com duas colunas para o sistema de lotes (C-008).
- `OBSERVED` — obrigação de transformação: o resultado e a percentagem são calculados a partir das entradas (PM-001, PM-002).
- `OBSERVED` — invariante: quem regista não liberta (C-002, C-005).
- `INFERRED` — o limite de alerta terá sido usado por uma versão anterior (PM-005).
- `HYPOTHESIS` — o grupo `Custo_Posto_*` é resíduo de um estudo (confirmado depois em C-009).

## 5. Anomalies & silent failures

`Parametros!B4` (limite de alerta) não é referido por nenhuma fórmula do workbook.

## 6. Interrogation list (PM-U-NNN)

| id | pergunta | criticidade |
|---|---|---|
| PM-U-001 | O `Resumo Aditivos` tem consumidor a jusante além da consulta interna? | Critical |
| PM-U-002 | O limite de alerta ainda governa alguma decisão? | Med |
| PM-U-003 | As colunas `Custo_Posto_*` alimentam algum cálculo? | Med |

## 7. Not captured

`fluxo-de-libertacao.pptx` — formato fora dos tiers de captura. Nada foi extraído; não é
falha do ficheiro nem prova de ausência de conteúdo material.
