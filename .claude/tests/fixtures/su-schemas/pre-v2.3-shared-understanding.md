# Shared Understanding — fixture pré-v2.3

> Engagement: fixture de esquema antigo
> Sponsor: —
> Iniciado: 2026-01-01
> Fase actual: Discovery
> Última actualização: 2026-01-01
> Saúde epistémica: —

<!--
  Esta SU existe para provar TOLERÂNCIA, não para ser realista.

  O esquema v2.3 acrescentou `verificado_em` e `validade` (meias-vidas epistémicas) e
  `custo`/`swing` (economia das perguntas). Uma SU escrita antes disso não os tem — e o
  parser tem de a ler na mesma, inferindo os valores em falta, porque engagements antigos
  não se reescrevem.

  Antes desta fixture, a garantia era exercida contra `projects/`, que é gitignored. Num
  clone limpo não havia SU antiga nenhuma e o caso falhava com «no pre-v2.3 SU left to
  prove tolerance against» — o que significava que TODA a suite só era verde em máquinas
  com material privado de cliente. Modelada a partir de uma SU real pré-v2.3
  (`cae-automation-pilot-4`), sem nada do conteúdo dela.
-->

## Confirmed

| id | lens | claim | evidência | ronda |
|---|---|---|---|---|
| C-001 | operations | O processo corre em três passos manuais | fonte: entrevista com o dono do processo | R-01 |

## Assumed

| id | lens | claim | base da assumption | ronda |
|---|---|---|---|---|
| A-001 | data | O volume mensal mantém-se estável | base: média dos últimos seis meses | R-01 |

## Unknown

| id | lens | pergunta | quem responde | criticidade | ronda |
|---|---|---|---|---|---|
| U-001 | data | Quem aprova uma excepção ao limite? | role: dono do processo | Critical | R-01 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
