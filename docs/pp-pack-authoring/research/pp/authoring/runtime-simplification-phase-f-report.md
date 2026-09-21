# Runtime Simplification — Phase F report: state scaffold

<!--
provenance: IMPLEMENTATION (1 skill file, 1 new test file)
scope: D9 (SU scaffold contract drift) + `_capture/` scaffold visibility
authored: 2026-09-04
basis: runtime-simplification-plan.md §2 D9 / §5 phase F + phase-e-report §12
no kernel file modified · no pack file modified · no lens/persona modified · no engagement file written
-->

Compatibility fix only. D1–D9 were not reopened.

## 1. D9 fix

`.claude/skills/aisa-start/SKILL.md` step 8, `## Unknown` header — was 6 columns, now 8:

```
| id | lens | pergunta | quem responde | criticidade | custo | swing | ronda |
```

Byte-identical column list and order to `library/kernel/states.md` §*Schema of Shared Understanding
rows*. Separator row widened to match. Semantics untouched: `custo`/`swing` are defined in
`states.md` §*Question economics* and nowhere else; step 8's preamble now names that section beside the
`verificado_em`/`validade` pointer it already carried. The other four state headers already matched the
contract (asserted for all five). No new column, no new metadata, no new state.

`docs/ARCHITECTURE.md §4.1` needed no edit — its table already carries `custo | swing`.

## 2. `_capture/` scaffold visibility

Step 5's directory listing gained one line and one clause:

```
├── inputs/                   (raw source material — any captured docs)
└── _capture/                 (deterministic shared evidence generated from supported inputs — written
                               by step 11; raw `inputs/` stays authoritative)
```

`_capture/` is named as generated evidence, not a replacement for `inputs/`. Its producer is unchanged
(step 11 → `aisa-capture`, the only writer of `_capture/evidence-index.md`). No second evidence
directory introduced (asserted).

## 3. Backward compatibility

No migration written, none needed.

- `dashboard.py` maps SU columns by header name and infers absent ones —
  `custo = email`, `swing = dimensionante`, flagged `custo_inferred` / `swing_inferred`, with a
  `schema_flavour = legacy` diagnostic. `states.md` already states the rule as *applied on read, never
  migrated*.
- The three pre-v2.3 engagements (`cae-automation`, `dpt-galp-jp`, `kam-onboarding`) keep their 6-column
  `## Unknown` header and parse (e.g. `cae-automation`: 43 Unknowns, all with inferred `custo`/`swing`).
  `pricing-marinha` already carries the 8 columns and parses as `v2.3`.
- Applies to newly initialized scaffolds only; existing SUs update naturally.

## 4. Tests

**New**: `.claude/tests/test_state_scaffold.py` — **15 tests, OK** (0.26 s). One file, stdlib
`unittest`, no scaffold driver, no fixture engagement.

| Group | Covers |
|---|---|
| `TestScaffoldMatchesContract` (6) | all 5 scaffold headers equal the `states.md` column lists parsed from the contract itself; `custo`+`swing` present in `## Unknown`, in contract order; separator widths match; kernel sections pointed at; no state invented |
| `TestCaptureVisibleInScaffold` (4) | `_capture/` in the listing beside `inputs/`; raw material not replaced (`authoritative`); exactly one evidence directory; producer still `aisa-capture` |
| `TestNoMigration` (5) | no migration/backfill wording in `aisa-start`; a pre-v2.3 SU still exists unconverted; the parser reads all 4 existing SUs and yields a `custo`/`swing_class` for every Unknown; defaults match the kernel's; the new skeleton parses as `v2.3` with 0 rows and 0 diagnostics |

**Existing checks re-run, all green:**

| Check | Result |
|---|---|
| `python .claude/tests/test_orchestrator_wiring.py` (Phase D) | 23 tests, **OK** |
| `python .claude/tests/test_council_wiring.py` (Phase E) | 31 tests, **OK** |
| `dashboard.py --engagement <slug>` × 4 | all build (mtime debounce skipped every write — the 4 `dashboard.html` mtimes are unchanged) |
| `phase-completeness.py` | exit 0 |
| `phase-gate-check.py` | exit 0 |

Not run: a live `/start`. Phase F changed the skeleton text the step writes and one listing line; steps
1–4, 6, 7, 9, 10, 11 — pack resolution, the exists-guard, the interactive capture, `context.json`, the
atomic `_state.json` write (`phase=discovery`, `round=R-00`), the header files, the output line and the
capture invocation — are byte-identical.

**Discovered inconsistency, reported not fixed** (out of Phase F scope): step 5's listing omits
`story.md`, which step 9 writes. Pre-existing, unrelated to D9, and it blocks nothing.

## 5. Files changed

**Modified**

1. `.claude/skills/aisa-start/SKILL.md` — step 8 `## Unknown` header + separator (D9); step 8 preamble
   pointer to *Question economics*; step 5 listing gains `_capture/` and the `inputs/` clause.

**New**

2. `.claude/tests/test_state_scaffold.py` — 15 tests.

**Not touched**: `library/**` (kernel and the whole PP pack), all 7 lens `SKILL.md`, all 7 persona
files, every other orchestrator (`aisa-round`, `aisa-status`, `aisa-frame`, `aisa-options`,
`aisa-capture`, `chairman-synthesis`), every hook, `.claude/settings.json`, `docs/*` outside this
report, and everything under `projects/`.

## 6. Deferred Phase G + kernel touch-up

| Item | Work |
|---|---|
| **G — PP cleanup** | Trim `extra_signals` to preferably 5–8 per Discovery lens under the survival test (the injected block is now observable in both loops); verify `question-bank.md` probe triggers are SU-observable; inspect `glossary.md`. |
| kernel touch-up | The single out-of-band edit from Phase E §9 — `library/kernel/orchestration.md` → *Question bank — runtime role*: replace `*(Consumer not yet wired; the contract is stated here first.)*` with "Wired since Phase D: `aisa-status` step 6d resolves and consults it." Still blocked by `pre-write-guard.py` + `settings.json deny`, by design; still the only item in that batch. |
| docs (unclaimed) | `docs/IMPLEMENTATION_PLAN.md:570` restates the pre-v2.3 `## Unknown` schema. Historical plan document, not a runtime contract — left alone. |

Not in scope and not started: migration machinery, engagement data changes, PP pack content, SU redesign.

---

PHASE F — STATE SCAFFOLD: PASS
