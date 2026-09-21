# Flow Craft — Power Automate Patterns, Decomposition and Expressions

<!--
provenance: RUNTIME (domain knowledge) · class: CRAFT
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Not an Options D3 pull target.
-->

Engagement and delivery practice. No independent research authority. This file must not state a platform
limit, threshold or comparative claim as fact; where one is required it refers to the RESEARCH unit that
owns it.

**Limits are not owned here.** Run, action, loop, nesting and duration ceilings, connector request meters,
throttling thresholds, retry entitlements and card lifetimes all belong to
`automation/automation-mechanisms.md` (and `integration/integration-mechanisms.md` for connector and gateway
behaviour). Every heuristic in this file is a *team convention* chosen for debuggability, not a restatement
of a platform ceiling. When a design needs a real number, read the owner — do not copy one from a pattern.

---

## 1 — Connector inventory (what to wire, not what it permits)

| System | Connector | Auth |
|---|---|---|
| SharePoint | SharePoint Online | OAuth |
| Dataverse | Microsoft Dataverse | OAuth |
| Azure SQL | SQL Server | Connection string or Entra auth |
| Exchange/Outlook | Office 365 Outlook | OAuth |
| Teams | Microsoft Teams | OAuth |
| HTTP | HTTP | Varies by endpoint |
| Excel Online | Excel Online (Business) | OAuth |
| SFTP | SFTP | Key / password |

Request meters, per-connection throttles and premium classification: `integration/integration-mechanisms.md`
and `automation/automation-mechanisms.md`. Never size a flow against a figure remembered from a pattern
file.

---

## 2 — Flow complexity classification (delivery tiering)

| Tier | Criteria (team convention) | Estimated effort |
|---|---|---|
| Simple | ≤5 actions, no loops, no child flows, no error handling | 0.5d |
| Medium | 5–15 actions, basic loops, simple error handling | 1.5–2d |
| Complex | Loops with child flows, parallel branches, complex error handling, stored-procedure calls, retry logic | 3–4d |

The same tiering feeds [`estimation-model.md`](estimation-model.md) (`PA flow (simple)` / `(medium)` /
`(complex)` rows). The action counts are our tiering boundaries, not platform boundaries.

---

## 3 — Error handling patterns

### Pattern 1 — Configure Run After (sequential steps)
```
Action: [Step N]
On failure: Run step [Error Handler]
Error Handler:
 - Send Teams notification: "Flow [name] failed at step [N]. Error: @{body('Step_N')['error']['message']}"
 - Insert to audit_executions / error log list
 - Update record status to 'Error' if applicable
```

### Pattern 2 — Try/Catch with Scope
```
Scope: Try
 [main logic actions]
Scope: Catch (Configure Run After: has failed, timed out, skipped)
 Condition: result of Try scope
 Yes (failed): [error handling actions]
 No: [cleanup if needed]
```

### Pattern 3 — Retry policy
Apply to every HTTP action and connector action. These are our chosen settings, not the platform's limits:
- Type: exponential interval
- Count: 4 retries
- Interval: PT5S, doubling each retry
- Maximum interval: PT1H

**Retry safety:** a retry re-executes the side effect. Where the effect is a posting, a notification or an
external write, add an idempotency key or a "already processed" check before the write — otherwise the
duplicate is invisible until reconciliation.

### Pattern 4 — Throttling handling
```
When an action returns 429 (Too Many Requests):
 Wait: @{outputs('HTTP')['headers']['Retry-After']} seconds
 Retry the action
```
Honour the response header rather than a hardcoded wait. What the actual throttle is:
`automation/automation-mechanisms.md`.

---

## 4 — Ingestion flow template

```
TRIGGER: Recurrence [schedule]

ACTION 1: Get data from source
 [HTTP GET / Read file / Query database]
 Retry policy: exponential

ACTION 2: Parse and validate
 Parse JSON / CSV
 Condition: Is data valid?
 No: Log error + send alert + terminate

ACTION 3: Deduplicate
 Filter: records already in destination
 [Query destination for existing IDs]

ACTION 4: Transform
 Select / Compose to map source fields to destination fields

ACTION 5: Insert to destination
 [Create records in Dataverse / SharePoint / SQL]
 Chunk the writes — pick the chunk size from the destination's own guidance, and make the chunk
 loop resumable so a partial run can be re-driven without duplicating rows

ACTION 6: Log success
 Insert to audit_executions / log list
 Teams notification: "Flow [name] completed. [N] records processed."

CATCH:
 Log error to audit_executions
 Teams alert to [team channel]
 Email to [responsible role]
```

---

## 5 — Calculation flow template

```
TRIGGER: [Button in the app / record event / Schedule]

ACTION 1: Validate preconditions
 Check: required input data exists
 Condition: valid?
 No: Return error to caller / Update record status to 'Error'

ACTION 2: Read input data
 [Get records from Silver table / Dataverse / list]

ACTION 3: Calculate
 [Apply to Each if iterating]
 [Compose/Select for transformations]
 [Child flow for reusable complex calculation]

[For SUMPRODUCT pattern:]
 Initialize variable: weighted_sum = 0
 Initialize variable: total_weight = 0
 Apply to Each record:
 Increment weighted_sum by (record.quantity * record.value)
 Increment total_weight by record.quantity
 Compose: result = IF(total_weight > 0, weighted_sum / total_weight, 0)

[For financial formulas:]
 See excel-translation.md § FINANCIAL and sql-delivery-conventions.md § financial formulas

ACTION 4: Write results
 [Update record / Insert to Gold table / Update list item]

ACTION 5: Trigger downstream
 [If this flow outputs to another flow's input: trigger it here]

ACTION 6: Log + notify
 Success log + Teams notification to responsible role

CATCH: Error log + alert
```

---

## 6 — Publication flow template

```
TRIGGER: [Approval completed event / Schedule / Manual trigger from the app]

ACTION 1: Get report data
 [Query the reporting view or Gold table or list view]

ACTION 2: Generate output file
 Option A — Excel via Office Scripts:
 Get file template from SharePoint
 Run Office Script to populate data
 Get file content
 Option B — PDF via Word template:
 Get Word template
 Populate dynamic fields
 Convert to PDF (check the conversion action's licensing classification before designing on it)
 Option C — Email body:
 Compose HTML from the source data

ACTION 3: Deliver
 Option A — Email: send with attachment
 Option B — SharePoint upload: create file in [destination library]
 Option C — External system: HTTP POST to API endpoint

ACTION 4: Archive
 Copy to archive folder: [path]/[YYYY-MM]/[filename_YYYYMMDD_HHmm].[ext]

ACTION 5: Log + confirm
 Update record status to 'Published'
 Log to audit table
 Teams notification: "Report [name] delivered to [recipients]"

CATCH: Error log + alert to [responsible role]
```

---

## 7 — Reporting integration patterns

Craft-side wiring only. Whether a given connection mode, refresh cadence or row-level-security mechanism is
available, and at what ceiling, is owned by `integration/integration-mechanisms.md`,
`data/query-and-delegation.md` and `security/security-controls.md`.

### Azure SQL → Power BI
```
Source: the vw_pbi_[dashboard] views — never raw tables
RLS: implement with USERPRINCIPALNAME + a mapping table (same mapping table the app uses)
Refresh: set the cadence from the business staleness tolerance, and write that tolerance into the spec
```

### Dataverse → Power BI
```
Connection: Dataverse connector
RLS: rely on the Dataverse security model where the report is user-scoped
Refresh: cadence from staleness tolerance; confirm the available minimum with the integration owner
```

### SharePoint list → Power BI
```
Connection: SharePoint Online Lists connector
Pre-filter at the source with list views rather than pulling everything and filtering in the model
RLS: implement with USERNAME + group membership mapping
Refresh: cadence from staleness tolerance
```

### Dashboard design principles
- Operational dashboard: current state, today's data, status indicators, alerts
- Audit dashboard: who did what when, approval history, change log
- Historical dashboard: trends, period comparisons, YoY/MoM analysis

---

## 8 — Stored-procedure orchestration via Power Automate

```
FLOW: flow_orchestrate_[process]
TRIGGER: [button / schedule / event]

Step 1: Set session context
 SQL: EXEC sp_set_session_context N'user_email', '[current_user]'

Step 2: Call SP chain (sequential)
 SQL: EXEC [dbo].[sp_ingest_[source]] @param = [value]
 Check rows affected / output param for the success signal

Step 3: Parallel SPs (if the DAG allows)
 Parallel branch A: EXEC [dbo].[sp_calculate_[A]]
 Parallel branch B: EXEC [dbo].[sp_calculate_[B]]

Step 4: Final SP (depends on the parallel results)
 SQL: EXEC [dbo].[sp_generate_[output]]

Step 5: Confirm + log
 Query audit_executions for all SP runs in this session
 Send Teams notification with the summary
```

Session context is per-connection and does not survive across actions — see
`sql-delivery-conventions.md` § SQL connector for the ordering rule.

---

## 9 — Flow decomposition

### Child flow vs inline

| Use a child flow when | Keep inline when |
|---|---|
| Logic is reused by ≥ 2 parent flows | Logic is unique to one flow |
| A branch grows past ~15 actions (readability convention) | The branch stays small |
| Logic needs its own error-handling scope | The error can be caught in the parent Try/Catch |
| Logic needs independent retry/timeout settings | Parent retry settings are sufficient |
| Approval sub-process (isolate card + wait) | Simple notification (no wait) |

**Naming:** child flows follow `[Parent] - [Responsibility] - Child` (e.g. `Invoice - Send Approval Card -
Child`).

**Data contract:** every child flow must define explicit input and output parameters. Never rely on
environment variables or implicit context to pass data between parent and child.

### Trigger selection guide

| Scenario | Trigger | Why |
|---|---|---|
| Record created/modified in the data source | Automated — "when an item is created or modified" | Reacts as the data changes |
| Batch processing (daily/weekly) | Scheduled — recurrence | Predictable, keeps request volume in a known window |
| User clicks a button in the app | Instant — Power Apps (V2) | User-initiated, synchronous feedback |
| Approval required after form submit | Automated — triggered by a status field change | Decouples the UI from flow execution |
| External system pushes data | Automated — HTTP request (webhook) | No polling, event-driven |
| Data aggregation / reporting | Scheduled — off-hours | Keeps the load off the interactive window |

### Flow categories (5-tier classification)

Classify every flow into exactly one category. The category drives the pattern, the trigger choice, and the
risk register.

| Category | Typical trigger | Typical pattern | Key risk |
|---|---|---|---|
| **Ingestion** (external → data layer) | Scheduled / HTTP webhook | Poll or receive → validate → upsert → log | Source unavailable, schema drift |
| **Calculation** (data layer → data layer) | Item modified / scheduled | Read inputs → compute → write results → log | Query delegability, circular triggers |
| **Publication** (data layer → external) | Scheduled / item modified | Query → format → send (email/file/API) → log | Recipient throttling, file size |
| **Monitoring** (cross-cutting) | Scheduled | Query metrics → evaluate thresholds → alert | Alert fatigue if thresholds are too sensitive |
| **Approval** (human-in-the-loop) | Item created/modified | Create adaptive card → wait → route on response → update record → log | Card lifetime and reassignment (see the automation owner) |

### Process decomposition checklist

1. **One flow per responsibility** — never mix ingestion + calculation + publication in one flow.
2. **Identify trigger chains** — if flow A writes a record that triggers flow B, document the chain
   explicitly and flag the loop risk.
3. **Map to data entities** — every flow states which entities it reads and writes.
4. **Keep flows readable** — past roughly 30 actions, decompose into parent + child. This is our
   debuggability convention; the platform's own action ceiling is a separate question for the automation
   owner.
5. **Check the meters** — cross-reference `automation/automation-mechanisms.md` and
   `integration/integration-mechanisms.md` for the request and run meters that apply, and test the flow at
   projected volume rather than at demo volume.
6. **Define the error boundary** — each flow has its own Try/Catch scope; child flows catch their own errors
   and return an error status to the parent.

---

## 10 — Expression catalogue

### Text

| Need | Expression | Notes |
|---|---|---|
| Concatenate | `concat('PRJ-', triggerBody?['ID'])` | |
| Substring | `substring(field, 0, 4)` | Start index, length |
| Replace | `replace(field, 'old', 'new')` | Case-sensitive |
| To upper | `toUpper(field)` | |
| To lower | `toLower(field)` | |
| Trim | `trim(field)` | Whitespace only |
| Contains | `contains(field, 'text')` | Returns bool |
| Length | `length(field)` | Returns int |
| Split | `split(field, ';')` | Returns array |
| Join | `join(variables('myArray'), ', ')` | Array → string |

### Date/Time

| Need | Expression | Notes |
|---|---|---|
| Current UTC | `utcNow` | ISO 8601 |
| Format date | `formatDateTime(field, 'dd/MM/yyyy')` | PT format |
| Format date+time | `formatDateTime(field, 'dd/MM/yyyy HH:mm')` | 24h |
| Add days | `addDays(utcNow, 7)` | Negative to subtract |
| Add hours | `addHours(utcNow, 2)` | |
| Day of week | `dayOfWeek(field)` | 0 = Sunday |
| Difference in days | `div(sub(ticks(endDate), ticks(startDate)), 864000000000)` | Ticks-based |
| Start of month | `startOfMonth(utcNow)` | |
| Convert timezone | `convertTimeZone(utcNow, 'UTC', 'Romance Standard Time')` | PT timezone |

### Logic

| Need | Expression | Notes |
|---|---|---|
| If/else | `if(equals(field, 'A'), 'result1', 'result2')` | Ternary |
| Null check | `coalesce(field, 'default')` | First non-null |
| Is null/empty | `empty(field)` | Returns bool |
| Equals | `equals(field, 'value')` | Type-safe |
| Greater than | `greater(field, 100)` | |
| And | `and(equals(a, 1), greater(b, 0))` | Nested |
| Or | `or(equals(a, 1), equals(a, 2))` | Nested |
| Not | `not(equals(field, 'Draft'))` | |

### Number

| Need | Expression | Notes |
|---|---|---|
| Parse int | `int(field)` | String → integer |
| Parse float | `float(field)` | String → decimal |
| Round | `formatNumber(field, 'N2')` | 2 decimal places |
| Multiply | `mul(quantity, unitPrice)` | |
| Divide | `div(total, count)` | No zero guard — wrap in `if` |
| Min/Max | `min(a, b)` / `max(a, b)` | |

### Array/Collection

| Need | Expression | Notes |
|---|---|---|
| First item | `first(body('Get_items')?['value'])` | |
| Last item | `last(body('Get_items')?['value'])` | |
| Length | `length(body('Get_items')?['value'])` | Item count |
| Filter | `@{body('Filter_array')}` | Use the Filter Array action |
| Item property | `items('Apply_to_each')?['Title']` | Inside a loop |
| Create array | `createArray('a', 'b', 'c')` | |

---

## 11 — Adaptive card — approval template

Standard approval card for Teams. Adapt fields per entity. PT example labels.

```json
{
 "type": "AdaptiveCard",
 "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
 "version": "1.4",
 "body": [
 {
 "type": "TextBlock",
 "text": "Aprovação Pendente",
 "weight": "Bolder",
 "size": "Large"
 },
 {
 "type": "FactSet",
 "facts": [
 { "title": "Tipo:", "value": "${entity_type}" },
 { "title": "Referência:", "value": "${reference_code}" },
 { "title": "Requerente:", "value": "${requester_name}" },
 { "title": "Data:", "value": "${request_date}" },
 { "title": "Valor:", "value": "${formatted_amount}" }
 ]
 },
 {
 "type": "TextBlock",
 "text": "Observações:",
 "weight": "Bolder",
 "spacing": "Medium"
 },
 {
 "type": "TextBlock",
 "text": "${notes}",
 "wrap": true
 },
 {
 "type": "Input.Text",
 "id": "approvalComment",
 "placeholder": "Comentário (obrigatório para rejeição)",
 "isMultiline": true
 }
 ],
 "actions": [
 {
 "type": "Action.Submit",
 "title": "Aprovar",
 "data": { "action": "approve" },
 "style": "positive"
 },
 {
 "type": "Action.Submit",
 "title": "Rejeitar",
 "data": { "action": "reject" },
 "style": "destructive"
 },
 {
 "type": "Action.Submit",
 "title": "Devolver",
 "data": { "action": "return" }
 }
 ]
}
```

**Usage in the flow:**
```
Post adaptive card and wait for a response (Teams)
 Channel: [approval channel or 1:1 chat with the approver]
 Card: [the JSON above with dynamic content]
 Update message: "Decisão: @{body('Post_Adaptive_Card')?['data']?['action']}"
 Should update card: Yes

Condition: action = 'reject' AND empty(approvalComment)
 Yes: post a follow-up card requiring a comment
 No: continue with action routing
```

**Card lifetime:** an unanswered card does not wait forever. Read the current lifetime from
`automation/automation-mechanisms.md` and, for anything time-critical, add an explicit parallel
Delay + timeout branch with an escalation route rather than depending on the default.

---

## 12 — Child flow contract

### Input/output contract

```
Child Flow: [Parent] - [Calculate Line Total] - Child
INPUTS:
 quantity (Number, required)
 unit_price (Number, required)
 discount_pct (Number, optional, default 0)
OUTPUTS:
 line_total (Number)
 error_message (String, empty if success)

LOGIC:
 Scope: Try
 Compose: line_total = mul(quantity, unit_price) * (1 - div(discount_pct, 100))
 Respond to the caller: { line_total, error_message: "" }
 Scope: Catch
 Respond: { line_total: 0, error_message: "Calculation failed: [error detail]" }
```

### Parent calling child

```
Parent Flow:
 Apply to Each [order lines]:
 Run child flow: Calculate Line Total
 quantity: items('Apply_to_each')?['Quantity']
 unit_price: items('Apply_to_each')?['UnitPrice']
 discount_pct: items('Apply_to_each')?['Discount']
 Condition: empty(outputs('Run_Child')?['body/error_message'])
 No: append to the errors array → continue the loop (do not break)
 After the loop: if errors > 0, send an alert with the error list
```

### Contract rules

- **Always set an explicit timeout** on a child flow. Inheriting the parent's is how a hung child becomes a
  hung parent chain.
- **Keep nesting shallow** — depth beyond two levels is unreadable in run history and hard to diagnose.
  There is also a hard platform nesting ceiling; that figure is owned by
  `automation/automation-mechanisms.md`, not by this file.
- **Never Terminate inside a child** — it takes the whole parent chain with it. Respond with an error status
  instead.
- **A synchronous child is a latency contract** — if the caller waits, the child must be short. Anything
  long-running becomes fire-and-forget plus a completion signal.

---

## 13 — Anti-patterns

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Apply to Each with a write action, unthrottled | The loop outruns the destination's request meter and starts failing part-way, leaving a partial write | Pace the loop, batch the writes, and make the loop re-drivable; read the meter from the automation/integration owner |
| Trigger "when item modified" + update the same item | Infinite loop — the flow triggers itself | Add a condition (`Modified By != flow service account`) or a flag column |
| Hardcoded URLs/IDs in flow actions | Breaks on environment promotion | Environment variables for site URLs, list GUIDs, addresses (`delivery-conventions.md` §3) |
| One giant flow | Undebuggable, timeout-prone, impossible to re-run partially | Decompose into parent + child (§9) |
| `Terminate` in a child flow | Terminates the entire parent chain | Respond with an error status |
| Secrets in flow variables | Visible in run history to anyone with edit access | Key Vault or a secret-type environment variable |
| No error handling ("I'll see the failure email") | No audit trail, no record state update, no user notification | Always Try/Catch with logging (§3) |
| Retry without an idempotency key | The retry re-executes the side effect; the duplicate posting or notification is invisible until reconciliation | Idempotency key or a processed-marker check before the write |
