---
template_id: solution-blueprint
canonical_deliverable: architecture-blueprint
# ^ id / file / CLI argument stay `solution-blueprint` (runtime alias, Step 6A §4).
#   The canonical deliverable name is Architecture Blueprint.
output_format: md
audience: technical

# ── PROJECTION CONTRACT ────────────────────────────────────────────────────────────────
# This template DECLARES; it does not execute. `aisa-render` executes only the
# transformations listed in `permitted_transformations`.
# Altitude: ARCHITECTURE. Nature: the human-readable projection of the FROZEN Step 5
# Architecture Layer. This is the ONE deliverable that does not compress the architecture.

activation: an architecture authorization exists for at least one scope
not_applicable_when: authorization == not-authorized for every scope
# ── BLUEPRINT VERSION THIS DELIVERABLE READS (P-18 / F08) ─────────────────────────────
# `v<latest authorized>` — the latest non-draft `_blueprint/ux-blueprint_v<NN>.yaml` whose
# `architecture.authorization` is `authorized` or `authorized-bounded` for at least one scope.
# NOT necessarily the approved one. Reason: the candidate-architectures section exists
# precisely while a structural choice is open, and a structural choice blocks APPROVAL
# (blueprint-contract.md hard rule 5) — a source of `v<approved>` could never show what
# this deliverable must show. Authorization (a recorded architecture fact) and approval
# (a human D-NNN) are distinct; this deliverable reads the first and DECLARES the second
# in `architecture_version_state`. The Implementation Specification and the Claude
# Design Brief keep `v<approved>` — what gets built is what the business validated.
blueprint_version_read: v<latest authorized>   # declared, never inferred from the newest file
# => deliverable-level SKIP, logged to render-log.md with the reason. NOT a gap.
# No empty architecture deliverable, no placeholder A-sections, no "architecture: none" document.

authority_sources:
  - the architecture block                                   # PRIMARY — the record
  - architecture-templates/architecture-core.md              # the FIXED shape (A1–A12)
  - the resolved fragments                                   # 0..1 experience · N+M boundary
  - _synthesis/architecture-story.md                         # narrative

conditional_sources:
  - decisions.md# D-NNN                                      # basis · conditions · proof obligations · tripwires
  - shared-understanding.md                                  # validity / state display, volatile stamps

forbidden_sources:
  - raw evidence for re-reasoning                            # anything already settled upstream
  - inputs/* · _capture/*
  - "preloaded Domain Knowledge — the architecture layer already pulled selectively;
     this deliverable CITES, it does not re-pull"
  - _synthesis/financial-story.md                            # no effort and no cost figure here
  - _render/<slug>_estimate_v<NN>.md                         # the Estimate is a different altitude
  - another deliverable's narrative as authority
  - options.md                                               # Options is closed

permitted_transformations:
  - A-section order and headings
  - tables and (degradable) diagrams per the core's own conditionals
  - architect-facing precision
  - weaving the architecture-story narrative paragraphs around the structured sections
  - projecting the four scope-ownership RENDER CATEGORIES from the (scope, outcome) pairs
    x the architecture block
  - blueprint version read -> one version-state line (approved D-NNN | not approved —
    N structural choice(s) open | not approved — awaiting business approval), from
    `_blueprint/` file names x `decisions.md` blueprint approvals x the record's
    open_architecture_choices[] — READ, never judged

forbidden_transformations:
  - choosing architecture authorization · experience mode · store / record authority ·
    pattern · composition · far-side solution        # all six belong to the frozen layer
  - scoring any architecture
  - selecting among candidate architectures
  - designing the far side of any boundary
  - re-deriving authorization, record authority, composition, scope relocation or pattern
  - carrying an executive summary                    # -> Executive Report
  - carrying an effort or estimate figure            # -> Estimate
  - staging an architecture-level alternatives comparison   # -> Executive Report, decision altitude
  - re-grading a proof obligation (V1–V4), method, owner or funded state
  - promoting an epistemic state · rendering an expired or unstamped volatile value as fact
  - inventing a fifth scope-ownership category, or turning a category into a state

# ── ARCHITECTURE INCLUDE — FIXED (§26, Step 5 frozen) ─────────────────────────────────
# ONE entry point. No branch, no per-decision template lookup, no router, no dynamic path.
sub_templates:
  - architecture-templates/architecture-core.md
# The core itself resolves ZERO or ONE experience fragment (from architecture.experience.mode;
# `none` resolves to NO include) and ZERO or MORE boundary-fragment instances (one per
# qualifying component). `aisa-render` performs that iteration; the N+M invariant is its rule.

# ── SCOPE-OWNERSHIP PROJECTION CATEGORIES (I-3, §12) ──────────────────────────────────
# FOUR render/projection categories. NOT states. NOT outcome classes. NOT epistemic values.
# Rendered where more than one (scope, outcome) pair exists. One row per responsibility.
# No category may be inferred from another.
scope_ownership_categories:
  1:
    name: architected here
    rendered_as: "sim — A4…A12"
    engaged_when: the scope carries authorized or authorized-bounded AND the responsibility
      is PP-owned
    architecture_consequence: full A-sections
  2:
    name: relocated — boundary represented
    rendered_as: "não — uma instância do fragmento de fronteira"
    engaged_when: a relocated_responsibilities[] entry whose owner is IDENTIFIED — a role, team or
      organisation on the far side, never a person (class 3 / class 4)
    architecture_consequence: one boundary fragment instance, six channels; NO far-side design;
      markers verbatim
  3:
    name: excluded — destination unevaluated
    rendered_as: "não — sem arquitectura e sem fragmento de fronteira; destino/contraparte
      não selecionado"
    engaged_when: class 6 (or 5 / 7 / 14) followed by class 8, where the destination is an
      emitted CANDIDATE SET
    architecture_consequence: NOTHING — no design, no boundary component, no owner, no imports,
      no gates, no inferred fit. `COMPARATIVE FIT UNEVALUATED` verbatim
  4:
    name: not applicable — no architecture authorization
    rendered_as: "não aplicável — sem autorização de arquitectura"
    engaged_when: authorization == not-authorized for every scope
    architecture_consequence: no architecture at all; the outcome basis + architectability
      basis carry the meaning

# ── EPISTEMIC PROJECTION (§15) ────────────────────────────────────────────────────────
epistemic_projection:
  Confirmed: fact + verificado_em / validade
  Confirmed_expired: re-verification obligation (A12)
  Assumed: assumed, NEVER promoted (A12)
  Unknown: an open_architecture_choices[] entry — never filled
  Conflicted: conflict rendered, NEITHER figure carried
  Risky: accepted-risk id (A12)

# ── PROOF-OBLIGATION CARRIAGE (§16) ───────────────────────────────────────────────────
proof_obligation_carriage:
  scope: ALL architecture proof obligations
  form: claim · level (V1–V4) · method · owner · funded?
  rule: quoted from the record; never re-graded, never marked satisfied, never re-methoded

required_slots:
  - solution_name
  - architecture_block
  - architecture_version_state
  - orientation

conditional_slots:
  - architecture_narrative
  - decision_basis
  - scope_ownership_projection
  - candidate_architectures_note
  - epistemic_and_validity_display

slot_conditions:
  architecture_narrative: _synthesis/architecture-story.md exists
  decision_basis: decisions.md# D-NNN exists
  scope_ownership_projection: more than one (scope, outcome) pair exists
  candidate_architectures_note: open_architecture_choices[] contains a structural:true entry
    leaving two materially distinct architectures defensible inside one authorized scope
  epistemic_and_validity_display: the architecture rests on at least one Assumed / Unknown /
    Conflicted / Risky row, or carries at least one volatile value

slot_sources:
  architecture_block: _blueprint/ux-blueprint_v<latest authorized>.yaml# architecture (P-18 / F08 — the latest non-draft version with an architecture authorization for at least one scope; NOT `v<approved>`, which cannot exist while a structural choice keeps the candidate-architectures section engaged)
  architecture_version_state: computed — the version read (`v<NN>`) + its approval state, READ from decisions.md# Blueprint bp-v<NN> aprovado and the record's open_architecture_choices[] — `aprovada (D-NNN)` | `não aprovada — N escolha(s) estrutural(is) em aberto` | `não aprovada — aguarda aprovação do negócio`. Never `approved` by inference; never a partial or UX-only state
  orientation: _synthesis/architecture-story.md# Chosen architecture (TWO SENTENCES MAX — an
    orientation paragraph, never an executive summary)
  architecture_narrative: _synthesis/architecture-story.md# Composition, components and boundaries, Imported obligations, Data, Integrations, Security model, Watch-list constraints
  decision_basis: decisions.md# D-NNN — (Scope, outcome) pairs — UNCOLLAPSED + Conditions + Preconditions + Proof obligations + Revision conditions / Tripwires
  scope_ownership_projection: decisions.md# D-NNN — (Scope, outcome) pairs — UNCOLLAPSED x the architecture block# relocated_responsibilities[] + compositions[] (projected into the four categories above)
  candidate_architectures_note: the architecture block# open_architecture_choices[] where structural == true
  epistemic_and_validity_display: shared-understanding.md# rows referenced by the architecture block (state + verificado_em + validade) + the architecture block# proof_obligations[] + open_architecture_choices[]
---

# Architecture Blueprint — {{solution_name}}

> A projecção legível da **camada de arquitectura registada**. Audience: solution architect / lead
> developer / tech lead.
>
> **Projecta; não decide.** Autorização, modo de experiência, autoridade de registo, composição,
> relocação de âmbito e padrão são **lidos** do registo — nunca derivados, escolhidos, pontuados,
> promovidos ou rebaixados aqui. Nenhuma arquitectura candidata é selecionada. Nenhum lado externo
> de uma fronteira é desenhado.
>
> **Altitudes que este documento não carrega**: sumário executivo (→ Relatório Executivo), esforço
> ou estimativa (→ Estimativa), comparação de alternativas (→ Relatório Executivo, altitude de
> decisão). O parágrafo de orientação abaixo tem duas frases e não é um sumário executivo.

## Orientação
{{orientation}}

## Base de decisão
> Os pares `(âmbito, resultado)` **não colapsados**, verbatim e com todos os marcadores; as condições,
> pré-condições e obrigações de prova que a decisão registou; os tripwires. Base — não re-decisão.

{{decision_basis}}

## Arquitectura

> **Versão do desenho lida e o seu estado.** Este documento projecta a versão **autorizada** mais
> recente do registo e declara se o negócio já a aprovou — a aprovação é lida de `decisions.md`,
> nunca inferida. Uma versão não aprovada por escolha estrutural em aberto renderiza-se aqui com
> as candidatas e nenhuma escolhida; a Especificação de Implementação e o Claude Design Brief
> continuam a exigir a versão **aprovada**.

{{architecture_version_state}}

<!--
FIXED INCLUDE. One entry point: architecture-core.md. It carries A1–A12 and its own conditionals,
resolves ZERO or ONE experience fragment from `architecture.experience.mode` (`none` => NO include,
A4 renders `not applicable` with its reason, and that is a FINALIZED architectural fact — not a gap),
and receives ZERO or MORE boundary-fragment instances (exactly N unique qualifying composition
components + M unique relocated responsibilities), each with all six channels.
Every engaged A-section is populated from the record; every non-engaged one carries
`not applicable — <reason>`.
-->

{{>> architecture-templates/architecture-core.md}}

## Narrativa de arquitectura
> Os parágrafos narrativos da história de arquitectura, tecidos em torno das secções estruturadas
> acima. Narrativa — não autoridade: onde a narrativa e o registo divergirem, o registo ganha.

{{architecture_narrative}}

## Propriedade de âmbitos — categorias de projecção
> **Quatro categorias de projecção** (não estados, não classes de resultado, não valores epistémicos).
> Uma linha por responsabilidade. Nenhuma categoria é inferida de outra.
>
> | # | Categoria | Renderizada como | Consequência arquitectural |
> |---:|---|---|---|
> | 1 | arquitectado aqui | `sim — A4…A12` | secções A completas |
> | 2 | relocado — fronteira representada | `não — uma instância do fragmento de fronteira` | uma instância, seis canais; **sem desenho do lado de fora** |
> | 3 | excluído — destino não avaliado | `não — sem arquitectura e sem fragmento de fronteira; destino/contraparte não selecionado` | **nada**: sem desenho, sem componente de fronteira, sem owner, sem imports, sem gates, sem ajuste inferido |
> | 4 | não aplicável — sem autorização de arquitectura | `não aplicável — sem autorização de arquitectura` | sem arquitectura; a base de outcome + a base de arquitectabilidade carregam o significado |
>
> Linhas de **categoria 3** carregam a frase de resultado emitida e o conjunto de candidatos tal como
> emitido — `COMPARATIVE FIT UNEVALUATED` verbatim — e **nenhum valor de owner** além disso.

{{scope_ownership_projection}}

## Arquitecturas candidatas
> **Apenas onde uma escolha estrutural em aberto deixa duas arquitecturas materialmente distintas
> defensáveis dentro de um âmbito autorizado.** Renderiza **ambas**, declara o que resolveria a
> escolha, e **escolhe nenhuma**. Sem pontuação, sem ranking, sem recomendação.
>
> Consequência mecânica (regra congelada, sem maquinaria nova): uma entrada `structural: true`
> bloqueia a **aprovação** do blueprint — nunca a sua **produção**. Por consequência, a Especificação
> de Implementação e o Claude Design Brief ficam **bloqueados**. Sem override por materialidade, sem
> aprovação parcial, sem aprovação só-de-UX.

{{candidate_architectures_note}}

## Livro epistémico e validade
> As linhas `Assumed` / `Unknown` / `Conflicted` / `Risky` em que esta arquitectura assenta, com os
> seus ids e estados; cada valor volátil com `verificado_em` e `validade`; cada obrigação de prova na
> forma de cinco partes (*afirmação · nível V1–V4 · método · dono · financiada?*), **citada e nunca
> re-graduada**; cada `open_architecture_choices[]` com a marca `structural?`.
>
> **Itens em aberto não tornam este documento incompleto — tornam-no honesto.**

{{epistemic_and_validity_display}}
