# flows-patterns — Power Automate Patterns and Power BI Integration

**Source:** transplanted 2026-05-28 from the previous-aisa references (`ref-09-flows.md`).
**Consulted by:** `lens-technology`, `solution-architect`, `implementation-spec` and `claude-design-brief` deliverable templates.
**Phase eligibility:** Options + Decision only.

Authoritative Power Automate reference for the pp pack. Cross-reference with [`azure-sql-reference.md`](azure-sql-reference.md) for SP-orchestration patterns, [`sharepoint-reference.md`](sharepoint-reference.md) for the SharePoint connector OData syntax, and [`security-patterns.md`](security-patterns.md) for service-account configuration.

---

## POWER AUTOMATE CONNECTOR REFERENCE

| System | Connector | Auth | Limits |
|---|---|---|---|
| SharePoint | SharePoint Online | OAuth | 600 calls/min |
| Dataverse | Microsoft Dataverse | OAuth | 6000 calls/5min |
| Azure SQL | SQL Server | Connection string | Pool size |
| Exchange/Outlook | Office 365 Outlook | OAuth | 1M/day |
| Teams | Microsoft Teams | OAuth | 500/day |
| HTTP | HTTP | Various | Varies by endpoint |
| Excel Online | Excel Online Business | OAuth | Rate limited |
| SFTP | SFTP | Key/Password | File size limits |

---

## FLOW COMPLEXITY CLASSIFICATION

| Tier | Criteria | Estimated Effort |
|---|---|---|
| Simple | ≤5 actions, no loops, no child flows, no error handling | 0.5 days |
| Medium | 5-15 actions, basic loops, simple error handling | 1.5-2 days |
| Complex | Loops with child flows, parallel branches, complex error handling, SP calls, retry logic | 3-4 days |

The same tiering feeds [`estimation-model.md`](estimation-model.md) (`PA flow (simple)`, `PA flow (medium)`, `PA flow (complex)` rows in the effort table).

---

## ERROR HANDLING PATTERNS

### Pattern 1 — Configure Run After (for sequential steps)
```
Action: [Step N]
On failure: Run step [Error Handler]
Error Handler:
 - Send Teams notification: "Flow [name] failed at step [N]. Error: @{body('Step_N')['error']['message']}"
 - Insert to audit_executions / SharePoint error log
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

### Pattern 3 — Retry Policy
Apply to every HTTP action and connector action:
- Type: Exponential interval
- Count: 4 retries
- Interval: PT5S (5 seconds, doubles each retry)
- Maximum interval: PT1H

### Pattern 4 — Throttling handling
```
When action returns 429 (Too Many Requests):
 Wait: @{outputs('HTTP')['headers']['Retry-After']} seconds
 Retry action
```

---

## INGESTION FLOW TEMPLATE

```
TRIGGER: Recurrence [schedule]

ACTION 1: Get data from source
 [HTTP GET / Read file / Query database]
 Retry policy: Exponential (4 retries)

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
 Chunk size: 100-1000 records (avoid timeout)

ACTION 6: Log success
 Insert to audit_executions / SharePoint log
 Teams notification: "Flow [name] completed. [N] records processed."

CATCH:
 Log error to audit_executions
 Teams alert to [team channel]
 Email to [responsible role]
```

---

## CALCULATION FLOW TEMPLATE

```
TRIGGER: [Button in Power Apps / Dataverse record event / Schedule]

ACTION 1: Validate preconditions
 Check: required input data exists
 Condition: valid?
 No: Return error to caller / Update record status to 'Error'

ACTION 2: Read input data
 [Get records from Silver table / Dataverse / SharePoint list]

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

[For Financial formulas:]
 See financial implementations in azure-sql-reference.md or implement via Azure Function

ACTION 4: Write results
 [Update Dataverse record / Insert to Gold table / Update SharePoint item]

ACTION 5: Trigger downstream
 [If this flow outputs to another flow's input: trigger it here]

ACTION 6: Log + notify
 Success log + Teams notification to responsible role

CATCH: Error log + alert
```

---

## PUBLICATION FLOW TEMPLATE

```
TRIGGER: [Approval completed event / Schedule / Manual trigger from Power Apps]

ACTION 1: Get report data
 [Query vw_pbi_[report] or Gold table or SharePoint list view]

ACTION 2: Generate output file
 Option A — Excel via Office Scripts:
 Get file template from SharePoint
 Run Office Script to populate data
 Get file content
 Option B — PDF via Word template:
 Get Word template
 Populate dynamic fields
 Convert to PDF (Premium action: Adobe / OneDrive convert)
 Option C — Email body:
 Compose HTML using Dataverse/SharePoint data

ACTION 3: Deliver
 Option A — Email: Send via Outlook with attachment
 Option B — SharePoint upload: Create file in [destination library]
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

## POWER BI INTEGRATION PATTERNS

### Azure SQL → Power BI
```
Connection: DirectQuery or Import
Source: vw_pbi_[dashboard] views (never raw tables)
RLS: Implement in Power BI using USERPRINCIPALNAME + mapping table
Refresh: Import mode → scheduled (15min / hourly / daily depending on staleness tolerance)
```

### Dataverse → Power BI
```
Connection: Dataverse connector (uses TDS endpoint)
Performance: Better than DirectQuery for large datasets — use Import when possible
RLS: Apply Dataverse security roles (data respects Dataverse permissions)
Refresh: Scheduled refresh (every 30min minimum for near-real-time)
```

### SharePoint → Power BI
```
Connection: SharePoint Online Lists connector
Limitation: No DirectQuery — Import only
Performance: Slow for >10k items — use list views to pre-filter
RLS: Implement in Power BI using USERNAME + SharePoint group membership
Refresh: Scheduled (hourly typically)
```

### Dashboard design principles
- Operational dashboard: current state, today's data, status indicators, alerts
- Audit dashboard: who did what when, approval history, change log
- Historical dashboard: trends, period comparisons, YoY/MoM analysis

---

## SP ORCHESTRATION VIA POWER AUTOMATE (Azure SQL)

```
FLOW: flow_orchestrate_[process]
TRIGGER: [button / schedule / event]

Step 1: Set session context
 SQL: EXEC sp_set_session_context N'user_email', '[current_user]'

Step 2: Call SP chain (sequential)
 SQL: EXEC [dbo].[sp_ingest_[source]] @param = [value]
 Check rows affected / output param for success signal

Step 3: Parallel SPs (if DAG allows)
 Parallel branch A: EXEC [dbo].[sp_calculate_[A]]
 Parallel branch B: EXEC [dbo].[sp_calculate_[B]]

Step 4: Final SP (depends on parallel results)
 SQL: EXEC [dbo].[sp_generate_[output]]

Step 5: Confirm + log
 Query audit_executions for all SP runs in this session
 Send Teams notification with summary
```

---

## FLOW DECOMPOSITION STRATEGY

### When to use Child Flows vs Inline

| Use Child Flow when | Keep Inline when |
|---|---|
| Logic is reused by ≥ 2 parent flows | Logic is unique to one flow |
| Action count within a branch > 15 | Branch has ≤ 15 actions |
| Logic requires its own error handling scope | Error can be caught in parent Try/Catch |
| Logic needs independent retry/timeout settings | Parent retry settings are sufficient |
| Approval sub-process (isolate card + wait) | Simple notification (no wait) |

**Naming:** Child flows follow `[Parent] - [Responsibility] - Child` (e.g. `Invoice - Send Approval Card - Child`).

**Data contract:** Every child flow must define explicit input/output parameters. Never rely on environment variables or implicit context to pass data between parent and child.

### Trigger Selection Guide

| Scenario | Trigger | Why |
|---|---|---|
| Record created/modified in data source | Automated — "When an item is created or modified" | Real-time reaction, lowest latency |
| Batch processing (daily/weekly) | Scheduled — Recurrence | Predictable, avoids API throttling |
| User clicks a button in Canvas App | Instant — Power Apps (V2) | User-initiated, synchronous feedback |
| Approval required after form submit | Automated — triggered by status field change | Decouples UI from flow execution |
| External system pushes data | Automated — HTTP Request (webhook) | No polling, event-driven |
| Data aggregation / reporting | Scheduled — off-hours (e.g. 02:00 UTC) | Avoids peak-hour throttling |

### Flow Categories (5-tier classification)

Classify every flow into exactly one of five categories. The category drives the pattern, the trigger choice, and the risk register.

| Category | Typical Trigger | Typical Pattern | Key Risk |
|---|---|---|---|
| **Ingestion** (external → data layer) | Scheduled / HTTP webhook | Poll or receive → validate → upsert → log | Source unavailable, schema drift |
| **Calculation** (data layer → data layer) | Item modified / Scheduled | Read inputs → compute → write results → log | Delegation limits, circular triggers |
| **Publication** (data layer → external) | Scheduled / Item modified | Query → format → send (email/file/API) → log | Recipient throttling, file size |
| **Monitoring** (cross-cutting) | Scheduled (hourly/daily) | Query metrics → evaluate thresholds → alert | Alert fatigue if thresholds too sensitive |
| **Approval** (human-in-the-loop) | Item created/modified | Create Adaptive Card → wait → route based on response → update record → log | Card expiry (30 days), reassignment |

### Process Decomposition Checklist

When the solution architect designs flows for the proposed option, apply this checklist:

1. **One flow per responsibility** — never mix ingestion + calculation + publication in one flow.
2. **Identify trigger chains** — if Flow A writes a record that triggers Flow B, document the chain explicitly and flag loop risk.
3. **Map to data entities** — every flow must reference which entities it reads and writes.
4. **Estimate action count** — if > 30 actions, decompose into parent + child flows.
5. **Check connector limits** — cross-reference the connector table above; flag any flow that could exceed daily/minute limits at projected volume.
6. **Define error boundary** — each flow must have its own Try/Catch scope; child flows catch their own errors and return error status to parent.

---

## POWER AUTOMATE EXPRESSION CATALOGUE

Most-used expressions for flow specs.

### Text

| Need | Expression | Notes |
|---|---|---|
| Concatenate | `concat('PRJ-', triggerBody?['ID'])` | Unlimited args |
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
| Add days | `addDays(utcNow, 7)` | Negative for subtract |
| Add hours | `addHours(utcNow, 2)` | |
| Day of week | `dayOfWeek(field)` | 0=Sunday |
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
| Divide | `div(total, count)` | No zero guard — wrap in if |
| Min/Max | `min(a, b)` / `max(a, b)` | |

### Array/Collection

| Need | Expression | Notes |
|---|---|---|
| First item | `first(body('Get_items')?['value'])` | |
| Last item | `last(body('Get_items')?['value'])` | |
| Length | `length(body('Get_items')?['value'])` | Item count |
| Filter | `@{body('Filter_array')}` | Use Filter Array action |
| Item property | `items('Apply_to_each')?['Title']` | Inside loop |
| Create array | `createArray('a', 'b', 'c')` | |

---

## ADAPTIVE CARD — APPROVAL TEMPLATE

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

**Usage in flow:**
```
Post Adaptive Card and wait for a response (Teams)
 Channel: [approval channel or 1:1 chat with approver]
 Card: [above JSON with dynamic content]
 Update message: "Decisão: @{body('Post_Adaptive_Card')?['data']?['action']}"
 Should update card: Yes

Condition: action = 'reject' AND empty(approvalComment)
 Yes: Post follow-up card requiring comment
 No: Continue with action routing
```

**Card expiry:** Default 30 days. For urgent approvals, add a parallel Delay + Timeout branch.

---

## CHILD FLOW PATTERNS

### Input/Output contract

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
 Respond to Power App or flow: { line_total, error_message: "" }
 Scope: Catch
 Respond: { line_total: 0, error_message: "Calculation failed: [error detail]" }
```

### Parent calling child

```
Parent Flow:
 Apply to Each [order lines]:
 Run Child Flow: Calculate Line Total
 quantity: items('Apply_to_each')?['Quantity']
 unit_price: items('Apply_to_each')?['UnitPrice']
 discount_pct: items('Apply_to_each')?['Discount']
 Condition: empty(outputs('Run_Child')?['body/error_message'])
 No: Append to errors array → continue loop (do not break)
 After loop: if errors > 0, send alert with error list
```

### Limits

- Max child flow nesting: 8 levels (avoid >2 for clarity)
- Child flow timeout: inherits parent if not set — always set explicit timeout
- Synchronous child flow max duration: 120 seconds

---

## ANTI-PATTERNS — Never Do These

| Anti-pattern | Why it fails | Correct approach |
|---|---|---|
| Apply to Each with Create Item (no throttle) | 429 errors after ~600 items/min on SharePoint | Add Delay of 100ms after each Create, or batch with Send HTTP |
| Trigger "When item modified" + Update same item | Infinite loop — flow triggers itself | Add condition: `Modified By != Flow Service Account` or use flag column |
| Hardcoded URLs/IDs in flow actions | Break on environment promotion (Dev→Prod) | Use Environment Variables for site URLs, list GUIDs, email addresses |
| Single giant flow with 50+ actions | Undebuggable, timeout-prone, impossible to rerun partially | Decompose into parent + child flows (see Decomposition Checklist) |
| Using Terminate (cancel/fail) in child flow | Terminates entire parent chain | Use Respond action with error status instead |
| Storing secrets in flow variables | Visible in run history to anyone with edit access | Use Azure Key Vault or Environment Variable (secret type) |
| No error handling (relying on "I'll see the failure email") | No audit trail, no record state update, no user notification | Always wrap in Try/Catch scope with logging |
