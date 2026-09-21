# compliance-officer — universal constraints

## RGPD (Regulamento Geral de Proteção de Dados — PT GDPR)
Applies to every process handling PII (employees, customers, suppliers). Surface in `regulations_applicable` even when "obvious". The new system must support: right of access, right of erasure, right of portability, data minimisation, purpose limitation.

## Financial audit retention
Portuguese Código Comercial: 10 years for accounting records. SOX-equivalent obligations for listed entities. Surface as a `retention_legal` floor.

## Public-sector accessibility floor
For internal tools in the Portuguese public sector: Decreto-Lei 83/2018 (WCAG 2.1 AA, keyboard, screen-reader, contrast). Not enforced as strictly internally as externally, but the audit floor is non-zero.

## Separation of duties (SoD)
Financial, procurement and HR processes **frequently** carry a split obligation — submitter ≠ approver, requester cannot self-approve. It is a hypothesis to test against the rule in scope, never a default constraint: cite the regulation, contract or policy that imposes it. Cited, it is a permission model the target must enforce (`plano de imposição de permissões`). Uncited, it is not a governance finding.

## Approval as process behaviour
Where approval is behaviour of the process in scope, what the target needs is structural: the states, the transitions, the **role** authorised at each, and the threshold that routes between them. Ask for the organisation's actual thresholds and record them with their source — a remembered figure is worse than an open question. Where approval is not process behaviour (project sign-off, release sign-off, stakeholder signature), it is outside this engagement and no row is written.

## Connector / data-handling policy
For low-code platforms with tenant-level DLP (the case for the `pp` pack and several others), each tenant has policies classifying connectors as Business / Non-Business / Blocked. Surface any required external integration as needing DLP review before /decide. State the need in policy terms ("the integration must be classified as Business by DLP") rather than naming the platform.

---

Same reading rule as `anti-patterns.md`: a constraint here is a **hypothesis with its
requirement and its technical consequence**, never a standing order. It fires where the
requirement is present; it says which of the eight axes moves; and an organisational gap
becomes the target's requirement, never pending work.
