---
template_id: estimate
output_format: md
audience: client
required_slots:
  - solution_name
  - chosen_architecture
  - components_table
  - effort_summary
  - timeline
  - cost_estimate
optional_slots:
  - assumptions
  - exclusions
sub_templates:
  - architecture-templates/{{chosen_architecture}}.md
slot_sources:
  chosen_architecture: decisions.md# D-NNN — Branch (if technology)
  components_table: _synthesis/architecture-story.md# Platform and components, Data, Integrations
  effort_summary: _synthesis/financial-story.md# Build effort and indicative cost
  timeline: _synthesis/financial-story.md# Build effort and indicative cost
  cost_estimate: _synthesis/financial-story.md# Build effort and indicative cost, Sensitivity and revision triggers
  assumptions: _synthesis/risks-and-assumptions.md# Assumptions to validate during build
  exclusions: decisions.md# D-NNN — Alternatives considered (the "why not" lines often state exclusions)
---

# Estimativa Detalhada — {{solution_name}}

> Estimativa de componentes, esforço, calendário e custo para a opção arquitectural escolhida. Audience: client (sponsor + financial controller).

## 1. Sumário Executivo
Estimativa de componentes para a opção arquitectural escolhida: **{{chosen_architecture}}**.

## 2. Componentes a entregar
{{components_table}}

## 3. Resumo de esforço
{{effort_summary}}

## 4. Calendário previsto
{{timeline}}

## 5. Estimativa de custo
{{cost_estimate}}

## 6. Pressupostos
{{assumptions}}

## 7. Exclusões
{{exclusions}}

## 8. Arquitectura escolhida
{{>> architecture-templates/{{chosen_architecture}}.md}}
