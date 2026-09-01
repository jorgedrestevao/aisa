# UX Blueprint Contract — Kernel v0.2.0

The blueprint is the structured artefact that turns the engagement's knowledge into a designed application concept — **deciding the design** so any downstream renderer (Claude Design or other) only has to **render** it. It is produced by the `aisa-blueprint` skill in the Decision phase (see [`phases.md`](phases.md)) and iterated with the business until approved. This contract is platform-agnostic; screen catalogues, naming conventions and hard caps come from the active pack's `domain-knowledge/`.

## Artefact and versioning

- Path: `<engagement>/_blueprint/ux-blueprint_v<NN>.yaml` — versioned, append-only (never overwrite; mirrors `_render/`).
- `<engagement>/_blueprint/blueprint-log.md` — one line per version: timestamp, trigger (initial / feedback round / re-run), SU ids consumed, cap violations raised.
- Approval: a `D-NNN` block in `decisions.md` ("Blueprint bp-v<NN> aprovado") + the matching SU row. The approved version is frozen; changes after approval produce a new version and a new approval.

## Schema (top-level keys)

| Key | Content | Source |
|---|---|---|
| `blueprint_id`, `engagement`, `concretizes_decision`, `branch` | Identity + the D-NNN and branch this blueprint concretizes | `_state.json`, `decisions.md` |
| `app` | name, device_targets, language | SU + context.json |
| `personas` | id, label, rbac_group, `su_refs` | SU `lens=user` + pack security patterns |
| `entities` | name, expected volume, state machine, `su_refs` | SU `lens=data` (+ operations for volumes) |
| `navigation` | home per persona + screen map | derived by the UX architect |
| `screens` | name (pack naming convention), pattern (pack catalogue), purpose, primary_persona, density, data (entity, primary/secondary columns), actions (primary/secondary), rbac_visibility, ui_states (loading/empty/error), platform constraint notes, optional `excel_anchor`, `su_refs` | pack consolidation rules applied to the SU |
| `excluded_from_ui` | fields deliberately NOT shown, each with reason + `su_refs` | SU (sensitivity, governance) |
| `open_questions` | Unknown ids that block design decisions | SU `## Unknown` |
| `validation` | pack hard-cap check result + violations list | pack consolidation rules |

## Hard rules

1. **Provenance everywhere.** Every screen, field group, action and exclusion carries `su_refs`. A node with no SU anchor is either removed or turned into an `open_questions` entry — the blueprint never invents.
2. **`excluded_from_ui` is first-class.** Deciding what NOT to show (sensitive fields, internal calculation columns) is a design decision with an id trail, not an omission.
3. **Cap violations become Conflicted rows.** When the pack's hard caps are violated (too many fields/actions/entities per screen), the blueprint records the violation AND the skill appends a Conflicted row to the SU. Resolution happens through the normal `/answer` path.
4. **Draft mode before Decision.** `/blueprint --option O-NNN` during Options produces a `draft: true` blueprint for a candidate option (used by `/simulate`); drafts are never approvable.
5. **The renderer is replaceable.** Nothing in the blueprint may depend on a specific prototype tool. Platform specifics enter only through the pack's constraint notes.

## Downstream consumers

- `claude-design-brief` deliverable: renders its screen/navigation/UX sections from the **approved** blueprint.
- `implementation-spec` deliverable: `screens_to_build` comes from the approved blueprint — what gets built is what the business validated.
- `/simulate`: uses draft blueprints per option for the side-by-side comparison.
- Future traceability (post-handoff): the `su_refs` stamped here are the join key for spec-vs-implementation diffing.
