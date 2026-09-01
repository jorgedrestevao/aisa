# Phases — Kernel v0.2.0

The aisa engagement progresses through 4 phases. Each phase declares its mode of orchestration, the lenses active, and soft entry/exit criteria. Phases are defined here; the 5 knowledge states are in [`states.md`](states.md); orchestration modes in [`orchestration.md`](orchestration.md).

## Phase 1: Discovery

**Goal**: Map operational context, shadow stakeholders, as-is process, constraints. Do not name vendor/product.

**Lenses active (sequential order)**: business → operations → user → data → governance → financial

**Mode**: `inline` (each lens sees the Shared Understanding accumulated by previous lenses)

**Entry criteria**:
- `_state.json` exists with `phase: discovery`.
- `context.json` has at minimum: literal request, requester role.
- Capture run for supported inputs — `_capture/` artefacts exist for every `.xlsx`/`.xlsm` in `inputs/` (soft — warn if missing; `/capture` fixes it).

**Exit criteria** (soft, advisory):
- `## Confirmed` has ≥10 rows.
- `## Unknown` Critical = 0.
- `## Conflicted` Critical = 0.
- All 6 lenses have written to `lens-outputs/`.

**Outputs**:
- `shared-understanding.md` populated.
- `lens-outputs/<lens>.md` per lens.

---

## Phase 2: Framing

**Goal**: Synthesize a single sentence: "The problem is X, felt by Y, costs Z today, evidence is W."

**Lenses active**: subset of the 6 Discovery lenses (chairman picks the 3-4 most relevant given the Shared Understanding).

**Mode**: `council-independent` (parallel Task subagents; only the chairman writes to the Shared Understanding).

**Entry criteria**:
- Exit criteria of Discovery met (overrideable with justification).

**Exit criteria** (soft):
- Frame sentence registered in `decisions.md` (D-001 typically).
- Sponsor explicitly confirmed.

**Outputs**:
- `frame.md` in the project root.
- New rows in `## Confirmed` from chairman synthesis.

---

## Phase 3: Options

**Goal**: Generate 3-5 options (including `do nothing` and `non-tech`) with pros/cons against constraints. **The technology lens enters here for the first time.**

**Lenses active**: technology (new) + business + operations + financial (others read-only).

**Mode**: `council-independent`.

**Entry criteria**:
- Phase 2 frame validated by sponsor.

**Exit criteria** (soft):
- ≥3 options recorded, with at least 1 non-technology option.
- `decision-tree.md` from the pack consulted (if applicable).

**Outputs**:
- `options.md` with a pros/cons matrix.
- Optional: `_simulation/options-comparison_v<NN>.md` (via `/simulate`) — a per-option projection (screens, effort band, risks, constraints) plus the value-of-information list of decision-flipping Unknowns.

---

## Phase 4: Decision

**Goal**: Capture choice + justification + alternatives + risks + revision conditions. Auto-trigger synthesis.

**Lenses active**: none by default — the decision is the **user's**. `lens-technology` (via the solution-architect agent) may be consulted ad-hoc with `/decide --consult` for an advisory review of the chosen option.

**Mode**: `interactive` (user-driven). No council synthesis runs in Decision — the council's work ended at Options; here the user chooses and justifies.

**Entry criteria**:
- Phase 3 options reviewed by sponsor.

**Exit criteria** (soft):
- `decisions.md` has the chosen option with justification + alternatives + risks + revision conditions.
- `/synthesize` auto-ran successfully (5 topic packs in `_synthesis/`).

**Outputs**:
- `decisions.md` (D-NNN entries) + the matching `D-NNN` row in the SU `## Confirmed`.
- `_synthesis/{business-story, as-is, architecture-story, risks-and-assumptions, financial-story}.md`.
- For engagements with a UI component: `_blueprint/ux-blueprint_v<NN>.yaml` (via `/blueprint`, per `blueprint-contract.md`) — iterated with the business until approved (its approval is itself a D-NNN).
- Render-ready state.

---

## Transition rules

- Transitions are user-triggered (`/frame`, `/options`, `/decide`).
- Soft gates emit warnings via the `phase-gate-check.py` hook but do not block.
- Override syntax: `/frame --override "reason"` — logged in `decisions.md`.
- Phase regression is allowed (`/round` from Framing returns to Discovery scope if needed).

See [`render-contract.md`](render-contract.md) for what happens after Decision (synthesize → render).
