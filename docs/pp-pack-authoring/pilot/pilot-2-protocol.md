# Pilot 2 — Protocol (pack pp 1.8.2, Step 8C baseline)

> Starts from the Step 8C checkpoint recorded in
> `step-8c-consolidated-runtime-repair-report.md` (§20). Pilot 1's protocol items that were not
> exercised are carried here unchanged; the fresh-session adversarial test is new. Nothing in this
> protocol is runtime: it is what the observer does and records.
>
> **Step 8D carry-forward (2026-09-06).** The pricing-marinha targeted architecture revisit
> (`step-8d-pricing-marinha-targeted-architecture-revisit.md`) is PASS / CLOSED; its runtime observations
> OBS-8D-05, OBS-8D-07, OBS-8D-08 and OBS-8D-12 are carried into §4–§5 below as watch items and one protocol
> requirement. Pack stays `1.8.2`; Step 8C.1 stays FROZEN; nothing in §2–§3 was weakened or removed.

## 1. Preconditions

- Baseline = the commit the tag `step-8c-baseline` resolves to (`git rev-parse step-8c-baseline^{commit}` — the Step 8C.1 freeze correction included); `pack_version: 1.8.2`; full suite green.
- The engagement is real (not a Pilot-1 replay) and has at least two normalized source kinds
  (a structured workbook and at least one document or transcript), so the cross-source synopsis is
  actually exercised.
- `projects/pricing-marinha/**` is **not** the Pilot-2 engagement. Its targeted architecture revisit ran
  separately from the same checkpoint (Step 8B §18 → Step 8D, PASS) and left that engagement's architecture
  **independently OPEN** (blueprint v06 not approved). Pilot 2 does **not** wait for it — see §6.

## 2. Fresh-session adversarial test (PR-6 — new)

```text
Session A — run Discovery to its soft exit (/round … until /frame's gate is green or overridden
            with a logged reason). Close the session. Keep no notes outside the repository.

Session B — a NEW session with NO prior transcript. It is given ONLY the `Read to resume` block
            that /status derives for the current phase — nothing else is pre-loaded.
```

Session B must, from the declared read set alone:

| # | Test | PASS when |
|---|---|---|
| 1 | **Process teach-back** — explain the current business process without naming any future solution | every material output family is traced to inputs, transformations, deciding actors and consumers — or its missing link is named as an explicit `Unknown` |
| 2 | **Invariants** — name the behaviours the business cannot lose | each one is an SU id (or `(none) — reason` in the frame block) |
| 3 | **Structural constraints** — name the conditions that could eliminate or reshape whole solution classes | each is an SU row, or an explicit `Unknown` with `swing: decisivo` |
| 4 | **Decision-changing Unknowns** — name them | they match the SU and the frame block |
| 5 | **Continue** — run `/frame` (or `/options` if Framing was closed in Session A) | the round proceeds on the persisted state; no request to "see the previous conversation" |

Record, per test:

- **lost material concepts** — present in the evidence or in Session A's reasoning, absent from Session B's account;
- **invented concepts** — stated by Session B with no SU id, synopsis line or locator behind them;
- **raw-source rereads** — every `*.text.md`, `inputs/` or `process-model.md` §2–§5 open Session B needed, and whether the synopsis/SU should have answered it;
- **unnecessary context** — anything in the read set Session B never used.

No new handoff artefact may be written to make the test pass. If Session B needs something the read set
does not carry, that is a finding against the synopsis / SU / frame block — not a reason to add a file.

## 3. Watch items carried from Pilot 1 / Step 8B / Step 8C

| Item | What to watch | Trigger for action |
|---|---|---|
| **PR-3 — experience-surface / task derivation** (`PILOT-2 WATCH ITEM`) | Does the blueprint's surface selection *record* the interaction-shape evaluation (task shapes: wide-grid entry, what-if, review, approve; computed columns visible to users) now that the synopsis carries material user tasks? Do screens serve tasks the SU/synopsis name? | If the interaction shape is again missed with the task semantics available → evaluate the **smallest** existing-contract strengthening of `aisa-blueprint` (one sentence at step 3/4). Do not pre-empt it. |
| Unverified technical claims | Any `Confirmed` row whose content is a platform capability or configuration and whose evidence is a business sponsor's yes/no; any structural `open_architecture_choices` entry closed without a recorded A / B / C basis | A single occurrence is a PR-1 enforcement regression — record the closure point |
| Deliverable consumer validation (not exercised in Pilot 1) | sponsor Executive-Report read; architecture handoff read; implementation handoff read; independent Estimate comparison (a developer/lead estimate to compare with Mode A) | Execute all four; record usefulness findings separately from framework findings |
| `solution_name` / A8 / A9 gaps | Do they recur at first `/render --dry-run`? | Recurrence → candidate template-prompt strengthening (Step 5/6 remain frozen unless the gate reopens them) |
| Cross-source synopsis cost | One heavier capture pass vs lighter Options/Architecture reads; source dispositions `USED` / `CHECKED` / `TARGETED` honest (a `CHECKED` source was actually inspected) | A synopsis that loads every transcript in full, or marks sources `CHECKED` unread, is a contract violation |
| Disposition burden | Count of `MAP` / `ADOPT` / `DISMISS` per round; time spent; whether `DISMISS` reasons are real | Ceremony without semantic benefit → revisit the labelled-line convention, never the principle |
| Teach-back trigger | Did `/status` group HYPOTHESIS/UNKNOWN items into one `reuniao` item? Did each covered Unknown close independently via `/answer`? | A "process confirmed" collapse row is a defect |
| Targeted revalidation | On any `/answer` or blueprint version that changes a premise: was the dependents list written (`still valid` / `revalidate`), or `(none)` for unrelated facts? Any broad "rerun" behaviour? | Silent carry-forward or wholesale rerun are both defects |

## 4. Watch items carried from Step 8D (observe and record — no runtime change during the pilot)

| Item | What to watch | What to record | Trigger for adjudication (after the pilot) |
|---|---|---|---|
| **OBS-8D-05 — selective rehydration cost** | Does the derived `Read to resume` set remain sufficient as the normal bootstrap, with only genuinely targeted additional pulls? Step 8D needed `options.md` and `answers.md` on top of the decision/architecture set (to revalidate Decision strengths and to check a verbatim answer) — legitimate targeted pulls, not failures. | For **every** fresh-session continuation: `default read-set files` · `targeted additional files` · `why each additional pull was necessary` · `whether the same pull recurs repeatedly` | The same supposedly non-default authority is **repeatedly** required to resume normal work in the same phase. Do **not** expand the runtime read-set during the pilot — record first. |
| **OBS-8D-07 — non-expired `Confirmed` revalidation** | Any case of `Confirmed row` + `still inside its validity window` + `new evidence / adjudication / premise change` → its truth or scope must be reconsidered. Step 8D had to route C-062 through the `--revalidate` "changed" fallback (written for expired rows) because no command re-questions a non-expired Confirmed row; `states.md` lists the `Confirmed → Unknown` transition but no skill executes it for that case. Observe whether the runtime offers a natural executable path. | `original row` · `changing evidence` · `attempted command` · `actual transition` · `whether manual/workaround reasoning was required` | A **second** case (Step 8D is the first) requires an undocumented or improvised path to reopen/revalidate a non-expired Confirmed row. No runtime repair during Pilot 2. |
| **OBS-8D-08 — `/revisit` readiness** | Pilot 1 never ran `/simulate`, so `_simulation/counterfactuals/` did not exist and `/revisit` would have stopped at "missing counterfactual" had Step 8D needed to escalate. §5 below makes `/simulate` before `/decide` a **protocol requirement** for Pilot 2. If a tripwire/revisit opportunity occurs naturally, execute `/revisit` and observe whether the persisted counterfactuals make the path usable. | `/simulate executed: YES/NO` · `counterfactuals persisted: YES/NO` · `/decide consumed them correctly: YES/NO` · (if it occurs) `/revisit usable on persisted counterfactuals: YES/NO` | `/revisit` remains structurally unusable even though the normal `/simulate → /decide` path was followed. Do **not** manufacture a tripwire to make the test pass. |
| **OBS-8D-12 — blueprint syntax integrity** | Pilot 1's approved `ux-blueprint_v05.yaml` is not strictly parseable YAML (a conditional key indented inside a list); the runtime reads blueprints as text, so nothing failed and the version was approved. For **every** blueprint version generated in Pilot 2, validate that the artefact parses as YAML (e.g. `python -c "import yaml; yaml.safe_load(open(<path>, encoding='utf-8'))"`). | Per version: `version` · `parseable: YES/NO` · `approved: YES/NO`. A blueprint that is not valid YAML is a pilot finding; record **especially** `parseable: NO` + `approved: YES`. | Another generated blueprint is syntactically invalid, particularly if the runtime allows its approval. Do **not** modify the Step-5 schema or add a runtime gate during the pilot. |

## 5. Simulate before decide — protocol requirement (from OBS-8D-08)

Pilot 2 **must** exercise, before the Decision is treated as complete:

```text
Options
→ /simulate
→ /decide
```

This is a protocol requirement for Pilot 2, not a new runtime rule. Record the three lines named in §4
(OBS-8D-08). Where `/simulate` cannot run (e.g. a single candidate option), record why rather than skipping
silently — that is itself an observation.

## 6. Pricing-marinha remains separate

`projects/pricing-marinha/**` is **not** Pilot 2, and Pilot 2 does **not** wait for its open architecture
questions. Its independent next actions, in its own engagement, remain:

```text
U-036 (SQL arrangement — IT / DB owner)
U-040 (workflow-state placement) · U-037 (hard row/column requirement) · U-038 (audit events / consumer)
U-039 (interactive what-if?) · U-034 (Mon/Tue input sparsity) · U-033 (Outputs BIOS consumer)
→ relevant proofs (SQL inspection V1, virtual-table spike V2, audit proof V2, calc parity V3)
→ /blueprint --refresh
→ v07+
→ approval if justified
→ rerender stale deliverables (solution-blueprint, implementation-spec, estimate, executive-report, design brief)
```

Anything learned there about the runtime enters Pilot 2 only as an observation in the log, never as a
mid-pilot repair.

## 7. Genericity discipline

During Pilot 2: **record observations only.** Do not classify a new finding as a generic defect while the
pilot runs, and do not edit the runtime. After Pilot 2, run a separate adjudication for every finding:

```text
observed failure
→ provenance
→ current-contract audit
→ genericity
→ repair decision
```

## 8. Recording

Observations go to a `pilot-2-observation-log.md` beside this file, one data point per entry, with the
same P-OBS register shape as Pilot 1 (`step-8-pilot-observation-log.md`). The §4 items carry their own
record shapes; use them verbatim so the post-pilot adjudication can compare like with like. The pilot report
follows the Pilot-1 report's section list plus §2, §4 and §5 above. Genericity of any defect is adjudicated
after the pilot, not during it (§7).

## Protocol check — Step 8D carry-forward

```text
STEP 8D OBSERVATIONS CARRIED FORWARD: YES
OBS-8D-05 REHYDRATION COST WATCH: YES
OBS-8D-07 NON-EXPIRED CONFIRMED REVALIDATION WATCH: YES
OBS-8D-08 SIMULATE-BEFORE-DECIDE EXERCISED: REQUIRED
OBS-8D-12 BLUEPRINT YAML VALIDITY WATCH: YES
PRICING-MARINHA BLOCKS PILOT 2: NO
PACK VERSION: 1.8.2
RUNTIME MODIFIED: NO
READY TO START PILOT 2: YES
```
