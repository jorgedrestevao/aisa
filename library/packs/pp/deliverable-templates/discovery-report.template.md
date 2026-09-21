---
template_id: discovery-report
canonical_deliverable: discovery-report
output_format: md
audience: sponsor-and-stakeholders
# render --html: this deliverable gets the interrogable HTML projection first (provenance
# tooltips per id + final Proveniência table); others follow in v3.1.

# §8.3 — pré-decisão por construção: não lê versão de desenho nenhuma.
blueprint_version_read: none

# ── PROJECTION CONTRACT ────────────────────────────────────────────────────────────────
# This template DECLARES; it does not execute. `aisa-render` executes only the
# transformations listed in `permitted_transformations`.
# Altitude: detailed discovery state. Phase truth: PRE-DECISION BY CONSTRUCTION, even
# though it renders after /decide.

activation: always

authority_sources:
  - shared-understanding.md                     # facts + epistemic states — ALL FIVE
  - context.json                                # requester, literal request
  - _synthesis/business-story.md
  - _synthesis/as-is.md

conditional_sources:
  - _synthesis/risks-and-assumptions.md         # assumptions / risks / critical unknowns
  - _capture/evidence-index.md                  # sources analysed, where capture ran
  - frame.md                                    # scope framing, where framing happened
  - decisions.md# D-001                         # the framing decision ONLY — never D-NNN outcomes

forbidden_sources:
  - decisions.md# D-NNN (decision, recommendation, architecture)   # post-decision content
  - the architecture block · architecture-templates/*              # no architecture at all
  - options.md                                                     # no option conclusions
  - any Domain Knowledge unit                                      # and no vendor/product naming
  - any CRAFT unit
  - _synthesis/architecture-story.md
  - _synthesis/financial-story.md
  - another deliverable's narrative as authority        # nothing in _render/ is a source here
  - _render/*

permitted_transformations:
  - narrative reconstruction of the as-is from already-recorded rows
  - table<->prose for the data inventory and the epistemic sections
  - materiality selection per `materiality` below, with counted residuals
  - audience language = the engagement language
  - inline id citation
  - HTML provenance projection (--html)

forbidden_transformations:
  - changing an epistemic state (no promotion, no silent expiry)
  - converting an Unknown into a finding, an assumption or a recommendation
  - choosing a side of a Conflicted row
  - rendering an expired Confirmed as fact
  - stating an Options conclusion, a technology recommendation or any vendor/product name
  - mechanically copying every Shared Understanding row
  - reproducing an interview transcript

# ── MATERIALITY (§8.1) ─────────────────────────────────────────────────────────────────
# A row reaches this deliverable if ANY of the seven classes holds. Rows failing all seven
# are OMITTED, not summarized.
materiality:
  survives_if_any:
    - anchors a claim in business-story.md or as-is.md
    - Unknown with criticidade = Critical, OR any Unknown a blocking-set entry needs
    - Conflicted and unresolved
    - Risky
    - Assumed and load-bearing for the problem statement, a volume, a cost baseline or a control
    - Confirmed and EXPIRED (renders as a re-verification obligation, never dropped)
    - a stakeholder concern the council recorded that no other row carries
  omission_rule: |
    Omission is SILENT for Confirmed rows and NEVER silent for Unknown / Conflicted /
    Risky / Assumed: an omitted row of those four states is a COUNTED RESIDUAL
    ("+ N further open items, see shared-understanding.md"), so the reader can see that
    compression happened.

# ── EPISTEMIC PROJECTION (§15) ─────────────────────────────────────────────────────────
epistemic_projection:
  Confirmed: stated as fact, with its id
  Confirmed_expired: re-verification obligation — never fact
  Assumed: assumed, with basis, validity and validator
  Unknown: own section, with criticality and who can answer
  Conflicted: conflict rendered, both sides, NEITHER chosen
  Risky: risk observed, with consequence
  binding_rule: deliverable brevity cannot upgrade epistemics

required_slots:
  - solution_name
  - business_context
  - current_state_summary
  - identified_processes
  - data_inventory
  - pain_points
  - perspectives_and_tensions
  - open_questions_unknown
  - conflicts_unresolved
  - risks_observed
  - assumptions_in_play
  - evidence_still_required

conditional_slots:
  - scope_framing
  - sources_analysed

optional_slots:
  - stakeholders_interviewed

slot_conditions:
  scope_framing: frame.md exists (framing phase happened)
  sources_analysed: _capture/evidence-index.md exists, else inputs/* inventory

slot_sources:
  business_context: _synthesis/business-story.md# Why this engagement exists, Who actually feels the problem
  current_state_summary: _synthesis/as-is.md# End-to-end process today, Volume and cycle time
  identified_processes: _synthesis/as-is.md# End-to-end process today
  data_inventory: shared-understanding.md# lens=data (Confirmed + Assumed, materiality-filtered, each with state + validity)
  pain_points: _synthesis/as-is.md# Top friction points
  perspectives_and_tensions: _synthesis/business-story.md + _synthesis/as-is.md (per-perspective findings and surviving tensions, as recorded)
  open_questions_unknown: shared-understanding.md# Unknown (criticidade + quem responde; residual count for omitted rows)
  conflicts_unresolved: shared-understanding.md# Conflicted (both sides verbatim; residual count for omitted rows)
  risks_observed: shared-understanding.md# Risky (risk + consequence; residual count for omitted rows)
  assumptions_in_play: shared-understanding.md# Assumed (basis + verificado_em + validade + validator) + _synthesis/risks-and-assumptions.md# Assumptions to validate during build
  evidence_still_required: shared-understanding.md# Confirmed (EXPIRED rows as re-verification obligations) + shared-understanding.md# Unknown (open blocking criteria) + _synthesis/risks-and-assumptions.md# Unresolved Unknowns (Critical)
  stakeholders_interviewed: context.json# requester
  sources_analysed: _capture/evidence-index.md (fallback inputs/* — an INVENTORY, never a reinterpretation)
  scope_framing: frame.md# problem statement + decisions.md# D-001
---

# Relatório de Descoberta — {{solution_name}}

> Documento de descoberta para o sponsor e stakeholders. Projecta o estado do conhecimento da
> iniciativa — o que está confirmado, o que é assumido, o que continua aberto, o que está em
> conflito e o que é arriscado — no estado em que o Shared Understanding o registou.
>
> **Neutro em tecnologia por construção.** Não recomenda, não decide, não descreve arquitectura
> e não nomeia fornecedores ou produtos (`.claude/rules/no-tech-mention-before-options.md`).
>
> **Compressão é permitida; promoção epistémica não.** Onde linhas abertas foram omitidas por
> imaterialidade, o número residual é declarado — a compressão é visível, nunca silenciosa.

## 1. Contexto de negócio
{{business_context}}

## 2. Estado actual — resumo
{{current_state_summary}}

## 3. Processos identificados
{{identified_processes}}

## 4. Inventário de dados
> Uma linha por elemento de dados: elemento · onde vive hoje · dono · sensibilidade · id · estado
> (`Confirmed`/`Assumed`) · `verificado_em` / `validade`. Um valor volátil sem selo não é facto.

{{data_inventory}}

## 5. Pontos de fricção identificados
{{pain_points}}

## 6. Perspectivas e tensões
> As conclusões por perspectiva e as tensões que **sobreviveram** — não resolvidas aqui. Uma tensão
> continua tensão; escolher um lado é proibido neste documento.

{{perspectives_and_tensions}}

## 7. Questões abertas (Unknown)
> Uma linha por `U-NNN` material: a pergunta · criticidade · quem pode responder · o que muda se
> resolver. Nenhum `Unknown` é convertido em conclusão, em premissa ou em recomendação.
>
> Termina com o residual: `+ N questões abertas adicionais (ver shared-understanding.md)`.

{{open_questions_unknown}}

## 8. Conflitos não resolvidos (Conflicted)
> Uma entrada por `X-NNN`: ambos os lados, verbatim, com a origem de cada. **Nenhum lado é
> escolhido** — nem com ressalva. Sem conflitos: `nenhum` (um facto, não uma lacuna).
>
> Termina com o residual quando houver omissões.

{{conflicts_unresolved}}

## 9. Riscos observados (Risky)
> Uma linha por `R-NNN`: o risco · a consequência · o que o tornaria observável. A identidade de
> risco preserva-se; um risco observado não é um risco mitigado.
>
> Termina com o residual quando houver omissões.

{{risks_observed}}

## 10. Premissas em jogo (Assumed)
> Uma linha por `A-NNN` load-bearing: a premissa · a base · quem valida · `verificado_em` /
> `validade`. Uma premissa nunca é promovida a facto por brevidade.
>
> Termina com o residual quando houver omissões.

{{assumptions_in_play}}

## 11. Evidência ainda necessária
> Três blocos, nesta ordem:
> 1. **Re-verificação** — cada `Confirmed` cuja validade expirou, como obrigação de re-verificação
>    com a pergunta reformulada. Nunca renderizado como facto.
> 2. **Critérios de bloqueio abertos** — as perguntas que impedem uma conclusão, com dono e forma
>    esperada da resposta.
> 3. **Plano de evidência** — o que resolver primeiro e porquê.

{{evidence_still_required}}

## 12. Stakeholders
{{stakeholders_interviewed}}

## 13. Fontes analisadas
> **Inventário** dos artefactos analisados (entrada: `_capture/evidence-index.md`). É uma lista de
> fontes, não uma reinterpretação de evidência.

{{sources_analysed}}

## 14. Enquadramento de âmbito
> O enquadramento registado em `frame.md` / `D-001`. Enquadramento não é decisão: não há aqui opção
> escolhida, recomendação nem arquitectura.

{{scope_framing}}
