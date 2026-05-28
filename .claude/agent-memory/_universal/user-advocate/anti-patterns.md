# user-advocate — anti-patterns (universal)

## "Users will adapt"
The sponsor's belief that users will train into the new tool inversely correlates with adoption. When a sponsor says this with no change-management plan, raise Risky on `adoption`. The mitigation is almost always: shadow a real user for an hour and revisit the assumption.

## One persona for everyone
When discovery emits one persona for a process touched by ≥3 roles, the lens is generalising and will miss the load-bearing edge cases. Push for distinct personas per role; if the sponsor resists, raise Unknown rather than collapsing.

## Mobile-need stated without device-context check
"It needs to work on a phone" without confirming the device, connectivity, and where-the-work-happens is a frequent over-spec that drives the build's complexity 2× higher than needed. Surface as Unknown on `devices_and_connectivity` even when "mobile" was on the request.

## Accessibility framed as a stretch goal
WCAG-level accessibility for an internal tool used by 12 people may be a stretch. WCAG for a 2000-user customer-facing tool is non-negotiable. Anchor the requirement to user count + audience.

## "What would obviously-better look like?" answered by the sponsor
The sponsor's "obviously-better" almost never matches the user's. If the desired-experience answer comes only from the sponsor, raise an Unknown specifically tagged for end-user validation.
