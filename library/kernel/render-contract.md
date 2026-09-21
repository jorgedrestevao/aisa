# Render Contract — Kernel v0.2.0

## Pipeline: Decision → (Blueprint) → Synthesize → Render

For engagements with a UI component, the Decision phase includes the blueprint loop before final render: `/decide` → `/blueprint` → prototype (external) → business feedback (`/answer`) → blueprint vN → approval (D-NNN) → `/synthesize` → `/render --all`. See [`blueprint-contract.md`](blueprint-contract.md).

```
shared-understanding.md  ──┐
lens-outputs/<lens>.md     ├──→ aisa-synthesize ──→ _synthesis/<topic>.md (5 files)
decisions.md               ─┘                                  │
                                                               ↓
                                              aisa-render ──→ _render/<deliverable>_vNN.<ext>
```

## The doctrine chain

```text
Shared Understanding
        ↓
Decision
        ↓
Architecture
        ↓
Deliverable projections
```

Every deliverable is a **projection contract**. It may select, compress, re-order, change audience language, change prose ↔ table, and perform the **explicitly-authorized bounded downstream transformations** its own contract declares. It may **not** re-settle evidence, re-decide Options, re-select architecture, alter scope, upgrade epistemics, re-grade proof, invent comparator fit, invent far-side design, or silently resolve an Unknown.

### Reasoning versus projection transformation

```text
REASONING
→ settles or changes upstream meaning                          FORBIDDEN downstream

PROJECTION TRANSFORMATION
→ deterministically derives a downstream representation
  from already-authoritative inputs
  under the active deliverable contract                        PERMITTED where declared
```

A projection transformation is legitimate exactly when it is **deterministic**, **bounded**, **declared by the active deliverable contract**, and **traceable to already-authoritative inputs**. Fail any of the four and it is reasoning, and therefore prohibited.

Permitted examples:

```text
architecture obligation        → implementation work package
proof obligation               → acceptance work package
implementation inventory       → estimate work unit
work units + estimation method → effort bands / ranges / arithmetic
approved UX blueprint          → generator-oriented screen block
```

No transformation may create its own upstream truth.

### Layer execution contract

| Layer | Owns | May | May **not** |
|---|---|---|---|
| **Synthesis** (`synthesis-templates/`, `aisa-synthesize`) | bounded narrative per topic, from named authoritative sources | narrate · compress · order · cite ids · refuse to write where sources are thin | decide · compare afresh · select an interpretation · re-grade epistemics · pull Domain Knowledge for richer prose · **compute the implementation estimate** |
| **Deliverable template** (`packs/<pack>/deliverable-templates/`) | projection semantics · allowed transformations · source contract · selection/materiality · structure · applicability | **declare** what to select, how to shape it, and which projection transformations are permitted | **execute anything itself** · reason · settle an upstream value · re-source a fact from raw evidence · include another deliverable's narrative |
| **Render** (this contract, `aisa-render`) | slot resolution order · the fixed architecture include · fragment iteration (0..1 experience, N+M boundary) · versioning · gap classification · applicability skips · **execution of the transformations the active contract declares** | assemble · validate · log · fail loud · execute **only** the projection transformations the active deliverable contract declares | create new upstream facts · choose an option · choose architecture · change scope · resolve an Unknown · promote epistemics · invent work · re-source evidence · create a comparator claim |

> **Render executes a projection contract; it does not reason beyond that contract.**

**No new engine and no new skill.** The executor is the existing `aisa-render`. The template declares; the renderer executes; neither reasons.

## Synthesis layer (`aisa-synthesize` skill)

Auto-runs at the end of `/decide`. Reads the Shared Understanding + `lens-outputs/` + `decisions.md`. Produces 5 topic packs:

| Topic pack | Sources |
|---|---|
| `_synthesis/business-story.md` | Confirmed/Assumed [lens=business] + lens-outputs/business.md |
| `_synthesis/as-is.md` | rows [lens=operations,user] + lens-outputs/{operations,user}.md |
| `_synthesis/architecture-story.md` | decisions.md + rows [lens=technology,data] + lens-outputs/{technology,data}.md + the **fixed** `architecture-templates/architecture-core.md` |
| `_synthesis/risks-and-assumptions.md` | Risky + Assumed + Unknown.criticality=Critical + unresolved Conflicted + expired Confirmed + decisions.md (accepted risks, conditions, preconditions, proof obligations) |
| `_synthesis/financial-story.md` | rows [lens=financial] + lens-outputs/financial.md + decisions.md (economic anchors) + options.md S8 — **decision economics ONLY** |

Each topic pack template lives in `library/kernel/synthesis-templates/<topic>.template.md`.

**Synthesis computes no implementation-effort figure.** The implementation estimate is semantically owned by the `estimate` deliverable and executed by `aisa-render` under that deliverable's projection contract. Financial synthesis carries decision economics; any implementation-effort prose there may only reference or project an already-produced Estimate, and is never where a figure first appears.

**`architecture-story.md` is a durable carrier, not architecture authority.** Where the architecture-entry gate yielded `not-authorized`, no blueprint version exists to hold the pair; the outcome basis stays in `decisions.md`, and the architectability basis — whose **semantic owner is the architecture-entry gate rule** — is durably carried in `_synthesis/architecture-story.md § Authorized scope and outcome basis`. Downstream deliverables read it **as that carrier** and never as a source of architectural truth; **no deliverable re-evaluates pack architectability**. This is the only such carriage exception, and it does not generalize to any other architecture field.

## Render layer (`aisa-render` skill)

Reads the topic packs + decisions + the architecture record + the pack's `deliverable-templates/<deliverable>.template.md`. Produces output in `_render/`.

### Coverage: two checks, and neither of them renders anything

Since kernel v0.2.0 the render layer answers the **preservation** question through the coverage motor ([`coverage-contract.md`](coverage-contract.md) §8.2, §8.3). Two checks, at two moments, and they are not the same question:

| moment | question | where the answer lives |
|---|---|---|
| **pre-render**, per deliverable | are the authorities **this** deliverable declares current, and does the version it must read exist? | `coverage.py check --stage render --deliverable <id>` (no `--target`) |
| **post-render**, per produced file | does the produced document carry the obligations the projection contract selected? | a stage-`render` coverage review of that file |

**The pre-render check reports facts; the template decides.** Which blueprint version a deliverable reads is declared by that deliverable's own `blueprint_version_read` (below); whether it is produced at all is declared by its `activation` / `blocked_when` / `not_applicable_when`. The motor resolves the version and reads the upstream review — it never derives applicability, and it never re-decides what the contract already declares.

**Not reaching an authority is not a gap.** A deliverable whose required version does not exist is `blocked` or `not applicable` with its reason, logged as a **skip** to `render-log.md` — never an entry in `render-gaps.md`. The three reasons an approved version can be missing stay distinct: no architecture authorization at all · authorized and not yet approved · a `structural: true` choice keeping approval blocked.

**A lost obligation is a gap, and the renderer does not invent it back.** Where the post-render review finds a selected obligation `partial` or `missing`, the entry goes to `render-gaps.md` with its owner, the deliverable is **not** declared complete, and the fix goes to the owner upstream. Render never reopens the source workbook to fill a slot, never edits the Shared Understanding, never resolves an Unknown and never upgrades an epistemic state. **An id carried in a comment is a reference, not a projection** — it does not prove preservation, and the motor refuses it as an anchor.

Coverage of a deliverable is **not** its approval and **not** proof that the solution works end to end. Absence of a review reads `not_evaluated`: never "complete", never "failed", and never a reason to revoke an approval already on file.

### The six projection contracts

| # | Canonical deliverable | Runtime id / file | Primary semantic authority |
|---:|---|---|---|
| 1 | Discovery Report | `discovery-report` | `shared-understanding.md` |
| 2 | Executive Report | `executive-report` | `decisions.md` `D-NNN` |
| 3 | **Architecture Blueprint** | `solution-blueprint` (alias) | the `architecture:` block of the **latest authorized** blueprint version (`v<latest authorized>`, its approval state declared) + the fixed architecture shape |
| 4 | Implementation Specification | `implementation-spec` | the `architecture:` block + the approved UX blueprint |
| 5 | Claude Design Brief | `claude-design-brief` | the **approved** UX blueprint |
| 6 | Estimate | `estimate` | **itself**, for the calculation (executor: `aisa-render`) |

Each template declares `canonical_deliverable`, `activation`, `authority_sources`, `conditional_sources`, `forbidden_sources`, `permitted_transformations` and `forbidden_transformations`. Those fields describe the active projection contract; they are **not** a router, and there is no concern→deliverable map and no outcome→template map.

**Exactly two bounded deliverable→deliverable read edges** exist, and no third:

| Edge | Payload | Excluded |
|---|---|---|
| `implementation-spec → estimate` | **inventory only** — components · obligations · proof work · migration steps · open work items | narrative · rationale · architecture description · acceptance text |
| `estimate → executive-report` | **the headline only** — one investment paragraph at decision altitude | phases · work breakdown · team mix · detailed range derivation · contingency detail · candidate inventories |

`--all` renders (4) before (6) before (2). The Executive Report never becomes a second Estimate authority: where the Estimate is `not applicable`, blocked or not produced, the Executive is **complete without an implementation-effort paragraph** — no gap, no placeholder, and no calculation inside the Executive or inside synthesis. The read graph is otherwise strictly downstream and **acyclic**.

### Slot resolution order

1. `_synthesis/<topic>.md` (declared by the template).
2. The architecture record + the fixed architecture shape (where the template declares them).
3. Shared Understanding structured rows (for tables, lists), with state and validity.
4. `decisions.md`.
5. `context.json`.
6. Computed — **only** where the active contract declares the transformation.
7. If none AND the slot is `required` → fail loud, log to `render-gaps.md`.
8. If none AND the slot is `conditional` and its condition does not hold → **not applicable**: omit and log a skip.
9. If none AND the slot is `optional` → omit the section.

### Versioning

- `v01`, `v02`, ... — `/render` always produces the next available version.
- Never overwrites existing files (user edits to v01 are preserved).
- `_render/<slug>_<deliverable>_v<NN>.<ext>` is the filename pattern.

### Counterfactuals

`_simulation/counterfactuals/<O-NNN>.md` (frozen at `/decide`) are engagement artefacts, not deliverables — they never render. The executive-report may carry the decision's structured tripwires via a conditional slot.

### Applicability

Applicability is declared per deliverable — in the template's `activation` / `not_applicable_when` / `blocked_when` fields, mirrored in `pack.yaml`'s `activation` metadata. It is **not** derived from whether the decision happened to be technological.

| State | Meaning | Behaviour |
|---|---|---|
| **required** | the deliverable's activation holds | render it |
| **conditional** | it holds for part of the situation | render the applicable part, state which part |
| **not applicable** | the activation does not hold | **do not produce it**; log a **skip** with the reason to `render-log.md`. **Never** an entry in `render-gaps.md` |
| **blocked** | a required authority does not yet exist | do not produce it; log the block with the reason and what would unblock it |

The architecture discriminator is **does an architecture authorization exist for at least one scope?** A positive outcome over a solution the active pack cannot architect authorizes no architecture: the Architecture Blueprint, the Implementation Specification and the Claude Design Brief are then `not applicable`, and the Executive Report carries the outcome basis and the architectability basis as **two distinct reasons** — neither relabelled *decision blocked*.

**Structural blocking, mechanically.** A `structural: true` open architecture choice blocks blueprint **approval** (`blueprint-contract.md` hard rule 5). The Implementation Specification and the Claude Design Brief both require the **approved** blueprint, so both are **blocked**. No materiality override, no partial approval and no UX-only approval exists.

**Whose contract is being read.** Each template also declares its own `template_id`, and a coverage review's `deliverable.id` must equal it. The two fields are declared by the same record and nothing else makes them agree: a review that calls itself the Implementation Specification while reading the Architecture Blueprint's template inherits `v<latest authorized>`, agrees with itself, and comes out complete **with no approved version in existence**. Identity is checked before the version, and a version is never resolved from another deliverable's contract.

**Where version selection is written.** Each template declares it in its frontmatter field `blueprint_version_read`, with exactly three tokens — `v<latest authorized>`, `v<approved>`, `none` (this deliverable reads no blueprint version). The field being **absent** is a contract defect, not a synonym for `none`: silence in the field that decides the authority version is the one reading the motor will not guess. The coverage motor translates the token, resolves it against the engagement, and **verifies** that a stage-`render` review consumed that version; a review of `v01` consumed for `v02` is `COV-AUTHORITY-MISMATCH`.

**Which blueprint version each deliverable reads (P-18 / F08).** Version selection is explicit per deliverable, never "the newest file": the **Architecture Blueprint** reads `v<latest authorized>` — the latest non-draft version whose `architecture.authorization` is `authorized` or `authorized-bounded` for at least one scope — and **declares** its approval state (`aprovada (D-NNN)` · `não aprovada — N escolha(s) estrutural(is) em aberto` · `não aprovada — aguarda aprovação do negócio`), because the candidate-architectures section exists only while a structural choice blocks approval; the **Implementation Specification** and the **Claude Design Brief** read `v<approved>` (the version a `Blueprint bp-v<NN> aprovado` D-NNN names). Authorization is a recorded architecture fact; approval is a human decision; a deliverable names which one it depends on.

**Decision blocked (outcome class 12).** Expected deliverables: Discovery Report + Executive Report. The Architecture Blueprint, Implementation Specification, Claude Design Brief and Estimate are `not applicable`. No future implementation work is invented.

### Architecture-containing output

A deliverable that includes the architecture renders it **only where an architecture authorization exists for at least one scope**. That authorization is the discriminator. Where no scope is authorized, render the emitted outcome basis instead and log a skip with the reason; a skip is not a gap.

The include is **fixed**: `architecture-templates/architecture-core.md`. There is no branch, no per-decision template lookup, no dynamic path and no router. The core resolves **zero or one** experience fragment from `architecture.experience.mode` (`none` → **zero** includes) and **zero or more** boundary-fragment instances — exactly N unique qualifying composition components + M unique relocated responsibilities, six channels each.

The architecture authorization is initialized once, at blueprint entry (see [`blueprint-contract.md`](blueprint-contract.md)), and is **read** by the render layer — never derived, upgraded or downgraded here.

### Scope-ownership projection categories

Where more than one `(scope, outcome)` pair exists, the deliverable layer projects **four render categories** — not states, not outcome classes, not epistemic values:

| # | Category | Consequence |
|---:|---|---|
| 1 | **architected here** | full A-sections; estimated |
| 2 | **relocated — boundary represented** | one boundary fragment instance, six channels; no far-side design; PP-side integration obligation estimated |
| 3 | **excluded — destination unevaluated** | **nothing** — no design, no boundary component, no owner, no imports, no gates; **never estimated**, and the exclusion is stated |
| 4 | **not applicable — no architecture authorization** | no architecture; the outcome basis + architectability basis carry the meaning |

No category may be inferred from another, and no fifth category exists. The far side never enters PP scope by silence.

### Render-gap classes

Four classes. **Not every missing slot is decision-blocking**, and the epistemic difference is preserved:

| Class | Trigger | Behaviour |
|---|---|---|
| **not applicable** | the section's — or the **deliverable's** — trigger does not hold | Omit / do not produce; log a **skip** with the reason to `render-log.md`. **Not a gap** |
| **optional** | an optional section with no content | Omit |
| **open work item** | a required section that **owned work** can still resolve | Render the open item with **its owner** and what would settle it; log it to `render-gaps.md`. **Not** decision-blocking |
| **decision-blocking** | no architecture authorization for any scope, or the decision itself forbids one | Render nothing architectural; render the emitted outcome sentence (+ the architectability basis) instead |

**Class 3 carries an owner:**

```text
owner ∈ { architecture | implementation | design | estimate | evidence }
```

The label generalizes the former *architecture work item*; the semantics, trigger and behaviour are unchanged. **No fifth class. No parallel taxonomy.**

**Deliverable-level skips never pollute `render-gaps.md`.** A deliverable that is `not applicable` for the situation is a skip logged in `render-log.md` with its reason. `render-gaps.md` remains the file that screams; skips must not dilute it.

A decision-blocked outcome is produced by the decision layer: the render layer may **repeat** it and never derive it.

### Output formats

- Markdown by default.
- Conversion to .docx via Pandoc (post-render step, optional in MVP).

See [`phases.md`](phases.md) for the phase that triggers this (Decision) and [`states.md`](states.md) for the row states the synthesis layer reads.
