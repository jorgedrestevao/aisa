---
template_id: architecture-hybrid
category: architecture
required_slots:
  - solution_name
  - dataverse_critical_entities
  - sharepoint_secondary_entities
  - canvas_app_pages
  - data_flow_diagram
optional_slots:
  - integrations_external
  - data_residency_notes
applies_to_branch: [hybrid]
output_format: md
---

## Arquitectura — Híbrida

**Plataforma:** Dataverse (entidades críticas) + SharePoint Online (entidades secundárias / anexos) + Canvas App
**Solução:** {{solution_name}}

### Entidades críticas em Dataverse
{{dataverse_critical_entities}}

### Entidades secundárias em SharePoint
{{sharepoint_secondary_entities}}

### Páginas da Canvas App
{{canvas_app_pages}}

### Fluxo de dados entre os dois sistemas
{{data_flow_diagram}}

### Integrações externas
{{integrations_external}}

### Notas de residência de dados
{{data_residency_notes}}
