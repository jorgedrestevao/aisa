# Step 8 — Pilot Observation Log — pricing-marinha

BASELINE COMMIT: 78391d7ea00cc59c45b23ec65b384de8c812ab39
BRANCH: pp-pack-authoring/step-2-discovery-layer
PACK VERSION: 1.8.1
ENGAGEMENT: projects/pricing-marinha (pack=pp)

Rule reminder: no runtime edits during pilot. Observations only. No repair until post-pilot review.

---

## P-OBS-001

- **timestamp/phase**: 2026-09-04T18:00–19:10Z / Discovery R-01
- **triggering action**: `/round` (6 lenses, sequential inline) + 4 `/answer` batches
- **user/stakeholder intent**: resolve all Critical Unknown/Conflicted before Discovery exit gate
- **runtime component**: lens-business/operations/user/data/governance/financial, `/answer`
- **expected behaviour**: lenses append SU rows with correct state; Critical items surfaced for sponsor
- **observed behaviour**: 25 Confirmed/5 Assumed/16 Unknown/1 Conflicted/5 Risky after R-01; all 14 Critical items (13 U + 1 X) resolved across 4 answer batches; 1 answer (U-010→A-006) correctly held at Assumed, not upgraded to Confirmed, because sponsor answer was impression ("provavelmente boa") not verification — no-silent-upgrade rule held
- **impact**: Discovery exit gate met cleanly (0 Critical Unknown, 0 Conflicted)
- **workaround required?**: no
- **evidence**: `projects/pricing-marinha/council-log.md` R-01 + batches 1–4
- **candidate classification**: none (positive — epistemic discipline held under real pressure)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-002

- **timestamp/phase**: Discovery R-01 / governance lens
- **triggering action**: governance + operations lenses both touch sign-off/loading control
- **user/stakeholder intent**: n/a (observed, not triggered)
- **runtime component**: lens-governance, lens-operations
- **expected behaviour**: segregation-of-duties rule (C-022) vs observed practice (C-005, same person decides+loads) should surface as Conflicted, not silently reconciled
- **observed behaviour**: correctly raised as X-001, left unresolved for sponsor adjudication at `/decide` (not force-resolved in lens itself); sponsor resolved it in `/answer` batch 1 → C-026, with R-001 explicitly kept open as separate residual risk (continuity gap not extinguished by the SoD answer)
- **impact**: correct separation of "SoD question answered" from "operational continuity risk still open" — no conflation
- **workaround required?**: no
- **evidence**: council-log.md X-001 entry + batch 1 entry
- **candidate classification**: none (positive — epistemic states not collapsed)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-003

- **timestamp/phase**: Discovery R-01 / financial lens
- **triggering action**: lens-financial run with no cost/budget source in evidence
- **expected behaviour**: financial lens should not invent as-is cost or budget envelope absent evidence
- **observed behaviour**: 1 Confirmed + 1 Assumed + 2 Unknown only; council-log explicitly notes "sem estimativa de custo as-is nem envelope orçamental em nenhuma fonte — a lente financeira fica sem âncora até isso ser respondido"
- **impact**: correct — no invented financial figures; Unknown preserved (U-015/U-016) until sponsor answered
- **workaround required?**: no
- **evidence**: council-log.md R-01 summary
- **candidate classification**: none (positive — P-B epistemic integrity held)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-004

- **timestamp/phase**: Framing F-01 (council-independent, 6 parallel personas + chairman)
- **triggering action**: `/frame`
- **expected behaviour**: single problem sentence synthesized from SU with full anchor traceability; open questions and conflicts still material carried forward, not resolved by the chairman itself
- **observed behaviour**: frame.md single sentence anchors every clause to specific SU ids (C-017/C-035/C-041/R-006, A-001/C-029/R-001/R-003, C-030/C-032/C-039/R-009); 5 open questions (U-017,U-019,U-021,U-024,U-018) carried forward as still-material, not fabricated closed; 3 conflicts (X-002,X-003,X-004) surfaced with explicit "partes:" (which two source lenses/evidence disagree), none silently resolved by chairman
- **impact**: frame reads as genuinely load-bearing (a human sponsor could verify each clause); D-001 registered cleanly with override field empty (no gate bypass used)
- **workaround required?**: no
- **evidence**: `projects/pricing-marinha/frame.md`, `decisions.md` D-001
- **candidate classification**: none so far (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics (Discovery R-01 + Framing F-01, provisional)

```
QUESTIONS ASKED (AskUserQuestion batches): 14 (across 4 batches, all Critical)
QUESTIONS LATER JUDGED UNNECESSARY: 0 so far
DUPLICATE QUESTIONS: 0
QUESTIONS ANSWERABLE FROM EXISTING EVIDENCE: 0 identified so far (all 14 were genuine stakeholder judgement/evidence gaps)

CRITICAL UNKNOWNS IDENTIFIED: 13 (Discovery R-01)
CONFLICTS IDENTIFIED: 2 (X-001 Discovery; X-002/X-003/X-004 Framing — carried, not yet resolved)
EPISTEMIC PROMOTIONS DETECTED (incorrect): 0 — 1 correct non-promotion observed (U-010→A-006 held at Assumed)

OPTIONS DK PULLS: n/a (not yet in Options phase)
ARCHITECTURE DK PULLS: n/a
DELIVERABLE DK PULLS: n/a

H1 EXPECTED HUMAN JUDGEMENT EVENTS: 14 (answer batches) + 1 (frame acceptance)
H2 ENGAGEMENT CLARIFICATIONS: 0 distinct from H1 so far
H3 USABILITY-FRICTION INTERVENTIONS: 0
H4 FRAMEWORK-REPAIR INTERVENTIONS: 0

RE-RUNS (new evidence / human decision change / runtime defect): 0 / 0 / 0

S0: 0 · S1: 0 · S2: 0 · S3: 0 · S4: 0
```

## P-OBS-005

- **timestamp/phase**: Options O-01 / `/options` transition + council + chairman-synthesis
- **triggering action**: `/options` — Framing exit gate (D-001 registered) checked, 7 personas launched in parallel (6 Discovery lenses + solution-architect for the first time), chairman-synthesis wrote options.md
- **expected behaviour**: solution-architect enters only now (never in Discovery/Framing — rule held); no vendor/product name should appear before this round; council convergence/divergence handled without forcing artificial consensus
- **observed behaviour**: solution-architect first appearance confirmed at O-01 (council-log: "pela 1ª vez neste engagement"); zero vendor/product names anywhere in frame.md or Discovery lens-outputs (checked); all 7 personas converged on same 4 blockers (X-002, U-017, capacidade da app de referência, sessão KAM) — council-log explicitly notes no dialectic round was needed because no material divergence; 7 new rows (6 Unknown + 1 Conflicted), 0 new Risky — correctly attributed as reinforcement of existing rows, not manufactured novelty
- **impact**: no-tech-before-options rule held cleanly across 2 full phases; convergence was reported honestly (not manufactured to look tidy) — chairman explicitly states why no dialectic round ran
- **workaround required?**: no
- **evidence**: `council-log.md` O-01 + chairman-synthesis entries; `lens-outputs/chairman-synthesis-O-01.md`
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-006

- **timestamp/phase**: Options O-01 / options.md structure and reasoning
- **triggering action**: chairman writes 6-option comparison (O-001..O-006) + concern coverage + comparator status
- **expected behaviour**: options.md should reason per §12 (option-class generation, disqualifiers, preconditions, proof obligations, reversibility, comparator status) rather than fill a template mechanically; `COMPARATOR EVIDENCE ABSENT` used honestly where no real comparison data exists rather than fabricating a ranking
- **observed behaviour**: strong reasoning signal — O-004 vs O-005 explicitly marked "não são comparadores entre si" (different scopes of the same tech, not a forced exclusive choice) rather than ranked against each other artificially; `COMPARATOR EVIDENCE ABSENT` used 2x (O-001 vs O-002, O-003 vs O-004/O-005) instead of inventing cost/effort numbers; O-006 correctly flagged as "achado, não candidato a construir" — a distinct category (already-solved segment) rather than shoehorned into the option list as if competing; concern coverage section explicitly marks several dimensions "não avaliado nesta ronda" / "não material" instead of forcing a verdict on every one of the 12 dimensions
- **impact**: this reads as reasoning, not form-filling (pilot §12 core question) — the framework did not pressure the chairman into fabricating comparability or false precision
- **workaround required?**: no
- **evidence**: `projects/pricing-marinha/options.md` (Comparison, Comparator status sections)
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-007

- **timestamp/phase**: Options O-01 / Domain Knowledge pulls
- **triggering action**: solution-architect anchors O-004 material strengths to pack domain knowledge
- **expected behaviour**: DK pulled only where materially needed, cited with concrete section, not loaded wholesale
- **observed behaviour**: exactly 2 DK citations in the entire round, both by solution-architect, both used in reasoning (not decorative): `library/packs/pp/domain-knowledge/data/dataverse.md §8-9` and `library/packs/pp/domain-knowledge/architecture/patterns.md §5`, feeding directly into O-004's stated preconditions/strengths (native row/column security, native audit trail, direct-integration pattern). No other persona pulled DK (correct — none of the other 6 lenses are technology-facing at this phase)
- **impact**: empirical data point for §11/§14 — 2 pulls total this round, both material, 0 wasted; consistent with (not enforcing) the Step 4C median≈1/max2 observation
- **workaround required?**: no
- **evidence**: `options.md` O-004 entry
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics update (through Options O-01)

```
QUESTIONS ASKED: 14 (Discovery only so far — Options round produced 0 new AskUserQuestion cycles yet; 7 new open items (6 U + 1 X) recorded but not yet answered)
CRITICAL UNKNOWNS IDENTIFIED (cumulative): 13 (Discovery) + open count in U-025..U-030 to be triaged for criticality
CONFLICTS IDENTIFIED (cumulative): X-001 (Discovery, resolved) + X-002/003/004 (Framing, open) + X-006 (Options, new, open)
EPISTEMIC PROMOTIONS DETECTED (incorrect): 0 (cumulative)

OPTIONS DK PULLS: 2 (both material, both used, 0 unnecessary)
ARCHITECTURE DK PULLS: n/a (phase not reached)
DELIVERABLE DK PULLS: n/a

H1 EXPECTED HUMAN JUDGEMENT EVENTS (cumulative): 15 (14 Discovery answers + 1 frame acceptance) — Options decision itself still pending (/decide not yet run)
H3/H4: 0 / 0 (cumulative)
RE-RUNS: 0 / 0 / 0 (cumulative)
S0–S4: 0 across the board (cumulative)
```

## P-OBS-008

- **timestamp/phase**: Options O-01 / `/answer` post-options (X-002, U-017)
- **triggering action**: sponsor resolves X-002 → C-052 (SAP is source of truth); U-017 → decomposed into 3 Confirmed facts (C-053 volume, C-054 market structure, C-055 rarity) + 1 Assumed (A-008, qualitative synthesis)
- **expected behaviour**: an Unknown asking for a EUR figure that only has qualitative evidence available should NOT be force-closed as a fabricated number; partial closure via component facts + honest Assumed synthesis is the correct move
- **observed behaviour**: exactly this — council-log explicitly labels A-008 as "não um número EUR final"; U-017 closed by evidence decomposition, not by inventing a figure to satisfy the pilot engagement's forward motion
- **impact**: correct handling of a decision-relevant financial Unknown under real pressure to "just get a number" — epistemic honesty held
- **workaround required?**: no
- **evidence**: council-log.md "O-01 — /answer (pós-options)"
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-009

- **timestamp/phase**: pre-decide / unsolicited scope clarification
- **triggering action**: sponsor volunteers (not asked) that KAM don't use the new app, only receive the price
- **expected behaviour**: unsolicited information that resolves an open Conflicted (X-004) should be captured as a new Confirmed row and propagate correctly to dependent artefacts (premortem) rather than sit unintegrated
- **observed behaviour**: C-056 recorded, X-004 explicitly resolved → C-056; premortem was re-run (not silently left stale) because cause-of-death #3 depended on the now-obsolete interface-collision framing; the re-run correctly downgraded that cause's probability and reframed it as "capacidade de simulação removida sem confirmação" instead of deleting it outright — and a new Risky (R-012) was opened for the residual concern rather than treating the resolution as total
- **impact**: this is a clean example of legitimate rework classification (§27: "new evidence" / "upstream correction", NOT runtime defect) — the pack correctly triggered a re-run instead of letting an artefact go stale
- **workaround required?**: no
- **evidence**: council-log.md "Clarificação de âmbito (não solicitada)" + "Premortem (re-corrido)"
- **candidate classification**: none (positive) — logged as legitimate rework, counts toward RE-RUNS (new evidence), not RUNTIME-DEFECT RE-RUNS
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-010

- **timestamp/phase**: Decision D-01 / `/decide` with 5 Critical Unknowns still open
- **triggering action**: sponsor picks O-004 while U-025 (veto reason), U-026 (tie-break rule), U-027 (data owner), U-028 (reference-app capacity), U-029 (support owner) remain open
- **expected behaviour**: Decision phase is user-driven/interactive — no forced 0-Critical-Unknown gate like Discovery's. Open items must not be hidden; they must surface as explicit preconditions/proof obligations on the decision record, not silently dropped
- **observed behaviour**: all 5 remaining Critical Unknowns surfaced explicitly in D-002 as **Preconditions** (dono de dados-mestre nomeado, regra de desempate, blast radius DF_GRID_1) or folded into **Conditions**/**Accepted risks** (R-001, R-009, R-010, R-012) — none silently disappeared; the decision record is honest about what is NOT yet resolved
- **impact**: this is the correct behaviour per pilot §17 ("Is it clear what was NOT evaluated?") — a sponsor/reviewer reading D-002 alone can see the decision is conditional, not falsely final
- **workaround required?**: no
- **evidence**: decisions.md D-002 (Preconditions, Conditions, Proof obligations, Accepted risks fields)
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

## P-OBS-011

- **timestamp/phase**: pre-decide / premortem quality (§17, §31 S3/S4 integrity check)
- **triggering action**: `/premortem --horizon 12 meses` targeting O-004, run once, then re-run after C-056
- **expected behaviour**: every failure cause anchored to real SU ids, not invented narrative; mitigations map 1:1 to requirements/tripwire candidates, not vague advice
- **observed behaviour**: all 5 causes-of-death cite concrete ids (U-025, U-027/U-026/R-008, R-012/C-045, X-005/C-050/A-004, R-010/U-029); "sinais que estavam à vista desde o início" section cross-references 6 more ids without re-narrating; mitigation table maps cleanly to REQUISITO (7) / TRIPWIRE candidato (3) / ACEITAÇÃO (1) — no fabricated technical claim, no invented platform capability
- **impact**: premortem functioned as intended — surfaced R-012 (new Risky) as a genuine byproduct, not a checkbox exercise
- **workaround required?**: no
- **evidence**: `projects/pricing-marinha/premortem.md`
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics update (through Decision D-01)

```
QUESTIONS ASKED (cumulative): 14 (Discovery) + 2 (Options post-round: X-002, U-017) = 16
QUESTIONS LATER JUDGED UNNECESSARY: 0
DUPLICATE QUESTIONS: 0
QUESTIONS ANSWERABLE FROM EXISTING EVIDENCE: 0

CRITICAL UNKNOWNS IDENTIFIED (cumulative): 13 (Discovery, all resolved) + Options-round criticals — 5 remain open at decision time (U-025..U-029), surfaced explicitly as preconditions, not resolved by fiat
CONFLICTS IDENTIFIED (cumulative): X-001 (resolved, Discovery), X-002 (resolved, Options), X-003/X-005/X-006 (still open, tracked), X-004 (resolved via unsolicited clarification → C-056)
EPISTEMIC PROMOTIONS DETECTED (incorrect): 0 (cumulative) — 2 correct non-fabrications observed (A-006 Discovery, A-008 Options: qualitative synthesis not forced into a number)

OPTIONS DK PULLS: 2 (unchanged, both used)
ARCHITECTURE DK PULLS: n/a (phase not reached — no architecture record yet for O-004)
DELIVERABLE DK PULLS: n/a (synthesis ran, render not yet)

H1 EXPECTED HUMAN JUDGEMENT EVENTS (cumulative): 15 (Discovery+frame) + 2 (X-002/U-017 answers) + 1 (decision itself) = 18
H2/H3/H4: 0 / 0 / 0 (cumulative)
RE-RUNS DUE TO NEW EVIDENCE: 1 (premortem re-run after unsolicited C-056 clarification) — legitimate, not a defect
RE-RUNS DUE TO HUMAN DECISION CHANGE: 0
RUNTIME-DEFECT RE-RUNS: 0

S0–S4 (cumulative): all 0
```

## P-OBS-012

- **timestamp/phase**: `/synthesize` (auto after /decide) — architecture-story.md
- **triggering action**: synthesis of 5 topic packs
- **expected behaviour**: architecture-story should honestly flag that no blueprint exists yet if synthesize runs before /blueprint
- **observed behaviour**: council-log explicitly notes "architecture-story (sem blueprint ainda — nota explícita)" — synthesis did not fabricate architecture content ahead of the blueprint step; all 5 packs passed sanity check (≥3 sections, ≥1 SU id cited), no warnings
- **impact**: correct sequencing discipline held across a phase boundary that could easily have been faked
- **workaround required?**: no
- **evidence**: council-log.md "D-01 — aisa-synthesize"
- **candidate classification**: none (positive)
- **repair suggested?**: NO

## P-OBS-013

- **timestamp/phase**: `/blueprint` v01 — entry gate + architecture cognitive load (§18–20)
- **triggering action**: first blueprint post-decision (D-002, O-004)
- **expected behaviour**: entry gate correctly classifies scope×outcome before authorizing; open architecture choices that are genuinely unresolved (data ownership, tie-break rule, legal retention, integration ownership) must block approval rather than being silently defaulted; composition ownership must stay UNKNOWN rather than invented; a relocated responsibility to an existing incumbent system (SAP) must be flagged for fit evaluation, not assumed compatible
- **observed behaviour**: entry gate correctly computed `authorized` (scope=whole solution × outcome classe 2 × architectable); 7 open architecture choices logged, 4 explicitly marked as blocking approval (U-027 data owner, U-026 tie-break rule, X-005 legal retention, U-029 integration owner) — none defaulted or invented; all 3 compositions carry owner=UNKNOWN (tied to U-029, not fabricated); the SAP-incumbent relocation is explicitly tagged `INCUMBENT FIT UNEVALUATED` rather than assumed to work; 2 entities with unitemized field counts registered as open_architecture_choice rather than silently passing or falsely flagging as a cap violation; KAM correctly excluded from personas per C-056
- **impact**: this is the architecture layer structuring the frozen decision (§18's core question) without re-deciding it, and without inventing resolution to items the engagement hasn't actually resolved — v01 is explicitly NOT yet approved (4 structural blockers open), consistent with §18-20 requiring iteration to business approval before being final
- **workaround required?**: no
- **evidence**: `_blueprint/blueprint-log.md`, `_blueprint/ux-blueprint_v01.yaml`
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics update (through Blueprint v01)

```
ARCHITECTURE DK PULLS: 0 explicit citations found in blueprint-log.md (uses SU ids + pack architecture templates/README §3-4 by reference, not a runtime DK-pull event distinct from Options' 2)
OPEN ARCHITECTURE CHOICES: 7 (4 structural/blocking, 3 non-blocking) — none defaulted, all traced to open SU ids
CAP VIOLATIONS: 0 confirmed (2 ambiguous cases correctly logged as open choices, not false positives/negatives)
H1/H2/H3/H4 (cumulative): unchanged — blueprint v01 is a system artefact, no new human intervention yet (approval still pending)
S0–S4 (cumulative): all 0
```

## P-OBS-014

- **timestamp/phase**: Blueprint v02 — resolving U-029 revealed a bigger fact
- **triggering action**: sponsor answers U-029 (integration owner), reveals an already-operated shared SQL Server DB will host this engagement's pricing data too (C-057)
- **expected behaviour**: a fact that changes `record_authority` classification for 3 domains and invalidates the v01 assumption of a native platform store should propagate honestly — including opening a NEW structural tension (native vs external store) rather than quietly keeping the old surface choice
- **observed behaviour**: exactly this — 3 domains' `record_authority` flipped to "external system of record / keep-in-place"; owner moved from UNKNOWN to known-by-class (not fabricated to a named individual); new open architecture choice A-009 opened explicitly (Record-centric app assumption vs. externally-authoritative data) instead of silently deciding it; blocker count correctly dropped 4→2, not to 0 (A-009 and narrower U-031 remained honestly open)
- **impact**: this is the blueprint layer correctly reacting to new evidence changing the architecture's foundations mid-iteration, without hiding the new uncertainty it created
- **workaround required?**: no
- **evidence**: `_blueprint/blueprint-log.md` v02 entry
- **candidate classification**: none (positive)
- **repair suggested?**: NO

## P-OBS-015

- **timestamp/phase**: Blueprint v03 — terminology correction mid-architecture
- **triggering action**: resolving U-031 (integration owner) surfaces that the target system is actually named "X-Author", not "X-ALT" — a naming error propagated across multiple earlier SU rows
- **expected behaviour**: a naming/identity error discovered mid-architecture must be corrected and its consequences traced (is this the same system as a previously-vetoed integration?), not silently absorbed or ignored because it's inconvenient this late
- **observed behaviour**: C-064 records the correction explicitly; the blueprint raises a "suspeita, não confirmada" (suspected, unconfirmed) link to the system killed by a prior stakeholder veto (C-038/U-025) rather than asserting or denying the link without evidence; the affected composition gets an explicit flag: do not proceed to technical design without closing U-025 first — turning a naming slip into a real, tracked architecture gate rather than a footnote
- **impact**: this is a concrete example of the framework surfacing a risk a human might have breezed past (multi-round naming drift is easy to miss); no invented fact either direction (link neither confirmed nor dismissed)
- **workaround required?**: no
- **evidence**: `_blueprint/blueprint-log.md` v03 entry
- **candidate classification**: none (positive) — arguably evidence this SHOULD be flagged as a general lesson (naming drift across rounds), but not a pack defect — it's evidence the epistemic discipline caught it
- **repair suggested?**: NO

## P-OBS-016

- **timestamp/phase**: U-025 — two closure attempts, both correctly held open
- **triggering action**: sponsor asked directly, twice, why the prior X-Author integration was vetoed
- **expected behaviour**: "não sei" from the sponsor must not be converted into any kind of closing fact (Confirmed or Assumed); the system should recognize when a question is structurally unanswerable by this stakeholder and redirect to the right next step instead of re-asking the same person
- **observed behaviour**: both attempts logged, U-025 stays Unknown both times, no fabricated row; council-log explicitly treats the "não sei" itself as informative (reinforces R-011 — nobody has investigated this internally); recommends the correct next step — external/vendor records or a different stakeholder — instead of scheduling a 3rd sponsor round
- **impact**: strong example of epistemic integrity under real repeated pressure to close an item — 2 consecutive non-answers did not erode the discipline
- **workaround required?**: no
- **evidence**: council-log.md "U-025 — tentativa de fecho, permanece aberta" (both entries)
- **candidate classification**: none (positive)
- **repair suggested?**: NO

## P-OBS-017

- **timestamp/phase**: Blueprint v04 — legitimate blocker dissolution via scope narrowing
- **triggering action**: unsolicited sponsor clarification (C-065) — the live X-Author integration is being handled by a different initiative; this app only prepares outputs for Excel export
- **expected behaviour**: a blocker tied to unresolved external risk (U-025) may legitimately dissolve if the actual boundary of THIS engagement's responsibility changes — but only if the composition is correctly relocated (owner = other initiative) rather than the underlying Unknown being resolved by fiat. U-025 itself must remain open in the SU for whoever it does concern
- **observed behaviour**: exactly this — `x-author-load-integration` composition removed, replaced by an explicit `relocated_responsibilities` entry with owner = "outra iniciativa (fora desta engagement)"; U-025 explicitly stated to remain Unknown in the SU, not deleted or force-closed; structural blockers correctly drop to 0 only because the boundary genuinely moved, with the boundary crossing pinned to a real evidence id (C-065), not just declared
- **impact**: correct handling of scope-boundary dissolution (§8/§18 scope integrity, P-D taxonomy) — the blocker went away for the right reason (responsibility no longer belongs here), not because the pack got tired of tracking it
- **workaround required?**: no
- **evidence**: `_blueprint/blueprint-log.md` v04 entry
- **candidate classification**: none (positive)
- **repair suggested?**: NO

---

## Running metrics update (through Blueprint v04)

```
BLUEPRINT ITERATIONS: 4 (v01→v04), each with a clear, evidenced trigger — no iteration was cosmetic
STRUCTURAL BLOCKERS: 4 (v01) → 2 (v02) → 1 (v03) → 0 (v04); each drop tied to a specific new Confirmed fact (C-058, C-059, C-060, C-062, C-063) or a legitimate scope relocation (C-065), never to silent default
NEW SU ROWS SURFACED DURING BLUEPRINT ITERATION: C-057, C-058, C-059, C-060, C-062, C-063, C-064, C-065 (facts) + A-009 (Risky-adjacent tension, resolved same session) + U-031 (narrower Unknown, resolved) + U-025 (unresolved, held open, 2 closure attempts both correctly refused)
TERMINOLOGY DRIFT CAUGHT: 1 (X-ALT → X-Author, C-064) — mid-architecture, before it reached a deliverable

H1 (cumulative): +2 (U-029 answer chain, U-031/A-009 resolution round) — running total ~20, exact count TBD at report time
H4 FRAMEWORK-REPAIR INTERVENTIONS: 0 (cumulative)
RE-RUNS DUE TO NEW EVIDENCE (cumulative): 2 (premortem re-run + this multi-version blueprint chain, which is normal iteration, not defect-driven rework)
RUNTIME-DEFECT RE-RUNS: 0
S0–S4 (cumulative): all 0
```

Blueprint v04: 0 structural blockers, ready for `/render` on the architecture side (3 non-structural items remain: DF_GRID_1 confirmation, KAM validation, exact export format — informing production, not blocking approval). Next: awaiting business approval of v04, or user proceeds to `/render`.

## P-OBS-018

- **timestamp/phase**: `/render --all --dry-run` against blueprint v04
- **triggering action**: dry-run render of all 6 deliverables without writing to `_render/`
- **expected behaviour**: render should identify real missing slots per deliverable's projection contract, correctly skip conditional slots whose trigger condition doesn't hold, and never silently fabricate a missing value (§21-22, render-gaps discipline)
- **observed behaviour**: exactly this across all 6 deliverables. Genuine gaps found: `solution_name` (missing in all 6 — never named anywhere in context.json or blueprint), `A9` (irreversible-choices/exit-cost, never written in blueprint — affects executive-report + implementation-spec sequencing), `A8` (environment/release, never written — affects implementation-spec), `app:` block (name/devices/language, never defined — affects design brief). Correctly-skipped conditionals: `structural_open_choices` (0 in v04 — correct, nothing to report), `scope_ownership_projection`/`candidate_architectures_note` (only 1 scope×outcome pair — correctly not applicable), `brand_guidance`/`accessibility_notes`/`async_state_requirements`/`inherited_surface_limits`/`design_validations` (no such requirement was ever raised in this engagement — correctly skipped, not silently invented)
- **impact**: this is the render-gaps mechanism (§21, rule `render-on-decision-only.md`) working exactly as designed — a real, honest gap list instead of either a hard crash or silently-filled placeholders
- **workaround required?**: no
- **evidence**: dry-run output (see conversation), blueprint v04 log
- **candidate classification**: none for the mechanism itself (positive). The underlying gaps (`solution_name`, A8, A9, `app:` block) are genuine missing-input findings — see P-OBS-019
- **repair suggested?**: NO (mechanism); gaps themselves are engagement input to close, not a pack defect

## P-OBS-019

- **timestamp/phase**: same dry-run — cross-cutting gap: `solution_name`
- **triggering action**: none of `/start`, `/frame`, `/options`, `/decide`, or `/blueprint` v01–v04 ever prompted for or recorded a solution name
- **expected behaviour**: n/a — no protocol step explicitly requires naming the solution before Options/Decision (naming typically follows from choosing/building a specific system); observing whether its absence is felt as friction at render time
- **observed behaviour**: all 6 deliverables share this exact same gap — it is not 6 separate gaps, it is 1 upstream gap surfacing 6 times downstream. The render layer correctly attributed it once per deliverable rather than masking it
- **impact**: mild — real usability friction at the render boundary (H3-type), not a decision-quality or epistemic problem. A human closing this takes seconds (name the solution) but nobody was prompted to do it earlier
- **workaround required?**: trivial (user names it before a real render)
- **evidence**: dry-run output — solution_name gap listed in all 6 deliverables
- **candidate classification**: P-F (context/process efficiency) or P-L (documentation/instruction clarity) — tentative; single occurrence, cannot yet tell if this is generic (every engagement will hit this) or specific to this one not having named a target system yet. **Do not classify further until more pilots confirm recurrence** (§32)
- **recurring or one-off?**: unclear — first data point
- **severity**: S1 (nuisance, safe/trivial workaround)
- **repair suggested?**: NO (record only, per pilot rule)

## P-OBS-020

- **timestamp/phase**: same dry-run — architecture-story.md staleness
- **triggering action**: dry-run render of solution-blueprint deliverable cross-checks `_synthesis/architecture-story.md` against the now-current blueprint v04
- **expected behaviour**: if a synthesis narrative predates blueprint iterations that changed underlying facts, the render should not silently prefer the stale narrative — SU/architecture record must win per `shared-understanding-as-source-of-truth.md`
- **observed behaviour**: exactly this — the render correctly identified that architecture-story.md was written before v02→v04 (shared SQL Server DB, X-Author correction, export-to-Excel) and explicitly noted "onde a narrativa e o registo divergirem, o registo ganha" (register wins) rather than rendering a document that quietly contradicts the approved architecture. Recommended re-running `/synthesize` for that topic pack before a real render
- **impact**: this is the source-of-truth rule holding under a genuine multi-iteration scenario, not just in theory — the render layer caught a staleness a human reviewer might have missed if they only read the narrative pack
- **workaround required?**: yes but cheap — re-run `/synthesize` (or the specific topic pack) before `/render --all`
- **evidence**: dry-run output re: solution-blueprint gap
- **candidate classification**: none (positive) — this is the safeguard working, though it does suggest synthesis packs can go stale across blueprint iterations; worth watching if this recurs across pilots (not a repair decision now)
- **recurring or one-off?**: unclear — first data point
- **severity**: S0 (caught cleanly, no consequence — render didn't proceed on stale data)
- **repair suggested?**: NO

## P-OBS-021

- **timestamp/phase**: same dry-run — A8 (environment/release) and A9 (irreversible choices/exit cost) never written in blueprint v01–v04
- **triggering action**: implementation-spec and executive-report render attempt to pull A8/A9 sections
- **expected behaviour**: gap correctly surfaced rather than defaulted; migration_and_cutover should reflect that this is genuinely a real migration (leaving Excel) even though the blueprint's A9 conditional for "replacing an existing artefact" was never triggered
- **observed behaviour**: gaps correctly reported, not silently defaulted. One nuance flagged by the render itself: `migration_and_cutover` comes back not-applicable not because there's no real migration (there is — this replaces the Excel workbook) but because blueprint v04 never activated A9's "existing-artefact-replacement" conditional — i.e. this is an architecture-authoring gap surfacing at render time, correctly attributed to the blueprint rather than papered over in the deliverable
- **impact**: moderate — this blocks a clean implementation-spec render until blueprint v05 adds A8/A9; but it was caught before producing a misleading spec that silently omits migration/cutover and environment/release content for what is, in fact, a system replacement
- **workaround required?**: yes — revisit blueprint (v05) to write A8/A9 before treating implementation-spec as final
- **evidence**: dry-run output re: implementation-spec + executive-report gaps
- **candidate classification**: unclear yet whether A8/A9 being frequently skipped is generic pack friction (blueprint authoring doesn't naturally prompt for them in a fast-moving iteration) or specific to this engagement's blueprint author choices — **first data point, do not repair from single pilot** (§32)
- **recurring or one-off?**: unclear
- **severity**: S1/S2 borderline — real content is missing from a required deliverable until closed, but caught cleanly pre-render with a clear next step (not S3: no wrong decision or misleading output was produced)
- **repair suggested?**: NO (record only)

## P-OBS-022

- **timestamp/phase**: same dry-run — estimate deliverable
- **triggering action**: estimate render attempted in dry-run mode
- **expected behaviour**: distinguish a genuine blocking gap from a mechanical artefact of `--dry-run` not writing intermediate files
- **observed behaviour**: correctly explained as neither Mode A nor Mode B resolving — Mode A needs an Implementation Specification already written to `_render/` (this is the first run and dry-run writes nothing), Mode B doesn't apply (architecture is approved, no blocking structural choice). Explicitly noted this self-resolves on a real `/render --all` because the Implementation Spec is written first in the same pass, and Estimate finds it right after
- **impact**: none — correctly distinguished a dry-run mechanical limitation from an actual pilot defect; no confusion introduced
- **workaround required?**: no (resolves itself on non-dry-run)
- **evidence**: dry-run output re: estimate
- **candidate classification**: none
- **repair suggested?**: NO

---

## Running metrics update (through render --dry-run)

```
RENDER GAPS FOUND (real): solution_name (×6, 1 root cause) + A8 (×1) + A9 (×2) + app: block (×1) + architecture-story staleness (×1)
RENDER GAPS CORRECTLY SKIPPED (conditional not triggered): structural_open_choices, scope_ownership_projection, candidate_architectures_note, brand_guidance, accessibility_notes, async_state_requirements, inherited_surface_limits, design_validations, investment_summary (this run)
FABRICATED/DEFAULTED VALUES: 0
DRY-RUN MECHANICAL NON-GAPS CORRECTLY DISTINGUISHED FROM REAL GAPS: 1 (estimate Mode A/B explanation)

S0: +1 (P-OBS-020) · S1: +1 (P-OBS-019) · S1/S2 borderline: +1 (P-OBS-021)
Cumulative severity: S0=1, S1=1, S2=0, S3=0, S4=0 (borderline P-OBS-021 counted conservatively as S1 pending report-time judgement)
```

Next step before a real `/render --all`: close `solution_name`, and decide whether to revisit blueprint (v05: write A8, A9) and re-run `/synthesize` for architecture-story before rendering for real, or proceed anyway and accept the resulting gaps as tracked backlog. That choice is the user's — not something this pilot log should resolve.

## P-OBS-023

- **timestamp/phase**: `solution_name` closed + Blueprint v05 (A8/A9 added)
- **triggering action**: user names the solution ("Pricing Marinha" in context.json); blueprint v05 written on top of the already-**approved and frozen** v04 (D-003), adding A8 (environments) and A9 (irreversible choices)
- **expected behaviour**: v04 is frozen per its own approval log ("versões futuras partem daqui, nunca o sobrescrevem") — v05 must build additively on it, not silently reopen or contradict the approved architecture; A8/A9 content must be sourced from real confirmed facts, not invented to satisfy the render gap; a genuinely unresolved item (does this count as "replacing an existing artefact"?) must stay open rather than being forced closed just to make the render clean
- **observed behaviour**: v05 correctly built on v04's frozen content (irreversible_choices §3 explicitly cites C-057/C-062 "Blueprint v02, reconfirmado em v03-v05" — traceable, not restated as new). A8 environments block is sourced from a direct sponsor confirmation (C-067, 2 tiers, no formal Test tier) and explicitly separates what the sponsor confirmed directly from what is "inferred by extension" (`policy_plane` note: "não confirmado como afirmação directa e distinta") — a fine but important epistemic distinction held even inside a single YAML field. A9 does the same for 3 irreversible choices, each with its own `exit_cost` reasoning. Critically: `replacement_of_existing_artefact.engaged: false` is **left false** with an explicit reason acknowledging the tension ("apesar de esta solução substituir na prática o ficheiro Excel actual... item de trabalho em aberto identificado no dry-run... ainda por resolver") — the author did NOT force this conditional true just to make the earlier dry-run gap disappear
- **impact**: this is a meaningful integrity signal — under direct pressure to close a specific named gap (from the dry-run I flagged), the framework/author held the line and left the genuinely unresolved item open rather than closing it cosmetically. That is exactly the failure mode §33 (no live optimization) and §9 (don't fabricate to help the pilot reach later phases) warn against, and it did not occur
- **workaround required?**: no — but the underlying open item (migration/cutover framing) still needs real resolution before implementation-spec can be fully clean; tracked, not closed
- **evidence**: `_blueprint/ux-blueprint_v05.yaml` (A8/A9 sections), `context.json` (solution_name)
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics update (post v05)

```
solution_name: CLOSED ("Pricing Marinha")
A8: written (v05) — sourced to C-067/C-063, epistemic distinction between direct confirmation and inference held
A9: written (v05) — 3 irreversible choices, each with exit_cost reasoning; replacement_of_existing_artefact LEFT OPEN (honest, not force-closed)
FABRICATED/DEFAULTED VALUES (cumulative): 0
CLOSURE-UNDER-PRESSURE INTEGRITY TEST: PASS (1 direct observation — did not force-close a gap just because it had been named)

S0–S4 (cumulative): still S0=1, S1=1, S2=0, S3=0, S4=0
```

Remaining before a fully clean `/render --all`: architecture-story.md still needs a `/synthesize` re-run (staleness from P-OBS-020, not yet addressed); `replacement_of_existing_artefact` conditional remains genuinely open (by design, correctly not forced). Next: user's call whether to re-synthesize now or render and accept that one tracked gap.

## P-OBS-024

- **timestamp/phase**: manual `/synthesize` re-run for architecture-story, after v05 was written but before v05 is approved
- **triggering action**: re-synthesize architecture-story to fix the staleness flagged at P-OBS-020
- **expected behaviour**: the re-synthesis must source architecture content from the last **approved** blueprint version (v04, D-003), not from the newer but still-unapproved v05 — even though v05 is more complete (has A8/A9) and was just written in direct response to this same pilot's feedback
- **observed behaviour**: exactly this — synthesis log explicitly states "v05 (não aprovada) citada apenas como nota, não como fonte de arquitectura"; the rewritten architecture-story.md sources every claim from `ux-blueprint_v04.yaml#architecture` (the approved, frozen version) and `decisions.md#D-002/D-003`; SU id citations jumped from 21 (stale version) to 37 (current); explicitly notes "nenhum lens=technology existe nesta engagement" and correctly does not fabricate a technology-lens citation to fill a template slot
- **impact**: this is the approval-gate discipline holding even when the more-complete unapproved version was sitting right there and would have made a "nicer" document — the pack did not quietly upgrade its source just because v05 existed and answered the very gap this pilot flagged
- **workaround required?**: no
- **evidence**: `_synthesis/_synthesis-log.md` (2026-09-05T01:45:00Z entry), `_synthesis/architecture-story.md`
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics update (post re-synthesis)

```
architecture-story.md: RE-SYNTHESIZED, sourced correctly from approved v04 (not unapproved v05), 21→37 SU ids cited
APPROVAL-GATE DISCIPLINE UNDER TEMPTATION: PASS (unapproved-but-more-complete version correctly not used as source)
FABRICATED/DEFAULTED VALUES (cumulative): still 0

S0–S4 (cumulative): still S0=1(+1 this obs, positive)=2, S1=1, S2=0, S3=0, S4=0
```

All known render-blocking gaps now closed or correctly tracked-open (solution_name closed; A8/A9 written in v05; architecture-story fresh; `replacement_of_existing_artefact` honestly left open, non-blocking). Engagement is ready for a real `/render --all` whenever the user chooses — this pilot log will pick up deliverable-consumer instrumentation (§21-25) at that point.

## P-OBS-025

- **timestamp/phase**: `/render --all` (real, not dry-run)
- **triggering action**: full render of all 6 deliverables, in dependency order (discovery-report → solution-blueprint → implementation-spec → estimate → executive-report → claude-design-brief, explicitly because executive-report needs the estimate headline)
- **expected behaviour**: render must source architecture content from the approved-and-frozen v04, not the unapproved v05 — even though v05 was written specifically to close these exact gaps and is sitting right there. Any resulting gap must be reported honestly rather than silently pulling from v05 to make the render look clean
- **observed behaviour**: 6/6 deliverables rendered, none skipped, none blocked. 5 required-slot gaps, all in solution-blueprint/implementation-spec/claude-design-brief (A8, A9, `app:` block) — every one attributed to the single root cause: "v05 já fecha estes 3 conteúdos... mas continua não aprovado. v04 continua a versão aprovada e frozen, e é dela que este render lê." `render-gaps.md` gives the exact one-line fix for each (approve v05) rather than leaving the user to reverse-engineer it. render-log.md correctly logs every conditional skip with its reason (`scope_ownership_projection`, `migration_and_cutover`, `design_blocking_open_items`, etc.) separately from actual gaps — the append-only gaps file stays clean of skips as its own header promises
- **impact**: this is the approval-gate discipline (`render-on-decision-only.md` + shared-understanding-as-source-of-truth's "register wins" logic extended to blueprint versions) holding under maximum realistic pressure — the fix was one approval away and available in the filesystem, and the render still refused to reach for it. Zero fabrication, zero silent gap-closure, and the diagnostic message told the user exactly what to do next
- **workaround required?**: yes — approve v05 (single step, no re-architecture) to close all 5 gaps at once
- **evidence**: `_render/render-log.md`, `_render/render-gaps.md` (2026-09-05T02:00:00Z run)
- **candidate classification**: none (positive) — P-C (authority/source discipline) explicitly tested and held
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics update (post `/render --all`)

```
DELIVERABLES RENDERED: 6/6 (0 skipped, 0 blocked)
REQUIRED-SLOT GAPS: 5, single root cause (v05 unapproved), each with an exact one-line resolution stated
FABRICATED/DEFAULTED VALUES (cumulative): still 0
APPROVAL-GATE DISCIPLINE UNDER MAXIMUM PRESSURE: PASS (2nd distinct test — P-OBS-024 tested synthesis, this tests render; both held)
CONDITIONAL SKIPS CORRECTLY SEPARATED FROM GAPS: yes (render-log.md vs render-gaps.md, per file's own stated contract)

S0 (cumulative): 3 · S1: 1 · S2: 0 · S3: 0 · S4: 0
```

Deliverables are usable now for consumer review (§21-25) with 5 known, tracked, single-cause gaps. Next: user's call — approve v05 and re-render for a fully clean pack, or proceed to consumer review (sponsor/architect/implementer reads) with the gaps as known backlog. Either is legitimate pilot data; this log does not recommend one over the other.

## P-OBS-026

- **timestamp/phase**: v05 approval (D-004) + `/render --all` re-run
- **triggering action**: sponsor approves v05; user re-runs `/render --all`
- **expected behaviour**: (a) v05's approval log should not silently assume future renders read v05 without the sponsor saying so explicitly — an unprompted "latest version wins" default would be a scope/authority overreach; (b) once approved and pointed at, the 5 previously-diagnosed gaps should close exactly as predicted, with no new gaps introduced and no prior gap reopened
- **observed behaviour**: (a) confirmed — the v05 blueprint-log entry explicitly states it does not assume future renders switch to v05: "Sinalizado ao sponsor: se quer que os próximos renders leiam v05..., precisa dizer explicitamente... — não assumido aqui." Only once D-004 (explicit approval) was registered did v05 become the read version; (b) confirmed — render-gaps.md's 2nd run entry: "Todas as 5 lacunas do run anterior fecharam-se... nenhuma foi reaberta. 0 lacunas required neste run."
- **impact**: this closes out a full, clean render→gap→diagnosis→fix→re-render loop with the exact predicted outcome and no surprises — a strong signal that the render-gaps mechanism's diagnoses are literally actionable, not just descriptive
- **workaround required?**: no
- **evidence**: `_blueprint/blueprint-log.md` v05 entry + APROVAÇÃO v05 entry; `_render/render-gaps.md` 2nd run entry
- **candidate classification**: none (positive)
- **recurring or one-off?**: n/a
- **repair suggested?**: NO

---

## Running metrics update (post 2nd `/render --all`)

```
2nd RENDER RUN: 6/6 rendered, 0 required-slot gaps, 0 gaps reopened
FULL LOOP VERIFIED: dry-run → diagnose → fix (name solution, v05 A8/A9) → re-synthesize → render → 5 gaps, single cause → approve v05 → re-render → 0 gaps
FABRICATED/DEFAULTED VALUES (cumulative): 0
RE-RUNS DUE TO NEW EVIDENCE (cumulative): 2 (premortem, blueprint chain) — this render re-run counts as RE-RUN DUE TO HUMAN DECISION (v05 approval), not a defect-driven re-run
RUNTIME-DEFECT RE-RUNS (cumulative): 0

S0 (cumulative): 4 · S1: 1 · S2: 0 · S3: 0 · S4: 0
```

Engagement now has a fully clean, gap-free 6-deliverable render pack based on approved architecture (v05, D-004). This is a strong natural checkpoint to begin §21-25 deliverable-consumer instrumentation (discovery-report → business analyst/lead reader; executive-report → sponsor; solution-blueprint/implementation-spec → architect/implementer; estimate → delivery lead) whenever those readers are available, or to move toward the pilot report if the engagement's legitimate stopping point is reached here.

---

## POST-HOC CORRECTION — reviewer (Jorge) feedback after report compiled, 2026-09-05

Three structural problems flagged by the human reviewer after `STEP 8 — REAL ENGAGEMENT PILOT: PASS` was first compiled. All three are upheld on review. **This reclassifies prior entries — see corrections below.**

## P-OBS-027

- **timestamp/phase**: Discovery R-01, retrospective review
- **triggering action**: reviewer notes the engagement never anchored deeply enough to the actual Excel process — inputs, formulas, calculation chain, outputs ("partir o elefante às postas" — decompose the real process before reasoning about it)
- **expected behaviour**: for a process-replacement engagement, Discovery/lens-operations/lens-data reasoning should be grounded in the captured process model (`_capture/process-model.md`, L1 extraction, L2 process model, L3 replay) at the level of actual calculation logic — not just SU-level summary facts about the process (e.g. "6-sheet duplication exists", C-041) without the reasoning ever engaging the concrete calculation chain itself
- **observed behaviour**: the capture pipeline ran once at engagement start and its output (`_capture/process-model.md`, 14 process rules, 11 PM-U questions) exists, but this pilot's own review of lens-outputs and options.md found no evidence that Options/Architecture reasoning engaged the process model's actual calculation logic in depth — reasoning stayed at the level of SU facts about the process (duplication exists, named ranges are unowned) rather than the process itself (which formulas, which dependency chains, which specific outputs feed which specific downstream steps)
- **impact**: **material** — a highly customized calculation process was being architected without the architecture reasoning demonstrably engaging the process's actual shape. This is upstream of, and likely a root cause of, P-OBS-028/029 below: if the real calculation/data shape had been engaged in depth, the surface-choice and data-authority contradiction might have surfaced during Options, not been retroactively discovered by a human reviewer
- **workaround required?**: yes — re-engage the process-capture output directly during Options/Architecture reasoning, not just its SU-level summary
- **evidence**: `_capture/process-model.md` (exists, appears underused downstream); `options.md`, `_blueprint/*.yaml` (no direct citation of process-model.md content observed)
- **candidate classification**: **P-F (context efficiency) crossed with P-A (semantic correctness)** — the capture output existed but downstream reasoning did not demonstrably pull from it at the needed depth
- **recurring or one-off?**: unclear — first data point, but plausibly systemic if the pack's Options/Architecture stages don't structurally require re-engaging `_capture/` outputs
- **severity**: **S3** (decision/architecture risk — reasoning proceeded on a shallower process model than the engagement actually needed)
- **repair suggested?**: NO (record only, per pilot rule) — but flagged as a strong repair candidate for post-pilot review

- **Step 8B adjudication note (2026-09-05)** — appended, original entry above unchanged. Lineage audit (`step-8b-post-pilot-adjudication-report.md` §12–13): 14/14 process rules traced. The absence of `_capture/process-model.md` citations in `options.md`/blueprints is **not** the defect (C-041, which they cite, carries PM-003/PM-U-009; the frozen model reasons from the SU). The material losses are: capture→SU **3** (PM-003 what-if facet `Simulador`; PM-007 model-style base sheets; PM-008 `Outputs BIOS` output family) plus PM-U-002 (Critical) never promoted; SU→Options **1** (Mon/Tue estimation rule treated as exposure, never as a capability requirement); Options→Architecture **2** (audit-trail mechanism and server-side authorization point not re-derived after C-057 — entangled with P-OBS-029). Root cause primarily `Discovery/capture-to-SU projection loss`; the PM-U adopt-or-dismiss step exists in `docs/PROCESS_CAPTURE_SPEC.md` and the capture template but in no lens `SKILL.md` (contract drift). **Severity stays S3, re-rooted.** Parse-once boundary preserved: no whole-process reread proposed. Candidate classification revised: PR-2 = DOCUMENTATION (contract drift), not a proven generic carriage/depth rule.

## P-OBS-028

- **timestamp/phase**: Blueprint v01 experience-surface choice, retrospective review
- **triggering action**: reviewer notes this is an extremely customized process (6 divergent calculation sheets, per-port/per-counterparty logic, heuristic-driven Monday/Tuesday estimation) — exactly the profile that argues for a Canvas app (full custom logic/UX control), not a Record-centric/model-driven app (which assumes a comparatively standard CRUD-over-entities shape)
- **expected behaviour**: the blueprint's experience-surface choice (A-early architecture decision) should weigh process customization level as a first-order input; a process this idiosyncratic should have triggered, at minimum, an explicit comparison note between Canvas and model-driven, not a single surface chosen and carried through v01-v05 without revisiting the customization signal already sitting in the SU (C-041 six-sheet duplication, C-046 heuristic rule, R-008 broken named range, etc.)
- **observed behaviour**: "Record-centric app (model-driven)" was chosen at v01 and never seriously re-examined on customization grounds — the only surface re-examination that happened (A-009, v02→v03) was about data-store location (native vs external), not about calculation/UX customization. The customization signal, which was abundant in the SU from Discovery onward, was not the trigger for any surface reconsideration
- **impact**: **material** — if the actual build proceeds on this blueprint, it risks fighting the model-driven paradigm for a process that doesn't fit it, independent of the data-authority problem in P-OBS-029
- **workaround required?**: yes — revisit experience-surface choice with process-customization explicitly as a decision input
- **evidence**: `_blueprint/blueprint-log.md` v01-v05 (surface only reconsidered on data-location grounds, never customization grounds)
- **candidate classification**: **P-A (semantic correctness)** — the architecture layer's surface-selection reasoning did not engage a material, already-available SU signal
- **recurring or one-off?**: unclear — first data point
- **severity**: **S3**
- **repair suggested?**: NO (record only)

- **Step 8B adjudication note (2026-09-05)** — appended, original entry above unchanged. The "high customization → Canvas" presumption in the original wording is **withdrawn**; it is not a rule of this pack (`application-surfaces.md` §12: no ranking, no size threshold). The valid finding stands, reformulated: the v01 surface selection evaluated identity class, data density, relational navigation and store-inherited controls only; it did **not** evaluate the interaction shape — daily wide-grid entry (~85 manual values/row, PM-001), calculation density visible to users (PM-002/003/007), and the what-if/estimation task (`Simulador`, PM-003; sponsor's literal ask #2; PM-U-002/003 Critical, never asked). Calculation complexity and interaction complexity are adjudicated separately (report §10–11). **Severity stays S3.** Candidate classification: PR-3 = ENGAGEMENT PRACTICE DEFECT at n=1 — knowledge was in the pack, signals were in capture/SU, not evaluated; watch for recurrence in Pilot 2.

## P-OBS-029

- **timestamp/phase**: Blueprint v02→v03, A-009 resolution via C-062 — **the most serious finding of this pilot**
- **triggering action**: reviewer notes model-driven (Dataverse) apps do not natively run against an external SQL Server as their record authority — this is a platform-level structural incompatibility, not a nuance
- **expected behaviour**: per §15, "any unsupported technical claim is a serious pilot defect." When A-009 was raised in v02 ("a superfície primária Record-centric app assume dados no store nativo da plataforma; com a autoridade de dados a mover para uma BD externa, Canvas app ou um desenho híbrido pode ser mais adequado" — the pack correctly identified the right question), its resolution in v03 needed either (a) real, checkable evidence that the specific connectivity pattern actually supports this (e.g., a named, verified virtual-table/connector mechanism with its real limitations), or (b) if that evidence wasn't available, staying Unknown rather than being marked Confirmed
- **observed behaviour**: A-009 was closed via **C-062** — "conectividade nativa já configurada, confirma Record-centric app" (native connectivity already configured, confirms Record-centric app) — treated as a Confirmed fact and used to keep the model-driven surface unchanged through v03/v04/v05. This claim, on the reviewer's correction, is technically false or at minimum unsupported as stated: model-driven apps' primary record store is Dataverse; an external SQL Server as `record_authority` (as v02-v05 explicitly declare — "external system of record / keep-in-place") is exactly the shape that argues AGAINST a model-driven surface, not for it
- **impact**: **severe** — this is the pack's own epistemic-integrity mechanism failing at the one moment it mattered most: the right question was asked (A-009), but the closing "fact" (C-062) was accepted without technical verification, and it happened to be the fact that determined whether the chosen architecture (model-driven, whole-solution, D-002/D-003/D-004, now the basis of a rendered Implementation Spec estimating 44-51 person-days) is even buildable as specified. **I (the pilot instrumenter) also failed here** — P-OBS-014 logged this same resolution as a positive example of "epistemic promotion held" without independently checking whether C-062's content was itself technically sound. That was a review-quality failure on my part, not just the engagement's
- **workaround required?**: yes, substantial — revisit the experience-surface choice with real technical verification of what connectivity model-driven Canvas Apps genuinely support against an external SQL Server authority (virtual tables, Dataverse ETL/sync, or abandoning model-driven for Canvas), before any build proceeds on the current blueprint/implementation-spec
- **evidence**: `_blueprint/blueprint-log.md` v02 (A-009 raised) and v03 (A-009 → C-062, closed); `ux-blueprint_v04/v05.yaml#architecture.record_authority` (external system of record, 3 domains)
- **candidate classification**: **P-B (epistemic integrity)** — an unverified/incorrect technical claim was promoted to Confirmed and used to foreclose the correct architectural question
- **recurring or one-off?**: unclear from 1 pilot, but this class of error (accepting a persona's technical claim without independent verification against real platform constraints) is exactly the failure mode §15 anticipates as "serious" — worth explicit attention in the next pilot regardless of recurrence
- **severity**: **S4** — integrity failure. This is not a nuisance or even a nice-to-have gap: an incorrect technical claim was accepted as Confirmed and became load-bearing for the entire subsequent architecture, blueprint, implementation-spec, and estimate
- **repair suggested?**: NO new pack edit during the pilot (rule held) — but this finding, unlike every other one in this pilot, is a strong, specific candidate for **bounded runtime repair** in post-pilot review: technical claims about platform/connector capability made by solution-architect (or absorbed into a blueprint) should require either a cited, checkable source or should stay Unknown, never Confirmed on the strength of the persona's assertion alone

- **Step 8B adjudication note (2026-09-05)** — appended, original entry above unchanged. **Technical formulation corrected**: the statement "model-driven (Dataverse) apps do not natively run against an external SQL Server as their record authority … a platform-level structural incompatibility" is **withdrawn as a factual assertion**. Current Microsoft Learn (read 2026-09-05): model-driven apps are Dataverse-only, Dataverse virtual tables keep rows in the external source, SQL Server is a supported virtual connector provider with CRUD, and virtual tables are usable by model-driven apps — so `external SQL authority ≠ automatic model-driven disqualifier`. **The integrity finding stands and is sharpened**: C-062 asserted that existing/native connectivity was sufficient to confirm the record-centric/model-driven surface; that conclusion was not supported by an identified connectivity mechanism (virtual tables? replication?) or by evidence that the mechanism satisfies the engagement's material data, security, audit, query and operability requirements. Under the only mechanism consistent with the recorded architecture (virtual tables), O-004's "native row/column security" and "native audit" strengths **do not apply** (no row-level or column security, no auditing, one shared credential, 1,000-record query cap, no dashboards). **S4 preserved** — unsupported load-bearing claim + treated as Confirmed + no authoritative technical evidence + closes a structural architecture question; S4 does not depend on the claim being false. Provenance: sponsor answered "Sim, já há ligação/gateway configurado." to a `would_be_settled_by` that the blueprint itself had defined as a *connectivity* fact; `/answer` wrote an interpretive clause into C-062; blueprint v03 inferred surface fit with no DK pull. Guard audit: **Case A** — `states.md`, `aisa-answer` rules 1/3, `orchestration.md` evidence contract, `aisa-blueprint` DK-pull/CRAFT-boundary/verification-obligation rules already forbade it; `dataverse.md` §14 and `patterns.md` §5 already held the mechanism knowledge. Classification: PR-1 = PROVEN GENERIC DEFECT of **enforcement** at one closure point (structural open choice resolved by `/answer`), repair = strengthen existing guards (`aisa-answer` step 4, `aisa-blueprint` step 15) + TC-1..TC-5 tests; no new principle, state, ledger or router. Full trace: `step-8b-post-pilot-adjudication-report.md` §4–9, §16–17.

---

## REVISED cumulative severity (after post-hoc correction)

```
S0: 4 (unchanged — these remain valid positive observations)
S1: 1 (unchanged)
S2: 0
S3: 2 (NEW — P-OBS-027, P-OBS-028)
S4: 1 (NEW — P-OBS-029)
```

**This changes the pilot's overall verdict.** See revised `step-8-real-engagement-pilot-report.md`.


---

## Step 8B — post-adjudication record (2026-09-05, appended)

Historical entries P-OBS-001..029 and the REVISED cumulative severity above are unchanged. Adjudication in
`step-8b-post-pilot-adjudication-report.md`.

```text
S0: 4 · S1: 1 · S2: 0 · S3: 2 (P-OBS-027 re-rooted; P-OBS-028 reformulated) · S4: 1 (P-OBS-029 — S4 preserved, technical wording corrected)
PILOT 1 HISTORICAL VERDICT: FAIL (unchanged)
P-OBS-029: Case A — existing guards forbade it; enforcement gap at one closure point → PR-1 PROVEN-GENERIC (enforcement)
P-OBS-028: Canvas presumption removed; material interaction-shape omission proven → PR-3 PRACTICE (n=1)
P-OBS-027: 14/14 rules traced; losses 3 / 1 / 2 (capture→SU / SU→Options / Options→Architecture) → PR-2 DOCUMENTATION (PM-U contract drift)
U-028: decision-changing, still open — COMPARATOR EVIDENCE ABSENT preserved
DELIVERABLE CONSUMER VALIDATION: NOT EXERCISED in Pilot 1
PRICING-MARINHA: TARGETED-ARCHITECTURE-REVISIT (escalation condition to DECISION-REVISIT named in the report §18)
RUNTIME MODIFIED IN STEP 8B: NO
```

Also preserved as pilot evidence: P-OBS-014 logged the A-009→C-062 resolution positively and did not challenge
C-062's content — the live instrumentation shared the failure mode it later documented.
