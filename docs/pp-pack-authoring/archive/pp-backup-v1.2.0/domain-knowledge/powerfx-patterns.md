# powerfx-patterns — Power FX Patterns and Validation Guide

**Source:** v33/v34 `ref-05-powerfx.md` (465 lines) + `ref-05b-powerfx-validator.md` (172 lines), consolidated.
**Consumers:** `formula-cell` (delegation-safe rule derivation), `design-spec-cell` (handoff to Claude Design with delegation-aware Power FX patterns).
**Token tier:** WARM (loaded only by cells that declare it in `pack.yaml § domain_knowledge_load`).

This file addresses gap 5 from service-desk-prioritization run: delegation traps not surfaced in design-spec, validation sequence absent. Every formula claim emitted by `formula-cell` must cross-reference at least one section here.

---

## § 1 — Delegation (THE MOST CRITICAL CONCEPT)

Delegation means the data source processes the operation server-side.
Non-delegable operations are processed client-side, limited to 500 records
(default) or 2000 (max setting in App.OnStart: `Set(App.MaxAppCacheSize, 2000)`).

### 1.1 — Delegable operations — Dataverse connector

| Operation | Delegable | Notes |
|---|---|---|
| Filter on Choice column | Yes | |
| Filter on Text (equals) | Yes | |
| Filter on Text (StartsWith) | Yes | |
| Filter on Text (Contains) | Partial | Only on primary name column |
| Filter on Number | Yes | |
| Filter on Date | Yes | |
| Filter on Lookup | Yes | If FK column is indexed |
| Filter on Calculated column | No | Never delegable |
| Search | Partial | Only on specific columns (searchable = Yes) |
| Sum(Table, Column) | Yes | |
| Average(Table, Column) | Yes | |
| Max/Min(Table, Column) | Yes | |
| CountRows(Table) | Yes | |
| CountIf(Table, delegable cond) | Yes | Condition must be delegable |
| Sort(Table, indexed col) | Yes | |
| Sort on non-indexed col | Partial | Client-side, 500 limit |

### 1.2 — Delegable operations — SharePoint connector

| Operation | Delegable | Notes |
|---|---|---|
| Filter on indexed column (equals) | Yes | Column must be indexed |
| Filter on non-indexed column | No | 500 limit |
| Sum, Average, Max, Min | No | Always non-delegable on SharePoint |
| CountRows | Yes | |
| CountIf with simple condition | Partial | Only on indexed column |
| Search | No | Never delegable on SharePoint |
| Sort on indexed column | Yes | |

---

## § 2 — Delegation Workarounds

### 2.1 — Collection preload (most common)
```powerfx
// In App.OnStart or Screen.OnVisible:
ClearCollect(colQuotes,
 Filter(cr_quote, cr_status = "Active") // delegable condition
);
// Then in gallery — no delegation limit:
Filter(colQuotes, Lower(cr_customername) = Lower(txtSearch.Text))
```

### 2.2 — Chunked loading for large tables
```powerfx
// Load in batches (for tables > 2000 records)
Clear(colAllData);
Collect(colAllData, FirstN(cr_largetable, 2000));
// If more records: implement pagination with cursor
```

### 2.3 — Server-side pre-filtering
```powerfx
// Filter at source level (delegable) before any non-delegable operation
ClearCollect(colThisMonthData,
 Filter(cr_quote,
 Year(cr_createdon) = Year(Today) &&
 Month(cr_createdon) = Month(Today)
 )
);
// Then aggregate locally
Sum(colThisMonthData, cr_totalvalue)
```

---

## § 3 — Validation Sequence (run on EVERY emitted formula)

Execute in this exact order. Each step may modify the formula before the next check.

### 3.1 — Syntax checks (auto-fix or downgrade)

**A1 Bracket Balance** — Count opening and closing `(` `)` `{` `}` `[` `]`. All must balance. If single missing bracket is unambiguous → auto-fix; else → downgrade to ⚠️ Ref.

**A2 String Literal Closure** — Every `"` must have a matching pair. Odd count → syntax error.

**A3 Semicolons vs Commas** — Power Fx uses `;` as separator in European locales and `,` in US locales. Use `;` by default (align with `meta.language`). If `meta.language = "en"` → use `,`. Never mix separators. Mixed → auto-correct to dominant separator.

**A4 Function Name Validity** — Every function name must exist in Power Fx. Common traps:

| Invalid | Correct | Notes |
|---|---|---|
| VLOOKUP | LookUp | Power Fx equivalent |
| SUMIF / SUMIFS | Sum(Filter(...)) | Decompose into Filter + Sum |
| COUNTIF / COUNTIFS | CountRows(Filter(...)) | Decompose into Filter + CountRows |
| CONCATENATE | Concat or `&` operator | |
| IFERROR | IfError | Case-sensitive |
| ISBLANK | IsBlank | Case-sensitive |
| LEFT / RIGHT / MID | Left / Right / Mid | Case-sensitive |
| TEXT (Excel-style) | Text(value, format) | Format strings differ |
| SUMPRODUCT | NEVER in Power Fx | Always Power Automate |
| NPV / IRR / PMT / RATE | NEVER in Power Fx | Always Power Automate |

**A5 Property-Context Compatibility** — Each Power Fx formula has a target property. Validate compatibility:

| Property | Accepts | Does NOT accept |
|---|---|---|
| Text | String expression | Table, Record, Void |
| Default | Matching type (text/number/date) | Table, Void |
| Items | Table expression | Scalar, Void |
| OnSelect | Action sequence (Set, Navigate, Patch, etc.) | Bare value expressions |
| Visible | Boolean expression | Table, Void, Action |
| DisplayMode | DisplayMode enum (Edit/View/Disabled) | Free text, Boolean |
| Fill / Color | Color value or RGBA | String, Number |
| OnChange | Action sequence | Bare value expressions |

If formula type mismatches property type → downgrade to ⚠️ Ref with note.

### 3.2 — Schema Reference Validation

**B1 Entity Name Check** — Every `DataSourceName` referenced MUST exist in `schema.entities_generated[]`. Extract via patterns: `Filter(EntityName,...)`, `EntityName.ColumnName`, `Collect(EntityName,...)`, `Patch(EntityName,...)`. If not found → flag as `SCHEMA_MISMATCH`. Never proceed with placeholder.

**B2 Column Name Check** — Every `ColumnName` referenced MUST exist in the corresponding entity's column list. Check for case mismatch (PascalCase vs camelCase) — auto-correct case if match found.

**B3 Naming Convention Consistency** — All names must follow `meta.naming_convention` (PascalCase / snake_case / Prefixed). Scan all entity/column references. Any deviation → auto-correct + note.

### 3.3 — Logic Validation

**C1 Division Zero-Guard** — Every division MUST be zero-guarded:
- Pattern: `A / B` → MUST be `If(B <> 0, A / B, 0)` or equivalent
- Nested: `A / (B * C)` → guard the full denominator: `If(B * C <> 0, A / (B * C), 0)`

Unguarded division → auto-correct.

**C2 Blank Handling** — LookUp results can be blank. If used in arithmetic → wrap with `Coalesce`:
- `LookUp(Table, condition).Field * X` → `Coalesce(LookUp(Table, condition).Field, 0) * X`
- For text: `Coalesce(LookUp(...).TextField, "")`

**C3 Delegation Safety** — Check every `Filter`, `Search`, `LookUp`, `CountRows(Filter)`, `Sum(Filter)`:
- Is the filter column indexed / delegable for the data source?
- SharePoint delegable: ID, Title, Created, Modified, lookup columns, choice columns, yes/no, single-line text (with limitations)
- Dataverse delegable: most columns except multi-select, file, image
- SQL: all columns delegable via server-side query

If non-delegable → flag `⚠️ DELEGATION` and provide collection workaround:
```powerfx
// Workaround — preload to collection
ClearCollect(colLocalData, EntityName);
Filter(colLocalData, NonDelegableColumn = "value")
```

**C4 Nested If Depth** — Power Fx supports nested If but readability degrades > 3 levels.
- ≤3 nested If → OK
- 4+ nested If → refactor suggestion: use `Switch` or intermediate variables with `With`

**C5 Anti-Pattern Detection**

| Anti-Pattern | Detection | Correction |
|---|---|---|
| `Filter(Filter(Table, A), B)` | Nested Filter | Flatten: `Filter(Table, A && B)` |
| `If(condition, true, false)` | Redundant If | Simplify: `condition` |
| `If(condition, false, true)` | Redundant If | Simplify: `!condition` |
| `Text(Value(textField),...)` | Double conversion | Check if intermediate conversion needed |
| `CountRows(Filter(Table, condition)) > 0` | Inefficient existence check | Use `!IsEmpty(Filter(Table, condition))` |
| `Set(varX, LookUp(...)); Set(varY, varX.Field)` | Unnecessary intermediate | `Set(varY, LookUp(...).Field)` with Coalesce |

### 3.4 — Validation Report Format

After validating all formulas, produce summary:

```
POWER FX VALIDATION
Total formulas: [N]
 Passed all checks: [N]
 Auto-corrected: [N] ([list corrections])
 Downgraded to Ref: [N] ([list reasons])
 Requires Power Automate: [N]

Schema mismatches: [N] — [list: formula_id → missing entity/column]
Delegation warnings: [N] — [list: formula_id → non-delegable column]
Zero-guard additions: [N]
Coalesce additions: [N]
Anti-patterns fixed: [N]
```

If `schema_mismatches > 0` → MAJOR flag in confidence scoring.
If `delegation_warnings > 0` → each is a MINOR flag.

---

## § 4 — Trap Catalogue

### Trap 1 — Delegation (silent data loss)
**Risk:** Filter/Search on non-delegable column returns max 500/2000 records silently.
**Detection:** Any formula using Filter where the condition column is: calculated, non-indexed, or uses Contains/text functions.
**Fix:** Preload into collection with delegable filter; then filter locally.
**Severity:** HIGH — causes wrong results at scale, no error shown to user.

### Trap 2 — SUMPRODUCT (no equivalent)
**Risk:** No Power Fx equivalent. Any attempt produces wrong results.
**Detection:** Any Excel formula starting with SUMPRODUCT.
**Fix:** Always Power Automate flow with running total pattern.
**Severity:** HIGH — cannot be translated to Power Fx.

### Trap 3 — WORKDAY (calendar dependency)
**Risk:** Power Fx approximation ignores public holidays.
**Detection:** WORKDAY or NETWORKDAYS in any formula.
**Fix:** Document approximation limitation. If holiday accuracy required: PA flow with cr_holidays reference table.
**Severity:** MEDIUM — results may be incorrect for holiday periods.

### Trap 4 — Financial functions (not in Power Fx)
**Risk:** NPV, IRR, PMT, RATE, FV, PV do not exist in Power Fx.
**Detection:** Any Excel financial function.
**Fix:** Always Power Automate (or T-SQL for Azure SQL path).
**Severity:** HIGH — cannot be translated.

### Trap 5 — Circular references
**Risk:** Power Fx and relational databases cannot handle circular dependencies.
**Detection:** Sheet A depends on Sheet B which depends on Sheet A.
**Fix:** Identify independent variable. Break circle. One direction becomes manual input.
**Severity:** HIGH — must be resolved before design proceeds.

### Trap 6 — Unguarded division
**Risk:** Division by zero crashes the formula; shows error in the control.
**Detection:** Any `/` operator in a formula.
**Fix:** Always: `If(divisor <> 0, numerator / divisor, 0)`.
**Severity:** MEDIUM — causes visible errors when denominator is zero.

### Trap 7 — Connector compatibility (Dataverse vs SharePoint)
**Risk:** Power Fx functions behave differently depending on the connector.
**Key differences:** SharePoint: Sum/Average/Max/Min NOT delegable. Search NOT delegable. CountIf limited.
**Fix:** For SharePoint: use collection preloading for all aggregations.
**Severity:** MEDIUM — affects apps switching data sources.

### Trap 8 — Concurrent edit conflicts
**Risk:** Two users editing the same record simultaneously — last save wins.
**Detection:** Any collaborative process with shared records.
**Fix:** Dataverse handles optimistic concurrency natively. SharePoint: document limitation. Add Last Modified timestamp check before Patch.
**Severity:** LOW — inform users, handle gracefully.

---

## § 5 — Standard Patterns

### 5.1 — Patch (Create/Edit) — complete pattern

```powerfx
// Save button OnSelect — complete pattern
// Step 1: Validate
If(
 IsBlank(txtName.Text),
 UpdateContext({errName: "Campo obrigatório"}); UpdateContext({varFormValid: false}),
 UpdateContext({errName: ""}); UpdateContext({varFormValid: true})
);

// Step 2: Cross-field validations
If(
 !IsBlank(dtEndDate.SelectedDate) && dtEndDate.SelectedDate < dtStartDate.SelectedDate,
 Notify("A data de fim não pode ser anterior à data de início.", NotificationType.Error);
 UpdateContext({varFormValid: false})
);

// Step 3: Patch only if valid
If(
 varFormValid,
 If(
 IsBlank(varSelectedId), // Create vs Edit
 Patch(cr_entity, Defaults(cr_entity), {
 cr_name: txtName.Text,
 cr_status: "Draft",
 cr_createdon: Now,
 cr_ownerid: varCurrentUserEmail
 }),
 Patch(cr_entity, LookUp(cr_entity, cr_id = varSelectedId), {
 cr_name: txtName.Text,
 cr_modifiedat: Now,
 cr_modifiedby: varCurrentUserEmail
 })
 );
 Notify("Guardado com sucesso.", NotificationType.Success);
 Navigate(ListScreen, ScreenTransition.Fade)
)
```

### 5.2 — Navigation

```powerfx
// Simple navigation
Navigate(TargetScreen, ScreenTransition.Fade)

// Navigation with context (pass selected record)
Navigate(DetailScreen, ScreenTransition.Fade, {varSelectedRecord: ThisItem})

// Back navigation
Back

// Navigate and reset form
Navigate(FormScreen, ScreenTransition.None);
ResetForm(frmEntity)
```

### 5.3 — Gallery (filter / sort / search)

```powerfx
// Filterable, searchable gallery
Filter(
 cr_entity,
 // Text search (delegable on searchable columns)
 (IsBlank(txtSearch.Text) || StartsWith(cr_name, txtSearch.Text)) &&
 // Status filter (delegable Choice column)
 (ddStatus.Selected.Value = "All" || cr_status = ddStatus.Selected.Value) &&
 // Role-based row filter (delegable on owner field)
 (varCurrentUserRole <> "Comercial" || Lower(cr_ownerid) = varCurrentUserEmail)
)

// Sort
SortByColumns(
 Filter(cr_entity,...),
 "cr_createdon",
 If(toggleSortAsc.Value, SortOrder.Ascending, SortOrder.Descending)
)
```

### 5.4 — Notification

```powerfx
// Success
Notify("Operação concluída com sucesso.", NotificationType.Success, 3000)

// Error
Notify("Erro: " & errMsg, NotificationType.Error, 5000)

// Warning
Notify("Atenção: " & warnMsg, NotificationType.Warning, 4000)

// Information
Notify("Informação: " & infoMsg, NotificationType.Information, 3000)
```

### 5.5 — Audit Log (mandatory for Approve, Delete, Export)

```powerfx
// Always log before the action, not after (action may fail)
Patch(cr_auditlog, Defaults(cr_auditlog), {
 cr_action: "Approve", // "Approve" | "Delete" | "Export"
 cr_entity_name: "cr_quote",
 cr_record_id: Text(ThisItem.cr_quoteid),
 cr_record_name: ThisItem.cr_name,
 cr_performed_by: varCurrentUserEmail,
 cr_performed_at: Now,
 cr_notes: txtApprovalNotes.Text
});

// Then perform the action
Patch(cr_quote, ThisItem, {
 cr_status: "Approved",
 cr_approved_by: varCurrentUserEmail,
 cr_approved_at: Now
});

Notify("Aprovado com sucesso.", NotificationType.Success)
```

### 5.6 — Error Handling UX

**IfError with fallback value (display):**
```powerfx
// Label.Text — show fallback instead of crashing
IfError(
 ThisItem.cr_total / ThisItem.cr_quantity,
 0
)
```

**IfError with Notify (save operations):**
```powerfx
// Button.OnSelect — catch Patch failures
IfError(
 Patch(cr_entity, ThisItem, { cr_status: "Approved" });
 Notify("Aprovado com sucesso.", NotificationType.Success);
 Navigate(ListScreen, ScreenTransition.Fade),

 Notify("Erro ao guardar: " & FirstError.Message, NotificationType.Error, 5000)
)
```

**Validate before save (multi-field):**
```powerfx
// Collect all errors before showing — do not stop at first
UpdateContext({
 errName: If(IsBlank(txtName.Text), "Campo obrigatório", ""),
 errDate: If(dtEnd.SelectedDate < dtStart.SelectedDate, "Data inválida", ""),
 errAmount: If(Value(txtAmount.Text) <= 0, "Valor deve ser positivo", "")
});

// Check if any error exists
If(
 IsBlank(errName) && IsBlank(errDate) && IsBlank(errAmount),
 // All valid → save
 Patch(cr_entity, Defaults(cr_entity), { /* fields */ }),
 // Has errors → do not save, just show
 Notify("Corrija os erros antes de guardar.", NotificationType.Error)
)
// Each field has a Label below it: Visible = !IsBlank(errName), Text = errName, Color = danger
```

### 5.7 — Collection Manipulation

**AddColumns — enrich data with computed fields:**
```powerfx
ClearCollect(colEnriched,
 AddColumns(
 Filter(cr_orders, cr_status = "Active"),
 "TotalWithTax", cr_total * 1.23,
 "DaysOpen", DateDiff(cr_createdon, Today, TimeUnit.Days),
 "IsOverdue", DateDiff(cr_createdon, Today, TimeUnit.Days) > 30
 )
)
```

**RenameColumns — standardise for export or display:**
```powerfx
ClearCollect(colForExport,
 RenameColumns(
 colEnriched,
 "cr_name", "Nome",
 "cr_status", "Estado",
 "TotalWithTax", "Total c/ IVA"
 )
)
```

**GroupBy — aggregate by category:**
```powerfx
ClearCollect(colByCategory,
 GroupBy(colEnriched, "cr_category", "Items")
)
// Result: table with cr_category + Items (sub-table)
// Access: ForAll(colByCategory, { Category: cr_category, Count: CountRows(Items) })
```

**DropColumns — remove sensitive fields before display:**
```powerfx
ClearCollect(colPublic,
 DropColumns(colEnriched, "cr_internal_notes", "cr_cost_price", "cr_margin")
)
```

**Distinct — unique values for filter dropdowns:**
```powerfx
Distinct(cr_orders, cr_category)
// Returns single-column table of unique categories
// Use in Dropdown.Items or ComboBox.Items
```

### 5.8 — Loading State

**Screen loading with spinner:**
```powerfx
// Screen.OnVisible
UpdateContext({varLoading: true});
ClearCollect(colData, Filter(cr_entity, cr_status = "Active"));
UpdateContext({varLoading: false})

// Spinner control: Visible = varLoading
// Gallery: Visible = !varLoading
// Empty state label: Visible = !varLoading && CountRows(colData) = 0
```

**Save button with processing state:**
```powerfx
// Button.OnSelect
UpdateContext({varSaving: true});
IfError(
 Patch(cr_entity, ThisItem, { cr_status: "Submitted" });
 Notify("Submetido.", NotificationType.Success),
 Notify("Erro: " & FirstError.Message, NotificationType.Error)
);
UpdateContext({varSaving: false})

// Button.Text = If(varSaving, "A guardar...", "Submeter")
// Button.DisplayMode = If(varSaving, DisplayMode.Disabled, DisplayMode.Edit)
```

---

## § 6 — Context Variable Management

### 6.1 — Naming convention

| Prefix | Scope | Example | Use |
|---|---|---|---|
| `var` | UpdateContext (screen) | `varSelectedId`, `varLoading` | Screen-local state |
| `gbl` | Set (global) | `gblCurrentUser`, `gblUserRole` | App-wide state |
| `col` | ClearCollect | `colOrders`, `colFiltered` | In-memory datasets |
| `err` | UpdateContext | `errName`, `errDate` | Validation error messages |

### 6.2 — App.OnStart — standard global init

```powerfx
// 1. User context
Set(gblCurrentUser, User);
Set(gblCurrentUserEmail, Lower(User.Email));

// 2. Role detection (from security role list or SharePoint group)
Set(gblUserRole,
 LookUp(lst_UserRoles, Lower(Email) = gblCurrentUserEmail, Role)
);
If(IsBlank(gblUserRole), Set(gblUserRole, "Viewer")); // Fallback

// 3. Reference data preload (small tables — always safe)
ClearCollect(colCategories, lst_Categories);
ClearCollect(colStatuses, lst_Statuses);
ClearCollect(colParameters, lst_Parameters);

// 4. App settings
Set(gblAppVersion, "1.0");
Set(gblDelegationWarning, 2000); // Match App Settings → Delegation limit
```

### 6.3 — Screen.OnVisible — standard screen init

```powerfx
// 1. Reset search and filters
UpdateContext({
 varSearchText: "",
 varFilterStatus: "All",
 varLoading: true,
 varSelectedRecord: Blank
});

// 2. Load data (delegable filter first)
ClearCollect(colScreenData,
 Filter(lst_Requests, Status <> "Cancelled")
);

// 3. Ready
UpdateContext({varLoading: false})
```

---

## § 7 — Control Property Reference

| Use case | Control | Property | Notes |
|---|---|---|---|
| Display calculated value | Label | Text | Most common |
| Input field default | TextInput | Default | Pre-populate |
| Date field default | DatePicker | DefaultDate | |
| Filter gallery/table | Gallery | Items | With Filter |
| Load dropdown options | Dropdown/ComboBox | Items | Reference table |
| Validate before save | Button | OnSelect | Before Patch |
| React to field change | TextInput/Dropdown | OnChange | |
| Conditional visibility | Any control | Visible | Role/state based |
| Enable/disable control | Any control | DisplayMode | Edit/View/Disabled |
| Conditional formatting | Label/Icon | Fill/Color | Status colours |
