# Architecture story — fx-coverage-f06

authority: _blueprint/ux-blueprint_v03.yaml# architecture @ sha256:8999007a996bd8c87a7b77756ee9e734b294fc22bf84390cbd00fadc8f0e922b

## Authorized scope and outcome basis

O âmbito autorizado é "registo, resumo, libertação e as saídas de resumo; ficheiro de
integração para o sistema de lotes (fora da fronteira de construção)", com o outcome
"viável com pré-condições" emitido em `decisions.md#D-002`.

## A arquitectura em prosa

A aplicação passa a ser o sistema de registo dos lotes. As duas saídas de resumo
continuam a existir, cada uma com o seu canal, e o ficheiro de integração é entregue
para a equipa a jusante carregar.

> Fixture: esta síntese existe para dar autoridade de leitura aos registos de cobertura
> da etapa `render`. Não é um artefacto de engagement real.
