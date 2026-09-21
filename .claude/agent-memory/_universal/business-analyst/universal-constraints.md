# business-analyst — universal constraints

Standing constraints that apply across most engagements. Probe each at least once per Discovery.

## Regulatory weight
- **GDPR / data protection**: any process handling PII has audit and right-to-erasure implications. Surface this even when the sponsor sees it as "obvious", so it lands as an SU row.
- **Sectoral**: financial services (BdP / EBA), energy (ERSE), telecom (ANACOM) — sector-specific reporting obligations shape "audit_requirements" and "retention_legal".

## Cost envelope, not approval paperwork
- Ask for the organisation's actual spend thresholds and record them with their source — the figure varies by organisation and year, and a remembered one is worse than an open question.
- What survives into the technical decision is the **envelope**: which option classes sit inside it and which do not. Where the likely band straddles the envelope, that is a real question on `custo`, and the answer changes which candidates survive.
- Who signs, and whether "authority to start" covers "authority to deploy", is administration. It does not gate `/decide` and it is not written as a row.

## Roles the target must serve
- Requester, business owner, end-user, operator, administrator. What the design needs from each is the **role**, what it does, on what data, and where that is enforced — never a person's name (P-21). A name is a source of information, never a requirement.
- Where a role in the as-is has no counterpart in the target, say so: that is a design decision, not a gap in the organisation.

## Prior-attempts archaeology
- Any "this was tried before" claim deserves a documented reason. The most common silent killers are: integration cost overrun, vendor lock-in fear, change-management push-back. Surface the actual reason; the new option must beat it explicitly.

---

Same reading rule as `anti-patterns.md`: a constraint here is a **hypothesis with its
requirement and its technical consequence**, never a standing order. It fires where the
requirement is present; it says which of the eight axes moves; and an organisational gap
becomes the target's requirement, never pending work.
