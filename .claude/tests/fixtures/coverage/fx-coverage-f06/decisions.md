# Decisions — fx-coverage-f06

## D-001 — Frame agreed (F-01)

- **Frame sentence**: O problema é a produção diária das duas saídas de resumo de lotes depender de uma só pessoa para operar e reconstruir uma folha de cálculo frágil, sentido por quem produz o resumo e pelas equipas que o consomem, custa hoje o atraso do resumo sempre que o ficheiro parte, e a evidência é a captura do ficheiro (`_capture/process-model.md` §3–4) e a declaração do dono do processo.
- **Agreed in round**: F-01
- **Frame sha256**: 98b77d8955444e2762e7bb3fb9707ad64cf65e55237f4b244ac33c70c40413fc
- **Supersedes**: —
- **Anchors**: ver `frame.md` § Anchors
- **Override used at /frame**: —
- **Validated by**: owner (Responsavel de Qualidade — fixture, via AskUserQuestion)
- **Timestamp**: 2026-03-05T10:00:00+01:00

## D-002 — Adopt O-002 — aplicação com base de dados governada

- **The aisa recommended**: O-002 — a única que remove a dependência de operador único dentro da fronteira declarada.
- **Chosen option**: O-002 — aplicação com base de dados governada
- **Recommendation followed?**: yes
- **Rule change decided**: —
- **Selected solution / composition**: aplicação com superfície de registo sobre uma base de dados governada, substituindo a folha de cálculo como sistema de registo.
- **(Scope, outcome) pairs — UNCOLLAPSED**:
  - registo, resumo, libertação e as duas saídas de resumo — viável com pré-condições
  - carregamento no sistema de lotes a jusante — fora da fronteira de construção, o ficheiro é entregue e a outra equipa carrega-o
- **Conditions**:
  - o ponto de imposição da segregação (U-009) fica decidido antes do build
- **Proof obligations**:
  - paridade de cálculo entre o sistema novo e a folha, sobre um período de referência — nível V2, dono: developer, financiado: não
- **Preconditions**: nenhuma
- **Justification**: O-002 é a única forma dentro da fronteira declarada que remove a dependência de operador único (R-001, C-003) e conserva as três saídas (C-006, C-007, C-008).
- **Alternatives considered**:
  - O-001 — mantém a dependência
  - O-003 — fora da fronteira declarada pelo dono
- **Accepted assumptions**: A-002 (identidade registada pelo sistema de autenticação existente, sem configuração observada)
- **Accepted risks**: R-002 (lógica de cálculo não documentada fora do ficheiro) — mitigado pela obrigação de prova acima
- **Revision conditions / Tripwires (estruturados)**:
  - **TW-1** — se U-009 obrigar a um componente de imposição fora da aplicação, reavaliar esforço e componentes
  - **TW-2** — se aparecer um consumidor externo do "Resumo Aditivos" (A-003), reavaliar o canal de entrega
- **Sponsor confirmation**: yes
- **Supersedes**: —
- **Decided in round**: D-01
- **Timestamp**: 2026-03-06T17:00:00+01:00
