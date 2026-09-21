# Release and lifecycle — the four rungs, and what each does not provide

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Which isolation and release rung does this control requirement reach, and what does that rung require?*
- *Can this be reversed — and was the mechanism enabled in time?*
- *Who coordinates a release that crosses the boundary?*
- *What does this lifecycle capability explicitly **not** provide?*

This file states **what each lifecycle rung buys, what it presupposes, and what it does not give you** —
including the capabilities the platform does not have at all. It does not decide which option wins, and it
does not restate the decision model's outcome semantics, stage order or exit classes — those belong to
`decision-tree.md` S4–S6 and its registers.

---

## 1. What this is for · `decision-grade`

Power Platform does not have one lifecycle model; it has **four rungs** that differ in who can operate them,
what they guarantee, and what they presuppose. Almost every lifecycle question is therefore a question about
which rung a requirement reaches — and the requirement that forces a step up is usually **review or team
size**, not automation.

The second thing this file exists to say is what the platform does **not** have, because those absences
change plans more than the features do: **there is no solution rollback**, there is **no supported
first-party low-code functional test framework**, there is **no multi-developer isolation inside one
environment**, and there is **no cross-tenant deployment** in the in-product pipeline mechanism.

## 2. When it becomes material · `decision-grade`

- The artefact must **survive its author** — anything beyond a personal tool.
- **Two or more people** will build at the same time, or on the same artefact.
- Changes must be **reviewed** before they reach a test environment, or traced to a work item.
- Someone other than the maker must **perform the deployment**, or the maker must not hold production rights.
- A **reversibility commitment** has been made, or will be asked for before go-live.
- Configuration differs between environments, or secrets are involved.
- The solution spans **more than one technology boundary** (an external API, a broker, a worker, an
  analytical target).
- The release must be **auditable**, or the workload will be classified business-critical.

## 3. The four rungs · `decision-grade`

| Rung  | Mechanism                                                                                 | What it buys                                                                                                                                                               | Prerequisites                                                                     | What it does **not** provide                                                                                                                                      |
| ----- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **0** | No solutions — build in the default solution, edit in place                               | Nothing                                                                                                                                                                    | None                                                                              | Portability, layering, reversibility, audit, selective promotion                                                                                                  |
| **1** | Manual solution export/import, managed downstream                                         | Layering, portability, a managed production estate                                                                                                                         | Discipline; one deliberate publisher; separate environments                       | Automation, traceability, approvals, artefact integrity, gate enforcement                                                                                         |
| **2** | In-product deployment pipelines                                                           | Automated promotion, **artefact immutability across stages**, connection and environment-variable handling, run history, optional approvals, delegated deployment identity | **Managed** target environments; a host environment; the entitlement that implies | Source control (unless combined with Git), multi-solution deploys, cross-tenant deploys, per-developer isolation, choice of import behaviour, code review or diff |
| **3** | Source-controlled ALM — Dataverse Git integration and/or build tools / repository actions | Version history, branching, pull requests, code review, code-first components, rehydratable environments, full pipeline control, work-item traceability                    | A Git provider; a development environment per maker or branch; pro-dev capability | **Automated functional testing** — no supported first-party low-code framework exists                                                                             |

**Rungs 2 and 3 are not alternatives.** The documented position is Git integration in *developer*
environments and pipelines for *deployment*: builds create the solution artefacts, pipelines deploy them. The
enterprise shape is therefore rung 3 for source plus rung 2 or 3 for deployment — not one or the other.

**The minimum for anything that matters** is a custom solution with a single deliberate publisher, and
managed solutions everywhere except the development environment. Two mechanical reasons, not tidiness:

- **An unmanaged layer defines runtime behaviour.** All unmanaged solutions and ad-hoc customisations share a
  single unmanaged layer that sits above every managed layer, and for all component types except
  model-driven app, form and site map the behaviour is "top level wins". So one ad-hoc production edit
  permanently shadows every future managed update to that component until the layer is explicitly removed.
  This is the mechanism behind environment drift.
- **A managed solution cannot be validated where it was built.** A managed solution cannot be imported into
  the environment that holds its originating unmanaged solution. A test environment is therefore
  *structurally* required, not a recommendation.

**Component-deletion semantics differ by operation**, and this decides how a component leaves production: an
*update* deploys over the previous version without adding a layer and **cannot delete components**; a *patch*
carries only changes and also cannot delete components (and patches are documented as not recommended); an
*upgrade* installs a new layer, deletes all existing patches and the base layer, and **deletes components
that existed but are no longer in the new version** — including anything a well-meaning administrator added
to that solution in the target.

## 4. Solution-awareness is the prerequisite for other capabilities · `decision-grade`

"Put it in a solution" is normally presented as good practice. Mechanically it is the **precondition** for
four independent capabilities:

| Capability | Requires the artefact to be in a solution |
|---|---|
| Backup and restore coverage | Backup and restore operations include only apps and automations that are **in a Dataverse solution** |
| Capacity-licensed ownership of an automation | A dedicated capacity licence can be assigned only to a solution automation |
| The automation monitoring surface | Only runs for solution-based cloud flows appear there |
| Pipeline deployment | Pipelines deploy solutions, and cannot be viewed or run from the default solution |

Consequences that bite later: a non-solution automation's owner **cannot be changed at all**; a per-user
artefact ceiling is worked around by moving artefacts into solutions; and restore treats the two classes
asymmetrically — **solution automations in the target are deleted, non-solution ones remain** — so a mixed
environment restores inconsistently. Solution-awareness is a day-one structural decision driven by the
criticality class, and retrofitting it is rework at exactly the moment the workload became important.

**Solutions carry metadata, not data — and not all metadata.** They contain no business data, and some system
tables cannot be added at all (application user, custom API, organization setting among them). Business units
and teams are not solution components either and must be created and managed in **each** environment; where a
modernised business-unit model is used, the owning-unit values must exist identically in the target or
synchronisation fails on a foreign-key violation. So reference and configuration data, service identities and
the security-model scaffolding all need their own per-environment provisioning step — automated, or it will
be forgotten.

**A solution has a documented maximum artefact size.** No volatility row owns that ceiling, so the figure is
not carried here: what is stable is the boundary shape — **a ceiling exists, and large binary or media
content should not travel inside the solution.** Read the current figure at the decision date and record it
on the engagement's own row.

## 5. Deployment pipelines, and their managed-environment dependency · `decision-grade`

What pipelines genuinely add over manual promotion, and nothing else does:

- **Artefact immutability across stages.** The solution is exported once, when the request is submitted, and
  the *same* artefact passes through the stages in sequential order; the system prevents modification of the
  exported artefact, so a customisation cannot bypass a QA stage or an approval.
- **Prevalidation against the target**, surfacing missing dependencies and other issues before deployment.
- **Configuration handling** for connections, connection references and environment variables.
- **Run history and automatic artefact retention** in the host, plus layer diffs visible in the target.
- **Approvals** through an extension point, and **delegated deployment**.

What they do not do, from the documented limitation set: no cross-tenant deployment; no multi-solution
deployment in one request; no choice of import behaviour (the default is upgrade without overwriting
customisations); no publishing of unmanaged customisations before export; connection references with no value
in either the solution or the target cannot be updated during deployment; one development environment per
solution, so no isolated multi-developer flow; one host per environment; no customisation of the
first-party pipeline app itself; and some analytical component types are unsupported.

**The dependency that changes the economics.** Development environments need not be managed and may run on
the developer plan. The host should be a production environment but need not be managed. **Every other
environment used in a pipeline must be enabled as a managed environment**, with the entitlement obligation
that implies for every active user of those environments.

> Documented reading · read 2026-09-04 · re-verify: TW-V1 (dated commitment — verify the outcome)
> Automatic conversion of pipeline **target** environments to managed environments began **February 2026**.
> Row `TW-V1` owns this subject; whether it completed as announced, and what it did to tenants that had not
> planned for the entitlement impact, is an open question in the baseline.

**Managed Environments themselves — the feature set, the entitlement shape, the affected population and the
dated enforcement milestone (`TW-V3`) — are owned by `governance/governance-and-environments.md`.** Read the
licence chain there; this file only records that adopting in-product ALM triggers it. The tension is real and
documented: the mechanism positioned as approachable, maker-usable ALM is the one with the population-wide
entitlement prerequisite. State it in the option's cost rather than discovering it afterwards.

**Delegated deployment is the platform's separation-of-duties mechanism**, and its shape matters:

- The stage deploys as the delegate — a service principal or the stage owner — **instead of the requesting
  maker**.
- The delegate needs the pipeline-administrator role in the host and **System Administrator in each target**,
  because lower-privileged roles cannot deploy plug-ins and other code components. So the control achieved is
  *"no human holds standing production rights"*, **not** *"nothing holds production rights"*.
- All delegated deployments are pending until approved; the approval path is an extension flow using the
  delegate's own connection.
- Sharing is assigned at **first** deployment only and cannot be updated on later versions; individual-user
  sharing is not currently supported; minimum privileges are assigned automatically. Approvers are explicitly
  responsible for reviewing the sharing and security-role information, because approval causes permissions to
  be assigned under the deploying identity.
- Stage-owner delegation cannot deploy solutions containing connection references for OAuth connections.

**Deployment creates ownership, and ownership creates the runtime identity.** Deployed objects are owned by
the **deploying identity** — the requesting maker in a standard deployment, the delegate in a delegated one.
Automations run under their connection owner. So without delegated deployment, production automations end up
owned by whoever pressed Deploy, which is precisely the condition that later produces the ownerless-artefact
backlog that governance detects but cannot repair.

## 6. Source-controlled ALM, and where version control belongs · `decision-grade`

Native Dataverse Git integration synchronises solutions and solution objects across one or more environments
using a supported Git provider. The documented placement is unambiguous: **use it with developer
environments, not in test or production environments; use builds to create artefacts and pipelines to
deploy.** Solutions in source control come from *unmanaged* solutions in a maker's environment; managed
solutions are **built** from source control and deployed downstream.

What it is the mechanism for:

- Source control as the single source of truth, with version history, code review and static analysis.
- **Short-lived development environments** that can be rehydrated from source control — which is what makes
  environment-per-maker or environment-per-branch practical.
- Fusion teams building independently in separate environments and collaborating through a shared repository.
- Recovery to a previous state or version *of the source*.
- A human-readable, de-duplicated file format.

Its documented edges: committing built artefacts back into a maker environment and then committing them
produces **two copies of the object in source control** and is explicitly not recommended — code-first objects
should travel through a solution build process. For the canvas app artefact specifically, in-editor Git
version control **was removed and is no longer supported**, commits happen only on publish, the YAML source
cannot be edited directly when the app contains code components, and only one maker can edit one app or
custom page at a time. The practical maturity of native solution-level Git integration *for canvas apps* is
**not established** in the baseline.

**Multi-developer isolation exists only at rung 3.** Working in an unmanaged solution provides no isolation —
every modification is applied directly to the environment regardless of which solution is being edited —
canvas co-authoring was removed, and the pipeline mechanism uses a single development environment per
solution. Two makers on one artefact therefore means environment-per-developer plus Git; anything less is a
serialisation agreement enforced by humans, and the guidance is explicit that simultaneous changes to complex
components should be avoided.

**Build-tool and repository-action pipelines** (rung 3 for deployment) cover what the in-product mechanism
does not: cross-tenant delivery, granular control, code-first components, and work-item traceability. Their
first design decision is the **deployment identity**: workload-identity federation is the recommended
connection type, service principal with a client secret is supported, and **username/password service
connections do not support accounts requiring multi-factor authentication** — which most enterprise tenants
enforce. The generated service principal defaults to System Administrator, and its secret is retrievable
once. Task versions cannot be mixed. Both require a Dataverse environment with a database.

**Solution organisation and development-environment count are one coupled decision**, driven by team size,
release independence and modularity. Three documented strategies exist: a single solution (small to medium
scope, modularisation unlikely — with the documented downside that makers in one development environment risk
overwriting each other); multiple solutions in one development environment (only for genuinely independent
functional areas that share no components — with the documented deadlock where each solution depends on the
other); and multiple solutions with **dedicated** development environments plus a base-managed-solution
layering (large scope, multiple developers or partners, strict governance and CI/CD — with higher
infrastructure and maintenance overhead). Four hard rules cut across all three: do not include the same
unmanaged component in more than one solution; **have only one solution that includes all your tables**; use
only one publisher; and avoid dependencies between solutions. The documented failure is quiet — a solution
imports successfully and the automation inside it does not work, because a dependency on a custom column was
not recognised.

## 7. Configuration binding — environment variables and connection references · `decision-grade`

These are the sanctioned mechanism for per-environment configuration, and both are ALM design objects rather
than implementation details.

**Environment variables.** Definition and value are separate records, and a value cannot exist without a
definition. The guidance on whether the value ships in the solution is verbatim: **no** — values are supplied
for the target environment at deployment. Documented edges that matter: value propagation into apps and
automations is **asynchronous and can lag**; there is **no Dataverse-side validation** (validation happens in
the consuming interfaces and components only); custom code must call the API to read a value and no cache is
exposed; a managed-solution variable's value is visible only through the default solution because the value
itself is an unmanaged customisation; the definition table is included in maker and basic roles by default;
list-store variables require display and logical names to match and the underlying internal identifiers may
not match across environments; and two names are reserved and will block saving an automation.

**Environment variables have a documented maximum value length, and updated values have a documented
propagation window.** No volatility row owns either figure, so neither is carried here. The stable part is
the shape: **a length ceiling exists, and propagation is not immediate** — which, together with the absence
of store-side validation, is a live source of "it worked in development" incidents. Read both at the decision
date and record them on the engagement's own row.

**Connection references.** During solution import a connection is provided for each reference so the
consuming automations can be turned on automatically. The asymmetry matters: **automations use connection
references for all connectors; canvas apps use them only for implicitly shared (non-OAuth) connections**, and
a canvas connection reference is associated only at the moment a data source is added. Artefacts added from
outside solutions are not upgraded to use references. Four documented failure modes:

1. **Canvas apps do not recognise connection references on custom connectors.** The documented workaround is
   to edit the app after import to remove and re-add the custom connector connection — and if the app is in a
   managed solution, editing it **creates an unmanaged layer**. The fix therefore breaks the
   production-integrity rule.
2. **Copying an environment breaks connection references for custom connectors**; a new reference must be
   created.
3. **Custom connectors must be imported in a separate solution from their connection references**, before the
   references or the consuming automations.
4. Enabling an automation requires ownership of, or explicit sharing on, every connection; otherwise it fails
   with an authorisation error. Reference ownership cannot be transferred from the modern solutions area.

**Where the workaround would create an unmanaged layer against a mandatory integrity control, the documented
rule is: redesign the seam, use another supported binding approach, or record a governance exception with an
owner and an expiry — do not disable the integrity control silently.** Secrets are a separate concern: they
live in a vault and are consumable by only three component types (automations, agents, custom connectors), so
every target environment needs its own vault permission model and its own variable values.

**Production integrity: block unmanaged customizations.** With it enabled, unmanaged-solution import is
blocked, creation of new solution components is blocked, and unmanaged changes to existing managed components
are blocked. What remains allowed is what makes read-only production support possible: changing environment
variables, enabling and disabling components, assigning ownership and sharing records, removing an unmanaged
layer, creating and exporting unmanaged solutions, reviewing run history, and running an automation to test
it. Two documented caveats: **dataflows are exempt** and will continue creating unmanaged layers even with
the setting on; and there is a **real break-list** of first-party features that fail with the same error while
it is enabled — including resource-scheduling optimisation install/upgrade, automatic record creation, legacy
workflow enable/disable, several field-service capabilities, sales-accelerator configuration,
customer-journey creation and publishing, omnichannel install/upgrade, SLA activation and editing, certain
attachment operations, work-queue items, and **agent publishing**. The vendor's own guidance is to disable the
setting where one of those features is required. That is a control-versus-capability decision to record with
an owner — not a default.

## 8. Reversibility and exit · `decision-grade`

**This is this file's single home for the reversibility concern.**

### 8.1 There is no rollback

There is **no solution rollback**. There are three imperfect recovery paths:

1. **Redeploy a previous solution version** through the pipeline — available **only if the pipeline setting is
   enabled**. If it is disabled, only *higher* solution versions can be deployed, and the documented
   workaround is downloading the artefact, incrementing the version in the solution manifest, and importing
   manually.
2. **Restore a backup** — an environment-level, disruptive operation (§8.2), not a release-level undo.
3. **Fix forward** — constrained by the deletion semantics of §3 (only an upgrade can delete a component) and
   by the pipeline's fixed import behaviour.

**And the emergency path is not a shortcut.** Patches are documented as not recommended, and a pipeline
cannot bypass a stage — so a hotfix is a normal release on a compressed schedule, or an explicitly governed
exception, and the role authorised to grant it. A human approval step is part of the pipeline only where a
requirement in scope puts it there; it is never a default stage.

### 8.2 Restore is not a rollback, and it has documented side effects

Restore constraints: it **cannot target a production environment directly** (the documented route is to
change the type to sandbox, restore, then change back); it must stay **in the same region**; a **managed
environment can be restored only to another managed environment**; customer-managed-key and
private-networking policy state must match; free capacity is required, and being over capacity **blocks
restore entirely**; a backup copy cannot be downloaded for offline use; coverage is limited to apps and
automations **in a solution**; and the operation can take longer than a day depending on data volume,
especially with audit data.

Documented post-restore effects, which is why a restore is a project with a runbook rather than a button:

- **Solution automations in the target are deleted; non-solution ones remain — and restored solution
  automations come back turned off.**
- **Connection references require new connections.**
- Custom connectors must be reviewed and, where needed, deleted and reinstalled.
- Apps shared with the org-wide group are **not** re-shared that way.
- **A canvas app's identifier differs after restore** — so every bookmark and deep link breaks.
- The environment returns in administration mode.

And it crosses boundaries: restoring one environment **rewinds one participant** while external systems,
queues and replicated copies retain later state. The recovery plan therefore needs a post-restore integration
step — pause affected writers, establish the restore time boundary, reconcile, replay or re-seed, validate,
then reopen traffic.

> Documented reading · read 2026-09-04 · re-verify: VS-17 (Options, and before any recovery commitment)
> System backups are continuous; retention is a documented window that differs by environment class, with
> extension available only for production managed environments; a deleted environment is recoverable within a
> documented window. Trial environments are not backed up at all.

### 8.3 Reversibility mechanisms often must be enabled BEFORE they are needed

This is the single most important sentence in this file. Three concrete cases:

- **Previous-version redeployment is a pipeline setting.** If it was not enabled before the bad release, it is
  not available during the incident — only higher versions can be deployed.
- **Extended backup retention** requires a production **managed** environment, and where a group rule sets
  retention the individual environment cannot override it. The retention you have during an incident is the
  one someone configured earlier.
- **Capacity headroom is a recoverability requirement, not a finance matter.** Being over capacity blocks
  restore, copy, recover and environment creation — so the failure is discovered at the worst possible
  moment.

The reversibility strategy must therefore be **named, enabled and rehearsed before go-live**: which
mechanism, what it destroys, who re-establishes connections and sharing, how long it takes, and what happens
to integrated systems and replicas. "We can roll it back" is false unless a specific mechanism has been
chosen, switched on and tested. Say this to sponsors before go-live, not during an incident.

### 8.4 Exit and portability mechanics

- **Portability comes from solutions, and it is directional.** A managed solution **cannot be exported**; an
  unmanaged solution can be exported *as* managed. So the exportable source of truth is the unmanaged
  solution in the development environment — or the repository, where rung 3 is in use.
- **Uninstalling a managed solution is data-destructive.** When it is deleted, all its customisations and
  extensions are removed, and **the data in its custom tables and in its custom columns on other tables is
  lost**. Solution boundaries are therefore data-lifecycle boundaries, and "remove the solution" is not a
  clean exit.
- **The publisher forecloses re-homing.** Once a component is introduced in a managed solution under a
  publisher, that publisher cannot be changed. Moving ownership across publishers requires deleting the
  component, upgrading the original solution to remove it from the target, and recreating it — **with loss of
  all data in that table unless it is migrated first**.
- **Data leaves by a different mechanism than metadata.** Solutions contain no business data, and a database
  backup cannot be copied out. Reference data, configuration data and business data all need their own
  migration mechanism.
- **Cross-tenant movement is not an in-product pipeline capability**, and tenant-to-tenant migration is not
  supported where the vendor-access-approval control is enabled. Cross-tenant delivery is a rung-3 activity.
- **The repository is the most portable artefact**: the Git file format is designed to be human-readable and
  de-duplicated, which is what makes a repository a genuine exit asset rather than a convenience.
- **Retirement of a running solution** is a documented multi-step procedure (solution with dependencies →
  export/import → security roles → configuration and data migration → test → notify → remove access →
  delete), owned by the governance side (`governance/governance-and-environments.md`). Its real work is the
  data-migration step.

The **cost** of any of this belongs to `economics/licensing-and-cost-drivers.md`; this file supplies the
mechanics and the sequencing obligations.

## 9. The gates, and the absent test framework · `decision-grade`

**Solution checker is static analysis, not a test.** It analyses exportable unmanaged solutions —
custom workflow activities, web resources, SDK message steps, cloud flows via the flow checker and Power Fx
expressions via the app checker — with severities and categories, and its output can be consumed as SARIF.
Managed and third-party managed solutions cannot be analysed. Its own stated limit is decisive: **using it
does not guarantee a successful import, because the static checks do not know the configured state of the
destination environment.** Only critical-severity rules block, exclusions are supported, and enforcement is
configured by governance per environment or group — the delivery team inherits it and cannot weaken it inside
its own pipeline (`governance/governance-and-environments.md`).

**There is no supported first-party low-code functional test framework.** The former low-code test engine is
**deprecated** — documentation and repository no longer maintained — with the stated reason that its
expression-language implementation created unnecessary limitations avoidable by using the browser-automation
framework directly, and the stated migration path being that framework's samples. Recorded as a deprecation,
not as a recommendation of the deprecated tool.

What follows mechanically:

- Solution checker is a code-quality gate; pipelines prevalidate dependencies and configuration; neither is a
  functional test. Treating a green check as release evidence is a category error.
- The documented environment guidance requires a test environment for end-to-end validation including the
  deployment itself — which is **manual by default**.
- Any requirement for automated regression testing forces pro-dev capability (a browser-automation harness or
  a custom one) and an explicit budget line. For a maker-built estate the honest position is manual
  acceptance testing plus static analysis, with regression risk rising with change velocity — which is itself
  an argument for smaller solutions and shorter release cycles.
- A business-critical release should state which validation level it requires and fund it: documentation and
  limits for hard support boundaries; a **bounded pilot with monitoring** for latency, throttling,
  security-model cost and recovery behaviour; a pro-dev automated harness for repeatable functional, API and
  performance regression; and **managed-environment fidelity** where the behaviour depends on
  managed-environment, network or security controls. A non-managed test environment cannot faithfully emulate
  a managed production environment.
- Unit testing of plug-ins and custom code follows normal practice for that stack and is outside the
  platform's own tooling — **not established** in the baseline.

**Release governance: what is auditable in-product, and what must be built.** In-product: pipeline run
history and analytics, automatic artefact retention, artefact immutability with sequential stages, approvals
through the extension point, the delegated identity, and retention control through bulk-delete jobs in the
host. **Not** in-product: change-advisory records, release notes, links to work items, an emergency-change
procedure, and any approval taxonomy beyond what the extension flow implements. A repository-based toolchain
supplies those natively. So traceability from requirement → change → release exists only at rung 3, or where
it is built around pipelines.

## 10. Release coordination across boundaries — the second supply chain · `decision-grade`

Where a design crosses into an external estate (an API layer, a broker, a worker, an analytical target), it
requires **two coordinated supply chains**: the solution pipeline **and** an infrastructure/code pipeline for
the external half. The release unit must declare **contract compatibility and sequencing**. Deploying only
one side is admissible only where backward and forward compatibility is *proven* — otherwise the two halves
diverge in production.

Four obligations that are easy to miss:

- **The connector and the API contract are one release boundary.** Connector definition, connection references
  and the consuming solution need an explicit import and deployment order, and the backend schema is a
  versioned contract.
- **Compensation and reconciliation artefacts are part of that contract** — idempotency keys, mapping rules,
  compensating actions, reconciliation schemas — and require change control equal to the forward write path.
  The identity permitted to execute them, and the business owner of unresolved items, are named on the
  security and governance sides.
- **Recovery crosses the boundary** (§8.2): a restore on one side needs a defined action on the other.
- **Someone must coordinate the release.** If the second supply chain cannot be funded or owned, the two-sided
  design has no operator — the same conclusion the governance side reaches from the ownership direction
  (`governance/governance-and-environments.md` §13).

This is not a claim that external components or custom connectors are inherently wrong. It is the condition
under which their lifecycle cost changes the delivery plan.

## 11. Irreversible choices made in the first days · `decision-grade`

All four are made before anyone thinks of them as decisions.

| Choice | Why it is irreversible | Consequence of getting it wrong |
|---|---|---|
| **The publisher** | The publisher of a component in a managed solution cannot be changed; ownership can move between solutions of the *same* publisher only | Delete, upgrade to remove, recreate — **with data loss unless migrated first**. Choose one publisher as a tenant standard, in week one |
| **Table ownership type** | Set at table creation | Recreating the table |
| **Dynamics 365 applications at environment creation** | They **cannot be uninstalled or installed later** | A new environment plus a migration; and dependency complications when distributing solutions |
| **Environment region** | Set at creation; binds the environment and constrains service-update alignment, key-management region matching and private-network region pairing | A new environment plus a migration (`governance/governance-and-environments.md` §7) |

**One further topology constraint is easy to mistake for a product defect.** Geographic service-update
stations mean a solution **can** be imported into an environment on a newer service version, but **cannot
reliably** be imported into one on an older version. Development environments must therefore sit on the same
or an earlier station than production — otherwise imports fail intermittently for reasons that look like bugs.

## 12. Deprecated tooling · `decision-grade`

Recorded as deprecations only, because a large body of circulating guidance still assumes them:

- **The community ALM accelerator is deprecated** — no new features, and issues are no longer reviewed or
  addressed. The stated direction is in-product pipelines, optionally extended into a repository toolchain.
  Its published comparison table remains the clearest framing of the rung choice but is **stale in at least
  one row**: it predates native Dataverse Git integration and lists source-code integration as planned.
- **The low-code test engine is deprecated** (§9).
- **The community governance starter kit is deprecated** — recorded in
  `governance/governance-and-environments.md`. It matters here because an organisation running both is
  carrying debt in delivery *and* in governance at once, with in-product replacements whose parity is not
  established.

Guidance predating that shift — including some still-published vendor pages — is historical.

## 13. Failure modes · `decision-grade`

> **Editing production directly.** The edit creates an unmanaged layer that defines runtime behaviour and
> permanently shadows every future managed update to that component. Consequence: a change that cannot be
> promoted, reviewed or reverted, and a component that silently stops receiving updates.

> **Rollback assumed to exist.** No mechanism was named, or the previous-version setting was never enabled.
> Consequence: an outage extended by a recovery path that breaks connections, changes app identifiers,
> disables automations and cannot target production directly — discovered during the incident.

> **Environment-specific values shipped inside the artefact.** The named outcome is production pointing at
> development data sources. Consequence: every promotion becomes a manual edit, which reintroduces manual
> release, and credentials travel in an artefact.

> **Manual promotion as the steady state.** No artefact integrity, no prevalidation, no run history — and the
> deployer becomes the **owner** of the deployed objects. Consequence: production ownership assigned by
> accident, which is the upstream cause of the ownerless-artefact backlog.

> **A shared development environment for a team.** Unmanaged solutions provide no isolation: every
> modification applies to the environment regardless of which solution is open. Consequence: silent
> overwriting, and a serialisation agreement that depends on people remembering it.

> **Solution checker treated as a release gate.** It is static analysis that explicitly does not know the
> target environment's state and does not guarantee import success. Consequence: a release signed off on
> evidence that tests nothing functional.

> **Multiple publishers, or dependencies between solutions.** Publisher ownership is irreversible;
> cross-solution dependencies enforce import order, deadlock, and produce imports that succeed while the
> automation inside does not work. Consequence: the repair is delete-and-recreate with data loss, or an
> undiagnosable non-functional deployment.

> **A one-sided supply chain for a two-sided design.** Only the low-code half is under a managed lifecycle.
> Consequence: contract versions mismatch in production, and compensation logic drifts out of step with the
> write path it is meant to reverse.

> **Non-solution artefacts above the departmental class.** Backup coverage, capacity-licensed ownership,
> monitoring visibility and pipeline deployment all require solution membership — and a non-solution
> automation's owner cannot be changed at all. Consequence: four independent operational failures from one
> apparently cosmetic choice, plus retrofit work when it matters most.

> **Rung 3 imposed on a single-maker departmental tool.** The prerequisites — repository, environment per
> maker, pro-dev capability — are a real cost. Consequence: lead time that pushes makers off-platform, which
> is the governance failure the rigour was meant to prevent.

## 14. Consequences elsewhere · `decision-grade`

- **→ governance.** The dev/test/prod topology *is* the environment strategy, so a governance decision about
  environment count directly changes lifecycle capability. The release gates — solution-checker enforcement
  and block unmanaged customizations — are environment or group settings a project inherits and cannot
  weaken. **Managed Environments, their entitlement chain and the dated milestones (`TW-V1`, `TW-V3`) are
  owned there.** Drift is fought on two fronts: solution-layer discipline here, environment-configuration
  consistency there — and business units, teams and service identities fall in the gap, travelling in neither
  solutions nor group rules. See `governance/governance-and-environments.md`.
- **→ operations.** **Deployment ownership is decided here and operated there**: the deploying identity owns
  the objects, automations run under their connection owner, and delegated deployment is the only mechanism
  that makes that identity a governed asset instead of an individual. Connections and connection references
  are first-class configuration items with an inventory (which reference, which connector, which identity,
  which credential store, which owner) because **every restore breaks them and every deployment must supply
  them**. Administrative and deployment operations are load events on production, and recovery is a runbook
  with owners and elapsed-time estimates. See `operations/operability-and-support.md`.
- **→ economics.** Two exit-side costs are decided here: **uninstalling a managed solution destroys the data
  in its custom tables and columns**, and cross-tenant or cross-publisher movement means recreate-and-migrate
  rather than move. Adopting in-product pipelines carries the managed-environment entitlement obligation for
  every active user of every target environment; environment count for isolation and rehydration is itself a
  cost axis; and the automated-testing gap is a budget line, not a configuration. See
  `economics/licensing-and-cost-drivers.md`.
- **→ integration.** The connector plus the API contract is **one release boundary** with an explicit import
  order; the canvas custom-connector workaround creates an unmanaged layer and therefore collides with a
  mandatory integrity control; a restore rewinds one participant while others retain later state, so a
  post-restore reconciliation step is part of the release plan. See `integration/integration-mechanisms.md`.
- **→ automation.** **Solution-awareness is the precondition for an automation's backup coverage,
  capacity-licensed ownership, monitoring visibility and deployability** (§4), and a non-solution automation's
  owner cannot be changed at all. Restore deletes solution automations in the target and returns them turned
  off. Connection ownership decides the runtime identity. See `automation/automation-mechanisms.md`.
- **→ data and security.** Region and residency are fixed at environment creation; table ownership type is
  immutable at table creation; some one-way upgrades exist. Restore requires matching key-management and
  private-networking policy state, so the **security posture determines which recovery paths remain open** —
  establish that before switching a control on, not after an incident. A secure implicitly-shared connection
  imported via a connection reference has a documented case where the security is not set properly in the
  target, so post-deployment verification belongs on the release checklist. See `data/store-boundaries.md`
  and `security/security-controls.md`.

## 15. What must be verified · `decision-grade`

| Fact | Register row |
|---|---|
| Release-artefact packaging ceilings — solution size, and environment-variable value length | `VS-26` |
| Automatic conversion of pipeline target environments to managed — outcome and current default | `TW-V1` |
| Managed-environment licence enforcement milestone (owned by the governance unit) | `TW-V3` |
| Backup and restore windows underpinning the recovery objective | `VS-17` |
| Backup retention windows by environment class | `VS-07` |
| Entitlement fit of the required lifecycle capability set for the affected population | `VC-05` |
| Preview / general-availability state of any lifecycle capability the plan leans on | `VC-10` |

**Not established in the baseline** — do not fill from general knowledge:

- Whether pipelines gained **source-code integration, multi-solution deployment, choice of import behaviour,
  or multi-developer support**. All four are documented as "not currently" or "planned", and at least one
  published comparison is already stale.
- Whether the **previous-version redeployment** setting is on by default, and whether it has retention limits.
  This is the reversibility mechanism most likely to be assumed rather than enabled.
- The general-availability state of native Dataverse Git integration and its coverage of the **canvas app
  artefact** specifically.
- Whether any **supported first-party functional-test option** has replaced the deprecated low-code engine.
- The **break-list** for block unmanaged customizations — it was updated during the research window; expect
  churn.
- The current **build-tool task version** position, and whether username/password service connections are
  still supported at all.
- The delegated-deployment **sharing limitations** ("first deployment only", "no individual users") — both are
  flagged as current-state.
- The **deployment settings file's** capabilities and its interaction with delegated deployments.
- The **catalog** mechanism as a component-distribution route.
- **Plug-in and custom-code unit-testing** practice, and any first-party support for it.
- The exact entitlement position of **developer-plan environments used as pipeline targets** — documented as a
  worked example and easy to over-read.
- **The solution size ceiling, the environment-variable length ceiling and the variable propagation window.**
  The shapes are carried in §4 and §7; no volatility row owns those numbers, so each is read at the decision
  date and recorded on the engagement's own row.

## 16. What not to infer · `decision-grade`

- **A capability absence is not a verdict.** "There is no rollback" and "there is no supported first-party
  low-code test framework" are domain knowledge. "Therefore the platform is inappropriate" is a selection
  verdict and belongs to `decision-tree.md`.
- **A documented boundary here is not evidence that another option class performs better.** The baseline holds
  no like-for-like lifecycle comparison against SaaS, custom/pro-code, incumbent platforms or other low-code
  estates — those stacks have their own reversibility, test-automation and supply-chain obligations, which
  were not evaluated. Where the comparison is material, the decision model's comparator semantics stand.
- **The rungs are a capability ladder, not a preference order and not a maturity score.** A single-maker
  departmental tool at rung 1 is a legitimate position; the failure is an *undeclared* rung, or a
  reversibility commitment the rung cannot support.
- **Do not read this file as the decision model.** Outcome semantics, stage order and exit classes are
  `decision-tree.md`'s; nothing here ranks options or gates them.
- **Do not treat pipelines as source control, or source control as deployment.** The documented placement is
  Git in developer environments, builds to produce artefacts, pipelines to deploy.
- **Do not treat "it imported successfully" as "it works".** The documented failure is an import that succeeds
  while the automation inside does not, because a dependency was not recognised.
- **Do not treat restore as an undo**, and do not treat capacity headroom as a finance matter — it is a
  precondition for restore.
- **Do not recommend deprecated tooling** (§12). It is recorded as deprecation and existing technical debt,
  nothing more.
- Naming conventions, traceability stamping in component descriptions, go-live and post-go-live checklists,
  and hypercare arrangements are **delivery practice** — `craft/delivery-conventions.md`, which is never an
  Options pull target and may never state a platform limit.
