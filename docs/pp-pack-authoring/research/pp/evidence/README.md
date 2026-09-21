# Power Platform Research Evidence

This directory contains the evidence collected during Power Platform research.

Each file represents a research topic.

The evidence corpus is NOT the final aisa Power Platform pack.

---

## File naming

Use descriptive names.

Examples:

- `platform-suitability.md`
- `dataverse.md`
- `power-automate.md`
- `integration.md`
- `security.md`
- `alm.md`
- `performance.md`
- `licensing.md`
- `anti-patterns.md`

---

## Structure of each research file

Each finding should use this structure:

## Finding

Short statement of what was discovered.

### Classification

One of:

- FACT
- RECOMMENDATION
- CONSTRAINT
- TRADE-OFF
- RISK
- ANTI-PATTERN
- DECISION CRITERION
- PATTERN

### Evidence

Explain the evidence supporting the finding.

### Why it matters

Explain why this matters for deciding or designing a solution.

### Decision impact

Explain which architectural or solution decision this could influence.

### Conditions

Describe conditions, exceptions or boundaries.

### Confidence

HIGH / MEDIUM / LOW

### Sources

List the supporting sources.

---

## Important rules

Do not write generic summaries.

Capture knowledge that can influence decisions.

Prefer:

"High transaction volume can make Power Automate unsuitable
for synchronous processing because..."

over:

"Power Automate is a workflow automation platform."

---

## Negative evidence

Negative findings are especially important.

Explicitly record:

- limitations;
- failure conditions;
- anti-patterns;
- scalability problems;
- licensing problems;
- governance problems;
- integration problems;
- cases where another technology is preferable.

---

## Unknowns

If something cannot be established confidently,
record it as:

UNKNOWN

Do not fill gaps with assumptions.

---

## Conflicts

If sources disagree, record:

CONFLICTED

and explain the disagreement.

---

## Research maturity

A topic is not considered complete merely because
documentation has been found.

It should answer:

1. What can Power Platform do?
2. What are its limits?
3. When should it be used?
4. When should it not be used?
5. What requirements change the answer?
6. What alternatives exist?
7. What architectural decisions follow from those requirements?