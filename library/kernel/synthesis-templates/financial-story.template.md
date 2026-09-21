---
template_id: financial-story
output_path: _synthesis/financial-story.md
# ── SCOPE: DECISION ECONOMICS NARRATIVE ONLY (Step 6A §18.1, §40.5) ───────────────────
# This synthesis topic carries DECISION ECONOMICS and NOTHING ELSE.
#
# The implementation-estimate calculation was REMOVED from this template in Step 6B. It is
# semantically owned by the `estimate` deliverable and executed by `aisa-render` under that
# deliverable's projection contract, from the Implementation Specification's inventory
# (mode A) or the candidate architecture record (mode B), with the method from
# `craft/estimation-model.md`.
#
#   S8 decision economics  -> option attractiveness / worth choosing   -> HERE, and the
#                                                                         Executive Report
#                                                                         projects it
#   implementation effort  -> how much work the chosen path is        -> the Estimate
#                                                                         deliverable
#
# NOT the same question, and NOT merged. No second synthesis file is created for
# implementation effort.
computes_implementation_effort: false
owns_calculation: false
forbidden_outputs:
  - a phased build plan
  - a per-phase effort table
  - a week-by-week timeline / Gantt
  - an effort summary in days
  - a team-by-profile effort table
  - an operational-impact delta table
  - any person-day figure
  - any total duration derived from work units
  - delivery recommendations
estimate_reference_rule: |
  Any implementation-effort sentence here may only REFERENCE or PROJECT an ALREADY-PRODUCED
  Estimate, citing it. It is never the calculation source and never where a figure first
  appears. Preferred outcome: no implementation-effort figure appears here at all.
sources:
  - shared-understanding.md# lens=financial
  - lens-outputs/financial.md
  - decisions.md# D-NNN — Conditions, Accepted risks, Revision conditions (economic anchors)
  - options.md# S8 (decision economics, as recorded — never re-compared)
synthesis_prompt: |
  Tell the DECISION-ECONOMICS story and stop there: the as-is cost baseline, the cost of
  doing nothing, the budget envelope and funding model, the payback profile of the chosen
  option, the entitlement and cost DRIVERS the decision rests on, and the financial revision
  triggers. Cite SU ids inline. Cost figures are Assumed unless documented — say so
  explicitly when a figure is inferred, and carry `verificado_em` / `validade` for any
  volatile value.

  DO NOT compute, decompose or table implementation effort. No phased build plan, no
  per-phase day counts, no timeline, no effort summary, no team-by-profile table, no
  operational-impact delta, no person-day total. That calculation belongs to the `estimate`
  deliverable, which is its semantic owner; `aisa-render` executes it. If an
  implementation-effort figure is needed in prose here, cite the already-produced Estimate
  as its source — never derive one.

  DO NOT emit prices, SKUs, platform rate cards, or quotas presented as cost facts. Drivers
  only.

  Vendor/product/platform naming is NOT allowed in this topic (it mirrors Discovery's
  neutrality); the chosen architecture is narrated in `architecture-story.md`. Refer to
  entitlement classes and audiences, not to products.
---

# Financial Story — {{slug}}

> **Economia de decisão apenas.** Este pacote responde a *vale a pena escolher esta opção?* — não a
> *quanto trabalho dá o caminho escolhido?*. Essa segunda pergunta pertence à entrega `estimate`, que é
> a dona semântica do cálculo. Nenhuma figura de esforço de implementação nasce aqui.

## As-is cost baseline
<paragraph quantifying what the current process costs — time, errors, delay, rework. Cite A-NNN or C-NNN rows; declare the basis for any inferred figure; carry `verificado_em` / `validade` for any volatile value.>

## Cost of doing nothing
<paragraph: the cost of the next 6–12 months if nothing changes. Anchor to the financial lens.>

## Budget envelope and funding
<paragraph: the budget envelope, approval threshold, CAPEX/OPEX, chargeback model. Cite SU ids.>

## Economic attractiveness of the chosen option
<paragraph at DECISION altitude (S8, as recorded): why the chosen option is economically defensible — or the recorded reason it is unattractive. Project the recorded economics; create no fresh comparison and no ranking. Anchor to D-NNN. NO effort figure, NO phase plan, NO duration derived here.>

## Entitlement and cost drivers
<bulleted list: the entitlement class per audience, the affected population, the meters engaged, and the growth driver at the stated horizon. DRIVERS ONLY — no prices, no SKUs, no quotas as cost facts. Cite the owning economics unit for what a driver IS; do not restate its content.>

## Payback / ROI
<paragraph: the payback period or ROI that makes this a clear yes for the sponsor. Cite the KPI targets from the business story. Where the decision recorded none, say so — the absence is honest.>

## Sensitivity and revision triggers
<bulleted list: the financial revision triggers from D-NNN (e.g., volume thresholds, entitlement shifts) that would force a re-think. Anchor each to its TW-n.>

## Investment reference
<ONE short paragraph, and ONLY where an Estimate has already been produced: cite the Estimate's headline and its file (`_render/<slug>_estimate_v<NN>.md`) as the source of the effort figure. Where no Estimate exists yet, write `Estimativa ainda não produzida — ver a entrega \`estimate\`.` NEVER derive a figure here.>
