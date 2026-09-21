# Blocking Set — decision-changing uncertainty

<!--
provenance: RUNTIME (decision-model register) · consumed at stage S3 of decision-tree.md
authored: 2026-09-04 (Step 3B1) · design authority: Step 3A — Options Decision Model
Stage-local: loaded at S3 only, and re-consulted when S3 is re-run after S8. Never preloaded.
This is NOT a questionnaire and NOT an elicitation instrument. It is consulted when an Options
decision is already in front of the reasoner.
-->

## 0. What this register is, and what it is not

**It is a pattern, not a plan.** The pack authors the *shape* of the question; the engagement supplies
the commitment.

| Pack-authored — belongs here | Engagement-resolved — **never** here |
|---|---|
| The evidence needed, stated as a question | The **actual role or source** that owes it (`role:` / `fonte:`) |
| The closure action **pattern** | The **actual due date** |
| The likely responsible **role type** | The **actual elapsed duration** |
| The expected **form** of the evidence | The **commitment** anyone makes to close it |
| The `custo` default, and `swing: decisivo` by construction | The engagement's own re-priced `custo`/`swing` where `/simulate` corrects it |
| The outcome each resolution would produce | Which resolution actually occurred |

The right-hand column lands on the engagement's own `Unknown` row (`quem responde`, `criticidade`,
`custo`, `swing`) and, on resolution, in `answers.md`. A pack that shipped an owner and a duration would be
asserting facts about an organisation it has never seen. What lands there is a **role** or a **source to
consult**, written with its prefix (`library/kernel/states.md` → *Schema of Shared Understanding rows*) —
never a person: the answer is owed by whoever holds the role, and no name is a precondition for the next
step.

**How S3 uses it.** For each entry engaged by the engagement: is the fact known, at what evidence grade?
If it is `Unknown`, `Conflicted`, or a provisional finding `decision-tree.md` §4 refuses to settle →
open an `Unknown` row carrying the question, the closure pattern, the expected form, the role type and
the `custo` default below; set `swing: decisivo`; and state **what each resolution would produce**. That
last part is what makes the evidence task worth funding.

**Only the seven technical axes block** (`decision-tree.md` §6.1, P-22). An entry of this register
blocks a decision only where it sits on one of those axes. The entries marked **requirement (P-22)**
below are real findings and stay in the register, but they resolve as **requirements and risks of the
chosen path** — recorded, carried into `/decide` and the implementation spec, priced at S8 where they
cost money — and they never produce *decision blocked* and never make an option unavailable. An
organisational gap recurs identically on every candidate, so it separates nothing.

**Roles, never people** (P-21). No entry closes on a person's name, a signature, an approval or a
document proving a third party's position. Where authority matters the closure is a **role**, the
operation it must perform, and the plane that enforces it.

**An organisational rule routes to class 15, never to an exclusion.** Where an entry resolves to
*the organisation's rule forbids this*, the option is not unavailable: it carries the outcome
**class 15** — *viable if the rule is changed* — with the rule's id, the condition, the impact, the
cost, the risk, the role that can change it and its status (`outcome-classes.md` §1.0). A rule is a
decision, and the owner is entitled to take it at `/decide`; an option deleted here never reaches
them. This holds for an **imposed platform** too: the set is generated inside that boundary
(`decision-tree.md` §6.2) and the alternative appears only as class 15.

**Every remaining entry is `swing: decisivo` by construction.** That is why they are in this register. It is
also why the register is short: the remaining material concerns can be carried on a declared `Assumed`
row with its basis, `verificado_em` and `validade` stamped. *A model that treats every unknown as
blocking never produces a recommendation; one that treats none as blocking produces confident nonsense.*

**`custo` vocabulary** (`library/kernel/states.md`): `email` · `documento` · `reuniao` · `spike`.

---

## 1. The 28 blocking entries

| # | What must be known | Why proceeding without it is unsafe | Closure pattern → expected form of evidence | Likely role type | `custo` | What each resolution produces |
|---:|---|---|---|---|---|---|
| B-01 | **Business criticality class** | Sets artefact structure, isolation class, ownership model, proof requirement and licence footprint at once. Wrong class = wrong architecture **and** wrong cost | Run a business-impact assessment with the sponsor → a stated class with its basis | sponsor | `reuniao` | Low class → *fit* or *fit with constraints* remain open. High class → escalates depth on every concern, engages the operability gates and the proof requirement; where it sits two or more classes above demonstrated maturity, see composed row CD-09 |
| B-02 | **Reconciliation role and mechanism per replicated entity** — **requirement (P-22)** | Replication, hybrid and bidirectional patterns need a role that can correct a divergence and a mechanism that surfaces it. Detection alone does not correct anything | State, per replicated entity, which **role** corrects a divergence and which mechanism detects it → the role, the operation and the detection mechanism | data owner · platform-owning team | `reuniao` | Stated → the pattern is designable as specified. Absent → a **requirement** on the chosen path plus a `Risky` row naming silent divergence; never an exclusion and never *decision blocked*. A person's name and their acceptance are not inputs here |
| B-03 | **User population identity class** | Selects the surface, the isolation topology, the licensing model and the security review depth simultaneously | Population and identity inventory → a per-population identity source | business owner · security owner | `documento` | Internal directory → surfaces and entitlement stay in the ordinary envelope. External / anonymous / non-directory → engages entitlement fit (B-24), external identity (B-15) and possibly *excluded, whole scope* |
| B-04 | **Source of record per entity and field** | Every data and integration decision follows from it, and no vendor definition exists to borrow | Entity/field authority matrix → the matrix, one authoritative store per entity and field | business owner · data owner | `reuniao` | Single owner → ordinary data architecture. Contested authority → a `Conflicted` row **before** design; multiple transactional owners feed composed row CD-01 |
| B-05 | **Data residency and sovereignty** | Decided **at environment creation and irreversible** | Read the regulation or contract clause verbatim → the clause | compliance owner | `documento` | Satisfiable → proceed. Not satisfiable → *excluded, whole scope*, decided **before** any architecture work |
| B-06 | **Integration ownership** | Step 1 of the topology test; skipping it produces the point-to-point estate | Consult the platform-owning team; obtain the published contract → a contract plus its lead time | platform-owning team | `reuniao` | Owned with a contract → the incumbent keeps authority (hybrid, enterprise-system form). Unowned → the integration responsibility is in scope and priced |
| B-07 | **Frequency distribution and peak shape** | No mechanism can be sized without a peak figure. Sizing on the average sizes for the case that never fails | Measure or model peak per interval → a measurement with its basis and date | delivery lead · platform-owning team | `spike` | Inside the documented envelope → proceed with the proof requirement stated. Outside → *excluded for the named responsibility*, or a hybrid split at the step |
| B-08 | **Per-mechanism throughput ceiling** | The published figures **conflict by an order of magnitude** on the main extensibility mechanism, and the conflict is live (see `volatility-register.md` VC-01) | Re-read **both** current sources **and** measure representative workload → two dated readings plus a measurement | platform-owning team | `spike` | Either reading confirmed **and** the workload measured inside it → proceed. Measured outside → *excluded for the named responsibility*. Unmeasured → **decision blocked**; do not encode either figure |
| B-09 | **Sustained end-to-end throughput at horizon** | Produces the sharpest exclusion verdict available; absent it, **both staying and leaving are unevidenced** | Volume projection with growth, against the weakest participant's capability → a projection with a stated basis | delivery lead · business owner | `spike` | Inside envelope → proceed. Outside with no partitioning → cloud-native or hybrid candidates come into scope |
| B-10 | **Network boundary and private connectivity** | The preconditions are **irreversible** (immutable subnet and DNS, region pinning) and licence-bearing | Network policy clause + endpoint inventory → the clause and the inventory | network policy owner | `documento` | Public egress permitted → ordinary. Private-network execution required → cloud-native / hybrid / incumbent candidates; feeds the economics of the mandated control |
| B-11 | **Stable business key availability (idempotency)** | Retry is on by default and duplicates side effects. A missing key is a **scope item**, not a detail | Confirm a stable business key exists, or fund creating one → the key's definition and its source | business owner · delivery lead | `documento` | Exists → retry semantics are safe. Absent → a funded scope item, and a precondition on every mechanism that retries |
| B-12 | **Failure semantics after partial completion** | There is **no rollback**. Absent an answer, the failure behaviour is whatever the implementation happens to do | Define the required post-failure state per operation → a per-operation statement | business owner | `reuniao` | Retry-and-continue or compensate → designable. *Never partially complete* across systems → composed row CD-01 |
| B-13 | **Data sensitivity classification** | Determines the mandated control set, and therefore the cost | Classify against the organisation's own scheme → a classification record | data owner · security owner | `documento` | Low tier → ordinary controls. High tier → mandated controls, whose **population** must then be funded (B-23, composed row CD-03) |
| B-14 | **Regulatory and contractual compliance regime** | Can mandate something documented as **unavailable** | Read the clauses; enumerate the mandated controls → the clauses plus a control list | compliance owner | `documento` | No mandate engaged → proceed. A mandated control that is unavailable → *excluded, whole scope*. Available but unfunded → *economically infeasible* |
| B-15 | **External identity requirement** | Selects surface, isolation topology and licence model; cross-tenant entitlement recognition is conditional | External population and identity inventory → a per-population identity source | business owner · security owner | `documento` | None → ordinary. Required → entitlement fit (B-24) and surface choice both re-open |
| B-16 | **Estate governance mechanisms** — **requirement (P-22)** | A boundary pattern needs an environment strategy, a release path across the boundary and a policy owner for the connector set. Absent them the pattern still runs — ungoverned | Record which environment strategy, release path and policy mechanism exist today → the mechanisms, or a recorded absence | platform-owning team | `reuniao` | Present → boundary patterns are designable as specified. Absent → a **requirement** on the chosen path plus a `Risky` row; it recurs identically on every class needing an external component, so it excludes nothing and blocks nothing |
| B-17 | **Support model — roles, surfaces and mechanisms** — **requirement (P-22)** | The vendor's support does not fill this gap: someone must see the failure and act. What the architecture consumes is the **mechanism** — alerting surface, diagnostic access, recovery path — not a staffing decision | State the roles of the support model and the surface and mechanism each uses → the roles and mechanisms | operations owner | `reuniao` | Stated → the observability and recovery requirements are specified. Absent → a **requirement** on the chosen path plus a `Risky` row; never an exclusion, never *decision blocked* |
| B-18 | **Reversibility requirement** | The mechanism must be **enabled before it is needed** — there is no rollback after the fact | Choose, enable **and rehearse** a mechanism → a rehearsal result | delivery lead · operations owner | `spike` | Fix-forward accepted → ordinary. Redeploy or full restore required → the mechanism is a funded precondition; unrehearsed at high criticality → composed row CD-04 |
| B-19 | **User concurrency** | **No figure is published anywhere.** Quoting one is invention | Load test against a production-like environment → a dated test result | delivery lead | `spike` | Measured inside the design's assumptions → proceed at proof level V3/V4. Unmeasured at a criticality that requires it → **decision blocked** |
| B-20 | **Request rate per acting identity** | Amplification is a property of the solution's own customisation and is never published | **Measure** on a prototype with the named instrumentation → a dated measurement | delivery lead | `spike` | Inside the documented tolerance → proceed. Outside → redesign, or the responsibility moves |
| B-21 | **Peak load shape and growth horizon** | The *scale anxiety without a number* case — neither staying nor leaving is evidenced without it | Build a growth model with a stated basis → the model and its basis | business owner · sponsor | `reuniao` | Flat or modest → ordinary economics. Steep → the cost dimensions that move are priced at S8, and the envelope is re-tested at horizon, not at launch |
| B-22 | **End-to-end availability of the composed flow** | Availability of a platform ≠ availability of a business flow. The second is computed from every dependency on the path | Per-flow dependency map with each dependency's own position → the map | delivery lead | `spike` | Computed figure meets the expectation → proceed with the proof requirement. Below it → a contractual commitment cannot rest here; classes that can underwrite it come into scope |
| B-23 | **Budget envelope and funding model** — **requirement (P-22)** | Cost is priced identically for every candidate at S8; funding is an organisational fact that does not separate them | State the envelope and the funding model → a stated envelope | sponsor · licensing owner | `reuniao` | Stated → the cost lines are comparable against it. Absent → the S8 economics are reported **without** an envelope verdict, plus a `Risky` row; a mandated control that is unfunded is a **requirement and a risk** carried into `/decide`, not *economically infeasible* and not *decision blocked* |
| B-24 | **Entitlement fit of the required capability set** | One capability decision can move the **whole population** from seeded to paid, and the general documentation is **not authoritative** on licensing | Read the licensing guide **and** the customer's own agreement, routed to the role that holds them → a dated reading of both | `role:` licensing owner | `documento` | Inside what is already held → the lighter answer may stand, with its graduation trigger. Outside → priced at S8; unfunded and mandated → *economically infeasible* |
| B-25 | **Recovery point and recovery time objectives** | *A backup exists* ≠ *recovery is possible*. No cross-region recovery-time commitment is published; a contractual objective must rest on the customer's own drills | Objectives per flow **plus a timed drill** → the objectives and a dated drill result | operations owner | `spike` | Drilled and met → the commitment is evidenced. Not drilled at a criticality that requires it → composed row CD-04, **decision blocked** |
| B-26 | **Operational maturity class** — **requirement (P-22)** | A gap between what is committed and how the organisation operates changes what the architecture must automate, alert on and recover by itself | Honest assessment of current operating practice → a stated class with examples | sponsor · operations owner | `reuniao` | Gap ≤ 1 class → ordinary operability requirements. Gap ≥ 2 classes → a **requirement** on the chosen path (the architecture carries what the operation cannot) plus a `Risky` row, and the commitments the operation cannot evidence are named. **Never a platform exclusion and never *decision blocked*** — the gap recurs identically on every platform, so it separates nothing |
| B-27 | **Deployment-model constraint** | Can eliminate the platform **entirely**, and must precede all architecture work | Obtain the clause stating where the runtime must execute → the clause | compliance owner · sponsor | `documento` | Vendor-operated acceptable → no constraint. Customer-hosted / private-cloud / air-gapped → *deployment model excludes this platform*, and this is the **one axis** where a comparator is evidenced |
| B-28 | **Team skills and pro-code capacity — in-house and available** — **requirement (P-22)** | A design needing absent capability is a documented risk, and it changes the build effort and the delivery shape | Capability inventory distinguishing **available** from **planned** → the inventory | delivery lead · sponsor | `reuniao` | Full engineering capability → custom and hybrid are ordinary. Low-code only, with a hybrid required → a **requirement** on the chosen path (buy the capability, or change the design) plus a `Risky` row and the effort consequence; never *excluded, whole scope* and never *decision blocked* |

---

## 2. The 3 scope-blockers

These do **not** block the decision as a whole. Each blocks a **named part** of it, and the blocked part
must be stated with the scope attached.

| # | What it blocks | Why | Closure pattern → expected form | Likely role type | `custo` | What each resolution produces |
|---:|---|---|---|---|---|---|
| BS-01 | The **commercial model for resale / multi-tenancy** | No evidence exists on multi-tenant resale licensing at all | Read the licensing terms and the customer's agreement → a dated reading of both | licensing owner | `documento` | Confirmed permissible → the commercial model proceeds. Otherwise → the **commercial model** is blocked; the technical decision may still proceed on its own scope |
| BS-02 | Any **commitment resting on a preview or unshipped capability** | Preview and general-availability states change; facts in this pack's own evidence already changed once | Check the general-availability state **on the day of the decision** → a dated state reading | platform-owning team | `documento` | Generally available → the commitment may rest on it. Preview or unshipped → **descope it, or block that commitment.** Putting a preview on the critical path is a named anti-pattern |
| BS-03 | The **commercial and governance model for an agent surface**; and, at the autonomous end, the **modality question itself** | Consumption is dependent on task complexity and therefore unmodellable in advance; agent-specific governance is evolving and its authentication and channel controls are preview | Establish consumption **empirically in a bounded pilot**; obtain the current governance position → a dated pilot measurement plus a written position | platform-owning team · licensing owner | `spike` | Measured and governed → the commercial model proceeds. Otherwise → the agent scope is blocked. **Fit itself is `UNKNOWN` in every option class** (`alternatives-register.md` row 29): the honest output is **decision blocked**, not a candidate set |

---

## 3. What is *not* in this register

The material concerns that are **not** listed above can be carried on a declared `Assumed` row with its
basis, `verificado_em` and `validade` stamped — provided the assumption is **stated, owned and dated**.
An **expired** row reads as weak `Assumed` and may never be cited as `Confirmed`.

Two reminders that stop this register being misused:

1. **Membership here is not the only route to *decision blocked*.** A `Conflicted` decision-critical
   value, a volatile fact with no current reading (`volatility-register.md`), or a decision-changing
   provisional disqualifier `decision-tree.md` §4 refuses to settle each reach the same terminal.
2. **Non-membership is not permission to skip a concern.** Coverage is set by the twelve concerns and the
   emergent-concern obligation (`decision-tree.md` §5, §7.3), never by this list.
