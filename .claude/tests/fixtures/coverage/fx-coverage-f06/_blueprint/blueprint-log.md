# Blueprint log — fx-coverage-f06

Um registo por versão. Append-only.

## v01 — 2026-03-06T18:30:00+01:00

**Trigger**: inicial, após D-002.

**SU ids consumidos**: C-001..C-009, A-001, A-002, U-009, U-010, D-002.

**Violações (cap e estruturais)**: nenhuma — a verificação estrutural do runtime passa
sobre esta versão. É esse o ponto da fixture: **estrutura válida e requisito perdido**.

**Escolhas estruturais em aberto**: U-009. Bloqueia aprovação, não produção.

**Não incluído nesta versão**: nada declarado. A ausência do percurso de publicação e
consulta do "Resumo Aditivos" (C-007) **não** está declarada — é exactamente a perda
silenciosa que a revisão de cobertura tem de apanhar.

## v02 — 2026-03-09T11:00:00+01:00

**Trigger**: correcção do requisito perdido em v01.

**SU ids consumidos, adicionais à v01**: C-007 (agora concretizado), A-003.

**Correcção**: acrescentados o componente de publicação diária do "Resumo Aditivos" na
área partilhada, o ecrã de consulta e os campos de entrega na entidade. A entidade
`ResumoAditivos` já existia na v01 com `su_refs: [C-007]` — existir não era entregar.

## v03 — 2026-03-09T16:00:00+01:00

**Trigger**: resposta a U-009 (`answers.md#U-009` → C-010).

**SU ids consumidos, adicionais à v02**: C-010.

**Correcção**: a regra de segregação passa a ter ponto de imposição desenhado no
armazenamento, com os dois identificadores no registo e obrigação de prova própria. A escolha
estrutural fecha com `closure_basis` — deixou de bloquear aprovação. **A aprovação do negócio
continua por dar**: é essa a separação que esta versão existe para mostrar.
