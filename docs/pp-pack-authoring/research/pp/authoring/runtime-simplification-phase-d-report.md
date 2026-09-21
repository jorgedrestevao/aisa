# Runtime Simplification — Phase D (Orchestrator) Report

<!--
provenance: IMPLEMENTATION (2 orchestrator skills wired; 1 new test file; no kernel, pack, lens,
  persona, hook or engagement file modified)
scope: .claude/skills/aisa-round/SKILL.md, .claude/skills/aisa-status/SKILL.md,
       .claude/tests/test_orchestrator_wiring.py (new)
authored: 2026-09-04
basis: runtime-simplification-plan.md §6 + §11 Phase D; phase-a-report.md (contracts),
       phase-b-report.md (shared evidence), phase-c-report.md (lens contract)
path note: written to the repo's actual `research/pp/authoring/` directory
  (`docs/pp-pack-authoring/research/pp/authoring/`), alongside the plan and the A/B/C reports.
-->

## 1. Implementation summary

Two skills wired, nothing invented. **Orchestrator = context provisioning + execution coordination.**

| Change | Where |
|---|---|
| Freshness check extended to both capture tiers + the index | `aisa-round` step 3.5 |
| Round context assembled once (evidence index · pack cues · next free SU ids) | `aisa-round` step 3.6 (new) |
| Explicit lens invocation payload + a "do not dump" rule | `aisa-round` step 4b |
| Boundary notes (lens→persona map · technology stays out · question bank is not lens context) | `aisa-round` *Notes* |
| Question-bank consult, selective and degradable | `aisa-status` step 6d (new) |

Phase C removed the bookkeeping from the lens files; Phase D is where that bookkeeping now lives.
The three things the lens used to resolve for itself — where the evidence is, what round/ids it is on,
what the pack adds — arrive as pointers in the invocation. Nothing else moved.

Cost: `aisa-round` 3,286 → 7,744 chars (+4.5k), `aisa-status` 4,938 → 6,308 (+1.4k). Above the plan's
+900/+700 indicative figures, and deliberately so: the plan's estimate predates the explicit payload
block and the failure/degradation clauses this phase's brief requires. It is paid once per round
against the −12.6k per round Phase C removed from six lens files.

## 2. Lens invocation payload

`aisa-round` step 4b now carries this block into `Skill: lens-<name>` — pointers, not contents:

```
Round: <R-NN> · engagement `<slug>` · engagement root `<engagement>`
Shared Understanding: `<engagement>/shared-understanding.md` — next free ids: C-NNN · A-NNN · U-NNN · X-NNN · R-NNN
Request context: `<engagement>/context.json`
Prior lens outputs this round: `<engagement>/lens-outputs/<lens>.md`, … (or "none — first lens of the round")
Shared evidence: `<engagement>/_capture/evidence-index.md` — this engagement's source map
  (source · format · normalized evidence · status · cite as). Raw sources stay at `<engagement>/inputs/`,
  are always openable, and are authoritative on conflict. Read what bears on your perspective;
  nobody has decided that for you.
Memory (optional): `.claude/agent-memory/_universal/<persona>/*.md` (incl. `diary.md`) · `_tenant/<tenant>/<persona>/*.md`
Pack attention cues (`<pack>`): <token>, … — cues, not a checklist. Follow only what is material to
  this engagement; an uncovered cue is not a gap and never becomes an `Unknown`.
```

Covers every item the brief lists: engagement identity/path · round id · SU (+ next free ids) · prior
lens outputs required by lens order · shared evidence source map · pack cues · memory pointer.

**Do not dump** is stated in the skill: no evidence bodies, no `pack.yaml`, no `question-bank.md`, no
domain-knowledge files, no full prior-lens prose. The lens opens what it needs. It is told where things
are — never what to conclude, which evidence matters, which cue is relevant, or which state a finding
should get.

Live resolution on `pricing-marinha` (read-only simulation of steps 3.5/3.6): index present, 5 sources
fresh across both tiers, cues resolved for all six lenses, next free ids `C-192 · A-047 · U-115 ·
X-037 · R-080`.

## 3. Shared evidence wiring

`_capture/evidence-index.md` (Phase B) is the shared source map. Step 3.6a resolves it and step 4b
carries its **path**; the lens reads it. Absent index → the invocation says so verbatim
(*"raw `inputs/` is the evidence surface"*), so shared capture is never silently assumed.

What the orchestrator explicitly does **not** do, stated in the skill: rank sources, assign sources to
lenses, summarize them, classify importance, or build a per-lens evidence bundle. *The orchestrator
exposes evidence; the lens decides what matters.*

## 4. Freshness behavior

One rule, both tiers — possible only because `xlsx_extract.py` and `text_extract.py` write the same
`identity.sha256` key:

- for each `.xlsx`/`.xlsm`/`.docx`/`.pdf`/`.vtt` in `inputs/`, compare the file's SHA-256 against
  `_capture/<file>.extraction.json → identity.sha256`;
- missing artefact · hash mismatch · missing `evidence-index.md` → invoke `aisa-capture` for those
  files before any lens runs (both extractors self-cache, so a fresh file costs one hash check);
- hash/status comparison only — **no semantic diff** of old vs new content;
- formats outside the tiers are not captured and are never stale;
- capture failure stays soft: warn, name the file, raw fallback — and any source left stale is named in
  the invocation, so no lens reasons over stale normalized evidence unknowingly.

Excel behaviour is unchanged: the same rule it already had, now written once for both tiers. No second
freshness system; `aisa-capture` remains the only capture path.

## 5. Pack signal injection

Step 3.6b: `_state.json.pack` → `library/packs/<pack>/pack.yaml` → `lenses_config.<lens>.extra_signals`,
resolved once per round for the lenses about to run, injected verbatim with the mandatory clause:

> Pack attention cues (`<pack>`): … — cues, not a checklist. Follow only what is material to this
> engagement; an uncovered cue is not a gap and never becomes an `Unknown`.

No scoring, no ranking, no filtering, no reordering, no rewriting into questions, no coverage
bookkeeping. The Discovery lens still never reads `pack.yaml` (asserted).

Injected block size per lens with the current PP pack — the observability the plan wanted before the
Phase G trim:

| lens | cues | injected line |
|---|---:|---:|
| business | 12 | 356 chars |
| operations | 14 | 426 |
| user | 15 | 508 |
| data | 20 | 625 |
| governance | 20 | 634 |
| financial | 8 | 259 |

Risk 2 of the plan ("injection re-creates the checklist") is live at 20 cues: `data` and `governance`
inject ~630 characters of tokens. The clause guards the semantics; Phase G's trim to 5–8 is what makes
the list readable.

## 6. Question-bank consumer

`aisa-status` step 6d — the single consumer, per D8. It resolves `pack.yaml → question_bank`, reads it,
and uses it to phrase agenda items as askable questions and to add a probe `P-<LENS>-NN` only where the
SU shows its stated trigger observed. The same consult may phrase what would resolve a material
`Conflicted`/`Risky` row or close an evidence gap the index reports (`failed`/`skipped`/`empty`).

Stated constraints: do not enumerate the bank · do not ask every core question · do not produce one
question per Unknown · never coverage. Prioritization is qualitative, using metadata the rows already
carry (`criticidade`, `custo`, `swing`, state) — no formula, no ranking engine. *Reason first,
formulate questions second.*

`grep -rn "question_bank" .claude/` → exactly one file: `aisa-status/SKILL.md`. `aisa-round` names the
bank only to keep it out of the launch context.

## 7. Council compatibility

Untouched by design (Phase E owns them): `aisa-frame`, `aisa-options`, the 7 persona files,
`chairman-synthesis`. Council behaviour is unchanged — their step-5 prompts still point personas at
their lens `SKILL.md`, and that pointer still resolves (the Phase C rewrite kept a *Hard rules*
section in every lens).

**Common execution context identified for Phase E** — every item below is repeated today across the two
council prompts and the seven persona files, and each is already produced by `aisa-round` step 3.6 or
stated once in `orchestration.md`:

| Common item | Today | Phase E source |
|---|---|---|
| mode statement (council-independent, phase, round, engagement, pack) | in both prompts | prompt preamble |
| read-only tool grant · no in-flight peer reads · returns, never writes | persona `## Mode` × 7 | preamble (`orchestration.md` → *Council-independent mode*) |
| the two binding hard rules (no vendor naming outside Options; no `Confirmed` without evidence) | persona restatement × 7 + prompt | preamble |
| persona return schema | persona `## Output format` × 7 | preamble; owner `chairman-synthesis` |
| shared evidence pointer | prompts still say "every file under `inputs/`" | step 3.6a output — the same index path |
| pack attention cues | absent from council prompts | step 3.6b resolution, reused per persona lens |
| memory pointer | prompt + persona file | preamble |

Phase E can lift steps 3.6a/3.6b verbatim; only the return schema and the SU-excerpt path are council-specific.

## 8. Failure / degradation behavior

| Situation | Behaviour |
|---|---|
| missing `evidence-index.md` | step 3.5 tries `aisa-capture`; still missing → the invocation says *"no `_capture/evidence-index.md` — raw `inputs/` is the evidence surface"*. Never silently assumed |
| source stale and capture could not refresh it | named in the invocation; lens is not left reasoning over stale normalized evidence |
| failed / skipped extraction | source stays listed in `evidence-index.md` with its status; the lens may read the raw source (unchanged Phase B contract) |
| empty / absent `extra_signals`, or no active pack | nothing injected, cue line omitted entirely; the lens runs on its universal perspective. Not a round failure |
| `pack.yaml` unparseable | visible failure — report and stop, as `aisa-start` step 3 does for a missing manifest. No new validation machinery |
| missing `question_bank` key or file | `/status` says so in one line and builds the agenda from SU rows alone |
| lens skill not installed | unchanged pre-existing guard |

Optional resources never break core Discovery: shared evidence, pack cues and the question bank each
degrade to the behaviour that existed before them.

## 9. Tests / checks

New: `.claude/tests/test_orchestrator_wiring.py` — **23 tests, OK** (~1 s). One file, stdlib
`unittest`, no framework. It asserts the declared wiring plus the one functional mechanism behind it.

| Group | Covers |
|---|---|
| `TestSharedEvidence` (4) | round resolves the index path; absence stated, not assumed; no ranking/assignment/summarizing/bundling; the index producer exists and is `aisa-capture`'s |
| `TestPackSignalInjection` (6) | manifest key resolved; PP declares signals for all six Discovery lenses; verbatim pass-through, no scoring; the "cues, not a checklist / uncovered cue is not a gap" clause present; empty/absent degrades and the cue line is omitted; technology is not in the Discovery loop |
| `TestDiscoveryPackBoundary` (2) | no Discovery lens references `pack.yaml`, `library/packs/`, or the question bank |
| `TestQuestionBankConsumer` (5) | exactly one `question_bank` resolver in `.claude/`; `aisa-round` only forbids it; consult is selective and non-coverage; degrades when absent; bank file exists |
| `TestFreshness` (3) | round covers both tiers by `identity.sha256`, hash/status only; **a changed `.vtt` is detected by the hash and re-captured, and the new passage appears in the artefact**; both extractors expose the same identity key |
| `TestInvocationCompactness` (3) | the "do not dump" rule; the payload names every required context item; the orchestrator does no domain reasoning |

Existing checks re-run, all green:

| Check | Result |
|---|---|
| `python library/kernel/tools/tests/test_text_extract.py` (Phase B, incl. **Excel regression**) | 23 tests, **OK** (~51 s) |
| `dashboard.py --engagement <slug>` × 4 engagements | all build |
| `pre-lens-order-check.py` on a temp fixture | **blocks** `lens-operations` with no prior output; **allows** it after a `## R-01 — business` block |
| `pre-write-guard.py` on `library/kernel/orchestration.md` | denies (fail-closed, as designed) |
| `phase-completeness.py`, `phase-gate-check.py` | exit 0 |
| live simulation of steps 3.5/3.6 on `pricing-marinha` | index resolvable · 5 sources fresh (2 docx, 1 xlsx, 2 vtt) · cues resolved for all 6 lenses · next free ids computed |

Not run: a live `/round` writing engagement state — Phase D changed the invocation, not the lens, and
the mechanical dependencies (order hook, freshness, resolution) are covered above. No engagement file
was modified in this phase.

## 10. Files changed

**Modified**

1. `.claude/skills/aisa-round/SKILL.md` — step 3.5 (both tiers + index), step 3.6 a/b/c (new), step 4b
   (payload + do-not-dump), *Notes* (lens→persona map, technology boundary, question-bank boundary).
2. `.claude/skills/aisa-status/SKILL.md` — step 6d (question-bank consult, prioritization, degradation)
   and one agenda output line.

**New**

3. `.claude/tests/test_orchestrator_wiring.py`

**Not touched**: `library/**` (kernel contracts, tools, and the whole PP pack — `pack.yaml`,
`question-bank.md`, `glossary.md`), all 7 lens `SKILL.md`, all 7 `.claude/agents/*`, `aisa-frame`,
`aisa-options`, `aisa-capture`, `aisa-start`, `chairman-synthesis`, every hook, `.claude/settings.json`,
`docs/*`, and everything under `projects/`.

**Known stale line, deliberately left**: `library/kernel/orchestration.md` → *Question bank — runtime
role* still ends with *"(Consumer not yet wired; the contract is stated here first.)"*. It is now wired.
`library/` is read-only at runtime and `pre-write-guard.py` denies the write; the correction belongs in
the same out-of-band batch as any other kernel edit (Phase E touches that file for the council
preamble). Flagged, not silently ignored.

## 11. Deferred Phase E/F/G work

| Phase | Work |
|---|---|
| **E — personas** | Trim the 7 agent files to identity + mandate + memory + lens pointer; author the council preamble and wire it into `aisa-frame`/`aisa-options` step 5 (replacing "every file under `inputs/`" with the index pointer and dropping "read your lens `SKILL.md`"); `chairman-synthesis` documents the return schema. §7 above lists exactly what the preamble absorbs. |
| **F — state scaffold** | `aisa-start` SU `## Unknown` header gains `custo` + `swing`; `_capture/` in the scaffold listing. |
| **G — PP cleanup** | Trim `extra_signals` to preferably 5–8 per Discovery lens under the survival test (the injected sizes in §5 are the input to that decision); verify `question-bank.md` probe triggers are SU-observable now that `/status` consults them; inspect `glossary.md`. |
| kernel touch-up | Remove the stale "consumer not yet wired" parenthetical in `orchestration.md` (§10). |

Not in scope and not started: evidence router, relevance scoring, question scoring, new state machine,
council persona changes, PP pack content changes.

## 12. Anti-complexity result

| | Question | Verdict | Basis |
|---|---|---|---|
| A | New routing engine? | **NO** | the orchestrator resolves three paths and one manifest key; no dispatch table, no rules |
| B | Evidence relevance assigned by the orchestrator? | **NO** | index path handed over intact; "do not rank, assign, summarize or bundle" is written into the skill and asserted by test |
| C | Signal scoring? | **NO** | tokens passed verbatim, order as authored |
| D | Signal coverage requirements? | **NO** | mandatory clause "cues, not a checklist; an uncovered cue is not a gap and never becomes an `Unknown`" |
| E | Question scoring formula? | **NO** | qualitative prioritization on metadata the rows already carry; "no scoring formula, no ranking engine" stated |
| F | Question bank in every lens? | **NO** | one resolver in `.claude/` (`aisa-status`); `aisa-round` forbids it in the launch context |
| G | Domain knowledge preloaded? | **NO** | not resolved in the Discovery loop at all; technology stays pull-based in Options |
| H | Full evidence bodies in the launch context? | **NO** | pointers only; "do not dump" rule + test |
| I | Orchestrator performs domain reasoning? | **NO** | it names locations, never conclusions, relevance, or states |
| J | Lens invocation simpler than the old read-everything model? | **YES** | ~1.1k-char pointer block replaces per-lens `inputs/` enumeration, capture protocol, id bookkeeping and pack parsing — all deleted in Phase C, none re-created here |

---

PHASE D — ORCHESTRATOR: PASS
SHARED EVIDENCE WIRED INTO ROUND: YES
TEXT-SOURCE FRESHNESS WIRED: YES
DISCOVERY PACK SIGNALS INJECTED: YES
SIGNALS TREATED AS ATTENTION CUES: YES
EMPTY PACK SIGNALS DEGRADE GRACEFULLY: YES
QUESTION BANK HAS SELECTIVE CONSUMER: YES
QUESTION BANK LOADED INTO LENSES: NO
EVIDENCE RELEVANCE DECIDED BY ORCHESTRATOR: NO
SIGNAL/QUESTION SCORING ENGINE INTRODUCED: NO
DOMAIN KNOWLEDGE PRELOADED: NO
COUNCIL BEHAVIOR PRESERVED: YES
PP PACK CONTENT MODIFIED: NO
READY FOR PHASE E — PERSONAS: YES
