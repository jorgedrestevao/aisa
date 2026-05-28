# data-steward — anti-patterns (universal)

## "We'll figure out master data later"
Master data ownership unresolved at /decide is the single most common cause of multi-month build delays. If `master_data_owners` is Unknown at the end of Discovery → raise Critical, not Med.

## Sensitivity classified by intuition
"This data is sensitive" without a formal classification (Public / Internal / Confidential / Restricted) leaks downstream into governance decisions. Probe the explicit class; if absent, raise Unknown rather than letting the engagement default to "Confidential" out of caution.

## "Volume is small"
Self-reported data volumes under 1k records are usually accurate. Over 1k they are usually wrong by 2-5×. Profile the actual input artefact; never accept the volume claim without a count.

## "It lives in the spreadsheet"
A single Excel file as the system of record for a business-critical entity is a load-bearing single point of failure. Raise Risky on `systems_of_record`; the mitigation must address it explicitly in /decide.

## Migration treated as zero-cost
Historical data migration is almost always under-estimated. If the chosen architecture changes the system of record, the migration is a discrete work package; surface it as a Risky if no migration plan is in the SU.
