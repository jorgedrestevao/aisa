---
template_id: risks-and-assumptions
output_path: _synthesis/risks-and-assumptions.md
sources:
  - shared-understanding.md# Risky (all) + Assumed (all) + Unknown (criticidade=Critical) + Conflicted (unresolved)
  - shared-understanding.md# Confirmed (rows whose validade has EXPIRED)
  - decisions.md# Accepted risks + Conditions + Preconditions + Proof obligations + Revision conditions from D-NNN

# ── BOUNDED NARRATIVE PROJECTION (Step 6A §25, §29) ───────────────────────────────────
# This file NARRATES; it is NOT the authority for any item it carries.
#   epistemic state        -> shared-understanding.md row state (+ library/kernel/states.md)
#   accepted risk          -> decisions.md# Accepted risks
#   condition/precondition -> decisions.md# Conditions / # Preconditions
#   proof obligation       -> decisions.md# Proof obligations -> the architecture block
# Every item is carried WITH ITS ID AND ITS STATE. Synthesis may compress and order; it may
# not decide, re-grade, promote, resolve or choose a side.
is_authority: false
always_retain:
  - the row id (A-NNN · R-NNN · U-NNN · X-NNN · C-NNN)
  - the row state
  - verificado_em / validade where the row carries them
forbidden:
  - promoting Assumed to Confirmed, or an expired Confirmed to fact
  - resolving an Unknown, or converting one into an assumption or a finding
  - choosing a side of a Conflicted row (with or without a caveat)
  - re-grading a proof obligation's level (V1–V4), method, owner or funded state
  - marking a proof obligation or a condition satisfied
  - dropping the accepted-risk identity of a Risky row
  - computing any implementation-effort figure

synthesis_prompt: |
  Consolidate the risks, assumptions, open questions and obligations the
  engagement carries forward. Keep six things distinct: (a) Assumed claims
  that must be validated, (b) accepted risks with their mitigations,
  (c) unresolved Unknowns of Critical criticality, (d) unresolved
  Conflicted rows, (e) the conditions, preconditions and proof obligations
  the decision recorded, and (f) Confirmed rows whose validity has EXPIRED.
  For each, state the impact, the proposed mitigation or validation, and
  the revision trigger from D-NNN if one applies. Cite SU ids inline and
  keep every state as recorded.

  Never promote a state for brevity. An expired Confirmed is a
  re-verification obligation, never a fact. A Conflicted row renders the
  conflict or omits the value — choosing a side is prohibited. An Unknown
  stays open. A proof obligation is QUOTED in its five-part shape
  (claim · level V1–V4 · method · owner · funded?) and never re-graded. A
  condition is never rendered as already satisfied: it becomes satisfied
  only through engagement evidence.

  Compute no effort figure. Vendor/product naming is not allowed in this
  topic.
---

# Risks and Assumptions — {{slug}}

## Assumptions to validate during build
<list of A-NNN rows that must be confirmed (e.g., as-is cost figures, sponsor authority levels, integration patterns). For each: the assumption, the basis, who validates it, by when, and `verificado_em` / `validade`. Never promoted.>

## Accepted risks (with mitigations)
<list of R-NNN rows accepted as part of the decision. For each: the risk, the impact, the agreed mitigation, the revision trigger from D-NNN. An accepted risk is NOT a mitigated risk — keep the accepted-risk identity.>

## Unresolved Unknowns (Critical)
<list of U-NNN rows still open with criticidade=Critical. For each: the question, who can answer, the impact of leaving it open, the recommended next step. None is resolved here.>

## Conflicts still on the table
<list of X-NNN rows not yet resolved (if any). For each: BOTH sides verbatim with the origin of each, and what would settle it. NEITHER side is chosen. Flag any that a decision passed over.>

## Expired validity — re-verification obligations
<list of Confirmed rows whose `validade` has EXPIRED, plus any Assumed row past its validity. For each: the fact as it was recorded, `verificado_em`, the expired `validade`, the re-question to ask, and who can answer. Rendered as an OBLIGATION, never as a fact.>

## Conditions and preconditions the decision recorded
<list from D-NNN: each as *condition — owner — funded? — by when*, and each precondition as *what must be true before work starts*. Include `not named` where the source named no owner or date. NEVER rendered as satisfied.>

## Proof obligations
<list from D-NNN, carried into the architecture block: each QUOTED in its five-part shape — *claim · level (V1–V4) · method · owner · funded?*. Never re-graded, never re-methoded, never marked satisfied.>

## Watch-list summary
<bulleted list: the measurable revision triggers from D-NNN — the engagement is committing to revisit the decision if any of these fires. One line per TW-n with its SU source.>
