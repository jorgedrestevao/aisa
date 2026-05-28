# compliance-officer — anti-patterns (universal)

## Separation of duties absent
When the same role can both submit and approve a request, the audit-readiness of the as-is is already weak. The new system must enforce SoD or the engagement inherits the gap. Surface as Risky if not already in the SU.

## Sign-off ladder is "ad-hoc"
"Whoever is available approves" → no audit chain. The new system cannot enforce a ladder that doesn't exist; either the sponsor must declare it explicitly during Discovery, or it surfaces as Unknown/Critical.

## Offline + sensitive data
A user-stated "offline" need combined with a data-lens classification of "Confidential" or above is a **Conflicted** row, not a Risky. The collision is intrinsic — only the sponsor can resolve it at /decide (offline subset only / no offline / re-classify). Do not silently choose.

## DLP-blind design
For organisations with tenant-level DLP (data-loss-prevention) policies governing external integrations: every required external data-flow needs a DLP classification check up front. A discovery that assumes "we can just add an integration to X" without surfacing the DLP question lands the engagement in a 4-8 week wait while IT changes policy. Always probe the DLP classification of any external integration the as-is implies.

## Audit "after-the-fact"
Designing audit as a quarterly export rather than per-event is a discovery anti-pattern. The audit-on-Approve / Audit-on-Delete / Audit-on-Export pattern (see `library/packs/pp/domain-knowledge/security-patterns.md`) must be in the design from day 1.
