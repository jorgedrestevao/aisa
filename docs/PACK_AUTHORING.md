# Pack Authoring Guide

A **pack** is the domain configuration aisa loads at engagement start. It declares the vocabulary, the question bank, the deliverable templates, and any pack-specific signal additions for the lenses. Packs live under `library/packs/<id>/` and are read-only at runtime.

This guide explains how to author or extend a pack. The canonical reference pack is `library/packs/pp/`.

## Pack identity

A pack is identified by:

- `pack_id` — short kebab-case slug, used in `_state.json.pack` and as the folder name.
- `pack_version` — semver. Bump on any change that affects engagement output.
- `display_name` — what `/status` and deliverables show.
- `language` — `pt` or `en` (drives the deliverable prose language).

## Required files

```
library/packs/<id>/
├── pack.yaml                  # the manifest — see "Manifest" below
├── glossary.md                # 30+ domain terms (see library/packs/pp/glossary.md)
├── question-bank.md           # 40+ questions, organised by lens
├── decision-tree.md           # architectural-branch decision tree (Options-only)
├── deliverable-templates/     # one .template.md per declared deliverable
├── architecture-templates/    # ONE fixed entry point (architecture-core.md) + fragments
└── domain-knowledge/          # PULL-BASED knowledge, never preloaded. README.md carries the use
                           # contract; RESEARCH units (application/ data/ automation/ integration/
                           # security/ governance/ alm/ performance/ economics/ operations/
                           # architecture/) state platform knowledge; craft/ states delivery
                           # practice and is never an Options pull target
```

## Manifest (`pack.yaml`)

Minimum required keys:

```yaml
pack_id: <id>
pack_version: <semver>
display_name: "<title>"
language: pt|en
description: >
  <one paragraph for /status>

deliverables:
  - id: <slug>
    mandatory: true|false
    template: deliverable-templates/<slug>.template.md
  # …

lenses_config:
  business:
    extra_signals: [<pack-specific signal>, …]
  operations:
    extra_signals: [<...>]
  user:
    extra_signals: [<...>]
  data:
    extra_signals: [<...>]
  technology:
    constraints_to_check: [<pack-specific constraint>, …]
  governance:
    extra_signals: [<...>]
  financial:
    extra_signals: [<...>]

domain_knowledge:
  # A MANIFEST only — not a load order, not a routing table, not a concern map,
  # not a priority list. No canonical research ids here.
  - domain-knowledge/README.md
  - domain-knowledge/<area>/<file>.md
  - domain-knowledge/craft/<file>.md
  # …

question_bank: question-bank.md
glossary: glossary.md

decision_tree:
  source: decision-tree.md
  consulted_in_phase: options
```

The keys are not enforced by a hard schema (yet — Phase 11+ will add `pack-validate.sh`), but skills assume them. Missing keys → skills will fall back to kernel defaults and warn.

## Authoring discipline

### Vocabulary in `glossary.md`

The glossary is the contract with the engagement participants. Two columns: term, definition. Prefer the language of the customer's daily work over vendor names; cross-reference vendor names only where unavoidable.

### Question bank

Organise by lens (the 7 in `library/kernel/glossary.md`). 5–8 questions per lens is typical. Phrase as open questions, not yes/no. Questions probe **need** and **current state**; in Discovery they MUST NOT presuppose a solution technology (see `.claude/rules/no-tech-mention-before-options.md`).

**Runtime role.** `question_bank` is a **question-generation resource**, not permanent context for the lenses — no lens or council persona loads it. It is consulted selectively, at question-generation time, to phrase askable questions around material `Unknown` / `Conflicted` / `Risky` rows and evidence gaps. Single intended consumer: the question-generation step in `aisa-status` (the meeting agenda). Two consumers would drift, so author for that one reader: each probe should state a trigger the Shared Understanding can actually satisfy ("fires when X observed"), and the file should be readable in one pass. Contract: `library/kernel/orchestration.md` → *Question bank — runtime role*.

### Lens signal extensions

Each Discovery lens has universal signals defined in its `SKILL.md`. Packs may *add* signals via `lenses_config.<lens>.extra_signals` — these are pack-specific things the lens should probe in this domain (e.g., for `pp`: `licensing_baseline`, `integration_licensing_exposure`). Discovery signals must stay vendor-neutral — name needs and current state, never target products (see `.claude/rules/no-tech-mention-before-options.md`).

**How they reach the lens.** The **orchestrator** resolves the active pack and injects the list into the lens invocation as attention cues. The six Discovery lenses are pack-agnostic — they never read `pack.yaml`, and `extra_signals` are never copied into a lens file. **Signals are attention cues, not checklist items**: the injected block carries the clause *"cues, not a checklist; uncovered cues are not gaps"*, and nothing requires a lens to cover every signal or to open an `Unknown` for an uncovered one.

**How many.** Soft authoring heuristic: prefer roughly **5–8 high-value extra signals per Discovery lens**. Not a limit and not validated — a long list is a list nobody reads, which is a quality problem, not a schema violation. **Survival test: a signal survives only if removing it would materially reduce the lens's ability to notice a domain-specific issue.** Research support alone is not sufficient reason for a signal to consume runtime context.

For `technology`, packs declare `constraints_to_check` — the architectural constraints the solution-architect must verify against each option (e.g., `premium_licensing`, `dataflow_capacity`, `dataverse_storage_quota`).

### Deliverable templates

See `docs/DELIVERABLE_AUTHORING.md`. The pack declares which deliverables are part of the engagement output; templates live in `deliverable-templates/`.

### Architecture sub-templates

The architecture layer is **fixed**: one entry point, `architecture-templates/architecture-core.md`, which carries the A1–A12 output shape. There is **no per-branch sub-template, no dynamic include path, no `<chosen>.md` lookup and no router** — the three store-first branch shapes were retired in Step 5B.

An architecture-consuming deliverable includes it literally:

```text
{{>> architecture-templates/architecture-core.md}}
```

The core resolves **zero or one** experience fragment from the recorded `architecture.experience.mode` (`none` resolves to **zero** includes — A4 renders `not applicable` with its reason, which is a finalized architectural fact, not a gap) and **zero or more** boundary-fragment instances, exactly one per qualifying component (N unique qualifying composition components + M unique relocated responsibilities, six channels each). `aisa-render` performs that iteration.

Its slots resolve from the recorded `architecture:` block first, then `_synthesis/architecture-story.md` for narrative glue. Authorization, experience mode, record authority, composition, scope relocation and pattern are **read**, never derived, upgraded or downgraded by a deliverable.

## Deliverable templates are projection contracts

Each of the six deliverable templates declares — declaratively, with **no routing logic**:

| Field | Meaning |
|---|---|
| `canonical_deliverable` | which of the six canonical deliverables this file is (the runtime id may be an alias: `solution-blueprint` ↔ `architecture-blueprint`) |
| `activation` / `blocked_when` / `not_applicable_when` | when it is produced, blocked, or skipped |
| `authority_sources` | the closest authoritative artefact per fact |
| `conditional_sources` | sources read only where a condition holds |
| `forbidden_sources` | artefacts this deliverable must never read |
| `permitted_transformations` | the bounded derivations `aisa-render` may execute for this contract |
| `forbidden_transformations` | what no projection of this deliverable may change |
| `slot_conditions` | per-slot conditions (this is what keeps a headless architecture from manufacturing a surface) |
| `materiality` | Discovery only — which rows survive, and how omissions are counted |
| `owns_calculation` | Estimate only — authorizes `aisa-render` to execute the bounded calculation the template defines |
| `input_modes` | Estimate only — exactly two, and no third |

The template **declares**; `aisa-render` **executes**, and executes only what is declared. Neither reasons.

A transformation is legitimate exactly when it is **deterministic**, **bounded**, **declared by the active contract**, and **traceable to already-authoritative inputs**. Fail any of the four and it is reasoning — which is prohibited downstream. Permitted examples: *architecture obligation → implementation work package*, *proof obligation → acceptance work package*, *implementation inventory → estimate work unit*, *work units + estimation method → effort bands*, *approved UX blueprint → generator-oriented screen block*.

**One primary semantic authority per information class.** A statement appearing in two deliverables has one authority; the second occurrence is a projection, not a competing claim. In particular: the Estimate is the semantic owner of the implementation-effort calculation (no synthesis template and no other skill computes effort), and the architecture-entry gate rule is the semantic owner of the architectability basis (`_synthesis/architecture-story.md` is its **durable carrier**, never its authority).

### Domain knowledge

WARM reference content (delegation matrices, security patterns, etc.) that `lens-technology` reads in Options and that `claude-design-brief.template.md` cross-references. Stay vendor-explicit here — this is the pack-specific deep knowledge that justifies having a pack at all.

**Pull-based, not push-based.** `lens-technology` is the only pack-aware lens, and only in Options; it consults the relevant files selectively and does not load the whole domain-knowledge base by default. Author each file so it can be read on its own, for one question.

## Validating a pack before use

There is no automated validator in the MVP (Phase 11 adds `pack-validate.sh` stub). Manual checklist:

1. `pack.yaml` parses (try `python -c "import yaml; yaml.safe_load(open('pack.yaml'))"` if PyYAML is installed; otherwise inspect for indent/colon errors).
2. Every deliverable declared in `pack.yaml` has a matching template file.
3. Every branch in `decision-tree.md` has a matching architecture sub-template.
4. Glossary has ≥30 terms; question bank has ≥5 per lens.
5. No skill or lens file under `.claude/` references a pack-specific concept by hard-coding — pack-specific data must come via `pack.yaml` keys.
6. No lens, agent or skill file copies `extra_signals` or `constraints_to_check` inline — pack signals reach Discovery lenses only by orchestrator injection.

## Versioning and updates

- Bump `pack_version` (semver) on **any** change to vocabulary, deliverables, or lens extensions.
- Domain-knowledge updates (e.g., Microsoft adds a new Dataverse delegable operation) are pack changes — bump the version.
- Engagements pin to the pack version they started under via `_state.json.pack` — re-rendering an old engagement keeps using the older templates unless explicitly migrated.

## Adding a new pack

Greenfield checklist:

1. `mkdir library/packs/<id>` and create the directory layout above.
2. Write `pack.yaml` first — it forces you to declare the deliverable set early.
3. Write `glossary.md` (30+ terms) — this anchors everything downstream.
4. Write `question-bank.md` (40+ questions across 7 lenses).
5. Decide the architectural branches → `decision-tree.md` + one architecture sub-template per branch.
6. Transplant or write 6 deliverable templates. The `claude-design-brief.template.md` and `implementation-spec.template.md` are mandatory; the others are pack discretion.
7. Domain knowledge — typically last, evolves as the pack hits real engagements.
8. Test with a fresh engagement on a known scenario; iterate.

The `outsystems`, `mendix`, and `generic` packs ship as skeletons (only `pack.yaml`) — they are deliberate placeholders for the team to fill as those engagement domains come online.
