---
template_id: estimate
canonical_deliverable: estimate
output_format: md
audience: client

# §8.3 — lê o inventário da Implementation Specification, não o desenho.
blueprint_version_read: none

# ── PROJECTION CONTRACT ────────────────────────────────────────────────────────────────
# This template DECLARES; it does not execute. `aisa-render` executes only the
# transformations listed in `permitted_transformations`.
# Nature: A CALCULATION AND PROJECTION over decided scope and implementation work.

activation: a decided scope exists AND the work is inside this pack's estimation authority
  AND one of the two input modes resolves
not_applicable_when: |
  decision class 12 (Decision Blocked)             -> NOT APPLICABLE (no decided scope to
                                                      calculate over; the evidence task belongs
                                                      to the Executive Report's "what happens
                                                      next" and the Discovery Report's
                                                      "evidence still required")
  the selected implementation is OUTSIDE this pack's estimation authority
                                                   -> NOT APPLICABLE, with the reason:
                                                      "this pack has no estimation basis for the
                                                      selected solution class"
blocked_when: neither input mode resolves
# A deliverable-level skip is logged to render-log.md with the reason. It is NOT a gap and
# never lands in render-gaps.md. Never a placeholder number, never a guess, never a
# comparative figure.

# ── SEMANTIC OWNERSHIP AND EXECUTION (§40.4) ──────────────────────────────────────────
owns_calculation: true
# MEANS: this deliverable contract AUTHORIZES `aisa-render` to execute the bounded calculation
#        defined by this template, using the named method authority.
# DOES NOT MEAN: this Markdown template reasons.
semantic_owner: estimate
# The Estimate is the semantic owner of: work-unit mapping · effort calculation · arithmetic ·
# estimate assumptions · range · contingency · confidence.
calculation_executor: aisa-render
# `aisa-render` and NOTHING ELSE executes it. No new engine. No new skill. No estimation agent.
# NO OTHER runtime artefact or skill may compute implementation effort — synthesis included.
no_second_estimate_authority: |
  There is exactly ONE implementation-effort authority in the runtime: this deliverable.
  No synthesis template, no other deliverable template and no skill computes an
  implementation-effort figure. Financial synthesis carries DECISION ECONOMICS only; any
  implementation-effort prose it carries may only REFERENCE or PROJECT an already-produced
  Estimate, and is never where a figure first appears.

# ── THE FOUR STRUCTURAL DECLARATIONS A CALCULATION-OWNING DELIVERABLE MUST CARRY ──────
# (§40.4, asserted by T-D19)
input_inventory_authority:
  mode_a: the Implementation Specification's inventory
  mode_b: the candidate architecture record(s) — per candidate
method_authority: library/packs/pp/domain-knowledge/craft/estimation-model.md
# METHOD ONLY, person-days. Its own banner states it is NOT VALID AS COMPARATIVE ECONOMICS,
# and this deliverable never uses it comparatively.
permitted_outputs:
  - work breakdown (inventory unit -> work unit)
  - effort bands — PLANNING INTERVALS (min-max) over the method's own bands
  - ranges
  - contingency
  - confidence statement
forbidden_semantic_changes:
  - no scope change (no scope added, dropped, widened or collapsed)
  - no epistemic promotion (Assumed stays assumed; Unknown stays unknown; Conflicted keeps
    both sides or neither; an expired Confirmed is an uncertainty line, never a fact)
  - no comparator claim (no economic-attractiveness verdict, no "cheaper than", no ranking)
  - no invented work unit (see the per-mode scope-control rule)
  - no price (no licence price, no SKU price, no platform rate card, no quota as a cost fact)

# ── INPUT MODES — EXACTLY TWO, AND NO THIRD (§40.6) ───────────────────────────────────
input_modes_count: 2
input_modes:
  A:
    name: implementation estimate
    status: the authoritative path
    available_when: an approved architecture exists AND an Implementation Specification exists
    inputs:
      - "the Implementation Specification's inventory — components, obligations,
         proof work, migration steps, open work items (INVENTORY ONLY: no narrative,
         no rationale, no architecture description, no acceptance text)"
      - library/packs/pp/domain-knowledge/craft/estimation-model.md   # method
      - decisions.md# D-NNN                            # scope · pairs · accepted risks ·
                                                       # conditions that change effort
    scope_control: |
      WHEN A SPECIFICATION EXISTS, THE ESTIMATE MAY NOT ADD A WORK UNIT ABSENT FROM THAT
      SPECIFICATION. A needed-but-absent unit is an OPEN WORK ITEM logged against the
      Specification (owner: implementation) — never an invented Estimate line.
  B:
    name: candidate planning estimate
    status: available ONLY where all three conditions hold
    available_when: |
      architecture candidates exist
      AND architecture approval is blocked by the unresolved structural choice
      AND a sponsor materially needs comparative delivery magnitude
    mandatory_label: "Candidate planning estimate — pre-Implementation-Specification;
      lower-confidence; architecture choice unresolved."
    inputs:
      - candidate architecture components
      - candidate-specific KNOWN configuration / build obligations
      - KNOWN proof work
      - KNOWN migration work
      - library/packs/pp/domain-knowledge/craft/estimation-model.md   # method
      - decisions.md# D-NNN
    isolation: |
      PER CANDIDATE: its own work inventory · its own estimate · its own uncertainty · its own
      confidence, each labelled with its candidate id and the mandatory label above.
      NEVER blend candidates into one figure. NEVER select a candidate. NEVER rank them.
    may_estimate:
      - architecture components
      - known configuration / build obligations
      - known proof work
      - known migration work
    may_not_estimate:
      - detailed implementation tasks not yet derivable
      - screen-level work while the UX blueprint is unapproved
      - an unevaluated far side
      - work whose existence depends on the unresolved choice without being assigned to the
        candidate it belongs to
    scope_control: |
      THE ESTIMATE MAY NOT ADD A WORK UNIT ABSENT FROM THE CANDIDATE ARCHITECTURE'S KNOWN
      COMPONENTS / OBLIGATIONS.
      no spec != permission to invent a spec
no_third_mode: |
  There is no third input mode. Where neither basis is present the Estimate is BLOCKED or
  NOT APPLICABLE, as appropriate — never a placeholder and never a guess.

authority_sources:
  - itself, for the calculation                  # SEMANTIC OWNER; aisa-render is only the executor
  - the Implementation Specification's inventory # MODE A input authority
  - library/packs/pp/domain-knowledge/craft/estimation-model.md   # METHOD authority, person-days
  - decisions.md# D-NNN                          # scope · pairs · accepted risks · conditions

conditional_sources:
  - the architecture block                       # MODE B component authority;
                                                 # open_architecture_choices[] as named uncertainty
  - the architecture block# A11 drivers + library/packs/pp/domain-knowledge/economics/licensing-and-cost-drivers.md
                                                 # DRIVERS ONLY — no prices
  - architecture-templates/architecture-core.md# A8, A10   # DELIVERY PRECONDITIONS ONLY —
                                                 # environments, release routes, policy plane,
                                                 # the operating model's roles and the support
                                                 # route. Never a work unit, never an effort
                                                 # figure, and never a person: a precondition
                                                 # owed by a role is complete with `not named`
  - _synthesis/risks-and-assumptions.md
  - _synthesis/architecture-story.md# Authorized scope and outcome basis
                                                 # where not-authorized: the reason for this
                                                 # deliverable's own applicability (DURABLE
                                                 # CARRIER of an architecture-entry result, never
                                                 # architecture authority, never re-evaluated here)

forbidden_sources:
  - live licence prices · SKU prices · platform rate cards · quotas presented as cost facts
  - options.md S8 comparative economics as an estimate input or output
  - library/packs/pp/domain-knowledge/craft/estimation-model.md used COMPARATIVELY
  - _synthesis/financial-story.md as the source of an effort figure   # the split runs the other way
  - "_synthesis/as-is.md — NOT required, NOT conditional, NOT fallback, NOT point-of-need.
     The as-is narrative is not an Estimate authority in either mode: no work unit, no
     effort figure and no operational-impact timing may originate there"
  - _synthesis/business-story.md
  - any discovery narrative as the source of a work unit
  - raw evidence · inputs/* · _capture/*
  - shared-understanding.md rows as the source of a work unit
  - "another deliverable's narrative as authority — the ONLY deliverable this Estimate reads
     is the Implementation Specification, and only its INVENTORY (§6.5)"

permitted_transformations:
  # DETERMINISTIC · BOUNDED · DECLARED HERE · TRACEABLE to an authoritative input.
  - inventory unit               -> work unit
  - work units + estimation method -> effort bands
  - work units + effort bands      -> phases
  - bands + named uncertainties    -> range + contingency + confidence
  - arithmetic over the above (person-days)
  - delivery precondition        -> gate on a NAMED phase (never a duration, never a work unit)
  - phase >= 5 person-days      -> task sub-table (task · planning interval min-max ·
                                   responsible profile) whose union CONTAINS the phase figure
  - team profile + the dedication declared in the preconditions -> minimum weeks
                                   (person-days / dedication) — arithmetic only
  - repetition dimension over N named instances -> pilot recommendation over a NAMED subset
  - tables

forbidden_transformations:
  - deciding whether this platform is cheaper, better or more attractive
  - settling economic attractiveness (that is S8, at decision altitude)
  - emitting any price, SKU, rate card or quota-derived cost
  - substituting the estimation method for S8 comparative economics
  - HIDING an architectural Unknown inside contingency
  - "filing a DELIVERY PRECONDITION — SME availability, an access or credential, a licence or
     entitlement, an environment or provisioning step, a third-party dependency — as an estimate
     assumption, as a named uncertainty or inside contingency. It has an owner, a due date and a
     phase it blocks, and it renders in its own section with that carriage"
  - rendering a delivery precondition as satisfied without recorded engagement evidence
  - "decomposing a phase in a way that changes its figure, or that changes the global total. The
     sub-table REDISTRIBUTES what the phase already carries; it never adds work, and the total
     person-day figure is identical before and after decomposition"
  - fabricating task granularity below what the active mode's authoritative inventory carries
  - "a weekly grid, a Gantt, a calendar date, or a derived overlap between profiles. Parallelism
     is judgement and the team is not observed here: the dependency list is the ONLY thing this
     Estimate says about it, and it says it in prose"
  - "claiming a quantile: never `P50`, never `P80`, never a confidence percentage over a
     distribution. The method carries no distribution; what this deliverable emits is a planning
     interval"
  - estimating far-side delivery
  - estimating an UNEVALUATED destination — no allowance, no placeholder, no contingency band
  - adding a work unit the active mode's authority does not carry
  - "as-is friction, as-is timing, as-is exception or any discovery narrative -> a new
     Estimate work unit. Mode A: a discovery fact that should alter implementation work but
     is absent from the authoritative inventory becomes an OPEN WORK ITEM against the
     Implementation Specification (owner: implementation), never an Estimate line. Mode B:
     usable only where it is already represented as a candidate-specific KNOWN architecture
     obligation; otherwise the uncertainty is PRESERVED, not resolved"
  - blending candidate estimates into one figure · selecting a candidate
  - fabricating implementation tasks, screen-level work or a far side
  - changing architecture · changing scope · re-grading a proof obligation
  - promoting an epistemic state

# ── THE CONTINGENCY-HONESTY RULE (§14.4) ──────────────────────────────────────────────
contingency_honesty: |
  Every structural open choice and every decision-changing Unknown that affects effort appears
  as a NAMED uncertainty line: the open item · the effort it swings · what would settle it ·
  its U-NNN. Contingency is a number OVER the named items, never a substitute for them.

# ── ECONOMICS SEPARATION (§18) ────────────────────────────────────────────────────────
economics_separation: |
  S8 decision economics -> economic attractiveness / option worth. Home: Executive Report.
  This Estimate          -> implementation effort / delivery projection. Home: here.
  NOT the same question, and NOT merged. An implementation estimate can be low while an
  option is economically unattractive, and the reverse.
# ── INTERVALS, NOT QUANTILES (F09) ────────────────────────────────────────────────────
# ── THE OPTIONS BAND IS NOT AN ESTIMATE ────────────────────────────────────
order_of_magnitude_boundary: |
  The order-of-magnitude band each option carried in options.md was produced to COMPARE options
  before a decision, from one of three declared sources (SIMULATED, PACK MODEL, ANALOGY). It is
  NOT an input to this deliverable and it NEVER becomes a delivery commitment by being carried
  across. This Estimate re-derives its figures from the work-unit inventory of the CHOSEN option
  against the method, post-decision, where sizing one path is the right job.
  Where the two disagree, the Estimate is the figure and the divergence is REPORTED, not smoothed:
  a band that was wide because the option was still unknown is information about the decision, not
  an error to hide. An option whose band read ORDER OF MAGNITUDE UNAVAILABLE is estimable here
  exactly like any other once it is chosen — the field said the comparison lacked a basis, never
  that the work is unsizeable.
interval_vocabulary: |
  Every range this deliverable emits is a PLANNING INTERVAL: a min-max over the method's own
  bands, with each factor cited to the section of craft/estimation-model.md that states it.
  It is NOT a quantile. The method carries per-component rates, complexity factors and a
  buffer; it carries NO distribution, so `P50`, `P80` or any other quantile may not be claimed
  here, in the Estimate or in simulation, until a probabilistic method is documented and
  calibrated in the pack. A factor with no section that states it is NOT applied.
denominator: |
  PERSON-DAYS remain the canonical denominator absent a valid engagement-provided delivery
  rate. Such a rate, if ever supplied, is an ENGAGEMENT INPUT WITH PROVENANCE — not Domain
  Knowledge and not a pack fact. This pack supplies none.

# ── SCOPE PAIRS AND SCOPE-OWNERSHIP CATEGORIES (§19.1) ────────────────────────────────
pricing_by_scope_category:
  1_architected_here: estimated
  2_relocated_boundary_represented: |
    the PP-side integration obligation IS estimated; far-side DELIVERY is EXCLUDED with the
    reason (its owner is external), and estimated only where this pack's estimation authority
    explicitly covers it AND evidence exists
  3_excluded_destination_unevaluated: |
    NEVER estimated. The exclusion is STATED, not silent. No allowance, no placeholder, no
    contingency band for an unknown external implementation.
  4_no_authorization: |
    only if the selected implementation is inside this pack's estimation authority
    (normally NOT applicable)

# ── EPISTEMIC PROJECTION (§15) ────────────────────────────────────────────────────────
epistemic_projection:
  Confirmed: fact; basis of the band
  Confirmed_expired: uncertainty line
  Assumed: assumed; feeds the range
  Unknown: NAMED uncertainty line — never absorbed into contingency
  Conflicted: NO figure chosen; range + named uncertainty
  Risky: uncertainty / contingency input, IDENTIFIED by its R-NNN

# ── PROOF-OBLIGATION CARRIAGE (§16) ───────────────────────────────────────────────────
proof_obligation_carriage:
  scope: the EFFORT for the proof work
  form: work unit + effort + uncertainty
  rule: the V-level, method, owner and funded state are quoted from the record, never changed

required_slots:
  - solution_name
  - input_mode_statement
  - estimate_scope_statement
  - work_breakdown
  - effort_bands
  - phases_table
  - effort_summary
  - named_uncertainties
  - range_and_contingency
  - confidence_statement
  - estimate_assumptions
  - excluded_scope

conditional_slots:
  - candidate_estimates
  - proof_work_effort
  - migration_effort
  - estimate_preconditions
  - team_effort
  - profile_load
  - operational_impact
  - cost_drivers
  - delivery_recommendations

slot_conditions:
  candidate_estimates: input mode == B (one separately labelled block per candidate)
  proof_work_effort: proof_obligations[] is non-empty
  migration_effort: the Specification carries a migration & cutover section (mode A) OR the
    candidate carries KNOWN migration work (mode B)
  phases_table: "REQUIRED. Any phase whose figure is >= 5 person-days carries a sub-table of its
    own — task · planning interval (min-max) · responsible profile — and the union of those
    intervals CONTAINS the phase figure: sum(min) <= phase figure <= sum(max). The phases table
    itself carries a `responsible profile` column. A phase under 5 person-days is NOT decomposed.
    Decomposition never changes the phase figure and never changes the global total; the interval
    derivation is stated as a method premise in the assumptions section. A task whose method entry
    is a POINT RATE renders min == max, flagged as such; a task with NO method entry renders
    min == max with the analogy named and `no band in the method`. A SPREAD IS NEVER FABRICATED to
    make a point rate look like a range — a degenerate interval that says why is information; an
    invented ± is not."
  named_uncertainties: "REQUIRED. Each named uncertainty ALSO appears, on ONE line, in the phase
    whose figure it threatens — the same item, cross-referenced by its id, never a second
    uncertainty and never a contingency line. An uncertainty that threatens no phase says so
    explicitly, and stays in the list."
  profile_load: "team_effort resolves AND the delivery preconditions declare a DEDICATION for at
    least one named profile. Per profile: person-days / dedication -> minimum weeks. ARITHMETIC
    ONLY — no grid, no calendar date, no derived overlap between profiles. Where the Implementation
    Specification's sequencing carries dependencies, they are listed as a CONSTRAINT ON
    PARALLELISM in prose, never resolved into a schedule. Absent a declared dedication for a
    profile, that profile renders `dedication not named` and NO week figure."
  estimate_preconditions: "A8, A10, decisions.md# Conditions / Preconditions or — in mode A —
    the Implementation Specification's build gates carry at least one DELIVERY PRECONDITION that
    must hold before a named phase of section 5 may proceed: SME or process-owner availability, an
    access or credential, a licence or entitlement, an environment or provisioning step, a
    third-party dependency. ALSO engaged where the architecture block carries a composition with
    `boundary: outside-platform` (ACCESS to a component another team operates gates the phase that
    touches it) or where the method's delivery guidance requires an availability be agreed in
    advance. REQUIRED SUBJECT TO EXISTENCE — present upstream means it renders, with
    the build-gate carriage (condition · owner · by when · WHICH PHASE it blocks · status). It is
    never compressed into an estimate assumption, a named uncertainty or contingency. Absent
    upstream: `not applicable`, logged as a skip, never a gap."
  team_effort: the work breakdown resolves to more than one delivery profile
  operational_impact: "the ACTIVE MODE'S authoritative inventory carries an operating-path
    change — mode A, the Implementation Specification's inventory; mode B, the candidate's
    KNOWN obligations. Otherwise NOT APPLICABLE"
  cost_drivers: A11 carries an entitlement or growth driver
  delivery_recommendations: "at least one delivery-sequencing or de-risking recommendation
    follows from the work breakdown. AND where the decomposition carries a REPETITION DIMENSION —
    the same work repeated over N named instances (sites, parks, products, customer segments,
    countries) with N >= 3 — a pilot over a NAMED SUBSET is recommended, the subset named FROM the
    inventory and never invented. Absent a repetition dimension, no pilot is manufactured."

slot_sources:
  input_mode_statement: computed — which of the TWO modes resolved, and why (mode B carries its mandatory label verbatim)
  estimate_scope_statement: decisions.md# D-NNN — (Scope, outcome) pairs — UNCOLLAPSED (the PP-owned side only) + the scope-ownership projection categories
  work_breakdown: MODE A — the Implementation Specification's inventory (components · obligations · proof work · migration steps · open work items) | MODE B — the candidate architecture record's KNOWN components and obligations. Each row carries a `driver` column (P-10) citing the inventory figure that sizes it — the Specification's §4 counts (n campos · n lidas · n escritas · grão · volume, e.g. `spec §4 InputsDiarios — 39 escritas/dia`), a §5 screen count, a §6 flow count, a §7 contract count — or `sem driver no inventário`; the Estimate never reads the capture, the SU or a topic pack for a driver
  effort_bands: computed — work units x library/packs/pp/domain-knowledge/craft/estimation-model.md (method only, person-days)
  phases_table: computed — work units + effort bands, sequenced by the Specification's architecture-derived dependencies (mode A) or the candidate's known dependencies (mode B); each phase carries its responsible profile from `team_effort`, and each phase >= 5 person-days carries its task sub-table (task · planning interval · profile) over the SAME work units, redistributing the phase figure and never adding to it
  effort_summary: computed — per-phase and total person-days
  proof_work_effort: the architecture block# proof_obligations[] (claim · V-level · method · owner · funded? quoted) -> work unit + effort + uncertainty
  migration_effort: the Implementation Specification# migration & cutover (mode A) | the candidate's KNOWN migration work (mode B)
  named_uncertainties: the architecture block# open_architecture_choices[] + decisions.md# D-NNN — Accepted risks + shared-understanding.md# Unknown / Conflicted / Risky / expired Confirmed rows that swing effort; each item ALSO cross-referenced, on one line, into the phase it threatens
  range_and_contingency: computed — a range over the bands + a contingency number OVER the named uncertainties
  confidence_statement: computed — must MATCH the epistemic state of the inputs (mode B is lower-confidence by construction)
  estimate_preconditions: "architecture-templates/architecture-core.md# A8 (environments, release routes, policy plane) + A10 (the operating model's roles and the support route) + decisions.md# D-NNN — Conditions, Preconditions + MODE A the Implementation Specification# build gates + the architecture block# compositions[] where `boundary: outside-platform` (the recorded `owner` of that composition is the precondition's owner) + library/packs/pp/domain-knowledge/craft/estimation-model.md# standard team composition and delivery guidance (the DEDICATION a profile owes, and any availability that guidance requires be agreed in advance) — each as condition · owner as a ROLE (`not named` included, NEVER invented; never a person) · by when · WHICH PHASE of section 5 it blocks · status ONLY where engagement evidence records it. The DEDICATION each profile commits here is the input to the profile-load calculation of section 16; a profile is a role, and the calculation runs whether or not anybody is named against it"
  estimate_assumptions: METHOD PREMISES ONLY — how the method was applied to THIS inventory (which band was used for a work unit and why, which midpoint, which analogy, calendar read as effort) + _synthesis/risks-and-assumptions.md# Assumptions to validate during build, and of those ONLY the ones that change a work unit or a band. SME availability, accesses, credentials, licences, entitlements and provisioning are NOT assumptions here — they are DELIVERY PRECONDITIONS and render in that section with an owner and the phase they block
  excluded_scope: the scope-ownership projection categories 2, 3 and 4 — each exclusion STATED with its reason
  team_effort: computed — delivery profiles implied by the work breakdown x the method's team guidance
  profile_load: "computed — per profile of `team_effort`, its person-days from the work breakdown / the DEDICATION declared in the delivery preconditions -> minimum weeks; + MODE A the Implementation Specification# sequencing as a PROSE constraint on parallelism. The dedication is never invented here and never re-declared: it is read from the preconditions section"
  operational_impact: MODE A — the Implementation Specification's inventory (the operating-path change the specified work produces — its section *Alteração do caminho operacional*, read as it stands — passo · quem · tempo actual · novo processo · tempo novo · Δ, Unknowns kept) | MODE B — the candidate's KNOWN obligations. Where the authoritative inventory carries no operating-path change, this section is NOT APPLICABLE. A delta over work whose authority this Estimate can name — never a reconstructed baseline, and never a cost claim
  cost_drivers: the architecture block# A11 + library/packs/pp/domain-knowledge/economics/licensing-and-cost-drivers.md (DRIVERS ONLY — no prices)
  delivery_recommendations: computed from the work breakdown — DELIVERY recommendations only
  candidate_estimates: MODE B ONLY — one separately labelled block per candidate architecture, each with its own inventory, estimate, uncertainty and confidence
---

# Estimativa de Implementação — {{solution_name}}

> Estimativa de **esforço de implementação** para o âmbito decidido. Audience: sponsor + procurement.
>
> **Esta entrega é a dona do cálculo.** O mapeamento inventário→unidades de trabalho, a aritmética, as
> premissas de estimativa, a gama, a contingência e a confiança pertencem-lhe; o método vem de
> `craft/estimation-model.md` (**método apenas**, pessoa-dias). Nenhum outro artefacto ou skill do
> runtime calcula esforço de implementação.
>
> **Não é economia de decisão.** A atractividade económica de uma opção (S8) vive no Relatório
> Executivo. Uma estimativa baixa não torna uma opção atractiva, nem o contrário.
>
> **Sem preços.** Sem preços de licença, sem SKUs, sem tabelas de preço de plataforma, sem quotas
> apresentadas como facto de custo. O denominador é **pessoa-dias**.

## 1. Modo de input
> Dois modos, e nenhum terceiro: **A — estimativa de implementação** (inventário da Especificação de
> Implementação) ou **B — estimativa de planeamento de candidatos** (registo de arquitectura candidata,
> apenas onde a aprovação está bloqueada por uma escolha estrutural não resolvida). O modo B carrega o
> seu rótulo obrigatório verbatim.

{{input_mode_statement}}

## 2. Âmbito desta estimativa
> Apenas o lado **PP-owned**. Uma estimativa que cobre parte do âmbito é completa quando **diz que
> parte**.

{{estimate_scope_statement}}

## 3. Decomposição de trabalho
> Uma linha por unidade de trabalho, ancorada à unidade de inventário que a origina, com a coluna
> **`driver`** (P-10): a figura do inventário que a dimensiona — os números da §4 da Especificação
> (n campos · n lidas · n escritas · grão · volume), uma contagem de ecrãs da §5, de fluxos da §6, de
> contratos da §7 — ou `sem driver no inventário`. O driver é **citado** à Especificação; esta estimativa
> não lê a captura, a SU nem um resumo por tema para o obter.
>
> **Controlo de âmbito** — modo A: nenhuma unidade de trabalho ausente da Especificação pode ser
> acrescentada; uma unidade necessária mas ausente é um **open work item** contra a Especificação
> (dono: `implementation`). Modo B: nenhuma unidade ausente dos componentes/obrigações **conhecidos**
> do candidato pode ser acrescentada. *Não haver especificação não é licença para inventar uma.*

{{work_breakdown}}

## 4. Bandas de esforço
> **Intervalos de planeamento (min–max)** sobre as bandas do próprio método, com cada factor
> citado à secção de `craft/estimation-model.md` que o enuncia. **Não são quantis.** O método
> carrega taxas por componente, factores de complexidade e um buffer; **não** carrega distribuição
> — logo `P50`, `P80` ou qualquer outro quantil não se afirmam aqui. Um factor sem secção que o
> enuncie não se aplica.

{{effort_bands}}

## 5. Fases
> Sequenciadas pelas dependências **derivadas da arquitectura** que a Especificação carrega (modo A) ou
> pelas dependências conhecidas do candidato (modo B). A narrativa financeira não é autoridade de
> sequenciamento.
>
> Cada fase carrega o seu **perfil responsável**. Uma fase de **≥ 5 pessoa-dias** carrega ainda a
> sua **sub-tabela de tarefas**: *tarefa · intervalo de planeamento (min–max) · perfil*. A união
> dos intervalos **contém** a figura da fase — `soma(min) ≤ figura da fase ≤ soma(max)`. Abaixo de
> 5 pessoa-dias não se decompõe: granularidade fabricada não é informação.
>
> **A decomposição redistribui, não acrescenta.** A figura da fase e o total global são idênticos
> antes e depois. A regra usada para derivar cada intervalo declara-se como premissa de método na
> secção 13.
>
> Cada incerteza nomeada da secção 9 aparece **numa linha** da fase que ameaça — o mesmo item,
> referenciado pelo seu id, nunca uma segunda incerteza.

{{phases_table}}

## 6. Resumo de esforço
{{effort_summary}}

## 7. Esforço de trabalho de prova
> Uma unidade de trabalho por obrigação de prova, com o seu esforço e incerteza. A *afirmação · nível
> (V1–V4) · método · dono · financiada?* são **citados** do registo — nunca re-graduados.

{{proof_work_effort}}

## 8. Esforço de migração
> **Condicional.** Lê a secção de migração e cutover da Especificação (modo A) ou o trabalho de migração
> **conhecido** do candidato (modo B). Nunca lido directamente de linhas de risco do SU.

{{migration_effort}}

## 9. Incertezas nomeadas
> Uma linha por item: **o item em aberto · o esforço que oscila · o que o resolveria · o `U-NNN`**.
>
> **Nenhum Unknown arquitectural é escondido dentro da contingência.** A contingência é um número
> **por cima** dos itens nomeados, nunca um substituto deles. Um `Conflicted` não recebe figura
> escolhida: recebe gama e uma incerteza nomeada.

{{named_uncertainties}}

## 10. Gama e contingência
{{range_and_contingency}}

## 11. Confiança
> A declaração de confiança **corresponde** ao estado epistémico dos inputs. Uma estimativa de modo B é
> de confiança inferior por construção, e diz isso.

{{confidence_statement}}

## 12. Estimativas por candidato
> **Modo B apenas.** Um bloco **separadamente rotulado** por arquitectura candidata, cada um com o seu
> inventário, a sua estimativa, a sua incerteza e a sua confiança.
>
> Rótulo obrigatório, verbatim, em cada bloco:
>
> > Candidate planning estimate — pre-Implementation-Specification; lower-confidence; architecture
> > choice unresolved.
>
> **Nunca misturar candidatos numa figura. Nunca escolher um candidato. Nunca inventar tarefas de
> especificação, trabalho ao nível de ecrã, nem um lado externo não avaliado.**

{{candidate_estimates}}

## 13. Premissas da estimativa
> **Premissas de método apenas** — como o método foi aplicado a *este* inventário: que banda foi
> usada para uma unidade de trabalho e porquê, que ponto médio, que analogia, que leitura de
> calendário como esforço.
>
> **Não pertencem aqui**: disponibilidade de SME ou do dono do processo, acessos, credenciais,
> licenças, entitlements, aprovisionamento, dependências de terceiros. Essas são **pré-condições
> de entrega** — têm dono, prazo e uma fase que travam, e vivem na secção 14. Uma pré-condição
> escrita como premissa perde o dono e o prazo, e é por isso que ninguém a fecha.

{{estimate_assumptions}}

## 14. Pré-condições de entrega
> **Condicional — engajada onde existe pelo menos uma pré-condição de entrega** que tem de se
> verificar antes de uma fase nomeada da secção 5 poder avançar: disponibilidade de SME ou do dono
> do processo, um acesso ou credencial, uma licença ou entitlement, um ambiente ou passo de
> aprovisionamento, uma dependência de terceiros.
>
> Uma linha por pré-condição: *condição · dono · até quando · **que fase trava** · estado*.
> `not named` renderiza-se como `not named` — nunca se inventa dono nem prazo.
>
> **Nenhuma pré-condição é convertida em «satisfeita» aqui.** Passa a satisfeita apenas através de
> evidência do engagement. Sem isso, renderiza-se por satisfazer, com a fase que trava.
>
> A **dedicação** que cada perfil nomeado aqui compromete é o input do cálculo de ocupação da
> secção 16 — é a mesma declaração, lida duas vezes, nunca duas declarações diferentes.
>
> Sem pré-condições registadas: `não aplicável` — omitida com a razão, registada como *skip*.

{{estimate_preconditions}}

## 15. Âmbito excluído desta estimativa
> Cada exclusão **declarada**, com a razão — nunca silenciosa:
> - **relocado, fronteira representada** — a obrigação de integração do lado PP é estimada; a entrega do
>   lado de fora é excluída (dono externo);
> - **excluído, destino não avaliado** — **nunca estimado**: sem provisão, sem placeholder, sem banda de
>   contingência para uma implementação externa desconhecida;
> - **sem autorização de arquitectura** — normalmente não aplicável a esta estimativa.

{{excluded_scope}}

## 16. Equipa e esforço por perfil
> Por perfil: pessoa-dias, dedicação e as fases em que entra. A **dedicação** é a que a secção 14
> declara — lida, não redeclarada.

{{team_effort}}

> **Ocupação por perfil** — *condicional*, engajada onde a secção 14 declara dedicação para pelo
> menos um perfil nomeado. Aritmética apenas: `pessoa-dias ÷ dedicação → semanas mínimas`. Um
> perfil sem dedicação declarada renderiza `dedication not named` e **nenhuma** figura de semanas.
>
> **Sem grelha, sem Gantt, sem data de calendário, sem sobreposição derivada entre perfis.** O
> paralelismo é julgamento e a equipa não é observada aqui. Onde a Especificação carrega
> dependências de sequenciamento, listam-se como **restrição ao paralelismo**, em prosa — nunca
> resolvidas num calendário.

{{profile_load}}

## 17. Impacto operacional
> **Condicional** — engajada apenas onde o inventário autoritativo do modo activo carrega uma
> alteração de caminho operacional (modo A: o inventário da Especificação de Implementação; modo B:
> as obrigações **conhecidas** do candidato). Caso contrário: **não aplicável**.
>
> A mudança de caminho operacional é **projectada do trabalho especificado**, não descoberta aqui. A
> narrativa de as-is **não** é fonte desta secção: esta estimativa não reconstrói uma baseline nem lê
> fricção, tempos ou excepções de descoberta para inventar trabalho. Onde um facto de descoberta
> devesse alterar o trabalho de implementação mas não conste do inventário autoritativo, isso é um
> **open work item** contra a Especificação (dono: `implementation`) — nunca uma linha desta
> estimativa.
>
> É um delta de tempo sobre trabalho cuja autoridade esta estimativa pode nomear — nunca uma afirmação
> de custo.

{{operational_impact}}

## 18. Drivers de custo
> **Drivers apenas** — classe de entitlement por audiência, população afectada, medidores engajados,
> driver de crescimento no horizonte declarado. **Sem preços, sem SKUs, sem quotas como facto de custo.**

{{cost_drivers}}

## 19. Recomendações de entrega
> **Recomendações de entrega apenas** — sequência, de-risking, faseamento, piloto. **Nenhuma afirmação
> sobre opções, atractividade económica, comparação ou ROI.**
>
> **Dimensão de repetição.** Onde a decomposição repete o mesmo trabalho sobre **N ≥ 3 instâncias
> nomeadas** (locais, parques, produtos, segmentos de cliente, países), recomenda-se **piloto sobre
> um subconjunto nomeado** — o subconjunto vem do inventário, nunca se inventa. Sem dimensão de
> repetição, não se fabrica piloto nenhum.

{{delivery_recommendations}}
