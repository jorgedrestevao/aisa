# Step 4A — Domain Knowledge Runtime Model and Re-taxonomy (design)

<!--
provenance: AUTHORING REPORT
date: 2026-09-04
scope: PP PACK AUTHORING — STEP 4A. Design and mapping only. No runtime file created, modified or deleted.
read (not reopened, not modified): pp-pack-authoring-map.md §3.4, §7, §8, §11, §12 ·
    step-3a-options-decision-model.md (final) · step-3b1-options-runtime-implementation-report.md ·
    step-3b2-options-runtime-gate-report.md (FROZEN) · library/packs/pp/decision-tree.md ·
    the five decision-model registers · pack.yaml · library/packs/pp/domain-knowledge/* (13 files) ·
    canonical Areas 1-12 + Block D as canonicalised (canonical-manifest.md §3, §5, §6, §7, §11-§13)
no research reopened · no web access · no canonical file modified · no PP runtime file modified
path note: `research/pp/authoring/` resolves to `docs/pp-pack-authoring/research/pp/authoring/`
-->

---

## 1. Purpose and doctrine

Design the domain-knowledge layer so a reasoner with a **concrete decision question** can go deep enough
to answer it defensibly, without the canonical corpus becoming permanent runtime context.

**Binding doctrine, inherited and not re-litigated:**

| # | Principle | Consequence in Step 4 |
|---|---|---|
| 1 | Evidence-heavy authoring, evidence-light runtime | The corpus (≈2.9 MB canonical) is the authoring authority. Runtime carries the answer shape, not the evidence trail |
| 2 | Light framework, not lightweight reasoning | Fewer, sharper pull targets. Depth inside a unit is not capped |
| 3 | Compress repetition, not decision coverage | The triple-stated delegation tables collapse; no decision question loses its home |
| 4 | Broad coverage, selective depth | Every material concern has a pull target; one question pulls one unit |
| 5 | Minimum sufficient complexity | Split only where unrelated questions would otherwise load together |
| 6 | Domain knowledge deepens a concrete decision question | Pull-based. No preload, no router, no per-concern bundle |
| 7 | Research completeness is authoring input, not runtime payload | Coverage is *accounted for*, not *copied* |
| 8 | Pull-based expertise, not a technology encyclopedia | A file exists because it answers a recurring material question |

**The dependency, never reversed:**

```text
decision model      → decides what question needs answering
domain knowledge    → provides the technical knowledge needed to answer it
```

**Step 3 is frozen.** Option-class generation, stage ordering, exit semantics, D0–D3 mechanics, blocking
logic, outcome selection, comparator semantics, recommendation semantics, preference rules and
composed-row orchestration stay in `decision-tree.md` + `decision-model/`. Nothing in this design moves
any of them into `domain-knowledge/`, and nothing here lets a domain file say which option wins.

**Doctrine 9, added 2026-09-10 (refoco em decisão técnica, fase 3).** *A knowledge unit describes
mechanisms as design objects; a person is never one of them.* What a unit may state about running a
design is the **role** that acts, the **identity** it acts as, the **permission** that identity needs,
the **mechanism** that detects the condition, the **alert destination**, and the **recovery procedure**.
Where a design has not defined them, the unit states a **requirement with a cost** — never
*"therefore unavailable"*, never *"therefore deferred"*, never a maturity grade that activates a package
by label. Two sentences a unit may not write, in any pack: *"no operator, therefore unavailable"* and
*"immature, therefore deferred"*. Both are selection verdicts (Doctrine 6 and README §6) and both rest on
a fact about the organisation rather than about the design. Preserved, because they are technical: the
artefact **owner** as a runtime dependency (throughput, suspension, licensing), data authority and
provenance, and the retention obligations a rule in scope imposes.

---

## 2. Current domain-knowledge inventory

13 files · 4,000 lines · ≈156 KB · flat namespace · zero provenance · zero volatility stamping.

| # | File | Lines | Subject | What it is today | Runtime usefulness | Plausible concrete pull question | Verdict |
|---:|---|---:|---|---|---|---|---|
| 1 | `powerfx-patterns.md` | 566 | Power Fx craft + delegation | Delegation tables · workarounds · 5+4 validation sequence · 8 traps · standard patterns · context-variable conventions | **High** for build/blueprint. Low for Options — a formula pattern never decides viability | *"What is the delegation-safe form of this access path, and how do I validate the emitted formula?"* | **SPLIT** → platform boundary to `data/query-and-delegation.md`; craft to `craft/powerfx.md` |
| 2 | `flows-patterns.md` | 514 | Power Automate | Connector reference · complexity tiers · error-handling patterns · 3 flow templates · reporting-integration patterns · expression catalogue · adaptive card · child-flow contract | **Mixed.** The decision-bearing automation evidence (shapes, meters, run limits, idempotency, retry semantics) is **absent**; what is present is build craft | *"Which automation mechanism carries this work shape, and what fails first?"* — the file **cannot answer it today** | **SPLIT + REWRITE** → `automation/automation-mechanisms.md` (new) + `craft/flow-craft.md` |
| 3 | `azure-sql-reference.md` | 554 | Azure SQL | Types · mandatory audit columns · medallion · SP wrapper template · DAG · views · RLS · T-SQL finance · CTE/MERGE/temporal · index strategy · connector actions | **Mixed.** ~15 % is store-choice evidence; ~85 % is the team's SQL build convention presented as platform reference | *"What is the connector envelope and tier boundary of a SQL store on this path?"* | **SPLIT** → `data/azure-sql.md` + `craft/sql-delivery-conventions.md` |
| 4 | `dataverse-reference.md` | 437 | Dataverse | Types · reserved names · flags · relationships · calc tiers · business rules · views · roles · column security · alternate keys · perf limits · plugin matrix · rollups · solution layering · **licence-price table** · anti-patterns · schema-rigor matrix | **Mixed.** Predates the corpus; limits carry no date or source; quotes prices | *"What transactional and authorization semantics does this store provide, and which decisions here are irreversible?"* | **REWRITE** → `data/dataverse.md`; schema-rigor matrix → craft; price table **deleted** |
| 5 | `sharepoint-reference.md` | 379 | SharePoint | Column types · hard limits · calculated functions · indexing · groups · no-CLS/no-RLS workarounds · validation formulas · perf rules · delegation · OData · 5K view strategy · growth planning | **Mixed.** Canonical figures present but undated; l.42 **restates the deleted R0 disqualification gates** and their invented numbers | *"What does this store not enforce, and what is its documented ceiling?"* | **REWRITE** → `data/sharepoint.md`; gate restatement **deleted** |
| 6 | `security-patterns.md` | 392 | Security | Role inference signals · 4 permission matrices · conflict resolution · Power Fx security blocks · role/CSP formats · SP groups · SQL RLS views · audit columns | **Craft, mislabelled.** Organised by artefact; the corpus organises security by **enforcement plane**, and the plane decides which lever moves. No plane model, no trust boundary, no egress, no key custody | *"Is the mandated control available at all, on which plane is it enforced, and for what population?"* — **cannot answer today** | **SPLIT + REWRITE** → `security/security-controls.md` (new) + `craft/security-craft.md` |
| 7 | `screen-patterns.md` | 269 | UX craft | 5 screen types · status palette · density · approval state machine · navigation · journey · validation UX · layout · states · tabs · responsive · caps · per-screen spec template | **High** for blueprint/design-brief. **Zero** for Options | *"What screen shape does this record-and-approval flow take?"* | **KEEP** → `craft/screen-patterns.md` |
| 8 | `estimation-model.md` | 260 | Effort / cost | Effort tables · multipliers · 20 % buffer · phases · overlap · team composition · standard risk register · output format · quick-win criteria · **licence price table** · worked example · anti-patterns · uncertainty handling | **High** for `/simulate` and `estimate`. **Hazardous at Options** — platform-only effort bands with no comparator basis create asymmetric preference | *"What effort band does this component inventory imply for a platform build?"* | **KEEP + partial DEPRECATE** → `craft/estimation-model.md`; prices **deleted**; barred from S8 |
| 9 | `anonymization.md` | 205 | Test data | 11 sensitivity types · methods · synthetic-value patterns · anonymisation log | **Moderate**, narrow, self-contained. Outside corpus scope entirely | *"How do we produce a non-production dataset for this sensitive entity?"* | **KEEP** → `craft/anonymization.md` |
| 10 | `excel-patterns.md` | 203 | Translation | Excel → Power Fx / T-SQL catalogue incl. the financial-function gap | **Moderate.** Consumed by `/capture` and Options translation work | *"Does this spreadsheet formula have a platform equivalent?"* | **KEEP** → `craft/excel-translation.md` |
| 11 | `delegation-matrix.md` | 77 | Delegation | Two delegable-operation tables · decision implications · workarounds | **High**, but **wholly duplicated** by `powerfx-patterns.md` §1–§2 and partly by `sharepoint-reference.md` §DELEGATION | *"Is this operation delegable on this connector?"* | **MERGE** → `data/query-and-delegation.md` |
| 12 | `screen-consolidation-rules.md` | 76 | Blueprint | Field-count → screen-type tree · naming · hard caps | **High.** The **named contract** of `library/kernel/blueprint-contract.md` | *"How many screens, of which types, does this field and role inventory produce?"* | **KEEP (filename)** → `craft/screen-consolidation-rules.md` |
| 13 | `delivery-conventions.md` | 62 | Delivery | Naming · `su:` traceability stamping · environments/ALM · security/data · go-live · post-go-live | **Moderate.** Explicitly `TODO(team)` defaults | *"What do we name this artefact and what must be true before go-live?"* | **UPDATE + RETAXONOMIZE** → `craft/delivery-conventions.md` |

**Tally.** KEEP 4 · KEEP + partial DEPRECATE 1 · SPLIT 3 · SPLIT + REWRITE 1 · REWRITE 2 · MERGE 1 ·
UPDATE + RETAXONOMIZE 1. **RETIRE outright: 0** — every file has salvageable content. What is retired is
*framing*, *duplication* and *specific numbers*.

---

## 3. Current defects and duplication

### 3.1 Decision logic living in domain knowledge — the load-bearing defect

| Evidence | Nature | Consequence |
|---|---|---|
| `azure-sql-reference.md` l.7 declares an **architecture branch** (`azure-sql-first`) the decision tree never had | Domain knowledge inventing an option | Already a **live engagement defect**: `projects/pricing-marinha/shared-understanding.md` **X-029** records the architect finding no branch in the pack's tree while a *reference file* declared one — and proceeding on the reference file's authority |
| `sharepoint-reference.md` l.42 restates the **deleted R0 gates** and their invented numbers (`>30,000` rows, `formula_count > 100`) as *"hard limits driving the disqualification gates"* | Domain knowledge asserting exclusions | `AP-D-051`, enforcement class **CONSTRAINT** — always wrong within scope. Step 3 deleted these from the spine; they survive here |
| `sharepoint-reference.md` l.133 — *"makes SharePoint inappropriate for entities with strong column-level access requirements"* | Comparative verdict | A capability absence is domain knowledge; *inappropriate* is a selection verdict |
| `dataverse-reference.md` § BUSINESS RULE vs POWER FX vs PLUGIN vs POWER AUTOMATE — **Decision Matrix** | Verdict grid | In-platform mechanism choice is legitimate architecture knowledge, but it must read as capability boundaries, not as a verdict grid |
| `screen-consolidation-rules.md` l.8 — *"apply after the architectural branch is chosen (sharepoint-first, dataverse-first, hybrid)"* | Dead vocabulary | The three-branch option space no longer exists |
| `delegation-matrix.md` § Decision implications | Verdicts per branch | Same |

The three obsolete branch names appear in **4 of 13 files**. They are the residue of the model Step 3 replaced.

### 3.2 Duplication

| Behaviour | Stated in | Divergence already present |
|---|---|---|
| Delegable-operation tables (two connectors) | `delegation-matrix.md`, `powerfx-patterns.md` §1.1–§1.2, `sharepoint-reference.md` §DELEGATION | **Three copies.** `powerfx` says *"limited to 500 records"*; `delegation-matrix` says *"default 500, max 2000"* |
| Delegation workarounds | `delegation-matrix.md`, `powerfx-patterns.md` §2, `sharepoint-reference.md` §Workaround patterns | Three copies |
| Audit-trail obligation and pattern | `security-patterns.md`, `powerfx-patterns.md` §5.5, `azure-sql-reference.md`, `flows-patterns.md`, `delivery-conventions.md` | Five touchpoints, no owner |
| RBAC / role modelling | `security-patterns.md`, `dataverse-reference.md` §SECURITY ROLES + §COLUMN SECURITY, `sharepoint-reference.md` §GROUPS, `azure-sql-reference.md` §RLS | Four store-local copies of one subject, with no plane model to reconcile them |
| Reporting integration | `flows-patterns.md` §POWER BI + constraints inside the store files | No owner |

### 3.3 Volatile facts presented as stable

**Zero** files carry `verificado_em`, `validade`, a re-verify trigger or a source date. Every service
limit, retention window, quota and entitlement statement in the layer reads as timeless.
`estimation-model.md`'s header line *"refresh on each major release wave"* is the layer's only
acknowledgement of decay, and it is prose, not a stamp.

### 3.4 Prices in the pack

`licensing-cost.md` §12 is explicit — the pack must never quote a price. Two files do:
`estimation-model.md` § LICENSE COST ESTIMATES (six per-user figures + two tier prices) and
`dataverse-reference.md` § LICENSING IMPACT ON ARCHITECTURE (a per-user and per-app price row).

### 3.5 Material knowledge absent

No file in the layer can answer a question about: the four automation shapes · the five metering systems ·
idempotency and retry duplication · the five security enforcement planes · trust boundary, egress or key
custody · the eight governance levers · managed environments and their licence chain · the four-rung ALM
ladder · no-rollback · environment topology · the five economic mechanisms and their meters · the four
operational maturity classes · monitoring and telemetry limits · backup ≠ recovery · integration mechanism
envelopes · network boundary (private-network paths and gateways) · identity propagation · the ten
architecture patterns.

**Every one of those is a D3 pull target the frozen Step 3 spine assumes exists.** This is the layer's
largest defect — larger than the duplication.

### 3.6 Craft indistinguishable from research

`azure-sql-reference.md` presents a medallion architecture, a stored-procedure wrapper and an
index-maintenance policy as *"authoritative reference"*. They are team conventions, entirely outside the
corpus, and are read at build time as platform truth. `security-patterns.md` and `estimation-model.md`
share the problem. Keeping craft is right; labelling it is missing.

### 3.7 Implementation trivia sharing a namespace with decision knowledge

T-SQL reserved-word list · control-property reference · adaptive-card JSON · status hex codes ·
notification timeout constants · GUID pool patterns. All legitimate build content; none of it belongs in a
namespace an Options reasoner is invited to pull from.

---

## 4. Domain-knowledge runtime contract

### 4.1 The job

Domain knowledge answers **"what is true about this mechanism, boundary or control?"**
It never answers **"which option should win?"**

### 4.2 The knowledge-unit shape

Two mandatory elements, then a flexible body. Not a rigid template — the subject decides which headings
earn their place.

**Mandatory — §0 `When to pull this file`.** Two to four **concrete decision questions**, phrased as the
reasoner would phrase them. This block plus the filename *is* the discoverability mechanism; there is
nothing else, and nothing else is needed (§19).

**Mandatory — the boundary line.** One sentence: *"This file states X. It does not decide Y — that is
`decision-tree.md` S-N."*

**Flexible body**, in this order, omitting what does not apply:

| | Heading | Content |
|---|---|---|
| A | What this is for | One paragraph of orientation. Never a product tour |
| B | When it becomes material | The requirement shapes that make this domain bear on a decision |
| C | Durable principles | Stable architecture and engineering truths that outlive a release |
| D | Important boundaries | What the mechanism can and cannot defensibly support |
| E | Decision-sensitive distinctions | Differences whose misunderstanding changes architecture or viability — delegable ≠ fast · backup ≠ recovery · documented limit ≠ measured performance · available ≠ enforced on the required plane · platform availability ≠ end-to-end availability |
| F | Failure modes | Only material ones, one to three lines each. Never an anti-pattern encyclopedia (§11) |
| G | Consequences elsewhere | Named cross-domain landings. This is how cross-domain coverage is carried without a matrix file (§17) |
| H | What must be verified | Volatile or environment-specific facts, each naming its `volatility-register` row |
| I | What not to infer | The invalid conclusions this subject invites |

### 4.3 Grade marking inside the unit

Every section carries one of `decision` · `architecture` · `implementation` (§6). **Decision-grade sections
come first.** A D3 pull reads the decision-grade sections and is not obliged to read further — the file's
ordering makes selective depth possible *inside* a file, not only across files.

### 4.4 Retrieval behaviour — binding

```text
concrete material question
  → pull ONE relevant knowledge unit
  → deepen
  → pull another ONLY if the first exposes a second material dependency
```

Forbidden, restating `decision-tree.md` §9 and `aisa-options`:

- `C4 is material` → load every data file. **No.**
- Options starts → preload `domain-knowledge/*`. **No.**
- A router, scoring index, embedding requirement, mandatory multi-file bundle, or per-concern preload map. **None.**
- **D0/D1 pull nothing · D2 pulls only where a boundary is contested · D3 pulls.**
- Cite the file **and the section** — never a filename alone.
- **`craft/` is never a D3 pull target.**

### 4.5 What the layer may never contain

Option-class generation · stage order · exit classes · outcome selection · blocking logic · composed rows ·
comparator or preference semantics · a fit score · an ordinal fit ladder · an architecture "branch" · a
price · a threshold presented as a rule · a comparative claim about an unevaluated alternative.

---

## 5. Stable vs volatile boundary

### 5.1 Single owner per responsibility — no competing sources of truth

| Responsibility | Owner | Never owned by |
|---|---|---|
| The **boundary question** in decision logic (*"is the required freshness below the documented external-site floor?"*) | `decision-tree.md` §11 | domain knowledge |
| The **stable explanation** — what the mechanism is, why the boundary exists, what it excludes, what it cannot prove | **the domain-knowledge unit** | the volatility register |
| **That a fact is volatile, and when to re-verify it** | `decision-model/volatility-register.md` (`VC-01…10`, `VS-01…20`, 3 tripwires) | domain knowledge |
| The **current factual value** used for a decision, with its date | the engagement's own SU row (`verificado_em` + `validade`) | any pack layer |

The Step 3 register states it in its own §5: *"It does not supply figures."* Step 4 does not change that
and does not copy the register into domain knowledge.

### 5.2 When a domain unit may carry a number

Numbers are **not forbidden**. A decision-relevant quantitative boundary is retained. What is mandatory is
that volatility becomes explicit.

A unit may carry a documented figure only when **all four** hold:

1. The figure is decision-relevant — the boundary *shape* alone cannot be tested against a real requirement.
2. It is stamped as a reading, not a rule: `documented reading · read <YYYY-MM-DD>`.
3. It names the volatility-register row owning its re-verify trigger (e.g. `re-verify: VS-04`).
4. It reads as **exclusion evidence with a shelf life** — never as a threshold rule, never as a state name.

**Two absolute prohibitions.**

- **A `CONFLICTED` figure is never carried, on either side.** The per-mechanism throughput ceiling
  (`20×` disagreement · `VC-01`/`VS-08` · blocking entry `B-08`) appears as *"conflicted — decision-blocked
  until measured"*, never as a number.
- **No price, ever.** Units, drivers, ratios and meters; no currency, no SKU, no tier price.

### 5.3 Classification of every content class

| Class | Examples | Home and treatment |
|---|---|---|
| **Stable principle** | A hard limit can exclude a design but cannot prove end-to-end performance · a security requirement must be satisfied on the lowest plane that can enforce it · retry duplicates non-idempotent effects · a backup existing ≠ recovery being possible · pooled storage is consumed by things nobody budgeted | Domain knowledge, unstamped |
| **Stable structural fact** | Five independent metering systems · four automation shapes distinguished by where state lives and what the unit of failure is · four ALM rungs · five security planes · eight governance levers · five economic mechanisms · four operational maturity classes | Domain knowledge, unstamped |
| **Documented reading** | List-view threshold · delegation default and maximum · payload ceilings · run-duration ceiling · retention windows · gateway host minimum · batch ceiling | Domain knowledge, **stamped** per §5.2; trigger owned by the register |
| **Commercial fact** | Entitlement rules · what a control obliges licence-wise · capacity assignability · metering units | Domain knowledge carries the **shape** (*"this control requires a managed environment, and every active user of that environment then requires a premium licence"*); the **date, enforcement state and price** belong to the register and the engagement row |
| **Feature state** | Preview / GA · connector classification · regional availability | Never asserted. Stated as *"verify current state"*, naming `VC-10` / `VS-20` |
| **Conflicted** | Custom-connector throughput | Rendered as the conflict, never as a value |

---

## 6. Decision-grade / architecture-grade / implementation-grade boundary

| Grade | Question it serves | Consumer | Rule |
|---|---|---|---|
| **Decision-grade** | Viability · option class · major trade-off · major control · economics · proof obligation | Options (D3 pull), `/simulate` | First in the file. Readable without the rest |
| **Architecture-grade** | How the mechanism composes once the option class is established | `/blueprint`, `solution-blueprint`, architecture templates (Step 5) | Second in the file |
| **Implementation-grade** | How to build it | `implementation-spec`, `claude-design-brief` | Last in the file, **or delegated to `craft/`** |

**Binding consequence: Options never reads implementation-grade content merely because it exists.**
Where a subject's implementation body is large it moves to `craft/` rather than sitting at the bottom of a
research file. That is the mechanism by which `powerfx-patterns.md` (566 lines, ~90 % build craft) stops
being reachable from an Options pull while `data/query-and-delegation.md` stays reachable.

**Grade map** (`●●` primary · `●` present · `—` absent):

| Unit | decision | architecture | implementation |
|---|:--:|:--:|:--:|
| `application/application-surfaces.md` | ●● | ● | — |
| `data/store-boundaries.md` | ●● | ● | — |
| `data/dataverse.md` | ● | ●● | ● |
| `data/sharepoint.md` | ● | ●● | ● |
| `data/azure-sql.md` | ● | ● | — |
| `data/query-and-delegation.md` | ●● | ● | ● |
| `automation/automation-mechanisms.md` | ●● | ● | — |
| `integration/integration-mechanisms.md` | ●● | ● | — |
| `security/security-controls.md` | ●● | ● | — |
| `governance/governance-and-environments.md` | ●● | ● | — |
| `alm/release-and-lifecycle.md` | ●● | ● | — |
| `performance/performance-and-scale.md` | ●● | ● | — |
| `economics/licensing-and-cost-drivers.md` | ●● | — | — |
| `operations/operability-and-support.md` | ●● | ● | — |
| `architecture/patterns.md` | ● | ●● | — |
| `craft/*` (10) | **never** | ● | ●● |

---

## 7. Proposed taxonomy

### 7.1 Tree

```text
library/packs/pp/domain-knowledge/
├── README.md                                  # the pull rule, the grade convention, the boundary line
├── application/
│   └── application-surfaces.md
├── data/
│   ├── store-boundaries.md
│   ├── dataverse.md
│   ├── sharepoint.md
│   ├── azure-sql.md
│   └── query-and-delegation.md
├── automation/
│   └── automation-mechanisms.md
├── integration/
│   └── integration-mechanisms.md
├── security/
│   └── security-controls.md
├── governance/
│   └── governance-and-environments.md
├── alm/
│   └── release-and-lifecycle.md
├── performance/
│   └── performance-and-scale.md
├── economics/
│   └── licensing-and-cost-drivers.md
├── operations/
│   └── operability-and-support.md
├── architecture/
│   └── patterns.md
└── craft/
    ├── powerfx.md
    ├── screen-patterns.md
    ├── screen-consolidation-rules.md
    ├── excel-translation.md
    ├── flow-craft.md
    ├── security-craft.md
    ├── sql-delivery-conventions.md
    ├── anonymization.md
    ├── estimation-model.md
    └── delivery-conventions.md
```

**15 RESEARCH units · 10 CRAFT units · 1 README = 26 files (25 knowledge units).**

### 7.2 Per-file specification — RESEARCH units

| File | Scope | Primary pull questions | Concerns | Stable / volatile mix | Replaces / absorbs | Canonical families | Downstream consumer |
|---|---|---|---|---|---|---|---|
| `application/application-surfaces.md` | Which surface can carry which experience, and each surface's documented boundary: configure/buy/first-party (rung 0), canvas, model-driven, custom pages, external-audience sites (both build models), code apps, team-hosted, embedded surfaces, branded native wrap, hybrid-with-cloud, custom development. Offline depth, device capability, accessibility regime, localisation and RTL, deep links, distribution | *Can this surface deliver the required interaction, identity class, offline behaviour and accessibility?* · *Is this requirement already met by a first-party app or a capability the organisation owns?* · *What does choosing this surface forfeit?* | C1, C2, C3, C12 | Stable structure; **volatile**: preview/GA banner states, modern controls, code-apps state, team-scoped store limits | — (new) | Area 2 §1–§3.7, §4, §9, §10; Area 1 §2 rows 1–19 | Options (C3 D3), `/blueprint`, `solution-blueprint`, `claude-design-brief` |
| `data/store-boundaries.md` | The cross-store capability map: per observable data requirement (authority, relational depth, integrity, atomicity span, granularity, queried volume, concurrency, attachments, retention, residency, operational vs analytical) what each store can and cannot defensibly support. Carries the replication / virtualization boundary and the obligations replication imports | *Which available store can satisfy this authority + integrity + query-shape requirement?* · *Does the reporting need force a second store, and what does that oblige?* | C4, C9, C11 | Stable dimensions; **volatile**: the ceilings quoted per store | Comparative fragments of the three current store references | Area 3 §2, §3, §6 | Options (C4 D3), `solution-architect`, `/simulate` |
| `data/dataverse.md` | Modelling and relationship semantics; ownership-type immutability and the other irreversible provisioning decisions; alternate keys; transactional scope (change set / plug-in / custom API); authorization grain (unit, team, row, column, masking); audit and long-term retention; capacity model and borrowing; virtual tables and what they forfeit; calculated and rollup boundaries; the extension-mechanism boundary | *What transactional and authorization semantics does this store provide?* · *Which decisions here cannot be undone after provisioning?* · *What does enabling audit cost in capacity?* | C4, C6, C9, C11 | Stable semantics; **volatile**: capacity ratios, retention windows, rollup and calculation limits | `dataverse-reference.md` (research half) | Area 3 §4.2, §4.7 (`DV:*`, `VT:*`) | Options (C4/C6 D3), `implementation-spec`, `claude-design-brief` |
| `data/sharepoint.md` | List and library store: documented ceilings; what it does **not** enforce (no column-level security, no native row-level edit security); indexing and view mechanics; calculated-column boundary; attachment and binary handling; the documented shapes for which it is the correct answer; the graduation trigger when it stops being so | *What does this store not enforce, and what is its documented ceiling on this access path?* · *Is this one of the shapes for which it is the documented answer?* | C4, C6, C3 | Stable absences; **volatile**: view threshold, item ceiling, join limit, call rate | `sharepoint-reference.md` (research half) | Area 3 §4.4 (`SP:S-*`), `DA-39`, `DA-40`, `DA-44` | Options (C4/C6 D3), `implementation-spec` |
| `data/azure-sql.md` | Relational store reached by connector: tier and log-rate envelope; connector call and concurrency envelope; identity model through the connector; row-level-security-through-connector semantics; cold-storage absence; what moves outside platform governance with the store | *What is the connector envelope and identity model when the store sits outside the platform?* · *What does putting the store here move out of platform governance?* | C4, C5, C6, C7, C10 | Stable structure; **volatile**: tier capabilities, connector call limits | `azure-sql-reference.md` (research ~15 %) | Area 3 §4.3, §4.9 (`SQ:*`, `SQ2:*`) | Options (C4 D3), `implementation-spec` |
| `data/query-and-delegation.md` | The corpus's most-collapsed distinction: **delegation-safe (correctness) vs fast (latency)**. Per-connector delegable-operation behaviour; silent-truncation semantics; client cache boundary; access-path design consequences | *Is this access path delegation-safe — and does delegation-safe also mean fast enough here?* · *What silently truncates?* | C4, C2, C9 | Stable principle; **volatile**: cache default and maximum, per-connector delegable sets | `delegation-matrix.md` (whole) + `powerfx-patterns.md` §1–§2 + `sharepoint-reference.md` §DELEGATION — **three copies collapse to one** | `DA-02`, `PS-13`, `PF-01`, Area 9 §5.4, `AP-D-050` | Options (C4 D3), `/simulate`, `/blueprint`, `claude-design-brief`, `craft/powerfx.md` |
| `automation/automation-mechanisms.md` | The four automation shapes and the ordered classification test (what holds state · what the unit of failure is); mechanism envelopes and what each fails first on; the three independent meters; run-duration, action-count, nesting and array boundaries; human-wait semantics; **idempotency and the retry-duplication rule**; ordering and dedup; human-in-the-loop and approval semantics; interface-automation boundaries; the corrected myths the pack must actively teach | *Which mechanism carries this work shape, and what fails first?* · *What happens on retry, and what must the design guarantee?* · *Can this wait survive a deployment or a version change?* | C2, C5, C9, C10 | Stable taxonomy and failure semantics; **volatile**: run, action, nesting and array ceilings, polling intervals, meter values | Decision fragments of `flows-patterns.md`; the shape / meter / idempotency content is **new** | Area 4 §2, §5, §6, §7, §8, §14 | Options (C2 D3), `implementation-spec` |
| `integration/integration-mechanisms.md` | Mechanism envelope table (standard, premium and custom connectors; generic HTTP; preauthorized HTTP; batch API; webhook; broker paths; business events; polling; scheduled replication; queue; API gateway; on-premises gateway; private-network subnet delegation); the topology test (direct · mediated · event-brokered · external); delivery, ordering and dedup guarantees; payload ceilings; the **network boundary** and its mutual exclusions; **identity propagation** through a mediation tier; the synchronization risk register; the nine conditions under which the integration responsibility belongs elsewhere | *Which mechanism supports this guarantee, payload and network boundary at this throughput?* · *Whose responsibility is this integration already?* · *What happens to identity through this tier?* | C5, C6, C2, C9, C10, C12 | Stable topology test; **volatile**: every envelope figure, gateway and private-network preconditions; one **conflicted** ceiling | — (new) | Area 5 §2, §3, §4, §5, §8, §12 | Options (C5 D3), `solution-architect`, `implementation-spec` |
| `security/security-controls.md` | The **five enforcement planes** — who enforces, at what grain, what fails independently; the lowest-plane rule; trust boundary and data egress; identity propagation and the shared-identity failure; key, certificate and secret custody where decision-material; data-policy enforcement semantics; controls that are **partial by design**; the irreversible security decisions; controls whose licence dependency sits outside the platform; the residual-risk statement obligation | *Is this mandated control available at all, on which plane is it enforced, and over what population?* · *Does this design change who the backend sees?* · *Which of these choices cannot be reversed?* | C6, C3, C4, C7, C11 | Stable plane model and lowest-plane rule; **volatile**: control availability per environment class, feature states | `security-patterns.md` (research half); the plane model is **new** | Area 6 §1–§4, §12, §14 | Options (C6 D3), `compliance-officer`, `implementation-spec` |
| `governance/governance-and-environments.md` | The eight levers and what each mechanically prevents; **tenant preconditions vs solution decisions** — the distinction that makes governance findings mostly *not* design choices; environment topology and blast radius; **managed environments and the licence chain they create**; data policies at estate level; sharing limits; solution-checker enforcement; preventive vs detective controls; the external-estate boundary — platform governance does not govern the external estate; control ownership; residency fixed at environment creation | *What tenant or estate preconditions does this control level require, who owns them, and are they funded?* · *What does this control cost the whole environment population, not just the app's users?* | C7, C6, C11, C10, C8 | Stable lever model; **volatile**: enforcement dates (tripwire), lever availability, tooling deprecations | Fragments of `delivery-conventions.md` | Area 7 §1–§5, §12, §14 | Options (C7 D3), `compliance-officer`, `estimate` |
| `alm/release-and-lifecycle.md` | The four-rung ladder — what each rung buys, requires and does **not** give; solution-awareness as a prerequisite for other capabilities; deployment pipelines and their managed-environment dependency; source-controlled ALM and where version control belongs; environment variables and connection references; **no rollback**, and what that means for reversibility; the absent first-party low-code test framework; cross-boundary release coordination as a second supply chain; **reversibility mechanisms must be enabled before they are needed**; exit and portability mechanics; deprecated tooling | *Which isolation and release rung does this control requirement reach, and what does the rung require?* · *Can this be reversed — and was the mechanism enabled in time?* · *Who coordinates a release that crosses the boundary?* | C8, C12, C7, C10 | Stable ladder and the no-rollback rule; **volatile**: pipeline capabilities, version-control integration state, tooling deprecations, one dated tripwire | `delivery-conventions.md` §3 fragments | Area 8 §1–§3, §5, §14 | Options (C8/C12 D3), `implementation-spec`, `craft/delivery-conventions.md` |
| `performance/performance-and-scale.md` | Workload classification before sizing; the **meter map** — five independent limit systems, each with its own scope and window, and the rule that the binding constraint is the smallest of the five; scale envelopes per layer; **documented limit ≠ measured performance**; throttling behaviour vs quota vs hard boundary; what a limit can and cannot prove; what must be measured, at what fidelity; the absence of any universal empirical benchmark | *Which meter binds first for this workload, and is the requirement inside or outside it?* · *What must be validated before this commitment, and at what fidelity?* | C9, C4, C5, C2, C11 | Stable meter model and the limit-vs-proof rule; **volatile**: every meter value; one **conflicted** ceiling | — (new) | Area 9 §1–§5, §6, §8; `NB-04`, `NB-07` | Options (C9 D3), `solution-architect`, `/simulate`, `solution-blueprint` |
| `economics/licensing-and-cost-drivers.md` | The five economic mechanisms and their **billing units**; what makes each grow; **affected-population concepts** (people vs (person, app) pairs vs unique visitors vs active environment users); capacity, storage and API meters and what silently consumes them; **control-related licensing consequences** — a mandated control obliging an entitlement for a population that is not the app's own users; cost-driver shape; growth at horizon; cost attribution as a design constraint; the licence-avoidance trap; sunk capability; exit cost as a cost dimension. **Units, drivers, ratios — never prices** | *Which meter moves with this audience-and-frequency shape?* · *Which population does this control oblige, and is it funded?* · *What grows at horizon that does not grow today?* | C11, C6, C7, C9, C12 | Stable mechanism taxonomy; **the most volatile body in the corpus** — every entitlement rule, meter, ratio, preview meter, and three dated tripwires | `estimation-model.md` § LICENSE COST ESTIMATES (**deleted**, not migrated) · `dataverse-reference.md` § LICENSING IMPACT (price row **deleted**) | Area 10 §1–§2.6, §3, §5, §7, §14.4 | Options (C11 D3, S8), `cfo-lens`, `estimate`, `executive-report` |
| `operations/operability-and-support.md` | The four operational maturity classes and **what each changes in the architecture** — not in the ways of working; who notices / who acts / with what evidence / what they bought; monitoring and telemetry depth and its managed-environment dependency; correlation across service boundaries; alerting; **backup ≠ recovery** and the restore-window reality; recovery objectives and drills; disaster recovery and its throughput cost; incident response, support hours and plan tiers; dependency ownership; deployment ownership; skills and pro-code capacity as *availability*, not preference; diagnostic and audit evidence retention; what evidence underwrites an operational commitment | *Can this organisation actually run this design, and who accepted?* · *What does this criticality class change in the architecture?* · *Is this recovery objective evidenced or asserted?* | C10, C9, C7, C11, C8 | Stable maturity model and the backup≠recovery rule; **volatile**: retention windows, backup and restore windows, support-plan structure | `delivery-conventions.md` §5–§6 fragments | Area 11 §1–§2.6, §3, §4, §5, §6 | Options (C10 D3, S7), `operations-lead`, `implementation-spec`, `executive-report` |
| `architecture/patterns.md` | The ten patterns as **reusable compositions of mechanisms** — intent, prerequisites, strengths, weaknesses, risks, and what each **imports** (governance, ALM, cost, monitoring, recovery, a named operator); the escalation ladder and how patterns move; composition rules; the pattern-selection failure modes; the inference-lineage marker where a pattern is supported synthesis rather than vendor-endorsed | *Given the option class is established, which composition of mechanisms fits, and what does it import?* · *What does moving from this pattern to the next one cost?* | C2, C5, C9, C10, C12 | Mostly stable; heavy inference lineage requiring the marker | — (new) | Area 12 §3.2, §4, §5, §6, §7, §8 | `/blueprint`, `solution-architect`, **architecture templates (Step 5)** |

### 7.3 Per-file specification — CRAFT units

`provenance: CRAFT` · **never a D3 pull target** · may not state a platform limit, a threshold or a
comparative claim; where one is needed it cites the RESEARCH unit that owns it.

| File | Scope | Absorbs | Consumer |
|---|---|---|---|
| `craft/powerfx.md` | Validation sequence, trap catalogue, standard patterns (write, navigation, gallery, notification, audit log, error UX, collections, loading), context-variable conventions, control-property reference | `powerfx-patterns.md` minus §1–§2 | `/blueprint`, `claude-design-brief`, `implementation-spec` |
| `craft/screen-patterns.md` | 5 screen types, density, status palette, approval state machine, navigation, journey, validation UX, layout, states, tabs, responsive notes, per-screen spec template | `screen-patterns.md`, substance unchanged | `/blueprint`, `claude-design-brief` |
| `craft/screen-consolidation-rules.md` | Field-inventory → screen-plan tree, naming, hard caps | `screen-consolidation-rules.md`. **Filename preserved** — the named contract of `library/kernel/blueprint-contract.md`. The dead branch sentence (l.8) is removed | `/blueprint` (**hard dependency**) |
| `craft/excel-translation.md` | Excel → Power Fx / T-SQL catalogue, including the financial-function gap | `excel-patterns.md` | `/capture`, Options translation work, `implementation-spec` |
| `craft/flow-craft.md` | Error-handling patterns, ingestion / calculation / publication templates, expression catalogue, adaptive cards, child-flow input-output contract, decomposition heuristics, reporting-integration patterns | `flows-patterns.md` minus the decision fragments | `implementation-spec` |
| `craft/security-craft.md` | Role-inference signals, the four permission matrices, conflict resolution and log format, Power Fx security blocks, audit-on-Approve/Delete/Export blocks, artefact formats (role definition, column-security profile, group model, row-level-security view shape) | `security-patterns.md` minus the plane model | `/blueprint`, `claude-design-brief`, `implementation-spec` |
| `craft/sql-delivery-conventions.md` | Medallion layering, mandatory audit columns, stored-procedure wrapper, execution DAG, view conventions, CTE / MERGE / temporal patterns, index strategy and maintenance, reserved words | `azure-sql-reference.md` build-convention sections (~85 %) | `implementation-spec` |
| `craft/anonymization.md` | 11 sensitivity types, methods, synthetic-value patterns, anonymisation log format | `anonymization.md` | `implementation-spec`, test-data preparation |
| `craft/estimation-model.md` | Effort tables, multipliers, buffer, phase structure, overlap, team composition, standard risk register, output format, quick-win criteria, worked example, estimation anti-patterns, uncertainty handling. **Prices deleted. Barred from Options S8 comparative economics (§13.3)** | `estimation-model.md` minus § LICENSE COST ESTIMATES | `/simulate` (platform-side projection only), `estimate` |
| `craft/delivery-conventions.md` | Naming, `su:` traceability stamping, environment and ALM conventions, security and data conventions, go-live and post-go-live checklists | `delivery-conventions.md`; platform assertions cite `alm/release-and-lifecycle.md` and `governance/governance-and-environments.md` | `implementation-spec`, `/blueprint`, traceability layer |

### 7.4 Deviations from the Authoring Map §7.2 taxonomy

Five. All are consequences of the frozen Step 3 model; nothing else changed.

| # | Authoring Map §7.2 | Step 4A | Why |
|---:|---|---|---|
| 1 | `data/store-selection.md` | `data/store-boundaries.md` | *Selection* is Step 3 S4/S5. A domain file named for selection is the exact construct that produced defect X-029 (an architecture branch declared inside a reference file). Same content, re-scoped to capability boundaries, with an explicit *"this file never selects a store"* rule |
| 2 | `alm/delivery-conventions.md` | `craft/delivery-conventions.md` | Authoring Map §8.3 forbids a `CRAFT` file from stating a platform limit; keeping craft in its own namespace is the mechanism that stops it being read as research. Housing it inside `alm/` weakens that at no gain — the cross-reference works from either location |
| 3 | `*-engineering.md` naming | `*-mechanisms.md` / `security-controls.md` | Discoverability (§19). *Engineering* names an activity; the reasoner arrives with a question about a **mechanism** or a **control** |
| 4 | `governance/preconditions.md` · `alm/alm-engineering.md` | `governance/governance-and-environments.md` · `alm/release-and-lifecycle.md` | The governance/ALM seam carries the corpus's largest cross-domain fact — managed environments unlock the controls **and** create the licence chain. Splitting by **question** rather than by area gives governance the estate and its licence consequences and ALM the release/isolation ladder, with managed environments having exactly one home |
| 5 | 16 RESEARCH files | 15 RESEARCH files | Net effect of deviations 1, 2 and 4 |

### 7.5 What deliberately gets no file

| Candidate | Verdict | Rationale |
|---|---|---|
| **Agent / assistant surfaces** | No file | The canonical position is *"none evaluable — `UNKNOWN` in every class"* and the correct output is decision blocked. Already carried by scope-blocker `BS-03` and volatility row `VS-20`. A file here would be invention |
| **Analytics / reporting** | No file | The boundary question (*does the operational store also serve reporting?*) is answered by `data/store-boundaries.md`; the mechanism by `architecture/patterns.md`; the aggregation ceiling by `performance/performance-and-scale.md`. Three files for one question fails complexity test C — so the **boundary** has one home and a second pull happens only if the answer is *"yes, replicate"* |
| **Reversibility / exit** | No file | Distributed by mechanism. `alm/release-and-lifecycle.md` carries a named, mandatory *Reversibility and exit* section as its single home; `economics` carries exit cost as a cost dimension. A dedicated file would be thin and duplicative |
| **Cross-domain interaction matrix** | No file | §17. Consequences are stated locally under heading G. A 12×12 matrix is 66 mostly-empty cells that still misses triples |
| **Anti-pattern encyclopedia** | No file | §11 |
| **Alternatives (SaaS, custom, cloud-native, other low-code, incumbent)** | No file | §15 / §20.4 |
| **Proof-level catalogue** | No file section | The four proof levels live in `decision-tree.md` §12. `performance/performance-and-scale.md` says *what must be proven for this mechanism* and never restates the ladder |
| **The ten economic dimensions** | No file section | They live in `decision-tree.md` S8. `economics/licensing-and-cost-drivers.md` explains what moves each meter |
| **Document generation / templating** | No file | Recorded in the corpus as absent from Areas 1–12. Handled by the emergent-concern obligation, marked as having no canonical basis, carried as an authoring feedback item |

### 7.6 Survival test per unit

Survives on at least one of: **(1)** removing it makes a material decision question harder to answer
defensibly · **(2)** removing it creates a material architecture blind spot · **(3)** its content is
frequently required together and deserves one coherent pull target · **(4)** it contains an important
technical boundary not safely inferable from generic reasoning.

| Unit | 1 | 2 | 3 | 4 | Decisive reason |
|---|:-:|:-:|:-:|:-:|---|
| `application-surfaces` | ● | ● | ● | ● | Surface forfeits (offline × field-level security; the one-way upgrade out of a team-scoped store) are not inferable |
| `store-boundaries` | ● | ● | ● | — | The only cross-store target; without it a C4 D3 question has no entry point |
| `dataverse` | ● | ● | — | ● | Irreversible provisioning decisions |
| `sharepoint` | ● | — | — | ● | Documented **absences** — an absence is never inferable from generic reasoning |
| `azure-sql` | ● | ● | — | ● | Governance and identity move outside the platform with the store |
| `query-and-delegation` | ● | — | ● | ● | Silent truncation; delegable ≠ fast |
| `automation-mechanisms` | ● | ● | ● | ● | Shape misclassification is the corpus's most common automation failure |
| `integration-mechanisms` | ● | ● | ● | ● | Network-boundary mutual exclusions; guarantee ≠ availability |
| `security-controls` | ● | ● | ● | ● | Lowest-plane rule; partial-by-design controls |
| `governance-and-environments` | ● | ● | ● | ● | Zero direct exits — invisible without an explicit home; the licence chain |
| `release-and-lifecycle` | ● | ● | ● | ● | No rollback; reversibility must be enabled in advance |
| `performance-and-scale` | ● | ● | ● | ● | Five independent meters; limit ≠ proof |
| `licensing-and-cost-drivers` | ● | — | ● | ● | Control-obliged populations; pooled storage consumed by unbudgeted things |
| `operability-and-support` | ● | ● | ● | ● | Where no operator can exist the pattern is **unavailable**, not expensive |
| `architecture/patterns` | — | ● | ● | ● | What a pattern **imports** is the blind spot; Step 5 generates templates from it |
| `craft/*` (10) | — | — | ● | ● | Named consumers (`/blueprint` hard contract, design brief, `/simulate`, `estimate`) and non-inferable convention. **Never** survives on decision grounds |

---

## 8. Concrete pull-question catalogue

**This is an authoring coverage test, not a runtime router.** Nothing here is encoded in the pack. Its job
is to prove that a materially complete set of D3 questions each has exactly one obvious first target.

| # | Candidate / mechanism context | Concern | Why deeper knowledge is needed | Concrete question | First pull | Expected answer shape | Stability | Needs current verification |
|---:|---|---|---|---|---|---|---|---|
| 1 | Candidate proposes a governed relational store as system of record | C4 | The requirement is atomicity across rows plus an authority claim | *What transactional and authorization semantics does this store provide, and where does atomicity stop?* | `data/dataverse.md` | Named transactional scope + the boundary at which it ends + the mechanism required to obtain it | Stable | No |
| 2 | Candidate keeps the list-based store and adds per-column confidentiality | C4 + C6 | An **absence** cannot be inferred | *Does this store enforce column-level confidentiality, and if not what is the documented consequence?* | `data/sharepoint.md` | *"Not enforced; the documented workarounds are X and Y and neither is enforcement"* + the landing in C6 | Stable | No |
| 3 | Any candidate with a queried entity above the client cache | C4 + C9 | Silent truncation is a correctness failure, not a latency one | *Is this access path delegation-safe, and is delegation-safe also fast enough here?* | `data/query-and-delegation.md` | Delegable / not-delegable per operation + the truncation semantics + the separate latency question | Stable principle, volatile figures | Cache default and maximum (`VS-02`) |
| 4 | Reporting requirement over the same entities as the operational app | C4 + C9 + C11 | Whether a second store is forced changes architecture and cost | *Can the operational store serve this reporting shape, or does it force replication — and what does replication oblige?* | `data/store-boundaries.md` | Boundary verdict + the obligations replication imports (reconciliation owner, restore, cost) | Stable boundary | Aggregation ceiling and refresh window (`VS-06`) |
| 5 | High-frequency machine work proposed as a workflow | C2 + C9 | Shape misclassification is the dominant automation failure | *Which shape is this, which mechanism carries it, and what fails first?* | `automation/automation-mechanisms.md` | Shape classification + mechanism envelope + the first-failing dimension | Stable taxonomy | Run and action ceilings (`VS-12`, `VS-13`) |
| 6 | Automation with side effects and a retry policy | C2 + C10 | Retry duplicates non-idempotent effects | *What does retry do to this side effect, and what must the design guarantee?* | `automation/automation-mechanisms.md` | Idempotency-key obligation + failure semantics + the reconciliation consequence | Stable | No |
| 7 | Long-running human wait spanning a release | C2 + C8 | A wait that outlives a run is a different shape | *Can this wait survive a deployment or a version change?* | `automation/automation-mechanisms.md` | Duration boundary + the shape escalation it forces | Stable shape, volatile ceiling | Run duration (`VS-13`) |
| 8 | Candidate crosses a private network boundary | C5 + C6 | Connectivity mechanisms have mutual exclusions | *Which connectivity mechanisms support this boundary, and what do they exclude?* | `integration/integration-mechanisms.md` | Supported paths + the mutually exclusive one + irreversible preconditions | Stable exclusions | Gateway and delegation preconditions (`VS-11`) |
| 9 | Guaranteed, ordered, deduplicated message exchange required | C5 + C9 | Guarantees differ per mechanism and are not interchangeable | *Which mechanism supports this guarantee at this payload and throughput?* | `integration/integration-mechanisms.md` | Guarantee matrix + payload ceiling + what moves outside the platform | Stable | Payload ceilings (`VS-10`); one **conflicted** ceiling |
| 10 | An enterprise integration capability already exists | C5 + C7 + C10 | Ownership precedes mechanism | *Whose responsibility is this integration already, and what does that leave in scope?* | `integration/integration-mechanisms.md` | Ownership test + the reduced remit + the governance consequence of ignoring it | Stable | No |
| 11 | Mediation tier in front of a per-user-authorizing backend | C6 + C5 | The backend may stop seeing the user | *What happens to identity through this tier, and where is authorization then enforced?* | `security/security-controls.md` | Plane analysis + the shared-identity failure + the condition that makes it acceptable | Stable | No |
| 12 | A mandated regulatory control | C6 + C11 | Availability, population and funding are three questions | *Is this control available at all, on which plane, over what population, and what does it oblige?* | `security/security-controls.md` | Availability verdict + enforcing plane + population + the landing in C11 | Stable model, volatile availability | Control availability per environment class (`VC-03`) |
| 13 | Data must not leave a boundary | C6 + C7 + C4 | Residency is fixed at environment creation | *Where is residency decided, and is that decision reversible?* | `security/security-controls.md` → `governance/governance-and-environments.md` | Irreversible-decision statement + the precondition owner | Stable | No |
| 14 | A preventive governance control is required | C7 + C11 | The control has an estate-wide licence consequence | *What does this control require of the estate, and what does it cost the whole environment population?* | `governance/governance-and-environments.md` | Precondition + the licence chain + who owns and funds it | Stable shape, **dated** enforcement | Enforcement date and current default (tripwire `TW-V3`) |
| 15 | Several makers changing one solution continuously | C8 + C7 | Isolation is a rung, not a practice | *Which release rung does this reach, and what does the rung require?* | `alm/release-and-lifecycle.md` | Rung + prerequisites + what the rung does **not** give | Stable ladder | Pipeline capabilities (`VC-05`) |
| 16 | Commitment includes the ability to undo a release | C8 + C12 | There is no rollback | *Can this be reversed, and was the mechanism enabled before it was needed?* | `alm/release-and-lifecycle.md` | The no-rollback statement + the enable-in-advance obligation + the exit mechanics | Stable | No |
| 17 | Peak throughput requirement on a multi-hop path | C9 + C5 | The binding meter is rarely the one people plan against | *Which of the five meters binds first here, and is the requirement inside it?* | `performance/performance-and-scale.md` | Meter identification + envelope + **what the limit does not prove** | Stable model | Every meter value; one **conflicted** ceiling (`VC-01`/`VS-08`) |
| 18 | A latency or availability commitment is being written | C9 + C10 | A documented limit proves nothing end-to-end | *What must be validated before this commitment, and at what fidelity?* | `performance/performance-and-scale.md` | The proof obligation + the measurement design; the **level** itself comes from the spine | Stable | No |
| 19 | Large unpredictable external audience | C11 | The meter and the population are the whole answer | *Which meter moves with this audience-and-frequency shape, and how is the population counted?* | `economics/licensing-and-cost-drivers.md` | Mechanism + billing unit + the counting hazard + growth at horizon | Stable taxonomy | Meter definitions and preview state (`VC-06`) |
| 20 | Mandated control whose population is unfunded | C11 + C6 | Infeasibility, not a trade-off | *Which population does this control oblige, and is that population funded?* | `economics/licensing-and-cost-drivers.md` | Obliged population + the funding question; the **outcome** is decided at S8 | Stable shape | Entitlement rules (`VC-05`) |
| 21 | Criticality above demonstrated operating maturity | C10 | Maturity is an architecture input | *What does this criticality class change in the architecture, and can this organisation run it?* | `operations/operability-and-support.md` | The class's architectural deltas + the capability gap + who must accept | Stable model | Support plan structure (`VC-08`) |
| 22 | A recovery objective is being committed | C10 + C9 | A backup existing is not recovery | *Is this recovery objective evidenced, and what is the actual restore behaviour?* | `operations/operability-and-support.md` | Backup ≠ recovery + restore-window reality + the drill obligation | Stable rule, volatile windows | Backup and restore windows (`VS-07`, `VS-17`) |
| 23 | Observability required for an operational commitment | C10 + C11 | Telemetry depth has a governance and licence dependency | *What telemetry is natively available, for how long, and what does obtaining more require?* | `operations/operability-and-support.md` | Native depth + retention + the managed-environment dependency + the cost landing | Stable | Retention windows (`VS-18`, `VS-19`) |
| 24 | Field population working disconnected, with confidentiality | C3 + C6 | The combination is a documented mutual exclusion | *Can this surface deliver offline at this depth alongside field-level confidentiality?* | `application/application-surfaces.md` | The forfeit + which surfaces are excluded + the landing in C6 | Stable | Feature states (`VC-10`) |
| 25 | External, unauthenticated audience | C3 + C6 + C11 | Surface, identity class and meter are one question | *Which surface serves this identity class, and what does it oblige downstream?* | `application/application-surfaces.md` | Surface set + identity model + landings in C6 and C11 | Stable | Preview / GA states (`VC-10`) |
| 26 | Requirement may already be met by an owned capability | C1 | Rung 0 precedes any app-type question | *Is this already met by a first-party app or a capability the organisation owns?* | `application/application-surfaces.md` | Rung-0 test + what configuration would cover + what it would not | Stable | No |
| 27 | Option class established; composition to be chosen | C2 + C5 + C10 | A pattern imports obligations nobody chose | *Which composition fits, and what does it import — governance, ALM, cost, monitoring, recovery, operator?* | `architecture/patterns.md` | Pattern + imported obligations + the escalation cost to the next pattern | Stable, inference-lineage marked | No |

**The brief's three worked examples.** Governed relational store + atomicity → row 1. Private network
boundary → row 8. High-frequency automation → rows 5 and 17. All three resolve to a single first pull, with
a second pull only where the first exposes a dependency.

---

## 9. Twelve-concern coverage

A unit may support several concerns; a concern may pull several units. **Authoring guidance, not runtime
routing.**

| Concern | Primary unit | Secondary units | Depth verdict |
|---|---|---|---|
| **C1** Need / value / existing capability | `application/application-surfaces.md` (rung 0 — configure, buy, first-party) | `economics/licensing-and-cost-drivers.md` (cost-of-ownership shape) | Sufficient. Most of C1 is engagement evidence and S0 logic, not domain knowledge |
| **C2** Functional / process | `automation/automation-mechanisms.md` | `integration/integration-mechanisms.md` (message-shaped work), `application/application-surfaces.md` (process-driven surfaces), `architecture/patterns.md` | Deep |
| **C3** User / experience | `application/application-surfaces.md` | `security/security-controls.md` (offline × confidentiality), `craft/screen-patterns.md` + `craft/screen-consolidation-rules.md` (post-Options) | Deep |
| **C4** Data / information | `data/store-boundaries.md` | `data/dataverse.md`, `data/sharepoint.md`, `data/azure-sql.md`, `data/query-and-delegation.md` | Deep — five units, each a distinct question |
| **C5** Integration / ecosystem | `integration/integration-mechanisms.md` | `automation/automation-mechanisms.md` (triggers, polling), `performance/performance-and-scale.md` (throughput), `architecture/patterns.md` | Deep |
| **C6** Security / privacy / control | `security/security-controls.md` | `integration/integration-mechanisms.md` (network, identity propagation), `governance/governance-and-environments.md` (policy levers), `data/*` (authorization grain per store) | Deep |
| **C7** Governance / authority / compliance | `governance/governance-and-environments.md` | `alm/release-and-lifecycle.md`, `operations/operability-and-support.md` (control ownership), `security/security-controls.md` | Deep — and required, because C7 produces **zero direct exits** and is otherwise invisible |
| **C8** Lifecycle / ALM / change | `alm/release-and-lifecycle.md` | `governance/governance-and-environments.md` (managed-environment prerequisite), `operations/operability-and-support.md` (deployment ownership) | Deep — same zero-direct-exit argument |
| **C9** Scale / performance / resilience | `performance/performance-and-scale.md` | `automation/*`, `integration/*` (per-mechanism envelopes), `data/query-and-delegation.md`, `operations/*` (recovery) | Deep |
| **C10** Operability / support / ownership | `operations/operability-and-support.md` | `governance/*` (control ownership), `alm/*` (release ownership), `architecture/patterns.md` (what a pattern imports) | Deep — first-class, per Step 3 §14 |
| **C11** Economics / entitlement / TCO | `economics/licensing-and-cost-drivers.md` | `governance/*` (licence chain), `operations/*` (support and telemetry cost), `performance/*` (capacity), `data/dataverse.md` (audit capacity) | Deep on drivers; **deliberately shallow on prices** (§13) |
| **C12** Strategic fit / reversibility / dependency | `alm/release-and-lifecycle.md` (named *Reversibility and exit* section) | `architecture/patterns.md` (dependency shape), `economics/*` (exit cost), `application/*` (one-way surface upgrades) | Sufficient. No own file — §7.5 |

**No file was created because a concern exists.** 12 concerns → 15 research units, many-to-many.

---

## 10. Canonical research coverage accounting

**Accounted for ≠ copied to runtime.** For each canonical family: which runtime unit carries it, what stays
authoring-only, what Step 3 already consumed, what belongs downstream, what is volatile, and what is
excluded with a reason.

| Area | Runtime unit(s) | Already consumed by Step 3 | Downstream (Step 5 templates / deliverables) | Authoring-only | Volatile handling | Intentional exclusions |
|---:|---|---|---|---|---|---|
| **1 Platform Suitability** | `application/application-surfaces.md` (fit rows), `data/store-boundaries.md` | Fit verdicts feed candidate generation and the exit classes | Outcome-shaped templates | The full 19-row matrix prose, the source register, evidence-quality notes | Feature-state rows → *verify current state* | Vendor positioning statements — not decision-bearing |
| **2 Application Architecture** | `application/application-surfaces.md`; a11y and l10n boundaries in the same unit | `DC-D-009…020`, `116` compressed into C3 | `canvas-application`, `model-driven-application`, `external-audience-site` templates | §11 source register, §8 evidence-quality notes | Preview/GA banner states (`VC-10`) | Portal and SPA build detail — implementation altitude |
| **3 Data Architecture** | `data/store-boundaries.md`, `data/dataverse.md`, `data/sharepoint.md`, `data/azure-sql.md`, `data/query-and-delegation.md` | Store-related absolutes and blocking entries | `dataverse-application`, `collaboration-surface` templates | 617 KB of finding prose; sub-registers `DV/SQ/SP/EX/XC/VT/SY/SQ2/SC/DQ`; source register | `VS-02`, `VS-04`, `VS-06` | Analytical-store product detail (§7.5); schema-modelling craft → `craft/` |
| **4 Automation Architecture** | `automation/automation-mechanisms.md`; craft to `craft/flow-craft.md` | Work-shape criteria (`DC-D-048…057`) compressed into C2 | — | §15 source register, §16 v1→v2 map, §8 negative-evidence prose | `VS-03`, `VS-12`, `VS-13`, `VS-14`, `VS-16` | Interface-automation product tour — only the boundary is decision-relevant |
| **5 Integration** | `integration/integration-mechanisms.md` | Network-boundary and permissibility floor entries; composed rows 3, 6, 8 | `hybrid-cloud-native`, `hybrid-enterprise-boundary` templates | §14 source register; the full envelope prose | `VS-10`, `VS-11`; the **conflicted** ceiling stays conflicted | Vendor-specific middleware comparison — no comparator evidence |
| **6 Security** | `security/security-controls.md`; craft to `craft/security-craft.md` | `DC-D-059`, `062`, `067` absolutes; composed rows 3, 6, 10 | `implementation-spec` irreversibility slot | §11 source register, §14 reconciliation prose | `VC-03`; control availability per environment class | Threat-modelling methodology — outside corpus scope |
| **7 Governance** | `governance/governance-and-environments.md` | Composed rows 11, 12; the preconditions framing | `estimate` unfunded-precondition slot | §11 source register, §12 cross-area prose | Tripwire `TW-V3`; lever availability | Deprecated tooling as a recommendation — recorded as deprecation only |
| **8 ALM / DevOps** | `alm/release-and-lifecycle.md`; conventions to `craft/delivery-conventions.md` | Composed rows 11, 12; the reversibility blocking entry | `solution-blueprint` proof slot | §11 source register; the eight churn-expected items | Tripwire `TW-V1`; pipeline capabilities | Pipeline UI walkthroughs — implementation altitude |
| **9 Performance and Scale** | `performance/performance-and-scale.md` | The limit-vs-proof rule and the proof ladder are **in the spine** | `solution-blueprint` validation slot | §14 source register; §11 cross-area prose | Every meter value; `VC-01`/`VS-08` conflict | Universal throughput thresholds — **would be invention** (`NB-07`) |
| **10 Licensing and Cost** | `economics/licensing-and-cost-drivers.md` | The ten cost dimensions are **in the spine** (S8); class-7 subtype logic | `estimate` cost-driver and entitlement slots | §13 source register; §4 cost-review method | 10 commercial rows + 3 tripwires | **All prices and SKUs** (§13); comparative TCO — no like-for-like evidence exists |
| **11 Operations and Support** | `operations/operability-and-support.md` | `DC-D-006`, `073`, `100`, `104`, `110` blocking entries; composed rows 2, 8, 9 | `executive-report` operating-model slot | §12 source register; §9 cross-area prose | `VS-07`, `VS-17`, `VS-18`, `VS-19` | Support-contract commercial terms — volatile and customer-specific |
| **12 Architecture Patterns** | `architecture/patterns.md` | Pattern-gated composed rows (2, 7) | **Step 5 templates are generated from this unit** | §12 source register; the full catalogue prose | Inference lineage marked, not dated | Pattern-by-pattern implementation guides — Step 5 and implementation altitude |
| **13 Anti-Patterns** | Failure-mode notes inside the owning units (§11) | 3 GATE + 4 CONSTRAINT already in the decision model | Some become template warnings | The 68 full entries, detection signals, exceptions, the ledger | — | A runtime anti-pattern encyclopedia (§11); the portfolio-altitude entry is never surfaced |
| **14 Alternatives** | **None** (§20.4) | `alternatives-register.md` — the whole family | — | The 11 class bodies | — | Pseudo-knowledge about alternatives |
| **15 Decision Criteria** | **None** — criteria are decision logic | Compressed into the 12 concerns; `blocking-set.md`; `outcome-classes.md` | — | All 116 criterion bodies | Both volatility classes → the register | A criteria register at runtime — Step 3 deliberately did not create one |
| **Decision Intelligence Matrix** | **None** | `composed-disqualifiers.md`, the stage order, the scenario corpus | — | The 18 scenarios | Matrix §4 → the register | — |
| **Reservations `NB-01…08`** | Carried as *what must be verified* / *what not to infer* inside the owning units | `NB-02` → the conflict; `NB-07` → the limit-vs-proof rule | — | The reservation prose | Each keeps its unknown | None — silently resolving a reservation is forbidden |

**No material canonical knowledge disappears.** Every family lands in exactly one of: a runtime unit · the
frozen decision model · a Step 5 template · an explicitly reasoned exclusion.

---

## 11. Anti-pattern disposition

**No runtime anti-pattern encyclopedia.** 68 entries would be a second decision model with no stage that
runs it.

### 11.1 Precedence — one behaviour, one primary runtime home

```text
1. decision model (GATE · CONSTRAINT · blocking · composed row)   ← if it can make an option unavailable
2. a failure-mode note inside the owning knowledge unit           ← if it is a technical failure mode
3. an architecture template warning (Step 5)                      ← if it is a composition failure
4. authoring-only                                                 ← if it is reasoning, portfolio or process
```

An entry appears at exactly one level. Lower levels may **cross-reference**, never restate.

### 11.2 Enforcement-class disposition

| Class | Count | Disposition |
|---|---:|---|
| **GATE** | 3 | **Decision model only.** They make an option unavailable; a domain file cannot carry that without carrying selection logic |
| **CONSTRAINT** | 4 | Split by nature. The *reasoning* constraint — inventing thresholds, treating a documented limit as proof — is already the spine's §11/§12 rule and is **not** restated in domain knowledge. The other three become one-line failure-mode notes in their owning unit, carrying the scope statement that bounds them |
| **ANTI-PATTERN** | 61 | Triaged per §11.3 |
| **Portfolio altitude** | 1 (within the 68) | **Authoring-only.** Never surfaced as an engagement finding; its constituent mechanisms fire through five other entries |

### 11.3 Per-family disposition

| Canonical family | Runtime home | Note |
|---|---|---|
| Selection and architecture | Decision model (already) + `architecture/patterns.md` for composition failures | The selection failures are Step 3's business; only the composition ones move |
| Data | Failure-mode notes in `data/*` | Store-named entries live in that store's file; cross-store ones in `store-boundaries.md` |
| Automation and process | Failure-mode notes in `automation/automation-mechanisms.md` | This family is largely one error — a shape-2/3/4 requirement built as shape 1 — so it becomes **one** decision-sensitive distinction, not N notes |
| Integration | Failure-mode notes in `integration/integration-mechanisms.md` | Point-to-point explosion and duplicated transformation reduce to the ownership test |
| Security | Failure-mode notes in `security/security-controls.md` | The app-as-authorization-layer entry becomes the lowest-plane rule's worked negative case |
| Governance | Decision model (composed rows) + notes in `governance/governance-and-environments.md` | **The matched pairs must both be carried** — over- and under-governance are opposing failures of one lever, and encoding one half systematically pushes engagements toward the other |
| ALM and delivery | Notes in `alm/release-and-lifecycle.md` | Concurrent-maker overwrite is a composed row, not a note |
| Performance and scale | The spine's limit-vs-proof rule + notes in `performance/performance-and-scale.md` | The proof-obligation cluster stays with the spine |
| Operations | Decision model (blocking + composed) + notes in `operations/operability-and-support.md` | *No operator ⇒ unavailable* is a gate, not a note |
| Cost | Notes in `economics/licensing-and-cost-drivers.md` | Includes the licence-avoidance trap and the too-cheap / too-heavy pair |
| Cross-cutting | Authoring-only, except where an entry names one mechanism | Cross-cutting entries with no single home are exactly the encyclopedia filler this section prevents |
| User experience and interaction | Notes in `application/application-surfaces.md`; the remainder authoring-only | Several are already absorbed into C3 signals |
| Pattern-selection anti-patterns (Area 12) | `architecture/patterns.md`, **only** where not already a decision-model entry | Cross-reference where they duplicate |

### 11.4 Form of a runtime failure-mode note

One to three lines, stating **the mechanism of failure**, not the story:

> **Retry without an idempotency key.** A retry re-executes the side effect. Where the effect is a posting,
> a notification or an external write, the duplicate is invisible until reconciliation. Consequence: a
> reconciliation owner becomes a requirement, not a nicety.

No id, no detection-signal list, no exception matrix — those stay in the corpus and, where decision-bearing,
in the decision model.

### 11.5 Duplication control

Step 4B produces a **behaviour → single-home table** covering all 68 entries. A behaviour appearing in two
runtime homes is a defect. Cross-references are not duplication; restatements are.

---

## 12. Architecture-pattern / architecture-template boundary

Three distinct things. Collapsing any two is how a template acquires unstated obligations.

| Layer | What it is | Where | Step |
|---|---|---|---|
| **Domain knowledge** | Mechanisms, constraints, boundaries and trade-offs | `domain-knowledge/*` (the 14 units besides `patterns.md`) | Step 4 |
| **Architecture pattern** | A reusable **composition of mechanisms**, with what it requires and what it **imports** | `domain-knowledge/architecture/patterns.md` | Step 4 |
| **Architecture template** | A reusable **blueprint / output shape** reachable from an outcome class | `architecture-templates/*` | **Step 5** |

**Rules.**

1. `architecture/patterns.md` explains patterns. It never renders a blueprint and never selects one.
2. Step 5 templates are **generated from** `patterns.md` plus the outcome-class set; the pattern file stays
   the knowledge, the template stays the output shape.
3. The positioning already frozen in `architecture-templates/README.md` — shapes are reachable *after* an
   outcome and are never the option space — is **unchanged by Step 4** and is not restated in `patterns.md`.
4. What a pattern **imports** (governance, ALM, cost, monitoring, recovery, a named operator) is the pattern
   file's most decision-bearing content, and it is the thing templates most often omit.

---

## 13. Licensing and cost boundary

### 13.1 Depth required — must support C11 and stage S8

Entitlement models · affected-population concepts · capacity, storage and API meters · control-related
licensing consequences · cost-driver shape · growth at horizon · operational and support consequences ·
cost attribution · sunk capability · exit cost.

### 13.2 The durable / volatile split — explicit

| Durable conceptual knowledge (lives in the unit) | Volatile, current-verification knowledge (register + engagement row) |
|---|---|
| Five economic mechanisms operate simultaneously, and a design decision can move cost between them without reducing it | Which mechanism a specific capability falls under **today** |
| The billing **unit** of each mechanism — a person · a (person, app) pair · an automation object · a usage event · a GB-month | The **price** of any unit — **never in the pack** |
| Storage is pooled at tenant level and consumed by things nobody budgets (audit, indexes, attachments, replicas); exceeding it blocks administrative operations | The pooled increments, the ratios, the over-limit countdown |
| A preventive governance control obliges an entitlement for **every active user of the environment**, not for the app's users | The enforcement date, the current default, the licence's name |
| The counting hazards: people ≠ (person, app) pairs; data volume ≠ audit volume; unique people ≠ billable visitors | Metering definitions and their documented over-count behaviour |
| Growth at horizon is what is priced, not the launch state | The growth rates — engagement facts |
| An unfunded mandated control is an economic **infeasibility question**, not a trade-off | Whether it is funded — an engagement fact |
| Cost of inaction and manual operation are priced on the same dimensions | The organisation's own figures |

### 13.3 What the unit must never become

A price list · a SKU catalogue · a detailed estimate · a comparative TCO against unevaluated alternatives.

**Binding consequence — `craft/estimation-model.md` is barred from Options S8 comparative economics.** It
carries platform-side effort bands with **no comparator-side basis**; using it at S8 produces a quantified
figure for one class against silence for every other, which is comparator preference by construction. It is
available (a) in `/simulate` for projecting a platform candidate, where the output must carry the asymmetry
statement, and (b) post-decision for the `estimate` deliverable. Recorded because it has already happened:
`projects/pricing-marinha/shared-understanding.md` **A-043** carries per-branch effort bands with no
comparator equivalent.

---

## 14. Security / governance / ALM coverage

Not compressed. Coverage check against the brief's list:

| Required depth | Home | Sufficient |
|---|---|---|
| Authorization enforcement | `security/security-controls.md` — the plane model + the lowest-plane rule | Yes |
| Trust boundaries | `security/security-controls.md` + `integration/integration-mechanisms.md` (mechanism side) | Yes |
| Data egress | `security/security-controls.md` (semantics) + `governance/governance-and-environments.md` (policy lever) | Yes — one home each, cross-referenced |
| Identity propagation | `integration/integration-mechanisms.md` (mechanism) + `security/security-controls.md` (the shared-identity failure) | Yes |
| Policy implications | `governance/governance-and-environments.md` (lever, cost, who configures) + `security/security-controls.md` (what it enforces and where) | Yes — the split is stated in both files |
| Environment topology | `governance/governance-and-environments.md` (estate strategy and its consequences) | Yes |
| Solution-aware deployment | `alm/release-and-lifecycle.md` (the prerequisite chain) | Yes |
| Maker governance | `governance/governance-and-environments.md` | Yes |
| Control ownership | `governance/governance-and-environments.md` + `operations/operability-and-support.md` | Yes |
| Recovery / rollback | `alm/release-and-lifecycle.md` (**no rollback**) + `operations/operability-and-support.md` (recovery) | Yes — two different questions, two homes |
| Audit / evidence retention | `data/dataverse.md` (audit capacity) + `operations/operability-and-support.md` (retention windows) + `governance/*` (the compliance obligation) | Yes |
| Key / certificate / secret handling | `security/security-controls.md`, **only where decision-material** | Yes — key custody and customer-managed keys are decision-material; rotation mechanics are implementation |

**Duplication controls at the three known seams:**

| Seam | Owner of the mechanism | Owner of the consequence |
|---|---|---|
| Data policies | `security/security-controls.md` — what they enforce, on which plane | `governance/governance-and-environments.md` — who configures, what it prevents estate-wide, what it costs |
| Managed environments | `governance/governance-and-environments.md` — sole home, including the licence chain | `alm/release-and-lifecycle.md` cross-references it as a rung-2 prerequisite |
| Environment topology | `governance/governance-and-environments.md` — the estate strategy | `alm/release-and-lifecycle.md` — what a rung requires of environments |

**Goal met:** no material enterprise-architecture blind spot when a question reaches D3.

---

## 15. Performance and scale coverage

The unit must keep seven things apart, because collapsing any pair produces a false verdict:

| Concept | What it is | What it is not |
|---|---|---|
| **Published hard boundary** | A documented structural ceiling | Evidence of performance |
| **Quota** | An entitlement allowance over a window | A throughput guarantee |
| **Throttling behaviour** | What the service does at the edge | A failure mode designable-around without measurement |
| **Measured workload** | An observation of the real system | A published figure |
| **Performance hypothesis** | A stated expectation | A commitment |
| **Validation requirement** | What must be measured, at what fidelity | The proof **level**, which is the spine's |
| **End-to-end SLA/SLO** | A composite over every dependency | A platform availability figure |

**Preserved Step 3 rule, stated once, in the unit:** *limits can exclude designs; they do not prove
performance.* No universal throughput threshold is invented — the corpus is limits-based, not
benchmark-based, and that absence is itself carried as evidence.

**The conflicted ceiling** is rendered as the conflict plus the measurement obligation, on both sides, and
symmetrically across candidate classes.

---

## 16. Operability coverage

C10 proved first-class in Step 3 (stage S7 gate + composed rows 2, 8, 9 + five blocking criteria). The unit
carries all ten required depths:

| Required | Carried as |
|---|---|
| Operational ownership | Named-and-accepted accountable ownership; what "accepted" means as evidence |
| Monitoring | Native telemetry depth, its managed-environment dependency, correlation across service boundaries |
| Alerting | What exists natively, what must be built, what must be staffed |
| Recovery | Backup ≠ recovery; restore-window reality; recovery objectives; drills; DR and its throughput cost |
| Support | First-line ownership, support hours, plan tiers, what the vendor's support does **not** fill |
| Dependency ownership | Platform resilience says nothing about the systems on the path |
| Deployment ownership | Cross-boundary coordination as a second supply chain |
| Skills / capability | Pro-code capacity as **availability** — in-house and available, not planned |
| Continuity | The four maturity classes and what each changes **in the architecture** |
| Evidence underwriting a commitment | What must exist for an operational commitment to be defensible |

**Explicitly not solved by adding Discovery cues.** This is technical and operating depth reached *after*
materiality is established, at S5 and S7. The Discovery layer is frozen and unchanged.

---

## 17. Cross-domain coverage

**No cross-domain matrix file.** Each unit states its consequences locally under heading G. Validation that
the six required interactions each have a stated home:

| Interaction | Stated in | Landing |
|---|---|---|
| security → economics | `security/security-controls.md` G · `economics/licensing-and-cost-drivers.md` (control-obliged population) | Composed row 3 |
| data → performance / cost | `data/store-boundaries.md` G · `data/dataverse.md` G (audit capacity) · `performance/*` | Capacity and meter consequences |
| governance → ALM / operations | `governance/governance-and-environments.md` G — managed environments unlock the controls **and** gate pipelines | Composed rows 11, 12 |
| user / offline → architecture / control / support | `application/application-surfaces.md` G (offline forfeits) → `security/*`, `operations/*` | Composed row 10 |
| integration → resilience / operations | `integration/integration-mechanisms.md` G (sync risk register, reconciliation owner) | Composed row 8 |
| scale → architecture / economics | `performance/performance-and-scale.md` G — the meter that binds moves the design, and the meter that bills | Growth-at-horizon pricing |

**Why local statements and not a matrix.** A consequence is only actionable next to the mechanism that
causes it. A matrix file would be pulled by nobody holding a concrete question, would duplicate every cell,
and would still miss triples — which is why Step 3 handles combinations with twelve registered rows plus an
emergent test rather than with 66 pairs.

---

## 18. Runtime provenance model

### 18.1 The convention, inherited from the frozen Step 3 runtime

Mechanically verified against the frozen files: `decision-tree.md` and the five registers contain **zero**
canonical research ids (`DC-D-*`, `AP-D-*`, area ids) and **zero** `Research basis:` lines. Step 3B1
deviation 2 resolved this deliberately — *"zero canonical research ids at runtime; local anchors so the rows
stay unambiguous and testable."*

**Step 4 follows the frozen convention.** This is a documented departure from `pp-pack-authoring-map.md`
§8, which specified a `Research basis:` line in every runtime file. The map's convention predates Step 3;
running two provenance conventions in one pack would be worse than either.

| Layer | Carries |
|---|---|
| **Authoring report (Step 4B)** | A per-file provenance table: every material rule → its canonical ids, with the map's §8.2 disambiguation for overloaded area-local ids. This table is the object gates G1/G3/G7 run against |
| **Runtime file** | Clear factual wording · an HTML-comment header · grade markers · volatility stamps naming a **runtime register row**, never a research id |
| **Engagement** | The reading actually used, with `verificado_em` + `validade` |

### 18.2 Runtime header

```markdown
# <Title — the question domain>

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH | CRAFT
authored: 2026-09-NN (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->
```

`class: CRAFT` files add one sentence in the body: *engagement practice, no research basis; states no
platform limit, threshold or comparative claim — where one is needed it cites the file that owns it.*

### 18.3 Volatility stamp

```markdown
> Documented reading · read 2026-09-NN · re-verify: VS-04 (design time)
```

Names a **runtime** register row. Register anchors (`VS-NN`, `VC-NN`, `TW-VN`, `B-NN`, `CD-NN`) are internal
execution anchors and are **never rendered to the engagement** — the same rule as `decision-tree.md` §14.3.

### 18.4 Non-goals

No claim ledger · no per-sentence ids · no bidirectional index · no confidence scores of our own · no
provenance subsystem. A maintainer with `grep` must be able to audit it.

---

## 19. Discoverability test

For each proposed file: could a reasoner holding the concrete question infer from the path and title that
this is the right file to open? **Must be YES.**

| Concrete question | Inferred target | Pass |
|---|---|---|
| *Can this surface work offline with field-level confidentiality?* | `application/application-surfaces.md` | ✅ |
| *Which store can carry this authority and integrity requirement?* | `data/store-boundaries.md` | ✅ |
| *What are this store's transactional semantics?* | `data/dataverse.md` · `data/sharepoint.md` · `data/azure-sql.md` | ✅ — named by the store the candidate proposes |
| *Is this query delegation-safe?* | `data/query-and-delegation.md` | ✅ |
| *Which automation mechanism carries this work shape?* | `automation/automation-mechanisms.md` | ✅ |
| *What connectivity supports this network boundary?* | `integration/integration-mechanisms.md` | ✅ |
| *Is this control available, and where is it enforced?* | `security/security-controls.md` | ✅ |
| *What tenant preconditions does this control level require?* | `governance/governance-and-environments.md` | ✅ |
| *Which release rung does this reach, and can it be reversed?* | `alm/release-and-lifecycle.md` | ✅ |
| *Which meter binds first, and what must be measured?* | `performance/performance-and-scale.md` | ✅ |
| *Which meter moves with this audience shape?* | `economics/licensing-and-cost-drivers.md` | ✅ |
| *Can this organisation run it, and is recovery evidenced?* | `operations/operability-and-support.md` | ✅ |
| *Which composition fits, and what does it import?* | `architecture/patterns.md` | ✅ |
| *What is the standard write pattern for this form?* | `craft/powerfx.md` | ✅ |
| *How many screens does this field inventory produce?* | `craft/screen-consolidation-rules.md` | ✅ |

**Renames driven by this test, not by taste:** `*-engineering.md` → `*-mechanisms.md` ·
`store-selection.md` → `store-boundaries.md` · `preconditions.md` → `governance-and-environments.md` ·
`alm-engineering.md` → `release-and-lifecycle.md` · `cost/` → `economics/`.

**No router.** The directory names are the subject boundaries, the filenames name the question domain, and
each file's §0 lists its pull questions. Bad taxonomy is not solved with a router — it is solved by
renaming, splitting or merging, which is what happened above.

---

## 20. Survival, depth and complexity tests

### 20.1 Survival — §7.6

All 25 units pass on at least one criterion. **No unit survives because canonical research exists for the
topic, because the topic is interesting, because completeness looks better, or because a vendor
documentation category exists.** The four candidates that failed on exactly those grounds are in §7.5:
agent surfaces, analytics, the cross-domain matrix, and alternatives.

### 20.2 Depth — the nine required areas

| Area | Question | Verdict | Where the depth is |
|---|---|---|---|
| Data | Can the reasoner choose and condition a data architecture? | **YES** | 5 units: cross-store boundaries + three store depths + query/delegation |
| Automation | Mechanism fit, waits, idempotency, failure semantics? | **YES** | Four shapes + classification test + meters + retry-duplication rule + wait boundaries |
| Integration | Ownership, delivery guarantees, network boundaries, throughput? | **YES** | Envelope table + topology test + ownership test + network boundary + sync risk register |
| Security | Authorization, trust and control boundaries? | **YES** | Five planes + lowest-plane rule + egress + identity propagation + partial-by-design + irreversibles |
| Governance / ALM | Environment, lifecycle, deployment, control obligations? | **YES** | Eight levers + preconditions framing + four rungs + no-rollback + cross-boundary coordination |
| Performance | Limits vs proof, and validation specification? | **YES** | Meter map + the seven-way separation (§15) + what must be measured |
| Licensing / economics | What moves cost, without pretending to price? | **YES** | Five mechanisms + units + drivers + obliged populations + growth at horizon; **zero prices** |
| Operability | Can the organisation actually run the design? | **YES** | Four maturity classes with architectural deltas + all ten required depths (§16) |
| Reversibility | Exit and dependency consequences? | **YES** | Named section in `alm/release-and-lifecycle.md` + pattern dependency shape + exit cost |

No `NO`. The taxonomy is not too shallow.

### 20.3 Complexity — the eight required checks

| | Check | Verdict | Evidence |
|---|---|---|---|
| **A** | Does Options preload domain knowledge? | **NO** | §4.4; the `aisa-options` clause is unchanged; `decision-tree.md` §9 is unchanged; the `test_council_wiring.py` assertion still holds |
| **B** | Does a material D3 question have a clear pull target? | **YES** | 27 catalogued questions (§8), each with a single first target; the 12-concern map (§9) |
| **C** | Does answering one question usually require many unrelated files? | **NO** | One first pull; a second only where the first exposes a dependency. The three-file analytics case was designed out (§7.5) |
| **D** | Has canonical research been copied into runtime? | **NO** | §10 — every family lands in a unit, the decision model, a Step 5 template, or a reasoned exclusion. Runtime carries answer shapes; the corpus stays authoring-side |
| **E** | Has material architecture knowledge been deleted for context reduction? | **NO** | Nothing is retired outright (§2). The layer **gains** 19 subjects it could not previously answer (§3.5) |
| **F** | Does domain knowledge decide which option wins? | **NO** | §4.5; the branch declaration and the restated disqualification gates are deleted (§3.1); `store-selection` was renamed for exactly this reason (§7.4) |
| **G** | Can rich platform knowledge create comparator preference? | **NO** | §20.4; no alternatives file; the effort model is barred from S8; comparator semantics remain the frozen register's |
| **H** | Can the taxonomy be understood without a router? | **YES** | §19 — 15 of 15 discoverability rows pass; the mechanism is directory + filename + §0 |

### 20.4 The alternatives-symmetry rule

The pack knows far more about this platform than about any alternative. That asymmetry is **epistemic, not
preferential**, and Step 4 does three things with it:

1. **No alternatives knowledge files.** Writing SaaS, custom-stack, incumbent-platform or other-low-code
   depth the corpus does not contain would be invention — and *thin* alternative knowledge is worse than
   none, because a thin claim reads as an evaluated one.
2. **Depth on this platform may raise confidence about this platform's boundaries. It may never become a
   comparative claim.** Every unit's *What not to infer* heading carries the specific form: *"a documented
   boundary here is not evidence that another class does better."*
3. **Where comparative evidence is absent, the frozen comparator semantics are authoritative** — the
   default `COMPARATOR EVIDENCE ABSENT` marker in `outcome-classes.md` stands, and no domain unit may
   weaken it.

---

## 21. Exact Step 4B implementation scope

**Ordered, with dependencies. Step 4B does not begin before this design is approved.**

### 21.1 In scope

| # | Work | Depends on | Output |
|---:|---|---|---|
| 1 | Author `domain-knowledge/README.md` — the pull rule, the grade convention, the boundary line, the CRAFT rule | — | 1 file |
| 2 | **Per-number adjudication sweep** over the 13 current files: classify **every** numeral as *stable-retain* · *volatile-retain-stamped* · *register-owned* · *implementation trivia* · *unsupported-remove*, each verdict citing the canonical id that supports it, or the absence of one | 1 | Authoring-side table; the input to steps 3–6 |
| 3 | Author the 15 RESEARCH units against §7.2, the §4.2 unit contract and the §6 grade ordering | 2 | 15 files |
| 4 | Author the 10 CRAFT units: migrate, strip prices, strip dead branch vocabulary, add the CRAFT header and the cite-don't-assert rule | 2 | 10 files |
| 5 | Apply the §11 anti-pattern disposition; produce the **behaviour → single-home** table for all 68 entries | 3, 4 | Authoring-side table; notes inside units |
| 6 | Apply the §5 volatility stamps; verify every stamped figure names an existing register row; verify no conflicted figure is carried and no price appears anywhere | 3, 4 | Stamped files |
| 7 | Produce the per-file **provenance table** (§18.1) — the G1/G3/G7 gate object | 3, 4 | Authoring report section |
| 8 | Update `pack.yaml.domain_knowledge` to the new paths; keep the list a manifest, not a load order; no research id enters `pack.yaml` | 3, 4 | `pack.yaml`, `pack_version` bump |
| 9 | Consumer sweep and update — `aisa-blueprint` (`screen-consolidation-rules.md`, **hard contract**) · `aisa-simulate` (three paths) · `claude-design-brief.template.md` (the 4-row cross-reference table) · `library/kernel/blueprint-contract.md` (generic reference) · `.claude/agent-memory/_universal/solution-architect/anti-patterns.md` (**restates a threshold** — must point at `data/query-and-delegation.md` instead) · `.claude/agent-memory/_universal/compliance-officer/anti-patterns.md` · `docs/ARCHITECTURE.md` · `docs/PACK_AUTHORING.md` · `docs/ONBOARDING.md` | 8 | Updated consumers; zero stale paths |
| 10 | Mechanical tests extending `.claude/tests/`: no price token · no canonical research id in any runtime domain file · every stamped figure resolves to a register row · no obsolete branch name · every unit has §0 and a boundary line · no `craft/` file states a platform limit · every unit declared in `pack.yaml` exists and vice versa | 3–9 | Test additions |
| 11 | Step 4B report, with the §10 coverage accounting re-run against the authored files | 1–10 | `step-4b-domain-knowledge-implementation-report.md` |

### 21.2 Explicitly out of scope for Step 4B

`decision-tree.md` · `decision-model/*` · the Discovery layer (`question-bank.md`, `glossary.md`,
`extra_signals`) · the lens skills and personas · `architecture-templates/*` (**Step 5**) ·
`deliverable-templates/*` beyond the design-brief cross-reference table · `library/kernel/**` beyond the
blueprint-contract path reference · all canonical research.

### 21.3 Landing mechanics

`library/**` is deny-listed for `Write`/`Edit` and guarded by `pre-write-guard.py`. Files are authored in
the session scratchpad and copied in via `Bash` on the authoring branch, out-of-band per
`.claude/rules/library-readonly.md`. Nothing is committed without review.

### 21.4 Open questions carried into Step 4B

| # | Question | Proposed default |
|---|---|---|
| **Q4-01** | Does the team accept `provenance: CRAFT` on ten files, including the estimation model it uses commercially? | Yes — the label protects the research files' authority and costs the craft files nothing. Restates map Q-07 |
| **Q4-02** | Language. The decision layer is English; domain knowledge is currently mixed (`delivery-conventions.md` is `pt`, the rest `en`) | **English** for all RESEARCH units — they carry vendor terminology the corpus states in English. CRAFT units keep the language their consumers use. Restates map Q-02 |
| **Q4-03** | `craft/screen-consolidation-rules.md` moves path but keeps its filename, and `aisa-blueprint` names it as a hard contract | Update the skill in step 9 rather than leave the file at the old path. A stale hard contract is worse than a path change |
| **Q4-04** | Does the S8 bar on `craft/estimation-model.md` need to be machine-checkable, or is the stated rule enough? | Stated rule plus a test asserting the bar is documented in the file. A hard block would need a loader the pack does not have |
| **Q4-05** | `pack.yaml.epistemics.half_lives_override` is still empty, while the §5 stamps assume a decay class | Propose `plataforma-tecnica: 9 meses`, `financeiro: 3 meses` at step 8; validate at the first retro. Restates map Q-08 |

---

`STEP 4A — DOMAIN KNOWLEDGE MODEL: PASS`
`CURRENT DOMAIN FILES: 13`
`PROPOSED DOMAIN FILES: 26`
`CANONICAL RESEARCH MATERIAL ACCOUNTED FOR: YES`
`CANONICAL RESEARCH COPIED WHOLESALE TO RUNTIME: NO`
`MATERIAL D3 QUESTIONS HAVE CLEAR PULL TARGETS: YES`
`DOMAIN KNOWLEDGE PRELOADED IN OPTIONS: NO`
`ROUTER INTRODUCED: NO`
`STABLE/VOLATILE BOUNDARY DEFINED: YES`
`DECISION/ARCHITECTURE/IMPLEMENTATION BOUNDARY DEFINED: YES`
`ANTI-PATTERN DUPLICATION CONTROLLED: YES`
`LICENSING VOLATILITY CONTROLLED: YES`
`OPERABILITY DEPTH SUFFICIENT: YES`
`CROSS-DOMAIN COVERAGE SUFFICIENT: YES`
`DOMAIN KNOWLEDGE CAN SELECT WINNING OPTION: NO`
`PP KNOWLEDGE DEPTH CREATES COMPARATOR PREFERENCE: NO`
`PP RUNTIME FILES MODIFIED: 0`
`READY FOR STEP 4A REVIEW: YES`
