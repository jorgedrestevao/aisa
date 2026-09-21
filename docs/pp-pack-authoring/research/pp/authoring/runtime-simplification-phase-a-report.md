# Runtime Simplification — Phase A (Contracts) Report

<!--
provenance: CONTRACT CHANGE (documentation only)
scope: docs/LENS_AUTHORING.md, library/kernel/orchestration.md, docs/ARCHITECTURE.md, docs/PACK_AUTHORING.md
authored: 2026-09-03
basis: runtime-simplification-plan.md §11 Phase A + approved decisions D1–D9
path note: written to the repo's actual `research/pp/authoring/` directory
  (`docs/pp-pack-authoring/research/pp/authoring/`), alongside the plan it implements.
-->

## 1. Contracts changed

| File | Change |
|---|---|
| `library/kernel/orchestration.md` | *Reading input documents* rewritten as **Evidence contract — parse once, reason many** (shared-evidence surface, capture tiers incl. capture-lite as target model, raw-inspection format table, materiality-based verification, evidence-integrity invariant). New: **Orchestrator boundaries**, **Pack context — Discovery vs Options**, **Question bank — runtime role**. *Council-independent mode* gains the common-mechanics ownership statement + the persona boundary. Old section title kept as an explicit alias so 19 runtime pointers still resolve. |
| `docs/LENS_AUTHORING.md` | Six mandatory sections preserved in order, each given an explicit responsibility (Role / Inputs / Outputs / Hard rules / Signal catalog / Execution steps). Hard rule 5 ("Open every file in `inputs/`") replaced by the evidence-integrity rule; new hard rule 6 = stamp/price obligation + local default, semantics by pointer. New *Signals and pack context* block. Persona-authoring step and the "propagate hard rules to the persona file" line corrected. Audit checklist items 4/6/7 rewritten, items 8 + "not checked, by design" added. Three anti-patterns added. Size stated as a soft heuristic. |
| `docs/ARCHITECTURE.md` | §3.3 lens-output shape → the lightweight 3-heading block; §3.4 council-mechanics ownership + persona boundary; §4.1 `## Unknown` illustrative table gains `custo` + `swing` (D9 alignment, real vocabulary); §7.2 lens contract template rewritten to the target contract + pack boundary + soft size note; §7.3 agent contract rewritten to identity + mandate + "not here" ownership list; changelog entry **v3.2.0**, and the v3.1.0 spot-check bullet marked superseded. |
| `docs/PACK_AUTHORING.md` | `extra_signals` reach lenses by **orchestrator injection** (never copied into a lens file), are cues not checklist items, with the soft 5–8 heuristic + survival test; `question_bank` runtime role + single consumer; domain knowledge stated as pull-based; validation checklist item 6 added. |

## 2. Authoritative ownership after Phase A

| Concern | Single owner | Everywhere else |
|---|---|---|
| Evidence reading (parse once, shared surface, raw inspection, materiality-based verification, citation + evidence integrity) | `library/kernel/orchestration.md` → *Evidence contract* | short pointer |
| Epistemic semantics (`verificado_em`, `validade`, `custo`, `swing`, decay, expiry, transitions, SU row schema) | `library/kernel/states.md` (unchanged) | obligation + local default only |
| Orchestrator may/must-not | `orchestration.md` → *Orchestrator boundaries* | — |
| Pack signal delivery + Discovery/Technology boundary | `orchestration.md` → *Pack context* | `LENS_AUTHORING.md`, `PACK_AUTHORING.md`, `ARCHITECTURE.md §7.2` point at it |
| Question-bank runtime role | `orchestration.md` → *Question bank* | `PACK_AUTHORING.md` authoring guidance points at it |
| Council mechanics + persona return schema | council invocation, documented in `orchestration.md` → *Council-independent mode*; schema owned by `chairman-synthesis` | `ARCHITECTURE.md §7.3`, `LENS_AUTHORING.md` point at it |
| Lens file authoring (six sections, responsibilities, audit) | `docs/LENS_AUTHORING.md` | `ARCHITECTURE.md §7.2` keeps the minimal template + pointer |
| Capture implementation detail (xlsx L1/L3/L2) | `docs/PROCESS_CAPTURE_SPEC.md` | `orchestration.md` capture-tier table points at it |

## 3. D1–D9 decisions represented

| D | Represented as | Phase A scope |
|---|---|---|
| D1 hybrid input model | Evidence contract: shared evidence normal, raw selective + materiality-based; lens `Inputs` = one line naming what it privileges | contract stated |
| D2 capture-lite | Capture-tier table: `.docx`/`.pdf`/`.vtt` = loss-minimizing extraction with provenance, no semantic summarization, no LLM in the text path — explicitly marked **not implemented yet** | contract only (Phase B builds it) |
| D3 state metadata by pointer + local default | Lens hard rule 6: obligation + `organizacional` default + "never blank"; tables stay in `states.md` | contract stated |
| D4 append-only locally, minimal | Lens hard rule 4 kept as one clause; SU mechanics stay in `states.md` | contract stated |
| D5 orchestrator signal injection | *Pack context*: Discovery lenses pack-agnostic, cues injected with the mandatory "uncovered cues are not gaps" clause; per-signal coverage semantics explicitly prohibited | contract stated (injection wired in Phase D) |
| D6 lightweight lens outputs | Outputs section: SU = atomic knowledge; `lens-outputs/<lens>.md` = short interpretation under `## <round> — <lens>` (what matters / tensions-risks / open evidence) | contract stated |
| D7 persona = identity + mandate | Persona boundary in `orchestration.md` + `ARCHITECTURE.md §7.3` + `LENS_AUTHORING.md`; no lens re-read required | contract stated (files trimmed in Phase E) |
| D8 question bank = generation resource | *Question bank — runtime role*, single intended consumer `aisa-status` | contract stated (consumer wired in Phase D) |
| D9 SU scaffold drift | `ARCHITECTURE.md §4.1` illustrative `## Unknown` table now carries `custo` + `swing` with the real vocabulary | doc alignment only (`aisa-start` in Phase F) |
| Amendment: raw spot-check quota removed | Materiality-based verification stated in both contracts; v3.1.0 changelog bullet marked superseded | done |
| Amendment: size targets soft | "size alone does not determine PASS/FAIL"; no validator | done |
| Amendment: 5–8 signals soft | `PACK_AUTHORING.md` heuristic + survival test, explicitly not a limit | done |
| Amendment: technology exception accepted | Stated in three places as *the* exception, with "the exception does not travel" | done |

## 4. Duplication removed / avoided

- The evidence-reading rule now exists **once** (`orchestration.md`); `LENS_AUTHORING.md` states the principle in three bullets and points at the owner. The format→tool table is not copied anywhere.
- Stamping/pricing/decay tables were **not** copied into the authoring guide — only the obligation and the default.
- Signal-cue principle stated once per document, with §5 of `LENS_AUTHORING.md` as the lens-side owner and *Signals and pack context* referencing it rather than restating it.
- `ARCHITECTURE.md §7.2/§7.3` reduced to a minimal template plus pointers, instead of a second authoring guide.
- Old section title "Reading input documents" retained as an alias line rather than duplicating the section under both names.
- No new subsystem document, no new abstraction layer, no new validator.

## 5. Deferred implementation work

| Phase | Work |
|---|---|
| B | `text_extract.py` + `aisa-capture` text tier + `evidence-index.md` (the file the contract now points at) |
| C | Rewrite the 7 lens `SKILL.md` files to the target contract |
| D | `aisa-round` shared-evidence + pack-cue injection; `aisa-status` question-bank consult; council preamble authored |
| E | Trim the 7 persona files; wire the preamble; `chairman-synthesis` documents the return schema |
| F | `aisa-start` SU `## Unknown` scaffold columns + `_capture/` in the scaffold listing |
| G | PP cleanup: trim `extra_signals` against the survival test; verify `question-bank.md` probe triggers; inspect `glossary.md` |

Until Phase B lands, `.docx`/`.pdf`/`.vtt` are read raw via the format table — the contract says so explicitly, so nothing points at a file that does not exist.

## 6. Files changed

1. `library/kernel/orchestration.md` — kernel contract. **Note:** `library/` is read-only *at runtime*; this is an out-of-band authoring edit landing as a git-tracked change, the path sanctioned by `.claude/rules/library-readonly.md`. Phase A §11 of the plan requires this file, and its PASS condition greps `library/kernel/`.
2. `docs/LENS_AUTHORING.md`
3. `docs/ARCHITECTURE.md`
4. `docs/PACK_AUTHORING.md`

Not touched: any lens `SKILL.md`, any `.claude/agents/*` persona, any orchestrator skill, any hook, `library/packs/**` (incl. the PP pack, `question-bank.md`, `pack.yaml`), `library/kernel/{states,phases,glossary,render-contract}.md`, `library/kernel/tools/*`, and every file under `projects/`.

## 7. Compatibility result

| Surface | Result |
|---|---|
| Existing engagements (`cae-automation`, `dpt-galp-jp`, `kam-onboarding`, `pricing-marinha`) | No migration. Nothing read or written by them changed. |
| `_state.json` | Unchanged — no new key, no schema change. |
| Existing `shared-understanding.md` | Unchanged. The D9 edit is an *illustrative* table in `ARCHITECTURE.md`; the normative schema (`states.md`) already carried `custo`/`swing` and already states the on-read compatibility default. |
| Existing `lens-outputs/*.md` | Unchanged. The 3-heading shape applies to rounds run after Phase C; `pre-lens-order-check.py` still finds the round id in old and new files. |
| Pack manifests | Unchanged. No key added, no key removed, no resolver introduced in this phase. |
| Existing runtime pointers to "Reading input documents" (19 files) | Resolve via the explicit alias line; they are updated in Phases C–E. |
| Commands / skills / hooks | No signature or behaviour change — Phase A wrote documentation only. |

Verification A–L of the Phase A brief: all pass. Six lens sections preserved in order; "open every file in `inputs/`" is no longer the lens runtime contract (the phrase survives once in `library/kernel/`, describing the *capture* pass); no spot-check quota anywhere current; shared-evidence/parse-once model documented; signals defined as attention cues; Discovery lenses pack-agnostic; technology exception explicit; question bank not permanent lens context; persona boundary documented; no size/token/signal validator; no runtime implementation and no PP pack content changed.
