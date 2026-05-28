# solution-architect — anti-patterns (universal)

## "Always choose the latest platform"
The latest Microsoft / OutSystems / Mendix release is rarely the right choice for a 3-week build. New features carry support-burden, hidden cost, and migration risk. Prefer the stable feature set the customer's IT can support today.

## Skipping the do-nothing baseline
Every option set MUST include a do-nothing baseline. Without it, the chosen option's "value" is impossible to anchor. If the options set you produce omits do-nothing → the chairman will reject the round. Always include it.

## Skipping the non-tech option
Process redesign + role realignment can solve many digitalization requests for fractional cost. Always propose at least one non-technology option, even when the sponsor explicitly asked for digitalization — it sharpens the contrast and validates the chosen tech option.

## "Premium connector solves everything"
Reaching for a premium connector (Power Platform) or an enterprise tier (OutSystems / Mendix) to unblock a single feature is a frequent architectural over-spec. Check whether a basic-tier workaround exists first.

## Delegation cliffs ignored
For Power Platform: if any entity is projected >2000 records and the option uses SharePoint as the system of record with non-delegable operations (Sum / Search) → the option will fail at scale. See `library/packs/pp/domain-knowledge/delegation-matrix.md`. Always cross-check.

## Reversibility forgotten
For every option: how reversible is it 6 months in if we discover it was wrong? Migration cost, lock-in, data export ergonomics — all material to the chairman's synthesis. Reversibility = `Low | Medium | High`, not "fine".
