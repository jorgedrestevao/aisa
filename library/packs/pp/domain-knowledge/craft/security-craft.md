# Security Craft — Role Inference, Permission Matrices and Enforcement Patterns

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

**Which controls exist, and where each one actually takes effect, is not decided here.** Control
availability, enforcement semantics and the interaction between store-level and app-level security belong to
`security/security-controls.md` (with `governance/governance-and-environments.md` for tenant and
environment-level policy). This file carries how a role model is *derived from the engagement*, how it is
*written down*, and the *build patterns* that implement it.

**A name or a job title is a hypothesis about a role — never an authorization.** A person named in a
spreadsheet, a mail thread or an org chart is evidence that somebody once did something; it is not evidence
that the target must let a role do it. Every cell of every matrix here is derived from a **requirement**, as
*action × resource × scope × role*: the action the requirement asks for, the resource it touches, the scope
it covers, and the role that owes it. A role with no action derived from a requirement gets no grant, and
`OK` on a resource is a grant like any other. Where the requirement is absent, the honest output is an open
requirement of the to-be — never a default that fills the gap.

**Authorization is enforced in the data or API layer.** Hiding a screen, disabling a control or masking a
label shapes what a user is *offered*; it does not stop a request. A permission that exists only in the app
layer is not satisfied, however complete the matrix looks: state the data/API-side control that enforces it
(Section E and `security/security-controls.md`), and treat the app-layer pattern as the second line, never
the only one.

---

## Section A — Role inference

### Signal sources (priority order)
1. Process answers: "Quem opera?" and "Quem consome?"
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
| Limited | Approves only certain types, or only below a stated value threshold |
| Full | Final approver, director, system administrator |

### Roles a requirement may still owe

Two roles are proposed only where a requirement asks for them, and each proposal carries the requirement
that activates it:

- **Platform administration role** — where the requirement names environment, solution or role
  administration. Its grants are those administration actions, derived cell by cell like everything else.
  There is no role with full access to everything by default.
- **Service identity** — where automation or an integration reaches the data with no human at the keyboard.
  Read/write on the entities that automation actually touches, no UI access. This is an **execution
  identity** and is preserved as one: it is what runs the flow and what the licence attaches to
  (`integration/integration-mechanisms.md`).

### Role containment — a way of writing the matrix, never a grant

Where the actions required of role A already contain those required of role B, the matrix may express the
containment instead of repeating cells. That is notation, not a reason to widen A. Being described as
senior or superior, or being the role that approves B's work, grants nothing: hierarchy is org structure and
the matrix comes from actions. Confirm containment against the requirements before writing it; never derive
it from a title.

---

## Section B — Permission matrices

Four matrices. Each is produced where the target has the thing it describes; the implementation spec
carries in full those produced and records `not applicable — <reason>` for the rest. Matrix 4 is engaged
**only** where an approval workflow is behaviour of the process in scope: a process with no approvals gets
no approval matrix, and none is invented to have one (`decision-tree.md` §6.1).

### Symbols
| Symbol | Meaning |
|---|---|
| OK | Full access (all CRUD within scope) |
| EDIT-OWN | Read all + edit only own records |
| READ | Read only (all records in scope) |
| CREATE | Create only (no edit/delete existing) |
| NONE | No access (screen hidden or entity blocked) |

### Matrix 1 — Role × Screen
- Every cell comes from the requirement that asks for the action; no role starts with `OK` everywhere
- Screen with NONE for a role: that screen's Visible property must be false for that role — and the
  entity-side grant must be absent too, or the screen is hidden while the data stays reachable
- Screens with READ: all write controls (Patch buttons, form fields) set to DisplayMode.Disabled
- Screens with EDIT-OWN: Gallery.Items filtered to own records; edit buttons conditionally visible

### Matrix 2 — Role × Entity × CRUD
| Symbol | C | R | U | D |
|---|---|---|---|---|
| Full (all) | Yes | Yes | Yes | Yes |
| Read + Edit own | No | Yes | own only | No |
| Read only | No | Yes | No | No |
| Create only | Yes | Yes (own) | No | No |
| None | No | No | No | No |

The scope qualifier is always stated: (own), (dept), (all).
Example: "R(all) U(own)" = can read all records, update only own.

### Matrix 3 — Sensitive fields
Flag from the engagement's sensitive-column inventory. For each:
- Financial columns: visible only to Finance, Manager, Admin
- Personal data columns: visible only to HR, Admin, and the record owner
- Approval fields (`approved_by`, `approved_at`): written by the transition, not by hand — no role gets
  update on them unless a requirement names a correction path, and then that path is itself an audited action

Sensitivity typing and test-data handling: [`anonymization.md`](anonymization.md).

### Matrix 4 — Approval permissions
From the approval workflow transitions, one row per transition the process actually has:
- Submit: the role(s) the requirement authorises
- Approve / Reject: the role(s) the requirement authorises. Whether the approver may be the same role as the
  requester is a **question for the obligation in scope** — cite the regulation, contract or policy that
  splits them, and record the split as a permission model the target must enforce. Uncited, no split is
  imposed: a generic separation of duties invents a control nobody asked for
  (`agent-memory/_universal/compliance-officer/universal-constraints.md`)
- Cancel, and any other post-transition correction: the role the requirement names, with the audited action
  it produces. No role holds it by default
- Export: the role(s) a requirement authorises, and the classification of what leaves. Export is privileged
  where the data classification makes it so — that is a fact about the data, read from the sensitive-column
  inventory, not a standing rule of this file

---

## Section C — Conflict resolution

### Conflict types and resolutions

**Type 1 — Multi-role conflict**
A user holds Role A (grants Edit) and Role B (grants Read-only) on the same resource.
Resolution: read-only wins (least privilege) as the *designed* outcome.
Caution: a store's own role-combination semantics may not be least-privilege — confirm the combination
behaviour with `security/security-controls.md` before assuming role design alone delivers the restriction,
and add an explicit app-side guard where it does not.

**Type 2 — Containment mismatch**
The matrix was written as containment (role A contains role B) and a cell contradicts it: B has an action A
does not.
Resolution: the requirements decide which cell is right, and the notation follows them — either A gains the
action because a requirement asks it of A, or the containment was the wrong way to write these two roles and
they are written out separately.
Not a rule about hierarchy: a role is not widened to preserve a diagram.

**Type 3 — Scope escalation**
A role has Create permission with "own" scope.
Resolution: create is always organisation scope (you cannot create a record you do not yet own). Flag it if
this contradicts design intent.

**Type 4 — Approval without Read**
A role can approve entity X but has no Read access to entity X.
Resolution: grant Read over exactly the records the approval decision needs — the ones routed to that role,
at the scope the routing implies. Never organisation scope to fix a workflow gap: widening Read across the
whole entity is a new grant, and it needs its own requirement.

**Type 5 — Transition with no authorised role**
A state transition has no role authorised to execute it.
Resolution: it is an **open requirement of the to-be**, written as such — which role the process means to
authorise here, and what it may see to decide. Not assigned to administration: an administration role that
absorbs every unassigned transition ends up holding the whole workflow, which is the opposite of what the
matrix is for. The transition stays unexecutable until the requirement says who executes it, and that is the
honest state.

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
Implementation note: [how to enforce — Power Fx guard / role design / store-side control / matrix cell]
```

---

## Section D — Power Fx security patterns

These are app-layer patterns. They shape what a user is offered; they are not by themselves a substitute for
store-side controls (see Section E and the control owner).

### App.OnStart security block
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

// Screen.OnVisible (defence in depth)
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

Every filter above is also a query — run it through the delegation check in `powerfx.md` §1.3 C3.

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
// lblFinancialValue.Text — show the value to Finance/Admin, mask for others
If(
 varCurrentUserRole = "Finance" || varCurrentUserRole = "Admin",
 Text(ThisItem.cr_totalvalue, "[$-pt-PT]#,##0.00"),
 "———"
)
```

A mask like this is presentation. Where the requirement is that the value must not reach the client at all,
the column has to be kept out of the result set — see Section E.

**DisplayMode for sensitive fields:**
```powerfx
// Sensitive field — edit only for Admin
If(varCurrentUserRole = "Admin", DisplayMode.Edit, DisplayMode.Disabled)
```

### Audit patterns — where an audit requirement covers the action

An audit row is written for an action when a requirement asks for one: a regulator or auditor needs
who-saw-what or who-did-what with a retention period, a contract or policy demands the trail, or the process
itself reads the history back. Cite the requirement next to the pattern. Where no requirement covers the
action, the trail is a proposal with its cost, not a default — and the entities, retention and mechanism
come from `security/security-controls.md`, not from this file. The patterns below are the *form* the trail
takes once required; Approve, Delete and Export are where the requirement most often lands, not a standing
obligation.

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

**Rule:** the audit row is written *before* the action, never after — the action may fail, and an
unattempted action with no trace is worse than a logged failure.

---

## Section E — Artifact formats

### Dataverse security role definition
```
SECURITY ROLE: [RoleName]
Description: [business purpose in plain language]
Member privilege inheritance: [Direct User (Non-Inherited) | Team privileges inherited]

TABLE PRIVILEGES:
 Table: [schema_name] ([Display Name])
 Create: [None | User | Business Unit | Parent: Child BUs | Organization]
 Read: [same options]
 Write: [same options]
 Delete: [same options]
 Append: [same options]
 Append To: [same options]
```

### Dataverse column security profile
```
PROFILE: [RoleName]_ColumnSecurity
Assign to roles: [list]

COLUMNS:
 [schema_column]:
 Allow Read: [Yes/No]
 Allow Create: [Yes/No]
 Allow Update: [Yes/No]
```

### SharePoint group model
```
PERMISSION GROUP: [SolutionName]_[RoleName]
Permission Level: [Full Control | Contribute | Read | Custom]
Members: [list test users here]

ITEM-LEVEL (if applicable):
 Read: [All items | Only their own]
 Edit: [All items | Only their own]
```

### Azure SQL — row-level security and role-specific views

Row-level security filters *rows*. Hiding *columns* per role is done with role-specific views: a view that
never selects the column cannot return it, so the value does not reach the client at all — unlike a Power Fx
mask, which only stops it being displayed. Which mechanisms are available and how they compose is owned by
`security/security-controls.md`; the RLS scaffold itself is in
[`sql-delivery-conventions.md`](sql-delivery-conventions.md) § Row-level security.

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

The app selects which view to bind per role at `App.OnStart`:

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

### Audit trail columns — once an entity is audited

An entity is audited where a requirement covers it (above). For each entity the requirement covers:
- `cr_audited_by` (lookup → users) — who performed the last write
- `cr_audited_at` (date/time) — when the last write happened
- `cr_audited_action` (choice: Create / Update / Approve / Reject / Delete / Export)
- `cr_audited_notes` (multiline text) — context

**Retention:** the retention period is a requirement, never a value this file supplies. Where the
engagement records one, it is used with its source; where it does not, the period is an open requirement of
the to-be with its cost driver stated, and the team's working figure (5 years, longer for financial records)
is a **proposal to be replaced**, marked as such in the spec. `TODO(team)`: capture the figures actually
agreed per domain in the pilot retro.
