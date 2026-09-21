# cfo-lens — universal constraints

## The rate is an engagement fact, never a standing number
Costing as-is work, build effort or operating burden needs a labour rate. **This file does not supply
one, and neither does any other standing memory.** A rate carried here would be undated, unsourced and
indistinguishable from market truth the moment a persona quoted it.

```text
delivery or as-is labour rate needed
  → use the engagement-provided / approved internal rate, and carry its provenance
  → unavailable and material  → Unknown (custo · swing · named owner), or a measurement obligation
  → unavailable and the decision model permits assuming it
                              → Assumed, with an explicit basis and an explicit validator
```

An `Assumed` rate is never silently treated as market truth, and it never settles anything the
evidence-grade rule reserves for `Confirmed` and current evidence (`library/packs/pp/decision-tree.md` §4).

## Build effort bands
- **Small** = 1–4 weeks.
- **Medium** = 4–12 weeks.
- **Large** = 12+ weeks.

Coarse duration bands for `/options`, where the honest answer is a band and a point estimate would be
false precision. They carry **no** money and **no** hour conversion: implementation effort is calculated
once, by the Estimate deliverable (`owns_calculation: true`), from the Implementation Specification's
inventory and `library/packs/pp/domain-knowledge/craft/estimation-model.md`. Any cost attached to a band
comes from the engagement's own rate, with its provenance.

## CAPEX vs OPEX
For most cloud / SaaS digitalization spend: OPEX. For on-prem or significant first-year licensing
pre-payment: CAPEX. Confirm with the sponsor; the answer drives approval thresholds.

## Spend envelope
Every organisation has spend thresholds — a department level, a finance level, an executive level.
**Ask for the actual thresholds and record them with their source**; they vary by organisation, by year
and by spend type, and a remembered figure is worse than an open question. What survives into the
technical decision is the **envelope**, not the ladder: which option classes sit inside it. Where the
likely band straddles it, that is a question on `custo` whose answers change which candidates survive.
Which role signs is administration — it never blocks the round and never becomes a row.

## ROI floor
For internal-tool digitalization a positive ROI is usually expected within about two years, and inside a
year is excellent. Where a tool cannot project a return inside that horizon, it needs a non-financial
justification — compliance, risk reduction, an obligation with a date — anchored in the SU. Treat the
horizon as the sponsor's expectation to confirm, not as a threshold this file sets.

## Cost of delay
Where doing nothing is plausible, quantify it: per-month cost of doing nothing = (monthly volume ×
marginal cost per case × inefficiency factor). Anchor every input to operations + data lens claims, and
to the engagement's own rate. Doing nothing and doing it manually are then priced on the same dimensions
as every other candidate, and are frequently the honest answer. Where the evidence makes them
implausible, say so with ids instead of carrying a candidate nobody can choose.

---

Same reading rule as `anti-patterns.md`: a constraint here is a **hypothesis with its
requirement and its technical consequence**, never a standing order. It fires where the
requirement is present; it says which of the eight axes moves; and an organisational gap
becomes the target's requirement, never pending work.
