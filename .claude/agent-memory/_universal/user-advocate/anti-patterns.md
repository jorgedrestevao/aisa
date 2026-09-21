# user-advocate — anti-patterns (universal)

## How to read this file — binding

Nothing here opens a question by itself. Every pattern below is a **hypothesis**: it fires
only where the requirement it names is present, and it says which technical axis moves when
it does. Turning one into an `Unknown` still owes the three declarations of
`library/kernel/states.md` → *Admission of a question*: what the answer serves (an `M-n`, or
the marker `TO-BE DIVERGENCE`), ≥ 2 answers, and which of the eight axes each answer moves.
Where the organisation has simply never decided something, the finding is **the target's
requirement**, not a question waiting on somebody.

## "Users will adapt"
The sponsor's belief that users will train into the new tool inversely correlates with adoption. It becomes a finding here when it has a **design** consequence: the assumption is usually hiding a step the tool must absorb rather than teach, and that changes surface, screen count and effort (`tecnologia` · `esforço de alto nível`). Shadow a real user for an hour and write what the tool must do. Change management itself is not this engagement's work.

## One persona for everyone
When discovery emits one persona for a process touched by ≥3 roles, the lens is generalising and will miss the load-bearing edge cases. Push for distinct personas per role; if the sponsor resists, raise Unknown rather than collapsing.

## Mobile-need stated without device-context check
"It needs to work on a phone" without confirming the device, connectivity, and where-the-work-happens is a frequent over-spec that drives the build's complexity 2× higher than needed. Surface as Unknown on `devices_and_connectivity` even when "mobile" was on the request.

## Accessibility framed as a stretch goal
WCAG-level accessibility for an internal tool used by 12 people may be a stretch. WCAG for a 2000-user customer-facing tool is non-negotiable. Anchor the requirement to user count + audience.

## "What would obviously-better look like?" answered by the sponsor
The sponsor's "obviously-better" almost never matches the user's. Where the two readings would build **different things** — a different surface, a different flow, a different device — that is a real question, and the swing names both. Where they differ only in emphasis, write the sponsor's as `Assumed` with its basis and validate it when a user is in the room. Not every unvalidated preference is an open question.
