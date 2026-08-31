# aisa — Implementation Plan

**Plano operacional de build, passo-a-passo, para Claude (builder) executar autonomamente em múltiplas sessões.**

> Versão: v1.0.0 — pronto para arrancar Fase 1
> Data criação: 2026-05-27
> Audiência: Claude (LLM builder) + Jorge (reviewer/sponsor)
> Companion docs: [`ARCHITECTURE.md`](ARCHITECTURE.md) (spec normativa), [`PHILOSOPHY.md`](PHILOSOPHY.md), [`MIGRATION_FROM_AISA.md`](MIGRATION_FROM_AISA.md), [`ONBOARDING.md`](ONBOARDING.md).

---

## 0. Como usar este plano

### 0.1 Audiência

Este documento tem **dois leitores**:

1. **Claude (LLM builder)** — lê no início de cada sessão de build para saber exactamente o que construir a seguir. Cada fase está descrita ao nível de "qual ficheiro, com que conteúdo, com que acceptance criteria". Não há ambiguidade sobre o próximo passo.

2. **Jorge (sponsor/reviewer)** — usa para auditar progresso entre sessões. Cada fase termina com **acceptance criteria explícitos** que o Jorge pode validar antes de autorizar a próxima fase.

### 0.2 Modo de operação

- **Sessões discretas**: cada fase é tipicamente 1 sessão (~1-2h). Algumas fases pequenas podem partilhar sessão.
- **Resume entre sessões**: a §16 ("Resume tracking") mantém estado actual. Início de cada sessão lê isto antes de qualquer ficheiro.
- **TaskCreate por fase**: cada sessão arranca com `TaskCreate` para os items da fase + `TaskUpdate` à medida que progride.
- **Commit no fim de cada fase** (se git activo): mensagem `phase-N: <descrição>`.
- **Stop on red flag**: se algo durante o build viola a arquitectura ou levanta dúvida material, parar e perguntar ao Jorge antes de continuar.

### 0.3 Defaults assumidos (sobrescrever se Jorge indicar diferente)

| Default                                   | Valor                                                                                                                    | Razão                                               |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| Localização repo `aisa/`                  | **CONFIRMADO 2026-05-27**: `C:\Users\jorge.estevao\Documents\Galp\Claude Code Projects\aisa\` (sibling do SPEA v5)       | Não contaminar workspace existente; greenfield real |
| Localização repo `aisa-engagements-galp/` | **CONFIRMADO 2026-05-27**: `C:\Users\jorge.estevao\Documents\Galp\Claude Code Projects\aisa-engagements-galp\` (sibling) | Mesma razão; criação adiada para Fase 11            |
| Git desde dia 1                           | Sim, `git init` em Fase 1                                                                                                | Permite rollback granular; commit por fase          |
| MCP no MVP                                | Não (Fase 12+)                                                                                                           | Reduz scope inicial; aisa funciona sem MCP          |
| Hooks completos                           | Skeleton em Fase 1; hard hooks em Fase 11                                                                                | pre-write-guard early; resto à medida               |
| Estratégia deliverable templates          | Transplantação + refactor leve do pp-consulting                                                                          | Mais rápido que reescrever; preserva fidelidade     |
| Idioma do código/docs internos            | English (identificadores, comments); Portuguese (conteúdo PT-target)                                                     | Convenção Claude Code                               |
| Versão Claude para build                  | claude-opus-4-7 (mantém-se ao longo)                                                                                     | Estável para sessões longas; razão custo-qualidade  |

### 0.4 Constraints invioláveis

1. **Nada em `library/` é editável após Fase 11** — hook `pre-write-guard.sh` activa-se aí; antes disso, edits ainda são permitidos.
2. **Cada fase tem acceptance criteria objectivos** — não avançar para fase N+1 sem N estar verde.
3. **Cada sessão termina com `## Resume tracking` actualizado** no fim deste documento.
4. **Não inventar arquitectura** — se algo não está em ARCHITECTURE.md v0.2.0, parar e perguntar.
5. **`projects/` mantém-se vazio até Fase 11** — engagements reais só depois do MVP estar testado com fixture.

---

## 1. Fase 1 — Repo skeleton

**Objectivo**: criar `aisa/` com a estrutura mínima de directorias + ficheiros foundation. No fim da fase, `claude .` numa shell aberta em `aisa/` consegue arrancar sem erros.

**Sessão estimada**: 1 sessão, ~60-90 min.

**Pré-condições**: confirmar com Jorge a localização do repo (default em §0.3).

### 1.1 Acções

| # | Acção | Detalhe |
|---|---|---|
| 1.1.1 | Criar root directory | `mkdir aisa` em `Claude Code Projects/` |
| 1.1.2 | `git init` | Inicializar repo |
| 1.1.3 | Criar `.gitignore` | Conteúdo em §1.3 abaixo |
| 1.1.4 | Criar `.env.example` | Conteúdo em §1.3 abaixo |
| 1.1.5 | Criar estrutura de directorias | Lista em §1.2 |
| 1.1.6 | Criar `CLAUDE.md` | Princípios; ver §1.4 para conteúdo |
| 1.1.7 | Criar `README.md` | Entry point enterprise; ver §1.5 |
| 1.1.8 | Criar `.claude/settings.json` | Deny rules + hooks placeholders; ver §1.6 |
| 1.1.9 | Criar `.claude/rules/*.md` (4 ficheiros curtos) | Ver §1.7 |
| 1.1.10 | Criar `.claude/hooks/pre-write-guard.sh` (stub) | Ver §1.8 — versão MVP, não enforce yet |
| 1.1.11 | Commit inicial | `phase-1: foundation skeleton` |

### 1.2 Directory structure a criar

```
aisa/
├── .gitignore
├── .env.example
├── CLAUDE.md
├── README.md
├── .claude/
│   ├── settings.json
│   ├── rules/
│   ├── skills/                  (vazio, populado em fases seguintes)
│   ├── commands/                (vazio)
│   ├── agents/                  (vazio)
│   ├── agent-memory/
│   │   ├── _universal/          (vazio)
│   │   └── _tenant/             (vazio)
│   ├── hooks/
│   └── output-styles/           (vazio, opcional)
├── library/
│   ├── kernel/                  (vazio, populado na Fase 2)
│   └── packs/
│       ├── pp/                  (vazio, populado na Fase 3)
│       ├── outsystems/          (vazio)
│       ├── mendix/              (vazio)
│       └── generic/             (vazio)
├── projects/                    (vazio; mount point para repo privado em Fase 11)
└── docs/
    └── ARCHITECTURE.md          (copiar de aisa-design/ARCHITECTURE.md)
    └── PHILOSOPHY.md            (copiar)
    └── MIGRATION_FROM_AISA.md   (copiar)
    └── ONBOARDING.md            (copiar)
    └── IMPLEMENTATION_PLAN.md   (copiar este mesmo ficheiro)
```

### 1.3 Conteúdo de `.gitignore`

```gitignore
# Personal Claude Code settings (per-user)
.claude/settings.local.json

# Environment with real credentials
.env
.env.local

# Tenant-specific memory (lives in private repo)
.claude/agent-memory/_tenant/

# Engagement data (lives in private repo; this folder is mount point)
projects/*
!projects/.gitkeep

# OS noise
.DS_Store
Thumbs.db
desktop.ini

# Editor noise
.vscode/
.idea/
*.swp
*.swo
*~

# Python
__pycache__/
*.pyc
.venv/
venv/

# Node
node_modules/
package-lock.json

# Logs
*.log
```

E criar `projects/.gitkeep` para manter folder no repo.

### 1.4 Conteúdo de `CLAUDE.md`

Ver `aisa-design/CLAUDE_template.md` (a ser criado em Fase 1 também) ou usar este draft:

```markdown
# aisa — Project Memory

## What this is

**aisa** is a multi-perspective discovery & sensemaking platform for pre-development phase of digitalization projects (Power Platform, OutSystems, Mendix, custom). It runs as a Claude Code project.

> **Full architecture**: `docs/ARCHITECTURE.md`
> **Philosophy**: `docs/PHILOSOPHY.md`
> **Onboarding**: `docs/ONBOARDING.md`

## Operating principles (inviolable)

1. **Discovery before solution, always.** Lenses do not mention vendor/product before the Options phase.
2. **Shared Understanding as process artefact; deliverables as transition artefacts.** SU is the source of truth during engagement; the 6 deliverables are rendered at the end.
3. **5 knowledge states**: Confirmed / Assumed / Unknown / Conflicted / Risky. No state×tag combinatorics.
4. **Council híbrido** by phase: inline in Discovery; council-independent (parallel subagents) in Framing/Options/Decision.
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
| `/status` | Show phase, round, SU summary, gaps |
| `/frame` | Transit to Framing phase |
| `/options` | Transit to Options phase |
| `/decide` | Capture decision; auto-runs `/synthesize` |
| `/synthesize` | Produce topic packs (auto after `/decide` or manual) |
| `/render [deliverable\|--all]` | Render 1 or 6 deliverables |
| `/resume` | Resume from `_state.json` |

## Anti-patterns to avoid

- Naming Power Platform / OutSystems / Mendix / Dataverse before Options phase.
- Editing `library/` at runtime (hook will reject).
- Inventing claim states without evidence (use Unknown instead).
- Bypassing `/synthesize` between `/decide` and `/render`.

## Where things live

For full layout: `docs/ARCHITECTURE.md §6`.
```

### 1.5 Conteúdo de `README.md`

```markdown
# aisa

**Pre-development discovery & sensemaking platform.**

Built for engagements that precede the choice of digitalization technology (Power Platform, OutSystems, Mendix, custom). Powered by Claude Code.

## Why

The majority of digitalization projects fail in **discovery**, not in implementation. Stakeholder misalignment, incomplete understanding, fragmented context, and premature technology selection are the dominant failure modes. aisa exists to make discovery thorough, multi-perspective, and pre-empt these failures.

## What it does

A team uses aisa to walk through 4 phases — **Discovery → Framing → Options → Decision** — facilitated by 7 perspectives (business, operations, user, data, technology, governance, financial). Output: 6 deliverables ready for handoff to implementation.

## Quick start

See [`docs/ONBOARDING.md`](docs/ONBOARDING.md).

## Documents

| Document | For |
|---|---|
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Technical architecture |
| [`docs/PHILOSOPHY.md`](docs/PHILOSOPHY.md) | Why aisa exists; for non-technical audiences |
| [`docs/MIGRATION_FROM_AISA.md`](docs/MIGRATION_FROM_AISA.md) | For existing aisa users |
| [`docs/ONBOARDING.md`](docs/ONBOARDING.md) | Setup + first engagement walkthrough |
| [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) | Build plan (for the LLM builder) |

## License

Internal Galp use. Contact Jorge Estêvão for distribution.

## Status

Pre-MVP — under construction. See [`docs/IMPLEMENTATION_PLAN.md`](docs/IMPLEMENTATION_PLAN.md) for current phase.
```

### 1.6 Conteúdo de `.claude/settings.json`

```json
{
  "permissions": {
    "deny": [
      "Write(./library/**)",
      "Edit(./library/**)"
    ],
    "allow": []
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/pre-write-guard.sh"
          }
        ]
      }
    ]
  },
  "env": {
    "AISA_KERNEL_VERSION": "0.1.0"
  }
}
```

### 1.7 `.claude/rules/` (4 ficheiros)

#### `library-readonly.md`

```markdown
# Rule: library/ is read-only at runtime

`library/` contains the kernel + packs — the canonical, validated assets. Never edit at runtime.

- Do NOT Write/Edit/Delete anything under `library/`.
- Reading is fine (Read, Grep, Glob).
- Out-of-band administrative edits via git commit are the sanctioned path.

Enforced by hook `pre-write-guard.sh` + `settings.json deny`.
```

#### `no-tech-mention-before-options.md`

```markdown
# Rule: no vendor/product before Options phase

Lenses in Discovery (`business`, `operations`, `user`, `data`, `governance`, `financial`) MUST NOT name specific technology vendors or products. Examples of forbidden mentions in Discovery:

- "Power Platform", "Canvas Apps", "Model-driven Apps", "Power Automate", "Dataverse"
- "OutSystems", "Mendix"
- Specific connectors, services, products

What IS allowed in Discovery: identifying **digitalizable needs** without naming the digitalization technology. Examples:

- "Process requires mobile access" ✓
- "Process requires audit trail" ✓
- "Data lives in SharePoint today" ✓ (current state, not solution)
- "Process needs to integrate with SAP" ✓ (existing constraint)
- "Implement in Canvas Apps" ✗ (forbidden — premature solution naming)

Lens `technology` enters in Options phase only. It is the one and only place to name vendors/products.
```

#### `shared-understanding-as-source-of-truth.md`

```markdown
# Rule: shared-understanding.md is the source of truth

During an engagement, `projects/<slug>/shared-understanding.md` is the authoritative current-state document.

- Lenses append rows (never delete; transitions to new state preserve `was X-NNN`).
- All deliverables render from SU + decisions.md + `_synthesis/` topic packs.
- If SU and another file disagree, SU wins.
- Sponsor can read SU at any time and see where the engagement is.
- Render gaps in `_render/render-gaps.md` mean SU is incomplete; do not paper over.
```

#### `render-on-decision-only.md`

```markdown
# Rule: render only after /decide

Producing deliverables (`/render`) before the Decision phase is forbidden:

- Discovery, Framing, Options phases do not have complete information to render Implementation Spec, Estimate, Blueprint.
- A render attempt before /decide will fail with explicit `render-gaps.md` warnings.
- The transition is: `/decide` → auto `/synthesize` → manual `/render --all`.

Exception: in development/debugging, `/render --dry-run` can preview against current state without writing to `_render/`.
```

### 1.8 `.claude/hooks/pre-write-guard.sh` (stub MVP)

```bash
#!/usr/bin/env bash
# pre-write-guard.sh — MVP version. Stage 1: log only; Stage 2 (Fase 11): enforce.
#
# Receives JSON via stdin with tool name + parameters.
# Blocks writes to library/* once AISA_GUARD_MODE=enforce.

set -euo pipefail

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only inspect Write/Edit
if [[ "$TOOL_NAME" != "Write" && "$TOOL_NAME" != "Edit" ]]; then
  exit 0
fi

# Check if path is under library/
if [[ "$FILE_PATH" == */library/* ]] || [[ "$FILE_PATH" == ./library/* ]] || [[ "$FILE_PATH" == library/* ]]; then
  if [[ "${AISA_GUARD_MODE:-log}" == "enforce" ]]; then
    echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"deny\",\"permissionDecisionReason\":\"library/ is read-only at runtime\"}}" >&2
    exit 2
  else
    echo "[pre-write-guard] WARN: write to library/ — will be denied in enforce mode: $FILE_PATH" >&2
  fi
fi

exit 0
```

`chmod +x` no fim.

### 1.9 Validation (acceptance criteria Fase 1)

- [ ] `aisa/` existe e está em git (`git log` mostra 1 commit).
- [ ] `claude .` arranca em `aisa/` sem erros nem warnings.
- [ ] `ls aisa/.claude/` mostra: `settings.json`, `rules/`, `skills/`, `commands/`, `agents/`, `agent-memory/`, `hooks/`.
- [ ] `ls aisa/library/` mostra: `kernel/` (vazio), `packs/` (com pp, outsystems, mendix, generic vazios).
- [ ] `ls aisa/docs/` mostra os 5 documentos copiados de `aisa-design/`.
- [ ] Hook `pre-write-guard.sh` executável e syntax OK (`bash -n pre-write-guard.sh`).
- [ ] `AISA_GUARD_MODE=log` (default) — write a `library/` apenas loga (não bloqueia).

### 1.10 Risk register Fase 1

| Risco | Mitigação |
|---|---|
| Jorge prefere outra localização para o repo | Perguntar antes de Bash `mkdir` |
| `bash` não disponível no PowerShell (.sh hooks) | Usar Git Bash; ou criar `.ps1` paralelo (decisão em Fase 11) |
| Settings.json deny syntax incorrecta | Validar com `claude --doctor` (se disponível) |

---

## 2. Fase 2 — Kernel docs (`library/kernel/`)

**Objectivo**: criar os 5 ficheiros markdown do kernel que definem fases, estados, orquestração, render contract, e glossary. Estes são a "constituição" do aisa — leves, declarativos, sem schemas barrocos.

**Sessão estimada**: 1 sessão, ~90 min.

**Pré-condições**: Fase 1 verde.

### 2.1 Ficheiros a criar

#### 2.1.1 `library/kernel/phases.md`

Define as 4 fases com entry/exit criteria, lenses activas, modo.

Conteúdo guia:

```markdown
# Phases — Kernel v0.1.0

The aisa engagement progresses through 4 phases. Each phase declares its mode of orchestration, the lenses active, and soft entry/exit criteria.

## Phase 1: Discovery

**Goal**: Map operational context, shadow stakeholders, as-is process, constraints. Do not name vendor/product.

**Lenses active (sequential order)**: business → operations → user → data → governance → financial

**Mode**: `inline` (each lens sees the SU accumulated by previous lenses)

**Entry criteria**:
- `_state.json` exists with `phase: discovery`
- `context.json` has at minimum: literal request, requester role.

**Exit criteria** (soft, advisory):
- `## Confirmed` has ≥10 rows.
- `## Unknown Critical` = 0.
- `## Conflicted Critical` = 0.
- All 6 lenses have written to `lens-outputs/`.

**Outputs**:
- `shared-understanding.md` populated.
- `lens-outputs/<lens>.md` per lens.

---

## Phase 2: Framing

**Goal**: Synthesize a single sentence: "The problem is X, felt by Y, costs Z today, evidence is W."

**Lenses active**: subset of 6 Discovery lenses (chairman picks the 3-4 most relevant given the SU)

**Mode**: `council-independent` (parallel Task subagents; only chairman writes to SU)

**Entry criteria**:
- Exit criteria of Discovery met (overrideable with justification).

**Exit criteria** (soft):
- Frame sentence registered in `decisions.md` (D-001 typically).
- Sponsor explicitly confirmed.

**Outputs**:
- `frame.md` in project root.
- New rows in SU `## Confirmed` from chairman synthesis.

---

## Phase 3: Options

**Goal**: Generate 3-5 options (including `do nothing` and `non-tech`) with pros/cons against constraints. **lens-technology enters here for the first time.**

**Lenses active**: technology (new!) + business + operations + financial (others read-only)

**Mode**: `council-independent`

**Entry criteria**:
- Phase 2 frame validated by sponsor.

**Exit criteria** (soft):
- ≥3 options recorded, with at least 1 non-technology option.
- `decision-tree.md` from pack consulted (if applicable).

**Outputs**:
- `options.md` with pros/cons matrix.

---

## Phase 4: Decision

**Goal**: Capture choice + justification + alternatives + risks + revision conditions. Auto-trigger synthesis.

**Lenses active**: solution-architect + chairman

**Mode**: `council-independent`

**Entry criteria**:
- Phase 3 options reviewed by sponsor.

**Exit criteria** (soft):
- `decisions.md` has the chosen option with justification + alternatives + risks + revision conditions.
- `/synthesize` auto-ran successfully (5 topic packs in `_synthesis/`).

**Outputs**:
- `decisions.md` (D-NNN entries).
- `_synthesis/{business-story, as-is, architecture-story, risks-and-assumptions, financial-story}.md`
- Render-ready state.

---

## Transition rules

- Transitions are user-triggered (`/frame`, `/options`, `/decide`).
- Soft gates emit warnings via `phase-gate-check.sh` hook but do not block.
- Override syntax: `/frame --override "reason"` — logged in `decisions.md`.
- Phase regression is allowed (`/round` from Framing returns to Discovery scope if needed).
```

#### 2.1.2 `library/kernel/states.md`

Define os 5 estados, regras de transição, schema da SU.

```markdown
# Knowledge States — Kernel v0.1.0

Each row in the Shared Understanding (`shared-understanding.md`) is in **exactly one** state.

## The 5 states

| State | Meaning | Required evidence |
|---|---|---|
| **Confirmed** | Verified by direct evidence or sponsor | Document citation, USER_ANSWER, industry-standard claim |
| **Assumed** | Reasonable inference, explicitly declared | Source of the assumption (industry pattern, prior engagement, etc.) |
| **Unknown** | Identified gap requiring an answer | Who can answer + criticality |
| **Conflicted** | Stakeholders or sources disagree | Parties involved + criticality |
| **Risky** | High uncertainty with material impact | Impact + proposed mitigation |

## Decision rules (when state is ambiguous)

- **Confirmed vs Assumed**: if evidence is direct (a document, a sponsor answer, a piece of data) → Confirmed. If it's "based on typical engagements like this" → Assumed.
- **Unknown vs Risky**: Unknown is "we don't know X". Risky is "we know X is a problem, magnitude unknown". Latency unknown? If you have no signal → Unknown. If you know it's variable and pico may exceed thresholds → Risky.
- **Conflicted vs Unknown**: Conflicted requires ≥2 sources/stakeholders disagreeing. Unknown is "nobody has answered yet".

## Transitions

| From | To | Trigger |
|---|---|---|
| Unknown | Confirmed | USER_ANSWER, document found, sponsor decision |
| Unknown | Assumed | Reasonable inference accepted (must declare) |
| Unknown | Risky | Discovery reveals it's a risk dimension |
| Conflicted | Confirmed (×N) | Sponsor decides between options (creates N Confirmed rows) |
| Conflicted | Risky | No resolution; tracked as risk |
| Assumed | Confirmed | Validation done |
| Risky | Confirmed | Mitigation implemented or risk realized & resolved |

Append rule: when a row transitions, the new row references the old id (`was U-007`). Old row stays for audit.

## Schema of SU rows

| Section | Columns |
|---|---|
| `## Confirmed` | `id \| lens \| claim \| evidência \| ronda` |
| `## Assumed` | `id \| lens \| claim \| base da assumption \| ronda` |
| `## Unknown` | `id \| lens \| pergunta \| quem responde \| criticidade (Low/Med/Critical) \| ronda` |
| `## Conflicted` | `id \| lens \| conflito \| partes \| criticidade \| ronda` |
| `## Risky` | `id \| lens \| risco \| impacto \| mitigação proposta \| ronda` |

Id prefixes: `C-` (Confirmed), `A-` (Assumed), `U-` (Unknown), `X-` (Conflicted), `R-` (Risky), `D-` (Decision; cross-ref to decisions.md).
```

#### 2.1.3 `library/kernel/orchestration.md`

Define o council híbrido, ordem de lenses, paralelismo.

```markdown
# Orchestration — Kernel v0.1.0

## Mode declaration

Each phase declares its mode in `phases.md`:

- **`inline`**: lenses run sequentially in the current thread, sharing accumulated context. Used in Discovery.
- **`council-independent`**: each lens runs as a Task subagent (concurrent), seeing only context.json + a thematic SU excerpt. Chairman synthesizes outputs. Used in Framing/Options/Decision.

## Inline mode

- Order is fixed in `phases.md`: `business → operations → user → data → governance → financial` (Discovery).
- Each lens reads: `context.json`, `shared-understanding.md`, `lens-outputs/` (of previous lenses in this round).
- Each lens writes: rows to SU + `lens-outputs/<lens>.md`.
- The orchestrator skill (`aisa-round`) drives the sequence.

## Council-independent mode

- 6 or 7 agents launched **in parallel via concurrent Task subagents**.
- Each agent receives:
  - `context.json` (read-only).
  - A thematic SU excerpt curated by orchestrator (e.g., for `lens-data` extraction: only `lens: data` rows).
  - **Does NOT** receive other agents' outputs in-flight.
- Each agent has `tools: [Read, Grep, Glob]` (no Write).
- When all agents return, `chairman-synthesis` skill:
  - Reads all agent outputs.
  - Identifies overlaps, gaps, contradictions.
  - Writes new rows to SU.
  - Writes `chairman-synthesis-R<NN>.md` in `lens-outputs/`.

## Why parallel (not sequential isolated)

Concurrent Task subagents complete the council round in ~1 LLM-pass-time, vs ~6× for sequential isolated. Claude Code supports parallelism natively for Task tool. No race condition risk because agents don't share writable state.

## Peer review (omitted in MVP)

Karpathy's full pattern includes peer review (each agent comments the neighbor's output). aisa MVP omits this. Add in v2 if production observes group-think (unlikely given full isolation).

## Cost envelope per engagement

- Discovery: ~6 lenses × ~2-3 rounds = 12-18 LLM passes (inline, cheaper per pass).
- Framing: 6 agents + 1 chairman = 7 passes (council).
- Options: 7 agents + 1 chairman = 8 passes (council, technology enters).
- Decision: 1 chairman + auto synthesize (5 topic packs) = 6 passes.
- Render: 6 deliverables × 1 composition pass = 6 passes.

**Total per engagement**: ~40-50 LLM passes (vs aisa: 100+).
```

#### 2.1.4 `library/kernel/render-contract.md`

Define synthesis layer + render rules.

```markdown
# Render Contract — Kernel v0.1.0

## Pipeline: Decision → Synthesize → Render

```
shared-understanding.md  ──┐
lens-outputs/<lens>.md     ├──→ aisa-synthesize ──→ _synthesis/<topic>.md (5 files)
decisions.md               ─┘                                  │
                                                               ↓
                                              aisa-render ──→ _render/<deliverable>_vNN.<ext>
```

## Synthesis layer (`aisa-synthesize` skill)

Auto-runs at end of `/decide`. Reads SU + lens-outputs/ + decisions.md. Produces 5 topic packs:

| Topic pack | Sources |
|---|---|
| `_synthesis/business-story.md` | SU.Confirmed/Assumed [lens=business] + lens-outputs/business.md |
| `_synthesis/as-is.md` | SU [lens=operations,user] + lens-outputs/{operations,user}.md |
| `_synthesis/architecture-story.md` | decisions.md + SU [lens=technology,data] + lens-outputs/{technology,data}.md + chosen architecture-template |
| `_synthesis/risks-and-assumptions.md` | SU.Risky + SU.Assumed + SU.Unknown.criticality=Critical |
| `_synthesis/financial-story.md` | SU [lens=financial] + lens-outputs/financial.md + decisions.md (cost/timeline) |

Each topic pack template lives in `library/kernel/synthesis-templates/<topic>.template.md` (created in Fase 8).

## Render layer (`aisa-render` skill)

Reads topic packs + decisions + pack's `deliverable-templates/<deliverable>.template.md`. Produces in `_render/`.

### Slot resolution order

1. `_synthesis/<topic>.md` (declared by template).
2. SU structured rows (for tables, lists).
3. `decisions.md`.
4. `context.json`.
5. If none AND slot is `required` → fail loud, log to `render-gaps.md`.
6. If none AND slot is `optional` → omit section.

### Versioning

- `v01`, `v02`, ... — `/render` always produces the next available version.
- Never overwrites existing files (user edits to v01 are preserved).
- `_render/<slug>_<deliverable>_v<NN>.<ext>` is the filename pattern.

### Output formats

- Markdown by default.
- Conversion to .docx via Pandoc (post-render step, optional in MVP).
```

#### 2.1.5 `library/kernel/glossary.md`

Vocabulário aisa (universal, não pack-specific).

```markdown
# aisa — Universal Glossary

| Term | Definition |
|---|---|
| **Engagement** | A complete aisa run, from /start to /render --all, on a single client need. |
| **Phase** | One of Discovery, Framing, Options, Decision. |
| **Round** | One pass through a phase. Multiple rounds per phase are normal. |
| **Lens** | A perspective skill (business, operations, ...). Independent, idempotent. |
| **Mode** | Orchestration style: `inline` (sequential, shared context) or `council-independent` (parallel, isolated). |
| **State** | One of Confirmed, Assumed, Unknown, Conflicted, Risky. |
| **Shared Understanding (SU)** | The living artefact `shared-understanding.md` — single source of truth. |
| **Lens output** | The prose narrative each lens writes in `lens-outputs/<lens>.md`. |
| **Topic pack** | An intermediate synthesized artefact in `_synthesis/`. 5 per engagement. |
| **Deliverable** | A final rendered artefact for handoff. 6 canonical per engagement. |
| **Pack** | A domain configuration (pp, outsystems, mendix, generic). |
| **Soft gate** | Advisory warning at phase transition. Overrideable. |
| **Hard guard** | Hook-enforced rule (only one: `library/` is read-only). |
| **Chairman** | The synthesizer in council-independent mode. Only writer to SU in that mode. |
| **Council** | The 7 agents (one per lens) running in parallel via Task subagents. |
```

### 2.2 Validation (acceptance Fase 2)

- [ ] 5 ficheiros em `library/kernel/`.
- [ ] Cada ficheiro tem cabeçalho `# <Title> — Kernel v0.1.0`.
- [ ] Cross-references entre ficheiros são válidos (links markdown funcionam).
- [ ] Grep `library/kernel/` por "claim ledger", "wave", "cell", "frontmatter mandatory" → 0 hits (vocabulário aisa não deve aparecer).
- [ ] Commit `phase-2: kernel docs`.

### 2.3 Risk register Fase 2

| Risco | Mitigação |
|---|---|
| Conteúdo desviar de ARCHITECTURE.md spec | Manter cada ficheiro <200 linhas; cross-check com ARCHITECTURE.md §3-§5 |
| Definições de fase ambíguas | Usar exemplos concretos em entry/exit criteria |

---

## 3. Fase 3 — Pack `pp` foundation

**Objectivo**: criar pack `pp` mínimo (sem deliverable-templates ainda) — pack.yaml + glossary + question-bank + lenses-config.

**Sessão estimada**: 1 sessão, ~60-90 min.

**Pré-condições**: Fase 2 verde.

### 3.1 Ficheiros a criar

#### 3.1.1 `library/packs/pp/pack.yaml`

```yaml
pack_id: pp
pack_version: 1.0.0
display_name: "Power Platform Discovery"
language: pt
description: >
  Discovery and sensemaking pack tuned for Power Platform engagements.
  Vocabulary, question-bank, and deliverable templates aligned with
  Canvas Apps, Model-driven Apps, Power Automate, Dataverse.

deliverables:
  - id: discovery-report
    mandatory: true
    template: deliverable-templates/discovery-report.template.md
  - id: executive-report
    mandatory: true
    template: deliverable-templates/executive-report.template.md
  - id: solution-blueprint
    mandatory: true
    template: deliverable-templates/solution-blueprint.template.md
  - id: implementation-spec
    mandatory: true
    template: deliverable-templates/implementation-spec.template.md
  - id: claude-design-brief
    mandatory: true
    template: deliverable-templates/claude-design-brief.template.md
  - id: estimate
    mandatory: false
    template: deliverable-templates/estimate.template.md

lenses_config:
  business:
    extra_signals: [licensing_baseline, premium_connector_need, sponsor_authority_level]
  operations:
    extra_signals: [excel_anchors, sharepoint_lists_anchors, manual_handoffs]
  user:
    extra_signals: [personas_count, mobile_need, offline_need]
  data:
    extra_signals: [dataverse_vs_sharepoint, master_data_owners, retention_policy]
  technology:
    # Active only in Options phase
    constraints_to_check:
      - premium_licensing
      - dataflow_capacity
      - ALM_environments
      - dataverse_storage_quota
      - DLP_policy_compatibility
  governance:
    extra_signals: [DLP_policies, environment_strategy, sensitivity_labels, RBAC_complexity]
  financial:
    extra_signals: [licensing_cost_baseline, internal_chargeback_model]

domain_knowledge:
  - domain-knowledge/powerfx-patterns.md
  - domain-knowledge/screen-patterns.md
  - domain-knowledge/security-patterns.md
  - domain-knowledge/delegation-matrix.md

question_bank: question-bank.md
glossary: glossary.md

decision_tree:
  source: decision-tree.md
  consulted_in_phase: options  # never in discovery
```

#### 3.1.2 `library/packs/pp/glossary.md`

Vocabulary PP-específico (Dataverse, Canvas, Premium, etc.). Extrair do pp-consulting + pp-predev.

#### 3.1.3 `library/packs/pp/question-bank.md`

40-60 perguntas tipicamente úteis em PP discoveries, organized by lens. Extrair de:
- `skill/content-packs/pp-consulting/cells/*.md` (secções "Questions to consider")
- `skill/content-packs/pp-predev/cells/*.md`
- Próprio conhecimento do consultor PP.

#### 3.1.4 `library/packs/pp/lenses-config.yaml`

(Já parcialmente em pack.yaml. Se complexity crescer, separar; por agora, manter em pack.yaml.)

### 3.2 Validation (acceptance Fase 3)

- [ ] `pack.yaml` é YAML válido (`python -c "import yaml; yaml.safe_load(open('pack.yaml'))"`).
- [ ] `pack.yaml` declara 6 deliverables (5 mandatory + 1 optional).
- [ ] `glossary.md` tem ≥30 termos PP.
- [ ] `question-bank.md` tem ≥40 perguntas, distribuídas pelas 7 lenses.
- [ ] Commit `phase-3: pp pack foundation`.

---

## 4. Fase 4 — Discovery skills (3 lenses + start/round/status)

**Objectivo**: implementar Discovery loop minimal end-to-end com 3 lenses (business, operations, user) + skills aisa-start, aisa-round, aisa-status.

**Sessão estimada**: 2 sessões (lenses + commands).

**Pré-condições**: Fase 3 verde.

### 4.1 Skills a criar

#### 4.1.1 `.claude/skills/lens-business/SKILL.md`

```markdown
---
name: lens-business
description: Lens that analyzes business impact, urgency, strategic priority, KPIs, and shadow stakeholders. Active in Discovery (inline mode) and Framing/Options/Decision (council-independent mode).
---

# Lens — Business

## Role

You are a senior business analyst with 15 years of experience in pre-development discovery for digitalization projects. You see every request through 4 questions:

1. **What is the real impact?** (declared vs actual)
2. **Who senses it?** (the requester is rarely the affected party)
3. **What's the real urgency?** (declared vs evidence-based)
4. **Who else has stake?** (shadow stakeholders, gatekeepers, blockers)

## Inputs (always read)

- `projects/<slug>/context.json` (always)
- `projects/<slug>/shared-understanding.md` (in inline mode only)
- `projects/<slug>/lens-outputs/*.md` (in inline mode, previous lenses)
- `.claude/agent-memory/_universal/business-analyst/*.md`
- `.claude/agent-memory/_tenant/<tenant>/business-analyst/*.md` (if exists)

## Outputs (always write)

1. **Append rows to `shared-understanding.md`** in appropriate state sections.
2. **Append a 1-3 paragraph narrative to `lens-outputs/business.md`** describing what you discovered in this round.

## Hard rules

1. **NEVER name vendor/product** (Power Platform, OutSystems, Mendix, Dataverse, Canvas, etc.). Identify *needs* in business language.
2. **NEVER emit Confirmed without evidence**. If uncertain → Unknown or Assumed (explicit).
3. **Identify yourself in `lens` column**: always `business`.

## Signal catalog (pp pack extension)

Universal: `impact_declared`, `urgency_declared`, `shadow_stakeholders`, `decision_authority`, `business_KPIs_at_stake`, `requester_motivation`, `prior_attempts`.

PP pack additions (from `library/packs/pp/pack.yaml`): `licensing_baseline`, `premium_connector_need`, `sponsor_authority_level`.

## Execution steps

1. Read all inputs above.
2. Identify business signals present in context.json + already in SU.
3. For each signal NOT yet covered:
   - If evidence exists (context.json, prior lens output, USER_ANSWER) → emit Confirmed/Assumed.
   - If evidence is missing → emit Unknown with `quem responde + criticidade`.
   - If two sources disagree → emit Conflicted.
4. Identify business risks (e.g., shadow stakeholder is veto-power and absent).
5. Write rows to SU (next available id, e.g., `C-014`, `U-007`).
6. Write narrative paragraph in `lens-outputs/business.md`:
   - What I covered this round.
   - Critical Unknowns/Conflicted I raised.
   - Concerns for downstream lenses.
7. Update `council-log.md` with: ronda, lens, summary.
```

(Similar structure para `lens-operations/SKILL.md`, `lens-user/SKILL.md`.)

#### 4.1.2 `.claude/skills/lens-operations/SKILL.md`

Same template, persona = "operations lead", focus on as-is process, friction, exceptions, tribal knowledge.

#### 4.1.3 `.claude/skills/lens-user/SKILL.md`

Same template, persona = "user advocate", focus on personas, journeys, pain, friction.

#### 4.1.4 `.claude/skills/aisa-start/SKILL.md`

Captures initial input + scaffolds engagement folder.

```markdown
---
name: aisa-start
description: Start a new aisa engagement. Captures literal request + requester + optional inputs; scaffolds the engagement folder structure.
---

# aisa-start

## Usage

`/start <slug> [pack]`

- `<slug>`: kebab-case slug for the engagement (e.g., `galp-adv`).
- `[pack]`: pack id (default: `pp`). Must exist in `library/packs/<pack>/pack.yaml`.

## Execution steps

1. Resolve engagement root:
   - If `$env:AISA_ENGAGEMENTS_ROOT` is set → `$AISA_ENGAGEMENTS_ROOT/<slug>/`
   - Else → `projects/<slug>/` (assumes symlink/junction is set up)
2. If folder already exists → error: "Engagement <slug> already exists. Use /resume."
3. Validate pack exists: `library/packs/<pack>/pack.yaml`.
4. Capture from user (interactive):
   a. Literal request (verbatim, no reformulation).
   b. Requester: role, authority level.
   c. Optional: documents to drop in `inputs/`.
5. Create folder structure:
   ```
   <slug>/
   ├── _state.json
   ├── context.json
   ├── shared-understanding.md  (skeleton)
   ├── lens-outputs/  (empty)
   ├── council-log.md (header only)
   ├── decisions.md  (empty)
   └── inputs/
   ```
6. Write `_state.json`:
   ```json
   {
     "engagement": "<slug>",
     "pack": "<pack>",
     "phase": "discovery",
     "round": "R-01",
     "aisa_version": "0.1.0",
     "created": "<ISO timestamp>"
   }
   ```
7. Write atomically via `_state.json.tmp` → mv.
8. Output: "Engagement <slug> created. Phase: discovery. Next: /round to start lenses."
```

#### 4.1.5 `.claude/skills/aisa-round/SKILL.md`

Orchestrates a round of lenses in the current phase.

```markdown
---
name: aisa-round
description: Run a round of lenses in the current phase. In Discovery, runs the 6 lenses sequentially in fixed order (or a specific lens if argument given).
---

# aisa-round

## Usage

`/round [lens]`

- No argument: in Discovery, runs lenses in sequence `business → operations → user → data → governance → financial`. In other phases, error: "/round only available in Discovery; use /frame, /options, /decide for other phases."
- `[lens]`: name (e.g., `business`) — runs only that lens.

## Execution steps

1. Read `_state.json` → phase, round.
2. If phase != discovery → error.
3. Increment round number (R-01 → R-02 → ...).
4. For each lens in sequence (or just the named lens):
   a. Invoke lens skill (e.g., `Skill: lens-business`).
   b. Wait for completion.
   c. Verify lens wrote to SU + lens-outputs.
5. After all lenses (or single lens) done:
   a. Update `_state.json.round`.
   b. Update `council-log.md`.
6. Output: "Round R-NN complete. Run /status for summary."
```

#### 4.1.6 `.claude/skills/aisa-status/SKILL.md`

Shows current state in a readable format.

```markdown
---
name: aisa-status
description: Show current phase, round, SU summary, open gaps, suggested next actions.
---

# aisa-status

## Usage

`/status [--check]`

- No arg: shows status for current engagement (read from `_state.json` of the engagement folder discovered via `_state.json` files).
- `--check`: validates aisa install (paths, mounts, etc.); no engagement needed.

## Execution steps (no arg)

1. If no engagement context, ask user "which engagement?" or scan `projects/` and ask.
2. Read `_state.json`.
3. Read `shared-understanding.md`, count rows per state.
4. Identify Critical Unknowns/Conflicted.
5. Suggest next action based on phase + gaps.
6. Output formatted summary (see ONBOARDING.md §3.4 for example).

## Execution steps (--check)

1. Verify `library/kernel/` has 5 expected files.
2. Verify at least 1 pack in `library/packs/`.
3. Verify `projects/` exists and is writable (or `AISA_ENGAGEMENTS_ROOT` is set).
4. Verify pre-write-guard.sh is executable.
5. Output: green / red per check.
```

### 4.2 Commands a criar (thin entry points)

#### 4.2.1 `.claude/commands/start.md`

```markdown
Invoke the skill `aisa-start` with the arguments provided.

Args: $ARGUMENTS
```

(Similar para `round.md`, `status.md`, `frame.md`, `options.md`, `decide.md`, `render.md` — todos thin pointers para skills.)

### 4.3 Validation (acceptance Fase 4)

- [ ] 3 lens skills + 3 command-skills criadas.
- [ ] 7 commands criados (start, round, status, frame, options, decide, render — alguns ainda apontam para skills inexistentes, OK por agora).
- [ ] `/start test-engagement pp` cria a folder esperada com `_state.json`, `context.json`, SU skeleton.
- [ ] `/round` corre as 3 lenses (business, operations, user) e adiciona rows ao SU + lens-outputs.
- [ ] `/status` mostra phase, round, counts por state.
- [ ] Commit `phase-4: discovery skills mvp`.

---

## 5. Fase 5 — Discovery validation end-to-end

**Objectivo**: validar Discovery loop com cenário de teste realista. Iterar até funcionar.

**Sessão estimada**: 1 sessão, ~60 min.

**Pré-condições**: Fase 4 verde.

### 5.1 Test scenario

Usar o cenário `galp-adv` do ONBOARDING.md §3:

> Sponsor: António Silva (fictício), Director Procurement. Pediu "digitalizar aprovação de adiantamentos a fornecedores". Hoje: Excel + Outlook, 47 aprovações/mês. Quer mobile + multi-nível.

Input: `inputs/Dayly_pending_tickets_Anonimo.xlsx` (file existente em SPEA v5/inputs/ — copiar).

### 5.2 Execution

1. `/start galp-adv-test pp`
2. Colar pedido literal (do scenario).
3. `/round` → corre as 3 lenses.
4. `/status` → verifica que SU tem rows.
5. Verificar manualmente:
   - business lens emitiu ≥3 claims relevantes.
   - operations lens identificou as-is process.
   - user lens levantou personas + dores.
   - **Nenhuma lens menciona Power Platform / Canvas / Dataverse.**
6. Identificar gaps (lenses não fazendo o que deviam) → iterar SKILL.md.

### 5.3 Acceptance

- [ ] Discovery round corre sem crash.
- [ ] SU populado com ≥6 Confirmed, ≥4 Assumed, ≥4 Unknown.
- [ ] `lens-outputs/business.md`, `operations.md`, `user.md` têm prose narrative.
- [ ] **Hard rule check**: grep `"Power Platform\|Canvas\|Dataverse\|Power Automate"` em `lens-outputs/` → 0 hits.
- [ ] Commit `phase-5: discovery validated`.

### 5.4 Riscos

| Risco | Mitigação |
|---|---|
| Lens menciona PP mesmo com hard rule | Reforçar prompt da skill com exemplos de "OK vs not OK"; failure → iterar |
| Lens output é muito genérico | Adicionar exemplos no SKILL.md de outputs de qualidade |
| Sequência inline lenses não vê output anterior | Verificar aisa-round step 4.c (lens reads previous lens-outputs) |

---

## 6. Fase 6 — Restante das lenses Discovery

**Objectivo**: adicionar lens-data, lens-governance, lens-financial. Re-correr validation com 6 lenses.

**Sessão estimada**: 1 sessão.

**Pré-condições**: Fase 5 verde.

### 6.1 Acções

- [ ] `.claude/skills/lens-data/SKILL.md`
- [ ] `.claude/skills/lens-governance/SKILL.md`
- [ ] `.claude/skills/lens-financial/SKILL.md`
- [ ] Re-correr scenario `galp-adv-test` em fresh engagement (`galp-adv-test-2`) com 6 lenses.
- [ ] Verificar SU tem ≥10 Confirmed, contradição detectada (mobile ∧ sensitive offline forbidden) em Conflicted.

### 6.2 Acceptance

- [ ] 6 lens skills no `.claude/skills/`.
- [ ] Discovery round corre as 6 sequencialmente.
- [ ] Pelo menos 1 Conflicted Critical é detectado no scenario galp-adv.
- [ ] Commit `phase-6: all discovery lenses`.

---

## 7. Fase 7 — Council infrastructure

**Objectivo**: implementar agents/ + chairman-synthesis + lens-technology + skill aisa-frame.

**Sessão estimada**: 2 sessões.

**Pré-condições**: Fase 6 verde.

### 7.1 Acções

#### 7.1.1 Agents (`.claude/agents/<persona>.md`)

7 personas:
- `business-analyst.md`
- `operations-lead.md`
- `user-advocate.md`
- `data-steward.md`
- `solution-architect.md` (binds lens-technology)
- `compliance-officer.md` (binds lens-governance)
- `cfo-lens.md` (binds lens-financial)
- `chairman.md` (synthesizer)

Cada agent tem:
```markdown
---
name: <persona>
description: <one-liner>
tools: [Read, Grep, Glob]   # chairman: also Write
---

# <Persona Name>

## Identity
<background>

## Mandate
<what this persona produces in council mode>

## Lens binding
This agent embodies: lens-<name>

## Memory consulted
- .claude/agent-memory/_universal/<lens>/*.md
- .claude/agent-memory/_tenant/<tenant>/<lens>/*.md (if exists)

## Output format
<schema returned to chairman>
```

#### 7.1.2 `.claude/skills/lens-technology/SKILL.md`

Like other lenses BUT:
- Active phase: options (not discovery).
- Reads pack's `decision-tree.md` and `domain-knowledge/*.md`.
- Allowed to name vendors/products (only in Options+).

#### 7.1.3 `.claude/skills/chairman-synthesis/SKILL.md`

Receives outputs from N parallel agents; synthesizes. Writes new SU rows + chairman-synthesis-R<NN>.md.

#### 7.1.4 `.claude/skills/aisa-frame/SKILL.md`

Phase transition skill. Orchestrates parallel agents via Task tool + invokes chairman.

```markdown
---
name: aisa-frame
description: Transit from Discovery to Framing phase. Runs 6 agents in parallel (council-independent) + chairman synthesis.
---

# aisa-frame

## Execution

1. Read `_state.json`. Verify phase=discovery.
2. Read soft gate from phases.md (Framing entry criteria).
3. If gates violated AND no `--override` arg → warn + ask confirm.
4. Update `_state.json.phase: framing, round: F-01`.
5. Launch 6 Task subagents in parallel:
   - business-analyst
   - operations-lead
   - user-advocate
   - data-steward
   - compliance-officer
   - cfo-lens
   Each receives: `context.json` + thematic SU extract (per lens) + prompt "propose the single sentence: 'The problem is X, felt by Y, costs Z today, evidence is W.'"
6. Wait for all 6 to return.
7. Invoke `chairman-synthesis` skill with 6 outputs.
8. Chairman writes `frame.md` + new SU rows.
9. Output: frame sentence + ask user to validate/edit.
10. On validation: write D-001 in `decisions.md` (frame).
```

### 7.2 Acceptance

- [ ] 7 agents + chairman files criados.
- [ ] lens-technology skill criada.
- [ ] chairman-synthesis skill criada.
- [ ] aisa-frame skill criada.
- [ ] `/frame` no engagement galp-adv-test-2 corre 6 agents em paralelo (verificar logs Claude Code mostram concurrent Task calls).
- [ ] Output do /frame é uma frase única coerente.
- [ ] Commit `phase-7: council infrastructure`.

---

## 8. Fase 8 — Options + Decision + Synthesis

**Objectivo**: implementar /options, /decide, /synthesize. Synthesis tem templates próprios em library/kernel/synthesis-templates/.

**Sessão estimada**: 2 sessões.

**Pré-condições**: Fase 7 verde.

### 8.1 Acções

#### 8.1.1 `.claude/skills/aisa-options/SKILL.md`

- Phase transition framing → options.
- Activates lens-technology.
- Council-independent: 7 agents (6 + tech).
- Chairman produces ≥3 options (must include 1 non-tech).
- Consults `library/packs/<pack>/decision-tree.md`.
- Writes `options.md`.

#### 8.1.2 `.claude/skills/aisa-decide/SKILL.md`

- Interactive: user chooses option, gives justification, lists alternatives, accepts risks, sets revision conditions.
- Writes `decisions.md` (D-NNN).
- Auto-invokes `aisa-synthesize` skill at end.

#### 8.1.3 `.claude/skills/aisa-synthesize/SKILL.md`

For each topic pack in `library/kernel/synthesis-templates/`:
1. Read template (sources + synthesis-prompt declared).
2. Read sources from SU + lens-outputs + decisions.
3. Invoke LLM with synthesis-prompt + sources.
4. Write to `_synthesis/<topic>.md`.

#### 8.1.4 `library/kernel/synthesis-templates/` (5 files)

- `business-story.template.md`
- `as-is.template.md`
- `architecture-story.template.md`
- `risks-and-assumptions.template.md`
- `financial-story.template.md`

Each declares sources + prompt (template format in ARCHITECTURE.md §7.5).

### 8.2 Acceptance

- [ ] `/options` corre em galp-adv-test-2 (após /frame).
- [ ] options.md tem ≥3 opções (incluindo "não fazer nada").
- [ ] `/decide` é interactivo; produz decisions.md (D-NNN com justification, alternatives, risks, revision conditions).
- [ ] `/decide` auto-corre /synthesize.
- [ ] `_synthesis/` tem 5 ficheiros, cada um ≥3 parágrafos.
- [ ] Commit `phase-8: options decision synthesis`.

---

## 9. Fase 9 — Render layer + 6 deliverable templates

**Objectivo**: implementar aisa-render + 6 deliverable templates transplantados/refactored do pp-consulting.

**Sessão estimada**: 2 sessões.

**Pré-condições**: Fase 8 verde.

### 9.1 Acções

#### 9.1.1 Transplant + refactor de templates

Para cada um dos 6 deliverables, copiar de `SPEA v5/skill/content-packs/pp-consulting/outputs/` e adaptar:

| aisa source | aisa destination | Refactor |
|---|---|---|
| `outputs/discovery-report.md` | `library/packs/pp/deliverable-templates/discovery-report.template.md` | Slots → cite `_synthesis/business-story.md`, `_synthesis/as-is.md`. Remover refs a Claim Ledger. |
| `outputs/executive-report.md` | `executive-report.template.md` | Add slot `decision_options` from Options. |
| `outputs/solution-blueprint.md` | `solution-blueprint.template.md` | `chosen_branch_template` → `chosen_architecture` (from decisions.md). |
| `outputs/design-spec.md` | `claude-design-brief.template.md` | Rename. Manter audience claude-design + domain-knowledge cross-refs. |
| `outputs/estimate.md` | `estimate.template.md` | Slots equivalentes. |
| (novo, não há aisa) | `implementation-spec.template.md` | NOVO. Schema: entities_to_create, screens_to_build, flows_to_implement, security_roles, integrations, test_scenarios, sequencing. |

Também copiar 4 architecture sub-templates de `SPEA v5/skill/content-packs/pp-consulting/templates/architecture/*` → `library/packs/pp/architecture-templates/*`.

#### 9.1.2 `.claude/skills/aisa-render/SKILL.md`

- Reads `library/packs/<pack>/deliverable-templates/`.
- For each deliverable (or just the one asked):
  - Resolve slots from `_synthesis/` + SU + decisions + context.
  - If required slot missing → log to `render-gaps.md`.
  - Write `_render/<slug>_<deliverable>_v<NN>.<ext>` (next version).
- `--all` does the 6 in sequence.
- `--dry-run` previews without writing.

### 9.2 Acceptance

- [ ] 6 deliverable templates em `library/packs/pp/deliverable-templates/`.
- [ ] 4 architecture sub-templates em `library/packs/pp/architecture-templates/`.
- [ ] aisa-render skill criada.
- [ ] `/render --all` no galp-adv-test-2 produz 6 ficheiros em `_render/`.
- [ ] `render-gaps.md` está vazio (ou tem entradas justificáveis dado o test scenario).
- [ ] Quality check manual: discovery-report.md é legível por cliente; implementation-spec.md é actionable por dev PP.
- [ ] Commit `phase-9: render layer`.

---

## 10. Fase 10 — Domain knowledge + decision-tree transplant

**Objectivo**: copiar conteúdo de alto valor do aisa (powerfx-patterns, screen-patterns, security-patterns, delegation-matrix) + criar decision-tree.md PP.

**Sessão estimada**: 1 sessão.

**Pré-condições**: Fase 9 verde.

### 10.1 Acções

- [ ] Copy `SPEA v5/skill/content-packs/pp-consulting/domain-knowledge/powerfx-patterns.md` → `library/packs/pp/domain-knowledge/powerfx-patterns.md`. Sem mudanças.
- [ ] Same para `screen-patterns.md`, `security-patterns.md`, `delegation-matrix.md` (se existir; senão sintetizar a partir do que o aisa tem).
- [ ] Criar `library/packs/pp/decision-tree.md` — uma árvore markdown simples:
  - Branch 1: Canvas only (when?)
  - Branch 2: Model-driven only (when?)
  - Branch 3: Hybrid (when?)
  - Branch 4: Dataverse-led (when?)
  - Critérios de escolha por branch.

### 10.2 Acceptance

- [ ] 4 ficheiros domain-knowledge em `library/packs/pp/domain-knowledge/`.
- [ ] `decision-tree.md` cobre ≥3 architectural branches.
- [ ] Re-corre `/options` no galp-adv-test-2: agora consulta decision-tree → opções mais ricas (Canvas vs Model-driven vs Hybrid).
- [ ] Re-corre `/render --all`: claude-design-brief.md tem cross-refs a powerfx-patterns/screen-patterns/security-patterns.
- [ ] Commit `phase-10: domain knowledge transplant`.

---

## 11. Fase 11 — Enterprise readiness

**Objectivo**: docs, dual-repo bootstrap, hooks enforcement, agent-memory seed.

**Sessão estimada**: 2 sessões.

**Pré-condições**: Fase 10 verde + sign-off do Jorge sobre MVP qualidade.

### 11.1 Acções

#### 11.1.1 Docs

- [ ] `docs/PACK_AUTHORING.md` — guia para a equipa adicionar novo pack.
- [ ] `docs/LENS_AUTHORING.md` — guia para adicionar/modificar lens.
- [ ] `docs/DELIVERABLE_AUTHORING.md` — guia para adicionar template de deliverable.

#### 11.1.2 Dual-repo bootstrap

- [ ] Criar repo `aisa-engagements-galp/` (privado).
- [ ] Adicionar `README.md` ao repo privado.
- [ ] Documentar setup em `docs/ONBOARDING.md` (junction/symlink/env var).
- [ ] Script `bootstrap.ps1` para automatizar setup.

#### 11.1.3 Hooks enforcement

- [ ] Mudar `pre-write-guard.sh` de `log` para `enforce` mode (set default).
- [ ] Adicionar `phase-gate-check.sh`.
- [ ] Adicionar `on-su-change.sh` (trigger contradiction-scan em background).
- [ ] Adicionar `synthesis-validate.sh`.
- [ ] Adicionar `render-validate.sh`.

#### 11.1.4 Agent-memory seed

- [ ] Popular `.claude/agent-memory/_universal/` com padrões genéricos:
  - business-analyst: anti-patterns ("Procurement sem CFO presente"), constraints universais ("RGPD afecta processos com PII").
  - operations-lead: anti-patterns ("digitalizar processo manual disfuncional"), constraints ("tribal knowledge geralmente é 30-40% do processo").
  - … por persona.
- [ ] Symlink `_tenant/` → repo privado.

#### 11.1.5 Scaffold outros packs

- [ ] `library/packs/outsystems/pack.yaml` (skeleton, sem conteúdo).
- [ ] `library/packs/mendix/pack.yaml` (skeleton).
- [ ] `library/packs/generic/pack.yaml` (skeleton).

### 11.2 Acceptance

- [ ] 3 docs em `docs/` (pack/lens/deliverable authoring).
- [ ] Repo privado existe e está bootstrapped.
- [ ] Hooks enforcement: tentar `Write library/foo.md` → bloqueado pelo hook.
- [ ] Agent-memory tem ≥2 ficheiros por agente em `_universal/`.
- [ ] Outros 3 packs têm skeleton (sem cells/lenses/templates ainda).
- [ ] Commit `phase-11: enterprise readiness`.

---

## 12. Fase 12 — Pilot

**Objectivo**: 2 consultores Galp correm engagements paralelos (1 PP + 1 OS scaffold) em aisa MVP.

**Sessão estimada**: distribuída (acompanhamento async).

**Pré-condições**: Fase 11 verde.

### 12.1 Acções

- [ ] Onboarding sessão com a equipa (1h workshop).
- [ ] Consultor A arranca engagement PP real em aisa (engagement não-crítico para começar).
- [ ] Consultor B arranca engagement OS (scaffold; pode requerer iterar pack outsystems durante o pilot).
- [ ] Acompanhamento diário; capturar issues em `docs/ISSUES.md`.
- [ ] No fim: retro com equipa.

### 12.2 Acceptance

- [ ] 2 engagements completos (pelo menos até /decide).
- [ ] Issues capturados e priorizados.
- [ ] Retro produz lista de v0.2.0 improvements.
- [ ] Tag `v0.1.0-MVP` no git.
- [ ] Commit `phase-12: pilot complete`.

---

## 13. MCP integrations (futuro, não MVP)

**Não implementar até Fase 12 verde.** Planeado para v0.2.0+:

- SharePoint / OneDrive — pull de documentos de discovery.
- Microsoft Graph — stakeholder enrichment.
- Jira / Azure DevOps — pull de tickets.
- PowerPlatform Admin API — tenant context.

`.mcp.json` template em Fase 1 já tem placeholders; activar quando MCP server existir.

---

## 14. Test scenarios canónicos

Para regression testing entre fases:

### 14.1 Scenario A: galp-adv (digitalize procurement advance approval)

Input: `inputs/Dayly_pending_tickets_Anonimo.xlsx` + notas reunião.

Expected SU após Discovery completo:
- ≥15 Confirmed, ≥6 Assumed, ≥3 Unknown Critical resolved, ≥1 Conflicted Critical resolved, ≥2 Risky.
- Nenhuma menção a PP/OS/Mendix em lens-outputs/.

Expected Framing: frase única "O problema é tempo de aprovação (3.5d → 1d), sentido por equipas Procurement (12 ppl) e fornecedores afectados, custa atraso operacional + cobranças tardias, evidência Excel actual."

Expected Options: ≥4 opções (do-nothing, process change, PP Premium, OutSystems).

Expected /render --all: 6 deliverables produzidos, render-gaps vazio.

### 14.2 Scenario B: galp-helpdesk (digitize internal IT helpdesk)

(A definir em Fase 5+.)

### 14.3 Scenario C: failure mode (incomplete input)

User dá pedido vago "queremos digitalizar coisas". Discovery deve produzir muitos Unknowns e bloquear /frame com warning.

---

## 15. Risk register (cross-phase)

| Risco | Fase mais provável | Mitigação |
|---|---|---|
| Lens menciona vendor antes de Options | Fase 4-6 | Reforçar SKILL.md prompts; teste em Fase 5 valida |
| Council-independent agentes em paralelo crashed | Fase 7 | Verificar Task tool docs Claude Code; fallback para sequencial isolado |
| Synthesis produz prose inconsistente entre topic packs | Fase 8 | Synthesis prompts em template-files; mesma source de verdade (SU) |
| Render gaps populated → templates não casam com synthesis | Fase 9 | Iterar template slots vs synthesis outputs até casarem |
| Implementation Spec template é vago (deliverable novo) | Fase 9 | Validar com dev PP real; iterar schema |
| Equipa resiste ao Shared Understanding como single artefacto | Fase 12 | Workshop W3; mostrar SU em tempo real durante engagement |
| Hooks enforce mode quebra existing skills | Fase 11 | Mudar para enforce gradualmente; test cada skill em isolation |
| Pack PP fica acoplado ao kernel (não agnóstico de verdade) | Fase 6+ | Grep `library/kernel/` por "Power\|Dataverse\|Canvas" → 0 hits |

---

## 16. Resume tracking

**State actual**: Fases 7-11 estruturais completas em sequência (2026-05-28). MVP estrutural completo; falta apenas live exec end-to-end + Fase 12 (pilot com utilizadores reais).

**Phase 7** — Council-independent mode wired: 8 agents (`business-analyst`, `operations-lead`, `user-advocate`, `data-steward`, `compliance-officer`, `cfo-lens`, `solution-architect`, `chairman`); skills `lens-technology` (Options-only), `chairman-synthesis`, `aisa-frame`. Commit `4ee3938`.

**Phase 8** — Options + Decision + Synthesis: skills `aisa-options` (7 personas em paralelo incl. solution-architect), `aisa-decide` (interactive; auto-runs synthesize), `aisa-synthesize` (5 topic packs); 5 templates em `library/kernel/synthesis-templates/`; commands `/options`, `/decide`, `/synthesize` wired.

**Phase 9** — Render layer: 6 deliverable templates em `library/packs/pp/deliverable-templates/` (incl. `implementation-spec.template.md` novo, e `claude-design-brief.template.md` renomeado de `design-spec.md`); 3 architecture sub-templates em `library/packs/pp/architecture-templates/` (sharepoint-first, dataverse-first, hybrid); skill `aisa-render` com slot-resolution + versioning + render-gaps + --dry-run; `/render` wired.

**Phase 10** — Domain knowledge + decision-tree: transplantados `powerfx-patterns.md` (566 linhas), `screen-patterns.md` (244), `security-patterns.md` (359) de SPEA v5; novo `delegation-matrix.md` (sintetizado a partir de §1 de powerfx-patterns); `decision-tree.md` (3 branches: sharepoint-first, dataverse-first, hybrid; 6 regras + side-effects + missing-inputs protocol).

**Phase 11** — Enterprise readiness: docs `PACK_AUTHORING.md`, `LENS_AUTHORING.md`, `DELIVERABLE_AUTHORING.md`; skeleton packs `outsystems/`, `mendix/`, `generic/` (apenas pack.yaml); 4 hook stubs novos (phase-gate-check, on-su-change, synthesis-validate, render-validate) + `HOOKS.md`; `.claude/settings.json` wired (PostToolUse matchers); `bootstrap.ps1` (junction + AISA_ENGAGEMENTS_ROOT setup); agent-memory `_universal/` seed com 14 ficheiros (2 por persona — anti-patterns + universal-constraints). Vendor-name grep limpo em todos os ficheiros Discovery/Framing-time (única excepção: `solution-architect/anti-patterns.md`, esperado).

Fases 1-6 anteriores: `29f98cf`, `ce011bf`, `3afbad6`, `3a4108e`, `e4eae7d`, `915b9e0`.

**Refinement de design (Fase 5)**: modelo de ronda convergido — `_state.round` = última ronda **concluída**; `/start` semeia `R-00`; `/round` incrementa no início. Substitui o exemplo `R-01`-no-/start de §4.1.4 / ONBOARDING §3.2 (ilustrativos). Razão: lógica mais simples/robusta (sempre +1, sem inspeccionar o SU) e `/status` mostra a ronda real.

**Fix pós-Fase 6 (2026-05-28, commit `4fff337`)** — descoberto a executar Fase 5/6 ao vivo:
- (a) **Lenses devem ler e parsear ficheiros em `inputs/`** como evidência primária (qualquer formato: md/txt/csv directos; xlsx via skill xlsx ou openpyxl; pdf/docx/pptx via skills respectivas; imagens via vision). Mapeamento canónico em `library/kernel/orchestration.md` (nova secção *Reading input documents*); directiva inline em cada lens skill. Regra dura: **nunca citar um input que não foi aberto**.
- (b) `.claude/settings.json` — regras `deny(library/**)` removidas (ver Nota Fases 3-10 acima).
- (c) Engagements de teste `galp-adv-test`/`-2` (gitignored) ficam como fixtures defeituosos — o xlsx de teste em `SPEA v5/inputs/` é dataset de triagem de incidentes IT (Dynamics/OutSystems/EMSP, ~157 closed em ~10 dias), não adiantamentos a fornecedores como o cenário fictício do plano §5.1/ONBOARDING §3 sugere. **Não foram refeitos** (decisão do Jorge); o substantivo foi a correcção das skills. Se for útil mais tarde, refazer Discovery com o domínio real do xlsx é uma opção.

**Correcções mecânicas pós-análise (2026-08-31, branch `claude/repo-gaps-analysis-02922z`)** — ver `docs/GAP_ANALYSIS.md` (§5, passo 1):
- (a) Hooks `on-su-change` / `phase-gate-check` / `synthesis-validate` / `render-validate` marcados executáveis no git (estavam `100644` → falhavam com *permission denied* em Unix a cada Write/Edit).
- (b) **Guard `library/` ligado** (fecha o item adiado da Fase 11, §0.4): `AISA_GUARD_MODE=enforce` por defeito em `.claude/settings.json` env, script `pre-write-guard.sh` fail-closed (unset ⇒ enforce), deny rules `Write/Edit(./library/**)` repostas. Edição administrativa de `library/`: out-of-band via git (sanctioned path) ou `AISA_GUARD_MODE=log` temporário.
- (c) Nome do log do chairman canonizado: `chairman-synthesis-<F|O|D>-<NN>.md` (chairman-synthesis skill, chairman.md, kernel orchestration.md, ARCHITECTURE §4.4/§6 — antes divergiam entre `R<NN>`, `F-<NN>` e `O-<NN>`).
- (d) Output do `solution-architect` alinhado com o parser do chairman-synthesis (secção `### Proposal`).
- (e) Resíduos removidos: nota de rascunho no `aisa-options` ("— wait, …") reescrita; nota obsoleta no `aisa-round` ("lenses … arrive in a later build phase") corrigida.

**Next-level build (2026-08-31, branch `claude/repo-gaps-analysis-02922z`)** — ver `docs/NEXT_LEVEL_PLAN.md`:
- Vaga 1 (fechar o loop): skill+comando `/answer` (transições de estado + answers.md), comando `/resume`, Decision interativa com `--consult` opcional + row D-NNN no SU (phases/orchestration/chairman alinhados), caminho non-tech no render (`applies_to` + fallbacks).
- Vaga 2 (contrato + wedge): `/blueprint` (kernel `blueprint-contract.md`, skill `aisa-blueprint`, re-sourcing de claude-design-brief e implementation-spec) e `/simulate` (comparação de opções + value-of-information em `_simulation/`).
- Pack pp v1.1.0: R4–R6 do decision-tree reescritas + inputs_used completado; sinais de Discovery neutralizados; novo `delivery-conventions.md` (naming, ALM, stamping `su:` para traceability futura).

**Próxima sessão**: live exec end-to-end (agora incluindo `/answer`, `/simulate` e `/blueprint` na sequência). Sequência recomendada num `claude .` fresco contra um engagement novo (`/start <slug> pp`) — ou contra um existente:

1. `/round` (Discovery — já validado em Fase 5/6, mas rever em conjunto com os PostToolUse hooks novos).
2. `/frame` — validar (a) que as 6 personas arrancam em paralelo (uma única assistant message com 6 Task calls), (b) que o `frame.md` produzido é uma frase única coerente, (c) que apenas o chairman escreve no SU (autores das novas linhas vs `lens-outputs/chairman-synthesis-F-01.md`).
3. `/options` — validar (a) que 7 personas arrancam em paralelo (incl. `solution-architect`), (b) que `options.md` tem ≥3 opções incl. do-nothing + non-tech, (c) que solution-architect consulta `decision-tree.md` + `domain-knowledge/`.
4. `/decide` — fluxo interactivo; auto-corre `aisa-synthesize`; produz 5 topic packs em `_synthesis/`.
5. `/render --all` — produz 6 deliverables em `_render/`; `render-gaps.md` deve ser pequeno (ou vazio).
6. Sanity: grep vendor-name em `_render/discovery-report*.md` e `_render/executive-report*.md` → 0 hits expectados.

Depois disso, **Fase 12 (pilot)** — workshop curto com 2 consultores Galp + 2 engagements paralelos. Esta fase é distribuída (acompanhamento async), não é uma sessão de build.

**Desvio registado (Fase 1)**: `jq` não está instalado na máquina de build (Windows). O hook `pre-write-guard.sh` é um stub em modo `log` no MVP; adicionou-se um guard que faz no-op gracioso se `jq` estiver ausente (em vez de erro em cada Write/Edit). Decisão durável (instalar jq vs reescrever hook em `.ps1`) adiada para Fase 11, conforme §1.10.

**Nota para Fases 3-10 (writes a `library/`)** — **Resolvido em 2026-05-28 (commit `4fff337`)**: regras `deny: Write/Edit(./library/**)` removidas de `.claude/settings.json` (adiadas para Fase 11 conforme §0.4). O hook `pre-write-guard.sh` continua wired e torna-se o guardião real em modo `enforce` na Fase 11.

**Nota (validação YAML, Fase 3)**: PyYAML não está instalado (python existe, módulo `yaml` não). A validação automática de `pack.yaml` (`python -c "import yaml..."`) não correu; o YAML foi validado por inspecção manual (estrutura simples, transcrita de §3.1.1) + contagem objectiva (6 `- id:` deliverables). O runtime aisa lê `pack.yaml` como texto (skills markdown interpretam-no; não há parse Python), por isso PyYAML não é dependência de runtime. Para validação automática de pack-authoring (Fase 11): `pip install pyyaml`.

**Pré-Fase 1 decisões fechadas em 2026-05-27**:
- Localização `aisa/`: `C:\Users\jorge.estevao\Documents\Galp\Claude Code Projects\aisa\` (sibling de SPEA v5) ✅
- Localização `aisa-engagements-galp/`: sibling, criação adiada para Fase 11 ✅
- Git init em Fase 1 ✅
- Hold para sign-off da equipa sobre os 5 documentos `aisa-design/` antes de arrancar Fase 1 ✅

**Quando arrancar Fase 1, ler primeiro**:
1. Este file §16 (state actual) + §1 (acções da Fase 1).
2. Memory entry [[project-aisa-implementation-status]] em `.claude/projects/.../memory/` para retomar estado.
3. ARCHITECTURE.md v0.2.0 (sanity check; spec não pode ter mudado entre sessões).

### Checkpoints por fase

| Fase | Status | Data | Commit hash | Notas |
|---|---|---|---|---|
| 0 — Pre-flight | ☑ done | 2026-05-27 | — | Location confirmed (§0.3/§16); team sign-off closed |
| 1 — Repo skeleton | ☑ done | 2026-05-28 | 29f98cf | jq missing on build machine → hook stub degrades gracefully (no-op); durable Windows fix deferred to Phase 11 |
| 2 — Kernel docs | ☑ done | 2026-05-28 | ce011bf | 5 files; jargon-grep (claim ledger/wave/cell/frontmatter) clean; headers OK |
| 3 — Pack pp foundation | ☑ done | 2026-05-28 | 3afbad6 | glossary 53 / q-bank 45 (7 lenses) / 6 deliverables; lenses_config in pack.yaml; PyYAML missing → YAML checked manually |
| 4 — Discovery skills (3 lenses) | ☑ done | 2026-05-28 | 3a4108e | 6 skills + 7 command stubs; structural validation OK; live /start /round /status exec deferred to Phase 5 (needs fresh `claude .` session) |
| 5 — Discovery validation | ☑ done | 2026-05-28 | e4eae7d | galp-adv-test loop OK (SU 6/6/9/0/3, no-tech grep clean); round-model converged (R-00 seed, increment-at-start) |
| 6 — Restantes lenses | ☑ done | 2026-05-28 | 915b9e0 | galp-adv-test-2 6-lens run: SU 10/10/15/1/6; X-001 Critical conflict (mobile/offline ∧ data sensitivity) detected by governance lens; no-tech clean |
| 7 — Council infrastructure | ☑ done (structural) | 2026-05-28 | 4ee3938 | 8 agents (7 personas + chairman) + 3 skills (lens-technology, chairman-synthesis, aisa-frame); /frame command wired; no-tech grep clean. |
| 8 — Options + Decision + Synthesis | ☑ done (structural) | 2026-05-28 | (bundled with 9-11) | 3 skills (aisa-options, aisa-decide, aisa-synthesize) + 5 synthesis templates in library/kernel/synthesis-templates/ + /options /decide /synthesize commands wired. |
| 9 — Render + 6 templates | ☑ done (structural) | 2026-05-28 | (bundled with 8,10,11) | 6 deliverable templates (incl. new implementation-spec, renamed claude-design-brief) + 3 architecture sub-templates + aisa-render skill (slot-resolution, versioning, render-gaps, --dry-run) + /render wired. |
| 10 — Domain knowledge transplant | ☑ done (structural) | 2026-05-28 | (bundled) | 3 patterns files transplanted from SPEA v5 (powerfx 566 / screen 244 / security 359 lines) + new delegation-matrix.md + decision-tree.md (3 branches, 6 rules + exclusions + missing-inputs protocol). |
| 11 — Enterprise readiness | ☑ done (structural) | 2026-05-28 | (bundled) | 3 authoring docs (PACK/LENS/DELIVERABLE) + 3 skeleton packs (outsystems, mendix, generic) + 4 hook stubs (log-mode) + HOOKS.md + settings.json wired + bootstrap.ps1 + 14 agent-memory _universal/ seed files. Live exec deferred. |
| 12 — Pilot | ☐ todo | — | — | Real-world distributed work with consultants — outside the build sessions. |

### Como actualizar este tracking

No fim de cada sessão de build, actualizar este section:
- Marcar fase como `☑ done`.
- Adicionar `data` e `commit hash`.
- Notas: quaisquer desvios, issues, decisões in-flight.

Se uma fase falha acceptance, manter `☐ todo` e adicionar nota explicando bloqueio. Próxima sessão retoma daí.

---

## 17. Estimativas e timeline

Assumindo ~1 sessão/dia útil:

| Sprint | Fases | Dias |
|---|---|---|
| Sprint 1 | 1-3 | ~3 dias |
| Sprint 2 | 4-5 | ~3 dias |
| Sprint 3 | 6-7 | ~3 dias |
| Sprint 4 | 8 | ~2 dias |
| Sprint 5 | 9 | ~2 dias |
| Sprint 6 | 10-11 | ~3 dias |
| Sprint 7 | 12 (pilot) | distribuído |
| **Total** | | **~16 dias úteis** |

Realista com buffer (iterar quando algo falha): **~3-4 semanas calendário**.

---

## 18. Definition of Done — MVP v0.1.0

aisa MVP v0.1.0 está "done" quando:

- [ ] Todas as 12 fases marcadas `☑ done`.
- [ ] Scenario A (galp-adv) corre end-to-end (start → render --all) sem intervenção manual além de input inicial + USER_ANSWERs e validações.
- [ ] 6 deliverables produzidos têm qualidade ≥ ao que o aisa pp-consulting produzia (assess subjectively + diff template-by-template).
- [ ] 2 engagements pilot completos com retro positivo.
- [ ] `docs/` tem 5 documentos (ARCHITECTURE, PHILOSOPHY, MIGRATION, ONBOARDING, IMPLEMENTATION_PLAN — este).
- [ ] Tag `v0.1.0-MVP` no git de `aisa/`.
- [ ] Email à equipa com link + onboarding session.

---

## 19. Apêndice — Comandos de arranque (próxima sessão)

```bash
# Próxima sessão deve começar com:

# 1. Verificar estado actual
cat aisa-design/IMPLEMENTATION_PLAN.md | grep -A2 "## 16. Resume tracking"

# 2. Ler ARCHITECTURE.md (sanity check)
cat aisa-design/ARCHITECTURE.md | head -50

# 3. Validar pré-condições da fase actual

# 4. Criar TaskList para items da fase
# (use TaskCreate via Claude Code)

# 5. Build!
```

---

**FIM — v1.0.0**

Próxima acção: confirmar localização do repo com Jorge → Fase 1.
