# decisions.md — fixture excerpt (D-002 shape)

## D-002 — Adopt O-004 — purpose-built platform application, whole solution

- **Chosen option**: O-004
- **Conditions**:
  - master-data owner named + minimal change control — owner: sponsor / governance
  - key cleanup funded before the first migration
  - audit / segregation of duties / sign-off ladder designed from scratch, not inherited from current practice
- **Justification**: O-004 closes every clause of the frame (D-001) — workbook fragility (C-041), master-data ownership (R-006), auditability (R-005) and the sponsor's requirement that continuity be solved "by construction" (C-029).
- **Accepted risks**: R-001, R-009, R-010, R-012
- **Tripwires**:
  - TW-1: build effort exceeds the initial estimate without an explicit scope review → stop and re-evaluate
