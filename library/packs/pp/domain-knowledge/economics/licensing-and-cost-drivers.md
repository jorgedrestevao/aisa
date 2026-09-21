# Licensing and cost drivers — meters, units and affected populations

<!--
provenance: RUNTIME (domain knowledge) · class: RESEARCH
authored: 2026-09-04 (Step 4B) · design authority: Step 4A — Domain Knowledge Runtime Model
Pull-based: consulted when a concrete decision question requires it (decision-tree.md §9).
Never preloaded. Canonical research traceability lives in the Step 4B authoring report.
-->

## 0. When to pull this file

- *Which meter moves with this audience-and-frequency shape?*
- *Which population does this control oblige, and is it funded?*
- *What grows at horizon that does not grow today?*
- *This design looks cheaper — did the cost actually fall, or did it move?*

This file states **the economic mechanisms of the platform: the unit each one bills, what makes it grow,
and which population it counts.** It carries **no prices** — deliberately, and permanently (§12). It does
not decide which option wins, and it does not price the options: that is the economics stage of the
decision model (`decision-tree.md` S8), which prices every surviving candidate on the same dimensions.
**This file supports that stage; it does not replace it.**

---

## 1. What this is for · `decision-grade`

Cost questions arrive as *"what does it cost?"* and are answerable only after the question is turned into
four parts: **which meter · what unit · which population · what growth mechanism.** The price attached to a
unit changes; the unit is an architectural fact with a long half-life. So the durable knowledge is the
*shape* of the model and the consequences of that shape — which designs are cheap and which are expensive
in a way that survives a price change.

One structural absence frames the whole domain: **the platform's own architecture framework has no
cost-optimisation discipline** — the vendor publishes one for its cloud platform and not for this one. So
there is no first-party design review that challenges cost the way reliability and performance are now
challenged, and cost guidance appears only as incidental callouts inside other pillars. Any cost discipline
applied here is **borrowed and translated — supported synthesis, not vendor-endorsed guidance for this
platform.** An organisation that adopted the framework as its review standard has adopted a standard that
does not look at cost.

## 2. When it becomes material · `decision-grade`

- The audience is **large, external, anonymous, or of unknown size**.
- The requirement names a **capability on the paid side of an entitlement boundary** — a specific system to
  integrate with, an on-premises data path, an external-facing site, a particular application type.
- A **mandated control** is in scope (governance, security, recovery, observability).
- **Audit, retention or archival** is a requirement rather than a preference.
- The workload has a **growth horizon** or a **seasonal peak**.
- Cost must be **attributed** to business units.
- The solution is expected to **live for years**, or has a plausible path from departmental to critical.

## 3. The five economic mechanisms · `decision-grade`

Five mechanisms operate **simultaneously**. Nothing is priced on one axis.

| # | Mechanism | Billing / metering unit | What makes it grow |
|---|---|---|---|
| 1 | **Per-user entitlement** | **A person**, per month | Headcount needing the capability, and whether that capability sits on the premium side of the entitlement boundary |
| 2 | **Per-app / per-scope entitlement** | **A (person, app) pair**, stackable, scoped to **one environment** | The number of *pairs* — so application **count** and environment **count** are both cost drivers, and the same app in two environments is two entitlements |
| 3 | **Capacity entitlement** | **An automation object** — an automation, a machine, a hosted machine | The number of automations needing autonomous entitlement or a higher throughput profile. Buys throughput and autonomy, **never access** — it cannot replace a user entitlement |
| 4 | **Consumption meter** | **A usage event** — an active (person, app) month · an automation run · a unique website visitor-month · an AI credit | Actual usage. Idle capacity costs nothing and a spike costs linearly |
| 5 | **Stored capacity** | **A GB-month** of database, file or log storage, **pooled at tenant level** | Data volume, file volume, **audit volume**, **index volume**, replica volume — over time |

**The durable principle, and the one that catches experienced teams:**

> **A design decision can move cost between these mechanisms without reducing it.**

Consolidating applications moves cost from (2) to (1). Assigning capacity to an automation moves it from
(1) to (3). Switching an environment to consumption billing moves it from (1)/(2) to (4) — and, if prepaid
assets are still assigned to that environment, adds cost rather than moving it (§8). Avoiding a premium
data path moves cost out of (1) and into build effort, duplicated data and storage (§9). **The test of a
cost improvement is therefore never the line that fell; it is the sum across all five plus the effort
lines.**

**Two ordinal relationships are worth carrying because they are design guidance that outlives any rate.**
Per GB-month, **database storage is the most expensive tier, log storage next, file storage the cheapest** —
by a wide margin, which is why a large object belongs in file storage rather than in a database column, and
why an index that bills at the *database* rate is an expensive thing to grow. And per run, **an unattended
robotic run costs materially more than an orchestration run, which in turn costs more than a
standard-connector run — which is free.** That last relationship prices the entitlement boundary a second
way, and it prices the *build-an-API versus automate-the-screen* choice.

**Two documented asymmetries in the consumption meter are design levers, not billing trivia.** Decomposing
orchestration logic into child definitions — which the structural action ceiling pushes you toward anyway —
is charged **once, at the parent**, for cloud and attended runs, and **at both parent and child** for
unattended runs. So the same good practice has opposite cost signs depending on run mode. And testing in
the designer and resubmitting failed runs is **not charged**, which removes a perverse incentive against
proper error handling.

## 4. Affected-population concepts · `decision-grade`

**Conflating these populations is the dominant costing error in this domain.** They are different
quantities, counted by different rules, and the design decides which one applies.

| Population concept | Counting rule | Where it bites |
|---|---|---|
| **People** | Headcount needing the capability | Mechanism 1. The premium boundary moves this *whole* population at once |
| **(Person, app) pairs** | One entitlement per person per application scope, stackable, **per environment** | Mechanism 2. Application decomposition and environment topology are both cost drivers here. Note the direct tension with performance and maintainability, which push toward *splitting* applications while this pushes toward consolidating them — that tension needs an explicit decision, not a default |
| **Active users of an application in a month** | A person who opens the application at least once in the month; repeat access is not counted; people already holding a full per-user entitlement are not counted at all | Mechanism 4. This is why *widely shared, infrequently used* is the consumption case |
| **Unique billable website visitors per site per month** | **Authenticated** uniqueness is the *contact record*; **anonymous** uniqueness is a *browser cookie* | Mechanism 4. Neither is a count of people — see §11 |
| **Every active user of an environment** | Everyone who uses anything in that environment, including users of non-premium applications | Mechanism 1, triggered by a **control** rather than by the application. This is §6 |

**The rule to hold on to:** the unit is the **affected population**, not the number of applications. A
control or an entitlement boundary that touches a population is a larger line than the application it was
introduced to protect.

## 5. Capacity, storage and request meters — and what silently consumes them · `decision-grade`

Stored capacity is the mechanism that surprises people, for three reasons: it is **pooled at tenant
level**, it is consumed by things nobody budgeted, and its failure mode is not a bill.

**What consumes it that no one plans for:**

- **Audit logs.** Auditing consumes **log** capacity, and **no application or automation user entitlement
  accrues any log capacity at all**. A retention requirement is therefore a priced, unfunded line by
  construction, and retention scope is a decision taken at creation because it is not retroactive.
  > Documented reading · read 2026-09-04 · re-verify: VS-05 (Options, and at any compliance review)
- **Search indexes**, which bill at the **most expensive** tier and grow with how many tables and columns
  are indexed. Disabling search is **not** a capacity remedy: the index deletion becomes permanent after a
  short documented window, reindexing a large organisation takes days, dependent experiences break, and the
  vendor's instruction is not to turn it off.
- **File attachments**, growing independently of row counts.
- **Recovery replicas.** Cross-region protection consumes a **second full copy** of the environment's
  storage, drawn from the same tenant pool — and overage management is explicitly outside that feature's
  own scope.
- **The per-environment floor.** Every environment consumes a storage floor even with no data, so
  environment proliferation has a direct capacity cost. Developer-plan and trial environments are free of
  it.

**Three mechanics that work against the customer:**

- **Borrowing across capacity types is one-directional.** A surplus in the cheaper type cannot offset a
  deficit in the more expensive one.
- **Nothing rolls over.** Request entitlements do not roll over between windows; site capacity does not
  carry forward between months. The **peak** window is the window that must be provisioned.
- **The request pool for non-licensed identities is shared tenant-wide** with no project-level view, so one
  integration's growth silently consumes another project's headroom. It needs a **named tenant-level
  owner**, which a project-level budget cannot supply.

**Two request-side drivers that are easy to miss:** **retries and pagination are billed as work**, so an
unreliable dependency is a cost driver; and the remedy the vendor names for throttling is **commercial** —
buy capacity, assign a capacity entitlement to the object, or move to consumption billing. A performance
problem therefore arrives as a licence decision.

**The failure mode is a block, not a bill.**

> **Exceeding pooled storage blocks administrative operations** — creating, copying, **restoring**,
> recovering and adding the data platform to an environment. Capacity headroom is therefore a
> **recoverability requirement with a standing minimum**, not a finance nicety, and a capacity problem is
> typically discovered *during an incident*. Notifications begin only when headroom is already low.

Detection is weak in the other direction too: consumption reporting is **preview and partial**, with
documented defects, and does not yet cover every surface. Treat the reported figure as incomplete.
> Documented reading · read 2026-09-04 · re-verify: VC-07 (design time, and annually)

## 6. Control-related entitlement obligations · `decision-grade`

This is the coupling that turns a governance or security requirement into the largest line in the model.

**The chain to model, in this order:**

```text
mandated control → required entitlement → affected population → current customer holdings → gap
```

**What makes it different from an ordinary cost driver:** nearly every capability needed to *operate* the
platform responsibly — telemetry export, extended backup, cross-region recovery, deployment pipelines,
network isolation, the preventive governance controls — sits behind the **managed environment class**, and
that class obliges an entitlement for **every active user of the environment**, not for the application's
own users, and **including users of non-premium applications**. Several individual controls additionally
require higher-tier productivity, directory or compliance entitlements for the users **in scope of the
control**, and identity-conditional access is a separate directory-entitlement decision of its own.

So the causal chain that produces the surprise is:

```text
criticality → operational requirements → managed environment class → entitlement for that environment's whole population
```

This is why *a departmental solution becomes expensive the day it matters* — not because of what the
application does, but because of what **operating it responsibly** requires.

**And where the control is mandated and that population is unfunded, this is an economic infeasibility
question, not a trade-off.** The instruction is explicit: **never remove a required control to make an
option look cheaper.** The honest outputs are a reduced scope, a different architecture or control, or the
economic-infeasibility outcome class — which asserts nothing whatsoever about what any other class would
cost (`decision-model/outcome-classes.md`, class 7).

> **`TW-V3` is the dated commitment that hardens this.** On its date, users of a managed environment
> without the appropriate entitlement are **blocked from opening applications** — governance capability
> acquires a hard, quantifiable price. On firing, re-price the **whole environment population**, not the
> application's own users.

> **`TW-V1` is the one that arrives without being chosen.** Deployment-pipeline target environments are
> automatically converted to the managed class, which turns adopting in-product lifecycle management into a
> **tenant entitlement decision**. Its date has passed and **whether the conversion completed as announced
> is an open question in the baseline** — confirm the current default with the platform-owning team before
> costing an in-product lifecycle path.

## 7. Demand shape, and growth at horizon · `decision-grade`

**The mechanism is selected by the shape of demand, not by unit price.** The two questions that most change
the answer are asked before any product is named:

- **Who** needs the capability — a fixed team, a whole workforce, or an unpredictable external population?
- **What shape is the demand** — steady per-person daily use, or bursty, seasonal, long-tail use?

The vendor publishes the break-even logic itself, and it is about shape:

| Shape | Mechanism it favours |
|---|---|
| **Many people × few interactions each** | Consumption (4) |
| **Few people × many interactions each** | Prepaid entitlement (1)/(3) |
| **Seasonal or campaign-shaped** | Consumption (4) — idle months cost nothing |
| **Adoption genuinely unknown** | Consumption first, deliberately, then true up to prepaid once patterns are measured |
| **High run count on one automation** | Capacity entitlement on the object, for price certainty |
| **A large or unpredictable external population** | External-site capacity, forecast on unique monthly visitors |
| **A handful of named partner individuals** | Guest entitlement — with the **tenant of record** recorded, because the entitlement must sit in the correct tenant and the data platform tightens that to the tenant holding the data |

Prepaid and consumption **coexist** in the same environment, so this is a per-workload choice, not a
tenant-wide posture. Plan a periodic true-up as an explicit activity.

**Growth at horizon is what is priced, not the launch state.** Every meter in §3 and §5 has a growth
mechanism, and three of them are provisioned against the **peak** rather than the average: site capacity
does not carry forward, AI capacity is enforced on the **peak month**, and storage notifications begin when
headroom is already thin. Size against the horizon volume and the peak window, name the **growth
mechanism** for each meter, and record the consumption level at which the economics change — that level is
a natural decision tripwire, and it is the economic twin of the redesign trigger in
`performance/performance-and-scale.md`.

> **`TW-V2` is the dated commitment on the AI meter.** The bundled credit entitlement is retired on its
> date, so any option economics resting on those bundled credits loses its basis. Per-operation consumption
> is **complexity-dependent and unpublished**, so it cannot be modelled from a per-transaction estimate:
> establish it **empirically in a bounded pilot**, then size for the peak month or use the consumption
> meter.

## 8. Cost attribution as a design constraint · `decision-grade`

**Consumption billing policies are the only documented cost-attribution mechanism**, and they operate **per
environment**, surfaced as a cloud resource that can carry resource groups and tags. The consequence is
structural: **a requirement to attribute cost to business units constrains the environment topology.** It
cannot be satisfied later by a reporting exercise.

Two mechanics to carry:

- **Enabling consumption billing on an environment silently invalidates prepaid assets assigned to it** —
  application passes, prepaid site capacity, unattended automation add-ons are **ignored and not consumed**.
  An administrator doing the right thing for flexibility can pay twice. Audit and reallocate the prepaid
  assets **before** enabling, and record the enablement as a change with a cost consequence and an owner.
- **Consumption billing overrides prepaid capacity in the same environment**, which means the two cannot be
  mixed *within* one environment as a hedging strategy — the hedge happens *across* environments, which is
  again a topology decision.

## 9. The licence-avoidance trap, and the entitlement boundary · `decision-grade`

**The entitlement boundary is where a technical choice silently sets the commercial model for a whole
population.** Which system the solution talks to — and whether the path crosses into premium or custom
connectors, an on-premises data path, or a particular application type — can move the entire user
population from seeded rights to standalone entitlement. **Multiplexing a shared identity to avoid it is
prohibited and carries a documented right of suspension**, so there is no workaround. Establish the
connector tier and its entitlement consequence **at design time, on the whole audience** — where a
standard-rights path meets the requirement the saving is population-wide; where it does not, the premium
line belongs in that option's economics from the first comparison.

One residual honesty to preserve: **whether a single premium capability obliges premium entitlement for
*every* user of the artefact is an open item.** It is stated categorically by independent sources and is
consistent with the vendor's entitlement statements, but it is not verbatim-confirmed. It is load-bearing
for the largest cost finding in the domain, so it is a **per-engagement verification item, not an
assumption** (`VC-05`).

**The trap.** Designing around an entitlement and paying for it in rebuild is a documented family, and the
mechanism is always the same: **a licence line is visible and a workaround cost is not, so the invisible
cost wins the decision.** The four documented cases:

1. **The cheap store** — carries the documented performance, integrity, security and query-delegation
   penalties, plus duplicated data and the synchronisation runs that keep it current.
2. **The shared identity** — prohibited multiplexing, and it collapses the whole workload onto one
   throughput budget.
3. **The cheap automation owner** — buys a lower performance profile with a wide documented spread on
   request and content throughput, fewer retries, a higher postpone floor, an inactivity suspension, and
   reversion to the lowest profile if the owner leaves. Ownership is an architectural decision taken with
   the design, and the remedies have prerequisites: a capacity entitlement requires the automation to be
   **in a solution**, coupling economics to the delivery lifecycle.
4. **Avoiding the managed environment class** — forfeits telemetry export, extended backup, cross-region
   recovery, pipelines and network isolation: *the means of diagnosing and recovering from incidents*. The
   saving returns as outage duration and support burden.

**The rule:** whenever a design choice is justified primarily by entitlement avoidance, **require the
workaround cost to be stated explicitly alongside the saving** — extra storage, extra synchronisation runs,
extra build effort, forfeited operational capability, migration risk. **If the workaround cost cannot be
estimated, the avoidance justification is not established.** If it exceeds the saving, the entitlement was
the cheaper option.

## 10. Sunk capability and exit cost · `decision-grade`

**Sunk capability is a real economic input.** Entitlements already held, and a platform team already
operating, change the arithmetic — and the economically correct answer may be the incumbent capability,
precisely to avoid funding a second platform's operating model. Alongside it, **process change without
technology, and not doing it at all, are legitimate priced options** and are frequently the honest answer
for a genuinely low-frequency process, because the non-licence lines can exceed the value on their own.

**Exit cost is a cost dimension, not an afterthought.** Three documented mechanisms:

- **A deliberately cheap starting point can have a one-way door.** The capped free tier cannot buy more
  capacity; reaching its ceiling stops new solution creation while data keeps growing; it excludes the
  capabilities a maturing solution needs (audit, enterprise lifecycle, custom connectors, log capacity,
  robotic automation, AI capability); its upgrade converts **all** users; and export to a full environment
  is **not available**, so **the exit may be a rebuild**. Define the **graduation trigger and its cost at
  the start**: which measurable condition moves the solution to the next class, what that costs, and
  whether the migration is a rebuild.
- **Deprecation-driven remediation is a recurring, unavoidable line**, not a contingency — and deprecated
  tooling invalidates the implementation guidance written for it.
- **Refactoring as artefacts approach structural limits** is a scheduled cost for anything long-lived.

Where a sponsor wants productivity-workload economics with a mission-critical lifecycle, **name the
contradiction** rather than resolving it silently.

## 11. The counting hazards · `decision-grade`

| Hazard | Why it produces a wrong number |
|---|---|
| **People ≠ (person, app) pairs** | Two different mechanisms with two different growth drivers. A headcount is not an entitlement count once application scope enters |
| **Data volume ≠ audit volume** | Different capacity types, different rates, and **different funding** — no user entitlement accrues log capacity. An audit requirement is not covered by sizing the data |
| **Unique people ≠ billable visitors** | Anonymous uniqueness is a **browser cookie**: the same person on a phone and a laptop, or one who clears cookies, is counted repeatedly — so the *same* audience costs more if it is privacy-conscious or multi-device, which correlates with exactly the public audiences these sites serve. Forecast with an explicit multi-device/cookie-churn multiplier, never from a unique-person estimate |
| **Authenticated uniqueness is a contact record** | So **contact duplication is a billing defect**. Deduplication is a data-quality requirement with a commercial consequence |
| **An availability probe can bill itself as traffic** | A monitor sending a standard browser user agent may be counted as an anonymous visitor. Point it at the documented service endpoint with a non-browser agent — an operations requirement with a cost rationale |
| **Per-environment minimum assignments** | External-site capacity carries minimum assignments per environment regardless of actual need, so several small sites cost more than one site with role-based content |
| **Preview billing caps** | A preview cap on the number of runs billed per day means the **bill can understate real usage**. Model from the full reported count, never from the billed figure |
| **Nothing rolls over** | Entitlements and site capacity both reset; a monthly average hides the peak that is actually provisioned |

## 12. The epistemic ceiling — and the price rule · `decision-grade`

> **This file carries no prices, and the pack must never quote one.** It carries billing **units**, cost
> **ratios** as orderings, cost **drivers**, affected **populations**, entitlement **shapes** and growth
> **mechanisms** — and it routes every figure to the licensing guide and the customer's own agreement.

That is not stylistic caution; it follows from the evidence. **The general product documentation is
explicitly not authoritative on entitlement** — every licensing page defers to the licensing guide, the
guide itself states that it is informational and that pricing is subject to change, and the universal
online-service terms sit above both. Published example prices are labelled *illustrative only* and vary by
contract, volume, agreement type and sector. And the terms carry a real consequence: **consumption above
documented entitlement permits suspension of the service after reasonable notice** — a genuine availability
risk with a commercial root cause.

**Consequences for the engagement's own record:**

- **No cost or entitlement claim is `Confirmed` from documentation.** All are `Assumed` with a validity date
  and a named validation owner — the customer's licensing desk.
- **Claims resting on transition-period, preview or bundled terms are `Risky`, not `Assumed`.** The estate
  can be structurally non-compliant with **no bill and no error** until enforcement begins, so nothing
  surfaces the problem on its own.
- **Several meters are in preview.** Never assert their state; re-read it (`VC-06`).
- Natural revalidation triggers: contract renewal · any vendor licensing announcement · request-reporting
  reaching general availability · the `TW-V1`/`TW-V2`/`TW-V3` dates · crossing a capacity notification
  threshold · any move of an environment to or from consumption billing.

## 13. Failure modes · `decision-grade`

> **The licence line treated as the total cost of ownership.** The business case prices entitlements and
> stops, omitting the lines the vendor states but does not price — and, in a hybrid design, omitting the
> other platform entirely. There is no cost-optimisation discipline for this platform to prompt for them, so
> nothing in the process catches the omission. Consequence: a business case that fails on the lines nobody
> priced, and a comparison that is asymmetric by construction.

> **Consumption without an owner or a growth model.** Metered consumption — requests, three storage types,
> audit and index growth, external service usage — has no owner, no growth model and no threshold.
> Consequence: the first visible symptom is an **administrative operation being blocked**, which surfaces as
> a recoverability incident rather than as a budget variance.

> **Operational and security prerequisites treated as configuration.** A mandated control is assumed to be a
> setting, when it carries an entitlement prerequisite priced by **affected population**. Consequence: a
> cost line larger than the platform entitlements themselves, discovered after the architecture is fixed —
> and the tempting remedy, dropping the control, is forbidden.

> **The entitlement boundary discovered after the design is fixed.** A capability on the paid side is
> committed to without checking the consequence for the **whole** audience, and multiplexing is prohibited so
> there is no retrofit. Consequence: the entire user population moves from seeded rights to standalone
> entitlement mid-project.

> **A cheap start on a path to criticality.** A solution begins on a capped free tier with a plausible route
> to business-criticality; the ceiling stops new solution creation while data keeps growing, and export to a
> full environment is unavailable. Consequence: the exit is a rebuild, and it arrives at the moment the
> solution has become important.

> **A case built on transition-period, preview or bundled terms.** Higher transition figures, a preview
> billing cap, or a bundled credit allocation with a dated removal are treated as the steady state.
> Consequence: an order-of-magnitude sizing error on a date the customer does not control.

## 14. Consequences elsewhere · `decision-grade`

- **→ governance and environments.** The licence chain runs through the environment: the per-scope
  entitlement is scoped to **one** environment, every environment consumes a storage floor, the managed
  class obliges entitlement for its whole population, and cost attribution is per environment. So the
  environment topology is simultaneously a governance decision and the largest single lever on this model —
  and the pipeline-conversion tripwire (`TW-V1`) changes it without being chosen. See
  `governance/governance-and-environments.md`.
- **→ security.** A mandated control's **obliged population** is the economic unit, and where it is unfunded
  the outcome is an infeasibility question rather than a trade-off. The security domain owns whether the
  control is required; this file owns what obliging it costs and whom it counts. See
  `security/security-controls.md`.
- **→ operations.** Support is a **separate purchase** whose tier follows criticality, and the observability
  that would explain an incident is itself gated and metered — telemetry export is licence-gated, and
  storing and querying logs has a cost. So diagnostic capability is a **funded capability**, budgeted from
  the criticality rather than from the entitlement count. See `operations/operability-and-support.md`.
- **→ performance.** Bidirectional, and both directions matter. **The meter that binds moves the design**:
  the documented remedy for a bound meter is frequently commercial, so a throughput problem becomes a
  licence decision. **The meter that bills is not the same meter**: retries and pagination are billed as
  work, a resilience requirement consumes a second copy of storage and degrades automation throughput, the
  cheapest owner profile forces the most expensive architecture, and archiving is simultaneously a
  performance and a capacity lever. Also: capacity misjudgement cuts both ways — over-provisioning costs
  money, under-provisioning costs performance. See `performance/performance-and-scale.md`.
- **→ data.** Audit capacity is the clearest case of a governance decision with an unfunded price: auditing
  consumes log capacity that no user entitlement accrues, retention scope is set at creation and is not
  retroactive, and the archival remedy's relative cost is an **open item** in the baseline. Index growth
  bills at the most expensive tier, and disabling search is not a remedy. See `data/dataverse.md`.
- **→ lifecycle.** Exit cost is a lifecycle artefact: solution-awareness from day one is a prerequisite for
  the capacity-entitlement remedy, deprecation remediation is a recurring line, and the graduation trigger
  out of a cheap starting tier must be defined before the tier is chosen. See
  `alm/release-and-lifecycle.md`.

## 15. What must be verified · `decision-grade`

| Fact class | Volatility row |
|---|---|
| Entitlement fit of the required capability set — including whether one premium capability obliges premium entitlement for **every** user of an artefact | `VC-05` |
| Audience and frequency shape — **several meters are preview**, and two metering units have documented over-count behaviour | `VC-06` |
| Capacity consumption profile — add-on assignability, and the analytical-replication storage ratio, which is **unpublished** | `VC-07` |
| External and hybrid service consumption — **gateway-at-scale cost is an open item** | `VC-08` |
| Connector and service permissibility posture, per environment | `VC-03` |
| Per-mechanism throughput ceiling — **conflicted**, and connector **counts** are licence-conditional | `VC-01` / `VS-08` |
| Multi-tenancy and resale requirement — an **unclosed gap** (scope-blocker `BS-01`) | `VC-09` |
| Roadmap and preview dependency — two facts in the baseline already changed once during its life (scope-blocker `BS-02`) | `VC-10` |
| Audit retention and log-availability windows | `VS-05` |
| Content-throughput meter by owner profile | `VS-03` |
| Backup retention by environment class | `VS-07` |
| Agent surface — request bucket, a bundled credit entitlement **with a dated removal**, preview states (scope-blocker `BS-03`) | `VS-20` |
| Dated commitments | `TW-V1` · `TW-V2` · `TW-V3` |

**Not established in the baseline** — do not fill from general knowledge:

- **Per-operation AI and agent consumption.** Complexity-dependent and unpublished, which makes agent
  economics **unmodellable in advance**. Where it is decision-critical it is a decision-blocking unknown
  closed by a bounded pilot, not by an estimate.
- **On-premises gateway cost at scale** — host sizing, clustering and infrastructure. Entitlement is
  included with premium; the estate cost is an open item.
- **The relative cost of long-term data retention or archival** against live storage, though archival is the
  recommended remedy for audit growth.
- **The elapsed time or capacity cost of an environment copy or restore**, beyond the free-space
  precondition.
- **The relationship between purchased external-site capacity and delivered throughput** — capacity is the
  only scale dial and its effect is unquantified.
- **Any comparative cost study** against named alternative classes. None exists in this baseline.

## 16. What not to infer · `decision-grade`

- **Do not produce a comparative total cost of ownership against unevaluated alternatives.** No current,
  like-for-like comparator evidence exists — alternative-class economics are engagement-specific and the
  baseline's own comparator claims were withdrawn as too weakly evidenced. What exists is a **method**: the
  same dimensions, the same workload, the same operating model, priced for every surviving candidate at
  `decision-tree.md` S8. That method may legitimately conclude this platform is economically wrong.
- **A documented cost mechanism here is not evidence that another option class is cheaper.** A meter,
  boundary or entitlement obligation stated in this file describes *this* platform's economics only.
- **`craft/estimation-model.md` is barred from comparative economics.** It carries platform-side effort
  bands with **no comparator-side basis**, so using it in a cross-class comparison is comparator preference
  by construction, not evidence. Effort bands support sizing *this* platform's build, nothing else.
- **Do not treat the users-to-work ratio as a verdict.** That this platform has important
  people-and-scope-based meters while infrastructure alternatives expose more compute-and-transaction meters
  is a **hypothesis to test** with current pricing and the actual agreement — never a crossover rule.
- **Do not restate the cost dimensions of the economics stage here.** They are decision logic
  (`decision-tree.md` S8) and this file supports them.
- **Do not treat an entitlement statement as documented fact.** The authoritative sources are the licensing
  guide and the customer's agreement; route the question to the role that holds them, or to the document
  itself (`role:` / `fonte:`).
- **A cost mechanism is not a selection verdict.** *"This control obliges an entitlement for the whole
  environment population"* is domain knowledge; *"therefore choose something else"* belongs to the decision
  model — and where a mandated control's population is unfunded, the correct output is the
  economic-infeasibility class **with its mandatory reason**, which asserts nothing about any other class.
- **Do not assume the cost fell because a line fell.** Check the sum across all five mechanisms plus the
  effort lines (§3).
- Cost estimation technique, effort banding, rate cards and commercial modelling are **delivery practice** —
  `craft/` files, which are never an Options pull target.
