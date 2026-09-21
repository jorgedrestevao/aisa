const fs = require("fs");
const path = require("path");
const {
  AlignmentType, BorderStyle, Document, Footer, Header, HeadingLevel,
  ImageRun, LevelFormat, Packer, PageBreak, PageNumber, Paragraph,
  ShadingType, Table, TableCell, TableRow, TextRun, VerticalAlign,
  WidthType,
} = require("docx");

const OUT = __dirname;
const VERSION = "1.0";
const EFFECTIVE_DATE = "3 September 2026";
const C = {
  navy: "12304A", blue: "0072CE", cyan: "00A6D6", orange: "F59E0B",
  ink: "1F2937", slate: "64748B", pale: "EAF4FA", mist: "F5F8FA",
  line: "CBD5E1", white: "FFFFFF", green: "138A5B", red: "B42318",
};

const evidence = [
  "Canonical manifest — research/pp/evidence/canonical-manifest.md",
  "Governance evidence — research/pp/evidence/governance.md",
  "Security evidence — research/pp/evidence/security.md",
  "ALM / DevOps evidence — research/pp/evidence/alm-devops.md",
  "Operations and support evidence — research/pp/evidence/operations-support.md",
  "Anti-pattern evidence — research/pp/evidence/anti-patterns.md",
];

const docs = [
  {
    file: "01-Governance-Charter.docx", code: "PP-GOV-001", title: "Power Platform\nGovernance Charter",
    strapline: "Decision rights, operating principles and accountability for a governed platform",
    owner: "Power Platform Governance Lead", approver: "Digital / Technology Governance Board", review: "Annual and after material platform change",
    sections: [
      { h: "Purpose and intended outcomes", lead: "This charter establishes how Power Platform is governed so teams can deliver quickly without compromising security, accountability, production integrity or cost control.", bullets: ["Enable delivery teams through clear, proportionate guardrails.", "Protect organisational data, identities, services and regulatory obligations.", "Maintain production traceability, durable ownership, supportability and recoverability.", "Make licensing, capacity and operating costs visible before architectural commitment."] },
      { h: "Scope", bullets: ["Applies to Power Apps, Power Automate, Dataverse, Power Pages, Copilot Studio assets, connectors, gateways and associated services.", "Applies to employees, contractors, suppliers, makers, developers, administrators, owners and support personnel.", "Hybrid components remain subject to the governance of their owning Azure, enterprise-platform or on-premises estate in addition to this framework."] },
      { h: "Governance principles", numbered: true, bullets: ["Govern centrally and enable delivery locally through a hybrid operating model.", "Prefer preventive controls; detective reporting alone is not assurance.", "Use source control as the authoritative representation of solution assets.", "Separate creation, approval, deployment, administration and audit duties where risk requires it.", "Assign durable business, technical and support ownership to every production asset.", "Prefer built-in platform governance and documented APIs before custom tooling.", "Design for least privilege, data minimisation, observable operation and recovery.", "Treat licensing, capacity and external-estate obligations as architecture constraints."] },
      { h: "Decision rights", table: [["Decision", "Accountable role", "Required consultation"], ["Tenant baseline, groups and data policies", "Platform Owner", "Security, Architecture, Data Protection"], ["Solution classification and architecture", "Business / Technical Owner", "Architecture, Security, Data Owner"], ["Production release", "Release Approver", "Product, Support and Security as required"], ["Exception acceptance", "Risk Owner", "Control Owner, Security, Architecture"], ["Retirement and data disposition", "Business Owner", "Data Owner, Support, Records / Privacy"]] },
      { h: "Core accountabilities", cards: [["PLATFORM OWNER", "Service strategy, tenant controls, capacity, roadmap and operating model."], ["BUSINESS OWNER", "Value, lawful use, funding, continuity and retirement."], ["TECHNICAL OWNER", "Design, quality, delivery, documentation and supportability."], ["SUPPORT OWNER", "Monitoring, runbooks, incidents, recovery and service reporting."]] },
      { h: "Governance rhythm", timeline: [["WEEKLY", "Ownership, orphan, inactivity, failed automation, security and platform-action review."], ["MONTHLY", "Service health, capacity, licences, exceptions, connectors and production changes."], ["QUARTERLY", "Access certification, criticality, recovery readiness and control effectiveness."], ["ANNUALLY", "Charter, standards, taxonomy, risk appetite and roadmap review."]] },
    ],
  },
  {
    file: "02-Engineering-Standards.docx", code: "PP-STD-001", title: "Power Platform\nEngineering Standards",
    strapline: "Mandatory engineering practices for secure, maintainable and supportable solutions",
    owner: "Power Platform Architecture Lead", approver: "Architecture Review Board", review: "Every six months",
    sections: [
      { h: "Environment and solution design", rules: [["MUST", "Business-critical solutions use dedicated development, test/UAT and production environments."], ["MUST NOT", "Production workloads run in the default environment."], ["MUST", "Non-development environments receive managed solutions only, except under an approved exception."], ["MUST", "One approved publisher and prefix is selected at project inception and used consistently."], ["MUST NOT", "An unmanaged component is included in more than one solution."], ["SHOULD", "Tables are owned by one designated solution; dependencies are documented and tested."], ["MUST", "Irreversible provisioning choices receive architecture review before creation."]] },
      { h: "Source, configuration and secrets", rules: [["MUST", "Source control is the source of truth and changes are attributable to reviewed work."], ["MUST", "Target-specific values are supplied through deployment settings or approved configuration stores."], ["MUST", "Connection references are used where supported."], ["MUST NOT", "Secrets are committed to source control or stored as ordinary text configuration."], ["SHOULD", "Production automations use governed workload identities or service-owned connections."]] },
      { h: "Data and integration", rules: [["MUST", "Every solution declares data classification, systems of record, retention needs and data owners."], ["MUST", "Connector combinations comply with applicable tenant and environment policies."], ["MUST", "Custom connectors, HTTP endpoints, gateways and external APIs receive security and architecture review."], ["MUST", "Integration contracts define identity, throttling, timeout, retry, idempotency, errors and observability."], ["MUST", "Cross-system writes define reconciliation and compensation where atomicity is unavailable."], ["MUST", "Performance-sensitive designs are measured with representative workloads."]] },
      { h: "Quality and operability", rules: [["MUST", "Solutions pass static analysis, dependency validation and required tests before production."], ["MUST", "Critical findings block release unless accepted through the exception process."], ["MUST", "Production components expose telemetry sufficient to identify failures and affected transactions."], ["SHOULD", "Accessibility and maintainability are verified through checker rules and user testing."], ["MUST", "Design records identify limits, unknowns and volatile assumptions requiring revalidation."]] },
    ],
  },
  {
    file: "03-Mandatory-Control-Policy.docx", code: "PP-POL-001", title: "Mandatory\nControl Policy",
    strapline: "The minimum control baseline for Power Platform environments and workloads",
    owner: "Power Platform Control Owner", approver: "Technology Risk Owner", review: "Quarterly",
    sections: [
      { h: "Control baseline", controls: [["CTL-01", "Environment", "No production workload in the default environment.", "Environment inventory"], ["CTL-02", "Ownership", "Named business, technical and support owners.", "Application register"], ["CTL-03", "Lifecycle", "Separate lifecycle environments for critical solutions.", "Architecture record"], ["CTL-04", "Integrity", "Managed solutions in non-development environments.", "Solution-layer report"], ["CTL-05", "Traceability", "Deployment from approved source and pipeline.", "Pipeline log + commit"], ["CTL-06", "Integrity", "No unmanaged production customisations.", "Environment setting + layer check"], ["CTL-07", "Data", "An applicable data policy covers every environment.", "Policy export"], ["CTL-08", "Integration", "Custom and HTTP integrations receive review.", "Approved design record"], ["CTL-09", "Identity", "Production identity is durable and governed.", "Owner / connection inventory"], ["CTL-10", "Release", "Required release gates and tests pass.", "Release evidence bundle"], ["CTL-11", "Resilience", "Recovery is documented and exercised.", "Runbook + exercise record"], ["CTL-12", "Risk", "Exceptions have an owner, controls and expiry.", "Exception register"]] },
      { h: "Enforcement model", bullets: ["Preventive controls MUST use tenant settings, managed environments, environment groups, data policies, sharing restrictions, pipelines and solution integrity controls where supported.", "Where technical enforcement is unavailable, the control owner MUST define a detective check, cadence, evidence location and remediation SLA.", "Control implementations MUST account for platform limitations, non-retroactive settings and connector paths outside the selected control surface."] },
      { h: "Non-compliance", callout: { label: "RELEASE RULE", text: "Critical non-compliance blocks release or service onboarding unless an authorised, time-bound exception explicitly accepts the residual risk." }, bullets: ["Production non-compliance is assigned an incident or remediation record with an accountable owner and due date.", "Repeated or expired exceptions are escalated to the Technology Risk Owner.", "Evidence is retained according to organisational audit and records requirements."] },
    ],
  },
  {
    file: "04-Delivery-and-Release-Process.docx", code: "PP-PRO-001", title: "Delivery & Release\nProcess",
    strapline: "A traceable path from intake to production operation and retirement",
    owner: "Engineering Delivery Lead", approver: "Power Platform Service Owner", review: "Every six months",
    sections: [
      { h: "Delivery lifecycle", timeline: [["01  INTAKE", "Record purpose, users, data, criticality, licensing and support expectations."], ["02  DESIGN", "Approve environment, solution boundary, identity, security, recovery and operating model."], ["03  BUILD", "Develop in an approved environment against source-controlled work items."], ["04  VALIDATE", "Run peer, static, dependency, functional, security and material performance checks."], ["05  PROMOTE", "Create a managed artifact and deploy through the approved pipeline."], ["06  VERIFY", "Smoke-test identity, connections, monitoring and business operation."], ["07  OPERATE", "Transfer ownership, support, runbooks, known limits and recovery procedures."], ["08  RETIRE", "Approve shutdown, handle data, remove access and update the inventory."]] },
      { h: "Release gates", table: [["Gate", "Minimum evidence", "Accountable outcome"], ["Architecture ready", "Approved design and classification", "Build may begin"], ["Build ready", "Reviewed change linked to work", "Artifact may be created"], ["Test ready", "Deployable artifact and test plan", "Controlled validation begins"], ["Production ready", "Controls, acceptance and support readiness", "Release is authorised"], ["Release complete", "Smoke test, monitoring and release record", "Service is operational"]] },
      { h: "Production rules", rules: [["MUST NOT", "Direct authoring occurs in production unless emergency access is invoked."], ["MUST", "The deploying identity and resulting component ownership are intentional and documented."], ["MUST", "Environment values and connection bindings are supplied per target."], ["MUST NOT", "A release claims instant rollback unless the exact method has been tested."], ["MUST", "Failures follow the documented incident, restore, redeploy, forward-fix or reconciliation path."]] },
    ],
  },
  {
    file: "05-Environment-and-Access-Standard.docx", code: "PP-STD-002", title: "Environment & Access\nStandard",
    strapline: "Environment purpose, provisioning boundaries and least-privilege access",
    owner: "Power Platform Platform Owner", approver: "Security and Platform Governance", review: "Quarterly",
    sections: [
      { h: "Environment taxonomy", table: [["Type", "Permitted purpose", "Key boundary"], ["Default", "Personal M365 productivity", "No production; restrictive baseline"], ["Developer", "Individual / isolated development", "No production users"], ["Test / UAT", "Validation and training", "Controlled data and access"], ["Production", "Live supported workload", "Managed deployment; least privilege"], ["Dataverse for Teams", "Bounded team productivity", "Not enterprise production by default"]] },
      { h: "Creation and grouping", rules: [["MUST", "Environment creation is restricted to authorised roles or an approved workflow."], ["MUST", "Existing environments are inventoried because creation restrictions are not retroactive."], ["SHOULD", "Managed environments are grouped by common control requirements and exception needs."], ["MUST", "Group rules are assessed before membership because they can overwrite and lock settings."], ["MUST", "Region and business-unit separation is decided before provisioning."], ["MUST", "Names identify purpose, lifecycle stage and organisational context."]] },
      { h: "Access baseline", rules: [["MUST", "Access follows least privilege and uses security groups where supported."], ["MUST NOT", "Makers and developers hold routine production authoring rights."], ["MUST", "Administrative roles are separately assigned and periodically certified."], ["MUST", "Guest access receives explicit business, security and data-owner approval."], ["MUST", "Sharing with Everyone remains disabled or constrained by the approved baseline."], ["MUST", "Emergency privileged access is time-bound, logged, reviewed and removed."]] },
      { h: "Default environment", callout: { label: "BOUNDARY", text: "The default environment is for personal Microsoft 365 productivity—not supported production workloads." }, bullets: ["Rename and communicate it as personal productivity.", "Apply the approved restrictive connector and data-policy baseline.", "Route eligible makers to personal developer environments.", "Restrict manual environment creation separately.", "Identify and migrate existing production or sensitive workloads through a controlled process."] },
    ],
  },
  {
    file: "06-Application-Lifecycle-Standard.docx", code: "PP-STD-003", title: "Application Lifecycle\nStandard",
    strapline: "Accountability from registration and classification through operation and retirement",
    owner: "Application Portfolio Owner", approver: "Power Platform Governance Lead", review: "Quarterly",
    sections: [
      { h: "Register and classify", rules: [["MUST", "Every application, flow, site, agent and material integration is registered before production use."], ["MUST", "The register records purpose, criticality, data, users, environment, dependencies, licences and lifecycle state."], ["MUST", "Every asset has named business, technical and support owners."], ["MUST", "Criticality determines approval, testing, monitoring, recovery and review depth."]] },
      { h: "Operate and review", bullets: ["Owners review continued need, access, licensing, compliance, supportability and technical health at the assigned cadence.", "Ownership change includes validation of permissions, connections, data access and transferred knowledge; reassignment alone is insufficient.", "Ownerless, inactive or non-compliant assets enter triage with a defined remediation SLA.", "Operational changes follow the same traceable release process as feature changes."] },
      { h: "Retire", timeline: [["DECIDE", "Business and data owners approve retirement."], ["DISCOVER", "Identify dependencies, consumers and required notices."], ["PRESERVE", "Migrate, archive or dispose of data according to retention obligations."], ["DISCONNECT", "Remove or reassign access, identities, licences, gateways, endpoints and monitoring."], ["CLOSE", "Quarantine where appropriate and retain the decision and evidence in inventory."]] },
    ],
  },
  {
    file: "07-Governance-Exception-Process.docx", code: "PP-PRO-002", title: "Governance Exception\nProcess",
    strapline: "A controlled, time-bound route for accepting residual risk",
    owner: "Technology Risk and Compliance", approver: "Designated Risk Owner", review: "Annual",
    sections: [
      { h: "Eligibility", callout: { label: "EXCEPTION PRINCIPLE", text: "An exception is not an exemption from accountability. It is a documented, temporary acceptance of residual risk." }, bullets: ["An exception MAY be requested only when a mandatory control cannot reasonably be met and value outweighs residual risk.", "Exceptions MUST NOT bypass licensing, legal, regulatory, privacy or contractual duties.", "A platform limitation does not automatically approve an exception; risk must still be assessed."] },
      { h: "Required request", table: [["Information", "Minimum content"], ["Scope", "Exact control, assets and environments"], ["Ownership", "Requestor, business, technical and risk owners"], ["Rationale", "Business need and alternatives considered"], ["Risk", "Threat, likelihood, impact, data and residual rating"], ["Compensation", "Preventive / detective controls and monitoring"], ["Remediation", "Plan, evidence location and target date"], ["Validity", "Start, expiry and review cadence"]] },
      { h: "Workflow", timeline: [["01  ASSESS", "Control Owner confirms applicability and compliant alternatives."], ["02  REVIEW", "Security, Architecture, Privacy or Legal review according to risk."], ["03  DECIDE", "Risk Owner accepts, rejects or applies conditions."], ["04  RECORD", "Approved exception enters the central register and is communicated."], ["05  MONITOR", "Evidence and compensating controls are reviewed to schedule."], ["06  CLOSE", "Control is met, asset retired, risk removed—or renewal is approved before expiry."]] },
      { h: "Register", table: [["Field", "Required value"], ["Exception ID", "Unique identifier"], ["Scope and control", "Named assets, environments and control ID"], ["Owners", "Business, technical, control and risk"], ["Risk", "Inherent and residual rating"], ["Compensation", "Controls, monitoring and evidence"], ["Validity", "Approval, review and expiry dates"], ["Status", "Requested / approved / rejected / expired / closed"]] },
    ],
  },
  {
    file: "08-Governance-Operations-Runbook.docx", code: "PP-RUN-001", title: "Governance Operations\nRunbook",
    strapline: "Repeatable oversight, evidence collection, escalation and recovery activities",
    owner: "Power Platform Operations Lead", approver: "Power Platform Service Owner", review: "Quarterly",
    sections: [
      { h: "Operating cadence", cards: [["WEEKLY", "Actions, inventory change, orphan/inactive assets, risky sharing, failed automation, credentials and service health."], ["MONTHLY", "Capacity, storage, limits, premium licences, connectors, gateways, releases, unmanaged layers and exceptions."], ["QUARTERLY", "Privileged access, application criticality, recovery readiness, control effectiveness and trend reporting."], ["EVENT-DRIVEN", "Platform change, incident, audit request, new connector, external exposure or material architecture change."]] },
      { h: "Weekly procedure", numbered: true, bullets: ["Collect current platform, inventory, ownership, automation, security and health signals.", "Validate severity, affected workload, owner and business impact.", "Create and assign remediation records against the agreed SLA.", "Escalate critical production, data or identity exposure immediately.", "Record reviewer, data source, findings, decisions, tickets and due dates."] },
      { h: "Incident and recovery", timeline: [["TRIAGE", "Open the incident, establish impact and identify the accountable owner."], ["PRESERVE", "Retain audit, deployment, flow-run, platform, integration and identity evidence."], ["RECOVER", "Use the rehearsed restore, redeploy, forward-fix, replay, reconciliation or compensation path."], ["AUTHORISE", "Obtain owner oversight before replaying or compensating business transactions."], ["LEARN", "Complete review and update controls, tests, monitoring and runbooks."]] },
      { h: "Operations record", table: [["Date", "Activity", "Reviewer", "Finding / ticket", "Decision", "Due"], ["", "", "", "", "", ""], ["", "", "", "", "", ""]] },
    ],
  },
  {
    file: "09-Architecture-Decision-Record-Template.docx", code: "PP-TPL-001", title: "Architecture Decision\nRecord Template",
    strapline: "A durable record of context, options, evidence, trade-offs and consequences",
    owner: "Solution Technical Owner", approver: "Architecture Authority", review: "Per decision and material change",
    sections: [
      { h: "Decision identification", table: [["Field", "Entry"], ["ADR ID", ""], ["Decision title", ""], ["Status", "Proposed / Accepted / Superseded / Rejected"], ["Owner", ""], ["Approvers", ""], ["Decision date", ""], ["Review trigger / date", ""]] },
      { h: "Context and requirements", prompts: ["Describe the business problem, users, criticality, data classification, expected scale, regions, dependencies and constraints.", "Separate verified facts from assumptions and mark UNKNOWN, CONFLICTED, INF and VOLATILE VALUE evidence.", "State measurable security, availability, recovery, performance, operability, cost and delivery requirements."] },
      { h: "Options considered", table: [["Option", "Benefits", "Risks / costs", "Evidence", "Outcome"], ["Power Platform native", "", "", "", ""], ["Hybrid", "", "", "", ""], ["Custom / alternative", "", "", "", ""]] },
      { h: "Decision", prompts: ["State the selected option and why it best satisfies the requirements.", "Record environment topology, solution boundaries, data ownership, integrations, identities and deployment model.", "Identify irreversible choices and decisions requiring revalidation before implementation or commitment."] },
      { h: "Consequences and controls", prompts: ["Describe positive and negative consequences, licences, support obligations, limits and imported external-estate governance.", "List mandatory controls, tests, monitoring, recovery, reconciliation and required evidence.", "Record approved exception IDs and expiry dates."] },
      { h: "Validation and review", prompts: ["Define proof-of-concept, functional, security, performance, recovery and operational acceptance criteria.", "Set review triggers: requirement change, platform change, incident, scale threshold, renewal or scheduled date.", "Link superseding ADRs without deleting this historical decision."] },
    ],
  },
  {
    file: "10-Application-Architecture-Standard.docx", code: "PP-STD-004", title: "Application Architecture\nStandard",
    strapline: "Fit-for-purpose application selection, design boundaries and platform-exit criteria",
    owner: "Power Platform Application Architecture Lead", approver: "Architecture Review Board", review: "Every six months and after material platform change",
    sections: [
      { h: "Architecture decision principles", callout: { label: "SELECTION PRINCIPLE", text: "Application type is selected from verified requirements and constraints—not maker familiarity, licence availability in a development tenant or visual preference." }, rules: [["MUST", "Teams evaluate configure, buy and first-party capabilities before creating a new application."], ["MUST", "The architecture decision records users, personas, data, experience, identity, device, offline, accessibility, localisation, scale, ALM, support and cost requirements."], ["MUST", "The least complex architecture that satisfies the verified requirements is selected."], ["MUST", "Moving to PCF, code apps, hybrid Azure or custom development has named professional-development and operational ownership."], ["MUST", "Unknown, conflicted or volatile capability assumptions are prototyped or retained as explicit decision risks."]] },
      { h: "Application-type selection matrix", table: [["Architecture", "Strong fit", "Review trigger / poor fit"], ["Configure / buy", "Requirement met by M365, Dynamics 365 or approved product", "Material gaps, lock-in or unacceptable lifecycle cost"], ["Canvas app", "Task-focused internal experience; few personas; connector-led data", "Divergent personas, complex relational process, brand-critical or large mutable UI"], ["Model-driven", "Dataverse-centric, data-dense, process-driven work", "Consumer-grade branding, device-heavy capture or non-Dataverse system of record"], ["Model-driven + custom pages", "Structured backbone with a bounded number of bespoke screens", "State-heavy, offline or device-capability experience"], ["Power Pages", "Authenticated external users over Dataverse", "Non-Dataverse system of record, bespoke API platform, offline or strict server control"], ["Code app", "Bespoke governed SPA for internal or B2B users", "Anonymous use, offline, native mobile or unsupported network restrictions"], ["Teams-hosted", "Bounded team-scoped productivity", "Enterprise scale, APIs, plug-ins, model-driven or offline needs"], ["Hybrid Azure", "Compute, integration or server logic beyond low-code limits", "No owner for the second security, ALM, monitoring and cost model"], ["Custom application", "Consumer UX, public API, custom sync, hard SLA or uneconomic licensing", "Commodity process readily served by governed platform capability"]] },
      { h: "Decision ladder", timeline: [["0  CONFIGURE / BUY", "Use an existing first-party or approved product when it meets the requirement."], ["1  CANVAS / MODEL-DRIVEN", "Choose the native application type that fits experience and data shape."], ["2  COMPONENT LIBRARY", "Standardise repeated canvas interaction and visual patterns."], ["3  PCF", "Introduce code-level controls only for a justified capability or UX gap."], ["4  CODE APP", "Use a pro-code SPA within the platform connector and governance model."], ["5  HYBRID", "Add governed Azure or enterprise services for bounded seams."], ["6  CUSTOM", "Exit the platform when product, scale, UX, API, offline or economics require it."]] },
      { h: "Canvas application standard", rules: [["SHOULD", "Canvas apps remain task-focused, with a bounded persona and screen model."], ["MUST", "Responsive behaviour is deliberately designed and tested for each supported form factor."], ["MUST", "Large or divergent experiences are partitioned using documented application or navigation boundaries."], ["MUST", "Named formulas, StartScreen and maintainable functions are preferred over monolithic initialisation logic."], ["MUST NOT", "Client-side visibility or role branching is treated as data authorisation."], ["MUST", "Data access avoids non-delegable queries and repeated per-row calls; representative performance is measured."], ["MUST", "Concurrent contribution follows the approved isolation and source-control model."]] },
      { h: "Model-driven and custom-page standard", rules: [["SHOULD", "Model-driven apps are used for Dataverse-centric, record-oriented and process-driven work."], ["MUST", "Persona segmentation uses security roles, app modules and platform security—not cosmetic navigation alone."], ["MUST", "Custom pages are limited to justified bespoke interactions and assessed against documented page, connector, navigation and offline constraints."], ["MUST", "Form scripts, controls, tabs and related data are reviewed for performance impact."], ["MUST", "Business process flows guide stages but do not substitute for server-side business logic or security."]] },
      { h: "External applications and Power Pages", callout: { label: "EXTERNAL BOUNDARY", text: "Any internet-facing or external-user application requires explicit identity, licensing, data-permission, abuse, capacity and operational review." }, rules: [["MUST", "Power Pages is used as a Dataverse-fronted external channel only when its data, caching, identity and lifecycle model fits."], ["MUST", "Table permissions and web roles enforce least privilege; anonymous access is explicitly justified and tested."], ["MUST", "Open registration, site visibility and public data exposure are reviewed before launch and after material change."], ["MUST", "Cache behaviour and freshness requirements are validated for each business-critical journey."], ["MUST", "A custom web architecture is evaluated when the system of record is outside Dataverse, a public API is required, or server/caching control is material."]] },
      { h: "Mobile, device and offline", rules: [["MUST", "Supported devices, browser/player context and required hardware capabilities are decided before application type."], ["MUST", "Offline requirements define data scope, conflict behaviour, sync timing, error recovery and security."], ["MUST", "Offline capability is proven with the selected application type and real integration dependencies."], ["MUST", "Wrap is assessed for audience, distribution, signing, Intune, update cadence and documented feature exclusions."], ["MUST NOT", "Push notification, sensor or offline capabilities are assumed from generic mobile support."]] },
      { h: "Reuse and extensibility", rules: [["SHOULD", "A governed design system and component libraries provide reusable canvas patterns."], ["MUST", "Library update ownership and consumer adoption are defined because updates are not automatically propagated."], ["MUST", "Allow-customisation decisions recognise that local changes create a permanent fork."], ["MUST", "PCF controls have code ownership, secure-development practices, dependency maintenance, accessibility testing and release support."], ["MUST", "External calls from extensibility components undergo connector, licensing, security and data-flow review."]] },
      { h: "Quality attributes", table: [["Attribute", "Mandatory architecture evidence"], ["Security", "Server-side authorisation, identity, data permissions and trust boundaries"], ["Accessibility", "Applicable standard, supported patterns and test evidence"], ["Localisation", "Languages, translation ownership, formatting and RTL validation where required"], ["Performance", "Representative data, request patterns, latency, concurrency and limits"], ["Reliability", "Failure modes, retry, reconciliation, recovery and user experience"], ["Maintainability", "Component boundaries, formula/code complexity, ownership and change isolation"], ["ALM", "Source, environments, artifact, configuration, testing and deployment path"], ["Operations", "Telemetry, support model, service dependencies and lifecycle obligations"]] },
      { h: "Architecture review triggers", bullets: ["External or anonymous audience; new identity provider; public exposure or material data-permission change.", "Offline, native-device capability, branded mobile distribution or push notification requirement.", "Multiple materially different personas, rapidly growing screen/form complexity or more than one concurrent maker.", "PCF, code app, custom connector, HTTP endpoint, gateway, Azure component or custom application.", "Material scale, latency, availability, recovery, regulatory, residency or accessibility requirement.", "New premium licensing exposure, external capacity model or a material change in lifecycle cost.", "Reliance on a preview, recently changed, undocumented or otherwise volatile platform capability."] },
      { h: "Architecture acceptance checklist", table: [["Gate", "Required outcome"], ["Fit", "Selected application type satisfies verified requirements without violating a documented boundary"], ["Security", "Identity, authorisation, data access and external exposure approved"], ["Experience", "Personas, responsiveness, accessibility, localisation and device context validated"], ["Engineering", "Composition, reuse, dependencies, testability and maintainability accepted"], ["Performance", "Limits reviewed and material workloads measured"], ["Lifecycle", "Source control, deployment, ownership, monitoring, support and recovery defined"], ["Economics", "Licensing, capacity and external-estate operating costs accepted"], ["Evidence", "ADR links decisions, assumptions, prototypes, exceptions and revalidation triggers"]] },
    ],
  },
];

function run(text, options = {}) { return new TextRun({ text, font: "Aptos", color: C.ink, size: 20, ...options }); }
function p(text, options = {}) { return new Paragraph({ spacing: { after: 130, line: 290 }, ...options, children: [run(text, options.run || {})] }); }
function label(text) { return new Paragraph({ spacing: { before: 100, after: 70 }, children: [run(text.toUpperCase(), { bold: true, color: C.blue, size: 17, characterSpacing: 80 })] }); }
function heading(text) { return new Paragraph({ heading: HeadingLevel.HEADING_1, keepNext: true, children: [run(text, { bold: true, color: C.navy, size: 29 })] }); }
function bullet(text, numbered = false) { return new Paragraph({ numbering: { reference: numbered ? "numbered" : "bullets", level: 0 }, spacing: { after: 105, line: 280 }, children: [run(text)] }); }
function cell(text, { header = false, width, shade, size = 18 } = {}) {
  return new TableCell({ width: width ? { size: width, type: WidthType.PERCENTAGE } : undefined, verticalAlign: VerticalAlign.CENTER,
    shading: { fill: shade || (header ? C.navy : C.white), type: ShadingType.CLEAR },
    margins: { top: 110, bottom: 110, left: 125, right: 125 },
    children: [new Paragraph({ spacing: { after: 0 }, children: [run(text ?? "", { bold: header, color: header ? C.white : C.ink, size })] })],
  });
}
function table(rows, widths) {
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, columnWidths: widths,
    borders: { top: { style: BorderStyle.SINGLE, color: C.line, size: 5 }, bottom: { style: BorderStyle.SINGLE, color: C.line, size: 5 }, left: { style: BorderStyle.SINGLE, color: C.line, size: 5 }, right: { style: BorderStyle.SINGLE, color: C.line, size: 5 }, insideHorizontal: { style: BorderStyle.SINGLE, color: C.line, size: 4 }, insideVertical: { style: BorderStyle.SINGLE, color: C.line, size: 4 } },
    rows: rows.map((r, ri) => new TableRow({ cantSplit: true, tableHeader: ri === 0, children: r.map((v, ci) => cell(v, { header: ri === 0, width: widths?.[ci], shade: ri > 0 && ri % 2 === 0 ? C.mist : undefined })) })),
  });
}
function spacer(n = 90) { return new Paragraph({ spacing: { after: n }, children: [] }); }
function callout(data) {
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.SINGLE, color: C.cyan, size: 22 }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } }, rows: [new TableRow({ children: [new TableCell({ shading: { fill: C.pale, type: ShadingType.CLEAR }, margins: { top: 160, bottom: 160, left: 190, right: 190 }, children: [label(data.label), p(data.text, { run: { bold: true, color: C.navy, size: 21 } })] })] })] });
}
function ruleTable(rules) {
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.SINGLE, color: C.line, size: 4 }, insideVertical: { style: BorderStyle.NONE } },
    rows: rules.map(([kind, text]) => new TableRow({ cantSplit: true, children: [new TableCell({ width: { size: 18, type: WidthType.PERCENTAGE }, margins: { top: 115, bottom: 115, left: 0, right: 120 }, children: [new Paragraph({ children: [run(kind, { bold: true, color: kind.includes("NOT") ? C.red : kind === "SHOULD" ? C.orange : C.blue, size: 16, characterSpacing: 50 })] })] }), new TableCell({ width: { size: 82, type: WidthType.PERCENTAGE }, margins: { top: 105, bottom: 105, left: 0, right: 0 }, children: [p(text)] })] })) });
}
function cards(items) {
  const rows = [];
  for (let i = 0; i < items.length; i += 2) rows.push(new TableRow({ cantSplit: true, children: items.slice(i, i + 2).map(([title, text]) => new TableCell({ width: { size: 50, type: WidthType.PERCENTAGE }, shading: { fill: C.mist, type: ShadingType.CLEAR }, margins: { top: 170, bottom: 170, left: 170, right: 170 }, children: [label(title), p(text)] })).concat(items.length - i === 1 ? [cell("")] : []) }));
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, borders: { top: { style: BorderStyle.SINGLE, color: C.white, size: 10 }, bottom: { style: BorderStyle.SINGLE, color: C.white, size: 10 }, left: { style: BorderStyle.SINGLE, color: C.white, size: 10 }, right: { style: BorderStyle.SINGLE, color: C.white, size: 10 }, insideHorizontal: { style: BorderStyle.SINGLE, color: C.white, size: 10 }, insideVertical: { style: BorderStyle.SINGLE, color: C.white, size: 10 } }, rows });
}
function timeline(items) {
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } }, rows: items.map(([step, text], i) => new TableRow({ cantSplit: true, children: [new TableCell({ width: { size: 22, type: WidthType.PERCENTAGE }, shading: { fill: i % 2 ? C.blue : C.navy, type: ShadingType.CLEAR }, verticalAlign: VerticalAlign.CENTER, margins: { top: 120, bottom: 120, left: 120, right: 120 }, children: [new Paragraph({ children: [run(step, { bold: true, color: C.white, size: 17 })] })] }), new TableCell({ width: { size: 78, type: WidthType.PERCENTAGE }, shading: { fill: C.mist, type: ShadingType.CLEAR }, margins: { top: 120, bottom: 120, left: 160, right: 130 }, children: [p(text)] })] })) });
}
function prompt(text) {
  return new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, borders: { top: { style: BorderStyle.SINGLE, color: C.line, size: 4 }, bottom: { style: BorderStyle.SINGLE, color: C.line, size: 4 }, left: { style: BorderStyle.SINGLE, color: C.line, size: 4 }, right: { style: BorderStyle.SINGLE, color: C.line, size: 4 }, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } }, rows: [new TableRow({ children: [new TableCell({ margins: { top: 130, bottom: 360, left: 140, right: 140 }, children: [p(text, { run: { italic: true, color: C.slate } })] })] })] });
}
function cover(d) {
  const parts = d.title.split("\n");
  return [
    new Paragraph({ spacing: { before: 300, after: 0 }, children: [new TextRun({ text: "AISA  /  POWER PLATFORM", font: "Aptos Display", bold: true, color: C.cyan, size: 18, characterSpacing: 180 })] }),
    new Paragraph({ spacing: { before: 900, after: 40 }, children: [new TextRun({ text: parts[0], font: "Aptos Display", bold: true, color: C.navy, size: 56 })] }),
    new Paragraph({ spacing: { after: 280 }, children: [new TextRun({ text: parts[1] || "", font: "Aptos Display", bold: true, color: C.blue, size: 56 })] }),
    new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, color: C.cyan, size: 20, space: 1 } }, spacing: { after: 260 }, children: [] }),
    p(d.strapline, { run: { color: C.slate, size: 25 } }), spacer(700),
    table([["DOCUMENT", d.code], ["STATUS", "Draft for organisational approval"], ["VERSION", VERSION], ["EFFECTIVE", EFFECTIVE_DATE], ["OWNER", d.owner], ["APPROVER", d.approver], ["REVIEW", d.review]], [26, 74]),
    spacer(160), callout({ label: "CONTROLLED DOCUMENT", text: "Review named authorities, risk thresholds, service levels, retention requirements and volatile platform behaviour before approval." }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}
function documentStatus() {
  return [heading("How to use this document"), p("This document is a draft governance instrument derived from the canonical Power Platform evidence set. It becomes binding only after approval through the organisation’s document-control process."),
    table([["Term", "Interpretation"], ["MUST / MUST NOT", "Mandatory requirement"], ["SHOULD / SHOULD NOT", "Expected; deviation requires recorded justification"], ["MAY", "Optional within the stated boundaries"]], [28, 72]), spacer(),
    callout({ label: "EVIDENCE HANDLING", text: "UNKNOWN, CONFLICTED, INF and VOLATILE VALUE evidence must retain its canonical meaning and must not be silently converted into a fixed rule." })];
}
function renderSection(s) {
  const out = [spacer(80), heading(s.h)];
  if (s.lead) out.push(p(s.lead, { run: { color: C.slate, size: 22 } }));
  if (s.callout) out.push(callout(s.callout), spacer());
  if (s.bullets) s.bullets.forEach(x => out.push(bullet(x, s.numbered)));
  if (s.rules) out.push(ruleTable(s.rules));
  if (s.table) out.push(table(s.table));
  if (s.controls) out.push(table([["ID", "Domain", "Mandatory requirement", "Evidence"], ...s.controls], [12, 18, 46, 24]));
  if (s.cards) out.push(cards(s.cards));
  if (s.timeline) out.push(timeline(s.timeline));
  if (s.prompts) s.prompts.forEach(x => { out.push(prompt(x)); out.push(spacer(55)); });
  return out;
}
function evidenceAndApproval(d) {
  return [spacer(120), heading("Evidence basis"), p("The policy wording synthesises the following internal research artifacts. References are repository-relative; source status and reservations remain governed by the canonical manifest.", { run: { color: C.slate } }), ...evidence.map(x => bullet(x)),
    spacer(120), heading("Approval record"), table([["Role", "Name", "Decision", "Date"], ["Document owner", "", "", ""], ["Security / architecture reviewer", "", "", ""], ["Approver", "", "", ""]], [34, 26, 22, 18])];
}
function header(d) {
  return new Header({ children: [new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, borders: { top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.SINGLE, color: C.line, size: 4 }, left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE }, insideHorizontal: { style: BorderStyle.NONE }, insideVertical: { style: BorderStyle.NONE } }, rows: [new TableRow({ children: [new TableCell({ width: { size: 65, type: WidthType.PERCENTAGE }, margins: { bottom: 70 }, children: [new Paragraph({ children: [run("AISA  /  POWER PLATFORM", { bold: true, color: C.blue, size: 15, characterSpacing: 100 })] })] }), new TableCell({ width: { size: 35, type: WidthType.PERCENTAGE }, margins: { bottom: 70 }, children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run(d.code, { bold: true, color: C.slate, size: 15 })] })] })] })] })] });
}
function footer(d) {
  return new Footer({ children: [new Paragraph({ border: { top: { style: BorderStyle.SINGLE, color: C.line, size: 4, space: 6 } }, children: [run(`Draft  |  v${VERSION}  |  ${d.owner}`, { color: C.slate, size: 15 }), new TextRun({ text: "                                             ", size: 15 }), run("Page ", { color: C.slate, size: 15 }), new TextRun({ children: [PageNumber.CURRENT], color: C.slate, size: 15 }), run(" of ", { color: C.slate, size: 15 }), new TextRun({ children: [PageNumber.TOTAL_PAGES], color: C.slate, size: 15 })] })] });
}
async function build(d) {
  const children = [...cover(d), ...documentStatus(), ...d.sections.flatMap(renderSection), ...evidenceAndApproval(d)];
  const doc = new Document({
    creator: "AISA Power Platform Governance", title: d.title.replace("\n", " "), subject: d.strapline,
    description: `${d.code} - generated governance document`,
    styles: { default: { document: { run: { font: "Aptos", size: 20, color: C.ink }, paragraph: { spacing: { after: 120, line: 290 } } } } },
    numbering: { config: [{ reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "-", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 250 } } } }] }, { reference: "numbered", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 500, hanging: 250 } } } }] }] },
    sections: [{ properties: { page: { margin: { top: 1100, right: 1100, bottom: 1050, left: 1100 }, size: { width: 11906, height: 16838 } } }, headers: { default: header(d) }, footers: { default: footer(d) }, children }],
  });
  fs.writeFileSync(path.join(OUT, d.file), await Packer.toBuffer(doc));
}

(async () => {
  for (const d of docs) await build(d);
  console.log(`Generated ${docs.length} production-grade Word documents in ${OUT}`);
})().catch(err => { console.error(err); process.exit(1); });
