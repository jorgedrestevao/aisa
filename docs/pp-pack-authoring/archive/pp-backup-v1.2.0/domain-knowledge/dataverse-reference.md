# dataverse-reference — Dataverse Complete Reference

**Source:** transplanted 2026-05-28 from the previous-aisa references (`ref-02-dataverse.md` + schema-rigor rules from `dt-06-schema-rigor.md`).
**Consulted by:** `lens-technology`, `solution-architect`, `implementation-spec` and `claude-design-brief` deliverable templates.
**Phase eligibility:** Options + Decision only.

This is the authoritative Dataverse reference for the pp pack. Cross-reference with [`decision-tree.md`](../decision-tree.md) when the chosen branch is `dataverse-first` or `hybrid`, and with [`security-patterns.md`](security-patterns.md) for column-level security and role design.

---

## DATA TYPES — Use Exactly These Names

| Category | Type Name | Use When | Notes |
|---|---|---|---|
| Text | Single Line of Text | Names, codes, short text | Max 4000 chars |
| Text | Multiple Lines of Text | Notes, descriptions | Plain or Rich text |
| Text | Email | Email addresses | Validated format |
| Text | URL | Web links | Validated format |
| Text | Phone | Phone numbers | No validation |
| Number | Whole Number | Counts, integers | No decimal |
| Number | Decimal Number | Precise decimals | Financial calcs |
| Number | Floating Point Number | Scientific/approximate | Never for money |
| Number | Currency | Monetary values | ALWAYS for money |
| Date | Date Only | Dates without time | YYYY-MM-DD |
| Date | Date and Time | Full timestamp | UTC recommended |
| Choice | Choice | Fixed options (local) | Only this table |
| Choice | Global Choice | Shared options | Reused across tables |
| Boolean | Yes/No | Binary flags | Renders as toggle |
| Lookup | Lookup | FK to another table | Creates relationship |
| File | File | Attachments | Max 128MB |
| Image | Image | Image fields | Square crop |
| Auto Number | Auto Number | Sequential IDs | System-generated |
| Unique Identifier | Unique Identifier | GUIDs, ext IDs | Always for PKs |

---

## RESERVED COLUMN NAMES — Never Use for Custom Columns

```
createdby, createdon, createdonbehalfby, importsequencenumber,
modifiedby, modifiedon, modifiedonbehalfby, organizationid,
overriddencreatedon, ownerid, owningbusinessunit, owningteam,
owninguser, statecode, statuscode, timezoneruleversionnumber,
utcconversiontimezonecode, versionnumber, entityimage,
entityimage_timestamp, entityimage_url, entityimageid
```

A name collision against this list causes silent data corruption at runtime — never override.

---

## COLUMN FLAGS — Rules for Setting

**Required (Yes/No):**
- Yes: columns that identify the record (name/code), columns needed for all calculations
- No: optional/supplementary fields, system-populated fields

**Searchable (Yes/No):**
- Yes: name, code, status, any field users will filter/search on
- No: calculated results, audit timestamps, internal flags, large text fields

**Auditable (Yes/No):**
- Yes: financial values, status fields, approval fields, quantities, any field that changes over time for compliance
- No: display-only fields, system-managed fields, reference data that never changes

---

## RELATIONSHIP TYPES

| Type | Definition | Power Apps Impact |
|---|---|---|
| Many-to-One (N:1) | Child has lookup to parent | Lookup column on child table |
| One-to-Many (1:N) | Parent has sub-grid of children | Sub-grid on parent form |
| Many-to-Many (N:N) | Both sides via junction | Two N:1 relationships on junction table |

**Relationship naming convention:**
- Lookup column: `[prefix]_[relatedtable]id` (e.g., `cr_quoteid` on QuoteLine)
- Relationship name: `[prefix]_[parenttable]_[childtable]` (e.g., `cr_quote_quoteline`)

---

## CALCULATED COLUMN — FORMULA COMPLEXITY TIERS

| Excel Equivalent | Dataverse Mechanism | Notes |
|---|---|---|
| A + B, A × B | Calculated column (Power Fx syntax) | Real-time |
| SUM across related records | Rollup column | Recalculates on schedule |
| IF, SWITCH simple | Calculated column or Business Rule | Real-time |
| VLOOKUP | Lookup column + related field | Native relationship |
| SUMPRODUCT, nested cross-entity | Power Automate flow | Triggered |
| NPV, IRR, PMT | Power Automate flow | Never in calculated columns |

**Calculated column Power Fx syntax examples:**
```
// Simple arithmetic
cr_linetotal = cr_unitprice * cr_quantity

// Conditional
cr_status_label = If(cr_status == 0, "Draft", If(cr_status == 1, "Approved", "Rejected"))

// Date arithmetic
cr_days_open = DateDiff(cr_createdon, Now, Days)
```

**Rollup column definition:**
- Aggregate: Sum / Count / Min / Max / Avg
- Related entity: [entity name]
- Filter: [optional condition]
- Field: [which field to aggregate]

---

## BUSINESS RULES — Structure

```
NAME: [RuleName] — descriptive, no spaces
SCOPE: Entity (server-side, always) | Form (client-side only)
TRIGGER: Always | On field change ([FieldName]) | On save

CONDITION: [field] [operator] [value]
 Operators: equals, does not equal, contains, does not contain,
 begins with, ends with, greater than, less than,
 is null, is not null

ACTION (one or more):
 - Show error message on [field]: "[message text]"
 - Show message: "[information text]"
 - Set field [field] = [value]
 - Set field [field] as Required / Not Required
 - Show field [field] / Hide field [field]
 - Lock field [field] / Unlock field [field]
```

**Business Rule limitations:**
- Cannot check user roles directly (use Power Fx or security roles instead)
- Cannot reference data from other tables (use calculated columns or Power Automate)
- Scope = Form means it only runs in the app, not via API or import

---

## DATAVERSE VIEWS — Minimum Per Table

| View Name | Filter | Sort | Purpose |
|---|---|---|---|
| Active [Entity] | statuscode = Active | modifiedon DESC | Default operational view |
| All [Entity] | None | createdon DESC | Full history |
| [Business filter] | [relevant condition] | [relevant sort] | Specific operational need |

**View design rules:**
- Never exceed 15 columns in a view (performance)
- Always include the primary column and at least one status/date column
- Filter columns must be searchable for performance

---

## SECURITY ROLES — Structure for Manual Configuration

```
SECURITY ROLE NAME: [RoleName]
Description: [business purpose]
Member privilege inheritance: Direct User (Non-Inherited)

TABLE PRIVILEGES:
 Table: [schema_name]
 Create: [None | User | Business Unit | Parent: Child Business Units | Organization]
 Read: [same options]
 Write: [same options]
 Delete: [same options]
 Append: [same options — ability to add child records]
 Append To: [same options — ability to be parent of child records]

SCOPE MAPPING:
 User = own records (ownerid = current user)
 Business Unit = own department
 Parent: Child Business Units = own BU + all child BUs
 Organization = all records
```

---

## COLUMN SECURITY PROFILES

```
PROFILE NAME: [RoleName]_ColumnSecurity
ASSIGN TO ROLES: [list of security roles]

RESTRICTED COLUMNS:
 [schema_column_name]:
 Allow Read: Yes / No
 Allow Create: Yes / No
 Allow Update: Yes / No
```

---

## ALTERNATE KEYS — For Uniqueness Constraints

Preferred over Business Rules for uniqueness — enforced at database level.
```
Table: [table_name]
Key Name: [prefix]_[table]_[columns]_key
Columns: [column1], [column2] (for composite uniqueness)
```

---

## PERFORMANCE LIMITS

| Limit | Value | Impact |
|---|---|---|
| Max columns per table | 400 | Schema design |
| Max records per query (delegation) | 500 (default) / 2000 (max setting) | Power Fx filter/aggregate |
| Max file attachment size | 128 MB | File columns |
| Max concurrent users (standard) | 500 | Architecture |
| Rollup column recalculation | Every 12 hours (default) | Near-real-time needs |
| Calculated column performance | Real-time | Complex calculations |

---

## PLUGIN / LOW-CODE PLUGIN — When to Use

Use when:
- Calculation must run server-side regardless of client
- Complex multi-step logic exceeding Power Automate capabilities
- High-frequency triggers where PA flow overhead is too high
- Pre/post operation hooks needed (validate before save, cascade on delete)

Low-code plugins (preview): Power Fx syntax, no C# needed, runs server-side.
Classic plugins: C# / .NET, full Dataverse SDK access.

---

## BUSINESS RULE vs POWER FX vs PLUGIN vs POWER AUTOMATE — Decision Matrix

| Need | Business Rule | Calculated Column / Power Fx | Power Automate | Plugin (low-code or C#) |
|---|---|---|---|---|
| Show/hide field based on value | BEST | Alternative (Visible property) | Overkill | Overkill |
| Set field required conditionally | BEST | Cannot change Required at runtime | Cannot | Overkill |
| Lock/unlock field based on status | BEST | Alternative (DisplayMode) | Cannot | Overkill |
| Show validation error message | BEST | Alternative (Notify) | Not UI | Not UI |
| Simple arithmetic (A × B) | Cannot calculate | BEST (Calculated column) | Overkill | Overkill |
| SUM across child records | Cannot | Not delegable | Flow triggered | BEST (pre/post) |
| Rollup (count/sum/avg related) | Cannot | Cannot | Use native Rollup | Rollup column BEST |
| Cross-table lookup logic | Single table only | LookUp in Canvas App | Good | BEST (server-side) |
| Cascade update to children | Cannot | Not efficient | Good (Apply to Each) | BEST (bulk) |
| Complex multi-step calculation | Cannot | Not suited | Good | BEST |
| Must run even via API/import | Scope=Entity | Canvas only | Trigger on create/modify | Always runs |
| Must run BEFORE save | Cannot block save | Cannot block | Async only | BEST (Pre-operation) |
| Must block save on condition | Shows error only | Cannot block Patch | Cannot | BEST (Pre-validation) |

**Decision shortcut:**
- UI-only logic (show/hide/lock/require) → Business Rule
- Display calculation (A×B, date diff) → Calculated Column
- Aggregation across records → Rollup Column (if simple) or Plugin (if complex)
- Cross-entity logic or side effects → Power Automate (async) or Plugin (sync)
- Must enforce regardless of client → Plugin (pre-operation)

---

## ROLLUP COLUMNS — Limitations and Caveats

| Limitation | Detail | Workaround |
|---|---|---|
| Recalculation frequency | Every 12 hours by default | Manual recalc via `RecalculateRollup` API call in PA flow |
| Max rollup columns per entity | 100 | Rarely a problem, but track count |
| Source must be a related entity | Cannot aggregate from unrelated tables | Create relationship first, or use PA flow |
| Cannot use calculated columns as source | Rollup ignores calculated column values | Use plain stored columns as source |
| Filter limited to simple conditions | No complex expressions in rollup filter | Pre-filter via PA flow writing to a flag column, then rollup on flag |
| Real-time display in Canvas App | Value may be stale (up to 12h old) | Show "Atualizado às [timestamp]" label. Force recalc on screen load via PA flow |

**Force recalculation pattern (Power Automate):**
```
TRIGGER: When record status changes to "Approved"
ACTION: HTTP request to Dataverse API
 Method: POST
 URL: [org]/api/data/v9.2/CalculateRollupField(Target=@t,FieldName='cr_totalvalue')
 @t: {"@odata.id":"cr_quotes([record_id])"}
```

---

## ALTERNATE KEYS — Upsert and Dedup Patterns

Alternate keys enforce uniqueness at database level (not just app level).

**When to use:**
- External system IDs (ERP code, API ID) — prevent duplicate imports
- Natural keys (product code + region) — enforce business uniqueness
- Integration scenarios where Patch must create-or-update without checking first

**Upsert with alternate key (Power Fx):**
```powerfx
// If record with this external_code exists → update. If not → create.
Patch(cr_products,
 LookUp(cr_products, cr_external_code = txtCode.Text),
 {
 cr_external_code: txtCode.Text,
 cr_name: txtName.Text,
 cr_price: Value(txtPrice.Text)
 }
)
// Note: LookUp returns blank for new records → Patch creates
```

**Upsert with alternate key (Power Automate / Dataverse connector):**
```
Update a row action:
 Table: cr_products
 Row ID: cr_external_code='ERP-001' ← uses alternate key syntax
 Fields: { name, price,... }
 "Upsert" behavior: creates if not found
```

**Composite key (multi-column uniqueness):**
```
Table: cr_quotelines
Key: cr_quoteid + cr_productid ← same product cannot appear twice in same quote
```

---

## SOLUTION ARCHITECTURE — Layering Basics

The `claude-design-brief` and `implementation-spec` deliverables draw on these layering basics when describing the deployment plan.

| Concept | Definition | Impact |
|---|---|---|
| Unmanaged solution | Editable, used in Development env | All customizations go here first |
| Managed solution | Read-only, used in Test/Prod | Exported from Dev, imported to target |
| Publisher prefix | `cr_` (or client-specific) | Set ONCE at project start. Cannot change later |
| Solution layering | Multiple solutions can overlay | Last imported wins for conflicts |

**Standard deployment flow:**
```
Dev environment → Export as Managed → Import to Test → Validate → Import to Prod
```

**Minimum solutions per project:**
1. `[SolutionCode]_Core` — tables, columns, relationships, security roles
2. `[SolutionCode]_Apps` — Canvas Apps, Model-Driven Apps
3. `[SolutionCode]_Flows` — Power Automate flows
4. `[SolutionCode]_Data` — reference data (if using Dataverse Configuration Migration Utility)

**Why separate:** Apps and flows change more frequently than schema. Separate solutions allow independent deployment without risking schema changes.

---

## LICENSING IMPACT ON ARCHITECTURE

| Feature | M365 Standard (included) | Power Apps Per User (~€20/user/month) | Power Apps Per App (~€5/app/user/month) |
|---|---|---|---|
| Canvas Apps | OK (custom connectors limited) | OK (Full) | OK (per app) |
| Model-Driven Apps | NO | OK | OK (per app) |
| Dataverse storage | NO (SharePoint only) | OK (1GB + 250MB/user) | OK (50MB/app) |
| Custom connectors | NO | OK | OK |
| Premium connectors | NO | OK | OK |
| AI Builder credits | NO | OK (included) | NO |
| Dataverse for Teams | OK (within Teams only) | N/A | N/A |

**Architectural impact:**
- If client has M365 Standard only → recommend SharePoint backend (no Dataverse).
- If client has Per User license → Dataverse is the default recommendation.
- If client needs Model-Driven Apps → Per User or Per App required.
- If < 10 users → Per App may be cheaper than Per User.

**Always flag:** "Confirmar licenciamento atual com IT antes de comprometer arquitetura." Indicative prices — confirm with Microsoft CSP.

---

## ANTI-PATTERNS — Never Do These

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Using FLOAT for currency | Rounding errors accumulate | Always use Currency type |
| Creating Choice with >150 options | UI unusable, performance degrades | Use Lookup to reference table instead |
| Rollup column for real-time totals | Up to 12h stale | Use PA flow or Canvas App collection Sum |
| Business Rule with Scope=Form for critical validation | Bypassed by API imports, Power Automate, bulk operations | Use Plugin (pre-validation) or enforce at data layer |
| Storing files in Multiple Lines of Text (base64) | 1MB limit, no preview, wastes storage | Use File or Image column type |
| Creating 1 security role per user | Unmanageable at scale, N roles × M tables = explosion | Create role per business profile (max 5-7 roles) |
| Publishing unmanaged solution to Prod | Cannot be cleanly removed, causes layering issues | Always export as Managed for Test/Prod |

---

## SCHEMA-RIGOR VALIDATION MATRIX (per-platform appendix)

These rules apply when the solution-architect or `implementation-spec` deliverable defines schema. They are mechanical checks that prevent inconsistencies between the chosen architectural branch and the schema decisions. Map any failure to the appropriate SU state (Confirmed if directly observed, Risky if it's a downstream-impact problem the architect is taking on).

### 1. Naming convention consistency

Pick ONE convention for the engagement and apply to every column:

- `PascalCase` → matches `/^[A-Z][a-zA-Z0-9]*$/`
- `snake_case` → matches `/^[a-z][a-z0-9_]*$/`
- `publisher_prefix` → matches `/^{prefix}_[a-z][a-z0-9_]*$/` (Dataverse default)

Mixing conventions across entities is a Conflicted SU row that must be resolved before render.

### 2. Reserved-word check (per platform)

| Platform | Source list |
|---|---|
| Dataverse | This file § Reserved Column Names |
| Azure SQL | [`azure-sql-reference.md`](azure-sql-reference.md) (reserved-word section) |
| SharePoint | [`sharepoint-reference.md`](sharepoint-reference.md) (forbidden names section) |

A match is non-negotiable — it causes silent data corruption at runtime. The architect MUST propose an alternative.

### 3. Type coherence

For every column, verify the proposed type is supported on the chosen platform:

- **Dataverse**: `Text, MultilineText, Lookup, OptionSet, Choice, Decimal, Money, Integer, DateTime, Boolean, File, Image, Customer, Owner`. Money precision is 4 decimals max. Decimal precision 1–23 digits, scale 0–10. Lookup target entity must exist in the schema (or be a system entity).
- **Azure SQL**: `NVARCHAR, INT, BIGINT, DECIMAL(p,s), DATETIME2, BIT, UNIQUEIDENTIFIER, VARBINARY`. `DECIMAL(p,s)`: `1 ≤ s ≤ p, p ≤ 38`. FK references must resolve to an existing entity PK column.
- **SharePoint**: `Single line of text, Multiple lines, Choice, Number, Currency, Date and Time, Lookup, Yes/No, Person or Group, Hyperlink, Calculated, Image`. Single line ≤ 255 chars. Currency 2 decimals max. Multi-line rich text 63KB per row. Lookup target must be a list in the same site collection.

Incompatible type → propose a substitute and record the substitution as an Assumed SU row (with `base da assumption`).

### 4. Foreign-key consistency

For every relationship:

- Both `from_entity` and `to_entity` exist in the schema.
- FK column name follows the chosen naming convention.
- FK column type matches the target PK type exactly (no implicit conversion).
- `ON DELETE` behaviour is explicit — `CASCADE | RESTRICT | SET NULL`. Never default.
- No circular references in the dependency graph.

### 5. Sensitive-column enumeration

The allowed values for sensitivity-type classification are:

```
person_name, email, phone, tax_id, address, financial,
company_name, iban, free_text_pii_risk, dob, health_data
```

Adding a new type requires updating both [`anonymization.md`](anonymization.md) and this enumeration. Every column matching one of these patterns must have either an anonymization method (from `anonymization.md`) or an explicit `no_anonymization_required` flag with justification.
