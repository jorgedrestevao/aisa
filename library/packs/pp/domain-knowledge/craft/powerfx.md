# Power Fx Craft — Validation Sequence, Traps and Standard Patterns

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

**Delegation is not owned here.** Delegability per operation and per data source, the client-side record
ceiling, and every related threshold belong to `data/query-and-delegation.md`. This file carries only the
*craft consequence*: how a formula is checked, and which pattern to write once that owner says an operation
is not delegable. Never restate a delegation figure from memory in a build artefact — read the owner.

---

## 1 — Validation sequence (run on EVERY emitted formula)

Execute in this exact order. Each step may modify the formula before the next check.

### 1.1 — Syntax checks (auto-fix or downgrade)

**A1 Bracket balance** — Count opening and closing `(` `)` `{` `}` `[` `]`. All must balance. If a single
missing bracket is unambiguous → auto-fix; else → downgrade to ⚠️ Ref.

**A2 String literal closure** — Every `"` must have a matching pair. Odd count → syntax error.

**A3 Semicolons vs commas** — Power Fx uses `;` as separator in European locales and `,` in US locales. Use
`;` by default (align with `meta.language`). If `meta.language = "en"` → use `,`. Never mix separators.
Mixed → auto-correct to the dominant separator.

**A4 Function name validity** — Every function name must exist in Power Fx. Common traps:

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
| SUMPRODUCT | No Power Fx equivalent | Implement in Power Automate |
| NPV / IRR / PMT / RATE | No Power Fx equivalent | Implement in Power Automate or T-SQL |

**A5 Property-context compatibility** — Each Power Fx formula has a target property. Validate compatibility:

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

If the formula type mismatches the property type → downgrade to ⚠️ Ref with a note.

### 1.2 — Schema reference validation

**B1 Entity name check** — Every `DataSourceName` referenced MUST exist in the engagement's generated entity
list. Extract via patterns: `Filter(EntityName,...)`, `EntityName.ColumnName`, `Collect(EntityName,...)`,
`Patch(EntityName,...)`. If not found → flag as `SCHEMA_MISMATCH`. Never proceed with a placeholder.

**B2 Column name check** — Every `ColumnName` referenced MUST exist in the corresponding entity's column
list. Check for case mismatch (PascalCase vs camelCase) — auto-correct case if a match is found.

**B3 Naming convention consistency** — All names must follow the engagement's naming convention
(PascalCase / snake_case / prefixed). Scan all entity/column references. Any deviation → auto-correct +
note. See `delivery-conventions.md` §1.

### 1.3 — Logic validation

**C1 Division zero-guard** — Every division MUST be zero-guarded:
- Pattern: `A / B` → MUST be `If(B <> 0, A / B, 0)` or equivalent
- Nested: `A / (B * C)` → guard the full denominator: `If(B * C <> 0, A / (B * C), 0)`

Unguarded division → auto-correct.

**C2 Blank handling** — LookUp results can be blank. If used in arithmetic → wrap with `Coalesce`:
- `LookUp(Table, condition).Field * X` → `Coalesce(LookUp(Table, condition).Field, 0) * X`
- For text: `Coalesce(LookUp(...).TextField, "")`

**C3 Delegation check** — Check every `Filter`, `Search`, `LookUp`, `CountRows(Filter)`, `Sum(Filter)`
against the delegation owner (`data/query-and-delegation.md`) for the data source actually chosen. This file
states no delegability fact and no record ceiling; it states only what to do with the owner's answer:

- Owner says delegable → leave the formula server-side. Do not preload.
- Owner says not delegable → flag `⚠️ DELEGATION` in the spec and write the collection workaround:

```powerfx
// Workaround — preload with a filter the owner confirms IS delegable, then filter locally
ClearCollect(colLocalData, Filter(EntityName, DelegableColumn = "value"));
Filter(colLocalData, NonDelegableColumn = "value")
```

- Owner says the answer is version- or configuration-dependent → the formula is not verifiable at design
  time. Record it as an open item for volume testing, not as a solved formula.

**C4 Nested If depth** — Readability degrades past ~3 nesting levels.
- ≤3 nested If → OK
- 4+ nested If → refactor: use `Switch`, or intermediate variables with `With`

**C5 Anti-pattern detection**

| Anti-pattern | Detection | Correction |
|---|---|---|
| `Filter(Filter(Table, A), B)` | Nested Filter | Flatten: `Filter(Table, A && B)` |
| `If(condition, true, false)` | Redundant If | Simplify: `condition` |
| `If(condition, false, true)` | Redundant If | Simplify: `!condition` |
| `Text(Value(textField),...)` | Double conversion | Check if the intermediate conversion is needed |
| `CountRows(Filter(Table, condition)) > 0` | Inefficient existence check | Use `!IsEmpty(Filter(Table, condition))` |
| `Set(varX, LookUp(...)); Set(varY, varX.Field)` | Unnecessary intermediate | `Set(varY, LookUp(...).Field)` with Coalesce |

### 1.4 — Validation report format

After validating all formulas, produce this summary:

```
POWER FX VALIDATION
Total formulas: [N]
 Passed all checks: [N]
 Auto-corrected: [N] ([list corrections])
 Downgraded to Ref: [N] ([list reasons])
 Requires Power Automate: [N]

Schema mismatches: [N] — [list: formula_id → missing entity/column]
Delegation warnings: [N] — [list: formula_id → column flagged by the delegation owner]
Zero-guard additions: [N]
Coalesce additions: [N]
Anti-patterns fixed: [N]
```

If `schema_mismatches > 0` → MAJOR flag in confidence scoring.
If `delegation_warnings > 0` → each is a MINOR flag.

---

## 2 — Trap catalogue

### Trap 1 — Delegation (silent wrong results)
**Risk:** a query the platform cannot delegate is evaluated over a truncated local page, and the result is
wrong with no error shown to the user.
**Detection:** any `Filter` / `Search` / aggregate whose condition column the delegation owner does not
confirm as delegable — typically calculated columns, non-indexed columns, and text-function conditions.
**Fix:** preload with a delegable filter, then filter locally (§1.3 C3). Test with realistic volume before
go-live.
**Severity:** HIGH — the failure is invisible at demo volume and appears only at production volume.
**Limit owner:** `data/query-and-delegation.md`.

### Trap 2 — SUMPRODUCT (no equivalent)
**Risk:** no Power Fx equivalent; any attempt produces wrong results.
**Detection:** any Excel formula using SUMPRODUCT.
**Fix:** Power Automate flow with the running-total pattern (`excel-translation.md`, `flow-craft.md`).
**Severity:** HIGH — cannot be translated to Power Fx.

### Trap 3 — WORKDAY / NETWORKDAYS (calendar dependency)
**Risk:** any Power Fx approximation ignores public holidays.
**Detection:** WORKDAY or NETWORKDAYS in a source formula.
**Fix:** document the approximation. If holiday accuracy is required, implement against an explicit holidays
reference table (flow or T-SQL).
**Severity:** MEDIUM — results are wrong around holiday periods only, which is how they survive testing.

### Trap 4 — Financial functions
**Risk:** NPV, IRR, PMT, RATE, FV, PV have no Power Fx equivalent.
**Detection:** any Excel financial function.
**Fix:** implement in Power Automate, or in T-SQL where the store is Azure SQL
(`sql-delivery-conventions.md`).
**Severity:** HIGH — cannot be translated in the app layer.

### Trap 5 — Circular references
**Risk:** neither Power Fx nor a relational schema resolves circular dependencies.
**Detection:** sheet A depends on sheet B which depends on sheet A.
**Fix:** identify the independent variable, break the circle; one direction becomes manual input.
**Severity:** HIGH — must be resolved before design proceeds.

### Trap 6 — Unguarded division
**Risk:** division by zero surfaces an error in the control.
**Detection:** any `/` operator.
**Fix:** always `If(divisor <> 0, numerator / divisor, 0)`.
**Severity:** MEDIUM — visible error whenever the denominator is empty or zero.

### Trap 7 — Connector-dependent behaviour
**Risk:** the same formula behaves differently depending on the data source behind it, so a formula validated
against one store is not validated for another.
**Detection:** any app whose data source changed after the formulas were written, or any formula reused
across stores.
**Fix:** re-run §1.3 C3 against the delegation owner for the *new* source; expect to add collection
preloads where an aggregation is not delegable there.
**Severity:** MEDIUM.
**Behaviour owner:** `data/query-and-delegation.md` and `data/store-boundaries.md`.

### Trap 8 — Concurrent edit conflicts
**Risk:** two users editing the same record — the later write silently overwrites the earlier one.
**Detection:** any collaborative process with shared records.
**Fix:** craft-side, read a Last Modified timestamp into context on open and compare it before `Patch`;
notify and reload on mismatch. Whether the store itself offers concurrency control is a platform question —
see `data/dataverse.md` / `data/store-boundaries.md`.
**Severity:** LOW with a timestamp check, HIGH without one on a contended record.

---

## 3 — Standard patterns

### 3.1 — Patch (create/edit) — complete pattern

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

### 3.2 — Navigation

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

### 3.3 — Gallery (filter / sort / search)

```powerfx
// Filterable, searchable gallery
// Every condition below must be checked against the delegation owner for the chosen source.
Filter(
 cr_entity,
 // Text search
 (IsBlank(txtSearch.Text) || StartsWith(cr_name, txtSearch.Text)) &&
 // Status filter
 (ddStatus.Selected.Value = "All" || cr_status = ddStatus.Selected.Value) &&
 // Role-based row filter
 (varCurrentUserRole <> "Comercial" || Lower(cr_ownerid) = varCurrentUserEmail)
)

// Sort
SortByColumns(
 Filter(cr_entity,...),
 "cr_createdon",
 If(toggleSortAsc.Value, SortOrder.Ascending, SortOrder.Descending)
)
```

### 3.4 — Notification

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

### 3.5 — Audit log (mandatory for Approve, Delete, Export)

```powerfx
// Always log before the action, not after (the action may fail)
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

Role-gated variants of the same three actions: `security-craft.md` § audit patterns.

### 3.6 — Error handling UX

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
// Collect all errors before showing — do not stop at the first
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

### 3.7 — Collection manipulation

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
Dropping a column in the client is presentation, not enforcement — see `security-craft.md` for the
server-side form.

**Distinct — unique values for filter dropdowns:**
```powerfx
Distinct(cr_orders, cr_category)
// Returns single-column table of unique categories
// Use in Dropdown.Items or ComboBox.Items
```

### 3.8 — Loading state

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

## 4 — Context variable management

### 4.1 — Naming convention

| Prefix | Scope | Example | Use |
|---|---|---|---|
| `var` | UpdateContext (screen) | `varSelectedId`, `varLoading` | Screen-local state |
| `gbl` | Set (global) | `gblCurrentUser`, `gblUserRole` | App-wide state |
| `col` | ClearCollect | `colOrders`, `colFiltered` | In-memory datasets |
| `err` | UpdateContext | `errName`, `errDate` | Validation error messages |

### 4.2 — App.OnStart — standard global init

```powerfx
// 1. User context
Set(gblCurrentUser, User);
Set(gblCurrentUserEmail, Lower(User.Email));

// 2. Role detection (from the role mapping the security design defines)
Set(gblUserRole,
 LookUp(lst_UserRoles, Lower(Email) = gblCurrentUserEmail, Role)
);
If(IsBlank(gblUserRole), Set(gblUserRole, "Viewer")); // Fallback

// 3. Reference data preload (small reference tables)
ClearCollect(colCategories, lst_Categories);
ClearCollect(colStatuses, lst_Statuses);
ClearCollect(colParameters, lst_Parameters);

// 4. App settings
Set(gblAppVersion, "1.0");
// Keep any client-side row budget in ONE place and set it from the app's configured
// data row limit — do not hardcode a platform figure here. Owner: data/query-and-delegation.md
```

The security-specific `App.OnStart` block (role, business unit, access-denied fallback) is in
`security-craft.md`.

### 4.3 — Screen.OnVisible — standard screen init

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

## 5 — Control property reference

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
