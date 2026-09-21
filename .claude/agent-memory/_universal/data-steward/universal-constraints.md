# data-steward — universal constraints

## GDPR right-to-erasure
Any entity containing PII has a right-to-erasure obligation. The target architecture must support deletion + retention timestamps. Surface in `retention_residency` even when the sponsor sees it as obvious.

## Residency by default
For EU operations: residency in the EU is a default constraint. For Portuguese public-sector or regulated industries: residency in PT may be a hard requirement. Probe explicitly.

## Quality typically below sponsor's belief
Sponsors typically estimate data quality at 85-95%. Reality is more often 60-75% on free-text fields and 80-90% on coded fields. Verify against the input artefact rather than accepting the estimate.

## Identifiers are the migration anchor
The migration plan starts and ends with whether the new system can preserve the legacy identifier (or maps it deterministically). If the legacy id is "the row number in the Excel", the migration cost is material — raise Risky.

## Audit retention
For most Portuguese regulated processes: 5-7 years legal retention; for financial processes: 10 years (per Código Comercial). Confirm the floor; default to longest stated obligation.

---

Same reading rule as `anti-patterns.md`: a constraint here is a **hypothesis with its
requirement and its technical consequence**, never a standing order. It fires where the
requirement is present; it says which of the eight axes moves; and an organisational gap
becomes the target's requirement, never pending work.
