# solution-architect — anti-patterns (universal)

## How to read this file — binding

Nothing here opens a question by itself. Every pattern below is a **hypothesis**: it fires
only where the requirement it names is present, and it says which technical axis moves when
it does. Turning one into an `Unknown` still owes the three declarations of
`library/kernel/states.md` → *Admission of a question*: what the answer serves (an `M-n`, or
the marker `TO-BE DIVERGENCE`), ≥ 2 answers, and which of the eight axes each answer moves.
Where the organisation has simply never decided something, the finding is **the target's
requirement**, not a question waiting on somebody.

## "Always choose the latest platform"
The latest Microsoft / OutSystems / Mendix release is rarely the right choice for a 3-week build. New features carry support-burden, hidden cost, and migration risk. Prefer the stable feature set the customer's IT can support today.

## Dropping the do-nothing baseline without saying so
Where doing nothing is plausible, it anchors the chosen option's value — without it, "value" floats. Where it is not plausible (a dated compliance finding, a system being switched off), say that, with ids, instead of carrying a candidate nobody can choose. The failure is the **silent** absence: a set that omits it with no reason leaves the chairman unable to tell "evaluated and ruled out" from "never considered".

## Dropping the process-change option without saying so
Process redesign + role realignment solves many digitalization requests for fractional cost, so check for it even when the sponsor explicitly asked for digitalization. Same rule as above: on the table where plausible, declared with ids where not. Proposing one that the evidence does not support is not contrast — it is padding.

## Arguing with an imposed technology
Where the organisation has fixed the platform, the option set is generated **inside** that boundary: compatible patterns, plus external components where the boundary is permitted. Proposing another platform is not architectural courage; it burns the round on a choice nobody is making. The imposition is itself a rule, so put a platform alternative on the table only as *viable if the rule is changed*, with the rule's id, what changing it costs and who can change it.

## Deleting an option an organisational rule blocks
A rule that makes an option unavailable does not make it non-existent. Return it as *viable if the rule is changed* — rule, condition, impact, cost, risk, who can change it, status. The owner cannot choose to change a rule for an option they were never shown.

## A composed architecture whose permission nobody checked
Splitting work across an external component only works where the organisation permits that boundary — a subscription to host it, an identity to run it, a team to operate it, a network path to reach it. **That permissibility is a constraint to validate before recommending, never an assumption.** Say which of the four the composition needs and which is unverified; where one is missing and the rule could change, the option stays on the table as *viable if the rule is changed*, with the rule's id, cost and who can change it. An unchecked boundary is a recommendation resting on someone else's permission.

## "Premium connector solves everything"
Reaching for a premium connector (Power Platform) or an enterprise tier (OutSystems / Mendix) to unblock a single feature is a frequent architectural over-spec. Check whether a basic-tier workaround exists first.

## Delegation cliffs ignored
For Power Platform: an access path whose query is not delegable to its store **silently truncates** — a correctness failure, not a slow one — and the exposure grows with the entity. Where an option puts a growing entity behind a non-delegable filter, sort or aggregate, cross-check the access path before accepting the option. The platform boundary (which operations delegate per store, the paging ceiling, what silently truncates) is owned by `library/packs/pp/domain-knowledge/data/query-and-delegation.md` — read the figure there at the decision date rather than carrying one here. Note also that **delegation-safe ≠ fast**: correctness and latency are separate questions.

## Reversibility forgotten
For every option: how reversible is it 6 months in if we discover it was wrong? Migration cost, lock-in, data export ergonomics — all material to the chairman's synthesis. Reversibility = `Low | Medium | High`, not "fine".
