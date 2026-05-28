# sharepoint-reference — SharePoint Online Complete Reference

**Source:** transplanted 2026-05-28 from the previous-aisa references (`ref-04-sharepoint.md`).
**Consulted by:** `lens-technology`, `solution-architect`, `implementation-spec` and `claude-design-brief` deliverable templates.
**Phase eligibility:** Options + Decision only.

Authoritative SharePoint reference for the pp pack. Use when the chosen branch is `sharepoint-first` (low volume, M365-only licensing, fast first delivery) or as the secondary/attachments side of a `hybrid` branch. Cross-reference with [`decision-tree.md`](../decision-tree.md) for the hard-gates that disqualify SharePoint at high volume.

---

## COLUMN TYPES — Use Exactly These Names

| Type Name | Use When | Notes |
|---|---|---|
| Single line of text | Short text, codes, names | Default max 255 chars |
| Multiple lines of text | Notes, descriptions | Plain text or Enhanced Rich Text |
| Number | Integers and decimals | Specify decimal places |
| Currency | Monetary values | Specify locale and currency |
| Date and Time | Dates | Specify: Date Only or Date & Time |
| Yes/No | Boolean flags | Renders as checkbox |
| Person or Group | User references | Single or multiple |
| Hyperlink or Picture | URLs | Hyperlink or Picture display |
| Choice | Fixed option list | List all choices |
| Lookup | FK to another list | Specify target list and column |
| Calculated | Formula-derived | See supported functions below |
| Managed Metadata | Taxonomy terms | Specify term set |

---

## HARD LIMITS — Never Violate

| Limit | Value | Consequence if violated |
|---|---|---|
| Indexed columns per list | **12 maximum** | SharePoint blocks additional indexes |
| List view threshold | **5,000 items** | Views returning >5k items are blocked |
| Lookup columns per list | **12 maximum** | Includes system lookups (Created By, Modified By = 2 already) |
| Effective max custom lookups | **10** | 12 total - 2 system = 10 custom |
| Calculated column references | Cannot ref other calculated columns | Formula fails silently |
| List item size | 256KB | Avoid many large text columns |
| Max list items | 30 million | Architecture concern |

These hard limits drive the disqualification gates in [`decision-tree.md`](../decision-tree.md): SharePoint is removed from the option set when `max_volume_per_entity > 30,000` rows, `formula_count > 100`, cross-list joins are required, or audit / multi-stage approval is mandatory.

---

## CALCULATED COLUMN — Supported Functions Only

SharePoint calculated columns use a subset of Excel functions. ONLY these work:

**Arithmetic:** `+`, `-`, `*`, `/`

**Text:**
`LEFT`, `RIGHT`, `MID`, `LEN`, `CONCATENATE`, `&`, `UPPER`, `LOWER`, `TRIM`,
`TEXT`, `VALUE`, `FIND`, `SEARCH`, `SUBSTITUTE`, `REPT`, `EXACT`, `FIXED`

**Date:**
`TODAY`, `NOW`, `YEAR`, `MONTH`, `DAY`, `DATE`, `DATEDIF`, `DAYS360`,
`HOUR`, `MINUTE`, `SECOND`, `TIME`, `WEEKDAY`, `NETWORKDAYS`, `WORKDAY`

**Logic:**
`IF`, `AND`, `OR`, `NOT`, `ISNUMBER`, `ISBLANK`, `ISERROR`, `ISTEXT`,
`ISNULL`, `TRUE`, `FALSE`

**Math:**
`ROUND`, `ROUNDUP`, `ROUNDDOWN`, `INT`, `ABS`, `MOD`, `CEILING`, `FLOOR`,
`MAX`, `MIN`, `AVERAGE`, `SUM`

**NOT supported (use Power Automate instead):**
`VLOOKUP`, `INDEX`, `MATCH`, `SUMIF`, `COUNTIF`, `SUMPRODUCT`, `INDIRECT`,
`OFFSET`, any financial function, any cross-list reference

---

## INDEXED COLUMN PLANNING

System columns already indexed (count toward limit):
- Title (1)
- ID (system — does not count)
- Created By (1) — if used in views
- Modified By (1) — if used in views

**Budget remaining for custom columns:** typically 9-10.

**Always index:**
- Status/State columns (used in almost every view filter)
- Date columns used for filtering (e.g., Created On, Due Date)
- Lookup columns that appear in view filters

**Indexing decision matrix:**
| Column | Volume >5k? | Used in filter? | Used in sort? | Index? |
|---|---|---|---|---|
| Status | Yes | Yes | No | Yes |
| Total Value | Yes | No | Yes | Yes |
| Category | Yes | Yes | No | Yes |
| Notes | Any | No | No | No |

---

## SHAREPOINT GROUPS AND PERMISSIONS

```
Site Permission Groups:
 [Site Name] Owners → Full Control (Admin role)
 [Site Name] Members → Contribute (standard edit access)
 [Site Name] Visitors → Read (read-only access)
 [Site Name] [Custom] → Custom level (role-specific)

Custom Permission Levels (Site Settings → Permission Levels):
 Name: [Role]_Access
 Permissions: Select specifically — Contribute minus Delete for standard users
```

**Item-level permissions (Advanced Settings):**
- Read: "Only their own" / "All items"
- Edit: "Only their own" / "All items"

**Override:** Members and Owners group bypass item-level restrictions.

---

## SENSITIVE COLUMN PROTECTION (SharePoint has no native column-level security)

Implement via Power Automate protection flow:
```
TRIGGER: When item is modified
CONDITION: [SensitiveColumn] changed AND modifier NOT IN [AuthorisedGroup]
ACTION:
 1. Get previous version of item
 2. Update item: restore [SensitiveColumn] to previous value
 3. Send notification: "You do not have permission to modify [FieldName]"
```

This is one of the structural weaknesses that makes SharePoint inappropriate for entities with strong column-level access requirements — surface this in the Options-phase trade-off when proposing `sharepoint-first`.

---

## EDIT-OWN PATTERN (SharePoint has no native row-level security for editing)

Implement via Power Automate:
```
TRIGGER: When item is modified
CONDITION: Modified By != Created By AND Modified By NOT IN [Manager/Admin group]
ACTION:
 1. Restore previous version
 2. Notify user: "You can only edit your own items"
```
Note: Race condition possible if two users submit simultaneously — document this limitation.

---

## VALIDATION FORMULAS

**Column-level (validates one column):**
```
=[ColumnInternalName] >= 0
=[ColumnInternalName] <= 100
=LEN([ColumnInternalName]) >= 3
```

**List-level (validates entire item — can reference multiple columns):**
```
=[EndDate] >= [StartDate]
=OR([Status]<>"Approved", AND([Status]="Approved", LEN(TRIM([ApprovalNote]))>0))
```

User message: plain language description shown when validation fails.

---

## LIST CREATION ORDER

Create in this sequence to satisfy Lookup dependencies:
1. Reference lists (looked up by others, no outbound lookups)
2. Parent lists
3. Child lists (contain Lookup columns)

---

## SITE COLUMNS (Reusable Columns)

Create as Site Column when the same column appears in 3+ lists:
- Ensures consistent naming, type, and choice options across lists
- Change once, update everywhere
- Navigation: Site Settings → Site Columns → Create

---

## SHAREPOINT + POWER AUTOMATE CALCULATION PATTERNS

Since SharePoint cannot do complex calculations natively:

**Pattern 1 — On-item-change flow:**
```
TRIGGER: When item is created or modified
ACTIONS:
 Get item → Calculate → Update item with result
RISK: Loop prevention needed (check if value already correct before updating)
```

**Pattern 2 — Scheduled aggregation:**
```
TRIGGER: Scheduled (e.g., daily at 06:00)
ACTIONS:
 Get all items → ForAll: compute → Update each item
USE FOR: Rollups, summaries, cross-list aggregations
```

**Loop prevention:**
Add condition before update: `If(calculated_value != current_value, update, skip)`

---

## PERFORMANCE RULES

- Always create indexed columns before loading data (index creation on large list is slow)
- Use modern experience views (not classic) for better performance
- Limit view to columns actually needed — avoid SELECT *
- Use "Group by" sparingly on large lists — expensive without proper indexes
- Consider JSON column (Single line of text storing JSON) for semi-structured data that doesn't need filtering

---

## DELEGATION — SHAREPOINT CONNECTOR SPECIFICS

SharePoint connector delegation is much more limited than Dataverse. Plan for it.

### Delegable vs non-delegable (SharePoint connector in Canvas Apps)

| Operation | Delegable? | Condition |
|---|---|---|
| Filter (=, <>, <, >) on indexed column | Yes | Column MUST be indexed |
| Filter on non-indexed column | No | 500-item client-side limit |
| Filter with `in` operator | No | Always client-side |
| StartsWith on text column | Yes | Only on indexed single-line text |
| Contains / Search | No | Always client-side |
| Sort on indexed column | Yes | |
| Sort on non-indexed column | No | Client-side, 500 limit |
| CountRows | Yes | |
| Sum / Average / Max / Min | No | Always non-delegable |
| CountIf | No | Always non-delegable |
| LookUp on indexed column | Yes | Equivalent to Filter + First |
| Distinct | No | Always client-side |

### Workaround patterns

**Pattern 1 — Pre-filtered collection (most common):**
```powerfx
// On Screen.OnVisible — use delegable filter to reduce dataset
ClearCollect(colActiveItems,
 Filter(lst_Requests, Status = "Active") // indexed column = delegable
);
// Gallery uses local collection — no delegation limits
Filter(colActiveItems, StartsWith(Title, txtSearch.Text))
```

**Pattern 2 — Paginated loading (lists > 2000 items):**
```powerfx
// SharePoint returns max 2000 per call (even with delegation)
// For larger datasets, use Power Automate to pre-aggregate
// or partition data across lists by year/department
```

**Pattern 3 — Aggregation via Power Automate:**
```
// SUM/AVERAGE/COUNT on SharePoint lists → never Canvas App Power Fx
TRIGGER: Button click (from Canvas App via Power Automate connector)
INPUT: filter parameters (status, date range)
ACTIONS:
 Get items (with OData filter) → Select (extract column) → Compose (aggregate)
RETURN: { total: 125000, count: 47, average: 2659.57 }
```

---

## POWER AUTOMATE — SHAREPOINT CONNECTOR PATTERNS

### OData filter syntax (Get Items action)

| Need | OData Filter | Notes |
|---|---|---|
| Status equals | `Status eq 'Active'` | Single quotes for text |
| Date after | `Created ge '2024-01-01T00:00:00Z'` | ISO 8601 format |
| Number greater | `Amount gt 1000` | No quotes for numbers |
| AND conditions | `Status eq 'Active' and Amount gt 1000` | Lowercase `and` |
| OR conditions | `(Status eq 'Draft') or (Status eq 'Pending')` | Parentheses required |
| Lookup column | `Department/Id eq 5` | `/Id` suffix for lookup FK |
| Person column | `AssignedTo/EMail eq 'user@company.com'` | `/EMail` for person |
| Null check | `ApprovedDate eq null` | Lowercase `null` |
| StartsWith | `startswith(Title,'PRJ')` | Function syntax |
| Year of date | `year(Created) eq 2024` | Date functions available |

**Top N pattern (avoid loading all items):**
- Get items → Top Count: 100 → Order By: `Modified desc`
- Always set Top Count even for "get all" — default is 100, max per page is 5000

**Pagination for >5000:**
- Settings → Pagination: ON → Threshold: 100000
- Performance: each page = 1 API call. 50K items = 10 calls = ~30s minimum

### Create/Update Item with Lookup

```
Create item:
 Site: [site URL]
 List: lst_RequestLines
 Title: @{triggerBody?['Title']}
 RequestId: @{triggerBody?['RequestId']} ← Lookup: pass the ID (integer)
 Amount: @{triggerBody?['Amount']}
```

Lookup fields accept the **integer ID** of the parent item — not the Title.

---

## VIEW STRATEGY FOR 5K THRESHOLD

Lists that will exceed 5,000 items MUST have filtered views that return <5K results.

**Standard view set:**

| View Name | Filter | Purpose | Indexed columns used |
|---|---|---|---|
| Active Items | Status = Active | Day-to-day work | Status |
| My Items | Created By = [Me] | Personal view | Created By |
| This Month | Created >= [1st of month] | Recent items | Created |
| Pending Approval | Status = Pending | Approver queue | Status |
| All (Admin) | None — but add column filters | Admin only | — |

**"All" view warning:** If total items > 5K and no filter applied, SharePoint blocks the view. Admin must use Search or indexed filters to access items.

---

## FORBIDDEN COLUMN NAMES

These cannot be used as internal column names — SharePoint reserves them and the API will reject or silently rewrite:

```
ID, Title, Created, Modified, Author, Editor, _UIVersionString, FileLeafRef,
FileRef, FileDirRef, FileSizeDisplay, FSObjType, ContentType, ContentTypeId,
GUID, owshiddenversion, _Level, _IsCurrentVersion, _ModerationStatus,
_ModerationComments, _CheckinComment, ItemChildCount, FolderChildCount,
AppAuthor, AppEditor
```

For display names, these terms can collide visually with system labels — prefer a domain-specific prefix (e.g., `Request_Title` instead of `Title`).

---

## ANTI-PATTERNS — Never Do These

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Lookup column referencing itself | Circular dependency — list creation fails | Use Choice or separate reference list |
| Calculated column referencing another calculated column | Silent failure — shows #REF or wrong value | Flatten formula into single calculated, or use PA flow |
| >10 custom Lookup columns on one list | Hard limit (12 total - 2 system). SharePoint blocks adding more | Consolidate lookups or use JSON column for denormalized refs |
| Using Person column for "Created By" audit | Redundant — system Created By exists. Wastes a Lookup slot | Use system Created By column |
| Relying on Content Approval for workflow | Limited to Approved/Pending/Rejected. No custom states | Use Choice column + Power Automate for custom state machine |
| Storing files as attachments on list items | No indexing, no metadata, 250MB item limit | Use Document Library with metadata columns |
| Using "Multiple lines of text" as searchable field | Not indexable, not filterable in views | Use "Single line of text" (255 char) + PA for overflow |

---

## GROWTH PLANNING — When Lists Approach Limits

| Threshold | Action |
|---|---|
| 2,000 items | Verify all views have indexed filters. Set Canvas App delegation warning limit. |
| 5,000 items | All views MUST filter on indexed columns. Create archive flow (move closed items to archive list). |
| 20,000 items | Consider partitioning by year/department. Evaluate migration to Dataverse or Azure SQL. |
| 100,000+ items | SharePoint is no longer appropriate as primary data store. Migrate to Dataverse/SQL. |

**Archive flow pattern:**
```
TRIGGER: Scheduled (monthly)
CONDITION: Status = "Closed" AND Modified < [6 months ago]
ACTIONS:
 Get items (filtered) → For each: Create item in lst_Archive → Delete from lst_Active
 Log: "[N] items archived"
```
