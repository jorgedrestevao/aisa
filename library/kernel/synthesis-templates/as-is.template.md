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
  technologies.

  CONSUMER (Step 6B projection model): the Discovery Report, which
  PROJECTS this narrative. This file is a bounded narrative projection and
  the Discovery Report is its consumer -- NEITHER is source authority.
  Authority stays upstream, with the artefacts Step 6A names: the Shared
  Understanding rows (facts and epistemic states), the capture / evidence
  index (sources analysed) and the framing record (scope).

  FORBIDDEN CONSUMERS. This topic is a forbidden source for the
  Architecture Blueprint; it is forbidden as the source of acceptance work
  or proof level in the Implementation Specification (friction may
  contribute test SCENARIOS, never a proof level -- defect D-7); and it is
  NOT an Estimate source in either input mode -- not required, not
  conditional, not fallback, not point-of-need. No as-is timing, friction
  or exception may become an Estimate work unit, effort figure or
  operational-impact baseline. Implementation effort reaches the Estimate
  only through the Implementation Specification's work inventory (mode A)
  or a candidate-specific KNOWN architecture obligation (mode B).

  Do not narrate a target architecture, a recommendation or an option
  conclusion here, and add no effort or estimate content.
---

# As-Is — {{slug}}

## End-to-end process today
<paragraph or numbered list reconstructing the real flow from the operations lens. Cite SU ids and the lens-outputs/operations.md narrative.>

## Volume and cycle time
<paragraph quantifying volume, peaks, and cycle time (current vs target if stated). Cite SU ids and any input artefact (e.g., the inputs/*.xlsx profile if relevant).>

### Passos e tempo (P-5)
<one row per named step of the as-is, carried from the operations lens rows (`step_duration`):
| passo | quem | tempo | estado · base | fonte |
`tempo` is the recorded figure with its unit; `estado · base` is `Assumed — <locator>` or `Unknown (U-nnn, custo=email)`;
never a guessed figure, never a total spread evenly. Close with the cycle total where the SU carries one (pilot-1: `C-030`, < 1h/dia).
This table is the ONE contracted source of the Implementation Specification's *Alteração do caminho operacional* section (P-10);
it is NOT an Estimate source in any mode (see FORBIDDEN CONSUMERS above) — the Estimate reads that change from the Specification.>

## Personas and their experience
<paragraph or per-persona bullets: who uses the process today, on what device, in what context, with what friction. Cite SU ids and lens-outputs/user.md.>

## Exceptions, handoffs, and tribal knowledge
<paragraph: what the happy path hides — exceptions, escalations, undocumented judgement, load-bearing spreadsheets only one person understands.>

## Top friction points
<bulleted list: the 3–6 friction points the operations and user lenses converged on; cite SU ids.>
