---
description: "O que falta para o próximo passo? — próximo marco, tripwires, bloqueios com dono e critério de fecho, uma próxima acção, agenda, contagens. --check valida a instalação."
argument-hint: "[--check]"
---

Invoke the `aisa-status` skill with the arguments provided.

The skill runs `library/kernel/tools/dashboard.py --json` first and reads every count,
date, version and reference from that model — it does not recount the Shared Understanding
by hand. What it adds on top is the judgement the model may not make: the tripwire verdict,
each blocker's consequence, the questions phrased from the pack's question bank, and the
next action.

The view reports four separate answers about a design version — structure, coverage,
approval and end to end — and never lets one speak for another. *Ainda não foi conferido* is
neither a pass nor a failure.

Report what the skill produces. Do not resolve rows, run proofs, change phase or approve
anything from here.

Args: $ARGUMENTS
