# Operability and support — who notices, who acts, and what they bought

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *What does running this design require — which roles, which execution identities, which alert
  destinations, which recovery procedures — and what does that cost?*
- *What does this criticality class change in the architecture, not in the ways of working?*
- *Is this recovery objective evidenced, or asserted?*
- *Who diagnoses a production failure, with what evidence, and what had to be bought for that evidence to exist?*

This file states **what must be true, and who must exist, for a design to be run in production — and which
of those requirements change the architecture rather than the runbook**. It does not decide which option
wins — that belongs to the decision model (`decision-tree.md` S4–S6).

---

## 1. What this is for · `decision-grade`

The platform operates **itself** well: zone redundancy in the production environment class, continuous
platform backups, automatic patching, and a service-health surface that needs nothing bought or enabled.

The **solution** is not operated at all unless someone decides to operate it. There is no default owner, no
default monitoring, no default alert and no default runbook. Every operational capability below has to be
deliberately turned on, and most of them sit behind an environment class whose licence footprint the maker
does not control.

So the operational question is never *"does it have monitoring?"* It is:

> **Who will notice, who will act, with what evidence, and what have they bought that lets them?**

Four words in that sentence are architectural inputs, not process inputs. Criticality decided late is
rework: it changes artefact structure, ownership identity, environment topology, region strategy and the
licence footprint of an entire environment population.

## 2. When it becomes material · `decision-grade`

- A requirement mentions availability, uptime, recovery, an objective in hours, or "24×7".
- A requirement mentions an audit trail, or reconstructing what happened N months ago.
- The design crosses a service boundary — another platform, an external estate, a self-hosted component.
- The sponsor cannot name an application owner, a first line, or an on-call arrangement.
- The design introduces any component the platform does not operate: a gateway host, a broker, a worker,
  an API tier, a replication pipeline.
- The workload is expected to outlive its maker.

## 3. The four operational maturity classes — and what each changes in the architecture · `decision-grade`

The vendor publishes the distinction as a two-column contrast between a *productivity* workload (built
ad-hoc, built by one, no tests, **development in production**, users monitor quality, short lifecycle) and
a *mission-critical* workload (built to last, built and maintained by a team, automated tests, exercises
lifecycle management, monitored to improve, long lifecycle). The four-class extension below, and
specifically the architecture column, is **supported synthesis over that contrast plus the documented
capability gates — not a vendor-published maturity model.**

| Class | Who notices · who acts · with what evidence | What changes **in the architecture** | What they had to buy |
|---|---|---|---|
| **Simple departmental** | Users notice and tell the maker; the maker acts; evidence is the artefact's own run history | **Nothing.** A shared or team environment, non-solution artefacts, no telemetry. This is a legitimate class, and over-engineering it is a real cost | Nothing beyond the base entitlement |
| **Business-critical** | An accountable **role** notices via an alert; that role acts; evidence is exported telemetry | **Solution-aware artefacts** (the precondition for backup coverage, capacity-licensed ownership, automation-centre visibility and pipeline deployment); **ownership by a service principal or a capacity-licensed identity** rather than a person; telemetry export, which requires the **managed-environment** class; an environment topology with development separated from production | Premium entitlement for the users of the managed environment; telemetry ingestion and retention |
| **Enterprise** | A platform team notices via enterprise monitoring; a change process acts; evidence is correlated across services | All of the above, plus an **explicit correlation identifier generated and propagated across every service seam**; auditing enabled as a store separate from diagnostics; **managed environments throughout the pipeline**, not only in production; data-loss-prevention and network policy, which are themselves managed-environment features | The above, plus audit log capacity — which no licence provides — and premium entitlement across every pipeline stage |
| **Mission-critical** | On-call notices; incident command acts; evidence is a health model with per-flow states | All of the above, plus **cross-region replication** (production class + managed environment + doubled storage, and it **degrades high-volume, highly parallel and latency-sensitive automation throughput**); **dependency-level failure-mode analysis**, because the platform's own resilience says nothing about the systems on the path; **documented and drilled runbooks** | The above, plus a premium support plan and the standing cost of drills |

**The load-bearing consequence.** Moving up a class is not a process upgrade. It changes the licence
footprint of every user in the environment, the artefact structure, the environment topology and the region
strategy. That is why criticality is established before the design is committed, not after the build.

## 4. Operational ownership — and what "accepted" means as evidence · `decision-grade`

Ownership here is not a metadata field. It is **runtime-significant**: the owning identity's plan sets the
artefact's throughput profile, and when the owner leaves the organisation the profile reverts to the lowest
one. Inactivity, sustained error and sustained throttling each carry an automatic disablement countdown,
and the warning is delivered by email to an individual mailbox — including a leaver's.

> Documented reading (the over-limit and inactivity disablement countdowns) · read 2026-09-04 · re-verify: VS-09 (design time)

Three ownership roles are genuinely distinct, and collapsing them is the commonest omission:

| Role | The question it answers | What it must hold |
|---|---|---|
| **Business owner** | *Does this process still matter, and do we accept this risk?* | Authority to accept risk, approve change, authorise retirement |
| **Application owner** | *Is this solution healthy, and what changed?* | Receives alerts and disablement notices at a **shared** destination; holds edit privileges on the maker monitoring surfaces; understands failover and failback |
| **Platform / operations owner** | *Is it the platform or us, and what do I do now?* | Environment-wide read access **pre-granted**, administrative rights, the support-plan relationship, the tenant capacity pool |

In a departmental solution the first two are usually the same person. In an enterprise solution they must
not be.

**What an evidenced operating model is.** Not a name in a document — three things the **design** states,
each of them checkable:

1. **The role and the identity it acts as**, with the permission that identity holds. "The platform team"
   in the abstract is not a role; `Role Operações` with environment-wide read pre-granted is.
2. **The authority the role carries** — that it can accept the risk, authorise the change, or run the
   recovery it is assigned. Authority is a permission, not a rank.
3. **A destination that already exists and is already shared**, not an intention to create one.

Where the design has not defined the intervening role, that is an **operating-model requirement with a
real cost**, priced with the option — not a documentation gap, and not an availability verdict about the
option (README §6). Where the alert destination is an individual mailbox, the model is **not yet
evidenced**: the platform's own notices are email to individuals, so a leaver silently becomes the incident
channel. That is a technical property of the destination, independent of who holds it.

**Ownership is also an architectural decision with a named outcome**, because the identity is a design
choice: own business-critical automation with a service principal, or assign a capacity licence to the
artefact — and the latter requires the artefact to be solution-aware, which is a day-one build decision.

## 5. Support ownership — and what the vendor's support does not fill · `decision-grade`

The vendor's support scope is narrower than teams assume, and every gap below has to be filled by someone
named:

- **A support plan is a precondition for raising a case at all**, and its tier follows from criticality.
  Advisory, escalation and account-management relationships exist only at the higher plan tiers.
- **End users cannot raise cases.** The documentation states there is no alternative to this. Therefore an
  **internal first line is not optional** — it is a role the design requires in order to be supportable.
- **Root-cause analyses are not produced as part of any support experience**, and requesting one is itself
  grounds for severity downgrade. An organisation that owes its business an RCA after every major incident
  must produce it **itself**, which means it must hold the telemetry that makes an RCA possible — see §6.
- **Performance cases and non-reproducible cases receive a bounded best-effort investment, after which the
  case is closed.** Design-level performance problems are therefore not a support outcome; they are a
  design outcome.

  > The exact per-case effort cap is a published figure that **no volatility row owns**, so it is not
  > carried here. What is carried is the boundary shape: *there is a documented cap, and past it the case
  > closes.*

- **Damaged data is explicitly out of scope.** No vendor path exists for correcting corrupted business data.
- **Preview capabilities sit outside the service commitments**, with reduced-hours, single-language
  break-fix handling. A preview capability on a critical path has no supported failure path.
- **Diagnosis requires the customer's consent**, so the runbook must pre-authorise it or name the person who
  can authorise it during an incident — otherwise consent becomes the first delay of every escalation.

**Support hours are a requirement, not an attribute.** What the business expects when something breaks
outside business hours has to be matched against a plan tier and an internal on-call arrangement. Both are
budget lines derived from the criticality class, and both belong in the option's economics.

The roles the support model must therefore name: first line (mandatory), an internal diagnostic and RCA
capability with the evidence to support it, and a partner or engineering escalation for anything
customised, performance-related or non-reproducible.

## 6. Monitoring — what exists, what is gated, what is lossy · `decision-grade`

**Nothing is on by default.** Every surface below requires a deliberate action, and several require a
tenant-level setting the maker cannot change.

**The one free capability.** Platform service health and known-issue visibility needs nothing bought or
enabled. It belongs in every support model at every class, subscribed to a **shared** mailbox, as the first
triage step in every runbook: *is it the platform, or is it us?*

**The real observability story is telemetry export to an external application-monitoring service** — and it
carries three boundaries that are decision-material:

1. **It requires the managed-environment class.** So "we must be able to diagnose production problems" is
   not a monitoring requirement; it is an **entitlement decision** about every active user of that
   environment, taken in Options.
2. **It is explicitly not lossless.** The vendor states that small losses occur from transient service
   issues. Consequence: exported telemetry **must never be the system of record for anything that has to be
   complete** — an audit trail, a compliance record, a metered or charged quantity, a claim that will be
   defended. The documentation is explicit that audit records must be kept complete and therefore separate
   from diagnostic logs.
3. **It is unavailable in sovereign clouds.** A sovereign-cloud engagement must design its operating model
   without the export path, and say so rather than assume it.

Additional boundaries that shape what a support model can promise:

- The **transactional record of automation is run history**, and it has a bounded retention window. Beyond
  that window, nothing reconstructs what the automation did unless the design wrote the evidence to a
  **business record** as part of the process. That is a functional requirement on the automation, elicited
  in Discovery — *will anyone need to reconstruct this later, and how far back?*
- The **aggregated admin monitoring surface** is not real-time: it aggregates daily, retains its event logs
  and its metrics for different and short windows, reports a **single percentile that is not a tail
  percentile** (so tail latency is invisible and cannot be alerted on), requires a tenant-level analytics
  setting to exist at all, and has **no coverage of the primary managed data store**. Recommendations within
  it require a managed environment.

  > Documented reading (native telemetry and run-history retention windows) · read 2026-09-04 · re-verify: VS-18 (Options, before any observability commitment)

- **Unused resources do not appear** in the monitoring surfaces, so an abandoned artefact is invisible while
  still consuming capacity.
- The **automation diagnostic surface** shows only solution-based automation, requires **ownership** rather
  than co-ownership, lags behind real time, is subject to a configurable retention that may simply have
  elapsed, and shows some artefacts as unnamed to broadly-scoped administrators. Some products have **no
  maker-facing monitoring surface at all**.
- The **compliance activity log** is comprehensive but the documentation explicitly says not to use it for
  real-time monitoring; its latency is measured in hours.
- **Makers and operators see different, partially non-overlapping surfaces.** No single surface answers all
  the questions. A support model must name **which surface each role uses for which question**. A "single
  pane of glass" requirement is satisfied only by the external telemetry sink, which re-imports boundary 1.

**Correlation across service boundaries is the architectural part of monitoring.** The guidance is explicit:
log at service boundaries and include a correlation identifier that flows across them. This is **not
automatic**. The solution must generate or accept an identifier at the first boundary, carry it in message
and API metadata and in the status or audit record, propagate it through every worker and backend call, and
emit it into the telemetry sink. The platform's own correlation-tracing capability is experimental and
limited to one extensibility mechanism, so a multi-hop design that must explain a failed transaction
end-to-end **designs the identifier in**, with its schema, storage, privacy and operational cost.

Both **black-box** and **white-box** monitoring are prescribed, and the black-box half matters here: an
externally-visible availability check is the only route to a customer-facing service-level indicator, and
the platform provides no synthetic monitoring. So an external check is a requirement — and it can meter
itself against the solution if pointed at a page rather than a service endpoint.

## 7. Alerting — what exists, what must be built, what must be staffed · `decision-grade`

Three distinct categories, and conflating them is how a monitoring requirement is under-costed:

| | |
|---|---|
| **Exists** | Service-health notifications. Capacity notifications by administrative email. Disablement warnings by email to the owning individual. All email-based, all to be re-routed to a **shared** destination |
| **Must be built** | Every alert about the solution's own behaviour. Failure and dependency-failure alert rules in the telemetry sink with an action group; anything scoped to an environment or an artefact set needs a custom log query. Deliberate trace events for the errors that matter, because the platform's own unhandled-error surfacing is experimental and not for production use |
| **Must be staffed** | An alert with no rota is a log line. The operational-excellence guidance names the human side explicitly: on-call rotations, incident management, emergency resource access and postmortems. This is the part a low-code delivery model most often skips, because the build was cheap enough that nobody budgeted the operating model |

The ordering is prescribed and inverted from habit: **rate the business flows → analyse each flow's failure
modes → set reliability targets per flow → define what healthy, degraded and unhealthy mean → then choose
instrumentation.** Without a health model, alert thresholds have no basis, monitoring produces noise, and
monitoring that produces noise gets switched off. Threshold setting is explicitly a practice of continuous
improvement, not a one-time configuration.

**Ingestion and retention of logs cost money**, and the vendor states it twice. Observability depth is a
budget decision with a meter behind it, not a switch.

## 8. Backup is not recovery · `decision-grade`

Platform backups are continuous and automatic. That fact is routinely mis-read as "we have a copy", and the
mis-reading is where recovery commitments go wrong.

**The record.** A manual backup is *a timestamp and a label* over the continuous backup — a named restore
point, not an additional copy. It **cannot be downloaded, exported, or kept beyond the retention window**.
So a short, same-region, non-downloadable backup window is a **recovery mechanism, not an archive and not a
legal hold**. A retention or archival requirement is satisfied by a data-retention design, not by the
backup window.

> Documented reading (backup retention windows by environment class) · read 2026-09-04 · re-verify: VS-07 (Options and renewal)
> (**7 days** by default; **28 days** only for a production environment in the managed class; trial
> environments are **not backed up at all**)

**The restore-window reality**, which is what an objective in hours must be tested against:

- Retention is short by default, and the longer window exists only for the **production managed**
  environment class — so extended retention is an entitlement decision.
- The **trial environment class is not backed up at all**.
- Restore **cannot target a production environment directly**; the target's type must be changed first — so
  in practice the restored system may only be reachable **as a new instance**, not as the original one.
- Restore is **same-region only**, and a managed environment restores only to another managed environment,
  with encryption, enterprise and network policies **matching** between source and target.
- Restore requires a documented minimum of **free capacity** and is **blocked entirely by overage**.
- Coverage is limited to artefacts held **in a solution**. A mixed environment restores inconsistently.
- Restore duration is **data-volume-dependent and can exceed a day**, particularly where audit data is
  included — and no measured figure exists anywhere in the baseline.
- A **failed restore disables the target**, with a mandatory wait before retry.

> Documented reading (the backup and restore windows underpinning the recovery objective) · read 2026-09-04 · re-verify: VS-17 (Options, and before any recovery commitment)

**And restore is not a rollback.** What breaks, documented, on the far side of a restore: solution-held
automation is deleted in the target while non-solution automation remains; restored automation is turned
off and must be re-enabled; connection references require **new** connections; custom extensibility
components may need removal and reinstallation; sharing to a broad audience is lost; application
identifiers change, so every saved link and bookmark breaks; the environment returns in administration
mode. None of this is automatic. Each item is a timed, owned step in a recovery runbook or it is an
unplanned outage extension.

## 9. Recovery objectives, drills and disaster recovery · `decision-grade`

**An objective is a commitment, and a commitment needs evidence.** Because restore duration is unmeasured
and data-dependent, an objective expressed in hours is **asserted** until a timed rehearsal has produced a
number for a representative data volume. That rehearsal is the evidence; the published windows are not.

**Cross-region resilience is a customer-operated, opt-in capability**, with the following documented shape:

- It is available only for the production class **and** requires the managed-environment class.
- **Backups are not replicated to the secondary region** unless it is explicitly enabled.
- **No cross-region recovery-time commitment is published.**
- It **doubles storage** consumption, and it **degrades** high-volume, highly parallel and latency-sensitive
  automation throughput — the throughput cost of resilience, and it is measurable before the decision, not
  after. The vendor instructs validating business-critical workloads before enabling it.
- Enabling it is not instantaneous, and **disabling it deletes the replicated data**.
- **Several geographies have no cross-region option at all.**
- **No deployments are possible while running from the secondary region** — which must appear in the
  incident-command assumptions, because a failover freezes the change pipeline.
- Named exclusions on failover: analytical replication links provide no objective during failover; one
  link type is not automatically recovered and needs manual relink; event endpoints stop delivering and
  must be recreated; some conversational and industry services do not fail over at all. **Connectors with
  hard-coded primary-region endpoints must be individually validated** as a specific pre-failover task.

**Drills.** The vendor publishes **no prescriptive test plan**, and states that a drill cannot perfectly
replicate a real regional outage because the primary region stays healthy. So the deliverable is a
**documented, drilled runbook covering the platform and every external integration**, with the role that
owns it and a periodic cadence. Where the organisation cannot commit to drills, the honest position is that
regional resilience is **not evidenced** — the design may still be built; the claim may not be made.

## 10. Incident response · `decision-grade`

What the incident-response capability actually requires, assembled from the constraints above:

1. **A triage order that starts outside the solution** — service health and known issues first, because the
   cheapest possible answer is "it is the platform".
2. **Pre-granted access.** Environment-wide read access and the diagnostic-tool security roles must be in
   place **before** the incident. Owner-scoped visibility on the automation surfaces will otherwise block
   diagnosis at the worst moment, and granting access is itself a change.
3. **Pre-authorised diagnostic consent**, or a named authoriser reachable out of hours.
4. **A route to raise a vendor case**, held by someone who is not an end user.
5. **Two failure surfaces per hop, not one.** Automation failures and transaction-scoped extensibility
   failures land in different views; both are monitored or one class of failure is invisible.
6. **A named degradation plan**, because peak capacity cannot be load-test-proven — the guidance limits
   testing to avoid unintended consequences, so operational confidence comes from production monitoring
   plus a plan, not from a pre-go-live test.
7. **Postmortems as a practice**, since the vendor produces no RCA.

One failure mode deserves naming here: **sustained overload is silent, then terminal.** The design does not
error under sustained pressure — it slows, and then the artefact is disabled after a sustained-breach
countdown. Editing the artefact resets the throttling evidence, so *"we edited it and it is fine now"* is
not a resolution. The alert must be on the **trend**.

## 11. Dependency ownership — platform resilience says nothing about the path · `decision-grade`

The vendor's commitments stop at the platform boundary, and it says so. A service-level percentage for a
platform service is **not** the solution's availability, and a recovery objective is not an uptime figure.

- **The weakest dependency governs the flow's real objective.** Availability must be stated **per business
  flow, across dependencies**, with the weakest link named — never as a platform figure quoted upward.
- **Percentages may not be multiplied or averaged into a business-flow commitment** without contractual
  scope and dependency modelling. The composite figure is `UNKNOWN` in the baseline, and inventing one is
  the failure this section exists to prevent.
- For each critical flow, record: the dependency with the weakest recovery capability, whether it is covered
  by the platform's own replication at all, and **what the manual recovery step is**.
- **Every dependency on the path needs an owner**, including the ones the customer operates — a gateway
  host, a self-hosted component, a broker, a worker. Introducing any of them converts a
  vendor-operated availability profile into a **customer-operated** one, and that is an operating-model cost
  that belongs in the option rather than in a footnote.
- A **dependency and exclusion inventory** is therefore a deliverable: what is on the path, who owns it,
  what it is committed to, and what is explicitly excluded from failover.

## 12. Deployment ownership — a second supply chain · `decision-grade`

Deployment is an operational responsibility with two properties that change designs.

**It is a load event on production.** Solution import, publishing customisations and bulk security-model
changes are named as intensive database operations to be kept out of business hours; a manual restore point
needs time to become restorable before a risky change. So a release window is an **operational requirement
with a performance basis**. "Frequent releases" plus "no business-hours degradation" is a genuine conflict,
and the resolution is a release calendar, not a configuration setting.

**Its ownership is explicit and it determines the owner of what is deployed.** The deploying identity owns
the deployed objects — the requesting maker for a standard deployment, the delegated identity for a
delegated one. That interacts directly with §4: an unintended deployment identity silently becomes the
runtime owner, with its throughput profile and its leaver risk.

**Governed deployment carries an entitlement precondition.** Every non-development stage of an in-product
pipeline must be a managed environment, which means premium entitlement for that environment's population.
Documented boundaries that shape the design rather than the process: **rollback works only if the setting
was enabled beforehand** — otherwise reverting is a manual export, a version increment and a manual
re-import; one solution per deployment; a single development environment per solution, so there is no
isolated multi-developer model; no cross-tenant deployment; unmanaged customisations are not published
before export; connection references without a value cannot be updated during deployment; and some
analytical artefact types are not carried at all.

> A dated conversion of pipeline target environments to the managed class is a live commitment that changes
> whether adopting in-product lifecycle management is a licence decision. Confirm the current default with
> the platform-owning team before costing that path — tripwire `TW-V1`.

**Cross-boundary deployment is a second supply chain, not a second script.** Where the design includes an
external component, there are two release routes, two artefact lifecycles and a contract between them that
must stay version-compatible. The coordination obligations are: a joint release sequence; a
fix-forward-or-revert strategy that spans both halves; and a tested mitigation for the case where one half
is updated and the other is not. **Connections and connection references are the fragile part of every
deployment and every recovery** — they are not carried by the artefacts, they break on restore, they must be
supplied at deployment time, and they determine both capability and whose entitlement is consumed. They are
configuration items with an inventory: which reference, which mechanism, which identity, which credential
store, who owns it.

**Test fidelity has a documented ceiling.** The guidance to mirror production collides with the fact that
managed-environment behaviour exists only in a managed environment. So some production behaviour is only
testable in a managed test environment, which has an entitlement cost. This tension is unresolved in the
baseline and should be surfaced rather than papered over.

## 13. Skills and pro-code capacity are an availability question · `decision-grade`

Team capability is an explicit architecture criterion, not a staffing preference. The guidance is direct:
choose services the team knows how to use, or **commit to training them before choosing the service**.

The operational form of this is sharper. Where a design includes a component the platform does not
operate — a broker, a worker, an API tier, an in-network gateway, a mediation layer — that component
requires an operating model of its own: the role that intervenes, the identity it runs as, an on-call
route, its own release pipeline and its own monitoring. Where the design has not defined them, that is an
**operating-model requirement with a cost**, carried by the option and priced with it. It is neither an
availability verdict (README §6 reserves those for the decision model) nor a comparative judgement about
the organisation.

What "available" means, and it is a higher bar than a plan:

- **In-house and available now**, or an explicit, funded and dated commitment to acquire the capability —
  not an intention.
- **Named**: who owns the external resources, how the two halves are deployed and monitored together, and
  what the second estate's run cost is. Where those three cannot be named, the honest output is the
  single-estate design plus a tripwire on the metric that would force the move — not a two-estate design
  nobody can operate.
- **Persistent**: a capability that exists for the duration of a delivery engagement and not afterwards is
  a handover problem, and handover from a delivery partner to a customer operations team is **entirely
  undocumented** in the baseline. Treat it as a deliverable to define, not a fact to look up.

The same test applies to the reconciliation pass of any two-copy data design, to dead-letter and replay
ownership in any brokered design, and to the platform team of any governed-boundary design.

## 14. Diagnostic and audit evidence retention · `decision-grade`

Four different retention questions that are routinely treated as one:

| Evidence | Character | Consequence |
|---|---|---|
| **Automation run history** | The transactional record of what the automation did. Bounded, and the boundary is short relative to most audit questions | Beyond the window, the evidence must have been written to a **business record** as part of the process. This is a design requirement, not a monitoring setting |
| **Exported diagnostic telemetry** | Customer-defined retention, correlated, queryable — and **not lossless** | The only route to investigating an incident from a past period. Never the record for anything that must be complete |
| **Data-store auditing** | Complete, and required for compliance. Consumes **log capacity that no licence provides** | A separate store, a separate retention decision and a separate budget. Kept **separate from diagnostics** precisely so that transactions are not dropped |
| **Compliance activity log** | Comprehensive, complete, latency measured in hours | Compliance evidence, explicitly **not** operational alerting |

> Documented reading (audit retention and log-availability windows) · read 2026-09-04 · re-verify: VS-05 (Options, and at any compliance review)
> Documented reading (native audit and diagnostic retention windows) · read 2026-09-04 · re-verify: VS-19 (Options, and at any compliance review)

**The conflict worth surfacing early.** Audit data is **excluded from restore by default**, because
including it materially increases restore duration. So *"the audit trail must be complete through a
recovery"* and *"we must recover fast"* are competing requirements that need an explicit decision, not a
default.

## 15. What must exist before an operational commitment is defensible · `decision-grade`

An operational commitment — an availability figure, a recovery objective, a support-hours promise, a
"business-critical" label — is defensible when the following exist. Absent them, the commitment is
asserted, and the honest artefact is an `Unknown` — with the role or the source that can answer it, and a
date — not a number.

| The commitment | The evidence that makes it defensible |
|---|---|
| *"Someone will notice"* | A named application owner, and an alert destination that is **shared** and already exists |
| *"Someone will act"* | An on-call or escalation arrangement, a first line that is not the end user, and pre-granted environment-wide access |
| *"We can diagnose it"* | Telemetry export actually enabled — therefore the environment class and its entitlement decided — plus a correlation identifier designed into every seam |
| *"We can prove what happened"* | The retention question answered per evidence class (§14), and the beyond-window evidence written into a business record by design |
| *"We can recover in N hours"* | A **timed** restore rehearsal at representative data volume, plus a runbook covering reconnection, re-enablement, re-sharing and re-publication, with per-step owners and elapsed times |
| *"We survive the loss of a region"* | Replication actually enabled, its throughput cost measured on the real workload, region-pinned endpoints audited, external integrations covered, and a **drill that has been run** |
| *"This flow is available X"* | Per-flow failure-mode analysis across dependencies, with the weakest link named — never a platform figure quoted upward, never a product of percentages |
| *"It is supported"* | A support plan at a tier matched to criticality, an internal RCA capability with the telemetry to support it, and an escalation route for customised and performance cases |
| *"We can run the external half"* | The role that operates it and the identity it runs as, its release pipeline, its monitoring, the role authorised to replay or reconcile, and its run cost |
| *"We can deploy safely"* | Rollback capability verified as enabled beforehand, a release calendar, and a connection inventory |
| *"It has a capacity headroom"* | A role accountable for the tenant capacity pool, monitored per meter, treated as a **recoverability** precondition rather than a finance metric |
| *"It will be maintained"* | A role accountable for platform-change and deprecation tracking, with a recurring remediation budget |
| *"It can be retired"* | An explicit retirement stage with an accountable role and a checklist — the platform's own response to abandonment is silent disablement |

## 16. Failure modes · `decision-grade`

> **The unowned artefact.** No accountable owner means the runtime owner is whoever built it. The
> throughput profile follows that identity's plan and reverts on departure; the inactivity, error and
> throttling disablement notices go to that identity's mailbox. Consequence: the outage arrives as a
> silence, and the warning was delivered to someone who left.

> **Monitoring assumed to exist.** Telemetry export needs an environment class; the aggregated surface
> needs a tenant setting; per-application telemetry needs both a tenant setting and a per-application
> configuration item. Nothing is on by default. Consequence: the first production incident is also the
> discovery that there is no evidence, and by then the entitlement decision is a change request.

> **The diagnostic sink treated as the record.** Exported telemetry is not lossless and the transactional
> record expires. Consequence: a question that must be answered completely — an audit finding, a charged
> quantity, a dispute — is answered from an incomplete source, and the gap is invisible until someone
> reconciles.

> **Restore mistaken for rollback.** A restore cannot target production directly, deletes solution-held
> automation in the target, breaks every connection reference, changes application identifiers and returns
> the environment in administration mode. Consequence: the recovery step intended to shorten an outage
> extends it, and the extension is unbudgeted because nobody timed it.

> **The undrilled resilience claim.** Cross-region replication is opt-in, publishes no recovery-time
> commitment, excludes several named dependencies and cannot be perfectly rehearsed. Consequence: a
> commitment exists that no evidence supports, and it is discovered at the only moment it matters.

> **The platform figure quoted upward.** A platform service's availability is presented as the solution's.
> Consequence: the promise omits every system on the path, and the first dependency failure breaks a
> commitment the platform never made.

> **Capacity ignored until it blocks something.** Overage does not slow the application — it disables
> restore, copy, recover and environment creation. Consequence: a finance oversight becomes an
> incident-response failure, at the moment recovery is needed.

> **Governance built on unmaintained tooling.** A widely-deployed community governance toolkit is no longer
> maintained and its issues are no longer reviewed, while being built from the same components subject to
> the continuous deprecation stream. Consequence: the operating model's own foundation is technical debt
> with a migration path, and it must be recorded as such rather than counted as capability.

> **No retirement lifecycle.** The platform silently disables rather than removes; unused artefacts are
> invisible to the monitoring surfaces yet still consume the capacity that gates restore. Consequence: an
> abandoned artefact contributes to the ceiling that blocks the recovery of a live one.

## 17. Consequences elsewhere · `decision-grade`

- **→ governance and environments.** Nearly the whole operational feature set — telemetry export, extended
  backup retention, cross-region replication, in-product pipelines, network and key controls, desktop-flow
  policy — sits behind the **managed-environment** class. Who operates each of those controls is a
  governance question with an accountable role; the environment **type** carries the operational consequences
  (zone redundancy, backup, retention, replication eligibility, pipeline eligibility). See
  `governance/governance-and-environments.md`.
- **→ ALM and release.** Release ownership, the deploying identity becoming the runtime owner, the
  **rollback setting that must be enabled beforehand**, one-solution-per-deployment, the single development
  environment, and connection-reference rebinding all live as lifecycle mechanics in
  `alm/release-and-lifecycle.md`. This file carries only their operational consequences.
- **→ economics.** Support plan tier, telemetry ingestion and retention, audit log capacity that no licence
  provides, doubled storage for replication, non-production environments, and recurring deprecation
  remediation are all separate cost drivers with their own meters and their own affected populations. The
  managed-environment gate converts an operational requirement into an entitlement decision for **every
  active user of the environment**, not only the solution's own users — with a dated enforcement commitment
  (`TW-V3`). See `economics/licensing-and-cost-drivers.md`.
- **→ performance and scale.** Deployment is a performance event; replication degrades automation
  throughput; restore duration is data-volume-dependent; sustained overload is silent then terminal; peak
  capacity cannot be load-test-proven. See `performance/performance-and-scale.md`.
- **→ architecture patterns.** Every composition **imports** an operating model — an intervening role and
  its execution identity, monitoring, an alert destination, a release route, a recovery order and a
  telemetry cost line. What each
  composition imports is stated in `architecture/patterns.md`.
- **→ integration mechanisms.** The correlation identifier that makes cross-boundary diagnosis possible has
  to be generated, propagated and stored by the design; dead-letter, replay and reconciliation ownership
  are per-stream obligations. See `integration/integration-mechanisms.md`.
- **→ data.** Audit mechanics, retention and the storage meters that gate restore are
  `data/store-boundaries.md` and `data/dataverse.md`.
- **→ security.** Advanced controls add operational preconditions of their own — key ownership and
  revocation, network allowlists, privileged identities, and the retention of the evidence they produce.
  See `security/security-controls.md`.

## 18. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Support plan structure and coverage — severity response windows, per-case effort cap, covered hours | `VS-36` |
| Cross-region protection envelope — recovery-point and recovery-time objectives, enablement lead time, and the throughput it degrades | `VS-37` |
| Customer-operated estate currency obligations for any self-hosted component on the path | `VS-28` |
| Backup retention windows by environment class | `VS-07` |
| The backup and restore windows underpinning the recovery objective | `VS-17` |
| Native telemetry retention window | `VS-18` |
| Native audit and diagnostic retention windows | `VS-19` |
| Audit retention and log-availability windows | `VS-05` |
| The over-limit and inactivity disablement countdown | `VS-09` |
| Capacity consumption profile (the headroom that gates restore) | `VC-07` |
| Preview or general-availability state of any capability the operating model relies on | `VC-10` |
| Entitlement fit of the required operational capability set | `VC-05` |
| Pipeline target conversion to the managed class | `TW-V1` |
| Managed-environment licence enforcement across the environment population | `TW-V3` |

**Not established in the baseline** — do not fill from general knowledge:

- **No composite availability percentage** for a business flow across platform services. A platform
  service's own figure exists and is dated; the composite requires contractual scope and dependency
  modelling and is `UNKNOWN`. Do not multiply or average.
- **No measured restore duration** for a representative environment size. The only statement is that it may
  exceed a day. A timed rehearsal is the only evidence.
- **No published cross-region recovery-time commitment**, and **no prescriptive drill plan**.
- **No programmatic capacity alerting** is evidenced beyond periodic administrative email.
- **No project-level view of the shared tenant request pool** — one integration's growth silently consumes
  another's headroom.
- **No guidance on operational handover** from a delivery partner to a customer operations team. This is
  the commonest real-world failure point for partner-delivered solutions and it is undocumented.
- **No independent post-mortem corpus** for this domain, so nothing triangulates the documentation.
- **Retention and query cost of the telemetry sink at realistic volumes** is unpublished; the vendor flags
  the cost without a volume basis.
- **No coverage of the primary managed data store** in the aggregated monitoring surface, and no statement
  of when that will change.

## 19. What not to infer · `decision-grade`

- **"The platform is resilient" is not "the solution is operated."** The first is a vendor property; the
  second is an organisational one that has to be bought, staffed and evidenced.
- **A capability absence is not a verdict.** *"Telemetry export requires the managed-environment class"* is
  domain knowledge. *"Therefore this is unsuitable"* is selection logic and belongs to the decision model.
- **An undefined operating model is a requirement with a cost, never an availability verdict.** That a
  design has not yet named the role that intervenes, the identity it runs as or the alert destination says
  the design is incomplete. It does not rank the organisation, it does not make any other option better,
  and it is not this file's call whether it blocks — that belongs to the decision model (README §6).
- **A documented boundary here is not evidence that another option class performs better.** The operational
  obligations of hosted services, custom-built systems and incumbent platforms are outside this baseline
  entirely; no like-for-like comparison exists. Where the comparison is material,
  `decision-model/outcome-classes.md`'s comparator semantics stand.
- **A published retention or restore window is not a recovery objective.** Objectives are evidenced by a
  timed rehearsal; windows only bound what is possible.
- **A drill is not a proof of a regional outage.** The vendor states a drill cannot perfectly replicate one
  because the primary region stays healthy. It is the best available evidence, not certainty.
- **The four maturity classes are a synthesis, not a vendor-published model.** The two-column contrast they
  extend is vendor-published; the four-class shape and the architecture column are supported synthesis.
- **The support-model role set is a synthesis** over the ownership, tooling and support facts — a checklist
  of what must exist, not a prescribed organisational structure.
- **"Included as an entitlement" is not "free."** The managed-environment *feature* carries no separate
  charge, while every active user of that environment must hold a qualifying licence. Both statements are
  in the documentation and they are consistent at different scopes.
- **Aged guidance is direction, not specifics.** The deployment-window guidance is corroborated in direction
  by current material but its detail predates the current platform. Treat it as a reason to have a release
  window, not as a specification of one.
