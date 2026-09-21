# Lens Contract Audit — kernel/runtime architecture

<!--
provenance: AUDIT (read-only; no files modified)
scope: kernel lens contract + persona agents + PP runtime boundary
authored: 2026-09-03
path note: written to the repo's actual `research/pp/authoring/` directory
  (`docs/pp-pack-authoring/research/pp/authoring/`), alongside
  `pp-pack-authoring-map.md` and `step-2-discovery-layer-report.md`.
  No root-level `research/` exists; creating one would fragment the workstream.
-->

**Question asked:** what in the lens architecture is essential contract, useful perspective, duplication, or runtime ceremony.
**Method:** full read of `docs/LENS_AUTHORING.md`, all 7 `lens-*/SKILL.md`, `library/kernel/{phases,states,orchestration,glossary}.md`, `.claude/rules/*`, all 8 `.claude/agents/*.md`, `aisa-round` / `aisa-frame` / `aisa-start`, `.claude/hooks/HOOKS.md` + `settings.json`, `library/packs/pp/{pack.yaml,question-bank.md}`, plus byte-level duplication measurement across the lens set.

---

## 1. Executive finding

**The lens contract is sound. The lens *files* are 3–4× larger than the contract requires, and the surplus is framework mechanics.**

Measured across the 7 lens files (42,849 chars total):

| Content class | Share | Verdict |
|---|---|---|
| Perspective / reasoning (Role + universal signals + lens-specific reasoning steps) | **~23%** | keep, expand |
| Framework mechanics (write protocol, stamping, id allocation, log appends) | **~52%** | centralize |
| Byte-identical lines repeated in ≥4 lenses | **42%** (18,004 chars) | centralize |
| Engagement evidence | **0%** in the lens file (all of it arrives at runtime) | correct |
| Pack/domain knowledge hardcoded in kernel lenses | ~6% (and **stale**) | remove |

Three findings are structural, not cosmetic:

1. **`LENS_AUTHORING.md` documents a mechanism that does not exist.** It states that a pack-specific signal added to `pack.yaml → lenses_config.<lens>.extra_signals` is picked up "at runtime via the pack metadata". **No Discovery lens reads `pack.yaml`.** All six hardcode a literal `pp pack additions:` line. Only `lens-technology` actually reads the manifest. The six hardcoded lists are now out of sync with `pack.yaml` v1.3.0 (governance lens lists 4 signals; `pack.yaml` declares 20 different ones).
2. **`question-bank.md` (506 lines, authored in Step 2) has zero runtime consumers.** `grep -rn "question.bank\|question_bank" .claude/` returns nothing. No lens, agent, skill or hook references it. It exists in `pack.yaml` as a declared key that nothing resolves.
3. **The costliest instruction in the system is a single line repeated 13 times** ("open every file in `inputs/`"): six Discovery lenses, seven council agents, once per round.

The framework-vs-engagement ratio is the answer to the brief's core question: **yes, Claude currently spends more attention learning how to be aisa than understanding the engagement** — roughly 3:1 in the lens files themselves, before any engagement byte is read.

---

## 2. Current Lens Contract (as built)

Six sections, mandated by `docs/LENS_AUTHORING.md` and mirrored in `docs/ARCHITECTURE.md §7.2`. Measured average size per lens:

| # | Section | Avg chars | Share | What it actually contains today |
|---|---|---|---|---|
| 1 | Role | 525 | 8.6% | Persona stance + 4 framing questions. **Pure perspective.** |
| 2 | Inputs (always read) | 1,176 | 19.2% | 7 bullets; 5 identical across lenses; the `inputs/` + `_capture/` bullets alone are 620 chars |
| 3 | Outputs (always write) | 243 | 4.0% | 2 bullets; identical except the lens name |
| 4 | Hard rules | 1,300 | 21.2% | 7–8 rules; rules 5/6/7 byte-identical in all 7 lenses |
| 5 | Signal catalog | 382 | 6.2% | Universal list (cue) + hardcoded pack list (leakage) |
| 6 | Execution steps | 2,170 | 35.5% | 7–8 steps; step 1 + step 1.5 (a–d) byte-identical in 6 lenses = ~1,400 chars each |

Not in the contract but present: `lens-technology` adds a **Phase gate** section (246 chars). It is the only lens with a genuine activation invariant, and the only lens where that section earns its place.

---

## 3. Per-lens complexity table

Classification: **A** essential contract · **B** perspective · **C** duplicated · **D** procedural overhead · **E** domain leakage.

| Lens | Total | B (perspective) | C+D (mechanics) | E (leakage) | Notes |
|---|---|---|---|---|---|
| `lens-business` | 6,135 | Role 426 + universal signals ~200 + steps 2–4 ~500 ≈ **1,130 (18%)** | ~4,750 | `pp pack additions` 250 chars, **stale** vs `pack.yaml` (lens says `licensing_baseline / integration_licensing_exposure / sponsor_authority_level`; pack declares 12 different `DC-D`-traced signals) | Only lens whose step 1 still says "from `_state.json`" — a wording drift |
| `lens-operations` | 5,960 | Role 547 (strongest stance in the set) + signals ~250 + steps 2–4 ~450 ≈ **1,250 (21%)** | ~4,540 | `excel_anchors`, `sharepoint_lists_anchors` — **Microsoft-product vocabulary in a Discovery lens**; already flagged in `GAP_ANALYSIS.md:152` | Hard rule 1 correctly carries the current-state carve-out; other lenses do not |
| `lens-user` | 5,821 | Role 483 + signals ~200 + steps 2–4 ~400 ≈ **1,080 (19%)** | ~4,500 | `personas_count`, `mobile_need`, `offline_need` — neutral, but stale vs `pack.yaml` (15 signals) | Step 4's "surface the tension for governance/data" is real cross-lens value, not ceremony |
| `lens-data` | 6,256 | Role 459 + signals ~250 + steps 2–4 ~600 ≈ **1,310 (21%)** | ~4,700 | `structured_vs_document_storage_today` (neutral, well-phrased), `master_data_owners`, `retention_policy` — stale vs 20 pack signals | Longest Inputs block (1,348) — adds a spreadsheet-profiling clause |
| `lens-governance` | 6,272 | Role 495 + signals ~250 + steps 3 ~700 ≈ **1,445 (23%)** | ~4,500 | `DLP_policies`, `environment_strategy`, `sensitivity_labels`, `RBAC_complexity` — **three are Microsoft platform terms**; stale vs 20 pack signals | Step 3 (conflict scan) is the single highest-value execution step in the whole set — it is genuine adjudication, not ceremony |
| `lens-financial` | 5,859 | Role 478 + signals ~180 + steps 2–3 ~400 ≈ **1,060 (18%)** | ~4,540 | `licensing_cost_baseline`, `internal_chargeback_model` — stale vs 8 pack signals | Step 2 (as-is envelope formula) is real method |
| `lens-technology` | 6,546 | Role 785 + 5 option questions + steps 3–4 ~800 ≈ **1,700 (26%)** | ~4,200 | **Signal catalog inlines the 5 `pp` constraints verbatim** while also telling the lens to read them from `pack.yaml` — duplication of the manifest, not leakage of the knowledge base | Phase gate (A, essential). Correctly points at `domain-knowledge/*.md` rather than inlining it — the knowledge-base risk is currently avoided |

**Every Discovery lens contains pack-specific knowledge (E). Every such block is stale. Three contain vendor vocabulary the no-tech rule exists to prevent.**

---

## 4. Cross-lens duplication

Byte-identical lines appearing in ≥4 lens files, measured:

| Repeated content | Lenses | Chars/copy | Runtime value | Must stay local? | Owner if centralized |
|---|---|---|---|---|---|
| Execution step 1.5 a–d (process-capture protocol) | 6 | ~1,200 | Medium — the spot-check rule is a real epistemic guard | **No** | `orchestration.md` → *Reading input documents*; orchestrator states it once per round |
| Hard rules 5/6/7 (stamp `verificado_em`/`validade`; price `custo`/`swing`; expired = weak) | 6–7 | ~1,000 | **High** — these govern what the lens writes | **Partially** — see D3 | `states.md` owns the semantics; lens keeps a 1-line pointer + the "in doubt: organizacional" default |
| Inputs bullets: `context.json`, `shared-understanding.md`, `lens-outputs/*.md`, `<engagement>` resolution | 6 | ~380 | Low — orchestrator already supplies these | **No** | `aisa-round` / kernel preamble |
| `inputs/` "open and PARSE every file" bullet | 5–7 | ~370 | **High value, highest cost** — see §5 | **No** | Orchestrator (decision D1) |
| `_capture/process-model.md` read-FIRST bullet | 5 | ~250 | Medium | **No** | Orchestrator |
| Execution step 1 (round + next free id + expired-row scan) | 6 | ~290 | Low — id allocation is bookkeeping | **No** | Orchestrator computes round + id base and passes it in |
| Hard rule 4 (append-only, `was X-NNN`) | 7 | ~90 | **High** — but a pointer suffices | Pointer only | `states.md` |
| Hard rule 2 (no Confirmed without evidence) | 7 | ~95 | **High** — this is the epistemic core | **Yes, verbatim** | Local |
| Hard rule 3 (identify in `lens` column) | 7 | ~70 | Medium | Yes (one clause) | Local |
| Hard rule 1 (no vendor naming) | 6 | ~180 | **High** — the defining Discovery invariant | **Yes** | Local + `.claude/rules/` |
| Execution step 3 pattern ("for each signal not covered → Confirmed/Assumed/Unknown/Conflicted") | 6 | ~280 | **Low** — restates `states.md` decision rules as a loop | **No** | `states.md` |
| Final step "append to `council-log.md`" | 7 | ~75 | Low — bookkeeping | **No** | `aisa-round` |

**Total identical-line duplication: 18,004 chars of 42,849 (42%).** Near-identical rewordings (hard rules 1–4, Outputs, Role framing) are excluded from that count and push the effective figure past 50%.

The pattern: **everything repeated is framework knowledge; nothing repeated is perspective.** Duplication and perspective are cleanly separable here, which is what makes the simplification tractable.

---

## 5. Input-loading analysis

### The rule as written

`LENS_AUTHORING.md` hard rule 5 + each lens's Inputs section + `aisa-frame` step 5's persona prompt: **every lens, and every council agent, opens and parses every file in `inputs/`.**

### Measured runtime implication

`projects/pricing-marinha/inputs/`:

| File | Size | Captured? |
|---|---|---|
| `PREÇO BANCAS_30_01_26.xlsx` | 1,378 KB | **Yes** → `process-model.md` (40.6 KB) + `replay.md` (51 KB) |
| `Fluxograma do Processo Atual…docx` | 41 KB | No |
| `Inputs, cálculos e outputs…docx` | 43 KB | No |
| `Pricing Marinha _ Kick-off.vtt` | 210 KB | No |
| `Processos Pricing…Gravação…vtt` | 86 KB | No |

Per Discovery round: **6 lenses × (92 KB of capture artefacts + ~380 KB of unparsed docx/VTT)**. The two meeting transcripts alone are ~296 KB (~75k tokens) that no capture layer covers — `aisa-capture` handles `.xlsx`/`.xlsm` only. Every lens is instructed to read them from scratch, every round.

Council mode is worse, not better: `aisa-frame` step 5 hands each of 6 parallel personas a *curated thematic SU excerpt* (correct — that is centralization working) and then tells each one to read **every file under `inputs/`** anyway, plus **its own lens `SKILL.md`**. So the council pays: 6× full inputs + 6× lens file + 6× agent file, in exchange for a curated 1× SU excerpt.

### Classification: **CENTRALIZE CANDIDATE**

Not REMOVE. The rule exists for a real reason — `orchestration.md` and the hard rule both target the failure mode of citing a filename without opening it, and `_capture/` exists precisely because that failure was observed. The evidence discipline is correct.

But the rule conflates two things:
- **"Evidence must be opened before it is cited"** — an epistemic invariant. Keep, verbatim, in every lens.
- **"Each lens independently parses every byte"** — an implementation of that invariant, and the expensive one.

The capture layer already proves the alternative works for spreadsheets: parse once deterministically, hand every lens a dense model with cell-level citations, require a spot-check against the raw file. That pattern is not applied to docx/pdf/vtt, which is where most of the un-deduplicated bytes now sit.

**KEEP** — the citation invariant, and the ≥1 spot-check per round against raw source.
**CENTRALIZE** — the parsing. One pass per input per round, shared.
**REMOVE** — nothing. No part of this rule is pure ceremony.

Blocking question for §11 (D1/D2).

---

## 6. Signal architecture analysis

### Are signals cues or checklists?

**Both, and the split is clean.**

- **The universal signal lists are cues.** 6–8 short tokens per lens (`shadow_stakeholders`, `tribal_knowledge`, `atomicity_span`). They cost ~200 chars and prime attention. This is the correct shape.
- **Execution step 3 turns them into a checklist.** Every Discovery lens contains: *"For each signal not yet covered: evidence exists → Confirmed…"*. That converts a list of things to notice into a coverage obligation to discharge. A lens working through the list mechanically will emit an Unknown per uncovered token rather than reasoning about what this engagement actually lacks. The rot is in step 3, not in the catalog.

This is why the honest answer to the final flag is **NO**: as authored, signals do not function *primarily* as attention cues — the execution contract makes them a checklist. The fix is one deleted loop, not a rewritten catalog.

### Placement violations

`LENS_AUTHORING.md` §"Modifying an existing lens" is explicit: *"Adding a pack-specific signal — do not touch the lens."*

| Lens | Hardcoded `pp pack additions` | Matches `pack.yaml` v1.3.0? | Vendor-neutral? |
|---|---|---|---|
| business | 3 signals | **No** (pack: 12, none matching) | Yes |
| operations | 3 signals | **No** (pack: 14) | **No** — `excel_anchors`, `sharepoint_lists_anchors` |
| user | 3 signals | **No** (pack: 15) | Yes |
| data | 3 signals | **No** (pack: 20) | Yes (`structured_vs_document_storage_today` is a good rewrite) |
| governance | 4 signals | **No** (pack: 20) | **No** — `DLP_policies`, `environment_strategy`, `sensitivity_labels` |
| financial | 2 signals | **No** (pack: 8) | Yes |
| technology | 5 constraints inlined verbatim | Yes — but duplicated from the file it is told to read | n/a (allowed) |

**Seven violations of a rule the authoring guide states in one sentence.** The cause is not carelessness: there is no mechanism to honour it. The lens has no instruction to read `pack.yaml`, so the only way to make a pack signal visible was to write it into the lens. Step 2 of PP pack authoring correctly wrote 89 traced signals into `pack.yaml` — and nothing in the runtime can see them.

This is the single highest-value correction in the audit: it is small, it is mechanical, and until it is made, the PP Discovery layer authored in Step 2 is inert.

---

## 7. Persona-agent analysis

Seven lens-bound agents, 65 lines each, structurally identical. Diffed against `business-analyst.md`:

| Section | Chars | Class | Assessment |
|---|---|---|---|
| Identity | ~350 | **B — perspective** | Genuinely independent voice. Near-restatement of the lens Role, but the *council-mode* stance ("sceptical of declared impact") is not fully in the lens |
| Lens binding | ~200 | **C — duplicated** | Says "all hard rules of that lens apply here verbatim", then re-states one of them. Meanwhile `aisa-frame` separately tells the agent to *read* the lens file. Restated **and** re-read |
| Mode (council-independent) | ~600 | **C + F (orchestration mechanics)** | "you do not write", "you do not read others' in-flight outputs", "read every file in inputs/". Identical in all 7. Belongs in the launch prompt (which already carries most of it) or `orchestration.md` |
| Memory consulted | ~300 | **A — essential**, but path-only | Only the persona name varies. Could be one templated line |
| Mandate per phase | ~450 | **B — perspective, highest value** | Framing / Options / Decision, three lines each, materially different per persona. **The most useful content in the agent files, and the smallest** |
| Output format (schema) | ~900 | **C — duplicated 7×** | Byte-identical Headline / Evidence anchors / Proposal / Open questions / Conflicts / Risks block, plus "if empty write `(none)`". The chairman is the consumer; the schema is the chairman's contract |

**~60% of each agent file is framework. ~40% is perspective, concentrated in Identity + Mandate.**

Applying *agent = independent perspective + mandate*: the useful content of a persona agent is **~800 chars**, currently delivered in ~2,600. And the council round pays this seven times in parallel, alongside seven full lens-file reads.

No agent contains domain knowledge — clean on that axis. `solution-architect` correctly defers vendor knowledge to `pack.yaml` + `domain-knowledge/`, and its `agent-memory/_universal/solution-architect/universal-constraints.md` is the one place that reads `lenses_config.technology.constraints_to_check` as intended.

`chairman.md` (133 lines) is out of scope as a lens-bound persona but is where the duplicated output schema should live.

---

## 8. PP / kernel boundary

Intended separation vs. built:

```
Kernel lens → universal perspective/signals     ✓ present   ✗ polluted (7 hardcoded pack blocks)
PP pack    → pack-specific extra signals         ✓ authored  ✗ never loaded by any Discovery lens
Question bank → optional probing resource        ✓ authored  ✗ zero runtime consumers
Domain knowledge → selectively consulted later   ✓ correct   ✓ pointer-only, Options-gated
```

Three violations:

1. **Downward leak (pack → kernel).** All 6 Discovery lenses hardcode pack signals. Three carry Microsoft vocabulary into Discovery, contradicting `.claude/rules/no-tech-mention-before-options.md` from inside the kernel itself.
2. **Broken edge (pack → runtime).** `pack.yaml.lenses_config.*.extra_signals` — 89 signals, each traced to a canonical `DC-D` id — is read by nothing. The join documented in `pp-pack-authoring-map.md §8` (grep an id, find signal + question + evidence) works for a human reading the repo, not for the runtime.
3. **Orphaned resource.** `question-bank.md` is declared (`question_bank: question-bank.md`) and never resolved. Its own §Discipline is well-designed for lens use ("a question source, not an interview script"; core vs trigger-fired probes) — exactly the shape a lens should consult selectively. Nothing consults it.

The boundary that *is* correct and worth preserving as the model: **`lens-technology` → `domain-knowledge/*.md` by pointer, gated on `phase ∈ {options, decision}`.** The knowledge base is named, not inlined. Discovery should use the same discipline for `pack.yaml`.

**Adjacent contract drift found while tracing the SU write path** (not lens-caused, but it breaks the lens hard rules): `aisa-start`'s `shared-understanding.md` skeleton writes `## Unknown` with columns `id | lens | pergunta | quem responde | criticidade | ronda`. `states.md` §Schema and every lens's hard rule 6 require `custo` and `swing`. New engagements are scaffolded with a table that cannot hold what the lenses are mandated to stamp.

---

## 9. Context-efficiency assessment

Where lens runtime context goes, per Discovery round (qualitative, `pricing-marinha` shape):

| Class | Where | Assessment |
|---|---|---|
| **Framework mechanics** | ~52% of the lens file, ×6 lenses | The dominant cost before any evidence is read |
| **Duplicated instructions** | 42% byte-identical across lenses, paid 6× | Pure waste — Claude re-learns the same protocol six times per round |
| **Perspective / reasoning** | ~23% of the lens file | The only content that differentiates the lenses; the smallest slice |
| **Engagement evidence** | ~470 KB of `inputs/` + `_capture/`, re-read per lens | The one thing that *should* dominate, and it is read 6× because it is not centralized |
| **Domain knowledge** | ~6% (stale pack blocks) in Discovery; pointer-only in `lens-technology` | Wrong in Discovery, right in Options |

**Answer to the brief's core question: yes.** Roughly three-quarters of what a lens reads about itself is how-to-be-aisa, and the framework instructions are paid once per lens rather than once per round. The engagement evidence — the only irreplaceable input — is simultaneously the least deduplicated.

Order-of-magnitude effect of centralizing framework text alone (no behaviour change): ~18k chars × 5 redundant copies ≈ **90k chars of instruction removed per Discovery round**, before touching the input-parsing question, which is larger still.

---

## 10. Minimum viable Lens Contract

Six sections preserved. Target: **~1,400 chars per lens** (from ~6,100), with perspective content *growing* in absolute terms.

### 1. Role
- **Purpose:** create a distinct, non-substitutable stance.
- **Must remain:** the persona sentence + the 3–4 questions it sees every request through. Where the operations lens says it *distrusts the documented process*, keep that — it is the lens.
- **Centralize/remove:** nothing. This section is currently correct and is the only section that should get longer.

### 2. Inputs
- **Purpose:** name the evidence this lens privileges — not enumerate the filesystem.
- **Must remain:** one line saying what this lens reads *differently* (data lens profiles spreadsheets; technology lens needs the full SU, not a slice).
- **Centralize:** `context.json`, `shared-understanding.md`, `lens-outputs/*.md`, `<engagement>` resolution, `_capture/` read-first, agent-memory paths, format→tool mapping → orchestrator preamble + `orchestration.md`. The `inputs/` parsing rule is decision **D1**; the *citation* invariant moves to Hard rules.

### 3. Outputs
- **Purpose:** state the minimum the lens must know to contribute.
- **Must remain:** one line — SU rows tagged `lens=<name>`, plus a narrative to `lens-outputs/<name>.md`.
- **Centralize/remove:** the `council-log.md` append (orchestrator bookkeeping); the council-mode return-schema pointer (chairman's contract).

### 4. Hard rules
- **Purpose:** the invariants that must fire *while the lens is reasoning*, when consulting another file would be too late.
- **Must remain local (4 rules, ~400 chars):**
  1. No vendor/product naming (with the current-state carve-out) — the defining Discovery invariant.
  2. No Confirmed without evidence; uncertain → Unknown or Assumed with declared basis.
  3. Cite what you opened; never a filename alone.
  4. Append-only; transitions carry `was X-NNN`.
- **Centralize to `states.md` + one pointer line:** stamping mechanics (`verificado_em`/`validade` classes), question pricing (`custo`/`swing` vocabularies), expired-row handling. Keep the *defaults* local — "in doubt: `organizacional`" — because a default consulted elsewhere will not be applied.
- **Not weakened:** every invariant above survives; only the tables and enumerations move.

### 5. Signal catalog
- **Purpose:** attention cues. What this lens notices that others do not.
- **Must remain:** the universal list, 6–8 tokens, no prose.
- **Remove:** the hardcoded `pp pack additions` line from all seven lenses.
- **Centralize:** pack signals arrive from `pack.yaml → lenses_config.<lens>.extra_signals`, either read by the lens or injected by the orchestrator (decision **D5**). One line: *"the active pack adds signals via its `lenses_config`; treat them as cues, not a checklist."*

### 6. Execution steps
- **Purpose:** invoke the perspective. Nothing else.
- **Must remain (target 5 steps, ~500 chars), mapped to the brief's conceptual target:**
  1. Understand the evidence (what this lens looks at first).
  2. Apply the perspective — the lens-specific reasoning move (governance's conflict scan; financial's as-is envelope; operations' exception reconstruction; technology's decision-tree crossing). **This is the step worth writing and the only one that should differ materially between lenses.**
  3. Probe material gaps and contradictions — including cross-lens tensions to hand downstream.
  4. Contribute findings as SU rows + narrative.
  5. Expose uncertainty rather than inventing certainty.
- **Remove as ceremony:** step 1's round/next-free-id bookkeeping (orchestrator supplies), step 1.5 a–d verbatim capture protocol (orchestrator states once), step 3's per-signal Confirmed/Assumed/Unknown loop (restates `states.md`, and converts cues into a checklist), the final `council-log.md` append.
- **Keep as method, not ceremony:** the ≥1 spot-check of a `PM-NNN` claim against raw source. It is one sentence and it is the guard that keeps the capture layer honest.

### Persona agents (same principle)
Identity + Mandate-per-phase + memory path. Lens binding as a one-line pointer. Mode block → launch prompt. Output schema → `chairman-synthesis`'s contract, referenced once. Target ~800 chars from ~2,600.

---

## 11. Architecture decisions requiring human choice

None of these are silently chosen in this audit.

| # | Decision | Options | What hangs on it |
|---|---|---|---|
| **D1** | **Every lens reads every `inputs/` file** | (a) keep as-is; (b) orchestrator parses once per round, hands lenses a shared evidence digest + raw access for spot-checks; (c) hybrid — shared digest, lens re-reads only files its perspective privileges | Largest single runtime cost. (b)/(c) require defining what a "digest" preserves so the no-citation-without-opening invariant survives |
| **D2** | **Capture covers `.xlsx`/`.xlsm` only** | (a) accept 6× re-parse for docx/pdf/vtt; (b) extend `aisa-capture` to transcripts and documents; (c) capture-lite: one deterministic text extraction per input, no process model | Depends on D1. `pricing-marinha`'s ~296 KB of meeting transcripts are currently the most re-read bytes in the system |
| **D3** | **Epistemic stamping rules (`verificado_em`/`validade`/`custo`/`swing`) repeated in every lens** | (a) keep verbatim — the lens is the writer, and a rule read elsewhere may not be applied; (b) pointer + local defaults only; (c) move enforcement to a hook that rejects unstamped rows | (b) is ~1,000 chars saved per lens but trades a guarantee for a reference. (c) makes it structural — but CLAUDE.md principle 5 says only `library/` read-only is a hard gate |
| **D4** | **Append-only / `was X-NNN` repeated locally** | (a) keep one clause per lens; (b) pointer to `states.md` only | Low cost either way; needs an explicit call so it is not re-added by drift |
| **D5** | **Pack metadata loading in Discovery lenses** | (a) lens reads `pack.yaml` directly (mirrors `lens-technology`); (b) orchestrator resolves `lenses_config` and injects the signal list into the lens invocation; (c) keep hardcoded lists and maintain them by hand | Blocks the entire Step-2 PP Discovery layer from having any runtime effect. (b) keeps the lens pack-agnostic and is the only option that also fixes council mode |
| **D6** | **Lens narrative outputs (`lens-outputs/<lens>.md`)** | (a) keep; (b) shorten to a fixed 3-bullet form; (c) drop for a structured return | Consumed by `chairman-synthesis`, `dashboard.py`, `phase-completeness.py`, and `pre-lens-order-check.py` (which detects the round id inside the file). Dropping it breaks the lens-order hook |
| **D7** | **Persona/lens duplication** | (a) agent = identity + mandate, everything else by pointer; (b) agent stays self-contained because a subagent pays a file read either way; (c) generate agents from lenses at build time | Council rounds pay 7× lens file + 7× agent file today. (a) needs a decision on whether a subagent may be trusted to follow a pointer |
| **D8** | **`question-bank.md` has no runtime consumer** | (a) lenses consult it selectively during step 3 (probing); (b) `/status` uses it to build the meeting agenda from open Unknowns; (c) leave it as a human authoring resource and drop the `question_bank:` key's implied contract | 506 authored lines currently inert. (a) adds context cost to every lens; (b) adds it once, where questions are actually asked |
| **D9** | **SU skeleton drift** | Fix `aisa-start`'s `## Unknown` columns to include `custo`/`swing` | Mechanical, but it is a `library/`-adjacent runtime contract and lenses are currently mandated to write columns the scaffold does not create |

---

## 12. Recommended simplifications — NOT IMPLEMENTED

Ordered by value/risk. **No file was modified by this audit.**

**Tier 1 — mechanical, no architectural decision needed**

1. Delete the `pp pack additions:` line from all 6 Discovery lenses; replace with one pack-agnostic line. Removes 7 boundary violations and 3 vendor-vocabulary leaks in one edit. *(Depends on D5 for the replacement mechanism.)*
2. Delete `lens-technology`'s inlined 5-constraint list; it already reads them from `pack.yaml`.
3. Delete execution step 3's per-signal Confirmed/Assumed/Unknown loop from all 6 Discovery lenses. It restates `states.md` and is what turns signals into a checklist.
4. Delete the final `council-log.md` append step from all 7 lenses — `aisa-round` step 5c already does it.
5. Correct `LENS_AUTHORING.md` §"Modifying an existing lens": the claim that a lens "picks up pack signals at runtime via the pack metadata" is false for the 6 Discovery lenses.
6. Fix `aisa-start`'s SU `## Unknown` columns (D9).

**Tier 2 — after D3/D4**

7. Collapse hard rules 5/6/7 to one pointer line + the `organizacional` default. ~1,000 chars × 7.
8. Collapse hard rule 4 to one clause.

**Tier 3 — after D1/D2**

9. Move execution step 1.5 a–d (capture protocol) to `orchestration.md`; lenses keep the one-sentence spot-check obligation. ~1,200 chars × 6.
10. Move the Inputs section's shared bullets to an orchestrator preamble; each lens keeps one line on what it privileges. ~900 chars × 6.
11. Move round/next-free-id bookkeeping out of step 1 into the orchestrator.

**Tier 4 — after D7**

12. Reduce persona agents to Identity + Mandate + memory path; move the output schema into `chairman-synthesis`; move the mode block into the launch prompt (which already carries it).
13. Stop telling council personas to read their own `lens-*/SKILL.md` while also restating its rules in the agent file — pick one channel.

**Tier 5 — after D8**

14. Wire `question-bank.md` to whichever consumer is chosen, or retire the `question_bank:` key's implied runtime contract.

Projected effect of Tiers 1–3 alone: lens files from ~6,100 → ~1,400 chars each, with the Role and lens-specific reasoning steps *unchanged or expanded*. Every hard invariant survives; only its number of copies changes.

---

LENS CONTRACT AUDIT COMPLETE: YES
KERNEL LENSES CONTAIN PACK-SPECIFIC KNOWLEDGE: YES
SIGNALS FUNCTION PRIMARILY AS ATTENTION CUES: NO
MATERIAL CROSS-LENS DUPLICATION FOUND: YES
INPUT READING MODEL NEEDS ARCHITECTURE DECISION: YES
PERSONA/LENS MATERIAL DUPLICATION FOUND: YES
CURRENT LENS CONTRACT OVER-PROCEDURAL: YES
MINIMUM VIABLE LENS CONTRACT IDENTIFIED: YES
FILES MODIFIED: 0
READY FOR HUMAN SIMPLIFICATION DECISIONS: YES
