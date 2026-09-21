---
name: aisa-render
description: Render the 6 (or a specific) deliverable(s) for the engagement by EXECUTING each deliverable template's projection contract against the architecture record, _synthesis/, the Shared Understanding, decisions and context. Writes versioned files to _render/. Missing required slots are logged to render-gaps.md; not-applicable deliverables are logged as skips to render-log.md (no silent failures, and skips never pollute the gap file). Supports --all and --dry-run.
---

# aisa-render

## Usage

`/render [<deliverable>|--all] [--dry-run]`

- `<deliverable>`: render only one — `discovery-report`, `executive-report`, `solution-blueprint`, `implementation-spec`, `claude-design-brief`, `estimate`.
- `--all`: render every deliverable declared in `library/packs/<pack>/pack.yaml` **whose activation holds** (see *Declarative activation* below). This is the default after `/decide` → `/synthesize`.
- `--dry-run`: resolve slots and surface gaps without writing to `_render/`. Useful for debugging templates without bumping versions.
- `--html`: additionally produce `<slug>_discovery-report_v<NN>.html` — the interrogable projection: self-contained HTML (inline CSS, ZERO external requests), every SU id citation rendered as `<span class="prov" title="<estado> · <evidência> · verificado <data> (<validade>)">C-014</span>`, a top banner ("documento gerado do Shared Understanding — cada afirmação é rastreável") and a final **Proveniência** section with the id → lens → evidência → validade table. v3.0 scope: discovery-report only (other deliverables in v3.1).

## What this skill is

**The executor of six projection contracts** — and nothing more.

```text
Shared Understanding → Decision → Architecture → Deliverable projections
```

> **Render executes a projection contract; it does not reason beyond that contract.**

The template **declares**; this skill **executes**; neither reasons. See `library/kernel/render-contract.md` for the binding layer contract.

### What this skill MAY do

Assemble · validate · log · fail loud · and **execute only the projection transformations the active deliverable contract declares in its `permitted_transformations`**, including the deterministic bounded derivations the Implementation Specification, the Claude Design Brief and the Estimate require.

A transformation is executable exactly when it is **deterministic**, **bounded**, **declared by the active contract**, and **traceable to an already-authoritative input**. Fail any of the four and it is reasoning — refuse it and log an open work item.

### What this skill MAY NOT do

Create new upstream facts · choose an option · choose or change architecture · change scope · resolve an Unknown · promote epistemics · invent work · re-source evidence to re-settle an upstream fact · create a comparator claim · re-grade a proof obligation · mark a condition satisfied · design a far side · blend candidate estimates.

**This skill is not an inference engine.** No new engine, no new skill, no new estimation agent is introduced.

## Phase gate (soft)

The engagement should be at `phase == decision` with `_synthesis/` populated (5 topic packs). Earlier `/render` attempts are allowed but most slots will be empty and `render-gaps.md` will scream. See `.claude/rules/render-on-decision-only.md`.

If `phase != decision` AND `--dry-run` is **not** set → stop with: "Render before /decide is forbidden by `.claude/rules/render-on-decision-only.md`. Use `--dry-run` to preview, or finish the engagement first."

## Declarative activation

Each deliverable declares its own applicability. Read it from the template frontmatter (`activation`, `blocked_when`, `not_applicable_when`), with `pack.yaml`'s `activation` as the manifest mirror. **There is no router**, no outcome→template map and no concern→deliverable map: the fields are read, not dispatched on.

| State | Behaviour |
|---|---|
| **required** | render it |
| **conditional** | render the applicable part and **state which part** |
| **not applicable** | **do not produce it**; log a **skip** with the reason to `render-log.md`. **Never** an entry in `render-gaps.md` |
| **blocked** | do not produce it; log the block with its reason **and what would unblock it** |

### The situations, and what each produces

| Situation | Discovery | Executive | Arch Blueprint | Impl Spec | Design Brief | Estimate |
|---|---|---|---|---|---|---|
| PP authorized | required | required | required | required | conditional ¹ | conditional ² |
| PP authorized-bounded | required | required | required (PP side only) | required (PP side only) | conditional ¹ | conditional ² |
| PP not-authorized | required | required | **not applicable** | conditional ³ | **not applicable** | conditional ⁴ |
| **Decision blocked (class 12)** | required | required | **not applicable** | **not applicable** | **not applicable** | **not applicable** |
| Headless (`experience.mode: none`) | required | required | required | required | **not applicable** | conditional ² |
| Structural open choice | required | required | required — both candidates, neither chosen | **blocked** | **blocked** | conditional ⁵ |

1. `required` where `experience.mode ∈ {owned-internal, owned-external}`; `conditional` (narrowed to what the solution may shape) where `inherited`; **`not applicable`** where `none`; **`blocked`** where no **approved** UX blueprint exists.
2. Estimation authority is platform-scoped: work outside it is **excluded with a reason**, never guessed.
3. `not applicable` for the non-authorized scope; **produced** for any other scope that does carry a PP authorization. With no such scope: not produced.
4. Produced only if the selected implementation is inside this pack's estimation authority; otherwise `not applicable` with the reason — *this pack has no estimation basis for the selected solution class*. Never a comparative or placeholder number.
5. Mode B only (see *Estimate input modes*): either not produced, or one **separately labelled** estimate per candidate.

### Structural blocking is mechanical

```text
open_architecture_choices[] has structural: true
→ blueprint APPROVAL blocked            (blueprint-contract.md hard rule 5)
→ no approved UX blueprint
→ Implementation Specification BLOCKED
→ Claude Design Brief BLOCKED
```

**No new machinery.** And **no exception**: no materiality override, no partial approval, no UX-only approval. A judgement that "the unresolved choice is not UX-material, so the brief can proceed" is **wrong** — the brief's required source does not exist. The Architecture Blueprint still renders, with **both** candidates and **neither chosen**.

### Which blueprint version each deliverable reads (P-18 / F08)

Version selection is **explicit per deliverable** and read from the template (`blueprint_version_read` / `slot_sources`), never "the newest file in `_blueprint/`":

| Deliverable | Reads | Declares |
|---|---|---|
| Architecture Blueprint (`solution-blueprint`) | `v<latest authorized>` — the latest non-draft version whose `architecture.authorization` is `authorized` or `authorized-bounded` for at least one scope | its approval state: `aprovada (D-NNN)` · `não aprovada — N escolha(s) estrutural(is) em aberto` · `não aprovada — aguarda aprovação do negócio` (`architecture_version_state`) |
| Implementation Specification · Claude Design Brief | `v<approved>` — the version the latest `Blueprint bp-v<NN> aprovado` D-NNN names | blocked while none exists **or while the approved version fails the structural check** (`dashboard.py --json` → `blueprint.approved_valid = false`; `render-validate.py` then records the gap and names the codes — refazer o desenho → `/blueprint`) |

Why two rules: the candidate-architectures section exists **only** while a structural choice is open, and that same choice blocks approval — a `v<approved>` source could never carry what the Architecture Blueprint must show. Authorization is a recorded architecture fact; approval is a human decision. `dashboard.py --json` publishes both (`status.blueprint.approved`, `status.blueprint.latest_authorized`); read them, never re-derive.

### Not-authorized: two distinct reasons

```text
outcome basis           semantic owner: the Options layer that emitted the sentence
                        durable source: decisions.md

architectability basis  semantic owner: THE ARCHITECTURE-ENTRY GATE RULE
                        durable carrier: _synthesis/architecture-story.md
```

Read the architectability basis **as the durable carrier of an architecture-entry result** — never as architecture authority. **Never re-evaluate pack architectability here.** For a positive non-PP decision: preserve the decision, preserve the architectability reason, do **not** call it *Decision Blocked*, do **not** imply this platform lost, and infer **nothing** about the selected solution's fit or cost.

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/frame.md`.
- `<engagement>/_synthesis/*.md` (the 5 topic packs).
- `<engagement>/_blueprint/ux-blueprint_v<NN>.yaml` — the blueprint version the active contract names: `v<approved>` for the Implementation Specification and the Claude Design Brief; `v<latest authorized>` for the Architecture Blueprint (see *Which blueprint version each deliverable reads*). Its `architecture` block is the architecture record.
- `<engagement>/_capture/evidence-index.md` — the source inventory for the Discovery Report.
- `<engagement>/_coverage/` — the published coverage reviews (`library/kernel/coverage-contract.md`). Read **through the motor** (steps 2b and 9b), never parsed by hand, and never edited: a record is immutable once published, and a new review is a new version.
- `library/packs/<pack>/pack.yaml` (lists the deliverables + activation mirror).
- `library/packs/<pack>/deliverable-templates/<id>.template.md` (one per deliverable).
- `library/packs/<pack>/architecture-templates/architecture-core.md` — the **fixed** architecture entry point. No branch, no per-decision template lookup, no dynamic path, no router. Plus, resolved from the recorded `architecture` block: **zero or one** `fragment-experience-<mode>.md`, and **zero or more** instances of `fragment-boundary-and-imports.md`.
- `library/packs/<pack>/domain-knowledge/craft/estimation-model.md` — the Estimate's **method** authority (method only, person-days).
- Any other domain-knowledge unit a template cites **at its point of need** (never a preload, never a catalogue scan).

`<engagement>` resolves to `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, otherwise `projects/<slug>`. `<pack>` is read from `_state.json.pack`.

**`options.md` is deliberately absent as a whole-file source.** No deliverable reads it whole — that invites a re-staged comparison. The Executive Report projects the decision's own recorded justification and per-alternative *why not* lines from `decisions.md`.

## Source-contract validation

Before resolving slots, validate the active template's contract:

1. Every `authority_sources` / `conditional_sources` entry a required slot depends on is **reachable**. Unreachable + required → gap. Unreachable + conditional whose condition does not hold → skip.
2. **No slot resolves from a `forbidden_sources` entry.** A slot source that names a forbidden artefact is a **contract defect**: fail loud, log it, and do not silently substitute.
3. Every `{{slot}}` in the body is declared in `required_slots ∪ conditional_slots ∪ optional_slots`, and every declared slot appears in the body.
4. `permitted_transformations` is present on every contract that needs a computed slot. A computed slot with no matching declared transformation is a **contract defect** — refuse the computation.

## Outputs (written)

- `<engagement>/_render/<slug>_<deliverable>_v<NN>.md` — versioned, append-only (never overwrites a previous version). `<NN>` is `01`, `02`, …, the next available integer.
- `<engagement>/_render/render-gaps.md` — every missing **required** slot encountered in this run, with the deliverable, the resolution attempt and the **owner**. Append-only.
- `<engagement>/_render/render-log.md` — per-run audit: timestamp, deliverables rendered, **deliverables skipped with their reason**, deliverables blocked with what would unblock them, version per file, gap count.

## Slot resolution order

For each `{{slot}}`, resolve in this order (per `library/kernel/render-contract.md`):

1. `_synthesis/<topic>.md` section (when the template's `slot_sources` declares it).
2. The **architecture record** + the fixed architecture shape (where declared).
3. The relevant Shared Understanding section (`Confirmed`, `Assumed`, `Unknown`, `Conflicted`, `Risky`), filtered by lens or row id when declared — carrying **state**, `verificado_em` and `validade`.
4. `decisions.md` (D-NNN fields).
5. `context.json`.
6. **Computed** — only where the active contract's `permitted_transformations` declares the derivation.
7. Otherwise: `required` → log a gap and render `> ⚠️ missing: <slot> (see render-gaps.md)`; `conditional` whose condition does not hold → **omit and log a skip**; `optional` → omit.

Sub-template includes (`{{>> path/to/sub.md}}`) recursively resolve the same way, with the sub-template's own `slot_sources`.

When no scope carries an architecture authorization and a still-applicable template includes `{{>> architecture-templates/…}}`, replace the include with a one-line note stating the **actual** reason — `> Sem arquitectura autorizada: <outcome forbade one | selected solution outside this pack's architecture authority> (ver decisions.md#D-NNN)` — and do not log a gap. Keep the two reasons distinct, and do not relabel either as *decision blocked*.

## Epistemic execution rules

**Deliverable brevity cannot upgrade epistemics.** Binding for every slot this skill fills:

- An `Unknown` may be **omitted** where immaterial for that audience, and the omission is **counted in a residual line** — never rewritten as a fact or an assumption.
- A `Conflicted` row renders the conflict **or** omits the value. **Choosing a side is prohibited** in every deliverable, at every altitude, with or without a caveat.
- An **expired** `Confirmed` never renders as fact anywhere, including the Executive Report — it renders as a re-verification obligation.
- `Assumed` never becomes `Confirmed`. `Risky` keeps its accepted-risk identity: an accepted risk is not a mitigated risk.
- Every rendered **volatile value** carries `value · verificado_em · validade`, or renders as a verification obligation where invalid or expired. Never introduce a live platform fact, and never treat a template as a fact store.
- **Proof obligations** are quoted in their five-part shape (*claim · level V1–V4 · method · owner · funded?*). This skill never changes the level, the method, the owner or the funded state, and never marks one satisfied.

## Scope-pair projection

Where `authorization: authorized-bounded`, or wherever more than one `(scope, outcome)` pair exists:

- Project the pairs **UNCOLLAPSED**, each outcome sentence **verbatim**, every marker preserved (`COMPARATIVE FIT UNEVALUATED`, `INCUMBENT FIT UNEVALUATED`, documented sufficiency, graduation triggers).
- Project the **four scope-ownership render categories** — architected here · relocated, boundary represented · **excluded, destination unevaluated** · not applicable, no architecture authorization. They are render categories, not states, not outcome classes, not epistemic values. No fifth category; none inferred from another.
- **Category 3 gets nothing**: no owner invented, no boundary component, no imports, no gates, no far-side design, and **no estimate line, allowance, placeholder or contingency band**. The exclusion is **stated**, not silent.
- Executive names both sides and their markers; the Blueprint architects the PP-owned side only; the Spec's build scope is the PP-owned side only; the Design Brief designs PP-owned surfaces only; the Estimate prices PP-owned work only.

**The far side never enters PP scope by silence.**

## Execution steps

### For each deliverable to render:

1. Read the template. Parse the frontmatter: `canonical_deliverable`, `activation` / `blocked_when` / `not_applicable_when`, `authority_sources`, `conditional_sources`, `forbidden_sources`, `permitted_transformations`, `forbidden_transformations`, `required_slots`, `conditional_slots`, `optional_slots`, `slot_conditions`, `slot_sources`, `sub_templates`, and (Estimate only) `owns_calculation` + `input_modes`.
2. Evaluate activation. `not applicable` → **skip**, log the reason to `render-log.md`, continue. `blocked` → log the block + what would unblock it, continue.
2b. **Pre-render — the authorities this deliverable needs, before producing anything.**
   `coverage-contract.md` §8.2 requires the authorities **that** deliverable declares to be
   current, and §8.3 requires the version it reads to be the one its own template names. Run
   it explicitly — the hook is a convenience, never the mechanism:

   ```bash
   python library/kernel/tools/coverage.py check --engagement <slug> --stage render --deliverable <id> --json
   ```

   Read three things, and do not collapse them into one:

   - `expected.version` / `expected.state` — the version this deliverable must read, and why
     it exists or does not. `available` → that is the version to open. `no-authorization`,
     `not-approved` and `structurally-blocked` are **three distinct reasons**, and each is the
     reason line of a **skip**, not a gap: an authority that does not exist yet is `blocked`
     or `not applicable` (step 2), never `render-gaps.md`.
   - `upstream` — the reconciliation or blueprint review this deliverable consumes.
     `not_evaluated` means no review exists: report it as *not verified*, never as failed, and
     never as a reason to revoke an approval already on file (§10). `eligible: false` means the
     upstream review is open — produce for discussion if you must, and do **not** announce the
     deliverable as complete.
   - `diagnostics` — a `COV-SCHEMA` here is a defect of the **template**, not of the
     engagement (a missing or unknown `blueprint_version_read`, or a template with no
     `template_id`). Fix the contract; do not guess the version. A
     `COV-AUTHORITY-MISMATCH` means the template named is **another deliverable's**: the
     version it declares is not this deliverable's authority, and no version is resolved
     from it. Point at the right template; never borrow one that happens to resolve.

   The motor reports facts; the template's `activation` / `blocked_when` /
   `not_applicable_when` decide. Never derive applicability from the coverage result.

3. Run *Source-contract validation* (above).
4. For each slot in `required_slots ∪ conditional_slots ∪ optional_slots`:
   a. Evaluate its `slot_conditions` entry, if any. False → **not applicable**: omit, log a skip, next slot.
   b. Look up `slot_sources`; walk the resolution order; capture the resolved text or `MISSING`.
5. Substitute slots. For the architecture sub-template reference:
   a. Read the **fixed** entry point `library/packs/<pack>/architecture-templates/architecture-core.md`. No inner slot is resolved into the path; there is nothing to select.
   b. Read the architecture record. Render the core only where `authorization` is `authorized` or `authorized-bounded` for at least one scope. Authorization is **read** here — **never derived, upgraded or downgraded** (`blueprint-contract.md` owns its initialization at blueprint entry).
   c. **Experience fragment — zero or one:**
      ```text
      experience.mode == none           → ZERO includes. Do NOT attempt to resolve
                                          fragment-experience-none.md; it does not exist.
                                          No A4, no placeholder, no missing-template warning,
                                          no render gap, no `surface unresolved`.
                                          Log a `not applicable` skip with the reason.
      experience.mode == owned-internal → fragment-experience-internal.md
      experience.mode == owned-external → fragment-experience-external.md
      experience.mode == inherited      → fragment-experience-inherited.md
      ```
   d. **Boundary fragment — zero or more instances.** The skill performs the iteration; there is no loop primitive and none is added:
      ```text
      for each qualifying recorded component:
          load fragment-boundary-and-imports.md
          bind that component
          render exactly one instance
          render six channels
      ```
      **Qualifying** = any `compositions[]` entry with `boundary: outside-platform`, or any composition beyond `direct`, or any `relocated_responsibilities[]` entry.

      **Component identity.** `component` is required on every composition, and is unique within the architecture scope; `responsibility` is the identity for a relocation. Fragment keys are `<scope>::component::<component>` and `<scope>::responsibility::<responsibility>` — structure only, never rendered as engagement vocabulary. Two components may legitimately share pattern, owner, boundary and forcing requirement and still render separately. **A duplicate `component` (or `responsibility`) within one scope is a contract defect: fail loud and log it.** Never merge, auto-suffix, overwrite or collapse imports.

      **Invariant**: N unique qualifying composition components + M unique relocated responsibilities ⇒ **exactly N + M instances**. Each key appears once; each instance carries all **six** channels (Governance · ALM · Cost · Monitoring · Recovery · Operator), each populated or `not engaged — <reason>`. **A missing channel is a defect**, not an omission.
   e. Recursively resolve each fragment's slots from the engagement.
6. **Headless (`experience.mode: none`)** — for the Implementation Specification: emit **no** required screens, **no** persona section, **no** navigation, **no** UX placeholder. Still project automation, integration, identity and enforcement, environments and release, monitoring, recovery, proof work and operator obligations **in full**. For the Claude Design Brief: the deliverable is **not applicable** — do not emit a persona, screen, navigation or UX-state slot, and do not emit a gap.
7. **Estimate — execute the bounded calculation** (see below), where and only where `owns_calculation: true`.
8. Compute the next version `<NN>`. Write `<engagement>/_render/<slug>_<deliverable>_v<NN>.md` unless `--dry-run`.
9. Append gaps to `render-gaps.md` with deliverable + slot + attempted source + **owner**. Then **read the
   `## Validação …` block `render-validate.py` appended for the file just written** (P-7 — the hook checks the
   template's `sufficiency:` rules by content: §4 dictionary and `authority` per entity, §6 `(none)` while an entity
   carries `state_machine` / `approval`, §8 role matrix, §7 authentication + custody) and report its gaps alongside yours in the output. The
   hook's finding is never overwritten, re-judged or filled by analogy: a content gap it names stays a gap until the
   record or the deliverable changes. Where the hook did not fire, run it: `python .claude/hooks/render-validate.py
   --engagement <slug> --deliverable <id>`.

9b. **Post-render — did the document carry what the contract selected?** Step 9 says the
   file is sufficient by content. It says nothing about whether the obligations the projection
   contract selected survived into it. That is a **stage `render`** coverage review of the file
   just written, and it is written, not computed (`coverage-contract.md` §9): one
   `coverage[]` entry per selected obligation, with a `targets[]` entry of
   `role: projection` pointing at the **section of this file** that carries it, plus the two
   passes — source → target (each obligation, and where it landed) and target → source (each
   material mechanism the document states, and where it came from).

   Three rules this step exists for, and each has already been the defect:

   - **An id in a comment is a reference, not a projection.** The motor refuses it as an
     anchor; do not reinstate it by declaring the item `covered` anyway.
   - **The anchor lives in the file under review.** A section of `v02` never proves the
     coverage of `v01`.
   - **A lost obligation is a gap with an owner, and the fix is upstream.** Never reopen the
     source workbook, never edit the Shared Understanding, never resolve an Unknown and never
     upgrade an epistemic state to close it. Write the entry as `partial` / `missing` with
     `required_action` + `responsible_role`, log it to `render-gaps.md`, and do **not** call
     the deliverable complete.

   The record, and then the verdict:

   ```bash
   python library/kernel/tools/coverage.py finalize --engagement <slug> --draft <tmp>/coverage-draft.json
   python library/kernel/tools/coverage.py check --engagement <slug> --stage render --target <engagement>/_render/<file>.md --json
   ```

   Draft to a temp file **outside** the engagement. A deliverable that is `not applicable` or
   `blocked` (step 2b) gets **no** record: its skip in `render-log.md` is the whole answer.

### After all deliverables:

10. Append a run summary to `<engagement>/_render/render-log.md`:
    ```
    <ISO timestamp> — rendered <N>/<M> deliverables — versions: { <id>: v<NN>, … } — gaps: <count>
      skipped: { <id>: "<reason>", … }
      blocked: { <id>: "<reason> — unblocked by <what>", … }
    ```
11. Append one narrative episode to `<engagement>/story.md` (`## Episódio <N> — <data> — as entregas prontas (render)`): 4-8 frases na voz do sponsor, sem jargão de kernel, máx. 2 ids citados. Create the file with `# Story — <slug>` if missing (pre-v2.3 engagements).
12. Output to the user (business language — `CLAUDE.md` → *Duas línguas*; kernel labels and ids only between parentheses). `--all` uses the first two lines; a single deliverable the third; `--dry-run` the fourth (print the resolved template inline, truncated at 50 lines, plus the gap list — write nothing). The `A seguir:` line closes every variant:
    ```user-output
    Documentos finais: <N> de <M> produzidos em `_render/` (versão <NN>). Não aplicáveis a esta escolha: <N> (razão em `_render/render-log.md`).
    Lacunas — o que o registo ainda não sabe e os documentos precisavam: <N> (lista em `_render/render-gaps.md`) <| nenhuma>.
    Do que foi pedido, ficou nos documentos: <N> de <M> temas <| ainda por verificar neste passo>.
    <Um documento: «<nome>» versão <NN> em `_render/<ficheiro>` — lacunas: <N>. | Não aplicável: <razão>. | Bloqueado: <razão> — desbloqueia com <o quê>.>
    <Ensaio (--dry-run): o documento resolvido segue abaixo, truncado a 50 linhas, e a lista de lacunas; nada foi escrito.>
    A seguir: fecha as lacunas → `/answer <id> "…"` (ou uma passagem `/round`); depois `/render --all` outra vez — sai a versão seguinte.
    ```

## Estimate — bounded calculation execution

The Estimate deliverable is the **semantic owner** of the implementation-effort calculation; **this skill is its executor, and the only one**. No synthesis template, no other deliverable template and no other skill computes implementation effort.

```text
authoritative work inventory
+ craft/estimation-model.md          (METHOD authority — person-days)
+ named estimate assumptions
        ↓
aisa-render executing estimate.template's projection contract
        ↓
work breakdown + effort bands + ranges + contingency + confidence
```

Execute only what the contract authorizes: the four declarations `input_inventory_authority`, `method_authority`, `permitted_outputs` and `forbidden_semantic_changes` must all be present. If any is missing, refuse the calculation and log a contract defect.

### Input mode selection — exactly two modes, and no third

```text
MODE A — implementation estimate            (the authoritative path)
  approved architecture + the Implementation Specification's inventory
  → implementation estimate
  SCOPE CONTROL: when a Specification exists, DO NOT add a work unit absent from it.
                 A needed-but-absent unit is an OPEN WORK ITEM against the Specification
                 (owner: implementation) — never an invented estimate line.

MODE B — candidate planning estimate        (available ONLY where all three hold)
  architecture candidates exist
  + architecture approval is blocked by the unresolved structural choice
  + a sponsor materially needs comparative delivery magnitude
  MANDATORY LABEL, verbatim, on every candidate block:
    "Candidate planning estimate — pre-Implementation-Specification; lower-confidence;
     architecture choice unresolved."
  PER CANDIDATE: its own inventory · its own estimate · its own uncertainty · its own
                 confidence. NEVER blend. NEVER choose.
  MAY estimate:     architecture components · known configuration/build obligations ·
                    known proof work · known migration work
  MAY NOT estimate: detailed implementation tasks not yet derivable · screen-level work
                    while the UX blueprint is unapproved · an unevaluated far side · work
                    whose existence depends on the unresolved choice without being assigned
                    to the candidate it belongs to
  SCOPE CONTROL: DO NOT add a work unit absent from the candidate architecture's KNOWN
                 components / obligations.

        no spec  ≠  permission to invent a spec

NEITHER BASIS PRESENT → the Estimate is BLOCKED or NOT APPLICABLE, as appropriate.
                        Never a placeholder. Never a guess.
```

### Estimate hard rules

- **Contingency honesty.** Every structural open choice and every decision-changing Unknown that affects effort renders as a **named** uncertainty line — *the open item · the effort it swings · what would settle it · its `U-NNN`*. Contingency is a number **over** the named items, never a substitute for them.
- **No price.** No licence price, no SKU price, no platform rate card, no quota presented as a cost fact. **Person-days** are the denominator absent a valid engagement-provided delivery rate (which would be an engagement input with provenance, not a pack fact).
- **S8 stays separate.** The Estimate never decides whether this platform is cheaper or more attractive; that is decision economics, and it belongs to the Executive Report. The estimation model is never used comparatively — its own banner forbids it.
- **Category 3 is never estimated** — no allowance, no placeholder, no contingency band for an unevaluated destination.
- **Confidence must match** the epistemic state of the inputs. Mode B is lower-confidence by construction and says so.
- **No discovery re-read.** `_synthesis/as-is.md` is **not** an Estimate input in either mode — not required, not conditional, not fallback, not point-of-need. As-is friction, as-is timing, as-is exceptions and any discovery narrative may **never** become an Estimate work unit, effort figure or operational-impact baseline. Where a discovery fact should alter implementation work but is absent from the authoritative inventory: **mode A** → log an **open work item** against the Implementation Specification (owner `implementation`), never an Estimate line; **mode B** → use it only if it is already a candidate-specific **KNOWN** architecture obligation, otherwise **preserve the uncertainty**. The Estimate calculates only over work whose authority it can name.

## Render-gap classes

Four classes, per `library/kernel/render-contract.md`. **Not every missing slot is decision-blocking**, and the epistemic difference must survive:

| Class | Trigger | Behaviour |
|---|---|---|
| **not applicable** | the section's — or the **deliverable's** — trigger does not hold (no offline requirement; no boundary component; `experience.mode: none`; the deliverable's activation fails) | Omit / do not produce; log a **skip** with the reason to `render-log.md`. **Not a gap** — never written to `render-gaps.md` |
| **optional** | an optional section with no content | Omit |
| **open work item** | a required section that **owned work** can still resolve | Render the open item with **its owner** and what would settle it; log to `render-gaps.md`. **Not** decision-blocking |
| **decision-blocking** | no architecture authorization for any scope, or the decision itself forbids one | Render nothing architectural; render the emitted outcome sentence (+ the architectability basis) instead |

**Class 3 carries an owner:**

```text
owner ∈ { architecture | implementation | design | estimate | evidence }
```

This generalizes the former *architecture work item* label; semantics, trigger and behaviour are unchanged. **No fifth class. No parallel taxonomy.**

A decision-blocked outcome belongs to the decision layer: this skill may **repeat** it and never derive it. Where no architecture was authorized, state the actual reason — outcome unreachable **or** selected solution outside the active pack's architecture authority — and keep the two distinct.

## Hard rules

1. **Append-only on `_render/`.** Never overwrite an existing version. User edits to `v01` are preserved; the next render produces `v02`.
2. **Missing required slot ≠ silent failure.** Every gap goes to `render-gaps.md` AND to the inline placeholder in the rendered file (`⚠️ missing: <slot>`), with its owner.
3. **Skips never pollute `render-gaps.md`.** A `not applicable` deliverable or section is a skip in `render-log.md`. `render-gaps.md` is the file that screams; skips must not dilute it.
4. **No vendor names in vendor-neutral deliverables.** `discovery-report.md` is technology-neutral by construction; if a `_synthesis/business-story.md` section drifts into vendor naming, the chairman or a re-synthesis must fix it — `aisa-render` only composes, it does not re-write.
5. **Execute the contract, nothing more.** A transformation not declared in `permitted_transformations` is not executed, however obvious it looks. When something is missing, log an open work item with its owner — never invent the content.
6. **Idempotence.** `--dry-run` is side-effect-free. A real render only writes a new version of each deliverable and appends to the gap/log files.
7. **Structure, coverage, approval and end-to-end are four questions.** A sufficient document never meant a covered one; a covered one never meant an approved one; an approval never meant the solution was proved end to end. Each is answered by its own check and reported on its own line, and none is ever announced on behalf of another. `not_evaluated` is the honest answer where no review exists (`coverage-contract.md` §10).
8. **Coverage verifies; it never redefines.** Render does not change a fact, a decision, the scope, an epistemic state or a proof level to close a coverage finding — and a missing authority is a **skip with its reason**, never a gap.
