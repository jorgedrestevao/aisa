# Deliverable Authoring Guide

A **deliverable** is a final artefact the engagement produces for handoff (Discovery Report, Executive Report, Solution Blueprint, Implementation Spec, Claude Design Brief, Estimate). Deliverables are rendered at the end (via `aisa-render`) from templates declared in the active pack.

This guide explains how to author or modify a deliverable template.

## Where deliverables live

Templates live in **the pack**, not in the kernel:

```
library/packs/<pack>/deliverable-templates/
├── discovery-report.template.md
├── executive-report.template.md
├── solution-blueprint.template.md
├── implementation-spec.template.md
├── claude-design-brief.template.md
└── estimate.template.md
```

Each is declared in `pack.yaml`:

```yaml
deliverables:
  - id: <slug>
    mandatory: true|false
    template: deliverable-templates/<slug>.template.md
```

`mandatory: true` deliverables are produced by `/render --all`. Optional ones are only produced when requested by name.

## Anatomy of a deliverable template

```markdown
---
template_id: <slug>
output_format: md|docx
audience: client|sponsor|technical|developer|claude-design
required_slots:
  - <slot-name>
  - …
optional_slots:
  - <slot-name>
  - …
sub_templates:
  - architecture-templates/{{<dynamic-slot>}}.md
  - …
slot_sources:
  <slot-name>: <resolution-spec>
  …
---

# <Title> — {{solution_name}}

> <One-line description of the deliverable's purpose and audience.>

## 1. <Section heading>
{{<slot-name>}}

## 2. <Section heading>
{{>> architecture-templates/{{<dynamic-slot>}}.md}}

…
```

### Frontmatter fields

- **`template_id`** — kebab-case slug; must match the filename and the `pack.yaml` declaration.
- **`output_format`** — `md` by default. `docx` triggers Pandoc conversion as a post-render step (Phase 11+, not yet implemented).
- **`audience`** — `client` / `sponsor` / `technical` / `developer` / `claude-design`. Drives the prose register the slot synthesis aims for.
- **`required_slots`** — the slots that MUST resolve to non-empty content. Missing required slots produce a gap entry in `render-gaps.md` AND an inline `⚠️ missing` placeholder in the rendered file.
- **`optional_slots`** — slots that may be empty. Missing optional slots render as an empty section heading.
- **`sub_templates`** — paths to sub-templates referenced via `{{>>` includes. Paths may contain `{{slot}}` for dynamic resolution (e.g., `architecture-templates/{{chosen_architecture}}.md`).
- **`slot_sources`** — explicit mapping of slot → source. The render skill uses this to resolve `{{slot}}` placeholders. Format: `<path>#<section-fragment-or-filter>`.

### Slot resolution

For each `{{slot}}` in the template body, `aisa-render` resolves it in this order (per `library/kernel/render-contract.md`):

1. **`slot_sources[<slot>]`** (the template's explicit mapping).
2. The corresponding **topic pack** in `_synthesis/` if the slot name maps to one (e.g., `business_context` → `_synthesis/business-story.md`).
3. The relevant **Shared Understanding section**, filtered by lens or row id.
4. **`decisions.md`** (D-NNN fields).
5. **`context.json`**.
6. Computed defaults (e.g., `solution_name` = title-cased slug).

If none resolves → gap.

### Sub-template includes

Syntax: `{{>> <path>}}`. The path can contain a dynamic placeholder like `{{>> architecture-templates/{{chosen_architecture}}.md}}` — `aisa-render` first resolves the inner placeholder (here `chosen_architecture` comes from `decisions.md`), then loads the sub-template and recursively resolves its own slots from the engagement.

## Authoring discipline

### Audience drives prose register

- **`client`** — Portuguese (or pack language), discoverable in 15 minutes, no vendor names if the deliverable is technology-neutral (e.g., `discovery-report.md`).
- **`sponsor`** — same as client, but more decision-orientated; executive-report.md should read in 10.
- **`technical`** — solution-blueprint.md; for solution architects, lead developers. Vendor names allowed; the architecture sub-template is the structural anchor.
- **`developer`** — implementation-spec.md; actionable, schemas + flows + tests; this is what the dev team uses to build.
- **`claude-design`** — claude-design-brief.md; written so a Claude Design session can produce Canvas App mockups directly. Includes domain-knowledge cross-references inline.

### Slot naming

- Use snake_case slot names.
- Prefer **concrete nouns** over generic verbs (`current_state_summary`, not `summarise_situation`).
- Keep the slot count under ~10 per deliverable. Heavy slots usually want a sub-template instead.

### Required vs optional

- A slot is **required** when the deliverable is incomplete without it (e.g., `business_case` in `executive-report.md`).
- A slot is **optional** when its absence is plausible (e.g., `accessibility_notes` if the engagement explicitly de-prioritises it).
- Better to have a slot required and let the render gap teach the engagement what is missing, than to have everything optional and ship empty sections.

### Cross-template consistency

When two deliverables share a slot (e.g., `chosen_architecture` in solution-blueprint, implementation-spec, claude-design-brief, estimate), they MUST source it from the same place — usually `decisions.md# D-NNN — Branch (if technology)`. Otherwise rendered deliverables drift.

## Adding a new deliverable

Greenfield checklist:

1. **Justify** — does an existing deliverable already cover this need? If you're adding a "Migration Plan" — is it `implementation-spec.md § Notas de migração de dados`? Usually yes.
2. **Pick a `template_id`** — kebab-case, mirrors the filename.
3. **Pick the audience** — drives slot wording.
4. **Identify the slots** — start with the section headings, then back out the slot per section. Aim for ≤10.
5. **Map slot_sources** — every slot must have a known source artefact. If a slot has no obvious source, the engagement is producing the wrong thing; rework the slot.
6. **Declare it** in `pack.yaml` and add to `deliverables`.
7. **Test** — run `/render <new-id> --dry-run` against a fixture engagement; review the resolution and gap log.

## Modifying an existing deliverable

- **Adding a slot** — declare it in frontmatter + slot_sources + use `{{slot}}` in the body. Re-running `/render` produces the next version with the new slot.
- **Removing a slot** — remove from frontmatter + body. Old rendered versions in `_render/` are preserved untouched (the directory is append-only).
- **Renaming a slot** — treat as remove + add. There is no migration mechanism.
- **Changing the audience or prose register** — bump the pack version (semver minor at least).

## Anti-patterns

- **Required slots that are usually empty** — leads to render-gaps.md noise. If a slot is empty 80% of the time, it should be optional.
- **Free-form prose in a slot** that should be a structured fragment (e.g., a table). The template is responsible for the structure; the slot fills the cells.
- **Sub-templates that hard-code branch names** instead of using `{{chosen_architecture}}`. Brittle to pack evolution.
- **Vendor names in `discovery-report.md`, `executive-report.md`, `business-story.md`, or `as-is.md`** — these are technology-neutral by construction. `aisa-render` does not police this; the chairman during synthesis must.
