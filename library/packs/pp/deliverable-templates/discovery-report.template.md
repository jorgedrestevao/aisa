---
template_id: discovery-report
# render --html: this deliverable gets the interrogable HTML projection first (provenance tooltips per id + final Proveniência table); others follow in v3.1
output_format: md
audience: client
required_slots:
  - solution_name
  - business_context
  - current_state_summary
  - identified_processes
  - pain_points
  - data_inventory
  - open_assumptions_list
optional_slots:
  - stakeholders_interviewed
  - sources_analysed
slot_sources:
  business_context: _synthesis/business-story.md# Why this engagement exists, Who actually feels the problem
  current_state_summary: _synthesis/as-is.md# End-to-end process today, Volume and cycle time
  identified_processes: _synthesis/as-is.md# End-to-end process today
  pain_points: _synthesis/as-is.md# Top friction points
  data_inventory: shared-understanding.md# lens=data (Confirmed + Assumed)
  open_assumptions_list: _synthesis/risks-and-assumptions.md# Assumptions to validate during build, Unresolved Unknowns (Critical)
  stakeholders_interviewed: context.json# requester
  sources_analysed: inputs/*
---

# Relatório de Descoberta — {{solution_name}}

> Documento de descoberta para o sponsor. Contexto de negócio, estado actual, processos, dados, pontos de fricção, e pontos pendentes de validação. Vendor- and product-neutral by construction.

## 1. Contexto de negócio
{{business_context}}

## 2. Estado actual — resumo
{{current_state_summary}}

## 3. Processos identificados
{{identified_processes}}

## 4. Inventário de dados
{{data_inventory}}

## 5. Pontos de fricção identificados
{{pain_points}}

## 6. Stakeholders entrevistados
{{stakeholders_interviewed}}

## 7. Fontes analisadas
{{sources_analysed}}

## 8. Pontos pendentes de validação
{{open_assumptions_list}}
