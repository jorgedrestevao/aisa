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

The body has six required sections in this order. The six sections and their order are the contract; what follows is what each one is *for*.

**Lens = perspective + minimal runtime contract.** The budget goes into perspective; mechanics live in the kernel contracts and the orchestrator invocation.

### 1. Role

The distinct, non-substitutable perspective: the persona stance and the 3–4 questions this lens sees every request through. It says what this perspective **notices and challenges** — and keeps the sharp stances literal (the operations lens *distrusts the documented process*).

Role carries no orchestration and no domain knowledge.

### 2. Inputs

One line: what this lens **privileges** in the shared evidence (e.g. the column profile in the extractions for `data`; exception passages in transcripts for `operations`; the full SU for `technology`). No filesystem enumeration, no format tables, no engagement-path resolution — the invocation carries those.

The evidence contract is `library/kernel/orchestration.md` → *Evidence contract — parse once, reason many*:

- **Parse once. Reason many.** The capture pass opens and parses `inputs/`; the lens reads the shared, already-ingested evidence (`_capture/`, entry point `evidence-index.md`). A lens is never required to open every file in `inputs/`.
- **Raw source inspection is selective** — appropriate when extraction may have lost relevant detail, a material claim depends on interpretation, evidence conflicts, provenance is insufficient, or the lens needs context the extraction did not preserve. **Verify raw evidence when material to confidence, not to satisfy a quota**: there is no mandatory spot-check count, per round or otherwise.

### 3. Outputs

Two surfaces, cleanly separated:

- **`shared-understanding.md`** — the **atomic** engagement knowledge/evidence state: one claim, question, conflict or risk per row, tagged `lens=<name>`, append-only.
- **`lens-outputs/<lens>.md`** — a **short perspective interpretation**, appended once per round under a `## <round> — <lens>` header (the round id in the file is a hard dependency of `pre-lens-order-check.py`). It communicates: **what matters** · **tensions / risks** · **open evidence**.

Keep the lens output lightweight. It is an interpretation, not a report: no long narrative, no restatement of the rows above it.

### 4. Hard rules

Only invariants that materially need **local visibility** — the ones that must fire mid-reasoning. Do not reproduce full definitions that a kernel contract already owns; prefer a short pointer.

Worth keeping locally: Discovery technology neutrality (where applicable) · no `Confirmed` without evidence · append-only Shared Understanding · evidence integrity (cite what you opened; never claim stronger support than the inspected evidence gives).

Owned by `library/kernel/states.md` and **not** reproduced in a lens: the semantics of `verificado_em`, `validade`, `custo`, `swing`, decay classes, expiry and transition mechanics. A lens keeps the *obligation* and its local default ("in doubt: `validade = organizacional`; never leave `custo`/`swing` blank"), never the tables.

### 5. Signal catalog

**Signals are attention cues, not checklist items.** Universal signals belong to the kernel lens — a short token list, no prose. Pack-specific Discovery signals are **not** authored here: they live in `pack.yaml → lenses_config.<lens>.extra_signals` and reach the lens through the runtime invocation.

Explicitly not the contract: *"every signal must be covered"*, or *"create an Unknown for every uncovered signal"*. An uncovered cue is not a gap.

### 6. Execution steps

The minimum reasoning loop, not a re-statement of orchestration:

1. understand the relevant evidence (shared first; raw when material to confidence);
2. **apply the lens perspective** — the signature reasoning move, the only step that differs materially between lenses;
3. probe material gaps, assumptions and contradictions (including cross-lens tensions to hand downstream);
4. contribute material findings — SU rows + the three-heading block;
5. expose uncertainty rather than manufacture certainty.

No round bookkeeping, no next-free-id computation, no council-log appends: the orchestrator does those and passes what the lens needs.

Lenses MUST be idempotent: running them twice on the same input adds the next round's rows but never deletes or rewrites prior rows.

### Size

Lens files are meant to be lightweight (indicatively ~1,600 characters, with Role and step 2 the parts worth spending on). **Material growth beyond the lightweight target requires justification; size alone does not determine PASS/FAIL.** There is no character, token or signal-count limit, and no validator asserts one.

The target constrains **framework text**, not analysis — see *Reasoning depth* below.

### Reasoning depth

**Light framework, not lightweight reasoning.** A lens file defines *how to look*. It does not define *how much reasoning is allowed*. The compression this contract encodes removed repeated mechanics, never analytical coverage.

- **Signals do not bound reasoning.** A lens follows a material concern that emerges from the engagement even when no universal signal, no injected pack cue and no question-bank entry names it. Signals help attention; the absence of a signal is not permission to ignore a material concern.
- **Compact output is not shallow reasoning.** `lens-outputs/<lens>.md` stays a short interpretation and SU rows stay atomic — but the reasoning behind *what is material enough to record* may be substantial. Output verbosity is not a proxy for analytical quality.
- **Materiality determines depth.** Depth rises with materiality, uncertainty, risk and decision consequence — dependencies, contradictions, cross-domain implications, reversibility. A low-risk engagement earns broad awareness with shallow depth on immaterial concerns; an engagement that exposes regulatory, data or operational consequence earns deep treatment of what it exposed. Neither outcome is a checklist.
- **A persona mandate is a focus, not a boundary.** The phase bullets in `.claude/agents/<persona>.md` say where that voice starts, not where it must stop. A council persona follows material evidence its mandate did not enumerate.
- **Do not answer this by growing the file.** The principle lives here and in `library/kernel/orchestration.md`; it is not restated in seven lens files.


## Hard rules every lens must obey

1. **No vendor/product names** before Options (`.claude/rules/no-tech-mention-before-options.md`). Existing systems may be named *as current state* (e.g., "the spreadsheet that anchors approvals today"). The only exception is `lens-technology`, which activates in Options.
2. **No Confirmed without evidence.** Direct citation (document, USER_ANSWER, sponsor statement) → Confirmed. Inference from industry pattern → Assumed (basis declared). Missing → Unknown (with `quem responde` + `criticidade`). Disagreement between ≥2 sources → Conflicted.
3. **Identify in the `lens` column.** Always `<lens-name>` (e.g., `business`, `governance`).
4. **Append-only on the Shared Understanding.** Never delete or rewrite an existing row. State transitions add a new row that references the old (`was X-NNN`); the old row stays for audit. See `library/kernel/states.md`.
5. **Evidence integrity.** Read the shared evidence (`_capture/`, entry point `evidence-index.md`); inspect a raw source in `inputs/` when it is material to confidence. Never cite an input by filename alone — cite the specific value, column, passage or locator you actually opened. **Never claim stronger evidential support than the evidence you inspected supports**: weaker → `Assumed` with the basis declared, or `Unknown`. Raw sources are authoritative on conflict. Full contract: `library/kernel/orchestration.md` → *Evidence contract — parse once, reason many*.
6. **Stamp and price what you write** — `Confirmed`/`Assumed` carry `verificado_em` + `validade`; `Unknown` carry `custo` + `swing`. In doubt: `validade = organizacional`; never leave `custo`/`swing` blank. An expired row reads as weak `Assumed` — never cite it as `Confirmed`. Semantics: `library/kernel/states.md` (not restated in the lens file).

### Signals and pack context

- **Signals are attention cues, not checklist items** (§5 above): nothing requires full coverage, and an uncovered signal never becomes an `Unknown`.
- **The six Discovery lenses are pack-agnostic.** They do not read `pack.yaml` and do not resolve the active pack. Pack-specific cues arrive injected by the orchestrator as a token list, with the mandatory trailing clause *"cues, not a checklist; uncovered cues are not gaps"*.
- **`lens-technology` is the one documented exception**: Options-only and pack-aware. It may selectively consult the pack's `decision-tree.md`, the relevant `domain-knowledge/*.md`, and `lenses_config.technology.constraints_to_check`. It does not load the whole domain-knowledge base by default — **domain knowledge is pull-based, not push-based**. The exception does not travel: a Discovery lens reading `pack.yaml` is a contract violation, not a precedent.
- **`question-bank.md` is a question-generation resource, not permanent lens context.** No lens loads it. It is consulted selectively, at question-generation time, to phrase askable questions around material `Unknown` / `Conflicted` / `Risky` rows and evidence gaps. See `library/kernel/orchestration.md` → *Question bank — runtime role*.

## Adding a new lens

If you need a perspective the kernel's 7 do not cover (rare — most needs become signal additions on an existing lens), follow this checklist:

1. **Justify the lens** — what perspective is genuinely missing? If the answer is "a sub-aspect of business" or "a sub-aspect of governance", add a signal to that lens instead.
2. **Pick the persona** — what real-world role embodies this lens? The persona becomes the council-independent agent (`.claude/agents/<persona>.md`).
3. **Pick the phase activation** — Discovery + council-independent (the default for the 6), or council-independent-only like `lens-technology`.
4. **Author the SKILL.md** — follow the 6-section template; mirror an existing lens (e.g., `lens-business`) for shape and tone.
5. **Author the persona agent** — `.claude/agents/<persona>.md` with `tools: [Read, Grep, Glob]`. **Agent = independent perspective + mandate**: identity, perspective, phase mandate, what it challenges, memory binding, and a one-line lens pointer. It does *not* carry kernel state semantics, orchestration, the full lens procedure, the common return schema, or domain knowledge — those belong to the council invocation layer (`library/kernel/orchestration.md` → *Council-independent mode*), and the return schema is owned by `chairman-synthesis`. A persona is not required to re-read its lens `SKILL.md`.
6. **Update the orchestrators** — `aisa-round` (Discovery) and/or `aisa-frame`/`aisa-options`/`aisa-decide` to include the new lens in the order or council launch list.
7. **Update the question bank** in each pack — add 5+ questions for the new lens.
8. **Update `library/kernel/phases.md`** — declare the new lens in the relevant phase's "Lenses active" line.
9. **Update `library/kernel/glossary.md`** with the new lens definition.

## Modifying an existing lens

- **Adding a universal signal** — list it in the `Signal catalog → Universal` section of the lens SKILL.md and ensure the question bank covers it for each pack.
- **Adding a pack-specific signal** — *do not touch the lens*. Add the signal to that pack's `pack.yaml → lenses_config.<lens>.extra_signals`. The **orchestrator** resolves the active pack and injects those cues into the lens invocation; the Discovery lens itself never reads `pack.yaml`. Cues, not a checklist. Authoring heuristic (soft): prefer ~5–8 high-value extra signals per Discovery lens — see `docs/PACK_AUTHORING.md`.
- **Changing the persona stance** — be cautious. The persona stance is what gives the lens its independent voice in council mode. If you change it, also update the persona agent file and re-run a council-independent phase on a fixture engagement to verify the synthesis still holds.
- **Tightening hard rules** — fine. Do *not* copy the new wording into the persona file: the rules that bind a council persona are carried by the council invocation (`library/kernel/orchestration.md` → *Council-independent mode*). One channel, so the two modes cannot drift apart.

## Auditing a lens

Quick checks before declaring a lens change "done":

1. Frontmatter has `name` and `description`.
2. The six required body sections exist in the right order.
3. The hard-rules section names the no-tech rule and the append-only rule.
4. The Inputs section names what the lens privileges in the **shared** evidence and does not enumerate `inputs/`; raw inspection is described as selective and materiality-based, with **no** spot-check quota.
5. Grep for vendor names in the lens file (except `lens-technology`) → must be 0 hits.
6. The persona agent file `.claude/agents/<persona>.md` states its identity, mandate and a lens-pointer line — and does *not* re-implement the lens procedure, the return schema, or state semantics.
7. The question bank in each pack covers the lens with ≥5 questions (a pack authoring resource — never loaded as lens context).
8. No per-signal coverage loop anywhere in the file, and no claim that an uncovered signal is a gap.

Not checked, by design: character counts, token counts and signal counts. They are authoring heuristics, never PASS/FAIL conditions, and no validator asserts them.

## Anti-patterns

- **Inventing a state** outside the kernel's 5 (`Confirmed / Assumed / Unknown / Conflicted / Risky`). If the row does not fit any of those, the gap is in the row's evidence, not in the state set.
- **Resolving a conflict silently** by picking a winner. Conflicts must surface as Conflicted rows; the user resolves at `/decide`.
- **Writing prose interpretation in the SU.** The SU rows are atomic claims. The interpretive paragraph belongs in `lens-outputs/<lens>.md`.
- **Treating brevity as a stopping rule.** Ending analysis, dropping a material tension or skipping a cross-domain implication in order to keep the file or the output small. Compress repetition, not decision coverage.
- **Turning signals into coverage.** "Every signal must be covered", or an `Unknown` created for each uncovered cue. Signals are attention cues; uncovered is not a gap.
- **Reading `pack.yaml` from a Discovery lens.** Pack cues arrive by orchestrator injection. `lens-technology` is the only pack-aware lens, and only in Options.
- **Re-stating a kernel contract locally.** Stamping tables, decay classes, SU append mechanics and return schemas have one authoritative home each; a lens carries the obligation and, where needed, its local default — never the tables.
- **Naming a vendor in Discovery or Framing**, even hypothetically ("we could use Power Automate for this"). The proper formulation is "we need automation that triggers on … and writes to …". The technology lens picks up the vendor question in Options.
