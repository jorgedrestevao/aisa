---
name: aisa-blueprint
description: Produce the UX blueprint (ux-blueprint_vNN.yaml) — the designed architecture and screen architecture derived from the Shared Understanding, the decision's authorized scope, and the pack's screen rules. The reasoning layer between domain knowledge and prototype generation; iterated with the business until approved (D-NNN). Draft mode (--option) supports /simulate during Options.
---

# aisa-blueprint

## Usage

`/blueprint [--option <O-NNN>] [--refresh]`

- No argument: requires `phase == decision` and a final `D-NNN` decision. Produces the next `_blueprint/ux-blueprint_v<NN>.yaml` for the chosen option.
- `--option <O-NNN>`: **draft mode** — allowed in Options phase; blueprints a candidate option (marked `draft: true`, never approvable). Used by `/simulate`. Pre-decision only.
- `--refresh`: shorthand after new `/answer` rows (e.g., prototype feedback) — re-runs against the updated SU and produces the next version.

The contract (schema, hard rules, versioning) is `library/kernel/blueprint-contract.md`. This skill is the executor of the pack's screen-consolidation rules — it **decides the design**; rendering the prototype happens outside aisa, from this artefact.

## Inputs (read)

- `<engagement>/_state.json`, `context.json`, `shared-understanding.md`, `frame.md`, `decisions.md`, `options.md` (draft mode), `lens-outputs/*.md`.
- `<engagement>/_coverage/` — the published coverage reviews (`library/kernel/coverage-contract.md`). Read through the motor (steps 1e, 13b, 15), never parsed by hand, and never edited: a record is immutable once published, and a new review is a new version.
- Pack knowledge (`<pack>` from `_state.json.pack`), **pulled selectively per the rules below — never preloaded**:
  - `library/packs/<pack>/architecture-templates/README.md` — the outcome-class reachability table and the architectability boundary. The **entry gate** reads this; no other file lists an outcome class.
  - `library/packs/<pack>/architecture-templates/architecture-core.md` — the **fixed** architecture output shape. There is one entry point and no per-decision template selection.
  - `library/packs/<pack>/domain-knowledge/craft/screen-consolidation-rules.md` — **the procedure** (field counts → screen types; role separation; approval-as-action; hard caps).
  - `craft/screen-patterns.md` — the screen-type catalogue, density rules, Excel Familiar Anchors.
  - `craft/security-craft.md` — the **form** of RBAC groups and the visibility matrix.
  - `data/query-and-delegation.md` (or pack equivalent) — the access-path constraints that shape list/search design. This is the platform authority for what delegates and what silently truncates; the `craft/` files never restate it.
- Previous blueprint version (if any) + `answers.md` (feedback already absorbed into the SU).

## Execution steps

1. **Pre-flight — the architecture entry gate.** Resolve the engagement; read `_state.json`.

   With `--option`: require `phase ∈ {options, decision}` and the option to exist in `options.md`. Draft mode is pre-decision only and skips steps 1c–1d (a draft records no authorization).

   **Draft mode is high-level, and it is high-level for every option equally.** It produces the shape `/simulate` needs to compare — screen count, patterns, entities touched, the main components and which side of the responsibility boundary each falls on. It does **not** produce the detailed architecture: no field-level data dictionary, no per-screen action set, no permission matrix, no integration contract. Those belong to the chosen option, after `/decide`. Detailing one candidate past its siblings does not sharpen the comparison — it manufactures the preference it appears to find, and it spends the engagement's budget on options nobody will build.

   Without `--option`: require `phase == decision` and a final `D-NNN`. Then run four mechanical steps:

   ```text
   read the decided (scope, outcome) pairs + the selected solution / composition, in plain language
     → check outcome reachability          (the frozen outcome, per architecture-templates/README.md §3)
     → check active-pack architectability  (the frozen selected solution × this pack's scope, §4)
     → initialize architecture.authorization + architectability_basis
   ```

   ```text
   architecture authorization = outcome reachability × active-pack architectability
   ```

   1a. Read the uncollapsed `(scope, outcome)` pairs and the selected option / composition from `decisions.md`. Never collapse a pair; never re-derive an outcome.
   1b. **Outcome reachability** per `architecture-templates/README.md` §3. Reachability alone is **never sufficient**.
   1c. **Active-pack architectability** per §4: *is the selected solution for this scope something this pack has the authority and knowledge to architect?* A PP application (any experience mode), a PP automation or integration composition, the **PP side** of a composed solution, or a capability this pack explicitly covers ⇒ architectable. A custom-only implementation, a packaged / SaaS product, a cloud-native-only architecture, incumbent internals, another platform's internals, or a candidate set with no selected architecture ⇒ **not** architectable.
   1d. **Initialize** `architecture.authorization` (`authorized` | `authorized-bounded` | `not-authorized`), `architecture.authorization_basis` (the emitted outcome sentence, **verbatim**) and `architecture.architectability_basis` (one sentence: why this pack can or cannot architect the selected solution).

   **This initialization is mechanical, not a new decision** — two inputs are frozen and the third is the active pack's own scope. It is **not** `/decide`'s to emit. After initialization the value is **read**, never derived, upgraded or downgraded.

   **No scope both reachable and architectable** ⇒ produce **no PP architecture**. Report the actual reason and keep the two distinct: *the outcome forbids one* versus *the selected solution is outside this pack's architecture authority*. Do **not** relabel either as `Decision Blocked` — that is an Options outcome class this skill may repeat and never derive. Preserve whatever the decision layer already carries (documented sufficiency, *this platform is not excluded*, the graduation trigger, `INCUMBENT FIT UNEVALUATED`) and infer nothing about the far side.

   **One or more bounded scopes architectable** ⇒ architect **only** those scopes.

   1e. **Reconciliation — the sources against the record, before anything is designed.** `library/kernel/coverage-contract.md` §8.1 requires a **current** reconciliation review before a version is produced. Run it **explicitly** — the hook is a convenience, never the mechanism, and a session where no hook fired loses visibility, not the check:

   ```
   python library/kernel/tools/coverage.py check --engagement <slug> --stage reconciliation --json
   ```

   - **exit 0** → complete and current. Open questions may remain — explicitly. Continue.
   - **exit 4** with `COV-NO-REVIEW` (no record) or `COV-STALE` (a source, an answer or the decision moved since the last review) → **do the review now**, then continue.
   - **exit 2** (schema) or **3** (engagement) → stop and say what is broken; never proceed on an unread check.

   Doing the review: `coverage.py inventory --engagement <slug> --json` gives the **denominator** — every unit of `context.json`, `enquadramento.md`, `answers.md`, the SU, the current solution decision, `inputs/`, `_capture/` and the phase artefacts. The motor builds it from the sources, never from what you write, so omitting a unit and its review line together does not produce a green. Write one `source_review[]` entry per unit or declared group (`reviewed` · `unverifiable` · `not_applicable`, each with its rationale) and one `coverage[]` entry per **material obligation**, with its disposition, the requirement it serves and what must happen to it. Then the two passes of §9 (described in step 13b). Draft to a temp file **outside the engagement**, then publish:

   ```
   python library/kernel/tools/coverage.py finalize --engagement <slug> --draft <tmp>/coverage-draft.json
   ```

   Three rules the executor does not break here:
   - **Reconcile upstream first, then snapshot.** Where the review finds an obligation the SU does not carry, the SU row is written first (through `/answer` or the lens path, preserving states and authority) and only then is the inventory re-read and the record finalized. Finalizing before the upstream change it describes stamps as reviewed a source nobody read in its current state.
   - **A routed gap still lets you produce.** A gap carrying `required_action` **and** `responsible_role` is eligible to produce a version for discussion; a gap with no owner and no next action is not, and neither is a dead reference or an unfinished review. `coverage: gaps` is what gets reported; `eligible: false` is what blocks — they are not the same line.
   - **Never invent an answer to close a gap.** A question that stays open stays open, and an insufficiency of the design is an execution gap, not a question for the business (`states.md` → *Admission of a question*).

   With `--option`: this step does **not** run. A candidate is not designed against a reconciliation of a solution nobody chose, and `draft: true` keeps the meaning contract rule 4 gives it — it is not, and never becomes, a marker for "produced with gaps".

2. **Author the `architecture:` block** (the contract, replacing the obsolete `branch` field). Facts serialized by `/decide` are read, not re-decided; `authorization` and `architectability_basis` come from step 1; everything else is architecture work.

   ```yaml
   architecture:
     scope: <the named scope, verbatim from the emitted (scope, outcome) pair>
     authorization: authorized | authorized-bounded | not-authorized
     authorization_basis: <the emitted outcome sentence, verbatim>
     architectability_basis: <why the selected solution is architectable by this pack>
     experience:
       mode: none | owned-internal | owned-external | inherited
       primary_surface: <a surface named in application/application-surfaces.md §3> | null
     record_authority:            # 0..N — empty ONLY with an affirmative rationale
       - domain: <entity or entity group>
         authority: <governed relational store | list/library store | relational via connector | external system of record>
         access_mode: owned | virtualized | replicated | keep-in-place
         su_refs: [...]
         key: <slug único no scope>   # P-6 — entities[].authority aponta para ele (unicidade como compositions[].component)
         grain: {row: <o que é uma linha>, dims: [<dimensões>]}
         volume: {rows: <n · unidade>, cadence: <diária|mensal|evento>, state, source}   # driver de P-10, com locator
         schema_owner: {value, state: Assumed|Confirmed|Unknown, su_ref, open: U-nnn}
         # exclusivo: owned (e replicated, com fields ⊆ reads)
         fields:
           - {name, name_basis: named_range|formula_ref|header|none|design, type: text|number|date|datetime|boolean|choice|reference|identifier|unknown,
              values: [...], required, default: null, index: primary|candidate|none, set_by: [...], rules: [...],
              computed, lineage: [...], state: Assumed|Confirmed|Unknown, source: <locator>, disposition: ADOPT|MAP|DISMISS}
         # exclusivo: keep-in-place | virtualized (| replicated)
         access_contract:
           reads:  [{name, aliases, name_basis, type, computed, lineage, by: [...], state, source, disposition}]
           writes: [{name, aliases, type, by: [...], cadence, write_semantics: insert|update|upsert|append, rules, state, source, disposition}]
           readonly: true|false            # true ⇒ writes: [] é afirmativo
           key: [<coluna(s)>]              # nunca vazio sem `open: U-nnn`
           join_keys: [...]
           dictionary_entries_without_data: [...]
           delegation_safe_paths: [...]    # cita DK, sem números de serviço
           mandatory_filters: [...]
           store_facts: {primary_key_type, primary_name_column, server_side_triggers, connection_identity}   # cada um {value, state, su_ref}
           confidentiality: {row_level: {value, state, su_ref}, column_level: {value, state, su_ref}}
           forfeits: [<o que o access_mode abdica — cita a unidade DK>]
     compositions:                # 0..N — names from architecture/patterns.md §5
       - component: <local, human-readable name, UNIQUE within this scope>   # required
         pattern: <direct | api-mediated | api-facade | event-driven | queue-based |
                   hybrid-low-code-pro-code | background-processing | data-virtualization |
                   data-replication | enterprise-boundary>
         forced_by: <the named requirement that forced this rung>            # mandatory
         boundary: in-platform | outside-platform
         owner: <named team or role> | UNKNOWN
         enclosing: true|false    # enterprise-boundary only
     relocated_responsibilities:  # 0..N — the scope-pair mechanism
       - responsibility: <name — UNIQUE within this scope; it is the identity>
         owner: <incumbent system | cloud-native services | named external team>
         outcome_basis: <the emitted class 3 or class 4 sentence, verbatim>
         markers: [INCUMBENT FIT UNEVALUATED, ...]
         gates_recorded: [operator, support, skills, cross-boundary-release-owner, maturity]
     proof_obligations:           # carried from the decision, never re-derived
       - claim: <what is being committed to>
         level: V1|V2|V3|V4
         method: <what will be run>
         owner: <role>
         funded: yes|no
     open_architecture_choices:   # 0..N
       - choice: <what is undecided>
         structural: true|false   # true ⇒ blocks approval, never production
         would_be_settled_by: <the fact, measurement or owner decision>
         su_ref: <U-NNN where one was opened>
   ```

   **Required**: `scope`, `authorization`, `authorization_basis`, `architectability_basis`, `experience.mode`, `compositions[]` (each with `component` **and** `forced_by`), `relocated_responsibilities[]` (may be empty), `proof_obligations[]`, `open_architecture_choices[]` (may be empty). `record_authority[]` is required **as a key** and may be empty. `experience.primary_surface` is required only where `experience.mode != none`. `imports` is deliberately **not** a field — imports are derived per component and carried structurally by the boundary fragment, so they cannot be declared satisfied by fiat.

3. **Experience mode — headless is a first-class outcome.** Answer the fork axis once and record it:

   ```text
   Is there a human-facing surface in this architecture at all?
     no  → mode: none          (headless)
     yes → does the solution own its own access model, lifecycle and capacity?
             no  → mode: inherited
             yes → is any part of the audience outside the directory?
                     yes → mode: owned-external
                     no  → mode: owned-internal
   ```

   Where `mode: none`: `primary_surface: null`, **zero** experience fragments, **no A4**, and **no** `surface unresolved`, empty A4, missing-template warning or render gap. `none` is a **finalized architectural fact**, not an Unknown — log it as a `not applicable` skip with its reason. **Never fabricate a user surface**, and never attempt to resolve `fragment-experience-none.md` (it intentionally does not exist). Steps 4–6 are then skipped and A6/A7 carry the architecture.

   Experience controls only experience-facing content. **It selects no architecture**, and it is orthogonal to composition.

4. **Compile the domain view from the SU** (no invention — ids or it doesn't exist):
   - `entities` ← `lens=data` rows (+ volumes from `lens=operations`), with state machines where approval flows exist. Each entity carries `authority: <record_authority[].key>` (the domain that owns its data) or `authority: none — <razão>` explicitly — never a silent gap.
   - **Fields and access contracts come from the L1 inventory, never from this skill's memory** (P-6, `docs/pp-pack-authoring/pilot/step-9a-onda-0-desenho-a5.md` §3–§4). Run the motor once per version (idempotent by the workbook's sha256):
     ```
     python library/kernel/tools/fields_draft.py --engagement <slug> --log
     ```
     It writes `_capture/<workbook>.fields-draft.json` — every populated column with `name` (`named_range → formula_ref → header → none`), `type`, `required`, `index`, `role` (`write` · `computed` · `no-data`), `lineage`, `rules`, its L1 `locator` and `state: Assumed` (or `Unknown` without a name or a type), plus the dictionary entries that point at columns without data. **Then judge, per column, and record the disposition in the record** (principle 10): `ADOPT` → the column becomes a `fields[]` line (domain `owned`) or a `reads[]` / `writes[]` line (domain external) of ONE `record_authority[].key`, `source` = the draft locator, state kept; `MAP` → an alias of a line already adopted (`maps_to`); `DISMISS — <razão>` → out of the to-be, reason written (a sheet that is a clone or a view, a parameter another system owns, an override the to-be does not admit). No column of the draft is left without a disposition, and no `fields[]` / `reads[]` / `writes[]` line exists without a `source`. `default` is never inferred; the split of metric vs port and counterparty vs technical prefix in the named-range dimensions is this skill's judgement, stated as such. The sponsor confirms (`/answer`), never the motor.
   - `personas` ← `lens=user` rows, mapped to access groups per `craft/security-craft.md`.
   - Constraints ← `lens=governance` rows (sensitivity, audit) and the platform boundaries owned by the pack's RESEARCH units for the responsibilities actually engaged.

5. **Run the consolidation tree** (`craft/screen-consolidation-rules.md`) over the field inventory per entity: derive each screen's type (from the pack catalogue), sections/tabs, role visibility, approval actions. Apply the pack naming convention.

6. **Design navigation**: home per persona, screen map. Prefer the shortest journey for the highest-frequency task (from `lens=operations` volumes).

7. **Decide the exclusions**: fields present in inputs/SU that must NOT appear (sensitivity, internal calc columns) → `excluded_from_ui` with reason + `su_refs`.

8. **Record authority — an empty set is affirmative or it is an open choice.** Where the solution does not own or introduce a persisted business-data domain, `record_authority: []` is legitimate **with** an explicit rationale, in the form:

   > *No persisted record authority introduced; the workflow acts on external authorities and retains only operational execution state.*

   **Missing evidence is never an empty set.** Where authority is undetermined, record an `open_architecture_choices` entry — `structural: true` where it decides the store — not an empty list and not a silent default.

9. **Component identity.** Every `compositions[]` entry carries `component`: human-readable, local to the architecture scope, **unique within that scope**, not globally stable, not canonical vocabulary, not a registry id. No UUIDs, no identifier subsystem. Examples: `erp-integration-api`, `crm-integration-api`, `dispatch-queue`, `document-processing-worker`, `analytical-copy`.

   Two components may legitimately share the same `pattern`, `owner`, `boundary` and even `forced_by` and still be two components. **Two entries in one scope declaring the same `component` name is a contract defect** — fail and give them distinct names; never merge, auto-suffix, overwrite or collapse their imports. Likewise `responsibility` must be unique within its scope.

10. **Fragment iteration.** Perform the iteration from recorded data — there is no loop primitive and none is added:

    ```text
    for each qualifying recorded component:
        load fragment-boundary-and-imports.md
        bind that component
        render exactly one instance
        render six channels
    ```

    **Qualifying** = any `compositions[]` entry with `boundary: outside-platform`, or any composition beyond `direct`, or any `relocated_responsibilities[]` entry. Keys: `<scope>::component::<component>` and `<scope>::responsibility::<responsibility>` — structure only, never rendered as engagement vocabulary.

    **Invariant**: N unique qualifying composition components + M unique relocated responsibilities ⇒ **exactly N + M instances**. Each key once; all **six** channels per instance (Governance · ALM · Cost · Monitoring · Recovery · Operator), each populated or `not engaged — <reason>`. A missing channel is a defect.

    A **relocated responsibility gets a boundary, an owner, its outcome basis and its gates — never a PP design for the far side**, and never an inferred comparator fit.

11. **Carry the open questions and structural choices.** Any design decision blocked by an Unknown goes to `open_questions` (never a silent default). If a NEW unknown emerges, append the `U-NNN` row to the SU first, then reference it. Record architecture-level uncertainty in `open_architecture_choices[]`.

    A `structural: true` entry **blocks approval of the version, not its production** — the blueprint is still produced. Structural examples: record authority; the authorization enforcement point; whether a responsibility leaves the platform; a composition where two materially distinct choices remain. On a composition, `owner` is the **role, team or organisation** that owns the far side, never a person: `<role> — not named` is complete, and a missing name is not an open choice of any kind. What is structural is a missing **operating model** — a failure path with no role authorised to intervene, or no diagnostic and recovery interface to intervene through (`architecture-core.md` A10). Where the organisation has not decided who owns the far side, that is a requirement of the to-be, cross-referenced to the simpler composition plus a tripwire the pattern unit already prescribes — never an availability verdict. Use the existing open-question and SU epistemic mechanisms: **no new state, no new outcome class, no new phase, no new approval state machine.**

    **Closing a structural choice — fact ≠ fit.** A `structural: true` entry may be marked resolved only when (i) the resolving evidence settles the fact named in its `would_be_settled_by` — not a narrower question answered sideways — and (ii) that evidence is ONE sufficient basis: **A** authoritative RESEARCH / Domain Knowledge (file + section) read against the engagement's material requirements, its exclusion and limitation list included; **B** engagement-verifiable technical evidence from an accountable source (a named mechanism, configuration or artefact — not a business sponsor's yes/no about connectivity); **C** a proof / measurement / spike result. A technical or configuration fact (a gateway is configured, a connection exists, a capability is documented) is an engagement fact, never a fit conclusion: record it, keep the choice open, and state what would settle it. Where the choice concerns record authority or access over an external store, the resolving basis names the **mechanism per data domain** and the pull rule below is executed for the one engaged pattern; `access_mode` and `pattern` are recorded per the mechanism actually established, never inferred from connectivity. **Capability confirmed ≠ fit confirmed**: where a documented limitation may defeat a material requirement (audit, row/column security, query shape, identity, write semantics), the capability may be Confirmed in the SU while the structural choice stays open until the requirement-level fit is recorded per domain. Where the current value depends on tenant or configuration (a policy, a gateway, an entitlement), Domain Knowledge alone is insufficient — basis B or C is required. No automatic web lookup, no three-source rule, no Domain Knowledge preload.

11b. **Cross-field architecture change — targeted revalidation.** When this version changes the value of an architecture-significant field recorded in the previous version — especially `record_authority[].authority` / `access_mode`, `compositions[].pattern`, `experience.mode` / `primary_surface`, the security or control boundary (authorization enforcement point, audit basis), or an integration mechanism — ask explicitly: **which existing architecture conclusions were materially based on the previous value?** Find them through what the record already carries: `su_refs` and `forced_by` naming the changed rows; rationale text naming the changed field or its property ("audit inherited from the store", "row security from the store"); `proof_obligations` and `open_architecture_choices` that assumed it; the decision's justification clauses and cited option strengths in `decisions.md` / `options.md`. Record the result — one line per conclusion, `still valid — <why>` or `revalidate — <what it assumed>` — in `blueprint-log.md` for this version, and where a conclusion is no longer settled: a `structural: true` `open_architecture_choices` entry (evidence insufficient), or a `proof_obligations` entry (a measurement settles it). No automatic reversal: the new fact makes the conclusion *not settled*, not false. No dependency graph, no registry, no new schema field. If a revalidated conclusion is part of the **Decision's** basis (a D-NNN justification clause, condition, or a strength the decision cites) → run the tripwire check and name `/revisit` in the output; architecture never rewrites the Decision.

12. **Validate the caps** (pack hard caps). Each violation: record in `validation.violations` AND append a Conflicted row to the SU (`partes: ux∧<lens>`), per the contract.

13. **Write** `_blueprint/ux-blueprint_v<NN>.yaml` (next version, never overwrite; `draft: true` + `option: O-NNN` in draft mode). **Then run the structural check** — `python library/kernel/tools/dashboard.py --blueprint-check <engagement>/_blueprint/ux-blueprint_v<NN>.yaml` (`blueprint-contract.md` → *Validação estrutural*; the `blueprint-validate.py` hook prints the same on the Write). Every `block` issue goes into this version's `validation.violations` (code · path · message) and into `blueprint-log.md`; the output line to the user says *esta versão não pode ser aprovada: <N> falhas estruturais*. A structural failure never stops the write — production is never blocked, approval is (step 15). Then append to `_blueprint/blueprint-log.md`: timestamp, trigger, SU ids consumed, violations (cap **and** structural), and — when an architecture-significant field changed value (step 11b) — the revalidation list (`still valid` / `revalidate`, one line each) and any structural choice closed in this version with its closure basis (A / B / C, cited). Append one line to `council-log.md`. Append one narrative episode to `<engagement>/story.md` (`## Episódio <N> — <data> — o desenho da aplicação (blueprint)`): 4-8 frases na voz do sponsor, sem jargão de kernel, máx. 2 ids citados. Create the file with `# Story — <slug>` if missing (pre-v2.3 engagements).

13b. **Coverage of the version just written — the second question, and never the same as the first.** Step 13 says the file is well formed. It says nothing about whether the design carries what the sources asked for: the case this mechanism exists for is a version the structural check calls `valid: yes (0 block, 0 warn)` that dropped a requirement the SU already carried. Two passes, both required for `semantic_review.status: completed` (`coverage-contract.md` §9):

    - **Source → target.** For each material obligation — request, invariants, clarifications, outputs **and their consumers**, the normal path, exceptions, permissions and segregation, data and calculations, integrations, failure and recovery, proofs — state the treatment and the **concrete point of this design** that carries it. An entity that mentions the subject is not a publication path, and a valid `su_ref` on a screen demonstrates nothing about whether the output is produced and consumed.
    - **Target → source.** For each material mechanism, rule or action proposed: confirmed requirement, explicit assumption, or design decision inside the authorized scope? This is the pass that catches invention, widened authority and implicit exclusion.

    Mechanics the motor verifies and will refuse: every `covered` needs a target that **resolves in this version** with a `role` pertinent to the stage — a link to an open question or a future proof is `proof_obligation` or `open_choice`, never implementation; every material requirement retired or altered needs `scope_basis_refs` naming the authority that allows it (dropping a mechanical calculation column from the UI may rest on design, dropping the business output may not); `partial` and `missing` are declared, never inferred from an absent field. Then publish and check:

    ```
    python library/kernel/tools/coverage.py finalize --engagement <slug> --draft <tmp>/coverage-draft.json
    python library/kernel/tools/coverage.py check --engagement <slug> --stage blueprint --target <engagement>/_blueprint/ux-blueprint_v<NN>.yaml --json
    ```

    **A version with gaps is produced, written and discussed — it is simply not announced ready for approval.** Record the gaps in `blueprint-log.md` for this version, beside the structural violations, with the same `required_action` / `responsible_role` the record carries. Do not repurpose `draft: true` to mean "incomplete": that field means *candidate before the decision* and its meaning does not move. Skip this step entirely in draft mode.

14. **Output** to the user:
   Business language (`CLAUDE.md` → *Duas línguas*); kernel labels and ids only between parentheses:
   ```user-output
   Desenho dos ecrãs — versão <NN> produzida.
   Âmbito autorizado pela escolha: <o que se constrói> — <autorizado | autorizado com limites | não autorizado> (<base, curta>).
   Como se usa: <aplicação para pessoas, superfície <qual> | sem ecrã humano — corre sozinho>.
   Quem manda em cada dado: <N> domínios com dono de registo <| nenhum, de propósito>.
   Peças que compõem a solução: <N> (<N> na fronteira com sistemas de fora) · responsabilidades movidas para fora: <M>.
   Ecrãs: <N> (<tipos>) · <N> perfis de utilizador · <N> entidades · campos fora dos ecrãs: <N> (lista em excluded_from_ui).
   Perguntas em aberto que condicionam o desenho: <nenhuma | <pergunta curta> (U-nnn) …>
   Escolhas de arquitectura ainda em aberto: <N> (<N> estruturais — sem elas o negócio não pode aprovar).
   Estrutura do desenho: <verificada, sem falhas | <N> falhas que impedem a aprovação (códigos entre parênteses) · <M> avisos>.
   O que foi pedido está todo no desenho: <sim — cada obrigação das fontes tem um ponto concreto no desenho | <N> por responder e <M> por fundamentar: <tema curto> (<id>) …> — lido nos dois sentidos, do pedido para o desenho e do desenho para o pedido.
   Pronto para levar à aprovação do negócio: <sim — só falta levares | não: <o que falta primeiro, em meia linha>>. Conferido não é aprovado: nada aqui aprova por ti, e aprovações antigas ficam como estão.
   Revisto por um campo ter mudado: <não se aplica | <campo>: <N> conclusões — <N> mantêm-se · <N> a rever · obriga a rever a decisão (/revisit): <sim | não>>.
   Limites do tipo de solução violados: <nenhum | <descrição curta> (X-nnn) …>.

   A seguir: gerar o protótipo a partir deste desenho e mostrá-lo ao negócio; registar o que disserem → `/answer`; refazer o desenho → `/blueprint --refresh`; quando aprovarem, diz-me — registo a aprovação (D-NNN) e esta versão fica fechada.
   ```

   Where no architecture was authorized, replace the architecture lines with the actual reason (outcome unreachable **or** selected solution outside this pack's architecture authority — stated separately), and say plainly that no PP architecture was produced.

15. **On approval** (user says the business approved v<NN>): run **two** mechanical checks, in this order, and let neither speak for the other.

    **(i) Structure** — `python library/kernel/tools/dashboard.py --blueprint-check <engagement>/_blueprint/ux-blueprint_v<NN>.yaml`. Exit 4 (any `block` issue) → approval is **refused mechanically** — list the issues (code · path · message) and what fixes each; no `AskUserQuestion`, no override: an invalid structure is an unfinished artefact, not a soft gate. A `structural: true` open architecture choice **blocks approval** — say which, and what would settle it. A structural choice marked resolved in this or an earlier version **without a recorded closure basis** (step 11: A / B / C, settling the fact its `would_be_settled_by` named) is not resolved — approval stays blocked and the version says so.

    **(ii) Coverage** — `python library/kernel/tools/coverage.py check --engagement <slug> --stage blueprint --target <engagement>/_blueprint/ux-blueprint_v<NN>.yaml --json`. A **new** approval requires, cumulatively with everything that already blocked (`coverage-contract.md` §8.1):
    1. a coverage review of stage `blueprint` that is **current** for **this** version — an approval of another version's review is `COV-AUTHORITY-MISMATCH`, not a substitute;
    2. `semantic_review.status: completed`, with both passes;
    3. no material requirement `missing` or `partial` without an authorized scope disposition;
    4. the structural blocks of (i);
    5. the explicit approval request to the business, which **no motor replaces**.

    `not_evaluated` is **not** a pass: an engagement that carries no review has not been reviewed, and the answer is to produce the review (step 13b), never to approve past it. `eligible: true` says the version may be **put** to the business — nothing more.

    **Then, and only then, ask.** The approval request goes through `AskUserQuestion` (CLAUDE.md, inviolable rule), with the version, what it commits to, and the open questions that remain visible in the options. A question in prose at the end of a reply is not a question asked, and silence is not an approval.

    On a clear yes: append the `D-NNN — Blueprint bp-v<NN> aprovado` block to `decisions.md` + the matching SU row, and note it in `blueprint-log.md` **with the coverage record the approval rests on** (`_coverage/coverage_vNN.json`) — the reference points from the approval to the review, never the other way round, so the approval cannot invalidate the review it consumes. Later renders read this version. Approvals already on file are never rewritten, superseded or revoked by this rule; where an older version was approved before the review existed, that approval stands and its coverage simply reads as not verified.

## Domain Knowledge pull rules

```text
architecture responsibility being described
  → pull ONE relevant knowledge unit
  → read its decision-grade and architecture-grade sections
  → populate the corresponding section
  → follow a second dependency ONLY where the first exposes a material import
```

Median 1 unit per section, **maximum 2**. **Forbidden**: preloading the pack's knowledge units; assembling an "architecture knowledge bundle"; opening `architecture/patterns.md` §5 in full to survey the ten patterns; a routing table keyed by section. For an engaged composition the pull is `architecture/patterns.md` §3 plus **the one** engaged pattern in §5, and a mechanism file only where necessary.

Reading decision-grade content is necessary and is **not** a licence to re-decide: the prohibition is on re-running selection, not on reading.

## CRAFT boundary

```text
RESEARCH             → establishes the technical boundary
architecture pattern → establishes the composition and its imports
CRAFT                → shapes implementation-facing blueprint detail
```

CRAFT **may** shape: screen consolidation, screen patterns and density, the **form** of the role and permission matrix, relational layering and naming where the store is relational-via-connector, delivery and solution naming conventions, and masking where a masking obligation already exists.

CRAFT **may not**: select the architecture, set an authorization, set record authority, establish a platform capability, establish a technical limit, or choose a proof level. `craft/estimation-model.md` is **not** used in the architecture blueprint. Where CRAFT and a RESEARCH unit disagree, **RESEARCH wins** and the CRAFT statement is a defect to report.

## No platform numbers

This skill and the architecture templates own no service limit, price, quota, retention window, threshold or SKU value. Where a volatile value is needed, resolve the engagement's verified SU row and carry `value · verificado_em · validade · re-verify trigger`; where no verified row exists, carry the **verification obligation** instead. The stable explanation stays in Domain Knowledge and is cited, never copied.

## Hard rules

1. Every node carries `su_refs`; a node without an anchor becomes an `open_questions` entry or is dropped.
2. Never overwrite a previous version; the approved version is frozen.
3. No prototype-tool specifics in the blueprint — platform constraints enter only via the pack's units.
4. Vendor naming is allowed here (post-Options), anchored to the **recorded architecture** — mirroring `lens-technology`'s rules.
5. Authorization is **read, never derived**. This skill initializes it once, mechanically, at the entry gate (step 1) from frozen inputs; nothing downstream upgrades or downgrades it, and no template selects itself.
6. There is **one** architecture entry point — `architecture-templates/architecture-core.md`. No branch, no per-decision template selection, no router.
7. **Fact ≠ fit.** A technical or configuration fact never closes a structural architecture choice by itself; closure needs basis A / B / C settling the named fact (step 11). Connectivity confirmed says nothing about which mechanism a surface uses over a store or whether that mechanism meets the material requirements.
8. **A premise change lists its dependents.** When an architecture-significant field changes value, the conclusions materially based on the previous value are named and marked `still valid` / `revalidate` in the log (step 11b) — never silently carried forward, never automatically reversed, never used to rewrite the Decision.
9. **The dictionary is drafted by the motor and judged here — never remembered.** Every `fields[]` / `reads[]` / `writes[]` line carries `state` and `source` (the L1 draft locator, an `answers.md` locator, or `design (<A-ref>)` for a field the architecture creates); every column of `_capture/<workbook>.fields-draft.json` receives `ADOPT` / `MAP` / `DISMISS — <razão>`; every entity carries `authority` (a `record_authority[].key` or `none — <razão>`). `default` is never inferred. A `Confirmed` line needs the owner's locator (`states.md` → *Confirmed threshold*); the motor's output is `Assumed` and stays so until then.
10. **Structure, coverage, approval and end-to-end are four questions.** A valid structure never meant a covered design; a complete coverage never meant an approval; an approval never meant the solution was proved end to end. Each is answered by its own check, reported on its own line, and none of them is ever announced on behalf of another. `not_evaluated` is the honest answer when no review exists — never "complete", never "failed", and never a reason to revoke an approval already recorded (`coverage-contract.md` §10).
