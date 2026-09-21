# Power Platform Pack — Question Bank

<!--
provenance: RUNTIME (formulation resource)
phase-visibility: consulted by `aisa-status` step 6d only
authored: 2026-09-03 (Step 2) · trimmed 2026-09-04 (runtime simplification, phase G)
authoring provenance: docs/pp-pack-authoring/research/pp/authoring/runtime-simplification-phase-g-report.md
-->

A resource for **formulating** questions, read at one place in aisa: `aisa-status` step 6d, after reasoning has already exposed a material gap. It is not a coverage specification, not a questionnaire, not an interview script, and no lens loads it.

## Discipline

1. **Reason first, formulate second.** A question is drawn from here because the Shared Understanding already shows something material is missing — never to fill the file's own set.
2. **Ask few.** The smallest number of questions that could change the framing, the options or the decision.
3. **Adapt the wording.** These are patterns, not scripts. Re-word each one in the engagement's own vocabulary.
4. **Discovery describes the problem, never the answer.** No question here names a vendor or a product, and none carries a platform number. Participants may name existing systems as current state; the requirement underneath is what gets recorded (`glossary.md` Part B).
5. **Every question moves a row.** The answer lands as Confirmed, Assumed, Unknown, Conflicted or Risky (`library/kernel/states.md`). Whether a question is worth a sponsor's hour is decided there — from `criticidade`, `custo` and `swing` — not here.
6. **A probe fires only when its trigger is observed** in the Shared Understanding or the captured evidence. No trigger observed, no probe.
7. **"No" must stay reachable.** See *Reachable outcomes* at the end.
8. **Roles, never people** (P-21). No question asks for a person's identity, a signature, an approval, or a document proving a third party's position. Where authority matters, ask for the **role**, the operation it must perform, and the plane that enforces it. A question whose only possible answer is a name or a piece of paper is out of scope — it changes no requirement, no data shape and no effort.

`Q-<LENS>-NN` = core pattern · `P-<LENS>-NN` = conditional probe. Ids are stable; gaps in the numbering are trimmed entries, not omissions.

---

# Part 1 — Core patterns

## Business

**Q-BUS-01** — What outcome does the sponsor expect from this, and how would they know six months later that it happened?

**Q-BUS-02** — If this stopped working — or never starts — what happens in the first hour, the first day and the first week? Which role is alerted, by which mechanism, and is there a manual fallback that has actually been used?

**Q-BUS-03** — Is this how your organisation differs from others doing the same job, or is it something every comparable organisation does much the same way? Does a product category exist for it?

**Q-BUS-04** — What is driving the date? What happens if it slips, and does a partial delivery have value?

**Q-BUS-05** — Which roles own the requirement, the data and the budget, and which role does a failure reach? Are they the same role — and what must each of them be able to do in the system?

**Q-BUS-06** — How often did the underlying rules change in the last two years, which role requested those changes, and how long is this expected to be in use?

## Operations

**Q-OPS-01** — Walk me through one real instance from start to finish. Who touches it, in what order, and what does each person actually do?

**Q-OPS-02** — What starts an instance, and how do the people involved find out it has started?

**Q-OPS-04** — What is the longest an instance has taken end to end, and what is the longest a person keeps one waiting?

**Q-OPS-05** — What happens when it goes wrong halfway — the first step completes and the second does not? What do people do today, and how do they find the half-finished ones?

**Q-OPS-06** — How many instances occur in a normal period, and in the busiest one? When are the busy periods, and what causes them?

**Q-OPS-08** — Which spreadsheets, shared mailboxes, shared files or paper forms is the process actually leaning on today, and who maintains each?

## User

**Q-USR-01** — Which distinct groups do this work, what does each one actually do, and roughly how many people are in each?

**Q-USR-02** — Whose accounts do these people use — the organisation's, a partner's, a customer's, or none at all?

**Q-USR-03** — Where does the work physically happen, on what devices, and what is the connectivity like at those places?

**Q-USR-06** — What accessibility and language obligations apply, and is any of it published, attested or contracted?

**Q-USR-07** — When something changes elsewhere, how current does what a user sees have to be, and what goes wrong if it is stale?

## Data

**Q-DAT-01** — List the things this work keeps information about. For each: who creates it, who corrects it, and which system is authoritative today?

**Q-DAT-02** — What relationships exist between those things, and which of them must remain consistent when either side changes?

**Q-DAT-03** — For each list or screen people work from: what do they filter, sort, search and count, and over how many records — today and in three years?

**Q-DAT-04** — Under your own classification scheme, how sensitive is this data, and what controls does that tier mandate?

**Q-DAT-05** — Who must not see which records, and which individual fields?

**Q-DAT-08** — Which other systems must this read from or write to? For each: who starts the exchange, what triggers it, what moves, and who owns that interface today?

## Governance

**Q-GOV-01** — Which regulations, standards, internal policies or contract clauses bind this work? Can we read the clauses themselves?

**Q-GOV-02** — Is there anything that constrains *where this must run* — as distinct from where the data may be stored?

**Q-GOV-04** — Must anyone be prevented from seeing this — including the people who administer the systems it runs on?

**Q-GOV-05** — What rules govern what a new workload here is allowed to connect to, on which environment, and what is the exception path and its lead time?

**Q-GOV-06** — Which role operates this after go-live, which role takes a user problem, and what mechanism does each one use — alert, log, dashboard, recovery path?

**Q-GOV-07** — Which role may change what is running, on which environment, and by which release mechanism? What must the platform be able to do when a change turns out to be bad — reverse it, isolate it, or hold it?

## Financial

**Q-FIN-01** — What does this cost today — time per instance times frequency, plus errors and delay — and which budget absorbs it now?

**Q-FIN-02** — What does the next twelve months cost if nothing changes at all?

**Q-FIN-03** — What budget is approved, on what basis, and is the recurring cost funded beyond year one?

**Q-FIN-04** — Is this capital or operational spend, and must costs be attributed back to business units?

**Q-FIN-05** — How many people will use this, how often does each one act, and how many distinct capabilities does each of them need?

**Q-FIN-06** — What does the organisation already hold and pay for that is relevant here?

---

# Part 2 — Conditional probes

Each trigger is observable in the Shared Understanding, the request context or the captured evidence. If you cannot point at the observation, the probe does not fire.

## Business

**P-BUS-01** · *Trigger: the requirement is recorded mainly as a list of features of the tool being replaced.*
Which of those features exist because the business needs them, and which exist because the current tool happens to work that way?

**P-BUS-02** · *Trigger: the work is recorded as something comparable organisations do much the same way.*
Has a packaged option been looked at? What did it fail on, and how much configuration would close the gap?

**P-BUS-03** · *Trigger: the requester is not the sponsor, or the sponsor is not the accountable owner.*
Who can stop this, and have they been asked? Whose budget carries it in year two?

**P-BUS-04** · *Trigger: more than one team or function is recorded in scope.*
Who uses it at launch, who might later, and would other teams come to depend on it?

## Operations

**P-OPS-01** · *Trigger: the same item can arrive or be submitted twice.*
Is there an identifier that is the same both times? Would a duplicate be noticed, and what would it cost?

**P-OPS-03** · *Trigger: a step is recorded as a calculation, an algorithm, a model, a solve, a render or a transform.*
How long does it take per item, does anything wait for the result, and does it need a specialist library?

**P-OPS-04** · *Trigger: a system on the path has no programmatic interface, or nobody knows whether it does.*
What is that system's remaining lifetime, how often does its screen layout change, and who would maintain an automation that drives it?

**P-OPS-05** · *Trigger: instances can pause for days or weeks.*
Where does the state of a paused instance live, and what is *"where is instance N?"* answered with today?

**P-OPS-06** · *Trigger: an approval chain is recorded.*
How many stages, who decides at each, are delegation and escalation required, what is the longest acceptable wait, and where does the decision happen today?

**P-OPS-09** · *Trigger: the organisation already runs comparable things.*
How are those operated today? Is there an on-call rota, has a recovery ever been rehearsed, and is ownership attested?

## User

**P-USR-01** · *Trigger: work occurs where connectivity is unreliable or absent.*
Is reading enough, or must people record work while disconnected? How long does a disconnected period last, and what should happen if two people changed the same thing while apart?

**P-USR-02** · *Trigger: any user is outside the organisation.*
Are they known partners, authenticated customers, or anonymous members of the public? Is the population knowable in advance, and is self-registration required?

**P-USR-03** · *Trigger: the audience is external, or brand conformance is recorded.*
Is a design system mandated, is conformance contractual, and which specific elements are non-negotiable?

**P-USR-05** · *Trigger: an icon on a phone, or notifications that arrive when the thing is closed, is expected.*
Must it be distributed under the organisation's brand, through an enterprise catalogue or a public store, and is the audience consumers?

**P-USR-06** · *Trigger: users are recorded as wanting to "ask it something" rather than fill in a form.*
Is the need retrieval and summary over existing content, or completing tasks that change something? What would it be permitted to do, and to whom? What would a wrong answer cost — a nuisance, money, or a regulatory event?

## Data

**P-DAT-01** · *Trigger: two teams already report different figures for the same thing.*
Which is authoritative, since when, who decided, and what does each side use theirs for?

**P-DAT-02** · *Trigger: a single business action must update more than one place.*
Which writes must be all-or-nothing? What does the business do today when one half succeeds? Is a correction window acceptable, and how long may it be?

**P-DAT-04** · *Trigger: reporting or dashboards are in scope.*
Do the reports aggregate, trend or span periods? Over how many records? Must they respect who is allowed to see what, and who is the audience?

**P-DAT-05** · *Trigger: documents, images or attachments are part of the work.*
How many per period and how large? Does protection have to travel with the file, and do large files move between systems?

**P-DAT-07** · *Trigger: a regulation, contract or policy is recorded as mentioning where data may be held.*
What does the clause say, word for word? Country-level or macro-region? Does the current estate already satisfy it?

**P-DAT-08** · *Trigger: an existing system is expected to keep authority over some of the data.*
Does that system enforce per-user rules itself today, or does it expect the caller to have done it?

**P-DAT-09** · *Trigger: an exchange with another system carries meaningful volume.*
How many records or messages per minute at peak — not per day? What drives arrival, and what is the other system's own capability?

## Governance

**P-GOV-01** · *Trigger: personal, special-category, financial or regulated data is in scope.*
Does a data protection assessment exist? What evidence must the system be able to produce, in what format, and how far back — and which mechanism produces it?

**P-GOV-02** · *Trigger: a clause mentions encryption keys, key custody or vendor access.*
Must keys be under the organisation's control? Is approval required before a vendor engineer may access anything, and who holds custody?

**P-GOV-03** · *Trigger: network policy is recorded, or an endpoint sits on a private network or on-premises.*
Is access required to be restricted to a corporate network or private connectivity? Who runs that connectivity today, how many users are in enforcement scope, and does the rule apply to machine identities too?

**P-GOV-06** · *Trigger: data is recorded as not permitted to leave a boundary.*
Is the requirement to *prevent* movement or to *detect* it? Must export to a spreadsheet be stopped as well?

**P-GOV-07** · *Trigger: business users are expected to build or change this themselves.*
What governs that? Is there a route from a personal experiment to a supported solution — which environments, which release-gate mechanism, and what lead time does the estate impose?

**P-GOV-10** · *Trigger: the process is validated, or under formal change control.*
Must behaviour stay frozen between releases? Does a change to the underlying platform require revalidation, and what mechanism detects that a change happened?

**P-GOV-13** · *Trigger: a portability, second-source or exit requirement is recorded.*
Which layers must be able to move, to what, and has anyone costed it?

## Financial

**P-FIN-01** · *Trigger: a control, an operating tier or a recovery commitment is recorded as mandated.*
Is it funded, and by whom? What happens to the requirement if it is not?

**P-FIN-02** · *Trigger: the audience is external, anonymous or unpredictable.*
Is the population knowable in advance? How would you count one person who visits from three devices?

**P-FIN-05** · *Trigger: an external party would build it.*
What is inside the price and what is not — running it, supporting it, monitoring it, tracking platform change, and the exit?

**P-FIN-06** · *Trigger: the budget is tight, or cost sensitivity is recorded as high.*
What would you drop first, and what is the smallest version that still delivers value?

**P-FIN-07** · *Trigger: volume, audience or machine work is expected to grow materially.*
What is the growth rate, what is it based on, and at what point would the economics change shape?

---

# Reachable outcomes

This pack is named for one platform. The questions must not be shaped to make that platform look suitable. Each outcome below must stay reachable from the evidence these questions produce:

- **it fits** — positive answers across the core patterns, no constraint engaged;
- **it fits with stated, funded conditions** — Q-BUS-02, Q-GOV-06, P-OPS-09, P-FIN-01;
- **another kind of technology is preferable** — for the whole scope, for one named responsibility, or on economics — Q-GOV-02 (where the runtime must execute), P-DAT-02 (atomicity across systems), P-OPS-03 (real compute), P-GOV-13 (portability), Q-DAT-08 + P-GOV-07 (an existing capability already owns it), Q-FIN-03 + P-FIN-01 (a mandated control that is unfunded);
- **an alternative is sufficient and this platform is not excluded** — Q-DAT-08 + P-GOV-07 (something already owns it), Q-USR-01 (how small the population really is), Q-DAT-03 + Q-DAT-05 (how little the access and volume requirement actually asks for), Q-FIN-06 (what is already held and paid for): the lighter answer stands on its own, with the condition that would force a revisit stated;
- **process change without new technology is preferable** — P-BUS-01, P-BUS-02, Q-BUS-03, Q-FIN-01;
- **doing nothing, or deferring, is preferable** — Q-FIN-02, Q-FIN-03 + P-FIN-01, Q-BUS-04;
- **the decision is blocked and more evidence is required** — any decision-blocking Unknown that cannot be closed in the window, any conflicted value that is decision-critical, and any exclusion resting on an assumption rather than on confirmed, current evidence. A stated block, naming the evidence and what each resolution would produce, is a legitimate result — not a failure to decide.

A finding may reach more than one of these at once, each bound to its own scope: the outcome for an application and the outcome for one responsibility inside it are separate answers and must not be collapsed.

Discovery records requirements and constraints. It does not emit fit verdicts, exclusions or platform recommendations — those are Options outputs (`library/kernel/phases.md`; `.claude/rules/no-tech-mention-before-options.md`).
