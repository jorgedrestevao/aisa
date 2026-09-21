# security-patterns — Security Model Reference

**Source:** v33/v34 `ref-06-security.md` (direct port).
**Consumers:** `security-cell` (RBAC matrix + audit trail design), `design-spec-cell` (Power FX security blocks for Claude Design).
**Token tier:** WARM (loaded only by cells that declare it in `pack.yaml § domain_knowledge_load`).

---

## SECTION A — ROLE INFERENCE

### Signal sources (priority order)
1. Process-cell answers: "Quem opera?" and "Quem consome?"
2. Approval workflow actors (who triggers each transition)
3. Data map: who validates results (decision points)
4. Sensitive columns: imply restricted-access roles (Finance = financial columns)
5. Column names: "Aprovado por", "Responsável", "Gestor", "Validado por"
6. Sheet names: "Dashboard_Gestão", "Input_Comercial", "Relatório_Direcção"

### Scope classification signals
| Scope | Signals |
|---|---|
| Own records | "operador", "comercial", "técnico", "agente" — creates and manages own data |
| Department/BU | "supervisor", "chefe de equipa", "team lead", "responsável de equipa" |
| Organisation | "director", "manager", "controller", "admin", "compliance" |

### Approval authority signals
| Authority | Signals |
|---|---|
| None | No mention of approving, validating, or authorising |
| Limited | Approves specific types (e.g., only quotes under €10k) |
| Full | Final approver, director, system administrator |

### Always add (if not detected)
- **Admin role**: full access to everything — every solution needs one
- **Service Account** (if flows/integrations access data): read/write on specific entities, no UI access

### Inheritance detection — suggest when
- Role A approves work done by Role B → Role A sees everything Role B sees
- Role A described as "senior" or "superior" to Role B
- Role A has all Role B permissions + additional ones

---

## SECTION B — PERMISSION MATRICES

### Symbols
| Symbol | Meaning |
|---|---|
| OK | Full access (all CRUD within scope) |
| EDIT-OWN | Read all + edit only own records |
| READ | Read only (all records in scope) |
| CREATE | Create only (no edit/delete existing) |
| NONE | No access (screen hidden or entity blocked) |

### Matrix 1 — Role × Screen rules
- Admin: OK on ALL screens — no exceptions
- Screen with NONE for a role: that screen's Visible property must be false for that role
- Screens with READ: all write controls (Patch buttons, form fields) set to DisplayMode.Disabled
- Screens with EDIT-OWN: Gallery.Items filtered to own records; edit buttons conditionally visible

### Matrix 2 — Role × Entity × CRUD rules
| Symbol | C | R | U | D |
|---|---|---|---|---|
| Full (all) | Yes | Yes | Yes | Yes |
| Read + Edit own | No | Yes | own only | No |
| Read only | No | Yes | No | No |
| Create only | Yes | Yes (own) | No | No |
| None | No | No | No | No |

Scope qualifier always stated: (own), (dept), (all)
Example: "R(all) U(own)" = can read all records, update only own

### Matrix 3 — Sensitive Fields rules
Flag from schema.sensitive_columns. For each:
- Financial columns: visible only to Finance, Manager, Admin
- Personal data columns: visible only to HR, Admin, and the record owner
- Approval fields (approved_by, approved_at): read-only for all except Admin

### Matrix 4 — Approval Permissions rules
From screens.approval_workflows transitions. For each action:
- Submit: Requester role(s)
- Approve: Approver role(s) — never same as Requester for the same record
- Reject: Approver role(s)
- Cancel: Admin only (post-approval cancellations)
- Export: Finance, Manager, Admin (data export is always a privileged action)

---

## SECTION C — CONFLICT RESOLUTION

### Conflict types and resolutions

**Type 1 — Multi-role conflict**
User has Role A (grants Edit) and Role B (grants Read-only) on same resource.
Resolution: Read-only wins (least privilege).
Dataverse note: Dataverse stacks roles with OR logic (most permissive wins natively).
To enforce least privilege in Dataverse: use Power Fx guards in the app, not role stacking.

**Type 2 — Inheritance violation**
Child role has MORE permissions than parent on any resource.
Resolution: Remove excess from child role.
Rule: Parent permissions ≥ child permissions on EVERY resource, EVERY intersection.

**Type 3 — Scope escalation**
Role has Create permission with "own" scope.
Resolution: Create is always organisation scope (you cannot create a record you don't own at creation time). Flag if contradicts design intent.

**Type 4 — Approval without Read**
Role can approve entity X but has no Read access to entity X.
Resolution: Add Read (organisation scope) to that role for that entity.

**Type 5 — Orphan approval action**
State transition has no role assigned to execute it.
Resolution: Assign to Admin role. Flag for business owner confirmation.

### Conflict log format
```
CONFLICT #[N]
Type: [type name]
Resource: [screen/entity/field/action name]
Roles involved: [Role A], [Role B]
Role A grants: [permission]
Role B grants: [permission]
Resolution: [most restrictive applied]
Principle: Least privilege
Impact on users: Users with both roles receive [resolved permission]
Implementation note: [how to enforce — PFx guard / role design / matrix cell]
```

---

## SECTION D — POWER FX SECURITY PATTERNS

### Complete App.OnStart security block
```powerfx
// ── Security Initialisation ────────────────────────────────
Set(varCurrentUserEmail, Lower(User.Email));

Set(varCurrentUserRole,
 LookUp([prefix]_userroles,
 Lower([prefix]_email) = varCurrentUserEmail,
 [prefix]_rolename
 )
);

If(IsBlank(varCurrentUserRole),
 Notify("Sem perfil de acesso. Contacta o administrador.", NotificationType.Error, 5000);
 Navigate(AccessDeniedScreen, ScreenTransition.None)
);

Set(varCurrentUserBU,
 LookUp([prefix]_userroles,
 Lower([prefix]_email) = varCurrentUserEmail,
 [prefix]_businessunit
 )
);
// ─────────────────────────────────────────────────────────────
```

### Screen access patterns

**Simple role check (single role):**
```powerfx
// Screen.Visible
varCurrentUserRole = "Admin"

// Screen.OnVisible (defense in depth)
If(varCurrentUserRole <> "Admin", Navigate(HomeScreen, ScreenTransition.None))
```

**Multiple roles:**
```powerfx
// Screen.Visible
varCurrentUserRole = "Manager" || varCurrentUserRole = "Admin"

// Screen.OnVisible
If(!(varCurrentUserRole = "Manager" || varCurrentUserRole = "Admin"),
 Navigate(HomeScreen, ScreenTransition.None))
```

**Exclusion pattern (everyone except one role):**
```powerfx
// Screen.Visible (hide from Comercial)
varCurrentUserRole <> "Comercial"
```

### Gallery row-level filter patterns

**Owner-only scope:**
```powerfx
Switch(varCurrentUserRole,
 "Comercial", Filter(cr_entity, Lower(cr_ownerid) = varCurrentUserEmail),
 "Manager", cr_entity,
 "Finance", cr_entity,
 "Admin", cr_entity,
 Filter(cr_entity, false)
)
```

**Department scope:**
```powerfx
Switch(varCurrentUserRole,
 "Comercial", Filter(cr_entity, Lower(cr_ownerid) = varCurrentUserEmail),
 "Manager", Filter(cr_entity, cr_businessunit = varCurrentUserBU),
 "Finance", cr_entity,
 "Admin", cr_entity,
 Filter(cr_entity, false)
)
```

### Button access patterns

**DisplayMode:**
```powerfx
// Edit vs Disabled based on role
If(varCurrentUserRole = "Manager" || varCurrentUserRole = "Admin",
 DisplayMode.Edit, DisplayMode.Disabled)

// Edit vs Disabled based on role AND ownership
If(
 (varCurrentUserRole = "Comercial" && Lower(ThisItem.cr_ownerid) = varCurrentUserEmail) ||
 varCurrentUserRole = "Manager" ||
 varCurrentUserRole = "Admin",
 DisplayMode.Edit, DisplayMode.Disabled
)
```

**Visible (completely hide):**
```powerfx
// Hide Delete button from non-Admin
varCurrentUserRole = "Admin"
```

### Field visibility patterns

**Show value or mask:**
```powerfx
// lblFinancialValue.Text — show actual value to Finance/Admin, mask to others
If(
 varCurrentUserRole = "Finance" || varCurrentUserRole = "Admin",
 Text(ThisItem.cr_totalvalue, "[$-pt-PT]#,##0.00 €"),
 "———"
)
```

**DisplayMode for sensitive fields:**
```powerfx
// Sensitive field — edit only for Admin
If(varCurrentUserRole = "Admin", DisplayMode.Edit, DisplayMode.Disabled)
```

### Audit patterns — mandatory for Approve, Delete, Export

**Approve:**
```powerfx
If(varCurrentUserRole = "Manager" || varCurrentUserRole = "Admin",
 Patch(cr_auditlog, Defaults(cr_auditlog), {
 cr_action: "Approve",
 cr_entity_name: "cr_quote",
 cr_record_id: Text(ThisItem.cr_quoteid),
 cr_record_name: ThisItem.cr_name,
 cr_performed_by: varCurrentUserEmail,
 cr_performed_at: Now,
 cr_notes: txtApprovalNotes.Text
 });
 Patch(cr_quote, ThisItem, {
 cr_status: "Approved",
 cr_approved_by: varCurrentUserEmail,
 cr_approved_at: Now
 });
 Notify("Aprovado com sucesso.", NotificationType.Success),
 Notify("Sem permissão para aprovar.", NotificationType.Error)
)
```

**Delete:**
```powerfx
If(varCurrentUserRole = "Admin",
 Patch(cr_auditlog, Defaults(cr_auditlog), {
 cr_action: "Delete",
 cr_entity_name: "cr_quote",
 cr_record_id: Text(ThisItem.cr_quoteid),
 cr_performed_by: varCurrentUserEmail,
 cr_performed_at: Now
 });
 Remove(cr_quote, ThisItem);
 Notify("Registo eliminado.", NotificationType.Warning),
 Notify("Só o administrador pode eliminar registos.", NotificationType.Error)
)
```

**Export:**
```powerfx
If(
 varCurrentUserRole = "Finance" || varCurrentUserRole = "Manager" || varCurrentUserRole = "Admin",
 Patch(cr_auditlog, Defaults(cr_auditlog), {
 cr_action: "Export",
 cr_entity_name: "ALL",
 cr_record_id: "BULK",
 cr_performed_by: varCurrentUserEmail,
 cr_performed_at: Now
 });
 Launch("[export-url-or-flow-trigger]"),
 Notify("Sem permissão para exportar.", NotificationType.Error)
)
```

---

## SECTION E — TECHNICAL ARTEFACTS

### Dataverse Security Role definition format
```
SECURITY ROLE: [RoleName]
Description: [business purpose in plain language]
Member privilege inheritance: Direct User (Non-Inherited)

TABLE PRIVILEGES:
 Table: [schema_name] ([Display Name])
 Create: [None | User | Business Unit | Parent: Child BUs | Organization]
 Read: [same options]
 Write: [same options]
 Delete: [same options]
 Append: [same options]
 Append To: [same options]
```

### Dataverse Column Security Profile format
```
PROFILE: [RoleName]_ColumnSecurity
Assign to roles: [list]

COLUMNS:
 [schema_column]:
 Allow Read: [Yes/No]
 Allow Create: [Yes/No]
 Allow Update: [Yes/No]
```

### SharePoint groups format
```
PERMISSION GROUP: [SolutionName]_[RoleName]
Permission Level: [Full Control | Contribute | Read | Custom]
Members: [list test users here]

ITEM-LEVEL (if applicable):
 Read: [All items | Only their own]
 Edit: [All items | Only their own]
```

### Azure SQL RLS — role-specific column views

When the architecture uses Azure SQL, Row-Level Security (see [`azure-sql-reference.md`](azure-sql-reference.md) § Row-Level Security) gives row filtering, but **column hiding** is best implemented with role-specific views. Pattern:

```sql
-- Comercial view: omit financial columns, restrict to own records
CREATE OR ALTER VIEW [dbo].[vw_app_quote_comercial] AS
SELECT [cr_quoteid], [cr_name], [cr_status], [cr_ownerid], [cr_createdon]
-- cr_totalvalue, cr_margin intentionally excluded
FROM [dbo].[slv_quote]
WHERE [cr_ownerid] = CAST(SESSION_CONTEXT(N'user_email') AS NVARCHAR(255));

-- Full view for Manager / Finance / Admin
CREATE OR ALTER VIEW [dbo].[vw_app_quote_full] AS
SELECT * FROM [dbo].[slv_quote];
```

The Canvas App selects which view to bind per role at `App.OnStart`:

```powerfx
Set(varQuoteSource,
 Switch(varCurrentUserRole,
  "Comercial", vw_app_quote_comercial,
  "Manager", vw_app_quote_full,
  "Finance", vw_app_quote_full,
  "Admin",   vw_app_quote_full,
  Blank
 )
)
```

This is enforced server-side (the view definition simply doesn't expose the columns) — defence-in-depth over Power Fx `If()` masks alone.

### Audit Trail mandatory columns

Every audited entity MUST have:
- `cr_audited_by` (Lookup → users) — who performed last write
- `cr_audited_at` (Date Time) — when last write happened
- `cr_audited_action` (Choice: Create / Update / Approve / Reject / Delete / Export)
- `cr_audited_notes` (Multiple Lines of Text) — context

Retention default: 5 years. Override per regulatory context (Galp internal: 7y for financial).
