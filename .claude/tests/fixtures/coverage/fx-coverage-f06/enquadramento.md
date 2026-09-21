# Enquadramento — fx-coverage-f06

> Fixture sintetica. A declaracao abaixo e do "dono do processo" inventado para esta
> fixture; nao descreve nenhuma organizacao real.

## T1 · actors

O responsavel de qualidade regista as entradas e produz o resumo. Um segundo tecnico
liberta o lote. As equipas de producao consomem o resumo.

## T2 · trigger

Todos os dias uteis, assim que as analises do turno da noite ficam disponiveis.

## T3 · activities

Registar as entradas do turno, recalcular o resumo, verificar os desvios, libertar o
lote e gravar o ficheiro.

## T4 · outcomes

Saem duas folhas de resumo: o "Resumo de Lotes", que segue por email para producao, e o
"Resumo Aditivos", que nao segue por email. Sabe-se que correu bem quando as duas saem
antes das 09:00 e ninguem pede correccoes.

## T5 · invariants

O ficheiro de resumo que as equipas ja conhecem tem de se manter. Nenhum lote e
libertado por quem o registou.

## T6 · failure_today

Quando o ficheiro parte, so uma pessoa o sabe reconstruir, e o resumo atrasa-se.

## T7 · change_requested

Sair da folha de calculo sem perder nenhuma das saidas nem a segunda verificacao.

## Invariantes (M-n)

| id | invariante (verbatim) | o que obriga | base |
|---|---|---|---|
| M-1 | O ficheiro de resumo que as equipas ja conhecem tem de se manter | qualquer proposta preserva o formato familiar das saidas de resumo | declaracao do dono, T5 |
| M-2 | Nenhum lote e libertado por quem o registou | o desenho mantem duas identidades distintas no percurso de libertacao | declaracao do dono, T5 |

## Regras

Quem pode confirmar factos sobre este processo: o dono do processo (todos os temas) e a
equipa de sistemas (apenas os temas tecnicos). Portao de financiamento: nao.
