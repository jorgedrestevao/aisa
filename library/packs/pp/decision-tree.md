---
dt_id: pp-options-decision-procedure
applies_to_phase: options
consulted_by: [lens-technology, solution-architect, chairman-synthesis, aisa-simulate]
registers_are_stage_local: true   # see §8; the consuming stage is declared in pack.yaml.decision_model
---

# Options Decision Procedure — `pp`

<!--
provenance: RUNTIME (Options spine)
authored: 2026-09-04 (Step 3B1) · design authority: Step 3A — Options Decision Model
This file is the durable reasoning procedure. The authoring evidence that produced it
(the canonical criteria register, provenance tables, the Step 3A audit) lives in the
authoring reports and never loads at runtime.
-->

## 1. Purpose and phase gate

This file is the **readable spine** of the Options phase for the `pp` pack: an ordered, semantic,
technology-neutral evaluation procedure. It replaces the scored three-branch tree.

- **Consulted in Options (and Decision), never before.** Discovery and Framing are pre-technology by
  construction (`library/kernel/phases.md`; `.claude/rules/no-tech-mention-before-options.md`).
- **It consumes the Shared Understanding.** It declares no input signature of its own, so nothing here
  can cap what Options may consider. Where the SU carries nothing on a material concern, the procedure
  **exposes the gap**; it does not fill it.
- **It does not decide.** It produces option assessments and *(scope, outcome)* pairs. The chairman
  synthesises; the user decides (`/decide`).

**Architecture shapes are not the option space.** `architecture-templates/` describes shapes reachable
*after* an outcome establishes that a solution containing this platform remains viable. They are never
the top level of the comparison.

---

## 2. Governing doctrine

| # | Principle | Consequence here |
|---|---|---|
| 1 | Light framework, not lightweight reasoning | The 10 stages and 12 concerns are framework; the reasoning under them is unbounded |
| 2 | Compress repetition, not decision coverage | The concerns are a complete compression of the canonical criteria — nothing was dropped |
| 3 | Broad coverage, selective depth | Every serious option × every material concern; depth is proportional (§7) |
| 4 | Materiality determines depth | Criticality × uncertainty × consequence × reversibility |
| 5 | Domain knowledge deepens a concrete decision question | Pull, never preload (§9) |
| 6 | An active technology pack must be able to reject its own technology | §13, §14 |

**States, not scores.** No numeric fit score, no weight, no aggregated verdict, no ordinal ladder
(`forte`/`adequada`/…) enters this procedure at any point. Combinations exist in which every dimension
reads *conditional* and the combination is unavailable; a weighted average passes all of them.

**Strong on disqualification, modest on preference.** The pack's evidence supports exclusion far better
than it supports preference. Being able to exclude this platform is **not** evidence that a replacement
is better (§13).

**No new state machine.** The five kernel states (`library/kernel/states.md`) carry all epistemics. The
terms below describe *option verdicts*, which live in `options.md`, not in the Shared Understanding.

---

## 3. Decision semantics

Seven terms. Internal codes are shown because the procedure executes on them; **they are never rendered
to the engagement** (§14.3).

| Term | Meaning | Rendered as |
|---|---|---|
| **Disqualifier** | Known evidence makes an option non-viable under a material requirement, **at a named scope**. Hard (settles non-viability) or provisional (conditional on an assumption) — §4 governs which | *"excluded for the whole scope"* · *"excluded for `<the named responsibility>`"* · *"economically infeasible / unattractive"* · *"excluded only in combination with `<the other conditions>`"* |
| **Precondition** | The option becomes viable only if a stated condition becomes true — named, owned, funded, dated | Stated as a condition, carried into the decision record |
| **Trade-off** | A material disadvantage consciously accepted; the option stays viable | `Assumed` row with its basis declared |
| **Risk** | A material adverse outcome whose likelihood or impact must be understood or mitigated | `Risky` row — impact + proposed mitigation |
| **Uncertainty** | Missing, stale or conflicted evidence capable of changing viability, architecture, risk, cost or preference | `Unknown` / `Conflicted` / an **expired** row, priced with `custo` + `swing` |
| **Preference** | Evidence-backed reason to favour one viable option over another | Only where a discriminating comparator signal exists (§13). Never a score |
| **Decision blocker** | Uncertainty or conflict material enough that selecting a preferred option would not yet be defensible | *"decision blocked — more evidence required"*, naming the evidence and what each resolution would produce |

**Exit scopes (internal `Xp` / `Xr` / `Xe` / `Xc`).** A disqualifier always carries a scope: the whole
solution scope; a named responsibility; an economic finding; or a **registered** combination only. The
scope decides which outcomes are reachable (`decision-model/outcome-classes.md`).

**Two consequences that are not disqualifiers, and must never produce one.**

| | Meaning | May never produce |
|---|---|---|
| **In-platform redirect** (internal `Ri`) | A documented in-platform pattern, store, mechanism or surface becomes unavailable and the documented answer is a **different in-platform choice**. Nothing leaves the platform | Any exclusion outcome. It routes to *fit with constraints*, or to *alternative sufficient* where the destination is a documented sufficiency |
| **Combination input** (internal `Cf`) | The finding carries no exit and no redirect of its own; its value is an **input** to another finding's exit or to a registered composed row | Any outcome on its own. Terminating on one is a category error — resolve the finding it feeds |

**Scope pairing (normative).** One outcome per **scope**, not per engagement. A responsibility-scoped
exclusion takes one named responsibility off the platform and leaves the rest, so an engagement
legitimately terminates in more than one outcome, each bound to a named scope. `options.md` renders
*(scope, outcome)* pairs and never collapses them — collapsing is how a bounded exclusion becomes a
whole-solution rejection.

---

## 4. Evidence grade required for a disqualifier

> **Binding rule. A settled hard disqualifier requires decision-grade evidence.
> `Assumed` evidence alone never settles a hard exclusion.**

| Evidence state of the disqualifying fact | Settles a hard exclusion? | What the procedure does |
|---|:--:|---|
| **`Confirmed` and current** (`verificado_em` + `validade` not expired) | **YES**, where the rule permits an exit at that state | Render the exclusion at its scope |
| **`Assumed`, not decision-changing** | **NO** | **Provisional disqualifier**, carried explicitly with its basis. It does not block the decision merely for being `Assumed`; it does not become a settled exclusion. Where an independent **`Confirmed` and current** disqualifier already excludes the option, the settled exclusion rests on **that** evidence and the assumption is corroboration, never the ground |
| **`Assumed`, decision-changing** (resolving it could restore viability or change which option is preferred) | **NO** | Provisional disqualifier **+ evidence obligation**: expose the assumption and its basis; name the evidence that would settle it and its expected form; open an `Unknown` with `swing: decisivo`; **decision blocked** where resolving it could change the recommendation |
| **`Unknown`** | **NO** | Evidence obligation created or retained. Decision blocked where decision-changing |
| **`Conflicted`** | **NO** | Evidence obligation naming both readings and what would resolve them. Decision blocked where decision-changing |
| **Materially expired `Confirmed`/`Assumed`** | **NO** | An expired row reads as **weak `Assumed`** and may never be cited as `Confirmed`. Revalidate (`/answer --revalidate`), or treat as the `Assumed` rows above. *Materially* expired means the decay matters here — a platform-technical row past its half-life carrying a service limit is materially expired; an organisational row a week past on a fact nobody disputes is not |

**Two separate responsibilities. Do not conflate them.**

```text
evidence grade      → determines whether an exclusion can be SETTLED
materiality / swing → determines whether unresolved uncertainty BLOCKS the decision
```

Decision-changing controls whether unresolved `Assumed` evidence must block the decision. **It does not
control whether `Assumed` evidence becomes fact.** No degree of immateriality upgrades an assumption to
`Confirmed`.

**Settled outcomes cannot be emitted from `Assumed` evidence alone** — decision-changing or not. The
settled exclusion outcomes are named in `decision-model/outcome-classes.md`; they require `Confirmed`
and current evidence on the finding that fires them. A provisional finding may still appear in the
option assessment; where it is decision-changing, the terminal is **decision blocked** until resolved.

**Symmetry.** This rule applies to every option class, not to this platform. An `Assumed` claim that a
*custom build* cannot meet a requirement is held to exactly the same standard as one about the platform.

---

## 5. The 12 material decision concerns

These are the **coverage object** of Options. They are not a checklist, not scored, and not the pack's
declared constraint list (§7.4).

| # | Concern | The decision question |
|---|---|---|
| **C1** | Need, value and existing capability | Should anything be built or changed at all, and does the organisation already own something that answers this? |
| **C2** | Functional and process fit | Can the option carry the required work shape, human waits, exception and failure behaviour? |
| **C3** | User and experience fit | Can it deliver the required interaction, identity class, accessibility, distribution and offline behaviour? |
| **C4** | Data and information fit | Can it satisfy authority, relationships, integrity, granularity, atomicity, volume, retention and residency? |
| **C5** | Integration and ecosystem fit | Can it exchange with the required systems, at the required guarantee, throughput, payload and network boundary? |
| **C6** | Security, privacy and control | Can the mandated controls, key custody, egress control and authorization model be satisfied? |
| **C7** | Governance, authority and compliance | Which **roles** may build, change and permit, and on which plane that is enforced; what does the compliance regime bind; is there an owning estate? Roles and mechanisms only — never a person, a signature or an approval (P-21) |
| **C8** | Lifecycle, ALM and change | Can it be built, released, isolated, tested, reversed and changed at the required cadence? |
| **C9** | Scale, performance and resilience | Can it meet peak, growth, concurrency, availability and recovery expectations — and can that be **proven** before commitment? |
| **C10** | Operability, support and ownership | Can the organisation run, observe, recover and support it — which **roles**, using which **mechanisms**, at which recovery objective? |
| **C11** | Economics, entitlement and TCO | Are acquisition, entitlement, growth and operating economics defensible, **on the same dimensions for every candidate**? |
| **C12** | Strategic fit, reversibility and dependency | What dependency, lock-in, exit cost, vendor-change exposure and future optionality does it create, over what lifespan? |

**Two concerns produce no exclusion of their own and are decisive only in combination** — C7 and C8.
They are visible here precisely so that an ungoverned estate or an unreachable isolation rung is not
invisible to per-concern reading (§10).

**Concerns are not stages.** Several concerns are evaluated at more than one stage (C1 at S0 and S1;
C10 at S5 and S7; C11 at S5 and S8), and several stages evaluate more than one concern. §6 is the
**order**; §5 is the **coverage**.

---

## 6. The 10 ordered stages

**The order is not commutative.** Evaluating direction before disqualification produces different — and
wrong — answers. S0–S3 are cheap and can end the engagement.

| Stage | Name | Job | Concerns |
|---|---|---|---|
| **S0** | **Intervention justification** | Is a technology response warranted at all? Value against **full** cost of ownership; process maturity; is the requirement a feature list of the outgoing tool? | C1 |
| **S1** | **Option-class generation** | Which materially different response classes are on the table? Read the dominant requirements against the trigger→candidate map. **Candidate generation only — never a verdict.** | C1 + the dominant requirement of any concern |
| **S2** | **Absolutes and hard viability** | The absolutes first (deployment model · residency · regulatory regime · administrator exclusion · atomicity span · compute intensity), then any other disqualifying evidence already in hand, **per candidate**. Classify every finding by scope, or as a redirect / combination input | C3, C4, C6, C12 |
| **S3** | **Decision-changing uncertainty** | The blocking set, the scope-blockers, any conflicted decision-critical value, and any provisional disqualifier §4 refuses to settle. Name the evidence needed, its expected form, and **the outcome each resolution would produce**. Owner, date and commitment are resolved **in the engagement** | all |
| **S4** | **Shape and ownership** | Whose problem is this, before what to build: source of record, integration ownership, existing estate, work shape, criticality class | C1, C2, C4, C5 |
| **S5** | **Material concern evaluation** | **Every serious option × every material concern**, at proportional depth. Absorbs the envelope analysis: documented limits **exclude designs, they never prove performance** | **C1–C12** |
| **S6** | **Composed disqualifiers** | Run the registered rows **explicitly**. A set of individually-conditional verdicts is **not** a pass. Resolve every combination input first. Then test **emergent** combinations (§10) | cross-concern |
| **S7** | **Operating and support requirements** | The operating **mechanisms** the chosen path needs: which role runs it, on which surface it is observed, which recovery mechanism at which objective, which release mechanism across a boundary, which skills the build requires. Recorded as **requirements and risks of the chosen path** — nothing here makes an option unavailable and nothing here blocks a decision (§6.1) | C7, C10 |
| **S8** | **Economics** | The **same ten cost dimensions** for **every surviving candidate**, on the same workload and operating model. An unfunded **mandated** control is infeasibility, not a trade-off | C11 (+ C6, C9, C10 consequences) |
| **S9** | **Comparative synthesis · comparator check · proof requirement** | Produce *(scope, outcome)* pairs from the closed set; run the four-part comparator separation (§13) **before writing any terminal sentence**; state and budget the proof requirement the commitment needs (§12) | all |

**The ten cost dimensions priced at S8**, identically for every candidate: audience · machine workload ·
data · security prerequisites *and the population they must cover* · environment and lifecycle ·
external estate · observability and support · build and change effort · existing sunk capability ·
exit and option value. **The cost of inaction is priced on the same dimensions** — doing nothing and
doing it manually are legitimate economic options and frequently the honest answer. Economics can
**reverse** a technical preference; it can never resurrect a disqualified option.

**Two standing rules that are not stages.**

- **Uncertainty re-check.** S3 is **re-run after S8**. Stages S5–S8 raise new uncertainty, and an
  unresolved decision-changing Unknown found at S8 blocks the decision exactly as one found at S3 does.
- **Reachability floor.** If the candidate set at S9 contains only forms of this platform, the procedure
  failed at S1 and must be re-run — **unless the platform is a declared imposed constraint**, in which
  case a set of compatible patterns inside that boundary is the correct result (§6.2).
  *Process change* and *do nothing / defer* are **conditional** members: S1 generates each where a
  requirement or a piece of evidence makes it plausible, and where it does not, S1 records why, with
  ids. Once generated, each is **never eliminated by a platform disqualifier** — only by its own
  evidence. The failure mode this guards against is the **silent** absence, not the reasoned one.

### 6.1 What may block a decision — the seven technical axes

**A decision is blocked only by an unresolved question on one of seven technical axes** (P-22):

1. **Data model, authority per entity and stable business key** — the entities, which store is authoritative for each, and the key that makes a write idempotent and repeatable.
2. **Audit-trail mechanism** — where the trail lives, whether it is independent of the write path, whether it carries a reason, and when its retention is stamped.
3. **Permission enforcement plane** — which plane imposes each role's access (row, column, API, application), whether it binds the administrator, and the sensitivity class and identity class that drive it.
4. **Environment, connector and licence-chain policy** — what the target environment permits, its residency and deployment model, the licence chain it creates, and the exception path.
5. **Integration mechanism and contract** — how each external system is reached, at what guarantee, payload, throughput and network boundary.
6. **Calculation-rule catalogue** — whether the rules to be implemented are known and separated from artefacts of the outgoing tool.
7. **Performance, concurrency and recovery envelope** — peak, concurrency, availability of the composed flow, and recovery objectives, **measured** rather than asserted.

Everything else is a **requirement or a risk of the chosen path**: operating model, support staffing,
team capacity, funding, organisational maturity, a third party's written position, who reviews, who
signs, who accepts. Those are recorded, carried into the decision record and into the implementation
spec, and priced at S8 where they cost money — but they never produce *decision blocked*, and they
never make an option unavailable. **S3's blocking set and S7 read this list**: a finding outside these
seven axes is a requirement, not a blocker. The reason is not optimism. An organisational gap recurs
identically on every candidate, so it separates nothing and decides nothing; a technical gap on one of
these axes changes which candidate survives.

### 6.2 A declared imposed technology is the boundary S1 generates inside

Where the engagement records the platform as a **fixed constraint** — a standing decision, a
framework agreement, an estate policy — S1 generates the candidate set **inside** that boundary:
the compatible patterns (simple · with automation · composed · permitted hybrid) and, where the
organisation permits the responsibility boundary, external components. The comparison is between
patterns, at the same rigour the procedure applies to any set.

**No candidate proposes changing platform, and no recommendation does.** The imposition is itself
an organisational rule, so a platform alternative may appear **only** as **class 15** — *viable if
the rule is changed* — carrying that class's seven fields. Costing and risking the alternative is
the honest way to show what the imposition buys and what it costs; presenting it as an ordinary
candidate is not, because nobody in the room can choose it.

The reachability floor above does not fire here: a set of one platform's forms is the correct
result of a constrained generation, not evidence that S1 failed.

---

## 7. Broad coverage, selective depth

> **Binding rule. Every *serious* option is considered against every *material* concern. Depth varies;
> coverage does not.**

### 7.1 What "serious" means

A candidate is serious unless it is (a) eliminated by a disqualifier at S2, S6 or S7, or (b) not
generated at S1 because no requirement triggers it. *Process change* and *do nothing / defer* are
serious **wherever they were generated** — and S1's reason for not generating one is itself a
recorded finding, never a silence. **A candidate eliminated at S2 still appears in the comparison with its disqualifier named** —
elimination is a finding, not a deletion.

### 7.2 Depth ladder (internal D0–D3)

The stage records which depth it used and why. A depth judgement is auditable; an omission is not.

| Depth | What it produces | When |
|---|---|---|
| **D0 — not material** | One line carrying an **affirmative rationale**: *"not material here — `<the engagement evidence that makes it so>`"* | The concern **has been considered** and available engagement evidence gives a defensible reason why it does not bear on this option or scope |
| **D1 — brief** | A stated verdict with its anchor; no analysis | Material but uncontested, low consequence, reversible, evidence current |
| **D2 — analysed** | Verdict + the mechanism + the trade-offs + what would change it | Material and consequential, or the evidence is `Assumed` / expired |
| **D3 — deep** | D2 + domain pull (§9) + the composed rows it feeds + the proof obligation + the uncertainty that would flip it | Decision-changing, or in the blocking set, or high-consequence and hard to reverse |

**D0 is a finding, not a default. Absence of evidence is never a D0 rationale.**

1. *"Nothing in the SU mentions offline"* does **not** justify D0 on C3's offline dimension. What
   justifies it is affirmative: *"every user works at a fixed workstation on the corporate network
   (`C-0NN`); no field or disconnected population exists in scope."*
2. Where the concern could plausibly be material and the evidence is missing, it is an **evidence gap,
   not D0**: record the concern at D1 with an `Unknown` carrying `custo` and `swing`. Existing
   materiality semantics then decide what happens — **most gaps are `dimensionante` or `cosmético` and
   are simply carried. Do not force every gap to become decision-blocking.** Only a `decisivo` swing, or
   membership of the blocking set **where the entry is engaged by the engagement**, escalates to
   *decision blocked* — presence in the register is not engagement
   (`decision-model/blocking-set.md` §0).
3. **D0 is auditable.** The concern-coverage line in `options.md` shows the rationale, so a reviewer can
   challenge it. An unexamined concern shows as neither D0 nor a gap — which is the defect §7.3 names.

**Depth drivers**, in the order they escalate: criticality class · decision-changing uncertainty ·
irreversibility · architectural consequence · cost consequence · risk · the gap between criticality and
demonstrated operational maturity. **Do not force D3 mechanically from a signal**; force it from
materiality.

### 7.3 The emergent-concern obligation

> A material concern raised by the Shared Understanding, the captured evidence, council reasoning or
> candidate-option analysis is evaluated at its proper depth **whether or not** it appears in
> `lenses_config.technology.constraints_to_check`, in the technology lens's signal catalog, **or in the
> twelve concerns above**.

Three sources of emergence, all real:

1. **Inside a concern.** A concern's boundary is its *question*, not an enumerated checklist.
2. **Between concerns.** Cross-domain interactions whose significance exists only in the pair (§10).
3. **Outside all twelve.** Possible and expected. A concern in this class is evaluated on **engagement
   evidence**, marked as having **no pack basis**, and recorded as an **authoring feedback item**. Do
   not invent platform certainty for it, and never suppress it for lacking an id.

**Silent omission is a defect.** If a concern is material and was not evaluated, the procedure produced
a wrong answer — regardless of whether any declared list mentioned it.

### 7.4 The declared constraints are a floor, never a ceiling

`lenses_config.technology.constraints_to_check` is a **standing-attention floor**: entries examined in
*every* engagement because their silent omission is a known failure mode. It is **not** the concern set
and **not** the coverage object. Adding entries to it does not widen coverage; §5 and §7.3 do.

### 7.5 What keeps this from becoming a 12×N matrix

D0 and D1 assessments are one line each. A five-candidate engagement at typical materiality produces
roughly sixty assessments of which most are one line. `options.md` carries a **twelve-line
concern-coverage summary**, never a proof-of-checking matrix (§14).

---

## 8. Stage-local registers

> **Decision registers are stage-local resources, not permanent Options context.**

This file is the **always-readable spine**. Everything else is consulted **only at the stage that needs
it**, and the procedure itself names which. **No preloading, and no router.**

| Stage | Register it consults | For |
|---|---|---|
| **S1** | `decision-model/alternatives-register.md` | The eleven option classes, the trigger→candidate map, the symmetry rules, the forbidden universals |
| **S3** | `decision-model/blocking-set.md` | The blocking entries and the scope-blockers, with their closure guidance |
| **S6** | `decision-model/composed-disqualifiers.md` | The registered composed rows and their reachable outcomes |
| **S9** | `decision-model/outcome-classes.md` | The closed outcome set, the render templates, the comparator separation |
| **any** | `decision-model/volatility-register.md` | **Only** where an active decision question depends on a volatile fact or a dated tripwire (§11). Never read as a standing checklist |
| S0, S2, S4, S5, S7, S8 | **none** | These run from this spine plus the Shared Understanding. S5 additionally pulls **domain knowledge** at D3 (§9) |

Two consequences worth stating. A register may be **re-consulted** at a later stage where a finding
sends the reasoning back to it — S9 legitimately re-reads the alternatives register for the candidate
list a terminal sentence must name. And a stage that consults nothing is not a stage doing less: **S5 is
the widest stage in the procedure and reads no register at all.**

---

## 9. Domain-knowledge pull rule

```text
candidate option  +  material concern  →  concrete decision question  →  pull the file that answers it
```

Pull because a question exists. **Never because a concern exists; never to be thorough.**

- **No preloading.** `aisa-options` must keep *"never place `decision-tree.md` or `domain-knowledge/`
  contents in the prompt — the architect pulls what it needs."*
- **No retrieval engine and no routing table** from concern to file. A routing table would be a second,
  silent coverage ceiling.
- **Depth gates the pull.** D0/D1 pull nothing. D2 pulls only where a boundary is contested. D3 pulls.
- **Cite what was used** — the file, the section or the SU row id; never a filename alone.
- **Selection logic never lives in domain knowledge.** Boundaries and mechanisms live there; *which
  option wins* lives here. Putting selection logic in a reference file is how this pack previously
  acquired invented thresholds.

---

## 10. Cross-domain and composed reasoning

Some concerns matter **only in combination**. Three mechanisms, and deliberately **no pairwise matrix**
— 66 mostly-empty cells that would still miss triples.

1. **Registered composed rows (S6).** Run explicitly from `decision-model/composed-disqualifiers.md`.
   Every one is invisible to per-concern reading. *A set of individually-conditional verdicts is not a
   pass.*
2. **Secondary consequence carriage.** A finding in one concern names where its consequence lands in
   another: security requirement → economics · data architecture → performance and cost · governance
   control → lifecycle and operations · user/offline requirement → data, security and support ·
   integration limitation → workaround and resilience · scale requirement → architecture and economics.
3. **Emergent combination test (S6, second half).** After the registered rows, ask one question: *do any
   two or more concerns, each individually acceptable, produce an unacceptable combination here?* An
   emergent combination is recorded as a `Risky` row with both anchors named and, where decisive, as a
   decision blocker. **It does not become a registered composed row merely because it occurred** —
   adding rows to make flags resolve would be invention.

---

## 11. Volatile-fact boundary

```text
stable decision principle   →  decision logic   (this file)
volatile platform fact      →  evidence         (domain knowledge + the engagement's own row)
```

1. **Encode the boundary shape, never the number.** *"Is the required freshness below the documented
   external-site floor?"* is decision logic. *"Is it below fifteen minutes?"* is a service limit
   disguised as a timeless rule. **This file contains no platform figure, and none may be added.**
2. **Read the figure at the decision date; record it with its date on the engagement's own row.** Kernel
   support exists: `verificado_em` + `validade`.
3. **No published figure is a state name.** Revalidating a limit changes one sentence, not a taxonomy.
4. **Verification obligation.** Where a volatile fact is decision-critical and sufficiently current
   evidence is unavailable, create a verification obligation: an `Unknown` (`custo: documento|spike`,
   `swing: decisivo`) whose `quem responde` carries the role that owes it or the source to consult
   (`role:` / `fonte:`, never a person), plus the date, and the affected conclusion is **not treated as
   settled**. Where the fact is in the blocking set, the terminal is *decision blocked*.

`decision-model/volatility-register.md` carries the entries, their re-verification triggers, the live
conflict and the dated tripwires that feed `/decide`'s revision conditions and `/revisit`. It is
consulted per §8, never loaded as a checklist.

---

## 12. Proof requirement — the four validation levels

S9 states **and budgets** what evidence the commitment requires. This is the Discovery vocabulary term
**proof requirement** (`glossary.md` A5) used unchanged in Options — one word, not two.

| Level | What it is | Typically required by |
|---|---|---|
| **V1** | Published-limit arithmetic against the documented envelope | Low criticality, uncontested envelope, reversible commitment |
| **V2** | A bounded pilot on representative work | A contested envelope, a new mechanism, an unmeasured amplification |
| **V3** | An engineered test harness | A commitment resting on sustained throughput, concurrency or ordering behaviour |
| **V4** | A production-like proof at managed-environment fidelity | A criticality or recovery commitment that must be evidenced, not asserted |

**Documented limits exclude designs; they never prove performance.** A level that is stated but not
funded is a precondition, not a plan — name its cost and the mechanism it requires.

---

## 13. Comparator discipline

Before writing **any** terminal sentence, separate four statements and never collapse them:

1. **Exclusion** — is this platform excluded, and **at which scope**? (In-platform redirects and
   unresolved combination inputs never enter this step.)
2. **Candidate generation** — which option classes come into scope?
3. **Comparative evaluation** — what does the evidence actually say about those classes, or
   **`COMPARATOR EVIDENCE ABSENT`**?
4. **Preference** — permitted **only** where step 3 returned a signal that discriminates between the
   candidates.

Steps 1 and 2 are almost always available. Step 3 is available on a minority of questions. **Step 4 is
available on the deployment-model axis alone.**

**Forbidden output.** Do not emit *better*, *cheaper*, *faster*, *easier*, *more scalable* or *lower
TCO* about any class without actual comparative evidence — in either direction. *"Custom development is
more expensive"* and *"low-code is faster"* are both prohibited. **Being able to exclude this platform
does not prove the replacement is superior.** Candidate generation and comparator evaluation are
distinct steps, and `COMPARATOR EVIDENCE ABSENT` is **part of the outcome sentence, not a footnote**.

**The gates cut both ways, and the output must say so.** The S7 capability gates make *custom*,
*cloud-native* and *hybrid* classes unavailable more often than they do this platform — that is a
documented capability gap in those classes, **not an advantage of this platform** — while classes with
an existing funded operator gain a candidate signal on the same criteria. State both halves.

---

## 14. Outcome and render handoff

S9 emits **one outcome per scope**, drawn from the **closed set** in
`decision-model/outcome-classes.md`. **Any label not in that set is a defect in the emitter, not a new
class.**

### 14.1 What the architect returns per option

Plain language, no internal codes: option name and **option class** · **form, where the class is
this platform** · scope · viability
(viable / viable with preconditions / **viable if the rule is changed** / disqualified — settled /
disqualified — provisional, naming the assumption / not assessable) · the outcome in its render
template · **high-level architecture** (the main components, and per component whether it falls
inside or outside the responsibility boundary) · **assumptions** · **order of magnitude with its
source** · material strengths · disqualifiers with their scope and **evidence grade** ·
preconditions (condition — **role or source, never a person** — funded? — by when) ·
material trade-offs · material risks · **cost drivers** · **reversibility** · **revision
condition** · decision-changing uncertainties (what they would change, and the cost to close) ·
the proof requirement · concern notes **only where decision-relevant**. `(none)` is written
explicitly — an empty field is indistinguishable from an unevaluated one.

**The order of magnitude declares where it came from, or declares itself unavailable.** One of
three sources, named on the line: the band `/simulate` projected · the pack's estimation model
applied to the option's shape at pre-blueprint granularity · a named analogy with a prior
engagement. With none of them the field reads *unavailable*, with what is missing to produce it.
It is a band, never a point. The method and its four verbatim markers are owned by
`.claude/skills/chairman-synthesis/SKILL.md` and are not restated here.

**High level means high level.** Enough to compare: the components and the responsibility
boundary. The detailed architecture — field-level data dictionary, per-screen actions, permission
matrix, integration contracts — is produced for the **chosen** option only, at `/blueprint`,
after the decision.

**The form is mandatory for a platform candidate, and it is named in products.** A platform
option's form is a *surface × store* pair from `decision-model/alternatives-register.md` §1.2 —
the record-centric app over the governed store, the canvas app over the external relational store,
the code app, the team-hosted app, and so on. **One option per form**: two forms differing in
surface or in store are two candidates, each with its own verdict, effort profile and
reversibility. An option returned as *"this platform"*, or as *"this platform over the store that
already runs"*, is **malformed** — the phase exists to put the named choice on the table, and the
store half alone withholds the surface the sponsor has to live with. Naming the form is **not** a
verdict about it (§0 of that register) and **never** an architecture decision: the architecture is
designed after the decision, at `/blueprint`.

### 14.2 What the round carries

Summary · **concern coverage** (one line per concern: the depth used, or *"not material — why"*) ·
**class coverage** (one line each for *do nothing* and *process change*: the candidate that carries
it, or why it is not plausible, with ids) · the per-option comparison · **the reasoned
recommendation** — the option, what separates it from its siblings, the assumptions holding it up,
what would flip it, and the terminal reached (preferred / conditionally preferred / multiple
defensible / decision blocked / no intervention justified); where the terminal is *decision blocked*
or *multiple defensible*, `no recommendation` with what would produce one · **comparator status**
per non-platform candidate.

**The recommendation is not the decision.** It is the procedure's reasoned reading, written so the
owner can disagree with it on the evidence. The choice, and the authority for it, are the owner's
at `/decide`.

### 14.3 Internal vocabulary stays internal

Never rendered as engagement vocabulary: exit-scope codes · redirect and combination-input codes ·
depth codes `D0`–`D3` · outcome class **numbers** · outcome subtype codes · register ids of any kind ·
scope-pair mechanics as jargon. The plain-language renderings are in §3, §7.2 and the outcome register.
The shared Options vocabulary a participant may legitimately meet is in `glossary.md` Part C.

**This is not a product-naming ban, and reading it as one is a defect.** *Internal* means the
framework's own machinery — the codes, the numbers, the register ids, the stage names. **Vendor and
product names are mandatory here**: Options is the one phase that may name them (`glossary.md` Part B
gate), and §14.1 requires the platform candidate's **form** to be named in products. Rendering a
candidate as *"this platform"* or *"this platform over the store that already runs"* is not plain
language — it is the option withholding its own identity. Plain language governs the *framework's*
vocabulary; the *product's* vocabulary is the content.

### 14.4 Downstream

`chairman-synthesis` writes `options.md` from §14.1/§14.2. `/simulate` consumes the same structure to
project each option and to list the uncertainties that would flip the ranking. `/premortem` and
`/decide` consume the risks, preconditions and tripwires. Nothing here renders a deliverable — that is
`/synthesize` → `/render`.
