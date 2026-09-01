# aisa — Project Memory

## What this is

**aisa** is a multi-perspective discovery & sensemaking platform for the pre-development phase of digitalization projects (Power Platform, OutSystems, Mendix, custom). It runs as a Claude Code project.

> **Full architecture**: `docs/ARCHITECTURE.md`
> **Philosophy**: `docs/PHILOSOPHY.md`
> **Onboarding**: `docs/ONBOARDING.md`

## Operating principles (inviolable)

1. **Discovery before solution, always.** Lenses do not mention vendor/product before the Options phase.
2. **Shared Understanding as process artefact; deliverables as transition artefacts.** SU is the source of truth during the engagement; the 6 deliverables are rendered at the end.
3. **5 knowledge states**: Confirmed / Assumed / Unknown / Conflicted / Risky. No state×tag combinatorics. Confirmed/Assumed carregam validade — conhecimento expira e revalida-se (`library/kernel/states.md` → *Epistemic half-lives*).
4. **Council híbrido** by phase: inline in Discovery; council-independent (parallel subagents) in Framing/Options. Decision is interactive (user-driven; optional `/decide --consult` technology review).
5. **Soft gates**: warnings, overrideable with justification. The only hard rule is `library/` is read-only at runtime.
6. **Native Claude Code primitives**: skills, agents, hooks, commands. No reinvention.
7. **Pack activo per-engagement**: declared in `projects/<slug>/_state.json.pack`. Not global.
8. **Atomic writes** to `_state.json`: tmp → mv pattern.

## Key paths

- `library/kernel/` — universal protocols (phases, states, orchestration, render-contract, glossary).
- `library/packs/<id>/` — domain-specific (PP, OS, Mendix). Read-only at runtime.
- `.claude/skills/` — lenses + commands + synthesis + render.
- `.claude/agents/` — personas for council-independent mode.
- `.claude/hooks/` — programmatic enforcement.
- `projects/<slug>/` — engagement state (mount point to private repo).

## Slash commands

| Command | Purpose |
|---|---|
| `/start <slug> [pack]` | New engagement |
| `/round [lens]` | Run a Discovery round (auto or specific lens) |
| `/answer <id> "..."` | Resolve an Unknown/Conflicted/Assumed/Risky row (state transition + answers.md) |
| `/status` | Show phase, round, SU summary, gaps |
| `/frame` | Transit to Framing phase |
| `/options` | Transit to Options phase |
| `/simulate [O-NNN ...]` | Project each option (screens, effort, risks) + decision-flipping Unknowns, before `/decide` |
| `/premortem [--horizon <meses>]` | Write the project's obituary before deciding — failure causes anchored to SU ids; mitigations → requirements/tripwires |
| `/decide [--consult]` | Capture decision; auto-runs `/synthesize` |
| `/blueprint` | Produce the UX blueprint (screen architecture) from the SU + pack rules; iterate to business approval |
| `/synthesize` | Produce topic packs (auto after `/decide` or manual) |
| `/render [deliverable\|--all]` | Render the deliverables (filtered by decision type) |
| `/resume` | Resume from `_state.json` and name the next command |

## Anti-patterns to avoid

- Naming Power Platform / OutSystems / Mendix / Dataverse before the Options phase.
- Editing `library/` at runtime (hook will reject).
- Inventing claim states without evidence (use Unknown instead).
- Bypassing `/synthesize` between `/decide` and `/render`.

## Where things live

For full layout: `docs/ARCHITECTURE.md §6`.
