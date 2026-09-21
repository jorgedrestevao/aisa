# Cenário de intake — manutenção preventiva

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
> Engagement de teste isolado: `docs/runtime-hardening/intake-scenarios/_runs/manutencao-preventiva/`.
> Nenhum engagement real foi tocado.

## INPUT

```
As paragens de máquina estão a matar-nos. O plano de manutenção está numa folha que o chefe de turno atualiza à mão, e quando uma máquina avaria ninguém sabe se a preventiva estava em dia. Precisamos de ver isto melhor.
```

## OWNER-SCRIPT

Baseline fixada **antes** da corrida, para se poder ver o que divergiu.

- **activation (`A saída deste processo é um preço, cotação, margem ou valorização?`)**: **Não**
- **T1 actors**: "O chefe de turno é quem manda no plano. Os técnicos de manutenção executam, e o responsável de produção é quem autoriza parar uma máquina."
- **T2 trigger**: "Há duas entradas: o calendário da preventiva, que é por horas de funcionamento, e a avaria, que entra a qualquer hora."
- **T3 activities**: "Ver o que está previsto para o turno, confirmar peças em armazém, pedir a janela de paragem à produção, executar, e registar o que foi feito. A decisão de parar ou adiar é do responsável de produção."
- **T4 outcomes**: "No fim sai uma ordem fechada com o que se fez e as horas gastas. Corre bem quando a preventiva é feita dentro da janela prevista e a máquina não volta a parar pelo mesmo motivo."
- **T5 invariants**: "Uma máquina não pára sem autorização da produção. Nenhuma intervenção fica sem registo de quem a fez. A preventiva conta-se por horas de funcionamento, não por data de calendário."
- **T6 failure_today**: "Perdemos horas de produção que não estavam previstas. No ano passado foram cerca de quarenta horas de paragem não planeada, e a cada uma delas ninguém consegue dizer se a preventiva estava em dia."
- **T7 change_requested**: "Queremos trocar a folha por um sistema, seja ele qual for."
- **autoridades**: "Ninguém — só eu."
- **funding gate**: Não

## ASKED

As 10 perguntas emitidas, por ordem, com a resposta escolhida. `[orient]` = `aisa-orient`
passo 3 · `[start]` = `aisa-start` passo 4.

1. `[orient]` T1 `actors` — Quem faz parte disto, que papéis intervêm, e quem manda no processo?
   → **Chefe de turno manda no plano**: "O chefe de turno é quem manda no plano. Os técnicos de manutenção executam, e o responsável de produção é quem autoriza parar uma máquina."
2. `[orient]` T2 `trigger` — O que faz este processo começar, e com que frequência?
   → **Calendário e avaria**: "Há duas entradas: o calendário da preventiva, que é por horas de funcionamento, e a avaria, que entra a qualquer hora."
3. `[orient]` T3 `activities` — O que se faz, por ordem, e onde é que se decide alguma coisa?
   → **Ver turno, peças, janela, executar**: "Ver o que está previsto para o turno, confirmar peças em armazém, pedir a janela de paragem à produção, executar, e registar o que foi feito. A decisão de parar ou adiar é do responsável de produção."
4. `[orient]` T4 `outcomes` — O que sai no fim, para quem, e como se sabe que correu bem?
   → **Ordem fechada com horas**: "No fim sai uma ordem fechada com o que se fez e as horas gastas. Corre bem quando a preventiva é feita dentro da janela prevista e a máquina não volta a parar pelo mesmo motivo."
5. `[orient]` **activation** — A saída deste processo é um preço, cotação, margem ou valorização?
   → **Não**
6. `[orient]` T5 `invariants` — O que tem de se manter sempre verdadeiro, as regras que ninguém pode quebrar?
   → **Autorização, registo, horas**: "Uma máquina não pára sem autorização da produção. Nenhuma intervenção fica sem registo de quem a fez. A preventiva conta-se por horas de funcionamento, não por data de calendário."
7. `[orient]` T6 `failure_today` — O que corre mal hoje, e quanto custa quando corre mal?
   → **Quarenta horas de paragem**: "Perdemos horas de produção que não estavam previstas. No ano passado foram cerca de quarenta horas de paragem não planeada, e a cada uma delas ninguém consegue dizer se a preventiva estava em dia."
8. `[orient]` T7 `change_requested` — O que é que o pedido quer mudar nisto?
   → **Substituir a folha por sistema**: "Queremos trocar a folha por um sistema, seja ele qual for."
9. `[orient]` **autoridades** — Para além de ti, quem tem autoridade para confirmar factos sobre este processo?
   → **Ninguém, só eu**: "Ninguém — só eu."
10. `[orient]` **funding gate** — A decisão de avançar depende de aprovação orçamental de terceiros?
   → **Não**
11. `[start]` — **nenhuma pergunta emitida**. Recebeu tudo de `aisa-orient` e não repetiu (passo 4: «do not ask again»).

Nenhuma das cinco perguntas de pricing foi emitida — a resposta à activação foi *Não*.

## DIVERGENCES

A resposta viva divergiu da baseline em 3 ponto(s). Vale a resposta viva; a baseline fica para se ver a diferença.

| tema | baseline (antes) | resposta viva (o que vale) |
|---|---|---|
| T7 `change_requested` | Queremos saber, a qualquer momento, o que está em atraso e porquê, sem ter de perguntar ao chefe de turno. | Queremos trocar a folha por um sistema, seja ele qual for. |
| autoridades | O responsável de produção, para tudo o que seja paragem. | Ninguém — só eu. |
| funding gate | Sim | Não |

## ENQUADRAMENTO

Escrito em `_runs/manutencao-preventiva/enquadramento.md` a partir das respostas acima, lido do disco:

```markdown
## T1 · actors
O chefe de turno é quem manda no plano. Os técnicos de manutenção executam, e o responsável de produção é quem autoriza parar uma máquina.

## T2 · trigger
Há duas entradas: o calendário da preventiva, que é por horas de funcionamento, e a avaria, que entra a qualquer hora.

## T3 · activities
Ver o que está previsto para o turno, confirmar peças em armazém, pedir a janela de paragem à produção, executar, e registar o que foi feito. A decisão de parar ou adiar é do responsável de produção.

## T4 · outcomes
No fim sai uma ordem fechada com o que se fez e as horas gastas. Corre bem quando a preventiva é feita dentro da janela prevista e a máquina não volta a parar pelo mesmo motivo.

## T5 · invariants
Uma máquina não pára sem autorização da produção. Nenhuma intervenção fica sem registo de quem a fez. A preventiva conta-se por horas de funcionamento, não por data de calendário.

## T6 · failure_today
Perdemos horas de produção que não estavam previstas. No ano passado foram cerca de quarenta horas de paragem não planeada, e a cada uma delas ninguém consegue dizer se a preventiva estava em dia.

## T7 · change_requested
Queremos trocar a folha por um sistema, seja ele qual for.

## Invariantes
Lidos de **T5**, verbatim, uma linha por frase declarada.

| id | invariante | o que orienta | fonte |
|---|---|---|---|
| M-1 | Uma máquina não pára sem autorização da produção. | quem autoriza, e o momento em que autoriza | declaração do dono, 2026-09-11 |
| M-2 | Nenhuma intervenção fica sem registo de quem a fez. | o trilho de auditoria que a solução tem de garantir | declaração do dono, 2026-09-11 |
| M-3 | A preventiva conta-se por horas de funcionamento, não por data de calendário. | a unidade em que o plano se mede | declaração do dono, 2026-09-11 |
```

Não existe secção `## pricing` e não existe o marcador `INTAKE-SET` em parte nenhuma do ficheiro.

## EVIDENCE-LEVEL

`interactive`

As 10 perguntas foram **emitidas** por `AskUserQuestion` e as 10 respostas foram escolhidas
ao vivo pelo dono. A passagem entre skills está registada: tudo foi recolhido em
`aisa-orient` passo 3 e `aisa-start` não repetiu nenhuma pergunta, como o seu passo 4 manda.

Limite honesto do que isto prova: é **uma** corrida, nesta sessão, com este modelo. Não
demonstra que qualquer sessão futura emita exactamente estas perguntas — demonstra que esta
emitiu, e deixa o registo para se poder comparar.

## CHECKS

CHECK-1: PASS — a pergunta de activação foi emitida exactamente uma vez, e em nenhum outro ponto do percurso. É a excepção explícita à regra do CHECK-2.
CHECK-2: PASS — resposta *Não*: zero perguntas de pricing emitidas, e o `enquadramento.md` não tem `## pricing` nem `INTAKE-SET`.
CHECK-3: PASS — `aisa-start` não emitiu pergunta nenhuma (último item de `ASKED`): recebeu tudo de `aisa-orient`; nenhum texto de pergunta aparece duas vezes na lista.
CHECK-4: PASS — os 3 `M-n` são as 3 frases de T5, verbatim, nem mais nem menos.
