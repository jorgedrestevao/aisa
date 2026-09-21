---
template_id: claude-design-brief
canonical_deliverable: claude-design-brief
output_format: md
audience: claude-design

# §8.3 — a APROVADA. O gerador recebe o desenho validado pelo negócio, nunca um
# candidato autorizado que ainda espera aprovação.
blueprint_version_read: v<approved>

# ── PROJECTION CONTRACT ────────────────────────────────────────────────────────────────
# This template DECLARES; it does not execute. `aisa-render` executes only the
# transformations listed in `permitted_transformations`.
# Altitude: DESIGN GENERATION. Nature: the generator-oriented projection of the APPROVED
# UX blueprint, plus the MATERIAL architecture constraints a generated design could violate.
#
# This deliverable receives NEITHER the architecture core NOR the rendered Implementation
# Specification. It receives the approved UX blueprint and a NARROW architecture digest.

# ── APPLICABILITY GATE (§13.5, §20) ───────────────────────────────────────────────────
activation: |
  experience.mode == none                              -> NOT APPLICABLE
  authorization == not-authorized for every scope       -> NOT APPLICABLE
  no approved UX blueprint                              -> BLOCKED
  open_architecture_choices[] has structural:true        -> blueprint approval blocked
                                                        -> no approved UX blueprint
                                                        -> BLOCKED (NO EXCEPTION)
  experience.mode in {owned-internal, owned-external}
    AND an approved UX blueprint exists                 -> REQUIRED
  experience.mode == inherited
    AND an approved UX blueprint exists                 -> CONDITIONAL — covers only what this
                                                           solution may shape of the inherited
                                                           surface; it never designs the host's
                                                           surface
not_applicable_when: experience.mode == none OR authorization == not-authorized for every scope
# => deliverable-level SKIP, logged to render-log.md with the reason. NOT a gap.
blocked_when: no approved UX blueprint exists (run /blueprint), OR a structural:true open
  architecture choice blocks approval
structural_block_rule: |
  structural: true -> blueprint approval blocked -> Implementation Specification BLOCKED
  -> Claude Design Brief BLOCKED.
  NO materiality override. NO partial approval. NO UX-only approval. NO exception based on
  whether the unresolved choice is judged UX-material. Each of those would be new workflow
  semantics, and none exists.

authority_sources:
  - _blueprint/ux-blueprint_v<approved>.yaml     # PRIMARY — screens · personas · navigation ·
                                                 # ui_states · excluded_from_ui · validation
  - decisions.md# Blueprint bp-v<NN> aprovado    # the approval id

conditional_sources:
  - architecture_constraints_digest              # a RUNTIME SELECTION, not a new artefact (§13.2)
  - context.json# brand_guidance
  - shared-understanding.md# lens=user           # accessibility / language rows, where material
  - selective CRAFT units                        # at the POINT OF NEED only
  - one selective RESEARCH unit                  # ONLY where a UI-visible access-path semantic
                                                 # must be expressed

forbidden_sources:
  - architecture-templates/architecture-core.md in full        # the whole architecture core
  - the resolved boundary fragments · the six import channels
  - the characterised Domain Knowledge table                   # D-10 — cite on demand instead
  - decisions.md architecture or economic content
  - _synthesis/financial-story.md
  - _synthesis/architecture-story.md
  - "_render/<slug>_solution-blueprint_v<NN>.md — never the rendered Architecture
     Blueprint, and never confuse it with the UX blueprint"
  - _render/<slug>_implementation-spec_v<NN>.md
  - raw evidence · inputs/* · _capture/*
  - options.md

permitted_transformations:
  - approved UX blueprint screen -> generator-oriented screen block
  - per-screen blocks · consumer-oriented phrasing
  - inline citation of the owning unit where an expression or control convention is needed
  - selecting the MATERIAL architecture constraints into the digest (named A-sections,
    filtered to surface-touching rows, addressed by heading)

forbidden_transformations:
  - selecting store, composition, pattern or experience mode      # all four belong to the
                                                                  # frozen architecture layer
  - re-consolidating screens                                      # the consolidation rules
                                                                  # already ran in /blueprint
  - adding a persona, screen, journey, action or state absent from the approved blueprint
  - changing a requirement
  - becoming an Architecture Blueprint copy
  - preloading the Domain Knowledge catalogue or characterising units it does not use
  - designing a surface for a scope that is not PP-owned
  - designing a screen or journey for a destination that is UNEVALUATED
  - re-grading a proof obligation · promoting an epistemic state · choosing a side of a
    Conflicted row
  - emitting a persona, screen, navigation or UX-state placeholder where the deliverable is
    NOT APPLICABLE

# ── ARCHITECTURE CONSTRAINTS DIGEST (§13.2, §19) ──────────────────────────────────────
# A RUNTIME SELECTION over the recorded architecture. NOT a new artefact, NOT a new file,
# NOT a template, NOT a router, and NOT an architecture reasoning layer.
# Survival test: could the generated design VIOLATE an approved UX / business / control
# requirement if this fact disappeared? YES -> include. Otherwise leave it upstream.
architecture_constraints_digest:
  includes:
    - A1 — the authorized scope this design may cover (one paragraph)
    - A3 — only the boundary-table rows a surface actually TOUCHES
    - A5 — only the UI-visible access-mode consequences (delegation and truncation limits,
        freshness, virtualized/replicated staleness)
    - A7 — identity class, enforcement point, role and permission model
    - A12 — only the DESIGN-RELEVANT items (design-blocking Unknowns, accessibility proof
        obligations, UX-relevant Conflicted rows)
    - A6 — ONLY where an asynchronous state consequence reaches the UX
  excludes:
    - A2 architecture intent                       # rationale, not a design constraint
    - A6 stream internals                          # idempotency basis, failure semantics
    - A8 environments / release topology
    - A9 irreversible choices / exit cost
    - A10 operability / the operating model
    - A11 economics
    - the boundary-fragment six channels
    - the full A3 boundary table
    - the full A5 store detail

# ── SELECTIVE CRAFT AND RESEARCH (§13.4, §29) ─────────────────────────────────────────
# The brief carries a short "where to verify" POINTER LIST (unit + section), never a
# characterised catalogue. A fresh pull is legitimate ONLY for a design decision this brief
# must itself express — an expression, a control convention, a UI-visible access-path limit.
# NEVER for richer prose.
selective_pulls:
  point_of_need: true
  screen_convention: cite the pack's screen-pattern craft unit for the screen type and density
    convention the blueprint ALREADY assigned
  expression: cite the pack's expression craft unit where the brief must emit or constrain an
    expression
  rbac_form: cite the pack's security craft unit for the FORM of the role matrix — never for a
    control's existence or reach
  spreadsheet_anchor: cite the pack's translation craft unit ONLY where the approved blueprint
    carries such an anchor
  consolidation: the pack's screen-consolidation contract is REFERENCE ONLY — its rules already
    ran in /blueprint
  access_path: cite the owning RESEARCH unit (the platform authority on access paths) where an
    A5 consequence reaches the UI
  rule: cite the unit and its section; do not copy it, do not characterise it, do not tabulate
    the catalogue
  craft_boundary: |
    CRAFT shapes the FORM of an artefact and never overrides RESEARCH or architecture. It
    never asserts a platform limit and never a control's existence or reach; where a limit
    is needed, the owning RESEARCH unit is cited.
  point_of_need_rule: |
    A fresh pull is legitimate ONLY at the point of need, for a design decision this brief
    must itself express. Never to make prose richer.

# ── EPISTEMIC PROJECTION (§15) ────────────────────────────────────────────────────────
epistemic_projection:
  Confirmed: fact
  Confirmed_expired: only if UX-material — and then as a re-verification obligation
  Assumed: assumed where UX-material — never promoted
  Unknown: design-blocking ones only, as OPEN — no design invented for them
  Conflicted: render the conflict, design NEITHER side
  Risky: only if UX-material, with its accepted-risk identity

# ── PROOF-OBLIGATION CARRIAGE (§16) ───────────────────────────────────────────────────
proof_obligation_carriage:
  scope: UX / design validations only (accessibility attestation, usability check)
  form: what must be validated · against what
  rule: quoted; never re-graded, never re-methoded, never marked satisfied

required_slots:
  # ONLY the identity slots are unconditional. NO SURFACE SLOT IS EVER `required`:
  # a headless architecture must never manufacture a surface, a persona or a gap.
  - solution_name
  - approved_blueprint_id
  - design_objective

conditional_slots:
  # Every surface slot lives here, gated on the recorded experience mode.
  - surface_inventory
  - persona_users
  - page_navigation_map
  - screen_specifications
  - ux_requirements
  - permissions_affecting_ux
  - excluded_from_ui
  - architecture_constraints_digest
  - brand_guidance
  - accessibility_notes
  - async_state_requirements
  - inherited_surface_limits
  - design_validations
  - design_blocking_open_items
  - where_to_verify

slot_conditions:
  # EVERY surface slot is conditional on the mode. None is ever unconditionally required:
  # a headless architecture must not manufacture a surface, a persona or a gap.
  surface_inventory: experience.mode != none
  persona_users: experience.mode != none
  page_navigation_map: experience.mode != none
  screen_specifications: experience.mode != none
  ux_requirements: experience.mode != none
  permissions_affecting_ux: experience.mode != none AND A7 carries a role model
  excluded_from_ui: experience.mode != none
  architecture_constraints_digest: at least one material design-facing constraint exists
  brand_guidance: context.json carries brand_guidance
  accessibility_notes: a material accessibility / language row exists in lens=user
  async_state_requirements: an A6 asynchronous state consequence reaches the UX
  inherited_surface_limits: experience.mode == inherited
  design_validations: a UX / accessibility proof obligation exists
  design_blocking_open_items: a design-blocking Unknown or a UX-relevant Conflicted row exists
  where_to_verify: the brief emits an expression, a control convention or an access-path limit

slot_sources:
  approved_blueprint_id: decisions.md# D-NNN — Blueprint bp-v<NN> aprovado
  design_objective: _blueprint/ux-blueprint_v<approved>.yaml# app (name, device_targets, language)
  surface_inventory: _blueprint/ux-blueprint_v<approved>.yaml# screens (the recorded primary surface, from architecture.experience.primary_surface)
  persona_users: _blueprint/ux-blueprint_v<approved>.yaml# personas
  page_navigation_map: _blueprint/ux-blueprint_v<approved>.yaml# navigation
  screen_specifications: _blueprint/ux-blueprint_v<approved>.yaml# screens (purpose, pattern, density, data, actions, rbac_visibility, ui_states, platform constraint notes, excel_anchor, su_refs)
  ux_requirements: _blueprint/ux-blueprint_v<approved>.yaml# screens (ui_states) + validation
  permissions_affecting_ux: architecture_constraints_digest# A7 (role and permission model, enforcement point)
  excluded_from_ui: _blueprint/ux-blueprint_v<approved>.yaml# excluded_from_ui (each with its reason + su_refs)
  architecture_constraints_digest: the architecture block# A1 authorized scope + A3 rows a surface touches + A5 UI-visible access-mode consequences + A7 identity/enforcement/roles + A12 design-relevant items (+ A6 where async state reaches the UX)
  brand_guidance: context.json# brand_guidance
  accessibility_notes: shared-understanding.md# lens=user (material accessibility / language rows, with ids and states)
  async_state_requirements: architecture_constraints_digest# A6 (only the asynchronous state consequence that reaches the UX)
  inherited_surface_limits: the architecture block# experience (what this solution may shape of the inherited surface)
  design_validations: the architecture block# proof_obligations[] (UX / accessibility subset only, quoted)
  design_blocking_open_items: _blueprint/ux-blueprint_v<approved>.yaml# open_questions + shared-understanding.md# Conflicted (UX-relevant rows)
  where_to_verify: the owning CRAFT / RESEARCH unit and section, cited at the point of need
---

# Claude Design Brief — {{solution_name}}

> Input para o gerador de design (mockups high-fidelity). **Projecção do blueprint de UX aprovado** —
> a fonte primária é `_blueprint/ux-blueprint_v<NN>.yaml` na versão **aprovada**
> (`library/kernel/blueprint-contract.md`), não o Architecture Blueprint renderizado.
>
> **O design já foi decidido.** Este brief não escolhe store, composição, padrão nem modo de
> experiência; não re-consolida ecrãs (as regras de consolidação já correram em `/blueprint`); e não
> acrescenta persona, ecrã, jornada, acção ou estado que o blueprint aprovado não carregue.
>
> **Sem catálogo de conhecimento técnico pré-carregado.** As unidades autoritativas são **citadas no
> ponto de necessidade**, com unidade e secção — nunca tabeladas nem caracterizadas.
>
> **Blueprint aprovado**: {{approved_blueprint_id}}

## 1. Objectivo de design
{{design_objective}}

## 2. Restrições de arquitectura (digest)
> **Selecção**, não cópia da arquitectura: apenas o que um design gerado poderia **violar** —
> âmbito autorizado (A1) · as linhas de fronteira que uma superfície **toca** (A3) · as consequências
> de modo de acesso **visíveis na UI** (A5: limites de delegação e truncagem, frescura, desactualização
> de dados virtualizados/replicados) · identidade, ponto de imposição e modelo de roles (A7) · os itens
> epistémicos **relevantes para design** (A12).
>
> Fora do digest, e deliberadamente: intenção arquitectural, internos de streams, ambientes e release,
> escolhas irreversíveis, operabilidade, economia, e os seis canais de importação de fronteira.

{{architecture_constraints_digest}}

## 3. Superfície
> A superfície que a arquitectura **registou** (`experience.primary_surface`) — não uma superfície
> assumida. Inventário de superfícies com o âmbito PP-owned que cada uma cobre.

{{surface_inventory}}

## 4. Personas / tipos de utilizador
{{persona_users}}

## 5. Mapa de navegação
{{page_navigation_map}}

## 6. Especificação por ecrã
> Um bloco por ecrã do blueprint **aprovado**: nome · padrão e densidade (convenção já atribuída) ·
> persona primária · dados apresentados e editados (colunas primárias/secundárias) · acções
> primárias/secundárias · visibilidade RBAC · estados de UI (loading / empty / error / success /
> failure) · comportamento de validação e erro · notas de restrição de plataforma · `su_refs`.
>
> **Nada é inventado.** Um ecrã sem âncora no blueprint aprovado não existe neste brief.

{{screen_specifications}}

## 7. Requisitos de UX e estados
{{ux_requirements}}

## 8. Estados assíncronos
> **Condicional** — apenas onde uma consequência de estado assíncrono chega efectivamente à UX. O
> mecanismo, a garantia e a base de idempotência ficam a montante; aqui entra só o que o utilizador vê.

{{async_state_requirements}}

## 9. Permissões que afectam a UX
> O modelo de roles e o ponto de imposição, projectados do digest. A **forma** da matriz segue a
> convenção de entrega; a **existência e o alcance** do controlo vêm de A7.

{{permissions_affecting_ux}}

## 10. Campos deliberadamente não apresentados
> `excluded_from_ui` é **first-class**: cada exclusão com a sua razão e `su_refs`. Não é omissão — é
> decisão de design com rasto.

{{excluded_from_ui}}

## 11. Limites de superfície herdada
> **Condicional a `experience.mode == inherited`.** O que esta solução pode moldar da superfície
> herdada — e o que pertence ao anfitrião e **não** é desenhado aqui.

{{inherited_surface_limits}}

## 12. Brand guidance
{{brand_guidance}}

## 13. Acessibilidade e linguagem
{{accessibility_notes}}

## 14. Validações de design a cumprir
> Apenas validações de UX/design (atestação de acessibilidade, verificação de usabilidade): *o que tem
> de ser validado · contra o quê*. O nível, o método, o dono e o estado de financiamento são **citados**,
> nunca re-graduados nem marcados como satisfeitos.

{{design_validations}}

## 15. Itens em aberto que bloqueiam design
> Os `Unknown` que bloqueiam uma decisão de design e as linhas `Conflicted` relevantes para UX: o
> conflito é **renderizado**, e **nenhum lado é desenhado**. Nenhum design é inventado para um item
> em aberto.

{{design_blocking_open_items}}

## 16. Onde verificar
> Lista curta de **apontadores** (unidade + secção) para as fontes autoritativas que este brief citou
> no ponto de necessidade. Sem caracterização, sem catálogo, sem tabela de unidades.

{{where_to_verify}}
