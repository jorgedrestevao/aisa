---
dt_id: pp-branch-qualification
applies_to_phase: options
consulted_by: [lens-technology, solution-architect]
branches:
  - id: sharepoint-first
    display_name: "SharePoint-first"
    sub_template: architecture-templates/sharepoint-first.md
  - id: dataverse-first
    display_name: "Dataverse-first"
    sub_template: architecture-templates/dataverse-first.md
  - id: hybrid
    display_name: "Hybrid (Dataverse + SharePoint)"
    sub_template: architecture-templates/hybrid.md
inputs_used:
  - max_volume_per_entity        # peak record count for the largest entity (from operations + data lenses)
  - requires_audit_trail         # boolean — explicit audit/regulatory requirement (governance)
  - relational_integrity_required # boolean — ≥1 FK relationship with cascade/business-rule semantics (data)
  - delivery_timeline_weeks      # integer — committed delivery window (business + financial)
  - admin_team_capability        # enum: keyuser | internal_power_platform | partner_delivery (operations)
  - existing_sharepoint          # boolean — solution must integrate with an existing SharePoint footprint
  - user_count                   # expected app users (business lens) — licensing scale
  - premium_licensing_rejected   # boolean — client explicitly rejects premium licensing (financial/business)
  - external_integrations_count  # non-Microsoft integrations needed (technology/operations)
  - formula_count                # calculated columns / formula load inherited from the legacy tool (data/operations)
  - financial_precision_decimals # required decimal precision for money fields (financial/data)
  - approval_stages_max          # max states in any approval state machine (operations/governance)
  - realtime_required            # boolean — sub-second interactive requirement (operations/user)
  - entity_profile               # counts of simple vs complex entities (data) — feeds the hybrid trigger
---

# Decision Tree — Power Platform Architectural Branches

> **Changelog 2026-08-31**: R4–R6 reescritas — as versões anteriores tinham veredictos idênticos nos dois ramos do IF/ELSE (defeito de edição, ver `docs/GAP_ANALYSIS.md` G-15); `inputs_used` completado com os inputs que R0 e o hybrid-trigger já usavam sem declarar. **Thresholds a validar com a equipa na primeira retro do pilot.**

This tree is the **only** Discovery-output-driven mechanism the solution architect uses to shortlist architectural branches for the `pp` pack. It is consulted in the **Options phase** and never before. Each rule maps a condition over the listed inputs to a per-branch verdict; the solution architect aggregates verdicts across the rules and assigns scores (`forte`, `adequada`, `intermédia`, `inadequada`, etc.). The branching is then proposed as 3–5 options for the chairman to synthesise into `options.md`.

The Inputs are SU claims emitted by the Discovery lenses. If an input is missing (no corresponding SU id) → solution-architect must STOP at that rule, surface an `Unknown` for the missing fact, and either obtain it or proceed with an explicit Assumption (basis declared).

## The three branches

- **A — `sharepoint-first`**: SharePoint Online + Power Automate + Canvas App. Lowest licensing cost, fastest first delivery, weakest audit/integrity guarantees.
- **B — `dataverse-first`**: Dataverse + Model-driven App + Power Automate. Strongest audit/integrity, premium licensing baseline, longest first delivery.
- **C — `hybrid`**: Dataverse for critical entities + SharePoint for secondary/attachments + Canvas App. Middle ground; complexity of two systems but volume + integrity on the Dataverse side.

---

## R0 — Hard gates (run before scoring)

Any branch that fails a hard gate is removed from the option set entirely (move it to "Alternatives Considered" in deliverables with the failing condition documented). Apply R0 BEFORE running R1–R6.

**`sharepoint-first` disqualified if ANY of:**
- `max_volume_per_entity` > 30,000 rows (list-view threshold degrades severely; even archive flows cannot rescue this).
- Cross-list joins required (>1 N-N relationship traversed in queries).
- `formula_count` > 100 across calculated columns (delegation breaks; per-column formula limits compound).
- Financial precision > 2 decimals required (SharePoint Currency caps at 2 decimals).
- Audit trail required for regulatory compliance (SharePoint has no native immutable audit; PA-based audit can be tampered).
- Multi-stage approval (>3 states in any state machine) — Content Approval can't model it.

**`dataverse-first` disqualified if ANY of:**
- Premium licensing explicitly rejected by the client (Per User / Per App not viable in their commercial frame).
- External non-Microsoft integrations > 3 (per-integration premium connector cost compounds).
- Sub-second real-time performance required (Dataverse latency is typically 200ms–2s — not fit-for-purpose for trading-floor-style scenarios).

**`hybrid` disqualified if:**
- The same disqualifications that kill *both* `sharepoint-first` AND `dataverse-first` for the project's profile — there's nothing for the hybrid to lean on.
- The team's `admin_team_capability` is `keyuser` only — managing two backends is beyond keyuser capability.

If all three branches are disqualified, the option set must include "Custom web app outside Power Platform" or "Process change without digitalisation" as the proposed paths forward.

The thresholds above mirror the platform hard limits documented in [`domain-knowledge/sharepoint-reference.md`](domain-knowledge/sharepoint-reference.md), [`domain-knowledge/dataverse-reference.md`](domain-knowledge/dataverse-reference.md), and [`domain-knowledge/azure-sql-reference.md`](domain-knowledge/azure-sql-reference.md). When in doubt, defer to the reference file — these are platform constraints, not preferences.

---

## R1 — Adequação ao volume

- IF `max_volume_per_entity` ≤ 5000 → A=adequada, B=forte, C=forte
- IF 5000 < `max_volume_per_entity` ≤ 100000 → A=inadequada, B=forte, C=forte
- IF `max_volume_per_entity` > 100000 → A=inadequada, B=adequada, C=adequada

## R2 — Governance e audit

- IF `requires_audit_trail` = true → A=básico, B=forte, C=forte
- ELSE → A=básico, B=intermédio, C=intermédio

## R3 — Esforço de implementação

- IF `delivery_timeline_weeks` ≤ 8 AND `max_volume_per_entity` ≤ 5000 → A=baixo, B=alto, C=alto
- IF `delivery_timeline_weeks` ≤ 12 → A=baixo, B=médio-alto, C=alto
- ELSE → A=baixo, B=médio, C=médio-alto

## R4 — Custo de licenciamento

- IF `premium_licensing_rejected` = true → A=mínimo, B=inviável (R0 aplica-se), C=inviável (R0 aplica-se)
- IF `user_count` ≤ 20 → A=mínimo (coberto por M365 standard), B=médio (Power Apps Per App torna o premium comportável a esta escala), C=médio
- ELSE → A=mínimo, B=alto (premium per-user para todos os utilizadores da app), C=alto (qualquer presença de Dataverse obriga licenciamento premium — o lado SharePoint do hybrid não o evita)

## R5 — Manutenção contínua

- IF `admin_team_capability` = keyuser → A=baixa, B=alta, C=alta (dois backends estão além de keyuser — ver também R0)
- IF `admin_team_capability` = internal_power_platform → A=baixa, B=média, C=média-alta (o custo do hybrid é a fronteira entre backends, não cada backend)
- IF `admin_team_capability` = partner_delivery → A=baixa, B=baixa-média (o parceiro absorve a curva Dataverse), C=média

## R6 — Reversibilidade se errar

- IF `max_volume_per_entity` ≤ 5000 AND `requires_audit_trail` = false → A=alta (listas pequenas exportam trivialmente), B=média (schema premium, mas dados pequenos migram num dia), C=baixa (dois backends para desmontar)
- ELSE → A=média (export volumoso de listas é doloroso mas viável), B=baixa (migração de schema + histórico auditado preso ao premium), C=baixa (dois backends + histórico repartido entre eles)

---

## Hybrid trigger

When the top two branches (after R0–R6) come out within a narrow margin AND the engagement has a heterogeneous entity profile, prefer the hybrid branch:

```
entities_simple  = entities where volume < 5,000 AND no complex calculations
entities_complex = entities where volume > 10,000 OR has financial formulas

IF entities_simple.count >= 2 AND entities_complex.count >= 2 →
  Propose hybrid: simple entities on SharePoint/Dataverse-light, complex entities on Dataverse/Azure-SQL.
  Document the split in the option's "scope per backend" section.
```

This is one of the two cases where `hybrid` should jump to top recommendation. The other is when the engagement profile literally requires it (e.g., document-heavy attachments + structured business data — SharePoint for files, Dataverse for records).

---

## Exclusion side-effects

After rule evaluation, apply these exclusions before the solution architect proposes the option set:

- IF `relational_integrity_required` = true AND `max_volume_per_entity` > 5000 → **exclude `sharepoint-first` from top-N** (move to "Alternatives Considered" in deliverables; flag the reason).
- IF `delivery_timeline_weeks` < 8 → **exclude `dataverse-first` from top-N** (effort floor breach for a fresh build).
- IF `admin_team_capability` = keyuser AND `requires_audit_trail` = true → flag **both** `dataverse-first` and `hybrid` with `⚠️ requires_external_support` — the maintenance load is real even if the branch is otherwise viable.

---

## Missing inputs handling

If any input has no corresponding SU id when the architect is about to consult this tree:

1. Open an `Unknown` row in the SU (`lens: technology`, `criticidade`: Med-Critical depending on which rule blocks).
2. Either resolve it (USER_ANSWER, document hunt) or proceed with an explicit `Assumed` row (`base da assumption: industry default for <…> in similar PP engagements`). Both paths feed back into the branching verdict.
3. Re-evaluate the affected rule once the input is known. The previous verdict is invalidated; record the change in the chairman synthesis log.

This protocol is consistent with the project rule `library/kernel/states.md` (Confirmed vs Assumed vs Unknown) and the orchestration discipline that the council does not invent claims.

---

## Always include a do-nothing and a non-technology option

Independent of this tree, `aisa-options` requires that the proposed option set contains:

- **One do-nothing baseline** — the cost of the next 6–12 months without action; the cfo-lens persona is the natural anchor.
- **One non-technology option** — process change, reorganisation, manual control redesign. The operations-lead persona is the natural anchor. This option NEVER consults this decision tree (the tree is about technology branches only).

These two are added by the chairman during synthesis, not by this tree.
