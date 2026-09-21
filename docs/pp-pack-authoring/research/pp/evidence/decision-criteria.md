Research Status: CANONICAL
Research Confidence: MEDIUM
Block: D — Decision Intelligence
Area: 15 — Decision Criteria
Gate: PASS — Block D Final Bounded Gate Recheck
Canonicalization Basis: Block D Final Bounded Gate Recheck (`block-d-final-gate-recheck.md`)
Upstream Evidence Baseline: Areas 1–12 canonical files (`canonical-manifest.md`)
Canonicalized: 2026-09-03
Freeze Status: FROZEN FOR PP PACK AUTHORING

# Decision Criteria — Block D Research Evidence

Research area: **15 — Decision Criteria** (`../research-areas.md`).
Derivation date: **2026-09-03**.
Primary input: `canonical-manifest.md` and the twelve canonical Area 1–12 files it names.
Source policy: `../source-policy.md`.
Peer files: `anti-patterns.md` (Area 13), `alternatives.md` (Area 14), `decision-intelligence-matrix.md`.

**Purpose.** Establish the canonical, technology-neutral set of requirements and constraints that can materially change an architecture decision — and, for each, what changes depending on its value. This is the most consequential Block D output: it is the layer a later question bank, signal catalogue and decision tree would be built from.

**What this file is not.** Not a question bank. Not a signal catalogue. Not a decision tree. Not a scoring model — see §2.4, which explains why a score would actively destroy information here.

---

## 1. Identifier namespace and lineage

### 1.1 The problem with `DC-NN`

The brief warns against reusing existing identifiers without first establishing whether they are local. Investigation on 2026-09-03 found that **`DC-NN` is the most heavily collided namespace in the canonical corpus**:

| File | Range | Meaning of `DC-01` in that file |
|---|---|---|
| `performance-scale.md` §7 | `DC-01` … `DC-20` | *"How many rows will the largest table hold at year 3, and must users filter/sort/aggregate freely over all of them?"* |
| `licensing-cost.md` §3 | `DC-01` … `DC-17` | *"Which systems must the solution read from or write to?"* |
| `operations-support.md` §3 | `DC-01` … `DC-20` | *"If this stops working, who notices, and how quickly must someone act?"* |

Three files define **`DC-01`–`DC-17` with entirely different meanings**. A bare `DC-07` reference is unresolvable without its file. The namespace is **file-local and source-specific**, exactly as the brief anticipated.

A further defect: **`licensing-cost.md` contains a duplicate `DC-14`** — *"Which security controls are mandatory and how many people are in their enforcement scope?"* (→ LC-30) and *"Does cost need to be attributed to business units?"* (→ LC-16) share the id. The manifest records `DUPLICATE CANONICAL IDS: 0` and cites a *"Licensing/Cost `DC-14…DC-18` repair"*; in the mounted snapshot that repair is **incomplete**. Recorded, not repaired (Block D does not modify Areas 1–12). See `anti-patterns.md` §1.4.

### 1.2 The canonical Block D namespace

Block D decision criteria use **`DC-D-NNN`**. Collision check on the canonical corpus, 2026-09-03: `grep -ohE '\bDC-D-[0-9]+\b' *.md` returned empty. The namespace is clean and mechanically distinguishable from every `DC-NN` above (a `\bDC-[0-9]+\b` regex does not match `DC-D-001`).

**This file establishes the canonical decision-criterion namespace for downstream extraction.** Local `DC-NN` identifiers in Areas 1–12 are **not renamed** — manifest §4 forbids it — and remain valid *within their own files*, cited file-qualified. §8 records the full lineage from every local criterion to its canonical successor.

### 1.3 Criteria expressed without identifiers in Areas 1–12

Six further files carry decision-criteria tables whose rows are numbered `1..N` with no prefix at all, and are therefore even less citable:

| File | Section | Rows |
|---|---|---|
| `integration-architecture.md` | §9 — the variables that change the integration architecture | 28 |
| `automation-architecture.md` | §9 — the questions that change the architecture | 22 |
| `security.md` | §4 — requirement → security constraint → consequence | 20 |
| `governance.md` | §4 — requirement → governance constraint → consequence | 15 |
| `alm-devops.md` | §4 — requirement → ALM constraint → consequence | 16 |
| `architecture-patterns.md` | §3.1 — variables that move a pattern boundary | 20 |

Plus the boundary lists and fit matrices of `platform-suitability.md` §2/§3, `application-architecture.md` §1/§2, `data-architecture.md` §2/§3 and `performance-scale.md` §4.

**Total local criteria surveyed: 236** (`20 + 17 + 20 + 28 + 22 + 20 + 15 + 16 + 20` numbered, plus 58 boundary statements counted once each where they express a distinct criterion). Consolidating to **115 canonical criteria** is roughly a 2:1 compression, achieved by merging criteria that ask the same question from different areas' vantage points — the compression is recorded per criterion in the `Lineage` field.

---

## 2. What qualifies as a decision criterion

### 2.1 The inclusion test

A criterion is included only if a change in its value can materially change at least one of:

1. whether Power Platform is suitable at all;
2. which Power Platform architecture is suitable;
3. whether a hybrid architecture is required;
4. whether another technology class should be selected.

Applied strictly, this excludes preferences that do not move an architecture (button colour, naming taste), and includes some criteria that look organisational rather than technical — team skills, operating-model maturity, ownership — because the corpus repeatedly makes them **architecture-changing**: *"Choose services that your team knows how to use, or commit to training them before you choose a service"* (`platform-suitability.md` PS-40), and *"if there is no operator, the pattern is unavailable, not merely expensive"* (`architecture-patterns.md` §13).

### 2.2 Technology neutrality

Every criterion is worded so it can be elicited in a Discovery phase that forbids naming vendors and products (`.claude/rules/no-tech-mention-before-options.md`). The corpus's own signal lists were written to the same rule (`platform-suitability.md` §9, `integration-architecture.md` §13.2), and this file inherits them.

| Not a criterion | The criterion |
|---|---|
| "Need Dataverse?" | *Does the solution require a governed relational operational data store with row- and column-level authorization and field-level audit?* (DC-D-022, DC-D-026, DC-D-027) |
| "Use Power Automate?" | *What are the workflow throughput, latency, elapsed duration and failure-recovery requirements?* (DC-D-040, DC-D-042, DC-D-049, DC-D-054) |
| "Power Pages users?" | *What identity and access model is required for users outside the organisation?* (DC-D-009, DC-D-061) |
| "Managed environment?" | *Which operational and security capabilities does the criticality class actually require?* (DC-D-001, DC-D-101, DC-D-104) |
| "Premium licence?" | *Which systems must the solution reach, and how large is the population that needs that reach?* (DC-D-035, DC-D-093) |

Four criteria cannot be fully technology-neutral because they are *about* the existing estate — DC-D-109 (existing productivity estate), DC-D-111 (existing enterprise platform estate), DC-D-110 (team skills), DC-D-114 (sourcing model). These describe **current state**, which the rule permits (*"Data lives in SharePoint today ✓ (current state, not solution)"*), and each says so.

### 2.3 States, not scores

States are **semantic** and exist only where the evidence supports a useful categorisation. Where the corpus publishes no threshold, the states are qualitative and the criterion carries a measurement obligation instead of a boundary — this is manifest §7's rule against *"inventing missing numeric thresholds"*, applied literally.

Three state patterns recur:

- **Ordinal where the evidence is ordinal:** `LOW` / `MEDIUM` / `HIGH`, `NONE` / `PARTIAL` / `FULL`.
- **Categorical where the evidence is categorical:** `INTERNAL` / `EXTERNAL AUTHENTICATED` / `PUBLIC ANONYMOUS`; `BATCH` / `NEAR-REAL-TIME` / `STRICT LOW-LATENCY`.
- **`UNKNOWN` as a first-class state on every criterion.** Manifest §5 requires it: *"do not silently infer it"*. For 28 criteria, `UNKNOWN` is additionally **decision-blocking** (§5).

Where a Microsoft-published figure *does* exist and is stable, it appears in the `Decision impact` field as the boundary it is — never promoted into a state name, so that a later revalidation changes one sentence rather than a taxonomy.

### 2.4 Why there is no scoring model — and why that is a finding, not an omission

The brief forbids scoring at this stage. The corpus supplies the substantive reason, which is worth stating because it is likely to be challenged later:

**`architecture-patterns.md` §13 documents eight combinations in which every individual dimension is merely `CONDITIONAL` and the combination is `POOR FIT`, `ANTI-PATTERN` or unavailable.** Block D derives **four more** from the same corpus, giving a register of **12** — carried identically in `decision-intelligence-matrix.md` §3 and `anti-patterns.md` AP-D-059. Three of the eight conclude the option is *unavailable*, not worse. A weighted average over favourable-but-conditional dimensions would pass every one of them. Any scoring model would therefore:

- convert *"the pattern is unavailable"* into *"the pattern scores 68"*;
- allow a strong score on nine criteria to outvote a single documented disqualifier;
- imply commensurability between criteria whose evidence classes differ (a Microsoft-stated hard limit and an `INF` synthesis would carry equal numeric weight);
- destroy the `UNKNOWN` and `CONFLICTED` semantics the manifest requires be preserved, by forcing them onto a numeric axis.

The decision logic that *is* supported by the evidence is **semantic and non-commutative**: disqualifiers first, then decision-blocking unknowns, then composed combinations, then direction. `decision-intelligence-matrix.md` §5 encodes that order. Scoring, if ever introduced, belongs to a later design phase and would need to preserve all four properties above.

### 2.5 The exit taxonomy — and why one was needed

The brief is explicit and the evidence agrees: *"Do not force all criteria to have a negative threshold."* Forcing an exit onto a criterion that does not carry one is invention.

**Repair note (2026-09-03).** The first version of this file counted exits with a single `X` flag and published **36**. The criterion bodies contained **48** substantive exit statements and the matrix carried **46**. The three counts disagreed because the file was *using* a distinction it never *named*: some exits take the whole solution off the platform, some take one responsibility off it, some are economic rather than capability findings, and some do not exist at all except in combination with another criterion. Criteria whose exit was written in the form *"none as a platform exit; it is an exit from patterns"* were counted as having no exit, while structurally identical ones written as *"the responsibility leaves the platform"* were counted as having one — DC-D-039 and DC-D-040 are the clearest pair. The taxonomy below names the distinction, and **every count in this file, in `anti-patterns.md` and in `decision-intelligence-matrix.md` is now regenerated from it rather than maintained by hand.**

**Repair note V2 (2026-09-03).** The V1 taxonomy above was applied consistently across all three representations and was still **unsound**, for one reason: its `Xr` definition carried two limbs — *a responsibility leaves the platform* **or** *an in-platform pattern becomes unavailable* — whose decision consequences are opposite. Six criteria whose documented answer is a **different in-platform store, pattern or surface** (DC-D-006, 021, 025, 030, 046, 088) were therefore filed in an exit class that `decision-intelligence-matrix.md` §1 maps to the exclusion outcomes, so a pack generated from the register would emit *"Power Platform excluded for this responsibility"* for a store change inside the platform. T-02 — the corpus's best-evidenced scenario — fires four such criteria and correctly concludes **fit with constraints**, so the rule and the worked instance disagreed. A second defect had the same shape: `Xc` asserted that its exit *"lives in §3"*, and 18 of the 24 `Xc` criteria appeared in **no** §3 row, so eighteen declared exits were undetectable by the mechanism declared to detect them.

V2 fixes the model rather than the counts. `Xr` keeps **one** limb. Two classes are added for the consequences that were being smuggled into the exit taxonomy, and **neither is an exit**. `Xc` gains a **registration requirement**. Every count below is regenerated from the classification.

**Repair note V3 (2026-09-03, bounded — Block D gate repair).** `research/pp/evidence/block-d-gate.md` found that V2's repaired one-limb `Xr` test was stated correctly but never **re-applied** to the whole `Xr` class: its membership was patched for the four (five, counting DC-D-046) criteria a prior review had named, not re-derived from the test itself. Applying V2's own decisive test — *"If nothing leaves the platform, this class does not apply"* — to all 28 surviving `Xr` criteria finds two that fail it. **DC-D-049** (Automation, process elapsed duration) reads *"`BEYOND 30 DAYS` held as a single run is a documented exit for the run mechanism (not necessarily for the platform, since the state-record pattern stays in-platform)"* — its own field states the case against its class. **DC-D-068** (Security, authorization enforcement point) names no off-platform destination anywhere in its body and is already registered at `decision-intelligence-matrix.md` §3 row 6, satisfying V2's own `Xc` registration requirement. V3 moves **DC-D-049 → `Ri`** (the durable-orchestrator limb is a design option for the same in-platform redirect, exactly as V2 already treated DC-D-025's external-object-store limb) and **DC-D-068 → `Xc`** (feeding the registered row rather than exiting alone). V3 additionally replaces the `Xc` class's single global outcome mapping {5, 12, 14} with a **per-row mapping**, because twelve registered rows do not share one consequence — three resolve to an economic infeasibility, a validation gap or a design constraint, not a platform-unavailability finding — and a global mapping was routing at least one of them (row 6, DC-D-068's own row) to no valid outcome at all. See matrix §3's Class column, restated in the mapping table below.

**Four exit classes.** An exit class means **something leaves the platform**. Each criterion carries exactly one class from the seven below. The exit class describes the *scope* of what leaves, not the *strength* of the evidence: an `Xr` is as evidence-backed as an `Xp`, and is narrower on purpose.

| Class | Meaning | Test |
|---|---|---|
| **`Xp`** | **Platform exit.** At a named state, the solution scope under discussion leaves the platform. | The field states an unconditional consequence at a named state that relocates the whole scope (*"out of the platform"*, *"→ custom application"*). |
| **`Xr`** | **Responsibility exit.** At a named state a bounded responsibility — a leg, step, attribute, surface, store, mechanism or component — **leaves the platform**. The platform legitimately keeps the remainder. | The field names *what leaves the platform* (*"the integration responsibility"*, *"the affected attribute"*, *"the run mechanism"*, *"the archival responsibility"*). **If nothing leaves the platform, this class does not apply** — see `Ri`. |
| **`Xe`** | **Economic exit.** At a named state the option becomes infeasible or unattractive on commercial grounds, with no capability finding attached. | The field states infeasibility or unattractiveness and cites cost, entitlement or budget rather than a documented capability boundary. |
| **`Xc`** | **Composed-only exit.** No exit from this criterion alone. An exit exists only in a **registered** combination. | The field delegates the exit to a combination, **and the criterion is named in a row of `decision-intelligence-matrix.md` §3 / `anti-patterns.md` AP-D-059.** An unregistered combination is not an exit — it is `Cf`. |

**Two consequence classes that are not exits.** These exist because the corpus documents real, decision-changing consequences that do not take anything off the platform, and V1 had nowhere to put them except an exit class.

| Class | Meaning | Test | What it may never produce |
|---|---|---|---|
| **`Ri`** | **In-platform redirect.** At a named state a documented in-platform pattern, store, mechanism or surface becomes **unavailable**, and the documented answer is a **different in-platform choice**. | The field names the in-platform thing that changes, and **nothing leaves the platform**. | Any exclusion outcome. An `Ri` routes to §6.2 class 2 (or class 13 where the redirect's destination is another class the corpus documents as sufficient) and **never** to classes 5, 6 or 7. |
| **`Cf`** | **Combination input.** The criterion carries **no exit and no redirect of its own**. Its value is a required **input** to another criterion's exit, or to a registered composed row, and the field names which. | The field says *"none from X alone; it combines with / feeds \<named criteria\>"*. | Any outcome at all, on its own. A pack must never terminate on a `Cf` criterion; it must resolve the criterion it feeds. |

| Class | Meaning |
|---|---|
| **`—`** | **No exit, no redirect, no named dependency.** The criterion produces positive and caution signals only. |

**Classification rule where a field states more than one consequence.** The class is the **broadest scope the field reaches at a named state without further conditions**. Where a field adds an escalation (*"…and at the extreme, out of the platform"*), that escalation is conditional and does not raise the class — DC-D-023 and DC-D-044 are the two instances, and both remain `Xr`.

**Four flags are orthogonal to the class and are not exits.**

- **`B`** — decision-blocking when `UNKNOWN` (§5.2). A criterion can be `B` with no exit at all (DC-D-052) and can carry an exit without being `B` (DC-D-042).
- **`B*`** — blocking on a narrower, named scope rather than on the decision as a whole (DC-D-113 commercial model, DC-D-115 general-availability state, DC-D-116 agent commercial and governance model). Recorded separately so §5.2's set stays exactly the 28 it claims.
- **`G`** — an **evidenced alternative-side signal** exists on this criterion (§4A). `G` is not a Power Platform exit; it is the one place the model can say something about a class *other* than Power Platform without inventing a comparison.
- **`V`** — volatile value requiring current verification (§7).

**The resulting distribution over the 116 criteria.** These numbers are the output of the classification above, not an input to it.

| Class | Count | What it means for a pack |
|---|---|---|
| `Xp` platform exit | **15** | The sharpest findings. A pack may terminate the platform question on these. |
| `Xr` responsibility exit | **26** | The most common and the most misread. These produce **hybrid** and **partial-scope** outcomes, never a whole-solution rejection on their own. |
| `Xe` economic exit | **5** | Infeasibility or unattractiveness. Never a capability claim, and never a claim that another class is cheaper (§6). |
| `Xc` composed-only, registered | **8** | Invisible to any per-criterion reading. These are exactly the criteria a scoring model would lose (§2.4), and every one is named in a §3 row. |
| `Ri` in-platform redirect | **7** | **Not an exit.** A design consequence inside the platform. Rendering one as an exclusion is the V1 defect this class exists to prevent. |
| `Cf` combination input | **17** | **Not an exit.** Elicitation dependencies: ask them, then resolve the criterion they feed. Terminating on one is a category error. |
| `—` no exit | **38** | Load-bearing. A pack that manufactures an exit here is inventing a threshold (`anti-patterns.md` AP-D-051). |

**Direct exits: 46 of 116** (`Xp` + `Xr` + `Xe`). **Registered composed-only: 8.** **In-platform redirects: 7.** **Combination inputs: 17.** **No exit: 38.**

**Class → outcome mapping.** This table is the repair. V1 named the classes and left the mapping implicit, which is how an in-platform store change acquired an exclusion outcome. The mapping is now stated once, here, and `decision-intelligence-matrix.md` §1 and §5 Step 7 reference it rather than restating it.

| Class | Outcome classes it may produce (§6.2) | It may **never** produce |
|---|---|---|
| `Xp` | 5 → 8 | 1, 2, 13 |
| `Xr` | 3, 4 or 6 → 8 | 1, 5 (alone) |
| `Xe` | 7 → 8 | 1, 5 |
| `Xc` | **2, 5, 7, 11, 12 or 14 — named per registered row by `decision-intelligence-matrix.md` §3's Class column, never one class for every `Xc` criterion** (Repair V3, 2026-09-03: the twelve registered rows do not share one consequence — see matrix §3) | anything on the criterion alone; any class the row's own Class column does not name |
| `Ri` | 2, or 13 where the redirect's destination is a class the corpus documents as sufficient | 3, 4, 5, 6, 7 |
| `Cf` | none on its own | everything — resolve the criterion it feeds |
| `—` | 1 or 2 | 5, 6, 7 |

The argument the old count of 36 was carrying — that the exit distribution is *evidential rather than constructed* — survives all three recounts and is sharpened by each: Governance and ALM still produce **zero** direct exits between them (§9 item 5), the 38 dashes are still 33% of the register, V2 **reduced** the exit count from 54 to 48 by refusing to call an in-platform redirect an exit, and **V3 reduces it again, to 46**, by applying that same refusal to the two criteria V2's own membership pass missed (§2.5 Repair note V3). An exit taxonomy that shrinks under scrutiny, twice in a row, is behaving correctly.

---

## 3. Domains and register

Twelve domains, as the brief requires. Counts are regenerated from the §2.5 taxonomy; the last three columns are the ones a pack should read.

| Domain | Ids | Count | `Xp` | `Xr` | `Xe` | `Xc` | `Ri` | `Cf` | `—` | `B` | `G` |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Business | DC-D-001 … 008 | 8 | 0 | 0 | 1 | 1 | 1 | 1 | 4 | 2 | 1 |
| Users and experience | DC-D-009 … 020, DC-D-116 | 13 | 4 | 2 | 1 | 1 | 0 | 1 | 4 | 1 | 0 |
| Data | DC-D-021 … 034 | 14 | 1 | 6 | 0 | 0 | 3 | 3 | 1 | 2 | 1 |
| Integration | DC-D-035 … 047 | 13 | 1 | 7 | 0 | 1 | 1 | 3 | 0 | 5 | 7 |
| Automation | DC-D-048 … 057 | 10 | 0 | 6 | 0 | 0 | 1 | 1 | 2 | 2 | 6 |
| Security | DC-D-058 … 068 | 11 | 2 | 2 | 0 | 3 | 0 | 2 | 2 | 3 | 0 |
| Governance | DC-D-069 … 075 | 7 | 0 | 0 | 0 | 0 | 0 | 0 | 7 | 2 | 2 |
| ALM and delivery | DC-D-076 … 083 | 8 | 0 | 0 | 0 | 1 | 0 | 0 | 7 | 1 | 1 |
| Performance and scale | DC-D-084 … 091 | 8 | 2 | 1 | 0 | 0 | 1 | 4 | 0 | 4 | 0 |
| Cost | DC-D-092 … 099 | 8 | 0 | 0 | 3 | 0 | 0 | 1 | 4 | 2 | 1 |
| Operations | DC-D-100 … 104 | 5 | 1 | 2 | 0 | 1 | 0 | 0 | 1 | 2 | 4 |
| Strategic and platform | DC-D-105 … 115 | 11 | 4 | 0 | 0 | 0 | 0 | 1 | 6 | 2 | 5 |
| **Total** | | **116** | **15** | **26** | **5** | **8** | **7** | **17** | **38** | **28** | **28** |

**Direct exits (`Xp` + `Xr` + `Xe`): 46.** Governance and ALM produce **zero direct exits** between them, which §9 item 5 explains and which all three recounts preserve.

**Exactly what V2 moved, and nothing else.** Six criteria left `Xr` for `Ri` — DC-D-006 (Business), DC-D-021, DC-D-025, DC-D-030 (Data), DC-D-046 (Integration), DC-D-088 (Performance). Seventeen left `Xc` for `Cf` — DC-D-004, 011, 022, 024, 027, 035, 038, 047, 048, 058, 061, 085, 086, 087, 090, 098, 112. Seven stayed `Xc`, each named in a `decision-intelligence-matrix.md` §3 row: DC-D-001, 015, 037, 063, 064, 080, 104. No criterion moved *into* an exit class, no `Xp` or `Xe` changed, and DC-D-032 stayed `Xr` because the archival responsibility genuinely does leave the platform (§4.3) — its V1 field said *"none evidenced"* and understated its own evidence, which V2 restated from `data-architecture.md` §2 row 12.

**Exactly what V3 moved, and nothing else** (`block-d-gate.md`, `block-d-gate-repair-report.md`). One criterion left `Xr` for `Ri` — **DC-D-049** (Automation): its exit field named nothing leaving the platform, and V2's own decisive test — applied here to the whole `Xr` class rather than to a named subset — does not admit it. One criterion left `Xr` for `Xc` — **DC-D-068** (Security), now an eighth criterion named in a matrix §3 row (row 6, previously registered but unreachable by any criterion's class). No criterion moved into an exit class, no `Xp` or `Xe` changed, and no V2 classification other than these two was revisited.

**On DC-D-116's identifier.** DC-D-116 belongs to the **Users and experience** domain but is appended at the end of the namespace rather than inserted into the DC-D-009…020 range. Block D's own ids are cited from three peer files and from `decision-intelligence-matrix.md`; renumbering them to preserve a contiguous domain range would break exactly the lineage discipline manifest §4 exists to protect. The domain is carried in the criterion's `Domain` field and in the table above, not in the number.

### 3.1 Register

`B` = decision-blocking when `UNKNOWN` (§5.2) · `B*` = blocking on a narrower named scope only (§5.2 footnote) · `V` = volatile value requiring current verification (§7) · `G` = an evidenced alternative-side signal exists (§4A) · `Xp` / `Xr` / `Xe` / `Xc` = **exit** class (§2.5) · `Ri` = in-platform redirect, **not an exit** · `Cf` = combination input, **not an exit** · no class marker = no exit, no redirect, no named dependency.

**A pack must read `Ri` and `Cf` as non-exits.** They appear in this column because they are the criterion's decision consequence, not because anything leaves the platform. §2.5's class → outcome mapping governs what each may emit.

| Id | Name | Flags |
|---|---|---|
| DC-D-001 | Business criticality | B Xc |
| DC-D-002 | Strategic importance and differentiation |  |
| DC-D-003 | Time-to-value requirement |  |
| DC-D-004 | Expected solution lifespan | Cf |
| DC-D-005 | Process maturity and stability |  |
| DC-D-006 | Accountable business ownership | B Ri G |
| DC-D-007 | Expected change frequency |  |
| DC-D-008 | Process value against cost of ownership | Xe |
| DC-D-009 | User population identity class | B Xp |
| DC-D-010 | User population size | Xe |
| DC-D-011 | Number of distinct persona experiences | Cf |
| DC-D-012 | Interaction complexity and experience bespokeness | Xp |
| DC-D-013 | Brand and design-system requirement | Xr |
| DC-D-014 | Accessibility regime |  |
| DC-D-015 | Device and form-factor mix | Xc |
| DC-D-016 | Offline operating requirement | Xp |
| DC-D-017 | Language count and script direction |  |
| DC-D-018 | Freshness expectation at the user surface | Xr |
| DC-D-019 | Navigation shape and deep-link requirement |  |
| DC-D-020 | Native distribution and push-notification requirement | Xp |
| DC-D-021 | System of record per entity and field | B Ri G |
| DC-D-022 | Relational complexity | Cf |
| DC-D-023 | Queried volume per interactive access path | Xr |
| DC-D-024 | Total data volume and growth | Cf |
| DC-D-025 | Attachment and binary volume | Ri |
| DC-D-026 | Access-granularity requirement | Xr |
| DC-D-027 | Audit and evidence-retention requirement | Cf |
| DC-D-028 | Transactional atomicity span | Xr |
| DC-D-029 | Consistency class and convergence window | Xr |
| DC-D-030 | Concurrent-edit contention | Ri |
| DC-D-031 | Analytical versus operational workload separation | Xr |
| DC-D-032 | Retention and archival requirement | Xr |
| DC-D-033 | Data residency and sovereignty | B Xp |
| DC-D-034 | Migration scope |  |
| DC-D-035 | Number of integration streams and systems | Cf G |
| DC-D-036 | Integration ownership | B Xr G |
| DC-D-037 | Frequency distribution and peak shape | B Xc |
| DC-D-038 | Directionality per stream | Cf |
| DC-D-039 | Per-mechanism throughput ceiling | B V Xr G |
| DC-D-040 | Sustained end-to-end throughput at horizon | B Xr G |
| DC-D-041 | Delivery guarantee and ordering requirement | Xr G |
| DC-D-042 | Latency class | Xp |
| DC-D-043 | Payload size and type | Xr G |
| DC-D-044 | Network boundary and private-connectivity requirement | B Xr G |
| DC-D-045 | Interface availability and protocol requirement | Xr |
| DC-D-046 | Contract volatility | Ri |
| DC-D-047 | Consumer count for a backend capability | Cf |
| DC-D-048 | Automation shape | Cf |
| DC-D-049 | Process elapsed duration | Ri G |
| DC-D-050 | Synchronous response requirement | Xr G |
| DC-D-051 | Event frequency floor and trigger freshness | V Xr G |
| DC-D-052 | Idempotency key availability | B |
| DC-D-053 | Concurrency, parallelism and ordering | Xr G |
| DC-D-054 | Failure semantics after partial completion | B Xr |
| DC-D-055 | Human-in-the-loop requirement | G |
| DC-D-056 | Unattended interface-automation need | Xr |
| DC-D-057 | Compute intensity | Xr G |
| DC-D-058 | Data sensitivity classification | B Cf |
| DC-D-059 | Regulatory and contractual compliance regime | B Xp |
| DC-D-060 | Authentication and identity model |  |
| DC-D-061 | External identity requirement | B Cf |
| DC-D-062 | Privileged access and administrator-exclusion | Xr |
| DC-D-063 | Platform network-isolation mandate | Xc |
| DC-D-064 | Encryption-key control requirement | Xc |
| DC-D-065 | Secrets and credential lifecycle | Xr |
| DC-D-066 | Access-revocation immediacy |  |
| DC-D-067 | Data-egress control requirement | Xp |
| DC-D-068 | Authorization enforcement point | Xc |
| DC-D-069 | Maker and delivery model |  |
| DC-D-070 | Organisational platform-governance maturity | B G |
| DC-D-071 | Environment strategy requirement |  |
| DC-D-072 | Connector and service permissibility posture | V |
| DC-D-073 | Support and operational ownership | B G |
| DC-D-074 | Solution scope: departmental to enterprise |  |
| DC-D-075 | Retirement and lifecycle accountability |  |
| DC-D-076 | Source-control requirement |  |
| DC-D-077 | Release frequency and window |  |
| DC-D-078 | Team size and concurrent development |  |
| DC-D-079 | Separation of duties between build and deploy |  |
| DC-D-080 | Reversibility requirement | B Xc |
| DC-D-081 | Automated-testing requirement |  |
| DC-D-082 | Environment count required by the lifecycle |  |
| DC-D-083 | Cross-boundary deployment coordination | G |
| DC-D-084 | Interactive response-time requirement | Xp |
| DC-D-085 | User concurrency | B Cf |
| DC-D-086 | Request rate per acting identity | B V Cf |
| DC-D-087 | Peak load shape and growth horizon | B Cf |
| DC-D-088 | Record count per access path at horizon | Ri |
| DC-D-089 | Provability of capacity before commitment | Xr |
| DC-D-090 | In-region availability requirement | Cf |
| DC-D-091 | End-to-end availability of the composed flow | B Xp |
| DC-D-092 | Budget envelope and funding model | B Xe |
| DC-D-093 | Entitlement fit of the required capability set | B V Xe |
| DC-D-094 | Audience and frequency shape | V |
| DC-D-095 | Capacity consumption profile | V |
| DC-D-096 | External and hybrid service consumption cost | V G |
| DC-D-097 | Operational and support cost tier | Xe |
| DC-D-098 | Migration and exit cost | Cf |
| DC-D-099 | Cost attribution requirement |  |
| DC-D-100 | Recovery point and recovery time objective | B Xp G |
| DC-D-101 | Monitoring and observability depth | Xr G |
| DC-D-102 | Incident response, support hours and support tier | G |
| DC-D-103 | Diagnostic and audit evidence retention | Xr |
| DC-D-104 | Operational maturity class | B Xc G |
| DC-D-105 | Vendor lock-in tolerance and portability | Xp G |
| DC-D-106 | Exit strategy and switching cost | Xp G |
| DC-D-107 | Tolerance to vendor-driven change cadence | Xp |
| DC-D-108 | Deployment-model constraint | B Xp G |
| DC-D-109 | Existing productivity and business-application estate |  |
| DC-D-110 | Team skills and pro-code capacity | B G |
| DC-D-111 | Existing enterprise platform estate | G |
| DC-D-112 | Platform-change tracking capacity and ownership | Cf |
| DC-D-113 | Multi-tenancy and resale requirement | B* V |
| DC-D-114 | Sourcing and delivery model |  |
| DC-D-115 | Roadmap and preview dependency | B* V |
| DC-D-116 | Conversational and agentic interaction requirement | B* V |

### 3.2 Near-duplicate clusters — one elicitation, two dimensions

**Repair note (2026-09-03).** Four clusters of criteria overlap enough that a question bank generated naively from the register would **ask the same fact twice with different state vocabularies**, which is how contradictory answers to a single fact enter a Shared Understanding.

**They are not merged.** Merging would delete published `DC-D-NNN` ids that `anti-patterns.md`, `alternatives.md` and `decision-intelligence-matrix.md` already cite, which is the lineage failure manifest §4 exists to prevent. The repair is a **binding elicitation rule** instead: each cluster is elicited **once**, and the members are the dimensions of that one elicitation, not separate questions.

| Cluster | The one fact to elicit | How the members divide it | Rule |
|---|---|---|---|
| **DC-D-023** Queried volume per interactive access path · **DC-D-088** Record count per access path at horizon | *For each access path, how many records must it reason over at the investment horizon, and how deep does it traverse?* | **DC-D-023 owns volume and delegability** per path (`BELOW CEILING` / `NON-DELEGABLE…`); **DC-D-088 owns traversal depth and model shape** per path (`SHALLOW AND SMALL` / `DEEP AND LARGE`) | Elicit once. **DC-D-088 must not restate the volume answer** — it carries the depth dimension only. Where the two vocabularies disagree, DC-D-023 is authoritative on volume and DC-D-088 on depth. |
| **DC-D-098** Migration and exit cost · **DC-D-105** Vendor lock-in tolerance and portability · **DC-D-106** Exit strategy and switching cost | *What portability or exit obligation exists, and what would satisfying it cost?* | **DC-D-105 owns the requirement** (is portability required, and of what?); **DC-D-106 owns the obligation form** (must an exit be *tested*?); **DC-D-098 owns the cost** of whichever the first two establish | Elicit once. DC-D-106 is DC-D-105 *"expressed as an obligation rather than a preference"* and inherits its answer; DC-D-098 is a **cost field on that answer**, never an independent question. All three share `platform-suitability.md` PS-51 and `licensing-cost.md` §6 as their root. |
| **DC-D-037** Frequency distribution and peak shape · **DC-D-087** Peak load shape and growth horizon | *What is the peak, over what window, and how does it grow?* | **DC-D-037 is scoped to per-stream arrival** — the peak per minute per integration stream, which is what sizes a mechanism; **DC-D-087 is scoped to whole-solution load and the growth horizon**, which is what moves DC-D-040 and DC-D-023 across their thresholds | Elicit once, then **decompose**: the per-stream figure is DC-D-037's, the aggregate and the growth curve are DC-D-087's. Both remain decision-blocking, on their own scopes. |
| **DC-D-071** Environment strategy requirement · **DC-D-082** Environment count required by the lifecycle | *What environment topology does this solution require, and why?* | **DC-D-071 owns the drivers** (residency, isolation, security boundary, tenancy); **DC-D-082 owns the lifecycle driver** (how many stations the release process needs) | Elicit once and record **one topology** with its drivers attributed. The two must never produce two different environment counts. |

**Why this is sufficient rather than a compromise.** The defect the review identified is *duplicated elicitation*, not duplicated evidence: each member's `Lineage` field cites a genuinely different canonical vantage point, and collapsing them would lose the attribution that makes the merges auditable (§9 item 2). The rule above removes the duplicated question while keeping the ids the rest of Block D points at.


---

## 4. The criteria

Field order: Domain · Volatility · Confidence · Definition · Why it matters · Discovery evidence · States · Decision impact · PP positive / caution / negative-exit · Related criteria · Related anti-patterns · Related alternatives · Lineage.

`Lineage` cites the local Area 1–12 criteria this canonical criterion consolidates, file-qualified. Origin tags follow the corpus: **MS** · **MS-V** · **INF** · **T3/T4**.

---

### 4.1 Business

#### DC-D-001 — Business criticality

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The material consequence of the solution being unavailable, wrong, or unrecoverable — expressed as business impact, not as a system tier.

**Why it matters.** This is the highest-leverage criterion in the corpus, because it is the head of a chain that ends in the licence model. `operations-support.md` states it twice: *criticality → operational requirements → managed environment → premium licences*, and *"Moving from 'business-critical' to 'mission-critical' … changes the licence footprint of every user in the environment, the artefact structure, the environment topology"*. It also sets the artefact structure from day one (solution-awareness), the ownership model (service principal or capacity licence), the environment class, the validation level required, and the support tier. Nearly every other criterion's *threshold of acceptability* is set by this one.

**Discovery evidence.** What happens in the first hour, day and week of unavailability; financial, regulatory, safety or reputational exposure; whether a manual fallback exists and has been used; existing incident history of the manual process; whether the process appears in a business-continuity plan; who would be told, and who would be accountable.

**States.** `SIMPLE DEPARTMENTAL` (one maker, users report problems, short life, no formal support) · `BUSINESS-CRITICAL` (named owner, monitored, support route, multi-year life) · `ENTERPRISE` (platform team, pipeline, change control, integrated monitoring) · `MISSION-CRITICAL` (24×7 expectation, recovery commitments, drills, incident command) · `UNKNOWN`.

**Decision impact.** At `SIMPLE DEPARTMENTAL`, *"Nothing"* changes architecturally — and over-engineering it is a documented cost. At `BUSINESS-CRITICAL` and above: solution-aware artefacts, non-personal ownership, telemetry, an environment class with backup coverage, a named support route. At `ENTERPRISE`: correlation identifiers across boundaries, audit enabled with its unfunded capacity cost, environment strategy. At `MISSION-CRITICAL`: regional resilience (with its storage doubling, premium licences and automation-throughput degradation), per-dependency failure-mode analysis, drills, incident command.

**PP positive.** `SIMPLE DEPARTMENTAL` to `BUSINESS-CRITICAL` where the estate already holds the entitlement — the platform's documented centre of gravity.
**PP caution.** `ENTERPRISE` and above: the managed-environment chain makes this an economic decision (DC-D-093, DC-D-097), and observability becomes licence-gated (DC-D-101).
**PP negative/exit.** [`Xc`] none evidenced from criticality alone. Criticality **combines** into exit conditions via DC-D-091, DC-D-100 and DC-D-089 — it never disqualifies by itself, and treating it as if it did is `anti-patterns.md` AP-D-039.

**Related criteria.** DC-D-074, DC-D-104, DC-D-100, DC-D-101, DC-D-102, DC-D-089, DC-D-093, DC-D-097.
**Related anti-patterns.** AP-D-039, AP-D-040, AP-D-047, AP-D-052, AP-D-053, AP-D-065.
**Related alternatives.** ALT-002, ALT-004, ALT-009, ALT-010.
**Lineage.** `operations-support.md` §1, §1.1, DC-16; `licensing-cost.md` DC-11, LC-23; `platform-suitability.md` PS-04, PS-33, §2 row 7; `alm-devops.md` §1, §4 rows 1–2; `architecture-patterns.md` §5.1 (operational-maturity row).

---

#### DC-D-002 — Strategic importance and differentiation

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether the capability differentiates the organisation competitively, or is a standardised process that any comparable organisation performs the same way.

**Why it matters.** It selects between building and buying, and it sets how much bespoke investment is justified. The corpus's ladder puts configure-or-buy at rung 0, *before any app type*, and warns that replicating a legacy solution *"can also lead to a highly customized solution that fails to apply the strengths of the new platform"*. For a non-differentiating domain, a packaged product usually wins on time and total cost; for a differentiating one, the constraints of a packaged product's configuration space become the binding limit.

**Discovery evidence.** Whether competitors do this differently; whether the process is a source of advantage or of parity; whether a product category exists for it; whether the organisation would licence this capability to others.

**States.** `COMMODITY` (standardised; products exist) · `ADAPTED` (standard process with organisation-specific variation) · `DIFFERENTIATING` (the process is the advantage) · `UNKNOWN`.

**Decision impact.** `COMMODITY` → configure or buy first (ALT-011, ALT-001, ALT-003); building is justified only if no product fits without customisation exceeding a build. `DIFFERENTIATING` → building is justified, and the constraint becomes which platform can express the difference (DC-D-012, DC-D-013). `ADAPTED` → the common and hardest case: buy the core and build the difference around it, which is a hybrid of ALT-011 and ALT-004.

**PP positive.** `ADAPTED` and `DIFFERENTIATING` for internal business processes — the platform's documented strength is organisation-specific process work over the existing estate.
**PP caution.** `COMMODITY` where a first-party or marketplace product covers the domain: the corpus routes this to `CUSTOM/OTHER (configure or buy)` before any build.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-003, DC-D-008, DC-D-012, DC-D-109, DC-D-111.
**Related anti-patterns.** AP-D-007, AP-D-004.
**Related alternatives.** ALT-011, ALT-001, ALT-003, ALT-007, ALT-004.
**Lineage.** `platform-suitability.md` PS-41, §2 row 26; `application-architecture.md` AA-36 rung 0, §1 row 0, AA-20; `licensing-cost.md` §6 (existing sunk capability).

---

#### DC-D-003 — Time-to-value requirement

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The date by which the capability must be delivering value, and the consequence of missing it.

**Why it matters.** It bounds which classes are reachable, and it is the criterion most often used to justify skipping the obligations other criteria impose. The corpus is careful in both directions: it never asserts that low-code is faster (a marketing claim by its own source policy), but it does record that lead time is a real property of a governed boundary — *"every new capability now needs a boundary change owned by another team"*, with the cost unquantified — and that a second platform imports a second delivery and operating model.

**Discovery evidence.** The driver behind the date (regulatory, contractual, seasonal, competitive, political); what happens if it slips; whether a partial delivery has value; the lead time of any team whose change is on the path.

**States.** `NO FIRM DATE` · `MONTHS` · `WEEKS` · `IMMEDIATE / IN-QUARTER` · `UNKNOWN`.

**Decision impact.** Aggressive dates favour classes with no new estate to stand up (ALT-001, ALT-002, ALT-003, ALT-011) and disfavour classes requiring a second operating model (ALT-006, ALT-009) or a platform change (ALT-008). Critically, an aggressive date **does not remove obligations**: where it collides with the criticality class's requirements (DC-D-001), the corpus's instruction is to name the contradiction rather than absorb it.

**PP positive.** `WEEKS` to `MONTHS` where the requirement fits existing entitlement and needs no external estate.
**PP caution.** `IMMEDIATE` combined with `BUSINESS-CRITICAL` or above: the operational and ALM obligations of DC-D-001 have lead times of their own, and compressing them is `anti-patterns.md` AP-D-052.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-001, DC-D-005, DC-D-070, DC-D-110, DC-D-114.
**Related anti-patterns.** AP-D-052, AP-D-041, AP-D-047.
**Related alternatives.** ALT-001, ALT-002, ALT-003, ALT-011, ALT-010.
**Lineage.** `architecture-patterns.md` AP-10 (weaknesses: lead time), §5.1; `automation-architecture.md` §4.1 (no operating model); `licensing-cost.md` LC-29; `platform-suitability.md` PS-40.

---

#### DC-D-004 — Expected solution lifespan

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How long the solution is expected to remain in service, and who will maintain it across that period.

**Why it matters.** Lifespan converts one-off costs into recurring ones and exposes the platform's change cadence. The corpus records the mechanism plainly: mandatory semi-annual release waves cannot be declined, the deprecation register is *"continuous and dated"* with items that *"delete or silently break things"*, and remediation is *"a recurring, unavoidable line"*. Lifespan also drives the refactoring cost of a deliberately-cheap start and the migration cost of any structural limit reached later. And it changes the exposure profile per surface — the corpus ranks vendor-driven interface change exposure as highest on the record-centric surface, medium on the task-focused one, lowest on a custom-coded one (which instead carries full own-maintenance).

**Discovery evidence.** Whether the process itself is expected to persist; whether the surrounding systems are on a decommissioning plan; whether a five-year-plus expectation exists; who is funded to maintain it in years two to five; whether a "no change" expectation has been stated.

**States.** `< 1 YEAR` · `1–3 YEARS` · `3–5 YEARS` · `> 5 YEARS` · `INDEFINITE` · `UNKNOWN`.

**Decision impact.** Longer lifespans require an explicit provision for deprecation remediation and refactoring, a named change-tracking owner (DC-D-112), and a preference for supported non-preview components (DC-D-115). At `> 5 YEARS` the corpus flags a `RISK → CONDITIONAL` verdict outright. Short lifespans legitimately relax ALM and operations obligations — and make ALT-002 and ALT-010 more attractive, since the amortisation window is small.

**PP positive.** `1–3 YEARS` with a funded maintainer and tolerance for the release cadence.
**PP caution.** `> 5 YEARS`: budget recurring remediation, and expect at least one component on the critical path to change. Where the sponsor wants productivity-workload economics with a long lifecycle, *name the contradiction*.
**PP negative/exit.** [`Cf`] none from lifespan alone; it becomes an exit condition only in combination with DC-D-107 (frozen-behaviour requirement).

**Related criteria.** DC-D-007, DC-D-107, DC-D-112, DC-D-115, DC-D-098, DC-D-008.
**Related anti-patterns.** AP-D-058, AP-D-065, AP-D-067, AP-D-006.
**Related alternatives.** ALT-002, ALT-010, ALT-005, ALT-011.
**Lineage.** `licensing-cost.md` DC-16, LC-14, LC-29; `platform-suitability.md` PS-50, §2 row 31; `operations-support.md` DC-18, OP-26, OP-28; `application-architecture.md` AA-54.

---

#### DC-D-005 — Process maturity and stability

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether the process being supported is settled, understood and consistently performed — or still being defined, contested, or performed differently by different groups.

**Why it matters.** Automating an unsettled process fixes the wrong version of it, and the corpus's strongest instruction on this is negative: *"Don't replicate your legacy solution"*, because doing so *"can lead to a highly customized solution that fails to apply the strengths of the new platform"*. Immaturity also destabilises almost every other criterion — volume, atomicity, ownership and freshness estimates all rest on a process description that is about to change.

**Discovery evidence.** Whether a documented process exists and matches observed behaviour; how many variants exist and why; whether the steps have owners; how recently it changed; whether the requirement is expressed as an outcome or as a feature list of the current tool.

**States.** `EMERGENT` (being defined) · `VARIABLE` (multiple unjustified variants) · `STABLE` (settled and consistent) · `UNKNOWN`.

**Decision impact.** `EMERGENT` or `VARIABLE` → standardisation before automation (ALT-002), or a deliberately disposable first implementation with the disposal accepted; and every volume, latency and atomicity figure gathered is provisional. `STABLE` → the other criteria's values can be relied on.

**PP positive.** `STABLE` processes, and `VARIABLE` ones where the platform's low change cost genuinely supports iterating toward stability — a legitimate use, provided the iteration is planned rather than perpetual.
**PP caution.** `EMERGENT` combined with `BUSINESS-CRITICAL`: the corpus's ALM obligations assume a target worth versioning.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-007, DC-D-008, DC-D-003, DC-D-048.
**Related anti-patterns.** AP-D-007, AP-D-001.
**Related alternatives.** ALT-002, ALT-010, ALT-004.
**Lineage.** `platform-suitability.md` PS-41; `licensing-cost.md` LC-28; `automation-architecture.md` §2 (shape classification depends on a stable description).

---

#### DC-D-006 — Accountable business ownership

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the design defines the **role** accountable for the solution's outcomes and its data, the **identity** its automation runs as, and the **procedure** followed when it fails — distinct from who builds it and who operates it. The criterion is about the design's completeness, never about which person holds the role.

**Why it matters.** The platform enforces no ownership. *"There is no default owner, no default alert and no default runbook"*; ownerless artefacts are **detected weekly and only in the managed environment class**, and reassigning ownership *"doesn't automatically"* grant the new owner environment or data-source permissions — so detection does not produce a working owner. Standard deployment makes the requesting maker the owner of deployed objects, which the corpus names as *the upstream cause of ownerless applications*. Ownership also has direct technical consequences: automation's throughput profile follows its owner's licence and reverts on their departure. And several decisions require an owner *by name* before an option is available: field authority, who may replay or compensate, who approves manual conflict resolution, who signs off reconciliation after a restore.

**Discovery evidence.** Which system is the record of truth for the data; which role is authorised to act when it breaks and on which signal; which identity the automation runs as (a service principal, a capacity-licensed identity, or a personal licence — the last carries the runtime dependency of DC-D-073); whether the reconciliation pass exists as a procedure. Who signs off, and who holds the budget, is administration and is not evidence for this criterion.

**States.** `DEFINED` (role, identity and procedure all stated) · `PARTIAL` (one or two stated) · `UNDEFINED` · `UNKNOWN`. The V1 states `NAMED AND ACCEPTED` / `NOMINAL` are retired: they graded the organisation, and the design's completeness is what a technical decision can consume.

**Decision impact.** `UNDEFINED` or `PARTIAL` is a **requirement with a cost**, priced into every option that carries it, and it is heavier on the composed patterns than on the simple ones — replication and bidirectional synchronisation of material data need the reconciliation pass to exist as a procedure, and a brokered or hybrid pattern needs the intervening role, its identity and its alert destination. It does not delete an option and it does not gate a class. Whether a cost blocks is the decision model's ruling (`decision-tree.md` §6.1 for the technical axes; `decision-model/outcome-classes.md` for the class); where an organisational rule is what stands in the way, the option returns as class 15, *viable if the rule is changed*.

> **ERRATA 2026-09-10 — refoco em decisao tecnica, fase 3.** A citacao acima fica intacta: e documentacao legitima e foi lida correctamente. O que se corrige e a **conclusao** que dela se tirou. Ver a linha *Decision impact* / *Consequence* reescrita nesta unidade, e o contrato em `05-OUTPUT-CONTRACT.md` §1, que passa a vincular qualquer re-autoria deste pacote e a autoria de qualquer outro.


**PP positive.** `DEFINED`, with automation running as a service principal or capacity-licensed identity rather than a personal one.
**PP caution.** `PARTIAL` for a departmental workload — legitimate, provided the throughput ceiling and the suspension behaviour of the chosen identity are stated.
**PP negative/exit.** [`Ri`] none as an exit from the platform. **In-platform consequence:** `UNDEFINED` or `PARTIAL` raises the cost and the risk of the composed patterns — replication and bidirectional synchronisation of material data, and the hybrid and brokered patterns — because each needs a procedure the design has not yet written. It makes none of them unavailable (the alternative-side gate, §4A.2). The documented answer is a single-owner, read-through or one-way shape with a named owner, not a platform change. Where governance ownership cannot exist at all, ALT-011's vendor-operated model or ALT-001's incumbent ownership may be the only viable classes — a **candidate** statement, not an exit.

**Related criteria.** DC-D-073, DC-D-036, DC-D-069, DC-D-075, DC-D-104.
**Related anti-patterns.** AP-D-036, AP-D-053, AP-D-013, AP-D-026, AP-D-066, AP-D-011.
**Related alternatives.** ALT-001, ALT-007, ALT-011, ALT-004.
**Lineage.** `operations-support.md` DC-01, OP-04, OP-05, OP-AP-01; `governance.md` DC/§4 row 7, GOV-13, GOV-14, GOV-XB-04; `alm-devops.md` ALM-20, ALM-A14; `automation-architecture.md` AT2-01, AT2-44, §9 rows 2, 17; `architecture-patterns.md` Y-13, §13.

---

#### DC-D-007 — Expected change frequency

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How often the solution's behaviour is expected to change after go-live, and who initiates those changes.

**Why it matters.** Change frequency selects the delivery rung and the partitioning of the solution. High change rates on a shared artefact collide with the isolation model: unmanaged work gives *"no isolation"* — *"Every modification is applied directly to the environment, regardless of which solution is being edited"* — and co-authoring on the low-code app artefact **was removed**, so parallel change requires an environment per maker. Change frequency also interacts with the release window (DC-D-077), because deployment operations are named as intensive database operations to keep out of business hours: *"Frequent releases plus no business-hours degradation is a conflict resolved by calendar, not configuration."*

**Discovery evidence.** How often the underlying rules changed in the last two years; who requests changes; whether business users expect to self-serve changes; whether change is seasonal.

**States.** `RARE` (annual or less) · `PERIODIC` (quarterly) · `FREQUENT` (monthly or more) · `CONTINUOUS` · `UNKNOWN`.

**Decision impact.** `FREQUENT` or `CONTINUOUS` → source control and per-maker environments (DC-D-076, DC-D-078, DC-D-082), partitioning by persona and team rather than by size heuristic, and an explicit release-window decision. `RARE` → lower rungs are proportionate, but DC-D-004's remediation obligation still applies regardless of the organisation's own change rate.

**PP positive.** `PERIODIC` to `FREQUENT` change initiated by business owners — the platform's documented advantage, provided the delivery rung matches.
**PP caution.** `CONTINUOUS` with several makers on one artefact: the isolation constraint is structural, not a tooling gap.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-076, DC-D-077, DC-D-078, DC-D-082, DC-D-011, DC-D-004.
**Related anti-patterns.** AP-D-042, AP-D-041, AP-D-043.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `alm-devops.md` ALM-06, ALM-23, §4 rows 3–5; `application-architecture.md` AA-03, AA-06, AA-C1; `performance-scale.md` DC-16, PF-44; `operations-support.md` DC-11.

---

#### DC-D-008 — Process value against cost of ownership

**Domain:** Business · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether the measurable value of automating or supporting the process exceeds its full cost of ownership over the expected lifespan.

**Why it matters.** This is the criterion that makes "do not build" a legitimate output. The corpus states it directly: full cost of ownership *"frequently exceeds the value of a low-frequency process even when licences are free"* — and notes that **no Microsoft source frames this option**, which is why it must be carried deliberately. It is also the criterion most often defeated by `anti-patterns.md` AP-D-060: if the cost side is a licence line rather than the twelve-plus real lines, the comparison is meaningless.

**Discovery evidence.** Frequency of the process; time per instance; cost of errors today; cost of delay today; who currently absorbs that cost; whether the value is a hard saving or an avoided cost; the full cost lines of DC-D-092 through DC-D-099.

**States.** `VALUE CLEARLY EXCEEDS COST` · `MARGINAL` · `COST EXCEEDS VALUE` · `UNKNOWN`.

**Decision impact.** `COST EXCEEDS VALUE` → ALT-002 or ALT-010, and the corpus requires both to be **priced options**, not mentions. `MARGINAL` → reduce scope, use existing entitlement only, or defer against a named trigger. Note the asymmetry this criterion exposes: the *cheapest build* is often the one whose operating obligations were omitted, so a marginal case that becomes positive after descoping the operational lines is usually a mis-priced negative case.

**PP positive.** `VALUE CLEARLY EXCEEDS COST` where the requirement sits inside existing entitlement.
**PP caution.** `MARGINAL` where the criticality class pulls in the managed-environment chain: the licence step change can invert the case (DC-D-093, DC-D-097).
**PP negative/exit.** [`Xe`] `COST EXCEEDS VALUE` → **do not build on any platform.** The exit here is not to an alternative technology but out of the technology decision entirely, which is why the corpus insists this option be carried.

**Related criteria.** DC-D-092 … DC-D-099, DC-D-001, DC-D-004, DC-D-005.
**Related anti-patterns.** AP-D-060, AP-D-039, AP-D-061.
**Related alternatives.** ALT-002, ALT-010, ALT-001, ALT-003.
**Lineage.** `licensing-cost.md` DC-15, LC-21, LC-28, §6, §0.4; `performance-scale.md` §11.1; `operations-support.md` §1.1.

---
### 4.2 Users and experience

#### DC-D-009 — User population identity class

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** What kind of identity the people using the solution hold: organisational identities, identities from another organisation, customer identities, or none at all.

**Why it matters.** It selects the application surface, the environment topology, the licensing model and the security review depth simultaneously — the corpus's four-tier ladder maps identity class directly onto available surfaces (employees → any internal surface; known partners → guest identities into internal surfaces, *conditional on cross-tenant licence recognition, which per-app entitlements do not satisfy*; authenticated customers → the external-site surface; anonymous public → that surface with the exposure conditions of `anti-patterns.md` AP-D-034, or a custom surface). Guest access to the governed data store is **restricted by default on new environments**, and that restriction covers that store only — guests still reach other surfaces in the same environment.

**Discovery evidence.** Who the users are and who employs them; whether they have organisational accounts; whether any are anonymous; whether the population is knowable in advance; whether users have an identity from a non-organisational provider.

**States.** `INTERNAL` · `EXTERNAL AUTHENTICATED — KNOWN PARTNERS` · `EXTERNAL AUTHENTICATED — CUSTOMERS` · `PUBLIC ANONYMOUS` · `NON-DIRECTORY POPULATION` (frontline, shared devices, third-party identity provider) · `MIXED` · `UNKNOWN`.

**Decision impact.** `INTERNAL` opens all surfaces. `KNOWN PARTNERS` requires a guest decision per environment, a dedicated environment, and a licence check that per-app entitlements will fail. `CUSTOMERS` or `PUBLIC ANONYMOUS` forces the external-site surface (with the data store fronting the data) or a custom surface, plus consumption-metered capacity, a mandatory permission review, a firewall and certificate/key lifecycle with a named owner. `NON-DIRECTORY POPULATION` carries an open unknown in the corpus on both identity and licensing.

**PP positive.** `INTERNAL`; `KNOWN PARTNERS` with recognised cross-tenant licensing; `CUSTOMERS` over the governed store with a reviewed permission model.
**PP caution.** `PUBLIC ANONYMOUS` — capacity metered on browser cookies rather than people, all traffic concentrated on one acting identity, freshness floor on the read surface, and a documented mass-exposure incident class.
**PP negative/exit.** [`Xp`] `PUBLIC ANONYMOUS` **combined with** any of: sub-freshness-floor requirement, a third-party integration surface (*"Web API not for third-party integration"*), server or caching control, or sensitivity the anonymous model cannot express → custom web surface. `NON-DIRECTORY POPULATION` is `UNKNOWN`, not exit.

**Related criteria.** DC-D-010, DC-D-018, DC-D-061, DC-D-058, DC-D-067, DC-D-094.
**Related anti-patterns.** AP-D-034, AP-D-032, AP-D-033.
**Related alternatives.** ALT-004, ALT-005, ALT-003.
**Lineage.** `application-architecture.md` AA-52, AA-25, §1 rows 4–5, §2; `platform-suitability.md` PS-36, PS-56, PS-60, §2 rows 14–15, 34; `security.md` SEC-04, SEC-32, §4 rows 7–8; `licensing-cost.md` DC-05, DC-06, LC-07, LC-12, LC-20.

---

#### DC-D-010 — User population size

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The number of people who will use the solution, and how many of them are active in a given period.

**Why it matters.** Population is the primary multiplier on the platform's dominant cost mechanisms — per-user and per-(person, app) entitlement — and it is also what makes a security control expensive, because control prerequisites are priced by **affected population, not by number of apps**. It does *not* select a technical ceiling: **no concurrent-user figure is published for any surface**, and the corpus checked sixteen sources. So population drives economics and validation obligations, not a limit.

**Discovery evidence.** Headcount in scope; how many are active daily, weekly, monthly; whether the population is bounded; expected growth; how many distinct applications each person needs.

**States.** `TENS` · `HUNDREDS` · `THOUSANDS` · `TENS OF THOUSANDS+` · `UNBOUNDED / PUBLIC` · `UNKNOWN`.

**Decision impact.** Large populations with low per-person frequency point toward consumption-based licensing; small populations with high frequency toward prepaid; unknown adoption toward consumption first with a true-up. Large populations also make any premium or higher-tier control prerequisite a step change (DC-D-093, DC-D-064, DC-D-063). Concurrency behaviour must be **load-tested**, never quoted (DC-D-085).

**PP positive.** Any size where the licensing shape matches the usage shape and the entitlement is funded.
**PP caution.** `TENS OF THOUSANDS+` with premium capability requirements — the corpus's retained hypothesis is that people-based mechanisms become less attractive as the users-to-work ratio rises (labelled a hypothesis, not a finding).
**PP negative/exit.** [`Xe`] Per-user or per-scope licensing *uneconomic at the audience's scale* is a documented trigger for a custom application — an economic exit, not a technical one.

**Related criteria.** DC-D-085, DC-D-093, DC-D-094, DC-D-092, DC-D-009.
**Related anti-patterns.** AP-D-051 (quoting a concurrency figure), AP-D-062, AP-D-064.
**Related alternatives.** ALT-005, ALT-004.
**Lineage.** `licensing-cost.md` DC-02, DC-03, LC-04, LC-18, §1; `data-architecture.md` SC-16, SC-17, U-31; `performance-scale.md` PF-09, §8.1 item 14; `application-architecture.md` AA-53, §1 row 10; `security.md` SEC-XB-01.

---

#### DC-D-011 — Number of distinct persona experiences

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How many materially different user experiences the solution must present — not roles in a permission sense, but genuinely divergent task flows and screen sets.

**Why it matters.** It selects the application surface and the partitioning seams. The corpus is explicit that the seam is drawn by **team and personas, not by a size number**: no numeric cap on screens or controls exists, the vendor's own large-implementation reference point is inadmissible as a threshold, and the widely-quoted screen-count heuristic is `T3/T4` and **must not be encoded**. Divergent experiences in one artefact produce formula sprawl and a one-maker bottleneck; partitioning across artefacts costs cross-artefact state loss and is a manual retrofit.

**Discovery evidence.** Persona inventory and what each actually does; whether their journeys share screens; whether one person holds several personas; how many makers will work on it.

**States.** `SINGLE PERSONA` · `2 PERSONAS, OVERLAPPING` · `2–3 DIVERGENT` · `MANY DIVERGENT` · `UNKNOWN`.

**Decision impact.** `SINGLE` or overlapping → one task-focused artefact. `2–3 DIVERGENT` or more → partition into several artefacts, or use a record-centric shell with a small number of bespoke pages (subject to that composition's own caps: page count, connector count per composition, state loss on back-navigation, and no device-capability or offline support in those pages). `MANY DIVERGENT` combined with high change frequency and several makers → the strongest in-platform argument for a record-centric surface, or for a coded surface.

**PP positive.** One to three personas with overlapping journeys.
**PP caution.** `MANY DIVERGENT` in one artefact — this is `anti-patterns.md` AP-D-005's mirror at the application layer, and the corpus names the resulting artefact as an anti-pattern.
**PP negative/exit.** [`Cf`] none evidenced from persona count alone; it combines with DC-D-012 and DC-D-013.

**Related criteria.** DC-D-012, DC-D-019, DC-D-078, DC-D-007, DC-D-068.
**Related anti-patterns.** AP-D-051 (encoding a size threshold), AP-D-050.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `application-architecture.md` AA-03, AA-04, AA-06, AA-10, AA-15, AA-16, AP-17, AA-C1, U-A1, §1 rows 1–3, §2; `platform-suitability.md` PS-06, §2 row 25.

---

#### DC-D-012 — Interaction complexity and experience bespokeness

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How far the required interaction departs from form-, list- and record-shaped patterns: bespoke layouts, novel interactions, complex client-side state, product-grade polish.

**Why it matters.** It selects a position on the corpus's documented experience ladder — platform controls → reusable components → custom code components (premium only where they make non-connector external calls) → coded applications → custom web. Each rung buys fidelity and costs maintenance, and the ladder's ordering is the vendor's own; inverting it (reaching for custom code components before platform controls) is a named anti-pattern. Reuse also has a hard structural limit that surprises teams: reusable components are **excluded from galleries and forms**, where custom code components are the only option.

**Discovery evidence.** Design artefacts and their fidelity; whether a design system must be honoured; whether interactions are described that no form or list expresses; whether the experience is customer-facing and brand-critical; whether the requirement includes a specific interaction library.

**States.** `FORM AND LIST SHAPED` · `MODERATE BESPOKE` · `HIGHLY BESPOKE` · `PRODUCT-GRADE` · `UNKNOWN`.

**Decision impact.** `FORM AND LIST SHAPED` → platform surfaces, no extension. `MODERATE` → components and selective custom code components. `HIGHLY BESPOKE` → coded applications (premium, and with their own constraints: a public asset endpoint, no repository integration, offline undocumented, no anonymous users) or a bespoke external-site surface (single-language, no repository, no offline-read). `PRODUCT-GRADE` → custom web or native.

**PP positive.** `FORM AND LIST SHAPED` and `MODERATE`.
**PP caution.** `HIGHLY BESPOKE`: the coded and bespoke-site surfaces both carry constraints the corpus keeps `CONDITIONAL` pending a general-availability check, and both carry premium licensing.
**PP negative/exit.** [`Xp`] `PRODUCT-GRADE` consumer experience, native gestures, or a mandated design system beyond colours, font and logo on the record-centric surface → custom web or native application.

**Related criteria.** DC-D-013, DC-D-015, DC-D-020, DC-D-011, DC-D-014.
**Related anti-patterns.** AP-D-003, AP-D-057.
**Related alternatives.** ALT-005, ALT-008, ALT-004.
**Lineage.** `application-architecture.md` AA-14, AA-31, AA-34, AA-35, AA-36, AA-37, AP-22, AA-23, §1 rows 1–5, 10, U-C6; `platform-suitability.md` PS-03, PS-10, §2 row 23.

---

#### DC-D-013 — Brand and design-system requirement

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How strictly the solution must conform to a brand or design system, and whether that conformance is contractual or reputational rather than aesthetic.

**Why it matters.** The record-centric surface's theming ceiling is documented and narrow — **colours, font and logo only** — so a design system that specifies component geometry, motion or layout cannot be satisfied there. The task-focused surface can go further with custom code components, and a coded or custom surface further still. Branded native distribution has its own separate ceiling (DC-D-020).

**Discovery evidence.** Whether a design system exists and is enforced; whether the audience is external; whether brand conformance is in a contract; which specific elements are mandated.

**States.** `NONE` · `LOGO AND COLOURS` · `FULL DESIGN SYSTEM` · `BRAND-CRITICAL EXTERNAL` · `UNKNOWN`.

**Decision impact.** `LOGO AND COLOURS` is satisfiable on every surface. `FULL DESIGN SYSTEM` rules out the record-centric surface's core pages and pushes to components, a coded application or custom web. `BRAND-CRITICAL EXTERNAL` combines with DC-D-009 and usually settles on the bespoke external-site surface or custom web.

**PP positive.** `NONE` and `LOGO AND COLOURS`.
**PP caution.** `FULL DESIGN SYSTEM` on a task-focused surface — reachable with custom code components, at a maintenance cost and with an inverted-ladder risk.
**PP negative/exit.** [`Xr`] A mandated design system on record-centric core pages → the ceiling is documented; either change surface or change the requirement.

**Related criteria.** DC-D-012, DC-D-020, DC-D-009, DC-D-014.
**Related anti-patterns.** AP-D-003 (as a dominant requirement).
**Related alternatives.** ALT-005, ALT-004.
**Lineage.** `application-architecture.md` AA-14, AA-36, AP-25, §1 row 2; `platform-suitability.md` PS-10, §2 row 23.

---

#### DC-D-014 — Accessibility regime

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether accessibility conformance is a legal or contractual obligation, and to which standard.

**Why it matters.** Conformance responsibility differs by surface in a way that matters legally: the external-site surface is **platform-attested**, the record-centric surface is built-in, and the task-focused surface is **maker-dependent with documented patterns that cannot be made accessible without custom code components**. The corpus also records that only **product-level** conformance reports exist — there are none per maker-built application — so a legal claim about a specific built artefact cannot rest on the platform's attestation.

**Discovery evidence.** The applicable legal regime; whether an accessibility statement will be published; whether procurement requires a conformance report; whether assistive-technology testing is contracted.

**States.** `NONE STATED` · `INTERNAL POLICY` · `LEGAL OBLIGATION` · `LEGAL OBLIGATION WITH ATTESTATION REQUIRED` · `UNKNOWN`.

**Decision impact.** A legal obligation favours the platform-attested and built-in surfaces and imposes a testing obligation on maker-built task-focused applications. Where an **attestation for the specific artefact** is required, the corpus's gap (no per-artefact conformance reports) means the obligation falls on the delivery team regardless of platform — an important symmetry, since a custom application has the same problem.

**PP positive.** `LEGAL OBLIGATION` where the external-site or record-centric surface fits the requirement.
**PP caution.** `LEGAL OBLIGATION` on a task-focused surface: conformance is the maker's, some patterns need custom code components, and one of the corpus's limitation sources is aged and may overstate the gaps.
**PP negative/exit.** [`—`] none evidenced — the obligation is surface- and process-shaped, not platform-disqualifying.

**Related criteria.** DC-D-012, DC-D-015, DC-D-017, DC-D-081.
**Related anti-patterns.** AP-D-052 (validation not matched to the claim).
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `application-architecture.md` AA-47, U-E3, AA-C7, §1 rows 2, 4; `platform-suitability.md` §2 row 2.

---

#### DC-D-015 — Device and form-factor mix

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The devices, form factors and clients through which people will use the solution — including whether device hardware (camera, scanner, location, near-field) is part of the task.

**Why it matters.** Several hard surface boundaries are decided here, and they are documented absolutes rather than degradations: the record-centric surface is **not supported in a phone browser** (a native client is required); bespoke pages inside a record-centric shell **do not support device controls**; the team-hosted surface **does not support camera, barcode or sensors**; responsive multi-device on the task-focused surface is an **opt-in rebuild** rather than a default, and the default sizing behaviour wastes screen space. Per-platform concurrent-request limits also differ between clients and are **unpublished**.

**Discovery evidence.** Device inventory in the user population; whether work happens away from a desk; whether hardware capture is part of the task; whether users will expect a browser or an installed application; network quality at the point of use.

**States.** `DESKTOP BROWSER ONLY` · `DESKTOP AND TABLET` · `MOBILE-FIRST` · `MOBILE WITH DEVICE HARDWARE` · `SHARED / KIOSK DEVICES` · `MIXED` · `UNKNOWN`.

**Decision impact.** `MOBILE WITH DEVICE HARDWARE` rules out the record-centric surface's bespoke pages and the team-hosted surface, and points to the task-focused surface (natively) or a custom application. `MOBILE-FIRST` with a record-centric requirement forces the native client, not the browser. `SHARED / KIOSK` is an open unknown in the corpus on both identity and licensing. Mobile acceptance must be **tested on target devices**.

**PP positive.** `DESKTOP BROWSER ONLY`, `DESKTOP AND TABLET`, and `MOBILE WITH DEVICE HARDWARE` on the task-focused surface.
**PP caution.** `MIXED` requiring one artefact to serve all — responsive is an opt-in effort, and the corpus warns against assuming it.
**PP negative/exit.** [`Xc`] `SHARED / KIOSK` is `UNKNOWN`. A genuine exit arises only in combination: mobile-first plus device hardware plus offline plus branded distribution with push is unsatisfiable in-platform (DC-D-016, DC-D-020).

**Related criteria.** DC-D-016, DC-D-020, DC-D-012, DC-D-084, DC-D-009.
**Related anti-patterns.** AP-D-003.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `application-architecture.md` AA-02, AA-16, AA-45, AA-50, AP-24, AP-31, U-E2, §1 rows 1–3, 6, §2; `platform-suitability.md` PS-60, U-14; `performance-scale.md` PF-11, PF-12, PF-13, PF-U-02.

---

#### DC-D-016 — Offline operating requirement

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether users must continue working without connectivity, on which surface, over which data, and whether they must **write** offline.

**Why it matters.** Offline is the corpus's cleanest set of documented absolutes, and it is where a requirement most often disqualifies a whole surface rather than constraining it. **Unsupported:** offline in a browser; offline on the team-hosted surface; offline in bespoke pages inside a record-centric shell; offline write on the external-site surface; offline combined with field-level security; offline combined with automations. Offline over the governed store is supported within a documented row ceiling and feature list; offline over non-governed data is bounded and much narrower. Offline on the coded surface is **undocumented and treated as unsupported**. Custom synchronisation or conflict rules are a documented trigger for a custom application.

**Discovery evidence.** Where the work physically happens; connectivity at those locations; whether read-only offline suffices or writes are required; how long a disconnected period lasts; what conflict behaviour the business expects on reconnection.

**States.** `NONE` · `OFFLINE READ` · `OFFLINE WRITE` · `EXTENDED DISCONNECTED OPERATION` · `UNKNOWN`.

**Decision impact.** Any offline requirement immediately narrows the surface set to the task-focused native client (over the governed store, within its list) — and eliminates the browser, the team-hosted surface, bespoke pages and the external-site surface for writes. `EXTENDED DISCONNECTED OPERATION` with custom conflict semantics moves out of the platform.

**PP positive.** `OFFLINE READ` or `OFFLINE WRITE` on the native client over the governed store, inside the documented row ceiling and without field-level security or offline automations.
**PP caution.** Offline combined with a security model that uses field-level security — the two are documented as mutually exclusive.
**PP negative/exit.** [`Xp`] Offline in a browser; offline over non-governed data beyond the documented bound; offline requiring custom synchronisation or conflict rules → custom application (ALT-005).

**Related criteria.** DC-D-015, DC-D-026, DC-D-029, DC-D-030, DC-D-021.
**Related anti-patterns.** AP-D-003, AP-D-012 (virtualization forfeits offline).
**Related alternatives.** ALT-005, ALT-004.
**Lineage.** `application-architecture.md` AA-42, AA-43, AA-44, AA-50, U-D3, U-E4, §1 rows 1–6, §2; `platform-suitability.md` PS-35, §2 rows 12–13, §3; `data-architecture.md` DA-45, §2 rows 5–6.

---

#### DC-D-017 — Language count and script direction

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How many languages the interface must present, and whether any requires right-to-left script.

**Why it matters.** Multi-language support differs sharply by surface: the record-centric surface and the templated external-site surface support it natively; the task-focused surface requires a **hand-built dictionary multiplied by screens and languages**; and the **bespoke external-site surface is single-language**. Right-to-left on a standalone task-focused application has **no vendor statement either way** — an earlier claim was withdrawn — and the corpus's rule is to *treat it as unsupported until prototyped*, never to assert it as a Microsoft position.

**Discovery evidence.** Languages required at launch and later; whether any is right-to-left; whether translation is maintained centrally; whether the audience is external.

**States.** `SINGLE` · `2–3` · `MANY` · `INCLUDES RIGHT-TO-LEFT` · `UNKNOWN`.

**Decision impact.** More than two or three languages favours the record-centric or templated external surfaces and disfavours the task-focused surface (labour) and the bespoke external surface (impossible). Right-to-left requires a prototype before commitment, on any surface.

**PP positive.** `SINGLE` or `2–3` on any surface; `MANY` on the record-centric or templated external surfaces.
**PP caution.** `MANY` on the task-focused surface — the labour is multiplicative and ongoing.
**PP negative/exit.** [`—`] none evidenced. `INCLUDES RIGHT-TO-LEFT` on a standalone task-focused application is `UNKNOWN`, to be closed by prototype — not an exit.

**Related criteria.** DC-D-012, DC-D-014, DC-D-009.
**Related anti-patterns.** AP-D-051 (asserting an unstated capability either way).
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `application-architecture.md` AA-48, AA-23, AP-33, AA-C11, U-E6, §1 rows 1–2, 4, §9 condition 1; `platform-suitability.md` §7 (deferred).

---

#### DC-D-018 — Freshness expectation at the user surface

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How current the data on the screen must be, from the moment of the change that produced it — expressed as a number, not as "real-time".

**Why it matters.** One surface has a documented, **non-reducible** freshness floor: the external-site surface's server-side cache carries a **15-minute** service level that cannot be shortened, and values derived by server-side logic there are *"never guaranteed to be immediate"* — a pattern the vendor calls *"not recommended"*. Clearing that cache on a busy live site *"can lead to users facing performance issues"*, so it is not an operational workaround either. Separately, automation writes are asynchronous and post-commit, so *"immediate"* is not available from that path at all; only synchronous server-side code runs inside the transaction. Upstream freshness also caps everything downstream — virtualizing over a batch-loaded store yields *"false freshness"*.

**Discovery evidence.** The business consequence of seeing a stale value; the actual number, in seconds or minutes; where the change originates; the upstream source's own refresh cadence; whether the user makes the change themselves.

**States.** `EVENTUAL (HOURS)` · `MINUTES` · `SUB-MINUTE` · `IMMEDIATE / READ-YOUR-WRITES` · `UNKNOWN`.

**Decision impact.** `IMMEDIATE` for a value the user just changed themselves → compute it inside the user's own transaction with synchronous server-side code. `SUB-15-MINUTE` on the external-site surface → that surface is out unless the change is made on the site itself. `MINUTES` → events or a queue. `EVENTUAL` → scheduled mechanisms, whose own floor is a 30-minute increment with a daily refresh cap.

**PP positive.** `EVENTUAL` or `MINUTES` on any surface; `IMMEDIATE` where the change is made in the same transaction on an internal surface.
**PP caution.** Derived values presented as real-time on any surface fed by background automation — a named anti-pattern.
**PP negative/exit.** [`Xr`] A **sub-15-minute freshness requirement on the external-site read surface** for data changed elsewhere → different read surface or custom web. This is one of the corpus's cleanest single-criterion exits.

**Related criteria.** DC-D-042, DC-D-051, DC-D-029, DC-D-031, DC-D-009.
**Related anti-patterns.** AP-D-024, AP-D-012 (false freshness), AP-D-009.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `performance-scale.md` PF-17, PF-18, PF-19, PF-20, DC-05, §3.A row 7, §8.1 items 8–10; `application-architecture.md` AA-27, AP-27, §2; `data-architecture.md` DA-47, DA-49, DA-51, C-11; `integration-architecture.md` I-32, §8; `automation-architecture.md` §4.3 (transaction participation).

---

#### DC-D-019 — Navigation shape and deep-link requirement

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether people navigate by browsing related records, or by moving through a defined task sequence — and whether individual records must be shareable and bookmarkable by link.

**Why it matters.** It is a clean surface discriminator. The record-centric surface provides **native record links** and automatic relational navigation; on the task-focused surface, deep links are **hand-built per destination**, and the corpus records a dated change that breaks mobile deep links without an environment identifier. Where many destinations must be linkable, the hand-built cost is multiplicative. Partitioning a task-focused estate into several artefacts also loses state on cross-artefact navigation.

**Discovery evidence.** Whether users send each other links to records today; whether records are referenced from email, chat or other systems; whether the task is a wizard or an exploration; how many distinct destination types exist.

**States.** `TASK SEQUENCE` · `RECORD BROWSING` · `MIXED` · `MANY LINKABLE DESTINATIONS` · `UNKNOWN`.

**Decision impact.** `RECORD BROWSING` or `MANY LINKABLE DESTINATIONS` → record-centric surface. `TASK SEQUENCE` → task-focused surface, or a guided-stage construct within the record-centric surface (subject to its caps and its inability to execute logic of its own). A deep-link inventory is a documented pre-commitment validation.

**PP positive.** Either shape, matched to the right surface.
**PP caution.** `MANY LINKABLE DESTINATIONS` on a task-focused surface — the labour and the dated mobile-link change.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-011, DC-D-012, DC-D-022.
**Related anti-patterns.** AP-D-058 (the dated link change).
**Related alternatives.** ALT-004.
**Lineage.** `application-architecture.md` AA-09, AA-18, AA-19, AA-03, AP-30, §1 rows 1–3, §2.

---

#### DC-D-020 — Native distribution and push-notification requirement

**Domain:** Users · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the solution must be distributed as an installable, organisation-branded application, and whether it must deliver push notifications to the device.

**Why it matters.** This is the corpus's sharpest combined absolute. Branded native distribution is available through a wrapping mechanism, but that mechanism **does not support push notifications**, **does not support consumer or business-to-consumer audiences**, is **unavailable in sovereign clouds**, excludes customer-managed keys and lockbox, caps package size, and requires a **monthly re-wrap operational commitment**. The corpus's conclusion is direct: *branded mobile app × push notifications → unsatisfiable in Power Platform*.

**Discovery evidence.** Whether the application must appear in an app store or an enterprise catalogue under the organisation's brand; whether notifications must reach the device when the app is closed; whether the audience is consumers; whether the tenant is a sovereign cloud.

**States.** `BROWSER / STANDARD CLIENT ONLY` · `BRANDED DISTRIBUTION, NO PUSH` · `BRANDED DISTRIBUTION WITH PUSH` · `CONSUMER APP STORE` · `UNKNOWN`.

**Decision impact.** `BRANDED DISTRIBUTION, NO PUSH` → the wrapping mechanism, with its monthly operational commitment, sovereign-cloud exclusion and audience limits accepted. `BRANDED DISTRIBUTION WITH PUSH` or `CONSUMER APP STORE` → out of the platform for the distribution layer; a custom native application, possibly over platform services (a hybrid front-end pattern).

**PP positive.** `BROWSER / STANDARD CLIENT ONLY`, and `BRANDED DISTRIBUTION, NO PUSH` for internal or partner-guest audiences.
**PP caution.** The wrapping mechanism's monthly re-wrap is an ongoing operations line, not a one-off (DC-D-104).
**PP negative/exit.** [`Xp`] **`BRANDED DISTRIBUTION WITH PUSH` and `CONSUMER APP STORE` are documented exits.** Push throttling limits are additionally an open unknown, so even the supported notification paths are unsized.

**Related criteria.** DC-D-015, DC-D-013, DC-D-009, DC-D-033.
**Related anti-patterns.** AP-D-003.
**Related alternatives.** ALT-005, ALT-009 (custom front end over platform services).
**Lineage.** `application-architecture.md` AA-38, AA-39, AA-40, AA-46, AP-28, U-E1, U-E5, §1 row 8, §2; `platform-suitability.md` PS-12, §2 rows 23–24.

---
#### DC-D-116 — Conversational and agentic interaction requirement

**Domain:** Users and experience · **Volatility:** VOLATILE VALUE (feature-state and commercial model) · **Confidence:** LOW

**Repair note (2026-09-03).** This criterion was **absent** from the first version of this file, and its absence was justified in §8.5 on *consumption economics* alone. That justification was too narrow: the canonical corpus carries substantive **governance, security, ALM and operations** evidence about agent surfaces which is neither economic nor covered by any other criterion. The criterion is added here on the **DC-D-113 pattern** — carried with its evidence base stated honestly, its unknowns preserved, and a blocking flag on the part the corpus cannot answer. It is **not** a fit assessment: no such assessment exists anywhere in the corpus, and this criterion does not invent one.

**Definition.** Whether the solution must expose a **conversational or agent-shaped** interaction surface — natural-language question-answering over organisational content, or an actor that completes tasks and calls services on a user's behalf — and, if so, how much autonomy that actor is required to have.

**Why it matters.** Four separate decision chains change, none of them reducible to the criteria that already exist:

1. **Governance scope changes.** Agents are first-class governed artefacts in the platform's own administration surface — the tenant inventory experience exists to *"view and govern all apps, flows, and **agents** created across your tenant"*, managed-environment sharing rules cover agents **with editor/viewer granularity**, and the recommended default-environment data policy is stated as *"prevent **agents**, apps, and flows from calling any service"*. So an agent requirement pulls the environment, sharing and connector-policy decisions forward exactly as an app requirement does.
2. **The connector-policy model does not fully cover it, and is documented as never intending to.** The advanced connector policy — the default-deny allowlist that is the strongest connector control available — states that *"**Virtual connectors**: ACP doesn't support virtual connectors and won't support them in the future"*, while Copilot Studio's virtual connectors are *"evolving into their own dedicated governance rules"*. A "default-deny connector posture" requirement is therefore **not met for the agent surface by the control that meets it elsewhere**.
3. **An authorization decision made at one plane can be bypassed at another.** *"Copilot Studio items using Microsoft Graph connectors **might access the information in these items even if you block guest access**."* This is a documented mechanism, not a hypothetical, and it is why an external-audience agent requirement is a security-review trigger rather than a UX preference (`anti-patterns.md` AP-D-068).
4. **The operational and resilience position is different from the rest of the platform.** Copilot Studio has **no maker monitoring page** (agent coverage in the admin Monitor experience is public preview), and — most sharply — *"Copilot Studio conversation runtime requests fail until Microsoft restores the service in the primary region"*: **agent runtime is explicitly not covered by self-service disaster recovery**. A criticality class that drove DC-D-100 to a cross-region objective does not get that objective on the agent surface.

**Discovery evidence.** Whether users are asking for "ask it a question" rather than "fill in this form"; whether the requirement is retrieval and summarisation over existing content, or task completion with side effects; what the actor would be permitted to *do* and *to whom*; whether the audience includes guests, partners or the public; whether an answer that is wrong is a nuisance, a cost or a regulatory event; whether an existing conversational estate already owns this channel; who would own the agent when its author leaves.

**States.** `NONE` (no conversational surface required) · `ASSISTED SEARCH AND SUMMARY` (retrieval and summarisation over existing content; no side effects) · `TASK-COMPLETING AGENT` (the actor performs bounded, user-initiated actions with side effects) · `AUTONOMOUS AGENT` (the actor initiates work without a user turn) · `UNKNOWN`.

**Decision impact.**

- `NONE` → no change; this criterion contributes nothing and should not be forced.
- `ASSISTED SEARCH AND SUMMARY` → the governance obligations of item 1 apply, the guest-access bypass of item 3 must be assessed against DC-D-009 and DC-D-058, and the consumption model of DC-D-095 becomes an **open** cost line rather than a priced one.
- `TASK-COMPLETING AGENT` → adds DC-D-052 (the actor's writes need an idempotency position), DC-D-068 (whose identity does the actor call downstream as), DC-D-060/DC-D-066 (what happens on revocation), DC-D-006 (who owns the agent), and the ALM conflict below.
- `AUTONOMOUS AGENT` → **the corpus cannot assess this at all.** `automation-architecture.md` U-14 records the gap in its own words: the corpus *"is silent on agent-based automation as an alternative or successor pattern"* and *"cannot answer 'should this be an agent instead of a flow?', which is an increasingly common stakeholder question"*, and records that **this deferral has no owner**. Proceeding on an autonomous-agent architecture from this corpus is a bet, not a decision.

Three further constraints apply at `TASK-COMPLETING AGENT` and above:

- **An ALM control conflict, documented.** *Block unmanaged customizations* — the control that protects production from ad-hoc change — *"breaks a documented list including journeys, SLAs and agent publishing"*. The corpus's own instruction is *"Either forgo that control or forgo those features — record the decision"*. This collides directly with DC-D-079 and DC-D-080 for any `BUSINESS-CRITICAL` or higher class.
- **A published request-bucket figure exists and is the only capacity fact in the corpus.** The Power Platform request meter lists *"250,000"* per 24 hours for *"Copilot Studio base and add-on"*, alongside the same page's official-versus-transition distinction. Size against the official limit, per `automation-architecture.md` AT2-03. **No throughput, latency, concurrency or accuracy figure exists for the agent surface** — the request bucket is a licensing meter, not a performance envelope.
- **Secrets are consumable by this surface.** Key Vault-backed environment variables are consumable by *"cloud flows, Copilot Studio agents and custom connectors only"*, which makes an agent one of the three components that can hold a secret-bearing integration — relevant to DC-D-065.

**Economics — `UNKNOWN`, and preserved as such.** The consumption meter is published (*"The Copilot Studio pay-as-you-go meter counts the total number of **Copilot Credits** consumed by agents"*, at $0.01 per credit) but the **unit is not modellable in advance**: *"The number of Copilot Credits decreased for each response or action is dependent on the complexity of the task completed by the agent"*, and the sibling AI meter states *"The amount of capacity consumed varies based on the AI model and the size and complexity of the data set"*. One bundled entitlement carries a dated removal (*"the 5,000 AI Builder credits will be removed on November 1, 2026"*). Enforcement is monthly and peak-based: *"Purchase capacity for the peak utilization monthly period."* The corpus's own instruction where a figure is needed is to establish consumption **empirically in a pilot**, not to estimate it.

**PP positive.** `NONE` — the criterion is inert, which is the common case and must not be treated as a gap. At `ASSISTED SEARCH AND SUMMARY` over content the platform already governs, no documented constraint is violated **provided** the audience is internal (DC-D-009) and the governance obligations of item 1 are funded.

**PP caution.** `ASSISTED SEARCH AND SUMMARY` with any external or guest audience — item 3's bypass must be assessed, not assumed away. `TASK-COMPLETING AGENT` at `BUSINESS-CRITICAL` or above — the ALM control conflict, the absent maker monitoring surface and the DR exclusion are three separate obligations, each with a named owner or the requirement changes. Any state above `NONE` where the budget is committed before a consumption pilot.

**PP negative/exit.** [`—`] **none evidenced — and the absence is the finding, not a verdict.** The corpus contains **no fit assessment of the agent surface**: `platform-suitability.md` and `application-architecture.md` carry **zero** mentions of it, so neither a positive nor a negative fit verdict can be derived. What *can* be produced, and must be, is a **block**: at `TASK-COMPLETING AGENT` and `AUTONOMOUS AGENT` the outcome is `DECISION BLOCKED — MORE EVIDENCE REQUIRED` on the commercial model (unmodellable consumption), on the governance model (agent-specific rules are *"evolving"*; `governance.md` GOV-U-06 records agent authentication and channel controls as **preview, not researched**) and — at `AUTONOMOUS AGENT` — on the modality question itself (`automation-architecture.md` U-14, an unowned deferral). This is the DC-D-113 treatment applied consistently: **evidence absent, so the criterion blocks rather than guesses.**

**Alternative-side signal.** `COMPARATOR EVIDENCE ABSENT` (§4A.1) — and here it is absolute rather than default. The corpus holds no assessment of conversational or agent capability in **any** class, including ALT-003, ALT-005, ALT-006, ALT-007 and ALT-011. No candidate set for this criterion can be evidence-ranked, and a pack must say so rather than produce one.

**Related criteria.** DC-D-009, DC-D-058, DC-D-060, DC-D-065, DC-D-066, DC-D-068, DC-D-006, DC-D-052, DC-D-072, DC-D-079, DC-D-080, DC-D-095, DC-D-100, DC-D-101, DC-D-115.
**Related anti-patterns.** AP-D-068, AP-D-033, AP-D-030, AP-D-057, AP-D-051, AP-D-062.
**Related alternatives.** ALT-003, ALT-004, ALT-007, ALT-011 — all `UNKNOWN` on this axis; see the alternative-side signal above.
**Lineage.** `governance.md` GOV-11b (G-13, G-17), GOV-16 (G-09), GOV-19 (G-12), GOV-03 (G-03), GOV-U-06; `security.md` SEC-04 (S-25), SEC-07/SEC-06 (S-28), SEC-24 (S-29), §9 (agent authentication/channels changed in the research window); `operations-support.md` OP-06 (O-08), OP-19 (O-19); `alm-devops.md` ALM-15, §4 row 15; `automation-architecture.md` AT2-03 (V-01, V-02), U-14, §12 (unowned deferral); `licensing-cost.md` LC-15 (L-03, L-04, L-05); `performance-scale.md` P-27. **`INF`** on the criterion's *framing* only — every fact above is MS-sourced; no fit verdict is synthesised from them.

**Research follow-up (required, and named as such).** `alternatives.md` §6 and this file's §9 record the consequence: the corpus needs an **agent/Copilot Studio research area** covering fit boundaries, governance scope, security posture (including the Graph-connector guest-access bypass), operational coverage and economics. Until it exists, this criterion blocks rather than decides, and that is the correct behaviour. It is **not** grounds for removing the criterion again.

---

### 4.3 Data

#### DC-D-021 — System of record per entity and field

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Which system holds authority for each entity — and, where authority is split, for each field and each lifecycle phase.

**Why it matters.** It is the criterion from which almost every data and integration decision follows: read-through versus copy, synchronisation direction, conflict rules, which system's controls and audit obligations apply, and who adjudicates when copies disagree. It must be established explicitly because **no vendor definition exists to borrow**: the implementation guidance uses *"primary data"* and *"master data source"*; the architecture guidance's only near-definition ties *"source of truth"* to a **consistency requirement** per entity (*"Other services might hold their own copy… not considered the source of truth"*); and authority is shown handing over between systems at a lifecycle boundary. The corpus's instruction is that a pack must *"declare its own vocabulary as pack-local, never cite Microsoft as the authority for a formal distinction"*.

**Discovery evidence.** An entity list with a named owning system and a named business owner per row; where each field is created and corrected today; whether authority changes at a lifecycle boundary; whether two teams already report different figures for the same thing.

**States.** `THIS SOLUTION` · `EXTERNAL SYSTEM` · `SPLIT BY FIELD` · `SPLIT BY LIFECYCLE PHASE` · `CONTESTED` · `UNKNOWN`.

**Decision impact.** `EXTERNAL SYSTEM` → read-through or a scoped one-way replica, never a bidirectional master (`anti-patterns.md` AP-D-010). `SPLIT BY FIELD` → a per-field ownership matrix is a precondition for any synchronisation. `SPLIT BY LIFECYCLE PHASE` → single-writer-per-phase with explicit authority handover, the corpus's preferred shape. `CONTESTED` or `UNKNOWN` → **decision-blocking**: integration and store decisions cannot be made, and the corpus lists `system_of_record_undecided` as a discovery signal for exactly this state.

**PP positive.** `THIS SOLUTION` — the platform's governed store as the master for new operational data.
**PP caution.** `SPLIT BY FIELD` — viable only with the matrix, conflict rules, reconciliation and the four named governance roles.
**PP negative/exit.** [`Ri`] none as a platform exit. **In-platform redirect:** bidirectional mastering is unavailable for critical data without the manifest **NB-01** failure/recovery test, and authoritative ledgers are excluded from bidirectional treatment by the vendor's own product design. The documented answer is read-through, a scoped one-way replica, or single-writer-per-phase with explicit authority handover (Decision impact) — not a platform change.

**Related criteria.** DC-D-029, DC-D-031, DC-D-036, DC-D-038, DC-D-052, DC-D-006.
**Related anti-patterns.** AP-D-014, AP-D-010, AP-D-011, AP-D-013, AP-D-027.
**Related alternatives.** ALT-001, ALT-007, ALT-009, ALT-011.
**Lineage.** `data-architecture.md` DQ-03, DQ-15, U-14, §2 row 13, §3 (last boundary), §6; `integration-architecture.md` IA-36, IA-37, §9 row 9, §13.2, I-26; `architecture-patterns.md` §3.1 (ownership row), matrix rows 16–22; `governance.md` GOV-XB-04; manifest NB-01.

---

#### DC-D-022 — Relational complexity

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The number and depth of relationships between entities, and whether referential integrity, cascades and multi-entity traversal are required.

**Why it matters.** It is the primary store discriminator, and the boundaries are documented per store. The document/list store carries a **12 lookup, person and metadata column ceiling** per view or retrieval, with integrity available only as opt-in delete behaviour; the governed relational store supports the full model with the broadest delegation table; a relational engine supports it natively but through a connector whose conformance must be checked. Traversal depth has a further, separate ceiling at the query layer: **at most two lookup levels (one when offline) and around twenty expanded entities** in a single query. A virtualized table can never be the "one" side of a one-to-many relationship. And relationships never cross environments — cross-environment **reads** are supported, but *"relationships, joins, cascades and security-role inheritance never cross environments"*.

**Discovery evidence.** An entity-relationship sketch; how many related entities appear on one screen; whether cascade delete or restrict-delete semantics are required; whether traversal depth exceeds two levels; whether a shared reference environment is proposed as a relational parent.

**States.** `FLAT` (no relationships) · `SIMPLE` (1–2 lookups) · `RELATIONAL` (several, with integrity) · `DEEP` (traversal beyond two levels) · `UNKNOWN`.

**Decision impact.** `FLAT` or `SIMPLE` opens the document/list store (ALT-003). `RELATIONAL` requires the governed store or a relational engine. `DEEP` forces server-side views, a flattened model, or a different surface — and is a **stricter, separate constraint offline**. A shared reference environment is viable only as a read source per artefact, never as a relational parent.

**PP positive.** `RELATIONAL` on the governed store — a documented **STRONG** verdict with the broadest delegation support.
**PP caution.** `DEEP`, and any relational model on the document/list store beyond two lookups.
**PP negative/exit.** [`Cf`] none from complexity alone; it combines with DC-D-023 and DC-D-088 to disqualify specific stores rather than the platform.

**Related criteria.** DC-D-023, DC-D-026, DC-D-088, DC-D-016, DC-D-021.
**Related anti-patterns.** AP-D-008, AP-D-012, AP-D-050.
**Related alternatives.** ALT-003, ALT-004, ALT-005.
**Lineage.** `data-architecture.md` DA-05, DA-06, DA-25 (revised), DA-30, DA-40, VT-17, C-16, §2 rows 1–2, §3; `performance-scale.md` PF-03, DC-02, §3.A row 3; `platform-suitability.md` PS-02, §2 row 2.

---

#### DC-D-023 — Queried volume per interactive access path

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** For each interactive screen or query, the number of records the query must consider — not the table's total size, but what one access path must reason over — projected to the investment horizon.

**Why it matters.** This is the corpus's most consequential correctness criterion, because exceeding it produces **wrong answers rather than errors**. Where an expression cannot be pushed to the source, only the first **500 (default) or 2,000 (maximum)** records are considered, and the result is presented as complete. Two indirection patterns produce **no warning at all**. Delegability is source-specific and the document/list store's table is the narrowest (`Not` never delegable; `IsBlank` unavailable on text and complex columns; identifier comparison only by equality). Aggregation has an independent ceiling (DC-D-031). The corpus supplies an explicit test: **set the data row limit to 1 and verify**.

**Discovery evidence.** Per screen: what the user filters, sorts, searches and counts, and over how many records at year three; whether free-text or negative-operator search is required; whether any access path uses a source not on the delegable list.

**States.** `BELOW CEILING` · `ABOVE CEILING, FULLY DELEGABLE` · `ABOVE CEILING, PARTIALLY DELEGABLE` · `ABOVE CEILING, NON-DELEGABLE` · `UNKNOWN`.

**Decision impact.** `ABOVE CEILING, NON-DELEGABLE` → the store must change, the expression set must be restricted to that store's delegable subset, or reads must be pre-shaped server-side. If none is possible, **the interactive surface is out of envelope** — a surface or store decision, not a tuning task. Access paths should also be **few and indexable**, which is a design constraint on the document/list store specifically.

**PP positive.** `BELOW CEILING`, or `ABOVE CEILING, FULLY DELEGABLE` against the governed store (broadest delegation).
**PP caution.** `PARTIALLY DELEGABLE`, and any growth trajectory approaching the ceiling with search or negative operators in scope.
**PP negative/exit.** [`Xr`] `NON-DELEGABLE` at volume with no server-side shaping option → the interactive read surface must move; at the extreme this becomes a custom-application trigger.

**Related criteria.** DC-D-022, DC-D-024, DC-D-088, DC-D-031, DC-D-084.
**Related anti-patterns.** AP-D-050, AP-D-008, AP-D-012.
**Related alternatives.** ALT-003, ALT-004, ALT-005, ALT-009.
**Lineage.** `performance-scale.md` PF-01, PF-02, PF-05, DC-01, B-01, §3.A rows 1–2, §8.1 items 1–2; `data-architecture.md` DA-02, DA-31, DA-39, DAP-22, C-09, §2 row 2, §3; `platform-suitability.md` PS-13, §2 row 6.

---

#### DC-D-024 — Total data volume and growth

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The total volume of data the solution will hold, and its growth rate, over the investment horizon.

**Why it matters.** The governed store has **no published technical size limit** — *"no technical limit on the size of a Dataverse environment"* — so the ceiling is a **purchased-entitlement ceiling**, not a technical one, which makes this a cost criterion before a capability one. Overage does not degrade the running application; it **blocks environment creation, copy, restore and recovery**, so capacity is a *recoverability* requirement. Note also what is **not** published: no standard-table row or size ceiling exists (only the high-volume table type carries a scale claim), so any quoted figure would be invention.

**Discovery evidence.** Current volume in the source; records added per period; growth rate and any seasonality; whether history is in scope; retention obligations; whether attachments are counted separately.

**States.** Anchored **relatively**, against the purchased entitlement and the redesign trigger — not against an invented absolute, because the corpus publishes no size ceiling for the governed store. `SMALL` (year-three volume well inside the entitlement already funded) · `MODERATE` (year-three volume inside the entitlement, with headroom that the growth rate does not consume within the horizon) · `LARGE` (year-three volume reaches the funded entitlement within the horizon, so a capacity purchase or a lifecycle job is on the critical path) · `VERY LARGE OR HIGH-GROWTH` (the growth rate reaches the **redesign trigger** — the point at which the store type itself changes — within the horizon) · `UNKNOWN`.

**Decision impact.** Size against **year-three volume and the peak**, not today's average. Model the three separately-metered capacity types, note that **no user entitlement accrues log capacity** while audit consumes it, and that cross-capacity borrowing is one-directional. Identify the **reachable limit and the redesign trigger before it is hit**. `VERY LARGE OR HIGH-GROWTH` with high ingest rates routes to a purpose-built store rather than either a relational engine or the governed store.

**PP positive.** `SMALL` to `LARGE` with a funded capacity model and a lifecycle job for binaries and history.
**PP caution.** `VERY LARGE OR HIGH-GROWTH` — the corpus has no published envelope for the governed store's standard tables, so this requires load and soak validation rather than a lookup.
**PP negative/exit.** [`Cf`] none from volume alone; combines with DC-D-031 and DC-D-040 for the analytical and ingest cases.

**Related criteria.** DC-D-025, DC-D-032, DC-D-087, DC-D-095, DC-D-031.
**Related anti-patterns.** AP-D-063, AP-D-051, AP-D-010.
**Related alternatives.** ALT-006, ALT-009, ALT-004.
**Lineage.** `performance-scale.md` PF-17, DC-20, §3.B row 11; `data-architecture.md` DA-14, DA-62, U-30, SQ2-06, §2 row 9; `licensing-cost.md` DC-04, LC-05, LC-10, LC-11, §7.2 items 11–16; `operations-support.md` OP-22, DC-17.

---

#### DC-D-025 — Attachment and binary volume

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The volume of files, images and documents the solution holds or moves, and whether they carry protection obligations that must travel with the file.

**Why it matters.** Binaries sit on a **different, much cheaper meter** than structured data, and the corpus records the ratio as material (file storage roughly an order of magnitude cheaper per unit than database storage) — so where binaries land is a cost architecture decision. Two capability facts then bite: the governed store's file columns have **no label mechanism**, so sensitivity labels that must travel with a downloaded file require the document store; and long-term retention gives **zero saving on files**. Movement has its own forgotten meter: **content throughput per 24 hours by owner profile**, which the corpus calls *"the forgotten meter in file-heavy designs"* and which spans a 50× range by profile — and it measures the **whole payload**, not just the file.

**Discovery evidence.** Files per period and average size; total binary volume at horizon; whether protection must travel with the file; whether large files move through automations; the owner profile of any automation that moves them.

**States.** Anchored **relatively**, against the content-throughput window and the payload ceilings named in `Decision impact` — the corpus publishes both, and neither becomes a state name (§2.3). `NONE` · `LOW` (bytes per window well inside the owner profile's content-throughput allowance) · `MODERATE` (inside the allowance, but the allowance is a design constraint rather than headroom) · `HIGH` (bytes per window reaches the owner profile's allowance, so the licence profile becomes a throughput decision) · `LARGE FILES` (individual files approach the per-payload ceiling, forcing chunking or a direct-to-storage pattern regardless of total volume) · `UNKNOWN`.

**Decision impact.** Put binaries in file storage or an external object store with a reference, not in the database meter. Where protection must travel with the file, the document store is required — accepting that a hybrid *"inherits two security models that do not synchronise"*. Size file movement **in bytes per window**, not in actions; `LARGE FILES` require chunking (where the mechanism supports it) or a direct-to-storage pattern.

**PP positive.** `LOW` to `MODERATE` with binaries on the file meter and a lifecycle job.
**PP caution.** `HIGH` or `LARGE FILES` with a low-profile automation owner — the content-throughput ceiling becomes the binding meter, and licence choice becomes a throughput decision.
**PP negative/exit.** [`Ri`] none evidenced. **In-platform redirect:** at `HIGH` or `LARGE FILES` the binaries leave the database meter for file storage or the document store with a reference — a store and pattern change, not a platform change. An external object store is a design option for the same redirect (Decision impact), not a documented exit.

**Related criteria.** DC-D-024, DC-D-043, DC-D-058, DC-D-095, DC-D-086.
**Related anti-patterns.** AP-D-063, AP-D-049, AP-D-066.
**Related alternatives.** ALT-003, ALT-006, ALT-009.
**Lineage.** `data-architecture.md` DA-14, DA-15, DA-17, DA-44, DA-59, DA-62, DAP-15, §2 rows 7–8; `performance-scale.md` PF-31, PF-35, DC-09, §3.C rows 16, 27; `licensing-cost.md` LC-05, LC-10, DC-04.

---

#### DC-D-026 — Access-granularity requirement

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The finest grain at which access must be controlled: whole dataset, by record, or by field.

**Why it matters.** It is a store discriminator with **irreversible** consequences. The governed store supports record scoping (by owner, team and organisational unit) and field-level security natively — but a table's **ownership type is immutable after creation**, so record-scoping must be decided per table *before build*. The document/list store has **no field-level security** and a recommended ceiling of around 5,000 unique permission scopes for record access. A relational engine can do both, but only with explicit per-user connections plus in-database rules — shared or implicit connections **collapse to one principal**, which the vendor's own reference architecture states plainly. Virtualized tables are **organisation-owned only** with **no field-level security**. And field-level security has documented exclusions that matter: it **never applies to the system administrator**, cannot secure lookups, formula, primary-name or system columns, and leaks through calculated and composite columns.

**Discovery evidence.** Which populations must not see which records, and which fields; whether administrators must be excluded; whether a re-organisation is expected; whether the scoping population exceeds a few thousand distinct scopes.

**States.** `DATASET` · `RECORD` · `FIELD` · `RECORD AND FIELD` · `ADMINISTRATOR-EXCLUDED` · `UNKNOWN`.

**Decision impact.** `RECORD` or `FIELD` requires the governed store or a relational engine with explicit identity — and disqualifies the document/list store and virtualized tables. Decide ownership type per table before the first table is created. `ADMINISTRATOR-EXCLUDED` is **not achievable** in the governed store: the attribute must live elsewhere, or the administrator population must be reduced to an auditable just-in-time set.

**PP positive.** `RECORD` and `FIELD` on the governed store — a documented **STRONG** verdict, subject to the field-security exclusions.
**PP caution.** Field-level security combined with offline (mutually exclusive), or with analytical replication (secured columns export as null unless the sync identity holds the profile). Also: authorization-heavy models have **no published performance curve** (manifest NB-04) and need a representative pilot.
**PP negative/exit.** [`Xr`] `ADMINISTRATOR-EXCLUDED` → the attribute leaves the governed store (ALT-001, ALT-005, ALT-007). Record- or field-level security **on data that must stay in an external system and be surfaced natively** → replication, not virtualization; if neither is acceptable, a custom surface.

**Related criteria.** DC-D-058, DC-D-062, DC-D-068, DC-D-016, DC-D-031, DC-D-021.
**Related anti-patterns.** AP-D-029, AP-D-030, AP-D-012, AP-D-008, AP-D-032.
**Related alternatives.** ALT-004, ALT-005, ALT-001, ALT-007.
**Lineage.** `data-architecture.md` DA-11, DA-12, DA-33, DA-42, DAP-10, DAP-11, DAP-12, DAP-38, SQ2-08, SQ2-15, §2 row 5, §3; `security.md` SEC-08, SEC-09, SEC-13, §4 rows 1–6; `architecture-patterns.md` matrix rows 17–18; `performance-scale.md` PF-U-07; manifest NB-04.

---

#### DC-D-027 — Audit and evidence-retention requirement

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether a provable record of who changed or saw what is required, over what period, and for what purpose.

**Why it matters.** Audit is **a capacity and licensing decision before it is a configuration one**: the governed store's audit consumes **log capacity that no user entitlement provides**, retention is **stamped at write time and non-retroactive**, the default is unbounded, and audit is **excluded from restore by default** and materially slows it when included. Audit also does **not** cover retrieve or export unless separate, licence-gated activity logging is enabled. Two related boundaries: the compliance log has roughly 24-hour latency (*"Don't use this information for real-time monitoring"*), and native automation run history — the only transactional record — expires at 30 days. The corpus's conclusion for anything beyond that: evidence must be written to a **business record as part of the process**, which is a functional requirement on the design.

**Discovery evidence.** The regulator's or contract's actual wording; retention period; whether read access must be evidenced, not just changes; whether an auditor has agreed the evidence format and cadence; how far back a reconstruction must reach.

**States.** `NONE` · `CHANGE HISTORY` · `CHANGE AND ACCESS HISTORY` · `PROVABLE COMPLIANCE EVIDENCE` · `UNKNOWN`.

**Decision impact.** Fix audit scope, retention and its capacity budget **at environment and table creation**. Separate audit from diagnostics — they are different stores with different retention and different budgets. Beyond 30 days of process evidence, design it into business records. Note the conflict to resolve explicitly: **audit completeness and fast recovery are in tension**, because audit data slows restore materially.

**PP positive.** `CHANGE HISTORY` on the governed store with a scoped, funded retention decision.
**PP caution.** `CHANGE AND ACCESS HISTORY` (needs the licence-gated activity log) and `PROVABLE COMPLIANCE EVIDENCE` (needs a separate store, a separate retention, a separate budget, and an auditor-agreed format). Also: audit is **not available with customer-managed keys** — a documented interaction between two compliance controls.
**PP negative/exit.** [`Cf`] none from audit alone; the exit arises where administrator-excluded confidentiality is also required (DC-D-062).

**Related criteria.** DC-D-026, DC-D-032, DC-D-058, DC-D-059, DC-D-064, DC-D-095, DC-D-103.
**Related anti-patterns.** AP-D-063, AP-D-054, AP-D-008.
**Related alternatives.** ALT-004, ALT-001, ALT-007.
**Lineage.** `data-architecture.md` DA-16, DA-17, DAP-13, §2 row 6, §3; `operations-support.md` DC-03, DC-04, OP-03, OP-09, OP-10; `licensing-cost.md` LC-05, LC-11, LC-AP-05, DC-04; `security.md` SEC-34, §4 row 16.

---

#### DC-D-028 — Transactional atomicity span

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The set of writes that must succeed or fail together, and how many stores and systems that set spans.

**Why it matters.** It is one of the corpus's hardest boundaries. **Atomicity exists only inside the governed store**, via a change set (bounded in size, unable to contain a loop, unable to chain outputs) or synchronous server-side code (with a two-minute ceiling); a relational engine offers it via a stored procedure. **Across connectors or systems there is no atomicity and no coordinator anywhere in the corpus.** The low-code expression language is *never* transactional, even within one store. The document/list store has none at all — last writer wins. And the synchronous outbound-callback variant is a documented dual-write hazard: *"the data operation rolls back but the request sent to the configured endpoint can't be recalled."*

**Discovery evidence.** Which writes must be all-or-nothing, and to which systems; what the business does today when one half succeeds; whether a compensation window is acceptable and how long; whether temporary inconsistency is tolerable at all.

**States.** `SINGLE WRITE` · `MULTI-WRITE, ONE STORE` · `MULTI-STORE` · `MULTI-SYSTEM` · `UNKNOWN`.

**Decision impact.** `MULTI-WRITE, ONE STORE` → change set or server-side code, within their limits. `MULTI-STORE` or `MULTI-SYSTEM` → either **collapse the unit of work into one system's transaction** (the corpus's preferred shape: compose in one place, lock, hand authority over) or move the orchestration to a host with durable state and compensation. Where temporary inconsistency is **intolerable**, the instruction is *"Use strong consistency mechanisms or atomic transactions across all steps instead"* — which no pattern here supplies across systems.

**PP positive.** `SINGLE WRITE` and `MULTI-WRITE, ONE STORE` on the governed store.
**PP caution.** `MULTI-STORE` with an accepted compensation window — viable as a saga with per-step idempotency keys, durable in-doubt state, irreversible steps last, and a human resolution path.
**PP negative/exit.** [`Xr`] **`MULTI-SYSTEM` with no acceptable compensation window is a documented exit** — and, in combination with more than one transactional owner, one of the corpus's composed disqualifiers: *"No pattern here supplies the required atomicity; collapse to one owner or move the transaction responsibility elsewhere."*

**Related criteria.** DC-D-029, DC-D-052, DC-D-054, DC-D-021, DC-D-036.
**Related anti-patterns.** AP-D-018, AP-D-017, AP-D-059, AP-D-003.
**Related alternatives.** ALT-005, ALT-006, ALT-007, ALT-009.
**Lineage.** `data-architecture.md` DA-07, DA-08, DA-50, DA-52, DAP-7, DAP-8, §2 row 3, §3, §6; `platform-suitability.md` PS-45, PS-57, §2 row 28, §3; `integration-architecture.md` IA-19, IA-20, IA-21, §2.1 rows 7–8, §12.3; `automation-architecture.md` AT2-17, AT2-19, AT2-21, §3.A row 4, §4.2; `architecture-patterns.md` matrix row 20, §13.

---

#### DC-D-029 — Consistency class and convergence window

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether all copies of the data must agree at all times, or whether convergence within a stated window is acceptable — and what that window is.

**Why it matters.** It is the criterion that makes the atomicity question answerable, and the corpus anchors it to the only near-definition of authority it found: *"Use a single source of truth when you require strong consistency."* Where convergence is acceptable, replication and eventing become available and the architecture simplifies dramatically; where it is not, the option set shrinks to single-owner designs or a coordinator outside the platform. Two open items constrain confidence: whether the governed store guarantees read-after-write **across sessions** is `UNKNOWN`, and whether it serves any replicated reads is `UNKNOWN` — the corpus explicitly refuses to assert either way.

**Discovery evidence.** What the business does if two systems disagree for an hour; whether any decision or payment depends on both agreeing; the acceptable convergence window in minutes or hours; whether a reader ever needs to see their own write from a different process.

**States.** `EVENTUAL, WIDE WINDOW` · `EVENTUAL, TIGHT WINDOW` · `READ-YOUR-WRITES` · `STRICT` · `UNKNOWN`.

**Decision impact.** `EVENTUAL` → replication, events and reconciliation are available; the window sets the mechanism (see DC-D-051). `READ-YOUR-WRITES` across processes → do **not** design on an assumption the corpus cannot confirm; test it. `STRICT` across systems → single transactional owner, or a coordinator outside the platform, or the requirement changes.

**PP positive.** `EVENTUAL` in either width, with a designed reconciliation pass.
**PP caution.** `READ-YOUR-WRITES` across sessions or processes — an open unknown to close by test, not by inference.
**PP negative/exit.** [`Xr`] `STRICT` across two or more systems → out of the platform for the coordination responsibility (ALT-005, ALT-006, ALT-007). The corpus also flags that no cloud transit at all, or distributed multi-primary writes, moves the whole store decision elsewhere.

**Related criteria.** DC-D-028, DC-D-021, DC-D-041, DC-D-051, DC-D-030.
**Related anti-patterns.** AP-D-011, AP-D-013, AP-D-018.
**Related alternatives.** ALT-005, ALT-006, ALT-007, ALT-009.
**Lineage.** `data-architecture.md` DQ-15, SC-06, U-27, U-28, §6 (last bullet); `integration-architecture.md` §2.1 rows 6–7, §9 rows 10–12, IA-38; `architecture-patterns.md` §3.1 (consistency row).

---

#### DC-D-030 — Concurrent-edit contention

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether several people will edit the same record at the same time, and what the business expects to happen when they do.

**Why it matters.** Behaviour differs by store and is partly undocumented. The governed store supports optimistic concurrency, but **through code or the API** — with a conflict error surfaced in the task-focused client rather than a managed merge. For a relational engine through a connector the semantics are **`UNKNOWN`** (isolation level, transaction scope of the write operations, deadlock retry). The document/list store has **no conflict setting at all** — version history is a recovery mechanism, not concurrency control — and the corpus's evidence there is `T4`. The spreadsheet store is explicit: *"Simultaneous file modifications … are not supported"*, with a six-minute lock and duplicate inserts on retry.

**Discovery evidence.** Whether two people work the same record today, and what happens; whether a lost update would be noticed; whether the business expects locking, merging, or last-writer-wins; volume of concurrent editing.

**States.** `NONE` · `RARE` · `ROUTINE` · `HIGH WITH BUSINESS CONSEQUENCE` · `UNKNOWN`.

**Decision impact.** `ROUTINE` or `HIGH` disqualifies the spreadsheet and document/list stores as the system of record, and requires an explicit concurrency design on the governed store (code or API-level optimistic concurrency, plus a defined user experience for the conflict). Where a relational engine is chosen, the semantics must be **tested**, not assumed.

**PP positive.** `NONE` or `RARE` on any store; `ROUTINE` on the governed store with a designed conflict experience.
**PP caution.** `ROUTINE` on a relational engine through a connector — undocumented semantics, closed only by test.
**PP negative/exit.** [`Ri`] none evidenced. **In-platform redirect:** `ROUTINE` or `HIGH` disqualifies the spreadsheet and the document/list store as the system of record and requires an explicit concurrency design on the governed store — a store change, not a platform change.

**Related criteria.** DC-D-029, DC-D-028, DC-D-016, DC-D-085.
**Related anti-patterns.** AP-D-008, AP-D-017.
**Related alternatives.** ALT-003, ALT-004, ALT-005.
**Lineage.** `data-architecture.md` DA-08, DA-41, U-04, U-05, C-14, §2 row 4; `platform-suitability.md` PS-46, U-13, §2 row 33.

---

#### DC-D-031 — Analytical versus operational workload separation

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the solution must serve aggregation, trend, cross-period or cross-entity analytical queries in addition to transactional work — and whether analytical results must respect per-user record security.

**Why it matters.** The governed store is a transactional store with a **documented aggregate ceiling** (the corpus's figure is around 50,000 records for aggregate operations, with query timeouts at five minutes, or two for broad selects and joins on the read endpoint) — and Microsoft's instruction is *"use a dedicated datastore for reporting purposes instead"*. Importantly, the boundary is **aggregation, charts and cross-period history**, not report size: ordinary filtered reports *"are allowed to span large datasets that are beyond 50,000 rows"* within the timeout. Reporting also **consumes the same per-identity budget as transactional work**, so the symptom appears in the application. And **security does not travel to the copy**: record security must be rebuilt, secured columns export as null unless the sync identity holds the profile, and embedded report visuals *"don't affect the data that is displayed"* by application roles.

**Discovery evidence.** The actual reports and dashboards required; whether they aggregate, trend or span periods; the row counts involved; whether reporting must respect per-user record visibility; who the report audience is.

**States.** `OPERATIONAL ONLY` · `FILTERED OPERATIONAL REPORTS` · `AGGREGATION AND TRENDS` · `ENTERPRISE ANALYTICS` · `ANALYTICS WITH PER-USER SECURITY` · `UNKNOWN`.

**Decision impact.** `AGGREGATION AND TRENDS` or above → an analytical copy **from day one**, with its own storage budget (billed on the platform's database meter, *"can double or triple your storage footprint"*, with **no published ratio**), its own security rebuild, its own freshness ceiling (plan for ≤ 1 hour; *"near real-time"* is undefined), and its own resilience gap (analytical replication is **not covered** by regional failover). `ANALYTICS WITH PER-USER SECURITY` → the per-user-secured direct-query path is the one case where keeping reporting on the operational store is *correct*, because security travels — subject to its own limits.

**PP positive.** `OPERATIONAL ONLY`, `FILTERED OPERATIONAL REPORTS`, and `ANALYTICS WITH PER-USER SECURITY` via the secured direct-query path.
**PP caution.** `AGGREGATION AND TRENDS` — the copy is required, budgeted and secured, and the drift modes of DC-D-013's related anti-pattern apply.
**PP negative/exit.** [`Xr`] `ENTERPRISE ANALYTICS` as the primary requirement → a data platform owns it and the operational store feeds it (ALT-006, ALT-007). High-ingest timestamped events route to a purpose-built engine, **not** a relational store.

**Related criteria.** DC-D-024, DC-D-023, DC-D-026, DC-D-018, DC-D-086, DC-D-095.
**Related anti-patterns.** AP-D-009, AP-D-013, AP-D-010, AP-D-049.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `data-architecture.md` DA-03 (revised), DA-19, DA-20, DA-21, DA-22, DA-51, DAP-3, DAP-16, DAP-17, SY-02, SY-14, C-06, C-11, U-01, SQ2-06, §2 rows 10–11, §3; `performance-scale.md` PF-46, DC-19, B-12; `operations-support.md` OP-19; `integration-architecture.md` §8, §12.8.

---

#### DC-D-032 — Retention and archival requirement

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How long data must be kept, whether it must remain queryable, and whether it must be deletable on request.

**Why it matters.** Several documented facts make this a design-time decision. **Backups are not an archive**: bounded to 7 days (28 only for a production managed environment), same-region and not downloadable — *"not a retention mechanism"*. Long-term retention on the governed store requires a managed environment, is **irreversible**, saves roughly half on database and **nothing on files**. Audit retention is **stamped at write time and non-retroactive**. On a relational engine, long-term retention is **backup retention restorable only as a new database, not a queryable archive**, and **no cold or cheap storage tier exists** for its rows — cheapness requires partitioning and archival compression (slower reads, more processing) or export elsewhere. Deletability has its own trap: append-only lake modes **do not propagate deletes**.

**Discovery evidence.** The retention obligation and its source; whether retained data must be queryable or merely producible; erasure obligations; whether the retained volume is material to cost; whether attachments are in scope.

**States.** `SHORT` · `MULTI-YEAR, QUERYABLE` · `MULTI-YEAR, PRODUCIBLE ONLY` · `INDEFINITE` · `WITH ERASURE OBLIGATION` · `UNKNOWN`.

**Decision impact.** Decide retention **and** audit scope at environment and table creation. `MULTI-YEAR, QUERYABLE` at volume → an archival store, not backups and not long-term retention alone. `WITH ERASURE OBLIGATION` → verify propagation through every copy, including lake and analytical paths. Note the direct tension with recovery: audit completeness slows restore materially.

**PP positive.** `SHORT` and `MULTI-YEAR, PRODUCIBLE ONLY` with a designed archival path.
**PP caution.** `MULTI-YEAR, QUERYABLE` — long-term retention's read-access limits and storage rate are an open unknown in the corpus.
**PP negative/exit.** [`Xr`] `MULTI-YEAR, QUERYABLE` at volume → the **archival responsibility leaves the platform** to a lake or archive store (ALT-006, ALT-009). In-platform long-term retention is `CONDITIONAL` only — managed environment, irreversible, no capacity saving for files, and retained data no longer surfaced to the analytical shortcuts — and backups are not a retention mechanism (`data-architecture.md` §2 row 12, DA-17, DA-18). The active record stays in-platform, which is why this is `Xr` and not `Xp`.

**Related criteria.** DC-D-024, DC-D-027, DC-D-095, DC-D-103, DC-D-033, DC-D-075.
**Related anti-patterns.** AP-D-054, AP-D-063, AP-D-067.
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `data-architecture.md` DA-16, DA-17, DA-18, DA-60, DAP-13, DAP-14, DAP-15, DAP-29, SQ2-04, SQ2-05, SQ2-14, U-16, U-21, §2 row 12, §3; `operations-support.md` DC-03, DC-04, DC-05, OP-14; `licensing-cost.md` LC-U-07.

---

#### DC-D-033 — Data residency and sovereignty

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Where data must physically reside and be processed, and whether a sovereign or regulated cloud regime applies.

**Why it matters.** Residency is decided **at environment creation and cannot be changed** — environments are bound to a geography — so multi-region means multi-environment. A macro-region boundary requires the tenant and **all** environments to sit in the correct macro region plus a matching billing address; country-level residency requires an additional add-on across all productivity seats. Three facts commonly surprise: **table and column names, application names and site URLs replicate globally**, so sensitive semantics must not live in names; **preview features default to a particular region**, which matters for regulated production; and **exact datacentre disclosure is not available**. Sovereign clouds carry eligibility requirements and **parity exceptions**, and several capabilities are unavailable in some of them (branded wrapping, telemetry export, machine groups, and private networking in one tier). Residency also collides with resilience: **some geographies have no regional pair at all**.

**Discovery evidence.** The regulation or contract clause verbatim; whether country-level or macro-region residency is required; whether a sovereign cloud applies; whether the tenant already satisfies the boundary; whether any datacentre-level disclosure is demanded.

**States.** `NO CONSTRAINT` · `MACRO-REGION` · `COUNTRY-LEVEL` · `SOVEREIGN / REGULATED CLOUD` · `IN-COUNTRY ON-PREMISES` · `UNKNOWN`.

**Decision impact.** Decide the region per environment **at creation**. `COUNTRY-LEVEL` requires the add-on across all seats — a population-priced cost. `SOVEREIGN` requires an eligibility and parity check per capability in the design. `IN-COUNTRY ON-PREMISES` interacts with DC-D-108. Where the geography has no pair, the **residency-versus-resilience trade-off must be surfaced**, not resolved silently.

**PP positive.** `NO CONSTRAINT` and `MACRO-REGION` where the tenant already satisfies it.
**PP caution.** `SOVEREIGN` — parity exceptions must be enumerated against the design, not assumed. `COUNTRY-LEVEL` — the add-on's population cost.
**PP negative/exit.** [`Xp`] Data that must **not transit the vendor's cloud at all** → out of the platform (its transit remains cloud even where the store is on-premises). `IN-COUNTRY ON-PREMISES` deployment → see DC-D-108.
**Blocking.** `UNKNOWN` is decision-blocking: the environment cannot be created without it, and the decision is irreversible.

**Related criteria.** DC-D-059, DC-D-108, DC-D-063, DC-D-090, DC-D-100, DC-D-115.
**Related anti-patterns.** AP-D-035, AP-D-057, AP-D-054.
**Related alternatives.** ALT-005, ALT-007, ALT-008.
**Lineage.** `data-architecture.md` DA-57, DA-58, DAP-27, §2 rows 18–20, §3; `platform-suitability.md` PS-17, PS-47, §2 rows 29–30, 36, §3; `security.md` SEC-15, SEC-29, SEC-30, §4 row 20; `integration-architecture.md` IA-29, §7 items 18–21, U-20; `performance-scale.md` PF-41, §8.1 item 31; `operations-support.md` §6.3.

---

#### DC-D-034 — Migration scope

**Domain:** Data · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** What existing data must be brought into the new solution: master data, open transactions, closed history, attachments — and what must be reconciled after.

**Why it matters.** Migration is a documented cost line that licence-based cases omit, and its scope drives capacity, throughput and validation. The corpus records the enumerated migration categories as **master data and open transactions**; note carefully that it also records (`data-architecture.md` U-41) that **Microsoft does not state "don't migrate history" as a rule**, so the boundary is an inference from those categories and must not be attributed to the vendor as a prohibition. Bulk loading into the governed store is bounded by per-identity service-protection windows and the platform's direction is *"move towards real-time integration"*; loading into a relational engine through the standard connector **cannot bulk-load at all** (a small operation ceiling per short window and a request timeout), implying a separate extract-and-load toolchain.

**Discovery evidence.** Volume by category; data quality in the source; whether history is genuinely needed or merely available; attachment volume; whether a reconciliation sign-off is required; who owns the source extract.

**States.** `NONE` · `MASTER DATA ONLY` · `MASTER PLUS OPEN TRANSACTIONS` · `INCLUDING HISTORY` · `UNKNOWN`.

**Decision impact.** `INCLUDING HISTORY` → challenge it against the capacity cost and the analytical alternative (history in the analytical store rather than the operational one); if genuinely required, it is a separate toolchain and a separate budget line. Any migration needs a reconciliation step with a named owner and an acceptance criterion, and a **measured** write-amplification figure rather than an assumed one (`anti-patterns.md` AP-D-051).

**PP positive.** `NONE` to `MASTER PLUS OPEN TRANSACTIONS` with a bulk mechanism and a delta strategy.
**PP caution.** `INCLUDING HISTORY` — capacity, throughput and cost; and the "don't migrate history" boundary is `INF`, not vendor-stated.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-024, DC-D-031, DC-D-040, DC-D-098, DC-D-086.
**Related anti-patterns.** AP-D-010, AP-D-016, AP-D-051, AP-D-063.
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `data-architecture.md` DA-10, DA-51, DA-54, DAP-4, DAP-6, U-41, SQ2-07, SQ2-12, SQ2-13, §2 row 17, §3; `licensing-cost.md` LC-21; `platform-suitability.md` PS-25.

---
### 4.4 Integration

#### DC-D-035 — Number of integration streams and systems

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How many distinct data or event flows exist, counted **per stream** rather than per system pair, and how many systems participate.

**Why it matters.** Stream count is the input to the topology decision, and the counting unit matters: the corpus's worked example decomposes one integration goal into four streams and treats them **differently**, and its rule is *"Decide per stream; per-stream heterogeneity is expected"*. Deciding once per system pair means every stream inherits either the worst constraints or the weakest guarantees of a single mechanism. Stream count also drives the estate-level failure the corpus names bluntly — *"spaghetti architecture"* — via unmanaged point-to-point growth.

**Discovery evidence.** A stream inventory: for each, the source, the target, the initiator, the payload, the trigger and the business purpose. The corpus lists `integration_stream_inventory_incomplete` as a discovery signal in its own right.

**States.** `NONE` · `ONE STREAM` · `2–5 STREAMS` · `MANY STREAMS, FEW SYSTEMS` · `MANY STREAMS, MANY SYSTEMS` · `UNKNOWN`.

**Decision impact.** Produce the inventory before choosing any mechanism. `MANY STREAMS, MANY SYSTEMS` combined with several makers and a governance requirement is the strongest condition for an enclosing boundary. A single stream with one consumer is the condition under which the simplest mechanism is not merely acceptable but preferred — which the corpus says *"is the correct answer far more often than architects trained on enterprise integration expect"*.

**PP positive.** `ONE STREAM` to `2–5 STREAMS` with stable contracts inside the throttles.
**PP caution.** `MANY STREAMS, MANY SYSTEMS` without a topology decision — this is how the estate-level anti-pattern forms.
**PP negative/exit.** [`Cf`] none from count alone; it combines with DC-D-036 and DC-D-047.

**Related criteria.** DC-D-036, DC-D-047, DC-D-046, DC-D-038, DC-D-070.
**Related anti-patterns.** AP-D-022, AP-D-028, AP-D-027.
**Related alternatives.** ALT-007, ALT-006, ALT-009.
**Lineage.** `integration-architecture.md` I-01, I-02, X-01, X-02, §2.2 step 6, §9 row 1, §13.2; `architecture-patterns.md` Y-14, matrix rows 1–2, 30.

---

#### DC-D-036 — Integration ownership

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Who owns the data, who owns the endpoint, who owns the pipeline, and who is paged when it breaks at three in the morning.

**Why it matters.** The corpus makes this **step 1** of its classification test and is explicit about why: *"Nothing in the fetched Microsoft material tells an architect to check this, which is precisely why it must be step 1."* Where an enterprise integration capability already exists with a published contract, the correct answer is to consume it — and building around it produces both the point-to-point estate and duplicated contract management. `governance.md` frames it as *a governance decision before a product decision*. Ownership also has a mechanical consequence: pipeline throughput and retry behaviour are properties of the **owner's licence**, and a departure reverts the profile.

**Discovery evidence.** Whether an integration platform, service bus or gateway exists; whether the target system is already integrated with it; who publishes and versions the contract; who is on call for the path; whether the platform-owning team has been consulted.

**States.** `NO EXISTING CAPABILITY` · `CAPABILITY EXISTS, CONTRACT PUBLISHED` · `CAPABILITY EXISTS, NO CONTRACT` · `OWNERSHIP CONTESTED` · `UNKNOWN`.

**Decision impact.** `CAPABILITY EXISTS, CONTRACT PUBLISHED` → consume the contract; the platform integrates nothing, and the transformation, contract and audit trail stay with the owner. `CAPABILITY EXISTS, NO CONTRACT` → negotiate the contract or record why the incumbent cannot meet the requirement, **per requirement**. `OWNERSHIP CONTESTED` or `UNKNOWN` → **decision-blocking**, because the topology cannot be chosen.

**PP positive.** `NO EXISTING CAPABILITY` with bounded streams the platform can serve directly.
**PP caution.** `CAPABILITY EXISTS, NO CONTRACT` — the temptation to go direct is exactly the documented failure.
**PP negative/exit.** [`Xr`] `CAPABILITY EXISTS, CONTRACT PUBLISHED` → the platform is **not** the integration layer for that stream (ALT-007). Note manifest **NB-06**: the enclosing-boundary pattern is `INF`, not vendor-endorsed, so the *reasoning* is sound and the *pattern name* is the corpus's own.

**Related criteria.** DC-D-035, DC-D-046, DC-D-047, DC-D-073, DC-D-111, DC-D-021.
**Related anti-patterns.** AP-D-027, AP-D-022, AP-D-025, AP-D-026.
**Related alternatives.** ALT-007, ALT-006, ALT-009.
**Lineage.** `integration-architecture.md` §12.1, §2.1 row 11, §2.2 step 1, §9 rows 20, 23, IA-16, IA-17; `governance.md` GOV-XB-02; `automation-architecture.md` AT2-52, §3.B row 19; `architecture-patterns.md` §3.1 (last variable), AP-10, matrix row 29; manifest NB-06.

---

#### DC-D-037 — Frequency distribution and peak shape

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How the volume arrives over time — the peak per minute and any seasonality — as distinct from the total per period.

**Why it matters.** The corpus treats this as a first-class dimension separate from volume, with a worked illustration: *"Two integration scenarios might involve the same total volume, such as 60,000 records per hour and 1,000 records per minute, but differ in frequency… the minute-by-minute expectation changes the solution design. Don't assume one solution fits both."* The mechanism limits that bind are **per-window rates per connection**, not daily totals, so a design sized on a daily average will throttle at peak. Spiky arrival is also the specific condition the corpus names for introducing a broker, and its escalation example runs in exactly that order.

**Discovery evidence.** Records or messages per minute at peak, not per day; when peaks occur and why; month-end, seasonal and campaign effects; whether arrival is externally driven.

**States.** `STEADY` · `PREDICTABLE PEAKS` · `SPIKY / BURSTY` · `EVENT-DRIVEN UNPREDICTABLE` · `UNKNOWN`.

**Decision impact.** Size every mechanism at the **peak per window**, per connection. `SPIKY` or `EVENT-DRIVEN UNPREDICTABLE` → queue-based load levelling with **bounded** consumers (autoscaling without bounding *"only moves the overload to downstream dependencies"*). `PREDICTABLE PEAKS` may be answerable by scheduling rather than architecture. `UNKNOWN` is **decision-blocking** for any mechanism selection.

**PP positive.** `STEADY` or `PREDICTABLE PEAKS` inside the per-window ceilings.
**PP caution.** `SPIKY` — the failure mode is 429 responses, retries piling up, and eventual automatic disablement.
**PP negative/exit.** [`Xc`] none from frequency alone; combines with DC-D-039 and DC-D-040.
**Blocking.** `UNKNOWN` is decision-blocking: without a peak figure, no mechanism can be sized and the *"scale anxiety without a number"* failure follows.

**Related criteria.** DC-D-039, DC-D-040, DC-D-087, DC-D-041, DC-D-051.
**Related anti-patterns.** AP-D-049, AP-D-016, AP-D-005 (buying a rung without the number).
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `integration-architecture.md` I-01, I-02, IA-02, IA-03, IA-11, §2.1 row 2, §9 row 2, §4.3, X-15; `performance-scale.md` §2, DC-20; `automation-architecture.md` §4.2, §9 row 3.

---

#### DC-D-038 — Directionality per stream

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** For each stream, which side originates the exchange and which receives — and whether either side is prevented from initiating.

**Why it matters.** Directionality decides the mechanism before throughput does, because some sides **cannot** initiate. The corpus's own framing: *"Legacy on-premises systems might restrict inbound connections. In such cases, design the integration so the legacy system initiates communication with the cloud application."* On the platform side the constraint is symmetrical and documented: the gateway is **outbound-only**, private networking is **outbound-only** (whether inbound private connectivity exists at all is an open unknown), so an enterprise system that must initiate needs an inbound endpoint and an application identity. Where **neither** side may initiate, a broker in the middle is the only shape.

**Discovery evidence.** Per stream: which system detects the business event; whether the source can call out; whether the target accepts inbound calls; firewall and network policy on both sides; whether the enterprise system has a scheduler.

**States.** `PLATFORM INITIATES` · `EXTERNAL SYSTEM INITIATES` · `BIDIRECTIONAL` · `NEITHER MAY INITIATE` · `UNKNOWN`.

**Decision impact.** `EXTERNAL SYSTEM INITIATES` → an inbound endpoint plus an application identity; note that the private-networking path does not cover inbound. `NEITHER MAY INITIATE` → a broker both sides reach outbound. `BIDIRECTIONAL` on the same entity escalates to DC-D-021's ownership matrix and the manifest **NB-01** test.

**PP positive.** `PLATFORM INITIATES` over a reachable endpoint.
**PP caution.** `EXTERNAL SYSTEM INITIATES` combined with a private-network requirement — the inbound private path is unestablished in the corpus.
**PP negative/exit.** [`Cf`] none from directionality alone; it selects mechanisms and combines with DC-D-044.

**Related criteria.** DC-D-044, DC-D-041, DC-D-021, DC-D-036, DC-D-045.
**Related anti-patterns.** AP-D-011, AP-D-035.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `integration-architecture.md` I-01, IA-04, IA-05, §2.1 row 3, §9 row 5, §4.3, U-09; `architecture-patterns.md` §3.1 (directionality row), matrix rows 7, 23–25.

---

#### DC-D-039 — Per-mechanism throughput ceiling

**Domain:** Integration · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** MEDIUM

**Definition.** The documented rate ceiling of each specific mechanism on the path, evaluated **per connection** at the peak window — for every mechanism on the path, not just the first.

**Why it matters.** This is where the platform most often fails at a fraction of assumed capacity, because the ceilings are per-mechanism, per-connection and per-short-window, and the corpus states that connector limits are *"often reached before"* platform limits. The published ceilings differ by an order of magnitude between mechanisms — one identity-protected mechanism carries **the tightest throttle in the platform** (100 calls per 60 seconds per connection) and additionally base64-encodes the body and does not support raw binary *"by design"*.

**The open conflict.** The **custom-connector** ceiling is `CONFLICTED` by a factor of **20×** and manifest **NB-02 / `IA-C-01`** requires that neither figure be encoded. Re-verified on 2026-09-03 (`anti-patterns.md` §6 V-D-02/V-D-03): the limits page states *"500 requests per minute per connection"* (page dated 2026-07-17, updated 2026-07-18) while the connector FAQ states *"10000 requests for each connection created by the connector"* for this platform (dated 2025-03-13, updated 2025-09-10). **The conflict is live in currently-maintained pages**, so it must be re-checked per engagement rather than treated as closed. A documented escalation path exists — adjustments are handled *"on a case-by-case basis"* with justification — which is a legitimate mitigation to propose and not something to rely on in advance.

**Discovery evidence.** Which mechanisms are on each stream's path; the calls per window each must sustain at peak; how many artefacts share one connection (throttle quota is per connection, and sharing is itself only `T3`-corroborated in the corpus); whether binary payloads are involved.

**States.** `WELL INSIDE` · `APPROACHING` · `EXCEEDS` · `CONFLICTED SOURCE` · `UNKNOWN`.

**Decision impact.** Compute per mechanism, per connection, at peak. `APPROACHING` or `EXCEEDS` → partition across connections or identities (which multiplies identity management), move the metered leg to a service-protection-exempt in-platform mechanism, introduce a broker, or move the responsibility out. `CONFLICTED SOURCE` → **decision-blocking**: a design sized on the higher figure *"fails by a factor of twenty"* if the lower is enforced.

**PP positive.** `WELL INSIDE` on standard mechanisms with headroom at the horizon.
**PP caution.** Any dependence on the identity-protected mechanism at volume, or on binary payloads through it.
**PP negative/exit.** [`Xr`] `EXCEEDS` with no partitioning available → the integration responsibility leaves the platform (ALT-006, ALT-007, ALT-009).
**Blocking.** `CONFLICTED SOURCE` and `UNKNOWN` are decision-blocking for any high-frequency custom-connector design — one of the corpus's own composed disqualifiers.

**Related criteria.** DC-D-037, DC-D-040, DC-D-043, DC-D-086, DC-D-045.
**Related anti-patterns.** AP-D-049, AP-D-051, AP-D-025, AP-D-016.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `integration-architecture.md` §3 (envelope table), IA-12, IA-13, IA-14, I-08, I-13, I-33, I-34, I-35, C-01, U-02, U-15, §7 items 1–4, §9 row 3; `performance-scale.md` §2 meter 3, PF-27, PF-28, §3.C row 29; `data-architecture.md` DA-32; manifest NB-02.

---

#### DC-D-040 — Sustained end-to-end throughput at horizon

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The total sustained rate the whole path must carry, projected to the investment horizon with a growth rate — evaluated against **all** meters and against the weakest participant.

**Why it matters.** This is the criterion that most cleanly produces a platform-exit verdict, and the corpus states the boundary precisely: sustained rate exceeding the smallest of {entitlement per owner, service protection per identity, connector throttle per connection}, **with no natural partitioning**, moves the integration responsibility out. Three supporting facts: **the meters are evaluated separately** and *"Batch operations aren't a valid strategy to bypass entitlement limits"*; the **weakest system in the chain governs** — *"Integration performance depends on the capability of each system involved"*; and sustained over-limit operation is not an error but a **14-day countdown to automatic disablement**, with editing the artefact resetting the evidence.

**Discovery evidence.** Records or messages per period at horizon, with a growth rate (the corpus's worked example uses a five-year window and 20% annual growth); the **other** system's documented or measured throughput; whether the load can be partitioned across connections, identities or artefacts; existing throttling evidence.

**States.** `INSIDE ENVELOPE` · `INSIDE WITH PARTITIONING` · `EXCEEDS, PARTITIONABLE` · `EXCEEDS, NOT PARTITIONABLE` · `UNKNOWN`.

**Decision impact.** `EXCEEDS, PARTITIONABLE` → distribute across identities or connections and accept the identity-management cost, or move the data leg to the exempt in-platform mechanism, or delegate the volume to a bulk mechanism with the automation orchestrating. `EXCEEDS, NOT PARTITIONABLE` → the platform keeps the user-facing and business-record parts; a broker plus workers takes the volume.

**PP positive.** `INSIDE ENVELOPE` at horizon with headroom, or volume delegable to a bulk mechanism.
**PP caution.** `EXCEEDS, PARTITIONABLE` — partitioning is a documented mitigation with a real management cost, not a free win.
**PP negative/exit.** [`Xr`] **`EXCEEDS, NOT PARTITIONABLE` is a documented exit** for the integration responsibility.
**Blocking.** `UNKNOWN` is decision-blocking — and the corpus is pointed about the failure mode: *"scale anxiety without a number"* is not a reason to leave, and an absent number is not a reason to stay.

**Related criteria.** DC-D-037, DC-D-039, DC-D-086, DC-D-087, DC-D-089, DC-D-045.
**Related anti-patterns.** AP-D-016, AP-D-049, AP-D-048, AP-D-021.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `integration-architecture.md` §12.4, IA-01, IA-06, IA-07, IA-10, §2.1 rows 1, 4, §9 rows 1, 6; `performance-scale.md` §2, PF-22, PF-29, B-03, B-09, DC-03, DC-20, §8.1 items 6–7; `automation-architecture.md` AT2-02, AT2-04, AT2-10, §4.1, §4.3, §9 row 3; `platform-suitability.md` PS-18, PS-19, §2 rows 10–11.

---

#### DC-D-041 — Delivery guarantee and ordering requirement

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** What must be true of every message: at-most-once, at-least-once or effectively-once delivery; whether order is required; whether duplicates are tolerable; whether replay is required; and what must happen to a message that cannot be processed.

**Why it matters.** **The guarantee is a property of the transport, not of the automation.** The platform's automation layer has **no dead-letter construct and no circuit-breaker construct** (both recorded as `INF` absence claims to be treated as unsupported until verified), so poison-message handling and fail-fast are not expressible in it. Ordering via a trigger setting is a trap: it is **irreversible**, drops triggers under load, and collapses batch size — the corpus's rule is that *"ordering at volume is a broker requirement, not a trigger setting"*. Both trigger types are **unsafe across an outage in opposite directions** (replay flood versus silent loss). And the transports differ materially: only one of the three common ones offers ordering, duplicate detection **and** dead-lettering together; the streaming one has **no dead-lettering**; the eventing one guarantees **neither ordering nor exactly-once**.

**Discovery evidence.** What the business does if a message is lost, duplicated or processed out of order; whether replay of a past window is required; whether a failed message must be quarantined and inspected; the volume at which ordering is required.

**States.** `BEST EFFORT` · `AT-LEAST-ONCE, DUPLICATES TOLERABLE` · `AT-LEAST-ONCE, IDEMPOTENT REQUIRED` · `ORDERED` · `EFFECTIVELY-ONCE` · `REPLAY REQUIRED` · `UNKNOWN`.

**Decision impact.** Anything beyond *"retry then fail and log it"* → transport selection, i.e. a broker, with the platform as producer or **idempotent consumer** — never the guarantee itself. `ORDERED` at volume → a broker with session or partition semantics, trigger concurrency left off. `REPLAY REQUIRED` → a transport with capture, or a durable message log outside the automation. Every at-least-once path additionally requires DC-D-052.

**PP positive.** `BEST EFFORT` and `AT-LEAST-ONCE, DUPLICATES TOLERABLE`.
**PP caution.** `AT-LEAST-ONCE, IDEMPOTENT REQUIRED` — achievable in-platform via an alternate key with upsert semantics, provided a stable business key exists.
**PP negative/exit.** [`Xr`] `ORDERED` at volume, `EFFECTIVELY-ONCE`, `REPLAY REQUIRED`, or any poison-message quarantine requirement → the guarantee moves to a transport outside the platform (ALT-006, ALT-009).

**Related criteria.** DC-D-052, DC-D-053, DC-D-054, DC-D-029, DC-D-103.
**Related anti-patterns.** AP-D-015, AP-D-017, AP-D-018, AP-D-021.
**Related alternatives.** ALT-006, ALT-009, ALT-007.
**Lineage.** `integration-architecture.md` IA-15, IA-26, IA-46, I-12, I-44, §2.1 row 6, §9 rows 12–13, X-09, X-10, U-11, U-12, U-16, §8; `automation-architecture.md` AT2-06, AT2-18, AT2-22, AT2-26, AT2-28, N-04, N-08, N-34…N-42, §9 rows 4, 11; `performance-scale.md` PF-36, DC-10, B-10; `architecture-patterns.md` matrix rows 9–12, AP-04.

---

#### DC-D-042 — Latency class

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How quickly each stream must complete, expressed as a number and a class: interactive, near-real-time, or eventually consistent.

**Why it matters.** The synchronous windows are hard, layered and documented — an automation's inbound and outbound windows, a task-focused client's outbound window, and server-side code's execution ceiling — and the documented remedy is *"asynchronous, not a longer timeout"*. Beyond the platform, the alternatives' windows are also bounded (one code-first orchestration tier shares the same synchronous window; a serverless host caps HTTP response at a fixed ceiling **on every plan**), so "move it out" does not automatically buy an unbounded synchronous window. And there is a harder absence behind all of it: **no end-to-end latency figure is published for any path**.

**Discovery evidence.** The number, in seconds, per stream; whether a person or a caller is waiting; what the business does if the response does not arrive; measured latency of the participating systems; user network conditions.

**States.** `EVENTUAL` · `NEAR-REAL-TIME` · `INTERACTIVE (SUB-SECOND TO SECONDS)` · `STRICT LOW-LATENCY` · `UNKNOWN`.

**Decision impact.** Beyond the synchronous window → respond inside it and continue asynchronously with a status resource, or move the step out entirely. `STRICT LOW-LATENCY` end-to-end across an application, an automation and an external system is **not sized anywhere in this corpus** and is an exit condition. On high-latency links the binding constraint becomes the **number of round trips**, not per-call latency.

**PP positive.** `EVENTUAL` and `NEAR-REAL-TIME`; `INTERACTIVE` for single-hop paths inside the windows.
**PP caution.** `INTERACTIVE` across several hops or a customer-operated participant (DC-D-091).
**PP negative/exit.** [`Xp`] **`STRICT LOW-LATENCY`, transactionally-visible, end-to-end → out of the platform**, or the requirement is renegotiated.

**Related criteria.** DC-D-050, DC-D-084, DC-D-091, DC-D-018, DC-D-051.
**Related anti-patterns.** AP-D-019, AP-D-048, AP-D-003.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `integration-architecture.md` IA-08, IA-09, §2.1 row 5, §9 row 4, X-07; `performance-scale.md` PF-04, PF-11, PF-14, PF-35, B-08, B-16, DC-07, DC-11, PF-U-01; `automation-architecture.md` AT2-12, AT2-32, N-18, N-26, §9 row 5; `platform-suitability.md` PS-28, §2 row 18.

---

#### DC-D-043 — Payload size and type

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Bytes per message or call, and whether the content is text, structured data or binary.

**Why it matters.** Payload ceilings are mechanism-specific, low in several cases, and cause **hard failure or silent truncation** rather than degradation. The documented set includes: an on-premises gateway write ceiling of about 2 MB (with a conflicting figure on another page, so the corpus's provisional reading is the lower one), read request and compressed-response ceilings, and a short URL ceiling; an event-publishing context ceiling above which heavy properties are **stripped** and, if still too large, *"an error occurs and the message isn't sent"*; a webhook truncation ceiling with a property-removal header; a batch-size ceiling with no nesting; and a standard-tier broker message ceiling **far below** the automation's own message ceiling, which forces a claim-check pattern for documents. Binary through the identity-protected mechanism is **unsupported by design** and *"may result in corrupted or unreadable files"*.

**Discovery evidence.** Bytes per message at the 95th percentile and at maximum; whether binary; whether documents move through the integration or by reference; total bytes per 24-hour window (DC-D-025).

**States.** `SMALL (KB)` · `MODERATE (SUB-MB)` · `LARGE (MB)` · `VERY LARGE / DOCUMENTS` · `BINARY` · `UNKNOWN`.

**Decision impact.** Check the payload ceiling of **every** mechanism on the path. `LARGE` through a gateway → the ceiling is decisive; place a component in-network instead. `VERY LARGE / DOCUMENTS` through a broker → claim-check (send a reference, store the payload). `BINARY` → exclude the identity-protected mechanism outright.

**PP positive.** `SMALL` to `MODERATE` on mechanisms with headroom.
**PP caution.** Designs sized "at about 3 MB" through a gateway — the two published figures conflict and the corpus's provisional reading is the lower.
**PP negative/exit.** [`Xr`] On-premises source with payloads above the gateway ceiling → an in-network component or an enclosing boundary (a self-hosted gateway is the documented mechanism).

**Related criteria.** DC-D-025, DC-D-039, DC-D-044, DC-D-041.
**Related anti-patterns.** AP-D-049, AP-D-035.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `integration-architecture.md` IA-12, IA-14, IA-25, IA-27, I-05, I-06, I-09, I-19, I-35, C-05, §3, §7 items 1, 5–9, §9 row 3; `automation-architecture.md` AT2-28, AT2-29, N-34, N-42; `data-architecture.md` DA-34, DA-50; `architecture-patterns.md` matrix rows 23–24.

---

#### DC-D-044 — Network boundary and private-connectivity requirement

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Where each endpoint sits — public internet, private network, or on-premises — who owns that network, and whether private connectivity is mandated for the path.

**Why it matters.** This criterion carries the corpus's densest set of hard preconditions and one outright collision. On-premises reach requires a **customer-operated** gateway estate: an 8 GB-minimum host, *"a cluster of Windows VMs"* for business-critical use, ≥ 2 nodes per cluster with separate development and production clusters, recovery-key custody described as *"a significant business risk"*, a credential-cache lag of hours, a data-source ceiling per cluster, only the last six monthly releases supported, and the vendor stating it *"doesn't investigate poor performance when a gateway … is overloaded"*. Private egress requires a linked subscription, delegated subnets in **both** regions of a pair (pinning the region), 25–30 production addresses per environment, and a dedicated subnet per policy; it **breaks public calls by design** unless address translation is attached; subnet range and DNS become **immutable**; a **custom root certificate authority cannot be added**; identity and token traffic **does not traverse it**; and it is unavailable on trial and team-hosted environments and in one sovereign tier. **The collision:** the platform's own event-publishing mechanism *"doesn't support VNet"*, so private egress and platform-native eventing cannot both be satisfied through that mechanism. And whether **inbound** private connectivity exists at all is an open unknown.

**Discovery evidence.** Endpoint location per stream; the network policy clause; whether the endpoint's certificate chains to a well-known authority; whether a gateway estate already exists and who runs it; whether an Azure subscription is linked to the tenant; the environment type.

**States.** `PUBLIC ENDPOINTS ACCEPTABLE` · `PRIVATE ENDPOINT REQUIRED` · `ON-PREMISES ENDPOINT` · `PRIVATE AND ON-PREMISES` · `AIR-GAPPED` · `UNKNOWN`.

**Decision impact.** `ON-PREMISES ENDPOINT` → a gateway estate with its operating cost and payload ceilings in the option, or an in-network component. `PRIVATE ENDPOINT REQUIRED` → private egress with all its preconditions costed and its region pinning accepted — and if platform-native eventing is also required, the collision must be resolved before the option is viable. `AIR-GAPPED` → see DC-D-108.
**Blocking.** `UNKNOWN` is decision-blocking: the preconditions are irreversible (immutable subnet and DNS, region pinning) and licence-bearing.

**PP positive.** `PUBLIC ENDPOINTS ACCEPTABLE`; `ON-PREMISES ENDPOINT` within the payload ceilings where a funded, owned gateway estate exists.
**PP caution.** `PRIVATE ENDPOINT REQUIRED` — a subscription dependency, region pinning, an immutable network decision, and a premium-licence prerequisite for the affected population.
**PP negative/exit.** [`Xr`] An endpoint the gateway cannot reach (unsupported protocol), a private certificate authority on the path, an excluded environment type or sovereign tier, or the private-egress/eventing collision with both required → an in-network component or an enclosing boundary; at the extreme, out of the platform.

**Related criteria.** DC-D-038, DC-D-043, DC-D-063, DC-D-033, DC-D-108, DC-D-091.
**Related anti-patterns.** AP-D-035, AP-D-026, AP-D-019.
**Related alternatives.** ALT-006, ALT-007, ALT-005, ALT-009.
**Lineage.** `integration-architecture.md` IA-27, IA-28, IA-29, IA-30, I-09, I-10, §3, §7 items 5, 18–22, 28–29, §12.5, U-09, U-19, U-20, §9 row 15; `data-architecture.md` DA-34, DA-35, DA-36, DAP-21, U-10, §2 rows 18–19; `security.md` SEC-30, §4 row 10; `architecture-patterns.md` matrix rows 23–25, Q-29; `licensing-cost.md` LC-30, LC-U-06.

---

#### DC-D-045 — Interface availability and protocol requirement

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether each target system exposes a programmatic interface the platform can consume, and over which protocol.

**Why it matters.** No interface means no connector, and the only in-platform remainder is interface automation — with the fragility, logging ceiling and per-concurrent-bot cost that carries. Protocol also decides the mechanism outright: only certain definition formats are accepted (one specification version only, with a definition-file size ceiling and **no client-credentials grant type**); a common legacy protocol is assigned to a different tier; and trading-partner protocols are explicitly assigned to an integration platform rather than the platform's automation layer. One enterprise-system case is documented in detail: its native call protocol *"only works with the SAP OData connector"* for the private-network path, so protocol choice and network choice interact.

**Discovery evidence.** Per system: does an interface exist, is it documented, who owns it, what protocol, what authentication; whether a definition file exists; whether the vendor supports integration at all; whether trading-partner protocols are in scope.

**States.** `MODERN INTERFACE AVAILABLE` · `LEGACY PROTOCOL` · `TRADING-PARTNER PROTOCOL` · `DATABASE-LEVEL ONLY` · `NO PROGRAMMATIC INTERFACE` · `UNKNOWN`.

**Decision impact.** `MODERN INTERFACE AVAILABLE` → a connector generated from its definition, subject to DC-D-039. `LEGACY PROTOCOL` or `TRADING-PARTNER PROTOCOL` → a mediation tier or an integration platform. `NO PROGRAMMATIC INTERFACE` → build the interface, or use interface automation as a **bounded bridge** only where the target's remaining lifetime does not justify building one and the volume fits the queue model.

**PP positive.** `MODERN INTERFACE AVAILABLE` with a stable contract.
**PP caution.** `DATABASE-LEVEL ONLY` — schema reuse requires an audit (server-side triggers break writes, missing keys make tables read-only, several types are unsupported, identifier rules apply).
**PP negative/exit.** [`Xr`] `TRADING-PARTNER PROTOCOL` → an integration platform tier. `LEGACY PROTOCOL` unsupported by any connector → a mediation tier. `NO PROGRAMMATIC INTERFACE` **plus** high volume → build the interface or move the responsibility.

**Related criteria.** DC-D-039, DC-D-044, DC-D-046, DC-D-056, DC-D-036.
**Related anti-patterns.** AP-D-020, AP-D-025, AP-D-035.
**Related alternatives.** ALT-006, ALT-007, ALT-005.
**Lineage.** `integration-architecture.md` IA-32, IA-39, I-08, I-25, §3, §9 row 24, §12.2, U-08, U-10, C-03; `data-architecture.md` DA-30, DAP-20; `automation-architecture.md` AT2-40, AT2-63, §9 row 15; `architecture-patterns.md` matrix row 15, Q-26; `platform-suitability.md` U-10.

---

#### DC-D-046 — Contract volatility

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How often the target system's interface contract is expected to change, and whether the platform side can absorb those changes.

**Why it matters.** Change cost on a direct seam is **manual and multiplicative across consumers**: a schema change *"requires republishing and removing/re-adding the connection in every consuming app"*. The documented remedy is a mediation tier whose gateway *"acts as a facade to the backend services, allowing API providers to abstract API implementations and evolve backend architecture without impacting API consumers"*. Where the contract is not merely volatile but **semantically hostile**, the documented answer is a translation layer, so that the legacy model does not leak into every artefact — with the caution that such a layer *"adds latency"* and *"adds an extra service that you must manage and maintain"*, and should be retired when its migration completes.

**Discovery evidence.** Release cadence of the target system; who controls it; whether breaking changes have occurred; how many consumers would need republishing; whether the contract's data model matches the business domain.

**States.** `STABLE` · `PERIODIC CHANGE` · `FREQUENT CHANGE` · `SEMANTICALLY HOSTILE` · `UNKNOWN`.

**Decision impact.** `STABLE` with one consumer → a direct seam, accepting the republish cost per change. `FREQUENT CHANGE` or two-plus consumers → a mediation tier with versioning. `SEMANTICALLY HOSTILE` → a translation layer, with a retirement decision recorded at the point it is created.

**PP positive.** `STABLE` with a single consumer.
**PP caution.** `PERIODIC CHANGE` on a business-critical path — the seam needs a named owner on both sides (DC-D-036).
**PP negative/exit.** [`Ri`] none evidenced. **In-platform redirect:** `FREQUENT CHANGE` or two-or-more consumers → a mediation tier with versioning; `SEMANTICALLY HOSTILE` → a translation layer with a recorded retirement decision. Whether that tier sits inside the platform or outside it is a design choice driven by DC-D-045 and DC-D-047, not a documented exit of this criterion.

**Related criteria.** DC-D-047, DC-D-036, DC-D-045, DC-D-083.
**Related anti-patterns.** AP-D-025, AP-D-023, AP-D-006 (not retiring the translation layer).
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `integration-architecture.md` I-07, I-20, I-47, IA-49, §4.2, §9 row 8; `architecture-patterns.md` AP-02, AP-08, matrix rows 3–4, §6.3, §8 items 4, 9; `alm-devops.md` ALM-14, §14.1.

---

#### DC-D-047 — Consumer count for a backend capability

**Domain:** Integration · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How many distinct consumer classes — applications, automations, agents, external systems — need the same backend capability.

**Why it matters.** It is the corpus's cleanest and most concrete escalation trigger, and it cuts both ways. **Two or more** consumer classes is the documented condition for centralising: *"shifting the logic from the canvas app to a RESTful API… centralizing the logic where it could be used by other applications in the organization"*. **One** consumer is the condition under which a mediation tier is *"unnecessary complexity"* — *"the API layer adds a hop, a bill, a team and a deployment unit with no requirement behind it"*.

**Discovery evidence.** Which artefacts need this capability now and which are planned; whether another team already calls the same backend; whether the same transformation exists in more than one place today.

**States.** `ONE` · `TWO` · `SEVERAL` · `MANY ACROSS TEAMS` · `UNKNOWN`.

**Decision impact.** `ONE` → direct seam; do not buy mediation. `TWO` or more → mediation for **that capability**, provided a mediation requirement actually applies. `MANY ACROSS TEAMS` combined with a governance requirement → an enclosing boundary, and the other patterns operate inside it. An anticipated second consumer counts only if it is dated and recorded as the justification.

**PP positive.** `ONE`, and `TWO` where a lightweight mediation option is available inside existing entitlement.
**PP caution.** `SEVERAL` without a topology decision — the point-to-point estate forms here.
**PP negative/exit.** [`Cf`] none from consumer count alone; combines with DC-D-036 (an existing boundary already provides the tier).

**Related criteria.** DC-D-035, DC-D-046, DC-D-036, DC-D-070.
**Related anti-patterns.** AP-D-022, AP-D-023, AP-D-005.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `integration-architecture.md` IA-49, I-31, §4.1, §4.2 (both directions), §9 rows 7, 18, X-11; `architecture-patterns.md` matrix rows 1–2, 5, §6.2, Y-02, Y-04, APR-U-09.

---

### 4.5 Automation

#### DC-D-048 — Automation shape

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Which of four shapes the requirement actually is, determined by **what holds the state** and **what the unit of failure is**: a bounded run, a long-lived process, a message in transit, or a volume of work to split.

**Why it matters.** The corpus makes this the first automation question because it decides the technology family before any limit does: *"Most failed Power Automate architectures are a shape-2/3/4 requirement implemented as shape 1."* The ordered test is: (1) is the artefact a **message that must not be lost, duplicated or reordered**? (2) must work be **split and recombined**, or does one step need real computation? (3) must the process **outlive a single run** — beyond 30 days, a deployment, a version change, or resume mid-way? (4) otherwise it is a bounded run.

**Discovery evidence.** What the business would ask about a stuck instance; where the state lives today; what the unit of retry is; whether the process survives a system restart; whether the artefact is a document, a case, a message or a batch.

**States.** `WORKFLOW (BOUNDED RUN)` · `PROCESS ORCHESTRATION` · `INTEGRATION ORCHESTRATION` · `DISTRIBUTED PROCESSING` · `MIXED` · `UNKNOWN`.

**Decision impact.** `WORKFLOW` → the platform's automation layer, which is a first-class engine for this shape. `PROCESS ORCHESTRATION` → durable state in a business process record with a re-triggering automation, or an external durable orchestrator. `INTEGRATION ORCHESTRATION` → a broker carries the guarantee; the platform is producer or idempotent consumer. `DISTRIBUTED PROCESSING` → a bulk mechanism, a data pipeline, or a fan-out orchestrator — with the platform orchestrating rather than iterating. `MIXED` is the common real case and legitimately produces more than one mechanism.

**PP positive.** `WORKFLOW`, and any shape where the platform is the front door and another mechanism does the work.
**PP caution.** `MIXED` implemented as a single shape — the corpus's named failure.
**PP negative/exit.** [`Cf`] none from shape alone; shape selects the family, and the specific ceilings (DC-D-049, DC-D-050, DC-D-057) produce the exits.

**Related criteria.** DC-D-049, DC-D-050, DC-D-041, DC-D-054, DC-D-057, DC-D-005.
**Related anti-patterns.** AP-D-015, AP-D-016, AP-D-018.
**Related alternatives.** ALT-004, ALT-006, ALT-009.
**Lineage.** `automation-architecture.md` §2 (the four shapes and the classification test), §3, §4, §9 row 1, AT2-21, AT2-32; `performance-scale.md` §1; `integration-architecture.md` §2.2.

---

#### DC-D-049 — Process elapsed duration

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How long a single business process instance may remain open, from start to completion, including any time waiting for a person.

**Why it matters.** The platform's run duration is a **30-day hard ceiling that includes pending human waits**, pending approvals **time out silently at 30 days**, and run history is retained for 30 days — so a process that runs longer cannot be held in a run at all, and its state is not addressable once the run ends. Beyond the platform, the alternatives differ: one code-first orchestration tier extends to 90 days in its stateful form but collapses to **five minutes** in its stateless form; a durable orchestrator has no documented orchestration ceiling but constrains its code (no current time, no random identifiers, no I/O, no sleeps) and **deploying a change can break in-flight instances**.

**Discovery evidence.** The longest observed instance duration; the longest acceptable human wait; whether instances are ever paused for weeks; whether an instance must survive a release; what "where is instance N?" is answered with today.

**States.** `MINUTES` · `HOURS` · `DAYS` · `UP TO 30 DAYS` · `BEYOND 30 DAYS` · `MONTHS OR OPEN-ENDED` · `UNKNOWN`.

**Decision impact.** `UP TO 30 DAYS` → a run is viable, with the approval timeout designed for. `BEYOND 30 DAYS` → the **run mechanism itself becomes unavailable**; the documented answer is a **business record with a re-triggering automation** — a legitimate in-platform pattern, not a platform change. A durable orchestrator is a **design option for the same redirect**, not the documented exit. `MONTHS OR OPEN-ENDED` → a queryable process record is mandatory regardless of platform, and audit retention beyond 30 days becomes a functional requirement on the design (DC-D-103).

**PP positive.** `MINUTES` to `UP TO 30 DAYS`, with the human-wait ceiling explicitly designed for.
**PP caution.** Processes near 30 days — the approval timeout is silent, which makes the failure invisible.
**PP negative/exit.** [`Ri`] none evidenced. **In-platform redirect:** at `BEYOND 30 DAYS` held as a single run, the run mechanism becomes unavailable and the documented answer is a **business record with a re-triggering automation** — a mechanism change, not a platform change (Repair V3, 2026-09-03: corrected from `Xr`; the field named nothing leaving the platform, so §2.5's decisive test does not admit this class — see DC-D-025 for the same pattern). A durable orchestrator is a design option for the same redirect (Decision impact), not a documented exit.

**Related criteria.** DC-D-048, DC-D-055, DC-D-054, DC-D-103, DC-D-101.
**Related anti-patterns.** AP-D-015, AP-D-021.
**Related alternatives.** ALT-006, ALT-009 — design options for the redirect, not exit destinations.
**Lineage.** `automation-architecture.md` AT2-13, AT2-14, AT2-24, N-09, N-19, N-22, N-28, N-30, §3.A row 8, §3.B row 12, §4.2, §9 row 7; `performance-scale.md` PF-37, DC-08, §3.C row 24; `platform-suitability.md` PS-22, PS-23.

---

#### DC-D-050 — Synchronous response requirement

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether any step must complete while a person or a calling system waits for its result, and within what time.

**Why it matters.** The synchronous windows are documented, layered and **not tunable**: an automation's inbound and outbound windows, a task-focused client's outbound window, and server-side code's execution ceiling. Every product in the family caps synchronous response in a narrow band, so escalating does not buy an unbounded window — one code-first tier extends it modestly, and a serverless host caps HTTP response at a fixed ceiling **regardless of its own timeout setting, on every plan**. Using an automation as a request/response interface at user-facing volume is additionally an anti-pattern for a second reason: **every action, including retries and pagination, consumes the owner's entitlement**.

**Discovery evidence.** Which steps have a waiting caller; the acceptable wait in seconds; whether a "submitted, we'll tell you" experience is acceptable; whether the caller can poll a status.

**States.** `NONE (ALL ASYNCHRONOUS)` · `WITHIN THE PLATFORM WINDOW` · `BEYOND THE PLATFORM WINDOW` · `STRICT SUB-SECOND` · `UNKNOWN`.

**Decision impact.** `BEYOND THE PLATFORM WINDOW` → respond inside the window and continue asynchronously **with a status resource** (*"you must implement a mechanism"*), or move the step to a host with a longer window. For a genuine request/response contract at volume, the answers are in-platform server-side code (a custom interface, transaction-capable, not subject to change-set restrictions) or a service outside — not an automation.

**PP positive.** `NONE` and `WITHIN THE PLATFORM WINDOW`.
**PP caution.** An automation used as an application's command channel — acceptable for fire-and-forget or short operations, not as an interface layer.
**PP negative/exit.** [`Xr`] `STRICT SUB-SECOND` at user-facing volume → server-side platform code or a service outside the platform.

**Related criteria.** DC-D-042, DC-D-084, DC-D-048, DC-D-057, DC-D-086.
**Related anti-patterns.** AP-D-019, AP-D-016, AP-D-015.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `automation-architecture.md` AT2-12, AT2-32, AT2-35, AT2-58, N-18, N-26, §3.A row 9, §3.B row 11, §9 row 5; `performance-scale.md` PF-04, PF-35, DC-07, B-08, §3.C row 23; `platform-suitability.md` PS-28, §2 row 18; `architecture-patterns.md` AP-09, matrix row 13, Y-08.

---

#### DC-D-051 — Event frequency floor and trigger freshness

**Domain:** Automation · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** MEDIUM

**Definition.** The shortest interval between events the solution must react to, and how quickly a change must be detected.

**Why it matters.** There is a **structural floor**: scheduled recurrence bottoms out at 60 seconds, per-trigger latency is a **per-connector property with no published aggregate**, and *"Instant triggers aren't truly instant"*. Below the floor it is *"not a tuning problem"* — it needs a different mechanism. The **volatility** is real: current per-licence polling intervals are an open unknown in **three** canonical areas, with one page's figures possibly stale, so no per-connector interval can be quoted. There is also a trade the corpus insists on stating: switching to push is **not a pure win**, because the two trigger types are *"unsafe across an outage, in opposite directions"* — polling replays a backlog, push silently loses events.

**Discovery evidence.** The shortest interval between real events; the detection latency the business needs; the connector or mechanism involved; whether the source can push; what must happen to events that occur during an outage.

**States.** `HOURLY OR SLOWER` · `MINUTES` · `SUB-MINUTE` · `CONTINUOUS STREAM` · `UNKNOWN`.

**Decision impact.** `SUB-MINUTE` → event or webhook push, a broker, or a synchronous call; not a schedule. `CONTINUOUS STREAM` → a streaming service, because a run per event is the wrong unit (and that service is **unsized** in this corpus). Always add a trigger-side predicate on a busy source, and **state the outage behaviour** of the trigger type chosen.

**PP positive.** `HOURLY OR SLOWER` and `MINUTES` with a trigger predicate.
**PP caution.** Any freshness figure derived from a per-connector interval — those figures are the corpus's open unknown, not a lookup.
**PP negative/exit.** [`Xr`] `CONTINUOUS STREAM` → a streaming service. `SUB-MINUTE` with no push mechanism available on the source → a broker or a synchronous call, and if neither exists the requirement changes.

**Related criteria.** DC-D-018, DC-D-042, DC-D-037, DC-D-041, DC-D-086.
**Related anti-patterns.** AP-D-024, AP-D-051, AP-D-063 (polling consumes entitlement on empty checks).
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `automation-architecture.md` AT2-11, AT2-22, AT2-26, AT2-60, N-08, U-02, U-13, §4.3, §9 row 6, C-05; `performance-scale.md` PF-32, DC-06, B-07, PF-U-08; `data-architecture.md` DA-47, C-10, U-20; `integration-architecture.md` X-04, I-22, §2.1 rows 2, 5.

---

#### DC-D-052 — Idempotency key availability

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether a stable business key exists that lets a repeated operation be recognised as a repeat rather than executed twice.

**Why it matters.** Retry is **on by default**, delivery on both trigger and transport sides is **at-least-once**, and the vendor's own examples of the consequence are a repeated insert causing *"incorrect values in the table"* and users receiving *"duplicate messages"*. So idempotency is **a precondition for enabling retry on a side-effecting action, not a later refinement**. The in-platform mechanism is an alternate key with upsert semantics — which requires the key to exist. **Duplicate detection is not a substitute**: it is suppressed by default on interface updates, has no default rules outside a few standard entities, and returns an error status that naive retry logic loops on. Retry depth is also **licence-dependent**, so the same design duplicates differently depending on who owns it.

**Discovery evidence.** Whether the payload carries a stable identifier from its source; whether the business has a natural unique key; whether duplicates would be noticed and what they would cost; whether the source can supply a correlation identifier.

**States.** `STABLE KEY EXISTS` · `KEY CAN BE CREATED` · `NO STABLE KEY, DUPLICATES TOLERABLE` · `NO STABLE KEY, DUPLICATES INTOLERABLE` · `UNKNOWN`.

**Decision impact.** `STABLE KEY EXISTS` → alternate key plus upsert; retry safe to enable. `KEY CAN BE CREATED` → **the requirement must fund creating it**, which is a scope item. `NO STABLE KEY, DUPLICATES INTOLERABLE` → collapse the write into one transactional boundary, or accept and document the duplicate risk with a named owner — there is no third option in the corpus. One retry owner per call chain must be named in the design.

**PP positive.** `STABLE KEY EXISTS` or `KEY CAN BE CREATED`.
**PP caution.** Any at-least-once path without a key, on any platform — this is symmetric, not platform-specific.
**PP negative/exit.** [`—`] none as a platform exit. It is a **blocking** condition for enabling retry, and therefore for any at-least-once design.
**Blocking.** `UNKNOWN` is decision-blocking for any brokered or retried side-effecting design.

**Related criteria.** DC-D-041, DC-D-028, DC-D-054, DC-D-021, DC-D-034.
**Related anti-patterns.** AP-D-017, AP-D-011, AP-D-013, AP-D-018.
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `automation-architecture.md` AT2-16, AT2-56, N-06, §9 rows 8–9; `data-architecture.md` DA-52, DA-53, DA-60, DAP-39, DQ-12, §2 row 23; `integration-architecture.md` I-44, IA-15, §8, §9 rows 12, 26; `performance-scale.md` PF-38.

---

#### DC-D-053 — Concurrency, parallelism and ordering

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How many instances may run at once, whether in-run iteration must be parallel, and whether processing order is required.

**Why it matters.** Three documented defaults and one irreversible setting decide this. In-run iteration **defaults to sequential** (a concurrency of one), which the corpus calls *"the commonest cause of 'the flow is slow'"*; the maximum is bounded. Trigger concurrency, if switched on to obtain ordering, is **irreversible without deleting and re-adding the trigger**, **drops triggers** under load (*"To ensure all triggers result in flow runs, leave the Concurrency Control setting off"*), and **collapses batch size from a large ceiling to 100**. So ordering at volume is a **transport** property, not a trigger setting. Array size in one iteration is also capped, and the cap is **licence-profile-dependent**.

**Discovery evidence.** Whether order matters and why; the volume at which it matters; whether concurrent instances would conflict on the same record; expected instances per minute; whether loss of a trigger would be noticed.

**States.** `ORDER IRRELEVANT` · `ORDER PREFERRED` · `ORDER REQUIRED, LOW VOLUME` · `ORDER REQUIRED, AT VOLUME` · `HIGH PARALLELISM REQUIRED` · `UNKNOWN`.

**Decision impact.** `ORDER REQUIRED, AT VOLUME` → an ordered transport in front, trigger concurrency **left off**. `ORDER REQUIRED, LOW VOLUME` → trigger concurrency of one is acceptable **only** for low-volume, loss-tolerant work in an isolated child artefact, with the irreversibility accepted. `HIGH PARALLELISM REQUIRED` → set in-run concurrency explicitly and bound it against the target's own limits (autoscaling without bounding moves the overload downstream).

**PP positive.** `ORDER IRRELEVANT` or `ORDER PREFERRED` with in-run concurrency set deliberately.
**PP caution.** `ORDER REQUIRED, LOW VOLUME` — the setting is irreversible and lossy; the corpus's advice is to isolate it.
**PP negative/exit.** [`Xr`] none as a platform exit; `ORDER REQUIRED, AT VOLUME` is an exit from the in-platform mechanism to a transport (ALT-006, ALT-009).

**Related criteria.** DC-D-041, DC-D-037, DC-D-086, DC-D-085, DC-D-093.
**Related anti-patterns.** AP-D-015, AP-D-049, AP-D-016.
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `automation-architecture.md` AT2-06, AT2-07, AT2-18, N-04, N-05, N-24, §9 row 4; `performance-scale.md` PF-34, PF-36, DC-10, B-10, §3.C rows 20–22; `integration-architecture.md` X-10, I-44, IA-22, U-17.

---

#### DC-D-054 — Failure semantics after partial completion

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** What the state of the world must be after a mid-process failure — and who or what resolves it.

**Why it matters.** **There is no rollback.** A failed run leaves completed actions completed, and nothing in the error-handling guidance describes an undo. So partial completion is the **default outcome**, and the design must state what that means for the business. The corpus's framing is a question the design must answer: *"what is the world's state after a mid-run failure?"* — and *"No answer → the design needs a transaction boundary, a saga with durable state, or per-message semantics."* Related: the platform's automation layer has **no dead-letter and no circuit-breaker construct**, so there is no in-platform place to put an unresolvable item.

**Discovery evidence.** What the business does today when half the work completes; whether an in-doubt state is recognised; whether someone reviews failures; whether a compensating action exists and is safe to repeat; how a failed item is currently found.

**States.** `TOLERANT (RETRY AND CONTINUE)` · `COMPENSATION DEFINED` · `IN-DOUBT STATE REQUIRED` · `MUST NOT PARTIALLY COMPLETE` · `UNKNOWN`.

**Decision impact.** `MUST NOT PARTIALLY COMPLETE` → collapse into one transactional boundary (DC-D-028) or leave the platform for the coordination. `IN-DOUBT STATE REQUIRED` → a persisted in-doubt marker on the business record, a human resolution path, and a named owner for the queue of unresolved items. `COMPENSATION DEFINED` → the compensating actions, mapping rules and reconciliation schema are **contract artefacts under change control**, and the identity permitted to execute them is a **privileged integration identity**.
**Blocking.** `UNKNOWN` is decision-blocking for a business-critical process: proceeding means the failure behaviour is whatever the implementation happens to do.

**PP positive.** `TOLERANT` and `COMPENSATION DEFINED` with idempotent steps.
**PP caution.** `IN-DOUBT STATE REQUIRED` — viable in-platform, but it is a design with owners, not a setting.
**PP negative/exit.** [`Xr`] `MUST NOT PARTIALLY COMPLETE` across systems → out of the platform for the coordination responsibility.

**Related criteria.** DC-D-028, DC-D-052, DC-D-041, DC-D-100, DC-D-006.
**Related anti-patterns.** AP-D-018, AP-D-017, AP-D-021, AP-D-011.
**Related alternatives.** ALT-005, ALT-006, ALT-007, ALT-009.
**Lineage.** `automation-architecture.md` AT2-21, AT2-64, N-07, §5.5, §9 row 8; `integration-architecture.md` X-16, IA-46, §8, §9 row 13, U-11, U-12; `data-architecture.md` DA-52, DAP-8; `security.md` SEC-XB-04; `alm-devops.md` §14.5; `governance.md` GOV-XB-04.

---

#### DC-D-055 — Human-in-the-loop requirement

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether a person must decide, approve, delegate, escalate, reject or cancel within the process — and within what elapsed time.

**Why it matters.** This is one of the corpus's clearest **positive** signals for the platform: approvals are a first-class construct backed by the governed store, with several response models including sequential, reachable from mail, chat and an action centre, on a **standard (non-premium) connector**. The bound is elapsed time: **pending steps time out at 30 days**, silently. Reassignment, timeout and escalation mechanics are an open unknown in the corpus and should be verified per engagement.

**Scope of the comparative claim (repair, 2026-09-03).** The first version of this criterion carried the unscoped phrase *"no equivalent in the alternatives"* and presented it as *"a comparative capability fact rather than a preference"*. That overstates what the source establishes. `automation-architecture.md` §4.1 row 12 is tagged AT2-23/AT2-24/AT2-25 — findings which establish that approvals **exist** and what they do, not what other classes lack. The defensible claim is narrower, and is the one this criterion now makes:

- **Against the code-first alternatives the corpus examined (ALT-005, ALT-006): evidenced.** *"Moving this leg to Logic Apps or Functions means building all of it"* — approval routing with delegation, escalation and an action centre has no equivalent there and must be built.
- **Against an incumbent process or service-management engine (ALT-007): `UNKNOWN`.** *"No Microsoft or independent source evaluates incumbent BPM/ESB platforms; treat as reasoning, not evidence"* (`automation-architecture.md` §3.B row 19), repeated in `alternatives.md` ALT-007. Many such engines exist precisely to do this. The corpus cannot say whether one is better, worse or equivalent, and this criterion does not.
- **Against other low-code platforms (ALT-008): `UNKNOWN`** — every dimension except deployment model is unassessed (`alternatives.md` §6 item 2).

**Discovery evidence.** Which steps need a human decision; the decision-maker population; whether delegation and escalation are required; the longest acceptable wait; where the decision happens today (mail, chat, a system, paper).

**States.** `NONE` · `SIMPLE APPROVAL` · `MULTI-STAGE OR SEQUENTIAL` · `WITH DELEGATION AND ESCALATION` · `GUIDED DATA ENTRY` · `UNKNOWN`.

**Decision impact.** Any human decision within 30 days → **keep this leg in the platform even if other legs move** — **precondition: DC-D-111 is not `PLATFORMS EXIST WITH PUBLISHED CONTRACTS` for this process class.** Where an incumbent process or workflow engine already owns the class, this rule and DC-D-036 / DC-D-111 / ALT-007's redirect point in opposite directions, and the redirect wins on the corpus's own instruction: *"Adding Power Automate duplicates the operating model rather than reducing it"* (`automation-architecture.md` AT2-52). Resolve DC-D-111 **before** applying this rule; the platform's approval construct is a reason to keep the leg where nothing else already owns it, not a reason to take it from an owner. `GUIDED DATA ENTRY` inside a record-centric surface → the guided-stage construct, within its caps and noting it **executes no logic of its own** (stretching it into a conditional wizard engine is a named anti-pattern). Waits beyond 30 days → state in a business record (DC-D-049).

**PP positive.** `SIMPLE APPROVAL` through `WITH DELEGATION AND ESCALATION` inside 30 days, **where no incumbent engine owns the process class** — the platform's strongest documented capability in this domain, and an evidenced gap in the code-first classes. Not a differentiator against incumbent process engines, which the corpus does not evaluate.
**PP caution.** Escalation and reassignment mechanics are an open unknown; verify before promising them.
**PP negative/exit.** [`—`] none evidenced. This criterion pulls **toward** the platform.

**Related criteria.** DC-D-049, DC-D-048, DC-D-009, DC-D-019, **DC-D-111** (the precondition), DC-D-036.
**Related anti-patterns.** AP-D-015 (moving this leg out without cause), AP-D-027 (bypassing an incumbent that already owns the process class).
**Related alternatives.** ALT-004 (positively, subject to DC-D-111), ALT-007 (where a process engine already owns it — comparative fit `UNKNOWN`, §4A.2).
**Lineage.** `automation-architecture.md` AT2-23, AT2-24, AT2-36, N-09, U-03, C-06, §3.A rows 1–2, §4.1, §9 row 12; `platform-suitability.md` PS-22, §2 row 5; `application-architecture.md` AA-19, AP-30.

---

#### DC-D-056 — Unattended interface-automation need

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether the solution must drive another application through its user interface, without a person present, and at what concurrency.

**Why it matters.** It is a bounded, expensive and operationally distinctive mechanism, and the corpus's positioning is explicitly exceptional: *"Use desktop flows on the rare occasions when the connectors don't meet your requirements or for a one-time screen scraping need."* The documented envelope: a bounded run queue, a maximum queue wait and a maximum run duration; dispatch adding up to 50 seconds per run, which *"can make parallel runs look sequential"*; **only the first 10,000 actions of a run are logged** — *"Extra actions are performed but aren't logged"*; one licence **per simultaneous unattended process**, with unattended runs costing a multiple of cloud runs; a premium **user** still required to register the machine; host sizing of four-plus cores plus two cores and 4 GB per additional session; and unavailability in several sovereign clouds.

**Discovery evidence.** Whether the target exposes any interface (DC-D-045); the target's remaining lifetime; runs per period and required concurrency; whether a person is present; the target's release cadence; who maintains the selectors.

**States.** `NOT REQUIRED` · `ATTENDED ONLY` · `UNATTENDED, LOW CONCURRENCY` · `UNATTENDED, HIGH CONCURRENCY` · `UNKNOWN`.

**Decision impact.** Justified only where **all** hold: no programmatic interface exists, the target's remaining lifetime does not justify building one, and the volume fits the queue model. Otherwise the decision is to build or buy the interface. `UNATTENDED, HIGH CONCURRENCY` → price the per-concurrent-bot licensing and the host estate, and treat the logging ceiling as an observability gap.

**PP positive.** `ATTENDED ONLY` on an interface-only target with a person present.
**PP caution.** `UNATTENDED, LOW CONCURRENCY` — the cost multiplier, the logging ceiling and the selector-maintenance owner.
**PP negative/exit.** [`Xr`] none as a platform exit; the exit is **from this mechanism** to the target's interface (DC-D-045). Note that the fragility framing is **not** a vendor statement — the corpus records that explicitly.

**Related criteria.** DC-D-045, DC-D-053, DC-D-096, DC-D-101, DC-D-033.
**Related anti-patterns.** AP-D-020, AP-D-021.
**Related alternatives.** ALT-005, ALT-006, ALT-001.
**Lineage.** `automation-architecture.md` AT2-37, AT2-38, AT2-39, AT2-40, AT2-63, N-43…N-50, U-06, U-07, §3.A rows 6–7; `licensing-cost.md` LC-08, LC-17, DC-09; `platform-suitability.md` PS-21; `architecture-patterns.md` §8 item 21.

---

#### DC-D-057 — Compute intensity

**Domain:** Automation · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether any step performs real computation — optimisation, simulation, iteration to convergence, large-matrix work, image or media processing — as distinct from orchestrating calls.

**Why it matters.** It is the corpus's **first** classification test and an out-of-platform verdict **before any other sizing**: *"Does one step need real computation… rather than orchestrating calls? → COMPUTE. Power Platform has no compute-sizing dial; this is an out-of-platform verdict before any other sizing."* The supporting facts: the expression language is not a general-purpose imperative language (no imperative loops, no mutable local state), with hard expression-evaluation ceilings; server-side platform code caps at two minutes **and its execution time is charged to the triggering request's service-protection budget**, so compute there consumes the caller's budget; and no surface exposes a compute-sizing control.

**Discovery evidence.** Whether any step is described as a calculation, an algorithm, a model, a solve, a render or a transform; whether a library is required; expected execution time per invocation; whether the result must be synchronous.

**States.** `ORCHESTRATION ONLY` · `LIGHT CALCULATION` · `SIGNIFICANT COMPUTE` · `SPECIALISED COMPUTE` (models, media, solvers) · `UNKNOWN`.

**Decision impact.** `SIGNIFICANT COMPUTE` or above → the compute step leaves the platform, and **the hosting plan is part of the decision** (plans differ in execution ceiling, cold-start behaviour and outbound-connection limits; one legacy plan has a dated retirement). The platform keeps the business-facing front door — this is the corpus's canonical hybrid shape, not a whole-solution relocation.

**PP positive.** `ORCHESTRATION ONLY` and `LIGHT CALCULATION`.
**PP caution.** Light calculation growing over time — the corpus notes that an automation which has grown a computation is usually also approaching its action ceiling, and treats both as the same signal.
**PP negative/exit.** [`Xr`] **`SIGNIFICANT COMPUTE` and `SPECIALISED COMPUTE` are documented exits** for the compute step, and evaluated *before* other sizing.

**Related criteria.** DC-D-050, DC-D-084, DC-D-048, DC-D-110, DC-D-096.
**Related anti-patterns.** AP-D-003, AP-D-015, AP-D-026.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `performance-scale.md` §1 (test step 1), PF-45, PF-22, B-14, DC-12, §3.A row 4; `automation-architecture.md` AT2-32, AT2-62, N-25…N-28, N-33, §3.B row 15, §4.2, §9 row 13; `platform-suitability.md` PS-08, PS-09, §2 row 17.

---
### 4.6 Security

#### DC-D-058 — Data sensitivity classification

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The organisation's own classification of the data the solution holds, and the controls that classification mandates.

**Why it matters.** Sensitivity is the input that turns several other criteria from preferences into requirements — access granularity, audit, key control, network isolation, egress control — and each of those carries a **licence prerequisite priced by affected population**, not by number of applications. It also drives the enforcement-plane question: a requirement must be satisfied on the **lowest plane that can enforce it**, and a requirement met only in the application is *"not enforced at all"* against someone holding the connection's credentials. One documented asymmetry is worth carrying: sensitivity labels that must **travel with a downloaded file** require the document store, because the governed store's file columns have no label mechanism.

**Discovery evidence.** The organisation's classification scheme and this data's tier; whether personal, special-category, financial or commercially sensitive data is in scope; the controls the classification mandates; whether a data protection assessment exists.

**States.** `PUBLIC` · `INTERNAL` · `CONFIDENTIAL` · `HIGHLY RESTRICTED` · `SPECIAL CATEGORY / REGULATED` · `UNKNOWN`.

**Decision impact.** Each tier upward adds mandated controls and therefore mandated entitlement across the affected population. `HIGHLY RESTRICTED` and above typically pull in DC-D-062, DC-D-063, DC-D-064 and DC-D-067 together — which is exactly the combination the corpus's composed disqualifier addresses when the population is unfunded.
**Blocking.** `UNKNOWN` is decision-blocking: the control set, and therefore the cost, cannot be established.

**PP positive.** `INTERNAL` and `CONFIDENTIAL` with record and field scoping on the governed store.
**PP caution.** `HIGHLY RESTRICTED` — verify each mandated control against DC-D-062's administrator exclusion and the field-security exclusion list before accepting the architecture.
**PP negative/exit.** [`Cf`] none from sensitivity alone; it combines with DC-D-062 (administrator exclusion) and DC-D-092 (unfunded control population) to produce exits.

**Related criteria.** DC-D-026, DC-D-027, DC-D-059, DC-D-062, DC-D-063, DC-D-064, DC-D-067, DC-D-092.
**Related anti-patterns.** AP-D-029, AP-D-030, AP-D-033, AP-D-034, AP-D-064.
**Related alternatives.** ALT-001, ALT-003, ALT-005, ALT-007.
**Lineage.** `security.md` §1 (five planes and the derived rule), SEC-13, SEC-18, SEC-34, §2, §4 rows 1–6, 16, SEC-XB-01; `data-architecture.md` DA-44, DA-59, §2 rows 5–7, 21, §3; `licensing-cost.md` LC-30.

---

#### DC-D-059 — Regulatory and contractual compliance regime

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The specific regulations, standards and contractual clauses the solution must satisfy, and the evidence each requires.

**Why it matters.** A regime converts several criteria into non-negotiables and can create requirements the platform documents as unavailable — most sharply confidentiality **from administrators** (`security.md` §4 row 6: not achievable in the governed store) and **exact datacentre disclosure** (documented as not available). It also drives residency (DC-D-033) with its irreversible environment decision, key control, evidence retention and assurance artefacts. Two corpus cautions matter here: the platform's own security score is **preview and *"for evaluation purposes only at this time"*** and *"must not be used as the assurance artefact"*; and preview capabilities are **excluded from the service commitments**, so a regulated production path must avoid them.

**Discovery evidence.** The named regimes and the clauses that bind; what evidence an auditor will require and in what format; whether an assurance report is contractually owed; whether sovereign-cloud eligibility applies; whether the regime prescribes key custody or administrator exclusion.

**States.** `NONE STATED` · `INTERNAL POLICY` · `SECTOR REGULATION` · `REGULATED WITH EXTERNAL AUDIT` · `SOVEREIGN / GOVERNMENT` · `UNKNOWN`.

**Decision impact.** Build assurance from **configuration evidence plus audit exports**, not from a platform score. Enumerate the regime's mandated controls and check each against the platform's documented exclusions **before** the option is accepted; where the regime mandates something documented as unavailable, the option changes.
**Blocking.** `UNKNOWN` is decision-blocking — one of the corpus's named "do not infer silently" cases.

**PP positive.** `INTERNAL POLICY` and `SECTOR REGULATION` where the mandated controls map onto available features and the population is funded.
**PP caution.** `REGULATED WITH EXTERNAL AUDIT` — the assurance artefact must be constructed, and preview components are excluded from the path.
**PP negative/exit.** [`Xp`] Administrator-excluded confidentiality; datacentre-level disclosure; or a regime whose mandated control has no available implementation → out of the governed store for that data, or out of the platform.

**Related criteria.** DC-D-033, DC-D-058, DC-D-062, DC-D-064, DC-D-103, DC-D-115.
**Related anti-patterns.** AP-D-033, AP-D-057, AP-D-029, AP-D-064.
**Related alternatives.** ALT-005, ALT-007, ALT-001, ALT-011.
**Lineage.** `security.md` SEC-35, §4 rows 6, 16, 18, SEC-U-04, SEC-C1; `platform-suitability.md` PS-17, PS-47, §2 rows 30, 36; `data-architecture.md` DA-55, DA-57, DA-58; `operations-support.md` OP-AP-14, §6.4; `governance.md` GOV-A12, §4 row 15.

---

#### DC-D-060 — Authentication and identity model

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How users and services authenticate, and which conditional or contextual controls apply.

**Why it matters.** Identity is the outermost enforcement plane and the one whose gaps are least visible. The corpus records that a conditional-access policy can **miss a first-party application identifier**, and that continuous access evaluation is supported by **one service only** — which is why revocation immediacy is a separate criterion (DC-D-066). It also records that a licence grants **neither** environment membership nor data-layer rights: both are required and neither is implied.

**Discovery evidence.** The identity provider(s) in use; whether conditional access applies and to which applications; whether privileged identity management is in place; whether service identities are used and who owns them; whether guests are involved.

**States.** `ORGANISATIONAL DIRECTORY ONLY` · `DIRECTORY WITH CONDITIONAL ACCESS` · `FEDERATED / MULTIPLE PROVIDERS` · `EXTERNAL CONSUMER IDENTITY` · `MIXED` · `UNKNOWN`.

**Decision impact.** Conditional-access coverage must be **verified per application identifier**, not assumed. Environment membership plus data-layer roles must both be designed. `EXTERNAL CONSUMER IDENTITY` routes to DC-D-061, where the corpus records a superseded recommendation that must not be carried forward.

**PP positive.** `ORGANISATIONAL DIRECTORY ONLY` and `DIRECTORY WITH CONDITIONAL ACCESS`.
**PP caution.** `FEDERATED / MULTIPLE PROVIDERS` — one mechanism explicitly does not support a federation service, and the corpus leaves the frontline and shared-device identity case as an open unknown.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-061, DC-D-066, DC-D-062, DC-D-009, DC-D-068.
**Related anti-patterns.** AP-D-032, AP-D-033.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `security.md` SEC-01…SEC-06, SEC-15, SEC-16, SEC-36, §1 plane 1, §2, §4 rows 3, 19; `integration-architecture.md` IA-31, I-35, I-37, §7 items 23–25; `platform-suitability.md` PS-60, U-14.

---

#### DC-D-061 — External identity requirement

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** For users outside the organisation, what identity and access model is required — guest identities from a partner organisation, customer identities, or anonymous access.

**Why it matters.** It selects the surface and the licensing model simultaneously, and it carries three documented traps. **Guest access to the governed store is restricted by default on new environments**, and that restriction covers that store only — guests still reach other surfaces in the same environment. **Cross-tenant licence recognition is conditional**: guest entitlement must be held in the correct tenant, and **per-app entitlements are not recognised cross-tenant**. And the recommended path for consumer identity **changed**: the corpus records an earlier recommendation as superseded (the previously-recommended consumer identity service closed to new tenants), so *new builds use the current external-identity offering* — a fact whose short half-life the corpus flags explicitly.

**Discovery evidence.** Who the external users are and who employs them; whether they already hold guest identities; whether the population is knowable; whether self-registration is required; whether anonymous access is genuinely needed or merely convenient.

**States.** `NONE` · `PARTNER GUESTS` · `CUSTOMER AUTHENTICATED` · `PUBLIC ANONYMOUS` · `MIXED` · `UNKNOWN`.

**Decision impact.** `PARTNER GUESTS` → a dedicated environment, an explicit guest decision per environment, and a licence check that per-app entitlements will fail. `CUSTOMER AUTHENTICATED` → the external-site surface with web roles and table permissions (**no access without a table permission; a table permission without a role has no effect**), consumption-metered on unique contacts. `PUBLIC ANONYMOUS` → the same surface with the exposure conditions of `anti-patterns.md` AP-D-034, or a custom surface.
**Blocking.** `UNKNOWN` is decision-blocking: the surface, the environment topology and the licence model all depend on it.

**PP positive.** `PARTNER GUESTS` with recognised entitlement; `CUSTOMER AUTHENTICATED` over the governed store with a reviewed permission model.
**PP caution.** `PUBLIC ANONYMOUS` — see DC-D-009's caution and negative signals.
**PP negative/exit.** [`Cf`] none from this criterion alone beyond DC-D-009's combined exits.

**Related criteria.** DC-D-009, DC-D-060, DC-D-067, DC-D-094, DC-D-018.
**Related anti-patterns.** AP-D-034, AP-D-033, AP-D-058 (the superseded recommendation).
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `security.md` SEC-04, SEC-32, §4 rows 7–8, SEC-C1, SEC-U-09; `application-architecture.md` AA-25, AA-52, AA-C5, AA-C10, §1 rows 4–5; `platform-suitability.md` PS-36, §2 rows 14–15; `licensing-cost.md` DC-05, LC-07, LC-12, §7.2 items 21, 40.

---

#### DC-D-062 — Privileged access and administrator-exclusion requirement

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether any data must be inaccessible to platform administrators, and how privileged access is governed and evidenced.

**Why it matters.** This produces one of the corpus's few unambiguous single-criterion exits. Field-level security **never applies to the system administrator**; the corpus's own conclusion for *"Confidential even from administrators"* is **"Not achievable in Dataverse"**, with the only options being *"Keep the attribute outside Dataverse, or reduce admins to an auditable, JIT-only set"*. Two supporting facts: broad privileges granted *"to unblock the project"* **cannot be walked back** (privileges are additive, with no subtraction); and key control has a documented malicious-administrator scenario requiring **separation of key-vault and platform administration duties**.

**Discovery evidence.** Whether a clause names administrator exclusion; the size of the administrator population; whether privileged identity management with just-in-time elevation is in place; whether privileged actions are audited and reviewed; who holds key custody.

**States.** `NONE` · `PRIVILEGED ACCESS GOVERNED` · `JUST-IN-TIME ONLY` · `ADMINISTRATOR EXCLUSION REQUIRED` · `UNKNOWN`.

**Decision impact.** `ADMINISTRATOR EXCLUSION REQUIRED` → the attribute leaves the governed store, or the administrator population is reduced to an auditable just-in-time set and the residual is accepted in writing. `PRIVILEGED ACCESS GOVERNED` → time-boxed elevation rather than permanent role widening, group-driven assignment, and separation of key and platform duties where key control is in scope.

**PP positive.** `NONE` and `PRIVILEGED ACCESS GOVERNED`.
**PP caution.** `JUST-IN-TIME ONLY` — achievable, and it must be evidenced rather than asserted.
**PP negative/exit.** [`Xr`] **`ADMINISTRATOR EXCLUSION REQUIRED` is a documented exit** for the affected attribute.

**Related criteria.** DC-D-026, DC-D-058, DC-D-064, DC-D-066, DC-D-068, DC-D-027.
**Related anti-patterns.** AP-D-029, AP-D-032, AP-D-030.
**Related alternatives.** ALT-005, ALT-001, ALT-007.
**Lineage.** `security.md` SEC-02, SEC-08, SEC-13, SEC-22, SEC-29, SEC-36, SEC-A4, SEC-A5, SEC-A12, §4 rows 5–6, 11; `data-architecture.md` DA-11, DA-55, DAP-10.

---

#### DC-D-063 — Platform network-isolation mandate

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the solution's own platform traffic must be restricted to corporate networks or private connectivity — as distinct from reaching a private endpoint (DC-D-044).

**Why it matters.** The controls exist and are narrower than commonly assumed. The address-based control is **available only in the managed environment class**, protects **one data service only**, **defaults to audit-only mode**, and by default still allows **all application identities and the vendor's trusted services**. Private egress carries the preconditions and the collision described in DC-D-044. Both carry **licence prerequisites across the affected population** — the managed environment class plus, for some controls, higher-tier productivity or directory entitlements. The corpus's rule: *"if unfunded, the option is economically infeasible rather than 'secure by configuration'"*.

**Discovery evidence.** The network policy clause; whether corporate-network-only access is mandated; whether the tenant already holds the prerequisite entitlements; how many users are in the enforcement scope; whether application identities are expected to be constrained too.

**States.** `NONE` · `CORPORATE NETWORK PREFERRED` · `CORPORATE NETWORK MANDATED` · `PRIVATE CONNECTIVITY MANDATED` · `UNKNOWN`.

**Decision impact.** `CORPORATE NETWORK MANDATED` → the managed environment class plus the licence population, an application-identity allowlist, and an audit-mode rollout — and **do not leave audit-only mode on and call it enabled**. `PRIVATE CONNECTIVITY MANDATED` → see DC-D-044's preconditions and collision.

**PP positive.** `NONE` and `CORPORATE NETWORK PREFERRED`.
**PP caution.** `CORPORATE NETWORK MANDATED` — the control's scope is one service, so other surfaces need their own answer (DC-D-067).
**PP negative/exit.** [`Xc`] A mandate whose licence population is **unfunded** → the corpus's composed disqualifier: the security requirement and the commercial constraint are *incompatible with the proposed design*.

**Related criteria.** DC-D-044, DC-D-058, DC-D-067, DC-D-092, DC-D-093, DC-D-071.
**Related anti-patterns.** AP-D-033, AP-D-035, AP-D-064, AP-D-059.
**Related alternatives.** ALT-005, ALT-006, ALT-007, ALT-008.
**Lineage.** `security.md` SEC-27, SEC-30, SEC-A11, §2, §4 rows 9–10, SEC-XB-01; `data-architecture.md` DA-36, DA-56, U-10, §2 row 19; `integration-architecture.md` I-10, §7 items 18–22; `licensing-cost.md` LC-30, DC-14 (security-controls variant); `architecture-patterns.md` §13.

---

#### DC-D-064 — Encryption-key control requirement

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the customer must control the encryption keys protecting the data, and whether it must be able to approve or refuse vendor access.

**Why it matters.** Both controls exist, both are gated, and both carry documented consequences that change the architecture. Customer key control requires the managed environment class **and** higher-tier productivity entitlements, covers a **listed** set of services and explicitly **excludes** connection settings, environment settings, application display names and descriptions, and connection metadata; **audit is not available with it**; backup and restore are constrained; and **revocation is an outage**. On a relational engine the equivalent is *cheaper to reach* (no managed-environment or higher-tier gate) but makes the key store a **tier-zero availability dependency with a short recovery cliff**. For the document store the corpus **corrects** a common claim: customer key control **is** available via a dedicated policy, and the real limit is **granularity** (one policy per tenant or geography, not per site or application) plus entitlement and two paid subscriptions.

**Discovery evidence.** Whether a clause requires customer-managed keys; whether vendor-access approval is required; who would hold key custody; whether the exclusion list conflicts with a stated requirement; whether audit is also required.

**States.** `PLATFORM-MANAGED ACCEPTABLE` · `CUSTOMER-MANAGED REQUIRED` · `CUSTOMER-MANAGED PLUS ACCESS APPROVAL` · `UNKNOWN`.

**Decision impact.** Adopt customer key control **only where a clause demands it**, and then: separate key-vault and platform administration duties, enumerate the exclusion list against the requirement, resolve the **audit conflict explicitly**, and treat the key store as a tier-zero dependency. The corpus's framing is that this is *"a data-at-rest control"* — not a general confidentiality answer.

**PP positive.** `PLATFORM-MANAGED ACCEPTABLE`.
**PP caution.** `CUSTOMER-MANAGED REQUIRED` — the entitlement population, the exclusion list, the audit conflict, and the revocation-as-outage behaviour. The interplay with analytical replication is an open unknown.
**PP negative/exit.** [`Xc`] none as an outright exit; where key control and audit are **both** mandated, the conflict must be resolved before the option is viable, which can eliminate it.

**Related criteria.** DC-D-058, DC-D-059, DC-D-027, DC-D-062, DC-D-093, DC-D-100.
**Related anti-patterns.** AP-D-064, AP-D-033, AP-D-035.
**Related alternatives.** ALT-003, ALT-005, ALT-007.
**Lineage.** `security.md` SEC-29, SEC-A12, §2, §4 row 11, SEC-XB-01; `data-architecture.md` DA-55, DAP-43, SQ2-01, SQ2-02, SQ2-09, SQ2-10, U-22, §2 row 21; `licensing-cost.md` LC-30.

---

#### DC-D-065 — Secrets and credential lifecycle

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the solution requires secrets, whether a "no stored secrets" policy applies, and who owns rotation and expiry.

**Why it matters.** The sanctioned mechanism is **vault-backed secret variables consumable by only three component types**, and *"the secrets aren't available for use in other customizations or generally via the API"* — so several surfaces have **no sanctioned mechanism**, which is why secrets end up in artefacts. A secret placed in an action input becomes **readable from run history**. Managed identity — the mechanism that removes the secret entirely — covers **server-side platform code only**, not connectors, automations or applications. Certificate and authentication-key expiry on external-facing sites are **dated obligations requiring a named owner**.

**Discovery evidence.** Which components need a secret and of what type; whether a "no stored secrets" policy exists; who owns rotation; whether certificates or keys expire and who is notified; whether run-history access is broader than the secret's audience.

**States.** `NO SECRETS REQUIRED` · `SECRETS IN SUPPORTED COMPONENTS ONLY` · `SECRETS REQUIRED IN UNSUPPORTED SURFACES` · `NO STORED SECRETS MANDATED` · `UNKNOWN`.

**Decision impact.** The policy **selects the component type**: secret-dependent logic moves to an automation, a connector, or server-side code with managed identity. `NO STORED SECRETS MANDATED` on a surface with no mechanism → the leg moves out of the platform. Certificate and key lifecycles get a named owner and a calendar entry.

**PP positive.** `NO SECRETS REQUIRED` and `SECRETS IN SUPPORTED COMPONENTS ONLY`.
**PP caution.** Run-history exposure — a secret in an action input is readable at high volume by anyone with history access.
**PP negative/exit.** [`Xr`] **`NO STORED SECRETS MANDATED` on a leg outside the three supported component types is a documented exit** for that leg (server-side code with managed identity, or a worker outside).

**Related criteria.** DC-D-060, DC-D-062, DC-D-044, DC-D-103, DC-D-075.
**Related anti-patterns.** AP-D-031, AP-D-032, AP-D-044.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `security.md` SEC-06, SEC-07, SEC-A10, §2, §4 row 12; `automation-architecture.md` AT2-49, AT2-50, N-14, §9 row 18; `integration-architecture.md` IA-31, IA-32, I-27, I-36, §7 items 22–23; `governance.md` GOV-23, §4 row 12; `architecture-patterns.md` matrix row 26.

---

#### DC-D-066 — Access-revocation immediacy

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How quickly access must actually cease after a termination, role change or compromise.

**Why it matters.** Removing a role does not immediately end a session: token lifetime is roughly an hour without continuous access evaluation, and continuous evaluation is supported by **one service only** — so the practical revocation window is a property of the identity configuration, not of the application. The corpus's remedy is explicit: continuous evaluation plus **group-driven role assignment**, rather than manual role removal. This also interacts with automation ownership: a departure changes an automation's performance profile and its notification destination (DC-D-006).

**Discovery evidence.** The stated revocation requirement in minutes or hours; whether joiner-mover-leaver automation is in place; whether roles are assigned via groups or directly; whether continuous evaluation is enabled; what happens to sessions in progress.

**States.** `NEXT DAY ACCEPTABLE` · `WITHIN HOURS` · `IMMEDIATE` · `UNKNOWN`.

**Decision impact.** `IMMEDIATE` → continuous access evaluation plus group-driven assignment, and an accepted residual on services that do not support continuous evaluation. Direct user-to-role assignment at scale defeats joiner-mover-leaver automation and is a named anti-pattern.

**PP positive.** `NEXT DAY ACCEPTABLE` and `WITHIN HOURS`.
**PP caution.** `IMMEDIATE` — reachable for the service that supports continuous evaluation; a residual remains elsewhere and should be stated rather than assumed away.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-060, DC-D-062, DC-D-006, DC-D-068.
**Related anti-patterns.** AP-D-032, AP-D-036.
**Related alternatives.** ALT-004.
**Lineage.** `security.md` SEC-03, SEC-11, SEC-A5, §4 row 19; `integration-architecture.md` I-37, §7 item 24; `automation-architecture.md` AT2-01, N-01.

---

#### DC-D-067 — Data-egress control requirement

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether data must be prevented from leaving the tenant or reaching unapproved services, and whether the control must be preventive or detective.

**Why it matters.** This is where over-claiming is most common and most consequential. Connector data policies are scoped by the vendor to reducing *"the risk of users **unintentionally** exposing organizational data"* — **guardrails, not an exfiltration control** — and the default state is permissive (*"By default, no data policies are implemented in the tenant"*). The newer allowlist mechanism currently covers **certified connectors only** and **does not cover custom or interface connectors**; endpoint filtering is preview and **not enforced** for environment variables, custom inputs or runtime-computed endpoints. Tenant isolation covers **directory-authenticated connectors only**, has a documented gap, and takes about an hour to propagate. And a further gap the corpus records as open: whether **any** control can restrict export to a spreadsheet or reads through the data endpoint beyond privacy privileges and the address control — with the data endpoint on by default.

**Discovery evidence.** The clause requiring egress control; whether the requirement is preventive or detective; whether custom or interface connectors are in scope; whether spreadsheet export must be prevented; whether the read endpoint's default state has been reviewed.

**States.** `NONE` · `DETECTIVE ONLY` · `PREVENTIVE FOR APPROVED SERVICES` · `STRICT EXFILTRATION PREVENTION` · `UNKNOWN`.

**Decision impact.** Build a **layered posture with each layer's scope stated**: the allowlist for what it covers, classic policy for the custom and interface gap, target-side controls beyond, tenant isolation with its residual accepted. Never design a control whose enforcement depends on a mechanism documented as non-enforcing. Note the operational hazard: a policy change can **suspend or quarantine running artefacts** with up to a day's enforcement lag.
**Exit.** `STRICT EXFILTRATION PREVENTION` as an absolute → **this corpus cannot evidence it**; the honest output is `DECISION BLOCKED` or a scope change, not a claim.

**PP positive.** `NONE` and `DETECTIVE ONLY`; `PREVENTIVE FOR APPROVED SERVICES` within the allowlist's documented coverage.
**PP caution.** Custom or interface connectors in scope of a preventive claim — the coverage gap is documented.
**PP negative/exit.** [`Xp`] `STRICT EXFILTRATION PREVENTION` → not evidenced as achievable; treat as blocked rather than met.

**Related criteria.** DC-D-058, DC-D-072, DC-D-063, DC-D-103, DC-D-036.
**Related anti-patterns.** AP-D-033, AP-D-038, AP-D-030.
**Related alternatives.** ALT-001, ALT-007, ALT-005.
**Lineage.** `security.md` SEC-23, SEC-24, SEC-25, SEC-26, SEC-A8, SEC-A9, SEC-C2, §2, §4 rows 14–15, SEC-U-07; `governance.md` GOV-10, GOV-11b, GOV-A4, GOV-A5; `platform-suitability.md` PS-29; `integration-architecture.md` §7 item 27, X-18.

---

#### DC-D-068 — Authorization enforcement point

**Domain:** Security · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Where authorization must be enforced — in the platform, in the target system, or in both — and whose identity the target sees.

**Why it matters.** It decides the connection model and eliminates whole mechanisms. With **explicit** authentication the user's own rights govern; with **implicit** authentication the maker's credentials govern **for every user, invisibly** (*"All users of the flow use embedded connections"*). Where the **target** must authorize per user, the design needs delegated identity — and **virtualized tables are excluded** because they are organisation-owned only. A facade or worker calling downstream as a **shared service identity changes the authorization semantics** and is one of the corpus's composed disqualifiers unless identity is propagated or compensating authorization is implemented. And a relational engine's user-context row-level security **collapses to one principal** behind a shared connection.

**Discovery evidence.** Whether the target system enforces per-user rules today; whether the platform is expected to be the enforcement point; whether shared or implicit connections are proposed; whether an intermediary tier would call downstream as itself.

**States.** `PLATFORM ENFORCES` · `TARGET ENFORCES PER USER` · `BOTH ENFORCE` · `SHARED IDENTITY ACCEPTABLE` · `UNKNOWN`.

**Decision impact.** `TARGET ENFORCES PER USER` → explicit delegated identity, **no shared connection**, and virtualized tables excluded; where a mediation tier is present, identity must be propagated through it **or the registered combination applies** (DC-D-036, DC-D-060; `decision-intelligence-matrix.md` §3 row 6). `PLATFORM ENFORCES` → the store must be able to express the rule (DC-D-026), and application-level filtering is **not** enforcement.

**PP positive.** `PLATFORM ENFORCES` on the governed store; `TARGET ENFORCES PER USER` with explicit identity where the connector supports it.
**PP caution.** `BOTH ENFORCE` — two models to keep aligned, and the corpus notes the composite behaviour is emergent.
**PP negative/exit.** [`Xc`] none from authorization enforcement point alone. Per-user target authorization **through a shared-identity intermediary** combines into a **registered** disqualifier via DC-D-036 and DC-D-060 (`decision-intelligence-matrix.md` §3 row 6) unless identity is propagated through the intermediary or compensating authorization is implemented (Repair V3, 2026-09-03: corrected from `Xr`; no off-platform destination is named anywhere in this criterion — see §2.5's decisive test — and the combination was already registered at matrix §3 row 6, whose Class is `DECISION CRITERION`, not an exclusion).

**Related criteria.** DC-D-026, DC-D-030, DC-D-036, DC-D-060, DC-D-062, DC-D-044.
**Related anti-patterns.** AP-D-030, AP-D-032, AP-D-012, AP-D-059.
**Related alternatives.** ALT-001, ALT-006, ALT-007.
**Lineage.** `security.md` SEC-18, SEC-19, SEC-21, SEC-A1, SEC-A7, §1 (planes 4–5), §2, §4 rows 1, 17, SEC-XB-04; `data-architecture.md` DA-33, DAP-18, DAP-38, SQ2-08, SQ2-15; `integration-architecture.md` IA-33, IA-34, §9 rows 16–17; `architecture-patterns.md` matrix row 17, §13.

---

### 4.7 Governance

#### DC-D-069 — Maker and delivery model

**Domain:** Governance · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Who is permitted to build, under what constraints, and how work moves from a maker's hands into a governed environment.

**Why it matters.** The documented model is *managed makers*: personal development environments, restricted sharing, a restrictive default-environment policy, and promotion via a pipeline — with the essential condition that **the promotion path must exist before makers are enabled**. Without it, adoption lands in the least governed place. The corpus also names both failure directions: over-centralising *drives shadow adoption*, while over-decentralising produces policy fragmentation.

**Discovery evidence.** Who will build; whether personal development environments exist; whether environment creation is restricted; whether a promotion path exists today; whether the organisation has chosen a centralised, decentralised or hybrid delivery model.

**States.** `CENTRAL IT DELIVERY` · `FUSION (BUSINESS PLUS PRO-CODE)` · `GOVERNED CITIZEN DEVELOPMENT` · `UNGOVERNED CITIZEN DEVELOPMENT` · `UNKNOWN`.

**Decision impact.** `UNGOVERNED CITIZEN DEVELOPMENT` → build the governance package first (routing, creation restriction, promotion path, ownership assignment, sharing limits) or keep the workload in a governed delivery model. `FUSION` → the pro-code capability must actually exist (DC-D-110), and where it does not, a design requiring it is a documented risk.

**PP positive.** `CENTRAL IT DELIVERY`, `FUSION` with real pro-code capacity, and `GOVERNED CITIZEN DEVELOPMENT`.
**PP caution.** `UNGOVERNED` — the corpus's detective controls run weekly and only in the managed class, so detection is not prevention.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-070, DC-D-071, DC-D-073, DC-D-110, DC-D-076.
**Related anti-patterns.** AP-D-036, AP-D-037, AP-D-039, AP-D-040.
**Related alternatives.** ALT-004, ALT-011.
**Lineage.** `governance.md` GOV-01, GOV-08, GOV-09, GOV-19, GOV-A1, GOV-A2, GOV-A9, GOV-A10, §2, §4 row 4; `platform-suitability.md` PS-39, PS-40; `alm-devops.md` §1, ALM-A5.

---

#### DC-D-070 — Organisational platform-governance maturity

**Domain:** Governance · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether the organisation has, today, the capability to govern and operate what the proposed architecture requires — including any second platform it introduces.

**Why it matters.** It is a **gating** criterion, not a preference. The corpus makes the point in its strongest form twice: patterns involving an external estate *"are not production-ready"* until a named owning team, inventory, access model, policy baseline, cost owner, delivery-pipeline owner, monitoring ownership and recovery position exist; and where there is no operator, the pattern is *"unavailable, not merely expensive"*. It also runs the argument the other way — the absence of an operating model for a second platform is an explicit, reasoned trigger to **stay in one platform**: *"single platform + a tripwire, not a paper hybrid"*.

**Discovery evidence.** Whether a platform team exists and what it owns; whether a subscription-owning team and an on-call rota exist for the other domain; whether infrastructure-as-code and a delivery pipeline exist there; whether a governance tooling estate exists and is maintained; who owns tenant capacity.

**States.** `NONE` · `EMERGING` · `ESTABLISHED FOR THIS PLATFORM` · `ESTABLISHED ACROSS PLATFORMS` · `UNKNOWN`.

**Decision impact.** `NONE` or `EMERGING` → hybrid, brokered and boundary options are **unavailable** unless the capability is acquired (with its cost and lead time in the option). `ESTABLISHED FOR THIS PLATFORM` → in-platform options with a tripwire on the constraint that would otherwise force a hybrid. Note the debt case: an existing governance estate built on an unmaintained accelerator must be recorded as **technical debt with a migration path**, not as a working capability.
**Blocking.** `UNKNOWN` is decision-blocking for any option with an external component.

**PP positive.** `ESTABLISHED FOR THIS PLATFORM` — and this is a genuine reason to prefer the platform over a hybrid.
**PP caution.** `EMERGING` with a hybrid in the design — the commonest way an option becomes undeliverable after approval.
**PP negative/exit.** [`—`] none as a platform exit; it is an exit from **hybrid and boundary options**.

**Related criteria.** DC-D-073, DC-D-104, DC-D-110, DC-D-083, DC-D-101, DC-D-114.
**Related anti-patterns.** AP-D-026, AP-D-046, AP-D-059, AP-D-058.
**Related alternatives.** ALT-004, ALT-006, ALT-007, ALT-009, ALT-011.
**Lineage.** `governance.md` GOV-XB-01, GOV-12, GOV-A11, GOV-C1; `architecture-patterns.md` Y-13, §5.1, §13, AP-10; `automation-architecture.md` §4.1, AT2-53, §9 row 22; `operations-support.md` §1.1, OP-27, OP-U-07; `alm-devops.md` §14.2, ALM-22.

---

#### DC-D-071 — Environment strategy requirement

**Domain:** Governance · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How many environments the solution requires and why — isolation, residency, lifecycle stages, criticality separation, external-audience separation.

**Why it matters.** The environment is the **security and blast-radius boundary**, and cross-environment data access is not supported; but the count is also a **cost driver on four independent axes** (a storage floor per environment regardless of database; per-app entitlement scoped **per environment**; per-environment minimum assignments for external sites; premium licences for every active user of every *managed* environment). Those axes point in different directions from the governance and lifecycle axes, which is what makes this a real trade-off. Two further facts: environments are **geography-bound at creation**, and the grouping mechanism that prevents configuration drift is **managed-class-only, one group per environment, no nesting, no per-environment exceptions**.

**Discovery evidence.** Isolation domains required; regions required; lifecycle stages required; whether external audiences need separation; whether the default environment currently holds anything that matters; whether creation is restricted.

**States.** `SINGLE ENVIRONMENT` · `DEV / TEST / PROD` · `MULTI-REGION OR MULTI-UNIT` · `COMPLEX ESTATE` · `UNKNOWN`.

**Decision impact.** Design the topology with the **cost axes visible** alongside isolation and lifecycle needs; keep development on developer-plan environments (free of both capacity and managed obligations); minimise the count of *managed* environments to those that need the premium feature set; restrict manual creation as a **separate, explicit** action.

**PP positive.** `DEV / TEST / PROD` with development on developer-plan environments.
**PP caution.** `COMPLEX ESTATE` — the four cost axes compound, and the grouping mechanism supports no exceptions.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-082, DC-D-033, DC-D-093, DC-D-063, DC-D-074, DC-D-001.
**Related anti-patterns.** AP-D-037, AP-D-040, AP-D-038.
**Related alternatives.** ALT-004.
**Lineage.** `governance.md` GOV-02, GOV-03, GOV-04, GOV-07, GOV-08, GOV-09, §1 lever 1, §2, §4 rows 3, 10; `licensing-cost.md` LC-25, DC-13; `security.md` SEC-15, SEC-16, SEC-17, §4 rows 2–3; `alm-devops.md` ALM-08, ALM-24, ALM-25; `operations-support.md` DC-15.

---

#### DC-D-072 — Connector and service permissibility posture

**Domain:** Governance · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** HIGH

**Definition.** Which connectors and external services are permitted in the target environment, and by what process an exception is obtained.

**Why it matters.** The design can be **invalidated at build time** by a policy the project did not check — and, worse, a policy change can **suspend or quarantine running artefacts** with up to a day of enforcement lag, presenting as an integration outage. The corpus's rule is that the required connector set must be verified against the target environment's policy **before commitment**, and it lists this as a standard pre-commitment validation. Volatility is intrinsic: **new connectors are added to the default group over time**, so a check is valid on its date only. And the layered coverage gap matters: the allowlist mechanism covers **certified connectors only** and not custom or interface connectors.

**Discovery evidence.** The tenant baseline policy and any environment exceptions; whether the required connectors are permitted **in the target environment**; the exception process and its owner and lead time; whether custom or interface connectors are in scope.

**States.** `NO POLICY` · `PERMISSIVE BASELINE` · `RESTRICTIVE BASELINE WITH EXCEPTIONS` · `STRICT ALLOWLIST` · `UNKNOWN`.

**Decision impact.** Verify the connector set against the target environment before committing to the design; where a required connector is blocked, either obtain a recorded exception with an owner and expiry, or change the design. Treat **policy count as an architectural variable** — a policy per project produces exponential fragmentation with maker-visible failures that are hard to diagnose.

**PP positive.** `PERMISSIVE BASELINE` or `RESTRICTIVE BASELINE WITH EXCEPTIONS` where the required set is permitted.
**PP caution.** `NO POLICY` — the permissive starting state is a governance gap, not a green light (DC-D-067).
**PP negative/exit.** [`—`] none evidenced; a blocked connector is a design change, not a platform exit.

**Related criteria.** DC-D-067, DC-D-035, DC-D-045, DC-D-071, DC-D-070.
**Related anti-patterns.** AP-D-038, AP-D-033, AP-D-035.
**Related alternatives.** ALT-006, ALT-007.
**Lineage.** `governance.md` GOV-10, GOV-11b, GOV-A4, GOV-A5, GOV-C3, §1 lever 4, §4 rows 5–6; `platform-suitability.md` PS-29, §3 (last boundary), §9; `security.md` SEC-23, SEC-24, SEC-25; `integration-architecture.md` §7 item 27, §9 row 28.

---

#### DC-D-073 — Support and operational ownership

**Domain:** Governance · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Who supports the solution in production — first line, second line, and the escalation path — and whether that capability exists today.

**Why it matters.** The vendor's support does **not** fill this gap: **a support plan is a separate purchase**, **end users cannot raise tickets**, there are **no root-cause analyses** *"as part of any support experience"*, there is a **four-hour cap** on performance and non-reproducible cases after which the case closes, and there is no help with corrupted data. The corpus's conclusion is therefore that **an internal first line is mandatory**, with internal root-cause capability and the telemetry to support it, plus a partner or engineering capability for customised and performance issues. Production support without production edit rights is possible, but it **depends on an ALM setting** — co-ownership on managed artefacts permits reading history, enabling and disabling, and running, without edit rights.

**Discovery evidence.** Who users will contact; whether a service desk exists and would accept this; whether a support plan is held and at what tier; whether anyone can read run history in production; whether a partner arrangement exists.

**States.** `NONE` · `INFORMAL (THE MAKER)` · `SERVICE DESK, FIRST LINE ONLY` · `FULL INTERNAL SUPPORT MODEL` · `PARTNER-SUPPORTED` · `UNKNOWN`.

**Decision impact.** For anything above the departmental class: a named first line, pre-granted read access for whoever is on call, an internal root-cause capability, a support-plan tier derived from **criticality** rather than licence count, and no preview components on critical paths. Note the corpus's own open item: operational handover from a delivery partner to a customer team is *"the commonest real-world failure point for partner-delivered solutions, and entirely undocumented"* — so `PARTNER-SUPPORTED` needs an explicit dated handover plan.
**Blocking.** `UNKNOWN` is decision-blocking above the departmental class.

**PP positive.** `SERVICE DESK, FIRST LINE ONLY` or better, with a support tier matched to criticality.
**PP caution.** `INFORMAL (THE MAKER)` for anything business-critical — the automation-ownership consequences of DC-D-006 follow directly.
**PP negative/exit.** [`—`] none as a platform exit; where no support capability can exist, a vendor-operated product (ALT-011) or the incumbent's own support (ALT-001, ALT-007) may be the only viable classes.

**Related criteria.** DC-D-006, DC-D-102, DC-D-104, DC-D-001, DC-D-097, DC-D-114.
**Related anti-patterns.** AP-D-053, AP-D-056, AP-D-036, AP-D-041.
**Related alternatives.** ALT-001, ALT-007, ALT-011, ALT-004.
**Lineage.** `operations-support.md` OP-24, OP-25, DC-13, DC-14, §2.5, §6.4, OP-C-04, OP-U-07; `governance.md` GOV-13, GOV-15, GOV-A8, §4 rows 7–8; `licensing-cost.md` LC-22, §7.2 item 39; `alm-devops.md` ALM-15; `security.md` §4 row 17.

---

#### DC-D-074 — Solution scope: departmental to enterprise

**Domain:** Governance · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The organisational breadth of the solution: one team, one function, several functions, or the whole organisation — and whether it is a shared capability others will build on.

**Why it matters.** Scope drives the environment topology, the governance obligations and the sharing model, and it is the criterion that most often changes *after* go-live — a team tool becomes a function's tool and then a dependency. The corpus's sharing controls are **forward-only**: limits *"prevent oversharing going forward"* and **existing shares are unaffected**, so a scope change does not retroactively tidy the estate. Scope also interacts with cost: licence auto-claim assigns a premium entitlement **when a user launches an application in a managed environment**, which makes sharing a cost event.

**Discovery evidence.** Who uses it at launch and who might later; whether other teams have asked for it; whether it will be shared broadly or at "everyone" scope; whether it becomes a dependency for other solutions.

**States.** `SINGLE TEAM` · `SINGLE FUNCTION` · `CROSS-FUNCTION` · `ENTERPRISE-WIDE` · `SHARED CAPABILITY` · `UNKNOWN`.

**Decision impact.** Beyond `SINGLE TEAM`: a dedicated environment with a security group, an ownership and support model, sharing limits set deliberately as both a security and a cost control, and a graduation trigger recorded. `SHARED CAPABILITY` additionally implies mediation (DC-D-047) and a contract others depend on.

**PP positive.** Any scope, matched to the environment class and governance obligations it implies.
**PP caution.** `SINGLE TEAM` with a plausible growth path and no graduation trigger — this is the free-tier trap in its governance form.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-001, DC-D-010, DC-D-071, DC-D-047, DC-D-093, DC-D-069.
**Related anti-patterns.** AP-D-065, AP-D-036, AP-D-039, AP-D-047.
**Related alternatives.** ALT-003, ALT-004.
**Lineage.** `governance.md` GOV-19, GOV-18, GOV-24, §1 lever 5, §4 rows 9, 11; `licensing-cost.md` LC-AP-09, DC-03; `operations-support.md` §1.1; `data-architecture.md` DA-13, DA-43; `application-architecture.md` AA-50.

---

#### DC-D-075 — Retirement and lifecycle accountability

**Domain:** Governance · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Who is accountable for deciding the solution's end, disposing of its data, and releasing its resources.

**Why it matters. No retirement process is documented**, and the platform's response to abandonment is **silent disablement** rather than removal — so nothing prompts a decision. Unused resources are **invisible to the monitoring surface but still consume capacity**, contributing to the ceiling that **blocks restore, copy, recovery and environment creation**. The platform supplies fragments (administrator quarantine, weekly orphan and inactivity detection in the managed class, automatic deletion of developer environments after a period, a documented move-out procedure), so retirement is *"a process with platform support, not a platform feature"*. The data side is harder and must be decided early: retention is stamped at write time and non-retroactive, and backups are not an archive.

**Discovery evidence.** Whether the lifecycle model includes a retirement stage; who owns end-of-life data disposition; whether a periodic usage review exists; whether anything currently in the estate is unused but still consuming capacity.

**States.** `NOT CONSIDERED` · `OWNER NAMED, NO PROCESS` · `PROCESS DEFINED` · `PROCESS DEFINED AND EXERCISED` · `UNKNOWN`.

**Decision impact.** Add an explicit retirement stage with a checklist and an owner; schedule a periodic inventory and usage review; and decide **retention, audit scope and deletion policy at environment and table creation**, because several of those decisions are non-retroactive.

**PP positive.** `PROCESS DEFINED` or better.
**PP caution.** `NOT CONSIDERED` — the cost appears as capacity that blocks recovery, not as a visible line.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-032, DC-D-006, DC-D-095, DC-D-004, DC-D-104.
**Related anti-patterns.** AP-D-067, AP-D-063, AP-D-054.
**Related alternatives.** ALT-010, ALT-004.
**Lineage.** `operations-support.md` OP-28, OP-22, DC-19, OP-AP-19, §2.6; `governance.md` GOV-17, GOV-A7, §2, §4 row 14; `data-architecture.md` DA-16, DA-17, DA-18, DAP-13, DAP-14; `alm-devops.md` ALM-25.

---

### 4.8 ALM and delivery

#### DC-D-076 — Source-control requirement

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether the solution's definition must live in a version-controlled repository with branching and reviewable change.

**Why it matters.** The corpus's key insight is that **automation does not supply this**: promotion tooling gives artefact immutability across stages, run history and optional approvals, but **no code review and no diff** — so *"source control is the requirement that forces rung 3, not automation"*. Two other requirements force it independently: **more than one maker on one artefact** (unmanaged work gives no isolation, and co-authoring on the low-code application artefact was removed), and **cross-tenant delivery** (the built-in promotion mechanism cannot cross tenants). Residual uncertainty is recorded: the practical maturity of repository integration for the low-code application artefact specifically is an open item.

**Discovery evidence.** Whether change review before test is required; how many makers; whether code-first components are in the solution; whether compliance requires a change-to-approval trace; whether delivery crosses tenants.

**States.** `NOT REQUIRED` · `DESIRABLE` · `REQUIRED FOR REVIEW` · `REQUIRED FOR MULTI-MAKER ISOLATION` · `REQUIRED FOR CROSS-TENANT DELIVERY` · `UNKNOWN`.

**Decision impact.** Any `REQUIRED` state forces the source-controlled rung, whose prerequisites belong in the option: a repository, a development environment per maker or branch, and pro-code capability. The two rungs are **complementary, not alternatives** — repository integration in *development* environments, promotion tooling for *deployment*.

**PP positive.** `NOT REQUIRED` or `DESIRABLE` for a single-maker departmental solution.
**PP caution.** `REQUIRED FOR REVIEW` — the prerequisites are real cost and capability, not a setting.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-078, DC-D-079, DC-D-082, DC-D-110, DC-D-113, DC-D-007.
**Related anti-patterns.** AP-D-042, AP-D-043, AP-D-041.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `alm-devops.md` §1, ALM-09, ALM-10, ALM-21, ALM-23, ALM-A7, §4 rows 3–5, 14, 16, ALM-C1, ALM-U-03; `application-architecture.md` AA-06, AA-C2; `platform-suitability.md` PS-24, PS-48.

---

#### DC-D-077 — Release frequency and window

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How often releases will occur, and when they are permitted to occur.

**Why it matters.** Release windows are a **performance requirement with an operational basis**: solution import, publishing customisations and bulk security changes are named as **intensive database operations to keep out of business hours**, and manual backups need lead time before a restore is possible. The corpus states the conflict plainly: *"Frequent releases plus no business-hours degradation is a conflict resolved by calendar, not configuration."* Two further constraints: promotion **cannot bypass a stage**, so a hotfix is a normal release on a compressed schedule or a governed exception; and patches are documented as *"not recommended"*. One caveat the corpus keeps open: the source for the intensive-operations list is aged and may not reflect current behaviour.

**Discovery evidence.** Planned release cadence; permitted windows; who approves a release; whether an emergency path exists and who authorises it; whether users are global (which shrinks the window).

**States.** `INFREQUENT, FLEXIBLE WINDOW` · `PERIODIC, DEFINED WINDOW` · `FREQUENT, DEFINED WINDOW` · `CONTINUOUS DELIVERY EXPECTED` · `UNKNOWN`.

**Decision impact.** `FREQUENT` or `CONTINUOUS` with a no-degradation expectation → resolve by calendar and communication, not by configuration; and the emergency path must be defined in advance as a compressed normal release or a recorded exception with a named approver.

**PP positive.** `INFREQUENT` to `PERIODIC` with a defined window.
**PP caution.** `CONTINUOUS DELIVERY EXPECTED` — the deployment operations themselves are a performance event.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-007, DC-D-080, DC-D-083, DC-D-090, DC-D-100.
**Related anti-patterns.** AP-D-045, AP-D-043, AP-D-041.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `performance-scale.md` PF-44, PF-AP-15, DC-16, PF-U-06, PF-C-04; `operations-support.md` OP-23, DC-11, OP-AP-17, OP-C-05; `alm-devops.md` ALM-04, ALM-10, ALM-A9, §4 row 10.

---

#### DC-D-078 — Team size and concurrent development

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How many people will build simultaneously, and whether they must work on the same artefacts.

**Why it matters.** It is a structural constraint, not a tooling preference. Unmanaged work provides **no isolation** — *"Every modification is applied directly to the environment, regardless of which solution is being edited"* — and **co-authoring on the low-code application artefact was removed and is no longer supported**, with one editor per application or page. So *"parallelism only via architecture"*: an environment per developer or branch, and partitioning by persona and team. The corpus is emphatic that the partition seam is drawn by **team and personas**, not by a size heuristic, and that no numeric size cap exists to encode.

**Discovery evidence.** Number of makers and their concurrency; whether they would work on the same artefact; whether developer environments exist per maker; whether pro-code components are involved.

**States.** `SINGLE MAKER` · `2 MAKERS, SEPARATE ARTEFACTS` · `SMALL TEAM, SHARED ARTEFACTS` · `LARGE TEAM` · `UNKNOWN`.

**Decision impact.** `SMALL TEAM, SHARED ARTEFACTS` or larger → an environment per developer or branch plus source control (DC-D-076), and an artefact partition designed around personas and teams. A shared development environment for a team is a named anti-pattern with overwriting as the documented outcome.

**PP positive.** `SINGLE MAKER` and `2 MAKERS, SEPARATE ARTEFACTS`.
**PP caution.** `SMALL TEAM, SHARED ARTEFACTS` — the isolation gap is structural and the retrofit is manual.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-076, DC-D-082, DC-D-011, DC-D-110, DC-D-007.
**Related anti-patterns.** AP-D-042, AP-D-041.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `alm-devops.md` ALM-06, ALM-23, ALM-A5, §2, §4 rows 3, 12; `application-architecture.md` AA-03, AA-06, AA-C1, U-A1, §2; `platform-suitability.md` PS-06.

---

#### DC-D-079 — Separation of duties between build and deploy

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the person who builds may deploy to production, and whether an approval is required in between.

**Why it matters.** The mechanism designed for this is **delegated deployment with a service principal**, and it has a hard prerequisite: that identity needs administrative rights in each target, because *"Lower permission security roles can't deploy plug-ins and other code components"* — making the deploying identity a **governed asset**. Manual deployment cannot satisfy separation of duties at all, and it additionally makes the **deployer the owner** of the deployed objects, which the corpus identifies as the upstream cause of ownerless applications. Security guidance is unambiguous on the related control: *"Don't allow maker permissions in test and production environments."*

**Discovery evidence.** Whether a compliance requirement mandates separation; who currently deploys; whether makers hold maker rights in production; whether an approval gate exists; whether a service identity exists and who owns it.

**States.** `NOT REQUIRED` · `APPROVAL REQUIRED` · `SEPARATION MANDATED` · `UNKNOWN`.

**Decision impact.** `SEPARATION MANDATED` → delegated deployment with a governed service identity, makers holding no maker rights in production, and production support via co-ownership on managed artefacts rather than edit rights. This also carries the promotion mechanism's own prerequisite: targets must be managed environments, hence premium-licensed.

**PP positive.** `NOT REQUIRED` and `APPROVAL REQUIRED` (approvals exist in the promotion tooling).
**PP caution.** `SEPARATION MANDATED` — the deploying identity becomes a privileged, owned asset with rights in every target.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-076, DC-D-082, DC-D-093, DC-D-062, DC-D-006.
**Related anti-patterns.** AP-D-043, AP-D-041, AP-D-032.
**Related alternatives.** ALT-004.
**Lineage.** `alm-devops.md` ALM-11, ALM-20, ALM-A6, ALM-A14, §2, §4 rows 5–6, ALM-U-07; `security.md` SEC-22, SEC-36, SEC-A14, SEC-A15, §4 row 17; `governance.md` GOV-14.

---

#### DC-D-080 — Reversibility requirement

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether a bad release must be undoable, how quickly, and by what mechanism.

**Why it matters. There is no solution rollback.** The three real options are redeploying a previous version (**only where that setting is enabled before it is needed**), restoring a backup, or fixing forward. Restore is **not** a rollback: it deletes solution automations in the target, invalidates every connection reference, changes application identifiers, loses broad sharing, returns the environment in administration mode, **cannot target production directly**, is same-region and managed-to-managed, requires free capacity, and **can take more than a day**. It also **rewinds one participant** while integrated systems and replicas retain later state, so a post-restore reconciliation step with a business sign-off owner is mandatory.

**Discovery evidence.** What the business expects if a release is bad; the acceptable time to recover; whether previous-version redeployment is enabled; whether a restore has ever been rehearsed and how long it took; whether integrated systems would need reconciliation.

**States.** `FIX FORWARD ACCEPTABLE` · `PREVIOUS-VERSION REDEPLOY REQUIRED` · `FULL RESTORE CAPABILITY REQUIRED` · `UNKNOWN`.

**Decision impact.** Name the mechanism, **enable it before go-live**, and rehearse it: what it destroys, who re-establishes connections and sharing, how long it takes, and what happens to integrated systems. Capacity headroom becomes a **recoverability requirement**, because overage blocks restore outright.
**Blocking.** `UNKNOWN` is decision-blocking for a business-critical release: the reversibility promise cannot be made without knowing which mechanism would honour it.

**PP positive.** `FIX FORWARD ACCEPTABLE`, and `PREVIOUS-VERSION REDEPLOY REQUIRED` with the setting enabled and tested.
**PP caution.** `FULL RESTORE CAPABILITY REQUIRED` — the side effects are extensive and the elapsed time is a day-scale unknown.
**PP negative/exit.** [`Xc`] none evidenced alone. An unrehearsed reversibility claim is the *no recovery drill* leg of the corpus's registered composed risk — `decision-intelligence-matrix.md` §3 row 4 (business- or mission-critical + no representative managed test environment + no recovery drill → the production commitment **cannot be evidenced**; `anti-patterns.md` AP-D-052).

**Related criteria.** DC-D-100, DC-D-077, DC-D-095, DC-D-083, DC-D-054.
**Related anti-patterns.** AP-D-045, AP-D-054, AP-D-052.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `alm-devops.md` ALM-18, ALM-A8, §2, §4 row 9, ALM-U-06, §14.4; `operations-support.md` OP-14, OP-17, OP-22, DC-05, DC-06, OP-AP-08, OP-U-03; `data-architecture.md` DA-18.

---

#### DC-D-081 — Automated-testing requirement

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether automated functional or regression testing is required, and at what depth.

**Why it matters.** There is **no supported first-party low-code functional-test framework** after the previous one's deprecation, so a functional harness is a **pro-code cost** (a browser-automation harness is the documented route) or a manual acceptance process with an **explicit regression-risk statement**. Static analysis is **not** a test gate: it *"doesn't guarantee that a solution import will be successful"* and is not a functional test. Also relevant: there is no documented unit-test mechanism for an automation definition, and the corpus leaves whether that is a platform gap or a knowledge gap as an open item.

**Discovery evidence.** Whether criticality mandates regression testing; whether a test capability exists; whether a browser-automation harness is in use elsewhere; whether manual acceptance is resourced; what the release cadence implies for regression effort.

**States.** `NONE` · `MANUAL ACCEPTANCE` · `AUTOMATED REGRESSION REQUIRED` · `FULL AUTOMATED SUITE REQUIRED` · `UNKNOWN`.

**Decision impact.** `AUTOMATED REGRESSION REQUIRED` and above → budget a pro-code harness in the option, or record the manual alternative **with its regression risk stated**. Match the validation level to the commitment being made (DC-D-089), and note that behaviour dependent on managed-environment, network or security controls must be tested where those controls exist.

**PP positive.** `NONE` and `MANUAL ACCEPTANCE` for the departmental class.
**PP caution.** `AUTOMATED REGRESSION REQUIRED` — an unfunded pro-code line, frequently omitted from the business case.
**PP negative/exit.** [`—`] none evidenced. Note the symmetry: a custom application also has to build its harness; the difference is that the tooling is conventional there.

**Related criteria.** DC-D-089, DC-D-001, DC-D-110, DC-D-077, DC-D-082.
**Related anti-patterns.** AP-D-052, AP-D-048.
**Related alternatives.** ALT-004, ALT-005.
**Lineage.** `alm-devops.md` ALM-16, ALM-17, ALM-A12, §4 row 11, §14.3, ALM-U-04; `platform-suitability.md` PS-53, §2 row 35; `automation-architecture.md` AT2-47, N-16, U-09; `performance-scale.md` PF-15, PF-20.

---

#### DC-D-082 — Environment count required by the lifecycle

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How many environments the delivery lifecycle needs, as distinct from those required for isolation or residency (DC-D-071).

**Why it matters.** The corpus records a real internal tension: basic lifecycle *"is possible with only development and production"*, yet *"at a minimum, any healthy ALM practice should include using a test environment"* — and a test environment is **structurally necessary**, because a managed solution's behaviour cannot be validated in the environment that authored it. Layered solutions need **dedicated development environments**; multiple makers need one each; and a further constraint binds region: a solution **cannot reliably be imported into an environment on an older service-update station**, so development must sit at or behind production's station. Every environment also carries the four cost axes of DC-D-071, and **promotion targets must be managed environments**.

**Discovery evidence.** Stages required; whether a test environment exists; whether layered solutions are planned; maker count; the service-update stations of the candidate regions; whether developer-plan environments are available.

**States.** `DEV AND PROD ONLY` · `DEV / TEST / PROD` · `PLUS UAT` · `PLUS PER-MAKER DEVELOPMENT` · `COMPLEX MULTI-STAGE` · `UNKNOWN`.

**Decision impact.** Include a test environment for anything above the departmental class. Keep development on developer-plan environments (free of capacity and managed obligations). Count the *managed* environments deliberately, since each carries premium licences for its active users. Check the service-update station relationship between development and production regions.

**PP positive.** `DEV / TEST / PROD` with development on developer-plan environments.
**PP caution.** `PLUS PER-MAKER DEVELOPMENT` and `COMPLEX MULTI-STAGE` — the cost axes compound; also the licence position of developer-plan environments used as promotion targets is an open item.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-071, DC-D-076, DC-D-078, DC-D-093, DC-D-033, DC-D-089.
**Related anti-patterns.** AP-D-037, AP-D-040, AP-D-041, AP-D-052.
**Related alternatives.** ALT-004.
**Lineage.** `alm-devops.md` ALM-02, ALM-06, ALM-08, ALM-25, §2, §4 rows 12–13, ALM-C2, ALM-C3, ALM-U-05; `licensing-cost.md` LC-25, DC-13; `governance.md` GOV-08; `operations-support.md` DC-15, OP-C-03.

---

#### DC-D-083 — Cross-boundary deployment coordination

**Domain:** ALM · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether the release unit spans more than one platform, and how the two sides' releases are sequenced and kept compatible.

**Why it matters.** A hybrid requires **two coordinated supply chains** — a solution pipeline **and** an infrastructure or code pipeline — with the release unit **declaring contract compatibility and sequencing**; deploying one side alone is admissible only under a guaranteed compatibility policy. The seam itself has documented mechanics: the connector needs a separate solution with an explicit import order, the low-code application artefact **does not recognise connection references**, and the documented workaround **can create an unmanaged layer** that conflicts with a production integrity control — which the corpus insists must be redesigned or exception-recorded rather than silently overridden. Compensation and reconciliation artefacts are **contract artefacts under equal change control**.

**Discovery evidence.** Whether the design has an external component; whether a pipeline exists on that side; who sequences the releases; whether the contract is versioned; whether backward compatibility is guaranteed.

**States.** `SINGLE PLATFORM` · `TWO PLATFORMS, INDEPENDENT AND COMPATIBLE` · `TWO PLATFORMS, COORDINATED RELEASES` · `TWO PLATFORMS, NO COORDINATION` · `UNKNOWN`.

**Decision impact.** `TWO PLATFORMS, NO COORDINATION` → the hybrid is **not available**; either fund and own the second pipeline or change the architecture. `TWO PLATFORMS, COORDINATED RELEASES` → declare sequencing and a compatibility policy, and treat the connector and interface contract as **one release boundary**.

**PP positive.** `SINGLE PLATFORM`, and `TWO PLATFORMS, INDEPENDENT AND COMPATIBLE` where compatibility is a designed property.
**PP caution.** The unmanaged-layer conflict — a real collision between a hybrid seam and a production integrity control.
**PP negative/exit.** [`—`] none as a platform exit; it is a **gate on hybrid options** (see DC-D-070).

**Related criteria.** DC-D-070, DC-D-046, DC-D-076, DC-D-080, DC-D-096.
**Related anti-patterns.** AP-D-046, AP-D-025, AP-D-026, AP-D-044.
**Related alternatives.** ALT-006, ALT-009, ALT-007.
**Lineage.** `alm-devops.md` ALM-14, §4 rows 8, 8a, §14.1, §14.2, §14.5; `architecture-patterns.md` §5.1 (deployment-maturity row), §13; `integration-architecture.md` I-07, IA-49, §12.7; `governance.md` GOV-XB-01.

---
### 4.9 Performance and scale

#### DC-D-084 — Interactive response-time requirement

**Domain:** Performance · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How quickly a user-facing action must complete, and what the business consequence of exceeding it is.

**Why it matters.** **No end-to-end latency figure is published for any path**, so a response-time commitment cannot be looked up — only measured. The bounds that *are* documented are timeouts, not targets: an application request ceiling with a retry count, and the synchronous windows of DC-D-050. Two client-side facts shape the design more than server behaviour: an aged but load-bearing recommendation of roughly 150 ms client latency, and the observation that on high-latency links (satellite round trips of several seconds) the binding constraint becomes the **number of round trips**, not per-call latency. Per-platform concurrent-request limits for mobile clients differ and are **unpublished**.

**Discovery evidence.** The acceptable response time per interaction, in seconds; where users are and on what networks; measured latency to the region from those locations; device mix; whether the requirement is contractual.

**States.** `TOLERANT (SECONDS)` · `RESPONSIVE (SUB-SECOND FOR COMMON ACTIONS)` · `STRICT` · `CONTRACTUAL` · `UNKNOWN`.

**Decision impact.** Measure latency **before** choosing the environment region. Design to minimise round-trip count rather than per-call time on poor networks. `CONTRACTUAL` or `STRICT` end-to-end across an application, an automation and an external system is **not sized anywhere in this corpus** and is an exit condition.

**PP positive.** `TOLERANT` and `RESPONSIVE` with delegable access paths and a designed payload.
**PP caution.** High-latency or mobile populations — acceptance must be tested on target devices, and the mobile concurrency figures are unpublished.
**PP negative/exit.** [`Xp`] **A hard sub-second, transactionally-visible end-to-end commitment → out of the platform**, or the commitment is renegotiated.

**Related criteria.** DC-D-042, DC-D-050, DC-D-023, DC-D-091, DC-D-015, DC-D-089.
**Related anti-patterns.** AP-D-048, AP-D-019, AP-D-050, AP-D-003.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `performance-scale.md` PF-04, PF-11, PF-12, PF-13, PF-14, DC-11, B-16, PF-U-01, PF-U-02, PF-U-09, §3.A rows 4, 10, §8.1 items 15–16; `automation-architecture.md` AT2-12; `platform-suitability.md` PS-28.

---

#### DC-D-085 — User concurrency

**Domain:** Performance · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How many people will use the solution simultaneously at peak.

**Why it matters. No concurrent-user figure is published for any surface**, anywhere in the corpus — checked across sixteen sources for the data layer and every fetched page for the application layer. The governing constraints are **not a headcount ceiling** but per-authenticated-user service protection, per-identity daily entitlement, and contention on shared records or identities. So the honest answer to "how many users can it take?" is a **load test against a production-like environment with realistic personas and data volumes** — and quoting a figure is a named anti-pattern in two areas. Two complications: full-scale load testing against the shared service is **constrained** (*"Limit tests to avoid unintended consequences"*), and a trial environment has **one web server**, so a proof of concept there measures a different platform.

**Discovery evidence.** Expected simultaneous users at peak; whether usage is bursty (shift changes, month-end); whether all users hit the same records; whether a load test is feasible and where.

**States.** `TENS` · `HUNDREDS` · `THOUSANDS` · `TENS OF THOUSANDS+` · `UNKNOWN`.

**Decision impact.** Do not quote a ceiling. Build confidence from **limit arithmetic plus a bounded pilot plus production throttling monitoring plus a degradation plan** (DC-D-089). Where all traffic reaches the data layer through **one** identity — a public surface or an integration identity — that concentration is the real constraint, and no application-side tuning changes it.
**Blocking.** `UNKNOWN` is decision-blocking at `THOUSANDS` and above, because neither sizing nor validation can be planned.

**PP positive.** `TENS` to `HUNDREDS` with delegable paths and distributed identities.
**PP caution.** `THOUSANDS+`, and any design concentrating traffic on one acting identity.
**PP negative/exit.** [`Cf`] none as a published ceiling — the exit is DC-D-089 (proof required but not obtainable), not a concurrency number.

**Related criteria.** DC-D-010, DC-D-086, DC-D-089, DC-D-030, DC-D-009.
**Related anti-patterns.** AP-D-051, AP-D-048, AP-D-052, AP-D-040.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `performance-scale.md` PF-09, PF-15, PF-16, PF-20, PF-25, PF-42, PF-AP-14, B-11, B-17, DC-04, DC-17, PF-U-01, PF-U-10, §8.1 items 5, 14, 17, PF-C-02, PF-C-03; `data-architecture.md` SC-16, SC-17, DAP-41, U-31; `application-architecture.md` AA-53, U-A1.

---

#### DC-D-086 — Request rate per acting identity

**Domain:** Performance · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** MEDIUM

**Definition.** The number of platform requests each acting identity generates per short window and per day, including the amplification the solution's own customisation adds.

**Why it matters.** This is normally the meter that binds, and it is the one licence conversations skip. Service protection is evaluated **per authenticated user, per web server, over a five-minute window** — and the web-server count is **undisclosed and licence-dependent**, so *effective* throughput is not a published number. The daily entitlement is a **separate** meter, and *"Batch operations aren't a valid strategy to bypass entitlement limits"*. Crucially, **amplification cannot be assumed**: the platform counts create-read-update-delete operations, assignment, sharing, *"user-driven and internal system requests required to complete CRUD transactions"*, server-side code, workflows and custom controls, plus **retries and pagination** — but publishes **no multiplier**, because it is a property of each solution's own customisation. Quoting one from memory or another engagement is a named anti-pattern. The volatility is twofold: the published figures are transition-period tolerances with **no announced enforcement date**, and the concurrency default *"might be higher"* per environment.

**Discovery evidence.** Business transactions per identity per five minutes at peak; a **measured** amplification factor from a prototype (the corpus names the instrumentation); whether reporting runs on the same identities; whether one integration identity carries everything.

**States.** `WELL INSIDE` · `APPROACHING` · `EXCEEDS PER-IDENTITY BUDGET` · `SINGLE-IDENTITY CONCENTRATION` · `UNKNOWN`.

**Decision impact.** Above the budget: distribute across identities (a documented mitigation with a real identity-management cost), or **move the data leg to the service-protection-exempt in-platform mechanism** — the corpus's *"highest-leverage documented remedy"*. Never size from the daily entitlement alone. Drive concurrency from the runtime hint the service returns rather than a hard-coded value. Design a back-off-driven busy state as a **functional** requirement.

**PP positive.** `WELL INSIDE` with a measured amplification factor.
**PP caution.** `SINGLE-IDENTITY CONCENTRATION` — one identity is one budget regardless of user count.
**PP negative/exit.** [`Cf`] none as a platform exit; combines with DC-D-040 to produce the integration exit.
**Blocking.** `UNKNOWN` amplification is decision-blocking for any volume-sensitive design — it must be **measured**, not assumed.

**Related criteria.** DC-D-039, DC-D-040, DC-D-085, DC-D-031, DC-D-093, DC-D-095.
**Related anti-patterns.** AP-D-049, AP-D-051, AP-D-016, AP-D-055.
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `performance-scale.md` §2, PF-22, PF-29, PF-30, PF-45, PF-46, DC-03, DC-19, B-03, B-09, PF-U-10, §8.1 items 4, 6–7, 19, 44, PF-C-01; `data-architecture.md` SC-01, SC-02, SC-21, DA-10, DAP-42, U-29, U-33, U-32; `automation-architecture.md` AT2-02, AT2-03, N-03; `licensing-cost.md` LC-09, §7.2 items 23–28.

---

#### DC-D-087 — Peak load shape and growth horizon

**Domain:** Performance · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The shape of peak demand, the growth expected over the investment horizon, and the point at which the design would have to change.

**Why it matters.** The corpus's instruction is to size against **year-three volume and the peak, not today's average**, and — more importantly — to *"Identify the **reachable limit** and the redesign trigger before it is hit"*, anchored to the vendor's own statement that *"For every system, there's a limit to how much you can scale it without redesigning, introducing a workaround, or incorporating human involvement"*. Cost has the mirror requirement: capacity notifications begin only when headroom is low, and one metered audience type **does not carry capacity forward month to month**, so *the peak month is the month that counts*. Over- and under-provisioning are both named as costs.

**Discovery evidence.** Peak-to-average ratio; when peaks occur; growth rate with a stated basis; the volume at which the current design would break; whether a seasonal or event-driven spike exists.

**States.** `FLAT AND STABLE` · `PREDICTABLE SEASONAL PEAK` · `EVENT-DRIVEN SPIKES` · `HIGH GROWTH` · `UNKNOWN`.

**Decision impact.** Size at the peak and the horizon; **record the redesign trigger** as a tripwire with an owner. `EVENT-DRIVEN SPIKES` → brokered load levelling with bounded consumers. `HIGH GROWTH` → the reachable limit is likely to be crossed inside the horizon, which legitimises building for it now with the forecast recorded as the justification.
**Blocking.** `UNKNOWN` is decision-blocking — it is the *"scale anxiety without a number"* case, and the corpus rejects both leaving and staying on that basis.

**PP positive.** `FLAT AND STABLE` and `PREDICTABLE SEASONAL PEAK` inside the envelope at horizon.
**PP caution.** `HIGH GROWTH` — capacity, entitlement and meter headroom all shrink together.
**PP negative/exit.** [`Cf`] none from growth alone; it moves DC-D-040 and DC-D-023 across their thresholds.

**Related criteria.** DC-D-024, DC-D-037, DC-D-040, DC-D-086, DC-D-095, DC-D-004.
**Related anti-patterns.** AP-D-049, AP-D-063, AP-D-006 (de-escalation when growth never arrives).
**Related alternatives.** ALT-006, ALT-009.
**Lineage.** `performance-scale.md` PF-47, DC-20, §8.1 item 39, §11.1 (capacity misjudgement); `licensing-cost.md` LC-AP-07, DC-04, §7.2 items 17–18; `integration-architecture.md` IA-01, §2.1 row 1.

---

#### DC-D-088 — Record count per access path at horizon

**Domain:** Performance · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** For each access path — screen, query, view, retrieval — the number of records it must reason over at year three, and the traversal depth it requires.

**Why it matters.** It is the operational form of DC-D-023, expressed per path rather than per store, and it carries two additional documented ceilings: **traversal depth** (at most two lookup levels, one offline; around twenty expanded entities per query) and, on the document/list store, a query threshold beyond which retrieval **fails** unless an indexed, selective filter exists — with the vendor stating *"the LVT limit can't be changed"*, which makes indexable access paths a design constraint. The corpus also notes that **all defined columns are returned even when unused** on that store, making column count a performance parameter of every read.

**Discovery evidence.** Per path: records considered at horizon, traversal depth, whether a selective indexable filter exists, column count on the retrieved entity.

**States.** `SHALLOW AND SMALL` · `SHALLOW AND LARGE` · `DEEP AND SMALL` · `DEEP AND LARGE` · `UNKNOWN`.

**Decision impact.** `DEEP` → server-side views, a flattened model, or a different surface; and offline is a **stricter, separate** constraint. `SHALLOW AND LARGE` → delegable expressions or server-side shaping. `DEEP AND LARGE` → the access path must be redesigned before the store is chosen.

**PP positive.** `SHALLOW AND SMALL`, and `SHALLOW AND LARGE` with delegable paths on the governed store.
**PP caution.** `DEEP` anywhere, and any path on the document/list store without an indexable selective filter.
**PP negative/exit.** [`Ri`] none evidenced. **In-platform redirect:** `DEEP` → server-side views, a flattened model, or a different surface; `DEEP AND LARGE` → the access path is redesigned before the store is chosen. A store, model or surface change, not a platform change.

**Related criteria.** DC-D-023, DC-D-022, DC-D-016, DC-D-031, DC-D-024.
**Related anti-patterns.** AP-D-050, AP-D-008.
**Related alternatives.** ALT-003, ALT-004, ALT-005.
**Lineage.** `performance-scale.md` PF-01, PF-02, PF-03, DC-01, DC-02, B-02, §3.A rows 1–3, §3.B row 11, §8.1 items 3, 38–39; `data-architecture.md` DA-39, DA-40, §2 rows 1–2, §3.

---

#### DC-D-089 — Provability of capacity before commitment

**Domain:** Performance · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether peak capacity must be **proven** before go-live, and by what evidence — and whether that evidence is obtainable.

**Why it matters.** This is the criterion that turns the corpus's central reservation into a decision. Manifest **NB-07**: the corpus is **limits-based, not benchmark-based**, and documented limits are *"exclusion/envelope evidence only"*. Full-scale load testing against the shared service is **constrained** (*"Limit tests to avoid unintended consequences"*), which sits in tension with the guidance to test in a production-like environment under stress — a conflict the corpus records rather than resolves. So peak confidence comes from **limit arithmetic plus a bounded pilot plus production throttling monitoring plus a degradation plan**, and the corpus states the consequence directly: *"If proof is existential, host the peak-bearing component elsewhere."* Fidelity also matters: a test environment cannot mirror production if production is a managed environment and the test one is not, and a trial environment has a single web server.

**Discovery evidence.** Whether a contract or a sponsor requires proof; what evidence would satisfy them; whether a production-like environment of the right class is available; whether a bounded pilot is fundable; whether a degradation plan is acceptable.

**States.** `NOT REQUIRED` · `LIMIT ARITHMETIC SUFFICES` · `BOUNDED PILOT REQUIRED` · `FULL LOAD PROOF REQUIRED` · `UNKNOWN`.

**Decision impact.** State the required **validation level** per commitment and budget it (V1 limits, V2 bounded pilot with monitoring, V3 pro-code harness, V4 managed-test fidelity). Where the required level cannot be reached, the corpus's composed disqualifier applies: *"Production commitment cannot be evidenced; do not encode 'ready' from limits alone."*

**PP positive.** `NOT REQUIRED` and `LIMIT ARITHMETIC SUFFICES`; `BOUNDED PILOT REQUIRED` where a representative environment of the right class exists.
**PP caution.** `BOUNDED PILOT REQUIRED` without a managed test environment when production is managed — the fidelity gap is documented.
**PP negative/exit.** [`Xr`] **`FULL LOAD PROOF REQUIRED` where testing against the service is constrained → host the peak-bearing component where load testing is permitted.**

**Related criteria.** DC-D-085, DC-D-086, DC-D-040, DC-D-081, DC-D-082, DC-D-101.
**Related anti-patterns.** AP-D-048, AP-D-052, AP-D-051, AP-D-040, AP-D-059.
**Related alternatives.** ALT-005, ALT-006, ALT-009.
**Lineage.** `performance-scale.md` PF-15, PF-20, DC-17, B-17, PF-U-01, PF-C-03, §8.1 items 5, 17, §8.3; `alm-devops.md` §14.3; `operations-support.md` OP-C-03, §13.5; `architecture-patterns.md` §13 (validation contract); manifest NB-07.

---

#### DC-D-090 — In-region availability requirement

**Domain:** Performance · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The availability the solution requires within a single region, and whether zone-level redundancy suffices.

**Why it matters.** This is the criterion where the platform is **strongest and requires no extra architecture**: production environments carry availability-zone redundancy with a recovery point *"approximately near zero"* and a recovery time *"under five minutes"*, automatically. Two boundaries qualify it: **non-production environment types get none of these guarantees** (*"don't deploy production processes and data in nonproduction types"*), and the platform's data service documents a **99.9% uptime commitment** which is **not** the solution's availability (DC-D-091). One caveat the corpus keeps open: whether a given tenant's region is on the zone architecture is unverified per tenant, with a rollout caveat recorded.

**Discovery evidence.** The stated availability requirement; whether it is contractual; the environment type in use; whether the region's zone status has been confirmed; whether the requirement is per business flow or per platform.

**States.** `BEST EFFORT` · `99.9% ACCEPTABLE` · `ABOVE 99.9%` · `CONTRACTUAL COMMITMENT` · `UNKNOWN`.

**Decision impact.** `99.9% ACCEPTABLE` → single-region zone redundancy needs **no extra architecture**, provided the environment is a production type. `ABOVE 99.9%` or `CONTRACTUAL` → construct the position per business flow from every dependency (DC-D-091), and confirm the tenant's region status.

**PP positive.** `BEST EFFORT` and `99.9% ACCEPTABLE` on a production environment type.
**PP caution.** `ABOVE 99.9%` — no platform commitment exists above it, and the composite figure is what matters.
**PP negative/exit.** [`Cf`] none from in-region availability alone; the exits are in DC-D-091 and DC-D-100.

**Related criteria.** DC-D-091, DC-D-100, DC-D-001, DC-D-071, DC-D-033.
**Related anti-patterns.** AP-D-040, AP-D-056, AP-D-054.
**Related alternatives.** ALT-004, ALT-005, ALT-006.
**Lineage.** `performance-scale.md` PF-39, DC-13, B-06, §3.D rows 31–33, §8.1 item 36, PF-AP-17; `platform-suitability.md` PS-37, C-9, U-12b, §2 row 21; `operations-support.md` OP-20, DC-15, OP-U-01; `security.md` "Cross-block availability boundary".

---

#### DC-D-091 — End-to-end availability of the composed flow

**Domain:** Performance · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The availability the **business flow** requires end to end, and the availability of the **weakest dependency on its path** — including the parts the customer operates.

**Why it matters.** Manifest **NB-03**: platform service availability **does not equal an end-to-end contractual solution availability**, and dependency and contractual scope are engagement-specific. The corpus is specific about what falls outside the platform's commitments: external-system recovery objectives are *"explicitly outside"* them; the commitments *"stop at the platform boundary"*, with several adjacent services **not covered**; and the governing figure is the **weakest link including the parts the customer operates** — a gateway host being one, with the vendor stating it *"doesn't investigate poor performance when a gateway … is overloaded"*. Its instruction is procedural: **rate each flow, analyse failure modes per flow, and record the weakest dependency as that flow's real objective.**

**Discovery evidence.** Per business flow: every dependency on its path, and each one's documented or measured availability; which are customer-operated; which are third-party; whether a composite figure has been calculated; whether a commitment has already been made.

**States.** `NO COMMITMENT` · `INTERNAL TARGET` · `CONTRACTUAL, PLATFORM-ONLY DEPENDENCIES` · `CONTRACTUAL, EXTERNAL DEPENDENCIES` · `UNKNOWN`.

**Decision impact.** Compute per flow, not per platform. `CONTRACTUAL, EXTERNAL DEPENDENCIES` → the commitment must be constructed from parsed service terms plus each dependency's position plus the customer's own drill evidence — **or the commitment must change**. Introducing a customer-operated component **converts a SaaS availability profile into an operated one**, and that cost belongs in the option.
**Blocking.** `UNKNOWN` is decision-blocking wherever a commitment is being made.

**PP positive.** `NO COMMITMENT` and `INTERNAL TARGET`; `CONTRACTUAL, PLATFORM-ONLY DEPENDENCIES` with the applicable terms parsed.
**PP caution.** Every additional synchronous hop or customer-operated component lowers the composite figure.
**PP negative/exit.** [`Xp`] **A contractual end-to-end commitment the composite path cannot support → the commitment is met by an architecture whose availability the customer controls, or it changes.**

**Related criteria.** DC-D-090, DC-D-100, DC-D-042, DC-D-044, DC-D-096, DC-D-102.
**Related anti-patterns.** AP-D-056, AP-D-019, AP-D-026, AP-D-054.
**Related alternatives.** ALT-005, ALT-006, ALT-007, ALT-009.
**Lineage.** `performance-scale.md` PF-40, PF-44, DC-13, §3.D row 37, §8.1 items 32–33; `operations-support.md` OP-19, DC-08, §6.3, OP-U-01; `integration-architecture.md` IA-27, IA-28, §2.1 row 10, §7 item 28; `architecture-patterns.md` §3.1 (availability row); `security.md` "Cross-block availability boundary"; manifest NB-03.

---

### 4.10 Cost

#### DC-D-092 — Budget envelope and funding model

**Domain:** Cost · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The approved budget, whether it is capital or operational, whether it is recurring, and who owns it.

**Why it matters.** Budget is a **hard constraint that can disqualify an option outright**, and the corpus says so in its most pointed form: where a mandated security control's licence population is unfunded, *"the option is economically infeasible rather than 'secure by configuration'"* — and *"Never remove a required security control merely to make the Power Platform option look cheaper."* It also appears as a first-class selection input: budget *"forces escalation / disqualifies when security prerequisites, premium audience, broker/API/worker, telemetry/support or external platform team exceed the approved TCO"*.

**Discovery evidence.** The approved figure and its basis; capital versus operational; whether recurring cost is funded beyond year one; who owns the budget; whether an unfunded gap can be escalated.

**States.** `UNCONSTRAINED` · `DEFINED AND ADEQUATE` · `DEFINED AND TIGHT` · `LICENCE-ONLY FUNDING` · `UNKNOWN`.

**Decision impact.** `LICENCE-ONLY FUNDING` is a red flag in itself, because at least eleven other cost lines exist. `DEFINED AND TIGHT` → reduce scope, use existing entitlement only, or select a different option class — **not** a degraded design presented as equivalent. Where a required control is unfunded, escalate the gap as a sponsor decision.
**Blocking.** `UNKNOWN` is decision-blocking: option comparison is meaningless without it.

**PP positive.** `DEFINED AND ADEQUATE` where the requirement sits inside existing entitlement.
**PP caution.** `DEFINED AND TIGHT` with a criticality class that pulls in the managed-environment chain — the step change can invert the case.
**PP negative/exit.** [`Xe`] **Budget inadequate for the mandated controls or the required audience → the option is infeasible.** Also: process change or do-nothing may be the correct answer (DC-D-008).

**Related criteria.** DC-D-008, DC-D-093 … DC-D-099, DC-D-063, DC-D-064.
**Related anti-patterns.** AP-D-060, AP-D-061, AP-D-064, AP-D-039.
**Related alternatives.** ALT-002, ALT-010, ALT-001, ALT-003.
**Lineage.** `licensing-cost.md` LC-21, LC-30, LC-28, §6, §2.5; `architecture-patterns.md` §5.1 (budget row), §13; `security.md` SEC-XB-01; `governance.md` GOV-XB-03.

---

#### DC-D-093 — Entitlement fit of the required capability set

**Domain:** Cost · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** HIGH

**Definition.** Whether the capabilities the design requires fall inside the entitlement the audience already holds, or require standalone entitlement for the whole population.

**Why it matters.** **The licence boundary is a fit boundary.** Seeded productivity rights cover standard connectors and the team-scoped store only; premium and custom connectors, on-premises and cloud data transfer, the full governed store, the record-centric application type, external-facing sites and the managed environment class **all** require standalone entitlement for **every active user** — and **multiplexing is prohibited**, with a documented right of suspension for consumption above entitlement. So a single connector decision can move the entire population from seeded to paid. Two honesty notes: the general documentation is **not authoritative on licensing** (every page defers to the licensing guide and the customer's agreement), and whether **one** premium connector obliges premium entitlement for **every** user of the artefact is an open item — stated categorically by independent sources, consistent with the vendor's entitlement statements, not verbatim-confirmed. It is load-bearing and must be verified per engagement.

**Discovery evidence.** The connector and capability list the design requires; the audience size; current entitlement holdings; whether the licensing guide and the customer agreement have been read by a named owner; whether a standard-connector path exists that meets the requirement.

**States.** `INSIDE EXISTING ENTITLEMENT` · `PREMIUM FOR A SUBSET` · `PREMIUM FOR THE WHOLE AUDIENCE` · `PLUS EXTERNAL PREREQUISITES` · `UNKNOWN`.

**Decision impact.** Establish the tier at **design time, on the whole audience**. Where a standard path meets the requirement the saving is population-wide; where it does not, the premium cost belongs in that option's economics **from the first comparison**. Route entitlement questions to the authoritative document and the customer's agreement with a **named owner**, and carry a validation action.
**Blocking.** `UNKNOWN` is decision-blocking: the option cannot be priced, and the corpus's largest cost finding depends on it.

**PP positive.** `INSIDE EXISTING ENTITLEMENT`, verified rather than assumed.
**PP caution.** `PREMIUM FOR THE WHOLE AUDIENCE` — a step change, and the commonest late discovery.
**PP negative/exit.** [`Xe`] `PLUS EXTERNAL PREREQUISITES` with an unfunded population → economically infeasible (DC-D-092).

**Related criteria.** DC-D-092, DC-D-094, DC-D-010, DC-D-035, DC-D-063, DC-D-064, DC-D-071.
**Related anti-patterns.** AP-D-062, AP-D-061, AP-D-064, AP-D-060.
**Related alternatives.** ALT-003, ALT-004, ALT-005, ALT-008.
**Lineage.** `licensing-cost.md` LC-02, LC-03, DC-01, DC-02, DC-03, LC-C-05, LC-U-02, LC-U-05, §7.1 items 2–4, §7.3 items 49–50; `platform-suitability.md` PS-26, PS-33, PS-36, PS-42, §2 rows 9, 22; `governance.md` GOV-06, GOV-11, GOV-18; `security.md` SEC-XB-01.

---

#### DC-D-094 — Audience and frequency shape

**Domain:** Cost · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** MEDIUM

**Definition.** The relationship between how many people use the solution and how often each of them interacts — which selects among the platform's five economic mechanisms.

**Why it matters.** The corpus reduces the licensing question to two: *"**Who** needs the capability — a fixed team, a whole workforce, or an unpredictable external population?"* and *"**What is the shape of the demand** — steady per-person daily use, or bursty/seasonal/long-tail use?"* Its documented rule: **many users × few interactions → consumption; few users × many interactions → prepaid; unknown adoption → consumption first, true up later**. Two metering traps: external anonymous uniqueness is **a browser cookie**, so the meter **over-counts** multi-device and cookie-clearing users (and an availability monitor with a browser user agent bills itself as traffic); and authenticated uniqueness is the **contact record**, so contact duplication is a billing defect.

**Discovery evidence.** Population and interaction frequency per person; whether adoption is predictable; whether the audience is external or anonymous; whether a multi-device or cookie-churn multiplier should be applied; whether a monitoring endpoint would be counted.

**States.** `SMALL POPULATION, HIGH FREQUENCY` · `LARGE POPULATION, LOW FREQUENCY` · `LARGE AND HIGH FREQUENCY` · `UNPREDICTABLE / EXTERNAL` · `UNKNOWN`.

**Decision impact.** Select the mechanism from the shape, not from habit. Forecast external audiences with an **explicit cookie-churn and multi-device multiplier**, and configure availability monitoring per the documented non-browser method. Note the corpus's retained hypothesis: the **users-to-work ratio** may be a useful crossover criterion against consumption-metered alternatives — labelled a hypothesis, not a finding.

**PP positive.** `SMALL POPULATION, HIGH FREQUENCY` on prepaid entitlement; `LARGE POPULATION, LOW FREQUENCY` on consumption.
**PP caution.** `UNPREDICTABLE / EXTERNAL` — the meter's unit is not a person.
**PP negative/exit.** [`—`] none as an exit; it is the input to the economic comparison of `alternatives.md` §5.2.

**Related criteria.** DC-D-010, DC-D-009, DC-D-093, DC-D-092, DC-D-087.
**Related anti-patterns.** AP-D-060, AP-D-063, AP-D-062.
**Related alternatives.** ALT-005, ALT-006, ALT-008, ALT-004.
**Lineage.** `licensing-cost.md` §1, DC-02, DC-05, DC-06, LC-04, LC-12, LC-18, LC-19, LC-20, LC-AP-11, §6, §7.2 items 19–21.

---

#### DC-D-095 — Capacity consumption profile

**Domain:** Cost · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** HIGH

**Definition.** How much stored capacity the solution will consume across each separately-metered type, and how that grows.

**Why it matters.** The failure mode is **not a bill, it is a block**: overage *"blocks environment create, copy, restore, recover and Dataverse-add"*, so capacity is a **recoverability** requirement. Several growth vectors are unfunded or invisible: **no user entitlement accrues log capacity**, yet audit consumes it; the search index bills at the **most expensive** rate and turning it off is effectively irreversible within a short window with a multi-day reindex; **every environment consumes a floor** regardless of database; borrowing between capacity types is **one-directional**; analytical replication bills as platform database storage and *"can double or triple your storage footprint"* with **no published ratio**; and regional resilience consumes a **second full copy** from the same pool. Notifications begin only when headroom is already low.

**Discovery evidence.** Projected volume per capacity type at horizon; audit scope; whether search is in use; environment count; whether analytical replication or regional resilience is planned; current tenant headroom and its owner.

**States.** `WELL WITHIN` · `APPROACHING THRESHOLDS` · `REQUIRES ADD-ON` · `AT RISK OF BLOCKING OPERATIONS` · `UNKNOWN`.

**Decision impact.** Model each meter separately; put binaries on the cheap meter; scope audit deliberately at creation; name a **tenant-level capacity owner**; treat a minimum free headroom as a **standing precondition** for recoverability. Note that add-ons **could not be assigned during the transition period** while the vendor recommended buying them anyway — a dated commercial artefact to re-check.
**Blocking.** `UNKNOWN` risks a recoverability failure discovered during an incident.

**PP positive.** `WELL WITHIN` with a funded model and lifecycle jobs.
**PP caution.** `APPROACHING THRESHOLDS` — administrative operations degrade before anything user-visible does.
**PP negative/exit.** [`—`] none evidenced.

**Related criteria.** DC-D-024, DC-D-025, DC-D-027, DC-D-031, DC-D-032, DC-D-071, DC-D-100.
**Related anti-patterns.** AP-D-063, AP-D-054, AP-D-037, AP-D-009.
**Related alternatives.** ALT-003, ALT-006, ALT-009.
**Lineage.** `licensing-cost.md` LC-05, LC-10, LC-11, LC-24, DC-04, DC-12, LC-AP-03, LC-AP-05, LC-AP-07, LC-AP-14, §7.2 items 11–18, 27, 37; `operations-support.md` OP-22, DC-17, OP-U-04; `data-architecture.md` DA-14, DA-19, DA-62, U-01.

---

#### DC-D-096 — External and hybrid service consumption cost

**Domain:** Cost · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** MEDIUM

**Definition.** The cost of every non-platform component the architecture introduces — brokers, mediation tiers, workers, gateway hosts, networking, monitoring ingestion and retention — plus its administration.

**Why it matters.** The corpus's named failure is evaluating a hybrid **on the platform cost alone**; its comparison method requires the *"external estate"* dimension explicitly, because hybrid patterns *"import Azure/on-premises consumption and administration"*. Concrete unpriced lines it names: the gateway estate at required scale (an open item), monitoring ingestion and retention (*"There are cost implications for storing and querying logs"*, and *"Logic monitoring tools are likely to increase costs"*), a mediation tier whose **tier choice locks in network and availability capabilities**, and the skills commitment described as *"well beyond a Power Platform app"*.

**Discovery evidence.** The external component list; each one's consumption driver and volume; whether a subscription and a cost owner exist; monitoring volume and retention; host infrastructure for any customer-operated component.

**States.** Anchored **relatively**, against the option's own total cost of ownership — a relative anchor requires no invented threshold and survives price changes. `NONE` (no external component) · `MINOR` (the external estate is a rounding item against the option's total) · `MATERIAL` (the external estate is a line the sponsor must see and fund separately, and a named cost owner in the other domain is a precondition) · `DOMINANT` (the external estate exceeds the platform line, at which point the option is a cloud-native architecture with a low-code front end and should be evaluated as ALT-006 rather than as ALT-009) · `UNKNOWN`.

**Decision impact.** Price the external estate as a first-class line with a **named cost owner in the other domain**; where no cost owner exists, the hybrid option is not fundable — which converges with DC-D-070's gate from the governance side.

**PP positive.** `NONE` — a single-platform option, which is why the corpus treats "no second estate" as a genuine advantage.
**PP caution.** `MATERIAL` — the corpus can name these lines but not price them, so the engagement must.
**PP negative/exit.** [`—`] none as an exit; it can make a hybrid option uneconomic, which is a different finding.

**Related criteria.** DC-D-070, DC-D-083, DC-D-101, DC-D-092, DC-D-044, DC-D-057.
**Related anti-patterns.** AP-D-060, AP-D-026, AP-D-046.
**Related alternatives.** ALT-006, ALT-009, ALT-005.
**Lineage.** `licensing-cost.md` §6 (external estate, observability/support rows), LC-21, LC-U-06, §7.4; `automation-architecture.md` AT2-53, N-51, N-52; `performance-scale.md` §11.1; `architecture-patterns.md` AP-10 (weaknesses), §5.1; `integration-architecture.md` §7 items 28–30.

---

#### DC-D-097 — Operational and support cost tier

**Domain:** Cost · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The recurring cost of operating and supporting the solution: support plan tier, monitoring, on-call, the operational feature set's licence prerequisites, and drills.

**Why it matters.** These are the lines a licence-only case omits, and they are **derived from criticality rather than from size**. A support plan is a **separate purchase** and the right to open a ticket depends on holding one; the operational feature set (telemetry export, extended backup, regional resilience, pipelines, network isolation) sits behind the managed environment class, i.e. **premium entitlement for every active user of that environment**. The corpus's chain is *criticality → operational requirements → managed environment → premium licences*, and its conclusion is that *"a departmental solution becomes expensive the day it matters."* Testing, separate environments and drills are all named as costs.

**Discovery evidence.** The criticality class; the support tier implied by it; whether a support plan is held; monitoring volume and retention; whether drills are required and resourced; whether an on-call rota exists.

**States.** `NONE BUDGETED` · `BASIC` · `BUSINESS-CRITICAL TIER` · `MISSION-CRITICAL TIER` · `UNKNOWN`.

**Decision impact.** Derive the tier from **criticality, not from licence count**, and put it in the option's economics during option selection. Where the operational tier is unfunded but the criticality is real, the honest outputs are a reduced criticality commitment, a different option class, or an escalated funding gap.

**PP positive.** `BASIC` for a departmental workload.
**PP caution.** `BUSINESS-CRITICAL TIER` — the managed-environment chain is where the step change happens.
**PP negative/exit.** [`Xe`] **Criticality requiring an operational tier the budget cannot fund → the option is economically unattractive**; and avoiding the tier to save cost forfeits *"the means of diagnosing and recovering from incidents"*, so *"the saving returns as outage duration."*

**Related criteria.** DC-D-001, DC-D-101, DC-D-102, DC-D-092, DC-D-093, DC-D-104.
**Related anti-patterns.** AP-D-060, AP-D-061, AP-D-064, AP-D-053.
**Related alternatives.** ALT-011, ALT-001, ALT-010, ALT-004.
**Lineage.** `licensing-cost.md` LC-22, LC-23, LC-26, LC-AP-04, LC-AP-10, DC-11, §2.5, §7.2 items 34–39, 46; `operations-support.md` OP-21, OP-24, DC-13, DC-16, §1.1; `performance-scale.md` §11.1.

---

#### DC-D-098 — Migration and exit cost

**Domain:** Cost · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The cost of getting data and behaviour **into** the solution, and the cost of getting **out** of it later.

**Why it matters.** The corpus makes exit an explicit cost dimension — *"exit/option value: migration/rewriting cost and lock-in constraints… future switching cost belongs in TCO where portability matters"* — and supplies the asymmetry that makes it calculable: **data and server-side .NET components are portable; the interface, the expression language and the automations are not**. It also names the specific traps: a deliberately-cheap starting point's migration cost is part of technical debt, and one team-scoped tier's **export to a full environment *"is not yet available"***, so its exit may be a **rebuild**.

**Discovery evidence.** Migration volume and quality (DC-D-034); whether an exit is foreseeable; what would have to be rewritten; whether the current tier has a documented export path; whether a decommissioning of the source is planned.

**States.** `LOW BOTH WAYS` · `MIGRATION-HEAVY` · `EXIT-HEAVY` · `HIGH BOTH WAYS` · `UNKNOWN`.

**Decision impact.** Price both directions. Where portability matters (DC-D-105), the non-portable layers are the exit cost and belong in the comparison. Where the starting tier has no export path, the exit is a rebuild and must be stated as such.

**PP positive.** `LOW BOTH WAYS`.
**PP caution.** `EXIT-HEAVY` where a portability requirement exists but has not been priced.
**PP negative/exit.** [`Cf`] none as an exit; it feeds DC-D-105 and DC-D-106.

**Related criteria.** DC-D-034, DC-D-105, DC-D-106, DC-D-092, DC-D-004, DC-D-065.
**Related anti-patterns.** AP-D-065, AP-D-060, AP-D-058.
**Related alternatives.** ALT-005, ALT-008, ALT-011.
**Lineage.** `licensing-cost.md` §6 (exit/option value), LC-14, LC-29, LC-AP-09, §7.2 items 31–32; `platform-suitability.md` PS-51, §2 row 32; `data-architecture.md` DA-43; `application-architecture.md` AA-50.

---

#### DC-D-099 — Cost attribution requirement

**Domain:** Cost · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether cost must be attributed to specific business units, cost centres or projects.

**Why it matters.** The corpus records **one documented attribution mechanism** — consumption billing policies scoped **per environment** and surfaced as a cloud resource with resource groups and tags — and notes that *"This is the only documented cost-attribution mechanism. It couples cost allocation to environment topology."* So an attribution requirement becomes an **environment-topology** requirement. Two cautions: enabling consumption billing **silently ignores** prepaid capacity assigned to that environment (so audit prepaid holdings first, or pay twice), and the tenant-level shared request pool has **no project-level view at all**, which the corpus records as an open item.

**Discovery evidence.** Whether chargeback or showback is required; the granularity demanded; whether prepaid capacity is already assigned to the candidate environments; who owns the tenant pool.

**States.** `NOT REQUIRED` · `SHOWBACK` · `CHARGEBACK BY BUSINESS UNIT` · `PER-PROJECT CHARGEBACK` · `UNKNOWN`.

**Decision impact.** Align billing policies to the business units that carry cost, which means aligning the **environment topology** to them (DC-D-071). Audit prepaid capacity before enabling consumption billing. `PER-PROJECT CHARGEBACK` for shared tenant-level consumption is **not achievable** with the documented mechanisms — state that rather than promising it.

**PP positive.** `NOT REQUIRED` and `SHOWBACK`.
**PP caution.** `CHARGEBACK BY BUSINESS UNIT` — it couples finance to environment design, which is otherwise decided on governance grounds.
**PP negative/exit.** [`—`] none evidenced; `PER-PROJECT CHARGEBACK` of shared pools is an unmet requirement to record.

**Related criteria.** DC-D-071, DC-D-095, DC-D-092, DC-D-006.
**Related anti-patterns.** AP-D-063, AP-D-037.
**Related alternatives.** ALT-004, ALT-006.
**Lineage.** `licensing-cost.md` LC-16, DC-14 (attribution variant — see §1.1), LC-AP-08, §7.2 items 22, 25, LC-U-10; `operations-support.md` DC-17, OP-U-05; `governance.md` GOV-XB-03.

---
### 4.11 Operations

#### DC-D-100 — Recovery point and recovery time objective

**Domain:** Operations · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How much data loss is acceptable, how quickly service must be restored, and whether the objective must survive the loss of a whole region.

**Why it matters.** In-region the platform is strong and automatic (recovery point *"approximately near zero"*, recovery time *"under five minutes"*). Cross-region is a different proposition entirely: **opt-in**, production-type only, **managed-environment-gated**, **doubles storage consumption** from the tenant pool, takes up to 48 hours to enable, **degrades high-volume automation throughput**, has **no published recovery-time commitment**, has **no prescriptive test plan**, permits **no deployments while failed over**, several geographies have **no option at all**, and a set of adjacent services is **not covered**. Backups are not an archive (7 days, 28 only for a production managed environment, **trial not backed up at all**, same-region, not downloadable), restore **cannot target production directly** and **can take more than a day**, capacity overage **blocks it**, and only artefacts **in solutions** are covered. And a restore **rewinds one participant** while integrated systems retain later state.

**Discovery evidence.** The stated objectives per business flow, and their source; whether they are contractual; whether a drill has ever been run and how long it took; whether the geography has a regional pair; which artefacts are in solutions; current capacity headroom.

**States.** `BEST EFFORT` · `IN-REGION ONLY` · `CROSS-REGION, NO COMMITTED TIME` · `CROSS-REGION WITH COMMITTED TIME` · `UNKNOWN`.

**Decision impact.** `IN-REGION ONLY` → no extra architecture on a production environment type. `CROSS-REGION` → a joint architecture, licensing and region decision, with the storage doubling, the automation-throughput degradation and the drill effort in the option. `CROSS-REGION WITH COMMITTED TIME` → the commitment must rest on **the customer's own drill evidence**, because none is published. Recovery must be a **designed, rehearsed procedure with an owner**, including reconnection, re-enablement, re-sharing, republishing and integration reconciliation.
**Blocking.** `UNKNOWN` is decision-blocking wherever a commitment exists.

**PP positive.** `BEST EFFORT` and `IN-REGION ONLY`.
**PP caution.** `CROSS-REGION, NO COMMITTED TIME` — achievable, at a cost that must be visible in the option.
**PP negative/exit.** [`Xp`] **A contractual cross-region recovery time → no platform commitment exists; the objective must be met by drill evidence the customer owns, or by an architecture whose recovery time the customer controls.** Where the geography has no pair, the residency-versus-resilience trade-off must be surfaced.

**Related criteria.** DC-D-090, DC-D-091, DC-D-080, DC-D-095, DC-D-033, DC-D-001, DC-D-089.
**Related anti-patterns.** AP-D-054, AP-D-056, AP-D-045, AP-D-047, AP-D-040.
**Related alternatives.** ALT-005, ALT-006, ALT-007, ALT-009.
**Lineage.** `operations-support.md` OP-03, OP-14, OP-15, OP-17, OP-18, OP-19, OP-22, DC-05, DC-06, DC-07, §6.2, §6.3, OP-U-03; `performance-scale.md` PF-39, PF-40, PF-41, PF-43, PF-44, DC-13, DC-14, DC-15, B-13, §3.D, §8.1 items 28–36; `licensing-cost.md` LC-24, DC-12; `alm-devops.md` ALM-18, §14.4; manifest NB-03.

---

#### DC-D-101 — Monitoring and observability depth

**Domain:** Operations · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** What must be observable about the solution in production, at what latency, and for how long.

**Why it matters.** **Nothing is monitored by default**, and depth is a **licensing decision taken during option selection**: telemetry export requires a managed environment, is *"not 100% lossless"*, and is unavailable in sovereign clouds; the aggregated surface requires tenant analytics to be enabled and is **daily-aggregated with short log retention and percentile-only metrics**; per-application insights need a tenant setting **and** a per-artefact connection string; the compliance log has roughly 24-hour latency with the vendor saying *"Don't use this information for real-time monitoring"*; and native run history — *"the only transactional record"* — **expires at 30 days**. The corpus's conclusion is the decision rule: *"If managed environments are out of scope, diagnosis capability is materially reduced and the support model must say so."* The enterprise class additionally requires **correlation identifiers across service boundaries**, which no platform supplies automatically.

**Discovery evidence.** What must be alerted on and to whom; whether a throttling metric is monitored; the required diagnostic depth; whether managed environments are in scope; whether the enterprise monitoring platform must receive the telemetry; retention required.

**States.** `NONE` · `NATIVE SURFACES ONLY` · `TELEMETRY EXPORT REQUIRED` · `INTEGRATED WITH ENTERPRISE MONITORING` · `UNKNOWN`.

**Decision impact.** Decide depth in Options, because it changes the licence footprint. Route alerts and suspension notices to a **shared destination** with pre-granted read access. Monitor the **throttling rate** with a named owner, or the automation stops without a decision. Where evidence must outlive 30 days, write it into **business records** as a functional requirement. `INTEGRATED WITH ENTERPRISE MONITORING` → correlation identifiers by design, and the ingestion and retention cost priced (DC-D-096).

**PP positive.** `NATIVE SURFACES ONLY` for the departmental class.
**PP caution.** `TELEMETRY EXPORT REQUIRED` — managed environment, premium population, and lossy by the vendor's own statement.
**PP negative/exit.** [`Xr`] A requirement for **complete, real-time, long-retention** message-level observability → a durable log outside the platform (a broker with dead-lettering plus a status store, or the enterprise platform's own message store).

**Related criteria.** DC-D-001, DC-D-103, DC-D-102, DC-D-097, DC-D-093, DC-D-096, DC-D-041.
**Related anti-patterns.** AP-D-021, AP-D-053, AP-D-061, AP-D-064.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `operations-support.md` OP-08, OP-09, OP-10, OP-11, DC-01, DC-02, DC-03, OP-AP-02, OP-AP-03, OP-AP-04, OP-AP-05, §6.1; `automation-architecture.md` AT2-42, AT2-61, N-10, N-11, §4.2, §9 row 16; `integration-architecture.md` §12.6, X-18; `licensing-cost.md` LC-23, §7.2 item 46; `performance-scale.md` §11.2.

---

#### DC-D-102 — Incident response, support hours and support tier

**Domain:** Operations · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The hours during which a failure must be responded to, by whom, within what time — and what the vendor will and will not do.

**Why it matters.** The vendor's boundaries are documented and narrower than commonly assumed: **a support plan is required to raise a ticket**, **end users cannot raise tickets**, there are **no root-cause analyses** *"as part of any support experience"*, there is a **four-hour cap** on performance and non-reproducible cases after which the case closes, there is no help with corrupted data, and **preview features are outside the service commitments**. A related conflict the corpus records: a top-severity case means *"you commit to continuous, 24x7 operation, every day with the Microsoft team until resolution"* while performance cases are capped — the two must be read together. Diagnostic access needs consent: *"Microsoft can't access or run diagnostics on data in your tenant or environment without consent"*, so **who authorises that must be named in the runbook**.

**Discovery evidence.** Required response hours and times; whether an internal first line exists; the support plan held; who may authorise vendor diagnostic access; whether a partner arrangement exists; whether preview components are on the path.

**States.** `BUSINESS HOURS, BEST EFFORT` · `BUSINESS HOURS, DEFINED RESPONSE` · `EXTENDED HOURS` · `24×7 WITH DEFINED RESPONSE` · `UNKNOWN`.

**Decision impact.** An **internal first line is mandatory** at every level above informal. Derive the support tier from **criticality**. Pre-authorise diagnostic consent or name the authoriser in the runbook. Keep **preview components off committed paths**. Budget internal root-cause capability with the telemetry to support it (DC-D-101).

**PP positive.** `BUSINESS HOURS, BEST EFFORT` and `BUSINESS HOURS, DEFINED RESPONSE` with an internal first line.
**PP caution.** `24×7 WITH DEFINED RESPONSE` — the vendor's contribution is bounded in ways the internal model must cover.
**PP negative/exit.** [`—`] none as a platform exit; where no internal capability can exist, a vendor-operated product or the incumbent's support may be the only viable classes.

**Related criteria.** DC-D-073, DC-D-001, DC-D-097, DC-D-101, DC-D-091, DC-D-115.
**Related anti-patterns.** AP-D-056, AP-D-053, AP-D-057.
**Related alternatives.** ALT-011, ALT-001, ALT-007, ALT-004.
**Lineage.** `operations-support.md` OP-24, OP-25, DC-13, DC-14, §2.5, §4, §6.4, OP-AP-13, OP-AP-14, OP-C-04; `licensing-cost.md` LC-22, §7.2 item 39; `performance-scale.md` §11.2 (four-hour case).

---

#### DC-D-103 — Diagnostic and audit evidence retention

**Domain:** Operations · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** How far back anyone must be able to reconstruct what happened — operationally, and for compliance — and from which store.

**Why it matters.** The corpus separates two obligations that are commonly conflated. **Operationally**, native run history is authoritative and **expires at 30 days**; exported telemetry is retained longer but is **lossy**; the compliance log is complete but has ~24-hour latency; and one automation surface is TTL-configurable with up to an hour's lag. **For compliance**, audit and diagnostics *"must be separate"*, audit consumes **log capacity that no entitlement provides**, and audit is **excluded from restore by default** and slows it materially when included. The corpus's decision rule is a design instruction: *"Beyond 30 days, evidence must be written to a **business record** as part of the process — a functional requirement on the design, not a monitoring setting."*

**Discovery evidence.** The reconstruction window required, operationally and for compliance; the auditor's accepted format; whether evidence must be complete or best-effort; whether process evidence is currently derived from run history.

**States.** `NONE` · `30 DAYS OPERATIONAL` · `BEYOND 30 DAYS OPERATIONAL` · `COMPLIANCE-GRADE, MULTI-YEAR` · `UNKNOWN`.

**Decision impact.** `BEYOND 30 DAYS OPERATIONAL` → export telemetry (managed environment, lossy) **and** write process evidence into business records. `COMPLIANCE-GRADE, MULTI-YEAR` → a separate store, a separate retention, a separate budget, and an explicit resolution of the **audit-completeness versus fast-recovery conflict**.

**PP positive.** `NONE` and `30 DAYS OPERATIONAL`.
**PP caution.** `BEYOND 30 DAYS OPERATIONAL` — the design changes, not a setting.
**PP negative/exit.** [`Xr`] A requirement for **complete, long-retention, message-level** evidence → a durable log outside the platform.

**Related criteria.** DC-D-027, DC-D-032, DC-D-101, DC-D-095, DC-D-059, DC-D-041.
**Related anti-patterns.** AP-D-021, AP-D-063, AP-D-054.
**Related alternatives.** ALT-006, ALT-007, ALT-009.
**Lineage.** `operations-support.md` OP-03, OP-09, OP-10, DC-03, DC-04, OP-AP-04, OP-AP-05, §6.1; `data-architecture.md` DA-16, DA-17; `licensing-cost.md` LC-11, LC-AP-05; `integration-architecture.md` §12.6, IA-45; `automation-architecture.md` §9 row 16.

---

#### DC-D-104 — Operational maturity class

**Domain:** Operations · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** The organisation's demonstrated ability to operate a solution of this criticality — ownership, monitoring, incident management, recovery, lifecycle — as it exists **today**, not as intended.

**Why it matters.** The corpus's headline claim for this area is that **operational maturity is a design input, not a post-deployment concern**: each class *"names the things that must change in the architecture, not only in the ways of working"*. Moving from business-critical to mission-critical *"changes the licence footprint of every user in the environment, the artefact structure, the environment topology"*. And where the maturity does not exist, specific options become **unavailable**: mission-critical requires drills, incident ownership, monitoring and recovery, and a pattern with an external component requires a named operator.

**Discovery evidence.** How similar existing solutions are operated today; whether an on-call rota exists; whether recovery has ever been rehearsed; whether ownership is assigned and attested; whether a governance estate exists and is maintained; whether external components are already operated.

**States.** `SIMPLE DEPARTMENTAL` · `BUSINESS-CRITICAL` · `ENTERPRISE` · `MISSION-CRITICAL` · `UNKNOWN`.

**Decision impact.** Match the **class of the solution** (DC-D-001) to the **class the organisation can actually operate**. Where they differ, the gap is a scope decision for the sponsor: raise the operating capability (with cost and lead time in the option), lower the criticality commitment, or select a class where someone else operates it (a vendor-operated product, or the incumbent). Do **not** deliver a mission-critical commitment into a departmental operating model.
**Blocking.** `UNKNOWN` is decision-blocking above the departmental class.

**PP positive.** A class match, at any level — including `SIMPLE DEPARTMENTAL`, which the corpus calls *"a legitimate class"* whose over-engineering is a real cost.
**PP caution.** A one-class gap — closable with a funded plan.
**PP negative/exit.** [`Xc`] A two-class gap with no funded plan → the commitment cannot be delivered; options with an external component are **unavailable**.

**Related criteria.** DC-D-001, DC-D-070, DC-D-073, DC-D-100, DC-D-101, DC-D-102, DC-D-097, DC-D-110.
**Related anti-patterns.** AP-D-053, AP-D-054, AP-D-026, AP-D-039, AP-D-059.
**Related alternatives.** ALT-011, ALT-001, ALT-007, ALT-010, ALT-004.
**Lineage.** `operations-support.md` §1, §1.1, OP-01, DC-16, OP-AP-01, OP-AP-02, OP-AP-06, OP-AP-09; `architecture-patterns.md` §5.1 (operational-maturity row), §13, Y-13; `governance.md` GOV-XB-01; `licensing-cost.md` LC-23, DC-11.

---

### 4.12 Strategic and platform

#### DC-D-105 — Vendor lock-in tolerance and portability

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** How much dependence on a single vendor the organisation accepts, and whether any layer of the solution must be re-hostable elsewhere.

**Why it matters.** The corpus supplies a precise asymmetry rather than a general warning: **data and server-side .NET components are portable; the interface, the expression language and the automations are not**. So "portability" must be asked **per layer**. This is also the criterion behind the deployment-model finding: at least one enterprise low-code alternative documents customer-hosted operation, which the target platform documents as unsupported — but note carefully that **running on the customer's own cluster is not the same as being portable off that vendor**, and the comparators' portability is `UNKNOWN` in this corpus.

**Discovery evidence.** Whether a policy or a contract addresses lock-in; which layers would have to move and to what; whether a second-source requirement exists; whether the organisation has migrated a platform before and what it cost.

**States.** `LOCK-IN ACCEPTED` · `DATA PORTABILITY REQUIRED` · `APPLICATION-LAYER PORTABILITY REQUIRED` · `FULL PORTABILITY REQUIRED` · `UNKNOWN`.

**Decision impact.** `DATA PORTABILITY REQUIRED` → satisfiable; data and server-side components are portable. `APPLICATION-LAYER PORTABILITY REQUIRED` → the interface, expression logic and automations are a **rewrite**, and that cost belongs in the option (DC-D-098). `FULL PORTABILITY REQUIRED` → a conventional stack is the only class this corpus can evidence.

**PP positive.** `LOCK-IN ACCEPTED` and `DATA PORTABILITY REQUIRED`.
**PP caution.** `APPLICATION-LAYER PORTABILITY REQUIRED` — priceable, and frequently unpriced.
**PP negative/exit.** [`Xp`] **`FULL PORTABILITY REQUIRED` → custom development** (ALT-005). Another low-code platform is a *candidate* here, but the corpus holds no evidence on comparator portability and will not infer it.

**Related criteria.** DC-D-106, DC-D-098, DC-D-108, DC-D-107, DC-D-111.
**Related anti-patterns.** AP-D-002, AP-D-003.
**Related alternatives.** ALT-005, ALT-008, ALT-007.
**Lineage.** `platform-suitability.md` PS-51, §2 row 32, §3; `licensing-cost.md` §6 (exit/option value); `alternatives.md` ALT-008 (and `anti-patterns.md` §6 V-D-01, V-D-04).

---

#### DC-D-106 — Exit strategy and switching cost

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Whether a documented exit path is required, and what leaving would actually cost.

**Why it matters.** It is DC-D-105 expressed as an obligation rather than a preference, and the corpus supplies two concrete traps. First, the portability asymmetry means an exit is a **partial rewrite**, not a data migration. Second, one team-scoped tier has **no export path to a full environment** (*"not yet available"*), so its exit *"may be a rebuild"* — the sharpest example of a cheap start with an expensive door. The corpus also frames exit as an **option value**, which is the right way to price it: *"future switching cost belongs in TCO where portability matters."*

**Discovery evidence.** Whether procurement or a contract requires an exit plan; what would trigger an exit; which layers would move; whether the chosen tier has a documented export path; whether an exit has been costed.

**States.** `NOT REQUIRED` · `DOCUMENTED PLAN REQUIRED` · `TESTED EXIT REQUIRED` · `UNKNOWN`.

**Decision impact.** `DOCUMENTED PLAN REQUIRED` → enumerate per layer what moves and what is rewritten, and price it. `TESTED EXIT REQUIRED` → this corpus records no mechanism for testing an exit, so the requirement is either descoped or met by a class where the exit is conventional. Avoid tiers with no documented export path where any exit obligation exists.

**PP positive.** `NOT REQUIRED`.
**PP caution.** `DOCUMENTED PLAN REQUIRED` — achievable and rarely done.
**PP negative/exit.** [`Xp`] `TESTED EXIT REQUIRED` → not evidenced as achievable on this platform; treat as blocked or descoped, and consider a conventional stack.

**Related criteria.** DC-D-105, DC-D-098, DC-D-113, DC-D-004.
**Related anti-patterns.** AP-D-065, AP-D-060.
**Related alternatives.** ALT-005, ALT-008, ALT-011.
**Lineage.** `platform-suitability.md` PS-51; `licensing-cost.md` §6, LC-AP-09, §7.2 item 32; `data-architecture.md` DA-43; `application-architecture.md` AA-50.

---

#### DC-D-107 — Tolerance to vendor-driven change cadence

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether the organisation can absorb changes it does not control, on the vendor's schedule.

**Why it matters.** The cadence is **mandatory**: two release waves a year cannot be declined, the deprecation register is *"continuous and dated"* with items that *"delete or silently break things"*, and *"assuming behaviour can be frozen"* is a named anti-pattern. The corpus records the verdict for the conflicting requirement plainly: a requirement for frozen behaviour or per-release change control *"conflicts with mandatory semi-annual waves and rolling deprecations"*, producing a `RISK → CONDITIONAL` fit. Exposure also differs by surface — the corpus ranks vendor-driven interface change exposure as highest on the record-centric surface, medium on the task-focused one, lowest on a coded one (which carries full own-maintenance instead).

**Discovery evidence.** Whether a validation or change-control regime forbids uncontrolled change; whether a regulated process requires revalidation on change; whether an early-access wave dry-run is feasible; who tracks the change stream today.

**States.** `TOLERANT` · `MANAGED WITH TESTING` · `CHANGE CONTROL REQUIRED` · `BEHAVIOUR MUST BE FROZEN` · `UNKNOWN`.

**Decision impact.** `MANAGED WITH TESTING` → an early-access wave regression dry-run and a named change-tracking owner (DC-D-112) with a recurring remediation budget. `CHANGE CONTROL REQUIRED` → a documented revalidation process on each wave, and a preference for the least interface-exposed surface. `BEHAVIOUR MUST BE FROZEN` → the requirement is incompatible with the platform.

**PP positive.** `TOLERANT` and `MANAGED WITH TESTING`.
**PP caution.** `CHANGE CONTROL REQUIRED` — feasible, and it makes the remediation budget non-optional.
**PP negative/exit.** [`Xp`] **`BEHAVIOUR MUST BE FROZEN` is a documented exit** — a self-managed stack whose upgrade schedule the organisation controls (ALT-005, and ALT-008 as a candidate on the deployment-model axis).

**Related criteria.** DC-D-004, DC-D-112, DC-D-115, DC-D-081, DC-D-059.
**Related anti-patterns.** AP-D-058, AP-D-057, AP-D-052.
**Related alternatives.** ALT-005, ALT-008, ALT-001.
**Lineage.** `platform-suitability.md` PS-50, AP-16, §2 row 31, §3, §9; `operations-support.md` OP-26, DC-18, OP-AP-12; `licensing-cost.md` LC-14, LC-29, §14.4; `application-architecture.md` AA-54, §9 condition 6.

---

#### DC-D-108 — Deployment-model constraint

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Where the solution's runtime must physically execute: vendor-operated multi-tenant service, the customer's own cloud subscription, the customer's data centre, or a disconnected environment.

**Why it matters.** It is the **cleanest single-criterion platform exit in the corpus**, and Block D re-verified it on 2026-09-03 (`anti-patterns.md` §6 V-D-01): the platform and its data service are **SaaS only**; no on-premises or self-hosted deployment option is documented. On-premises *connectivity* exists (a gateway, and private networking with a private circuit into the network); on-premises *deployment* does not. Two related absolutes: **exact datacentre disclosure is not available**, and disconnected or customer-hosted deployment is unsupported. This is also the one axis on which Block D admits comparator evidence: at least one enterprise low-code platform documents Kubernetes-based private-cloud and on-premises deployment including *"fully air-gapped private clouds or on-premise"*; a second announced self-hosted deployment in an **early-access programme, not generally available** (`anti-patterns.md` §6 V-D-04, vendor documentation, capability facts only).

**Discovery evidence.** The clause or policy stating where the runtime must execute; whether it is a residency requirement (DC-D-033) or a *deployment* requirement, which are different; whether disconnected operation is required; whether datacentre-level disclosure is demanded; whether an existing exception process exists.

**States.** `VENDOR-OPERATED SERVICE ACCEPTABLE` · `CUSTOMER CLOUD SUBSCRIPTION REQUIRED` · `CUSTOMER DATA CENTRE REQUIRED` · `AIR-GAPPED REQUIRED` · `UNKNOWN`.

**Decision impact.** `VENDOR-OPERATED SERVICE ACCEPTABLE` → no constraint. Anything else → the platform is **out** for the runtime. The outcome is §6.2 class 9 **`DEPLOYMENT MODEL EXCLUDES THIS PLATFORM — COMPARATOR EVIDENCED ON THIS AXIS`** — the **only** class in the set permitted to name a comparator, because this is the one axis on which a comparator documents a generally-available capability the platform documents as unsupported (with the second comparator's capability in Early Access, not GA — AP-D-057). ALT-005 also satisfies the axis. On every dimension other than deployment model the candidates remain **`COMPARATIVE FIT UNEVALUATED`** (§4A.1). Distinguish this from residency carefully: a residency requirement is often satisfiable by region selection, whereas a deployment requirement is not satisfiable at all.
**Blocking.** `UNKNOWN` is decision-blocking: it can eliminate the platform entirely, so it must be established before any architecture work.

**PP positive.** `VENDOR-OPERATED SERVICE ACCEPTABLE`.
**PP caution.** A requirement stated as "on-premises" that is really about **residency or network reach** — clarify, because the answers differ completely.
**PP negative/exit.** [`Xp`] **`CUSTOMER CLOUD SUBSCRIPTION REQUIRED`, `CUSTOMER DATA CENTRE REQUIRED` and `AIR-GAPPED REQUIRED` are documented exits.**

**Related criteria.** DC-D-033, DC-D-044, DC-D-063, DC-D-105, DC-D-059, DC-D-111.
**Related anti-patterns.** AP-D-035, AP-D-003, AP-D-057.
**Related alternatives.** ALT-005, ALT-008, ALT-007, ALT-001.
**Lineage.** `platform-suitability.md` PS-17, PS-47, §2 rows 29, 36, §3; `integration-architecture.md` §12.5, I-10; `data-architecture.md` §2 row 18, DA-58; `anti-patterns.md` §6 V-D-01, V-D-04; `alternatives.md` ALT-008.

---

#### DC-D-109 — Existing productivity and business-application estate

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** What the organisation already licenses and operates in the vendor's productivity and business-application families, and which of it is actually in use.

**Why it matters.** It is a **current-state** criterion (permissible in a technology-neutral Discovery) that materially changes economics and options in both directions. Positively: seeded entitlement, existing identity, existing document stores and existing business applications reduce the incremental cost and can make the requirement satisfiable without new entitlement. Negatively: it is also the source of the corpus's *configure-or-buy-first* rung — a requirement already covered by a first-party application or a platform feature routes to configure or buy **before any build**. One trap the corpus records: touching restricted business-application tables has its own entitlement consequence, and the current restricted-table list was itself an open item.

**Discovery evidence.** Current entitlement holdings by SKU and population; which business applications are deployed and used; whether document stores and collaboration surfaces are in use; whether a first-party application overlaps this requirement.

**States.** `MINIMAL` · `PRODUCTIVITY ONLY` · `PRODUCTIVITY PLUS SOME PREMIUM` · `EXTENSIVE INCLUDING BUSINESS APPLICATIONS` · `UNKNOWN`.

**Decision impact.** Run the configure-or-buy check against the existing estate **before** any build decision. Where existing entitlement covers the requirement, the saving is population-wide and the option is strong. Where a first-party application overlaps, that becomes a priced option (ALT-011). Where restricted tables are touched, verify the entitlement consequence.

**PP positive.** `PRODUCTIVITY PLUS SOME PREMIUM` and above, where the requirement fits inside it.
**PP caution.** `EXTENSIVE INCLUDING BUSINESS APPLICATIONS` — the overlap check is mandatory, not optional, and a custom build duplicating a first-party application has a documented lifecycle conflict.
**PP negative/exit.** [`—`] none evidenced; it makes other classes *more* attractive rather than disqualifying this one.

**Related criteria.** DC-D-002, DC-D-093, DC-D-111, DC-D-110, DC-D-092.
**Related anti-patterns.** AP-D-007, AP-D-062, AP-D-004.
**Related alternatives.** ALT-003, ALT-011, ALT-001, ALT-004.
**Lineage.** `platform-suitability.md` PS-41, PS-42, U-5, §2 rows 25–26; `application-architecture.md` AA-20, AA-36 rung 0, AP-35, §1 row 0; `licensing-cost.md` LC-03, §6, DC-01; `data-architecture.md` §2 rows 4, 7.

---

#### DC-D-110 — Team skills and pro-code capacity

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** The capability actually available to build and maintain the solution — low-code, pro-code, data, cloud infrastructure — distinguishing what exists from what is planned.

**Why it matters.** The corpus makes skills an **explicit architecture criterion**, quoted directly: *"Choose services that your team knows how to use, or commit to training them before you choose a service"*, and *"The best service for your workload might be a technology that your team isn't skilled at, can't afford, or it might require extra security…"*. Its decision rule is blunt: *"a HYBRID needing .NET plug-ins is POOR for a team with no developers"*, and a design requiring a capability the team lacks is a documented **RISK**. At the pattern level it becomes a **composed disqualifier**: *"Hybrid architecture required + no pro-dev/enterprise platform capability available → POOR FIT."* The fusion-development guidance names the three signals where citizen development is insufficient — no connector exists, integrity logic must be enforced, complex dynamic business flows — and *"Any of the three signals → HYBRID; all three at scale → consider CUSTOM."*

**Discovery evidence.** Who will build and who will maintain; whether pro-code capability exists **in-house** and is available (not merely present); whether cloud infrastructure capability exists; whether a training commitment is funded; whether a partner fills the gap and for how long.

**States.** `LOW-CODE ONLY` · `LOW-CODE PLUS SOME PRO-CODE` · `FUSION TEAM AVAILABLE` · `FULL ENGINEERING CAPABILITY` · `PARTNER-DEPENDENT` · `UNKNOWN`.

**Decision impact.** Feed capability into **every** hybrid or custom recommendation. `LOW-CODE ONLY` → in-platform options, with any hybrid trigger recorded as a constraint requiring either a funded capability plan or a different architecture. `PARTNER-DEPENDENT` → a dated handover plan, because partner-to-customer operational handover is the corpus's named undocumented failure point.
**Blocking.** `UNKNOWN` is decision-blocking for any option with a pro-code or infrastructure component.

**PP positive.** `LOW-CODE ONLY` and `LOW-CODE PLUS SOME PRO-CODE` for in-platform options — and this is a genuine reason to prefer the platform.
**PP caution.** `PARTNER-DEPENDENT` for a long-lived solution.
**PP negative/exit.** [`—`] none as a platform exit. It is a **gate on hybrid and custom options** — and, symmetrically, `FULL ENGINEERING CAPABILITY` makes ALT-005 and ALT-006 genuinely cheaper than they would otherwise be, which is a legitimate input the other direction.

**Related criteria.** DC-D-070, DC-D-076, DC-D-078, DC-D-104, DC-D-114, DC-D-057, DC-D-003.
**Related anti-patterns.** AP-D-002, AP-D-026, AP-D-046, AP-D-059.
**Related alternatives.** ALT-004, ALT-005, ALT-006, ALT-009, ALT-011.
**Lineage.** `platform-suitability.md` PS-39, PS-40, §2 row 27; `architecture-patterns.md` §13 (hybrid/pro-dev disqualifier), §5.1, Y-13; `automation-architecture.md` §4.1, §9 row 22; `operations-support.md` OP-U-07; `alm-devops.md` §1 (rung 3 prerequisites), §14.2.

---

#### DC-D-111 — Existing enterprise platform estate

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Which enterprise platforms already exist and own domains adjacent to this requirement — resource planning, customer, service management, process, integration, data — and whether each has an owning team and a published contract.

**Why it matters.** It is a **current-state** criterion that produces one of the corpus's strongest redirects, and one it flags as invisible in vendor guidance: *"Nothing in the fetched Microsoft material tells an architect to check this, which is precisely why it must be step 1."* Where an integration capability exists with a published contract, the platform consumes it and integrates nothing; where a process engine already owns the process class, adding another *"duplicates the operating model rather than reducing it"*. Governance frames it as **a governance decision before a product decision**, with the essential caveat that **reuse is not automatic**: *"an incumbent that cannot meet the requirements remains unsuitable."*

**Discovery evidence.** Platform inventory with owning teams; whether the target systems are already integrated and via what; whether contracts are published and current; the platform teams' lead times; whether any incumbent is on a decommissioning plan.

**States.** `NONE` · `PLATFORMS EXIST, NO OWNERSHIP` · `PLATFORMS EXIST WITH OWNERSHIP` · `PLATFORMS EXIST WITH PUBLISHED CONTRACTS` · `UNKNOWN`.

**Decision impact.** `PLATFORMS EXIST WITH PUBLISHED CONTRACTS` → consume the contract; the enclosing boundary is the architecture and the other patterns operate inside it. `PLATFORMS EXIST WITH OWNERSHIP` → negotiate the contract or record, **per requirement**, why the incumbent cannot meet it. `PLATFORMS EXIST, NO OWNERSHIP` → treat as technical debt rather than as a capability.

**PP positive.** `NONE` — a genuinely greenfield integration position.
**PP caution.** Any state where a boundary exists and has not been consulted — the point-to-point estate forms exactly here.
**PP negative/exit.** [`—`] none as a platform exit; it redirects **specific responsibilities** to the incumbent (ALT-007), and the platform keeps the experience and human-workflow layers.

**Related criteria.** DC-D-036, DC-D-021, DC-D-002, DC-D-070, DC-D-109, DC-D-003.
**Related anti-patterns.** AP-D-027, AP-D-022, AP-D-002, AP-D-007.
**Related alternatives.** ALT-007, ALT-001, ALT-011, ALT-009.
**Lineage.** `integration-architecture.md` §12.1, §2.2 step 1, §9 row 23; `governance.md` GOV-XB-02; `automation-architecture.md` AT2-52, §3.B row 19, §4.3; `architecture-patterns.md` AP-10, Y-12, matrix rows 29–30, APR-U-08; manifest NB-06.

---

#### DC-D-112 — Platform-change tracking capacity and ownership

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** HIGH

**Definition.** Whether someone is accountable for monitoring the platform's change and deprecation streams, and whether remediation is funded.

**Why it matters.** The corpus treats this as a **standing duty with a named owner**, because the change stream is continuous and dated and *"several items delete or silently break things"*. It also converts it into a **cost line**: remediation is *"a recurring, unavoidable line"*, and technical debt is named by the vendor as a performance-efficiency concern. Concrete instances already in the corpus show the duty is not hypothetical: two accelerators are deprecated and unmaintained (one of them the previous governance tooling, *"Issues are no longer reviewed or addressed"*), the previous low-code test framework is deprecated leaving no supported first-party equivalent, a bundled credit allocation has a **dated removal**, and a consumer-identity service closed to new tenants changing the recommended path.

**Discovery evidence.** Who monitors the change stream and the message centre today; whether a remediation budget line exists; whether any current dependency is already announced as deprecated or unmaintained; whether early-access waves are ever tested.

**States.** `NO OWNER` · `INFORMAL` · `NAMED OWNER, NO BUDGET` · `NAMED OWNER WITH RECURRING BUDGET` · `UNKNOWN`.

**Decision impact.** Assign the duty and fund the remediation, proportionate to lifespan (DC-D-004) and change tolerance (DC-D-107). Record existing dependencies on unmaintained components as **technical debt with a migration path**, not as working capability. Prefer supported, non-preview components on critical paths.

**PP positive.** `NAMED OWNER WITH RECURRING BUDGET`.
**PP caution.** `NO OWNER` for a solution expected to live beyond a year — the first silent break will be discovered by a user.
**PP negative/exit.** [`Cf`] none evidenced; but combined with a frozen-behaviour requirement it is DC-D-107's exit.

**Related criteria.** DC-D-107, DC-D-004, DC-D-115, DC-D-070, DC-D-097, DC-D-075.
**Related anti-patterns.** AP-D-058, AP-D-057, AP-D-006.
**Related alternatives.** ALT-011 (vendor-operated), ALT-001, ALT-004.
**Lineage.** `operations-support.md` OP-26, OP-27, DC-18, DC-20, OP-AP-12, OP-AP-18, §6.5; `licensing-cost.md` LC-14, LC-29, §14.4; `governance.md` GOV-12, GOV-A11, GOV-C1; `alm-devops.md` ALM-17, ALM-22, ALM-A13; `application-architecture.md` AA-C5, §9 condition 6.

---

#### DC-D-113 — Multi-tenancy and resale requirement

**Domain:** Strategic · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** LOW

**Definition.** Whether the solution must be delivered to more than one tenant, or licensed and resold to third parties.

**Why it matters.** Two documented constraints and one open gap. **Promotion tooling cannot deploy across tenants**, so cross-tenant delivery forces the source-controlled rung with external pipelines. And **independent-software-vendor and multi-tenant resale licensing was an open deferral in the corpus** — recorded as *"No row; POOR/CONDITIONAL unknown"* — so the commercial model for resale is not established here at all. Anyone building for resale must treat this as a research gap rather than a constraint list.

**Discovery evidence.** Whether the solution serves more than one tenant; whether it will be sold or licensed; whether a marketplace listing is intended; whether a partner delivery model applies.

**States.** `SINGLE TENANT` · `MULTI-TENANT INTERNAL (GROUP COMPANIES)` · `RESALE OR MARKETPLACE INTENDED` · `UNKNOWN`.

**Decision impact.** `MULTI-TENANT INTERNAL` or `RESALE` → the source-controlled rung with external pipelines is mandatory, and the **licensing model must be established from the authoritative licensing document and the vendor's partner terms**, because this corpus does not contain it.
**Blocking.** `RESALE OR MARKETPLACE INTENDED` should be treated as **decision-blocking on the commercial model** until that gap is closed.

**PP positive.** `SINGLE TENANT`.
**PP caution.** `MULTI-TENANT INTERNAL` — deliverable, with the delivery rung's prerequisites.
**PP negative/exit.** [`—`] none evidenced — because the evidence does not exist. That absence is the finding, not a verdict.

**Related criteria.** DC-D-076, DC-D-082, DC-D-093, DC-D-106, DC-D-114.
**Related anti-patterns.** AP-D-042, AP-D-062.
**Related alternatives.** ALT-005, ALT-011.
**Lineage.** `alm-devops.md` ALM-10, §4 row 16; `platform-suitability.md` §7 (ISV/multi-tenant resale deferral, target Area 10); `licensing-cost.md` LC-02, LC-U-02.

---

#### DC-D-114 — Sourcing and delivery model

**Domain:** Strategic · **Volatility:** STATIC PRINCIPLE · **Confidence:** MEDIUM

**Definition.** Who will build and who will run the solution — internal team, partner, vendor-operated product, or a combination — and how responsibility transfers between them.

**Why it matters.** It is a **current-state** criterion that changes which options are deliverable and which obligations are real. The corpus records the specific failure it produces: **operational handover from a delivery partner to a customer operations team is *"the commonest real-world failure point for partner-delivered solutions, and entirely undocumented"***, and it is left as a permanently open item. It also interacts with several gates: a hybrid needs a named operator, a business-critical solution needs an internal first line, and a service identity needs a lifecycle owner — none of which a build-only engagement supplies.

**Discovery evidence.** Who builds; who operates after go-live; whether a handover plan and date exist; whether the partner's engagement extends into operations and for how long; whether the internal team will have the telemetry and access it needs.

**States.** `INTERNAL BUILD AND RUN` · `PARTNER BUILD, INTERNAL RUN` · `PARTNER BUILD AND RUN` · `VENDOR-OPERATED PRODUCT` · `UNKNOWN`.

**Decision impact.** `PARTNER BUILD, INTERNAL RUN` → a **dated handover plan** with named recipients, pre-granted access, documented runbooks and a rehearsed recovery, because nothing in the platform supplies this. `VENDOR-OPERATED PRODUCT` → ALT-011's economics, and the vendor's availability joins the weakest-link analysis. Where no run capability exists in any model, the option set narrows to vendor-operated or incumbent-owned classes.

**PP positive.** `INTERNAL BUILD AND RUN` with capability matched to the criticality class.
**PP caution.** `PARTNER BUILD, INTERNAL RUN` — the corpus's named failure point, and the one most often left implicit.
**PP negative/exit.** [`—`] none as a platform exit.

**Related criteria.** DC-D-073, DC-D-104, DC-D-110, DC-D-070, DC-D-006, DC-D-102.
**Related anti-patterns.** AP-D-053, AP-D-026, AP-D-036, AP-D-047.
**Related alternatives.** ALT-011, ALT-001, ALT-007, ALT-004.
**Lineage.** `operations-support.md` OP-U-07, §1.1, DC-01, DC-13; `architecture-patterns.md` Y-13, §13; `platform-suitability.md` PS-40; `security.md` §4 row 13.

---

#### DC-D-115 — Roadmap and preview dependency

**Domain:** Strategic · **Volatility:** **VOLATILE VALUE / requires current verification** · **Confidence:** HIGH

**Definition.** Whether the design depends on a capability that is in preview, in early access, announced but unshipped, or whose general-availability state is unverified.

**Why it matters.** Preview capabilities are *"Provided as-is, with all faults, and as available… **excluded from the Service SLAs**"*, with restricted-language, business-hours break-fix support, and they default to particular regions — which matters for a regulated workload. The corpus also holds several **live** instances: a set of general-availability states it could not confirm (a high-volume table type, a bespoke external-site surface, a coded application surface, a server-logic capability), which it handles by keeping the corresponding fit verdicts **CONDITIONAL** pending a browser check; controls that are preview and therefore *cannot be the control*; and cost meters that are preview with billing caveats. Two facts have **already changed once** during the corpus's own life, which the corpus flags explicitly as a warning about half-life.

**Discovery evidence.** Which components in the design are preview or early access; whether their general-availability state has been checked **today**; whether any business case line depends on a preview meter; whether an announced-but-unshipped capability is assumed.

**States.** `NO PREVIEW DEPENDENCY` · `PREVIEW ON NON-CRITICAL PATH` · `PREVIEW ON CRITICAL PATH` · `DEPENDS ON UNSHIPPED CAPABILITY` · `UNKNOWN`.

**Decision impact.** Keep preview components **off committed paths**. Where a requirement can only be met by one, the outputs are: proceed with an explicitly accepted, owner-named risk and a **dated re-verification**; change the requirement; or select an option that does not depend on it. Where the general-availability state is unverified, the fit verdict stays **CONDITIONAL** — the corpus's own gate condition. Never build a business case on a preview meter or a bundled allocation with a removal date.

**PP positive.** `NO PREVIEW DEPENDENCY`.
**PP caution.** `PREVIEW ON NON-CRITICAL PATH` — legitimate, with a re-verification date.
**PP negative/exit.** [`—`] none as a platform exit; `PREVIEW ON CRITICAL PATH` and `DEPENDS ON UNSHIPPED CAPABILITY` are **blocking** until re-verified or descoped.

**Related criteria.** DC-D-107, DC-D-112, DC-D-059, DC-D-102, DC-D-092.
**Related anti-patterns.** AP-D-057, AP-D-055, AP-D-058.
**Related alternatives.** ALT-011, ALT-005, ALT-010.
**Lineage.** `operations-support.md` OP-AP-14, §6.4, §6.5; `application-architecture.md` U-C6, AA-C3, AA-C10, §9 conditions 2, 4, 6; `security.md` SEC-25, SEC-35, SEC-U-02, SEC-U-06, SEC-C1; `licensing-cost.md` LC-AP-06, §7.1 item 10, §7.2 item 47, LC-U-09; `data-architecture.md` C-02, U-02, U-06; `platform-suitability.md` U-16, C-10.

---
## 4A. Alternative-side signals — and where the comparator evidence is absent

**Why this section exists.** §4's signal fields evaluate **one class**. Every criterion asks *"what does this state mean for Power Platform"*, and no other class has per-criterion states. That makes this model strong at deciding whether Power Platform is in or out, and structurally unable to decide **which of the survivors fits** — a criticism this file accepts, and which `alternatives.md` §9 states in its own words: *"A decision model built on this must be strong on **disqualification** and modest on **preference**."*

The correct repair is **not** to manufacture symmetry. It is to encode the alternative-side evidence that genuinely exists, and to mark its absence everywhere else so the hand-off is visibly incomplete rather than silently so.

### 4A.1 The default rule

> **`COMPARATOR EVIDENCE ABSENT` is the default on every criterion.**
>
> The corpus holds **no empirical benchmark for any technology** (manifest NB-07), **no comparative TCO study against any named alternative** (`licensing-cost.md` LC-U-04, §7.3 item 51), **no evaluation of any incumbent enterprise platform** (`automation-architecture.md` §3.B row 19), **no failure-rate or incident evidence for any service** (`automation-architecture.md` §8.7), and **nothing on comparator low-code platforms except the deployment-model axis** (`alternatives.md` §6 item 2).
>
> Therefore: where §4A.2 does not carry a row for a criterion, the model's output for that criterion is `POWER PLATFORM <exit class> → CANDIDATES: ALT-NNN… — COMPARATOR EVIDENCE ABSENT`, and a pack must render that phrase rather than a preference.

This is the rule that governs §6's outcome-class names. It applies symmetrically: it forbids *"custom development is more expensive"* exactly as firmly as it forbids *"custom development is preferred"*.

**88 of the 116 criteria carry no alternative-side signal at all.** That is not an omission to be closed by better reading inside Block D; the gaps are research commissions (`alternatives.md` §6).

### 4A.2 The criteria where alternative-side evidence does exist

The `G`-flagged criteria of §3.1. Signal strengths, in descending force:

- **`UNAVAILABLE`** — the corpus states the option cannot be exercised, not that it is worse.
- **`CONSTRAINED`** — a documented obligation or hard limit on the alternative class itself.
- **`CAUTION`** — a documented negative fact about the alternative class, short of a limit.
- **`CANDIDATE`** — the class comes into scope, with its fit unevaluated.
- **`UNKNOWN`** — the corpus explicitly cannot assess the class here. Recorded so it is not read as silence.

| Criterion | Class(es) | Signal | Evidence |
|---|---|---|---|
| DC-D-006 Accountable ownership | ALT-005, ALT-006, ALT-009 | **UNAVAILABLE** where no owner can exist | `architecture-patterns.md` §13 row 2 — *"unavailable, not merely expensive"*; AP-D-026 |
| DC-D-006 (cont.) | ALT-001, ALT-007, ALT-011 | CANDIDATE — vendor- or incumbent-operated ownership survives | `alternatives.md` ALT-011, ALT-001 |
| DC-D-021 System of record | ALT-007 | **CONSTRAINED** — authoritative ledgers are *deliberately excluded* from the vendor's bidirectional product | `integration-architecture.md` I-26 |
| DC-D-035 Stream and system count | ALT-005, ALT-006 | CAUTION — connectivity must be built: *"A dozen built-in binding types - Write code for custom bindings"* against 1,400+ connectors | `automation-architecture.md` §8.3; `alternatives.md` ALT-005 |
| DC-D-036 Integration ownership | ALT-007 | CAUTION — lead time is the incumbent's and *"nothing in the fetched evidence quantifies this"*; double abstraction across three contracts; the enclosing-boundary pattern is `INF`, **not vendor-endorsed** | manifest NB-06; `architecture-patterns.md` APR-U-08; `integration-architecture.md` §12.1 |
| DC-D-036 (cont.) | ALT-007 | **`UNKNOWN`** on any specific incumbent's fit | `automation-architecture.md` §3.B row 19 |
| DC-D-039 Per-mechanism throughput ceiling | ALT-006 | **`UNKNOWN`** — two of the three broker services recommended here were **never sized** | `automation-architecture.md` U-13; `integration-architecture.md` U-03 |
| DC-D-040 Sustained throughput | ALT-006 | CONSTRAINED — 1,000 operations per second on the standard broker tier; autoscaling can move the overload downstream rather than absorb it | `automation-architecture.md` §8.4 |
| DC-D-041 Delivery guarantee and ordering | ALT-006 | CONSTRAINED — the event service **guarantees neither ordering nor exactly-once**; the streaming service has **no dead-lettering**; idempotent consumers are required regardless | `automation-architecture.md` §8.4 |
| DC-D-043 Payload size and type | ALT-006 | CONSTRAINED — 256 KB standard-tier broker messages force a claim-check for documents | `automation-architecture.md` §8.4 |
| DC-D-044 Network boundary | ALT-004 + ALT-006 | **CONSTRAINED (mutual exclusion)** — the platform's own event-publishing mechanism *"doesn't support VNet"*, so *events out to a broker* and *all egress private* cannot both hold through it | `automation-architecture.md` §8.4 |
| DC-D-049 Process elapsed duration | ALT-005 | CONSTRAINED — a **230-second maximum HTTP response on every plan** of the serverless host; a 5/10-minute execution cap on its legacy plan, itself legacy with a dated retirement | `automation-architecture.md` §8.3 |
| DC-D-049 (cont.) | ALT-006 | CONSTRAINED — a stateless choice silently shrinks the envelope to a 5-minute run duration | `automation-architecture.md` §8.4 |
| DC-D-050 Synchronous response | ALT-006 | **CONSTRAINED — escalation does not relieve the ceiling.** The code-first orchestration service's consumption tier has the **same 120-second synchronous window**; *"'Move to Logic Apps' does not relieve it."* | `automation-architecture.md` §8.2 |
| DC-D-050 (cont.) | ALT-005 | CONSTRAINED — 230-second maximum HTTP response on every plan | `automation-architecture.md` §8.3 |
| DC-D-051 Event frequency floor | ALT-006 | CONSTRAINED — *"all connector triggers are long-polling with a 30-second wait — a latency floor, not push"* | `automation-architecture.md` §8.4 |
| DC-D-053 Concurrency, parallelism, ordering | ALT-006 | **CONSTRAINED** — the code-first orchestration service has the **identical** 500-action / 8-nesting ceiling and prescribes the same remedy | `automation-architecture.md` §8.2 |
| DC-D-055 Human-in-the-loop | ALT-005, ALT-006 | **ABSENT CAPABILITY** — approval routing with delegation, escalation and an action centre has **no equivalent in the code-first alternatives the corpus examined**, and must be built | `automation-architecture.md` §4.1 row 12, AT2-23…AT2-25; `alternatives.md` ALT-005 |
| DC-D-055 (cont.) | ALT-007 | **`UNKNOWN`** — *"no Microsoft or independent source evaluates incumbent BPM/ESB platforms; treat as reasoning, not evidence"* | `automation-architecture.md` §3.B row 19 |
| DC-D-057 Compute intensity | ALT-006 | CONSTRAINED — orchestrator code is constrained (no current time, random identifiers, bindings, I/O, statics, environment variables, HTTP, sleeps or arbitrary async); its **non-determinism guard is explicitly unreliable**; deploying a change **can break in-flight orchestrations**; one hosting model has a dated end of support | `automation-architecture.md` §8.4 |
| DC-D-057 (cont.) | ALT-005 | CAUTION — cold starts unless always-ready instances are paid for continuously; a 600-active-outbound-connection cap on that plan | `automation-architecture.md` §8.3 |
| DC-D-070 Governance maturity | ALT-006, ALT-009, ALT-007 (boundary form) | **UNAVAILABLE** at `NONE` / `EMERGING` — *"unavailable, not merely expensive"* | `architecture-patterns.md` §13 row 2; AP-D-026 |
| DC-D-073 Support and operational ownership | ALT-005, ALT-006, ALT-009 | **UNAVAILABLE** where no support capability can exist | `architecture-patterns.md` §13 row 2; `operations-support.md` §1.1 |
| DC-D-073 (cont.) | ALT-011, ALT-001, ALT-007 | CANDIDATE — vendor-operated or incumbent support already exists | `alternatives.md` ALT-011, ALT-001, ALT-007 |
| DC-D-083 Cross-boundary deployment coordination | ALT-006, ALT-009 | CONSTRAINED — a **second coordinated supply chain** is required; deploying one side alone is admissible only under a guaranteed compatibility policy; compensation, reconciliation and idempotency artefacts need change control equal to the forward path | `alm-devops.md` §14.2; `alternatives.md` ALT-006 |
| DC-D-096 External and hybrid consumption cost | ALT-006, ALT-009 | CAUTION — a second billing model, plus the estate, its administration, its monitoring and its log retention, which the corpus names and **does not price**; gateway-at-scale infrastructure cost is an open item | `licensing-cost.md` LC-U-06; `alternatives.md` ALT-006 |
| DC-D-100 Recovery point / recovery time | ALT-005, ALT-006, ALT-007 | CANDIDATE — these classes **can** underwrite a contractual objective where the platform cannot | manifest NB-03 |
| DC-D-100 (cont.) | all eleven classes | **`UNKNOWN`** — no benchmark, no failure-rate evidence, no incumbent evaluation. *"Custom will recover in time"* is exactly as unevidenced as the platform claim | manifest NB-07; `automation-architecture.md` §8.7, §3.B row 19 |
| DC-D-101 Observability depth | ALT-006 | CAUTION — *"There are cost implications for storing and querying logs"*; two surfaces to correlate, with **no platform-provided correlation** unless the design propagates an explicit id | `automation-architecture.md` §8.6; `alternatives.md` ALT-006 |
| DC-D-102 Incident response and support tier | ALT-005, ALT-006 | CONSTRAINED — monitoring, alerting, incident response, backup, recovery, drills and retirement must all be built **and staffed** | `alternatives.md` ALT-005, ALT-006 |
| DC-D-102 (cont.) | ALT-011, ALT-001, ALT-007 | CANDIDATE — an operator already exists and is funded | `alternatives.md` ALT-007, ALT-011 |
| DC-D-104 Operational maturity class | every class carrying an external component | **UNAVAILABLE** at a two-class gap with no funded plan | `decision-intelligence-matrix.md` §3 (Block D composed row); `architecture-patterns.md` §5.1 |
| DC-D-105 Vendor lock-in and portability | ALT-005 | CANDIDATE — the only class the corpus can name for `FULL PORTABILITY REQUIRED` | `platform-suitability.md` PS-51 |
| DC-D-105 (cont.) | ALT-008 | **`UNKNOWN`** — *"a platform that runs on the customer's own cluster is not thereby portable off that vendor. Do not infer."* | `alternatives.md` ALT-008 |
| DC-D-106 Exit strategy and switching cost | ALT-005, ALT-008 | **`UNKNOWN`** — a *tested* exit is not evidenced as achievable on **any** platform in this corpus; the redirect to a conventional stack is a candidate, not a finding | `platform-suitability.md` PS-51; `alternatives.md` §6 |
| DC-D-108 Deployment-model constraint | ALT-008 | **EVIDENCE-BACKED — the corpus's only comparative axis.** At least one enterprise low-code platform documents generally-available Kubernetes-based private-cloud and on-premises deployment including *"fully air-gapped private clouds or on-premise"* | `anti-patterns.md` §6 V-D-04 (vendor documentation, capability facts only) |
| DC-D-108 (cont.) | ALT-008, second comparator | CONSTRAINED — that platform's self-hosted capability is **Early Access, not generally available**; adopting it on a critical path is AP-D-057 | `anti-patterns.md` §6 V-D-04 |
| DC-D-108 (cont.) | ALT-005 | CANDIDATE — deployment location is a design choice in this class | `alternatives.md` ALT-005 |
| DC-D-110 Team skills and pro-code capacity | ALT-005, ALT-006, ALT-009 | **UNAVAILABLE** at `LOW-CODE ONLY` — *"Hybrid architecture required + no pro-dev/enterprise platform capability available → POOR FIT"* | `architecture-patterns.md` §13 row 7; `platform-suitability.md` PS-40 |
| DC-D-110 (cont.) | ALT-005, ALT-006 | **POSITIVE** at `FULL ENGINEERING CAPABILITY` — the class inherits a mature delivery capability instead of building it. Recorded because it is the one alternative-side signal in this table that points *toward* a class | `alternatives.md` ALT-005 (Delivery/ALM consequences) |
| DC-D-111 Existing enterprise platform estate | ALT-007 | CANDIDATE, with the standing caveat *"reuse is not automatic — an incumbent that cannot meet the requirements remains unsuitable"* | `integration-architecture.md` §12.1 |
| DC-D-111 (cont.) | ALT-007 | **`UNKNOWN`** on the incumbent's actual fit — assess per requirement, never assume | `automation-architecture.md` §3.B row 19; manifest NB-06 |

### 4A.3 What this section deliberately does **not** contain

No row asserts that an alternative class is faster, cheaper, more scalable, more productive or more reliable than any other — including than Power Platform. Every row is either a documented **limit** on the alternative, a documented **unavailability**, a documented **capability the alternative lacks**, an explicit **`UNKNOWN`**, or the single documented **positive** on DC-D-110.

The consequence is deliberate and should be stated plainly to anyone using this material: **on the four questions most often asked of a decision model — which is cheaper, which is faster, which scales further, which is more reliable — Block D's answer is `COMPARATOR EVIDENCE ABSENT`, in every direction, for every class.** Closing that requires the research commissions in `alternatives.md` §6.

### 4A.4 What a pack must render

For any criterion producing an exit, the terminal statement has **four separable parts**, and a pack must not collapse them:

1. **Exclusion** — *Power Platform is excluded, at which scope* (`Xp` whole scope · `Xr` the named responsibility · `Xe` on commercial grounds · `Xc` only in the registered combination). **`Ri` and `Cf` are not exits and must not enter this step**: an `Ri` states an in-platform redirect and an unresolved `Cf` states an open elicitation dependency. §2.5's class → outcome mapping is authoritative.
2. **Candidate generation** — which `ALT-NNN` classes come into scope (`alternatives.md` §5.1).
3. **Comparative evaluation** — the signals in §4A.2, or `COMPARATOR EVIDENCE ABSENT`.
4. **Preference** — permitted **only** where step 3 returned an evidenced signal that discriminates between the candidates. On current evidence that is one axis: DC-D-108's deployment model.

Steps 1 and 2 are almost always available. Step 3 is available on 28 criteria. Step 4 is available on one.

---

## 5. Decision-blocking criteria — handling insufficient evidence

### 5.1 The rule

Manifest §5 is explicit: an `UNKNOWN` must not be silently inferred; it is preserved, converted into a required validation, test or input, or it **blocks the local decision** where it is decision-critical.

Block D adds the operational form: **28 of the 116 criteria block a decision unconditionally when unknown**, and three more block a named narrower scope (`B*`, below). For these, the correct output is

`DECISION BLOCKED — MORE EVIDENCE REQUIRED`

together with the named evidence task, its owner and its expected duration. This is a legitimate engagement outcome, not a failure to decide — and it is materially better than the alternative, which is a confident recommendation resting on a guess.

### 5.2 The blocking set

| Id | Criterion | Why proceeding without it is unsafe | How it is closed |
|---|---|---|---|
| DC-D-001 | Business criticality | Sets the artefact structure, environment class, ownership model, validation level and licence footprint. Wrong class = wrong architecture and wrong cost. | Business impact assessment with the sponsor |
| DC-D-006 | Accountable business ownership | Gates specific patterns outright (replication, hybrid, bidirectional sync). Detection does not produce a working owner. | Name the owner; name the four reconciliation roles |
| DC-D-009 | User population identity class | Selects the surface, environment topology, licensing model and security review depth simultaneously. | Population and identity inventory |
| DC-D-021 | System of record per entity and field | Every data and integration decision follows from it; no vendor definition exists to borrow. | Entity/field ownership matrix with business owners |
| DC-D-033 | Data residency and sovereignty | Decided **at environment creation and irreversible**. | The regulation or contract clause, verbatim |
| DC-D-036 | Integration ownership | Step 1 of the topology test; skipping it produces the point-to-point estate. | Consult the platform-owning team; obtain the contract |
| DC-D-037 | Frequency distribution and peak shape | No mechanism can be sized without a peak figure. | Measure or model peak per minute |
| DC-D-039 | Per-mechanism throughput ceiling | `CONFLICTED` by 20× on the main extensibility mechanism (**NB-02**, re-verified 2026-09-03). | Re-read current documentation **and** measure representative workload |
| DC-D-040 | Sustained end-to-end throughput at horizon | Produces the clearest platform-exit verdict; absent, both staying and leaving are unevidenced. | Volume projection with growth + weakest-participant capability |
| DC-D-044 | Network boundary and private connectivity | Preconditions are irreversible (immutable subnet and DNS, region pinning) and licence-bearing. | Network policy clause + endpoint inventory |
| DC-D-052 | Idempotency key availability | Retry is on by default and duplicates side effects; a missing key is a scope item, not a detail. | Confirm a stable business key exists or fund creating one |
| DC-D-054 | Failure semantics after partial completion | There is no rollback; absent an answer, the failure behaviour is whatever the implementation happens to do. | Define the required post-failure state per operation |
| DC-D-058 | Data sensitivity classification | Determines the mandated control set and therefore the cost. | Classification against the organisation's own scheme |
| DC-D-059 | Regulatory and contractual compliance regime | Can mandate something documented as unavailable (administrator exclusion, datacentre disclosure). | Read the clauses; enumerate mandated controls |
| DC-D-061 | External identity requirement | Selects surface, environment and licence model; cross-tenant entitlement recognition is conditional. | External population and identity inventory |
| DC-D-070 | Organisational governance maturity | Where there is no operator, hybrid and boundary patterns are **unavailable, not merely expensive**. | Name the owning teams, or record their absence |
| DC-D-073 | Support and operational ownership | The vendor's support does not fill this gap; an internal first line is mandatory. | Name the first line and the support tier |
| DC-D-080 | Reversibility requirement | The mechanism must be **enabled before it is needed**; there is no rollback. | Choose, enable and rehearse a mechanism |
| DC-D-085 | User concurrency | No figure is published anywhere; quoting one is invention. | Load test against a production-like environment |
| DC-D-086 | Request rate per acting identity | Amplification is a property of the solution's own customisation and is never published. | **Measure** on a prototype with the named instrumentation |
| DC-D-087 | Peak load shape and growth horizon | The *"scale anxiety without a number"* case — neither staying nor leaving is evidenced. | Growth model with a stated basis |
| DC-D-091 | End-to-end availability of the composed flow | Platform availability ≠ solution availability (**NB-03**). | Per-flow dependency map with each dependency's position |
| DC-D-092 | Budget envelope and funding model | An unfunded mandated control makes an option economically infeasible. | Confirm the envelope and its owner |
| DC-D-093 | Entitlement fit of the required capability set | One connector decision can move the whole population from seeded to paid; the general documentation is not authoritative on licensing. | Licensing guide + the customer's agreement, named owner |
| DC-D-100 | Recovery point and recovery time objective | No cross-region recovery-time commitment is published; a contractual objective must rest on the customer's own drills. | Objectives per flow + a timed drill |
| DC-D-104 | Operational maturity class | A two-class gap means the commitment cannot be delivered. | Honest assessment of current operating practice |
| DC-D-108 | Deployment-model constraint | Can eliminate the platform entirely; must precede all architecture work. | The clause stating where the runtime must execute |
| DC-D-110 | Team skills and pro-code capacity | Gates hybrid and custom options; a design needing absent capability is a documented risk. | Capability inventory, distinguishing available from planned |

**Additionally blocking on a narrower scope (`B*`).** These three do not block the decision as a whole; each blocks a named part of it, and the register marks them `B*` so §5.2's set stays exactly the 28 above.

| Id | What it blocks | Why |
|---|---|---|
| DC-D-113 | The **commercial model** for resale | The corpus contains no evidence on multi-tenant resale licensing at all |
| DC-D-115 | Any **commitment resting on a preview or unshipped capability** | `PREVIEW ON CRITICAL PATH` and `DEPENDS ON UNSHIPPED CAPABILITY` block until re-verified or descoped; two facts already changed once during the corpus's own life |
| DC-D-116 | The **commercial and governance model** for an agent surface, at `TASK-COMPLETING AGENT` and above; and additionally the **modality question itself** at `AUTONOMOUS AGENT` | Consumption is *"dependent on the complexity of the task"* and therefore unmodellable in advance; agent-specific governance rules are *"evolving"* and agent authentication/channels are recorded as preview and unresearched (`governance.md` GOV-U-06); `automation-architecture.md` U-14 records the *"should this be an agent instead of a flow?"* question as an **unowned deferral** |

### 5.3 What is *not* decision-blocking

The remaining 88 criteria can be left `UNKNOWN` with a recorded assumption, provided the assumption is stated, owned and dated. The distinction matters: a pack that treats every unknown as blocking will never produce a recommendation, and one that treats none as blocking will produce confident nonsense. The 28 above are the set where the corpus's own evidence says proceeding is a bet rather than a decision.

---

## 6. Outcome classes — the closed terminal set

**Repair note (2026-09-03).** The first version of this section named its non-Power-Platform outcomes `CUSTOM DEVELOPMENT PREFERRED`, `EXISTING ENTERPRISE PLATFORM PREFERRED` and `BUY — PACKAGED PRODUCT OR SERVICE`. Those are **preference claims**, and the corpus holds no comparative TCO, no comparative benchmark and no evaluation of any incumbent or product. Every internal caveat in four files was discarded at the one boundary where it matters most — the sentence that lands in a decision record. The classes below fix that. They also close two other defects: §6 previously had **no explicit rejection class** at all, while `anti-patterns.md` AP-D-059 and `decision-intelligence-matrix.md` T-14 were emitting `POWER PLATFORM POOR FIT` and `POWER PLATFORM IS ECONOMICALLY UNATTRACTIVE`, which §6 never defined.

### 6.1 The governing rule

> **Exclusion, candidate generation, comparative evaluation and preference are four different statements. A terminal outcome must not collapse them.**
>
> Block D can, on evidence, say *"Power Platform is excluded for this scope"* and *"these classes come into scope"*. It can say something about a comparator only on the 28 criteria of §4A.2, and it can state a **preference between candidates** only where §4A.2 returns a signal that discriminates between them — on current evidence, one axis (DC-D-108, deployment model).
>
> This is `alternatives.md` §9 made governing rather than advisory: *"A decision model built on this must be strong on **disqualification** and modest on **preference**."*

Two rules follow, and a pack must enforce both.

1. **No outcome class may contain the word "preferred", "better", "cheaper" or "faster" about a class the corpus has not evaluated.** The permitted form is *excluded → candidates → evidence obligation*.
2. **Every non-Power-Platform terminal outcome carries `COMPARATOR EVIDENCE ABSENT` unless §4A.2 says otherwise.** The marker is part of the outcome, not a footnote to it.

**The one narrow exception, and why it is not a preference (added 2026-09-03).** Class 13 names a specific alternative without class 8 in exactly one situation: where the corpus **states that alternative's sufficiency for the requirement shape in its own words**. Today that is ALT-003 on the four shapes `data-architecture.md` §6 and `anti-patterns.md` AP-D-008's Exceptions state positively — the document is the record; a small flat tracker with one or two lookups, list-level security and low write concurrency; a form whose audience is the list's audience; team scope matching seeded entitlement. `alternatives.md` ALT-003 records the corpus's own framing: *"In these cases it is not a compromise — it is the documented recommendation."*

This is **not** the comparative claim rule 1 forbids, and the distinction is worth stating precisely because it is the one place a reader could think the rule had been relaxed:

- It is a statement about **one class's documented sufficiency for a named shape**, sourced to the vendor's own guidance. It is not a ranking, and it does not survive outside those four shapes.
- It asserts **nothing** about cost, speed, scale or reliability relative to any other class. Class 13's *"lighter option"* clause is scoped to the entitlement fact the corpus does state — the collaboration surface runs on seeded licences the organisation already holds (DC-D-093) — and never to a comparative TCO, which `licensing-cost.md` LC-U-04 records as absent. §6.2's render template carries this scoping in the **string itself, not only in this paragraph**: the comparative clause is emitted only in class 13's form (a), where ALT-003 is the substituted class; form (b) — ALT-001, ALT-011 or any other candidate — carries `COMPARATOR EVIDENCE ABSENT` and no comparative word at all.
- **Power Platform is not excluded**, which class 13 must say. Where the requirement crosses any of AP-D-008's triggers, class 13 does not apply and ALT-004 is the answer.
- For every class other than ALT-003, class 13 is followed by class 8 and carries `COMPARATOR EVIDENCE ABSENT` like everything else. **The exception is one class on four documented shapes, not a general licence.**

### 6.2 The classes

**Repair note V2 (2026-09-03).** The V1 set declared itself closed and was not: `decision-intelligence-matrix.md` T-01 emitted `COLLABORATION-PLATFORM NATIVE` and T-05 emitted `single platform + a tripwire`, neither defined here. The stray labels were the symptom; the cause was that the set had **no class for an outcome in which Power Platform is not excluded and an alternative is nonetheless the documented answer** — which is ALT-003's own outcome and the commonest departmental shape in this domain. Class 8 is the terminal form *for exclusions*, so it could not carry it, and a pack forced to choose between dropping the branch and inventing a class would have biased toward Power Platform on exactly the case where the corpus is most explicit that over-engineering is a real cost. A second gap sat under T-10: a composed row concluding *"cannot be brought to the required class in place"* is not *"the option is unavailable"*, so class 5 does not fire and class 8 alone was carrying a conclusion the set never defined.

V2 adds **class 13** and **class 14**, and states the closure rule as a check rather than an assertion. The twelve existing numbers are unchanged, because `anti-patterns.md` AP-D-003, AP-D-035, AP-D-059 and AP-D-061 and eight matrix scenarios cite them by number; the new classes are appended for the same lineage reason DC-D-116 was.

Fourteen classes. The set is **closed**, and closure is a testable property, not a claim: **every outcome string emitted anywhere in `anti-patterns.md` or `decision-intelligence-matrix.md` must appear verbatim in the table below.** A label that does not appear here is a defect in the emitting file, not a new class.

| # | Outcome | Generated when | Evidence anchor |
|---|---|---|---|
| 1 | **POWER PLATFORM — STRONG FIT** | Positive signals across the relevant criteria; no exit of any class; no composed disqualifier; entitlement funded; operating model matches the criticality class. Phrased as *"no documented constraint violated"*, never as endorsement. | `platform-suitability.md` §1 |
| 2 | **POWER PLATFORM — FIT WITH CONSTRAINTS** | One or more caution signals with **funded, owned** mitigations; the conditions are stated as conditions and carried into the decision record. | `platform-suitability.md` §1 CONDITIONAL |
| 3 | **POWER PLATFORM + CLOUD-NATIVE HYBRID** | An `Xr` exit on a bounded, nameable excess (compute, guarantee, duration, protocol, network reach, secret-free identity) **and** DC-D-070 / DC-D-110 / DC-D-073 / DC-D-083 / DC-D-104 all satisfied (§4A.2 makes them `UNAVAILABLE` gates, not preferences). | `architecture-patterns.md` AP-05; `alternatives.md` ALT-009 |
| 4 | **POWER PLATFORM + ENTERPRISE-SYSTEM HYBRID** | An `Xr` exit on the integration or authority responsibility; the incumbent keeps authority and the contract; the platform supplies experience and human workflow. Carries `INCUMBENT FIT UNEVALUATED` (NB-06). | `integration-architecture.md` §12.1; `alternatives.md` ALT-007 + ALT-009 |
| 5 | **POWER PLATFORM — POOR FIT** | An `Xp` exit fires, **or** a composed disqualifier (`Xc` combination, matrix §3) concludes the option is unavailable. This is the explicit rejection class the first version lacked; `platform-suitability.md`'s own classification model carries `POOR`. | `platform-suitability.md` §1 POOR; `anti-patterns.md` AP-D-059 |
| 6 | **POWER PLATFORM — EXCLUDED FOR THIS RESPONSIBILITY** | An `Xr` exit fires and no in-scope hybrid shape is available, or the responsibility is the whole deliverable. **Names the responsibility.** The platform may remain the correct answer for the surrounding scope, and the outcome must say so. | §2.5 `Xr`; `integration-architecture.md` §12.9 (*"one difficult step"*) |
| 7 | **POWER PLATFORM — ECONOMICALLY UNATTRACTIVE OR INFEASIBLE** | An `Xe` exit fires: the required entitlement, control population or operational tier is unfunded or disproportionate to the value. **Infeasible** where a mandated control is unfunded; **unattractive** where it is a proportionality judgement. **Never** implies another class is cheaper. | `licensing-cost.md` §6, LC-30; `anti-patterns.md` AP-D-061, AP-D-064 |
| 8 | **CANDIDATE SET — COMPARATIVE FIT UNEVALUATED** | The terminal form for classes 5, 6, 7 and 14, and for class 13 where the alternative's sufficiency is **not** documented. Renders as: *"Power Platform \<excluded / excluded for responsibility R / economically unattractive / not remediable in place\> for this scope. Candidates: ALT-NNN, ALT-NNN. Comparative fit `UNEVALUATED` — engagement assessment required: \<the named assessment\>."* Candidates come from `alternatives.md` §5.1; the evidence obligation comes from `alternatives.md` §6. | `alternatives.md` §5.1, §6, §9 |
| 9 | **DEPLOYMENT MODEL EXCLUDES THIS PLATFORM — COMPARATOR EVIDENCED ON THIS AXIS** | DC-D-108 requires customer-hosted, private-cloud or air-gapped operation. **The only class in this set that may name a comparator on evidence:** the platform documents SaaS-only, and at least one enterprise low-code platform documents generally-available air-gapped/on-premises deployment; a second is Early Access only (AP-D-057). ALT-005 also satisfies the axis. Evidenced on **this axis alone** — every other comparative dimension stays `UNKNOWN`. | `platform-suitability.md` PS-47; `anti-patterns.md` §6 V-D-01, V-D-04; `alternatives.md` ALT-008 |
| 10 | **PROCESS REDESIGN / NO NEW APPLICATION** | Value below full cost of ownership; immature or self-inflicted process complexity; the requirement is a feature list of the outgoing tool. **Not a technology decision**, so no comparator claim arises. | `licensing-cost.md` LC-28; `alternatives.md` ALT-002 |
| 11 | **DO NOTHING / DEFER** | Economics negative; or a decision-blocking unknown unresolvable in the window; or a required control unfunded; or a dated change imminent that would alter the answer. **Not a technology decision.** | `licensing-cost.md` LC-28; `alternatives.md` ALT-010 |
| 12 | **DECISION BLOCKED — MORE EVIDENCE REQUIRED** | Any criterion in §5.2 is `UNKNOWN`; or a `CONFLICTED` value is decision-critical (DC-D-039); or a `B*` scope is engaged (DC-D-113, DC-D-115, DC-D-116). | manifest §5; §5 of this file |
| 13 | **ALTERNATIVE SUFFICIENT — POWER PLATFORM NOT EXCLUDED** *(added 2026-09-03; render template corrected 2026-09-03 — Repair V3)* | **No exit of any class fires**, and a class other than ALT-004 is the documented answer for this requirement shape — either because the corpus states it positively, or because an `Ri` redirect's destination is that class. **Renders as two forms, selected by the substituted class, and a pack must never merge them. (a) Where the substituted class is ALT-003** (the four shapes `data-architecture.md` §6 and `anti-patterns.md` AP-D-008's Exceptions state positively): *"No documented constraint excludes Power Platform. ALT-003 is the documented answer for this shape, and is the lighter option on the seeded-entitlement fact alone (DC-D-093) — no comparative TCO is asserted. Graduation trigger: \<the named DC-D-074 / DC-D-001 condition\>."* **(b) Where the substituted class is a candidate rather than a documented sufficiency** (ALT-001, ALT-011, or any other class §6.1 admits here): *"No documented constraint excludes Power Platform. ALT-NNN is a candidate for this shape. `COMPARATOR EVIDENCE ABSENT` — engagement-level evaluation required. Graduation trigger: \<the named DC-D-074 / DC-D-001 condition\>."* **Two mandatory parts in both forms.** (i) It must state that Power Platform is **not excluded**, so the class can never be read as a rejection. (ii) It must carry a **graduation trigger**, because the documented growth path out of the collaboration and team-hosted surfaces is a **one-way upgrade** that converts every user to premium. Form (a) stands alone; form (b) is followed by class 8. **The comparative clause exists only in form (a), scoped to the DC-D-093 entitlement fact, and never in form (b).** *(V1/V2 defect, repaired here: the clause previously sat outside the substitution slot and was emitted unconditionally, pricing ALT-001 and ALT-011 on no evidence — `block-d-gate.md` finding V2-M-01/G-M-01.)* | `application-architecture.md` AA-36 rung 0, AA-20, AA-50 (one-way upgrade); `data-architecture.md` §2 row 7, §6; `licensing-cost.md` LC-28, LC-U-04; `operations-support.md` §1.1; `anti-patterns.md` AP-D-008 Exceptions, AP-D-005, AP-D-039, AP-D-065; `alternatives.md` ALT-003, ALT-001, ALT-011 |
| 14 | **IN-PLACE REMEDIATION UNAVAILABLE — MIGRATION REQUIRED** *(added 2026-09-03)* | A **registered** composed row concludes that the existing artefact **cannot be brought to the required class in place** — distinct from class 5, because the option is not unavailable: the same platform is a legitimate candidate **rebuilt**. Renders as: *"The workload cannot be brought to the \<required\> class in place: \<the named mechanisms\>. The work is a migration, not a remediation. Candidates: ALT-NNN…"* followed by class 8. **The class exists because the remediation estimate a sponsor is usually given is for the wrong work.** | `decision-intelligence-matrix.md` §3 (Block D composed row 3); `governance.md` G-03; `operations-support.md` O-05, O-10; `alm-devops.md` ALM-14; `anti-patterns.md` AP-D-036, AP-D-040, AP-D-047, AP-D-066, AP-D-059 |

**Why 13 and 14 sit after `DECISION BLOCKED`.** Numeric position carries no ordering and no preference (§6.4). The twelve V1 numbers are cited by number from `anti-patterns.md` and from eight matrix scenarios, and renumbering them to put the new classes in semantic order would break exactly the lineage discipline manifest §4 exists to protect — the same reason DC-D-116 is numbered outside its domain's range (§3).

### 6.3 What was removed, and what replaced it

| Removed class | Why | Replacement |
|---|---|---|
| `CUSTOM DEVELOPMENT PREFERRED` | Preference claim. `alternatives.md` ALT-005 Confidence: *"The comparative claims are deliberately absent, because the corpus holds no comparative TCO or benchmark evidence."* | Class 5, 6 or 7 + class 8 naming ALT-005 as a candidate |
| `EXISTING ENTERPRISE PLATFORM PREFERRED` | Preference claim about a class the corpus evaluates **not at all**: *"no Microsoft or independent source evaluates incumbent BPM/ESB platforms; treat as reasoning, not evidence."* | Class 4 (hybrid, where authority stays) or class 8 naming ALT-007 as a candidate with `INCUMBENT FIT UNEVALUATED` |
| `BUY — PACKAGED PRODUCT OR SERVICE` | Preference claim. No product was evaluated and no comparative pricing was fetched. | Class 8 naming ALT-011 as a candidate; the buy-check obligation itself is carried by DC-D-002 and `application-architecture.md` AA-36 rung 0 |
| `ANOTHER LOW-CODE PLATFORM SHOULD BE EVALUATED` | Correct in substance but under-specified: it did not distinguish the one evidenced axis from the six candidate ones. | Class 9 for the evidenced axis; class 8 naming ALT-008 as a candidate everywhere else |
| `COLLABORATION-PLATFORM NATIVE` *(withdrawn 2026-09-03)* | Emitted by `decision-intelligence-matrix.md` T-01 and defined nowhere. It was carrying a real outcome the set could not express — see the V2 note in §6.2. | **Class 13**, naming ALT-003, with the graduation trigger mandatory |
| `single platform + a tripwire` *(withdrawn as an outcome label, 2026-09-03)* | Emitted by T-05 and defined nowhere. It is the corpus's own phrase (`automation-architecture.md` AT2-53, §4 row 22) for a **condition on a fit**, not a terminal class: the hybrid was triggered and its operator gate failed, so the responsibility stays in-platform with the constraint documented. | **Class 2**, with the tripwire stated as the named condition and the metric that would force the move. The corpus's phrase is retained as the condition's wording, not as a class name |

Nothing that the model could previously conclude has been removed, and two things it concluded without a class now have one. **T-07, T-12, T-13 and T-14 still reject or displace Power Platform on exactly the same evidence** — they now say so without asserting a comparison the corpus never made.

### 6.4 Two standing rules about outcomes

**They are not mutually exclusive by phase.** A `DECISION BLOCKED` outcome usually names the outcome it *would* produce under each resolution of the unknown, which is what makes the evidence task worth funding. This remains the single most useful property of the model.

**They are not ordered by preference.** The corpus's evidence supports disqualification far more strongly than preference (`alternatives.md` §9), so a pack should be confident when rejecting, explicit about conditions when accepting, and honest that "which alternative wins" is an engagement calculation the research does not contain. Numeric order carries nothing — see the note on classes 13 and 14 in §6.2.

**One outcome per scope, not one per engagement (stated explicitly 2026-09-03).** An `Xr` exit takes a *named responsibility* off the platform and leaves the rest, so a single engagement legitimately terminates in **more than one class, each bound to a named scope** — class 2 for the application and class 3 for the analytical responsibility (T-06); class 5 for a consumer surface and class 1 or 2 for the operations behind it (T-13); class 6 for an integration responsibility and class 4 where the incumbent keeps authority (T-12). A pack must therefore render *(scope, class)* pairs and never collapse them into one verdict, because collapsing them is how a bounded `Xr` becomes a whole-solution rejection. This was already how the matrix's scenarios behaved; it was never stated as a rule, and §6.2's class-8 antecedent depends on it.


---

## 7. Volatility register

Volatility has **two classes** here, and the first version of this file registered only one. §7.1 is the commercial and licensing register as originally written. §7.2 is the service-limit register the original omitted, together with the withdrawal of a mitigation this file claimed and did not implement.

### 7.1 Commercial and licensing volatility

Ten criteria carry values that are date-sensitive and require verification at decision, implementation and renewal time. Manifest §5's `VOLATILE VALUE` rule applies: canonicalisation does not freeze these.

| Id | Criterion | What is volatile | Re-verify at |
|---|---|---|---|
| DC-D-039 | Per-mechanism throughput ceiling | The custom-connector figure is **`CONFLICTED` by 20×** and the conflict is live in currently-maintained pages (re-verified 2026-09-03). Connector counts are licence-conditional. | Every engagement, before sizing |
| DC-D-051 | Event frequency floor and trigger freshness | Per-licence polling intervals are an open unknown in three canonical areas; one page's figures may be stale. | Every engagement, per connector |
| DC-D-072 | Connector and service permissibility posture | New connectors are added to the default group over time; a policy check is valid on its date only. | Before design commitment, per environment |
| DC-D-086 | Request rate per acting identity | Published figures are **transition-period tolerances with no announced enforcement date**; the concurrency default *"might be higher"* per environment. | Design time, and on any enforcement announcement |
| DC-D-093 | Entitlement fit | Licensing is not authoritatively documented in the general documentation; prices are labelled illustrative; whether one premium connector obliges premium entitlement for every user of an artefact is an open item. | Options, implementation and renewal |
| DC-D-094 | Audience and frequency shape | Several meters are preview; metering units (browser cookie, contact record) have documented over-count behaviour. | Options and renewal |
| DC-D-095 | Capacity consumption profile | Add-on assignability was constrained during the transition period; analytical-replication storage ratio is unpublished. | Design time and annually |
| DC-D-096 | External and hybrid service consumption cost | Cloud pricing and tier capabilities change; gateway-at-scale cost is an open item. | Options and renewal |
| DC-D-113 | Multi-tenancy and resale requirement | Resale and multi-tenant licensing is an **unclosed deferral** in the corpus. | Before any resale commitment |
| DC-D-115 | Roadmap and preview dependency | Preview and general-availability states change; two facts in the corpus **already changed once** during its own life. | Every engagement, and before encoding |

These ten are `VOLATILE VALUE` on their **commercial** dimension. Every other criterion is `STATIC PRINCIPLE` in the sense that matters — **the question is durable** — but that is not the same as saying the figures inside them are. See §7.2.

### 7.2 Service-limit volatility — the class the register originally missed

**Repair note (2026-09-03).** §7.1 registers **commercial and licensing** volatility only. Manifest §5's `VOLATILE VALUE` definition explicitly also covers *"quota, limit, feature-state"*, and this file previously asserted a mitigation for the other criteria that **was never implemented**: *"Where a static criterion's decision impact quotes a figure, the figure carries its own source and date in the lineage."* No `Lineage` field in this file carries a date. That sentence is **withdrawn** and replaced by the register below, because a stated-but-unimplemented mitigation is worse than a named gap.

The damage this closes is downstream rather than present: today most matrix exit cells are phrased qualitatively (*"beyond 30 days as a single run"*, *"sub-15-minute freshness"*) and the figures behind them were current at the derivation date. A pack authored from the `Decision impact` fields without this register would encode a 2026 service limit as a **timeless decision rule** — the brief's own `BAD` example.

**Twenty criteria carry a service limit, quota or feature-state figure inside a `Decision impact` field.** The set was derived mechanically from the criterion bodies, not by judgement; two apparent hits were excluded as false positives (DC-D-059's *"§4 row 6"* is a section reference; DC-D-037's *"60,000 records per hour and 1,000 records per minute"* is the corpus's own illustration of *shape*, not a limit).

| Id | Figure(s) embedded in `Decision impact` | Re-verify at |
|---|---|---|
| DC-D-018 | External-site cache floor (15 minutes) and the surrounding freshness window | Options, and before any freshness commitment |
| DC-D-023 | Delegation ceilings (default and maximum) | Design time, per data source |
| DC-D-025 | Content-throughput-per-24-hours meter by owner profile | Design time, and on any licence change |
| DC-D-026 | List-store scale threshold used as the access-granularity boundary | Design time |
| DC-D-027 | Audit retention and log-availability windows | Options, and at any compliance review |
| DC-D-031 | Aggregation ceiling and the analytical-replication refresh window | Design time, before any reporting commitment |
| DC-D-032 | Backup retention windows by environment class | Options and renewal |
| DC-D-039 | *(already `V` — §7.1)* per-mechanism ceilings; **`CONFLICTED` by 20×** | Every engagement, before sizing |
| DC-D-040 | The over-limit disablement countdown | Design time |
| DC-D-043 | Payload ceilings by mechanism | Design time, per stream |
| DC-D-044 | Gateway host minimum and network preconditions | Design time, before any network commitment |
| DC-D-048 | Run-duration ceiling as a shape boundary | Options |
| DC-D-049 | Run-duration ceiling and the trigger-inactivity window | Options, before any long-running design |
| DC-D-051 | *(already `V` — §7.1)* trigger polling intervals | Every engagement, per connector |
| DC-D-055 | The human-decision window used as the in-platform boundary | Options |
| DC-D-056 | Interface-automation throughput and payload figures | Design time |
| DC-D-100 | Backup and restore windows underpinning the recovery objective | Options, and before any recovery commitment |
| DC-D-101 | Native telemetry retention window | Options, and before any observability commitment |
| DC-D-103 | Native audit/diagnostic retention window | Options, and at any compliance review |
| DC-D-116 | *(already `V` — §7.1)* request bucket, credit entitlement with a dated removal, preview feature-states | Every engagement |

### 7.3 The rule a pack must inherit

**A figure inside a `Decision impact` field is exclusion evidence with a shelf life, never a permanent decision rule.** Three consequences:

1. A pack encodes the **question and the boundary shape** (*"is the required freshness below the documented external-site floor?"*), not the number (*"is it below 15 minutes?"*).
2. Where the number must appear — because the engagement has to test a real requirement against it — it is **re-read from the current documentation at the decision date**, and the reading is recorded with its date on the engagement's own row, not baked into the pack.
3. §2.3's rule holds and is the reason this is survivable: **no published figure is a state name.** Revalidating a limit changes one sentence, not a taxonomy. Verified across all 116 criteria — the only numerals in any state name are the population bands (`TENS`, `HUNDREDS`, `THOUSANDS`) and DC-D-035's `2–5 STREAMS`, which are semantic anchors rather than product limits.



---

## 8. Lineage map

Manifest §4 forbids renaming canonical identifiers, so the local `DC-NN` namespaces in Areas 9, 10 and 11 remain valid **within their own files**. This map records where each went. It is the audit trail for the consolidation claimed in §1.3.

### 8.1 `performance-scale.md` DC-01 … DC-20 → canonical

| Local | Canonical successor(s) |
|---|---|
| DC-01 largest-table rows + free filter/sort/aggregate | DC-D-023, DC-D-088 |
| DC-02 relationship depth in one view | DC-D-022, DC-D-088 |
| DC-03 records created/updated per identity per 5 min | DC-D-086 |
| DC-04 all traffic through one account | DC-D-086, DC-D-009 |
| DC-05 data freshness on screen | DC-D-018 |
| DC-06 shortest interval between events | DC-D-051 |
| DC-07 step completes while caller waits | DC-D-050 |
| DC-08 how long a process instance stays open | DC-D-049 |
| DC-09 megabytes of documents per day | DC-D-025, DC-D-043 |
| DC-10 ordering required, at what volume | DC-D-053, DC-D-041 |
| DC-11 users, devices, network | DC-D-015, DC-D-084 |
| DC-12 step is computation not orchestration | DC-D-057 |
| DC-13 availability the business flow needs | DC-D-090, DC-D-091 |
| DC-14 survive loss of a region, committed time | DC-D-100 |
| DC-15 high-volume **and** cross-region protected | DC-D-100, DC-D-040 |
| DC-16 how often and when deployments occur | DC-D-077 |
| DC-17 must peak capacity be proven | DC-D-089 |
| DC-18 who owns the automation, what licence | DC-D-006, DC-D-093 |
| DC-19 reporting against the transactional store | DC-D-031, DC-D-086 |
| DC-20 growth, seasonal or event-driven peak | DC-D-087, DC-D-024 |

### 8.2 `licensing-cost.md` DC-01 … DC-17 → canonical

| Local | Canonical successor(s) |
|---|---|
| DC-01 which systems must be read from or written to | DC-D-035, DC-D-093 |
| DC-02 how many people, how often each interacts | DC-D-010, DC-D-094 |
| DC-03 how many distinct applications per person | DC-D-074, DC-D-093 |
| DC-04 data, files, audit retention | DC-D-024, DC-D-025, DC-D-027, DC-D-095 |
| DC-05 external or partner organisations participate | DC-D-009, DC-D-061, DC-D-094 |
| DC-06 audience anonymous, multi-device, privacy-conscious | DC-D-009, DC-D-094 |
| DC-07 API calls and dependency reliability | DC-D-086, DC-D-095 |
| DC-08 automation surviving its owner; throughput | DC-D-006, DC-D-093 |
| DC-09 unattended robotic automation required | DC-D-056 |
| DC-10 AI capability required, variability of use | *not carried* — see §9 item 6 |
| DC-11 criticality and what must be possible when it breaks | DC-D-001, DC-D-097, DC-D-101 |
| DC-12 survive loss of a region | DC-D-100, DC-D-095 |
| DC-13 environments required by governance and lifecycle | DC-D-071, DC-D-082 |
| **DC-14 (a)** mandatory security controls and enforcement population | DC-D-063, DC-D-064, DC-D-092 |
| **DC-14 (b)** cost attributed to business units | DC-D-099 |
| DC-15 is the process high-value enough to automate | DC-D-008 |
| DC-16 expected lifespan and who maintains it | DC-D-004, DC-D-112 |
| DC-17 economics dependent on transition or preview terms | DC-D-115, and `anti-patterns.md` AP-D-055 |

**Note the duplicate.** `licensing-cost.md` DC-14 exists twice with different meanings; the two are mapped separately above as (a) and (b). Downstream must disambiguate by question text, never by number. Recorded in §1.1 and `anti-patterns.md` §1.4.

### 8.3 `operations-support.md` DC-01 … DC-20 → canonical

| Local | Canonical successor(s) |
|---|---|
| DC-01 who notices, how quickly must someone act | DC-D-006, DC-D-102, DC-D-101 |
| DC-02 who diagnoses, with what evidence | DC-D-101, DC-D-073 |
| DC-03 how far back must events be reconstructed | DC-D-103 |
| DC-04 provable audit trail required | DC-D-027, DC-D-103 |
| DC-05 what must be recoverable, from when, how fast | DC-D-100 |
| DC-06 what breaks when an environment is restored | DC-D-080, DC-D-100 |
| DC-07 survive loss of a region, and will it be drilled | DC-D-100, DC-D-089 |
| DC-08 availability each critical flow needs end to end | DC-D-091 |
| DC-09 how changes reach production and how undone | DC-D-079, DC-D-080 |
| DC-10 artefacts backed up, licensed, monitorable, deployable | DC-D-001 (via solution-awareness), DC-D-101 |
| DC-11 how often releases happen, in what window | DC-D-077 |
| DC-12 what identities the integrations run as | DC-D-068, DC-D-065, DC-D-006 |
| DC-13 what support the business expects | DC-D-102, DC-D-073, DC-D-097 |
| DC-14 who authorises vendor diagnostic access | DC-D-102 |
| DC-15 which environment types the solution lives in | DC-D-071, DC-D-090 |
| DC-16 which operational capabilities the criticality class requires | DC-D-001, DC-D-097, DC-D-104 |
| DC-17 who owns tenant capacity and the shared request pool | DC-D-095, DC-D-099, DC-D-006 |
| DC-18 who tracks platform changes and deprecations | DC-D-112 |
| DC-19 what happens when the solution is no longer needed | DC-D-075 |
| DC-20 does existing governance tooling underpin operations | DC-D-070, DC-D-112 |

### 8.4 Unnumbered criteria tables → canonical

| Source | Rows | Consolidated into |
|---|---|---|
| `integration-architecture.md` §9 (28 variables) | 1–28 | DC-D-021, 029, 035–047, 052, 065, 068, 086, 096, 103, plus DC-D-033, 072 |
| `automation-architecture.md` §9 (22 criteria) | 1–22 | DC-D-006, 041, 048–057, 065, 070, 093, 101, 103, 110, 111 |
| `security.md` §4 (20 rows) | 1–20 | DC-D-026, 033, 058–068, 073, 079, 102 |
| `governance.md` §4 (15 rows) | 1–15 | DC-D-001, 006, 069–075, 090, 093, 099, 103 |
| `alm-devops.md` §4 (16 rows) | 1–16 | DC-D-007, 044 (seam), 065, 076–083, 113 |
| `architecture-patterns.md` §3.1 (20 variables) | — | DC-D-021, 029, 035–047, 070, 091, 093 — plus §5.1's four cross-block rows → DC-D-092, 083, 104, 093 |
| `platform-suitability.md` §2/§3 | 36 rows + boundaries | distributed across all twelve domains; the fit matrix is the origin of most exit signals |
| `application-architecture.md` §1/§2 | 11 rows + boundaries | DC-D-009–020, 074, 078 |
| `data-architecture.md` §2/§3 | 27 rows + boundaries | DC-D-021–034, 088, 095 |
| `performance-scale.md` §4 (B-01…B-17) | 17 boundaries | DC-D-023, 040, 042, 050, 057, 084–091, 100 |

### 8.5 `licensing-cost.md` DC-10 — carried, after being wrongly dropped

**Repair note (2026-09-03).** This section previously recorded `licensing-cost.md` DC-10 (AI and assistant capability consumption) as **deliberately not carried**, on the ground that no per-operation consumption figure is published, that per-interaction consumption is an open unknown making *"agent economics unmodellable in advance"*, that a bundled allocation has a dated removal, and that governance of the capability is *"preview; not researched here"*.

**Every one of those statements is true, and none of them justified the omission.** They are all statements about **economics and governance maturity** — and the corpus carries substantive *non-economic* agent evidence in governance, security, ALM and operations which was not carried forward at all: agents as governed artefacts in the tenant inventory and in managed-environment sharing rules; the advanced connector policy's documented and **permanent** non-coverage of virtual connectors; the Graph-connector guest-access bypass; the *block unmanaged customizations* versus agent-publishing conflict; the absent maker monitoring surface; and the exclusion of agent conversation runtime from self-service disaster recovery.

The inconsistency was internal to this file. **DC-D-113** (multi-tenancy and resale) is carried as a full criterion with `LOW` confidence, an explicitly empty evidence base, a `V` flag and a blocking status on the commercial model — which is the correct treatment of a decision-relevant requirement whose evidence is absent. Agents received the opposite treatment for the same situation.

`licensing-cost.md` DC-10 is therefore now carried, as **DC-D-116** (§4.2), on the DC-D-113 pattern: the evidence that exists is encoded, the economics are preserved as `UNKNOWN`, and the criterion **blocks** on the commercial and governance model rather than guessing. The corpus's own instruction where a figure is needed still applies and is stated in the criterion: establish consumption **empirically in a pilot** and size for the peak period.

**The residual gap is a research follow-up, not grounds for omission.** No fit assessment of the agent surface exists anywhere in the corpus — `platform-suitability.md` and `application-architecture.md` carry **zero** mentions — and `automation-architecture.md` U-14 records the *"should this be an agent instead of a flow?"* question as a deferral that **has no owner**. §9 item 6 records the commission.

**Local criteria deliberately not carried: 0.**

---

## 9. Evidence-quality notes

1. **Derivation, not discovery.** All 116 criteria are extracted from Areas 1–12. Their confidence is inherited from and capped by the canonical findings they cite. Four criteria additionally rest on the external checks in `anti-patterns.md` §6: DC-D-039 (V-D-02/V-D-03), DC-D-108 and DC-D-105 (V-D-01/V-D-04).
2. **Consolidation ratio and its risk.** 236 local criteria → 116 canonical. Merging loses the originating area's framing, which is why every entry carries a `Lineage` field naming its sources file-qualified. A reviewer should spot-check the merges in §8.4, where several areas' vantage points collapse into one criterion (DC-D-006, DC-D-093 and DC-D-101 are the widest merges and the most likely to have lost nuance).
3. **`UNKNOWN` and `CONFLICTED` preserved.** No criterion converts an open item into a threshold. Explicitly preserved: NB-01 (DC-D-021, DC-D-029), NB-02 (DC-D-039, DC-D-086), NB-03 (DC-D-091, DC-D-100), NB-04 (DC-D-026), NB-05 (DC-D-026 via virtualization), NB-06 (DC-D-036, DC-D-111), NB-07 (DC-D-084…DC-D-089); plus `LC-U-05` (DC-D-093), the unpublished concurrency figure (DC-D-085), the unpublished amplification multiplier (DC-D-086), and the polling-interval unknowns (DC-D-051).
4. **No invented thresholds.** Where a figure appears in a `Decision impact` field it is the corpus's, with its source in the lineage; where none exists, the criterion carries a measurement obligation instead. The register's `V` flags mark the ten criteria whose figures are date-sensitive.
5. **Exit signals are asymmetric by design, and the asymmetry survives three corrections in a row.** Of 116 criteria, **46 carry a direct exit** (15 `Xp`, 26 `Xr`, 5 `Xe`), **8 exit only in a registered combination** (`Xc`), **7 are in-platform redirects that are not exits** (`Ri`), **17 are combination inputs that are not exits** (`Cf`), and **38 carry no exit at all**. The history is worth keeping, because it is the clearest evidence in this file that the counting was driven by classification rather than the reverse: V0 published **36** against criteria bodies containing **48** substantive statements and a matrix carrying **46**; V1 named a five-class taxonomy and reached **54** by admitting six in-platform redirects and eighteen unregistered combinations into exit classes; V2 removed both and reached **48**; V3 re-applied V2's own one-limb test to the whole `Xr` class rather than to the criteria a prior review had named, and reached **46**. **The count went down three times.** §2.5 records each step and the test that produced it. The distribution remains uneven for the reason visible in the domain table: Governance and ALM produce **zero direct exits** between them, because the corpus's governance and lifecycle findings are about *obligations and cost*, not about capability absence. A pack that expects every domain to be able to reject the platform will invent thresholds in those two.
5b. **Two consequence classes exist because two consequences are not exits.** `Ri` (7 criteria) is a documented in-platform pattern, store or surface becoming unavailable with the answer inside the platform; `Cf` (17) is an elicitation dependency on another criterion's exit. Filing either as an exit — which V1 did — makes a pack emit an exclusion for a store change and terminate on a criterion that carries no conclusion. Both are stated with their outcome mapping in §2.5 and neither may reach an exclusion class.
5a. **The evaluation apparatus is one-sided, and §4A now says where.** All 116 criteria carry Power Platform signals; **28** carry an evidenced alternative-side signal; **88 carry none, and are marked `COMPARATOR EVIDENCE ABSENT` rather than left silent**. Exactly **one** criterion (DC-D-108, deployment model) carries comparator evidence strong enough to support a preference between candidate classes. This is a structural property of the corpus, not a defect of the extraction, and §4A.1 states the default so it cannot be lost downstream.
6. **The one scoping gap previously carried forward has been closed as far as the evidence allows.** AI and assistant-capability consumption is now DC-D-116 (§8.5), carried on the DC-D-113 pattern with its economics preserved as `UNKNOWN` and a `B*` block on the commercial and governance model. **Local criteria deliberately not carried: 0.** The residual gap — that no fit assessment of the agent surface exists in any canonical file — is a **research commission**, recorded in `alternatives.md` §6 and in `decision-intelligence-matrix.md` §8.3.
7. **Technology neutrality is near-complete.** Four criteria describe current state and therefore name estate rather than requirements (DC-D-109, DC-D-110, DC-D-111, DC-D-114); the corpus's own Discovery rule permits current-state statements. All other 112 are expressible without naming a vendor or product.
7a. **The pack-local vocabulary is undeclared, and that is a named prerequisite for authoring.** *"The governed relational store"*, *"the task-focused surface"*, *"the record-centric surface"*, *"the external-site surface"*, *"the document/list store"* and *"the team-hosted surface"* are used consistently across all four Block D files and never slip into product names — but the mapping to product names is nowhere written down. `data-architecture.md` DQ-03/U-14 requires a pack to *"declare its own vocabulary as pack-local"*. Block D correctly does **not** author that glossary (the Options phase is where the mapping is permitted to exist), but it is a **prerequisite**, not an optional extra: this material is not usable until it is written.
8. **Confidence distribution.** HIGH 57 · MEDIUM 56 · LOW 3 (DC-D-113 resale, DC-D-116 agent surface, and DC-D-102's vendor-boundary reading is MEDIUM-HIGH but its conflict is unresolved). No criterion claims HIGH confidence on a comparative statement, because the corpus holds no comparative evidence.
9. **Single author, single session**, as with Areas 1–12. §5's blocking set and §8's lineage map exist so an independent reviewer can audit the two most consequential judgements in this file — what blocks a decision, and what was merged — rather than only the criteria themselves.

---

## 10. Implications for the aisa knowledge model (pointers, not pack content)

Per `03-KNOWLEDGE-MODEL.md` the chain is Requirement → Signal → Evidence → Knowledge State → Decision Criterion → Candidate Options → Trade-offs → Risk → Validation. This file is the **Decision Criterion** link, and it is deliberately the only one it occupies.

- **Signals** would derive from each criterion's `Discovery evidence` field; they are technology-neutral wherever the evidence allowed it. The four current-state criteria (§9 item 7) need a signal form that describes the estate without prescribing a solution.
- **Knowledge states** map directly: a criterion whose value is established is Confirmed; one resting on a stated assumption is Assumed; one in §5.2 without a value is **Unknown and decision-blocking**; DC-D-039 is the model for a **Conflicted** decision-critical value; the ten volatile criteria are the model for **Confirmed with a validity date**.
- **Candidate options** come from `alternatives.md` §5.1, filtered by this file's exit signals, then reduced by the composed test.
- **Trade-offs and Risks** come from `alternatives.md`'s `*Consequences` fields and `anti-patterns.md`'s `Consequences` fields respectively.
- **Validation** obligations are concentrated in DC-D-089 (which level is required), DC-D-086 (measure amplification), DC-D-085 (load test), DC-D-039 (measure and re-read), DC-D-100 (drill) and DC-D-026 (representative pilot for authorization-heavy models).
- **The order of evaluation matters and is not commutative.** `decision-intelligence-matrix.md` §5 records it: deployment model and other absolutes first, then decision-blocking unknowns, then composed disqualifiers, then direction. A pack that evaluates criteria in register order will produce different answers from one that evaluates them in dependency order — and only the latter is supported by the evidence.
- **Scoring remains out of scope**, for the reason in §2.4 rather than merely because the brief says so.

Nothing in this section is pack content. Question banks, signal catalogues, glossaries and decision trees remain out of scope by instruction.

---

## 11. Summary

| | |
|---|---|
| Canonical decision criteria | **116** |
| Domains covered | **12** (all required by the brief) |
| Local criteria surveyed and consolidated | **236** (≈ 2:1 compression) |
| Criteria decision-blocking when `UNKNOWN` | **28** unconditionally (§5.2) · **3** on a narrower named scope (`B*`: DC-D-113, DC-D-115, DC-D-116) |
| **`Xp`** platform exits | **15** |
| **`Xr`** responsibility exits | **26** |
| **`Xe`** economic exits | **5** |
| **`Xc`** composed-only exits, each named in a registered §3 row | **8** |
| **`Ri`** in-platform redirects — **not exits** | **7** |
| **`Cf`** combination inputs — **not exits** | **17** |
| **`—`** no exit evidenced (correctly) | **38** |
| Direct exits (`Xp` + `Xr` + `Xe`) | **46** |
| Domains producing zero direct exits | **2** — Governance, ALM (§9 item 5) |
| Criteria with an evidenced **alternative-side** signal (`G`) | **28** (§4A.2) |
| Criteria marked `COMPARATOR EVIDENCE ABSENT` | **88** (§4A.1 default) |
| Axes on which a **preference between candidate classes** is evidenced | **1** — DC-D-108 deployment model (§6 class 9) |
| Volatile criteria — commercial and licensing | **10** (§7.1) |
| Criteria carrying a service-limit figure in `Decision impact` | **20** (§7.2) |
| Outcome classes supported | **14** (§6), closed set — closure testable as *every emitted label appears in §6.2* — including an explicit rejection class, an economic class, an alternative-sufficient class, a migration class, three non-technology outcomes and `DECISION BLOCKED` |
| Local criteria deliberately not carried | **0** (`licensing-cost.md` DC-10 is now DC-D-116 — §8.5) |
| Lineage defects recorded, not repaired | **1** (`licensing-cost.md` duplicate DC-14 — §1.1, §8.2) |
| Scoring model | **none, deliberately** (§2.4) |

**The single most important structural finding** is in §2.4: the corpus documents eight combinations in which every dimension is individually `CONDITIONAL` and the combination is unavailable, and Block D derives four more — **12 in total**. That is why this file produces a **semantic, ordered, non-commutative** decision layer rather than a score — and it is the finding most likely to be argued with by anyone who wants a number at the end.

**The single most important honesty constraint** is in §4A.1 and §6.1: the model can exclude on evidence and cannot prefer on evidence. `46` direct exits against `1` evidenced comparative axis is the shape of this corpus, and a pack that hides that ratio will make confident recommendations the research does not support.

`Research Status: CANONICAL` — Block D review 2026-09-03 returned `PASS WITH CORRECTIONS`; the bounded repair of H-01…H-04 and the MEDIUM/LOW findings is recorded in `block-d-repair-report.md`. The independent **re-review** 2026-09-03 returned `FAIL` (`block-d-re-review.md`: HIGH 1, gate-blocking MEDIUM 1) and this file carried the **V2 repair** of both — the exit taxonomy (§2.5, §3, §3.1, §9 item 5, §11) and the closed outcome set (§6.1, §6.2, §6.3, §6.4) — recorded in `block-d-repair-v2-report.md`. **Re-review V2** (`block-d-re-review-v2.md`) returned `FAIL` (HIGH 1 — V2-H-01, gate-blocking MEDIUM 1 — V2-M-01), and the **Block D gate** (`block-d-gate.md`) independently confirmed both as unresolved and added one dependent finding (V2-M-02 / G-M-02, non-blocking). This file carries the **bounded V3 gate repair** of all three — the `Xr` membership re-derivation and the per-row `Xc` outcome mapping (§2.5, §3, §3.1, §9 items 5/5b, §11) and the class 13 comparator clause (§6.2) — recorded in `block-d-gate-repair-report.md`. **Gate recheck performed:** `block-d-final-gate-recheck.md` returned `FINAL BOUNDED GATE RECHECK: PASS` with `NEW GATE-BLOCKING FINDINGS: 0`. Canonicalized 2026-09-03; lineage in `canonical-manifest.md`.

---
