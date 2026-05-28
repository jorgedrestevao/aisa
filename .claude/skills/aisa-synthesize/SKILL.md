---
name: aisa-synthesize
description: Produce the 5 topic packs in <engagement>/_synthesis/ from the Shared Understanding, lens-outputs, and decisions. Auto-runs at the end of aisa-decide; can also be invoked manually. Uses templates in library/kernel/synthesis-templates/.
---

# aisa-synthesize

## Usage

`/synthesize [<topic>]`

- No argument: produce all 5 topic packs.
- `<topic>`: produce only one — `business-story`, `as-is`, `architecture-story`, `risks-and-assumptions`, `financial-story`.

## When it runs

- **Automatically** as the last step of `/decide`.
- **Manually** when a topic pack failed and must be retried, or when the user wants to refresh the synthesis after editing the SU.

## Inputs (read)

- `<engagement>/_state.json` (must be `phase == decision` to produce the full set; manual single-topic runs allowed earlier with a warning).
- `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/frame.md`, `<engagement>/options.md`.
- `<engagement>/lens-outputs/*.md` (every lens narrative and every chairman synthesis log).
- `library/kernel/synthesis-templates/<topic>.template.md` (one per topic — defines sources + the synthesis prompt).
- `library/packs/<pack>/pack.yaml` (for any pack-specific synthesis hooks).

## Outputs (written)

- `<engagement>/_synthesis/<topic>.md` — one file per topic, overwritten on re-synthesis.
- `<engagement>/_synthesis/_synthesis-log.md` — append-only audit of each synthesis run (timestamp, topics produced, source counts, warnings).

## The 5 topic packs and their sources

| Topic pack | Primary sources |
|---|---|
| `business-story.md` | SU rows where `lens ∈ {business}` (Confirmed + Assumed) + `lens-outputs/business.md` + `frame.md` |
| `as-is.md` | SU rows where `lens ∈ {operations, user}` + `lens-outputs/{operations,user}.md` |
| `architecture-story.md` | `decisions.md` (chosen option + branch) + SU rows where `lens ∈ {technology, data}` + `lens-outputs/{technology,data}.md` + the pack's chosen architecture template (`library/packs/<pack>/architecture-templates/<branch>.md`) |
| `risks-and-assumptions.md` | SU sections `Risky` + `Assumed` + `Unknown` (Critical only) + `decisions.md` (Accepted risks + Revision conditions) |
| `financial-story.md` | SU rows where `lens ∈ {financial}` + `lens-outputs/financial.md` + `decisions.md` (cost/timeline anchors) |

## Execution steps

### For each topic to synthesise:

1. Read `library/kernel/synthesis-templates/<topic>.template.md`. The template declares `sources` (paths to read), `prose_structure` (the markdown skeleton), and `synthesis_prompt` (what to do with the sources).
2. Read the engagement files in `sources` (per the table above).
3. Apply the `synthesis_prompt` to produce 3–6 short paragraphs (no fluff; cite SU ids inline like `C-007`).
4. Compose the final markdown by filling the `prose_structure` skeleton.
5. Write `<engagement>/_synthesis/<topic>.md` (overwrite if exists).
6. Append a line to `<engagement>/_synthesis/_synthesis-log.md`:
   ```
   <ISO timestamp> — <topic> — sources: <count> SU rows, <count> lens-outputs, <count> decisions — <N> paragraphs, <N> SU ids cited
   ```

### After all topics:

7. Sanity check: every topic file is ≥3 paragraphs and contains at least one SU id citation. If any check fails → log a warning to `_synthesis/_synthesis-log.md` and surface in the wrap-up output.
8. Wrap-up output: "Synthesis complete: `<N>/5` topic packs in `_synthesis/`. Run `/render --all` to produce the 6 deliverables, or `/render <deliverable>` for one."

## Hard rules

1. **Never invent claims.** Every sentence in a topic pack must be traceable to a source artefact. If a topic has thin source material, write less — do not fabricate.
2. **Cite SU ids inline.** Each non-trivial claim should anchor to `C-NNN`, `A-NNN`, `R-NNN`, `X-NNN`, or `D-NNN`. Topic packs that omit citations are flagged in the synthesis log.
3. **No vendor names** in `business-story.md`, `as-is.md`, `risks-and-assumptions.md`, `financial-story.md` (these mirror Discovery's neutrality). Vendor names only appear in `architecture-story.md`, anchored to the decision and the pack's architecture template.
4. **Idempotence.** Re-running `/synthesize` overwrites the topic packs cleanly. The log is append-only.
