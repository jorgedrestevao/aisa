# Power Platform — Question Bank

Discovery and evaluation questions, organized by lens, tuned for Power Platform engagements. Lenses draw on these as prompts, not a script — adapt to the engagement.

> **Discipline**: in Discovery (business, operations, user, data, governance, financial), questions probe the *problem* and the *current state* — they must NOT presuppose or name a solution technology. Existing systems may be named as current state. The **technology** lens runs only in the Options phase; that is where vendor/product fit is explored.

## Business

1. What outcome does the sponsor expect, and how will they know it was achieved?
2. Who actually feels this problem day to day — and are they in the room?
3. What is the evidence-based urgency, versus the stated urgency?
4. What happens if we do nothing for the next 6–12 months?
5. Have there been prior attempts to solve this? What happened to them?
6. Which KPIs or targets are tied to this work, and who owns them?
7. Who can veto or block this, and have they been consulted?

## Operations

8. Walk me through the current process end to end — who touches it, in what order?
9. Where do handoffs, waiting, or rework happen today?
10. What exceptions and edge cases does the "happy path" hide?
11. What tribal knowledge or undocumented judgement keeps this running?
12. Which spreadsheets, inboxes, or shared files are load-bearing today?
13. What volume does this process handle (per day/week/month), and what are the peaks?
14. How long does one case take end to end today, and what is the target?

## User

15. Who are the distinct user groups, and roughly how many in each?
16. Where do users work — desk, field, shop floor, on the move?
17. What is the single most frustrating part of the task today?
18. What devices and connectivity do users actually have?
19. What accessibility or language needs must be supported?
20. What would "obviously better" look like from the user's seat?

## Data

21. What are the key data entities, and who owns each (master data)?
22. Where does the data live today, and how good is its quality?
23. How sensitive is the data (PII, financial, confidential), and how is it classified?
24. What are the retention, residency, and audit requirements?
25. What systems of record must this read from or write to?
26. What data volumes and growth rates should we design for?
27. Are there known duplication, reconciliation, or lineage problems?

## Technology (Options phase only)

28. Given the needs identified, which delivery options are viable — including non-technology ones?
29. What is the tenant's current licensing baseline, and does the option need premium entitlements?
30. What integrations are required, and do connectors/APIs exist for them?
31. What are the expected request/transaction volumes versus platform limits?
32. Is mobile or offline genuinely required, and what does that imply for each option?
33. What environment and ALM landscape (DEV/UAT/PROD) must the option fit into?
34. How reversible is each option if it proves wrong?

## Governance

35. What regulations, policies, or standards apply (GDPR, ISO, internal)?
36. What are the access-control and separation-of-duties requirements?
37. What must be auditable, and for how long?
38. What data-handling / DLP policies constrain connectors and data movement?
39. Who approves go-live, and what sign-offs are mandatory?
40. What is the appetite for citizen-developer ownership versus central control?

## Financial

41. What does the current ("as-is") process cost — time, errors, delay?
42. What is the cost of doing nothing?
43. What budget envelope or approval threshold applies?
44. Is funding CAPEX or OPEX, and is there a chargeback model across business units?
45. What payback period or ROI would make this a clear "yes"?

---

## Quality gates — facts to confirm (or accept as risks)

Beyond the open Discovery prompts above, the lenses also probe a fixed set of **quality gates** that experience says break Power Platform engagements when missed. Treat each as either a fact to be Confirmed during Discovery, an explicit Assumed row in the SU (with the basis declared), or — if accepting it knowingly — a Risky row. They are organised here by lens so each lens knows what to chase.

These gates are derived from historical engagements; they pre-date the technology choice (so they're appropriate in Discovery), though their *resolution* often happens in Options/Decision.

### Operations / Data — data integrity

- **D1** — Every spreadsheet sheet in the as-is is classified (operational, reference, output, scratch). No orphan sheets.
- **D2** — Every discovered data input has a corresponding entity in the to-be model (or an explicit "excluded because…" note).
- **D3** — Every discovered calculation has an implementation mechanism slated (Power Fx, SP, Power Automate, Business Rule).
- **D4** — Every discovered output has a delivery mechanism (file, email, dashboard, API).
- **D5** — No orphan entities — every table is consumed by something (a screen, a flow, a report).
- **D6** — Every FK relationship is defined on both sides (parent and child entities both know about it).
- **D7** — Entity creation order respects the dependency chain (no FK declared before its parent exists).
- **D8** — Every formula identified during Discovery has a translation plan into the chosen platform.

### Technology / Solution-architect — schema rigor (Options phase)

- **S1** — Dataverse: no reserved system column names used as custom columns.
- **S2** — Dataverse: `required` / `searchable` / `auditable` flags set explicitly on every column.
- **S3** — Azure SQL: every table has the 5 mandatory audit columns (`id, created_at, created_by, modified_at, modified_by`).
- **S4** — Azure SQL: Bronze tables never have UPDATE or DELETE in any SP (append-only).
- **S5** — Azure SQL: every SP has TRY/CATCH with ROLLBACK and an INSERT into `audit_executions`.
- **S6** — Azure SQL: the SP execution DAG is complete and acyclic.
- **S7** — SharePoint: never exceed 12 indexed columns per list.
- **S8** — SharePoint: every view filter uses an indexed column.
- **S9** — Naming convention applied consistently throughout (one of PascalCase / snake_case / publisher_prefix) — zero exceptions.

### Technology — Power Fx pitfalls (Options phase)

- **P1** — Every division operation is zero-guarded: `If(divisor<>0, n/d, 0)`.
- **P2** — SUMPRODUCT is never in Power Fx — always migrated to a Power Automate pattern.
- **P3** — NPV / IRR / PMT / RATE are never in Power Fx — always Power Automate or T-SQL.
- **P4** — Every LookUp on a non-PK column carries a delegation warning + collection workaround.
- **P5** — Every Filter / Search has a delegation check.
- **P6** — `App.OnStart` includes a fallback for blank user role (navigate to AccessDenied).
- **P7** — All global variables used in formulas are declared in `App.OnStart`.
- **P8** — All data sources used in formulas appear in the deployment handoff.
- **P9** — The state machine documents ALL transitions — not only the happy path.
- **P10** — WORKDAY translation always includes the holiday-table warning + Power Automate alternative.

### Governance / Compliance-officer — security gates

- **E1** — No cell in the permission matrix is blank — undefined defaults to "no access" and is documented.
- **E2** — Least privilege wins on conflicts — never grant higher than the most restrictive overlap.
- **E3** — Admin role has full access to all resources without exception.
- **E4** — Every approval action has at least one role assigned to execute it.
- **E5** — Inheritance: a parent role's permissions ≥ child role's permissions on every resource.
- **E6** — Audit Power Fx is mandatory for Approve, Delete, Export actions.
- **E7** — Test users use `@demo.com` emails — never real organisation domains.

### Financial / CFO — estimation gates

- **M1** — Every component identified in the SU is counted in the estimate.
- **M2** — Complexity multiplier is applied to all effort figures (1.0× / 1.2× / 1.5×).
- **M3** — Parallel operation during UAT is mandatory — minimum 2 weeks in Phase 7.
- **M4** — Sizing units are always days — never hours.
- **M5** — Every risk in the register has a specific, actionable mitigation (no generalised mitigations).
- **M6** — Operational impact shows specific time savings per manual step (with quantification).
- **M7** — Quick wins are always proposed — at least 2.
- **M8** — Deploy order is documented (data → security → flows → app → sample data → UAT).
- **M9** — Rollback plan covers every deploy phase — not just the full solution.
