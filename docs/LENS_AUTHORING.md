# Lens Authoring Guide

Lenses are the perspective skills aisa uses during Discovery (`inline` mode) and during Framing/Options/Decision (`council-independent` mode, via persona agents). This guide explains how to add a new lens, modify an existing one, or audit a lens for kernel-compliance.

Existing lenses (the kernel's 7):

- `lens-business` — impact, urgency, KPIs, shadow stakeholders.
- `lens-operations` — as-is process, friction, exceptions, tribal knowledge.
- `lens-user` — personas, journeys, devices, accessibility.
- `lens-data` — ownership, quality, sensitivity, retention.
- `lens-governance` — compliance, security, audit, separation of duties.
- `lens-financial` — as-is cost, do-nothing cost, payback.
- `lens-technology` — vendor/product fit (Options-only).

The first 6 are the **Discovery lenses**. The 7th (`lens-technology`) activates only in Options. See `library/kernel/phases.md`.

## Anatomy of a lens

Every lens lives at `.claude/skills/lens-<name>/SKILL.md` with this frontmatter:

```yaml
---
name: lens-<name>
description: <one line — when this lens runs and what it covers>
---
```

The body has six required sections in this order:

1. **Role** — the persona stance and the 3–4 questions the lens sees every request through.
2. **Inputs (always read)** — the engagement files + `inputs/` policy + agent-memory paths.
3. **Outputs (always write)** — SU rows + the lens narrative.
4. **Hard rules (kernel-enforced)** — no vendor naming (except `lens-technology`), no Confirmed without evidence, always identify in the `lens` column, append-only.
5. **Signal catalog** — universal signals + pack additions.
6. **Execution steps** — numbered procedure the lens follows.

Lenses MUST be idempotent: running them twice on the same input adds the next round's rows but never deletes or rewrites prior rows.

## Hard rules every lens must obey

1. **No vendor/product names** before Options (`.claude/rules/no-tech-mention-before-options.md`). Existing systems may be named *as current state* (e.g., "the spreadsheet that anchors approvals today"). The only exception is `lens-technology`, which activates in Options.
2. **No Confirmed without evidence.** Direct citation (document, USER_ANSWER, sponsor statement) → Confirmed. Inference from industry pattern → Assumed (basis declared). Missing → Unknown (with `quem responde` + `criticidade`). Disagreement between ≥2 sources → Conflicted.
3. **Identify in the `lens` column.** Always `<lens-name>` (e.g., `business`, `governance`).
4. **Append-only on the Shared Understanding.** Never delete or rewrite an existing row. State transitions add a new row that references the old (`was X-NNN`); the old row stays for audit. See `library/kernel/states.md`.
5. **Open every file in `inputs/`.** Never cite an input by filename alone — read and parse it per `library/kernel/orchestration.md` → *Reading input documents*. Cite the specific value, column, or passage.

## Adding a new lens

If you need a perspective the kernel's 7 do not cover (rare — most needs become signal additions on an existing lens), follow this checklist:

1. **Justify the lens** — what perspective is genuinely missing? If the answer is "a sub-aspect of business" or "a sub-aspect of governance", add a signal to that lens instead.
2. **Pick the persona** — what real-world role embodies this lens? The persona becomes the council-independent agent (`.claude/agents/<persona>.md`).
3. **Pick the phase activation** — Discovery + council-independent (the default for the 6), or council-independent-only like `lens-technology`.
4. **Author the SKILL.md** — follow the 6-section template; mirror an existing lens (e.g., `lens-business`) for shape and tone.
5. **Author the persona agent** — `.claude/agents/<persona>.md` with `tools: [Read, Grep, Glob]`, the output schema (Headline / Evidence anchors / Proposal / Open questions / Conflicts / Risks), and the lens binding.
6. **Update the orchestrators** — `aisa-round` (Discovery) and/or `aisa-frame`/`aisa-options`/`aisa-decide` to include the new lens in the order or council launch list.
7. **Update the question bank** in each pack — add 5+ questions for the new lens.
8. **Update `library/kernel/phases.md`** — declare the new lens in the relevant phase's "Lenses active" line.
9. **Update `library/kernel/glossary.md`** with the new lens definition.

## Modifying an existing lens

- **Adding a universal signal** — list it in the `Signal catalog → Universal` section of the lens SKILL.md and ensure the question bank covers it for each pack.
- **Adding a pack-specific signal** — *do not touch the lens*. Add the signal to that pack's `pack.yaml → lenses_config.<lens>.extra_signals`. The lens picks it up at runtime via the pack metadata.
- **Changing the persona stance** — be cautious. The persona stance is what gives the lens its independent voice in council mode. If you change it, also update the persona agent file and re-run a council-independent phase on a fixture engagement to verify the synthesis still holds.
- **Tightening hard rules** — fine, but propagate the same wording to the persona agent file so the council-independent mode honours it identically.

## Auditing a lens

Quick checks before declaring a lens change "done":

1. Frontmatter has `name` and `description`.
2. The six required body sections exist in the right order.
3. The hard-rules section names the no-tech rule and the append-only rule.
4. The execution steps include a "read every file in inputs/" step with the format-to-tool mapping reference.
5. Grep for vendor names in the lens file (except `lens-technology`) → must be 0 hits.
6. The persona agent file `.claude/agents/<persona>.md` mentions the lens binding and mirrors the hard rules.
7. The question bank in each pack covers the lens with ≥5 questions.

## Anti-patterns

- **Inventing a state** outside the kernel's 5 (`Confirmed / Assumed / Unknown / Conflicted / Risky`). If the row does not fit any of those, the gap is in the row's evidence, not in the state set.
- **Resolving a conflict silently** by picking a winner. Conflicts must surface as Conflicted rows; the user resolves at `/decide`.
- **Writing prose interpretation in the SU.** The SU rows are atomic claims. The interpretive paragraph belongs in `lens-outputs/<lens>.md`.
- **Naming a vendor in Discovery or Framing**, even hypothetically ("we could use Power Automate for this"). The proper formulation is "we need automation that triggers on … and writes to …". The technology lens picks up the vendor question in Options.
