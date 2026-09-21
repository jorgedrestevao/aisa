# Options — fx-coverage-f06 / Round O-02

| opção | tecnologia | veredicto | ordem de grandeza | reversibilidade | o que bloqueia |
|---|---|---|---|---|---|
| O-001 | manter a folha com procedimento escrito | viável, não resolve a dependência | 5–8d | alta | R-001 mantém-se |
| O-002 | aplicação com base de dados governada | viável com pré-condições | 30–40d | média | U-009 |
| O-003 | serviço externo de laboratório | inviável no âmbito | — | baixa | fora da fronteira declarada pelo dono |

## O-001 — manter a folha

Não remove a dependência de operador único; fica no conjunto como referência de custo.

## O-002 — aplicação com base de dados governada

Substitui o ficheiro como sistema de registo e mantém as duas saídas de resumo mais o
ficheiro de integração. Depende de U-009 para o ponto de imposição da segregação.

## O-003 — serviço externo

O dono excluiu levar os dados para fora. Fica registada com o veredicto, não apagada.

## Recomendação do aisa

O-002, porque é a única que remove a dependência de operador único dentro da fronteira
declarada. O que a separa de O-001 é a fonte única de verdade; o que a faria virar é
U-009 obrigar a um componente de imposição que o âmbito não financia.
