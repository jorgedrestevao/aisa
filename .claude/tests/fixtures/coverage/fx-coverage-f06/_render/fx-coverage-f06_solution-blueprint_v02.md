# Architecture Blueprint — fx-coverage-f06

> Versão de arquitectura lida: `_blueprint/ux-blueprint_v03.yaml` (latest authorized).
> Estado de aprovação: não aprovada — aguarda aprovação do negócio.

## A1 — Autorização e âmbito

Âmbito autorizado: registo, resumo, libertação e as saídas de resumo. O carregamento no
sistema de lotes fica do lado de lá da fronteira.

## A3 — Contexto e fronteiras

| componente | fronteira | forçado por |
|---|---|---|
| `resumo-email` | in-platform | C-006 |
| `resumo-aditivos-publicacao` | outside-platform | C-007 — o ficheiro é gravado diariamente na área partilhada e fica disponível para consulta |
| `lote-export` | outside-platform | C-008 |
| `imposicao-segregacao-no-armazenamento` | outside-platform | C-010 |

## A5 — Autoridade de dados e stores

O domínio `lotes` é próprio da solução e regista quem registou e quem libertou cada lote. O
domínio `publicacoes` regista cada publicação diária por saída e canal, incluindo o local de
publicação e o instante. O domínio `parametros` é próprio da solução.

## A7 — Identidade e ponto de imposição da autorização

A regra de que quem regista não liberta é imposta ao nível do armazenamento, e não apenas no
ecrã: um acesso directo fica sujeito à mesma regra (C-010). O ecrã de libertação mostra as
duas identidades lado a lado (C-002, C-005).

## A12 — Obrigações de prova

Paridade de cálculo sobre um mês de referência (V2). Recusa de libertação pelo próprio
registador, pela aplicação e por acesso directo (V2). Publicação diária observada em ambiente
de teste durante uma semana (V2).
