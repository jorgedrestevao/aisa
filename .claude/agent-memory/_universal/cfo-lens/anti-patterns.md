# cfo-lens — anti-patterns (universal)

## "It pays for itself"
Sponsor-stated payback under 6 months for a digitalization project is almost always wrong. Real-world payback for low-code internal tools sits at 12-24 months on a fully-loaded cost basis. Anchor the claim or downgrade to Assumed.

## As-is cost = "we'll figure it out"
The as-is cost is the baseline the chosen option must beat. If the engagement reaches /options without an as-is cost estimate → raise Critical Unknown. The financial story has no anchor without it.

## Licensing modelled at the per-user list price
Vendor list prices for low-code platforms are negotiation starting points. Volume + multi-product + enterprise agreements typically deliver 30-50% off list. For the SU, capture the *expected licensing-cost magnitude* without naming any platform; the solution-architect names vendors at Options. Flag the negotiation factor as an Assumption with `base: list-price-baseline pattern; real cost depends on enterprise agreement`.

## Internal cost forgotten
Build cost ≠ total cost. Add: internal change-management time, training, business-team time during UAT, ongoing administration. Surface as `internal_chargeback_model` and probe.

## Cost-of-delay invisible
Sponsors rarely articulate the cost of delay until it's quantified. "Each month we wait, X happens" — anchor X explicitly. Without it, do-nothing looks free; doing-nothing-as-an-option becomes the strongest "alternative" by default.
