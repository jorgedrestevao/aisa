# Screen Design Patterns (Canvas standard)

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

**Scope:** Canvas standard components only. Rich/interactive prototyping decisions (layout density,
animation, modal vs side-peek, etc.) belong to Claude Design (claude.ai/design) — out of scope here.
The screen-plan decision tree is `screen-consolidation-rules.md`; this file is the catalogue.

---

## 1 · Design Principles

1. **Task-driven layout** — start from the user's task, not the data.
2. **One primary action per screen** — dominant button visible without scrolling.
3. **Read-before-edit** — Detail screens decide; Form screens change. Never blur.
4. **Surface state** — any record with a workflow shows current state prominently.
5. **Density proportional to frequency** — daily users dense, occasional users airy (§4).
6. **Fail safely** — every interactive screen has loading, empty, error states.
7. **Familiar anchors** — Excel users need a visual cue connecting to their old sheet (§9).

---

## 2 · Standard Screen Types

### 2.1 List Screen (Gallery)
Browse and select records. Components: search bar, filter dropdowns, sortable columns, pagination, "New" button, status badges.

### 2.2 Form Screen (Create/Edit)
Enter or edit a record. Components: field groups, inline validation, save/cancel, calculated fields read-only, mandatory asterisks.

### 2.3 Detail Screen (Read-only)
View a record and act on it. All fields read-only, status prominent, action buttons role-gated.

### 2.4 Dashboard Screen (KPIs + Summary)
Aggregated metrics. KPI cards, charts, drill-down links to list screens.

### 2.5 Admin / Configuration Screen
Reference table editing. Inline edit gallery + bulk actions per role.

---

## 3 · Status Badge Colours (Fluent 2 standard)

| State family | Background | Text | Border |
|---|---|---|---|
| Success / Approved | `#DFF6DD` | `#107C10` | `#9FD89F` |
| Pending / In Progress | `#FFF4CE` | `#C19B01` | `#F2D96A` |
| Rejected / Error | `#FDE7E9` | `#D13438` | `#EDA4A7` |
| Info / Submitted | `#EFF6FC` | `#0078D4` | `#9ACCF0` |
| Neutral / Draft | `#F0F0F0` | `#616161` | `#D6D6D6` |
| Severe / Overdue | `#F2E6DC` | `#8E562E` | `#D4A373` |

---

## 4 · Information Density Guidelines

| Density | Padding | Font | Use case |
|---|---|---|---|
| HIGH (compact) | 4px row, 8px field gap | 12px | Daily power users, ≥15 columns visible |
| NORMAL | 8px row, 12px field gap | 14px (default) | Weekly users, 8–14 columns |
| LOW (comfortable) | 12px row, 16px field gap | 14–16px | Monthly/occasional users, ≤8 columns |

**Density selection rules:**
- `process.frequency = "daily"` AND `column_count_active ≥ 15` → HIGH
- `process.frequency = "monthly"` OR users described as "non-technical" → LOW
- Default → NORMAL

---

## 5 · Approval Workflow — State Machine Design

Standard state pattern:
```
Draft → Submitted → [Reviewer Action]
  ├── Approved (terminal-positive)
  ├── Rejected (terminal-negative, with reason)
  └── Returned for Revision → Draft (loop)
```

**Rules:**
- State machine MUST be linear at the happy path (no parallel approvals at a single state — split into multiple state transitions instead)
- Every transition has: actor (role), trigger (button label), conditions (Power Fx guard), audit fields written
- Approval action buttons live on the entity Form screen — NOT on a separate "Approval screen"
- Audit fields per transition: `approved_by`, `approved_at`, `approval_notes` (or rejected_* counterparts)

---

## 6 · Navigation Patterns

### 6.1 Sidebar (standard)
Vertical sidebar with home + 3–7 primary screens. Role-gated visibility per the engagement's
screen-permission matrix (`security-craft.md` § Matrix 1).

### 6.2 Breadcrumb (deep navigation)
Used when navigation depth > 2 levels. Format: `Home > Quotes > Q-2024-001 > Edit`.

### 6.3 Modal / Panel (quick action without leaving context)
Used for confirmations, single-field edits, role switches. Never used for multi-field forms.

---

## 7 · User Journey Pattern

For each role, document journey as ordered task list:
```
ROLE: Sales Manager
1. Open Quote List (→ ListScreen)
2. Filter by status = "Submitted"
3. Open quote → review fields (→ DetailScreen)
4. Approve OR Return for Revision (→ FormScreen action)
5. Confirmation message + return to list
```

**Rule:** every user task carried by the blueprint MUST appear in at least one role's journey, OR be flagged
as an orphan.

---

## 8 · Field Validation — UX Rules

| Validation type | UX behaviour |
|---|---|
| Required | Asterisk on label; on save attempt with empty → red border + inline message |
| Format (email, phone, IBAN) | Validate on blur; red border + format hint |
| Range (numeric, date) | Validate on blur; show min/max inline |
| Cross-field (start ≤ end) | Validate on save; banner at top of form |
| Async (uniqueness check) | Validate on blur after 500ms debounce; spinner indicator |

**Rule:** every validation rule in the design MUST surface a user-facing message in the engagement's
language.

---

## 9 · Excel Transition — Familiar Anchors

Goal: every screen shows at least one element that connects to the user's mental model from the old Excel.

| Anchor pattern | Example |
|---|---|
| Sheet name → Screen title | "Pricing 2024" sheet → "Pricing 2024" screen title |
| Column header → Field label (verbatim) | Header "Cliente" → label "Cliente" (not "Customer Name") |
| Row colour rule → Conditional formatting | Excel red rows → red status badge |
| Total row at bottom → KPI card or footer | Excel SUM → footer card with total |

**Anti-pattern:** renaming columns "for clarity". The user knows their headers — keep them.

**Transition note format:** the screen's `familiar_anchor` carries the Excel reference; `key_differences`
documents what improves vs Excel.

---

## 10 · Form Layout Patterns

### 10.1 Two-column (tablet, default for NORMAL density)
Required fields in left column, optional in right. Sections divided by horizontal rule.

### 10.2 Field group pattern (reusable)
Group of 3–5 related fields under a section header. Used when form has ≥10 fields total.

### 10.3 Accordion sections (≥12 fields)
Collapsible sections. First section expanded by default. Used for settings or complex create flows.

---

## 11 · Loading, Empty, Error States

Every list/detail screen MUST implement all three:

| State | Trigger | UI |
|---|---|---|
| Loading | Initial fetch, filter change, action in flight | Skeleton rows or spinner |
| Empty | Zero records after fetch | Icon + message + primary action ("New" button) |
| Error | Fetch/save fails | Banner with error code + "Tentar novamente" / "Try again" button |

**Empty state messages must be context-aware:**
- "Sem propostas. Cria a tua primeira." (after first-time use)
- "Sem propostas que correspondam aos filtros aplicados." (after filter)

---

## 12 · Tab / Section Patterns

### 12.1 Tab pattern (Canvas)
Used when single screen needs ≥3 logical sub-views (e.g., quote with tabs: Items / Pricing / History).

### 12.2 When to use tabs vs separate screens
- Tabs: same primary entity, related data, user switches frequently
- Separate screens: different entities, different roles, navigation rare

---

## 13 · Responsive Design Notes (Canvas)

Canvas Apps responsiveness via container-based layout:
- Use `Container` controls with `LayoutMode = Vertical | Horizontal`
- Set `LayoutDirection = Auto` for adaptive behaviour
- Breakpoints: 1023px (tablet), 640px (phone)
- Sidebar collapses to hamburger menu < 768px

Detailed Canvas responsiveness patterns are documented in Microsoft's Power Apps docs — do not duplicate here.

---

## 14 · Screen Count and Field-Count Caps

### Screen count (team planning bands — not a platform limit)

| App size | Screens | Notes |
|---|---|---|
| Small | 3–5 | Single primary entity, 1–2 roles |
| Medium | 6–10 | 2–4 entities, 3–4 roles |
| Large | 11–15 | 5+ entities, complex approval flows |
| Very large | 16+ | The screen plan is itself the problem — re-run `screen-consolidation-rules.md`, and take any surface question back to the decision model |

These bands are a delivery-planning convention. Which application surface a screen count implies is not
decided here — see `application/application-surfaces.md`.

### Field-count thresholds per form screen

The full screen-consolidation decision tree lives in [`screen-consolidation-rules.md`](screen-consolidation-rules.md). The thresholds it produces and the hard caps it enforces are mirrored here for quick reference:

| Editable fields on the entity | Recommended layout |
|---|---|
| ≤ 8 editable + ≤ 4 read-only | Single form screen |
| 9–16 editable | Single form screen with sections / tabs |
| > 16 editable | Multi-step form (wizard) OR split into sub-screens |

### Hard caps (any violation is a Conflicted SU row)

- Max **3 entities** writable on a single screen.
- Max **12 editable fields** visible simultaneously (use tabs / sections — see §12).
- Max **5 action buttons** (split: primary visible + secondary overflow).

### Naming convention (entity-prefixed)

- Gallery: `[Entity]ListScreen`
- Form: `[Entity]FormScreen`
- Dashboard: `[Entity]DashboardScreen` or `DashboardScreen` (cross-entity)
- Approval: NOT a separate screen — action on `[Entity]FormScreen` (see §5).

---

## 15 · Per-Screen Spec Template

```
SCREEN: [ScreenName]
PURPOSE: [one sentence]
ROLES WITH ACCESS: [roles]

LAYOUT TYPE: [List | Form | Dashboard | Detail | Approval | Settings]
PRIMARY ENTITY: [schema_name]
SECONDARY ENTITIES: [list, if any]

CANVAS COMPONENTS:
  - Gallery: [purpose]
  - EditForm: [purpose]
  - Button: [actions]
  - Combobox: [data source]

KEY INTERACTIONS:
  - [interaction 1]

VALIDATION:
  - V01: [rule]

APPROVAL ACTIONS (if entity has workflow):
  - Submit: Draft → Submitted (Requester)

NAVIGATION ACTIONS:
  - Navigate(view-quote-list, Fade)

FAMILIAR ANCHOR: [what Excel element this mirrors]
TRANSITION NOTE: [what improves vs Excel]
```
