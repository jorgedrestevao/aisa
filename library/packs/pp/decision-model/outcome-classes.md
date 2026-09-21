# Outcome Classes — the closed terminal set

<!--
provenance: RUNTIME (decision-model register) · consumed at stage S9 of decision-tree.md
authored: 2026-09-04 (Step 3B1) · design authority: Step 3A — Options Decision Model
Stage-local: loaded at S9 only. Never preloaded.
Class NUMBERS and subtype CODES are internal execution anchors. `options.md` renders the class's
NAME and its template sentence — never "class 6", never "7-INFEASIBLE" (decision-tree.md §14.3).
-->

## 0. The governing rule

> **Exclusion, candidate generation, comparative evaluation and preference are four different
> statements. A terminal outcome must never collapse them.**

Two consequences a terminal sentence must obey:

1. **No outcome may contain *preferred*, *better*, *cheaper*, *faster*, *easier*, *more scalable* or
   *lower TCO* about a class the pack has not evaluated.** The permitted form is
   *excluded → candidates → evidence obligation*.
2. **Every non-platform terminal outcome carries `COMPARATOR EVIDENCE ABSENT` unless §4 says otherwise.
   The marker is part of the outcome, not a footnote to it.**

**Closure is testable.** Any outcome label emitted anywhere that does not appear in §1 below is a
**defect in the emitter, not a new class**. Two labels were withdrawn on exactly this test during the
pack's own authoring.

**Numeric position carries no ordering and no preference.** The numbers exist so the registers and tests
can reference a class unambiguously; they are bookkeeping.

---

## 1. The fifteen classes

| # | Name | Emitted when | Render template |
|---:|---|---|---|
| **1** | **STRONG FIT** | Positive signals across the relevant concerns; no disqualifier of any scope; no composed row fires; entitlement funded; operating model matches the criticality class | *"No documented constraint is violated for this scope: `<the concerns that were decisive>`."* Phrased as *no documented constraint violated*, **never as endorsement** |
| **2** | **FIT WITH CONSTRAINTS** | One or more caution signals with **funded, owned** mitigations; the conditions are stated as conditions and carried into the decision record | *"Viable for this scope, provided: `<condition — owner — funded? — by when>`. `<Where a tripwire applies: the metric that would force the move.>`"* |
| **3** | **HYBRID WITH CLOUD-NATIVE SERVICES** | A responsibility-scoped exclusion on a **bounded, nameable** excess (compute, delivery guarantee, run duration, protocol, network reach, secret-free identity) **and** every capability gate at S7 satisfied | *"For `<the application scope>`: viable. For `<the named responsibility>`: relocated to cloud-native services. Gates satisfied: `<operator · support · skills · cross-boundary release owner · maturity>`."* Rendered as a **scope pair** |
| **4** | **HYBRID WITH THE INCUMBENT SYSTEM** | A responsibility-scoped exclusion on the integration or authority responsibility; the incumbent keeps authority and the contract; the platform supplies experience and human workflow | *"For `<the application scope>`: viable. For `<the authority/integration responsibility>`: the incumbent owns it. `INCUMBENT FIT UNEVALUATED`."* Rendered as a **scope pair** |
| **5** | **POOR FIT — EXCLUDED FOR THIS SCOPE** | A whole-scope disqualifier fires, **or** a registered composed row concludes the option is unavailable | *"`<The platform>` is excluded for `<scope>`: `<the requirement it cannot satisfy>`."* Followed by class **8** |
| **6** | **EXCLUDED FOR THIS RESPONSIBILITY** | A responsibility-scoped disqualifier fires and no in-scope hybrid shape is available, or the responsibility **is** the whole deliverable. **Names the responsibility** | *"`<The platform>` is excluded for `<the named responsibility>`. It may remain the correct answer for `<the surrounding scope>`."* — and the outcome **must say so**. Followed by class **8** |
| **7** | **ECONOMICALLY INFEASIBLE \| ECONOMICALLY UNATTRACTIVE** | An economic disqualifier fires: the required entitlement, control population or operating tier is unfunded, or disproportionate to the value. **Carries a mandatory reason — see §2** | See §2. Followed by class **8**. **Never implies another class is cheaper** |
| **8** | **CANDIDATE SET — COMPARATIVE FIT UNEVALUATED** | The terminal form for classes 5, 6, 7 and 14, and for class 13 form (b) | *"Candidates: `<the option classes, in plain language>`. Comparative fit `UNEVALUATED` — engagement assessment required: `<the named assessment>`."* Candidates come from `alternatives-register.md` §2; the evidence obligation from its §5 |
| **9** | **DEPLOYMENT MODEL EXCLUDES THIS PLATFORM — COMPARATOR EVIDENCED ON THIS AXIS** | The runtime is required to execute customer-hosted, private-cloud or air-gapped | *"The runtime must execute `<where>`. `<The platform>` documents vendor-operated deployment only. At least one enterprise low-code platform documents generally-available air-gapped/on-premises deployment; a second comparator's equivalent is **early access, not generally available**, and putting it on a critical path is itself an anti-pattern. A custom build also satisfies this axis. **Evidenced on this axis alone** — every other comparative dimension remains `UNKNOWN`."* **The only class that may name a comparator on evidence.** State both halves |
| **10** | **PROCESS REDESIGN / NO NEW APPLICATION** | Value below full cost of ownership; immature or self-inflicted process complexity; the requirement is a feature list of the outgoing tool | *"No new application is warranted: `<the evidence>`. The work is `<the process change>`."* **Not a technology decision**, so no comparator claim arises |
| **11** | **DO NOTHING / DEFER** | Economics negative; or a decision-blocking unknown unresolvable in the window; or a required control unfunded; or a dated change imminent that would alter the answer | *"No intervention now: `<the reason>`. Revisit when `<the named condition or date>`."* **Not a technology decision** |
| **12** | **DECISION BLOCKED — MORE EVIDENCE REQUIRED** | Any blocking-set entry is unknown; or a conflicted value is decision-critical; or a scope-blocker is engaged; or a decision-changing provisional disqualifier cannot be settled (`decision-tree.md` §4) | *"Decision blocked for `<scope>`. Evidence required: `<the question>` — expected form: `<clause \| inventory \| measurement \| drill result>` — likely owner type: `<role type>`. If it resolves to `<A>` the outcome is `<X>`; if to `<B>`, `<Y>`."* **The per-resolution outcome is mandatory** — it is what makes the evidence task worth funding |
| **13** | **ALTERNATIVE SUFFICIENT — THIS PLATFORM IS NOT EXCLUDED** | **No disqualifier of any scope fires**, and a class other than this platform is the documented answer for this requirement shape — either stated positively by the pack, or because an in-platform redirect's destination is that class. **Two forms — see §3** | See §3 |
| **14** | **IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED** | A **registered** composed row concludes the existing artefact **cannot be brought to the required class in place**. Distinct from class 5: the option is not unavailable — the same platform is a legitimate candidate **rebuilt** | *"The workload cannot be brought to the `<required>` class in place: `<the named mechanisms>`. The work is a **migration, not a remediation**."* Followed by class **8** |
| **15** | **VIABLE IF THE RULE IS CHANGED** | An **existing rule of the organisation** — not a technical limit — is what makes the option unavailable: a standing policy, an estate standard, an imposed platform, a segregation convention. The technical evaluation reached *viable* or *viable with preconditions*, and only the rule stands in the way | *"Viable if the rule is changed — **rule**: `<which, with its id>` · **condition**: `<what would have to change>` · **impact**: `<what it buys>` · **cost**: `<effort or money of changing it>` · **risk**: `<what goes wrong>` · **who can change it**: `<role>` · **status**: `<not requested \| requested \| refused>`."* **Never followed by class 8**: the option is not excluded, it is conditional. Whether to pursue the rule change is the owner's decision at `/decide` — and it cannot be taken about an option nobody was shown |

### 1.0 An organisational rule reaches class 15, never an exclusion

**A rule of the organisation is not a technical finding, and it never emits classes 5, 6, 7, 9 or
14.** Those are exclusions on the evidence: the platform cannot satisfy the requirement. A rule is
a decision someone made and someone can unmake, so the honest terminal is **class 15** — the
option stays on the table, priced, risked, with the rule named and the role that can change it.
Deleting the option instead hides a decision the owner is entitled to take, and makes the
organisation's own policy look like a law of physics.

Two consequences:

- **An imposed technology is a rule.** The set is generated inside it (`decision-tree.md` §6.2);
  another platform appears only as class 15, never as an ordinary candidate.
- **Class 15 is not architectable while the rule stands.** Its status field is what a later round
  reads: `refused` closes it for this engagement (carry a `Risky` row), `requested` keeps it open.

### 1.1 Which outcomes are settled exclusions

**Classes 5, 6, 7, 9 and 14 are settled exclusions and cannot be emitted from `Assumed` evidence alone**
— decision-changing or not. They require `Confirmed` **and current** evidence on the finding that fires
them (`decision-tree.md` §4). A provisional finding may still appear in the option assessment; where it
is decision-changing, the terminal is **class 12** until it is resolved.

### 1.2 Scope pairs

**One outcome per scope, not one per engagement.** A responsibility-scoped exclusion takes a named
responsibility off the platform and leaves the rest, so an engagement legitimately terminates in more
than one class, each bound to a named scope:

- *fit with constraints* for the application **and** *hybrid* for the analytical responsibility;
- *excluded* for a consumer surface **and** *strong fit* for the operations behind it;
- *excluded for this responsibility* for an integration **and** *hybrid with the incumbent* where the
  incumbent keeps authority.

**Render *(scope, class)* pairs and never collapse them.** Collapsing is how a bounded exclusion becomes
a whole-solution rejection.

### 1.3 What in-platform redirects and combination inputs may reach

- An **in-platform redirect** may produce class **2**, or class **13** where its destination is a class
  the pack documents as sufficient. It may **never** produce 3, 4, 5, 6 or 7. *An in-platform store,
  pattern or surface change is not an exclusion of the platform.*
- A **combination input** produces **no outcome on its own**. Resolve the finding it feeds.

---

## 2. Class 7 — the mandatory reason discriminator

Class 7 is **one** class covering two materially different findings. The bare disjunction
*"economically unattractive or infeasible"* is something a sponsor cannot act on. **No class 15 is
created.** The class carries a mandatory reason instead.

| Internal subtype | Meaning | Trigger | What is rendered |
|---|---|---|---|
| `7-INFEASIBLE` | **Economically infeasible.** A mandatory requirement or control cannot be funded or economically satisfied. **A funding fact, not a judgement** | An unfunded **mandated** control, entitlement or operating tier; composed row `CD-03` | *"`<The platform>` is **economically infeasible** for this scope: `<the mandated control or entitlement>` is unfunded. Candidates: `<classes>`. Comparative fit `UNEVALUATED`."* |
| `7-UNATTRACTIVE` | **Economically unattractive.** The option is feasible; its economics are disproportionate to the stated value or constraints. **A proportionality judgement**, and reversible if the value case changes | Value below full cost of ownership; the audience-and-frequency shape; the required support tier — **with funding available** | *"`<The platform>` is **economically unattractive** for this demand shape: `<the dimensions that move, and by what mechanism>`. Candidates: `<classes>`. Comparative fit `UNEVALUATED`."* |

**Four rules.**

1. **The disjunction is never rendered where the evidence supports one condition.** Writing *"economically
   unattractive or infeasible"* when the finding is an unfunded mandated control hides the only fact the
   sponsor can act on — **funding it restores viability; a proportionality judgement does not**.
2. **The subtype is chosen from the trigger, not from tone.** Unfunded **mandated** requirement ⇒
   `7-INFEASIBLE`, always. Everything else ⇒ `7-UNATTRACTIVE`.
3. **Both subtypes carry the evidence-grade rule.** An unfunded mandate asserted from an `Assumed` budget
   row is a **provisional** finding, never a settled class 7 — carried with its basis where it is not
   decision-changing, and escalated to **class 12** naming the budget confirmation where it is.
4. **Neither subtype may imply another class is cheaper.** No comparative TCO exists in either direction.

**The internal codes never appear in output.** The **discriminator must be visible in the sentence**
(*economically infeasible* / *economically unattractive*); the code must not.

---

## 3. Class 13 — two forms that never merge

**Both forms are mandatory on two points**, and a sentence missing either is malformed:

- (i) it must state that **this platform is not excluded**, so the class can never be read as a
  rejection; and
- (ii) it must carry a **graduation trigger** — the named condition under which the answer must be
  revisited — because the documented growth path out of the lighter surfaces is a **one-way upgrade**
  that converts every user to the paid tier. Without the trigger, the answer is a trap.

| Form | When | Render |
|---|---|---|
| **(a) documented sufficiency** | The substituted class is the **collaboration-platform native capability**, on one of the four shapes the pack states positively: the document *is* the record · a small flat tracker with one or two lookups, list-level security and low write concurrency · a form whose audience is the list's audience · team scope matching seeded entitlement | *"No documented constraint excludes `<the platform>`. `<The collaboration capability>` is the documented answer for this shape, and is the lighter option **on the seeded-entitlement fact alone** — no comparative TCO is asserted. Graduation trigger: `<the named condition>`."* **Stands alone** — not followed by class 8 |
| **(b) candidate, not documented sufficiency** | The substituted class is **any other** class — extend the existing system, buy a product, or anything else | *"No documented constraint excludes `<the platform>`. `<The class>` is a candidate for this shape. `COMPARATOR EVIDENCE ABSENT` — engagement-level evaluation required. Graduation trigger: `<the named condition>`."* **Followed by class 8** |

> **The comparative clause exists only in form (a), scoped to the entitlement fact, and never in form
> (b).** Emitting it unconditionally prices other classes on no evidence — the defect this split repairs.

Where the requirement crosses any of the collaboration surface's documented exclusion triggers, **class
13 does not apply** and this platform is the answer.

---

## 4. Comparator separation — run before writing any terminal sentence

`COMPARATOR EVIDENCE ABSENT` is the **default**. Four steps, never collapsed:

| Step | Question | Availability |
|---|---|---|
| 1 | **Exclusion** — is this platform excluded, and at which scope? | Almost always available |
| 2 | **Candidate generation** — which option classes come into scope? | Almost always available |
| 3 | **Comparative evaluation** — what does the evidence actually say about those classes? | A minority of questions |
| 4 | **Preference** — which of the survivors is better? | **One axis only: the deployment model (class 9).** Everywhere else: not permitted |

In-platform redirects and unresolved combination inputs **never enter step 1**.

**What the evidence at step 3 actually contains**, so it is neither overstated nor forgotten: documented
**limits** on an alternative class, documented **unavailability**, a documented **capability the
alternative lacks**, an explicit **`UNKNOWN`**, and exactly one documented **positive** (a class with
full engineering capability inherits a mature delivery capability instead of building it). **Nothing in
it says any class is faster, cheaper, more scalable or more reliable than any other — including than
this platform.**

**On the four questions most often asked of a decision model — which is cheaper, which is faster, which
scales further, which is more reliable — the answer is `COMPARATOR EVIDENCE ABSENT`, in every direction,
for every class.**

**Residual risk, recorded rather than closed.** The pack's negative evidence is richer for this platform
than for any alternative, while its coverage of *fit* runs the other way. The countermeasure is that
`COMPARATOR EVIDENCE ABSENT` is **part of the outcome string**, so a reader cannot mistake *unevaluated*
for *evaluated-and-lost*.

---

## 5. Recommendation semantics

What the round-level *"what the evidence supports"* line may say, and which outcomes back it.

| Recommendation | Meaning | Backed by |
|---|---|---|
| **Preferred** | Evidence supports one option over the viable alternatives | 1, 2; 9 or 13(a) where the comparator or sufficiency evidence exists |
| **Conditionally preferred** | Strongest **provided** explicit preconditions hold — named, owned, funded, dated | 2 with its conditions; 3 / 4 with their gates satisfied |
| **Multiple defensible options** | Evidence does not justify pretending one is uniquely superior | 8 with two or more candidates; 13(b) |
| **Decision blocked** | Decision-changing uncertainty remains | 12 |
| **No technology intervention justified** | The problem does not warrant new software | 10, 11 |
| **Excluded, at a named scope** | Out for the whole scope, for a responsibility, or on economics | 5, 6, 7 — each followed by 8 |
| **Migration, not remediation** | The artefact cannot be brought to the required class in place | 14 → 8 |
