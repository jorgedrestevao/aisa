# Enquadramento — manutencao-preventiva

> Dono do processo: Responsável de manutenção (dono do processo)
> Data da declaração: 2026-09-11
> Executor que registou: corrida interactiva da camada 2 de B4 (perguntas emitidas por `AskUserQuestion`)
> Pedido literal (`context.json.literal_request`): "As paragens de máquina estão a matar-nos. O plano de manutenção está numa folha que o chefe de turno atualiza à mão, e quando uma máquina avaria ninguém sabe se a preventiva estava em dia. Precisamos de ver isto melhor."

## T1 · actors

O chefe de turno é quem manda no plano. Os técnicos de manutenção executam, e o responsável de produção é quem autoriza parar uma máquina.

## T2 · trigger

Há duas entradas: o calendário da preventiva, que é por horas de funcionamento, e a avaria, que entra a qualquer hora.

## T3 · activities

Ver o que está previsto para o turno, confirmar peças em armazém, pedir a janela de paragem à produção, executar, e registar o que foi feito. A decisão de parar ou adiar é do responsável de produção.

## T4 · outcomes

No fim sai uma ordem fechada com o que se fez e as horas gastas. Corre bem quando a preventiva é feita dentro da janela prevista e a máquina não volta a parar pelo mesmo motivo.

## activation · pricing

Pergunta emitida: *A saída deste processo é um preço, cotação, margem ou valorização?*  Resposta do dono: **Não**.

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

## Autoridades nomeadas pelo dono

Pergunta emitida: *Para além de ti, quem tem autoridade para confirmar factos sobre este processo?*

Resposta: **"Ninguém — só eu."**

## Regras

- O enquadramento é a **hipótese do dono**, não facto verificado: `/frame` confirma ou corrige cada `M-n` com evidência.
- Nenhum `M-n` foi inferido do pedido literal nem do `_capture`; só o que o dono disse.
- Sem vendor, sem produto, sem solução em `M-n`.
