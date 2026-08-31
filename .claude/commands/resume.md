---
description: Resume an engagement in a fresh session — reads _state.json, shows where things stand, and names the exact next command.
argument-hint: "[slug]"
---

Invoke the `aisa-status` skill (for the engagement given in the arguments, or the one found in the engagements root). After showing the status summary, end by naming the exact next command for the current phase and open items — e.g. `/answer <id> "…"` for open critical Unknowns/Conflicted, `/round` for another Discovery pass, `/frame`, `/options`, `/decide`, `/blueprint`, or `/render --all`. This command is the session re-entry point; do not start new analysis, only reorient.

Args: $ARGUMENTS
