# Composed Disqualifiers — the registered combinations

<!--
provenance: RUNTIME (decision-model register) · consumed at stage S6 of decision-tree.md
authored: 2026-09-04 (Step 3B1) · design authority: Step 3A — Options Decision Model
Stage-local: loaded at S6 only. Never preloaded.
`CD-NN` ids are internal execution anchors and are NEVER rendered to the engagement.
-->

## 0. Why this register exists

These are **not** concerns and **not** criteria. They are **combinations in which every participating
condition reads individually acceptable and the combination is worse than any of its parts.**

> **A set of individually-conditional verdicts is not a pass.**

They are invisible to per-concern reading, which is exactly why S6 runs them **explicitly** rather than
hoping they surface. Two of the twelve are drawn from **governance** and **lifecycle** — the two concerns
that produce no exclusion of their own. Before they were registered, a concern that could not reject the
platform on any single question was contributing nothing to the one test designed to catch precisely
that.

**Run order at S6.**

1. **Resolve every combination input first.** A finding whose only role is to feed a row below is not a
   terminal. Terminating on one is a category error — resolve the row it feeds.
2. **Run the twelve rows below.** Each row fires only when **all** its participating conditions hold.
3. **Then run the emergent test** (§2).

**The register is closed at twelve.** Adding a thirteenth row to make a flag resolve would be invention:
it would assert a conjunction the pack's evidence never states as a disqualifier.

---

## 1. The twelve registered rows

Scope column: **whole solution** = the finding applies to the solution scope under discussion ·
**named responsibility** = it applies only to the responsibility named · **sponsor-side** = the finding
is about the organisation, not about any technology.

| # | Participating conditions (all must hold) | Scope | Consequence | Reachable outcome |
|---:|---|---|---|---|
| **CD-01** | Strict cross-system atomicity required **+** more than one transactional owner **+** no acceptable compensation window | whole solution | **No pattern supplies the atomicity.** The answer is to collapse to one transactional owner, not to choose a mechanism | **Poor fit — excluded, whole scope** → candidate set |
| **CD-02** | A pattern requiring an external component **+** no operating **mechanism** stated for it: no role that can act on a failure, no alerting or diagnostic surface, no recovery path | whole solution | The pattern's **operation is unspecified** — not the pattern unavailable. What an architecture consumes is the mechanism, never a staffing decision (`blocking-set.md` B-17) | **Fit with constraints** — a **requirement** on the chosen path (the alerting surface, the diagnostic access and the recovery path it must carry) plus a `Risky` row. **Never an exclusion and never *decision blocked*:** an absent operator recurs identically on every candidate that needs an external component, so it separates nothing |
| **CD-03** | Private-network / key-control / firewall requirement **+** the licence population it implies is unfunded | whole solution | Security requirement and commercial constraint are **incompatible**. This is an **economic** finding, not a capability one | **Economically infeasible** (mandated control unfunded) → candidate set. **Never implies another class is cheaper** |
| **CD-04** | Business- or mission-critical **+** no representative managed test environment **+** no recovery drill | whole solution | The production commitment **cannot be evidenced.** A validation gap, not a platform-capability finding | **Decision blocked** — the drill and the test environment are the evidence task, never an exclusion |
| **CD-05** | High-frequency custom-connector workload **+** sizing resting on either side of the open throughput conflict, unmeasured | named responsibility | Sizing is **decision-blocking**. The row cannot resolve until the figure is re-read and the workload measured | **Decision blocked** — naming both the re-read and the measurement. Cuts across the platform, cloud-native and hybrid classes **symmetrically** |
| **CD-06** | Per-user backend authorization required **+** a facade or worker calling downstream as a shared identity | named responsibility | The pattern **changes the authorization semantics** of every exchange through it | **Conditional.** *Fit with constraints* where identity is propagated through the intermediary, or compensating authorization is implemented — the condition is stated and owned. **Decision blocked** where propagation feasibility is unknown. **Never an exclusion outcome** — no off-platform destination is named by any condition in this row |
| **CD-07** | Hybrid architecture required **+** no pro-code capacity **and** no enterprise-platform capability | whole solution | A platform-only implementation is the wrong fit, and the classes that would carry the other half are **equally unavailable** | **Poor fit — excluded, whole scope** → candidate set, with the capability gap named on **both** sides |
| **CD-08** | Replication in the design **+** no reconciliation **role and detection mechanism** stated per replicated entity **+** a recovery/restore requirement | whole solution | A routine restore creates data divergence that **nothing detects and no role can correct**. Detection alone does not correct anything (`blocking-set.md` B-02) | **Fit with constraints** — a **requirement** on the chosen path (per replicated entity: the role that corrects, the mechanism that detects) plus a `Risky` row naming silent divergence. **Never an exclusion**; a person's name and their acceptance are not inputs here |
| **CD-09** | Criticality class **two or more levels above** demonstrated operating maturity **+** no funded maturity plan | **sponsor-side** | The gap changes **what the architecture must automate, alert on and recover by itself** — it does not change which architecture is right (`blocking-set.md` B-26) | **Fit with constraints** — a **requirement** on the chosen path (the architecture carries what the operation cannot) plus a `Risky` row naming the commitments the operation cannot evidence. **Never a platform exclusion and never *decision blocked*** — the gap recurs identically on every candidate, so it separates nothing, and naming this platform would misattribute a sponsor-side finding as a capability one |
| **CD-10** | Offline write **+** field-level security · **or** offline **+** non-governed data beyond the documented bound · **or** mobile-first **+** device hardware **+** branded distribution with push | whole solution | Each pair is a **documented mutual exclusion**; the combination is unsatisfiable in-platform | **Poor fit — excluded, whole scope** → candidate set |
| **CD-11** | Citizen-built artefacts outside a managed solution, in the default estate **+** criticality now business-critical or above **+** the original maker gone | whole solution | The workload **cannot be brought to the required class in place**: non-solution artefacts are outside backup, ineligible for capacity licensing and undeployable, a non-solution automation's owner **cannot be changed at all**, and the departed maker's profile has already reverted | **In-place remediation unavailable — migration required** → candidate set. **The class exists because the remediation estimate a sponsor is usually given is for the wrong work** |
| **CD-12** | Continuous change **+** two or more concurrent makers **+** no pro-code capacity to reach the source-controlled isolation rung | whole solution | **No isolation mechanism is available at any reachable rung.** Every modification lands directly on the environment, co-authoring is not available, and there is no supported first-party functional-test framework to catch the overwrite. **Overwriting is the documented outcome**, not a risk | **Poor fit — excluded, whole scope** → candidate set |

**Two rows are deliberately conditional** — CD-06 and CD-09 — and in both cases the condition is
**stated, not left to inference**. Do not collapse either into a single verdict.

**Three rows produce a requirement, never an exclusion** — CD-02, CD-08 and CD-09 (P-22). An absent
operator, an absent reconciliation role and an operating-maturity gap are **organisational**, and an
organisational gap recurs identically on every candidate: it separates nothing, so it decides nothing.
Each lands as a **requirement on the chosen path plus a `Risky` row**, carried into `/decide` and into the
implementation spec, and priced where it costs money. Before this alignment the three excluded or deferred
while `blocking-set.md` B-02, B-17 and B-26 — the same findings, read one stage earlier — already resolved
them as requirements: the register contradicted the set that feeds it. What still excludes is a capability
or economic finding about the platform, and what still blocks a decision is an unresolved question on one
of the seven technical axes (`decision-tree.md` §6.1) — neither is touched here.

**No row maps to an exclusion outcome unless its consequence is an actual capability or economic finding
about the platform.** CD-01, CD-07 and CD-10 are capability findings; CD-03 is economic; CD-04, CD-05 and
CD-06's unresolved branch are evidence gaps; CD-02, CD-08 and CD-09 are requirements and risks of the
chosen path; CD-11 is a migration, not an exclusion.

---

## 2. Emergent combinations — evaluated, never registered

After the twelve rows, ask **one** question:

> *Do any two or more concerns, each individually acceptable, produce an unacceptable combination here?*

If the answer is yes:

- **Record it as a `Risky` row** with **both** anchors named, and where it is decisive, as a decision
  blocker with its `swing: decisivo`.
- **Evaluate it on engagement evidence.** Where the pack's own evidence does not support the conjunction,
  say so — mark it as having **no pack basis** and log it as an authoring feedback item
  (`decision-tree.md` §7.3).
- **Do not invent platform certainty** to make it resolve.

> **An emergent combination does not become a registered row merely because it occurred.**

The distinction is load-bearing. A registered row carries a documented conjunction and a **reachable
outcome**; an emergent one carries engagement reasoning and its own evidence. Promoting an emergent
combination into this register is how a pack acquires disqualifiers nobody can trace — the same failure
mode as an invented threshold. Promotion is an **authoring** decision, taken with evidence, outside
runtime.
