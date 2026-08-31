---
name: aisa-answer
description: Record an answer or resolution for a Shared Understanding row (Unknown, Conflicted, Assumed or Risky) and apply the state transition from library/kernel/states.md. The answer is kept verbatim in answers.md; the resolved content re-enters the SU as new row(s) with `was <id>`; the original row is marked resolved. Works in any phase — used for Discovery answers and for prototype-validation feedback alike.
---

# aisa-answer

## Usage

`/answer <id> "<answer>" [--source "<who/what>"] [--to confirmed|assumed|risky]`

- `<id>`: the SU row being resolved — `U-NNN` (Unknown), `X-NNN` (Conflicted), `A-NNN` (Assumed, being validated), or `R-NNN` (Risky, being closed).
- `"<answer>"`: the answer/resolution, verbatim — do not paraphrase away specifics (numbers, names, thresholds).
- `--source`: who or what answered (default: "sponsor"). Becomes part of the evidence.
- `--to`: force the target state. Default inference: a direct sponsor/document statement → `Confirmed`; a reasonable-but-unverified statement → `Assumed`; an answer that reveals a material uncertainty → `Risky`.

## State transitions applied (per `library/kernel/states.md`)

| From | Default to | Notes |
|---|---|---|
| Unknown | Confirmed (or Assumed/Risky via `--to` or inference) | 1 new row |
| Conflicted | Confirmed ×N | One new row **per resolved side** (e.g., "multi-level >10k€, 1-step <10k€" → 2 rows) |
| Assumed | Confirmed | Validation of the assumption |
| Risky | Confirmed | Mitigation done or risk resolved |

## Execution steps

1. Resolve the engagement root (`$AISA_ENGAGEMENTS_ROOT/<slug>` or `projects/<slug>`) and read `shared-understanding.md` + `_state.json` (current round).
2. Locate the row `<id>` in its section. If not found → stop and list the open ids of that prefix. If already marked `resolved → …` → stop and say so.
3. **Record the answer verbatim** in `<engagement>/answers.md` (create with header `# Answers — <slug>` if missing):
   ```markdown
   ## <id> — <date ISO>
   - **Pergunta/conflito**: <original row text>
   - **Resposta**: <verbatim answer>
   - **Fonte**: <source>
   - **Transição**: <id> → <new-id(s)> (<target state>)
   ```
4. **Append the new row(s)** to the target section of the SU: next free id, `lens` = the original row's lens, claim = the answered fact (specifics preserved), `evidência` = `USER_ANSWER <date> — <source> (was <id>)`, `ronda` = current round. For Conflicted, create one row per resolved side.
5. **Mark the original row resolved**: append ` — resolved → <new-id(s)>` to the original row's last column. Never delete the row — it stays for audit (append-only rule; explicit state transitions are the one sanctioned edit).
6. Update the SU header `Última actualização`. Append one line to `council-log.md`: `<round> — /answer <id> → <new-id(s)> (<state>)`.
7. Output: "`<id>` resolved → `<new-id(s)>` (`<state>`). Open critical items remaining: <N> Unknown, <N> Conflicted. Next: `/status`, more `/answer`, or `/round`."

## Hard rules

1. **Verbatim in, structured out.** answers.md keeps the raw answer; the SU row carries the extracted fact. Never lose numbers or thresholds in the extraction.
2. **Never delete or rewrite** the original row beyond the `resolved →` marker.
3. **No silent upgrades**: an answer that is hearsay or inference goes to Assumed with the basis declared, not Confirmed — even if the user typed it confidently. Say so when downgrading.
4. If the answer itself surfaces a NEW conflict or risk, additionally append the corresponding Conflicted/Risky row (new id, this round) and mention it in the output.
