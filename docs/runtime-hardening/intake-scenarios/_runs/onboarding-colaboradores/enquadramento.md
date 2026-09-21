# Enquadramento — onboarding-colaboradores

> Dono do processo: Responsável de equipa (dono do processo de entrada)
> Data da declaração: 2026-09-11
> Executor que registou: corrida interactiva da camada 2 de B4 (perguntas emitidas por `AskUserQuestion`)
> Pedido literal (`context.json.literal_request`): "Temos um problema com a entrada de gente nova. Quando entra alguém, o responsável manda um email ao IT a pedir acessos, outro ao facilities para a secretária e o cartão, e depois anda atrás de toda a gente durante duas semanas. Já aconteceu alguém chegar no primeiro dia e não ter computador. Queríamos organizar isto."

## T1 · actors

O responsável da equipa que recebe a pessoa é quem manda no processo. Entram o IT para os acessos, o facilities para o espaço e o cartão, e os recursos humanos para o contrato.

## T2 · trigger

Começa quando o contrato é assinado, e normalmente é uma ou duas pessoas por mês, com picos em Setembro.

## T3 · activities

Pedir os acessos, pedir o posto e o cartão, preparar o contrato, marcar a formação de segurança, e no primeiro dia apresentar a equipa. Quem decide o que a pessoa pode aceder é o responsável da equipa.

## T4 · outcomes

No fim a pessoa está a trabalhar. Corre bem quando no primeiro dia tem computador, acessos e alguém à espera dela.

## activation · pricing

Pergunta emitida: *A saída deste processo é um preço, cotação, margem ou valorização?*  Resposta do dono: **Não**.

## T5 · invariants

Ninguém entra sem contrato assinado. Ninguém tem acesso a um sistema sem o responsável da equipa aprovar. A formação de segurança tem de estar feita nos primeiros cinco dias.

## T6 · failure_today

Perde-se a primeira semana da pessoa. Já aconteceu duas vezes este ano alguém chegar sem computador, e isso custa-nos uma semana de trabalho mais a impressão que fica.

## T7 · change_requested

Queremos que os pedidos saiam sozinhos quando o contrato é assinado, e ver num sítio só o que falta para cada pessoa.

## Invariantes

Lidos de **T5**, verbatim, uma linha por frase declarada.

| id | invariante | o que orienta | fonte |
|---|---|---|---|
| M-1 | Ninguém entra sem contrato assinado. | o gatilho do processo | declaração do dono, 2026-09-11 |
| M-2 | Ninguém tem acesso a um sistema sem o responsável da equipa aprovar. | o plano de imposição de permissões | declaração do dono, 2026-09-11 |
| M-3 | A formação de segurança tem de estar feita nos primeiros cinco dias. | o prazo que qualquer solução tem de respeitar | declaração do dono, 2026-09-11 |

## Autoridades nomeadas pelo dono

Pergunta emitida: *Para além de ti, quem tem autoridade para confirmar factos sobre este processo?*

Resposta: **"O responsável de recursos humanos também pode confirmar."**

## Regras

- O enquadramento é a **hipótese do dono**, não facto verificado: `/frame` confirma ou corrige cada `M-n` com evidência.
- Nenhum `M-n` foi inferido do pedido literal nem do `_capture`; só o que o dono disse.
- Sem vendor, sem produto, sem solução em `M-n`.
