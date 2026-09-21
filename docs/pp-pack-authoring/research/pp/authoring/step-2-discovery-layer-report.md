# PP Pack Authoring — Step 2 Report: Discovery Layer

**Step:** PP PACK AUTHORING — STEP 2 (Discovery layer authoring)
**Date:** 2026-09-03
**Branch:** `pp-pack-authoring/step-2-discovery-layer` (created off `master`; not committed — pending review)
**Scope:** `library/packs/pp/glossary.md`, the Discovery portions of `library/packs/pp/question-bank.md`, and the Discovery `lenses_config` block of `library/packs/pp/pack.yaml`. `technology.constraints_to_check`, `decision_tree`, `domain_knowledge` and `epistemics` were left byte-for-byte unchanged in content (only a scoping comment added), per this step's instructions.

---

## 1. Inputs consumed

| Input | Use |
|---|---|
| `docs/pp-pack-authoring/research/pp/authoring/pp-pack-authoring-map.md` | Transformation plan for this step — §3.1 (glossary SPLIT, question-bank SPLIT+REWRITE), §4.1 (evidence→artifact mapping), §5 (A/B/C/D classification), §6 (neutrality boundary + N-01…N-10 rules + contamination inventory), §8 (traceability convention) |
| `docs/pp-pack-authoring/research/pp/evidence/canonical-manifest.md` | Frozen-baseline confirmation, semantic handling rules (§5), non-blocking reservations (§6) |
| `docs/pp-pack-authoring/research/pp/evidence/decision-criteria.md` §4 | All 116 `DC-D-NNN` bodies — `Discovery evidence` and `States` fields extracted and used as the primary source for every question and every signal |
| `docs/pp-pack-authoring/research/pp/evidence/anti-patterns.md` | §4 register, §8 (Detection Signals are neutral "wherever the underlying evidence allowed it") |
| `docs/pp-pack-authoring/research/pp/evidence/{platform-suitability,application-architecture,data-architecture,automation-architecture,integration-architecture,security,governance,alm-devops,performance-scale,licensing-cost,operations-support}.md` | Each file's "technology-neutral Discovery signals" implication bullet (§9/§10/§11/§13/§14 per file, read in full in Step 1 and re-consulted here) |
| `docs/PACK_AUTHORING.md`, `docs/LENS_AUTHORING.md` | Manifest key shapes, lens signal-extension mechanism, glossary/question-bank conventions |
| `library/kernel/phases.md`, `states.md`, `orchestration.md` | Discovery phase contract, 5 knowledge states, question economics (`custo`/`swing`) |
| `.claude/rules/no-tech-mention-before-options.md` | The binding neutrality rule this whole step is tested against |
| `library/packs/pp/glossary.md`, `question-bank.md`, `pack.yaml` (pre-Step-2, v1.2.0) | Baseline read before rewrite; a full backup of the pre-Step-2 pack already exists untracked at `library/packs/pp-backup/` (found on disk, not created by this step) |

No conflict was found between the Authoring Map and the canonical research during this step. Where the map's own defaults (e.g. §12 Q-08 half-life values) were not yet actioned, they were left as-is — out of this step's scope, not a conflict.

## 2. Files changed

| File | Change | Lines |
|---|---|---|
| `library/packs/pp/glossary.md` | Full rewrite | 95 → 288 |
| `library/packs/pp/question-bank.md` | Full rewrite | 137 → 505 |
| `library/packs/pp/pack.yaml` | Discovery `lenses_config` blocks rewritten; `pack_version` bumped 1.2.0 → 1.3.0; `description` updated to state the neutrality property; `technology`, `deliverables`, `domain_knowledge`, `decision_tree`, `epistemics` sections carried with only scoping comments added, no content change | 92 → 194 |

Landing mechanics: `library/packs/pp/` is guarded fail-closed for the `Write`/`Edit` tools (`.claude/settings.json` → `permissions.deny`, plus `pre-write-guard.py`). Per the Authoring Map's Q-03 and the user's explicit choice this turn, the files were authored in the session scratchpad, a branch `pp-pack-authoring/step-2-discovery-layer` was created off `master`, and the files were copied in via `Bash` (not gated by the Write/Edit guard). **Nothing has been committed** — this is presented for review first, per the chosen option.

## 3. Glossary changes

`glossary.md` is restructured into two parts (Authoring Map §3.1 SPLIT decision):

- **Part A — Discovery vocabulary** (11 sections, A1–A11, ~140 terms): process/work, actors, information, users, exchange-with-other-systems, scale-and-proof, continuity/operations/change, constraint/compliance, money, a "distinctions that must not be collapsed" table (14 rows), and the knowledge-state vocabulary. Every term is phrased so it applies unchanged to a custom build, another low-code platform, or "no new technology" (the test in map §6.1). Every section carries a `Research basis:` header citing the `DC-D-NNN` range and Area ids it derives from; several terms carry their own more specific line.
- **Part B — Contextual vendor vocabulary (quarantined)**: not a dictionary of platform terms, but a **translation table** — "if a participant says X, that is evidence of Y, ask Z instead". Explicitly marked `PHASE: options+`, explicitly forbidden from being used to select or exclude anything. This satisfies the brief's instruction #3: vendor terms are retained only as classified contextual vocabulary that must not imply solution selection.

The old glossary's two structural problems (Authoring Map F-01, F-06) were resolved by removal, not by softening:
- The 6-axis "Discovery fit criteria" rating table (a scoring model) is **gone**. It is not carried forward anywhere in this step — scoring is Block D territory (`decision-criteria.md` §2.3–§2.4) and out of scope until Step 3.
- The ~55-term vendor dictionary that Discovery lenses previously loaded directly is **gone** from Discovery visibility; its content is not deleted from the project (recoverable via `library/packs/pp-backup/` and git history) and is explicitly deferred to the Step 3 Options vocabulary (closing note at the bottom of the file).

## 4. Question-bank design

`question-bank.md` follows the brief's Core/Probe structure exactly (§6 of the instructions):

- **Part 1 — Core questions**: 8 per lens × 6 lenses = **48 questions**. (The brief's target was 5–8; 8 was used uniformly because the `Discovery evidence` fields for the decision-blocking criteria alone (§5 below) filled that budget in every lens without redundancy.)
- **Part 2 — Conditional probes**: **60 questions**, each with an explicit `*Trigger: …*` line, grouped by lens (Business 8, Operations 10, User 8, Data 12, Governance 14, Financial 8). Data and Governance carry the most probes because those two domains carry the densest decision-blocking and irreversible-precondition criteria in the corpus (`decision-criteria.md` §5.2; `security.md`/`governance.md` §10).
- **Appendix A** — signal traceability note (the id in a signal's `pack.yaml` comment is the same id in the matching question's `Research basis:` line — one convention, no separate index, per map §8.6).
- **Appendix B** — the outcome-reachability guard, required by instruction §11 (see §9 below).
- **Appendix C** — everything from v1.2.0 that is *not* Discovery content (the old `technology` lens question list, and the `S1–S9`/`P1–P10`/`M1–M9` implementation-grade "quality gates"), carried verbatim and explicitly marked out of Discovery scope, so nothing from the old file is silently lost before Step 3/4 re-home it (map §6.4, §11).

Every question was checked against the brief's 8 quality rules (§5 of the instructions) during drafting: open-ended, evidence-seeking, no suggested answer, no assumed technology, no assumed automation, moves a knowledge-state, readable by a business participant, and traceable to a canonical finding. The `custo`/`swing` pricing itself is a lens-execution-time act (kernel `states.md`), not authored per-question here; instruction rule 6 is satisfied structurally — every question is written to produce evidence that lands as one of the 5 states.

## 5. Lens signal extensions

`pack.yaml → lenses_config.<lens>.extra_signals`, six Discovery lenses:

| Lens | Signal count (was → now) | Density driver |
|---|---:|---|
| business | 3 → 12 | `DC-D-001…008` (all 8 Business criteria) + 3 cross-cutting (scope, existing capability, prior attempts) |
| operations | 3 → 14 | `DC-D-048…057` (Automation, 10 criteria — the four-shape classification is neutral by construction) + operational-maturity + current-state anchors |
| user | 3 → 15 | `DC-D-009…020` + `DC-D-116` (all 13 Users criteria) + response-time + frontline-reality signal |
| data | 3 → 20 | `DC-D-021…034` (Data, 14) + `DC-D-035, 036, 038, 041, 045` (the neutral half of Integration) + data-quality |
| governance | 4 → 20 | `DC-D-059…073, 075, 077, 079, 080, 107, 108` — Security + Governance + the ALM preconditions that are irreversible-before-build (`security.md`/`alm-devops.md` §10) |
| financial | 2 → 8 | `DC-D-008, 092, 094, 099, 109` + cost-of-doing-nothing + value-horizon + growth |

Signal-naming discipline followed throughout (brief §7 examples): every signal names a fact to notice (`business_criticality_class`, `access_granularity_requirement`, `deployment_model_constraint`), never a question and never a platform noun. Compared against the brief's explicit bad examples — no `power_automate_throttling`, no `dataverse_candidate`, no `power_pages_requirement` — none of that shape exists in the authored set (confirmed mechanically, §7 below).

`technology.constraints_to_check` (5 entries: `premium_licensing`, `dataflow_capacity`, `ALM_environments`, `dataverse_storage_quota`, `DLP_policy_compatibility`) is **unchanged** — explicitly out of this step's scope per the instructions, and per the Authoring Map §3.1 which schedules its rewrite for Step 3 against `decision-tree.md`.

## 6. Canonical coverage matrix

Format: `canonical area → relevant Discovery artifact → coverage status`, per instruction §9. Statuses: `COVERED` / `INTENTIONALLY DEFERRED TO OPTIONS` / `INTENTIONALLY DEFERRED TO IMPLEMENTATION` / `NOT APPLICABLE TO DISCOVERY` / `GAP`.

| Canonical area | Relevant Discovery artifact | Status |
|---|---|---|
| Area 1 — Platform Suitability, §9 signal list | Glossary A1/A6/A9; Q-BUS-02, Q-BUS-03, P-BUS-01/02 | `COVERED` |
| Area 1 — fit matrix, decision boundaries (§1–§3) | — | `INTENTIONALLY DEFERRED TO OPTIONS` (map §5.1: fit verdict is class B) |
| Area 2 — Application Architecture, §10 signal list | Glossary A4; Q-USR-01…08; P-USR-01…08 | `COVERED` |
| Area 2 — surface fit/boundaries (§1–§3.7) | — | `INTENTIONALLY DEFERRED TO OPTIONS`/`IMPLEMENTATION` |
| Area 3 — Data Architecture, §11 signals + §4.11 vocabulary | Glossary A3; Q-DAT-01…08; P-DAT-01…12 | `COVERED` |
| Area 3 — store engineering (§4.2–§4.9) | — | `INTENTIONALLY DEFERRED TO IMPLEMENTATION` |
| Area 4 — Automation Architecture, §14 signal list | Glossary A1 (work shape, elapsed duration, failure semantics); Q-OPS-01…08; P-OPS-01…10 | `COVERED` |
| Area 4 — mechanism limits (`AT2-*`, §5, §7, §8) | — | `INTENTIONALLY DEFERRED TO OPTIONS`/`IMPLEMENTATION` |
| Area 5 — Integration, §13.2 signal list (16 signals) | Glossary A5; Q-DAT-08; P-DAT-09/10; `data.exchange_*` signals | `COVERED` |
| Area 5 — mechanism envelope, topology test (§3–§5, §12) | — | `INTENTIONALLY DEFERRED TO OPTIONS` |
| Area 6 — Security, §10 plane-named signals | Glossary A8; Q-GOV-01…08; P-GOV-01…06, 09 | `COVERED` |
| Area 6 — enforcement mechanics (§1–§4) | — | `INTENTIONALLY DEFERRED TO IMPLEMENTATION` |
| Area 7 — Governance, §10 signals | Glossary A2/A7; Q-GOV-05…08; P-GOV-07/08/10/12 | `COVERED` |
| Area 7 — environment/DLP feature mechanics (§1–§5) | — | `INTENTIONALLY DEFERRED TO OPTIONS`/`IMPLEMENTATION` |
| Area 8 — ALM/DevOps, §10 signals | Glossary A7 (Build isolation, Change-review gate, Testing regime, Reversibility requirement); P-GOV-14 | `COVERED` |
| Area 8 — ALM ladder mechanics, pipelines (§1–§3, §5) | — | `INTENTIONALLY DEFERRED TO IMPLEMENTATION` |
| Area 9 — Performance and Scale, §13 signals | Glossary A6; Q-DAT-03; P-USR-08; P-DAT-09 | `COVERED` |
| Area 9 — meter map, scale envelopes (§2–§6, §8) | — | `INTENTIONALLY DEFERRED TO OPTIONS`/`IMPLEMENTATION` |
| Area 10 — Licensing and Cost, §12 signals | Glossary A9; Q-FIN-01…08; P-FIN-01…08 | `COVERED` |
| Area 10 — unit economics/TCO structure (§1–§2.6, §3, §5) | — | `INTENTIONALLY DEFERRED TO OPTIONS` (never a price in Discovery — map §6.3 N-04) |
| Area 11 — Operations and Support, §11 signals + §0 central question | Glossary A2/A7; Q-GOV-06/08; P-OPS-09; P-GOV-08 | `COVERED` |
| Area 11 — monitoring/backup/support mechanics (§2–§3, §5–§6) | — | `INTENTIONALLY DEFERRED TO IMPLEMENTATION` |
| Area 12 — Architecture Patterns | — | `NOT APPLICABLE TO DISCOVERY` (map §5.1: pure class B — candidate options and trade-offs; no independent Discovery signal set exists for this area) |
| Block D — Decision Criteria, 116 `DC-D` `Discovery evidence` fields | Glossary (all sections); every core question and 56 of 60 probes | `COVERED` — 113/116 by direct id citation, 3 more (`DC-D-039`, `082`, `093`) by explicit section-range citation; see §10 below for why those three keep a design-dependent remainder deferred |
| Block D — Decision Criteria, §2.5/§5/§6/§7/§4A (exit classes, blocking set as a *mechanism*, outcome classes, volatility register, comparator rules) | — | `INTENTIONALLY DEFERRED TO OPTIONS` — explicitly out of this step's scope ("Do NOT author Options/Decision logic yet") |
| Block D — Anti-Patterns, `Detection Signals` fields (neutral subset) | Glossary A10 (14 collapse-pairs); 34 of 68 `AP-D-NNN` cited directly across questions | `COVERED` for the neutral subset |
| Block D — Anti-Patterns, `GATE`/`CONSTRAINT` verdicts, composed disqualifiers, non-neutral signals (per anti-patterns.md §8, some entries say so themselves) | — | `INTENTIONALLY DEFERRED TO OPTIONS` |
| Block D — Alternatives, trigger-to-class map (§5.1) | Underlying requirement signals covered (`existing_capability_overlap`, `source_of_record_per_entity`, etc.); the 11 class *names* themselves are not | `COVERED` (requirement side) / `INTENTIONALLY DEFERRED TO OPTIONS` (class-naming side) |
| Block D — Decision Intelligence Matrix (composed rows, evaluation order, outcome-class render strings, adversarial scenarios) | — | `INTENTIONALLY DEFERRED TO OPTIONS` — pure class B, Step 3 scope |

**No unexplained `GAP` row.** Every canonical area maps to at least one `COVERED` Discovery artifact for its neutral content, with the design-dependent or platform-specific remainder explicitly and reasonedly deferred.

## 7. Technology contamination scan

Performed on every file changed in this step (§2), against the required term list plus the map's own denylist candidates.

**Method**: exact-word regex sweep for `power platform`, `power apps`, `canvas`, `model-driven`, `dataverse`, `power automate`, `power fx`, `sharepoint`, `microsoft lists`, `copilot`, `power pages`, `premium connector`, `environment strategy`, `\bsolution\b`, `managed solution`, case-insensitive, over the full text of `glossary.md`, `question-bank.md`, and `pack.yaml`.

| File | Hit | Location | Classification | Why |
|---|---|---|---|---|
| `glossary.md` | "Power Platform" | Line 1, file title (`# Power Platform Pack — Glossary`) | `CONTEXTUAL AND SAFE` | The pack's own filename-equivalent identity; it never appears inside a Discovery term, question or signal. No lens reasons from this line. |
| `glossary.md` | "solution" | Part B row: *"we'll just ship it as a solution / package"* | `CONTEXTUAL AND SAFE` | A quoted **participant phrase** inside the translation table, whose entire purpose is to redirect that phrase to a neutral question (*"What is the release window, who approves…"*). The row does not adopt the word as vocabulary; it defuses it. |
| `question-bank.md` | "Power Platform" | Line 1, file title | `CONTEXTUAL AND SAFE` | Same as above — file identity, not reasoning content. |
| `pack.yaml` | "Power Platform" | Comment line, `lenses_config:` header: *"...the PP mapping happens in Options via lens-technology."* | `CONTEXTUAL AND SAFE` | An author-facing YAML comment explaining the phase boundary itself — not a signal name, not consumed by any lens at runtime. |
| `pack.yaml` | "dataverse_storage_quota" | `technology.constraints_to_check` | `NON-DISCOVERY CONTENT` | Inside the `technology` block, active in Options only, explicitly preserved unchanged per this step's instructions ("Do NOT author `technology` content... Preserve any existing technology/Options configuration"). Not part of any Discovery lens's signal set. |

No other hit, of any term on the required list, in any changed file.

`DISCOVERY TECHNOLOGY CONTAMINATION VIOLATIONS: 0`

## 8. Traceability validation

Applied the exact convention from `pp-pack-authoring-map.md` §8 — a `Research basis:` line, most-specific-id-first, with disambiguation by file-qualification for overloaded Area ids. No second convention was invented.

**Mechanical checks run:**

1. **`DC-D` namespace** (116 ids) — exhaustively enumerable. 113 cited by exact string; the remaining 3 (`DC-D-039`, `082`, `093`) are cited via their section's explicit id-range header (e.g. `DC-D-035…DC-D-047`) rather than individually, which is the convention's own stated form for class-level attribution — not a gap (§10 explains the substantive reason for each).
2. **`AP-D` namespace** — 34 of 68 ids cited directly, all resolved against `anti-patterns.md`'s register.
3. **Area-local ids** (`PS-`, `AA-`, `DA-`, `AT2-`, `IA-`, `SEC-`/`S-`, `GOV-`/`G-`, `ALM-`/`D-`, `PF-`, `LC-`, `OP-`, `SC-`, `DQ-`, `SY-`, `VT-`, `SQ2-`, `NB-`) — every occurrence checked with a Python word-boundary match against the actual canonical evidence files (not a substring match, which would have produced false positives against ids like `GOV-XB-01`). All resolved.
4. **File-qualification** — where an id is drawn from a specific Area file rather than Block D, the file is named inline (e.g. *"operations-support.md §1.1"*, *"licensing-cost.md LC-28"*), per §8.2 of the convention.

`BROKEN CANONICAL REFERENCES: 0`

No claim ledger was created; no per-sentence ids; the convention stayed exactly as scoped (§8.6 of the map — a maintainer with `grep` and no tooling can resolve every reference).

## 9. Bias check (instruction §11)

Ran the required test: can a Discovery round using only this bank plausibly conclude each of the five outcomes the brief lists? Documented as **Appendix B** inside `question-bank.md` itself (so it travels with the artefact, not just this report), with a table naming which questions can produce evidence for each outcome:

| Outcome | Can the bank reach it? | Evidence path |
|---|---|---|
| Power Platform is appropriate | Yes | Positive answers across the core sets; no constraint engaged |
| Power Platform is appropriate with constraints | Yes | Q-BUS-02 (criticality), Q-GOV-06 (ownership), P-FIN-01 (unfunded control), P-OPS-09 (maturity gap) |
| Another technology is preferable | Yes | Q-GOV-02 (deployment-model constraint — can eliminate a whole class on its own), P-DAT-02 (cross-system atomicity), P-OPS-03 (real compute), P-GOV-13 (portability), Q-DAT-08 + P-GOV-08 (existing capability already owns it) |
| Process change without new technology | Yes | P-BUS-01 (requirement is a feature list of the outgoing tool), Q-BUS-07 (value vs cost of ownership), Q-OPS-07 (unjustified variants) |
| Do nothing / defer | Yes | Q-FIN-02 (cost of doing nothing), Q-FIN-03 + P-FIN-01 (unfunded), Q-BUS-04 (no real driver behind the date), any unresolved decision-blocking Unknown |

No question in the core or probe set presupposes automation is desirable, presupposes a build is needed, or is phrased as a comparison against a platform threshold (checked individually against brief rule §5.4/§5.5 during drafting, and spot-checked again for this report). Signals name things to notice, never solutions (§5 above, and mechanically confirmed in §7).

`DISCOVERY OUTCOME BIAS CHECK: PASS`

## 10. Gaps / deferred knowledge

**Genuine authoring gap found and fixed during this step**, not merely deferred:
`DC-D-076` (source-control requirement), `DC-D-078` (team size/concurrent development) and `DC-D-081` (automated-testing requirement) had **no** Discovery representation at all in the first draft — not even by section range, because the A7 glossary header originally started its range at `DC-D-077`. Fixed by: (a) widening the A7 header to `DC-D-076…DC-D-083`; (b) adding three glossary terms (**Build isolation**, **Change-review gate**, **Testing regime**); (c) adding probe **P-GOV-14** (*trigger: more than one person will build or maintain this, or a compliance regime requires a change-to-approval trace*). This is recorded here rather than silently folded in, because it is exactly the kind of drift the map's gate G8 (coverage) exists to catch, and it is worth the team knowing it happened once already in Step 2.

**Deliberately partial, not gaps:**

| Criterion | Why the remainder stays in Options |
|---|---|
| `DC-D-039` — per-mechanism throughput ceiling | Its own `Discovery evidence` field requires knowing *which mechanisms are on the path* — that is design knowledge, not a Discovery fact. The requirement-side sibling, `DC-D-040` (sustained end-to-end throughput at horizon), *is* a full Discovery question (`P-DAT-09`). |
| `DC-D-082` — environment count required by the lifecycle | A near-duplicate of `DC-D-071` (environment strategy requirement, fully covered — `Isolation domain` term, `environment_isolation_requirement` signal). The corpus itself names this pattern (`decision-criteria.md` §3.2, "near-duplicate clusters — one elicitation, two dimensions"); asking both separately would double-elicit the same fact. |
| `DC-D-093` — entitlement fit of the required capability set | Its `Discovery evidence` field opens with *"the connector and capability list the design requires"* — inherently Options-dependent (you cannot check entitlement fit before a candidate design exists). The elicitable half — audience size, current entitlement holdings — is fully covered (`DC-D-094` via Q-FIN-05, `DC-D-109` via Q-FIN-06, plus the `Entitlement`/`Entitlement exposure` glossary terms). |

**Structurally deferred (not this step's scope, not a gap):** all Options/Decision-logic content — exit classes, outcome classes, the blocking-set *mechanism* (as distinct from the requirement-side questions, which are covered), composed disqualifiers, the alternatives class-naming, the decision-intelligence matrix, and `decision-tree.md` itself. All scheduled for Step 3 per the Authoring Map's sequence (§9, stages S3–S6). All implementation-grade domain knowledge (store engineering, mechanism limits, enforcement mechanics, ALM ladder mechanics) is scheduled for Step 4.

**Carried, not lost:** the v1.2.0 `technology`-lens question list and the `S1–S9`/`P1–P10`/`M1–M9` quality gates are preserved verbatim in `question-bank.md` Appendix C, explicitly marked out of Discovery scope, pending their Step 3/4 re-homing per map §6.4 and §11.

**Open from Step 1, unaffected by this step:** map §12 Q-02 (decision-layer language — English vs `pt`) and Q-08 (half-life override values) remain open; neither blocks Discovery authoring and neither was touched here.

## 11. Recommended Step 2 Gate scope

Per the Authoring Map's gate design (§10), the gates relevant to a Discovery-layer authoring step are:

- **G1 — canonical reference resolution**: run the exhaustive `DC-D`/`AP-D` check plus the word-boundary Area-id check (both already run manually in §8 above; recommend scripting them as the permanent G1 check rather than re-deriving by hand each step).
- **G2 — Discovery neutrality**: run the denylist sweep (§7 above) as the permanent G2 check; recommend formalising the term list into `neutrality-denylist.md` now (Authoring Map §3.7, `CREATE`) so future rounds don't hand-maintain the regex.
- **G3 — unsupported assertion**: **not fully applicable yet** — this step's `RESEARCH`-class content states no numeric threshold and no comparative claim by construction (Discovery never carries a number, rule N-04), so there is nothing for G3's "unbasis'd numeral" check to find. Recommend a light pass confirming that remains true (it does — no digit-bearing sentence in `glossary.md`/`question-bank.md` states a platform limit) rather than the full G3 sweep, which is more consequential once Options content exists.
- **G6 — duplication and conflict**: recommend checking the new `pack.yaml` signal list against the (not-yet-authored) `decision-model/criteria-register.md` once Step 3 lands, to confirm no criterion is elicited under two different signal names.
- **G8 — coverage**: the matrix in §6 above **is** the G8 check for this step; recommend it be re-run automatically (id-extraction script + range-expansion) rather than manually next time, since the manual run is what caught the `DC-D-076/078/081` gap in §10.
- **G0, G4, G5, G7**: not applicable to this step — G0 (structural) has nothing new to break, G4/G5 apply once Options decision logic exists, G7 (volatility stamping) applies once volatile canonical facts are encoded as pack rules (this step encodes none — Discovery states no platform fact).

Recommend running the Step 2 Gate on **G1, G2, G8** as scoped above before merging this branch; G3/G6/G7 as light advisory passes; G0/G4/G5 skipped as not-yet-applicable.

---

`DISCOVERY GLOSSARY AUTHORED: YES`
`DISCOVERY QUESTION BANK AUTHORED: YES`
`DISCOVERY LENS SIGNALS AUTHORED: YES`
`UNEXPLAINED CANONICAL DISCOVERY GAPS: 0`
`DISCOVERY TECHNOLOGY CONTAMINATION VIOLATIONS: 0`
`BROKEN CANONICAL REFERENCES: 0`
`DISCOVERY OUTCOME BIAS CHECK: PASS`
`READY FOR STEP 2 AUTHORING GATE: YES`

---

## Addendum — 2026-09-04: superseded by runtime simplification Phase G

Nothing above was rewritten. Three statements no longer describe the runtime and are recorded here so
the report stays accurate:

1. **§5 signal counts (89 across six lenses) are superseded.** `pack.yaml` now carries 36 cues
   (business 5 · operations 7 · user 5 · data 7 · governance 7 · financial 5) after the survival test
   and consolidation the runtime-simplification plan §9 scheduled. `pack_version` is 1.4.0.
2. **§4 question counts (48 core + 60 probes) are superseded** — 35 core + 34 probes. Retired ids are
   listed in the Phase G report §4; surviving ids were **not** renumbered, so every id cited in §6, §9
   and §10 above still resolves to the same question or is listed as retired.
3. **§8's traceability convention no longer holds.** The `# DC-D-NNN` comments in `pack.yaml` and the
   `Research basis:` lines in `question-bank.md` / `glossary.md` were removed: PP runtime carries zero
   canonical ids. The complete runtime→research mapping — surviving cue → basis, and which criteria
   lost their standing cue while keeping Discovery representation — is in
   `runtime-simplification-phase-g-report.md` §9. `BROKEN CANONICAL REFERENCES: 0` still holds; the
   references moved to the authoring side rather than breaking.

The §6 canonical coverage matrix verdicts are unaffected: for every criterion that lost a cue, the
artifact carrying its Discovery representation changed (universal lens cue or a triggered probe), not
the fact of coverage. `question-bank.md` Appendix C is preserved verbatim in the Phase G report §9.4.
