---
description: Render 1 or all 6 deliverables from the synthesis topic packs + decisions.
argument-hint: "[deliverable|--all] [--dry-run]"
---

Invoke the `aisa-render` skill with the arguments provided.

The skill runs two coverage checks it never merges: **before** producing each deliverable,
the pre-render check of the authorities that deliverable declares (`coverage.py check
--stage render --deliverable <id>`); **after**, the projection review of the file written.
A missing authority is a skip with its reason, never a gap — see
`library/kernel/coverage-contract.md` §8.2. Do not re-derive the algorithm here.

Args: $ARGUMENTS
