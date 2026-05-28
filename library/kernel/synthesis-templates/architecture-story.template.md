---
template_id: architecture-story
output_path: _synthesis/architecture-story.md
sources:
  - decisions.md# chosen option + branch
  - shared-understanding.md# lens IN (technology, data)
  - lens-outputs/technology.md
  - lens-outputs/data.md
  - library/packs/<pack>/architecture-templates/<branch>.md
  - library/packs/<pack>/decision-tree.md
synthesis_prompt: |
  Narrate the architecture of the chosen option. State the branch from
  the pack's decision-tree.md, the platform, the data entities and where
  each lives, the integrations, the security model, and the constraints
  on the watch-list. Vendor and product names ARE allowed here (this is
  the only synthesis topic where that is true). Anchor to the chosen
  decision (D-NNN), the pack's architecture template, and SU ids for
  technology + data.
---

# Architecture Story — {{slug}}

## Chosen architecture
<one paragraph: the option chosen (O-NNN), the branch from decision-tree.md, why it won over alternatives. Cite D-NNN and the relevant SU ids.>

## Platform and components
<paragraph or bulleted list naming the platform and the major components — e.g., Canvas App + Dataverse tables + Power Automate flows, or SharePoint Online + Canvas App + Power Automate. Anchor to the pack's architecture template.>

## Data
<paragraph: entities, where each lives, sensitivity, ownership, retention. Cite SU ids from the data lens and lens-outputs/data.md.>

## Integrations
<paragraph or list: external systems to read from / write to, the connectors/APIs involved, the DLP policy classification.>

## Security model
<paragraph: roles, separation of duties, audit trail, sign-off ladder. Anchor to the security-patterns domain-knowledge file in the pack.>

## Watch-list constraints
<bulleted list: the pack's `lenses_config.technology.constraints_to_check` items, with the per-constraint state (pass / risky / blocker) and the trigger that would force a re-think. Cite the corresponding revision conditions from D-NNN.>
