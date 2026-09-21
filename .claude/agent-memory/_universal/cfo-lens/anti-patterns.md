# cfo-lens — anti-patterns (universal)

## How to read this file — binding

Nothing here opens a question by itself. Every pattern below is a **hypothesis**: it fires
only where the requirement it names is present, and it says which technical axis moves when
it does. Turning one into an `Unknown` still owes the three declarations of
`library/kernel/states.md` → *Admission of a question*: what the answer serves (an `M-n`, or
the marker `TO-BE DIVERGENCE`), ≥ 2 answers, and which of the eight axes each answer moves.
Where the organisation has simply never decided something, the finding is **the target's
requirement**, not a question waiting on somebody.

## "It pays for itself"
Sponsor-stated payback under 6 months for a digitalization project is almost always wrong. Real-world payback for low-code internal tools sits at 12-24 months on a fully-loaded cost basis. Anchor the claim or downgrade to Assumed.

## As-is cost = "we'll figure it out"
The as-is cost is the baseline a do-nothing candidate is priced against. **Fires when**: doing nothing is on the table, or the candidates differ enough in cost that the ranking turns on it. **Technical consequence**: `custo`, and which classes survive. Where neither holds, an order of magnitude with its basis is enough — an `Assumed`, not a Critical. Raising it Critical by default makes a number nobody will use block the round.

## Licensing modelled at the per-user list price
Vendor list prices for low-code platforms are negotiation starting points. Volume + multi-product + enterprise agreements typically deliver 30-50% off list. For the SU, capture the *expected licensing-cost magnitude* without naming any platform; the solution-architect names vendors at Options. Flag the negotiation factor as an Assumption with `base: list-price-baseline pattern; real cost depends on enterprise agreement`.

## Internal cost forgotten
Build cost ≠ total cost. Add: internal change-management time, training, business-team time during UAT, ongoing administration. Surface as `internal_chargeback_model` and probe.

## Cost-of-delay invisible
Sponsors rarely articulate the cost of delay until it's quantified. "Each month we wait, X happens" — anchor X explicitly. Unpriced, delay looks free, and a do-nothing candidate wins on an absence of evidence rather than on evidence. Price it where doing nothing is plausible; where it is not, say why with ids rather than carrying a candidate nobody can choose.
