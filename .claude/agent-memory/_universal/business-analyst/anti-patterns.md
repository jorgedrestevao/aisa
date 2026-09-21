# business-analyst — anti-patterns (universal)

Patterns seen often enough across engagements to flag automatically when they show up. Each item explains the failure mode so the lens raises an Unknown/Risky/Conflicted instead of letting it slide.

## How to read this file — binding

Nothing here opens a question by itself. Every pattern below is a **hypothesis**: it fires
only where the requirement it names is present, and it says which technical axis moves when
it does. Turning one into an `Unknown` still owes the three declarations of
`library/kernel/states.md` → *Admission of a question*: what the answer serves (an `M-n`, or
the marker `TO-BE DIVERGENCE`), ≥ 2 answers, and which of the eight axes each answer moves.
Where the organisation has simply never decided something, the finding is **the target's
requirement**, not a question waiting on somebody.

## Run-cost nobody has priced
Procurement-driven requests frequently surface unfunded run-cost in month three. What matters technically is not who was in the room: it is whether the **cost envelope** is known well enough to tell which option classes are reachable. **Fires when**: the candidate classes differ materially in run cost and no envelope is stated. **Technical consequence**: `custo`, and through it which classes survive. Written that way it is a real question; written as "has Finance seen it" it is not.

## The declared urgency does not match the volume signal
Sponsor says "urgent" but `operations.volume_and_peaks` resolves to a few cases per month. Either the urgency anchors on a quality/audit failure (not throughput) or the urgency is performative. Raise a Conflicted (`partes: sponsor∧operations`) and ask the sponsor to anchor the urgency to a measurable event.

## Prior attempts that "failed" with no post-mortem
"This was tried before and didn't work" with no documented reason is worth reopening for one thing only: the **technical** reason, where there was one — an integration that did not exist, a volume that broke it, a cost that landed. That reason is evidence about an axis and belongs in the SU. A veto or a lost budget is history, not a constraint on the target: record it as context, never as a Risky the engagement must clear.

## A system the requester does not control
When the request lives outside IT but touches a system another team runs, the constraint is technical, not political: what that team's ownership permits — the integration mechanism it exposes, the identity that may call it, the change window, whether a new component may sit inside its boundary. **Fires when**: an option depends on that system. **Technical consequence**: `componentes`, `padrão arquitetural`, `plano de imposição de permissões`. The person who would object is not the finding; the boundary they own is.

## "Just digitalise this" with no measurable target
A request that frames the goal as "have a system to do X" rather than "reduce Y by Z% by Q4" rarely survives /decide intact. Push back during business round 1; if no measurable target lands → record the gap, do not invent one.
