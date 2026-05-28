---
template_id: financial-story
output_path: _synthesis/financial-story.md
sources:
  - shared-understanding.md# lens=financial
  - lens-outputs/financial.md
  - decisions.md# cost/timeline anchors
synthesis_prompt: |
  Tell the financial story end to end: as-is cost, do-nothing cost,
  budget envelope, funding model, build effort, and the payback profile
  of the chosen option. Cite SU ids inline. Cost figures are Assumed
  unless documented — say so explicitly when the figure is inferred.
  Vendor/product naming is allowed only when referencing the chosen
  option's licensing component anchored in D-NNN.
---

# Financial Story — {{slug}}

## As-is cost baseline
<paragraph quantifying what the current process costs — time, errors, delay, rework. Cite A-NNN or C-NNN rows; declare the basis for any inferred figure.>

## Cost of doing nothing
<paragraph: the cost of the next 6–12 months if nothing changes. Anchor to the financial lens.>

## Budget envelope and funding
<paragraph: the budget envelope, approval threshold, CAPEX/OPEX, chargeback model. Cite SU ids.>

## Build effort and indicative cost
<paragraph: the effort band from the chosen option (Small/Medium/Large), the indicative cost, the build timeline. Anchor to D-NNN and the architecture story.>

## Payback / ROI
<paragraph: the payback period or ROI that makes this a clear yes for the sponsor. Cite the KPI targets from the business story.>

## Sensitivity and revision triggers
<bulleted list: the financial revision triggers from D-NNN (e.g., volume thresholds, licensing cost shifts) that would force a re-think.>
