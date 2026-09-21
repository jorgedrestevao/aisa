# screen-consolidation-rules — Decision Tree for App Screen Consolidation

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

**Named hard contract.** `library/kernel/blueprint-contract.md` and the `aisa-blueprint` skill reference this
file by name and depend on the rules below exactly as written. Do not renumber, reword or relax them.

**Consulted by:** `lens-technology`, `solution-architect`, `aisa-blueprint`, the `implementation-spec` and
`claude-design-brief` deliverable templates.
**Companion file:** [`screen-patterns.md`](screen-patterns.md) — the full Canvas screen-pattern catalogue.
This file is the *decision tree*; that file is the *catalogue*.

The rules below convert the engagement's field inventory, role list, and approval semantics into a screen
plan. Apply them once the decision's data model and role model are known, and before the
`implementation-spec` is written.

---

## Inputs to the tree

- All editable/viewable fields surfaced by the data lens (Confirmed or Assumed SU rows).
- Source entities and their relationships (data lens).
- Target roles and their approval authority (governance lens + [`security-craft.md`](security-craft.md)).
- Process steps (operations lens).

---

## The tree

```
1. Group all fields by PRIMARY ENTITY.

For each entity group:

2. Count editable fields:
   ├── ≤ 8 editable + ≤ 4 read-only → Single form screen (unless Step 3 splits)
   ├── 9–16 editable                → Single form screen with sections/tabs
   └── > 16 editable                → Multi-step form (wizard) OR split into sub-screens

3. Role separation:
   ├── All editing roles edit SAME fields → Single screen, no role visibility logic
   ├── Roles edit OVERLAPPING fields → Single screen, conditional visibility (Visible = User.Email in RoleGroup)
   └── Roles edit DIFFERENT fields → Separate screens per role

4. Gallery/list need:
   ├── > 1 record visible at a time → Gallery/List + Detail/Edit
   └── Otherwise → Direct form (e.g., settings, profile)

5. Approval need:
   ├── Entity has STATE column with approval transitions → Add approval action buttons to the form (NOT a separate screen)
   └── Otherwise → Standard CRUD

6. Reporting need:
   ├── Entity feeds OUTPUT zone or summary → Dashboard screen (read-only, aggregated)
   └── Otherwise → No additional screen
```

---

## Naming convention

- Gallery: `[Entity]ListScreen`
- Form: `[Entity]FormScreen`
- Dashboard: `[Entity]DashboardScreen` or `DashboardScreen` (cross-entity)
- Approval: NOT a separate screen — action on `[Entity]FormScreen`

---

## Hard caps

- Max **3 entities** writable on a single screen.
- Max **12 editable fields** visible simultaneously (use tabs/sections — see `screen-patterns.md` §12).
- Max **5 action buttons** (split: primary visible + secondary overflow).

A violation of any cap is a Conflicted SU row that must be resolved — typically by splitting the screen or moving optional fields into an accordion/secondary tab.

---

## When in doubt

- Default to **gallery + form** rather than a single dense screen — easier to evolve.
- Default to **role-conditional visibility** rather than separate screens, *unless* roles edit truly disjoint field sets.
- Default to **approval-as-action-on-form** rather than a dedicated approval screen — see `screen-patterns.md` §5.
