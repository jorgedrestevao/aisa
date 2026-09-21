# Enquadramento — pricing-marinha-cenario

> Dono do processo: Pedro O. — Responsável de Pricing Marinha
> Data da declaração: 2026-09-11
> Executor que registou: corrida interactiva da camada 2 de B4 (perguntas emitidas por `AskUserQuestion`)
> Pedido literal (`context.json.literal_request`): "Precissmos de ajuda a melhor este processo de pricing, o excel já foi corronpido varia vezes e só eu sei porá-lo."

## T1 · actors

O comité de pricing é quem manda; eu só executo o cálculo diário.

## T2 · trigger

Começa todos os dias de manhã, quando chegam as cotações do dia.

## T3 · activities

Recolher as cotações, lançar a cedência do Supply, calcular o preço por produto e por unidade, levar as margens ao comité quando mudam, e publicar o preço do dia. A decisão de margem é do comité.

## T4 · outcomes

Sai o preço diário por produto, para os comerciais e para o carregamento. Corre bem quando o preço sai antes da hora de carregamento e a margem apurada bate com a valorizada.

## activation · pricing

Pergunta emitida: *A saída deste processo é um preço, cotação, margem ou valorização?*  Resposta do dono: **Sim**.

## pricing
<!-- INTAKE-SET: pricing -->

### P1 · sold_what_when

Vende-se combustível de marinha, por carregamento, ao longo da semana.

### P2 · price_fixing_moment

Eu defino um preço hoje, para uma venda que só se vai verificar na próxima semana.

### P3 · cost_driver

O custo de cedência é indexado a cotações Platts.

### P4 · valuation_driver

Uma venda hoje é valorizada à média das cotações da semana anterior.

### P5 · uncertainty_shape

A incerteza decresce ao longo da semana: 0 a 1 cotações à 2ª feira, 4 à 6ª.

## T5 · invariants

O preço fixa-se hoje como referência para uma venda que se verifica na semana seguinte. A venda é valorizada à média das cotações da semana anterior à venda. O custo de cedência é indexado a Platts. A incerteza decresce ao longo da semana. O efeito é valorização errada, não venda perdida.

## T6 · failure_today

O ficheiro já foi corrompido várias vezes e só eu o sei repor. Quando isso acontece, faço-o nas minhas férias, e o preço do dia atrasa.

## T7 · change_requested

Queremos tirar isto de um ficheiro que só uma pessoa sabe reparar, sem perder a forma como o preço se calcula.

## Invariantes

Lidos de **T5**, verbatim, uma linha por frase declarada.

| id | invariante | o que orienta | fonte |
|---|---|---|---|
| M-1 | O preço fixa-se hoje como referência para uma venda que se verifica na semana seguinte. | o momento em que o preço é decidido, e o horizonte que a solução tem de cobrir | declaração do dono, 2026-09-11 |
| M-2 | A venda é valorizada à média das cotações da semana anterior à venda. | o alvo da projecção: o fecho da média semanal | declaração do dono, 2026-09-11 |
| M-3 | O custo de cedência é indexado a Platts. | fontes de cotação e o momento em que cada uma se conhece | declaração do dono, 2026-09-11 |
| M-4 | A incerteza decresce ao longo da semana. | o problema é de 2ª e 3ª feira; qualquer solução mede-se aí | declaração do dono, 2026-09-11 |
| M-5 | O efeito é valorização errada, não venda perdida. | o KPI é margem apurada vs valorizada | declaração do dono, 2026-09-11 |

## Autoridades nomeadas pelo dono

Pergunta emitida: *Para além de ti, quem tem autoridade para confirmar factos sobre este processo?*

Resposta: **"Ninguém — só eu. O Supply, o IT e os comerciais são fontes, não autoridades."**

## Regras

- O enquadramento é a **hipótese do dono**, não facto verificado: `/frame` confirma ou corrige cada `M-n` com evidência.
- Nenhum `M-n` foi inferido do pedido literal nem do `_capture`; só o que o dono disse.
- Sem vendor, sem produto, sem solução em `M-n`.
