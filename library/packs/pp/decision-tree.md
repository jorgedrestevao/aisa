---
dt_id: pp-branch-qualification
applies_to_phase: options
consulted_by: [lens-technology, solution-architect]
branches:
  - id: sharepoint-first
    display_name: "SharePoint-first"
    sub_template: architecture-templates/sharepoint-first.md
  - id: dataverse-first
    display_name: "Dataverse-first"
    sub_template: architecture-templates/dataverse-first.md
  - id: hybrid
    display_name: "Hybrid (Dataverse + SharePoint)"
    sub_template: architecture-templates/hybrid.md
inputs_used:
  - max_volume_per_entity        # peak record count for the largest entity (from operations + data lenses)
  - requires_audit_trail         # boolean — explicit audit/regulatory requirement (governance)
  - relational_integrity_required # boolean — ≥1 FK relationship with cascade/business-rule semantics (data)
  - delivery_timeline_weeks      # integer — committed delivery window (business + financial)
  - admin_team_capability        # enum: keyuser | internal_power_platform | partner_delivery (operations)
  - existing_sharepoint          # boolean — solution must integrate with an existing SharePoint footprint
---

# Decision Tree — Power Platform Architectural Branches

This tree is the **only** Discovery-output-driven mechanism the solution architect uses to shortlist architectural branches for the `pp` pack. It is consulted in the **Options phase** and never before. Each rule maps a condition over the listed inputs to a per-branch verdict; the solution architect aggregates verdicts across the rules and assigns scores (`forte`, `adequada`, `intermédia`, `inadequada`, etc.). The branching is then proposed as 3–5 options for the chairman to synthesise into `options.md`.

The Inputs are SU claims emitted by the Discovery lenses. If an input is missing (no corresponding SU id) → solution-architect must STOP at that rule, surface an `Unknown` for the missing fact, and either obtain it or proceed with an explicit Assumption (basis declared).

## The three branches

- **A — `sharepoint-first`**: SharePoint Online + Power Automate + Canvas App. Lowest licensing cost, fastest first delivery, weakest audit/integrity guarantees.
- **B — `dataverse-first`**: Dataverse + Model-driven App + Power Automate. Strongest audit/integrity, premium licensing baseline, longest first delivery.
- **C — `hybrid`**: Dataverse for critical entities + SharePoint for secondary/attachments + Canvas App. Middle ground; complexity of two systems but volume + integrity on the Dataverse side.

---

## R1 — Adequação ao volume

- IF `max_volume_per_entity` ≤ 5000 → A=adequada, B=forte, C=forte
- IF 5000 < `max_volume_per_entity` ≤ 100000 → A=inadequada, B=forte, C=forte
- IF `max_volume_per_entity` > 100000 → A=inadequada, B=adequada, C=adequada

## R2 — Governance e audit

- IF `requires_audit_trail` = true → A=básico, B=forte, C=forte
- ELSE → A=básico, B=intermédio, C=intermédio

## R3 — Esforço de implementação

- IF `delivery_timeline_weeks` ≤ 8 AND `max_volume_per_entity` ≤ 5000 → A=baixo, B=alto, C=alto
- IF `delivery_timeline_weeks` ≤ 12 → A=baixo, B=médio-alto, C=alto
- ELSE → A=baixo, B=médio, C=médio-alto

## R4 — Custo de licenciamento

- IF `requires_audit_trail` = true OR `relational_integrity_required` = true → A=mínimo, B=alto, C=médio
- ELSE → A=mínimo, B=alto, C=médio

## R5 — Manutenção contínua

- IF `admin_team_capability` = keyuser → A=baixa, B=alta, C=alta
- IF `admin_team_capability` = internal_power_platform → A=baixa, B=média, C=média-alta
- ELSE → A=baixa, B=média, C=média-alta

## R6 — Reversibilidade se errar

- IF `max_volume_per_entity` ≤ 5000 AND `requires_audit_trail` = false → A=alta, B=baixa, C=média
- ELSE → A=alta, B=baixa, C=média

---

## Exclusion side-effects

After rule evaluation, apply these exclusions before the solution architect proposes the option set:

- IF `relational_integrity_required` = true AND `max_volume_per_entity` > 5000 → **exclude `sharepoint-first` from top-N** (move to "Alternatives Considered" in deliverables; flag the reason).
- IF `delivery_timeline_weeks` < 8 → **exclude `dataverse-first` from top-N** (effort floor breach for a fresh build).
- IF `admin_team_capability` = keyuser AND `requires_audit_trail` = true → flag **both** `dataverse-first` and `hybrid` with `⚠️ requires_external_support` — the maintenance load is real even if the branch is otherwise viable.

---

## Missing inputs handling

If any input has no corresponding SU id when the architect is about to consult this tree:

1. Open an `Unknown` row in the SU (`lens: technology`, `criticidade`: Med-Critical depending on which rule blocks).
2. Either resolve it (USER_ANSWER, document hunt) or proceed with an explicit `Assumed` row (`base da assumption: industry default for <…> in similar PP engagements`). Both paths feed back into the branching verdict.
3. Re-evaluate the affected rule once the input is known. The previous verdict is invalidated; record the change in the chairman synthesis log.

This protocol is consistent with the project rule `library/kernel/states.md` (Confirmed vs Assumed vs Unknown) and the orchestration discipline that the council does not invent claims.

---

## Always include a do-nothing and a non-technology option

Independent of this tree, `aisa-options` requires that the proposed option set contains:

- **One do-nothing baseline** — the cost of the next 6–12 months without action; the cfo-lens persona is the natural anchor.
- **One non-technology option** — process change, reorganisation, manual control redesign. The operations-lead persona is the natural anchor. This option NEVER consults this decision tree (the tree is about technology branches only).

These two are added by the chairman during synthesis, not by this tree.
