# Glossary — Kernel v0.2.0

Universal aisa vocabulary (not pack-specific). Pack-specific terms live in `library/packs/<id>/glossary.md`.

| Term | Definition |
|---|---|
| **Engagement** | A complete aisa run, from `/start` to `/render --all`, on a single client need. |
| **Phase** | One of Discovery, Framing, Options, Decision. See [`phases.md`](phases.md). |
| **Round (ronda)** | One pass through a phase. Multiple rounds per phase are normal. |
| **Lens** | A perspective skill (business, operations, ...). Independent, idempotent. |
| **Mode** | Orchestration style: `inline` (sequential, shared context) or `council-independent` (parallel, isolated). See [`orchestration.md`](orchestration.md). |
| **State** | One of Confirmed, Assumed, Unknown, Conflicted, Risky. See [`states.md`](states.md). |
| **Shared Understanding (SU)** | The living artefact `shared-understanding.md` — the single source of truth during an engagement. |
| **Lens output** | The prose narrative each lens writes in `lens-outputs/<lens>.md`. |
| **Topic pack** | An intermediate synthesized artefact in `_synthesis/`. 5 per engagement. |
| **Deliverable** | A final rendered artefact for handoff. 6 canonical per engagement. |
| **Pack** | A domain configuration (pp, outsystems, mendix, generic). |
| **Soft gate** | Advisory warning at a phase transition. Overrideable with logged justification. |
| **Hard guard** | A hook-enforced rule. Three: `library/` is read-only at runtime, `_state.json` writes are atomic, and Discovery lenses run in order. |
| **Process capture** | Reading an engagement input file (`.xlsx`/`.xlsm`) for the process logic it encodes, before any lens looks at it. Three layers: deterministic extraction, replay, and the process model. Run by `/capture`, automatically at `/start` and when a file changes. |
| **Extraction** | The machine record of what a file *is* — sheets, columns classified as input/derived/manual, formula patterns, validation and formatting rules, colour used as data, anomalies. Deterministic: no judgement, no LLM. Cached on the file's checksum. |
| **Replay** | Re-running a fixed battery of checks against the file's own data — lookups, key uniqueness, whitespace, ageing, pattern exceptions, orphan references — so silent failures surface mechanically. Rule: **no check = no claim**; anything outside the battery is listed as not replayable, never guessed. |
| **Process model** | `_capture/process-model.md` — the as-is logic reconstructed as evidenced rules plus questions. Discovery-facing; lenses read it first but must spot-check it. |
| **PM-NNN** | A business rule in the process model. Always cites a cell or range. Carries `verificado_em` (the *file's* last-edit date) and `validade`, like any SU row. |
| **PM-U-NNN** | A question in the process model's interrogation list — what the file implies but cannot prove. Priced with `custo` and `swing`, so a lens can promote it to an SU Unknown without inventing them. |
| **Spot-check** | The rule that each lens verifies at least one process-model claim against the raw file per round. The raw file is always authoritative; a mismatch becomes a Conflicted row. It is what stops one wrong model from poisoning six lenses at once. |
| **Manual column** | A column of typed values with no formula — someone maintains it by hand. Read as a human step in the process, and one of the strongest signals the file gives. |
| **Chairman** | The synthesizer in council-independent mode. The only writer to the SU in that mode. |
| **Council** | The agents (one per lens) running in parallel via Task subagents. |
| **Half-life (validade)** | Decay class of a Confirmed/Assumed row; past it, the row is expired and must be revalidated. See [`states.md`](states.md). |
| **Custo / Swing** | The price of answering an Unknown and what changes if answered (`decisivo`/`dimensionante`/`cosmético`). Drives the meeting agenda and VOI. |
| **Meeting agenda** | `/status` output: the questions worth the sponsor's synchronous time, ranked by swing — and the ones explicitly not worth it. |
| **Pre-mortem** | The project's obituary written before `/decide`; causes anchored to SU ids, mitigations become requirements/tripwires. |
| **Story** | `story.md` — the engagement narrated episode by episode in sponsor language; a projection of the SU, not a source. |
