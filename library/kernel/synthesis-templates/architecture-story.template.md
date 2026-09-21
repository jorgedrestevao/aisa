---
template_id: architecture-story
output_path: _synthesis/architecture-story.md
sources:
  - decisions.md# chosen option + selected solution + (scope, outcome) pairs
  - _blueprint/ux-blueprint_v<NN>.yaml# architecture
  - shared-understanding.md# lens IN (technology, data)
  - lens-outputs/technology.md
  - lens-outputs/data.md
  - library/packs/<pack>/architecture-templates/architecture-core.md

# ── I-1 — DURABLE CARRIAGE, NOT SEMANTIC AUTHORITY (Step 6A §21, §40.3) ───────────────
# This file is a BOUNDED NARRATIVE PROJECTION. It is NOT architecture authority.
#
#   outcome basis
#     semantic owner  -> the Options layer that emitted the outcome sentence
#     durable source  -> decisions.md# (Scope, outcome) pairs — UNCOLLAPSED
#
#   architectability basis
#     semantic owner  -> THE ARCHITECTURE-ENTRY GATE RULE
#                        (the selected solution x the frozen active-pack architectability
#                        boundary, per architecture-templates/README.md)
#     durable carrier -> this file, section `Authorized scope and outcome basis`
#                        (ONLY where no architecture artefact exists to hold it)
#
# As DURABLE CARRIER this file:
#   - does NOT own the rule;
#   - may NOT change the wording's meaning;
#   - may NOT widen or narrow the active pack's architecture authority;
#   - may NOT introduce a new basis;
#   - must carry a result REPRODUCIBLE from the already-recorded selected solution x the
#     frozen active-pack architectability boundary.
#
# Downstream deliverables read it AS THE DURABLE CARRIER OF AN ARCHITECTURE-ENTRY RESULT,
# never as a source of architectural truth, and NO deliverable re-evaluates pack
# architectability. THIS IS THE ONLY CARRIAGE EXCEPTION IN THE MODEL, and it does not
# generalize to any other architecture field.
carriage:
  architectability_basis:
    role: durable carrier
    is_semantic_authority: false
    semantic_owner: the architecture-entry gate rule
    exception_scope: this one basis only
  outcome_basis:
    role: projection
    is_semantic_authority: false
    semantic_owner: the Options layer that emitted the outcome sentence
    durable_source: decisions.md
is_architecture_authority: false

synthesis_prompt: |
  Narrate the architecture of the chosen option. State the authorized
  scope, its outcome basis, the architecture intent, the composition,
  the boundaries, and the imported obligations each boundary component
  carries. Then the data authority per domain, the integrations, the
  security model, and the constraints on the watch-list. Vendor and
  product names ARE allowed here (this is the only synthesis topic where
  that is true). Anchor to the chosen decision (D-NNN), the recorded
  architecture block, and SU ids for technology + data.

  Read authorization; never derive, upgrade or downgrade it. Where no
  scope is authorized, describe the chosen intervention and state the
  actual reason no architecture exists — the outcome forbade one, or the
  selected solution is outside the active pack's architecture authority —
  keeping the two reasons distinct.

  I-2 — NO FRESH COMPARISON. Do not explain why an architecture "won".
  Reproduce THE JUSTIFICATION THE DECISION RECORDED
  (`decisions.md# D-NNN — Justification`) in substance, plus the recorded
  per-alternative "why not" lines where they are cited. Create no new
  comparison, no ranking, no score and no superiority claim. Where the
  decision recorded no comparison, record none — the absence is honest.
  Stating a comparator's recorded STATUS (`COMPARATIVE FIT UNEVALUATED`,
  `INCUMBENT FIT UNEVALUATED`, class 9's single-axis evidence) is not a
  comparison: those are recorded facts and they render verbatim.

  I-1 — CARRIAGE, NOT AUTHORITY. Where the architecture-entry gate yielded
  `not-authorized`, this file is the DURABLE CARRIER of that result and NOT
  its semantic authority: the semantic owner is the entry gate's own rule.
  Carry the architectability basis as a reproducible evaluation of the
  pack's frozen architectability boundary against the recorded selected
  solution — never a fresh judgement, never re-scoped, never widened or
  narrowed. Never label this file the source of architectural truth.

  Do not compute or table implementation effort here; that belongs to the
  `estimate` deliverable. Do not re-grade a proof obligation, promote an
  epistemic state, or choose a side of a Conflicted row.
---

# Architecture Story — {{slug}}
<!-- authority: _blueprint/ux-blueprint_v<NN>.yaml#architecture @ sha256:<hex> — written verbatim from
     `python library/kernel/tools/dashboard.py --engagement <slug> --authority-stamp` (P-18 / F04). Names the
     blueprint version whose architecture block this story projects; the motor compares it with the approved one. -->

## Authorized scope and outcome basis

<!--
DURABLE CARRIER — NOT SEMANTIC AUTHORITY.
Where the architecture-entry gate yielded `not-authorized`, no blueprint version exists to hold
the pair, and THIS SECTION is its durable carrier. The SEMANTIC OWNER of the architectability
basis is the ARCHITECTURE-ENTRY GATE RULE (the recorded selected solution x the frozen
active-pack architectability boundary). The outcome basis's durable source is `decisions.md`.
This section owns neither rule; it carries a reproducible result. No downstream deliverable
may treat it as architecture authority, and none may re-evaluate pack architectability.
-->

<one line per emitted `(scope, outcome)` pair, UNCOLLAPSED, each carrying the outcome sentence verbatim; then the authorization value and, in one sentence each, its outcome basis and its architectability basis. Cite D-NNN. Where the value is `not-authorized`, keep the two reasons DISTINCT, state that the architectability basis is the recorded evaluation of this pack's frozen architectability boundary against the selected solution, and never relabel a positive non-pack outcome as *Decision Blocked*.>

## Chosen architecture
<one paragraph: the option chosen (O-NNN), the architecture intent — the requirement each structural choice answers — and the justification the decision recorded (`decisions.md# D-NNN — Justification`), reproduced verbatim in substance. Create no new comparison. Cite D-NNN and the relevant SU ids.>

## Composition, components and boundaries
<paragraph or bulleted list naming the platform and the major components, using the names the recorded architecture block gives them — the kernel stays vendor-neutral; platform vocabulary enters only via the pack. State per component: what forced it, whether it sits inside or outside platform governance, which trust boundary it crosses, and who owns it. Anchor to the pack's `architecture-templates/architecture-core.md`. For a non-technology / do-nothing decision, describe the chosen intervention instead (no platform, no architecture template).>

## Imported obligations
<per boundary component: the obligations the engaged composition imports — governance, ALM, cost, monitoring, recovery and operator. Cite the pack's architecture-pattern unit; do not restate its mechanisms, limits or risk catalogue. A relocated responsibility gets its boundary, owner and outcome basis — never a design for the far side, and never an inferred comparator fit.>

## Data
<paragraph: entities, where each lives, sensitivity, ownership, retention. Cite SU ids from the data lens and lens-outputs/data.md.
Then the DICTIONARY TABLE, carried (never authored) from the stamped blueprint version's `record_authority[]` (P-6):
one row per domain — `key` · `access_mode` · owned: n campos / externo: n lidas · n escritas · `key[]` · dono do schema
(com estado) · estado das linhas (n Assumed / Confirmed / Unknown) · entidades do blueprint que apontam para ele.
A domain no entity points at, or an entity whose `authority` does not resolve, is written as such — this file is a
carrier: it copies the record's counts and states, decides no disposition, promotes no line, invents no field.>

## Integrations
<paragraph or list: external systems to read from / write to, the connectors/APIs involved, the DLP policy classification.>

## Security model
<paragraph: roles and what each may do, the plane that enforces it, the permission split where an obligation in scope requires one, and the audit trail where a requirement covers it — each of the last two only if the engagement has it. No approval ladder and no signature: where approval is behaviour of the process, it is states, transitions and the role authorised at each. Anchor to the security knowledge unit the architecture layer actually cited; the pack's manifest names it.>

## Watch-list constraints
<bulleted list: the pack's `lenses_config.technology.constraints_to_check` items the round found
material, each with the finding the round recorded against it — in that round's own vocabulary
(disqualifier at its scope · precondition · trade-off · risk · uncertainty) — and the trigger that
would force a re-think. Cite the corresponding revision conditions from D-NNN. PROJECT the recorded
finding: do not restate it as a verdict on a scale this model does not have, and do not grade a
constraint the round did not find material.>
