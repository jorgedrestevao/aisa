---
template_id: executive-report
output_format: md
audience: sponsor
required_slots:
  - solution_name
  - business_case
  - chosen_solution_summary
  - timeline_overview
  - investment_summary
  - risks_and_mitigations
optional_slots:
  - decision_context
  - decision_options
  - alternatives_summary
  - open_assumptions_list
slot_sources:
  business_case: _synthesis/business-story.md# What success looks like to the sponsor, The impact in business terms
  chosen_solution_summary: _synthesis/architecture-story.md# Chosen architecture, Platform and components
  timeline_overview: _synthesis/financial-story.md# Build effort and indicative cost
  investment_summary: _synthesis/financial-story.md# Budget envelope and funding, Build effort and indicative cost, Payback / ROI
  risks_and_mitigations: _synthesis/risks-and-assumptions.md# Accepted risks (with mitigations), Watch-list summary
  decision_context: decisions.md# D-NNN — Justification
  decision_options: options.md
  alternatives_summary: decisions.md# D-NNN — Alternatives considered
  open_assumptions_list: _synthesis/risks-and-assumptions.md# Assumptions to validate during build, Unresolved Unknowns (Critical)
---

# Relatório Executivo — {{solution_name}}

> Documento síntese destinado ao sponsor / C-level. Foco em business case, decisão tomada, investimento, e riscos. Lê em ~10 minutos.

## 1. Business Case
{{business_case}}

## 2. Solução escolhida
{{chosen_solution_summary}}

## 3. Calendário de alto nível
{{timeline_overview}}

## 4. Investimento previsto
{{investment_summary}}

## 5. Contexto da decisão
{{decision_context}}

## 6. Opções avaliadas
{{decision_options}}

## 7. Alternativas resumo
{{alternatives_summary}}

## 8. Riscos e mitigações
{{risks_and_mitigations}}

## 9. Pontos pendentes de validação
{{open_assumptions_list}}
