# Cenário de intake — pricing

> Camada 2 de B4, **corrida interactiva**. `## INPUT` e `## OWNER-SCRIPT` foram fixados antes;
> `## ASKED` regista as perguntas **efectivamente emitidas** e a resposta escolhida em cada
> uma; `## ENQUADRAMENTO` é o ficheiro que a corrida escreveu, lido do disco.
>
> **Como foi corrido.** Cada pergunta desta lista foi emitida por `AskUserQuestion` nesta
> sessão, uma a uma, pela ordem que `aisa-orient` passo 3 declara. O dono respondeu ao vivo,
> escolhendo entre as opções apresentadas; a resposta registada é o texto da opção escolhida,
> verbatim. Nenhuma resposta foi lida de um guião durante a corrida — o `OWNER-SCRIPT` serve
> agora de **baseline**, e onde a resposta viva divergiu dele, diz-se em `## DIVERGENCES`.
>
> Engagement de teste isolado: `docs/runtime-hardening/intake-scenarios/_runs/pricing-marinha-cenario/`.
> Nenhum engagement real foi tocado.

## INPUT

```
Precissmos de ajuda a melhor este processo de pricing, o excel já foi corronpido varia vezes e só eu sei porá-lo.
```

## OWNER-SCRIPT

Baseline fixada **antes** da corrida, para se poder ver o que divergiu.

- **activation (`A saída deste processo é um preço, cotação, margem ou valorização?`)**: **Sim**
- **T1 actors**: "O comité de pricing é quem manda; eu só executo o cálculo diário."
- **T2 trigger**: "Começa todos os dias de manhã, quando chegam as cotações do dia."
- **T3 activities**: "Recolher as cotações, lançar a cedência do Supply, calcular o preço por produto e por unidade, levar as margens ao comité quando mudam, e publicar o preço do dia. A decisão de margem é do comité."
- **T4 outcomes**: "Sai o preço diário por produto, para os comerciais e para o carregamento. Corre bem quando o preço sai antes da hora de carregamento e a margem apurada bate com a valorizada."
- **T5 invariants**: "O preço fixa-se hoje como referência para uma venda que se verifica na semana seguinte. A venda é valorizada à média das cotações da semana anterior à venda. O custo de cedência é indexado a Platts. A incerteza decresce ao longo da semana. O efeito é valorização errada, não venda perdida."
- **T6 failure_today**: "O ficheiro já foi corrompido várias vezes e só eu o sei repor. Quando isso acontece, faço-o nas minhas férias, e o preço do dia atrasa."
- **T7 change_requested**: "Queremos tirar isto de um ficheiro que só uma pessoa sabe reparar, sem perder a forma como o preço se calcula."
- **P1 sold_what_when**: "Vende-se combustível de marinha, por carregamento, ao longo da semana."
- **P2 price_fixing_moment**: "Eu defino um preço hoje, para uma venda que só se vai verificar na próxima semana."
- **P3 cost_driver**: "O custo de cedência é indexado a cotações Platts."
- **P4 valuation_driver**: "Uma venda hoje é valorizada à média das cotações da semana anterior."
- **P5 uncertainty_shape**: "A incerteza decresce ao longo da semana: 0 a 1 cotações à 2ª feira, 4 à 6ª."
- **autoridades**: "Ninguém — só eu. O Supply, o IT e os comerciais são fontes, não autoridades."
- **funding gate**: Não

## ASKED

As 15 perguntas emitidas, por ordem, com a resposta escolhida. `[orient]` = `aisa-orient`
passo 3 · `[start]` = `aisa-start` passo 4.

1. `[orient]` T1 `actors` — Quem faz parte disto, que papéis intervêm, e quem manda no processo?
   → **O comité manda**: "O comité de pricing é quem manda; eu só executo o cálculo diário."
2. `[orient]` T2 `trigger` — O que faz este processo começar, e com que frequência?
   → **Cotações da manhã, diariamente**: "Começa todos os dias de manhã, quando chegam as cotações do dia."
3. `[orient]` T3 `activities` — O que se faz, por ordem, e onde é que se decide alguma coisa?
   → **Cotações, cedência, cálculo, comité**: "Recolher as cotações, lançar a cedência do Supply, calcular o preço por produto e por unidade, levar as margens ao comité quando mudam, e publicar o preço do dia. A decisão de margem é do comité."
4. `[orient]` T4 `outcomes` — O que sai no fim, para quem, e como se sabe que correu bem?
   → **Preço diário por produto**: "Sai o preço diário por produto, para os comerciais e para o carregamento. Corre bem quando o preço sai antes da hora de carregamento e a margem apurada bate com a valorizada."
5. `[orient]` **activation** — A saída deste processo é um preço, cotação, margem ou valorização?
   → **Sim**
6. `[orient]` P1 `sold_what_when` — O que se vende, e quando?
   → **Combustível por carregamento**: "Vende-se combustível de marinha, por carregamento, ao longo da semana."
7. `[orient]` P2 `price_fixing_moment` — Quando é que o preço se fixa, e quando é que a venda acontece?
   → **Fixa hoje, vende para a semana**: "Eu defino um preço hoje, para uma venda que só se vai verificar na próxima semana."
8. `[orient]` P3 `cost_driver` — O que determina o custo?
   → **Cedência indexada a Platts**: "O custo de cedência é indexado a cotações Platts."
9. `[orient]` P4 `valuation_driver` — O que determina a valorização?
   → **Média da semana anterior**: "Uma venda hoje é valorizada à média das cotações da semana anterior."
10. `[orient]` P5 `uncertainty_shape` — De onde vem a incerteza, e como evolui no tempo?
   → **Decresce ao longo da semana**: "A incerteza decresce ao longo da semana: 0 a 1 cotações à 2ª feira, 4 à 6ª."
11. `[orient]` T5 `invariants` — O que tem de se manter sempre verdadeiro, as regras que ninguém pode quebrar?
   → **As cinco de pilot-3**: "O preço fixa-se hoje como referência para uma venda que se verifica na semana seguinte. A venda é valorizada à média das cotações da semana anterior à venda. O custo de cedência é indexado a Platts. A incerteza decresce ao longo da semana. O efeito é valorização errada, não venda perdida."
12. `[orient]` T6 `failure_today` — O que corre mal hoje, e quanto custa quando corre mal?
   → **Ficheiro corrompido, só eu reponho**: "O ficheiro já foi corrompido várias vezes e só eu o sei repor. Quando isso acontece, faço-o nas minhas férias, e o preço do dia atrasa."
13. `[orient]` T7 `change_requested` — O que é que o pedido quer mudar nisto?
   → **Tirar do ficheiro único**: "Queremos tirar isto de um ficheiro que só uma pessoa sabe reparar, sem perder a forma como o preço se calcula."
14. `[orient]` **autoridades** — Para além de ti, quem tem autoridade para confirmar factos sobre este processo?
   → **Ninguém, só eu**: "Ninguém — só eu. O Supply, o IT e os comerciais são fontes, não autoridades."
15. `[orient]` **funding gate** — A decisão de avançar depende de aprovação orçamental de terceiros?
   → **Não**
16. `[start]` — **nenhuma pergunta emitida**. Recebeu tudo de `aisa-orient` e não repetiu (passo 4: «do not ask again»).

As cinco perguntas de pricing foram emitidas logo a seguir à activação e **antes** de T5, porque a resposta foi *Sim*.

## DIVERGENCES

A resposta viva divergiu da baseline em 1 ponto(s). Vale a resposta viva; a baseline fica para se ver a diferença.

| tema | baseline (antes) | resposta viva (o que vale) |
|---|---|---|
| T1 `actors` | Sou eu que faço o preço todos os dias e sou eu que mando no processo. O Supply dá-me a cedência, o comité aprova as margens, e os comerciais consomem o preço. | O comité de pricing é quem manda; eu só executo o cálculo diário. |

## ENQUADRAMENTO

Escrito em `_runs/pricing-marinha-cenario/enquadramento.md` a partir das respostas acima, lido do disco:

```markdown
## T1 · actors
O comité de pricing é quem manda; eu só executo o cálculo diário.

## T2 · trigger
Começa todos os dias de manhã, quando chegam as cotações do dia.

## T3 · activities
Recolher as cotações, lançar a cedência do Supply, calcular o preço por produto e por unidade, levar as margens ao comité quando mudam, e publicar o preço do dia. A decisão de margem é do comité.

## T4 · outcomes
Sai o preço diário por produto, para os comerciais e para o carregamento. Corre bem quando o preço sai antes da hora de carregamento e a margem apurada bate com a valorizada.

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
```

A secção `## pricing` existe e abre com `<!-- INTAKE-SET: pricing -->`, com `### P1`..`### P5` verbatim.

## EVIDENCE-LEVEL

`interactive`

As 15 perguntas foram **emitidas** por `AskUserQuestion` e as 15 respostas foram escolhidas
ao vivo pelo dono. A passagem entre skills está registada: tudo foi recolhido em
`aisa-orient` passo 3 e `aisa-start` não repetiu nenhuma pergunta, como o seu passo 4 manda.

Limite honesto do que isto prova: é **uma** corrida, nesta sessão, com este modelo. Não
demonstra que qualquer sessão futura emita exactamente estas perguntas — demonstra que esta
emitiu, e deixa o registo para se poder comparar.

## CHECKS

CHECK-1: PASS — a pergunta de activação foi emitida exactamente uma vez, e em nenhum outro ponto do percurso. É a excepção explícita à regra do CHECK-2.
CHECK-2: PASS — resposta *Sim*: as cinco perguntas foram emitidas (`ASKED` #6–#10) e o `enquadramento.md` tem `## pricing` com `<!-- INTAKE-SET: pricing -->`.
CHECK-3: PASS — `aisa-start` não emitiu pergunta nenhuma (último item de `ASKED`): recebeu tudo de `aisa-orient`; nenhum texto de pergunta aparece duas vezes na lista.
CHECK-4: PASS — os 5 `M-n` são as 5 frases de T5, verbatim, nem mais nem menos; as frases reusam verbatim as declarações registadas em `projects/pricing-marinha-pilot-3/enquadramento.md` (M-1..M-5).
