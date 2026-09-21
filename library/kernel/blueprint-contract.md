# UX Blueprint Contract — Kernel v0.2.0

The blueprint is the structured artefact that turns the engagement's knowledge into a designed application concept — **deciding the design** so any downstream renderer (Claude Design or other) only has to **render** it. It is produced by the `aisa-blueprint` skill in the Decision phase (see [`phases.md`](phases.md)) and iterated with the business until approved. This contract is platform-agnostic; screen catalogues, naming conventions and hard caps come from the active pack's `domain-knowledge/craft/` units (for `pp`: `craft/screen-consolidation-rules.md`, `craft/screen-patterns.md`, `craft/security-craft.md`). Platform boundaries that condition a design — what an access path can return, what a store enforces — come from the pack's `RESEARCH` units instead, never from `craft/`.

## Artefact and versioning

- Path: `<engagement>/_blueprint/ux-blueprint_v<NN>.yaml` — versioned, append-only (never overwrite; mirrors `_render/`).
- `<engagement>/_blueprint/blueprint-log.md` — one line per version: timestamp, trigger (initial / feedback round / re-run), SU ids consumed, cap violations raised.
- Approval: a `D-NNN` block in `decisions.md` ("Blueprint bp-v<NN> aprovado") + the matching SU row. The approved version is frozen; changes after approval produce a new version and a new approval.

## Schema (top-level keys)

| Key | Content | Source |
|---|---|---|
| `blueprint_id`, `engagement`, `concretizes_decision` | Identity + the D-NNN this blueprint concretizes | `_state.json`, `decisions.md` |
| `architecture` | The architecture this blueprint describes: the named `scope`; `authorization` and its two bases (the emitted outcome sentence, and why the active pack can or cannot architect the selected solution); the optional experience dimension (mode + optional primary surface); record authority per data domain (may be an affirmative empty set) — each domain with a `key`, its `grain` / `volume` / `schema_owner`, and its data dictionary: `fields[]` where `owned`, `access_contract` (`reads[]` · `writes[]` · `key[]` · …) where external, every line with `state` and `source` (P-6); compositions; relocated responsibilities; proof obligations; open architecture choices. **Value vocabulary — experience modes, surface names, composition names — belongs to the active pack, never to the kernel.** | initialized at blueprint entry (see below) + `decisions.md` + architecture work |
| `app` | name, device_targets, language | SU + context.json |
| `personas` | id, label, rbac_group, `su_refs` | SU `lens=user` + pack security patterns |
| `entities` | name, expected volume, state machine, `su_refs`, **`authority`** — the `record_authority[].key` of the domain that owns the entity's data, or `none — <reason>` explicitly (P-6; a silent gap is a §4 lacuna downstream) | SU `lens=data` (+ operations for volumes); `authority` from the `architecture.record_authority[]` block |
| `navigation` | home per persona + screen map | derived by the UX architect |
| `screens` | name (pack naming convention), pattern (pack catalogue), purpose, primary_persona, density, data (entity, primary/secondary columns), actions (primary/secondary), rbac_visibility, ui_states (loading/empty/error), platform constraint notes, optional `excel_anchor`, `su_refs` | pack consolidation rules applied to the SU |
| `excluded_from_ui` | fields deliberately NOT shown, each with reason + `su_refs` | SU (sensitivity, governance) |
| `open_questions` | Unknown ids that block design decisions | SU `## Unknown` |
| `validation` | pack hard-cap check result + violations list | pack consolidation rules |

## Entry gate

A blueprint requires an **architecture authorization for at least one scope**. That authorization is
**initialized at blueprint entry** from the frozen decision outcome and the frozen selected option,
against the active pack's architecture scope — and is never derived, upgraded or downgraded thereafter.
It is not a new decision: two inputs are already frozen and the third is the active pack's own scope.
The phase that produced the outcome owns it; the blueprint layer only reads it.

Where the entry gate yields `not-authorized`, **no blueprint version is produced**. The pair that
carries the meaning splits: the **outcome basis** remains in `decisions.md` (the emitted outcome
sentence, verbatim), and the **architectability basis** — whose **semantic owner is this entry gate's
own rule**, the recorded selected solution × the frozen active-pack architectability boundary — is
**durably carried** in `_synthesis/architecture-story.md` §*Authorized scope and outcome basis*, which
downstream deliverables read **as that carrier** and never as a source of architectural truth. No
deliverable re-evaluates pack architectability. This is the only carriage exception, and it does not
generalize to any other architecture field: **no new artefact, no empty blueprint, no new field.**

A blueprint **need not contain a human-facing surface**. An architecture with no human-facing surface is
a legitimate, finalized result — not an unresolved one — and produces no missing-surface gap.

## Hard rules

1. **Provenance everywhere.** Every screen, field group, action and exclusion carries `su_refs`. A node with no SU anchor is either removed or turned into an `open_questions` entry — the blueprint never invents.
2. **`excluded_from_ui` is first-class.** Deciding what NOT to show (sensitive fields, internal calculation columns) is a design decision with an id trail, not an omission.
3. **Cap violations become Conflicted rows.** When the pack's hard caps are violated (too many fields/actions/entities per screen), the blueprint records the violation AND the skill appends a Conflicted row to the SU. Resolution happens through the normal `/answer` path.
4. **Draft mode before Decision, and high level is the point.** `/blueprint --option O-NNN` during
   Options produces a `draft: true` blueprint for a candidate option (used by `/simulate`); drafts
   are never approvable. A draft carries the **high-level** shape only — screens, patterns, entities
   touched, the main components and which side of the responsibility boundary each falls on. It does
   **not** carry the detailed architecture: no field-level dictionary, no per-screen action set, no
   permission matrix, no integration contract. Those are produced for the **chosen** option, after
   the decision. Detailing one candidate past its siblings manufactures the preference it appears to
   find, and spends the engagement on options nobody will build.
5. **A structural open architecture choice blocks approval.** An architecture choice recorded as
   structural — one that decides the shape of the architecture rather than the shape of the build —
   blocks **approval** of a version; it never blocks its **production**. It uses the existing
   open-question and epistemic-row mechanisms: no new state, no new phase and no new approval state
   machine.

   **Which choices are structural is decided by the pack's architecture template, section by section,
   and recorded in the blueprint as `structural: true`.** The kernel reads the flag; it never derives
   it. Two consequences the kernel does hold: a missing *person* is never a structural choice — an
   authority the architecture needs is a role, and who fills it is the organisation's business — and a
   structural choice states what would settle it, so a version can be unblocked by evidence rather than
   by re-opening the decision.
6. **The renderer is replaceable.** Nothing in the blueprint may depend on a specific prototype tool. Platform specifics enter only through the pack's constraint notes.
7. **A new approval requires an applicable coverage review.** From the moment the coverage
   mechanism is active (`coverage-contract.md`), a version is **produced** against a current
   reconciliation and **approved** only with a current coverage review of that concrete
   version. Structure and coverage are two different questions and each blocks on its own
   terms; neither is an approval, and an approval is not a proof that the solution works.
   This rule governs the **next** approval, never the ones already recorded: a version
   approved before the mechanism existed keeps its approval, and its coverage simply reads
   as *not verified*. `draft: true` keeps the meaning rule 4 gives it and never becomes a
   marker for "produced with gaps" — a version with gaps is produced, written and discussed
   like any other; it is only not announced ready for approval.

## Validação estrutural

The structure of a version is checked **by code** before approval (`library/kernel/tools/dashboard.py::bp_validate`,
CLI `--blueprint-check <file>`, hook `.claude/hooks/blueprint-validate.py`). The motor reads presence, type and form; it
never decides what is structural, whether a closure basis suffices, or whether a `su_ref` points at the right row.

**Consequence of a `block` issue.** The version can be *produced* but not *approved* (`aisa-blueprint` step 15 refuses
mechanically — no soft gate, no override). An approval already recorded over a version that fails is **history, not a
source**: `blueprint_state.approved.valid = false`, and `render-validate.py`, `--authority-stamp` (exit 5, stamp
suffixed ` INVALID`) and the synthesis freshness treat it as *no approved version*. Existing engagements are reported,
never rewritten — but the rule itself carries **no exception by date** (owner decision, 2026-09-10): a version
authored before this check existed is judged by it like any other. A contract the runtime describes and does not
impose is not a contract.

### YAML subset the kernel reads (stdlib, no PyYAML — by design)

| id | form | note |
|---|---|---|
| Y1 | scalar `k: v` | null is `null` / `~` / empty **only**; **`none` is text** (the headless `experience.mode`); booleans `true/false/yes/no/on/off` (the template writes `funded: yes\|no`); quotes always win; `-?\d+` → int |
| Y2 | flow list `k: [a, b]` | bracket- and quote-aware split |
| Y3 | block list `k:` + deeper `- a` | |
| Y4 | list of maps `- k: v` + sibling keys | the item's mapping sits where its first key sits; a scalar first value cannot own key-shaped children |
| Y5 | flow mapping `k: {a: 1, b: [x]}` | **one** level of braces |
| Y6 | block mapping `k:` + deeper `k2: v2` | any depth |
| Y7 | block scalar `>` / `\|` | folded to one line |

Outside the subset and **signalled** (`BP-YAML-UNSUPPORTED`, never read in silence): anchors, aliases, tags, explicit
keys, nested flow mappings `{a: {b: c}}`, a second document. Tab indentation or a line that is neither `key:` nor `- `
→ `BP-YAML-MALFORMED` (the line is skipped, the rest is still read; a document that is not a map is `unreadable`).

### Codes

`block` prevents approval; `warn` is reported. Severity lives in one table (`BP_SEVERITY`) so it can be recalibrated
without touching the rules.

| code | severity | condition |
|---|---|---|
| `BP-YAML-UNSUPPORTED` | block | form outside Y1-Y7 |
| `BP-YAML-MALFORMED` | block | tab indentation, line without `key:`/`- `, document not a map |
| `BP-REQ-KEY` | block / warn | top-level key **absent**: block for `version`, `architecture`, `personas`, `entities`, `screens`, `excluded_from_ui`, `validation`, `engagement\|blueprint_id`, `decision_ref\|concretizes_decision` (non-draft); **warn** for `open_questions`, `navigation`, `app`. `pack.yaml: blueprint.required_keys[]` adds block keys |
| `BP-TYPE` | block | container present with the wrong type, **or** an unresolvable `SEE_Vnn` reference on `architecture` (the block was never read, so nothing was verified — a resolvable one is followed and the target validated);  — list expected and value is null/text/map; map expected and value is list/scalar. `[]`/`{}` are affirmative. A `SEE_Vnn` back-reference, or a delta map `{baseline: SEE_Vnn, changes_…: […]}`, is a valid container |
| `BP-ARCH-REQ` | block | absent in `architecture`: `scope`, `authorization`, `authorization_basis`, `architectability_basis`, `experience` (map), `experience.mode`, or one of the lists `record_authority`, `compositions`, `relocated_responsibilities`, `proof_obligations`, `open_architecture_choices` (empty is valid) |
| `BP-ENUM` | block | `authorization`, `experience.mode`, `record_authority[].access_mode`, `compositions[].boundary`, `proof_obligations[].level` outside their enumerations. A wrong **type** is a wrong value (`authorization: true` fires) |
| `BP-SURFACE` | block | `mode: none` with a `primary_surface`; `mode ≠ none` without one |
| `BP-COMP-REQ` | block | composition without `component`, `pattern`, `forced_by`, `boundary`; duplicate `component` |
| `BP-RA-REQ` | block | record authority without `domain`, `authority`, `access_mode`, `key`; duplicate `key`; `owned` without `fields` nor `access_contract`; `keep-in-place`/`virtualized` without `access_contract` |
| `BP-AC-KEY` | block | `access_contract.key` empty without `open: U-nnn` |
| `BP-RR-REQ` | block | relocated responsibility without `responsibility`, `owner`, `outcome_basis`; duplicate |
| `BP-ITEM-TYPE` | block | an item of a contract list that is not a mapping (`open_architecture_choices: ["…"]`, a null item). Skipping such an item is how a version whose structure was never checked passed as valid |
| `BP-NO-SUREFS` | block | node of `personas`, `entities`, `screens` (and their `actions`/`data` groups when they are maps), `excluded_from_ui`, `record_authority`, `open_architecture_choices` without a non-empty `su_refs` **or** `su_ref` (rule 1; singular and plural are equivalent) |
| `BP-LEAF-NO-SUREF` | warn | `{value, state: Assumed\|Confirmed}` leaf without `su_ref(s)` nor `source` |
| `BP-BAD-ID` | warn | token in `su_refs` that is not an id |
| `BP-DEAD-ID` | warn | id (`C A U X R RI CF D`) without a row in the SU — evaluated only with an engagement |
| `BP-STRUCT-TYPE` | block | `structural` present and not boolean |
| `BP-STRUCT-MISSING` | block | choice without `structural` — the classification is explicit or there is no approval (rule 5); the motor still never decides the value |
| `BP-STRUCT-NO-SETTLE` | block | `structural: true` without `would_be_settled_by` |
| `BP-RESOLVED-TYPE` | block | `resolved` present and not boolean |
| `BP-RESOLVED-NO-BASIS` | block | structural choice `resolved: true` without `closure_basis` (fact ≠ fit) |
| `BP-PO-REQ` | warn | proof obligation without `claim`, `level`, `method`, `owner`, `funded` |
| `BP-DRAFT` | block | `draft: true` — never approvable (rule 4) |
| `BP-VERSION` | block | `version` in the file ≠ `vNN` in the file name |
| `BP-NESTED-SPLIT` | warn | a list item that is a bare id — the symptom of the pre-1.13.0 reader, kept to flag artefacts it produced |

### O carimbo de autoridade do `architecture-story`

`_synthesis/architecture-story.md` abre com o carimbo que nomeia a versao cuja `architecture`
projectou. Reconhecer a FORMA do carimbo nao e verifica-lo, e `SYN-STAMP`
(`dashboard.py::synthesis_check`) verifica:

- a versao carimbada **existe** em `_blueprint/`;
- **corresponde** a autoridade do engagement (a aprovada, ou a ultima autorizada);
- essa versao esta **autorizada** (`authorized` | `authorized-bounded`);
- o `sha256` corresponde ao bloco `architecture` actual — e um digest que nao e um digest
  (menos de 64 hex) e sinalizado, em vez de ler como *carimbo sem sha*;
- a versao passa a **validacao estrutural** acima.

**O caso sem arquitectura** (a entry gate deu `not-authorized`, e nenhuma versao foi
produzida) escreve-se `authority: none — <razao>`, com a razao em
{`outcome-forbade`, `outside-pack-authority`}. A base documental sao os pares
`(scope, outcome)` que `aisa-decide` serializa, e a validacao tem **alcance estrutural** —
falta de informacao e uma coisa, inconsistencia verificavel e outra, e o motor nao as junta:

| estado registado | resultado |
|---|---|
| sem decisao de solucao, ou sem bloco de pares | **nao avaliado**, com o motivo. Nunca apresentado como verificado |
| bloco presente sem um unico par completo, ou linhas que nao sao pares | **`SYN-STAMP`** — dados malformados, nao ausentes |
| existe versao autorizada em disco | **`SYN-STAMP`** — contradicao verificavel; nunca convertida em nao avaliado |
| `outside-pack-authority` sem `Selected solution / composition` | **`SYN-STAMP`** — essa razao fala da solucao seleccionada |
| >= 1 par completo (e a solucao, quando a razao a exige) | limpo, com **nota**: a base documental existe, o *significado* da razao nao foi avaliado |

QUAL das duas razoes se aplica continua a ser da skill: separa-las exige ler a frase do
outcome contra a fronteira de architectabilidade do pacote, que hoje e prosa. Torna-la
legivel pelo motor e uma evolucao declarada, nao um pressuposto desta verificacao. A
presenca dos dados e o criterio: a geracao do engagement nunca se infere pela data nem pela
versao.

## Cobertura — a segunda pergunta sobre a mesma versão

A verificação estrutural acima responde *o artefacto está bem formado?*. Ela nunca respondeu
— e nunca poderia responder — *o desenho carrega o que as fontes pediram?*. O caso que obrigou
a separá-las é literal: uma versão com `valid: yes (0 block, 0 warn)` que tinha deixado cair um
requisito que a Shared Understanding já carregava. Estrutura verde e cobertura são coisas
diferentes, e juntá-las num veredicto só esconde qual das duas disse que sim.

A definição normativa da cobertura — esquema, etapas, locators, atualidade, códigos e regra de
passagem — vive em [`coverage-contract.md`](coverage-contract.md) e **não se duplica aqui**. O
que este contrato fixa é a sua ligação ao desenho:

| momento | o que se exige | onde |
|---|---|---|
| antes de produzir uma versão | reconciliação completa e **actual**; lacuna com dono e próxima acção pode seguir | `coverage-contract.md` §8.1 |
| depois de produzir | verificação estrutural **e** revisão de cobertura da versão concreta | idem |
| para uma **nova** aprovação | as duas acima, `semantic_review: completed`, nenhum requisito material `missing`/`partial` sem autoridade de âmbito, os bloqueios estruturais da regra 5, e o pedido explícito ao negócio | idem |

Quatro perguntas, quatro respostas, nunca uma: **estrutura** · **cobertura** · **aprovação** ·
**ponta-a-ponta**. `not_evaluated` é a resposta honesta de quem não tem revisão nenhuma — não é
aprovação, não é reprovação, e não revoga aprovação nenhuma já registada
(`coverage-contract.md` §10). A aprovação **refere** a revisão que consumiu; a revisão nunca
refere a aprovação, para que aprovar não invalide a revisão que a sustenta (§6.4).

## Downstream consumers

- `solution-blueprint` (Architecture Blueprint) deliverable: renders the `architecture:` block of the **latest authorized** version and declares whether that version is approved — the one deliverable that may show a version a structural choice still blocks (hard rule 5), with both candidates and neither chosen (P-18 / F08).
- `claude-design-brief` deliverable: renders its screen/navigation/UX sections from the **approved** blueprint.
- `implementation-spec` deliverable: `screens_to_build` comes from the approved blueprint — what gets built is what the business validated.
- `/simulate`: uses draft blueprints per option for the side-by-side comparison.
- Future traceability (post-handoff): the `su_refs` stamped here are the join key for spec-vs-implementation diffing.
