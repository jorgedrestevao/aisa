# aisa

<!-- SCOPE-STATEMENT v1 -->
**aisa runs discovery on a process to reach a grounded technical decision: which technology and pattern, against which alternatives, at what cost. It is not an open-ended business-discovery platform; a question is admitted only when its answer can change the decision.**

Built for engagements that precede the choice of digitalization technology (Power Platform, OutSystems, Mendix, custom). It runs as a Claude Code project — skills, agents, hooks and slash commands, no service and no database.

## Why

Most digitalization projects fail in **discovery**, not in implementation. Stakeholder misalignment, incomplete understanding, fragmented context and premature technology selection are the dominant failure modes. aisa exists to make discovery thorough, multi-perspective, and to pre-empt those failures.

## What it does

Four phases — **Discovery → Framing → Options → Decision** — facilitated by 7 perspectives (business, operations, user, data, technology, governance, financial). The technology perspective activates only in Options: no vendor or product is named before then, and a hook enforces it.

What the engagement carries while it runs is the **Shared Understanding** — every claim in one of five knowledge states (Confirmed · Assumed · Unknown · Conflicted · Risky), each with its evidence, its owner and its expiry date. Knowledge expires and is revalidated; questions carry a price; decisions keep their counterfactuals. The 6 deliverables are rendered at the end, from that understanding — they are the handoff, not the working state.

## Commands

`/start` · `/round` · `/capture` · `/answer` · `/status` · `/frame` · `/options` · `/simulate` · `/premortem` · `/decide` · `/blueprint` · `/synthesize` · `/render` · `/revisit` · `/retro` · `/resume` · `/dashboard`

A message with no command that describes a process or asks for a result is the main entry point, not an error — it orients and proposes `/start`.

Full table with what each one does: [`CLAUDE.md`](CLAUDE.md).

## How state survives

The engagement's state lives in the repository, not in a session. Six deterministic motors (stdlib only) make it durable:

| | |
|---|---|
| `graph.py` | the engagement's additive graph; mirrors the Shared Understanding and never prevails over it |
| `operation.py` | the coordinator — every knowledge write goes through intent → pending marker → publish → verify → receipt |
| `bootstrap.py` | the common reconstruction that readers and writers consult **before** concluding |
| `resolve.py` | state transitions and the four lifecycle operations |
| `migrate.py` | legacy → persistent memory, and the graph a new engagement is born with |
| `projection.py` | operational state in business language: blockers with reason, evidence and action |

Two limits are stated rather than papered over: atomicity is **observable to supported readers**, not a filesystem transaction; and a derived artefact citing a row that changed is a suspicion, not proof that it predates the change — the engine returns candidates, the verdict is human.

## Quick start

- Using it: [`docs/COMO-USAR.md`](docs/COMO-USAR.md) — one page, in business language.
- Setting it up or extending it: [`docs/ONBOARDING.md`](docs/ONBOARDING.md).

## Documents

| Document | For |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | Project memory: operating principles, key paths, every command |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Technical architecture and contracts |
| [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md) | Why aisa exists; for non-technical audiences |
| [`docs/COMO-USAR.md`](docs/COMO-USAR.md) | One page for whoever runs an engagement |
| [`docs/ONBOARDING.md`](docs/ONBOARDING.md) | Setup + first engagement walkthrough (consultant / developer) |
| [`library/kernel/`](library/kernel/) | The contracts themselves — phases, states, orchestration, render, blueprint, coverage, glossary |
| [`docs/PACK_AUTHORING.md`](docs/PACK_AUTHORING.md) · [`docs/LENS_AUTHORING.md`](docs/LENS_AUTHORING.md) | Writing a technology pack or a perspective |
| [`docs/evolution/`](docs/evolution/) | How it got here: one report per phase, P0–P8 |

## Status

Built and running, under continuous hardening. 65 test files, ~2480 cases, stdlib-only Python.

**Not yet demonstrated**: that a fresh Claude Code session, with no answer given to it in advance, drives a real engagement end to end through the kernel. That is what `docs/evolution/p8/PROTOCOLO.md` exists to establish, and until those runs exist the comparator returns `SEM EXECUÇÃO` — never a pass. Nothing else in this repository substitutes for it.

## License

Internal Galp use. Contact Jorge Estêvão for distribution.
