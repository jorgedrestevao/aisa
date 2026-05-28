---
template_id: as-is
output_path: _synthesis/as-is.md
sources:
  - shared-understanding.md# lens IN (operations, user)
  - lens-outputs/operations.md
  - lens-outputs/user.md
synthesis_prompt: |
  Reconstruct the real as-is process and user experience. Describe the
  flow, the handoffs, the exceptions, the tribal knowledge, the personas
  affected, their devices, and the top friction in their words. Cite SU
  ids inline. Existing systems may be named as current state (e.g.,
  "approvals tracked in a shared spreadsheet") but do NOT name solution
  technologies. This section feeds the Discovery Report and Solution
  Blueprint (as the baseline the chosen option must improve upon).
---

# As-Is — {{slug}}

## End-to-end process today
<paragraph or numbered list reconstructing the real flow from the operations lens. Cite SU ids and the lens-outputs/operations.md narrative.>

## Volume and cycle time
<paragraph quantifying volume, peaks, and cycle time (current vs target if stated). Cite SU ids and any input artefact (e.g., the inputs/*.xlsx profile if relevant).>

## Personas and their experience
<paragraph or per-persona bullets: who uses the process today, on what device, in what context, with what friction. Cite SU ids and lens-outputs/user.md.>

## Exceptions, handoffs, and tribal knowledge
<paragraph: what the happy path hides — exceptions, escalations, undocumented judgement, load-bearing spreadsheets only one person understands.>

## Top friction points
<bulleted list: the 3–6 friction points the operations and user lenses converged on; cite SU ids.>
