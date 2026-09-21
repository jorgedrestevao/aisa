# Step 5A — Architecture Template Runtime Model and Authoring Design

<!--
provenance: AUTHORING (design) · Step 5A
authored: 2026-09-04 · inputs: Step 3 (FROZEN), Step 4 (FROZEN), current runtime
Design only. No runtime file under library/ was modified by this step. The only write outside this
report was the documentation-only freeze marker appended to step-4c-domain-knowledge-semantic-gate-report.md.
-->

## 1. Purpose and doctrine

Step 5 converts a **defensible, already-justified** PP-containing decision into a reusable architecture
description. It does not decide anything.

```text
OPTIONS DECISION MODEL   → whether and where a PP-containing solution remains defensible
DOMAIN KNOWLEDGE         → mechanisms, constraints, boundaries, technical obligations
ARCHITECTURE PATTERN     → reusable composition of mechanisms + everything it imports
ARCHITECTURE TEMPLATE    → reusable output shape for an architecture already justified
```

The dependency runs downward only. Five prohibitions bind every template this model proposes; each is
restated as a gate check in §23:

1. A template never decides whether PP is the winning option, nor which outcome class applies.
2. A template never decides whether a requirement is material or a comparator superior.
3. A template never restates domain knowledge — it cites the unit that owns it.
4. A template never owns a platform number.
5. A template never selects itself. Selection is one recorded field, resolved once, by one include.

**What this step is actually repairing.** The current layer answers the question *"which of three
store-first branches did we pick?"* Step 3 deleted that question. The replacement question is *"for which
scope is a PP architecture authorized, what composition has been justified, and what did that composition
import?"* — three facts, none of which the current layer can express.

---

## 2. Current template inventory

Four files, 5.7 KB total. `README.md` is positioning, not a template; the runtime template count is **3**.

| File | Purpose | Activation | Required inputs | Output structure |
|---|---|---|---|---|
| `README.md` | Positioning: shapes are not the option space; reachability by outcome | n/a | n/a | Prose + reachability table |
| `sharepoint-first.md` | "Lighter in-platform shape" | `applies_to_branch: [sharepoint-first]` | `solution_name`, `entities_in_sharepoint`, `automation_flows`, `canvas_app_pages` | 5 headings, all free text |
| `dataverse-first.md` | "Relational in-platform shape" | `applies_to_branch: [dataverse-first]` | `solution_name`, `dataverse_tables`, `business_rules`, `model_driven_app_areas`, `security_roles` | 6 headings, all free text |
| `hybrid.md` | "In-platform split across two stores" | `applies_to_branch: [hybrid]` | `solution_name`, `dataverse_critical_entities`, `sharepoint_secondary_entities`, `canvas_app_pages`, `data_flow_diagram` | 6 headings, all free text |

**Per-file diagnosis.**

| Property | `sharepoint-first` | `dataverse-first` | `hybrid` |
|---|---|---|---|
| Duplicated knowledge | none (too thin to duplicate) | none | none |
| Hardcoded PP assumptions | store, surface **and** automation mechanism fixed in the filename's semantics | store + surface + security model fixed | two stores + surface fixed |
| Obsolete branch semantics | `applies_to_branch`, filename | same | same, plus the word *hybrid* colliding with outcome classes 3 and 4 |
| Acts as an architecture composition | no | no | no — a two-store split is a store decision, not a composition |
| Acts as a blueprint shape | partially — 5 headings | partially — 6 headings | partially — 6 headings |
| Contains decision logic | no (the Step 3B1 re-scope removed it) | no | no |
| Contains implementation craft | no | no | no |
| Contains volatile facts | no | no | no |
| Survives in the new model | **no** | **no** | **no** |

**Verdicts.** `README.md` **REWRITE**. `sharepoint-first.md` **RETIRE**. `dataverse-first.md` **RETIRE**.
`hybrid.md` **RETIRE** (the authoring map's earlier `SPLIT` verdict is superseded: the two structurally
different hybrids are **scope pairs plus a boundary fragment**, not two shapes — §11, §12).

**Three defects the table understates.**

- **Product-named slots.** `entities_in_sharepoint`, `dataverse_tables`, `model_driven_app_areas` make the
  store and the surface part of the *slot name*. Changing the store changes the template; that is the
  combinatorial trap the commission warns about, already realised.
- **A second, drifting copy of the closed 14.** Each shape's front matter carries
  `available_after_outcome: [strong-fit, fit-with-constraints, platform-side-of-a-hybrid-scope-pair]`.
  The third value is **not an outcome class** — it is a scope-pair mechanic — and the first two are
  slugified renames of class 1 and class 2. Three files each hold an unversioned copy of a closed set that
  lives in `decision-model/outcome-classes.md`. The new model removes all three copies (§4).
- **Nothing carries an import.** Governance, ALM, cost, monitoring, recovery and operator appear in none of
  the three. That is precisely the content Step 4 identified as the most decision-bearing in
  `architecture/patterns.md` §3, and the content output shapes most often omit.

---

## 3. Current branch-model diagnosis (Q4-08)

**The producer emits a value its own authority no longer defines.** `aisa-decide` writes
`**Branch (if technology)**: <decision-tree branch>`; `decision-tree.md` §1 states it *"replaces the scored
three-branch tree"*. The field has no source.

**Full consumer chain of `branch`:**

| Consumer | Use |
|---|---|
| `.claude/skills/aisa-decide/SKILL.md` | writes the field into the `D-NNN` block; renders `(<branch> · effort · reversibility)` in the option list |
| `.claude/skills/aisa-blueprint/SKILL.md` | pre-flight requires *"a final D-NNN with a technology branch"*; input `architecture-templates/<branch>.md`; step 2 *"platform limits for the branch"*; hard rule 4 *"branch-anchored"* vendor naming |
| `library/kernel/blueprint-contract.md` | schema key `branch` |
| `library/packs/pp/deliverable-templates/solution-blueprint.template.md` | `chosen_architecture: decisions.md# D-NNN — Branch (if technology)` + `{{>> architecture-templates/{{chosen_architecture}}.md}}` |
| `library/packs/pp/deliverable-templates/claude-design-brief.template.md` | same slot + same include |
| `library/packs/pp/deliverable-templates/implementation-spec.template.md` | same slot, no include |
| `library/kernel/synthesis-templates/architecture-story.template.md` | source `architecture-templates/<branch>.md`; prompt *"state the branch from decision-tree.md"* |
| `.claude/skills/aisa-synthesize/SKILL.md` | same path |
| `.claude/skills/aisa-render/SKILL.md` | input `architecture-templates/<branch>.md`; `applies_to` read from the `Branch` field |
| `.claude/skills/aisa-options/SKILL.md`, `aisa-simulate/SKILL.md` | render `<branch>` per option / *"constraint verdicts for its branch"* |

**Six defects, in dependency order.**

1. **Filename *is* the decision.** Template selection is a 3-value enum resolved by string interpolation
   into a path. There is no field to inspect, no field to leave unresolved, and no field to version.
2. **Conflation.** One value simultaneously encodes store authority, application surface and split. A
   composition, a scope pair and an unresolved choice are all inexpressible.
3. **Options contamination.** `options.md` option lines carry `<branch>`, which presents store-first shapes
   as if they were option classes — the exact defect Step 3 exists to remove. This is the one place where
   the branch model still leaks *upward* into the frozen layer.
4. **Ten of fourteen outcome classes are unrepresentable.** Classes 3, 4 (scope pairs), 5, 6, 7, 8, 9, 10,
   11, 12, 13, 14 have no expression; the model implicitly assumes class 1 or 2.
5. **Non-PP technology decisions break the include.** A decision for custom development, cloud-native
   assembly or buy is a *technology* decision by `applies_to`, so `solution-blueprint` renders and the
   include `architecture-templates/{{chosen_architecture}}.md` resolves to nothing.
6. **`applies_to: [technology]` is the wrong discriminator.** The question a deliverable containing an
   architecture section must ask is *"is a PP architecture authorized for at least one scope?"*, not *"was
   the decision technological?"*

**Interaction with the contracts.** `blueprint-contract.md` is otherwise platform-agnostic and correct: its
provenance rule (`su_refs` everywhere), `excluded_from_ui` first-class, cap-violations-become-Conflicted and
draft-mode rules all survive unchanged. Only the `branch` key is affected. `render-contract.md` needs no new
capability: nested slots inside include paths already work, and the render layer is **skill-executed**, so a
"repeat this block per component" instruction is sufficient — no template-inheritance framework (§12).

---

## 4. Outcome-class reachability — the blueprint entry gate

Derived from `decision-model/outcome-classes.md` §1, §1.1, §1.2, §1.3, §2, §3. **Outcome → permission and
scope to architect. Never outcome → template.**

> **Corrected 2026-09-04 (§27.1). Outcome reachability is necessary and not sufficient.**
>
> ```text
> architecture authorization = outcome reachability × pack architectability
> ```
>
> The *"Architecture reachable?"* column below states **outcome reachability only** — whether the emitted
> outcome leaves any architecture permissible for a scope. A PP architecture is authorized only where the
> **selected** solution for that scope is also something this pack has the authority and knowledge to
> architect (§27.2). A positive generic outcome over a custom-only, packaged, cloud-native-only, incumbent
> or other-platform solution is reachable and **not** architectable here.

| # | Class | Architecture reachable? | Scope | Mandatory consequence for the architecture output |
|---:|---|---|---|---|
| 1 | Strong fit | **reachable** — authorized **only if** the selected option is PP-containing and architectable (§27.2) | the named scope | Render the class's *no documented constraint violated* sentence as the decision basis; never as endorsement |
| 2 | Fit with constraints | **reachable** — same architectability condition as class 1 | the named scope | Every condition carried as *condition — owner — funded? — by when*; an unowned or unfunded condition ⇒ an open architecture item, never a silent assumption. Tripwire metric where one applies |
| 3 | Hybrid with cloud-native services | **yes, bounded** | the application scope only | The named responsibility gets a **boundary fragment**, never a PP design. The S7 gate record (operator · support · skills · cross-boundary release owner · maturity) is required content |
| 4 | Hybrid with the incumbent system | **yes, bounded** | the experience / human-workflow scope only | Boundary fragment for the authority responsibility, carrying `INCUMBENT FIT UNEVALUATED`. The incumbent's internals are not designed here |
| 5 | Poor fit — excluded for this scope | **no** for that scope | — | No PP architecture. If another scope carries an emitted 1/2/3/4/13(a) pair, architect that scope only |
| 6 | Excluded for this responsibility | **no** for the named responsibility | surrounding scope only where a pair was **emitted** | Never infer the surrounding scope's authorization from the exclusion of the responsibility |
| 7 | Economically infeasible / unattractive | **no** | — | The subtype's discriminator is repeated verbatim. Funding a mandated control can restore viability — that is an Options re-run, never a template-layer lift |
| 8 | Candidate set — comparative fit unevaluated | **no** | — | Not an authorization; it is the terminal render of 5/6/7/14/13(b). Its output belongs to the executive / discovery deliverables |
| 9 | Deployment model excludes this platform | **no** | — | The one class that may name a comparator; both halves of the sentence are repeated, and no PP architecture follows |
| 10 | Process redesign / no new application | **no** | — | No application exists to architect |
| 11 | Do nothing / defer | **no** | — | Revisit condition recorded; no architecture |
| 12 | Decision blocked | **no** | — | Architecture is **prohibited**, not deferred-with-a-draft. Draft mode (`/blueprint --option`) remains legitimate *before* the decision, for `/simulate` only |
| 13(a) | Alternative sufficient — documented sufficiency | **reachable, and never automatic** — authorized only where the sufficient existing capability is explicitly inside this pack's architectable scope (§27.2) | the named shape | Where authorized: `experience.mode: inherited`. Where **not** architectable: no PP architecture is produced, and documented sufficiency, *this platform is not excluded* and the **graduation trigger** are preserved in the decision and deliverable layers. The trigger is mandatory either way; without it the output is malformed |
| 13(b) | Alternative sufficient — candidate | **no** | — | The answer is another class; followed by class 8 |
| 14 | In-place remediation unavailable — migration required | **no** on its own | — | Terminates in class 8. A rebuilt PP solution is a legitimate candidate, but it must arrive as a newly emitted 1/2 pair. Where it does, the core's *replacement of an existing artefact* conditional section is engaged |

**Authorization vocabulary — three values, not fourteen.** Each requires **both** factors.

```text
authorized          ← an emitted class 1, 2 or 13(a) pair for this scope
                      AND the selected solution for that scope is architectable by this pack
authorized-bounded  ← an emitted class 3 or 4 pair, or class 6's surrounding scope
                      AND the PP-owned side is architectable; the far side never is
not-authorized      ← the outcome is unreachable, OR the selected solution is not architectable here.
                      Carries the emitted outcome sentence, plus the architectability reason where that
                      is what failed — the two reasons are never merged
```

**Two rules that keep this a gate and not a router.**

- **No template file lists an outcome class.** The reachability table above lives in one place —
  `architecture-templates/README.md` — and the *value* lives in the engagement's architecture record. The
  three copies in current front matter are deleted.
- **Authorization is read, never derived.** The template layer cannot compute an authorization from
  evidence, cannot upgrade `authorized-bounded` to `authorized`, and cannot emit *decision blocked* — only
  repeat one that Options emitted.

---

## 5. Decision-to-blueprint handoff

**Minimum that must already exist** before architecture work begins (all produced by Step 3 / `/decide`,
none invented here):

| Fact | Source | Why blocking |
|---|---|---|
| `(scope, outcome class)` pairs, uncollapsed | `options.md` → `decisions.md` | The authorization itself |
| The decided option's **class** in plain language | `decisions.md` | Distinguishes a PP-containing answer from *extend the existing system*, *custom*, *cloud-native*, *incumbent*, *another low-code platform*, *buy* |
| Residency / region and deployment-model verdict | SU `Confirmed` (S2 absolutes) | Fixed at environment creation, upstream of every architecture choice |
| Identity class of the audience | SU (C3) | Decides which surfaces are reachable at all |
| Authorization enforcement point | SU (C6) | Decides the store's role and the security section's form |
| Mandated controls and their funding state | SU (C6, C11) | An unfunded mandate is class 7, not an architecture risk |
| Proof requirement level (V1–V4) and its owner | `options.md` (S9) | Carried, never re-derived at architecture altitude |
| Blocking-set state for this scope | the engagement's rows against `decision-model/blocking-set.md` | An engaged blocking entry means class 12 |
| Accepted risks, preconditions, tripwires | `decisions.md` D-NNN | Become architecture obligations, not new findings |

**Legitimately still open at handoff — and blueprinting proceeds:** store selection where two stores both
satisfy every documented constraint; composition rung within an authorized escalation; surface variant
within a shape; screen architecture; environment count; monitoring implementation; naming.

**Requires additional technical analysis, and the section says so:** any sizing that rests on the
`CONFLICTED` per-mechanism ceiling; any measurement obligation at V2+; delegation behaviour on a contested
access path; write-through virtualization support.

**Prevents a section being finalized:** an open Unknown that decides store authority, the authorization
enforcement point, the identity class, or whether a responsibility leaves the platform. These are
**structural** open choices (§18) and they block *approval*, not *production*.

**May remain open while blueprinting proceeds:** every non-structural open choice, and every proof
obligation whose level, method, owner and funding are named.

---

## 6. Architecture-selection contract — the replacement for `technology branch`

One block, in the artefact that already exists (`_blueprint/ux-blueprint_v<NN>.yaml`). No new file, no new
state machine, no second decision model, no scoring, no restatement of the 12 concerns or S0–S9.

```yaml
architecture:                      # replaces `branch`
  scope: <the named scope, verbatim from the emitted (scope, outcome) pair>
  authorization: authorized | authorized-bounded | not-authorized
  authorization_basis: <the emitted outcome sentence, verbatim>   # never re-derived
  architectability_basis: <why the selected solution is architectable by this pack>  # §27.2
  experience:                      # ONE optional architectural dimension — not a shape, not a branch
    mode: none | owned-internal | owned-external | inherited
    primary_surface: <a surface named in application/application-surfaces.md §3> | null
                                   # required only where mode != none; null where mode == none
  record_authority:                # 0..N — never one global store value; empty needs a rationale (§27.5)
    - domain: <entity or entity group>
      authority: <governed relational store | list/library store | relational via connector | external system of record>
      access_mode: owned | virtualized | replicated | keep-in-place
      su_refs: [...]
  compositions:                    # 0..N — names from architecture/patterns.md §5
    - component: <local, human-readable component name, unique within this scope>   # required (§28.1)
      pattern: <direct | api-mediated | api-facade | event-driven | queue-based |
                hybrid-low-code-pro-code | background-processing | data-virtualization |
                data-replication | enterprise-boundary>
      forced_by: <the named requirement that forced this rung>     # mandatory
      boundary: in-platform | outside-platform
      owner: <named team or role> | UNKNOWN
      enclosing: true|false        # enterprise-boundary only
  relocated_responsibilities:      # 0..N — the scope-pair mechanism
    - responsibility: <name — unique within this scope; it is the identity (§28.2)>
      owner: <incumbent system | cloud-native services | named external team>
      outcome_basis: <the class 3 or class 4 sentence, verbatim>
      markers: [INCUMBENT FIT UNEVALUATED, ...]
      gates_recorded: [operator, support, skills, cross-boundary-release-owner, maturity]
  proof_obligations:               # carried from S9, never re-derived
    - claim: <what is being committed to>
      level: V1|V2|V3|V4
      method: <what will be run>
      owner: <role>
      funded: yes|no
  open_architecture_choices:       # 0..N
    - choice: <what is undecided>
      structural: true|false       # true ⇒ blocks approval (§18, §26 of the commission)
      would_be_settled_by: <the fact, measurement or owner decision>
      su_ref: <U-NNN where one was opened>
```

**Minimum required fields.** `scope`, `authorization`, `authorization_basis`, `architectability_basis`,
`experience.mode`, `compositions[]` (each with `component` **and** `forced_by`),
`relocated_responsibilities[]` (may be empty; `responsibility` unique within the scope),
`proof_obligations[]`, `open_architecture_choices[]` (may be empty). `record_authority[]` is required as a
key and **may be empty**, with an affirmative rationale (§27.5). `experience.primary_surface` is required
only where `experience.mode != none`; where the mode is `none` it is `null` and that is a **finalized
architectural fact, never `unresolved`**. `imports` is deliberately **not** a field: imports are derived
per component and carried structurally by the fragment (§10), so they cannot be declared satisfied by fiat.

**Where each field is initialized.** `scope`, `authorization_basis`, `proof_obligations[]` and the decision
conditions are **serialized by `/decide` from already-decided facts**. `authorization` and
`architectability_basis` are **initialized mechanically at `/blueprint` entry** (§20, §27.3) — not a new
decision, and not `aisa-decide`'s to emit. Everything else is architecture work.

**What the contract deliberately does not contain:** any option class other than as `authorization_basis`
prose; any fit score; any comparator statement; any outcome-class list; any platform number; any store or
surface preference; any stage or concern identifier.

---

## 7. Architecture pattern → template mapping

Survival test applied to each of the ten canonical compositions: *would a separate template materially
change the structure of the blueprint that must be produced?*

| Composition | Distinct output shape? | How it is carried |
|---|---|---|
| Direct integration | no | A row in the core's integration table. Adds no import, so no fragment |
| API-mediated | no | Boundary fragment (`outside-platform`) |
| API facade / BFF | no | Boundary fragment + the composed-backends and single-point-of-failure rows |
| Event-driven | no | Boundary fragment |
| Queue-based | no | Boundary fragment |
| Hybrid low-code + pro-code | no | Boundary fragment; usually also a `relocated_responsibility` |
| Background processing | no | Boundary fragment; the **status resource** is a mandatory obligation row |
| Data virtualization | no | `access_mode: virtualized` + fragment; forfeits land in the store and security sections, irreversibility in the irreversible-choices section |
| Data replication | no | `access_mode: replicated` + fragment; **reconciliation owner** mandatory |
| Enterprise boundary | no | Fragment with `enclosing: true` — it encloses the others rather than replacing them |

**Ten canonical patterns → zero new templates.** Every one is an instance of one fragment with typed
content. Composition of patterns (`patterns.md` §6 documents seven pairings) is *N fragment instances*, and
their imports accumulate rather than merge — which the fragment enforces by existing once per component.

---

## 8. No template per product

Tested explicitly against the products named in the commission:

| Named thing | Separate template? | Why |
|---|---|---|
| Governed relational store (Dataverse) | no | A `record_authority.authority` value. Same responsibilities: authority, grain, integrity, retention, residency |
| List / library store (SharePoint) | no | Same. Its *forfeits* differ (no column security, no multi-row atomicity, versioning-not-audit) — different resolved content in the same section |
| Relational via connector (Azure SQL) | no | Same. Its identity model is the structural difference, and identity already has its own required section |
| Power Automate | no | Automation responsibilities section; mechanism choice is content |
| Custom connectors | no | Fragment where the component sits outside; otherwise an integration row |
| Brokers | no | Fragment (`queue-based` / `event-driven`) |
| External workers | no | Fragment (`hybrid-low-code-pro-code`) |

**The governing principle, stated as the test 5C will run:** *same architectural responsibilities +
different store or mechanism implementation ⇒ same output shape, different resolved content.* A separate
template is justified only where the **set of required sections** changes — which happens exactly three
times (§9).

---

## 9. Re-evaluation of the Step 4A provisional shapes

The provisional list mixed four taxonomy levels — surface (`canvas`, `model-driven`), store (`dataverse`),
audience (`external-audience`) and composition (`hybrid-*`) — at one level. That mixing is why the
provisional count was seven.

| Provisional candidate | Verdict | Reason |
|---|---|---|
| `canvas-application` | **merge** → experience mode `owned-internal` | Surface is a slot. Personas, screens, RBAC, navigation, access paths, offline, device are the same sections |
| `model-driven-application` | **merge** → experience mode `owned-internal` | Areas / forms / views are screens with a different pattern from the pack catalogue; the store prerequisite is store-section content |
| `dataverse-application` | **reject as a shape** | The name encodes a store choice. Becomes `record_authority.authority` |
| `collaboration-surface` | **rename + keep** → experience mode `inherited` | The structural property is not "collaboration": it is that access, lifecycle and capacity are **inherited from a host**, and growth is a one-way graduation |
| `external-audience-site` | **keep** → experience mode `owned-external` | Genuinely different required sections (§11): external identity prerequisite, table-permission × web-role model, public exposure, cache and freshness semantics, accessibility attestation. Build model (low-code / code-first) is a slot |
| `hybrid-cloud-native` | **reject as a shape** | Class 3 is a scope pair. Composition + fragment |
| `hybrid-enterprise-boundary` | **reject as a shape** | Class 4 is a scope pair. Composition + fragment |
| `non-technology-intervention`, `candidate-set` (authoring map §3.5) | **reject as architecture templates** | Classes 8, 10 and 11 authorize no architecture. Their rendering belongs to the executive / discovery deliverables (Step 6) |

**The single fork axis that produces the surviving three** — corrected 2026-09-04 (§27.4): these three are
**experience modes**, not whole-architecture shapes, and the axis opens with a third question that admits a
headless architecture.

```text
Is there a human-facing surface in this architecture at all?
  no  → experience.mode: none          (headless — zero experience fragments)
  yes → does the solution own its own access model, lifecycle and capacity?
          no  → experience.mode: inherited
          yes → is any part of the audience outside the directory?
                  yes → experience.mode: owned-external
                  no  → experience.mode: owned-internal
```

The three provisional candidates below therefore survive as **experience fragments**, and the merge/reject
verdicts in the table are unaffected — only their altitude changes.

Embedded surfaces (list-customised form, report visual, chat tab) fold into `inherited`: access
inherited from the host, no independent lifecycle, no portability. Branded native wrapping and code apps
fold into `owned-internal` as `primary_surface` values with their own forfeits.

---

## 10. Imported-obligation carriage — the mandatory mechanism

Step 4 established that a composition's **imports** are its most decision-bearing content
(`architecture/patterns.md` §3, six channels). The carriage mechanism is structural, not editorial:

```text
for every entry in compositions[] with boundary: outside-platform, or any escalation beyond `direct`,
and for every entry in relocated_responsibilities[]
  → one instance of fragment-boundary-and-imports.md
  → each instance carries all six channels
  → a channel is either populated, or marked `not engaged — <reason>`
```

| Channel | What the instance must state |
|---|---|
| **Governance** | The new controlled asset, who may create and change it, who classifies its data, and **which platform controls stop applying at its edge** |
| **ALM** | How many release routes now exist, which contract must stay version-compatible, what is rebound after each deployment |
| **Cost** | The new meters and the population each is charged against (drivers only — no prices) |
| **Monitoring** | The new health signal, where its failures land, and the correlation the design must generate itself |
| **Recovery** | What happens in what order after a restore of any participant, and **who reconciles** |
| **Operator** | Who is paged, by name or role |

**Two hard rules.**

1. **Silent disappearance is a defect, and it is testable.** The 5C check is structural: one instance per
   qualifying component, six channel rows per instance, `not engaged` requiring a reason. It does not
   require every instance to be full — it forbids a channel from being absent.
2. **`operator: UNKNOWN` is not a risk row.** `patterns.md` §7 states the composition is *unavailable
   because no operator exists* — a capability fact about the design. The template surfaces it as a
   **structural** open architecture choice (blocking approval) and cross-references the honest output the
   pattern file already prescribes: the simpler composition plus a tripwire on the metric that would force
   the move. The template states none of that as its own judgement.

---

## 11. Common architecture blueprint contract

**COMMON REQUIRED — eleven sections.** Every PP-containing blueprint, headless or not. **A4 moved to
COMMON CONDITIONAL by §27.6**: it is engaged only where `experience.mode != none`. A7 stays **common** —
a headless architecture still has identity, trust boundaries and an authorization enforcement point
(§27.7).

| # | Section | Content | Shape-specific body? |
|---:|---|---|---|
| **A1** | Authorization and scope | The `(scope, outcome)` pairs verbatim; the decided option class; the D-NNN; what is authorized and what is explicitly not | no |
| **A2** | Architecture intent | The requirement each structural choice answers; the simplest-composition default and, per escalation, the requirement that forced it | no |
| **A3** | Context and boundaries | The required boundary table (§17) + trust boundaries + what sits inside / outside platform governance | no |
| ~~A4~~ | *moved to COMMON CONDITIONAL* — Application and surface responsibilities | Surface, its forfeits, what the surface is responsible for; handoff to the screen architecture | rendered by the experience fragment |
| **A5** | Data authority and stores | Per domain: authority, store role, access mode, grain, residency, retention, forfeits. **May be an affirmative empty set** (§27.5) | no (content varies) |
| **A6** | Automation and integration responsibilities | Per stream: mechanism class, guarantee, failure semantics, idempotency basis. Explicit `(none)`. **The whole architecture where the mode is `none`** | no |
| **A7** | Identity and authorization enforcement point | Identity class **or service / managed / connection identity**; the enforcement plane; trust boundary; secret and certificate custody where material; the role / permission model where a human audience exists | no — **common, never owned by an experience fragment**; a fragment may only specialize the human-user part |
| **A8** | Environment, governance and release topology | Environments, residency binding, policy plane, release route(s), what is managed-environment-gated | the **inherited** form comes from the inherited experience fragment |
| **A9** | Irreversible choices and exit | Ownership type, publisher, region / residency, first-party app installation, control generation, one-way graduations, virtualization modelling, exit cost | no |
| **A10** | Operability, support and named ownership | Named operator; support route; monitoring and alert ownership; recovery order and reconciler; what "accepted" means as evidence | no |
| **A11** | Economics and entitlement consequences | Entitlement class per audience, affected population, meters engaged, growth driver at horizon. **No prices** | no |
| **A12** | Proof obligations and epistemic ledger | V1–V4 obligations with method / owner / funding; Assumed / Unknown / Conflicted / Risky rows the architecture rests on; volatile values with `verificado_em` + `validade`; open architecture choices | no |

**COMMON CONDITIONAL — engaged only when its trigger holds.**

| Section | Engaged when |
|---|---|
| **A4 — application and surface responsibilities** | `experience.mode != none` — rendered by the matching experience fragment (§27.6) |
| Imported obligations per boundary component | any qualifying component (§10) — one instance each |
| Scope ownership | more than one `(scope, outcome)` pair exists (§12) |
| Analytical / reporting responsibility | reporting forces a second store or a copy |
| Offline and device capability | a named offline depth is required |
| Replacement of an existing artefact | the authorized scope replaces an artefact that reached class 14 |
| Component / sequence diagram | a composed or asynchronous path exists (§17) |
| Candidate architectures | a structural open choice remains (§18) |

**EXPERIENCE-FRAGMENT-SPECIFIC** (was *shape-specific*; §27.4). The A4 body, the human-user part of A7, the
A8 inherited form, plus:

- `owned-internal`: delegation-safe access paths per surface; distribution; offline depth; device
  capability; the forfeits of the chosen surface.
- `owned-external`: the external identity provider as a **prerequisite** (own tenant, cost, operating
  burden); table-permission × web-role model, deny-by-default; anonymous exposure and self-registration
  defaults; cache and freshness semantics (writes made outside the site are never guaranteed to be
  immediate); accessibility conformance basis; localization; build-model forfeits.
- `inherited`: the host and what access is inherited from it; the capacity ceiling as an engagement-verified
  value with its date; the **mandatory graduation trigger**; what is forfeited (interface access,
  extensions, audit, column security, offline, solution portability); the explicit statement that no
  independent environment or release topology exists, and why that is a choice.
- `none`: **no fragment.** The architecture is A1–A3, A5–A12 plus its boundary fragments. No application
  section is synthesized, and no surface is reported as `unresolved`.

**Rejected as ceremony.** A standalone "performance" section (its content is A12's proof obligations plus
A6's guarantees), a standalone "risk register" (D-NNN owns accepted risks; `patterns.md` owns pattern
risks), and a standalone "alternatives considered" section (Options owns it; the deliverable already has
the slot).

---

## 12. Template composition and scope pairs

**Chosen composition: one base + fragments, with a fixed entry point.**

```text
architecture-core.md                                   ← the entry point. Fixed path, always
  {{>> fragment-experience-<experience.mode>.md}}      ← ZERO or one, per §27.8
  {{>> fragment-boundary-and-imports.md}}              ← zero or more instances, one per component
```

Corrected 2026-09-04 (§27.8): the core includes **zero or one** experience fragment — `none` includes none —
and the include controls **only experience-section rendering**. It selects no architecture.

> **`experience.mode: none` execution** (§28.4). The render skill performs **zero** experience-fragment
> includes. It must **not** attempt to resolve `fragment-experience-none.md` — that file intentionally does
> not exist. No placeholder, no render gap, no missing-template warning, no *surface unresolved*. This is a
> finalized **not applicable** condition, and §18's *not applicable* class is what logs it: a skip with a
> reason, never a gap.

Two consequences that matter more than the file count:

- **Template selection disappears from every caller.** `aisa-blueprint`, `aisa-render`, `aisa-synthesize`
  and the deliverable templates all reference the same fixed path, `architecture-core.md`. The one
  interpolation left in the system is inside the core, driven by one recorded field. That is why the design
  needs no router.
- **No inheritance framework and no loop primitive.** The render layer is skill-executed, so the core
  carries the repeat instruction **once** and the skill performs the iteration from recorded data. The
  binding execution semantics and the component-identity rule that makes *N components ⇒ exactly N
  instances* testable are in §27.9–§27.10. Nested slots inside include paths already work today
  (`solution-blueprint` does it), so `render-contract.md` needs no new capability.

**Scope pairs.** `A1` renders the pairs; the conditional *scope ownership* section renders the table:

| Responsibility | Owner | Outcome basis | Described here? |
|---|---|---|---|
| Application / experience | this platform | class 1/2/3/4 sentence | yes — A4…A12 |
| Reporting / analytical | external | class 3 or 6 sentence | no — one fragment instance, plus what this pack does **not** know about it |
| Integration / authority | incumbent | class 4 sentence + `INCUMBENT FIT UNEVALUATED` | no — one fragment instance |

The rule: **a relocated responsibility gets a boundary and an owner, never a PP design.** The pack has no
comparator evidence about the far side and must not draw one. Collapsing the pairs into a single template
name is the failure mode this replaces — no `hybrid` shape exists, so it cannot recur.

---

## 13. Evidence and epistemic handling

The kernel's five states survive unchanged into the architecture output:

| State | Rendering rule |
|---|---|
| `Confirmed` | Rendered as fact **with** `verificado_em` / `validade`; an expired row renders as a re-verification obligation, not as fact |
| `Assumed` | Rendered as *assumed*, with its basis and validity. **An architecture section may never promote it** |
| `Unknown` | Never filled. Becomes an `open_architecture_choices` entry; `structural: true` where it decides shape, store authority, enforcement point or whether a responsibility leaves the platform |
| `Conflicted` | The conflict is the content. Neither figure is carried. Where sizing rests on it, the output is a proof obligation (typically V3) — the number is not rendered on either side |
| `Risky` | Carried in A10 / A12 with the accepted-risk id from the D-NNN |

**Volatile values.** The template structure never owns a number. Where a value is needed, the slot resolves
to the engagement's verified SU row and renders `value · verificado_em · validade · re-verify trigger`; where
no verified row exists, it renders the verification obligation instead. The stable explanation stays in
domain knowledge and is cited, never copied. `decision-model/volatility-register.md` remains the owner of
*that a fact is volatile*.

---

## 14. Domain Knowledge pull behaviour during blueprinting

**The Step 4C pull discipline survives, with a wider grade window and no bundle.**

```text
architecture responsibility being described
  → pull ONE relevant knowledge unit
  → read its decision-grade and architecture-grade sections
  → populate the corresponding section
  → follow a second dependency ONLY where the first exposes a material import
```

**Grade window.** `/blueprint` and the architecture render may read **decision-grade and
architecture-grade** sections. Reading decision-grade content is necessary, not a licence to re-decide:
only seven sections across four units are tagged `architecture-grade`, and the composing content lives in
the decision-grade bodies and the *Consequences elsewhere* sections. The prohibition is on **re-running
selection**, not on reading.

| Section | First pull | Legitimate second |
|---|---|---|
| A4 surface | `application/application-surfaces.md` §3, §6, §7 | `craft/screen-*` (CRAFT, §15) |
| A5 stores | `data/store-boundaries.md` §3, §4, §7, §8 | the specific store unit, only where a boundary is contested |
| A5 access paths | `data/query-and-delegation.md` §10, §11 | — |
| A6 automation | `automation/automation-mechanisms.md` §7, §12 | — |
| A6 integration | `integration/integration-mechanisms.md` §7, §12, §13 | `architecture/patterns.md` where a rung is engaged |
| A7 identity / authorization | `security/security-controls.md` §3, §6, §7 | the store unit, for grain |
| A8 governance / environments | `governance/governance-and-environments.md` §6, §7, §8 | `alm/release-and-lifecycle.md` §3, §10 |
| A9 irreversible | the unit that owns each choice (`security` §11, `alm` §11, `data/dataverse` §4, `governance` §7) | — |
| A10 operability | `operations/operability-and-support.md` §4, §6, §11, §12 | — |
| A11 economics | `economics/licensing-and-cost-drivers.md` §3, §4, §5, §7 | — |
| A12 proof | `performance/performance-and-scale.md` §10 | — |
| Fragment | `architecture/patterns.md` §3 + **the one** composition in §5 | the mechanism unit behind it |

**Forbidden:** preloading the 15 units; an "architecture knowledge bundle"; opening `patterns.md` §5 in full
to survey the ten; a routing table keyed by section. **Budget:** median 1 unit per section, maximum 2; the
5C gate counts pulls per fixture exactly as 4C did.

---

## 15. CRAFT boundary during blueprinting

Unlike Options, blueprinting may consume CRAFT — for implementation-facing shape only.

```text
RESEARCH             → establishes the technical boundary
architecture pattern → establishes the composition and its imports
CRAFT                → shapes implementation-facing blueprint detail
```

| CRAFT unit | Permitted use | Never |
|---|---|---|
| `craft/screen-consolidation-rules.md` | A4 screen architecture — the named contract, unchanged | — |
| `craft/screen-patterns.md` | A4 pattern catalogue and density | asserting a platform limit |
| `craft/security-craft.md` | the **form** of the role and permission matrix in A7 | which control exists, or where it takes effect (`security/security-controls.md`) |
| `craft/sql-delivery-conventions.md` | A5 layering and naming where the store is relational-via-connector | tiers, limits, throughput (`data/azure-sql.md`) |
| `craft/delivery-conventions.md` | A8 naming and solution conventions | topology capability (`alm/`, `governance/`) |
| `craft/anonymization.md` | A5, only where a masking obligation exists | any platform claim |
| `craft/estimation-model.md` | **not in the architecture blueprint** — it carries its own comparative-economics prohibition | — |
| `craft/powerfx.md`, `craft/flow-craft.md`, `craft/excel-translation.md` | implementation altitude — downstream deliverables | — |

**Hard rule.** `CRAFT heuristic → selects architecture` is forbidden. CRAFT may not set the shape, the store
authority, the composition, an authorization value or a proof level. Where CRAFT and a RESEARCH unit
disagree, RESEARCH wins and the CRAFT statement is a defect to report.

---

## 16. Blueprint vs implementation altitude

| In the architecture blueprint | Downstream (`implementation-spec`, `claude-design-brief`, `craft/`) |
|---|---|
| Components and their responsibilities | Power Fx expressions |
| Authority per data domain; store role; access mode | Table-by-table schema, indexes, DDL, stored procedures |
| Data flow and trust boundaries | Flow action graphs and connector expressions |
| Deployment and environment topology | Pipeline definitions, environment-variable values |
| Major interfaces **with the guarantee each carries** | Payload contracts field by field |
| Ownership, operator, support route | Runbook steps |
| Constraints engaged and forfeits accepted | Workarounds for each |
| Proof obligations with method and fidelity | Test cases |
| Irreversible choices | Migration scripts |
| Screen architecture handoff (patterns, personas, exclusions) | Pixel-level UX, component trees |

**Boundary test:** *would changing this invalidate the architecture, or only the build?* Only the build ⇒
downstream.

---

## 17. Diagram contract

The repository has **no diagram tooling**: no Mermaid anywhere, and `library/kernel/tools/dashboard.py`
renders fenced blocks as `<pre><code>` — plain text. The contract is therefore output-oriented and adds no
subsystem.

**REQUIRED — the boundary table.** Deterministic and testable; it replaces `hybrid.md`'s free-text
`data_flow_diagram` slot:

| Component | Role | Platform governance | Trust boundary crossed | Owner | Data classification |
|---|---|---|---|---|---|

Every component in `compositions[]`, `record_authority[]` and `relocated_responsibilities[]` must appear
exactly once. Nothing may appear in a diagram that is absent from this table.

**OPTIONAL — one context picture**, as a fenced block (Mermaid or ASCII, author's choice), constrained to:
nodes = table rows; edges labelled with direction **and** mechanism class; trust boundaries shown as
grouping or annotation; relocated responsibilities visually separated from the platform scope. It must
degrade to readable text, because that is how it will be displayed.

**OPTIONAL — one sequence sketch**, only where an asynchronous or composed path exists (a status resource, a
reconciliation pass, a saga with an external pivot).

No diagram is ever the authority: a statement that exists only in a diagram is not in the blueprint.

---

## 18. Render gaps and unresolved slots

Four classes, preserving epistemic meaning. **Not every missing slot is *decision blocked*.**

| Class | Trigger | Behaviour |
|---|---|---|
| **not applicable** | the section's trigger does not hold (no offline requirement; no boundary component) | Omit; log a **skip** with the reason. Not a gap |
| **optional** | optional section, no content | Omit |
| **architecture work item** | required section, resolvable by architecture work | Render the open item with owner and what would settle it; log to `render-gaps.md` as an architecture-open gap. **Not** decision blocked |
| **decision-blocking** | no architecture authorization for any scope, or an emitted class 12 | Render nothing architectural; render the emitted outcome sentence instead |

**Two rules.** *Decision blocked* is an **Options outcome class**; the render layer may repeat it and never
derive it. And a **structural** open architecture choice (§5) blocks *approval* of the blueprint, not its
production — reusing the existing mechanism (`open_questions` plus an Unknown / Conflicted SU row), with no
new flag and no new state.

---

## 19. Proposed architecture-template taxonomy

Corrected 2026-09-04 (§27.4, §27.8): the three surface files are **experience fragments**, not whole
architecture shapes. The runtime unit count is unchanged.

```text
library/packs/pp/architecture-templates/
  README.md                          REWRITE  (positioning · fork axis · reachability · architectability · legacy read)
  architecture-core.md               NEW      the entry point — A1…A12 + conditional sections
  fragment-experience-internal.md    NEW
  fragment-experience-external.md    NEW
  fragment-experience-inherited.md   NEW
  fragment-boundary-and-imports.md   NEW      one instance per boundary component
  (retired: sharepoint-first.md · dataverse-first.md · hybrid.md)
```

**Runtime template units: 5** (1 core + 3 experience fragments + 1 boundary fragment). `README.md` is
positioning, matching today's convention. **No headless-specific template exists**: a headless architecture
is `architecture-core` + zero experience fragments + zero or more boundary fragments.

| File | Purpose | Activation / reachability | Common vs fragment-specific | Patterns it can render | Required inputs | Conditional sections | Domain Knowledge dependencies | CRAFT dependencies | Explicitly does NOT decide |
|---|---|---|---|---|---|---|---|---|---|
| `architecture-core.md` | The architecture description skeleton, A1–A3 + A5–A12, with A4 delegated | Any scope whose authorization is `authorized` or `authorized-bounded` — reachability **×** architectability | Common. **Complete on its own for a headless architecture** | all ten, through fragments | the `architecture:` block + SU + `decisions.md` + `_synthesis/` | A4 · scope ownership · analytical responsibility · replacement of an existing artefact · diagrams · candidate architectures | one unit per section (§14) | none directly | authorization · architectability · outcome class · experience mode · materiality · comparator |
| `fragment-experience-internal.md` | The solution owns its surface and access lifecycle; audience is directory identity | `experience.mode: owned-internal` | Fragment: A4 body, human-user part of A7, A8 owned form | none of its own — compositions render through the boundary fragment | `primary_surface`, personas | offline and device · distribution | `application-surfaces.md`, `query-and-delegation.md` | `screen-consolidation-rules.md`, `screen-patterns.md`, `security-craft.md`, `delivery-conventions.md` | surface choice · store choice · whether a surface exists |
| `fragment-experience-external.md` | The solution owns a surface with an audience outside the directory | `experience.mode: owned-external` | Fragment: external identity prerequisite, web-role model, public exposure, cache / freshness, accessibility, localization | none of its own | `primary_surface` (build model), identity class, the external identity provider decision | anonymous exposure · localization · offline read | `application-surfaces.md` §3/§4, `governance-and-environments.md` §11, `security-controls.md` | `security-craft.md` | whether an external audience is in scope |
| `fragment-experience-inherited.md` | Access, lifecycle and capacity inherited from a host | `experience.mode: inherited` — typically an **architectable** class 13(a) | Fragment: host and inherited access, ceiling, **mandatory graduation trigger**, forfeits, no independent topology | none of its own | host surface, the seeded-entitlement basis, the graduation trigger, the ceiling as an engagement-verified value | replacement of an existing artefact | `application-surfaces.md` §3/§7, `data/sharepoint.md` §3/§8 | `delivery-conventions.md` | that this platform is excluded (it is not) · when to graduate · whether the capability is architectable here |
| `fragment-boundary-and-imports.md` | One boundary component: what it is, why, who owns it, six imports, gates | one instance per qualifying `compositions[]` / `relocated_responsibilities[]` entry | Common, repeated | all ten, one at a time | `pattern`, `forced_by`, `boundary`, `owner`, and the gate record for a relocation | `INCUMBENT FIT UNEVALUATED` marker · status resource · reconciliation owner · enclosing boundary | `architecture/patterns.md` §3 + the one composition | none | whether the composition is justified · whether the far side is a good design |

**No file is named after a product, a store or a vendor surface.** No file lists an outcome class. No file
contains a number.

---

## 20. `aisa-blueprint` target contract (design only)

**Removed:** the pre-flight requirement for *"a technology branch"*; the input
`architecture-templates/<branch>.md`; *"platform limits for the branch"*; the *"branch-anchored"* wording in
hard rule 4.

**Added — five changes, no routing framework:**

1. **Entry gate — four mechanical steps** (corrected 2026-09-04, §27.3):

   ```text
   read the decided (scope, outcome) pairs + the selected solution / composition, in plain language
     → check outcome reachability            (frozen outcome, §4)
     → check active-pack architectability     (frozen selected option × pack scope, §27.2)
     → initialize architecture.authorization + architectability_basis
   ```

   No scope architectable ⇒ **no PP architecture is created**; render or preserve the emitted decision
   basis where appropriate, with no inference about the far side and no comparator claim. One or more
   bounded scopes architectable ⇒ architect **only** those scopes. This initialization is **not a
   decision**: both inputs are frozen and the third is the active pack's own scope. Draft mode
   (`--option`) is unchanged and remains pre-decision only.
2. **New input field.** The `architecture:` block (§6), written into
   `_blueprint/ux-blueprint_v<NN>.yaml`, replacing `branch`. Facts serialized by `/decide` come from
   `decisions.md` (scope, outcome basis, proof obligations, conditions, accepted risks); `authorization`
   and `architectability_basis` are initialized here; everything else — experience mode, surface, record
   authority, compositions, relocations, open choices — is architecture work.
3. **Template selection.** None in the skill. The skill records `architecture.experience.mode`; the single
   include inside `architecture-core.md` resolves **zero or one** experience fragment at render time.
   Multi-pattern compositions are N boundary-fragment instances; scope pairs are N `(scope, outcome)`
   entries plus one boundary fragment per relocated responsibility. A headless architecture includes no
   experience fragment and requires no additional template.
4. **Unresolved architecture choices.** Recorded in `open_architecture_choices[]`; a `structural: true`
   entry blocks approval (§18). Vendor naming stays permitted post-Options, now anchored to the recorded
   architecture instead of a branch.
5. **Pull and CRAFT rules.** §14 and §15 stated in the skill body, replacing the flat input list.

**Backward compatibility.** One legacy engagement (`projects/cae-automation`) carries
`Branch (decision-tree): sharepoint-first` and an already-rendered, frozen `solution-blueprint_v01`.
Rendered versions are immutable, so nothing must be regenerated. A **read-compat paragraph** in the
rewritten `README.md` states the legacy mapping for a re-render — `sharepoint-first` and `hybrid` ⇒
`experience.mode: owned-internal` with list-store authority (`hybrid`: two `record_authority` entries),
`dataverse-first` ⇒ `experience.mode: owned-internal` with governed-store authority — and states that a
re-render must record the `architecture:` block properly rather than rely on the mapping. No code, no shim,
no router.

---

## 21. Kernel and blueprint-contract implications

`library/kernel/blueprint-contract.md` — **three minimal edits**, all platform-agnostic:

1. Schema row: `branch` → `architecture` (the block of §6, described generically: scope, authorization and
   its two bases, experience mode and optional surface, record authority, compositions, relocations, proof
   obligations, open choices). PP's experience-mode values, surface names and pattern names stay in the
   pack.
2. One entry-gate sentence: a blueprint requires an architecture authorization for at least one scope,
   **initialized at blueprint entry from the frozen outcome and the frozen selected option against the
   active pack's architecture scope**, and never derived, upgraded or downgraded thereafter. One further
   generic sentence: a blueprint need not contain a human-facing surface.
3. One approval rule: a structural open architecture choice blocks approval of a version.

`library/kernel/render-contract.md` — **two edits**: a deliverable containing an architecture sub-template
renders only where an architecture authorization exists for at least one scope (replacing the
`applies_to: [technology]` discriminator for that purpose); and the four render-gap classes of §18.

`library/kernel/synthesis-templates/architecture-story.template.md` + `.claude/skills/aisa-synthesize` —
the source path becomes the fixed `architecture-templates/architecture-core.md`; the prompt's *"state the
branch from decision-tree.md"* becomes *"state the authorized scope, its outcome basis, and the
composition"*.

**No PP taxonomy enters the kernel.** No new state, no new phase, no new artefact path, no new render
capability.

---

## 22. Deliverable and render compatibility (Step 6 inputs — nothing authored here)

| Deliverable | Architecture slots it will need | Feasible from this model |
|---|---|---|
| `solution-blueprint` | the whole core via the fixed include; `chosen_architecture` becomes the A2 intent paragraph plus the A1 basis, and its slot source moves off `decisions.md# Branch` | yes |
| `implementation-spec` | A5 (authority per domain, store, access mode) · A6 (mechanism, guarantee, idempotency basis, failure semantics) · A7 roles · A9 irreversible decisions · the fragment (reconciliation owner, release routes) · A12 proof fidelity. This confirms the authoring map's proposed new slots resolve from this layer | yes |
| `claude-design-brief` | A3 boundary table + A4 + the A7 form, addressed by heading rather than by a narrower template | yes |
| `estimate` | A11 drivers, affected population, meters engaged, environment population, fragment cost channels — no prices | yes |
| `executive-report` | the `(scope, outcome)` pairs uncollapsed · comparator status · the A2 intent sentence · A9 irreversible choices · A12 proof obligations · tripwires | yes |

`pack.yaml`'s `applies_to: [technology]` on `solution-blueprint`, `claude-design-brief` and
`implementation-spec` is the wrong discriminator (§3, defect 6) and is repaired by the render-contract rule
in §21 — not by adding a PP-specific value to the kernel vocabulary.

---

## 23. Regression fixture design (authoring-side; executed in 5B/5C, not here)

| Id | Scenario | What it must prove |
|---|---|---|
| **F-1** | List-based tracker with its native form; **architectable** class 13(a) | `experience.mode: inherited`; graduation trigger present; no environment / release topology section; *not excluded* statement present |
| **F-2** | Canvas surface over a list store, direct composition; class 2 | `experience.mode: owned-internal`; zero fragments; audit forfeit recorded; conditions carried with owner and funding |
| **F-3** | Record-centric app over the governed store, row + column security + audit; class 1 | `experience.mode: owned-internal`; irreversible block populated; managed-environment licence chain surfaced without a price |
| **F-4** | Canvas over relational-via-connector with an on-premises gateway | identity-model difference in A7; delegation-safe access paths; private-network mutual exclusion in A3 |
| **F-5** | Authenticated external customers, low-code build model | `experience.mode: owned-external`; external identity prerequisite; cache / freshness; anonymous defaults; accessibility basis |
| **F-6** | Application + analytical copy (data replication) | one fragment; reconciliation owner mandatory; second cost meter; *security does not travel into a copy* |
| **F-7** | Application + API-mediated tier | one fragment; second governance plane; second release route; contract compatibility |
| **F-8** | Application + queue + external worker, no named operator | three fragments; imports accumulate; `operator: UNKNOWN` ⇒ structural open choice plus a tripwire, and no design drawn |
| **F-9** | Virtualized external system of record | forfeits (audit, row security, offline, search) in A5 / A7; irreversible modelling in A9 |
| **F-10** | Scope pair, class 3 | application authorized, responsibility relocated; gates recorded; no PP design for the far side; pairs uncollapsed |
| **F-11** | Scope pair, class 4 | `INCUMBENT FIT UNEVALUATED` preserved; incumbent internals not designed |
| **F-12** | Two defensible architectures inside one authorized scope | structural open choice; approval refused; nothing silently chosen; no scoring |
| **F-13** | Class 12 decision blocked | no architecture rendered; the outcome sentence rendered; not a render gap |
| **F-14** | Class 5 excluded plus class 8 candidate set | no PP architecture; architecture-including deliverables skipped with a reason, not a gap |
| **F-15** | **Headless automation** — scheduled or triggered automation, no human-facing application | PP architecture authorized; `experience.mode: none`; `primary_surface: null`; **no A4 section**; A6/A7/A8/A10/A12 populated; **no `surface unresolved`**; no additional template |
| **F-16** | **Headless composed integration** — queue / event-driven plus an external worker, no surface | zero experience fragments; **multiple** boundary fragments; imports accumulate; service identity and trust boundary rendered in A7; operator obligation preserved |
| **F-17** | **Non-PP class 1/2** — a custom-only or packaged solution receives a positive generic outcome | outcome reachable **and** not architectable here ⇒ **no PP blueprint**; no PP template renders; the two reasons stated separately |
| **F-18** | **Class 13(a) outside pack architecture authority** | documented sufficiency, *this platform is not excluded* and the graduation trigger all preserved; **no PP architecture generated**; no inherited experience fragment rendered |
| **F-19** | **Repeated pattern, same owner** — two API-mediated integrations (ERP API, CRM API), both `pattern: api-mediated`, both owned by the Integration Team, distinct `component` names | **2 distinct composition components ⇒ 2 fragment instances**, each with its own six channels. Never collapsed to one on the shared pattern-plus-owner. Also proves the duplicate-name case fails rather than merging (§28.3) |

**Gate checks for 5C:** template-unit count and no product-named file · six-channel completeness per
fragment instance · **N unique components + M unique relocated responsibilities ⇒ exactly N + M instances**
(§28.3) · **duplicate component identity fails rather than merging** · no outcome-class list in any
template · no platform number in any template · no CRAFT authority claim · zero selection verdicts · pairs
never collapsed · entry gate honoured 19/19 · **architectability failure never renders a PP template** ·
**`experience.mode: none` performs zero experience includes, never opens `fragment-experience-none.md`,
emits no unresolved surface, no empty A4 and no render gap** · Domain Knowledge pulls per fixture
(median ≤ 1 per section, max 2) · legacy read-compat paragraph present.

---

## 24. Complexity test

| Question | Required | Result |
|---|---|---|
| Does the model recreate the old three branches? | NO | **NO** — one core; store and surface are slots; the three surface files are experience fragments, not branches (§27.4) |
| Does the model introduce a new application-only branch model? | NO | **NO** — `experience.mode: none` is a first-class finalized value (§27.4–§27.6) |
| Is a headless PP architecture representable? | YES | **YES** — core + zero experience fragments (§27.4, F-15, F-16) |
| Does an outcome class alone authorize a PP architecture? | NO | **NO** — reachability × architectability (§27.1–§27.2, F-17, F-18) |
| Does `aisa-decide` own the architecture authorization? | NO | **NO** — it serializes decided facts; authorization initializes at `/blueprint` entry (§27.3) |
| Does one product imply one template? | NO | **NO** — §8: seven products tested, zero templates |
| Does every canonical pattern require one template? | prefer NO | **NO** — ten patterns, one fragment |
| Can multi-pattern architectures be rendered? | YES | **YES** — N fragment instances, imports accumulate |
| Can scope pairs be rendered? | YES | **YES** — N `(scope, outcome)` pairs plus one fragment per relocation |
| Can templates be understood without a router? | YES | **YES** — one fixed entry point, one include driven by one field |
| Do templates repeat Domain Knowledge? | NO | **NO** — cite-only; strengths, weaknesses, risks, mechanisms and readings stay in Domain Knowledge |
| Do templates select winning options? | NO | **NO** — authorization is read, never derived or upgraded |
| Do imported obligations survive into the blueprint? | YES | **YES** — structural carriage, six channels, testable |
| Is repeatable fragment rendering deterministic and testable? | YES | **YES** — §27.9 execution semantics + §28.2 component identity (collision-safe) + §28.3 invariant |
| Can blueprinting selectively pull architecture knowledge? | YES | **YES** — one unit per section, second only on a material import |
| Does the design require a new state machine? | NO | **NO** — no new phase, state, artefact path or render capability |

---

## 25. Exact Step 5B implementation scope

**In scope — create / rewrite under `library/packs/pp/architecture-templates/`:**

1. `README.md` — rewrite: positioning (retained), the fork axis, the §4 reachability table as its single
   home, the "no outcome list in a template" rule, and the legacy read-compat paragraph.
2. `architecture-core.md` — A1–A3 + A5–A12, plus the eight conditional sections (A4 included), the two
   includes, and front matter (`required_slots`, `optional_slots`, `sub_templates`, `slot_sources`).
   Complete on its own for a headless architecture.
3. `fragment-experience-internal.md`
4. `fragment-experience-external.md`
5. `fragment-experience-inherited.md`
6. `fragment-boundary-and-imports.md` — carrying the §27.9 iteration instruction and the §28.2 identity key.
7. Delete `sharepoint-first.md`, `dataverse-first.md`, `hybrid.md`.

**In scope — consumer updates:**

8. `.claude/skills/aisa-blueprint/SKILL.md` — the §20 target contract.
9. `.claude/skills/aisa-decide/SKILL.md` — **bounded serialization cleanup only** (corrected 2026-09-04,
   §27.3): remove the obsolete `Branch` vocabulary; serialize the already-decided facts `/blueprint`
   needs — uncollapsed `(scope, outcome)` pairs, the selected option / composition in plain language,
   decision conditions, proof obligations, accepted risks / preconditions / tripwires; drop `<branch>` from
   the option-list rendering. **It must not emit `architecture.authorization`**, nor own experience mode,
   compositions, record authority or template selection.
10. `library/kernel/blueprint-contract.md` — the three edits of §21.
11. `library/kernel/render-contract.md` — the two edits of §21.
12. `library/kernel/synthesis-templates/architecture-story.template.md` + `.claude/skills/aisa-synthesize`
    — fixed path, reworded prompt.
13. `.claude/skills/aisa-render/SKILL.md` — input path; the four gap classes.
14. `.claude/skills/aisa-options/SKILL.md`, `.claude/skills/aisa-simulate/SKILL.md` — remove `<branch>` from
    rendered option lines (defect §3, item 3). **Rendering only; no decision semantics change.** Re-run the
    Step 3 gate suite to prove the freeze holds.
15. Tests — rewrite `test_pp_options_decision_model.py::TestArchitectureTemplatesRescoped` (it asserts
    exactly three shapes); add `test_pp_architecture_templates.py` for the §23 gate checks, including the
    architectability gate, the headless path and the §28.3 instance-count invariant; extend
    `OBSOLETE_BRANCH_VOCAB` coverage to the architecture-template directory. Three assertions are named
    explicitly (§28.5): **experience-none** (zero experience-fragment instances · no attempt to open
    `fragment-experience-none.md` · no A4 · no render gap); **repeated pattern** (same pattern + same owner
    + distinct `component` ⇒ separate fragments); **duplicate component identity** (same scope, same
    `component` twice ⇒ contract/test failure).

**Out of scope for 5B:** deliverable templates (Step 6), `pack.yaml` deliverable rewrites beyond the
discriminator note, any new research, any change to Step 3 registers or Step 4 knowledge units, any diagram
tooling.

**Open questions carried into 5B:** (i) whether `claude-design-brief` should include the core and address
sections by heading, or receive a narrower entry — resolve in Step 6 with the deliverable in hand;
(ii) whether the conditional *replacement of an existing artefact* section is better owned by
`implementation-spec` (`migration_notes`) than by the core.

---

## 26. Result

The model replaces a 3-value filename enum with one recorded architecture contract, an optional experience
dimension with four values (one of which is *no surface at all*), and one repeatable fragment that makes a
composition's imports structurally impossible to lose. Ten canonical patterns, four store roles, eleven
surfaces, headless architectures and every documented composition pairing render through five runtime
template units. No outcome class, no product and no number lives in a template — and no outcome class, on
its own, authorizes a PP architecture.

```text
STEP 5A — ARCHITECTURE TEMPLATE MODEL: PASS
CURRENT ARCHITECTURE TEMPLATES: 3
PROPOSED ARCHITECTURE TEMPLATES: 5
OLD THREE-BRANCH MODEL SURVIVES: NO
TEMPLATE TAXONOMY DRIVEN BY PRODUCTS: NO
ONE TEMPLATE PER CANONICAL PATTERN: NO
OUTCOME-CLASS REACHABILITY DEFINED: YES
DECISION-TO-BLUEPRINT HANDOFF DEFINED: YES
MULTI-PATTERN ARCHITECTURES SUPPORTED: YES
SCOPE-PAIR ARCHITECTURES SUPPORTED: YES
IMPORTED OBLIGATIONS PRESERVED: YES
DOMAIN KNOWLEDGE DUPLICATED INTO TEMPLATES: NO
CRAFT CAN SELECT ARCHITECTURE: NO
TEMPLATES CAN SELECT WINNING OPTION: NO
VOLATILE VALUES HARDCODED IN TEMPLATES: NO
ROUTER INTRODUCED: NO
NEW STATE MACHINE INTRODUCED: NO
PP RUNTIME FILES MODIFIED: 0
STEP 4 — DOMAIN KNOWLEDGE FROZEN: YES
READY FOR STEP 5A REVIEW: YES
```

---

## 27. Bounded correction record (2026-09-04)

Review verdict on the v1 model: **direction APPROVED, three bounded corrections**. The approved core is
unchanged: one core plus fragments · no router · no scoring · no new state machine · ten patterns to zero
pattern-specific templates · six-channel import carriage · scope-pair behaviour · evidence and epistemic
rendering · volatile-value ownership · selective Domain Knowledge pulls · the CRAFT boundary · the
blueprint-vs-implementation altitude · the diagram contract · the four render-gap classes · the no-product
taxonomy. **No Step 3 outcome semantics were changed and no runtime file was modified.**

| # | Correction | Applied in |
|---:|---|---|
| **C1** | **Outcome reachability separated from pack architectability.** Authorization is now a product of two factors; a positive generic outcome over a non-PP solution authorizes nothing here | §4 (intro, rows 1/2/13(a), vocabulary), §19, §20, §21, §27.1–§27.2 |
| **C2** | **Headless PP architectures are first-class.** The whole-architecture `shape` enum is replaced by an optional `experience` dimension; A4 becomes conditional; A7 stays common; `record_authority` may be an affirmative empty set | §6, §9, §11, §12, §19, §23, §27.4–§27.7 |
| **C3** | **Repeatable boundary-fragment execution made explicit and testable.** Iteration semantics and a deterministic component identity, with no template-engine subsystem | §12, §23, §27.8–§27.10 |

### 27.1 The authorization formula

```text
architecture authorization = outcome reachability × pack architectability
```

Outcome reachability is **necessary and not sufficient**. Each factor fails for its own reason, and the two
reasons are reported separately — a sponsor reading *"no architecture produced"* must be able to tell
*"the decision forbids one"* from *"this pack cannot author one"*.

| Outcome | Selected solution | Result |
|---|---|---|
| class 1 or 2 | PP-containing | may authorize a PP architecture |
| class 1 or 2 | custom-only · packaged / SaaS · cloud-native-only · incumbent · another low-code platform | **no PP architecture authorization** |
| class 3 or 4 | PP keeps the near side | `authorized-bounded` for the PP side only |
| class 13(a) | the sufficient capability is inside the pack's architectable scope | may authorize, `experience.mode: inherited` |
| class 13(a) | the sufficient capability is outside it | **no PP architecture.** Documented sufficiency, *this platform is not excluded* and the graduation trigger are preserved in the decision and deliverable layers |
| any unreachable class | anything | not authorized, for the outcome's own reason |

**Nothing above changes an outcome class, a render template or a comparator rule.** The correction adds a
second gate on the architecture side; Step 3's terminal set and sentences are untouched.

### 27.2 Pack architectability — the smallest sufficient test

One question, answered from facts already recorded. **No routing table, no new stage, no scoring, no
comparator logic, no pattern selection.**

> **Is the selected solution for this scope something this pack has the authority and the knowledge to
> architect?**

| Architectable | Not architectable |
|---|---|
| A PP application (any experience mode) | A custom-only implementation |
| A PP automation or integration composition | A packaged-product / SaaS architecture |
| A PP solution composed with external components — the PP side | A cloud-native-only architecture |
| An inherited or native capability the pack explicitly covers | Incumbent-system internals |
| | Another platform's internals |
| | A candidate set with no selected architecture |

Two rules. **The far side of a scope pair is never architectable here** — architect the PP-owned side and
render a boundary for the relocated responsibility, with no inference about the far side and no comparator
claim. And **the test states its own answer**: `architectability_basis` records why, in one sentence, so a
reader never has to reconstruct it.

### 27.3 Who initializes the authorization — Step 3 stays frozen

`aisa-decide` is **not** the owner. It serializes only already-decided facts: uncollapsed
`(scope, outcome)` pairs · the selected option / composition in plain language · decision conditions ·
proof obligations · accepted risks, preconditions and tripwires. It must **not** emit
`architecture.authorization`, nor own experience mode, compositions, record authority or template
selection. Its Step 5B change is a bounded serialization cleanup only (§25, item 9).

Authorization is **initialized at `/blueprint` entry**:

```text
frozen outcome  +  frozen selected option  +  active pack architecture scope
        ↓
architecture.authorization (+ architectability_basis)
```

This is a **mechanical architecture-entry gate, not a new decision**: two inputs are frozen and the third
is the active pack's own scope. After initialization, templates **read** the authorization and never
derive, upgrade or downgrade it. The Step 3 freeze is preserved: no stage, register, outcome or sentence
changes.

### 27.4 Experience as a dimension, not a shape

The whole-architecture `shape` enum is withdrawn. A PP-containing architecture may legitimately be
**headless** — automation-only, integration-only, scheduled machine work, event-driven processing, queue
plus worker, background processing, API-mediated orchestration, data movement and reconciliation. No fourth
top-level branch is created; instead the core became independent of whether a user surface exists.

```yaml
architecture:
  experience:
    mode: none | owned-internal | owned-external | inherited
    primary_surface: <surface> | null
```

| Value | Meaning | `primary_surface` |
|---|---|---|
| `none` | No human-facing surface is part of this architecture. **A legitimate finalized value, not an Unknown** | `null` / not applicable |
| `owned-internal` | The solution owns its surface and access lifecycle; internal directory audience | required |
| `owned-external` | The solution owns a surface with an audience outside the directory | required |
| `inherited` | Surface access, lifecycle and capacity are inherited from a host | required |

These four are **not option classes and not architecture branches**. They affect only experience-facing
blueprint content. Architecture composition and user experience are **orthogonal dimensions** (§27.11).

### 27.5 Record authority may be empty — affirmatively

`record_authority` changes from `1..N` to `0..N`. Empty is legitimate **only** where the solution does not
own or introduce a persisted business-data domain, and the output must then carry an affirmative rationale,
in the form:

> *No persisted record authority introduced; the workflow acts on external authorities and retains only
> operational execution state.*

**Missing evidence must never be mistaken for an intentional empty set.** Where authority is undetermined,
the entry is an `open_architecture_choices` item — `structural: true` where it decides the store — not an
empty list. Storage is not mandatory for a headless architecture.

### 27.6 A4 becomes conditional

*Application and surface responsibilities* is no longer required merely because a PP architecture exists.
It is **COMMON CONDITIONAL**, engaged where `experience.mode != none`, and rendered by the matching
experience fragment. A headless architecture therefore contains A1–A3, A5–A12 and its boundary fragments,
with **no artificial application section**. Where the mode is `none`, the output must **not** emit *surface
unresolved* or an empty A4: `none` is a known architectural fact.

### 27.7 A7 does not depend on a surface

Identity and authorization reasoning stays **common**. A headless architecture still requires service
identity, managed identity where applicable, connection identity, the trust boundary, the authorization
enforcement point, and secret or certificate custody where material. An experience fragment may
**specialize** A7 for human-user surfaces; it may never own the security section.

### 27.8 Corrected composition contract

```text
architecture-core
  → ZERO or ONE experience fragment
  → ZERO or MORE boundary/import fragment instances
```

| `experience.mode` | Experience fragment |
|---|---|
| `none` | none |
| `owned-internal` | `fragment-experience-internal.md` |
| `owned-external` | `fragment-experience-external.md` |
| `inherited` | `fragment-experience-inherited.md` |

The field controls **only experience-section rendering**. It selects no architecture. Runtime template
units remain **5**: one core, three experience fragments, one boundary fragment. No headless-specific
template is required.

### 27.9 Repeatable fragment execution semantics — binding

The render system has sub-template includes and **no loop primitive**, and none is added. The render layer
is skill-executed, so the iteration is performed by the skill from recorded data:

```text
for each qualifying entry in compositions[] and relocated_responsibilities[]:
    aisa-render / blueprint synthesis
      → instantiate the same fragment body once
      → bind that component's recorded values
      → render all six import channels
```

- **Qualifying** = `boundary: outside-platform`, or any composition beyond `direct`, or any entry in
  `relocated_responsibilities[]`.
- The **core carries the repeat instruction exactly once**; it is a reference, not N copies.
- No new template syntax is introduced, and `render-contract.md` gains no capability.
- The behaviour is nonetheless **testable** — see §28.2–§28.3 (which supersede §27.10).

### 27.10 Fragment uniqueness — deterministic component identity

> **Superseded 2026-09-04 by §28.** The formula stated here —
> `<pattern | responsibility> :: <owner or boundary target>` — **collides** on the legitimate case of two
> components sharing a pattern and an owner (two API-mediated integrations owned by one team), so it could
> not prove the fragment-count invariant. The binding identity and the corrected invariant are §28.2 and
> §28.3. The *purpose* stated here is unchanged and still narrow: catch **lost fragments, duplicated
> fragments and collapsed imports**, with no identifier subsystem invented.

### 27.11 Compositions and experience are orthogonal

The approved pattern treatment is unchanged: **ten canonical patterns → zero pattern-specific templates**.
Patterns remain entries in `compositions[]`, rendered through `fragment-boundary-and-imports.md` where
qualifying. Headless architectures use them identically:

```text
background-processing              + experience.mode = none          → valid
queue-based + hybrid-low-code-pro-code + experience.mode = none      → valid
api-mediated                       + experience.mode = owned-internal → valid
data-replication                   + experience.mode = none          → valid
```

Neither dimension constrains the other, and neither is an option class.

### 27.12 Verification

| # | Check | Result |
|---:|---|:--:|
| 1 | A positive generic outcome over a non-PP solution cannot authorize a PP architecture | **PASS** — §27.1 row 2; §4 rows 1/2; fixture F-17 |
| 2 | Class 13(a) does not automatically authorize a PP blueprint | **PASS** — §4 row 13(a); §27.1; fixture F-18; sufficiency, non-exclusion and the graduation trigger preserved in the decision layer |
| 3 | Architectability is testable without a router, stage, score or comparator | **PASS** — §27.2, one question, two lists |
| 4 | `aisa-decide` does not own an architecture-layer verdict | **PASS** — §27.3; §25 item 9 reduced to serialization cleanup |
| 5 | Step 3 semantics unchanged | **PASS** — no outcome, stage, register or sentence touched; the entry gate reads frozen inputs |
| 6 | A headless PP architecture is representable with no new template | **PASS** — §27.4, §27.8; fixtures F-15, F-16 |
| 7 | No human-facing surface is required, and `none` is not an Unknown | **PASS** — §27.4, §27.6; the *surface unresolved* output is explicitly forbidden |
| 8 | A7 survives without A4 | **PASS** — §27.7; A7 remains COMMON and cannot be owned by a fragment |
| 9 | An empty `record_authority` is distinguishable from missing evidence | **PASS** — §27.5, affirmative rationale required; undetermined authority is a structural open choice |
| 10 | Runtime template units unchanged at 5, no whole-architecture shape enum | **PASS** — §19, §27.8 |
| 11 | Repeat rendering is deterministic and testable with no engine | **PASS** — §27.9 semantics + §27.10 key and count test |
| 12 | No runtime file modified | **PASS** — this correction wrote one authoring file |

**Unchanged by these corrections**, as instructed: the six-channel import carriage · scope-pair behaviour ·
evidence and epistemic rendering · volatile-value ownership · selective Domain Knowledge pulls · the CRAFT
boundary · blueprint-vs-implementation altitude · the diagram contract · the render-gap classes · the
no-product taxonomy · the no-pattern-per-template rule · no router · no scoring · no new state machine.

---

`STEP 5A FINAL BOUNDED CORRECTION: PASS`
`OUTCOME REACHABILITY ALONE AUTHORIZES PP ARCHITECTURE: NO`
`PACK ARCHITECTABILITY GATE DEFINED: YES`
`AISA-DECIDE OWNS ARCHITECTURE AUTHORIZATION: NO`
`HEADLESS PP ARCHITECTURE SUPPORTED: YES`
`HUMAN-FACING SURFACE REQUIRED: NO`
`PRIMARY SURFACE REQUIRED WHEN EXPERIENCE=NONE: NO`
`RECORD AUTHORITY MAY BE EMPTY WITH AFFIRMATIVE RATIONALE: YES`
`WHOLE-ARCHITECTURE SHAPE ENUM RETAINED: NO`
`EXPERIENCE FRAGMENTS: 3`
`PATTERN-SPECIFIC TEMPLATES: 0`
`BOUNDARY FRAGMENT ITERATION DEFINED: YES`
`NON-PP CLASS-1/2 PP-BLUEPRINT REGRESSION FIXTURE ADDED: YES`
`HEADLESS REGRESSION FIXTURES ADDED: 2`
`STEP 3 DECISION SEMANTICS CHANGED: NO`
`PP RUNTIME FILES MODIFIED: 0`
`READY FOR STEP 5B IMPLEMENTATION: YES`

---

## 28. Component-identity micro-correction (2026-09-04)

One semantic defect in §27.10, plus one clarification of already-approved behaviour. **Nothing else
changes**: outcome reachability × architectability · `/blueprint` owning authorization initialization ·
headless semantics · A4 conditionality · A7 common semantics · the empty-`record_authority` rationale ·
five runtime template units · three experience fragments · zero pattern-specific templates · six-channel
import carriage · scope pairs · epistemic handling · Domain Knowledge pull rules · the CRAFT boundary ·
blueprint altitude · the diagram contract · render-gap classes · Step 3 semantics.

**The defect.** §27.10's key was `<pattern | responsibility> :: <owner or boundary target>`. Two
legitimate components collide:

```yaml
compositions:
  - pattern: api-mediated
    forced_by: ERP integration
    owner: Integration Team
  - pattern: api-mediated
    forced_by: CRM integration
    owner: Integration Team
```

Both resolve to `api-mediated::Integration Team`, yet they are **two architectural components requiring
two fragment instances**. The invariant *N qualifying components ⇒ exactly N instances* was therefore
unprovable — the exact failure the key existed to catch.

### 28.1 The local component field

One required field is added to every `compositions[]` entry:

```yaml
compositions:
  - component: erp-integration-api
    pattern: api-mediated
    forced_by: ERP integration
    boundary: outside-platform
    owner: Integration Team
```

The field is **local to the architecture block**: it identifies the actual component or responsibility
instance, is human-readable, and is unique within the architecture scope. It is **not** a registry id, not
canonical vocabulary, not an option class; it carries no semantics outside this blueprint and needs no
globally stable identity. Examples: `erp-integration-api` · `crm-integration-api` · `dispatch-queue` ·
`document-processing-worker` · `analytical-copy` · `customer-master-virtualization`.

**No UUIDs and no id registry are introduced.** `component` is required for every composition; every other
approved field in §6 is unchanged.

### 28.2 Fragment identity — binding

```text
composition fragment key            → <scope>::component::<component>
relocated-responsibility fragment key → <scope>::responsibility::<responsibility>
```

- **`component` is the uniqueness-bearing field** for a composition. `component + "::" + pattern` may be
  used as a validation or debug representation, but it is not the identity.
- Two components may legitimately share the **same pattern, the same owner, the same boundary and even the
  same forcing requirement** and still render separately.
- For a relocated responsibility, the existing `responsibility` **is** the identity and must be unique
  within the architecture scope. No second identifier field is created.
- The **scope prefix exists only for deterministic uniqueness across a multi-scope blueprint**. It is local
  authoring and runtime structure, and it is **never rendered as engagement vocabulary** — consistent with
  `decision-tree.md` §14.3.

### 28.3 Duplicate handling and the corrected invariant

Two entries in the same scope declaring the same local `component` name is an **architecture-contract
defect**. The render and blueprint layers must **not** silently merge them, **not** silently suffix them
and **not** collapse their imports. The architecture work gives them distinct local names.

```text
N unique qualifying composition components
+ M unique relocated responsibilities
→ exactly N + M boundary/import fragment instances
```

Per rendered instance: the key appears **exactly once**; all **six** import channels appear; each channel
is populated or carries `not engaged — <reason>`.

**Fail on:** a missing fragment · a duplicate fragment · a duplicate component identity · collapsed
components · fewer than six channels.

### 28.4 `experience.mode: none` execution — clarification, not a change

```text
experience.mode = none  →  the render skill performs ZERO experience-fragment includes
```

It must **not** attempt to resolve `fragment-experience-none.md`; that file intentionally does not exist.
No placeholder, no render gap, no missing-template warning, no *surface unresolved*. This is a finalized
**not applicable** condition, logged by §18's *not applicable* class as a skip with a reason. Stated in
§12 and §27.8.

### 28.5 Step 5B test additions

| Assertion | Expected |
|---|---|
| **experience-none** | zero experience-fragment instances · no attempt to open `fragment-experience-none.md` · no A4 section · no render gap |
| **repeated pattern** | same pattern + same owner + distinct `component` names ⇒ separate fragments, each with six channels |
| **duplicate component identity** | same scope + same `component` name twice ⇒ contract / test **failure**, never a merge |

Carried alongside the §23 gate checks and fixture **F-19**, which exercises the collision case
mechanically.

### 28.6 Verification

| # | Check | Result |
|---:|---|:--:|
| 1 | Two components sharing pattern and owner render as two fragments | **PASS** — §28.1–§28.2; fixture F-19 |
| 2 | Composition identity is unique within scope and collision-safe | **PASS** — §28.2, `<scope>::component::<component>` |
| 3 | No UUID, registry or global identifier introduced | **PASS** — local, human-readable, no stability requirement |
| 4 | Relocated-responsibility identity defined without a new field | **PASS** — §28.2, `responsibility` is the identity, scope-prefixed |
| 5 | Duplicate identity never silently merged, suffixed or collapsed | **PASS** — §28.3, contract defect |
| 6 | The `N + M` invariant is provable | **PASS** — §28.3; the §27.10 formula is superseded, not retained |
| 7 | `experience.mode: none` opens no missing include and emits no gap | **PASS** — §28.4; §12 and §27.8 updated |
| 8 | Internal identity never becomes engagement vocabulary | **PASS** — §28.2, scope prefix is structure only |
| 9 | Step 3 semantics unchanged | **PASS** — no outcome, stage, register or sentence touched |
| 10 | No runtime file modified | **PASS** — this micro-correction wrote one authoring file |

---

`STEP 5A COMPONENT-IDENTITY MICRO-CORRECTION: PASS`
`COMPOSITION COMPONENT FIELD DEFINED: YES`
`COMPOSITION COMPONENT UNIQUE WITHIN SCOPE: YES`
`SAME PATTERN + SAME OWNER MAY RENDER MULTIPLE COMPONENTS: YES`
`DUPLICATE COMPONENT IDENTITY SILENTLY MERGED: NO`
`RELOCATED RESPONSIBILITY IDENTITY DEFINED: YES`
`N+M FRAGMENT COUNT INVARIANT DEFINED: YES`
`F-19 COLLISION FIXTURE ADDED: YES`
`EXPERIENCE=NONE ATTEMPTS MISSING INCLUDE: NO`
`EXPERIENCE=NONE PRODUCES RENDER GAP: NO`
`STEP 3 DECISION SEMANTICS CHANGED: NO`
`PP RUNTIME FILES MODIFIED: 0`
`STEP 5A MODEL READY TO FREEZE: YES`
`READY FOR STEP 5B IMPLEMENTATION: YES`

---

## 29. Freeze marker (documentation only)

<!--
provenance: AUTHORING (freeze marker) · appended at the start of Step 5B
Documentation only. No runtime change belongs to this marker.
-->

```text
STEP 5A — ARCHITECTURE TEMPLATE MODEL: FROZEN
FINAL BOUNDED CORRECTION: PASS
COMPONENT-IDENTITY MICRO-CORRECTION: PASS
OUTCOME REACHABILITY ALONE AUTHORIZES PP ARCHITECTURE: NO
PACK ARCHITECTABILITY GATE: DEFINED
HEADLESS PP ARCHITECTURE: SUPPORTED
WHOLE-ARCHITECTURE SHAPE ENUM: REMOVED
RUNTIME TEMPLATE UNITS: 5
EXPERIENCE FRAGMENTS: 3
PATTERN-SPECIFIC TEMPLATES: 0
BOUNDARY FRAGMENT ITERATION: DEFINED
COMPONENT IDENTITY: COLLISION-SAFE
STEP 3 DECISION SEMANTICS CHANGED: NO
READY FOR STEP 5B IMPLEMENTATION: YES
```

`STEP 5A: FROZEN`
