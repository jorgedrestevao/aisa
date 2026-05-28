---
template_id: solution-blueprint
output_format: md
audience: technical
required_slots:
  - solution_name
  - chosen_architecture
  - executive_summary
  - entity_inventory
  - rbac_summary
  - integration_inventory
  - estimation_summary
optional_slots:
  - alternatives_considered
  - open_assumptions_list
sub_templates:
  - architecture-templates/{{chosen_architecture}}.md
slot_sources:
  executive_summary: _synthesis/architecture-story.md# Chosen architecture
  entity_inventory: _synthesis/architecture-story.md# Data
  rbac_summary: _synthesis/architecture-story.md# Security model
  integration_inventory: _synthesis/architecture-story.md# Integrations
  estimation_summary: _synthesis/financial-story.md# Build effort and indicative cost
  alternatives_considered: decisions.md# D-NNN — Alternatives considered
  open_assumptions_list: _synthesis/risks-and-assumptions.md
  chosen_architecture: decisions.md# D-NNN — Branch (if technology)
---

# Solution Blueprint — {{solution_name}}

> Technical blueprint of the chosen architecture. Audience: solution architect / lead developer / tech lead. Includes the architecture sub-template for the chosen branch.

## 1. Sumário Executivo
{{executive_summary}}

## 2. Arquitectura Escolhida
{{>> architecture-templates/{{chosen_architecture}}.md}}

## 3. Modelo de Dados
{{entity_inventory}}

## 4. Segurança e RBAC
{{rbac_summary}}

## 5. Integrações
{{integration_inventory}}

## 6. Estimativa
{{estimation_summary}}

## 7. Alternativas Avaliadas
{{alternatives_considered}}

## 8. Pontos pendentes de validação
{{open_assumptions_list}}
