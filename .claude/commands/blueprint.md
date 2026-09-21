---
description: Produce the UX blueprint (designed screen architecture with SU provenance) from the decision + pack rules; iterate with business feedback until approved.
argument-hint: "[--option <O-NNN>] [--refresh]"
---

Invoke the `aisa-blueprint` skill with the arguments provided.

The skill runs two mechanical checks around the version and never merges them: the
structural check (`blueprint-contract.md` → *Validação estrutural*) and the coverage review
(`coverage-contract.md`) — the reconciliation before producing, the review of the concrete
version after. A version with gaps is still produced and still discussed; it is only not
announced ready for approval.

Approval is the business's, asked explicitly through `AskUserQuestion` — no check here
approves anything, and approvals already recorded are never revoked.

Args: $ARGUMENTS
