# Premortem — fx-coverage-f06

> Obituário escrito a 12 meses, antes de decidir. Todas as causas ancoradas em ids da SU.

## Causa 1 — a saída que ninguém viu (C-007, A-003)

A solução entrou em serviço com o resumo que segue por email e sem o resumo que ficava
disponível para consulta. Ninguém reclamou na primeira semana, porque as consultas são
esporádicas; reclamaram no fecho do trimestre.

**Mitigação → requisito:** o desenho tem de concretizar as duas saídas, cada uma com o
seu canal.

## Causa 2 — a segregação ficou nominal (C-002, C-005, U-009)

A regra existe no ecrã e não no armazenamento; um acesso directo contorna-a.

**Mitigação → condição de revisão:** TW-1.

## Causa 3 — o cálculo divergiu em silêncio (R-002)

Nunca se comparou o resultado novo com o antigo sobre um período de referência.

**Mitigação → obrigação de prova:** paridade de cálculo.
