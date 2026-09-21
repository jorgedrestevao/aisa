# Step 3A — Options Decision Model (design)

<!--
provenance: AUTHORING DESIGN (no runtime file modified)
date: 2026-09-04
scope: PP PACK AUTHORING — STEP 3A. Design only. decision-tree.md, pack.yaml, domain-knowledge/*,
       lenses, personas and orchestrators are UNCHANGED by this step.
basis (read, not reopened): decision-criteria.md (Block D, frozen) · decision-intelligence-matrix.md ·
       alternatives.md · canonical-manifest.md · pp-pack-authoring-map.md §1.5, §3.1–§3.2, §4.2, §9, §12 ·
       authoring-principle-alignment-report.md · runtime-simplification-phase-g-report.md ·
       step-2-discovery-layer-report.md · current library/packs/pp/{decision-tree.md, pack.yaml,
       glossary.md, question-bank.md} · lens-technology · solution-architect · aisa-options ·
       chairman-synthesis · aisa-simulate · kernel {phases.md, states.md, orchestration.md}
no research reopened · no web access · no runtime write
path note: `research/pp/authoring/` resolves to `docs/pp-pack-authoring/research/pp/authoring/`
-->

---

## 1. Purpose and governing doctrine

Step 3A designs the Options decision model the `pp` pack will run from Step 3B onward. It replaces a
three-branch scored tree with an **ordered, semantic, technology-neutral evaluation procedure** whose
option space is the canonical eleven `ALT` classes and whose terminal vocabulary is the canonical closed
fourteen outcome classes.

**Governing doctrine** (`pp-pack-authoring-map.md` §1.5, binding from Step 3):

| # | Principle | Consequence for this model |
|---|---|---|
| 1 | Light framework, not lightweight reasoning | 10 stages and 12 concerns are framework; the reasoning under them is unbounded |
| 2 | Compress repetition, not decision coverage | 116 canonical criteria compress to 12 concerns; **zero criteria are dropped** (§7) |
| 3 | Broad coverage, selective depth | every serious option × every material concern; depth is proportional (§6) |
| 4 | Minimum sufficient complexity | 6 runtime artifacts, not the 10 the Step-1 map projected (§24) |
| 5 | Research completeness is authoring input, not runtime payload | the `DC-D-NNN` register never loads at runtime |
| 6 | Materiality determines depth | criticality × uncertainty × consequence × reversibility set depth |
| 7 | Domain knowledge deepens a concrete decision question | pull, never preload (§10) |
| 8 | An active technology pack must be able to reject its own technology | proven in §21 |

**Two doctrines added by Block D and inherited verbatim.**

- **States, not scores** (`decision-criteria.md` §2.3–§2.4). Eight documented combinations exist in which
  every dimension reads `CONDITIONAL` and the combination is `POOR FIT`, `ANTI-PATTERN` or *unavailable*.
  A weighted average passes all eight. No numeric fit score enters this model at any point.
- **Strong on disqualification, modest on preference** (`alternatives.md` §9; `decision-criteria.md` §4A).
  The corpus holds no comparative TCO, no benchmark for any technology, no incumbent evaluation and no
  failure-rate evidence. `COMPARATOR EVIDENCE ABSENT` is the default on every criterion, and preference
  between surviving candidates is licensed on **one** axis today (`DC-D-108`, deployment model).

**The objective is not the smallest procedure.** It is the least framework that still preserves materially
complete, balanced and defensible reasoning.

---

## 2. Current Options diagnosis + Q-11

### 2.1 Disposition of `decision-tree.md` (157 lines)

| Content | Verdict | Reason |
|---|---|---|
| Front-matter `branches:` (3 branches, sub-templates) | **TRANSFORM** | 3 PP-internal architecture shapes cannot express 11 `ALT` classes × 14 outcome classes (`pp-pack-authoring-map.md` §12 F-03). Becomes *architecture shapes reachable after* an outcome class is chosen, not the option space |
| Front-matter `inputs_used:` (15 typed inputs) | **TRANSFORM** | Right instinct (declared Discovery inputs), wrong shape: a fixed 15-slot signature is exactly the ceiling Q-11 names. Becomes the Discovery→Options handoff of §8, which is open-ended |
| Intro: *"consulted in the Options phase and never before"* | **KEEP** | Phase gate is correct and enforced by `.claude/rules/no-tech-mention-before-options.md` |
| Intro: *"the solution architect aggregates verdicts and assigns scores (`forte`, `adequada`, …)"* | **REMOVE** | Hidden scoring model. `decision-criteria.md` §2.4 — a scoring model converts *"the pattern is unavailable"* into *"the pattern scores 68"* |
| R0 hard gates — *concept* | **KEEP** | Disqualification-before-direction is the canonical order (matrix §5 Step 0) |
| R0 thresholds — 30,000 rows · `formula_count > 100` · `external_integrations_count > 3` · "sub-second" · 2-decimal currency · >3 approval states | **REMOVE** | Invented numbers (`AP-D-051`). Canonical SharePoint figures are `DA-39`/`DA-40`; `SC-16`/`SC-18` record that **no** user-concurrency and **no** standard-table row ceiling are published. Also violates `decision-criteria.md` §7.3: a figure is exclusion evidence with a shelf life, never a decision rule |
| R1–R6 verdict ladders (`forte`/`adequada`/`intermédia`/`inadequada`, `baixo`/`médio`/`alto`) | **REMOVE** | Ordinal scoring by another name; commensurates a hard limit with a judgement |
| R4 licensing rules (`user_count ≤ 20` etc.) | **RELOCATE** → `volatility-register.md` + concern C11 | Commercial volatility class (`decision-criteria.md` §7.1, `DC-D-093`): *"the general documentation is not authoritative on licensing"* |
| R5 maintenance / `admin_team_capability` | **TRANSFORM** → C10 + gate stage S7 | The canonical form is stronger: at `NONE`/`EMERGING` the pattern is **unavailable, not merely expensive** (`architecture-patterns.md` §13 row 2) |
| R6 reversibility ladder | **TRANSFORM** → C12 | Keep the concern, drop the ordinal verdicts; `DC-D-080` is decision-blocking when unknown |
| Hybrid trigger (entity-count arithmetic) | **REMOVE** | Invented arithmetic. Canonical hybrid trigger is an `Xr` exit on a **bounded nameable excess** plus five satisfied gates (`decision-criteria.md` §6.2 class 3) |
| Exclusion side-effects (3 rules) | **CONSOLIDATE** into S2/S6 | Same mechanism as R0, stated twice |
| Missing-inputs protocol (Unknown → resolve or Assume, re-evaluate, log) | **KEEP** | Kernel-correct; upgraded in S3 with the blocking set and question economics |
| *"Always include a do-nothing and a non-technology option"* | **KEEP**, promote | Canonically mandatory (`licensing-cost.md` LC-28; `alternatives.md` §3), and mandatory earlier — at S1, not appended by the chairman |
| Changelog / *"Thresholds a validar com a equipa"* | **REMOVE** | Stale; the thresholds it defers are the ones being deleted |
| Cross-references to `sharepoint-reference.md` / `dataverse-reference.md` / `azure-sql-reference.md` | **RELOCATE** | Selection logic must not live in engineering reference files (`pp-pack-authoring-map.md` §7). Becomes S5 domain pull |

**Duplicated Discovery logic in the current tree.** `max_volume_per_entity`, `requires_audit_trail`,
`relational_integrity_required`, `user_count`, `formula_count`, `approval_stages_max`,
`financial_precision_decimals` are all elicited by the Step-2 Discovery layer already (`pack.yaml`
`data.*`, `operations.*`, `governance.*` cues; `question-bank.md` Q-DAT/Q-OPS/Q-GOV). The tree re-declares
them as its own inputs. **CONSOLIDATE**: Options consumes Shared Understanding rows, never a parallel
input signature (§8).

**Platform fact dumps.** None in the tree itself — but R0/R1/R4 *encode* platform facts as rules, which is
the more damaging form: a fact in a reference file can be revalidated, a fact fused into a rule cannot.

**Implementation checks.** `formula_count`, `financial_precision_decimals`, `entity_profile` are build-time
sizing inputs, not viability inputs. **RELOCATE** downstream to `/blueprint` and the estimate deliverable.

**Vendor preference.** Structural, not textual: the option space *is* three PP architectures. Non-PP options
exist only as a fallback sentence — *"If all three branches are disqualified…"* — reachable only after PP
fails three times. **This is the model's central defect** and the reason §21 exists.

### 2.2 Disposition of the surrounding Options mechanics

| Artifact | Element | Verdict |
|---|---|---|
| `pack.yaml` | `technology.constraints_to_check` (5 entries) | **TRANSFORM** → floor of 10, explicitly non-limiting (§19) |
| `lens-technology` | 5 questions per candidate · phase gate · pull-based domain knowledge · hard rules 1–6 · *"Cues, not coverage"* | **KEEP** — all correct |
| `lens-technology` | execution step 2 — *"a constraint verdict per constraint (pass / risky / blocker)"* | **TRANSFORM** — this clause is the mechanical half of Q-11. Becomes *a verdict per material concern, the declared constraints being the floor* |
| `lens-technology` | signal catalog (9 tokens) | **KEEP** as cues; **REMOVE** any reading of it as coverage — already carried by *"Cues, not coverage"* |
| `solution-architect` | *"produce 3-5 candidate options … including at least one do-nothing baseline and one non-technology option"* | **KEEP**; add: candidates are generated from the `ALT` trigger map, not from the three branches |
| `chairman-synthesis` | `options.md` template — Pros / Cons / Constraints checked / Reversibility / Effort band | **TRANSFORM** — the shape cannot express viability, disqualifiers, preconditions or decision-changing uncertainty (§16) |
| `chairman-synthesis` | *"one do-nothing baseline; one non-technology option"* floor | **KEEP** |
| `aisa-options` | 7 parallel personas · dialectic round · pull-based pack access · *"never place decision-tree.md or domain-knowledge/ contents in the prompt"* | **KEEP** — all correct, and Principle 7 depends on the last one |
| `aisa-simulate` | per-option projection + value-of-information | **KEEP**; it consumes the new comparison structure unchanged |

### 2.3 Q-11 explicitly

> **Q-11.** Today the Options layer bounds constraint evaluation to
> `lenses_config.technology.constraints_to_check` (5 entries for `pp`) plus the technology lens's 9-token
> signal catalog, and `lens-technology` execution step 2 emits *a verdict per constraint*. A material
> concern outside that fixed list can be silently omitted.

**Diagnosis.** The ceiling is produced by three mechanisms acting together, and patching any one of them
leaves it standing:

1. **A closed enumeration is the only declared coverage object.** Five keys, and nothing in the runtime
   says the list is partial.
2. **The lens emits per-constraint verdicts.** Output shape follows the enumeration, so an evaluated
   concern outside it has nowhere to land — and an unevaluated one leaves no hole.
3. **The option space is three PP branches.** A concern that would eliminate all three (deployment model,
   administrator exclusion, differentiation) has no expressible consequence, so it is never raised.

Mechanism 3 is why the alignment report was right to defer this to the decision model rather than patch
the lens: widening the list without widening the option space produces concerns with no reachable verdict.

**Resolution — four parts, all in the model, none in a longer list.**

| Part | Mechanism |
|---|---|
| R1 | The **12 material decision concerns** (§4) are the coverage object, not `constraints_to_check`. Concerns are the compression of the whole 116-criterion canonical register (§7), so the coverage object is complete by construction |
| R2 | `constraints_to_check` is redefined as a **standing-attention floor**: entries that must be examined in *every* PP Options engagement. The floor is declared non-limiting in `pack.yaml`'s own comment and in the procedure (§19) |
| R3 | The **emergent-concern obligation** (§6.3): any concern raised by the Shared Understanding, captured evidence, council reasoning or candidate-option analysis is evaluated whether or not it is declared anywhere. A concern that emerges and is not evaluated is a defect, not an omission |
| R4 | The **option space is the eleven `ALT` classes** (§5), so every concern has a reachable consequence — including concerns that eliminate every PP form |

The declared list grows from 5 to 10 (§19) because five of the current entries are under-derived, **not**
because a longer list closes the gap. It cannot: R1 and R3 close it.

---

## 3. Decision semantics

Seven terms, each bound to canonical machinery. **No parallel state machine**: the five kernel states
(`library/kernel/states.md`) carry all epistemics; these terms describe *option verdicts*, which live in
`options.md`, not in the Shared Understanding.

| Term | Definition | Canonical binding | Kernel binding |
|---|---|---|---|
| **Disqualifier** | Known evidence makes an option non-viable under a material requirement, at a named scope. **Hard** (settles non-viability) or **provisional** (conditional on an assumption) — §3.1 governs which | Exit classes `Xp` (whole scope) · `Xr` (named responsibility) · `Xe` (economic) · `Xc` (registered combination only) → outcome classes 5 / 6 / 7 / per-row | Evidence grade per §3.1; the verdict is an `options.md` field |
| **Precondition** | The option may become viable only if a stated condition becomes true — named, owned, funded, dated | Outcome class 2 conditions · class 13 graduation trigger · the five capability gates | Unresolved precondition ⇒ `Unknown` row with `custo` + `swing`; accepted precondition ⇒ decision condition in `decisions.md` |
| **Trade-off** | A material disadvantage consciously accepted; the option stays viable | Class 2 *"caution signals with funded, owned mitigations"*; `licensing-cost.md` LC-29 (low-code trades first-version cost against change cost) | `Assumed` row with basis declared |
| **Risk** | A material adverse outcome whose likelihood or impact must be understood or mitigated | `anti-patterns.md` `RISK` classification; matrix §3 row 4 | `Risky` row — impact + proposed mitigation |
| **Uncertainty** | Missing, stale or conflicted evidence capable of changing viability, architecture, risk, cost or preference | `UNKNOWN` as a first-class state on every criterion; `CONFLICTED` (`DC-D-039`, live by 20×); volatile values (§12) | `Unknown` · `Conflicted` · **expired** `Confirmed`/`Assumed` (reads as weak `Assumed`) |
| **Preference** | Evidence-backed reason to favour one viable option over another | §4A.4 step 4 — permitted **only** where §4A.2 returns a signal that discriminates. Today: one axis (`DC-D-108`) | Recorded with its evidence anchor, never as a score |
| **Decision blocker** | Uncertainty or conflict material enough that selecting a preferred option would not yet be defensible | Outcome class 12 · the 28 `B` criteria · the 3 `B*` scopes · matrix §5 Step 1 | `Unknown`/`Conflicted` with `swing: decisivo`; every `B` criterion is `swing: decisivo` by construction |

**Two non-disqualifiers that must be carried, or the V1 defect returns.**

| Term | Definition | Must never produce |
|---|---|---|
| **In-platform redirect (`Ri`)** | A documented in-platform pattern, store, mechanism or surface becomes unavailable and the documented answer is a **different in-platform choice**. Nothing leaves the platform | Any exclusion outcome (3, 4, 5, 6, 7). It routes to class 2, or 13 where the destination is a documented sufficiency |
| **Combination input (`Cf`)** | The criterion carries no exit and no redirect of its own; its value is an **input** to another criterion's exit or to a registered composed row | Any outcome on its own. Terminating on a `Cf` is a category error — resolve the row it feeds |

`decision-criteria.md` §2.5 records the concrete damage: six criteria whose answer is a different
in-platform store were filed as exits, so a pack generated from the register would have emitted *"Power
Platform excluded for this responsibility"* for a store change **inside** the platform.

### 3.1 Evidence grade required for a disqualifier

> **Binding rule. A settled hard disqualifier requires decision-grade evidence. `Assumed` evidence alone
> never settles a hard exclusion.**

A **hard** disqualifier settles non-viability and terminates the option. A **provisional** disqualifier is
a cautionary non-viability finding that is carried, with its basis, and never rendered as settled.

| Evidence state of the disqualifying fact | Settles a hard exclusion? | What the model does |
|---|:--:|---|
| **`Confirmed` and current** (`verificado_em` + `validade` not expired) | **YES**, where the canonical rule permits an exit at that state | Render the exit at its class and scope |
| **`Assumed`** — **not** decision-changing | **NO** | **Provisional disqualifier**, carried explicitly with its basis. It does **not** block the decision merely for being `Assumed`, it does **not** become a settled exclusion, and it does **not** produce a settled class 5/6/7/9/14 by itself. Where another **independent `Confirmed` and current** disqualifier already excludes the option, the settled exclusion rests on **that** evidence and the `Assumed` finding is supplementary — cited as corroboration, never as the ground |
| **`Assumed`** — **is** decision-changing (resolving it could restore viability, or change which option is preferred) | **NO** | **Provisional disqualifier + evidence obligation**: (a) expose the assumption and its basis; (b) name the evidence that would settle it and its expected form; (c) `Unknown` row, `swing: decisivo`; (d) **`DECISION BLOCKED`** (class 12) where resolving it could change the recommendation |
| **`Unknown`** | **NO** | Evidence obligation created or retained. Class 12 where decision-changing |
| **`Conflicted`** | **NO** | Evidence obligation naming both readings and what would resolve them. Class 12 where decision-changing (`DC-D-039` is the standing instance) |
| **Materially expired `Confirmed`/`Assumed`** | **NO** | An expired row reads as **weak `Assumed`** and may never be cited as `Confirmed`. Revalidate (`/answer --revalidate`), or treat as the `Assumed` rows above. *Materially* expired means the decay matters here — a `plataforma-tecnica` row past 12 months carrying a service limit is materially expired; an `organizacional` row a week past on a fact nobody disputes is not |

**Symmetry.** The rule applies to every option class, not to PP. An `Assumed` claim that `ALT-005` cannot
meet a requirement is held to exactly the same standard as one about `ALT-004` — this is
`alternatives.md` §2.1's equal evidential burden made operational.

### 3.1.1 Two separate responsibilities

```text
evidence grade      → determines whether an exclusion can be SETTLED
materiality / swing → determines whether unresolved uncertainty BLOCKS the decision
```

They are not interchangeable, and conflating them produces both of the model's failure modes at once —
a settled rejection resting on an inference, and a decision blocked by an assumption nobody needed
resolved.

**Decision-changing controls** whether unresolved `Assumed` evidence must block the decision.
**It does not control whether `Assumed` evidence becomes fact.** No degree of immateriality upgrades an
assumption to `Confirmed`.

Consequently:

- **Not decision-changing** ⇒ carried as a provisional finding, no blocker. The option's assessment states
  the finding, its basis and that it is unverified.
- **Decision-changing** ⇒ evidence obligation, and class 12 where resolving it could change the
  recommendation. Consequence and reversibility set how hard that obligation is pushed — `custo` and
  `swing` are where the judgement is written down, and `/simulate`'s value-of-information section is where
  it is tested against the evidence.

**Outcome classes — explicit.** Classes **5, 6, 7, 9 and 14** are **settled exclusions** and **cannot be
emitted solely from `Assumed` evidence**, decision-changing or not. They require `Confirmed` and current
evidence on the criterion that fires them. A provisional finding may still appear in the option assessment;
where it is decision-changing, the terminal is **class 12** until it is resolved. This is exactly how the
canonical scenarios behave: `T-04`, `T-08`, `T-09` and `T-10` all reach class 12 *first*, and only then
their exclusion class.

**Explicitly excluded from the semantics.** Numeric fit scores · weighted criteria · aggregated verdicts ·
any ordinal ladder (`forte`/`adequada`/…) · any ranking that is not backed by a discriminating comparator
signal. Rationale: `decision-criteria.md` §2.4, four named failure modes.

**Scope pairing (normative).** One outcome per **scope**, not per engagement. An `Xr` exit takes a named
responsibility off the platform and leaves the rest, so an engagement legitimately terminates in more than
one class, each bound to a named scope. `options.md` renders *(scope, class)* pairs and never collapses
them — collapsing is how a bounded `Xr` becomes a whole-solution rejection (`decision-criteria.md` §6.4).

---

## 4. Material decision concern model

**12 concerns.** Each is a coherent decision question with its own failure mode. The set is the compression
of all 116 canonical criteria (§7), and it is the coverage object Q-11 requires.

| # | Concern | The decision question | Failure mode if omitted |
|---|---|---|---|
| **C1** | **Need, value and existing capability** | Should anything be built or changed at all, and does the organisation already own something that answers this? | Building what is already owned; building what a process change would fix; criticality misclassified, so every downstream depth judgement is wrong |
| **C2** | **Functional and process fit** | Can the option carry the required work shape, human waits, exception and failure behaviour? | An automation shape the mechanism cannot express; retry duplicating side effects with no idempotency key; failure behaviour left to whatever the implementation happens to do |
| **C3** | **User and experience fit** | Can it deliver the required interaction, identity class, accessibility, distribution and offline behaviour? | Identity class discovered after the surface is chosen; offline + field-level security promised as a mutual exclusion |
| **C4** | **Data and information fit** | Can it satisfy authority, relationships, integrity, granularity, atomicity, volume, retention and residency? | Residency decided at environment creation and irreversible; contested authority carried into design as agreement |
| **C5** | **Integration and ecosystem fit** | Can it exchange with the required systems, at the required guarantee, throughput, payload and network boundary? | Point-to-point estate; guaranteed delivery assumed where none exists; a private-network requirement discovered at build |
| **C6** | **Security, privacy and control** | Can the mandated controls, key custody, egress control and authorization model be satisfied? | A mandated control that is documented as unavailable; authorization semantics silently changed by a mediation tier |
| **C7** | **Governance, authority and compliance** | Who may build, change and permit; what does the compliance regime bind; is there an owning estate? | Governance maturity produces **zero** direct exits, so an ungoverned estate is invisible to per-criterion reading and only appears in composed rows |
| **C8** | **Lifecycle, ALM and change** | Can it be built, released, isolated, tested, reversed and changed at the required cadence? | Same as C7 — zero direct exits; concurrent makers overwriting each other is a documented outcome, not a risk |
| **C9** | **Scale, performance and resilience** | Can it meet peak, growth, concurrency, availability and recovery expectations, and can that be proven before commitment? | Sizing on the average; *"scale anxiety without a number"*; a commitment that cannot be evidenced |
| **C10** | **Operability, support and ownership** | Can the organisation run, observe, recover, support and own it — with named people who accepted? | Where there is no operator, the pattern is **unavailable, not merely expensive**. A technically feasible option the organisation cannot operate |
| **C11** | **Economics, entitlement and TCO** | Are acquisition, entitlement, growth and operating economics defensible, on the same dimensions for every candidate? | Reducing economics to *"does it need premium licensing?"*; an unfunded mandated control priced as a trade-off rather than infeasibility |
| **C12** | **Strategic fit, reversibility and dependency** | What dependency, lock-in, exit cost, vendor-change exposure and future optionality does it create, over what lifespan? | Reversibility mechanisms must be **enabled before they are needed**; portability discovered as a requirement after commitment |

### 4.1 Why 12, and why not fewer or more

Tested against the survival test (`pp-pack-authoring-map.md` §1.5): *a concern may be compressed away only
when its omission could not materially change viability · option class · architecture · functional fit ·
user fit · integration · data architecture · security posture · governance · lifecycle · scale ·
resilience · operability · cost · strategic fit · reversibility · risk · preference · decision confidence.*

| Merge considered | Rejected because |
|---|---|
| C6 + C7 (security + governance) | Different failure modes and different authorities. C6 produces direct exits (`DC-D-059`, `067`); C7 produces **none** and reaches the decision only through composed rows 2, 9, 11 and 12. Merging hides the second mechanism inside the first |
| C7 + C8 (governance + ALM) | Both produce zero direct exits, which is the argument *for* keeping them visible: composed rows 11 and 12 are *"the only composed rows drawn from Governance and ALM"*, and before they were registered *"a domain that could not reject the platform on any single criterion was contributing nothing to the one test designed to catch precisely that"* |
| C9 + C10 (scale + operability) | Availability of a platform ≠ availability of a business flow ≠ ability to operate either. C9 is a property of the design; C10 is a property of the organisation. Composed row 9 turns on exactly that gap |
| C11 folded into each concern | Cross-domain economics (§14) is a first-class reversal mechanism (scenario 11) and needs one place where the same ten dimensions are priced for every candidate |
| C12 folded into C7 | Reversibility (`DC-D-080`) is decision-blocking and ALM-shaped; lock-in (`DC-D-105`–`107`) is strategic and reaches an `Xp` exit. Different mechanisms, different stages |
| C2 folded into C4/C5 | Work shape decides the mechanism class before volume does; ten criteria (`DC-D-048`…`057`) with six `Xr` exits would become invisible under a data or integration heading |
| C1 split into "need" and "estate" | The two questions are asked together in practice — *is this worth doing, and do we already have it* — and `AA-36` rung 0 puts configure-or-buy **before any app type** |

| Split considered | Rejected because |
|---|---|
| C6 → privacy / security / control | Same authority, same evidence source (the clause), same stage. Three headings, one reasoning |
| C9 → scale / performance / resilience | Sized by one envelope analysis; `DC-D-089` (provability) binds all three to one validation obligation |
| C12 → reversibility / lock-in | `DC-D-098` is a **cost field** on the answer `DC-D-105`/`106` establish — never an independent question (§3.2 cluster rule) |

**Concerns are not stages.** Several concerns are evaluated at more than one stage (C1 at S0 and S1; C10
at S5 and S7; C11 at S5 and S8), and several stages evaluate more than one concern. §5 is the order; §4 is
the coverage.

---

## 5. Ordered decision procedure

**10 stages.** The order is **not commutative** — evaluating direction before disqualification produces
different and wrong answers (matrix §5). S2–S9 are matrix §5 Steps 0–8 + 7a, preserved in order; S0 and S1
are prepended because matrix §5 begins after the option space already exists, which is where the current
tree's vendor bias lives.

| Stage | Name | Job | Concerns | Canonical anchor | Reachable outcomes |
|---|---|---|---|---|---|
| **S0** | **Intervention justification** | Is a technology response warranted at all? Value against full cost of ownership; process maturity; is the requirement a feature list of the outgoing tool? | C1 | `LC-28`, `PS-41`, `PS-44`; `ALT-002`, `ALT-010` | **10** (process redesign), **11** (do nothing / defer) |
| **S1** | **Option-class generation** | Which materially different response classes are on the table? Read the dominant requirements against the trigger→class map. **Mandatory members: `ALT-002` and `ALT-010`.** Candidate generation only — never a verdict | C1, and the dominant requirement of any concern | `alternatives.md` §5.1, §3; `LC-28` (a)–(e) | — (produces the candidate set) |
| **S2** | **Absolutes and hard viability** | The six absolutes, then any other exit-class evidence already in hand, **per candidate**. Classify each finding `Xp`/`Xr`/`Xe`/`Xc`/`Ri`/`Cf`/`—` | C3, C4, C6, C12 | matrix §5 Step 0 — `DC-D-108`, `033`, `059`, `062`, `028`, `057`; §2.5 class→outcome map | **5**, **6**, **9**; `Ri`→2 or 13 |
| **S3** | **Decision-changing uncertainty** | The 28 blocking criteria + the 3 `B*` scopes + any `CONFLICTED` decision-critical value + any provisional disqualifier §3.1 refuses to settle. Name the evidence needed, its expected form, and **the outcome each resolution would produce**; the **actual owner, due date and commitment are resolved in the engagement**, never read from the register | all | matrix §5 Step 1; `decision-criteria.md` §5.2 | **12** |
| **S4** | **Shape and ownership** | Whose problem is this, before what to build: source of record, integration ownership, existing estate, work shape, criticality class | C1, C2, C4, C5 | matrix §5 Step 2 — `DC-D-021`, `036`, `111`, `048`, `001` | narrows the candidate set; sets depth (§6) |
| **S5** | **Material concern evaluation** | **Every serious option × every material concern**, at proportional depth. Absorbs the envelope analysis: limits **exclude designs, never prove performance** | **C1–C12** | matrix §5 Step 3 + the fit domains | **1**, **2**, **3**, **4**, **6**, **13**; raises `Ri`/`Cf` |
| **S6** | **Composed disqualifiers** | Run the 12 registered rows **explicitly**. A set of individually-`CONDITIONAL` verdicts is **not** a pass. Resolve every `Cf` input first. Then test emergent combinations (§11) | cross-concern | matrix §3; `AP-D-059`; matrix §5 Step 4 | per-row: **2**, **5**, **7**, **11**, **12**, **14** |
| **S7** | **Obligation and capability gates** | Operator, support, skills, cross-boundary release owner, operational maturity, accountable ownership. These make options **unavailable**, not worse | C7, C10 | matrix §5 Step 5 — `DC-D-070`, `073`, `083`, `104`, `110`, `006` | **5**; removes candidates |
| **S8** | **Economics** | The same ten cost dimensions for **every surviving candidate**. An unfunded mandated control is infeasibility, not a trade-off — and the class 7 subtype is chosen here (§16.4) | C11 (+ C6, C9, C10 consequences) | matrix §5 Step 6; `licensing-cost.md` §6 | **7** (`7-INFEASIBLE` \| `7-UNATTRACTIVE`), **11** |
| **S9** | **Comparative synthesis, comparator check, validation level** | Produce *(scope, outcome class)* pairs from the closed 14; run the four-part comparator separation before writing any terminal sentence; state and budget the validation level the commitment requires | all | matrix §5 Steps 7, 7a, 8; `decision-criteria.md` §4A.4, §6.2 | any of the 14 |

### 5.1 Stage-local register loading

> **Decision registers are stage-local resources, not permanent Options context.**

`decision-tree.md` is the **always-readable spine** — the procedure, the concerns, the semantics, the depth
ladder. Everything else is consulted **only at the stage that needs it**, and the procedure itself names
which. No preloading, and **no router**: the stage says what it consults, the same way §10 has the reasoner
pull domain knowledge from a concrete question rather than from a routing table.

| Stage | Register it consults | Consulted for |
|---|---|---|
| S1 | `alternatives-register.md` | The trigger→class map; the eleven classes; the forbidden universals |
| S3 | `blocking-set.md` | The 28 + 3 entries and their closure guidance |
| S6 | `composed-disqualifiers.md` | The 12 registered rows and their reachable outcomes |
| S9 | `outcome-classes.md` | The closed 14, the render templates, the comparator separation |
| any | `volatility-register.md` | **Only** where an active decision question depends on a volatile fact or a dated tripwire (§12 rule 4). Never read as a standing checklist |
| S0, S2, S4, S5, S7, S8 | none | These stages run from the spine plus the Shared Understanding; S5 additionally pulls **domain knowledge** at D3 (§10) |

**Two consequences worth stating.** A register may be re-consulted at a later stage where a finding sends
the reasoning back to it — S9 legitimately re-reads `alternatives-register.md` for the candidate list a
class-8 string must name. And a stage that consults nothing is not a stage doing less: S5 is the widest
stage in the procedure and reads no register at all.

**Two standing rules that are not stages.**

- **Uncertainty re-check.** S3 runs early because it is cheap and can terminate the analysis. It is
  **re-run after S8**: stages S5–S8 raise new uncertainty, and an unresolved decision-changing Unknown
  discovered at S8 blocks the decision exactly as one discovered at S3 does.
- **Reachability floor.** If the candidate set at S9 contains only PP forms, the procedure has failed at S1
  and must be re-run. `ALT-002` and `ALT-010` are mandatory members and are never eliminated by a PP
  disqualifier — only by their own evidence.

**Why this order.** S0–S3 are cheap and can end the engagement; running them last wastes it and produces a
recommendation that one unasked question invalidates. S6–S7 exist because per-criterion favourability does
not compose. S8 comes after the gates because an option that is *unavailable* cannot be made available by
being cheap. S9 is last because the model's caveats were surviving every earlier step and being discarded
at the boundary where the outcome is written down.

---

## 6. Broad coverage / selective depth mechanics

**Binding rule.** Every **serious** option is considered against every **material** concern. Depth varies;
coverage does not.

### 6.1 What "serious" means

A candidate is serious unless it is (a) eliminated by an exit at S2, S6 or S7, or (b) not generated at S1
because no requirement triggers it. `ALT-002` and `ALT-010` are always serious. A candidate eliminated at
S2 still appears in the comparison with its disqualifier named — elimination is a finding, not a deletion.

### 6.2 Depth ladder

Four depths. The stage records which depth it used and why; a depth judgement is auditable, an omission is not.

| Depth | What it produces | When |
|---|---|---|
| **D0 — Not material** | One line carrying an **affirmative rationale**: *"not material here — <the engagement evidence that makes it so>"* | The concern **has been considered** and available engagement evidence gives a defensible reason why it does not bear on this option or scope. **Absence of information is never that reason** — see below |
| **D1 — Brief** | A stated verdict with its anchor; no analysis | Material but uncontested, low consequence, reversible, evidence current |
| **D2 — Analysed** | Verdict + the mechanism + the trade-offs + what would change it | Material and consequential, or the evidence is `Assumed`/expired |
| **D3 — Deep** | D2 + domain pull (§10) + the composed rows it feeds + the validation obligation + the uncertainty that would flip it | Decision-changing, or a blocking criterion, or high-consequence and hard to reverse |

**D0 is a finding, not a default.** Three consequences:

1. **An empty Shared Understanding is not evidence of non-materiality.** *"Nothing in the SU mentions
   offline"* does **not** justify D0 on C3's offline dimension. What justifies it is affirmative:
   *"every user works at a fixed workstation on the corporate network (`C-0NN`); no field or disconnected
   population exists in scope."*
2. **Where the concern could plausibly be material and the evidence is missing, it is an evidence gap, not
   D0.** The concern is recorded at D1 with an `Unknown` row carrying `custo` and `swing`. Existing
   materiality semantics decide what happens next — most gaps are `dimensionante` or `cosmético` and are
   simply carried; **do not force every gap to become decision-blocking.** Only a `decisivo` swing, or
   membership of the blocking set, escalates to class 12.
3. **D0 is auditable.** The concern-coverage line (§16.2) shows the rationale, so a reviewer can challenge
   a D0 judgement. An unexamined concern shows as neither D0 nor a gap — which is the defect §6.3 defines.

**Depth drivers**, in the order they escalate: criticality class (`DC-D-001`) · decision-changing
uncertainty (the 28) · irreversibility · architectural consequence · cost consequence · risk · the
criticality-vs-maturity gap (`DC-D-001` vs `DC-D-104`).

Worked contrast, both required by the same model:

- *Low-risk internal departmental workflow, ≤20 users, no regulated data.* C9 resilience at **D1**
  (*"no availability commitment recorded; platform default accepted — `A-0NN`"*). C6 at D1. C4 at D2 because
  the store choice is architectural. C3's offline dimension at **D0 with an affirmative rationale** —
  a fixed-workstation population is recorded, not merely unmentioned. C11 at D3 (entitlement). Note the
  contrast within one concern: C12 reversibility is **not** D0 here — no evidence establishes the expected
  lifespan, so it is a D1 assessment plus an `Unknown` priced `custo: email`, `swing: dimensionante`.
- *Regulated, mission-critical, external-facing workload.* C6, C7, C8, C9, C10 all at **D3**; C11 at D3
  because a mandated control's population drives it; C1 at D2. Zero D0 — at this criticality no concern has
  a defensible affirmative non-materiality rationale.

### 6.3 The emergent-concern obligation (Q-11 R3)

> A material concern raised by the Shared Understanding, the captured evidence, council reasoning or
> candidate-option analysis is evaluated at its proper depth **whether or not** it appears in
> `technology.constraints_to_check`, in the technology signal catalog, or in the 12 concerns.

Three sources of emergence, all real:

1. **Inside a concern.** A concern's boundary is its *question*, not an enumerated checklist. `DC-D-116`
   (agentic interaction) reached the canonical register late and lands in C3 without a new concern.
2. **Between concerns.** Cross-domain interactions (§11) whose significance exists only in the pair.
3. **Outside all twelve.** Possible and expected — the canonical corpus itself records **document
   generation and templating** as *"absent from the entire corpus"*, an Areas 1–12 scoping gap. A concern
   in this class is evaluated on engagement evidence, marked as having **no canonical basis**, and recorded
   as an authoring feedback item. It is never suppressed for lacking an id.

**Silent omission is a defect.** If a concern is material and not evaluated, the model produced a wrong
answer — regardless of whether any declared list mentioned it.

### 6.4 What prevents this from becoming a 12×N matrix

Depth D0 and D1 are one line each. A five-candidate engagement at typical materiality produces roughly
60 assessments of which ~40 are one line — readable, and the reason §16 forbids a giant proof-of-coverage
matrix while requiring that no material concern go unevaluated.

---

## 7. Canonical criteria compression + coverage accounting

**Compression map.**

```text
116 canonical criteria (DC-D-001 … 116, 12 domains)
      ↓  survival test: may this be compressed without changing a material outcome?
12 material decision concerns (C1 … C12)
      ↓  materiality (§6.2)
D0 not material · D1 brief · D2 analysed · D3 deep + domain pull (§10)
```

**Accounting rule.** Every canonical criterion maps to exactly one **primary** concern; several carry a
named secondary consequence in another. *Accounted for ≠ loaded*: the concern carries the durable
**question shape**; the criterion's id, states and boundary figures stay authoring-side and reach the
engagement only through domain pull (§10) or a register (§24). No `DC-D-NNN` id is required at runtime.

| Concern | Primary criteria | n | Secondary consequence carried elsewhere |
|---|---|---:|---|
| C1 Need, value, existing capability | 001, 002, 003, 005, 008, 109, 111 | 7 | 001 → depth driver for all concerns; 111 → C5 |
| C2 Functional / process fit | 048–057 | 10 | 052, 054 → C10 (operational consequence); 057 → C9 |
| C3 User and experience fit | 009–020, 116 | 13 | 010 → C11 (Xe, population economics); 016+026+015+020 → S6 row 10 |
| C4 Data and information fit | 021–034 | 14 | 033 → S2 absolute; 034 → C11 (migration cost); 027 → C6, C10 |
| C5 Integration and ecosystem fit | 035–047 | 13 | 044 → C6, C11; 039, 040 → C9; 036 → S4, C10 |
| C6 Security, privacy and control | 058–068 | 11 | 059, 062 → S2 absolutes; 063, 064 → S6 row 3 (economics); 068 → S6 row 6 |
| C7 Governance, authority, compliance | 069, 070, 071, 072, 074, 075 | 6 | 070 → S7 gate; 071 → C8 (topology, elicited once with 082); 072 → C11 (volatile) |
| C8 Lifecycle, ALM and change | 007, 076–083 | 9 | 080 → C12, S6 row 4; 083 → S7 gate; 078, 081 → S6 row 12 |
| C9 Scale, performance, resilience | 084–091 | 8 | 089 → S9 validation level; 091 → C10; 087 → C11 (growth) |
| C10 Operability, support, ownership | 006, 073, 100–104, 110, 114 | 9 | 073, 104, 110 → S7 gates; 100 → C9; 104 vs 001 → S6 row 9 |
| C11 Economics, entitlement, TCO | 092–099 | 8 | 092, 093 → S6 row 3; 098 → C12 (cost field on 105/106) |
| C12 Strategic fit, reversibility | 004, 105, 106, 107, 108, 112, 113, 115 | 8 | 108 → S2 absolute + the one comparator axis; 113, 115 → `B*` scopes |
| **Total** | | **116** | |

**Verification.** 7+10+13+14+13+11+6+9+8+9+8+8 = **116**. Every id in `DC-D-001…116` appears exactly once
as a primary. No criterion is dropped, and none is excluded as non-decision-material — Block D's own
inclusion test (§2.1) already removed everything that could not change an architecture.

**Cross-domain reassignments away from the canonical domain, and why.**

| Criterion | Canonical domain | Concern | Why |
|---|---|---|---|
| `DC-D-004` lifespan | Business | C12 | A `Cf` input to reversibility and exit-cost reasoning, not to the need question |
| `DC-D-006` accountable ownership | Business | C10 | `Ri` + gate: a named, **accepted** owner is an operability precondition; detection does not produce a working owner |
| `DC-D-007` change frequency | Business | C8 | Feeds composed row 12 (continuous change + concurrent makers) — an ALM mechanism |
| `DC-D-073` support ownership | Governance | C10 | An operating-model gate; the vendor's support does not fill it |
| `DC-D-109`, `DC-D-111` estate | Strategic | C1 | *"Capability already exists in the estate"* is the S0/S1 question, at `AA-36` rung 0 |
| `DC-D-110` skills, `DC-D-114` sourcing | Strategic | C10 | Capability to build **and run**; `DC-D-110` gates hybrid and custom |
| `DC-D-116` agentic interaction | Users (appended id) | C3 | Its domain field says Users; the id sits outside the range for lineage reasons only |

**Near-duplicate clusters — elicited once (§3.2 binding rule), carried into the concerns.**

| Cluster | Concerns spanned | Rule inherited |
|---|---|---|
| `023` volume ÷ `088` depth | C4, C9 | Elicit once; `023` authoritative on volume, `088` on traversal depth. `088` must not restate volume |
| `098` cost ÷ `105` requirement ÷ `106` obligation | C11, C12 | Elicit once; `098` is a **cost field** on the answer, never an independent question |
| `037` per-stream peak ÷ `087` whole-solution peak | C5, C9 | Elicit once, then decompose. Both stay decision-blocking on their own scopes |
| `071` drivers ÷ `082` lifecycle stations | C7, C8 | Elicit once; record **one** topology with drivers attributed |

**Registers and closed sets — accounted for as mechanisms, not criteria.**

| Canonical object | Count | Where it lives |
|---|---|---|
| Exit classes `Xp`/`Xr`/`Xe`/`Xc` + non-exits `Ri`/`Cf`/`—` + class→outcome map | 7 | §3 semantics → `decision-tree.md` |
| Decision-blocking set | 28 `B` + 3 `B*` | S3 → `blocking-set.md` |
| Composed disqualifiers | 12 registered rows | S6 → `composed-disqualifiers.md` |
| Outcome classes (closed) | 14 | S9 → `outcome-classes.md` |
| `ALT` classes + trigger→class map | 11 classes, 30 triggers | S1 → `alternatives-register.md` |
| Comparator signals `G` | 28 criteria, 1 discriminating axis | S9 (7a) → folded into `outcome-classes.md` |
| Volatility: commercial + service-limit | 10 + 20 | §12 → `volatility-register.md` |
| Validation levels V1–V4 | 4 | S9 → `decision-tree.md` |
| Anti-patterns `AP-D-001…068` | 68 (3 `GATE`, 4 `CONSTRAINT`, 61 `ANTI-PATTERN`) | Detection signals via domain pull; the 3 `GATE` and 4 `CONSTRAINT` entries are absorbed into S2/S6/S7 as gates. **Not a runtime register** (§24) |
| Criteria register `DC-D-001…116` | 116 | **Authoring artifact only.** Complexity test A |

---

## 8. Discovery → Options handoff

**Options consumes the Shared Understanding. It does not re-run Discovery and does not declare its own
input signature.** The current tree's 15 `inputs_used` slots are replaced by SU consumption, which is
open-ended by construction and therefore cannot cap what Options may consider.

The Step-2 Discovery cue set (36 `extra_signals`) maps into the concerns as follows. The mapping is a
reading aid for the architect; **an absent cue is not an absent concern**.

| Discovery lens | Cue | → Concern | Feeds stage |
|---|---|---|---|
| business | `business_criticality_class` | C1 | S0, S4; **depth driver everywhere** |
| business | `differentiation_class` | C1, C12 | S0, S1 (`ALT-011`/`ALT-001` triggers) |
| business | `existing_capability_overlap` | C1 | S0, S1 |
| business | `scope_reach` | C7 | S5, S6 row 11 |
| business | `expected_lifespan_and_change_frequency` | C8, C12 | S5, S6 row 12 |
| operations | `work_shape_class` | C2 | S4 |
| operations | `long_running_wait_and_approval_shape` | C2 | S2, S5 |
| operations | `partial_failure_behaviour_today` | C2 | S3 (`DC-D-054` blocking) |
| operations | `stable_business_key_availability` | C2 | S3 (`DC-D-052` blocking) |
| operations | `system_without_programmatic_interface` | C5, C2 | S5 |
| operations | `compute_intensive_step_present` | C2, C9 | S2 absolute (`DC-D-057`) |
| operations | `spreadsheet_and_mailbox_anchors` | C1, C4 | S0, S1 |
| user | `user_population_identity_class` | C3 | S3 (`DC-D-009` blocking), S5 |
| user | `interaction_bespokeness_and_design_obligation` | C3 | S5 |
| user | `offline_operating_requirement` | C3 | S2, S6 row 10 |
| user | `native_distribution_and_push_need` | C3 | S2, S6 row 10 |
| user | `response_and_freshness_expectation` | C3, C9 | S5 |
| data | `relational_depth_and_integrity` | C4 | S5 |
| data | `queried_volume_per_access_path` | C4, C9 | S5 (cluster with depth) |
| data | `access_granularity_requirement` | C4, C6 | S5, S6 row 10 |
| data | `atomicity_span_and_consistency_window` | C4 | S2 absolute (`DC-D-028`), S6 row 1 |
| data | `analytical_versus_operational_need` | C4 | S5 (`Xr` → class 3) |
| data | `attachment_and_binary_volume` | C4 | S5 (`Ri` — never an exclusion) |
| data | `external_exchange_profile` | C5 | S5 |
| governance | `deployment_model_constraint` | C12 | **S2 absolute** (`DC-D-108`) — the one comparator axis |
| governance | `connectivity_and_egress_policy_posture` | C6, C5 | S2, S3 (`DC-D-044` blocking) |
| governance | `vendor_trust_boundary_requirement` | C6 | S2 (`DC-D-062`) |
| governance | `authorization_enforcement_point` | C6 | S6 row 6 (`Xc`) |
| governance | `maker_and_platform_governance_model` | C7 | S7 gate (`DC-D-070`) |
| governance | `release_control_and_reversibility_expectation` | C8, C12 | S3 (`DC-D-080` blocking), S6 row 4 |
| governance | `vendor_change_tolerance` | C12 | S5 (`Xp`) |
| financial | `audience_and_frequency_shape` | C11 | S8 (volatile) |
| financial | `existing_entitlement_baseline` | C11 | S3 (`DC-D-093` blocking), S8 |
| financial | `mandated_control_funding_gap` | C11, C6 | S6 row 3, S8 (→ class 7) |
| financial | `cost_driver_growth_at_horizon` | C11, C9 | S8 |
| financial | `cost_attribution_requirement` | C11 | S8 |

**Coverage of the 12 concerns by Discovery.** C1–C9, C11, C12 are all cued. **C10 (operability) has no
direct Discovery cue** — it is elicited through `Q-GOV-06` (who operates after go-live, and have they
agreed) and probes `P-GOV-07`, `P-FIN-05`, plus the `operational_maturity_class` vocabulary already in
`glossary.md` A6. This is a real thinness: three of the five S7 gates and composed rows 2 and 9 turn on
C10. **Recorded as a Step-3B/S7 authoring item** (§24) — do not fix it by adding a cue in Step 3A.

**Missing evidence.** If a concern is material and the SU carries nothing, Options **exposes the gap**; it
does not fill it. Where the gap is one of the 28 blocking criteria, S3 yields class 12 with the evidence
task in its pack-authored form and the outcome each resolution would produce; the engagement then supplies
the actual owner, date and commitment on its own `Unknown` row (§24). Where it is not blocking, the
architect may proceed on a declared `Assumed` row with its basis, `verificado_em` and `validade` stamped.
An **expired** `Confirmed` reads as weak `Assumed` and may never be cited as `Confirmed`.

---

## 9. Technology lens role

`lens-technology` / `solution-architect` is the **specialist evaluator** inside Options, not the decider.

| It does | It does not |
|---|---|
| Generate technically plausible option classes at S1 from the `ALT` trigger map | Advocate PP, or start from PP and search for reasons |
| Test architectural feasibility per candidate at S2–S5 | Load the domain-knowledge base by default |
| Identify disqualifiers with their **exit class and scope**, and preconditions with owner and funding | Re-open the framed problem, or re-run Discovery |
| Follow material technical concerns **beyond** the declared constraints (§6.3) | Emit a verdict *per declared constraint* and stop |
| Pull domain knowledge for a concrete decision question (§10) | Perform detailed implementation design — that is `/blueprint` and the implementation spec |
| Identify technology-dependent uncertainty, including volatile-fact obligations (§12) | Assert a comparator claim the corpus does not carry |
| Assess consequences across the **full material concern set**, at proportional depth | Choose the final option alone |

**Two runtime-contract changes for Step 3B**, both minimal:

1. Execution step 2 — *"a constraint verdict per constraint (pass / risky / blocker)"* → **"a verdict per
   material concern, at proportional depth; the pack's declared constraints are the floor, never the
   ceiling; classify each disqualifying finding by exit class and scope."** This is the lens half of the
   Q-11 fix; the model half is §4 and §6.3.
2. Execution step 2 — *"Cross the framed problem against the pack's decision tree to identify the candidate
   branches"* → **"…to generate the candidate option classes"**. Branches are architecture shapes reached
   *after* an outcome class, not the option space.

Everything else in both files stays: the phase gate, the five questions, pull-based domain knowledge, the
do-nothing + non-technology floor, hard rules 1–6, and the *"Cues, not coverage"* clause.

**Synthesis remains the chairman's.** The architect returns option assessments; cross-perspective
synthesis, divergence handling and the Conflicted rows that survive the dialectic round are
`chairman-synthesis`'s, unchanged. The six Discovery personas keep contributing needs and constraints at
Options and are the anchors for C1, C7, C10 and C11 — the architect is not the sole voice on economics or
operability.

---

## 10. Domain-knowledge pull boundary

**Rule.** Pull domain knowledge because a **candidate option + a material concern** has produced a concrete
decision question. Never because a concern exists; never to be thorough.

```text
candidate option  +  material concern  →  concrete decision question  →  pull the file that answers it
```

| Trigger | Question | Pull |
|---|---|---|
| Candidate + C4 volume/granularity at D3 | *Does this access path stay inside the documented ceiling for the store we are proposing?* | the store-selection knowledge for that store |
| Candidate + C8 strict release control at D3 | *Which isolation rung does this reach, and what does the rung require?* | ALM/lifecycle knowledge |
| Candidate + C11 economic uncertainty at D3 | *Which meter moves with this audience-and-frequency shape?* | licensing/cost knowledge + the **current** commercial reading (§12) |
| Candidate + C6 mandated control at D3 | *Is the control available at all, and on what population?* | security knowledge + the clause |
| Candidate + C5 guarantee/throughput at D3 | *Which mechanism can carry this guarantee at this peak?* | integration/automation knowledge |

**Boundaries.**

- **No preloading.** `aisa-options` must keep *"never place `decision-tree.md` or `domain-knowledge/`
  contents in the prompt — the architect pulls what it needs."*
- **No retrieval engine, no routing table.** The reasoner determines what is required from the question.
  A routing table would be a second, silent coverage ceiling.
- **Depth gates the pull.** D0/D1 pull nothing. D2 pulls only where a boundary is contested. D3 pulls.
- **Cite what was used.** Branch, file or SU row id — never a filename alone (`lens-technology` hard rule 3).
- **Selection logic never lives in domain knowledge.** Boundaries and mechanisms live there; *which option
  wins* lives in the procedure. Putting selection logic in a reference file is how the current pack
  acquired invented thresholds.

---

## 11. Cross-domain interaction handling

Some concerns matter only in combination. The model handles this with **three mechanisms and no pairwise
matrix** — a 12×12 matrix would be 66 pairs of mostly-empty cells and would still miss triples.

**Mechanism 1 — the registered composed rows (S6).** Twelve rows the corpus states explicitly. Every one is
a cross-domain interaction, and every one is invisible to per-criterion reading. They are run explicitly
because *a set of individually-`CONDITIONAL` verdicts is not a pass*.

| Row | Interaction | Outcome |
|---|---|---|
| 1 | atomicity + multiple transactional owners + no compensation window | 5 |
| 2 | external component required + no named operator/on-call/release owner | 5 — **unavailable, not expensive** |
| 3 | private-network / key-control requirement + unfunded licence population | **7** — security requirement × economics |
| 4 | criticality + no representative test environment + no recovery drill | 12 — validation gap |
| 5 | high-frequency custom-connector workload + unmeasured sizing across a live 20× conflict | 12 |
| 6 | per-user backend authorization + facade calling as a shared identity | 2 with the named condition; 12 if propagation is `UNKNOWN`. **Never 5/6/7** |
| 7 | hybrid required + no pro-code or enterprise-platform capability | 5 |
| 8 | replication + no reconciliation owner + a restore requirement | 5 |
| 9 | criticality ≥2 classes above demonstrated maturity, unfunded | 11 or 12 — **platform-independent**, never a PP exclusion |
| 10 | offline + field-level security, **or** offline + ungoverned data, **or** mobile-first + hardware + branded push | 5 |
| 11 | citizen-built artefacts outside a solution + criticality risen + maker gone | **14 — migration, not remediation** |
| 12 | continuous change + ≥2 concurrent makers + no pro-code capacity for the isolating rung | 5 |

**Mechanism 2 — secondary consequence carriage (§7).** Every concern's row names where its consequences
land in other concerns. The six interactions the brief names are all carried:

| Interaction | Carried by |
|---|---|
| security requirement → licensing consequence | C6 → C11; row 3 |
| data architecture → performance + cost | C4 → C9, C11; `DC-D-023`/`088` cluster |
| governance control → ALM + operational | C7 → C8, C10; rows 11, 12 |
| user/offline requirement → architecture + support | C3 → C4, C6, C10; row 10 |
| integration limitation → workaround + resilience | C5 → C2, C9, C10; `Xr` → class 3/4 |
| scale requirement → architecture + economics | C9 → C4, C11; `DC-D-087` → `DC-D-095` |

**Mechanism 3 — emergent combination test (S6, second half).** After the 12 registered rows, the architect
asks one question: *do any two or more concerns, each individually acceptable, produce an unacceptable
combination here?* An emergent combination is recorded as a `Risky` row with both anchors named and, where
it is decisive, as a decision blocker. It is **not** treated as a registered disqualifier — the corpus
registers twelve, and adding rows to make flags resolve would be invention.

---

## 12. Volatile-fact handling

**The distinction the model runs on:**

```text
stable decision principle          →  decision logic  (decision-tree.md)
volatile platform fact             →  evidence        (domain knowledge + the engagement's own row)
```

**Rule 1 — encode the boundary shape, never the number.** *"Is the required freshness below the documented
external-site floor?"* is decision logic. *"Is it below 15 minutes?"* is a 2026 service limit disguised as a
timeless rule. This deletes every threshold in the current tree (§2.1).

**Rule 2 — read the figure at the decision date, record it with its date on the engagement's row.** Never
bake it into the pack. Kernel support already exists: `verificado_em` + `validade`, with
`plataforma-tecnica` = 12 months and `financeiro` = 6 months as the relevant decay classes.

**Rule 3 — no published figure is a state name.** Verified across all 116 criteria. Revalidating a limit
changes one sentence, not a taxonomy.

**Rule 4 — verification obligation.** Where a volatile fact is **decision-critical** and sufficiently
current evidence is unavailable, the model creates a **verification obligation**: an `Unknown` row
(`custo: documento|spike`, `swing: decisivo`) plus a named owner and date, and the affected conclusion is
**not treated as settled**. Where the fact is in the blocking set, this is outcome class 12.

**Two volatility classes, both carried.**

| Class | Members | Re-verify |
|---|---|---|
| Commercial / licensing | `DC-D-039`, `051`, `072`, `086`, `093`, `094`, `095`, `096`, `113`, `115` (10) | Options, implementation, renewal |
| Service limit / quota / feature-state | `DC-D-018`, `023`, `025`, `026`, `027`, `031`, `032`, `039`, `040`, `043`, `044`, `048`, `049`, `051`, `055`, `056`, `100`, `101`, `103`, `116` (20) | Design time, per the register's per-row trigger |

**The live conflict.** `DC-D-039` is `CONFLICTED` by **20×** between two currently-maintained pages, and is
in the blocking set. Any option whose sizing or economics rests on a high-frequency custom connector is
**decision-blocked until measured** — and this cuts across `ALT-004`, `ALT-006` and `ALT-009` symmetrically,
so it is not a PP-specific penalty.

**Dated tripwires** (from the canonical registers) belong in `volatility-register.md` and feed `/decide`'s
revision conditions and `/revisit`. They are the mechanism by which a decision made today knows when to
re-examine itself.

---

## 13. Economics

**Rejected framing:** *does it require premium licensing?* That is one line of one dimension, and it is the
question the current R4 asks.

**Adopted framing:** for **every surviving candidate**, price the **same ten dimensions** for the **same
workload and operating model**. Comparative economic defensibility — not estimation.

| # | Dimension | Required input |
|---|---|---|
| 1 | Audience | named users, active users, external/anonymous population, user×capability pairs |
| 2 | Machine workload | calls / messages / compute time / transactions, and peak shape |
| 3 | Data | volume, growth, audit, replicas, retention |
| 4 | Security prerequisites | the required controls **and the population they must cover** |
| 5 | Environment / lifecycle | non-production stations, managed fidelity, pipelines |
| 6 | External estate | gateway, broker, workers, gateway hosts, network |
| 7 | Observability / support | telemetry ingestion and retention, alerting, support plan, on-call |
| 8 | Build / change effort | initial build, migration, test automation, release frequency, deprecations |
| 9 | Existing sunk capability | licences and platform teams already owned — avoid double-paying for a second platform |
| 10 | Exit / option value | migration and rewrite cost, lock-in constraints |

**Six rules.**

1. **Cost of inaction is a priced option.** `ALT-010` and `ALT-002` are priced on the same dimensions
   (`Q-FIN-01`, `Q-FIN-02` already elicit it). *Not-doing-it and doing-it-manually are legitimate economic
   options and frequently the honest answer.*
2. **An unfunded mandated control is infeasibility, not a trade-off** → class 7 subtype `7-INFEASIBLE`,
   distinct from `7-UNATTRACTIVE`, which is a proportionality judgement (§16.4). The subtype is chosen from
   the trigger and is always rendered explicitly.
3. **Growth at horizon is priced, not the launch state.** The dimension that moves is `DC-D-087`/`095`.
4. **Cost attribution** (`DC-D-099`) is a design constraint where chargeback is mandated, not a reporting
   detail.
5. **The users-to-work ratio is a hypothesis to test, never a verdict.** Many people doing a little each
   tends toward people-based mechanisms; few people driving much machine work tends toward
   consumption meters. It must be tested on all ten dimensions with current pricing and the customer's own
   agreement.
6. **Comparative TCO is the corpus's largest gap.** No like-for-like comparator pricing exists. The model
   **asks for the numbers; it does not supply them.** *"Custom development is more expensive"* and
   *"low-code is faster"* are both forbidden output.

**Where economics enters.** Primarily S8, after the gates — an unavailable option cannot be made available
by being cheap. It also enters S2 (`Xe` absolutes: `DC-D-008` value below cost of ownership) and S6 row 3
(security × funding). Economics can **reverse** a technical preference (scenario 11); it cannot resurrect a
disqualified option.

---

## 14. Operability

**First-class, evaluated at S5 (C10) and gated at S7.** A technically feasible option can be operationally
inferior, and where no operator can exist the pattern is **unavailable, not merely expensive**.

| Sub-concern | Criterion | Standing |
|---|---|---|
| Accountable business ownership — named **and accepted** | `DC-D-006` | Blocking; gates replication, hybrid and bidirectional patterns outright |
| Support and operational ownership — the named first line | `DC-D-073` | Blocking; the vendor's support does not fill it |
| Operational maturity class — how the organisation *actually* operates comparable things | `DC-D-104` | Blocking; a two-class gap means the commitment cannot be delivered |
| Monitoring and observability depth | `DC-D-101` | `Xr`; funded capability, with a retention window that is a volatile figure |
| Incident response, support hours and tier | `DC-D-102` | Must be built **and staffed** for code-first classes |
| Recovery point and recovery time | `DC-D-100` | Blocking; *a backup exists* ≠ *recovery is possible* |
| Diagnostic and audit evidence retention | `DC-D-103` | `Xr`; volatile window |
| Cross-boundary deployment coordination | `DC-D-083` | Gate; a **second coordinated supply chain** |
| Team skills and pro-code capacity — **in-house and available**, not planned | `DC-D-110` | Blocking; gates hybrid and custom |
| Sourcing and delivery model | `DC-D-114` | What is inside the price and what is not |
| Change burden | `DC-D-007`, `112` | Who tracks the vendor change stream today |

**Symmetry.** These gates apply to **every** candidate, not to PP. `ALT-005`, `ALT-006` and `ALT-009` are
the classes most often made *unavailable* by them — the corpus is explicit that monitoring, alerting,
incident response, backup, recovery, drills and retirement must all be built and staffed there, and that
approval routing with delegation and escalation has **no equivalent** in the code-first alternatives it
examined. `ALT-011`, `ALT-001` and `ALT-007` gain a `CANDIDATE` signal on the same criteria because an
operator already exists and is funded. This is one of the few places the corpus carries genuine
alternative-side evidence, and the model uses it in both directions.

---

## 15. Strategic fit / reversibility

**Evaluated at S5 (C12), with `DC-D-108` promoted to an S2 absolute.**

| Sub-concern | Criterion | Standing |
|---|---|---|
| Deployment-model constraint — where the runtime must **execute** | `DC-D-108` | S2 absolute; blocking; `Xp`; **the corpus's only evidenced comparative axis** → outcome class 9 |
| Vendor lock-in tolerance and portability | `DC-D-105` | `Xp` at `FULL PORTABILITY REQUIRED` |
| Exit strategy and switching cost — is a **tested** exit required? | `DC-D-106` | `Xp`; a tested exit is not evidenced as achievable on **any** platform in this corpus |
| Migration and exit cost | `DC-D-098` | A **cost field** on `105`/`106`, never an independent question |
| Tolerance to vendor-driven change cadence | `DC-D-107` | `Xp` where behaviour must be frozen between releases |
| Reversibility requirement | `DC-D-080` | Blocking; `Xc` (row 4). The mechanism must be **enabled before it is needed** — there is no rollback |
| Platform-change tracking capacity and ownership | `DC-D-112` | `Cf` — an input, never a terminal |
| Expected solution lifespan | `DC-D-004` | `Cf` — sets the horizon over which the other seven are weighed |
| Multi-tenancy / resale | `DC-D-113` | `B*` — blocks the **commercial model** only |
| Roadmap and preview dependency | `DC-D-115` | `B*` — blocks any commitment resting on a preview or unshipped capability |

**Rules.**

- **Vendor dependency is not automatically a penalty.** Its materiality depends on the engagement:
  lifespan, differentiation, change-control regime and whether portability is a stated obligation. A
  six-month departmental tool and a fifteen-year regulated ledger weigh `DC-D-105` differently, and the
  model must let them.
- **Symmetry holds.** *"A platform that runs on the customer's own cluster is not thereby portable off that
  vendor. Do not infer."* `ALT-008` is `UNKNOWN` on portability; `ALT-005` is the only class the corpus can
  name for `FULL PORTABILITY REQUIRED`, and even there a *tested* exit is unevidenced everywhere.
- **`DC-D-108` is the model's one licensed preference.** At `customer-hosted / private-cloud / air-gapped`,
  the platform documents SaaS-only and at least one comparator documents generally-available air-gapped
  deployment — while a second comparator's equivalent is **Early Access, not GA**, and adopting it on a
  critical path is itself an anti-pattern. The model states both halves.

---

## 16. Comparison and recommendation semantics

### 16.1 Per-option comparison structure

Replaces `chairman-synthesis`'s Pros / Cons / Constraints-checked / Reversibility / Effort block, which
cannot express viability, disqualifiers, preconditions or decision-changing uncertainty.

```markdown
### O-00N — <option name>   ·   class: ALT-0NN   ·   scope: <whole solution | named responsibility>
- **Viability**: viable | viable-with-preconditions | **disqualified (settled)** | **disqualified (provisional — assumption <id>)** | not assessable (evidence)
- **Outcome class**: <the class **name** from the closed 14, in its own render template; class 7 carries its explicit subtype sentence — §16.4>
- **Material strengths**: <evidence-anchored; no comparative adjectives>
- **Disqualifiers**: <what it fails + at what scope, in plain language + the SU anchor + **evidence grade** per §3.1> | (none)
- **Preconditions**: <condition — owner — funded? — by when> | (none)
- **Material trade-offs**: <consciously acceptable disadvantages>
- **Material risks**: <impact + proposed mitigation → SU Risky rows>
- **Economic implications**: <the dimensions of §13 that move, and in which direction>
- **Decision-changing uncertainties**: <SU id — what it would change — cost to close>
- **Validation obligation**: V1 limits | V2 bounded pilot | V3 pro-code harness | V4 managed-test fidelity
- **Concern notes** *(only where non-obvious)*: <C-n: the assessment that decided something>
```

**Rules.** `(none)` is written explicitly — an empty field is indistinguishable from an unevaluated one.
Depth D0/D1 assessments do **not** get their own line; they are visible in the round's concern-coverage
line (below). No numeric score appears anywhere. **Internal framework vocabulary is not rendered** (§17.1):
the blocks carry plain language, and exit codes, class numbers and depth codes stay in the model.
Owners and dates in the preconditions and uncertainty lines are **engagement-resolved**, never copied from
a pack register (§24, artifact 3).

### 16.2 Round-level structure

```markdown
## Summary
<what the candidate set spans, the dominant trade-offs, and the outcome-class pairs reached>

## Concern coverage — round O-NN
<one line per concern: depth used per option, or "not material — <why>">

## Comparison
<the per-option blocks>

## What the evidence supports
<preferred | conditionally preferred | multiple defensible | decision blocked | no intervention justified>
<the decisive evidence, the decisive concerns, and why each serious alternative lost>

## Comparator status
<per non-PP candidate: the §4A.2 signal, or COMPARATOR EVIDENCE ABSENT>
```

The concern-coverage line is what makes broad coverage auditable **without** a giant matrix: twelve lines,
each naming a depth, is enough to see that nothing was skipped.

### 16.3 Recommendation semantics — bound to the closed 14

| Recommendation | Meaning | Outcome classes |
|---|---|---|
| **Preferred** | Evidence supports one option over the viable alternatives | 1, 2 (PP side); 9 or 13(a) where the comparator/sufficiency evidence exists |
| **Conditionally preferred** | Strongest **provided** explicit preconditions hold — named, owned, funded, dated | 2 with its conditions; 3 / 4 with their gates satisfied |
| **Multiple defensible options** | Evidence does not justify pretending one is uniquely superior | 8 with ≥2 candidates; 13(b) |
| **Decision blocked** | Decision-changing uncertainty remains | 12 |
| **No technology intervention justified** | The problem does not warrant new software | 10, 11 |
| **Excluded, at a named scope** | PP is out for the whole scope, a responsibility, or on economics | 5, 6, 7 (`7-INFEASIBLE` \| `7-UNATTRACTIVE` — §16.4) — each followed by 8 |
| **Migration, not remediation** | The artefact cannot be brought to the required class in place | 14 → 8 |

### 16.4 Class 7 — reason discriminator

Class 7 is **one** canonical class covering two materially different findings, and the canonical label
(*"economically unattractive or infeasible"*) is a disjunction a sponsor cannot act on. **The closed 14 is
preserved — no class 15 is created.** Class 7 carries a mandatory `reason` subtype instead.

| Subtype | Meaning | Trigger | Render |
|---|---|---|---|
| `7-INFEASIBLE` | **ECONOMICALLY INFEASIBLE.** A mandatory requirement or control cannot be funded or economically satisfied. Not a judgement — a funding fact | An unfunded **mandated** control, entitlement or operating tier (`DC-D-092` envelope vs `DC-D-093` fit; composed row 3) | *"Power Platform is **economically infeasible** for this scope: `<the mandated control/entitlement>` is unfunded. Candidates: ALT-NNN… Comparative fit `UNEVALUATED`."* |
| `7-UNATTRACTIVE` | **ECONOMICALLY UNATTRACTIVE.** The option is feasible; its economics are disproportionate to the stated value or constraints. A proportionality judgement, and reversible if the value case changes | `DC-D-008` value below full cost of ownership; `DC-D-010`/`094` audience-and-frequency shape; `DC-D-097` support tier — with funding available | *"Power Platform is **economically unattractive** for this demand shape: `<the dimensions that move and by what mechanism>`. Candidates: ALT-NNN… Comparative fit `UNEVALUATED`."* |

**Rules.**

- **The disjunction is never rendered where the evidence supports one condition.** Writing *"economically
  unattractive or infeasible"* when the finding is an unfunded mandated control hides the only fact the
  sponsor can act on — funding it restores viability; a proportionality judgement does not.
- **The subtype is chosen from the trigger, not from tone.** Unfunded **mandated** requirement ⇒
  `7-INFEASIBLE`, always. Everything else ⇒ `7-UNATTRACTIVE`.
- **Both subtypes carry §3.1.** An unfunded mandate asserted from an `Assumed` budget row is a
  **provisional** finding, never a settled class 7 — carried with its basis where it is not
  decision-changing, and escalated to **class 12** naming the budget confirmation where it is.
- **Neither subtype may imply another class is cheaper.** The canonical prohibition is unchanged: no
  comparative TCO exists.
- `7-INFEASIBLE` is the mapping composed row 3 already names (*"infeasible where a mandated control is
  unfunded"*), so the subtype makes an existing distinction explicit rather than adding one.

**Three prohibitions carried verbatim from the canonical governing rule.**

1. **No outcome may contain "preferred", "better", "cheaper" or "faster" about a class the corpus has not
   evaluated.** The permitted form is *excluded → candidates → evidence obligation*.
2. **Every non-PP terminal outcome carries `COMPARATOR EVIDENCE ABSENT`** unless §4A.2 says otherwise. The
   marker is part of the outcome, not a footnote.
3. **Class 13's two forms never merge.** Form (a) — `ALT-003` on the four documented shapes — carries the
   seeded-entitlement clause scoped to `DC-D-093` and stands alone. Form (b) — any other class — carries
   `COMPARATOR EVIDENCE ABSENT`, no comparative word, and is followed by class 8. Both forms must state
   that **PP is not excluded** and both must carry a **graduation trigger**, because the documented growth
   path out of the collaboration surface is a **one-way upgrade** converting every user to premium.

**Closure is testable.** Any outcome label not in the closed 14 is a defect in the emitter, not a new class.
Two labels were withdrawn on exactly this test during canonicalisation.

---

## 17. Options vocabulary proposal

**Method.** A term is kept only where the absence of a shared meaning could materially damage decision
reasoning. Terms already carried by `glossary.md` Part A (Discovery vocabulary, 50 rows) are **not**
restated — that file already defines work shape, failure semantics, source of record, access granularity,
atomicity span, identity class, deployment-model constraint, administrator exclusion, authorization
enforcement point, criticality class, operational maturity class, reversibility requirement, proof
requirement, precondition, entitlement exposure and audience-and-frequency shape. Restating them would
create the two-vocabularies defect the map's N-07 exists to prevent.

**Two populations, not one.** The 14 terms split by *who needs the shared meaning*:

- **INTERNAL DECISION SEMANTIC** — needed by the runtime to execute the procedure correctly, and of no
  value as engagement vocabulary. Home: `decision-tree.md` and the register that owns the mechanism.
  **These do not become glossary terms**, and they do not appear in `options.md` prose.
- **SHARED OPTIONS VOCABULARY** — a term whose shared meaning materially helps an architect, sponsor or
  reviewer understand the decision. Only these are Options-gated glossary content.

> **Strong internal semantics do not require exposing framework vocabulary to the user.**

### 17.1 Internal decision semantics — 8 terms, not glossary

| Term | Home | Plain-language rendering used in output |
|---|---|---|
| Exit classes `Xp` / `Xr` / `Xe` / `Xc` | `decision-tree.md` §semantics | *"excluded for the whole scope"* · *"excluded for `<the named responsibility>`"* · *"economically infeasible/unattractive"* · *"excluded only in combination with `<the other conditions>`"* |
| `Ri` in-platform redirect | `decision-tree.md` §semantics | *"this does not exclude the platform; it changes which `<store/pattern/surface>` is used, and the answer stays in-platform"* |
| `Cf` combination input | `decision-tree.md` §semantics + `composed-disqualifiers.md` | *"on its own this decides nothing; it is an input to `<the named finding>`"* |
| Depth `D0`–`D3` | `decision-tree.md` §depth | The coverage line states the rationale, not the code: *"not material — `<why>`"* / *"assessed"* / *"assessed in depth"* |
| Scope-pair mechanics | `decision-tree.md` §semantics | Plain language is sufficient and clearer: *"for the application: … ; for the reporting responsibility: …"* |
| Outcome-class **numbers** (1–14) | `outcome-classes.md` | The class's own **name** is the render; the number is bookkeeping. `options.md` never prints *"class 6"* |
| Class 7 subtype codes `7-INFEASIBLE` / `7-UNATTRACTIVE` | `outcome-classes.md` | The two explicit sentences of §16.4 — the discriminator must be **visible in the output**, the code must not |
| `DC-D-NNN`, `ALT-NNN`, `AP-D-NNN`, `T-NN` ids | authoring / registers | Never rendered. Anchors in `options.md` are SU row ids and named files |

### 17.2 Shared Options vocabulary — 6 terms

| Term | Purpose | PP-specific? | Why the shared meaning is needed during Options |
|---|---|---|---|
| **Option class** | The kind of response an option is — process change, extend what exists, buy, build, platform, hybrid, do nothing | No | Without it the option space silently collapses to platform architectures, which is the current defect. A sponsor comparing *"SharePoint-first vs Dataverse-first"* is being shown one class presented as the whole choice |
| **Disqualifier** *(and the hard ÷ provisional distinction)* | A requirement an option cannot satisfy, at a named scope — settled, or conditional on an assumption (§3.1) | No | The single most important thing a reviewer must be able to challenge: *what exactly ruled this out, and how sure are we?* |
| **Precondition** | Something that must become true — named, owned, funded, dated — before an option is viable | No | Already in the Discovery vocabulary (`glossary.md` A5) as *"a deliverable with an owner and a cost, not a footnote"*. Options **reuses the Discovery definition**; it does not restate it |
| **Comparator evidence absent** | We can say this option is excluded; we cannot say the replacement is better, because no comparison exists | No | It is part of the outcome sentence, not a caveat. Without shared meaning a sponsor reads *"excluded → candidates"* as *"candidates are better"* — the exact error the canonical repair exists to prevent |
| **Validation level** (limits · bounded pilot · pro-code harness · production-like proof) | What evidence a commitment requires before it can be made — and what it costs | Semi | S9 must **budget** it. Already in the Discovery vocabulary as *"proof requirement"* — Options uses the same term, and Step 3B should keep one word, not two |
| **Graduation trigger** | The named condition under which a *"the lighter option is sufficient"* answer must be revisited | Yes | The documented growth path out of the collaboration surface is a **one-way upgrade** converting every user to premium. Without the trigger, that answer is a trap |

**Net: 6 glossary terms, not 14** — and two of the six (**precondition**, **validation level** / *proof
requirement*) already exist in `glossary.md` Part A. Step 3B's actual vocabulary authoring is therefore
**4 new terms** plus one alignment decision (*proof requirement* vs *validation level* — pick one word).

**Rejected as vocabulary.** *Branch* (an architecture shape, not an option class — keep the word, demote
its role) · *material decision concern* (an internal coverage object; the output says *"we looked at
security, at cost, at who runs it"*) · *score / fit rating / weighting* (no scoring model) · *pros / cons*
(replaced by the strengths / trade-offs / disqualifiers distinction, which carries decision meaning) ·
*recommendation strength* (replaced by the five recommendation semantics of §16.3) · *verification
obligation* (internal; the output says *"this figure must be re-read before we commit — owner, by when"*).

**Placement.** The 6 go to the Options-gated vocabulary (`options-glossary.md` in the map's layout, or an
Options section of `glossary.md` — Step 3B's call). None may leak into the Discovery vocabulary: four of
them are outcome semantics, which are Options artefacts by rule N-09. The 8 internal semantics stay in
`decision-tree.md` and the registers and are **never** Options-gated glossary content.

---

## 18. Technology-question disposition

**Finding: after Phase G there are zero Technology-lens questions in `question-bank.md`.** The bank holds
35 core + 34 probes across the six Discovery lenses only; there is no `Q-TEC-*` or `P-TEC-*` namespace, and
no lens loads the bank (`aisa-status` step 6d is its one consumer). **Nothing to keep, rewrite, merge,
relocate or remove in a Technology section, because none exists.** This is the correct state and Step 3B
must not create one — a Technology questionnaire would reintroduce the coverage ceiling on the elicitation
side.

**What does exist** is the bank's closing *Reachable outcomes* block, which names Discovery questions whose
answers are decisive in Options. Disposition:

| Element | Verdict | Reason |
|---|---|---|
| *Reachable outcomes* block (5 outcomes, question anchors) | **KEEP + REWRITE** | The neutrality guarantee on the elicitation side. Its five outcomes must be re-expressed against the closed 14 so Discovery and Options share one terminal vocabulary: *it fits* → 1 · *fits with conditions* → 2 · *another technology* → 5/6/9 + 8 · *process change* → 10 · *do nothing/defer* → 11 · **plus the two it is missing**: 12 (decision blocked) and 13 (alternative sufficient, PP not excluded) |
| `Q-GOV-02` (where must this run) | **KEEP** | Elicits `DC-D-108` — an S2 absolute and the one comparator axis |
| `Q-GOV-04` (administrator exclusion) | **KEEP** | `DC-D-062`, S2 absolute |
| `Q-GOV-05` (permissibility posture, exception process, lead time) | **KEEP** | `DC-D-072`, volatile, and the lead time is a precondition cost |
| `Q-GOV-06` (who operates after go-live, and have they agreed) | **KEEP** | One of only three C10 elicitations; blocking (`DC-D-073`) |
| `Q-GOV-07` (change authority + expected behaviour on a bad change) | **KEEP** | `DC-D-080`, blocking |
| `P-GOV-13` (portability layers, target, costed?) | **KEEP** | `DC-D-105`/`106`/`098` cluster, elicited once |
| `P-GOV-03`, `P-GOV-06` (network boundary, egress) | **KEEP** | `DC-D-044` blocking; `DC-D-067` `Xp` |
| `P-GOV-10` (behaviour frozen between releases) | **KEEP** | `DC-D-107` `Xp` |
| `P-DAT-02` (atomicity across systems) | **KEEP** | `DC-D-028`, S2 absolute, composed row 1 |
| `P-OPS-03` (real compute in a step) | **KEEP** | `DC-D-057`, S2 absolute |
| `Q-DAT-08` + `P-GOV-07` (existing capability owns it) | **KEEP** | S0/S1 |
| `Q-FIN-01`…`Q-FIN-06`, `P-FIN-01`, `P-FIN-05`, `P-FIN-07` | **KEEP** | Nine of the ten cost dimensions are reachable from them |
| `Q-BUS-03`, `P-BUS-01`, `P-BUS-02` | **KEEP** | S0 intervention justification |
| A Technology question set | **DO NOT CREATE** | Questions arise from **candidate-option uncertainty**, formulated at the moment the uncertainty is material. The model's question generator is S3 (the blocking set, each entry carrying its closing task, owner and duration) plus §12 rule 4 |

**One Options-side artifact is justified** — the map's `options-checks.md`, scoped tightly as a
**verification-obligation list**, not a questionnaire: the 10 commercial + 20 service-limit volatile facts
with their per-row re-verify trigger, and the 28 + 3 blocking entries with their closing task, owner and
the outcome each resolution would produce. Step 3B decides whether this is one file or two
(`blocking-set.md` + `volatility-register.md` already cover it — see §24).

**Survival test applied.** Every question kept above has an answer that could change viability, option
class, architecture, control posture, lifecycle, scale, operability, economics, risk, preference or decision
confidence. None was kept for symmetry.

---

## 19. `technology.constraints_to_check` disposition

**Redefinition first.** The key becomes a **standing-attention floor**: concerns whose silent omission is a
known failure mode across a meaningful range of PP Options engagements, and which are therefore examined in
every engagement regardless of what the SU surfaced. It is **never the concern set** (§4) and never the
coverage object (§6.3). `pack.yaml`'s own comment must say so.

**Current five.**

| Entry | Verdict | Reason |
|---|---|---|
| `premium_licensing` | **MERGE** → `entitlement_fit` | Too narrow: the canonical question is whether the required **capability set** falls outside what the organisation already holds, for a subset or for everyone (`DC-D-093`, blocking, volatile). "Premium yes/no" is one answer to it |
| `dataflow_capacity` | **MERGE** → `throughput_and_capacity_envelope` | Product-specific and partial; the decision-bearing envelope is per-mechanism ceiling + sustained end-to-end throughput + queried volume per access path (`DC-D-039`, `040`, `023`) |
| `ALM_environments` | **MERGE** → `environment_and_release_topology` | Environment **count** is one driver; the canonical pair is drivers (`DC-D-071`) + lifecycle stations (`DC-D-082`), elicited once as **one** topology |
| `dataverse_storage_quota` | **MOVE TO DOMAIN PULL** | A store-specific quota — a volatile figure, pulled at D3 when a candidate proposes that store. Not a standing concern |
| `DLP_policy_compatibility` | **MERGE** → `service_permissibility_and_egress` | Product-named; the canonical concern is the organisation's permissibility posture, its exception process and lead time, plus egress control (`DC-D-072`, `067`, `044`) |

**Proposed floor — 10 entries**, each technology-neutral, each traced, each justified by a standing failure
mode rather than by research support alone.

| # | Entry | Traces | Why it is a standing floor |
|---|---|---|---|
| 1 | `deployment_model_and_residency` | `DC-D-108`, `033` | Both irreversible after environment creation; `108` can eliminate the platform entirely and is the one comparator axis |
| 2 | `regulatory_and_control_mandates` | `DC-D-059`, `062`, `063`, `064` | Can mandate something documented as unavailable; feeds composed row 3 |
| 3 | `service_permissibility_and_egress` | `DC-D-072`, `067`, `044` | Volatile by nature (a policy check is valid on its date only); `044`'s preconditions are irreversible and licence-bearing |
| 4 | `entitlement_fit` | `DC-D-093`, `092` | Blocking, volatile; one connector decision can move the whole population from seeded to paid |
| 5 | `throughput_and_capacity_envelope` | `DC-D-039`, `040`, `023`, `095` | Contains the live 20× `CONFLICTED` figure; the clearest platform-exit verdict in the corpus |
| 6 | `environment_and_release_topology` | `DC-D-071`, `082`, `079` | Real recurring cost and a validation prerequisite; feeds composed row 4 |
| 7 | `reversibility_mechanism` | `DC-D-080` | Blocking; **must be enabled before it is needed** — there is no rollback |
| 8 | `operator_and_support_availability` | `DC-D-070`, `073`, `110`, `104` | Four blocking criteria; makes patterns **unavailable**; C10's Discovery cover is thin (§8) |
| 9 | `observability_and_evidence_retention` | `DC-D-101`, `103` | Funded capability with volatile retention windows; silently omitted today |
| 10 | `authorization_enforcement_point` | `DC-D-068`, `026` | Registered composed row 6; changes the semantics of every exchange, and is invisible per-criterion |

**Why 10 and not 5, and not 30.** Each entry above is a Step-0 absolute, a blocking criterion, or a
registered composed-row input — the three categories where silent omission produces a wrong decision rather
than a shallow one. Nothing else qualifies for standing attention: everything else is reached by the
concern model when the engagement makes it material. **The list is not the fix for Q-11** (§2.3 R1/R3); it
is a floor that happens to be better derived than the one it replaces.

**No `pack.yaml` edit in this step.** Step 3B applies it, together with the comment declaring the list
non-limiting.

---

## 20. Regression scenarios

Traced against the proposed model. Canonical scenario ids (`T-01`…`T-18`) are named where Block D already
carries an equivalent; the full `T-01…T-18` replay is gate **G5** at stage S6 of the authoring sequence,
not this step.

| # | Scenario | Trace | Terminal | Passes |
|---:|---|---|---|:--:|
| 1 | **No intervention** (no canonical `T` — class 10 has no dedicated scenario; recorded for G5) | S0: value below full cost of ownership (`DC-D-008` `Xe`), process immature/self-inflicted (`DC-D-005`) → `ALT-002` triggered at S1; no further stage needed | **10** — process redesign / no new application. *Not a technology decision, so no comparator claim arises* | ✅ |
| 2 | **Existing capability sufficient** (`T-01` — class 1 or 13/`ALT-003`; `T-12` — class 6 → 8/`ALT-007`) | S1: *capability already exists in the estate* → `ALT-001`/`003`/`007`/`011`. S2–S7: no exit fires (`T-01`), or an `Xr` on the integration responsibility fires (`T-12`) | **13** — form (a) if `ALT-003` on one of the four documented shapes, with the graduation trigger; form (b) + class 8 otherwise. **PP explicitly not excluded** in class 13. `T-12` reaches **6 → 8** with `INCUMBENT FIT UNEVALUATED` | ✅ |
| 3 | **Straightforward PP fit** (`T-02` — class 2; `T-17` — class 2; `T-01` — class 1) | S2 clear; S3 closed; S5 caution signals only; S6 no row fires; S7 gates satisfied; S8 entitlement funded | **1** where nothing is engaged, **2** where mitigations are funded and owned. Phrased as *"no documented constraint violated"*, never as endorsement | ✅ |
| 4 | **PP conditionally viable** (`T-05` — class 3, conditional on the operator gate; `T-08`; `T-18` — 12 → 2 on the named condition) | S5 raises caution; mitigations exist but need an owner and funding; S6 row 6 resolves on the named condition | **2** with preconditions stated as conditions and carried into the decision record, plus the tripwire metric that would force the move | ✅ |
| 5 | **PP disqualified** (`T-07` and `T-13` — class 5, `Xp`; `T-04`, `T-09`, `T-12` — class 6, `Xr`) | S2: an `Xp` fires (latency class, offline, identity class, residency) — or an `Xr` takes a named responsibility off — or S6 concludes unavailable | **5** (whole scope) or **6** (named responsibility) → **8** naming candidates with `COMPARATIVE FIT UNEVALUATED`. Note the canonical shape: `T-04`, `T-09` reach class 12 **first**, per §3.1 | ✅ |
| 6 | **Pro-code preferable** (`T-13`) | S1 triggers `ALT-005` (product-grade experience, public third-party API, frozen behaviour). S2/S5 exit; S7 gates **must** pass for `ALT-005` too (`DC-D-110` `FULL ENGINEERING CAPABILITY`) | **5** → **8** naming `ALT-005`. The model may **not** say *custom is better* — only that PP is excluded and `ALT-005` is the candidate. `T-13`'s own wording: *scope narrowing, not evaluation* | ✅ |
| 7 | **SaaS / package preferable** (no canonical `T` terminates here — correctly, since *"BUY preferred"* is a withdrawn preference class. `T-10` and `T-14` are the two that name `ALT-011` as a candidate) | S0/S1: standardised, non-differentiating domain (`DC-D-002`) → `ALT-011`, `ALT-007` at `AA-36` rung 0 | **8** naming `ALT-011`, with the buy-check obligation and `COMPARATOR EVIDENCE ABSENT`; or **13** form (b) if no exit fires. *"Strongest candidate"* means **first to assess**, never *chosen* | ✅ |
| 8 | **Hybrid** (`T-11` — class 3 with all gates passing; `T-06` — scope pair 2 + 3; `T-05` — class 3 conditional) | S5: an `Xr` on a **bounded, nameable** excess (compute, guarantee, duration, protocol, network reach). S7: all five gates satisfied | **3** or **4**, as a **scope pair** — class 2 for the application, class 3 for the relocated responsibility. Never collapsed into one verdict | ✅ |
| 9 | **Security / governance dominant** (`T-08`; `T-18`) | S2 absolutes (`059`, `062`, `067`); S6 row 3 (control × funding), row 6 (authorization semantics) | **5** where a mandated control is unavailable; **7** where it is unfunded (`7-INFEASIBLE`); **2** where identity propagation is implemented; **12** where propagation feasibility is `UNKNOWN` | ✅ |
| 10 | **Scale / performance dominant** (`T-09` — recovery/availability; `T-05` — throughput; `T-04` — freshness) | S5 envelope: limits **exclude designs, never prove performance**. S9: validation level V2–V4 named and budgeted | **6** on a documented ceiling for a named responsibility; **12** where the figure is unmeasured (`DC-D-085`, `086`, `087` all blocking) | ✅ |
| 11 | **Economics reverses technical preference** (`T-14`) | S5 leaves PP viable; S8 prices all ten dimensions; the mandated control's population is unfunded, or the audience×frequency shape moves the entitlement line | **7**, rendered with its subtype: `7-INFEASIBLE` where a mandated control is unfunded, `7-UNATTRACTIVE` where it is proportionality (§16.4) → **8**. **Never** implies another class is cheaper | ✅ |
| 12 | **Operability reverses technical preference** (`T-05`'s **operator-gate-fails branch** is the canonical instance; `T-11` is the inverse — the gates pass and *that is the finding*. **No canonical `T` terminates on composed row 9**; `T-03` and `T-10` carry `DC-D-104` but end elsewhere — recorded for G5) | S5 leaves the option technically viable; S7 gate fails — no named operator (row 2), or criticality ≥2 classes above demonstrated maturity with no funded plan (row 9) | **2** where the responsibility stays in-platform with the tripwire stated (`T-05`'s documented branch); **5** where the pattern needs an external component and no operator can exist; **11**/**12** for row 9, which is **platform-independent** and must never render as a PP exclusion | ✅ |
| 13 | **Volatile fact blocks the decision** (`T-05` carries the connector conflict; matrix §3 row 5) | S5 sizing rests on `DC-D-039` — `CONFLICTED` by 20×, blocking, and in the commercial volatility register. §12 rule 4 creates the verification obligation; §3.1 forbids settling an exclusion on it | **12**, naming the re-read **and** the measurement. Cuts across `ALT-004`, `006` and `009` symmetrically | ✅ |
| 14 | **Unexpected material concern** (the Q-11 case; **no canonical `T` exists — that absence is the gap**) | A concern outside `constraints_to_check`, outside the 9-token catalog, and possibly outside the 12 (e.g. document generation at volume, which the corpus records as absent). §6.3 obligation fires: evaluated at proportional depth, marked **no canonical basis**, logged as an authoring feedback item | Whatever the evidence supports — including **12** if it is decision-changing and unresolvable. **The concern is never suppressed for lacking an id**, and §6.2's D0 rule forbids retiring it for want of information | ✅ |
| 15 | **Multiple defensible options** (`T-14` — six candidates; `T-09`, `T-12` — candidate sets that are *sets to assess*) | S9 step 7a: exclusion and candidate generation available; §4A.2 returns no discriminating signal | **8** with ≥2 candidates and `COMPARATIVE FIT UNEVALUATED`, or **13** form (b). The model states plainly that evidence does not support a single winner | ✅ |
| 16 | **Insufficient evidence** (`T-15`; `T-16`; `T-18`) | S3: one of the 28 is `UNKNOWN`, a `B*` scope is engaged, or §3.1 refuses a settled exclusion on non-decision-grade evidence | **12**, naming the evidence task, its expected form **and the outcome each resolution would produce** — which is what makes the task worth funding. Owner and date are **engagement-resolved**, not pack-authored (§24) | ✅ |

**Canonical scenario id audit.** All eighteen are referenced and each is used for exactly one canonical
meaning. The Step-3A v1 defect — `T-10` cited both for *operability reverses preference* and for
*citizen-built artefact becomes enterprise-owned* — is repaired: `T-10` is the **migration** scenario only,
and scenario 12's canonical instance is `T-05`'s operator-gate-fails branch.

| Canonical id | Canonical subject | Cited by scenario |
|---|---|---|
| `T-01` simple departmental internal app | class 1 / class 13 `ALT-003` | 2, 3 |
| `T-02` Excel replacement | class 2 | 3 |
| `T-03` business-critical internal app | 12 → class 4 hybrid | 12 (as a row-9 near-miss) |
| `T-04` external customer portal | 12 → class 2 or 6 (`Xr`, freshness) | 5, 10 |
| `T-05` high-volume integration | class 3, or class 2 when the operator gate fails | 4, 8, 12, 13 |
| `T-06` complex data-centric enterprise app | scope pair 2 + 3 | 8 |
| `T-07` strict low-latency | class 5 (`Xp`) | 5 |
| `T-08` regulated, security-sensitive | 12 → class 3 or 5 | 4, 9 |
| `T-09` mission-critical workload | 12 → class 6 (recovery commitment) | 5, 10, 15 |
| `T-10` citizen-developed app become enterprise-owned | 12 → class **14** → 8 | carry-forward |
| `T-11` hybrid platform + cloud-native | class 3, gates pass | 8, 12 (inverse) |
| `T-12` existing enterprise system owns it | class 6 → 8 (`ALT-007`) | 2, 5, 15 |
| `T-13` custom application preferable | class 5 → 8 (`ALT-005`) | 5, 6 |
| `T-14` economically unattractive | class 7 → 8 | 11, 15, 7 |
| `T-15` insufficient information | class 12 | 16 |
| `T-16` conversational assistant | class 12 in **every** class | 16, carry-forward |
| `T-17` multi-month approval process | class 2 (`Ri`, not an exit) | 3, carry-forward |
| `T-18` per-user backend authorization | class 12 → 2 on condition (`Xc`, never an exclusion) | 4, 9, 16, carry-forward |

**Four canonical scenarios carried explicitly into G5**, because they exercise mechanisms the sixteen above
touch only in passing:

- **`T-10`** — citizen-built artefact become enterprise-owned → outcome **14**, *migration, not
  remediation*. The class exists because *the remediation estimate a sponsor is usually given is for the
  wrong work*.
- **`T-16`** — conversational/agentic surface → **12** in **every** class including `ALT-004`. The corpus
  holds no fit assessment of an agent surface anywhere; the honest output is a block, not a candidate set.
- **`T-17`** — the `Ri` test. Before the canonical Repair V3 this case rendered as *"excluded for this
  responsibility"* for a requirement whose documented answer stays in-platform. G5 must confirm the
  authored model reaches **class 2**.
- **`T-18`** — the `Xc` test. Same defect shape: an in-platform authorization design constraint with no
  off-platform destination named anywhere. G5 must confirm **12 → 2**, never 6.

**No scores were manipulated, because there are none.**

---

## 21. Neutrality result

| # | Test | Result | Mechanism |
|---|---|:--:|---|
| **N1** | Can PP lose to process change? | **YES** | S0 runs **before** any option class is generated; `ALT-002` is a mandatory S1 member; outcome class 10 is reachable with no PP analysis performed |
| **N2** | Can PP lose to existing capability? | **YES** | S1 trigger *"capability already exists in the estate"* → `ALT-001`/`003`/`007`/`011`; outcome 13 states explicitly that PP is **not excluded** and the alternative is still the answer — the class exists precisely because the previous model biased toward PP on the commonest departmental shape |
| **N3** | Can PP lose to SaaS/package? | **YES** | `DC-D-002` differentiation + `AA-36` rung 0 (configure-or-buy **before any app type**) → `ALT-011`; outcome 8 or 13(b) |
| **N4** | Can PP lose to pro-code? | **YES** | `Xp` exits at S2/S5 (`DC-D-012`, `016`, `020`, `042`, `084`, `105`, `106`, `107`) → outcome 5/6 → 8 naming `ALT-005`. Note the honesty constraint: PP **loses**, `ALT-005` is not thereby declared *better* |
| **N5** | Can PP participate only as part of a hybrid? | **YES** | `Xr` = a bounded responsibility leaves the platform and PP legitimately keeps the rest → outcomes 3 / 4, rendered as **scope pairs** |
| **N6** | Can the model conclude DECISION BLOCKED? | **YES** | S3 on 28 + 3 criteria, re-run after S8; outcome 12; scenarios 13, 14, 16 |
| **N7** | Does PP gain preference merely because the PP pack has richer domain knowledge? | **NO** | Four independent mechanisms below |

**N7 in detail** — the hardest test, because it is a structural bias rather than a rule:

1. **Preference is licensed by comparator evidence, not by knowledge depth.** §4A.4 step 4 permits a
   preference **only** where a discriminating signal exists — one axis today, and on that axis the
   comparator wins.
2. **Depth of knowledge is confined to evaluation, not to ranking.** Domain pull answers *can this option
   satisfy this requirement*. It never emits a comparative claim; `COMPARATOR EVIDENCE ABSENT` is the
   default output for the comparison.
3. **Five universal claims are forbidden output**, including *"custom development is more expensive"* and
   *"low-code is faster"* — the two that a knowledge-rich PP pack would otherwise generate for free.
4. **The gates are symmetric and bite hardest on the alternatives — and the model says so.** `ALT-005`,
   `ALT-006` and `ALT-009` are made *unavailable* by S7 more often than PP is. The model must state that
   this is a **documented capability gap in those classes**, not a PP advantage, and must equally state the
   `CANDIDATE` signals that favour `ALT-001`/`007`/`011` on the same criteria (an operator already exists
   and is funded).

**Residual neutrality risk, recorded rather than closed.** The corpus's negative evidence is far richer for
PP than for any alternative (16 documented negatives on PP's automation surface against 33 on the
alternatives it recommends — the asymmetry runs *against* PP there, but the coverage of *fit* runs toward
it). The model's countermeasure is the `COMPARATOR EVIDENCE ABSENT` marker being **part of the outcome
string**, not a footnote — so a reader cannot mistake unevaluated for evaluated-and-lost. G5 must test this
on `T-13` and `T-14` specifically.

---

## 22. Defensibility result

**Question:** could a senior architect, a governance/security reviewer, a financial stakeholder and a
business sponsor each understand why the preferred option won and why serious alternatives lost?

**PASS**, on the following exposed reasoning:

| Reader | What the model exposes to them |
|---|---|
| **Senior architect** | Exit class and scope per disqualifier; the composed rows that fired and why per-criterion favourability did not compose; the `Ri` redirects that changed the design without excluding anything; the validation level required and why; the envelope figures re-read at the decision date with their dates |
| **Governance / security reviewer** | Which mandated controls were checked, against which clause; the authorization enforcement point and whether the design changes its semantics; residency and deployment model as absolutes decided first; what is unfunded, and the consequence stated as infeasibility rather than as a trade-off |
| **Financial stakeholder** | The same ten cost dimensions priced for every surviving candidate, on the same workload and operating model; cost of inaction priced as an option; growth at horizon; what is a hypothesis (users-to-work ratio) and what is a reading; every comparative TCO claim marked absent rather than guessed |
| **Business sponsor** | Whether a technology response is warranted at all; which options were serious and which were disqualified by what requirement; the preconditions the organisation must satisfy, with owners and funding; the risks accepted; the uncertainty that remains and what it would cost to close — and, where the answer is class 12, what each resolution would produce |

**Four properties that carry the defensibility, and one that does not.**

- **Decisive evidence is anchored.** Every verdict cites an SU row id, a domain-knowledge file or a
  registered row — never a filename alone.
- **Decisive concerns are visible.** The concern-coverage line shows the depth used for each of the twelve
  per option, so *not material* is distinguishable from *not examined*.
- **Assumptions and preconditions are separated from findings.** `Assumed` rows carry their basis,
  `verificado_em` and `validade`; expired rows read as weak `Assumed` and may not be cited as `Confirmed`.
- **Uncertainty is priced, not hidden.** `custo` + `swing` on every Unknown; `swing: decisivo` is what makes
  class 12 legible as a decision rather than a failure.
- **Not carried by verbosity.** D0 and D1 assessments are one line. The comparison is a per-option block
  plus a twelve-line coverage summary — not a 12×N proof-of-checking matrix (§16, §28-D below).

---

## 23. Complexity result

| # | Test | Required | Result | Evidence |
|---|---|---|:--:|---|
| **A** | Does runtime require the canonical Decision Criteria register? | NO | **NO** | The 116 criteria compress to 12 concerns (§7). `criteria-register.md` is **demoted to an authoring artifact** — a change from the Step-1 map, recorded in §24. No `DC-D-NNN` id appears in any runtime file |
| **B** | Does runtime preload all domain knowledge? | NO | **NO** | Pull-based (§10), depth-gated (D0/D1 pull nothing); `aisa-options` already forbids putting pack contents in a prompt. **The same rule now governs the decision registers**: stage-local, named by the procedure, no router (§5.1) |
| **C** | Can material concerns outside declared constraint lists be followed? | YES | **YES** | §6.3 emergent-concern obligation, three sources including *outside all twelve*; the option space (§5 S1) gives every concern a reachable consequence |
| **D** | Are all serious options considered against all material concerns? | YES | **YES** | S5 is the coverage stage; the concern-coverage line makes it auditable; silent omission is defined as a defect |
| **E** | Is depth proportional rather than uniform? | YES | **YES** | Four depths, seven escalation drivers, two worked contrasts (§6.2) |
| **F** | Can the decision logic be understood without reading canonical research? | YES | **YES** | The runtime spine is one procedure + five stage-local registers (§24); the semantics are seven terms; the outcome set is a closed 14 with render templates. Canonical files are cited as provenance, never as required reading. Only **6** of the 22 semantic objects surface as user vocabulary (§17) |
| **G** | Implementable without becoming a rules engine? | YES | **YES** | No scoring, no weights, no pairwise matrix, no routing table. The only enumerations are the ones the corpus itself closes: 12 composed rows, 14 outcomes, 11 `ALT` classes, 28+3 blocking criteria |
| **H** | Could removing any proposed concern create a material blind spot? | preserve if YES | **YES for all 12** | §4.1 tests every merge and split against the survival test; C7 and C8 are the sharpest cases — zero direct exits, decisive only through composed rows |
| **I** | Is framework complexity justified by decision value? | YES | **YES** | Net runtime change: `decision-tree.md` 157 lines of scored branches → a procedure + 5 registers; the 10 registers the Step-1 map projected reduce to 5; the Options concern set goes from an implicit 5 to an explicit, complete 12 |

**Complexity ledger.**

| Object | Count | Closed by |
|---|---:|---|
| Shared Options vocabulary terms | **6** (4 new) | §17.2 |
| Internal decision semantics (not user-facing) | 8 | §17.1 |
| Material decision concerns | 12 | authoring (§4.1 survival test) |
| Ordered stages | 10 | canonical matrix §5 + 2 prepended |
| Decision semantics terms | 7 (+2 non-exits) | `decision-criteria.md` §2.5 |
| Outcome classes | 14 | **closed set**, testable |
| Option classes | 11 | `alternatives.md` §4 |
| Composed disqualifier rows | 12 | registered; adding rows would be invention |
| Blocking criteria | 28 (+3 `B*`) | `decision-criteria.md` §5.2 |
| Standing constraint floor | 10 | §19 |
| Depth levels | 4 | §6.2 |
| Validation levels | 4 | canonical |
| Runtime artifacts | 6 | §24 |
| Numeric scores / weights | **0** | doctrine |
| New kernel states | **0** | §3 |

---

## 24. Exact Step 3B implementation scope

**Runtime artifacts — 6, not the 10 the Step-1 map projected.** Loading is **stage-local** (§5.1):
`decision-tree.md` is the always-readable spine; the five registers are consulted only at the stage that
needs them, named by the procedure itself. Step 3B must not preload them and must not build a router.

| # | Artifact | Verdict | Content | Why it is load-bearing |
|---:|---|---|---|---|
| 1 | `decision-tree.md` | **REWRITE** (filename kept — `pack.yaml.decision_tree.source`, `lens-technology`, `solution-architect`, `aisa-simulate` reference it) | The 10-stage procedure (§5) · the 12 concerns (§4) · decision semantics incl. exit classes and the class→outcome map (§3) · the depth ladder and emergent-concern obligation (§6) · validation levels V1–V4 · the domain-pull rule (§10) | The single readable spine. Everything else is a register it runs against |
| 2 | `decision-model/outcome-classes.md` | **CREATE** | The closed 14 with render templates, class 13's two non-mergeable forms, the scope-pair rule, and the four-part comparator separation with `COMPARATOR EVIDENCE ABSENT` as default | Closure is testable only if the set is written once. **Absorbs the map's separate `comparator-rules.md`** — §4A is the render discipline for these strings, not a separate mechanism |
| 3 | `decision-model/blocking-set.md` | **CREATE** — **engagement-neutral** (see below) | 28 `B` + 3 `B*`, each with: the evidence needed · the closure action **pattern** · the likely responsible **role type** · the expected evidence **form** · the canonically justified `custo` default · `swing: decisivo` · the outcome each resolution would produce | S3 has nothing to run without it; it is also the model's question generator |
| 4 | `decision-model/composed-disqualifiers.md` | **CREATE** | The 12 registered rows with criteria, consequence, class and reachable outcome — including rows 6 and 9's conditional mappings | S6 has nothing to run without it; the rows are invisible to per-criterion reading |
| 5 | `decision-model/alternatives-register.md` | **CREATE** | `ALT-001…011`, the trigger→class map **as candidate generation**, the symmetry rule, the five forbidden universals as prohibited output, and the §5.3 symmetric unknowns | S1 has nothing to run without it; it is the mechanism that makes N1–N5 reachable |
| 6 | `decision-model/volatility-register.md` | **CREATE** | 10 commercial + 20 service-limit entries with per-row re-verify triggers; the live `DC-D-039` 20× conflict; dated tripwires feeding `/decide` and `/revisit` | §12 rule 4 has nothing to run without it; it is what keeps a 2026 figure from becoming a timeless rule |

**`blocking-set.md` — pack-authored guidance vs engagement-resolved commitment.** The register is a
**pattern**, not a plan. The line between them is strict, because a pack that ships a named owner and a
duration is asserting facts about an organisation it has never seen.

| Pack-authored (belongs in the register) | Engagement-resolved (never in the register) |
|---|---|
| The evidence needed, stated as a question | The **actual named owner** |
| The closure action pattern (*"read the clause verbatim"*, *"measure on a prototype with the named instrumentation"*, *"name the four reconciliation roles"*) | The **actual due date** |
| The likely responsible **role type** (sponsor · platform-owning team · network policy owner · licensing owner) | The **actual elapsed duration** |
| The expected **form** of the evidence (a clause · an inventory · a measurement · a drill result) | The **commitment** anyone makes to close it |
| The `custo` default where canonically justified, and `swing: decisivo` by construction | The engagement's own re-priced `custo`/`swing` where `/simulate` corrects it |
| The outcome each resolution would produce | Which resolution actually occurred |

At runtime the right-hand column lands on the engagement's own `Unknown` row (`quem responde`,
`criticidade`, `custo`, `swing`) and, on resolution, in `answers.md` — mechanisms that already exist. The
register supplies the **shape** of the question; the engagement supplies the commitment.

**Four map-projected artifacts deliberately not created at runtime** — recorded as revisions to
`pp-pack-authoring-map.md` §3.2 for the map owner to accept or reject:

| Artifact | Disposition | Reason |
|---|---|---|
| `decision-model/criteria-register.md` (116 rows) | **AUTHORING ONLY** | Complexity test A. The concerns carry the durable question shape; the register's states and figures reach an engagement through domain pull and the volatility register. Keeping it at runtime would make the canonical register a runtime payload — Principle 5 violated |
| `decision-model/exit-classes.md` | **MERGE** into `decision-tree.md` §semantics | Seven class definitions plus one mapping table. Splitting the semantics from the procedure that applies them is how the V1 rendering defect happened |
| `decision-model/comparator-rules.md` | **MERGE** into `outcome-classes.md` | §4A is the discipline for writing terminal strings; it belongs with the strings |
| `decision-model/validation-levels.md` | **MERGE** into `decision-tree.md` S9 | Four levels, one paragraph each |
| `decision-model/anti-pattern-register.md` (68 entries) | **SPLIT** — the 3 `GATE` and 4 `CONSTRAINT` entries absorbed into S2/S6/S7; the 61 `ANTI-PATTERN` detection signals to domain knowledge, pulled at D3 | A 68-entry register is a fact dump at runtime. The 7 enforcement-strength entries are decision logic; the rest are detection craft |

**Runtime contract edits — minimal, and only these.**

| File | Edit |
|---|---|
| `pack.yaml` | `technology.constraints_to_check` → the 10 of §19, with the non-limiting comment; add a `decision_model:` block listing artifacts 2–6 **with the consuming stage per register** (§5.1) and a comment stating they are stage-local, not preloaded; `decision_tree.consulted_in_phase: options` unchanged; `pack_version` bump |
| `lens-technology/SKILL.md` | Execution step 2, two clauses (§9): *verdict per constraint* → *verdict per material concern, floor not ceiling, classified by exit class and scope*; *candidate branches* → *candidate option classes*. Nothing else |
| `solution-architect.md` | Options mandate: candidates generated from the `ALT` trigger map, not from three branches. One sentence |
| `chairman-synthesis/SKILL.md` | The `options.md` template → §16.1/§16.2. The do-nothing + non-technology floor stays |
| `architecture-templates/` | Re-scoped: architecture shapes reachable **after** an outcome class, not the option space. `sharepoint-first` / `dataverse-first` / `hybrid` survive as shapes under outcome classes 1, 2, 3 and 13 |

**Not in Step 3B scope.** `domain-knowledge/*` re-taxonomy (map §7, Step 4) · the `glossary.md` split beyond
adding the 14 Options terms · `question-bank.md` beyond rewriting the *Reachable outcomes* block against the
closed 14 · Discovery `extra_signals` (Phase G is final) · kernel files · `epistemics.half_lives_override`
(map Q-08, separate).

**Two authoring items carried forward, not fixed here.**

1. **C10 Discovery thinness** (§8). Operability has no direct Discovery cue and three S7 gates depend on
   it. **No Discovery signal is added — not in Step 3A and not by default in Step 3B.** Step 3B's
   obligations are exactly three: (a) **S7 must evaluate C10** for every serious option; (b) where material
   evidence is absent, expose the appropriate `Unknown` (`DC-D-006`, `073`, `104`, `110` are all blocking,
   so the swing is `decisivo` and the terminal is class 12); (c) use the **existing** question and probe
   resources where they help — `Q-GOV-06`, `P-GOV-07`, `P-FIN-05`, and `glossary.md` A2/A6 already carry
   *operational ownership*, *operational maturity class* and *pro-code capacity*. Adding a Discovery cue is
   a **pilot-calibration decision** to be taken at the retro with real evidence that the existing route is
   insufficient — not a Step 3B default. Phase G's `extra_signals` set stays at 36.
2. **Concerns with no canonical basis** (§6.3 source 3), e.g. document generation at volume. The model
   evaluates them and logs them; accumulating them is the input to a future research commission.

**Gate on entry to Step 3B:** the G5 replay of `T-01`…`T-18` against the authored spine (map §9 S6). No
Discovery or domain-knowledge authoring is worth doing against a spine that fails the corpus's own
scenarios.

---

## 25. Bounded correction record (2026-09-04)

Review verdict on the v1 design: `PASS WITH BOUNDED CORRECTIONS`. Seven corrections applied. **The
approved core is unchanged**: 12 concerns · 10 stages · broad coverage / selective depth · canonical
criteria compression · 11 `ALT` classes · closed 14 outcome classes · no weighted scoring · pull-based
domain knowledge · economics and operability first-class · the Q-11 coverage model · constraints as floor.

| # | Correction | Applied in |
|---:|---|---|
| 1 | **Disqualifier epistemics tightened.** A hard exclusion requires `Confirmed` + current. `Assumed` yields a **provisional** disqualifier — carried with its basis where not decision-changing, escalated to an evidence obligation + class 12 where it is. `Unknown`/`Conflicted`/materially-expired cannot settle one. *(Micro-correction 2026-09-04: v2's table wrongly let a non-decision-changing `Assumed` settle an exit. `Assumed` alone now settles nothing, and §3.1.1 separates the two responsibilities that were being conflated.)* | §3 (row), **§3.1 + §3.1.1**, §5 S3, §16.1, §16.4, §20 scenarios 5, 13, 16 |
| 2 | **D0 tightened.** D0 requires an **affirmative** non-materiality rationale from available evidence; absence of information is an evidence gap at D1 with a priced `Unknown`, never D0. Not every gap blocks | §6.2 (definition, 3 consequences, both worked examples), §20 scenario 14 |
| 3 | **Class 7 disambiguated** — no class 15. Mandatory subtype `7-INFEASIBLE` (unfunded mandated requirement) vs `7-UNATTRACTIVE` (proportionality), each with its own render string. The disjunction is never printed where evidence supports one condition | **§16.4** (new), §5 S8, §13 rule 2, §16.3, §20 scenarios 9, 11 |
| 4 | **Registers made stage-local.** `decision-tree.md` is the always-readable spine; S1→alternatives, S3→blocking-set, S6→composed-disqualifiers, S9→outcome-classes, volatility only on an active volatile-fact question. No preloading, no router | **§5.1** (new), §23 test B, §24 |
| 5 | **Internal semantics separated from user vocabulary.** 14 proposed terms → **8 internal** (exit codes, `Ri`, `Cf`, D0–D3, class numbers, subtype codes, scope-pair mechanics, all ids) living in `decision-tree.md`/registers with plain-language renderings, and **6 shared** — of which 2 already exist in `glossary.md` Part A. Step 3B authors **4 new terms** | **§17.1 / §17.2** (rewritten), §16.1, §23 test F |
| 6 | **Canonical scenario ids repaired.** The duplicate `T-10` is fixed: `T-10` is the **migration** scenario only; scenario 12's canonical instance is `T-05`'s operator-gate-fails branch, with `T-11` as the inverse and composed row 9 recorded as having **no** canonical scenario. Full 18-row audit added; `T-17` and `T-18` promoted to G5 carry-forwards | §20 (table + **id audit** + carry-forwards) |
| 7 | **Blocking register kept engagement-neutral.** Pack authors the evidence needed, the closure **pattern**, the likely **role type**, the expected **form**, the canonical `custo` default and the per-resolution outcomes. Actual owner, due date, elapsed duration and commitment are engagement-resolved on the `Unknown` row | §5 S3, §8, §16.1, **§24** (new split table) |
| — | **C10 unchanged and re-scoped.** No Discovery signal added. Step 3B: S7 must evaluate C10; absent evidence → the appropriate `Unknown`; use existing questions/probes. A new cue is a **pilot-calibration decision**, not a Step 3B default. `extra_signals` stays at 36 | §24 carry-forward 1 |

**Verification.**

| # | Check | Result |
|---:|---|:--:|
| 1 | No hard exclusion can be settled solely from `Assumed` evidence — decision-changing or not | **PASS** — §3.1 rows 2 and 3 both answer **NO**; classes 5/6/7/9/14 explicitly require `Confirmed` + current evidence on the firing criterion. §3.1.1 keeps evidence grade (can it be settled) separate from materiality (does it block) |
| 2 | D0 cannot be inferred from missing evidence | **PASS** — §6.2 definition + consequence 1; the gap path is D1 + priced `Unknown` |
| 3 | Economic class 7 has unambiguous reason semantics | **PASS** — §16.4, two subtypes, two render strings, trigger-selected |
| 4 | Registers are stage-local, not preloaded | **PASS** — §5.1 table; §24 loading rule; no router introduced |
| 5 | Internal framework vocabulary is not automatically user vocabulary | **PASS** — 8 internal / 6 shared; plain-language renderings given for all 8 |
| 6 | Canonical scenario ids unique and correct | **PASS** — 18-row audit; every id used for exactly one canonical meaning |
| 7 | Blocking register hardcodes no engagement owner or date | **PASS** — §24 split table; the right-hand column lands on the SU row and `answers.md` |
| 8 | C10 does not inflate Discovery | **PASS** — 0 cues added; `extra_signals` = 36 (Phase G value) |
| 9 | No new state machine exists | **PASS** — the five kernel states are unchanged; §3 terms are option verdicts in `options.md`, and §3.1 maps onto the existing `verificado_em`/`validade` and `custo`/`swing` columns |
| 10 | No runtime file modified | **PASS** — `library/packs/pp/decision-tree.md`, `pack.yaml`, `domain-knowledge/*`, lenses, personas and orchestrators untouched; this step wrote one authoring file |

**Unchanged by these corrections**, as instructed: the 12 concerns · the 10 stages · option plurality · the
broad-coverage / selective-depth contract · the emergent-concern obligation · cross-domain handling · the
10 economic dimensions · the operability model · the reversibility model · comparator discipline · the
10-item standing constraint floor · the six-artifact architecture (loading semantics only).

---

`STEP 3A — OPTIONS DECISION MODEL: PASS`
`BROAD COVERAGE / SELECTIVE DEPTH: PASS`
`MATERIAL DECISION CONCERNS: 12`
`ORDERED DECISION STAGES: 10`
`CANONICAL CRITERIA ACCOUNTED FOR: YES`
`CANONICAL CRITERIA REQUIRED AT RUNTIME: NO`
`MATERIAL CONCERNS OUTSIDE DECLARED CONSTRAINTS FOLLOWED: YES`
`ALL SERIOUS OPTIONS TESTED AGAINST MATERIAL CONCERNS: YES`
`WEIGHTED SCORING INTRODUCED: NO`
`DOMAIN KNOWLEDGE PULL-BASED: YES`
`CROSS-DOMAIN INTERACTIONS SUPPORTED: YES`
`VOLATILE FACT VERIFICATION BOUNDARY: PASS`
`ECONOMICS FIRST-CLASS: YES`
`OPERABILITY FIRST-CLASS: YES`
`REVERSIBILITY/STRATEGIC CONSEQUENCE SUPPORTED: YES`
`PP CAN LOSE: YES`
`MULTIPLE DEFENSIBLE OPTIONS SUPPORTED: YES`
`DECISION BLOCKED SUPPORTED: YES`
`DEFENSIBILITY TEST: PASS`
`NEW RUNTIME STATE MACHINE INTRODUCED: NO`
`PP RUNTIME FILES MODIFIED: 0`
`READY FOR STEP 3A REVIEW: YES`

`STEP 3A BOUNDED CORRECTION: PASS`
`HARD DISQUALIFIER REQUIRES DECISION-GRADE EVIDENCE: YES`
`ASSUMED ALONE CAN SETTLE HARD EXCLUSION: NO`
`D0 REQUIRES AFFIRMATIVE NON-MATERIALITY RATIONALE: YES`
`ECONOMIC CLASS 7 REASON DISAMBIGUATED: YES`
`DECISION REGISTERS STAGE-LOCAL: YES`
`INTERNAL SEMANTICS SEPARATED FROM USER VOCABULARY: YES`
`CANONICAL SCENARIO IDS UNAMBIGUOUS: YES`
`BLOCKING REGISTER HARDCODES ENGAGEMENT OWNER/DATE: NO`
`C10 DISCOVERY SIGNAL ADDED: NO`
`NEW RESEARCH REQUIRED: NO`
`PP RUNTIME FILES MODIFIED: 0`
`READY FOR STEP 3B IMPLEMENTATION: YES`

`STEP 3A FINAL MICRO-CORRECTION: PASS`
`ASSUMED ALONE CAN SETTLE HARD EXCLUSION: NO`
`NON-DECISION-CHANGING ASSUMPTION AUTOMATICALLY BLOCKS: NO`
`DECISION-CHANGING ASSUMPTION REQUIRES EVIDENCE OBLIGATION: YES`
`SETTLED EXCLUSIONS REQUIRE DECISION-GRADE EVIDENCE: YES`
`SCENARIO MAPPINGS CHANGED: NO`
`PP RUNTIME FILES MODIFIED: 0`
`READY FOR STEP 3B IMPLEMENTATION: YES`
