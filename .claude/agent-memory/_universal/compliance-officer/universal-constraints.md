# compliance-officer — universal constraints

## RGPD (Regulamento Geral de Proteção de Dados — PT GDPR)
Applies to every process handling PII (employees, customers, suppliers). Surface in `regulations_applicable` even when "obvious". The new system must support: right of access, right of erasure, right of portability, data minimisation, purpose limitation.

## Financial audit retention
Portuguese Código Comercial: 10 years for accounting records. SOX-equivalent obligations for listed entities. Surface as a `retention_legal` floor.

## Public-sector accessibility floor
For internal tools in the Portuguese public sector: Decreto-Lei 83/2018 (WCAG 2.1 AA, keyboard, screen-reader, contrast). Not enforced as strictly internally as externally, but the audit floor is non-zero.

## Separation of duties (SoD)
For any financial or procurement process: the submitter cannot also be the approver. For HR processes: the requester cannot self-approve their own changes. Surface as a `separation_of_duties` constraint by default.

## Sign-off ladder
For most Portuguese mid-cap procurement processes: department head + finance + (if > 10k€) executive. Confirm the actual ladder; the new system encodes it.

## Connector / data-handling policy
For low-code platforms with tenant-level DLP (the case for the `pp` pack and several others), each tenant has policies classifying connectors as Business / Non-Business / Blocked. Surface any required external integration as needing DLP review before /decide. State the need in policy terms ("the integration must be classified as Business by DLP") rather than naming the platform.
