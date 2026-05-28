# Orchestration — Kernel v0.1.0

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
  - Writes `chairman-synthesis-R<NN>.md` in `lens-outputs/`.

## Why parallel (not sequential isolated)

Concurrent Task subagents complete the council round in ~1 LLM-pass-time, versus ~6× for sequential isolated. Claude Code supports parallelism natively for the Task tool. There is no race-condition risk because agents do not share writable state.

## Peer review (omitted in MVP)

Karpathy's full pattern includes peer review (each agent comments on the neighbor's output). The aisa MVP omits this. Add in v2 if production observes group-think (unlikely given full isolation).

## Cost envelope per engagement

- Discovery: ~6 lenses × ~2-3 rounds = 12-18 LLM passes (inline, cheaper per pass).
- Framing: 6 agents + 1 chairman = 7 passes (council).
- Options: 7 agents + 1 chairman = 8 passes (council, technology enters).
- Decision: 1 chairman + auto synthesize (5 topic packs) = 6 passes.
- Render: 6 deliverables × 1 composition pass = 6 passes.

**Total per engagement**: ~40-50 LLM passes.
