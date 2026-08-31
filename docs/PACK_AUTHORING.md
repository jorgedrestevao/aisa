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
├── architecture-templates/    # one .md per architectural branch declared in decision-tree.md
└── domain-knowledge/          # WARM reference content for lens-technology + claude-design-brief
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
  - domain-knowledge/<file>.md
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

### Lens signal extensions

Each Discovery lens has universal signals defined in its `SKILL.md`. Packs may *add* signals via `lenses_config.<lens>.extra_signals` — these are pack-specific things the lens should probe in this domain (e.g., for `pp`: `licensing_baseline`, `integration_licensing_exposure`). Discovery signals must stay vendor-neutral — name needs and current state, never target products (see `.claude/rules/no-tech-mention-before-options.md`).

For `technology`, packs declare `constraints_to_check` — the architectural constraints the solution-architect must verify against each option (e.g., `premium_licensing`, `dataflow_capacity`, `dataverse_storage_quota`).

### Deliverable templates

See `docs/DELIVERABLE_AUTHORING.md`. The pack declares which deliverables are part of the engagement output; templates live in `deliverable-templates/`.

### Architecture sub-templates

When `decision-tree.md` exposes architectural branches, each branch needs a sub-template under `architecture-templates/<branch-id>.md`. Deliverables include them via `{{>> architecture-templates/{{chosen_architecture}}.md}}`. The sub-template's slots are resolved from `_synthesis/architecture-story.md`.

### Domain knowledge

WARM reference content (delegation matrices, security patterns, etc.) that `lens-technology` reads in Options and that `claude-design-brief.template.md` cross-references. Stay vendor-explicit here — this is the pack-specific deep knowledge that justifies having a pack at all.

## Validating a pack before use

There is no automated validator in the MVP (Phase 11 adds `pack-validate.sh` stub). Manual checklist:

1. `pack.yaml` parses (try `python -c "import yaml; yaml.safe_load(open('pack.yaml'))"` if PyYAML is installed; otherwise inspect for indent/colon errors).
2. Every deliverable declared in `pack.yaml` has a matching template file.
3. Every branch in `decision-tree.md` has a matching architecture sub-template.
4. Glossary has ≥30 terms; question bank has ≥5 per lens.
5. No skill or lens file under `.claude/` references a pack-specific concept by hard-coding — pack-specific data must come via `pack.yaml` keys.

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
