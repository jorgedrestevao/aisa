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
  of the chosen option. Then decompose the build into a phased plan with
  per-phase task/effort/owner detail, a week-by-week timeline, an effort
  summary, a team-by-profile table, and the expected operational impact
  (as-is time vs target time per step). Cite SU ids inline. Cost and
  effort figures are Assumed unless documented — say so explicitly when
  a figure is inferred. Vendor/product/platform and role naming IS
  allowed in this story (the chosen architecture is fixed at Decision):
  anchor every named component to the architecture story and D-NNN. The
  phased plan, timeline, and operational-impact sections feed the
  Estimate deliverable directly — produce them as tables exactly in the
  shapes shown below.
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

## Estimate headline
<a single summary line (used as the deliverable's headline box) in the form:
`Duração total: <N semanas / ~N meses> | Sprints: <N sprints, cadência> | Equipa: <N pessoas + SMEs> | Risco global: <Baixo|Médio|Alto> (<one-line reason>)`. Anchor the duration and team size to the phased build plan below.>

## Phased build plan
<a markdown table — one row per phase, in execution order — with columns:
`Fase | Descrição | Duração | Responsável`. Include a Fase 0 (preparation/mapping) if the engagement carries discovery risk. Anchor each phase to the architecture story scope and to D-NNN. Name platform/components/roles freely (the architecture is fixed).>

## Detailed estimate by phase
<for EACH phase in the phased build plan, emit a level-3 heading `### <Fase N — name> | <weeks> / <working days>` followed by a markdown table with columns `Tarefa | Dias | Responsável` and a final `TOTAL <Fase N> | <days> |` row. Where a phase carries a material risk, add a short `> ⚠ RISCO:` callout line after its table. Effort in days is Assumed unless a documented basis exists — say so.>

## Timeline
<a markdown table representing a week-by-week Gantt: first column `Fase / Semana`, then one column per week (`S1`, `S2`, …). Mark active weeks with `█` and idle weeks blank. One row per phase. State total duration and any phases that can run in parallel.>

## Effort summary by phase
<a markdown table with columns `Fase | Semanas | Dias úteis | Notas` — one row per phase — and a final `TOTAL | <weeks> | <days> | <~N meses>` row. Notes call out blocking phases and the highest-risk phase.>

## Team and effort by profile
<a markdown table with columns `Perfil | Responsabilidades | Dedicação | Pessoas`. One row per delivery profile (e.g., platform developer, BI developer, SME). Anchor responsibilities to the phased plan scope.>

## Operational impact
<a markdown table with columns `Passo | Quem (atual) | Tempo atual | Novo processo | Tempo novo | Δ` — one row per current process step from the as-is story — and a final `TOTAL DIÁRIO ESTIMADO | … | <as-is total> | … | <target total> | <delta>` row. Anchor the as-is times to the as-is/operations story and the targets to the chosen architecture.>

## Recommendations
<a numbered or bulleted list of the strategic recommendations the estimate should carry — e.g., treat preparation/mapping as a critical deliverable, de-risk the hardest integration first, pilot before full rollout, share infrastructure across related initiatives. Each recommendation states the why. Anchor to the risks story and D-NNN.>
