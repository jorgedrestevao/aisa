# Runtime Simplification — Phase C (Lenses) Report

<!--
provenance: IMPLEMENTATION (7 lens SKILL.md files rewritten; nothing else touched)
scope: .claude/skills/lens-{business,operations,user,data,governance,financial,technology}/SKILL.md
authored: 2026-09-04
basis: runtime-simplification-plan.md §7 + §11 Phase C; phase-a-report.md (contracts); phase-b-report.md (shared evidence)
path note: written to the repo's actual `research/pp/authoring/` directory
  (`docs/pp-pack-authoring/research/pp/authoring/`), alongside the plan and the Phase A/B reports.
-->

## 1. Summary

The seven lens files were rewritten to the Phase A contract: **lens = perspective + minimal runtime
contract**. The six mandatory sections are preserved in order; what shrank is everything that
restated a kernel contract, enumerated the filesystem, or turned signals into coverage.

Removed from every Discovery lens: the "open and PARSE every file in `inputs/`" instruction, the
1.5 a–d capture protocol with its **mandatory `≥1 PM` raw spot-check**, the per-signal coverage loop
("for each signal not yet covered → Confirmed/Assumed/Unknown"), the `pp pack additions:` line, the
round/next-free-id bookkeeping, the `council-log.md` append, and the full local definitions of
`verificado_em` / `validade` / `custo` / `swing` / expiry.

Retained and, in several lenses, sharpened: the perspective — what this lens notices that the others
miss, and what it naturally distrusts.

Net: **−13,976 characters (−32%)** of lens framework text; deletions exceed additions by roughly 5:1.
Per Discovery round the six lenses now load ~24.0k instead of ~36.6k characters.

## 2. Per-lens before / after

| Lens | Chars before | Chars after | Δ | Lines before | Lines after |
|---|---:|---:|---:|---:|---:|
| business | 6,259 | 3,997 | −36% | 66 | 55 |
| operations | 6,086 | 4,099 | −33% | 66 | 55 |
| user | 5,949 | 3,991 | −33% | 66 | 55 |
| data | 6,383 | 4,027 | −37% | 67 | 55 |
| governance | 6,394 | 4,264 | −33% | 64 | 55 |
| financial | 5,977 | 4,012 | −33% | 64 | 55 |
| technology | 6,691 | 5,373 | −20% | 86 | 66 |
| **total** | **43,739** | **29,763** | **−32%** | **479** | **396** |

Size is reported as a diagnostic, per plan §7 — no limit is asserted and no validator was added. The
files sit above the plan's ~1,600-character indicative target: the residue is the six-section
scaffolding itself (Inputs pointer, Outputs shape, six hard rules, cue framing), which every lens
needs locally. Everything that could be replaced by a pointer was.

`lens-technology` shrinks least by design — its Role, its constraint reasoning and its pull-based pack
rule are the parts worth spending on.

## 3. Perspective preserved

Verified per lens (Role + execution step 2, the only step that differs materially between lenses):

| Lens | Still notices |
|---|---|
| business | declared vs **evidenced** impact and urgency; who actually senses the pain; decision authority; the veto-holders nobody invited; why now; prior attempts |
| operations | one real instance end to end; exceptions and their frequency; waits, rework, manual re-keying; discretionary calls; single-person dependencies; operational ownership; peak vs steady-state volume. Keeps the sharp stance verbatim: **"You distrust the documented process."** |
| user | distinct user populations; context of use (place, device, connectivity, language); friction in the users' words, not the sponsor's; accessibility; **who is asked to work harder — where adoption fails**; hands offline/sensitivity tensions to data + governance |
| data | entities and owners; **quality read off the column profile, not off an assertion**; sensitivity classification; retention/residency lifecycle; lineage, duplication, systems of record, data dependencies; records sensitivity so governance can adjudicate |
| governance | the **conflict scan first** — earlier lenses' stated needs against policy, with collisions becoming `Conflicted` rows (`partes`, `criticidade`) and **never silently resolved**; authority, separation of duties, provability at audit, privacy, go-live approvals |
| financial | as-is cost from volume × cycle time × loaded rate with the arithmetic visible and declared `Assumed`; cost of doing nothing and of delay; budget envelope, funding model, thresholds; **which input the estimate is most sensitive to** |
| technology | architectural fit against the framed problem; integration surface; security; governance fit; ALM/lifecycle; scale; operability; cost implications; reversibility; effort band — with a do-nothing and a non-technology option mandatory |

Homogenization check: Role and step 2 differ substantively across all seven; only Inputs/Outputs/Hard
rules/cue framing are shared, and those are the runtime contract, not the perspective.

## 4. Framework duplication removed

| Deleted content | Copies | Now owned by |
|---|---:|---|
| "Every file in `inputs/` — open and PARSE each one" + format→tool table pointer | 7 | `orchestration.md` → *Evidence contract* (capture parses once) |
| Step 1.5 a–d process-capture protocol (~1,200 chars each) | 6 | `orchestration.md` → *Evidence contract* + `aisa-capture` |
| **Mandatory `≥1 PM` raw spot-check per lens per round** | 6 | deleted outright — replaced by materiality-based verification |
| Per-signal coverage loop ("for each signal not yet covered…") | 6 | deleted outright — signals are cues |
| `pp pack additions:` line (incl. vendor-vocabulary leaks) | 6 | pack manifest; injected by the orchestrator in Phase D |
| Inlined 5-constraint PP list in the signal catalog | 1 (technology) | `lenses_config.technology.constraints_to_check` |
| Full `verificado_em`/`validade`/`custo`/`swing`/expiry definitions | 7 (~1,000 each) | `states.md`; lens keeps obligation + `organizacional` default |
| SU append mechanics prose | 7 | `states.md`; lens keeps one clause |
| Engagement path resolution, `context.json`, memory paths, `<engagement>` resolution | 7 (~380 each) | the invocation (Phase D) |
| Round + next-free-id bookkeeping | 7 | `aisa-round` |
| Final `council-log.md` append step | 7 | `aisa-round` step 5c (already did it) |

Test applied to every surviving instruction: *if this disappeared, would Claude materially perform
worse?* Six hard rules survived it — vendor neutrality, no `Confirmed` without evidence, evidence
integrity (cite what you opened; never overstate), append-only, stamp/price with local default, and
expired-reads-as-weak. Everything else became a pointer.

## 5. New Inputs behavior

Each Discovery lens now says, in three sentences:

- shared evidence first — `_capture/evidence-index.md` is a **source map**: what sources exist, which
  are normalized, where that evidence lives, what failed or was skipped;
- **read the normalized evidence bearing on this perspective, not every file** — there is no
  requirement to consume every normalized artefact, and no requirement to enumerate `inputs/`;
- raw sources stay openable and are inspected **when material to confidence, never to fill a quota**,
  with the trigger list owned by `orchestration.md`.

Plus one line naming what the lens privileges (business: statements of consequence · operations:
accounts of how the work really runs · user: first-person accounts of use · data: the column profile
in the extractions · governance: stated rules and authority · financial: volumes, cycle times, rates,
budgets · technology: the full cross-lens SU).

The Inputs section closes by naming what the invocation carries (round id, next free SU ids, the SU,
prior lens outputs, pack cues) — so the lens is ready for the Phase D payload without depending on it
today.

## 6. Signal behavior

Every lens opens its catalog with: *"Cues, not coverage: follow what is material here; an uncovered
cue is not a gap and never becomes an `Unknown`."* The catalog is a bare token list, no prose.

No lens contains "not yet covered", "every signal", "must be covered" or an equivalent loop
(grep-verified, 0 hits across all seven).

Pack cues are **not** loaded by the lens. Each Discovery lens carries one line — *"The invocation may
carry extra runtime cues — same status"* — which is enough to receive Phase D's injection without
knowing that packs, manifests or `pack.yaml` exist. No Discovery lens references `pack.yaml`
(grep-verified).

Universal catalogs were kept and lightly sharpened where the old token was vague
(`impact_declared` → `impact_declared_vs_evidenced`) or where §10's required perspective was implicit
rather than named (`operational_ownership`, `adoption_risk`, `data_dependencies`, `privacy_obligations`,
`cost_sensitivity`, `funding_model`).

## 7. Technology-lens behavior

- **Options-only, unchanged.** `## Phase gate` is kept verbatim in force (active in Options/Decision;
  refuses in Discovery/Framing with the `phases.md` pointer), and execution step 1 checks it before
  anything else.
- **Role re-aimed at evaluation**: it assesses candidate options against the requirements and
  constraints Discovery and Framing surfaced, and explicitly does not re-open what the problem is.
- **Perspective preserved across all eight dimensions** the brief names: architectural fit,
  integration, security, governance, lifecycle/ALM, scale/performance, operability, cost implications
  — plus reversibility and the effort band.
- **Domain knowledge is pull-based.** The lens may resolve the active pack and consult *the branch it
  is actually evaluating*, *the domain-knowledge file bearing on the question in front of it*, and
  `lenses_config.technology.constraints_to_check`. The instruction not to load the base by default is
  explicit.
- **The inlined PP constraint list is gone.** The lens says the pack declares its constraints and
  where — it does not restate them. No platform knowledge is duplicated in the lens file.

## 8. Tests / checks

Existing checks, all green:

| Check | Result |
|---|---|
| `python library/kernel/tools/tests/test_text_extract.py` | 23 tests, **OK** (~53 s) |
| `dashboard.py --engagement <slug>` on all 4 engagements | all build |
| `pre-lens-order-check.py` on a temp fixture — no prior lens output | **blocks** `lens-operations` with the round-R-01 message |
| `pre-lens-order-check.py` — business wrote the new `## R-01 — business` 3-heading block | **allows** `lens-operations` (the new output shape satisfies the hook's round-id grep) |

Static verification:

| Assertion | Result |
|---|---|
| all seven lenses exist | yes |
| six mandatory sections, in order, in all seven | yes (`technology` additionally keeps `## Phase gate` between Role and Inputs) |
| frontmatter `name` + `description` in all seven | yes |
| `grep -in "pp pack additions\|excel_anchors\|sharepoint\|DLP_policies\|sensitivity_labels\|pack.yaml\|Power Platform\|Dataverse\|Power Automate\|Canvas\|OutSystems\|Mendix\|Excel\|premium_licensing\|RBAC_complexity\|environment_strategy"` across the 6 Discovery lenses | **0 hits** |
| coverage-loop semantics (`not yet covered`, `every signal`, `must be covered`, `for each signal`) across all 7 | **0 hits** |
| spot-check quota (`spot-check`, `≥1 PM`) across all 7 | **0 hits** |
| read-all-inputs semantics (`Every file in`, `open and PARSE`, `always read`) across all 7 | **0 hits** |
| `council-log` appends in any lens | **0 hits** |
| `## <round> — <lens>` header present in all 7 | yes |
| pointers resolve: `orchestration.md`, `states.md`, `phases.md`, `no-tech-mention-before-options.md`, `decision-tree.md`, `domain-knowledge/`, `lenses_config.technology.constraints_to_check` | all resolve |

No test was added, and no existing test assumed the old verbose lens contract — the only automated
dependency on lens output shape is `pre-lens-order-check.py`'s round-id grep, which the new header
satisfies (tested above).

Not re-run here: a live `/round` on an engagement. It writes engagement state, and Phase D is what
provisions the invocation payload the new `Inputs` section describes; running it now would exercise a
half-wired path. The hook-level fixture test covers the one mechanical dependency.

## 9. Files changed

Modified (7, all of them lens skills):

1. `.claude/skills/lens-business/SKILL.md`
2. `.claude/skills/lens-operations/SKILL.md`
3. `.claude/skills/lens-user/SKILL.md`
4. `.claude/skills/lens-data/SKILL.md`
5. `.claude/skills/lens-governance/SKILL.md`
6. `.claude/skills/lens-financial/SKILL.md`
7. `.claude/skills/lens-technology/SKILL.md`

Not touched: `library/**` (kernel contracts, tools, **and the whole PP pack** — `pack.yaml`,
`question-bank.md`, `glossary.md`), `.claude/agents/*`, every orchestrator skill (`aisa-round`,
`aisa-frame`, `aisa-options`, `aisa-status`, `aisa-start`, `aisa-capture`), every hook, `docs/*`, and
everything under `projects/`.

Known stale line left in place: `docs/IMPLEMENTATION_PLAN.md:873` still quotes the old
"1-3 paragraph narrative" output. It is a historical build plan, not a live contract, and
`docs/LENS_AUTHORING.md` (Phase A) is authoritative.

## 10. Deferred Phase D work

Owned by Phase D, deliberately not implemented here:

- `aisa-round` step 3.6 — read `_capture/evidence-index.md` and carry it into each lens invocation;
- pack signal injection — resolve `_state.json.pack → lenses_config.<lens>.extra_signals` and inject
  the cue string with its mandatory *"cues, not a checklist; uncovered cues are not gaps"* clause;
- invocation payload — round id, next free SU id per section, engagement paths and memory pointers
  (the lens files now name these as invocation-carried rather than resolving them);
- text-source freshness in `aisa-round` step 3.5 (still hashes `.xlsx`/`.xlsm` only);
- `aisa-status` step 6 — the single `question_bank` consumer;
- council launch changes (`aisa-frame` / `aisa-options` step 5 still instruct personas to read their
  lens `SKILL.md` "for the hard rules" — that pointer still resolves, since the rewritten files keep
  a Hard rules section; removing it is Phase E).

Also deferred: Phase E (persona trim), Phase F (`aisa-start` SU scaffold), Phase G (PP `extra_signals`
trim to the 5–8 heuristic under the survival test).

Until Phase D lands, a lens invoked without the payload falls back to reading the engagement files it
is told about and `_capture/evidence-index.md` directly — nothing points at a file that does not
exist, and no lens depends on an injection that has not been wired.
