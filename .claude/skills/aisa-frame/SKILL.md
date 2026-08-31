---
name: aisa-frame
description: Transition Discovery → Framing. Checks Discovery's soft exit gate, flips _state.json to phase=framing/round=F-01, launches 6 council personas in parallel via the Task tool (council-independent mode), then invokes the chairman-synthesis skill to write frame.md and the synthesised Shared Understanding rows. On user validation, registers D-001 in decisions.md.
---

# aisa-frame

## Usage

`/frame [--override "<reason>"]`

- No argument: runs the soft gate check; if any criterion is red and no override is provided, stop with a clear summary and ask the user before proceeding.
- `--override "<reason>"`: bypass the soft gate. The reason is logged in `decisions.md`.

## Phase model

- **From**: `phase: discovery`.
- **To**: `phase: framing`, `round: F-01` (subsequent framing rounds become `F-02`, `F-03`, …, by re-running `/frame`).
- **Mode**: `council-independent`. See `library/kernel/orchestration.md`.

The aisa-frame skill is itself **NOT a lens** — it does no lens analysis. It is the orchestrator that fans out to the 6 council personas (Discovery lenses, embodied as agents) and then in-fans to the chairman synthesis.

## Inputs (read)

- `<engagement>/_state.json`, `<engagement>/context.json`, `<engagement>/shared-understanding.md`, `<engagement>/decisions.md`, `<engagement>/council-log.md`.
- `<engagement>/lens-outputs/*.md` (so you can compose each persona's thematic SU excerpt).
- `library/kernel/phases.md` (Framing entry criteria).
- `library/packs/<pack>/pack.yaml` (for any pack-driven persona signals).

`<engagement>` resolves to `$AISA_ENGAGEMENTS_ROOT/<slug>` if set, otherwise `projects/<slug>`. `<pack>` is read from `_state.json.pack`.

## Outputs (written, via chairman-synthesis except where noted)

- `<engagement>/_state.json` (atomic write — this skill).
- `<engagement>/frame.md` (chairman-synthesis).
- New rows in `<engagement>/shared-understanding.md` (chairman-synthesis).
- `<engagement>/lens-outputs/chairman-synthesis-F-<NN>.md` (chairman-synthesis).
- `D-001` line in `<engagement>/decisions.md` after the user validates the frame sentence (this skill, on validation).
- `<engagement>/council-log.md` summary lines (this skill + chairman-synthesis).

## Execution steps

### 1. Pre-flight

1. Resolve the engagement root and read `_state.json`. If `phase != discovery` → stop with: "/frame transitions Discovery → Framing; current phase is `<phase>`. Use /options or /decide instead." Exception: if `phase == framing` already, treat this as a re-run (subsequent framing round).
2. Read `library/kernel/phases.md`, section "Phase 2: Framing — Entry criteria".

### 2. Soft gate check (Discovery exit criteria, advisory)

Compute from `shared-understanding.md`:

- `confirmed_count` — rows in `## Confirmed`.
- `unknown_critical_count` — rows in `## Unknown` with `criticidade = Critical`.
- `conflicted_critical_count` — rows in `## Conflicted` with `criticidade = Critical`.
- `lenses_with_output` — set of lens narratives present under `lens-outputs/` (expect `business`, `operations`, `user`, `data`, `governance`, `financial`).

Soft criteria from `phases.md`:
- `confirmed_count ≥ 10`.
- `unknown_critical_count == 0`.
- `conflicted_critical_count == 0`.
- `len(lenses_with_output) == 6`.

If any criterion is red AND no `--override` was passed → stop with a one-line-per-criterion summary and ask the user: "Proceed anyway (re-run with `--override "<reason>"`)? Or run more Discovery rounds (`/round`)?" Do not transition yet.

If `--override` is set, log the override reason — it goes into `decisions.md` as part of D-001 metadata.

### 3. Flip state to Framing (atomic)

1. Determine the framing round:
   - If `_state.json.round` does not yet start with `F-` → set `round = F-01`.
   - Else → increment (`F-01` → `F-02`).
2. Update `_state.json`: `phase = framing`, `round = <F-NN>`. Write atomically: `_state.json.tmp` → `Move-Item -Force` (Windows) / `mv` (Unix).
3. Update the SU header `Fase actual: Framing` and `Última actualização: <ISO timestamp>`.

### 4. Compose thematic Shared Understanding excerpts

For each of the 6 personas, slice the SU into a thematic excerpt:

| Persona | Slice |
|---|---|
| business-analyst | All rows where `lens = business` + any row touching shadow stakeholders, KPIs, sponsor authority |
| operations-lead | All rows where `lens = operations` + any row touching as-is process steps, volumes, cycle times |
| user-advocate | All rows where `lens = user` + any row touching personas, devices, accessibility |
| data-steward | All rows where `lens = data` + any row touching sensitivity, ownership, retention |
| compliance-officer | All rows where `lens = governance` + every Conflicted row + every row touching audit/access control |
| cfo-lens | All rows where `lens = financial` + any row touching cost, volume × time anchors |

Each excerpt is a Markdown fragment with the section headers preserved. **Every excerpt must ALSO include the resolved rows and their resolutions** (rows marked `resolved →` plus the `C-` rows carrying `(was …)`), under a heading "Resoluções já fechadas (não re-litigar)" — otherwise personas whose slice missed a resolution re-raise closed conflicts (observed in live validation). Save each as a transient file under `<engagement>/lens-outputs/_council-prep/F-<NN>-<persona>.md` so the audit trail can show what each agent saw. Save the union of these into the council-log too.

**solution-architect is NOT invoked in Framing.** Do not launch it. (Its own agent file refuses if called pre-Options.)

### 5. Launch the 6 personas in parallel via the Task tool

Send **one assistant message with 6 Task tool calls** so they execute concurrently. Each Task call:

- `subagent_type`: the persona name (`business-analyst`, `operations-lead`, `user-advocate`, `data-steward`, `compliance-officer`, `cfo-lens`).
- `description`: e.g., "Framing F-01 — business angle".
- `prompt`: self-contained brief, structured as:

```
You are running in council-independent mode for the Framing phase, round F-<NN>, of engagement <slug> (pack: <pack>).

Your lens binding and output format are in `.claude/agents/<your-persona>.md`. You do not write any file directly — you return your structured proposal as your tool result.

Read:
- `<engagement>/context.json`
- `<engagement>/lens-outputs/_council-prep/F-<NN>-<your-persona>.md` (your thematic SU excerpt)
- every file under `<engagement>/inputs/` per `library/kernel/orchestration.md` → *Reading input documents*
- your lens skill at `.claude/skills/lens-<your-lens>/SKILL.md` for the hard rules
- (optional) `.claude/agent-memory/_universal/<your-persona>/*.md`

Mandate (Framing): propose the single sentence "The problem is X, felt by Y, costs Z today, evidence is W." from your angle, and provide evidence anchors, open questions, conflicts, and risks per your output schema.

Hard rule: do NOT name any vendor or product. Discovery and Framing are pre-technology by construction.

Return your response in the exact section format documented in your agent file.
```

Wait for all 6 to return. Collect their tool results verbatim.

### 6. Hand off to chairman-synthesis

Invoke the `chairman-synthesis` skill with:

- The 6 persona outputs (just collected).
- The current `<engagement>` paths.
- Phase = `framing`, round = `F-<NN>`.

The chairman-synthesis skill writes `frame.md`, the new SU rows, and the synthesis log. Wait for it to return.

### 7. Present the frame to the user and ask for validation

Output to the user:

```
Frame proposal (round F-<NN>):

  <single sentence from frame.md>

Anchors:
  - <bullet per clause>

Open questions still material:
  - <Unknown id> — <question>
Conflicts still open:
  - <Conflicted id> — <conflict>

Validate this frame?
  - "yes" → I will register it as D-001 in decisions.md.
  - "edit: <new sentence>" → I will save your edit and register that as D-001.
  - "more rounds" → I will roll the state back to discovery so /round runs again.
```

### 8. On validation, write D-001 (this skill)

Append to `<engagement>/decisions.md`:

```markdown

## D-001 — Frame agreed

- **Frame sentence**: <final agreed sentence>
- **Agreed in round**: F-<NN>
- **Anchors**: <list of clause → SU ids>
- **Override used at /frame**: <reason or "—">
- **Timestamp**: <ISO-8601>
```

Then append a one-line summary to `council-log.md`: "F-<NN> — frame agreed (D-001)".

### 8a. On "more rounds"

Roll back `_state.json.phase` to `discovery` and leave `round` at the last completed Discovery round (`R-NN`). Tell the user: "Returned to Discovery at `R-NN`. Run `/round` to continue."

### 8b. On "edit: <new sentence>"

Overwrite the single-sentence line of `frame.md` with the user's edit (preserve all other sections), then proceed with step 8 using the edited sentence.

### 9. Wrap-up output

"Framing F-<NN> complete. D-001 registered. Next: `/options` to enter the Options phase (the technology lens activates there). Run `/status` for the SU summary."

## Notes

- **Concurrency**: the 6 personas must launch in a single assistant message (one message with 6 parallel Task tool uses). Sequential launches defeat the cost envelope advantage described in `library/kernel/orchestration.md`.
- **Only the chairman writes the SU.** The 6 personas have `tools: [Read, Grep, Glob]` and return their proposals as text — they cannot write even if they tried.
- **Idempotence**: re-running `/frame` is allowed (produces F-02, F-03, …). The previous `frame.md` is overwritten; chairman-synthesis-F-<NN>.md from each round is preserved.
