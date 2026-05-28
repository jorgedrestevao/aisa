---
template_id: implementation-spec
output_format: md
audience: developer
required_slots:
  - solution_name
  - chosen_architecture
  - entities_to_create
  - screens_to_build
  - flows_to_implement
  - security_roles
  - integrations
  - test_scenarios
  - sequencing
optional_slots:
  - open_assumptions_list
  - migration_notes
slot_sources:
  chosen_architecture: decisions.md# D-NNN — Branch (if technology)
  entities_to_create: _synthesis/architecture-story.md# Data
  screens_to_build: _synthesis/architecture-story.md# Platform and components
  flows_to_implement: _synthesis/architecture-story.md# Platform and components, Integrations
  security_roles: _synthesis/architecture-story.md# Security model
  integrations: _synthesis/architecture-story.md# Integrations
  test_scenarios: _synthesis/as-is.md# Top friction points, Exceptions, handoffs, and tribal knowledge
  sequencing: _synthesis/financial-story.md# Build effort and indicative cost
  open_assumptions_list: _synthesis/risks-and-assumptions.md# Assumptions to validate during build
  migration_notes: shared-understanding.md# lens=data (Risky rows about historical data / migration)
---

# Implementation Spec — {{solution_name}}

> Actionable build specification. Audience: implementation team (PP / OS / Mendix / custom — pack-specific). Each section maps to a concrete deliverable the dev team owns; if a section is thin, the engagement is not ready to build and must loop back to the decision or synthesis layer.

## 1. Arquitectura escolhida
{{chosen_architecture}}

## 2. Entidades a criar
> One row per entity: name, owner, fields (name · type · required · default), relationships, indexes (where applicable).

{{entities_to_create}}

## 3. Ecrãs / componentes a construir
> One block per screen/component: name, type (List / Form / Detail / Dashboard / Admin), data sources, key controls, behaviour notes.

{{screens_to_build}}

## 4. Fluxos a implementar
> One block per flow: trigger, source/destination, steps, error handling, idempotency, schedule (if any).

{{flows_to_implement}}

## 5. Modelo de segurança e roles
> Roles + permissions matrix (screen × entity × CRUD). Sign-off rules (separation of duties).

{{security_roles}}

## 6. Integrações
> Per integration: system, direction (in/out/two-way), connector/API, authentication, frequency, DLP classification.

{{integrations}}

## 7. Cenários de teste
> Scenario per friction point + exception identified in as-is. Each: pre-condition, steps, expected outcome, acceptance criterion.

{{test_scenarios}}

## 8. Sequenciamento (sprints / waves)
> Recommended build sequence with dependencies. Identifies what must land first.

{{sequencing}}

## 9. Notas de migração de dados
{{migration_notes}}

## 10. Pontos pendentes de validação
{{open_assumptions_list}}
