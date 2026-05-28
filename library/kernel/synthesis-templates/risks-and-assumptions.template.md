---
template_id: risks-and-assumptions
output_path: _synthesis/risks-and-assumptions.md
sources:
  - shared-understanding.md# Risky (all) + Assumed (all) + Unknown (criticidade=Critical)
  - decisions.md# Accepted risks + Revision conditions from D-NNN
synthesis_prompt: |
  Consolidate the risks and assumptions the engagement carries forward.
  Distinguish between (a) Assumed claims that must be validated during
  build, (b) accepted risks (with mitigations), and (c) unresolved
  Unknowns of Critical criticality. For each, state the impact, the
  proposed mitigation, and the revision trigger (from D-NNN) if one
  applies. Cite SU ids inline.
---

# Risks and Assumptions — {{slug}}

## Assumptions to validate during build
<list of A-NNN rows that must be confirmed (e.g., as-is cost figures, sponsor authority levels, integration patterns). For each: the assumption, the basis, who validates it, and by when.>

## Accepted risks (with mitigations)
<list of R-NNN rows accepted as part of the decision. For each: the risk, the impact, the agreed mitigation, the revision trigger from D-NNN.>

## Unresolved Unknowns (Critical)
<list of U-NNN rows still open with criticidade=Critical. For each: the question, who can answer, the impact of leaving it open, the recommended next step.>

## Conflicts still on the table
<list of X-NNN rows not yet resolved (if any). Each should already have been resolved via /decide; flag any that remain.>

## Watch-list summary
<bulleted list: the measurable revision triggers from D-NNN — the engagement is committing to revisit the decision if any of these fires.>
