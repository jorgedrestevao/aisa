---
name: aisa-render
description: Render the 6 (or a specific) deliverable(s) for the engagement, by resolving the pack's deliverable templates against _synthesis/, the Shared Understanding, decisions, and context. Writes versioned files to _render/. Missing required slots are logged to render-gaps.md (no silent failures). Supports --all and --dry-run.
---

# aisa-render

## Usage

`/render [<deliverable>|--all] [--dry-run]`

- `<deliverable>`: render only one — `discovery-report`, `executive-report`, `solution-blueprint`, `implementation-spec`, `claude-design-brief`, `estimate`.
- `--all`: render every deliverable declared in `library/packs/<pack>/pack.yaml` **that applies to the decision type** (see *Applicability by decision type* below). This is the default after `/decide` → `/synthesize`.
- `--dry-run`: resolve slots and surface gaps without writing to `_render/`. Useful for debugging templates without bumping versions.

## Phase gate (soft)

The engagement should be at `phase == decision` with `_synthesis/` populated (5 topic packs). Earlier `/render` attempts are allowed but most slots will be empty and `render-gaps.md` will scream. See `.claude/rules/render-on-decision-only.md`.

If `phase != decision` AND `--dry-run` is **not** set → stop with: "Render before /decide is forbidden by `.claude/rules/render-on-decision-only.md`. Use `--dry-run` to preview, or finish the engagement first."

## Applicability by decision type

`pack.yaml` may declare `applies_to` per deliverable (`all`, or a list such as `[technology]`). Read the decision type from the final `D-NNN` block in `decisions.md` (`Branch (if technology)`: a decision-tree branch = technology decision; `non-technology` / `do-nothing` otherwise):

- **Technology decision** → render every declared deliverable.
- **Non-technology / do-nothing decision** → render only deliverables with `applies_to: all` (typically discovery-report, executive-report, estimate). Skip the others and log each skip to `render-log.md` with the reason (`not applicable: non-technology decision`) — a skip is **not** a gap and must not pollute `render-gaps.md`.
- A deliverable without `applies_to` defaults to `all` (backwards compatible with older packs).

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/frame.md`, `<engagement>/options.md`.
- `<engagement>/_synthesis/*.md` (the 5 topic packs).
- `library/packs/<pack>/pack.yaml` (lists the deliverables).
- `library/packs/<pack>/deliverable-templates/<id>.template.md` (one per deliverable).
- `library/packs/<pack>/architecture-templates/<branch>.md` (when a deliverable includes a sub-template; the branch is read from `decisions.md`).
- Any other domain-knowledge files referenced by a deliverable.

`<engagement>` resolves to `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, otherwise `projects/<slug>`. `<pack>` is read from `_state.json.pack`.

## Outputs (written)

- `<engagement>/_render/<slug>_<deliverable>_v<NN>.md` — versioned, append-only (never overwrites a previous version). `<NN>` is `01`, `02`, …, the next available integer.
- `<engagement>/_render/render-gaps.md` — log of every missing required slot encountered in this render run, with the deliverable and the resolution attempt. Append-only across runs.
- `<engagement>/_render/render-log.md` — per-run audit: timestamp, deliverables rendered, version per file, gap count.

## Slot resolution order

For each `{{slot}}` in a template, resolve in this order (per `library/kernel/render-contract.md`):

1. `_synthesis/<topic>.md` section (when the template's `slot_sources` declares it).
2. The relevant Shared Understanding section (`Confirmed`, `Assumed`, `Risky`, etc.), filtered by lens or row id when declared.
3. `decisions.md` (D-NNN fields).
4. `context.json`.
5. Computed (e.g., `solution_name` defaults to `<engagement-slug>` title-cased if not declared in context).

If none of the above yields a value AND the slot is `required` → log a gap, render the slot as `> ⚠️ missing: <slot> (see render-gaps.md)`, and continue. If the slot is `optional` → render an empty section heading or omit per template guidance.

Sub-template includes (`{{>> path/to/sub.md}}`) recursively resolve the same way, with the sub-template's own slot_sources.

When the decision is non-technology/do-nothing and a still-applicable template includes `{{>> architecture-templates/…}}` (e.g., the estimate), replace the include with a one-line note — `> Decisão non-technology / do-nothing — sem sub-template arquitectural (ver decisions.md#D-NNN)` — and do not log a gap.

## Versioning

- `<engagement>/_render/` is scanned for files matching `<slug>_<deliverable>_v*.md`. The next version is the highest existing + 1, or `01` if none exists.
- Never overwrite an existing file — user edits to v01 are preserved across re-renders.
- `--dry-run` writes nothing to `_render/`, only outputs the preview + gap list to the chat.

## Execution steps

### For each deliverable to render:

1. Read the template `library/packs/<pack>/deliverable-templates/<id>.template.md`. Parse the YAML frontmatter: `required_slots`, `optional_slots`, `slot_sources`, `sub_templates`.
2. For each slot in `required_slots ∪ optional_slots`:
   a. Look up the slot's `slot_sources` entry (if any).
   b. Walk the resolution order above; capture the resolved text or `MISSING`.
3. Substitute slots in the template body. For sub-template references (`{{>> architecture-templates/{{chosen_architecture}}.md}}`):
   a. First resolve the inner `{{chosen_architecture}}` against `decisions.md`.
   b. Read `library/packs/<pack>/architecture-templates/<resolved>.md`.
   c. Recursively resolve its slots from the engagement (sub-template slots use the same resolution order; they typically map to `_synthesis/architecture-story.md`).
4. Compute the next version `<NN>` for `<engagement>/_render/`. Write `<engagement>/_render/<slug>_<deliverable>_v<NN>.md` unless `--dry-run`.
5. Append any encountered gaps to `<engagement>/_render/render-gaps.md` with deliverable + slot + attempted-source.

### After all deliverables:

6. Append a run summary to `<engagement>/_render/render-log.md`:
   ```
   <ISO timestamp> — rendered <N>/<M> deliverables — versions: { <id>: v<NN>, … } — gaps: <count>
   ```
7. Append one narrative episode to `<engagement>/story.md` (`## Episódio <N> — <data> — as entregas prontas (render)`): 4-8 frases na voz do sponsor, sem jargão de kernel, máx. 2 ids citados. Create the file with `# Story — <slug>` if missing (pre-v2.3 engagements).
8. Output to the user:
   - `--all`: "Rendered <N>/<M> deliverables to _render/. Gaps: <count>. Review `_render/render-gaps.md` and adjust the SU/synthesis if needed, then re-run /render --all (will produce v<NN+1>)."
   - Single deliverable: "Rendered <id> v<NN> at `_render/<file>`. Gaps: <count>."
   - `--dry-run`: print the resolved template inline (truncated if >50 lines) and the gap list. Do not write.

## Hard rules

1. **Append-only on `_render/`.** Never overwrite an existing version. User edits to `v01` are preserved; the next render produces `v02`.
2. **Missing required slot ≠ silent failure.** Every gap goes to `render-gaps.md` AND to the inline placeholder in the rendered file (`⚠️ missing: <slot>`). The user must see what is missing.
3. **No vendor names in vendor-neutral deliverables.** `discovery-report.md` is technology-neutral by construction; if a `_synthesis/business-story.md` section drifts into vendor naming, the chairman or a re-synthesis must fix it — `aisa-render` only composes, it does not re-write.
4. **Idempotence**. `--dry-run` is side-effect-free. A real render only writes a new version of each deliverable and appends to the gap/log files.
