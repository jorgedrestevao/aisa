# estimation-model — Implementation Estimation Model

**Source:** transplanted 2026-05-28 from the previous-aisa references (`ref-08-estimation.md`).
**Consulted by:** `cfo-lens`, `solution-architect`; feeds the `estimate.template.md` deliverable directly.
**Phase eligibility:** Options + Decision only.
**Locale:** license prices and team-composition costs are PT-locale defaults; adapt per engagement.

This is the canonical effort / risk / phase model used by the `estimate` deliverable. The numbers below were calibrated against historical Galp-style engagements; refresh on each major Power Platform release wave.

---

## EFFORT TABLE (days per component per technology)

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
| PA flow (medium, 5-15 actions) | 1.5d | 2d | — |
| PA flow (complex: loops, child, error) | 3d | 4d | — |
| PA flow (ingestion, scheduled) | — | — | 1.5d |
| PA flow (triggered, SP orchestration) | — | — | 1d |
| PA flow (publication, file gen + email) | — | — | 2d |
| Low-code plugin | — | 3d | — |
| Canvas App screen (simple, ≤5 fields) | 1.5d | 2d | 2d |
| Canvas App screen (complex, form/approval) | 3d | 4d | 4d |
| Model-Driven App screen | — | 1d | — |
| Approval workflow | — | 2d | 3d |
| External integration (ERP/API) | — | 3-5d | 3-5d |
| Power BI dashboard | 4d | 4d | 5d |
| Historical data migration | — | — | 2-3d |
| Security role (Dataverse) | — | 0.5d | — |
| RLS policy (Azure SQL) | — | — | 1d |
| SharePoint permission group | 0.25d | — | — |

## COMPLEXITY MULTIPLIER
- Simple (<10 sheets, <5 entities): 1.0×
- Medium (10-25 sheets, 5-20 entities): 1.2×
- Complex (>25 sheets, >20 entities, financial/statistical): 1.5×

## BUFFER: Always add 20% to total for unknowns.

---

## STANDARD PHASE STRUCTURE

**Phase 0 — Preparation & Mapping** (1-2 weeks, always first)
- Process mapping sessions with SME
- Formalise ALL business rules from Excel (before any dev)
- Clarify external system integrations
- Validate data model
- Setup environments (Dev/Test/Prod)
- Estimate adjustment based on discoveries

**Phase 1 — Data Layer** (scales with component count)
- Create all tables/lists/SQL schemas
- Implement calculation logic (SPs / flows / columns / plugins)
- Create consumption layer (views / Dataverse views)
- Load reference data
- Unit test: calculations must match Excel exactly for reference period

**Phase 2 — Ingestion** (1-3 weeks, based on source count)
- Automated ingestion flows per external source
- Error handling and alerts
- Integration tests with real data

**Phase 3 — Application** (2-5 weeks, based on screen count)
- Build all Canvas App / Model-Driven screens
- Implement approval workflows
- User testing with SME

**Phase 4 — Publication** (2-3 weeks, based on output count)
- Output generation flows
- External system integration
- End-to-end tests

**Phase 5 — Specialised Modules** (2-3 weeks, only if applicable)
- Complex features specific to the process
- Only if Preparation phase identified specialised sub-processes

**Phase 6 — Dashboards** (1-2 weeks)
- Power BI dashboards
- Publication and permissions

**Phase 7 — UAT & Go-Live** (2-3 weeks, ALWAYS include)
- Integration testing (end-to-end)
- UAT with business users
- **PARALLEL OPERATION: MANDATORY — minimum 2 weeks** (new system + Excel simultaneously)
- Bug fixes and adjustments
- Training and documentation
- Go-live and first-week support

## OVERLAP RULES
- Phases 0-2: always sequential
- Phases 3 and 4: can partially overlap (start 4 when 3 is 70% done)
- Phase 5 (if exists): can overlap with 4
- Phases 6 and 7: can partially overlap
- Phase 7: must be AFTER all development phases complete

---

## STANDARD TEAM COMPOSITION

| Profile | Responsibilities | Dedication |
|---|---|---|
| Power Platform Developer | Data model, logic, Power Apps, Power Automate, integrations | 100% |
| Power BI Developer | Dashboards, data model, publication | 50-100% (concentrated Phase 6) |
| SME / Process Owner | Validate ALL business rules and calculations. UAT. | 20% throughout |
| IT / Infrastructure | Environments, external system access, security, licensing | Punctual (Phase 0 + go-live) |

Scale for project size:
- Simple: 1 PP Developer + SME
- Medium: 1-2 PP Developers + Power BI Dev + SME
- Complex: 2-3 PP Developers + Power BI Dev + Architect (part-time) + SME

---

## STANDARD RISK REGISTER (always include all 6, add context-specific)

| # | Risk | Impact | Probability | Mitigation |
|---|---|---|---|---|
| R1 | Integration with [ERP/API] has undocumented edge cases or format changes | High | Medium | Dedicate Phase 2 to integration testing with real data before Phase 3 begins |
| R2 | Excel formulas have undocumented edge cases or implicit business rules | High | High | Phase 0 mandatory: formalise all rules before development; SME sign-off required |
| R3 | License not provisioned at go-live | Critical | Low | Confirm all licenses 2 weeks before go-live; include in Phase 0 checklist |
| R4 | SME unavailability during critical validation phases | Medium | Medium | Agree SME calendar blocks in advance; identify backup SME |
| R5 | Scope expansion during development | Medium | High | Define MVP scope explicitly; change request process from Phase 0 |
| R6 | Performance at scale (delegation limits, large data volumes) | High | Medium | Test with production-volume data in UAT; implement collection preloads from Phase 3 |

The `risks-and-assumptions` topic pack should always merge these 6 with the engagement-specific risks the Discovery + Framing lenses surfaced (Risky rows in the SU).

---

## OUTPUT FORMAT (10 sections — feed into estimate.template.md)

1. Executive summary box: total duration, team size, phases, overall risk level
2. Phase overview table: phase, description, duration (weeks + days), team
3. Gantt timeline (weeks as columns, phases as rows, overlaps marked)
4. Detailed task list per phase: task name, effort (days), responsible profile
5. Summary table: phase × total weeks × total days × notes
6. Team and effort by profile: profile, total days, phases involved, cost estimate (€/day × days)
7. Risk register: all risks with impact/probability/mitigation
8. Operational impact: manual step → automated equivalent → time saved → annual FTE impact
9. Assumptions and exclusions: what was assumed, what is OUT of scope
10. Recommendations: the single most important recommendation + quick wins + phased approach

---

## QUICK WIN CRITERIA (from fragility analysis)

A quick win is an improvement deliverable NOW in the existing Excel, before the new solution goes live:
- Fix broken #REF! or #NAME? errors → immediate reliability improvement
- Add IFERROR to critical formulas → prevents error propagation
- Add password protection to formula sheets → prevent accidental modification
- Implement naming convention in file names (YYYYMMDD_v1) → version control
- Create a backup copy procedure → disaster recovery
- Document the critical path in a README sheet → reduce single-person dependency
- Replace hardcoded values with a named Parameters sheet → easier maintenance

---

## LICENSE COST ESTIMATES (indicative — always confirm with CSP)

These numbers are indicative as of the previous refresh and decay. Always confirm with Microsoft CSP before committing budget.

| License | EUR/user/month | Notes |
|---|---|---|
| Power Apps per user | ~€18-20 | Includes Dataverse |
| Power Automate per user | ~€12-15 | Attended flows |
| Microsoft 365 E3 | ~€30-35 | SharePoint + basic Power Apps |
| Power BI Pro | ~€8-10 | Per consumer |
| Azure SQL (S2 tier) | ~€120-150/month | Shared, scales with DTU |
| Azure SQL (S0 tier) | ~€15/month | Development/small |

Always add to estimate output: "Preços indicativos — confirmar com Microsoft CSP antes de comprometer orçamento."

---

## WORKED ESTIMATION EXAMPLE — SharePoint Backend

**Scenario:** IT Service Desk migrated from Excel. 7 SharePoint lists, 4 Canvas App screens, 3 flows, 1 approval workflow, 1 Power BI dashboard.

### Step 1 — Count components from SU + Options

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

### Step 2 — Apply multiplier

Complexity: Medium (7 entities, ~15 calculated columns) → 1.2×
`24.25 × 1.2 = 29.1d`

### Step 3 — Add buffer

`29.1 × 1.2 (buffer) = 34.9d ≈ 35 days`

### Step 4 — Map to phases

| Phase | Tasks | Days | Weeks (1 dev) |
|---|---|---|---|
| 0 — Preparation | Discovery, data model validation, env setup | 5d | 1 |
| 1 — Data Layer | Lists + permissions + ref data load | 4.25d | 1 |
| 2 — Ingestion | Not applicable (no external sources) | 0d | 0 |
| 3 — Application | 4 screens + approval workflow | 13d | 2.5 |
| 4 — Publication | 1 complex flow (report generation) | 3d | 0.5 |
| 6 — Dashboards | 1 Power BI dashboard | 4d | 1 |
| 7 — UAT & Go-Live | Testing + parallel operation + training | 8d | 2 |
| **Total** | | **37.25d** | **8 weeks** |

**Result:** ~8 weeks, 1 developer full-time + SME 20%. Present as "8–10 weeks" (add margin for scope uncertainty).

---

## ESTIMATION ANTI-PATTERNS

| Anti-pattern | Why it's wrong | Correct approach |
|---|---|---|
| Not counting approval workflows separately | Approvals are cross-cutting (card + wait + routing + error). Always ≥2d | Count as standalone component, separate from the screen that triggers it |
| Using "simple flow" for anything with error handling | Error handling alone adds 3-5 actions (scope + log + notify) | If flow has Try/Catch → minimum "medium" classification |
| Omitting Phase 7 (UAT) or setting it at <2 weeks | Parallel operation with Excel is MANDATORY and takes minimum 2 weeks | Always include 2-3 weeks for Phase 7. Non-negotiable |
| Not accounting for SharePoint delegation workarounds | Collection preloads and PA-based aggregations add 0.5-1d per screen | Add 0.5d per screen that uses non-delegable operations |
| Estimating Power BI as "just a report" | Data model + DAX measures + RLS + publish + training | Minimum 4d for any dashboard, regardless of simplicity |
| Forgetting reference data loading | Someone must enter/import categories, parameters, users, etc. | Add 0.5d per reference list for data preparation and import |
| Single-point estimate (e.g., "35 days") | Gives false precision, no room for negotiation | Always present as range: "35–42 days" or "8–10 weeks" |

---

## UNCERTAINTY HANDLING

When the SU has Unknown or Assumed rows that block precise sizing, use these rules:

| Unknown | Estimation approach | SU surface |
|---|---|---|
| Number of external integrations | Count 0 in base estimate. Add: "Each integration adds 3-5d (simple API) or 5-8d (complex/undocumented)" | Open `Unknown` row, criticidade=Critical if any integration is required |
| Volume of historical data to migrate | Add 2-3d as placeholder. Note: "Effort scales with data volume and cleanup needs" | Open `Unknown` row on data lens |
| Number of users / roles | Use roles from SU + security claims. Note: "Adding roles post-go-live adds ~1d per role for permission setup + testing" | — |
| Calculation complexity (formulas not fully mapped) | Use formula_count signal if available. If high (>20), apply 1.5× multiplier on translator effort | Open `Risky` row if mapping is incomplete |
| Client responsiveness (SME availability) | Add 1 week buffer to Phase 0 and Phase 7 if client history suggests delays | Open `Risky` row referencing R4 |

**Golden rule:** When in doubt, round UP. Delivering early is a win; delivering late damages trust.
