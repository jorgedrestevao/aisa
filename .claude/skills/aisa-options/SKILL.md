---
name: aisa-options
description: Transition Framing → Options. Checks Framing's exit gate, flips _state.json to phase=options/round=O-01, launches 7 council personas in parallel via the Task tool (council-independent mode — adds solution-architect for the first time), then invokes chairman-synthesis to write options.md and synthesised Shared Understanding rows.
---

# aisa-options

## Usage

`/options [--override "<reason>"]`

- No argument: runs the soft gate check; if any criterion is red and no override is provided, stop with a clear summary and ask the user before proceeding.
- `--override "<reason>"`: bypass the soft gate. The reason is logged in `decisions.md`.

## Phase model

- **From**: `phase: framing`.
- **To**: `phase: options`, `round: O-01` (subsequent options rounds become `O-02`, `O-03`, …).
- **Mode**: `council-independent` with **7** personas (the 6 Discovery personas + `solution-architect`). The solution-architect activates here for the first time in the engagement — this is where vendor/product naming becomes allowed (via `lens-technology`).

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/council-log.md`.
- `<engagement>/frame.md` (the agreed problem sentence from Framing).
- `<engagement>/lens-outputs/*.md` (incl. any prior chairman-synthesis logs).
- `library/kernel/phases.md` (Options entry criteria).
- `library/packs/<pack>/pack.yaml`, `library/packs/<pack>/decision-tree.md`, `library/packs/<pack>/domain-knowledge/*.md` (solution-architect needs these).

## Outputs (written, via chairman-synthesis except where noted)

- `<engagement>/_state.json` — atomic write (this skill).
- `<engagement>/options.md` (chairman-synthesis).
- New rows in `<engagement>/shared-understanding.md` (chairman-synthesis).
- `<engagement>/lens-outputs/chairman-synthesis-O-<NN>.md` (chairman-synthesis).
- `<engagement>/council-log.md` summary lines (this skill + chairman-synthesis).

## Execution steps

### 1. Pre-flight

1. Resolve the engagement root and read `_state.json`. If `phase != framing` AND `phase != options` → stop with: "/options transitions Framing → Options; current phase is `<phase>`. Use /frame first." If `phase == options` already, treat as a re-run.
2. Verify `<engagement>/frame.md` exists and `decisions.md` contains a `D-001` line (frame agreed). If not → stop and ask the user to run `/frame` first or supply `--override "..."`.
3. Read `library/kernel/phases.md` (Options entry criteria).

### 2. Soft gate check

- Frame sentence registered in `decisions.md` (D-001) → must be true; the pre-flight already checks.
- Sponsor confirmation captured in D-001 (look for the `Frame agreed` block).

If a soft criterion is red and no `--override` was passed → stop with a one-line-per-criterion summary and ask the user. If `--override` is set, log the reason — it goes into `decisions.md` alongside D-NNN.

### 3. Flip state to Options (atomic)

1. Compute the options round:
   - If `_state.json.round` does not yet start with `O-` → set `round = O-01`.
   - Else → increment (`O-01` → `O-02`).
2. Update `_state.json`: `phase = options`, `round = <O-NN>`. Atomic write (`_state.json.tmp` → `Move-Item -Force` / `mv`).
3. Update the SU header `Fase actual: Options` and `Última actualização: <ISO timestamp>`.

### 4. Compose thematic Shared Understanding excerpts

Same slicing as `aisa-frame` for the first 6 personas — including the mandatory "Resoluções já fechadas (não re-litigar)" block in every excerpt. Add a 7th excerpt for `solution-architect`:

| Persona | Slice |
|---|---|
| solution-architect | The **full** Shared Understanding (the architect needs the cross-lens picture) + the pack metadata files listed in *Inputs* + `frame.md` |

Each excerpt is saved transiently under `<engagement>/lens-outputs/_council-prep/O-<NN>-<persona>.md` for the audit trail.

### 5. Launch the 7 personas in parallel via the Task tool

Send **one assistant message with 7 Task tool calls** so they execute concurrently. Each Task call:

- `subagent_type`: persona name (`business-analyst`, `operations-lead`, `user-advocate`, `data-steward`, `compliance-officer`, `cfo-lens`, `solution-architect`).
- `description`: e.g., "Options O-01 — architecture proposal".
- `prompt`: self-contained brief structured as:

```
You are running in council-independent mode for the Options phase, round O-<NN>, of engagement <slug> (pack: <pack>).

Your lens binding and output format are in `.claude/agents/<your-persona>.md`. You do not write any file directly — you return your structured proposal as your tool result.

Read:
- `<engagement>/context.json`
- `<engagement>/frame.md` (the agreed problem)
- `<engagement>/lens-outputs/_council-prep/O-<NN>-<your-persona>.md` (your thematic SU excerpt)
- For solution-architect: `library/packs/<pack>/decision-tree.md` and every file under `library/packs/<pack>/domain-knowledge/`
- every file under `<engagement>/inputs/` per `library/kernel/orchestration.md` → *Reading input documents*
- your lens skill at `.claude/skills/lens-<your-lens>/SKILL.md` for the hard rules
- (optional) `.claude/agent-memory/_universal/<your-persona>/*.md`

Mandate (Options):
- The 6 Discovery personas: for each candidate option you can imagine, assess fit through your lens — pros/cons/constraints — and feed that back. Hard rule: do NOT name vendors or products yourself; you are providing the *needs* and *constraint* lens.
- solution-architect: produce 3–5 candidate options against the SU + pack decision-tree.md. MUST include at least one do-nothing baseline and one non-technology option. For each: branch (from decision-tree.md), pros, cons, constraints checked, reversibility, indicative effort band. This is the ONLY persona that may name vendors/products.

Return your response in the exact section format documented in your agent file.
```

Wait for all 7 to return. Collect their tool results verbatim.

### 6. Hand off to chairman-synthesis

Invoke `chairman-synthesis` with the 7 persona outputs and phase = `options`, round = `O-<NN>`. The chairman writes `options.md` (≥3 options, ≥1 non-technology, ≥1 do-nothing) and the new SU rows.

### 7. Present options to the user

Output to the user:

```
Options round O-<NN> complete. <N> options proposed:

  - O-001 — <name> (<branch>) — effort <S|M|L>, reversibility <L|M|H>
  - O-002 — …
  - …

Open questions still material to Options:
  - <Unknown id> — <question>
Conflicts still open:
  - <Conflicted id> — <conflict>

Review `options.md`. When ready, run `/decide` to pick one and capture the rationale.
If options feel incomplete or the architect missed a branch, re-run `/options` (produces O-02).
```

### 8. Wrap-up output

"Options O-<NN> complete. Next: `/decide` (or re-run `/options` to add another round). Run `/status` for the SU summary."

## Notes

- **Concurrency**: the 7 personas must launch in a single assistant message (one message with 7 parallel Task tool uses), mirroring `aisa-frame`.
- **solution-architect is the lone vendor-naming surface.** The other 6 personas keep returning *needs and constraints*, never vendor choices, per `.claude/rules/no-tech-mention-before-options.md` (they run isolated and never see the solution-architect's output in-flight). The chairman, when synthesising, may name a vendor only where it is anchored to a solution-architect output; cross-lens rows not pinned to such an anchor stay technology-neutral.
- **Idempotence**: re-running `/options` produces O-02, O-03, …. The previous `options.md` is overwritten; each round's `chairman-synthesis-O-<NN>.md` is preserved.
