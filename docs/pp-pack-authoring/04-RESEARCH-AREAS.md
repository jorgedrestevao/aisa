# \# Power Platform Research Areas

# 

# The research must cover the following areas.

# 

# The objective is not to document Power Platform comprehensively.

# 

# The objective is to understand the decisions, constraints, patterns and risks

# that matter when deciding whether and how to use Power Platform.

# 

# \---

# 

# \## 01 — Platform Suitability

# 

# Investigate:

# 

# \- What types of problems Power Platform is designed to solve.

# \- What types of problems it is not designed to solve.

# \- Typical characteristics of successful Power Platform solutions.

# \- Characteristics of poor Power Platform candidates.

# \- Factors that make a solution a good, conditional or poor fit.

# \- Boundaries between Power Platform and traditional software development.

# \- Boundaries between Power Platform and other Microsoft technologies.

# \- Situations where a hybrid architecture is preferable.

# 

# Key question:

# 

# > What characteristics of a requirement should influence the decision

# > to use or not use Power Platform?

# 

# \---

# 

# \## 02 — Application Architecture

# 

# Investigate:

# 

# \- Canvas Apps.

# \- Model-driven Apps.

# \- Power Pages.

# \- Custom pages.

# \- Components.

# \- Reusable components.

# \- Application architecture patterns.

# \- UX complexity.

# \- Offline requirements.

# \- Device requirements.

# \- Accessibility.

# \- Application lifecycle considerations.

# \- When each application approach is appropriate.

# \- When Power Apps becomes unsuitable.

# 

# Key question:

# 

# > What application requirements drive the architectural choice?

# 

# \---

# 

# \## 03 — Data Architecture

# 

# Investigate:

# 

# \- Dataverse.

# \- SQL Server / Azure SQL.

# \- SharePoint.

# \- Microsoft Lists.

# \- External databases.

# \- Data ownership.

# \- Data volume.

# \- Data relationships.

# \- Transactional requirements.

# \- Reporting requirements.

# \- Data residency.

# \- Data security.

# \- Data integration.

# \- Data migration.

# \- Master data.

# \- Data quality.

# \- Delegation and query limitations.

# \- When Dataverse should be used.

# \- When external databases should be used.

# 

# Key question:

# 

# > What characteristics of the data should influence the architecture?

# 

# \---

# 

# \## 04 — Automation Architecture

# 

# Investigate:

# 

# \- Power Automate cloud flows.

# \- Desktop flows.

# \- Business process flows.

# \- Event-driven automation.

# \- Scheduled automation.

# \- Approval workflows.

# \- Long-running processes.

# \- Human-in-the-loop processes.

# \- Error handling.

# \- Retry strategies.

# \- Idempotency.

# \- Monitoring.

# \- Transaction boundaries.

# \- High-volume automation.

# \- Integration-triggered automation.

# \- When Power Automate is appropriate.

# \- When another orchestration technology is preferable.

# 

# Key question:

# 

# > What process characteristics determine whether Power Automate

# > is appropriate?

# 

# \---

# 

# \## 05 — Integration

# 

# Investigate:

# 

# \- APIs.

# \- REST.

# \- SOAP.

# \- Custom connectors.

# \- Standard connectors.

# \- On-premises data gateway.

# \- Azure integration services.

# \- SAP integration.

# \- Microsoft 365 integration.

# \- External systems.

# \- Authentication.

# \- Authorization.

# \- Synchronous integration.

# \- Asynchronous integration.

# \- Event-driven integration.

# \- Data volume.

# \- Frequency.

# \- Latency.

# \- Reliability.

# \- Failure handling.

# \- Integration ownership.

# 

# Key question:

# 

# > What integration requirements create architectural constraints?

# 

# \---

# 

# \## 06 — Security

# 

# Investigate:

# 

# \- Identity.

# \- Microsoft Entra ID.

# \- Authentication.

# \- Authorization.

# \- Dataverse security.

# \- Role-based access.

# \- Row-level security.

# \- Field-level security.

# \- Environment security.

# \- Application security.

# \- Connector security.

# \- Secrets.

# \- Service principals.

# \- Managed identities.

# \- Data loss prevention.

# \- Sensitive data.

# \- External users.

# 

# Key question:

# 

# > What security requirements can materially change the solution architecture?

# 

# \---

# 

# \## 07 — Governance

# 

# Investigate:

# 

# \- Environments.

# \- Environment strategy.

# \- DLP policies.

# \- Managed environments.

# \- CoE concepts.

# \- Maker governance.

# \- Ownership.

# \- Application lifecycle governance.

# \- Connector governance.

# \- Naming conventions.

# \- Solution governance.

# \- Tenant-level considerations.

# \- Production support.

# \- Operational ownership.

# 

# Key question:

# 

# > What governance requirements must exist for an enterprise Power Platform solution?

# 

# \---

# 

# \## 08 — ALM / DevOps

# 

# Investigate:

# 

# \- Solutions.

# \- Managed solutions.

# \- Unmanaged solutions.

# \- Source control.

# \- Git.

# \- Deployment pipelines.

# \- Azure DevOps.

# \- CI/CD.

# \- Branching.

# \- Pull requests.

# \- Environment promotion.

# \- Development / Test / Production.

# \- Configuration.

# \- Environment variables.

# \- Connection references.

# \- Deployment strategy.

# \- Rollback.

# \- Versioning.

# \- Release management.

# 

# Key question:

# 

# > What does a production-grade Power Platform delivery lifecycle require?

# 

# \---

# 

# \## 09 — Performance and Scale

# 

# Investigate:

# 

# \- App performance.

# \- Query performance.

# \- Delegation.

# \- Data volume.

# \- Concurrent users.

# \- API limits.

# \- Power Automate limits.

# \- Connector limits.

# \- Dataverse capacity.

# \- Throughput.

# \- Latency.

# \- Large datasets.

# \- High-frequency automation.

# \- Batch processing.

# \- Caching.

# \- Asynchronous patterns.

# 

# Key question:

# 

# > At what point do scale and performance requirements change the architecture?

# 

# \---

# 

# \## 10 — Licensing and Cost

# 

# Investigate:

# 

# \- Power Apps licensing.

# \- Power Automate licensing.

# \- Dataverse capacity.

# \- Premium connectors.

# \- Per-user / per-app concepts.

# \- Pay-as-you-go concepts.

# \- Licensing dependencies.

# \- Environment costs.

# \- Azure dependencies.

# \- Cost drivers.

# \- Total cost of ownership.

# \- Cost implications of architecture decisions.

# 

# Key question:

# 

# > Which requirements and architectural choices materially affect cost?

# 

# \---

# 

# \## 11 — Operations and Support

# 

# Investigate:

# 

# \- Monitoring.

# \- Application Insights where applicable.

# \- Flow monitoring.

# \- Error handling.

# \- Alerting.

# \- Logging.

# \- Audit.

# \- Operational ownership.

# \- Support model.

# \- Incident management.

# \- Backup.

# \- Recovery.

# \- Business continuity.

# \- Disaster recovery.

# \- Production troubleshooting.

# 

# Key question:

# 

# > What operational requirements must be considered before production?

# 

# \---

# 

# \## 12 — Architecture Patterns

# 

# Investigate recurring architecture patterns involving:

# 

# \- Power Apps.

# \- Dataverse.

# \- SQL.

# \- SharePoint.

# \- Power Automate.

# \- APIs.

# \- Azure.

# \- Microsoft 365.

# \- External systems.

# \- Hybrid architectures.

# 

# For each pattern identify:

# 

# \- When to use it.

# \- Why it works.

# \- Main benefits.

# \- Main risks.

# \- Important constraints.

# \- When not to use it.

# 

# \---

# 

# \## 13 — Anti-Patterns

# 

# Actively search for situations where Power Platform

# or a particular Power Platform architecture performs poorly.

# 

# Investigate examples such as:

# 

# \- excessive complexity;

# \- excessive data volume;

# \- inappropriate use of SharePoint as a database;

# \- inappropriate use of Power Automate as a high-volume processing engine;

# \- excessive customisation;

# \- poor ALM;

# \- poor governance;

# \- excessive connector dependency;

# \- integration bottlenecks;

# \- licensing-driven architecture problems;

# \- performance problems;

# \- solutions that should have been built using traditional development;

# \- solutions that should use Azure or another platform.

# 

# Key question:

# 

# > What mistakes repeatedly lead to poor Power Platform solutions?

# 

# \---

# 

# \## 14 — Alternatives

# 

# Investigate when the following may be preferable:

# 

# \- Traditional web application.

# \- Custom API/backend.

# \- Azure Functions.

# \- Azure Logic Apps.

# \- Azure Service Bus.

# \- SQL-based applications.

# \- SharePoint solutions.

# \- Microsoft 365-native solutions.

# \- Other relevant Microsoft technologies.

# 

# The objective is NOT to compare products generically.

# 

# The objective is to understand:

# 

# > What requirement makes an alternative more appropriate than Power Platform?

# 

# \---

# 

# \## 15 — Decision Criteria

# 

# Across all research areas identify measurable or observable

# requirements that can influence architecture decisions.

# 

# Examples:

# 

# \- number of users;

# \- number of concurrent users;

# \- data volume;

# \- transaction volume;

# \- process frequency;

# \- integration frequency;

# \- latency;

# \- availability;

# \- security classification;

# \- regulatory requirements;

# \- offline requirement;

# \- external user requirement;

# \- licensing constraints;

# \- development complexity;

# \- operational complexity;

# \- support requirements.

# 

# These criteria will later become inputs to aisa's decision model.

