# screen-consolidation-rules — Decision Tree for App Screen Consolidation

**Source:** transplanted 2026-05-28 from the previous-aisa references (`decision-trees/dt-04-screen-consolidation.md`).
**Consulted by:** `lens-technology`, `solution-architect`, `implementation-spec` and `claude-design-brief` deliverable templates.
**Phase eligibility:** Options + Decision only.
**Companion file:** [`screen-patterns.md`](screen-patterns.md) — the full Canvas screen-pattern catalogue. This file is the *decision tree*; that file is the *catalogue*.

The rules below convert the engagement's field inventory, role list, and approval semantics into a screen plan. Apply them after the architectural branch is chosen (sharepoint-first, dataverse-first, hybrid) and before the `implementation-spec` is written.

---

## Inputs to the tree

- All editable/viewable fields surfaced by the data lens (Confirmed or Assumed SU rows).
- Source entities and their relationships (data lens).
- Target roles and their approval authority (governance lens + security-patterns).
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
