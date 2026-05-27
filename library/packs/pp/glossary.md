# Power Platform — Pack Glossary

PP-specific vocabulary for the `pp` pack. Universal aisa terms live in `library/kernel/glossary.md`. This glossary keeps the lenses, question-bank, and deliverable templates consistent in their Power Platform terminology.

> Reminder: Discovery lenses identify *needs* and *current state*; they do not propose these technologies. The vocabulary below is for the Options phase onward (and for describing existing systems as current state).

## Platform & licensing

| Term | Definition |
|---|---|
| **Power Platform** | Microsoft's low-code suite — Power Apps, Power Automate, Power Pages, Power BI, Copilot Studio — over a shared data and governance layer. |
| **Power Apps** | The app-building service; produces Canvas and Model-driven apps. |
| **Power Automate** | The workflow/automation service (cloud flows + desktop flows / RPA). |
| **Power Pages** | External-facing website service over Dataverse. |
| **Dataverse** | The managed relational data platform underpinning Power Platform: tables, relationships, security, and business logic in one store. |
| **Standard connector** | A connector included with seeded Microsoft 365 licensing (e.g., SharePoint, Outlook, Teams). |
| **Premium connector** | A connector requiring a premium license (e.g., SQL Server, HTTP, custom connectors, SAP). |
| **Per-app plan** | License covering one user for one app/portal. |
| **Per-user plan** | License covering one user for unlimited apps/flows. |
| **Pay-as-you-go** | Azure-metered consumption billing, charged per active user/app/month. |
| **API request limits** | Per-user daily Power Platform request entitlements; high-volume automation can exceed them. |

## Apps & UI

| Term | Definition |
|---|---|
| **Canvas App** | Pixel-precise app with designer-controlled layout; strong for task-focused, mobile, tailored UX. |
| **Model-driven App** | Metadata-driven app generated from the Dataverse schema; strong for data-dense, process-centric scenarios. |
| **Custom page** | A Canvas-built page embedded inside a Model-driven app (hybrid UI). |
| **Power FX** | The Excel-like formula language used in Canvas apps and increasingly across Power Platform. |
| **PCF (Power Apps Component Framework)** | Framework for building reusable custom UI controls. |
| **Responsive layout** | Containers / flexible-height design enabling apps to adapt across form factors. |

## Data

| Term | Definition |
|---|---|
| **Table (entity)** | A Dataverse data set: rows and columns with typed metadata. |
| **Column (field)** | A typed attribute on a table. |
| **Choice (option set)** | A reusable set of named values for a column. |
| **Relationship** | A link between tables (1:N or N:N) with referential behavior. |
| **Business rule** | No-code server/client validation and logic on a table. |
| **Rollup / calculated column** | A server-computed aggregate or formula column. |
| **Dataflow** | A Power Query-based ETL pipeline loading data into Dataverse or a lake. |
| **Virtual table** | A Dataverse table that surfaces external data without copying it. |
| **Delegation** | Pushing query operations to the data source so large data sets are processed server-side. |
| **Delegation limit** | The local row cap (default 500, max 2000) when an operation is non-delegable — a common correctness trap. |
| **Master data** | The authoritative reference data (customers, suppliers, cost centres) and its owner. |

## Automation

| Term | Definition |
|---|---|
| **Cloud flow** | A server-side automated / instant / scheduled workflow. |
| **Desktop flow (RPA)** | UI automation via Power Automate Desktop for systems without APIs. |
| **Trigger** | The event that starts a flow (record change, schedule, request, etc.). |
| **Connection reference** | A solution-aware pointer to a connection, decoupling credentials from the flow. |
| **Environment variable** | A solution parameter whose value differs per environment (DEV/UAT/PROD). |
| **Approvals** | The built-in approvals capability (sequential/parallel) used for sign-off flows. |
| **Child flow** | A reusable flow invoked by a parent flow. |

## Governance & security

| Term | Definition |
|---|---|
| **Environment** | An isolated container for apps, flows, and (optionally) a Dataverse database. |
| **Environment strategy** | The DEV/UAT/PROD (and per-business-unit) layout governing where work lives and promotes. |
| **DLP policy (Data Loss Prevention)** | Rules classifying connectors (business / non-business / blocked) to prevent data exfiltration. |
| **Managed environment** | Premium governance features (sharing limits, usage insights, solution-checker enforcement) on an environment. |
| **Security role** | A Dataverse privilege set assigning create/read/write/delete at record-ownership scopes. |
| **Business unit** | A Dataverse org-hierarchy node scoping data access. |
| **Field-level security** | Per-column access control for sensitive attributes. |
| **Sensitivity label** | A Microsoft Purview classification applied to data/content. |

## ALM

| Term | Definition |
|---|---|
| **Solution** | The unit of packaging/transport for Power Platform components (managed or unmanaged). |
| **ALM** | Application Lifecycle Management — source control, build, and promotion across environments. |
| **Power Platform Pipelines** | Native in-product deployment pipelines promoting solutions DEV→UAT→PROD. |
| **Publisher / prefix** | The solution publisher and its customization prefix on schema names. |

## Discovery fit criteria

Categorical criteria driving the Options-phase architecture comparison (closed vocabularies — wording may vary, category may not).

| Criterion | Allowed values |
|---|---|
| **Volume fit** | inadequate / adequate / strong |
| **Governance & audit fit** | basic / intermediate / strong |
| **Implementation effort** | low / med-low / med / med-high / high |
| **Licensing cost** | minimal / low / med / high |
| **Ongoing maintenance** | low / medium / med-high / high |
| **Reversibility** | high / medium / low |
