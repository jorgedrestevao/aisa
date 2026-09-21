---
template_id: executive-report
canonical_deliverable: executive-report
output_format: md
audience: sponsor

# §8.3 — altitude de decisão: inventários de ecrãs não são conteúdo de decisão.
blueprint_version_read: none

# ── PROJECTION CONTRACT ────────────────────────────────────────────────────────────────
# This template DECLARES; it does not execute. `aisa-render` executes only the
# transformations listed in `permitted_transformations`.
# Altitude: DECISION. Reads in ~10 minutes.
# Primary semantic authority: decisions.md (D-NNN).

activation: always

authority_sources:
  - decisions.md# D-NNN                         # PRIMARY — the decision and everything it recorded
  - _synthesis/business-story.md                # problem / value, at sponsor altitude
  - _synthesis/risks-and-assumptions.md

conditional_sources:
  - the architecture block A1 / A2 / A9         # SHAPE ONLY, where an authorization exists
  - _synthesis/architecture-story.md            # narrative; and the I-1 durable carriage
  - decision-economics narrative                # _synthesis/financial-story.md — attractiveness,
                                                # envelope, funding, payback (S8 altitude)
  - the Estimate's headline                     # ONE investment paragraph, where an estimate exists
  - shared-understanding.md                     # validity / state display of decision-changing rows

forbidden_sources:
  - options.md as a whole-file read             # invites a re-staged comparison (I-2)
  - raw evidence · inputs/* · _capture/*        # nothing is re-settled here
  - any Domain Knowledge unit
  - any CRAFT unit
  - architecture-core.md sections A3–A8, A10–A12   # architecture detail below decision altitude
  - the boundary fragments · import channels
  - _blueprint/ux-blueprint_v<NN>.yaml          # screen inventories are not decision content
  - "another deliverable's narrative as authority — the ONLY exception is the Estimate's
     own headline figure, projected as one paragraph (§5, §28.2); no other _render/ file
     is a source here"

permitted_transformations:
  - compression to sponsor language (no kernel jargon, no lens names)
  - prose over tables, EXCEPT the (scope, outcome) pairs and the tripwires
  - one investment paragraph projected from the Estimate — never a phase table
  - architecture NAMED, not described
  - table<->prose · reordering · audience re-voicing

forbidden_transformations:
  - creating any new option comparison, ranking, score or superiority claim
  - converting a condition into a satisfied state
  - dropping a marker (COMPARATIVE FIT UNEVALUATED · INCUMBENT FIT UNEVALUATED)
  - collapsing or re-wording a (scope, outcome) pair
  - re-grading a proof obligation (V1–V4), its method, owner or funded state
  - promoting an epistemic state · rendering an expired Confirmed as fact
  - deriving a phase plan, an effort figure or a build sequence
  - "projecting phases, work breakdown, team mix, contingency derivation or rate, effort
     arithmetic, delivery duration or calendar schedule, a detailed uncertainty inventory, or
     candidate inventories from the Estimate into the investment paragraph — the Estimate
     remains the authority for all of them and the bounded edge does not carry them"
  - recalculating, re-rounding, recombining or interpolating an effort figure
  - blending candidate planning estimates into one headline figure, or naming a best candidate
  - reconstructing the as-is, the data inventory or a perspective-by-perspective walk
  - inferring anything about a non-PP selected solution's fit, quality or cost
  - relabelling a positive non-PP outcome as `Decision Blocked`

# ── THE RATIONALE RULE (I-2, §9.1) ────────────────────────────────────────────────────
rationale_rule: |
  This report reproduces THE JUSTIFICATION THE DECISION RECORDED
  (decisions.md# Justification + the per-alternative "why not" lines, as recorded).
  It does NOT explain why an architecture "won". Where the decision recorded no
  comparison, this report records none — the absence is honest, not a gap.
  Project existing comparison EVIDENCE only; create no fresh comparison.

# ── BOUNDED SLOT PAYLOAD — the estimate → executive edge (§6.5, render-contract.md) ─────
# The edge itself is unchanged and authorized: the Estimate is the ONLY `_render/` file this
# report reads, and it reads ONLY the headline. What follows defines WHAT A HEADLINE IS, so
# that "one paragraph" is not filled differently by different runs.
#
#   The Executive receives THE RESULT, not the calculation anatomy.
#
# The question the paragraph answers: WHAT DELIVERY MAGNITUDE SHOULD THE SPONSOR UNDERSTAND?
# It does not answer who staffs it, how contingency was derived, how phases are structured,
# what the calendar is, or which candidate contains which tasks.
slot_payload:
  investment_summary:
    form: ONE paragraph, maximum
    includes:
      - base_effort                    # e.g. "27 pessoa-dias base"
      - effort_range                   # e.g. "25–32"
      - contingency_inclusive_total    # e.g. "32,4 dias" — the TOTAL, never the rate
      - confidence_statement           # e.g. "confiança média-alta"
    excludes:
      - phases
      - work_breakdown
      - team_mix                       # profiles, headcount, allocation percentages
      - contingency_rate_or_derivation # "+20%", "10% over the named items", how it was applied
      - effort_arithmetic              # bands x units, multipliers, buffers, sums
      - duration_or_calendar_schedule  # weeks, months, go-live dates
      - candidate_inventories
      - detailed_uncertainty_inventory # counts or lists of named uncertainty lines
    attribution: |
      The paragraph names the Estimate as the owner of the figure. The Executive PROJECTS it;
      it never recomputes, re-rounds, recombines, interpolates or derives from it.
    unresolved_architecture_rule: |
      MODE B — where architecture remains structurally unresolved and only CANDIDATE PLANNING
      ESTIMATES exist, the Executive may NOT combine them into one headline. Either OMIT the
      investment paragraph, or state QUALITATIVELY that separate candidate planning estimates
      exist and reference them WITHOUT blending. No midpoint, no combined range, no
      "best candidate" figure, no scoring.

# ── NON-OMISSIBLE CONTENT (§9.2) ──────────────────────────────────────────────────────
# Each is `required SUBJECT TO EXISTENCE`: absent upstream => not-applicable skip;
# present upstream => it RENDERS. Compression may never drop one.
non_omissible:
  - scope_outcome_pairs          # uncollapsed
  - conditions
  - preconditions
  - accepted_risks
  - proof_obligations            # decision-changing only, at this altitude
  - structural_open_choices
  - revision_tripwires
  - architectability_basis       # where no architecture is authorized (I-1)

# ── EPISTEMIC PROJECTION (§15) ────────────────────────────────────────────────────────
epistemic_projection:
  Confirmed: stated as fact
  Confirmed_expired: only if decision-changing — and then as a re-verification obligation, never fact
  Assumed: assumed where material to the decision
  Unknown: decision-changing ones only, as OPEN — never filled
  Conflicted: only if decision-changing; render the conflict, choose no side
  Risky: accepted-risk identity + consequence — an accepted risk is not a mitigated risk

# ── PROOF-OBLIGATION CARRIAGE (§16) ───────────────────────────────────────────────────
proof_obligation_carriage:
  scope: decision-changing / high-level obligations ONLY
  form: claim · why it qualifies the decision · owner · funded?
  rule: quoted from the record; the level (V1–V4), the method, the owner and the funded state
    are never changed, and no obligation is ever marked satisfied here

# ── I-1 CARRIAGE (§21, §40.3) ─────────────────────────────────────────────────────────
not_authorized_carriage:
  outcome_basis:
    semantic_owner: the Options layer that emitted the outcome sentence
    durable_source: decisions.md# (Scope, outcome) pairs — UNCOLLAPSED
  architectability_basis:
    semantic_owner: the architecture-entry gate rule (selected solution x the frozen
      active-pack architectability boundary)
    durable_carrier: _synthesis/architecture-story.md# Authorized scope and outcome basis
    note: |
      DURABLE CARRIER, NOT SEMANTIC AUTHORITY. This report reads it as the durable carrier
      of an architecture-entry result, never as a source of architectural truth, and never
      re-evaluates pack architectability. The two reasons stay DISTINCT and neither is
      relabelled `Decision Blocked`.

required_slots:
  - solution_name
  - business_case
  - the_decision
  - scope_outcome_pairs
  - decision_justification
  - conditions_and_preconditions
  - accepted_risks
  - risks_and_mitigations
  - what_happens_next

conditional_slots:
  - architecture_shape
  - architectability_basis
  - investment_summary
  - decision_economics
  - proof_obligations
  - structural_open_choices
  - revision_tripwires
  - alternatives_why_not
  - open_epistemics

slot_conditions:
  architecture_shape: an architecture authorization exists for at least one scope
  architectability_basis: authorization == not-authorized for every scope
  investment_summary: an Estimate exists for this engagement AND it is not a set of unblended
    candidate planning estimates (mode B — see slot_payload.investment_summary)
  decision_economics: S8 / decision-economics content exists upstream
  proof_obligations: decisions.md# Proof obligations is non-empty (decision-changing subset)
  structural_open_choices: open_architecture_choices[] contains a structural:true entry
  revision_tripwires: decisions.md# Revision conditions / Tripwires is non-empty
  alternatives_why_not: decisions.md# Alternatives considered carries recorded why-not lines
  open_epistemics: a decision-changing Assumed / Unknown / Conflicted / expired Confirmed exists

slot_sources:
  business_case: _synthesis/business-story.md# What success looks like to the sponsor, The impact in business terms
  the_decision: decisions.md# D-NNN — Chosen option, Selected solution / composition (plain language, as recorded)
  scope_outcome_pairs: decisions.md# D-NNN — (Scope, outcome) pairs — UNCOLLAPSED (verbatim, every marker preserved)
  decision_justification: decisions.md# D-NNN — Justification (the justification the decision recorded)
  alternatives_why_not: decisions.md# D-NNN — Alternatives considered (the RECORDED per-alternative why-not lines only)
  conditions_and_preconditions: decisions.md# D-NNN — Conditions + Preconditions (each as condition — owner — funded? — by when; `not named` included)
  accepted_risks: decisions.md# D-NNN — Accepted risks (+ the SU R-NNN rows it points at)
  proof_obligations: decisions.md# D-NNN — Proof obligations (decision-changing subset; claim · V-level · method · owner · funded? — quoted, never re-graded)
  structural_open_choices: the architecture block# open_architecture_choices[] where structural == true
  architecture_shape: the architecture block# A1 authorization and scope + A2 intent + A9 irreversible/exit (2–5 sentences)
  architectability_basis: _synthesis/architecture-story.md# Authorized scope and outcome basis (DURABLE CARRIER of the architecture-entry result)
  decision_economics: _synthesis/financial-story.md# As-is cost baseline, Cost of doing nothing, Budget envelope and funding, Payback / ROI
  investment_summary: _render/<slug>_estimate_v<NN>.md# headline — ONE paragraph, payload bounded by `slot_payload.investment_summary` (base effort · range · contingency-inclusive total · confidence). The Estimate owns the figure and every excluded detail
  risks_and_mitigations: _synthesis/risks-and-assumptions.md# Accepted risks (with mitigations), Watch-list summary
  open_epistemics: _synthesis/risks-and-assumptions.md# Assumptions to validate during build, Unresolved Unknowns (Critical), Conflicts still on the table, Expired validity
  revision_tripwires: decisions.md# D-NNN — Revision conditions / Tripwires (estruturados)
  what_happens_next: decisions.md# D-NNN — Preconditions + Revision conditions + Sponsor confirmation (the next actions, as recorded)
---

# Relatório Executivo — {{solution_name}}

> Documento síntese para o sponsor / C-level. Projecta **a decisão** — o que foi decidido, para que
> âmbitos, sob que condições, com que riscos aceites, e o que forçaria uma revisão. Lê em ~10 minutos.
>
> **Não é um Relatório de Descoberta mais curto** (sem reconstrução do as-is, sem inventário de dados,
> sem passeio por perspectivas) **nem um Blueprint de Arquitectura** (sem tabela de fronteiras, sem
> detalhe de stores, sem canais de importação).
>
> **Sem nova comparação.** Reproduz a justificação que a decisão registou e as linhas de *porque não*
> por alternativa tal como ficaram registadas. Não explica porque é que uma arquitectura "ganhou".

## 1. Business case
{{business_case}}

## 2. A decisão
> A opção escolhida e a solução seleccionada **em linguagem simples**, tal como a decisão a registou.

{{the_decision}}

## 3. Âmbitos e resultados — pares não colapsados
> Uma linha por par `(âmbito, resultado)` emitido, com a frase de resultado **verbatim** e **todos** os
> marcadores preservados (`COMPARATIVE FIT UNEVALUATED`, `INCUMBENT FIT UNEVALUATED`, suficiência
> documentada, gatilho de graduação). **Nunca colapsar dois âmbitos numa linha.**
>
> Para um âmbito `authorized-bounded`: uma frase que nomeia o que **não** está no âmbito desta
> plataforma e a sua categoria de propriedade de âmbito — *arquitectado aqui* · *relocado, fronteira
> representada* · *excluído, destino não avaliado* · *não aplicável, sem autorização de arquitectura*.
> O lado de fora **nunca** entra no âmbito por silêncio.

{{scope_outcome_pairs}}

## 4. Porquê — a justificação registada
{{decision_justification}}

## 5. Alternativas — o *porque não* registado
> As linhas de *porque não* por alternativa **tal como a decisão as registou**. Sem nova comparação,
> sem ranking, sem pontuação. Onde a decisão não registou comparação, esta secção diz isso.

{{alternatives_why_not}}

## 6. Condições e pré-condições
> Cada uma como *condição — dono — financiada? — até quando*, incluindo `not named` onde a origem não
> nomeou. **Nenhuma condição é convertida em «satisfeita»** neste documento: uma condição só passa a
> satisfeita através de evidência do engagement (uma linha `Confirmed` ou uma transição `/answer`).

{{conditions_and_preconditions}}

## 7. Riscos aceites
> Os riscos que a decisão aceitou, com a sua consequência e o `R-NNN`. Um risco aceite **não** é um
> risco mitigado.

{{accepted_risks}}

## 8. Obrigações de prova que qualificam a decisão
> Apenas as obrigações **decision-changing**: a afirmação · porque qualifica a decisão · o dono ·
> financiada?. O nível (V1–V4), o método, o dono e o estado de financiamento são **citados**, nunca
> re-graduados.

{{proof_obligations}}

## 9. Escolhas estruturais em aberto
> Cada entrada `structural: true`: a escolha · o que a resolveria · o `U-NNN`. Uma escolha estrutural
> bloqueia a **aprovação** da arquitectura — e por consequência a Especificação de Implementação e o
> Design Brief. Diz-se; não se resolve aqui.

{{structural_open_choices}}

## 10. Forma da arquitectura
> **Apenas onde existe autorização de arquitectura.** 2–5 frases: o que está autorizado e para que
> âmbito (A1), a intenção arquitectural (A2), e a consequência irreversível ou de saída material (A9).
> A arquitectura é **nomeada, não descrita**.

{{architecture_shape}}

## 11. Porque não existe arquitectura nesta plataforma
> **Apenas onde nenhum âmbito está autorizado.** Duas razões, **distintas**:
> 1. **Base de outcome** — a frase de resultado emitida, verbatim (autoridade: `decisions.md`).
> 2. **Base de arquitectabilidade** — porque este pack não arquitecta a solução seleccionada. A
>    autoridade semântica é a **regra do gate de entrada de arquitectura**; `_synthesis/architecture-story.md`
>    é o **portador durável** desse resultado, não a sua autoridade.
>
> Um resultado positivo sobre uma solução fora do âmbito de arquitectura deste pack **não** é
> `Decision Blocked`, **não** significa que esta plataforma perdeu, e **nada** se infere sobre o
> ajuste, a qualidade ou o custo da solução seleccionada.

{{architectability_basis}}

## 12. Economia da decisão
> Atractividade, envelope orçamental, modelo de financiamento, payback — a **altitude de decisão**
> (S8). Não é a estimativa de implementação: são perguntas diferentes.

{{decision_economics}}

## 13. Investimento previsto
> **Um parágrafo, no máximo**, projectado da Estimativa. Responde a **uma** pergunta: *que
> magnitude de entrega deve o sponsor compreender?*
>
> **Carrega apenas**: esforço base · gama · total com contingência incluída · declaração de
> confiança — e a atribuição à Estimativa.
>
> **Não carrega**: fases · decomposição de trabalho · composição de equipa ou perfis · a **taxa** de
> contingência ou como foi derivada · aritmética de esforço · duração ou calendário (semanas,
> meses, datas) · inventário detalhado de incertezas · inventários de candidatos.
> Este documento recebe **o resultado, não a anatomia do cálculo**; tudo o que fica de fora
> pertence à Estimativa e lê-se lá.
>
> **Arquitectura por resolver (modo B)**: onde existem apenas estimativas de planeamento por
> candidato, **não se combina nada num só valor**. Ou se omite este parágrafo, ou se diz
> qualitativamente que existem estimativas separadas por candidato e referenciam-se — sem ponto
> médio, sem gama combinada, sem «melhor candidato».

{{investment_summary}}

## 14. Riscos e mitigações
{{risks_and_mitigations}}

## 15. Pontos epistémicos abertos que qualificam a decisão
> Apenas os que são **decision-changing**: premissas materiais (`A-NNN`), Unknowns abertos
> (`U-NNN`, como abertos — nunca preenchidos), conflitos não resolvidos (`X-NNN`, o conflito
> renderizado, nenhum lado escolhido) e `Confirmed` expirados (como obrigação de re-verificação).

{{open_epistemics}}

## 16. O que forçaria uma revisão (tripwires)
> Uma linha por `TW-n`: a condição mensurável · a fonte no SU · o contrafactual congelado a comparar.

{{revision_tripwires}}

## 17. O que acontece a seguir
{{what_happens_next}}
