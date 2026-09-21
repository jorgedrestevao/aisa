# Step 8C — Consolidated Post-Pilot Runtime Repair — pack pp 1.8.1 → 1.8.2

> One bounded runtime repair, decided in Step 8B (`step-8b-post-pilot-adjudication-report.md`) and its
> semantic-continuity addendum (`step-8b-addendum-semantic-continuity.md`). It implements PR-1, the
> consolidated Comprehension Survival Contract (PR-2A + PR-4 + PR-5 + proven PR-8 subsets), PR-7 and PR-6.
> PR-3 is deliberately **not** implemented. Steps 1–7 stay frozen; `projects/pricing-marinha/**` is untouched;
> Domain Knowledge is untouched.

**Verdict: `STEP 8C — CONSOLIDATED POST-PILOT RUNTIME REPAIR: PASS`** — full output block at the end.

---

## 1. Basis

| | |
|---|---|
| Baseline repaired | commit `78391d7ea00cc59c45b23ec65b384de8c812ab39`, branch `pp-pack-authoring/step-2-discovery-layer`, pack `pp` 1.8.1 |
| Inputs taken as established | Step 8B adjudication (PR-1 PROVEN-GENERIC; PR-2 → PR-2A DOCUMENTATION; PR-3 PRACTICE; TC-1..TC-5 designed) · Step 8B addendum (PR-4, PR-5, PR-7 PROVEN-GENERIC; PR-6, PR-8 DOCUMENTATION; Package C recommended; §60 one-source table) |
| Pilot-1 verdict | FAIL — preserved, unchanged |
| Steps 3–7 semantics reopened | **NO** — decision tree, 11 ALT classes, 12 concerns, S0–S9, 14 outcome classes, Domain Knowledge units, architecture templates / Step-5 schema, deliverable contracts, Estimate modes, render gaps, Step-6 projection semantics all untouched (their own suites: 95 + 64 + 116 + 218 + 97 tests, all green) |
| `projects/pricing-marinha/**` modified | **NO** — read only; the static proof (§15) runs on fixtures under `.claude/tests/fixtures/step8c/` |
| Domain Knowledge modified | **NO** — `git diff --stat -- library/packs/pp/domain-knowledge/` is empty |
| Pilot 1 replayed live | **NO** |
| Web research | **NO** |
| Library edit path | out-of-band shell edit (`cp` from scratchpad; Python patch script) + git commit — the sanctioned administrative path (`.claude/rules/library-readonly.md`); the `pre-write-guard` hook stayed in `enforce` throughout |

---

## 2. Files changed

Runtime (7 skills + 2 kernel + manifest):

| File | Change | Repair |
|---|---|---|
| `library/kernel/capture-templates/process-model.template.md` | `sources` gains `evidence-index.md` + `*.text.md`; `synthesis_prompt` rewritten (cross-source, source-complete in coverage, markers, depth = materiality + uncertainty + consequence); §4 becomes **Process synopsis (cross-source)** with the reasoning dimensions, OBSERVED/INFERRED/HYPOTHESIS/UNKNOWN marking, projection rules, backticked labels for material lines, output lineage, genuine-vs-accidental as HYPOTHESIS; §6 names the incoherence shapes and the disposition obligation; §7 names unavailable text sources | PR-4 / PR-8 |
| `library/kernel/orchestration.md` | Capture tiers: L2 reads all normalized evidence (replaces "stays scoped to `.xlsx`/`.xlsm`"); new section **Comprehension survival — what must not be silently lost** (doctrine shorthand, the class table, disposition, fact ≠ fit, targeted revalidation, phase ≠ session) | doctrine, PR-2A/4/5/8, PR-1, PR-7, PR-6 |
| `library/packs/pp/pack.yaml` | `pack_version: 1.8.2` + header block naming the repair | version |
| `.claude/skills/aisa-capture/SKILL.md` | step 5 → cross-source L2 (5a2 selective source-complete comprehension, USED/CHECKED/TARGETED, no size targets); 5b runs before 5; log/output carry dispositions and marker counts; hard rules 1, 5 widened; new hard rules 9 (synopsis is evidence, not authority) and 10 (cross-source ≠ full preload); degradation row for unavailable text sources | PR-4 |
| `.claude/skills/aisa-round/SKILL.md` | step 4b context gains the **Comprehension survival** line (MAP / ADOPT / DISMISS, markers ≠ states, Critical PM-U never disappears); step 5e disposition bookkeeping (string presence only; `undisposed` reported, never disposed by the orchestrator); note *Disposition is projection, not resolution* | PR-2A |
| `.claude/skills/chairman-synthesis/SKILL.md` | Inputs gain the synopsis; council preamble gains the synopsis pointer; Step 3 rule (HYPOTHESIS never becomes Confirmed/Assumed); Framing template gains **## What must survive into Options** (5 id-anchored sub-lists) + its rules (ID-anchored or explicit Unknown · SU first, then project · `(none) — reason` · generic/technology-neutral · no product-licensing question · HYPOTHESIS never as fact) | PR-5 |
| `.claude/skills/aisa-frame/SKILL.md` | Inputs gain synopsis + `Open evidence` blocks; step 2 soft gate gains the **Comprehension survival test** (7 questions incl. disposition completeness, no score; failure names the concrete missing understanding; override reason → `(none) — reason`); step 7 displays the survival block; note *projection, not a second truth* | PR-5, §20–21 |
| `.claude/skills/aisa-answer/SKILL.md` | step 4 **Verbatim boundary**; new step 4b **Architecture-significant technical claims — fact ≠ fit** (trigger, settle-the-named-fact, closure basis A/B/C, capability ≠ fit); step 7 **Targeted revalidation**; output line; hard rules 7–8 | PR-1, PR-7 |
| `.claude/skills/aisa-blueprint/SKILL.md` | step 11 **Closing a structural choice — fact ≠ fit**; new step 11b **Cross-field architecture change — targeted revalidation**; step 13 log carries the revalidation list + closure basis; step 15 blocks approval on an unbased closure; output line; hard rules 7–8 | PR-1, PR-7 |
| `.claude/skills/aisa-status/SKILL.md` | step 6e **Process teach-back** (materiality-triggered `reuniao` item, Unknowns keep identity); step 8b **Derive the `Read to resume` set** (phase table, PHASE ≠ SESSION, computed not persisted, selective); output template gains both | §22–23, PR-6 |

Documentation / tests:

| File | Change |
|---|---|
| `CLAUDE.md` | principle 10 (the shorthand doctrine) |
| `docs/ARCHITECTURE.md` | changelog v3.3.0; principle 10; new §3.5 *Fase ≠ Sessão — rehidratação selectiva*; `/capture` and `/resume` rows |
| `docs/PHILOSOPHY.md` | one "o que aisa não é" bullet: no deterministic cognition; determinism governs survival |
| `docs/PROCESS_CAPTURE_SPEC.md` | Step 8C note: L2 is cross-source; §6 kept as historical MVP shape |
| `docs/pp-pack-authoring/pilot/step-8b-post-pilot-adjudication-report.md` | §0 corrections (§3 below) — §9 note, new §20a, three final-block lines |
| `docs/pp-pack-authoring/pilot/pilot-2-protocol.md` | **new** — fresh-session adversarial test + carried watch items (PR-3 first) |
| `.claude/tests/test_step8c_semantic_continuity.py` | **new** — 58 tests: TC, CS, PMU, FS, SI + C-057, RH, pricing-marinha static proof, guards |
| `.claude/tests/fixtures/step8c/*` | **new** — 10 fixtures + README (synopsis, PM-U, SU excerpt, open-evidence dispositions, frame survival block, C-057 blueprint v01 / v02 / v03-defect, decisions and options excerpts) |

Not changed although listed as candidates: none of the listed files was left unchanged — each carried one of the repairs. Not touched: `aisa-options`, the six lens skills, every agent file, every hook, every Domain Knowledge unit, every architecture and deliverable template, `states.md`, `phases.md`, `blueprint-contract.md`, `render-contract.md`.

Diff size (tracked runtime + docs): 14 files, +320 / −44 lines.

---

## 3. Step 8B final corrections

Applied first (`step-8b-post-pilot-adjudication-report.md` §9 note, §20a, final block):

```text
SPECIFIC SQL ACCESS MECHANISM IDENTIFIED: NO
MODEL-DRIVEN + EXTERNAL SQL CAN BE DEFENSIBLE WITH PRECONDITIONS: YES
A-009 FINAL STATUS: UNKNOWN
```

Reason recorded in §20a: the research identified supported **candidate** mechanisms (M1–M4); the engagement
did **not** establish which mechanism is used per data domain, nor its fit. `candidate mechanism exists` ≠
`engagement mechanism established`. The original lines are preserved as history; §18's disposition
(TARGETED-ARCHITECTURE-REVISIT) is unchanged and now starts from `UNKNOWN`. Guard test:
`Guards.test_step_8b_final_corrections_recorded`.

---

## 4. Governing doctrine

Added only where the existing guidance owns it — `orchestration.md` (kernel contract), `ARCHITECTURE.md` §2
principle 10 and §3.5, `PHILOSOPHY.md` ("o que aisa não é"), `CLAUDE.md` principle 10:

```text
reason deeply → persist selectively → claim conservatively → rehydrate selectively → revalidate when premises change
```

Determinism governs what must survive, what authority owns it, what may not be silently promoted or dropped,
what must be revalidated, and what a fresh session must reload. No internal reasoning sequence is prescribed
anywhere (guard: `Guards.test_doctrine_lives_where_guidance_owns_it` asserts the shorthand and the absence of
a "reasoning sequence" clause). The OBSERVED/INFERRED/HYPOTHESIS/UNKNOWN marking constrains how a conclusion
is **labelled when persisted**, not how it is reached.

---

## 5. PR-1 — technical-claim closure enforcement

Implemented as R-A + R-B from Step 8B §17.3, in the two files where the Pilot-1 chain slipped:

- **`aisa-answer` step 4 + 4b.** Verbatim boundary (the Confirmed claim may not exceed the answer; runtime
  inference → separate Assumed with basis, or Unknown / verification obligation; second-hand configuration
  statements → Assumed until the accountable owner confirms). Trigger = the row is the `su_ref` of a
  structural open choice **or** the claim would settle / materially support a structural architecture
  conclusion — explicitly *not* merely `validade: plataforma-tecnica` on an unrelated fact (§25 of the brief).
  Settle the named fact: `would_be_settled_by` = mechanism + fit and the answer = connection exists →
  engagement fact recorded, structural choice stays open (§27). Closure basis A / B / C, else open (§28). No
  automatic web lookup, no three-source rule, no DK preload.
- **`aisa-blueprint` step 11 / 13 / 15.** A structural choice may be marked resolved only when the basis
  settles the fact its `would_be_settled_by` named **and** is A / B / C. Fact ≠ fit; capability confirmed ≠
  fit confirmed (TC-5); tenant/configuration-dependent values need B or C (TC-4); over an external store the
  mechanism per data domain is named and `access_mode` / `pattern` follow it, never connectivity. Approval
  stays blocked on an unbased closure; the log records the closure basis.

TC-1..TC-5 (§17.4 of 8B) are encoded in a reference evaluator (`closure_verdict`) plus contract assertions;
the Pilot-1 defect shape (fixture `c057-blueprint-v03-defect.yaml`: surface "confirmed" on a gateway answer,
`keep-in-place` + `direct`, rationale still "audit inherited from the store") is rejected by
`structural_closure_defects`, and the corrected shape (`c057-blueprint-v02.yaml`) is accepted. **5/5 PASS**
(`TC_TechnicalClaimClosure`, 8 tests).

---

## 6. Cross-source comprehension

The three contract statements that scoped L2 to the workbook are removed (`aisa-capture` *Supported formats*
and step 5; `process-model.template.md` `synthesis_prompt`; `orchestration.md` *Capture tiers*). L2 now reads
extraction JSON + replay + `*.text.md`, selected through `evidence-index.md`. LT stays extraction-only
(hard rule 7 untouched). Binding rule, in the kernel and the skill: **source-complete in coverage, not
source-total in simultaneous context.** An engagement with text sources and no workbook still gets an L2 pass.
Guard: `CS_ComprehensionSurvival.test_contract_L2_reads_all_normalized_evidence`.

---

## 7. Selective evidence loading

`aisa-capture` step 5a2: inspect the index → identify materially process-bearing sources/sections → read
compact process documents in full where appropriate → pull targeted transcript passages → give **every**
process-bearing source a disposition → reconstruct across sources. Dispositions `USED` / `CHECKED` /
`TARGETED (<locators>)` are recorded in the model header and the existing `_capture-log.md` L2 line — no new
register (§5 of the brief). No maximum source count, KB budget or transcript-length threshold (§6): the
contract is *enough evidence inspected to reconstruct the material process*. A `CHECKED` source must have been
inspected (hard rule 10); an unavailable source is `CHECKED — unavailable (<status>)` and its semantics are
`UNKNOWN` lines where material (degradation table).

---

## 8. Process synopsis

`process-model.md` §4 → **Process synopsis (cross-source)**: the durable process-comprehension carrier, richer
than the SU, never authoritative over it (§3 of the brief). Reasoning dimensions offered, none mandatory:
purpose · end-to-end flow · actors · inputs · transformation/calculation stages · intermediate state ·
decisions · outputs and consumers · variants · exceptions and workarounds · business invariants · structural
constraints · material user tasks · genuine vs accidental complexity · material unresolved semantics. "An
irrelevant dimension gets no heading, never an empty one." Every line: marker + citation (PM id, cell/range
or text locator). Material lines carry a short backticked **label** so a lens can name what it disposed of —
a naming convention, not a new id namespace. Calculation lineage `input → transformation → intermediate →
transformation → output → consumer` at the depth **materiality + uncertainty + consequence** warrant — stages,
never formula-by-formula (§9). Every material output family is traced or its missing link is `UNKNOWN`; no
silent disappearance (§10). Repeated workbook structure is never converted automatically into a repeated
business requirement; the genuine/accidental split stays `HYPOTHESIS` unless evidenced (§11). Markers project
as OBSERVED → Confirmed (with evidence) · INFERRED → Assumed with basis · HYPOTHESIS → stays or projects as
the Unknown that would settle it · UNKNOWN → Unknown; they are **not** engagement states (§8; guard
`Guards.test_no_new_epistemic_state`). Technology-neutral (guard: no vendor term in the template).

---

## 9. Semantic disposition

The widened PR-2A rule, carried by `aisa-round` (one line in the round context, one bookkeeping step) and the
kernel: at the Discovery projection boundary every material synopsis line (output family, transformation
obligation, invariant, user task, exception, structural constraint) and every `PM-U` row receives **exactly
one** disposition in the lens's `Open evidence` block — `MAP <SU id>` · `ADOPT → <new id>` · `DISMISS —
<reason>`. No silent fourth outcome (§12). The orchestrator checks *presence* (string), never *which*:
`aisa-round` step 5e reports `undisposed`; `/frame`'s gate reads the same list (question 7). Critical PM-U:
MAP / ADOPT / DISMISS with materiality reason; adoption does not require resolution — an adopted Critical
PM-U may stay `Unknown` (§13). SU remains the authority; the synopsis is never copied into it (§14): rich
reconstruction → selective material projection → compact SU. Fixture proof: the pricing-marinha synopsis
(37 marked lines, 32 labelled) and 11 PM-U rows are fully disposed by four lenses' `Open evidence` blocks;
removing the `Outputs BIOS` disposition or the `PM-U-002` line makes the evaluator report them (CS-5,
PMU-4). **PMU-1..PMU-5: 5/5 PASS** (`PMU_Disposition`, 6 tests).

---

## 10. Business invariants

Existing semantics, no state, no field (§15): an invariant is a `Confirmed`/`Assumed` row whose claim is a
behaviour that must remain valid regardless of the solution. The synopsis lists candidates under *Business
invariants*; the disposition step projects them; `frame.md` names their ids. Examples stay engagement-specific
(the kernel table gives the definition, the fixture gives instances such as "Mon/Tue pricing must remain
possible with incomplete quotes") — nothing hard-coded into runtime logic.

---

## 11. Structural constraints

Definition adopted verbatim from the addendum (§16): a confirmed or unresolved condition whose truth could
materially eliminate, reshape or gate whole solution classes. Placement: Discovery/Framing identify
generically → Options evaluate candidate consequence → Architecture implements the response. Represented as
`Confirmed` rows or `Unknown` rows with `swing: decisivo` — no new state, no register. Licensing/entitlement
boundary (§17): user population / identity class, existing entitlement boundary and willingness to acquire
incremental entitlement are pre-Options; candidate-specific entitlement is Options; exact composition is
Architecture; no product-licensing question pre-Options because the active pack is PP (stated in the kernel
section and the chairman rules; guard `Guards.test_no_product_licensing_question_pre_options`).

---

## 12. Framing survival

`chairman-synthesis` Framing template gains **## What must survive into Options** with five sub-lists —
process meaning · business invariants · structural constraints · decision-changing Unknowns · material scope
/ task obligations. Every entry is an SU id (or explicit Unknown) plus one line; `(none) — <reason>` is valid;
an empty sub-list is not. The block is a projection: no free-text truth; a missing material item is written to
the SU first (Step 5) and projected second (§18–19). `aisa-frame` step 7 displays it; step 2 runs the
pre-Options comprehension survival test (§20 — six questions + disposition completeness, no score) with the
failure behaviour of §21: name the concrete missing understanding (`output X has no identified consumer`,
`material calculation chain Y is not reconstructed`, `structural question Z is still absent`), route it through
`/round <lens>` or `/answer`, never manufacture certainty; logged override stays possible and its reason
becomes the `(none) — reason` entry *(as first written — this last clause was the defect the freeze review
found; corrected in §23, Step 8C.1: an override never produces `(none)`, the gap stays projected as its id)*.
Fixture evaluator `survival_defects`: FS-1 invariant id-anchored (C-073);
FS-2 constraints id-anchored (C-013, C-036, C-028, C-052, U-035); FS-3 decision-changing Unknowns visible
(U-028, U-032); FS-4 `(none) — reason` valid, empty sub-list invalid; FS-5 an invented `C-099` and an
unanchored free-text constraint are defects. **FS-1..FS-5 PASS** (`FS_FramingSurvival`, 6 tests).

---

## 13. Teach-back

`aisa-status` step 6e: materiality-triggered, never mandatory. When the synopsis carries a material
`HYPOTHESIS` / `UNKNOWN` about an output family, transformation, consumer, invariant or process shape — or an
adopted Critical PM-U is still open — the related Unknowns are grouped into **one** `reuniao` agenda item.
Every underlying Unknown keeps its own identity and closure criterion and transitions independently via
`/answer <id>`; no "process confirmed" collapse row (§22–23). Guard:
`Guards.test_teach_back_groups_without_collapsing`.

---

## 14. PR-7 — targeted semantic revalidation

Two extensions of existing steps, no graph, no registry, no `depends_on`, no template field (§30–31):

- **`aisa-answer` step 7.** When the new fact contradicts or materially changes a premise downstream used:
  grep the resolved id and the fact's subject across `frame.md`, `options.md`, `decisions.md`,
  `_blueprint/*.yaml` (`su_refs`, `forced_by`, `would_be_settled_by`, rationale), `_synthesis/*`; write one
  line per dependent — `still valid — why` / `revalidate — what it assumed`; `(none)` for unrelated facts.
  Decision-layer dependents → tripwire check → `/revisit` (§33); the Decision is never rewritten.
- **`aisa-blueprint` step 11b.** When an architecture-significant field changes value (record authority,
  access mode, composition pattern, experience mode/surface, security/control boundary, integration
  mechanism) the executor asks *which existing conclusions were materially based on the previous value?* and
  records them in `blueprint-log.md`, `open_architecture_choices` (structural where evidence is insufficient)
  and `proof_obligations` (§32). No automatic reversal: the new fact makes a conclusion *not settled*, not
  false.

SI-1..SI-5 use a reference evaluator that finds dependents only through existing references — `su_refs`
overlap, rationale/`forced_by` prose naming the field's property ("audit inherited from the store"), option
strengths and decision clauses sharing that vocabulary. SI-1 lists security, audit, access, composition and
surface; SI-2 (a terminology correction) lists nothing; SI-3 routes to `tripwire check → /revisit` and leaves
`decisions.md` untouched; SI-4 catches the prose dependence although `experience.su_refs` never named the store
rows — with no schema field (`depends_on` absent from `aisa-blueprint` and the fixtures); SI-5 flags the
defect version where the premise changed and the rationale stayed settled. **SI-1..SI-5 PASS**
(`SI_SemanticInvalidation`, 7 tests incl. C-057).

---

## 15. C-057 regression

Fixture pair `c057-blueprint-v01.yaml` → `c057-blueprint-v02.yaml` reproduces the semantic shape: governed
store owned ×3 with a surface rationale "row/column security and audit inherited from the governed store" →
new fact: external record authority. Expected and asserted: record authority changes for the three domains;
security / audit / access / composition / surface implications are listed; **no automatic reversal** (the
surface value is unchanged and the surface choice is `structural: true`, `would_be_settled_by` = mechanism per
domain **and** fit, "Connectivity alone does not settle it"); ≥3 structural choices remain open (surface,
audit mechanism, authorization enforcement point); the decision layer (O-004 strengths, D-002 auditability
clause) routes to `/revisit`. The Pilot-1 v03 shape is the negative control (rejected in TC and SI-5).
**C-057 REVALIDATION FIXTURE: PASS.**

---

## 16. PR-6 — rehydration

`aisa-status` step 8b derives a **`Read to resume (<phase>)`** block from `_state.json.phase` and the file
system — computed on every run, never persisted, not a new authority, not a handoff summary (§35). The phase
table lists only what the phase materially needs (phase authority + SU material rows + synopsis where
relevant + current phase artefact + targeted pulls) and names what is never default reading (raw evidence,
transcripts, lens outputs of other rounds, Domain Knowledge) (§37). **PHASE ≠ SESSION** documented in the
kernel, `ARCHITECTURE.md` §3.5 and the skill (§36). `/resume` needs no change — it already delegates to
`aisa-status`. RH-1..RH-5 run a reference derivation over temp engagement folders: phase derivable; current
authorities present; no transcript/conversation item; no handoff artefact anywhere in the runtime (and no skill
directory named like one); detailed process evidence absent from the default set, synopsis present only when
`process-model.md` exists. **RH-1..RH-5: 5/5 PASS** (`RH_Rehydration`, 6 tests). The live fresh-session test
is in the Pilot-2 protocol (§38 of the brief; `pilot-2-protocol.md` §2).

---

## 17. PR-3 — explicitly NOT implemented

`aisa-blueprint` steps 3–4 are unchanged: no task matrix, no "each screen names the task it serves", no
mandatory interaction-shape evaluation (guard `Guards.test_PR3_not_implemented` asserts the absence and that
step 4 still compiles entities from `lens=data` rows and personas from `lens=user` rows). Reason (§39): Pilot 1
proved the interaction shape was missed; it did not prove the architecture contract lacks a generic rule. PR-4
now makes material user tasks available in the synopsis and, through disposition, in the SU. Pilot 2 decides
whether Architecture uses them naturally. If the omission recurs, the smallest existing-contract strengthening
is evaluated then (`pilot-2-protocol.md` §3, first row). No mockup solution presumption was encoded (§40;
guard `test_no_mockup_solution_presumption`).

---

## 18. New fixtures and tests

`.claude/tests/test_step8c_semantic_continuity.py` — 58 tests in 8 groups:

| Group | Tests | What is proven |
|---|---|---|
| `TC_TechnicalClaimClosure` | 8 | contract in `aisa-answer` / `aisa-blueprint`; TC-1..TC-5 via `closure_verdict`; Pilot-1 defect shape rejected, corrected shape accepted |
| `CS_ComprehensionSurvival` | 9 | L2 cross-source contract; synopsis dimensions/markers; CS-1 cross-source flow; CS-2 documentary output family survives + Unknown consumer; CS-3 chain as stages, no formulas; CS-4 genuine/accidental as HYPOTHESIS; CS-5 undisposed line → FAIL; dispositions point at existing rows; round/frame contract |
| `PMU_Disposition` | 6 | PMU-1 MAP · PMU-2 ADOPT · PMU-3 DISMISS needs a reason · PMU-4 silent Critical → FAIL (Med/Low is lens judgement) · PMU-5 adopted Critical may stay Unknown · all 6 Critical rows disposed |
| `FS_FramingSurvival` | 6 | chairman template + rules; FS-1..FS-5 |
| `SI_SemanticInvalidation` | 7 | contract; SI-1..SI-5; C-057 regression |
| `RH_Rehydration` | 6 | contract; RH-1..RH-5 |
| `PricingMarinhaStaticProof` | 5 | engagement untouched; chain / four units / BIOS / Simulador / Mon-Tue survive to SU and frame; structural constraints visible pre-Options incl. "where must pricing data live" as `swing: decisivo`; incomplete-input behaviour is an invariant and a decision-changing Unknown, not only an exposure; synopsis technology-neutral |
| `Guards` | 11 | pack 1.8.2; 5 states; 4 phases; 8 agents; no graph/matrix/`depends_on`; no `process-understanding.md`; PR-3 absent; no mockup presumption; parse-once preserved; no product-licensing question pre-Options; teach-back does not collapse; doctrine placement; Step 8B corrections recorded |

Fixtures (`.claude/tests/fixtures/step8c/`, 10 + README): a static re-capture of the Pilot-1 evidence in the
1.8.2 shape — synopsis (37 marked lines across workbook, two documents and two transcripts), PM-U table,
SU excerpt (engagement ids + the rows the disposition step would have adopted, `C-070+`, `U-032+`, `A-010`,
`X-007`), four lenses' `Open evidence` dispositions, the frame survival block, C-057 blueprint v01 / v02 /
v03-defect, decisions and options excerpts. The reference evaluators are test instruments written from the
contract; no runtime router, scorer or ledger exists.

---

## 19. Full regression

```text
python -m unittest discover -s .claude/tests -p "test_*.py"
Ran 739 tests — OK (0 failures, 0 errors)
```

| Module | Tests | Result |
|---|---|---|
| `test_council_wiring.py` | 31 | OK |
| `test_orchestrator_wiring.py` (answer/state/orchestration wiring) | 23 | OK |
| `test_state_scaffold.py` | 15 | OK |
| `test_pp_discovery_runtime.py` (Discovery) | 22 | OK |
| `test_pp_options_decision_model.py` (**Step 3**) | 95 | OK |
| `test_pp_domain_knowledge.py` (**Step 4**) | 64 | OK |
| `test_pp_architecture_templates.py` (**Step 5**) | 116 | OK |
| `test_pp_deliverable_templates.py` (**Step 6**) | 218 | OK |
| `test_pp_pack_integrity.py` (**Step 7 integrity**) | 97 | OK |
| `test_step8c_semantic_continuity.py` (**Step 8C**) | 58 | OK |
| **Total** | **739** | **0 failures** |

Baseline before the repair: 681 tests, OK. Pilot 1 was not replayed as a live engagement.

---

## 20. Version and checkpoint

`pack_version: 1.8.1 → 1.8.2` — *Pilot-1 bounded semantic-continuity enforcement repair: technical-claim
closure, deep process comprehension survival, structural-constraint projection, targeted semantic revalidation
and selective session rehydration.* Not 1.9.0: no semantic model change.

```text
RUNTIME REPAIR COMMIT: b26f39126d930ddf0ebf61cb5f274cb70f73f2d8
STEP 8C CHECKPOINT COMMIT: the commit `step-8c-baseline` resolves to — see §23 (Step 8C.1 freeze correction)
STEP 8C CHECKPOINT TAG: step-8c-baseline → `git rev-parse step-8c-baseline^{commit}`
PACK VERSION: 1.8.2
RUNTIME TREE: clean — the only untracked files are unrelated non-runtime files, listed explicitly:
  2026-09-03.md, Untitled.canvas (stray Obsidian files at the repo root, deliberately uncommitted)
  docs/FRAMEWORK-NEGOCIO.md (user document, unrelated to the runtime, deliberately uncommitted)
```

*(History: as first written this block called the repair SHA `STEP 8C BASELINE COMMIT` and pointed the tag at a
docs-only recording commit, `a6d617bda5fa2c5ae7588f275b120a2f260bbb29`. The freeze review flagged the
ambiguity; §23 records the corrected identity. That recording commit stays in history and is no longer tagged.)*

Pilot 2 and the pricing-marinha targeted architecture revisit start from the commit tagged `step-8c-baseline`.

---

## 21. Remaining Pilot-2 watch items

From `pilot-2-protocol.md` §3: **PR-3** surface/task derivation (first); unverified technical claims reaching
`Confirmed` or closing a structural choice anywhere; the deliverable consumer tests never exercised in Pilot 1
(sponsor Executive-Report read, architecture handoff, implementation handoff, independent Estimate comparison);
`solution_name` / A8 / A9 recurrence; cross-source synopsis cost and honest source dispositions; disposition
burden; teach-back trigger and independent closure; targeted revalidation written (`still valid` /
`revalidate` / `(none)`) rather than silent carry-forward or wholesale rerun. Plus the fresh-session
adversarial test (§2 of the protocol) — Session A closes Discovery, Session B starts with no transcript and
only the derived `Read to resume` set; record lost concepts, invented concepts, raw-source rereads,
unnecessary context.

---

## 22. Final verdict

The repair is one contract (comprehension survival), one enforcement (fact ≠ fit at the two closure points),
one obligation (targeted revalidation through existing references), one derived output (`Read to resume`) and
doctrine text — spread over seven skills, one template, one kernel section and the manifest version. Nothing
new was added to the model: no artefact, phase, agent, state, graph, matrix, handoff file, router, ledger or
scoring model. The static proof shows that, on the Pilot-1 evidence shape, the chain, the four-unit output
family, `Outputs BIOS`, the Simulador's what-if role and the Monday/Tuesday behaviour now reach the SU and the
frame with dispositions, that the invisible structural constraint becomes an explicit decision-changing
Unknown, and that C-057 lists its dependents for revalidation instead of closing the surface on a gateway
answer. Claude's reasoning is not constrained by any of it; its understanding now has to become state before it
is compressed, reloaded or built on.

```text
STEP 8C — CONSOLIDATED POST-PILOT RUNTIME REPAIR: PASS
PR-1 TECHNICAL-CLAIM ENFORCEMENT: PASS
TC-1...TC-5: 5/5
COMPREHENSION-SURVIVAL CONTRACT: PASS
L2 CROSS-SOURCE COMPREHENSION: PASS
L2 REQUIRES FULL SIMULTANEOUS SOURCE PRELOAD: NO
NEW PROCESS-COMPREHENSION ARTEFACT: NO
MATERIAL SYNOPSIS SEMANTICS REQUIRE DISPOSITION: YES
CRITICAL PM-U MAY DISAPPEAR SILENTLY: NO
PMU-1...PMU-5: 5/5
FRAMING SURVIVAL BLOCK: PASS
FRAMING MAY CREATE NEW FACTUAL AUTHORITY: NO
STRUCTURAL CONSTRAINT REQUIRES NEW STATE: NO
SPECIFIC PRODUCT LICENSING QUESTION PRE-OPTIONS: NO
TEACH-BACK MAY GROUP QUESTIONS WITHOUT COLLAPSING UNKNOWNS: YES
PR-7 TARGETED SEMANTIC REVALIDATION: PASS
NEW DEPENDENCY GRAPH: NO
NEW ARCHITECTURE DEPENDS_ON FIELD: NO
C-057 REVALIDATION FIXTURE: PASS
PR-6 SELECTIVE SESSION REHYDRATION: PASS
PREVIOUS CHAT TRANSCRIPT REQUIRED: NO
NEW SESSION-HANDOFF ARTEFACT: NO
FRESH-SESSION FIXTURES: 5/5
PR-3 SURFACE/TASK RUNTIME RULE IMPLEMENTED: NO
PARSE-ONCE BOUNDARY PRESERVED: YES
NEW STATE INTRODUCED: NO
NEW ROUTER INTRODUCED: NO
DOMAIN KNOWLEDGE MODIFIED: NO
STEP 3 REGRESSION: PASS
STEP 4 REGRESSION: PASS
STEP 5 REGRESSION: PASS
STEP 6 REGRESSION: PASS
STEP 7 INTEGRITY: PASS
FULL REGRESSION TESTS: 739
FULL REGRESSION FAILURES: 0
PACK VERSION: 1.8.2
RUNTIME REPAIR COMMIT: b26f39126d930ddf0ebf61cb5f274cb70f73f2d8
STEP 8C CHECKPOINT COMMIT: see §23 — the commit tagged step-8c-baseline (Step 8C.1 included)
READY FOR PRICING-MARINHA TARGETED ARCHITECTURE REVISIT: YES
READY FOR PILOT 2: YES
```

*(The Step 8C block above is preserved as written on 2026-09-05, except its checkpoint-identity line, which
was ambiguous and is restated in §23.)*

---

## 23. Step 8C.1 — freeze correction

```text
initial Step 8C PASS (§22)
→ freeze review found an override-masking edge case in the Framing survival gate
→ Step 8C.1 bounded correction (this section)
→ regression: Step 8C module 64 tests, full suite 745 tests, 0 failures
→ final freeze verdict: PASS — Step 8C FROZEN
```

Not a new repair scope. Nothing changed in PR-1, comprehension-survival, PR-7 or PR-6 semantics, PR-3 status
(still `PILOT-2-WATCH`), Steps 3–7, Domain Knowledge, the architecture schema or the pack version (`1.8.2`).

### 23.1 The defect

`aisa-frame` step 2 (as written in Step 8C) said: *"An override of the comprehension survival test names the
failing question(s) in the reason; the chairman then writes the corresponding survival-block entry as
`(none) — <the logged reason>`."* That let a soft-gate override **erase** a semantic gap: a material output
family with an Unknown consumer, a failed pre-Options test and a logged reason would have produced
`Material scope / task obligations: (none) — overridden to proceed` — an override standing in for absence.

### 23.2 The correction (two files, one evaluator)

| File | Change |
|---|---|
| `.claude/skills/aisa-frame/SKILL.md` step 2 | Binding rule **override ≠ evidence · ≠ resolution · ≠ absence** — an override changes whether execution may proceed, never what is known. The gate output records `gate: FAIL · missing understanding: <category> — <specific gap> · override: YES · override reason · proceed: allowed under existing soft-gate doctrine`; the reason goes where it already goes (`decisions.md` D-001 `Override used at /frame` — the existing soft-gate record, no new field). The missing item stays visible as an SU `Unknown` (written first through the authority model if absent), an unresolved material trace or an `undisposed` line, and the chairman projects **that id**. `(none) — <reason>` is reserved for the substantive conclusion that no material item of the class exists. Step 7 display gains the gate line. |
| `.claude/skills/chairman-synthesis/SKILL.md` survival-block rules | `(none) — <reason>` valid **only** as a substantive conclusion and only when (1) the category was evaluated, (2) no known material SU item belongs to it, (3) no material synopsis line requiring disposition is unresolved for it, (4) no gate failure on it is hidden by the entry. New rule *Override ≠ evidence, ≠ resolution, ≠ absence*: a category with a known unresolved gap carries the gap's id, never `(none) — <override reason>`; the override lives in D-001, not in the block. Template intro tightened. Five sub-lists unchanged; no `### Gate override` heading. |
| `.claude/tests/test_step8c_semantic_continuity.py` | Evaluator `none_entry_defects` / `survival_defects_full` (the four conditions + a lexical guard against override wording in a `(none)` reason; gate record parsed from the existing gate output and D-001 line). New class `FS6_OverrideCannotMaskMissingUnderstanding` (6 tests). |

Genuine NONE remains valid:

```text
Structural constraints:
(none) — no constraint has been identified that materially eliminates or reshapes solution classes.
```

Override with an open gap — the honest shape:

```text
Material scope / task obligations:
U-033 — consumer/use of the `Outputs BIOS` output family remains unresolved

decisions.md#D-001 · Override used at /frame: <reason>      (gate: FAIL · override: YES · proceed: allowed)
```

### 23.3 FS-6 — override cannot mask missing understanding

Input: material output family (`Outputs BIOS`, C-071) + consumer Unknown (U-033) + pre-Options survival test
FAIL on *Material scope / task obligations* + override reason supplied + frame writes `(none) — overridden to
proceed` → **FAIL** (three defects: known material items exist · `(none)` hides a gate failure naming U-033 ·
override wording used as a `(none)` reason). Correct shape — the fixture frame names U-033 and the override is
recorded in D-001 — → **PASS**, with the gate record still reading `FAIL / override: YES`: the override did not
change what is known. The same evaluator runs over all five categories (`test_FS6_generic_over_all_five_categories`)
with a masked `(none)` per category → FAIL each time, honest shape → PASS each time. Genuine `(none)` on a
category whose synopsis dimension is absent, whose SU has no item and whose gate passed → valid; the same
wording with an override behind it, or with the dimension still present, → FAIL. An override never transitions
the Unknown (U-033 stays open, unmarked, projected). One generic evaluator, no per-category runtime rule.

**FS-1..FS-6: 6/6 PASS.** Step 8C module: 64 tests (58 + 6). Full suite: **745 tests, 0 failures**.

### 23.4 Checkpoint identity (definitive)

```text
RUNTIME REPAIR COMMIT:        b26f39126d930ddf0ebf61cb5f274cb70f73f2d8   (Step 8C runtime repair, pack 1.8.2)
STEP 8C.1 CORRECTION COMMIT:  the commit this section is committed in — it IS the checkpoint
STEP 8C CHECKPOINT COMMIT:    git rev-parse step-8c-baseline^{commit}
STEP 8C CHECKPOINT TAG:       step-8c-baseline → that commit (lightweight tag; moved from the superseded
                              docs-only recording commit a6d617bda5fa2c5ae7588f275b120a2f260bbb29)
```

A commit cannot carry its own SHA in its tree, so the checkpoint SHA is recorded by the tag itself and in the
Step 8C.1 final output block; it is **not** a further docs-only commit — the tag, the report and the runtime
tree are the same commit. Pilot 2 (`pilot-2-protocol.md`) and the pricing-marinha targeted architecture
revisit start from `step-8c-baseline`.

```text
RUNTIME TREE: clean
untracked, unrelated, listed exactly as before: 2026-09-03.md · Untitled.canvas · docs/FRAMEWORK-NEGOCIO.md
```

### 23.5 Final freeze verdict

```text
STEP 8C.1 — FREEZE CORRECTION: PASS
SOFT-GATE OVERRIDE MAY CREATE (none): NO
OVERRIDE MAY RESOLVE A MATERIAL UNKNOWN: NO
OVERRIDE MAY HIDE A MISSING MATERIAL TRACE: NO
GENUINE (none) REMAINS VALID: YES
FS-1...FS-6: 6/6
NEW STATE INTRODUCED: NO
NEW FRAME FIELD INTRODUCED SOLELY FOR OVERRIDE: NO
STEP 8C SEMANTIC-CONTINUITY TESTS: PASS
FULL REGRESSION TESTS: 745
FULL REGRESSION FAILURES: 0
PACK VERSION: 1.8.2
RUNTIME REPAIR COMMIT: b26f39126d930ddf0ebf61cb5f274cb70f73f2d8
STEP 8C CHECKPOINT COMMIT: git rev-parse step-8c-baseline^{commit}  (recorded in the tag and the Step 8C.1 output)
STEP 8C CHECKPOINT TAG: step-8c-baseline → that commit
PR-3 STATUS: PILOT-2-WATCH
PILOT-2 PROTOCOL VALID: YES
STEP 8C FROZEN: YES
READY FOR PRICING-MARINHA TARGETED ARCHITECTURE REVISIT: YES
READY FOR PILOT 2: YES
```
