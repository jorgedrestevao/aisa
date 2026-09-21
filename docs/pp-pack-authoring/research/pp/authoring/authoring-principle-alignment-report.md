# Authoring Principle Alignment Report

<!--
provenance: ALIGNMENT (documentation only; no runtime file, no pack file modified)
date: 2026-09-04
scope: bounded semantic alignment ahead of PP Pack Authoring Step 3
basis: runtime-simplification-plan.md + pp-pack-authoring-map.md + docs/LENS_AUTHORING.md
not in scope: D1-D9, Runtime Simplification A-G, new research, Options re-authoring
-->

## 1. Semantic issue corrected

Runtime Simplification A–G is correct and stays. Its vocabulary — *framework text shrinks*, *lightweight lens*, *keep the lens output lightweight*, *evidence-light runtime*, indicative character targets — described **framework mechanics**, but nothing in the three governing documents said so explicitly. A later reader could have inferred that smaller output, a short mandate or an absent signal was a licence to reason less.

Three misreadings were possible and are now closed:

- **A — smaller means better.** Size figures could read as a target for analysis rather than for framework text.
- **B — selective means optional.** "Selective" could read as *ignore a material concern unless a signal triggers it*.
- **C — light means superficial.** Compact lens/persona files and the three-heading output block could read as instructions to stop reasoning early.

The correction is one distinction, stated in three places: **framework/mechanical context may shrink; analytical coverage may not.**

## 2. Authoritative principles established

Home: `pp-pack-authoring-map.md` §1.5 (integrated into the existing map — no separate principles framework).

1. Light framework, not lightweight reasoning.
2. Compress repetition, not decision coverage.
3. Broad coverage, selective depth.
4. Minimum sufficient complexity — the least framework complexity preserving materially complete, balanced, defensible reasoning; **not** the smallest number of rules, stages or criteria.
5. Research completeness is authoring input, not runtime payload.
6. Materiality determines depth.
7. Domain knowledge deepens a concrete decision question; it does not flood context pre-emptively.
8. Neutrality means an active technology pack must remain capable of concluding its own technology is not the best option.

Plus, in the same section: the **survival test** (a concern may not be compressed away when its omission could materially change viability · option class · architecture · security/control posture · governance · lifecycle/ALM · scale/performance · operability · cost/economics · risk · reversibility · preference · decision confidence), the **Discovery vs Options** completeness split, and **signals do not bound reasoning**.

## 3. Documents changed

| File | Change |
|---|---|
| `pp-pack-authoring-map.md` | new **§1.5 Authoring principles (binding from Step 3)**; new **Q-11** in §12 recording the Options material-coverage gap for Step 3A; one closing marker line |
| `runtime-simplification-plan.md` | new **§1.1 scope note** — what "simplification" means, attached to the four principles it clarifies; one closing marker line. No A–G content altered |
| `docs/LENS_AUTHORING.md` | new **Reasoning depth** subsection (signals do not bound reasoning · compact output ≠ shallow reasoning · materiality determines depth · a persona mandate is a focus, not a boundary); one pointer sentence on *Size*; one anti-pattern (*treating brevity as a stopping rule*) |

Nothing else was touched: no canonical research, no `pack.yaml`, no question bank, no glossary, no domain knowledge, no decision tree, no persona, no capture, no SU schema.

## 4. Runtime contradictions found

**0.** R1–R4 were checked against the current runtime, not re-audited repository-wide.

| # | Check | Finding |
|---|---|---|
| R1 | Lens prohibited from following a concern absent from its Signal Catalog | **No.** Every lens §5 reads *"Cues, not coverage: follow what is material here; an uncovered cue is not a gap"*; `orchestration.md` → *Pack context* states it for both cue sources; the per-signal coverage loop was deleted in Phase C |
| R2 | Lens must stop analysis to stay small | **No.** No size instruction exists in any lens file. Grep for `minimal / smallest / keep it short / limit your / stop analysis` across the 7 lens files, 7 personas and `orchestration.md` returns 0 relevant hits. The one brevity instruction (*keep the lens output lightweight*) governs the written block, and step 5 pushes the other way (*expose uncertainty rather than manufacture certainty*) |
| R3 | Persona prevented from following evidence outside its mandate | **No.** `Mandate per phase` bullets are enumerations with no closing clause; `orchestration.md` → *Persona boundary* defines a persona as perspective + mandate and removes only duplicated mechanics. No council prompt restricts scope (grep for `stay within / only consider / restrict your / limit your` = 0) |
| R4 | `aisa-status` can only ask questions already in the bank | **No.** The agenda is built from SU rows (step 6 a–c); the bank is consulted at 6d **to phrase**, and the degradation path builds the full agenda with no bank at all. `orchestration.md` → *Question bank* states the same role. The `P-<LENS>-NN` "only where the trigger is observed" clause restricts *bank probes*, not question formulation |
| R5 | Options reasoning bounded by a fixed list | **Yes — deferred by instruction.** See §7 |

No runtime instruction contradicts the new principles, so no smallest-semantic-correction was required.

## 5. Runtime changes

**None.** Documentation-only alignment. `.claude/skills/`, `.claude/agents/`, `.claude/hooks/`, `library/kernel/` and `library/packs/pp/` are unchanged by this pass.

## 6. A–G regression status

**No A–G outcome reversed.** All of the following stand unchanged: parse once / reason many · Capture-lite · shared evidence · `evidence-index.md` as source map · materiality-based selective raw verification · small lens runtime contracts · distinct lens perspectives · signals as attention cues · Discovery lenses pack-agnostic · `lens-technology` pack-aware in Options · question bank on-demand with one consumer · small council personas · centralized council mechanics · no duplicated state semantics · no weighted/scoring engines · PP Discovery `extra_signals` at 36 · simplified question bank · simplified glossary.

No PP runtime inflation: 0 signals added, 0 questions added, 0 glossary terms added, 0 lens or persona bytes added, no new mandatory Discovery checklist. The three edits add authoring documentation only — none of it is loaded at runtime.

## 7. Implication for Step 3A — Options decision model

Step 3A is the first stage where **broad coverage, selective depth** is a build requirement rather than a reading rule, because Options is where candidate choices are evaluated.

Carried in as **Q-11**:

> Today the Options layer bounds constraint evaluation to `lenses_config.technology.constraints_to_check` (5 entries for `pp`: `premium_licensing`, `dataflow_capacity`, `ALM_environments`, `dataverse_storage_quota`, `DLP_policy_compatibility`) plus the technology lens's 9-token signal catalog, and `lens-technology` execution step 2 emits *a verdict per constraint*. A material concern outside that fixed list can be silently omitted.

Direction for Step 3A — fix in the decision model (§9 S3/S8), **not** by patching the lens:

1. The constraint set becomes **materiality-driven**: the declared list is a floor, never a ceiling; a material concern raised by the engagement is evaluated whether or not it is declared.
2. Every serious option is considered against every **material** decision concern; depth varies by relevance, risk, uncertainty and consequence. Equal depth per option is not required; silent omission of a material concern is not permitted.
3. The survival test (§1.5) governs what may be compressed out of the decision procedure — gates G3/G8 already carry the mechanics to check it.
4. Principle 8 is a Step 3A acceptance condition: the authored model must be able to reach `Xp/Xr/Xe/Xc`, the `ALT` classes and `DECISION BLOCKED` on real inputs. Gate G5's 18-scenario replay is where that is proven.

Reasoning-example check (conceptual): **A** simple engagement — no framework mechanic forces analysis of immaterial concerns: PASS. **B** complex regulated engagement — no size or scope instruction caps depth: PASS. **C** concern outside every PP `extra_signal` — cue semantics are permissive in lens §5 and in `orchestration.md`: PASS. **D** complex Options decision — currently bounded by the fixed constraint list: the requirement is now stated; satisfying it is Step 3A's job.

---

`AUTHORING PRINCIPLE ALIGNMENT: PASS`
`LIGHT FRAMEWORK ≠ LIGHTWEIGHT REASONING: EXPLICIT`
`COMPRESS REPETITION, NOT DECISION COVERAGE: EXPLICIT`
`BROAD COVERAGE, SELECTIVE DEPTH: EXPLICIT`
`MINIMUM SUFFICIENT COMPLEXITY: DEFINED`
`SIGNALS BOUND REASONING: NO`
`OUTPUT COMPACTNESS BOUNDS ANALYTICAL DEPTH: NO`
`DISCOVERY CHECKLIST REGRESSION INTRODUCED: NO`
`OPTIONS MATERIAL-COVERAGE REQUIREMENT DEFINED: YES`
`CURRENT RUNTIME BEHAVIORAL CONTRADICTIONS FOUND: 0`
`A-G SIMPLIFICATION REVERSED: NO`
`PP RUNTIME INFLATED: NO`
`NEW RESEARCH REQUIRED: NO`
`READY FOR STEP 3A — OPTIONS DECISION MODEL: YES`
