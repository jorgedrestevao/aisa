# Answers — fx-coverage-f06

## U-001 — 2026-03-03
- **Pergunta/conflito**: Quantos lotes por dia passam pelo registo?
- **Resposta**: "Entre 8 e 14 em dia normal. Nos fins de semana nao ha registo."
- **Fonte**: USER_ANSWER 2026-03-03 — dono do processo
- **Transição**: U-001 → C-003 (Confirmed)

## U-002 — 2026-03-03
- **Pergunta/conflito**: Quem liberta o lote quando o segundo tecnico falta?
- **Resposta**: "Fica pendente. Nunca liberto eu, mesmo que atrase."
- **Fonte**: USER_ANSWER 2026-03-03 — dono do processo
- **Transição**: U-002 → C-005 (Confirmed)

## U-004 — 2026-03-03
- **Pergunta/conflito**: A folha "Resumo Aditivos" nao segue por email; nao esta confirmado
  quem a consome a jusante nem se a solucao futura tem de continuar a produzi-la.
  `TO-BE DIVERGENCE`: o alvo tem de decidir se mantem esta saida e por que canal a entrega.
- **Resposta**: "O Resumo Aditivos funciona como a outra folha. Como as consultas sao
  esporadicas nao o envio por email. Mas podem consultar o ficheiro porque diariamente e
  gravado na area partilhada da qualidade."
- **Fonte**: USER_ANSWER 2026-03-03 — dono do processo, relatado pelo consultor
- **Transição**: U-004 → C-007 (Confirmed, mecanismo de distribuicao interna) + A-003
  (Assumed — a hipotese de um consumidor externo fica sem confirmacao nem negacao directa;
  ausencia de mencao nao e confirmacao de ausencia)

## U-006 — 2026-03-04
- **Pergunta/conflito**: Que colunas leva o ficheiro de integracao para o sistema de lotes?
- **Resposta**: "lote e resultado; excel; diario."
- **Fonte**: USER_ANSWER 2026-03-04 — dono do processo
- **Transição**: U-006 → C-008 (Confirmed). NAO revoga C-007 nem C-001: sao saidas distintas.

## U-007 — 2026-03-04
- **Pergunta/conflito**: As colunas `Custo_Posto_A/B/C` da folha Entradas sao usadas no resumo?
- **Resposta**: "Sao rascunho de um estudo antigo. Nao entram no resultado."
- **Fonte**: USER_ANSWER 2026-03-04 — dono do processo
- **Transição**: U-007 → C-009 (Confirmed)

## U-009 — 2026-03-08
- **Pergunta/conflito**: Onde e imposta a regra de que quem regista nao liberta?
- **Resposta**: "Tem de ficar na base de dados. Se ficar so no ecra, quem tiver acesso
  directo contorna-a, e foi isso que a auditoria apontou."
- **Fonte**: USER_ANSWER 2026-03-08 — equipa de sistemas, confirmado pelo dono do processo
- **Transicao**: U-009 → C-010 (Confirmed)
