# Render Contract — Kernel v0.1.0

## Pipeline: Decision → (Blueprint) → Synthesize → Render

For engagements with a UI component, the Decision phase includes the blueprint loop before final render: `/decide` → `/blueprint` → prototype (external) → business feedback (`/answer`) → blueprint vN → approval (D-NNN) → `/synthesize` → `/render --all`. See [`blueprint-contract.md`](blueprint-contract.md).

```
shared-understanding.md  ──┐
lens-outputs/<lens>.md     ├──→ aisa-synthesize ──→ _synthesis/<topic>.md (5 files)
decisions.md               ─┘                                  │
                                                               ↓
                                              aisa-render ──→ _render/<deliverable>_vNN.<ext>
```

## Synthesis layer (`aisa-synthesize` skill)

Auto-runs at the end of `/decide`. Reads the Shared Understanding + `lens-outputs/` + `decisions.md`. Produces 5 topic packs:

| Topic pack | Sources |
|---|---|
| `_synthesis/business-story.md` | Confirmed/Assumed [lens=business] + lens-outputs/business.md |
| `_synthesis/as-is.md` | rows [lens=operations,user] + lens-outputs/{operations,user}.md |
| `_synthesis/architecture-story.md` | decisions.md + rows [lens=technology,data] + lens-outputs/{technology,data}.md + chosen architecture-template |
| `_synthesis/risks-and-assumptions.md` | Risky + Assumed + Unknown.criticality=Critical |
| `_synthesis/financial-story.md` | rows [lens=financial] + lens-outputs/financial.md + decisions.md (cost/timeline) |

Each topic pack template lives in `library/kernel/synthesis-templates/<topic>.template.md` (created in a later build phase).

## Render layer (`aisa-render` skill)

Reads the topic packs + decisions + the pack's `deliverable-templates/<deliverable>.template.md`. Produces output in `_render/`.

### Slot resolution order

1. `_synthesis/<topic>.md` (declared by the template).
2. Shared Understanding structured rows (for tables, lists).
3. `decisions.md`.
4. `context.json`.
5. If none AND the slot is `required` → fail loud, log to `render-gaps.md`.
6. If none AND the slot is `optional` → omit the section.

### Versioning

- `v01`, `v02`, ... — `/render` always produces the next available version.
- Never overwrites existing files (user edits to v01 are preserved).
- `_render/<slug>_<deliverable>_v<NN>.<ext>` is the filename pattern.

### Applicability by decision type

`pack.yaml` may declare `applies_to` per deliverable (`all` or a list such as `[technology]`). For a non-technology / do-nothing decision, only `applies_to: all` deliverables render; the rest are skipped with a logged reason (a skip is not a gap). `architecture-story.md` is still synthesized but describes the chosen intervention, not a platform architecture. Missing `applies_to` defaults to `all`.

### Output formats

- Markdown by default.
- Conversion to .docx via Pandoc (post-render step, optional in MVP).

See [`phases.md`](phases.md) for the phase that triggers this (Decision) and [`states.md`](states.md) for the row states the synthesis layer reads.
