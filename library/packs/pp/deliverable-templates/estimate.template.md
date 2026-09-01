---
template_id: estimate
output_format: md
audience: client
required_slots:
  - solution_name
  - estimate_headline
  - phases_table
  - timeline
  - detailed_phases
  - effort_summary
  - team_effort
  - risks_table
  - assumptions
optional_slots:
  - operational_impact
  - recommendations
slot_sources:
  estimate_headline: _synthesis/financial-story.md# Estimate headline
  phases_table: _synthesis/financial-story.md# Phased build plan
  detailed_phases: _synthesis/financial-story.md# Detailed estimate by phase
  timeline: _synthesis/financial-story.md# Timeline
  effort_summary: _synthesis/financial-story.md# Effort summary by phase
  team_effort: _synthesis/financial-story.md# Team and effort by profile
  operational_impact: _synthesis/financial-story.md# Operational impact
  recommendations: _synthesis/financial-story.md# Recommendations
  risks_table: _synthesis/risks-and-assumptions.md# Accepted risks (with mitigations)
  assumptions: _synthesis/risks-and-assumptions.md# Assumptions to validate during build
---

# Estimativa de Implementação — {{solution_name}}

> Estimativa de fases, esforço, calendário, equipa e custo para a opção arquitectural escolhida. Audience: client (sponsor + financial controller).

## 1. Resumo
{{estimate_headline}}

## 2. Fases do Projeto
{{phases_table}}

## 3. Timeline
{{timeline}}

## 4. Estimativa Detalhada por Fase
{{detailed_phases}}

## 5. Resumo da Estimativa
{{effort_summary}}

## 6. Equipa e Esforço por Perfil
{{team_effort}}

## 7. Análise de Riscos
{{risks_table}}

## 8. Impacto Operacional Esperado
{{operational_impact}}

## 9. Premissas
{{assumptions}}

## 10. Recomendações
{{recommendations}}
