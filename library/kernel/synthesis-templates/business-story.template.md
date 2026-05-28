---
template_id: business-story
output_path: _synthesis/business-story.md
sources:
  - shared-understanding.md# lens=business (Confirmed + Assumed)
  - lens-outputs/business.md
  - frame.md
  - decisions.md# D-001 (frame agreed)
synthesis_prompt: |
  Write the business story of the engagement: the impact, the urgency, the
  stakeholders (declared and shadow), the KPIs at stake, and what the
  sponsor will recognise as success. Anchor every non-trivial claim to a
  Shared Understanding id (C-NNN, A-NNN) inline. No vendor or product
  names — this section is technology-neutral by design and will feed the
  client-facing Discovery Report and the sponsor-facing Executive Report.
---

# Business Story — {{slug}}

## Why this engagement exists
<one paragraph: the request as it landed (literal_request), the requester, the declared problem. Cite the frame sentence (D-001) where it is the cleanest summary.>

## Who actually feels the problem
<one paragraph: the declared stakeholders + the shadow stakeholders the council surfaced. Cite SU ids that anchor each.>

## The impact in business terms
<one paragraph: the KPI(s) at stake, the urgency (declared vs evidence-based), the cost of delay, prior attempts and why they failed. Cite SU ids.>

## What success looks like to the sponsor
<one paragraph: the recognisable outcome (process time cut, error rate down, audit gap closed, etc.). Stay outcome-language; no technology promises here.>

## Open issues still material to the business story
<bulleted list of Unknown/Conflicted ids that, if unresolved, would weaken the case to act>
