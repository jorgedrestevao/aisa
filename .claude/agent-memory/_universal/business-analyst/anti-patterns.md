# business-analyst — anti-patterns (universal)

Patterns seen often enough across engagements to flag automatically when they show up. Each item explains the failure mode so the lens raises an Unknown/Risky/Conflicted instead of letting it slide.

## Procurement-led without the CFO in the room
Procurement-driven digitalization requests that have not been seen by Finance frequently break at the budget approval gate, or surface unfunded run-cost in month three. If the requester is Procurement and `financial.sponsor_authority` is not Confirmed → raise an Unknown on the financial lens explicitly.

## The declared urgency does not match the volume signal
Sponsor says "urgent" but `operations.volume_and_peaks` resolves to a few cases per month. Either the urgency anchors on a quality/audit failure (not throughput) or the urgency is performative. Raise a Conflicted (`partes: sponsor∧operations`) and ask the sponsor to anchor the urgency to a measurable event.

## Prior attempts that "failed" with no post-mortem
"This was tried before and didn't work" without a documented reason almost always hides a stakeholder veto or a budget loss. Mark as Risky with `mitigação: surface the actual reason before committing to this engagement`.

## The shadow stakeholder is the IT manager
When the request lives outside IT but touches a system IT owns, the IT manager is a veto-holding shadow stakeholder. Their absence from kick-off is the single most common reason a discovery's chosen option later gets blocked. Always raise as an Unknown on `decision_authority`.

## "Just digitalise this" with no measurable target
A request that frames the goal as "have a system to do X" rather than "reduce Y by Z% by Q4" rarely survives /decide intact. Push back during business round 1; if no measurable target lands → record the gap, do not invent one.
