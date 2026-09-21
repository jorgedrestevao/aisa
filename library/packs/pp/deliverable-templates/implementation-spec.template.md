---
template_id: implementation-spec
canonical_deliverable: implementation-specification
output_format: md
audience: developer

# §8.3 — a APROVADA, e só ela: o que se constrói é o que o negócio validou. Uma
# escolha `structural: true` em aberto bloqueia a aprovação e portanto este
# deliverable (blueprint-contract.md hard rule 5); ler a autorizada em vez dela
# seria construir sobre uma versão que ninguém validou.
blueprint_version_read: v<approved>

# ── PROJECTION CONTRACT ────────────────────────────────────────────────────────────────
# This template DECLARES; it does not execute. `aisa-render` executes only the
# transformations listed in `permitted_transformations`.
# Altitude: BUILD. Nature: ARCHITECTURE -> BUILD OBLIGATIONS AND IMPLEMENTATION CONTRACTS.

activation: an architecture authorization exists for at least one scope AND the blueprint
  is approved
blocked_when: open_architecture_choices[] contains a structural:true entry
# structural:true -> blueprint APPROVAL blocked (blueprint-contract.md hard rule 5)
# -> this deliverable's primary authority (the APPROVED architecture) does not exist
# -> BLOCKED. Mechanical consequence of frozen rules; no new machinery, no override.
not_applicable_when: authorization == not-authorized for the scope
# Produced for any OTHER scope that does carry a PP authorization. With no such scope:
# not produced — a deliverable-level SKIP logged to render-log.md. NOT a gap.

authority_sources:
  - "the architecture block — PRIMARY: record_authority, compositions,
     relocated_responsibilities, proof_obligations, open_architecture_choices"
  - architecture-templates/architecture-core.md  # the FIXED shape — A5–A10 projection targets
  - the resolved fragments                       # 0..1 experience · N+M boundary
  - decisions.md# D-NNN                          # conditions · preconditions · proof obligations

conditional_sources:
  - _blueprint/ux-blueprint_v<approved>.yaml     # screens / entities / entities[].state_machine ·
                                                 # entities[].approval — ONLY where experience.mode != none
  - the architecture block# A9 replacement conditional + the class-14 outcome sentence   # migration & cutover
  - selective RESEARCH units                     # implementation-grade detail, at the POINT OF NEED
  - selective CRAFT units                        # delivery conventions, artefact FORM
  - _synthesis/architecture-story.md             # narrative glue only
  - "_synthesis/as-is.md# Passos e tempo — ONLY as the source of the operating-path change table
     (P-10): passo · quem · tempo actual come from there; novo processo · tempo novo come from THIS
     deliverable's inventory (the screen / flow / contract that replaces the step, and A5 volume ×
     cadence). Never a work unit, never acceptance work, never a proof level"

forbidden_sources:
  - raw shared-understanding.md rows as the source of a migration plan
  - _synthesis/as-is.md as the source of acceptance work        # scenarios only, NEVER proof level
  - _synthesis/financial-story.md as the source of sequencing
  - _render/<slug>_estimate_v<NN>.md                            # the Estimate reads THIS, not the reverse
  - options.md                                                  # Options is closed
  - the whole Domain Knowledge catalogue                        # no preload, no catalogue scan
  - "inputs/* · _capture/* to re-settle an upstream fact — ONE declared exception (P-6): the `source`
     locator a fields[] / reads[] / writes[] line carries into _capture/<workbook>.fields-draft.json is CITED
     as provenance (transformation `L1 column inventory -> fields[] draft (Assumed)`, executed UPSTREAM by
     aisa-blueprint via fields_draft.py); this deliverable never re-reads the draft to add, drop or
     re-type a line"

permitted_transformations:
  # Each is DETERMINISTIC, BOUNDED, DECLARED HERE, and TRACEABLE to an authoritative input.
  - architecture obligation      -> build / configuration obligation
  - proof obligation             -> ONE work package + ONE acceptance condition
  - architecture dependency      -> sequencing constraint (NO durations)
  - A9 replacement + class-14 outcome + access_mode transition -> migration & cutover steps
  - approved UX blueprint screen -> screen/component build block
  - per-section shape contracts (one row per entity, one block per flow, …)
  - "as-is step (passo · quem · tempo actual, from _synthesis/as-is.md# Passos e tempo) x the inventory item
     that replaces it -> one operating-path change row (passo · quem · tempo actual · novo processo · tempo
     novo · Δ); `tempo novo` only where the inventory item carries a basis (A5 volume × cadence, a flow's
     schedule) — otherwise `not derivable` with the reason; a step nothing replaces renders `inalterado`"
  - "record_authority[].fields[] | access_contract -> §4 rows, one per APPROVED-blueprint entity joined by
     entities[].authority = record_authority[].key (P-6): owned -> campos (nome · tipo · obrigatório · default);
     externo -> lidas (n) · escritas (n) · chave; the counts n campos · n lidas · n escritas · grão · volume are
     WRITTEN in the row (the Estimate cites them as its driver); an entity whose authority does not resolve
     -> a ⚠️ lacuna row + a render-gaps.md entry, NEVER a value by analogy with a neighbouring entity"
  - entity state_machine / approval step -> state-transition obligation
    (who transitions · what validates · what notifies whom · what triggers the cycle)
  - operational and imperative language

forbidden_transformations:
  - selecting or changing record authority / store            # A5 is READ-ONLY here
  - selecting or changing a composition or a pattern          # A3 / A6 are READ-ONLY here
  - changing the experience mode                              # A4 is READ-ONLY here
  - changing architecture authorization or scope
  - reopening Options · re-deciding anything the decision settled
  - fabricating implementation detail for an UNRESOLVED architecture choice
    # -> renders as an OPEN WORK ITEM with its owner and what would settle it
  - re-grading a proof obligation (V1–V4), its method, its owner or its funded state
  - marking a proof obligation satisfied
  - promoting an epistemic state · choosing a side of a Conflicted value
  - specifying an external implementation for a destination that is UNEVALUATED
    # class 6 -> class 8: no interface, no contract, no migration, no cutover to an
    # unnamed counterparty. Where the PP side must eventually exchange with it, that is an
    # OPEN WORK ITEM naming the unselected destination.
  - "dropping, compressing away or re-labelling a build-gating condition or a precondition
     — §17.1 non-negotiable. Filing one under `open work items` is NOT carriage: a condition
     with an owner, a funding state and a due date is not an open work item, and the two
     identities are never collapsed"
  - rendering a build gate as satisfied without recorded engagement evidence
  - inventing a user surface where experience.mode == none
  - "inventing the actor, the validation rule, the notification recipient or the trigger of a
     state transition. A transition whose actor A7 does not name renders as `not named` PLUS an
     open work item; §6 never fills it by analogy with another entity, another role or another
     engagement"
  - "rendering §6 as `(none)` while an entity of the APPROVED blueprint carries a state machine
     or an approval step — the absence of an asynchronous stream in A6 is not the absence of a
     transition to specify"
  - pixel-level detail no downstream consumer uses

# ── ARCHITECTURE INCLUDE — FIXED ──────────────────────────────────────────────────────
architecture_projection: |
  The architecture reaches this deliverable as a PROJECTION of the recorded block and the
  FIXED shape (architecture-templates/architecture-core.md + resolved fragments). There is
  no branch, no per-decision template lookup, no dynamic path and no router. Architecture
  is READ-ONLY here: this deliverable states what must be BUILT to satisfy it.

# ── DERIVATION RULES (§11.1 — replacing D-7, D-8, D-9, D-12) ──────────────────────────
derivation_rules:
  architecture_constraints:
    authority: the architecture block + architecture-core.md sections — PROJECTED, not re-derived
  entities_and_data_structures:
    authority: the architecture block# record_authority[] (fields[] | access_contract per domain, P-6) + the approved blueprint# entities (joined by entities[].authority = record_authority[].key)
    gap_form: an entity without a resolvable authority renders a ⚠️ lacuna row and a render-gaps.md entry; the neighbouring domain is never borrowed
  screens_and_components:
    authority: the approved blueprint# screens
    condition: experience.mode != none
  flows_and_integrations:
    authority: the architecture block# A6 streams + the boundary fragments
  security_implementation:
    authority: A7 identity / enforcement point / role model
    craft_use: CRAFT shapes the FORM of the matrix only — never a control's existence or reach
  test_and_proof_work:
    authority: the architecture block# proof_obligations[] (claim · V-level · method · owner · funded?)
    derivation: ONE work package + ONE acceptance condition per obligation
    scenarios_may_come_from: _synthesis/as-is.md friction — as SCENARIOS ONLY, never the proof level
  sequencing:
    authority: architecture dependencies only — A3 boundaries · A8 release routes ·
      A9 fixed-at points · the fragment cross-boundary release owner
    form: CONSTRAINTS ONLY, no durations
    forbidden_authority: _synthesis/financial-story.md
  migration_and_cutover:
    authority: A9 replacement-of-an-existing-artefact conditional + the class-14 outcome
      sentence + record_authority[].access_mode transitions
    condition: the authorized scope replaces an artefact that reached the migration-required outcome
    forbidden_authority: raw shared-understanding.md Risky rows
    boundary: |
      The Architecture Blueprint owns WHAT is replaced, coexistence, the transition architecture
      and architectural cutover dependencies. THIS deliverable owns migration steps, conversion,
      detailed cutover, sequencing and tasks, cleanup and the rollback procedure.
      No separate migration deliverable exists.
  operating_path_change:
    authority: _synthesis/as-is.md# Passos e tempo (passo · quem · tempo actual) x THIS deliverable's inventory (novo processo · tempo novo)
    condition: the as-is carries at least one named step with a recorded time or an Unknown for it, AND the inventory replaces at least one step
    form: passo · quem · tempo actual · novo processo · tempo novo · Δ — a delta over work this deliverable specifies, never a cost claim, never a reconstructed baseline
    consumer: the Estimate's operational_impact reads THIS section (mode A) and nothing upstream of it
  open_implementation_questions:
    authority: open_architecture_choices[] (NON-structural) + implementation-local unknowns

# ── HEADLESS BEHAVIOUR (§16) ──────────────────────────────────────────────────────────
headless_behaviour: |
  experience.mode == none:
    NO required screens · NO persona section · NO navigation · NO UX placeholder ·
    NO "surface unresolved" note · NO gap.
  STILL PROJECTED IN FULL: automation · integration · identity and enforcement ·
    environments and release · monitoring · recovery · proof work · operator obligations.
  A6 and A7 typically carry the whole architecture. No fake application surface.

# ── SCOPE PAIRS (§19) ─────────────────────────────────────────────────────────────────
scope_rule: |
  Build scope = the PP-OWNED side only, stated as such. Where a boundary component exists
  (category 2) the far side appears as an INTERFACE / CONTRACT OBLIGATION and nothing more.
  Where the destination is UNEVALUATED (category 3) the far side appears as NOTHING.
  The far side never enters PP implementation scope by silence.

# ── SELECTIVE DOMAIN KNOWLEDGE AND CRAFT (§29) ────────────────────────────────────────
selective_pulls:
  point_of_need: true
  rule: |
    ONE unit per obligation, opened at the POINT OF NEED, for implementation-grade detail the
    architecture correctly left at architecture altitude (a mechanism's configuration surface,
    an access path's implementation consequence, a control's implementation form) or for a
    delivery convention. NEVER a preload, NEVER a bundle, NEVER a catalogue scan, NEVER to
    make prose richer. Prefer the upstream derived fact: if the architecture already stated
    the consequence, PROJECT it.
  citation: cite the owning unit inline; do not copy it
  craft_boundary: CRAFT shapes artefact FORM; it never asserts a platform limit or overrides
    architecture. Where a limit is needed, the owning RESEARCH unit is cited.

# ── EPISTEMIC PROJECTION (§15) ────────────────────────────────────────────────────────
epistemic_projection:
  Confirmed: fact
  Confirmed_expired: re-verification obligation + an open work item
  Assumed: assumed + validation work — never promoted
  Unknown: OPEN WORK ITEM; no fabricated detail
  Conflicted: NO value chosen; a proof obligation instead
  Risky: risk + mitigation obligation, accepted-risk identity preserved

# ── PROOF-OBLIGATION CARRIAGE (§16) ───────────────────────────────────────────────────
proof_obligation_carriage:
  scope: ALL, translated
  form: one work package + one acceptance condition per obligation
  preserved_verbatim: claim · level (V1–V4) · method · owner · funded?
  rule: no re-grading, no method substitution, no satisfaction marking

# ── NON-OMISSIBLE CONTENT (§17.1) ───────────────────────────────────────
# Each is `required SUBJECT TO EXISTENCE`: absent upstream => not-applicable skip;
# present upstream => it RENDERS. Compression may NEVER drop one.
# Step 6A §17.1, second non-negotiable: A CONDITION REQUIRED TO BUILD NEVER DISAPPEARS
# FROM THE IMPLEMENTATION SPECIFICATION.
non_omissible:
  - build_gating_conditions      # decisions.md# Conditions — any condition that must hold
                                 # BEFORE build starts, or that gates a build activity
  - preconditions                # decisions.md# Preconditions, in full
  - proof_obligations            # ALL, translated to work package + acceptance condition
  - open_work_items              # each with its owner and what would settle it

# ── BUILD GATES — the dedicated carriage path (§17, §17.1, §17.2) ──────────────────
# A condition with an owner, a funding state and a due date is NOT an open work item.
# It has its own carriage path and its own section; `open_work_items` may not absorb it.
build_gates:
  source:
    - decisions.md# D-NNN — Conditions
    - decisions.md# D-NNN — Preconditions
  include_if:
    - the condition gates build (it must hold before build starts, or before a named
      build activity may proceed)
    - the precondition gates implementation or release
  preserved_per_gate:
    - condition text            # as recorded, never re-worded into a weaker claim
    - owner                     # `not named` included, never invented
    - funded                    # `not named` included, never inferred
    - by_when                   # the recorded due date, where one exists
    - gates                     # WHICH activity it gates (build start, a release route, …)
    - status                    # ONLY where engagement evidence explicitly records it
  identities_preserved: |
    conditions, preconditions and open work items are THREE DISTINCT THINGS. They may render
    in one concise `Build gates` section, but none is collapsed into another and none is
    re-labelled as another.
  satisfaction_rule: |
    NO template may convert `must be validated before build` into `validated`. A gate becomes
    satisfied ONLY through engagement evidence — a Confirmed SU row or an /answer transition
    that says so. Absent that, it renders as an unsatisfied gate with its owner and funding
    state. Projection never satisfies a gate.
  applicability: |
    Where no condition and no precondition gates build, the section is `not applicable` under
    the existing render-gap convention — omitted with its reason, logged as a skip, never a
    gap, and never padded with ceremony.

required_slots:
  - solution_name
  - architecture_constraints
  - entities_to_create
  - flows_to_implement
  - security_implementation
  - integrations
  - environment_and_release
  - monitoring_and_recovery
  - proof_work_packages
  - sequencing
  - build_scope_statement
  - open_work_items

conditional_slots:
  - build_gates
  - screens_to_build
  - migration_and_cutover
  - operator_obligations
  - analytical_responsibility
  - operating_path_change

# ── SUFFICIENCY (P-7) — deterministic rules render-validate.py checks BY CONTENT ─────────
# A rule that fails is a `required` gap in render-gaps.md (owner: architecture), never a slot
# filled by analogy. Presence of a section is not sufficiency.
sufficiency:
  entities_to_create:
    - "every entity of the approved blueprint resolves entities[].authority to a record_authority[].key, or the section carries its ⚠️ lacuna row"
    - "owned domain: fields[] has >= 1 line with type != unknown; fields ⊇ the primary/secondary columns the approved screens reference for that entity; >= 1 line with index primary"
    - "external domain: reads[] non-empty; writes[] non-empty or readonly true; key[] non-empty or open U-nnn; schema_owner present with a state"
    - "every fields[] / reads[] / writes[] line carries state and source; a Confirmed line's locator exists"
  flows_to_implement:
    - "(none) is legitimate only where A6 carries no stream AND no approved entity carries state_machine or approval true"
  security_implementation:
    - "a Papel × (Ecrã | Entidade) table exists in the body; a citation of the craft unit does not count"
  integrations:
    - "per integration, the authentication mechanism and the secret custody are present, or a named gap (store_facts.connection_identity Unknown renders as the named gap)"
slot_conditions:
  flows_to_implement: "REQUIRED. `(none)` is legitimate ONLY where A6 carries no stream AND no
    entity of the APPROVED blueprint carries a `state_machine` or `approval: true`. Where
    experience.mode != none AND at least one such entity exists, §6 carries, PER ENTITY, the
    state-transition block — who transitions · what validates the transition · what notifies whom ·
    what triggers the cycle — even with NO asynchronous stream in A6. A transition an operator
    performs by hand is still this section's scope: without an actor, a validation rule, a
    notification and a trigger it is not buildable. Where A7 and decisions.md name none of them,
    THAT is what renders — `not named` plus an open work item, never an invented one."
  build_gates: "decisions.md# Conditions or decisions.md# Preconditions carries at least one
    entry that gates build start, a build activity, implementation or release. REQUIRED
    SUBJECT TO EXISTENCE — present upstream means it renders; it is never compressed away."
  screens_to_build: experience.mode != none AND an approved UX blueprint exists
  migration_and_cutover: the A9 replacement conditional is engaged OR the class-14 outcome applies
  operator_obligations: A10 names an operator (an UNKNOWN operator is a STRUCTURAL open choice,
    not a work item here)
  analytical_responsibility: the A5 analytical/reporting conditional is engaged
  operating_path_change: "_synthesis/as-is.md# Passos e tempo carries at least one named step (with a
    recorded time or an Unknown for it) AND this deliverable's inventory replaces at least one of those
    steps. Otherwise not applicable — a skip, never a gap. Where engaged, EVERY step of the as-is table
    appears: replaced (with novo processo · tempo novo · Δ, or `tempo novo: not derivable — <reason>`)
    or `inalterado`. A step with `tempo actual: Unknown (U-nnn)` keeps its Unknown in the row."

slot_sources:
  build_gates: decisions.md# D-NNN — Conditions + Preconditions (each as condition — owner — funded? — by when — what it gates — status only where recorded; `not named` included; NEVER rendered as satisfied)
  architecture_constraints: the architecture block + architecture-templates/architecture-core.md# A1, A2, A3, A5, A6, A7, A8, A9 (PROJECTED, not re-derived)
  entities_to_create: the architecture block# record_authority[] — each domain's fields[] (owned) | access_contract (keep-in-place · virtualized · replicated) with every line's state and source — joined to _blueprint/ux-blueprint_v<approved>.yaml# entities by entities[].authority = record_authority[].key (P-6). One row per entity; counts n campos · n lidas · n escritas · grão · volume written in the row; unresolved authority -> ⚠️ lacuna row + render-gaps.md entry
  screens_to_build: _blueprint/ux-blueprint_v<approved>.yaml# screens (the APPROVED version — the sole authority; no narrative fallback)
  flows_to_implement: the architecture block# A6 streams + the resolved boundary fragments +
    _blueprint/ux-blueprint_v<approved>.yaml# entities[].state_machine · entities[].approval (the
    transition SET is READ from the approved blueprint, never chosen here; the actor, the validation
    rule, the notification recipient and the trigger are PROJECTED from
    architecture-templates/architecture-core.md# A7 role and permission model + decisions.md# D-NNN,
    and render as `not named` with an open work item where those name none)
  security_implementation: architecture-templates/architecture-core.md# A7 (identity class, enforcement plane, trust boundary, role and permission model)
  integrations: the architecture block# A6 + compositions[] + the resolved boundary fragments
  environment_and_release: architecture-templates/architecture-core.md# A8 (environments, residency binding, policy plane, release routes)
  monitoring_and_recovery: architecture-templates/architecture-core.md# A10 (detection mechanism, alert destination, recovery procedure and its order, and — where data is replicated or copied — the reconciling role and the mechanism it reconciles through) + the boundary fragments# Monitorização, Recuperação. A role with `not named` against it is complete; no slot here waits on a person
  operator_obligations: architecture-templates/architecture-core.md# A10 (the role authorised to intervene, the identity and permission it intervenes with, the support route) + the boundary fragments# Operador
  analytical_responsibility: architecture-templates/architecture-core.md# A5 conditional — responsabilidade analítica / reporting
  proof_work_packages: the architecture block# proof_obligations[] + decisions.md# D-NNN — Proof obligations
  sequencing: the architecture block# A3 boundaries + A8 release routes + A9 fixed-at points + the boundary fragments# ALM (cross-boundary release owner) — DEPENDENCIES ONLY
  migration_and_cutover: architecture-templates/architecture-core.md# A9 conditional — substituição de um artefacto existente + decisions.md# D-NNN — (Scope, outcome) pairs (the class-14 outcome sentence) + the architecture block# record_authority[].access_mode transitions
  build_scope_statement: decisions.md# D-NNN — (Scope, outcome) pairs — UNCOLLAPSED (the PP-owned side, stated as such) + the scope-ownership projection categories
  open_work_items: the architecture block# open_architecture_choices[] (non-structural) + decisions.md# D-NNN — Conditions, Preconditions + implementation-local unknowns
  operating_path_change: _synthesis/as-is.md# Passos e tempo (passo · quem · tempo actual — the ONLY thing read there) x this deliverable's own inventory (§4 A5 volume × cadence · §5 screens · §6 flows · §7 contracts — the novo processo and its tempo novo, where a basis exists) -> passo · quem · tempo actual · novo processo · tempo novo · Δ (P-10)
---

# Implementation Specification — {{solution_name}}

> Especificação de construção accionável. Audience: equipa de implementação.
>
> **Arquitectura → obrigações de construção.** A arquitectura registada é **lida**: esta especificação
> não escolhe store, não escolhe composição nem padrão, não altera o modo de experiência, não reabre
> Options e não inventa detalhe de implementação para uma escolha arquitectural **não resolvida** —
> essa renderiza-se como *open work item* com dono e com o que a resolveria.
>
> **Completa para handoff**, não *completamente especificada*: itens em aberto explícitos são
> compatíveis com completude.

## 1. Âmbito de construção
> O lado **PP-owned** apenas, declarado como tal. Onde existe componente de fronteira, o lado de fora
> aparece como **obrigação de interface/contrato** e nada mais. Onde o destino está **não avaliado**,
> o lado de fora aparece como **nada** — sem interface, sem contrato, sem migração, sem cutover para
> uma contraparte não nomeada. O lado de fora nunca entra no âmbito por silêncio.

{{build_scope_statement}}

## 2. Portões de construção (condições e pré-condições que travam o arranque)
> **Condicional — engajada onde a decisão registou pelo menos uma condição ou pré-condição que
> trava o arranque de construção, uma actividade de construção, a implementação ou o release.**
>
> Uma linha por portão: *condição · dono · financiada? · até quando · **o que trava** · estado*.
> `not named` renderiza-se como `not named` — nunca se inventa dono nem financiamento.
>
> **Uma condição que trava a construção nunca desaparece desta especificação** (§17.1). Não é um
> *item de trabalho em aberto*: tem dono, estado de financiamento e prazo, e vive nesta secção.
> Condições, pré-condições e itens em aberto mantêm identidades distintas.
>
> **Nenhum portão é convertido em «satisfeito» aqui.** Um portão passa a satisfeito apenas através
> de evidência do engagement (uma linha `Confirmed` ou uma transição `/answer` que o diga). Sem
> isso, renderiza-se como portão por satisfazer.
>
> Sem portões registados: `não aplicável` — secção omitida com a razão, registada como *skip*.

{{build_gates}}

## 3. Restrições de arquitectura (projectadas)
> As secções A do registo, projectadas como restrições de construção. **Somente leitura.**

{{architecture_constraints}}

## 4. Entidades e estruturas de dados
> Uma linha por entidade do blueprint **aprovado**, ligada ao seu domínio por `entities[].authority`:
> *Entidade · Domínio (`key`) · `access_mode` e o que esse modo abdica · **owned**: campos (nome · tipo ·
> obrigatório · default) / **externo**: lidas (n) · escritas (n) · chave · Relações (`join_keys`) · Índices
> (`index` / caminhos delegáveis) · Estado (n `Assumed` / `Confirmed` / `Unknown` · dono do schema)*; por
> entidade, a sub-tabela com as linhas do dicionário — cada uma com o seu `source`.
>
> Os números **ficam escritos** aqui (n campos · n lidas · n escritas · grão · volume): a Estimativa cita-os
> como `driver` e não lê `_capture/` nem a SU. **Uma entidade cuja autoridade não resolve é uma lacuna,
> não uma linha preenchida**: `⚠️ lacuna — entidade sem autoridade de registo — dono: architecture —
> resolve-se com: <key> ou racionalização` e entrada em `render-gaps.md` — nunca a autoridade da entidade
> vizinha, nunca «ver secção 16». Onde o conjunto de autoridade de registo é **afirmativamente vazio**,
> declara-se a racionalização verbatim.

{{entities_to_create}}

## 5. Ecrãs / componentes a construir
> **Condicional a `experience.mode != none`.** Um bloco por ecrã do blueprint **aprovado**: nome ·
> padrão · fontes de dados · controlos-chave · estados de UI · visibilidade RBAC · exclusões
> (`excluded_from_ui`) com a razão. **Nenhum ecrã, persona ou estado é inventado.**
>
> Onde `experience.mode == none`: esta secção **não é produzida** — sem placeholder, sem nota de
> superfície não resolvida, sem lacuna.

{{screens_to_build}}

## 6. Fluxos, automação e transições de estado a implementar
> Um bloco por stream: gatilho · classe de mecanismo · garantia · semântica de falha · base de
> idempotência · origem/destino · passos · tratamento de erro · agendamento. Os quatro primeiros são
> **lidos** de A6, não escolhidos aqui.
>
> **Transições de estado — obrigatórias onde existem, mesmo sem stream em A6.** Onde
> `experience.mode != none` e uma entidade do blueprint **aprovado** carrega `state_machine` ou
> `approval: true`, esta secção carrega, por entidade: **quem transiciona · o que valida a
> transição · o que notifica quem · o que dispara o ciclo**. Uma transição que um operador executa
> à mão continua a ser âmbito desta secção — sem actor, regra de validação, notificação e gatilho
> não é construível.
>
> O **conjunto** de transições é lido do blueprint. O actor, a regra, o destinatário e o gatilho são
> projectados de A7 e de `decisions.md`; onde nenhum dos dois os nomeia, renderiza-se `not named`
> **e** um item de trabalho em aberto — nunca se preenche por analogia com outra entidade ou outro
> role.
>
> `(none)` só é legítimo onde A6 não tem stream **e** nenhuma entidade carrega máquina de estados
> nem passo de aprovação.

{{flows_to_implement}}

## 7. Integrações
> Por integração: sistema · direcção · mecanismo · autenticação e custódia de segredos · frequência ·
> classificação de dados · fronteira de confiança atravessada. Ancorado a A6 e ao componente de
> fronteira que o registo nomeia.

{{integrations}}

## 8. Implementação de segurança e roles
> Classe de identidade (ou identidade de serviço/gerida/de conexão) · plano de imposição · fronteira de
> confiança · matriz de roles e permissões · regras de assinatura e separação de funções. A **forma** da
> matriz pode seguir uma convenção de entrega; a **existência e o alcance** de um controlo vêm de A7.
>
> Numa arquitectura sem superfície humana esta secção mantém-se **em pleno**.

{{security_implementation}}

## 9. Ambientes, governação e release
> Ambientes · vinculação de residência · plano de política · rotas de release · o que fica gated por um
> ambiente gerido. Projectado de A8.

{{environment_and_release}}

## 10. Monitorização e recuperação
> Propriedade de monitorização e alertas · ordem de recuperação · o reconciliador nomeado · o que
> "aceite" significa como evidência. Projectado de A10 e dos canais **Monitorização** e **Recuperação**
> de cada instância de fronteira.

{{monitoring_and_recovery}}

## 11. Obrigações do operador
> O operador nomeado e a rota de suporte (A10 + canal **Operador** de cada fronteira). Um operador
> `UNKNOWN` **não** é um item de trabalho desta especificação: é uma escolha arquitectural
> **estrutural** e bloqueia a aprovação.

{{operator_obligations}}

## 12. Responsabilidade analítica / reporting
> **Condicional** — engajada apenas onde o reporting força um segundo store ou uma cópia.

{{analytical_responsibility}}

## 13. Pacotes de trabalho de prova e condições de aceitação
> **Um pacote de trabalho e uma condição de aceitação por obrigação de prova.** Cada pacote preserva,
> verbatim: *afirmação · nível (V1–V4) · método · dono · financiada?*. **Nunca re-graduar o nível,
> nunca substituir o método, nunca marcar como satisfeita.**
>
> Cenários de fricção do as-is podem **acrescentar cenários** de teste; nunca determinam o nível de
> prova.

{{proof_work_packages}}

## 14. Sequenciamento
> **Dependências apenas — sem durações.** Derivado de: fronteiras A3 · rotas de release A8 · pontos
> fixos A9 · dono de release cross-boundary de cada fronteira. O que tem de aterrar primeiro, e porquê.
> A narrativa financeira **não** é autoridade de sequenciamento.

{{sequencing}}

## 15. Migração e cutover
> **Condicional** — engajada apenas onde o âmbito autorizado substitui um artefacto que atingiu o
> resultado de migração-necessária.
>
> Esta secção é dona de: passos de migração · procedimento de conversão · sequenciamento e tarefas ·
> limpeza de dados · execução detalhada do cutover · procedimento de rollback.
>
> O **Architecture Blueprint** é dono de: o que é substituído · a fronteira de coexistência · a
> arquitectura de transição · as dependências de cutover que são arquitecturais (A9).

{{migration_and_cutover}}

## 16. Alteração do caminho operacional
> **Condicional** — engajada onde o as-is (`_synthesis/as-is.md# Passos e tempo`) tem passos nomeados com
> tempo registado (ou `Unknown` para ele) **e** o inventário desta especificação substitui pelo menos um deles.
> Caso contrário `não aplicável` — skip, nunca lacuna.
>
> Uma linha por passo do as-is: *passo · quem · tempo actual · novo processo · tempo novo · Δ*. O **tempo
> actual** é lido do as-is com o seu estado (`Assumed` com base, ou `Unknown (U-nnn)` que fica na linha). O
> **novo processo** é o item deste inventário que substitui o passo (o ecrã da §5, o fluxo da §6, o contrato
> da §7, a entrada de A5 com o seu volume × cadência); o **tempo novo** só onde esse item carrega uma base —
> senão `not derivable — <razão>`. Um passo que nada substitui renderiza `inalterado`. Δ é uma diferença de
> tempo sobre trabalho que esta especificação nomeia — **nunca** uma afirmação de custo, nunca uma baseline
> reconstruída, nunca a justificação do investimento (`funding_gate: false`).
>
> É esta secção — e só esta — que a Estimativa lê para o seu *Impacto operacional* (modo A).

{{operating_path_change}}

## 17. Itens de trabalho em aberto
> Uma linha por item: o item · **dono** (`architecture` · `implementation` · `design` · `estimate` ·
> `evidence`) · o que o resolveria · o `U-NNN` / `X-NNN` / `A-NNN` que o ancora.
>
> Onde uma escolha arquitectural continua em aberto, **nada de implementação é inventado** para ela.
> Um `Conflicted` não recebe valor escolhido: recebe uma obrigação de prova.

{{open_work_items}}
