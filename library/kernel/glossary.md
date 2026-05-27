# Glossary — Kernel v0.1.0

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
| **Hard guard** | A hook-enforced rule (only one: `library/` is read-only at runtime). |
| **Chairman** | The synthesizer in council-independent mode. The only writer to the SU in that mode. |
| **Council** | The agents (one per lens) running in parallel via Task subagents. |
