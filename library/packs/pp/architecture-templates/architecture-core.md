---
template_id: architecture-core
category: architecture
scope: architecture-output-shape   # NOT an option class — see architecture-templates/README.md
entry_point: true                  # the ONE fixed path every caller references
required_slots:
  - solution_name
  - architecture_block             # the `architecture:` block of the approved blueprint
optional_slots:
  - scope_ownership_table
  - analytical_responsibility
  - offline_and_device
  - replacement_of_existing_artefact
  - context_picture
  - sequence_sketch
  - candidate_architectures
sub_templates:
  # ZERO or ONE experience fragment, resolved from architecture.experience.mode.
  # `none` resolves to NO include. There is deliberately no fragment-experience-none.md.
  - fragment-experience-internal.md
  - fragment-experience-external.md
  - fragment-experience-inherited.md
  # ZERO or MORE instances — one per qualifying component. The skill performs the iteration.
  - fragment-boundary-and-imports.md
slot_sources:
  architecture_block: _blueprint/ux-blueprint_v<NN>.yaml# architecture
  solution_name: context.json# solution_name
output_format: md
---

## Arquitectura — {{solution_name}}

> **An architecture output shape for an architecture that is already justified.** This template does not
> select an option, assign an outcome, determine materiality, compare options or vendors, score an
> architecture, or re-decide anything Options settled. Authorization is **read** from the recorded
> `architecture:` block, never derived, upgraded or downgraded here. Positioning, the outcome-class
> reachability table and the architectability boundary live in `README.md` — this file lists no outcome
> class and owns no platform number.

<!--
RENDER CONTRACT — read once, then execute.

1. ENTRY. Render this file only where `architecture.authorization` is `authorized` or
   `authorized-bounded` for at least one scope. Where it is `not-authorized`, render nothing
   architectural: render the emitted outcome sentence, and the architectability reason where that is
   what failed — the two reasons stay distinct, and neither is relabelled `Decision Blocked`.

2. EXPERIENCE FRAGMENT — zero or one:
       architecture.experience.mode == none            → ZERO includes. Do NOT attempt to resolve
                                                         fragment-experience-none.md; it does not exist.
                                                         A4 is not engaged. No placeholder, no
                                                         missing-template warning, no render gap, no
                                                         `surface unresolved`. Log a `not applicable`
                                                         skip with the reason.
       architecture.experience.mode == owned-internal  → fragment-experience-internal.md
       architecture.experience.mode == owned-external  → fragment-experience-external.md
       architecture.experience.mode == inherited       → fragment-experience-inherited.md

3. BOUNDARY FRAGMENT — the repeat instruction, carried EXACTLY ONCE, here:

       for each qualifying recorded component:
           load fragment-boundary-and-imports.md
           bind that component
           render exactly one instance
           render six channels

   Qualifying = any `compositions[]` entry with `boundary: outside-platform`, or any composition
   beyond `direct`, or any `relocated_responsibilities[]` entry.

   Fragment keys:
       composition              → <scope>::component::<component>
       relocated responsibility → <scope>::responsibility::<responsibility>

   Invariant: N unique qualifying composition components + M unique relocated responsibilities
              ⇒ exactly N + M instances. Each key appears once; each instance carries six channels
              (Governance · ALM · Cost · Monitoring · Recovery · Operator), each populated or marked
              `not engaged — <reason>`. A missing channel is a defect;
              nothing is collapsed. Two entries in one scope sharing a `component` name is a
              CONTRACT DEFECT — fail; never merge, auto-suffix or overwrite.

   The scope prefix exists only for deterministic uniqueness. It is never rendered as engagement
   vocabulary.

4. CONDITIONAL SECTIONS. A condition that is not engaged renders as `not applicable` with its reason.
   That is a skip, NOT a missing required slot and NOT a render gap.

5. EVIDENCE. `Confirmed` renders as fact with `verificado_em` / `validade` (an expired row renders as a
   re-verification obligation, not as fact). `Assumed` renders as assumed, with basis and validity, and
   is never promoted. `Unknown` is never filled — it becomes an `open_architecture_choices` entry.
   `Conflicted` renders the conflict, carrying neither figure. `Risky` carries its accepted-risk id.

6. NUMBERS. This template owns no service limit, price, quota, retention window, threshold or SKU
   value. Where a volatile value is needed, resolve the engagement's verified SU row and render
   `value · verificado_em · validade · re-verify trigger`; where no verified row exists, render the
   verification obligation instead. The stable explanation stays in Domain Knowledge and is cited.

7. DOMAIN KNOWLEDGE. One relevant unit per architecture responsibility; read its decision-grade and
   architecture-grade sections; a second pull only where the first exposes a material dependency.
   Never preload the units, never assemble an architecture knowledge bundle, never survey all ten
   patterns. Cite the owning unit; do not copy it.
-->

### A1 — Authorização e âmbito

<the `(scope, outcome)` pairs, verbatim and UNCOLLAPSED — one line each; the decided option class in
plain language; the `D-NNN`. State what is authorized and what is explicitly not. Render
`architecture.authorization`, `authorization_basis` (the emitted outcome sentence, verbatim) and
`architectability_basis` (why this pack can architect the selected solution). For an
`authorized-bounded` scope, state which side is PP-owned and that the far side is not designed here.>

### A2 — Intenção arquitectural

<the requirement each structural choice answers. State the simplest-composition default, and per
escalation the named requirement that forced it (`compositions[].forced_by`). No scoring, no comparison,
no endorsement.>

### A3 — Contexto e fronteiras

**Tabela de fronteiras (obrigatória).** Every component in `compositions[]`, `record_authority[]` and
`relocated_responsibilities[]` appears **exactly once**. Nothing may appear in a picture that is absent
from this table.

| Componente | Papel | Governação da plataforma | Fronteira de confiança atravessada | Owner | Classificação de dados |
|---|---|---|---|---|---|
| <component / domain / responsibility> | <role> | <in-platform \| outside-platform> | <yes: which \| no> | <role or team \| UNKNOWN> | <classification> |

<then: the trust boundaries, and what sits inside versus outside platform governance.>

**Conditional — imagem de contexto**: engaged only where a composed or asynchronous path exists.
Otherwise `not applicable — <reason>`. One fenced block (Mermaid or ASCII), nodes = table rows, edges
labelled with direction **and** mechanism class, trust boundaries shown as grouping or annotation,
relocated responsibilities visually separated from the platform scope. It must degrade to readable text.
**No diagram is ever the authority**: a statement that exists only in a diagram is not in the blueprint.

**Conditional — sequência**: engaged only where an asynchronous or composed path exists (a status
resource, a reconciliation pass, a saga with an external pivot). Otherwise `not applicable — <reason>`.

### A4 — Aplicação e responsabilidades de superfície

<!--
CONDITIONAL. Engaged only where `architecture.experience.mode != none`, and rendered by the matching
experience fragment (step 2 of the render contract). Where the mode is `none`, this section is
`not applicable — arquitectura sem superfície humana (experience.mode: none)`: a finalized
architectural fact. Do NOT emit an empty A4, a `surface unresolved` note or a render gap.
-->

{{>> fragment-experience-<architecture.experience.mode>.md}}

### A5 — Autoridade de dados e stores

<per domain in `record_authority[]`: authority, store role, `access_mode`, grain, residency, retention
and the forfeits that access mode accepts. Cite the owning Domain Knowledge unit for every boundary
claim; restate none of it.

**An affirmative empty set is legitimate** where the solution does not own or introduce a persisted
business-data domain. Render the rationale explicitly, in the form:

> *No persisted record authority introduced; the workflow acts on external authorities and retains only
> operational execution state.*

**Missing evidence is never an empty set.** Where authority is undetermined, it is an
`open_architecture_choices` entry with `structural: true` — not an empty list, and not a silent default.>

**Dicionário de dados — dois sub-blocos, exclusivos por `access_mode`** (P-6; forma completa e
critérios por entidade em `docs/pp-pack-authoring/pilot/step-9a-onda-0-desenho-a5.md` §4, §8):

- `key` — slug único no scope (mesma regra de unicidade de `compositions[].component`);
  `entities[].authority` do blueprint aponta para ele. Uma entidade cuja `authority` não resolve, ou é
  `none — <razão>`, renderiza na §4 da Especificação como **lacuna** — nunca preenchida por analogia com a
  entidade vizinha, nunca enterrada numa célula de notas.
- `grain` (o que é uma linha) · `volume` (linhas · cadência, com locator L1 ou SU) · `schema_owner`
  (`value · state · su_ref · open`) — valores com estado, nunca afirmados acima da evidência.
- `owned` → `fields[]`: `name · name_basis · type · values · required · default · index · set_by · rules ·
  computed · lineage · state · source · disposition`.
- `keep-in-place` | `virtualized` → `access_contract`: `reads[] · writes[] · readonly · key[] · join_keys[] ·
  dictionary_entries_without_data[] · delegation_safe_paths[] · mandatory_filters[] · store_facts ·
  confidentiality · forfeits[]`. `replicated` leva ambos, com `fields ⊆ reads`. `writes: []` só com
  `readonly: true`; `key: []` só com `open: U-nnn`.
- **Estado por linha.** Toda a linha de `fields` / `reads` / `writes` carrega `state` (`Assumed` · `Confirmed` ·
  `Unknown`) e `source` (locator — `library/kernel/states.md` → *Confirmed threshold*). O rascunho vem do
  inventário L1 (`_capture/<workbook>.fields-draft.json`, motor `library/kernel/tools/fields_draft.py`, invocado
  por `aisa-blueprint` step 4) e entra `Assumed`; `Confirmed` só com declaração do dono (`answers.md#…`).
  `default` nunca é inferido. Toda a coluna do rascunho recebe `disposition` `ADOPT` / `MAP` / `DISMISS —
  <razão>` (princípio 10 do kernel): nada é promovido nem descartado em silêncio.
- **Sem limites de serviço** em `delegation_safe_paths` / `mandatory_filters`: cita-se a unidade de Domain
  Knowledge e a linha SU verificada (regra 6 deste contrato), nunca o literal.

*Forma de projecção na §4 da Especificação de Implementação* — uma linha por entidade, ligada ao domínio por
`entities[].authority`: *Entidade · Domínio (`key`) · `access_mode` e o que abdica · **owned**: campos (nome ·
tipo · obrigatório · default) / **externo**: lidas (n) · escritas (n) · chave · Relações (`join_keys`) · Índices
(`index` / `delegation_safe_paths`) · Estado (n `Assumed` / `Confirmed` / `Unknown` · dono do schema)*; sub-tabela
com as linhas. Os números (n campos · n lidas · n escritas · grão · volume) ficam **escritos** na §4: são o que a
Estimativa cita como `driver` (ela não lê `_capture/` nem a SU). Entidade sem autoridade → linha
`⚠️ lacuna — entidade sem autoridade de registo — dono: architecture — resolve-se com: <key> ou racionalização`
**e** entrada em `render-gaps.md`.

**Conditional — responsabilidade analítica / reporting**: engaged only where reporting forces a second
store or a copy. Otherwise `not applicable — <reason>`.

### A6 — Automação e integração

<per stream: mechanism class, guarantee, failure semantics, idempotency basis. An explicit `(none)` where
no stream exists. Where `experience.mode: none`, this section plus A7 typically carry the whole
architecture — describe it in full, and do not fabricate a user surface to sit above it.>

### A7 — Identidade e ponto de imposição da autorização

<!--
COMMON. Never owned by an experience fragment; a fragment may only SPECIALIZE the human-user part.
A headless architecture still requires this section in full.
-->

<the identity class **or** the service / managed / connection identity; the enforcement plane; the trust
boundary; secret and certificate custody where material; the role and permission model where a human
audience exists. Cite the security unit for what a control does and where it takes effect — CRAFT may
shape the *form* of a matrix and never the control's existence or reach.>

### A8 — Ambientes, governação e topologia de release

<environments, residency binding, policy plane, release route(s), and what is gated by a managed
environment. Where `experience.mode: inherited`, the inherited form of this section comes from the
inherited experience fragment.>

### A9 — Escolhas irreversíveis e saída

<ownership type, publisher, region / residency, first-party app installation, control generation, one-way
graduations, virtualization modelling, exit cost. One line per choice: what is fixed, when it is fixed,
and what it would cost to leave.>

**Conditional — substituição de um artefacto existente**: engaged only where the authorized scope
replaces an artefact that reached the migration-required outcome. Otherwise `not applicable — <reason>`.

### A10 — Operabilidade, suporte e modelo de operação

<the operating model as **roles and mechanisms**. For each failure path the architecture has, six things:
the `role` authorised to intervene · the `identity` it intervenes with · the `permission` that identity
needs · the `mechanism` that detects the failure · the `alert destination` that fact reaches · the
`recovery procedure`, with its order where order matters. Plus the support route, and — where the
composition replicates or copies data — the role that reconciles and the mechanism it reconciles through.

**No person.** Which individual holds a role is the organisation's to fill and changes without changing the
architecture; `not named` is a legitimate value here and produces no row, no risk and no gap.

**What counts as a structural open choice in this section**: the *operating model is absent* — a failure
path with no role authorised to intervene, or no diagnostic and recovery interface to intervene through.
That is a fact about the architecture: there is a way for it to break and no designed way to act on it, so
the shape of the architecture is not settled. It goes to A12 as `structural: true` and blocks approval.

An operator **without a name** is not that. Where role, permission, mechanism, alert destination and
recovery are stated, the section is complete and whoever holds the role executes it. A missing name never
blocked approval and must not be recorded as though it did.>

### A11 — Economia e consequências de entitlement

<entitlement class per audience, affected population, meters engaged, growth driver at the stated
horizon. **Drivers only — no prices, no SKU data, no quotas.**>

### A12 — Obrigações de prova e livro epistémico

<`proof_obligations[]` as *claim — level (V1–V4) — method — owner — funded?*, carried from the decision
and never re-derived. Then the `Assumed` / `Unknown` / `Conflicted` / `Risky` rows this architecture
rests on, with ids. Then every volatile value with `verificado_em` and `validade`. Then
`open_architecture_choices[]` as *choice — structural? — would be settled by — su_ref*.

A `structural: true` entry blocks **approval** of the blueprint; it does not block its **production**.
Use the existing open-question and SU epistemic mechanisms — no new state, no new outcome class, no new
phase and no new approval state machine.>

**Conditional — arquitecturas candidatas**: engaged only where a structural open choice leaves two
materially distinct architectures defensible inside one authorized scope. Render both, state what would
settle the choice, and choose neither. No scoring. Otherwise `not applicable — <reason>`.

**Conditional — propriedade de âmbitos (scope ownership)**: engaged only where more than one
`(scope, outcome)` pair exists. Otherwise `not applicable — <reason>`.

| Responsabilidade | Owner | Base de outcome | Descrita aqui? |
|---|---|---|---|
| <responsibility> | <this platform \| external owner> | <the emitted outcome sentence> | <yes — A4…A12 \| no — one boundary fragment instance> |

<A relocated responsibility gets a boundary, an owner and its imports — **never a PP design for the far
side**, and never an inferred comparator fit. Where the incumbent is the owner, `INCUMBENT FIT
UNEVALUATED` is preserved verbatim.>

### Obrigações importadas por componente de fronteira

<!--
CONDITIONAL. Engaged for each qualifying component (step 3 of the render contract). Where none
qualifies: `not applicable — arquitectura sem componentes de fronteira`. One instance per qualifying
component, all six channels each, nothing collapsed.
-->

{{>> fragment-boundary-and-imports.md}}   <!-- repeated once per qualifying component -->
