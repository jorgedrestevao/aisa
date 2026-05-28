---
template_id: claude-design-brief
output_format: md
audience: claude-design
required_slots:
  - solution_name
  - chosen_architecture
  - canvas_app_pages
  - page_navigation_map
  - persona_users
  - ux_requirements
optional_slots:
  - brand_guidance
  - accessibility_notes
sub_templates:
  - architecture-templates/{{chosen_architecture}}.md
slot_sources:
  chosen_architecture: decisions.md# D-NNN — Branch (if technology)
  canvas_app_pages: _synthesis/architecture-story.md# Platform and components
  page_navigation_map: _synthesis/as-is.md# End-to-end process today
  persona_users: _synthesis/as-is.md# Personas and their experience
  ux_requirements: _synthesis/as-is.md# Top friction points, Personas and their experience
  brand_guidance: context.json# brand_guidance (if captured)
  accessibility_notes: shared-understanding.md# lens=user (rows about accessibility/language)
---

# Claude Design Brief — {{solution_name}}

> Input para Claude Design (mockups high-fidelity da Canvas App). Especificação UI/UX detalhada que permite a geração de mockups directamente — Power FX validado, screens com paleta consistente, RBAC implementado.

## 1. Contexto e Arquitectura
{{>> architecture-templates/{{chosen_architecture}}.md}}

## 2. Personas / Tipos de utilizador
{{persona_users}}

## 3. Páginas da Canvas App
{{canvas_app_pages}}

## 4. Mapa de navegação entre páginas
{{page_navigation_map}}

## 5. Requisitos de UX
{{ux_requirements}}

## 6. Brand guidance
{{brand_guidance}}

## 7. Notas de acessibilidade
{{accessibility_notes}}

## 8. Domain knowledge cross-references

Os ficheiros abaixo (do pack `pp`) carregam o contexto técnico denso que Claude Design downstream precisa para produzir Power FX validado, ecrãs com paleta consistente, e RBAC implementado correctamente. Cada ficheiro é citável directamente — este brief pode embed snippets relevantes quando necessário.

| Ficheiro | Conteúdo crítico para Claude Design |
|---|---|
| `library/packs/pp/domain-knowledge/powerfx-patterns.md` | Delegation matrix (Dataverse vs SharePoint), traps (SUMPRODUCT, financial precision, WORKDAY, division-by-zero), Validation Sequence (5 syntax + 4 logic checks), Standard Patterns (Patch, Navigation, Gallery, Audit Log, Error Handling UX), Context Variable naming conventions (var/gbl/col/err) |
| `library/packs/pp/domain-knowledge/screen-patterns.md` | 5 Standard Screen Types (List/Form/Detail/Dashboard/Admin), Status Badge Colours Fluent 2 palette (hex codes), Information Density rules (HIGH/NORMAL/LOW), Approval Workflow state machine, Excel Familiar Anchors |
| `library/packs/pp/domain-knowledge/security-patterns.md` | RBAC symbols + 2-matrix template (screen × entity×CRUD), Role Inference signal sources, Power FX security blocks (App.OnStart com varCurrentUserRole + role detection fallback), Audit-on-Approve/Delete/Export patterns (mandatory PFx blocks) |
| `library/packs/pp/domain-knowledge/delegation-matrix.md` | Quick reference: which operations are delegable on Dataverse vs SharePoint, with workarounds for non-delegable patterns |

**Convenção de citação no brief renderizado**: quando a especificação precisar de emitir Power FX, screen colour, ou RBAC snippet específico, deve incluir a referência inline (e.g. "(consultar `domain-knowledge/powerfx-patterns.md § Audit Log`)") para que Claude Design saiba onde verificar a fonte autoritativa.
