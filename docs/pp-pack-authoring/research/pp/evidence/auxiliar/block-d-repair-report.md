Repair Status: COMPLETE
Repair date: **2026-09-03**
Scope: **bounded repair of `block-d-review.md`'s findings only.** No Block D redesign. No pack authoring. `library/packs/pp/` untouched. Areas 1–12 read but **not modified**.
Authority: `research/pp/evidence/block-d-review.md` (independent review, verdict `PASS WITH CORRECTIONS`, `READY FOR BLOCK D GATE: NO`).

# Block D Bounded Repair Report

Files modified: `decision-criteria.md` · `anti-patterns.md` · `alternatives.md` · `decision-intelligence-matrix.md`.
External research performed: **none.** Every correction below is derived from the canonical Areas 1–12 corpus already mounted, or from Block D's own internal consistency. Where the corpus could not close a finding, `UNKNOWN`, `INF`, `CONFLICTED` or `COMPARATOR EVIDENCE ABSENT` is preserved and the residual is recorded as a research follow-up.

---

## 0. What changed at the level of the model

Three structural additions, each traceable to a HIGH finding:

1. **An exit taxonomy** (`decision-criteria.md` §2.5) — five mutually exclusive classes, applied to all 116 criteria, with every derived count regenerated from the classification rather than maintained by hand.
2. **An alternative-side signal layer** (`decision-criteria.md` §4A) — 28 criteria carrying evidenced signals about non-Power-Platform classes, `COMPARATOR EVIDENCE ABSENT` as the stated default on the other 88, and a four-part rule separating exclusion from candidate generation from comparative evaluation from preference.
3. **A closed outcome set** (`decision-criteria.md` §6.2) — 12 classes including an explicit rejection class and an economic class, with every emitting site in the other two files pointed at it.

One criterion and one anti-pattern were added (DC-D-116, AP-D-068). Nothing was deleted. No canonical identifier was renamed. No threshold was invented.

**Headline arithmetic, before and after.**

| Quantity | Before | After | How |
|---|---|---|---|
| Criteria | 115 | **116** | DC-D-116 added (H-03) |
| "Exit signals evidenced" | **36 / 46 / 48** (three files disagreed) | superseded by the taxonomy | H-01 |
| `Xp` platform exits | — | **15** | regenerated |
| `Xr` responsibility exits | — | **34** | regenerated |
| `Xe` economic exits | — | **5** | regenerated |
| `Xc` composed-only | — | **24** | regenerated |
| `—` no exit evidenced | 79 | **38** | regenerated |
| Direct exits (`Xp`+`Xr`+`Xe`) | — | **54** | regenerated |
| Composed disqualifiers | **8 / 10 / 8** (three files disagreed) | **12** in all three | M-02 |
| Anti-pattern entries | 67 | **68** | AP-D-068 (M-10) |
| Outcome classes | 11 (open, three vocabularies) | **12, closed** | H-02, M-07 |
| Adversarial scenarios | 15 | **16** | T-16 (H-03) |

**Why 36 became 54 rather than 46 or 48.** The review found 48 substantive exit statements in the criteria bodies. Applying the taxonomy consistently found **nine more** hidden in fields phrased *"none as a platform exit; it is an exit from patterns"* — DC-D-006, 021, 025, 030, 032, 046, 053, 056, 088 — which are responsibility exits written as if they were absences. Three of the 48 (DC-D-015, 063, 104) are composed-only and are correctly **not** direct exits. 45 + 9 = 54. The derivation is reproducible from the criterion bodies alone.

---

## 1. HIGH findings

### H-01 — Contradictory exit-signal taxonomy and counts

**Status: RESOLVED.**

**Files changed.** `decision-criteria.md` (§2.5 rewritten, §3 domain table, §3.1 register, all 116 criterion bodies, §9 item 5, §11); `decision-intelligence-matrix.md` (§1 legend, all 116 §2 rows, §9); `anti-patterns.md` (§5 header legend).

**Exact correction.**

1. **The taxonomy was established before any count changed**, as instructed. `decision-criteria.md` §2.5 now defines five mutually exclusive exit classes with a stated classification test and a stated precedence rule for fields carrying more than one consequence (*"the broadest scope the field reaches at a named state without further conditions"*; escalations such as DC-D-023's and DC-D-044's *"at the extreme, out of the platform"* are conditional and do not raise the class):
   - `Xp` platform exit · `Xr` responsibility/pattern exit · `Xe` economic exit · `Xc` composed-only exit · `—` no exit evidenced.
   - Two orthogonal flags are explicitly **not** exits: `B` (decision-blocking unknown) and `G` (an evidenced alternative-side signal exists). A third, `B*`, was added for the three criteria that block a narrower named scope (DC-D-113, DC-D-115, DC-D-116), so §5.2's set stays exactly the 28 it claims.
2. **All 116 criteria were re-flagged against the named classes**, mechanically, from their own `PP negative/exit` field text. Each criterion body now carries its class inline (`**PP negative/exit.** [`Xr`] …`), the §3.1 register carries it as a flag, and the matrix row carries it in the exit cell. The three representations are generated from one map and are verified equal (§5 below).
3. **Every derived count was regenerated**, not patched: the §3 domain table (now five class columns plus `B` and `G`), §2.5's distribution table, §9 item 5, §11, matrix §9, and the matrix §1 legend.
4. **DC-D-093 and DC-D-104 were reconciled** between body and matrix. DC-D-093's matrix cell said `— (combines with 092)` while its body states an economic exit; it now reads `[Xe] Premium plus external prerequisites across an unfunded population → economically infeasible`. DC-D-104's cell already carried the text and now carries `[Xc]` to match the body.
5. **The review's named pair is fixed.** DC-D-039 and DC-D-040 are now both `Xr`; previously DC-D-040 carried `X` and DC-D-039 did not, despite identical consequences.
6. **The load-bearing argument was re-tested, not quietly dropped.** §2.5 and §9 item 5 used the 36/79 split to argue the exit distribution is evidential rather than constructed. The recount preserves the argument and states the correction openly: Governance and ALM still produce **zero direct exits** between them, and 38 of 116 criteria (33%) still carry no exit at all.

**Evidence used.** The 116 `PP negative/exit` fields themselves; `decision-criteria.md` §3.1's original `X`/`B`/`V` flags; the matrix's own exit cells. No canonical Areas 1–12 evidence was re-interpreted — this finding is entirely about Block D's internal consistency, which is why it could be closed without external research.

**Remaining uncertainty.** The classification of two criteria is a judgement the review did not pre-empt and a re-reviewer may contest:
- **DC-D-018** (external-site freshness) is classed `Xr`, not `Xp`, because its own field says *"different read surface or custom web"* — the read surface leaves, not the solution. T-04's outcome was rewritten to match. It is the corpus's cleanest single-criterion exit and the demotion is **scope**, not strength; §2.5 states that explicitly.
- **DC-D-063** and **DC-D-104** are classed `Xc` because both fields describe the corpus's own composed disqualifiers rather than a single-criterion consequence.

**External research required?** No.

---

### H-02 — Unsupported comparative preference in terminal outcomes

**Status: RESOLVED.**

**Files changed.** `decision-criteria.md` (§6 fully rewritten as §6.1–§6.4); `decision-intelligence-matrix.md` (T-04, T-07, T-08, T-09, T-10, T-12, T-13, T-14 outcome lines; §5 Step 7a added; §7); `anti-patterns.md` (AP-D-059, AP-D-061, AP-D-003, AP-D-035 decision-impact lines).

**Exact correction.**

1. **The four statements are now separated by rule**, exactly as the brief requires. `decision-criteria.md` §6.1 and §4A.4:
   - **Exclusion** — Power Platform is out, and at what scope (`Xp` / `Xr` / `Xe` / `Xc`).
   - **Candidate generation** — which `ALT-NNN` classes come into scope (`alternatives.md` §5.1).
   - **Comparative evaluation** — §4A.2's signals, or `COMPARATOR EVIDENCE ABSENT`.
   - **Preference** — permitted **only** where comparative evaluation discriminates between the candidates.
   Step 3 is available on 28 criteria. **Step 4 is available on exactly one axis** — DC-D-108, deployment model.
2. **The three preference labels were retired and replaced**:

   | Retired | Replaced by |
   |---|---|
   | `CUSTOM DEVELOPMENT PREFERRED` | class 5 `POWER PLATFORM — POOR FIT` or class 6 `POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY`, each followed by class 8 `CANDIDATE SET — COMPARATIVE FIT UNEVALUATED` naming ALT-005 |
   | `EXISTING ENTERPRISE PLATFORM PREFERRED` | class 4 `POWER PLATFORM + ENTERPRISE-SYSTEM HYBRID` where authority stays with the incumbent, otherwise class 6 + class 8 with `INCUMBENT FIT UNEVALUATED` carried explicitly |
   | `BUY — PACKAGED PRODUCT OR SERVICE` | class 8 naming ALT-011 as a candidate; the buy-check obligation stays with DC-D-002 and `application-architecture.md` AA-36 rung 0 |
   | `ANOTHER LOW-CODE PLATFORM SHOULD BE EVALUATED` | class 9 `DEPLOYMENT MODEL EXCLUDES THIS PLATFORM — COMPARATOR EVIDENCED ON THIS AXIS` for the evidenced axis; class 8 naming ALT-008 everywhere else |

3. **`alternatives.md` §9's sentence is now a governing rule, not an observation** — §6.1 quotes it and derives two enforceable prohibitions from it: no outcome may contain *preferred / better / cheaper / faster* about an unevaluated class, and every non-Power-Platform terminal outcome carries `COMPARATOR EVIDENCE ABSENT` unless §4A.2 says otherwise.
4. **A new evaluation step (7a) makes the check ordered rather than optional** — the matrix §5 order now runs the comparator check immediately before the terminal sentence is written, because that boundary is precisely where the caveats were being discarded.
5. **The one place a comparator may be named is scoped and kept.** Class 9 exists because the deployment-model axis genuinely is evidenced on both sides (`platform-suitability.md` PS-47 versus `anti-patterns.md` §6 V-D-04), with the Early-Access caveat carried on the second comparator.

**Evidence used.** `alternatives.md` §5.3, §6 items 1–3, §9, ALT-005 Confidence, ALT-007 Confidence, ALT-008 Confidence; `licensing-cost.md` LC-U-04, §7.3 item 51, §6; `automation-architecture.md` §3.B row 19, §8.7; manifest NB-03, NB-06, NB-07; `platform-suitability.md` §1 (which supplies the `POOR` classification the outcome set previously lacked).

**Verification that nothing was softened.** All eight rewritten scenarios were re-run. **None changed its substantive conclusion.** T-07 and T-13 still say the platform is a **POOR FIT** — a class §6 previously did not contain at all — and T-13 still rests on four independent `Xp` exits plus an `Xe`. The repair *adds* an explicit rejection vocabulary and *removes* an unevidenced preference vocabulary; it does not weaken any rejection. The before/after table is in `decision-intelligence-matrix.md` §7.

**Remaining uncertainty.** None on the finding. The underlying gap — that no comparative evaluation exists — is unchanged and is now stated in the output rather than only in an internal caveat.

**External research required?** Not to close the finding. To close the **gap** the finding exposes, yes: `alternatives.md` §6 item 1 (comparative TCO) and item 2 (other low-code platforms) are research commissions. They are out of this repair's scope and were not attempted.

---

### H-03 — Missing conversational / agentic requirement coverage

**Status: RESOLVED** for coverage and blocking behaviour; **the underlying research gap is explicitly preserved and escalated.**

**Files changed.** `decision-criteria.md` (DC-D-116 added in §4.2; §3 domain table and register; §5.2 `B*` footnote; §8.5 rewritten; §9 items 6 and 8; §11); `anti-patterns.md` (AP-D-068 added in §5.5; §3.5 ledger; §4 register; §7; §9); `alternatives.md` (§5.1 row, §6 item 9, §9); `decision-intelligence-matrix.md` (§2.2 row, §8.3 rewritten, T-16 added, §7).

**Exact correction.**

1. **DC-D-116 — Conversational and agentic interaction requirement**, in the Users domain, on the **DC-D-113 pattern** the review identified as the correct precedent. States: `NONE` · `ASSISTED SEARCH AND SUMMARY` · `TASK-COMPLETING AGENT` · `AUTONOMOUS AGENT` · `UNKNOWN`. Confidence `LOW`. Flags `B* V`.
2. **No agent architecture model was fabricated.** The criterion encodes only evidence already present in Areas 1–12, and its `PP negative/exit` field states plainly that **no fit assessment of the agent surface exists anywhere in the corpus** (`platform-suitability.md` and `application-architecture.md`: zero mentions), so neither a positive nor a negative fit verdict is derivable.
3. **The criterion produces `DECISION BLOCKED — MORE EVIDENCE REQUIRED`** at `TASK-COMPLETING AGENT` and above, on three separable and separately closable grounds — commercial model, governance model, and (at `AUTONOMOUS AGENT`) the modality question itself. This is the behaviour the brief required.
4. **§8.5 was rewritten to record the error honestly.** The original justification for dropping `licensing-cost.md` DC-10 covered only consumption economics; the file now states that every sentence of that justification was true and none of it justified the omission, and that the treatment was internally inconsistent with DC-D-113. **Local criteria deliberately not carried: 0.**
5. **AP-D-068 — *Agent surface treated as covered by the app and flow access model*** was added (M-10), with three MS-documented mechanisms, filed in the same failure family as AP-D-030 and AP-D-033.
6. **T-16 was added** — a partner-and-internal conversational assistant over enterprise data — and terminates at `DECISION BLOCKED` with the three grounds named and the outcome each resolution would produce.

**Evidence used — all MS-sourced, all already in the canonical corpus.**

| Fact | Source |
|---|---|
| Agents are first-class governed artefacts in the tenant inventory (*"view and govern all apps, flows, and agents"*) | `governance.md` GOV-16 (G-09) |
| Managed-environment sharing rules cover agents with editor/viewer granularity | `governance.md` GOV-19 (G-12); `security.md` (S-24) |
| Default-environment policy stated as *"prevent agents, apps, and flows from calling any service"* | `governance.md` GOV-03 (G-03) |
| **Advanced connector policy: *"Virtual connectors: ACP doesn't support virtual connectors and won't support them in the future"*** | `security.md` SEC-24 (S-29) |
| Copilot Studio virtual connectors *"evolving into their own dedicated governance rules"* | `governance.md` GOV-11b (G-13, G-17) |
| **Graph-connector guest-access bypass: items *"might access the information … even if you block guest access"*** | `security.md` SEC-04 (S-25) |
| Design-time enforcement rolls out per workload (Power Automate → Copilot Studio → Power Apps); runtime-only until then | `security.md` SEC-24 (S-29) |
| Key Vault secrets consumable by *"cloud flows, Copilot Studio agents and custom connectors only"* | `security.md` SEC-07/SEC-06 (S-28) |
| *"Block unmanaged customizations"* breaks a list including **agent publishing** — *"Either forgo that control or forgo those features"* | `alm-devops.md` ALM-15, §4 row 15 |
| No maker monitoring page for Copilot Studio; agent coverage in admin Monitor is public preview | `operations-support.md` OP-06 (O-08) |
| **Agent conversation runtime is not covered by self-service disaster recovery** — requests *"fail until Microsoft restores the service in the primary region"* | `operations-support.md` OP-19 (O-19); `performance-scale.md` P-27 |
| Published request bucket: *"250,000"* per 24 h for *"Copilot Studio base and add-on"* | `automation-architecture.md` AT2-03 (V-01, V-02) |
| Copilot Credits at $0.01, *"dependent on the complexity of the task"*; AI Builder allocation removed 2026-11-01; monthly peak enforcement | `licensing-cost.md` LC-15 (L-03, L-04, L-05) |
| Agent authentication and channel controls: **preview, not researched** | `governance.md` GOV-U-06 |
| Agent authentication/channels changed within the research window — re-verify | `security.md` §9 |
| *"The corpus cannot answer 'should this be an agent instead of a flow?'"* — deferral with **no owner** | `automation-architecture.md` U-14, §12 |

**Remaining uncertainty — preserved explicitly, not closed.**
- **Economics: `UNKNOWN`.** The consumption unit is not modellable in advance by the vendor's own statement. The criterion's instruction is a pilot, not an estimate.
- **Capacity, latency, concurrency, accuracy: `UNKNOWN`.** The 250,000 figure is a licensing meter, not a performance envelope, and the criterion says so.
- **Governance maturity: `UNKNOWN` beyond the documented controls.** GOV-U-06 is carried verbatim, and AP-D-068's confidence note states the entry **cannot claim to be complete** for this surface.
- **Fit, in every class including Power Platform: `COMPARATOR EVIDENCE ABSENT`, absolutely rather than by default.** `alternatives.md` §6 item 9 records this as the one gap in the corpus that is not asymmetric — it is total.
- **`AUTONOMOUS AGENT` as a modality: unanswerable from this corpus**, with an unowned upstream deferral.

**External research required?** **Yes — and the review explicitly identifies it as necessary to make Block D decision-safe** (§19 item 6). An **agent / Copilot Studio research area** is required, covering fit boundaries, governance scope, security posture (including the graph-connector bypass), operational coverage and economics. It was **not** performed here: the repair's mandate forbids external research, and the criterion is written to block rather than guess until that commission lands. The commission is recorded in `alternatives.md` §6 item 9, `decision-criteria.md` §9 item 6 and `decision-intelligence-matrix.md` §8.3.

---

### H-04 — Asymmetric evaluation of alternative classes

**Status: PARTIALLY RESOLVED — and this is the correct outcome, not a shortfall.**

**Files changed.** `decision-criteria.md` (§4A added — §4A.1 default rule, §4A.2 signal table, §4A.3 prohibition, §4A.4 rendering rule; `G` flag on 28 register rows; §9 item 5a; §11); `decision-intelligence-matrix.md` (§1 Alternatives-column note, §5 Step 7a, §8.1, §9); `alternatives.md` (§5.1 header and evidence-column semantics, §9).

**Exact correction.** The instruction was explicit: **do not manufacture symmetry.** The repair therefore does two things and refuses a third.

1. **Where canonical evidence exists, the constraint is encoded.** 28 criteria carry an evidenced alternative-side signal in §4A.2, graded `UNAVAILABLE` · `CONSTRAINED` · `CAUTION` · `CANDIDATE` · `UNKNOWN`. The evidence is real and was already in the corpus, unused structurally. Load-bearing examples:
   - **Capability gates that make alternatives *unavailable*, not worse** — DC-D-070, DC-D-073, DC-D-104, DC-D-110, DC-D-006 (`architecture-patterns.md` §13 rows 2 and 7: *"unavailable, not merely expensive"*; *"Hybrid architecture required + no pro-dev/enterprise platform capability available → POOR FIT"*).
   - **Documented hard limits on ALT-006** — the code-first orchestrator's **identical** 500-action/8-nesting ceiling (*"'Move to Logic Apps' does not relieve it"*), the **same** 120-second synchronous window on its consumption tier, 256 KB standard-tier broker messages, 1,000 operations per second, connector triggers as **30-second long-polling — a latency floor, not push**, an event service guaranteeing **neither ordering nor exactly-once**, a streaming service with **no dead-lettering**, orchestrator code constraints with an **explicitly unreliable** non-determinism guard, and the private-egress/eventing **mutual exclusion**.
   - **Documented hard limits on ALT-005** — a **230-second maximum HTTP response on every plan**, a 5/10-minute legacy execution cap, cold starts unless always-ready instances are paid for, a 600-connection cap, connectivity that must be built (*"A dozen built-in binding types"* against 1,400+ connectors), and human-workflow constructs with **no equivalent**.
   - **The one documented positive** — DC-D-110 `FULL ENGINEERING CAPABILITY` makes ALT-005/ALT-006 genuinely cheaper than they would otherwise be. Recorded because refusing to record a signal that points *toward* an alternative would itself be a bias.
   - **The one evidenced comparative axis** — DC-D-108, deployment model.
2. **Where evidence does not exist, the absence is encoded explicitly.** §4A.1 makes `COMPARATOR EVIDENCE ABSENT` the **default on every criterion**, sourced to NB-07, LC-U-04, `automation-architecture.md` §3.B row 19 and §8.7, and `alternatives.md` §6 item 2. **88 of 116 criteria carry it.** The matrix's Alternatives column now carries the same warning, and `alternatives.md` §5.1's evidence column is re-labelled *"Evidence (that these classes come into scope)"*.
3. **What was refused.** No equivalent evaluation data was invented for custom development, Azure/cloud-native, other low-code platforms, packaged products or incumbent enterprise platforms. §4A.3 states that no row asserts any class is faster, cheaper, more scalable, more productive or more reliable than any other — including than Power Platform — and re-checks `alternatives.md` §2.2's five forbidden universals against §4A's finished text.

**Why PARTIALLY and not fully.** The finding is structural: the model evaluates one class per criterion, and the corpus does not contain the evidence to evaluate the others. That cannot be repaired by better extraction — only by the research commissions in `alternatives.md` §6. What the repair changes is that **the hand-off is now visibly incomplete instead of silently so**, and that the 28 criteria where evidence *does* exist now constrain alternatives instead of sitting in prose. §4A.3 states the residual plainly: on the four questions most often asked of a decision model — which is cheaper, faster, scales further, more reliable — Block D's answer is `COMPARATOR EVIDENCE ABSENT`, in every direction, for every class.

**Evidence used.** `architecture-patterns.md` §13 rows 2 and 7, §5.1; `automation-architecture.md` §8.2, §8.3, §8.4, §8.6, §8.7, §4.1 row 12, AT2-23…AT2-25, §3.B row 19, U-13; `integration-architecture.md` I-26, §12.1, U-03; `platform-suitability.md` PS-40, PS-47, PS-51; `licensing-cost.md` LC-U-04, LC-U-06, §6; `alm-devops.md` §14.2; `operations-support.md` §1.1; `anti-patterns.md` §6 V-D-01, V-D-04; manifest NB-03, NB-06, NB-07.

**Remaining uncertainty.** Comparative TCO, comparator low-code capability beyond deployment model, incumbent platform fit, empirical performance for any technology, broker and streaming capacity for two of three services, gateway-at-scale cost. All were already recorded in `alternatives.md` §6 and are unchanged.

**External research required?** **Yes, to close the gap** — `alternatives.md` §6 items 1, 2, 3, 5 and 8. **No, to close the finding**, which asked for the evidence that exists to be encoded and the evidence that does not to be marked. Both were done.

---

## 2. MEDIUM findings

Repaired where they affect decision correctness, downstream pack authoring, semantic consistency, volatility handling, combinatorial reasoning, lineage or cross-file consistency — as instructed.

### M-01 — Service-limit volatility not registered; §7's mitigation not implemented

**Status: RESOLVED.** *(Volatility handling.)*

**Files changed.** `decision-criteria.md` §7 (restructured into §7.1 commercial, §7.2 service-limit, §7.3 the rule a pack inherits); `decision-intelligence-matrix.md` §4.

**Exact correction.** The unimplemented mitigation — *"where a static criterion's decision impact quotes a figure, the figure carries its own source and date in the lineage"* — was **withdrawn**, because no `Lineage` field carries a date and a stated-but-unimplemented mitigation is worse than a named gap. It is replaced by a **service-limit register of 20 criteria**, derived mechanically from the criterion bodies by scanning `Decision impact` fields for quantities. Two apparent hits were excluded as false positives and the exclusion is recorded (DC-D-059's *"§4 row 6"* is a section reference; DC-D-037's *"60,000 records per hour and 1,000 records per minute"* is the corpus's own illustration of *shape*). §7.3 states the rule a pack must inherit: encode the **boundary shape**, not the number; re-read the figure at the decision date; and rely on §2.3's verified property that **no published figure is a state name**.

**Evidence used.** Manifest §5's `VOLATILE VALUE` definition; the 116 criterion bodies; `decision-criteria.md` §2.3.

**Remaining uncertainty.** Per-figure `ms.date` values are still not carried. Implementing that would require re-reading dates from Areas 1–12 for roughly twenty figures — an Areas 1–12 read that is in scope but was judged lower value than the register, because the register makes re-verification a *trigger* rather than a *decoration*. Recorded here so a re-reviewer can disagree.

**External research required?** No.

---

### M-02 — Composed-disqualifier register under-populated and out of step

**Status: RESOLVED.** *(Combinatorial reasoning; cross-file consistency.)*

**Files changed.** `anti-patterns.md` AP-D-059 trigger table and *"Why it fails"*; `decision-intelligence-matrix.md` §3; `decision-criteria.md` §2.4 and §11.

**Exact correction.** All three homes now carry **12** composed disqualifiers — 8 inherited from `architecture-patterns.md` §13, 4 derived by Block D and marked as derived. The two Block D additions that previously existed only in the matrix are now in AP-D-059 as well, and **two new rows were added from Governance and ALM**, which the review correctly identified as the structural cause of the gap:

| New row | Consequence | Canonical evidence |
|---|---|---|
| Citizen-built artefacts outside a solution, in the default environment + criticality now business-critical or above + the original maker gone | The workload **cannot be brought to the required class in place** — non-solution artefacts are excluded from backup, ineligible for capacity licences and undeployable; a non-solution automation's **owner cannot be changed at all**; the departed maker's profile has already reverted. **Migration, not remediation** | `governance.md` G-03; `operations-support.md` O-05, O-10; `alm-devops.md` ALM-14 |
| Continuous change + two or more concurrent makers + no pro-code capacity to reach the source-controlled rung | No isolation mechanism at any reachable rung — *"Every modification is applied directly to the environment, regardless of which solution is being edited"*, co-authoring removed, and the isolating rung needs pro-dev capability DC-D-110 gates. **Overwriting is the documented outcome**, with no supported first-party functional-test framework to catch it | `alm-devops.md` ALM-06, ALM-17, ALM-23, §4 rows 3 and 11; `application-architecture.md` AA-06 |

T-10 previously reached the right answer by conjoining four separately-detected anti-patterns; it now reaches it by an explicit rule, and the scenario says so.

**Evidence used.** As tabulated. Both rows are conjunctions of MS-stated facts; the composition is `INF`, consistent with AP-D-059's own origin tag.

**Remaining uncertainty.** None material. **External research required?** No.

---

### M-03 / M-04 — Duplicate and near-duplicate criteria

**Status: PARTIALLY RESOLVED — deliberately.** *(Downstream pack authoring; semantic consistency.)*

**Files changed.** `decision-criteria.md` §3.2 added.

**Exact correction.** The four clusters (DC-D-023/088 · DC-D-098/105/106 · DC-D-037/087 · DC-D-071/082) are **not merged**, because merging would delete published `DC-D-NNN` ids that three peer files already cite — the lineage failure manifest §4 exists to prevent, and the review itself rates these findings non-gate-blocking. Instead §3.2 states a **binding elicitation rule**: each cluster is elicited **once**, its members are the dimensions of that one elicitation, and each member's scope is stated so a question bank cannot ask the same fact twice with two vocabularies. DC-D-023 owns volume and delegability, DC-D-088 owns depth; DC-D-105 owns the requirement, DC-D-106 the obligation form, DC-D-098 the cost; DC-D-037 is scoped to per-stream arrival, DC-D-087 to whole-solution load and growth; DC-D-071 owns the drivers, DC-D-082 the lifecycle count.

**Remaining uncertainty.** A re-reviewer may hold that merging is still correct. The trade recorded in §3.2 is: merging removes the duplicate question **and** loses the per-vantage-point lineage attribution that makes the 236→116 consolidation auditable (§9 item 2). The rule removes the duplicate question and keeps the attribution.

**External research required?** No.

---

### M-05 — Unanchored ordinal states

**Status: RESOLVED.** *(Semantic consistency.)*

**Files changed.** `decision-criteria.md` DC-D-024, DC-D-025, DC-D-096.

**Exact correction.** All three state sets are anchored **relatively**, which requires no invented threshold — the review's own recommendation. DC-D-024 is anchored against the **purchased entitlement and the redesign trigger** (the corpus publishes no size ceiling for the governed store, so an absolute anchor would be invention). DC-D-025 is anchored against the **content-throughput window and the payload ceilings**, both of which the corpus publishes and neither of which becomes a state name. DC-D-096 is anchored against **the option's own total cost of ownership**, with `DOMINANT` given a decision consequence: the option is a cloud-native architecture with a low-code front end and should be evaluated as ALT-006 rather than ALT-009.

**Evidence used.** DC-D-024's and DC-D-025's own `Decision impact` fields; `licensing-cost.md` §6's ten-dimension method.

**Remaining uncertainty.** None. **External research required?** No.

---

### M-06 — DC-D-055 asserts a comparative claim the corpus forbids

**Status: RESOLVED.** *(Decision correctness; the only positive comparative claim in the signal layer.)*

**Files changed.** `decision-criteria.md` DC-D-055 (`Why it matters`, `Decision impact`, `PP positive`, related fields); §4A.2 row.

**Exact correction.** The unscoped *"no equivalent in the alternatives"* — presented as *"a comparative capability fact rather than a preference"* — is replaced by a three-way scoped statement, because the cited source (`automation-architecture.md` §4.1 row 12, tagged AT2-23/24/25) establishes that approvals **exist** and what they do, not what other classes lack:

- **Against the code-first alternatives the corpus examined (ALT-005, ALT-006): evidenced.** *"Moving this leg to Logic Apps or Functions means building all of it."*
- **Against an incumbent process or service-management engine (ALT-007): `UNKNOWN`** — *"no Microsoft or independent source evaluates incumbent BPM/ESB platforms; treat as reasoning, not evidence."*
- **Against other low-code platforms (ALT-008): `UNKNOWN`.**

The unqualified rule *"Any human decision within 30 days → keep this leg in the platform even if other legs move"* now carries an explicit **precondition on DC-D-111**, and states that where an incumbent already owns the process class the redirect wins on the corpus's own instruction (*"Adding Power Automate duplicates the operating model rather than reducing it"*, AT2-52). `PP positive` no longer calls it a differentiator against classes the corpus does not evaluate. AP-D-027 was added to its related anti-patterns.

**Evidence used.** `automation-architecture.md` §4.1 row 12, AT2-23…AT2-25, §3.B row 19, AT2-52; `alternatives.md` ALT-007, §2.2.

**Remaining uncertainty.** None. **External research required?** No.

---

### M-07 — Outcome-class vocabulary drift

**Status: RESOLVED.** *(Cross-file consistency; downstream pack authoring.)*

**Files changed.** `decision-criteria.md` §6.2 (the closed set); `anti-patterns.md` AP-D-059, AP-D-061, AP-D-003, AP-D-035; `decision-intelligence-matrix.md` T-04, T-07, T-08, T-09, T-10, T-12, T-13, T-14.

**Exact correction.** The outcome set is defined **once**, in `decision-criteria.md` §6.2, is **closed**, and now contains the two classes the other files were emitting without a definition: class 5 `POWER PLATFORM — POOR FIT` (the explicit rejection class §6 previously lacked entirely, taken from `platform-suitability.md` §1's own `POOR`) and class 7 `POWER PLATFORM — ECONOMICALLY UNATTRACTIVE OR INFEASIBLE`. Every emitting site now names the class and its number. A mechanical check confirms that the four retired labels survive **only** inside repair notes explaining their retirement.

**Remaining uncertainty.** None. **External research required?** No.

---

### M-08 — Six anti-patterns are constraints by Block D's own test

**Status: RESOLVED.** *(Downstream pack authoring — a pack renders a gate and a warning differently.)*

**Files changed.** `anti-patterns.md` §2 (three classifications defined), §5 header legend, the `Classification` field of seven entries, §8, §9.

**Exact correction.** `Classification` now takes one of three values and carries the **enforcement strength** a pack must apply: **`ANTI-PATTERN`** (61) · **`GATE`** (3: AP-D-026, AP-D-059, AP-D-013 — where they hold, an option is *unavailable*) · **`CONSTRAINT`** (4: AP-D-031, AP-D-044, AP-D-051, AP-D-067 — always wrong within their stated scope, the `Exceptions` field bounding scope rather than admitting exemption). §8's prose list of *"three entries are gates rather than risks"* is folded into the field, resolving the review's observation that §8 half-recognised this without following it through. AP-D-013 was added to the `GATE` set because §8 already named it one.

**Remaining uncertainty.** None. **External research required?** No.

---

### M-09 — AP-D-004 has no distinct failure mechanism

**Status: RESOLVED, by re-scoping rather than merging.** *(Downstream pack authoring.)*

**Files changed.** `anti-patterns.md` AP-D-004 (title, classification, altitude note); §8.

**Exact correction.** The entry is retained and marked **portfolio altitude, explicitly outside the engagement-altitude set**. The reasoning is recorded in the entry: its mechanism decomposes without residue into AP-D-015, AP-D-009, AP-D-039/AP-D-036 and AP-D-063; what remains is estate-level and no single-engagement Discovery can produce its trigger conditions. It is not merged away because the estate-level finding is real and MS-evidenced (shared tenant capacity, estate-wide restore blocking, no project-level request view) and is the only place the corpus records that a platform *standard* needs a workload-class exclusion list. §8 instructs that a pack must not surface it as an engagement finding.

**Remaining uncertainty.** None material. **External research required?** No.

---

### M-10 — Missing anti-pattern: agent surface bypassing the data access model

**Status: RESOLVED.** *(Decision correctness; security relevance.)*

**Files changed.** `anti-patterns.md` (AP-D-068 added in §5.5 Security; §3.5 ledger gains four agent candidate rows; §4 register; §7; §9); `decision-criteria.md` DC-D-116 related anti-patterns.

**Exact correction.** **AP-D-068 — *Agent surface treated as covered by the app and flow access model***, with three documented mechanisms and no synthesis beyond the framing: the advanced connector policy's **permanent** non-coverage of virtual connectors; the graph-connector guest-access bypass; and per-workload design-time enforcement leaving the policy runtime-only until each maker portal ships. Full `Trigger conditions` / `Why it fails` / `Consequences` / `Detection signals` / `Decision impact` / `Better alternatives` / `Exceptions` / `Evidence` / `Confidence` fields, per §5's contract. Two real `Exceptions` are stated so the entry is context-conditional rather than a constraint. Its confidence note records that GOV-U-06 makes the entry **incomplete by construction** for this surface.

The §3 ledger, which previously did not mention agents at all, now carries four candidates — one accepted, two merged, and **one rejected as evidence-absent** (autonomous agents as an automation modality, where an entry would be invention on `automation-architecture.md` U-14's own statement).

**Remaining uncertainty.** Agent governance beyond the documented controls is `UNKNOWN` (GOV-U-06). Stated in the entry.

**External research required?** Same commission as H-03.

---

### M-11 — User/UX domain has the highest exit density and the thinnest detection

**Status: RESOLVED — with a corrected finding.** *(Downstream pack authoring.)*

**Files changed.** `anti-patterns.md` §3.11b added; §3.12 ledger totals; §9.

**Exact correction.** `application-architecture.md` **AP-17 … AP-35** were re-tested **individually** against §2's four-element test, and the ledger records each of the nineteen by its own id and summary. The result: **0 new entries · 9 merged · 5 confirmed to an existing home (AP-D-034, AP-D-024, AP-D-030, AP-D-065, AP-D-007) · 5 rejected as Areas 1–12 altitude.**

**The honest finding is that the thin UX coverage was correct.** The domain's decision weight genuinely sits in the criteria — DC-D-012, DC-D-013, DC-D-015, DC-D-016, DC-D-018, DC-D-020 carry seven exits between them — and in AP-D-003, which is the detection home for five of the nineteen candidates. What the audit adds is the **mapping**: for every UX failure the canonical file documents, the ledger now names where in Block D it is detected. That is what a question bank needs, and its absence is what made the coverage impossible to check.

**Note on this repair's own process.** A first draft of §3.11b was written from plausible-sounding candidate names rather than from the file. It was discarded and rewritten against the actual AP-17…AP-35 entries. The discarded version is not in any file.

**Remaining uncertainty.** None. **External research required?** No.

---

## 3. LOW findings

Repaired where mechanical or trivial. None triggered structural change.

| Finding | Status | Correction | File(s) |
|---|---|---|---|
| **L-01** two id transpositions | **RESOLVED** | T-05's *"AP-D-053 ordering by trigger concurrency"* → **AP-D-015**, with **DC-D-053** named as the criterion. T-10's *"DC-D-047 solution-awareness"* → **DC-D-001** driving solution-awareness, whose failure is **AP-D-047**. Both corrections state the original error and why it was silent (`AP-D-NNN` and `DC-D-NNN` share a numeric range, so both ids resolve) | `decision-intelligence-matrix.md` |
| **L-02** `IA-U-14` / `IA-C-01` citation form | **RESOLVED** | Both citations now name **both** forms — `manifest NB-01 / IA-U-14 (= integration-architecture.md U-14)` — and a citation-form note in §1 records that a mechanical check against the mounted file will report these two as unresolved, that they are not errors, and that this is the manifest's own reservation **recorded, not repaired** | `anti-patterns.md` |
| **L-03** V1–V4 model cited to a non-existent section | **RESOLVED** | AP-D-052's evidence re-anchored from `integration-architecture.md` §15.8 (that file has fourteen sections) to **`alm-devops.md`**, with the four levels named. The dangling citation is inherited from two canonical files and is recorded as an Areas 1–12 defect, **not repaired** | `anti-patterns.md` |
| **L-04** register ordering | **RESOLVED** | An ordering note in the §5 header records that AP-D-055 and AP-D-067 sit outside strict numeric order within their subsections because they are filed by the category their `Consequences` land in, and that **§4's register is authoritative and complete** — so a sequential read of §5 is not a completeness check. Entries were not moved | `anti-patterns.md` |
| **L-05** pack-local vocabulary undeclared | **RESOLVED as a recorded prerequisite** | §9 item 7a names the six circumlocutions, cites `data-architecture.md` DQ-03/U-14's requirement that a pack *"declare its own vocabulary as pack-local"*, and states that Block D correctly does **not** author the glossary (the Options phase is where the mapping is permitted to exist) but that **this material is not usable until it is written** | `decision-criteria.md` |
| **L-06** §3.12 ledger arithmetic | **RESOLVED** | The reconciliation is now an explicit **footnote** stating that the table does not balance on its own, that 134 verdict rows against 124 candidates differ by exactly 10, and that the cause is ten accepted topics splitting into two entries each | `anti-patterns.md` |
| **L-07** DC-D-093 / DC-D-104 body-versus-matrix | **RESOLVED** | Subsumed in H-01; both rows reconciled per-row | `decision-intelligence-matrix.md` |

---

## 4. What was deliberately **not** done

| Item | Why |
|---|---|
| Merging DC-D-023/088, DC-D-098/105/106, DC-D-037/087, DC-D-071/082 | Would delete published ids cited by three peer files. Replaced by a binding elicitation rule (M-03/M-04) |
| Carrying `ms.date` on every quoted figure | Not implemented; the unimplemented claim was **withdrawn** and replaced by a register with re-verification triggers (M-01). Recorded as a residual |
| Repairing `licensing-cost.md`'s duplicate `DC-14` | Areas 1–12 repair, out of scope. Block D's record of it — including that the manifest's `DUPLICATE CANONICAL IDS: 0` is wrong — is left intact |
| Repairing the `integration-architecture.md` §15.8 dangling citation in Areas 1–12 | Same. Block D's own citation was re-anchored; the upstream defect is recorded |
| Any comparative TCO, benchmark, incumbent or comparator-low-code claim | The corpus holds none. `COMPARATOR EVIDENCE ABSENT` encoded instead (H-04) |
| Any agent fit verdict, capacity envelope, cost model or governance completeness claim | The corpus holds none. `UNKNOWN` preserved and the criterion blocks (H-03) |
| An agent architecture model | Explicitly forbidden by the repair brief, and unsupported by evidence |
| Re-review, gate, canonicalisation, pack authoring | Out of scope by instruction |

---

## 5. Validation performed

### 5.1 Mechanical

A section-scoped checker was run over all four files. **44 checks, 44 PASS, 0 FAIL.**

| Check | Result |
|---|---|
| Duplicate `DC-D-*` / `AP-D-*` / `ALT-*` definitions | 0 · 0 · 0 (116 · 68 · 11 defined) |
| Dangling `DC-D-*` references across all four files | **0** (116 distinct referenced) |
| Dangling `AP-D-*` references | **0** (68 distinct) |
| Dangling `ALT-*` references | **0** (11 distinct) |
| §3.1 register: exactly one row per criterion | 116 ✓ |
| Register ids == body ids (as sets) | ✓ |
| Every criterion body carries an exit-class tag | 116 ✓ |
| **Register flag == body tag == classification map, all 116** | ✓ |
| Matrix carries a tagged row for every criterion | 116 ✓ |
| **Matrix exit class == criterion body class, all 116** | ✓ |
| Exit-class distribution == published counts | `Xp` 15 · `Xr` 34 · `Xe` 5 · `Xc` 24 · `—` 38 ✓ |
| Direct exits == 54 · total == 116 | ✓ |
| §3 domain-table totals row regenerated | ✓ |
| Blocking counts: `B` == 28 · `B*` == 3 (113, 115, 116) | ✓ |
| §5.2 table lists exactly the 28 `B`-flagged criteria | ✓ |
| Alternative-side signal `G` == 28 | ✓ |
| Every `G` criterion has a §4A.2 row, **and §4A.2 contains no criterion that is not `G`** | ✓ (both directions) |
| §4A.1 states the 88 / 28 split | ✓ |
| Composed disqualifiers == 12 in matrix §3, **and** == 12 in AP-D-059 | ✓ |
| All three homes state `8 + 4 = 12` | ✓ |
| Outcome set: rejection, economic, responsibility-scope and candidate-set classes defined | ✓ |
| **Four retired labels survive only inside repair notes** | ✓ |
| `COMPARATOR EVIDENCE ABSENT` present in all three decision files | ✓ |
| Anti-pattern classifications: 61 `ANTI-PATTERN` / 3 `GATE` / 4 `CONSTRAINT`, 68 entries | ✓ |
| Anti-pattern register rows == 68 · AP-D-068 defined, registered and referenced | ✓ |
| Every criterion names ≥1 anti-pattern · ≥1 alternative · a file-qualified `Lineage` | 116 / 116 / 116 ✓ |
| Every anti-pattern reachable from a criterion · every alternative reachable | ✓ · ✓ |
| Adversarial scenarios present | 16 ✓ |

### 5.2 Manual verification of the HIGH repairs against canonical evidence

| Repair | Verified against | Result |
|---|---|---|
| H-01 taxonomy applied consistently | All 116 `PP negative/exit` fields re-read; the nine reclassified *"none as a platform exit"* fields (DC-D-006, 021, 025, 030, 032, 046, 053, 056, 088) checked individually | Each names what leaves — a pattern, store, mechanism or surface. `Xr` correct |
| H-01 DC-D-039 / DC-D-040 parity | Both bodies | Structurally identical consequences, now identically classed |
| H-02 retired labels vs source | `alternatives.md` §6 items 1–3, ALT-005/007/008 Confidence, `licensing-cost.md` LC-U-04 | Confirms the corpus holds no comparative TCO, no benchmark, no incumbent evaluation. The labels were unsupported |
| H-02 class 9 is genuinely evidenced | `platform-suitability.md` PS-47; `anti-patterns.md` §6 V-D-01, V-D-04 | One comparator documents GA air-gapped/on-premises deployment; the second is Early Access, and the caveat is carried |
| H-03 every fact in DC-D-116 | Each source read in place (table in §1 above) | All fifteen facts quoted from MS-sourced canonical text. No fit verdict synthesised |
| H-03 the absence claim | `platform-suitability.md`, `application-architecture.md` grep | **0 mentions** in both — the claim that no fit assessment exists is verified, not asserted |
| H-03 the unowned deferral | `automation-architecture.md` U-14, §12 | Quoted verbatim, including *"This deferral has no owner"* |
| H-04 the `UNAVAILABLE` gates | `architecture-patterns.md` §13 rows 2 and 7 | *"unavailable, not merely expensive"* and the pro-dev row confirmed verbatim |
| H-04 the ALT-005 / ALT-006 limits | `automation-architecture.md` §8.2–§8.4, §8.6 | Every figure and quotation traced to the negative-evidence register the corpus assembled deliberately |
| M-02 the two new composed rows | `alm-devops.md` ALM-06/17/23, §4 rows 3 and 11; `application-architecture.md` AA-06; `operations-support.md` O-05, O-10 | Both conjunctions rest on MS-stated facts; the composition is `INF`, matching AP-D-059's origin |
| M-11 the UX ledger | `application-architecture.md` §11 AP-17…AP-35 | All nineteen entries read; the ledger quotes their own ids and summaries |

### 5.3 Adversarial regression

All sixteen scenarios were re-run against the repaired files, including every scenario the repair brief names. The before/after table is in `decision-intelligence-matrix.md` §7.

| Scenario | Named in the brief | Substantive conclusion changed? |
|---|---|---|
| T-05 high-volume integration | ✓ | **No.** Same `Xr` exit on DC-D-040, same hybrid, same DC-D-039 block. Id transposition corrected |
| T-07 strict low-latency | ✓ | **No.** Still rejected, on the strongest available grounds. Label now states exclusion + unevaluated candidates |
| T-10 citizen app → enterprise-owned | ✓ | **No** — and it is now reached by an explicit composed disqualifier rather than by narrative reasoning |
| T-12 existing enterprise platform should own it | ✓ | **No.** Still excluded for the integration responsibility; `INCUMBENT FIT UNEVALUATED` now carried |
| T-13 custom clearly preferable | ✓ | **No.** Still the corpus's most over-determined rejection — four `Xp` exits plus an `Xe` |
| T-14 economically unattractive | ✓ | **No.** Same mechanism; the *"→ EXTEND or BUY"* continuation removed as unevidenced |
| T-15 insufficient evidence | ✓ | **No.** Unchanged |
| T-16 conversational / agentic | ✓ | **New capability** — `DECISION BLOCKED` on three separable grounds |

**Bias check.** The renames move in one direction only: away from asserting a non-Power-Platform class is preferred. Tested for the obvious risk that this softens rejection: it does not. T-07 and T-13 now say **`POWER PLATFORM — POOR FIT`**, an explicit rejection class §6 previously **did not contain at all**. Power Platform is rejected, displaced or blocked in **12 of 16** scenarios (6 rejected or displaced, 6 blocked) — the same 11 as before, plus T-16.

**Artificial-comparator-certainty check.** No scenario gained a claim about an alternative's fitness. T-04's note that *"the replacement's adequacy is unevidenced"* and T-09's note that NB-07 applies to the candidates too were **added**, not removed.

---

## 6. Findings the repair leaves open

| Finding | Why open | Gate-blocking? |
|---|---|---|
| **H-04 (residual)** | The corpus contains no comparative evaluation of any alternative class. Encoded as `COMPARATOR EVIDENCE ABSENT` on 88 criteria; closing it requires the research commissions in `alternatives.md` §6 items 1, 2, 3, 5, 8 | **No** — the finding asked for the evidence that exists to be encoded and the absence to be marked. Both done. The gap is an upstream commission |
| **H-03 (residual)** | No fit assessment of the agent surface exists in any canonical file; `automation-architecture.md` U-14's deferral is unowned. Encoded as a criterion that **blocks** | **No** — for the same reason. The review names the commission at §19 item 6 |
| **M-01 (residual)** | Per-figure `ms.date` values are still not carried; the register with re-verification triggers replaces the withdrawn claim | No |
| **M-03 / M-04 (residual)** | Clusters disambiguated by rule rather than merged, to preserve cited ids | No — the review rates them non-gate-blocking |
| **Areas 1–12: duplicate `DC-14`** | Out of Block D's scope. The manifest's `DUPLICATE CANONICAL IDS: 0` is wrong and Block D records it | No, for Block D. **Yes for the manifest**, per the review §19 item 1 |
| **Areas 1–12: `integration-architecture.md` §15.8** | Out of scope. Block D's own citation re-anchored | No, for Block D |
| **NB-02 remains `CONFLICTED`** | Correctly preserved and re-verified; DC-D-039 blocks on it | No — the model handles it |

**Unresolved gate-blocking findings: 0.** Every finding the review marked gate-blocking (§18 rows 1–7: H-01, H-02, H-03, H-04, M-01, M-02, M-07) is repaired. Rows 8–17 (M-03…M-11, L-01…L-06), which the review asked to be applied before pack authoring rather than before the gate, are also repaired, with M-03/M-04 partially and by a stated design choice.

---

## 7. Files modified

| File | Lines before | Lines after | Nature of change |
|---|---|---|---|
| `decision-criteria.md` | 3,438 | **3,750** | §2.5 taxonomy · §3 domain table · §3.1 register (116 rows re-flagged) · §3.2 elicitation rule · DC-D-116 added · 116 exit-class tags · §4A added · §5.2 `B*` · §6 rewritten · §7 restructured · §8.5 rewritten · §9 · §11 |
| `anti-patterns.md` | 2,391 | **2,505** | §1.4 citation-form note · §2 three classifications · §3.5 agent candidates · §3.11b UX ledger · §3.12 totals · §4 register · §5 header · AP-D-004 re-scoped · 7 classifications changed · AP-D-052 re-anchored · AP-D-059 12 rows · AP-D-061 · AP-D-068 added · §7 · §8 · §9 |
| `alternatives.md` | 796 | **804** | §5.1 candidate-set semantics · §6 items 9 and 10 · §9 · status line |
| `decision-intelligence-matrix.md` | 598 | **687** | §1 legend and exit classes · 116 tagged rows + DC-D-116 · §3 twelve composed rows · §4 service-limit group · §5 Step 7a · T-04/05/07/08/09/10/12/13/14 · T-16 added · §7 before/after and bias check · §8.1 · §8.3 rewritten · §9 |
| `block-d-repair-report.md` | — | **485** | This report |

`library/packs/pp/` — **untouched.** Areas 1–12 canonical files — **read only, not modified.**

---

## 8. Verdict

`BLOCK D HIGH FINDINGS RESOLVED: YES`
`BLOCK D DECISION MODEL INTERNALLY CONSISTENT: YES`
`UNRESOLVED GATE-BLOCKING FINDINGS: 0`
`READY FOR BLOCK D RE-REVIEW: YES`

---

**Not performed, by instruction:** the re-review · the Block D gate · canonicalisation · PP pack authoring · any external research.
