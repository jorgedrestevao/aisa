# Implementation Estimation Model

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

---

## ⚠ NOT VALID AS COMPARATIVE ECONOMICS

**This model must not be used to compare option classes at the Options economics stage.**

It carries effort bands for building on *this* platform and nothing else. There is no comparator-side basis
in it: no effort model for a SaaS product, for pro-code, for an incumbent system, or for any other low-code
platform. Applying it comparatively produces a quantified number for one option class and silence for every
other — and a number next to a blank reads as the better option regardless of what it says. That is
comparator preference created by the shape of the evidence, not by the evidence itself.

Three legitimate uses:

1. **Projecting a platform candidate in simulation** (`/simulate`). The projected effort band is a
   property of *that candidate*, and the output must carry the asymmetry statement explicitly: this band
   exists for this option class only, no equivalent band was computed for the alternatives, and the absence
   of a comparator number is not evidence that the alternative is cheaper or dearer.
2. **As source `PACK MODEL` of the Options order-of-magnitude field.** An Options candidate may take
   its band from this model applied to the option's shape, at the granularity this file supports
   *before* a blueprint exists — component counts and complexity, not screens designed. The option
   line then carries the marker `PACK MODEL` **and the asymmetry statement above**, unchanged: the
   band belongs to that candidate and to no comparison between classes. Naming the source is what
   makes the number readable; a band with no source is invented, and the field is then written
   `ORDER OF MAGNITUDE UNAVAILABLE` instead. The method and its four markers are owned by
   `.claude/skills/chairman-synthesis/SKILL.md` and are not restated here.
3. **Post-decision, for the estimate deliverable.** Once a decision exists, the comparison is over and
   sizing the chosen path is exactly the right job for this model.

**No prices here.** Rates, licence costs and any monetary figure belong to the engagement's own commercial
model and to `economics/licensing-and-cost-drivers.md` for the cost *drivers*. This file is denominated in
person-days only.


**O que um «always» significa neste ficheiro.** Convenção da equipa, não limite de plataforma: cada uma é
uma **proposta explícita e substituível**, e existe porque uma propriedade técnica a justifica — a razão
está ao lado da regra. Um engagement pode adoptar outra convenção; a que adoptar fica registada com a sua
razão. Nenhuma delas é obrigação de governance, nenhuma depende de alguém a aprovar, e nenhuma se aplica
onde a propriedade técnica que a justifica não existe.

**Calibration:** the bands were calibrated against past engagements of this team. They are a delivery
convention with a shelf life — revisit them when the team's composition or the platform's build experience
changes materially. They are not platform measurements.

---

## EFFORT TABLE (days per component per store)

| Component | SharePoint | Dataverse | Azure SQL |
|---|---|---|---|
| List/Table (simple, ≤5 cols, no rules) | 0.25d | 0.5d | — |
| List/Table (complex, >5 cols, rules) | 0.5d | 1d | — |
| Bronze table | — | — | 0.5d |
| Silver table | — | — | 1d |
| Gold table | — | — | 0.5d |
| Reference table | 0.25d | 0.5d | 0.5d |
| Calculated/rollup column | 0.25d | 0.25d | — |
| Business rule | — | 0.5d | — |
| SP (ingestion/output) | — | — | 1d |
| SP (complex calculation) | — | — | 1.5d |
| SQL View | — | — | 0.5d |
| PA flow (simple, ≤5 actions) | 0.5d | 0.5d | — |
| PA flow (medium, 5–15 actions) | 1.5d | 2d | — |
| PA flow (complex: loops, child, error) | 3d | 4d | — |
| PA flow (ingestion, scheduled) | — | — | 1.5d |
| PA flow (triggered, SP orchestration) | — | — | 1d |
| PA flow (publication, file gen + email) | — | — | 2d |
| Low-code plugin | — | 3d | — |
| Canvas App screen (simple, ≤5 fields) | 1.5d | 2d | 2d |
| Canvas App screen (complex, form/approval) | 3d | 4d | 4d |
| Model-driven app screen | — | 1d | — |
| Approval workflow | — | 2d | 3d |
| External integration (ERP/API) | — | 3–5d | 3–5d |
| Power BI dashboard | 4d | 4d | 5d |
| Historical data migration | — | — | 2–3d |
| Security role (Dataverse) | — | 0.5d | — |
| RLS policy (Azure SQL) | — | — | 1d |
| SharePoint permission group | 0.25d | — | — |

A blank cell means "this component does not exist in that store", not "that store is unsuitable".

## COMPLEXITY MULTIPLIER
- Simple (<10 sheets, <5 entities): 1.0×
- Medium (10–25 sheets, 5–20 entities): 1.2×
- Complex (>25 sheets, >20 entities, financial/statistical): 1.5×

## BUFFER: +20% for unknowns — the team's working figure

Convenção da equipa, não limite de plataforma: é uma **proposta explícita e substituível** — o engagement pode adoptar outra, e a que adoptar fica registada com a sua razão. The figure is a function of what is still open, not a constant: where the SU carries
material open questions on the axes that size the work, it goes up and the estimate says which rows drove
it; where the scope is closed and evidenced, it goes down. A buffer applied without saying what it covers is
a number with no basis, which the estimate is not allowed to emit.

---

## STANDARD PHASE STRUCTURE

**Phase 0 — Preparation & mapping** (1–2 weeks, first — the rules the later phases build against are
formalised here, so the ordering is a technical dependency, not a policy)
- Process mapping sessions with the SME
- Formalise ALL business rules from Excel (before any dev)
- Clarify external system integrations
- Validate the data model
- Set up environments (see `delivery-conventions.md` §3)
- Adjust the estimate based on what Phase 0 discovers

**Phase 1 — Data layer** (scales with component count)
- Create all tables/lists/SQL schemas
- Implement calculation logic (SPs / flows / columns / plugins)
- Create the consumption layer (views)
- Load reference data
- Unit test: calculations must match Excel exactly for a reference period

**Phase 2 — Ingestion** (1–3 weeks, based on source count)
- Automated ingestion flows per external source
- Error handling and alerts
- Integration tests with real data

**Phase 3 — Application** (2–5 weeks, based on screen count)
- Build all screens
- Implement approval workflows
- User testing with the SME

**Phase 4 — Publication** (2–3 weeks, based on output count)
- Output generation flows
- External system integration
- End-to-end tests

**Phase 5 — Specialised modules** (2–3 weeks, only if applicable)
- Complex features specific to the process
- Only if Phase 0 identified specialised sub-processes

**Phase 6 — Dashboards** (1–2 weeks)
- Reporting build
- Publication and permissions

**Phase 7 — UAT & go-live** (2–3 weeks, engaged where the target replaces or feeds something already in
use — which is the normal case; where nothing is being replaced, the phase is scoped to what is actually
verified and the estimate says so)
- Integration testing (end-to-end)
- UAT with business users
- **Parallel operation** (new system + the existing artefact simultaneously): engaged where the existing
  artefact is load-bearing while the new one is proven — the requirement is *continuity of the process
  during cutover*, not a fixed duration. The team's working figure is 2 weeks minimum; the real figure comes
  from the process cadence (a monthly cycle needs a cycle, a daily one needs less)
- Bug fixes and adjustments
- Training and documentation
- Go-live and first-week support

## OVERLAP RULES — technical dependencies, not scheduling policy

Each rule below exists because one phase consumes what the previous one produces. Where that dependency does
not hold for a given engagement, the rule does not either.

- Phases 0–2: sequential — the data layer is built against formalised rules, and ingestion against the
  data layer
- Phases 3 and 4: can partially overlap (start 4 when 3 is 70% done)
- Phase 5 (if it exists): can overlap with 4
- Phases 6 and 7: can partially overlap
- Phase 7: must be AFTER all development phases complete

---

## STANDARD TEAM COMPOSITION — delivery guidance, replaceable

**Not part of the estimation model.** Who staffs the work, at what dedication, is the delivering
organisation's call and never an input to which technology or pattern is recommended. The table stays
because `estimate.template.md` cites it by name for the `team_effort` and `profile_load` slots, and because
a profile-load calculation needs *some* declared composition to run against. Convenção da equipa, não limite de plataforma: é uma **proposta explícita e substituível** — o engagement pode adoptar outra, e a que adoptar fica registada com a sua razão. An
engagement that declares its own composition uses that one, and the estimate records which it used.

The **profiles** below are roles, not people. No name is an input, and an unnamed profile blocks nothing.

| Profile | Responsibilities | Dedication |
|---|---|---|
| Power Platform developer | Data model, logic, apps, flows, integrations | 100% |
| Power BI developer | Dashboards, data model, publication | 50–100% (concentrated in Phase 6) |
| SME / process owner | Validate ALL business rules and calculations. UAT. | 20% throughout |
| IT / infrastructure | Environments, external system access, security, entitlement provisioning | Punctual (Phase 0 + go-live) |

Scale for project size:
- Simple: 1 PP developer + SME
- Medium: 1–2 PP developers + Power BI dev + SME
- Complex: 2–3 PP developers + Power BI dev + architect (part-time) + SME

---

## STANDARD RISK REGISTER — the six the team keeps seeing

Each row is a **hypothesis to test against the engagement**, carried with the condition that makes it real,
not a risk asserted because the register has six lines. A row whose condition does not hold in this
engagement is dropped, and the estimate does not list it. Context-specific risks come from the SU's `Risky`
rows and are never replaced by these.

| # | Risk | Impact | Probability | Mitigation |
|---|---|---|---|---|
| R1 | Integration with [ERP/API] has undocumented edge cases or format changes | High | Medium | Dedicate Phase 2 to integration testing with real data before Phase 3 begins |
| R2 | Excel formulas have undocumented edge cases or implicit business rules | High | High | Formalise the rules in Phase 0, before development; each rule confirmed by the **role** that owns it, against the artefact — a confirmation is evidence at a locator (`states.md` → *Confirmed threshold*), not a signature |
| R3 | Entitlements not provisioned at go-live | Critical | Low | Confirm all entitlements well before go-live; include in the Phase 0 checklist |
| R4 | The role that owns the business rules is not available to validate them when needed | Medium | Medium | Agree the availability the validation needs, in advance, with whoever holds the role; more than one holder is what makes the plan survive one absence |
| R5 | Scope expansion during development | Medium | High | Define MVP scope explicitly; change-request process from Phase 0 |
| R6 | Performance at scale (query behaviour, large data volumes) | High | Medium | Test with production-volume data in UAT; apply the delegation-safe patterns from Phase 3 |

The `risks-and-assumptions` topic pack merges the rows whose condition holds with the engagement-specific
risks the Discovery + Framing lenses surfaced (`Risky` rows in the SU). A row carried without its condition
holding is noise in the pack, and it costs the reader the ones that matter.

---

## OUTPUT FORMAT (10 sections — feeds estimate.template.md)

1. Executive summary box: total duration, team size, phases, overall risk level
2. Phase overview table: phase, description, duration (weeks + days), team
3. Gantt timeline (weeks as columns, phases as rows, overlaps marked)
4. Detailed task list per phase: task name, effort (days), responsible profile
5. Summary table: phase × total weeks × total days × notes
6. Team and effort by profile: profile, total days, phases involved — **days only**; rates and any monetary
   conversion are applied outside this model, in the engagement's commercial layer
7. Risk register: all risks with impact/probability/mitigation
8. Operational impact: manual step → automated equivalent → time saved → annual FTE impact
9. Assumptions and exclusions: what was assumed, what is OUT of scope
10. Recommendations: the single most important recommendation + quick wins + phased approach

If the output is produced during Options rather than after the decision, section 1 must carry the
comparative-invalidity statement from the top of this file, verbatim in substance.

---

## QUICK WIN CRITERIA (from fragility analysis)

A quick win is an improvement deliverable NOW in the existing Excel, before the new solution goes live:
- Fix broken `#REF!` or `#NAME?` errors → immediate reliability improvement
- Add IFERROR to critical formulas → prevents error propagation
- Add protection to formula sheets → prevents accidental modification
- Implement a naming convention in file names (YYYYMMDD_v1) → version control
- Create a backup copy procedure → disaster recovery
- Document the critical path in a README sheet → reduces single-person dependency
- Replace hardcoded values with a named Parameters sheet → easier maintenance

---

## WORKED ESTIMATION EXAMPLE

**Scenario:** IT service desk migrated from Excel onto a SharePoint-backed build. 7 lists, 4 app screens,
3 flows, 1 approval workflow, 1 dashboard.

### Step 1 — Count components from the SU + Options

| Component | Qty | Unit effort | Subtotal |
|---|---|---|---|
| SharePoint list (simple, ≤5 cols) | 3 | 0.25d | 0.75d |
| SharePoint list (complex, >5 cols, rules) | 4 | 0.5d | 2.0d |
| Reference table | 2 | 0.25d | 0.5d |
| SharePoint permission group | 4 | 0.25d | 1.0d |
| PA flow (simple) | 1 | 0.5d | 0.5d |
| PA flow (medium) | 1 | 1.5d | 1.5d |
| PA flow (complex: loops, child, error) | 1 | 3d | 3.0d |
| Canvas App screen (simple) | 2 | 1.5d | 3.0d |
| Canvas App screen (complex, form/approval) | 2 | 3d | 6.0d |
| Approval workflow | 1 | — | 2.0d |
| Power BI dashboard | 1 | 4d | 4.0d |
| **Raw total** | | | **24.25d** |

### Step 2 — Apply the multiplier

Complexity: Medium (7 entities, ~15 calculated columns) → 1.2×
`24.25 × 1.2 = 29.1d`

### Step 3 — Add the buffer

`29.1 × 1.2 (buffer) = 34.9d ≈ 35 days`

### Step 4 — Map to phases

| Phase | Tasks | Days | Weeks (1 dev) |
|---|---|---|---|
| 0 — Preparation | Discovery, data model validation, env setup | 5d | 1 |
| 1 — Data layer | Lists + permissions + ref data load | 4.25d | 1 |
| 2 — Ingestion | Not applicable (no external sources) | 0d | 0 |
| 3 — Application | 4 screens + approval workflow | 13d | 2.5 |
| 4 — Publication | 1 complex flow (report generation) | 3d | 0.5 |
| 6 — Dashboards | 1 dashboard | 4d | 1 |
| 7 — UAT & go-live | Testing + parallel operation + training | 8d | 2 |
| **Total** | | **37.25d** | **8 weeks** |

**Result:** ~8 weeks, 1 developer full-time + SME 20%. Present as "8–10 weeks" (margin for scope
uncertainty).

Note what this example is and is not: it sizes one build. It says nothing about what the same service desk
would cost as a product subscription or as a pro-code build, because no such figure was computed.

---

## ESTIMATION ANTI-PATTERNS

| Anti-pattern | Why it's wrong | Correct approach |
|---|---|---|
| Not counting approval workflows separately | Approvals are cross-cutting (card + wait + routing + error) | Count as a standalone component, separate from the screen that triggers it |
| Calling anything with error handling a "simple flow" | Error handling alone adds a scope + log + notify | If the flow has Try/Catch → minimum "medium" |
| Sizing Phase 7 without asking what cutover has to prove | Where the existing artefact is load-bearing, running the two in parallel is what proves the new one — and it takes at least one process cycle | Derive the duration from the process cadence, and state which cycle it covers. The team's working figure is 2–3 weeks |
| Ignoring query workarounds | Collection preloads and flow-based aggregations are real build work | Add 0.5d per screen that needs a workaround for an operation the delegation owner flags as non-delegable (`data/query-and-delegation.md`) |
| Estimating a dashboard as "just a report" | Data model + measures + row-level security + publish + training | Minimum 4d for any dashboard, regardless of apparent simplicity |
| Forgetting reference data loading | Someone must enter/import categories, parameters, users | Add 0.5d per reference list for preparation and import |
| Single-point estimate ("35 days") | False precision, no room for negotiation | Always a range: "35–42 days" or "8–10 weeks" |
| Using this model to compare option classes | Produces a number for one class and silence for the others | Restrict to simulation of a platform candidate (with the asymmetry statement) or to post-decision sizing |

---

## UNCERTAINTY HANDLING

When the SU has Unknown or Assumed rows that block precise sizing:

| Unknown | Estimation approach | SU surface |
|---|---|---|
| Number of external integrations | Count 0 in the base estimate. Add: "each integration adds 3–5d (simple API) or 5–8d (complex/undocumented)" | Open `Unknown` row, criticidade=Critical if any integration is required |
| Volume of historical data to migrate | Add 2–3d as a placeholder. Note: "effort scales with data volume and cleanup needs" | Open `Unknown` row on the data lens |
| Number of users / roles | Use the roles from the SU + security claims. Note: "adding roles post-go-live adds ~1d per role for permission setup + testing" | — |
| Calculation complexity (formulas not fully mapped) | Use the formula-count signal if available; where the count is high, apply the 1.5× multiplier to translation effort | Open `Risky` row if the mapping is incomplete |
| Client responsiveness (SME availability) | Add 1 week of buffer to Phase 0 and Phase 7 if history suggests delays | Open `Risky` row referencing R4 |

**Golden rule:** when in doubt, round UP. Delivering early is a win; delivering late damages trust.
