---
description: Retomar um engagement numa sessão nova — onde está, o que falta, e o comando exacto a seguir. Reorienta; não analisa.
argument-hint: "[slug]"
---

Invoke the `aisa-status` skill for the engagement named in the arguments, or the one found
in the engagements root.

**Show four of its seven blocks, in this order** — this command re-enters a session, it does
not review the engagement. Language: the column *como se diz ao utilizador* of
`library/kernel/glossary.md`, exactly as `/status` prints it (kernel terms and ids only between
parentheses, after the business phrase).

1. **Onde estamos · O que falta para o próximo passo · O que tens de fazer tu** — the three
   opening lines.
2. **Alerta** — only when there is one: a revision condition fired (named FIRST; its command
   is `/revisit TW-n`), a grave fact expired, the topic summaries predate the approval.
3. **O que falta para o próximo passo** — abbreviated: the top-3 items in one line each
   (tema · quem · comando). No "também importa" list.
4. **Para retomar** — the derived read set for the current phase (`Read to resume`).

Skip the other blocks (the meeting agenda, the delta since the last round, the confidence
counts); `/status` is where those belong. Do not start new analysis, do not formulate sponsor
questions, do not read Domain Knowledge. Close with the `A seguir:` line — the human step, if
any, then the exact command: `/answer <id> "…"`, `/round`, `/frame`, `/options`, `/decide`,
`/blueprint`, `/blueprint --refresh`, `/synthesize` or `/render --all`, whichever the
milestone actually names.

A fresh session needs no previous transcript: everything above is derived from
`_state.json` and the repository state, through the same model `/status` reads.

Args: $ARGUMENTS
