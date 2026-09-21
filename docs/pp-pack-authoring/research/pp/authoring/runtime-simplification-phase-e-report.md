# Runtime Simplification — Phase E report: council personas

<!--
provenance: IMPLEMENTATION (7 persona agents, 2 council orchestrators, 1 synthesis skill, 1 new test)
scope: D7 (persona contract + council preamble) + §6.4/§7/§8/§10 of the plan
authored: 2026-09-04
basis: runtime-simplification-plan.md §6.4/§7/§8 + phase-d-report §7 (implementation map)
no pack file modified · no lens SKILL.md modified · no kernel file modified (see §9)
path note: same directory as the plan and the A-D reports
-->

Implements Phase D §7 as written. D1–D9 were not reopened.

---

## 1. Implementation summary

Four moves, all subtractive except the preamble that absorbs what was subtracted.

1. **One canonical council preamble**, authored once in `.claude/skills/chairman-synthesis/SKILL.md`
   → *Council launch preamble*. It carries, per persona, everything the seven files used to restate:
   mode · phase · round · engagement · pack · the `_council-prep` excerpt · the shared-evidence
   pointer · pack attention cues · the memory pointer · the independence rule · the phase's
   technology-neutrality rule · the evidence-integrity invariant · the return schema. Owner is the
   schema's only consumer, so schema and parser cannot drift.
2. **`aisa-frame` step 5 and `aisa-options` step 5** now build every persona prompt from that block
   with substitutions. Both gained a **step 4b** that resolves the same three things `aisa-round`
   step 3.6 resolves (evidence index · `extra_signals` cues · memory pointer) — lifted, not reinvented.
3. **All 7 persona files reduced** to identity (including *what you challenge*), lens-binding line,
   phase mandate and memory binding. Deleted: `## Mode (council-independent)`, `## Output format`,
   the lens hard-rule restatement, the "read every file under `inputs/`" instruction.
4. **No persona is sent to its lens `SKILL.md`.** The two council prompts dropped that line; each
   persona file states positively that it does not read it.

No new file, directory, skill, agent, config key or hook was introduced. One test file was added.

---

## 2. Persona before/after

Size is diagnostic only — no threshold gates anything.

| Persona | before | after | Δ |
|---|---:|---:|---:|
| `business-analyst` | 3 462 | 1 942 | −44% |
| `operations-lead` | 3 142 | 1 901 | −40% |
| `user-advocate` | 2 997 | 1 976 | −34% |
| `data-steward` | 3 125 | 2 079 | −33% |
| `compliance-officer` | 3 208 | 2 135 | −33% |
| `cfo-lens` | 3 032 | 2 051 | −32% |
| `solution-architect` | 3 708 | 3 053 | −18% |
| **total** | **22 674** | **15 137** | **−33%** |

`solution-architect` shrank least, deliberately: it keeps its `## Phase gate` and its pull-based pack
paragraph, the two things that are genuinely its own and not supplied by the invocation.

What each persona **gained**: an explicit *What you challenge* paragraph. That is the phase's one
addition, and it is the part that makes the voice independent rather than a label.

**Council framework context per persona, per round** (the number that matters at runtime):

| | launch prompt | persona file | mandated lens read | total |
|---|---:|---:|---:|---:|
| Framing, before | 1 087 | 3 161 | 3 972 | **8 220** |
| Framing, after | 3 176 | 2 014 | — | **5 190** (−37%) |
| Options, before (six) | 1 552 | 3 161 | 3 972 | **8 685** |
| Options, after (six) | 3 347 | 2 014 | — | **5 361** (−38%) |
| Options, before (architect) | 1 552 | 3 708 | 5 373 | **10 633** |
| Options, after (architect) | ~3 530 | 3 053 | — | **6 583** (−38%) |

Whole-round framework text: Framing 49 320 → 31 140 · Options 62 743 → 38 746. The launch prompt grew
because it now carries what seven files carried seven times; it is authored once and, unlike the lens
`SKILL.md` read it replaced, it is bounded.

---

## 3. Perspective preservation

Each persona keeps its bound concern and states what it refuses to accept at face value.

| Persona | Bound concern | What it challenges (kept sharp) |
|---|---|---|
| `business-analyst` | outcomes, value, strategic rationale, stakeholder/decision implications | declared impact nobody measures · urgency that is a calendar, not a cost · the veto-holder the sponsor's framing hides · a KPI nobody owns |
| `operations-lead` | operational reality, exceptions, handoffs, ownership, supportability | **distrusts the documented process** · the happy path sold as the process · "rare" exceptions with no count · work that survives on one person's memory |
| `user-advocate` | lived experience, adoption, accessibility, context of use | "the users" as one group · a journey drawn from a desk · adoption assumed from betterness · accessibility as a later increment. Hands offline/sensitivity tensions to data + governance |
| `data-steward` | information quality, ownership, lifecycle, sensitivity, dependencies | an owner that turns out to be a mailbox · "clean data" nobody profiled · two systems of record · sensitivity by habit. Records sensitivity; does not adjudicate it |
| `compliance-officer` | authority, controls, compliance, privacy, auditability | runs the **conflict scan** across the other perspectives' stated needs; a collision becomes an explicit conflict with both sides named, never a chosen winner |
| `cfo-lens` | affordability, economics, cost sensitivity, value uncertainty | a benefit with no denominator · an as-is cost never built from volume × cycle time × loaded rate · savings in hours that never leave payroll · payback at uncommitted volume |
| `solution-architect` | feasibility, architecture, integration, security, scale, lifecycle, operability | elegance standing in for fit · premature vendor commitment and its reversibility cost · an integration priced as a connector · an all-technology option set |

Tested mechanically: seven distinct `## Identity` bodies (no two equal, each >200 chars), each with a
*What you challenge* paragraph, and each retaining the vocabulary of its bound concern.

Lens ↔ persona remain the **same perspective in two runtime roles** — lens = inline reasoning
perspective, persona = independent council voice — not runtime copies of each other. Keeping them
aligned is an authoring duty, already stated in `docs/LENS_AUTHORING.md` (§*Adding a lens* step 5,
§*Modifying* and audit item 6) and `docs/ARCHITECTURE.md §7.3`; no doc edit was needed this phase.

---

## 4. Common preamble

Location: `.claude/skills/chairman-synthesis/SKILL.md` → *Council launch preamble* (one fenced block,
~3 450 chars including all phase selectors). Consumers: `aisa-frame` step 5, `aisa-options` step 5.

Placed with the chairman because the return schema at its foot has exactly one consumer — the
synthesis procedure in the same file. A schema authored away from its parser drifts from it.

Substitution, not duplication: the two orchestrators reference the block and list what to substitute
(`<phase>`, `<round>`, `<slug>`, `<pack>`, `<engagement>`, `<persona>`, the excerpt path, and whatever
step 4b resolved). Bracketed `[…]` lines are selectors — the launcher keeps the one that applies and
drops the rest. Neither orchestrator restates the mechanics, and nothing was copied into a persona file.

`library/kernel/orchestration.md` already owns the contract this implements (*Council-independent mode*
→ "Common council mechanics live here, not in the persona files", and *Persona boundary* → "A council
persona is not required to re-read its lens `SKILL.md`"). Phase E is that contract's implementation;
the kernel needed no new wording.

---

## 5. Shared evidence behavior

`read every file under <engagement>/inputs/` is gone from both council prompts. In its place:

- **Source map** — `<engagement>/_capture/evidence-index.md` (source · format · normalized evidence ·
  status · cite as), the same artefact Discovery reads. Personas open the normalized evidence bearing
  on their mandate, and a raw source when material to their confidence.
- **Raw sources unchanged** — `inputs/` stays openable and authoritative on conflict.
- **Absence is stated, never assumed** — no index → the prompt says *"no `_capture/evidence-index.md`
  — raw `inputs/` is the evidence surface"*; sources reported `failed` / `skipped` are named.
- **No routing** — step 4b is explicit that the orchestrator does not rank, assign, summarize or
  bundle sources and builds no per-persona evidence view; the prompt tells the persona *"nobody ranked
  it for you, and no evidence has been assigned to you"*. No evidence bundles, no relevance scores.

---

## 6. Pack cue behavior

For the six Discovery personas, step 4b resolves `_state.json.pack` → `pack.yaml` →
`lenses_config.<lens>.extra_signals` for the lens each persona is the council voice of, and injects the
tokens **verbatim** — no scoring, ranking, filtering, reordering or rewriting. Same semantics as
Discovery, same trailing clause: *"cues, not a checklist. Follow only what is material to this
engagement; an uncovered cue is not a gap and never becomes an `Unknown`."*

Degradation: missing `pack` key, missing `lenses_config.<lens>`, missing `extra_signals`, or an empty
list → nothing injected and the cue line omitted entirely. An unparseable `pack.yaml` is a visible
failure (report and stop), as elsewhere.

`solution-architect` is **outside** this model, as in Discovery: it receives no `extra_signals`. Its
pack access stays pull-based and Options-only — the prompt adds one line naming the resolved pack root
(`library/packs/<pack>/`), and the mandate to pull only the branch and domain-knowledge file it is
actually evaluating lives in its agent file. Neither orchestrator reads `decision-tree.md` or
`domain-knowledge/`, and neither ever puts their contents in a prompt.

---

## 7. Return schema ownership

Owner: `chairman-synthesis` — the schema sits inside the preamble it authors, immediately above the
procedure that parses it. Both orchestrators carry it to the personas; no persona file contains it.

The schema is byte-identical to what the seven files used to each carry: `## <persona> — Round <round>
/ Phase <phase>` plus `Headline` · `Evidence anchors` · `Proposal` · `Open questions / Unknowns
flagged` · `Conflicts seen` · `Risks`, with the `- (none)` convention for empty sections and the
"never omit a header" rule. One schema for all personas — the phase-specific variation lives inside
`### Proposal`, exactly as before.

---

## 8. Chairman compatibility

Synthesis reasoning untouched: Steps 1, 2, 2b (dialectic hand-back), 3, 4, 5, 6, 7, 8 and all six hard
rules are unchanged. Three documentation-only lines changed, the minimum needed to say where the schema
lives now:

- *Role* — "see persona agent files for the schema" → "in the schema this skill owns (*Council launch
  preamble* below — the launch prompt carries it to them; the persona files do not)".
- *Inputs* — "shaped per `.claude/agents/<persona>.md` → *Output format*" → "shaped per the return
  schema in *Council launch preamble* below".
- Step 1 — "Parse the six sections" → "Parse the six sections of the return schema".

Trimmed personas still satisfy the chairman's input: the six sections it parses are the six the
preamble mandates (asserted by test), and the anchor/criticidade/partes/impacto/mitigação micro-formats
its Step 3 table consumes are unchanged.

---

## 9. Kernel cleanup result

**Not done — blocked by the guard, as designed. Reported, not bypassed.**

The one stale line Phase D flagged is `library/kernel/orchestration.md` → *Question bank — runtime
role*: `*(Consumer not yet wired; the contract is stated here first.)*`. It has been wired since Phase D
(`aisa-status` step 6d). The intended replacement text is:

> Wired since Phase D: `aisa-status` step 6d resolves and consults it.

The edit was attempted with the normal tool and refused twice over: `.claude/settings.json`
`permissions.deny` (`Edit(./library/**)`) and `pre-write-guard.py` (fail-closed, verified again this
phase — exit 2, `permissionDecision: deny`). Editing it another way would be bypassing the guard, which
this phase does not do. It remains a one-line out-of-band kernel edit, now the only item in that batch.

**No other kernel edit was needed.** The council-contract wording Phase E depends on — mechanics
ownership, schema owner, and "a council persona is not required to re-read its lens `SKILL.md`" — is
already in `orchestration.md` from Phase A/C. Nothing was opportunistically rewritten.

---

## 10. Tests / checks

**New**: `.claude/tests/test_council_wiring.py` — **31 tests, OK** (<0.1 s). One file, stdlib
`unittest`, no framework, no council driver, no fixture engagement.

| Group | Covers |
|---|---|
| `TestPersonasExistAndStayDistinct` (4) | all 7 exist with Identity + Mandate (Framing/Options/Decision) + Memory; each states what it challenges; no two Identity bodies equal; each keeps its bound-concern vocabulary |
| `TestNoFrameworkDuplicationInPersonas` (6) | no `## Output format`, no schema section, no `## Mode`, no in-flight/tool-grant/"every file under" text, no kernel state semantics (`verificado_em`, `validade`, `states.md`, `was <id>`, append-only); no persona references its own lens `SKILL.md`; neither council prompt sends one there; size diagnostic |
| `TestCommonMechanicsCentralized` (4) | preamble exists exactly once and both orchestrators reference it; it carries all 12 required context items; the independence rule is in the launch context and in no persona file; `orchestration.md` owns the boundary |
| `TestSharedEvidenceInCouncil` (4) | "every file under `inputs/`" gone from both prompts; index is a source map, raw authoritative on conflict; no bundles/scores/router and no per-persona view; absence stated explicitly |
| `TestPackCues` (4) | cue semantics ("cues, not a checklist", "uncovered cue is not a gap"); verbatim pass-through + degradation; technology excluded from the Discovery cue model; domain knowledge not preloaded and never dumped |
| `TestPhaseBoundaries` (3) | Framing neutrality line present and selected, and no Discovery persona names a vendor (7 vendor strings checked); architect not launched in Framing (orchestrator + phase gate + `not invoked` mandate); Options technology reasoning allowed for the architect only |
| `TestChairmanCompatibility` (4) | the six sections the chairman parses are the six the schema mandates; the chairman still consumes each label; no residual pointer to persona files for the schema; `- (none)` convention kept; synthesis steps 1/2/2b/3 unchanged |
| `TestMemoryBinding` (2) | each persona keeps its own `_universal` / `_tenant` paths and its diary; memory is a pointer, not a dump |

**Existing checks re-run, all green:**

| Check | Result |
|---|---|
| `python .claude/tests/test_orchestrator_wiring.py` (Phase D) | 23 tests, **OK** (~1 s) |
| `python library/kernel/tools/tests/test_text_extract.py` (Phase B) | 23 tests, **OK** (~52 s) |
| `dashboard.py --engagement <slug>` × 4 (`cae-automation`, `dpt-galp-jp`, `kam-onboarding`, `pricing-marinha`) | all build |
| `phase-completeness.py` (incl. `check_framing` / `check_options`) | exit 0 |
| `phase-gate-check.py` | exit 0 |
| `pre-write-guard.py` on `library/kernel/orchestration.md` | deny, exit 2 (fail-closed, as designed) |

Not run: a live `/frame` or `/options` on an engagement. Phase E changed prompt composition and persona
briefings, not the synthesis or the state machine; the mechanical dependencies (`_council-prep` files,
artefact presence, 6/7 persona counts) are the ones `phase-completeness.py` asserts, and they are
unaffected by prompt text. No engagement file was modified.

---

## 11. Files changed

**Modified**

1. `.claude/agents/business-analyst.md` — rewritten to the target contract.
2. `.claude/agents/operations-lead.md` — idem.
3. `.claude/agents/user-advocate.md` — idem.
4. `.claude/agents/data-steward.md` — idem.
5. `.claude/agents/compliance-officer.md` — idem.
6. `.claude/agents/cfo-lens.md` — idem (keeps nothing mechanical).
7. `.claude/agents/solution-architect.md` — idem, keeping `## Phase gate` and the pull-based pack paragraph.
8. `.claude/skills/chairman-synthesis/SKILL.md` — new *Council launch preamble* section (incl. the return schema); three reference lines updated. Synthesis procedure and hard rules untouched.
9. `.claude/skills/aisa-frame/SKILL.md` — *Inputs*: + evidence index, + `extra_signals`, + preamble source; **step 4b (new)**: evidence · cues · memory resolution; **step 5**: rewritten to build the prompt from the preamble (− "read your lens `SKILL.md`", − "every file under `inputs/`", − per-persona mechanics); *Notes*: one-prompt-template line.
10. `.claude/skills/aisa-options/SKILL.md` — same, plus: pack-file inputs corrected to pull-based, `solution-architect` excluded from Discovery cues, one architect-only prompt line (pack root), *Notes*: no-preload line.

**New**

11. `.claude/tests/test_council_wiring.py` — 31 tests.

**Not touched**: `library/**` (all kernel contracts and tools, and the whole PP pack — `pack.yaml`,
`question-bank.md`, `glossary.md`, `decision-tree.md`, `domain-knowledge/`), all 7 lens `SKILL.md`,
`.claude/agents/chairman.md`, `aisa-round`, `aisa-status`, `aisa-capture`, `aisa-start`, every hook,
`.claude/settings.json`, `docs/*`, and everything under `projects/`.

---

## 12. Deferred Phase F/G work

| Phase | Work |
|---|---|
| **F — state scaffold** | `aisa-start` SU `## Unknown` header gains `custo` + `swing` (D9); `_capture/` in the scaffold listing. `dashboard.py` maps by header name and tolerates absence, so the change is additive. |
| **G — PP cleanup** | Trim `extra_signals` to preferably 5–8 per Discovery lens under the survival test — the injected block is now observable in **both** loops (Discovery invocation and council preamble), which is the input to that decision; verify `question-bank.md` probe triggers are SU-observable; inspect `glossary.md`. |
| kernel touch-up | The single out-of-band edit in §9 (`orchestration.md`, question-bank consumer line). |

Not in scope and not started: evidence router, per-persona evidence bundles, new council machinery,
schema variants per persona, changes to chairman synthesis reasoning, PP pack content changes.

---

## 13. Anti-complexity result

| | Question | Verdict | Basis |
|---|---|---|---|
| A | New council subsystem introduced? | **NO** | no new file/skill/agent/config key/hook; one preamble section inside an existing skill, plus one test file |
| B | Persona-specific evidence routing introduced? | **NO** | one index for all; "do not rank, assign, summarize or bundle · no per-persona evidence view" in step 4b, "no evidence has been assigned to you" in the prompt, both asserted by test |
| C | Personas duplicate lens procedures? | **NO** | no execution steps, no signal catalog, no state semantics in any persona file (asserted) |
| D | Personas duplicate the common return schema? | **NO** | zero occurrences of any schema section across the 7 files (asserted); one copy, in the preamble |
| E | Personas require a full lens `SKILL.md` read? | **NO** | both prompts dropped the line; each persona states it does not read it (asserted both ways) |
| F | Council preloads full domain knowledge? | **NO** | orchestrators never read `decision-tree.md` / `domain-knowledge/`; architect pulls selectively; "Do not dump" in the preamble |
| G | Pack cues become coverage requirements? | **NO** | verbatim tokens + "cues, not a checklist; an uncovered cue is not a gap and never becomes an `Unknown`" |
| H | Independent reasoning preserved? | **YES** | parallel launch unchanged; no in-flight peer reads; read-only tool grant; dialectic round untouched |
| I | Persona perspectives remain distinct? | **YES** | seven distinct identities, each with its own *What you challenge* and bound concern (asserted) |
| J | Total council framework context reduced? | **YES** | per-persona framework text −37/−38%; whole round 49 320 → 31 140 (Framing) and 62 743 → 38 746 (Options); persona files −33% |

---

PHASE E — PERSONAS: PASS
ALL 7 PERSONAS RETAIN DISTINCT MANDATES: YES
PERSONAS REQUIRE FULL LENS SKILL READ: NO
COMMON COUNCIL MECHANICS CENTRALIZED: YES
COUNCIL USES SHARED EVIDENCE INDEX: YES
PERSONA-SPECIFIC EVIDENCE ROUTING INTRODUCED: NO
COMMON RETURN SCHEMA CENTRALIZED: YES
PACK CUES REMAIN ATTENTION CUES: YES
FRAMING TECHNOLOGY NEUTRALITY PRESERVED: YES
OPTIONS TECHNOLOGY REASONING PRESERVED: YES
CHAIRMAN COMPATIBILITY: PASS
TOTAL COUNCIL FRAMEWORK CONTEXT REDUCED: YES
PP PACK CONTENT MODIFIED: NO
READY FOR PHASE F — STATE SCAFFOLD: YES
