# Shared Understanding — fx-coverage-f06

> Engagement: fx-coverage-f06
> Sponsor: Responsavel de Qualidade (fixture)
> Iniciado: 2026-03-02
> Fase actual: Decision
> Última actualização: 2026-03-06T18:00:00+01:00
> Saúde epistémica: 100% (0 expiradas) — 2026-03-06

## Confirmed

| id | lens | claim | evidência | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| C-001 | enquadramento | O ficheiro de resumo que as equipas ja conhecem tem de se manter (M-1) | declaração do dono do processo, 2026-03-02 — enquadramento.md#M-1 | 2026-03-02 | organizacional | R-00 |
| C-002 | enquadramento | Nenhum lote e libertado por quem o registou (M-2) | declaração do dono do processo, 2026-03-02 — enquadramento.md#M-2 | 2026-03-02 | organizacional | R-00 |
| C-003 | operations | Passam 8 a 14 lotes por dia util; nao ha registo ao fim-de-semana (was U-001) | USER_ANSWER 2026-03-03 — answers.md#U-001 | 2026-03-03 | organizacional | R-01 |
| C-004 | data | O ficheiro tem quatro folhas: uma de entradas, duas de resumo e uma de parametros | `_capture/registo-de-lotes.xlsx.extraction.json#sheets` — 4 folhas | 2026-03-02 | organizacional | R-01 |
| C-005 | governance | A libertacao fica pendente quando o segundo tecnico falta — o dono nunca liberta o que registou (was U-002) | USER_ANSWER 2026-03-03 — answers.md#U-002 | 2026-03-03 | organizacional | R-01 |
| C-006 | operations | O "Resumo de Lotes" segue por email para as equipas de producao todos os dias uteis | declaração do dono do processo — enquadramento.md#T4 | 2026-03-02 | organizacional | R-01 |
| C-007 | data | A saída "Resumo Aditivos" funciona operacionalmente como a folha principal de resumo — não é distribuída por email por as consultas serem esporádicas; fica disponível para consulta porque o ficheiro é gravado diariamente na área partilhada da qualidade (was U-004) | USER_ANSWER 2026-03-03 — dono do processo, relatado pelo consultor — answers.md#U-004 | 2026-03-03 | organizacional | F-01 |
| C-008 | operations | O ficheiro de integracao para o sistema de lotes tem duas colunas (`lote`, `resultado`), formato Excel, cadencia diaria (was U-006) | USER_ANSWER 2026-03-04 — answers.md#U-006 | 2026-03-04 | organizacional | O-01 |
| C-009 | data | As colunas `Custo_Posto_A/B/C` sao rascunho de um estudo antigo e nao entram no resultado (was U-007) | USER_ANSWER 2026-03-04 — answers.md#U-007 | 2026-03-04 | organizacional | O-01 |
| C-010 | governance | A regra de que quem regista nao liberta e imposta ao nivel da base de dados, nao apenas no ecra — acesso directo ao armazenamento tem de ficar sujeito a mesma regra (was U-009) | USER_ANSWER 2026-03-08 — equipa de sistemas, confirmado pelo dono — answers.md#U-009 | 2026-03-08 | plataforma-tecnica | O-01 |
| D-002 | chair | Decisão: O-002 — aplicação com base de dados governada; ver decisions.md#D-002 | decisions.md#D-002 | 2026-03-06 | organizacional | D-01 |

## Assumed

| id | lens | claim | base da assumption | verificado_em | validade | ronda |
|---|---|---|---|---|---|---|
| A-001 | data | O volume anual mantem-se na ordem dos 3 000 registos | extrapolação de C-003 sobre dias uteis; nao confirmado pelo dono | 2026-03-03 | organizacional | R-01 |
| A-002 | governance | A identidade de quem liberta fica registada pelo sistema de autenticação existente | prática relatada pela equipa de sistemas, sem configuração observada | 2026-03-04 | plataforma-tecnica | O-01 |
| A-003 | data | A hipótese de que o "Resumo Aditivos" alimenta um consumidor externo fica sem confirmação nem negação directa (was U-004) | a resposta do dono (C-007) descreve consulta interna e não nomeia consumidor externo; ausência de menção não é confirmação de ausência — answers.md#U-004 | 2026-03-03 | organizacional | F-01 |

## Unknown

| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
|---|---|---|---|---|---|---|---|
| U-009 | governance | Onde é imposta a regra de que quem regista não liberta — na base de dados ou apenas na aplicação? (M-2) | role: equipa de sistemas \| fonte: configuração do ambiente | Critical | reuniao | decisivo: na base de dados → o desenho precisa de um ponto de imposição fora da aplicação e muda componentes; só na aplicação → a imposição vive no percurso de ecrãs e o risco de contorno fica aceite — muda o padrão arquitetural e o risco técnico | O-01 — resolved → C-010 |
| U-010 | operations | Qual o indicador observável que decide se o resumo pode sair antes de todas as análises chegarem? (M-1) | role: dono do processo | Med | reuniao | dimensionante: existe indicador → a solução calcula-o e o ecrã mostra-o; não existe → fica sempre decisão manual — muda o modelo de dados e o esforço de alto nível | O-01 |

## Conflicted

| id | lens | conflito | partes | criticidade | ronda |
|---|---|---|---|---|---|

## Risky

| id | lens | risco | impacto | mitigação proposta | ronda |
|---|---|---|---|---|---|
| R-001 | operations | A reconstrução do ficheiro depende de uma só pessoa | resumo atrasado enquanto essa pessoa estiver ausente | procedimento escrito + segunda pessoa treinada | R-01 |
| R-002 | data | A lógica de cálculo do resumo não está documentada fora do ficheiro | a solução nova pode divergir sem que ninguém detecte | prova de paridade sobre um período de referência | O-01 |
