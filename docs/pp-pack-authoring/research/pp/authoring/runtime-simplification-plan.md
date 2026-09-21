# Runtime Simplification Plan — kernel lens/persona/orchestrator layer

<!--
provenance: PLAN (no runtime file modified; no pack file modified)
scope: kernel lens contract, persona agents, orchestrators, capture layer, SU scaffold
authored: 2026-09-03
basis: research/pp/authoring/lens-contract-audit.md + approved decisions D1-D9
path note: written to the repo's actual `research/pp/authoring/` directory
  (`docs/pp-pack-authoring/research/pp/authoring/`), alongside the audit it
  implements. No root-level `research/` exists; creating one would fragment
  the workstream (same reasoning as the audit's own path note).
-->

Implements the nine approved decisions, plus the four amendments approved at plan review:

1. `lens-technology`'s pack-aware exception **accepted** — the 6 Discovery lenses stay pack-agnostic (§2/D5).
2. The mandatory per-round raw spot-check quota **removed**, replaced by materiality-based raw verification (§5).
3. Lens/persona character targets are **soft authoring guardrails**, never PASS/FAIL conditions (§7/§8/§11).
4. The deferred PP signal trim targets **preferably 5–8 cues per Discovery lens** (§9).

Evidence is the audit; this document does not restate it.

---

## 1. Target architecture

Three tiers, each owning one thing exactly once.

| Tier | Files | Owns | Never contains |
|---|---|---|---|
| **Kernel contracts** | `library/kernel/{states,orchestration,phases}.md` | epistemic semantics (half-lives, question economics, transitions), evidence-reading protocol, mode mechanics | perspective, pack knowledge |
| **Orchestrators** | `aisa-round`, `aisa-frame`, `aisa-options`, `aisa-capture`, `aisa-status`, `aisa-start` | execution mechanics: round + id bookkeeping, shared-evidence provisioning, pack-signal resolution/injection, council common preamble, question-bank access at the one step that formulates questions | domain reasoning, lens perspective |
| **Perspectives** | `lens-*/SKILL.md`, `.claude/agents/<persona>.md` | stance, the lens-specific reasoning move, the 4 invariants that must fire mid-reasoning | filesystem enumeration, stamping tables, output schemas, pack parsing, orchestration |

Data flow per Discovery round:

```
inputs/ ──(parse once, deterministic)──> _capture/  ──┐
                                                      ├─> orchestrator invocation ─> lens (perspective only)
pack.yaml lenses_config.<lens>.extra_signals ─────────┘        │
                                                               └─ raw inputs/ remain openable whenever
                                                                  material to confidence
```

Four principles the plan is checked against: parse once / reason many · evidence-heavy authoring, evidence-light runtime · signals are cues, not coverage · framework text shrinks.

### 1.1 What "simplification" means here (scope note)

Added at the authoring-principle alignment (2026-09-04). Nothing in A–G is reversed; this fixes how the four principles above may be read.

**Every reduction in this plan is a reduction of *framework text*, never of analytical coverage.**

- *Framework text shrinks* means mechanics stated once instead of seven times. It does not mean a lens reasons less, stops early, or drops a material tension to stay small. **Light framework, not lightweight reasoning.**
- *Signals are cues, not coverage* cuts both ways: no cue creates an obligation, **and no missing cue removes one**. A lens follows a material concern that no universal signal, injected pack cue or question-bank entry names.
- *Evidence-light runtime* is about what is loaded, not about how hard the runtime thinks. Evidence-light runtime ≠ decision-light reasoning.
- The size figures in §4, §7, §8 and §9 are **diagnostics and soft authoring heuristics** — already stated as such and unchanged. They report where the budget went; they are never a stopping rule for analysis and no validator asserts them.
- **Compact output ≠ shallow reasoning.** The §D6 three-heading block and atomic SU rows constrain what is *written*; the reasoning that decides what is material enough to write may be substantial.
- **Materiality determines depth** — depth rises with materiality, uncertainty, risk and decision consequence. This is the same rule §5 already applies to raw verification, generalised: *depth when material to the decision, not to satisfy a quota, and not suppressed to satisfy a size target*.

Authoritative statement of the principles: `pp-pack-authoring-map.md` §1.5. Lens-side statement: `docs/LENS_AUTHORING.md` → *Reasoning depth*.

---

## 2. D1–D9 implementation mapping

### D1 — Input model: HYBRID

**Change.** The orchestrator provides already-ingested evidence; the lens reads shared evidence first and opens a raw source only when its perspective needs more than the extraction preserved.

- `orchestration.md` → *Reading input documents* becomes the single owner: shared evidence first (`_capture/evidence-index.md`), the format→tool table stays here for raw inspection, and the citation invariant stays here in full.
- Each lens `Inputs` section keeps **one line** naming what it privileges (data lens: the column profile in the extraction JSONs; operations lens: transcript exception passages; technology lens: the full SU).
- The rule, stated once: *shared extraction is the normal evidence surface; inspect the raw source when material to confidence* (§5).

**Not built.** No routing table, no per-lens evidence manifest, no relevance scoring. Which raw source a lens opens is a judgement the lens makes, not a mechanism the framework encodes.

**Invariant preserved.** Cite what you opened, never a filename alone (moves to lens Hard rule 3, verbatim). Raw verification is **risk-based, not per-round quota** — see §5.

### D2 — Capture model: CAPTURE-LITE

**Change.** New deterministic text tier for `.docx` / `.pdf` / `.vtt`. Structured xlsx capture (L1/L3/L2) unchanged. Detail in §5.

### D3 — State metadata in lenses: pointer + minimum local defaults

**Change.** Lens hard rules 5/6/7 (~1,000 chars each lens) collapse to two lines:

```
5. Stamp what you write. Confirmed/Assumed carry `verificado_em` + `validade`;
   Unknown carry `custo` + `swing`. Semantics: `library/kernel/states.md`.
   In doubt: `validade = organizacional`. Never leave `custo`/`swing` blank.
6. An expired row reads as weak Assumed — never cite it as Confirmed.
```

Local defaults survive because a default consulted elsewhere is a default not applied. Tables, class lists and swing vocabularies stay in `states.md` only. `states.md` needs no edit — it is already authoritative.

### D4 — Append-only invariant: keep locally, minimal

**Change.** One clause per lens, unchanged in force:

```
4. Shared Understanding is append-only. Never rewrite a previous row;
   a transition adds a row carrying `was <id>`.
```

SU mechanics (resolved markers, sanctioned edits, status counting) stay in `states.md`.

### D5 — Pack signal delivery: ORCHESTRATOR INJECTION

**Change.**

1. Delete the `pp pack additions:` line from all 6 Discovery lenses (7 boundary violations, 3 vendor-vocabulary leaks).
2. Delete `lens-technology`'s inlined 5-constraint list (duplicate of the file it already reads).
3. `aisa-round` resolves `_state.json.pack` → `library/packs/<pack>/pack.yaml` → `lenses_config.<lens>.extra_signals` once per round and passes the list into each lens invocation. `aisa-frame` / `aisa-options` do the same in the Task prompt.
4. Lens Signal catalog keeps the universal token list and one line: *the active pack may add attention cues; the invocation carries them. Cues, not a checklist.*
5. Delete execution step 3's `for each signal not covered → Confirmed/Assumed/Unknown` loop from all 6 Discovery lenses. This is the edit that makes signals cues again.

**Scope of D5 — accepted at plan review.**

- The **6 Discovery lenses remain pack-agnostic**: they never read `pack.yaml`. Pack-specific Discovery signals are injected by the orchestrator.
- **`lens-technology` remains Options-only and pack-aware.** It may selectively read `decision-tree.md` and the relevant `domain-knowledge/*.md`, plus `lenses_config.technology.constraints_to_check`.
- **Duplicated inline constraint knowledge is removed** wherever the pack is already authoritative — here, the 5-constraint list copied into the lens's Signal catalog.

`LENS_AUTHORING.md` states this distinction explicitly so drift cannot re-open it.

### D6 — Lens outputs: keep, lightweight

**Change.** `lens-outputs/<lens>.md` stays (it has six downstream consumers, §3). Its shape becomes fixed and small — appended once per round:

```markdown
## <round> — <lens>

**What matters** — 2-4 sentences.
**Tensions / risks** — bullets, or `(none)`.
**Open evidence** — what this lens could not close, and where the answer lives. Or `(none)`.
```

Hard dependency: the round id must appear in the file — `pre-lens-order-check.py` greps the in-progress round string. The `## <round> — <lens>` header satisfies it. "1-3 paragraph narrative" is replaced by the three headings; the SU remains the atomic-knowledge surface.

### D7 — Council personas: identity + mandate + independent perspective

**Change.** Persona agent file keeps: frontmatter, `## Identity`, `## Mandate per phase`, `## Memory consulted`, and a single lens-pointer line. Deleted from every persona file:

- the `## Mode (council-independent)` block → the launch prompt already carries ~90% of it; the remainder moves there;
- the `## Output format` block (~900 chars × 7) → becomes one shared block in the council launch preamble, with `chairman-synthesis` as its documented owner;
- the re-stated lens hard rule ("all hard rules apply verbatim" + one of them restated) → the launch preamble states the two that bind a read-only persona (no vendor naming; no Confirmed without evidence).

`aisa-frame` step 5 / `aisa-options` step 5 stop instructing the persona to read `.claude/skills/lens-<lens>/SKILL.md`. One channel, chosen: the invocation.

### D8 — Question bank: question-generation resource

**Owner: `aisa-status` step 6** — the smallest existing runtime location that already formulates questions for humans (it builds the meeting agenda from open Unknowns and already resolves `pack.yaml` for `epistemics.half_lives_override`).

**Change.** Step 6 gains one sub-step: resolve `pack.yaml → question_bank`, read it, and use it to (a) phrase each agenda item as an askable question rather than echoing the terse `pergunta` cell, and (b) add a probe (`P-<LENS>-NN`) only where the SU shows its stated trigger observed. Core questions are not enumerated; the bank is read at this step and nowhere else.

**Not built.** No new skill, no index, no per-lens loading, no `question_bank` resolution in `aisa-round`, `aisa-frame`, `aisa-options`, `/answer` or any lens. Single consumer by design — two consumers would drift.

Consequence: the `question_bank:` key in `pack.yaml` acquires a real resolver, and the 506 authored lines stop being inert without becoming permanent context.

### D9 — SU scaffold: fix contract drift

**Change.** `aisa-start` step 8, `## Unknown` header:

```
| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
```

Contract alignment only. `dashboard.py` maps SU columns by header name and tolerates absence (`custo_inferred` / `swing_inferred`), so this is additive. `docs/ARCHITECTURE.md §4.1`'s illustrative block gains the same columns or an explicit "normative schema is `states.md`" note (the note already exists in prose; the table contradicts it).

---

## 3. Files affected

| # | File | Change | Regression risk | Existing check |
|---|---|---|---|---|
| D5,D3,D4,D1,D6 | `.claude/skills/lens-{business,operations,user,data,governance,financial}/SKILL.md` | rewrite to the target contract (§7) | **Medium** — behaviour lives in these files | `pre-lens-order-check.py` (order); no shape assertion anywhere |
| D5,D3,D4,D1,D6 | `.claude/skills/lens-technology/SKILL.md` | same, minus pack reads; `## Phase gate` kept verbatim | Low | none |
| D1,D2 | `library/kernel/orchestration.md` | *Reading input documents* rewritten as the single owner: shared evidence first, format table for raw inspection, citation invariant, capture protocol (step 1.5 a–d moves here) | Low | none |
| D7 | `library/kernel/orchestration.md` → *Council-independent mode* | add: the invocation carries mechanics + output schema; personas do not read lens skills | Low | none |
| D1,D5,D6 | `.claude/skills/aisa-round/SKILL.md` | step 3.6 (new): resolve pack signals + evidence index; step 4b: pass signals, id base, round; step 4c: assert the 3-heading output | **Medium** — the Discovery entry point | `pre-lens-order-check.py`; `phase-completeness.py` has no Discovery contract |
| D5,D7 | `.claude/skills/aisa-frame/SKILL.md` | step 5 prompt: + pack signals, + shared-evidence pointer, + output schema block, − "read your lens SKILL.md", − per-persona mechanics | **Medium** | `phase-completeness.py check_framing` (6 `_council-prep` files, artefacts) — unaffected by prompt text |
| D5,D7 | `.claude/skills/aisa-options/SKILL.md` | same; `solution-architect` keeps its `decision-tree.md` + `domain-knowledge/` reads | **Medium** | `phase-completeness.py check_options` |
| D7 | `.claude/agents/{business-analyst,operations-lead,user-advocate,data-steward,compliance-officer,cfo-lens,solution-architect}.md` | reduce to identity + mandate + memory + lens pointer | Low — the deleted content moves into the prompt that invokes them | none |
| D7 | `.claude/skills/chairman-synthesis/SKILL.md` | document ownership of the persona return schema (it already parses those six sections) | Low | `synthesis-validate.py` (log-only) |
| D2 | `library/kernel/tools/text_extract.py` **(new)** | deterministic docx/pdf/vtt → markdown + identity JSON | Low — additive; failure is soft | none → **one new test justified** (§4) |
| D2 | `.claude/skills/aisa-capture/SKILL.md` | add the text tier + `evidence-index.md`; supported-formats and degradation tables extended | Low | `_capture-log.md` audit trail |
| D8 | `.claude/skills/aisa-status/SKILL.md` | step 6: resolve + consult `question_bank` | Low | none |
| D9 | `.claude/skills/aisa-start/SKILL.md` | SU `## Unknown` header + `_capture/` in the scaffold listing | Low | `dashboard.py` header-name mapping |
| docs | `docs/LENS_AUTHORING.md` | six-section responsibilities restated per §7; the false claim that a lens "picks up pack signals at runtime via the pack metadata" corrected to orchestrator injection; audit checklist item 4 ("read every file in inputs/") replaced by the shared-evidence + materiality-based verification check | Low | none |
| docs | `docs/ARCHITECTURE.md` | §4.1 SU table columns (D9); §7.2 lens contract template; §3.4 council mechanics ownership | Low | none |
| docs | `docs/PACK_AUTHORING.md` | `extra_signals` are injected cues, not lens-file entries; `question_bank` has one consumer (`/status`) | Low | none |
| docs | `.claude/hooks/HOOKS.md` | note that `pre-lens-order-check` depends on the round id in the lens-output header | Low | n/a |

**Dependencies.** D3/D4/D5/D6 → lens rewrite (one pass, not four). D1 → `orchestration.md` before lenses. D2 → `text_extract.py` before `aisa-capture` before the lens `Inputs` line can promise an evidence index. D7 → orchestrator preamble before persona files are trimmed (never the reverse: trimming first leaves a round with no output schema). D8 and D9 are independent.

**Tests that already exist:** `pre-lens-order-check.py`, `phase-completeness.py`, `pre-write-guard.py`, `dashboard.py --engagement <slug>`, `/status --check`. **New test genuinely necessary:** exactly one, for `text_extract.py` (§4).

---

## 4. Deletions / consolidations

Deleted outright (not moved):

| Content | Copies | Chars/copy | Why it goes |
|---|---|---|---|
| Execution step 3 per-signal coverage loop | 6 | ~280 | restates `states.md`; converts cues into a checklist |
| `pp pack additions:` line | 6 | ~250 | boundary violation, stale, 3 vendor leaks |
| `lens-technology` inlined constraint list | 1 | ~300 | duplicate of the manifest it reads |
| Final `council-log.md` append step | 7 | ~75 | `aisa-round` step 5c already does it |
| Step 1 round + next-free-id bookkeeping | 6 | ~290 | orchestrator computes and passes it |
| Persona `## Output format` schema block | 7 | ~900 | the chairman is the consumer; one copy in the preamble |
| Persona `## Mode` block | 7 | ~600 | already in the launch prompt |
| Persona lens-binding restatement | 7 | ~200 | one pointer line replaces it |
| "read your lens `SKILL.md`" in council prompts | 2 skills × 7 personas | — | one channel only |

Centralized (moved, one copy):

| Content | From | To |
|---|---|---|
| Step 1.5 a–d capture protocol | 6 lenses (~1,200 each) | `orchestration.md` → *Reading input documents* |
| `inputs/` parse-every-file bullet + format→tool table | 5–7 lenses | `orchestration.md` (raw inspection) + `aisa-capture` (the parse-once pass) |
| Shared Inputs bullets (`context.json`, SU, `lens-outputs/*`, `<engagement>` resolution, agent-memory paths) | 6 lenses (~380 each) | orchestrator invocation + `orchestration.md` |
| Stamping / pricing / expiry tables | 6–7 lenses (~1,000 each) | `states.md` (already there) + 2 local lines |
| SU append mechanics | 7 lenses | `states.md` + 1 local clause |

Replaced by a short pointer: pack signals (one line), state semantics (two lines), append-only (one clause), council schema (one preamble block).

**Measured budget** (chars of framework text; `text_extract.py` is code, never loaded into a model's context, so it is excluded):

| | Now | After | Δ |
|---|---|---|---|
| 7 lens files | 42,849 | ~11,200 | **−31,600** |
| 7 persona files | 22,397 | ~7,700 | **−14,700** |
| `orchestration.md` | 4,889 | ~6,100 | +1,200 |
| `aisa-round` | 3,240 | ~4,100 | +900 |
| `aisa-frame` + `aisa-options` | 20,099 | ~21,500 | +1,400 |
| `aisa-capture` | 6,259 | ~7,800 | +1,500 |
| `aisa-status` + `aisa-start` | 9,016 | ~9,700 | +700 |
| **Static total** | **108,749** | **~68,100** | **−40,600 (−37%)** |

Per-round loaded context matters more than static total:

- **Discovery round**: 6 × 6.1k = 36.6k → 6 × 1.6k + ~2.5k orchestrator preamble ≈ 12.1k (**−67%**).
- **Council round**: 7 agents × 3.2k + 7 lens files × 6.1k = 65.2k → 7 × 1.1k + 7 × 0.9k preamble ≈ 14.0k (**−79%**), while raw `inputs/` re-parsing drops from 7× to 1× (§5).

Framework text shrinks; engagement evidence is what grows in relative share. Gate H/I: YES.

---

## 5. Capture-lite boundary

**Extraction responsibility.** One new deterministic script, `library/kernel/tools/text_extract.py`, invoked by `aisa-capture` — never by a lens. No LLM in this path.

**Normalized output location.** `<engagement>/_capture/`, matching the existing xlsx tier:

| Artefact | Content |
|---|---|
| `<file>.text.md` | the extracted text, provenance markers inline |
| `<file>.extraction.json` | `identity` only: `sha256`, `modified`, `size`, `format`, `status`, unit counts. Enables the existing `aisa-round` step 3.5 freshness check unchanged |
| `evidence-index.md` | **one table for the whole engagement**: source · format · normalized file · status · provenance unit. The single entry point a lens is pointed at |

**Minimum provenance** (per format, deterministic, no interpretation):

| Format | Library | Marker written into `<file>.text.md` | Cite as |
|---|---|---|---|
| `.docx` | `python-docx` | `[¶NN]` per paragraph; `### <heading>` preserved; tables as markdown | `<file> · §<heading> ¶12` |
| `.pdf` | `pypdf` (fallback `PyMuPDF`) | `[p.N]` per page; detected heading lines kept as `### ` | `<file> · p.7` |
| `.vtt` | stdlib | `[HH:MM:SS] Speaker:` per cue, consecutive cues from one speaker merged | `<file> · [00:12:34] <speaker>` |

All three libraries verified present in this environment (`python-docx`, `pypdf`, `PyMuPDF`).

**No new id namespace.** Locators are plain text in the SU `evidência` column, which already accepts `inputs/<file>:<locator>`. `PM-NNN` remains the only capture id space, and it stays xlsx-only. (Gate B: no new evidence taxonomy.)

**No semantic summarization.** The text tier writes no model, no findings, no interrogation list, no §-structure interpretation. Loss-minimizing extraction only: everything the source said, plus where it said it. The L2 process model (LLM) stays scoped to `.xlsx`/`.xlsm`. (Gate G: YES → NO.)

**Fallback when extraction fails.** Mirrors the existing xlsx degradation contract exactly:

| Situation | Behaviour |
|---|---|
| library missing | `status: skipped` in the index + `_capture-log.md`; lens falls back to raw reading. Never an empty extraction file |
| encrypted / corrupt / image-only PDF | `status: failed` + reason in the index; lens falls back to raw reading |
| `.vtt` with no cues | `status: empty` — stated explicitly; absence is evidence |
| unsupported format (`.pptx`, images, `.msg`) | not captured, not a failure; the format→tool table in `orchestration.md` governs |

**How a lens inspects raw evidence.** Unchanged and always available: `inputs/` is read-only primary evidence, opened with the format→tool table in `orchestration.md`. No permission mechanism, no manifest: raw files were never gated and are not gated now. A lens opens one when its perspective needs detail the extraction did not preserve (cell-level formulas, a passage's full context, tone in a transcript), or to verify a claim per the rule below.

**Raw verification is materiality-based.** The mandatory *≥1 `PM-NNN` raw spot-check per lens per round* is deleted. In its place, one paragraph in `orchestration.md` and one sentence in the lens Execution step 1:

> Shared extraction is the normal evidence surface. Inspect raw evidence when material to confidence: when extraction may have lost relevant detail, a material claim depends on interpretation, evidence conflicts, provenance is insufficient, or the lens needs context the extraction did not preserve.

**Principle: verify raw evidence when material to confidence, not to satisfy a quota.**

Preserved unchanged: cite evidence you actually inspected, at the appropriate level. Evidence integrity is not weakened — a mismatch between the extraction and the raw source still produces a **Conflicted** row citing both (`PM-NNN` vs the raw `sheet!cell` / locator) and flags a capture re-run in `_capture-log.md`, and raw files stay authoritative on conflict.

---

## 6. Orchestrator changes

Four additions, all bookkeeping. None performs domain reasoning.

**6.1 Shared evidence** — `aisa-round` step 3.5 already runs the freshness check and invokes `aisa-capture`. Step 3.6 (new): read `_capture/evidence-index.md` and carry it into each lens invocation as *"shared evidence for this round: <index table>; raw sources at `inputs/`"*. Council orchestrators add the same pointer to the Task prompt in place of "read every file under `inputs/`".

**6.2 Pack signals** — resolve `_state.json.pack` → `pack.yaml → lenses_config.<lens>.extra_signals` once per round; inject as *"Pack attention cues (`<pack>`): a, b, c — cues, not a checklist; uncovered cues are not gaps."* Empty or absent key → inject nothing. The trailing clause is load-bearing: it is what stops injection from re-creating the coverage loop D5 deletes.

**6.3 Question generation** — `aisa-status` step 6 only (D8). No other skill resolves `question_bank`.

**6.4 Council common mechanics** — one preamble block, authored once and used verbatim by `aisa-frame` step 5 and `aisa-options` step 5: read-only tool grant · no in-flight peer reads · returns, does not write · the two binding hard rules · the return schema (owned by `chairman-synthesis`) · shared evidence pointer · pack cues. Replaces seven copies of the same three sections in the persona files.

**Also passed, replacing lens bookkeeping:** current round id, and the next free id per SU section.

**Flag — nothing here reasons about the domain.** The orchestrator resolves paths, reads a manifest key, reads an index, and concatenates a preamble. It does not decide which evidence is relevant, which signals matter, which questions to ask, or how to state a claim. If a later revision has the orchestrator scoring evidence relevance, ranking signals, or selecting questions, that is the line being crossed.

---

## 7. Lens target contract

Six sections preserved, in order. Indicative size ~1,600 chars per lens (from ~6,100), with Role and the lens-specific reasoning step unchanged or longer.

**Sizes here are lightweight authoring heuristics, not gates.** They say where the budget should go — perspective up, mechanics down. **Material growth beyond the lightweight target requires justification; size alone does not determine PASS/FAIL.** No token counter and no size validator is introduced; §11's PASS conditions check *content*.

| Section | Responsibility | Size |
|---|---|---|
| **1. Role** | Distinct, non-substitutable perspective. Persona sentence + the 3–4 questions it sees every request through. Keep the sharp stances verbatim (operations *distrusts the documented process*). | ~500, unchanged |
| **2. Inputs** | What this lens privileges — one line. Shared evidence first; raw source when the perspective needs it. No filesystem enumeration. | ~150 (was ~1,176) |
| **3. Outputs** | Two lines: SU rows tagged `lens=<name>`; a `lens-outputs/<name>.md` block in the fixed 3-heading shape under a `## <round> — <lens>` header. | ~150 (was ~243 + step) |
| **4. Hard rules** | Only invariants that must fire mid-reasoning: (1) no vendor/product naming, with the current-state carve-out — every lens gets the carve-out, today only operations has it; (2) no Confirmed without evidence, uncertain → Unknown or Assumed with declared basis; (3) cite what you opened, never a filename alone; (4) append-only, transitions carry `was <id>`; (5) stamp/price + local default `organizacional`; (6) expired reads as weak Assumed. | ~450 (was ~1,300) |
| **5. Signal catalog** | 6–8 universal tokens, no prose + one line: the invocation may carry pack cues; cues, not a checklist. | ~200 (was ~382 incl. leakage) |
| **6. Execution steps** | Five steps: (1) understand the relevant evidence — with the risk-based raw-verification sentence (§5); (2) **apply the perspective** — the lens-specific reasoning move, the only step that differs materially between lenses; (3) probe material gaps and contradictions, including cross-lens tensions to hand downstream; (4) contribute findings — SU rows + the narrative block; (5) expose uncertainty rather than manufacture certainty. | ~600 (was ~2,170) |

Step 2, per lens — the content worth keeping and expanding, extracted from today's files:

| Lens | Signature reasoning move |
|---|---|
| business | declared vs actual impact and urgency; who senses it; shadow stakeholders and veto-holders |
| operations | reconstruct one real instance end to end; exceptions, waits, rework, tribal knowledge |
| user | distinct populations and their contexts; hand the offline/sensitivity tension to data + governance |
| data | entities and owners; sensitivity and quality; record the sensitivity clearly so governance can adjudicate |
| governance | **conflict scan** — earlier lenses' stated needs against policy; collisions become Conflicted rows, never silently resolved |
| financial | as-is cost envelope from volume × cycle time × loaded rate, declared as Assumed with the basis; cost of doing nothing |
| technology | cross the pack's decision tree against the SU; constraint verdicts pass/risky/blocker; reversibility and effort band |

`lens-technology` keeps `## Phase gate` (its only genuine activation invariant) and its direct pack reads.

**`LENS_AUTHORING.md` compatibility.** The six sections and their order are unchanged, so the guide stays structurally valid. Three edits are required, all corrections of statements the audit proved false or now stale: the pack-signal mechanism (§D5), hard rule 5 ("open every file in `inputs/`" → shared extraction as the normal surface + the citation invariant + materiality-based verification), and audit checklist item 4.

---

## 8. Persona target contract

Indicative size ~1,100 chars per agent (from ~3,200) — a lightweight heuristic, not a gate, on the same terms as §7. Persona = independent perspective + mandate.

```markdown
---
name: <persona>
description: <one line — lens, phases, returns to chairman, does not write>
tools: [Read, Grep, Glob]
---

# <Persona>

## Identity
<the independent voice — including the council-mode stance the lens Role does not
carry, e.g. "sceptical of declared impact". This section may grow.>

## Lens binding
You are the council voice of `lens-<x>`. You do not need to read its SKILL.md —
the invocation carries the rules that bind you.

## Mandate per phase
- **Framing**: <…>
- **Options**: <…>
- **Decision**: <…>

## Memory consulted
`.claude/agent-memory/_universal/<persona>/*.md` (incl. `diary.md` — cite a prior
pattern by domain, never by client name) · `_tenant/<tenant>/<persona>/*.md`
```

Owned elsewhere: execution mechanics → council preamble (§6.4); return schema → `chairman-synthesis`; state/vendor rules → the two lines in the preamble; domain knowledge → `pack.yaml` + `domain-knowledge/` (only `solution-architect` reads them, unchanged).

Lens and persona stay the same perspective, expressed twice for two modes — not runtime copies. Nothing requires a persona to re-read its lens file. (Gate E: NO.)

---

## 9. PP cleanup deferred work

Not touched now. Expected after the runtime is stable (Phase G).

| Target | Expected work | Trigger |
|---|---|---|
| `pack.yaml → lenses_config.*.extra_signals` | 89 signals across 6 lenses (data 20, governance 20, user 15, operations 14, business 12, financial 8). Once injected as an attention-cue string, 20 cues per lens is a list nobody reads. Trim target: **preferably 5–8 per Discovery lens**. **Survival test: a pack signal survives only if removing it would materially reduce the lens's ability to notice a domain-specific issue. Research support alone is NOT sufficient reason for a signal to consume runtime context.** Signals remain attention cues, never coverage requirements. The `# DC-D-NNN` trace comments stay in the manifest (authoring evidence, never injected — the orchestrator injects tokens only). | after Phase D proves injection works and the injected block's size is observable |
| `question-bank.md` | 506 lines, `Q-<LENS>-NN` core + `P-<LENS>-NN` probes. Once `/status` is the single consumer, verify probe triggers are stated in a form the SU can actually satisfy ("fires when X observed"), and that the file is readable in one pass at that step. Its `## Discipline` section is already correctly shaped — keep. | after Phase D |
| `glossary.md` | Inspect only. No runtime change touches it; edit only if the signal trim orphans a term. | after the signal trim |

Not in scope, now or later: reintroducing canonical `DC-D` / `AP-D` / `PS` research ids into runtime context. They live in `pack.yaml` comments and `question-bank.md` `Research basis:` lines — authoring-side, greppable by humans, never injected.

---

## 10. Compatibility impact

| Surface | Impact |
|---|---|
| **Existing engagements** (`cae-automation`, `dpt-galp-jp`, `kam-onboarding`, `pricing-marinha`) | None required. Nothing is rewritten or migrated. |
| **`_state.json`** | Unchanged — no new keys, no schema change. |
| **Existing `shared-understanding.md`** | Unchanged. D9 fixes the *scaffold* for new engagements only. `pricing-marinha` already carries `custo`/`swing`; `dashboard.py` maps columns by header name and infers absent ones (`custo_inferred`/`swing_inferred`), and `states.md` already states the on-read compatibility rule. No migration. |
| **Existing `lens-outputs/*.md`** | Unchanged. The new shape applies to rounds run after the change; consumers (`aisa-synthesize`, `aisa-blueprint`, `aisa-decide`, `aisa-simulate`, `aisa-retro`, `aisa-frame`/`aisa-options` excerpt composition) read prose either way. `pre-lens-order-check.py` needs the round id in the file — the new header provides it, old files keep theirs. |
| **`_capture/`** | Additive. New `*.text.md` + `evidence-index.md`; existing `*.extraction.json` / `*.replay.md` / `process-model.md` untouched. An engagement with no `_capture/` gets an index on its next `/capture` or `/round`. |
| **Pack manifests** | No schema change. `extra_signals` and `question_bank` acquire resolvers; both keys already exist and are already declared by `pp`. Other packs (scaffolds) with no `lenses_config.<lens>` inject nothing. |
| **Commands** | No command signature changes. No new command. `/capture` covers more formats; `/status` phrases better. |

No migration machinery. Additive changes plus text edits.

---

## 11. Ordered implementation sequence + PASS conditions

| Phase | Work | PASS condition |
|---|---|---|
| **A — contracts** | `orchestration.md` becomes the single owner of evidence reading + council mechanics. Correct `LENS_AUTHORING.md` (pack-signal mechanism, hard rule 5, checklist item 4). Align `ARCHITECTURE.md` §4.1/§7.2/§3.4 and `PACK_AUTHORING.md`. | `grep -c "open and PARSE every file"` in `library/kernel/` = 1 · `LENS_AUTHORING.md` no longer claims lenses read pack metadata · `/status --check` green |
| **B — shared evidence** | `text_extract.py` + `aisa-capture` text tier + `evidence-index.md`. | `python library/kernel/tools/text_extract.py` on all 5 `pricing-marinha` inputs → 2 docx + 2 vtt extracted with provenance markers, xlsx untouched; a deliberately corrupt file yields `status: failed`, not a crash · `evidence-index.md` lists all 5 with correct status · re-run on unchanged input is a cache hit · **the one new test**: a fixture per format asserting locator format and byte-identical output across two runs |
| **C — lenses** | Rewrite the 7 lens files to §7. | `grep -in "pp pack additions\|excel_anchors\|sharepoint\|DLP_policies\|sensitivity_labels"` across `.claude/skills/lens-{business,operations,user,data,governance,financial}` = 0 hits · no per-signal coverage loop in any lens · all 4+2 hard rules present in all 7 · the 6 sections in order · `/round business` on a fixture writes SU rows + the 3-heading block, and `pre-lens-order-check` still blocks an out-of-order lens. *(Size is reported for review, never asserted — §7.)* |
| **D — orchestrator** | `aisa-round` step 3.6 + invocation payload; `aisa-status` step 6 question-bank consult; council preamble authored. | a `/round` on `pricing-marinha` shows pack cues in the lens invocation and no per-lens `inputs/` enumeration · `grep -rn "question_bank" .claude/` returns exactly one skill · `/status` agenda items read as askable questions and cite no product name |
| **E — personas** | Trim the 7 agent files; wire the preamble into `aisa-frame`/`aisa-options`; `chairman-synthesis` documents the schema. | `grep -rn "SKILL.md" .claude/agents/` = 7 pointer lines, none instructing a read · `grep -c "### Headline"` in `.claude/agents/` = 0, and the schema appears once per council orchestrator · `/frame` on a fixture → `phase-completeness.py` reports 8/8 council + 6/6 `_council-prep`. *(Size is reported for review, never asserted — §8.)* |
| **F — state scaffold** | `aisa-start` SU `## Unknown` columns (+ `_capture/` in the scaffold listing). | `/start <fixture>` produces a `## Unknown` header with `custo` + `swing` · `dashboard.py --engagement <fixture>` builds with `flavour = v2.3` · the 4 existing engagements still build |
| **G — PP cleanup** | Trim `extra_signals` to preferably 5–8 per Discovery lens against the survival test (§9); verify `question-bank.md` probe triggers; inspect `glossary.md`. | every retained signal passes the survival test and keeps its `# DC-D-NNN` trace · every probe states an SU-observable trigger · no runtime file changed in this phase |

Order is dependency-forced: A before C (lenses point at the centralized text), B before C (the `Inputs` line promises an index that must exist), D after C (nothing to inject into until the lens has the cue line), E after D (the preamble must exist before the persona files lose their copies). F and G are independent; G last by definition.

---

## 12. Risks

| # | Risk | Likelihood | Mitigation |
|---|---|---|---|
| 1 | **A pointer is a rule not applied.** A lens told that stamping semantics live in `states.md` writes an unstamped row. | Medium | The two local lines carry the *obligation* and the default (`organizacional`, never blank) — only the tables are remote. Detectable: `dashboard.py` already flags `custo_inferred`/`swing_inferred`. If it recurs, the D3 option (c) escalation is a hook, not more lens text. |
| 2 | **Injection re-creates the checklist.** A 20-cue injected block reads as coverage even with the loop deleted. | **High** | Two guards: the trailing clause "*uncovered cues are not gaps*" is mandatory in the injected string, and Phase G trims the count. This is the single most likely way the simplification is undone. |
| 3 | **Extraction loses what the lens needed.** A VTT merge or PDF layout collapse drops the detail that mattered. | Medium | Loss-minimizing, not summarizing: everything is kept, only marked. Raw sources stay openable and authoritative on conflict, and "extraction may have lost relevant detail" is itself one of the §5 triggers for inspecting the raw source. |
| 4 | **Trimmed persona under-performs** because the preamble is thinner than the file it replaced. | Medium | Identity + Mandate — the 40% the audit measured as the useful part — is kept and may grow. Verify by running `/frame` on `pricing-marinha` and diffing the chairman synthesis against `chairman-synthesis-F-02.md`. |
| 5 | **Lens-output shape breaks the order hook.** `pre-lens-order-check.py` greps the in-progress round string inside `lens-outputs/<lens>.md`. | Low | The `## <round> — <lens>` header is a Phase C PASS assertion. |
| 6 | **The technology exception is copied into a Discovery lens** by later drift ("lens-technology reads the pack, why not this one"). | Low | `LENS_AUTHORING.md` states the distinction explicitly (§2/D5); the Phase C grep catches a pack block reappearing in any Discovery lens. |
| 7 | **Six lens files rewritten in one pass** — the largest behavioural surface in the plan. | Medium | Phase C runs on a fixture before touching a live engagement; existing SUs are append-only, so a bad round adds rows rather than corrupting prior ones. |
| 8 | **Two question-bank consumers appear later** and drift. | Low | Single-consumer stated as a design constraint, asserted by the Phase D grep. |

---

## 13. Anti-complexity gate

| | Question | Verdict | Basis |
|---|---|---|---|
| A | New state machine? | **NO** | 5 states unchanged; transitions unchanged; no new phase, no new mode. `states.md` needs no edit. |
| B | New evidence taxonomy? | **NO** | No new id namespace. `PM-NNN` stays xlsx-only; text locators are plain strings in the existing `evidência` column. `evidence-index.md` is a file listing, not a classification. |
| C | Routing engine? | **NO** | The orchestrator resolves a manifest key and hands over an index. Which raw source a lens opens is the lens's judgement, stated in one sentence. |
| D | Discovery lenses must understand pack structure? | **NO** | The 6 Discovery lenses never read `pack.yaml`; cues arrive as a token list. `lens-technology` is Options-only and pack-aware by design — the accepted exception (§2/D5). |
| E | Personas duplicate lens execution? | **NO** | Persona = identity + mandate. No persona reads a lens file; mechanics are stated once in the invocation. |
| F | Question bank as permanent context? | **NO** | One consumer, one step: `aisa-status` step 6. Zero lens/persona/council loads. |
| G | Evidence summarized before lens reasoning? | **NO** | Capture-lite is deterministic extraction with provenance. No LLM in the text path; the L2 process model stays xlsx-only, and its claims are verified against raw source when material to confidence (§5). |
| H | Framework context smaller? | **YES** | −40,600 chars static (−37%); −67% per Discovery round, −79% per council round (§4). |
| I | Engagement evidence more prominent? | **YES** | Framework text per Discovery round falls ~3×; raw-input parsing goes from 6–7× to 1× per round, and what a lens reads is an extraction with locators rather than the same bytes re-parsed. |

**Net text check.** Removals (~46.3k) exceed additions (~5.7k) by roughly 8:1. The plan does not add more framework text than it removes.

---

RUNTIME SIMPLIFICATION PLAN COMPLETE: YES
D1-D9 FULLY MAPPED: YES
PLAN REVIEW CHANGES APPLIED: YES
NEW STATE MACHINE INTRODUCED: NO
NEW EVIDENCE TAXONOMY INTRODUCED: NO
NEW ROUTING ENGINE INTRODUCED: NO
DISCOVERY LENSES REMAIN PACK-AGNOSTIC: YES
TECHNOLOGY LENS PACK-AWARE IN OPTIONS: YES
MANDATORY RAW SPOT-CHECK QUOTA REMOVED: YES
RAW VERIFICATION REMAINS MATERIALITY-BASED: YES
SIZE LIMITS ARE SOFT GUARDRAILS: YES
LIGHT FRAMEWORK ≠ LIGHTWEIGHT REASONING: EXPLICIT (§1.1)
PP EXTRA SIGNAL TARGET: preferably 5–8 per Discovery lens
QUESTION BANK PERMANENT LENS CONTEXT: NO
COUNCIL PERSONAS REQUIRE FULL LENS RE-READ: NO
CAPTURE PERFORMS SEMANTIC SUMMARIZATION: NO
EXPECTED FRAMEWORK CONTEXT AFTER CHANGE: SMALLER
PP PACK MODIFIED: NO
RUNTIME FILES MODIFIED: NO
READY FOR PHASE A — CONTRACTS: YES
