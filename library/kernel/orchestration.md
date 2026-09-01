# Orchestration — Kernel v0.2.0

## Mode declaration

Each phase declares its mode in [`phases.md`](phases.md):

- **`inline`**: lenses run sequentially in the current thread, sharing accumulated context. Used in Discovery.
- **`council-independent`**: each lens runs as a Task subagent (concurrent), seeing only `context.json` + a thematic Shared Understanding excerpt. The chairman synthesizes outputs. Used in Framing/Options/Decision.

## Reading input documents

Lenses (and council agents) treat everything under `<engagement>/inputs/` as **primary evidence** and must open and parse it — never cite it by filename alone. Pick the tool by format:

| Format | How to read |
|---|---|
| `.md`, `.txt`, `.json`, `.csv` | read directly |
| `.xlsx`, `.xlsm` | the `xlsx` skill, or `openpyxl` / `pandas` (profile: sheets, columns, row counts, value distributions, date ranges) |
| `.pdf` | the `pdf` skill |
| `.docx` | the `docx` skill |
| `.pptx` | the `pptx` skill |
| images | read directly (vision) |

**Rule**: never record a `Confirmed` or `Assumed` row that cites an input you have not actually opened. Cite the specific value, column, or passage you found. If an input is anonymized/obfuscated, the structure (columns, counts, dates, distributions) is still valid evidence.

## Inline mode

- Order is fixed in `phases.md`: `business → operations → user → data → governance → financial` (Discovery).
- Each lens reads: `context.json`, `shared-understanding.md`, `lens-outputs/` (of previous lenses in this round).
- Each lens writes: rows to the Shared Understanding + `lens-outputs/<lens>.md`.
- The orchestrator skill (`aisa-round`) drives the sequence.

## Council-independent mode

- 6 or 7 agents launched **in parallel via concurrent Task subagents**.
- Each agent receives:
  - `context.json` (read-only).
  - A thematic Shared Understanding excerpt curated by the orchestrator (e.g., for the data lens: only `lens: data` rows).
  - It does **not** receive other agents' outputs in-flight.
- Each agent has `tools: [Read, Grep, Glob]` (no Write).
- When all agents return, the `chairman-synthesis` skill:
  - Reads all agent outputs.
  - Identifies overlaps, gaps, contradictions.
  - Writes new rows to the Shared Understanding.
  - Writes `chairman-synthesis-<round>.md` in `lens-outputs/` (`F-<NN>` in Framing, `O-<NN>` in Options — the Decision phase runs no council synthesis).

## Dialectic round

Full peer review was rejected for cost. Its surgical replacement: when the chairman detects **material divergences** between persona outputs (claim vs counter-claim that would change the phase artefact), the orchestrator runs an antithesis round for those points ONLY — each side attacks the other's strongest thesis and returns `Concedo / Contesto / Síntese proposta`. Cap: **3 divergences × 2 calls = ≤6 extra passes** per council round. Divergences that survive the antithesis become Conflicted rows; the chairman never silently picks a winner. Thesis → antithesis → synthesis, only where there is real disagreement.

## Why parallel (not sequential isolated)

Concurrent Task subagents complete the council round in ~1 LLM-pass-time, versus ~6× for sequential isolated. Claude Code supports parallelism natively for the Task tool. There is no race-condition risk because agents do not share writable state.

## Peer review (omitted in MVP)

Karpathy's full pattern includes peer review (each agent comments on the neighbor's output). aisa omits the full version by cost; the **dialectic round** above is its surgical replacement — antithesis only where personas materially disagree.

## Cost envelope per engagement

- Discovery: ~6 lenses × ~2-3 rounds = 12-18 LLM passes (inline, cheaper per pass).
- Framing: 6 agents + 1 chairman = 7 passes (council) + 0-6 dialectic passes (only on material divergence).
- Options: 7 agents + 1 chairman = 8 passes (council, technology enters) + 0-6 dialectic passes.
- Decision: interactive (user-driven) + optional 1 solution-architect review (`/decide --consult`) + auto synthesize (5 topic packs) = 5-7 passes.
- Render: 6 deliverables × 1 composition pass = 6 passes.

**Total per engagement**: ~40-50 LLM passes.
